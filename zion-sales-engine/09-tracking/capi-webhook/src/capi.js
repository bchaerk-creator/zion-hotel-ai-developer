'use strict';
// Envio para a Graph API (Conversions API). Token vai no corpo, nunca em log.
async function sendEvents(cfg, events, fetchImpl = fetch) {
  const url = `${cfg.graphBase}/${cfg.graphVersion}/${cfg.pixelId}/events`;
  const payload = { data: events, access_token: cfg.accessToken };
  if (cfg.testEventCode) payload.test_event_code = cfg.testEventCode;
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), 10000);
  try {
    const res = await fetchImpl(url, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload),
      signal: ctl.signal,
    });
    let body = null;
    try { body = await res.json(); } catch (_) { body = null; }
    const received = body && typeof body.events_received === 'number' ? body.events_received : 0;
    return {
      ok: res.ok && received >= events.length,
      httpStatus: res.status,
      eventsReceived: received,
      fbtraceId: body && body.fbtrace_id ? body.fbtrace_id : undefined,
      errorMessage: body && body.error ? String(body.error.message || 'erro').slice(0, 200) : undefined,
    };
  } catch (e) {
    return { ok: false, httpStatus: 0, eventsReceived: 0, errorMessage: `falha_de_rede:${e.name}` };
  } finally {
    clearTimeout(timer);
  }
}

module.exports = { sendEvents };

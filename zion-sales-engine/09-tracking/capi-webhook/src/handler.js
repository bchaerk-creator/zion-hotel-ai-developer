'use strict';
const crypto = require('node:crypto');
const { buildMap, extract, getPath } = require('./mapping');
const { classify } = require('./classify');
const { buildPurchase, buildRefundEvent } = require('./event');
const { sendEvents } = require('./capi');

function safeEqual(a, b) {
  const ha = crypto.createHash('sha256').update(String(a)).digest();
  const hb = crypto.createHash('sha256').update(String(b)).digest();
  return crypto.timingSafeEqual(ha, hb);
}

function createHandler({ cfg, store, fetchImpl, now = () => Math.floor(Date.now() / 1000), log = () => {} }) {
  const map = buildMap(cfg.adapter, cfg.fieldMapJson);
  const inflight = new Set();
  const reply = (status, json) => ({ status, json });

  return async function handle({ method, url = '/', headers = {}, rawBody = '' }) {
    if (method !== 'POST') return reply(405, { error: 'metodo_nao_permitido' });
    if (!cfg.secret) return reply(500, { error: 'servidor_sem_WEBHOOK_SECRET' });
    if (Buffer.byteLength(rawBody) > cfg.maxBodyBytes) return reply(413, { error: 'corpo_grande_demais' });

    const u = new URL(url, 'http://local');
    const h = {};
    for (const [k, v] of Object.entries(headers)) h[k.toLowerCase()] = Array.isArray(v) ? v[0] : v;

    let body;
    try { body = JSON.parse(rawBody); } catch (_) { return reply(400, { error: 'json_invalido' }); }
    if (!body || typeof body !== 'object') return reply(400, { error: 'json_invalido' });

    let provided = h[cfg.secretHeader];
    if (!provided && cfg.secretQuery) provided = u.searchParams.get(cfg.secretQuery);
    if (!provided && cfg.secretBodyPath) provided = getPath(body, cfg.secretBodyPath);
    if (!provided || !safeEqual(provided, cfg.secret)) {
      log({ level: 'warn', msg: 'segredo_invalido' });
      return reply(401, { error: 'nao_autorizado' });
    }

    const hint = u.searchParams.get(cfg.eventQueryParam) || undefined;
    const record = extract(body, map);
    const verdict = classify(record, cfg, hint);
    const eid = record.eventId ? String(record.eventId) : undefined;
    const nowSec = now();

    if (verdict.decision === 'ignore') {
      log({ level: 'info', msg: 'ignorado', event_id: eid, reason: verdict.reason });
      return reply(200, { status: 'ignored', reason: verdict.reason });
    }

    if (!cfg.pixelId || !cfg.accessToken) return reply(500, { error: 'servidor_sem_pixel_ou_token' });

    if (verdict.decision === 'refund') {
      const key = `refund:${eid}`;
      if (!eid) return reply(200, { status: 'rejected', reason: 'sem_event_id' });
      if (store.get(key)) return reply(200, { status: 'duplicate' });
      const hadPurchase = store.get(`purchase:${eid}`) === 'sent';
      let sentRefundEvent = false;
      if (cfg.sendRefundEvent) {
        const built = buildRefundEvent(record, cfg, nowSec);
        if (!built.error) {
          const r = await sendEvents(cfg, [built.event], fetchImpl);
          if (!r.ok) {
            log({ level: 'error', msg: 'falha_evento_reembolso', event_id: eid, http: r.httpStatus, err: r.errorMessage });
            return reply(502, { error: 'meta_recusou' });
          }
          sentRefundEvent = true;
        }
      }
      store.set(key, 'registered');
      log({ level: 'info', msg: 'reembolso_registrado', event_id: eid, had_purchase_sent: hadPurchase, sent_refund_event: sentRefundEvent });
      return reply(200, { status: 'refund_registered', purchase_had_been_sent: hadPurchase, refund_event_sent: sentRefundEvent });
    }

    // purchase
    const built = buildPurchase(record, cfg, nowSec);
    if (built.error) {
      log({ level: 'warn', msg: 'rejeitado', event_id: eid, reason: built.error });
      return reply(200, { status: 'rejected', reason: built.error }); // 2xx de proposito: nao adianta o ClickMax tentar de novo
    }
    const key = `purchase:${eid}`;
    if (store.get(key) === 'sent') return reply(200, { status: 'duplicate' });
    if (inflight.has(key)) return reply(200, { status: 'duplicate_in_flight' });
    inflight.add(key);
    try {
      const r = await sendEvents(cfg, [built.event], fetchImpl);
      if (!r.ok) {
        log({ level: 'error', msg: 'meta_recusou', event_id: eid, http: r.httpStatus, err: r.errorMessage });
        return reply(502, { error: 'meta_recusou' }); // 5xx: o ClickMax tenta de novo (ate 3x)
      }
      store.set(key, 'sent');
      log({
        level: 'info', msg: 'purchase_enviado', event_id: eid, value: built.event.custom_data.value,
        currency: built.event.custom_data.currency, time_fallback: built.timeFallback, fbtrace_id: r.fbtraceId,
        test_mode: Boolean(cfg.testEventCode),
      });
      return reply(200, { status: 'sent', event_id: eid, value: built.event.custom_data.value, fbtrace_id: r.fbtraceId });
    } finally {
      inflight.delete(key);
    }
  };
}

module.exports = { createHandler };

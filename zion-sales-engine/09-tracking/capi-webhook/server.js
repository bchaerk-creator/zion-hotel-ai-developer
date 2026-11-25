'use strict';
// Servidor HTTP minimo (sem dependencias). Rotas: POST /webhook, GET /health.
const http = require('node:http');
const { loadConfig } = require('./src/config');
const { createStore } = require('./src/store');
const { createHandler } = require('./src/handler');

function createServer(cfg = loadConfig(), deps = {}) {
  const store = deps.store || createStore(cfg.dedupeStore);
  const log = deps.log || ((o) => console.log(JSON.stringify({ ts: new Date().toISOString(), ...o })));
  const handle = createHandler({ cfg, store, fetchImpl: deps.fetchImpl, now: deps.now, log });
  return http.createServer((req, res) => {
    if (req.method === 'GET' && req.url.startsWith('/health')) {
      res.writeHead(200, { 'content-type': 'application/json' });
      return res.end(JSON.stringify({ ok: true }));
    }
    const chunks = [];
    let size = 0;
    let aborted = false;
    req.on('data', (c) => {
      size += c.length;
      if (size > cfg.maxBodyBytes) {
        aborted = true;
        res.writeHead(413, { 'content-type': 'application/json' });
        res.end(JSON.stringify({ error: 'corpo_grande_demais' }));
        req.destroy();
        return;
      }
      chunks.push(c);
    });
    req.on('end', async () => {
      if (aborted) return;
      try {
        const out = await handle({ method: req.method, url: req.url, headers: req.headers, rawBody: Buffer.concat(chunks).toString('utf8') });
        res.writeHead(out.status, { 'content-type': 'application/json' });
        res.end(JSON.stringify(out.json));
      } catch (e) {
        log({ level: 'error', msg: 'erro_interno', err: e.name });
        res.writeHead(500, { 'content-type': 'application/json' });
        res.end(JSON.stringify({ error: 'erro_interno' }));
      }
    });
  });
}

if (require.main === module) {
  const cfg = loadConfig();
  createServer(cfg).listen(cfg.port, () => console.log(JSON.stringify({ msg: 'ouvindo', port: cfg.port, adapter: cfg.adapter, test_mode: Boolean(cfg.testEventCode) })));
}

module.exports = { createServer };

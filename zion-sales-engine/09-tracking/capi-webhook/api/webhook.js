'use strict';
// Exemplo para funcao serverless no estilo Vercel/Netlify (Node 18+). Reaproveita o mesmo handler.
// ATENCAO: memoria de funcao serverless nao e confiavel para idempotencia. Use DEDUPE_STORE em disco
// persistente ou um KV da hospedagem (ver README.md, secao "Idempotencia em serverless").
const { loadConfig } = require('../src/config');
const { createStore } = require('../src/store');
const { createHandler } = require('../src/handler');

const cfg = loadConfig();
const handle = createHandler({
  cfg,
  store: createStore(cfg.dedupeStore),
  log: (o) => console.log(JSON.stringify({ ts: new Date().toISOString(), ...o })),
});

module.exports = async function (req, res) {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const out = await handle({ method: req.method, url: req.url, headers: req.headers, rawBody: Buffer.concat(chunks).toString('utf8') });
  res.statusCode = out.status;
  res.setHeader('content-type', 'application/json');
  res.end(JSON.stringify(out.json));
};
module.exports.config = { api: { bodyParser: false } };

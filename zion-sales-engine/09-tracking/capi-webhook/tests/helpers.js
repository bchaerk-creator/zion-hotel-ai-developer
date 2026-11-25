'use strict';
// Servidor Graph SIMULADO. Nenhuma chamada real a Meta. Todos os dados de teste sao FICTICIOS.
const http = require('node:http');
const crypto = require('node:crypto');

function startFakeGraph() {
  const calls = [];
  const state = { fail: false };
  const server = http.createServer((req, res) => {
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', () => {
      const body = JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}');
      calls.push({ url: req.url, body });
      if (state.fail) {
        res.writeHead(500, { 'content-type': 'application/json' });
        return res.end(JSON.stringify({ error: { message: 'erro simulado' } }));
      }
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ events_received: (body.data || []).length, messages: [], fbtrace_id: 'FAKE_TRACE' }));
    });
  });
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => {
      resolve({
        calls, state,
        base: `http://127.0.0.1:${server.address().port}`,
        close: () => new Promise((r) => server.close(r)),
      });
    });
  });
}

const sha = (s) => crypto.createHash('sha256').update(s, 'utf8').digest('hex');

function baseEnv(graphBase, extra = {}) {
  return {
    META_PIXEL_ID: '111222333444555', // ficticio
    META_ACCESS_TOKEN: 'TOKEN_FALSO_DE_TESTE',
    META_GRAPH_BASE: graphBase,
    WEBHOOK_SECRET: 'segredo-de-teste',
    ADAPTER: 'clickmax-delivery',
    ...extra,
  };
}

// Payload FICTICIO no formato das variaveis documentadas do webhook de entrega do ClickMax.
function deliveryPayload(over = {}) {
  return {
    id: 'TX-TESTE-0001',
    event: 'checkout.transaction.paid.v1',
    datetime: '2026-11-25T12:00:00.000Z',
    offerId: 'oferta-ficticia',
    buyerName: 'Maria Exemplo da Silva',
    buyerEmail: '  Maria.Exemplo@Example.COM ',
    buyerPhone: '5548999990000',
    transaction: { amount: 9700, status: 'paid', currency: 'BRL', paymentMethod: 'pix', isSubscriptionInvoice: false },
    utm: {
      source: 'meta', medium: 'paid', campaign: 'campanha-teste', content: 'criativo-teste',
      term: '120250000000000001', src: null, sck: '120250000000000002',
    },
    ...over,
  };
}

module.exports = { startFakeGraph, sha, baseEnv, deliveryPayload };

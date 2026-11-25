'use strict';
// Suite e2e do receptor capi-webhook: servidor HTTP REAL do receptor + servidor Graph SIMULADO (local, mais rigoroso
// que o dos testes unitarios: valida o contrato minimo da Conversions API). Tudo FICTICIO. Nenhum token real,
// nenhuma chamada a Meta. Rode: node --test tests/e2e_ciclo.test.js
const test = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { loadConfig } = require('../src/config');
const { createServer } = require('../server');

const sha = (s) => crypto.createHash('sha256').update(s, 'utf8').digest('hex');
const TOKEN = 'TOKEN_FALSO_E2E';
const SECRET = 'segredo-e2e-32-caracteres-fictício!';
const HEX64 = /^[0-9a-f]{64}$/;

// ---- Graph simulado: devolve erro 400 como a Meta faria se o contrato minimo for violado.
function startStrictGraph() {
  const calls = [];
  const server = http.createServer((req, res) => {
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', () => {
      const body = JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}');
      const problems = [];
      if (!/^\/v[\d.]+\/\d+\/events$/.test(req.url)) problems.push('rota');
      if (body.access_token !== TOKEN) problems.push('access_token');
      if (!Array.isArray(body.data) || !body.data.length) problems.push('data');
      const now = Math.floor(Date.now() / 1000);
      for (const e of body.data || []) {
        if (!e.event_name || !e.event_time || !e.event_id) problems.push('campos_basicos');
        if (now - e.event_time > 7 * 86400) problems.push('evento_com_mais_de_7_dias');
        if (e.event_time > now + 300) problems.push('evento_no_futuro');
        if (e.action_source === 'website' && !e.event_source_url) problems.push('website_sem_event_source_url');
        const ud = e.user_data || {};
        for (const k of ['em', 'ph', 'fn', 'ln']) if (ud[k] && !ud[k].every((h) => HEX64.test(h))) problems.push(`user_data.${k}_sem_hash`);
        if (e.event_name === 'Purchase') {
          const cd = e.custom_data || {};
          if (typeof cd.value !== 'number' || !cd.currency) problems.push('purchase_sem_value_currency');
        }
      }
      calls.push({ url: req.url, body, problems });
      if (problems.length) {
        res.writeHead(400, { 'content-type': 'application/json' });
        return res.end(JSON.stringify({ error: { message: 'simulado: ' + problems.join(',') } }));
      }
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ events_received: body.data.length, messages: [], fbtrace_id: 'FAKE_E2E' }));
    });
  });
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve({
    calls, base: `http://127.0.0.1:${server.address().port}`, close: () => new Promise((r) => server.close(r)),
  })));
}

async function boot(extraEnv = {}) {
  const graph = await startStrictGraph();
  const logs = [];
  const cfg = loadConfig({
    META_PIXEL_ID: '111222333444555', META_ACCESS_TOKEN: TOKEN, META_GRAPH_BASE: graph.base,
    WEBHOOK_SECRET: SECRET, ADAPTER: 'clickmax-delivery', MAX_EVENT_AGE_DAYS: '7',
    EVENT_SOURCE_URL_DEFAULT: 'https://exemplo.invalid/mini-mentoria', // OBRIGATORIO na pratica: ver teste 'sem EVENT_SOURCE_URL_DEFAULT'
    ...extraEnv,
  });
  const srv = createServer(cfg, { log: (o) => logs.push(o) });
  await new Promise((r) => srv.listen(0, '127.0.0.1', r));
  const url = `http://127.0.0.1:${srv.address().port}/webhook`;
  return {
    graph, logs, url,
    send: async (payload, headers = {}) => {
      const r = await fetch(url, { method: 'POST', headers: { 'content-type': 'application/json', 'cm-token': SECRET, ...headers }, body: JSON.stringify(payload) });
      return { status: r.status, json: await r.json() };
    },
    close: async () => { await new Promise((r) => srv.close(r)); await graph.close(); },
  };
}

const minutesAgo = (m) => new Date(Date.now() - m * 60000).toISOString();

// Payloads FICTICIOS no formato das variaveis documentadas do webhook de entrega do ClickMax.
function pedido(id, over = {}) {
  return {
    id, event: 'checkout.transaction.paid.v1', datetime: minutesAgo(5), offerId: 'oferta-ficticia',
    buyerName: 'Carla Exemplo Teste', buyerEmail: '  Carla.Exemplo@Example.COM ', buyerPhone: '(48) 99999-0001',
    transaction: { amount: 4700, status: 'paid', currency: 'BRL', paymentMethod: 'pix', isSubscriptionInvoice: false },
    utm: { source: 'meta', medium: 'paid', campaign: 'mm47', content: 'criativo-teste-varB', term: '120250000000000001', src: null, sck: '120250000000000002' },
    ...over,
  };
}

test('E2E ciclo completo: lead, Pix gerado, aprovado, reentregas e reembolso (um Purchase só, nunca no Pix gerado nem no reembolso)', async () => {
  const t = await boot({ SEND_REFUND_EVENT: 'false' });
  try {
    const ORDER = 'PEDIDO-E2E-0001';
    // 1) Lead (envio do formulario). Lead nao e compra: o receptor nao envia nada, e o Lead do Meta nasce no formulario/anuncio.
    const lead = await t.send({ id: 'LEAD-E2E-1', event: 'form.submitted', buyerEmail: 'carla.exemplo@example.com', utm: { source: 'facebook', medium: 'lead_ads', campaign: 'captacao' } });
    assert.equal(lead.status, 200); assert.equal(lead.json.status, 'ignored');
    assert.equal(t.graph.calls.length, 0, 'lead nao chama o Graph');

    // 2) Pix gerado (pedido pendente): ignorado, nunca Purchase.
    const pix = await t.send(pedido(ORDER, { event: 'checkout.transaction.pix_generated.v1', transaction: { amount: 4700, status: 'pending', currency: 'BRL', paymentMethod: 'pix', isSubscriptionInvoice: false } }));
    assert.equal(pix.json.status, 'ignored');
    assert.equal(t.graph.calls.length, 0, 'Pix gerado nao vira Purchase');

    // 3) Aprovado: um Purchase.
    const ok = await t.send(pedido(ORDER));
    assert.equal(ok.status, 200); assert.equal(ok.json.status, 'sent');
    assert.equal(t.graph.calls.length, 1);

    // 4) Reentrega do mesmo pedido (3 vezes): idempotente.
    for (let i = 0; i < 3; i++) assert.equal((await t.send(pedido(ORDER))).json.status, 'duplicate');
    assert.equal(t.graph.calls.length, 1, 'reentrega nao chama o Graph de novo');

    // 5) Reembolso: registrado, sem Purchase novo e sem evento ao Meta por padrao.
    const ref = await t.send(pedido(ORDER, { event: 'checkout.transaction.refunded.v1', transaction: { amount: 4700, status: 'refunded', currency: 'BRL', paymentMethod: 'pix', isSubscriptionInvoice: false } }));
    assert.equal(ref.json.status, 'refund_registered');
    assert.equal(ref.json.purchase_had_been_sent, true);
    assert.equal(ref.json.refund_event_sent, false);
    const ref2 = await t.send(pedido(ORDER, { event: 'checkout.transaction.refunded.v1', transaction: { amount: 4700, status: 'refunded', currency: 'BRL' } }));
    assert.equal(ref2.json.status, 'duplicate');

    // Saldo final: exatamente 1 chamada, 1 evento, e e Purchase.
    assert.equal(t.graph.calls.length, 1);
    const evs = t.graph.calls.flatMap((c) => c.body.data);
    assert.deepEqual(evs.map((e) => e.event_name), ['Purchase']);
    assert.deepEqual(t.graph.calls[0].problems, [], 'o Graph simulado nao achou violacao de contrato');
  } finally { await t.close(); }
});

test('E2E Purchase aprovado: valor em reais, event_id = id do pedido, hash do e-mail normalizado, UTMs e conteudo', async () => {
  const t = await boot();
  try {
    const r = await t.send(pedido('PEDIDO-E2E-0002'));
    assert.equal(r.json.status, 'sent');
    const e = t.graph.calls[0].body.data[0];
    assert.equal(e.event_name, 'Purchase');
    assert.equal(e.event_id, 'PEDIDO-E2E-0002');
    assert.equal(e.custom_data.value, 47, 'amount 4700 centavos vira 47 reais');
    assert.notEqual(e.custom_data.value, 4700); assert.notEqual(e.custom_data.value, 0.47);
    assert.equal(e.custom_data.currency, 'BRL');
    assert.equal(e.custom_data.order_id, 'PEDIDO-E2E-0002');
    // e-mail com espacos e maiusculas: normalizado antes do hash
    assert.deepEqual(e.user_data.em, [sha('carla.exemplo@example.com')]);
    assert.notEqual(e.user_data.em[0], sha('  Carla.Exemplo@Example.COM '));
    assert.deepEqual(e.user_data.external_id, [sha('carla.exemplo@example.com')]);
    assert.deepEqual(e.user_data.ph, [sha('5548999990001')], 'telefone so digitos com 55');
    // UTMs preservadas
    assert.equal(e.custom_data.utm_source, 'meta'); assert.equal(e.custom_data.utm_medium, 'paid');
    assert.equal(e.custom_data.utm_campaign, 'mm47'); assert.equal(e.custom_data.utm_content, 'criativo-teste-varB');
    assert.equal(e.custom_data.utm_term, '120250000000000001'); assert.equal(e.custom_data.sck, '120250000000000002');
    assert.equal(e.custom_data.content_name, 'Mini Mentoria de Estruturação Zion');
    assert.deepEqual(e.custom_data.content_ids, ['mm47']);
    // nenhum dado pessoal em texto puro no corpo enviado
    const raw = JSON.stringify(t.graph.calls[0].body);
    assert.ok(!raw.includes('Carla') && !raw.toLowerCase().includes('example.com') && !raw.includes('99999-0001'));
    // event_time = hora do pagamento, nao a hora do recebimento
    const delta = Math.floor(Date.now() / 1000) - e.event_time;
    assert.ok(delta >= 290 && delta <= 330, `event_time deve refletir o pagamento de ~5 min atras (delta=${delta}s)`);
  } finally { await t.close(); }
});

test('E2E pedido sem UTM: nenhuma atribuicao inventada (fica "nao atribuida" na conciliacao)', async () => {
  const t = await boot();
  try {
    const p = pedido('PEDIDO-E2E-0003');
    delete p.utm;
    const r = await t.send(p);
    assert.equal(r.json.status, 'sent');
    const cd = t.graph.calls[0].body.data[0].custom_data;
    for (const k of ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'sck', 'ad_id', 'campaign_id', 'adset_id']) {
      assert.equal(cd[k], undefined, `${k} nao pode existir sem dado`);
    }
    assert.equal(cd.value, 47);
  } finally { await t.close(); }
});

test('E2E Pix gerado nunca e Purchase, mesmo com o evento opcional ligado (evento proprio, id proprio)', async () => {
  const t = await boot({ SEND_PIX_GENERATED: 'true' });
  try {
    const pend = pedido('PEDIDO-E2E-0004', { event: 'checkout.transaction.pix_generated.v1', transaction: { amount: 4700, status: 'pending', currency: 'BRL', paymentMethod: 'pix' } });
    const a = await t.send(pend);
    assert.equal(a.json.status, 'sent'); assert.equal(a.json.event_name, 'PixGenerated');
    let evs = t.graph.calls.flatMap((c) => c.body.data);
    assert.deepEqual(evs.map((e) => e.event_name), ['PixGenerated']);
    assert.equal(evs[0].event_id, 'pix-PEDIDO-E2E-0004');
    await t.send(pedido('PEDIDO-E2E-0004'));
    evs = t.graph.calls.flatMap((c) => c.body.data);
    assert.deepEqual(evs.map((e) => e.event_name), ['PixGenerated', 'Purchase']);
    assert.equal(evs.filter((e) => e.event_name === 'Purchase').length, 1);
    assert.equal(evs[1].event_id, 'PEDIDO-E2E-0004');
  } finally { await t.close(); }
});

test('E2E reembolso antes de qualquer pagamento ou sem Purchase enviado: registra e nao envia Purchase', async () => {
  const t = await boot();
  try {
    const r = await t.send(pedido('PEDIDO-E2E-0005', { event: 'checkout.transaction.refunded.v1', transaction: { amount: 4700, status: 'refunded', currency: 'BRL' } }));
    assert.equal(r.json.status, 'refund_registered'); assert.equal(r.json.purchase_had_been_sent, false);
    assert.equal(t.graph.calls.length, 0);
  } finally { await t.close(); }
});

test('E2E reentrega depois de reinicio do servidor continua idempotente (armazenamento em arquivo so com ids)', async () => {
  const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'zion-e2e-')), 'ids.jsonl');
  const t1 = await boot({ DEDUPE_STORE: file });
  await t1.send(pedido('PEDIDO-E2E-0006'));
  assert.equal(t1.graph.calls.length, 1);
  await t1.close();
  const t2 = await boot({ DEDUPE_STORE: file });
  try {
    const r = await t2.send(pedido('PEDIDO-E2E-0006'));
    assert.equal(r.json.status, 'duplicate');
    assert.equal(t2.graph.calls.length, 0, 'apos reinicio o mesmo pedido nao e reenviado');
    const conteudo = fs.readFileSync(file, 'utf8');
    assert.ok(!/example\.com|Carla/i.test(conteudo), 'arquivo de ids nao guarda dado pessoal');
  } finally { await t2.close(); }
});

test('E2E pagamento com mais de 7 dias e rejeitado pelo receptor antes do Graph (200 rejected, sem nova tentativa)', async () => {
  const t = await boot();
  try {
    t.graph.calls.length = 0;
    const velho = await t.send(pedido('PEDIDO-E2E-0007', { datetime: new Date(Date.now() - 9 * 86400000).toISOString() }));
    assert.equal(velho.json.status, 'rejected');
    assert.equal(t.graph.calls.length, 0);
  } finally { await t.close(); }
});

test('E2E seguranca e privacidade: sem segredo 401; logs sem e-mail, telefone, nome nem token', async () => {
  const t = await boot();
  try {
    const r = await fetch(t.url, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(pedido('PEDIDO-E2E-0008')) });
    assert.equal(r.status, 401);
    await t.send(pedido('PEDIDO-E2E-0008'));
    await t.send(pedido('PEDIDO-E2E-0008', { event: 'checkout.transaction.refunded.v1', transaction: { amount: 4700, status: 'refunded' } }));
    const todos = JSON.stringify(t.logs);
    assert.ok(!/example\.com|Carla|99999-0001|5548999990001|TOKEN_FALSO|segredo-e2e/i.test(todos), 'log vazou dado pessoal ou segredo');
    assert.ok(t.logs.some((l) => l.msg === 'purchase_enviado'));
  } finally { await t.close(); }
});

test('E2E achado de configuracao: sem EVENT_SOURCE_URL_DEFAULT o payload do ClickMax (sem URL) e recusado pelo contrato da CAPI para action_source=website', async () => {
  const t = await boot({ EVENT_SOURCE_URL_DEFAULT: '' });
  try {
    const r = await t.send(pedido('PEDIDO-E2E-0009'));
    assert.equal(r.status, 502, 'o Graph simulado recusa website sem event_source_url');
    assert.deepEqual(t.graph.calls[0].problems, ['website_sem_event_source_url']);
    // e nada fica marcado como enviado: com a variavel corrigida, a mesma reentrega envia
  } finally { await t.close(); }
});

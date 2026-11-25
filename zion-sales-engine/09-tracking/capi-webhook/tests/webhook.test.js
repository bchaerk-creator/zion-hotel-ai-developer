'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { loadConfig } = require('../src/config');
const { createStore } = require('../src/store');
const { createHandler } = require('../src/handler');
const { createServer } = require('../server');
const { startFakeGraph, sha, baseEnv, deliveryPayload } = require('./helpers');

const NOW = Math.floor(Date.parse('2026-11-25T12:05:00Z') / 1000);

async function setup(extraEnv = {}, storeSpec = 'memory') {
  const graph = await startFakeGraph();
  const cfg = loadConfig(baseEnv(graph.base, extraEnv));
  const logs = [];
  const store = createStore(storeSpec);
  const handle = createHandler({ cfg, store, now: () => NOW, log: (o) => logs.push(o) });
  const send = (payload, opts = {}) => handle({
    method: 'POST', url: opts.url || '/webhook',
    headers: opts.headers || { 'cm-token': 'segredo-de-teste' },
    rawBody: typeof payload === 'string' ? payload : JSON.stringify(payload),
  });
  return { graph, cfg, logs, store, send };
}

test('Purchase pago: value 97 BRL, hash correto, event_id = id da transacao', async () => {
  const { graph, send } = await setup();
  const out = await send(deliveryPayload());
  assert.equal(out.status, 200);
  assert.equal(out.json.status, 'sent');
  assert.equal(graph.calls.length, 1);
  assert.match(graph.calls[0].url, /^\/v21\.0\/111222333444555\/events$/);
  assert.equal(graph.calls[0].body.access_token, 'TOKEN_FALSO_DE_TESTE');
  const ev = graph.calls[0].body.data[0];
  assert.equal(ev.event_name, 'Purchase');
  assert.equal(ev.event_id, 'TX-TESTE-0001');
  assert.equal(ev.action_source, 'website');
  assert.equal(ev.event_time, Math.floor(Date.parse('2026-11-25T12:00:00Z') / 1000));
  assert.strictEqual(ev.custom_data.value, 97);
  assert.equal(typeof ev.custom_data.value, 'number');
  assert.equal(ev.custom_data.currency, 'BRL');
  assert.equal(ev.custom_data.order_id, 'TX-TESTE-0001');
  // hash independente: e-mail em minusculas e sem espacos; telefone so digitos com 55
  assert.deepEqual(ev.user_data.em, [sha('maria.exemplo@example.com')]);
  assert.deepEqual(ev.user_data.ph, [sha('5548999990000')]);
  assert.deepEqual(ev.user_data.fn, [sha('maria')]);
  assert.deepEqual(ev.user_data.ln, [sha('silva')]);
  assert.ok(!JSON.stringify(ev).includes('example.com'), 'e-mail em texto puro nao pode ir ao Meta');
  await graph.close();
});

test('UTMs viram custom_data e ids numericos de anuncio/campanha sao derivados so se existirem', async () => {
  const { graph, send } = await setup();
  await send(deliveryPayload());
  const cd = graph.calls[0].body.data[0].custom_data;
  assert.equal(cd.utm_source, 'meta');
  assert.equal(cd.utm_campaign, 'campanha-teste');
  assert.equal(cd.utm_content, 'criativo-teste');
  assert.equal(cd.ad_id, '120250000000000001');
  assert.equal(cd.campaign_id, '120250000000000002');
  assert.equal(cd.ids_derived, true);
  assert.equal(cd.src, undefined, 'src nulo nao vira campo');
  await graph.close();
});

test('venda sem UTM nao inventa atribuicao', async () => {
  const { graph, send } = await setup();
  await send(deliveryPayload({ utm: { source: null, medium: null, campaign: null, content: null, term: null, src: null, sck: null } }));
  const cd = graph.calls[0].body.data[0].custom_data;
  for (const k of ['utm_source', 'utm_campaign', 'utm_content', 'ad_id', 'campaign_id', 'adset_id']) assert.equal(cd[k], undefined, k);
  await graph.close();
});

test('valor nao e dividido duas vezes: 4700 vira 47 (nunca 0,47 nem 4700)', async () => {
  const { graph, send } = await setup();
  await send(deliveryPayload({ id: 'TX-47', transaction: { amount: 4700, status: 'paid', currency: 'BRL' } }));
  const v = graph.calls[0].body.data[0].custom_data.value;
  assert.strictEqual(v, 47);
  assert.notStrictEqual(v, 0.47);
  assert.notStrictEqual(v, 4700);
  await graph.close();
});

test('AMOUNT_UNIT=reais nao divide', async () => {
  const { graph, send } = await setup({ AMOUNT_UNIT: 'reais' });
  await send(deliveryPayload({ id: 'TX-R', transaction: { amount: '97.00', status: 'paid' } }));
  assert.strictEqual(graph.calls[0].body.data[0].custom_data.value, 97);
  await graph.close();
});

test('valores de unidade errada sao barrados (0,97; 9700 reais; centavos fracionados)', async () => {
  const { graph, send } = await setup();
  const a = await send(deliveryPayload({ id: 'A', transaction: { amount: 97, status: 'paid' } })); // 0,97
  assert.equal(a.json.status, 'rejected'); assert.match(a.json.reason, /valor_fora_da_faixa/);
  const b = await send(deliveryPayload({ id: 'B', transaction: { amount: 970000, status: 'paid' } })); // 9700,00
  assert.equal(b.json.status, 'rejected');
  const c = await send(deliveryPayload({ id: 'C', transaction: { amount: 97.5, status: 'paid' } }));
  assert.equal(c.json.reason, 'centavos_deve_ser_inteiro');
  assert.equal(graph.calls.length, 0);
  await graph.close();
});

test('idempotencia: o mesmo pedido enviado 3 vezes gera 1 chamada ao Meta', async () => {
  const { graph, send } = await setup();
  const r1 = await send(deliveryPayload());
  const r2 = await send(deliveryPayload());
  const r3 = await send(deliveryPayload());
  assert.equal(r1.json.status, 'sent');
  assert.equal(r2.json.status, 'duplicate');
  assert.equal(r3.json.status, 'duplicate');
  assert.equal(graph.calls.length, 1);
  await graph.close();
});

test('idempotencia sobrevive a reinicio quando DEDUPE_STORE e arquivo, e o arquivo nao guarda dado pessoal', async () => {
  const f = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'zcapi-')), 'ids.jsonl');
  const s1 = await setup({}, f);
  await s1.send(deliveryPayload());
  const s2 = await setup({}, f); // "reinicio"
  const r = await s2.send(deliveryPayload());
  assert.equal(r.json.status, 'duplicate');
  assert.equal(s2.graph.calls.length, 0);
  const content = fs.readFileSync(f, 'utf8');
  assert.ok(!/@|5548999990000|maria/i.test(content), 'arquivo de ids sem dados pessoais');
  await s1.graph.close(); await s2.graph.close();
});

test('Pix gerado / transacao criada / pendente / expirado sao ignorados', async () => {
  const { graph, send } = await setup();
  const cases = [
    { id: 'P1', event: 'checkout.pix.generated.v1', transaction: { amount: 9700, status: 'pending', paymentMethod: 'pix' } },
    { id: 'P2', event: 'checkout.transaction.created.v1', transaction: { amount: 9700, status: 'pending', paymentMethod: 'pix' } },
    { id: 'P3', event: 'checkout.transaction.paid.v1', transaction: { amount: 9700, status: 'pending' } }, // evento diz pago mas status nao: nao envia
    { id: 'P4', event: 'pix.expired.v1', transaction: { amount: 9700, status: 'expired' } },
    { id: 'P5', event: 'checkout.transaction.failed.v1', transaction: { amount: 9700, status: 'failed' } },
  ];
  for (const c of cases) {
    const out = await send(deliveryPayload(c));
    assert.equal(out.status, 200, c.id);
    assert.equal(out.json.status, 'ignored', c.id);
  }
  assert.equal(graph.calls.length, 0);
  await graph.close();
});

test('Pix gerado e depois pago: so o pago vira Purchase', async () => {
  const { graph, send } = await setup();
  await send(deliveryPayload({ event: 'checkout.pix.generated.v1', transaction: { amount: 9700, status: 'pending' } }));
  assert.equal(graph.calls.length, 0);
  const paid = await send(deliveryPayload());
  assert.equal(paid.json.status, 'sent');
  assert.equal(graph.calls.length, 1);
  await graph.close();
});

test('renovacao de assinatura nao e compra', async () => {
  const { graph, send } = await setup();
  const out = await send(deliveryPayload({ transaction: { amount: 9700, status: 'paid', isSubscriptionInvoice: true } }));
  assert.equal(out.json.status, 'ignored');
  assert.equal(graph.calls.length, 0);
  await graph.close();
});

test('reembolso: nao envia Purchase, registra, e nao envia evento por padrao', async () => {
  const { graph, send, logs } = await setup();
  await send(deliveryPayload()); // compra paga antes
  assert.equal(graph.calls.length, 1);
  const out = await send(deliveryPayload({ event: 'checkout.transaction.refunded.v1', transaction: { amount: 9700, status: 'refunded' } }));
  assert.equal(out.json.status, 'refund_registered');
  assert.equal(out.json.purchase_had_been_sent, true);
  assert.equal(out.json.refund_event_sent, false);
  assert.equal(graph.calls.length, 1, 'nenhuma chamada nova ao Meta');
  assert.ok(logs.some((l) => l.msg === 'reembolso_registrado'));
  const again = await send(deliveryPayload({ event: 'checkout.transaction.refunded.v1', transaction: { amount: 9700, status: 'refunded' } }));
  assert.equal(again.json.status, 'duplicate');
  await graph.close();
});

test('reembolso com SEND_REFUND_EVENT=true envia evento proprio (nunca Purchase)', async () => {
  const { graph, send } = await setup({ SEND_REFUND_EVENT: 'true' });
  await send(deliveryPayload({ id: 'TX-RF', event: 'checkout.transaction.refunded.v1', transaction: { amount: 9700, status: 'refunded' } }));
  assert.equal(graph.calls.length, 1);
  const ev = graph.calls[0].body.data[0];
  assert.equal(ev.event_name, 'ZionRefund');
  assert.notEqual(ev.event_name, 'Purchase');
  assert.equal(ev.event_id, 'refund-TX-RF');
  await graph.close();
});

test('falha do Meta devolve 502, nao marca como enviado e a nova tentativa funciona', async () => {
  const { graph, send, store } = await setup();
  graph.state.fail = true;
  const r1 = await send(deliveryPayload());
  assert.equal(r1.status, 502);
  assert.equal(store.get('purchase:TX-TESTE-0001'), undefined);
  graph.state.fail = false;
  const r2 = await send(deliveryPayload());
  assert.equal(r2.json.status, 'sent');
  assert.equal(graph.calls.length, 2);
  await graph.close();
});

test('evento com mais de 7 dias e rejeitado; futuro e travado em agora', async () => {
  const { graph, send } = await setup();
  const old = await send(deliveryPayload({ id: 'OLD', datetime: '2026-11-10T12:00:00.000Z' }));
  assert.equal(old.json.reason, 'evento_mais_antigo_que_o_limite_da_meta');
  await send(deliveryPayload({ id: 'FUT', datetime: '2026-11-26T12:00:00.000Z' }));
  assert.equal(graph.calls[0].body.data[0].event_time, NOW);
  await graph.close();
});

test('sem e-mail, telefone, fbc ou fbp: nao envia (Meta nao conseguiria casar)', async () => {
  const { graph, send } = await setup();
  const out = await send(deliveryPayload({ buyerEmail: null, buyerPhone: null }));
  assert.equal(out.json.reason, 'sem_dado_para_correspondencia');
  assert.equal(graph.calls.length, 0);
  await graph.close();
});

test('fbc e fbp vao sem hash quando existem', async () => {
  const { graph, send } = await setup();
  await send(deliveryPayload({ fbc: 'fb.1.1700000000000.ABCDEF', fbp: 'fb.1.1700000000000.123456' }));
  const ud = graph.calls[0].body.data[0].user_data;
  assert.equal(ud.fbc, 'fb.1.1700000000000.ABCDEF');
  assert.equal(ud.fbp, 'fb.1.1700000000000.123456');
  await graph.close();
});

test('telefone brasileiro sem 55 e normalizado antes do hash', async () => {
  const { graph, send } = await setup();
  await send(deliveryPayload({ buyerPhone: '(48) 99999-0000' }));
  assert.deepEqual(graph.calls[0].body.data[0].user_data.ph, [sha('5548999990000')]);
  await graph.close();
});

test('seguranca: sem segredo 401, segredo errado 401, GET 405, JSON invalido 400', async () => {
  const { graph, send } = await setup();
  assert.equal((await send(deliveryPayload(), { headers: {} })).status, 401);
  assert.equal((await send(deliveryPayload(), { headers: { 'cm-token': 'errado' } })).status, 401);
  const get = await createHandler({ cfg: loadConfig(baseEnv(graph.base)), store: createStore('memory') })({ method: 'GET', headers: {}, rawBody: '' });
  assert.equal(get.status, 405);
  assert.equal((await send('{nao e json')).status, 400);
  assert.equal(graph.calls.length, 0);
  await graph.close();
});

test('segredo tambem aceito por query e por caminho no corpo', async () => {
  const q = await setup({ WEBHOOK_SECRET_QUERY: 'token' });
  assert.equal((await q.send(deliveryPayload(), { headers: {}, url: '/webhook?token=segredo-de-teste' })).json.status, 'sent');
  const b = await setup({ WEBHOOK_SECRET_BODY_PATH: 'auth.token' });
  assert.equal((await b.send(deliveryPayload({ auth: { token: 'segredo-de-teste' } }), { headers: {} })).json.status, 'sent');
  await q.graph.close(); await b.graph.close();
});

test('logs nao contem dados pessoais nem token', async () => {
  const { graph, send, logs } = await setup();
  await send(deliveryPayload());
  await send(deliveryPayload({ id: 'X2', transaction: { amount: 9700, status: 'pending' }, event: 'checkout.pix.generated.v1' }));
  const text = JSON.stringify(logs);
  for (const bad of ['example.com', '5548999990000', 'Maria', 'TOKEN_FALSO_DE_TESTE', 'segredo-de-teste']) assert.ok(!text.includes(bad), bad);
  await graph.close();
});

test('META_TEST_EVENT_CODE vai no corpo quando preenchido', async () => {
  const { graph, send } = await setup({ META_TEST_EVENT_CODE: 'TEST00000' });
  await send(deliveryPayload());
  assert.equal(graph.calls[0].body.test_event_code, 'TEST00000');
  await graph.close();
});

test('adaptador clickmax-out: SALE_MADE por ?evento=, REFUND_MADE e expirado', async () => {
  const { graph, send } = await setup({ ADAPTER: 'clickmax-out' });
  const sale = { transactionId: 'TX-OUT-1', email: 'comprador@example.org', telephone: '5548988887777', saleValue: 4700, saleDate: '2026-11-25T11:59:00.000Z', utmSource: 'meta', utmCampaign: 'c1', status: 'paid' };
  const r = await send(sale, { url: '/webhook?evento=SALE_MADE' });
  assert.equal(r.json.status, 'sent');
  assert.strictEqual(graph.calls[0].body.data[0].custom_data.value, 47);
  const ref = await send({ ...sale }, { url: '/webhook?evento=REFUND_MADE' });
  assert.equal(ref.json.status, 'refund_registered');
  const exp = await send({ ...sale, transactionId: 'TX-OUT-2' }, { url: '/webhook?evento=PIX_OR_BOLETO_EXPIRED_OR_OVERDUE' });
  assert.equal(exp.json.status, 'ignored');
  const pend = await send({ ...sale, transactionId: 'TX-OUT-3', status: 'pending' }, { url: '/webhook?evento=SALE_MADE' });
  assert.equal(pend.json.status, 'ignored', 'SALE_MADE com status pendente nao e compra');
  assert.equal(graph.calls.length, 1);
  await graph.close();
});

test('FIELD_MAP_JSON sobrescreve caminhos (formato custom)', async () => {
  const { graph, send } = await setup({
    ADAPTER: 'custom', AMOUNT_UNIT: 'reais',
    FIELD_MAP_JSON: JSON.stringify({ eventId: ['pedido.numero'], status: ['pedido.situacao'], amount: ['pedido.total'], email: ['cliente.mail'], paidAt: ['pedido.pago_em'] }),
  });
  const out = await send({ pedido: { numero: 'N-9', situacao: 'approved', total: '47.00', pago_em: '2026-11-25T12:00:00Z' }, cliente: { mail: 'x@example.net' } });
  assert.equal(out.json.status, 'sent');
  assert.strictEqual(graph.calls[0].body.data[0].custom_data.value, 47);
  await graph.close();
});

test('ponta a ponta por HTTP real (servidor + Graph simulado)', async () => {
  const graph = await startFakeGraph();
  const cfg = loadConfig(baseEnv(graph.base));
  const srv = createServer(cfg, { store: createStore('memory'), log: () => {}, now: () => NOW });
  await new Promise((r) => srv.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${srv.address().port}`;
  const res = await fetch(`${base}/webhook`, { method: 'POST', headers: { 'content-type': 'application/json', 'cm-token': 'segredo-de-teste' }, body: JSON.stringify(deliveryPayload()) });
  assert.equal(res.status, 200);
  assert.equal((await res.json()).status, 'sent');
  const bad = await fetch(`${base}/webhook`, { method: 'POST', body: '{}' });
  assert.equal(bad.status, 401);
  const health = await fetch(`${base}/health`);
  assert.equal(health.status, 200);
  assert.equal(graph.calls.length, 1);
  await new Promise((r) => srv.close(r));
  await graph.close();
});

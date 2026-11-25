'use strict';
// Adaptadores: dizem em que lugar do JSON de cada plataforma esta cada campo.
// Cada campo aceita VARIOS caminhos (o primeiro que existir vence). Caminhos usam ponto: "transaction.amount".
//
// Estado de confirmacao dos formatos (ver PLANO_EXECUTAVEL.md):
// - clickmax-delivery: variaveis documentadas em docs.clickmax.io/features/products/webhook-delivery-payload.
//   Voce escreve o JSON no painel da oferta; o exemplo pronto esta em README.md. [E]
// - clickmax-out: o corpo de SALE_MADE e REFUND_MADE existe na referencia de webhooks, mas os nomes exatos dos
//   campos de venda nao foram lidos por completo nesta sessao. Os caminhos abaixo sao candidatos. [NC]
//   Confirme com o botao "Enviar teste" do ClickMax e ajuste com FIELD_MAP_JSON.
// - ticto: formato do webhook Ticto 2.0 sem documentacao oficial lida. Candidatos, [NC].

const COMMON_UTMS = {
  utm_source: ['utm.source', 'utmSource', 'utm_source', 'query_params.utm_source'],
  utm_medium: ['utm.medium', 'utmMedium', 'utm_medium', 'query_params.utm_medium'],
  utm_campaign: ['utm.campaign', 'utmCampaign', 'utm_campaign', 'query_params.utm_campaign'],
  utm_content: ['utm.content', 'utmContent', 'utm_content', 'query_params.utm_content'],
  utm_term: ['utm.term', 'utmTerm', 'utm_term', 'query_params.utm_term'],
  src: ['utm.src', 'src', 'query_params.src'],
  sck: ['utm.sck', 'sck', 'query_params.sck'],
  ad_id: ['ad_id', 'adId', 'query_params.ad_id'],
  campaign_id: ['campaign_id', 'campaignId', 'query_params.campaign_id'],
  adset_id: ['adset_id', 'adsetId', 'query_params.adset_id'],
};

const ADAPTERS = {
  'clickmax-delivery': {
    eventId: ['id', 'transaction.id', 'transactionId'],
    eventName: ['event'],
    status: ['transaction.status'],
    amount: ['transaction.amount'],
    currency: ['transaction.currency'],
    email: ['buyerEmail'],
    phone: ['buyerPhone'],
    firstName: [],
    fullName: ['buyerName'],
    paymentMethod: ['transaction.paymentMethod'],
    paidAt: ['datetime'],
    url: ['linkCheckout', 'pageUrl'],
    fbc: ['fbc'],
    fbp: ['fbp'],
    ip: ['ip', 'clientIp'],
    userAgent: ['userAgent'],
    isRenewal: ['transaction.isSubscriptionInvoice', 'isSubscriptionInvoice'],
    ...COMMON_UTMS,
  },
  'clickmax-out': {
    eventId: ['transactionId', 'id', 'saleId'],
    eventName: [],
    status: ['status', 'saleStatus', 'transaction.status'],
    amount: ['saleValue', 'amount', 'value', 'transaction.amount'],
    currency: ['currency'],
    email: ['email', 'buyer.email'],
    phone: ['telephone', 'phone', 'buyer.phone'],
    firstName: [],
    fullName: ['fullname', 'name', 'buyer.name'],
    paymentMethod: ['paymentMethod', 'payment_method'],
    paidAt: ['saleDate', 'paidAt', 'datetime'],
    url: ['linkCheckout', 'pageUrl'],
    fbc: ['fbc'],
    fbp: ['fbp'],
    ip: ['ip'],
    userAgent: ['userAgent'],
    isRenewal: ['isSubscriptionInvoice'],
    ...COMMON_UTMS,
  },
  ticto: {
    eventId: ['order.hash', 'order.id', 'transaction.hash', 'id'],
    eventName: ['status', 'event'],
    status: ['status', 'order.status'],
    amount: ['order.paid_amount', 'transaction.paid_amount', 'item.amount', 'amount'],
    currency: ['currency'],
    email: ['customer.email', 'email'],
    phone: ['customer.phone.number', 'customer.phone', 'phone'],
    firstName: [],
    fullName: ['customer.name'],
    paymentMethod: ['payment_method', 'order.payment_method'],
    paidAt: ['order.paid_at', 'paid_at', 'order.date'],
    url: ['checkout_url', 'url'],
    fbc: ['fbc'],
    fbp: ['fbp'],
    ip: ['ip'],
    userAgent: ['user_agent'],
    isRenewal: [],
    ...COMMON_UTMS,
  },
  custom: {},
};

function getPath(obj, path) {
  if (!obj || !path) return undefined;
  let cur = obj;
  for (const k of String(path).split('.')) {
    if (cur === null || cur === undefined || typeof cur !== 'object') return undefined;
    cur = cur[k];
  }
  return cur;
}

function pick(obj, paths) {
  for (const p of paths || []) {
    const v = getPath(obj, p);
    if (v !== undefined && v !== null && v !== '') return v;
  }
  return undefined;
}

function buildMap(adapterName, fieldMapJson) {
  const base = ADAPTERS[adapterName];
  if (!base) throw new Error(`ADAPTER desconhecido: ${adapterName}`);
  let extra = {};
  if (fieldMapJson) {
    try { extra = JSON.parse(fieldMapJson); } catch (e) { throw new Error('FIELD_MAP_JSON invalido'); }
  }
  const map = { ...base };
  for (const [k, v] of Object.entries(extra)) map[k] = Array.isArray(v) ? v : [v];
  return map;
}

// Extrai um registro neutro do corpo recebido.
function extract(body, map) {
  const r = {};
  for (const key of Object.keys(map)) r[key] = pick(body, map[key]);
  return r;
}

module.exports = { ADAPTERS, getPath, pick, buildMap, extract };

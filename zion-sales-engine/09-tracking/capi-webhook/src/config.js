'use strict';
// Toda configuracao vem de variaveis de ambiente. Nenhum valor real mora no repositorio.
function list(v, def) {
  return String(v === undefined || v === '' ? def : v)
    .split(',').map((s) => s.trim().toLowerCase()).filter(Boolean);
}
function num(v, def) {
  const n = Number(v);
  return v === undefined || v === '' || Number.isNaN(n) ? def : n;
}
function bool(v, def) {
  if (v === undefined || v === '') return def;
  return /^(1|true|yes|sim)$/i.test(String(v));
}

function loadConfig(env = process.env) {
  return {
    pixelId: env.META_PIXEL_ID || '',
    accessToken: env.META_ACCESS_TOKEN || '',
    graphVersion: env.META_GRAPH_VERSION || 'v21.0',
    graphBase: env.META_GRAPH_BASE || 'https://graph.facebook.com',
    testEventCode: env.META_TEST_EVENT_CODE || '',
    secret: env.WEBHOOK_SECRET || '',
    secretHeader: (env.WEBHOOK_SECRET_HEADER || 'cm-token').toLowerCase(),
    secretQuery: env.WEBHOOK_SECRET_QUERY || '',
    secretBodyPath: env.WEBHOOK_SECRET_BODY_PATH || '',
    adapter: env.ADAPTER || 'clickmax-delivery',
    fieldMapJson: env.FIELD_MAP_JSON || '',
    amountUnit: (env.AMOUNT_UNIT || 'cents').toLowerCase(),
    eventQueryParam: env.EVENT_QUERY_PARAM || 'evento',
    // Pago = so o que esta aqui. Padrao conservador (auditoria A05): 'authorized' (cartao nao capturado) e
    // 'completed' NAO contam. Ampliar so via PAID_STATUSES, com evidencia do payload real do gateway.
    paidStatuses: list(env.PAID_STATUSES, 'paid,approved'),
    refundStatuses: list(env.REFUND_STATUSES, 'refunded,refunding,chargedback,chargeback,canceled,cancelled'),
    minValue: num(env.MIN_VALUE, 1),
    maxValue: num(env.MAX_VALUE, 2000),
    currency: (env.CURRENCY || 'BRL').toUpperCase(),
    eventTimeFallbackNow: bool(env.EVENT_TIME_FALLBACK_NOW, true),
    maxEventAgeDays: num(env.MAX_EVENT_AGE_DAYS, 7),
    eventSourceUrlDefault: env.EVENT_SOURCE_URL_DEFAULT || '',
    sendRefundEvent: bool(env.SEND_REFUND_EVENT, false),
    refundEventName: env.REFUND_EVENT_NAME || 'ZionRefund',
    // Eventos opcionais do funil P0. DESLIGADOS por padrao. Pix gerado NUNCA e Purchase.
    sendPixGenerated: bool(env.SEND_PIX_GENERATED, false),
    pixGeneratedEventName: env.PIX_GENERATED_EVENT_NAME || 'PixGenerated',
    sendAccessDelivered: bool(env.SEND_ACCESS_DELIVERED, false),
    accessDeliveredEventName: env.ACCESS_DELIVERED_EVENT_NAME || 'AccessDelivered',
    contentName: env.CONTENT_NAME || 'Mini Mentoria de Estruturação Zion',
    contentId: env.CONTENT_ID || 'mm47',
    dedupeStore: env.DEDUPE_STORE || 'memory',
    port: num(env.PORT, 8787),
    maxBodyBytes: num(env.MAX_BODY_BYTES, 262144),
  };
}

module.exports = { loadConfig };

'use strict';
// Monta o evento da Conversions API. Valor em REAIS com ponto decimal, dividido UMA unica vez (aqui).
const { hashed, sha256, normEmail, normPhone, normName } = require('./normalize');

function toNumber(raw) {
  if (typeof raw === 'number') return raw;
  const s = String(raw).trim();
  if (!/^-?\d+(\.\d+)?$/.test(s)) return NaN;
  return Number(s);
}

function toValue(raw, unit, cfg) {
  if (raw === undefined || raw === null || raw === '') return { error: 'sem_valor' };
  const n = toNumber(raw);
  if (!Number.isFinite(n) || n <= 0) return { error: 'valor_invalido' };
  let value;
  if (unit === 'cents') {
    if (!Number.isInteger(n)) return { error: 'centavos_deve_ser_inteiro' };
    value = n / 100;
  } else {
    value = n;
  }
  value = Math.round(value * 100) / 100;
  if (value < cfg.minValue || value > cfg.maxValue) {
    return { error: `valor_fora_da_faixa:${value}` };
  }
  return { value };
}

function toEpoch(raw, cfg, nowSec) {
  if (raw === undefined || raw === null || raw === '') {
    return cfg.eventTimeFallbackNow ? { time: nowSec, fallback: true } : { error: 'sem_hora_do_pagamento' };
  }
  let t;
  if (/^\d{13}$/.test(String(raw))) t = Math.floor(Number(raw) / 1000);
  else if (/^\d{10}$/.test(String(raw))) t = Number(raw);
  else {
    const ms = Date.parse(String(raw));
    if (Number.isNaN(ms)) return { error: 'hora_invalida' };
    t = Math.floor(ms / 1000);
  }
  if (t > nowSec + 300) t = nowSec; // relogio adiantado: nunca no futuro
  if (nowSec - t > cfg.maxEventAgeDays * 86400) return { error: 'evento_mais_antigo_que_o_limite_da_meta' };
  return { time: t };
}

const UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'src', 'sck', 'ad_id', 'campaign_id', 'adset_id'];

function buildCustomData(record, value, currency, eventId, cfg) {
  const cd = { value, currency, order_id: String(eventId) };
  if (cfg) { cd.content_name = cfg.contentName; cd.content_ids = [cfg.contentId]; cd.content_type = 'product'; }
  if (record.paymentMethod) cd.payment_method = String(record.paymentMethod);
  for (const k of UTM_KEYS) if (record[k] !== undefined) cd[k] = String(record[k]);
  // Ids numericos que ja vieram na URL do anuncio: utm_term={{ad.id}} e sck={{campaign.id}}. Nada e inventado.
  if (cd.ad_id === undefined && /^\d{8,}$/.test(cd.utm_term || '')) { cd.ad_id = cd.utm_term; cd.ids_derived = true; }
  if (cd.campaign_id === undefined && /^\d{8,}$/.test(cd.sck || '')) { cd.campaign_id = cd.sck; cd.ids_derived = true; }
  return cd;
}

function buildUserData(record) {
  const ud = {};
  const em = hashed(record.email, normEmail);
  if (em) { ud.em = [em]; ud.external_id = [em]; }
  const ph = hashed(record.phone, normPhone);
  if (ph) ud.ph = [ph];
  const full = normName(record.fullName);
  if (full) {
    const parts = full.split(/\s+/);
    ud.fn = [sha256(parts[0])];
    if (parts.length > 1) ud.ln = [sha256(parts[parts.length - 1])];
  }
  if (record.fbc) ud.fbc = String(record.fbc);
  if (record.fbp) ud.fbp = String(record.fbp);
  if (record.ip) ud.client_ip_address = String(record.ip);
  if (record.userAgent) ud.client_user_agent = String(record.userAgent);
  return ud;
}

function hasMatchKey(ud) {
  return Boolean(ud.em || ud.ph || ud.fbc || ud.fbp || ud.client_ip_address);
}

function buildPurchase(record, cfg, nowSec) {
  if (!record.eventId) return { error: 'sem_event_id' };
  const v = toValue(record.amount, cfg.amountUnit, cfg);
  if (v.error) return { error: v.error };
  const t = toEpoch(record.paidAt, cfg, nowSec);
  if (t.error) return { error: t.error };
  const ud = buildUserData(record);
  if (!hasMatchKey(ud)) return { error: 'sem_dado_para_correspondencia' };
  const currency = /^[A-Za-z]{3}$/.test(String(record.currency || '')) ? String(record.currency).toUpperCase() : cfg.currency;
  const eventId = String(record.eventId);
  const event = {
    event_name: 'Purchase',
    event_time: t.time,
    event_id: eventId,
    action_source: 'website',
    user_data: ud,
    custom_data: buildCustomData(record, v.value, currency, eventId, cfg),
  };
  const url = record.url || cfg.eventSourceUrlDefault;
  if (url) event.event_source_url = String(url);
  return { event, timeFallback: Boolean(t.fallback) };
}

// Evento custom opcional (Pix gerado, acesso entregue). event_id proprio (prefixo + id do pedido): nunca igual ao do Purchase.
// 'value' so vai se o valor existir e passar na mesma validacao do Purchase (reais, ponto decimal). Nao e conversao de compra.
function buildCustomEvent(record, cfg, nowSec, { name, prefix }) {
  if (!record.eventId) return { error: 'sem_event_id' };
  const ud = buildUserData(record);
  if (!hasMatchKey(ud)) return { error: 'sem_dado_para_correspondencia' };
  const eventId = `${prefix}-${record.eventId}`;
  const cd = buildCustomData(record, undefined, undefined, record.eventId);
  delete cd.value; delete cd.currency; delete cd.payment_method;
  cd.order_id = String(record.eventId);
  cd.content_name = cfg.contentName;
  cd.content_ids = [cfg.contentId];
  cd.content_type = 'product';
  if (record.amount !== undefined && record.amount !== null && record.amount !== '') {
    const v = toValue(record.amount, cfg.amountUnit, cfg);
    if (v.error) return { error: v.error };
    cd.value = v.value;
    cd.currency = /^[A-Za-z]{3}$/.test(String(record.currency || '')) ? String(record.currency).toUpperCase() : cfg.currency;
  }
  if (record.paymentMethod) cd.payment_method = String(record.paymentMethod);
  const event = { event_name: name, event_time: nowSec, event_id: eventId, action_source: 'website', user_data: ud, custom_data: cd };
  const url = record.url || cfg.eventSourceUrlDefault;
  if (url) event.event_source_url = String(url);
  return { event };
}

function buildRefundEvent(record, cfg, nowSec) {
  const base = buildPurchase(record, cfg, nowSec);
  if (base.error) return base;
  const e = base.event;
  e.event_name = cfg.refundEventName;
  e.event_id = `refund-${e.event_id}`;
  return { event: e };
}

module.exports = { buildCustomEvent, buildPurchase, buildRefundEvent, toValue, toEpoch };

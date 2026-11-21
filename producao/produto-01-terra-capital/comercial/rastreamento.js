// Modelo de referência e teste do rastreamento do Produto 01. NÃO é um servidor em produção:
// valida as regras (assinatura, idempotência, acesso só após pagamento, reembolso, conciliação, UTM) que o fluxo real deve cumprir.
const crypto = require('crypto');
const PRODUTO = 'p01_terra_capital';
const VERSOES = { A47: { preco: 47 }, B67: { preco: 67 } };

function parseUtm(search) {
  const q = new URLSearchParams(search || ''), o = {};
  for (const k of ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'price_version']) if (q.get(k)) o[k] = String(q.get(k)).slice(0, 80);
  return o;
}
// Evento deduplicável: o mesmo event_id vai pelo navegador (Pixel) e pelo servidor (CAPI) para o Meta descartar a repetição.
function eventId(tipo, ref) { return `${PRODUTO}:${tipo}:${ref}`; }
function eventoCompra(pag) {
  // sem e-mail, telefone, nome, CPF ou valores patrimoniais; hash só se o CAPI for usado e houver consentimento
  return { event_name: 'Purchase', event_id: eventId('purchase', pag.paymentId), value: pag.valor, currency: 'BRL', custom_data: { produto: PRODUTO, versao_preco: pag.versao, offer_id: pag.offerId } };
}
function assinar(corpo, segredo) { return crypto.createHmac('sha256', segredo).update(corpo).digest('hex'); }
function conferir(corpo, assinatura, segredo) {
  const esperado = Buffer.from(assinar(corpo, segredo)), recebido = Buffer.from(String(assinatura || ''));
  return esperado.length === recebido.length && crypto.timingSafeEqual(esperado, recebido);
}

class Loja {
  constructor(segredo) { this.segredo = segredo; this.pagamentos = new Map(); this.acessos = new Set(); this.eventosEnviados = new Map(); this.log = []; }
  // recebe o webhook cru (string) + assinatura
  webhook(corpo, assinatura) {
    if (!conferir(corpo, assinatura, this.segredo)) { this.log.push('rejeitado: assinatura'); return { ok: false, motivo: 'assinatura inválida' }; }
    let e; try { e = JSON.parse(corpo); } catch { return { ok: false, motivo: 'json inválido' }; }
    if (!e.paymentId || !e.tipo) return { ok: false, motivo: 'campos obrigatórios' };
    const p = this.pagamentos.get(e.paymentId) || { paymentId: e.paymentId, status: 'novo', vistos: new Set() };
    if (p.vistos.has(e.eventoId)) return { ok: true, duplicado: true };       // idempotência por id do evento
    p.vistos.add(e.eventoId);
    const ordem = { novo: 0, pendente: 1, pago: 2, reembolsado: 3 };
    const alvo = { 'pagamento.criado': 'pendente', 'pagamento.confirmado': 'pago', 'pagamento.reembolsado': 'reembolsado' }[e.tipo];
    if (!alvo) return { ok: false, motivo: 'tipo desconhecido' };
    if (ordem[alvo] < ordem[p.status]) { this.pagamentos.set(e.paymentId, p); return { ok: true, ignorado: 'evento fora de ordem' }; }
    Object.assign(p, { status: alvo, valor: e.valor ?? p.valor, versao: e.versao ?? p.versao, offerId: e.offerId ?? p.offerId, leadRef: e.leadRef ?? p.leadRef });
    this.pagamentos.set(e.paymentId, p);
    if (alvo === 'pago') this.acessos.add(p.leadRef);                           // acesso só com pagamento confirmado
    if (alvo === 'reembolsado') this.acessos.delete(p.leadRef);
    if (alvo === 'pago' && !this.eventosEnviados.has(eventId('purchase', p.paymentId))) this.eventosEnviados.set(eventId('purchase', p.paymentId), eventoCompra(p));
    return { ok: true, status: p.status };
  }
}
// Conciliação: ClickMax x Asaas por id do pagamento; devolve divergências
function conciliar(clickmax, asaas) {
  const a = new Map(asaas.map(x => [x.paymentId, x])), c = new Map(clickmax.map(x => [x.paymentId, x])), div = [];
  for (const [id, x] of c) { const y = a.get(id); if (!y) div.push({ id, tipo: 'só no ClickMax' }); else { if (x.status !== y.status) div.push({ id, tipo: 'status diferente', clickmax: x.status, asaas: y.status }); if (x.valor !== y.valor) div.push({ id, tipo: 'valor diferente', clickmax: x.valor, asaas: y.valor }); } }
  for (const id of a.keys()) if (!c.has(id)) div.push({ id, tipo: 'só no Asaas' });
  return div;
}
module.exports = { PRODUTO, VERSOES, parseUtm, eventId, eventoCompra, assinar, conferir, Loja, conciliar };

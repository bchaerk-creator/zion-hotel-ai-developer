// Modelo de referência e teste do rastreamento da Mini Mentoria de Performance Hoteleira. NÃO é servidor em produção:
// fixa as regras que o fluxo real (Asaas + ClickMax + CRM + Zaya) deve cumprir.
const crypto = require('crypto');
const PRODUTO = 'mmph47', SKU = 'MMPH-47';
const ETAPAS = ['lead', 'checkout', 'pago', 'acesso', 'diagnostico', 'dossie', 'autorizacao', 'reuniao', 'proposta'];
function parseUtm(search) { const q = new URLSearchParams(search || ''), o = {}; for (const k of ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'ad_id', 'campaign_id', 'lead_id']) if (q.get(k)) o[k] = String(q.get(k)).slice(0, 80); return o; }
const eventId = (tipo, ref) => `${PRODUTO}:${tipo}:${ref}`;
// Purchase só com pagamento confirmado; sem e-mail, telefone, nome, CPF nem respostas do diagnóstico
function eventoCompra(p) { return { event_name: 'Purchase', event_id: eventId('purchase', p.paymentId), value: p.valor, currency: 'BRL', custom_data: { produto: PRODUTO, sku: SKU, offer_id: p.offerId, order_id: p.orderId, ad_id: p.adId, campaign_id: p.campaignId, creative: p.utmContent } }; }
const assinar = (c, s) => crypto.createHmac('sha256', s).update(c).digest('hex');
const conferir = (c, a, s) => { const e = Buffer.from(assinar(c, s)), r = Buffer.from(String(a || '')); return e.length === r.length && crypto.timingSafeEqual(e, r); };
class Loja {
  constructor(segredo) { this.segredo = segredo; this.pagamentos = new Map(); this.acessos = new Set(); this.eventosEnviados = new Map(); this.crm = new Map(); this.optOut = new Set(); this.mensagens = []; }
  etapa(ref, e) { const c = this.crm.get(ref) || { etapas: new Set() }; c.etapas.add(e); this.crm.set(ref, c); }
  webhook(corpo, assinatura) {
    if (!conferir(corpo, assinatura, this.segredo)) return { ok: false, motivo: 'assinatura inválida' };
    let e; try { e = JSON.parse(corpo); } catch { return { ok: false, motivo: 'json inválido' }; }
    if (!e.paymentId || !e.tipo) return { ok: false, motivo: 'campos obrigatórios' };
    const p = this.pagamentos.get(e.paymentId) || { paymentId: e.paymentId, status: 'novo', vistos: new Set() };
    if (p.vistos.has(e.eventoId)) return { ok: true, duplicado: true }; p.vistos.add(e.eventoId);
    const ordem = { novo: 0, pendente: 1, pago: 2, reembolsado: 3 }, alvo = { 'pagamento.criado': 'pendente', 'pagamento.confirmado': 'pago', 'pagamento.reembolsado': 'reembolsado' }[e.tipo];
    if (!alvo) return { ok: false, motivo: 'tipo desconhecido' };
    if (ordem[alvo] < ordem[p.status]) { this.pagamentos.set(e.paymentId, p); return { ok: true, ignorado: 'evento fora de ordem' }; }
    for (const k of ['valor', 'offerId', 'orderId', 'leadRef', 'adId', 'campaignId', 'utmContent']) if (e[k] !== undefined) p[k] = e[k];
    p.status = alvo; this.pagamentos.set(e.paymentId, p);
    if (alvo === 'pendente') this.etapa(p.leadRef, 'checkout');
    if (alvo === 'pago') { this.acessos.add(p.leadRef); this.etapa(p.leadRef, 'checkout'); this.etapa(p.leadRef, 'pago'); this.etapa(p.leadRef, 'acesso'); }
    if (alvo === 'reembolsado') this.acessos.delete(p.leadRef);
    if (alvo === 'pago' && !this.eventosEnviados.has(eventId('purchase', p.paymentId))) this.eventosEnviados.set(eventId('purchase', p.paymentId), eventoCompra(p));
    return { ok: true, status: p.status };
  }
  // eventos do produto (o servidor só recebe contagens, nunca as respostas)
  evento(ref, tipo) { if (!ETAPAS.includes(tipo)) return { ok: false }; if (tipo !== 'lead' && tipo !== 'checkout' && !this.acessos.has(ref)) return { ok: false, motivo: 'sem acesso pago' }; this.etapa(ref, tipo); return { ok: true }; }
  // Zaya: só com consentimento e sem opt-out; nunca é pré-requisito para entregar o produto
  podeContatar(ref, consentimento) { return !!consentimento && !this.optOut.has(ref); }
  enviarZaya(ref, consentimento, texto) { if (!this.podeContatar(ref, consentimento)) return { ok: false, motivo: this.optOut.has(ref) ? 'opt-out' : 'sem consentimento' }; this.mensagens.push({ ref, texto }); return { ok: true }; }
  parar(ref) { this.optOut.add(ref); }
}
function conciliar(clickmax, asaas) { const a = new Map(asaas.map(x => [x.paymentId, x])), c = new Map(clickmax.map(x => [x.paymentId, x])), d = [];
  for (const [id, x] of c) { const y = a.get(id); if (!y) d.push({ id, tipo: 'só no ClickMax' }); else { if (x.status !== y.status) d.push({ id, tipo: 'status diferente', clickmax: x.status, asaas: y.status }); if (x.valor !== y.valor) d.push({ id, tipo: 'valor diferente' }); } }
  for (const id of a.keys()) if (!c.has(id)) d.push({ id, tipo: 'só no Asaas' }); return d; }
// Métricas por criativo: receita líquida só de pagamentos pagos e não reembolsados; divisão por zero vira null
function metricas(linhas, gastoPorCriativo, taxaPct) {
  const o = {};
  for (const [cr, g] of Object.entries(gastoPorCriativo || {})) o[cr] = { gasto: g, leads: 0, pagos: 0, receitaBruta: 0, diag: 0, dossie: 0, oportunidades: 0 };
  for (const l of linhas) { const m = o[l.criativo] = o[l.criativo] || { gasto: 0, leads: 0, pagos: 0, receitaBruta: 0, diag: 0, dossie: 0, oportunidades: 0 };
    m.leads++; if (l.status === 'pago') { m.pagos++; m.receitaBruta += l.valor; } if (l.etapas && l.etapas.includes('diagnostico')) m.diag++; if (l.etapas && l.etapas.includes('dossie')) m.dossie++; if (l.etapas && (l.etapas.includes('reuniao') || l.etapas.includes('proposta'))) m.oportunidades++; }
  for (const m of Object.values(o)) { m.cpl = m.leads ? +(m.gasto / m.leads).toFixed(2) : null; m.cpa = m.pagos ? +(m.gasto / m.pagos).toFixed(2) : null; m.receitaLiquida = +(m.receitaBruta * (1 - (taxaPct || 0) / 100)).toFixed(2); m.conclusao = m.pagos ? +(m.diag / m.pagos * 100).toFixed(1) : null; }
  return o;
}
module.exports = { PRODUTO, SKU, ETAPAS, parseUtm, eventId, eventoCompra, assinar, conferir, Loja, conciliar, metricas };

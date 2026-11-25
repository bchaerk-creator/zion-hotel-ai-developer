'use strict';
// Decide o que fazer com o webhook: purchase (enviar), refund (registrar) ou ignore.
// Regra central: so existe Purchase quando ha sinal de PAGAMENTO CONFIRMADO. Pix gerado, pendente,
// aguardando, expirado, falho e recusado sao ignorados.

const REFUND_NAME = /(refund|reembols|chargeback|estorn|sale_cancel|cancel)/i;
const PENDING_NAME = /(unpaid|not[_ .-]?paid|waiting|pending|aguard|pix[_.]generated|pix[_ ]gerado|created|expired|expirad|failed|falh|refused|recusad|abandon)/i;
const PAID_NAME = /(paid|sale_made|venda[_ ]realizada|approved|aprovad|pago)/i;

function lower(v) { return v === undefined || v === null ? '' : String(v).trim().toLowerCase(); }

function classify(record, cfg, hint) {
  const name = lower(hint) || lower(record.eventName);
  const status = lower(record.status);

  if (record.isRenewal === true || lower(record.isRenewal) === 'true') {
    return { decision: 'ignore', reason: 'renovacao_de_assinatura_nao_e_compra' };
  }

  const nameRefund = REFUND_NAME.test(name);
  const statusRefund = status && cfg.refundStatuses.includes(status);
  if (nameRefund || statusRefund) {
    return { decision: 'refund', reason: nameRefund ? `evento:${name}` : `status:${status}` };
  }

  // Qualquer palavra de pendencia no nome vence a palavra 'paid' (ex.: 'paid_pending' nunca e compra; A05).
  if (PENDING_NAME.test(name)) {
    return { decision: 'ignore', reason: `evento_sem_pagamento:${name}` };
  }

  const namePaid = PAID_NAME.test(name);
  const statusPaid = status && cfg.paidStatuses.includes(status);

  if (status && !statusPaid) {
    return { decision: 'ignore', reason: `status_nao_pago:${status}` };
  }
  if (namePaid || statusPaid) {
    return { decision: 'purchase', reason: statusPaid ? `status:${status}` : `evento:${name}` };
  }
  return { decision: 'ignore', reason: name ? `evento_sem_pagamento:${name}` : 'sem_sinal_de_pagamento' };
}

module.exports = { classify };

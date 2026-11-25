'use strict';
// Normalizacao e hash de dados do comprador para a Conversions API.
// Regra da Meta: normalizar (minusculas, sem espacos; telefone so digitos com codigo do pais) e aplicar SHA-256 hexadecimal.
// NAO se aplica hash a fbc, fbp, client_ip_address e client_user_agent.
const crypto = require('node:crypto');

function sha256(text) {
  return crypto.createHash('sha256').update(String(text), 'utf8').digest('hex');
}

function normEmail(v) {
  if (v === undefined || v === null) return null;
  const s = String(v).trim().toLowerCase();
  return s.includes('@') ? s : null;
}

// Telefone brasileiro: so digitos; se vier com 10 ou 11 digitos (DDD + numero), acrescenta 55.
function normPhone(v) {
  if (v === undefined || v === null) return null;
  let d = String(v).replace(/\D+/g, '').replace(/^0+/, '');
  if (!d) return null;
  if (d.length === 10 || d.length === 11) d = '55' + d;
  if (d.length < 11) return null;
  return d;
}

function normName(v) {
  if (v === undefined || v === null) return null;
  const s = String(v).trim().toLowerCase();
  return s || null;
}

function hashed(value, normalizer) {
  const n = normalizer(value);
  return n ? sha256(n) : null;
}

module.exports = { sha256, normEmail, normPhone, normName, hashed };

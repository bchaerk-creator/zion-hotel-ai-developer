// Utilitários comuns da suíte de homologação financeira (Comando 05C).
// Nada aqui altera ferramentas de produção: só lê e compara.
"use strict";

// Tolerâncias do Plano de Homologação v0.2 (seção 3).
const TOL = {
  reais: 0.01,        // R$ 0,01
  pct: 0.0001,        // 0,01 ponto percentual (fração)
  anos: 0.01,         // 0,01 ano
  noites: 0.01,       // 0,01 noite
  pct1casa: 0.0005,   // valores que o plano dá com 1 casa (ex.: 20,4%, −8,4%)
  anos1casa: 0.05,    // valores que o plano dá com 1 casa (ex.: 38,6 anos)
};

// Tipos de caso (instrução 4 do Comando 05C).
const TIPO = {
  FORMULA: "formula",            // fórmula deve estar matematicamente correta
  DIVERGENCIA: "divergencia",    // diferença conhecida da metodologia APROVADA (D1, D2-C, D3-A, D4, D7-C, D11-A)
  LIMITACAO: "limitacao",        // diferença conhecida ligada a decisão AINDA PENDENTE (D5, D6, D8...)
  ECONOMICO: "economico",        // parâmetro pendente de validação econômica (T12)
};

// Status no relatório.
const STATUS = {
  OK: "OK",
  FALHOU: "FALHOU",
  DIV_CONFIRMADA: "DIVERGÊNCIA CONFIRMADA",
  DIV_NAO_REPRODUZIDA: "DIVERGÊNCIA NÃO REPRODUZIDA (revisar)",
  LIM_CONFIRMADA: "LIMITAÇÃO CONFIRMADA (decisão pendente)",
  LIM_NAO_REPRODUZIDA: "LIMITAÇÃO NÃO REPRODUZIDA (revisar)",
  PENDENTE: "PENDENTE DE VALIDAÇÃO ECONÔMICA",
  NAO_EXECUTADO: "NÃO EXECUTADO (dependência ausente)",
  ERRO: "ERRO AO EXECUTAR",
};

function iguais(obtido, esperado, tol) {
  if (esperado === null || esperado === undefined) return obtido === null || obtido === undefined;
  if (typeof esperado === "number") return typeof obtido === "number" && Number.isFinite(obtido) && Math.abs(obtido - esperado) <= (tol ?? 0) + 1e-12;
  if (typeof esperado === "boolean") return obtido === esperado;
  if (Array.isArray(esperado)) return Array.isArray(obtido) && esperado.length === obtido.length && esperado.every((e, i) => iguais(obtido[i], e, tol));
  return obtido === esperado;
}

const fmt = (v) => {
  if (v === null || v === undefined) return "—";
  if (typeof v === "number") return Number.isInteger(v) ? String(v) : v.toFixed(6).replace(/0+$/, "").replace(/\.$/, "");
  if (Array.isArray(v)) return "[" + v.map(fmt).join(", ") + "]";
  return String(v);
};

module.exports = { TOL, TIPO, STATUS, iguais, fmt };

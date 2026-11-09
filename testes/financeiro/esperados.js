// Valores esperados e premissas, copiados do Plano de Homologação v0.2
// (docs/academy/comando-05b/PLANO_TESTES_HOMOLOGACAO.md) e do Dicionário Financeiro v0.4.
// REGRA (Comando 05C, item 6): estes valores NÃO podem ser alterados para acomodar divergências.
// Qualquer mudança aqui exige nova versão do plano aprovada pelo Bruno.
"use strict";

const PLANO = "PLANO_TESTES_HOMOLOGACAO.md v0.2 (09/11/2026)";
const DICIONARIO = "DICIONARIO_FINANCEIRO.md v0.4 (09/11/2026)";

// T1 · Cenário Z-base (dados fictícios).
const ZBASE = {
  unidades: 3, diaria: 680, ocupacao: 0.38, dias: 365,
  deducoes: 0.17, variavelNoite: 80, fixoMensal: 6000,
  quebra: 0, proLabore: 0, reserva: 0,
  investimento: 900000, taxa: 0.10, horizonte: 10, multiploSaida: null,
};
const T1 = {
  receitaBruta: 282948.00,
  receitaReal: 234846.84,
  resultadoOperacional: 129558.84,
  ocupacaoEquilibrio: 0.1357,
  vpl: -103917.01,
  tir: 0.0724,
  paybackSimples: 6.95,
  paybackDescontado: null, // "não ocorre em 10 anos"
  retornoAnual: 0.1440,
  retornoAcumulado10: 0.4395,
};

// T2 · Z-completo (regras v0 da ZAIOS: quebra 1%, reserva 3% da receita bruta, rampa 40/50/75 a partir de janeiro).
const T2 = {
  semRampa: { resultadoOperacional: 126729.36, geracao: 118240.92, geracaoAno1: 118240.92, vpl: -173460.73, tir: 0.0530, payback: 7.61, vplSaida6x: 119697.19 },
  comRampa: { resultadoOperacional: 126729.36, geracao: 118240.92, geracaoAno1: 42405.16, vpl: -242402.34, tir: 0.0371, payback: 8.25, vplSaida6x: 50755.59 },
};

// T3 · Casos de referência (F01, F02, F03). Entradas dos casos F03 tiradas dos testes da própria ZAIOS
// (src/test/viabilidade.test.ts), lidos sem alterar nada.
const T3 = {
  F01: { linhas: { infra: 250000, projeto: 70000, obra: 390000, apoio: 90000, ffe: 195000 }, osePct: 0.12, prePct: 0.05, contingenciaPct: 0.25, capex: 1237400 },
  F02: { unidades: 3, diaria: 680, ocupacao: 0.38, deducoes: 0.17, fixoMensal: 10500, receitaReal: 234846.84, resultadoOperacional: 108846.84, equilibrioNoites: 223.25, ocupacaoEquilibrio: 0.204 },
  F03c1: { capex: 1237400, geracaoAno1: -59071.13, geracaoRegime: 34505.6, ebitdaRegime: 52505.6, vpl: -1110447.78, payback: 38.6, tirComSaida: -0.084 },
  F03c2: { capex: 1000000, geracaoAno1: 50000, geracaoRegime: 200000, ebitdaRegime: 230000, payback: 5.75, paybackDescontado: 8.82, vpl: 92549.78, vplComSaida: 624599.52 },
};

// T4 · Orçamento.
const T4 = {
  B06iniciante: { capex: 449500, inter: 524450, cons: 598617.50 },
  F05exemplo: { subtotal: 197040, reserva: 19704, total: 216744 },
};

// T7 · Régua Única (D11-A), sobre T1 com saída 6× EBITDA no critério 4.
const T7 = {
  conservador: { receitaBruta: 203722.56, geracao: 70459.32 },
  saida: { valorAno10: 777353.04, valorPresente: 299703.25, vplComSaida: 195786.24 },
  criterios: ["passa", "passa", "passa", "ajustar", "nao_avaliado"],
  apresentacao: "4 de 5 critérios avaliados. Sinal parcial, não representa aprovação do projeto.",
};

// T9 · Reserva e quebra sem dupla contagem (D2-C, D3-A).
const T9 = {
  deducoes: 48101.16, quebra: 2829.48, resultadoOperacional: 126729.36, reserva4: 11317.92, geracao: 115411.44,
  reservaRef: 0.04, reservaFaixa: [0.03, 0.06], quebraRef: 0.01,
};

// T10 · Pró-labore (D4).
const T10 = { proLaboreMes: 3464.00, proLaboreAno: 41568.00, resultadoComProLabore: 87990.84 };

// T11 · Valor de saída (D7-C). Custo de venda de 6% é ILUSTRATIVO (dados fictícios).
const T11 = { valorBruto6x: 777353.04, custoVendaIlustrativo: 46641.18, liquidoAntesTributos: 730711.86 };

// T12 · Parâmetros pendentes de validação econômica (referências atuais).
const T12 = [
  { parametro: "Deduções sobre a receita", referencia: 0.17, decisao: "v0" },
  { parametro: "Quebra e perdas", referencia: 0.01, decisao: "D3-A" },
  { parametro: "Reserva de reposição", referencia: 0.04, faixa: [0.03, 0.06], decisao: "D2-C" },
  { parametro: "Valor da hora do pró-labore (R$)", referencia: 40, decisao: "D4" },
  { parametro: "Rampa do 1º ano (meses 1–3, 4–6, 7–12)", referencia: [0.4, 0.5, 0.75], decisao: "v0" },
  { parametro: "OS&E sobre FF&E", referencia: 0.12, faixa: [0.10, 0.15], decisao: "v0" },
  { parametro: "Pré-abertura sobre a base", referencia: 0.05, faixa: [0.05, 0.10], decisao: "v0" },
  { parametro: "Contingência primeira obra", referencia: [0.20, 0.25], decisao: "v0" },
  { parametro: "Contingência com experiência", referencia: [0.10, 0.15], decisao: "v0" },
  { parametro: "Cenário conservador (diária, ocupação)", referencia: [-0.10, -0.20], decisao: "D10 pendente" },
  { parametro: "Cenário otimista (diária, ocupação)", referencia: [0.10, 0.15], decisao: "D10 pendente" },
  { parametro: "Múltiplo de saída (método 1)", referencia: 6, decisao: "D7-C" },
  { parametro: "Régua: payback passa / ajustar (anos)", referencia: [8, 12], decisao: "D11-A" },
  { parametro: "Régua: colchão mínimo sobre o CAPEX", referencia: 0.10, decisao: "D11-A" },
  { parametro: "Régua: déficit conservador aceito (meses de fixo)", referencia: 3, decisao: "D11-A" },
];

module.exports = { PLANO, DICIONARIO, ZBASE, T1, T2, T3, T4, T7, T9, T10, T11, T12 };

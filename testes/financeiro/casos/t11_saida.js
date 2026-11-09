// T11 · Métodos de valor de saída (D7-C).
"use strict";
const E = require("../esperados"), { TOL, TIPO } = require("../lib/base"), U = require("./_util");
module.exports = (D) => {
  const c = [], Z = D.zaios;
  const add = (o) => c.push(Object.assign({ teste: "T11", decisao: "D7-C" }, o));
  const ebitda = () => U.anoZaios(Z, E.ZBASE).ano.ebitda;
  add({ id: "T11-ZAIOS-01", ferramenta: "ZAIOS", indicador: "Método 1 · 6× EBITDA de 129.558,84", tipo: TIPO.FORMULA, esperado: E.T11.valorBruto6x, tol: TOL.reais, requer: "zaios", obter: () => Z.viabilidade.valorSaida(6, ebitda()) / 100 });
  add({ id: "T11-ZAIOS-02", ferramenta: "ZAIOS", indicador: "Métodos 2 e 3 (avaliação patrimonial, valor informado) e valor líquido de custos, tributos e obrigações", tipo: TIPO.DIVERGENCIA, esperado: true, requer: "zaios", nota: "A ZAIOS só tem o múltiplo do EBITDA.",
    obter: () => /patrimonial|valorLiquido|metodoSaida/i.test(D.zaiosFontes.viabilidade || "") });
  add({ id: "T11-ZAIOS-03", ferramenta: "ZAIOS", indicador: "Valor líquido com custo de venda ilustrativo de 6% (antes de tributos)", tipo: TIPO.DIVERGENCIA, esperado: E.T11.liquidoAntesTributos, tol: TOL.reais, requer: "zaios", nota: "Sem função de valor líquido; o custo de 6% é ilustrativo.",
    obter: () => (typeof Z.viabilidade.valorSaidaLiquido === "function" ? Z.viabilidade.valorSaidaLiquido({ bruto: Z.viabilidade.valorSaida(6, ebitda()), custoVendaPct: 0.06 }) / 100 : null) });
  add({ id: "T11-B08-01", ferramenta: "B08", indicador: "Saída aceita múltiplo do EBITDA (residual hoje em % do investimento, até 100%)", tipo: TIPO.DIVERGENCIA, esperado: true, requer: "arsenal",
    obter: () => U.contem(D.arsenal.carregarProduto("B08").fonte, /m[úu]ltiplo/i) });
  return c;
};

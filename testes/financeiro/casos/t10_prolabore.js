// T10 · Pró-labore, distribuição de resultados e caixa disponível (D4).
"use strict";
const E = require("../esperados"), { TOL, TIPO } = require("../lib/base"), U = require("./_util");
module.exports = (D) => {
  const c = [], Z = D.zaios;
  const add = (o) => c.push(Object.assign({ teste: "T10", decisao: "D4" }, o));
  add({ id: "T10-ZAIOS-01", ferramenta: "ZAIOS", indicador: "Pró-labore 20 h × R$ 40 × 4,33 por mês", tipo: TIPO.FORMULA, esperado: E.T10.proLaboreMes, tol: TOL.reais, requer: "zaios", obter: () => Z.receitas.retiradaMensal(20, 40) });
  add({ id: "T10-ZAIOS-02", ferramenta: "ZAIOS", indicador: "Pró-labore por ano", tipo: TIPO.FORMULA, esperado: E.T10.proLaboreAno, tol: TOL.reais, requer: "zaios", obter: () => U.anoZaios(Z, Object.assign({}, E.ZBASE, { proLaboreMes: E.T10.proLaboreMes })).ano.retirada / 100 });
  add({ id: "T10-ZAIOS-03", ferramenta: "ZAIOS", indicador: "Resultado operacional do T1 com pró-labore como custo fixo", tipo: TIPO.FORMULA, esperado: E.T10.resultadoComProLabore, tol: TOL.reais, requer: "zaios", obter: () => U.anoZaios(Z, Object.assign({}, E.ZBASE, { proLaboreMes: E.T10.proLaboreMes })).ano.resultadoOperacional / 100 });
  add({ id: "T10-ZAIOS-04", ferramenta: "ZAIOS", indicador: "Distribuição de resultados e caixa disponível separados do resultado", tipo: TIPO.DIVERGENCIA, esperado: true, requer: "zaios", nota: "A ZAIOS não tem distribuição nem caixa disponível.",
    obter: () => /distribui|caixaDisponivel/i.test((D.zaiosFontes.receitas || "") + (D.zaiosFontes.viabilidade || "")) });
  add({ id: "T10-J2-01", ferramenta: "Folha J2", indicador: "Pró-labore do exemplo (20 h × R$ 40 × 4,33)", tipo: TIPO.FORMULA, esperado: E.T10.proLaboreMes, tol: TOL.reais, requer: "folha", obter: () => { const F = D.folha.api; return F.calcular(F.normalizar(F.EXEMPLO)).retirada; } });
  add({ id: "T10-J2-02", ferramenta: "Folha J2", indicador: "Distribuição de resultados com nome próprio, fora do resultado", tipo: TIPO.DIVERGENCIA, esperado: true, requer: "folha", nota: "A Folha tem pró-labore e bloco de caixa, mas não nomeia a distribuição.",
    obter: () => D.folha.api.CAMPOS.some((x) => /distribui/i.test(x.id + " " + (x.r || ""))) });
  return c;
};

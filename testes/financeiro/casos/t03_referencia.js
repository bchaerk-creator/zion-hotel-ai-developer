// T3 · Casos de referência F01, F02 e F03 (Método Zion 360°), na ZAIOS.
"use strict";
const E = require("../esperados"), { TOL, TIPO } = require("../lib/base"), U = require("./_util");
module.exports = (D) => {
  const c = [], Z = D.zaios, R = U.R;
  const add = (o) => c.push(Object.assign({ teste: "T3", ferramenta: "ZAIOS", requer: "zaios", decisao: "v0", tipo: TIPO.FORMULA }, o));
  add({ id: "T3-F01-01", indicador: "F01 · CAPEX com contingência de 25% da base", esperado: E.T3.F01.capex, tol: TOL.reais, obter: () => {
    const { capex: K, tipos: T } = Z, l = E.T3.F01.linhas, ins = (n, v) => T.insumo(n, R(v));
    const base = K.baseContingencia(ins("infraestrutura", l.infra), ins("obra", l.obra), ins("apoio", l.apoio)).valor;
    const cont = K.contingenciaCapex(T.insumo("base", base), T.insumo("percentual", E.T3.F01.contingenciaPct)).valor;
    const ose = K.referenciaOse(R(l.ffe)), pre = K.referenciaPreAbertura(base);
    const linhas = [ins("infra", l.infra), ins("projeto", l.projeto), ins("obra", l.obra), ins("apoio", l.apoio), ins("ffe", l.ffe), T.insumo("ose", ose), T.insumo("pre", pre)];
    return K.capexComContingencia(linhas, T.insumo("contingência", cont)).valor / 100; } });
  const f02 = () => U.anoZaios(Z, { unidades: 3, diaria: 680, ocupacao: 0.38, deducoes: 0.17, variavelNoite: 0, fixoMensal: E.T3.F02.fixoMensal });
  add({ id: "T3-F02-01", indicador: "F02 · Receita real", esperado: E.T3.F02.receitaReal, tol: TOL.reais, obter: () => f02().ano.receitaReal / 100 });
  add({ id: "T3-F02-02", indicador: "F02 · Resultado operacional", esperado: E.T3.F02.resultadoOperacional, tol: TOL.reais, obter: () => f02().ano.resultadoOperacional / 100 });
  add({ id: "T3-F02-03", indicador: "F02 · Equilíbrio em noites", esperado: E.T3.F02.equilibrioNoites, tol: TOL.noites, obter: () => { const r = f02(); return Z.receitas.pontoEquilibrio(r.ano, r.p, 0.38).noites; } });
  add({ id: "T3-F02-04", indicador: "F02 · Ocupação de equilíbrio (20,4%)", esperado: E.T3.F02.ocupacaoEquilibrio, tol: TOL.pct1casa, obter: () => { const r = f02(); return Z.receitas.pontoEquilibrio(r.ano, r.p, 0.38).ocupacao; } });
  const c1 = () => Z.viabilidade.fluxoProjeto(R(E.T3.F03c1.capex), R(E.T3.F03c1.geracaoAno1), R(E.T3.F03c1.geracaoRegime));
  add({ id: "T3-F03-C1-1", indicador: "F03 caso 1 · VPL a 10%", esperado: E.T3.F03c1.vpl, tol: TOL.reais, obter: () => Z.viabilidade.vpl(c1(), 0.1) / 100 });
  add({ id: "T3-F03-C1-2", indicador: "F03 caso 1 · Payback simples estendido (38,6 anos)", esperado: E.T3.F03c1.payback, tol: TOL.anos1casa, obter: () => Z.viabilidade.paybackSimples(c1(), R(E.T3.F03c1.geracaoRegime)).anos });
  add({ id: "T3-F03-C1-3", indicador: "F03 caso 1 · TIR com saída 6× (−8,4%)", esperado: E.T3.F03c1.tirComSaida, tol: TOL.pct1casa, obter: () => Z.viabilidade.tir(Z.viabilidade.comSaida(c1(), Z.viabilidade.valorSaida(6, R(E.T3.F03c1.ebitdaRegime)))).taxa });
  const c2 = () => Z.viabilidade.fluxoProjeto(R(E.T3.F03c2.capex), R(E.T3.F03c2.geracaoAno1), R(E.T3.F03c2.geracaoRegime));
  add({ id: "T3-F03-C2-1", indicador: "F03 caso 2 · Payback simples", esperado: E.T3.F03c2.payback, tol: TOL.anos, obter: () => Z.viabilidade.paybackSimples(c2(), R(E.T3.F03c2.geracaoRegime)).anos });
  add({ id: "T3-F03-C2-2", indicador: "F03 caso 2 · Payback descontado", esperado: E.T3.F03c2.paybackDescontado, tol: TOL.anos, obter: () => Z.viabilidade.paybackDescontado(c2(), 0.1).anos });
  add({ id: "T3-F03-C2-3", indicador: "F03 caso 2 · VPL sem saída", esperado: E.T3.F03c2.vpl, tol: TOL.reais, obter: () => Z.viabilidade.vpl(c2(), 0.1) / 100 });
  add({ id: "T3-F03-C2-4", indicador: "F03 caso 2 · VPL com saída 6×", esperado: E.T3.F03c2.vplComSaida, tol: TOL.reais, obter: () => Z.viabilidade.vpl(Z.viabilidade.comSaida(c2(), Z.viabilidade.valorSaida(6, R(E.T3.F03c2.ebitdaRegime))), 0.1) / 100 });
  return c;
};

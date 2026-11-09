// T1 · Cenário Z-base: premissas idênticas em todas as ferramentas de resultado.
"use strict";
const E = require("../esperados"), { TOL, TIPO } = require("../lib/base"), U = require("./_util");
module.exports = (D) => {
  const c = [];
  const add = (o) => c.push(Object.assign({ teste: "T1" }, o));
  const Z = D.zaios;
  const z = () => U.viabZaios(Z, E.ZBASE, { investimento: E.ZBASE.investimento });
  // ZAIOS
  add({ id: "T1-ZAIOS-01", ferramenta: "ZAIOS", indicador: "Receita bruta/ano", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.receitaBruta, tol: TOL.reais, requer: "zaios", obter: () => z().ano.receitaBruta / 100 });
  add({ id: "T1-ZAIOS-02", ferramenta: "ZAIOS", indicador: "Receita real", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.receitaReal, tol: TOL.reais, requer: "zaios", obter: () => z().ano.receitaReal / 100 });
  add({ id: "T1-ZAIOS-03", ferramenta: "ZAIOS", indicador: "Resultado operacional", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.resultadoOperacional, tol: TOL.reais, requer: "zaios", obter: () => z().ano.resultadoOperacional / 100 });
  add({ id: "T1-ZAIOS-04", ferramenta: "ZAIOS", indicador: "Ocupação de equilíbrio", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.ocupacaoEquilibrio, tol: TOL.pct, requer: "zaios", obter: () => { const r = z(); return Z.receitas.pontoEquilibrio(r.ano, r.p, E.ZBASE.ocupacao).ocupacao; } });
  add({ id: "T1-ZAIOS-05", ferramenta: "ZAIOS", indicador: "VPL a 10%", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.vpl, tol: TOL.reais, requer: "zaios", obter: () => Z.viabilidade.vpl(z().f, E.ZBASE.taxa) / 100 });
  add({ id: "T1-ZAIOS-06", ferramenta: "ZAIOS", indicador: "TIR", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.tir, tol: TOL.pct, requer: "zaios", obter: () => Z.viabilidade.tir(z().f).taxa });
  add({ id: "T1-ZAIOS-07", ferramenta: "ZAIOS", indicador: "Payback simples", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.paybackSimples, tol: TOL.anos, requer: "zaios", obter: () => { const r = z(); return Z.viabilidade.paybackSimples(r.f, r.ger).anos; } });
  add({ id: "T1-ZAIOS-08", ferramenta: "ZAIOS", indicador: "Payback descontado (não ocorre em 10 anos)", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.paybackDescontado, requer: "zaios", obter: () => Z.viabilidade.paybackDescontado(z().f, E.ZBASE.taxa).anos });
  add({ id: "T1-ZAIOS-09", ferramenta: "ZAIOS", indicador: "Retorno anual sobre o investimento", decisao: "D1", tipo: TIPO.FORMULA, esperado: E.T1.retornoAnual, tol: TOL.pct, requer: "zaios", obter: () => { const r = z(); return Z.viabilidade.retornoSimples(r.ger, U.R(E.ZBASE.investimento)); } });
  add({ id: "T1-ZAIOS-10", ferramenta: "ZAIOS", indicador: "Retorno acumulado em 10 anos", decisao: "D1", tipo: TIPO.DIVERGENCIA, esperado: E.T1.retornoAcumulado10, tol: TOL.pct, requer: "zaios", nota: "A ZAIOS não calcula o retorno acumulado (aderência parcial à D1).",
    obter: () => { const r = z(); return typeof Z.viabilidade.retornoAcumulado === "function" ? Z.viabilidade.retornoAcumulado(r.f, U.R(E.ZBASE.investimento)) : null; } });
  // B08
  const b = () => D.arsenal.rodar("B08", U.b08Z(), {});
  add({ id: "T1-B08-01", ferramenta: "B08", indicador: "Receita bruta/ano", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.receitaBruta, tol: TOL.reais, requer: "arsenal", obter: () => D.arsenal.pegar(b(), "base.anos.0.receita") });
  add({ id: "T1-B08-02", ferramenta: "B08", indicador: "Receita real", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.receitaReal, tol: TOL.reais, requer: "arsenal", obter: () => { const a = D.arsenal.pegar(b(), "base.anos.0"); return a.receita - a.deducoes; } });
  add({ id: "T1-B08-03", ferramenta: "B08", indicador: "Resultado operacional", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.resultadoOperacional, tol: TOL.reais, requer: "arsenal", obter: () => b().fc1 });
  add({ id: "T1-B08-04", ferramenta: "B08", indicador: "Ocupação de equilíbrio", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.ocupacaoEquilibrio, tol: TOL.pct, requer: "arsenal", obter: () => b().occBE });
  add({ id: "T1-B08-05", ferramenta: "B08", indicador: "VPL a 10%", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.vpl, tol: TOL.reais, requer: "arsenal", obter: () => b().vpl });
  add({ id: "T1-B08-06", ferramenta: "B08", indicador: "TIR", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.tir, tol: TOL.pct, requer: "arsenal", obter: () => b().tir });
  add({ id: "T1-B08-07", ferramenta: "B08", indicador: "Payback simples", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.paybackSimples, tol: TOL.anos, requer: "arsenal", obter: () => b().paybackS });
  add({ id: "T1-B08-08", ferramenta: "B08", indicador: "Payback descontado (não ocorre em 10 anos)", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.paybackDescontado, requer: "arsenal", obter: () => b().paybackD });
  add({ id: "T1-B08-09", ferramenta: "B08", indicador: "Retorno anual (valor)", decisao: "D1", tipo: TIPO.FORMULA, esperado: E.T1.retornoAnual, tol: TOL.pct, requer: "arsenal", obter: () => D.arsenal.pegar(b(), "base.roiEstab") });
  add({ id: "T1-B08-10", ferramenta: "B08", indicador: "Retorno acumulado em 10 anos (valor)", decisao: "D1", tipo: TIPO.FORMULA, esperado: E.T1.retornoAcumulado10, tol: TOL.pct, requer: "arsenal", obter: () => b().roi10 });
  // A09 (365 dias, informando 365/12 noites por mês)
  const a = () => D.arsenal.rodar("A09", U.a09Z(), {});
  add({ id: "T1-A09-01", ferramenta: "A09", indicador: "Receita bruta/ano (365 dias)", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.receitaBruta, tol: TOL.reais, requer: "arsenal", obter: () => a().cen[1].recBruta });
  add({ id: "T1-A09-02", ferramenta: "A09", indicador: "Receita real", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.receitaReal, tol: TOL.reais, requer: "arsenal", obter: () => a().cen[1].recBruta - a().cen[1].ded });
  add({ id: "T1-A09-03", ferramenta: "A09", indicador: "Resultado operacional", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.resultadoOperacional, tol: TOL.reais, requer: "arsenal", obter: () => a().cen[1].resultado });
  add({ id: "T1-A09-04", ferramenta: "A09", indicador: "Ocupação de equilíbrio", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.ocupacaoEquilibrio, tol: TOL.pct, requer: "arsenal", obter: () => a().occBE });
  add({ id: "T1-A09-05", ferramenta: "A09", indicador: "Payback (simplificado, sem rampa)", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T1.paybackSimples, tol: TOL.anos, requer: "arsenal", obter: () => a().cen[1].payback });
  add({ id: "T1-A09-06", ferramenta: "A09", indicador: "Retorno anual (valor)", decisao: "D1", tipo: TIPO.FORMULA, esperado: E.T1.retornoAnual, tol: TOL.pct, requer: "arsenal", obter: () => a().cen[1].roi });
  add({ id: "T1-A09-07", ferramenta: "A09", indicador: "Receita bruta/ano com o campo como a interface permite (30 noites × 12)", decisao: "D5 (pendente)", tipo: TIPO.LIMITACAO, esperado: E.T1.receitaBruta, tol: TOL.reais, requer: "arsenal", nota: "O campo de noites por mês é inteiro: 360 dias no máximo.", obter: () => D.arsenal.rodar("A09", U.a09Z({ rc_noites: 30 }), {}).cen[1].recBruta });
  return c;
};

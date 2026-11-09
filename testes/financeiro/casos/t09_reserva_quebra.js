// T9 · Reserva de reposição e quebra sem dupla contagem (D2-C e D3-A).
"use strict";
const E = require("../esperados"), { TOL, TIPO } = require("../lib/base"), U = require("./_util");
module.exports = (D) => {
  const c = [], Z = D.zaios;
  const add = (o) => c.push(Object.assign({ teste: "T9" }, o));
  const o = Object.assign({}, E.ZBASE, { quebra: E.T9.quebraRef, reserva: E.T9.reservaRef });
  const z = () => U.anoZaios(Z, o).ano;
  add({ id: "T9-ZAIOS-01", ferramenta: "ZAIOS", decisao: "v0", indicador: "Deduções (17%) sem quebra nem reserva", tipo: TIPO.FORMULA, esperado: E.T9.deducoes, tol: TOL.reais, requer: "zaios", obter: () => z().deducoes / 100 });
  add({ id: "T9-ZAIOS-02", ferramenta: "ZAIOS", decisao: "D3-A", indicador: "Quebra de 1% como custo variável", tipo: TIPO.FORMULA, esperado: E.T9.quebra, tol: TOL.reais, requer: "zaios", obter: () => { const a = z(); return (a.custosVariaveis - a.noitesVendidas * U.R(E.ZBASE.variavelNoite)) / 100; } });
  add({ id: "T9-ZAIOS-03", ferramenta: "ZAIOS", decisao: "D3-A", indicador: "Resultado operacional com quebra", tipo: TIPO.FORMULA, esperado: E.T9.resultadoOperacional, tol: TOL.reais, requer: "zaios", obter: () => z().resultadoOperacional / 100 });
  add({ id: "T9-ZAIOS-04", ferramenta: "ZAIOS", decisao: "D2-C", indicador: "Reserva de 4% da receita bruta (informada) abaixo do EBITDA", tipo: TIPO.FORMULA, esperado: E.T9.reserva4, tol: TOL.reais, requer: "zaios", obter: () => z().reserva / 100 });
  add({ id: "T9-ZAIOS-05", ferramenta: "ZAIOS", decisao: "D2-C", indicador: "Geração de caixa (a cascata fecha, reserva sai uma vez)", tipo: TIPO.FORMULA, esperado: E.T9.geracao, tol: TOL.reais, requer: "zaios", obter: () => z().geracaoCaixa / 100 });
  add({ id: "T9-ZAIOS-06", ferramenta: "ZAIOS", decisao: "D2-C", indicador: "Referência da reserva de reposição = 4%", tipo: TIPO.DIVERGENCIA, esperado: E.T9.reservaRef, tol: 1e-9, requer: "zaios", nota: "A ZAIOS usa 3% (REF_RESERVA).", obter: () => Z.receitas.REF_RESERVA });
  add({ id: "T9-ZAIOS-07", ferramenta: "ZAIOS", decisao: "D2-C", indicador: "Faixa da reserva de reposição = 3% a 6%", tipo: TIPO.DIVERGENCIA, esperado: E.T9.reservaFaixa, tol: 1e-9, requer: "zaios", nota: "A ZAIOS usa 3% a 5% (RESERVA_FAIXA). Achado novo deste comando.", obter: () => Z.receitas.RESERVA_FAIXA });
  add({ id: "T9-ZAIOS-08", ferramenta: "ZAIOS", decisao: "D3-A", indicador: "Aceita quebra medida em R$ (prioridade ao valor real)", tipo: TIPO.DIVERGENCIA, esperado: true, requer: "zaios", nota: "O P6 só aceita a quebra em percentual.", obter: () => /quebra(Valor|Medida|Reais)/.test(D.zaiosFontes.receitas || "") });
  // Folha J2
  const F = () => D.folha.api, j = (s) => F().calcular(F().normalizar(s || F().EXEMPLO));
  add({ id: "T9-J2-01", ferramenta: "Folha J2", decisao: "D2-C", indicador: "Referência da reserva = 4%, faixa 3% a 6%", tipo: TIPO.FORMULA, esperado: [4, 3, 6], requer: "folha", obter: () => [F().REF.reservaPct, F().REF.reservaMin, F().REF.reservaMax] });
  add({ id: "T9-J2-02", ferramenta: "Folha J2", decisao: "D2-C", indicador: "Reserva = 4% da receita bruta realizada (exemplo: 4% × 17.220,00 = 688,80)", tipo: TIPO.DIVERGENCIA, esperado: 688.80, tol: TOL.reais, requer: "folha", nota: "A Folha aplica 4% sobre a receita real (542,62).", obter: () => j().reservaReposicao });
  add({ id: "T9-J2-03", ferramenta: "Folha J2", decisao: "D3-A", indicador: "Quebra sem medição = 1% da receita de hospedagem (162,40)", tipo: TIPO.FORMULA, esperado: 162.40, tol: TOL.reais, requer: "folha", obter: () => j().quebraValor });
  add({ id: "T9-J2-04", ferramenta: "Folha J2", decisao: "D3-A", indicador: "Quebra medida em R$ tem prioridade (informada 150,00)", tipo: TIPO.FORMULA, esperado: 150, tol: TOL.reais, requer: "folha", obter: () => j(Object.assign({}, F().EXEMPLO, { quebra: 150, quebraRef: false })).quebraValor });
  add({ id: "T9-J2-05", ferramenta: "Folha J2", decisao: "D3-A", indicador: "Deduções não contêm quebra (650 + 18,5% × 16.240 = 3.654,40)", tipo: TIPO.FORMULA, esperado: 3654.40, tol: TOL.reais, requer: "folha", obter: () => j().deducoes });
  // B08 e A09
  add({ id: "T9-B08-01", ferramenta: "B08", decisao: "D2-C", indicador: "Reserva de 4% fora das deduções (deduções continuam 48.101,16)", tipo: TIPO.DIVERGENCIA, esperado: E.T9.deducoes, tol: TOL.reais, requer: "arsenal", nota: "O B08 soma a reserva às deduções.", obter: () => D.arsenal.pegar(D.arsenal.rodar("B08", U.b08Z({ reserva: 4 }), {}), "base.anos.0.deducoes") });
  add({ id: "T9-B08-02", ferramenta: "B08", decisao: "D3-A", indicador: "Quebra como custo variável disponível", tipo: TIPO.DIVERGENCIA, esperado: true, requer: "arsenal", obter: () => U.camposDe(D.arsenal.carregarProduto("B08").fonte).some((x) => /quebra/.test(x)) });
  add({ id: "T9-A09-01", ferramenta: "A09", decisao: "D3-A", indicador: "Quebra como custo variável disponível", tipo: TIPO.DIVERGENCIA, esperado: true, requer: "arsenal", obter: () => U.camposDe(D.arsenal.carregarProduto("A09").fonte).some((x) => /quebra/.test(x)) });
  return c;
};

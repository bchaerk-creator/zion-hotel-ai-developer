// T5 · Folha Única J2 x ZAIOS (mês real): a cascata fecha e o pró-labore usa a mesma regra.
"use strict";
const { TOL, TIPO } = require("../lib/base");
module.exports = (D) => {
  const c = [];
  const add = (o) => c.push(Object.assign({ teste: "T5", requer: "folha" }, o));
  const r = () => { const F = D.folha.api; return F.calcular(F.normalizar(F.EXEMPLO)); };
  add({ id: "T5-J2-01", ferramenta: "Folha J2", indicador: "Receita real − custos variáveis = margem de contribuição", decisao: "v0", tipo: TIPO.FORMULA, esperado: 0, tol: TOL.reais, obter: () => { const x = r(); return x.receitaReal - x.variaveis - x.margemContribuicao; } });
  add({ id: "T5-J2-02", ferramenta: "Folha J2", indicador: "Margem de contribuição − fixos = resultado operacional", decisao: "v0", tipo: TIPO.FORMULA, esperado: 0, tol: TOL.reais, obter: () => { const x = r(); return x.margemContribuicao - x.fixosOperacionais - x.resultadoOperacional; } });
  add({ id: "T5-J2-03", ferramenta: "Folha J2", indicador: "Resultado operacional − custos do modelo = EBITDA", decisao: "v0", tipo: TIPO.FORMULA, esperado: 0, tol: TOL.reais, obter: () => { const x = r(); return x.resultadoOperacional - x.custosModelo - x.ebitda; } });
  add({ id: "T5-J2-04", ferramenta: "Folha J2", indicador: "EBITDA − reserva de reposição = geração de caixa", decisao: "v0", tipo: TIPO.FORMULA, esperado: 0, tol: TOL.reais, obter: () => { const x = r(); return x.ebitda - x.reservaReposicao - x.geracaoCaixa; } });
  add({ id: "T5-J2-05", ferramenta: "Folha J2 × ZAIOS", indicador: "Pró-labore 20 h × R$ 40 × 4,33 igual nas duas", decisao: "D4", tipo: TIPO.FORMULA, esperado: 0, tol: TOL.reais, requer: "folha+zaios",
    obter: () => r().retirada - D.zaios.receitas.retiradaMensal(20, 40) });
  return c;
};

// T7 · Régua Única de Viabilidade (D11-A), sobre o T1 com saída 6× EBITDA no critério 4.
"use strict";
const E = require("../esperados"), { TOL, TIPO } = require("../lib/base"), U = require("./_util");
module.exports = (D) => {
  const c = [], Z = D.zaios, V = () => Z.viabilidade;
  const add = (o) => c.push(Object.assign({ teste: "T7", decisao: "D11-A" }, o));
  const base = () => U.viabZaios(Z, E.ZBASE, { investimento: E.ZBASE.investimento });
  const cons = () => U.anoZaios(Z, Object.assign({}, E.ZBASE, { diaria: E.ZBASE.diaria * 0.9, ocupacao: E.ZBASE.ocupacao * 0.8 })).ano;
  const saida = () => { const b = base(); return V().valorSaida(6, b.ano.ebitda); };
  const criterios = () => { const b = base(); const vS = V().vpl(b.f, 0.1), vC = V().vpl(V().comSaida(b.f, saida()), 0.1);
    return [V().passoBase(b.ger), V().passoConservador(cons().geracaoCaixa, U.R(E.ZBASE.fixoMensal)), V().passoPayback(V().paybackSimples(b.f, b.ger).anos), V().passoVpl(vS, vC), "nao_avaliado"]; };
  add({ id: "T7-ZAIOS-01", ferramenta: "ZAIOS", indicador: "Conservador · receita bruta (diária 612, ocupação 30,4%)", tipo: TIPO.FORMULA, esperado: E.T7.conservador.receitaBruta, tol: TOL.reais, requer: "zaios", obter: () => cons().receitaBruta / 100 });
  add({ id: "T7-ZAIOS-02", ferramenta: "ZAIOS", indicador: "Conservador · geração de caixa", tipo: TIPO.FORMULA, esperado: E.T7.conservador.geracao, tol: TOL.reais, requer: "zaios", obter: () => cons().geracaoCaixa / 100 });
  add({ id: "T7-ZAIOS-03", ferramenta: "ZAIOS", indicador: "Valor de saída no ano 10 (6× EBITDA)", tipo: TIPO.FORMULA, esperado: E.T7.saida.valorAno10, tol: TOL.reais, requer: "zaios", obter: () => saida() / 100 });
  add({ id: "T7-ZAIOS-04", ferramenta: "ZAIOS", indicador: "Valor presente da saída", tipo: TIPO.FORMULA, esperado: E.T7.saida.valorPresente, tol: TOL.reais, requer: "zaios", obter: () => saida() / Math.pow(1.1, 10) / 100 });
  add({ id: "T7-ZAIOS-05", ferramenta: "ZAIOS", indicador: "VPL com saída", tipo: TIPO.FORMULA, esperado: E.T7.saida.vplComSaida, tol: TOL.reais, requer: "zaios", obter: () => V().vpl(V().comSaida(base().f, saida()), 0.1) / 100 });
  add({ id: "T7-ZAIOS-06", ferramenta: "ZAIOS", indicador: "Resultado dos 5 critérios (o 5º não avaliável no T1)", tipo: TIPO.FORMULA, esperado: E.T7.criterios, requer: "zaios", obter: criterios });
  add({ id: "T7-ZAIOS-07", ferramenta: "ZAIOS", indicador: "Borda · payback de 8,00 anos passa", tipo: TIPO.FORMULA, esperado: "passa", requer: "zaios", obter: () => V().passoPayback(8) });
  add({ id: "T7-ZAIOS-08", ferramenta: "ZAIOS", indicador: "Borda · payback de 12,00 anos pede ajuste", tipo: TIPO.FORMULA, esperado: "ajustar", requer: "zaios", obter: () => V().passoPayback(12) });
  add({ id: "T7-ZAIOS-09", ferramenta: "ZAIOS", indicador: "Borda · payback acima de 12 pede redesenho", tipo: TIPO.FORMULA, esperado: "redesenhar", requer: "zaios", obter: () => V().passoPayback(12.01) });
  add({ id: "T7-ZAIOS-10", ferramenta: "ZAIOS", indicador: "Borda · colchão de 10% passa", tipo: TIPO.FORMULA, esperado: "passa", requer: "zaios", obter: () => V().passoColchao(0.1) });
  add({ id: "T7-ZAIOS-11", ferramenta: "ZAIOS", indicador: "Borda · déficit igual a 3 × fixo pede ajuste", tipo: TIPO.FORMULA, esperado: "ajustar", requer: "zaios", obter: () => V().passoConservador(-U.R(18000), U.R(6000)) });
  add({ id: "T7-ZAIOS-12", ferramenta: "ZAIOS", indicador: "Borda · déficit acima de 3 × fixo pede redesenho", tipo: TIPO.FORMULA, esperado: "redesenhar", requer: "zaios", obter: () => V().passoConservador(-U.R(18000) - 1, U.R(6000)) });
  add({ id: "T7-ZAIOS-13", ferramenta: "ZAIOS", indicador: "Leitura: um 'redesenhar' dá Redesenhar; só 'ajustar' dá Ajustar; tudo 'passa' dá Avançar", tipo: TIPO.FORMULA, esperado: ["Redesenhar", "Ajustar", "Avançar"], requer: "zaios",
    obter: () => [V().leituraDecisao(["passa", "redesenhar", "passa", "passa", "passa"]), V().leituraDecisao(["passa", "ajustar", "passa", "passa", "passa"]), V().leituraDecisao(Array(5).fill("passa"))] });
  add({ id: "T7-ZAIOS-14", ferramenta: "ZAIOS", indicador: "Apresentação com 4 de 5 critérios: sinal parcial, sem veredito", tipo: TIPO.DIVERGENCIA, esperado: E.T7.apresentacao, requer: "zaios",
    nota: "A ZAIOS calcula o veredito com qualquer quantidade de passos e não tem trava de homologação.",
    obter: () => (typeof V().sinalParcial === "function" ? V().sinalParcial(criterios()) : V().leituraDecisao(criterios().filter((x) => x !== "nao_avaliado"))) });
  for (const id of ["B08", "A09"]) {
    add({ id: `T7-${id}-01`, ferramenta: id, indicador: "Mostra 'X de 5 critérios avaliados. Sinal parcial…'", tipo: TIPO.DIVERGENCIA, esperado: true, requer: "arsenal",
      obter: () => U.contem(D.arsenal.carregarProduto(id).fonte, /crit[ée]rios avaliados/i) });
  }
  add({ id: "T7-A09-02", ferramenta: "A09", indicador: "Metas pessoais (prazo e retorno desejados) em bloco separado da Régua Zion", tipo: TIPO.DIVERGENCIA, esperado: true, requer: "arsenal",
    nota: "Hoje os avisos de meta aparecem misturados aos demais.", obter: () => U.contem(D.arsenal.carregarProduto("A09").fonte, /sua meta/i) });
  return c;
};

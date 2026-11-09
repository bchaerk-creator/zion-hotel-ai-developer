// T6 · Limites e erros.
"use strict";
const { TIPO } = require("../lib/base"), U = require("./_util");
module.exports = (D) => {
  const c = [], Z = D.zaios;
  const add = (o) => c.push(Object.assign({ teste: "T6" }, o));
  add({ id: "T6-ZAIOS-01", ferramenta: "ZAIOS", indicador: "TIR inexistente quando o fluxo não muda de sinal", decisao: "v0", tipo: TIPO.FORMULA, esperado: null, requer: "zaios", obter: () => Z.viabilidade.tir([-100, -10, -10]).taxa });
  add({ id: "T6-ZAIOS-02", ferramenta: "ZAIOS", indicador: "Aviso de mais de uma TIR com duas trocas de sinal", decisao: "v0", tipo: TIPO.FORMULA, esperado: true, requer: "zaios", obter: () => Z.viabilidade.tir([-100, 230, -132]).podeTerMaisDeUma });
  add({ id: "T6-ZAIOS-03", ferramenta: "ZAIOS", indicador: "Payback acima do horizonte marcado como estendido", decisao: "v0", tipo: TIPO.FORMULA, esperado: true, requer: "zaios", obter: () => Z.viabilidade.paybackSimples(Z.viabilidade.fluxoProjeto(U.R(1237400), U.R(-59071.13), U.R(34505.6)), U.R(34505.6)).estendido });
  add({ id: "T6-ZAIOS-04", ferramenta: "ZAIOS", indicador: "Sem equilíbrio quando a diária é menor que o custo variável", decisao: "v0", tipo: TIPO.FORMULA, esperado: null, requer: "zaios",
    obter: () => { const r = U.anoZaios(Z, { unidades: 3, diaria: 70, ocupacao: 0.38, deducoes: 0.17, variavelNoite: 80, fixoMensal: 6000 }); return Z.receitas.pontoEquilibrio(r.ano, r.p, 0.38).noites; } });
  add({ id: "T6-ZAIOS-05", ferramenta: "ZAIOS", indicador: "Sem equilíbrio com ocupação 0%", decisao: "v0", tipo: TIPO.FORMULA, esperado: null, requer: "zaios",
    obter: () => { const r = U.anoZaios(Z, { unidades: 3, diaria: 680, ocupacao: 0, deducoes: 0.17, variavelNoite: 80, fixoMensal: 6000 }); return Z.receitas.pontoEquilibrio(r.ano, r.p, 0).noites; } });
  add({ id: "T6-ZAIOS-06", ferramenta: "ZAIOS", indicador: "Geração do regime negativa: não se paga", decisao: "v0", tipo: TIPO.FORMULA, esperado: null, requer: "zaios", obter: () => Z.viabilidade.paybackSimples(Z.viabilidade.fluxoProjeto(100, 10, -5), -5).anos });
  add({ id: "T6-B08-01", ferramenta: "B08", indicador: "Payback acima de 10 anos com valor estendido (padrão proposto)", decisao: "D8 (pendente)", tipo: TIPO.LIMITACAO, esperado: "número acima de 10", requer: "arsenal", nota: "O B08 devolve nulo acima de 10 anos.",
    obter: () => { const p = D.arsenal.rodar("B08", U.b08Z({ invest: 3000000 }), {}).paybackS; return typeof p === "number" && p > 10 ? "número acima de 10" : p; } });
  return c;
};

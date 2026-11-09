// T2 · Z-completo: regras v0 da ZAIOS (quebra 1%, reserva 3% da receita bruta, rampa 40/50/75 a partir de janeiro).
// Valores do plano calculados com a reserva v0 de 3%. A reserva aprovada na D2-C (4%) é testada no T9.
"use strict";
const E = require("../esperados"), { TOL, TIPO } = require("../lib/base"), U = require("./_util");
module.exports = (D) => {
  const c = [], Z = D.zaios;
  const o = Object.assign({}, E.ZBASE, { quebra: 0.01, reserva: 0.03 });
  for (const [modo, rampa, exp] of [["sem rampa", false, E.T2.semRampa], ["com rampa", true, E.T2.comRampa]]) {
    const r = () => U.viabZaios(Z, o, { rampa, investimento: E.ZBASE.investimento });
    const tag = rampa ? "R" : "S";
    const add = (k, ind, esp, tol, f) => c.push({ teste: "T2", id: `T2-ZAIOS-${tag}${k}`, ferramenta: "ZAIOS", indicador: `${ind} (${modo})`, decisao: "v0", tipo: TIPO.FORMULA, esperado: esp, tol, requer: "zaios", obter: f });
    add("1", "Resultado operacional (regime)", exp.resultadoOperacional, TOL.reais, () => r().ano.resultadoOperacional / 100);
    add("2", "Geração de caixa (regime)", exp.geracao, TOL.reais, () => r().ger / 100);
    add("3", "Geração do 1º ano", exp.geracaoAno1, TOL.reais, () => r().a1 / 100);
    add("4", "VPL a 10%", exp.vpl, TOL.reais, () => Z.viabilidade.vpl(r().f, 0.1) / 100);
    add("5", "TIR", exp.tir, TOL.pct, () => Z.viabilidade.tir(r().f).taxa);
    add("6", "Payback simples", exp.payback, TOL.anos, () => { const x = r(); return Z.viabilidade.paybackSimples(x.f, x.ger).anos; });
    add("7", "VPL com saída 6× EBITDA", exp.vplSaida6x, TOL.reais, () => { const x = r(); return Z.viabilidade.vpl(Z.viabilidade.comSaida(x.f, Z.viabilidade.valorSaida(6, x.ano.ebitda)), 0.1) / 100; });
  }
  return c;
};

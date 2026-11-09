// Montagem de parâmetros para os motores (somente leitura).
"use strict";
const R = (reais) => Math.round(reais * 100); // ZAIOS trabalha em centavos inteiros

// Parâmetros do P6 da ZAIOS para um cenário de temporada única.
function paramsP6(o) {
  return {
    unidades: o.unidades, temporadaDoMes: Array(12).fill("media"),
    diaria: { alta: null, media: R(o.diaria), baixa: null }, ocupacao: { alta: null, media: o.ocupacao, baixa: null },
    outrasPct: 0, deducoesPct: o.deducoes, variavelNoite: R(o.variavelNoite || 0), custoEstadia: 0, permanencia: null,
    quebraPct: o.quebra || 0, fixoMensal: R(o.fixoMensal), retirada: R(o.proLaboreMes || 0),
    aluguel: 0, gestaoPct: 0, royaltyPct: 0, reservaPct: o.reserva || 0,
  };
}
function anoZaios(Z, o) {
  const p = paramsP6(o);
  return { p, ano: Z.receitas.somarMeses(Z.receitas.anoRegime(p)) };
}
function viabZaios(Z, o, { rampa = false, investimento }) {
  const { p, ano } = anoZaios(Z, o);
  const ger = ano.geracaoCaixa;
  const a1 = rampa ? Z.receitas.somarMeses(Z.receitas.primeiroAno(p, 0)).geracaoCaixa : ger;
  const f = Z.viabilidade.fluxoProjeto(R(investimento), a1, ger);
  return { p, ano, ger, a1, f };
}

// Entradas equivalentes ao Z-base para B08 e A09 (mesmos dias, despesas e tributos; sem rampa, reajuste ou variações).
const b08Z = (extra = {}) => Object.assign({ invest: 900000, unidades: 3, noites_ano: 365, diaria: 680, reajuste: 0, extras: 0, ocup1: 38, ocup_est: 38, rampa: 1, cf_ano: 72000, cv_noite: 80, comissao: 0, imposto: 17, reserva: 0, taxa: 10, var_ocup: 0, var_diaria: 0, var_invest: 0 }, extra);
// A09 cobra custo variável por estadia: 160 por estadia ÷ 2 noites = 80 por noite (equivalente).
const a09Z = (extra = {}) => Object.assign({ unidades: 3, inv: [{ name: "Construção", value: 900000 }], infra: [], inv_cont: 0, rc_diaria: 680, rc_ocup: 38, rc_noites: 365 / 12, rc_meses: 12, co_fixos: [{ name: "Fixos", value: 6000 }], co_estadia: 160, co_estmedia: 2, co_comissao: 0, co_imposto: 17, ce_var_ocup: 0, ce_var_diaria: 0, ind_ref: 10, ind_prazo: 8 }, extra);

// Ids de campos declarados no arquivo de uma mini mentoria.
const camposDe = (fonte) => [...fonte.matchAll(/\{id:'([a-z_0-9]+)'/g)].map((m) => m[1]);
const contem = (fonte, re) => re.test(fonte);

module.exports = { R, paramsP6, anoZaios, viabZaios, b08Z, a09Z, camposDe, contem };

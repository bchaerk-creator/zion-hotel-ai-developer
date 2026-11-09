// Testes complementares (Comando 05E) · B08, A09, B06, F05 e Folha J2.
// Valores esperados: independente/esperados_complementares.json, gerado por
// independente/complementares_referencia.py (cálculo independente, sem ler o código das ferramentas).
"use strict";
const path = require("path"), fs = require("fs");
const { TOL, TIPO } = require("../lib/base"), U = require("./_util");
const X = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "independente", "esperados_complementares.json"), "utf8"));
module.exports = (D) => {
  const c = [];
  const add = (o) => c.push(Object.assign({ teste: "C" }, o));
  // ---------- B08 ----------
  const b8 = (extra) => D.arsenal.rodar("B08", Object.assign({ invest: 1200000, unidades: 4, noites_ano: 365, diaria: 500, reajuste: 5, extras: 10, ocup1: 25, ocup_est: 40, rampa: 3, cf_ano: 90000, cv_noite: 70, comissao: 15, imposto: 6, reserva: 0, taxa: 12, var_ocup: 0, var_diaria: 0, var_invest: 0 }, extra || {}), {});
  for (const [k, ind, tol] of [["fc1", "Fluxo do ano 1 (rampa 25%→40% em 3 anos, reajuste 5%, extras 10%)", TOL.reais], ["vpl", "VPL a 12%", TOL.reais], ["tir", "TIR", TOL.pct], ["paybackS", "Payback simples", TOL.anos], ["paybackD", "Payback descontado (não ocorre em 10 anos)", TOL.anos], ["roi10", "Retorno acumulado em 10 anos (valor)", TOL.pct]])
    add({ id: `C-B08-R-${k}`, ferramenta: "B08", indicador: ind, decisao: "v0", tipo: TIPO.FORMULA, esperado: X.b08_rampa[k], tol, requer: "arsenal", obter: () => b8()[k] });
  for (const [k, ind, tol] of [["vpl", "VPL a 12% com valor residual de 50%", TOL.reais], ["tir", "TIR com valor residual", TOL.pct], ["roi10", "Retorno acumulado com residual (valor)", TOL.pct], ["paybackS", "Payback simples (o residual não entra)", TOL.anos]])
    add({ id: `C-B08-V-${k}`, ferramenta: "B08", indicador: ind, decisao: "D7-C (método residual)", tipo: TIPO.FORMULA, esperado: X.b08_residual[k], tol, requer: "arsenal", obter: () => b8({ residual: 50 })[k] });
  add({ id: "C-B08-E-1", ferramenta: "B08", indicador: "Ocupação de equilíbrio sem reserva", decisao: "v0", tipo: TIPO.FORMULA, esperado: X.b08_equilibrio_sem_reserva, tol: TOL.pct, requer: "arsenal", obter: () => D.arsenal.rodar("B08", U.b08Z(), {}).occBE });
  add({ id: "C-B08-E-2", ferramenta: "B08", indicador: "Ocupação de equilíbrio com reserva de 4%, pela regra aprovada (reserva fora das deduções não muda o equilíbrio)", decisao: "D2-C (O3)", tipo: TIPO.DIVERGENCIA, esperado: X.b08_equilibrio_com_reserva_regra_aprovada, tol: TOL.pct, requer: "arsenal",
    nota: "O B08 trata a reserva como dedução e eleva o equilíbrio.", obter: () => D.arsenal.rodar("B08", U.b08Z({ reserva: 4 }), {}).occBE });
  add({ id: "C-B08-E-3", ferramenta: "B08", indicador: "Ocupação de equilíbrio com reserva de 4% como dedução (conferência da conta atual)", decisao: "v0", tipo: TIPO.FORMULA, esperado: X.b08_equilibrio_com_reserva_como_deducao, tol: TOL.pct, requer: "arsenal", obter: () => D.arsenal.rodar("B08", U.b08Z({ reserva: 4 }), {}).occBE });
  // ---------- A09 ----------
  const a9v = { unidades: 2, inv: [{ name: "Unidades", value: 600000 }], infra: [{ name: "Infraestrutura", value: 80000 }], inv_cont: 10, rc_diaria: 550, rc_ocup: 45, rc_noites: 30, rc_meses: 12, rc_extras: 1000, co_fixos: [{ name: "Fixos", value: 8000 }], co_estadia: 150, co_estmedia: 2.5, co_comissao: 12, co_imposto: 6, co_gestao: 10, ce_var_ocup: 0, ce_var_diaria: 0, ind_ref: 10, ind_prazo: 8 };
  const a9 = () => D.arsenal.rodar("A09", a9v, {});
  add({ id: "C-A09-P-1", ferramenta: "A09", indicador: "Investimento total com contingência de 10%", decisao: "v0", tipo: TIPO.FORMULA, esperado: X.a09_payback.invTotal, tol: TOL.reais, requer: "arsenal", obter: () => a9().invTotal });
  for (const [k, ind, tol] of [["recBruta", "Receita bruta com extras de R$ 1.000/mês", TOL.reais], ["ded", "Deduções (comissão 12% + imposto 6% + gestão 10%)", TOL.reais], ["resultado", "Resultado do ano", TOL.reais], ["roi", "Retorno anual (valor)", TOL.pct], ["payback", "Payback simplificado (34,8 anos, sem limite)", TOL.anos]])
    add({ id: `C-A09-P-${k}`, ferramenta: "A09", indicador: ind, decisao: "v0", tipo: TIPO.FORMULA, esperado: X.a09_payback[k], tol, requer: "arsenal", obter: () => a9().cen[1][k] });
  add({ id: "C-A09-G-1", ferramenta: "A09", indicador: "Resultado operacional antes da taxa de gestão (dicionário: gestão é custo do modelo)", decisao: "O2 (a classificar)", tipo: TIPO.LIMITACAO, esperado: X.a09_payback.resultadoAntesGestao, tol: TOL.reais, requer: "arsenal",
    nota: "O A09 desconta a gestão nas deduções; o 'resultado' equivale a um EBITDA.", obter: () => a9().cen[1].resultado });
  add({ id: "C-A09-D-1", ferramenta: "A09", indicador: "Receita com o máximo do campo (31 noites × 12 = 372 dias) igual à de 365 dias", decisao: "D5 (pendente)", tipo: TIPO.LIMITACAO, esperado: X.a09_365_dias.recBruta365, tol: TOL.reais, requer: "arsenal",
    nota: "Com 31 noites/mês o ano tem 372 dias; com 30, 360.", obter: () => D.arsenal.rodar("A09", U.a09Z({ rc_noites: 31 }), {}).cen[1].recBruta });
  add({ id: "C-A09-D-2", ferramenta: "A09", indicador: "Conferência: 31 × 12 noites calculam como definido", decisao: "v0", tipo: TIPO.FORMULA, esperado: X.a09_365_dias.recBruta31x12, tol: TOL.reais, requer: "arsenal", obter: () => D.arsenal.rodar("A09", U.a09Z({ rc_noites: 31 }), {}).cen[1].recBruta });
  // ---------- B06 ----------
  const perfis = JSON.parse(fs.readFileSync(path.join(D.arsenal.APP, "..", "tests", "profiles", "B06.json"), "utf8")).profiles;
  for (const p of perfis) {
    const u = {}; (p.unknown || []).forEach((k) => (u[k] = true));
    const r = () => D.arsenal.rodar("B06", p.values, u), e = X["b06_" + p.name];
    for (const [k, ind] of [["capex", "CAPEX"], ["inter", "Cenário intermediário (contingência fora do giro)"], ["cons", "Cenário conservador (variação × contingência)"], ["giro", "Capital de giro (fixo × meses)"], ["desembMes", "Desembolso mensal"]])
      if (e[k] !== null) add({ id: `C-B06-${p.name}-${k}`, ferramenta: "B06", indicador: `${ind} · perfil ${p.name}`, decisao: "v0", tipo: TIPO.FORMULA, esperado: e[k], tol: TOL.reais, requer: "arsenal", obter: () => r()[k] });
    if (e.porM2 !== null) add({ id: `C-B06-${p.name}-m2`, ferramenta: "B06", indicador: `Custo por m² da unidade · perfil ${p.name}`, decisao: "v0", tipo: TIPO.FORMULA, esperado: e.porM2, tol: TOL.reais, requer: "arsenal", obter: () => r().m2 });
  }
  // ---------- F05 ----------
  const f = () => { const r = D.f05(); if (!r.ok) throw new Error(r.motivo); return r.valores; };
  add({ id: "C-F05-1", ferramenta: "F05", indicador: "Diferença verba − total (exemplo)", decisao: "v0", tipo: TIPO.FORMULA, esperado: X.f05_exemplo.diferenca, tol: TOL.reais, requer: "f05", obter: () => f().diferenca });
  add({ id: "C-F05-2", ferramenta: "F05", indicador: "Custo por m² de área interna (exemplo)", decisao: "v0", tipo: TIPO.FORMULA, esperado: X.f05_exemplo.porM2Interna, tol: TOL.reais, requer: "f05", obter: () => f().porM2Interna });
  add({ id: "C-F05-3", ferramenta: "F05", indicador: "Custo por m² de área total, interna + deck (exemplo)", decisao: "v0", tipo: TIPO.FORMULA, esperado: X.f05_exemplo.porM2Total, tol: TOL.reais, requer: "f05", obter: () => f().porM2Total });
  add({ id: "C-F05-4", ferramenta: "F05", indicador: "Versão em branco: subtotal zero e leitura de espera", decisao: "v0", tipo: TIPO.FORMULA, esperado: [0, "Ainda não há itens com cotação"], requer: "f05",
    obter: () => { const r = D.f05(D.f05BRANCO); if (!r.ok) throw new Error(r.motivo); return [r.valores.subtotal || 0, r.valores.leitura]; } });
  // ---------- Folha J2 ----------
  const F = () => D.folha.api, j = (s) => F().calcular(F().normalizar(s || F().EXEMPLO));
  for (const [k, ind, tol] of [["noitesDisponiveis", "Noites disponíveis (4 × 31)", TOL.noites], ["ocupacao", "Ocupação", TOL.pct], ["diariaMediaBruta", "Diária média bruta", TOL.reais], ["margemPorNoite", "Margem por noite", TOL.reais], ["pontoEquilibrioNoites", "Ponto de equilíbrio (noites)", TOL.noites], ["saldoFinal", "Saldo final do caixa", TOL.reais], ["mesesFolego", "Meses de fôlego", 0.001]])
    add({ id: `C-J2-I-${k}`, ferramenta: "Folha J2", indicador: ind, decisao: "v0", tipo: TIPO.FORMULA, esperado: X.j2_indicadores[k], tol, requer: "folha", obter: () => j()[k] });
  const jm = () => j(Object.assign({}, F().EXEMPLO, { aluguel: 800, taxaGestao: 1200, marca: 300 }));
  for (const [k, ind, tol] of [["custosModelo", "Custos do modelo (aluguel 800 + gestão 1.200 + marca 300)", TOL.reais], ["ebitda", "EBITDA com custos do modelo", TOL.reais], ["geracaoCaixa", "Geração de caixa com custos do modelo", TOL.reais], ["mesesFolego", "Meses de fôlego com custos do modelo", 0.001], ["pontoEquilibrioNoites", "Ponto de equilíbrio com custos do modelo", TOL.noites]])
    add({ id: `C-J2-M-${k}`, ferramenta: "Folha J2", indicador: ind, decisao: "v0", tipo: TIPO.FORMULA, esperado: X.j2_modelo[k === "geracaoCaixa" ? "geracao" : k], tol, requer: "folha", obter: () => jm()[k] });
  return c;
};

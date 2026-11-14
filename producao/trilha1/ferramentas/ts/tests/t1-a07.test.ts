// Aula 7 · CAPEX. Números da Marina: auditoria-aula-7-capex.md, seção 3 (itens 1 a 12).
import { test } from "node:test";
import assert from "node:assert/strict";
import { calculadoras } from "../index";
import { calc, det, idsDoJson, perto, saneamento } from "./helpers";

const calcular = calculadoras["1-7"];
const marina = {
  unidades: 3, area_fechada_unidade: 38, area_deck_unidade: 16, area_apoio: 30,
  custo_m2_piso: 3500, custo_m2_teto: 5000, ffe_unidade_piso: 40000, ffe_unidade_teto: 80000,
  infraestrutura: "nao_sei", projetos_consultas: "nao_sei", // cotações pedidas
  fatores_risco: ["remoto", "sistema_inedito"], contingencia_pct: 15, origem_numeros: "faixa", corte_experiencia: "nao",
};

test("1-7 (a) Marina: 192 m², CAPEX parcial de R$ 963.240 a R$ 1.531.800; avança", async () => {
  const res = calcular(marina);
  saneamento(res, await idsDoJson("07"));
  perto(calc(res, "area_total").valor, 192);
  perto(det(res, "area_total", "esquecida_m2"), 78);
  perto(det(res, "area_total", "pct_esquecida"), 40.625, 0.001);
  perto(det(res, "obra", "obra_piso"), 672000); perto(det(res, "obra", "obra_teto"), 960000);
  perto(det(res, "ffe_ose", "ffe_piso"), 120000); perto(det(res, "ffe_ose", "ffe_teto"), 240000);
  perto(det(res, "ffe_ose", "ose_piso"), 12000); perto(det(res, "ffe_ose", "ose_teto"), 36000);
  perto(det(res, "pre_abertura", "pre_piso"), 33600); perto(det(res, "pre_abertura", "pre_teto"), 96000);
  perto(det(res, "contingencia", "base_piso"), 837600); perto(det(res, "contingencia", "base_teto"), 1332000);
  perto(det(res, "contingencia", "cont_piso"), 125640); perto(det(res, "contingencia", "cont_teto"), 199800);
  perto(det(res, "contingencia", "capex_piso"), 963240); perto(det(res, "contingencia", "capex_teto"), 1531800);
  assert.equal(det(res, "contingencia", "parcial"), true);
  // Proporções: piso 69,8 / 12,5 / 1,2 / 3,5 / 13,0; teto 62,7 / 15,7 / 2,4 / 6,3 / 13,0.
  const p = (k: string) => det(res, "sanidade", k);
  perto(p("pct_hard_piso"), 69.8, 0.05); perto(p("pct_ffe_piso"), 12.5, 0.05); perto(p("pct_ose_piso"), 1.2, 0.05); perto(p("pct_pre_piso"), 3.5, 0.05); perto(p("pct_cont_piso"), 13.0, 0.05);
  perto(p("pct_hard_teto"), 62.7, 0.05); perto(p("pct_ffe_teto"), 15.7, 0.05); perto(p("pct_ose_teto"), 2.4, 0.05); perto(p("pct_pre_teto"), 6.3, 0.05); perto(p("pct_cont_teto"), 13.0, 0.05);
  assert.equal(calc(res, "contingencia_faixa").valor, true);
  perto(det(res, "custo_por_unidade", "custo_unidade_piso"), 321080); perto(det(res, "custo_por_unidade", "custo_unidade_teto"), 510600);
  perto(calc(res, "teto_briefing").valor, 270000); perto(det(res, "teto_briefing", "ffe_unidade"), 80000);
  assert.equal(calc(res, "degrau").valor, "estimador, saindo");
  assert.equal(res.veredito_sugerido, "avancar");
});

test("1-7 peso de R$ 100 mil de rede: R$ 33.333 por cabana (item 11)", async () => {
  const res = calcular({ ...marina, infraestrutura: 100000 });
  perto(det(res, "custo_por_unidade", "infra_por_unidade"), 33333.33, 0.01);
  // item 10: 100.000 × 1,05 × 1,15 = 120.750 a mais no CAPEX piso
  perto((det(res, "contingencia", "capex_piso") as number) - 963240, 120750);
  perto((det(res, "contingencia", "capex_teto") as number) - 1531800, 126500);
});

test("1-7 (b) vários Não sei não quebram e caem em testar", async () => {
  const res = calcular({
    unidades: 3, area_fechada_unidade: 38, area_deck_unidade: "nao_sei", area_apoio: "nao_sei",
    custo_m2_piso: "nao_sei", custo_m2_teto: 5000, ffe_unidade_piso: "nao_sei", ffe_unidade_teto: "nao_sei",
    infraestrutura: "nao_sei", projetos_consultas: "nao_sei", fatores_risco: [], contingencia_pct: 15, origem_numeros: "palpite", corte_experiencia: "nao_sei",
  });
  saneamento(res, await idsDoJson("07"));
  assert.equal(det(res, "contingencia", "capex_piso"), null);
  assert.equal(res.veredito_sugerido, "testar");
  saneamento(calcular({ unidades: 0, area_fechada_unidade: 0, contingencia_pct: 0 }), await idsDoJson("07"));
  saneamento(calcular({}), await idsDoJson("07"));
});

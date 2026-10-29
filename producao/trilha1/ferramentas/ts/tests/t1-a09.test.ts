// Aula 9 · Viabilidade. Números da Marina: auditoria-aula-9-viabilidade.md, seção 3 (itens 1 a 14).
import { test } from "node:test";
import assert from "node:assert/strict";
import { calculadoras } from "../index";
import { calc, det, idsDoJson, perto, saneamento } from "./helpers";

const calcular = calculadoras["1-9"];
const marina = {
  capex_piso: 963240, capex_teto: 1531800, unidades: 3, diaria_media: 645, contribuicao_noite: 408.9, fixo_completo_mes: 13000,
  ocup_alta: 64, ocup_media: 40, ocup_vale: 22,
  meses_alta: ["jun", "jul", "ago"], meses_vale: ["fev", "mar", "abr", "out", "nov"],
  mes_abertura: "jun", rampa: "escola", diaria_testada: "so_mercado",
};

test("1-9 (a) Marina: ano 1 de -R$ 60.943,02, giro de R$ 124.500, payback 74 anos, conservador negativo; testa", async () => {
  const res = calcular(marina);
  saneamento(res, await idsDoJson("09"));
  perto(calc(res, "regime").valor, 14020.62);
  perto(det(res, "regime", "noites_regime_ano"), 415.8);
  perto(calc(res, "ano1").valor, -60943.02);
  perto(det(res, "ano1", "noites_ano1"), 232.47);
  perto(det(res, "ano1", "mes_mais_fundo"), -8951.89);
  perto(calc(res, "ano1_vs_regime").valor, 44.09, 0.01); // 44,1%
  perto(det(res, "retorno_simples", "retorno_piso_pct"), 1.46, 0.005); perto(det(res, "retorno_simples", "retorno_teto_pct"), 0.92, 0.005);
  perto(det(res, "giro", "etapa02"), 124461.92); perto(det(res, "giro", "etapa01"), 78000);
  assert.equal(calc(res, "giro").valor, 124500);
  perto(calc(res, "reserva_sazonalidade").valor, 8172.97);
  perto(calc(res, "curva_caixa").valor, 63556.98);
  perto(det(res, "curva_caixa", "folego_meses"), 4.89, 0.01);
  perto(det(res, "colchao", "colchao_piso_pct"), 6.6, 0.01); perto(det(res, "colchao", "colchao_teto_pct"), 4.15, 0.01);
  perto(det(res, "colchao", "falta_para_10_piso"), 32767.02); perto(det(res, "colchao", "falta_para_10_teto"), 89623.02);
  perto(det(res, "payback", "payback_piso_anos"), 74.05, 0.005); perto(det(res, "payback", "payback_teto_anos"), 114.6, 0.005);
  perto(det(res, "cenarios", "conservador"), -37576.83); perto(det(res, "cenarios", "otimista"), 64814.12);
  perto(calc(res, "diaria_conservador_fecha").valor, 798.07);
  perto(calc(res, "ruptura").valor, 35.33, 0.005);
  perto(det(res, "dor", "perda_diaria"), 21991.66); perto(det(res, "dor", "perda_ocupacao"), 17002.06);
  assert.equal(calc(res, "dor").valor, "diária");
  assert.equal(res.veredito_sugerido, "testar");
  // Rampa no piso (item 4): ano 1 de -R$ 79.932,33.
  perto(calc(calcular({ ...marina, rampa: "piso" }), "ano1").valor, -79932.33);
  // Com a diária testada e o conservador ainda negativo, a página ajusta.
  assert.equal(calcular({ ...marina, diaria_testada: "testada" }).veredito_sugerido, "ajustar");
});

test("1-9 (b) vários Não sei não quebram e caem em testar", async () => {
  const res = calcular({
    capex_piso: "nao_sei", capex_teto: null, unidades: 3, diaria_media: 645, contribuicao_noite: 408.9, fixo_completo_mes: 13000,
    ocup_alta: 64, ocup_media: "nao_sei", ocup_vale: 22, meses_alta: [], meses_vale: ["jun"], mes_abertura: null, rampa: "", diaria_testada: "nao_sei",
  });
  saneamento(res, await idsDoJson("09"));
  assert.equal(calc(res, "regime").valor, null);
  assert.equal(res.veredito_sugerido, "testar");
  const semCapex = calcular({ ...marina, capex_piso: "nao_sei", capex_teto: "nao_sei" });
  saneamento(semCapex, await idsDoJson("09"));
  assert.equal(semCapex.veredito_sugerido, "testar");
  const zero = calcular({ ...marina, contribuicao_noite: 0, fixo_completo_mes: 0, unidades: 0 });
  saneamento(zero, await idsDoJson("09"));
  saneamento(calcular({}), await idsDoJson("09"));
});

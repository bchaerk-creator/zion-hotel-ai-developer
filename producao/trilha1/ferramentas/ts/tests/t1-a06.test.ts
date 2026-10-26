// Aula 6 · Masterplan. Números da Marina: auditoria-aula-6-masterplan.md, seção 3 (itens 1, 2 e 4) e seção 10.
import { test } from "node:test";
import assert from "node:assert/strict";
import { calculadoras } from "../index";
import { calc, det, idsDoJson, perto, saneamento } from "./helpers";

const calcular = calculadoras["1-6"];
const marina = {
  zonas_nunca: "Mata ciliar do riacho (lei); a crista (produto)", tres_gestos: ["marcado", "fotografado", "clausula"],
  unidades_fase1: 3, area_fechada_unidade: 38, area_apoio: 30,
  apoio_resolvido: ["rouparia_lavanderia", "deposito", "residuo", "copa_vestiario", "estac_servico", "oficina", "gas_reservatorio"],
  dia_simulado: "sim", caminhos: "nao_cruzam", caminhada_estacas: "sim",
  unidades_projeto_completo: 5, rede_para: 5, gatilho_escrito: ["demanda", "caixa", "maturidade"], condicionantes: 7, consulta_previa: "protocolada",
};

test("1-6 (a) Marina: apoio de 20,8% sobre 144 m², rede para 5; avança", async () => {
  const res = calcular(marina);
  saneamento(res, await idsDoJson("06"));
  perto(calc(res, "pct_apoio").valor, 20.83, 0.01);
  perto(det(res, "pct_apoio", "area_fechada_total_m2"), 144);
  assert.equal(calc(res, "rede_vs_projeto").valor, false);
  assert.equal(calc(res, "esquecidos").valor, 0);
  assert.equal(calc(res, "gatilho").valor, 3);
  assert.equal(res.veredito_sugerido, "avancar");
  // Desenho completo com o apoio de 30 m²: 30 ÷ 220 = 13,6%, abaixo de 15% (auditoria, item 4).
  const completo = calcular({ ...marina, unidades_fase1: 5 });
  perto(calc(completo, "pct_apoio").valor, 13.64, 0.01);
  assert.equal(completo.veredito_sugerido, "ajustar");
  // Com 34 m²: 34 ÷ 224 = 15,2%.
  perto(calc(calcular({ ...marina, unidades_fase1: 5, area_apoio: 34 }), "pct_apoio").valor, 15.18, 0.01);
  // Critério para parar: a consulta prévia tira as cabanas do ponto.
  assert.equal(calcular({ ...marina, consulta_previa: "tira" }).veredito_sugerido, "pausar");
});

test("1-6 (b) vários Não sei não quebram e caem em testar", async () => {
  const res = calcular({
    zonas_nunca: "nao_sei", tres_gestos: [], unidades_fase1: 3, area_fechada_unidade: 0, area_apoio: "nao_sei",
    apoio_resolvido: [], unidades_projeto_completo: "nao_sei", rede_para: "nao_sei", gatilho_escrito: [], condicionantes: "nao_sei", consulta_previa: "nao_sei",
  });
  saneamento(res, await idsDoJson("06"));
  assert.equal(calc(res, "pct_apoio").valor, null);
  assert.equal(res.veredito_sugerido, "testar");
  saneamento(calcular({ unidades_fase1: 0, area_fechada_unidade: 0, area_apoio: 0 }), await idsDoJson("06"));
  saneamento(calcular({}), await idsDoJson("06"));
});

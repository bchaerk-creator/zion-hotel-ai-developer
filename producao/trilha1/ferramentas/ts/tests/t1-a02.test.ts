// Aula 2 · Território. Números da Marina: auditoria-aula-2-escada.md (15.000 m², 30%, 5 unidades, 27%) e
// ebook-02-territorio.txt (subtrações, R$ 12 / R$ 40 / R$ 120 mil, 2,4 vezes); investimento total de
// R$ 2.220.000 conferido em auditoria-aula-3-mercado.md (ponto de partida).
import { test } from "node:test";
import assert from "node:assert/strict";
import { calculadoras } from "../index";
import { calc, det, idsDoJson, perto, saneamento } from "./helpers";

const calcular = calculadoras["1-2"];
const marina = {
  area_matricula: 50000, sub_preservacao: 12000, sub_reserva_legal: 10000, sub_encosta: 8000, sub_recuos: 1500, sub_servico: 3500,
  preco_terreno: 600000, investimento_total: 2220000,
  limite_fisico: 12, limite_infra: 10, limite_experiencia: 7, limite_mercado: 5,
  documentos: ["matricula", "car"], caminho_leitura: "investigar",
};

test("1-2 (a) Marina: área usável, três preços, capacidade, ilusão e peso batem com a auditoria", async () => {
  const res = calcular(marina);
  saneamento(res, await idsDoJson("02"));
  perto(calc(res, "area_usavel").valor, 15000);
  perto(calc(res, "pct_usavel").valor, 30);
  perto(det(res, "tres_precos", "preco_m2_total"), 12);
  perto(det(res, "tres_precos", "preco_m2_usavel"), 40);
  perto(det(res, "tres_precos", "preco_por_unidade"), 120000);
  assert.equal(calc(res, "capacidade").valor, 5);
  assert.deepEqual(det(res, "capacidade", "limite_que_manda"), ["limite_mercado"]);
  perto(calc(res, "ilusao_preco").valor, 2.4);
  perto(calc(res, "peso_terreno").valor, 27.03, 0.01);
  assert.equal(calc(res, "peso_terreno").alerta, "critico");
  // DIVERGÊNCIA D1: a auditoria dá "testa"; a fórmula do JSON checa "peso > 20% → ajustar" antes de "investigar → testar".
  assert.equal(res.veredito_sugerido, "ajustar");
});

test("1-2 (b) vários Não sei não quebram e caem em testar", async () => {
  const res = calcular({
    area_matricula: 50000, sub_preservacao: "nao_sei", sub_reserva_legal: "nao_sei", sub_encosta: 8000, sub_recuos: "", sub_servico: null,
    preco_terreno: 600000, investimento_total: "nao_sei",
    limite_fisico: 12, limite_infra: "nao_sei", limite_experiencia: "nao_sei", limite_mercado: "nao_sei",
    documentos: [], caminho_leitura: "nao_sei",
  });
  saneamento(res, await idsDoJson("02"));
  perto(calc(res, "area_usavel").valor, 42000);
  assert.equal(det(res, "area_usavel", "provisoria"), true);
  assert.equal(calc(res, "capacidade").valor, 12);
  assert.equal(calc(res, "peso_terreno").valor, null);
  assert.equal(res.veredito_sugerido, "testar");
  const zero = calcular({ area_matricula: 0, preco_terreno: 0, investimento_total: 0, limite_fisico: 0 });
  saneamento(zero, await idsDoJson("02"));
  saneamento(calcular({}), await idsDoJson("02"));
});

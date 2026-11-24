// Aula 12 · Dossiê final. Números da Marina: auditoria-aula-12-dossie.md, seção 3 (contagem conferida duas vezes).
import { test } from "node:test";
import assert from "node:assert/strict";
import { calculadoras } from "../index";
import { calc, det, idsDoJson, saneamento } from "./helpers";

const calcular = calculadoras["1-12"];
const marina = {
  veredito_p1: "testar", veredito_p2: "ajustar", veredito_p3: "avancar", veredito_p4: "avancar", veredito_p5: "avancar",
  veredito_p6: "avancar", veredito_p7: "testar", veredito_p8: "testar", veredito_p9: "testar", veredito_p10: "testar",
  paginas_completas: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
};

test("1-12 (a) Marina: avança 4, ajusta 1, testa 5; o projeto testa, ritmo das páginas 1 e 7 a 10", async () => {
  const res = calcular(marina);
  saneamento(res, await idsDoJson("12"));
  assert.equal(det(res, "contagem", "avancar"), 4);
  assert.equal(det(res, "contagem", "ajustar"), 1);
  assert.equal(det(res, "contagem", "testar"), 5);
  assert.equal(calc(res, "veredito_projeto").valor, "testar");
  assert.equal(calc(res, "paginas_mais_fracas").valor, "1, 7, 8, 9, 10");
  assert.equal(calc(res, "completas").valor, 10);
  assert.deepEqual(det(res, "completas", "faltam"), ["0"]); // a ficha da Marina está em branco no capital próprio
  assert.equal(det(res, "por_etapa", "etapa1"), "testar");
  assert.equal(det(res, "por_etapa", "etapa2"), "avancar");
  assert.equal(det(res, "por_etapa", "etapa3"), "testar");
  assert.equal(det(res, "por_etapa", "etapa4"), "testar");
  assert.equal(res.veredito_sugerido, "testar");
  assert.equal(calcular({ ...marina, veredito_p5: "pausar" }).veredito_sugerido, "pausar");
});

test("1-12 (b) páginas não feitas e vazias não quebram e contam como testar", async () => {
  const res = calcular({ veredito_p1: "avancar", veredito_p2: "nao_fiz", veredito_p3: null, veredito_p4: "nao_sei", paginas_completas: [], depende_repetido: "nao_sei", maior_lacuna: "nao_sei", criterio_projeto: "nao_sei" });
  saneamento(res, await idsDoJson("12"));
  assert.equal(det(res, "contagem", "nao_fiz"), 9);
  assert.equal(res.veredito_sugerido, "testar");
  const todasAvancam = calcular(Object.fromEntries(Array.from({ length: 10 }, (_, i) => [`veredito_p${i + 1}`, "avancar"])));
  assert.equal(todasAvancam.veredito_sugerido, "avancar");
  assert.match(todasAvancam.motivo_veredito, /não estão completas/);
  saneamento(calcular({}), await idsDoJson("12"));
});

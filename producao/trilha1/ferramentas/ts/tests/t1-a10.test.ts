// Aula 10 · Capital e captação. Números da Marina: auditoria-aula-10-capital.md, seção 3 (itens 3, 4, 5, 6 e 7).
import { test } from "node:test";
import assert from "node:assert/strict";
import { calculadoras } from "../index";
import { calc, det, idsDoJson, perto, saneamento } from "./helpers";

const calcular = calculadoras["1-10"];
const marina = {
  p1_construir: "sim", p2_diaria: "nao", p3_retorno: "sim",
  nota_capex: "nao_sei", nota_receita: "nao_sei", nota_ebitda: "nao_sei", nota_tir: "nao_sei", nota_viabilidade: "nao_sei",
  conservador_fecha: "nao", capex: 963240, giro: 124500, menor_saldo: 63556.98,
  capital_proprio: 0, // hipótese da auditoria (item 6): o aporte cobre todos os usos antes do custo
  contribuicao_documentada: 600000, // o terreno, se o laudo confirmar
};

test("1-10 (a) Marina no piso: reforço de R$ 32.767,02, Régua de R$ 1.120.507,02, participação de 65,13%; testa", async () => {
  const res = calcular(marina);
  saneamento(res, await idsDoJson("10"));
  assert.equal(calc(res, "tres_perguntas").valor, true);
  assert.equal(calc(res, "score").valor, "em branco");
  assert.equal(calc(res, "regra_prevalece").valor, "não captar ainda");
  perto(calc(res, "colchao").valor, 32767.02);
  perto(det(res, "colchao", "giro_ajustado"), 157267.02);
  perto(det(res, "regua", "necessidade_antes"), 1120507.02);
  perto(calc(res, "participacao").valor, 65.13, 0.005);
  // Custo da captação: a auditoria cita 2% a 5% "do captado" como 22.410,14 a 56.025,35 (percentual sobre a necessidade).
  // A fórmula do JSON faz externo ÷ (1 - taxa): 1.143.374,51 a 1.179.481,07 (custo de 22.867,49 a 58.974,05). Ver README D5.
  perto(det(res, "regua", "com_custo_2"), 1143374.51); perto(det(res, "regua", "com_custo_5"), 1179481.07);
  assert.equal(res.veredito_sugerido, "testar");
});

test("1-10 Marina no teto: reforço de R$ 89.623,02, Régua de R$ 1.745.923,02, participação de 74,42%", async () => {
  const res = calcular({ ...marina, capex: 1531800 });
  perto(calc(res, "colchao").valor, 89623.02);
  perto(det(res, "colchao", "giro_ajustado"), 214123.02);
  perto(det(res, "regua", "necessidade_antes"), 1745923.02);
  perto(calc(res, "participacao").valor, 74.42, 0.005);
});

test("1-10 score e faixas", async () => {
  const notas = { nota_capex: 80, nota_receita: 70, nota_ebitda: 60, nota_tir: 75, nota_viabilidade: 90 };
  const res = calcular({ ...marina, ...notas, p2_diaria: "sim", conservador_fecha: "sim" });
  perto(calc(res, "score").valor, 75);
  assert.equal(res.veredito_sugerido, "avancar");
  assert.equal(calcular({ ...marina, ...notas, nota_capex: 0, nota_receita: 0, nota_ebitda: 0 }).veredito_sugerido, "pausar");
  assert.equal(calcular({ ...marina, p2_diaria: "sim" }).veredito_sugerido, "pausar"); // diária testada e conservador não fecha
});

test("1-10 (b) vários Não sei não quebram e caem em testar", async () => {
  const res = calcular({ ...marina, p1_construir: "nao_sei", p2_diaria: "nao_sei", p3_retorno: null, conservador_fecha: "nao_sei", capital_proprio: "nao_sei", contribuicao_documentada: "nao_sei", menor_saldo: "nao_sei" });
  saneamento(res, await idsDoJson("10"));
  assert.equal(calc(res, "participacao").valor, null);
  assert.equal(res.veredito_sugerido, "testar");
  saneamento(calcular({ capex: 0, giro: 0, menor_saldo: 0, capital_proprio: 0, contribuicao_documentada: 0 }), await idsDoJson("10"));
  saneamento(calcular({}), await idsDoJson("10"));
});

// Aula 1 · Marco Zero. Sem auditoria com números: a Marina refaz a ficha na Aula 12 (ebook-12, "A ficha de entrada da Marina, refeita hoje").
import { test } from "node:test";
import assert from "node:assert/strict";
import { calculadoras } from "../index";
import { calc, idsDoJson, saneamento } from "./helpers";

const calcular = calculadoras["1-1"];

test("1-1 (a) Marina, ficha refeita: 5 de 5, vitrine A, ocupação 38,5% com movimento de fim de semana", async () => {
  const res = calcular({
    situacao_letra: "nao_sei", // "Em branco: o capital próprio dela nunca foi escrito"
    perguntas_investidor: ["produto", "custo", "retorno", "lucro", "tempo"],
    vitrine: "A",
    etapa_ordem: "4",
    nota_21_pontos: "nao_sei",
    custo_espera: "nao_sei",
    perfil_demanda: "fds",
    ocupacao_imaginada: 38.5,
  });
  saneamento(res, await idsDoJson("01"));
  assert.equal(calc(res, "respostas_investidor").valor, 5);
  assert.equal(calc(res, "linha_ficha").valor, "não sei, 5 de 5, A, etapa 4");
  assert.equal(calc(res, "comeco_recomendado").valor, null);
  assert.equal(calc(res, "regua_ocupacao").valor, false);
  assert.equal(calc(res, "regua_ocupacao").alerta, "ok");
  assert.equal(res.veredito_sugerido, "nao_se_aplica");
});

test("1-1 exemplo do slide ficha: \"B, 1 de 5, A, etapa 1\", nota 8 e 70% só de fim de semana", async () => {
  const res = calcular({ situacao_letra: "B", perguntas_investidor: ["custo"], vitrine: "A", etapa_ordem: "1", nota_21_pontos: 8, perfil_demanda: "fds", ocupacao_imaginada: 70 });
  saneamento(res, await idsDoJson("01"));
  assert.equal(calc(res, "linha_ficha").valor, "B, 1 de 5, A, etapa 1");
  assert.equal(calc(res, "comeco_recomendado").valor, "Começar pela etapa 1 da Ordem, Ler o terreno");
  assert.equal(calc(res, "regua_ocupacao").valor, true);
  assert.equal(calc(res, "regua_ocupacao").alerta, "critico");
});

test("1-1 (b) tudo em Não sei ou vazio não quebra", async () => {
  const res = calcular({
    situacao_letra: "nao_sei", obj_hospedagem: "nao_sei", problema_mercado: "", perguntas_investidor: [],
    vitrine: "nao_sei", etapa_ordem: null, nota_21_pontos: "nao_sei", custo_espera: "nao_sei",
    perfil_demanda: "nao_sei", ocupacao_imaginada: "nao_sei", primeira_decisao: "nao_sei",
  });
  saneamento(res, await idsDoJson("01"));
  assert.equal(calc(res, "respostas_investidor").valor, 0);
  assert.equal(calc(res, "regua_ocupacao").valor, null);
  const vazio = calcular({});
  saneamento(vazio, await idsDoJson("01"));
});

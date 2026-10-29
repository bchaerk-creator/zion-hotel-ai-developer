// Aula 5 · Modelo de negócio. A auditoria (seção 3) não faz conta: só o veredito "avança" da Marina, que opera
// a fase um de 3 cabanas com uma pessoa local. As respostas abaixo são as que o ebook-05 descreve.
import { test } from "node:test";
import assert from "node:assert/strict";
import { calculadoras } from "../index";
import { calc, idsDoJson, saneamento } from "./helpers";

const calcular = calculadoras["1-5"];
const marina = {
  quer_operar: "sim", horas_hospede: 20, horas_anotadas: "sim_cobrem", unidades_fase1: 3, quem_opera: "eu_com_local",
  quem_faz_momento: "A pessoa local, antes das sete", fica_comigo: ["preco", "excecao", "produto"], rotina_escrita: "repetida",
  naturezas_receita: ["hospedagem", "cessao"], valorizacao_na_conta: "nao", saida_pretendida: "operar", receita_formal: "toda",
  nao_faco: "Eventos com som", requisitos_licenciar: [],
};

test("1-5 (a) Marina: sem alertas, licenciar não é opção hoje; avança", async () => {
  const res = calcular(marina);
  saneamento(res, await idsDoJson("05"));
  assert.equal(calc(res, "alerta_escala").valor, false);
  assert.equal(calc(res, "tres_decisoes").valor, "nenhuma");
  assert.equal(calc(res, "adequacao").valor, false);
  assert.equal(calc(res, "valorizacao").valor, false);
  assert.equal(calc(res, "portas_saida").valor, false);
  assert.equal(calc(res, "licenciar").valor, 0);
  assert.equal(res.veredito_sugerido, "avancar");
  // A gestão volta à mesa com cinco: operando sozinha 5 unidades, o alerta acende.
  const cinco = calcular({ ...marina, unidades_fase1: 5 });
  assert.equal(calc(cinco, "alerta_escala").valor, true);
  assert.equal(cinco.veredito_sugerido, "ajustar");
  // Critério para parar: horas que não cobrem o horário de hóspede.
  assert.equal(calcular({ ...marina, horas_anotadas: "sim_nao_cobrem" }).veredito_sugerido, "pausar");
});

test("1-5 (b) vários Não sei não quebram e caem em testar", async () => {
  const res = calcular({
    quer_operar: "nao_sei", horas_hospede: "nao_sei", horas_anotadas: "nao_anotei", unidades_fase1: null, quem_opera: "nao_sei",
    fica_comigo: [], rotina_escrita: null, valorizacao_na_conta: "nao_sei", receita_formal: "nao_sei", requisitos_licenciar: [],
  });
  saneamento(res, await idsDoJson("05"));
  assert.equal(calc(res, "alerta_escala").valor, null);
  assert.equal(res.veredito_sugerido, "testar");
  saneamento(calcular({}), await idsDoJson("05"));
});

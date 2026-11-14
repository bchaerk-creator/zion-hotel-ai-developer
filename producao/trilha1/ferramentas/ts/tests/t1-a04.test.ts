// Aula 4 · Produto. Números da Marina: auditoria-aula-4-produto.md, seção 3 (itens 5 e 6); frase, provas e veredito do ebook-04.
import { test } from "node:test";
import assert from "node:assert/strict";
import { calculadoras } from "../index";
import { calc, idsDoJson, perto, saneamento } from "./helpers";

const calcular = calculadoras["1-4"];
const marina = {
  publico_principal: "O casal que vem descansar",
  momento_assinatura: "O vale às sete, da cama, com café na varanda, preparado pela pessoa local",
  requisitos_momento: ["so_aqui", "sem_voce", "uma_frase", "foto"],
  frase_produto: "Acordar com o vale entrando pela janela, para casais que precisam de silêncio, num lugar onde a cama olha o nascente e nada mais se move.",
  provas: "A cama virada para o nascente, na meia encosta.\nNenhuma janela enxerga outra unidade.\nO vale às sete, da cama, com o café na varanda.",
  teste_vizinho: "falsa_para_os_tres", teste_cinco_segundos: "mesma",
  tipologia: "cabana_madeira", area_interna: 38, unidades_abertura: 3,
  diaria_regiao: 645.45, diaria_hipotese: 716.36,
};

test("1-4 (a) Marina: frase limpa, 3 provas, 38 m², mix de 3 e hipótese 11% acima; avança", async () => {
  const res = calcular(marina);
  saneamento(res, await idsDoJson("04"));
  assert.equal(calc(res, "lista_negra").valor, "");
  assert.equal(calc(res, "momento_ok").valor, true);
  assert.equal(calc(res, "conta_provas").valor, 3);
  assert.equal(calc(res, "faixa_area").valor, "cabana de casal com sala (32 a 45 m²)");
  assert.equal(calc(res, "mix").valor, "tudo igual; o segundo público entra por produto e preço");
  perto(calc(res, "hipotese_vs_regiao").valor, 10.99, 0.01); // 716,36 ÷ 645,45 = 1,110
  assert.equal(res.veredito_sugerido, "avancar"); // "avança, com o preço em teste"
});

test("1-4 lista negra pega plural, feminino e acento; mix acima de 4", async () => {
  const res = calcular({ ...marina, frase_produto: "O refúgio mais EXCLUSIVO da serra, experiências únicas e inesquecíveis", unidades_abertura: 6 });
  assert.equal(calc(res, "lista_negra").valor, "único, exclusivo, inesquecível");
  assert.equal(calc(res, "mix").valor, "4 para o público principal e 2 para o público da semana");
  assert.equal(res.veredito_sugerido, "ajustar");
});

test("1-4 (b) vários Não sei não quebram e caem em testar", async () => {
  const res = calcular({
    publico_principal: "nao_sei", frase_produto: "nao_sei", provas: "nao_sei", requisitos_momento: [],
    teste_vizinho: "nao_fiz", teste_cinco_segundos: null, tipologia: "nao_sei",
    area_interna: "nao_sei", unidades_abertura: "nao_sei", diaria_regiao: 0, diaria_hipotese: "nao_sei",
  });
  saneamento(res, await idsDoJson("04"));
  assert.equal(calc(res, "hipotese_vs_regiao").valor, null);
  assert.equal(res.veredito_sugerido, "testar");
  saneamento(calcular({}), await idsDoJson("04"));
});

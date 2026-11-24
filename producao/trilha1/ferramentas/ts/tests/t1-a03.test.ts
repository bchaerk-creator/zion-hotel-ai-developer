// Aula 3 · Mercado. Números da Marina: auditoria-aula-3-mercado.md, "Exemplo resolvido ilustrativo", passos 1 a 9.
import { test } from "node:test";
import assert from "node:assert/strict";
import { calculadoras } from "../index";
import { calc, det, idsDoJson, perto, saneamento } from "./helpers";

const calcular = calculadoras["1-3"];
const marina = {
  unidades_comparaveis: 96, ocup_fds: 78, ocup_semana: 26, diaria_fds: 700, diaria_semana: 580,
  amplitude: 3.03, // 1.150 ÷ 380 = 3,03 (a auditoria arredonda para 3,0)
  meses_alta: 3, ocup_alta: 64, meses_fraco: 5, ocup_fraco: 22, ocup_media: 40,
  crescimento_ate_abrir: (1.07 ** 3 - 1) * 100, // 7% ao ano por 3 anos = 22,5%
  unidades_em_obra: 18, unidades_pretendidas: 5,
};

test("1-3 (a) Marina: semana, ano, receita por unidade e absorção batem com a auditoria", async () => {
  const res = calcular(marina);
  saneamento(res, await idsDoJson("03"));
  perto(det(res, "conta_semana", "noites_semana"), 2.86);
  perto(det(res, "conta_semana", "receita_semana"), 1846);
  perto(det(res, "conta_semana", "ocup_janela_pct"), 40.857, 0.001);
  perto(calc(res, "conta_semana").valor, 645.45);
  perto(det(res, "conta_semana", "por_noite_disponivel"), 263.71);
  perto(calc(res, "fds_vs_semana").valor, 3.0);
  assert.equal(calc(res, "regua_amplitude").alerta, "ok");
  perto(calc(res, "ocup_ano").valor, 38.5);
  perto(calc(res, "erro_mes_cheio").valor, 66.23, 0.01); // "66% a mais"
  perto(calc(res, "receita_bruta_unidade").valor, 90703, 1); // R$ 90.703
  perto(calc(res, "mes_fraco_unidade").valor, 4260, 1); // "cerca de R$ 4.260" (Aula 8)
  // Absorção com a fórmula corrigida (sobra = mais - menos). A auditoria usa 38% e chega a 499 noites e 3 cabanas;
  // com os 38,5% do ano a sobra é 506,5 noites e 3,6 cabanas: cabem as mesmas 3.
  perto(det(res, "absorcao", "sobra"), 506.5, 0.5);
  assert.equal(calc(res, "absorcao").valor, 3);
  assert.equal(calc(res, "checa_regua").valor, false);
  // A Aula 3 diz "seguir com condições"; a Aula 12 registra "Ajusta (abre com 3)", que é o que a regra do JSON dá.
  assert.equal(res.veredito_sugerido, "ajustar");
});

test("1-3 absorção exatamente como a auditoria (38%)", async () => {
  const res = calcular({ ...marina, meses_alta: 0, meses_fraco: 0, ocup_media: 38 });
  perto(det(res, "absorcao", "sobra"), 499, 1);
  perto(det(res, "absorcao", "noites_por_unidade"), 138.7);
  assert.equal(calc(res, "absorcao").valor, 3);
});

test("1-3 (b) vários Não sei não quebram e caem em testar", async () => {
  const res = calcular({
    unidades_comparaveis: 96, ocup_fds: "nao_sei", ocup_semana: 26, diaria_fds: 700, diaria_semana: "nao_sei",
    amplitude: "nao_sei", meses_alta: 3, ocup_alta: 64, meses_fraco: 5, ocup_fraco: "nao_sei", ocup_media: 40,
    crescimento_ate_abrir: "nao_sei", unidades_em_obra: "nao_sei", unidades_pretendidas: 5,
  });
  saneamento(res, await idsDoJson("03"));
  assert.equal(calc(res, "conta_semana").valor, null);
  assert.equal(calc(res, "ocup_ano").valor, null);
  assert.equal(res.veredito_sugerido, "testar");
  const s = calcular({ ...marina, crescimento_ate_abrir: "nao_sei", unidades_em_obra: "nao_sei" });
  assert.equal(det(s, "absorcao", "sem_serie"), true);
  assert.equal(s.veredito_sugerido, "testar");
  saneamento(calcular({ ocup_semana: 0, ocup_fds: 0, diaria_fds: 0, diaria_semana: 0, meses_alta: 12, meses_fraco: 0, ocup_alta: 0 }), await idsDoJson("03"));
  saneamento(calcular({}), await idsDoJson("03"));
});

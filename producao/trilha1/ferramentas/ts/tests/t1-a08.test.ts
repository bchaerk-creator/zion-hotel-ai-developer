// Aula 8 · Receitas e custos. Números da Marina: auditoria-aula-8-receitas.md, seção 3 (itens 1 a 15).
import { test } from "node:test";
import assert from "node:assert/strict";
import { calculadoras } from "../index";
import { calc, det, idsDoJson, perto, saneamento } from "./helpers";

const calcular = calculadoras["1-8"];
const base = {
  unidades: 3, diaria_media: 645, meses_alta: 3, ocup_alta: 64, meses_vale: 5, ocup_vale: 22, ocup_media: 40,
  deducoes_pct: 17, variavel_noite: 60, limpeza_estadia: 120, estadia_media: 2, fixos_operacionais_mes: 10500, retirada_mes: 1400,
};
// A auditoria arredonda a reserva para R$ 1.100 por mês (4,9% da bruta). Para reproduzir as contas, o teste usa o
// percentual exato que dá R$ 1.100: 13.200 ÷ 268.191. Com 5% cheio, ver o teste seguinte.
const marina = { ...base, reserva_pct: (13200 / 268191) * 100 };

test("1-8 (a) Marina: cascata de R$ 14.020,62 (5,23%), folga 3,17 e diária de R$ 687,75; testa", async () => {
  const res = calcular(marina);
  saneamento(res, await idsDoJson("08"));
  perto(calc(res, "noites").valor, 415.8);
  perto(det(res, "noites", "ocup_ano_pct"), 38.5);
  perto(det(res, "receita", "receita_bruta"), 268191); perto(det(res, "receita", "receita_real"), 222598.53);
  perto(calc(res, "variavel_por_noite").valor, 126.45);
  perto(calc(res, "contribuicao_noite").valor, 408.9);
  perto(calc(res, "fixo_completo").valor, 13000);
  perto(det(res, "cascata", "margem_contrib"), 170020.62);
  perto(det(res, "cascata", "resultado_operacional"), 27220.62);
  perto(det(res, "cascata", "depois_reserva"), 14020.62);
  perto(calc(res, "cascata").valor, 5.23, 0.005);
  perto(det(res, "mes_a_mes", "resultado_mes_alta"), 10552.64); perto(det(res, "mes_a_mes", "resultado_mes_media"), 1720.4); perto(det(res, "mes_a_mes", "resultado_mes_vale"), -4903.78);
  perto(calc(res, "mes_a_mes").valor, -24518.9);
  perto(det(res, "equilibrio", "noites_equilibrio_ano"), 381.51, 0.01);
  perto(det(res, "equilibrio", "ocup_equilibrio_pct"), 35.33, 0.01);
  perto(calc(res, "equilibrio").valor, 3.17, 0.01);
  perto(det(res, "custo_por_diaria", "custo_alta"), 352.14); perto(det(res, "custo_por_diaria", "custo_media"), 487.56);
  perto(det(res, "custo_por_diaria", "custo_vale"), 783.02); perto(det(res, "custo_por_diaria", "custo_ano"), 501.63);
  perto(calc(res, "diaria_criterio").valor, 687.75);
  perto(calc(res, "taxa_que_empata").valor, 6.26, 0.005);
  assert.equal(res.veredito_sugerido, "testar");
});

test("1-8 cenário R$ 716 (item 13): 12,84% de margem, ajusta; e reserva de 5% cheio", async () => {
  const r716 = calcular({ ...marina, diaria_media: 716 });
  // Com R$ 716 a reserva segue em R$ 1.100 na auditoria; aqui ela acompanha a receita (5% x receita nova).
  const r716fixa = calcular({ ...marina, diaria_media: 716, reserva_pct: (13200 / (415.8 * 716)) * 100 });
  perto(det(r716fixa, "cascata", "depois_reserva"), 38228.5, 0.01);
  perto(calc(r716fixa, "cascata").valor, 12.84, 0.005);
  perto(calc(r716fixa, "equilibrio").valor, 7.58, 0.01);
  assert.equal(r716fixa.veredito_sugerido, "ajustar");
  assert.ok(typeof calc(r716, "cascata").valor === "number");
  const cinco = calcular({ ...base, reserva_pct: 5 });
  perto(det(cinco, "fixo_completo", "reserva_mes"), 1117.46);
  perto(det(cinco, "cascata", "depois_reserva"), 13811.07, 0.01);
  assert.equal(cinco.veredito_sugerido, "testar");
});

test("1-8 (b) vários Não sei não quebram e caem em testar", async () => {
  const res = calcular({ ...base, variavel_noite: "nao_sei", limpeza_estadia: "nao_sei", estadia_media: 0, fixos_operacionais_mes: "nao_sei", retirada_mes: "nao_sei", reserva_pct: 4 });
  saneamento(res, await idsDoJson("08"));
  assert.equal(calc(res, "cascata").valor, null);
  assert.equal(res.veredito_sugerido, "testar");
  // Contribuição negativa: não existe equilíbrio e a página pausa.
  const neg = calcular({ ...marina, diaria_media: 100 });
  saneamento(neg, await idsDoJson("08"));
  assert.equal(neg.veredito_sugerido, "pausar");
  saneamento(calcular({}), await idsDoJson("08"));
});

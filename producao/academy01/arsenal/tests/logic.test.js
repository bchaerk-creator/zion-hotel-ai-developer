// Testes do motor do Bloco 01 (Raio-X). Rodar: node producao/academy01/arsenal/tests/logic.test.js
const assert = require("assert");
const L = require("../src/logic.js");
let ok = 0, falhas = 0;
function t(nome, fn) { try { fn(); ok++; console.log("  ok  " + nome); } catch (e) { falhas++; console.log("  FALHOU  " + nome + "\n        " + e.message); } }
const base = (x) => Object.assign({ periodo: "30", disponiveis: "30", ocupadas: "9", diaria: "320", visualizacoes: "340", consultas: "6", reservas: "3", mesmoPeriodo: true, reservaInstantanea: "nao" }, x);
const ids = (fb) => fb.map((b) => b.id);
const texto = (fb) => fb.map((b) => [b.titulo, b.resultado, b.significado, b.atencao, b.fazer, b.verificar].join(" ")).join(" ");
const PROIBIDAS = /\b(bom|boa|ruim|baixa demais|alta demais|abaixo da média|acima da média|média do mercado|garant)/i;

console.log("Fórmulas");
t("ocupação = ocupadas ÷ disponíveis × 100", () => { const r = L.calcular(base()); assert.strictEqual(r.ocupacao, 30); assert.strictEqual(r.noitesVazias, 21); });
t("receita = noites ocupadas × diária efetiva", () => assert.strictEqual(L.calcular(base()).receita, 2880));
t("consultas por visualização = consultas ÷ visualizações × 100", () => assert.ok(Math.abs(L.calcular(base()).taxaConsulta - 1.7647) < 1e-3));
t("conversão = reservas ÷ consultas × 100", () => assert.strictEqual(L.calcular(base()).taxaReserva, 50));
t("estadia média usa noites ÷ reservas (não mistura as duas)", () => assert.strictEqual(L.calcular(base()).estadiaMedia, 3));
t("diária com vírgula e milhar", () => { assert.strictEqual(L.lerNumero("1.250,50").valor, 1250.5); assert.strictEqual(L.lerNumero("R$ 320").valor, 320); });

console.log("Cenário A · baixa procura");
const A = base({ disponiveis: "30", ocupadas: "4", diaria: "280", visualizacoes: "95", consultas: "2", reservas: "1", meta: "15" });
t("calcula a conta da meta com as taxas atuais", () => { const r = L.calcular(A); assert.ok(r.necessario); assert.strictEqual(r.necessario.noites, 11); assert.ok(r.necessario.visualizacoes > 0); });
t("orienta visibilidade, disponibilidade e apresentação", () => { const s = texto(L.feedback(L.calcular(A))); assert.match(s, /visibilidade/i); assert.match(s, /disponibilidade/i); assert.match(s, /apresenta/i); });
t("não afirma causa comprovada", () => { const s = texto(L.feedback(L.calcular(A))); assert.match(s, /hipótese/i); assert.doesNotMatch(s, PROIBIDAS); });
t("sem meta e sem histórico: só linha de base, sem julgar", () => { const s = texto(L.feedback(L.calcular(Object.assign({}, A, { meta: "" })))); assert.match(s, /linha de base/i); assert.doesNotMatch(s, PROIBIDAS); });

console.log("Cenário B · interesse sem reservas");
const B = base({ disponiveis: "30", ocupadas: "6", diaria: "450", visualizacoes: "1800", consultas: "24", reservas: "1",
  anterior: { ativo: true, visualizacoes: "1600", consultas: "20", reservas: "6", ocupadas: "14", disponiveis: "30" } });
t("com histórico, aponta a queda na conversão", () => { const fb = L.feedback(L.calcular(B)); const s = texto(fb); assert.match(s, /conversão de consultas em reservas caiu/i); assert.match(s, /atendimento/i); assert.match(s, /preço final/i); assert.match(s, /objeç/i); });
t("consultas sem nenhuma reserva gera a Situação B", () => { const fb = L.feedback(L.calcular(base({ visualizacoes: "1800", consultas: "24", reservas: "0", ocupadas: "0" }))); assert.ok(ids(fb).includes("B")); assert.match(texto(fb), /demonstram interesse/); });
t("visualizações sem consultas gera a Situação A do prompt", () => { const fb = L.feedback(L.calcular(base({ visualizacoes: "900", consultas: "0", reservas: "0", ocupadas: "0" }))); assert.ok(ids(fb).includes("A")); assert.match(texto(fb), /fotos, a descrição, o preço total, as regras e a disponibilidade/); });

console.log("Cenário C · reservas com margem reduzida (Pilar 5)");
t("Bloco 01 calcula receita e encaminha custos para o Pilar 5, sem chamar de lucro", () => { const r = L.calcular(base({ ocupadas: "22", diaria: "390" })); assert.strictEqual(r.receita, 8580); const fb = L.feedback(r, { dificuldade: "dinheiro" }); const s = texto(fb) + r.foraDoCalculo.join(" "); assert.match(s, /Pilar 5/); assert.doesNotMatch(s, /lucro/i); });

console.log("Casos de borda");
t("campos vazios viram pendência e Situação D", () => { const r = L.calcular({ periodo: "30" }); const fb = L.feedback(r); assert.strictEqual(fb[0].id, "D"); assert.ok(r.pendencias.length >= 6); });
t("valores negativos são recusados", () => assert.ok(L.calcular(base({ ocupadas: "-3" })).erros.ocupadas));
t("texto no lugar de número é recusado", () => assert.ok(L.calcular(base({ diaria: "trezentos" })).erros.diaria));
t("noites fracionadas são recusadas", () => assert.ok(L.calcular(base({ ocupadas: "4,5" })).erros.ocupadas));
t("divisão por zero: 0 disponíveis gera erro e nenhuma conta", () => { const r = L.calcular(base({ disponiveis: "0", ocupadas: "0" })); assert.ok(r.erros.disponiveis); assert.strictEqual(r.ocupacao, null); });
t("divisão por zero: 0 visualizações não gera taxa", () => assert.strictEqual(L.calcular(base({ visualizacoes: "0", consultas: "0", reservas: "0", ocupadas: "0" })).taxaConsulta, null));
t("ocupadas maiores que disponíveis: erro", () => assert.ok(L.calcular(base({ ocupadas: "31" })).erros.ocupadas));
t("disponíveis maiores que os dias do período: erro", () => assert.ok(L.calcular(base({ periodo: "30", disponiveis: "45" })).erros.disponiveis));
t("consultas maiores que visualizações: aviso e taxa não calculada", () => { const r = L.calcular(base({ visualizacoes: "5", consultas: "9" })); assert.strictEqual(r.taxaConsulta, null); assert.ok(r.avisos.some((a) => /mais consultas/.test(a))); });
t("reservas maiores que consultas: aviso e conversão não calculada", () => { const r = L.calcular(base({ consultas: "2", reservas: "5", ocupadas: "10" })); assert.strictEqual(r.taxaReserva, null); assert.ok(r.avisos.some((a) => /mais reservas/.test(a))); });
t("reserva instantânea: conversão não calculada", () => assert.strictEqual(L.calcular(base({ reservaInstantanea: "sim" })).taxaReserva, null));
t("períodos diferentes: nenhuma taxa entre métricas", () => { const r = L.calcular(base({ mesmoPeriodo: false })); assert.strictEqual(r.taxaConsulta, null); assert.strictEqual(r.taxaReserva, null); assert.strictEqual(r.ocupacao, 30); });
t("\"Não tenho esse dado\" não vira número fictício", () => { const r = L.calcular(base({ visualizacoes: { semDado: true } })); assert.strictEqual(r.visualizacoes, null); assert.strictEqual(r.taxaConsulta, null); assert.ok(r.pendencias.some((p) => /Não tenho esse dado/.test(p))); assert.ok(ids(L.feedback(r)).includes("D")); });
t("período personalizado inválido é recusado", () => assert.ok(L.calcular(base({ periodo: "outro", periodoDias: "0" })).erros.periodoDias));
t("meta acima das disponíveis é recusada", () => assert.ok(L.calcular(base({ meta: "40" })).erros.meta));
t("correção de dados: recalcula do zero", () => { const r1 = L.calcular(base({ ocupadas: "31" })); assert.ok(!r1.valido); const r2 = L.calcular(base({ ocupadas: "12" })); assert.ok(r2.valido); assert.strictEqual(r2.ocupacao, 40); });
t("todo feedback tem as 5 partes preenchidas", () => { [A, B, base(), base({ consultas: "0" }), { periodo: "30" }].forEach((x) => L.feedback(L.calcular(x)).forEach((b) => ["resultado", "significado", "atencao", "fazer", "verificar"].forEach((k) => assert.ok(b[k] && b[k].trim(), b.id + " sem " + k)))); });
t("nenhum feedback usa juízo de valor sem referência", () => { [A, B, base(), base({ consultas: "0" })].forEach((x) => assert.doesNotMatch(texto(L.feedback(L.calcular(x))), PROIBIDAS)); });

console.log("\n" + ok + " passaram, " + falhas + " falharam");
process.exit(falhas ? 1 : 0);

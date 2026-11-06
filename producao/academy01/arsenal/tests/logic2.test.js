// Testes dos Pilares 2 a 7. Rodar: node producao/academy01/arsenal/tests/logic2.test.js
const assert = require("assert");
const P = require("../src/logic2.js");
let ok = 0, falhas = 0;
function t(n, fn) { try { fn(); ok++; console.log("  ok  " + n); } catch (e) { falhas++; console.log("  FALHOU  " + n + "\n        " + e.message); } }
const PROIBIDAS = /\b(bom|boa|ruim|abaixo da média|acima da média|garant|lucro líquido de)/i;
const txt = (fb) => fb.map((b) => [b.resultado, b.significado, b.atencao, b.fazer, b.verificar].join(" ")).join(" ");

console.log("Pilar 2 · Perfil");
t("afinidade = itens que o imóvel tem ÷ itens do perfil", () => { const a = P.afinidade(["banheira", "lareira", "vista"], 2); const c = a.find((x) => x.id === "casal"); assert.strictEqual(c.pct, 75); assert.deepStrictEqual(c.faltam, ["isolamento"]); assert.strictEqual(a[0].id, "casal"); });
t("perfil que não cabe na capacidade vai para o fim", () => { const a = P.afinidade(["quartos2", "churrasqueira", "piscina", "areaExterna"], 2); assert.notStrictEqual(a[0].id, "amigos"); assert.strictEqual(a.find((x) => x.id === "amigos").cabe, false); });
t("valida pessoas acima da capacidade", () => assert.ok(P.validarPerfil({ publico: "casal", ocasiao: "x", pessoas: "5", necessidade: "x", objecao: "x", essenciais: ["a", "b", "c"] }, [], 2).erros.pessoas));
t("exige exatamente 3 essenciais", () => assert.ok(P.validarPerfil({ publico: "casal", ocasiao: "x", pessoas: "2", necessidade: "x", objecao: "x", essenciais: ["vista"] }, ["vista"], 2).erros.essenciais));
t("avisa essencial que o imóvel não tem", () => { const v = P.validarPerfil({ publico: "casal", ocasiao: "aniversário", pessoas: "2", necessidade: "privacidade", objecao: "vizinhos", essenciais: ["banheira", "vista", "piscina"] }, ["banheira", "vista"], 2); assert.ok(v.valido); assert.ok(v.avisos.some((a) => /Piscina/.test(a))); });

console.log("Pilar 3 · Proposta de valor");
const ctx3 = { hospedagem: "Cabana Serra", publicoNome: "Casal em escapada", necessidade: "privacidade", diferenciais: [{ caracteristica: "Ofurô com vista para o vale", beneficio: "relaxar a dois ao entardecer", verdadeiro: true }, { caracteristica: "Lareira a lenha", verdadeiro: true }, { caracteristica: "Piscina aquecida", verdadeiro: false }] };
t("monta a frase só com diferenciais verdadeiros", () => { const s = P.montarProposta(ctx3); assert.match(s, /Ofurô com vista para o vale e Lareira a lenha/); assert.doesNotMatch(s, /Piscina/); });
t("avaliação aprova a proposta montada", () => { const a = P.avaliarProposta(P.montarProposta(ctx3), ctx3); assert.strictEqual(a.aprovados, a.total); });
t("aponta palavras vagas e diferencial não confirmado", () => { const a = P.avaliarProposta("Para casal, um lugar aconchegante e incrível com Piscina aquecida e muita paz para descansar.", ctx3); assert.ok(a.checks.some((c) => !c.ok && /aconchegante/.test(c.txt))); assert.ok(a.checks.some((c) => !c.ok && /Piscina aquecida/.test(c.txt))); });

console.log("Pilar 4 · Anúncio");
t("título acima de 50 caracteres reprova", () => assert.ok(!P.avaliarTitulo("Cabana para casal com ofurô e lareira na serra catarinense", ctx3).checks[0].ok));
t("título bom passa nos 5 critérios", () => { const a = P.avaliarTitulo("Ofurô e lareira: cabana para casal na serra", ctx3); assert.strictEqual(a.aprovados, a.total, JSON.stringify(a.checks)); });
t("título em maiúsculas e vago reprova", () => { const a = P.avaliarTitulo("CASA INCRÍVEL E ACONCHEGANTE", ctx3); assert.ok(a.aprovados <= 2); });
t("descrição curta e sem regras reprova", () => assert.ok(P.avaliarDescricao("Casa linda.", {}).aprovados <= 2));

console.log("Pilar 5 · Financeiro (Cenário C)");
const C = { receita: "8580", noites: "22", reservas: "8", taxaPlataforma: "15", impostos: "6", limpezaPorReserva: "120", variavelPorNoite: "45", fixosPeriodo: "5200" };
t("margem de contribuição com fórmula explícita", () => { const r = P.financeiro(C); assert.strictEqual(Math.round(r.taxas), 1287); assert.strictEqual(Math.round(r.impostos), 515); assert.strictEqual(r.variaveis, 960 + 990); assert.strictEqual(Math.round(r.margem), 4828); });
t("resultado operacional = margem − fixos", () => assert.strictEqual(Math.round(P.financeiro(C).resultado), -372));
t("ponto de equilíbrio em noites", () => { const r = P.financeiro(C); assert.strictEqual(r.equilibrioNoites, Math.ceil(5200 / (r.margem / 22))); });
t("Cenário C: identifica que a margem não cobre os fixos e o maior custo", () => { const fb = P.feedbackFinanceiro(P.financeiro(C)); assert.strictEqual(fb[0].id, "C2"); assert.match(txt(fb), /custos fixos do período/); assert.match(txt(fb), /taxas, despesas variáveis e margem/); });
t("não chama resultado de lucro líquido", () => { [C, Object.assign({}, C, { fixosPeriodo: "100" })].forEach((x) => { const r = P.financeiro(x); assert.doesNotMatch(txt(P.feedbackFinanceiro(r)), PROIBIDAS); assert.ok(r.premissas.some((p) => /Não é lucro líquido/.test(p))); }); });
t("margem negativa: cada noite custa mais do que rende", () => assert.strictEqual(P.feedbackFinanceiro(P.financeiro(Object.assign({}, C, { variavelPorNoite: "400" })))[0].id, "C1"));
t("percentual acima de 100 é recusado", () => assert.ok(P.financeiro(Object.assign({}, C, { taxaPlataforma: "120" })).erros.taxaPlataforma));
t("0 noites: sem divisão por zero", () => { const r = P.financeiro(Object.assign({}, C, { noites: "0" })); assert.ok(!r.valido); assert.ok(r.erros.noites); });
t("reservas acima das noites recusado", () => assert.ok(P.financeiro(Object.assign({}, C, { reservas: "30" })).erros.reservas));
t("simulador mantém estadia média e proporções", () => { const s = P.simular(P.financeiro(C), "450", "22"); assert.strictEqual(s.receita, 9900); assert.strictEqual(s.reservas, 8); assert.ok(s.resultado > P.financeiro(C).resultado); });
t("simulador recusa noites zero", () => assert.strictEqual(P.simular(P.financeiro(C), "450", "0"), null));

console.log("Pilar 6 · Experiência");
t("prioridade = impacto × 2 − custo − esforço", () => { assert.strictEqual(P.prioridade(3, 1, 1), 4); assert.strictEqual(P.prioridade(1, 3, 3), -4); assert.strictEqual(P.prioridade(4, 1, 1), null); });
t("ordena melhorias pela prioridade", () => { const r = P.rankMelhorias([{ texto: "a", impacto: 1, custo: 3, esforco: 3 }, { texto: "b", impacto: 3, custo: 1, esforco: 1 }]); assert.strictEqual(r[0].texto, "b"); });
t("etapas com falha são listadas", () => assert.deepStrictEqual(P.etapasFrageis({ chegada: "falha", estadia: "funciona", pos: "falha" }), ["Chegada", "Pós-estadia"]));

console.log("Pilar 7 · Plano de 30 dias");
t("quadrantes da matriz impacto × esforço", () => { assert.strictEqual(P.quadrante("alto", "baixo"), "Fazer primeiro"); assert.strictEqual(P.quadrante("baixo", "alto"), "Deixar para depois"); });
t("cronograma exige semana para cada ação", () => assert.ok(!P.validarCronograma([{ texto: "x", selecionada: true }]).valido));
t("avisa duas mudanças no mesmo indicador na mesma semana", () => { const v = P.validarCronograma([{ texto: "foto", selecionada: true, semana: 1, indicador: "Consultas por visualização" }, { texto: "título", selecionada: true, semana: 1, indicador: "Consultas por visualização" }]); assert.ok(v.valido); assert.ok(v.avisos.some((a) => /mesmo indicador/.test(a))); });
t("limita a 8 ações", () => assert.ok(!P.validarCronograma(Array.from({ length: 9 }, (_, i) => ({ texto: "a" + i, selecionada: true, semana: 1 + (i % 4) }))).valido));

console.log("\n" + ok + " passaram, " + falhas + " falharam");
process.exit(falhas ? 1 : 0);

// Testes da lógica do Diagnóstico de Gestão. Uso: node tests/test_logic.js
const Z = require("../src/logic.js");
let ok = 0, fal = 0; const log = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
const todos = (v) => Object.fromEntries(Z.AREAS.map((a) => [a.id, v]));
const cinco = (v) => Object.fromEntries(Z.CINCO.map((q) => [q.id, v]));

// 1. tudo zero → nota 0, improviso, área 1 frágil, começa pelo módulo 1
let r = Z.calcular({ situacao: "dono", cinco: cinco(0), areas: todos(0) });
log(r.nota === 0 && r.faixa.rot === "Gestão no improviso", `tudo zero: nota ${r.nota}, faixa ${r.faixa.rot}`);
log(r.fragil && r.fragil.id === "metas" && r.inicio.n === 1, "tudo zero: área frágil = Planejamento e metas, módulo 1");
log(r.nsCinco.length === 5 && r.zero.length === 8, "tudo zero: 5 Não sei e 8 áreas em branco");

// 2. tudo no máximo → nota 100, método, sem área frágil, módulo 7
r = Z.calcular({ situacao: "dono", cinco: cinco(2), areas: todos(2) });
log(r.nota === 100 && r.faixa.rot === "Gestão com método", `tudo no máximo: nota ${r.nota}`);
log(r.fragil === null && r.inicio.n === 7, "tudo no máximo: sem área frágil, começa pelo módulo 7");
log(/Nenhuma área em branco/.test(Z.textoFragil(r)), "texto do frágil quando nada falta");

// 3. pesos: áreas valem 60, cinco perguntas valem 40
r = Z.calcular({ cinco: cinco(0), areas: todos(2) }); log(r.nota === 60, `só áreas cheias = 60 (deu ${r.nota})`);
r = Z.calcular({ cinco: cinco(2), areas: todos(0) }); log(r.nota === 40, `só cinco perguntas cheias = 40 (deu ${r.nota})`);
r = Z.calcular({ cinco: cinco(1), areas: todos(1) }); log(r.nota === 50 && r.faixa.rot === "Gestão em construção", `tudo pela metade = 50, em construção (deu ${r.nota})`);

// 4. faixas nos limites
log(Z.calcular({ cinco: { entrou: 2, sobrou: 2, ocupacao: 2, diaria: 1, custo: 0 }, areas: { metas: 1, financas: 1, preco: 1, vendas: 1, pessoas: 1, compras: 0, operacao: 0, qualidade: 0 } }).nota === 47, "mistura: 5/16 áreas e 7/10 perguntas = 19 + 28 = 47");
const f = (n) => Z.FAIXAS.find((x) => n >= x.min && n <= x.max).rot;
log(f(34) === "Gestão no improviso" && f(35) === "Gestão em construção" && f(64) === "Gestão em construção" && f(65) === "Gestão com método", "limites das faixas: 34/35 e 64/65");

// 5. área frágil: primeira com 0; sem 0, primeira com 1
r = Z.calcular({ cinco: cinco(2), areas: { metas: 2, financas: 1, preco: 2, vendas: 0, pessoas: 2, compras: 1, operacao: 2, qualidade: 2 } });
log(r.fragil.id === "vendas" && r.inicio.n === 4, "frágil = primeira área com 0 (vendas), módulo 4");
r = Z.calcular({ cinco: cinco(2), areas: { metas: 2, financas: 1, preco: 2, vendas: 2, pessoas: 2, compras: 1, operacao: 2, qualidade: 2 } });
log(r.fragil.id === "financas" && r.inicio.n === 2, "sem 0: frágil = primeira área com 1 (finanças), módulo 2");
// operação (área 7) aponta para o módulo 6 e é a ponte para a Jornada 3
r = Z.calcular({ cinco: cinco(2), areas: { ...todos(2), operacao: 0 } });
log(r.fragil.id === "operacao" && r.inicio.n === 6, "operação frágil → módulo 6");
// todas as áreas em 2, mas Não sei nas cinco → área 8 (indicadores)
r = Z.calcular({ cinco: cinco(0), areas: todos(2) });
log(r.fragil.id === "qualidade" && r.inicio.n === 7, "só os números faltam → área 8, módulo 7");

// 6. ação e verificação vêm da área frágil
r = Z.calcular({ cinco: cinco(2), areas: { ...todos(2), preco: 0 } });
log(Z.acaoSugerida(r) === Z.AREAS[2].acao && Z.comoVerificar(r) === Z.AREAS[2].verifica, "ação e verificação da área de preço");

// 7. completo e concluído
const S = { situacao: "dono", cinco: cinco(1), areas: todos(1) };
log(Z.completo(S) && !Z.completo({ ...S, situacao: "" }) && !Z.completo({ ...S, areas: { ...todos(1), metas: null } }), "completo exige situação, cinco perguntas e oito áreas");
log(!Z.concluido(S) && !Z.concluido({ ...S, acao: "curta", prazo: "2026-12-01" }) && Z.concluido({ ...S, acao: "Fechar o mês passado em uma folha", prazo: "2026-12-01" }), "concluído exige ação (10+ letras) e prazo");

// 8. leituras de rotina e tempo
log(Z.leituraSaida({ saida: "nao" }).includes("ponto de partida") && Z.leituraSaida({}) === "" && Z.leituraRotina({ rotina: "nunca" }).includes("começa") && Z.leituraTempo({ tempo: "operacao" }).includes("hora marcada") && Z.leituraRotina({}) === "", "leituras de rotina e tempo");

// 9. integridade dos dados
log(Z.AREAS.length === 8 && Z.CINCO.length === 5 && Z.MODULOS.length === 8, "8 áreas, 5 perguntas, 8 módulos");
log(Z.AREAS.every((a) => a.acao.length > 30 && a.verifica.length > 20 && a.s && a.p), "cada área tem ação e verificação");
log(Object.values(Z.MODULO_DA_AREA).every((n) => n >= 1 && n <= 7), "cada área aponta para um módulo de 1 a 7");
const proibidas = /garant|retorno garantido|lucro certo|renda extra|valoriza/i;
log(!proibidas.test(JSON.stringify(Z)), "nenhuma promessa proibida nos textos");

console.log(`\n${ok} ok, ${fal} falhou`); process.exit(fal ? 1 : 0);

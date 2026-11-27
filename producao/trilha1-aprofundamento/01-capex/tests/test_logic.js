// Testes da lógica da ficha "Faça agora · O meu CAPEX" (PLANO.md, seções 6 e 7).
// Uso: node producao/trilha1-aprofundamento/01-capex/tests/test_logic.js
"use strict";
const fs = require("fs"), path = require("path");
const Z = require("../src/logic.js");
const HOJE = "2026-11-27";
let ok = 0, fal = 0;
const disparados = new Set();
function t(nome, cond, extra) { if (cond) ok++; else { fal++; console.log("  FALHOU  " + nome + (extra !== undefined ? "  -> " + JSON.stringify(extra) : "")); } }
const perto = (a, b, tol = 0.005) => typeof a === "number" && Math.abs(a - b) <= tol;
const ids = (A) => { A.forEach((a) => disparados.add(a.id)); return A.map((a) => a.id); };
const clone = (x) => JSON.parse(JSON.stringify(x));

/* ---------- um estado pequeno e válido, para as bordas ---------- */
function linha(o) { const l = Z.novaLinha({ nome: o.nome || "Linha", modo: o.modo || "valor", tagP6: o.tag, porUnidade: o.pu, tipologia: o.tip, forma: o.forma, enxoval: o.enx }); return Object.assign(l, o.campos || {}); }
const cot = (nome, valor, extra) => linha({ nome, campos: Object.assign({ valor, origem: "cotacao", nCotacoes: 3, mesmaEspec: true }, extra || {}) });
const est = (nome, valor) => linha({ nome, campos: { valor, origem: "estimativa" } });
const bra = (nome) => linha({ nome, campos: { origem: "branco" } });
const na = (nome) => linha({ nome, campos: { origem: "naoAplica" } });
function base(o = {}) {
  const E = Z.estadoInicial(HOJE);
  Object.assign(E, {
    projeto: "Projeto de teste", situacao: "abrir", tipo: "cabanas", imovelPronto: false, d1: "palpite", d2: "alguns", d3: "algumas", d4: "nao",
    palpite: 200000, unidadesFase: 2, unidadesProjeto: 2, primeiraObra: false, fatoresRisco: [],
    distanciaEnergiaM: 100, infraDimensionadaPara: 2, enxovalNaoDuplicado: true, contingenciaPct: 10,
    regraParaQue: "Imprevisto da obra orçada.", regraQuemAutoriza: "Eu, depois do engenheiro.", regraComoRegistra: "Planilha com data e motivo.", regraQuandoConfere: "A cada medição da obra.",
    giro: 30000, terrenoSituacao: "meu", terrenoValor: 100000, acao30: "Pedir três cotações da unidade.", verificacao: "Três propostas com a mesma especificação.", prazo: Z.somaDias(HOJE, 10),
  });
  const tip = linha({ nome: "Unidade tipo 1", tip: true, forma: "construida", campos: { qtd: 2, areaM2: 50, custoM2: 1000, origem: "cotacao", nCotacoes: 3, mesmaEspec: true } });
  E.blocos = { 1: [cot("Projetos", 10000)], 2: [cot("Rede", o.b2 !== undefined ? o.b2 : 50000)], 3: [tip], 4: [cot("Móveis", o.b4 !== undefined ? o.b4 : 100000)], 5: [cot("Enxoval e utensílios", o.b5 !== undefined ? o.b5 : 12000)], 6: [cot("Pré-abertura", o.b6 !== undefined ? o.b6 : 7500)] };
  return E;
}
const calc = (E) => Z.calcular(E, HOJE);
const al = (E) => ids(Z.alertas(E, calc(E)));

/* ================= 1. O exemplo dos Chalés do Ribeirão, campo a campo ================= */
const EX = Z.exemplo(HOJE);
const C = calc(EX);
t("ex: bloco 1 = 40.000", C.totalBloco[1] === 40000, C.totalBloco[1]);
t("ex: bloco 2 = 170.000", C.totalBloco[2] === 170000, C.totalBloco[2]);
t("ex: bloco 3 = 682.000", C.totalBloco[3] === 682000, C.totalBloco[3]);
t("ex: bloco 4 = 85.800", C.totalBloco[4] === 85800, C.totalBloco[4]);
t("ex: bloco 5 = 11.700", C.totalBloco[5] === 11700, C.totalBloco[5]);
t("ex: bloco 6 = 21.000", C.totalBloco[6] === 21000, C.totalBloco[6]);
t("ex: subtotal = 1.010.500", C.subtotal === 1010500, C.subtotal);
t("ex: reserva 15% = 151.575", perto(C.contingencia, 151575, 1e-6), C.contingencia);
t("ex: CAPEX da fase = 1.162.075", perto(C.capexFase, 1162075, 1e-6), C.capexFase);
t("ex: giro = 3 × 15.000 = 45.000", C.giro === 45000, C.giro);
t("ex: investimento total = 1.207.075", perto(C.investimentoTotal, 1207075, 1e-6), C.investimentoTotal);
t("ex: custo por unidade = 290.518,75", perto(C.custoPorUnidade, 290518.75, 1e-6), C.custoPorUnidade);
t("ex: investimento por unidade = 301.768,75", perto(C.investimentoPorUnidade, 301768.75, 1e-6), C.investimentoPorUnidade);
t("ex: área total = 188 m²", C.areaTotal === 188, C.areaTotal);
t("ex: custo por m² = 6.181,25", perto(C.custoPorM2, 6181.25, 1e-6), C.custoPorM2);
const PESOS = { 1: 0.034421, 2: 0.146290, 3: 0.586881, 4: 0.073833, 5: 0.010068, 6: 0.018071, 7: 0.130435 };
t("ex: pesos dos sete blocos (6 casas)", Object.keys(PESOS).every((b) => perto(C.pctBloco[b], PESOS[b], 1e-6)), C.pctBloco);
const somaPesos = Object.values(C.pctBloco).reduce((s, x) => s + x, 0);
t("ex: soma dos pesos = 1", Math.abs(somaPesos - 1) < 1e-9, somaPesos);
t("ex: com uma casa a soma dá 99,9%", Object.values(C.pctBloco).reduce((s, x) => s + Z.arred(x * 100, 1), 0).toFixed(1) === "99.9");
t("ex: obra = 852.000 e 73,3%", C.obra === 852000 && Z.fmtPct(C.pctObra) === "73,3%", [C.obra, C.pctObra]);
t("ex: palpite cobre 60,2%", Z.fmtPct(C.palpiteCobre) === "60,2%", C.palpiteCobre);
t("ex: diferença do palpite = 462.075", perto(C.diferencaPalpite, 462075, 1e-6), C.diferencaPalpite);
t("ex: 32 linhas (17 C, 10 E, 5 B)", C.nLinhas === 32 && C.nCotadas === 17 && C.nEstimadas === 10 && C.nBranco === 5, [C.nLinhas, C.nCotadas, C.nEstimadas, C.nBranco]);
t("ex: 53,1% das linhas com cotação", Z.fmtPct(C.pctLinhasCotadas) === "53,1%", C.pctLinhasCotadas);
t("ex: valor cotado 957.000 e estimado 53.500", C.valorCotado === 957000 && C.valorEstimado === 53500, [C.valorCotado, C.valorEstimado]);
t("ex: 94,7% do valor com cotação", Z.fmtPct(C.pctValorCotado) === "94,7%", C.pctValorCotado);
t("ex: conferência dupla por origem", C.valorCotado + C.valorEstimado === C.subtotal);
t("ex: três maiores = chalés, apoio, energia", C.top3.map((x) => x.valor).join() === "576000,70000,42000", C.top3);
t("ex: degrau Calculista, diagnóstico Estimador", C.degrau === "Calculista" && C.degrauDiagnostico === "Estimador", [C.degrau, C.degrauDiagnostico]);
t("ex: 7 cotações completas e 10 incompletas", C.n3Cotacoes === 7 && C.nCotacoesIncompletas === 10, [C.n3Cotacoes, C.nCotacoesIncompletas]);
t("ex: incompletas = 2 com uma cotação e 8 com duas", C.incompletas.filter((x) => x.n === 1).length === 2 && C.incompletas.filter((x) => x.n === 2).length === 8);
t("ex: 1 vencida (água, 130 dias)", C.cotacoesVencidas === 1 && C.vencidas[0].dias === 130 && /Água/.test(C.vencidas[0].nome), C.vencidas);
t("ex: enxoval ÷ mobiliário = 13,6%", Z.fmtPct(C.osePctFFE) === "13,6%", C.osePctFFE);
t("ex: pré-abertura ÷ obra = 2,5%", Z.fmtPct(C.preAberturaPctObra) === "2,5%", C.preAberturaPctObra);
const AEX = Z.alertas(EX, C);
t("ex: alertas na ordem A11, A13, A14", ids(Z.tresPrimeiros(AEX)).join() === "A11,A13,A14", ids(AEX));
t("ex: sem A6, A4, A3, A9, A12", !ids(AEX).some((x) => ["A6", "A4", "A3", "A9", "A12"].includes(x)));
const sEX = Z.acaoSugerida(EX, C, AEX);
t("ex: ação de ordem 3 (linhas em branco)", sEX.ordem === 3, sEX);
t("ex: ação lista as cinco linhas em branco na ordem", sEX.acao === "Pedir cotação escrita das linhas em branco: licença ambiental, internet, segurança, licença de funcionamento e cadastros e seguro do primeiro ano.", sEX.acao);
t("ex: verificação das cinco propostas", sEX.verificacao === "As 5 propostas recebidas, com data e escopo, lançadas na ficha.", sEX.verificacao);
t("ex: prazo 27/12/2026", EX.prazo === "2026-12-27" && Z.prazoOk(EX.prazo, HOJE));
const T = C.transposicao;
t("ex: transposição unidade 144.000, deck 9.000, luz 3.500, água 2.500", T.l_unidade === 144000 && T.l_deck === 9000 && T.l_luz === 3500 && T.l_agua === 2500, T);
t("ex: transposição mobiliário 22.125 e piso 0 no m²", T.l_mobilia === 22125 && T.l_piso === 0 && T.pisoNoM2 === true);
t("ex: unidade pronta 181.125", T.pronta === 181125, T.pronta);
t("ex: licenças 40.000 e reserva 15%", T.licencas === 40000 && T.reserva_pct === 15);
t("ex: infraestrutura comum à parte 288.900", perto(T.infra, 288900, 1e-6), T.infra);
t("ex: identidade da transposição = CAPEX", T.confere && perto(T.conferencia, 1162075, 0.01), T.conferencia);
t("ex: terreno 300.000 à parte, fora da soma", C.terreno === 300000 && perto(C.investimentoTotal, C.capexFase + 45000, 1e-6));
const CR = Z.criterio(EX, C, HOJE);
t("ex: critério 1 a 8 cumpridos antes do PDF", CR.antesDoPdf && !CR.ok && CR.faltas.length === 1, CR.faltas);
const EX2 = clone(EX); EX2.pdfBaixado = true;
t("ex: com o PDF baixado, selo concedido", Z.criterio(EX2, calc(EX2), HOJE).ok);
t("ex: todas as telas validam", Z.TELAS.every((tl) => Z.validarTela(tl, EX, HOJE) === ""), Z.TELAS.map((tl) => Z.validarTela(tl, EX, HOJE)));
t("ex: notas da página 6 (3, 1, 0)", Z.notaP6("cotacao") === 3 && Z.notaP6("estimativa") === 1 && Z.notaP6("branco") === 0 && Z.notaP6("naoAplica") === null);
t("ex: resumo.dados com capex e investimento", (() => { const d = Z.resumoDados(EX, C); return d.capex_fase === 1162075 && d.investimento_total === 1207075 && d.exemplo === true && d.infra_comum === 288900; })());
t("ex: rótulo de dados fictícios", /dados fictícios/.test(Z.TEXTOS.exemplo));

/* ================= 2. Exercícios E2 e E4 ================= */
const E2 = clone(EX);
const ch = E2.blocos[3][0]; Object.assign(ch, { forma: "pronta", modo: "qtdUnit", valorUnit: 150000, areaM2: "", freteMontagemConfirmados: false });
const C2 = calc(E2);
t("E2: bloco 3 = 706.000", C2.totalBloco[3] === 706000, C2.totalBloco[3]);
t("E2: subtotal = 1.034.500", C2.subtotal === 1034500, C2.subtotal);
t("E2: reserva = 155.175", perto(C2.contingencia, 155175, 1e-6), C2.contingencia);
t("E2: CAPEX = 1.189.675", perto(C2.capexFase, 1189675, 1e-6), C2.capexFase);
t("E2: alerta A15 (frete, fundação e montagem)", al(E2).includes("A15"));
t("E2: estrutura pronta sem área: custo por m² nulo", C2.areaTotal === null && C2.custoPorM2 === null);
t("E2: transposição continua fechando", C2.transposicao.confere);
ch.freteMontagemConfirmados = true;
t("E2: confirmado por escrito, sem A15", !al(E2).includes("A15"));

const E4 = clone(EX); E4.contingenciaPct = 8;
const C4 = calc(E4);
t("E4: reserva a 8% = 80.840", perto(C4.contingencia, 80840, 1e-6), C4.contingencia);
t("E4: diferença para 15% = 70.735", perto(C.contingencia - C4.contingencia, 70735, 1e-6));
t("E4: alertas A3 e A4", al(E4).includes("A3") && al(E4).includes("A4"));
const E12 = clone(EX); E12.contingenciaPct = 12;
t("exemplo a 12%: A4 por primeira obra, sem A3", al(E12).includes("A4") && !al(E12).includes("A3"));

/* ================= 3. Fórmulas básicas e modos de linha ================= */
const B = base();
const CB = calc(B);
t("base: subtotal 279.500 e CAPEX 307.450", CB.subtotal === 279500 && perto(CB.capexFase, 307450, 1e-6), [CB.subtotal, CB.capexFase]);
t("base: sem alertas", al(B).length === 0, al(B));
t("base: transposição fecha", CB.transposicao.confere);
t("modo valor", Z.valorLinha(cot("x", "12.500,50"), B) === 12500.5);
t("modo quantidade × valor", Z.valorLinha(linha({ modo: "qtdUnit", campos: { qtd: 3, valorUnit: 1000, origem: "estimativa" } }), B) === 3000);
t("modo área: qtd × área × m²", Z.valorLinha(linha({ modo: "area", campos: { qtd: 2, areaM2: "12,5", custoM2: 2000, origem: "cotacao", nCotacoes: 1 } }), B) === 50000);
t("linha por unidade sem qtd usa as unidades da fase", Z.valorLinha(linha({ modo: "qtdUnit", pu: true, campos: { valorUnit: 500, origem: "estimativa" } }), B) === 1000);
t("enxoval = unidades × camas × 3 jogos × custo", Z.valorLinha(linha({ enx: true, campos: { camasPorUnidade: 2, custoJogo: 400, origem: "cotacao", nCotacoes: 3, mesmaEspec: true } }), B) === 2 * 2 * 3 * 400);
t("linha em branco vale 0", Z.valorLinha(linha({ campos: { valor: 9999, origem: "branco" } }), B) === 0);
t("linha não se aplica vale 0", Z.valorLinha(linha({ campos: { valor: 9999, origem: "naoAplica" } }), B) === 0);
t("valor inválido devolve null e erro", Z.valorLinha(cot("x", 0), B) === null && Z.erroLinha(cot("x", 0), B, HOJE) !== "");
t("valor acima de 100 milhões é recusado", Z.erroLinha(cot("Linha", 100000001), B, HOJE) !== "" && Z.erroLinha(cot("Linha", 100000000), B, HOJE) === "");
t("linha sem origem bloqueia a tela", (() => { const E = base(); E.blocos[1].push(linha({ nome: "Sem origem" })); return /de onde vem/.test(Z.validarTela("b1", E, HOJE)); })());
t("cotação sem número de propostas bloqueia", Z.erroLinha(linha({ nome: "Cotada", campos: { valor: 10, origem: "cotacao" } }), B, HOJE) !== "");
t("data de cotação no futuro é recusada", Z.erroLinha(cot("Linha", 10, { dataCotacao: "2026-11-28" }), B, HOJE) !== "" && Z.erroLinha(cot("Linha", 10, { dataCotacao: HOJE }), B, HOJE) === "");
t("qtd fracionada é recusada", Z.erroLinha(linha({ nome: "Itens", modo: "qtdUnit", campos: { qtd: "2,5", valorUnit: 10, origem: "estimativa" } }), B, HOJE) !== "");
t("área fora da faixa é recusada (0,05 m²)", Z.erroLinha(linha({ nome: "Sala", modo: "area", campos: { qtd: 1, areaM2: "0,05", custoM2: 10, origem: "estimativa" } }), B, HOJE) !== "");
t("bloco com 16 linhas é recusado", (() => { const E = base(); E.blocos[1] = Array.from({ length: 16 }, (_, i) => cot("L" + i, 10)); return /15 linhas/.test(Z.validarTela("b1", E, HOJE)); })());
t("bloco sem linhas é recusado", (() => { const E = base(); E.blocos[4] = []; return Z.validarTela("b4", E, HOJE) !== ""; })());
t("pré-abertura inteira não se aplica é recusada", (() => { const E = base(); E.blocos[6] = [na("Tudo")]; return Z.validarTela("b6", E, HOJE) !== ""; })());

/* ================= 4. Bordas ================= */
// tipologias ≠ fase
const ET = base(); ET.blocos[3][0].qtd = 3;
t("tipologias somando 3 com fase de 2: A17 primeiro", al(ET)[0] === "A17");
t("tipologias ≠ fase bloqueiam a tela das unidades", /somam 3/.test(Z.validarTela("b3", ET, HOJE)));
t("tipologias ≠ fase impedem o critério 1", !Z.criterio(ET, calc(ET), HOJE).itens[0].ok);
const ET2 = base(); ET2.blocos[3].push(linha({ nome: "Tipo 2", tip: true, forma: "construida", campos: { qtd: 1, areaM2: 30, custoM2: 1000, origem: "estimativa" } })); ET2.blocos[3][0].qtd = 1;
t("duas tipologias somando a fase passam", Z.validarTela("b3", ET2, HOJE) === "" && Z.tipologiasConferem(ET2));
const ET3 = base(); ET3.blocos[3].push(...["T2", "T3", "T4"].map((n) => linha({ nome: n, tip: true, campos: { origem: "naoAplica" } })));
t("quatro tipologias são recusadas", /até 3/.test(Z.validarTela("b3", ET3, HOJE)));
// zero unidades
const EZ = base(); EZ.unidadesFase = 0;
t("zero unidades: tela da fase recusa", Z.validarTela("fase", EZ, HOJE) !== "");
t("zero unidades: custo por unidade nulo e sem transposição", calc(EZ).custoPorUnidade === null && calc(EZ).transposicao === null);
t("zero unidades: critério 1 falha", !Z.criterio(EZ, calc(EZ), HOJE).itens[0].ok);
t("201 unidades: tela da fase recusa", (() => { const E = base(); E.unidadesFase = 201; return Z.validarTela("fase", E, HOJE) !== ""; })());
t("projeto completo menor que a fase é recusado", (() => { const E = base(); E.unidadesProjeto = 1; return Z.validarTela("fase", E, HOJE) !== ""; })());
// capexFase = 0
const E0 = base(); for (let b = 1; b <= 6; b++) E0.blocos[b].forEach((l) => (l.origem = "branco"));
const C0 = calc(E0);
t("CAPEX zero: pesos nulos", C0.capexFase === 0 && Object.values(C0.pctBloco).every((x) => x === null));
t("CAPEX zero: degrau Sonhador", C0.degrau === "Sonhador");
t("CAPEX zero: A1 com os seis blocos", (() => { const A = Z.alertas(E0, C0); ids(A); const a = A.find((x) => x.id === "A1"); return a && a.blocos.length === 6; })());
t("CAPEX zero: ação de ordem 1", Z.acaoSugerida(E0, C0).ordem === 1);
t("CAPEX zero: critério 3 falha", !Z.criterio(E0, C0, HOJE).itens[2].ok);
t("CAPEX zero: custo por m² = 0 e palpite sem comparação", C0.custoPorM2 === 0 && C0.palpiteCobre === null);
// só o bloco 3 com valor
const E3 = base(); [1, 2, 4, 5, 6].forEach((b) => E3.blocos[b].forEach((l) => (l.origem = "branco")));
t("só o bloco 3 com valor: Sonhador", calc(E3).degrau === "Sonhador");
// bloco 4 = 0
const E4z = base(); E4z.blocos[4][0].origem = "branco";
t("bloco 4 = 0: proporção do enxoval nula, sem A9", calc(E4z).osePctFFE === null && !al(E4z).includes("A9"));
t("bloco 4 em branco: A1 aponta o bloco 4", Z.alertas(E4z, calc(E4z)).find((a) => a.id === "A1").blocos.join() === "4");
// obra = 0 (imóvel pronto, blocos 2 e 3 não se aplicam)
const EO = base(); EO.imovelPronto = true; EO.blocos[2] = [na("Rede")]; EO.blocos[3] = [na("Adequação")]; EO.contingenciaPct = 20;
const CO = calc(EO);
t("obra = 0: pré-abertura ÷ obra nula, sem A11", CO.obra === 0 && CO.preAberturaPctObra === null && !al(EO).includes("A11"));
t("imóvel pronto: blocos 2 e 3 inteiros em não se aplica passam", Z.validarTela("b2", EO, HOJE) === "" && Z.validarTela("b3", EO, HOJE) === "");
t("imóvel pronto: critério 2 e 5 cumpridos", (() => { const it = Z.criterio(EO, CO, HOJE).itens; return it[1].ok && it[4].ok; })());
t("sem imóvel pronto: bloco 2 inteiro não se aplica é recusado", (() => { const E = base(); E.blocos[2] = [na("Rede")]; return Z.validarTela("b2", E, HOJE) !== ""; })());
t("imóvel pronto: nome do bloco 3 vira Adequação e reforma", Z.nomeBloco(3, EO) === "Adequação e reforma" && Z.nomeBloco(3, B) === "Unidades e áreas comuns");
// área ausente
const EA = base(); EA.blocos[3][0] = linha({ nome: "Bolha", tip: true, forma: "pronta", campos: { qtd: 2, valorUnit: 50000, origem: "cotacao", nCotacoes: 3, mesmaEspec: true, freteMontagemConfirmados: true } });
t("tipologia sem área: área total e custo por m² nulos", calc(EA).areaTotal === null && calc(EA).custoPorM2 === null);
EA.blocos[3][0].areaM2 = Z.NS;
t("área Não sei: só afeta o custo por m²", calc(EA).custoPorM2 === null && calc(EA).totalBloco[3] === 100000 && Z.validarTela("b3", EA, HOJE) === "");
// reserva 0, 10, 15, 25, 25,01
const res = (p, o = {}) => { const E = base(); E.contingenciaPct = p; Object.assign(E, o); return al(E); };
t("reserva 0: A3z e CAPEX = subtotal", res(0).includes("A3z") && (() => { const E = base(); E.contingenciaPct = 0; const c = calc(E); return c.capexFase === c.subtotal; })());
t("reserva vazia: A3z", res("").includes("A3z"));
t("reserva 0: critério 4 falha", (() => { const E = base(); E.contingenciaPct = 0; return !Z.criterio(E, calc(E), HOJE).itens[3].ok; })());
t("reserva 0 é recusada na tela", (() => { const E = base(); E.contingenciaPct = 0; return Z.validarTela("reserva", E, HOJE) !== ""; })());
t("reserva 9,99: A3", res(9.99).includes("A3"));
t("reserva 10: sem A3", !res(10).includes("A3") && res(10).length === 0);
t("reserva 10 com primeira obra: A4", res(10, { primeiraObra: true }).includes("A4"));
t("reserva 10 com fator de risco: A4", res(10, { fatoresRisco: ["remoto"] }).includes("A4"));
t("reserva 15 com primeira obra: sem A4", !res(15, { primeiraObra: true }).includes("A4"));
t("reserva 25: sem A5", !res(25).includes("A5"));
t("reserva 25,01: A5", res(25.01).includes("A5"));
t("reserva 50,01 é recusada na tela", (() => { const E = base(); E.contingenciaPct = 50.01; return Z.validarTela("reserva", E, HOJE) !== ""; })());
t("imóvel pronto a 12%: A3 (régua de reforma 15%)", res(12, { imovelPronto: true }).includes("A3") && !res(15, { imovelPronto: true }).includes("A3"));
t("reserva = subtotal × % (base dos blocos 1 a 6)", (() => { const E = base(); E.contingenciaPct = 12.5; const c = calc(E); return perto(c.contingencia, c.subtotal * 0.125, 1e-9); })());
// enxoval ÷ mobiliário exatamente 10% e 15%
t("enxoval exatamente 10%: sem A9", !al(base({ b5: 10000 })).includes("A9"));
t("enxoval exatamente 15%: sem A9", !al(base({ b5: 15000 })).includes("A9"));
t("enxoval 9,999%: A9 (abaixo)", al(base({ b5: 9999 })).includes("A9") && /abaixo/.test(Z.alertas(base({ b5: 9999 })).find((a) => a.id === "A9").tit));
t("enxoval 15,001%: A9 (acima)", al(base({ b5: 15001 })).includes("A9") && /acima/.test(Z.alertas(base({ b5: 15001 })).find((a) => a.id === "A9").tit));
// pré-abertura exatamente 5%
t("pré-abertura exatamente 5% da obra: sem A11", (() => { const E = base({ b6: 7500 }); return Z.div(calc(E).totalBloco[6], calc(E).obra) === 0.05 && !al(E).includes("A11"); })());
t("pré-abertura 4,99%: A11", al(base({ b6: 7499 })).includes("A11"));
t("pré-abertura 0: A11 (inclui zero)", (() => { const E = base(); E.blocos[6] = [bra("Pré-abertura")]; return al(E).includes("A11"); })());
// obra exatamente 80% e 80,01%
t("obra exatamente 80%: sem A12", (() => { const E = base({ b2: 846000, b6: 7000 }); return calc(E).pctObra === 0.8 && !al(E).includes("A12"); })());
t("obra 80,01%: A12", (() => { const E = base({ b2: 847000, b6: 7000 }); return calc(E).pctObra > 0.8001 && al(E).includes("A12"); })());
// cotação com 90 e 91 dias
t("cotação com 90 dias ainda vale", (() => { const E = base(); E.blocos[1][0].dataCotacao = Z.somaDias(HOJE, -90); return calc(E).cotacoesVencidas === 0 && !al(E).includes("A13"); })());
t("cotação com 91 dias vence: A13", (() => { const E = base(); E.blocos[1][0].dataCotacao = Z.somaDias(HOJE, -91); return calc(E).cotacoesVencidas === 1 && al(E).includes("A13"); })());
t("data antiga em linha estimada não conta como vencida", (() => { const E = base(); E.blocos[1][0] = Object.assign(est("Projetos", 10000), { dataCotacao: "2025-01-01" }); return calc(E).cotacoesVencidas === 0; })());
// linhas cotadas exatamente 50%
function meioCotado(extraCot) {
  const E = base();
  E.blocos[1] = [cot("A", 100000), est("e1", 1000)];
  E.blocos[2] = [cot("B", 90000), est("e2", 1000)];
  E.blocos[4] = [extraCot ? cot("e3", 1000) : est("e3", 1000)];
  E.blocos[5] = [];
  E.blocos[6] = [];
  return E; // linhas: A, e1, B, e2, tipologia (cotada), e3 → 3 de 6 = 50%
}
t("exatamente 50% das linhas cotadas: não é Calculista", (() => { const c = calc(meioCotado(false)); return c.pctLinhasCotadas === 0.5 && c.degrau === "Estimador"; })());
t("mais de 50% e três maiores cotadas: Calculista", (() => { const c = calc(meioCotado(true)); return c.pctLinhasCotadas > 0.5 && c.degrau === "Calculista"; })());
t("maioria cotada mas a maior linha estimada: Estimador", (() => { const E = meioCotado(true); E.blocos[1][0].origem = "estimativa"; E.blocos[1][1].origem = "cotacao"; E.blocos[1][1].nCotacoes = 3; return calc(E).degrau === "Estimador"; })());
t("leituras das linhas cotadas: 0 / até 50% / mais de 50%", /mapa do que cotar/.test(Z.leituraLinhasCotadas(0)) && /maior parte/.test(Z.leituraLinhasCotadas(0.5)) && /maioria/.test(Z.leituraLinhasCotadas(0.5001)));
// giro
t("giro de 3 meses: sem A16", (() => { const E = base(); E.giroMeses = 3; E.giroCustoMensal = 10000; return !al(E).includes("A16") && calc(E).giro === 30000; })());
t("giro de 2,9 meses: A16", (() => { const E = base(); E.giroMeses = "2,9"; E.giroCustoMensal = 10000; return al(E).includes("A16"); })());
t("giro 25 meses é recusado", (() => { const E = base(); E.giroMeses = 25; E.giroCustoMensal = 1; return Z.validarTela("giro", E, HOJE) !== ""; })());
t("giro zero para quem vai abrir é recusado", (() => { const E = base(); E.giro = 0; return /maior que zero/.test(Z.validarTela("giro", E, HOJE)) && !Z.criterio(E, calc(E), HOJE).itens[5].ok; })());
t("giro zero para quem amplia, com justificativa: aceito", (() => { const E = base(); E.situacao = "ampliar"; E.giro = 0; E.giroZeroJustificativa = "O caixa da operação já cobre o giro separado."; return Z.validarTela("giro", E, HOJE) === "" && Z.criterio(E, calc(E), HOJE).itens[5].ok; })());
t("giro zero para quem amplia, sem justificativa: recusado", (() => { const E = base(); E.situacao = "ampliar"; E.giro = 0; return Z.validarTela("giro", E, HOJE) !== ""; })());
// prazo
t("prazo em hoje + 30: válido", Z.prazoOk(Z.somaDias(HOJE, 30), HOJE));
t("prazo em hoje + 31: inválido", !Z.prazoOk(Z.somaDias(HOJE, 31), HOJE));
t("prazo ontem: inválido", !Z.prazoOk(Z.somaDias(HOJE, -1), HOJE) && Z.prazoOk(HOJE, HOJE));
t("prazo inválido bloqueia a tela e o critério 8", (() => { const E = base(); E.prazo = Z.somaDias(HOJE, 31); return Z.validarTela("acao", E, HOJE) !== "" && !Z.criterio(E, calc(E), HOJE).itens[7].ok; })());
t("ação com 9 letras é recusada", (() => { const E = base(); E.acao30 = "123456789"; return Z.validarTela("acao", E, HOJE) !== ""; })());

/* ================= 5. "Não sei" em cada campo que o aceita ================= */
const ns = (campo, v = Z.NS) => { const E = base(); E[campo] = v; return E; };
t("palpite Não sei: tela passa, sem comparação", (() => { const E = ns("palpite"); return Z.validarTela("palpite", E, HOJE) === "" && calc(E).palpiteCobre === null && /Sem palpite/.test(Z.leituraPalpite(calc(E))); })());
t("palpite 0 é aceito (cobre 0%)", (() => { const E = ns("palpite", 0); return Z.validarTela("palpite", E, HOJE) === "" && calc(E).palpiteCobre === 0; })());
t("palpite negativo é recusado", Z.validarTela("palpite", ns("palpite", -1), HOJE) !== "");
t("unidades do projeto Não sei: A7 e critério 1 falha", (() => { const E = ns("unidadesProjeto"); return Z.validarTela("fase", E, HOJE) === "" && al(E).includes("A7") && !Z.criterio(E, calc(E), HOJE).itens[0].ok; })());
t("rede Não sei: A7, ação de ordem 2 e critério 5 falha", (() => { const E = ns("infraDimensionadaPara"); return al(E).includes("A7") && Z.acaoSugerida(E).ordem === 2 && !Z.criterio(E, calc(E), HOJE).itens[4].ok; })());
t("distância da energia Não sei: A8", (() => { const E = ns("distanciaEnergiaM"); return Z.validarTela("b2", E, HOJE) === "" && al(E).includes("A8"); })());
t("distância 0 m é aceita, sem A8", (() => { const E = ns("distanciaEnergiaM", 0); return Z.validarTela("b2", E, HOJE) === "" && !al(E).includes("A8"); })());
t("reserva Não sei: tela passa, A3z e critério 4 falha", (() => { const E = ns("contingenciaPct"); return Z.validarTela("reserva", E, HOJE) === "" && al(E).includes("A3z") && !Z.criterio(E, calc(E), HOJE).itens[3].ok; })());
t("giro Não sei: investimento total nulo e critério 6 falha", (() => { const E = ns("giro"); return Z.validarTela("giro", E, HOJE) === "" && calc(E).investimentoTotal === null && !Z.criterio(E, calc(E), HOJE).itens[5].ok; })());
t("valor do terreno Não sei: terreno nulo, tela passa", (() => { const E = ns("terrenoValor"); return calc(E).terreno === null && Z.validarTela("giro", E, HOJE) === ""; })());
t("terreno sem situação bloqueia a tela e o critério 7", (() => { const E = ns("terrenoSituacao", null); return Z.validarTela("giro", E, HOJE) !== "" && !Z.criterio(E, calc(E), HOJE).itens[6].ok; })());

/* ================= 6. Os outros alertas, um a um ================= */
t("A6: rede para 4 com projeto de 6", (() => { const E = base(); E.unidadesProjeto = 6; E.infraDimensionadaPara = 4; return al(E).includes("A6") && Z.acaoSugerida(E).ordem === 2 && /6 unidades/.test(Z.acaoSugerida(E).acao); })());
t("A6 não dispara com rede = projeto", (() => { const E = base(); E.unidadesProjeto = 6; E.infraDimensionadaPara = 6; return !al(E).includes("A6"); })());
t("A2: bloco com valor e sem cotação", (() => { const E = base(); E.blocos[1][0].origem = "estimativa"; const A = Z.alertas(E, calc(E)); ids(A); return A.find((a) => a.id === "A2").blocos.join() === "1"; })());
t("A10: enxoval não confirmado", (() => { const E = base(); E.enxovalNaoDuplicado = false; return al(E).includes("A10"); })());
t("A14: cotação com duas propostas", (() => { const E = base(); E.blocos[1][0].nCotacoes = 2; return al(E).includes("A14") && calc(E).nCotacoesIncompletas === 1; })());
t("A14: três propostas sem a mesma especificação", (() => { const E = base(); E.blocos[1][0].mesmaEspec = false; return al(E).includes("A14"); })());
t("A18: vou comprar o terreno", al(ns("terrenoSituacao", "comprar")).includes("A18"));
t("A19: quem amplia", al(ns("situacao", "ampliar")).includes("A19"));
t("A20: regra de uso com menos de 10 letras", (() => { const E = ns("regraQuandoConfere", "sempre"); return al(E).includes("A20") && !Z.criterio(E, calc(E), HOJE).itens[3].ok; })());
t("A20 não bloqueia a tela da reserva (bloqueia o selo)", Z.validarTela("reserva", ns("regraQuandoConfere", ""), HOJE) === "");
t("ordem dos alertas segue a lista do plano", (() => { const E = base(); E.situacao = "ampliar"; E.terrenoSituacao = "comprar"; E.contingenciaPct = 5; E.primeiraObra = true; E.enxovalNaoDuplicado = false; E.distanciaEnergiaM = Z.NS; const A = al(E); return A.join() === ["A8", "A3", "A4", "A10", "A18", "A19"].join(); })());
t("só três alertas na Atenção", (() => { const E = base(); E.situacao = "ampliar"; E.terrenoSituacao = "comprar"; E.contingenciaPct = 5; E.primeiraObra = true; return Z.tresPrimeiros(Z.alertas(E)).length === 3; })());

/* ================= 7. Ações de 30 dias (ordem 4 a 7) ================= */
t("ação 4: degrau abaixo de Calculista, sem brancos", (() => { const E = base(); E.blocos[2][0].origem = "estimativa"; E.blocos[4][0].origem = "estimativa"; E.blocos[5][0].origem = "estimativa"; const s = Z.acaoSugerida(E); return s.ordem === 4 && /três maiores linhas: unidade tipo 1, móveis e rede/.test(s.acao); })(), Z.acaoSugerida((() => { const E = base(); E.blocos[2][0].origem = "estimativa"; E.blocos[4][0].origem = "estimativa"; E.blocos[5][0].origem = "estimativa"; return E; })()));
t("ação 5: Calculista com cotação incompleta", (() => { const E = base(); E.blocos[1][0].nCotacoes = 2; return Z.acaoSugerida(E).ordem === 5; })());
t("ação 6: só faixa de conferência (enxoval)", (() => { const E = base({ b5: 5000 }); const s = Z.acaoSugerida(E); return s.ordem === 6 && /bloco 4 · Mobiliário e equipamentos e 5 · Enxoval/.test(s.acao); })());
t("ação 7: nada disparou, volta ao Pilar 6", (() => { const s = Z.acaoSugerida(base()); return s.ordem === 7 && /Pilar 6/.test(s.acao); })());
t("ação 7 para operador fala do dono", /ao dono/.test(Z.acaoSugerida(ns("situacao", "operador")).acao));
t("próxima etapa muda com a turma", /encontro do Pilar 6/.test(Z.proximaEtapa({ turma: "acompanhamento" })) && /Planilha 2/.test(Z.proximaEtapa({ turma: "autonomo" })));
t("toda verificação sugerida está na lista", [EX, base(), E0, ns("infraDimensionadaPara"), base({ b5: 5000 })].every((E) => Z.VERIFICACOES.some((v) => v === Z.acaoSugerida(E).verificacao || /propostas recebidas/.test(Z.acaoSugerida(E).verificacao))));

/* ================= 8. Identidade da transposição em estados variados ================= */
let semente = 7; const rnd = () => ((semente = (semente * 16807) % 2147483647) / 2147483647);
let todasFecham = true;
for (let k = 0; k < 200; k++) {
  const E = base({ b2: Math.round(rnd() * 400000) + 1, b4: Math.round(rnd() * 200000) + 1, b5: Math.round(rnd() * 30000) + 1, b6: Math.round(rnd() * 50000) + 1 });
  E.unidadesFase = 1 + Math.floor(rnd() * 9); E.unidadesProjeto = E.unidadesFase; E.blocos[3][0].qtd = E.unidadesFase;
  E.contingenciaPct = Math.round(rnd() * 5000) / 100 || 1;
  E.blocos[2].push(linha({ nome: "Luz", modo: "qtdUnit", pu: true, tag: "luz", campos: { valorUnit: Math.round(rnd() * 9000) + 1, origem: "estimativa" } }));
  E.blocos[3].push(linha({ nome: "Deck", modo: "qtdUnit", pu: true, tag: "deck", campos: { valorUnit: Math.round(rnd() * 9000) + 1, origem: "cotacao", nCotacoes: 2 } }));
  E.blocos[4].push(linha({ nome: "Cama", modo: "qtdUnit", pu: true, tag: "mobilia", campos: { valorUnit: Math.round(rnd() * 9000) + 1, origem: "estimativa" } }));
  const c = calc(E);
  if (!c.transposicao.confere) { todasFecham = false; break; }
}
t("transposição fecha com o CAPEX em 200 estados sorteados (tolerância R$ 0,01)", todasFecham);

/* ================= 9. Integridade dos dados e varredura de promessas ================= */
t("21 alertas na lista de prioridade, sem repetição", Z.ORDEM_ALERTAS.length === 21 && new Set(Z.ORDEM_ALERTAS).size === 21);
t("sete blocos, o 7 é a reserva", Z.BLOCOS.length === 7 && Z.BLOCOS[6].nome === "Reserva do imprevisto");
t("quatro perguntas de diagnóstico", Z.DIAG.length === 4 && Z.DIAG.every((d) => d.op.length >= 2));
t("cinco fatores de risco", Z.FATORES.length === 5);
t("ajuda para as 10 telas de pergunta, com por que, onde e exemplo", ["palpite", "fase", "b1", "b2", "b3", "b4", "b5", "b6", "reserva", "giro"].every((k) => Z.AJUDA[k] && Z.AJUDA[k].porque && Z.AJUDA[k].onde && Z.AJUDA[k].exemplo && Z.AJUDA[k].explica));
const sugeridas = [];
for (const sit of ["abrir", "ampliar"]) for (const ip of [false, true]) for (let b = 1; b <= 6; b++) Z.linhasSugeridas(b, { situacao: sit, imovelPronto: ip, tipo: "cabanas" }).forEach((l) => sugeridas.push({ b, l }));
t("linhas sugeridas vêm só com o nome, nunca com valor", sugeridas.length > 0 && sugeridas.every(({ l }) => l.nome && !l.valor && !l.valorUnit && !l.custoM2 && !l.areaM2 && !l.qtd && !l.origem && !l.custoJogo));
t("bloco 2 de quem amplia sugere reforço da rede existente", Z.linhasSugeridas(2, { situacao: "ampliar" })[0].nome === "Reforço da rede existente" && !Z.linhasSugeridas(2, { situacao: "abrir" }).some((l) => /Reforço/.test(l.nome)));
t("bloco 3 sugere uma tipologia com etiqueta unidade", Z.linhasSugeridas(3, {}).filter((l) => l.tipologia && l.tagP6 === "unidade").length === 1);
t("bloco 5 traz a linha especial do enxoval", Z.linhasSugeridas(5, {}).some((l) => l.enxoval));
t("todas as linhas sugeridas têm até 15 por bloco e nome de 2 a 80 letras", sugeridas.every(({ l }) => l.nome.length >= 2 && l.nome.length <= 80) && [1, 2, 3, 4, 5, 6].every((b) => Z.linhasSugeridas(b, { situacao: "ampliar" }).length <= 15));
t("estado inicial sem nenhum valor de referência", (() => { const E = Z.estadoInicial(HOJE); return ["palpite", "unidadesFase", "contingenciaPct", "giro", "terrenoValor", "acao30"].every((k) => E[k] === ""); })());
// varredura: todo texto que a ficha mostra
const textos = [];
Object.values(Z.TEXTOS).forEach((x) => textos.push(x));
Z.REGUA.forEach((x) => textos.push(x.t)); Object.values(Z.AJUDA).forEach((a) => Object.values(a).forEach((x) => textos.push(x))); Z.VERIFICACOES.forEach((x) => textos.push(x));
Object.values(Z.INFO).forEach((x) => (Array.isArray(x) ? x.forEach((y) => textos.push(y)) : textos.push(x)));
[EX, E2, E4, E0, ET, EO, base(), ns("situacao", "ampliar"), ns("terrenoSituacao", "comprar"), base({ b5: 5000 }), base({ b2: 847000, b6: 7000 })].forEach((E) => {
  const c = calc(E); Z.alertas(E, c).forEach((a) => textos.push(a.tit, a.txt)); const s = Z.acaoSugerida(E, c); textos.push(s.acao, s.verificacao, Z.leituraDegrau(c), Z.leituraReserva(E), Z.leituraPalpite(c), Z.proximaEtapa(E));
});
sugeridas.forEach(({ l }) => textos.push(l.nome));
t("varredura: nenhuma promessa proibida (" + textos.length + " textos)", textos.every(Z.textoSeguro), textos.filter((x) => !Z.textoSeguro(x)));
t("varredura: a própria varredura pega 'retorno garantido'", !Z.textoSeguro("Retorno garantido em 12 meses"));
t("varredura: sem a Marina e sem siglas FF&E e OS&E", textos.every((x) => !/Marina|FF&E|OS&E/.test(x)));
t("aviso diz que não substitui engenheiro, arquiteto ou contador", /não substitui engenheiro, arquiteto ou contador/.test(Z.TEXTOS.aviso));
t("promessa no formato 'Aprenda o passo a passo'", /^Aprenda o passo a passo/.test(Z.TEXTOS.promessa));
t("formatação pt-BR (brl, fmtPct, empate para o par)", Z.brl(1162075) === "R$ 1.162.075,00" && Z.fmtPct(0.13043478) === "13,0%" && Z.arred(0.125, 2) === 0.12 && Z.paraNumero("1.162.075,50") === 1162075.5);

/* ================= 10. A página pública usa esta mesma lógica ================= */
const PUB = path.resolve(__dirname, "../../../../docs/trilha1/capex");
if (fs.existsSync(path.join(PUB, "index.html"))) {
  const html = fs.readFileSync(path.join(PUB, "index.html"), "utf8");
  t("cópia pública de logic.js idêntica à de src/", fs.readFileSync(path.join(PUB, "logic.js"), "utf8") === fs.readFileSync(path.resolve(__dirname, "../src/logic.js"), "utf8"));
  t("a página carrega logic.js", /<script src="logic\.js"><\/script>/.test(html));
  t("a página não envia dados (sem fetch, XMLHttpRequest, sendBeacon, FEEDBACK_URL)", !/fetch\(|XMLHttpRequest|sendBeacon|FEEDBACK_URL|webhook/i.test(html));
  t("a página usa o jsPDF 2.5.1 do cdnjs, como o Pilar 6", /cdnjs\.cloudflare\.com\/ajax\/libs\/jspdf\/2\.5\.1\/jspdf\.umd\.min\.js/.test(html));
  t("a página salva na chave zion-t1-pilar6a com try/catch", /zion-t1-pilar6a/.test(html) && /try\s*\{\s*window\.localStorage\.setItem/.test(html));
  t("a página não tem mentor virtual", !/mentor/i.test(html));
  t("varredura da página: nenhuma promessa proibida", Z.textoSeguro(html.replace(/<script[\s\S]*?<\/script>/g, "")));
} else console.log("  (página pública ainda não existe: verificações da seção 10 puladas)");

/* ================= 11. Todos os 21 alertas foram disparados em algum teste ================= */
const faltando = Z.ORDEM_ALERTAS.filter((x) => !disparados.has(x));
t("os 21 alertas foram disparados ao menos uma vez", faltando.length === 0, faltando);

console.log(`\n${ok} testes aprovados, ${fal} falharam (lógica do CAPEX).`);
process.exit(fal ? 1 : 0);

// Testes da lógica da ficha "Faça agora · O seu CAPEX" (página 6A), PLANO.md versão 2, seções 6 e 7.
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
function linha(o) { const l = Z.novaLinha({ nome: o.nome || "Linha", modo: o.modo || "valor", tagP6: o.tag, porUnidade: o.pu, tipologia: o.tip, forma: o.forma, enxoval: o.enx, comum: o.comum, geral: o.geral }); return Object.assign(l, o.campos || {}); }
const cot = (nome, valor, extra) => linha({ nome, campos: Object.assign({ valor, origem: "cotacao", nCotacoes: 3, mesmaEspec: true }, extra || {}) });
const est = (nome, valor) => linha({ nome, campos: { valor, origem: "estimativa" } });
const bra = (nome) => linha({ nome, campos: { origem: "branco" } });
const na = (nome) => linha({ nome, campos: { origem: "naoAplica" } });
function base(o = {}) {
  const E = Z.estadoInicial(HOJE);
  Object.assign(E, {
    projeto: "Projeto de teste", situacao: "terreno", tipo: "cabanas", imovelPronto: false, d1: "referencia", d2: "algumas", d3: "algumas", d4: "nao",
    pagina6Total: 300000, limite6: 400000, unidadesFase: 2, unidadesProjeto: 2, primeiraObra: false, fatoresRisco: [],
    distanciaEnergiaM: 100, infraDimensionadaPara: 2, enxovalNaoDuplicado: true, reservaPct: 10,
    regraParaQue: "Imprevisto da obra orçada.", regraQuemAutoriza: "Eu, depois do engenheiro.", regraComoRegistra: "Planilha com data e motivo.", regraQuandoConfere: "A cada medição da obra.",
    giro: 30000, terrenoSituacao: "meu", terrenoValor: 100000, acao30: "Pedir três cotações da unidade.", verificacao: "Três propostas com a mesma especificação.", prazo: Z.somaDias(HOJE, 10),
  });
  const tip = linha({ nome: "Unidade tipo 1", tip: true, forma: "construida", campos: { qtd: 2, areaM2: 50, custoM2: 1000, origem: "cotacao", nCotacoes: 3, mesmaEspec: true } });
  E.partes = { 1: [cot("Projetos", 10000)], 2: [cot("Rede", o.p2 !== undefined ? o.p2 : 50000)], 3: [tip], 4: [cot("Móveis", o.p4 !== undefined ? o.p4 : 100000, { tagP6: "mobilia" })], 5: [cot("Enxoval e utensílios", o.p5 !== undefined ? o.p5 : 12000, { tagP6: "mobilia" })], 6: [cot("Pré-abertura", o.p6 !== undefined ? o.p6 : 7500)] };
  return E;
}
const calc = (E, h = HOJE) => Z.calcular(E, h);
const al = (E) => ids(Z.alertas(E, calc(E)));

/* ================= 1. O caso da Marina (PLANO seção 7), campo a campo ================= */
const EX = Z.exemplo(HOJE);
const C = calc(EX);
t("Marina: rótulo «Exemplo ilustrativo · dados fictícios»", Z.TEXTOS.exemplo === "Exemplo ilustrativo · dados fictícios. Não são preços de referência." && EX.exemplo === true);
t("Marina: situação do Marco Zero «terreno», cabanas, 3 de 5, primeira obra", EX.situacao === "terreno" && EX.tipo === "cabanas" && EX.unidadesFase === 3 && EX.unidadesProjeto === 5 && EX.primeiraObra === true && EX.fatoresRisco.length === 0);
t("Marina: tela 1 com 690.529,18 e limite 870.130,80, infraestrutura à parte", Z.paraNumero(EX.pagina6Total) === 690529.18 && Z.paraNumero(EX.limite6) === 870130.8 && EX.pagina6Infra === "");
t("Marina: limite = 8 × 108.766,35 (conferência)", perto(8 * 108766.35, 870130.8, 1e-6));
t("Marina: energia a 260 m, rede para 5", EX.distanciaEnergiaM === 260 && EX.infraDimensionadaPara === 5);
const TOT = { 1: 36000, 2: 128200, 3: 428400, 4: 72000, 5: 10740, 6: 12600 };
for (const p of [1, 2, 3, 4, 5, 6]) t(`Marina: Parte ${p} = ${TOT[p]}`, perto(C.totalParte[p], TOT[p], 1e-6), C.totalParte[p]);
t("Marina: subtotal = 687.940", perto(C.subtotal, 687940, 1e-6), C.subtotal);
t("Marina: reserva 15% = 103.191", perto(C.reserva, 103191, 1e-6), C.reserva);
t("Marina: CAPEX da fase = 791.131", perto(C.capexFase, 791131, 1e-6), C.capexFase);
t("Marina: giro = 40.787,38 (veio da página 6)", perto(C.giro, 40787.38, 1e-9), C.giro);
t("Marina: investimento total = 831.918,38", perto(C.investimentoTotal, 831918.38, 1e-6), C.investimentoTotal);
t("Marina: folga até o limite = 38.212,42 e dentro", perto(C.folga6, 38212.42, 1e-6) && C.dentroLimite === true, C.folga6);
t("Marina: folga em subtotal = 33.228,19 (38.212,42 ÷ 1,15)", perto(C.folgaEmSubtotal, 33228.19, 0.005), C.folgaEmSubtotal);
t("Marina: folga = cerca de 4,8% do CAPEX", Z.fmtPct(C.folgaPctCapex) === "4,8%", C.folgaPctCapex);
t("Marina: custo por unidade = 263.710,33", Z.brl(C.custoPorUnidade) === "R$ 263.710,33", C.custoPorUnidade);
t("Marina: investimento por unidade = 277.306,13", Z.brl(C.investimentoPorUnidade) === "R$ 277.306,13", C.investimentoPorUnidade);
t("Marina: área total da Parte 3 = 208 m²", C.areaTotal === 208, C.areaTotal);
t("Marina: custo por m² = 3.803,51", Z.brl(C.custoPorM2) === "R$ 3.803,51", C.custoPorM2);
const PESOS = { 1: 0.045504, 2: 0.162047, 3: 0.541503, 4: 0.091009, 5: 0.013576, 6: 0.015927, 7: 0.130435 };
t("Marina: pesos das sete partes (6 casas)", Object.keys(PESOS).every((p) => perto(C.pctParte[p], PESOS[p], 1e-6)), C.pctParte);
t("Marina: pesos exibidos 4,6 / 16,2 / 54,2 / 9,1 / 1,4 / 1,6 / 13,0", [1, 2, 3, 4, 5, 6, 7].map((p) => Z.fmtPct(C.pctParte[p])).join(" ") === "4,6% 16,2% 54,2% 9,1% 1,4% 1,6% 13,0%");
t("Marina: soma arredondada dá 100,1%", Object.values(C.pctParte).reduce((s, x) => s + Z.arred(x * 100, 1), 0).toFixed(1) === "100.1");
t("Marina: obra = 556.600 e 70,4% (sem A12)", perto(C.obra, 556600, 1e-6) && Z.fmtPct(C.pctObra) === "70,4%");
t("Marina: enxoval ÷ mobiliário = 14,9%", Z.fmtPct(C.oseSobreFFE) === "14,9%", C.oseSobreFFE);
t("Marina: pré-abertura ÷ obra = 2,3%, faltam 15.230 para os 5%", Z.fmtPct(C.preAberturaSobreObra) === "2,3%" && perto(C.faltaPreAbertura, 15230, 1e-6), C.faltaPreAbertura);
t("Marina: 39 linhas: 16 C, 18 E, 5 B (recepção NA fora)", C.nLinhas === 39 && C.nCotadas === 16 && C.nEstimadas === 18 && C.nBranco === 5 && C.nNaoAplica === 1, [C.nLinhas, C.nCotadas, C.nEstimadas, C.nBranco, C.nNaoAplica]);
const CEB = { 1: [3, 2, 1, 0], 2: [5, 4, 1, 0], 3: [3, 1, 0, 0], 4: [3, 4, 0, 0], 5: [1, 4, 1, 1], 6: [1, 3, 2, 0] };
t("Marina: linhas C / E / B / NA por parte", Object.keys(CEB).every((p) => { const x = C.porParte[p]; return [x.nCotadas, x.nEstimadas, x.nBranco, x.nNaoAplica].join() === CEB[p].join(); }), C.porParte);
const COT = { 1: [32500, 3500], 2: [99300, 28900], 3: [418800, 9600], 4: [50700, 21300], 5: [7020, 3720], 6: [4800, 7800] };
t("Marina: cotado e estimado por parte", Object.keys(COT).every((p) => perto(C.porParte[p].cotado, COT[p][0], 1e-6) && perto(C.porParte[p].estimado, COT[p][1], 1e-6)));
t("Marina: 41,0% das linhas com cotação", Z.fmtPct(C.pctLinhasCotadas) === "41,0%", C.pctLinhasCotadas);
t("Marina: valor cotado 613.120 e estimado 74.820 (conferência por origem)", perto(C.valorCotado, 613120, 1e-6) && perto(C.valorEstimado, 74820, 1e-6) && perto(C.valorCotado + C.valorEstimado, C.subtotal, 1e-6));
t("Marina: 89,1% do valor com cotação", Z.fmtPct(C.pctValorCotado) === "89,1%", C.pctValorCotado);
t("Marina: três maiores = cabanas, apoio, decks, todas cotadas", C.top3.map((x) => x.valor).join() === "319200,66000,33600" && C.top3.every((x) => x.origem === "cotacao"), C.top3);
t("Marina: degrau Estimador, igual ao diagnóstico", C.degrau === "Estimador" && C.degrauDiagnostico === "Estimador", [C.degrau, C.degrauDiagnostico]);
t("Marina: faltam 4 linhas cotadas para a maioria", C.faltamParaMaioria === 4 && /Faltam 4 linhas cotadas/.test(Z.leituraDegrau(C)), C.faltamParaMaioria);
t("Marina: 7 cotações completas e 9 incompletas (2 com uma, 7 com duas)", C.n3Cotacoes === 7 && C.nCotacoesIncompletas === 9 && C.incompletas.filter((x) => x.n === 1).length === 2 && C.incompletas.filter((x) => x.n === 2).length === 7);
t("Marina: 1 vencida (água, 135 dias)", C.cotacoesVencidas === 1 && C.vencidas[0].dias === 135 && /Água/.test(C.vencidas[0].nome), C.vencidas);
t("Marina: página 6 cobria 83,0% da 6A", Z.fmtPct(C.pagina6Cobre) === "83,0%", C.pagina6Cobre);
t("Marina: diferença página 6 × 6A = 141.389,20", perto(C.difPagina6, 141389.2, 1e-6), C.difPagina6);
t("Marina: leitura página 6 × 6A sem julgamento", Z.leituraPagina6(C, EX) === "A sua página 6 cobria 83,0% da 6A; a diferença é de R$ 141.389,20.");
t("Marina: leitura do limite (cabe, folga, R$ 33.228,19)", /Cabe no limite da página 6 \(R\$ 870\.130,80\), com folga de R\$ 38\.212,42/.test(Z.leituraLimite(C)) && /R\$ 33\.228,19/.test(Z.leituraLimite(C)));
t("Marina: o que sobra para as linhas em branco = 17.998,19", perto(C.folgaEmSubtotal - C.faltaPreAbertura, 17998.19, 0.005));
t("número em texto pt-BR para os campos", Z.numTexto(690529.18) === "690.529,18" && Z.numTexto(870130.8) === "870.130,80" && Z.numTexto(3) === "3" && Z.paraNumero(Z.numTexto(870130.8)) === 870130.8);
t("Marina: terreno 600.000 à parte, fora da soma", C.terreno === 600000 && perto(C.investimentoTotal, C.capexFase + C.giro, 1e-9));
const AEX = Z.alertas(EX, C);
t("Marina: alertas A11, A13, A14, nesta ordem", ids(AEX).join() === "A11,A13,A14", ids(AEX));
t("Marina: não disparam A21, A1, A2, A3, A4, A6, A7, A8, A9, A12, A22, A23", !ids(AEX).some((x) => ["A21", "A1", "A2", "A3", "A4", "A6", "A7", "A8", "A9", "A12", "A22", "A23"].includes(x)));
t("Marina: A11 diz faltam cerca de R$ 15.230", /Faltam cerca de R\$ 15\.230 para os 5% da obra/.test(AEX[0].txt), AEX[0].txt);
t("Marina: A13 aponta a água", /água \(135 dias\)/.test(AEX[1].txt), AEX[1].txt);
t("Marina: A14 com 9 linhas", /^9 linhas/.test(AEX[2].tit));
const sEX = Z.acaoSugerida(EX, C, AEX);
t("Marina: ação de ordem 4 (linhas em branco)", sEX.ordem === 4, sEX);
t("Marina: ação nomeia as cinco linhas em branco", sEX.acao === "Pedir cotação escrita das linhas em branco: licença ambiental, internet, segurança, licença de funcionamento e seguro do primeiro ano.", sEX.acao);
t("Marina: verificação das cinco propostas", sEX.verificacao === "As cinco propostas, com data e escopo, lançadas na ficha.", sEX.verificacao);
t("Marina: prazo 27/12/2026", EX.prazo === "2026-12-27" && Z.prazoOk(EX.prazo, HOJE));
const T = C.transposicao;
t("Marina: transposição unidade 106.400, deck 11.200, luz 1.800, água 1.600", T.l_unidade === 106400 && T.l_deck === 11200 && T.l_luz === 1800 && T.l_agua === 1600, T);
t("Marina: transposição mobiliário 26.780 e piso 0 digitado (no m²)", perto(T.l_mobilia, 26780, 1e-6) && T.l_piso === 0 && T.pisoNoM2 === true);
t("Marina: unidade pronta 147.780", perto(T.pronta, 147780, 1e-6), T.pronta);
t("Marina: licenças 36.000, reserva 15%, giro 3 meses", T.licencas === 36000 && T.reserva_pct === 15 && T.giro_meses === 3);
t("Marina: infraestrutura comum 245.290", perto(T.infra, 245290, 1e-6), T.infra);
t("Marina: identidade da transposição = CAPEX", T.confere && perto(T.conferencia, 791131, 0.01), T.conferencia);
t("Marina: notas 3 / 3 / 1 / 1 / 1 / — / 1 / 1", [T.notas.l_unidade, T.notas.l_deck, T.notas.l_luz, T.notas.l_agua, T.notas.l_mobilia, T.notas.l_piso, T.notas.licencas, T.notas.infra].join() === "3,3,1,1,1,,1,1", T.notas);
const P1 = C.planilha1;
t("Marina: Planilha 1 Premissas 352.800, Infraestrutura 252.400, FF&E 69.600, OS&E 13.140", perto(P1.premissas, 352800, 1e-6) && perto(P1.infraestrutura, 252400, 1e-6) && perto(P1.ffe, 69600, 1e-6) && perto(P1.ose, 13140, 1e-6), P1);
t("Marina: Planilha 1 subtotal 687.940 e TOTAL 791.131 (identidade)", P1.confere && perto(P1.subtotal, 687940, 1e-6) && perto(P1.total, 791131, 1e-6));
t("Marina: contingência = 13,0% do total na Planilha 1", Z.fmtPct(P1.contingenciaPctTotal) === "13,0%");
const CR = Z.criterio(EX, C, HOJE);
t("Marina: critério 1 a 9 cumprido antes do PDF", CR.antesDoPdf && !CR.ok && CR.faltas.length === 1 && CR.itens.length === 10, CR.faltas);
const EXp = clone(EX); EXp.pdfBaixado = true;
t("Marina: com o PDF baixado, selo concedido", Z.criterio(EXp, calc(EXp), HOJE).ok);
t("Marina: todas as telas validam", Z.TELAS.every((tl) => Z.validarTela(tl, EX, HOJE) === ""), Z.TELAS.map((tl) => Z.validarTela(tl, EX, HOJE)));
t("Marina: resumo.dados (capex, investimento, folga, infra comum, página 6)", (() => { const d = Z.resumoDados(EX, C); return d.capex_fase === 791131 && d.investimento_total === 831918.38 && d.folga6 === 38212.42 && d.infra_comum === 245290 && d.pagina6_total === 690529.18 && d.pagina6_cobre_pct === 83 && d.exemplo === true && d.parte3 === 428400; })(), Z.resumoDados(EX, C));
t("Marina: página 6 refeita daria 7,65 anos e cerca de R$ 617 de diária", Z.fmtN(C.investimentoTotal / 108766.35, 2) === "7,65" && Math.round(C.investimentoTotal / 8 / 0.4 / 421.575) === 617);
t("Marina: sensibilidade CAPEX +20% = 990.144,58 (a 6A só cita)", perto(C.capexFase * 1.2 + C.giro, 990144.58, 0.005) && /não calcula/.test(Z.TEXTOS.sensibilidade));
t("Marina: o exemplo mostra os mesmos números em outro dia (datas andam com hoje)", (() => { const h = "2027-03-15"; const E2 = Z.exemplo(h); const c = calc(E2, h); return perto(c.capexFase, 791131, 1e-6) && c.cotacoesVencidas === 1 && c.vencidas[0].dias === 135 && E2.prazo === "2027-04-14" && ids(Z.alertas(E2, c)).join() === "A11,A13,A14" && Z.TELAS.every((tl) => Z.validarTela(tl, E2, h) === ""); })());
t("Marina: nenhuma linha com preço da Zion Glamping Store", (() => { const s = JSON.stringify(EX); return !/129000|192346|25915|3931/.test(s); })());

/* ================= 2. Exercícios E2 e E4 (PLANO 5.4) ================= */
const E2 = clone(EX);
const agua = E2.partes[2].find((l) => /^Água: poço/.test(l.nome)); agua.valor = 22400; agua.dataCotacao = HOJE;
const C2 = calc(E2);
t("E2: Parte 2 = 130.800", perto(C2.totalParte[2], 130800, 1e-6), C2.totalParte[2]);
t("E2: subtotal = 690.540", perto(C2.subtotal, 690540, 1e-6));
t("E2: reserva = 103.581", perto(C2.reserva, 103581, 1e-6), C2.reserva);
t("E2: CAPEX = 794.121", perto(C2.capexFase, 794121, 1e-6), C2.capexFase);
t("E2: investimento total = 834.908,38", perto(C2.investimentoTotal, 834908.38, 1e-6));
t("E2: folga = 35.222,42", perto(C2.folga6, 35222.42, 1e-6), C2.folga6);
t("E2: A13 some", !al(E2).includes("A13") && al(E2).includes("A11"));
t("E2: transposição continua fechando", C2.transposicao.confere && C2.planilha1.confere);
t("E4: 10% das seis linhas por cabana = 44.334", perto(0.1 * 3 * C.transposicao.pronta, 44334, 1e-6));
const E4 = clone(EX); E4.reservaPct = 10;
const C4 = calc(E4);
t("E4: 10% do subtotal = 68.794", perto(C4.reserva, 68794, 1e-6), C4.reserva);
t("E4: diferença para 15% = 34.397", perto(C.reserva - C4.reserva, 34397, 1e-6));
t("E4: a 10%, aparece A4 (primeira obra), sem A3", al(E4).includes("A4") && !al(E4).includes("A3"));
t("E4: a 10%, a ação continua a das linhas em branco", Z.acaoSugerida(E4).ordem === 4);

/* ================= 3. Fórmulas básicas e modos de linha ================= */
const B = base();
const CB = calc(B);
t("base: subtotal 279.500, CAPEX 307.450, investimento 337.450, folga 62.550", CB.subtotal === 279500 && perto(CB.capexFase, 307450, 1e-6) && perto(CB.investimentoTotal, 337450, 1e-6) && perto(CB.folga6, 62550, 1e-6));
t("base: sem alertas", al(B).length === 0, al(B));
t("base: transposição e Planilha 1 fecham", CB.transposicao.confere && CB.planilha1.confere);
t("modo valor", Z.valorLinha(cot("x", "12.500,50"), B) === 12500.5);
t("modo quantidade × valor", Z.valorLinha(linha({ modo: "qtdUnit", campos: { qtd: 3, valorUnit: 1000, origem: "estimativa" } }), B) === 3000);
t("modo área: qtd × área × m²", Z.valorLinha(linha({ modo: "area", campos: { qtd: 2, areaM2: "12,5", custoM2: 2000, origem: "cotacao", nCotacoes: 1 } }), B) === 50000);
t("linha por unidade sem qtd usa as unidades da fase", Z.valorLinha(linha({ modo: "qtdUnit", pu: true, campos: { valorUnit: 500, origem: "estimativa" } }), B) === 1000);
t("enxoval = unidades × camas × 3 jogos × custo", Z.valorLinha(linha({ enx: true, campos: { camasPorUnidade: 2, custoJogo: 400, origem: "cotacao", nCotacoes: 3, mesmaEspec: true } }), B) === 2 * 2 * 3 * 400);
t("linha em branco vale 0", Z.valorLinha(linha({ campos: { valor: 9999, origem: "branco" } }), B) === 0);
t("linha não se aplica vale 0", Z.valorLinha(linha({ campos: { valor: 9999, origem: "naoAplica" } }), B) === 0);
t("valor inválido devolve null e erro", Z.valorLinha(cot("x", 0), B) === null && Z.erroLinha(cot("x", 0), B, HOJE) !== "");
t("valor acima de 100 milhões é recusado", Z.erroLinha(cot("Linha", 100000001), B, HOJE) !== "" && Z.erroLinha(cot("Linha", 100000000), B, HOJE) === "");
t("quantidade de 999 metros cabe; 1.000 não", Z.erroLinha(linha({ nome: "Caminho", modo: "qtdUnit", campos: { qtd: 999, valorUnit: 10, origem: "estimativa" } }), B, HOJE) === "" && Z.erroLinha(linha({ nome: "Caminho", modo: "qtdUnit", campos: { qtd: 1000, valorUnit: 10, origem: "estimativa" } }), B, HOJE) !== "");
t("tipologia com 201 unidades é recusada", Z.erroLinha(linha({ nome: "Tipo", tip: true, campos: { qtd: 201, areaM2: 10, custoM2: 10, origem: "estimativa" } }), B, HOJE) !== "");
t("linha sem origem bloqueia a tela", (() => { const E = base(); E.partes[1].push(linha({ nome: "Sem origem" })); return /de onde vem/.test(Z.validarTela("p1", E, HOJE)); })());
t("cotação sem número de propostas bloqueia", Z.erroLinha(linha({ nome: "Cotada", campos: { valor: 10, origem: "cotacao" } }), B, HOJE) !== "");
t("data de cotação no futuro é recusada", Z.erroLinha(cot("Linha", 10, { dataCotacao: "2026-11-28" }), B, HOJE) !== "" && Z.erroLinha(cot("Linha", 10, { dataCotacao: HOJE }), B, HOJE) === "");
t("qtd fracionada é recusada", Z.erroLinha(linha({ nome: "Itens", modo: "qtdUnit", campos: { qtd: "2,5", valorUnit: 10, origem: "estimativa" } }), B, HOJE) !== "");
t("área fora da faixa é recusada (0,05 m²)", Z.erroLinha(linha({ nome: "Sala", modo: "area", campos: { qtd: 1, areaM2: "0,05", custoM2: 10, origem: "estimativa" } }), B, HOJE) !== "");
t("parte com 16 linhas é recusada", (() => { const E = base(); E.partes[1] = Array.from({ length: 16 }, (_, i) => cot("L" + i, 10)); return /15 linhas/.test(Z.validarTela("p1", E, HOJE)); })());
t("parte sem linhas é recusada", (() => { const E = base(); E.partes[4] = []; return Z.validarTela("p4", E, HOJE) !== ""; })());
t("pré-abertura inteira não se aplica é recusada", (() => { const E = base(); E.partes[6] = [na("Tudo")]; return Z.validarTela("p6", E, HOJE) !== ""; })());

/* ================= 4. Tela 1 · a página 6 ================= */
const p6 = (v, o = {}) => { const E = base(); E.pagina6Total = v; Object.assign(E, o); return E; };
t("página 6 com número: tela passa", Z.validarTela("pagina6", p6(300000), HOJE) === "");
t("página 6 vazia: tela bloqueia", Z.validarTela("pagina6", p6(""), HOJE) !== "");
t("página 6 negativa e acima de 100 milhões: recusadas", Z.validarTela("pagina6", p6(-1), HOJE) !== "" && Z.validarTela("pagina6", p6(100000001), HOJE) !== "");
t("página 6 = 0 é aceita (cobre 0%)", Z.validarTela("pagina6", p6(0), HOJE) === "" && calc(p6(0)).pagina6Cobre === 0);
t("Não fiz a página 6: tela passa, A22, sem comparação", (() => { const E = p6(Z.NAO_FIZ, { limite6: "" }); const c = calc(E); return Z.validarTela("pagina6", E, HOJE) === "" && al(E).includes("A22") && c.pagina6Cobre === null && /ainda não fez/.test(Z.leituraPagina6(c, E)) && !al(E).includes("A23"); })());
t("Não fiz a página 6 não bloqueia o selo (critério 1)", (() => { const E = p6(Z.NAO_FIZ); return Z.criterio(E, calc(E), HOJE).itens[0].ok; })());
t("Não sei na página 6: tela passa, critério 1 cumprido, sem comparação", (() => { const E = p6(Z.NS); return Z.validarTela("pagina6", E, HOJE) === "" && Z.criterio(E, calc(E), HOJE).itens[0].ok && calc(E).pagina6Cobre === null; })());
t("página 6 em branco: critério 1 falha", !Z.criterio(p6(""), calc(p6("")), HOJE).itens[0].ok);
t("data da página 6 no futuro é recusada", Z.validarTela("pagina6", p6(1, { pagina6Data: "2026-11-28" }), HOJE) !== "" && Z.validarTela("pagina6", p6(1, { pagina6Data: HOJE }), HOJE) === "");
t("infraestrutura da página 6 negativa é recusada; vazia é «à parte»", Z.validarTela("pagina6", p6(1, { pagina6Infra: -5 }), HOJE) !== "" && Z.validarTela("pagina6", p6(1, { pagina6Infra: "" }), HOJE) === "");
t("limite6 Não sei: tela passa, A23, sem folga", (() => { const E = p6(300000, { limite6: Z.NS, pagina6ResultadoCons: 50000 }); const c = calc(E); return Z.validarTela("pagina6", E, HOJE) === "" && al(E).includes("A23") && c.folga6 === null && c.dentroLimite === null && /não diz se a conta cabe/.test(Z.leituraLimite(c)); })());
t("limite6 ausente sem resultado: A23", al(p6(300000, { limite6: "" })).includes("A23"));
t("limite6 ausente com resultado_cons: usa 8 × resultado", (() => { const E = p6(300000, { limite6: "", pagina6ResultadoCons: 50000 }); const c = calc(E); return c.limite6 === 400000 && perto(c.folga6, 62550, 1e-6) && !al(E).includes("A23"); })());
t("limite6 inválido é recusado na tela", Z.validarTela("pagina6", p6(1, { limite6: "abc" }), HOJE) !== "");
t("folga exatamente 0: dentro, sem A21", (() => { const E = p6(300000, { limite6: 337450 }); const c = calc(E); return c.folga6 === 0 && c.dentroLimite === true && !al(E).includes("A21"); })());
t("folga −0,01: A21 em terceiro lugar na prioridade e ação de ordem 1", (() => { const E = p6(300000, { limite6: 337449.99 }); const c = calc(E); const A = al(E); const s = Z.acaoSugerida(E, c); return c.dentroLimite === false && A[0] === "A21" && s.ordem === 1 && /três ajustes possíveis/.test(s.acao) && c.folgaEmSubtotal === null && /Passou do limite/.test(Z.leituraLimite(c)); })());
t("A21 não bloqueia o selo (critério não exige estar dentro)", (() => { const E = p6(300000, { limite6: 1, pdfBaixado: true }); return Z.criterio(E, calc(E), HOJE).ok; })());
t("giro Não sei: sem folga nem comparação", (() => { const E = base(); E.giro = Z.NS; const c = calc(E); return c.folga6 === null && c.pagina6Cobre === null && /Falta o giro/.test(Z.leituraLimite(c)) && /Falta o giro/.test(Z.leituraPagina6(c, E)); })());

/* ================= 5. Leituras de outras páginas (tolerantes) ================= */
const PAG6_MARINA = { versao: 1, pilar: 6, perfil: { nome: "Marina", cidade: "Cidade", uf: "SC" }, respostas: {}, resumo: { data: "2026-11-13", dados: { unidades: 3, soma_folha: 649741.8, infra: null, giro: 40787.38, giro_meses: 3, total: 690529.18, total_sem_giro: 649741.8, terreno: 600000, resultado_cons: 108766.35, inv8: 870130.8 } } };
const L6 = Z.lerPagina6(JSON.stringify(PAG6_MARINA));
t("lerPagina6: resumo.dados (texto JSON)", L6.total === 690529.18 && L6.limite === 870130.8 && L6.infra === null && L6.giro === 40787.38 && L6.giro_meses === 3 && L6.terreno === 600000 && L6.unidades === 3 && L6.data === "2026-11-13" && L6.temDados, L6);
t("lerPagina6: dados na raiz (objeto)", (() => { const x = Z.lerPagina6({ data: "2026-10-01", dados: { total: "500.000,00", resultado_cons: 40000 } }); return x.total === 500000 && x.limite === 320000 && x.inv8 === null && x.data === "2026-10-01"; })());
t("lerPagina6: JSON quebrado devolve null, sem erro", Z.lerPagina6("{quebrado") === null && Z.lerPagina6(null) === null && Z.lerPagina6("[]") === null && Z.lerPagina6("42") === null);
t("lerPagina6: sem números, temDados falso", Z.lerPagina6({ perfil: { nome: "X" } }).temDados === false && Z.lerPagina6({ resumo: { dados: "lixo" } }).total === null);
t("aplicarPagina6: preenche só o que está vazio e marca a origem", (() => { const E = Z.estadoInicial(HOJE); E.giro = "1000"; const v = Z.aplicarPagina6(E, L6, HOJE); return E.pagina6Total === "690.529,18" && E.limite6 === "870.130,80" && E.pagina6Infra === "" && E.unidadesFase === "3" && E.giro === "1000" && E.terrenoValor === "600.000" && E.pagina6GiroMeses === "3" && E.cidadeUF === "Cidade/SC" && v.pagina6Total === "página 6" && !v.giro && !v.pagina6Infra; })());
t("aplicarPagina6: não troca Não sei nem Não fiz", (() => { const E = Z.estadoInicial(HOJE); E.pagina6Total = Z.NAO_FIZ; E.limite6 = Z.NS; Z.aplicarPagina6(E, L6, HOJE); return E.pagina6Total === Z.NAO_FIZ && E.limite6 === Z.NS; })());
t("aplicarPagina6: data futura da página 6 não entra", (() => { const E = Z.estadoInicial(HOJE); Z.aplicarPagina6(E, Object.assign({}, L6, { data: "2026-12-01" }), HOJE); return E.pagina6Data === ""; })());
t("aplicarPagina6 com página 6 nula: nada muda", (() => { const E = Z.estadoInicial(HOJE); const v = Z.aplicarPagina6(E, null, HOJE); return Object.keys(v).length === 0 && E.pagina6Total === ""; })());
t("aplicarPagina6 + cálculo: a Marina sem o botão chega ao mesmo limite", (() => { const E = clone(EX); E.pagina6Total = ""; E.limite6 = ""; Z.aplicarPagina6(E, L6, HOJE); const c = calc(E); return perto(c.folga6, 38212.42, 1e-6) && Z.fmtPct(c.pagina6Cobre) === "83,0%"; })());
t("lerMarcoZero: situação com as palavras do Marco Zero", (() => { const m = Z.lerMarcoZero(JSON.stringify({ situacao: "opero", nome: "Ana" })); return m.situacao === "opero" && m.nome === "Ana"; })());
t("lerMarcoZero: situação desconhecida e JSON quebrado", Z.lerMarcoZero({ situacao: "outra" }).situacao === null && Z.lerMarcoZero("{x") === null);
t("migrar: respostas da versão 1 (blocos, contingência, situação antiga)", (() => { const r = Z.migrar({ blocos: { 1: [1] }, contingenciaPct: 12, situacao: "operador", d1: "palpite", d2: "soUnidade", d3: "algumas" }); return r.partes[1][0] === 1 && !r.blocos && r.reservaPct === 12 && r.contingenciaPct === undefined && r.situacao === "terreno" && r.paraOutro === true && r.d1 === "referencia" && r.d2 === "nenhuma" && r.d3 === "algumas"; })());
t("migrar: ampliar vira opero; estado novo fica igual", Z.migrar({ situacao: "ampliar" }).situacao === "opero" && JSON.stringify(Z.migrar(clone(EX))) === JSON.stringify(clone(EX)));

/* ================= 6. Bordas ================= */
const ET = base(); ET.partes[3][0].qtd = 3;
t("tipologias somando 3 com fase de 2: A17 primeiro", al(ET)[0] === "A17");
t("tipologias ≠ fase bloqueiam a tela da Parte 3", /somam 3/.test(Z.validarTela("p3", ET, HOJE)));
t("tipologias ≠ fase impedem o critério 2", !Z.criterio(ET, calc(ET), HOJE).itens[1].ok);
const ET2 = base(); ET2.partes[3].push(linha({ nome: "Tipo 2", tip: true, forma: "construida", campos: { qtd: 1, areaM2: 30, custoM2: 1000, origem: "estimativa" } })); ET2.partes[3][0].qtd = 1;
t("duas tipologias somando a fase passam", Z.validarTela("p3", ET2, HOJE) === "" && Z.tipologiasConferem(ET2));
const ET3 = base(); ET3.partes[3].push(...["T2", "T3", "T4"].map((n) => linha({ nome: n, tip: true, campos: { origem: "naoAplica" } })));
t("quatro tipologias são recusadas", /até 3/.test(Z.validarTela("p3", ET3, HOJE)));
const EZ = base(); EZ.unidadesFase = 0;
t("zero unidades: tela da fase recusa", Z.validarTela("fase", EZ, HOJE) !== "");
t("zero unidades: custo por unidade nulo e sem transposição", calc(EZ).custoPorUnidade === null && calc(EZ).transposicao === null);
t("zero unidades: critério 2 falha", !Z.criterio(EZ, calc(EZ), HOJE).itens[1].ok);
t("201 unidades: tela da fase recusa", (() => { const E = base(); E.unidadesFase = 201; return Z.validarTela("fase", E, HOJE) !== ""; })());
t("projeto completo menor que a fase é recusado", (() => { const E = base(); E.unidadesProjeto = 1; return Z.validarTela("fase", E, HOJE) !== ""; })());
const E0 = base(); for (let p = 1; p <= 6; p++) E0.partes[p].forEach((l) => (l.origem = "branco"));
const C0 = calc(E0);
t("CAPEX zero: pesos nulos", C0.capexFase === 0 && Object.values(C0.pctParte).every((x) => x === null));
t("CAPEX zero: degrau Sonhador", C0.degrau === "Sonhador");
t("CAPEX zero: A1 com as seis partes", (() => { const A = Z.alertas(E0, C0); ids(A); const a = A.find((x) => x.id === "A1"); return a && a.partes.length === 6; })());
t("CAPEX zero: ação de ordem 2 (parte em branco)", Z.acaoSugerida(E0, C0).ordem === 2 && /Listar as linhas da Parte 1/.test(Z.acaoSugerida(E0, C0).acao));
t("CAPEX zero: critério 4 falha", !Z.criterio(E0, C0, HOJE).itens[3].ok);
t("CAPEX zero: custo por m² = 0, faltaPreAbertura nula", C0.custoPorM2 === 0 && C0.faltaPreAbertura === null);
const E3 = base(); [1, 2, 4, 5, 6].forEach((p) => E3.partes[p].forEach((l) => (l.origem = "branco")));
t("só a Parte 3 com valor: Sonhador", calc(E3).degrau === "Sonhador");
const E4z = base(); E4z.partes[4][0].origem = "branco";
t("Parte 4 = 0: proporção do enxoval nula, sem A9", calc(E4z).oseSobreFFE === null && !al(E4z).includes("A9"));
t("Parte 4 em branco: A1 aponta a Parte 4", Z.alertas(E4z, calc(E4z)).find((a) => a.id === "A1").partes.join() === "4");
const EO = base(); EO.imovelPronto = true; EO.partes[2] = [na("Rede")]; EO.partes[3] = [na("Adequação")]; EO.reservaPct = 20;
const CO = calc(EO);
t("obra = 0: pré-abertura ÷ obra nula, sem A11", CO.obra === 0 && CO.preAberturaSobreObra === null && !al(EO).includes("A11"));
t("imóvel pronto: Partes 2 e 3 inteiras em não se aplica passam", Z.validarTela("p2", EO, HOJE) === "" && Z.validarTela("p3", EO, HOJE) === "");
t("imóvel pronto: critérios 3 e 6 cumpridos", (() => { const it = Z.criterio(EO, CO, HOJE).itens; return it[2].ok && it[5].ok; })());
t("sem imóvel pronto: Parte 2 inteira não se aplica é recusada", (() => { const E = base(); E.partes[2] = [na("Rede")]; return Z.validarTela("p2", E, HOJE) !== ""; })());
t("imóvel pronto: Parte 3 vira Adequação e reforma", Z.nomeParte(3, EO) === "Adequação e reforma" && Z.nomeParte(3, B) === "Unidades e áreas comuns");
const EA = base(); EA.partes[3][0] = linha({ nome: "Bolha", tip: true, forma: "pronta", campos: { qtd: 2, valorUnit: 50000, origem: "cotacao", nCotacoes: 3, mesmaEspec: true, freteMontagemConfirmados: true } });
t("tipologia sem área: área total e custo por m² nulos", calc(EA).areaTotal === null && calc(EA).custoPorM2 === null);
t("estrutura pronta vai para a FF&E da Planilha 1 e a identidade fecha", (() => { const c = calc(EA); return c.planilha1.ffe === 100000 + 100000 && c.planilha1.premissas === 0 && c.planilha1.confere; })());
EA.partes[3][0].areaM2 = Z.NS;
t("área Não sei: só afeta o custo por m²", calc(EA).custoPorM2 === null && calc(EA).totalParte[3] === 100000 && Z.validarTela("p3", EA, HOJE) === "");
EA.partes[3][0].freteMontagemConfirmados = false;
t("A15: estrutura pronta sem frete e montagem confirmados", al(EA).includes("A15"));
const res = (p, o = {}) => { const E = base(); E.reservaPct = p; Object.assign(E, o); return al(E); };
t("reserva 0: A3z e CAPEX = subtotal", res(0).includes("A3z") && (() => { const E = base(); E.reservaPct = 0; const c = calc(E); return c.capexFase === c.subtotal; })());
t("reserva vazia: A3z", res("").includes("A3z"));
t("reserva 0: critério 5 falha e a tela recusa", (() => { const E = base(); E.reservaPct = 0; return !Z.criterio(E, calc(E), HOJE).itens[4].ok && Z.validarTela("reserva", E, HOJE) !== ""; })());
t("reserva 9,99: A3", res(9.99).includes("A3"));
t("reserva 10: sem A3", !res(10).includes("A3") && res(10).length === 0);
t("reserva 10 com primeira obra: A4", res(10, { primeiraObra: true }).includes("A4"));
t("reserva 10 com fator de risco: A4", res(10, { fatoresRisco: ["remoto"] }).includes("A4"));
t("reserva 15 com primeira obra: sem A4", !res(15, { primeiraObra: true }).includes("A4"));
t("reserva 25: sem A5", !res(25).includes("A5"));
t("reserva 25,01: A5", res(25.01).includes("A5"));
t("reserva 50 aceita, 50,01 recusada na tela", (() => { const E = base(); E.reservaPct = 50; const a = Z.validarTela("reserva", E, HOJE) === ""; E.reservaPct = 50.01; return a && Z.validarTela("reserva", E, HOJE) !== ""; })());
t("imóvel pronto a 12%: A3 (régua de reforma 15%)", res(12, { imovelPronto: true }).includes("A3") && !res(15, { imovelPronto: true }).includes("A3"));
t("reserva = subtotal × % (base das Partes 1 a 6)", (() => { const E = base(); E.reservaPct = 12.5; const c = calc(E); return perto(c.reserva, c.subtotal * 0.125, 1e-9); })());
t("leituras da reserva: abaixo, dentro, acima com fator, acima de 25%", /Abaixo/.test(Z.leituraReserva({ reservaPct: 9 })) && /Dentro/.test(Z.leituraReserva({ reservaPct: 15 })) && /fator de risco/.test(Z.leituraReserva({ reservaPct: 20 })) && /Acima de 25%/.test(Z.leituraReserva({ reservaPct: 26 })) && /nunca é zero/.test(Z.leituraReserva({ reservaPct: "" })));
t("enxoval exatamente 10%: sem A9", !al(base({ p5: 10000 })).includes("A9"));
t("enxoval exatamente 15%: sem A9", !al(base({ p5: 15000 })).includes("A9"));
t("enxoval 9,999%: A9 (abaixo)", al(base({ p5: 9999 })).includes("A9") && /abaixo/.test(Z.alertas(base({ p5: 9999 })).find((a) => a.id === "A9").tit));
t("enxoval 15,001%: A9 (acima)", al(base({ p5: 15001 })).includes("A9") && /acima/.test(Z.alertas(base({ p5: 15001 })).find((a) => a.id === "A9").tit));
t("pré-abertura exatamente 5% da obra: sem A11", (() => { const E = base({ p6: 7500 }); return Z.div(calc(E).totalParte[6], calc(E).obra) === 0.05 && !al(E).includes("A11") && calc(E).faltaPreAbertura === 0; })());
t("pré-abertura 4,99%: A11", al(base({ p6: 7499 })).includes("A11"));
t("pré-abertura 0: A11 (inclui zero)", (() => { const E = base(); E.partes[6] = [bra("Pré-abertura")]; return al(E).includes("A11"); })());
t("obra exatamente 80%: sem A12", (() => { const E = base({ p2: 846000, p6: 7000 }); E.limite6 = 5000000; return calc(E).pctObra === 0.8 && !al(E).includes("A12"); })());
t("obra 80,01%: A12", (() => { const E = base({ p2: 847000, p6: 7000 }); E.limite6 = 5000000; return calc(E).pctObra > 0.8001 && al(E).includes("A12"); })());
t("cotação com 90 dias ainda vale", (() => { const E = base(); E.partes[1][0].dataCotacao = Z.somaDias(HOJE, -90); return calc(E).cotacoesVencidas === 0 && !al(E).includes("A13"); })());
t("cotação com 91 dias vence: A13", (() => { const E = base(); E.partes[1][0].dataCotacao = Z.somaDias(HOJE, -91); return calc(E).cotacoesVencidas === 1 && al(E).includes("A13"); })());
t("data antiga em linha estimada não conta como vencida", (() => { const E = base(); E.partes[1][0] = Object.assign(est("Projetos", 10000), { dataCotacao: "2025-01-01" }); return calc(E).cotacoesVencidas === 0; })());
function meioCotado(extraCot) {
  const E = base();
  E.partes[1] = [cot("A", 100000), est("e1", 1000)];
  E.partes[2] = [cot("B", 90000), est("e2", 1000)];
  E.partes[4] = [extraCot ? cot("e3", 1000) : est("e3", 1000)];
  E.partes[5] = []; E.partes[6] = [];
  return E; // linhas: A, e1, B, e2, tipologia (cotada), e3 → 3 de 6 = 50%
}
t("exatamente 50% das linhas cotadas: não é Calculista", (() => { const c = calc(meioCotado(false)); return c.pctLinhasCotadas === 0.5 && c.degrau === "Estimador" && c.faltamParaMaioria === 1; })());
t("mais de 50% e três maiores cotadas: Calculista", (() => { const c = calc(meioCotado(true)); return c.pctLinhasCotadas > 0.5 && c.degrau === "Calculista" && c.faltamParaMaioria === 0; })());
t("maioria cotada mas a maior linha estimada: Estimador", (() => { const E = meioCotado(true); E.partes[1][0].origem = "estimativa"; E.partes[1][1].origem = "cotacao"; E.partes[1][1].nCotacoes = 3; return calc(E).degrau === "Estimador"; })());
t("leituras das linhas cotadas: 0 / até 50% / mais de 50%", /mapa do que cotar/.test(Z.leituraLinhasCotadas(0)) && /maior parte/.test(Z.leituraLinhasCotadas(0.5)) && /maioria/.test(Z.leituraLinhasCotadas(0.5001)) && /Ainda não/.test(Z.leituraLinhasCotadas(null)));
t("diagnóstico: não fiz → Sonhador; cotação e maioria → Calculista; resto → Estimador", Z.degrauDiagnostico({ d1: "naoFiz" }) === "Sonhador" && Z.degrauDiagnostico({ d1: "cotacao", d3: "maioria" }) === "Calculista" && Z.degrauDiagnostico({ d1: "cotacao", d3: "algumas" }) === "Estimador" && Z.degrauDiagnostico({}) === null);
t("giro de 3 meses na calculadora: sem A16", (() => { const E = base(); E.giroMeses = 3; E.giroCustoMensal = 10000; return !al(E).includes("A16") && calc(E).giro === 30000; })());
t("giro de 2,9 meses: A16", (() => { const E = base(); E.giroMeses = "2,9"; E.giroCustoMensal = 10000; return al(E).includes("A16"); })());
t("giro 25 meses é recusado", (() => { const E = base(); E.giroMeses = 25; E.giroCustoMensal = 1; return Z.validarTela("giro", E, HOJE) !== ""; })());
t("giro zero para quem ainda não hospeda é recusado", (() => { const E = base(); E.giro = 0; return /maior que zero/.test(Z.validarTela("giro", E, HOJE)) && !Z.criterio(E, calc(E), HOJE).itens[6].ok; })());
t("giro zero para quem já opera, com justificativa: aceito", (() => { const E = base(); E.situacao = "opero"; E.giro = 0; E.giroZeroJustificativa = "O caixa separado da operação já cobre o giro."; return Z.validarTela("giro", E, HOJE) === "" && Z.criterio(E, calc(E), HOJE).itens[6].ok; })());
t("giro zero para quem faz para outra pessoa, com justificativa: aceito", (() => { const E = base(); E.paraOutro = true; E.giro = 0; E.giroZeroJustificativa = "O dono já tem o giro separado."; return Z.validarTela("giro", E, HOJE) === "" && Z.criterio(E, calc(E), HOJE).itens[6].ok; })());
t("giro zero para quem opera, sem justificativa: recusado", (() => { const E = base(); E.situacao = "opero"; E.giro = 0; return Z.validarTela("giro", E, HOJE) !== ""; })());
t("prazo em hoje + 30: válido", Z.prazoOk(Z.somaDias(HOJE, 30), HOJE));
t("prazo em hoje + 31: inválido", !Z.prazoOk(Z.somaDias(HOJE, 31), HOJE));
t("prazo ontem: inválido; hoje: válido", !Z.prazoOk(Z.somaDias(HOJE, -1), HOJE) && Z.prazoOk(HOJE, HOJE));
t("prazo inválido bloqueia a tela e o critério 9", (() => { const E = base(); E.prazo = Z.somaDias(HOJE, 31); return Z.validarTela("acao", E, HOJE) !== "" && !Z.criterio(E, calc(E), HOJE).itens[8].ok; })());
t("ação com 9 letras é recusada", (() => { const E = base(); E.acao30 = "123456789"; return Z.validarTela("acao", E, HOJE) !== ""; })());
t("verificação curta é recusada", (() => { const E = base(); E.verificacao = "curta"; return Z.validarTela("acao", E, HOJE) !== "" && !Z.criterio(E, calc(E), HOJE).itens[8].ok; })());

/* ================= 7. "Não sei" em cada campo que o aceita ================= */
const ns = (campo, v = Z.NS) => { const E = base(); E[campo] = v; return E; };
t("unidades do projeto Não sei: A7 e critério 2 falha", (() => { const E = ns("unidadesProjeto"); return Z.validarTela("fase", E, HOJE) === "" && al(E).includes("A7") && !Z.criterio(E, calc(E), HOJE).itens[1].ok; })());
t("rede Não sei: A7, ação de ordem 3 e critério 6 falha", (() => { const E = ns("infraDimensionadaPara"); return al(E).includes("A7") && Z.acaoSugerida(E).ordem === 3 && !Z.criterio(E, calc(E), HOJE).itens[5].ok; })());
t("distância da energia Não sei: A8", (() => { const E = ns("distanciaEnergiaM"); return Z.validarTela("p2", E, HOJE) === "" && al(E).includes("A8"); })());
t("distância 0 m é aceita, sem A8", (() => { const E = ns("distanciaEnergiaM", 0); return Z.validarTela("p2", E, HOJE) === "" && !al(E).includes("A8"); })());
t("reserva Não sei: tela passa, A3z e critério 5 falha", (() => { const E = ns("reservaPct"); return Z.validarTela("reserva", E, HOJE) === "" && al(E).includes("A3z") && !Z.criterio(E, calc(E), HOJE).itens[4].ok; })());
t("giro Não sei: investimento total nulo e critério 7 falha", (() => { const E = ns("giro"); return Z.validarTela("giro", E, HOJE) === "" && calc(E).investimentoTotal === null && !Z.criterio(E, calc(E), HOJE).itens[6].ok; })());
t("valor do terreno Não sei: terreno nulo, tela passa", (() => { const E = ns("terrenoValor"); return calc(E).terreno === null && Z.validarTela("giro", E, HOJE) === ""; })());
t("terreno sem situação bloqueia a tela e o critério 8", (() => { const E = ns("terrenoSituacao", null); return Z.validarTela("giro", E, HOJE) !== "" && !Z.criterio(E, calc(E), HOJE).itens[7].ok; })());
t("área Não sei na linha é aceita", Z.erroLinha(linha({ nome: "Sala", modo: "valor", campos: { valor: 10, areaM2: Z.NS, origem: "estimativa" } }), B, HOJE) === "");

/* ================= 8. Os outros alertas, um a um ================= */
t("A6: rede para 4 com projeto de 6", (() => { const E = base(); E.unidadesProjeto = 6; E.infraDimensionadaPara = 4; return al(E).includes("A6") && Z.acaoSugerida(E).ordem === 3 && /6 unidades/.test(Z.acaoSugerida(E).acao); })());
t("A6 não dispara com rede = projeto", (() => { const E = base(); E.unidadesProjeto = 6; E.infraDimensionadaPara = 6; return !al(E).includes("A6"); })());
t("A2: parte com valor e sem cotação", (() => { const E = base(); E.partes[1][0].origem = "estimativa"; const A = Z.alertas(E, calc(E)); ids(A); return A.find((a) => a.id === "A2").partes.join() === "1"; })());
t("A10: enxoval não confirmado", al(ns("enxovalNaoDuplicado", false)).includes("A10"));
t("A14: cotação com duas propostas", (() => { const E = base(); E.partes[1][0].nCotacoes = 2; return al(E).includes("A14") && calc(E).nCotacoesIncompletas === 1; })());
t("A14: três propostas sem a mesma especificação", (() => { const E = base(); E.partes[1][0].mesmaEspec = false; return al(E).includes("A14"); })());
t("A18: vou comprar o terreno", al(ns("terrenoSituacao", "comprar")).includes("A18"));
t("A19: quem já opera", al(ns("situacao", "opero")).includes("A19") && !al(ns("situacao", "ideia")).includes("A19"));
t("A20: regra de uso com menos de 10 letras", (() => { const E = ns("regraQuandoConfere", "sempre"); return al(E).includes("A20") && !Z.criterio(E, calc(E), HOJE).itens[4].ok; })());
t("A20 não bloqueia a tela da reserva (bloqueia o selo)", Z.validarTela("reserva", ns("regraQuandoConfere", ""), HOJE) === "");
t("regra com mais de 200 letras é recusada", Z.validarTela("reserva", ns("regraParaQue", "x".repeat(201)), HOJE) !== "");
t("ordem dos alertas segue a lista do plano", (() => { const E = base(); E.situacao = "opero"; E.terrenoSituacao = "comprar"; E.reservaPct = 5; E.primeiraObra = true; E.enxovalNaoDuplicado = false; E.distanciaEnergiaM = Z.NS; E.limite6 = ""; return al(E).join() === ["A8", "A3", "A4", "A10", "A23", "A18", "A19"].join(); })(), (() => { const E = base(); E.situacao = "opero"; E.terrenoSituacao = "comprar"; E.reservaPct = 5; E.primeiraObra = true; E.enxovalNaoDuplicado = false; E.distanciaEnergiaM = Z.NS; E.limite6 = ""; return al(E); })());
t("só três alertas na Atenção", (() => { const E = base(); E.situacao = "opero"; E.terrenoSituacao = "comprar"; E.reservaPct = 5; E.primeiraObra = true; return Z.tresPrimeiros(Z.alertas(E)).length === 3; })());
t("todo alerta traz título, texto e fonte", [EX, E0, ET, EA, ns("situacao", "opero"), p6(Z.NAO_FIZ)].every((E) => Z.alertas(E, calc(E)).every((a) => a.tit && a.txt && a.fonte)));

/* ================= 9. Ações de 30 dias (ordem 5 a 8) ================= */
const semCot = () => { const E = base(); E.partes[2][0].origem = "estimativa"; E.partes[4][0].origem = "estimativa"; E.partes[5][0].origem = "estimativa"; return E; };
t("ação 5: degrau abaixo de Calculista, sem brancos", (() => { const s = Z.acaoSugerida(semCot()); return s.ordem === 5 && /três maiores linhas: unidade tipo 1, móveis e rede/.test(s.acao); })(), Z.acaoSugerida(semCot()));
t("ação 6: Calculista com cotação incompleta", (() => { const E = base(); E.partes[1][0].nCotacoes = 2; return Z.acaoSugerida(E).ordem === 6; })());
t("ação 7: só faixa de conferência (enxoval)", (() => { const s = Z.acaoSugerida(base({ p5: 5000 })); return s.ordem === 7 && /Parte 4 · Mobiliário e equipamentos e Parte 5 · Enxoval/.test(s.acao); })());
t("ação 8: nada disparou, refazer a página 6 e Planilha 2 B5", (() => { const s = Z.acaoSugerida(base()); return s.ordem === 8 && /Refazer a página 6/.test(s.acao) && /B5/.test(s.acao); })());
t("ação 8 para quem faz para outra pessoa fala do dono", /ao dono/.test(Z.acaoSugerida(ns("paraOutro", true)).acao));
t("próxima etapa muda com a turma e com o dono", /encontro do Pilar 6/.test(Z.proximaEtapa({ turma: "acompanhamento" })) && /Planilha 1 ou a Planilha 2/.test(Z.proximaEtapa({ turma: "autonomo" })) && /Meu Dossiê/.test(Z.proximaEtapa({})) && /ao dono/.test(Z.proximaEtapa({ paraOutro: true })));
t("próximos passos na ordem do Mapa: Meu Dossiê, página 6, Planilha 1, Planilha 2 (B5, B6, B9), sensibilidade, Pilar 7", Z.PROXIMOS.length === 6 && /Meu Dossiê/.test(Z.PROXIMOS[0]) && /página 6/.test(Z.PROXIMOS[1]) && /Planilha 1/.test(Z.PROXIMOS[2]) && /B5.*B6.*B9/.test(Z.PROXIMOS[3]) && /CAPEX \+20%/.test(Z.PROXIMOS[4]) && /Dias 61 a 90/.test(Z.PROXIMOS[5]));
t("nenhum próximo passo cita Ferramenta 05 nem Calculadora de Implantação", Z.PROXIMOS.concat(Object.values(Z.TEXTOS)).every((x) => !/Ferramenta 05|Calculadora de Implanta/.test(x)));
t("toda verificação sugerida está na lista (ou é a das propostas)", [EX, base(), E0, ns("infraDimensionadaPara"), base({ p5: 5000 }), semCot(), p6(1, { limite6: 1 })].every((E) => { const v = Z.acaoSugerida(E).verificacao; return Z.VERIFICACOES.includes(v) || /propostas?, com data e escopo, lançadas? na ficha/.test(v); }));
t("uma linha em branco: verificação no singular", (() => { const E = base(); E.partes[1].push(bra("Licença")); return Z.acaoSugerida(E).verificacao === "A proposta, com data e escopo, lançada na ficha."; })());

/* ================= 10. As duas identidades em estados sorteados ================= */
let semente = 7; const rnd = () => ((semente = (semente * 16807) % 2147483647) / 2147483647);
let fechaT = true, fechaP = true;
for (let k = 0; k < 300; k++) {
  const E = base({ p2: Math.round(rnd() * 400000) + 1, p4: Math.round(rnd() * 200000) + 1, p5: Math.round(rnd() * 30000) + 1, p6: Math.round(rnd() * 50000) + 1 });
  E.unidadesFase = 1 + Math.floor(rnd() * 9); E.unidadesProjeto = E.unidadesFase; E.partes[3][0].qtd = E.unidadesFase;
  if (rnd() < 0.3) Object.assign(E.partes[3][0], { forma: "pronta", modo: "qtdUnit", valorUnit: Math.round(rnd() * 90000) + 1 });
  E.reservaPct = Math.round(rnd() * 5000) / 100 || 1;
  E.partes[2].push(linha({ nome: "Luz", modo: "qtdUnit", pu: true, tag: "luz", campos: { valorUnit: Math.round(rnd() * 9000) + 1, origem: "estimativa" } }));
  E.partes[3].push(linha({ nome: "Deck", modo: "qtdUnit", pu: true, tag: "deck", campos: { valorUnit: Math.round(rnd() * 9000) + 1, origem: "cotacao", nCotacoes: 2 } }));
  E.partes[3].push(linha({ nome: "Piso", modo: "qtdUnit", pu: true, tag: "piso", campos: { valorUnit: Math.round(rnd() * 900) + 1, origem: "estimativa" } }));
  E.partes[3].push(linha({ nome: "Apoio", modo: "area", comum: true, campos: { qtd: 1, areaM2: 20, custoM2: Math.round(rnd() * 3000) + 1, origem: "estimativa" } }));
  E.partes[4].push(linha({ nome: "Equipamentos gerais", geral: true, campos: { valor: Math.round(rnd() * 9000) + 1, origem: "estimativa" } }));
  E.partes[2].push(linha({ nome: "Mobília fora do lugar", tag: "mobilia", campos: { valor: Math.round(rnd() * 900) + 1, origem: "estimativa" } }));
  const c = calc(E);
  if (!c.transposicao.confere) fechaT = false;
  if (!c.planilha1.confere) fechaP = false;
}
t("transposição fecha com o CAPEX em 300 estados sorteados (R$ 0,01)", fechaT);
t("Planilha 1 fecha com o subtotal e o CAPEX em 300 estados sorteados", fechaP);

/* ================= 11. Integridade dos dados e varredura de textos ================= */
t("24 alertas na lista de prioridade, sem repetição", Z.ORDEM_ALERTAS.length === 24 && new Set(Z.ORDEM_ALERTAS).size === 24);
t("sete partes, a 7 é a reserva; nomes do plano", Z.PARTES.length === 7 && Z.PARTES[6].nome === "Reserva do imprevisto" && Z.PARTES[0].nome === "Projetos, licenças e documentação");
t("situações com as palavras exatas do Marco Zero", Z.SITUACOES.map((s) => s.r).join("|") === "Tenho um terreno e ainda não hospedo ninguém|Tenho uma ideia, ou o capital, e ainda não tenho o terreno|Já opero uma hospedagem e quero crescer" && Z.SITUACOES.map((s) => s.v).join() === "terreno,ideia,opero");
t("quatro perguntas de diagnóstico sobre a página 6", Z.DIAG.length === 4 && Z.DIAG.every((d) => d.op.length >= 2) && /página 6/.test(Z.DIAG[0].p) && Z.DIAG[0].op.some((o) => o.v === "naoFiz"));
t("cinco fatores de risco", Z.FATORES.length === 5);
t("telas: abertura, página 6, fase, Partes 1 a 6, reserva, giro, resultado, ação", Z.TELAS.join() === "abertura,pagina6,fase,p1,p2,p3,p4,p5,p6,reserva,giro,resultado,acao");
t("ajuda para as 10 telas de pergunta, com por que, onde e a Marina", ["pagina6", "fase", "p1", "p2", "p3", "p4", "p5", "p6", "reserva", "giro"].every((k) => Z.AJUDA[k] && Z.AJUDA[k].porque && Z.AJUDA[k].onde && Z.AJUDA[k].exemplo && Z.AJUDA[k].explica));
t("caixas da Marina batem com o caso (36.000, 128.200, 428.400, 72.000, 10.740, 12.600, 103.191)", ["36.000", "128.200", "428.400", "72.000", "10.740", "12.600", "103.191"].every((n, i) => Z.AJUDA[["p1", "p2", "p3", "p4", "p5", "p6", "reserva"][i]].exemplo.includes("R$ " + n)));
t("quadro partes → abas da Planilha 1: 10 linhas, pré-abertura sem aba própria, reserva em B15", Z.PL1_MAPA.length === 10 && /Sem aba própria/.test(Z.PL1_MAPA.find((x) => /Pré-abertura/.test(x.parte)).aba) && /B15/.test(Z.PL1_MAPA[9].aba));
const sugeridas = [];
for (const sit of ["terreno", "opero"]) for (const ip of [false, true]) for (const tp of ["cabanas", "glamping"]) for (let p = 1; p <= 6; p++) Z.linhasSugeridas(p, { situacao: sit, imovelPronto: ip, tipo: tp }).forEach((l) => sugeridas.push({ p, l }));
t("linhas sugeridas vêm só com o nome, nunca com valor", sugeridas.length > 0 && sugeridas.every(({ l }) => l.nome && !l.valor && !l.valorUnit && !l.custoM2 && !l.areaM2 && !l.qtd && !l.origem && !l.custoJogo));
t("Parte 2 de quem já opera sugere reforço da rede existente", Z.linhasSugeridas(2, { situacao: "opero" })[0].nome === "Reforço da rede existente" && !Z.linhasSugeridas(2, { situacao: "terreno" }).some((l) => /Reforço/.test(l.nome)));
t("Parte 3 sugere uma tipologia com etiqueta unidade (pronta no glamping)", Z.linhasSugeridas(3, {}).filter((l) => l.tipologia && l.tagP6 === "unidade").length === 1 && Z.linhasSugeridas(3, { tipo: "glamping" })[0].forma === "pronta");
t("Parte 5 traz a linha especial do enxoval", Z.linhasSugeridas(5, {}).some((l) => l.enxoval));
t("linhas sugeridas: até 15 por parte e nome de 2 a 80 letras", sugeridas.every(({ l }) => l.nome.length >= 2 && l.nome.length <= 80) && [1, 2, 3, 4, 5, 6].every((p) => Z.linhasSugeridas(p, { situacao: "opero" }).length <= 15));
t("linhas da Marina com nome de 2 a 80 letras", Object.values(EX.partes).flat().every((l) => l.nome.length >= 2 && l.nome.length <= 80));
t("estado inicial sem nenhum valor de referência", (() => { const E = Z.estadoInicial(HOJE); return ["pagina6Total", "limite6", "unidadesFase", "reservaPct", "giro", "terrenoValor", "acao30"].every((k) => E[k] === "") && E.partes && !E.blocos; })());
t("notas da página 6: cotação 3, estimativa 1, em branco Não sei", Z.notaP6("cotacao") === 3 && Z.notaP6("estimativa") === 1 && Z.notaP6("branco") === Z.NS && Z.notaP6("naoAplica") === null);
const textos = [];
Object.values(Z.TEXTOS).forEach((x) => textos.push(x));
Z.REGUA.forEach((x) => textos.push(x.t)); Object.values(Z.AJUDA).forEach((a) => Object.values(a).forEach((x) => textos.push(x))); Z.VERIFICACOES.forEach((x) => textos.push(x)); Z.PROXIMOS.forEach((x) => textos.push(x));
Z.DIAG.forEach((d) => { textos.push(d.p); d.op.forEach((o) => textos.push(o.r)); }); Z.SITUACOES.forEach((s) => textos.push(s.r));
Object.values(Z.INFO).forEach((x) => (Array.isArray(x) ? x.forEach((y) => textos.push(y)) : textos.push(x)));
[EX, E2, E4, E0, ET, EO, EA, base(), ns("situacao", "opero"), ns("terrenoSituacao", "comprar"), base({ p5: 5000 }), base({ p2: 847000, p6: 7000 }), p6(Z.NAO_FIZ), p6(1, { limite6: 1 }), p6(1, { limite6: Z.NS })].forEach((E) => {
  const c = calc(E); Z.alertas(E, c).forEach((a) => textos.push(a.tit, a.txt)); const s = Z.acaoSugerida(E, c); textos.push(s.acao, s.verificacao, Z.leituraDegrau(c), Z.leituraReserva(E), Z.leituraPagina6(c, E), Z.leituraLimite(c), Z.proximaEtapa(E));
});
sugeridas.forEach(({ l }) => textos.push(l.nome)); Object.values(EX.partes).flat().forEach((l) => textos.push(l.nome));
t("varredura: nenhuma promessa proibida nem palavra fora do curso (" + textos.length + " textos)", textos.every(Z.textoSeguro), textos.filter((x) => !Z.textoSeguro(x)));
t("varredura: a própria varredura pega 'retorno garantido', 'payback', 'Bloco 3' e 'aluno'", !Z.textoSeguro("Retorno garantido em 12 meses") && !Z.textoSeguro("payback") && !Z.textoSeguro("Bloco 3 · Unidades") && !Z.textoSeguro("o aluno"));
t("varredura: sem Helena, Chalés do Ribeirão, palpite, Rodrigo e Priscila", textos.every((x) => !/Helena|Ribeir|palpite|Rodrigo|Priscila/i.test(x)));
t("varredura: nenhum preço da Zion Glamping Store (129.000, 192.346, 40%)", textos.every((x) => !/129\.000|192\.346|25\.915|Glamping Store|margem de 40/.test(x)));
t("varredura: FF&E e OS&E só como nome de aba da Planilha 1", textos.every((x) => !/FF&E|OS&E/.test(x)) && Z.PL1_MAPA.some((x) => /FF&E/.test(x.aba)));
t("varredura: sem travessão nos textos", textos.every((x) => !/[—–]/.test(x)));
t("aviso educativo do plano, com «A Zion avalia cada caso.»", /^Material educativo\./.test(Z.TEXTOS.aviso) && /engenheiro, arquiteto, prefeitura e contador/.test(Z.TEXTOS.aviso) && /A Zion avalia cada caso\.$/.test(Z.TEXTOS.aviso));
t("«Esta ficha não envia nada» e o lembrete da pasta Meu Dossiê", Z.TEXTOS.naoEnvia === "Esta ficha não envia nada: o PDF fica só com você." && Z.TEXTOS.dossie === "Salve o PDF da página 6A na pasta Meu Dossiê, ao lado da página 6.");
t("título «Faça agora · O seu CAPEX» e página «Página 6A · CAPEX»", Z.TEXTOS.tituloCompleto === "Faça agora · O seu CAPEX" && Z.TEXTOS.pagina === "Página 6A · CAPEX");
t("promessa no formato 'Aprenda o passo a passo'", /^Aprenda o passo a passo/.test(Z.TEXTOS.promessa));
t("CAPEX explicado como no Pilar 6", /^O nome técnico é CAPEX, do inglês capital expenditure/.test(Z.TEXTOS.capex));
t("formatação pt-BR (brl, fmtPct, empate para o par, extenso)", Z.brl(791131) === "R$ 791.131,00" && Z.fmtPct(0.13043478) === "13,0%" && Z.arred(0.125, 2) === 0.12 && Z.paraNumero("831.918,38") === 831918.38 && Z.extenso(5) === "cinco" && Z.extenso(12) === "12");

/* ================= 12. A página pública usa esta mesma lógica ================= */
const PUB = path.resolve(__dirname, "../../../../docs/trilha1/pilar6a");
t("a pasta antiga docs/trilha1/capex não existe mais", !fs.existsSync(path.resolve(__dirname, "../../../../docs/trilha1/capex/index.html")));
if (fs.existsSync(path.join(PUB, "index.html"))) {
  const html = fs.readFileSync(path.join(PUB, "index.html"), "utf8");
  const semScript = html.replace(/<script[\s\S]*?<\/script>/g, "");
  t("cópia pública de logic.js idêntica à de src/", fs.readFileSync(path.join(PUB, "logic.js"), "utf8") === fs.readFileSync(path.resolve(__dirname, "../src/logic.js"), "utf8"));
  t("a página carrega logic.js", /<script src="logic\.js"><\/script>/.test(html));
  t("a página não envia dados (sem fetch, XMLHttpRequest, sendBeacon, FEEDBACK_URL)", !/fetch\(|XMLHttpRequest|sendBeacon|FEEDBACK_URL|webhook/i.test(html));
  t("a página usa o jsPDF 2.5.1 do cdnjs, como o Pilar 6", /cdnjs\.cloudflare\.com\/ajax\/libs\/jspdf\/2\.5\.1\/jspdf\.umd\.min\.js/.test(html));
  t("a página salva na chave zion-t1-pilar6a com try/catch", /zion-t1-pilar6a/.test(html) && /try\s*\{\s*window\.localStorage\.setItem/.test(html));
  t("a página lê zion-t1-pilar6 e zion-t1-marco-zero", /zion-t1-pilar6"/.test(html) && /zion-t1-marco-zero/.test(html));
  t("título da página: Faça agora · O seu CAPEX", /<title>Faça agora · O seu CAPEX<\/title>/.test(html));
  t("identidade da ficha do Pilar 6 (Playfair Display, Inter, #16261C, #E0BE5E)", /Playfair\+Display/.test(html) && /Inter/.test(html) && /#16261C/.test(html) && /#E0BE5E/.test(html));
  t("a página não tem mentor virtual", !/mentor/i.test(html));
  t("varredura da página: nenhuma promessa proibida nem «Bloco N»", Z.textoSeguro(semScript) && !/Helena|Ribeir|O meu CAPEX/.test(html));
} else t("página pública docs/trilha1/pilar6a/index.html existe", false);

/* ================= 13. Todos os 24 alertas foram disparados em algum teste ================= */
const faltando = Z.ORDEM_ALERTAS.filter((x) => !disparados.has(x));
t("os 24 alertas foram disparados ao menos uma vez", faltando.length === 0, faltando);

console.log(`\n${ok} testes aprovados, ${fal} falharam (lógica do CAPEX, página 6A).`);
process.exit(fal ? 1 : 0);

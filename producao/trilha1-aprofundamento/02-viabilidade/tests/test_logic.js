// Testes da lógica da ficha "Faça agora · A sua conta" (página 6B · Viabilidade), PLANO.md seções 6, 7 e 13.
// Escritos antes da interface. Uso: node producao/trilha1-aprofundamento/02-viabilidade/tests/test_logic.js
"use strict";
const fs = require("fs"), path = require("path");
const Z = require("../src/logic.js");
const HOJE = "2026-11-28";
let ok = 0, fal = 0;
const disparados = new Set();
function t(nome, cond, extra) { if (cond) ok++; else { fal++; console.log("  FALHOU  " + nome + (extra !== undefined ? "  -> " + JSON.stringify(extra) : "")); } }
const perto = (a, b, tol = 0.005) => typeof a === "number" && Math.abs(a - b) <= tol;
const ids = (L) => { L.forEach((a) => disparados.add(a.id)); return L.map((a) => a.id); };
const clone = (x) => JSON.parse(JSON.stringify(x));
const calc = (E) => Z.calcular(E, HOJE);
const al = (E) => ids(Z.alertas(E, calc(E)));
const brl = Z.brl;

/* ================= 1. O caso da Marina (PLANO seção 7), campo a campo ================= */
const EX = Z.exemplo(HOJE);
const EX_ANTES = JSON.stringify(EX);
const C = calc(EX), A = C.A, c = A.cons, b = A.base, o = A.otim;
t("Marina: a conta está completa", C.pronto === true, C.faltas);
t("Marina: rótulo «Exemplo ilustrativo · dados fictícios»", Z.TEXTOS.exemplo === "Exemplo ilustrativo · dados fictícios. Não são preços de referência." && EX.exemplo === true);
t("Marina: imposto de 6% como resposta fictícia do contador dela, com data de 20/11/2026", EX.imposto === "6" && EX.impostoData === "2026-11-20" && /fictícia/.test(EX.impostoQuem) && Z.impostoValido(EX) && Z.TEXTOS.contador === "Resposta fictícia do contador dela, para o caso dela; não vale para você.");
t("Marina: parte da 6A (CAPEX 791.131, giro 40.787,38), 3 cabanas, terreno 600.000, margem 6 de 40% como referência", Z.paraNumero(EX.capex) === 791131 && Z.paraNumero(EX.giro6A) === 40787.38 && EX.unidades === "3" && Z.paraNumero(EX.terreno) === 600000 && EX.margem6 === "40" && /referência da Zion/.test(EX.margem6Origem) && EX.origemCapex === "6A");
t("Marina: calendário jun a ago alta, set/out e abr/mai médios, nov a mar fracos; abre em junho; estadia de 2 noites", EX.calendario.join(",") === "fraco,fraco,fraco,medio,medio,alta,alta,alta,medio,medio,fraco,fraco" && EX.mesAbertura === "6" && EX.estadiaMedia === "2");
t("Marina: ocupação do ano = (3 × 64 + 4 × 40 + 5 × 22) ÷ 12 = 38,5%", perto(Z.ocupConsDe(EX), 38.5, 1e-9));
t("Marina: noites vendidas 421,575 / 547,5 / 711,75", perto(c.N, 421.575, 1e-9) && perto(b.N, 547.5, 1e-9) && perto(o.N, 711.75, 1e-9));
t("Marina: estadias 210,79 / 273,75 / 355,88", brl(c.estadias) === "R$ 210,79" && brl(b.estadias) === "R$ 273,75" && brl(o.estadias) === "R$ 355,88");
const T73 = [ // [campo, conservador, base, otimista] (PLANO 7.3)
  ["bruta", 271915.88, 353137.50, 459078.75], ["imposto", 16314.95, 21188.25, 27544.73], ["comissao", 24472.43, 31782.38, 41317.09], ["cartao", 3262.99, 4237.65, 5508.95],
  ["cancelamento", 5438.32, 7062.75, 9181.58], ["deducoes", 49488.69, 64271.03, 83552.33], ["real", 222427.19, 288866.48, 375526.42], ["vPct", 2719.16, 3531.38, 4590.79], ["variaveis", 43822.72, 56912.63, 73986.41], ["contrib", 178604.46, 231953.85, 301540.01],
  ["fixoAno", 112627.20, 112627.20, 112627.20], ["antes", 65977.26, 119326.65, 188912.81], ["modelo", 0, 0, 0], ["reserva", 8157.48, 10594.13, 13772.36], ["sobra", 57819.79, 108732.53, 175140.44],
];
for (const [k, vc, vb, vo] of T73) t(`Marina 7.3: ${k} = ${vc} / ${vb} / ${vo}`, Z.arred(c[k], 2) === Z.arred(vc, 2) && Z.arred(b[k], 2) === Z.arred(vb, 2) && Z.arred(o[k], 2) === Z.arred(vo, 2), [c[k], b[k], o[k]]);
t("Marina 7.3: lavanderia 14.755,13 / 19.162,50 / 24.911,25 e amenidades 9.485,44 / 12.318,75 / 16.014,38", [c, b, o].map((x) => brl(70 * x.estadias) + "|" + brl(45 * x.estadias)).join(" ") === "R$ 14.755,13|R$ 9.485,44 R$ 19.162,50|R$ 12.318,75 R$ 24.911,25|R$ 16.014,38");
t("Marina 7.3: energia 11.804,10 / 15.330,00 / 19.929,00 e limpeza 5.058,90 / 6.570,00 / 8.541,00", [c, b, o].map((x) => brl(28 * x.N) + "|" + brl(12 * x.N)).join(" ") === "R$ 11.804,10|R$ 5.058,90 R$ 15.330,00|R$ 6.570,00 R$ 19.929,00|R$ 8.541,00");
t("Marina: margem 21,3% (atenção) / 30,8% / 38,2%", Z.fmtPct(c.margem) === "21,3%" && Z.fmtPct(b.margem) === "30,8%" && Z.fmtPct(o.margem) === "38,2%" && Z.leituraMargem(c.margem).faixa === "atencao");
t("Marina: por mês, em média, 4.818,32 / 9.061,04 / 14.595,04", brl(c.sobra / 12) === "R$ 4.818,32" && brl(b.sobra / 12) === "R$ 9.061,04" && brl(o.sobra / 12) === "R$ 14.595,04");
t("Marina: fixo do mês 9.385,60 (8.000 + retirada 8 × 40 × 4,33 = 1.385,60), duodécimos do seguro e das taxas", perto(C.P.fixoMes, 9385.6, 1e-9) && perto(C.P.retirada, 1385.6, 1e-9) && perto(C.P.fixoLinhas, 8000, 1e-9));
t("Marina: o que fica de cada noite = 645 × 0,778 − 97,50 = 404,31", perto(A.cNoite, 404.31, 1e-9) && perto(C.planilha2.porNoite, 404.31, 1e-9));
t("Marina: conferência pelo caminho da noite (421,575 × 404,31 − 112.627,20 = 57.819,79)", perto(421.575 * 404.31 - 112627.2, c.sobra, 1e-6));
t("Marina: diferença com a página 6: 271.915,88 × 40% = 108.766,35", brl(C.resultado6) === "R$ 108.766,35" && Z.fmtNum(C.difPontos * 100, 1) === "18,7");
t("Marina: pesos 18,2 / 16,1 / 41,4 / 3,0 (soma 78,7; sobra 21,3)", [C.pesos.deducoes, C.pesos.variaveis, C.pesos.fixos, C.pesos.reserva].map((x) => Z.fmtPct(x)).join(" ") === "18,2% 16,1% 41,4% 3,0%");
t("Marina: as quatro saídas somam 214.096,09", brl(c.deducoes + c.variaveis + c.fixoAno + c.reserva) === "R$ 214.096,09");
// 7.4
t("Marina 7.4: equilíbrio 278,57 noites = 25,4%, folga 13,1 pontos, com folga", Z.fmtNum(A.Neq, 2) === "278,57" && Z.fmtPct(A.ocupEq) === "25,4%" && Z.fmtNum(A.folga * 100, 1) === "13,1" && Z.leituraEquilibrio(A).faixa === "folga");
t("Marina 7.4: custo por diária vendida R$ 507,85", brl(A.custoPorDiaria) === "R$ 507,85");
t("Marina 7.4: cada R$ 1 de diária vale R$ 327,99 por ano; diária de equilíbrio R$ 468,71", brl(A.efeito1) === "R$ 327,99" && brl(A.diariaEq) === "R$ 468,71");
t("Marina 7.4: piso que ainda paga a noite R$ 125,32", brl(A.piso) === "R$ 125,32");
// 7.5 mês a mês
const M75 = [[6, 59.08, 59.08], [7, 59.08, 118.16], [8, 59.08, 177.24], [9, -2006.94, -1829.70], [10, -2006.94, -3836.64], [11, -5327.34, -9163.98], [12, -3298.21, -12462.19], [1, -3298.21, -15760.39], [2, -3298.21, -19058.60], [3, -3298.21, -22356.81], [4, 1682.39, -20674.42], [5, 1682.39, -18992.04]];
t("Marina 7.5: os 12 meses do primeiro ano (mês, resultado e acumulado)", M75.every(([m, r, ac], i) => A.meses[i].mes === m && brl(A.meses[i].res) === brl(r) && brl(A.meses[i].acum) === brl(ac)), A.meses.slice(0, 12).map((x) => [x.mes, Z.arred(x.res, 2), Z.arred(x.acum, 2)]));
t("Marina 7.5: noites do mês 23,36 / 18,25 / 10,04 / 15,06 / 27,38 e contribuição 9.444,68 / 7.378,66 / 4.058,26 / 6.087,39 / 11.067,99", [0, 3, 5, 6, 10].map((i) => Z.fmtNum(A.meses[i].noites, 2) + "|" + brl(A.meses[i].contrib)).join(" ") === "23,36|R$ 9.444,68 18,25|R$ 7.378,66 10,04|R$ 4.058,26 15,06|R$ 6.087,39 27,38|R$ 11.067,99");
t("Marina 7.5: menor saldo −22.356,81 em março (mês 10)", brl(A.menorAcum) === "-R$ 22.356,81" && A.menorMes === 10 && A.meses[9].nome === "mar");
const ano1 = A.meses.slice(0, 12);
t("Marina 7.5: ano 1 com 231,59 noites, contribuição 93.635,16 e resultado −18.992,04", Z.fmtNum(ano1.reduce((s, x) => s + x.noites, 0), 2) === "231,59" && brl(ano1.reduce((s, x) => s + x.contrib, 0)) === "R$ 93.635,16" && brl(A.ano1.cons) === "-R$ 18.992,04");
t("Marina 7.5: r = 253,8 ÷ 462 = 0,549351 e as duas contas do ano 1 batem", perto(A.r, 253.8 / 462, 1e-12) && Z.fmtNum(A.r, 6) === "0,549351" && perto(A.ano1Resultado, A.ano1.cons, 1e-6));
const reg = A.regime;
t("Marina 7.5: ano em regime: alta +14.226,10, médio +5.371,72, fraco −1.269,08", brl(reg.find((x) => x.mes === 7).res) === "R$ 14.226,10" && brl(reg.find((x) => x.mes === 9).res) === "R$ 5.371,72" && brl(reg.find((x) => x.mes === 1).res) === "-R$ 1.269,08");
t("identidade: a soma dos 12 meses do ano em regime = o que sobra no conservador", perto(A.somaRegime, c.sobra, 1e-6));
t("Marina 7.5: do mês 13 ao 36 o acumulado não volta abaixo de −22.356,81 e passa de R$ 28 mil nos fracos do segundo ano", A.meses.slice(12).every((x) => x.acum >= A.menorAcum - 1e-6) && A.meses.slice(12, 24).filter((x) => x.tipo === "fraco").every((x) => x.acum > 28000));
t("Marina 7.5: reserva de sazonalidade 6.345,38 ÷ 3 = 2.115,13 por mês de alta", brl(A.deficitVale) === "R$ 6.345,38" && brl(A.porMesAlta) === "R$ 2.115,13");
// 7.6
t("Marina 7.6: conta A 53.524,02; conta B 50.513,61; giro da 6B 53.524,02", brl(A.giroA) === "R$ 53.524,02" && brl(A.giroB) === "R$ 50.513,61" && brl(A.giroMinimo) === "R$ 53.524,02" && A.giro6BOk);
t("Marina 7.6: investimento refeito 844.655,02 (diferença de 12.736,64 da 6A)", brl(A.investimento) === "R$ 844.655,02" && brl(A.investimento - 831918.38) === "R$ 12.736,64");
t("Marina 7.6: colchão 31.167,21 = 3,9% do CAPEX; giro que daria 10%: 101.469,91", brl(A.colchao) === "R$ 31.167,21" && Z.fmtPct(A.colchaoPct) === "3,9%" && brl(A.giro10) === "R$ 101.469,91");
t("Marina 7.6: fôlego de 5,7 meses de fixo", Z.fmtNum(A.folego, 1) === "5,7");
// 7.7
t("Marina 7.7: retorno simples 7,3% ao ano; com o terreno, 4,2%", Z.fmtPct(A.retorno) === "7,3%" && Z.fmtPct(A.retornoTerreno) === "4,2%");
t("Marina 7.7: tempo de volta em escada 15,0 anos (15,01)", Z.fmtVolta(A.volta.cons) === "15,0 anos" && Z.fmtNum(A.volta.cons, 2) === "15,01");
t("Marina 7.7: conferência da escada: fim do ano 15 = −646,00", brl(A.ano1.cons - 791131 + 14 * c.sobra) === "-R$ 646,00");
t("Marina 7.7: como o Pilar 6 calcula, 14,6 anos; com o terreno, 25,4 anos", Z.fmtVolta(A.voltaP6.cons) === "14,6 anos" && Z.fmtVolta(A.voltaTerreno) === "25,4 anos");
t("Marina 7.7: base ano 1 +8.976,91 e 8,2 anos; otimista +45.458,14 e 5,3 anos; Pilar 6: 7,8 e 4,8", brl(A.ano1.base) === "R$ 8.976,91" && Z.fmtVolta(A.volta.base) === "8,2 anos" && brl(A.ano1.otim) === "R$ 45.458,14" && Z.fmtVolta(A.volta.otim) === "5,3 anos" && Z.fmtVolta(A.voltaP6.base) === "7,8 anos" && Z.fmtVolta(A.voltaP6.otim) === "4,8 anos");
t("Marina 7.7: soma simples dos dez anos 501.386,06 < CAPEX: negativo a qualquer taxa (passo 4 decidido sem taxa)", brl(A.somaSimples) === "R$ 501.386,06" && A.p4.status === "redesenhar" && A.p4.decidido && A.p4.motivo === "somaSimples");
const saidaM = 6 * c.depoisModelo;
t("Marina 7.7: venda pela referência da régua 6 × 65.977,26 = 395.863,59; soma com ela 897.249,65", brl(saidaM) === "R$ 395.863,59" && brl(Z.arred(A.somaSimples, 2) + Z.arred(saidaM, 2)) === "R$ 897.249,65");
t("Marina 7.7: com a venda, o valor presente vira negativo em cerca de 1,6% ao ano", Z.fmtPct(Z.taxaVirada(A.fluxos, 791131, saidaM)) === "1,6%");
t("Marina 7.7: valor presente com a venda a 1% (+38.816,74) e a 2% (−22.319,65), tolerância de R$ 0,15 (o plano arredondou à mão)", perto(Z.vp(A.fluxos, 791131, 0.01, saidaM), 38816.74, 0.15) && perto(Z.vp(A.fluxos, 791131, 0.02, saidaM), -22319.65, 0.15));
// 7.8
t("Marina 7.8: teste de queda (R$ 580,50; 30,8%): 354,13 por noite, 337,26 noites, +6.806,35, passa", brl(A.queda.diaria) === "R$ 580,50" && Z.fmtPct(A.queda.ocup) === "30,8%" && Z.fmtNum(A.queda.N, 2) === "337,26" && brl(A.sobraQueda) === "R$ 6.806,35");
t("Marina 7.8: sensibilidade: diária −15% → 26.087,21 e 32,7 anos; ocupação −10 pontos → 13.547,84 e 62,6 anos; CAPEX +20% → 17,7 anos", brl(A.sens.diaria.sobra) === "R$ 26.087,21" && Z.fmtVolta(A.sens.diaria.volta) === "32,7 anos" && brl(A.sens.ocupacao.sobra) === "R$ 13.547,84" && Z.fmtVolta(A.sens.ocupacao.volta) === "62,6 anos" && Z.fmtVolta(A.sens.capex.volta) === "17,7 anos");
t("Marina 7.8: o que precisa ser verdade em 8 anos: x = 224.144,92; 50,6%; R$ 808,72; CAPEX até 385.746,48", brl(A.verdade[8].x) === "R$ 224.144,92" && Z.fmtPct(A.verdade[8].ocup) === "50,6%" && brl(A.verdade[8].diaria) === "R$ 808,72" && brl(A.verdade[8].capex) === "R$ 385.746,48");
t("Marina 7.8: em 12 anos: 41,9%; R$ 690,96; CAPEX até 617.025,63", Z.fmtPct(A.verdade[12].ocup) === "41,9%" && brl(A.verdade[12].diaria) === "R$ 690,96" && brl(A.verdade[12].capex) === "R$ 617.025,63");
t("Marina 7.8: o limite da página 6 com a margem aberta: 8 × 57.819,79 = 462.558,31", brl(A.limiteNovo) === "R$ 462.558,31");
// 7.9
t("Marina 7.9: passos passa, passa, redesenhar, redesenhar, ajustar", A.passos.map((p) => p.status).join() === "passa,passa,redesenhar,redesenhar,ajustar");
t("Marina 7.9: veredito sugerido «Redesenhar», sem premissa não provada", A.regua === "Redesenhar" && A.sugerido === "Redesenhar" && A.premissas.length === 0);
t("Marina 7.9: o motivo do veredito cita os passos 3 e 4", Z.motivoVeredito(A) === "Redesenhar no passo 3 e passo 4: neste desenho a conta não fecha.");
t("Marina 7.9: alertas B5, B7, B11 (os três da tela e do PDF) e B15, nessa ordem", al(EX).join() === "B5,B7,B11,B15" && Z.tresPrimeiros(Z.alertas(EX, C)).map((a) => a.id).join() === "B5,B7,B11");
const AL = Z.alertas(EX, C);
t("Marina: B5 diz que três meses de custo passam a R$ 53.524,02", /R\$ 53\.524,02/.test(AL[0].txt));
t("Marina: B7 mostra R$ 31.167,21 no banco no pior mês", /R\$ 31\.167,21/.test(AL[1].txt) && /3,9%/.test(AL[1].txt));
t("Marina: B11 diz que o limite passa a R$ 462.558,31", /R\$ 462\.558,31/.test(AL[2].txt) && /margem de referência/.test(AL[2].txt));
t("Marina: B15 com o terreno a 25,4 anos", /25,4 anos/.test(AL[3].txt));
t("Marina 7.9: veredito escrito Redesenhar e o critério dela", EX.vereditoPessoa === "Redesenhar" && EX.criterioParar === "Se nenhum redesenho passar de 12 para 8 anos com premissas provadas, eu não assino a obra.");
const acM = Z.acaoSugerida(EX, C);
t("Marina 7.9: ação de 30 dias (ordem 2) e verificação", acM.ordem === 2 && EX.acao30 === "Rodar a 6B com três redesenhos, uma alavanca por vez, e não assinar contrato de obra." && EX.verificacao === "As três versões da 6B salvas, com data.");
t("Marina 7.9: prazo 28/12/2026", EX.prazo === "2026-12-28" && Z.prazoOk(EX.prazo, HOJE));
// 7.10 alavancas
const ALV = [["diaria", 50, 74219.06, -9983.09, "11,8 anos", "ajustar"], ["diaria", 71, 81106.75, -6199.33, "10,8 anos", "ajustar"], ["ocupacao", 5, 79955.76, -6831.63, "11,0 anos", "ajustar"],
  ["fixo", -10, 69082.51, -7729.32, "12,6 anos", "redesenhar"], ["capex", -10, 57819.79, -18992.04, "13,6 anos", "redesenhar"], ["extras", true, 65079.31, -15004.01, "13,4 anos", "redesenhar"], ["unidades", 2, 1004.13, -50203.76, "mais de 100 anos", "redesenhar"]];
for (const [tp, v, s, a1, vt, p3] of ALV) { const r = Z.alavanca(EX, tp, v, HOJE); t(`Marina 7.10: alavanca ${tp} ${v} → ${s}, ${a1}, ${vt}, ${p3}`, r.ok && brl(r.sobra) === brl(s) && brl(r.ano1) === brl(a1) && Z.fmtVolta(r.volta) === vt && r.passo3 === p3, r.ok ? [r.sobra, r.ano1, r.volta, r.passo3] : r.motivo); }
t("Marina 7.10: custo fixo −10% = R$ 8.447,04 por mês; CAPEX −10% = 712.017,90; duas cabanas: CAPEX 622.150", brl(Z.alavanca(EX, "fixo", -10, HOJE).fixoMes) === "R$ 8.447,04" && brl(Z.alavanca(EX, "capex", -10, HOJE).capex) === "R$ 712.017,90" && Z.alavanca(EX, "unidades", 2, HOJE).capex === 622150);
t("alavancas: fora da faixa é recusada (diária +301, ocupação +16, fixo −31, unidades sem CAPEX por unidade)", !Z.alavanca(EX, "diaria", 301, HOJE).ok && !Z.alavanca(EX, "ocupacao", 16, HOJE).ok && !Z.alavanca(EX, "fixo", -31, HOJE).ok && !Z.alavanca(Object.assign(clone(EX), { capexPorUnidade: "" }), "unidades", 2, HOJE).ok && !Z.alavanca(EX, "unidades", 3, HOJE).ok);
t("alavancas nunca gravam por cima da conta", JSON.stringify(EX) === EX_ANTES && Z.calcular(EX, HOJE).A.cons.sobra === c.sobra);
// 7.11 ajustado
const AJ = Z.ajustado(EX, HOJE), aj = AJ.A, ajc = aj.cons;
t("Marina 7.11: ajustado definido (R$ 716, 42%, cesta de café)", Z.ajustadoDefinido(EX) && AJ.ok);
t("Marina 7.11: noites 459,9 / estadias 229,95; hospedagem 329.288,40; cestas 19.315,80; bruta 348.604,20", perto(ajc.N, 459.9, 1e-9) && perto(ajc.estadias, 229.95, 1e-9) && brl(ajc.hosp) === "R$ 329.288,40" && brl(ajc.extras) === "R$ 19.315,80" && brl(ajc.bruta) === "R$ 348.604,20");
t("Marina 7.11: deduções da hospedagem 59.930,49 e imposto das cestas 1.158,95", brl(ajc.deducoes - 0.06 * ajc.extras) === "R$ 59.930,49" && brl(0.06 * ajc.extras) === "R$ 1.158,95");
t("Marina 7.11: custos de cada noite 48.133,13 e custo das cestas 9.657,90", brl(ajc.vEstadia + ajc.vNoite + ajc.vPct) === "R$ 48.133,13" && brl(ajc.vExtras) === "R$ 9.657,90");
t("Marina 7.11: antes da reserva 117.096,53; reserva 10.458,13; o que sobra 106.638,40 (margem 30,6%)", brl(ajc.antes) === "R$ 117.096,53" && brl(ajc.reserva) === "R$ 10.458,13" && brl(ajc.sobra) === "R$ 106.638,40" && Z.fmtPct(ajc.margem) === "30,6%");
t("Marina 7.11: ano 1 +7.826,50; menor saldo −1.878,35 em março; escada 8,3 anos", brl(aj.ano1.cons) === "R$ 7.826,50" && brl(aj.menorAcum) === "-R$ 1.878,35" && aj.meses[aj.menorMes - 1].nome === "mar" && Z.fmtVolta(aj.volta.cons) === "8,3 anos");
t("Marina 7.11: giro 60.491,45 (conta A); colchão 58.613,10 = 7,4%; com giro de 80.991,45 passaria", brl(aj.giroUsado) === "R$ 60.491,45" && brl(aj.colchao) === "R$ 58.613,10" && Z.fmtPct(aj.colchaoPct) === "7,4%" && brl(aj.giro10) === "R$ 80.991,45");
t("Marina 7.11: teste de queda (R$ 644,40; 33,6%) +42.290,37", brl(aj.queda.diaria) === "R$ 644,40" && Z.fmtPct(aj.queda.ocup) === "33,6%" && brl(aj.sobraQueda) === "R$ 42.290,37");
t("Marina 7.11: sem taxa: passos passa, passa, ajustar, pendente, ajustar → régua Ajustar, ficha mostra «Testar»", aj.passos.map((p) => p.status).join() === "passa,passa,ajustar,pendente,ajustar" && aj.regua === "Ajustar" && AJ.veredito === "Testar");
t("Marina 7.11: Testar porque a diária passa de 1,05 × 645 = 677,25 e a ocupação passa da medida", aj.premissas.includes("diaria") && aj.premissas.includes("ocupacao"));
const EXt = (taxa, mult) => Object.assign(clone(EX), { taxa: taxa, multiploSaida: mult });
const AJ8 = Z.ajustado(EXt("8", "6"), HOJE).A, AJ12 = Z.ajustado(EXt("12", "6"), HOJE).A;
t("Marina 7.11: valor presente do ajustado a 8%, 10% e 12% (sem/com saída), tolerância de R$ 0,10 (arredondamento do plano)", perto(AJ8.vpSem, -167071.13, 0.10) && perto(AJ8.vpCom, 158358.97, 0.10) && perto(Z.ajustado(EXt("10", "6"), HOJE).A.vpSem, -225713.19, 0.10) && perto(Z.ajustado(EXt("10", "6"), HOJE).A.vpCom, 45161.50, 0.10) && perto(AJ12.vpSem, -276825.15, 0.10));
t("Marina 7.11: passo 4 do ajustado ajusta até cerca de 10,9% ao ano (positivo só com a saída) e redesenha acima", AJ8.passos[3].status === "ajustar" && AJ12.passos[3].status === "redesenhar" && Z.fmtPct(aj.taxaViradaCom === null ? Z.taxaVirada(aj.fluxos, 791131, 6 * ajc.depoisModelo) : aj.taxaViradaCom) === "10,9%");
t("Marina 7.11: com taxa de 8% e saída 6×, a régua do ajustado dá Ajustar e a ficha, Testar", AJ8.regua === "Ajustar" && AJ8.sugerido === "Testar");
// 7.12 quadros de volta
const TP = C.transposicao;
t("Marina 7.12: página 6 refeita: margem 21,26, nota 3, giro 3 meses", TP.margem === 21.26 && TP.nota === 3 && TP.giroMeses === 3);
const rec = c.hosp, m = TP.margem / 100, res6 = rec * m, giro6 = 3 * (1 - m) * rec / 12;
t("Marina 7.12: a ficha do Pilar 6 vai mostrar 57.809,32; giro 53.526,64; investimento 844.657,64; 14,6 anos; limite 462.474,52 (passou em 382.183,12)", brl(res6) === "R$ 57.809,32" && brl(giro6) === "R$ 53.526,64" && brl(791131 + giro6) === "R$ 844.657,64" && Z.fmtNum((791131 + giro6) / res6, 1) === "14,6" && brl(8 * res6) === "R$ 462.474,52" && brl(791131 + giro6 - 8 * res6) === "R$ 382.183,12");
t("Marina 7.12: na página 6 refeita, base e otimista 11,3 e 8,7 anos", Z.fmtNum((791131 + giro6) / (b.hosp * m), 1) === "11,3" && Z.fmtNum((791131 + giro6) / (o.hosp * m), 1) === "8,7");
const P2 = C.planilha2;
t("Marina 7.12: Planilha 2: B5 791.131, B6 0, B7 =53.524,02/B8, diária 645 nos três, 38,5% / 50% / 65%", P2.b5 === 791131 && P2.b6 === 0 && P2.b7 === "=53.524,02/B8" && P2.diaria === 645 && P2.ocup.map((x) => Z.fmtPct(x)).join() === "38,5%,50,0%,65,0%");
t("Marina 7.12: Planilha 2: B10 0, B11 12,2%, B12 123,30, B13 6%, B14 0, B15 0", P2.b10 === 0 && perto(P2.b11, 0.122, 1e-12) && perto(P2.b12, 123.3, 1e-9) && P2.b13 === 0.06 && P2.b14 === 0 && P2.b15 === 0);
t("Marina 7.12: fixos B18 4.600, B19 500, B20 350, B21 800, B22 450, B23 1.100, B24 1.585,60; C25 9.385,60", P2.fixos.map((x) => x.cel + "=" + Z.fmtNum(x.valor, 2)).join(" ") === "B18=4.600,00 B19=500,00 B20=350,00 B21=800,00 B22=450,00 B23=1.100,00 B24=1.585,60" && perto(P2.c25, 9385.6, 1e-9));
// identidade da Planilha 2 (fórmulas da aba Modelo de renda, linhas 29 a 44, refeitas aqui de forma independente)
const pl2 = (col) => { const un = P2.unidades, d = P2.diaria, oc = P2.ocup[col], B10 = P2.b10, B11 = P2.b11, B12 = P2.b12, B13 = P2.b13 || 0, B14 = P2.b14; const disp = un * 365, vend = disp * oc; const recH = vend * d, recX = vend * d * B10; const C26 = P2.c25 * 12;
  const liq = recH * (1 - B11 - B13) + recX * (1 - B13); const gest = liq * B14; const noi = liq - gest - vend * B12 - C26; const eq = C26 / (disp * (d * (1 - B11 - B13) * (1 - B14) + d * B10 * (1 - B13) * (1 - B14) - B12)); return { noi, eq }; };
t("identidade: a Planilha 2 com o quadro dá o resultado anual do conservador = o que sobra (R$ 0,01) nos três cenários", perto(pl2(0).noi, c.sobra, 0.01) && perto(pl2(1).noi, b.sobra, 0.01) && perto(pl2(2).noi, o.sobra, 0.01));
t("identidade: a ocupação de equilíbrio da Planilha 2 = a da 6B (25,4%)", perto(pl2(0).eq, A.ocupEq, 1e-9));

/* ================= 2. Exercícios E2 e E4 (PLANO 5.4) ================= */
const E2 = Object.assign(clone(EX), { pPlataforma: "80" });
const C2 = calc(E2), c2 = C2.A.cons;
t("E2: comissão 12%, cartão 0,6%, deduções 20,6% da receita", perto(c2.comissao / c2.hosp, 0.12, 1e-12) && perto(c2.cartao / c2.hosp, 0.006, 1e-12) && perto(c2.deducoes / c2.bruta, 0.206, 1e-12));
t("E2: o que fica de cada noite R$ 388,83; o que sobra 51.293,81; margem 18,9% (risco)", brl(C2.A.cNoite) === "R$ 388,83" && brl(c2.sobra) === "R$ 51.293,81" && Z.fmtPct(c2.margem) === "18,9%" && Z.leituraMargem(c2.margem).faixa === "risco");
t("E2: equilíbrio 289,66 noites = 26,5%; folga 12,0 pontos", Z.fmtNum(C2.A.Neq, 2) === "289,66" && Z.fmtPct(C2.A.ocupEq) === "26,5%" && Z.fmtNum(C2.A.folga * 100, 1) === "12,0");
const E4 = Object.assign(clone(EX), { diaria: "695" });
const C4 = calc(E4);
t("E4: diária 695: noite 443,21; sobra 74.219,06; ano 1 −9.983,09; 11,79 anos → ajustar", brl(C4.A.cNoite) === "R$ 443,21" && brl(C4.A.cons.sobra) === "R$ 74.219,06" && brl(C4.A.ano1.cons) === "-R$ 9.983,09" && Z.fmtNum(C4.A.volta.cons, 2) === "11,79" && C4.A.passos[2].status === "ajustar");
t("E4: os R$ 50 valem 16.399,27 por ano (na margem de referência da página 6, 8.431,50)", brl(50 * A.efeito1) === "R$ 16.399,27" && brl(50 * 421.575 * 0.40) === "R$ 8.431,50");
t("E4: diária de 695 dá Testar se a medida é 645 (passa de 677,25)? Não: Redesenhar segue, porque o passo 4 redesenha", C4.A.premissas.includes("diaria") && C4.A.sugerido === "Redesenhar");

/* ================= 3. Bordas ================= */
function simples(o = {}) {
  const E = Z.estadoInicial(HOJE);
  Object.assign(E, { projeto: "Teste", situacao: "terreno", d1: "sim", d2: "sim", d3: "sim", d4: "sim", capex: "300000", giro6A: "10000", unidades: "1", origemCapex: "6A",
    diaria: "500", calendario: Array(12).fill("medio"), ocupMedia: "50", ocupAlta: "", ocupFraco: "", ocupBase: "60", ocupOtim: "70", mesAbertura: "1", estadiaMedia: "2",
    imposto: "5", impostoQuem: "Contador X", impostoData: "2026-11-01", pPlataforma: "0", comissaoPlataforma: "", cartaoDireto: "0", cancelamento: "2", comissaoNaoDuplicada: true,
    varLinhas: [Z.novaLinhaVar({ nome: "Limpeza", base: "porNoite", valor: "50", origem: "cotacao" })], fixLinhas: [Z.novaLinhaFixa({ nome: "Pessoa", valor: "2000", origem: "cotacao", grupo: "equipe" })],
    duodecimos: true, naoTrabalho: true, semModelo: true, reservaRep: "3", vereditoPessoa: "Ajustar", criterioParar: "Se a diária não passar, eu paro.", acao30: "Uma ação de teste", verificacao: "Uma verificação", prazo: Z.somaDias(HOJE, 10) }, o);
  return E;
}
const S0 = simples(), CS = calc(S0);
t("borda: o estado simples está completo", CS.pronto, CS.faltas);
t("borda: escada exatamente 8 anos passa; 8,0001 ajusta; 12 ajusta; 12,0001 redesenha", Z.classPasso3(8) === "passa" && Z.classPasso3(8.0001) === "ajustar" && Z.classPasso3(12) === "ajustar" && Z.classPasso3(12.0001) === "redesenhar" && Z.classPasso3(Infinity) === "redesenhar");
const E8 = Object.assign(clone(EX), { capex: A.verdade[8].capex });
const C8 = calc(E8);
t("borda: com o CAPEX máximo de 8 anos, a escada dá 8 e o passo 3 passa; com R$ 6 a mais, ajusta", perto(C8.A.volta.cons, 8, 1e-9) && C8.A.passos[2].status === "passa" && calc(Object.assign(clone(EX), { capex: A.verdade[8].capex + 6 })).A.passos[2].status === "ajustar");
t("borda: colchão exatamente 10% passa; 0 ajusta; −R$ 0,01 redesenha", calc(Object.assign(clone(EX), { giro6B: A.giro10 })).A.passos[4].status === "passa" && Z.classPasso5(0) === "ajustar" && Z.classPasso5(-0.01 / 791131) === "redesenhar");
t("borda: déficit do teste de queda exatamente 3 × fixo do mês ajusta; um centavo acima redesenha", Z.classPasso2(-3 * 9385.6, 9385.6) === "ajustar" && Z.classPasso2(-3 * 9385.6 - 0.01, 9385.6) === "redesenhar" && Z.classPasso2(0, 9385.6) === "passa");
const fixZero = (CS.A.cons.sobra + CS.A.cons.fixoAno) / 12;
const SZ = calc(simples({ fixLinhas: [Z.novaLinhaFixa({ nome: "Pessoa", valor: fixZero, origem: "cotacao" })] }));
t("borda: o que sobra = 0 passa no passo 1, e a escada «não se paga»", perto(SZ.A.cons.sobra, 0, 1e-6) && SZ.A.passos[0].status === "passa" && Z.fmtVolta(SZ.A.volta.cons) === "não se paga" && SZ.A.passos[2].status === "redesenhar" && Z.classPasso1(0) === "passa");
t("borda: diária = 1,05 × medida não pede Testar; um centavo acima pede", !calc(simples({ diaria: "525", diariaMedida: "500" })).A.premissas.includes("diaria") && calc(simples({ diaria: "525,01", diariaMedida: "500" })).A.premissas.includes("diaria"));
const SI = simples({ impostoData: "" });
t("borda: imposto com número e sem a data é tratado como em branco (B1, resultado antes do imposto)", !Z.impostoValido(SI) && calc(SI).P.imposto === 0 && calc(SI).A.premissas.includes("imposto") && al(SI).includes("B1"));
t("borda: imposto com data no futuro também fica em branco", !Z.impostoValido(simples({ impostoData: "2026-12-01" })));
const SN = simples({ varLinhas: [Z.novaLinhaVar({ nome: "Caro", base: "porNoite", valor: "600", origem: "cotacao" })] });
const CN = calc(SN);
t("borda: custo da noite maior que a diária: «cada noite vendida aumenta o prejuízo», sem equilíbrio (B4)", CN.A.cadaNoitePiora && CN.A.ocupEq === null && Z.leituraEquilibrio(CN.A).faixa === "critico" && al(SN).includes("B4"));
t("borda: folga exatamente 0 fica em «fina»; 5 pontos fica «com folga»; −0,1 é crítico", Z.leituraEquilibrio({ folga: 0, ocupEq: 0.4 }).faixa === "fina" && Z.leituraEquilibrio({ folga: 0.05, ocupEq: 0.4 }).faixa === "folga" && Z.leituraEquilibrio({ folga: -0.001, ocupEq: 0.4 }).faixa === "critico");
t("borda: equilíbrio acima de 70% é «estrutural, não comercial» (B4)", /estrutural/.test(Z.leituraEquilibrio({ folga: 0.01, ocupEq: 0.71 }).t));
const fl = [-10000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000];
const somaFl = fl.reduce((s, x) => s + x, 0);
t("borda: soma simples dos fluxos = CAPEX: decidido, negativo a qualquer taxa", Z.classPasso4(fl, somaFl, null, 0).status === "redesenhar" && Z.classPasso4(fl, somaFl, null, 0).decidido);
t("borda: soma simples acima do CAPEX e taxa vazia: passo 4 pendente (B14 e Testar)", Z.classPasso4(fl, somaFl - 1, null, 0).status === "pendente");
t("borda: com taxa, valor presente ≥ 0 passa; negativo sem e positivo com a saída ajusta; negativo nos dois redesenha", Z.classPasso4(fl, 100000, 0.05, 0).status === "passa" && Z.classPasso4(fl, 160000, 0.05, 100000).status === "ajustar" && Z.classPasso4(fl, 160000, 0.05, 0).status === "redesenhar");
t("borda: taxa 0% = soma simples menos o CAPEX", perto(Z.vp(fl, 100000, 0, 0), somaFl - 100000, 1e-9));
const SB6 = Object.assign(clone(EX), { calendario: ["fraco", "fraco", "medio", "medio", "medio", "alta", "alta", "alta", "medio", "medio", "fraco", "fraco"] });
t("borda: calendário com contagens diferentes da página 2 dispara B6", al(SB6).includes("B6") && /4 fracos/.test(Z.alertas(SB6, calc(SB6)).find((x) => x.id === "B6").txt));
t("borda: ocupação do ano diferente da página 2 em mais de 0,1 ponto dispara B6; 0,1 exato não", al(Object.assign(clone(EX), { p2OcupAno: "38,3" })).includes("B6") && !al(Object.assign(clone(EX), { p2OcupAno: "38,4" })).includes("B6"));
const ED = Object.assign(clone(EX), { mesAbertura: "12" }), CD = calc(ED);
t("borda: abertura em dezembro vira o ano (mês 1 = dez, mês 2 = jan, mês 13 = dez)", CD.A.meses[0].mes === 12 && CD.A.meses[1].mes === 1 && CD.A.meses[12].mes === 12 && Z.mesDoCalendario(12, 2) === 1);
t("borda: abertura em dezembro: as duas contas do ano 1 batem e o regime continua = o que sobra", perto(CD.A.ano1Resultado, CD.A.ano1.cons, 1e-6) && perto(CD.A.somaRegime, CD.A.cons.sobra, 1e-6));
const CE1 = calc(simples({ estadiaMedia: "1" }));
t("borda: estadia média de 1 noite: estadias = noites", perto(CE1.A.cons.estadias, CE1.A.cons.N, 1e-9));
const SX = simples({ extras: [Z.novoExtra({ nome: "Passeio", captura: "50", ticket: "100", custoDireto: "120" })] });
t("borda: outra receita com preço ≤ custo direto é apontada", Z.extrasSemGanho(SX).length === 1 && Z.extrasSemGanho(simples({ extras: [Z.novoExtra({ nome: "Cesta", captura: "50", ticket: "140", custoDireto: "70" })] })).length === 0);
const SA = simples({ situacao: "opero", contaAmpliacao: true, extrato: true, fixLinhas: [Z.novaLinhaFixa({ nome: "Pessoa nova", valor: "2000", origem: "cotacao" }), Z.novaLinhaFixa({ nome: "Gerente que já existe", valor: "5000", origem: "cotacao", jaExiste: true })] });
t("borda: modo ampliação: só as linhas novas entram no fixo da ampliação", perto(calc(SA).P.fixoLinhas, 2000, 1e-9) && perto(calc(Object.assign(clone(SA), { contaAmpliacao: false })).P.fixoLinhas, 7000, 1e-9));
t("borda: prazo em hoje + 30 vale; hoje + 31 não; ontem não", Z.prazoOk(Z.somaDias(HOJE, 30), HOJE) && !Z.prazoOk(Z.somaDias(HOJE, 31), HOJE) && !Z.prazoOk(Z.somaDias(HOJE, -1), HOJE));
t("borda: divisão por zero devolve null (div)", Z.div(1, 0) === null && Z.div(null, 2) === null);
t("borda: ocupação zero não quebra: sem equilíbrio nem meses", (() => { const x = calc(simples({ ocupMedia: "0", ocupBase: "0", ocupOtim: "0" })); return x.pronto && x.A.cNoite === null && x.A.meses.length === 0 && x.A.ano1.cons === null; })());
t("borda: «Não sei» na diária deixa a conta pendente (nunca um zero escondido)", !calc(simples({ diaria: Z.NS })).pronto && calc(simples({ diaria: Z.NS })).faltas.includes("a diária"));
t("borda: a reserva de reposição «Não sei» vale 0 na conta e bloqueia o selo", calc(simples({ reservaRep: Z.NS })).P.reserva === 0 && !Z.criterio(simples({ reservaRep: Z.NS }), undefined, HOJE).itens[6].ok);
t("borda: retirada = horas × valor-hora × 4,33; não trabalho = 0", Z.retiradaMes({ horasSemana: "10", valorHora: "50" }) === 10 * 50 * 4.33 && Z.retiradaMes({ naoTrabalho: true }) === 0);
t("borda: linhas anuais entram divididas por 12", Z.valorFixoMes({ valor: "3.600", periodo: "anual", origem: "estimativa" }) === 300 && Z.valorFixoMes({ valor: "3.600", periodo: "mensal", origem: "estimativa" }) === 3600 && Z.valorFixoMes({ valor: "", origem: "branco" }) === 0);
t("borda: % da receita entre 0 e 20; acima é erro", Z.valorVar({ base: "pctReceita", valor: "1", origem: "estimativa" }) === 0.01 && Z.valorVar({ base: "pctReceita", valor: "21", origem: "estimativa" }) === null && Z.erroVar({ nome: "Perdas", base: "pctReceita", valor: "21", origem: "estimativa" }) !== "");

/* ================= 4. Alertas restantes ================= */
t("B2: sem a página 6A no aparelho", al(simples({ origemCapex: "digitado" })).includes("B2") && !al(S0).includes("B2"));
t("B3: no cenário medido não sobra nada", al(simples({ fixLinhas: [Z.novaLinhaFixa({ nome: "Pessoa", valor: "20000", origem: "cotacao" })] })).includes("B3"));
t("B5 e B7 não disparam com giro e colchão folgados", (() => { const x = al(simples({ giro6A: "1000000", giro6B: "1000000" })); return !x.includes("B5") && !x.includes("B7"); })());
t("B8: zero horas sem marcar que não trabalha", al(simples({ naoTrabalho: false, horasSemana: "0", valorHora: "40" })).includes("B8") && !al(S0).includes("B8"));
t("B9: reserva de reposição abaixo de 3%", al(simples({ reservaRep: "2" })).includes("B9") && !al(S0).includes("B9"));
t("B10: comissão e duodécimos sem confirmar bloqueiam o selo", al(simples({ comissaoNaoDuplicada: false })).includes("B10") && Z.alertas(simples({ duodecimos: false })).find((x) => x.id === "B10").tipo === "bloqueia");
const EB12 = Object.assign(clone(EX), { taxa: "1", multiploSaida: "6" });
t("B12: com taxa de 1% e saída 6×, só a venda salva a conta (passo 4 ajustar)", calc(EB12).A.passos[3].status === "ajustar" && al(EB12).includes("B12"));
t("B12 não dispara com taxa de 2% (negativo também com a saída)", calc(Object.assign(clone(EX), { taxa: "2", multiploSaida: "6" })).A.passos[3].status === "redesenhar" && !al(Object.assign(clone(EX), { taxa: "2", multiploSaida: "6" })).includes("B12"));
const SB13 = simples({ fixLinhas: [Z.novaLinhaFixa({ nome: "Pessoa", valor: "6500", origem: "cotacao" })], extras: [Z.novoExtra({ nome: "Cesta", captura: "100", ticket: "200", custoDireto: "20" })] });
t("B13: a conta só passa no passo 1 com as outras receitas", calc(SB13).A.passos[0].status === "passa" && al(SB13).includes("B13"));
t("B14: taxa vazia com a soma simples sem decidir", al(Object.assign(clone(EX), { diaria: "1500" })).includes("B14") && calc(Object.assign(clone(EX), { diaria: "1500" })).A.p4.status === "pendente");
t("B16: quem já opera sem o extrato de doze meses", al(simples({ situacao: "opero" })).includes("B16") && !al(simples({ situacao: "opero", extrato: true })).includes("B16"));
t("os 16 alertas foram disparados ao menos uma vez", Z.ORDEM_ALERTAS.every((x) => disparados.has(x)), Z.ORDEM_ALERTAS.filter((x) => !disparados.has(x)));
t("INFO fixo: «Pergunte ao seu contador» com as quatro perguntas e «Esta ficha não envia nada»", Z.INFO.tit === "Pergunte ao seu contador" && Z.INFO.contador.length === 4 && Z.INFO.naoEnvia === "Esta ficha não envia nada: o PDF fica só com você.");

/* ================= 5. Veredito, Testar, ação de 30 dias ================= */
const SV = simples({ capex: "50000", giro6B: "100000", taxa: "8" });
const CV = calc(SV);
t("régua: tudo passando dá Avançar", CV.A.passos.every((p) => p.status === "passa") && CV.A.sugerido === "Avançar", CV.A.passos.map((p) => p.status));
t("Testar substitui Avançar com imposto em branco, e nunca Redesenhar", calc(simples({ capex: "50000", giro6B: "100000", taxa: "8", imposto: Z.BRANCO })).A.sugerido === "Testar" && calc(Object.assign(clone(EX), { imposto: Z.BRANCO })).A.sugerido === "Redesenhar");
t("Testar com ocupação acima de 65%", calc(simples({ capex: "50000", giro6B: "100000", ocupMedia: "70", ocupBase: "75", ocupOtim: "80" })).A.premissas.includes("ocupacao65"));
t("Pausar nunca é sugerido (só escolha da pessoa)", ![CV, C, C2, C4, CS, SZ, CN].some((x) => x.A.sugerido === "Pausar") && Z.VEREDITOS.some((v) => v.v === "Pausar"));
t("ação 1: imposto em branco → levar a conta ao contador", Z.acaoSugerida(simples({ imposto: Z.BRANCO })).ordem === 1 && /contador/.test(Z.acaoSugerida(simples({ imposto: Z.BRANCO })).acao));
t("ação 2: Redesenhar → três redesenhos", acM.ordem === 2);
const ST = simples({ capex: "50000", giro6B: "100000", taxa: "8", diaria: "600", diariaMedida: "500" });
t("ação 3: Testar por premissa não provada → provar a premissa", calc(ST).A.sugerido === "Testar" && Z.acaoSugerida(ST).ordem === 3);
const SCol = simples({ taxa: "8", giro6B: "", giro6A: "0" });
t("ação 4: ajustar pelo colchão → recalcular o pedido com 10% de colchão", calc(SCol).A.passos[4].status === "ajustar" && Z.acaoSugerida(SCol).ordem === 4, calc(SCol).A.passos.map((p) => p.status));
const SVol = simples({ capex: "411800", taxa: "0", giro6B: "1000000" });
t("ação 5: ajustar pelo tempo de volta (8 a 12) → escolher uma alavanca", calc(SVol).A.passos[2].status === "ajustar" && Z.acaoSugerida(SVol).ordem === 5, calc(SVol).A.passos.map((p) => p.status));
const S6 = simples({ capex: "50000", giro6B: "100000", taxa: "8", fixLinhas: [Z.novaLinhaFixa({ nome: "Pessoa", valor: "2000", origem: "estimativa" })] });
t("ação 6: linhas fixas sem cotação → propostas das três maiores", Z.acaoSugerida(S6).ordem === 6);
t("ação 7: Avançar com tudo cotado → refazer a página 6 e a Planilha 2", Z.acaoSugerida(SV).ordem === 7 && /Planilha 2/.test(Z.acaoSugerida(SV).acao));
t("ação 7 para quem faz para outra pessoa: leva ao dono", /dono/.test(Z.acaoSugerida(Object.assign(clone(SV), { paraOutro: true })).acao));
t("as verificações da lista são as sete do plano", Z.VERIFICACOES.length === 7 && Z.VERIFICACOES[0] === "A alíquota anotada, com a data e o nome de quem respondeu.");
t("próxima etapa: autônomo e acompanhamento (turma)", /Planilha 2 e siga ao Pilar 7/.test(Z.proximaEtapa({})) && /encontro do Pilar 6/.test(Z.proximaEtapa({ turma: "acompanhamento" })));

/* ================= 6. Telas e critério de conclusão ================= */
const V0 = Z.estadoInicial(HOJE);
t("telas: as 13 telas do plano, na ordem", Z.TELAS.join() === "abertura,parte,entra,real,noite,mes,reserva,caixa,vale,resultado,alavancas,veredito,acao");
t("telas: estado vazio bloqueia abertura, parte, entra, real, noite, mes, veredito e ação", ["abertura", "parte", "entra", "real", "noite", "mes", "veredito", "acao"].every((x) => Z.validarTela(x, V0, HOJE) !== ""));
t("telas: o exemplo da Marina passa em todas as telas", Z.TELAS.every((x) => Z.validarTela(x, EX, HOJE) === ""), Z.TELAS.map((x) => [x, Z.validarTela(x, EX, HOJE)]).filter((x) => x[1]));
t("tela 3: imposto «em branco, aguardando o contador» é aceito; número sem quem é recusado", Z.validarTela("real", Object.assign(clone(EX), { imposto: Z.BRANCO, impostoQuem: "" }), HOJE) === "" && /quem respondeu/.test(Z.validarTela("real", Object.assign(clone(EX), { impostoQuem: "" }), HOJE)));
t("tela 2: base abaixo do conservador é recusada", /cenário base/.test(Z.validarTela("entra", Object.assign(clone(EX), { ocupBase: "30" }), HOJE)));
t("tela 5: modelo com os três zeros pede «não há»", /não há/.test(Z.validarTela("mes", Object.assign(clone(EX), { semModelo: false, aluguelMes: "0", gestaoPct: "0", royaltyPct: "0" }), HOJE)));
t("tela 7: giro abaixo da maior das três contas é recusado; acima pede justificativa", /53\.524,02/.test(Z.validarTela("caixa", Object.assign(clone(EX), { giro6B: "50.000" }), HOJE)) && /por quê/.test(Z.validarTela("caixa", Object.assign(clone(EX), { giro6B: "60.000" }), HOJE)) && Z.validarTela("caixa", Object.assign(clone(EX), { giro6B: "60.000", giroJustificativa: "Mais um mês de folga." }), HOJE) === "");
t("tela 8: taxa acima de 30% é recusada", Z.validarTela("vale", Object.assign(clone(EX), { taxa: "31" }), HOJE) !== "" && Z.validarTela("vale", Object.assign(clone(EX), { taxa: Z.NS }), HOJE) === "");
const CR = Z.criterio(EX, C, HOJE);
t("critério: 12 itens; a Marina tem os 11 primeiros e falta só o PDF", CR.itens.length === 12 && CR.antesDoPdf && !CR.ok && CR.faltas.length === 1 && /PDF/.test(CR.faltas[0]));
t("critério: com o PDF baixado, selo «Pronto para levar à página 6»", Z.criterio(Object.assign(clone(EX), { pdfBaixado: true }), undefined, HOJE).ok);
t("critério: o selo sai com o imposto em branco (decisão de Bruno, primeira versão honesta)", Z.criterio(Object.assign(clone(EX), { imposto: Z.BRANCO, pdfBaixado: true }), undefined, HOJE).ok);
t("critério: o selo não exige Avançar (Redesenhar recebe o selo)", Z.criterio(Object.assign(clone(EX), { pdfBaixado: true }), undefined, HOJE).ok && C.A.sugerido === "Redesenhar");
t("critério: sem as confirmações (B10) o item 4 falha", !Z.criterio(Object.assign(clone(EX), { duodecimos: false }), undefined, HOJE).itens[3].ok);
t("critério: giro abaixo do mínimo falha o item 8", !Z.criterio(Object.assign(clone(EX), { giro6B: "40.000" }), undefined, HOJE).itens[7].ok);
t("critério: passo 4 pendente sem taxa falha o item 9; com taxa, passa", !Z.criterio(Object.assign(clone(EX), { diaria: "1500" }), undefined, HOJE).itens[8].ok && Z.criterio(Object.assign(clone(EX), { diaria: "1500", taxa: "8" }), undefined, HOJE).itens[8].ok);
t("critério: estado vazio lista o que falta, um item por linha", Z.criterio(V0, undefined, HOJE).faltas.length === 12);

/* ================= 7. Leituras tolerantes das outras páginas ================= */
const P6A = { resumo: { dados: { capex_fase: 791131, giro: 40787.38, investimento_total: 831918.38, terreno: 600000, terreno_situacao: "meu", unidades: 3, unidades_projeto: 5, limite6: 870130.8 } } };
const P6 = { fontes: { margem: "referencia" }, resumo: { dados: { diaria: 645, ocup_cons: 38.5, ocup_base: 50, ocup_otim: 65, margem: 40, resultado_cons: 108766.35, inv8: 870130.8, unidades: 3, giro: 40787.38, terreno: 600000 } } };
const P2d = { respostas: { meses_alta: "3", meses_fraco: "5", ocup_alta: "64", ocup_media: "40", ocup_fraco: "22" }, resumo: { dados: { diaria_media: 645.45, ocup_ano: 38.5 } } };
t("leitura da 6A com resumo.dados", Z.lerPagina6A(JSON.stringify(P6A)).capex === 791131 && Z.lerPagina6A(JSON.stringify(P6A)).temDados);
t("leitura da 6A com dados na raiz", Z.lerPagina6A({ dados: P6A.resumo.dados }).giro === 40787.38);
t("leitura da 6A com JSON quebrado devolve null; sem CAPEX, temDados falso", Z.lerPagina6A("{quebrado") === null && Z.lerPagina6A("{}").temDados === false && Z.lerPagina6A(null) === null);
t("leitura da página 6 com resumo.dados, a origem da margem e dados na raiz", Z.lerPagina6(JSON.stringify(P6)).margem === 40 && /referência da Zion/.test(Z.lerPagina6(P6).margemOrigem) && Z.lerPagina6({ dados: { diaria: 700 } }).diaria === 700);
t("leitura da página 6 com JSON quebrado devolve null", Z.lerPagina6("[1,2") === null && Z.lerPagina6("[]") === null);
t("leitura da página 2: diária média, ocupação do ano e a curva", (() => { const x = Z.lerPagina2(JSON.stringify(P2d)); return x.diariaMedia === 645.45 && x.ocupAno === 38.5 && x.mesesAlta === 3 && x.mesesFraco === 5 && x.ocupFraco === 22; })());
t("leitura da página 2 com dados na raiz e com JSON quebrado", Z.lerPagina2({ dados: { diaria_media: 500 } }).diariaMedia === 500 && Z.lerPagina2("x") === null);
const EL = Z.estadoInicial(HOJE);
const veio = Z.aplicarLeituras(EL, { p6a: Z.lerPagina6A(P6A), p6: Z.lerPagina6(P6), p2: Z.lerPagina2(P2d) });
t("leituras preenchem só o vazio, com a origem: CAPEX e giro da 6A, margem e limite, diária da página 6", EL.capex === "791.131" && veio.capex === "página 6A" && EL.giro6A === "40.787,38" && EL.margem6 === "40" && EL.limite6 === "870.130,80" && EL.diaria === "645" && veio.diaria === "página 6" && EL.origemCapex === "6A");
t("leituras: a curva do Pilar 2 (64 / 40 / 22) e as contagens 3 e 5; o calendário não é preenchido", EL.ocupAlta === "64" && EL.ocupFraco === "22" && EL.p2MesesAlta === "3" && EL.p2OcupAno === "38,5" && EL.calendario.every((x) => x === null));
t("leituras: nenhum valor de referência entra (imposto, reserva, valor-hora, cancelamento, taxa, múltiplo ficam vazios)", ["imposto", "reservaRep", "valorHora", "cancelamento", "taxa", "multiploSaida", "horasSemana"].every((k) => EL[k] === ""));
const EL2 = Z.estadoInicial(HOJE); EL2.capex = "500.000";
Z.aplicarLeituras(EL2, { p6a: Z.lerPagina6A(P6A) });
t("leituras não sobrescrevem o que a pessoa já digitou", EL2.capex === "500.000");
const EL3 = Z.estadoInicial(HOJE); Z.aplicarLeituras(EL3, { p2: Z.lerPagina2(P2d) });
t("sem a página 6, a diária vem da página 2 arredondada ao real", EL3.diaria === "645" && EL3.diariaMedida === "645,45");
t("Marco Zero: situação lida, valor estranho ignorado", Z.lerMarcoZero('{"situacao":"opero"}').situacao === "opero" && Z.lerMarcoZero('{"situacao":"x"}').situacao === null && Z.lerMarcoZero("{") === null);
t("estado inicial: nenhum valor de referência pré-preenchido e linhas sugeridas só com o nome", (() => { const e = Z.estadoInicial(HOJE); const v = Z.linhasVarSugeridas(), f = Z.linhasFixasSugeridas(); return e.reservaRep === "" && e.imposto === "" && v.length === 5 && f.length === 11 && v.concat(f).every((l) => l.valor === "" && l.origem === null); })());

/* ================= 8. resumo.dados (PLANO 6.8) ================= */
const RD = Z.resumoDados(EX, C);
const CHAVES68 = ["unidades", "diaria", "ocup_cons", "ocup_base", "ocup_otim", "estadia_media", "bruta", "deducoes", "real", "variaveis", "contribuicao", "fixo_ano", "retirada_mes", "antes_reserva", "modelo", "reserva_rep", "sobra", "margem_pct", "imposto_pct", "imposto_quem", "imposto_data", "ocup_eq", "folga_pontos", "custo_por_diaria", "diaria_eq", "ano1", "menor_acum", "giro_6a", "giro_a", "giro_b", "giro_6b", "investimento_6b", "colchao", "colchao_pct", "volta_escada", "volta_p6", "volta_com_terreno", "retorno_simples", "taxa", "vp_sem_saida", "vp_com_saida", "passos", "veredito_sugerido", "veredito_pessoa", "criterio_parar", "margem_para_p6", "giro_meses_para_p6", "exemplo"];
t("resumo.dados com todas as chaves do plano 6.8", CHAVES68.every((k) => k in RD), CHAVES68.filter((k) => !(k in RD)));
t("resumo.dados da Marina: sobra, investimento, volta, veredito, margem para a página 6", RD.sobra[0] === 57819.79 && RD.investimento_6b === 844655.02 && RD.volta_escada[0] === 15.01 && RD.veredito_sugerido === "Redesenhar" && RD.margem_para_p6 === 21.26 && RD.giro_meses_para_p6 === 3 && RD.imposto_pct === 6 && RD.exemplo === true);
t("resumo.dados é JSON (sem Infinity)", (() => { const x = Z.resumoDados(SZ.P ? simples({ fixLinhas: [Z.novaLinhaFixa({ nome: "Pessoa", valor: fixZero, origem: "cotacao" })] }) : S0, SZ); return JSON.parse(JSON.stringify(x)).volta_escada[0] === null; })());

/* ================= 9. Textos: promessas proibidas e voz do curso ================= */
const textos = [];
Object.values(Z.TEXTOS).forEach((x) => textos.push(x));
Object.values(Z.AJUDA).forEach((a) => Object.values(a).forEach((x) => textos.push(x)));
Z.VEREDITOS.forEach((x) => textos.push(x.v, x.t)); Z.VERIFICACOES.forEach((x) => textos.push(x)); Z.PROXIMOS.forEach((x) => textos.push(x)); Z.ALAVANCAS.forEach((x) => textos.push(x.r, x.dica));
Object.values(Z.ACOES).forEach((x) => textos.push(x.acao, x.verificacao)); Z.DIAG.forEach((d) => { textos.push(d.p); d.op.forEach((o) => textos.push(o.r)); }); Z.SITUACOES.forEach((s) => textos.push(s.r));
Object.values(Z.INFO).forEach((x) => (Array.isArray(x) ? x.forEach((y) => textos.push(y)) : textos.push(x)));
[EX, E2, E4, S0, SI, SN, SB6, SA, SB13, EB12, SV, ST, SCol, SVol, S6, simples({ situacao: "opero" }), simples({ reservaRep: "2" }), simples({ naoTrabalho: false, horasSemana: "0", valorHora: "1" })].forEach((E) => {
  const x = calc(E); Z.alertas(E, x).forEach((a) => textos.push(a.tit, a.txt)); const s = Z.acaoSugerida(E, x); textos.push(s.acao, s.verificacao, Z.proximaEtapa(E));
  if (x.A) textos.push(Z.motivoVeredito(x.A), Z.leituraMargem(x.A.cons.margem).t, Z.leituraEquilibrio(x.A).t, Z.leituraVolta(x.A.volta.cons));
});
EX.varLinhas.concat(EX.fixLinhas).forEach((l) => textos.push(l.nome)); Z.linhasVarSugeridas().concat(Z.linhasFixasSugeridas()).forEach((l) => textos.push(l.nome));
t("varredura: nenhuma promessa proibida, sigla técnica na tela ou frase que desmereça o Pilar 6 (" + textos.length + " textos)", textos.every(Z.textoSeguro), textos.filter((x) => !Z.textoSeguro(x)));
t("varredura: a própria varredura pega «retorno garantido», «payback», «NOI», «TIR», «estava errada» e «aluno»", ["Retorno garantido", "payback", "a linha NOI", "a TIR", "a margem estava errada", "o aluno", "margem inflada"].every((x) => !Z.textoSeguro(x)));
t("varredura: sem travessão nos textos", textos.every((x) => !/[—–]/.test(x)));
t("varredura: nenhum preço da Zion Glamping Store (129.000, 192.346) e a margem de 40% só como ponto de partida da página 6", textos.every((x) => !/129\.000|192\.346|25\.915|Glamping Store/.test(x)) && textos.filter((x) => /margem[^.]*\b40%|\b40%[^.]*margem/.test(x)).every((x) => /página 6|referência/.test(x)));
t("varredura: nenhuma alíquota sugerida fora do caso da Marina (6% só com «fictícia» ou «Marina»)", textos.filter((x) => /\b6%/.test(x) && /imposto/i.test(x)).every((x) => /fictícia|dela/.test(x)));
t("aviso educativo do plano, com «A Zion avalia cada caso.»", Z.TEXTOS.aviso === "Material educativo. Não é estudo de viabilidade, projeção nem promessa de retorno. Impostos se confirmam com o contador; contratos, com o advogado. A Zion avalia cada caso.");
t("«Esta ficha não envia nada» e o lembrete da pasta Meu Dossiê (páginas 6 e 6A)", Z.TEXTOS.naoEnvia === "Esta ficha não envia nada: o PDF fica só com você." && Z.TEXTOS.dossie === "Salve o PDF da página 6B na pasta Meu Dossiê, ao lado das páginas 6 e 6A.");
t("título «Faça agora · A sua conta» e página «Página 6B · Viabilidade»; promessa «Aprenda o passo a passo»", Z.TEXTOS.tituloCompleto === "Faça agora · A sua conta" && Z.TEXTOS.pagina === "Página 6B · Viabilidade" && /^Aprenda o passo a passo/.test(Z.TEXTOS.promessa));
t("nota da decisão de Bruno: a página 6 era a primeira conta, a conta aberta decide, sem desmerecer o Pilar 6", /primeira conta/.test(Z.TEXTOS.notaP6) && /simplificação, não promessa/.test(Z.TEXTOS.notaP6) && /conta aberta que decide/.test(Z.TEXTOS.notaP6));
t("«Cenários, não promessas.» e a taxa sem sugestão da Zion", Z.TEXTOS.cenarios === "Cenários, não promessas." && /A Zion não sugere taxa/.test(Z.TEXTOS.taxa));
t("formatação pt-BR (brl, fmtPct, fmtVolta, empate para cima)", brl(57819.79) === "R$ 57.819,79" && Z.fmtPct(0.2126) === "21,3%" && Z.fmtVolta(Infinity) === "não se paga" && Z.fmtVolta(101) === "mais de 100 anos" && Z.arred(0.125, 2) === 0.13 && Z.paraNumero("844.655,02") === 844655.02);

/* ================= 10. A página pública usa esta mesma lógica ================= */
const PUB = path.resolve(__dirname, "../../../../docs/trilha1/pilar6b");
if (fs.existsSync(path.join(PUB, "index.html"))) {
  const html = fs.readFileSync(path.join(PUB, "index.html"), "utf8");
  const semScript = html.replace(/<script[\s\S]*?<\/script>/g, "").replace(/<style[\s\S]*?<\/style>/g, "");
  t("cópia pública de logic.js idêntica à de src/", fs.existsSync(path.join(PUB, "logic.js")) && fs.readFileSync(path.join(PUB, "logic.js"), "utf8") === fs.readFileSync(path.resolve(__dirname, "../src/logic.js"), "utf8"));
  t("a página carrega logic.js", /<script src="logic\.js"><\/script>/.test(html));
  t("a página não envia dados (sem fetch, XMLHttpRequest, sendBeacon, webhook)", !/fetch\(|XMLHttpRequest|sendBeacon|FEEDBACK_URL|webhook/i.test(html));
  t("a página usa o jsPDF 2.5.1 do cdnjs, como a 6A", /cdnjs\.cloudflare\.com\/ajax\/libs\/jspdf\/2\.5\.1\/jspdf\.umd\.min\.js/.test(html) && /cdnjs\.cloudflare\.com\/ajax\/libs\/jspdf\/2\.5\.1/.test(fs.readFileSync(path.resolve(__dirname, "../../../../docs/trilha1/pilar6a/index.html"), "utf8")));
  t("a página salva só na chave zion-t1-pilar6b, com try/catch", /"zion-t1-pilar6b"/.test(html) && /try\s*\{\s*window\.localStorage\.setItem\(CHAVE/.test(html) && (html.match(/localStorage\.setItem\(/g) || []).length === 1);
  t("a página lê zion-t1-pilar6a, zion-t1-pilar6, zion-t1-aula2 e zion-t1-marco-zero", /"zion-t1-pilar6a"/.test(html) && /"zion-t1-pilar6"/.test(html) && /"zion-t1-aula2"/.test(html) && /zion-t1-marco-zero/.test(html));
  t("título da página: Faça agora · A sua conta", /<title>Faça agora · A sua conta<\/title>/.test(html));
  t("identidade da ficha da 6A (Playfair Display, Inter, #16261C, #E0BE5E)", /Playfair\+Display/.test(html) && /Inter/.test(html) && /#16261C/.test(html) && /#E0BE5E/.test(html));
  t("botão de exemplo «Exemplo ilustrativo»", /Exemplo ilustrativo/.test(html) && /id="ver-exemplo"/.test(html));
  t("varredura da página: nenhuma promessa proibida, sem mentor, noindex", Z.textoSeguro(semScript) && !/mentor/i.test(html) && /noindex/.test(html));
} else t("página pública docs/trilha1/pilar6b/index.html existe", false);

console.log(`\n${ok} testes aprovados, ${fal} falharam (lógica da viabilidade, página 6B).`);
process.exit(fal ? 1 : 0);

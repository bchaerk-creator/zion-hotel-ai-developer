// Testes da lógica da Folha Única do Mês. Uso: node tests/test_logic.js
const Z = require("../src/logic.js");
let ok = 0, fal = 0; const log = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
const perto = (a, b, tol) => a != null && Math.abs(a - b) <= (tol == null ? 0.005 : tol);
const EX = Z.EXEMPLO;

console.log("1. Exemplo didático (Cabanas do Vale, dados fictícios, PLANO seção 9)");
let r = Z.calcular(EX);
log(r.bloqueios.length === 0 && r.avisos.length === 0, "exemplo sem bloqueio nem aviso" + (r.bloqueios.length ? ": " + r.bloqueios.join(" | ") : ""));
log(r.noitesDisponiveis === 124 && perto(r.ocupacao, 58 / 124, 1e-9) && perto(r.mediaNoitesPorEstadia, 2.32), `124 noites disponíveis, ocupação ${Z.pct(r.ocupacao)}, ${Z.dec(r.mediaNoitesPorEstadia, 2)} noites por estadia`);
log(perto(r.deducoes, 3654.40), `deduções = ${r.deducoes.toFixed(2)} (ref 3.654,40)`);
log(perto(r.receitaRealHospedagem, 12585.60), `receita real de hospedagem = ${r.receitaRealHospedagem.toFixed(2)} (ref 12.585,60)`);
log(perto(r.diariaMediaBruta, 280) && perto(r.diariaMediaReal, 216.99), `diária média bruta ${r.diariaMediaBruta.toFixed(2)}, real ${r.diariaMediaReal.toFixed(2)} (ref 280 e 216,99)`);
log(perto(r.taxaDeducaoReal, 0.225, 1e-4), `taxa de dedução real ${Z.pct(r.taxaDeducaoReal)} (ref 22,5%)`);
log(perto(r.limpezaLiquida, 500) && r.excedenteLimpeza === 0 && perto(r.quebraValor, 162.40), "limpeza líquida 500, sem excedente, quebra por referência 162,40");
log(perto(r.variaveis, 2062.40), `variáveis = ${r.variaveis.toFixed(2)} (ref 2.062,40)`);
log(perto(r.receitaReal, 13565.60) && perto(r.receitaBrutaTotal, 17220), `receita real total ${r.receitaReal.toFixed(2)}, faturamento ${r.receitaBrutaTotal.toFixed(2)}`);
log(perto(r.margemContribuicao, 11503.20), `margem de contribuição = ${r.margemContribuicao.toFixed(2)} (ref 11.503,20)`);
log(perto(r.retirada, 3464) && perto(r.fixosOperacionais, 7234), `retirada 20 h × 40 × 4,33 = ${r.retirada.toFixed(2)}; fixos = ${r.fixosOperacionais.toFixed(2)} (ref 7.234)`);
log(perto(r.resultadoOperacional, 4269.20), `resultado operacional = ${r.resultadoOperacional.toFixed(2)} (ref 4.269,20)`);
log(perto(r.margemOperacionalPct, 0.2479, 0.0005), `margem operacional ${Z.pct(r.margemOperacionalPct)} (ref 24,8%)`);
log(r.custosModelo === 0 && perto(r.ebitda, 4269.20) && perto(r.reservaReposicao, 542.62), `reserva 4% = ${r.reservaReposicao.toFixed(2)} (ref 542,62)`);
log(perto(r.geracaoCaixa, 3726.58), `geração de caixa = ${r.geracaoCaixa.toFixed(2)} (ref 3.726,58)`);
log(perto(r.custoVariavelPorNoite, 28.32) && perto(r.custoPorNoiteVendida, 153.03, 0.05), `custo variável por noite ${r.custoVariavelPorNoite.toFixed(2)}; custo por noite vendida ${r.custoPorNoiteVendida.toFixed(2)} (ref 153,03 ± 0,05)`);
log(perto(r.margemPorNoite, 188.67, 0.02) && perto(r.pontoEquilibrioNoites, 35.4, 0.05), `margem por noite ${r.margemPorNoite.toFixed(2)}; ponto de equilíbrio ${r.pontoEquilibrioNoites.toFixed(2)} noites (ref 35,4)`);
log(perto(r.ocupacaoEquilibrio, 0.285, 0.0015), `ocupação de equilíbrio ${Z.pct(r.ocupacaoEquilibrio)} (ref 28,5%)`);
log(r.saldoFinal === 13620 && perto(r.mesesFolego, 1.88, 0.005), `saldo final ${r.saldoFinal}; fôlego ${r.mesesFolego.toFixed(2)} (ref 1,88)`);
log(r.resultadoContabilIndicativo === null, "depreciação não informada: resultado contábil indicativo não aparece");
let L = Z.leituras(r);
log(L.noite.k === "paga" && L.equilibrio.k === "folgada" && L.folego.k === "risco" && L.margem.k === "viavel" && L.caixa.k === "juntos", `leituras: ${L.noite.k}, ${L.equilibrio.k}, ${L.folego.k}, ${L.margem.k}, ${L.caixa.k}`);
let P = Z.prioridades(r, EX);
log(P.length === 1 && P[0].id === "reserva" && Z.causaPrincipal(r, EX).r === "Sem reserva para a baixa", `causa principal: ${P[0].r} (única prioridade disparada)`);
log(/Abrir uma conta separada/.test(Z.planoSugerido(P)) && !/^1\. /.test(Z.planoSugerido(P)), "plano sugerido vem da ação da prioridade; sem numeração quando é uma só");
log(perto(r.receitaPorNoiteDisponivel, 16240 / 124), "receita por noite disponível");
log(Z.nivelSeparacao(EX).n === 2 && Z.nivelSeparacao({ diag: {} }).n === 1 && Z.nivelSeparacao({ diag: { conta: "sim", custo: "sim", retirada: "sim", reserva: "sim" } }).n === 4, "nível da Linha de Separação: 2 sim → nível 2; nenhum → 1; quatro → 4");

console.log("2. Entrada com vírgula, vazio e referência Zion");
let S = { ...EX, receitaHospedagem: "16.240,00", comissoesPct: "11", processamentoPct: "1,5", impostoPct: "6", enxoval: "", noites: "58" };
r = Z.calcular(S); log(perto(r.deducoes, 3654.40) && r.N.enxoval === 0 && r.N.noites === 58, "aceita vírgula decimal e milhar; vazio vira 0");
log(Z.num("abc") === null && Z.num("") === null && Z.num(" 1.234,5 ") === 1234.5 && Z.num("12.5") === 12.5 && Z.num("R$ 300") === 300, "conversor de número: texto inválido = null; formatos brasileiro e com ponto");
S = Z.aplicarReferenciaDeducoes({ ...EX, comissoesPct: "", processamentoPct: "", impostoPct: "", cancelamentos: "" });
r = Z.calcular(S);
log(S.deducoesRef && perto(r.deducoes, 650 + 16240 * 0.17) && perto(r.N.cancelamentos, 324.80), `referência Zion: 15% + 2% da receita (+ descontos) = ${r.deducoes.toFixed(2)}`);
r = Z.calcular({ ...EX, quebra: "", quebraRef: true }); log(perto(r.quebraValor, 162.40), "quebra por referência = 1% da receita de hospedagem");
r = Z.calcular({ ...EX, quebra: "200", quebraRef: false }); log(r.quebraValor === 200 && perto(r.variaveis, 2062.40 - 162.40 + 200), "quebra em R$ substitui a referência");
r = Z.calcular({ ...EX, reservaPct: "" }); log(perto(r.reservaReposicao, 13565.60 * 0.04), "reserva vazia usa o padrão 4%");
log(Z.REF.deducoesPct + Z.REF.cancelamentosPct === 17 && Z.REF.quebraPct === 1 && Z.REF.reservaMin === 3 && Z.REF.reservaMax === 6 && /referência Zion/.test(Z.REF.nota), "parâmetros de referência: 17 = 15 + 2, quebra 1, reserva 3 a 6, marcados como referência");

console.log("3. Bordas");
r = Z.calcular({ ...EX, noites: 0, estadias: 0, receitaHospedagem: 0, taxaLimpezaCobrada: 0, outrasReceitas: 0, custoOutrasReceitas: 0, descontos: 0 });
log(r.diariaMediaReal === null && r.custoPorNoiteVendida === null && r.pontoEquilibrioNoites === null && r.taxaDeducaoReal === null && r.margemOperacionalPct === null, "noites = 0 e receita = 0: indicadores por noite e por receita = null");
L = Z.leituras(r); log(/Sem noite vendida, cada real que saiu é prejuízo/.test(L.noite.t) && L.equilibrio.k === "na" && L.margem.k === "na", "leitura de mês sem noite vendida");
log(r.resultadoOperacional < 0 && perto(r.resultadoOperacional, -(r.variaveis + 7234)), "sem venda, o resultado é o custo negativo");
r = Z.calcular({ ...EX, receitaHospedagem: 0 }); log(r.receitaRealHospedagem === 0 && r.taxaDeducaoReal === null && r.bloqueios.some((e) => /deduções/i.test(e)), "receita 0 com descontos em R$: deduções passam da receita e bloqueiam");
let v = Z.validar({ ...EX, descontos: 20000 }, "entrou"); log(!v.ok && /passam da receita/.test(v.erros[0]), "deduções > receita bloqueia a tela 'o que entrou'");
r = Z.calcular({ ...EX, descontos: 20000 }); log(r.receitaRealHospedagem === 0 && r.deducoesAcimaDaReceita, "receita real nunca fica abaixo de zero");
r = Z.calcular({ ...EX, taxaLimpezaCobrada: 2500 });
log(r.limpezaLiquida === 0 && r.excedenteLimpeza === 500 && perto(r.outrasReceitasTotal, 1480) && perto(r.receitaBrutaTotal, 17720), "limpeza cobrada > paga: excedente de 500 vai a outras receitas");
log(Z.validar({ ...EX, taxaLimpezaCobrada: 2500 }, "entrou").avisos.some((a) => /excedente/.test(a)), "aviso de excedente de limpeza");
r = Z.calcular({ ...EX, taxaLimpezaCobrada: 1200 }); log(r.limpezaLiquida === 800 && r.excedenteLimpeza === 0 && perto(r.variaveis, 2362.40), "limpeza cobrada < paga: diferença fica no custo variável");
r = Z.calcular({ ...EX, estadias: 0 }); v = Z.validar({ ...EX, estadias: 0 }, "mes");
log(r.estadiasAssumidas && r.estadiasUsadas === 58 && r.mediaNoitesPorEstadia === 1 && v.ok && /assume uma estadia por noite/.test(v.avisos[0]), "estadias = 0: assume estadias = noites, média 1 e avisa sem bloquear");
v = Z.validar({ ...EX, noites: 125 }, "mes"); log(!v.ok && /passam das noites disponíveis/.test(v.erros[0]), "noites > unidades × dias bloqueia");
v = Z.validar({ ...EX, noites: 124 }, "mes"); log(v.ok, "noites = disponíveis passa");
v = Z.validar({ ...EX, enxoval: -5 }, "variaveis"); log(!v.ok && /negativo/.test(v.erros[0]), "valor negativo bloqueia");
v = Z.validar({ ...EX, comissoesPct: 100 }, "entrou"); log(!v.ok && /0 a 99,9/.test(v.erros[0]), "percentual acima de 99,9 bloqueia");
v = Z.validar({ ...EX, dias: 27 }, "mes"); log(!v.ok && /mínimo é 28/.test(v.erros[0]) && !Z.validar({ ...EX, dias: 32 }, "mes").ok && !Z.validar({ ...EX, unidades: 0 }, "mes").ok, "dias fora de 28 a 31 e unidades 0 bloqueiam");
v = Z.validar({ ...EX, enxoval: "abc" }, "variaveis"); log(!v.ok && /só números/.test(v.erros[0]), "texto num campo numérico bloqueia");
v = Z.validar({ ...EX, dias: "", unidades: "", noites: "" }, "mes"); log(!v.ok && v.erros.length === 3, "campos obrigatórios vazios bloqueiam a tela do mês");
v = Z.validar({ ...EX, retiradaHoras: -2 }, "fixos"); log(!v.ok, "horas negativas na Conta da Retirada bloqueiam");
r = Z.calcular({ ...EX, retiradaModo: "valor", retirada: "3.464,00" }); log(perto(r.retirada, 3464), "retirada em valor direto");

console.log("4. Retirada zero: decidida ou não");
r = Z.calcular({ ...EX, retiradaModo: "valor", retirada: "0", retiradaDecidida: false });
P = Z.prioridades(r, {}); log(P.map((p) => p.id).join(",") === "reserva,retirada", `retirada 0 sem decisão → prioridades ${P.map((p) => p.id).join(", ")}`);
r = Z.calcular({ ...EX, retiradaModo: "valor", retirada: "", retiradaDecidida: true });
P = Z.prioridades(r, {}); log(P.map((p) => p.id).join(",") === "reserva" && r.N.informado.retirada, "retirada 0 decidida → não dispara e conta como informada");
r = Z.calcular({ ...EX, retiradaModo: "horas", retiradaHoras: 20, retiradaValorHora: 40, retiradaDecidida: true }); log(r.retirada === 0, "decisão de retirada zero sobrepõe a calculadora");

console.log("5. Prioridades na ordem da fonte e limite de três");
S = { ...EX, duodecimos: 0, retiradaModo: "valor", retirada: 0, retiradaDecidida: false, descontos: 9000 };
r = Z.calcular(S); P = Z.prioridades(r, S);
log(P.length === 3 && P.map((p) => p.id).join(",") === "duodecimos,reserva,retirada", `até três, na ordem: ${P.map((p) => p.id).join(", ")}`);
log(/^1\. /.test(Z.planoSugerido(P)) && Z.planoSugerido(P).split("\n").length === 3, "plano sugerido numerado com três linhas");
log(Z.comoVerificar(P).length > 50, "como verificar junta as verificações");
S = { ...EX, reservasSeparadas: 5000, descontos: 9000 }; r = Z.calcular(S); P = Z.prioridades(r, S);
log(P[0].id === "diaria" && P.some((p) => p.id === "deducoes"), `diária abaixo do custo (${Z.brl(r.diariaMediaReal)} < ${Z.brl(r.custoPorNoiteVendida)}) e deduções ${Z.pct(r.taxaDeducaoReal)} > 25%: ${P.map((p) => p.id).join(", ")}`);
S = { ...EX, reservasSeparadas: 5000, enxoval: 6000 }; r = Z.calcular(S); P = Z.prioridades(r, S);
log(P.some((p) => p.id === "variavel") && r.custoVariavelPorNoite >= 0.5 * r.diariaMediaReal, "custo variável ≥ metade da diária real dispara");
S = { ...EX, reservasSeparadas: 5000, equipe: 12000 }; r = Z.calcular(S); P = Z.prioridades(r, S);
log(P.some((p) => p.id === "equilibrio") && r.ocupacaoEquilibrio > 0.70, `ocupação de equilíbrio ${Z.pct(r.ocupacaoEquilibrio)} > 70% dispara`);
S = { ...EX, reservasSeparadas: 5000 }; r = Z.calcular(S); P = Z.prioridades(r, S);
log(P.length === 1 && P[0].id === "ok" && /mesmo mês do ano anterior/.test(P[0].acao), "nada dispara → mês dentro das réguas");

console.log("6. Faixas das leituras nos limites");
const base = Z.calcular(EX);
const comEq = (o) => Z.leituras({ ...base, naoFecha: false, ocupacaoEquilibrio: o }).equilibrio.k;
log(comEq(0.701) === "alerta" && comEq(0.70) === "limite" && comEq(0.651) === "limite" && comEq(0.65) === "saudavel" && comEq(0.45) === "saudavel" && comEq(0.449) === "folgada", "ocupação de equilíbrio: 70% / 65% / 45%");
log(Z.leituras({ ...base, naoFecha: true, ocupacaoEquilibrio: null }).equilibrio.k === "naofecha", "margem por noite ≤ 0 → não fecha");
const comF = (f) => Z.leituras({ ...base, mesesFolego: f }).folego.k;
log(comF(1.99) === "risco" && comF(2) === "apertado" && comF(3.99) === "apertado" && comF(4) === "confortavel" && comF(6) === "confortavel" && comF(6.01) === "muito" && comF(null) === "na", "fôlego: 2 / 4 / 6 e não calculável");
const comM = (m) => Z.leituras({ ...base, margemOperacionalPct: m }).margem.k;
log(comM(0.301) === "boa" && comM(0.30) === "viavel" && comM(0.20) === "viavel" && comM(0.199) === "apertada" && comM(0.10) === "apertada" && comM(0.099) === "naofecha", "margem: 30 / 20 / 10");
const comN = (d, cv, ct) => Z.leituras({ ...base, diariaMediaReal: d, custoVariavelPorNoite: cv, custoPorNoiteVendida: ct }).noite.k;
log(comN(153.03, 28.32, 153.03) === "paga" && comN(100, 28.32, 153.03) === "ajuda" && comN(28.32, 28.32, 153.03) === "ajuda" && comN(20, 28.32, 153.03) === "consome", "diária real × custo por noite: três leituras");

console.log("7. Caixa × resultado (quatro combinações)");
const comC = (varCaixa, res) => Z.leituras({ ...base, variacaoCaixa: varCaixa, resultadoOperacional: res }).caixa.k;
log(comC(1000, -500) === "caixa-bom" && /alta temporada|repasse/.test(Z.leituras({ ...base, variacaoCaixa: 1000, resultadoOperacional: -500 }).caixa.t), "saldo subiu e resultado negativo");
log(comC(-1000, 500) === "resultado-bom" && comC(0, 500) === "resultado-bom", "saldo caiu (ou parado) e resultado positivo");
log(comC(-1000, -500) === "dois" && /dois alertas/.test(Z.leituras({ ...base, variacaoCaixa: -1000, resultadoOperacional: -500 }).caixa.t), "ambos negativos");
log(comC(1000, 500) === "juntos", "ambos positivos");
log(/a receber/.test(Z.leituras(Z.calcular({ ...EX, aReceber: 900 })).caixa.t), "a receber aparece na leitura do caixa");

console.log("8. Regra do desconto em três faixas");
log(Z.faixaDesconto(160, base).k === "pode" && Z.faixaDesconto(153.05, base).k === "pode", "diária com desconto acima do custo por noite vendida: pode");
log(Z.faixaDesconto(100, base).k === "so-vazia" && Z.faixaDesconto(28.32, base).k === "so-vazia", "entre o variável e o custo total: só para noite vazia");
log(Z.faixaDesconto(20, base).k === "nao" && Z.faixaDesconto("abc", base).k === "na" && Z.faixaDesconto(100, Z.calcular({ ...EX, noites: 0 })).k === "na", "abaixo do variável: não; sem custo: não avalia");

console.log("9. Completo e concluído");
log(Z.completo(EX), "exemplo está completo");
log(!Z.completo({ ...EX, receitaHospedagem: 0 }) && Z.completo({ ...EX, receitaHospedagem: 0, descontos: 0, situacao: "abrir" }), "receita 0 só passa para quem vai abrir");
log(!Z.completo({ ...EX, saldoInicial: "" }) && !Z.completo({ ...EX, noites: "" }) && !Z.completo({ ...EX, situacao: "" }), "falta de caixa, noites ou situação deixa incompleto");
log(!Z.completo({ ...EX, retiradaHoras: "", retiradaValorHora: "" }) && Z.completo({ ...EX, retiradaHoras: "", retiradaValorHora: "", retiradaDecidida: true }), "retirada precisa ser informada ou decidida como zero");
log(!Z.completo({ ...EX, limpezaPaga: "", enxoval: "", amenidades: "", energiaVariavel: "", cafe: "", quebra: "", quebraRef: false, outrosVariaveis: "" }), "sem nenhum custo variável fica incompleto");
log(!Z.completo({ ...EX, noites: 200 }), "bloqueio deixa incompleto");
const C = { ...EX, acao: "Abrir a conta de reservas e programar a transferência.", prazo: "2026-12-10", pdf: "2026-11-08T10:00:00Z" };
log(Z.concluido(C) && !Z.concluido({ ...C, pdf: "" }) && !Z.concluido({ ...C, prazo: "" }) && !Z.concluido({ ...C, acao: "curta" }), "concluído exige ação (10+ letras), prazo e PDF baixado");
log(Z.pendencias({ ...C, pdf: "" }).length === 1 && Z.pendencias({}).length === 4, "pendências listam o que falta");

console.log("10. Integridade dos dados e textos");
log(Z.CAMPOS.length === 40 && Z.CAMPOS.every((c) => c.r && c.pq && c.onde && c.ex && c.tela), `${Z.CAMPOS.length} campos, todos com rótulo, por que, onde conseguir e exemplo`);
log(Z.TELAS.length === 8 && ["mes", "entrou", "variaveis", "fixos", "modelo", "caixa"].every((t) => Z.CAMPOS.some((c) => c.tela === t) && Z.TITULOS[t]), "8 telas; cada tela de dados tem campos e título");
log(Z.DIAG.length === 4 && Z.NIVEIS.length === 4 && Z.REGRAS.length === 7 && Z.REGRAS.every((g) => g.acao.length > 30 && g.verifica.length > 20), "4 perguntas, 4 níveis, 7 regras com ação e verificação");
log(Z.cascata(base).length === 13 && Z.indicadores(base).length === 10 && Z.indicadores(base).every((i) => i.v && i.v !== "—"), "cascata com 13 linhas e 10 indicadores preenchidos no exemplo");
log(Z.brl(1234.5) === "R$ 1.234,50" && Z.brl(-3.2) === "−R$ 3,20" && Z.brl(null) === "—" && Z.pct(0.2853) === "28,5%" && Z.dec(1.88, 1) === "1,9", "formatação brasileira");
const proibidas = /garant|retorno garantido|lucro certo|renda extra|valoriza/i;
const textos = JSON.stringify(Z, (k, v) => (typeof v === "function" ? v.toString() : v));
log(!proibidas.test(textos), "nenhuma promessa proibida nos textos");
log(!/\b(DRE|EBITDA|KPI|ADR|RevPAR)\b/.test(textos), "nenhuma sigla nos textos da ficha");
log(/dados fictícios|exemplo/i.test(EX.hospedagem) && /Outubro/.test(EX.mes), "exemplo rotulado como exemplo");

// Modo da retirada sem gravação: a tela mostra "Calcular por horas" marcado, então a lógica tem de assumir horas.
{ const S = { ...EX, retiradaModo: undefined, retiradaHoras: "20", retiradaValorHora: "40", retirada: "" }; const r = Z.calcular(S);
  log(Math.abs(r.retirada - 20 * 40 * 4.33) < 0.01, "retirada por horas vale mesmo sem retiradaModo gravado (" + r.retirada.toFixed(2) + ")"); }
{ const S = { ...EX, retiradaModo: "valor", retirada: "3000", retiradaHoras: "20", retiradaValorHora: "40" }; const r = Z.calcular(S);
  log(r.retirada === 3000, "retiradaModo valor usa o valor informado"); }

console.log(`\n${ok} ok, ${fal} falhou`); process.exit(fal ? 1 : 0);

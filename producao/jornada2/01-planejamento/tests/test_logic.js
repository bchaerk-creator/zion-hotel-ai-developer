// Testes da lógica pura da ficha "O meu Painel de Gestão". Uso: node tests/test_logic.js
const Z = require("../src/logic.js");
let ok = 0, fal = 0;
const t = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
const perto = (a, b, tol = 1e-6) => a != null && Math.abs(a - b) <= tol;
const EX = Z.EXEMPLO;
const com = (o) => Object.assign({}, EX, { diag: Object.assign({}, EX.diag) }, o);

console.log("Conversão de números");
t(Z.num("16.240,00") === 16240 && Z.num("1234.56") === 1234.56 && Z.num(" R$ 280 ") === 280, "aceita formato brasileiro, ponto decimal e R$");
t(Z.num("-500") === -500 && Z.num("−1.200,50") === -1200.5, "aceita negativo (inclusive sinal tipográfico)");
t(Z.num("") === null && Z.num("abc") === null && Z.num("12a") === null && Z.num(null) === null, "vazio e texto viram null");
t(Z.num("46,8%") === 46.8, "aceita o símbolo de percentual");
t(Z.num("13.000") === 13000 && Z.num("1.234.567") === 1234567 && Z.num("4.7") === 4.7 && Z.num("12.5") === 12.5, "ponto de milhar sem vírgula (13.000 = treze mil); ponto decimal mantido (4.7)");

console.log("Nível do painel (4 perguntas)");
t(Z.nivelPainel({ diag: {} }).n === 1 && Z.nivelPainel({ diag: { painel: "sim" } }).n === 1, "zero ou um sim = nível 1");
t(Z.nivelPainel({ diag: { painel: "sim", metas: "sim" } }).n === 2 && Z.nivelPainel({ diag: { painel: "sim", metas: "sim", donos: "sim" } }).n === 3, "dois sim = 2; três sim = 3");
t(Z.nivelPainel({ diag: { painel: "sim", metas: "sim", donos: "sim", reuniao: "sim" } }).r === "Painel com rotina", "quatro sim = Painel com rotina");
t(Z.nivelPainel(EX).r === "Sem painel", "exemplo (quatro não) = Sem painel");

console.log("Os cinco indicadores vêm do Pilar G7");
t(Z.IND.map((i) => i.id).join(",") === "ocupacao,diaria,resultado,nota,vendaDireta", "ocupação, diária média, resultado, nota e taxa de venda direta, nessa ordem");
t(Z.IND.every((i) => i.def && i.onde && i.ex && i.exMeta), "cada indicador tem definição, onde conseguir e exemplo");

console.log("Exemplo didático · dados fictícios (Cabanas do Vale)");
const r = Z.calcular(EX);
t(r.noitesDisponiveis === 124, "31 dias × 4 unidades = 124 noites disponíveis");
t(perto(r.noitesMeta, 62) && perto(r.receitaMeta, 18600), "metas pedem 62 noites e R$ 18.600 de hospedagem (50% × 124 × R$ 300)");
t(perto(r.receitaPorNoiteDispBase, 131.04) && perto(r.receitaPorNoiteDispMeta, 150), "receita por noite disponível: R$ 131,04 → R$ 150,00");
t(perto(r.variacaoReceita, 150 / 131.04 - 1) && Z.pct(r.variacaoReceita) === "14,5%", "variação da receita pedida = 14,5%");
t(r.sabidos === 5, "sabe os cinco números do ponto de partida");
const pn = Z.painel(r);
t(pn[0].base === "46,8%" && pn[0].meta === "50,0%" && pn[0].variacao === "+ 3,2 pontos", "ocupação 46,8% → 50,0% (+ 3,2 pontos)");
t(pn[1].base === "R$ 280,00" && pn[1].meta === "R$ 300,00" && pn[1].variacao === "+ R$ 20,00 (+7,1%)", "diária R$ 280 → R$ 300 (+7,1%)");
t(pn[2].base === "R$ 11.890,00" && pn[2].meta === "R$ 13.000,00" && pn[2].variacao === "+ R$ 1.110,00 (+9,3%)", "resultado R$ 11.890 → R$ 13.000 (+9,3%)");
t(pn[3].base === "4,7 de 5" && pn[3].meta === "4,8 de 5" && pn[3].variacao === "+ 0,1 ponto (+2,1%)", "nota 4,7 → 4,8 de 5");
t(pn[4].base === "30,0%" && pn[4].meta === "40,0%" && pn[4].variacao === "+ 10,0 pontos", "venda direta 30% → 40% (+ 10 pontos)");
t(pn.every((l) => l.dono === "Ana" && l.leitura === "meta acima do ponto de partida"), "cinco donos (Ana) e cinco metas acima do ponto de partida");
const at = Z.atencao(r, EX);
t(at.length === 1 && at[0].id === "semRetirada", "atenção no exemplo: só o resultado sem a retirada");
const le = Z.leituras(r, EX);
t(/62 noites vendidas e R\$ 18\.600,00/.test(le[1]) && /14,5% acima/.test(le[1]), "leitura do que as metas pedem");
t(/mesmo mês daqui a 12 meses \(o mês de partida é Outubro de 2026\)/.test(le[2]) && /junho contra junho/.test(le[2]), "leitura: meta vale para o mesmo mês, comparar junho contra junho");
const plano = Z.planoSugerido(EX, r);
t(plano.split("\n").length === 4 && /^1\. Marcar na agenda a reunião semanal: toda segunda-feira às 08:00, 30 minutos/.test(plano), "plano sugerido: reunião + três pilares");
t(/2\. Semanas 1 e 2: Módulo 2 · Finanças/.test(plano) && /3\. Semanas 3 e 4: Módulo 3/.test(plano) && /4\. Semanas 5 e 6: Módulo 4/.test(plano), "plano segue as semanas 1-2, 3-4, 5-6");
t(/refeito com a retirada dentro/.test(Z.comoVerificar(r, EX)) && /quatro linhas/.test(Z.comoVerificar(r, EX)), "como verificar: quatro reuniões e o resultado refeito");
t(Z.completo(EX) && !Z.concluido(EX), "exemplo completo, mas não concluído sem plano, data e PDF");

console.log("Validação · ponto de partida");
t(!Z.validar(com({ mesBase: "" }), "partida").ok, "sem mês de partida bloqueia");
t(!Z.validar(com({ dias: 32 }), "partida").ok && !Z.validar(com({ dias: 27 }), "partida").ok && !Z.validar(com({ dias: "30,5" }), "partida").ok, "dias fora de 28 a 31 ou fracionado bloqueia");
t(!Z.validar(com({ unidades: 0 }), "partida").ok && !Z.validar(com({ unidades: -2 }), "partida").ok, "unidades zero ou negativas bloqueiam");
t(/0 a 100/.test(Z.validar(com({ base_ocupacao: "120" }), "partida").erros.join()), "ocupação acima de 100% bloqueia");
t(/negativo/.test(Z.validar(com({ base_diaria: "-10" }), "partida").erros.join()), "diária negativa bloqueia");
t(Z.validar(com({ base_resultado: "-2.500,00" }), "partida").ok, "resultado negativo é aceito (mês no prejuízo)");
t(/0 a 5/.test(Z.validar(com({ base_nota: "6" }), "partida").erros.join()) && Z.validar(com({ base_nota: "9,2", escalaNota: "10" }), "partida").ok, "nota respeita a escala (5 ou 10)");
t(/só números/.test(Z.validar(com({ base_vendaDireta: "doze" }), "partida").erros.join()), "texto no lugar de número bloqueia");
const semBase = com({ base_nota: "", base_vendaDireta: "" });
const vb = Z.validar(semBase, "partida");
t(vb.ok && /nota das avaliações, taxa de venda direta/.test(vb.avisos.join()) && /não sei/.test(vb.avisos.join()), "não sei é aceito, com aviso");

console.log("Validação · metas");
t(/Falta a meta de ocupação/.test(Z.validar(com({ meta_ocupacao: "" }), "metas").erros.join()), "meta é obrigatória nos cinco indicadores");
t(/maior que zero/.test(Z.validar(com({ meta_ocupacao: "0" }), "metas").erros.join()) && /maior que zero/.test(Z.validar(com({ meta_diaria: "0" }), "metas").erros.join()), "meta de ocupação ou diária zero bloqueia");
t(!Z.validar(com({ meta_vendaDireta: "101" }), "metas").ok && !Z.validar(com({ meta_nota: "5,1" }), "metas").ok, "meta fora da faixa bloqueia");
t(Z.validar(com({ meta_resultado: "-1000" }), "metas").ok, "meta de resultado negativa é aceita (reduzir prejuízo)");
t(!Z.validar(com({ ocupacaoEquilibrio: "130" }), "metas").ok && !Z.validar(com({ numeroCorte: "x" }), "metas").ok, "ocupação de equilíbrio e número de corte validados");

console.log("Validação · donos, reunião, seis semanas");
t(/Falta o dono de nota das avaliações/.test(Z.validar(com({ dono_nota: " " }), "donos").erros.join()), "indicador sem dono bloqueia (indicador sem dono é arquivado)");
t(!Z.validar(com({ reuniaoDia: "" }), "reuniao").ok && !Z.validar(com({ reuniaoHora: "25:00" }), "reuniao").ok && !Z.validar(com({ reuniaoHora: "8h" }), "reuniao").ok, "dia e hora obrigatórios, hora válida");
t(!Z.validar(com({ reuniaoDuracao: "5" }), "reuniao").ok && !Z.validar(com({ reuniaoDuracao: "200" }), "reuniao").ok, "duração de 10 a 120 minutos");
const longa = Z.validar(com({ reuniaoDuracao: "45" }), "reuniao");
t(longa.ok && /trinta minutos/.test(longa.avisos.join()), "reunião de 45 minutos passa com aviso da fonte");
t(/três pilares diferentes/.test(Z.validar(com({ s34: "2" }), "seis").erros.join()), "pilares repetidos bloqueiam (escolha três e faça bem)");
t(!Z.validar(com({ s56: "" }), "seis").ok && !Z.validar(com({ s12: "9" }), "seis").ok, "os três pilares são obrigatórios e da lista");
t(/evita culpa/.test(Z.validar(com({ depois: "" }), "seis").avisos.join()) && Z.validar(com({ depois: "" }), "seis").ok, "o que deixar para depois: aviso, não bloqueio");

console.log("Atenção · regras");
const ids = (o) => Z.atencao(Z.calcular(com(o)), com(o)).map((a) => a.id);
t(ids({ resultadoSemRetirada: false }).length === 0, "sem alerta quando o resultado já tem a retirada");
t(ids({ ocupacaoEquilibrio: "55" }).includes("equilibrio") && !ids({ ocupacaoEquilibrio: "28,5" }).includes("equilibrio"), "meta de ocupação abaixo do equilíbrio (55%) alerta; 28,5% não");
t(ids({ numeroCorte: "15000" }).includes("corte") && !ids({ numeroCorte: "2000" }).includes("corte"), "meta de resultado abaixo do número de corte alerta");
t(ids({ base_nota: "" }).includes("semBase"), "sem ponto de partida alerta");
t(ids({ meta_ocupacao: "40" }).includes("abaixo") && /ocupação é vaidade/.test(Z.atencao(Z.calcular(com({ meta_ocupacao: "40" })), com({ meta_ocupacao: "40" })).find((a) => a.id === "abaixo").t), "meta abaixo do ponto de partida alerta, com o estudo de caso");
t(Z.calcular(com({ meta_diaria: "280" })).L.diaria.situacao === "igual" && Z.painel(Z.calcular(com({ meta_diaria: "280" })))[1].variacao === "manter", "meta igual ao ponto de partida = manter");
t(ids({ quem: "equipe" }).includes("donoUnico") && !ids({ quem: "so" }).includes("donoUnico") && !ids({ quem: "equipe", dono_nota: "Carla" }).includes("donoUnico"), "cinco números com a mesma pessoa só alerta quando há equipe");
t(ids({ reuniaoDuracao: "60" }).includes("longa"), "reunião acima de 30 minutos entra na atenção");
t(/série histórica/.test(Z.ERRO_COMUM), "erro comum da fonte sempre disponível");

console.log("Sem ponto de partida e metas parciais");
const s2 = com({ base_ocupacao: "", base_diaria: "", base_resultado: "", base_nota: "", base_vendaDireta: "", resultadoSemRetirada: false });
const r2 = Z.calcular(s2);
t(r2.sabidos === 0 && r2.variacaoReceita === null && perto(r2.receitaMeta, 18600), "sem base: sem variação, mas a receita pedida existe");
t(/sabe 0 de 5/.test(Z.leituras(r2, s2)[0]) && Z.painel(r2).every((l) => l.base === "não sei" && l.variacao === "sem ponto de partida"), "leitura e painel mostram não sei");
t(/Na primeira reunião, anotar o ponto de partida que falta/.test(Z.planoSugerido(s2, r2)) && Z.planoSugerido(s2, r2).split("\n").length === 5, "plano ganha o passo de anotar a base");
t(Z.calcular(com({ base_resultado: "0", meta_resultado: "1000" })).L.resultado.variacaoPct === null, "resultado base zero: variação em R$, sem percentual");
t(Z.valor("brlneg", -2500) === "−R$ 2.500,00" && Z.valor("nota", 9.2, 10) === "9,2 de 10", "formatação de negativo e nota de 10");

console.log("Conclusão (selo)");
const fim = com({ acao: Z.planoSugerido(EX), prazo: "2026-11-16", pdf: "2026-11-10T12:00:00Z" });
t(Z.concluido(fim), "painel completo + plano + data + PDF = pronto para avançar");
t(!Z.concluido(com({ acao: "curta", prazo: "2026-11-16", pdf: "x" })) && /10 letras/.test(Z.pendencias(com({ acao: "curta" })).join()), "plano curto demais não conclui");
t(!Z.concluido(com({ acao: Z.planoSugerido(EX), pdf: "x" })) && /primeira reunião/.test(Z.pendencias(com({})).join()), "sem a data da primeira reunião não conclui");
t(!Z.concluido(com({ acao: Z.planoSugerido(EX), prazo: "2026-11-16" })), "sem PDF não conclui");
t(!Z.completo(com({ quem: "" })) && !Z.completo(com({ situacao: "" })), "sem situação ou sem quem cuida não está completo");
t(Z.proximaVazia(com({ dono_ocupacao: "" })) === "donos" && Z.proximaVazia(EX) === "resultado", "continuar de onde parei leva à primeira tela incompleta");

console.log("Leitura da Folha Única (Módulo 2)");
let ZF = null; try { ZF = require("../../02-financas/src/logic.js"); } catch (e) {}
if (ZF) {
  const f = Z.daFolha(Object.assign({}, ZF.EXEMPLO), ZF);
  t(f && f.base_ocupacao === 46.8 && f.base_diaria === 280 && f.base_resultado === 4269.2 && f.ocupacaoEquilibrio === 28.5 && f.resultadoSemRetirada === false, "da Folha do exemplo: ocupação 46,8, diária 280, resultado 4.269,20 com a retirada, equilíbrio 28,5%");
  t(Z.daFolha({ mes: "x" }, ZF) === null && Z.daFolha(null, ZF) === null, "Folha incompleta ou ausente não sugere nada");
} else t(false, "logic.js do Módulo 2 não encontrado");

console.log(`\n${ok} ok, ${fal} falhou`); process.exit(fal ? 1 : 0);

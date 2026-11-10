// Testes da lógica do Montador do Plano de Gestão (Módulo 7). Uso: node tests/test_logic.js
const fs = require("fs"), path = require("path");
const Z = require("../src/logic.js");
const D = path.resolve(__dirname, "../../../../docs/trilha2");
let ok = 0, fal = 0; const log = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
const perto = (a, b, tol) => a != null && Math.abs(a - b) <= (tol == null ? 0.0005 : tol);
const copia = (o) => JSON.parse(JSON.stringify(o));
const EX = Z.exemplo();
// Estados de exemplo das sete páginas anteriores (os exemplos didáticos de cada módulo, com o PDF gerado)
const MODS = {}; Z.PAGINAS.slice(0, 7).forEach((p) => { try { MODS[p.slug] = require(path.join(D, p.slug, "logic.js")); } catch (e) { MODS[p.slug] = null; } });
const MZ = { situacao: "dono", quem: "so", tipo: "Cabanas ou chalés", unidades: "4", hospedagem: "Cabanas do Vale (exemplo)", cinco: { entrou: 2, sobrou: 0, ocupacao: 1, diaria: 2, custo: 0 },
  areas: { metas: 0, financas: 1, preco: 1, vendas: 2, pessoas: 1, compras: 2, operacao: 1, qualidade: 0 }, rotina: "as-vezes", tempo: "operacao", saida: "acho", prazo: "2026-12-15", pdf: "2026-11-09T10:00:00.000Z" };
const EST = { "marco-zero": MZ };
Z.PAGINAS.slice(1, 7).forEach((p) => { const m = MODS[p.slug]; if (m) EST[p.slug] = Object.assign({}, m.EXEMPLO || m.exemplo(), { nome: "Ana Exemplo", pdf: "2026-11-09T12:00:00.000Z" }); });
const PG = Z.paginas(EST);

console.log("1. Exemplo didático (Cabanas do Vale, dados fictícios, PLANO seção 9)");
Z.TELAS.slice(0, -1).forEach((t) => { const v = Z.validar(EX, t); log(v.ok && v.avisos.length === 0, `tela ${t} do exemplo valida sem erro nem aviso` + (v.erros.length ? ": " + v.erros.join(" | ") : "") + (v.avisos.length ? " avisos: " + v.avisos.join(" | ") : "")); });
let r = Z.calcular(EX, PG);
log(r.notaAtual === 4.7 && r.notaMeta === 4.8 && r.notaMin === 4.7 && r.gapMeta === 0.1 && !r.abaixoMin, "nota 4,7, meta 4,8 (Módulo 1), mínima 4,7 (Módulo 5): falta 0,1 ponto e não está abaixo da mínima");
log(perto(r.apos3, 181.6 / 39) && Z.dec(r.apos3, 2) === "4,66", "38 avaliações: uma de 3 leva a média a 4,66 ((4,7 × 38 + 3) ÷ 39)");
log(perto(r.taxa, 25 / 72) && Z.pct(r.taxa, 1) === "34,7%" && r.taxaBaixa, "taxa de avaliação 25 ÷ 72 = 34,7%, abaixo dos 40%");
log(r.difConc === 0.1 && r.dimensao.v === "limpeza" && r.dimensaoNota === 4.6, "0,1 ponto acima dos concorrentes; dimensão mais baixa: limpeza 4,6");
log(r.produto && r.repeticoes === 3 && !r.respostaLenta, "crítica repetida 3 vezes = problema de produto; resposta de 40 min dentro dos 60");
log(r.padrao.length === 7 && r.padrao.every((p) => p.ok), "padrão mínimo com as 7 regras definidas");
log(r.padrao[5].v === "Trocar o sifão do chuveiro da cabana 3 e incluir o ralo no checklist de limpeza · até 30/11/2026", "ajuste de produto com prazo 30/11/2026");
const F = r.fases.lista;
log(F[0].de === "2026-11-16" && F[0].ate === "2027-01-10" && F[1].de === "2027-01-11" && F[1].ate === "2027-03-07", "Fase 1: 16/11/2026 a 10/01/2027; Fase 2: 11/01 a 07/03/2027");
log(F[2].de === "2027-03-08" && F[2].ate === "2027-06-13" && F[2].semanas === 14 && r.fases.f3ok, "Fase 3: 08/03 a 13/06/2027, 14 semanas (pelo menos 8)");
log(F[3].de === "2027-06-14" && F[3].ate === "2027-06-27" && r.teste.ate === "2027-06-27", "teste das duas semanas: 14/06 a 27/06/2027");
log(r.fases.totalDias === 224 && r.fases.meses === 7.4 && r.fases.noPrazo, "do início ao teste: 224 dias = 7,4 meses, dentro dos 6 a 8 da fonte");
log(r.rotina.trimestral.join() === "2027-01-11,2027-04-11,2027-07-11,2027-10-11" && r.rotina.anual === "2027-11-08", "trimestrais 11/01, 11/04, 11/07, 11/10/2027; anual 08/11/2027");
log(r.rotina.semanal[0].q === "Segunda-feira, 08:00" && r.rotina.semanal[1].q === "Segunda-feira" && r.rotina.mensal[0].q === "dia 5", "rotina: reunião segunda 08:00 (Módulo 1), painel segunda (Módulo 5), Folha no dia 5");
log(r.condOk === 1 && r.segunda.r === "Agora não" && /Faltam 3 de 4/.test(r.segunda.t), "segunda unidade: 1 de 4 condições, agora não");
log(r.tempoSobra.v === "negocio" && r.veredito === null, "tempo que sobra: trabalhar sobre o negócio; teste ainda não feito");
log(r.presentes === 7 && r.itens.every((i) => i.ok) && r.prontos === 7, "com as sete páginas prontas, os 7 itens do critério estão prontos");
log(!Z.concluido(EX, PG) && Z.pendencias(EX, PG).join() === "baixar o PDF do Plano completo", "sem o PDF do Plano, falta só baixar");
log(Z.concluido(Object.assign(copia(EX), { pdf: "2026-11-10" }), PG), "com o PDF: concluído");
const L = Z.leituras(r, EX);
log(L.titulo === "As oito páginas do seu Plano estão juntas" && L.nota === "Nota 4,7 de 5, com 38 avaliações; meta de 4,8 de 5 (faltam 0,1 ponto).", "leitura principal: oito páginas juntas; nota, volume e meta");
log(L.atencao.map((a) => a.id).join() === "produto,taxa", "atenção na ordem: crítica repetida, depois taxa de avaliação");
log(/7,4 meses \(16\/11\/2026 a 27\/06\/2027\), dentro dos seis a oito meses/.test(L.saida) && /14\/06\/2027/.test(L.verificar), "leituras do plano de saída e do como verificar com as datas");
log(L.fazer.length === 4 && /30\/11\/2026/.test(L.fazer[0]) && /segunda-feira às 08:00/.test(L.fazer[2]), "o que fazer: ajuste até 30/11, rotina na segunda às 08:00, Fase 1");

console.log("2. As páginas anteriores, lidas do mesmo aparelho");
log(Z.paginas({}).every((p) => p.estado === "falta") && Z.rotuloEstado(Z.paginas({})[0]) === "Página ainda não feita", "sem nenhuma chave: todas 'página ainda não feita'");
const parcial = Z.paginas({ "marco-zero": MZ, financas: { situacao: "dono" }, marketing: null, compras: {} });
log(parcial[0].estado === "pronta" && parcial[0].quando === "2026-11-09" && parcial[2].estado === "andamento" && parcial[4].estado === "falta" && parcial[6].estado === "falta", "pronta (com PDF), em andamento (sem PDF), falta (sem chave ou vazia)");
log(parcial[0].link === "../marco-zero/" && parcial[4].chave === "zion-t2-marketing" && Z.rotuloEstado(parcial[2]) === "Em andamento · falta chegar ao PDF", "link e chave de cada ficha; rótulo do andamento");
const rp = Z.calcular(EX, parcial);
log(rp.presentes === 1 && !rp.itens[0].ok && Z.pendencias(EX, parcial)[0] === "terminar as páginas 1, 2, 3, 4, 5, 6 (fichas dos módulos)", "faltando páginas: item 1 pendente com a lista");
const Lp = Z.leituras(rp, EX);
log(Lp.titulo === "Faltam 6 de 8 páginas para fechar o Plano" && Lp.atencao[0].id === "paginas" && /2 · Folha Única do Mês \(em andamento\)/.test(Lp.atencao[0].t), "leitura: faltam 6 de 8; atenção começa pelas páginas que faltam");
const A = Z.daAnteriores(EST);
log(A.nome === "Ana Exemplo" && A.hospedagem === "Cabanas do Vale (exemplo)" && A.situacao === "dono", "nome, hospedagem e situação vindos das fichas anteriores");
if (MODS.planejamento && MODS.pessoas) log(A.notaAtual === "4,7" && A.notaMeta === "4,8" && A.escala === "5" && A.reuniaoDia === "segunda" && A.reuniaoHora === "08:00", "do Painel de Gestão (Módulo 1): nota 4,7, meta 4,8, segunda 08:00");
if (MODS.pessoas) log(A.notaMin === "4,7" && A.painelDia === "segunda" && A.inicioF1 === "2026-11-16", "do Mapa de Pessoas (Módulo 5): nota mínima 4,7, painel na segunda, início em 16/11/2026");
if (MODS.preco) log(A.metaDireta === 40 && A.prazoDireta === "2027-06-30", "da Tabela de Preço (Módulo 3): venda direta 40% até 30/06/2027");

console.log("3. Resumo de cada página no Plano em PDF");
const R = (n) => Z.resumoPagina(n, EST[Z.PAGINAS[n].slug], MODS[Z.PAGINAS[n].slug]);
let x = R(0); log(x.feita && x.linhas[0] === "Nota de gestão: 50 de 100 · Gestão em construção" && x.linhas[1] === "Área mais frágil: 1 · Planejamento e metas" && /15\/12\/2026/.test(x.linhas[2]), "página 0: nota 50, gestão em construção, área 1, ação até 15/12/2026");
if (MODS.planejamento) { x = R(1); log(x.linhas.includes("Nota das avaliações: 4,7 de 5 → 4,8 de 5 (Ana)") && x.linhas.includes("Taxa de venda direta: 30,0% → 40,0% (Ana)"), "página 1: nota 4,7 → 4,8 e venda direta 30% → 40%"); }
if (MODS.financas) { x = R(2); log(/Resultado do mês: R\$ 4\.269,20/.test(x.linhas[0]) && /ocupação de equilíbrio 28,5%/.test(x.linhas[2]), "página 2: resultado R$ 4.269,20 e ocupação de equilíbrio 28,5%"); }
if (MODS.preco) { x = R(3); log(x.linhas[0] === "Piso escrito: R$ 225,00 · diária de referência R$ 300,00" && x.linhas[2] === "Venda direta: 30% hoje, meta de 40% até 30/06/2027", "página 3: piso R$ 225, referência R$ 300, venda direta 30% → 40% até 30/06/2027"); }
if (MODS.marketing) { x = R(4); log(x.feita && x.linhas.length >= 1 && !/indisponível/.test(x.linhas[0]), "página 4: resumo da Marca e Captação montado (" + x.linhas.length + " linhas)"); }
if (MODS.pessoas) { x = R(5); log(/^20 horas por semana/.test(x.linhas[0]) && /Check-in e check-out/.test(x.linhas[1]) && /R\$ 100,00 · no segundo mês R\$ 300,00/.test(x.linhas[2]) && /16\/11\/2026/.test(x.linhas[3]), "página 5: 20 horas, check-in, alçada 100 → 300, semana 1 em 16/11/2026"); }
if (MODS.compras) { x = R(6); log(x.feita && x.linhas.length >= 1 && !/indisponível/.test(x.linhas[0]), "página 6: resumo da Matriz de Compras montado (" + x.linhas.length + " linhas)"); }
x = Z.resumoPagina(4, null, MODS.marketing); log(!x.feita && x.linhas[0] === "Página ainda não feita. Abra a ficha do módulo: trilha2/marketing/", "página sem chave: 'página ainda não feita' com o endereço da ficha");
x = Z.resumoPagina(2, { situacao: "dono", pdf: "2026-11-01T00:00:00Z" }, { calcular: () => { throw new Error("mudou"); } });
log(x.feita && /Resumo indisponível nesta versão/.test(x.linhas[0]) && /01\/11\/2026/.test(x.linhas[0]), "lógica de um módulo quebrada: cai no resumo mínimo, sem erro");
x = Z.resumoPagina(3, EST.preco, null); log(/Resumo indisponível/.test(x.linhas[0]), "módulo sem lógica carregada: resumo mínimo");

console.log("4. Bloqueios e avisos");
const v = (mud, tela) => Z.validar(Object.assign(copia(EX), mud), tela);
log(!v({ notaAtual: "5,2" }, "nota").ok && !v({ notaAtual: "abc" }, "nota").ok, "nota acima da escala ou não numérica bloqueia");
log(v({ escala: "10", notaAtual: "9,4", notaMeta: "9,6", dimensaoNota: "9", concorrentes: "9,2", notaMin: "9,4", notaMedia3m: "9,4" }, "nota").ok, "escala de 0 a 10 aceita 9,4");
log(!v({ avaliacoes3m: "80" }, "nota").ok && /passam das estadias/.test(v({ avaliacoes3m: "80" }, "nota").erros.join()), "avaliações dos 3 meses acima das estadias bloqueia");
log(!v({ avaliacoes: "20" }, "nota").ok, "avaliações dos 3 meses acima do total acumulado bloqueia");
log(!v({ avaliacoes: "3,5" }, "nota").ok, "número de avaliações não inteiro bloqueia");
log(v({ notaMeta: "4,6" }, "nota").avisos.length === 1, "meta abaixo da nota atual: aviso");
log(!v({ notaAtual: "", avaliacoes: "" }, "nota").ok && v({ situacao: "abrir", notaAtual: "", avaliacoes: "", estadias3m: "", avaliacoes3m: "" }, "nota").ok, "nota e volume obrigatórios para quem opera; opcionais para quem vai abrir");
log(!v({ criticaRepetida: "", repeticoes: "2" }, "nota").ok, "repetições sem a crítica bloqueia");
log(!v({ pedido: "Avalie" }, "protocolo").ok && !v({ respNegativa: "" }, "protocolo").ok && !v({ regra24: "" }, "protocolo").ok, "pedido curto, resposta negativa vazia ou regra das 24 h sem resposta bloqueiam");
log(v({ naoPedir: "nao" }, "protocolo").ok && v({ naoPedir: "nao" }, "protocolo").avisos.length === 1 && v({ regra24: "nao" }, "protocolo").avisos.length === 1, "não usar as regras: segue, com aviso da fonte");
log(!v({ notaMin: "4,9" }, "protocolo").ok, "nota mínima acima da meta bloqueia");
log(v({ respostaMax: "120" }, "protocolo").avisos.some((a) => /menos de uma hora/.test(a)) && v({ taxaMin: "30" }, "protocolo").avisos.some((a) => /40%/.test(a)), "resposta acima de 60 min e taxa abaixo de 40%: avisos");
log(!v({ ajuste: "" }, "protocolo").ok && !v({ ajustePrazo: "" }, "protocolo").ok && v({ repeticoes: "2", ajuste: "", ajustePrazo: "" }, "protocolo").ok, "crítica repetida 3 vezes exige ajuste e prazo; com 2, não");
log(!v({ folhaDia: "30" }, "rotina").ok && !v({ reuniaoHora: "" }, "rotina").ok && !v({ trimestral1: "2027-02-30" }, "rotina").ok, "Folha no dia 30, hora vazia ou data inválida bloqueiam");
log(v({ painelDia: "quarta" }, "rotina").avisos.length === 1 && v({ anual: "2026-12-01" }, "rotina").avisos.some((a) => /antes da primeira trimestral/.test(a)), "painel em outro dia e anual antes da trimestral: avisos");
log(!v({ inicioTeste: "2027-03-01" }, "prontidao").ok, "teste antes do fim da Fase 2 bloqueia");
log(v({ inicioTeste: "2027-04-12" }, "prontidao").avisos.some((a) => /Hoje são 5/.test(a)), "Fase 3 de 5 semanas: aviso (pelo menos oito)");
log(v({ semanasF1: "12" }, "prontidao").avisos.some((a) => /seis a dez/.test(a)) && !v({ semanasF1: "0" }, "prontidao").ok, "Fase 1 fora de 6 a 10 semanas: aviso; zero bloqueia");
log(!v({ ocupProjetada: "120" }, "prontidao").ok && !v({ responsavel: "" }, "prontidao").ok && !v({ tempoSobra: "" }, "prontidao").ok, "ocupação acima de 100, sem responsável ou sem o tempo que sobra bloqueiam");
log(!v({ cond: { teste: "nao", retirada: "", reserva: "nao", supervisao: "nao" } }, "prontidao").ok, "condição da segunda unidade sem resposta bloqueia");
log(v({ periodoMedio: "nao" }, "prontidao").avisos.some((a) => /ocupação média/.test(a)), "período que não é de ocupação média: aviso");
log(!v({ feito: "sim" }, "prontidao").ok, "teste feito sem os resultados bloqueia");
log(!v({ situacao: "" }, "abertura").ok, "abertura sem situação bloqueia");

console.log("5. A leitura do teste das duas semanas (Etapa 10, Passo 12)");
const T = (mud) => Z.veredito(Object.assign(copia(EX), { feito: "sim" }, mud));
log(T({ ocupReal: "52", notaPeriodo: "4,8", contatos: "1" }).id === "passou" && T({ ocupReal: "50", notaPeriodo: "4,6", contatos: "2" }).passou, "ocupação e nota mantidas, até 2 contatos: passou (4,6 está dentro da tolerância de 0,1)");
log(T({ ocupReal: "52", notaPeriodo: "4,8", contatos: "3" }).id === "criterio", "muitos contatos: falta critério");
log(T({ ocupReal: "52", notaPeriodo: "4,5", contatos: "0" }).id === "nota", "nota caiu: falta padrão ou treino");
log(T({ ocupReal: "40", notaPeriodo: "4,8", contatos: "0", causaExterna: "nao" }).id === "ocupacao" && T({ ocupReal: "40", notaPeriodo: "4,8", contatos: "0", causaExterna: "sim" }).id === "externa", "ocupação caiu: sem causa externa falta quem trabalhe a demanda; com causa externa, repetir");
log(T({ ocupReal: "40", notaPeriodo: "4,4", contatos: "5" }).id === "nota", "nota caída tem prioridade na leitura");
log(Z.veredito(EX) === null && T({ ocupReal: "", notaPeriodo: "4,8", contatos: "1" }) === null, "sem teste feito ou sem dados: sem leitura");
const rs = Z.calcular(Object.assign(copia(EX), { feito: "sim", ocupReal: "52", notaPeriodo: "4,8", contatos: "1", cond: { teste: "sim", retirada: "sim", reserva: "sim", supervisao: "sim" }, tempoSobra: "segunda" }), PG);
log(rs.veredito.passou && rs.segunda.r === "Pode estudar a segunda unidade", "teste passou e as quatro condições: pode estudar a segunda unidade");
const rs2 = Z.calcular(Object.assign(copia(EX), { tempoSobra: "segunda" }), PG);
log(Z.leituras(rs2, Object.assign(copia(EX), { tempoSobra: "segunda" })).atencao.some((a) => a.id === "segunda"), "escolheu a segunda unidade sem as condições: atenção");

console.log("6. Bordas e utilidades");
log(Z.num("13.000") === 13000 && Z.num("4,7") === 4.7 && Z.num("1.234,56") === 1234.56 && Z.num("40%") === 40 && Z.num("60 min") === 60 && Z.num("4.7") === 4.7 && Z.num("") === null && Z.num("x") === null, "num: 13.000 = treze mil (correção do Módulo 1), vírgula, por cento e minutos");
log(Z.somaMeses("2027-01-31", 1) === "2027-02-28" && Z.somaMeses("2027-11-30", 3) === "2028-02-29" && Z.somaDias("2026-12-28", 7) === "2027-01-04", "datas: fim de mês, ano bissexto e virada do ano");
const b = Z.completar({}); const rb = Z.calcular(b, Z.paginas({}));
log(rb.prontos === 0 && rb.fases.meses === null && rb.veredito === null && Z.leituras(rb, b).atencao[0].id === "paginas", "ficha vazia: nada pronto, sem erro, atenção pelas páginas");
log(Z.proximaVazia(b) === "nota" && Z.proximaVazia(EX) === "resultado", "continuar de onde parei: primeira tela incompleta");
const r10 = Z.calcular(Object.assign(copia(EX), { escala: "10", notaAtual: "9,4", avaliacoes: "38" }), PG);
log(perto(r10.apos3, (9.4 * 38 + 6) / 39), "escala de 10: a avaliação ruim equivalente é 6");
const curto = Z.fases(Object.assign(copia(EX), { semanasF1: "6", semanasF2: "6", inicioTeste: "2027-04-12" }));
log(curto.meses < 6 && curto.noPrazo === false, "plano mais curto que 6 meses: fora do prazo da fonte");

console.log("7. Conformidade de linguagem (textos da lógica)");
const fonte = fs.readFileSync(path.join(__dirname, "../src/logic.js"), "utf8");
log(!/[—–]/.test(fonte), "sem travessões");
log(!/consultoria|\bcurso\b|comunidade|mentoria|airbnb/i.test(fonte), "sem consultoria, curso, comunidade, mentoria, Airbnb");
log(!/garant|lucro certo|vai faturar|retorno garantido/i.test(fonte), "sem promessa de resultado");
log(fs.readFileSync(path.join(D, "qualidade/logic.js"), "utf8") === fonte, "docs/trilha2/qualidade/logic.js é cópia de src/logic.js");

console.log(`\n${ok} ok, ${fal} falhou`); process.exit(fal ? 1 : 0);

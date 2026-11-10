// Teste de ponta a ponta do Montador do Plano de Gestão no celular (iPhone 13).
// Uso: node tests/e2e.js <pasta-saida> <caminho-jspdf.umd.min.js>  (servidor local de docs/ na porta 8817)
const { chromium, devices } = require("playwright");
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");
const Z = require("../src/logic.js");
const D = path.resolve(__dirname, "../../../../docs/trilha2");
const OUT = process.argv[2], JSPDF = fs.readFileSync(process.argv[3], "utf8");
const URL = "http://localhost:8817/trilha2/qualidade/";
let ok = 0, fal = 0; const log = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
fs.mkdirSync(OUT, { recursive: true });
const EX = Z.exemplo();
const MODS = {}; Z.PAGINAS.slice(0, 7).forEach((p) => { try { MODS[p.slug] = require(path.join(D, p.slug, "logic.js")); } catch (e) { MODS[p.slug] = null; } });
const MZ = { situacao: "dono", quem: "so", tipo: "Cabanas ou chalés", unidades: "4", nome: "Ana Exemplo", email: "ana@exemplo.com", hospedagem: "Cabanas do Vale (exemplo)", cinco: { entrou: 2, sobrou: 0, ocupacao: 1, diaria: 2, custo: 0 },
  areas: { metas: 0, financas: 1, preco: 1, vendas: 2, pessoas: 1, compras: 2, operacao: 1, qualidade: 0 }, rotina: "as-vezes", tempo: "operacao", saida: "acho", prazo: "2026-12-15", pdf: "2026-11-09T10:00:00.000Z", tela: 6 };
const estado = (slug, pdf) => Object.assign({}, MODS[slug].EXEMPLO || MODS[slug].exemplo(), { nome: "Ana Exemplo", hospedagem: "Cabanas do Vale (exemplo)" }, pdf ? { pdf: "2026-11-09T12:00:00.000Z" } : {});
const pdfTexto = (f) => { try { return execFileSync("pdftotext", ["-layout", f, "-"]).toString(); } catch (e) { return ""; } };
const pdfPaginas = (f) => { try { return +(/Pages:\s+(\d+)/.exec(execFileSync("pdfinfo", [f]).toString()) || [0, 0])[1]; } catch (e) { return 0; } };

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ ...devices["iPhone 13"], acceptDownloads: true });
  await ctx.route("**/jspdf.umd.min.js", (r) => r.fulfill({ contentType: "application/javascript", body: JSPDF }));
  await ctx.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
  const p = await ctx.newPage(); const erros = [];
  p.on("pageerror", (e) => erros.push(e.message)); p.on("console", (m) => m.type() === "error" && erros.push(m.text()));
  const shot = (n) => p.screenshot({ path: `${OUT}/${n}.png`, fullPage: true });
  const semScrollX = async () => (await p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1));
  const vaiOff = () => p.locator("#vai").isDisabled();
  const radio = (name, v) => p.locator(`input[name="${name}"][value="${v}"]`).locator("xpath=..").click();
  const live = () => p.textContent("#live");
  let telasSemScroll = true; const confereScroll = async () => { if (!(await semScrollX())) telasSemScroll = false; };

  // Cinco páginas prontas (0, 1, 2, 3, 5), a 4 em andamento (sem PDF) e a 6 ainda não feita
  await p.goto(URL);
  await p.evaluate((st) => { localStorage.clear(); for (const [k, v] of Object.entries(st)) localStorage.setItem(k, JSON.stringify(v)); }, {
    "zion-t2-marco-zero": MZ, "zion-t2-planejamento": estado("planejamento", 1), "zion-t2-financas": estado("financas", 1), "zion-t2-preco": estado("preco", 1),
    "zion-t2-marketing": estado("marketing", 0), "zion-t2-pessoas": estado("pessoas", 1) });
  await p.reload(); await p.waitForFunction(() => !!window.jspdf && !!window.ZQ && window.__apis === true);
  log(await p.title() === "Montador do Plano de Gestão" && (await p.locator("h1").textContent()) === "O Montador do Plano de Gestão", "abertura carrega com o título certo");
  log((await p.inputValue("#nome")) === "Ana Exemplo" && (await p.inputValue("#hospedagem")) === "Cabanas do Vale (exemplo)" && (await p.inputValue("#email")) === "ana@exemplo.com", "nome, e-mail e hospedagem lidos das fichas anteriores");
  log(await p.locator('input[name="sit"][value="dono"]').isChecked(), "situação lida das fichas anteriores (já opero)");
  log((await p.locator("#retoma").count()) === 0, "primeira visita, mesmo com as fichas anteriores: sem 'continuar de onde parei'");
  log(/Não é promessa de renda, retorno ou resultado/.test(await p.textContent("footer")), "rodapé educacional");
  const apis = await p.evaluate(() => Object.fromEntries(Object.entries(window.APIS || {}).map(([k, v]) => [k, !!(v && v.calcular)])));
  await shot("p01-abertura"); await confereScroll();
  await p.click("#vai");

  // Tela 1 · As páginas
  log(/Tela 1 de 5/.test(await p.textContent(".progresso")) && /As páginas que você já fez/.test(await p.textContent("h2")), "tela 1: as páginas, com progresso");
  const st = await p.$$eval("#paginas .pag", (els) => els.map((e) => e.dataset.n + ":" + e.querySelector(".st").textContent));
  log(st.length === 8 && st.filter((s) => /Pronta · PDF de 09\/11\/2026/.test(s)).length === 5, "cinco páginas prontas com a data do PDF");
  log(/^4:Em andamento/.test(st[4]) && /^6:Página ainda não feita/.test(st[6]) && /^7:Você monta agora/.test(st[7]), "página 4 em andamento, página 6 ainda não feita, página 7 montada aqui");
  log((await p.locator('#paginas .pag[data-n="6"] a').getAttribute("href")) === "../compras/" && (await p.locator('#paginas .pag[data-n="0"] a').count()) === 0, "link para a ficha só nas páginas que faltam");
  log(/Páginas prontas: 5 de 7/.test(await p.textContent("#contagem")) && !(await vaiOff()), "contagem 5 de 7 e dá para seguir");
  await shot("p02-paginas"); await confereScroll(); await p.click("#vai");

  // Tela 2 · A nota
  log(/A nota e as avaliações/.test(await p.textContent(".eyebrow")), "tela 2: a nota e as avaliações");
  log((await p.inputValue("#notaAtual")) === "4,7" && (await p.inputValue("#notaMeta")) === "4,8", "nota 4,7 e meta 4,8 trazidas do Painel de Gestão (Módulo 1)");
  log(await vaiOff() && /avaliações acumuladas/.test(await p.textContent("#erro")), "bloqueada sem o número de avaliações");
  await p.fill("#avaliacoes", "38"); await p.fill("#prazoMeta", "2027-10-31"); await p.fill("#tempoResposta", "40");
  await p.fill("#estadias3m", "20"); await p.fill("#avaliacoes3m", "25");
  log(await vaiOff() && /passam das estadias/.test(await p.textContent("#erro")), "avaliações acima das estadias bloqueiam com mensagem");
  await p.fill("#estadias3m", "72");
  await p.selectOption("#dimensao", "limpeza"); await p.fill("#dimensaoNota", "4,6"); await p.fill("#concorrentes", "4,6"); await p.fill("#criticas3m", "7");
  await p.fill("#criticaRepetida", EX.criticaRepetida); await p.fill("#repeticoes", "3");
  const lv = await live();
  log(!(await vaiOff()) && /leva a média para 4,66/.test(lv) && /35%/.test(lv) && /\+0,1/.test(lv) && /problema de produto/.test(lv), "ao vivo: média depois de uma de 3 = 4,66; 35% avaliam; +0,1 dos concorrentes; problema de produto");
  await shot("p03-nota"); await confereScroll(); await p.click("#vai");

  // Tela 3 · Protocolo e padrão mínimo
  log(/Resposta às avaliações e padrão mínimo/.test(await p.textContent(".eyebrow")), "tela 3: protocolo e padrão mínimo");
  log((await p.inputValue("#notaMin")) === "4,7" && (await p.inputValue("#respostaMax")) === "60" && (await p.inputValue("#taxaMin")) === "40", "nota mínima 4,7 trazida do Módulo 5; referências da fonte 60 min e 40%");
  log(await vaiOff() && (await p.locator("#ajuste").count()) === 1, "bloqueada sem o protocolo; campo do ajuste aparece (crítica repetida 3 vezes)");
  await p.fill("#pedido", EX.pedido); await radio("naoPedir", "sim"); await p.fill("#respPositiva", EX.respPositiva); await p.fill("#respNegativa", EX.respNegativa);
  await radio("regra24", "nao");
  log(/irritação fresca/.test(await p.textContent("#avisos")), "sem a regra das 24 horas: aviso da fonte");
  await radio("regra24", "sim"); await p.fill("#quemResponde", "Ana (dona)"); await radio("auditoria", "sim");
  await p.fill("#notaMin", "4,9"); log(await vaiOff() && /não pode passar da meta/.test(await p.textContent("#erro")), "nota mínima acima da meta bloqueia");
  await p.fill("#notaMin", "4,7");
  log(await vaiOff() && /ajuste de produto/.test(await p.textContent("#erro")), "sem o ajuste de produto, bloqueada");
  await p.fill("#ajuste", EX.ajuste); await p.fill("#ajustePrazo", "2026-11-30");
  log(!(await vaiOff()) && /Trocar o sifão do chuveiro da cabana 3 e incluir o ralo no checklist de limpeza · até 30\/11\/2026/.test(await live()), "padrão mínimo ao vivo com o ajuste e o prazo");
  await shot("p04-protocolo"); await confereScroll(); await p.click("#vai");

  // Tela 4 · Rotina
  log(/A rotina semanal/.test(await p.textContent(".eyebrow")), "tela 4: a rotina semanal");
  log((await p.inputValue("#reuniaoDia")) === "segunda" && (await p.inputValue("#reuniaoHora")) === "08:00" && (await p.inputValue("#painelDia")) === "segunda", "reunião de segunda 08:00 (Módulo 1) e painel de segunda (Módulo 5) já preenchidos");
  await p.fill("#folhaDia", "30"); log(await vaiOff() && /de 1 a 28/.test(await p.textContent("#erro")), "Folha no dia 30 bloqueia");
  await p.fill("#folhaDia", "5"); await p.fill("#trimestral1", "2027-01-11"); await p.fill("#anual", "2027-11-08");
  log(!(await vaiOff()) && /11\/01\/2027 · 11\/04\/2027 · 11\/07\/2027 · 11\/10\/2027/.test(await live()) && /08\/11\/2027/.test(await live()), "quatro trimestrais e a anual calculadas");
  await shot("p05-rotina"); await confereScroll(); await p.click("#vai");

  // Tela 5 · Teste de prontidão e plano de crescimento
  log(/O teste de prontidão e o plano de crescimento/.test(await p.textContent(".eyebrow")), "tela 5: teste de prontidão e plano de crescimento");
  log((await p.inputValue("#inicioF1")) === "2026-11-16", "início da Fase 1 trazido do Mapa de Pessoas (16/11/2026)");
  await p.fill("#inicioTeste", "2027-03-01"); await p.fill("#responsavel", EX.responsavel); await p.fill("#ocupProjetada", "50"); await p.fill("#notaMedia3m", "4,7");
  await radio("periodoMedio", "sim"); await p.locator("label.op", { hasText: "Trabalhar sobre o negócio" }).click(); await p.fill("#tempoSobraTxt", EX.tempoSobraTxt);
  for (const [k, v2] of Object.entries(EX.cond)) await radio("cond-" + k, v2);
  log(await vaiOff() && /antes do fim da Fase 2/.test(await p.textContent("#erro")), "teste antes do fim da Fase 2 bloqueia");
  await p.fill("#inicioTeste", "2027-06-14");
  const lp = await live();
  log(!(await vaiOff()) && /Fase 3 · Acompanhar por exceção: 08\/03\/2027 a 13\/06\/2027 \(14 semanas\)/.test(lp) && /7,4 meses/.test(lp) && /Agora não/.test(lp), "fases ao vivo: Fase 3 com 14 semanas, 7,4 meses, segunda unidade agora não");
  await radio("feito", "sim");
  log(await vaiOff() && (await p.locator("#ocupReal").count()) === 1, "teste já feito: pede os resultados");
  await p.fill("#ocupReal", "52"); await p.fill("#notaPeriodo", "4,8"); await p.fill("#contatos", "3");
  log(/Ocupação e nota mantidas, com muitos contatos/.test(await live()), "leitura do teste: muitos contatos = falta critério");
  await radio("feito", "nao");
  await shot("p06-prontidao"); await confereScroll(); await p.click("#vai");

  // Resultado
  const salvo = await p.evaluate(() => JSON.parse(localStorage.getItem("zion-t2-qualidade")));
  const estAtual = await p.evaluate((ks) => Object.fromEntries(ks.map((k) => [k[0], JSON.parse(localStorage.getItem(k[1]))])), Z.PAGINAS.slice(0, 7).map((x) => [x.slug, x.chave]));
  const esperado = Z.calcular(salvo, Z.paginas(estAtual)), LE = Z.leituras(esperado, salvo);
  log(/Faltam 2 de 8 páginas/.test(await p.textContent(".leitura .rot")) && /6 de 8/.test(await p.textContent("#paginasN")), "resultado: 6 de 8 páginas no Plano, faltam 2");
  log((await p.textContent("#leituraNota")) === LE.nota, "leitura da nota igual à lógica");
  const pad = await p.$$eval("#padrao tbody tr", (t) => t.map((x) => x.children[1].textContent));
  log(JSON.stringify(pad) === JSON.stringify(esperado.padrao.map((x) => x.v)), "tabela do padrão mínimo igual à lógica, linha a linha");
  log((await p.textContent('#indicadores [data-id="taxa"] strong')) === "35%" && (await p.textContent('#indicadores [data-id="saida"] strong')) === "7,4 meses", "indicadores: 35% avaliam, 7,4 meses até o teste");
  const at = await p.$$eval("#atencao > div", (t) => t.map((x) => x.dataset.id));
  log(at.join() === LE.atencao.map((a) => a.id).join() && at[0] === "paginas" && at.includes("produto") && at.includes("taxa"), "atenção na ordem da lógica: páginas, produto, taxa");
  const fases = await p.$$eval("#fases tbody tr", (t) => t.map((x) => x.children[2].textContent));
  log(/16\/11\/2026 a 10\/01\/2027/.test(fases[0]) && /14\/06\/2027 a 27\/06\/2027/.test(fases[3]), "plano de saída com as quatro fases datadas");
  log(/14\/06\/2027/.test(await p.textContent("#teste")) && /Ana \(dona\)/.test(await p.textContent("#rotina")), "teste de 14/06 a 27/06/2027; rotina com quem responde as avaliações");
  const cresc = await p.textContent("#crescimento");
  log(/4,7 de 5 → 4,8 de 5 até 31\/10\/2027/.test(cresc) && /40% até 30\/06\/2027 \(Módulo 3\)/.test(cresc) && /Agora não/.test(cresc), "plano de crescimento: nota 4,7 → 4,8, venda direta 30% → 40% até 30/06/2027, segunda unidade agora não");
  log(/terminar as páginas 4, 6/.test(await p.textContent("#selo")) && /baixar o PDF/.test(await p.textContent("#selo")), "selo pendente: terminar as páginas 4 e 6 e baixar o PDF");
  await shot("p07-resultado"); await confereScroll();
  let [dl] = await Promise.all([p.waitForEvent("download"), p.click("#pdf")]);
  log(dl.suggestedFilename() === "plano-de-gestao-profissional.pdf", "PDF baixado: " + dl.suggestedFilename());
  const pdf1 = `${OUT}/plano-parcial.pdf`; await dl.saveAs(pdf1);
  let t1 = pdfTexto(pdf1);
  log(/Nota de gestão: 50 de 100/.test(t1) && /R\$ 4\.269,20/.test(t1) && /Piso escrito: R\$ 225,00/.test(t1) && /20 horas por semana/.test(t1), "PDF: resumos das páginas 0, 2, 3 e 5 com os números das fichas");
  log(/Página ainda não feita\. Abra a ficha do módulo: trilha2\/compras\//.test(t1) && /Em andamento/.test(t1), "PDF: página 6 'ainda não feita' com o endereço; página 4 em andamento");
  log(/O PADRÃO MÍNIMO/.test(t1) && /A ROTINA SEMANAL/.test(t1) && /O TESTE DE PRONTIDÃO E O PLANO DE SAÍDA/.test(t1) && /Jornada 3/.test(t1), "PDF: página 7, rotina semanal, teste e próxima etapa");
  log(/terminar as páginas 4, 6/.test(await p.textContent("#selo")), "com páginas faltando, o PDF sai mas o selo continua pendente");

  // A dona termina as páginas 4 e 6 neste aparelho e volta ao Montador
  await p.evaluate((st2) => { for (const [k, v] of Object.entries(st2)) localStorage.setItem(k, JSON.stringify(v)); }, { "zion-t2-marketing": estado("marketing", 1), "zion-t2-compras": estado("compras", 1) });
  await p.reload(); await p.waitForFunction(() => window.__apis === true); await p.waitForTimeout(200);
  log(/As oito páginas do seu Plano estão juntas/.test(await p.textContent(".leitura .rot")) && /8 de 8/.test(await p.textContent("#paginasN")), "com as sete páginas prontas: 8 de 8");
  [dl] = await Promise.all([p.waitForEvent("download"), p.click("#pdf")]);
  const pdf2 = `${OUT}/plano-de-gestao-profissional.pdf`; await dl.saveAs(pdf2); const t2 = pdfTexto(pdf2); const np = pdfPaginas(pdf2);
  log((await p.textContent("#selo")) === "Plano completo · pronto para a Jornada 3", "selo: Plano completo, pronto para a Jornada 3");
  log(fs.statSync(pdf2).size > 20000 && np >= 3 && np <= 8, `PDF completo com ${fs.statSync(pdf2).size} bytes e ${np} páginas`);
  log(!/Página ainda não feita/.test(t2) && /PÁGINA 6/.test(t2) && /PÁGINA 4/.test(t2), "PDF completo: todas as páginas resumidas");
  log(Object.values(apis).filter(Boolean).length === 7 && /Ação de 30 dias/.test(t2), "a lógica dos sete módulos carregou sem conflito de nomes (três usam ZP)");
  fs.copyFileSync(pdf2, path.join(__dirname, "../demonstracao/plano-de-gestao-profissional.pdf"));
  const salvo2 = await p.evaluate(() => JSON.parse(localStorage.getItem("zion-t2-qualidade")));
  log(salvo2.pdf && salvo2.avaliacoes === "38" && salvo2.notaAtual === "4,7" && salvo2.inicioTeste === "2027-06-14" && salvo2.cond.retirada === "sim", "chave zion-t2-qualidade guarda as respostas como digitadas e a data do PDF");

  // Persistência e continuar de onde parei
  await p.evaluate(() => { const s = JSON.parse(localStorage.getItem("zion-t2-qualidade")); s.tela = 0; localStorage.setItem("zion-t2-qualidade", JSON.stringify(s)); });
  await p.reload(); await p.waitForFunction(() => !!window.ZQ);
  log((await p.locator("#retoma").count()) === 1, "abertura oferece continuar de onde parei");
  await p.click("#retoma"); log(/O meu Plano de Gestão Profissional/.test(await p.textContent(".eyebrow")), "continuar leva ao resultado (tudo preenchido)");
  await p.click("#refaz"); log(/As páginas que você já fez/.test(await p.textContent("h2")), "revisar as respostas volta à tela 1");
  await p.click("#vai"); log((await p.inputValue("#avaliacoes")) === "38", "respostas mantidas ao revisar");

  // Aparelho novo, sem fichas anteriores: botão do exemplo
  const c2 = await b.newContext({ ...devices["iPhone 13"], acceptDownloads: true });
  await c2.route("**/jspdf.umd.min.js", (r) => r.fulfill({ contentType: "application/javascript", body: JSPDF }));
  await c2.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
  const q = await c2.newPage(); q.on("pageerror", (e) => erros.push(e.message));
  await q.goto(URL); await q.waitForFunction(() => window.__apis === true);
  log((await q.inputValue("#nome")) === "" && (await q.locator("#vai").isDisabled()), "aparelho novo: nada preenchido, Começar bloqueado sem situação");
  await q.click("#exemplo");
  log(/As páginas que você já fez/.test(await q.textContent("h2")) && (await q.$$eval("#paginas .st.falta", (e) => e.length)) === 7, "exemplo preenche só a página 7: as sete anteriores aparecem como ainda não feitas");
  for (let i = 0; i < 5; i++) await q.click("#vai");
  log(/Faltam 7 de 8 páginas/.test(await q.textContent(".leitura .rot")), "resultado do exemplo sem as fichas: faltam 7 de 8");
  const [dl3] = await Promise.all([q.waitForEvent("download"), q.click("#pdf")]); const pdf3 = `${OUT}/so-pagina-7.pdf`; await dl3.saveAs(pdf3);
  log((pdfTexto(pdf3).match(/Página ainda não feita\. Abra a ficha/g) || []).length === 7, "PDF com as sete páginas marcadas 'ainda não feita'");
  await q.screenshot({ path: `${OUT}/d01-exemplo-sem-fichas.png`, fullPage: true });

  // Quem vai abrir: nota e volume opcionais
  await q.evaluate(() => { const s = JSON.parse(localStorage.getItem("zion-t2-qualidade")); Object.assign(s, { situacao: "abrir", notaAtual: "", avaliacoes: "", estadias3m: "", avaliacoes3m: "", notaMedia3m: "", tela: 6 }); localStorage.setItem("zion-t2-qualidade", JSON.stringify(s)); });
  await q.reload(); await q.waitForFunction(() => window.__apis === true);
  log(/Sem nota ainda: você vai abrir/.test(await q.textContent("#leituraNota")) && /desenho/.test(await q.textContent(".card")), "quem vai abrir: leitura sem nota e aviso de desenho");

  // Desktop
  const c3 = await b.newContext({ viewport: { width: 1280, height: 900 } });
  await c3.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
  const dpg = await c3.newPage(); await dpg.goto(URL); await dpg.waitForFunction(() => !!window.ZQ);
  log(await dpg.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), "desktop 1280: sem rolagem horizontal");
  await dpg.screenshot({ path: `${OUT}/d02-desktop.png` });

  log(telasSemScroll, "nenhuma tela com rolagem horizontal no iPhone 13");
  log(erros.length === 0, "sem erro de JavaScript" + (erros.length ? ": " + erros.join(" | ") : ""));
  await b.close();
  console.log(`\n${ok} ok, ${fal} falhou`); process.exit(fal ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });

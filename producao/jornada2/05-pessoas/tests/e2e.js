// Teste de ponta a ponta da ficha "O meu Mapa de Pessoas e Alçadas" no celular (iPhone 13).
// Uso: node tests/e2e.js <pasta-saida> <caminho-jspdf.umd.min.js>  (servidor local de docs/ na porta 8815)
const { chromium, devices } = require("playwright");
const fs = require("fs");
const Z = require("../src/logic.js");
const ZF = require("../../02-financas/src/logic.js");
const OUT = process.argv[2], JSPDF = fs.readFileSync(process.argv[3], "utf8");
const URL = "http://localhost:8815/trilha2/pessoas/";
let ok = 0, fal = 0; const log = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
fs.mkdirSync(OUT, { recursive: true });
const EX = Z.exemplo();
const rf = ZF.calcular(ZF.EXEMPLO);
const FIN = { fixoTotalMes: rf.fixoTotalMes, margemOutras: rf.margemOutras, margemPorNoite: rf.margemPorNoite, noitesDisponiveis: rf.noitesDisponiveis, ocupacaoEquilibrio: rf.ocupacaoEquilibrio };
const esperado = Z.calcular(EX, FIN), LE = Z.leituras(esperado, EX);
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
  let telasSemScroll = true;
  const confereScroll = async () => { if (!(await semScrollX())) telasSemScroll = false; };

  // nome e Folha Única vindos do Módulo 2 (o teste de viabilidade usa a Folha)
  await p.goto(URL);
  await p.evaluate((f) => localStorage.setItem("zion-t2-financas", JSON.stringify(Object.assign({}, f, { nome: "Ana Exemplo", hospedagem: "Cabanas do Vale (exemplo)" }))), ZF.EXEMPLO);
  await p.reload(); await p.waitForFunction(() => !!window.jspdf && !!window.ZP && !!window.ZF);
  log(await p.title() === "Mapa de Pessoas e Alçadas" && (await p.locator("h1").textContent()) === "O meu Mapa de Pessoas e Alçadas", "abertura carrega com o título certo");
  log((await p.inputValue("#nome")) === "Ana Exemplo" && (await p.inputValue("#hospedagem")) === "Cabanas do Vale (exemplo)", "nome e hospedagem lidos da Folha Única (Módulo 2)");
  log(/Não é promessa de renda, retorno ou resultado/.test(await p.textContent("footer")), "rodapé educacional");
  log(await vaiOff(), "Começar bloqueado sem situação, unidades e a pergunta dos 7 dias");
  await shot("p01-abertura"); await confereScroll();
  await p.locator("label.op", { hasText: "Já opero" }).click();
  await p.fill("#unidades", "4"); await p.fill("#equipeHoje", "2"); await p.fill("#feriasDias", "0");
  log(await vaiOff(), "ainda bloqueado sem a pergunta dos 7 dias");
  await p.locator("label.op", { hasText: "Nunca, desde que abri" }).click();
  log(!(await vaiOff()), "Começar liberado");
  await p.click("#vai");

  // Tela 1 · O que só você sabe
  log(/Tela 1 de 5/.test(await p.textContent(".progresso")) && /O que só você sabe/.test(await p.textContent("h2")), "tela 1: o que só você sabe, com progresso");
  log(await vaiOff(), "tela 1 bloqueada sem as quatro dependências");
  for (const [k, v] of Object.entries(EX.dep)) await radio("dep-" + k, v);
  log(!(await vaiOff()) && /Dependência mais forte: Decisão/.test(await live()), "dependência mais forte: decisão (empate resolvido na ordem da fonte)");
  log(/resolver esta primeiro/.test(await p.textContent("#avisos")), "aviso: acesso não é fraca e sem data");
  await p.fill("#acessoData", "2026-11-14"); log((await p.textContent("#avisos")).trim() === "", "com a data, o aviso some");
  await p.fill("#invTotal", "10"); await p.fill("#invSimples", "18");
  log(await vaiOff() && /passam do total/.test(await p.textContent("#erro")), "classes acima do total bloqueiam com mensagem");
  await p.fill("#invTotal", "52"); await p.fill("#invDecisao", "14"); await p.fill("#invAcesso", "9");
  log(!(await vaiOff()) && /52<\/b> linhas, <b>79%/.test(await p.innerHTML("#live")), "inventário: 52 linhas, 79% de resolução rápida");
  await shot("p02-cabeca"); await confereScroll(); await p.click("#vai");

  // Tela 2 · Quem faz o quê
  log(/Quem faz o quê/.test(await p.textContent(".eyebrow")), "tela 2: quem faz o quê");
  log(await vaiOff(), "tela 2 bloqueada sem responsáveis");
  log((await p.locator('input[name="julg-compras"][value="alto"]').isChecked()) && (await p.locator('input[name="julg-limpeza"][value="baixo"]').isChecked()), "julgamento sugerido pela fonte já marcado");
  for (const a of Z.ATIVIDADES) { await p.fill("#resp-" + a.id, EX.ativ[a.id].resp); await p.fill("#horas-" + a.id, EX.ativ[a.id].horas); }
  await p.fill("#horas-checkin", "-2"); log(await vaiOff() && /negativo/.test(await p.textContent("#erro")), "hora negativa bloqueia");
  await p.fill("#horas-checkin", "5");
  log(!(await vaiOff()) && /Horas suas por semana: <b>20<\/b>/.test(await p.innerHTML("#live")), "total de 20 horas por semana (coerente com a Conta da Retirada do Módulo 2)");
  log(/Primeira a delegar, pela regra da fonte: <b>Check-in e check-out/.test(await p.innerHTML("#live")) && /4 de 6/.test(await live()), "primeira a delegar: check-in e check-out; 4 de 6 setores só da dona");
  await shot("p03-mapa"); await confereScroll(); await p.click("#vai");

  // Tela 3 · Alçadas
  log(/Até quanto cada um decide/.test(await p.textContent(".eyebrow")), "tela 3: alçadas");
  log(await vaiOff() && /alçada inicial/.test(await p.textContent("#erro")), "bloqueada sem a alçada inicial");
  for (const s of Z.SITUACOES_CRITERIO) { const c = EX.crit[s.id]; await p.fill("#quem-" + s.id, c.quem); await p.fill("#regra-" + s.id, c.regra); await p.fill("#alc-" + s.id, c.alcada); }
  await p.fill("#alcadaInicial", "100"); await p.fill("#alcada2mes", "50");
  log(/está abaixo da inicial/.test(await p.textContent("#avisos")), "aviso quando a alçada do segundo mês desce");
  await p.fill("#alcada2mes", "300");
  log(!(await vaiOff()) && /6 de 7/.test(await live()) && /R\$ 100,00/.test(await live()) && /R\$ 300,00/.test(await live()), "6 de 7 regras escritas; alçada 100 → 300");
  await shot("p04-alcadas"); await confereScroll(); await p.click("#vai");

  // Tela 4 · Painel
  log(/Como acompanhar de fora/.test(await p.textContent(".eyebrow")) && (await p.locator(".c-sig li").count()) === 6, "tela 4: painel com os seis indicadores");
  log(await vaiOff(), "bloqueada sem nota mínima, percentual, dia e nível");
  await p.fill("#notaMin", "4,7"); await p.fill("#gastoPct", "10"); await p.selectOption("#diaSemanal", "segunda");
  await p.fill("#quemEnvia", EX.quemEnvia); await p.fill("#conversaMensal", EX.conversaMensal);
  await p.locator("label.op", { hasText: "1 · Operando" }).click();
  log(!(await vaiOff()) && /\(4,7\)/.test(await live()) && /mais de 10%/.test(await live()) && /R\$ 100,00/.test(await live()), "quatro exceções com nota 4,7, gasto 10% e alçada 100");
  await shot("p05-painel"); await confereScroll(); await p.click("#vai");

  // Tela 5 · Plano
  log(/As quatro semanas/.test(await p.textContent(".eyebrow")), "tela 5: plano de quatro semanas");
  log((await p.inputValue("#ativPlano")) === "checkin" && /sugerida/.test(await p.textContent("#ativPlano option:checked")), "atividade sugerida já selecionada: check-in e check-out");
  log(await vaiOff(), "bloqueada sem pessoa, formato, início e cobertura");
  await p.fill("#pessoa", EX.pessoa); await p.locator("label.op", { hasText: "Diarista por estadia" }).click();
  await p.fill("#inicio", "2026-11-16"); await p.fill("#cobertura", EX.cobertura); await p.fill("#custoMes", "500");
  await radio("pre-preAcesso", "nao"); await radio("pre-preProc", "nao"); await radio("pre-preCrit", "sim");
  await p.fill("#tempoLivre", EX.tempoLivre);
  const lv = await live();
  log(/1 · 16\/11 a 22\/11/.test(lv) && /4 · 07\/12 a 13\/12/.test(lv) && /13\/12\/2026/.test(lv), "semanas de 16/11 a 13/12 e avaliação em 13/12/2026");
  log(/5 horas/.test(lv) && /25%/.test(lv), "5 horas por semana saem da dona (25%)");
  log((await p.locator('input[name="equi"]').count()) === 0 && /28,5%/.test(lv) && /30,7%/.test(lv), "teste de viabilidade calculado pela Folha Única: 28,5% → 30,7%");
  log(!(await vaiOff()) && (await p.textContent("#vai")).trim() === "Ver o meu mapa", "liberado; botão Ver o meu mapa");
  await shot("p06-plano"); await confereScroll(); await p.click("#vai");

  // Resultado
  log((await p.textContent("#horas")).includes("20 h") && (await p.textContent("#horas")).includes("7 de 7"), "resultado: 20 h e 7 de 7 itens prontos");
  log((await p.textContent("#primeira")).trim() === LE.primeira, "primeira a delegar igual à lógica");
  const linhas = await p.locator("#mapa tbody tr").all(); const M = Z.mapa(esperado, EX);
  let mapaOk = linhas.length === 8;
  for (let i = 0; i < linhas.length && mapaOk; i++) { const tx = await linhas[i].textContent(); mapaOk = tx.includes(M[i].atividade) && tx.includes(M[i].resp) && tx.includes(M[i].alcada); }
  log(mapaOk, "mapa de quem faz o quê com alçada bate com logic.js, linha a linha");
  log(/Depois: Diarista, que já faz a limpeza/.test(await p.textContent('#mapa tr[data-id="checkin"]')), "linha do check-in mostra quem assume depois do plano");
  log((await p.locator("#criterios tbody tr").count()) === 7 && /regra a escrever/.test(await p.textContent("#criterios")), "tabela de critérios com as 7 situações, uma a escrever");
  const leit = await p.textContent("#leituras");
  log([LE.horas, LE.setores, LE.dependencia, LE.inventario, LE.criterios, LE.nivel].every((s) => leit.includes(s)), "as seis leituras batem com logic.js");
  log((await p.locator("#atencao > div").count()) === LE.atencao.length && /nunca ficou sete dias/.test(await p.textContent("#atencao")), "atenção: alertas na ordem da lógica, começando pelos 7 dias");
  log(/de 28,5% para 30,7%/.test(await p.textContent("#viabilidade")), "teste de viabilidade na tela");
  log((await p.locator("#semanas tbody tr").count()) === 4 && /Sombra/.test(await p.textContent("#semanas")) && /Autonomia com alçada/.test(await p.textContent("#semanas")), "as quatro semanas da fonte");
  log(/Falta/.test(await p.textContent("#prereq")) && /Pronto/.test(await p.textContent("#prereq")), "antes da semana 1: o que falta e o que está pronto");
  log((await p.textContent("#excecoes")).includes("segunda-feira") && (await p.locator("#excecoes li").count()) === 4, "painel por exceção: segunda-feira e quatro exceções");
  log((await p.textContent("#verificar")).trim() === LE.verificar, "como verificar: avaliação em 13/12/2026");
  const texto = await p.textContent(".card");
  log(!/\b(KPI|SOP|RH|ADR|RevPAR|DRE)\b/.test(texto), "sem sigla na tela de resultado");
  log(/Módulo 6 · Compras, estoque e manutenção/.test(texto), "próxima etapa aponta o módulo 6");
  log((await p.locator('a[href="../materiais/planilhas/"]').count()) === 1 && (await p.locator('a[href="../"]').count()) === 1, "links para a planilha e para as ferramentas");
  log(/Falta: o PDF baixado/.test(await p.textContent("#selo")), "selo pendente: falta só o PDF");
  await confereScroll(); log(telasSemScroll, "sem rolagem horizontal em nenhuma tela no celular");
  await shot("p07-resultado");
  const [dl] = await Promise.all([p.waitForEvent("download"), p.click("#pdf")]);
  log(dl.suggestedFilename() === "mapa-de-pessoas-e-alcadas.pdf", "PDF baixado: " + dl.suggestedFilename());
  const pdfPath = `${OUT}/mapa-de-pessoas.pdf`; await dl.saveAs(pdfPath); log(fs.statSync(pdfPath).size > 8000, `PDF com ${fs.statSync(pdfPath).size} bytes`);
  log(/Pronto para avançar/.test(await p.textContent("#selo")), "selo: pronto para avançar após o PDF");
  // persistência
  await p.reload(); await p.waitForFunction(() => !!window.ZP);
  log((await p.textContent("#horas")).includes("20 h") && /Pronto/.test(await p.textContent("#selo")), "recarregar mantém o resultado e o selo (salvo no aparelho)");
  const salvo = await p.evaluate(() => JSON.parse(localStorage.getItem("zion-t2-pessoas")));
  log(salvo && salvo.ativ.checkin.horas === "5" && salvo.crit.cortesia.alcada === "42" && salvo.pdf && salvo.inicio === "2026-11-16", "chave zion-t2-pessoas guarda as respostas como digitadas");
  // revisar volta à tela 1 com as respostas
  await p.click("#refaz"); log(/Tela 1 de 5/.test(await p.textContent(".progresso")) && (await p.inputValue("#invTotal")) === "52", "revisar volta à tela 1 com as respostas mantidas");
  // continuar de onde parei
  await p.evaluate(() => { const s = JSON.parse(localStorage.getItem("zion-t2-pessoas")); s.tela = 0; s.cobertura = ""; localStorage.setItem("zion-t2-pessoas", JSON.stringify(s)); });
  await p.reload(); await p.waitForFunction(() => !!window.ZP);
  log(await p.locator("#retoma").isVisible(), "abertura oferece continuar de onde parei");
  await p.click("#retoma"); log(/As quatro semanas/.test(await p.textContent(".eyebrow")), "continuar leva à primeira tela incompleta (plano, sem cobertura)");
  // sem a Folha Única: pergunta do equilíbrio aparece e "não sei" vira alerta
  await p.evaluate(() => localStorage.removeItem("zion-t2-financas")); await p.reload(); await p.waitForFunction(() => !!window.ZP);
  log((await p.locator('input[name="equi"]').count()) === 3, "sem a Folha Única, a ficha pergunta o teste de viabilidade");
  await radio("equi", "naosei"); await p.fill("#cobertura", "Eu (dona)"); await p.click("#vai");
  log(/Folha Única do Módulo 2 antes de fechar/.test(await p.textContent("#atencao")), "\"não sei\" vira alerta para fazer a conta no Módulo 2");
  // exemplo didático pelo botão
  await p.evaluate(() => localStorage.clear()); await p.reload(); await p.waitForFunction(() => !!window.ZP);
  await p.click("#exemplo"); log(/Tela 1 de 5/.test(await p.textContent(".progresso")) && (await p.inputValue("#invTotal")) === "52", "botão do exemplo leva à tela 1 com os dados do exemplo");
  for (let i = 0; i < 5; i++) { if (await vaiOff()) break; await p.click("#vai"); }
  log((await p.textContent("#horas")).includes("20 h") && /Cabanas do Vale \(exemplo\)/.test(await p.textContent(".eyebrow")), "exemplo didático percorre as cinco telas e dá o mesmo mapa");
  await shot("p08-exemplo");
  // desktop
  const d = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await d.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
  await d.route("**/jspdf.umd.min.js", (r) => r.fulfill({ contentType: "application/javascript", body: JSPDF }));
  await d.goto(URL); await d.waitForFunction(() => !!window.ZP); await d.screenshot({ path: `${OUT}/d01-abertura.png`, fullPage: true });
  log(erros.length === 0, "sem erros de JavaScript" + (erros.length ? ": " + erros.join(" | ") : ""));
  await b.close();
  console.log(`\n${ok} ok, ${fal} falhou`); process.exit(fal ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });

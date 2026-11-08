// Teste de ponta a ponta da ficha "Diagnóstico de Gestão" no celular.
// Uso: node tests/e2e.js <pasta-saida> <caminho-jspdf.umd.min.js>  (servidor local de docs/ na porta 8790)
const { chromium, devices } = require("playwright");
const fs = require("fs"), path = require("path");
const Z = require("../src/logic.js");
const OUT = process.argv[2], JSPDF = fs.readFileSync(process.argv[3], "utf8");
const URL = "http://localhost:8790/trilha2/marco-zero/";
let ok = 0, fal = 0; const log = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ ...devices["iPhone 13"], acceptDownloads: true });
  await ctx.route("**/jspdf.umd.min.js", (r) => r.fulfill({ contentType: "application/javascript", body: JSPDF }));
  await ctx.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
  const p = await ctx.newPage(); const erros = [];
  p.on("pageerror", (e) => erros.push(e.message)); p.on("console", (m) => m.type() === "error" && erros.push(m.text()));
  const shot = (n) => p.screenshot({ path: `${OUT}/${n}.png`, fullPage: true });
  const semScrollX = async () => (await p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1));

  await p.goto(URL); await p.waitForFunction(() => !!window.jspdf && !!window.ZG);
  log(await p.locator("h1").textContent() === "O seu Diagnóstico de Gestão", "abertura carrega");
  await shot("m01-abertura");
  await p.fill("#nome", "Ana Exemplo"); await p.fill("#email", "ana@exemplo.com"); await p.fill("#hospedagem", "Cabanas do Vale (exemplo)");
  await p.fill("#cidade", "Urubici, SC"); await p.selectOption("#tipo", "Cabanas ou chalés");
  await p.fill("#unidades", "-3"); await p.click("#vai"); log(/0 a 999/.test(await p.textContent("#erro")), "unidades negativas recusadas");
  await p.fill("#unidades", "4"); await p.click("#vai");
  log(/Qual destas frases/.test(await p.textContent("h2")), "tela 1: situação");
  log(await p.locator("#vai").isDisabled(), "avançar bloqueado sem resposta");
  await p.locator("label.op", { hasText: "Já opero" }).click(); await shot("m02-situacao"); await p.click("#vai");
  await p.locator("label.op", { hasText: "Eu, sozinho" }).click(); await p.click("#vai");
  log(/cinco perguntas|números você sabe/i.test(await p.textContent(".card")), "tela 3: cinco perguntas");
  // cinco: entrou=2, sobrou=0, ocupacao=1, diaria=2, custo=0  → 5 pontos
  const marca = async (nome, v) => p.locator(`input[name="${nome}"][value="${v}"]`).locator("xpath=..").click();
  await marca("c-entrou", 2); await marca("c-sobrou", 0); await marca("c-ocupacao", 1); await marca("c-diaria", 2);
  log(await p.locator("#vai").isDisabled(), "cinco perguntas: bloqueia com uma faltando");
  await marca("c-custo", 0); await shot("m03-cinco"); await p.click("#vai");
  // áreas 1-4: metas=0, financas=1, preco=1, vendas=2
  await marca("a-metas", 0); await marca("a-financas", 1); await marca("a-preco", 1); await marca("a-vendas", 2); await shot("m04-areas1"); await p.click("#vai");
  // áreas 5-8: pessoas=1, compras=2, operacao=1, qualidade=0  → total áreas 8
  await marca("a-pessoas", 1); await marca("a-compras", 2); await marca("a-operacao", 1); await marca("a-qualidade", 0); await p.click("#vai");
  await p.locator("label.op", { hasText: "Quando dá" }).click(); await p.locator("label.op", { hasText: "Quase todo na operação" }).click(); log(await p.locator("#vai").isDisabled(), "rotina: bloqueia sem a pergunta da saída"); await p.locator("label.op", { hasText: "nunca fiz a conta" }).click(); await shot("m06-rotina"); await p.click("#vai");
  // resultado
  const esperado = Z.calcular({ situacao: "dono", cinco: { entrou: 2, sobrou: 0, ocupacao: 1, diaria: 2, custo: 0 }, areas: { metas: 0, financas: 1, preco: 1, vendas: 2, pessoas: 1, compras: 2, operacao: 1, qualidade: 0 } });
  const nota = (await p.locator(".leitura .nota").textContent()).trim();
  log(nota.startsWith(String(esperado.nota)), `nota na tela = ${esperado.nota} (${nota.replace(/\s+/g, " ")})`);
  log(esperado.nota === 50 && esperado.faixa.rot === "Gestão em construção", "cenário: 8/16 áreas = 30 + 5/10 perguntas = 20 → 50, em construção");
  log((await p.textContent(".leitura .rot")) === esperado.faixa.rot, "faixa na tela");
  log(/Área 1 · Planejamento e metas/.test(await p.textContent(".fragil")), "área frágil = Planejamento e metas (primeira com 0)");
  log(/Módulo 1 · Planejamento/.test(await p.textContent(".card")), "próxima etapa aponta o módulo 1");
  log(/Quanto sobrou, O custo por noite vendida/.test(await p.textContent(".c-at")), "lista os números que não sabe");
  log((await p.inputValue("#acao")) === Z.AREAS[0].acao, "ação sugerida da área frágil preenchida");
  log(/Falta a ação ou o prazo/.test(await p.textContent("#selo")), "selo pendente sem prazo");
  log(/hora marcada/.test(await p.textContent(".c-sig")), "leitura do tempo (quase todo na operação)");
  log(/Achar que sobraria não é saber/.test(await p.textContent(".c-sig")), "leitura da pergunta da saída");
  await p.fill("#prazo", "2026-12-15"); log(/Pronto para avançar/.test(await p.textContent("#selo")), "selo muda para pronto com prazo");
  await p.fill("#acao", "curta"); log(/Falta a ação/.test(await p.textContent("#selo")), "ação curta demais volta a pendente");
  await p.fill("#acao", "Escrever a meta do ano em uma página e revisar todo mês."); log(/Pronto/.test(await p.textContent("#selo")), "ação própria aceita");
  log(await semScrollX(), "sem rolagem horizontal no celular");
  await shot("m07-resultado");
  // PDF
  const [dl] = await Promise.all([p.waitForEvent("download"), p.click("#pdf")]);
  log(dl.suggestedFilename() === "diagnostico-de-gestao-marco-zero.pdf", "PDF baixado: " + dl.suggestedFilename());
  const pdfPath = `${OUT}/diagnostico.pdf`; await dl.saveAs(pdfPath); log(fs.statSync(pdfPath).size > 3000, `PDF com ${fs.statSync(pdfPath).size} bytes`);
  // persistência
  await p.reload(); await p.waitForFunction(() => !!window.ZG);
  log((await p.locator(".leitura .nota").textContent()).trim().startsWith("50"), "recarregar mantém o resultado (salvo no aparelho)");
  log((await p.inputValue("#acao")) === "Escrever a meta do ano em uma página e revisar todo mês." && (await p.inputValue("#prazo")) === "2026-12-15", "ação e prazo persistem");
  // voltar e refazer
  await p.click("#refaz"); log(/Qual destas frases/.test(await p.textContent("h2")), "refazer volta à tela 1");
  log(await p.locator('input[name="sit"][value="dono"]').isChecked(), "respostas anteriores continuam marcadas ao refazer");
  // tela de abertura mostra "continuar"
  await p.goto(URL + "?x=1"); await p.evaluate(() => { const s = JSON.parse(localStorage.getItem("zion-t2-marco-zero")); s.tela = 0; localStorage.setItem("zion-t2-marco-zero", JSON.stringify(s)); });
  await p.reload(); await p.waitForFunction(() => !!window.ZG);
  log(await p.locator("#retoma").isVisible(), "abertura oferece continuar de onde parei");
  await p.click("#retoma"); log(/diagnóstico de gestão/i.test(await p.textContent(".eyebrow")), "continuar leva ao resultado quando tudo respondido");
  // desktop
  const d = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await d.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
  await d.goto(URL); await d.waitForFunction(() => !!window.ZG); await d.screenshot({ path: `${OUT}/d01-abertura.png`, fullPage: true });
  log(erros.length === 0, "sem erros de JavaScript" + (erros.length ? ": " + erros.join(" | ") : ""));
  await b.close();
  console.log(`\n${ok} ok, ${fal} falhou`); process.exit(fal ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });

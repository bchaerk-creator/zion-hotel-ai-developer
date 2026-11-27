// Teste de ponta a ponta da ficha "Faça agora · O meu CAPEX" no celular (iPhone 13, Playwright).
// Uso: node producao/trilha1-aprofundamento/01-capex/tests/test_e2e.js [caminho/jspdf.umd.min.js]
// Sobe um servidor local de docs/ na porta 8790 e serve o jsPDF 2.5.1 do pacote npm no lugar do cdnjs (bloqueado aqui).
"use strict";
const { chromium, devices } = require("playwright");
const fs = require("fs"), path = require("path"), { spawn } = require("child_process");
const Z = require("../src/logic.js");
const RAIZ = path.resolve(__dirname, "../../../..");
const DOCS = path.join(RAIZ, "docs");
const OUT = path.resolve(__dirname, "../demonstracao");
const TMP = path.join(process.env.CAPEX_E2E_TMP || require("os").tmpdir(), "capex-e2e");
const PORTA = 8790, URL = `http://localhost:${PORTA}/trilha1/capex/`;
function acharJsPDF() {
  const cands = [process.argv[2], process.env.JSPDF];
  try { cands.push(require.resolve("jspdf/dist/jspdf.umd.min.js", { paths: [__dirname, process.cwd()] })); } catch (e) {}
  for (const c of cands) if (c && fs.existsSync(c)) return c;
  throw new Error("jsPDF não encontrado: passe o caminho de jspdf.umd.min.js (npm install jspdf@2.5.1 numa pasta de trabalho).");
}
const JSPDF = fs.readFileSync(acharJsPDF(), "utf8");
let ok = 0, fal = 0;
const log = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
fs.mkdirSync(OUT, { recursive: true }); fs.mkdirSync(TMP, { recursive: true });

(async () => {
  const srv = spawn("python3", ["-m", "http.server", String(PORTA), "--bind", "127.0.0.1", "--directory", DOCS], { stdio: "ignore" });
  await new Promise((r) => setTimeout(r, 900));
  const b = await chromium.launch();
  const ctx = await b.newContext({ ...devices["iPhone 13"], deviceScaleFactor: 1, acceptDownloads: true });
  const externos = [];
  await ctx.route("**/*", (rt) => {
    const u = rt.request().url();
    if (u.startsWith(`http://localhost:${PORTA}/`)) return rt.continue();
    if (u === "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js") return rt.fulfill({ contentType: "application/javascript", body: JSPDF });
    if (u.startsWith("https://fonts.googleapis.com/") || u.startsWith("https://fonts.gstatic.com/")) return rt.fulfill({ contentType: "text/css", body: "" });
    externos.push(u); return rt.abort();
  });
  const p = await ctx.newPage();
  const erros = [];
  p.on("pageerror", (e) => erros.push(e.message));
  p.on("console", (m) => m.type() === "error" && erros.push(m.text()));
  p.on("dialog", (d) => d.accept());
  const semRolagemX = async () => p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
  const texto = async (sel) => ((await p.textContent(sel)) || "").trim();
  const avancar = async () => { await p.click("#avancar"); await p.waitForTimeout(80); };
  const telasSemRolagem = [];
  const conferirTela = async (nome) => { const s = await semRolagemX(); telasSemRolagem.push(s); if (!s) console.log("    rolagem horizontal em " + nome); };

  await p.goto(URL);
  await p.waitForFunction(() => !!window.ZCAPEX && !!window.jspdf);
  const HOJE = await p.evaluate(() => { const d = new Date(); d.setHours(12, 0, 0, 0); const q = (n) => String(n).padStart(2, "0"); return d.getFullYear() + "-" + q(d.getMonth() + 1) + "-" + q(d.getDate()); });
  log((await texto("h1")) === "O meu CAPEX", "abertura carrega com o título O meu CAPEX");
  log(await p.isVisible("text=Material educativo"), "aviso educativo visível (não substitui engenheiro, arquiteto ou contador)");
  log(/não substitui engenheiro, arquiteto ou contador/.test(await p.textContent("body")), "aviso cita engenheiro, arquiteto e contador");
  log(await p.locator("#avancar").isDisabled(), "Começar bloqueado sem respostas");
  log((await p.inputValue("#f-projeto")) === "" && (await p.inputValue("#f-nome")) === "", "nenhum valor pré-preenchido na abertura");
  await conferirTela("abertura");
  await p.screenshot({ path: path.join(OUT, "01-abertura-celular.png") });

  // ---------- o exemplo pelo botão ----------
  await p.click("#ver-exemplo");
  log((await p.inputValue("#f-projeto")) === "Chalés do Ribeirão", "botão do exemplo carrega os Chalés do Ribeirão");
  log(await p.isVisible(".faixa-ex"), "rótulo 'dados fictícios' aparece com o exemplo");
  log(!(await p.locator("#avancar").isDisabled()), "com o exemplo, Começar liberado");
  await avancar();
  log((await p.inputValue("#f-palpite")) === "700000", "tela 1: palpite de R$ 700.000");
  await conferirTela("palpite"); await avancar();
  log((await p.inputValue("#f-unidadesFase")) === "4" && (await p.inputValue("#f-unidadesProjeto")) === "6", "tela 2: 4 unidades na fase e 6 no projeto");
  await p.fill("#f-unidadesFase", "0");
  log(await p.locator("#avancar").isDisabled(), "zero unidades bloqueia o Avançar");
  await p.fill("#f-unidadesFase", "4");
  await conferirTela("fase"); await avancar();

  // ---------- bloco 1 e uma linha à mão ----------
  log((await texto("#tot-bloco")) === "R$ 40.000,00", "bloco 1: total R$ 40.000,00 na tela");
  const n1 = await p.locator("#linhas .lin").count();
  await p.click("#mais-linha");
  log((await p.locator("#linhas .lin").count()) === n1 + 1, "linha nova acrescentada à mão");
  log(await p.locator("#avancar").isDisabled(), "linha sem nome e sem origem bloqueia o Avançar");
  await p.fill(`#l-1-${n1}-nome`, "Sondagem do solo");
  await p.locator(`#lin-1-${n1} label.chip`, { hasText: "Estimativa minha" }).click();
  await p.fill(`#l-1-${n1}-valor`, "2.000");
  log((await texto(`#lt-1-${n1}`)) === "R$ 2.000,00", "linha à mão: R$ 2.000,00");
  log((await texto("#tot-bloco")) === "R$ 42.000,00", "bloco 1 com a linha à mão: R$ 42.000,00");
  log(!(await p.locator("#avancar").isDisabled()), "linha completa libera o Avançar");
  const estado = async () => p.evaluate(() => JSON.parse(localStorage.getItem("zion-t1-pilar6a")));
  let st = await estado();
  const Cm = Z.calcular(st.respostas, HOJE);
  log(Math.abs(Cm.capexFase - 1164375) < 1e-6, "lógica com a linha à mão: CAPEX R$ 1.164.375 ((1.010.500 + 2.000) × 1,15)");
  await p.click(`#lin-1-${n1} .lin-x`);
  log((await texto("#tot-bloco")) === "R$ 40.000,00", "linha apagada: volta a R$ 40.000,00");
  await conferirTela("bloco 1"); await avancar();

  // ---------- bloco 2 ----------
  log((await texto("#tot-bloco")) === "R$ 170.000,00" && (await p.inputValue("#f-distanciaEnergiaM")) === "180", "bloco 2: R$ 170.000,00 e 180 m até a energia");
  await conferirTela("bloco 2"); await avancar();

  // ---------- bloco 3 e a soma das tipologias ----------
  log((await texto("#tot-bloco")) === "R$ 682.000,00", "bloco 3: R$ 682.000,00");
  log(/somam 4 de 4/.test(await texto("#tip-soma")), "tipologias somam 4 de 4");
  await p.fill("#l-3-0-qtd", "3");
  log(await p.locator("#avancar").isDisabled() && /somam 3/.test(await texto("#falta")), "tipologias ≠ fase bloqueiam a tela (A17)");
  await p.fill("#l-3-0-qtd", "4");
  log(!(await p.locator("#avancar").isDisabled()), "tipologias de volta a 4: liberado");
  await p.locator("#lin-3-0").scrollIntoViewIfNeeded();
  await p.evaluate(() => window.scrollBy(0, -70));
  await p.screenshot({ path: path.join(OUT, "02-bloco3-linhas-celular.png") });
  await conferirTela("bloco 3"); await avancar();
  log((await texto("#tot-bloco")) === "R$ 85.800,00", "bloco 4: R$ 85.800,00");
  await conferirTela("bloco 4"); await avancar();
  log((await texto("#tot-bloco")) === "R$ 11.700,00", "bloco 5: R$ 11.700,00");
  await conferirTela("bloco 5"); await avancar();
  log((await texto("#tot-bloco")) === "R$ 21.000,00", "bloco 6: R$ 21.000,00");
  await conferirTela("bloco 6"); await avancar();

  // ---------- reserva ----------
  log((await texto("#res-subtotal")) === "R$ 1.010.500,00" && (await texto("#res-valor")) === "R$ 151.575,00", "reserva: subtotal R$ 1.010.500,00 e 15% = R$ 151.575,00");
  await p.fill("#f-contingenciaPct", "12");
  log((await p.locator('#res-alertas [data-id="A4"]').count()) === 1, "reserva a 12% com primeira obra mostra o alerta A4");
  await p.fill("#f-contingenciaPct", "0");
  log(await p.locator("#avancar").isDisabled() && (await p.locator('#res-alertas [data-id="A3z"]').count()) === 1, "reserva 0 bloqueia e mostra A3z");
  await p.fill("#f-contingenciaPct", "15");
  await conferirTela("reserva"); await avancar();

  // ---------- giro e terreno ----------
  log((await texto("#giro-final")) === "R$ 45.000,00", "giro pela calculadora: 3 × R$ 15.000 = R$ 45.000,00");
  await conferirTela("giro"); await avancar();

  // ---------- resultado ----------
  const esperado = { "#r-capex": "R$ 1.162.075,00", "#r-invest": "R$ 1.207.075,00", "#r-unidade": "R$ 290.518,75", "#r-invunidade": "R$ 301.768,75", "#r-m2": "R$ 6.181,25", "#r-subtotal": "R$ 1.010.500,00" };
  for (const [sel, v] of Object.entries(esperado)) log((await texto(sel)) === v, `resultado ${sel} = ${v}`);
  const blocos = ["R$ 40.000,00", "R$ 170.000,00", "R$ 682.000,00", "R$ 85.800,00", "R$ 11.700,00", "R$ 21.000,00", "R$ 151.575,00"];
  const pesos = ["3,4%", "14,6%", "58,7%", "7,4%", "1,0%", "1,8%", "13,0%"];
  let blocosOk = true;
  for (let k = 1; k <= 7; k++) { const tds = await p.$$eval(`#r-b${k} td`, (x) => x.map((t) => t.textContent.trim())); if (tds[1] !== blocos[k - 1] || tds[2] !== pesos[k - 1]) { blocosOk = false; console.log("    bloco", k, tds); } }
  log(blocosOk, "os sete blocos com valor e peso do plano");
  st = await estado();
  const C = Z.calcular(st.respostas, HOJE);
  log((await texto("#r-capex")) === Z.brl(C.capexFase) && (await texto("#r-invest")) === Z.brl(C.investimentoTotal), "números da tela batem com logic.js sobre o estado salvo");
  const top = await p.$$eval("#p-atencao > .alerta[data-id]", (x) => x.map((a) => a.dataset.id));
  log(top.join() === "A11,A13,A14", "Atenção: A11, A13 e A14 (os três primeiros)");
  log(top.join() === Z.tresPrimeiros(Z.alertas(st.respostas, C)).map((a) => a.id).join(), "alertas da tela iguais aos de logic.js");
  log(/Calculista/.test(await texto("#degrau")) && /Estimador/.test(await texto("#degrau")), "degrau Calculista (diagnóstico Estimador)");
  log(/60,2%/.test(await texto("#r-palpite")) && /R\$ 462\.075,00/.test(await texto("#r-palpite")), "palpite cobria 60,2%, diferença de R$ 462.075,00");
  log(/53,1%/.test(await texto("#r-pctlinhas")) && /94,7%/.test(await texto("#r-pctvalor")), "53,1% das linhas e 94,7% do valor com cotação");
  log(/licença ambiental, internet, segurança, licença de funcionamento e cadastros e seguro do primeiro ano/.test(await texto("#r-acao")), "o que fazer: cotar as cinco linhas em branco");
  log(await p.isVisible("#info"), "bloco fixo Pergunte ao seu engenheiro e ao seu contador");
  for (const id of ["p-resultado", "p-significado", "p-atencao", "p-fazer", "p-verificar"]) log(await p.isVisible("#" + id), "parte do feedback visível: " + id);
  await conferirTela("resultado");
  await p.screenshot({ path: path.join(OUT, "03-resultado-celular.png"), fullPage: true });
  await avancar();

  // ---------- ação, critério, PDF e selo ----------
  log(/Pedir cotação escrita das linhas em branco/.test(await p.inputValue("#f-acao30")), "ação de 30 dias vem pré-preenchida e editável");
  log((await p.inputValue("#f-prazo")) === Z.somaDias(HOJE, 30), "prazo do exemplo em hoje + 30");
  let crit = await p.$$eval("#criterio li", (x) => x.map((l) => l.classList.contains("ok")));
  log(crit.length === 9 && crit.slice(0, 8).every(Boolean) && !crit[8], "critério: 8 de 9 antes do PDF (falta baixar)");
  log((await p.locator("#selo-ok").count()) === 0, "sem selo antes do PDF");
  await p.fill("#f-acao30", "curta");
  log(/10 a 300/.test(await texto("#falta")), "ação curta é apontada");
  await p.click("#usar-sug");
  const [dl] = await Promise.all([p.waitForEvent("download"), p.click("#pdf")]);
  const arq = path.join(TMP, dl.suggestedFilename());
  await dl.saveAs(arq);
  const pdf = fs.readFileSync(arq);
  const pdfTxt = pdf.toString("latin1");
  log(pdf.slice(0, 5).toString() === "%PDF-" && pdf.length > 5000, `PDF baixado (${dl.suggestedFilename()}, ${(pdf.length / 1024).toFixed(1)} KB)`);
  const nPag = (pdfTxt.match(/\/Type \/Page\b(?!s)/g) || []).length;
  const info = await p.evaluate(() => window.__ultimoPDF);
  log(nPag === 2 && info.paginas === 2, "PDF com 2 páginas: a página 6A e o anexo de cotações");
  log(info.yPagina1 <= info.limitePagina1, `página principal cabe em uma folha (fim em ${info.yPagina1.toFixed(1)} mm de ${info.limitePagina1} mm)`);
  log(/O meu CAPEX/.test(pdfTxt) && /Anexo/.test(pdfTxt) && /PRONTO PARA LEVAR/.test(pdfTxt) && /DADOS FICT/.test(pdfTxt), "PDF traz título, selo, anexo e o rótulo de dados fictícios");
  log(/R\$ 1\.162\.075,00/.test(pdfTxt) && /R\$ 1\.207\.075,00/.test(pdfTxt) && /R\$ 288\.900,00/.test(pdfTxt), "PDF traz CAPEX, investimento total e a infraestrutura comum da página 6");
  log(await p.isVisible("#selo-ok"), "selo 'Pronto para levar à página 6' depois do PDF");
  crit = await p.$$eval("#criterio li", (x) => x.map((l) => l.classList.contains("ok")));
  log(crit.every(Boolean), "critério de conclusão: 9 de 9");
  await conferirTela("ação");
  await p.locator("#selo").scrollIntoViewIfNeeded();
  await p.screenshot({ path: path.join(TMP, "04-selo.png") });

  // ---------- persistência ao recarregar ----------
  await p.reload(); await p.waitForFunction(() => !!window.ZCAPEX);
  log(await p.isVisible("#continuar"), "ao recarregar: 'Continuar de onde parei'");
  log((await p.inputValue("#f-projeto")) === "Chalés do Ribeirão", "ao recarregar: respostas mantidas no aparelho");
  await p.click("#continuar");
  log(await p.isVisible("#selo-ok") && (await p.inputValue("#f-prazo")) === Z.somaDias(HOJE, 30), "continuar volta à tela da ação, com selo e prazo");
  st = await estado();
  log(st.resumo && st.resumo.dados && st.resumo.dados.capex_fase === 1162075 && st.resumo.dados.investimento_total === 1207075 && st.respostas.pdfBaixado === true, "salvo em zion-t1-pilar6a com respostas e resumo.dados");

  // ---------- refazer ----------
  await p.click("#refazer");
  log((await texto("h1")) === "O meu CAPEX" && (await p.inputValue("#f-projeto")) === "", "Refazer apaga e volta à abertura vazia");
  st = await estado();
  log(!st || !st.respostas.projeto, "Refazer limpa o aparelho");
  // preenchimento à mão da abertura
  await p.fill("#f-projeto", "Meu projeto");
  log(await p.locator("#avancar").isDisabled(), "abertura segue bloqueada sem situação e diagnóstico");
  await p.locator("label.op", { hasText: "Tenho terreno e ainda não construí" }).click();
  await p.locator("label.op", { hasText: "Cabanas ou chalés" }).click();
  for (const t of ["Tenho um palpite", "Só a unidade", "Nenhuma"]) await p.locator("label.op", { hasText: t }).first().click();
  await p.locator("fieldset", { hasText: "regra escrita" }).locator("label.op", { hasText: "Não" }).click();
  log(!(await p.locator("#avancar").isDisabled()), "abertura preenchida à mão libera o Começar");
  await avancar();
  await p.fill("#f-palpite", "-5");
  log(await p.locator("#avancar").isDisabled(), "palpite negativo bloqueia");
  await p.click("#ns-palpite");
  log(!(await p.locator("#avancar").isDisabled()), "Não sei no palpite é aceito");
  await avancar(); await p.fill("#f-unidadesFase", "2"); await p.click("#ns-unidadesProjeto");
  await p.locator("label.op", { hasText: "Sim, é a minha primeira obra" }).click(); await avancar();
  const nomes = await p.$$eval("#linhas .lin input[data-l$=':nome']", (x) => x.map((i) => i.value));
  const valores = await p.$$eval("#linhas .lin input[data-l$=':valor']", (x) => x.map((i) => i.value));
  log(nomes.length === 5 && nomes[0] === "Arquitetura" && valores.length === 0, "bloco 1 novo: linhas sugeridas só com o nome, sem valor");
  log(await p.locator("#avancar").isDisabled(), "bloco sem origem nas linhas fica bloqueado");
  await conferirTela("bloco 1 novo");

  // ---------- fechamento ----------
  log(telasSemRolagem.length >= 14 && telasSemRolagem.every(Boolean), `sem rolagem horizontal em ${telasSemRolagem.length} telas`);
  log(erros.length === 0, "sem erro de JavaScript" + (erros.length ? ": " + erros.join(" | ") : ""));
  log(externos.length === 0, "nenhum envio para fora (só o jsPDF e as fontes, servidos localmente)" + (externos.length ? ": " + externos.join(" ") : ""));
  await b.close(); srv.kill();
  console.log(`\n${ok} verificações aprovadas, ${fal} falharam (ponta a ponta no celular).`);
  process.exit(fal ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });

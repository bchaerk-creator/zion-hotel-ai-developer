// Teste de ponta a ponta da ficha "Faça agora · O seu CAPEX" (página 6A) no celular (iPhone 13, Playwright).
// Uso: node producao/trilha1-aprofundamento/01-capex/tests/test_e2e.js [caminho/jspdf.umd.min.js]
// Sobe um servidor local de docs/ na porta 8790 e serve o jsPDF 2.5.1 do pacote npm no lugar do cdnjs (bloqueado aqui).
// Dois casos: (1) sem a página 6 no aparelho, com o botão da Marina e o caminho à mão;
//             (2) com a página 6, a página 5, o Marco Zero e o que a aula interativa grava, semeados no localStorage.
"use strict";
const { chromium, devices } = require("playwright");
const fs = require("fs"), path = require("path"), { spawn } = require("child_process");
const Z = require("../src/logic.js");
const RAIZ = path.resolve(__dirname, "../../../..");
const DOCS = path.join(RAIZ, "docs");
const OUT = path.resolve(__dirname, "../demonstracao");
const TMP = path.join(process.env.CAPEX_E2E_TMP || require("os").tmpdir(), "capex-e2e");
const PORTA = 8790, URL = `http://localhost:${PORTA}/trilha1/pilar6a/`;
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

/* A página 6 da Marina como a ficha do Pilar 6 grava (zion-t1-pilar6: perfil + resumo.dados + resumo.data). */
const PAG6 = { versao: 1, pilar: 6, perfil: { nome: "Marina", email: "", cidade: "Cidade do exemplo", uf: "SC" }, respostas: {}, atualizado: "2026-11-13T12:00:00.000Z",
  resumo: { pilar: 6, data: "2026-11-13", dados: { unidades: 3, unidade_pronta: 192346, soma_folha: 649741.8, infra: null, giro: 40787.38, giro_meses: 3, total: 690529.18, total_sem_giro: 649741.8, por_chave: 230176.39, terreno: 600000, resultado_cons: 108766.35, inv8: 870130.8, folga8: 179601.62 } } };
const PAG5 = { versao: 1, pilar: 5, perfil: { nome: "Marina" }, resumo: { dados: { unidades_fase1: 3, unidades_projeto_completo: 5, rede_para: 5 } } };
const MZ = { tela: 5, nome: "Marina", situacao: "terreno", dor: "" };
const AULA = { respostas: { d3: "algumas", palpite: 700000, dataPalpite: "2026-11-01" }, aulaExtras: { slide: 7, respostas: { cotadas: "algumas" } }, atualizado: "2026-11-20T10:00:00.000Z" };

(async () => {
  const srv = spawn("python3", ["-m", "http.server", String(PORTA), "--bind", "127.0.0.1", "--directory", DOCS], { stdio: "ignore" });
  await new Promise((r) => setTimeout(r, 900));
  const b = await chromium.launch();
  const externos = [], erros = [];
  async function novoContexto() {
    const ctx = await b.newContext({ ...devices["iPhone 13"], deviceScaleFactor: 1, acceptDownloads: true });
    await ctx.route("**/*", (rt) => {
      const u = rt.request().url();
      if (u.startsWith(`http://localhost:${PORTA}/`)) return rt.continue();
      if (u === "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js") return rt.fulfill({ contentType: "application/javascript", body: JSPDF });
      if (u.startsWith("https://fonts.googleapis.com/") || u.startsWith("https://fonts.gstatic.com/")) return rt.fulfill({ contentType: "text/css", body: "" });
      externos.push(u); return rt.abort();
    });
    const p = await ctx.newPage();
    p.on("pageerror", (e) => erros.push(e.message));
    p.on("console", (m) => m.type() === "error" && erros.push(m.text()));
    p.on("dialog", (d) => d.accept());
    return { ctx, p };
  }
  let { ctx, p } = await novoContexto();
  const semRolagemX = async () => p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
  const texto = async (sel) => ((await p.textContent(sel)) || "").trim();
  const avancar = async () => { await p.click("#avancar"); await p.waitForTimeout(80); };
  const telasSemRolagem = [];
  const conferirTela = async (nome) => { const s = await semRolagemX(); telasSemRolagem.push(s); if (!s) console.log("    rolagem horizontal em " + nome); };
  const estado = async () => p.evaluate(() => JSON.parse(localStorage.getItem("zion-t1-pilar6a")));

  /* ======================= Caso 1 · sem a página 6 no aparelho ======================= */
  console.log("Caso 1 · sem a página 6 no aparelho (botão da Marina e caminho à mão)");
  await p.goto(URL);
  await p.waitForFunction(() => !!window.ZCAPEX && !!window.jspdf);
  const HOJE = await p.evaluate(() => { const d = new Date(); d.setHours(12, 0, 0, 0); const q = (n) => String(n).padStart(2, "0"); return d.getFullYear() + "-" + q(d.getMonth() + 1) + "-" + q(d.getDate()); });
  log((await texto("h1")) === "O seu CAPEX" && (await p.title()) === "Faça agora · O seu CAPEX", "abertura: título O seu CAPEX (Faça agora · O seu CAPEX)");
  log(/Pilar 6/.test(await texto(".topo .etiqueta")) && /Aprofundamento 6A · CAPEX/.test(await texto(".topo .etiqueta")), "cabeçalho Zion · Método Zion / Pilar 6 / Aprofundamento 6A · CAPEX");
  log(/Você já fez a página 6 no Pilar 6/.test(await texto(".lead")), "abertura retoma a página 6 («Você já fez a página 6 no Pilar 6…»)");
  log(/Material educativo/.test(await p.textContent("body")) && /Esta ficha não envia nada/.test(await p.textContent("body")), "aviso educativo e «Esta ficha não envia nada» visíveis");
  const sitTextos = await p.$$eval("input[name=r-situacao] + span", (x) => x.map((s) => s.textContent));
  log(sitTextos.join("|") === Z.SITUACOES.map((s) => s.r).join("|"), "situações com as palavras do Marco Zero");
  log(await p.locator("#avancar").isDisabled(), "Começar bloqueado sem respostas");
  log((await p.inputValue("#f-projeto")) === "" && (await p.inputValue("#f-nome")) === "", "nada pré-preenchido quando o aparelho não tem outras fichas");
  await conferirTela("abertura");
  await p.screenshot({ path: path.join(OUT, "01-abertura-celular.png") });

  // ---------- a Marina pelo botão ----------
  await p.click("#ver-exemplo");
  log((await p.inputValue("#f-projeto")) === "Cabanas da Marina", "botão do exemplo carrega a Marina");
  log((await texto(".faixa-ex")) === "Exemplo ilustrativo · dados fictícios. Não são preços de referência.", "rótulo «Exemplo ilustrativo · dados fictícios» aparece");
  log(!(await p.locator("#avancar").isDisabled()), "com o exemplo, Começar liberado");
  await avancar();
  log((await p.inputValue("#f-pagina6Total")) === "690.529,18" && (await p.inputValue("#f-limite6")) === "870.130,80", "tela 1: página 6 de R$ 690.529,18 e limite de R$ 870.130,80");
  log(/não confirmada; a Zion também vende esse tipo de estrutura/.test(await texto("#p6-ref")), "tela 1: rótulo da referência orientativa da página 6");
  log((await p.locator('[data-veio="pagina6Total"]').count()) === 1, "tela 1: «Veio da página 6» ao lado do número");
  await conferirTela("página 6");
  await p.screenshot({ path: path.join(OUT, "02-pagina6-marina-celular.png") });
  await avancar();
  log((await p.inputValue("#f-unidadesFase")) === "3" && (await p.inputValue("#f-unidadesProjeto")) === "5", "tela 2: 3 unidades na fase um e 5 no projeto completo");
  await p.fill("#f-unidadesFase", "0");
  log(await p.locator("#avancar").isDisabled(), "zero unidades bloqueia o Avançar");
  await p.fill("#f-unidadesFase", "3");
  await conferirTela("fase"); await avancar();

  // ---------- Parte 1 e uma linha à mão ----------
  log((await texto("h1")) === "Parte 1 · Projetos, licenças e documentação" && (await texto("#tot-parte")) === "R$ 36.000,00", "Parte 1: título «Parte 1 · …» e total R$ 36.000,00");
  const n1 = await p.locator("#linhas .lin").count();
  await p.click("#mais-linha");
  log((await p.locator("#linhas .lin").count()) === n1 + 1, "linha nova acrescentada à mão");
  log(await p.locator("#avancar").isDisabled(), "linha sem nome e sem origem bloqueia o Avançar");
  await p.fill(`#l-1-${n1}-nome`, "Estudo de solo complementar");
  await p.locator(`#lin-1-${n1} label.chip`, { hasText: "Estimativa minha" }).click();
  await p.fill(`#l-1-${n1}-valor`, "2.000");
  log((await texto(`#lt-1-${n1}`)) === "R$ 2.000,00", "linha à mão: R$ 2.000,00");
  log((await texto("#tot-parte")) === "R$ 38.000,00", "Parte 1 com a linha à mão: R$ 38.000,00");
  log(!(await p.locator("#avancar").isDisabled()), "linha completa libera o Avançar");
  let st = await estado();
  const Cm = Z.calcular(st.respostas, HOJE);
  log(Math.abs(Cm.capexFase - 793431) < 1e-6, "lógica com a linha à mão: CAPEX R$ 793.431 ((687.940 + 2.000) × 1,15)");
  await p.click(`#lin-1-${n1} .lin-x`);
  log((await texto("#tot-parte")) === "R$ 36.000,00", "linha apagada: volta a R$ 36.000,00");
  await conferirTela("Parte 1"); await avancar();

  // ---------- Parte 2 ----------
  log((await texto("#tot-parte")) === "R$ 128.200,00" && (await p.inputValue("#f-distanciaEnergiaM")) === "260" && (await p.inputValue("#f-infraDimensionadaPara")) === "5", "Parte 2: R$ 128.200,00, energia a 260 m, rede para 5");
  await conferirTela("Parte 2"); await avancar();

  // ---------- Parte 3 e a soma das tipologias ----------
  log((await texto("#tot-parte")) === "R$ 428.400,00", "Parte 3: R$ 428.400,00");
  log(/somam 3 de 3/.test(await texto("#tip-soma")), "tipologias somam 3 de 3");
  await p.fill("#l-3-0-qtd", "2");
  log(await p.locator("#avancar").isDisabled() && /somam 2/.test(await texto("#falta")), "tipologias ≠ fase bloqueiam a tela (A17)");
  await p.fill("#l-3-0-qtd", "3");
  log(!(await p.locator("#avancar").isDisabled()), "tipologias de volta a 3: liberado");
  await p.locator("#lin-3-0").scrollIntoViewIfNeeded();
  await p.evaluate(() => window.scrollBy(0, -70));
  await p.screenshot({ path: path.join(OUT, "03-parte3-linhas-celular.png") });
  await conferirTela("Parte 3"); await avancar();
  log((await texto("#tot-parte")) === "R$ 72.000,00", "Parte 4: R$ 72.000,00");
  await conferirTela("Parte 4"); await avancar();
  log((await texto("#tot-parte")) === "R$ 10.740,00", "Parte 5: R$ 10.740,00");
  await conferirTela("Parte 5"); await avancar();
  log((await texto("#tot-parte")) === "R$ 12.600,00", "Parte 6: R$ 12.600,00");
  await conferirTela("Parte 6"); await avancar();

  // ---------- Parte 7 · reserva ----------
  log((await texto("#res-subtotal")) === "R$ 687.940,00" && (await texto("#res-valor")) === "R$ 103.191,00", "Parte 7: subtotal R$ 687.940,00 e 15% = R$ 103.191,00");
  await p.fill("#f-reservaPct", "10");
  log((await texto("#res-valor")) === "R$ 68.794,00" && (await p.locator('#res-alertas [data-id="A4"]').count()) === 1, "reserva a 10% (R$ 68.794,00) com primeira obra mostra o alerta A4");
  await p.fill("#f-reservaPct", "0");
  log(await p.locator("#avancar").isDisabled() && (await p.locator('#res-alertas [data-id="A3z"]').count()) === 1, "reserva 0 bloqueia e mostra A3z");
  await p.fill("#f-reservaPct", "15");
  await conferirTela("reserva"); await avancar();

  // ---------- giro e terreno ----------
  log((await p.inputValue("#f-giro")) === "40.787,38" && (await p.locator('[data-veio="giro"]').count()) === 1, "giro de R$ 40.787,38, com «Veio da página 6»");
  log(await p.locator('input[name=r-terrenoSituacao][value="meu"]').isChecked() && (await p.inputValue("#f-terrenoValor")) === "600.000", "terreno: já é dela, R$ 600.000, fora da soma");
  await conferirTela("giro"); await avancar();

  // ---------- resultado ----------
  const esperado = { "#r-capex": "R$ 791.131,00", "#r-invest": "R$ 831.918,38", "#r-limite": "R$ 870.130,80", "#r-folga": "folga de R$ 38.212,42", "#r-unidade": "R$ 263.710,33", "#r-invunidade": "R$ 277.306,13", "#r-m2": "R$ 3.803,51", "#r-subtotal": "R$ 687.940,00" };
  for (const [sel, v] of Object.entries(esperado)) log((await texto(sel)) === v, `resultado ${sel} = ${v}`);
  const partes = ["R$ 36.000,00", "R$ 128.200,00", "R$ 428.400,00", "R$ 72.000,00", "R$ 10.740,00", "R$ 12.600,00", "R$ 103.191,00"];
  const pesos = ["4,6%", "16,2%", "54,2%", "9,1%", "1,4%", "1,6%", "13,0%"];
  let partesOk = true;
  for (let k = 1; k <= 7; k++) { const tds = await p.$$eval(`#r-p${k} td`, (x) => x.map((t) => t.textContent.trim())); if (tds[1] !== partes[k - 1] || tds[2] !== pesos[k - 1] || !/^Parte \d/.test(tds[0])) { partesOk = false; console.log("    parte", k, tds); } }
  log(partesOk, "as sete partes com valor e peso do plano (4,6 / 16,2 / 54,2 / 9,1 / 1,4 / 1,6 / 13,0)");
  st = await estado();
  const C = Z.calcular(st.respostas, HOJE);
  log((await texto("#r-capex")) === Z.brl(C.capexFase) && (await texto("#r-invest")) === Z.brl(C.investimentoTotal) && (await texto("#r-folga")) === "folga de " + Z.brl(C.folga6), "números da tela batem com logic.js sobre o estado salvo");
  const top = await p.$$eval("#p-atencao > .alerta[data-id]", (x) => x.map((a) => a.dataset.id));
  log(top.join() === "A11,A13,A14", "Atenção: A11, A13 e A14");
  log(top.join() === Z.tresPrimeiros(Z.alertas(st.respostas, C)).map((a) => a.id).join(), "alertas da tela iguais aos de logic.js");
  log(/Degrau Estimador/.test(await texto("#degrau")) && /mesmo degrau do diagnóstico/.test(await texto("#degrau")) && /Faltam 4 linhas cotadas/.test(await texto("#degrau")), "degrau Estimador (o mesmo do diagnóstico), faltam 4 linhas cotadas");
  log((await texto("#r-pagina6")) === "A sua página 6 cobria 83,0% da 6A; a diferença é de R$ 141.389,20.", "página 6 × 6A: cobria 83,0%, diferença de R$ 141.389,20");
  log(/Cabe no limite da página 6/.test(await texto("#r-limite-leitura")) && /R\$ 33\.228,19/.test(await texto("#r-limite-leitura")), "leitura do limite: cabe, e a folga paga R$ 33.228,19 de linhas novas");
  log(/41,0%/.test(await texto("#r-pctlinhas")) && /16 de 39/.test(await texto("#r-pctlinhas")) && /89,1%/.test(await texto("#r-pctvalor")), "41,0% das linhas (16 de 39) e 89,1% do valor com cotação");
  log((await texto("#r-acao")) === "Pedir cotação escrita das linhas em branco: licença ambiental, internet, segurança, licença de funcionamento e seguro do primeiro ano.", "o que fazer: cotar as cinco linhas em branco");
  log((await texto("#r-verifica")) === "As cinco propostas, com data e escopo, lançadas na ficha.", "como verificar: as cinco propostas");
  log(await p.isVisible("#info"), "bloco fixo Pergunte ao seu engenheiro e ao seu contador");
  for (const id of ["p-resultado", "p-significado", "p-atencao", "p-fazer", "p-verificar"]) log(await p.isVisible("#" + id), "parte do feedback visível: " + id);
  await conferirTela("resultado");
  await p.screenshot({ path: path.join(OUT, "04-resultado-celular.png"), fullPage: true });
  await avancar();

  // ---------- ação, quadros, critério, PDF e selo ----------
  log(/Pedir cotação escrita das linhas em branco/.test(await p.inputValue("#f-acao30")), "ação de 30 dias vem pré-preenchida e editável");
  log((await p.inputValue("#f-prazo")) === Z.somaDias(HOJE, 30), "prazo do exemplo em hoje + 30");
  log(/R\$ 106\.400,00 · nota 3/.test(await texto("#q-unidade")) && /R\$ 26\.780,00 · nota 1/.test(await texto("#q-mobilia")) && /R\$ 147\.780,00/.test(await texto("#q-pronta")) && /R\$ 245\.290,00 · nota 1/.test(await texto("#q-infra")), "quadro «Como levar para a página 6»: 106.400 (3), 26.780 (1), pronta 147.780, infraestrutura comum 245.290 (1)");
  log(/Digite 0 onde for zero/.test(await texto("#quadro")), "quadro avisa: digite 0 onde for zero");
  log(/R\$ 352\.800,00/.test(await texto("#pl1-premissas")) && /R\$ 252\.400,00/.test(await texto("#pl1-infra")) && /R\$ 69\.600,00/.test(await texto("#pl1-ffe")) && /R\$ 13\.140,00/.test(await texto("#pl1-ose")) && /R\$ 791\.131,00/.test(await texto("#pl1-total")), "quadro da Planilha 1: 352.800 + 252.400 + 69.600 + 13.140; TOTAL 791.131");
  log((await p.locator("#quadro-pl1 tbody tr").count()) === 10, "quadro «partes da 6A → abas da Planilha 1» com 10 linhas");
  log(/pasta Meu Dossiê, ao lado da página 6/.test(await texto("#lembrete")) && /Esta ficha não envia nada/.test(await texto("#lembrete")), "lembrete da pasta Meu Dossiê e «Esta ficha não envia nada»");
  log((await p.locator(".passos li").count()) === 6 && /Planilha 2/.test(await texto(".passos")) && !/Ferramenta 05|Calculadora de Implanta/.test(await p.textContent("body")), "próxima etapa na ordem do Mapa, sem produto avulso");
  let crit = await p.$$eval("#criterio li", (x) => x.map((l) => l.classList.contains("ok")));
  log(crit.length === 10 && crit.slice(0, 9).every(Boolean) && !crit[9], "critério: 9 de 10 antes do PDF (falta baixar)");
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
  log(nPag === info.paginas && nPag >= 2 && nPag <= 3, `PDF com a página 6A numa folha e o anexo em seguida (${nPag} páginas no arquivo)`);
  log(info.yPagina1 <= info.limitePagina1, `página 6A cabe em uma folha (fim em ${info.yPagina1.toFixed(1)} mm de ${info.limitePagina1} mm)`);
  log(/Página 6A · CAPEX/.test(pdfTxt) && /O seu CAPEX/.test(pdfTxt) && /Anexo/.test(pdfTxt) && /PRONTO PARA LEVAR/.test(pdfTxt) && /EXEMPLO ILUSTRATIVO/.test(pdfTxt), "PDF traz cabeçalho Página 6A · CAPEX, título, selo, anexo e o rótulo do exemplo");
  log(/R\$ 791\.131,00/.test(pdfTxt) && /R\$ 831\.918,38/.test(pdfTxt) && /folga R\$ 38\.212,42/.test(pdfTxt) && /R\$ 245\.290,00/.test(pdfTxt) && /R\$ 352\.800,00/.test(pdfTxt), "PDF traz CAPEX, investimento total, folga, infraestrutura comum e a Planilha 1");
  log(/83,0%/.test(pdfTxt) && /Meu Dossi/.test(pdfTxt) && /envia nada/.test(pdfTxt), "PDF traz página 6 × 6A, a pasta Meu Dossiê e «não envia nada»");
  log(!/129\.000|192\.346/.test(pdfTxt), "PDF sem preço da Zion Glamping Store");
  log(await p.isVisible("#selo-ok"), "selo «Pronto para levar à página 6» depois do PDF");
  crit = await p.$$eval("#criterio li", (x) => x.map((l) => l.classList.contains("ok")));
  log(crit.every(Boolean), "critério de conclusão: 10 de 10");
  await conferirTela("ação");
  await p.locator("#selo").scrollIntoViewIfNeeded();
  await p.screenshot({ path: path.join(OUT, "05-acao-selo-celular.png") });

  // ---------- persistência ao recarregar ----------
  await p.reload(); await p.waitForFunction(() => !!window.ZCAPEX);
  log(await p.isVisible("#continuar"), "ao recarregar: «Continuar de onde parei»");
  log((await p.inputValue("#f-projeto")) === "Cabanas da Marina", "ao recarregar: respostas mantidas no aparelho");
  await p.click("#continuar");
  log(await p.isVisible("#selo-ok") && (await p.inputValue("#f-prazo")) === Z.somaDias(HOJE, 30), "continuar volta à tela da ação, com selo e prazo");
  st = await estado();
  const d = st.resumo && st.resumo.dados;
  log(d && d.capex_fase === 791131 && d.investimento_total === 831918.38 && d.folga6 === 38212.42 && d.pagina6_total === 690529.18 && st.respostas.pdfBaixado === true && st.respostas.partes && !st.respostas.blocos, "salvo em zion-t1-pilar6a com respostas (partes) e resumo.dados");

  // ---------- refazer e o caminho à mão, sem a página 6 ----------
  await p.click("#refazer");
  log((await texto("h1")) === "O seu CAPEX" && (await p.inputValue("#f-projeto")) === "", "Refazer apaga e volta à abertura vazia");
  st = await estado();
  log(!st || !st.respostas.projeto, "Refazer limpa o aparelho");
  await p.fill("#f-projeto", "Meu projeto");
  log(await p.locator("#avancar").isDisabled(), "abertura segue bloqueada sem situação e diagnóstico");
  await p.locator("label.op", { hasText: "Tenho uma ideia, ou o capital, e ainda não tenho o terreno" }).click();
  await p.locator("label.op", { hasText: "Cabanas ou chalés" }).click();
  await p.locator("fieldset", { hasText: "A sua página 6 tem" }).locator("label.op", { hasText: "Ainda não fiz a página 6" }).click();
  await p.locator("fieldset", { hasText: "já inclui infraestrutura" }).locator("label.op", { hasText: "Não sei" }).click();
  await p.locator("fieldset", { hasText: "Quantas linhas" }).locator("label.op", { hasText: "Nenhuma" }).click();
  await p.locator("fieldset", { hasText: "regra de uso escrita" }).locator("label.op", { hasText: "Não" }).click();
  log(!(await p.locator("#avancar").isDisabled()), "abertura preenchida à mão libera o Começar");
  await avancar();
  log(/Não encontramos a página 6 neste aparelho/.test(await texto("#p6-status")) && (await p.inputValue("#f-pagina6Total")) === "", "tela 1 sem a página 6 no aparelho: aviso e campo vazio");
  log(await p.locator("#avancar").isDisabled(), "tela 1 vazia bloqueia o Avançar");
  await p.fill("#f-pagina6Total", "-5");
  log(await p.locator("#avancar").isDisabled(), "número negativo na página 6 bloqueia");
  await p.click("#nf-pagina6Total");
  log(!(await p.locator("#avancar").isDisabled()) && (await p.locator("#f-pagina6Total").isDisabled()), "«Não fiz a página 6» é aceito");
  await conferirTela("página 6 ausente");
  await p.screenshot({ path: path.join(OUT, "06-pagina6-ausente-celular.png") });
  await avancar(); await p.fill("#f-unidadesFase", "2"); await p.click("#ns-unidadesProjeto");
  await p.locator("label.op", { hasText: "Sim, é a minha primeira obra" }).click(); await avancar();
  const nomes = await p.$$eval("#linhas .lin input[data-l$=':nome']", (x) => x.map((i) => i.value));
  const valores = await p.$$eval("#linhas .lin input[data-l$=':valor']", (x) => x.map((i) => i.value));
  log(nomes.length === 6 && nomes[0] === "Levantamento topográfico e sondagem" && valores.length === 0, "Parte 1 nova: linhas sugeridas só com o nome, sem valor");
  log(await p.locator("#avancar").isDisabled(), "parte sem origem nas linhas fica bloqueada");
  await conferirTela("Parte 1 nova");
  st = await estado();
  const A22 = Z.alertas(st.respostas, Z.calcular(st.respostas, HOJE)).map((a) => a.id);
  log(A22.includes("A22") && !A22.includes("A23"), "sem a página 6: a lógica sobre o estado salvo dá A22 (sem A23)");
  await ctx.close();

  /* ======================= Caso 2 · com a página 6 no aparelho ======================= */
  console.log("Caso 2 · com a página 6, a página 5, o Marco Zero e a aula no aparelho");
  ({ ctx, p } = await novoContexto());
  await p.goto(URL);
  await p.evaluate(([a, b5, mz, aula]) => { localStorage.clear(); localStorage.setItem("zion-t1-pilar6", a); localStorage.setItem("zion-t1-pilar5", b5); localStorage.setItem("zion-t1-marco-zero", mz); localStorage.setItem("zion-t1-pilar6a", aula); }, [JSON.stringify(PAG6), JSON.stringify(PAG5), JSON.stringify(MZ), JSON.stringify(AULA)]);
  const p6Antes = JSON.stringify(PAG6);
  await p.reload(); await p.waitForFunction(() => !!window.ZCAPEX && !!window.jspdf);
  log(await p.locator('input[name=r-situacao][value="terreno"]').isChecked() && /Veio do seu Marco Zero/.test(await p.textContent("body")), "situação pré-marcada a partir do Marco Zero");
  log((await p.inputValue("#f-nome")) === "Marina", "nome lido do perfil salvo nas outras fichas");
  log((await p.inputValue("#f-cidadeUF")) === "Cidade do exemplo/SC", "«Terreno em» lido do perfil da página 6");
  log(await p.locator('input[name=r-d3][value="algumas"]').isChecked(), "resposta d3 gravada pela aula interativa aparece marcada");
  await p.fill("#f-projeto", "Cabanas da Marina");
  await p.locator("label.op", { hasText: "Cabanas ou chalés" }).click();
  await p.locator("fieldset", { hasText: "A sua página 6 tem" }).locator("label.op", { hasText: "Referência ou estimativa" }).click();
  await p.locator("fieldset", { hasText: "já inclui infraestrutura" }).locator("label.op", { hasText: "Nenhuma" }).click();
  await p.locator("fieldset", { hasText: "regra de uso escrita" }).locator("label.op", { hasText: "Não" }).click();
  await conferirTela("abertura lida");
  await avancar();
  log(/Encontramos a sua página 6 neste aparelho/.test(await texto("#p6-status")), "tela 1: «Encontramos a sua página 6 neste aparelho»");
  log((await p.inputValue("#f-pagina6Total")) === "690.529,18" && (await p.inputValue("#f-limite6")) === "870.130,80" && (await p.inputValue("#f-pagina6Data")) === "2026-11-13" && (await p.inputValue("#f-pagina6Infra")) === "", "tela 1 lê total (690.529,18), limite inv8 (870.130,80), data e infraestrutura à parte");
  log((await p.locator('[data-veio="pagina6Total"]').count()) === 1 && (await p.locator('[data-veio="limite6"]').count()) === 1, "«Veio da página 6» no total e no limite");
  log(!(await p.locator("#avancar").isDisabled()), "tela 1 lida libera o Avançar");
  await conferirTela("página 6 lida");
  await p.screenshot({ path: path.join(OUT, "07-pagina6-lida-celular.png") });
  await avancar();
  log((await p.inputValue("#f-unidadesFase")) === "3" && (await p.inputValue("#f-unidadesProjeto")) === "5" && (await p.locator('[data-veio="unidadesFase"]').count()) === 1, "fase: 3 e 5 lidos da página 5");
  st = await estado();
  log(st.respostas.giro === "40.787,38" && st.respostas.terrenoValor === "600.000" && st.respostas.pagina6GiroMeses === "3" && st.respostas.pagina6ResultadoCons === "108.766,35", "giro, terreno e meses de giro da página 6 guardados para as telas seguintes");
  log(st.aulaExtras && st.aulaExtras.slide === 7 && st.respostas.palpite === 700000, "o que a aula gravou na mesma chave continua lá (aulaExtras e campos antigos)");
  log(await p.evaluate((x) => localStorage.getItem("zion-t1-pilar6") === x, p6Antes), "a ficha não altera a página 6 salva (zion-t1-pilar6 intacta)");
  const Cr = Z.calcular(st.respostas, HOJE);
  log(Cr.limite6 === 870130.8 && Cr.pagina6Total === 690529.18, "lógica sobre o estado salvo usa o limite e o total lidos");
  await ctx.close();

  // ---------- fechamento ----------
  log(telasSemRolagem.length >= 17 && telasSemRolagem.every(Boolean), `sem rolagem horizontal em ${telasSemRolagem.length} telas`);
  log(erros.length === 0, "sem erro de JavaScript" + (erros.length ? ": " + erros.join(" | ") : ""));
  log(externos.length === 0, "nenhum envio para fora (só o jsPDF e as fontes, servidos localmente)" + (externos.length ? ": " + externos.join(" ") : ""));
  await b.close(); srv.kill();
  console.log(`\n${ok} verificações aprovadas, ${fal} falharam (ponta a ponta no celular, iPhone 13).`);
  process.exit(fal ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });

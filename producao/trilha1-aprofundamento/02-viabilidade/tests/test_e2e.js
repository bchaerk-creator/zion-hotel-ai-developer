// Teste de ponta a ponta da ficha "Faça agora · A sua conta" (página 6B) no celular (iPhone 13, Playwright).
// Uso: node producao/trilha1-aprofundamento/02-viabilidade/tests/test_e2e.js [caminho/jspdf.umd.min.js]
// Sobe um servidor local de docs/ na porta 8790 e serve o jsPDF 2.5.1 do pacote npm no lugar do cdnjs (bloqueado aqui).
// Dois casos: (1) sem as outras páginas no aparelho: o botão «Exemplo ilustrativo», uma linha à mão, o PDF, recarregar e refazer;
//             (2) com a 6A, a página 6, a página 2 e o Marco Zero semeados no localStorage (leitura presente, sem alterá-las).
"use strict";
const { chromium, devices } = require("playwright");
const fs = require("fs"), path = require("path"), { spawn } = require("child_process");
const Z = require("../src/logic.js");
const RAIZ = path.resolve(__dirname, "../../../..");
const DOCS = path.join(RAIZ, "docs");
const OUT = path.resolve(__dirname, "../demonstracao");
const TMP = path.join(process.env.VIAB_E2E_TMP || require("os").tmpdir(), "viab-e2e");
const PORTA = 8790, URL = `http://localhost:${PORTA}/trilha1/pilar6b/`;
const JSPDF_PADRAO = "/tmp/claude-0/-home-user-zion-hotel-ai-developer/91bcceae-fc21-575c-a018-9785e7142343/scratchpad/jspdf/node_modules/jspdf/dist/jspdf.umd.min.js";
function acharJsPDF() {
  const cands = [process.argv[2], process.env.JSPDF, JSPDF_PADRAO];
  try { cands.push(require.resolve("jspdf/dist/jspdf.umd.min.js", { paths: [__dirname, process.cwd()] })); } catch (e) {}
  for (const c of cands) if (c && fs.existsSync(c)) return c;
  throw new Error("jsPDF não encontrado: passe o caminho de jspdf.umd.min.js (npm install jspdf@2.5.1 numa pasta de trabalho).");
}
const JSPDF = fs.readFileSync(acharJsPDF(), "utf8");
let ok = 0, fal = 0;
const log = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
fs.mkdirSync(OUT, { recursive: true }); fs.mkdirSync(TMP, { recursive: true });

/* As páginas da Marina como as fichas gravam (6A, página 6, página 2, Marco Zero). */
const PAG6A = { versao: 2, pilar: "6A", perfil: { nome: "Marina", cidade: "" }, respostas: { projeto: "Cabanas da Marina" }, atualizado: "2026-11-27T12:00:00.000Z",
  resumo: { pagina: "6A", data: "2026-11-27", dados: { unidades: 3, unidades_projeto: 5, capex_fase: 791131, giro: 40787.38, investimento_total: 831918.38, terreno: 600000, terreno_situacao: "meu", limite6: 870130.8 } } };
const PAG6 = { versao: 1, pilar: 6, perfil: { nome: "Marina", email: "", cidade: "Cidade do exemplo", uf: "SC" }, fontes: { margem: "referencia" }, respostas: {}, atualizado: "2026-11-13T12:00:00.000Z",
  resumo: { pilar: 6, data: "2026-11-13", dados: { unidades: 3, giro: 40787.38, giro_meses: 3, total: 690529.18, terreno: 600000, diaria: 645, ocup_cons: 38.5, ocup_base: 50, ocup_otim: 65, margem: 40, resultado_cons: 108766.35, inv8: 870130.8 } } };
const PAG2 = { versao: 1, pilar: 2, perfil: { nome: "Marina" }, respostas: { meses_alta: "3", meses_fraco: "5", ocup_alta: "64", ocup_media: "40", ocup_fraco: "22" }, resumo: { dados: { diaria_media: 645.45, ocup_ano: 38.5 } } };
const MZ = { tela: 5, nome: "Marina", situacao: "terreno", dor: "" };

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
  const kv = async (sel) => ((await p.textContent(sel + " span:last-child")) || "").trim();
  const avancar = async () => { await p.click("#avancar"); await p.waitForTimeout(80); };
  const travado = async () => p.locator("#avancar").isDisabled();
  const telasSemRolagem = [];
  const conferirTela = async (nome) => { const s = await semRolagemX(); telasSemRolagem.push(s); if (!s) console.log("    rolagem horizontal em " + nome); };
  const estado = async () => p.evaluate(() => JSON.parse(localStorage.getItem("zion-t1-pilar6b")));

  /* ======================= Caso 1 · sem as outras páginas no aparelho ======================= */
  console.log("Caso 1 · sem a 6A no aparelho (botão «Exemplo ilustrativo», uma linha à mão, PDF, recarregar, refazer)");
  await p.goto(URL);
  await p.waitForFunction(() => !!window.ZVIAB && !!window.jspdf);
  const HOJE = await p.evaluate(() => { const d = new Date(); d.setHours(12, 0, 0, 0); const q = (n) => String(n).padStart(2, "0"); return d.getFullYear() + "-" + q(d.getMonth() + 1) + "-" + q(d.getDate()); });
  log((await texto("h1")) === "A sua conta" && (await p.title()) === "Faça agora · A sua conta", "abertura: título A sua conta (Faça agora · A sua conta)");
  log(/Pilar 6/.test(await texto(".topo .etiqueta")) && /Aprofundamento 6B · Viabilidade/.test(await texto(".topo .etiqueta")), "cabeçalho Zion · Método Zion / Pilar 6 / Aprofundamento 6B · Viabilidade");
  log(/Você já fez a página 6 no Pilar 6 e a 6A/.test(await texto(".lead")), "abertura retoma as páginas 6 e 6A");
  log(/primeira conta/.test(await p.textContent("body")) && /conta aberta que decide/.test(await p.textContent("body")), "nota curta: a página 6 era a primeira conta; a conta aberta decide");
  log(/Material educativo/.test(await p.textContent("body")) && /Esta ficha não envia nada/.test(await p.textContent("body")), "aviso educativo e «Esta ficha não envia nada» visíveis");
  const sitTextos = await p.$$eval("input[name=r-situacao] + span", (x) => x.map((s) => s.textContent));
  log(sitTextos.join("|") === Z.SITUACOES.map((s) => s.r).join("|"), "situações com as palavras do Marco Zero");
  log(await travado(), "Começar bloqueado sem respostas");
  log((await p.inputValue("#f-projeto")) === "" && (await p.inputValue("#f-nome")) === "", "nada pré-preenchido quando o aparelho não tem outras fichas");
  log(/Exemplo ilustrativo/.test(await texto("#ver-exemplo")), "botão de exemplo «Exemplo ilustrativo»");
  await conferirTela("abertura");
  await p.screenshot({ path: path.join(OUT, "01-abertura-celular.png") });

  // ---------- a Marina pelo botão ----------
  await p.click("#ver-exemplo");
  log((await p.inputValue("#f-projeto")) === "Cabanas da Marina", "botão do exemplo carrega a Marina");
  log((await texto(".faixa-ex")) === "Exemplo ilustrativo · dados fictícios. Não são preços de referência.", "rótulo «Exemplo ilustrativo · dados fictícios» aparece");
  log(!(await travado()), "com o exemplo, Começar liberado");
  await avancar();
  // tela 1
  log((await p.inputValue("#f-capex")) === "791.131" && (await p.inputValue("#f-giro6A")) === "40.787,38" && (await p.inputValue("#f-unidades")) === "3", "tela 1: CAPEX 791.131 e giro 40.787,38 da 6A, 3 unidades");
  log((await p.locator('[data-veio="capex"]').count()) === 1 && /página 6A/.test(await texto('[data-veio="capex"]')), "tela 1: «Veio da página 6A» ao lado do CAPEX");
  log((await p.inputValue("#f-margem6")) === "40" && /não confirmada; a Zion também vende/.test(await texto("#ref-40")), "tela 1: margem 40% da página 6 com o rótulo da referência orientativa");
  await p.fill("#f-unidades", "0");
  log(await travado(), "tela 1: zero unidades bloqueia o Avançar");
  await p.fill("#f-unidades", "3");
  await conferirTela("de onde você parte");
  await p.screenshot({ path: path.join(OUT, "02-de-onde-parte-celular.png") });
  await avancar();
  // tela 2
  log((await p.inputValue("#f-diaria")) === "645" && (await p.inputValue("#cal-5")) === "alta" && (await p.inputValue("#cal-0")) === "fraco", "tela 2: diária R$ 645, junho alta, janeiro fraco");
  log((await kv("#ocup-cons")) === "38,5%", "tela 2: ocupação do ano 38,5% calculada pelo calendário");
  await p.selectOption("#cal-0", "");
  log(await travado() && /12 meses/.test(await texto("#falta")), "tela 2: calendário incompleto bloqueia o Avançar");
  await p.selectOption("#cal-0", "fraco");
  log(!(await travado()), "tela 2: calendário completo libera");
  await conferirTela("quanto entra"); await avancar();
  // tela 3
  log((await p.inputValue("#f-imposto")) === "6" && /fictícia do contador dela/.test(await texto("#imposto-ficticio")), "tela 3: imposto 6% rotulado como resposta fictícia do contador dela");
  log((await kv("#ded-pct")) === "12,2% da hospedagem", "tela 3: comissão + cartão + cancelamento = 12,2% da hospedagem");
  await p.click("#br-imposto");
  log((await p.locator('[data-id="B1"]').count()) === 1 && !(await travado()), "tela 3: «em branco, aguardando o contador» é aceito e mostra o alerta B1");
  let st = await estado();
  log(Z.calcular(st.respostas, HOJE).A.sugerido === "Redesenhar" && Z.calcular(st.respostas, HOJE).impostoBranco === true, "com o imposto em branco, a lógica dá «antes do imposto» (e Redesenhar continua)");
  await p.click("#br-imposto"); await p.fill("#f-imposto", "6");
  log((await p.inputValue("#f-impostoQuem")) !== "" && !(await travado()), "tela 3: imposto de volta a 6%, com quem e a data");
  await conferirTela("do bruto ao real"); await avancar();
  // tela 4 e uma linha à mão
  log((await texto("#cada-noite")) === "R$ 404,31", "tela 4: o que fica de cada noite R$ 404,31");
  const n4 = await p.locator("#linhas .lin").count();
  await p.click("#mais-linha");
  log((await p.locator("#linhas .lin").count()) === n4 + 1 && await travado(), "linha nova acrescentada à mão; sem nome e origem bloqueia");
  await p.fill(`#v-${n4}-nome`, "Café da manhã simples");
  await p.locator(`#lv-${n4} label.chip`, { hasText: "Estimativa" }).click();
  await p.fill(`#v-${n4}-valor`, "10");
  log((await texto(`#lvt-${n4}`)) === "R$ 10,00 por noite" && (await texto("#cada-noite")) === "R$ 394,31", "linha à mão: R$ 10 por noite; cada noite passa a R$ 394,31");
  log(!(await travado()), "linha completa libera o Avançar");
  st = await estado();
  const Cm = Z.calcular(st.respostas, HOJE);
  log(Z.brl(Cm.A.cons.sobra) === "R$ 53.604,04", "lógica com a linha à mão: sobra R$ 53.604,04 (421,575 × 394,31 − 112.627,20)");
  await p.click(`#lv-${n4} .lin-x`);
  log((await texto("#cada-noite")) === "R$ 404,31", "linha apagada: volta a R$ 404,31");
  await conferirTela("custo de cada noite"); await avancar();
  // tela 5
  log((await texto("#fixo-mes")) === "R$ 9.385,60" && (await kv("#retirada")) === "R$ 1.385,60", "tela 5: fixo do mês R$ 9.385,60 com a retirada de R$ 1.385,60");
  await conferirTela("custo de cada mês"); await avancar();
  // tela 6
  log((await kv("#res-sobra")) === "R$ 57.819,79" && (await kv("#res-margem")) === "21,3%", "tela 6: o que sobra R$ 57.819,79, margem 21,3%");
  await p.fill("#f-reservaRep", "2");
  log((await p.locator('#res-alerta [data-id="B9"]').count()) === 1, "tela 6: reserva de 2% mostra o alerta B9");
  await p.fill("#f-reservaRep", "3");
  await conferirTela("reserva"); await avancar();
  // tela 7
  log((await kv("#giro-min")) === "R$ 53.524,02" && (await kv("#giro-b")) === "R$ 50.513,61" && (await kv("#menor")) === "-R$ 22.356,81", "tela 7: giro mínimo 53.524,02, conta B 50.513,61, menor saldo −22.356,81");
  log((await p.locator("#tab-meses tbody tr").count()) === 12 && /mar/.test(await texto("#tab-meses tr.tot")), "tela 7: os 12 meses, com março marcado como o menor saldo");
  log((await kv("#colchao")) === "R$ 31.167,21 · 3,9% do CAPEX", "tela 7: colchão R$ 31.167,21 = 3,9% do CAPEX");
  await p.fill("#f-giro6B", "50.000");
  log(await travado() && /53\.524,02/.test(await texto("#falta")), "tela 7: giro abaixo do mínimo bloqueia");
  await p.click("#usar-giro");
  log((await p.inputValue("#f-giro6B")) === "53.524,02" && !(await travado()), "tela 7: «Usar o giro mínimo» libera");
  await conferirTela("primeiro ano e caixa");
  await p.screenshot({ path: path.join(OUT, "03-primeiro-ano-celular.png") });
  await avancar();
  // tela 8
  log((await p.inputValue("#f-taxa")) === "" && (await p.inputValue("#f-multiploSaida")) === "", "tela 8: taxa e múltiplo vazios (nenhuma taxa sugerida)");
  await conferirTela("vale a pena"); await avancar();
  // resultado
  const esperado = { "#r-sobra": "R$ 57.819,79", "#r-margem": "21,3%", "#r-equilibrio": "25,4% · 13,1", "#r-ano1": "-R$ 18.992,04", "#r-volta": "15,0 anos", "#r-invest": "R$ 844.655,02", "#r-veredito": "Redesenhar" };
  for (const [sel, v] of Object.entries(esperado)) log((await texto(sel)) === v, `resultado ${sel} = ${v}`);
  const deg = await p.$$eval("#d-sobra td", (x) => x.map((t) => t.textContent.trim()));
  log(deg.slice(1).join(" | ") === "R$ 57.819,79 | R$ 108.732,53 | R$ 175.140,44", "seis degraus: o que sobra nos três cenários (57.819,79 / 108.732,53 / 175.140,44)");
  log((await kv("#r-voltap6")) === "14,6 anos" && (await kv("#r-voltaterreno")) === "25,4 anos" && (await kv("#r-cpd")) === "R$ 507,85" && (await kv("#r-deq")) === "R$ 468,71", "Pilar 6 14,6 anos; com o terreno 25,4; custo por diária 507,85; diária de equilíbrio 468,71");
  log(/negativo a qualquer taxa/.test(await kv("#r-vp")) && (await kv("#r-queda")) === "R$ 6.806,35", "valor presente negativo a qualquer taxa (soma simples); teste de queda +6.806,35");
  const passos = await p.$$eval("#passos li", (x) => x.map((l) => l.dataset.status));
  log(passos.join() === "passa,passa,redesenhar,redesenhar,ajustar", "cinco passos em semáforo: passa, passa, redesenhar, redesenhar, ajustar");
  st = await estado();
  const C = Z.calcular(st.respostas, HOJE);
  log((await texto("#r-sobra")) === Z.brl(C.A.cons.sobra) && (await texto("#r-volta")) === Z.fmtVolta(C.A.volta.cons) && (await texto("#r-veredito")) === C.A.sugerido, "números da tela batem com logic.js sobre o estado salvo");
  const top = await p.$$eval("#p-atencao > .alerta[data-id]", (x) => x.map((a) => a.dataset.id));
  log(top.join() === "B5,B7,B11" && top.join() === Z.tresPrimeiros(Z.alertas(st.respostas, C)).map((a) => a.id).join(), "Atenção: B5, B7 e B11, iguais aos de logic.js");
  log((await texto("#r-acao")) === "Rodar a 6B com três redesenhos, uma alavanca por vez, e não assinar contrato de obra." && (await texto("#r-verifica")) === "As três versões da 6B salvas, com data.", "o que fazer e como verificar (ordem 2)");
  for (const id of ["p-resultado", "p-significado", "p-atencao", "p-fazer", "p-verificar"]) log(await p.isVisible("#" + id), "parte do feedback visível: " + id);
  log(await p.isVisible("#info") && /Pergunte ao seu contador/.test(await texto("#info")), "bloco fixo «Pergunte ao seu contador»");
  await conferirTela("resultado");
  await p.screenshot({ path: path.join(OUT, "04-resultado-celular.png"), fullPage: true });
  await avancar();
  // alavancas
  log((await texto("#alv-volta")) === "11,8 anos" && (await texto("#alv-passo3")) === "ajustar" && (await texto("#alv-sobra")) === "R$ 74.219,06", "alavanca diária +50: 74.219,06, 11,8 anos, ajustar");
  log((await texto("#aj-veredito")) === "Testar" && (await texto("#aj-volta")) === "8,3 anos" && (await texto("#aj-sobra")) === "R$ 106.638,40", "cenário ajustado (716, 42%, cesta): 106.638,40, 8,3 anos, a ficha mostra Testar");
  await p.selectOption("#alv-tipo", "unidades");
  log((await texto("#alv-volta")) === "mais de 100 anos", "alavanca duas cabanas: mais de 100 anos");
  await p.selectOption("#alv-tipo", "diaria");
  st = await estado();
  log(Z.calcular(st.respostas, HOJE).A.cons.sobra === C.A.cons.sobra, "alavancas não gravam por cima da conta");
  await conferirTela("alavancas");
  await p.screenshot({ path: path.join(OUT, "05-alavancas-celular.png"), fullPage: true });
  await avancar();
  // veredito
  log(await p.locator('input[name=r-vereditoPessoa][value="Redesenhar"]').isChecked() && /12 para 8 anos/.test(await p.inputValue("#f-criterioParar")) && (await texto("#v-sugerido")) === "Redesenhar", "veredito: Redesenhar escrito, critério da Marina, sugestão da régua");
  await p.fill("#f-criterioParar", "curto");
  log(await travado(), "critério curto bloqueia");
  await p.fill("#f-criterioParar", "Se nenhum redesenho passar de 12 para 8 anos com premissas provadas, eu não assino a obra.");
  await conferirTela("veredito"); await avancar();
  // ação, quadros, critério, PDF e selo
  log(/Rodar a 6B com três redesenhos/.test(await p.inputValue("#f-acao30")) && (await p.inputValue("#f-prazo")) === Z.somaDias(HOJE, 30), "ação de 30 dias pré-preenchida e editável, prazo em hoje + 30");
  log((await kv("#q-margem")) === "21,26 · Lista de custos ou extrato (nota 3)" && (await kv("#q-giro")) === "3,00", "quadro «Como levar para a página 6»: margem 21,26 (nota 3) e 3,00 meses de giro");
  log((await texto("#pl2-b5")) === "R$ 791.131,00" && (await texto("#pl2-b7")) === "=53.524,02/B8" && (await texto("#pl2-b11")) === "12,20%" && /R\$ 123,30/.test(await texto("#pl2-b12")), "quadro «Planilha 2, célula a célula»: B5, B7, B11 12,20%, B12 R$ 123,30");
  log(/pasta Meu Dossiê, ao lado das páginas 6 e 6A/.test(await texto("#lembrete")) && /Esta ficha não envia nada/.test(await texto("#lembrete")), "lembrete da pasta Meu Dossiê e «Esta ficha não envia nada»");
  let crit = await p.$$eval("#criterio li", (x) => x.map((l) => l.classList.contains("ok")));
  log(crit.length === 12 && crit.slice(0, 11).every(Boolean) && !crit[11], "critério: 11 de 12 antes do PDF (falta baixar)");
  log((await p.locator("#selo-ok").count()) === 0, "sem selo antes do PDF");
  await p.fill("#f-acao30", "curta");
  log(/10 a 300/.test(await texto("#falta")), "ação curta é apontada");
  await p.click("#usar-sug");
  const [dl] = await Promise.all([p.waitForEvent("download"), p.click("#pdf")]);
  const arq = path.join(TMP, dl.suggestedFilename());
  await dl.saveAs(arq);
  const pdf = fs.readFileSync(arq), pdfTxt = pdf.toString("latin1");
  log(pdf.slice(0, 5).toString() === "%PDF-" && pdf.length > 5000, `PDF baixado (${dl.suggestedFilename()}, ${(pdf.length / 1024).toFixed(1)} KB)`);
  const info = await p.evaluate(() => window.__ultimoPDF);
  const nPag = (pdfTxt.match(/\/Type \/Page\b(?!s)/g) || []).length;
  log(nPag === info.paginas && nPag >= 2 && nPag <= 3, `PDF com a página 6B numa folha e o anexo em seguida (${nPag} páginas)`);
  log(info.yPagina1 <= info.limitePagina1, `página 6B cabe em uma folha (fim em ${info.yPagina1.toFixed(1)} mm de ${info.limitePagina1} mm)`);
  log(/Página 6B · Viabilidade/.test(pdfTxt) && /A sua conta/.test(pdfTxt) && /Alavancas e cen/.test(pdfTxt) && /PRONTO PARA LEVAR/.test(pdfTxt) && /EXEMPLO ILUSTRATIVO/.test(pdfTxt), "PDF traz cabeçalho Página 6B, título, anexo, selo e o rótulo do exemplo");
  log(/R\$ 57\.819,79/.test(pdfTxt) && /R\$ 844\.655,02/.test(pdfTxt) && /15,0 anos/.test(pdfTxt) && /Redesenhar/.test(pdfTxt) && /R\$ 123,30/.test(pdfTxt) && /21,26/.test(pdfTxt), "PDF traz o que sobra, o investimento, 15,0 anos, Redesenhar, a Planilha 2 e a margem para a página 6");
  log(/Meu Dossi/.test(pdfTxt) && /envia nada/.test(pdfTxt) && /Pergunte ao seu contador/.test(pdfTxt), "PDF traz a pasta Meu Dossiê, «não envia nada» e as perguntas ao contador");
  log(!/129\.000|192\.346/.test(pdfTxt), "PDF sem preço da Zion Glamping Store");
  log(await p.isVisible("#selo-ok"), "selo «Pronto para levar à página 6» depois do PDF");
  crit = await p.$$eval("#criterio li", (x) => x.map((l) => l.classList.contains("ok")));
  log(crit.every(Boolean), "critério de conclusão: 12 de 12");
  await conferirTela("ação");
  await p.locator("#selo").scrollIntoViewIfNeeded();
  await p.screenshot({ path: path.join(OUT, "06-acao-selo-celular.png") });
  await p.locator("#quadro").scrollIntoViewIfNeeded();
  await p.screenshot({ path: path.join(OUT, "07-quadros-celular.png") });

  // ---------- persistência ao recarregar ----------
  await p.reload(); await p.waitForFunction(() => !!window.ZVIAB);
  log(await p.isVisible("#continuar"), "ao recarregar: «Continuar de onde parei»");
  log((await p.inputValue("#f-projeto")) === "Cabanas da Marina", "ao recarregar: respostas mantidas no aparelho");
  await p.click("#continuar");
  log(await p.isVisible("#selo-ok") && (await p.inputValue("#f-prazo")) === Z.somaDias(HOJE, 30), "continuar volta à tela da ação, com selo e prazo");
  st = await estado();
  const d = st.resumo && st.resumo.dados;
  log(d && d.sobra[0] === 57819.79 && d.investimento_6b === 844655.02 && d.veredito_sugerido === "Redesenhar" && d.margem_para_p6 === 21.26 && st.respostas.pdfBaixado === true && st.resumo.selo === true, "salvo em zion-t1-pilar6b com respostas e resumo.dados (sobra, investimento, veredito, margem para a página 6)");

  // ---------- refazer e o caminho à mão, sem a 6A ----------
  await p.click("#refazer");
  log((await texto("h1")) === "A sua conta" && (await p.inputValue("#f-projeto")) === "", "Refazer apaga e volta à abertura vazia");
  st = await estado();
  log(!st || !st.respostas.projeto, "Refazer limpa o aparelho");
  await p.fill("#f-projeto", "Meu projeto");
  log(await travado(), "abertura segue bloqueada sem situação e diagnóstico");
  await p.locator("label.op", { hasText: "Tenho um terreno e ainda não hospedo ninguém" }).click();
  for (const [q, r] of [["lista dos custos fixos", "Em parte"], ["contador já respondeu", "Não"], ["seu trabalho está na conta", "Sim"], ["curva do ano", "Sim"]]) await p.locator("fieldset", { hasText: q }).locator("label.op", { hasText: r }).first().click();
  log(!(await travado()), "abertura preenchida à mão libera o Começar");
  await avancar();
  log(/Não encontramos a 6A neste aparelho/.test(await texto("#p6a-status")) && (await p.inputValue("#f-capex")) === "", "tela 1 sem a 6A: alerta B2 e CAPEX vazio para digitar");
  log(await travado(), "tela 1 vazia bloqueia o Avançar");
  await p.fill("#f-capex", "500.000"); await p.fill("#f-giro6A", "30.000"); await p.fill("#f-unidades", "2");
  log(!(await travado()), "CAPEX, giro e unidades digitados à mão liberam");
  await conferirTela("6A ausente");
  await p.screenshot({ path: path.join(OUT, "08-sem-6a-celular.png") });
  await avancar();
  log((await p.inputValue("#f-diaria")) === "" && (await p.inputValue("#f-ocupAlta")) === "" && await travado(), "tela 2 nova: nada pré-preenchido e bloqueada");
  st = await estado();
  const L = Z.alertas(st.respostas, Z.calcular(st.respostas, HOJE)).map((a) => a.id);
  log(L.includes("B2") && L.includes("B1"), "sem a 6A: a lógica sobre o estado salvo dá B2 (e B1, imposto ainda em branco)");
  log(st.respostas.reservaRep === "" && st.respostas.imposto === "" && st.respostas.valorHora === "", "nenhum valor de referência inserido (reserva, imposto, valor-hora)");
  await ctx.close();

  /* ======================= Caso 2 · com a 6A, a página 6 e a página 2 no aparelho ======================= */
  console.log("Caso 2 · com a 6A, a página 6, a página 2 e o Marco Zero no aparelho");
  ({ ctx, p } = await novoContexto());
  await p.goto(URL);
  const sem = [JSON.stringify(PAG6A), JSON.stringify(PAG6), JSON.stringify(PAG2), JSON.stringify(MZ)];
  await p.evaluate(([a, b6, b2, mz]) => { localStorage.clear(); localStorage.setItem("zion-t1-pilar6a", a); localStorage.setItem("zion-t1-pilar6", b6); localStorage.setItem("zion-t1-aula2", b2); localStorage.setItem("zion-t1-marco-zero", mz); }, sem);
  await p.reload(); await p.waitForFunction(() => !!window.ZVIAB && !!window.jspdf);
  log(await p.locator('input[name=r-situacao][value="terreno"]').isChecked() && /Veio do seu Marco Zero/.test(await p.textContent("body")), "situação pré-marcada a partir do Marco Zero");
  log((await p.inputValue("#f-nome")) === "Marina" && (await p.inputValue("#f-cidadeUF")) === "Cidade do exemplo/SC", "nome e «Terreno em» lidos dos perfis salvos");
  await p.fill("#f-projeto", "Cabanas da Marina");
  for (const [q, r] of [["lista dos custos fixos", "Em parte"], ["contador já respondeu", "Sim"], ["seu trabalho está na conta", "Sim"], ["curva do ano", "Sim"]]) await p.locator("fieldset", { hasText: q }).locator("label.op", { hasText: r }).first().click();
  await conferirTela("abertura lida"); await avancar();
  log(/Encontramos a sua página 6A neste aparelho/.test(await texto("#p6a-status")), "tela 1: «Encontramos a sua página 6A neste aparelho»");
  log((await p.inputValue("#f-capex")) === "791.131" && (await p.inputValue("#f-giro6A")) === "40.787,38" && (await p.inputValue("#f-terreno")) === "600.000" && (await p.inputValue("#f-unidades")) === "3", "tela 1 lê da 6A: CAPEX 791.131, giro 40.787,38, terreno 600.000, 3 unidades");
  log((await p.inputValue("#f-margem6")) === "40" && /referência da Zion/.test(await texto("#margem6-origem")) && (await p.inputValue("#f-limite6")) === "870.130,80", "tela 1 lê da página 6: margem 40% (referência da Zion) e o limite 870.130,80");
  log((await p.locator('[data-veio="capex"]').count()) === 1 && (await p.locator('[data-veio="margem6"]').count()) === 1, "«Veio da página 6A» e «Veio da página 6» ao lado dos números");
  await conferirTela("6A lida");
  await p.screenshot({ path: path.join(OUT, "09-6a-lida-celular.png") });
  await avancar();
  log((await p.inputValue("#f-diaria")) === "645" && (await p.inputValue("#f-ocupAlta")) === "64" && (await p.inputValue("#f-ocupFraco")) === "22" && (await p.inputValue("#f-ocupBase")) === "50", "tela 2 lê a diária da página 6 e a curva da página 2 (64 / 22), base 50%");
  log(/Na página 2: 3 de alta e 5 fracos/.test(await texto("#cal-conta")) && /645,45/.test(await texto("#diaria-medida")), "tela 2 mostra as contagens e a diária medida da página 2");
  log(await travado(), "tela 2: o calendário não é preenchido por ninguém (a pessoa marca os meses)");
  await conferirTela("quanto entra lida");
  const depois = await p.evaluate(() => ["zion-t1-pilar6a", "zion-t1-pilar6", "zion-t1-aula2", "zion-t1-marco-zero"].map((k) => localStorage.getItem(k)));
  log(depois.join("§") === sem.join("§"), "a ficha não altera a 6A, a página 6, a página 2 nem o Marco Zero salvos");
  st = await estado();
  log(st.respostas.origemCapex === "6A" && st.respostas.p2OcupAno === "38,5" && st.respostas.imposto === "", "estado salvo: origem 6A, ocupação medida 38,5 e o imposto em branco para o aluno");
  await ctx.close();

  // ---------- fechamento ----------
  log(telasSemRolagem.length >= 20 && telasSemRolagem.every(Boolean), `sem rolagem horizontal em ${telasSemRolagem.length} telas`);
  log(erros.length === 0, "sem erro de JavaScript" + (erros.length ? ": " + erros.join(" | ") : ""));
  log(externos.length === 0, "nenhum envio para fora (só o jsPDF e as fontes, servidos localmente)" + (externos.length ? ": " + externos.join(" ") : ""));
  await b.close(); srv.kill();
  console.log(`\n${ok} verificações aprovadas, ${fal} falharam (ponta a ponta no celular, iPhone 13).`);
  process.exit(fal ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });

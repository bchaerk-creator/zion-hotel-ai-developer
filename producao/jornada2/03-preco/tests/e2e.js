// Teste de ponta a ponta da ficha "A minha Tabela de Preço e Canais" no celular.
// Uso: node tests/e2e.js <pasta-saida> <caminho-jspdf.umd.min.js>  (servidor local de docs/ na porta 8813)
const { chromium, devices } = require("playwright");
const fs = require("fs");
const Z = require("../src/logic.js");
const ZF = require("../../../../docs/trilha2/financas/logic.js");
const OUT = process.argv[2], JSPDF = fs.readFileSync(process.argv[3], "utf8");
const URL = "http://localhost:8813/trilha2/preco/";
let ok = 0, fal = 0; const log = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
fs.mkdirSync(OUT, { recursive: true });
const EX = Z.EXEMPLO, esp = Z.calcular(EX), LE = Z.leituras(esp), PE = Z.prioridades(esp);
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
  const f = async (id, v) => { await p.fill("#" + id, v); };
  const live = () => p.textContent("#live");
  let scrollOk = true; const confereScroll = async () => { if (!(await semScrollX())) scrollOk = false; };

  // nome e Folha vindos do Módulo 2 (exemplo do Módulo 2 salvo no aparelho)
  await p.goto(URL);
  await p.evaluate((fx) => localStorage.setItem("zion-t2-financas", JSON.stringify({ ...fx, nome: "Ana Exemplo", hospedagem: "Cabanas do Vale (exemplo)" })), ZF.EXEMPLO);
  await p.reload(); await p.waitForFunction(() => !!window.jspdf && !!window.ZP && !!window.ZF);
  log(await p.title() === "Tabela de Preço e Canais" && (await p.locator("h1").textContent()) === "A minha Tabela de Preço e Canais", "abertura carrega com o título certo");
  log((await p.inputValue("#nome")) === "Ana Exemplo" && (await p.inputValue("#hospedagem")) === "Cabanas do Vale (exemplo)", "nome e hospedagem lidos da Folha do Módulo 2");
  log(/Não é promessa de renda, retorno, ocupação ou resultado/.test(await p.textContent("footer")), "rodapé educacional");
  log(await vaiOff(), "Começar bloqueado sem situação e diagnóstico");
  await confereScroll(); await shot("p01-abertura");
  await p.locator("label.op", { hasText: "Já opero" }).click();
  for (const [q, v] of [["varia", "nao"], ["piso", "nao"], ["liquido", "nao"], ["direta", "sim"]]) await p.locator(`input[name="d-${q}"][value="${v}"]`).locator("xpath=..").click();
  log(/Nível 1 de 4/.test(await p.textContent("#nivel")), "nível 1 de 4 (um sim)");
  log(!(await vaiOff()), "Começar liberado após responder"); await p.click("#vai");

  // Tela 1 · Custo
  log(/Tela 1 de 6/.test(await p.textContent(".progresso")) && /custa cada noite/.test(await p.textContent("h2")), "tela 1: o custo da noite");
  log(await vaiOff(), "tela 1 bloqueada sem os custos");
  await p.click("#importa");
  const rf = ZF.calcular(ZF.EXEMPLO);
  log((await p.inputValue("#custoNoiteVendida")) === String(Math.round(rf.custoPorNoiteVendida * 100) / 100).replace(".", ",") && (await p.inputValue("#custoVariavelNoite")) === "28,32" && (await p.inputValue("#noitesPorEstadia")) === "2,32" && /Trazido da sua Folha/.test(await p.textContent(".card")), "botão traz os números da Folha do Módulo 2 (custo " + (await p.inputValue("#custoNoiteVendida")) + ")");
  await f("custoNoiteVendida", "20"); log(await vaiOff() && /não pode ser menor/.test(await p.textContent("#erro")), "custo por noite menor que o variável bloqueia");
  await f("custoNoiteVendida", "153,04"); await f("diariaAtual", "280"); await f("receitaMes", "16.240,00");
  log(!(await vaiOff()) && /124,72/.test(await live()), "exemplo do plano (153,04): custo fixo por noite 124,72");
  await confereScroll(); await shot("p02-custo"); await p.click("#vai");

  // Tela 2 · Canais
  log(/Os seus canais/.test(await p.textContent(".eyebrow")), "tela 2: os seus canais");
  const canais = [["Plataforma A", "50", "16", "1,5", "0"], ["Plataforma B", "20", "15", "1,5", "0"], ["Venda direta (site e WhatsApp)", "30", "0", "1,5", "0"]];
  for (let i = 0; i < 3; i++) { const [n, m, c, pg, x] = canais[i]; await f(`c-${i}-nome`, n); await f(`c-${i}-mix`, m); await f(`c-${i}-comissao`, c); await f(`c-${i}-pagamento`, pg); await f(`c-${i}-extra`, x); }
  log((await p.isChecked("#c-2-direta")) && !(await p.isChecked("#c-0-direta")), "terceira linha já vem marcada como venda direta");
  await f("impostoPct", "6");
  log(!(await vaiOff()) && /100,0%/.test(await live()) && /11,0%/.test(await live()) && /30,0%/.test(await live()), "mix 100%, comissão média 11,0%, venda direta 30%");
  await f("c-1-mix", "10"); log(await vaiOff() && /soma 90,0%/.test(await p.textContent("#erro")), "mix de 90% bloqueia");
  await f("c-1-mix", "20");
  await p.click("#addCanal"); log((await p.locator(".canal").count()) === 4, "adicionar canal cria uma quarta linha");
  await p.locator("[data-rm='3']").click(); log((await p.locator(".canal").count()) === 3 && (await p.inputValue("#c-0-nome")) === "Plataforma A", "remover canal mantém os outros");
  await p.check("#gestorCanais");
  await confereScroll(); await shot("p03-canais"); await p.click("#vai");

  // Tela 3 · Referência
  log(/diária de referência/.test(await p.textContent("h2")), "tela 3: diária de referência");
  const conc = ["270", "280", "290", "300", "310", "320", "360"]; for (let i = 0; i < conc.length; i++) await f(`conc-${i}`, conc[i]);
  log(/média de <b>R\$ 300,00<\/b> em 5/.test(await p.innerHTML("#live")), "descarta 270 e 360: média 300 em 5 concorrentes");
  await p.locator("label.op", { hasText: "Terço de cima" }).click(); log(/R\$ 360,00/.test(await live()), "terço de cima: 360");
  await p.locator("label.op", { hasText: "Meio" }).click(); await p.click("#usaSug");
  log((await p.inputValue("#referencia")) === "300" && !(await vaiOff()), "usar a sugerida preenche a referência 300");
  await confereScroll(); await shot("p04-referencia"); await p.click("#vai");

  // Tela 4 · Piso
  await f("margemMinima", "10");
  log(/R\$ 200,05/.test(await live()) && /R\$ 220,06/.test(await live()), "custo no canal mais caro 200,05; piso calculado 220,06");
  await f("pisoDeclarado", "350"); log(await vaiOff() && /maior que a diária de referência/.test(await p.textContent("#erro")), "piso acima da referência bloqueia");
  await f("pisoDeclarado", "180"); log(!(await vaiOff()) && /abaixo do custo/.test(await p.textContent("#avisos")), "piso abaixo do custo: aviso");
  await f("pisoDeclarado", "225"); await f("quemConhece", "Eu e quem responde o WhatsApp");
  await f("cond-0", "Terceira noite com café da manhã incluso"); await f("cond-1", "Saída tardia até as 14 h"); await f("cond-2", "Cesta de boas-vindas com produtos da região");
  log(/75,0% da referência/.test(await live()) && (await p.textContent("#avisos")).trim() === "", "piso 225 = 75% da referência, sem aviso");
  await confereScroll(); await shot("p05-piso"); await p.click("#vai");

  // Tela 5 · Calendário
  log(/Como o preço muda/.test(await p.textContent("h2")) && (await p.inputValue("#f-vale")) === "0,75", "tela 5: fatores com o ponto de partida da fonte");
  await f("ano", "2027");
  log(await vaiOff() && /faltam 12/.test(await p.textContent("#erro")), "sem as faixas dos meses: bloqueado");
  for (let i = 0; i < 12; i++) { await p.selectOption(`#m-${i}-sem`, EX.meses[i].sem); await p.selectOption(`#m-${i}-fds`, EX.meses[i].fds); }
  log(!(await vaiOff()) && /Vale <b>R\$ 225,00<\/b>/.test(await p.innerHTML("#live")) && /Pico <b>R\$ 660,00<\/b>/.test(await p.innerHTML("#live")), "diárias das faixas: vale 225 ... pico 660");
  await f("f-vale", "0,6"); log(/fora do ponto de partida/.test(await p.textContent("#avisos")) && /Abaixo do piso/.test(await live()), "fator 0,60: aviso da fonte e vale abaixo do piso");
  await f("f-vale", "0,75");
  await confereScroll(); await shot("p06-calendario"); await p.click("#vai");

  // Tela 6 · Picos e meta
  log(/datas de pico/.test(await p.textContent("h2")) && /30,0%/.test(await p.textContent(".card")), "tela 6: picos e venda direta atual 30%");
  await p.click("#addPico"); await p.click("#addPico");
  const picos = EX.picos;
  for (let i = 0; i < 4; i++) { await f(`p-${i}-nome`, picos[i].nome); await p.selectOption(`#p-${i}-mes`, String(picos[i].mes)); await f(`p-${i}-noites`, String(picos[i].noites)); await f(`p-${i}-fator`, String(picos[i].fator).replace(".", ",")); await f(`p-${i}-minimo`, String(picos[i].minimo)); }
  await f("metaDireta", "40"); await p.fill("#prazoMeta", "2027-06-30");
  log(/<b>16<\/b>/.test(await p.innerHTML("#live")) && /305,92/.test(await live()), "16 noites de pico e diária média do calendário 305,92");
  await f("p-3-noites", "40"); log(await vaiOff() && /passam dos dias/.test(await p.textContent("#erro")), "40 noites no réveillon bloqueiam");
  await f("p-3-noites", "5");
  log((await p.textContent("#vai")).trim() === "Ver a minha Tabela", "botão final: Ver a minha Tabela");
  await confereScroll(); await shot("p07-picos"); await p.click("#vai");

  // Resultado
  const card = await p.textContent(".card");
  log((await p.textContent("#piso")).trim() === "R$ 225,00" && /R\$ 305,92/.test(card), "resultado: piso 225 e diária média 305,92");
  const fx = await p.locator("#faixas tr").allTextContents();
  log(fx.length === 7 && /Vale.*R\$ 225,00.*84/.test(fx[1]) && /Alta.*R\$ 450,00.*44/.test(fx[4]) && /Pico.*16/.test(fx[5]) && /365/.test(fx[6]), "tabela das faixas com diárias e noites (84 ... 16, total 365)");
  const cal = await p.locator("#calendario tr").allTextContents();
  log(cal.length === 13 && esp.meses.every((m, i) => cal[i + 1].includes(Z.brl(m.media))), "calendário de 12 meses bate com logic.js, mês a mês");
  log((await p.locator("#picos tr").count()) === 5 && /R\$ 720,00/.test(await p.textContent("#picos")), "datas de pico listadas (réveillon 720)");
  log(/R\$ 229,50/.test(await p.textContent("#canais")) && /R\$ 249,18/.test(await p.textContent("#canais")), "líquido por canal: 229,50 ... 249,18");
  log(/Eu e quem responde o WhatsApp/.test(await p.textContent("#pisobox")) && /Saída tardia/.test(await p.textContent("#pisobox")), "folha do piso com quem conhece e condições");
  const leit = await p.textContent("#leituras");
  log([LE.custo, LE.piso, LE.calendario, LE.fds, LE.canais, LE.direta].every((l) => leit.includes(l.t)), "as seis leituras batem com logic.js");
  log((await p.textContent("#desconto")).includes(LE.desconto.t), "regra do desconto em três faixas");
  log(/Causa principal: Venda direta sem motor de reservas/.test(await p.textContent("#causa")), "causa principal: venda direta sem motor de reservas");
  log((await p.inputValue("#acao")) === Z.planoSugerido(PE), "plano de ação sugerido preenchido");
  log(!/\b(ADR|RevPAR|OTA|PMS|KPI|DRE)\b/.test(card), "sem sigla na tela de resultado");
  log(/Módulo 4 · Marketing e vendas/.test(card) && (await p.locator('a[href="https://infoprodutos-zion.clickmax.space/zar-a02"]').count()) === 1 && (await p.locator('a[href="https://infoprodutos-zion.clickmax.space/diaria-minima"]').count()) === 1 && (await p.locator('a[href*="adbc67069af26ae0"]').count()) === 0, "próxima etapa e complementos (Precificador e Ferramenta 01) apontando para a página de vendas");
  log(/Falta:.*PDF/.test(await p.textContent("#selo")), "selo pendente antes do prazo e do PDF");
  await p.fill("#prazo", "2027-01-31"); log(/Falta: o PDF baixado/.test(await p.textContent("#selo")), "com prazo, falta só o PDF");
  await p.fill("#acao", "curta"); log(/10 letras/.test(await p.textContent("#selo")), "ação curta volta a pendente");
  await p.fill("#acao", "Instalar o motor de reservas no site ligado ao calendário.");
  await confereScroll(); await shot("p08-resultado");
  const [dl] = await Promise.all([p.waitForEvent("download"), p.click("#pdf")]);
  log(dl.suggestedFilename() === "tabela-de-preco-e-canais.pdf", "PDF baixado: " + dl.suggestedFilename());
  const pdfPath = `${OUT}/tabela-preco.pdf`; await dl.saveAs(pdfPath); log(fs.statSync(pdfPath).size > 5000, `PDF com ${fs.statSync(pdfPath).size} bytes`);
  log(/Pronto para avançar/.test(await p.textContent("#selo")), "selo: pronto para avançar após o PDF");
  // persistência
  await p.reload(); await p.waitForFunction(() => !!window.ZP);
  log((await p.textContent("#piso")).trim() === "R$ 225,00" && (await p.inputValue("#prazo")) === "2027-01-31" && /Pronto/.test(await p.textContent("#selo")), "recarregar mantém resultado, prazo e selo");
  const salvo = await p.evaluate(() => JSON.parse(localStorage.getItem("zion-t2-preco")));
  log(salvo && salvo.pisoDeclarado === "225" && salvo.canais.length === 3 && salvo.pdf && salvo.situacao === "dono", "chave zion-t2-preco guarda os dados como digitados");
  await p.click("#refaz"); log(/Tela 1 de 6/.test(await p.textContent(".progresso")) && (await p.inputValue("#custoNoiteVendida")) === "153,04", "refazer volta à tela 1 com as respostas");
  await p.evaluate(() => { const s = JSON.parse(localStorage.getItem("zion-t2-preco")); s.tela = 0; localStorage.setItem("zion-t2-preco", JSON.stringify(s)); });
  await p.reload(); await p.waitForFunction(() => !!window.ZP);
  log(await p.locator("#retoma").isVisible(), "abertura oferece continuar de onde parei");
  await p.click("#retoma"); log(/A minha Tabela de Preço e Canais/.test(await p.textContent(".eyebrow")), "continuar leva ao resultado quando tudo está preenchido");
  // exemplo didático pelo botão
  await p.evaluate(() => localStorage.clear()); await p.reload(); await p.waitForFunction(() => !!window.ZP);
  await p.click("#exemplo"); log(/Tela 1 de 6/.test(await p.textContent(".progresso")) && (await p.inputValue("#custoNoiteVendida")) === "153,04", "botão do exemplo leva à tela 1 preenchida");
  for (let i = 0; i < 6; i++) { await p.click("#vai"); await confereScroll(); }
  log((await p.textContent("#piso")).trim() === "R$ 225,00" && /Cabanas do Vale \(exemplo\)/.test(await p.textContent(".eyebrow")) && /R\$ 305,92/.test(await p.textContent(".card")), "exemplo percorre as seis telas e dá o mesmo resultado");
  // preço fixo: todas as faixas base, sem picos
  await p.click("#refaz"); for (let i = 0; i < 4; i++) await p.click("#vai");
  for (let i = 0; i < 12; i++) { await p.selectOption(`#m-${i}-sem`, "base"); await p.selectOption(`#m-${i}-fds`, "base"); }
  await p.click("#vai"); for (let i = 3; i >= 0; i--) await p.locator(`[data-rm='${i}']`).click();
  await p.click("#vai");
  log(/Causa principal: Preço fixo o ano inteiro/.test(await p.textContent("#causa")) && /Datas de pico sem regra/.test(await p.textContent("#prioridades")), "preço fixo sem picos: causa principal e prioridade de picos");
  await shot("p09-preco-fixo");
  // desktop
  const d = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await d.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
  await d.route("**/jspdf.umd.min.js", (r) => r.fulfill({ contentType: "application/javascript", body: JSPDF }));
  await d.goto(URL); await d.waitForFunction(() => !!window.ZP); await d.screenshot({ path: `${OUT}/d01-abertura.png`, fullPage: true });
  log(scrollOk, "sem rolagem horizontal no celular em nenhuma tela");
  log(erros.length === 0, "sem erros de JavaScript" + (erros.length ? ": " + erros.join(" | ") : ""));
  await b.close();
  console.log(`\n${ok} ok, ${fal} falhou`); process.exit(fal ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });

// Teste de ponta a ponta da ficha "A minha Folha Única do Mês" no celular.
// Uso: node tests/e2e.js <pasta-saida> <caminho-jspdf.umd.min.js>  (servidor local de docs/ na porta 8790)
const { chromium, devices } = require("playwright");
const fs = require("fs");
const Z = require("../src/logic.js");
const OUT = process.argv[2], JSPDF = fs.readFileSync(process.argv[3], "utf8");
const URL = "http://localhost:8790/trilha2/financas/";
let ok = 0, fal = 0; const log = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
fs.mkdirSync(OUT, { recursive: true });
const EX = Z.EXEMPLO, esperado = Z.calcular(EX), LE = Z.leituras(esperado), PE = Z.prioridades(esperado, EX);
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
  const preenche = async (id, v) => { await p.fill("#" + id, v); };
  const brlIn = (n) => String(n.toFixed(2)).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, "."); // "16.240,00"

  // nome vindo do Marco Zero
  await p.goto(URL); await p.evaluate(() => localStorage.setItem("zion-t2-marco-zero", JSON.stringify({ nome: "Ana Exemplo", hospedagem: "Cabanas do Vale (exemplo)" })));
  await p.reload(); await p.waitForFunction(() => !!window.jspdf && !!window.ZF);
  log(await p.title() === "Folha Única do Mês" && (await p.locator("h1").textContent()) === "A minha Folha Única do Mês", "abertura carrega com o título certo");
  log((await p.inputValue("#nome")) === "Ana Exemplo", "nome lido do Marco Zero");
  log(/Não é promessa de renda, retorno ou resultado/.test(await p.textContent("footer")), "rodapé educacional");
  log(await vaiOff(), "Começar bloqueado sem situação e diagnóstico");
  await shot("f01-abertura");
  await p.locator("label.op", { hasText: "Já opero" }).click();
  for (const [q, v] of [["conta", "sim"], ["custo", "nao"], ["retirada", "sim"], ["reserva", "nao"]]) await p.locator(`input[name="d-${q}"][value="${v}"]`).locator("xpath=..").click();
  log(/Nível 2 de 4/.test(await p.textContent("#nivel")), "nível da Linha de Separação = 2 (dois sim)");
  log(!(await vaiOff()), "Começar liberado após responder");
  await p.click("#vai");

  // Tela 1 · O mês
  log(/Tela 1 de 6/.test(await p.textContent(".progresso")) && /Qual mês/.test(await p.textContent("h2")), "tela 1: o mês, com progresso");
  log(await vaiOff(), "tela 1 bloqueada sem os campos obrigatórios");
  await preenche("mes", "Outubro de 2026"); await preenche("dias", "31"); await preenche("unidades", "4"); await preenche("noites", "200"); await preenche("estadias", "25");
  log(await vaiOff() && /passam das noites disponíveis/.test(await p.textContent("#erro")), "noites > disponíveis bloqueia com mensagem");
  await preenche("noites", "-3"); log(await vaiOff() && /negativo/.test(await p.textContent("#erro")), "noite negativa bloqueia");
  await preenche("noites", "58"); log(!(await vaiOff()) && /124/.test(await p.textContent("#live")), "noites 58: liberado e mostra 124 noites disponíveis");
  await shot("f02-mes"); await p.click("#vai");

  // Tela 2 · O que entrou
  log(/O que entrou/.test(await p.textContent(".eyebrow")), "tela 2: o que entrou");
  await preenche("receitaHospedagem", "16.240,00"); await preenche("taxaLimpezaCobrada", "1500"); await preenche("outrasReceitas", "980"); await preenche("custoOutrasReceitas", "420");
  await p.click("#refZion");
  log((await p.inputValue("#comissoesPct")) === "15" && /Aplicada/.test(await p.textContent(".ref")) && /2\.760,80/.test(await p.textContent("#live")), "botão referência Zion: 15% e 2% aplicados (deduções 2.760,80 = 17% de 16.240, sem descontos)");
  await preenche("descontos", "20000"); log(await vaiOff() && /passam da receita/.test(await p.textContent("#erro")), "deduções > receita bloqueiam");
  await preenche("descontos", "650"); await preenche("comissoesPct", "11"); await preenche("processamentoPct", "1,5"); await preenche("impostoPct", "6"); await preenche("cancelamentos", "0");
  log(!(await vaiOff()) && /3\.654,40/.test(await p.textContent("#live")) && /12\.585,60/.test(await p.textContent("#live")), "valores do exemplo com vírgula: deduções 3.654,40 e receita real 12.585,60");
  await shot("f03-entrou"); await p.click("#vai");

  // Tela 3 · Variáveis
  await preenche("limpezaPaga", "2000"); await preenche("enxoval", "380"); await preenche("amenidades", "260"); await preenche("energiaVariavel", "340"); await preenche("cafe", "0");
  await p.check("#quebraRef"); await p.waitForFunction(() => document.getElementById("quebraRef").checked);
  log(/162,40/.test(await p.textContent("#live")) && /2\.062,40/.test(await p.textContent("#live")), "quebra por referência 162,40 e variáveis 2.062,40");
  await shot("f04-variaveis"); await p.click("#vai");

  // Tela 4 · Fixos
  await preenche("equipe", "1800"); await preenche("comuns", "620"); await preenche("software", "190"); await preenche("contador", "300"); await preenche("marketingFixo", "150"); await preenche("duodecimos", "460"); await preenche("manutencaoContratada", "250");
  await preenche("retiradaHoras", "20"); await preenche("retiradaValorHora", "40");
  log(/3\.464,00/.test(await p.textContent("#live")) && /7\.234,00/.test(await p.textContent("#live")), "Conta da Retirada 20 × 40 × 4,33 = 3.464 e fixos 7.234");
  await p.check("#retDec"); log(/R\$ 0,00/.test(await p.textContent("#live")) && /decidida como zero/.test(await p.textContent("#live")), "decidi retirada zero: retirada vai a 0");
  await p.uncheck("#retDec"); log(/3\.464,00/.test(await p.textContent("#live")), "desmarcar volta à conta");
  await shot("f05-fixos"); await p.click("#vai");

  // Tela 5 · Modelo
  log(/referência Zion de 3 a 6%/.test(await p.textContent(".ref")) && (await p.inputValue("#reservaPct")) === "4", "tela 5: reserva padrão 4% marcada como referência ajustável");
  log(/542,62/.test(await p.textContent("#live")) && /3\.726,58/.test(await p.textContent("#live")), "reserva 542,62 e geração de caixa 3.726,58");
  await shot("f06-modelo"); await p.click("#vai");

  // Tela 6 · Caixa
  log(await vaiOff(), "tela 6 bloqueada sem o caixa");
  await preenche("saldoInicial", "9800"); await preenche("entradasCaixa", "18470"); await preenche("saidasCaixa", "14650"); await preenche("reservasSeparadas", "0");
  log(/13\.620,00/.test(await p.textContent("#live")) && /1,9/.test(await p.textContent("#live")), "saldo final 13.620 e fôlego 1,9");
  log((await p.textContent("#vai")).trim() === "Ver a minha Folha", "botão final: Ver a minha Folha");
  await shot("f07-caixa"); await p.click("#vai");

  // Resultado
  const texto = await p.textContent(".card");
  log(/Quanto sobrou do mês/.test(texto) && (await p.textContent("#sobrou")).trim() === Z.brl(esperado.resultadoOperacional), `resultado na tela = ${Z.brl(esperado.resultadoOperacional)}`);
  const linhas = await p.locator("#cascata tr").allTextContents();
  const casc = Z.cascata(esperado);
  log(linhas.length === casc.length && casc.every((l, i) => linhas[i].includes(Z.brl(l.v))), "cascata na tela bate com logic.js, linha a linha");
  const ind = {}; for (const el of await p.locator("#indicadores div[data-id]").all()) ind[await el.getAttribute("data-id")] = await el.locator("strong").textContent();
  log(ind.custoNoite === Z.brl(esperado.custoPorNoiteVendida) && ind.diariaReal === Z.brl(esperado.diariaMediaReal) && /35,4 noites/.test(ind.pe) && /1,9 meses/.test(ind.folego), `indicadores: custo por noite ${ind.custoNoite}, diária real ${ind.diariaReal}, equilíbrio ${ind.pe}, fôlego ${ind.folego}`);
  log(!/\b(DRE|EBITDA|KPI|ADR|RevPAR)\b/.test(texto), "sem sigla na tela de resultado");
  const leit = await p.textContent("#leituras");
  log(leit.includes(LE.noite.t) && leit.includes(LE.equilibrio.t) && leit.includes(LE.folego.t) && leit.includes(LE.margem.t), "as quatro leituras batem com logic.js");
  log(/Causa principal: Sem reserva para a baixa/.test(await p.textContent("#causa")), "causa principal: sem reserva para a baixa");
  log((await p.textContent("#caixa-x")).includes(LE.caixa.t), "caixa × resultado na tela");
  log((await p.locator("#prioridades > div").count()) === PE.length && /Sem reserva para a baixa/.test(await p.textContent("#prioridades")), "prioridades listadas");
  log((await p.inputValue("#acao")) === Z.planoSugerido(PE), "plano de ação sugerido preenchido");
  log(/Módulo 3 · Preço, reservas e distribuição/.test(texto), "próxima etapa aponta o módulo 3");
  log((await p.locator('a[href="../materiais/planilhas/"]').count()) === 1 && (await p.locator('a[href="../"]').count()) === 1, "links para o Painel do Mês e para as ferramentas");
  log(/Falta:.*PDF/.test(await p.textContent("#selo")), "selo pendente antes do prazo e do PDF");
  await p.fill("#prazo", "2026-12-15"); log(/Falta: o PDF baixado/.test(await p.textContent("#selo")), "com prazo, falta só o PDF");
  await p.fill("#acao", "curta"); log(/10 letras/.test(await p.textContent("#selo")), "ação curta demais volta a pendente");
  await p.fill("#acao", "Abrir a conta de reservas e programar a transferência no dia do repasse.");
  log(await semScrollX(), "sem rolagem horizontal no celular");
  await shot("f08-resultado");
  const [dl] = await Promise.all([p.waitForEvent("download"), p.click("#pdf")]);
  log(dl.suggestedFilename() === "folha-unica-do-mes.pdf", "PDF baixado: " + dl.suggestedFilename());
  const pdfPath = `${OUT}/folha-unica.pdf`; await dl.saveAs(pdfPath); log(fs.statSync(pdfPath).size > 5000, `PDF com ${fs.statSync(pdfPath).size} bytes`);
  log(/Pronto para avançar/.test(await p.textContent("#selo")), "selo: pronto para avançar após o PDF");
  // persistência
  await p.reload(); await p.waitForFunction(() => !!window.ZF);
  log((await p.textContent("#sobrou")).trim() === Z.brl(esperado.resultadoOperacional), "recarregar mantém o resultado (salvo no aparelho)");
  log((await p.inputValue("#acao")).startsWith("Abrir a conta de reservas") && (await p.inputValue("#prazo")) === "2026-12-15" && /Pronto/.test(await p.textContent("#selo")), "ação, prazo e selo persistem");
  const salvo = await p.evaluate(() => JSON.parse(localStorage.getItem("zion-t2-financas")));
  log(salvo && salvo.receitaHospedagem === "16.240,00" && salvo.pdf, "chave zion-t2-financas guarda os dados como digitados");
  // refazer
  await p.click("#refaz"); log(/Tela 1 de 6/.test(await p.textContent(".progresso")) && (await p.inputValue("#noites")) === "58", "refazer volta à tela 1 com as respostas mantidas");
  // continuar de onde parei
  await p.evaluate(() => { const s = JSON.parse(localStorage.getItem("zion-t2-financas")); s.tela = 0; localStorage.setItem("zion-t2-financas", JSON.stringify(s)); });
  await p.reload(); await p.waitForFunction(() => !!window.ZF);
  log(await p.locator("#retoma").isVisible(), "abertura oferece continuar de onde parei");
  await p.click("#retoma"); log(/A minha Folha Única do Mês/.test(await p.textContent(".eyebrow")), "continuar leva ao resultado quando tudo está preenchido");
  // exemplo didático preenchido pelo botão
  await ctx.clearCookies(); await p.evaluate(() => localStorage.clear()); await p.reload(); await p.waitForFunction(() => !!window.ZF);
  await p.click("#exemplo"); log(/Tela 1 de 6/.test(await p.textContent(".progresso")) && (await p.inputValue("#receitaHospedagem").catch(() => "")) === "" , "botão do exemplo leva à tela 1 com os dados do exemplo");
  for (let i = 0; i < 6; i++) await p.click("#vai");
  log((await p.textContent("#sobrou")).trim() === Z.brl(esperado.resultadoOperacional) && /Cabanas do Vale \(exemplo\)/.test(await p.textContent(".eyebrow")), "exemplo didático percorre as seis telas e dá o mesmo resultado");
  // sem venda: noites 0
  await p.click("#refaz"); await preenche("noites", "0"); await preenche("estadias", "0"); for (let i = 0; i < 6; i++) await p.click("#vai");
  log(/Sem noite vendida, cada real que saiu é prejuízo/.test(await p.textContent("#leituras")), "mês sem noite vendida: leitura explica, sem erro");
  await shot("f09-sem-noite");
  // desktop
  const d = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await d.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
  await d.goto(URL); await d.waitForFunction(() => !!window.ZF); await d.screenshot({ path: `${OUT}/d01-abertura.png`, fullPage: true });
  log(erros.length === 0, "sem erros de JavaScript" + (erros.length ? ": " + erros.join(" | ") : ""));
  await b.close();
  console.log(`\n${ok} ok, ${fal} falhou`); process.exit(fal ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });

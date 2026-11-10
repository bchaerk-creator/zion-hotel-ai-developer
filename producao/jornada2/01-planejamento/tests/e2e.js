// Teste de ponta a ponta da ficha "O meu Painel de Gestão" no celular (iPhone 13).
// Uso: node tests/e2e.js <pasta-saida> <caminho-jspdf.umd.min.js>  (servidor local de docs/ na porta 8811)
const { chromium, devices } = require("playwright");
const fs = require("fs");
const Z = require("../src/logic.js");
const ZF = require("../../02-financas/src/logic.js");
const OUT = process.argv[2], JSPDF = fs.readFileSync(process.argv[3], "utf8");
const PORTA = process.env.PORTA || 8811;
const URL = `http://localhost:${PORTA}/trilha2/planejamento/`;
let ok = 0, fal = 0; const log = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
fs.mkdirSync(OUT, { recursive: true });
const EX = Z.EXEMPLO;
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ ...devices["iPhone 13"], acceptDownloads: true });
  await ctx.route("**/jspdf.umd.min.js", (r) => r.fulfill({ contentType: "application/javascript", body: JSPDF }));
  await ctx.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
  const p = await ctx.newPage(); const erros = [];
  p.on("pageerror", (e) => erros.push(e.message)); p.on("console", (m) => m.type() === "error" && erros.push(m.text()));
  const shot = (n) => p.screenshot({ path: `${OUT}/${n}.png`, fullPage: true });
  const semScrollX = async () => p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
  const vaiOff = () => p.locator("#vai").isDisabled();
  const live = () => p.textContent("#live");
  const telaOk = async (n, re) => /Tela \d de 5/.test(await p.textContent(".progresso")) && (await p.textContent(".progresso")).includes(`Tela ${n} de 5`) && re.test(await p.textContent("h2.pergunta"));

  // nome vindo do Marco Zero
  await p.goto(URL); await p.evaluate(() => { localStorage.clear(); localStorage.setItem("zion-t2-marco-zero", JSON.stringify({ nome: "Ana Exemplo", email: "ana@exemplo.com", hospedagem: "Cabanas do Vale (exemplo)" })); });
  await p.reload(); await p.waitForFunction(() => !!window.jspdf && !!window.ZP);
  log(await p.title() === "Painel de Gestão" && (await p.locator("h1").textContent()) === "O meu Painel de Gestão", "abertura carrega com o título certo");
  log((await p.inputValue("#nome")) === "Ana Exemplo" && (await p.inputValue("#hospedagem")) === "Cabanas do Vale (exemplo)", "nome e hospedagem lidos do Marco Zero");
  log(/Não é promessa de renda, retorno, ocupação ou resultado/.test(await p.textContent("footer")), "rodapé educacional");
  log(await vaiOff(), "Começar bloqueado sem situação, quem e diagnóstico");
  await shot("p01-abertura");
  await p.locator("label.op", { hasText: "Já opero" }).click();
  await p.locator("label.op", { hasText: "Eu, sozinho" }).click();
  for (const q of ["painel", "metas", "donos"]) await p.locator(`input[name="d-${q}"][value="nao"]`).locator("xpath=..").click();
  log(await vaiOff(), "Começar bloqueado com uma pergunta faltando");
  await p.locator(`input[name="d-reuniao"][value="nao"]`).locator("xpath=..").click();
  log(/Nível 1 de 4/.test(await p.textContent("#nivel")) && /Sem painel/.test(await p.textContent("#nivel")), "nível do painel = 1, Sem painel");
  log(!(await vaiOff()), "Começar liberado");
  await p.click("#vai");

  // Tela 1 · ponto de partida
  log(await telaOk(1, /De onde você parte/), "tela 1: ponto de partida, com progresso");
  log((await p.locator("#daFolha").count()) === 0, "sem Folha Única, não oferece importar");
  log(await vaiOff(), "tela 1 bloqueada sem mês, dias e unidades");
  await p.fill("#mesBase", "Outubro de 2026"); await p.fill("#dias", "31"); await p.fill("#unidades", "0");
  log(await vaiOff() && /1 a 999/.test(await p.textContent("#erro")), "unidades zero bloqueia com mensagem");
  await p.fill("#unidades", "4");
  log(!(await vaiOff()) && /124/.test(await live()) && /0 de 5/.test(await live()), "liberado só com o mês: 124 noites, 0 de 5 números (não sei é aceito)");
  log(/não sei/.test(await p.textContent("#avisos")), "aviso de não sei aparece");
  await p.fill("#base_ocupacao", "120"); log(await vaiOff() && /0 a 100/.test(await p.textContent("#erro")), "ocupação acima de 100% bloqueia");
  await p.fill("#base_ocupacao", "46,8"); await p.fill("#base_diaria", "280,00"); await p.fill("#base_resultado", "11.890,00"); await p.check("#semRet");
  await p.fill("#base_nota", "4,7"); await p.fill("#base_vendaDireta", "12");
  log(!(await vaiOff()) && /5 de 5/.test(await live()), "cinco números do exemplo: 5 de 5");
  await shot("p02-partida"); await p.click("#vai");

  // Tela 2 · metas
  log(await telaOk(2, /12 meses/), "tela 2: metas de 12 meses");
  log(/Ponto de partida: R\$ 280,00/.test(await p.textContent(".card")) && /mesmo mês daqui a 12 meses/.test(await p.textContent(".aviso")), "mostra o ponto de partida e a regra do mesmo mês");
  log(await vaiOff(), "tela 2 bloqueada sem as metas");
  await p.fill("#meta_ocupacao", "50"); await p.fill("#meta_diaria", "300"); await p.fill("#meta_resultado", "13.000"); await p.fill("#meta_nota", "5,5"); await p.fill("#meta_vendaDireta", "20");
  log(await vaiOff() && /0 a 5/.test(await p.textContent("#erro")), "meta de nota acima da escala bloqueia");
  await p.fill("#meta_nota", "4,8");
  log(!(await vaiOff()) && /62 noites/.test(await live()) && /R\$ 18\.600,00/.test(await live()) && /14,5% acima/.test(await live()), "metas pedem 62 noites e R$ 18.600 (14,5% acima)");
  await shot("p03-metas"); await p.click("#vai");

  // Tela 3 · donos
  log(await telaOk(3, /Quem olha cada número/), "tela 3: donos");
  log(/arquivado/.test(await p.textContent(".explica")), "cita: indicador sem dono é arquivado");
  for (const i of Z.IND.slice(0, 4)) await p.fill("#dono_" + i.id, "Ana");
  log(await vaiOff() && /Falta o dono de taxa de venda direta/.test(await p.textContent("#erro")) && /4 de 5/.test(await live()), "falta um dono: bloqueia");
  await p.fill("#dono_vendaDireta", "Ana"); log(!(await vaiOff()), "cinco donos: liberado");
  await shot("p04-donos"); await p.click("#vai");

  // Tela 4 · reunião
  log(await telaOk(4, /reunião semanal/), "tela 4: reunião semanal");
  log(await vaiOff(), "tela 4 bloqueada sem dia e hora");
  await p.selectOption("#reuniaoDia", "Segunda-feira"); await p.fill("#reuniaoHora", "08:00");
  log((await p.inputValue("#reuniaoDuracao")) === "30" && !(await vaiOff()), "duração padrão 30 minutos; liberado com dia e hora");
  await p.fill("#reuniaoDuracao", "45"); log(!(await vaiOff()) && /trinta minutos/.test(await p.textContent("#avisos")), "45 minutos: aviso da fonte");
  await p.fill("#reuniaoDuracao", "30"); await p.fill("#reuniaoQuem", "Ana, sozinha, com a planilha");
  log(/segunda-feira/.test(await live()) && /08:00/.test(await live()), "resumo da reunião ao vivo");
  await shot("p05-reuniao"); await p.click("#vai");

  // Tela 5 · seis semanas
  log(await telaOk(5, /seis semanas/), "tela 5: plano de seis semanas");
  await p.selectOption("#s12", "2"); await p.selectOption("#s34", "2"); await p.selectOption("#s56", "4");
  log(await vaiOff() && /três pilares diferentes/.test(await p.textContent("#erro")), "pilar repetido bloqueia");
  await p.selectOption("#s34", "3"); await p.fill("#s12Por", EX.s12Por); await p.fill("#s34Por", EX.s34Por); await p.fill("#s56Por", EX.s56Por);
  log(!(await vaiOff()) && /evita culpa/.test(await p.textContent("#avisos")), "liberado; aviso para o que deixar para depois");
  await p.fill("#depois", EX.depois);
  log((await p.textContent("#vai")).trim() === "Ver o meu Painel", "botão final: Ver o meu Painel");
  await shot("p06-seis"); await p.click("#vai");

  // Resultado
  const esperado = Z.calcular(Object.assign({}, EX)); const P = Z.painel(esperado);
  log(/Cinco números, cinco donos/.test(await p.textContent(".leitura")) && (await p.textContent("#resumoNota")).startsWith("5"), "resultado: cinco números, cinco donos (5 de 5)");
  const linhas = await p.locator("#painel tr[data-id]").all();
  let bate = linhas.length === 5;
  for (let k = 0; k < linhas.length; k++) { const tx = await linhas[k].textContent(); bate = bate && tx.includes(P[k].base) && tx.includes(P[k].meta) && tx.includes(P[k].variacao) && tx.includes("Ana"); }
  log(bate, "tabela do painel bate com logic.js, linha a linha");
  const lt = await p.textContent("#leituras");
  log(Z.leituras(esperado, EX).every((x) => lt.includes(x)), "as três leituras batem com logic.js");
  log((await p.locator("#atencao [data-id]").count()) === 1 && (await p.getAttribute("#atencao [data-id]", "data-id")) === "semRetirada", "atenção: resultado sem a retirada");
  log(/série histórica/.test(await p.textContent("#erroComum")), "erro comum da fonte");
  log((await p.locator("#seis > div").count()) === 3 && /Módulo 3 · Preço/.test(await p.textContent("#seis")), "seis semanas listadas");
  log((await p.inputValue("#acao")) === Z.planoSugerido(Object.assign({}, EX, { reuniaoQuem: "Ana, sozinha, com a planilha" })), "plano sugerido preenchido");
  const card = await p.textContent(".card");
  log(/Módulo 2 · Finanças, fluxo de caixa e fechamento/.test(card), "próxima etapa: Módulo 2");
  log(!/\b(KPI|ADR|RevPAR|OTA|DRE)\b/.test(card), "sem sigla na tela de resultado");
  log((await p.locator('a[href="../materiais/planilhas/"]').count()) === 1 && (await p.locator('a[href="../"]').count()) === 1, "links para a planilha e para as ferramentas");
  log(/Falta:.*primeira reunião.*PDF/.test(await p.textContent("#selo")), "selo pendente sem data e PDF");
  await p.fill("#prazo", "2026-11-16"); log(/Falta: o PDF baixado/.test(await p.textContent("#selo")), "com a data, falta só o PDF");
  const acaoOriginal = await p.inputValue("#acao");
  await p.fill("#acao", "curta"); log(/10 letras/.test(await p.textContent("#selo")), "plano curto volta a pendente");
  await p.fill("#acao", acaoOriginal);
  log(await semScrollX(), "sem rolagem horizontal no celular");
  await shot("p07-resultado");
  const [dl] = await Promise.all([p.waitForEvent("download"), p.click("#pdf")]);
  log(dl.suggestedFilename() === "painel-de-gestao.pdf", "PDF baixado: " + dl.suggestedFilename());
  const pdfPath = `${OUT}/painel-de-gestao.pdf`; await dl.saveAs(pdfPath); log(fs.statSync(pdfPath).size > 5000, `PDF com ${fs.statSync(pdfPath).size} bytes`);
  log(/Pronto para avançar/.test(await p.textContent("#selo")), "selo: pronto para avançar após o PDF");

  // persistência
  await p.reload(); await p.waitForFunction(() => !!window.ZP);
  log((await p.locator("#painel tr[data-id]").count()) === 5 && /Pronto/.test(await p.textContent("#selo")) && (await p.inputValue("#prazo")) === "2026-11-16", "recarregar mantém painel, data e selo (salvo no aparelho)");
  const salvo = await p.evaluate(() => JSON.parse(localStorage.getItem("zion-t2-planejamento")));
  log(salvo && salvo.base_resultado === "11.890,00" && salvo.dono_nota === "Ana" && salvo.pdf && salvo.resultadoSemRetirada === true, "chave zion-t2-planejamento guarda os dados como digitados");
  await p.click("#refaz"); log((await p.textContent(".progresso")).includes("Tela 1 de 5") && (await p.inputValue("#base_diaria")) === "280,00", "refazer volta à tela 1 com as respostas mantidas");
  await p.evaluate(() => { const s = JSON.parse(localStorage.getItem("zion-t2-planejamento")); s.tela = 0; s.dono_nota = ""; localStorage.setItem("zion-t2-planejamento", JSON.stringify(s)); });
  await p.reload(); await p.waitForFunction(() => !!window.ZP);
  log(await p.locator("#retoma").isVisible(), "abertura oferece continuar de onde parei");
  await p.click("#retoma"); log((await p.textContent(".progresso")).includes("Tela 3 de 5"), "continuar leva à primeira tela incompleta (donos)");

  // exemplo didático pelo botão
  await p.evaluate(() => localStorage.clear()); await p.reload(); await p.waitForFunction(() => !!window.ZP);
  await p.click("#exemplo"); log((await p.textContent(".progresso")).includes("Tela 1 de 5") && (await p.inputValue("#base_ocupacao")) === "46,8", "botão do exemplo leva à tela 1 com os dados fictícios");
  for (let i = 0; i < 5; i++) await p.click("#vai");
  log((await p.locator("#painel tr[data-id]").count()) === 5 && /Cabanas do Vale \(exemplo\)/.test(await p.textContent(".eyebrow")) && (await p.textContent("#painel")).includes("R$ 13.000,00"), "exemplo percorre as cinco telas e monta o mesmo painel");

  // Folha Única do Módulo 2 presente: importa o ponto de partida
  await p.evaluate((f) => { localStorage.clear(); localStorage.setItem("zion-t2-financas", JSON.stringify(f)); }, Object.assign({}, ZF.EXEMPLO, { nome: "Ana Exemplo" }));
  await p.reload(); await p.waitForFunction(() => !!window.ZP && !!window.ZF);
  log((await p.inputValue("#nome")) === "Ana Exemplo", "nome lido da Folha Única quando não há Marco Zero");
  await p.locator("label.op", { hasText: "Já opero" }).click(); await p.locator("label.op", { hasText: "Tenho gerente" }).click();
  for (const q of ["painel", "metas", "donos", "reuniao"]) await p.locator(`input[name="d-${q}"][value="sim"]`).locator("xpath=..").click();
  log(/Nível 4 de 4/.test(await p.textContent("#nivel")), "quatro sim: nível 4");
  await p.click("#vai");
  log(await p.locator("#daFolha").isVisible(), "com a Folha Única, oferece usar os números");
  await p.click("#daFolha");
  log((await p.inputValue("#base_ocupacao")) === "46,8" && (await p.inputValue("#base_diaria")) === "280" && (await p.inputValue("#base_resultado")) === "4269,2" && !(await p.isChecked("#semRet")), "importa ocupação 46,8, diária 280 e resultado 4.269,20 com a retirada");
  await shot("p08-da-folha");
  await p.click("#vai");
  log((await p.inputValue("#ocupacaoEquilibrio")) === "28,5", "importa a ocupação de equilíbrio 28,5%");
  await p.fill("#meta_ocupacao", "25"); await p.fill("#meta_diaria", "300"); await p.fill("#meta_resultado", "5000"); await p.fill("#meta_nota", "4,8"); await p.fill("#meta_vendaDireta", "20"); await p.fill("#numeroCorte", "6000");
  await p.click("#vai");
  for (const i of Z.IND) await p.fill("#dono_" + i.id, "Bia"); await p.click("#vai");
  await p.selectOption("#reuniaoDia", "Terça-feira"); await p.fill("#reuniaoHora", "09:30"); await p.click("#vai");
  await p.selectOption("#s12", "5"); await p.selectOption("#s34", "6"); await p.selectOption("#s56", "7"); await p.click("#vai");
  const ids = await p.locator("#atencao [data-id]").evaluateAll((els) => els.map((e) => e.getAttribute("data-id")));
  log(ids.join(",") === "equilibrio,corte,semBase,abaixo,donoUnico", "atenção dispara: equilíbrio, corte, sem base, meta abaixo e dono único (" + ids.join(",") + ")");
  log(/sabe 3 de 5/.test(await p.textContent("#leituras")), "leitura: sabe 3 de 5 (nota e venda direta não vêm da Folha)");
  await shot("p09-alertas");

  // desktop
  const d = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await d.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
  await d.route("**/jspdf.umd.min.js", (r) => r.fulfill({ contentType: "application/javascript", body: JSPDF }));
  d.on("pageerror", (e) => erros.push(e.message));
  await d.goto(URL); await d.waitForFunction(() => !!window.ZP); await d.screenshot({ path: `${OUT}/d01-abertura.png`, fullPage: true });
  log(await d.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), "desktop sem rolagem horizontal");
  log(erros.length === 0, "sem erros de JavaScript" + (erros.length ? ": " + erros.join(" | ") : ""));
  await b.close();
  console.log(`\n${ok} ok, ${fal} falhou`); process.exit(fal ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });

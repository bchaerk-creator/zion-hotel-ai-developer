// Teste de ponta a ponta da ficha "A minha Marca e Captação" no celular (iPhone 13).
// Uso: node tests/e2e.js <pasta-saida> <caminho-jspdf.umd.min.js>  (servidor local de docs/ na porta 8814, ou PORTA=...)
const { chromium, devices } = require("playwright");
const fs = require("fs");
const Z = require("../src/logic.js");
const OUT = process.argv[2], JSPDF = fs.readFileSync(process.argv[3], "utf8");
const PORTA = process.env.PORTA || 8814;
const URL = `http://localhost:${PORTA}/trilha2/marketing/`;
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
  const erro = () => p.textContent("#erro");
  const telaOk = async (n, re) => (await p.textContent(".progresso")).includes(`Tela ${n} de 5`) && re.test(await p.textContent("h2.pergunta"));
  const radio = (name, v) => p.locator(`input[name="${name}"][value="${v}"]`).locator("xpath=..").click();

  // nome vindo do Painel (Módulo 1) e meta de venda direta do Painel
  await p.goto(URL); await p.evaluate(() => { localStorage.clear(); localStorage.setItem("zion-t2-planejamento", JSON.stringify({ nome: "Ana Exemplo", email: "ana@exemplo.com", hospedagem: "Cabanas do Vale (exemplo)", base_vendaDireta: "30", meta_vendaDireta: "40" })); });
  await p.reload(); await p.waitForFunction(() => !!window.jspdf && !!window.ZM);
  log(await p.title() === "Marca e Captação" && (await p.locator("h1").textContent()) === "A minha Marca e Captação", "abertura carrega com o título certo");
  log((await p.inputValue("#nome")) === "Ana Exemplo" && (await p.inputValue("#hospedagem")) === "Cabanas do Vale (exemplo)", "nome e hospedagem lidos do Painel (Módulo 1)");
  log(/Não é promessa de renda, retorno, ocupação, reservas ou resultado/.test(await p.textContent("footer")), "rodapé educacional");
  log(await vaiOff(), "Começar bloqueado sem situação e diagnóstico");
  await shot("p01-abertura");
  await p.locator("label.op", { hasText: "Já opero" }).click();
  for (const q of ["promessa", "lista", "canal"]) await radio("d-" + q, "nao");
  log(await vaiOff(), "Começar bloqueado com uma pergunta faltando");
  await radio("d-custo", "nao");
  log(/Nível 1 de 4/.test(await p.textContent("#nivel")) && /Audiência alugada/.test(await p.textContent("#nivel")), "nível 1 de 4: Audiência alugada");
  log(!(await vaiOff()), "Começar liberado"); await p.click("#vai");

  // Tela 1 · para quem e promessa
  log(await telaOk(1, /Por que alguém escolheria/), "tela 1: para quem e a promessa");
  log(await vaiOff(), "tela 1 bloqueada vazia");
  await p.fill("#publico", EX.publico); await p.fill("#naoPublico", EX.naoPublico);
  await p.fill("#promessa", "Cabana aconchegante com vista incrível");
  for (const q of Z.TESTES) await radio("t-" + q.id, "sim");
  await p.selectOption("#cinco", "4");
  log(!(await vaiOff()) && /adjetivo genérico/.test(await p.textContent("#avisos")) && /aconchegante, incrivel/.test(await live()), "adjetivo genérico: aviso e destaque ao vivo, sem bloquear");
  await p.fill("#promessa", EX.promessa);
  log(!(await vaiOff()) && /4 de 4/.test(await live()) && !/adjetivo/.test(await p.textContent("#avisos")), "promessa do exemplo: 4 de 4 testes, sem aviso");
  await shot("p02-marca"); await p.click("#vai");

  // Tela 2 · prova e tom
  log(await telaOk(2, /antes da reserva/), "tela 2: a prova e o tom");
  await p.fill("#prova", EX.prova); await p.fill("#tom", EX.tom); await p.fill("#banidas", EX.banidas); await p.fill("#nunca", EX.nunca);
  log(await vaiOff() && /ponto de contato/.test(await erro()), "pontos de contato sem resposta bloqueiam");
  for (const [k, v] of Object.entries(EX.pontos)) await radio("p-" + k, v);
  log(!(await vaiOff()) && /aparece em 2/.test(await live()) && /falta em 4/.test(await live()), "2 pontos com a promessa, 4 faltando");
  log((await p.locator('a[href="https://infoprodutos-zion.clickmax.space/kit-mensagens"]').count()) === 1 && (await p.locator('a[href*="adbc67069af26ae0"]').count()) === 0, "aponta para a página de vendas do Kit de Mensagens (Ferramenta 11)");
  await shot("p03-prova"); await p.click("#vai");

  // Tela 3 · lista própria
  log(await telaOk(3, /lista própria/), "tela 3: a lista própria");
  await p.fill("#contatos", "64"); await p.fill("#autorizados", "70");
  log(/não pode passar/.test(await erro()), "autorizados acima dos contatos bloqueia");
  await p.fill("#autorizados", "0"); await p.selectOption("#onde", "celular"); await p.fill("#acesso", EX.acesso); await p.fill("#frase", EX.frase);
  await radio("canalLista", "WhatsApp"); await p.fill("#metaLista", "120"); await p.fill("#estadiasMes", "25");
  log(!(await vaiOff()) && /10 autorizações por mês/.test(await live()) && /40%/.test(await live()), "ritmo ao vivo: 10 autorizações por mês, 40% das estadias");
  await shot("p04-lista"); await p.click("#vai");

  // Tela 4 · canais
  log(await telaOk(4, /Quanto custa cada reserva/), "tela 4: os canais e o custo por reserva");
  log((await p.locator(".canal").count()) === 1 && await vaiOff(), "começa com um canal; bloqueada vazia");
  await p.fill("#mesCanais", EX.mesCanais);
  for (let k = 0; k < 5; k++) {
    if (k > 0) await p.click("#maisCanal");
    const c = EX.canais[k];
    await p.fill(`#c${k}_nome`, c.nome); await p.selectOption(`#c${k}_tipo`, c.tipo);
    await p.fill(`#c${k}_reservas`, String(c.reservas)); await p.fill(`#c${k}_receita`, k === 0 ? "8.120" : String(c.receita).replace(".", ","));
    await p.fill(`#c${k}_comissao`, String(c.comissao)); await p.fill(`#c${k}_gasto`, k === 2 ? "150,00" : String(c.gasto));
  }
  log((await p.locator(".canal").count()) === 5, "adicionar canal: cinco canais na tela");
  log(!(await vaiOff()) && /25/.test(await live()) && /R\$ 77,46/.test(await live()) && /30,0%/.test(await live()), "ao vivo: 25 reservas, R$ 77,46 por reserva, venda direta 30,0% (8.120 lido como oito mil)");
  await p.click("#maisCanal"); await p.fill("#c5_reservas", "3");
  log(await vaiOff() && /Canal 6: dê um nome/.test(await erro()), "linha sem nome com número bloqueia");
  await p.fill("#c5_reservas", "");
  log(!(await vaiOff()), "linha vazia de novo: liberado");
  await shot("p05-canais"); await p.click("#vai");

  // Tela 5 · meta
  log(await telaOk(5, /sem plataforma/), "tela 5: a meta de venda direta");
  log(/30,0%/.test(await p.textContent(".card")) && await p.locator("#doPainel").isVisible(), "mostra a venda direta de hoje e oferece a meta do Painel");
  await p.click("#doPainel");
  log((await p.inputValue("#metaDireta")) === "40" && await vaiOff(), "meta do Painel: 40; sem prazo, bloqueado");
  await p.fill("#prazoMeta", "2027-06-30");
  log(!(await vaiOff()) && /R\$ 6\.496,00/.test(await live()) && /R\$ 255,20/.test(await live()), "meta pede R$ 6.496,00; comissão R$ 255,20");
  log((await p.textContent("#vai")).trim() === "Ver a minha Marca e Captação", "botão final");
  await shot("p06-meta"); await p.click("#vai");

  // Resultado
  const esperado = Z.calcular(EX);
  log(/30,0%/.test(await p.textContent("#resumoNota")) && /meta 40,0% até 30\/06\/2027/.test(await p.textContent("#resumoNota")), "resultado: 30,0% hoje, meta 40% até 30/06/2027");
  const folha = await p.textContent("#folha");
  log(Z.folha(EX).every((l) => folha.includes(l.r) && folha.includes(l.t.slice(0, 30))), "marca em uma folha com as cinco linhas");
  const linhas = await p.locator("#canais tr[data-nome]").all(); let bate = linhas.length === 5;
  for (let k = 0; k < linhas.length; k++) { const tx = await linhas[k].textContent(); const l = esperado.linhas[k]; bate = bate && tx.includes(l.nome) && tx.includes(Z.brl(l.custo)) && tx.includes(Z.brl(l.custoPorReserva)); }
  log(bate && (await p.textContent("#canais")).includes("R$ 1.936,40"), "tabela de canais bate com logic.js, linha a linha, e total R$ 1.936,40");
  const lt = await p.textContent("#leituras");
  log(Z.leituras(esperado, EX).every((x) => lt.includes(x)), "as quatro leituras batem com logic.js");
  const ids = await p.locator("#atencao [data-id]").evaluateAll((els) => els.map((e) => e.getAttribute("data-id")));
  log(ids.join() === "semAutorizacao,guardada,cinco", "atenção: " + ids.join());
  log(/audiência emprestada/.test(await p.textContent("#erroComum")), "erro comum da fonte");
  log((await p.inputValue("#acao")) === Z.planoSugerido(EX), "plano sugerido preenchido igual ao logic.js");
  const card = await p.textContent(".card");
  log(/Módulo 5 · Pessoas e organização das áreas/.test(card), "próxima etapa: Módulo 5");
  log(!/\b(KPI|ADR|RevPAR|OTA|DRE|CRM|LGPD|CPA)\b/.test(card), "sem sigla na tela de resultado");
  log(!/consultoria|mentoria|comunidade|\bcurso\b|Airbnb|—/i.test(await p.evaluate(() => document.body.innerText)), "sem palavras proibidas nem travessão na tela");
  log((await p.locator('a[href="../materiais/planilhas/"]').count()) === 1 && (await p.locator('a[href="../"]').count()) === 1, "links para a planilha e para as ferramentas");
  log(/Falta:.*check-in.*PDF/.test(await p.textContent("#selo")), "selo pendente sem data e PDF");
  await p.fill("#prazo", "2026-11-20"); log(/Falta: o PDF baixado/.test(await p.textContent("#selo")), "com a data, falta só o PDF");
  const ac = await p.inputValue("#acao"); await p.fill("#acao", "curta"); log(/10 letras/.test(await p.textContent("#selo")), "plano curto volta a pendente"); await p.fill("#acao", ac);
  log(await semScrollX(), "sem rolagem horizontal no celular");
  await shot("p07-resultado");
  const [dl] = await Promise.all([p.waitForEvent("download"), p.click("#pdf")]);
  log(dl.suggestedFilename() === "marca-e-captacao.pdf", "PDF baixado: " + dl.suggestedFilename());
  const pdfPath = `${OUT}/marca-e-captacao.pdf`; await dl.saveAs(pdfPath); log(fs.statSync(pdfPath).size > 5000, `PDF com ${fs.statSync(pdfPath).size} bytes`);
  log(/Pronto para avançar/.test(await p.textContent("#selo")), "selo: pronto para avançar após o PDF");

  // persistência
  await p.reload(); await p.waitForFunction(() => !!window.ZM);
  log((await p.locator("#canais tr[data-nome]").count()) === 5 && /Pronto/.test(await p.textContent("#selo")) && (await p.inputValue("#prazo")) === "2026-11-20", "recarregar mantém resultado, data e selo");
  const salvo = await p.evaluate(() => JSON.parse(localStorage.getItem("zion-t2-marketing")));
  log(salvo && salvo.canais[0].receita === "8.120" && salvo.canais[2].gasto === "150,00" && salvo.pontos.whatsapp === "nao" && salvo.pdf, "chave zion-t2-marketing guarda os dados como digitados");
  await p.click("#refaz"); log((await p.textContent(".progresso")).includes("Tela 1 de 5") && (await p.inputValue("#promessa")) === EX.promessa, "refazer volta à tela 1 com as respostas");
  await p.evaluate(() => { const s = JSON.parse(localStorage.getItem("zion-t2-marketing")); s.tela = 0; s.frase = ""; localStorage.setItem("zion-t2-marketing", JSON.stringify(s)); });
  await p.reload(); await p.waitForFunction(() => !!window.ZM);
  log(await p.locator("#retoma").isVisible(), "abertura oferece continuar de onde parei");
  await p.click("#retoma"); log((await p.textContent(".progresso")).includes("Tela 3 de 5"), "continuar leva à primeira tela incompleta (lista)");

  // exemplo didático pelo botão (sem Painel no aparelho)
  await p.evaluate(() => localStorage.clear()); await p.reload(); await p.waitForFunction(() => !!window.ZM);
  await p.click("#exemplo"); log((await p.textContent(".progresso")).includes("Tela 1 de 5") && (await p.inputValue("#promessa")) === EX.promessa, "botão do exemplo leva à tela 1 com os dados fictícios");
  for (let i = 0; i < 3; i++) await p.click("#vai");
  log((await p.locator(".canal").count()) === 6 && (await p.inputValue("#c1_receita")) === "3248", "exemplo mostra os canais (receita 3248)");
  for (let i = 0; i < 2; i++) await p.click("#vai");
  log((await p.locator("#canais tr[data-nome]").count()) === 5 && /Cabanas do Vale \(exemplo\)/.test(await p.textContent(".eyebrow")) && (await p.textContent("#canais")).includes("R$ 108,27"), "exemplo percorre as cinco telas e monta o mesmo resultado");

  // cenário com alertas: lista na plataforma, promessa com adjetivo, gasto sem reserva, meta diferente do Painel
  await p.evaluate((e) => { const s = JSON.parse(JSON.stringify(e)); s.tela = 6; s.onde = "plataforma"; s.autorizados = 10; s.cinco = "5"; s.promessa = "Experiência única e inesquecível"; s.metaDireta = 35; s.canais[5] = { nome: "Anúncio pago", tipo: "direto", comissao: 0, gasto: 200, reservas: 0, receita: 0 }; localStorage.clear(); localStorage.setItem("zion-t2-planejamento", JSON.stringify({ base_vendaDireta: 30, meta_vendaDireta: 40 })); localStorage.setItem("zion-t2-marketing", JSON.stringify(s)); }, EX);
  await p.reload(); await p.waitForFunction(() => !!window.ZM);
  const ids2 = await p.locator("#atencao [data-id]").evaluateAll((els) => els.map((e) => e.getAttribute("data-id")));
  log(ids2.join() === "guardada,adjetivo,gastoSemReserva,painel", "cenário de alertas: " + ids2.join());
  await shot("p08-alertas");

  // desktop
  const d = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await d.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
  await d.route("**/jspdf.umd.min.js", (r) => r.fulfill({ contentType: "application/javascript", body: JSPDF }));
  d.on("pageerror", (e) => erros.push(e.message));
  await d.goto(URL); await d.waitForFunction(() => !!window.ZM); await d.screenshot({ path: `${OUT}/d01-abertura.png`, fullPage: true });
  log(await d.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), "desktop sem rolagem horizontal");
  log(erros.length === 0, "sem erros de JavaScript" + (erros.length ? ": " + erros.join(" | ") : ""));
  await b.close();
  console.log(`\n${ok} ok, ${fal} falhou`); process.exit(fal ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });

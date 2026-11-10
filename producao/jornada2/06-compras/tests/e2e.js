// Teste de ponta a ponta da ficha "A minha Matriz de Compras e Manutenção" no celular.
// Uso: node tests/e2e.js <pasta-saida> <caminho-jspdf.umd.min.js>  (servidor local de docs/ na porta 8816)
const { chromium, devices } = require("playwright");
const fs = require("fs");
const Z = require("../src/logic.js");
const ZF = require("../../../../docs/trilha2/financas/logic.js");
const OUT = process.argv[2], JSPDF = fs.readFileSync(process.argv[3], "utf8");
const URL = "http://localhost:8816/trilha2/compras/";
let ok = 0, fal = 0; const log = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
fs.mkdirSync(OUT, { recursive: true });
const EX = Z.EXEMPLO, esp = Z.calcular(EX), LE = Z.leituras(esp), PE = Z.prioridades(esp);
const vg = (n) => String(n).replace(".", ",");
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

  // Folha do Módulo 2 salva no aparelho (exemplo do Módulo 2)
  await p.goto(URL);
  await p.evaluate((fx) => localStorage.setItem("zion-t2-financas", JSON.stringify({ ...fx, nome: "Ana Exemplo", hospedagem: "Cabanas do Vale (exemplo)" })), ZF.EXEMPLO);
  await p.reload(); await p.waitForFunction(() => !!window.jspdf && !!window.ZC && !!window.ZF);
  log(await p.title() === "Matriz de Compras e Manutenção" && (await p.locator("h1").textContent()) === "A minha Matriz de Compras e Manutenção", "abertura carrega com o título certo");
  log((await p.inputValue("#nome")) === "Ana Exemplo" && (await p.inputValue("#hospedagem")) === "Cabanas do Vale (exemplo)", "nome e hospedagem lidos da Folha do Módulo 2");
  log(/Não é promessa de renda, retorno, ocupação ou resultado/.test(await p.textContent("footer")), "rodapé educacional");
  log(await vaiOff(), "Começar bloqueado sem situação e diagnóstico");
  await confereScroll(); await shot("p01-abertura");
  await p.locator("label.op", { hasText: "Já opero" }).click();
  for (const [q, v] of Object.entries(EX.diag)) await p.locator(`input[name="d-${q}"][value="${v}"]`).locator("xpath=..").click();
  log(/Nível 1 de 4/.test(await p.textContent("#nivel")), "nível 1 de 4 (um sim)");
  log(!(await vaiOff()), "Começar liberado após responder"); await p.click("#vai");

  // Tela 1 · Consumo
  log(/Tela 1 de 5/.test(await p.textContent(".progresso")) && /Em quantas noites/.test(await p.textContent("h2")), "tela 1: o período e o consumo");
  log((await p.inputValue("#mesesPeriodo")) === "3", "três meses vêm preenchidos (regra da fonte)");
  log(await vaiOff(), "tela 1 bloqueada sem as noites");
  await p.click("#importa");
  log((await p.inputValue("#custoVariavelNoite")) === "28,32" && (await p.inputValue("#unidades")) === "4" && /58 noites vendidas/.test(await p.textContent(".card")), "botão traz custo variável 28,32 e 4 unidades da Folha");
  await f("noitesPeriodo", "17,5"); log(await vaiOff() && /inteiro/.test(await p.textContent("#erro")), "noites quebradas bloqueiam");
  await f("noitesPeriodo", "174"); await f("hospedesPeriodo", "150");
  log(!(await vaiOff()) && /58,0/.test(await live()) && /0,86/.test(await live()) && /120/.test(await live()), "58 noites por mês, 0,86 hóspede por noite, 120 noites no mês cheio");
  await confereScroll(); await shot("p02-consumo"); await p.click("#vai");

  // Tela 2 · Matriz
  log(/A Matriz de Compras/.test(await p.textContent(".eyebrow")) && (await p.locator(".item6").count()) === 5, "tela 2: Matriz com cinco linhas");
  for (let i = 0; i < 5; i++) {
    const it = EX.itens[i];
    await f(`i-${i}-nome`, it.nome); await f(`i-${i}-gasto`, vg(it.gasto)); await p.selectOption(`#i-${i}-tipo`, it.tipo); await f(`i-${i}-unidade`, it.unidade);
    await f(`i-${i}-precoAtual`, vg(it.precoAtual)); for (let k = 0; k < 3; k++) await f(`i-${i}-c${k}`, vg(it.cot[k])); await p.selectOption(`#i-${i}-contrato`, it.contrato);
  }
  log(await vaiOff() && /até quando vai fechar/.test(await p.textContent("#erro")), "contrato a fechar sem data bloqueia");
  await p.fill("#prazoContratos", "2027-03-31");
  const lm = await live();
  log(!(await vaiOff()) && /R\$ 3\.900,00/.test(lm) && /R\$ 15,17/.test(lm) && /53,6%/.test(lm) && /R\$ 437,00/.test(lm) && /três cotações: 5/.test(lm), "total 3.900, variáveis 15,17 por noite (53,6%), diferença 437, 5 com três cotações");
  await f("i-1-c2", "abc"); log(await vaiOff() && /cotação inválida/.test(await p.textContent("#erro")), "cotação com texto bloqueia");
  await f("i-1-c2", ""); log(!(await vaiOff()) && /2 de 3 cotações/.test(await p.textContent("#avisos")), "duas cotações: aviso");
  await f("i-1-c2", "3,20");
  await p.click("#addItem"); log((await p.locator(".item6").count()) === 6, "adicionar item cria uma sexta linha");
  await p.locator("[data-rm='5']").click(); log((await p.locator(".item6").count()) === 5 && (await p.inputValue("#i-0-nome")) === EX.itens[0].nome, "remover item mantém os outros");
  await confereScroll(); await shot("p03-matriz"); await p.click("#vai");

  // Tela 3 · Estoque
  log(/Quando pedir/.test(await p.textContent("h2")) && (await p.inputValue("#e-0-seguranca")) === "7" && (await p.inputValue("#e-0-ciclo")) === "30", "tela 3: estoque com segurança 7 e ciclo 30 sugeridos");
  log(await vaiOff(), "estoque vazio bloqueia");
  await p.click("#addEst"); await p.click("#addEst");
  for (let i = 0; i < 4; i++) { const e = EX.estoque[i]; for (const k of ["nome", "unidade", "usoMes", "atual", "entrega", "seguranca", "ciclo"]) await f(`e-${i}-${k}`, vg(e[k])); }
  await f("camas", "4");
  log(await vaiOff() && /jogos de cama/.test(await p.textContent("#erro")), "camas sem jogos bloqueia");
  await f("jogos", "10");
  const le = await p.innerHTML("#live");
  log(!(await vaiOff()) && /Papel higiênico: mínimo <b>24<\/b>, ponto de pedido <b>40<\/b> <span class="tag">pedir 110<\/span>/.test(le) && /Kit de amenidades: mínimo <b>6<\/b>, ponto de pedido <b>12<\/b>/.test(le) && /<b>2,5<\/b> jogos por cama/.test(le), "papel: mínimo 24, ponto 40, pedir 110; kit 6/12; 2,5 jogos por cama");
  await confereScroll(); await shot("p04-estoque"); await p.click("#vai");

  // Tela 4 · Manutenção
  log(/O que a casa precisa/.test(await p.textContent("h2")), "tela 4: calendário de manutenção");
  log((await p.inputValue("#receitaReserva")) === "13565,6", "receita real da Folha trazida para a reserva (13.565,60)");
  await f("ano", "2027"); await f("receitaReserva", "13.565,60"); await f("reservaPct", "2");
  log(/3% a 6%/.test(await p.textContent("#avisos")), "reserva de 2%: aviso da fonte");
  await f("reservaPct", "3");
  for (const m of EX.casaCheia) await p.locator(`[data-cheia="${m}"]`).locator("xpath=..").click();
  for (let i = 0; i < 6; i++) await p.click("#addTar");
  for (let i = 0; i < 9; i++) { const t = EX.tarefas[i]; await f(`t-${i}-nome`, t.nome); await p.selectOption(`#t-${i}-freq`, t.freq); await p.selectOption(`#t-${i}-inicio`, String(t.inicio)); await f(`t-${i}-custo`, vg(t.custo)); await f(`t-${i}-quem`, t.quem); }
  const lt = await live();
  log(!(await vaiOff()) && /Tarefas no ano: 17/.test(lt) && /R\$ 3\.690,00/.test(lt) && /R\$ 4\.883,62/.test(lt) && !/Na casa cheia/.test(lt), "17 tarefas, R$ 3.690 no ano, reserva de 4.883,62, nada na casa cheia");
  await p.selectOption("#t-8-inicio", "7"); log(/Na casa cheia:.*deck/.test(await live()), "deck em julho: aparece na casa cheia");
  await p.selectOption("#t-8-inicio", "1"); log(/Reserva não cobre em janeiro/.test(await live()), "deck em janeiro: reserva não cobre");
  await p.selectOption("#t-8-inicio", "11");
  await p.selectOption("#t-0-freq", ""); log(await vaiOff() && /frequência/.test(await p.textContent("#erro")), "tarefa sem frequência bloqueia");
  await p.selectOption("#t-0-freq", "trimestral");
  await confereScroll(); await shot("p05-manutencao"); await p.click("#vai");

  // Tela 5 · Rotina
  log(/Quem compra/.test(await p.textContent("h2")) && (await p.locator('a[href="../../p/adbc67069af26ae0/ocorrencias-14/"]').count()) === 1 && (await p.locator('a[href="../../p/adbc67069af26ae0/manutencao-18/"]').count()) === 1, "tela 5: rotina com as Ferramentas 14 e 18");
  await p.selectOption("#diaContagem", "segunda-feira"); await f("quemCompra", "Ana (dona)"); await f("alcada", "300"); await p.check("#ronda"); await p.check("#ocorrencias");
  log(/segunda-feira/.test(await live()) && /R\$ 300,00/.test(await live()) && /Ronda diária: sim/.test(await live()), "rotina: segunda-feira, limite de R$ 300, ronda");
  log((await p.textContent("#vai")).trim() === "Ver a minha Matriz", "botão final: Ver a minha Matriz");
  await confereScroll(); await shot("p06-rotina"); await p.click("#vai");

  // Resultado
  const card = await p.textContent(".card");
  log((await p.textContent("#porNoite")).trim() === "R$ 15,17" && /R\$ 437,00/.test(card) && /R\$ 3\.690,00/.test(card) && /R\$ 4\.883,62/.test(card), "resultado: 15,17 por noite, diferença 437, plano 3.690, reserva 4.883,62");
  const mt = await p.locator("#matriz .mxi").allTextContents();
  log(mt.length === 6 && /^1\. Café/.test(mt[0]) && esp.itens.every((it, i) => mt[i].includes(Z.brl(it.porNoite)) && mt[i].includes(Z.brl(it.diferenca)) && mt[i].includes(Z.brl(it.gasto))) && /R\$ 3\.900,00/.test(mt[5]), "Matriz por valor, item a item igual a logic.js");
  log(/por hóspede: R\$ 5,20/.test(await p.textContent("#matriz")) && /sem contrato/.test(await p.textContent("#matriz")) && /fechar até 31\/03\/2027/.test(await p.textContent("#matriz")), "consumo por hóspede e situação dos contratos");
  const et = await p.locator("#estoque tr").allTextContents();
  log(et.length === 5 && /Papel.*24.*40.*110/.test(et[2]) && /ok/.test(et[1]), "estoque: papel pede 110, kit ok");
  const ct = await p.locator("#calendario tr").allTextContents();
  log(ct.length === 14 && esp.meses.every((m, i) => ct[i + 1].includes(Z.brl(m.custo))) && /nov.*Tratamento do deck.*R\$ 1\.330,00/.test(ct[11]) && /jul \*/.test(ct[7]), "calendário de 12 meses bate com logic.js (novembro 1.330; julho marcado)");
  const leit = await p.textContent("#leituras");
  log([LE.peso, LE.consumo, LE.mesCheio, LE.cotacao, LE.contrato, LE.estoque, LE.enxoval, LE.manutencao, LE.reserva, LE.casaCheia].every((l) => leit.includes(l.t)), "as dez leituras batem com logic.js");
  log(/Causa principal: Compra recorrente sem contrato/.test(await p.textContent("#causa")), "causa principal: compra recorrente sem contrato");
  log((await p.locator("#prioridades > div").count()) === 3 && /Item no ponto de pedido/.test(await p.textContent("#prioridades")) && /três jogos por cama/.test(await p.textContent("#prioridades")), "três prioridades: contrato, pedido, enxoval");
  log((await p.inputValue("#acao")) === Z.planoSugerido(PE), "plano de ação sugerido preenchido");
  log(!/\b(ADR|RevPAR|OTA|PMS|KPI|DRE|EOQ)\b/.test(card), "sem sigla na tela de resultado");
  log(/Módulo 7 · Qualidade, reputação e plano de crescimento/.test(card) && (await p.locator('a[href="../../p/adbc67069af26ae0/enxoval-13/"]').count()) === 1 && (await p.locator('a[href*="Matriz-de-Compras-e-Manutencao-Zion-EM-BRANCO.xlsx"]').count()) === 1, "próxima etapa, planilha e Ferramenta 13");
  log(/Falta:.*PDF/.test(await p.textContent("#selo")), "selo pendente antes do prazo e do PDF");
  await p.fill("#prazo", "2027-01-31"); log(/Falta: o PDF baixado/.test(await p.textContent("#selo")), "com prazo, falta só o PDF");
  await p.fill("#acao", "curta"); log(/10 letras/.test(await p.textContent("#selo")), "ação curta volta a pendente");
  await p.fill("#acao", "Fechar contrato do gás com preço e prazo até março.");
  await confereScroll(); await shot("p07-resultado");
  const [dl] = await Promise.all([p.waitForEvent("download"), p.click("#pdf")]);
  log(dl.suggestedFilename() === "matriz-de-compras-e-manutencao.pdf", "PDF baixado: " + dl.suggestedFilename());
  const pdfPath = `${OUT}/matriz-compras.pdf`; await dl.saveAs(pdfPath); log(fs.statSync(pdfPath).size > 5000, `PDF com ${fs.statSync(pdfPath).size} bytes`);
  log(/Pronto para avançar/.test(await p.textContent("#selo")), "selo: pronto para avançar após o PDF");
  // persistência
  await p.reload(); await p.waitForFunction(() => !!window.ZC);
  log((await p.textContent("#porNoite")).trim() === "R$ 15,17" && (await p.inputValue("#prazo")) === "2027-01-31" && /Pronto/.test(await p.textContent("#selo")), "recarregar mantém resultado, prazo e selo");
  const salvo = await p.evaluate(() => JSON.parse(localStorage.getItem("zion-t2-compras")));
  log(salvo && salvo.noitesPeriodo === "174" && salvo.itens.length === 5 && salvo.estoque.length === 4 && salvo.tarefas.length === 9 && salvo.pdf && salvo.situacao === "dono", "chave zion-t2-compras guarda os dados como digitados");
  await p.click("#refaz"); log(/Tela 1 de 5/.test(await p.textContent(".progresso")) && (await p.inputValue("#noitesPeriodo")) === "174", "refazer volta à tela 1 com as respostas");
  await p.evaluate(() => { const s = JSON.parse(localStorage.getItem("zion-t2-compras")); s.tela = 0; localStorage.setItem("zion-t2-compras", JSON.stringify(s)); });
  await p.reload(); await p.waitForFunction(() => !!window.ZC);
  log(await p.locator("#retoma").isVisible(), "abertura oferece continuar de onde parei");
  await p.click("#retoma"); log(/A minha Matriz de Compras e Manutenção/.test(await p.textContent(".eyebrow")), "continuar leva ao resultado quando tudo está preenchido");
  // exemplo didático pelo botão
  await p.evaluate(() => localStorage.clear()); await p.reload(); await p.waitForFunction(() => !!window.ZC);
  await p.click("#exemplo"); log(/Tela 1 de 5/.test(await p.textContent(".progresso")) && (await p.inputValue("#noitesPeriodo")) === "174", "botão do exemplo leva à tela 1 preenchida");
  for (let i = 0; i < 5; i++) { await p.click("#vai"); await confereScroll(); }
  log((await p.textContent("#porNoite")).trim() === "R$ 15,17" && /Cabanas do Vale \(exemplo\)/.test(await p.textContent(".eyebrow")) && /R\$ 1\.193,62/.test(await p.textContent(".card")), "exemplo percorre as cinco telas e dá o mesmo resultado");
  // cenário resolvido: contrato, estoque e enxoval em dia
  await p.click("#refaz"); await p.click("#vai");
  await p.selectOption("#i-3-contrato", "sim"); await p.click("#vai");
  await f("e-1-atual", "200"); await f("jogos", "12"); await p.click("#vai"); await p.click("#vai"); await p.click("#vai");
  log(/Causa principal: Compras e manutenção dentro das regras da fonte/.test(await p.textContent("#causa")), "tudo resolvido: dentro das regras da fonte");
  await shot("p08-dentro");
  // desktop
  const d = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await d.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
  await d.route("**/jspdf.umd.min.js", (r) => r.fulfill({ contentType: "application/javascript", body: JSPDF }));
  await d.goto(URL); await d.waitForFunction(() => !!window.ZC); await d.screenshot({ path: `${OUT}/d01-abertura.png`, fullPage: true });
  log(scrollOk, "sem rolagem horizontal no celular em nenhuma tela");
  log(erros.length === 0, "sem erros de JavaScript" + (erros.length ? ": " + erros.join(" | ") : ""));
  await b.close();
  console.log(`\n${ok} ok, ${fal} falhou`); process.exit(fal ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });

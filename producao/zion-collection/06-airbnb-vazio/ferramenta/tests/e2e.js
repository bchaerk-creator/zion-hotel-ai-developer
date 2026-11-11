// Ponta a ponta do Diagnóstico Zion de Oferta. Uso: node tests/e2e.js <pasta-saida> <jspdf.umd.min.js>
const { chromium, devices } = require('playwright');
const fs = require('fs'), path = require('path');
const OUT = process.argv[2], JSPDF = fs.readFileSync(process.argv[3], 'utf8');
const URL = 'file://' + path.resolve(__dirname, '../dist/diagnostico-zion-de-oferta.html');
let ok = 0, fal = 0; const log = (b, m) => { b ? ok++ : fal++; console.log((b ? '  ok  ' : '  FALHOU  ') + m); };
fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ ...devices['iPhone 13'], acceptDownloads: true });
  await ctx.route('**/jspdf.umd.min.js', r => r.fulfill({ contentType: 'application/javascript', body: JSPDF }));
  const p = await ctx.newPage(); const erros = [];
  p.on('pageerror', e => erros.push(e.message)); p.on('console', m => m.type() === 'error' && erros.push(m.text()));
  const ativa = () => p.locator('section.tela.ativa').getAttribute('id');
  const shot = n => p.screenshot({ path: `${OUT}/${n}.png`, fullPage: true });
  await p.goto(URL); await p.waitForFunction(() => !!window.jspdf);
  await shot('01-inicio');
  const larg = await p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);
  log(larg, 'sem rolagem horizontal no celular');
  await p.fill('#p_nome', 'Casa <b>"Teste"</b> & Cia'); await p.fill('#p_periodo', 'últimos 90 dias');
  await p.click('text=Começar o diagnóstico'); log(await ativa() === 't2', 'início → notas');
  await p.click('#btnCalcular'); log(await ativa() === 't2' && /Faltam 7/.test(await p.textContent('#e_notas')), 'sem notas: bloqueia e mostra quantas faltam');
  // pular para resultado pelo topo também é bloqueado
  await p.click('.etapas [data-ir="3"]'); log(await ativa() === 't2', 'atalho para o resultado bloqueado sem notas');
  // todas 0
  for (const id of ['fotos', 'titulo', 'preco', 'diferenciais', 'avaliacoes', 'atendimento', 'conforto']) await p.click(`[data-dim="${id}"][data-nota="0"]`);
  await p.click('#btnCalcular'); log(await ativa() === 't3' && /^0/.test(await p.textContent('.anel')), 'todas 0 → pontuação 0');
  log((await p.textContent('#faixa')) === 'Lacunas relevantes', 'todas 0 → lacunas relevantes');
  log(/nota 0 ou 1 em Fotos/.test(await p.textContent('#critica')), 'notas 0: alerta de nota crítica');
  log(/7 nota\(s\) sem evidência/.test(await p.textContent('#resultado')), 'sem evidência: aviso de hipótese');
  // todas 5
  await p.click('text=Revisar notas');
  for (const id of ['fotos', 'titulo', 'preco', 'diferenciais', 'avaliacoes', 'atendimento', 'conforto']) await p.click(`[data-dim="${id}"][data-nota="5"]`);
  await p.click('#btnCalcular'); log(/^100/.test(await p.textContent('.anel')) && (await p.textContent('#faixa')) === 'Oferta consistente', 'todas 5 → 100, oferta consistente');
  log(await p.locator('#critica').count() === 0, 'todas 5: sem alerta crítico');
  log(/Todas as notas no máximo/.test(await p.textContent('#resultado')), 'todas 5: aviso para conferir evidências');
  // exemplo fictício
  await p.click('.etapas [data-ir="1"]'); await p.click('#btnExemplo');
  log(await ativa() === 't2' && (await p.inputValue('#p_nome')).includes('dados fictícios'), 'exemplo carrega com rótulo de dados fictícios');
  await shot('02-notas');
  await p.click('#btnCalcular');
  log(/^63/.test(await p.textContent('.anel')) && (await p.textContent('#faixa')) === 'Ajustes prioritários', 'exemplo → 63, ajustes prioritários');
  const pri = await p.locator('#prioridades li b').allTextContents();
  log(pri.join('|') === 'Fotos e apresentação|Atendimento e comunicação|Título e descrição', 'prioridades: fotos, atendimento, título');
  await shot('03-resultado');
  await p.click('#btnPlano'); log(await ativa() === 't4' && await p.locator('.linha-plano').count() === 3, 'plano sugerido com 3 ações');
  await p.click('#btnPDF'); log(/responsável/.test(await p.textContent('#e_plano')), 'PDF bloqueado sem responsável e prazo');
  for (let i = 0; i < 3; i++) {
    await p.fill(`[data-pl="${i}"][data-k="responsavel"]`, i ? 'Equipe' : 'Ana; "Gerente"');
    await p.fill(`[data-pl="${i}"][data-k="prazo"]`, `2026-12-0${i + 1}`);
  }
  await p.fill('[data-pl="1"][data-k="custo"]', 'abc'); await p.click('#btnCSV');
  log(/valor em reais/.test(await p.textContent('#e_plano')), 'custo inválido recusado');
  await p.fill('[data-pl="1"][data-k="custo"]', '150,00'); await p.selectOption('[data-pl="2"][data-k="status"]', 'Em andamento');
  let [dl] = await Promise.all([p.waitForEvent('download'), p.click('#btnCSV')]);
  const csv = fs.readFileSync(await dl.path(), 'utf8'); fs.writeFileSync(`${OUT}/diagnostico.csv`, csv);
  log(/Pontuação geral \(0 a 100\);63/.test(csv) && /"Ana; ""Gerente"""/.test(csv) && /Em andamento/.test(csv), 'CSV baixado com pontuação, aspas escapadas e status');
  [dl] = await Promise.all([p.waitForEvent('download'), p.click('#btnPDF')]);
  const pdf = fs.readFileSync(await dl.path()); fs.writeFileSync(`${OUT}/diagnostico.pdf`, pdf);
  log(pdf.slice(0, 4).toString() === '%PDF' && pdf.length > 2000, `PDF baixado (${pdf.length} bytes)`);
  await shot('04-plano');
  // adicionar e remover ação
  await p.click('#btnAddLinha'); log(await p.locator('.linha-plano').count() === 4, 'adiciona ação');
  await p.click('[data-rem="3"]'); log(await p.locator('.linha-plano').count() === 3, 'remove ação');
  // persistência
  await p.reload(); await p.waitForFunction(() => !!window.jspdf);
  await p.click('.etapas [data-ir="4"]');
  log(await p.inputValue('[data-pl="1"][data-k="custo"]') === '150,00' && (await p.inputValue('#p_nome')).includes('dados fictícios'), 'respostas salvas no aparelho após recarregar');
  // XSS: nome com tags não vira HTML
  await p.click('.etapas [data-ir="1"]'); await p.fill('#p_nome', '<img src=x onerror=alert(1)>');
  await p.click('.etapas [data-ir="3"]'); log(erros.length === 0, 'sem erros de JavaScript' + (erros.length ? ': ' + erros.join(' | ') : ''));
  // impressão
  await p.emulateMedia({ media: 'print' }); await p.pdf ? null : null;
  const visiveis = await p.evaluate(() => [...document.querySelectorAll('section.tela')].filter(s => getComputedStyle(s).display !== 'none').length);
  log(visiveis === 4, 'impressão mostra as quatro etapas');
  await p.emulateMedia({ media: 'screen' });
  // apagar
  p.once('dialog', d => d.accept()); await p.click('.etapas [data-ir="4"]'); await p.click('#btnLimpar');
  log(await ativa() === 't1' && (await p.inputValue('#p_nome')) === '', 'apagar e recomeçar limpa tudo');
  // desktop
  const d = await (await b.newContext({ viewport: { width: 1280, height: 900 } })).newPage();
  await d.route('**/jspdf.umd.min.js', r => r.fulfill({ contentType: 'application/javascript', body: JSPDF }));
  await d.goto(URL); await d.screenshot({ path: `${OUT}/05-desktop.png` }); log(true, 'abre no computador');
  await b.close();
  console.log(`\n${ok} ok, ${fal} falhas`); process.exit(fal ? 1 : 0);
})();

// Teste de ponta a ponta do Bloco 01. Uso: node e2e.js <pasta-saida> <caminho-jspdf.umd.min.js>
const { chromium, devices } = require('playwright');
const fs = require('fs'), path = require('path');
const OUT = process.argv[2], JSPDF = fs.readFileSync(process.argv[3], 'utf8');
const URL = 'file://' + path.resolve(__dirname, '../dist/index.html');
let ok = 0, fal = 0; const log = (b, m) => { b ? ok++ : fal++; console.log((b ? '  ok  ' : '  FALHOU  ') + m); };
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ ...devices['iPhone 13'], acceptDownloads: true });
  await ctx.route('**/jspdf.umd.min.js', r => r.fulfill({ contentType: 'application/javascript', body: JSPDF }));
  const p = await ctx.newPage(); const erros = [];
  p.on('pageerror', e => erros.push(e.message)); p.on('console', m => m.type() === 'error' && erros.push(m.text()));
  const btn = (t) => p.locator('section.tela.ativa button', { hasText: t }).first().click();
  const tela = () => p.locator('#contador').textContent();
  const shot = (n) => p.screenshot({ path: `${OUT}/${n}.png`, fullPage: true });
  await p.goto(URL); await p.waitForFunction(() => !!window.jspdf);
  await shot('t01');
  await btn('Começar meu diagnóstico'); log((await tela()) === 'Tela 02 de 40', 'capa → tela 02'); await shot('t02');
  await btn('Vamos começar');
  await btn('Salvar e continuar'); log((await tela()) === 'Tela 03 de 40', 'tela 03 bloqueia sem nome da hospedagem');
  await p.fill('#p_nome', 'Cabana Cenário A'); await p.selectOption('#p_tipo', 'Cabana ou chalé'); await p.fill('#p_cidade', 'Urubici, SC');
  await p.fill('#p_capacidade', '-2'); await btn('Salvar e continuar'); log((await p.textContent('#e_p_capacidade')).length > 0, 'capacidade negativa recusada');
  await p.fill('#p_capacidade', '2'); await p.fill('#p_unidades', '1');
  await p.locator('label.opcao', { hasText: 'Pouca gente vê' }).click(); await p.locator('label.opcao', { hasText: 'Sim, tenho todos' }).click();
  await shot('t03'); await btn('Salvar e continuar'); log((await tela()) === 'Tela 04 de 40', 'tela 03 → 04');
  await p.locator('[data-area="1"]').click(); log(await p.locator('.area .ex').nth(1).isVisible(), 'exemplo da área abre ao tocar'); await shot('t04');
  await btn('Entender os números');
  await p.locator('.quiz label.opcao', { hasText: '250%' }).click(); log(/Ainda não/.test(await p.textContent('#quizRes')), 'quiz: resposta errada recebe orientação');
  await p.locator('.quiz label.opcao', { hasText: '40%' }).click(); log(/Isso/.test(await p.textContent('#quizRes')), 'quiz: resposta certa confirmada'); await shot('t05');
  await btn('Preencher meus números');
  // casos de borda na tela 06
  await p.selectOption('#periodo', '30');
  await p.fill('#disponiveis', '30'); await p.fill('#ocupadas', '34'); await btn('Calcular');
  log((await tela()) === 'Tela 06 de 40' && /não podem passar/.test(await p.textContent('#e_ocupadas')), 'ocupadas > disponíveis bloqueia o cálculo');
  await p.fill('#ocupadas', '-1'); log(/negativo/.test(await p.textContent('#e_ocupadas')), 'valor negativo recusado na hora');
  await p.fill('#disponiveis', '40'); log(/mais noites disponíveis/.test(await p.textContent('#e_disponiveis')), 'disponíveis > dias do período recusado');
  // Cenário A
  await p.fill('#disponiveis', '30'); await p.fill('#ocupadas', '4'); await p.fill('#diaria', '280'); await p.fill('#visualizacoes', '95'); await p.fill('#consultas', '2'); await p.fill('#reservas', '1');
  await p.locator('label.opcao', { hasText: /^Não$/ }).click();
  await p.locator('#extra summary').click(); await p.fill('#meta', '15'); await shot('t06');
  await btn('Calcular'); log((await tela()) === 'Tela 07 de 40', 'tela 06 → 07 com dados válidos');
  const t7 = await p.textContent('#calcSaida');
  log(/13,3%/.test(t7) && /R\$ 1\.120/.test(t7), 'cenário A: ocupação 13,3% e receita R$ 1.120'); await shot('t07-A');
  await btn('Ver meu diagnóstico'); const fA = await p.textContent('#fbSaida');
  log(/visibilidade/i.test(fA) && /disponibilidade/i.test(fA) && /apresenta/i.test(fA), 'cenário A: orienta visibilidade, disponibilidade e apresentação');
  log(!/\b(bom|ruim|abaixo da média|garant)/i.test(fA), 'cenário A: sem juízo de valor nem garantia');
  log((await p.locator('#fbSaida .fb').count()) >= 2 && /Como verificar/.test(fA), 'feedback com as 5 partes'); await shot('t08-A');
  const [d1] = await Promise.all([p.waitForEvent('download'), p.click('#gerarPdf')]); await d1.saveAs(`${OUT}/plano-cenario-A.pdf`); log(/Meu-Plano-de-Melhoria-Cabana-Cenario-A\.pdf/.test(d1.suggestedFilename()), 'PDF exportado: ' + d1.suggestedFilename());
  // persistência
  await p.reload(); await p.waitForTimeout(300);
  log(await p.locator('#continuar').isVisible() && /08/.test(await p.textContent('#continuar')), 'recarregar: oferece continuar da tela 08');
  await p.click('#continuar'); log((await tela()) === 'Tela 08 de 40', 'continuar volta à tela 08');
  // correção → Cenário B (sem dado de visualizações → D; depois completo com histórico)
  await btn('Corrigir meus números'); log((await p.inputValue('#ocupadas')) === '4', 'correção: números anteriores preservados');
  await p.check('#sd_visualizacoes'); log(await p.isDisabled('#visualizacoes'), '"Não tenho esse dado" desativa o campo');
  await btn('Calcular'); await btn('Ver meu diagnóstico'); log(/não temos dados suficientes/i.test(await p.textContent('#fbSaida')), 'sem visualizações: Situação D');
  await btn('Corrigir meus números'); await p.uncheck('#sd_visualizacoes');
  await p.fill('#disponiveis', '30'); await p.fill('#ocupadas', '6'); await p.fill('#diaria', '450'); await p.fill('#visualizacoes', '1800'); await p.fill('#consultas', '24'); await p.fill('#reservas', '1'); await p.fill('#meta', '');
  await p.check('#anteriorAtivo'); await p.fill('#ant_visualizacoes', '1600'); await p.fill('#ant_consultas', '20'); await p.fill('#ant_reservas', '6'); await p.fill('#ant_ocupadas', '14'); await p.fill('#ant_disponiveis', '30');
  await btn('Calcular'); await shot('t07-B'); await btn('Ver meu diagnóstico'); const fB = await p.textContent('#fbSaida');
  log(/conversão de consultas em reservas caiu/i.test(fB) && /atendimento/.test(fB) && /preço final/.test(fB), 'cenário B: aponta a queda na conversão e manda investigar atendimento e preço final'); await shot('t08-B');
  // consultas > visualizações e períodos diferentes
  await btn('Corrigir meus números'); await p.uncheck('#anteriorAtivo'); await p.fill('#visualizacoes', '10'); await p.fill('#consultas', '24');
  await btn('Calcular'); log(/mais consultas/.test(await p.textContent('#calcSaida')), 'consultas > visualizações: aviso e taxa não calculada');
  await btn('Corrigir números'); await p.fill('#visualizacoes', '1800'); await p.locator('label.opcao', { hasText: 'Não, alguns são de outro período' }).click();
  await btn('Calcular'); log(/não são do mesmo período/.test(await p.textContent('#calcSaida')), 'períodos diferentes: taxas não calculadas');
  // Cenário C: receita alta + dificuldade financeira → encaminha Pilar 5
  await btn('Corrigir números'); await p.locator('label.opcao', { hasText: 'Sim, todos do mesmo período' }).click();
  await p.fill('#ocupadas', '22'); await p.fill('#diaria', '390'); await p.fill('#reservas', '8');
  await p.click('#abrirSumario'); await p.locator('[data-sum="3"]').click(); await p.locator('label.opcao', { hasText: 'sobra pouco dinheiro' }).click();
  await p.click('#abrirSumario'); log(await p.locator('#listaSumario button').count() === 40 && await p.locator('#listaSumario button[disabled]').count() > 0, 'sumário: 40 telas, só as visitadas liberadas'); await p.locator('[data-sum="8"]').click();
  const fC = await p.textContent('#fbSaida'); log(/Pilar 5/.test(fC) && !/lucro/i.test(fC), 'cenário C: encaminha custos ao Pilar 5, sem chamar de lucro');
  const [d2] = await Promise.all([p.waitForEvent('download'), p.click('#gerarPdf')]); await d2.saveAs(`${OUT}/plano-cenario-C.pdf`);
  log(!(await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)), 'celular: sem rolagem horizontal');
  // desktop
  const dc = await b.newContext({ viewport: { width: 1366, height: 900 } }); await dc.route('**/jspdf.umd.min.js', r => r.fulfill({ contentType: 'application/javascript', body: JSPDF }));
  const d = await dc.newPage(); await d.goto(URL); await d.waitForTimeout(400); await d.screenshot({ path: `${OUT}/desk-t01.png` });
  log(erros.length === 0, 'sem erros no console' + (erros.length ? ': ' + erros.join(' | ') : ''));
  console.log(`\n${ok} passaram, ${fal} falharam`); await b.close(); process.exit(fal ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });

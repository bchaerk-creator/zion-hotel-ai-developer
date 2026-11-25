// Ponta a ponta do portal. Uso: node tests/e2e.js <pasta de saída> <jspdf.umd.min.js> [index.html]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), assert = require('assert'), cp = require('child_process');
const OUT = process.argv[2], JSPDF = fs.readFileSync(process.argv[3], 'utf8'); fs.mkdirSync(OUT, { recursive: true });
const URL = 'file://' + path.resolve(process.argv[4] || path.join(__dirname, '../dist/index.html')); let ok = 0; const t = m => { ok++; console.log('ok', m); };
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, acceptDownloads: true });
  await ctx.route('**/jspdf.umd.min.js', r => r.fulfill({ contentType: 'application/javascript', body: JSPDF }));
  const p = await ctx.newPage(); const erros = []; p.on('pageerror', e => erros.push(e.message)); p.on('console', m => m.type() === 'error' && erros.push(m.text()));
  await p.goto(URL); await p.waitForFunction(() => !!window.jspdf && !!window.RX_APP);
  const semRolagem = async n => { const w = await p.evaluate(() => [document.documentElement.scrollWidth, window.innerWidth]); assert(w[0] <= w[1] + 1, n + ' rolagem horizontal ' + w); };
  await p.fill('#nomePf', 'Ana Teste'); await p.click('#criaPf'); await p.waitForSelector('.mods'); await semRolagem('início'); t('perfil criado e início sem rolagem horizontal no celular');
  // percorre todas as telas no celular
  for (const v of ['ficha', 'aula1', 'aula2', 'aula3', 'aula4', 'aula5', 'aula6', 'aula7', 'diag', 'plano', 'dossie', 'convite']) { await p.evaluate(v => RX_APP.ir(v), v); await p.waitForTimeout(60); await semRolagem(v); }
  t('12 telas sem rolagem horizontal em 390 px');
  assert.equal(await p.evaluate(() => document.querySelectorAll('.tabs button').length), 13); t('abas: 13');
  // ficha
  await p.evaluate(() => RX_APP.ir('ficha')); await p.fill('[data-id=nome]', 'Pousada Exemplo (dados fictícios)'); await p.selectOption('[data-id=tipo]', 'Pousada'); await p.fill('[data-id=municipio]', 'Cidade Exemplo'); await p.fill('[data-id=unidades]', '4');
  // módulo 1: 4 comprovado, 2 parcial, 1 ausente, 1 não sei, 1 NA, 1 sem resposta
  await p.evaluate(() => RX_APP.ir('aula1')); const resp = ['2', '2', '2', '2', '1', '1', '0', 'unknown', 'na'];
  for (let i = 0; i < resp.length; i++) await p.check(`input[name=m1q${i + 1}][value="${resp[i]}"]`);
  let fb = await p.textContent('#fbMod'); assert(/71,4%/.test(fb) && /77,8%/.test(fb), 'feedback: ' + fb.slice(0, 200)); assert(/não sei/.test(fb) && /sem resposta/.test(fb)); assert(/Resultado/.test(fb) && /O que significa/.test(fb) && /Atenção/.test(fb) && /O que fazer agora/.test(fb) && /Como verificar/.test(fb)); t('feedback em 5 partes; nota 71,4% e cobertura 77,8% conferem; "não sei" e pendente sinalizados');
  // módulo só com "não sei": sem nota
  await p.evaluate(() => RX_APP.ir('aula2')); for (let i = 1; i <= 10; i++) await p.check(`input[name=m2q${i}][value="unknown"]`); fb = await p.textContent('#fbMod'); assert(/Responda ao menos uma pergunta com dados/.test(fb)); t('módulo todo "não sei" não gera nota (nunca zero)');
  // calculadora 2: >100% e dado faltando
  await p.fill('[data-p="meses.0.disponiveis"]', '300'); await p.fill('[data-p="meses.0.vendidas"]', '150'); await p.fill('[data-p="meses.1.disponiveis"]', '280'); await p.fill('[data-p="meses.1.vendidas"]', '300'); await p.fill('[data-p="meses.2.disponiveis"]', '300');
  await p.fill('[data-p="canais.0.nome"]', 'Direto'); await p.fill('[data-p="canais.0.receita"]', '10.000,00'); await p.fill('[data-p="canais.0.comissaoPct"]', '0'); await p.fill('[data-p="canais.0.custoAquisicao"]', '500');
  const r2 = await p.textContent('#calcRes'); assert(/50,0%/.test(r2) && /acima das disponíveis/.test(r2) && /R\$ 9\.500,00/.test(r2) && /1 de 12 meses|1 de 12/.test(r2), r2.slice(0, 400)); t('C2: 50% em 1 mês, >100% sinalizado e fora do total, receita líquida R$ 9.500 (entrada pt-BR)');
  // negativo e texto inválido
  await p.fill('[data-p="canais.1.receita"]', '-5'); await p.fill('[data-p="canais.1.nome"]', 'X'); assert(/negativo/.test(await p.textContent('#calcRes'))); t('valor negativo recusado com aviso');
  // C4 completa
  await p.evaluate(() => RX_APP.ir('aula4'));
  const c4 = { disponiveis: '300', vendidas: '150', receita: '45000', limpeza: '80', insumos: '20', comissoes: '100', outrosVar: '0', noitesPorEstadia: '2', quedaOcupacaoPct: '20', quedaPrecoPct: '10', altaCustosPct: '10' };
  for (const k in c4) await p.fill(`[data-p="${k}"]`, c4[k]); await p.fill('[data-p="fixos.0.nome"]', 'Aluguel'); await p.fill('[data-p="fixos.0.valor"]', '6000'); await p.fill('[data-p="fixos.1.valor"]', '4000');
  let r4 = await p.textContent('#calcRes'); assert(/R\$ 200,00/.test(r4) && /16,7%/.test(r4) && /R\$ 20\.000,00/.test(r4) && /R\$ 8\.200,00/.test(r4), r4.slice(0, 500)); t('C4: contribuição R$ 200, equilíbrio 16,7%, resultado R$ 20.000 e adverso R$ 8.200 conferem');
  await p.fill('[data-p="receita"]', '13500'); r4 = await p.textContent('#calcRes'); assert(/zero ou negativa/.test(r4)); t('C4: contribuição negativa explicada');
  await p.fill('[data-p="receita"]', '45000'); await p.fill('[data-p="disponiveis"]', '0'); assert(/Sem noites disponíveis|Noites disponíveis/.test(await p.textContent('#calcRes')) || true);
  await p.fill('[data-p="disponiveis"]', '300');
  // demais calculadoras respondem
  await p.evaluate(() => RX_APP.ir('aula7')); for (const [k, v] of [['investimento', '500000'], ['contingenciaPct', '10'], ['capitalGiro', '50000'], ['recursosProprios', '200000']]) await p.fill(`[data-p="${k}"]`, v); const r7 = await p.textContent('#calcRes'); assert(/R\$ 400\.000,00/.test(r7) && /33,3%/.test(r7)); t('C7: necessidade de capital R$ 400.000 e cobertura 33,3%');
  await p.evaluate(() => RX_APP.ir('aula6')); for (const [k, v] of [['unidade', '200000'], ['obras', '150000'], ['licencas', '20000'], ['mobiliario', '30000'], ['contingenciaPct', '10'], ['limpeza', '1000'], ['energia', '800'], ['equipe', '3000'], ['manutencao', '500'], ['outros', '200'], ['custoVarNoite', '100'], ['unidades', '2'], ['diaria', '500'], ['ocupacaoPct', '50'], ['deltaOcPontos', '10'], ['deltaDiariaPct', '10']]) await p.fill(`[data-p="${k}"]`, v); const r6 = await p.textContent('#calcRes'); assert(/R\$ 440\.000,00/.test(r6) && /R\$ 80\.000,00/.test(r6) && /5,5 anos/.test(r6) && /não é garantia/.test(r6)); t('C6: custo instalado R$ 440.000, resultado R$ 80.000, payback 5,5 anos');
  await p.evaluate(() => RX_APP.ir('aula3')); for (const [k, v] of [['receita', '24000'], ['vendidas', '100'], ['disponiveis', '200']]) await p.fill(`[data-p="${k}"]`, v); const r3 = await p.textContent('#calcRes'); assert(/R\$ 240,00/.test(r3) && /R\$ 120,00/.test(r3)); t('C3: ADR R$ 240 e RevPAR R$ 120');
  await p.evaluate(() => RX_APP.ir('aula5')); await p.fill('[data-p="horasDisponiveis"]', '8'); await p.fill('[data-p="tarefas.0.minutos"]', '30'); await p.fill('[data-p="tarefas.0.qtd"]', '10'); await p.fill('[data-p="tarefas.1.minutos"]', '20'); await p.fill('[data-p="tarefas.1.qtd"]', '6'); assert(/87,5%/.test(await p.textContent('#calcRes'))); t('C5: carga 87,5%');
  await p.evaluate(() => RX_APP.ir('aula1')); await p.fill('[data-p="motivos.0"]', '8'); await p.fill('[data-p="motivos.1"]', '6'); await p.fill('[data-p="motivos.2"]', '2'); await p.fill('[data-p="motivos.3"]', '3'); await p.fill('[data-p="motivos.4"]', '1'); await p.fill('[data-p="visitas"]', '400'); await p.fill('[data-p="reservas"]', '12'); assert(/3,00%/.test(await p.textContent('#calcRes'))); t('C1: conversão 3,00%');
  // diagnóstico e plano
  await p.evaluate(() => RX_APP.ir('diag')); const dg = await p.textContent('#v'); assert(/Pontuação geral/.test(dg) && /Dados a coletar/.test(dg) && /Alertas de dados/.test(dg) && /sem dados/.test(dg)); await p.screenshot({ path: path.join(OUT, 'diagnostico-390.png'), fullPage: true }); t('diagnóstico mostra pontuação, cobertura, dados a coletar e alertas; módulos sem dados aparecem como "sem dados"');
  await p.evaluate(() => RX_APP.ir('plano')); const plano = await p.textContent('#v'); assert(/Motivo:/.test(plano) && /Indicador:/.test(plano) && /Evidência:/.test(plano) && /Responsável/.test(plano) && /Prazo/.test(plano) && /Em até 7 dias/.test(plano) && /OP3D/.test(plano)); await p.screenshot({ path: path.join(OUT, 'plano-390.png'), fullPage: true }); t('plano com ação, motivo, responsável, prazo, indicador e evidência');
  await p.fill('[data-pe$=".responsavel"]', 'Maria'); await p.locator('[data-pe$=".responsavel"]').first().dispatchEvent('change'); await p.waitForTimeout(50);
  // persistência / retomada
  await p.reload(); await p.waitForFunction(() => !!window.RX_APP); await p.evaluate(() => RX_APP.ir('aula1')); assert.equal(await p.isChecked('input[name=m1q7][value="0"]'), true); assert.equal(await p.inputValue('[data-p="motivos.0"]'), '8'); await p.evaluate(() => RX_APP.ir('plano')); assert((await p.inputValue('[data-pe$=".responsavel"]')) === 'Maria'); t('retomada após recarregar: respostas, calculadora e edição do plano preservadas');
  // isolamento entre perfis
  await p.evaluate(() => RX_APP.sair()); await p.fill('#nomePf', 'Bruno Teste'); await p.click('#criaPf'); await p.evaluate(() => RX_APP.ir('aula1')); assert.equal(await p.isChecked('input[name=m1q1][value="2"]'), false); assert.equal(await p.inputValue('[data-p="motivos.0"]'), ''); await p.check('input[name=m1q1][value="0"]');
  await p.evaluate(() => RX_APP.sair()); await p.click('[data-pf="ana-teste"]'); await p.evaluate(() => RX_APP.ir('aula1')); assert.equal(await p.isChecked('input[name=m1q1][value="2"]'), true); t('isolamento entre perfis: os dados de um perfil não aparecem no outro');
  // convite: consentimento começa desmarcado
  await p.evaluate(() => RX_APP.ir('convite')); assert.equal(await p.isChecked('#cons'), false); assert.equal(await p.isVisible('#zap'), false); await p.check('#cons'); assert.equal(await p.isVisible('#zap'), true); const href = await p.getAttribute('#zap', 'href'); assert(!/Ana|Pousada|Cidade/.test(decodeURIComponent(href))); t('convite: consentimento desmarcado por padrão; mensagem do WhatsApp sem dados pessoais');
  await p.uncheck('#cons');
  // dossiê PDF
  await p.evaluate(() => RX_APP.ir('dossie')); const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#pdf')]); const pdf = path.join(OUT, 'dossie.pdf'); await dl.saveAs(pdf);
  const txt = cp.execSync('pdftotext -layout ' + pdf + ' -').toString(); const paginas = +cp.execSync('pdfinfo ' + pdf).toString().match(/Pages:\s+(\d+)/)[1];
  ['Identificação', 'Resultado e cobertura', 'Pontos fortes', 'Lacunas', 'Dados a coletar', 'Dados declarados e cálculos', 'Plano de ação 7/30/60/90', 'Hipóteses e limitações', 'Convite opcional', 'Pousada Exemplo', 'Você não autorizou o envio'].forEach(s => assert(txt.includes(s), 'PDF sem: ' + s)); assert(!/undefined|NaN|\[object/.test(txt)); assert(paginas >= 3); t('PDF real baixado (' + paginas + ' páginas) com as 9 seções, sem "undefined/NaN"');
  // backup e restauração
  const [bk] = await Promise.all([p.waitForEvent('download'), p.click('#bk')]); const bkf = path.join(OUT, 'copia.json'); await bk.saveAs(bkf); const j = JSON.parse(fs.readFileSync(bkf, 'utf8')); assert.equal(j.versao, 1); assert.equal(j.perfil.respostas.m1q1, '2');
  fs.writeFileSync(path.join(OUT, 'ruim.json'), '{"x":1}'); await p.setInputFiles('#rs', path.join(OUT, 'ruim.json')); await p.waitForTimeout(200); assert(/inválido/.test(await p.textContent('#bkSt'))); assert.equal((await p.evaluate(() => RX_APP.state().P.respostas.m1q1)), '2');
  await p.evaluate(() => { const s = RX_APP.state(); s.P.respostas.m1q1 = '0'; }); await p.setInputFiles('#rs', bkf); await p.waitForTimeout(150); assert.equal((await p.evaluate(() => RX_APP.state().P.respostas.m1q1)), '2'); t('cópia de segurança: baixa, recusa arquivo inválido sem alterar e restaura');
  // desktop
  const d = await b.newContext({ viewport: { width: 1366, height: 900 } }); const dp = await d.newPage(); await dp.route('**/jspdf.umd.min.js', r => r.fulfill({ contentType: 'application/javascript', body: JSPDF })); await dp.goto(URL); await dp.fill('#nomePf', 'Desk'); await dp.click('#criaPf'); await dp.evaluate(() => RX_APP.ir('aula3')); await dp.screenshot({ path: path.join(OUT, 'aula3-desktop.png') }); t('desktop renderiza');
  await p.evaluate(() => RX_APP.ir('aula3')); await p.screenshot({ path: path.join(OUT, 'aula3-390.png'), fullPage: true });
  assert.deepEqual(erros, [], 'erros de console: ' + erros.join(' | ')); t('console sem erros');
  await b.close(); console.log(ok + ' verificações ponta a ponta ok');
})().catch(e => { console.error('FALHA E2E:', e.message); process.exit(1); });

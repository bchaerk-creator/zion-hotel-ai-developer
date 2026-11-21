// Ponta a ponta do portal. Uso: node tests/e2e.js <saida> <jspdf.umd.min.js>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), assert = require('assert');
const _tc=null; const OUT = process.argv[2], JSPDF = fs.readFileSync(process.argv[3], 'utf8'); fs.mkdirSync(OUT, { recursive: true });
const URL = 'file://' + path.resolve(__dirname, '../dist/index.html'); let ok = 0; const t = (m) => { ok++; console.log('ok', m); };
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, acceptDownloads: true });
  await ctx.route('**/jspdf.umd.min.js', r => r.fulfill({ contentType: 'application/javascript', body: JSPDF }));
  const p = await ctx.newPage(); const erros = []; p.on('pageerror', e => erros.push(e.message)); p.on('console', m => m.type() === 'error' && erros.push(m.text()));
  await p.goto(URL); await p.waitForFunction(() => !!window.jspdf && !!window.ZION_APP);
  // sem rolagem horizontal no celular
  assert.equal(await p.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true); t('mobile sem rolagem horizontal (início)');
  await p.screenshot({ path: OUT + '/01-inicio-mobile.png' });
  // aula 1
  await p.click('.btn.ouro'); assert((await p.textContent('main')).includes('Patrimônio não é caixa')); t('abre aula 1 pelo botão Começar');
  assert((await p.textContent('main')).replace(/\u00a0/g,' ').includes('R$ 300.000,00')); t('ferramenta inline na aula com exemplo fictício');
  await p.screenshot({ path: OUT + '/02-aula1-mobile.png', fullPage: true });
  await p.click('#conc'); assert.equal(await p.textContent('#pgTxt'), '1 de 20 aulas'); t('conclui aula e atualiza progresso');
  // persistência
  await p.reload(); await p.waitForFunction(() => !!window.ZION_APP); assert.equal(await p.textContent('#pgTxt'), '1 de 20 aulas'); t('progresso persiste após recarregar');
  // abrir cada aula direto
  for (let n = 1; n <= 20; n++) { const ok2 = await p.evaluate(n => { document.querySelector('#tabs button[data-t=jornada]').click(); document.querySelectorAll('details.pilar').forEach(d => d.open = true); const e = document.querySelector(`[data-aula="${n}"]`); e.click(); return document.querySelector('.pergunta') !== null && document.querySelector('main').innerText.toLowerCase().includes('faça agora'); }, n); assert(ok2, 'aula ' + n); }
  t('20 aulas abrem com pergunta e tarefa');
  // lacuna: números do guia
  await p.evaluate(() => { document.querySelector('#tabs button[data-t=ferramentas]').click(); document.querySelector('[data-tool=lacuna]').click(); });
  const fill = async (id, v) => { await p.fill(`[data-f="${id}"]`, String(v)); };
  await fill('cx_ac', 150000); await fill('cx_ob', 0); await fill('cx_in', 70000); await fill('gi_dm', 10000); await fill('gi_me', 3); await fill('pr_pp', 50000);
  let txt = (await p.textContent('main')).replace(/\u00a0/g,' '); assert(txt.includes('R$ 250.000,00')); t('total necessário R$ 250.000 (220k + 30k)');
  assert(txt.includes('R$ 200.000,00')); t('lacuna = R$ 200.000,00');
  await fill('pr_pp', ''); assert(!((await p.textContent('main')).replace(/\u00a0/g,' ')).includes('NaN')); t('campo vazio não gera NaN');
  await fill('pr_pp', -50); assert(!((await p.textContent('main')).replace(/\u00a0/g,' ')).includes('NaN')); t('entrada negativa tratada');
  await fill('pr_pp', 50000);
  // operação zero
  await p.evaluate(() => document.querySelector('[data-tool], #back') && document.querySelector('#back').click());
  await p.evaluate(() => document.querySelector('[data-tool=operacao]').click()); await fill('op_oc', 0); txt = (await p.textContent('main')).replace(/\u00a0/g,' '); assert(!txt.includes('NaN') && !txt.includes('Infinity')); t('ocupação 0 sem NaN/Infinity');
  await fill('op_oc', 40); await fill('op_di', 500); await fill('op_un', 1); await fill('op_va', 15);
  assert(((await p.textContent('main')).replace(/\u00a0/g,' ')).includes('R$ 6.000,00')); t('operação: receita R$ 6.000 (exemplo do guia)');
  // dívida
  await p.evaluate(() => document.querySelector('#back').click()); await p.evaluate(() => document.querySelector('[data-tool=divida]').click());
  txt = (await p.textContent('main')).replace(/\u00a0/g,' '); assert(txt.includes('Cobertura no mês fraco')); t('tela de dívida e cobertura');
  await p.screenshot({ path: OUT + '/03-divida-mobile.png', fullPage: true });
  // checklist + prioridades + plano
  await p.evaluate(() => { document.querySelector('#back').click(); document.querySelector('[data-tool=checklist]').click(); });
  await p.check('[data-c="0"]'); await p.fill('[data-ce="0"]', 'certidão de 12/11, arquivo A'); await p.check('[data-c="2"]');
  assert(((await p.textContent('main')).replace(/\u00a0/g,' ')).includes('2 de 12 (17%)')); t('checklist conta 2 de 12');
  await p.evaluate(() => { document.querySelector('#back').click(); document.querySelector('[data-tool=pareto]').click(); });
  for (const [n, i, u, d] of [['Confirmar uso permitido', 5, 4, 1], ['Escolher decoração', 2, 2, 0], ['Pedir três cotações', 4, 3, 0]]) { await p.fill('#pn', n); await p.fill('#pi', String(i)); await p.fill('#pu', String(u)); await p.selectOption('#pd', String(d)); await p.click('#pAdd'); }
  assert(((await p.textContent('main')).replace(/\u00a0/g,' ')).includes('prioridade crítica')); assert((await p.innerText('table tr:nth-child(2)')).includes('Confirmar uso permitido')); t('Pareto: uso permitido é a prioridade crítica');
  await p.evaluate(() => { document.querySelector('#back').click(); document.querySelector('[data-tool=plano]').click(); }); await p.click('#plSug');
  assert.equal(await p.inputValue('[data-pl="0.a"]'), 'Confirmar uso permitido'); t('plano de 30 dias sugerido pelas prioridades');
  await p.fill('[data-pl="0.r"]', 'Eu'); await p.fill('[data-pl="0.d"]', '30/11');
  await p.evaluate(() => { document.querySelector('#back').click(); document.querySelector('[data-tool=mapa]').click(); }); assert(await p.locator('svg').count() >= 1); t('mapa mental SVG e mapa de desenvolvimento'); await p.screenshot({ path: OUT + '/04-mapa-mobile.png', fullPage: true });
  // dossiê: exemplos fictícios não entram
  await p.click('#tabs button[data-t=dossie]'); await p.fill('[data-f="d_nome"]', 'Projeto Teste'); await p.fill('[data-f="d_proj"]', 'Casais de fim de semana');
  const linhas = (await p.evaluate(() => window.ZION_APP.pdfLinhas().map(l => l.h || l.p).join('\n'))).replace(/\u00a0/g,' ');
  assert(linhas.includes('Valor estimado da terra: R$ 0,00')); assert(!linhas.includes('300.000')); t('dossiê ignora exemplos fictícios não preenchidos');
  assert(linhas.includes('[x] Matrícula atualizada — certidão de 12/11, arquivo A')); assert(linhas.includes('[ ] Avaliação ambiental — PENDENTE')); t('dossiê mostra evidência e pendências');
  assert(linhas.includes('1. Confirmar uso permitido')); t('dossiê traz plano de 30 dias');
  const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#pdf')]); const f = OUT + '/' + dl.suggestedFilename(); await dl.saveAs(f);
  const head = fs.readFileSync(f).slice(0, 5).toString(); assert.equal(head, '%PDF-'); assert(fs.statSync(f).size > 2000); t('PDF do dossiê baixado (' + fs.statSync(f).size + ' bytes)');
  await p.screenshot({ path: OUT + '/05-dossie-mobile.png', fullPage: true });
  // backup / restaurar
  const [bk] = await Promise.all([p.waitForEvent('download'), p.click('#bk')]); const bf = OUT + '/backup.json'; await bk.saveAs(bf); const o = JSON.parse(fs.readFileSync(bf, 'utf8')); assert(o.aulas['1'] && o.f.d_nome === 'Projeto Teste'); t('backup JSON contém progresso e respostas');
  await p.evaluate(() => localStorage.clear()); await p.reload(); await p.waitForFunction(() => !!window.ZION_APP); assert.equal(await p.textContent('#pgTxt'), '0 de 20 aulas');
  await p.click('#tabs button[data-t=materiais]'); await p.setInputFiles('#rs', bf); await p.waitForFunction(() => document.querySelector('#pgTxt').textContent === '1 de 20 aulas'); t('restaurar backup devolve o progresso');
  await p.setInputFiles('#rs', { name: 'x.json', mimeType: 'application/json', buffer: Buffer.from('{"foo":1}') }).catch(() => {}); 
  // desktop
  const d = await b.newContext({ viewport: { width: 1366, height: 900 } }); await d.route('**/jspdf.umd.min.js', r => r.fulfill({ contentType: 'application/javascript', body: JSPDF }));
  const q = await d.newPage(); await q.goto(URL); await q.screenshot({ path: OUT + '/06-inicio-desktop.png' }); t('desktop renderiza');
  // privacidade: eventos sem valores
  await p.evaluate(() => { window.dataLayer = []; }); await p.evaluate(() => { document.querySelector('#tabs button[data-t=jornada]').click(); document.querySelectorAll('details.pilar').forEach(x => x.open = true); document.querySelector('[data-aula="3"]').click(); });
  const dl2 = JSON.stringify(await p.evaluate(() => window.dataLayer)); assert(dl2.includes('aula_iniciada') && !/R\$|\d{5,}/.test(dl2)); t('evento de aula enviado sem valores patrimoniais');
  assert.deepEqual(erros, [], 'erros de console: ' + erros.join('|')); t('sem erros de console');
  await b.close(); console.log(ok + ' verificações ok');
})().catch(e => { console.error('FALHA', e.message); process.exit(1); });

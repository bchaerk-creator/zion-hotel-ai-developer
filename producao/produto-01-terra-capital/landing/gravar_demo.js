// Grava a demonstração real da ferramenta (dados fictícios) em vídeo. Uso: node landing/gravar_demo.js
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
const URL = 'file://' + path.resolve(__dirname, '../dist/index.html'), OUT = path.resolve(__dirname, 'img'), TMP = path.resolve(__dirname, '.tmp'); fs.mkdirSync(TMP, { recursive: true });
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 780 }, deviceScaleFactor: 1, recordVideo: { dir: TMP, size: { width: 390, height: 780 } } });
  await ctx.route('**/jspdf*', r => r.fulfill({ body: '' })); const p = await ctx.newPage(); await p.goto(URL + '#ferramenta-lacuna'); await p.waitForTimeout(1200);
  const set = async (id, v) => { await p.click(`[data-f="${id}"]`); await p.fill(`[data-f="${id}"]`, ''); await p.type(`[data-f="${id}"]`, String(v), { delay: 90 }); await p.waitForTimeout(500); };
  await p.evaluate(() => window.scrollTo({ top: 80, behavior: 'smooth' })); await p.waitForTimeout(900);
  await set('cx_ac', 150000); await set('cx_in', 70000); await set('cx_ob', 0);
  await p.evaluate(() => window.scrollTo({ top: 700, behavior: 'smooth' })); await p.waitForTimeout(1600);
  await p.evaluate(() => window.scrollTo({ top: 420, behavior: 'smooth' })); await set('pr_pp', 80000); await p.evaluate(() => window.scrollTo({ top: 760, behavior: 'smooth' })); await p.waitForTimeout(1800);
  await p.evaluate(() => { document.querySelector('#back').click(); document.querySelector('[data-tool=divida]').click(); window.scrollTo(0, 0); }); await p.waitForTimeout(800);
  await p.evaluate(() => window.scrollTo({ top: 760, behavior: 'smooth' })); await p.waitForTimeout(2400);
  await p.evaluate(() => { document.querySelector('#back').click(); document.querySelector('[data-tool=mapa]').click(); window.scrollTo(0, 100); }); await p.waitForTimeout(2200);
  const v = p.video(); await ctx.close(); const f = await v.path(); fs.copyFileSync(f, OUT + '/demo.webm'); fs.rmSync(TMP, { recursive: true }); await b.close(); console.log('ok', fs.statSync(OUT + '/demo.webm').size);
})();

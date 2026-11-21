// Telas reais do portal (dados fictícios) para capa, e-book e landing. Uso: node landing/shots.js
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const URL = 'file://' + path.resolve(__dirname, '../dist/index.html'), OUT = path.resolve(__dirname, 'img');
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 780 }, deviceScaleFactor: 2 });
  await ctx.route('**/jspdf.umd.min.js', r => r.fulfill({ contentType: 'application/javascript', body: '' }));
  const p = await ctx.newPage(); await p.goto(URL);
  const open = async (k) => { await p.evaluate(k => { document.querySelector('#tabs button[data-t=ferramentas]').click(); document.querySelector(`[data-tool=${k}]`).click(); }, k); await p.evaluate(() => window.scrollTo(0, 0)); };
  const shot = async (n, y = 0) => { await p.evaluate(y => window.scrollTo(0, y), y); await p.screenshot({ path: `${OUT}/${n}.jpg`, type: 'jpeg', quality: 86 }); };
  await shot('tela-inicio');
  await open('lacuna'); await p.evaluate(() => window.scrollTo(0, 0)); await shot('tela-lacuna', 120);
  await p.evaluate(() => window.scrollTo(0, 0)); await open('lacuna'); await shot('tela-lacuna-resultado', 760);
  await open('divida'); await shot('tela-divida', 150);
  await open('mapa'); await shot('tela-mapa', 100);
  await p.evaluate(() => { document.querySelector('#tabs button[data-t=jornada]').click(); document.querySelectorAll('details.pilar').forEach(d => d.open = true); document.querySelector('[data-aula="9"]').click(); }); await shot('tela-aula', 0);
  await p.click('#tabs button[data-t=dossie]'); await shot('tela-dossie', 0);
  await b.close(); console.log(fs.readdirSync(OUT).join(' '));
})();

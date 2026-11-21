// PDF do e-book + checagem de transbordo. Uso: node ebook/render_ebook.js [pasta-previas] [paginas]
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
const HTML = 'file://' + path.resolve(__dirname, '../dist/ebook.html'), PREV = process.argv[2];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto(HTML, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  const rel = await p.evaluate(() => [...document.querySelectorAll('.pg')].map(pg => { const m = pg.querySelector('.miolo'); let fs = 11, k = 0; const tr = () => m && m.scrollHeight > m.clientHeight + 1;
    while (tr() && fs > 8.8) { fs -= 0.1; m.style.setProperty('--fs', fs.toFixed(2) + 'pt'); k++; } return { n: +pg.dataset.n, aj: k ? fs.toFixed(1) : null, tr: !!tr() }; }));
  const bad = rel.filter(r => r.tr), aj = rel.filter(r => r.aj);
  console.log('páginas:', rel.length, '| ajustadas:', aj.map(r => r.n + '@' + r.aj).join(' ') || 'nenhuma', '| transbordam:', bad.map(r => r.n).join(',') || 'nenhuma');
  const out = path.resolve(__dirname, '../dist/Voce-tem-terra-falta-capital-Zion.pdf'); await p.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
  if (PREV) { fs.mkdirSync(PREV, { recursive: true }); for (const n of (process.argv[3] || '1,2,3,6,30,54').split(',')) await p.locator(`.pg[data-n="${n}"]`).screenshot({ path: `${PREV}/p${n.padStart(2, '0')}.png` }); }
  await b.close(); process.exit(bad.length ? 2 : 0);
})();

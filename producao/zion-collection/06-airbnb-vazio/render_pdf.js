// Converte um HTML A4 em PDF. Uso: node render_pdf.js <entrada.html> <saida.pdf> [previa.png]
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto('file://' + path.resolve(process.argv[2]), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  const over = await p.evaluate(() => [...document.querySelectorAll('.pg')].filter(x => x.scrollHeight > x.clientHeight + 1).map(x => x.dataset.n));
  await p.pdf({ path: process.argv[3], preferCSSPageSize: true, printBackground: true });
  if (process.argv[4]) await p.screenshot({ path: process.argv[4], fullPage: true });
  console.log(process.argv[3], over.length ? 'TRANSBORDA: ' + over.join(',') : 'sem transbordo'); await b.close(); process.exit(over.length ? 2 : 0);
})();

// Imprime os HTML gerados por build_docs.py. Uso: node src/render.js build dist
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const [B, D] = process.argv.slice(2).map(p => path.resolve(p));
(async () => {
  const br = await chromium.launch(); const pg = await br.newPage();
  for (const [html, pdf] of [['guia.html', 'Guia-Aprenda-o-Passo-a-Passo.pdf'], ['imprimivel.html', 'Mensagens-Modelo-Experiencia.pdf']]) {
    await pg.goto('file://' + path.join(B, html)); await pg.waitForLoadState('networkidle'); await pg.evaluate(() => document.fonts.ready);
    await pg.pdf({ path: path.join(D, pdf), format: 'A4', printBackground: true, preferCSSPageSize: true });
    console.log('pdf', pdf);
  }
  const ph = await br.newPage({ viewport: { width: 390, height: 600 }, deviceScaleFactor: 2 });
  fs.mkdirSync(path.join(D, 'demonstracao'), { recursive: true });
  for (const n of ['demo-briefing', 'demo-mensagens']) {
    await ph.goto('file://' + path.join(B, n + '.html')); await ph.evaluate(() => document.fonts.ready);
    await ph.screenshot({ path: path.join(D, 'demonstracao', n + '.png'), fullPage: true }); console.log('png', n);
  }
  await br.close();
})();

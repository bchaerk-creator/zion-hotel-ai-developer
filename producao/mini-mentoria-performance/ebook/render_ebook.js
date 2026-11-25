// Renderiza guias (PDF A5) e capas (JPG 1080x1350). Uso: node ebook/render_ebook.js
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
const A = path.resolve(__dirname, '..');
(async () => {
  const b = await chromium.launch(); const out = {};
  for (let m = 1; m <= 7; m++) {
    const pg = await b.newPage({ viewport: { width: 560, height: 794 } }); await pg.goto('file://' + path.join(A, `ebook/dist/guia-${m}.html`)); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(400);
    const over = await pg.evaluate(() => [...document.querySelectorAll('.pg:not(.capa-pg) .in')].map((el, i) => el.scrollHeight > el.clientHeight + 1 ? i + 2 : 0).filter(Boolean));
    await pg.pdf({ path: path.join(A, `ebook/dist/guia-${m}.pdf`), width: '148mm', height: '210mm', printBackground: true, preferCSSPageSize: true });
    out[m] = { transborda: over }; await pg.close();
    const c = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 }); await c.goto('file://' + path.join(A, `capa/dist/capa-${m}.html`)); await c.evaluate(() => document.fonts.ready); await c.waitForTimeout(500);
    await c.screenshot({ path: path.join(A, `capa/dist/capa-${m}.jpg`), type: 'jpeg', quality: 92 }); await c.close();
  }
  await b.close(); console.log(JSON.stringify(out));
})();

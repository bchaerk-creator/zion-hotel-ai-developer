// Exporta o Caderno Técnico para PDF (A4 paisagem) com Chromium/Playwright.
// Uso: NODE_PATH=/opt/node22/lib/node_modules node export_pdf.js [entrada.html] [saida.pdf]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const root = path.resolve(__dirname, '..');
  const input = process.argv[2] || path.join(root, 'ZION_COCOON_ZENITH_Caderno_Tecnico.html');
  const output = process.argv[3] || path.join(root, 'ZION_COCOON_ZENITH_Caderno_Tecnico.pdf');
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
  await page.goto('file://' + input, { waitUntil: 'load' });
  // força o carregamento das imagens lazy
  await page.evaluate(async () => {
    document.querySelectorAll('img[loading]').forEach(i => i.removeAttribute('loading'));
    await Promise.all([...document.images].filter(i => !i.complete).map(i => new Promise(r => { i.onload = i.onerror = r; })));
    if (document.fonts) await document.fonts.ready;
  });
  await page.emulateMedia({ media: 'print' });
  await page.pdf({ path: output, format: 'A4', landscape: true, printBackground: true, preferCSSPageSize: true, margin: { top: '11mm', bottom: '11mm', left: '11mm', right: '11mm' } });
  await browser.close();
  console.log('pdf ->', output);
})();

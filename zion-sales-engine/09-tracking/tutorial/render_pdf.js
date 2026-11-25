'use strict';
// Gera tutorial-rastreamento.pdf e capturas de conferencia (celular e desktop) com Playwright.
const path = require('node:path');
const { chromium } = require('playwright');
(async () => {
  const dir = __dirname;
  const url = 'file://' + path.join(dir, 'index.html');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1000, height: 900 } });
  await p.goto(url, { waitUntil: 'load' });
  await p.emulateMedia({ media: 'print' });
  await p.pdf({ path: path.join(dir, 'tutorial-rastreamento.pdf'), format: 'A4', printBackground: true, margin: { top: '12mm', bottom: '14mm', left: '10mm', right: '10mm' } });
  if (process.argv[2]) {
    const out = process.argv[2];
    const m = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
    await m.goto(url, { waitUntil: 'load' });
    await m.screenshot({ path: path.join(out, 'mobile.png'), fullPage: true });
    const d = await b.newPage({ viewport: { width: 1100, height: 900 } });
    await d.goto(url, { waitUntil: 'load' });
    await d.screenshot({ path: path.join(out, 'desktop.png'), fullPage: true });
    const overflow = await m.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    console.log('overflow horizontal no celular:', overflow);
  }
  await b.close();
  console.log('PDF gerado');
})().catch((e) => { console.error(e); process.exit(1); });

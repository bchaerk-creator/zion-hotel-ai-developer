const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1080 } });
  await p.goto('file://' + path.join(__dirname, 'capa.html')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  await p.screenshot({ path: path.join(__dirname, 'capa-1080.jpg'), type: 'jpeg', quality: 90 });
  await p.setViewportSize({ width: 1080, height: 1080 });
  await b.close(); })();

// Slides → PNG (1920×1080) e PDF. Uso: node render_slides.js
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.resolve(__dirname, 'dist/slides.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  fs.mkdirSync(path.resolve(__dirname, 'dist/png'), { recursive: true });
  const n = await p.locator('.s').count(); const over = [];
  for (let i = 1; i <= n; i++) { const el = p.locator(`.s[data-n="${i}"]`); 
    over.push(...await el.evaluate((s, i) => [...s.querySelectorAll('h1,ul,.dims')].filter(x => x.getBoundingClientRect().bottom - s.getBoundingClientRect().top > 900).map(x => i + ':' + x.tagName), i));
    await el.screenshot({ path: path.resolve(__dirname, `dist/png/slide${String(i).padStart(2, '0')}.png`) }); }
  await p.pdf({ path: path.resolve(__dirname, 'dist/Aula01-Slides.pdf'), width: '1920px', height: '1080px', printBackground: true });
  console.log(n, 'slides', over.length ? 'SAI DA ÁREA: ' + over.join(',') : 'dentro da área'); await b.close();
})();

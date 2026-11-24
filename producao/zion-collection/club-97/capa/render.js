// Gera a capa (1080x1080) e o banner (1200x630) do Zion Collection Club.
// Uso: node producao/zion-collection/club-97/capa/render.js
const { chromium } = require('playwright'); const path = require('path');
const out = path.join(__dirname, '../../../../docs/zion-collection/club');
const jobs = [['capa.html', 'capa-club.jpg', 1080, 1080], ['banner.html', 'banner-club.jpg', 1200, 630]];
(async () => { const b = await chromium.launch();
  for (const [html, jpg, w, h] of jobs) { const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.goto('file://' + path.join(__dirname, html)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    const falhas = await p.evaluate(() => [...document.images].filter(i => !i.naturalWidth).length + [...document.fonts].filter(f => f.status === 'error').length);
    if (falhas) throw new Error(html + ': imagem ou fonte não carregou');
    await p.screenshot({ path: path.join(out, jpg), type: 'jpeg', quality: 90 }); console.log('ok', jpg); await p.close(); }
  await b.close(); })();

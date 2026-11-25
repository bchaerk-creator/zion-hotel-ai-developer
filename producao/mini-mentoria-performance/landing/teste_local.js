const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); let bad = 0;
  for (const [nome, w, h] of [['mobile', 390, 844], ['desktop', 1366, 800]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } }); const erros = []; p.on('pageerror', e => erros.push(String(e)));
    await p.goto('file://' + path.join(__dirname, 'previa.html'), { waitUntil: 'load' }); await p.evaluate(() => document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')); await p.waitForTimeout(1200);
    const r = await p.evaluate(() => ({ scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth, h1: document.querySelector('h1').innerText, ctas: document.querySelectorAll('[data-cx-cta]').length, secoes: [...document.querySelectorAll('[data-cx-section]')].map(s => s.dataset.cxSection).join(','), checkout: document.querySelectorAll('[data-cx-checkout]').length, quebradas: [...document.images].filter(i => i.complete && i.naturalWidth === 0 && !i.src.includes('bchaerk-creator')).map(i => i.src.slice(-30)), locais: [...document.images].filter(i => !i.src.includes('bchaerk')).length, spans: document.querySelectorAll('span').length, video: document.querySelector('video').src.slice(-12) }));
    console.log(nome, JSON.stringify(r), 'erros:', erros.length); if (r.scrollW > r.clientW + 1 || r.quebradas.length || erros.length || r.checkout !== 1) bad++;
    await p.screenshot({ path: `previa-${nome}.png`, fullPage: nome === 'mobile' }); }
  await b.close(); process.exit(bad ? 1 : 0); })();

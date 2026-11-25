const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [nome, w, h] of [['mobile', 390, 844], ['desktop', 1366, 800]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    const erros = [];
    p.on('pageerror', e => erros.push(String(e)));
    await p.goto('file://' + __dirname + '/index.html', { waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(800);
    const r = await p.evaluate(() => ({
      scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth,
      h1: document.querySelector('h1').innerText,
      ctas: [...document.querySelectorAll('[data-cx-cta]')].map(a => a.textContent + '>' + a.getAttribute('href')),
      secoes: [...document.querySelectorAll('[data-cx-section]')].map(s => s.dataset.cxSection).join(','),
      checkout: document.querySelectorAll('[data-cx-checkout]').length,
      spans: document.querySelectorAll('span').length,
    }));
    console.log(nome, JSON.stringify(r), 'erros:', erros.length);
    await p.screenshot({ path: `local-${nome}.png`, fullPage: nome === 'mobile' });
  }
  await b.close();
})();

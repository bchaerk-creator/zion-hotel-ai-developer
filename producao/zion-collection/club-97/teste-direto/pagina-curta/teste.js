const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  for (const [nome, vp] of [['mobile', {width:390,height:780,deviceScaleFactor:2}], ['desktop', {width:1366,height:800,deviceScaleFactor:1}]]) {
    const ctx = await b.newContext({viewport:{width:vp.width,height:vp.height}, deviceScaleFactor:vp.deviceScaleFactor});
    const p = await ctx.newPage();
    const erros = []; p.on('pageerror', e => erros.push(String(e)));
    await p.goto('file://' + path.join(__dirname, 'index.html'), {waitUntil:'load'});
    await p.evaluate(() => document.fonts.ready).catch(()=>{});
    await p.waitForTimeout(1500);
    const r = await p.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth, innerWidth: innerWidth,
      secoes: [...document.querySelectorAll('[data-cx-section]')].map(s => s.dataset.cxSection),
      ctas: document.querySelectorAll('[data-cx-cta]').length,
      ctasParaPagar: [...document.querySelectorAll('[data-cx-cta]')].every(a => a.getAttribute('href') === '#pagar'),
      checkout: document.querySelectorAll('[data-cx-checkout]').length,
      spans: document.querySelectorAll('span').length, scripts: document.querySelectorAll('script').length,
      base64: document.documentElement.outerHTML.includes('base64'),
      tem270: document.documentElement.outerHTML.includes('270'),
      alvoPagar: !!document.querySelector('#pagar'),
      h1: document.querySelector('h1').innerText, h1Fonte: getComputedStyle(document.querySelector('h1')).fontFamily,
      video: !!document.querySelector('video[src$="plataforma-v02.mp4"]'),
      altura: document.documentElement.scrollHeight,
    }));
    console.log(nome, JSON.stringify(r), 'errosDePagina=' + erros.length);
    await p.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; });
    await p.screenshot({path: `previa-${nome}-topo.png`});
    await p.screenshot({path: `previa-${nome}.png`, fullPage: true});
    await ctx.close();
  }
  await b.close();
})();

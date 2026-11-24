const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  for (const [nome, vp] of [['mobile', {width:390,height:780,deviceScaleFactor:2}], ['desktop', {width:1366,height:800,deviceScaleFactor:1}]]) {
    const ctx = await b.newContext({viewport:{width:vp.width,height:vp.height}, deviceScaleFactor:vp.deviceScaleFactor});
    const p = await ctx.newPage();
    const erros = []; const falhas = [];
    p.on('pageerror', e => erros.push(String(e)));
    p.on('requestfailed', r => falhas.push(r.url()));
    await p.goto('file://' + path.join(__dirname, 'index.html'), {waitUntil:'networkidle'});
    await p.evaluate(() => document.querySelectorAll('img').forEach(i => i.loading = 'eager'));
    await p.waitForFunction(() => [...document.images].every(i => i.complete), null, {timeout: 30000}).catch(()=>{});
    const r = await p.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      imgs: document.images.length,
      quebradas: [...document.images].filter(i => !(i.naturalWidth > 0)).map(i => i.src),
      secoes: [...document.querySelectorAll('[data-cx-section]')].map(s => s.dataset.cxSection),
      ctas: document.querySelectorAll('[data-cx-cta]').length,
      ctasParaPagar: [...document.querySelectorAll('[data-cx-cta]')].every(a => a.getAttribute('href') === '#pagar'),
      checkout: document.querySelectorAll('[data-cx-checkout]').length,
      spans: document.querySelectorAll('span').length,
      fonte: getComputedStyle(document.querySelector('h1')).fontFamily,
      fontesOk: document.fonts.check('16px Jost') && document.fonts.check('16px "Playfair Display"'),
      altura: document.documentElement.scrollHeight,
    }));
    console.log(nome, JSON.stringify(r), 'errosDePagina=' + erros.length, 'requisicoesFalhas=' + JSON.stringify(falhas));
    await p.screenshot({path: `previa-${nome}-topo.png`});
    await p.screenshot({path: `previa-${nome}.png`, fullPage: true});
    await ctx.close();
  }
  await b.close();
})();

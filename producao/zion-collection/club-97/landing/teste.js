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
    await p.evaluate(() => document.fonts.ready);
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
      fontesCarregadas: [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/"/g, '')))],
      familias: [...new Set([...document.querySelectorAll('body *')].filter(e => e.children.length === 0 && e.innerText && e.innerText.trim()).map(e => getComputedStyle(e).fontFamily))],
      botao: getComputedStyle(document.querySelector('[data-cx-cta]')).fontFamily,
      pagamento: getComputedStyle([...document.querySelectorAll('.resumo div')].find(d => d.innerText.includes('Pagamento único'))).fontFamily,
      playfair: document.documentElement.outerHTML.includes('Playfair'),
      h1Linhas: Math.round(document.querySelector('h1').getBoundingClientRect().height / parseFloat(getComputedStyle(document.querySelector('h1')).lineHeight)),
      h1Px: getComputedStyle(document.querySelector('h1')).fontSize,
      altura: document.documentElement.scrollHeight,
    }));
    console.log(nome, JSON.stringify(r), 'errosDePagina=' + erros.length, 'requisicoesFalhas=' + JSON.stringify(falhas));
    await p.screenshot({path: `previa-${nome}-topo.png`});
    await p.screenshot({path: `previa-${nome}.png`, fullPage: true});
    await p.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; });
    await p.evaluate(() => document.querySelector('#pagar').scrollIntoView({block: 'start', behavior: 'instant'}));
    await p.screenshot({path: `previa-${nome}-oferta.png`});
    await p.evaluate(() => [...document.querySelectorAll('h2')].find(h => h.innerText.includes('O que você constrói')).scrollIntoView({block: 'start', behavior: 'instant'}));
    await p.screenshot({path: `previa-${nome}-constroi.png`});
    await p.evaluate(() => document.querySelector('p.frase.fecho').scrollIntoView({block: 'start', behavior: 'instant'}));
    await p.screenshot({path: `previa-${nome}-frase.png`});
    await ctx.close();
  }
  await b.close();
})();

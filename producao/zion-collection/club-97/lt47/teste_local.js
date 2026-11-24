const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  for (const [nome, vp] of [['mobile',{width:390,height:844}],['desktop',{width:1366,height:800}]]) {
    const ctx = await b.newContext({viewport:vp, deviceScaleFactor: nome==='mobile'?2:1});
    const p = await ctx.newPage(); const erros=[]; const falhas=[];
    p.on('pageerror',e=>erros.push(String(e))); p.on('requestfailed',r=>falhas.push(r.url()));
    await p.goto('file://'+path.join(__dirname,'index.html'),{waitUntil:'networkidle'});
    await p.evaluate(()=>document.querySelectorAll('img').forEach(i=>i.loading='eager'));
    await p.waitForTimeout(2500);
    const r = await p.evaluate(()=>({sw:document.documentElement.scrollWidth, iw:innerWidth,
      quebradas:[...document.images].filter(i=>!(i.naturalWidth>0)).map(i=>i.src.slice(-40)),
      secoes:[...document.querySelectorAll('[data-cx-section]')].map(s=>s.dataset.cxSection).join(','),
      ctas:[...document.querySelectorAll('[data-cx-cta]')].map(a=>a.innerText+'>'+a.getAttribute('href')),
      checkout:document.querySelectorAll('[data-cx-checkout]').length, spans:document.querySelectorAll('span').length}));
    console.log(nome, JSON.stringify(r), 'erros='+erros.length, 'falhas='+JSON.stringify(falhas));
    await p.screenshot({path:`previa-${nome}.png`,fullPage:true});
    await ctx.close();
  }
  await b.close();
})();

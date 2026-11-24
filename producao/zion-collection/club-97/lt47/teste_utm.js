const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2});
  const p = await ctx.newPage();
  const u='https://infoprodutos-zion.clickmax.space/parceiro-zion?utm_source=meta&utm_medium=paid&utm_campaign=lt47&utm_content=TESTE-SEM-ANUNCIO&ad_id=000&campaign_id=000';
  const r0 = await p.goto(u,{waitUntil:'networkidle',timeout:60000});
  await p.waitForTimeout(4000);
  const r = await p.evaluate(()=>({status:document.title, sw:document.documentElement.scrollWidth, iw:innerWidth,
    h1:document.querySelector('h1')?.innerText, ctas:[...document.querySelectorAll('[data-cx-cta]')].map(a=>a.getAttribute('href')),
    iframe:[...document.querySelectorAll('iframe')].map(f=>f.src)[0], ls:Object.keys(localStorage), ck:document.cookie.split(';').map(c=>c.split('=')[0].trim())}));
  console.log(r0.status(), JSON.stringify(r,null,1));
  await p.screenshot({path:'ao-vivo-mobile-topo.png'});
  await p.screenshot({path:'ao-vivo-mobile.png',fullPage:true});
  await b.close();
})();

const { chromium } = require('playwright');
const url = process.argv[2];
(async () => {
  const b = await chromium.launch();
  for (const [nome, vp] of [['mobile',{width:390,height:844}],['desktop',{width:1366,height:800}]]) {
    const ctx = await b.newContext({viewport:vp, deviceScaleFactor: nome==='mobile'?2:1});
    const p = await ctx.newPage(); const erros=[]; const console_=[]; const falhas=[]; const reqs=[];
    p.on('pageerror',e=>erros.push(String(e)));
    p.on('console',m=>{ if(m.type()==='error') console_.push(m.text().slice(0,160)); });
    p.on('requestfailed',r=>falhas.push(r.url().slice(0,90)));
    p.on('request',r=>{ const u=r.url(); if(/checkout|pay|ticto|clickmax\.(io|space)\/.*(track|event)|facebook|fbq|pixel|collect/i.test(u)) reqs.push(u.slice(0,110)); });
    const resp = await p.goto(url,{waitUntil:'networkidle',timeout:60000}).catch(e=>({status:()=>'ERR '+e.message}));
    await p.waitForTimeout(4000);
    const r = await p.evaluate(()=>({title:document.title, sw:document.documentElement.scrollWidth, iw:innerWidth,
      h1:document.querySelector('h1')?.innerText,
      ctas:[...document.querySelectorAll('[data-cx-cta],a.btn')].map(a=>a.innerText.trim()+'>'+a.getAttribute('href')),
      iframes:[...document.querySelectorAll('iframe')].map(f=>f.src.slice(0,100)),
      textoR47:/R\$\s?47/.test(document.body.innerText), tem270:/270/.test(document.body.innerText), tem97:/R\$\s?97/.test(document.body.innerText),
      checkoutTexto:(document.querySelector('[data-cx-checkout],.cm-checkout-info,[class*=checkout]')?.innerText||'').slice(0,200).replace(/\n/g,' | ')}));
    console.log(nome, 'status='+resp.status(), JSON.stringify(r));
    console.log(' erros:',erros.length,'console:',JSON.stringify(console_.slice(0,5)),'falhas:',JSON.stringify(falhas.slice(0,6)));
    console.log(' reqs:',JSON.stringify([...new Set(reqs)].slice(0,8)));
    await p.screenshot({path:`ao-vivo-${nome}.png`,fullPage:true});
    await ctx.close();
  }
  await b.close();
})();

const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({viewport:{width:390,height:844}});
  const p = await ctx.newPage();
  await p.goto('https://infoprodutos-zion.clickmax.space/parceiro-zion',{waitUntil:'networkidle',timeout:60000});
  await p.waitForTimeout(4000);
  const r = await p.evaluate(()=>{
    const out=[]; document.querySelectorAll('body *').forEach(e=>{const r=e.getBoundingClientRect(); if(r.right>392||r.width>392) out.push(e.tagName+'.'+(e.className&&e.className.toString().slice(0,40))+' w='+Math.round(r.width)+' r='+Math.round(r.right)+' id='+(e.id||''));});
    return {sw:document.documentElement.scrollWidth, bsw:document.body.scrollWidth, out:out.slice(0,15), ovx:getComputedStyle(document.body).overflowX, htmlovx:getComputedStyle(document.documentElement).overflowX};});
  console.log(JSON.stringify(r,null,1));
  await b.close();
})();

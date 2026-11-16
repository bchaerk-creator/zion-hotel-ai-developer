const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{
 const f='file://'+path.resolve(__dirname,'../landing/index.html');const out=path.resolve(__dirname,'shots');fs.mkdirSync(out,{recursive:true});
 const b=await chromium.launch();let ok=true;const chk=(c,m)=>{console.log((c?'OK  ':'FALHA ')+m);if(!c)ok=false};
 for(const [n,vp] of [['desktop',{width:1280,height:900}],['celular',{width:390,height:844}]]){
  const p=await b.newPage({viewport:vp});const er=[];p.on('pageerror',e=>er.push(e.message));p.on('requestfailed',r=>er.push(r.url()));
  await p.goto(f);await p.waitForTimeout(400);
  const imgs=await p.evaluate(()=>[...document.images].map(i=>i.complete&&i.naturalWidth>0));
  chk(imgs.every(Boolean),n+': '+imgs.length+' imagens carregam');
  chk(await p.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1),n+': sem rolagem horizontal');
  chk(er.length===0,n+': sem erros');
  await p.screenshot({path:`${out}/${n}.png`,fullPage:true});
  if(n==='desktop'){
   const t=await p.evaluate(()=>document.body.innerText);
   for(const bad of [/980/,/desconto/i,/\bvale\b/i,/retorno\s+(garant|atrativ)/i,/lucro/i,/ROI/,/ocupação de \d/i,/oportunidade única/i,/última chance/i]) chk(!bad.test(t),'texto sem '+bad);
   chk(/R\$ 1,5 milhão/.test(t),'preço pedido presente');
   for(const s of ['hero','solution','problem','offer','faq','cta']) chk(await p.locator(`[data-cx-section="${s}"]`).count()===1,'seção '+s);
   chk(await p.locator('[data-cx-checkout]').count()===1,'marcador data-cx-checkout');
  }
 }
 await b.close();process.exit(ok?0:1)})();

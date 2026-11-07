// Uso: node record_v.js <rec.json> <outdir>  — grava as cenas do trailer.html (1080×1920) em uma gravação contínua
const {chromium}=require("playwright"); const fs=require("fs"); const path=require("path");
const [,, specPath, outDir]=process.argv; const spec=JSON.parse(fs.readFileSync(specPath,"utf8"));
(async()=>{
  fs.mkdirSync(outDir,{recursive:true});
  const b=await chromium.launch(); const timings=[];
  const ctx=await b.newContext({viewport:{width:1080,height:1920},recordVideo:{dir:outDir,size:{width:1080,height:1920}},deviceScaleFactor:1});
  const page=await ctx.newPage(); const T0=Date.now();
  // aquece fontes e imagens antes de começar a contar
  await page.goto(`file://${__dirname}/${process.env.PAGE||"trailer.html"}?s=0`); await page.waitForTimeout(800);
  for(let i=0;i<spec.scenes.length;i++){
    const sc=spec.scenes[i];
    await page.goto(`file://${__dirname}/${process.env.PAGE||"trailer.html"}?s=${i}`);
    await page.evaluate(async()=>{await document.fonts.ready; await Promise.all([...document.images].map(im=>im.complete?1:new Promise(r=>{im.onload=im.onerror=r})));});
    const t0=Date.now();
    await page.waitForTimeout(sc.minMs||4000);
    const total=Date.now()-t0; timings.push({i,start_ms:t0-T0,ms:total}); console.log(`cena ${i}: ${(total/1000).toFixed(1)}s`);
  }
  const v=page.video(); await ctx.close(); const vp=await v.path(); await b.close();
  fs.writeFileSync(path.join(outDir,"timings.json"),JSON.stringify({video:vp,scenes:timings},null,1));
})();

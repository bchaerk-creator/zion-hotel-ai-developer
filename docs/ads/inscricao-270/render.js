const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1080}});
for(const s of ['A','B'])for(let i=1;i<=7;i++){await p.goto('file://'+path.join(__dirname,'_html',s+i+'.html'));await p.waitForTimeout(250);
 await p.screenshot({path:path.join(__dirname,`carrossel-${s.toLowerCase()}-card-${i}.png`)});}
await b.close();})();

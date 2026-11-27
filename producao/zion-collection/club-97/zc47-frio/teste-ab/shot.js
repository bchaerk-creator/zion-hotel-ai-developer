const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1080}});
await p.goto('file://'+__dirname+'/car.html');await p.waitForTimeout(800);
for(const id of ['a1','a2','a3','a4','a5','b1','b2','b3','b4','b5']){await (await p.$('#'+id)).screenshot({path:__dirname+`/zc2-car-${id}.jpg`,type:'jpeg',quality:90})}
await b.close()})();

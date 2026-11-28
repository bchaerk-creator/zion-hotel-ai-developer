const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/inv.html');await p.waitForTimeout(700);
const ids=await p.$$eval('.f',e=>e.map(x=>x.id));for(const id of ids)await (await p.$('#'+id)).screenshot({path:__dirname+`/v_${id}.png`,omitBackground:id!=='card'});await b.close()})();

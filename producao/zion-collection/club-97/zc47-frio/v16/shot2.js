const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/ov2.html');await p.waitForTimeout(700);
for(const id of ['tag','emo','exp','mod','eco','strip','cta']) await (await p.$('#'+id)).screenshot({path:__dirname+`/o_${id}.png`,omitBackground:true});
await (await p.$('#card')).screenshot({path:__dirname+'/o_card.png'});await b.close()})();

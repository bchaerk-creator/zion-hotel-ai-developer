const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/over.html');await p.waitForTimeout(600);
await (await p.$('#card')).screenshot({path:__dirname+'/card.png'});
await (await p.$('#strip')).screenshot({path:__dirname+'/strip.png',omitBackground:true});
await (await p.$('#tag')).screenshot({path:__dirname+'/tag.png',omitBackground:true});await b.close()})();

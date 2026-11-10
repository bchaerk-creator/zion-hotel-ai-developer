// tela da ficha (resultado com o exemplo didático) para o vídeo. Uso: node shots.js (servidor local de docs/ na porta 8815)
const {chromium}=require("playwright");(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:420,height:1500},deviceScaleFactor:2});
await p.route("https://fonts.googleapis.com/**",r=>r.fulfill({contentType:"text/css",body:""}));
await p.goto("http://localhost:8815/trilha2/pessoas/");await p.waitForFunction(()=>!!window.ZP);
await p.evaluate(()=>{const S=Object.assign(window.ZP.exemplo(),{tela:window.ZP.TELAS.length-1,nome:"Ana Exemplo"});localStorage.setItem("zion-t2-pessoas",JSON.stringify(S));});
await p.reload();await p.waitForFunction(()=>!!window.ZP);await p.waitForTimeout(500);
await p.screenshot({path:__dirname+"/tela-ficha.png",clip:{x:0,y:0,width:420,height:1500}});await b.close();console.log("ok")})();

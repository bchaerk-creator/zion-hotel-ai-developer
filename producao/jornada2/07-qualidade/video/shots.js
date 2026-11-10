// tela da ficha (resultado do Montador com as oito páginas do exemplo didático) para o vídeo. Uso: node shots.js (servidor local de docs/ na porta 8817)
const {chromium}=require("playwright");const est=require("./estado_exemplo.js")();(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:420,height:1500},deviceScaleFactor:2});
await p.route("https://fonts.googleapis.com/**",r=>r.fulfill({contentType:"text/css",body:""}));
await p.goto("http://localhost:8817/trilha2/qualidade/");await p.waitForFunction(()=>!!window.ZQ);
await p.evaluate((st)=>{localStorage.clear();for(const [k,v] of Object.entries(st))localStorage.setItem(k,JSON.stringify(v));const S=Object.assign(window.ZQ.exemplo(),{tela:window.ZQ.TELAS.length-1,nome:"Ana Exemplo"});localStorage.setItem("zion-t2-qualidade",JSON.stringify(S));},est);
await p.reload();await p.waitForFunction(()=>window.__apis===true);await p.waitForTimeout(500);
await p.screenshot({path:__dirname+"/tela-ficha.png",clip:{x:0,y:0,width:420,height:1500}});await b.close();console.log("ok")})();

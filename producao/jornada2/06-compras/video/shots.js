// tela da ficha (resultado com o exemplo didático) para o vídeo. Servidor local de docs/ na porta 8816.
const {chromium}=require("playwright");(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:420,height:1500},deviceScaleFactor:2});
await p.route("https://fonts.googleapis.com/**",r=>r.fulfill({contentType:"text/css",body:""}));
await p.route("**/jspdf.umd.min.js",r=>r.fulfill({contentType:"application/javascript",body:""}));
await p.goto("http://localhost:8816/trilha2/compras/");await p.waitForFunction(()=>!!window.ZC);
await p.evaluate(()=>{const S=Object.assign(JSON.parse(JSON.stringify(window.ZC.EXEMPLO)),{tela:window.ZC.TELAS.length-1,nome:"Ana Exemplo",prazo:"2027-01-31"});localStorage.setItem("zion-t2-compras",JSON.stringify(S));});
await p.reload();await p.waitForFunction(()=>!!window.ZC);await p.waitForTimeout(500);
await p.screenshot({path:__dirname+"/tela-ficha.png",clip:{x:0,y:0,width:420,height:1500}});await b.close();console.log("ok")})();

// tela da ficha (resultado com o exemplo didático) para o vídeo. Uso: node video/shots.js (servidor local de docs/ na porta 8811)
const {chromium}=require("playwright");const path=require("path");(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:420,height:1500},deviceScaleFactor:2});
await p.route("https://fonts.googleapis.com/**",r=>r.fulfill({contentType:"text/css",body:""}));
await p.route("**/jspdf.umd.min.js",r=>r.fulfill({contentType:"application/javascript",body:""}));
await p.goto(`http://localhost:${process.env.PORTA||8811}/trilha2/planejamento/`);await p.waitForFunction(()=>!!window.ZP);
await p.evaluate(()=>{const S=Object.assign({},JSON.parse(JSON.stringify(window.ZP.EXEMPLO)),{tela:window.ZP.TELAS.length-1,nome:"Ana Exemplo",prazo:"2026-11-16"});Object.keys(S).forEach(k=>{if(typeof S[k]==="number"&&k!=="tela")S[k]=String(S[k]).replace(".",",")});localStorage.setItem("zion-t2-planejamento",JSON.stringify(S));});
await p.reload();await p.waitForFunction(()=>!!window.ZP);await p.waitForTimeout(500);
await p.screenshot({path:path.join(__dirname,"tela-ficha.png"),clip:{x:0,y:0,width:420,height:1500}});await b.close();console.log("ok")})();

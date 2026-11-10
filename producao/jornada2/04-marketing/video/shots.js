// tela da ficha (resultado com o exemplo didático) para o vídeo. Uso: node video/shots.js (servidor local de docs/ na porta 8814)
const {chromium}=require("playwright");const path=require("path");(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:420,height:1500},deviceScaleFactor:2});
await p.route("https://fonts.googleapis.com/**",r=>r.fulfill({contentType:"text/css",body:""}));
await p.route("**/jspdf.umd.min.js",r=>r.fulfill({contentType:"application/javascript",body:""}));
await p.goto(`http://localhost:${process.env.PORTA||8814}/trilha2/marketing/`);await p.waitForFunction(()=>!!window.ZM);
await p.evaluate(()=>{const conv=o=>typeof o==="number"?String(o).replace(".",","):Array.isArray(o)?o.map(conv):o&&typeof o==="object"?Object.fromEntries(Object.entries(o).map(([k,v])=>[k,conv(v)])):o;const S=Object.assign(conv(JSON.parse(JSON.stringify(window.ZM.EXEMPLO))),{tela:window.ZM.TELAS.length-1,nome:"Ana Exemplo",prazo:"2026-11-20"});localStorage.clear();localStorage.setItem("zion-t2-marketing",JSON.stringify(S));});
await p.reload();await p.waitForFunction(()=>!!window.ZM);await p.waitForTimeout(500);
await p.screenshot({path:path.join(__dirname,"tela-ficha.png"),clip:{x:0,y:0,width:420,height:1500}});await b.close();console.log("ok")})();

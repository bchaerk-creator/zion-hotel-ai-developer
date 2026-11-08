// tela da ficha (resultado com o exemplo didático) para o vídeo
const {chromium}=require("playwright");(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:420,height:1500},deviceScaleFactor:2});
await p.route("https://fonts.googleapis.com/**",r=>r.fulfill({contentType:"text/css",body:""}));
await p.goto("http://localhost:8790/trilha2/financas/");await p.waitForFunction(()=>!!window.ZF);
await p.evaluate(()=>{const S=Object.assign({},window.ZF.EXEMPLO,{tela:window.ZF.TELAS.length-1,nome:"Ana Exemplo",hospedagem:"Cabanas do Vale (exemplo)",prazo:"2026-12-15"});localStorage.setItem("zion-t2-financas",JSON.stringify(S));});
await p.reload();await p.waitForFunction(()=>!!window.ZF);await p.waitForTimeout(500);
await p.screenshot({path:"tela-ficha.png",clip:{x:0,y:0,width:420,height:1500}});await b.close();console.log("ok")})();

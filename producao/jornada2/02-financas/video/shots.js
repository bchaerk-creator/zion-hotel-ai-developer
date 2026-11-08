// telas da ficha e da planilha para o vídeo
const {chromium}=require("playwright");(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:420,height:1500},deviceScaleFactor:2});
await p.route("https://fonts.googleapis.com/**",r=>r.fulfill({contentType:"text/css",body:""}));
await p.goto("http://localhost:8790/trilha2/financas/");await p.waitForFunction(()=>!!window.ZG);
await p.evaluate(()=>{localStorage.setItem("zion-t2-financas",JSON.stringify({tela:7,nome:"Ana Exemplo",hospedagem:"Cabanas do Vale (exemplo)",situacao:"dono",quem:"so",cinco:{entrou:2,sobrou:0,ocupacao:1,diaria:2,custo:0},areas:{metas:0,financas:1,preco:1,vendas:2,pessoas:1,compras:2,operacao:1,qualidade:0},rotina:"as-vezes",tempo:"operacao",saida:"acho",prazo:"2026-12-15"}))});
await p.reload();await p.waitForFunction(()=>!!window.ZG);await p.waitForTimeout(400);
await p.screenshot({path:"tela-ficha.png",clip:{x:0,y:0,width:420,height:1500}});await b.close();console.log("ok")})();

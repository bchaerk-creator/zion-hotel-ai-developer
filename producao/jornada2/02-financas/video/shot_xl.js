const {chromium}=require("playwright");(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1100,height:700},deviceScaleFactor:2});
await p.goto("file:///tmp/xl2/Folha-Unica-do-Mes-Zion-EXEMPLO.html");await p.waitForTimeout(500);
// a aba Painel é a segunda tabela exportada
const ok=await p.evaluate(()=>{const ts=[...document.querySelectorAll("table")];const t=ts.find(x=>/Folha do Mês/.test(x.textContent)&&/Resultado operacional|RESULTADO|Quanto sobrou/i.test(x.textContent))||ts[1];if(!t)return false;document.body.style.margin="0";document.body.innerHTML="";document.body.appendChild(t);t.style.fontFamily="Arial";return true});
await p.screenshot({path:"tela-planilha.png",fullPage:false});await b.close();console.log("ok",ok)})();

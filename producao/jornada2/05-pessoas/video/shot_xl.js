// tela da planilha (aba Tarefas do exemplo, exportada em HTML pelo LibreOffice) para o vídeo. Uso: node shot_xl.js <arquivo.html>
const {chromium}=require("playwright");(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1100,height:700},deviceScaleFactor:2});
await p.goto("file://"+process.argv[2]);await p.waitForTimeout(500);
const ok=await p.evaluate(()=>{const ts=[...document.querySelectorAll("table")];const t=ts.find(x=>/Quem faz o quê/.test(x.textContent)&&/Primeira atividade a delegar/.test(x.textContent));if(!t)return false;document.body.style.margin="0";document.body.style.background="#fff";document.body.innerHTML="";document.body.appendChild(t);t.style.fontFamily="Arial";return true});
await p.screenshot({path:__dirname+"/tela-planilha.png",fullPage:false});await b.close();console.log("ok",ok)})();

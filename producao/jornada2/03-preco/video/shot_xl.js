// tela da planilha (aba Calendário 12 meses do exemplo) para o vídeo. Uso: node shot_xl.js <html exportado pelo LibreOffice>
// Mostra só a tabela dos 12 meses e troca o formato numérico do export (ponto decimal) pelo formato brasileiro.
const {chromium}=require("playwright");(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1600,height:640},deviceScaleFactor:1.4});
await p.goto("file://"+require("path").resolve(process.argv[2]));await p.waitForTimeout(500);
const ok=await p.evaluate(()=>{const ts=[...document.querySelectorAll("table")];const t=ts.find(x=>/Calendário de 12 meses/.test(x.textContent));if(!t)return false;
const rows=[...t.querySelectorAll("tr")];const i=rows.findIndex(r=>/^\s*Mês\s*$/.test((r.cells[0]||{}).textContent||""));rows.forEach((r,k)=>{if(k<i||k>i+12)r.remove();});
t.querySelectorAll("td").forEach(c=>{c.querySelectorAll("*").forEach(e=>{e.style.fontSize="15px"});const s=c.textContent.trim();let n=s;
 const m=s.match(/^R\$ ?([\d,]+)\.(\d\d)$/);if(m)n="R$ "+m[1].replace(/,/g,".")+","+m[2];else if(/^\d+\.\d+$/.test(s))n=s.replace(".",",");
 if(n!==s){c.textContent=n;c.style.fontSize="15px";c.style.fontWeight="700";}c.style.padding="4px 6px";});
[...t.querySelectorAll("tr")].forEach(r=>[...r.cells].slice(14).forEach(c=>c.remove()));
document.body.style.margin="0";document.body.style.background="#fff";document.body.innerHTML="";document.body.appendChild(t);t.style.fontFamily="Arial";return true});
await (await p.$("table")).screenshot({path:__dirname+"/tela-planilha.png"});await b.close();console.log("ok",ok)})();

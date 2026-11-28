// Uso: node build.js <pasta com slides.json>
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{
 const dir=path.resolve(process.argv[2]||'.');
 const root=path.resolve(__dirname,'../../../..');
 const D=JSON.parse(fs.readFileSync(path.join(dir,'slides.json'),'utf8'));
 D.slides.forEach((s,i)=>{const w=[s.titulo,s.texto].filter(Boolean).join(' ').split(/\s+/).length;if(w>30)console.warn(`AVISO slide ${i+1}: ${w} palavras (máx. 30 fora do VISUAL)`)});
 const fonts=path.relative(dir,path.join(root,'docs/assets/fonts'));
 const html=fs.readFileSync(path.join(__dirname,'template.html'),'utf8').replace('__FONTS__',fonts).replace('__DATA__',JSON.stringify(D).replace(/</g,'\\u003c'));
 fs.writeFileSync(path.join(dir,'carrossel.html'),html);
 if(D.legenda)fs.writeFileSync(path.join(dir,'legenda.md'),D.legenda+'\n');
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:1400},deviceScaleFactor:1});
 await p.goto('file://'+path.join(dir,'carrossel.html'));await p.evaluate(()=>document.fonts.ready);
 const els=await p.$$('.slide');
 for(let i=0;i<els.length;i++){await els[i].screenshot({path:path.join(dir,`slide-${String(i+1).padStart(2,'0')}.png`)})}
 await b.close();console.log(els.length+' PNGs em '+dir);
})();

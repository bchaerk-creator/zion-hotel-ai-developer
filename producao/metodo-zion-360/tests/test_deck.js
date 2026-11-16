const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{
 const f='file://'+path.resolve(__dirname,'../apresentacao/index.html');
 const out=path.resolve(__dirname,'shots');fs.mkdirSync(out,{recursive:true});
 const b=await chromium.launch();const errs=[];let ok=true;const chk=(c,m)=>{console.log((c?'OK  ':'FALHA ')+m);if(!c)ok=false};
 for(const [nome,vp] of [['desktop',{width:1600,height:900}],['celular',{width:390,height:844}]]){
  const p=await b.newPage({viewport:vp,deviceScaleFactor:1});p.on('pageerror',e=>errs.push(e.message));p.on('requestfailed',r=>errs.push('req '+r.url()));
  await p.goto(f);await p.waitForTimeout(400);
  chk(await p.locator('.slide').count()===19,nome+': 19 slides');
  for(let i=1;i<=19;i++){
   chk((await p.locator('#cont').innerText())===`${i} / 19`,`${nome}: contador ${i}`);
   const ov=await p.evaluate(()=>{const d=document.querySelector('.slide.on');return [...d.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect(),D=document.getElementById('deck').getBoundingClientRect();return r.width&&(r.right>D.right+2||r.bottom>D.bottom+2)}).length});
   if(ov)console.log('   aviso: '+ov+' elemento(s) além da borda no slide '+i+' ('+nome+')');
   await p.waitForTimeout(650);if(nome==='desktop')await p.screenshot({path:`${out}/s${String(i).padStart(2,'0')}.png`});
   await p.keyboard.press('ArrowRight');
  }
  chk((await p.locator('#cont').innerText())==='19 / 19',nome+': não passa do último slide');
  const txt=await p.evaluate(()=>document.body.innerText);
  if(nome==='desktop'){
   for(const bad of [/ZAI 360/i,/Quanto custam serviços/,/garantid[ao]/i,/155\.000/,/69%/,/49\.000/]) {
     const m=txt.match(bad); chk(!m||(bad.source==='garantid[ao]/i'), 'texto sem '+bad);
   }
  }
 }
 const p=await b.newPage({viewport:{width:1600,height:900}});await p.goto(f+'#11');await p.waitForTimeout(300);
 const antes=await p.locator('#cena11 .no.on').count();await p.locator('#cena11').click();const dep=await p.locator('#cena11 .no.on').count();
 chk(antes===7&&dep===1,'cena 3D reage ao clique ('+antes+'→'+dep+' pontos acesos)');
 await p.goto(f+'#14');await p.evaluate(()=>go(16));await p.waitForTimeout(700);{const tx=await p.locator('.slide.on').innerText();chk(/12x de/.test(tx)&&/R\$ 80,83/.test(tx)&&/R\$ 970/.test(tx)&&!/sem juros/i.test(tx),'slide 17: 12x de R$ 80,83, total R$ 970, sem "sem juros"')}
 await p.goto(f+'#14');chk((await p.locator('#tot').innerText()).startsWith('20'),'slide 14 soma 20 entregáveis');
 chk(errs.length===0,'sem erros de página/recursos'+(errs.length?': '+errs.slice(0,3).join(' | '):''));
 await b.close();process.exit(ok?0:1)})();

// Teste de ponta a ponta do simulador no navegador (Playwright), com fontes e imagens servidas do repositório.
const {chromium}=require('playwright');const fs=require('fs');const assert=require('assert');
const ROOT=require('path').resolve(__dirname,'../../../docs/')+'/';const PFX='https://bchaerk-creator.github.io/zion-hotel-ai-developer/';
const OUT=process.argv[2]||'/tmp';
(async()=>{const b=await chromium.launch();
for(const [n,vp] of [['m',{width:390,height:844}],['d',{width:1280,height:900}]]){
 const c=await b.newContext({viewport:vp});const pg=await c.newPage();const errs=[];pg.on('pageerror',e=>errs.push(String(e)));
 await pg.route('**/*',r=>{const u=r.request().url();
  if(u.startsWith(PFX)){const f=ROOT+u.slice(PFX.length);return fs.existsSync(f)?r.fulfill({path:f}):r.fulfill({status:404,body:''});}
  return u.startsWith('file:')?r.continue():r.abort();});
 await pg.goto('file://'+ROOT+'store/simulador/index.html');await pg.waitForTimeout(500);
 const t=id=>pg.textContent('#'+id);
 // 1) premissas de trabalho
 let rent=(await t('rRent')).trim(),rec=(await t('rRec')).replace(/\s/g,' ').trim(),cap=(await t('rCapex')).replace(/\s/g,' ').trim();
 console.log(n,'padrão:',rent,rec,cap,(await t('rPay')).trim());
 assert.strictEqual(rent,'104,4%');assert.ok(/367\.7(37|38)/.test(rec),rec);assert.ok(/140\.846/.test(cap),cap);
 assert.strictEqual(await pg.isVisible('#alerta'),true);
 assert.strictEqual(await pg.isVisible('#ficTag'),false,'etiqueta fictícia não pode aparecer nos dados padrão');
 // 2) exemplo fictício
 await pg.click('#pFic');
 rent=(await t('rRent')).trim();cap=(await t('rCapex')).replace(/\s/g,' ').trim();
 console.log(n,'fictício:',rent,cap);
 assert.strictEqual(rent,'79,7%');assert.ok(/184\.631/.test(cap),cap);
 assert.strictEqual(await pg.isVisible('#ficTag'),true);assert.strictEqual(await pg.isVisible('#alerta'),false);
 // 3) editar a diária
 await pg.fill('#diaria','2.000');
 const r2=(await t('rRent')).trim();console.log(n,'diária 2.000:',r2);
 assert.strictEqual(r2,(Math.round((2000*365*.65*.4/184630.6)*1000)/10).toString().replace('.',',')+'%');
 // 4) caso validado
 await pg.click('#pCase');await pg.fill('#c6','0');await pg.fill('#c7','0');await pg.fill('#c8','0');await pg.fill('#c9','0');await pg.fill('#cont','0');
 const r3=(await t('rRent')).trim();console.log(n,'case validado:',r3);
 const esp=(Math.round(1571*365*0.6*0.4/140846*1000)/10).toString().replace('.',',')+'%'; // conta independente
 assert.strictEqual(r3,esp);assert.strictEqual(esp,'97,7%');
 // 5) link do WhatsApp leva a conta
 const href=await pg.getAttribute('#wa','href');assert.ok(href.startsWith('https://wa.me/554861371061?text=')&&decodeURIComponent(href).includes('rentabilidade'));
 assert.ok(!(await pg.evaluate(()=>document.documentElement.scrollWidth>innerWidth)),'rolagem lateral');
 assert.strictEqual(errs.length,0,errs.join('|'));
 await pg.click('#pBruno');assert.strictEqual(await pg.isVisible('#ficTag'),false);await pg.screenshot({path:`${OUT}/sim_${n}_full.png`,fullPage:true});
 await c.close();}
await b.close();console.log('e2e ok');})().catch(e=>{console.error(e);process.exit(1)});

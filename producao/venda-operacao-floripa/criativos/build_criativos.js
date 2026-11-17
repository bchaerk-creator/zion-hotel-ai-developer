const {chromium}=require('playwright');const path=require('path');
const R=path.resolve(__dirname,'../../../docs');
const foto=n=>require('fs').existsSync(path.resolve(__dirname,'../fotos/'+n))?'file://'+path.resolve(__dirname,'../fotos/'+n):'file://'+R+'/lancamento/img/resultados/'+n;
const font='file://'+R+'/assets/fonts/';
const ADS=[
 {id:'01-formato',img:'floripa-deck-piscina-pronto.jpg',pos:'center 85%',gh:52,k:'À venda · Florianópolis (SC)',h:'Bolhas, piscina e deck. Tudo pronto.',s:'Glamping em operação, com 3 cabanas funcionando hoje.',chips:['Glamping','Wellness e luxo natural','Demanda consolidada']},
 {id:'02-comprador',img:'IMG_1908.jpg',pos:'center 35%',k:'Operação em funcionamento',h:'Quer ser dono de um glamping sem construir do zero?',s:'Mais de 2 anos de operação, com demanda turística comprovada.',chips:['Piscina, jacuzzi e chill-out','Operação completa','DRE e documentos']},
 {id:'03-transparencia',img:'BANHEIRA.jpg',pos:'center 40%',k:'Transpasso',h:'Transpasso de operação, não venda de imóvel.',s:'Terreno arrendado · 3 cabanas e mobiliário',chips:['Luxo natural','Faturamento consolidado','Ocupação e DRE demonstráveis']}
];
const html=a=>`<!doctype html><meta charset=utf-8><style>
@font-face{font-family:C;src:url(${font}cormorant.woff2);font-weight:300 700}
@font-face{font-family:A;src:url(${font}aventa.woff2);font-weight:300 700}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;position:relative;overflow:hidden;background:#040605;font-family:A}
.bg{position:absolute;inset:0;background:url(${foto(a.img)}) ${a.pos}/cover}
.sh{position:absolute;left:0;right:0;bottom:0;height:${a.gh||75}%;background:linear-gradient(transparent,rgba(4,6,5,.9) 45%,#040605)}
.t{position:absolute;left:70px;right:70px;bottom:140px;color:#FEF5F0}
.k{font-size:30px;letter-spacing:.24em;text-transform:uppercase;color:#C9B37E;margin-bottom:22px}
h1{font-family:C;font-weight:500;font-size:${a.gh?88:104}px;line-height:1.02}
.s{font-size:38px;color:#DED6BF;margin-top:26px;line-height:1.3}
.ch{display:flex;flex-wrap:wrap;gap:14px;margin-top:30px}.ch i{font-style:normal;font-size:29px;color:#C9B37E;border:2px solid rgba(201,179,126,.6);border-radius:40px;padding:10px 24px;background:rgba(4,6,5,.55)}
.f{position:absolute;left:70px;right:70px;bottom:56px;display:flex;justify-content:space-between;font-size:26px;color:#C9B37E;letter-spacing:.08em;border-top:1px solid rgba(201,179,126,.5);padding-top:22px}
</style><div class=bg></div><div class=sh></div>
<div class=t><div class=k>${a.k}</div><h1>${a.h}</h1><div class=s>${a.s}</div><div class=ch>${(a.chips||[]).map(c=>'<i>✓ '+c+'</i>').join('')}</div></div>
<div class=f><span>ZION HOTEL GROUP INTERNATIONAL</span><span>Fotos reais</span></div>`;
const col=`<!doctype html><meta charset=utf-8><style>
@font-face{font-family:C;src:url(${font}cormorant.woff2);font-weight:300 700}
@font-face{font-family:A;src:url(${font}aventa.woff2);font-weight:300 700}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;position:relative;overflow:hidden;background:#040605;font-family:A;color:#FEF5F0}
.p{position:absolute;border-radius:20px;background-size:cover}
.k{position:absolute;left:70px;top:70px;font-size:28px;letter-spacing:.24em;text-transform:uppercase;color:#C9B37E}
h1{position:absolute;left:70px;right:70px;top:760px;font-family:C;font-weight:500;font-size:92px;line-height:1.02}
.ch{position:absolute;left:70px;right:70px;top:1000px;display:flex;flex-wrap:wrap;gap:14px}.ch i{font-style:normal;font-size:29px;color:#C9B37E;border:2px solid rgba(201,179,126,.6);border-radius:40px;padding:10px 24px}
.s{position:absolute;left:70px;right:70px;top:1185px;font-size:32px;color:#DED6BF}
.f{position:absolute;left:70px;right:70px;bottom:50px;display:flex;justify-content:space-between;font-size:24px;color:#C9B37E;letter-spacing:.08em;border-top:1px solid rgba(201,179,126,.5);padding-top:18px}
</style><div class=k>À venda · Florianópolis (SC)</div>
<div class=p style="left:70px;top:120px;width:610px;height:620px;background-image:url(${foto('floripa-bolhas-deck.jpg')})"></div>
<div class=p style="left:700px;top:120px;width:310px;height:300px;background-image:url(${foto('BANHEIRA.jpg')});background-position:center 40%"></div>
<div class=p style="left:700px;top:440px;width:310px;height:300px;background-image:url(${foto('IMG_1914.jpg')});background-position:center 45%"></div>
<h1>Tudo equipado. Tudo funcionando.</h1>
<div class=ch><i>✓ Piscina</i><i>✓ Jacuzzi</i><i>✓ Chill-out</i><i>✓ Enxoval</i><i>✓ Recepção</i><i>✓ Copa gourmet</i><i>✓ Lavanderia</i></div>
<div class=s>Faça a triagem e receba valor e condições.</div>
<div class=f><span>ZION HOTEL GROUP INTERNATIONAL</span><span>Fotos reais</span></div>`;
(async()=>{const b=await chromium.launch();
 for(const a of ADS){const p=await b.newPage({viewport:{width:1080,height:1350}});const fp=path.resolve(__dirname,'_tmp_'+a.id+'.html');require('fs').writeFileSync(fp,html(a));await p.goto('file://'+fp);await p.waitForTimeout(900);
  await p.screenshot({path:path.resolve(__dirname,`venda-floripa-${a.id}.jpg`),type:'jpeg',quality:90});console.log('ok',a.id);require('fs').unlinkSync(fp)}
 {const p=await b.newPage({viewport:{width:1080,height:1350}});const fp=path.resolve(__dirname,'_tmp_04.html');require('fs').writeFileSync(fp,col);await p.goto('file://'+fp);await p.waitForTimeout(900);await p.screenshot({path:path.resolve(__dirname,'venda-floripa-04-estrutura.jpg'),type:'jpeg',quality:90});require('fs').unlinkSync(fp);console.log('ok 04')}
 await b.close()})();

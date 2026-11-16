const {chromium}=require('playwright');const path=require('path');
const R=path.resolve(__dirname,'../../../docs');
const foto=n=>n.startsWith('IMG')?'file://'+path.resolve(__dirname,'../fotos/'+n):'file://'+R+'/lancamento/img/resultados/'+n;
const font='file://'+R+'/assets/fonts/';
const ADS=[
 {id:'01-formato',img:'IMG_1914.jpg',pos:'center 45%',k:'À venda · Florianópolis (SC)',h:'Operação de glamping à venda em Florianópolis',s:'3 cabanas em operação · mobiliário · a operação inteira',chips:['Mais de 2 anos de operação','Demanda turística comprovada']},
 {id:'02-comprador',img:'IMG_1908.jpg',pos:'center 40%',k:'Operação em funcionamento',h:'Quer ser dono de um glamping sem construir do zero?',s:'Mais de 2 anos de operação, com demanda turística comprovada.',chips:['Faturamento consolidado','Taxa de ocupação demonstrável','DRE e documentos']},
 {id:'03-transparencia',img:'IMG_1916.jpg',pos:'center 50%',k:'Transpasso',h:'Transpasso de operação, não venda de imóvel.',s:'Terreno arrendado · 3 cabanas e mobiliário',chips:['Faturamento consolidado','DRE demonstrável']}
];
const html=a=>`<!doctype html><meta charset=utf-8><style>
@font-face{font-family:C;src:url(${font}cormorant.woff2);font-weight:300 700}
@font-face{font-family:A;src:url(${font}aventa.woff2);font-weight:300 700}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;position:relative;overflow:hidden;background:#040605;font-family:A}
.bg{position:absolute;inset:0;background:url(${foto(a.img)}) ${a.pos}/cover}
.sh{position:absolute;left:0;right:0;bottom:0;height:75%;background:linear-gradient(transparent,rgba(4,6,5,.9) 45%,#040605)}
.t{position:absolute;left:70px;right:70px;bottom:140px;color:#FEF5F0}
.k{font-size:30px;letter-spacing:.24em;text-transform:uppercase;color:#C9B37E;margin-bottom:22px}
h1{font-family:C;font-weight:500;font-size:104px;line-height:1.02}
.s{font-size:38px;color:#DED6BF;margin-top:26px;line-height:1.3}
.ch{display:flex;flex-wrap:wrap;gap:14px;margin-top:30px}.ch i{font-style:normal;font-size:29px;color:#C9B37E;border:2px solid rgba(201,179,126,.6);border-radius:40px;padding:10px 24px;background:rgba(4,6,5,.55)}
.f{position:absolute;left:70px;right:70px;bottom:56px;display:flex;justify-content:space-between;font-size:26px;color:#C9B37E;letter-spacing:.08em;border-top:1px solid rgba(201,179,126,.5);padding-top:22px}
</style><div class=bg></div><div class=sh></div>
<div class=t><div class=k>${a.k}</div><h1>${a.h}</h1><div class=s>${a.s}</div><div class=ch>${(a.chips||[]).map(c=>'<i>✓ '+c+'</i>').join('')}</div></div>
<div class=f><span>ZION HOTEL GROUP INTERNATIONAL</span><span>Fotos reais</span></div>`;
(async()=>{const b=await chromium.launch();
 for(const a of ADS){const p=await b.newPage({viewport:{width:1080,height:1350}});const fp=path.resolve(__dirname,'_tmp_'+a.id+'.html');require('fs').writeFileSync(fp,html(a));await p.goto('file://'+fp);await p.waitForTimeout(900);
  await p.screenshot({path:path.resolve(__dirname,`venda-floripa-${a.id}.jpg`),type:'jpeg',quality:90});console.log('ok',a.id);require('fs').unlinkSync(fp)}
 await b.close()})();

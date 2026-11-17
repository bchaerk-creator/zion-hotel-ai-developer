const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
const R=path.resolve(__dirname,'../../../docs');
const foto=n=>'file://'+path.resolve(__dirname,'../fotos/'+n+'.jpg');
const font='file://'+R+'/assets/fonts/';
const base=`@font-face{font-family:C;src:url(${font}cormorant.woff2);font-weight:300 700}
@font-face{font-family:A;src:url(${font}aventa.woff2);font-weight:300 700}
*{margin:0;box-sizing:border-box}body{position:relative;overflow:hidden;background:#040605;font-family:A;color:#FEF5F0}
.bg{position:absolute;inset:0;background-size:cover}
.k{font-size:27px;letter-spacing:.24em;text-transform:uppercase;color:#C9B37E}
.f{position:absolute;left:64px;right:64px;bottom:40px;display:flex;justify-content:space-between;font-size:23px;color:#C9B37E;letter-spacing:.08em;border-top:1px solid rgba(201,179,126,.45);padding-top:18px}
.n{position:absolute;right:64px;top:56px;font-size:26px;color:#C9B37E;letter-spacing:.1em;z-index:3}
.li{display:flex;gap:20px;align-items:flex-start;margin:0 0 24px}
.ic{flex:0 0 62px;height:62px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:700;background:#C9B37E;color:#040605}
.li b{display:block;font-size:42px;font-weight:600;line-height:1.1}
.li span{display:block;font-size:27px;color:#DED6BF;margin-top:4px;line-height:1.3}
h1{font-family:C;font-weight:500;line-height:1.02}`;
const foot=(r)=>`<div class=f><span>ZION COLLECTION</span><span>${r||'Fotos reais'}</span></div>`;
const ph=(n,x,y,w,h,pos)=>`<div style="position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:18px;background:url(${foto(n)}) ${pos||'center'}/cover"></div>`;
const cap=(k,t,s,sz)=>`<div style="position:absolute;left:64px;right:64px;bottom:118px"><div class=k>${k}</div><div style="font-family:C;font-size:${sz||70}px;line-height:1.02;margin-top:10px">${t}</div>${s?`<div style="font-size:31px;color:#DED6BF;margin-top:12px;line-height:1.3">${s}</div>`:''}</div>`;
const full=(img,pos,grad)=>`<div class=bg style="background-image:url(${foto(img)});background-position:${pos}"></div><div style="position:absolute;inset:0;background:linear-gradient(transparent ${(grad||55)-8}%,rgba(4,6,5,.94) 82%,#040605)"></div>`;
const S=1080,N=10;
const page=(w,h,inner,extra)=>`<style>${base}body{width:${w}px;height:${h}px}${extra||''}</style>${inner}`;
const top=(k,t,sub,sz)=>`<div style="position:absolute;left:64px;right:64px;top:70px"><div class=k>${k}</div><div style="font-family:C;font-size:${sz||70}px;line-height:1.02;margin-top:12px">${t}</div>${sub?`<div style="font-size:30px;color:#DED6BF;margin-top:12px;line-height:1.3">${sub}</div>`:''}</div>`;
const shade=(dir,pct)=>`<div style="position:absolute;inset:0;background:linear-gradient(${dir},rgba(4,6,5,.9),transparent ${pct}%)"></div>`;
const bgp=(img,pos)=>`<div class=bg style="background-image:url(${foto(img)});background-position:${pos||'center'}"></div>`;
const CARDS=[
 page(S,S,`${bgp('bolha-jacuzzi','center 30%')}${full('bolha-jacuzzi','center 30%',50)}<div class=n>1/${N}</div>${cap('À venda · Urubici (SC)','Imóvel e operação hoteleira, no meio da Serra','Glamping de luxo natural, com mais de 5 anos de operação',70)}${foot()}`),
 page(S,S,`<div class=n>2/${N}</div>${ph('aerea-floresta',64,80,560,420)}${ph('aerea-topo',644,80,372,420,'center 40%')}${ph('bolha-nuvens',64,520,372,300)}${ph('interior-neon',456,520,270,300,'center 55%')}${ph('interior-araucaria',746,520,270,300,'center 40%')}<div style="position:absolute;left:64px;right:64px;bottom:118px"><div class=k>Glamping · luxo natural</div><div style="font-family:C;font-size:58px;line-height:1.05;margin-top:8px">Hospedagem de experiência cercada de araucárias</div></div>${foot()}`),
 page(S,S,`${bgp('panoramica','center')}${shade('to top',58).replace('rgba(4,6,5,.9),transparent','rgba(4,6,5,.95),transparent')}<div class=n>3/${N}</div>${cap('O imóvel','3 hectares escriturados, de frente para a SC-110','Condomínio Mont Blanc Village, na Serra Catarinense',66)}${foot()}`),
 page(S,S,`${bgp('american-house','center 60%')}${shade('to top',55).replace('rgba(4,6,5,.9),transparent','rgba(4,6,5,.95),transparent')}<div class=n>4/${N}</div>${cap('Guest houses','Duas casas de alto padrão, com vista para o vale','American Guest House e Scandi Guest House, 3 quartos cada',64)}${foot()}`),
 page(S,S,`${full('duas-bolhas','center 50%',55)}<div class=n>5/${N}</div>${cap('3 suítes glamping','Bolhas com deck privativo na mata','Cama queen, ar-condicionado, frigobar e enxoval de alta qualidade',66)}${foot()}`),
 page(S,S,`<div class=n>6/${N}</div>${ph('interior-araucaria',64,80,310,480,'center 35%')}${ph('interior-neon',394,80,310,480,'center 50%')}${ph('ceu-bolha',724,80,292,480,'center')}${ph('bolha-nuvens',64,580,952,250,'center 40%')}<div style="position:absolute;left:64px;right:64px;bottom:118px"><div class=k>Por dentro das suítes</div><div style="font-family:C;font-size:58px;line-height:1.05;margin-top:8px">Vista aberta para as araucárias e o céu</div></div>${foot()}`),
 page(S,S,`${full('aerea-neon','center 45%',55)}<div class=n>7/${N}</div>${cap('Experiência','Deck privativo e banheira de imersão ao ar livre','Silêncio, privacidade e conexão com a natureza',62)}${foot()}`),
 page(S,S,`<div class=n>8/${N}</div><div style="position:absolute;left:64px;right:64px;top:100px"><div class=k>Operação hoteleira ativa</div><h1 style="font-size:70px;margin:12px 0 32px">Um ativo que já opera. E você confere.</h1>
 <div class=li><div class=ic>✓</div><div><b>Operação com mais de 5 anos</b><span>Hospedagem em funcionamento, recebendo hóspedes</span></div></div>
 <div class=li><div class=ic>✓</div><div><b>Faturamento e ocupação demonstráveis</b><span>Resultado da operação auditável, após o termo de confidencialidade</span></div></div>
 <div class=li><div class=ic>✓</div><div><b>Ativo off-market</b><span>Informações completas mediante contato direto</span></div></div></div>${ph('aerea-topo',64,720,952,230,'center 45%')}${foot('Material confidencial')}`,'body{background:#1B2117}'),
 page(S,S,`<div class=n>9/${N}</div><div style="position:absolute;left:64px;right:64px;top:90px"><div class=k>O que vem no ativo</div><h1 style="font-size:66px;margin:12px 0 30px">Terreno, hospedagens e estrutura de operação</h1>
 <div class=li><div class=ic>✓</div><div><b>3 suítes glamping e 2 guest houses</b><span>Cada unidade com área privativa</span></div></div>
 <div class=li><div class=ic>✓</div><div><b>Estrutura completa de operação</b><span>Cozinha profissional, lavanderia, manutenção e recepção</span></div></div>
 <div class=li><div class=ic>✓</div><div><b>Estacionamento para 8 veículos</b><span>Acesso direto pela SC-110</span></div></div></div>${ph('panoramica',64,690,952,270,'center 45%')}${foot()}`,'body{background:#040605}'),
 page(S,S,`${bgp('aerea-floresta','center')}<div style="position:absolute;inset:0;background:rgba(4,6,5,.6)"></div><div class=n>10/${N}</div><div style="position:absolute;left:64px;right:64px;top:150px"><div class=k>Interessado?</div><h1 style="font-size:92px;margin:16px 0 26px">Quer conhecer o ativo?</h1><div style="font-size:38px;color:#DED6BF;line-height:1.3">Responda ao formulário e veja o valor e as condições.</div><div style="display:inline-block;margin-top:44px;padding:26px 52px;background:#C9B37E;color:#040605;border-radius:60px;font-size:36px;font-weight:700">Quero saber mais</div></div>${foot()}`)
];
const ads=[
 {id:'01-ativo',img:'bolha-jacuzzi',pos:'center 40%',k:'À venda · Urubici (SC)',h:'Imóvel e operação hoteleira, no meio da Serra',s:'Glamping de luxo natural, com mais de 5 anos de operação.',chips:['3 hectares escriturados','Operação ativa','Off-market']},
 {id:'02-estrutura',img:'aerea-floresta',pos:'center 40%',k:'Urubici · Serra Catarinense',h:'Não é projeto. É um ativo em operação.',s:'Operação hoteleira com mais de 5 anos, faturando e recebendo hóspedes, com o imóvel.',chips:['Faturamento demonstrável','Ocupação e DRE','Ativo off-market']},
 {id:'03-imovel',img:'panoramica',pos:'center 50%',k:'Imóvel + operação',h:'3 hectares, 3 suítes glamping e 2 guest houses',s:'No Mont Blanc Village, de frente para a SC-110.',chips:['Escriturado','Glamping de luxo natural','Estrutura completa']}
];
const adHtml=a=>`<style>${base}body{width:1080px;height:1350px}.sh{position:absolute;left:0;right:0;bottom:0;height:62%;background:linear-gradient(transparent,rgba(4,6,5,.9) 45%,#040605)}.t{position:absolute;left:70px;right:70px;bottom:140px}.ch{display:flex;flex-wrap:wrap;gap:14px;margin-top:30px}.ch i{font-style:normal;font-size:29px;color:#C9B37E;border:2px solid rgba(201,179,126,.6);border-radius:40px;padding:10px 24px;background:rgba(4,6,5,.55)}</style>${a.full?`<div class=bg style="background-image:url(${foto(a.img)});background-position:center 96%"></div><div style="position:absolute;left:0;right:0;top:0;height:50%;background:linear-gradient(rgba(4,6,5,.92),transparent)"></div>`:`<div class=bg style="height:760px;background-image:url(${foto(a.img)});background-position:${a.pos}"></div><div class=sh style="top:560px;height:auto"></div>`}<div class=t ${a.full?'style="top:70px;bottom:auto"':''}><div class=k>${a.k}</div><h1 style="font-size:80px;margin-top:20px">${a.h}</h1><div style="font-size:38px;color:#DED6BF;margin-top:24px;line-height:1.3">${a.s}</div><div class=ch>${a.chips.map(c=>'<i>✓ '+c+'</i>').join('')}</div></div><div class=f style="left:70px;right:70px;bottom:56px"><span>ZION COLLECTION</span><span>Fotos reais</span></div>`;
(async()=>{const b=await chromium.launch();
 const shot=async(html,w,h,out)=>{const p=await b.newPage({viewport:{width:w,height:h}});const fp=path.resolve(__dirname,'_t.html');fs.writeFileSync(fp,'<!doctype html><meta charset=utf-8>'+html);await p.goto('file://'+fp);await p.waitForTimeout(900);await p.screenshot({path:path.resolve(__dirname,out),type:'jpeg',quality:90});fs.unlinkSync(fp);console.log('ok',out)};
 for(let i=0;i<CARDS.length;i++) await shot(CARDS[i],S,S,`carrossel-c${i+1}.jpg`);
 for(const a of ads) await shot(adHtml(a),1080,1350,`urubici-${a.id}.jpg`);
 await b.close()})();

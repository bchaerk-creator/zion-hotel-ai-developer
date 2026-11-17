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
const S=1080,N=8;
const page=(w,h,inner,extra)=>`<style>${base}body{width:${w}px;height:${h}px}${extra||''}</style>${inner}`;
const CARDS=[
 page(S,S,`${full('bolha-araucaria','center 40%',58)}<div class=n>1/${N}</div>${cap('À venda · Urubici (SC)','Imóvel e operação hoteleira em Urubici','R$ 4,5 milhões · negociável. Operação com mais de 5 anos.',76)}${foot()}`),
 page(S,S,`<div class=n>2/${N}</div>${ph('aerea-bolha',64,80,560,420)}${ph('jacuzzi-bolha',644,80,372,420,'center')}${ph('interior-cama',64,520,372,300)}${ph('aerea-mata',456,520,270,300)}${ph('noturna',746,520,270,300,'center')}<div style="position:absolute;left:64px;right:64px;bottom:118px"><div class=k>Glamping · luxo natural</div><div style="font-family:C;font-size:58px;line-height:1.05;margin-top:8px">Hospedagem de experiência em Urubici, onde neva no inverno</div></div>${foot()}`,'body{background:#040605}'),
 page(S,S,`<div class=n>3/${N}</div><div style="position:absolute;left:64px;right:64px;top:90px"><div class=k>O que vem no ativo</div><h1 style="font-size:70px;margin:12px 0 30px">Terreno, hospedagens e estrutura de operação</h1>
 <div class=li><div class=ic>✓</div><div><b>3 hectares escriturados</b><span>Condomínio Mont Blanc Village, de frente para a SC-110</span></div></div>
 <div class=li><div class=ic>✓</div><div><b>3 suítes glamping e 2 guest houses</b><span>American Guest House e Scandi Guest House</span></div></div>
 <div class=li><div class=ic>✓</div><div><b>Estrutura completa de operação</b><span>Cozinha profissional, lavanderia, recepção e estacionamento para 8 veículos</span></div></div></div>${ph('aerea-vertical',64,700,300,260,'center 40%')}${ph('deck-vista',384,700,632,260)}${foot('Fotos reais')}`,'body{background:#1B2117}'),
 page(S,S,`${full('noturna','center 40%',50)}<div class=n>4/${N}</div>${cap('Experiência','Noites sob o céu estrelado','Suítes com vista para o vale e o céu aberto')}${foot()}`),
 page(S,S,`${full('jacuzzi-bolha','center 55%',58)}<div class=n>5/${N}</div>${cap('Wellness e luxo natural','Deck privativo com banheira de imersão ao ar livre','Ar-condicionado, frigobar e enxoval de alta qualidade',64)}${foot()}`),
 page(S,S,`<div class=n>6/${N}</div>${ph('interior-banheira',64,80,470,330)}${ph('cama-cortinas',554,80,462,330)}${ph('por-do-sol',64,430,470,300)}${ph('bolha-banheira',554,430,462,300)}<div style="position:absolute;left:64px;right:64px;bottom:118px"><div class=k>Por dentro das suítes</div><div style="font-family:C;font-size:58px;line-height:1.05;margin-top:8px">Cama queen, vista aberta e iluminação cênica</div></div>${foot()}`,'body{background:#040605}'),
 page(S,S,`<div class=n>7/${N}</div><div style="position:absolute;left:64px;right:64px;top:100px"><div class=k>Operação hoteleira ativa</div><h1 style="font-size:70px;margin:12px 0 32px">Um ativo que já opera. E você confere.</h1>
 <div class=li><div class=ic>✓</div><div><b>Operação com mais de 5 anos</b><span>Hospedagem em funcionamento, recebendo hóspedes</span></div></div>
 <div class=li><div class=ic>✓</div><div><b>Faturamento e ocupação demonstráveis</b><span>Resultado da operação auditável, após o termo de confidencialidade</span></div></div>
 <div class=li><div class=ic>✓</div><div><b>Ativo off-market</b><span>Informações completas mediante contato direto</span></div></div></div>${ph('aerea-mata',64,720,952,230,'center 45%')}${foot('Material confidencial')}`,'body{background:#1B2117}'),
 page(S,S,`${full('bolha-banheira','center 50%',20)}<div class=n>8/${N}</div><div style="position:absolute;left:64px;right:64px;top:150px"><div class=k>Interessado?</div><h1 style="font-size:92px;margin:16px 0 26px">Receba valor e condições</h1><div style="font-size:38px;color:#DED6BF;line-height:1.3">R$ 4,5 milhões, negociável. Responda ao formulário e enviamos os detalhes do ativo.</div><div style="display:inline-block;margin-top:44px;padding:26px 52px;background:#C9B37E;color:#040605;border-radius:60px;font-size:36px;font-weight:700">Quero saber mais</div></div>${foot()}`,'.bg{filter:brightness(.55)}')
];
const ads=[
 {id:'01-ativo',img:'bolha-araucaria',pos:'center 45%',k:'À venda · Urubici (SC)',h:'Imóvel e operação hoteleira em Urubici',s:'R$ 4,5 milhões, negociável. Operação com mais de 5 anos.',chips:['3 hectares escriturados','Glamping e guest houses','Neva no inverno']},
 {id:'02-estrutura',img:'aerea-bolha',pos:'center 40%',k:'Urubici · Serra Catarinense',h:'Não é projeto. É um ativo em operação.',s:'Operação hoteleira com mais de 5 anos, faturando e recebendo hóspedes. R$ 4,5 milhões, negociável.',chips:['Faturamento demonstrável','Ocupação e DRE','Ativo off-market']},
 {id:'03-experiencia',img:'jacuzzi-bolha',pos:'center 50%',k:'Hospedagem de experiência',h:'Glamping de luxo natural, pronto para operar',s:'Imóvel mais operação por R$ 4,5 milhões, negociável.',chips:['3 suítes glamping','2 guest houses','Mont Blanc Village']}
];
const adHtml=a=>`<style>${base}body{width:1080px;height:1350px}.sh{position:absolute;left:0;right:0;bottom:0;height:62%;background:linear-gradient(transparent,rgba(4,6,5,.9) 45%,#040605)}.t{position:absolute;left:70px;right:70px;bottom:140px}.ch{display:flex;flex-wrap:wrap;gap:14px;margin-top:30px}.ch i{font-style:normal;font-size:29px;color:#C9B37E;border:2px solid rgba(201,179,126,.6);border-radius:40px;padding:10px 24px;background:rgba(4,6,5,.55)}</style><div class=bg style="height:760px;background-image:url(${foto(a.img)});background-position:${a.pos}"></div><div class=sh style="top:560px;height:auto"></div><div class=t><div class=k>${a.k}</div><h1 style="font-size:80px;margin-top:20px">${a.h}</h1><div style="font-size:38px;color:#DED6BF;margin-top:24px;line-height:1.3">${a.s}</div><div class=ch>${a.chips.map(c=>'<i>✓ '+c+'</i>').join('')}</div></div><div class=f style="left:70px;right:70px;bottom:56px"><span>ZION COLLECTION</span><span>Fotos reais</span></div>`;
(async()=>{const b=await chromium.launch();
 const shot=async(html,w,h,out)=>{const p=await b.newPage({viewport:{width:w,height:h}});const fp=path.resolve(__dirname,'_t.html');fs.writeFileSync(fp,'<!doctype html><meta charset=utf-8>'+html);await p.goto('file://'+fp);await p.waitForTimeout(900);await p.screenshot({path:path.resolve(__dirname,out),type:'jpeg',quality:90});fs.unlinkSync(fp);console.log('ok',out)};
 for(let i=0;i<CARDS.length;i++) await shot(CARDS[i],S,S,`carrossel-c${i+1}.jpg`);
 for(const a of ads) await shot(adHtml(a),1080,1350,`urubici-${a.id}.jpg`);
 await b.close()})();

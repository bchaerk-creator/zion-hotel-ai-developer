const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
const R=path.resolve(__dirname,'../../../docs');
const foto=n=>'file://'+R+'/lancamento/img/resultados/'+n;
const font='file://'+R+'/assets/fonts/';
const base=`@font-face{font-family:C;src:url(${font}cormorant.woff2);font-weight:300 700}
@font-face{font-family:A;src:url(${font}aventa.woff2);font-weight:300 700}
*{margin:0;box-sizing:border-box}body{position:relative;overflow:hidden;background:#040605;font-family:A;color:#FEF5F0}
.bg{position:absolute;inset:0;background-size:cover}
.k{font-size:27px;letter-spacing:.24em;text-transform:uppercase;color:#C9B37E}
h1{font-family:C;font-weight:500;line-height:1.02}
.f{position:absolute;left:64px;right:64px;bottom:40px;display:flex;justify-content:space-between;font-size:23px;color:#C9B37E;letter-spacing:.08em;border-top:1px solid rgba(201,179,126,.45);padding-top:18px}
.n{position:absolute;right:64px;top:56px;font-size:26px;color:#C9B37E;letter-spacing:.1em}
.li{display:flex;gap:22px;align-items:flex-start;margin:0 0 30px}
.ic{flex:0 0 76px;height:76px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:700}
.ok{background:#C9B37E;color:#040605}.no{border:3px solid #8B714E;color:#e6c9a0}
.li b{display:block;font-size:50px;font-weight:600;line-height:1.1}
.li span{display:block;font-size:33px;color:#DED6BF;margin-top:6px;line-height:1.3}`;
const strip=(n)=>`<div style="position:absolute;left:64px;right:64px;bottom:110px;height:250px;border-radius:22px;background:url(${foto(n)}) center/cover"></div>`;
const foot=(r)=>`<div class=f><span>ZION HOTEL GROUP INTERNATIONAL</span><span>${r||'Fotos reais'}</span></div>`;
const S=1080;
const CARDS=[
 {id:'c1',w:S,h:S,html:`<style>${base}body{width:${S}px;height:${S}px}.bg{background-image:url(${foto('floripa-bolhas-deck.jpg')});background-position:center 35%}
 .sh{position:absolute;inset:0;background:linear-gradient(transparent 20%,rgba(4,6,5,.92) 62%,#040605)}
 .t{position:absolute;left:64px;right:64px;bottom:130px}h1{font-size:98px;margin:16px 0 22px}.s{font-size:36px;color:#DED6BF;line-height:1.3}</style>
 <div class=bg></div><div class=sh></div><div class=n>1/6</div>
 <div class=t><div class=k>À venda · Florianópolis (SC)</div><h1>Seja dono de um glamping em operação</h1><div class=s>3 cabanas funcionando hoje. Sem construir do zero.</div></div>${foot()}`},
 {id:'c2',w:S,h:S,html:`<style>${base}body{width:${S}px;height:${S}px;background:#1B2117}.t{position:absolute;left:64px;right:64px;top:100px}h1{font-size:76px;margin:14px 0 38px}</style>
 <div class=n>2/6</div><div class=t><div class=k>O que está à venda</div><h1>Você leva a operação inteira</h1>
 <div class=li><div class="ic ok">✓</div><div><b>3 cabanas em operação</b><span>Ativas e recebendo hóspedes hoje</span></div></div>
 <div class=li><div class="ic ok">✓</div><div><b>Todo o mobiliário</b><span>Dos 3 glampings, como estão operando</span></div></div>
 <div class=li><div class="ic ok">✓</div><div><b>O transpasso da operação</b><span>Você assume o negócio que já funciona</span></div></div></div>${strip('floripa-banheira-vista-piscina.jpg')}${foot('Venda do negócio')}`},
 {id:'c3',w:S,h:S,html:`<style>${base}body{width:${S}px;height:${S}px;background:#040605}.t{position:absolute;left:64px;right:64px;top:100px}h1{font-size:76px;margin:14px 0 38px}</style>
 <div class=n>3/6</div><div class=t><div class=k>O que NÃO está na venda</div><h1>Fica claro desde o início</h1>
 <div class=li><div class="ic no">✕</div><div><b>O terreno</b><span>É arrendado. Você não compra o imóvel.</span></div></div>
 <div class=li><div class="ic no">✕</div><div><b>Venda de imóvel</b><span>É transpasso de operação, não escritura</span></div></div>
 <div class=li><div class="ic no">✕</div><div><b>A expansão para mais 3 cabanas</b><span>É uma possibilidade, sujeita à autorização do proprietário e às licenças</span></div></div></div>${strip('floripa-deck-piscina-pronto.jpg')}${foot('Sem letra miúda')}`},
 {id:'c4',w:S,h:S,html:`<style>${base}body{width:${S}px;height:${S}px}.bg{background-image:url(${foto('floripa-interior-quarto.jpg')});background-position:center}
 .sh{position:absolute;inset:0;background:linear-gradient(transparent 45%,rgba(4,6,5,.92) 78%,#040605)}.t{position:absolute;left:64px;right:64px;bottom:120px}h1{font-size:78px;margin:12px 0 14px}.s{font-size:34px;color:#DED6BF;line-height:1.3}</style>
 <div class=bg></div><div class=sh></div><div class=n>4/6</div>
 <div class=t><div class=k>Operação ativa</div><h1>Hospedagem funcionando, não um projeto no papel</h1><div class=s>Fotos reais da operação em Florianópolis.</div></div>${foot()}`},
 {id:'c5',w:S,h:S,html:`<style>${base}body{width:${S}px;height:${S}px;background:#1B2117}.t{position:absolute;left:64px;right:64px;top:110px}h1{font-size:74px;margin:14px 0 40px}
 .p{display:flex;gap:24px;align-items:center;margin:0 0 26px;font-size:38px}.p i{flex:0 0 58px;height:58px;border-radius:50%;border:3px solid #C9B37E;color:#C9B37E;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:30px;font-weight:700}.p span{color:#DED6BF;font-size:28px;display:block}</style>
 <div class=n>5/6</div><div class=t><div class=k>Como funciona</div><h1>Do primeiro contato à visita</h1>
 <div class=p><i>1</i><div>Triagem rápida<span>Oito perguntas</span></div></div>
 <div class=p><i>2</i><div>Conversa com a equipe da Zion<span>Condições e perguntas</span></div></div>
 <div class=p><i>3</i><div>Termo de confidencialidade<span>Antes de abrir os dados</span></div></div>
 <div class=p><i>4</i><div>Dados da operação<span>Com documentos</span></div></div>
 <div class=p><i>5</i><div>Visita<span>Conhecer de perto</span></div></div></div>${foot('Processo reservado')}`},
 {id:'c6',w:S,h:S,html:`<style>${base}body{width:${S}px;height:${S}px}.bg{background-image:url(${foto('floripa-deck-piscina-pronto.jpg')});background-position:center 60%}
 .sh{position:absolute;inset:0;background:linear-gradient(rgba(4,6,5,.35),rgba(4,6,5,.9) 55%,#040605)}.t{position:absolute;left:64px;right:64px;top:150px}h1{font-size:92px;margin:16px 0 26px}
 .pr{font-family:C;font-size:110px;color:#C9B37E;line-height:1}.s{font-size:34px;color:#DED6BF;margin-top:14px}
 .b{display:inline-block;margin-top:44px;padding:26px 52px;background:#C9B37E;color:#040605;border-radius:60px;font-size:36px;font-weight:700}</style>
 <div class=bg></div><div class=sh></div><div class=n>6/6</div>
 <div class=t><div class=k>Quer saber mais?</div><h1>Receba as condições</h1><div class=pr>R$ 1,5 milhão</div><div class=s>Condições negociáveis na conversa.</div><div class=b>Faça a triagem e saiba mais</div></div>${foot()}`}
];
const ESTATICO={id:'estatico-4x5',w:1080,h:1350,html:`<style>${base}body{width:1080px;height:1350px}.bg{background-image:url(${foto('floripa-aerea-pronta.jpg')});background-position:center;height:560px;position:absolute;left:0;right:0;top:0}
 .sh{position:absolute;left:0;right:0;top:300px;height:260px;background:linear-gradient(transparent,#040605)}.t{position:absolute;left:64px;right:64px;top:520px}
 h1{font-size:80px;margin:10px 0 24px}.c{display:flex;gap:30px}.col{flex:1;border:2px solid rgba(201,179,126,.5);border-radius:20px;padding:26px 28px}
 .col h3{font-family:C;font-size:42px;color:#C9B37E;margin-bottom:14px}.col div{font-size:29px;line-height:1.35;margin:8px 0;color:#FEF5F0}.col.n2 h3{color:#e6c9a0}
 .pr{margin-top:26px;font-size:36px;color:#DED6BF}.pr b{color:#C9B37E;font-family:C;font-size:60px;font-weight:600}</style>
 <div class=bg></div><div class=sh></div>
 <div class=t><div class=k>À venda · Florianópolis (SC)</div><h1>Glamping em operação à venda</h1>
 <div class=c><div class=col><h3>✓ Está na venda</h3><div>3 cabanas em operação</div><div>Todo o mobiliário</div><div>O transpasso da operação</div></div>
 <div class="col n2"><h3>✕ Não está</h3><div>O terreno (arrendado)</div><div>Venda de imóvel</div><div>A expansão para mais 3 cabanas</div></div></div>
 <div class=pr>Por <b>R$ 1,5 milhão</b> · condições negociáveis</div></div>${foot()}`};
(async()=>{const b=await chromium.launch();
 for(const c of [...CARDS,ESTATICO]){const p=await b.newPage({viewport:{width:c.w,height:c.h}});const fp=path.resolve(__dirname,'_t_'+c.id+'.html');
  fs.writeFileSync(fp,'<!doctype html><meta charset=utf-8>'+c.html);await p.goto('file://'+fp);await p.waitForTimeout(900);
  await p.screenshot({path:path.resolve(__dirname,'carrossel-'+c.id+'.jpg'),type:'jpeg',quality:90});fs.unlinkSync(fp);console.log('ok',c.id)}
 await b.close()})();

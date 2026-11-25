// ZION CREATIVE · Captação corrigida (Caminho A) · Carrossel C v-captação, 7 cartões 1080x1350 PNG.
// Regras: mesma ordem narrativa do campeão; nenhum texto sobre foto (foto nítida em bloco próprio, texto em painel sólido);
// só fotos reais sem pessoas; cadastro gratuito explícito; formação paga citada; sem reunião, consultoria, avaliação, investimento ou parceria.
// Uso: node build_cards_captacao.js [pasta de saída]   (padrão: docs/ads/captacao-p0)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const R=path.resolve(__dirname,'../../docs');
const OUT=process.argv[2]||path.join(R,'ads/captacao-p0');
const F=p=>'file://'+path.join(R,p);
const C={musgo:'#1B2117',preto:'#040605',creme:'#FEF5F0',areia:'#DED6BF',terra:'#8B714E',ouro:'#C9B37E'};
const FONT=`@font-face{font-family:Co;src:url(${F('assets/fonts/cormorant.woff2')});font-weight:300 900}
@font-face{font-family:Co;font-style:italic;src:url(${F('assets/fonts/cormorant-italic.woff2')});font-weight:300 900}
@font-face{font-family:Av;src:url(${F('assets/fonts/aventa.woff2')});font-weight:300 900}`;
const CSS=`${FONT}*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Av}
.b{position:absolute}.co{font-family:Co}.c{text-align:center}
.foot{position:absolute;left:0;top:1252px;width:1080px;height:98px;background:${C.preto};color:#e8dfc8;display:flex;align-items:center;justify-content:center;padding:0 40px;font-size:20px;line-height:1.3;text-align:center}
.band{position:absolute;left:0;width:1080px;height:96px;background:${C.ouro};color:${C.preto};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:31px;letter-spacing:.01em}
.tag{position:absolute;right:80px;top:70px;height:48px;padding:0 24px;border-radius:24px;border:2px solid ${C.terra};color:${C.terra};display:flex;align-items:center;font-weight:700;font-size:19px;letter-spacing:.14em;text-transform:uppercase}
.ph{position:absolute;left:0;width:1080px;background-size:cover;background-repeat:no-repeat}
.li{display:flex;gap:24px;align-items:center;margin-top:22px}.ic{flex:0 0 60px;height:60px;border-radius:50%;background:${C.ouro};color:${C.preto};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:32px}`;
// rodapé de condições (todas as telas)
const COND='Cadastro gratuito, sem obrigação de compra · Formações pagas à parte, a partir de R$ 47 · Sem reunião, consultoria nem avaliação do terreno · Sem promessa de investimento, parceria ou renda · Fotos reais da Zion Bubble Glamping';
const COND3='Cadastro gratuito, sem obrigação de compra · Formações pagas à parte, a partir de R$ 47 · Sem reunião, consultoria nem avaliação do terreno · Sem promessa de investimento, parceria ou renda';
const foot=t=>`<div class="foot">${t||COND}</div>`;
const logo=(dark=true,l=80,t=58,w=230)=>`<img class="b" src="${F(dark?'brand/zion-logo-claro.png':'brand/zion-logo-escuro.png')}" style="left:${l}px;top:${t}px;width:${w}px">`;
const bg=(c,h=1252)=>`<div class="b" style="left:0;top:0;width:1080px;height:${h}px;background:${c}"></div>`;
const IMG=p=>F('assets/'+p);
const PHO=(p,pos,h)=>`<div class="ph" style="top:0;height:${h}px;background-image:url(${IMG(p)});background-position:${pos}"></div>`;
const PANEL=(top,col=C.musgo)=>`<div class="b" style="left:0;top:${top}px;width:1080px;height:${1252-top}px;background:${col};border-top:6px solid ${C.ouro}"></div>`;
const K=t=>`<div style="font-size:25px;letter-spacing:.2em;text-transform:uppercase;font-weight:800;color:${C.ouro}">${t}</div>`;
const H1=(t,s=84)=>`<div class="co" style="font-size:${s}px;line-height:1.02;font-weight:600;color:${C.creme};margin-top:10px">${t}</div>`;
const S=(t,s=36)=>`<div style="font-size:${s}px;line-height:1.3;font-weight:500;color:${C.areia};margin-top:20px">${t}</div>`;
const em=t=>`<i style="color:${C.ouro}">${t}</i>`;
const li=a=>a.map(t=>`<div class="li"><div class="ic">✓</div><b style="font-size:46px;font-weight:600;line-height:1.1;color:${C.creme}">${t}</b></div>`).join('');
const PT=(n,tot,img,pos,ph,body,panel=C.musgo)=>`${bg(C.preto)}${PHO(img,pos,ph)}${PANEL(ph,panel)}${logo(true,72,ph+26,200)}<div class="b" style="right:72px;top:${ph+30}px;font-size:24px;color:${C.ouro};letter-spacing:.1em">${n}/${tot}</div><div class="b" style="left:72px;right:72px;top:${ph+100}px">${body}</div>${foot()}`;
const TOT=7;
const cards=[
// 1 · hook preservado ("tem terreno, mas não tem capital?"), foto sem pessoa
PT(1,TOT,'operacoes/op08.webp','center',700,`${K('Terreno')}${H1('Você tem um terreno em um destino '+em('turístico')+', mas não tem capital para desenvolver?',70)}${S('Existe um primeiro passo que não exige obra: estruturar o projeto.',34)}`),
// 2 · potencial não basta
PT(2,TOT,'operacoes/op12.webp','center',640,`${H1('Seu terreno pode ter potencial turístico. '+em('Sozinho, isso não vira negócio.'),70)}${S('Falta transformar a vista bonita em projeto, números e conceito.',36)}`,C.preto),
// 3 · equação (sem foto)
`${bg(C.creme)}${logo(false)}<div class="tag">Zion · Educação</div><div class="b" style="left:80px;top:210px;font-size:24px;letter-spacing:.2em;font-weight:800;color:${C.terra}">A EQUAÇÃO</div>
<div class="b co c" style="left:80px;right:80px;top:300px;font-size:120px;line-height:1.1;font-weight:600;color:${C.musgo}">Terreno<br><i style="color:${C.terra}">+ projeto</i><br>= destino</div>
<div class="b" style="left:80px;right:80px;top:860px;font-size:38px;line-height:1.3;font-weight:500;color:${C.preto};text-align:center">Sem projeto, orçamento e estudo de viabilidade, é mais difícil apresentar o seu terreno a potenciais parceiros e investidores.</div>${foot(COND3)}`,
// 4 · o que se aprende (metodologia Zion)
PT(4,TOT,'store/dentro.webp','center',540,`${K('A metodologia Zion, em passos')}${li(['Território e infraestrutura','Mercado e público','Orçamento do projeto','Pré-viabilidade e Dossiê'])}`),
// 5 · autoridade documentada (Urubici e Florianópolis são operações reais da Zion)
PT(5,TOT,'store/noite.webp','center',640,`${K('De onde vem o conhecimento')}${H1('A Zion já opera hospedagens '+em('em Urubici e Florianópolis.'),72)}${S('E organiza esse conhecimento em formação digital para quem quer estruturar um projeto turístico.',33)}`),
// 6 · não precisa construir um hotel
PT(6,TOT,'operacoes/op09.webp','center',640,`${H1('Você não precisa começar '+em('construindo um hotel.'),84)}${S('Comece estruturando: dá para fazer isso no papel.',40)}`,C.preto),
// 7 · cartão final: cadastro gratuito + formação paga (preço claro), faixa reta, sem aparência de botão
`${bg(C.preto)}${PHO('operacoes/op11.webp','center',470)}${PANEL(470)}${logo(true,72,496,200)}<div class="b" style="right:72px;top:500px;font-size:24px;color:${C.ouro};letter-spacing:.1em">7/${TOT}</div>
<div class="b" style="left:72px;right:72px;top:570px">${K('Zion · educação para projetos turísticos')}<div class="co" style="font-size:124px;line-height:1;font-weight:700;color:${C.ouro};margin-top:10px">Cadastro gratuito</div>
<div style="font-size:40px;line-height:1.3;color:${C.creme};margin-top:28px">Receba conteúdos para dar os primeiros passos na estruturação do seu projeto. Sem obrigação de compra.</div>
<div style="font-size:35px;line-height:1.3;color:${C.areia};margin-top:30px">Existem formações pagas, como a <b style="color:${C.creme}">Mini Mentoria de Estruturação Zion (R$ 47, pagamento único)</b>. Só compra quem quiser.</div></div>
<div class="band" style="top:1156px">Cadastro gratuito · Formação paga a partir de R$47</div>${foot()}`
];
module.exports={cards};
if(require.main===module)(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
fs.mkdirSync(OUT,{recursive:true});const out=[];
for(let i=0;i<cards.length;i++){const name=`capt-c-carrossel-c-${i+1}.png`;const f=path.join(OUT,'_t.html');
  fs.writeFileSync(f,`<!doctype html><meta charset=utf-8><style>${CSS}</style><body>${cards[i]}</body>`);
  await pg.goto('file://'+f);await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(400);await pg.screenshot({path:path.join(OUT,name),type:'png'});fs.unlinkSync(f);out.push(name);}
await b.close();console.log(out.join('\n'));})();

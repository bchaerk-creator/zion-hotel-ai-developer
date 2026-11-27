// Carrossel V2 (dono de pousada / Airbnb) · Plataforma Zion Collection R$ 47. Mesmo visual do campeão, fotos reais Zion sem pessoas.
// Uso: node build_v2.js  (gera zc47v2-card-1..7.png)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const D=__dirname, R=path.resolve(D,'../..');
const IMG=n=>`file://${R}/assets/${n}`;
const css=`@font-face{font-family:P;src:url(file://${R}/trilha1/apresentacao/_motor/fonts/playfair-display-latin-wght-normal.woff2);font-weight:400 900}
@font-face{font-family:A;src:url(file://${R}/assets/fonts/aventa.woff2);font-weight:300 900}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;position:relative;overflow:hidden;background:#133107;color:#fff}
.b{position:absolute}.ph{position:absolute;background-size:cover;background-position:center}
.w{font-family:A;font-weight:800;text-transform:uppercase;text-align:center;line-height:1.08;letter-spacing:.01em}
.s{font-family:P;text-align:center;line-height:1.12}
.strip{position:absolute;left:0;top:0;width:1080px;height:54px;background:#0a0a0a;color:#C9B37E;font-family:A;font-weight:700;font-size:25px;letter-spacing:.2em;display:flex;align-items:center;justify-content:center;text-transform:uppercase;z-index:9}
.btn{position:absolute;display:flex;align-items:center;justify-content:center;text-align:center;font-family:P}
.leg{position:absolute;left:24px;bottom:20px;background:rgba(0,0,0,.6);color:#fff;font-family:A;font-size:19px;padding:6px 14px;border-radius:8px}
.note{font-family:P;text-align:center;line-height:1.15}`;
const G='#133107',Y='#947620',PU='#8f688f',BE='#d5c1bc';
const NOTA='*Parceria sujeita à análise. Não é garantida.';
const cards=[
// 1 hook
`<div class="b" style="left:0;top:54px;width:1080px;height:430px;background:${G}"></div>
<div class="b" style="left:215px;top:92px;width:650px;height:64px;background:#fff;display:flex;align-items:center;justify-content:center;font-family:A;font-weight:800;font-size:34px;letter-spacing:.3em;color:#111;padding-left:.3em">POUSADA · AIRBNB</div>
<div class="b w" style="left:80px;right:80px;top:190px;font-size:45px">Dono de pousada ou Airbnb: pensando em <i>diferenciação</i> e em expandir no seu destino?</div>
<div class="ph" style="left:0;top:484px;width:1080px;height:520px;background-image:url(${IMG('operacoes/op10.webp')})"></div><div class="leg">Fotos reais de operações da Zion</div>
<div class="b" style="left:0;top:1004px;width:1080px;height:346px;background:${G}"></div>
<div class="btn" style="left:65px;top:1050px;width:950px;height:122px;border-radius:26px;background:${Y};font-size:40px;line-height:1.1;padding:0 30px">INSCREVA-SE NA NOSSA PLATAFORMA · R$ 47</div>
<div class="b w" style="left:60px;right:60px;top:1210px;font-size:27px;text-transform:none;font-weight:700;line-height:1.25">Apresente a sua ideia e o seu negócio de forma estruturada</div>`,
// 2 virada
`<div class="ph" style="left:0;top:54px;width:1080px;height:1296px;background-image:url(${IMG('store/hero.webp')});background-position:50% 30%"></div>
<div class="b" style="left:0;top:700px;width:1080px;height:650px;background:linear-gradient(0deg,rgba(4,6,5,.96) 55%,rgba(4,6,5,0))"></div>
<div class="b s" style="left:70px;right:70px;top:930px;font-size:78px;font-weight:600;line-height:1.05">Pare de vender <i style="color:#C9B37E">paredes</i>.<br>Comece a vender <i style="color:#C9B37E">experiência</i>.</div>
<div class="b w" style="left:70px;right:70px;top:1215px;font-size:27px;text-transform:none;font-weight:600;color:rgba(255,255,255,.9)">Diferenciação é o que faz o seu destino ser lembrado</div><div class="leg" style="bottom:auto;top:76px">Foto real de operação da Zion</div>`,
// 3 oportunidade
`<div class="b" style="left:0;top:54px;width:560px;height:1296px;background:${Y}"></div>
<div class="b w" style="left:40px;width:480px;top:130px;font-size:30px;color:#fff">Para donos de pousada e Airbnb</div>
<div class="b s" style="left:36px;width:488px;top:300px;font-size:62px;font-weight:700;color:#0b0b0b;line-height:1.08">Estamos abrindo a oportunidade de você ser um parceiro Zion*</div>
<div class="b s" style="left:40px;width:480px;top:830px;font-size:36px;color:#fff;line-height:1.2">Inscreva-se na nossa plataforma e apresente a sua ideia e o seu negócio.</div>
<div class="note b" style="left:40px;width:480px;top:1250px;font-size:22px;color:#fff">${NOTA}</div>
<div class="ph" style="left:560px;top:54px;width:520px;height:1296px;background-image:url(${IMG('store/dentro.webp')});background-position:38% 50%"></div>`,
// 4 como funciona
`<div class="ph" style="left:0;top:54px;width:1080px;height:560px;background-image:url(${IMG('operacoes/op07.webp')});background-position:50% 55%"></div>
<div class="b" style="left:0;top:614px;width:1080px;height:736px;background:${G}"></div>
<div class="b s" style="left:60px;right:60px;top:650px;font-size:50px;font-weight:700;color:#C9B37E">Como funciona</div>
<div class="b" style="left:80px;top:760px;width:920px;font-family:P;font-size:46px;line-height:1.28;color:#fff">
<div style="margin-bottom:34px"><span style="color:#C9B37E;font-weight:700">1.</span> Preencha os formulários</div>
<div style="margin-bottom:34px"><span style="color:#C9B37E;font-weight:700">2.</span> Assista aos vídeos</div>
<div style="margin-bottom:34px"><span style="color:#C9B37E;font-weight:700">3.</span> Faça os exercícios</div></div>
<div class="b w" style="left:70px;right:70px;top:1235px;font-size:26px;text-transform:none;font-weight:600">Apresente a sua ideia e o seu negócio de forma estruturada</div><div class="leg" style="bottom:auto;top:76px">Foto real de operação da Zion</div>`,
// 5 queremos te conhecer
`<div class="ph" style="left:0;top:54px;width:1080px;height:1050px;background-image:url(${IMG('store/noite.webp')});background-position:50% 50%"></div>
<div class="b" style="left:0;top:54px;width:1080px;height:520px;background:linear-gradient(180deg,rgba(4,6,5,.75),rgba(4,6,5,0))"></div>
<div class="b s" style="left:70px;right:70px;top:150px;font-size:92px;font-weight:600;line-height:1.02">Queremos te <i style="color:#C9B37E">conhecer</i>.</div>
<div class="b" style="left:0;top:1104px;width:1080px;height:246px;background:${BE}"></div>
<div class="b w" style="left:60px;right:60px;top:1128px;font-size:33px;color:#232c0a;font-weight:500">Depois de preencher os formulários, você pode solicitar a sua sessão de direcionamento com a nossa equipe, com os próximos passos*</div>
<div class="note b" style="left:60px;right:60px;top:1296px;font-size:21px;color:#232c0a">*Sessão sujeita à análise e à agenda. Parceria não é garantida.</div>`,
// 6 autoridade
`<div class="ph" style="left:0;top:54px;width:1080px;height:760px;background-image:url(${IMG('operacoes/op11.webp')});background-position:50% 45%"></div>
<div class="b" style="left:0;top:814px;width:1080px;height:536px;background:${PU}"></div>
<div class="b s" style="left:60px;right:60px;top:850px;font-size:66px;font-weight:900;color:#0b0b0b;line-height:1.05">Vem com a Zion.</div>
<div class="b s" style="left:80px;right:80px;top:960px;font-size:44px;font-weight:700;color:#0b0b0b;text-transform:uppercase;line-height:1.1">Desenvolvemos projetos de hospedagem e turismo há mais de 20 anos</div>
<div class="b s" style="left:80px;right:80px;top:1150px;font-size:36px;font-weight:700;color:#fff;text-transform:uppercase;line-height:1.12">E somos referência em glamping no Brasil</div>
<div class="leg" style="bottom:auto;top:76px">Foto real de operação da Zion</div>`,
// 7 conversão
`<div class="b" style="left:0;top:54px;width:572px;height:1296px;background:${Y}"></div>
<div class="b s" style="left:40px;width:492px;top:130px;font-size:50px;font-weight:900;color:#0b0b0b;text-transform:uppercase;line-height:1.1">Plataforma Zion Collection</div>
<div class="b s" style="left:40px;width:492px;top:310px;font-size:31px;color:#0b0b0b;line-height:1.2">Apresente a sua ideia e o seu negócio de forma estruturada e tenha a possibilidade de ser parceiro Zion*</div>
<div class="b s" style="left:40px;width:492px;top:520px;font-size:120px;color:#0b0b0b;line-height:1">R$ 47</div>
<div class="b s" style="left:40px;width:492px;top:670px;font-size:28px;color:#0b0b0b;line-height:1.3">Pagamento único, sem mensalidade<br>Pix ou cartão<br>Reembolso em até 7 dias</div>
<div class="btn" style="left:46px;top:900px;width:480px;height:215px;border-radius:52px;background:#ffed00;color:#0b0b0b;font-size:40px;font-weight:900;line-height:1.05;padding:0 24px">INSCREVA-SE NA NOSSA PLATAFORMA</div>
<div class="note b" style="left:40px;width:492px;top:1180px;font-size:21px;color:#0b0b0b">${NOTA}</div>
<div class="ph" style="left:572px;top:54px;width:508px;height:1296px;background-image:url(${IMG('operacoes/op12.webp')});background-position:50% 50%"></div>`];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(let i=0;i<cards.length;i++){const f=`${D}/_t2.html`;
 fs.writeFileSync(f,`<!doctype html><meta charset=utf-8><style>${css}</style><body>${cards[i]}<div class="strip">Acesso pago · Plataforma Zion Collection · R$ 47</div></body>`);
 await p.goto('file://'+f);await p.waitForTimeout(500);await p.screenshot({path:`${D}/zc47v2-card-${i+1}.png`});}
fs.unlinkSync(`${D}/_t2.html`);await b.close();})();

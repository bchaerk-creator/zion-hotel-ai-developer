// ZION INVESTORS · adaptação do carrossel campeão (Carrossel C, anúncio 120250522199990016).
// Base: os 7 cartões já renderizados do campeão (../inscricao-270/campeao-narrativa/, NÃO alterados).
// Fotos, ordem, fontes, cores e blocos preservados; muda só o texto. Exceção autorizada: Cartão 04
// (smartphone com print real do Instagram). Se existir ig-print.png nesta pasta, entra na tela do celular;
// sem ele, a tela mostra um aviso de "print pendente" (nunca um print inventado).
// Uso: node build.js  -> card-1..7.jpg, comparativo.jpg
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const D=__dirname, R=path.resolve(D,'../..');
const BASE=path.resolve(D,'../inscricao-270/campeao-narrativa');
const IG=path.join(D,'ig-print.png');const temIG=fs.existsSync(IG);
const css=`@font-face{font-family:P;src:url(file://${R}/trilha1/apresentacao/_motor/fonts/playfair-display-latin-wght-normal.woff2);font-weight:400 900}
@font-face{font-family:A;src:url(file://${R}/assets/fonts/aventa.woff2);font-weight:300 900}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;position:relative;overflow:hidden}
.o{position:absolute;inset:0;width:1080px;height:1350px}.b{position:absolute}
.w{font-family:A;font-weight:800;text-transform:uppercase;text-align:center;line-height:1.08;letter-spacing:.01em;transform:scaleX(1.12)}
.s{font-family:P;text-align:center;line-height:1.1}`;
const G='#133107',Y='#947620',O='#5a5529',PU='#8f688f',BE='#d5c1bc';
const cards=[
// 01 · atenção e identificação (campeão 1)
[1,`<div class="b" style="left:0;top:0;width:1080px;height:400px;background:${G}"></div>
<div class="b" style="left:195px;top:44px;width:720px;height:62px;background:#fff;display:flex;align-items:center;justify-content:center;font-family:A;font-weight:800;font-size:34px;letter-spacing:.42em;color:#111;padding-left:.42em">INVESTIDOR</div>
<div class="b w" style="left:50px;right:50px;top:128px;font-size:41px;color:#fff;line-height:1.1">Quem disse que você tem que construir um grande hotel para começar a faturar com hospedagem?</div>
<div class="b" style="left:0;top:1020px;width:1080px;height:330px;background:${G}"></div>
<div class="b s" style="left:45px;top:1090px;width:990px;height:122px;border-radius:26px;background:${Y};color:#fff;font-size:46px;display:flex;align-items:center;justify-content:center;letter-spacing:.01em">SEJA UM INVESTIDOR DA ZION.</div>`],
// 02 · clareza da oportunidade (campeão 2)
[2,`<div class="b" style="left:430px;top:0;width:650px;height:236px;background:${O}"></div>
<div class="b w" style="left:470px;width:560px;top:26px;font-size:38px;color:#16210a;line-height:1.05">Não estamos vendendo Bubbles.</div>
<div class="b" style="left:470px;top:128px;width:570px;text-align:center;font-family:A;font-weight:600;font-size:25px;line-height:1.22;color:#16210a">Estamos convidando você a investir capital na expansão dos nossos negócios.</div>
<div class="b" style="left:585px;top:628px;width:495px;height:210px;background:${O}"></div>
<div class="b s" style="left:590px;width:480px;top:636px;font-size:74px;font-weight:700;color:#fff;line-height:1">+23<br><span style="font-size:48px;letter-spacing:.04em">DESTINOS</span></div>
<div class="b" style="left:600px;top:782px;width:460px;text-align:center;font-family:A;font-weight:600;font-size:22px;line-height:1.2;color:#fff">Um plano de expansão em destinos turísticos por todo o Brasil.</div>
<div class="b" style="left:0;top:1285px;width:640px;height:65px;background:${O}"></div>
<div class="b s" style="left:0;top:1295px;width:640px;font-size:34px;color:#fff;font-style:italic">Seu capital. Nossa experiência.</div>`],
// 03 · autoridade e experiência (campeão 3)
[3,`<div class="b" style="left:0;top:0;width:514px;height:1350px;background:${Y}"></div>
<div class="b w" style="left:34px;width:446px;top:96px;font-size:34px;color:#fff">Pioneiros do glamping no Brasil.</div>
<div class="b s" style="left:30px;width:454px;top:330px;font-size:104px;color:#111;line-height:1">+20</div>
<div class="b s" style="left:30px;width:454px;top:440px;font-size:46px;color:#fff;letter-spacing:.06em">ANOS</div>
<div class="b" style="left:50px;width:414px;top:510px;text-align:center;font-family:A;font-weight:600;font-size:23px;line-height:1.2;color:#fff">De experiência dos fundadores no mercado hoteleiro.</div>
<div class="b s" style="left:30px;width:454px;top:646px;font-size:40px;color:#fff;letter-spacing:.1em">DESDE</div>
<div class="b s" style="left:30px;width:454px;top:690px;font-size:100px;color:#111;line-height:1">2020</div>
<div class="b" style="left:50px;width:414px;top:820px;text-align:center;font-family:A;font-weight:600;font-size:23px;line-height:1.2;color:#fff">De trajetória operacional da Zion no Brasil.</div>
<div class="b s" style="left:36px;width:442px;top:960px;height:215px;border-radius:34px;background:#000;color:#fff;font-size:35px;display:flex;align-items:center;justify-content:center;line-height:1.12;padding:0 22px">Não estamos começando do zero. Estamos expandindo.</div>
<div class="b" style="left:514px;top:0;width:566px;height:286px;background:#0c1608"></div><div class="b" style="left:514px;top:779px;width:566px;height:571px;background:#0c1608"></div>
<div class="b w" style="left:560px;width:470px;top:112px;font-size:30px;color:#fff;font-weight:500">Operação própria</div>
<div class="b s" style="left:560px;width:470px;top:905px;font-size:46px;color:#fff;text-align:left;line-height:1.12">CONSOLIDANDO UM MODELO DE NEGÓCIO VALIDADO NA PRÁTICA.</div>`],
// 05 · validação financeira (campeão 5)
[5,`<div class="b" style="left:0;top:1102px;width:1080px;height:248px;background:${BE}"></div>
<div class="b w" style="left:60px;right:60px;top:1128px;font-size:38px;color:#232c0a;font-weight:600;line-height:1.05">Um negócio sustentado por números reais.</div>
<div class="b" style="left:60px;right:60px;top:1236px;text-align:center;font-family:A;font-weight:600;font-size:24px;line-height:1.2;color:#232c0a">Conheça os indicadores de um modelo de negócio validado na prática.</div>
<div class="b" style="left:70px;right:70px;top:545px;text-align:center;font-family:A;font-weight:700;font-size:26px;line-height:1.5;letter-spacing:.06em;color:#fff;text-transform:uppercase;text-shadow:0 2px 10px rgba(0,0,0,.7)">Faturamento consolidado · Taxa de ocupação<br>Margem operacional · Rentabilidade histórica</div>`],
// 06 · oportunidade de mercado (campeão 6)
[6,`<div class="b" style="left:562px;top:0;width:518px;height:1350px;background:${Y}"></div>
<div class="b s" style="left:618px;width:400px;top:165px;height:815px;border-radius:44px;background:#000;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 26px;gap:34px"><div style="font-size:50px;line-height:1.14">Invista no futuro do turismo brasileiro.</div><div style="font-family:A;font-size:25px;line-height:1.25;font-weight:500;opacity:.92">O novo luxo está na natureza, na exclusividade e nas experiências.</div></div>
<div class="b s" style="left:595px;width:450px;top:1090px;font-size:34px;color:#fff;line-height:1.14">Conheça o potencial de um mercado que está transformando a hotelaria mundial.</div>`],
// 07 · conversão (campeão 7)
[7,`<div class="b" style="left:0;top:0;width:572px;height:1030px;background:${Y}"></div>
<div class="b s" style="left:30px;width:512px;top:70px;font-size:47px;font-weight:900;color:#0b0b0b;text-transform:uppercase;line-height:1.14">Invista em experiências.<br>Invista no glamping.<br>Invista na Zion.</div>
<div class="b s" style="left:40px;width:492px;top:420px;font-size:40px;color:#0b0b0b;line-height:1.12">Faça parte da nossa expansão pelo Brasil.</div>
<div class="b s" style="left:76px;width:424px;top:620px;height:230px;border-radius:52px;background:#ffed00;color:#0b0b0b;font-size:56px;display:flex;align-items:center;justify-content:center;line-height:1.02;letter-spacing:-.02em">SEJA UM INVESTIDOR.</div>
<div class="b" style="left:40px;top:880px;width:492px;text-align:center;font-family:A;font-weight:600;font-size:25px;line-height:1.25;color:#0b0b0b">Cadastre-se gratuitamente e solicite uma apresentação empresarial exclusiva.</div>
<div class="b" style="left:30px;top:1080px;width:420px;height:150px;background:${Y}"></div>
<div class="b" style="left:30px;top:1090px;width:420px;font-family:A;font-weight:800;font-size:24px;letter-spacing:.14em;line-height:1.35;color:#fff">ZION HOTEL GROUP<br>INTERNATIONAL</div>`]];
// 04 · a força da marca (única composição nova): smartphone + Instagram
const tela=temIG?`<img src="file://${IG}" style="width:100%;height:100%;object-fit:cover;object-position:top">`
 :`<div style="width:100%;height:100%;background:#1b1b1b;display:flex;align-items:center;justify-content:center;text-align:center;font-family:A;color:#c9b37e;font-size:25px;line-height:1.35;padding:30px;border:3px dashed #c9b37e">PRINT REAL DO INSTAGRAM<br>@zionbubble<br>A INSERIR<br><span style="font-size:19px;color:#ddd">pendente de Bruno</span></div>`;
const card4=`<div class="b" style="left:0;top:0;width:1080px;height:795px;background:rgba(10,20,8,.66)"></div>
<div class="b" style="left:445px;top:795px;width:635px;height:555px;background:${PU}"></div><div class="b" style="left:0;top:795px;width:445px;height:555px;background:${PU}"></div>
<div class="b" style="left:52px;top:300px;width:400px;height:800px;border-radius:64px;background:#0b0b0b;padding:14px;box-shadow:0 30px 70px rgba(0,0,0,.6);border:3px solid #3a3a3a"><div style="width:100%;height:100%;border-radius:50px;overflow:hidden;background:#000;position:relative">${tela}<div style="position:absolute;top:12px;left:50%;transform:translateX(-50%);width:110px;height:30px;border-radius:20px;background:#000"></div></div></div>
<div class="b s" style="left:500px;width:530px;top:120px;font-size:54px;font-weight:700;color:#fff;text-align:left;line-height:1.08">UMA REFERÊNCIA NACIONAL EM GLAMPING.</div>
<div class="b s" style="left:500px;width:530px;top:420px;font-size:98px;font-weight:700;color:#c9b37e;text-align:left;line-height:.95">+260<br><span style="font-size:42px;letter-spacing:.05em;color:#fff">MIL SEGUIDORES</span></div>
<div class="b" style="left:500px;top:640px;width:530px;font-family:A;font-weight:600;font-size:27px;line-height:1.5;color:#fff">• Forte posicionamento online<br>• Excelente reputação digital<br>• Reconhecimento nacional</div>
<div class="b" style="left:480px;top:850px;width:560px;font-family:A;font-weight:400;font-size:23px;line-height:1.35;color:#0b0b0b;font-weight:600">A Zion tornou-se uma referência no mercado brasileiro de glamping e hotelaria de luxo natural.</div>
<div class="b" style="left:0;top:1160px;width:1080px;height:190px;background:${PU}"></div>
<div class="b s" style="left:60px;width:960px;top:1200px;font-size:42px;font-weight:700;color:#0b0b0b;text-transform:uppercase;line-height:1.12">Mais do que hospedagem, construímos uma marca desejada.</div>`;
cards.splice(3,0,[4,card4]);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const [n,html] of cards){const f=`${D}/_t.html`;
 fs.writeFileSync(f,`<!doctype html><meta charset=utf-8><style>${css}</style><body><img class="o" src="file://${BASE}/carrossel-c-card-${n}.png">${html}</body>`);
 await p.goto('file://'+f);await p.waitForTimeout(400);await p.screenshot({path:`${D}/card-${n}.png`,type:'png'});}
fs.unlinkSync(`${D}/_t.html`);await b.close();})();

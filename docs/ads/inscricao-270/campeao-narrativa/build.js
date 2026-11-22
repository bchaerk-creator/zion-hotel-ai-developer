const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const D=__dirname, R=path.resolve(D,'../../..');
const css=`@font-face{font-family:P;src:url(file://${R}/trilha1/apresentacao/_motor/fonts/playfair-display-latin-wght-normal.woff2);font-weight:400 900}
@font-face{font-family:A;src:url(file://${R}/assets/fonts/aventa.woff2);font-weight:300 900}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;position:relative;overflow:hidden}
.o{position:absolute;inset:0;width:1080px;height:1350px}.b{position:absolute}
.w{font-family:A;font-weight:800;text-transform:uppercase;text-align:center;line-height:1.08;letter-spacing:.01em;transform:scaleX(1.12)}
.s{font-family:P;text-align:center;line-height:1.1}`;
const G='#133107',Y='#947620',O='#5a5529',PU='#8f688f',BE='#d5c1bc';
const cards=[
// 1 espelhamento (original 1)
[`o1.png`,`<div class="b" style="left:0;top:0;width:1080px;height:400px;background:${G}"></div>
<div class="b" style="left:195px;top:60px;width:720px;height:70px;background:#fff;display:flex;align-items:center;justify-content:center;font-family:A;font-weight:800;font-size:38px;letter-spacing:.42em;color:#111;padding-left:.42em">TERRENO</div>
<div class="b w" style="left:90px;right:90px;top:168px;font-size:47px;color:#fff">Você tem um terreno em um destino <i>turístico</i>, mas não tem capital para desenvolver?</div>
<div class="b" style="left:0;top:1020px;width:1080px;height:330px;background:${G}"></div>
<div class="b s" style="left:65px;top:1080px;width:950px;height:122px;border-radius:26px;background:${Y};color:#fff;font-size:64px;display:flex;align-items:center;justify-content:center;letter-spacing:.02em">INSCREVA SEU TERRENO</div>
<div class="b w" style="left:90px;right:90px;top:1232px;font-size:32px;color:#fff;text-transform:none">A Zion quer conhecer sua oportunidade</div>`],
// 2 confronto (original 2)
[`o2.png`,`<div class="b" style="left:430px;top:0;width:650px;height:236px;background:${O}"></div>
<div class="b w" style="left:470px;width:560px;top:44px;font-size:35px;color:#16210a">Seu terreno pode ter potencial turístico. Sozinho, isso não vira um negócio.</div>`],
// 3 reconhecimento (original 4)
[`o4.png`,`<div class="b" style="left:0;top:0;width:514px;height:1350px;background:${Y}"></div>
<div class="b w" style="left:40px;width:434px;top:110px;font-size:33px;color:#fff">Sem projeto, orçamento e estudo de viabilidade, fica mais difícil conversar com investidores</div>
<div class="b s" style="left:30px;width:454px;top:520px;font-size:60px;color:#fff;line-height:1.05">TERRENO +<br>PROJETO =<br><span style="color:#111;font-size:72px">DESTINO</span></div>
<div class="b s" style="left:30px;width:454px;top:760px;font-size:74px;color:#fff;letter-spacing:.02em">ZION</div>
<div class="b s" style="left:48px;width:424px;top:980px;height:175px;border-radius:34px;background:#000;color:#fff;font-size:58px;display:flex;align-items:center;justify-content:center;line-height:1.05">Inscreva seu terreno</div>
<div class="b" style="left:514px;top:0;width:566px;height:340px;background:linear-gradient(180deg,#0c1608 84%,rgba(12,22,8,0))"></div>
<div class="b w" style="left:560px;width:470px;top:120px;font-size:30px;color:#fff;font-weight:500">Apresente o que você já tem</div>
<div class="b" style="left:514px;top:715px;width:566px;height:635px;background:linear-gradient(0deg,#0c1608 90%,rgba(12,22,8,0))"></div>
<div class="b s" style="left:560px;width:470px;top:900px;font-size:54px;color:#fff;text-align:left;line-height:1.1">PROJETOS &amp;<br>OPORTUNIDADES</div>
<div class="b w" style="left:560px;width:470px;top:1120px;font-size:27px;color:#fff;font-weight:500;text-transform:none;line-height:1.25">A Zion avalia cada caso. Cadastro e análise não garantem investimento nem parceria.</div>`],
// 4 autoridade (original 6)
[`o6.png`,`<div class="b" style="left:445px;top:795px;width:635px;height:555px;background:${PU}"></div><div class="b" style="left:150px;top:1160px;width:930px;height:190px;background:${PU}"></div>
<div class="b s" style="left:455px;width:590px;top:835px;font-size:52px;font-weight:900;color:#0b0b0b;text-transform:uppercase;line-height:1.08">A Zion já opera hospedagens em Urubici e Florianópolis</div>
<div class="b s" style="left:150px;width:900px;top:1200px;font-size:38px;color:#fff;text-transform:uppercase;line-height:1.15">Mais de 20 anos de experiência internacional</div>`],
// 5 oportunidade (original 5)
[`o5.png`,`<div class="b" style="left:0;top:1102px;width:1080px;height:248px;background:${BE}"></div>
<div class="b w" style="left:80px;right:80px;top:1150px;font-size:44px;color:#232c0a;font-weight:500">Inscrições abertas para terrenos e projetos turísticos</div>`],
// 6 orientacao (original 3)
[`o3.png`,`<div class="b" style="left:562px;top:0;width:518px;height:1350px;background:${Y}"></div>
<div class="b s" style="left:618px;width:400px;top:165px;height:815px;border-radius:44px;background:#000;color:#fff;font-size:63px;display:flex;align-items:center;justify-content:center;line-height:1.16;padding:0 26px">Você não precisa começar construindo um hotel</div>
<div class="b s" style="left:600px;width:440px;top:1120px;font-size:44px;color:#fff;line-height:1.1">Apresente seu projeto em uma sessão estratégica</div>`],
// 7 conversao (original 7)
[`o7.png`,`<div class="b" style="left:0;top:0;width:572px;height:1030px;background:${Y}"></div>
<div class="b s" style="left:40px;width:492px;top:96px;font-size:52px;font-weight:900;color:#0b0b0b;text-transform:uppercase;line-height:1.1">A Zion quer conhecer sua oportunidade.</div>
<div class="b s" style="left:40px;width:492px;top:478px;font-size:66px;color:#0b0b0b;line-height:1.04">Inscrição<br>R$ 270</div>
<div class="b s" style="left:76px;width:424px;top:748px;height:258px;border-radius:52px;background:#ffed00;color:#0b0b0b;font-size:62px;display:flex;align-items:center;justify-content:center;line-height:1.0;letter-spacing:-.02em">Cadastre seu terreno ou projeto</div>`]];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(let i=0;i<cards.length;i++){const f=`${D}/_t.html`;fs.writeFileSync(f,`<!doctype html><meta charset=utf-8><style>${css}</style><body><img class="o" src="src/${cards[i][0]}">${cards[i][1]}</body>`);
 await p.goto('file://'+f);await p.waitForTimeout(350);await p.screenshot({path:`${D}/carrossel-c-card-${i+1}.png`});}
fs.unlinkSync(`${D}/_t.html`);await b.close();})();

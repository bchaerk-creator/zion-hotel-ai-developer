// Carrossel campeão com a narrativa do ACESSO À PLATAFORMA Zion Collection (R$ 47).
// Bases: cartões renderizados do campeão narrativo (inscricao-270/campeao-narrativa) e do Carrossel C de venda
// (venda-carrossel-c; fotos 4 e 7 já sem pessoas). Repinta os mesmos blocos de cor com texto novo.
// Uso: node build.js
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const D=__dirname, A=path.resolve(D,'..'), R=path.resolve(D,'../..');
const CN=`${A}/inscricao-270/campeao-narrativa/carrossel-c-card-`, VC=`${A}/venda-carrossel-c/carrossel-c-venda-`;
const css=`@font-face{font-family:P;src:url(file://${R}/trilha1/apresentacao/_motor/fonts/playfair-display-latin-wght-normal.woff2);font-weight:400 900}
@font-face{font-family:A;src:url(file://${R}/assets/fonts/aventa.woff2);font-weight:300 900}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;position:relative;overflow:hidden}
.o{position:absolute;inset:0;width:1080px;height:1350px}.b{position:absolute}
.w{font-family:A;font-weight:800;text-transform:uppercase;text-align:center;line-height:1.08;letter-spacing:.01em;transform:scaleX(1.12)}
.s{font-family:P;text-align:center;line-height:1.1}
.strip{position:absolute;left:0;top:0;width:1080px;height:54px;background:#0a0a0a;color:#C9B37E;font-family:A;font-weight:700;font-size:25px;letter-spacing:.2em;display:flex;align-items:center;justify-content:center;text-transform:uppercase}
.ilus{position:absolute;left:24px;bottom:22px;background:rgba(0,0,0,.6);color:#fff;font-family:A;font-size:20px;padding:6px 14px;border-radius:8px}`;
const G='#133107',Y='#947620',O='#5a5529',PU='#8f688f',BE='#d5c1bc';
const NOTA='*Parceria e investimento sujeitos à análise. Não são garantidos.';
const cards=[
// 1 hook
[CN+'1.png',`<div class="b" style="left:0;top:0;width:1080px;height:400px;background:${G}"></div>
<div class="b" style="left:195px;top:84px;width:720px;height:70px;background:#fff;display:flex;align-items:center;justify-content:center;font-family:A;font-weight:800;font-size:38px;letter-spacing:.42em;color:#111;padding-left:.42em">TERRENO</div>
<div class="b w" style="left:90px;right:90px;top:188px;font-size:47px;color:#fff">Você tem um terreno em um destino <i>turístico</i>, mas não tem capital para desenvolver?</div>
<div class="b" style="left:0;top:1020px;width:1080px;height:330px;background:${G}"></div>
<div class="b s" style="left:65px;top:1080px;width:950px;height:122px;border-radius:26px;background:${Y};color:#fff;font-size:50px;display:flex;align-items:center;justify-content:center">ACESSE A PLATAFORMA · R$ 47</div>
<div class="b w" style="left:60px;right:60px;top:1232px;font-size:31px;color:#fff;text-transform:none">Aprenda o passo a passo para estruturar o seu projeto</div>`],
// 2 confronto
[CN+'2.png',`<div class="b" style="left:430px;top:0;width:650px;height:236px;background:${O}"></div>
<div class="b w" style="left:470px;width:560px;top:70px;font-size:31px;color:#16210a">Seu terreno pode ter potencial turístico. Sozinho, isso não vira um projeto.</div><div class="ilus">Imagens ilustrativas</div>`],
// 3 reconhecimento
[CN+'3.png',`<div class="b" style="left:0;top:0;width:514px;height:1350px;background:${Y}"></div>
<div class="b w" style="left:40px;width:434px;top:110px;font-size:33px;color:#fff">Sem projeto estruturado, fica difícil apresentar a sua visão</div>
<div class="b s" style="left:30px;width:454px;top:500px;font-size:52px;color:#fff;line-height:1.05">TERRENO +<br>PASSO A PASSO =<br><span style="color:#111;font-size:76px">PROJETO</span></div>
<div class="b s" style="left:30px;width:454px;top:790px;font-size:74px;color:#fff;letter-spacing:.02em">ZION</div>
<div class="b s" style="left:48px;width:424px;top:980px;height:175px;border-radius:34px;background:#000;color:#fff;font-size:50px;display:flex;align-items:center;justify-content:center;line-height:1.05">Acesse a plataforma</div>
<div class="b" style="left:514px;top:0;width:566px;height:340px;background:linear-gradient(180deg,#0c1608 84%,rgba(12,22,8,0))"></div>
<div class="b w" style="left:560px;width:470px;top:120px;font-size:30px;color:#fff;font-weight:500">Estruture o que você já tem</div>
<div class="b" style="left:514px;top:715px;width:566px;height:635px;background:linear-gradient(0deg,#0c1608 90%,rgba(12,22,8,0))"></div>
<div class="b s" style="left:560px;width:470px;top:900px;font-size:50px;color:#fff;text-align:left;line-height:1.1">AULAS, FICHAS &amp;<br>FERRAMENTAS</div>
<div class="b w" style="left:560px;width:470px;top:1120px;font-size:27px;color:#fff;font-weight:500;text-transform:none;line-height:1.25">Material educativo. Parceria e investimento sujeitos à análise, sem garantia.</div>`],
// 4 autoridade (foto sem pessoas)
[VC+'4.png',`<div class="b" style="left:445px;top:1090px;width:635px;height:260px;background:${PU}"></div><div class="b" style="left:150px;top:1100px;width:930px;height:250px;background:${PU}"></div>
<div class="b s" style="left:170px;width:860px;top:1108px;font-size:34px;color:#fff;line-height:1.22">Ao se inscrever, você acessa a plataforma Zion, que faz parte da nossa expansão. E pode ser um próximo parceiro Zion a partir do resultado do seu projeto*</div>
<div class="b s" style="left:150px;width:900px;top:1304px;font-size:23px;color:#fff;line-height:1.1">${NOTA}</div>`],
// 5 plataforma
[CN+'5.png',`<div class="b" style="left:0;top:1102px;width:1080px;height:248px;background:${BE}"></div>
<div class="b w" style="left:70px;right:70px;top:1138px;font-size:40px;color:#232c0a;font-weight:500">Seja um parceiro Zion: inscreva seu terreno ou projeto, de forma estruturada, pela nossa plataforma*</div>
<div class="b s" style="left:70px;right:70px;top:1290px;font-size:22px;color:#232c0a">${NOTA}</div>`],
// 6 como funciona
[CN+'6.png',`<div class="b" style="left:562px;top:0;width:518px;height:1350px;background:${Y}"></div>
<div class="b s" style="left:618px;width:400px;top:165px;height:815px;border-radius:44px;background:#000;color:#fff;font-size:68px;display:flex;align-items:center;justify-content:center;line-height:1.2;padding:0 26px">Aprenda.<br>Estruture.<br>Apresente.</div>
<div class="b s" style="left:590px;width:460px;top:1060px;font-size:36px;color:#fff;line-height:1.15">Preencha o formulário, assista aos vídeos e anexe fotos do seu terreno</div>
<div class="b s" style="left:590px;width:460px;top:1235px;font-size:22px;color:#fff;line-height:1.15">*Sujeito à análise e à agenda. Parceria e investimento não são garantidos.</div>`],
// 7 conversão
[VC+'10.png',`<div class="b" style="left:0;top:0;width:572px;height:1030px;background:${Y}"></div>
<div class="b s" style="left:40px;width:492px;top:96px;font-size:50px;font-weight:900;color:#0b0b0b;text-transform:uppercase;line-height:1.1">Plataforma Zion Collection</div>
<div class="b s" style="left:40px;width:492px;top:290px;font-size:34px;color:#0b0b0b">Aprenda o passo a passo para estruturar o seu projeto</div>
<div class="b s" style="left:40px;width:492px;top:440px;font-size:120px;color:#0b0b0b;line-height:1.0">R$ 47</div>
<div class="b s" style="left:40px;width:492px;top:590px;font-size:27px;color:#0b0b0b;line-height:1.3">Pagamento único, sem mensalidade<br>Pix ou cartão<br>Reembolso em até 7 dias</div>
<div class="b s" style="left:46px;width:480px;top:790px;height:215px;border-radius:52px;background:#ffed00;color:#0b0b0b;font-size:50px;font-weight:900;display:flex;align-items:center;justify-content:center;line-height:1.05;padding:0 20px">QUERO INICIAR MINHA JORNADA NA ZION</div>`]];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(let i=0;i<cards.length;i++){const f=`${D}/_t.html`;
 fs.writeFileSync(f,`<!doctype html><meta charset=utf-8><style>${css}</style><body><img class="o" src="file://${cards[i][0]}">${cards[i][1]}<div class="strip">Acesso pago · Plataforma Zion Collection · R$ 47</div></body>`);
 await p.goto('file://'+f);await p.waitForTimeout(350);await p.screenshot({path:`${D}/zc47-card-${i+1}.png`});}
fs.unlinkSync(`${D}/_t.html`);await b.close();})();

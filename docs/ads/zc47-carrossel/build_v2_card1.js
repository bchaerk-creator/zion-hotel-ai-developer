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
<div class="b" style="left:195px;top:84px;width:720px;height:70px;background:#fff;display:flex;align-items:center;justify-content:center;font-family:A;font-weight:800;font-size:38px;letter-spacing:.42em;color:#111;padding-left:.42em">POUSADA · AIRBNB</div>
<div class="b w" style="left:90px;right:90px;top:188px;font-size:42px;color:#fff">Você tem uma pousada ou Airbnb e quer transformar seu empreendimento em um destino de experiências?</div>
<div class="b" style="left:0;top:1020px;width:1080px;height:330px;background:${G}"></div>
<div class="b s" style="left:65px;top:1080px;width:950px;height:122px;border-radius:26px;background:${Y};color:#fff;font-size:35px;display:flex;align-items:center;justify-content:center;line-height:1.1;padding:0 30px">INSCREVA SEU EMPREENDIMENTO NA NOSSA PLATAFORMA</div>
<div class="b w" style="left:60px;right:60px;top:1222px;font-size:26px;color:#fff;text-transform:none;line-height:1.2">Estruture seu projeto de expansão, diferenciação ou desenvolvimento através da plataforma Zion Collection.</div><div class="b w" style="left:60px;right:60px;top:1314px;font-size:17px;color:rgba(255,255,255,.8);text-transform:none;font-weight:500">Acesso pago: R$ 47. Material educativo.</div>`]];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
const f=`${D}/_t3.html`;
fs.writeFileSync(f,`<!doctype html><meta charset=utf-8><style>${css}</style><body><img class="o" src="file://${cards[0][0]}">${cards[0][1]}<div class="strip">Acesso pago · Plataforma Zion Collection · R$ 47</div></body>`);
await p.goto('file://'+f);await p.waitForTimeout(400);await p.screenshot({path:`${D}/zc47v2-card-1-pousada-bolha.png`});
fs.unlinkSync(f);await b.close();})();

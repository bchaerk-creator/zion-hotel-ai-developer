// ZION INVESTORS v4 · carrossel PARA INVESTIDORES (adaptação do Carrossel C campeão, anúncio 120250522199990016).
// Base: os 7 cartões já renderizados do campeão (../inscricao-270/campeao-narrativa/, NÃO alterados).
// Cores, fontes, blocos e ordem preservados; muda o texto. Direção de Bruno (28/11): "Seja um investidor na
// expansão da Zion. Não estamos oferecendo estruturas, estamos oferecendo a oportunidade de você investir
// capital na expansão da Zion. Marca reconhecida."
// Regras desta versão: só números com prova (+266 mil seguidores = print real ig-print.png; operação própria
// desde 2020 em Urubici e Florianópolis). "+23 destinos", "+20 anos" e "pioneiros" ficam FORA até Bruno comprovar.
// Sem promessa de retorno, renda, faturamento ou valorização. Aviso do cartão 7 = TEXTO A VALIDAR COM ADVOGADO.
// Fotos novas (cartões 1 e 2): só fotos reais da Zion SEM pessoas (op08, noite, op04, deck, hero), conferidas
// visualmente. Cartão 2: as etiquetas CABANAS/BUBBLE/TENDAS/BUBBLES saem e as fotos de terceiros (cabanas e
// tenda) são trocadas; a lua do desenho original é recortada do campeão (canvas) e repintada por cima.
// Uso: node build.js  -> card-1..7.jpg e comparativo.jpg (antes = git HEAD:card-N.jpg, se existir em _antes/)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {execSync}=require('child_process');
const D=__dirname, R=path.resolve(D,'../..');
const BASE=path.resolve(D,'../inscricao-270/campeao-narrativa');
const OP=path.join(R,'assets/operacoes'), ST=path.join(R,'assets/store');
const IG=path.join(D,'ig-print.png');const temIG=fs.existsSync(IG);
const css=`@font-face{font-family:P;src:url(file://${R}/trilha1/apresentacao/_motor/fonts/playfair-display-latin-wght-normal.woff2);font-weight:400 900}
@font-face{font-family:A;src:url(file://${R}/assets/fonts/aventa.woff2);font-weight:300 900}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;position:relative;overflow:hidden}
.o{position:absolute;inset:0;width:1080px;height:1350px}.b{position:absolute}
.f{position:absolute;object-fit:cover;display:block}
.w{font-family:A;font-weight:800;text-transform:uppercase;text-align:center;line-height:1.08;letter-spacing:.01em;transform:scaleX(1.12)}
.s{font-family:P;text-align:center;line-height:1.1}`;
const G='#133107',Y='#947620',O='#5a5529',PU='#8f688f',BE='#d5c1bc';
const foto=(src,x,y,w,h,pos='center')=>`<img class="f" src="file://${src}" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;object-position:${pos}">`;
// lua + estrela do cartão 2 do campeão, recortadas por brilho (branco puro dentro da elipse da lua; a etiqueta BUBBLE é cinza 244 e fica de fora)
const lua=`<canvas id="lua" class="b" width="1080" height="1350" style="left:0;top:0"></canvas><script>
const i=new Image();i.onload=()=>{const c=document.getElementById('lua').getContext('2d');const t=document.createElement('canvas');t.width=1080;t.height=1350;
const x=t.getContext('2d');x.drawImage(i,0,0);const s=x.getImageData(0,0,1080,1350),o=c.createImageData(1080,1350);
for(let y=520;y<845;y++)for(let X=405;X<725;X++){const ex=(X-565)/153,ey=(y-682)/154;if(ex*ex+ey*ey>1)continue;
const k=(y*1080+X)*4,r=s.data[k],g=s.data[k+1],b=s.data[k+2],m=Math.min(r,g,b);
if(Math.max(r,g,b)-m>8)continue;const a=Math.max(0,Math.min(255,(m-246)*255/9|0));if(a){o.data[k]=o.data[k+1]=o.data[k+2]=255;o.data[k+3]=a;}}
c.putImageData(o,0,0);window.pronto=1};i.src='file://${BASE}/carrossel-c-card-2.png';</script>`;
const cards=[
// 01 · para quem é (campeão 1): PARA INVESTIDORES + pergunta de quem tem capital. Foto: op08 (Zion, sem pessoas),
// a mesma cena do campeão, redesenhada para tirar a etiqueta CABANA.
[1,`${foto(`${OP}/op08.webp`,0,400,1080,620,'center 55%')}
<div class="b" style="left:0;top:0;width:1080px;height:400px;background:${G}"></div>
<div class="b" style="left:120px;top:40px;width:840px;height:78px;background:#fff;display:flex;align-items:center;justify-content:center;font-family:A;font-weight:800;font-size:40px;letter-spacing:.3em;color:#111;padding-left:.3em">PARA INVESTIDORES</div>
<div class="b w" style="left:100px;right:100px;top:156px;font-size:43px;color:#fff;line-height:1.12">Você quer investir capital na expansão de uma marca de glamping reconhecida?</div>
<div class="b" style="left:0;top:1020px;width:1080px;height:330px;background:${G}"></div>
<div class="b s" style="left:45px;top:1066px;width:990px;height:140px;border-radius:26px;background:${Y};color:#fff;font-size:42px;display:flex;align-items:center;justify-content:center;letter-spacing:.01em;line-height:1.12;padding:0 30px">SEJA UM INVESTIDOR NA EXPANSÃO DA ZION.</div>
<div class="b" style="left:40px;right:40px;top:1246px;text-align:center;font-family:A;font-weight:600;font-size:26px;color:#fff">+266 mil seguidores · Operação própria desde 2020</div>`],
// 02 · a oportunidade (campeão 2): investir capital, não comprar estrutura. Sem etiquetas; fotos só da Zion.
[2,`<div class="b" style="left:0;top:0;width:1080px;height:1350px;background:${O}"></div>
${foto(`${ST}/noite.webp`,0,12,410,456,'center 60%')}
${foto(`${OP}/op04.webp`,0,506,565,620,'center 60%')}
${foto(`${ST}/deck.webp`,591,240,489,365,'center')}
${foto(`${ST}/hero.webp`,675,842,405,508,'center 70%')}
${lua}
<div class="b" style="left:430px;top:0;width:650px;height:236px;background:${O}"></div>
<div class="b w" style="left:470px;width:560px;top:22px;font-size:37px;color:#16210a;line-height:1.05">Não estamos oferecendo estruturas.</div>
<div class="b" style="left:462px;top:118px;width:586px;text-align:center;font-family:A;font-weight:700;font-size:25px;line-height:1.2;color:#16210a">Estamos oferecendo a oportunidade de você investir capital na expansão da Zion.</div>
<div class="b" style="left:735px;top:640px;width:330px;text-align:center;font-family:A;font-weight:800;font-size:19px;letter-spacing:.18em;color:#fff">PARA INVESTIDORES</div>
<div class="b s" style="left:735px;width:330px;top:674px;font-size:36px;font-weight:700;color:#fff;line-height:1.08">Operação própria desde 2020</div>
<div class="b" style="left:735px;top:800px;width:330px;text-align:center;font-family:A;font-weight:600;font-size:21px;line-height:1.2;color:#fff">Urubici e Florianópolis</div>
<div class="b" style="left:0;top:1285px;width:640px;height:65px;background:${O}"></div>
<div class="b s" style="left:0;top:1295px;width:640px;font-size:34px;color:#fff;font-style:italic">Seu capital na expansão da Zion.</div>`],
// 03 · operação real (campeão 3): só o que tem prova (desde 2020, Urubici e Florianópolis)
[3,`<div class="b" style="left:0;top:0;width:514px;height:1350px;background:${Y}"></div>
<div class="b w" style="left:34px;width:446px;top:90px;font-size:30px;color:#fff;letter-spacing:.06em">Para investidores</div>
<div class="b s" style="left:40px;width:434px;top:160px;font-size:44px;color:#111;line-height:1.1">Uma operação real, não um projeto no papel.</div>
<div class="b s" style="left:30px;width:454px;top:420px;font-size:40px;color:#fff;letter-spacing:.1em">DESDE</div>
<div class="b s" style="left:30px;width:454px;top:466px;font-size:104px;color:#111;line-height:1">2020</div>
<div class="b" style="left:50px;width:414px;top:590px;text-align:center;font-family:A;font-weight:600;font-size:24px;line-height:1.2;color:#fff">Operação própria da Zion.</div>
<div class="b s" style="left:30px;width:454px;top:690px;font-size:48px;color:#111;line-height:1.12">URUBICI<br><span style="font-size:30px;color:#fff">E</span><br>FLORIANÓPOLIS</div>
<div class="b" style="left:50px;width:414px;top:880px;text-align:center;font-family:A;font-weight:600;font-size:24px;line-height:1.2;color:#fff">Santa Catarina</div>
<div class="b s" style="left:36px;width:442px;top:960px;height:215px;border-radius:34px;background:#000;color:#fff;font-size:34px;display:flex;align-items:center;justify-content:center;line-height:1.14;padding:0 26px">Você investe na expansão de uma operação que já existe.</div>
<div class="b" style="left:514px;top:0;width:566px;height:286px;background:#0c1608"></div><div class="b" style="left:514px;top:779px;width:566px;height:571px;background:#0c1608"></div>
<div class="b w" style="left:560px;width:470px;top:112px;font-size:30px;color:#fff;font-weight:500">Operação própria</div>
<div class="b s" style="left:560px;width:470px;top:880px;font-size:44px;color:#fff;text-align:left;line-height:1.12">INVESTIR NA EXPANSÃO DE UMA MARCA QUE JÁ OPERA.</div>`],
// 05 · indicadores (campeão 5): sem números no anúncio; os indicadores vão para a reunião
[5,`<div class="b" style="left:0;top:1102px;width:1080px;height:248px;background:${BE}"></div>
<div class="b w" style="left:60px;right:60px;top:1124px;font-size:36px;color:#232c0a;font-weight:700;line-height:1.08">Antes de investir, conheça a operação.</div>
<div class="b" style="left:90px;right:90px;top:1196px;text-align:center;font-family:A;font-weight:600;font-size:30px;line-height:1.25;color:#232c0a">Apresentamos os indicadores da operação na reunião com investidores.</div>
<div class="b" style="left:70px;right:70px;top:540px;text-align:center;font-family:A;font-weight:700;font-size:28px;line-height:1.5;letter-spacing:.08em;color:#fff;text-transform:uppercase;text-shadow:0 2px 10px rgba(0,0,0,.75)">Para investidores<br><span style="font-weight:600;font-size:24px;letter-spacing:.04em;text-transform:none;color:#fff">Os números são apresentados e analisados com você, na reunião.</span></div>`],
// 06 · o convite (campeão 6)
[6,`<div class="b" style="left:562px;top:0;width:518px;height:1350px;background:${Y}"></div>
<div class="b s" style="left:618px;width:400px;top:165px;height:815px;border-radius:44px;background:#000;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 30px;gap:34px"><div style="font-family:A;font-size:22px;font-weight:800;letter-spacing:.22em;color:#c9b37e">PARA INVESTIDORES</div><div style="font-size:50px;line-height:1.14">Invista capital na expansão da Zion.</div><div style="font-family:A;font-size:25px;line-height:1.25;font-weight:500;opacity:.92">Uma marca de glamping reconhecida, com operação própria.</div></div>
<div class="b s" style="left:595px;width:450px;top:1090px;font-size:34px;color:#fff;line-height:1.14">Conheça a proposta da Zion para investidores.</div>`],
// 07 · conversão (campeão 7). Aviso = TEXTO A VALIDAR COM ADVOGADO antes de veicular.
[7,`<div class="b" style="left:0;top:0;width:572px;height:1030px;background:${Y}"></div>
<div class="b s" style="left:30px;width:512px;top:64px;font-size:50px;font-weight:900;color:#0b0b0b;text-transform:uppercase;line-height:1.12">Seja um investidor na expansão da Zion.</div>
<div class="b s" style="left:40px;width:492px;top:330px;font-size:38px;color:#0b0b0b;line-height:1.14">Cadastre o seu interesse e receba a apresentação da Zion.</div>
<div class="b s" style="left:76px;width:424px;top:560px;height:220px;border-radius:52px;background:#ffed00;color:#0b0b0b;font-size:50px;display:flex;align-items:center;justify-content:center;line-height:1.04;letter-spacing:-.01em;padding:0 20px">QUERO SER INVESTIDOR.</div>
<div class="b" style="left:44px;top:830px;width:484px;text-align:center;font-family:A;font-weight:600;font-size:20px;line-height:1.3;color:#0b0b0b">Não é oferta pública de investimento.<br>Investimentos envolvem riscos.<br>A Zion avalia cada caso.</div>
<div class="b" style="left:30px;top:1080px;width:420px;height:150px;background:${Y}"></div>
<div class="b" style="left:30px;top:1090px;width:420px;font-family:A;font-weight:800;font-size:24px;letter-spacing:.14em;line-height:1.35;color:#fff">ZION HOTEL GROUP<br>INTERNATIONAL</div>`]];
// 04 · marca reconhecida, com prova (única composição nova): smartphone + print real do Instagram
const tela=temIG?`<img src="file://${IG}" style="width:100%;height:100%;object-fit:cover;object-position:top">`
 :`<div style="width:100%;height:100%;background:#1b1b1b;display:flex;align-items:center;justify-content:center;text-align:center;font-family:A;color:#c9b37e;font-size:25px;line-height:1.35;padding:30px;border:3px dashed #c9b37e">PRINT REAL DO INSTAGRAM<br>@zionbubble<br>A INSERIR<br><span style="font-size:19px;color:#ddd">pendente de Bruno</span></div>`;
const card4=`<div class="b" style="left:0;top:0;width:1080px;height:795px;background:rgba(10,20,8,.66)"></div>
<div class="b" style="left:445px;top:795px;width:635px;height:555px;background:${PU}"></div><div class="b" style="left:0;top:795px;width:445px;height:555px;background:${PU}"></div>
<div class="b" style="left:52px;top:300px;width:400px;height:800px;border-radius:64px;background:#0b0b0b;padding:14px;box-shadow:0 30px 70px rgba(0,0,0,.6);border:3px solid #3a3a3a"><div style="width:100%;height:100%;border-radius:50px;overflow:hidden;background:#000;position:relative">${tela}<div style="position:absolute;top:12px;left:50%;transform:translateX(-50%);width:110px;height:30px;border-radius:20px;background:#000"></div></div></div>
<div class="b" style="left:500px;top:84px;width:530px;font-family:A;font-weight:800;font-size:22px;letter-spacing:.24em;color:#c9b37e">PARA INVESTIDORES</div>
<div class="b s" style="left:500px;width:530px;top:128px;font-size:54px;font-weight:700;color:#fff;text-align:left;line-height:1.08">UMA MARCA DE GLAMPING RECONHECIDA.</div>
<div class="b s" style="left:500px;width:530px;top:420px;font-size:98px;font-weight:700;color:#c9b37e;text-align:left;line-height:.95">+266<br><span style="font-size:42px;letter-spacing:.05em;color:#fff">MIL SEGUIDORES</span></div>
<div class="b" style="left:500px;top:640px;width:530px;font-family:A;font-weight:600;font-size:27px;line-height:1.5;color:#fff">• Perfil Zion Bubble Glamping<br>• Operação própria desde 2020<br>• Urubici e Florianópolis</div>
<div class="b" style="left:480px;top:850px;width:560px;font-family:A;font-weight:600;font-size:25px;line-height:1.35;color:#0b0b0b">Você investe na expansão de uma marca que o público já conhece e acompanha.</div>
<div class="b" style="left:0;top:1160px;width:1080px;height:190px;background:${PU}"></div>
<div class="b s" style="left:60px;width:960px;top:1196px;font-size:40px;font-weight:700;color:#0b0b0b;text-transform:uppercase;line-height:1.12">Seu capital na expansão de uma marca reconhecida.</div>`;
cards.splice(3,0,[4,card4]);
(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const [n,html] of cards){const f=`${D}/_t.html`;
 fs.writeFileSync(f,`<!doctype html><meta charset=utf-8><style>${css}</style><body><img class="o" src="file://${BASE}/carrossel-c-card-${n}.png">${html}</body>`);
 await p.goto('file://'+f);if(html.includes('id="lua"'))await p.waitForFunction(()=>window.pronto===1);
 await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
 await p.screenshot({path:`${D}/card-${n}.jpg`,type:'jpeg',quality:90});}
fs.unlinkSync(`${D}/_t.html`);
// comparativo: antes (versão do último commit) × depois
const tmp=fs.mkdtempSync(path.join(require('os').tmpdir(),'zinv-'));let antes=[];
for(let n=1;n<=7;n++){try{execSync(`git -C "${R}" show HEAD:docs/ads/investidores-carrossel/card-${n}.jpg > "${tmp}/a${n}.jpg"`);antes.push(`file://${tmp}/a${n}.jpg`)}catch(e){antes.push('')}}
const fila=(t,arr)=>`<div style="font:600 22px sans-serif;color:#fff;margin:18px 20px 10px">${t}</div><div style="display:flex;gap:14px;padding:0 20px">${arr.map(s=>s?`<img src="${s}" style="width:300px;height:375px;object-fit:cover">`:`<div style="width:300px;height:375px;background:#333"></div>`).join('')}</div>`;
await p.setViewportSize({width:2224,height:900});
fs.writeFileSync(`${D}/_c.html`,`<!doctype html><meta charset=utf-8><body style="margin:0;background:#111;width:2224px;height:900px">${fila('ANTES (versão do último commit)',antes)}${fila('DEPOIS · v4 PARA INVESTIDORES (proposta, não publicada)',[1,2,3,4,5,6,7].map(n=>`file://${D}/card-${n}.jpg?${Date.now()}`))}</body>`);
await p.goto(`file://${D}/_c.html`);await p.waitForTimeout(600);
await p.screenshot({path:`${D}/comparativo.jpg`,type:'jpeg',quality:88});
fs.unlinkSync(`${D}/_c.html`);fs.rmSync(tmp,{recursive:true});await b.close();})();

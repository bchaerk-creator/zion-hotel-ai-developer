// Carrossel C de VENDA (Mini Mentoria de Estruturação Zion, R$ 47) a partir do gerador do campeão
// (docs/ads/inscricao-270/campeao-narrativa/build.js, NÃO alterado): mesmas imagens originais, mesmos
// blocos de cor, mesmas fontes, mesma posição. Só os textos mudam. Cartões 4 e 7 usam foto real sem pessoas
// (troca_fotos.py). Uso: SRC=<pasta com o1..o7.png originais> node build.js
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const D=__dirname, R=path.resolve(D,'../..');
const SRC=process.env.SRC||path.join(D,'src');
const css=`@font-face{font-family:P;src:url(file://${R}/trilha1/apresentacao/_motor/fonts/playfair-display-latin-wght-normal.woff2);font-weight:400 900}
@font-face{font-family:A;src:url(file://${R}/assets/fonts/aventa.woff2);font-weight:300 900}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;position:relative;overflow:hidden}
.o{position:absolute;inset:0;width:1080px;height:1350px}.b{position:absolute}
.w{font-family:A;font-weight:800;text-transform:uppercase;text-align:center;line-height:1.08;letter-spacing:.01em;transform:scaleX(1.12)}
.s{font-family:P;text-align:center;line-height:1.1}`;
const G='#133107',Y='#947620',O='#5a5529',PU='#8f688f',BE='#d5c1bc';
const cards=[
// 1 espelhamento (original 1): hook mantido
[`o1.png`,`<div class="b" style="left:0;top:0;width:1080px;height:400px;background:${G}"></div>
<div class="b" style="left:195px;top:60px;width:720px;height:70px;background:#fff;display:flex;align-items:center;justify-content:center;font-family:A;font-weight:800;font-size:38px;letter-spacing:.42em;color:#111;padding-left:.42em">TERRENO</div>
<div class="b w" style="left:90px;right:90px;top:168px;font-size:47px;color:#fff">Você tem um terreno em um destino <i>turístico</i>, mas não tem capital para desenvolver?</div>
<div class="b" style="left:0;top:1020px;width:1080px;height:330px;background:${G}"></div>
<div class="b s" style="left:65px;top:1080px;width:950px;height:122px;border-radius:26px;background:${Y};color:#fff;font-size:50px;display:flex;align-items:center;justify-content:center;letter-spacing:.01em">MINI MENTORIA ZION · R$ 47</div>
<div class="b w" style="left:60px;right:60px;top:1232px;font-size:31px;color:#fff;text-transform:none">Aprenda o passo a passo para estruturar o seu projeto</div>`],
// 2 confronto (original 2)
[`o2.png`,`<div class="b" style="left:430px;top:0;width:650px;height:236px;background:${O}"></div>
<div class="b w" style="left:470px;width:560px;top:40px;font-size:34px;color:#16210a">Seu terreno pode ter potencial turístico. Estruturar o projeto se aprende, passo a passo.</div>
<div class="b" style="left:40px;top:1310px;font-family:A;font-size:20px;color:#fff">Imagens ilustrativas</div>`],
// 3 reconhecimento (original 4)
[`o4.png`,`<div class="b" style="left:0;top:0;width:514px;height:1350px;background:${Y}"></div>
<div class="b w" style="left:40px;width:434px;top:100px;font-size:31px;color:#fff">Sem projeto, orçamento e estudo de viabilidade, fica mais difícil apresentar o terreno a potenciais parceiros e investidores</div>
<div class="b s" style="left:30px;width:454px;top:500px;font-size:56px;color:#fff;line-height:1.05">TERRENO +<br>PASSO A PASSO =<br><span style="color:#111;font-size:72px">PROJETO</span></div>
<div class="b s" style="left:30px;width:454px;top:790px;font-size:74px;color:#fff;letter-spacing:.02em">ZION</div>
<div class="b s" style="left:48px;width:424px;top:980px;height:175px;border-radius:34px;background:#000;color:#fff;font-size:52px;display:flex;align-items:center;justify-content:center;line-height:1.05">Mini Mentoria Zion</div>
<div class="b" style="left:514px;top:0;width:566px;height:340px;background:linear-gradient(180deg,#0c1608 84%,rgba(12,22,8,0))"></div>
<div class="b w" style="left:560px;width:470px;top:120px;font-size:30px;color:#fff;font-weight:500">Estruture o que você já tem</div>
<div class="b" style="left:514px;top:715px;width:566px;height:635px;background:linear-gradient(0deg,#0c1608 90%,rgba(12,22,8,0))"></div>
<div class="b s" style="left:560px;width:470px;top:900px;font-size:50px;color:#fff;text-align:left;line-height:1.1">AULAS, FICHAS &amp;<br>FERRAMENTAS</div>
<div class="b w" style="left:560px;width:470px;top:1100px;font-size:28px;color:#fff;font-weight:500;text-transform:none;line-height:1.25">Possibilidade de parcerias e investimento sujeita à análise de cada interessado. Sem garantia.</div>`],
// 4 autoridade (original 6, foto trocada por foto real sem pessoas)
[`o6.png`,`<div class="b" style="left:445px;top:795px;width:635px;height:555px;background:${PU}"></div><div class="b" style="left:150px;top:1160px;width:930px;height:190px;background:${PU}"></div>
<div class="b s" style="left:455px;width:590px;top:828px;font-size:46px;font-weight:900;color:#0b0b0b;text-transform:uppercase;line-height:1.06">Operamos hospedagens há mais de 20 anos</div>
<div class="b s" style="left:455px;width:590px;top:985px;font-size:30px;font-weight:700;color:#0b0b0b;text-transform:uppercase;line-height:1.1">e somos referência em glamping no Brasil</div>
<div class="b s" style="left:160px;width:880px;top:1120px;font-size:34px;color:#fff;line-height:1.18">Ao fazer a mentoria, você acessa a plataforma Zion, que faz parte da nossa expansão. E pode ser um próximo parceiro Zion a partir do resultado do seu projeto*</div>
<div class="b s" style="left:160px;width:880px;top:1290px;font-size:24px;color:#fff;line-height:1.1">*Possibilidade sujeita à análise, sem garantia de parceria ou investimento.</div>`],
// 5 oportunidade (original 5): o que recebe
[`o5.png`,`<div class="b" style="left:0;top:1102px;width:1080px;height:248px;background:${BE}"></div>
<div class="b w" style="left:60px;right:60px;top:1128px;font-size:40px;color:#232c0a;font-weight:500">9 módulos, 70 aulas e materiais</div>
<div class="b w" style="left:60px;right:60px;top:1228px;font-size:30px;color:#232c0a;font-weight:500">12 meses de acesso · pagamento único</div>`],
// 6 orientacao (original 3)
[`o3.png`,`<div class="b" style="left:562px;top:0;width:518px;height:1350px;background:${Y}"></div>
<div class="b s" style="left:618px;width:400px;top:165px;height:815px;border-radius:44px;background:#000;color:#fff;font-size:63px;display:flex;align-items:center;justify-content:center;line-height:1.16;padding:0 26px">Você não precisa começar construindo um hotel</div>
<div class="b s" style="left:590px;width:460px;top:1060px;font-size:40px;color:#fff;line-height:1.12">Aulas gravadas, fichas “Faça agora”, e-books por pilar, 2 planilhas em branco, Kit do Investidor e Dossiê em PDF</div>
<div class="b" style="left:562px;top:1318px;width:518px;height:30px;display:flex;align-items:center;justify-content:center;font-family:A;font-size:20px;color:#fff;background:transparent">Imagem ilustrativa</div>`],
// 7 conversao (original 7, foto trocada por foto real sem pessoas)
[`o7.png`,`<div class="b" style="left:0;top:0;width:572px;height:1030px;background:${Y}"></div>
<div class="b s" style="left:40px;width:492px;top:70px;font-size:46px;font-weight:900;color:#0b0b0b;text-transform:uppercase;line-height:1.08">Mini Mentoria de Estruturação Zion</div>
<div class="b s" style="left:40px;width:492px;top:330px;font-size:34px;color:#0b0b0b;line-height:1.12">Aprenda o passo a passo para estruturar o seu projeto</div>
<div class="b s" style="left:40px;width:492px;top:470px;font-size:96px;color:#0b0b0b;line-height:1">R$ 47</div>
<div class="b s" style="left:40px;width:492px;top:590px;font-size:30px;color:#0b0b0b;line-height:1.18">Pagamento único, sem mensalidade<br>Pix ou cartão · 12 meses de acesso<br>Garantia de 7 dias</div>
<div class="b s" style="left:46px;width:480px;top:790px;height:216px;border-radius:52px;background:#ffed00;color:#0b0b0b;font-size:44px;display:flex;align-items:center;justify-content:center;line-height:1.02;letter-spacing:-.01em;padding:0 22px;font-weight:700;text-transform:uppercase">Quero acessar a plataforma por R$47</div>`]];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(let i=0;i<cards.length;i++){const f=`${D}/_t.html`;fs.writeFileSync(f,`<!doctype html><meta charset=utf-8><style>${css}</style><body><img class="o" src="file://${SRC}/${cards[i][0]}">${cards[i][1]}</body>`);
 await p.goto('file://'+f);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);await p.screenshot({path:`${D}/carrossel-c-venda-${i+1}.png`});}
fs.unlinkSync(`${D}/_t.html`);await b.close();})();

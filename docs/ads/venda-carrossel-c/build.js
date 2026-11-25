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
<div class="b s" style="left:455px;width:600px;top:830px;font-size:37px;font-weight:900;color:#0b0b0b;text-transform:uppercase;line-height:1.06">Desenvolvemos projetos de hospedagem e turismo há mais de 20 anos</div>
<div class="b s" style="left:455px;width:590px;top:968px;font-size:30px;font-weight:700;color:#0b0b0b;text-transform:uppercase;line-height:1.1">e somos referência em glamping no Brasil</div>
<div class="b s" style="left:160px;width:880px;top:1120px;font-size:34px;color:#fff;line-height:1.18">Ao fazer a mentoria, você acessa a plataforma Zion, que faz parte da nossa expansão. E pode ser um próximo parceiro Zion a partir do resultado do seu projeto*</div>
<div class="b s" style="left:160px;width:880px;top:1290px;font-size:24px;color:#fff;line-height:1.1">*Possibilidade sujeita à análise, sem garantia de parceria ou investimento.</div>`],
// 4b gancho da plataforma (cartão extra, a pedido de Bruno): mesmo layout do cartão 4, outra foto real sem pessoas
[`o8.png`,`<div class="b" style="left:445px;top:795px;width:635px;height:555px;background:${PU}"></div><div class="b" style="left:150px;top:1160px;width:930px;height:190px;background:${PU}"></div>
<div class="b s" style="left:455px;width:600px;top:830px;font-size:44px;font-weight:900;color:#fff;text-transform:uppercase;line-height:1.06">Estruture o seu projeto e faça parte da nossa expansão*</div>
<div class="b s" style="left:455px;width:600px;top:1030px;font-size:28px;font-weight:700;color:#f6ecc4;text-transform:uppercase;line-height:1.1">Depois, a sessão de diagnóstico estratégico</div>
<div class="b s" style="left:160px;width:880px;top:1112px;font-size:30px;color:#fff;line-height:1.16">Ao concluir o Dossiê, você pode solicitar a sua sessão de diagnóstico estratégico com a nossa equipe: é a sua oportunidade de buscar parceiros e investimentos para tirar o plano do papel.</div>
<div class="b s" style="left:160px;width:880px;top:1290px;font-size:24px;color:#fff;line-height:1.1">*Sessão sujeita à análise e à agenda. Parceria e investimento não são garantidos.</div>`],
// 5 oportunidade (original 5): o que recebe
[`o5.png`,`<div class="b" style="left:0;top:1102px;width:1080px;height:248px;background:${BE}"></div>
<div class="b w" style="left:60px;right:60px;top:1128px;font-size:40px;color:#232c0a;font-weight:500">9 módulos, 70 aulas e materiais</div>
<div class="b w" style="left:60px;right:60px;top:1228px;font-size:30px;color:#232c0a;font-weight:500">12 meses de acesso · pagamento único</div>`],
// 6 orientacao (original 3)
[`o3.png`,`<div class="b" style="left:562px;top:0;width:518px;height:1350px;background:${Y}"></div>
<div class="b s" style="left:618px;width:400px;top:165px;height:815px;border-radius:44px;background:#000;color:#fff;font-size:63px;display:flex;align-items:center;justify-content:center;line-height:1.16;padding:0 26px">Você não precisa começar construindo um hotel</div>
<div class="b s" style="left:590px;width:460px;top:1060px;font-size:40px;color:#fff;line-height:1.12">Aulas gravadas, fichas “Faça agora”, e-books por pilar, 2 planilhas em branco, Kit do Investidor e Dossiê em PDF</div>
<div class="b" style="left:562px;top:1318px;width:518px;height:30px;display:flex;align-items:center;justify-content:center;font-family:A;font-size:20px;color:#fff;background:transparent">Imagem ilustrativa</div>`],
// 6b entregáveis claros (a pedido de Bruno): lista objetiva do que a pessoa recebe (redação segura da vistoria + sessão de diagnóstico estratégico)
[`o1.png`,`<div class="b" style="left:0;top:0;width:1080px;height:1350px;background:#0e1f09"></div>
<div class="b w" style="left:60px;right:60px;top:84px;font-size:52px;color:#e8d28a">O que você recebe</div>
<div class="b" style="left:70px;top:190px;width:940px;height:80px;background:#16300f;border-left:8px solid #e8d28a;border-radius:10px"></div><div class="b" style="left:104px;top:203px;font-family:A;font-weight:900;font-size:40px;color:#e8d28a">✔</div><div class="b" style="left:170px;width:830px;top:203px;font-family:A;font-weight:800;font-size:36px;color:#fff;line-height:1.1">9 módulos · 70 conteúdos</div>
<div class="b" style="left:70px;top:286px;width:940px;height:80px;background:#16300f;border-left:8px solid #e8d28a;border-radius:10px"></div><div class="b" style="left:104px;top:299px;font-family:A;font-weight:900;font-size:40px;color:#e8d28a">✔</div><div class="b" style="left:170px;width:830px;top:299px;font-family:A;font-weight:800;font-size:36px;color:#fff;line-height:1.1">Vídeo-aulas + 8 tutoriais em vídeo</div>
<div class="b" style="left:70px;top:382px;width:940px;height:80px;background:#16300f;border-left:8px solid #e8d28a;border-radius:10px"></div><div class="b" style="left:104px;top:395px;font-family:A;font-weight:900;font-size:40px;color:#e8d28a">✔</div><div class="b" style="left:170px;width:830px;top:395px;font-family:A;font-weight:800;font-size:36px;color:#fff;line-height:1.1">8 fichas interativas "Faça agora"</div>
<div class="b" style="left:70px;top:478px;width:940px;height:80px;background:#16300f;border-left:8px solid #e8d28a;border-radius:10px"></div><div class="b" style="left:104px;top:491px;font-family:A;font-weight:900;font-size:40px;color:#e8d28a">✔</div><div class="b" style="left:170px;width:830px;top:491px;font-family:A;font-weight:800;font-size:36px;color:#fff;line-height:1.1">8 e-books em PDF (um por pilar)</div>
<div class="b" style="left:70px;top:574px;width:940px;height:80px;background:#16300f;border-left:8px solid #e8d28a;border-radius:10px"></div><div class="b" style="left:104px;top:587px;font-family:A;font-weight:900;font-size:40px;color:#e8d28a">✔</div><div class="b" style="left:170px;width:830px;top:587px;font-family:A;font-weight:800;font-size:36px;color:#fff;line-height:1.1">2 planilhas de cálculo com fórmulas</div>
<div class="b" style="left:70px;top:670px;width:940px;height:80px;background:#16300f;border-left:8px solid #e8d28a;border-radius:10px"></div><div class="b" style="left:104px;top:683px;font-family:A;font-weight:900;font-size:40px;color:#e8d28a">✔</div><div class="b" style="left:170px;width:830px;top:683px;font-family:A;font-weight:800;font-size:36px;color:#fff;line-height:1.1">Kit do Investidor: guia das 6 peças</div>
<div class="b" style="left:70px;top:766px;width:940px;height:80px;background:#16300f;border-left:8px solid #e8d28a;border-radius:10px"></div><div class="b" style="left:104px;top:779px;font-family:A;font-weight:900;font-size:40px;color:#e8d28a">✔</div><div class="b" style="left:170px;width:830px;top:779px;font-family:A;font-weight:800;font-size:36px;color:#fff;line-height:1.1">9 comandos de IA prontos</div>
<div class="b" style="left:70px;top:862px;width:940px;height:80px;background:#16300f;border-left:8px solid #e8d28a;border-radius:10px"></div><div class="b" style="left:104px;top:875px;font-family:A;font-weight:900;font-size:40px;color:#e8d28a">✔</div><div class="b" style="left:170px;width:830px;top:875px;font-family:A;font-weight:800;font-size:36px;color:#fff;line-height:1.1">Seu Dossiê para baixar em PDF</div>
<div class="b" style="left:70px;top:958px;width:940px;height:80px;background:#2a3a10;border-left:8px solid #e8d28a;border-radius:10px"></div><div class="b" style="left:104px;top:971px;font-family:A;font-weight:900;font-size:40px;color:#e8d28a">✔</div><div class="b" style="left:170px;width:830px;top:971px;font-family:A;font-weight:800;font-size:36px;color:#fff;line-height:1.1">Sessão de diagnóstico estratégico*</div>
<div class="b s" style="left:60px;right:60px;top:1066px;font-size:54px;font-weight:900;color:#e8d28a">R$ 47 · pagamento único</div>
<div class="b s" style="left:60px;right:60px;top:1146px;font-size:28px;color:#fff;line-height:1.2">Pix ou cartão · 12 meses de acesso · garantia de 7 dias</div>
<div class="b s" style="left:60px;right:60px;top:1198px;font-size:22px;color:#fff;line-height:1.2">*Sessão gratuita ao concluir o Dossiê, mediante solicitação, sujeita à análise e à agenda. Parceria e investimento não são garantidos.</div>
<div class="b s" style="left:60px;right:60px;top:1288px;font-size:24px;color:#e8d28a">Mini Mentoria de Estruturação Zion · formação digital autônoma</div>`],
// 6c telas reais maiores (dossiê página a página)
[`o1.png`,`<div class="b" style="left:0;top:0;width:1080px;height:1350px;background:#0e1f09"></div>
<div class="b w" style="left:60px;right:60px;top:92px;font-size:46px;color:#e8d28a">Por dentro da plataforma</div>
<img class="b" src="file://${R}/zion-collection/club/telas/diagnostico.jpg" style="left:55px;top:210px;width:455px;height:800px;object-fit:cover;object-position:top;border-radius:20px;border:4px solid #e8d28a">
<img class="b" src="file://${R}/zion-collection/club/telas/previab.jpg" style="left:570px;top:210px;width:455px;height:800px;object-fit:cover;object-position:top;border-radius:20px;border:4px solid #e8d28a">
<div class="b s" style="left:55px;width:455px;top:1030px;font-size:30px;font-weight:700;color:#fff">Diagnóstico prévio</div>
<div class="b s" style="left:570px;width:455px;top:1030px;font-size:30px;font-weight:700;color:#fff">Pré-viabilidade</div>
<div class="b s" style="left:70px;right:70px;top:1115px;font-size:40px;font-weight:700;color:#fff;line-height:1.12">Cada ficha vira uma página do seu Dossiê de Desenvolvimento</div>
<div class="b s" style="left:70px;right:70px;top:1270px;font-size:24px;color:#e8d28a">Telas reais da plataforma Zion</div>`],
// 7 conversao (original 7, foto trocada por foto real sem pessoas)
[`o7.png`,`<div class="b" style="left:0;top:0;width:572px;height:1030px;background:${Y}"></div>
<div class="b s" style="left:40px;width:492px;top:70px;font-size:46px;font-weight:900;color:#0b0b0b;text-transform:uppercase;line-height:1.08">Mini Mentoria de Estruturação Zion</div>
<div class="b s" style="left:40px;width:492px;top:330px;font-size:34px;color:#0b0b0b;line-height:1.12">Aprenda o passo a passo para estruturar o seu projeto</div>
<div class="b s" style="left:40px;width:492px;top:470px;font-size:96px;color:#0b0b0b;line-height:1">R$ 47</div>
<div class="b s" style="left:40px;width:492px;top:590px;font-size:30px;color:#0b0b0b;line-height:1.18">Pagamento único, sem mensalidade<br>Pix ou cartão · 12 meses de acesso<br>Garantia de 7 dias</div>
<div class="b s" style="left:46px;width:480px;top:790px;height:216px;border-radius:52px;background:#ffed00;color:#0b0b0b;font-size:44px;display:flex;align-items:center;justify-content:center;line-height:1.02;letter-spacing:-.01em;padding:0 22px;font-weight:700;text-transform:uppercase">Quero acessar a plataforma por R$47</div>`]];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(let i=0;i<cards.length;i++){const f=`${D}/_t.html`;fs.writeFileSync(f,`<!doctype html><meta charset=utf-8><style>${css}</style><body><img class="o" src="file://${SRC}/${cards[i][0]}">${cards[i][1]}<div style="position:absolute;left:0;top:0;width:1080px;height:54px;background:#0b0b0b;color:#e8d28a;font-family:A;font-weight:800;font-size:24px;letter-spacing:.2em;display:flex;align-items:center;justify-content:center;text-transform:uppercase;z-index:9">Formação paga · Mini Mentoria Zion · R$ 47</div></body>`);
 await p.goto('file://'+f);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);await p.screenshot({path:`${D}/carrossel-c-venda-${i+1}.png`});}
fs.unlinkSync(`${D}/_t.html`);await b.close();})();

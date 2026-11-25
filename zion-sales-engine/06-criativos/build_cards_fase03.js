// ZION CREATIVE · Fase 03 · peças da Mini Mentoria (R$ 47) em 1080x1350.
// Regras: fundo sólido (musgo/creme), sem texto sobre foto, sem pessoas, telas reais da plataforma
// (docs/zion-collection/club/telas: aula, diagnostico, previab), logo oficial, Cormorant + Aventa.
// Uso: node build_cards_fase03.js [pasta de saída]   (padrão: docs/ads/mm47-fase03)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const R=path.resolve(__dirname,'../../docs');
const OUT=process.argv[2]||path.join(R,'ads/mm47-fase03');
const F=p=>'file://'+path.join(R,p);
const C={musgo:'#1B2117',preto:'#040605',creme:'#FEF5F0',areia:'#DED6BF',terra:'#8B714E',ouro:'#C9B37E'};
const FONT=`@font-face{font-family:Co;src:url(${F('assets/fonts/cormorant.woff2')});font-weight:300 900}
@font-face{font-family:Co;font-style:italic;src:url(${F('assets/fonts/cormorant-italic.woff2')});font-weight:300 900}
@font-face{font-family:Av;src:url(${F('assets/fonts/aventa.woff2')});font-weight:300 900}`;
const CSS=`${FONT}*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Av}
.b{position:absolute}.co{font-family:Co}.c{text-align:center}
.foot{position:absolute;left:0;top:1252px;width:1080px;height:98px;background:${C.preto};color:#e8dfc8;display:flex;align-items:center;justify-content:center;padding:0 48px;font-size:21px;line-height:1.3;text-align:center}
.cta{position:absolute;left:80px;width:920px;height:96px;border-radius:48px;background:${C.ouro};color:${C.preto};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:33px;letter-spacing:.02em;text-transform:uppercase}
.tag{position:absolute;right:80px;top:70px;height:48px;padding:0 24px;border-radius:24px;border:2px solid ${C.ouro};color:${C.ouro};display:flex;align-items:center;font-weight:700;font-size:19px;letter-spacing:.14em;text-transform:uppercase}
.frame{position:absolute;border-radius:28px;border:4px solid ${C.ouro};background-size:cover;background-position:top;background-repeat:no-repeat}`;
const DISC='Conteúdo digital, sem reunião nem atendimento individual. Não promete renda, parceria ou investimento; qualquer parceria é possibilidade sujeita à análise. R$ 47 · Pix ou cartão à vista · reembolso em 7 dias.';
const foot=()=>`<div class="foot">${DISC}</div>`;
const logo=(dark=true)=>`<img class="b" src="${F(dark?'brand/zion-logo-claro.png':'brand/zion-logo-escuro.png')}" style="left:80px;top:58px;width:230px">`;
const tag=()=>`<div class="tag">Mini Mentoria</div>`;
const bg=c=>`<div class="b" style="left:0;top:0;width:1080px;height:1252px;background:${c}"></div>`;
const cta=(y,t='Aprenda o passo a passo · R$ 47')=>`<div class="cta" style="top:${y}px">${t}</div>`;
const H=(t,top,size=92,col=C.creme,extra='')=>`<div class="b co" style="left:80px;right:80px;top:${top}px;font-size:${size}px;line-height:1.02;font-weight:600;color:${col};${extra}">${t}</div>`;
const T=(t,top,size=36,col=C.creme,extra='')=>`<div class="b" style="left:80px;right:80px;top:${top}px;font-size:${size}px;line-height:1.3;font-weight:500;color:${col};${extra}">${t}</div>`;
const TELA=n=>F(`zion-collection/club/telas/${n}.jpg`);
// tela real recortada no topo (moldura dourada)
const tela=(n,left,top,w,h)=>`<div class="frame" style="left:${left}px;top:${top}px;width:${w}px;height:${h}px;background-image:url(${TELA(n)});background-size:${w-8}px auto"></div>`;
const num=(n,top)=>`<div class="b" style="left:80px;top:${top}px;font-size:24px;letter-spacing:.2em;font-weight:800;color:${C.ouro}">${n}</div>`;

const P=[];
const add=(id,file,fmt,cards)=>P.push({id,file,fmt,cards});

// C03 · dor específica: custo escondido (texto vem da própria tela Raio-X do Marco Zero)
add('mm47f3-c03-custo-escondido','c03-custo-escondido','imagem',[
`${bg(C.musgo)}${logo()}${tag()}
${num('DOR ESPECÍFICA',200)}
${H('Você sabe o preço da cabana.<br><i style="color:'+C.ouro+'">Sabe quanto custa deixar tudo pronto?</i>',250,86)}
${T('Quando a conta começa, aparecem estrada, energia, fossa, projeto, taxas, móveis e enxoval.',620,38,C.areia)}
<div class="b" style="left:80px;top:760px;width:920px;height:250px;border-radius:26px;background:${C.creme};padding:34px 44px;color:${C.preto}">
<div style="font-size:21px;letter-spacing:.16em;font-weight:800;color:${C.terra}">NA MINI MENTORIA</div>
<div class="co" style="font-size:52px;line-height:1.08;font-weight:600;margin-top:12px">Aprenda o passo a passo para montar o orçamento de abertura e a pré-viabilidade do seu projeto.</div></div>
${T('Planilhas de cálculo em branco, para você preencher.',1030,28,C.areia)}
${cta(1110)}${foot()}`]);

// C06 · colapso de crença
add('mm47f3-c06-obra-ultimo-passo','c06-obra-ultimo-passo','imagem',[
`${bg(C.creme)}${logo(false)}<div class="tag" style="border-color:${C.terra};color:${C.terra}">Mini Mentoria</div>
${num('VOCÊ PODE ESTAR PENSANDO',200).replace(C.ouro,C.terra)}
<div class="b co" style="left:80px;right:80px;top:250px;font-size:70px;line-height:1.08;font-weight:500;color:${C.terra};font-style:italic">“Primeiro eu construo. Depois eu vejo se dá certo.”</div>
<div class="b" style="left:80px;top:470px;width:920px;height:6px;background:${C.ouro}"></div>
${H('Começar pela obra é começar pelo último passo.',510,100,C.musgo)}
${T('Antes de gastar com a obra, dá para organizar território, mercado, produto, modelo de negócio, masterplan e a conta do projeto.',900,35,C.preto)}
${cta(1120,'Estruture antes de construir · R$ 47').replace(C.ouro,C.musgo).replace(`color:${C.preto}`,`color:${C.creme}`)}${foot()}`]);

// C08 · oferta objetiva (com telas reais)
add('mm47f3-c08-oferta-47','c08-oferta-47','imagem',[
`${bg(C.musgo)}${logo()}${tag()}
${H('Mini Mentoria<br>de Estruturação',190,96)}
<div class="b co" style="left:80px;top:420px;font-size:200px;line-height:1;font-weight:700;color:${C.ouro}">R$ 47</div>
${T('pagamento único<br>Pix ou cartão à vista<br>reembolso em 7 dias',650,38,C.creme)}
${tela('aula',650,420,350,470)}
<div class="b" style="left:650px;top:900px;width:350px;font-size:20px;text-align:center;color:${C.areia}">Tela real da plataforma</div>
<div class="b" style="left:80px;top:940px;width:560px;font-size:30px;line-height:1.3;font-weight:700;color:${C.ouro}">9 módulos · 70 conteúdos<br>acesso à plataforma digital</div>
${T('Aulas gravadas, fichas “Faça agora”, e-books, planilhas em branco, modelos e Dossiê.',1030,26,C.areia,'right:380px')}
${cta(1142,'Aprenda o passo a passo · R$ 47')}${foot()}`]);

// C09 · quebra de objeções
const OBJ=[['É reunião ou consultoria?','Não. É acesso a uma plataforma, sem reunião e sem atendimento individual.'],
['Preciso ter o capital?','Não para começar a estruturar. O passo a passo começa pelo Marco Zero.'],
['E se eu não gostar?','Reembolso em 7 dias, como prevê o Código de Defesa do Consumidor.'],
['Garante parceria ou investimento?','Não. São possibilidades, sujeitas à análise, e não fazem parte do produto.']];
add('mm47f3-c09-objecoes','c09-objecoes','imagem',[
`${bg(C.musgo)}${logo()}${tag()}
${num('ANTES DE DECIDIR',190)}
${H('Quatro perguntas<br>honestas',232,78)}
${OBJ.map((o,i)=>`<div class="b" style="left:80px;top:${450+i*190}px;width:920px;height:170px;border-radius:22px;background:${C.creme};padding:22px 36px;color:${C.preto}">
<div class="co" style="font-size:40px;font-weight:700;color:${C.terra};line-height:1.05">${o[0]}</div>
<div style="font-size:27px;line-height:1.25;margin-top:8px;font-weight:500">${o[1]}</div></div>`).join('')}
<div class="b c" style="left:80px;right:80px;top:1210px;font-size:30px;font-weight:800;color:${C.ouro};letter-spacing:.03em;text-transform:uppercase">Mini Mentoria · R$ 47 · Aprenda o passo a passo</div>${foot()}`]);

// C10 · comparação de alternativas (abordagens, sem citar concorrente)
add('mm47f3-c10-obra-ou-estrutura','c10-obra-ou-estrutura','imagem',[
`${bg(C.musgo)}${logo()}${tag()}
${num('DUAS FORMAS DE COMEÇAR',190)}
${H('Obra primeiro<br>ou estrutura primeiro?',232,74)}
<div class="b" style="left:80px;top:470px;width:440px;height:520px;border-radius:26px;background:${C.preto};border:3px solid ${C.terra};padding:34px 32px;color:${C.creme}">
<div style="font-size:21px;letter-spacing:.16em;font-weight:800;color:${C.areia}">COMEÇAR PELA OBRA</div>
<div class="co" style="font-size:44px;line-height:1.1;font-weight:600;margin-top:22px">As dúvidas aparecem no meio do caminho.</div>
<div style="font-size:28px;line-height:1.3;margin-top:26px;color:${C.areia}">Custo, mercado e projeto são descobertos com a obra em andamento.</div></div>
<div class="b" style="left:560px;top:470px;width:440px;height:520px;border-radius:26px;background:${C.creme};border:3px solid ${C.ouro};padding:34px 32px;color:${C.preto}">
<div style="font-size:21px;letter-spacing:.16em;font-weight:800;color:${C.terra}">COMEÇAR PELA ESTRUTURA</div>
<div class="co" style="font-size:44px;line-height:1.1;font-weight:600;margin-top:22px">As perguntas são respondidas no papel.</div>
<div style="font-size:28px;line-height:1.3;margin-top:26px">Território, mercado, produto, modelo, masterplan e conta do projeto, antes de gastar com a obra.</div></div>
${T('A Mini Mentoria ensina a segunda forma, em sete pilares.',1040,32,C.ouro,'text-align:center;font-weight:700')}
<div class="b c" style="left:80px;right:80px;top:1130px;font-size:31px;font-weight:800;color:${C.creme};letter-spacing:.03em;text-transform:uppercase">Aprenda o passo a passo · R$ 47</div>${foot()}`]);

// C02 · demonstração real da plataforma (carrossel 5)
const dem=(n,kick,title,body,tl)=>`${bg(C.musgo)}${logo()}${tag()}
${num(kick,190)}${H(title,232,78)}${T(body,370,32,C.areia)}
${tela(tl,190,520,700,720)}`;
add('mm47f3-c02-plataforma-por-dentro','c02-plataforma','carrossel',[
`${bg(C.musgo)}${logo()}${tag()}
${num('DEMONSTRAÇÃO REAL',250)}
${H('Veja por dentro<br>da plataforma',300,112)}
${T('Capturas reais das telas que você usa na Mini Mentoria de Estruturação.',700,40,C.areia)}
${T('Deslize para ver',1030,30,C.ouro,'font-weight:800;letter-spacing:.1em;text-transform:uppercase')}${foot()}`,
dem(2,'1 · ONBOARDING E MARCO ZERO','Comece pela visão da jornada','Você sai sabendo onde está e por qual pilar começar.','aula')+foot(),
dem(3,'2 · FAÇA AGORA','O seu diagnóstico prévio','Em uns seis minutos, você vê onde está, o seu ponto mais frágil e a primeira ação.','diagnostico')+foot(),
dem(4,'3 · PILAR 6','A sua pré-viabilidade','Quanto custa abrir, quanto entra, quanto sobra e o tempo de volta, em três cenários.','previab')+foot(),
`${bg(C.musgo)}${logo()}${tag()}
${H('Mini Mentoria<br>de Estruturação',200,96)}
<div class="b co" style="left:80px;top:430px;font-size:190px;line-height:1;font-weight:700;color:${C.ouro}">R$ 47</div>
${T('pagamento único · Pix ou cartão à vista<br>reembolso em 7 dias · acesso à plataforma digital',660,36,C.creme)}
${T('9 módulos · 70 conteúdos: aulas gravadas, fichas “Faça agora”, e-books, planilhas em branco, kit do investidor (modelos) e Dossiê.',820,31,C.areia)}
${cta(1040,'Aprenda o passo a passo · R$ 47')}${foot()}`]);

// C04 · carrossel educativo/tutorial: a ordem certa (conteúdo da trilha da plataforma)
const edu=(k,t,b,extra='')=>`${bg(C.creme)}${logo(false)}<div class="tag" style="border-color:${C.terra};color:${C.terra}">Passo a passo</div>
${num(k,230).replace(C.ouro,C.terra)}${H(t,290,128,C.musgo)}<div class="b" style="left:80px;top:700px;width:920px;height:6px;background:${C.ouro}"></div>${T(b,750,46,C.preto)}${extra}${foot()}`;
add('mm47f3-c04-ordem-certa','c04-ordem-certa','carrossel',[
`${bg(C.musgo)}${logo()}${tag()}
${num('TUTORIAL',250)}
${H('A ordem certa para estruturar um empreendimento turístico',300,96)}
${T('Sete pilares, do chão ao capital. Deslize.',840,40,C.areia)}${foot()}`,
edu('0 · MARCO ZERO','Primeiro, onde você está','Antes dos pilares, um diagnóstico prévio mostra a sua situação, o ponto mais frágil e a primeira ação para os próximos sete dias.'),
edu('PILARES 1 A 3','Lugar, demanda e produto','Território e destino, mercado e demanda, produto e tipologias: definem o lugar, a demanda e o que você vai oferecer.'),
edu('PILARES 4 E 5','Dinheiro e espaço','Modelo de negócio e masterplan faseado: decidem como o projeto ganha dinheiro e onde fica cada coisa.'),
edu('PILARES 6 E 7','A conta e o Dossiê','Pré-viabilidade com planilhas para a conta completa. Depois, o Dossiê reúne tudo e organiza a decisão sobre capital.'),
`${bg(C.musgo)}${logo()}${tag()}
${H('Aprenda esse passo a passo na Mini Mentoria',200,92)}
<div class="b co" style="left:80px;top:560px;font-size:170px;line-height:1;font-weight:700;color:${C.ouro}">R$ 47</div>
${T('9 módulos · 70 conteúdos · acesso à plataforma digital<br>pagamento único · Pix ou cartão à vista · reembolso em 7 dias',760,32,C.creme)}
${cta(1010,'Aprenda o passo a passo · R$ 47')}${foot()}`]);

module.exports={P};
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
fs.mkdirSync(OUT,{recursive:true});const man=[];
for(const p of P){for(let i=0;i<p.cards.length;i++){
  const name=p.cards.length>1?`${p.file}-${i+1}.png`:`${p.file}.png`;const f=path.join(OUT,'_t.html');
  fs.writeFileSync(f,`<!doctype html><meta charset=utf-8><style>${CSS}</style><body>${p.cards[i]}</body>`);
  await pg.goto('file://'+f);await pg.waitForTimeout(300);await pg.screenshot({path:path.join(OUT,name)});fs.unlinkSync(f);man.push(name);}}
await b.close();console.log(man.join('\n'));})();

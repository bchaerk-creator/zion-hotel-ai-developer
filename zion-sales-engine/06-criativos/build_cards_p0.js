// ZION CREATIVE · P0 de coerência · versões v-P0 dos campeões e peças novas da Mini Mentoria Zion (R$ 47), 1080x1350.
// Regras: nenhum texto sobre foto (foto nítida em bloco próprio, texto em painel sólido); sem pessoas; só telas reais
// aula/diagnostico/previab (as telas raiox/implantacao mostram "Zion Collection Club" e não entram); logo oficial; Cormorant + Aventa.
// Uso: node build_cards_p0.js [pasta de saída]   (padrão: docs/ads/mm47-p0)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const R=path.resolve(__dirname,'../../docs');
const OUT=process.argv[2]||path.join(R,'ads/mm47-p0');
const F=p=>'file://'+path.join(R,p);
const C={musgo:'#1B2117',preto:'#040605',creme:'#FEF5F0',areia:'#DED6BF',terra:'#8B714E',ouro:'#C9B37E'};
const FONT=`@font-face{font-family:Co;src:url(${F('assets/fonts/cormorant.woff2')});font-weight:300 900}
@font-face{font-family:Co;font-style:italic;src:url(${F('assets/fonts/cormorant-italic.woff2')});font-weight:300 900}
@font-face{font-family:Av;src:url(${F('assets/fonts/aventa.woff2')});font-weight:300 900}`;
const CSS=`${FONT}*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Av}
.b{position:absolute}.co{font-family:Co}.c{text-align:center}
.foot{position:absolute;left:0;top:1252px;width:1080px;height:98px;background:${C.preto};color:#e8dfc8;display:flex;align-items:center;justify-content:center;padding:0 48px;font-size:21px;line-height:1.3;text-align:center}
.band{position:absolute;left:0;width:1080px;height:96px;background:${C.ouro};color:${C.preto};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:34px;letter-spacing:.02em;text-transform:uppercase}
.tag{position:absolute;right:80px;top:70px;height:48px;padding:0 24px;border-radius:24px;border:2px solid ${C.ouro};color:${C.ouro};display:flex;align-items:center;font-weight:700;font-size:19px;letter-spacing:.14em;text-transform:uppercase}
.frame{position:absolute;border-radius:28px;border:4px solid ${C.ouro};background-size:cover;background-position:top;background-repeat:no-repeat}
.ph{position:absolute;left:0;width:1080px;background-size:cover;background-repeat:no-repeat}
.li{display:flex;gap:24px;align-items:center;margin-top:22px}.ic{flex:0 0 60px;height:60px;border-radius:50%;background:${C.ouro};color:${C.preto};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:32px}`;
const DISC='Conteúdo digital, sem reunião nem atendimento individual. Não promete renda, parceria ou investimento. R$ 47 · pagamento único · Pix ou cartão à vista · reembolso em 7 dias.';
const DISCF='Fotos reais da Zion Bubble Glamping · Conteúdo digital, sem reunião · Sem promessa de renda, parceria ou investimento · R$ 47 · reembolso em 7 dias';
const foot=(t=DISC)=>`<div class="foot">${t}</div>`;
const logo=(dark=true,l=80,t=58,w=230)=>`<img class="b" src="${F(dark?'brand/zion-logo-claro.png':'brand/zion-logo-escuro.png')}" style="left:${l}px;top:${t}px;width:${w}px">`;
const tag=(t='Mini Mentoria',dark=true)=>`<div class="tag" ${dark?'':`style="border-color:${C.terra};color:${C.terra}"`}>${t}</div>`;
const bg=(c,h=1252)=>`<div class="b" style="left:0;top:0;width:1080px;height:${h}px;background:${c}"></div>`;
const band=(y,t='Acesse a plataforma por R$ 47',bgc=C.ouro,col=C.preto)=>`<div class="band" style="top:${y}px;background:${bgc};color:${col}">${t}</div>`;
const H=(t,top,size=92,col=C.creme,extra='')=>`<div class="b co" style="left:80px;right:80px;top:${top}px;font-size:${size}px;line-height:1.02;font-weight:600;color:${col};${extra}">${t}</div>`;
const T=(t,top,size=36,col=C.creme,extra='')=>`<div class="b" style="left:80px;right:80px;top:${top}px;font-size:${size}px;line-height:1.3;font-weight:500;color:${col};${extra}">${t}</div>`;
const num=(n,top,col=C.ouro)=>`<div class="b" style="left:80px;top:${top}px;font-size:24px;letter-spacing:.2em;font-weight:800;color:${col}">${n}</div>`;
const TELA=n=>F(`zion-collection/club/telas/${n}.jpg`);
const tela=(n,left,top,w,h)=>`<div class="frame" style="left:${left}px;top:${top}px;width:${w}px;height:${h}px;background-image:url(${TELA(n)});background-size:${w-8}px auto"></div>`;
const IMG=p=>F('assets/'+p);
const PHO=(p,pos,h)=>`<div class="ph" style="top:0;height:${h}px;background-image:url(${IMG(p)});background-position:${pos}"></div>`;
const PANEL=(top,col=C.musgo)=>`<div class="b" style="left:0;top:${top}px;width:1080px;height:${1252-top}px;background:${col};border-top:6px solid ${C.ouro}"></div>`;
const li=a=>a.map(t=>`<div class="li"><div class="ic">✓</div><b style="font-size:46px;font-weight:600;line-height:1.1;color:${C.creme}">${t}</b></div>`).join('');
// cartão "foto em cima + painel"; n/tot = contador
const PT=(n,tot,img,pos,ph,body,panel=C.musgo)=>`${bg(C.preto)}${PHO(img,pos,ph)}${PANEL(ph,panel)}${logo(true,72,ph+26,200)}<div class="b" style="right:72px;top:${ph+30}px;font-size:24px;color:${C.ouro};letter-spacing:.1em">${n}/${tot}</div><div class="b" style="left:72px;right:72px;top:${ph+100}px">${body}</div>${foot(DISCF)}`;
const K=t=>`<div style="font-size:25px;letter-spacing:.2em;text-transform:uppercase;font-weight:800;color:${C.ouro}">${t}</div>`;
const H1=(t,s=84)=>`<div class="co" style="font-size:${s}px;line-height:1.02;font-weight:600;color:${C.creme};margin-top:10px">${t}</div>`;
const S=(t,s=36)=>`<div style="font-size:${s}px;line-height:1.3;font-weight:500;color:${C.areia};margin-top:20px">${t}</div>`;
const em=t=>`<i style="color:${C.ouro}">${t}</i>`;
// cartão de oferta (último de cada carrossel). Faixa dourada reta, sem aparência de botão.
const OFERTA=(n,tot,img,pos,ph)=>PT(n,tot,img,pos,ph,`${K('Mini Mentoria de Estruturação Zion')}<div class="co" style="font-size:150px;line-height:1;font-weight:700;color:${C.ouro};margin-top:4px">R$ 47</div><div style="font-size:30px;line-height:1.3;color:${C.creme};margin-top:6px">pagamento único · 12 meses de acesso<br>Pix ou cartão à vista · reembolso em 7 dias</div><div style="font-size:30px;font-weight:700;color:${C.ouro};margin-top:18px">9 módulos · 70 aulas e materiais</div>`).replace(foot(DISCF),band(1156,'Acesse a plataforma por R$ 47')+foot(DISCF).replace('top:1252px;height:98px','top:1252px;height:98px'));

const P=[];const add=(id,file,fmt,cards,meta={})=>P.push({id,file,fmt,cards,...meta});

/* ===== v-P0 dos campeões ===== */
// A1 v2 · Dor direta (Curso Terreno): mesma ordem, foto em cima e painel musgo, fotos e hook preservados
add('vp0-a1-dor-direta','vp0-a1-dor-direta','carrossel',[
PT(1,5,'store/hero.webp','center 62%',780,`${K('Para quem tem terreno')}${H1('Tem terreno, '+em('mas não tem capital?'),76)}${S('Aprenda o passo a passo para estruturar o seu projeto antes de construir.',34)}`),
PT(2,5,'store/ceu.webp','center',640,`${H1('Terreno sem projeto '+em('é só terreno.'),86)}${S('Com projeto e números, você sabe o que apresentar a potenciais parceiros e investidores.',38)}`),
PT(3,5,'operacoes/op05.webp','center',640,`${H1('Você já tem a terra. '+em('Falta o passo a passo.'),86)}${S('Falta o conhecimento para transformá-la em projeto.',40)}`),
PT(4,5,'store/deck.webp','center',560,`${K('O que você vai aprender')}${li(['Analisar o território','Estudo de mercado','Orçamento do projeto','Montar o Dossiê do projeto'])}`),
OFERTA(5,5,'store/noturna.webp','center',470)]);
// A3 v2 · Saiba o custo
add('vp0-a3-saiba-o-custo','vp0-a3-saiba-o-custo','carrossel',[
PT(1,5,'store/hero.webp','center 62%',720,`${K('Antes de falar com um investidor')}${H1('Saiba quanto custa '+em('o seu projeto.'),82)}${S('Orçamento, mercado e território, no seu ritmo.',38)}`),
PT(2,5,'operacoes/op08.webp','center',640,`${H1('Sem números, '+em('é difícil apresentar o projeto.'),82)}${S('Aprenda a calcular o custo e a organizar tudo no Dossiê.',38)}`),
PT(3,5,'operacoes/op07.webp','center',560,`${K('Em três passos')}${li(['Analise o território','Estude o mercado','Monte o orçamento'])}`),
PT(4,5,'operacoes/op11.webp','center',640,`${H1('Você não precisa construir '+em('um hotel')+' para começar.',80)}${S('Descubra o que estruturar primeiro.',40)}`),
OFERTA(5,5,'store/noite.webp','center',470)]);
// Carrossel C campeão (narrativa nova): mesma ordem narrativa (dor, potencial, terreno+projeto, o que você tem, autoridade, não precisa construir, convite)
add('vp0-carrossel-c-narrativa','vp0-carrossel-c-narrativa','carrossel',[
PT(1,7,'operacoes/op08.webp','center',700,`${K('Terreno')}${H1('Você tem um terreno em um destino '+em('turístico')+', mas não tem capital para desenvolver?',70)}${S('Existe um primeiro passo que não exige obra: estruturar.',34)}`),
PT(2,7,'operacoes/op12.webp','center',640,`${H1('Seu terreno pode ter potencial turístico. '+em('Sozinho, isso não vira negócio.'),70)}${S('Falta transformar a vista bonita em projeto, números e conceito.',36)}`,C.preto),
`${bg(C.creme)}${logo(false)}${tag('Mini Mentoria',false)}${num('A EQUAÇÃO',210,C.terra)}
<div class="b co c" style="left:80px;right:80px;top:300px;font-size:120px;line-height:1.1;font-weight:600;color:${C.musgo}">Terreno<br><i style="color:${C.terra}">+ projeto</i><br>= destino</div>
${T('Sem projeto, orçamento e estudo de viabilidade, é mais difícil apresentar o seu terreno a potenciais parceiros e investidores.',860,38,C.preto,'text-align:center')}${foot(DISC)}`,
PT(4,7,'store/dentro.webp','center',540,`${K('Estruture o que você já tem')}${li(['Território e infraestrutura','Mercado e público','Orçamento do projeto','Pré-viabilidade e Dossiê'])}`),
PT(5,7,'store/noite.webp','center',640,`${K('De onde vem o método')}${H1('A Zion já opera hospedagens '+em('em Urubici e Florianópolis.'),72)}${S('A Mini Mentoria é o passo a passo que a Zion organizou para estruturar um empreendimento turístico.',33)}`),
PT(6,7,'operacoes/op09.webp','center',640,`${H1('Você não precisa começar '+em('construindo um hotel.'),84)}${S('Comece estruturando: dá para fazer isso no papel.',40)}`,C.preto),
OFERTA(7,7,'operacoes/op11.webp','center',470)]);

/* ===== peças novas (conceitos sem arte) ===== */
// N01 · Autoridade (bastidor documentado da operação)
add('mm47p0-n01-autoridade-operacao','n01-autoridade-operacao','imagem',[
`${bg(C.preto)}${PHO('operacoes/op12.webp','center',650)}${PANEL(650)}${logo(true,72,676,200)}
<div class="b" style="left:72px;right:72px;top:748px">${K('Autoridade · de onde vem o método')}${H1('A Zion opera hospedagens em '+em('Urubici e Florianópolis.'),68)}${S('A Mini Mentoria reúne, em passo a passo, a forma como estruturamos um empreendimento turístico. Formação digital, sem reunião.',31)}</div>
${band(1156,'Acesse a plataforma por R$ 47')}${foot(DISCF)}`],{conceito:'Autoridade (bastidor documentado)'});
// N02 · Passeio pelo Dossiê (carrossel 4): demonstração em tela real, layout lateral
const lat=(k,t,b,tl)=>`${bg(C.creme)}${logo(false)}${tag('Mini Mentoria',false)}${num(k,200,C.terra)}
${H(t,250,76,C.musgo,'right:470px')}${T(b,520,34,C.preto,'right:470px')}
${tela(tl,650,200,360,720)}<div class="b c" style="left:650px;width:360px;top:1000px;font-size:20px;color:${C.terra}">Tela real da plataforma</div>${foot()}`;
add('mm47p0-n02-dossie-passeio','n02-dossie-passeio','carrossel',[
`${bg(C.musgo)}${logo()}${tag()}${num('PASSEIO PELA PLATAFORMA',240)}${H('Cada ficha vira <i style="color:'+C.ouro+'">uma página do seu Dossiê.</i>',290,100)}${T('Veja, em três telas, como você aplica o passo a passo dentro da Mini Mentoria. Deslize.',760,38,C.areia)}${foot()}`,
lat('1 · VOCÊ PREENCHE A FICHA','O diagnóstico prévio','Em uns seis minutos, você vê onde está, o seu ponto mais frágil e a primeira ação.','diagnostico'),
lat('2 · A FICHA VIRA PÁGINA','A pré-viabilidade','Quanto custa abrir, quanto entra, quanto sobra e o tempo de volta, em três cenários.','previab'),
`${bg(C.musgo)}${logo()}${tag()}${H('No final, você gera o Dossiê em PDF.',200,92)}
<div class="b co" style="left:80px;top:520px;font-size:170px;line-height:1;font-weight:700;color:${C.ouro}">R$ 47</div>
${T('Mini Mentoria de Estruturação Zion<br>pagamento único · 12 meses de acesso<br>Pix ou cartão à vista · reembolso em 7 dias',730,34,C.creme)}${band(1010,'Acesse a plataforma por R$ 47')}${foot()}`],{conceito:'Demonstração / passeio pela plataforma (Dossiê)'});
// N03 · Exemplo resolvido com dados fictícios (no lugar de caso real: não há caso documentado)
const ROWS=[['Acesso e infraestrutura','R$ 40.000'],['Projeto e taxas','R$ 15.000'],['3 unidades','R$ 180.000'],['Mobiliário e enxoval','R$ 30.000'],['Imprevistos','R$ 20.000']];
add('mm47p0-n03-exemplo-ficticio','n03-exemplo-ficticio','imagem',[
`${bg(C.creme)}${logo(false)}${tag('Dados fictícios',false)}${num('EXEMPLO RESOLVIDO · PILAR 6',200,C.terra)}
${H('Como a conta do projeto <i style="color:'+C.terra+'">vira uma tabela.</i>',250,80,C.musgo)}
<div class="b" style="left:80px;top:520px;width:920px;border-radius:26px;background:${C.musgo};padding:26px 40px 20px">
${ROWS.map(r=>`<div style="display:flex;justify-content:space-between;font-size:34px;color:${C.creme};padding:15px 0;border-bottom:1px solid rgba(201,179,126,.35)"><span>${r[0]}</span><b style="color:${C.ouro}">${r[1]}</b></div>`).join('')}
<div style="display:flex;justify-content:space-between;font-size:38px;color:${C.creme};padding:20px 0 4px;font-weight:800"><span>Orçamento de abertura</span><b style="color:${C.ouro}">R$ 285.000</b></div></div>
${T('<b>Dados fictícios</b>, só para mostrar como a planilha em branco funciona. Não é referência de custo, de mercado nem resultado de aluno.',1010,26,C.terra)}
${band(1130,'Faça a sua conta · R$ 47',C.musgo,C.creme)}${foot()}`],{conceito:'Caso real: sem caso documentado; exemplo resolvido fictício rotulado'});
// N04 · Tutorial: 3 perguntas antes de gastar com a obra
add('mm47p0-n04-tres-perguntas','n04-tres-perguntas','imagem',[
`${bg(C.creme)}${logo(false)}${tag('Passo a passo',false)}${num('TESTE RÁPIDO',200,C.terra)}
${H('Responda antes de gastar com a obra:',250,84,C.musgo)}
${['Quanto custa deixar tudo pronto?','Quem é o hóspede e por que ele viria?','Quanto precisa entrar por mês para a conta fechar?'].map((q,i)=>`<div class="b" style="left:80px;top:${540+i*168}px;width:920px;height:146px;border-radius:24px;background:${C.musgo};display:flex;align-items:center;padding:0 36px;gap:30px"><div class="co" style="font-size:84px;font-weight:700;color:${C.ouro}">${i+1}</div><div class="co" style="font-size:44px;line-height:1.1;font-weight:600;color:${C.creme}">${q}</div></div>`).join('')}
${T('Travou em alguma? Aprenda o passo a passo para responder cada uma.',1060,28,C.preto)}
${band(1156,'Acesse a plataforma por R$ 47')}${foot()}`],{conceito:'Tutorial prático / dor específica'});
// N05 · Transformação (processo, nunca resultado externo)
add('mm47p0-n05-ponto-de-partida','n05-ponto-de-partida','imagem',[
`${bg(C.musgo)}${logo()}${tag()}${num('TRANSFORMAÇÃO DO CONHECIMENTO',200)}
${H('Do terreno e das dúvidas <i style="color:'+C.ouro+'">ao Dossiê organizado.</i>',250,80)}
<div class="b" style="left:80px;top:560px;width:410px;height:430px;border-radius:26px;background:${C.preto};border:3px solid ${C.terra};padding:30px 30px;color:${C.creme}"><div style="font-size:20px;letter-spacing:.16em;font-weight:800;color:${C.areia}">PONTO DE PARTIDA</div><div class="co" style="font-size:46px;line-height:1.1;font-weight:600;margin-top:20px">Um terreno, uma ideia e muitas dúvidas.</div><div style="font-size:26px;line-height:1.3;margin-top:18px;color:${C.areia}">Custo, mercado e projeto ainda soltos.</div></div>
<div class="b co c" style="left:490px;top:720px;width:100px;font-size:90px;color:${C.ouro}">→</div>
<div class="b" style="left:590px;top:560px;width:410px;height:430px;border-radius:26px;background:${C.creme};border:3px solid ${C.ouro};padding:30px 30px;color:${C.preto}"><div style="font-size:20px;letter-spacing:.16em;font-weight:800;color:${C.terra}">PONTO DE CHEGADA</div><div class="co" style="font-size:46px;line-height:1.1;font-weight:600;margin-top:20px">Um Dossiê em PDF com a sua estrutura.</div><div style="font-size:26px;line-height:1.3;margin-top:18px">Território, mercado, produto, modelo, masterplan e pré-viabilidade.</div></div>
${T('É a transformação do seu conhecimento e dos seus documentos. O resultado externo depende de você e do mercado.',1030,27,C.areia)}
${band(1130,'Acesse a plataforma por R$ 47')}${foot()}`],{conceito:'Transformação (processo)'});
// N06 · Entregáveis em números (verificados em ENTREGAVEIS_VERIFICADOS.md)
const GR=[['9','módulos'],['70','aulas e materiais'],['12','meses de acesso'],['10','fichas “Faça agora”'],['8','e-books por pilar'],['2','planilhas em branco'],['9','comandos de IA (kit de prompts)'],['8','tutoriais em vídeo das fichas'],['1','Dossiê em PDF']];
add('mm47p0-n06-entregaveis-numeros','n06-entregaveis-numeros','imagem',[
`${bg(C.musgo)}${logo()}${tag()}${H('O que vem dentro, <i style="color:'+C.ouro+'">em números.</i>',190,80)}
${GR.map((g,i)=>`<div class="b" style="left:${80+(i%3)*313}px;top:${380+Math.floor(i/3)*240}px;width:293px;height:222px;border-radius:24px;background:${i%2?C.preto:C.creme};padding:22px 24px;border:3px solid ${C.ouro}"><div class="co" style="font-size:100px;line-height:.95;font-weight:700;color:${i%2?C.ouro:C.terra}">${g[0]}</div><div style="font-size:27px;line-height:1.2;font-weight:700;margin-top:10px;color:${i%2?C.creme:C.preto}">${g[1]}</div></div>`).join('')}
${T('Formação digital · pagamento único · sem mensalidade',1110,27,C.areia,'text-align:center')}
${band(1156,'Acesse a plataforma por R$ 47')}${foot()}`],{conceito:'Demonstração dos entregáveis (oferta)'});
// N07 · Para quem é / para quem não é (filtro de curiosos)
add('mm47p0-n07-para-quem-e','n07-para-quem-e','imagem',[
`${bg(C.musgo)}${logo()}${tag()}${H('É para você? <i style="color:'+C.ouro+'">Seja direto.</i>',190,82)}
<div class="b" style="left:80px;top:420px;width:440px;height:600px;border-radius:26px;background:${C.creme};padding:30px 30px;color:${C.preto}"><div style="font-size:21px;letter-spacing:.16em;font-weight:800;color:${C.terra}">É PARA VOCÊ SE</div>
${['Tem um terreno ou uma ideia de empreendimento turístico.','Quer entender custo, mercado e produto antes de construir.','Topa estudar e preencher fichas no seu ritmo.'].map(t=>`<div class="co" style="font-size:38px;line-height:1.1;font-weight:600;margin-top:24px">${t}</div>`).join('')}</div>
<div class="b" style="left:560px;top:420px;width:440px;height:600px;border-radius:26px;background:${C.preto};border:3px solid ${C.terra};padding:30px 30px;color:${C.creme}"><div style="font-size:21px;letter-spacing:.16em;font-weight:800;color:${C.areia}">NÃO É PARA VOCÊ SE</div>
${['Espera reunião ou consultoria individual.','Espera garantia de parceria, investimento ou renda.','Quer tudo pronto, sem preencher nada.'].map(t=>`<div class="co" style="font-size:38px;line-height:1.1;font-weight:600;margin-top:24px">${t}</div>`).join('')}</div>
${T('É uma formação digital: aprenda o passo a passo e aplique no seu projeto.',1050,28,C.areia,'text-align:center')}
${band(1156,'Acesse a plataforma por R$ 47')}${foot()}`],{conceito:'Quebra de objeções / filtro de público'});

module.exports={P};
if(require.main===module)(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
fs.mkdirSync(OUT,{recursive:true});const man=[];
for(const p of P){for(let i=0;i<p.cards.length;i++){
  const name=p.cards.length>1?`${p.file}-${i+1}.jpg`:`${p.file}.jpg`;const f=path.join(OUT,'_t.html');
  fs.writeFileSync(f,`<!doctype html><meta charset=utf-8><style>${CSS}</style><body>${p.cards[i]}</body>`);
  await pg.goto('file://'+f);await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(400);await pg.screenshot({path:path.join(OUT,name),type:'jpeg',quality:90});fs.unlinkSync(f);man.push(name);}}
await b.close();console.log(man.join('\n'));})();

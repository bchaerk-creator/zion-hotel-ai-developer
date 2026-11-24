// Gerador dos 5 carrosséis LT47 (7 cards 1080x1350). Uso: node build_cards.js [pasta]
// Molde: carrossel campeão "Narrativa nova" (docs/ads/inscricao-270/campeao-narrativa): blocos de cor + foto,
// Aventa 800 em caixa alta, Playfair nos destaques, rótulos brancos, pílula preta, lua+estrela, CTA amarelo.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const R=path.resolve(__dirname,'../../../../docs');
const OUT=process.argv[2]||path.join(R,'ads/lt47');
const F=p=>'file://'+path.join(R,p);
const FONT=`@font-face{font-family:P;src:url(${F('trilha1/apresentacao/_motor/fonts/playfair-display-latin-wght-normal.woff2')});font-weight:400 900}
@font-face{font-family:P;font-style:italic;src:url(${F('trilha1/apresentacao/_motor/fonts/playfair-display-latin-wght-italic.woff2')});font-weight:400 900}
@font-face{font-family:A;src:url(${F('assets/fonts/aventa.woff2')});font-weight:300 900}`;
const C={musgo:'#1B2117',preto:'#040605',creme:'#FEF5F0',areia:'#DED6BF',terra:'#8B714E',ouro:'#C9B37E',ocre:'#947620',amar:'#ffed00'};
const DISC='Parcerias e investimentos são possibilidades, sujeitas à análise; o valor corresponde ao acesso à plataforma, não garante parceria ou investimento.';
const CSS=`${FONT}*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;position:relative;overflow:hidden;background:${C.preto};font-family:A;color:${C.creme}}
.b{position:absolute}.ph{position:absolute;background-size:cover;background-position:center}
.w{font-family:A;font-weight:800;text-transform:uppercase;text-align:center;line-height:1.1;letter-spacing:.01em}
.s{font-family:P;text-align:center;line-height:1.12}.t{font-family:A;text-align:center;line-height:1.28}
.pill{display:flex;align-items:center;justify-content:center;text-align:center}
.foot{position:absolute;left:0;top:1274px;width:1080px;height:76px;background:${C.preto};display:flex;align-items:center;justify-content:center;padding:0 40px;font-size:22px;line-height:1.25;text-align:center;color:#e8dfc8}`;
const STAR='<path d="M0,-1 C.09,-.22 .22,-.09 1,0 C.22,.09 .09,.22 0,1 C-.09,.22 -.22,.09 -1,0 C-.22,-.09 -.09,-.22 0,-1Z"/>';
const lua=(x,y,s,rot=0)=>`<svg class="b" style="left:${x}px;top:${y}px;width:${s}px;height:${s}px;transform:rotate(${rot}deg)" viewBox="0 0 200 200"><path d="M100 8A92 92 0 0 0 100 192A150 150 0 0 1 100 8Z" fill="#fff"/><g transform="translate(128 100) scale(24)" fill="#fff">${STAR}</g></svg>`;
const star=(s,col)=>`<svg width="${s}" height="${s}" viewBox="-1 -1 2 2" fill="${col}" style="flex:none">${STAR}</svg>`;
const img=p=>`url(${F(p)})`;
const OP=n=>`assets/operacoes/op${n}.webp`,ST=n=>`assets/store/${n}.webp`,CL=n=>`zion-collection/club/fotos/${n}.jpg`;
const TELA=n=>`zion-collection/club/telas/${n}.jpg`;
const LOGO=F('brand/zion-logo-claro.png');

const N={
'01-parceiro':{tag:'PARCEIRO ZION',c1:'Você tem o terreno. Nós podemos ser o seu parceiro.',btn:'CONHEÇA A PLATAFORMA',sub:'A Zion avalia cada projeto',
 ph:{p1:OP('08'),col:[OP('09'),OP('07'),OP('10')],p3:OP('12'),p4:ST('noturna'),p7:ST('hero')},
 c2:'Ter o terreno é um começo. Sozinho, ele ainda não é um projeto.',lab:['O TERRENO','A IDEIA','O PROJETO'],k2:'Falta estruturar.',
 c3a:'Você não precisa ter todo o capital para começar.',
 c4h:'A Zion pode ser a sua parceira',c4t:'Estamos em expansão e avaliamos cada projeto. Se fizer sentido, podemos conversar sobre parceria e conexão com investidores.',c4f:'Já operamos hospedagens em Urubici e Florianópolis'},
'02-capital':{tag:'CAPITAL',c1:'Tem um terreno, mas não tem capital para desenvolver?',btn:'CONHEÇA A PLATAFORMA',sub:'A Zion avalia cada projeto',
 ph:{p1:OP('11'),col:[OP('04'),OP('12'),OP('10')],p3:OP('05'),p4:ST('noite'),p7:CL('bolha-interior')},
 c2:'Sem projeto, orçamento e estudo de viabilidade, fica mais difícil conversar sobre capital.',lab:['PROJETO','ORÇAMENTO','VIABILIDADE'],k2:'Capital pede projeto.',
 c3a:'Você não precisa ter todo o capital para começar.',
 c4h:'Quem estrutura, apresenta melhor',c4t:'A Zion está em expansão. Se o seu projeto fizer sentido, podemos avaliar uma parceria ou conectar você a investidores.',c4f:'Uma possibilidade, sempre sujeita à análise'},
'03-patrimonio':{tag:'PATRIMÔNIO',c1:'E se a sua terra fosse a sua participação em um empreendimento?',btn:'CONHEÇA A PLATAFORMA',sub:'A Zion avalia cada projeto',
 ph:{p1:ST('deck'),col:[OP('08'),OP('05'),OP('11')],p3:ST('dentro'),p4:OP('09'),p7:CL('bolha-aerea')},
 c2:'Você olha para o terreno e vê o valor da terra. Falta transformá-lo em projeto.',lab:['A TERRA','O PROJETO','A PARTICIPAÇÃO'],k2:'Terra + projeto.',
 c3a:'Você não precisa ter todo o capital para começar.',
 c4h:'A terra pode entrar na conversa',c4t:'Em uma parceria, a terra pode ser a participação do proprietário. A Zion avalia cada caso, e o formato depende da análise.',c4f:'Possibilidade, não garantia'},
'04-expansao':{tag:'EXPANSÃO',c1:'Nosso próximo empreendimento pode nascer no seu terreno.',btn:'CONHEÇA A PLATAFORMA',sub:'A Zion avalia cada projeto',
 ph:{p1:OP('09'),col:[OP('12'),OP('04'),ST('dentro')],p3:OP('07'),p4:ST('ceu'),p7:OP('05')},
 c2:'Um bom terreno precisa chegar organizado a quem vai avaliá-lo.',lab:['LOCALIZAÇÃO','INFRAESTRUTURA','IDEIA'],k2:'Organize para apresentar.',
 c3a:'Você não precisa ter todo o capital para começar.',
 c4h:'A Zion está em expansão',c4t:'Já operamos hospedagens em Urubici e Florianópolis e olhamos novos projetos. Podemos ser parceiros ou apresentar o seu a investidores, se fizer sentido.',c4f:'Cada projeto passa por análise'},
'05-investidor':{tag:'INVESTIMENTOS',c1:'Quer encontrar um investidor para desenvolver seu terreno?',btn:'CONHEÇA A PLATAFORMA',sub:'A Zion avalia cada projeto',
 ph:{p1:OP('07'),col:[ST('noite'),OP('11'),OP('10')],p3:CL('bolha-interior'),p4:OP('08'),p7:ST('hero')},
 c2:'Quem pensa em investir quer entender o projeto, os números e o que já existe no terreno.',lab:['PROJETO','NÚMEROS','TERRENO'],k2:'Mostre com clareza.',
 c3a:'Você não precisa ter todo o capital para começar.',
 c4h:'Conexão com investidores',c4t:'Se o seu projeto fizer sentido, a Zion pode avaliá-lo e, a seu critério, conectá-lo a investidores. É uma possibilidade, sujeita à análise.',c4f:'Possibilidade, não garantia'}};

const foot=()=>`<div class="foot">${DISC}</div>`;
const cards=n=>{const d=N[n],p=d.ph;return[
// 1 desejo
`<div class="b" style="left:0;top:0;width:1080px;height:470px;background:${C.musgo}"></div>
<img class="b" src="${LOGO}" style="left:440px;top:34px;width:200px">
<div class="b pill" style="left:240px;top:118px;width:600px;height:62px;background:#fff;font-family:A;font-weight:800;font-size:32px;letter-spacing:.38em;color:#111;padding-left:.38em">${d.tag}</div>
<div class="b w" style="left:80px;right:80px;top:212px;font-size:49px;color:#fff;line-height:1.12">${d.c1}</div>
<div class="ph" style="left:0;top:470px;width:1080px;height:530px;background-image:${img(p.p1)}"></div>
<div class="b" style="left:0;top:1000px;width:1080px;height:274px;background:${C.musgo}"></div>
<div class="b s pill" style="left:75px;top:1036px;width:930px;height:112px;border-radius:26px;background:${C.ocre};color:#fff;font-size:50px;letter-spacing:.02em;font-weight:500">${d.btn}</div>
<div class="b t" style="left:80px;right:80px;top:1182px;font-size:32px;color:#fff;font-weight:500">${d.sub}</div>${foot()}`,
// 2 dor
`<div class="b" style="left:0;top:0;width:1080px;height:1274px;background:${C.musgo}"></div>
<div class="b w" style="left:70px;right:70px;top:70px;font-size:47px;color:${C.creme};line-height:1.14">${d.c2}</div>
<div class="ph" style="left:50px;top:340px;width:500px;height:640px;background-image:${img(p.col[0])}"></div>
<div class="ph" style="left:580px;top:340px;width:450px;height:310px;background-image:${img(p.col[1])}"></div>
<div class="ph" style="left:580px;top:670px;width:450px;height:310px;background-image:${img(p.col[2])}"></div>
<div class="b pill s" style="left:80px;top:884px;padding:0 26px;height:70px;border-radius:14px;background:#fff;color:#111;font-size:34px;font-weight:700">${d.lab[0]}</div>
<div class="b pill s" style="left:610px;top:566px;padding:0 24px;height:62px;border-radius:14px;background:#fff;color:#111;font-size:30px;font-weight:700">${d.lab[1]}</div>
<div class="b pill s" style="left:610px;top:886px;padding:0 24px;height:62px;border-radius:14px;background:#fff;color:#111;font-size:30px;font-weight:700">${d.lab[2]}</div>
${lua(440,520,150,0)}
<div class="b s" style="left:60px;right:60px;top:1060px;font-size:66px;color:${C.ouro};font-style:italic;font-weight:600">${d.k2}</div>${foot()}`,
// 3 crença
`<div class="ph" style="left:0;top:0;width:560px;height:1274px;background-image:${img(p.p3)}"></div>
<div class="b" style="left:560px;top:0;width:520px;height:1274px;background:${C.ocre}"></div>
${lua(-40,-20,260,20)}
<div class="b s pill" style="left:610px;top:130px;width:420px;height:760px;border-radius:44px;background:#000;color:#fff;font-size:56px;line-height:1.16;padding:0 30px">${d.c3a}</div>
<div class="b s" style="left:600px;width:440px;top:960px;font-size:50px;color:#fff;line-height:1.12;font-weight:600">Comece estruturando, não construindo.</div>${foot()}`,
// 4 Zion parceira
`<div class="ph" style="left:0;top:0;width:1080px;height:700px;background-image:${img(p.p4)}"></div>
${lua(-30,300,330,-10)}
<div class="b" style="left:0;top:700px;width:1080px;height:574px;background:${C.terra}"></div>
<div class="b s" style="left:60px;right:60px;top:740px;font-size:50px;font-weight:900;color:#111;text-transform:uppercase;line-height:1.08">${d.c4h}</div>
<div class="b t" style="left:80px;right:80px;top:880px;font-size:35px;color:#fff;font-weight:500">${d.c4t}</div>
<div class="b pill" style="left:120px;top:1150px;width:840px;height:80px;border-radius:40px;background:#000;font-family:A;font-weight:700;font-size:29px;color:#fff">${d.c4f}</div>${foot()}`,
// 5 plataforma (capturas reais)
`<div class="b" style="left:0;top:0;width:1080px;height:1274px;background:linear-gradient(180deg,#0c1608,${C.preto})"></div>
<img class="b" src="${LOGO}" style="left:450px;top:36px;width:180px">
<div class="b w" style="left:60px;right:60px;top:122px;font-size:30px;letter-spacing:.2em;color:${C.ouro};font-weight:700">A plataforma por dentro</div>
<div class="b s" style="left:50px;right:50px;top:176px;font-size:56px;font-weight:700;color:${C.creme}">Plataforma de Estruturação Zion Collection</div>
${['aula','diagnostico','previab'].map((t,i)=>`<div class="ph" style="left:${45+i*345}px;top:350px;width:300px;height:520px;border-radius:26px;border:3px solid ${C.ouro};background-image:${img(TELA(t))};background-position:top"></div>`).join('')}
${['Marco Zero','Diagnóstico prévio','Pré-viabilidade'].map((t,i)=>`<div class="b t" style="left:${45+i*345}px;width:300px;top:888px;font-size:27px;color:${C.ouro};font-weight:600">${t}</div>`).join('')}
<div class="b t" style="left:60px;right:60px;top:934px;font-size:22px;color:#b9b19a">Capturas reais da plataforma</div>
${[['Marco Zero e 7 pilares'],['Formação em vídeos e aulas'],['Ferramentas e formulários'],['Dossiê de Desenvolvimento']].map((t,i)=>`<div class="b" style="left:${60+(i%2)*500}px;top:${1000+Math.floor(i/2)*100}px;width:480px;height:80px;display:flex;align-items:center;gap:16px;font-size:30px;font-weight:600;color:${C.creme};line-height:1.15">${star(34,C.ouro)}<span style="color:${C.creme}">${t[0]}</span></div>`).join('')}${foot()}`,
// 6 jornada
`<div class="b" style="left:0;top:0;width:1080px;height:1274px;background:${C.ocre}"></div>
<div class="b w" style="left:70px;right:70px;top:80px;font-size:50px;color:#0b0b0b;font-weight:800">Da inscrição ao seu projeto apresentado</div>
<div class="b" style="left:127px;top:330px;width:5px;height:690px;background:#0b0b0b"></div>
${['Inscreva-se','Receba o acesso','Aprenda','Estruture','Apresente à Zion'].map((t,i)=>`<div class="b pill" style="left:92px;top:${300+i*172}px;width:75px;height:75px;border-radius:50%;background:#0b0b0b;color:#fff;font-family:P;font-size:38px">${i+1}</div><div class="b s" style="left:205px;top:${312+i*172}px;text-align:left;font-size:58px;color:#0b0b0b;font-weight:500">${t}</div>`).join('')}
<div class="b t" style="left:60px;right:60px;top:1190px;font-size:30px;color:#fff;font-weight:600">Cada projeto é avaliado. Sem garantias.</div>${foot()}`,
// 7 oferta
`<div class="b" style="left:0;top:0;width:590px;height:1020px;background:${C.ocre}"></div>
<div class="ph" style="left:590px;top:0;width:490px;height:1020px;background-image:${img(p.p7)}"></div>
${lua(500,780,250,200)}
<img class="b" src="${LOGO}" style="left:195px;top:44px;width:200px">
<div class="b s" style="left:40px;width:510px;top:150px;font-size:50px;font-weight:900;color:#0b0b0b;text-transform:uppercase;line-height:1.08">Acesso à plataforma</div>
<div class="b s" style="left:40px;width:510px;top:310px;font-size:140px;font-weight:800;color:#0b0b0b;line-height:1">R$ 47</div>
<div class="b w" style="left:40px;width:510px;top:468px;font-size:32px;color:#0b0b0b;font-weight:800">pagamento único</div>
<div class="b t" style="left:40px;width:510px;top:528px;font-size:29px;color:#fff;font-weight:600">Pix ou cartão à vista<br>Reembolso em 7 dias</div>
<div class="b s pill" style="left:50px;width:490px;top:660px;height:290px;border-radius:56px;background:${C.amar};color:#0b0b0b;font-size:56px;line-height:1.05;letter-spacing:-.01em;font-weight:700;padding:0 24px;text-transform:uppercase">Quero começar meu projeto</div>
<div class="b" style="left:0;top:1020px;width:1080px;height:330px;background:${C.preto}"></div>
<div class="b t" style="left:70px;right:70px;top:1062px;font-size:34px;color:${C.creme};font-weight:500;line-height:1.3">${DISC}</div>
<div class="b t" style="left:70px;right:70px;top:1262px;font-size:26px;color:${C.ouro};font-weight:600">A Zion avalia cada projeto.</div>`
];};

(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
for(const n of Object.keys(N)){fs.mkdirSync(path.join(OUT,n),{recursive:true});const cs=cards(n);
 for(let i=0;i<7;i++){const f=path.join(OUT,n,'_t.html');fs.writeFileSync(f,`<!doctype html><meta charset=utf-8><style>${CSS}</style><body>${cs[i]}</body>`);
  await pg.goto('file://'+f);await pg.waitForTimeout(250);await pg.screenshot({path:path.join(OUT,n,`card-0${i+1}.png`)});fs.unlinkSync(f);}}
await b.close();})();

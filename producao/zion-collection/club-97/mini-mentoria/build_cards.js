// Gerador dos 5 carrosséis MM47 (Mini Mentoria de Estruturação) (7 cards 1080x1350). Uso: node build_cards.js [pasta]
// Molde: carrossel campeão "Narrativa nova" (docs/ads/inscricao-270/campeao-narrativa): blocos de cor + foto,
// Aventa 800 em caixa alta, Playfair nos destaques, rótulos brancos, pílula preta, lua+estrela, CTA amarelo.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const R=path.resolve(__dirname,'../../../../docs');
const OUT=process.argv[2]||path.join(R,'ads/mm47');
const F=p=>'file://'+path.join(R,p);
const FONT=`@font-face{font-family:P;src:url(${F('trilha1/apresentacao/_motor/fonts/playfair-display-latin-wght-normal.woff2')});font-weight:400 900}
@font-face{font-family:P;font-style:italic;src:url(${F('trilha1/apresentacao/_motor/fonts/playfair-display-latin-wght-italic.woff2')});font-weight:400 900}
@font-face{font-family:A;src:url(${F('assets/fonts/aventa.woff2')});font-weight:300 900}`;
const C={musgo:'#1B2117',preto:'#040605',creme:'#FEF5F0',areia:'#DED6BF',terra:'#8B714E',ouro:'#C9B37E',ocre:'#947620',amar:'#ffed00'};
const DISC='Parcerias e investimentos são possibilidades, sujeitas à análise; o valor corresponde ao acesso ao conteúdo digital, não garante parceria ou investimento.';
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
'01-capital':{tag:'CAPITAL',c1:'Tenho terreno, mas não tenho capital.',
 ph:{p1:OP('11'),col:[OP('04'),OP('12'),OP('10')],p3:OP('05'),p4:ST('noite'),p7:CL('bolha-interior')},
 c2:'Sem projeto, orçamento e estudo de viabilidade, fica mais difícil conversar sobre capital.',lab:['PROJETO','ORÇAMENTO','VIABILIDADE'],k2:'Capital pede projeto.',
 c4h:'Quem estrutura, apresenta melhor',c4t:'A Zion está em expansão. Se o seu projeto fizer sentido, podemos avaliar uma parceria ou conectar você a investidores.',c4f:'Uma possibilidade, sempre sujeita à análise'},
'02-destino':{tag:'DESTINO',c1:'Transforme seu terreno em um destino turístico.',
 ph:{p1:ST('hero'),col:[OP('09'),OP('07'),OP('12')],p3:ST('deck'),p4:ST('ceu'),p7:OP('08')},
 c2:'Um terreno bonito ainda não é um destino. Antes, ele precisa de conceito e de projeto.',lab:['O TERRENO','O CONCEITO','O PROJETO'],k2:'Falta estruturar.',
 c4h:'A Zion pode ser a sua parceira',c4t:'Já operamos hospedagens em Urubici e Florianópolis e estamos em expansão. Avaliamos cada projeto e, se fizer sentido, podemos conversar sobre parceria.',c4f:'Já operamos hospedagens em Urubici e Florianópolis'},
'03-participacao':{tag:'PARTICIPAÇÃO',c1:'Sua terra pode ser sua participação.',
 ph:{p1:ST('deck'),col:[OP('08'),OP('05'),OP('11')],p3:ST('dentro'),p4:OP('09'),p7:CL('bolha-aerea')},
 c2:'Você olha para o terreno e vê o valor da terra. Falta transformá-lo em projeto.',lab:['A TERRA','O PROJETO','A PARTICIPAÇÃO'],k2:'Terra + projeto.',
 c4h:'A terra pode entrar na conversa',c4t:'Em uma parceria, a terra pode ser a participação do proprietário. A Zion avalia cada caso, e o formato depende da análise.',c4f:'Possibilidade, não garantia'},
'04-airbnb':{tag:'AIRBNB',c1:'Quero construir um Airbnb, mas não sei por onde começar.',
 ph:{p1:OP('04'),col:[OP('10'),OP('11'),OP('05')],p3:OP('07'),p4:OP('12'),p7:ST('noturna')},
 c2:'Antes de construir, é preciso saber o que construir, onde, para quem e se o projeto fecha as contas.',lab:['O CONCEITO','O PÚBLICO','AS CONTAS'],k2:'Comece pelo projeto.',
 c4h:'A Zion pode ser a sua parceira',c4t:'Já operamos hospedagens em Urubici e Florianópolis e estamos em expansão. Avaliamos cada projeto e, se fizer sentido, podemos conversar sobre parceria.',c4f:'Já operamos hospedagens em Urubici e Florianópolis'},
'05-parceiro':{tag:'PARCEIRO ZION',c1:'Seja um potencial parceiro Zion.',
 ph:{p1:OP('08'),col:[OP('09'),OP('07'),OP('10')],p3:OP('12'),p4:ST('noturna'),p7:ST('hero')},
 c2:'Ter o terreno é um começo. Sozinho, ele ainda não é um projeto.',lab:['O TERRENO','A IDEIA','O PROJETO'],k2:'Falta estruturar.',
 c4h:'A Zion pode ser a sua parceira',c4t:'Estamos em expansão e avaliamos cada projeto. Se fizer sentido, podemos conversar sobre parceria e conexão com investidores.',c4f:'Já operamos hospedagens em Urubici e Florianópolis'}};
for(const k in N)Object.assign(N[k],{c3a:'Você não precisa ter todo o capital para começar.',btn:'CONHEÇA A MENTORIA',sub:'Mini Mentoria de Estruturação'});

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
// 5 mentoria por dentro (capturas reais)
`<div class="b" style="left:0;top:0;width:1080px;height:1274px;background:linear-gradient(180deg,#0c1608,${C.preto})"></div>
<img class="b" src="${LOGO}" style="left:460px;top:30px;width:160px">
<div class="b w" style="left:60px;right:60px;top:108px;font-size:28px;letter-spacing:.2em;color:${C.ouro};font-weight:700">A mentoria por dentro</div>
<div class="b s" style="left:40px;right:40px;top:152px;font-size:56px;font-weight:700;color:${C.creme}">Mini Mentoria de Estruturação</div>
${['aula','diagnostico','previab'].map((t,i)=>`<div class="ph" style="left:${45+i*345}px;top:260px;width:300px;height:400px;border-radius:26px;border:3px solid ${C.ouro};background-image:${img(TELA(t))};background-position:top"></div>`).join('')}
${['Marco Zero','Diagnóstico prévio','Pré-viabilidade'].map((t,i)=>`<div class="b t" style="left:${45+i*345}px;width:300px;top:672px;font-size:26px;color:${C.ouro};font-weight:600">${t}</div>`).join('')}
<div class="b t" style="left:60px;right:60px;top:712px;font-size:21px;color:#b9b19a">Capturas reais da plataforma</div>
<div class="b w" style="left:60px;right:60px;top:768px;font-size:30px;letter-spacing:.12em;color:${C.creme};font-weight:700">O que você aprende</div>
${['Potencial territorial','Inteligência de mercado','Conceito do empreendimento','Estruturação do projeto','Viabilidade financeira','Preparação para potenciais investidores','Possibilidade de parceria com a Zion'].map((t,i)=>`<div class="b" style="left:${i==6?60:60+(i%2)*500}px;top:${830+Math.floor(i/2)*108}px;width:${i==6?960:470}px;height:96px;display:flex;align-items:center;gap:14px;font-size:28px;font-weight:600;color:${C.creme};line-height:1.15">${star(30,C.ouro)}<span style="color:${C.creme}">${t}</span></div>`).join('')}${foot()}`,
// 6 jornada
`<div class="b" style="left:0;top:0;width:1080px;height:1274px;background:${C.ocre}"></div>
<div class="b w" style="left:70px;right:70px;top:60px;font-size:48px;color:#0b0b0b;font-weight:800">Da inscrição ao seu projeto apresentado</div>
<div class="b" style="left:127px;top:290px;width:5px;height:700px;background:#0b0b0b"></div>
${['Inscreva-se','Receba o acesso','Aprenda','Estruture','Gere seu Dossiê','Apresente à Zion'].map((t,i)=>`<div class="b pill" style="left:92px;top:${262+i*138}px;width:75px;height:75px;border-radius:50%;background:#0b0b0b;color:#fff;font-family:P;font-size:38px">${i+1}</div><div class="b s" style="left:205px;top:${274+i*138}px;text-align:left;font-size:56px;color:#0b0b0b;font-weight:500">${t}</div>`).join('')}
<div class="b t" style="left:60px;right:60px;top:1150px;font-size:30px;color:#fff;font-weight:600">Cada projeto é avaliado. Sem garantias.</div>${foot()}`,
// 7 oferta
`<div class="b" style="left:0;top:0;width:590px;height:1020px;background:${C.ocre}"></div>
<div class="ph" style="left:590px;top:0;width:490px;height:1020px;background-image:${img(p.p7)}"></div>
${lua(500,780,250,200)}
<img class="b" src="${LOGO}" style="left:195px;top:44px;width:200px">
<div class="b s" style="left:40px;width:510px;top:140px;font-size:44px;font-weight:900;color:#0b0b0b;text-transform:uppercase;line-height:1.08">Mini Mentoria de Estruturação</div>
<div class="b s" style="left:40px;width:510px;top:330px;font-size:140px;font-weight:800;color:#0b0b0b;line-height:1">R$ 47</div>
<div class="b w" style="left:40px;width:510px;top:480px;font-size:32px;color:#0b0b0b;font-weight:800">pagamento único</div>
<div class="b t" style="left:40px;width:510px;top:535px;font-size:29px;color:#fff;font-weight:600">Pix ou cartão à vista<br>Reembolso em 7 dias</div>
<div class="b s pill" style="left:50px;width:490px;top:660px;height:290px;border-radius:56px;background:${C.amar};color:#0b0b0b;font-size:50px;line-height:1.05;letter-spacing:-.01em;font-weight:700;padding:0 24px;text-transform:uppercase">Quero transformar meu terreno</div>
<div class="b" style="left:0;top:1020px;width:1080px;height:330px;background:${C.preto}"></div>
<div class="b t" style="left:70px;right:70px;top:1062px;font-size:34px;color:${C.creme};font-weight:500;line-height:1.3">${DISC}</div>
<div class="b t" style="left:70px;right:70px;top:1262px;font-size:26px;color:${C.ouro};font-weight:600">A Zion está em expansão e avalia cada projeto.</div>`
];};

(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
for(const n of Object.keys(N)){fs.mkdirSync(path.join(OUT,n),{recursive:true});const cs=cards(n);
 for(let i=0;i<7;i++){const f=path.join(OUT,n,'_t.html');fs.writeFileSync(f,`<!doctype html><meta charset=utf-8><style>${CSS}</style><body>${cs[i]}</body>`);
  await pg.goto('file://'+f);await pg.waitForTimeout(250);await pg.screenshot({path:path.join(OUT,n,`card-0${i+1}.png`)});fs.unlinkSync(f);}}
await b.close();})();

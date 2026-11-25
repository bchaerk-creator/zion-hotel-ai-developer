// Gerador dos 7 carrosséis da Mini Mentoria de Performance Hoteleira (7 cards 1080x1350 cada = 49 copies do pacote). Uso: node build_cards.js [pasta]
// Molde: carrossel campeão "Narrativa nova" (docs/ads/inscricao-270/campeao-narrativa): blocos de cor + foto,
// Aventa 800 em caixa alta, Playfair nos destaques, rótulos brancos, pílula preta, lua+estrela, CTA amarelo.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const R=path.resolve(__dirname,'../../../docs');
const OUT=process.argv[2]||path.join(R,'ads/mm-performance');
const F=p=>'file://'+path.join(R,p);
const FONT=`@font-face{font-family:P;src:url(${F('trilha1/apresentacao/_motor/fonts/playfair-display-latin-wght-normal.woff2')});font-weight:400 900}
@font-face{font-family:P;font-style:italic;src:url(${F('trilha1/apresentacao/_motor/fonts/playfair-display-latin-wght-italic.woff2')});font-weight:400 900}
@font-face{font-family:A;src:url(${F('assets/fonts/aventa.woff2')});font-weight:300 900}`;
const C={musgo:'#1B2117',preto:'#040605',creme:'#FEF5F0',areia:'#DED6BF',terra:'#8B714E',ouro:'#C9B37E',ocre:'#947620',amar:'#ffed00'};
const DISC='Parcerias sujeitas à análise. Orientação baseada nos dados que você informar, sem garantia de reservas, ocupação, renda ou investimento. O valor refere-se ao acesso ao conteúdo digital.';
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
const TELA=n=>'../producao/mini-mentoria-performance/anuncios/telas/'+n+'.jpg';
const LOGO=F('brand/zion-logo-claro.png');


const OPf=OP,STf=ST;
const N={
'01-calendario':{tag:'CALENDÁRIO',c1:'Seu calendário de reservas não está cheio?',c2:'Você conhece o motivo da viagem do hóspede?',lab:['O MOTIVO','O PÚBLICO','A OFERTA'],k2:'Comece pelo dado.',c3:'Antes de investir mais, selecione cinco hospedagens da mesma região, capacidade e padrão; compare datas iguais.',c4h:'Ação possível',c4t:'Teste duas versões do título.',c4f:'Aprenda o passo a passo com a Zion',
 ph:{p1:ST('hero'),col:[OP('04'),OP('12'),OP('10')],p3:ST('deck'),p4:ST('noite'),p7:OP('08')}},
'02-erros':{tag:'AIRBNB',c1:'Os 7 erros que podem estar deixando seu Airbnb vazio.',c2:'Você registra noites disponíveis?',lab:['NOITES','BLOQUEIOS','OCUPAÇÃO'],k2:'Conte antes de agir.',c3:'Antes de investir mais, divida noites vendidas por disponíveis no mesmo período.',c4h:'Ação possível',c4t:'Planeje campanhas antes da baixa temporada.',c4f:'Aprenda o passo a passo com a Zion',
 ph:{p1:OP('04'),col:[OP('10'),OP('11'),OP('05')],p3:OP('07'),p4:OP('12'),p7:ST('noturna')}},
'03-concorrente':{tag:'PREÇO',c1:'Por que seu concorrente cobra mais?',c2:'Você mapeia a experiência completa?',lab:['A CHEGADA','A ESTADIA','O PÓS'],k2:'Veja como o hóspede vê.',c3:'Antes de investir mais, simule a chegada de um visitante sem conhecimento local.',c4h:'Ação possível',c4t:'Corrija falhas essenciais antes de adicionar luxo.',c4f:'Aprenda o passo a passo com a Zion',
 ph:{p1:OP('12'),col:[OP('09'),OP('07'),OP('10')],p3:ST('dentro'),p4:ST('hero'),p7:ST('deck')}},
'04-lucro':{tag:'MARGEM',c1:'Você fatura, mas não consegue lucrar?',c2:'Você separa hospedagem de extras?',lab:['RECEITA','CUSTOS','CONTRIBUIÇÃO'],k2:'Separe, some, concilie.',c3:'Antes de investir mais, liste aluguel, salários, sistemas e contratos.',c4h:'Ação possível',c4t:'Padronize unidades de cálculo.',c4f:'Aprenda o passo a passo com a Zion',
 ph:{p1:OP('08'),col:[OP('04'),OP('05'),OP('10')],p3:ST('noite'),p4:ST('ceu'),p7:ST('hero')}},
'05-capital':{tag:'OPERAÇÃO',c1:'Quer expandir, mas não tem capital?',c2:'Cada tarefa tem responsável?',lab:['TAREFAS','RESPONSÁVEIS','PADRÃO'],k2:'Organize antes de crescer.',c3:'Antes de investir mais, crie sequência por ambiente e inspeção final.',c4h:'Ação possível',c4t:'Elimine etapas redundantes.',c4f:'Aprenda o passo a passo com a Zion',
 ph:{p1:ST('deck'),col:[OP('08'),OP('05'),OP('11')],p3:OP('12'),p4:OP('09'),p7:ST('noturna')}},
'06-experiencia':{tag:'EXPANSÃO',c1:'Talvez não falte estrutura. Falte experiência.',c2:'Você conhece a infraestrutura disponível?',lab:['INFRAESTRUTURA','CAPACIDADE','CONSERVAÇÃO'],k2:'Inventarie o que já existe.',c3:'Antes de investir mais, reúna matrícula, levantamento e regras locais com especialistas.',c4h:'Ação possível',c4t:'Condicione investimento à viabilidade.',c4f:'Aprenda o passo a passo com a Zion',
 ph:{p1:ST('dentro'),col:[OP('09'),OP('07'),OP('12')],p3:ST('ceu'),p4:OP('04'),p7:OP('05')}},
'07-parceiro':{tag:'PARCERIA',c1:'Você tem um empreendimento turístico? Queremos conhecer você.',c2:'Você definiu o que busca em um parceiro?',lab:['CAPITAL','OPERAÇÃO','DISTRIBUIÇÃO'],k2:'Prepare seus números.',c3:'Antes de investir mais, liste propriedade, equipamentos, marca e operação com evidências.',c4h:'Ação possível',c4t:'Identifique lacunas antes de apresentar.',c4f:'Parcerias sujeitas à análise',
 ph:{p1:OP('08'),col:[OP('09'),OP('07'),OP('10')],p3:OP('12'),p4:ST('noturna'),p7:ST('hero')}}};
for(const k in N)Object.assign(N[k],{btn:'FAÇA SEU RAIO-X',sub:'Mini Mentoria de Performance Hoteleira'});
const ENT=[
{t:'7 aulas',d:'Uma aula por pilar da hospedagem',i:'<circle cx="24" cy="24" r="18"/><path d="M20 16l13 8-13 8z" fill="#111"/>'},
{t:'7 guias',d:'Passo a passo, exemplos e registro de trabalho',i:'<path d="M24 12c-5-4-12-4-16-3v27c4-1 11-1 16 3 5-4 12-4 16-3V9c-4-1-11-1-16 3zM24 12v27"/>'},
{t:'7 formulários',d:'70 perguntas com cobertura e "não sei"',i:'<rect x="9" y="7" width="30" height="34" rx="4"/><path d="M15 17l3 3 5-6M15 29l3 3 5-6M28 18h6M28 30h6"/>'},
{t:'7 calculadoras',d:'Ocupação, diária, margem, equilíbrio e mais',i:'<rect x="8" y="9" width="32" height="30" rx="3"/><path d="M8 19h32M8 29h32M20 9v30"/>'},
{t:'Diagnóstico Raio-X',d:'Nota por pilar, com a cobertura dos seus dados',i:'<circle cx="22" cy="22" r="13"/><path d="M32 32l9 9"/>'},
{t:'Plano e dossiê em PDF',d:'Plano de 7, 30, 60 e 90 dias para você ajustar',i:'<path d="M12 6h17l9 9v27H12z"/><path d="M29 6v9h9M18 25h14M18 32h14"/>'}];
const foot=()=>`<div class="foot">${DISC}</div>`;
const cards=n=>{const d=N[n],p=d.ph;const fs3=d.c3.length>100?44:d.c3.length>70?50:56;return[

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
<div class="b s pill" style="left:610px;top:130px;width:420px;height:760px;border-radius:44px;background:#000;color:#fff;font-size:${fs3}px;line-height:1.18;padding:0 36px">${d.c3}</div>
<div class="b s" style="left:600px;width:440px;top:960px;font-size:50px;color:#fff;line-height:1.12;font-weight:600">Dados antes de decisões.</div>${foot()}`,
// 4 Zion parceira
`<div class="ph" style="left:0;top:0;width:1080px;height:700px;background-image:${img(p.p4)}"></div>
${lua(-30,300,330,-10)}
<div class="b" style="left:0;top:700px;width:1080px;height:574px;background:${C.terra}"></div>
<div class="b s" style="left:60px;right:60px;top:748px;font-size:44px;letter-spacing:.14em;font-weight:900;color:#111;text-transform:uppercase;line-height:1.08">${d.c4h}</div>
<div class="b s" style="left:70px;right:70px;top:860px;font-size:58px;line-height:1.14;color:#fff;font-weight:600">${d.c4t}</div>
<div class="b pill" style="left:120px;top:1150px;width:840px;height:80px;border-radius:40px;background:#000;font-family:A;font-weight:700;font-size:29px;color:#fff">${d.c4f}</div>${foot()}`,
// 5 o que você recebe (entregáveis reais da turma + capturas reais)
`<div class="b" style="left:0;top:0;width:1080px;height:1274px;background:linear-gradient(180deg,#0c1608,${C.preto})"></div>
<img class="b" src="${LOGO}" style="left:470px;top:22px;width:140px">
<div class="b w" style="left:60px;right:60px;top:84px;font-size:24px;letter-spacing:.2em;color:${C.ouro};font-weight:700">Mini Mentoria de Performance Hoteleira</div>
<div class="b s" style="left:40px;right:40px;top:122px;font-size:62px;font-weight:700;color:${C.creme}">O que você recebe</div>
<div class="b pill" style="left:60px;top:208px;width:960px;height:54px;border-radius:27px;background:${C.ouro};color:#111;font-family:A;font-weight:800;font-size:24px;letter-spacing:.04em">7 AULAS · 7 GUIAS · 7 FORMULÁRIOS · 7 CALCULADORAS</div>
${['formulario','calculadora','plano'].map((t,i)=>`<div class="ph" style="left:${45+i*345}px;top:288px;width:300px;height:196px;border-radius:20px;border:3px solid ${C.ouro};background-image:${img(TELA(t))};background-position:top"></div>`).join('')}
<div class="b t" style="left:60px;right:60px;top:492px;font-size:20px;color:#b9b19a">Capturas reais da plataforma · exemplo com dados fictícios</div>
${ENT.map((e,i)=>`<div class="b" style="left:${45+(i%2)*500}px;top:${534+Math.floor(i/2)*242}px;width:490px;height:228px;border-radius:26px;background:${C.musgo};border:2px solid ${C.ouro}"></div>
<div class="b pill" style="left:${65+(i%2)*500}px;top:${554+Math.floor(i/2)*242}px;width:84px;height:84px;border-radius:50%;background:${C.ouro}"><svg width="48" height="48" viewBox="0 0 48 48" fill="none" stroke="#111" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">${e.i}</svg></div>
<div class="b" style="left:${165+(i%2)*500}px;width:350px;top:${556+Math.floor(i/2)*242}px;height:82px;display:flex;align-items:center;font-family:A;font-weight:800;font-size:29px;line-height:1.08;color:${C.ouro};text-transform:uppercase">${e.t}</div>
<div class="b" style="left:${65+(i%2)*500}px;width:450px;top:${656+Math.floor(i/2)*242}px;font-size:25px;line-height:1.25;color:${C.creme};font-weight:500">${e.d}</div>`).join('')}${foot()}`,
// 6 jornada
`<div class="b" style="left:0;top:0;width:1080px;height:1274px;background:${C.ocre}"></div>
<div class="b w" style="left:70px;right:70px;top:60px;font-size:48px;color:#0b0b0b;font-weight:800">Faça seu Raio-X e gere um plano de ação personalizado</div>
<div class="b" style="left:127px;top:290px;width:5px;height:700px;background:#0b0b0b"></div>
${['Acesse a plataforma','Aprenda','Responda','Calcule','Veja seu diagnóstico','Gere seu plano'].map((t,i)=>`<div class="b pill" style="left:92px;top:${262+i*138}px;width:75px;height:75px;border-radius:50%;background:#0b0b0b;color:#fff;font-family:P;font-size:38px">${i+1}</div><div class="b s" style="left:205px;top:${274+i*138}px;text-align:left;font-size:56px;color:#0b0b0b;font-weight:500">${t}</div>`).join('')}
<div class="b t" style="left:60px;right:60px;top:1150px;font-size:30px;color:#fff;font-weight:600">Orientação baseada nos seus dados. Sem garantias.</div>${foot()}`,
// 7 oferta
`<div class="b" style="left:0;top:0;width:590px;height:1020px;background:${C.ocre}"></div>
<div class="ph" style="left:590px;top:0;width:490px;height:1020px;background-image:${img(p.p7)}"></div>
${lua(500,780,250,200)}
<img class="b" src="${LOGO}" style="left:195px;top:44px;width:200px">
<div class="b s" style="left:40px;width:510px;top:140px;font-size:38px;font-weight:900;color:#0b0b0b;text-transform:uppercase;line-height:1.08">Mini Mentoria de Performance Hoteleira</div>
<div class="b s" style="left:40px;width:510px;top:330px;font-size:140px;font-weight:800;color:#0b0b0b;line-height:1">R$ 47</div>
<div class="b w" style="left:40px;width:510px;top:500px;font-size:32px;color:#0b0b0b;font-weight:800">pagamento único</div>
<div class="b t" style="left:40px;width:510px;top:552px;font-size:29px;color:#fff;font-weight:600">Pix ou cartão à vista<br>Reembolso em 7 dias</div>
<div class="b s pill" style="left:50px;width:490px;top:660px;height:290px;border-radius:56px;background:${C.amar};color:#0b0b0b;font-size:50px;line-height:1.05;letter-spacing:-.01em;font-weight:700;padding:0 24px;text-transform:uppercase">Faça seu diagnóstico</div>
<div class="b" style="left:0;top:1020px;width:1080px;height:330px;background:${C.preto}"></div>
<div class="b t" style="left:70px;right:70px;top:1048px;font-size:26px;color:${C.creme};font-weight:500;line-height:1.3">${DISC}</div>
<div class="b t" style="left:50px;right:50px;top:1180px;font-size:25px;color:${C.ouro};font-weight:700">7 aulas, 7 guias, 7 formulários, 7 calculadoras, diagnóstico e dossiê</div>
<div class="b t" style="left:70px;right:70px;top:1262px;font-size:26px;color:${C.creme};font-weight:600">Acesso completo · sem reunião obrigatória</div>`
];};

(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
for(const n of Object.keys(N)){fs.mkdirSync(path.join(OUT,n),{recursive:true});const cs=cards(n);
 for(let i=0;i<7;i++){const f=path.join(OUT,n,'_t.html');fs.writeFileSync(f,`<!doctype html><meta charset=utf-8><style>${CSS}</style><body>${cs[i]}</body>`);
  await pg.goto('file://'+f);await pg.waitForTimeout(250);await pg.screenshot({path:path.join(OUT,n,`card-0${i+1}.png`)});fs.unlinkSync(f);}}
await b.close();})();

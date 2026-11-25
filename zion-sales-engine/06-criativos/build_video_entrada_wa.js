// ZION CREATIVE · Entrada por WhatsApp · vídeos 01 e 02 SEM áudio, SEM preço, SEM promessa: só "queremos te conhecer" + "converse com a equipe pelo WhatsApp".
// Reaproveita o b-roll (sem pessoas) das cenas já geradas por build_video_captacao.js (corta o painel antigo, põe painel novo). Não altera nenhum vídeo-fonte.
// Uso: node build_video_entrada_wa.js <pasta _cenas de build_video_captacao> <pasta-de-saida>   (requer ffmpeg e playwright)
// Variante A = ordem literal de Bruno (não menciona formação). Variante B = recomendada (uma linha avisa que a equipe apresenta uma formação paga, sem preço).
const {chromium}=require('playwright');const {execFileSync}=require('child_process');const fs=require('fs');const path=require('path');
const SRC=process.argv[2],OUT=process.argv[3];if(!SRC||!OUT){console.error('uso: node build_video_entrada_wa.js <_cenas> <saida>');process.exit(1)}
const R=path.resolve(__dirname,'../../docs');const F=p=>'file://'+path.join(R,p);
const C={musgo:'#1B2117',preto:'#040605',creme:'#FEF5F0',areia:'#DED6BF',ouro:'#C9B37E'};
const CSS=`@font-face{font-family:Co;src:url(${F('assets/fonts/cormorant.woff2')});font-weight:300 900}
@font-face{font-family:Av;src:url(${F('assets/fonts/aventa.woff2')});font-weight:300 900}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Av}
.pn{position:absolute;left:0;top:1344px;width:1080px;height:576px;background:${C.musgo};border-top:6px solid ${C.ouro};padding:44px 64px}
.k{font-size:24px;letter-spacing:.2em;text-transform:uppercase;font-weight:800;color:${C.ouro}}
.t{font-family:Co;font-size:70px;line-height:1.05;font-weight:600;color:${C.creme};margin-top:14px}.t i{color:${C.ouro}}
.s{font-size:30px;line-height:1.3;color:${C.areia};margin-top:16px}
.lg{position:absolute;left:64px;top:1840px;width:170px}.fd{position:absolute;right:64px;top:1858px;font-size:20px;color:${C.areia}}`;
const LOGO=`<img class="lg" src="${F('brand/zion-logo-claro.png')}">`;
const panel=(k,t,s,fd='Zion · educação para projetos turísticos')=>`<div class="pn"><div class="k">${k}</div><div class="t">${t}</div><div class="s">${s}</div></div>${LOGO}<div class="fd">${fd}</div>`;
const fim=(sub)=>`<div style="position:absolute;inset:0;background:${C.musgo}"></div><img src="${F('brand/zion-logo-claro.png')}" style="position:absolute;left:64px;top:90px;width:260px">
 <div style="position:absolute;left:64px;right:64px;top:360px"><div class="k">Zion · educação para projetos turísticos</div><div style="font-family:Co;font-size:200px;line-height:.95;font-weight:700;color:${C.ouro};margin-top:14px">Queremos te conhecer</div>
 <div style="font-size:48px;line-height:1.3;color:${C.creme};margin-top:40px">${sub}</div>
 <div style="font-size:30px;line-height:1.35;color:${C.areia};margin-top:44px">Sem promessa de investimento, parceria ou renda.</div></div>
 <div style="position:absolute;left:0;top:1560px;width:1080px;height:130px;background:${C.ouro};color:${C.preto};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:38px">Converse com a equipe pelo WhatsApp</div>`;
const SUBB='Converse com a equipe pelo WhatsApp. A equipe também apresenta uma formação digital paga da Zion, se você quiser conhecer.';
const SUBA='Converse com a equipe pelo WhatsApp.';
const V02=(v)=>[
 {n:0,html:panel('Dono de terreno','Ei, <i>dono de terreno!</i>','Você tem um terreno e ainda não sabe por onde começar?')},
 {n:1,html:panel('O primeiro passo','Antes do capital, <i>vem o projeto.</i>','Estruturar no papel é o primeiro passo e não exige obra.')},
 {n:2,html:panel('De onde vem','A Zion opera hospedagens <i>em Urubici e Florianópolis.</i>','Conhecemos esse caminho por dentro.')},
 {n:3,html:panel('Um convite','Queremos <i>conhecer</i> você, dono de terreno.','Conte quem você é e o que tem em mente.')},
 {n:4,html:panel('WhatsApp','Toque em <i>Enviar mensagem.</i>',v==='B'?'A equipe responde por lá e explica como a Zion pode ajudar, inclusive com uma formação paga.':'A equipe responde por lá.')},
 {tp:'fim',d:8,html:fim(v==='B'?SUBB:SUBA)}];
const V01=(v)=>[
 {n:0,html:panel('Terreno','Terreno parado há tanto tempo, <i>sem saber por onde começar?</i>','Você não precisa começar construindo um hotel.')},
 {n:1,html:panel('O primeiro passo','Dá para <i>estruturar o projeto no papel</i> antes da obra.','Território, mercado, orçamento e pré-viabilidade.')},
 {n:2,html:panel('De onde vem','A Zion opera hospedagens <i>em Urubici e Florianópolis.</i>','Conhecemos esse caminho por dentro.')},
 {n:3,html:panel('Um convite','Queremos <i>conhecer</i> você, dono de terreno.','Conte quem você é e o que tem em mente.')},
 {n:5,html:panel('WhatsApp','Toque em <i>Enviar mensagem.</i>',v==='B'?'A equipe responde por lá e explica como a Zion pode ajudar, inclusive com uma formação paga.':'A equipe responde por lá.')},
 {tp:'fim',d:8,html:fim(v==='B'?SUBB:SUBA)}];
async function build(S,pref,name,pg,T){const clips=[];
for(let i=0;i<S.length;i++){const s=S[i];const hf=path.join(T,`${name}-c${i}.html`);
 fs.writeFileSync(hf,`<!doctype html><meta charset=utf-8><style>${CSS}</style><body>${s.html}</body>`);await pg.goto('file://'+hf);await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(300);
 const png=path.join(T,`${name}-c${i}.png`);await pg.screenshot({path:png,omitBackground:s.tp!=='fim'});const mp=path.join(T,`${name}-c${i}.mp4`);
 const enc=['-c:v','libx264','-pix_fmt','yuv420p','-crf','28','-preset','medium','-r','30','-an','-movflags','+faststart'];
 if(s.tp==='fim')execFileSync('ffmpeg',['-v','error','-y','-loop','1','-t',String(s.d),'-i',png,...enc,mp]);
 else execFileSync('ffmpeg',['-v','error','-y','-i',path.join(SRC,`${pref}-c${s.n}.mp4`),'-loop','1','-i',png,'-filter_complex','[0:v]crop=1080:1344:0:0,pad=1080:1920:0:0:color=0x040605[v];[v][1:v]overlay=0:0:shortest=1,format=yuv420p',...enc,mp]);
 clips.push(mp);}
fs.writeFileSync(path.join(T,`${name}-lista.txt`),clips.map(c=>`file '${c}'`).join('\n'));
execFileSync('ffmpeg',['-v','error','-y','-f','concat','-safe','0','-i',path.join(T,`${name}-lista.txt`),'-c','copy',path.join(OUT,`${name}.mp4`)]);}
(async()=>{fs.mkdirSync(OUT,{recursive:true});const T=path.join(OUT,'_cenas');fs.mkdirSync(T,{recursive:true});
const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
for(const v of ['A','B']){await build(V02(v),'capt-v02-dono-terreno-sem-audio',`entrada-wa-v02-dono-terreno-${v}-sem-audio`,pg,T);await build(V01(v),'capt-v01-terreno-capital-sem-audio',`entrada-wa-v01-terreno-capital-${v}-sem-audio`,pg,T);}
await b.close();console.log('ok');})();

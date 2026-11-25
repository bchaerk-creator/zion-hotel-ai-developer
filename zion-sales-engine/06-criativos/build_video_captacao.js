// ZION CREATIVE · Captação corrigida · vídeos 01 e 02 v-captação (SEM áudio original, SEM voz sintética): imagens reais da Zion (corte da parte de cima do vídeo-fonte,
// que exclui as legendas antigas e a cena com pessoa) + telas reais da plataforma + cartelas novas. Não altera o vídeo-fonte.
// Uso: node build_video_captacao.js <video-fonte-dono-de-terras.mp4> <pasta-de-saida>      (requer ffmpeg e playwright)
const {chromium}=require('playwright');const {execFileSync}=require('child_process');const fs=require('fs');const path=require('path');
const SRC=process.argv[2],OUT=process.argv[3];if(!SRC||!OUT){console.error('uso: node build_video_captacao.js <fonte.mp4> <saida>');process.exit(1)}
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
// cena: tipo 'br' (b-roll do vídeo-fonte, início em ss) ou 'tela' (tela real) ; dur em segundos

const fim=(sub)=>`<div style="position:absolute;inset:0;background:${C.musgo}"></div><img src="${F('brand/zion-logo-claro.png')}" style="position:absolute;left:64px;top:90px;width:260px">
 <div style="position:absolute;left:64px;right:64px;top:330px"><div class="k">Zion · educação para projetos turísticos</div><div style="font-family:Co;font-size:190px;line-height:.95;font-weight:700;color:${C.ouro};margin-top:14px">Cadastro gratuito</div>
 <div style="font-size:42px;line-height:1.35;color:${C.creme};margin-top:30px">${sub}</div>
 <div style="font-size:36px;line-height:1.35;color:${C.areia};margin-top:34px">Existem formações pagas, como a <b style="color:${C.creme}">Mini Mentoria de Estruturação Zion (R$ 47, pagamento único)</b>. Você só compra se quiser.</div>
 <div style="font-size:30px;line-height:1.35;color:${C.areia};margin-top:34px">Sem reunião, consultoria nem avaliação do terreno. Sem promessa de investimento, parceria ou renda.</div></div>
 <div style="position:absolute;left:0;top:1560px;width:1080px;height:130px;background:${C.ouro};color:${C.preto};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:38px">Cadastro gratuito · Formação paga a partir de R$47</div>`;
// V02 · Dono de Terreno (hook "Ei, você, dono de terreno!" preservado; ordem: dor, passo, origem, cadastro, formação paga, clareza)
const V02=[
 {tp:'br',ss:6,d:6,html:panel('Dono de terreno','Ei, você, <i>dono de terreno!</i>','Achou que o seu caso não tinha solução, né?')},
 {tp:'br',ss:14,d:6,html:panel('A dor','Você tem a área e a matrícula, <i>mas não tem capital.</i>','Antes do capital, vem o projeto.')},
 {tp:'br',ss:22,d:6,html:panel('O primeiro passo','Estruturar o projeto <i>no papel.</i>','Território, mercado, orçamento e pré-viabilidade, sem começar pela obra.')},
 {tp:'br',ss:30,d:6,html:panel('De onde vem o conhecimento','A Zion opera hospedagens <i>em Urubici e Florianópolis.</i>','E organiza esse conhecimento em formação digital.')},
 {tp:'br',ss:38,d:6,html:panel('Cadastro gratuito','Cadastre-se grátis e receba <i>conteúdos para começar.</i>','Sem obrigação de compra.')},
 {tp:'tela',img:'aula',d:7,html:panel('Formação paga, à parte','Existem formações pagas, como a <i>Mini Mentoria por R$ 47.</i>','Pagamento único. Você só compra se quiser.','Tela real da plataforma')},
 {tp:'br',ss:50,d:6,html:panel('Para ser claro','Isto é <i>educação.</i>','Não é reunião, consultoria nem avaliação do terreno. Não prometemos investimento nem parceria.')},
 {tp:'fim',d:9,html:fim('Receba conteúdos para dar os primeiros passos. Sem obrigação de compra.')}];
// V01 · Terreno Capital (hook "Você aí, dono de terreno" preservado)
const V01=[
 {tp:'br',ss:10,d:6,html:panel('Terreno','Você aí, <i>dono de terreno.</i>','Terreno parado há tanto tempo e sem saber por onde começar?')},
 {tp:'br',ss:18,d:6,html:panel('Colapso de crença','Você não precisa começar <i>construindo um hotel.</i>','Comece estruturando: dá para fazer isso no papel.')},
 {tp:'br',ss:26,d:6,html:panel('Metodologia Zion','Aprenda a <i>estruturar antes de construir.</i>','Educação para desenvolver projetos turísticos: território, mercado, orçamento e Dossiê.')},
 {tp:'br',ss:34,d:6,html:panel('Cadastro gratuito','Cadastre-se grátis e receba <i>conteúdos para começar.</i>','Sem obrigação de compra.')},
 {tp:'tela',img:'diagnostico',d:7,html:panel('Formação paga, à parte','Existem formações pagas, como a <i>Mini Mentoria por R$ 47.</i>','Pagamento único. Você só compra se quiser.','Tela real da plataforma')},
 {tp:'br',ss:44,d:6,html:panel('Para ser claro','Não é reunião, consultoria <i>nem avaliação do terreno.</i>','Não prometemos investimento, parceria nem renda. Formação digital.')},
 {tp:'fim',d:9,html:fim('Aprenda a estruturar o seu projeto antes de construir. Sem obrigação de compra.')}];
async function build(S,name,pg,T){const clips=[];
for(let i=0;i<S.length;i++){const s=S[i];const hf=path.join(T,`${name}-c${i}.html`);
 let body=s.html;if(s.tp==='tela')body=`<div style="position:absolute;inset:0;background:${C.preto}"></div><div style="position:absolute;left:204px;top:0;width:672px;height:1344px;border:4px solid ${C.ouro};background:url(${F('zion-collection/club/telas/'+s.img+'.jpg')}) top/672px auto no-repeat"></div>`+s.html;
 fs.writeFileSync(hf,`<!doctype html><meta charset=utf-8><style>${CSS}</style><body>${body}</body>`);await pg.goto('file://'+hf);await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(300);
 const png=path.join(T,`${name}-c${i}.png`);await pg.screenshot({path:png,omitBackground:s.tp==='br'});const mp=path.join(T,`${name}-c${i}.mp4`);
 const enc=['-c:v','libx264','-pix_fmt','yuv420p','-crf','28','-preset','medium','-r','30','-an','-movflags','+faststart'];
 if(s.tp==='br')execFileSync('ffmpeg',['-v','error','-y','-ss',String(s.ss),'-t',String(s.d),'-i',SRC,'-loop','1','-t',String(s.d),'-i',png,'-filter_complex','[0:v]crop=1080:1344:0:0,pad=1080:1920:0:0:color=0x040605[v];[v][1:v]overlay=0:0:shortest=1,format=yuv420p',...enc,mp]);
 else execFileSync('ffmpeg',['-v','error','-y','-loop','1','-t',String(s.d),'-i',png,...enc,mp]);clips.push(mp);}
fs.writeFileSync(path.join(T,`${name}-lista.txt`),clips.map(c=>`file '${c}'`).join('\n'));
execFileSync('ffmpeg',['-v','error','-y','-f','concat','-safe','0','-i',path.join(T,`${name}-lista.txt`),'-c','copy',path.join(OUT,`${name}.mp4`)]);}
(async()=>{fs.mkdirSync(OUT,{recursive:true});const T=path.join(OUT,'_cenas');fs.mkdirSync(T,{recursive:true});
const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
await build(V02,'capt-v02-dono-terreno-sem-audio',pg,T);await build(V01,'capt-v01-terreno-capital-sem-audio',pg,T);await b.close();console.log('ok');})();

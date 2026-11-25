// ZION CREATIVE · P0 · vídeo curto v-P0 (SEM áudio, SEM voz sintética): imagens reais da Zion (corte da parte de cima do vídeo-fonte,
// que exclui as legendas antigas e a cena com pessoa) + telas reais da plataforma + cartelas novas. Não altera o vídeo-fonte.
// Uso: node build_video_p0.js <video-fonte.mp4> <pasta-de-saida>      (requer ffmpeg e playwright)
const {chromium}=require('playwright');const {execFileSync}=require('child_process');const fs=require('fs');const path=require('path');
const SRC=process.argv[2],OUT=process.argv[3];if(!SRC||!OUT){console.error('uso: node build_video_p0.js <fonte.mp4> <saida>');process.exit(1)}
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
const panel=(k,t,s,fd='Mini Mentoria de Estruturação Zion')=>`<div class="pn"><div class="k">${k}</div><div class="t">${t}</div><div class="s">${s}</div></div>${LOGO}<div class="fd">${fd}</div>`;
// cena: tipo 'br' (b-roll do vídeo-fonte, início em ss) ou 'tela' (tela real) ; dur em segundos
const S=[
 {tp:'br',ss:6,d:6,html:panel('Dor específica','Você sabe o preço da cabana. <i>Sabe quanto custa deixar tudo pronto?</i>','Estrada, energia, fossa, projeto, taxas, móveis e enxoval.')},
 {tp:'br',ss:14,d:6,html:panel('Colapso de crença','Quem começa pela obra <i>começa pelo último passo.</i>','Antes de gastar, dá para estruturar o projeto no papel.')},
 {tp:'br',ss:24,d:6,html:panel('Orientação','Aprenda o passo a passo para <i>estruturar antes de construir.</i>','Mini Mentoria de Estruturação Zion: formação digital em 7 pilares.')},
 {tp:'tela',img:'aula',d:6,html:panel('Implementação · 1','Comece pelo <i>Marco Zero.</i>','Você vê onde está e por qual pilar começar.','Tela real da plataforma')},
 {tp:'tela',img:'diagnostico',d:6,html:panel('Implementação · 2','Preencha a ficha <i>“Faça agora”.</i>','Cada ficha vira uma página do seu Dossiê, que você gera em PDF.','Tela real da plataforma')},
 {tp:'tela',img:'previab',d:6,html:panel('Implementação · 3','Faça a conta <i>da pré-viabilidade.</i>','Quanto custa abrir, quanto entra, quanto sobra e o tempo de volta, com planilhas em branco.','Tela real da plataforma')},
 {tp:'br',ss:38,d:7,html:panel('O que você recebe','9 módulos, 70 conteúdos, <i>acesso à plataforma digital.</i>','Aulas gravadas, e-books por pilar, 2 planilhas em branco, kit de prompts e Dossiê em PDF.')},
 {tp:'fim',d:9,html:`<div style="position:absolute;inset:0;background:${C.musgo}"></div><img src="${F('brand/zion-logo-claro.png')}" style="position:absolute;left:64px;top:90px;width:260px">
 <div style="position:absolute;left:64px;right:64px;top:380px"><div class="k">Mini Mentoria de Estruturação Zion</div><div style="font-family:Co;font-size:300px;line-height:1;font-weight:700;color:${C.ouro};margin-top:10px">R$ 47</div>
 <div style="font-size:42px;line-height:1.35;color:${C.creme};margin-top:20px">pagamento único · sem mensalidade<br>acesso à plataforma digital<br>Pix ou cartão à vista · reembolso em 7 dias</div>
 <div style="font-size:34px;line-height:1.35;color:${C.areia};margin-top:40px">Formação digital: sem reunião e sem atendimento individual. Não promete renda, parceria ou investimento.</div></div>
 <div style="position:absolute;left:0;top:1560px;width:1080px;height:130px;background:${C.ouro};color:${C.preto};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:46px;text-transform:uppercase">Acesse a plataforma por R$ 47</div>`}];
(async()=>{fs.mkdirSync(OUT,{recursive:true});const T=path.join(OUT,'_cenas');fs.mkdirSync(T,{recursive:true});
const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});const clips=[];
for(let i=0;i<S.length;i++){const s=S[i];const hf=path.join(T,`c${i}.html`);
 let body=s.html;if(s.tp==='tela')body=`<div style="position:absolute;inset:0;background:${C.preto}"></div><div style="position:absolute;left:204px;top:0;width:672px;height:1344px;border:4px solid ${C.ouro};background:url(${F('zion-collection/club/telas/'+s.img+'.jpg')}) top/672px auto no-repeat"></div>`+s.html;
 fs.writeFileSync(hf,`<!doctype html><meta charset=utf-8><style>${CSS}</style><body>${body}</body>`);await pg.goto('file://'+hf);await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(300);
 const png=path.join(T,`c${i}.png`);await pg.screenshot({path:png,omitBackground:s.tp==='br'});const mp=path.join(T,`c${i}.mp4`);
 const enc=['-c:v','libx264','-pix_fmt','yuv420p','-crf','28','-preset','medium','-r','30','-an','-movflags','+faststart'];
 if(s.tp==='br')execFileSync('ffmpeg',['-v','error','-y','-ss',String(s.ss),'-t',String(s.d),'-i',SRC,'-loop','1','-t',String(s.d),'-i',png,'-filter_complex','[0:v]crop=1080:1344:0:0,pad=1080:1920:0:0:color=0x040605[v];[v][1:v]overlay=0:0:shortest=1,format=yuv420p',...enc,mp]);
 else execFileSync('ffmpeg',['-v','error','-y','-loop','1','-t',String(s.d),'-i',png,...enc,mp]);clips.push(mp);}
await b.close();fs.writeFileSync(path.join(T,'lista.txt'),clips.map(c=>`file '${c}'`).join('\n'));
execFileSync('ffmpeg',['-v','error','-y','-f','concat','-safe','0','-i',path.join(T,'lista.txt'),'-c','copy',path.join(OUT,'vp0-v02-passeio-mm47-sem-audio.mp4')]);console.log('ok');})();

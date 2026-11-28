// Teste da página /oportunidades (docs/investidores/index.html). Sem rede real: imagens do GitHub Pages
// são servidas do disco e o endpoint do formulário é simulado. Uso: node producao/investidores/test_page.js
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const ROOT=path.resolve(__dirname,'../..'),DOCS=path.join(ROOT,'docs'),OUT=path.join(__dirname,'prints');
const PAGES='https://bchaerk-creator.github.io/zion-hotel-ai-developer/';
let pass=0,fail=0;const ck=(n,c,x='')=>{c?pass++:fail++;console.log((c?'OK  ':'FALHA ')+n+(x?'  '+x:''))};
const TEST_CFG={ENDPOINT:''}; // WA01/WA02 usam os padrões da página (1061 e 98872-9883)
async function novo(b,vp,cfg=TEST_CFG,url='file://'+DOCS+'/investidores/index.html'){
  const ctx=await b.newContext({viewport:vp,deviceScaleFactor:1,isMobile:vp.width<600,hasTouch:vp.width<600});
  await ctx.addInitScript(c=>{window.ZION_CONFIG=c},cfg);
  await ctx.route(u=>true,r=>{const u=r.request().url();
    if(u.startsWith(PAGES)){const f=path.join(DOCS,u.slice(PAGES.length).split('?')[0]);if(fs.existsSync(f))return r.fulfill({path:f});return r.fulfill({status:404,body:''})}
    if(u.startsWith('file://'))return r.continue();return r.abort()});
  const p=await ctx.newPage();await p.goto(url);await p.waitForTimeout(500);return {ctx,p};
}
async function responde(p,vals){for(const v of vals){await p.check(`#card input[value="${v}"]`,{force:true});await p.click('#prox')}}
const RESP=['nao','empresario','participacao','redes','sul','agora','sim','sim'];
(async()=>{const b=await chromium.launch();
 // 1. lógica pura
 {const {ctx,p}=await novo(b,{width:390,height:844});
  const L=await p.evaluate(()=>{const z=window.ZionInvestors;return{
   a:z.classificar({interesse:'participacao',prazo:'agora',reuniao:'sim'}),b:z.classificar({interesse:'participacao',prazo:'6m',reuniao:'sim'}),
   c:z.classificar({interesse:'conhecer',prazo:'pesquisando',reuniao:'ainda_nao'}),d:z.classificar({interesse:'comprar_bubble',prazo:'agora',reuniao:'sim'}),
   e:z.classificar({interesse:'conhecer',prazo:'90d',reuniao:'sim'}),
   f1:z.normFone('(48) 99999-9999'),f2:z.normFone('48 3333-4444'),f3:z.normFone('123'),f4:z.normFone('+55 48 99999-9999'),f5:z.normFone('(48) 89999-9999')}});
  ck('classificação aderente',L.a==='aderente');ck('classificação em maturação',L.b==='em_maturacao'&&L.e==='em_maturacao');
  ck('classificação apenas pesquisa',L.c==='apenas_pesquisa');ck('classificação comprador de Bubble',L.d==='comprador_bubble');
  ck('telefone celular normalizado',L.f1==='5548999999999');ck('telefone fixo normalizado',L.f2==='554833334444');
  ck('telefone inválido recusado',L.f3===null&&L.f5===null);ck('telefone com +55',L.f4==='5548999999999');
  await ctx.close()}
 // 2. layout em 3 larguras mobile + desktop
 for(const [nome,vp] of [['360',{width:360,height:740}],['390',{width:390,height:844}],['430',{width:430,height:932}],['desktop',{width:1440,height:900}]]){
  const {ctx,p}=await novo(b,vp);
  const m=await p.evaluate(()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,
   peq:[...document.querySelectorAll('a.btn,button.btn,.opt span')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.height<44)}).length,
   imgsQuebradas:[...document.images].filter(i=>i.complete&&i.naturalWidth===0&&i.src.startsWith('http')).length}));
  ck(`sem rolagem horizontal (${nome})`,m.sw<=m.cw,`${m.sw}/${m.cw}`);ck(`toque >= 44px (${nome})`,m.peq===0,`${m.peq} pequenos`);
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}window.scrollTo(0,0)});await p.waitForTimeout(800);
  const q=await p.evaluate(()=>[...document.images].filter(i=>i.complete&&i.naturalWidth===0).length);ck(`imagens carregam (${nome})`,q===0,`${q} quebradas`);
  await p.screenshot({path:`${OUT}/pagina-${nome}.png`,fullPage:true});await ctx.close()}
 // 3. formulário completo mobile, endpoint simulado
 {const {ctx,p}=await novo(b,{width:390,height:844},{...TEST_CFG,ENDPOINT:'https://teste.invalid/hook'});
  let posts=[];await ctx.route('https://teste.invalid/hook',r=>{posts.push(JSON.parse(r.request().postData()));r.fulfill({status:200,body:'{}'})});
  await p.locator('#cadastro').scrollIntoViewIfNeeded();
  await p.click('#prox');ck('bloqueia sem resposta',(await p.textContent('#err')).includes('Escolha'));
  await p.screenshot({path:`${OUT}/form-1-pergunta.png`});
  await responde(p,RESP);
  await p.click('#env');ck('exige dados',(await p.textContent('#err')).includes('nome'));
  await p.screenshot({path:`${OUT}/form-2-dados.png`});
  await p.fill('#nome','Maria Souza');await p.fill('#cidade','Florianopolis');await p.click('#env');ck('exige UF',(await p.textContent('#err')).includes('UF'));
  await p.fill('#cidade','Florianópolis, SC');await p.fill('#fone','123');await p.click('#env');ck('exige WhatsApp válido',(await p.textContent('#err')).includes('WhatsApp'));
  await p.fill('#fone','(48) 99999-9999');await p.click('#env');ck('exige consentimento',(await p.textContent('#err')).includes('autorize'));
  await p.check('#lgpd');await p.click('#env');await p.waitForSelector('.ok');
  ck('um envio',posts.length===1);const d=posts[0]||{};
  ck('payload: telefone normalizado',d.whatsapp==='5548999999999');ck('payload: classificação aderente',d.classificacao_declarada==='aderente');
  ck('payload: consentimento e termo',d.consentimento_whatsapp===true&&!!d.termo_consentimento&&!!d.consentimento_em);
  ck('payload: id de submissão único',/\S{8,}/.test(d.submission_id||''));ck('payload: 8 respostas',Object.keys(d.respostas||{}).length===8);
  ck('payload sem CPF/patrimônio/faixa de capital',!/cpf|patrimonio|capital|faixa/i.test(JSON.stringify(d)));
  ck('tela final: dois canais de WhatsApp',(await p.locator('#go1').count())===1&&(await p.locator('#go2').count())===1);
  ck('link 02 usa o número escolhido',(await p.getAttribute('#go2','href')).includes('5548988729883'));ck('link 01 usa o final 1061',(await p.getAttribute('#go1','href')).includes('554861371061'));
  ck('link 02 sem dados pessoais',!/Maria|9999|Florian/.test(await p.getAttribute('#go2','href')));
  await p.screenshot({path:`${OUT}/form-3-conclusao.png`});
  await p.reload();await p.waitForTimeout(400);ck('lead já cadastrado não vê o formulário de novo',(await p.textContent('#card')).includes('já está cadastrado'));
  await p.screenshot({path:`${OUT}/form-4-ja-cadastrado.png`});await ctx.close()}
 // 4. robô (honeypot), falha de rede, comprador de Bubble
 {const {ctx,p}=await novo(b,{width:390,height:844},{...TEST_CFG,ENDPOINT:'https://teste.invalid/hook'});let n=0;await ctx.route('https://teste.invalid/hook',r=>{n++;r.fulfill({status:200,body:'{}'})});
  await responde(p,RESP);await p.fill('#nome','Robo Teste');await p.fill('#cidade','X, SC');await p.fill('#fone','(48) 99999-9999');await p.fill('#site','http://spam');await p.check('#lgpd');await p.click('#env');
  await p.waitForTimeout(300);ck('honeypot não envia',n===0);await ctx.close()}
 {const {ctx,p}=await novo(b,{width:390,height:844},{...TEST_CFG,ENDPOINT:'https://teste.invalid/hook'});await ctx.route('https://teste.invalid/hook',r=>r.fulfill({status:500,body:''}));
  await responde(p,RESP);await p.fill('#nome','Ana Lima');await p.fill('#cidade','Curitiba, PR');await p.fill('#fone','(41) 99999-9999');await p.check('#lgpd');await p.click('#env');await p.waitForTimeout(400);
  ck('falha de servidor mantém o formulário e avisa',(await p.textContent('#err')).includes('Não foi possível')&&(await p.locator('#env').isEnabled()));await ctx.close()}
 {const {ctx,p}=await novo(b,{width:390,height:844});await responde(p,['nao','empresario','comprar_bubble','nao','nao_sei','pesquisando','nao','ainda_nao']);
  await p.fill('#nome','Beto Souza');await p.fill('#cidade','Recife, PE');await p.fill('#fone','(81) 99999-9999');await p.check('#lgpd');await p.click('#env');await p.waitForSelector('.ok');
  ck('comprador de Bubble vai para a loja, sem prospecção de investimento',(await p.textContent('#card')).includes('loja')&&(await p.locator('#go2').count())===0);await ctx.close()}
 // 5. sem config: nada quebra e não expõe link de WhatsApp
 {const {ctx,p}=await novo(b,{width:390,height:844},{WA01:'',WA02:''});await responde(p,RESP);await p.fill('#nome','Caio Reis');await p.fill('#cidade','Salvador, BA');await p.fill('#fone','(71) 99999-9999');await p.check('#lgpd');await p.click('#env');await p.waitForSelector('.ok');
  ck('sem número configurado, nenhum link de WhatsApp aparece',(await p.locator('a[href*="wa.me"]').count())===0);await ctx.close()}
 // 6. conteúdo proibido
 {const {ctx,p}=await novo(b,{width:390,height:844});ck('vídeo sem URL aprovada não toca e não mostra botão de play',(await p.locator('#vbtn .play').count())===0&&(await p.locator('#vbtn video').count())===0);await ctx.close()}
 const html=fs.readFileSync(path.join(DOCS,'investidores/index.html'),'utf8');
 ck('formulário não oferece investir nas operações atuais (Urubici/Florianópolis à parte)',!/Operações existentes|value="urubici"|\["urubici"|\["florianopolis"/.test(html));
 const vis=html.replace(/nem promessa de rentabilidade/,'').replace(/<script[\s\S]*?<\/script>/g,'').replace(/<style[\s\S]*?<\/style>/g,'');
 ck('sem preço, checkout, mensalidade ou rentabilidade prometida',!/R\$\s?\d|checkout|mensalidade|garantid|retorno de|rentabilidade|à venda|vendemos|compre/i.test(vis));
 console.log(`\n${pass} ok, ${fail} falhas`);await b.close();process.exit(fail?1:0)})();

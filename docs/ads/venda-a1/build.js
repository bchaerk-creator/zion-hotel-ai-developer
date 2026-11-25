// Gera os cards 1080x1350 dos 3 anúncios do curso (fotos reais da Zion, sem pessoas).
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
const R=path.resolve(__dirname,'../..');
const F='file://'+R+'/assets/fonts/';const IMG=n=>'file://'+R+'/assets/'+n;
const LOGO='file://'+R+'/brand/zion-logo-claro.png';
const W=1080,H=1350;
const css=`@font-face{font-family:C;src:url(${F}cormorant.woff2);font-weight:300 700}
@font-face{font-family:A;src:url(${F}aventa.woff2);font-weight:300 700}
*{margin:0;box-sizing:border-box}body{width:${W}px;height:${H}px;position:relative;overflow:hidden;background:#040605;font-family:A;color:#FEF5F0}
.bg{position:absolute;inset:0;background-size:cover}.sh{position:absolute;inset:0}
.logo{position:absolute;left:72px;top:64px;height:54px}
.n{position:absolute;right:72px;top:72px;font-size:26px;color:#C9B37E;letter-spacing:.1em}
.box{position:absolute;left:72px;right:72px}
.k,h1,.s{text-shadow:0 2px 14px rgba(4,6,5,.9)}.k{font-size:28px;letter-spacing:.22em;text-transform:uppercase;color:#C9B37E}
h1{font-family:C;font-weight:600;line-height:1.02;font-size:104px}
h1 em{font-style:normal;color:#C9B37E}
.s{font-size:40px;line-height:1.3;color:#FEF5F0;margin-top:28px}
.foot{position:absolute;left:72px;right:72px;bottom:44px;font-size:21px;white-space:nowrap;color:#DED6BF;letter-spacing:.02em;border-top:1px solid rgba(201,179,126,.45);padding-top:16px;display:flex;justify-content:space-between}
.li{display:flex;gap:26px;align-items:center;margin-top:30px}.ic{flex:0 0 78px;height:78px;border-radius:50%;background:#C9B37E;color:#040605;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:40px}
.li b{font-size:50px;font-weight:600;line-height:1.1}
.btn{display:flex;align-items:center;justify-content:center;background:#C9B37E;color:#040605;font-weight:700;font-size:46px;border-radius:999px;height:104px;margin-top:40px}
.price{font-family:C;font-size:150px;color:#C9B37E;line-height:1;margin-top:18px}`;
const card=(n,tot,img,pos,top,body)=>`<style>${css}.ph{position:absolute;left:0;top:0;width:${W}px;height:660px;background:url(${IMG(img)}) ${pos}/cover}.pn{position:absolute;left:0;top:660px;width:${W}px;height:690px;background:#1B2117;border-top:6px solid #C9B37E}.logo{top:auto;bottom:auto;position:absolute;left:72px;top:690px;height:44px}.n{top:700px}.box{top:770px}.foot{bottom:36px}.k{font-size:27px}h1{font-size:96px}.s{font-size:41px;margin-top:22px}.li{margin-top:20px}.li b{font-size:42px;line-height:1.12}.ic{flex:0 0 64px;height:64px;font-size:34px}.price{font-size:120px;margin-top:8px}.btn{height:88px;font-size:40px;margin-top:24px}${n===1?`.ph{height:850px}.pn{top:850px;height:500px}.logo{top:874px}.n{top:884px}.box{top:936px}.k{font-size:24px}h1{font-size:72px;margin-top:6px}.s{font-size:32px;margin-top:10px}`:''}</style><div class=ph></div><div class=pn></div><img class=logo src="${LOGO}"><div class=n>${n}/${tot}</div><div class=box>${body}</div><div class=foot><span>Fotos reais da Zion Bubble Glamping</span><span>Material educativo · sem promessa</span></div>`;
const list=(a)=>a.map(t=>`<div class=li><div class=ic>✓</div><b>${t}</b></div>`).join('');
const cta=(kicker,price,sub)=>`<div class=k>${kicker}</div><h1 style="font-size:76px;margin-top:10px">Aprenda o <em>passo a passo</em></h1><div class=price>${price}</div><div class=s style="margin-top:14px">${sub}</div><div class=btn>Saiba mais</div>`;
const ADS={
 a1:[
  ['','store/hero.webp','center 62%',600,`<div class=k>Para quem tem terreno</div><h1>Tem terreno, <em>mas não tem capital?</em></h1><div class=s>Aprenda o passo a passo para estruturar o seu projeto. Mini Mentoria Zion, R$ 47.</div>`],
  ['','store/ceu.webp','center',600,`<h1>Terreno parado <em>não vira projeto sozinho.</em></h1><div class=s>Projeto com números e proposta clara se aprende, passo a passo.</div>`],
  ['','operacoes/op05.webp','center',600,`<h1>Você já tem a parte mais difícil: <em>a terra.</em></h1><div class=s>Falta o conhecimento para estruturá-la em projeto.</div>`],
  ['','store/deck.webp','center',560,`<div class=k>O que você recebe</div>${list(['Aulas gravadas e fichas “Faça agora”','E-books por pilar','2 planilhas em branco e Kit do Investidor','Dossiê do projeto em PDF'])}`],
  ['','store/noturna.webp','center',480,cta('Mini Mentoria de Estruturação Zion','R$ 47','Pagamento único · Pix ou cartão · Acesso à plataforma digital · garantia de 7 dias').replace('<div class=btn>','<div class=btn style="font-size:33px;height:104px">').replace('Saiba mais','QUERO ACESSAR A PLATAFORMA POR R$47')]
 ],
};
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:W,height:H},deviceScaleFactor:1});
 for(const [id,cards] of Object.entries(ADS)){for(let i=0;i<cards.length;i++){const [,img,pos,top,body]=cards[i];
  const hf=path.resolve(__dirname,'_tmp.html');fs.writeFileSync(hf,'<html><meta charset=utf-8><body>'+card(i+1,cards.length,img,pos,top,body)+'</body></html>');
  await p.goto('file://'+hf,{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
  await p.screenshot({path:path.resolve(__dirname,`${id==='a1'?'carrossel-a1-venda-'+(i+1)+'.png':''}`),type:'png'});}}
 await b.close();fs.unlinkSync(path.resolve(__dirname,'_tmp.html'));})();

// Slides 1080x1920 do vídeo (Reels/Stories, 30 s). Uso: node build_reels.js && bash montar_reels.sh
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
const A = __dirname, R = path.resolve(A, '../../..'), F = (p) => 'file://' + path.join(R, 'docs/assets/fonts', p);
const CSS = `@font-face{font-family:Cormorant;src:url(${F('cormorant.woff2')});font-weight:300 700}@font-face{font-family:Cormorant;font-style:italic;src:url(${F('cormorant-italic.woff2')})}@font-face{font-family:Aventa;src:url(${F('aventa.woff2')})}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1920px;background:radial-gradient(circle at 80% 10%,#2c3524,#1B2117 55%,#040605);color:#FEF5F0;font-family:Aventa,sans-serif;position:relative;overflow:hidden}
.logo{position:absolute;top:270px;left:0;right:0;text-align:center}.logo img{height:54px}
.c{position:absolute;left:90px;right:90px}h1{font:500 112px/1.02 Cormorant,serif}h1 i{color:#C9B37E}h2{font:500 74px/1.05 Cormorant,serif}
.k{font:500 28px Aventa;letter-spacing:.22em;color:#C9B37E;text-transform:uppercase}
li{list-style:none;font:500 46px/1.25 Aventa;padding:22px 0;border-top:1px solid rgba(222,214,191,.25)}li b{color:#C9B37E;margin-right:14px}
.f{position:absolute;left:60px;right:60px;top:1650px;text-align:center;font:500 24px Aventa;letter-spacing:.06em;color:#C9B37E}`;
const L = '<img src="file://' + path.join(R, 'docs/brand/zion-logo-claro.png') + '">';
const slides = {
  s1: `<div class="logo">${L}</div><div class="c" style="top:560px"><div class="k">Zion Hotel Academy</div><h1 style="margin-top:26px">Tem um terreno em <i>destino turístico?</i></h1><h2 style="margin-top:44px;color:#DED6BF">Veja como planejar o projeto e calcular o capital necessário.</h2></div><div class="f">MATERIAL EDUCATIVO · SEM PROMESSA DE CRÉDITO, SÓCIO OU RETORNO</div>`,
  fundo: `<div class="c" style="top:262px"><div class="k">A ferramenta funcionando</div></div><div class="f" style="top:1690px">Exemplo com dados fictícios · parcela sem tarifas, seguros ou indexação</div>`,
  s3: `<div class="logo">${L}</div><div class="c" style="top:520px"><div class="k">O que você recebe</div><h2 style="margin:22px 0 36px">Aprenda o passo a passo.</h2><ul><li><b>20</b>microaulas curtas com tarefa</li><li><b>60</b>páginas de guia em PDF</li><li><b>✓</b>simuladores de capital, operação e dívida</li><li><b>✓</b>checklist documental e plano de 30 dias</li><li><b>✓</b>gerador de dossiê em PDF</li></ul></div><div class="f">VÍDEOS DAS AULAS EM PRODUÇÃO · O CONTEÚDO COMPLETO JÁ ESTÁ NO PORTAL</div>`,
  s4: `<div class="logo">${L}</div><div class="c" style="top:640px;text-align:center"><h1>Da terra <i>ao negócio.</i></h1><h2 style="margin-top:50px;color:#DED6BF">Aprenda o passo a passo.</h2><div style="display:inline-block;margin-top:70px;background:#C9B37E;color:#040605;font:600 44px Aventa;padding:26px 54px;letter-spacing:.06em">SAIBA MAIS</div></div><div class="f">MATERIAL EDUCATIVO · SEM PROMESSA DE CRÉDITO, SÓCIO OU RETORNO</div>`,
};
(async () => {
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1080, height: 1920 } }); const T = path.join(A, '.tmp'); fs.mkdirSync(T, { recursive: true }); fs.mkdirSync(A + '/dist/video', { recursive: true });
  for (const [k, h] of Object.entries(slides)) { const f = T + '/' + k + '.html'; fs.writeFileSync(f, `<!doctype html><meta charset="utf-8"><style>${CSS}</style>${h}`); await p.goto('file://' + f); await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: `${A}/dist/video/${k}.png` }); }
  fs.rmSync(T, { recursive: true }); await b.close(); console.log('slides ok');
})();

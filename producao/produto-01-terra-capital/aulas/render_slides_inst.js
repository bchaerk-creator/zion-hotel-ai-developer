const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
const A = __dirname, W = A + '/.work', J = JSON.parse(fs.readFileSync(W + '/inst.json', 'utf8')), R = J.R, F = (p) => 'file://' + path.join(R, 'docs/assets/fonts', p);
const CSS = `@font-face{font-family:Cormorant;src:url(${F('cormorant.woff2')});font-weight:300 700}@font-face{font-family:Cormorant;font-style:italic;src:url(${F('cormorant-italic.woff2')})}@font-face{font-family:Aventa;src:url(${F('aventa.woff2')})}
*{margin:0;box-sizing:border-box}body{width:1280px;height:720px;background:radial-gradient(circle at 85% 0,#2c3524,#1B2117 55%,#0a0d09);color:#FEF5F0;font-family:Aventa,sans-serif;position:relative;overflow:hidden}
.top{position:absolute;top:34px;left:64px}.top img{height:30px}.c{position:absolute;left:64px;right:64px;top:110px;bottom:70px;display:flex;gap:48px;align-items:center}
h1{font:500 italic 76px/1.06 Cormorant,serif}.t{font:400 42px/1.3 Aventa,sans-serif}.tx{flex:1}
.im{width:400px;flex:none}.im img{width:400px;height:440px;object-fit:cover;object-position:top;border-radius:8px;display:block}.im span{display:block;font:400 15px Aventa;color:#A39E8E;margin-top:8px}
.f{position:absolute;left:64px;right:64px;bottom:26px;font:400 15px Aventa;color:#A39E8E;display:flex;justify-content:space-between}`;
(async () => { const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  for (const s of J.segs) { const [img, cap] = (s.img || '|').split('|');
    const mid = (s.tipo === 'titulo' ? `<div class="tx"><h1>${s.tela}</h1></div>` : `<div class="tx"><div class="t" style="font-size:${s.tela.length > 120 ? 36 : 42}px">${s.tela}</div></div>`) + (img ? `<div class="im"><img src="file://${path.join(R, img)}"><span>${cap}</span></div>` : '');
    const f = W + '/i.html'; fs.writeFileSync(f, `<!doctype html><meta charset="utf-8"><style>${CSS}</style><div class="top"><img src="file://${path.join(R, 'docs/brand/zion-logo-claro.png')}"></div><div class="c">${mid}</div><div class="f"><span>Zion Hotel Academy · Você tem terra. Falta capital?</span><span>Material educativo · sem promessa de crédito, sócio ou retorno · narração sintética</span></div>`);
    await p.goto('file://' + f); await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: `${W}/${s.v}_${s.k}.png` }); }
  await b.close(); })();

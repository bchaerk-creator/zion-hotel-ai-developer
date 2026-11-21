// Slides 1280x720 das microaulas + tela real de cada ferramenta (dados fictícios). Chamado por gerar_videos.py.
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
const A = __dirname, P = path.resolve(A, '..'), R = path.resolve(P, '../..'), W = A + '/.work', F = (p) => 'file://' + path.join(R, 'docs/assets/fonts', p);
const segs = JSON.parse(fs.readFileSync(W + '/segs.json', 'utf8')); const E = (s) => String(s).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
const CSS = `@font-face{font-family:Cormorant;src:url(${F('cormorant.woff2')});font-weight:300 700}@font-face{font-family:Cormorant;font-style:italic;src:url(${F('cormorant-italic.woff2')})}@font-face{font-family:Aventa;src:url(${F('aventa.woff2')})}
*{margin:0;box-sizing:border-box}body{width:1280px;height:720px;background:radial-gradient(circle at 85% 0,#2c3524,#1B2117 55%,#0a0d09);color:#FEF5F0;font-family:Aventa,sans-serif;position:relative;overflow:hidden}
.top{position:absolute;top:34px;left:64px;right:64px;display:flex;justify-content:space-between;align-items:center}.top img{height:30px}.k{font:500 17px Aventa;letter-spacing:.2em;color:#C9B37E;text-transform:uppercase}
.c{position:absolute;left:64px;right:64px;top:120px;bottom:70px;display:flex;flex-direction:column;justify-content:center}
h1{font:500 italic 66px/1.08 Cormorant,serif;color:#FEF5F0}h2{font:500 40px/1.1 Cormorant,serif;color:#C9B37E;margin-top:26px}
.n{font:500 italic 110px/1 Cormorant,serif;color:#C9B37E}.t{font:400 40px/1.32 Aventa,sans-serif;color:#FEF5F0;margin-top:10px}
.f{position:absolute;left:64px;right:64px;bottom:26px;font:400 15px Aventa;color:#A39E8E;letter-spacing:.04em;display:flex;justify-content:space-between}
.duo{display:flex;gap:50px;align-items:center}.duo .tx{flex:1}.ph{width:270px;height:480px;border:6px solid #040605;border-radius:26px;overflow:hidden;flex:none;box-shadow:0 14px 40px rgba(0,0,0,.6)}.ph img{width:100%}
.tag{display:inline-block;background:#C9B37E;color:#040605;font:600 20px Aventa;letter-spacing:.14em;padding:8px 16px;text-transform:uppercase}`;
(async () => {
  const b = await chromium.launch();
  // telas reais das ferramentas
  const m = await b.newPage({ viewport: { width: 390, height: 693 }, deviceScaleFactor: 2 }); await m.route('**/jspdf*', r => r.fulfill({ body: '' }));
  for (const k of [...new Set(segs.filter(s => s.ferramenta).map(s => s.ferramenta))]) { await m.goto('file://' + P + '/dist/index.html#ferramenta-' + k); await m.reload(); await m.evaluate(() => { const r = document.querySelector('.res'); if (r) { r.scrollIntoView(); window.scrollBy(0, -210); } else window.scrollTo(0, 120); }); await m.screenshot({ path: `${W}/tool-${k}.png` }); }
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } }); const logo = 'file://' + path.join(R, 'docs/brand/zion-logo-claro.png');
  for (const s of segs) {
    const top = `<div class="top"><img src="${logo}"><div class="k">Pilar ${s.pilar} · ${E(s.pnome)} · Aula ${s.aula} de 20</div></div>`;
    const fs2 = s.tela.length > 190 ? 32 : s.tela.length > 140 ? 36 : 40;
    let mid = s.tipo === 'abre' ? `<h1>${E(s.tela)}</h1><h2>${E(s.sub)}</h2>`
      : s.tipo === 'card' ? `<div class="n">${s.n}</div><div class="t" style="font-size:${fs2}px">${E(s.tela)}</div>`
        : `<div class="duo"><div class="tx"><span class="tag">Faça agora</span><div class="t" style="font-size:46px;margin-top:26px">${E(s.tela)}</div><div class="t" style="font-size:24px;color:#DED6BF;margin-top:22px">A ferramenta está aberta logo abaixo desta aula.</div></div><div class="ph"><img src="file://${W}/tool-${s.ferramenta}.png"></div></div>`;
    const f = `${W}/s.html`; fs.writeFileSync(f, `<!doctype html><meta charset="utf-8"><style>${CSS}</style>${top}<div class="c">${mid}</div><div class="f"><span>Zion Hotel Academy · Você tem terra. Falta capital?</span><span>Material educativo · exemplos com dados fictícios · narração sintética</span></div>`);
    await p.goto('file://' + f); await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: `${W}/a${String(s.aula).padStart(2, '0')}_${s.k}.png` });
  }
  await b.close(); console.log('slides ok:', segs.length);
})();

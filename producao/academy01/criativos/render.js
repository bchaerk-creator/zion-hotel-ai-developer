// Gera os 10 criativos 1080x1350 (PNG) a partir de cards.json. Uso: node render.js <pasta-saida>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const R = path.resolve(__dirname, '../../../docs'); const out = process.argv[2]; fs.mkdirSync(out, { recursive: true });
const b64 = (p) => fs.readFileSync(p).toString('base64');
const fonte = (f) => `url(data:font/woff2;base64,${b64(path.join(R, 'assets/fonts', f))})`;
const logo = 'data:image/png;base64,' + b64(path.join(R, 'brand/zion-logo-claro.png'));
const cards = JSON.parse(fs.readFileSync(path.join(__dirname, 'cards.json')));
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/\n/g, '<br>');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (const c of cards) {
    const ext = path.extname(c.foto).slice(1); const foto = `data:image/${ext};base64,` + b64(path.join(R, 'assets', c.foto));
    await p.setContent(`<!doctype html><html><head><style>
@font-face{font-family:C;src:${fonte('cormorant.woff2')}}@font-face{font-family:C;font-style:italic;src:${fonte('cormorant-italic.woff2')}}@font-face{font-family:A;src:${fonte('aventa.woff2')}}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;position:relative;overflow:hidden;background:#040605;font-family:A,Arial}
.f{position:absolute;inset:0;background:url(${foto}) center/cover}
.g{position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,6,5,.55) 0%,rgba(4,6,5,.1) 26%,rgba(4,6,5,.25) 45%,rgba(4,6,5,.92) 70%,#040605 100%)}
.top{position:absolute;top:64px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center}
.top img{height:46px}.n{font-size:22px;letter-spacing:.24em;color:#C9B37E;text-transform:uppercase}
.base{position:absolute;left:72px;right:72px;bottom:96px}
.fase{font-size:22px;letter-spacing:.28em;text-transform:uppercase;color:#C9B37E;margin-bottom:22px}
h1{font-family:C;font-weight:400;font-size:${c.titulo.length > 26 ? 86 : 100}px;line-height:1.0;color:#FEF5F0;margin-bottom:28px;letter-spacing:-.01em}
p{font-size:${c.texto.length > 110 ? 33 : 36}px;line-height:1.38;color:#DED6BF;max-width:900px;margin-bottom:44px}
.cta{display:inline-block;background:#C9B37E;color:#040605;font-weight:700;font-size:28px;letter-spacing:.08em;padding:26px 40px;border-radius:3px}
.rod{position:absolute;left:72px;right:72px;bottom:40px;display:flex;justify-content:space-between;font-size:19px;letter-spacing:.14em;color:#8E8A7C;text-transform:uppercase}
</style></head><body><div class="f"></div><div class="g"></div>
<div class="top"><img src="${logo}"><span class="n">${String(c.n).padStart(2, '0')} / 10</span></div>
<div class="base"><div class="fase">Zion Hotel Academy · ${c.fase}</div><h1>${esc(c.titulo)}</h1><p>${esc(c.texto)}</p><span class="cta">${c.cta}</span></div>
<div class="rod"><span>Seu Airbnb Está Vazio? · Guia interativo</span><span>Foto: Zion Bubble Glamping</span></div></body></html>`);
    await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(out, `arsenal01-card${String(c.n).padStart(2, '0')}.png`) });
  }
  await b.close(); console.log('ok', cards.length);
})();

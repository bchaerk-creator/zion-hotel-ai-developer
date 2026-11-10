// Capas do Kit Inicial de Captação no padrão das capas Zion (docs/capas-zion, gerador producao/capas-piloto/compor_pilotos.js):
// foto real da Zion de fundo, degradê musgo, Cormorant + Aventa, dourado #E0BE5E, logo oficial.
// Saídas: kit-captacao-h.jpg (1280×720) e kit-captacao-v.jpg (720×1080), desenhadas em 1920×1080 / 1080×1620 e reduzidas (fator 2/3), como as "-modulo".
// Uso: node src/build_capas.js <pasta-saida>
const { chromium } = require("playwright"); const path = require("path"); const fs = require("fs");
const OUT = path.resolve(process.argv[2] || "dist"); fs.mkdirSync(OUT, { recursive: true });
const D = path.resolve(__dirname, "../../../../docs");
const data = (f, m) => `data:${m};base64,` + fs.readFileSync(f).toString("base64");
const LOGO = data(path.join(D, "brand/zion-logo-claro.png"), "image/png");
const fonte = (f) => data(path.join(D, "assets/fonts", f), "font/woff2");
const fonts = `@font-face{font-family:Cormorant;src:url(${fonte("cormorant.woff2")})}@font-face{font-family:Cormorant;font-style:italic;src:url(${fonte("cormorant-italic.woff2")})}@font-face{font-family:Aventa;src:url(${fonte("aventa.woff2")})}`;
const FOTO = data(path.join(D, "assets/operacoes/op09.webp"), "image/webp");
const C = { kicker: "Club Zion Collection · Kit Inicial", titulo: "Captação", titulo2: "de Recursos", sub: "Você tem a terra. Aprenda o caminho para tirar o projeto do papel." };
const M = {
  h: { W: 1920, H: 1080, pad: "110px 128px", logo: 96, k: 32, h1: 160, gap1: 26, bar: [150, 5], gap2: 34, h2: 56, h2w: 980, r: 22, grad: "90deg", g: [0, 46, 74, 100], pos: "75% 50%" },
  v: { W: 1080, H: 1620, pad: "100px 84px", logo: 88, k: 28, h1: 118, gap1: 22, bar: [150, 5], gap2: 30, h2: 48, h2w: 900, r: 21, grad: "0deg", g: [0, 44, 72, 100], pos: "50% 30%" },
};
const html = (m) => `<!doctype html><html><head><meta charset="utf-8"><style>${fonts}
*{margin:0;box-sizing:border-box}body{width:${m.W}px;height:${m.H}px;position:relative;overflow:hidden;background:#16261C;color:#F5F1E8;font-family:Aventa,Arial,sans-serif}
.f{position:absolute;inset:0;background:url(${FOTO}) ${m.pos}/cover}
.v{position:absolute;inset:0;background:linear-gradient(${m.grad},rgba(22,38,28,.97) ${m.g[0]}%,rgba(22,38,28,.86) ${m.g[1]}%,rgba(22,38,28,.28) ${m.g[2]}%,rgba(22,38,28,.12) ${m.g[3]}%)}
.w{position:absolute;inset:0;padding:${m.pad};display:flex;flex-direction:column;justify-content:space-between}
img{height:${m.logo}px;align-self:flex-start}
.k{color:#E0BE5E;letter-spacing:.2em;text-transform:uppercase;font-weight:700;font-size:${m.k}px}
h1{font-family:Cormorant,Georgia,serif;font-weight:500;font-size:${m.h1}px;line-height:.92;margin:${m.gap1}px 0 ${m.gap2}px}
h1 em{font-style:italic}
.bar{width:${m.bar[0]}px;height:${m.bar[1]}px;background:#E0BE5E;margin:0 0 ${m.gap2}px}
h2{font-family:Cormorant,Georgia,serif;font-style:italic;font-weight:400;font-size:${m.h2}px;color:#E0BE5E;line-height:1.12;max-width:${m.h2w}px}
.r{font-size:${m.r}px;opacity:.85;letter-spacing:.22em;text-transform:uppercase;font-weight:700;color:#E0BE5E}
</style></head><body><div class="f"></div><div class="v"></div><div class="w"><img src="${LOGO}"><div><div class="k">${C.kicker}</div><h1>${C.titulo}<br><em>${C.titulo2}</em></h1><div class="bar"></div><h2>${C.sub}</h2></div><div class="r">Zion Hotel Group International</div></div></body></html>`;
(async () => {
  const b = await chromium.launch();
  for (const [suf, m] of Object.entries(M)) {
    const p = await b.newPage({ viewport: { width: m.W, height: m.H }, deviceScaleFactor: 2 / 3 });
    await p.setContent(html(m)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
    const f = path.join(OUT, `kit-captacao-${suf}.jpg`); await p.screenshot({ path: f, type: "jpeg", quality: 88 }); await p.close(); console.log("capa", f);
  }
  await b.close();
})();

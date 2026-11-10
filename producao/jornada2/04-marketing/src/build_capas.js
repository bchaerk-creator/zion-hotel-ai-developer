// Capas do módulo e das aulas (padrão visual das capas da Trilha 1). Uso: node src/build_capas.js <pasta docs/trilha2/capas>
const { chromium } = require("playwright"); const path = require("path"); const fs = require("fs");
const OUT = path.resolve(process.argv[2]); fs.mkdirSync(OUT, { recursive: true });
const D = path.resolve(__dirname, "../../../../docs");
const data = (f, mime) => `data:${mime};base64,` + fs.readFileSync(f).toString("base64");
const LOGO_C = data(path.join(D, "brand/zion-logo-claro.png"), "image/png"), LOGO_E = data(path.join(D, "brand/zion-logo-escuro.png"), "image/png"), FOTO = data(path.join(D, "assets/operacoes/op08.webp"), "image/webp");
const fonts = `@font-face{font-family:Cormorant;src:url(file://${D}/assets/fonts/cormorant.woff2)}@font-face{font-family:Cormorant;font-style:italic;src:url(file://${D}/assets/fonts/cormorant-italic.woff2)}@font-face{font-family:Aventa;src:url(file://${D}/assets/fonts/aventa.woff2)}`;
const modulo = (W, H, v) => `<!doctype html><html><head><meta charset="utf-8"><style>${fonts}
*{margin:0;box-sizing:border-box}body{width:${W}px;height:${H}px;position:relative;overflow:hidden;background:#16261C;color:#F5F1E8;font-family:Aventa,Arial,sans-serif}
.f{position:absolute;inset:0;background:url(${FOTO}) center/cover}
.v{position:absolute;inset:0;background:linear-gradient(${v ? "180deg" : "90deg"},rgba(22,38,28,.96) 0%,rgba(22,38,28,.86) 45%,rgba(22,38,28,.35) 100%)}
.w{position:absolute;left:${v ? 56 : 88}px;right:${v ? 56 : 88}px;top:${v ? 90 : 70}px;bottom:${v ? 80 : 70}px;display:flex;flex-direction:column;justify-content:space-between}
img{height:${v ? 46 : 52}px;align-self:flex-start}
.k{color:#E0BE5E;letter-spacing:.2em;text-transform:uppercase;font-weight:700;font-size:${v ? 22 : 30}px}
h1{font-family:Cormorant,Georgia,serif;font-weight:500;font-size:${v ? 110 : 150}px;line-height:1;margin:18px 0 22px}
.bar{width:130px;height:4px;background:#E0BE5E;margin:0 0 26px}
h2{font-family:Cormorant,Georgia,serif;font-style:italic;font-weight:400;font-size:${v ? 48 : 58}px;color:#E0BE5E;line-height:1.1}
</style></head><body><div class="f"></div><div class="v"></div><div class="w"><img src="${LOGO_C}"><div><div class="k">Jornada 2 · Gestão</div><h1>Módulo 4</h1><div class="bar"></div><h2>Marketing e vendas</h2></div><div class="k" style="font-size:${v ? 16 : 18}px;opacity:.8">Zion Hospitality Business</div></div></body></html>`;
const aula = (kicker, titulo, sub, selo, icone) => `<!doctype html><html><head><meta charset="utf-8"><style>${fonts}
*{margin:0;box-sizing:border-box}body{width:1280px;height:720px;position:relative;overflow:hidden;background:#F5F1E8;color:#16261C;font-family:Aventa,Arial,sans-serif}
.w{position:absolute;left:72px;right:72px;top:64px;bottom:56px}
img{height:52px}
.k{color:#7A5E12;letter-spacing:.2em;text-transform:uppercase;font-weight:700;font-size:22px;margin-top:70px}
h1{font-family:Cormorant,Georgia,serif;font-weight:500;font-size:112px;line-height:1;margin:14px 0 14px;max-width:760px}
h2{font-family:Cormorant,Georgia,serif;font-style:italic;font-weight:400;font-size:42px;color:#16261C;max-width:760px;line-height:1.15}
.s{position:absolute;left:0;bottom:0;background:#16261C;color:#F5F1E8;border-radius:999px;padding:16px 28px;font-size:20px;letter-spacing:.18em;text-transform:uppercase;font-weight:700}
.ic{position:absolute;right:40px;top:120px;width:300px;height:360px;border-radius:26px;background:#fff;border:6px solid #16261C;display:flex;flex-direction:column;gap:26px;padding:60px 36px;justify-content:center}
.ic i{display:block;height:22px;border-radius:11px;background:#C9C3B4}
.ic i.g{background:#7A5E12;width:60%}
.num{position:absolute;right:60px;top:40px;font-family:Cormorant,serif;font-size:220px;color:#E0BE5E;opacity:.35;line-height:1}
</style></head><body><div class="w"><img src="${LOGO_E}"><div class="k">${kicker}</div><h1>${titulo}</h1><h2>${sub}</h2><div class="s">${selo}</div>${icone === "num" ? `<div class="num">4</div>` : `<div class="ic"><i class="g"></i><i></i><i></i><i class="g" style="width:80%"></i><i></i></div>`}</div></body></html>`;
(async () => {
  const b = await chromium.launch();
  const shots = [
    ["g4-h.jpg", 1280, 720, modulo(1280, 720, false)], ["g4-v.jpg", 720, 1080, modulo(720, 1080, true)],
    ["g4-c-aula.jpg", 1280, 720, aula("Jornada 2 · Módulo 4", "Aula em vídeo", "Marca, lista própria e custo por reserva", "Vídeo · promessa · lista · canais", "num")],
    ["g4-c-faca.jpg", 1280, 720, aula("Jornada 2 · Módulo 4", "Faça agora", "A minha Marca e Captação · página 4", "Ferramenta · Tutorial · PDF", "ic")],
    ["g4-c-resumo.jpg", 1280, 720, aula("Jornada 2 · Módulo 4", "Resumo", "O que ficou da aula, em oito páginas", "PDF · Exemplo didático", "ic")],
    ["g4-c-planilha.jpg", 1280, 720, aula("Jornada 2 · Módulo 4", "Plano de Captação", "Marca, canais, lista própria e 12 meses", "Planilha · Em branco e exemplo", "ic")],
  ];
  for (const [n, W, H, html] of shots) {
    const p = await b.newPage({ viewport: { width: W, height: H } }); await p.setContent(html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(OUT, n), type: "jpeg", quality: 86 }); await p.close(); console.log("capa", n);
  }
  await b.close();
})();

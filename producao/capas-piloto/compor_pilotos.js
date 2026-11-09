// Capas-piloto (prévia). Script NOVO e separado: segue o mesmo método das capas atuais
// (producao/jornada2/00-marco-zero/src/build_capas.js: HTML + Playwright, foto de fundo, degradê musgo,
// Cormorant e Aventa, dourado #E0BE5E, logo oficial), sem alterar o programa existente.
// Uso: node producao/capas-piloto/compor_pilotos.js <pasta de saída> [pasta com fundos gerados]
// Sem a segunda pasta, usa fotos próprias da Zion já existentes no repositório como fundo PROVISÓRIO.
const { chromium } = require("playwright"); const path = require("path"); const fs = require("fs");
const OUT = path.resolve(process.argv[2] || "previas"); fs.mkdirSync(OUT, { recursive: true });
const ARG3 = process.argv[3] ? path.resolve(process.argv[3]) : null;
// 3º argumento: pasta com fundos gerados (sem texto) OU um .json com fotos escolhidas por capa:
// { "01-desenvolvimento": { "foto": "/caminho/foto.jpg", "posH": "50% 30%", "posV": "50% 20%", "modoH": "painel" | "cover", "tom": true } }
const GERADOS = ARG3 && !ARG3.endsWith(".json") ? ARG3 : null;
const MAPA = ARG3 && ARG3.endsWith(".json") ? JSON.parse(fs.readFileSync(ARG3, "utf8")) : {};
const D = path.resolve(__dirname, "../../docs");
const mime = (f) => (f.endsWith(".png") ? "image/png" : f.endsWith(".webp") ? "image/webp" : "image/jpeg");
const data = (f) => `data:${mime(f)};base64,` + fs.readFileSync(f).toString("base64");
const LOGO_C = data(path.join(D, "brand/zion-logo-claro.png"));
// Fontes embutidas (data URL): a página criada com setContent não carrega arquivos locais por file://.
const fonte = (f) => `data:font/woff2;base64,` + fs.readFileSync(path.join(D, "assets/fonts", f)).toString("base64");
const fonts = `@font-face{font-family:Cormorant;src:url(${fonte("cormorant.woff2")})}@font-face{font-family:Cormorant;font-style:italic;src:url(${fonte("cormorant-italic.woff2")})}@font-face{font-family:Aventa;src:url(${fonte("aventa.woff2")})}`;

// Fundo provisório: foto própria da Zion. Fundo final: arquivo gerado (sem texto) com o mesmo nome-base.
const CAPAS = [
  { id: "01-desenvolvimento", kicker: "Trilha 1 · Desenvolvimento", titulo: "Desenvolvimento", titulo2: "Hoteleiro", sub: "Do terreno ao empreendimento turístico",
    foto: "trilha1/apresentacao/fotos/c8d0eb086b.jpg", posH: "70% 50%", posV: "38% 50%" },
  { id: "02-gestao", kicker: "Jornada 2 · Gestão", titulo: "Gestão", titulo2: "Hoteleira", sub: "O empreendimento administrado com método",
    foto: "land-members/img/zion-bubble-interior-original.jpg", posH: "50% 60%", posV: "55% 50%" },
  { id: "03-land-bank", kicker: "Zion Land Bank · Banco de áreas", titulo: "Land", titulo2: "Bank", sub: "O potencial do terreno, estruturado em projeto",
    foto: "trilha1/apresentacao/fotos/901904223c.jpg", posH: "50% 10%", posV: "70% 0%" },
];
const FORMATOS = [ { suf: "h", W: 1920, H: 1080, v: false }, { suf: "v", W: 1080, H: 1620, v: true } ];

function fundo(c, suf) {
  const m = MAPA[c.id];
  if (m && m.foto) return { src: data(m.foto), provisorio: false, escolhida: true };
  if (GERADOS) for (const ext of [".png", ".jpg", ".jpeg", ".webp"]) {
    for (const nome of [`${c.id}-${suf}${ext}`, `${c.id}${ext}`]) { const f = path.join(GERADOS, nome); if (fs.existsSync(f)) return { src: data(f), provisorio: false }; }
  }
  return { src: data(path.join(D, c.foto)), provisorio: true };
}
// Medidas explícitas por formato (horizontal 1920×1080 e vertical 1080×1620), nas proporções das capas atuais.
const M = {
  h: { pad: "110px 128px", logo: 96, k: 32, h1: 172, gap1: 26, bar: [150, 5], gap2: 34, h2: 58, h2w: 980, r: 22, grad: "90deg", g: [0, 46, 74, 100] },
  v: { pad: "100px 84px", logo: 88, k: 28, h1: 122, gap1: 22, bar: [150, 5], gap2: 30, h2: 50, h2w: 900, r: 21, grad: "0deg", g: [0, 44, 72, 100] },
};
const html = (c, f, bg, pos) => { const { W, H } = f, m = M[f.suf], o = MAPA[c.id] || {}, painel = f.suf === "h" && o.modoH === "painel", tom = !!o.tom; return `<!doctype html><html><head><meta charset="utf-8"><style>${fonts}
*{margin:0;box-sizing:border-box}body{width:${W}px;height:${H}px;position:relative;overflow:hidden;background:#16261C;color:#F5F1E8;font-family:Aventa,Arial,sans-serif}
.f{position:absolute;${painel ? `top:0;bottom:0;right:0;width:${o.larguraPainel || 62}%;background:url(${bg}) ${o.posPainel || "right center"}/cover;-webkit-mask-image:linear-gradient(90deg,transparent 0%,#000 45%);mask-image:linear-gradient(90deg,transparent 0%,#000 45%)` : `inset:0;background:url(${bg}) ${pos}/cover`}}
.t{position:absolute;inset:0;background:#16261C;mix-blend-mode:color;opacity:${tom ? .55 : 0}}
.v{position:absolute;inset:0;background:linear-gradient(${m.grad},rgba(22,38,28,.97) ${m.g[0]}%,rgba(22,38,28,.86) ${m.g[1]}%,rgba(22,38,28,.28) ${m.g[2]}%,rgba(22,38,28,.12) ${m.g[3]}%)}
.w{position:absolute;inset:0;padding:${m.pad};display:flex;flex-direction:column;justify-content:space-between}
img{height:${m.logo}px;align-self:flex-start}
.k{color:#E0BE5E;letter-spacing:.2em;text-transform:uppercase;font-weight:700;font-size:${m.k}px}
h1{font-family:Cormorant,Georgia,serif;font-weight:500;font-size:${m.h1}px;line-height:.92;margin:${m.gap1}px 0 ${m.gap2}px}
h1 em{font-style:italic}
.bar{width:${m.bar[0]}px;height:${m.bar[1]}px;background:#E0BE5E;margin:0 0 ${m.gap2}px}
h2{font-family:Cormorant,Georgia,serif;font-style:italic;font-weight:400;font-size:${m.h2}px;color:#E0BE5E;line-height:1.12;max-width:${m.h2w}px}
.r{font-size:${m.r}px;opacity:.85;letter-spacing:.22em;text-transform:uppercase;font-weight:700;color:#E0BE5E}
</style></head><body><div class="f"></div><div class="t"></div><div class="v"></div><div class="w"><img src="${LOGO_C}"><div><div class="k">${c.kicker}</div><h1>${c.titulo}<br><em>${c.titulo2}</em></h1><div class="bar"></div><h2>${c.sub}</h2></div><div class="r">Zion Hospitality Business</div></div></body></html>`; };

(async () => {
  const b = await chromium.launch(); const relacao = [];
  for (const c of CAPAS) for (const f of FORMATOS) {
    const bg = fundo(c, f.suf), nome = `${c.id}-${f.suf}${bg.provisorio ? "-provisoria" : ""}.jpg`, o = MAPA[c.id] || {};
    const p = await b.newPage({ viewport: { width: f.W, height: f.H } }); await p.setContent(html(c, f, bg.src, f.v ? (o.posV || c.posV) : (o.posH || c.posH)));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
    await p.screenshot({ path: path.join(OUT, nome), type: "jpeg", quality: 88 }); await p.close();
    relacao.push({ arquivo: nome, largura: f.W, altura: f.H, fundo: bg.escolhida ? `foto escolhida: ${path.basename(o.foto)}` : bg.provisorio ? `provisório: docs/${c.foto}` : "imagem gerada (sem texto)" });
    console.log("capa", nome);
  }
  // Fundos sem texto (o que o gerador de imagem deve entregar), no mesmo enquadramento, para comparação.
  for (const c of CAPAS) for (const f of FORMATOS) {
    const bg = fundo(c, f.suf), nome = `${c.id}-${f.suf}-fundo-sem-texto${bg.provisorio ? "-provisorio" : ""}.jpg`;
    const p = await b.newPage({ viewport: { width: f.W, height: f.H } });
    await p.setContent(`<html><body style="margin:0;width:${f.W}px;height:${f.H}px;background:url(${bg.src}) ${f.v ? c.posV : c.posH}/cover"></body></html>`);
    await p.waitForTimeout(150); await p.screenshot({ path: path.join(OUT, nome), type: "jpeg", quality: 88 }); await p.close();
    relacao.push({ arquivo: nome, largura: f.W, altura: f.H, fundo: bg.provisorio ? `provisório: docs/${c.foto}` : "imagem gerada" });
  }
  await b.close(); fs.writeFileSync(path.join(OUT, "relacao.json"), JSON.stringify(relacao, null, 1));
})();

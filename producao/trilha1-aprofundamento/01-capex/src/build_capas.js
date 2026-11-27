// Capas das aulas novas do aprofundamento CAPEX (1280×720), no estilo das capas p6-c-*.jpg da Trilha 1:
// fundo chapado, logo, kicker, título, subtítulo em itálico, ícone à direita e selo embaixo. Sem foto de hospedagem.
// Uso: node src/build_capas.js [pasta de saída]   (padrão: docs/trilha1/capas)
// Fontes da marca e logo embutidos como data URI (setContent abre em about:blank, que não lê file://).
const { chromium } = require("playwright"); const path = require("path"); const fs = require("fs");
const D = path.resolve(__dirname, "../../../../docs");
const OUT = path.resolve(process.argv[2] || path.join(D, "trilha1/capas")); fs.mkdirSync(OUT, { recursive: true });
const data = (f, mime) => `data:${mime};base64,` + fs.readFileSync(f).toString("base64");
const LOGO_C = data(path.join(D, "brand/zion-logo-claro.png"), "image/png"), LOGO_E = data(path.join(D, "brand/zion-logo-escuro.png"), "image/png");
const fonte = (n) => data(path.join(D, "assets/fonts", n), "font/woff2");
const FONTS = `@font-face{font-family:Cormorant;font-weight:300 700;src:url(${fonte("cormorant.woff2")}) format("woff2")}@font-face{font-family:Cormorant;font-style:italic;font-weight:300 700;src:url(${fonte("cormorant-italic.woff2")}) format("woff2")}@font-face{font-family:Aventa;font-weight:100 900;src:url(${fonte("aventa.woff2")}) format("woff2")}`;
const C = { preto: "#040605", musgo: "#1B2117", creme: "#FEF5F0", areia: "#DED6BF", terra: "#8B714E", ouro: "#C9B37E" };

// Ícones em SVG (traço simples, como nas capas da Trilha 1)
const ICONE = {
  livro: (cor, fundo) => `<svg width="230" height="300" viewBox="0 0 230 300"><rect x="0" y="0" width="230" height="300" rx="10" fill="${C.creme}"/><rect x="0" y="0" width="26" height="300" rx="4" fill="${C.ouro}"/>
    <rect x="52" y="34" width="140" height="10" rx="5" fill="${C.terra}"/><rect x="52" y="56" width="100" height="8" rx="4" fill="${C.areia}"/>
    ${[96, 116, 136, 156, 176, 196].map((y, i) => `<rect x="52" y="${y}" width="${[150, 120, 140, 110, 145, 90][i]}" height="6" rx="3" fill="${C.areia}"/>`).join("")}
    <text x="52" y="262" font-family="Cormorant" font-size="34" font-weight="600" fill="${C.musgo}">CAPEX</text></svg>`,
  monitor: () => `<svg width="300" height="250" viewBox="0 0 300 250"><rect x="6" y="6" width="288" height="190" rx="16" fill="none" stroke="${C.ouro}" stroke-width="6"/>
    <rect x="36" y="38" width="110" height="12" rx="6" fill="${C.ouro}"/><rect x="36" y="64" width="180" height="8" rx="4" fill="#8E8E80"/><rect x="36" y="82" width="150" height="8" rx="4" fill="#8E8E80"/>
    <circle cx="44" cy="120" r="8" fill="none" stroke="${C.ouro}" stroke-width="3"/><circle cx="44" cy="120" r="4" fill="${C.ouro}"/><rect x="62" y="116" width="110" height="8" rx="4" fill="#8E8E80"/>
    <circle cx="44" cy="146" r="8" fill="none" stroke="#8E8E80" stroke-width="3"/><rect x="62" y="142" width="90" height="8" rx="4" fill="#8E8E80"/>
    <rect x="118" y="214" width="64" height="10" rx="5" fill="${C.ouro}"/>
    <path d="M196 122 L196 180 L210 166 L222 192 L232 187 L220 162 L240 162 Z" fill="${C.creme}" stroke="${C.preto}" stroke-width="3" stroke-linejoin="round"/></svg>`,
  prancheta: () => `<svg width="230" height="290" viewBox="0 0 230 290"><rect x="10" y="26" width="180" height="250" rx="14" fill="#fff" stroke="${C.musgo}" stroke-width="6"/><rect x="62" y="8" width="76" height="34" rx="8" fill="${C.musgo}"/>
    ${[90, 140, 190].map((y, i) => `<rect x="38" y="${y - 14}" width="28" height="28" rx="4" fill="#fff" stroke="${C.musgo}" stroke-width="4"/>${i < 2 ? `<path d="M43 ${y} l7 8 l13 -16" fill="none" stroke="${C.terra}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>` : ""}<rect x="80" y="${y - 4}" width="${[80, 70, 76][i]}" height="8" rx="4" fill="#B9B4A6"/>`).join("")}
    <circle cx="180" cy="236" r="40" fill="${C.terra}"/><text x="180" y="250" text-anchor="middle" font-family="Cormorant" font-size="40" font-weight="700" fill="${C.creme}">6A</text></svg>`,
  lista: () => `<svg width="240" height="300" viewBox="0 0 240 300"><rect x="6" y="6" width="228" height="288" rx="14" fill="${C.creme}"/>
    <text x="30" y="56" font-family="Cormorant" font-size="30" font-weight="600" fill="${C.musgo}">Checklist</text>
    ${[96, 136, 176, 216, 256].map((y, i) => `<rect x="30" y="${y - 14}" width="24" height="24" rx="4" fill="#fff" stroke="${C.musgo}" stroke-width="3.5"/>${i < 3 ? `<path d="M35 ${y - 2} l6 7 l11 -14" fill="none" stroke="${C.terra}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>` : ""}<rect x="68" y="${y - 6}" width="${[140, 120, 132, 110, 126][i]}" height="8" rx="4" fill="${C.areia}"/>`).join("")}</svg>`,
  play: () => `<svg width="260" height="260" viewBox="0 0 260 260"><circle cx="130" cy="130" r="118" fill="none" stroke="${C.musgo}" stroke-width="8"/><path d="M104 80 L190 130 L104 180 Z" fill="${C.musgo}"/></svg>`,
};

const capa = ({ fundo, texto, kicker, sub, selo, seloFundo, seloTexto, logo, titulo, icone, linha }) => `<!doctype html><html><head><meta charset="utf-8"><style>${FONTS}
*{margin:0;box-sizing:border-box}body{width:1280px;height:720px;overflow:hidden;background:${fundo};color:${texto};font-family:Aventa,Arial,sans-serif;position:relative}
.logo{position:absolute;left:72px;top:64px;height:50px}
.k{position:absolute;left:72px;top:174px;color:${kicker.cor};letter-spacing:.2em;text-transform:uppercase;font-weight:700;font-size:22px}
h1{position:absolute;left:68px;top:214px;font-family:Cormorant,Georgia,serif;font-weight:600;font-size:118px;line-height:1;max-width:780px;font-variant-numeric:lining-nums}
h2{position:absolute;left:72px;top:350px;font-family:Cormorant,Georgia,serif;font-style:italic;font-weight:500;font-size:44px;line-height:1.15;max-width:740px}
.l{position:absolute;left:72px;top:${linha ? 478 : 0}px;font-size:21px;letter-spacing:.04em;color:${kicker.cor};border:1.5px solid ${kicker.cor};border-radius:999px;padding:8px 20px}
.s{position:absolute;left:72px;bottom:66px;background:${seloFundo};color:${seloTexto};border-radius:999px;padding:13px 26px;font-size:19px;letter-spacing:.18em;text-transform:uppercase;font-weight:700}
.ic{position:absolute;right:96px;top:50%;transform:translateY(-50%)}
</style></head><body><img class="logo" src="${logo}"><div class="k">${kicker.txt}</div><h1>${titulo}</h1><h2>${sub}</h2>${linha ? `<div class="l">${linha}</div>` : ""}<div class="s">${selo}</div><div class="ic">${icone}</div></body></html>`;

const K = "Pilar 6 · Aprofundamento · CAPEX";
const CAPAS = [
  ["capex-c-ebook.jpg", capa({ fundo: C.musgo, texto: C.creme, kicker: { txt: K, cor: C.ouro }, logo: LOGO_C, titulo: "E-book", sub: "Quanto custa o seu projeto inteiro, bloco por bloco", linha: "Para Airbnb, casas, apartamentos, pousadas e glampings", selo: "PDF · Leitura · 30 páginas", seloFundo: C.ouro, seloTexto: C.musgo, icone: ICONE.livro() })],
  ["capex-c-aula.jpg", capa({ fundo: C.preto, texto: C.creme, kicker: { txt: K, cor: C.ouro }, logo: LOGO_C, titulo: "Aula interativa", sub: "Os sete blocos, a reserva e o caso dos Chalés do Ribeirão", selo: "Comece por aqui", seloFundo: C.ouro, seloTexto: C.musgo, icone: ICONE.monitor() })],
  ["capex-c-faca.jpg", capa({ fundo: C.creme, texto: C.musgo, kicker: { txt: K, cor: C.terra }, logo: LOGO_E, titulo: "Faça agora", sub: "O meu CAPEX · página 6A", selo: "Ferramenta · Tutorial · PDF", seloFundo: C.musgo, seloTexto: C.creme, icone: ICONE.prancheta() })],
  ["capex-c-check.jpg", capa({ fundo: C.terra, texto: C.creme, kicker: { txt: K, cor: C.creme }, logo: LOGO_C, titulo: "Checklist", sub: "Antes de pedir cotação e antes de fechar o número", selo: "PDF · 2 páginas", seloFundo: C.musgo, seloTexto: C.creme, icone: ICONE.lista() })],
  ["capex-c-tutorial.jpg", capa({ fundo: C.ouro, texto: C.musgo, kicker: { txt: K, cor: C.musgo }, logo: LOGO_E, titulo: "Tutorial", sub: "A ficha preenchida passo a passo, com dados fictícios", selo: "Vídeo · Ficha O meu CAPEX", seloFundo: C.musgo, seloTexto: C.creme, icone: ICONE.play() })],
];

(async () => {
  const b = await chromium.launch();
  for (const [nome, html] of CAPAS) {
    const p = await b.newPage({ viewport: { width: 1280, height: 720 } }); await p.setContent(html, { waitUntil: "load" }); await p.evaluate(() => document.fonts.ready);
    const faltam = await p.evaluate(async () => { const t = ["600 100px Cormorant", "italic 500 40px Cormorant", "700 20px Aventa"]; for (const f of t) await document.fonts.load(f); return t.filter((f) => !document.fonts.check(f)); });
    if (faltam.length) throw new Error("fonte da marca não carregou em " + nome + ": " + faltam.join(", "));
    // nada pode sair da tela nem encostar no ícone
    const fora = await p.evaluate(() => { const r = []; const ic = document.querySelector(".ic").getBoundingClientRect();
      document.querySelectorAll("h1,h2,.k,.l,.s,.logo").forEach((e) => { const bb = e.getBoundingClientRect(); if (bb.right > 1280 || bb.bottom > 720 || bb.left < 0) r.push(e.className || e.tagName);
        const range = document.createRange(); range.selectNodeContents(e); const tb = range.getBoundingClientRect(); if (tb.width && tb.right > ic.left - 16 && tb.bottom > ic.top && tb.top < ic.bottom) r.push((e.className || e.tagName) + " encosta no ícone"); });
      const h2 = document.querySelector("h2").getBoundingClientRect(), l = document.querySelector(".l"), s = document.querySelector(".s").getBoundingClientRect();
      if (l && l.getBoundingClientRect().top < h2.bottom + 8) r.push("linha sobre o subtítulo"); if (h2.bottom > s.top - 10) r.push("subtítulo sobre o selo"); return r; });
    if (fora.length) throw new Error(nome + ": " + fora.join(", "));
    await p.waitForTimeout(120); await p.screenshot({ path: path.join(OUT, nome), type: "jpeg", quality: 88 }); await p.close(); console.log("capa", nome);
  }
  await b.close();
})();

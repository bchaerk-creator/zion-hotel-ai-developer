// Capas das cinco aulas do Aprofundamento 6B · Viabilidade (1280×720), mesmo molde das p6a-c-*, no padrão das capas p6-c-*.jpg da Trilha 1
// (PLANO.md 5.8): fundo chapado com a cor do tipo de peça, logo Zion no topo, sobretítulo, título em Playfair Display,
// subtítulo em itálico, selo em pílula embaixo e ícone à direita. Sem foto, sem cabeçalho nem rodapé.
// Cor por tipo: aula #0F1A14 · Faça agora #F5F1E8 · e-book #5B3A29 · checklist #EBE4D4 · tutorial #22382A · dourado #E0BC64.
// Uso: node src/build_capas.js [pasta de saída]   (padrão: docs/trilha1/capas)
// Fontes (Playfair Display e Inter de _motor/fonts) e logo de docs/brand embutidos como data URI.
const { chromium } = require("playwright"); const path = require("path"); const fs = require("fs");
const D = path.resolve(__dirname, "../../../../docs");
const OUT = path.resolve(process.argv[2] || path.join(D, "trilha1/capas")); fs.mkdirSync(OUT, { recursive: true });
const data = (f, mime) => `data:${mime};base64,` + fs.readFileSync(f).toString("base64");
const LOGO_C = data(path.join(D, "brand/zion-logo-claro.png"), "image/png"), LOGO_E = data(path.join(D, "brand/zion-logo-escuro.png"), "image/png");
const fonte = (n) => data(path.join(D, "trilha1/apresentacao/_motor/fonts", n), "font/woff2");
const FONTS = `@font-face{font-family:'Playfair Display';font-weight:400 900;src:url(${fonte("playfair-display-latin-wght-normal.woff2")}) format("woff2")}
@font-face{font-family:'Playfair Display';font-style:italic;font-weight:400 900;src:url(${fonte("playfair-display-latin-wght-italic.woff2")}) format("woff2")}
@font-face{font-family:Inter;font-weight:100 900;src:url(${fonte("inter-latin-wght-normal.woff2")}) format("woff2")}`;
const C = { verde: "#16261C", aula: "#0F1A14", creme: "#F5F1E8", creme2: "#EBE4D4", marrom: "#5B3A29", verde2: "#22382A", ouro: "#E0BC64", ouroT: "#997A1F", cinza: "#B3B4B0", cinzaE: "#8E948C" };

// Ícones em traço simples, no desenho das capas p6-c-*
const ICONE = {
  monitor: () => `<svg width="190" height="130" viewBox="0 0 190 130" style="width:190px"><rect x="3" y="3" width="184" height="110" rx="10" fill="none" stroke="${C.ouro}" stroke-width="4"/>
    <rect x="18" y="18" width="76" height="8" rx="4" fill="${C.ouro}"/><rect x="18" y="35" width="116" height="5" rx="2.5" fill="${C.cinzaE}"/><rect x="18" y="47" width="96" height="5" rx="2.5" fill="${C.cinzaE}"/>
    <circle cx="33" cy="76" r="7" fill="none" stroke="${C.ouro}" stroke-width="2.5"/><circle cx="33" cy="76" r="3.4" fill="${C.ouro}"/><rect x="46" y="73.5" width="70" height="5" rx="2.5" fill="${C.cinzaE}"/>
    <circle cx="33" cy="96" r="7" fill="none" stroke="${C.cinzaE}" stroke-width="2.5"/><rect x="46" y="93.5" width="56" height="5" rx="2.5" fill="${C.cinzaE}"/>
    <rect x="72" y="120" width="46" height="7" rx="3.5" fill="${C.ouro}"/>
    <path d="M128 72 L128 112 L138 102 L146 120 L153 117 L145 99 L159 99 Z" fill="${C.creme}" stroke="${C.aula}" stroke-width="2.5" stroke-linejoin="round"/></svg>`,
  prancheta: () => `<svg width="310" height="360" viewBox="0 0 310 360"><rect x="12" y="20" width="250" height="330" rx="16" fill="#fff" stroke="${C.verde}" stroke-width="7"/><rect x="88" y="6" width="98" height="34" rx="10" fill="${C.verde}"/>
    ${[110, 180, 250].map((y, i) => `<rect x="47" y="${y - 20}" width="40" height="40" rx="7" fill="#fff" stroke="${C.verde}" stroke-width="5"/>${i < 2 ? `<path d="M54 ${y} l9 10 l18 -22" fill="none" stroke="${C.ouroT}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>` : ""}<rect x="106" y="${y - 6}" width="${[130, 110, 130][i]}" height="12" rx="6" fill="${C.cinza}"/>`).join("")}
    <circle cx="258" cy="300" r="52" fill="${C.ouroT}"/><text x="258" y="317" text-anchor="middle" font-family="Playfair Display" font-weight="700" font-size="46" fill="${C.creme}">6B</text></svg>`,
  livro: () => `<svg width="130" height="170" viewBox="0 0 130 170" style="width:130px"><rect x="0" y="0" width="130" height="170" rx="4" fill="${C.creme}"/><rect x="0" y="0" width="13" height="170" fill="${C.ouro}"/>
    <rect x="28" y="22" width="82" height="7" rx="3.5" fill="${C.marrom}" opacity=".85"/><rect x="28" y="36" width="62" height="5" rx="2.5" fill="#B9A89A"/>
    ${[58, 69, 80, 91, 102, 113, 124].map((y, i) => `<rect x="28" y="${y}" width="${[66, 56, 48, 66, 58, 46, 66][i]}" height="3.4" rx="1.7" fill="#B9A89A"/>`).join("")}
    <text x="28" y="155" font-family="Playfair Display" font-size="17" fill="${C.marrom}">ZION</text></svg>`,
  lista: () => `<svg width="260" height="320" viewBox="0 0 260 320"><rect x="6" y="6" width="248" height="308" rx="14" fill="#fff" stroke="${C.verde}" stroke-width="6"/>
    <rect x="36" y="40" width="120" height="12" rx="6" fill="${C.ouroT}"/>
    ${[100, 150, 200, 250].map((y, i) => `<rect x="36" y="${y - 17}" width="34" height="34" rx="6" fill="#fff" stroke="${C.verde}" stroke-width="4.5"/>${i < 2 ? `<path d="M42 ${y} l8 9 l15 -19" fill="none" stroke="${C.ouroT}" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>` : ""}<rect x="86" y="${y - 5}" width="${[130, 112, 124, 100][i]}" height="10" rx="5" fill="${C.cinza}"/>`).join("")}</svg>`,
  play: () => `<svg width="250" height="250" viewBox="0 0 250 250"><circle cx="125" cy="125" r="116" fill="none" stroke="${C.ouro}" stroke-width="8"/><path d="M100 78 L178 125 L100 172 Z" fill="${C.creme}"/></svg>`,
};

const capa = ({ fundo, titulo, sub, selo, escuro, icone, escala = 1 }) => {
  const txt = escuro ? C.creme : C.verde, kick = escuro ? C.ouro : C.ouroT;
  const seloF = escuro ? C.ouro : C.verde, seloT = escuro ? C.aula : C.creme;
  return `<!doctype html><html><head><meta charset="utf-8"><style>${FONTS}
*{margin:0;box-sizing:border-box}body{width:1280px;height:720px;overflow:hidden;background:${fundo};color:${txt};font-family:Inter,Arial,sans-serif;position:relative}
.logo{position:absolute;left:72px;top:66px;height:62px}
.k{position:absolute;left:73px;top:172px;color:${kick};letter-spacing:.16em;text-transform:uppercase;font-weight:700;font-size:21.5px}
h1{position:absolute;left:70px;top:212px;font-family:'Playfair Display',Georgia,serif;font-weight:600;font-size:${Math.round(102 * escala)}px;line-height:1.08;white-space:nowrap;font-variant-numeric:lining-nums}
h2{position:absolute;left:72px;top:${212 + Math.round(100 * escala * 1.08) + 18}px;font-family:'Playfair Display',Georgia,serif;font-style:italic;font-weight:400;font-size:39px;line-height:1.2;max-width:660px}
.s{position:absolute;left:72px;top:616px;height:48px;display:flex;align-items:center;background:${seloF};color:${seloT};border-radius:999px;padding:0 22px;font-size:18.5px;letter-spacing:.14em;text-transform:uppercase;font-weight:700}
.ic{position:absolute;left:${icone.x || 1000}px;top:350px;transform:translate(-50%,-50%) scale(${icone.e || 1})}
</style></head><body><img class="logo" src="${escuro ? LOGO_C : LOGO_E}"><div class="k">Pilar 6 · Aprofundamento 6B</div><h1>${titulo}</h1><h2>${sub}</h2><div class="s">${selo}</div><div class="ic">${icone.svg}</div></body></html>`;
};

const CAPAS = [
  ["p6b-c-aula.jpg", capa({ fundo: C.aula, escuro: true, titulo: "Aula interativa", sub: "Os seis degraus da conta e a conta da Marina, tudo num lugar só", selo: "Comece por aqui", icone: { svg: ICONE.monitor(), e: 1.9 } })],
  ["p6b-c-faca.jpg", capa({ fundo: C.creme, escuro: false, titulo: "Faça agora", sub: "A sua conta · página 6B", selo: "Ferramenta · PDF", icone: { svg: ICONE.prancheta(), e: 1 } })],
  ["p6b-c-tutorial.jpg", capa({ fundo: C.verde2, escuro: true, titulo: "Tutorial da ficha", sub: "A Marina monta a conta dela passo a passo, com dados fictícios", selo: "Vídeo · Passo a passo", icone: { svg: ICONE.play(), e: 0.95, x: 1065 } })],
  ["p6b-c-ebook.jpg", capa({ fundo: C.marrom, escuro: true, titulo: "E-book", sub: "Viabilidade, para ler com calma", selo: "PDF · Leitura", icone: { svg: ICONE.livro(), e: 1.95 } })],
  ["p6b-c-check.jpg", capa({ fundo: C.creme2, escuro: false, titulo: "Checklist", sub: "Antes de mostrar a conta a alguém", selo: "PDF · Checklist", icone: { svg: ICONE.lista(), e: 1 } })],
];

(async () => {
  const b = await chromium.launch();
  for (const [nome, html] of CAPAS) {
    const p = await b.newPage({ viewport: { width: 1280, height: 720 } }); await p.setContent(html, { waitUntil: "load" }); await p.evaluate(() => document.fonts.ready);
    const faltam = await p.evaluate(async () => { const t = ["600 100px 'Playfair Display'", "italic 400 36px 'Playfair Display'", "700 20px Inter"]; for (const f of t) await document.fonts.load(f); return t.filter((f) => !document.fonts.check(f)); });
    if (faltam.length) throw new Error("fonte não carregou em " + nome + ": " + faltam.join(", "));
    // nada sai da tela, o texto não encosta no ícone e o subtítulo não encosta no selo
    const fora = await p.evaluate(() => {
      const r = []; const ic = document.querySelector(".ic svg").getBoundingClientRect();
      document.querySelectorAll("h1,h2,.k,.s,.logo").forEach((e) => {
        const bb = e.getBoundingClientRect(); if (bb.right > 1240 || bb.bottom > 690 || bb.left < 0 || bb.top < 0) r.push((e.className || e.tagName) + " fora da margem");
        const range = document.createRange(); range.selectNodeContents(e); const tb = range.getBoundingClientRect();
        if (tb.width && tb.right > ic.left - 24 && tb.bottom > ic.top && tb.top < ic.bottom) r.push((e.className || e.tagName) + " encosta no ícone");
      });
      if (ic.right > 1240 || ic.top < 20 || ic.bottom > 700) r.push("ícone fora da margem");
      const h2 = document.querySelector("h2").getBoundingClientRect(), s = document.querySelector(".s").getBoundingClientRect();
      if (h2.bottom > s.top - 24) r.push("subtítulo sobre o selo"); return r;
    });
    if (fora.length) throw new Error(nome + ": " + fora.join(", "));
    await p.waitForTimeout(100); await p.screenshot({ path: path.join(OUT, nome), type: "jpeg", quality: 90 }); await p.close(); console.log("capa", nome);
  }
  await b.close();
})();

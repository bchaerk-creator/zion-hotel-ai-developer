// Imprime um HTML de páginas A4 (section.pg) em PDF e confere a altura de cada página.
// Uso: node src/render.js <entrada.html> <saida.pdf> [pasta-png]
// Falha (código 1) se alguma página passar de 297 mm ou se o conteúdo invadir o rodapé.
const { chromium } = require("playwright"); const path = require("path"); const fs = require("fs");
(async () => {
  const [html, pdf, png] = process.argv.slice(2).map((p) => p && path.resolve(p));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto("file://" + html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250);
  const faltam = await p.evaluate(async () => { const t = ["500 20px Titulo", "italic 500 20px Titulo", "400 12px Texto"]; for (const f of t) await document.fonts.load(f); return t.filter((f) => !document.fonts.check(f)); });
  if (faltam.length) throw new Error("fonte não carregou: " + faltam.join(", "));
  const r = await p.evaluate(() => {
    const mm = 96 / 25.4; const out = [];
    document.querySelectorAll("section.pg").forEach((s, i) => {
      const top = s.getBoundingClientRect().top; const h = s.getBoundingClientRect().height;
      const rod = s.querySelector(".rod"); const limite = rod ? rod.getBoundingClientRect().top - top - 1.5 * mm : h - 8 * mm;
      let fundo = 0; s.querySelectorAll(".in *").forEach((e) => { const bb = e.getBoundingClientRect(); if (bb.height) fundo = Math.max(fundo, bb.bottom - top); });
      out.push({ pagina: i + 1, alturaMm: +(h / mm).toFixed(1), conteudoMm: +(fundo / mm).toFixed(1), limiteMm: +(limite / mm).toFixed(1), folgaMm: +((limite - fundo) / mm).toFixed(1) });
    });
    return out;
  });
  let erro = 0;
  for (const x of r) { const ok = x.alturaMm <= 297.1 && x.folgaMm >= 0; if (!ok) erro++; console.log(`pág ${String(x.pagina).padStart(2)}  altura ${x.alturaMm} mm  conteúdo até ${x.conteudoMm} mm  folga ${x.folgaMm} mm ${ok ? "" : "  <<< TRANSBORDA"}`); }
  await p.pdf({ path: pdf, format: "A4", printBackground: true, preferCSSPageSize: true });
  if (png) {
    fs.mkdirSync(png, { recursive: true }); const secs = await p.$$("section.pg");
    for (let i = 0; i < secs.length; i++) await secs[i].screenshot({ path: path.join(png, `p${String(i + 1).padStart(2, "0")}.png`) });
  }
  console.log("pdf", pdf, r.length, "páginas;", erro ? erro + " com problema" : "todas dentro de 297 mm");
  await b.close(); process.exit(erro ? 1 : 0);
})();

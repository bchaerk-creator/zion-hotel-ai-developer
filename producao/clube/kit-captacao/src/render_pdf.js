// Imprime o guia em PDF A4 e confere transbordo. Uso: node src/render_pdf.js <build/guia.html> <saida.pdf> [pasta-png]
const { chromium } = require("playwright"); const path = require("path"); const fs = require("fs");
(async () => {
  const [html, pdf, png] = process.argv.slice(2).map((p) => p && path.resolve(p));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto("file://" + html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  // Transbordo: nenhum elemento de texto pode passar do topo do rodapé (ou do fim da página, se não houver rodapé).
  const prob = await p.evaluate(() => [...document.querySelectorAll("section.pg")].map((pg, i) => {
    const r = pg.getBoundingClientRect(); const rod = pg.querySelector(".rod"); const lim = rod ? rod.getBoundingClientRect().top - 2 : r.bottom - 8;
    let max = 0, quem = "";
    pg.querySelectorAll("p,li,tr,h2,h3,div.card,div.fonte6,div.ex,div.caixa,div.ouro,table,a,img").forEach((e) => { if (e.closest(".rod")) return; const q = e.getBoundingClientRect(); if (q.bottom > max) { max = q.bottom; quem = e.tagName + "." + e.className + " " + (e.textContent || "").slice(0, 40); } });
    return { pagina: i + 1, folga_px: Math.round(lim - max), quem };
  }));
  prob.forEach((x) => console.log(`pág. ${x.pagina}: folga ${x.folga_px}px${x.folga_px < 0 ? "  TRANSBORDA: " + x.quem : ""}`));
  await p.pdf({ path: pdf, format: "A4", printBackground: true, preferCSSPageSize: true });
  if (png) {
    fs.mkdirSync(png, { recursive: true }); const els = await p.$$("section.pg");
    for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: path.join(png, `pag${String(i + 1).padStart(2, "0")}.png`) });
  }
  console.log("pdf", pdf, prob.length, "páginas", prob.some((x) => x.folga_px < 0) ? "COM TRANSBORDO" : "sem transbordo"); await b.close();
})();

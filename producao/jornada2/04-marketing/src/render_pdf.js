// Imprime o resumo em PDF. Uso: node src/render_pdf.js <build/resumo.html> <saida.pdf>
const { chromium } = require("playwright"); const path = require("path");
(async () => {
  const [html, pdf] = process.argv.slice(2).map((p) => path.resolve(p));
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto("file://" + html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
  await p.pdf({ path: pdf, format: "A4", printBackground: true, preferCSSPageSize: true });
  const n = await p.evaluate(() => document.querySelectorAll("section.pg").length);
  console.log("pdf", pdf, n, "páginas"); await b.close();
})();

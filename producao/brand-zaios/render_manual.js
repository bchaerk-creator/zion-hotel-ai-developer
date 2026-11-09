// Renderiza as aplicações (PNG) e o manual (PDF + PNG por página). Uso: node producao/brand-zaios/render_manual.js <pasta do kit>
const { chromium } = require("playwright"); const fs = require("fs"); const path = require("path");
const K = path.resolve(process.argv[2]); const A = path.join(K, "aplicacoes"); const T = JSON.parse(fs.readFileSync(path.join(A, "tamanhos.json"), "utf8"));
(async () => {
  const b = await chromium.launch();
  for (const [n, [w, h]] of Object.entries(T)) {
    const p = await b.newPage({ viewport: { width: w, height: h } }); await p.goto("file://" + path.join(A, n + ".html")); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
    await p.screenshot({ path: path.join(A, n + ".png") }); await p.close();
  }
  const p = await b.newPage(); await p.goto("file://" + path.join(K, "manual.html")); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.pdf({ path: path.join(K, "ZAIOS_SYSTEM_Manual_de_Identidade_v1.1.pdf"), format: "A4", landscape: true, printBackground: true });
  const pv = await b.newPage({ viewport: { width: 1123, height: 794 } }); await pv.goto("file://" + path.join(K, "manual.html")); await pv.evaluate(() => document.fonts.ready);
  const n = await pv.evaluate(() => document.querySelectorAll(".pg").length); fs.mkdirSync(path.join(K, "manual-paginas"), { recursive: true });
  for (let i = 0; i < n; i++) { const el = (await pv.$$(".pg"))[i]; await el.screenshot({ path: path.join(K, "manual-paginas", `pagina-${String(i + 1).padStart(2, "0")}.png`) }); }
  await b.close(); console.log("aplicações", Object.keys(T).length, "· manual", n, "páginas");
})();

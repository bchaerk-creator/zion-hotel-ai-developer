// Renderiza os SVG do kit em PNG (Chromium/Playwright). Uso: node producao/brand-zaios/render_png.js <pasta do kit>
const { chromium } = require("playwright"); const fs = require("fs"); const path = require("path");
const K = path.resolve(process.argv[2]); const M = JSON.parse(fs.readFileSync(path.join(K, "manifesto.json"), "utf8"));
const larguras = (n) => n.includes("favicon") ? [16, 32, 48, 180, 192, 512] : n.includes("icone-app") ? [1024, 512, 180] : n.includes("simbolo") ? [1024, 256] : [2400, 1200];
(async () => {
  const b = await chromium.launch(); fs.mkdirSync(path.join(K, "png"), { recursive: true }); const pngs = [];
  for (const a of M.arquivos) {
    const nome = path.basename(a.arquivo, ".svg"), src = fs.readFileSync(path.join(K, a.arquivo), "utf8");
    for (const lw of larguras(nome)) {
      const lh = Math.round(lw * a.altura / a.largura);
      const p = await b.newPage({ viewport: { width: lw, height: lh }, deviceScaleFactor: 1 });
      await p.setContent(`<html><body style="margin:0;background:transparent">${src.replace(/width="[\d.]+" height="[\d.]+"/, `width="${lw}" height="${lh}"`)}</body></html>`);
      const out = path.join(K, "png", `${nome}-${lw}.png`);
      await p.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: lw, height: lh } }); await p.close(); pngs.push(path.relative(K, out));
    }
  }
  await b.close(); M.png = pngs; fs.writeFileSync(path.join(K, "manifesto.json"), JSON.stringify(M, null, 1)); console.log(pngs.length, "PNG");
})();

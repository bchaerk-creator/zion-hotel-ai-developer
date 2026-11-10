// Uso: node record_h.js <rec.json> <outdir>: grava as cenas de aula.html (W×H, env W/H, padrão 1920×1080) numa gravação contínua
const { chromium } = require("playwright"); const fs = require("fs"); const path = require("path");
const [, , specPath, outDir] = process.argv; const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
const W = +(process.env.W || 1920), H = +(process.env.H || 1080); const PAGE = process.env.PAGE || "aula.html"; const sep = PAGE.includes("?") ? "&" : "?";
(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch(); const timings = [];
  const ctx = await b.newContext({ viewport: { width: W, height: H }, recordVideo: { dir: outDir, size: { width: W, height: H } }, deviceScaleFactor: 1 });
  const page = await ctx.newPage(); const T0 = Date.now();
  await page.goto(`file://${__dirname}/${PAGE}${sep}s=0`); await page.waitForTimeout(900);
  for (let i = 0; i < spec.scenes.length; i++) {
    const sc = spec.scenes[i];
    await page.goto(`file://${__dirname}/${PAGE}${sep}s=${i}`);
    await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map((im) => im.complete ? 1 : new Promise((r) => { im.onload = im.onerror = r; }))); });
    const t0 = Date.now();
    await page.waitForTimeout(sc.minMs || 4000);
    const total = Date.now() - t0; timings.push({ i, start_ms: t0 - T0, ms: total }); console.log(`cena ${i}: ${(total / 1000).toFixed(1)}s`);
  }
  const v = page.video(); await ctx.close(); const vp = await v.path(); await b.close();
  fs.writeFileSync(path.join(outDir, "timings.json"), JSON.stringify({ video: vp, scenes: timings }, null, 1));
})();

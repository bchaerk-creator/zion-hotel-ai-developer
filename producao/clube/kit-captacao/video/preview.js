// Prévia estática de todas as cenas (para revisão visual antes de gravar). Uso: node video/preview.js <pagina?d=x> <n-cenas> <W> <H> <saida-dir>
const { chromium } = require("playwright"); const fs = require("fs"); const path = require("path");
const [, , page, n, W, H, out] = process.argv; fs.mkdirSync(out, { recursive: true });
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +W, height: +H } });
  for (let i = 0; i < +n; i++) { await p.goto(`file://${__dirname}/${page}&s=${i}`); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(3200);
    await p.screenshot({ path: path.join(out, `c${String(i).padStart(2, "0")}.jpg`), type: "jpeg", quality: 70 }); }
  await b.close(); })();

// Renderiza as capas 1080x1080 listadas por build_entrega.py. Uso: node producao/utilitarios/render_capas.js
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const jobs = JSON.parse(fs.readFileSync(path.join(__dirname, '.build_capas/jobs.json')));
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1080 } });
  for (const [html, out] of jobs) { await p.goto('file://' + html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.screenshot({ path: out, type: 'jpeg', quality: 88 }); console.log('capa', out); }
  await b.close(); })();

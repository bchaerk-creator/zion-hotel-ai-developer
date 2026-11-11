// Gera o PDF do e-book e ajusta a fonte das páginas que transbordam. Uso: node render_ebook.js [pasta-previas]
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const HTML = 'file://' + path.resolve(__dirname, 'dist/ebook.html'), PREV = process.argv[2];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto(HTML, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  const rel = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('.pg').forEach(pg => {
      const m = pg.querySelector('.miolo'); const col = pg.querySelector('.col');
      const transborda = () => m && (m.scrollHeight > m.clientHeight + 1 || (col && col.scrollWidth > col.clientWidth + 2));
      let fs = 9.6, passos = 0, lh = 6.6;
      if (pg.classList.contains('ex')) { while (transborda() && lh > 5.2) { lh -= 0.2; m.style.setProperty('--lh', lh.toFixed(1) + 'mm'); passos++; }
        while (transborda() && fs > 8.4) { fs -= 0.15; m.style.setProperty('--fs', fs.toFixed(2) + 'pt'); passos++; } }
      if (col && transborda()) { while (transborda() && fs > 8.1) { fs -= 0.15; col.style.setProperty('--fs', fs.toFixed(2) + 'pt'); passos++; } }
      out.push({ n: +pg.dataset.n, ajustada: passos ? fs.toFixed(2) : null, transborda: !!transborda() });
    });
    return out;
  });
  const prob = rel.filter(r => r.transborda), aj = rel.filter(r => r.ajustada);
  console.log('páginas:', rel.length, '| ajustadas:', aj.map(r => r.n + '@' + r.ajustada + 'pt').join(' ') || 'nenhuma', '| ainda transbordam:', prob.map(r => r.n).join(',') || 'nenhuma');
  await p.pdf({ path: path.resolve(__dirname, 'dist/Seu-Airbnb-Esta-Vazio-Zion-Collection.pdf'), preferCSSPageSize: true, printBackground: true });
  if (PREV) { fs.mkdirSync(PREV, { recursive: true }); for (const n of (process.argv[3] || '1,5,6,7,9,44,45,55,60').split(',')) { const el = p.locator(`.pg[data-n="${n}"]`); await el.screenshot({ path: `${PREV}/p${n.padStart(2, '0')}.png` }); } }
  await b.close(); process.exit(prob.length ? 2 : 0);
})();

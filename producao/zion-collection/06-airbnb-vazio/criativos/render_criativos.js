// Renderiza cada criativo em PNG 1080×1350 e checa se o texto invade a faixa do botão. Uso: node criativos/render_criativos.js
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + path.resolve(__dirname, 'dist/criativos.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  for (const id of await p.$$eval('.c', e => e.map(x => x.id))) {
    const el = p.locator('#' + id);
    const col = await el.evaluate(c => { const top = c.getBoundingClientRect().top, cta = c.querySelector('.cta').getBoundingClientRect().top - top;
      const els = [...c.querySelectorAll('h1,.sub,.cal,.tach,.ab,.passos,.leg,.foto')]; const r = els.map(e => e.getBoundingClientRect());
      const choque = []; els.forEach((e, i) => { if (r[i].bottom - top > cta - 10) choque.push(e.className || e.tagName); for (let j = i + 1; j < els.length; j++) { const a = r[i], b2 = r[j]; if (a.left < b2.right && b2.left < a.right && a.top < b2.bottom && b2.top < a.bottom) choque.push((e.className || e.tagName) + '×' + (els[j].className || els[j].tagName)); } });
      return choque; });
    await el.screenshot({ path: path.resolve(__dirname, `dist/${id}.png`) }); console.log(id, col.length ? 'SOBREPOSIÇÃO: ' + col.join(', ') : 'ok');
  }
  await b.close();
})();

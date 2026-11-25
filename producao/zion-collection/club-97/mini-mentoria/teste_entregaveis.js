// node teste_entregaveis.js <slug> <hashOferta> <dirSaida> [urlBase]
const { chromium } = require('playwright');
const [slug, hash, out, base] = process.argv.slice(2);
const url = (base || 'https://infoprodutos-zion.clickmax.space/') + slug + '?utm_source=meta&utm_medium=paid&utm_campaign=teste&utm_content=ent';
(async () => {
  const b = await chromium.launch();
  const res = {};
  for (const [nome, vp] of [['mobile', { width: 390, height: 844 }], ['desktop', { width: 1366, height: 800 }]]) {
    const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: nome === 'mobile' ? 2 : 1 });
    const p = await ctx.newPage();
    const erros = [];
    p.on('pageerror', e => erros.push(String(e)));
    await p.goto(url, { waitUntil: 'load', timeout: 60000 }).catch(e => erros.push('goto ' + e.message));
    await p.waitForTimeout(2500);
    const r = await p.evaluate((hash) => {
      const sec = document.querySelector('#entregaveis');
      const secs = [...document.querySelectorAll('[data-cx-section]')].map(s => s.getAttribute('data-cx-section') + (s.id ? '#' + s.id : ''));
      const prev = sec && sec.previousElementSibling;
      const fr = document.querySelector('iframe[data-testid="public-checkout-iframe"], .cm-checkout iframe, iframe[src*="payments.clickmax"]');
      return {
        sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
        secoes: secs, existe: !!sec, cartoes: document.querySelectorAll('.ent-card').length,
        antes: prev ? (prev.id || prev.tagName) : null,
        iframeSrc: fr ? fr.src : null, hashOk: fr ? fr.src.includes(hash) : false,
        ctas: [...document.querySelectorAll('[data-cx-cta]')].map(a => a.getAttribute('href')),
        spans: document.querySelectorAll('.ent-sec span').length,
        overflowSec: sec ? sec.scrollWidth - sec.clientWidth : null,
        textoPix: /calculadora|simulador|reuni|acompanhamento|mentoria ao vivo/i.test(sec ? sec.innerText : ''),
      };
    }, hash);
    r.erros = erros;
    r.utmNoIframe = r.iframeSrc ? /utm_source=meta/.test(r.iframeSrc) : false;
    if (nome === 'mobile') {
      const el = await p.$('#entregaveis');
      const box = await el.boundingBox();
      r.altura = Math.round(box.height);
      const n = 3, h = Math.ceil(box.height / n);
      for (let i = 0; i < n; i++) {
        await p.screenshot({ path: `${out}/${slug}-entregaveis-mobile-${i + 1}.png`, fullPage: true, clip: { x: 0, y: box.y + i * h, width: 390, height: Math.min(h, box.height - i * h) } });
      }
      // CTA leva ao checkout
      await p.click('a[data-cx-cta]');
      await p.waitForTimeout(800);
      r.ctaScrollY = await p.evaluate(() => { const t = document.querySelector('#pagar').getBoundingClientRect().top; return Math.round(t); });
    } else {
      const el = await p.$('#entregaveis');
      await el.screenshot({ path: `${out}/${slug}-entregaveis-desktop.png` });
    }
    res[nome] = r;
    await ctx.close();
  }
  await b.close();
  console.log(JSON.stringify(res, null, 1));
})();

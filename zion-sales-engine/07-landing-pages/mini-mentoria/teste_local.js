// Teste local (Playwright) das variantes: node teste_local.js
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const PROIBIDOS = [/sócio/i, /receber investimento/i, /faturamento/i, /garantid[oa]s? (de )?(retorno|renda|lucro)/i, /consultoria/i, /R\$ ?97/, /rede de investidores/i, /simulador/i, /calculadora/i];
(async () => {
  const b = await chromium.launch(); let falhas = 0;
  for (const v of ['a', 'b']) {
    const arq = path.join(__dirname, `variante-${v}`, 'index.html');
    const html = fs.readFileSync(arq, 'utf8');
    for (const m of html.matchAll(/.{0,25}(reuni[aã]o|atendimento individual)/gi)) if (!/(não há|nem|sem) /i.test(m[0])) { console.log(v, 'REUNIAO/ATEND fora de negação:', m[0]); falhas++; }
    for (const re of PROIBIDOS) if (re.test(html.replace(/<style>[\s\S]*?<\/style>/, ''))) { console.log(v, 'PROIBIDO:', re); falhas++; }
    for (const [nome, w, h] of [['mobile', 390, 844], ['desktop', 1366, 800]]) {
      const p = await b.newPage({ viewport: { width: w, height: h } });
      const erros = []; p.on('pageerror', e => erros.push(String(e)));
      await p.goto('file://' + arq, { waitUntil: 'domcontentloaded' }); await p.waitForTimeout(700);
      const r = await p.evaluate(() => {
        const ctas = [...document.querySelectorAll('[data-cx-cta]')];
        const hero = document.querySelector('#hero');
        return {
          overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
          checkout: document.querySelectorAll('[data-cx-checkout]').length,
          spans: document.querySelectorAll('span').length, scripts: document.querySelectorAll('script').length,
          secoes: [...new Set([...document.querySelectorAll('[data-cx-section]')].map(s => s.dataset.cxSection))].join(','),
          ctas: ctas.length, ctasSemPreco: ctas.filter(a => !/R\$ ?47/.test(a.textContent)).length,
          ctaNoHero: hero.querySelectorAll('[data-cx-cta]').length,
          ctaPrimeiroY: Math.round(ctas[0].getBoundingClientRect().top + scrollY),
          h1: document.querySelector('h1').innerText,
        };
      });
      const bad = r.overflow || r.checkout !== 1 || r.spans || r.scripts || r.ctasSemPreco || erros.length;
      if (bad) falhas++;
      console.log(v.toUpperCase(), nome, JSON.stringify(r), 'erros:', erros.length, bad ? 'FALHA' : 'ok');
      await p.screenshot({ path: path.join(process.env.SHOTS || __dirname, `local-${v}-${nome}.png`), fullPage: nome === 'mobile' });
    }
  }
  await b.close(); console.log(falhas ? 'FALHAS: ' + falhas : 'TUDO OK'); process.exit(falhas ? 1 : 0);
})();

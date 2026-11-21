// Captura a ferramenta REAL (dados fictícios) em tela de notebook, para substituir a tela ilustrada do card 04.
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 760, height: 497 }, deviceScaleFactor: 1 });
  await p.route('**/jspdf*', r => r.fulfill({ body: '' })); await p.goto('file://' + path.resolve(__dirname, '../dist/index.html') + '#ferramenta-lacuna');
  await p.addStyleTag({ content: 'main{max-width:none!important;padding:12px 40px!important}.stk{position:static!important}body{zoom:1}' });
  await p.evaluate(() => { const m = document.querySelector('main'); m.style.display = 'grid'; m.style.gridTemplateColumns = '1fr'; window.scrollTo(0, 0); });
  // mostra o resultado: rola até o bloco verde e usa 2 colunas via zoom menor
  await p.evaluate(() => { document.body.style.zoom = '1'; });
  await p.evaluate(() => { const r = document.querySelector('.res'); r.scrollIntoView(); window.scrollBy(0, -70); });
  await p.evaluate(() => { const d = document.createElement('div'); d.textContent = 'Exemplo com dados fictícios · ferramenta real do portal'; d.style.cssText = 'position:fixed;left:0;right:0;bottom:0;background:#1B2117;color:#C9B37E;font:600 15px Aventa,sans-serif;text-align:center;padding:10px;letter-spacing:.06em;z-index:99'; document.body.appendChild(d); });
  await p.waitForTimeout(300); await p.screenshot({ path: path.resolve(__dirname, 'src/tela-real-notebook.png') }); await b.close(); console.log('ok');
})();

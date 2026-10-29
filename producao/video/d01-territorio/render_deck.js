#!/usr/bin/env node
// Converte um deck do tipo Slides (project/deck.json + project/slides/<id>.html + imagens /_blob/<id>)
// em slides/NN.png 1920x1080, na ordem do deck. Substitui o passo do PDF quando a aula está no Claude.
// Uso: node render_deck.js <pasta-com-project/> [pasta-das-imagens]
const path = require('path');
const fs = require('fs');

let chromium;
try { ({ chromium } = require('playwright')); } catch {
  ({ chromium } = require(path.join(require('child_process').execSync('npm root -g').toString().trim(), 'playwright')));
}

const raiz = path.resolve(process.argv[2] || '.');
const imagens = path.resolve(process.argv[3] || raiz);
const deck = JSON.parse(fs.readFileSync(path.join(raiz, 'project/deck.json'), 'utf8'));
const saida = path.join(__dirname, 'slides');
fs.mkdirSync(saida, { recursive: true });

const blob = id => {
  const arq = fs.readdirSync(imagens).find(f => f.startsWith(id + '.'));
  if (!arq) throw new Error(`imagem ${id} não encontrada em ${imagens}`);
  return 'file://' + path.join(imagens, arq);
};
const fontes = Object.values(deck.faces || {}).filter(f => f.href).map(f => `<link rel="stylesheet" href="${f.href}">`).join('');

// Reset equivalente ao da apresentação: sem margens, caixa 1920x1080, filhos fixos relativos ao slide.
const base = `*{margin:0;padding:0;box-sizing:border-box}html,body{width:1920px;height:1080px;overflow:hidden}
section{position:relative;width:1920px;height:1080px;overflow:hidden;line-height:1.2}
section *{position:relative}aside{display:none}img{display:block}table{border-collapse:collapse}
th,td{text-align:left;vertical-align:top;padding:16px 20px}`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  for (const [i, id] of deck.order.entries()) {
    let html = fs.readFileSync(path.join(raiz, 'project/slides', `${id}.html`), 'utf8');
    html = html.replace(/\/_blob\/([0-9a-f]+)/g, (_, b) => blob(b));
    // a página precisa estar em file:// para o navegador aceitar as imagens locais
    const tmp = path.join(imagens, `.slide-${id}.html`);
    fs.writeFileSync(tmp, `<!doctype html><html><head><meta charset="utf-8">${fontes}<style>${base}</style></head><body>${html}</body></html>`);
    await page.goto('file://' + tmp, { waitUntil: 'networkidle' });
    await page.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
    fs.unlinkSync(tmp);
    await page.evaluate(() => document.fonts.ready);
    const arq = path.join(saida, `${String(i + 1).padStart(2, '0')}.png`);
    await page.locator('section').first().screenshot({ path: arq });
    console.log(path.basename(arq), id);
  }
  await browser.close();
})();

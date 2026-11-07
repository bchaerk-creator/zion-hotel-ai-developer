// Renderiza os criativos 1080×1350 de um produto a partir de creatives/<ID>.json → out/criativos/<ID>/ZAR-<ID>-CRnn.png + copies.csv
// Uso: node creatives/render.js A02 [A03 ...]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const REPO = '/home/user/zion-hotel-ai-developer/docs';
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const ttl = t => esc(t).replace(/\*(.+?)\*/g, '<em>$1</em>');
const csv = v => '"' + String(v == null ? '' : v).replace(/"/g, '""') + '"';
function art(c, assets) {
  const L = c.layout || 'text';
  const shot = c.shot ? `<img class="shot" src="${assets}/tela-${c.shot}.png">` : '';
  const list = (c.list || []).map((t, k) => `<li><b>${c.listMark === 'x' ? '✕' : c.listMark === 'check' ? '✓' : String(k + 1).padStart(2, '0')}</b><span>${esc(t)}</span></li>`).join('');
  const cmp = c.compare ? `<div class="cmp"><div class="c bad"><h4>${esc(c.compare[0].h)}</h4>${c.compare[0].items.map(i => `<p>✕ ${esc(i)}</p>`).join('')}</div><div class="c good"><h4>${esc(c.compare[1].h)}</h4>${c.compare[1].items.map(i => `<p>✓ ${esc(i)}</p>`).join('')}</div></div>` : '';
  return `<div class="cr L-${L}${c.photo ? ' ph' : ''}">${c.photo ? `<div class="bg" style="background-image:url(${REPO}/assets/operacoes/${c.photo}.webp)"></div><div class="veil"></div>` : ''}
<div class="top"><img src="${REPO}/brand/zion-logo-claro.png" class="logo"><span>Zion Collection Club</span></div>
${L === 'shot-right' || L === 'shot-top' ? `<div class="shots">${shot}</div>` : ''}
<div class="txt"><div class="k">${esc(c.kicker)}</div>${c.big ? `<div class="big">${esc(c.big)}</div>` : ''}<h1>${ttl(c.title)}</h1>${c.text ? `<p class="t">${esc(c.text)}</p>` : ''}${list ? `<ol>${list}</ol>` : ''}${cmp}</div>
${c.caption ? `<div class="cap">${esc(c.caption)}</div>` : ''}
<div class="bar"><span class="pill">${esc(c.button || 'Saiba mais')}</span><span class="price">R$ 27 · pagamento único</span></div>
${c.note ? `<div class="note">${esc(c.note)}</div>` : ''}</div>`;
}
const CSS = `@font-face{font-family:Cormorant;src:url(${REPO}/assets/fonts/cormorant.woff2)}@font-face{font-family:Cormorant;font-style:italic;src:url(${REPO}/assets/fonts/cormorant-italic.woff2)}@font-face{font-family:Aventa;src:url(${REPO}/assets/fonts/aventa.woff2)}
*{box-sizing:border-box;margin:0}body{width:1080px;height:1350px;overflow:hidden;background:#040605}
.cr{position:relative;width:1080px;height:1350px;background:linear-gradient(165deg,#1B2117 0%,#10150e 55%,#040605 100%);color:#FEF5F0;font-family:Aventa,sans-serif;overflow:hidden}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}.veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,6,5,.5) 0%,rgba(4,6,5,.2) 30%,rgba(4,6,5,.86) 62%,#040605 100%)}
.top{position:absolute;top:56px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;z-index:3}.logo{height:52px}.top span{font-size:20px;letter-spacing:.3em;text-transform:uppercase;color:#C9B37E}
.txt{position:absolute;left:72px;right:72px;bottom:190px;z-index:2}
.k{font-size:24px;letter-spacing:.24em;text-transform:uppercase;color:#C9B37E;margin-bottom:20px}
h1{font-family:Cormorant,serif;font-weight:500;font-size:84px;line-height:1.03;color:#FEF5F0;margin-bottom:24px}h1 em{color:#C9B37E;font-style:italic}
.t{font-size:33px;line-height:1.42;color:#DED6BF}
.big{font-family:Cormorant,serif;font-size:190px;line-height:.95;color:#C9B37E;margin-bottom:10px}
ol{list-style:none;padding:0}li{display:flex;gap:22px;align-items:baseline;padding:15px 0;border-top:1px solid rgba(201,179,126,.25);font-size:31px;line-height:1.32}li b{font-family:Cormorant,serif;font-weight:500;font-size:36px;color:#C9B37E;min-width:44px}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:8px}.c{border-radius:22px;padding:24px 22px}.c h4{font-size:22px;letter-spacing:.14em;text-transform:uppercase;margin-bottom:12px}.c p{font-size:27px;line-height:1.35;margin:9px 0}
.c.bad{background:rgba(163,67,47,.16);border:1px solid rgba(163,67,47,.45)}.c.bad h4{color:#e7a08f}.c.good{background:rgba(201,179,126,.12);border:1px solid rgba(201,179,126,.5)}.c.good h4{color:#C9B37E}
.shots{position:absolute;z-index:1}.L-shot-top .shots{top:150px;left:0;right:0;height:520px;display:flex;justify-content:center}.L-shot-top .shot{height:100%}
.L-shot-right .shots{top:150px;left:0;right:0;height:470px;display:flex;justify-content:center}.L-shot-right .shot{height:100%}
.shot{border-radius:28px;box-shadow:0 30px 70px rgba(0,0,0,.6);border:2px solid rgba(201,179,126,.35)}
.L-shot-top h1,.L-shot-right h1{font-size:74px}
.L-text .txt,.L-list .txt{top:150px;bottom:170px;display:flex;flex-direction:column;justify-content:center}.L-text h1{font-size:108px}.L-list h1{font-size:96px}.L-text .t{font-size:38px}.L-list li{font-size:36px;padding:20px 0}
.L-photo h1{font-size:96px}
.cap{position:absolute;top:130px;left:72px;font-size:20px;letter-spacing:.12em;color:#DED6BF;z-index:3}
.bar{position:absolute;left:72px;right:72px;bottom:72px;display:flex;align-items:center;justify-content:space-between;z-index:3}
.pill{background:#C9B37E;color:#040605;font-size:30px;font-weight:600;padding:22px 40px;border-radius:999px}.price{font-size:24px;color:#DED6BF;letter-spacing:.04em}
.note{position:absolute;left:72px;right:72px;bottom:28px;font-size:17px;color:#DED6BF;opacity:.7;z-index:3}`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const id of process.argv.slice(2)) {
    const cfg = JSON.parse(fs.readFileSync(path.join(__dirname, id + '.json'), 'utf8'));
    const out = path.join(__dirname, '..', 'out', 'criativos', id); fs.mkdirSync(out, { recursive: true });
    const assets = path.join(__dirname, '..', 'out', 'promo', id);
    const rows = [['codigo', 'angulo', 'arquivo', 'texto_principal', 'titulo', 'descricao', 'botao', 'url']];
    const problems = [];
    for (const [k, c] of cfg.creatives.entries()) {
      const code = `ZAR-${id}-CR${String(k + 1).padStart(2, '0')}`;
      const hf = path.join(out, '_tmp.html'); fs.writeFileSync(hf, `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head><body>${art(c, assets)}</body></html>`); await p.goto('file://' + hf, { waitUntil: 'load' });
      await p.evaluate(() => document.fonts.ready);
      // ajusta o título até o texto caber sem invadir a tela da ferramenta nem o topo
      const fit = await p.evaluate(() => { const t = document.querySelector('.txt'), h = document.querySelector('h1'), sh = document.querySelector('.shots');
        const limit = () => sh ? sh.getBoundingClientRect().bottom + 24 : 140; let fs = parseFloat(getComputedStyle(h).fontSize), n = 0;
        while (t.getBoundingClientRect().top < limit() && fs > 50 && n < 30) { fs -= 3; h.style.fontSize = fs + 'px'; n++; }
        return { ok: t.getBoundingClientRect().top >= limit(), fs }; });
      if (!fit.ok) problems.push(code + ' texto não coube');
      await p.screenshot({ path: path.join(out, code + '.png') });
      const utm = `?utm_source=meta&utm_medium=paid&utm_campaign=zar-${id.toLowerCase()}&utm_content=${code.toLowerCase()}`;
      rows.push([code, c.angle, code + '.png', c.primary, c.headline, c.description, 'Saiba mais', `https://infoprodutos-zion.clickmax.space/zar-${id.toLowerCase()}${utm}`]);
      for (const [f, max] of [['headline', 40], ['description', 30]]) if ((c[f] || '').length > max) problems.push(`${code} ${f} com ${c[f].length} caracteres (máx. ${max})`);
    }
    fs.rmSync(path.join(out, '_tmp.html'), { force: true }); fs.writeFileSync(path.join(out, 'copies.csv'), '﻿' + rows.map(r => r.map(csv).join(';')).join('\n'));
    console.log(id, cfg.creatives.length, 'criativos', problems.length ? '· ' + problems.join(' | ') : '· ok');
  }
  await b.close();
})();

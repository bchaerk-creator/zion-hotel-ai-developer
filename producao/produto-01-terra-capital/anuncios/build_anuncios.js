// Gera os 6 anúncios 1080x1350 (versão neutra de texto onde preciso), as versões 9:16 (Stories/Reels) e confere medidas.
// Uso: node anuncios/build_anuncios.js   (precisa de src/originais/ e src/card_04_real.jpg)
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
const A = __dirname, R = path.resolve(A, '../../..'), F = (p) => 'file://' + path.join(R, 'docs/assets/fonts', p), IMG = (p) => 'file://' + path.join(A, 'src', p);
const CSS = `@font-face{font-family:Cormorant;src:url(${F('cormorant.woff2')});font-weight:300 700}@font-face{font-family:Cormorant;font-style:italic;src:url(${F('cormorant-italic.woff2')})}@font-face{font-family:Aventa;src:url(${F('aventa.woff2')})}
*{box-sizing:border-box;margin:0}body{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Cormorant,serif}
img.bg{position:absolute;inset:0;width:1080px;height:1350px}
.pn{position:absolute;left:0;right:0;top:166px;padding:20px 80px 0;background:linear-gradient(180deg,rgba(254,245,240,1) 0,rgba(254,245,240,1) 92%,rgba(254,245,240,0) 100%)}
.pn h1{font-weight:500;font-size:104px;line-height:1.02;color:#1B2117;letter-spacing:-.5px}.pn h1 i{color:#8d7439;font-weight:500}
.pn .sb{font:400 42px Aventa,sans-serif;color:#1B2117;margin-top:22px}.pn .rl{width:150px;height:4px;background:#C9B37E;margin:26px 0 0}
.tag{position:absolute;left:34px;bottom:22px;font:500 22px Aventa,sans-serif;color:#fff;text-shadow:0 1px 6px rgba(0,0,0,.75);letter-spacing:.04em}`;
const NEUTRO = {
  1: ['Tem um terreno em <i>destino turístico?</i><br>Aprenda a planejar o projeto.', 520, ''],
  2: ['Documentação, riscos e alternativas: <i>organize antes de decidir.</i>', 480, 'Material educativo. Não é oferta de crédito.'],
  3: ['Uma proposta clara <i>para potenciais parceiros.</i>', 500, 'Aportes e responsabilidades definidos por escrito.'],
  4: ['Calcule o capital <i>necessário para o seu projeto.</i>', 520, 'Ferramenta educativa, passo a passo.'],
};
const cards = [
  { n: 1, ori: 'originais/card_01.jpg', neutro: true }, { n: 2, ori: 'originais/card_02.jpg', neutro: true }, { n: 3, ori: 'originais/card_03.jpg', neutro: true },
  { n: 4, ori: 'card_04_real.jpg', neutro: true }, { n: 5, ori: 'originais/card_05.jpg' }, { n: 6, ori: 'originais/card_06.jpg' }];
const TMP = path.join(A, '.tmp'); fs.mkdirSync(TMP, { recursive: true });
const show = async (pg, html) => { const f = path.join(TMP, 'p.html'); fs.writeFileSync(f, '<!doctype html><meta charset="utf-8">' + html); await pg.goto('file://' + f, { waitUntil: 'load' }); };
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  const out = path.join(A, 'dist'); fs.mkdirSync(out + '/feed', { recursive: true }); fs.mkdirSync(out + '/stories', { recursive: true });
  const render = async (c, neutro, file) => {
    const pn = neutro ? `<div class="pn" style="height:${NEUTRO[c.n][1]}px"><h1>${NEUTRO[c.n][0]}</h1><div class="rl"></div>${NEUTRO[c.n][2] ? `<p class="sb">${NEUTRO[c.n][2]}</p>` : ''}</div>` : '';
    await show(p, `<style>${CSS}</style><img class="bg" src="${IMG(c.ori)}">${pn}<div class="tag">Imagem ilustrativa</div>`);
    await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: file, type: 'jpeg', quality: 93 });
  };
  for (const c of cards) {
    if (c.neutro) await render(c, true, `${out}/feed/anuncio_0${c.n}_neutro_1080x1350.jpg`);
    if (c.n === 4) { await render(c, false, `${out}/feed/anuncio_04_original-com-tela-real_1080x1350.jpg`); }
    if (!c.neutro) await render(c, false, `${out}/feed/anuncio_0${c.n}_1080x1350.jpg`);
  }
  // 9:16: o card inteiro, sem esticar nem cortar, em faixa musgo; topo e base livres para a interface do Meta
  const s = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const f of fs.readdirSync(out + '/feed').filter(x => x.endsWith('.jpg') && !x.includes('original-com'))) {
    const nome = f.replace('_1080x1350', '_1080x1920');
    await show(s, `<style>${CSS.split('body{')[0]}*{margin:0}body{width:1080px;height:1920px;background:#1B2117;position:relative;overflow:hidden}img{position:absolute;left:0;top:250px;width:1080px;height:1350px}.t{position:absolute;left:0;right:0;top:1632px;text-align:center;font:500 26px Aventa,sans-serif;color:#C9B37E;letter-spacing:.08em}</style><img src="file://${out}/feed/${f}"><div class="t">MATERIAL EDUCATIVO · SEM PROMESSA DE CRÉDITO, SÓCIO OU RETORNO</div>`);
    await s.screenshot({ path: `${out}/stories/${nome}`, type: 'jpeg', quality: 92 });
  }
  fs.rmSync(TMP, { recursive: true }); await b.close(); console.log(fs.readdirSync(out + '/feed').join('\n'), '\n', fs.readdirSync(out + '/stories').join('\n'));
})();

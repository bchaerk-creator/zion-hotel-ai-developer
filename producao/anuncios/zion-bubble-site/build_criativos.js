// Gera os criativos 1080x1350 dos anúncios Meta do site zionbubbleglamping.com
// Uso: node producao/anuncios/zion-bubble-site/build_criativos.js
const {chromium} = require('playwright');
const path = require('path');
const fs = require('fs');
const ROOT = path.resolve(__dirname, '../../..');
const url = p => 'file://' + path.join(ROOT, p);
const OUT = path.join(__dirname, 'criativos');

// Cada criativo: foto real da Zion (sem pessoas), selo, título, apoio e chamada.
const C = [
  {id:'CR01-urubici-estrelas', foto:'docs/assets/operacoes/op08.webp', pos:'50% 50%',
   selo:'URUBICI · SERRA CATARINENSE', titulo:'Durma sob as estrelas<br><em>a 1.600 m de altitude</em>',
   apoio:'Bubble no meio do bosque, jacuzzi externo e café da manhã incluído.', cta:'Ver as bubbles de Urubici'},
  {id:'CR02-floripa-piscina', foto:'docs/assets/store/deck.webp', pos:'50% 50%',
   selo:'FLORIANÓPOLIS · NORTE DA ILHA', titulo:'Sua bubble com<br><em>piscina privativa</em>',
   apoio:'Um refúgio tropical a poucos minutos de Jurerê e Santo Antônio de Lisboa.', cta:'Ver as bubbles de Floripa'},
  {id:'CR03-banheira-imersao', foto:'docs/assets/operacoes/op04.webp', pos:'50% 60%',
   selo:'FLORIANÓPOLIS', titulo:'Banheira de imersão<br><em>com vista para o céu</em>',
   apoio:'Na bubble Mintaka, também tem piscina privativa e jacuzzi externo.', cta:'Conhecer a Mintaka'},
  {id:'CR04-privacidade', foto:'docs/assets/operacoes/op09.webp', pos:'50% 45%',
   selo:'URUBICI · BOSQUE NATIVO', titulo:'Só vocês dois<br><em>e a floresta</em>',
   apoio:'No mínimo 100 m entre cada bubble e um caminho privativo até a sua.', cta:'Escolher a sua bubble'},
  {id:'CR05-presente', foto:'docs/assets/store/noite.webp', pos:'50% 50%',
   selo:'VOUCHER PRESENTE', titulo:'Dê de presente<br><em>uma noite sob as estrelas</em>',
   apoio:'Voucher para uma noite em uma acomodação bolha, em Urubici ou Floripa.', cta:'Presentear alguém'},
  {id:'CR06-cafe-incluso', foto:'docs/assets/store/hero.webp', pos:'50% 55%',
   selo:'URUBICI E FLORIANÓPOLIS', titulo:'Café da manhã<br><em>servido na sua bubble</em>',
   apoio:'Incluído em todas as tarifas, com produtos frescos da região.', cta:'Ver valores e datas'},
];

const html = c => `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Cormorant;src:url('${url('docs/assets/fonts/cormorant.woff2')}')}
@font-face{font-family:CormorantI;src:url('${url('docs/assets/fonts/cormorant-italic.woff2')}')}
@font-face{font-family:Aventa;src:url('${url('docs/assets/fonts/aventa.woff2')}')}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;position:relative;overflow:hidden;background:#040605;font-family:Aventa,sans-serif;color:#FEF5F0}
.foto{position:absolute;inset:0;background:url('${url(c.foto)}') ${c.pos}/cover}
.veu{position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,6,5,.78) 0%,rgba(4,6,5,.35) 12%,rgba(4,6,5,0) 24%,rgba(4,6,5,0) 45%,rgba(4,6,5,.82) 72%,#040605 100%)}
.marca{position:absolute;top:66px;left:64px;font-size:24px;letter-spacing:.32em;color:#FEF5F0}
.selo{position:absolute;top:68px;right:64px;font-size:22px;letter-spacing:.18em;color:#C9B37E;text-align:right}
.txt{position:absolute;left:64px;right:64px;bottom:72px}
h1{font-family:Cormorant,serif;font-weight:400;font-size:92px;line-height:1.02;color:#FEF5F0}
h1 em{font-family:CormorantI,serif;font-style:italic;color:#DED6BF}
p{margin-top:26px;font-size:32px;line-height:1.35;color:#DED6BF;max-width:900px}
.cta{display:inline-block;margin-top:40px;padding:24px 44px;background:#C9B37E;color:#040605;font-size:30px;letter-spacing:.04em;border-radius:2px}
.cta:after{content:"  →"}
</style></head><body><div class="foto"></div><div class="veu"></div>
<div class="marca">ZION BUBBLE</div><div class="selo">${c.selo}</div>
<div class="txt"><h1>${c.titulo}</h1><p>${c.apoio}</p><span class="cta">${c.cta}</span></div></body></html>`;

(async () => {
  fs.mkdirSync(OUT, {recursive: true});
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 1080, height: 1350}, deviceScaleFactor: 1});
  for (const c of C) {
    const f = path.join(OUT, c.id + '.html');
    fs.writeFileSync(f, html(c));
    await p.goto('file://' + f);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.screenshot({path: path.join(OUT, c.id + '.jpg'), type: 'jpeg', quality: 90});
    fs.unlinkSync(f);
    console.log('ok', c.id);
  }
  await b.close();
})();

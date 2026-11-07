// Gera a landing ECROI (10 dobras) de um produto a partir de landings/<ID>.json → out/landings/<ID>.html
// Uso: node scripts/landing.js A02
const fs = require('fs'), path = require('path');
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
function build(d) {
  const li = a => a.map(x => `<li>${x}</li>`).join('');
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(d.seoTitle)}</title><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Jost:wght@400;500;600&display=swap" rel="stylesheet"><meta name="description" content="${esc(d.seoDescription)}">
<style>
:root{--cx-color-background:#FEF5F0;--cx-color-headline:#040605;--cx-color-subheadline:#1B2117;--cx-color-content:#2a2c25;--cx-color-colored:#C9B37E;--cx-color-on-colored:#040605;--cx-color-surface:#ffffff;--cx-color-hairline:#DED6BF;--cx-font-headline:"Cormorant Garamond";--cx-font-content:"Jost";--musgo:#1B2117}
*{box-sizing:border-box}body{margin:0;background:#FEF5F0;color:#2a2c25;font-family:Jost,system-ui,sans-serif;line-height:1.6}
.w{max-width:960px;margin:0 auto;padding:56px 20px}
h1,h2,h3{font-family:"Cormorant Garamond",Georgia,serif;color:#040605;line-height:1.12;margin:0 0 14px}
h1{font-size:clamp(34px,6vw,56px)}h2{font-size:clamp(28px,4.5vw,40px)}h3{font-size:22px}
.k{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#8B714E;font-weight:700;margin-bottom:10px;display:block}
.dark{background:linear-gradient(160deg,#1B2117,#040605);color:#DED6BF}.dark h1,.dark h2,.dark h3,.dark p,.dark li,.dark span{color:#FEF5F0}
.lead{font-size:20px;max-width:720px}
.btn{display:inline-block;background:#C9B37E;color:#040605;text-decoration:none;font-weight:700;padding:16px 28px;border-radius:12px;margin-top:10px}
.grid{display:grid;gap:16px;grid-template-columns:1fr}@media(min-width:760px){.grid.c2{grid-template-columns:1fr 1fr}.grid.c3{grid-template-columns:1fr 1fr 1fr}}
.card{background:#fff;border:1px solid #DED6BF;border-radius:16px;padding:22px}
.card h3{margin-top:0}
ul.chk{list-style:none;padding:0}ul.chk li{padding:8px 0 8px 30px;position:relative}ul.chk li:before{content:"✓";position:absolute;left:0;color:#1B2117;font-weight:700}
ul.x li:before{content:"✕";color:#A3432F}
.steps{counter-reset:s;list-style:none;padding:0}.steps li{counter-increment:s;padding:12px 0 12px 52px;position:relative;border-bottom:1px solid #DED6BF}.steps li:before{content:counter(s);position:absolute;left:0;top:10px;width:36px;height:36px;border-radius:50%;background:#1B2117;color:#FEF5F0;display:flex;align-items:center;justify-content:center;font-weight:700}
.demo{background:#040605;border-radius:18px;padding:18px;color:#DED6BF}
.demo .row{display:flex;justify-content:space-between;border-bottom:1px solid #1f2419;padding:9px 4px;font-size:15px}.demo .row span{color:#DED6BF}.demo .row b{color:#C9B37E}.demo p{color:#DED6BF}
.demo .res{background:#1B2117;border:1px solid #C9B37E;border-radius:12px;padding:14px;margin-top:12px}
.price{font-family:"Cormorant Garamond",serif;font-size:64px;color:#040605;font-weight:600}
.faq details{background:#fff;border:1px solid #DED6BF;border-radius:12px;padding:14px 18px;margin:10px 0}.faq summary{font-weight:700;cursor:pointer}
.small{font-size:13px;opacity:.8}
img.cm-image{width:100%;border-radius:16px;display:block}
</style></head><body>

<section data-cx-section="hero" class="dark"><div class="w">
<span class="k" style="color:#C9B37E">Zion Collection Club · Hotel Business Academy</span>
<h1>${d.headline}</h1><p class="lead">${d.subheadline}</p>
<a class="btn" data-cx-cta href="#oferta">${esc(d.cta)}</a>
<p class="small">Mini mentoria interativa + ${esc(d.tool)} · R$ 27 · pagamento único</p>
<img class="cm-image" alt="${esc(d.tool)} em uso" data-cx-image-slot="hero" data-cx-image-hint="Tela da ferramenta ${esc(d.tool)} com resultado, 16:9" data-cx-image-kind="brand">
</div></section>

<section data-cx-section="problem"><div class="w">
<span class="k">Talvez o problema não seja o que você pensa</span>
<h2>${d.collapseTitle}</h2><p class="lead">${d.collapse}</p>
<h3 style="margin-top:34px">Você se reconhece em alguma destas situações?</h3>
<ul class="chk x">${li(d.symptoms.slice(0,3))}</ul>
</div></section>



<section data-cx-section="solution"><div class="w">
<span class="k">Como funciona</span>
<h2>${esc(d.demoTitle)}</h2>
<div class="grid c2"><div><ol class="steps">${li(d.demoSteps)}</ol></div>
<div class="demo"><div class="k" style="color:#C9B37E">${esc(d.tool)} · exemplo ilustrativo</div>
${d.demoInputs.map(r => `<div class="row"><span>${r[0]}</span><b>${r[1]}</b></div>`).join('')}
<div class="res">${d.demoResult}</div></div></div>
<p class="small">Números fictícios, apenas para demonstrar o funcionamento. Na mini mentoria você usa os seus.</p>
</div></section>



<section data-cx-section="offer" id="oferta"><div class="w">
<span class="k">O que você recebe</span><h2>Tudo em uma compra só</h2>
<div class="grid c2"><div><ul class="chk">${li(d.deliverables)}</ul></div>
<div class="card" style="text-align:center"><img class="cm-image" alt="${esc(d.title)}" data-cx-image-slot="offer" data-cx-image-hint="Mockup do produto, 1:1" data-cx-image-kind="brand">
<div class="price">R$ 27</div><p>Pagamento único · sem assinatura · acesso após a aprovação do pagamento</p>
<div data-cx-checkout></div></div></div>
</div></section>

<section data-cx-section="faq" class="faq"><div class="w">
<span class="k">Perguntas frequentes</span><h2>Antes de comprar</h2>
${d.faq.slice(0,3).concat(d.faq.filter(f=>/acesso/i.test(f[0])).slice(0,1)).filter((f,i,a)=>a.indexOf(f)===i).map(f => `<details><summary>${esc(f[0])}</summary><p>${f[1]}</p></details>`).join('')}
</div></section>

<section data-cx-section="cta" class="dark"><div class="w" style="text-align:center">
<h2>${d.finalHeadline}</h2><p class="lead" style="margin:0 auto">Aprenda o passo a passo. Utilize as ferramentas. Construa seu resultado.</p>
<a class="btn" data-cx-cta href="#oferta">${esc(d.cta)}</a>
<p class="small" style="margin-top:26px">${d.disclaimer}<br>Zion Collection Club · Hotel Business Academy · uma iniciativa Zion Hotel Group International.</p>
</div></section>
</body></html>`;
}
const id = process.argv[2];
const d = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'landings', id + '.json'), 'utf8'));
const out = path.join(__dirname, '..', 'out', 'landings'); fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, id + '.html'), build(d)); console.log('ok', path.join(out, id + '.html'));

// Vídeo de apresentação (9:16) de uma ferramenta, no estilo editorial Zion: cenas + narração + telas reais.
// Uso: node promo/make.js A02   (requer promo/<ID>.json e out/promo/<ID>/tela-*.png de promo/shots.js)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const id = process.argv[2];
const REPO = '/home/user/zion-hotel-ai-developer/docs';
const SCR = '/tmp/claude-0/-home-user-zion-hotel-ai-developer/312d9b1e-220b-5865-9c6e-31457236f0ae/scratchpad';
const OUT = path.join(__dirname, '..', 'out', 'promo', id);
const cfg = JSON.parse(fs.readFileSync(path.join(__dirname, id + '.json'), 'utf8'));
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const title = t => esc(t).replace(/\*(.+?)\*/g, '<em>$1</em>');
// assets locais (fontes, logo, fotos)
for (const [src, dst] of [[`${REPO}/assets/fonts/cormorant.woff2`, 'cormorant.woff2'], [`${REPO}/assets/fonts/cormorant-italic.woff2`, 'cormorant-italic.woff2'], [`${REPO}/assets/fonts/aventa.woff2`, 'aventa.woff2'], [`${REPO}/brand/zion-logo-claro.png`, 'logo.png']]) fs.copyFileSync(src, path.join(OUT, dst));
cfg.scenes.forEach(s => { if (s.photo) fs.copyFileSync(`${REPO}/assets/operacoes/${s.photo}.webp`, path.join(OUT, s.photo + '.webp')); });
// 1) narração
const rot = path.join(OUT, 'roteiro.json'); fs.writeFileSync(rot, JSON.stringify({ segments: cfg.scenes.map((s, i) => ({ id: 'c' + (i + 1), say: s.say })) }));
execFileSync(`${SCR}/tts/venv/bin/python`, [path.join(__dirname, '..', 'tutorial', 'tts.py'), rot, path.join(OUT, 'wav'), `${SCR}/voz/vits-piper-pt_BR-faber-medium/pt_BR-faber-medium.onnx`, `${SCR}/tts/venv/bin/piper`]);
const dur = JSON.parse(fs.readFileSync(path.join(OUT, 'wav', 'duracoes.json'), 'utf8'));
// 2) cenas
const scene = (s, i) => {
  const shots = (s.shots || []).map((n, k) => `<img class="shot${s.shots.length > 1 ? ' s' + k : ''}" data-a="${3 + k}" src="${n}.png">`).join('');
  const list = (s.list || []).map((t, k) => `<li data-a="${3 + k}"><b>${String(k + 1).padStart(2, '0')}</b><span>${esc(t)}</span></li>`).join('');
  return `<section class="sc${s.photo ? ' ph' : ''}${s.shots ? ' has-shots' : ''}" id="c${i + 1}">${s.photo ? `<div class="bg" style="background-image:url(${s.photo}.webp)"></div><div class="veil"></div>` : ''}
  <div class="top"><img src="logo.png" class="logo"><span>Zion Collection Club</span></div>
  ${shots ? `<div class="shots">${shots}</div>` : ''}
  <div class="txt"><div class="k" data-a="0">${esc(s.kicker)}</div><h1 data-a="1">${title(s.title)}</h1>${s.text ? `<p data-a="2">${esc(s.text)}</p>` : ''}${list ? `<ol>${list}</ol>` : ''}
  ${s.cta ? `<div class="btn" data-a="3">${esc(cfg.cta)}</div>` : ''}<div class="rule" data-a="4"></div></div>
  ${s.caption ? `<div class="cap">${esc(s.caption)}</div>` : ''}
  <div class="foot">${esc(s.fine || 'Hotel Business Academy · Aprenda o passo a passo')}</div></section>`;
};
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Cormorant;src:url(cormorant.woff2)}@font-face{font-family:Cormorant;font-style:italic;src:url(cormorant-italic.woff2)}@font-face{font-family:Aventa;src:url(aventa.woff2)}
*{box-sizing:border-box;margin:0}html,body{width:1080px;height:1920px;overflow:hidden;background:#040605}
.sc{position:absolute;inset:0;background:linear-gradient(170deg,#1B2117 0%,#11160f 55%,#040605 100%);opacity:0;transition:opacity .7s ease;color:#FEF5F0;font-family:Aventa,sans-serif}
.sc.on{opacity:1}.bg{position:absolute;inset:0;background-size:cover;background-position:center;transform:scale(1.12);transition:transform 9s linear}.sc.on .bg{transform:scale(1)}
.veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,6,5,.55) 0%,rgba(4,6,5,.25) 35%,rgba(4,6,5,.88) 70%,#040605 100%)}
.top{position:absolute;top:70px;left:90px;right:90px;display:flex;justify-content:space-between;align-items:center;z-index:2}.logo{height:62px}
.top span{font-size:24px;letter-spacing:.32em;text-transform:uppercase;color:#C9B37E;opacity:.85}
.txt{position:absolute;left:90px;right:90px;bottom:250px;z-index:2}.has-shots .txt{bottom:200px}
.k{font-size:28px;letter-spacing:.26em;text-transform:uppercase;color:#C9B37E;margin-bottom:26px}
h1{font-family:Cormorant,serif;font-weight:500;font-size:104px;line-height:1.02;color:#FEF5F0;margin-bottom:34px}h1 em{color:#C9B37E;font-style:italic}
p{font-size:40px;line-height:1.45;color:#DED6BF;max-width:880px}
ol{list-style:none;padding:0;margin-top:10px}li{display:flex;gap:28px;align-items:baseline;padding:22px 0;border-top:1px solid rgba(201,179,126,.25);font-size:38px;line-height:1.35;color:#FEF5F0}
li b{font-family:Cormorant,serif;font-weight:500;font-size:44px;color:#C9B37E;min-width:56px}
.rule{width:150px;height:3px;background:#C9B37E;margin-top:44px}
.btn{display:inline-block;margin-top:40px;background:#C9B37E;color:#040605;font-size:38px;font-weight:600;padding:30px 54px;border-radius:999px}
.shots{position:absolute;top:190px;left:0;right:0;height:760px;display:flex;justify-content:center;gap:40px;z-index:1}
.shot{height:100%;border-radius:34px;box-shadow:0 40px 90px rgba(0,0,0,.6);border:2px solid rgba(201,179,126,.35)}
.shots .s0{transform:rotate(-4deg) translateY(20px)}.shots .s1{transform:rotate(4deg) translateY(-10px)}
.has-shots h1{font-size:92px}.has-shots li{padding:16px 0;font-size:35px}
.cap{position:absolute;top:150px;left:90px;font-size:24px;letter-spacing:.12em;color:#DED6BF;opacity:.9;z-index:2}
.foot{position:absolute;bottom:90px;left:90px;right:90px;font-size:22px;letter-spacing:.06em;color:#DED6BF;opacity:.7;z-index:2;line-height:1.4}
[data-a]{opacity:0;transform:translateY(34px);transition:opacity .8s ease,transform .8s ease}.sc.on [data-a]{opacity:1;transform:none}
${[0, 1, 2, 3, 4, 5, 6, 7].map(n => `.sc.on [data-a="${n}"]{transition-delay:${0.25 + n * 0.32}s}`).join('')}
.shots [data-a]{transform:translateY(60px)}.sc.on .shots .s0{transform:rotate(-4deg) translateY(20px)}.sc.on .shots .s1{transform:rotate(4deg) translateY(-10px)}
</style></head><body>${cfg.scenes.map(scene).join('')}<script>function fit(){document.querySelectorAll('.sc').forEach(s=>{const sh=s.querySelector('.shots');if(!sh)return;const was=s.classList.contains('on');s.classList.add('on');const t=s.querySelector('.txt');t.querySelectorAll('[data-a]').forEach(e=>e.style.transition='none');const top=t.getBoundingClientRect().top;if(!was)s.classList.remove('on');t.querySelectorAll('[data-a]').forEach(e=>e.style.transition='');sh.style.height=Math.max(420,Math.min(760,top-190-50))+'px';});}document.fonts.ready.then(fit);window.show=i=>{document.querySelectorAll('.sc').forEach((s,k)=>s.classList.toggle('on',k===i));}</script></body></html>`;
fs.writeFileSync(path.join(OUT, 'cenas.html'), html);
// 3) gravação
(async () => {
  const tmp = path.join(OUT, 'tmpvid'); fs.rmSync(tmp, { recursive: true, force: true });
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1080, height: 1920 }, recordVideo: { dir: tmp, size: { width: 1080, height: 1920 } } });
  const p = await ctx.newPage(); const t0 = Date.now(); await p.goto('file://' + path.join(OUT, 'cenas.html')); await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400); const starts = [];
  for (let i = 0; i < cfg.scenes.length; i++) { await p.evaluate(i => show(i), i); starts.push(Date.now() - t0 + 600); await p.waitForTimeout(dur['c' + (i + 1)] * 1000 + 1700); }
  await p.waitForTimeout(800); const vp = await p.video().path(); await ctx.close(); await b.close();
  const args = ['-y', '-loglevel', 'error', '-i', vp]; cfg.scenes.forEach((_, i) => args.push('-i', path.join(OUT, 'wav', `c${i + 1}.wav`)));
  const f = cfg.scenes.map((_, i) => `[${i + 1}:a]adelay=${starts[i]}|${starts[i]},aresample=44100[a${i}]`).join(';') + ';' + cfg.scenes.map((_, i) => `[a${i}]`).join('') + `amix=inputs=${cfg.scenes.length}:normalize=0,volume=0.95,alimiter=limit=0.7:level=false[aout]`;
  const outF = path.join(OUT, `${id}-apresentacao-9x16.mp4`);
  execFileSync('ffmpeg', [...args, '-filter_complex', f, '-map', '0:v', '-map', '[aout]', '-c:v', 'libx264', '-crf', '21', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', outF]);
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log('ok', outF, execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', outF]).toString().trim() + 's');
})();

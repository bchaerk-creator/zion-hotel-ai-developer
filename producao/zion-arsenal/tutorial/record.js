// Grava tutorial narrado: roteiro tutorial/<ID>.json + WAVs (tts.py) → out/tutoriais/<ID>-tutorial.mp4
// Uso: node tutorial/record.js A02 <pasta_wavs>
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), http = require('http'), { execFileSync } = require('child_process');
const [id, wavDir] = process.argv.slice(2);
const ROOT = path.join(__dirname, '..', 'app'), OUT = path.join(__dirname, '..', 'out', 'tutoriais');
const rot = JSON.parse(fs.readFileSync(path.join(__dirname, id + '.json'), 'utf8'));
const dur = JSON.parse(fs.readFileSync(path.join(wavDir, 'duracoes.json'), 'utf8'));
const prof = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'tests', 'profiles', id + '.json'), 'utf8')).profiles[0];
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
const wait = ms => new Promise(r => setTimeout(r, ms));
const CURSOR = `(()=>{const add=()=>{if(document.getElementById('zc'))return;const c=document.createElement('div');c.id='zc';
c.innerHTML='<svg width="26" height="26" viewBox="0 0 24 24"><path d="M3 2l7.5 19 2.6-7.9L21 10.5z" fill="#fff" stroke="#040605" stroke-width="1.6" stroke-linejoin="round"/></svg>';
c.style.cssText='position:fixed;left:0;top:0;z-index:2147483647;pointer-events:none;transform:translate(-3px,-2px);transition:none';document.documentElement.appendChild(c);
const r=document.createElement('div');r.id='zr';r.style.cssText='position:fixed;z-index:2147483646;pointer-events:none;width:34px;height:34px;margin:-17px 0 0 -17px;border-radius:50%;border:3px solid #C9B37E;opacity:0;transition:opacity .45s,transform .45s';document.documentElement.appendChild(r);
addEventListener('mousemove',e=>{c.style.left=e.clientX+'px';c.style.top=e.clientY+'px';},true);
addEventListener('mousedown',e=>{r.style.left=e.clientX+'px';r.style.top=e.clientY+'px';r.style.transition='none';r.style.opacity=1;r.style.transform='scale(.4)';requestAnimationFrame(()=>{r.style.transition='opacity .5s,transform .5s';r.style.opacity=0;r.style.transform='scale(1.4)';});},true);};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',add);else add();})();`;
(async () => {
  const srv = await new Promise(r => { const s = http.createServer((q, res) => { let p = q.url.split('?')[0]; if (p.endsWith('/')) p += 'index.html'; const f = path.join(ROOT, p);
    if (!f.startsWith(ROOT) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res); }).listen(0, () => r(s)); });
  fs.mkdirSync(OUT, { recursive: true }); const tmp = path.join(OUT, 'tmp-' + id); fs.rmSync(tmp, { recursive: true, force: true });
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 720 }, recordVideo: { dir: tmp, size: { width: 1280, height: 720 } } });
  await ctx.addInitScript(CURSOR);
  const page = await ctx.newPage(); const t0 = Date.now();
  await page.goto(`http://127.0.0.1:${srv.address().port}/index.html?p=${id}`); await page.waitForSelector('#za-next');
  let mx = 640, my = 360; await page.mouse.move(mx, my);
  const moveTo = async sel => { const el = page.locator(sel).first(); await el.scrollIntoViewIfNeeded().catch(() => {}); const bb = await el.boundingBox(); if (!bb) return;
    const x = bb.x + Math.min(bb.width / 2, 60), y = bb.y + bb.height / 2; await page.mouse.move(x, y, { steps: 28 }); mx = x; my = y; await wait(250); };
  const starts = {};
  await wait(800);
  for (const seg of rot.segments) {
    starts[seg.id] = Date.now() - t0; const end = Date.now() + dur[seg.id] * 1000;
    for (const [op, a, v] of seg.do) {
      if (op === 'move') await moveTo(a);
      else if (op === 'click') { await moveTo(a); await page.mouse.down(); await page.mouse.up(); await wait(500); }
      else if (op === 'type') { await moveTo(a); await page.locator(a).click(); await page.locator(a).pressSequentially(v, { delay: 85 }); await wait(250); }
      else if (op === 'select') { await moveTo(a); await page.locator(a).selectOption(v); await wait(300); }
      else if (op === 'check') { await moveTo(a); await page.locator(a).first().check(); await wait(350); }
      else if (op === 'scroll') { await page.mouse.wheel(0, a); await wait(400); }
      else if (op === 'wait') await wait(a);
      else if (op === 'go') { await page.evaluate(i => ZA.go(i), a); await wait(600); }
      else if (op === 'prefill') { await page.evaluate(([vals, idx]) => { const st = ZA.state(); const sc = ZA.screens[idx];
          const blank = new Set(sc.kind === 'form' ? sc.fields.map(f => f.id) : []);
          ZA.allFields().forEach(f => { if (blank.has(f.id) || st.u[f.id] || vals[f.id] === undefined) return; const cur = st.v[f.id];
            const empty = cur == null || cur === '' || (Array.isArray(cur) && !cur.some(r => r && (r.value != null && r.value !== '' || typeof r === 'string')));
            if (empty) st.v[f.id] = vals[f.id]; });
          ZA.screens.forEach((s, i) => { if (s.kind === 'apply' && i < idx) (s.actions || []).slice(0, 2).forEach(x => st.checks[x.id] = true); });
          st.max = 39; ZA.go(idx); }, [prof.values, a]); await wait(700); }
    }
    const left = end - Date.now(); await wait(Math.max(0, left) + 450);
    const pos = await page.evaluate(() => ZA.state().pos + 1); console.log(seg.id, 'início', (starts[seg.id]/1000).toFixed(1)+'s', 'fala', dur[seg.id].toFixed(1)+'s', 'tela no fim', pos, left < 0 ? '(ações mais longas que a fala: '+(-left/1000).toFixed(1)+'s)' : '');
  }
  await wait(1200); const vpath = await page.video().path(); await ctx.close(); await b.close(); srv.close();
  // monta o áudio no tempo de cada trecho
  const ids = rot.segments.map(s => s.id); const args = ['-y', '-loglevel', 'error', '-i', vpath];
  ids.forEach(i => args.push('-i', path.join(wavDir, i + '.wav')));
  const f = ids.map((i, k) => `[${k + 1}:a]adelay=${starts[i]}|${starts[i]},aresample=44100[a${k}]`).join(';') + ';' + ids.map((_, k) => `[a${k}]`).join('') + `amix=inputs=${ids.length}:normalize=0,volume=0.95,alimiter=limit=0.7:level=false[aout]`;
  const outFile = path.join(OUT, `${id}-tutorial.mp4`);
  execFileSync('ffmpeg', [...args, '-filter_complex', f, '-map', '0:v', '-map', '[aout]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '22', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', outFile]);
  fs.rmSync(tmp, { recursive: true, force: true });
  const d = execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', outFile]).toString().trim();
  console.log('ok', outFile, Number(d).toFixed(1) + 's');
})();

// Grava vídeo-demonstração real da ferramenta (9:16 e 4:5) a partir do perfil 1 de testes.
// Uso: node tests/demo.js A02 [A01 ...]  → out/demos/<ID>-9x16.mp4, <ID>-4x5.mp4, <ID>-frame-*.png
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), http = require('http'), { execFileSync } = require('child_process');
const ROOT = path.join(__dirname, '..', 'app'), OUT = path.join(__dirname, '..', 'out', 'demos');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
const serve = () => new Promise(r => { const s = http.createServer((q, res) => { let p = q.url.split('?')[0]; if (p.endsWith('/')) p += 'index.html'; const f = path.join(ROOT, p);
  if (!f.startsWith(ROOT) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res); }).listen(0, () => r(s)); });
const wait = ms => new Promise(r => setTimeout(r, ms));
async function demo(browser, base, id) {
  const prof = JSON.parse(fs.readFileSync(path.join(__dirname, 'profiles', id + '.json'), 'utf8')).profiles[0];
  // 1) estado completo do perfil 1 (sem gravar)
  const c0 = await browser.newContext(); const p0 = await c0.newPage(); await p0.goto(`${base}/index.html?p=${id}`); await p0.waitForSelector('#za-next');
  const info = await p0.evaluate((vals) => {
    const st = ZA.state(); ZA.allFields().forEach(f => { if (vals[f.id] !== undefined) st.v[f.id] = vals[f.id]; });
    ZA.screens.forEach(s => (s.actions || []).slice(0, 2).forEach(a => st.checks[a.id] = true));
    // tela-vitrine: exercício com mais campos numéricos
    let best = -1, bi = 0; ZA.screens.forEach((s, i) => { if (s.kind !== 'form') return; const n = (s.fields || []).filter(f => ['number', 'money', 'percent'].includes(f.type)).length; if (n > best) { best = n; bi = i; } });
    return { st: JSON.parse(JSON.stringify(st)), showIdx: bi, fields: ZA.screens[bi].fields.map(f => ({ id: f.id, type: f.type })), key: 'za:v1:' + ZA.cfg.code, title: ZA.cfg.title };
  }, prof.values);
  await c0.close();
  const st = info.st; info.fields.forEach(f => { if (['number', 'money', 'percent', 'text'].includes(f.type)) delete st.v[f.id]; });
  st.pos = info.showIdx; st.max = 39; st.updated = null;
  fs.mkdirSync(OUT, { recursive: true }); const tmp = path.join(OUT, 'tmp-' + id); fs.rmSync(tmp, { recursive: true, force: true });
  const ctx = await browser.newContext({ viewport: { width: 1080, height: 1920 }, recordVideo: { dir: tmp, size: { width: 1080, height: 1920 } } });
  await ctx.addInitScript(([k, v]) => { try { if (!sessionStorage.getItem('demo')) { localStorage.setItem(k, v); sessionStorage.setItem('demo', '1'); } } catch (e) { } }, [info.key, JSON.stringify(st)]);
  await ctx.addInitScript(() => { document.addEventListener('DOMContentLoaded', () => { const st = document.createElement('style'); st.textContent = 'html{zoom:2.5}'; document.head.appendChild(st); }); });
  const page = await ctx.newPage(); await page.goto(`${base}/index.html?p=${id}`); await page.waitForSelector('#za-next'); await wait(1200);
  for (const f of info.fields) { if (!['number', 'money', 'percent', 'text'].includes(f.type) || prof.values[f.id] === undefined) continue;
    const el = page.locator('#f_' + f.id); await el.scrollIntoViewIfNeeded(); await el.click(); await el.pressSequentially(String(prof.values[f.id]), { delay: 90 }); await wait(250); }
  await wait(600); await page.click('#za-next'); await wait(3200);
  await page.screenshot({ path: path.join(OUT, `${id}-frame-feedback.png`) });
  await page.evaluate(() => ZA.go(ZA.screens.length - 2)); await wait(1500);
  for (let y = 0; y < 5; y++) { await page.mouse.wheel(0, 1050); await wait(700); }
  await page.evaluate(() => ZA.go(ZA.screens.length - 1)); await wait(1800);
  await page.screenshot({ path: path.join(OUT, `${id}-frame-relatorio.png`) });
  for (let y = 0; y < 8; y++) { await page.mouse.wheel(0, 1125); await wait(650); }
  await wait(800); const vpath = await page.video().path(); await ctx.close();
  const mp4 = path.join(OUT, `${id}-9x16.mp4`);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', vpath, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', mp4]);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', mp4, '-vf', 'crop=1080:1350:0:120', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', path.join(OUT, `${id}-4x5.mp4`)]);
  fs.rmSync(tmp, { recursive: true, force: true });
  const dur = execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp4]).toString().trim();
  console.log(`${id}: ${mp4} (${Number(dur).toFixed(1)}s) · tela-vitrine ${info.showIdx + 1}`);
}
(async () => { const s = await serve(); const base = `http://127.0.0.1:${s.address().port}`; const b = await chromium.launch();
  for (const id of process.argv.slice(2)) { try { await demo(b, base, id); } catch (e) { console.log(id, 'ERRO', e.message); } }
  await b.close(); s.close(); })();

// Captura telas reais da ferramenta (perfil 1 de teste) para usar nos vídeos de apresentação.
// Uso: node promo/shots.js A02  → out/promo/<ID>/tela-*.png
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), http = require('http');
const ROOT = path.join(__dirname, '..', 'app'); const id = process.argv[2];
const OUT = path.join(__dirname, '..', 'out', 'promo', id); fs.mkdirSync(OUT, { recursive: true });
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
(async () => {
  const srv = await new Promise(r => { const s = http.createServer((q, res) => { let p = q.url.split('?')[0]; if (p.endsWith('/')) p += 'index.html'; const f = path.join(ROOT, p);
    if (!fs.existsSync(f)) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'content-type': MIME[path.extname(f)] }); fs.createReadStream(f).pipe(res); }).listen(0, () => r(s)); });
  const prof = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'tests', 'profiles', id + '.json'), 'utf8')).profiles[0];
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 430, height: 820 }, deviceScaleFactor: 2.5 });
  const p = await ctx.newPage(); await p.goto(`http://127.0.0.1:${srv.address().port}/index.html?p=${id}`); await p.waitForSelector('#za-next');
  const idx = await p.evaluate(vals => { const st = ZA.state(); ZA.allFields().forEach(f => { if (vals[f.id] !== undefined) st.v[f.id] = vals[f.id]; });
    ZA.screens.forEach(s => (s.actions || []).slice(0, 2).forEach(a => st.checks[a.id] = true)); st.max = 39;
    let best = -1, bi = 15; ZA.screens.forEach((s, i) => { if (s.kind !== 'form' || s.pillar < 2) return; const n = (s.fields || []).filter(f => ['number','money','percent'].includes(f.type)).length; if (n > best) { best = n; bi = i; } });
    return bi; }, prof.values);
  const shots = [['form', idx], ['feedback', idx + 1], ['consolidacao', 38], ['relatorio', 39]];
  for (const [n, i] of shots) { await p.evaluate(i => ZA.go(i), i); await p.waitForTimeout(400); await p.screenshot({ path: path.join(OUT, `tela-${n}.png`) }); }
  // recorte do OP3D da consolidação
  await p.evaluate(() => ZA.go(38)); await p.waitForTimeout(300); const op = p.locator('.za-op3d').first();
  if (await op.count()) { await op.scrollIntoViewIfNeeded(); await op.screenshot({ path: path.join(OUT, 'tela-op3d.png') }); }
  await b.close(); srv.close(); console.log('ok', fs.readdirSync(OUT).join(' '));
})();

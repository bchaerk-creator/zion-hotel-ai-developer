// Harness de testes do Zion Arsenal. Uso: node tests/run.js A02 [A01 ...]  (ou "all")
// Para cada produto: valida a config, executa 3 perfis pela interface (desktop + mobile),
// testa validação, persistência (reload), gera PDF e screenshots em tests/out/<ID>/.
const { chromium, devices } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..', 'app');
const OUT = path.join(__dirname, 'out');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml' };
function serve() {
  return new Promise(r => { const s = http.createServer((q, res) => {
    let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
    const f = path.join(ROOT, p); if (!f.startsWith(ROOT) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
  }).listen(0, () => r(s)); });
}
async function fillScreen(page, fields, prof) {
  for (const f of fields) {
    const sel = `[data-f="${f.id}"]`;
    if ((prof.unknown || []).includes(f.id) && f.allowUnknown) { const u = page.locator(`${sel} [data-unk]`); if (!(await u.isChecked())) await u.check(); continue; }
    let v = prof.values[f.id];
    if (v === undefined) continue;
    switch (f.type) {
      case 'number': case 'money': case 'percent': case 'text': case 'textarea':
        await page.locator(`#f_${f.id}`).fill(String(v)); break;
      case 'select': await page.locator(`#f_${f.id}`).selectOption(String(v)); break;
      case 'radio': case 'scale': await page.locator(`${sel} input[value="${v}"]`).check(); break;
      case 'checks': for (const x of v) await page.locator(`${sel} input[value="${x}"]`).check(); break;
      case 'list': {
        // v = array de {name,value}; substitui as linhas existentes
        const n = await page.locator(`${sel} .za-list-row`).count();
        for (let i = 0; i < Math.max(n, v.length); i++) {
          if (i >= n) await page.locator(`${sel} [data-add]`).click();
          const row = page.locator(`${sel} .za-list-row`).nth(i);
          const it = v[i] || { name: '', value: '' };
          await row.locator('[data-lk=name]').fill(String(it.name || ''));
          await row.locator('[data-lk=value]').fill(it.value == null ? '' : String(it.value));
        }
        break; }
    }
  }
}
async function runProduct(browser, id) {
  const cfgFile = path.join(__dirname, 'profiles', id + '.json');
  if (!fs.existsSync(cfgFile)) throw new Error('sem perfis de teste: ' + cfgFile);
  const spec = JSON.parse(fs.readFileSync(cfgFile, 'utf8'));
  const out = path.join(OUT, id); fs.mkdirSync(out, { recursive: true });
  const log = []; const fail = m => { log.push('FAIL ' + m); };
  const pass = m => log.push('ok   ' + m);
  for (const [pi, prof] of spec.profiles.entries()) {
    const ctx = await browser.newContext(pi === 1 ? devices['iPhone 13'] : { viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage(); const errs = [];
    page.on('pageerror', e => errs.push(String(e))); page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await page.goto(`${BASE}/index.html?p=${id}`); await page.waitForSelector('#za-next');
    if (pi === 0) {
      const v = await page.evaluate(() => ZA.validateConfig(ZA.cfg));
      v.length ? fail('estrutura: ' + v.join('; ')) : pass('estrutura: 40 telas, 7 pilares × 5 momentos, 7 exercícios');
    }
    const screens = await page.evaluate(() => ZA.screens.map(s => ({ kind: s.kind, idx: s.idx, fields: (s.fields || []).map(f => ({ id: f.id, type: f.type, allowUnknown: !!f.allowUnknown, required: !!f.required })), actions: (s.actions || []).map(a => a.id) })));
    for (let i = 0; i < screens.length - 1; i++) {
      const sc = screens[i];
      if (sc.fields.length) {
        // teste de validação: avançar com obrigatório vazio deve bloquear (somente perfil extremo, 1ª tela com campo numérico)
        if (pi === 2 && sc.fields.some(f => ['number', 'money', 'percent'].includes(f.type) && f.required && !(prof.unknown || []).includes(f.id))) {
          const f = sc.fields.find(f => ['number', 'money', 'percent'].includes(f.type) && f.required && !(prof.unknown || []).includes(f.id));
          await page.locator(`#f_${f.id}`).fill('-5'); await page.click('#za-next');
          const pos = await page.evaluate(() => ZA.state().pos);
          pos === i ? pass(`validação bloqueia negativo em ${f.id}`) : fail(`aceitou valor negativo em ${f.id}`);
        }
        await fillScreen(page, sc.fields, prof);
      }
      if (sc.kind === 'apply') { for (const a of sc.actions.slice(0, prof.actionsPerPillar ?? 2)) await page.locator(`[data-act="${a}"]`).check(); }
      if (sc.kind === 'feedback' || sc.kind === 'consolidation') {
        const t = await page.locator('#za-root').innerText();
        if (/NaN|undefined|Infinity|\[object/.test(t)) fail(`${sc.idx}: texto inválido na tela (${t.match(/.{0,40}(NaN|undefined|Infinity|\[object).{0,20}/)[0]})`);
      }
      await page.click('#za-next');
      const pos = await page.evaluate(() => ZA.state().pos);
      if (pos !== i + 1) { const e = await page.locator('.za-field.invalid .za-err').allInnerTexts(); fail(`perfil ${prof.name}: travou na tela ${sc.idx} (${e.join(' | ')})`); break; }
      if (i === 15) { await page.waitForTimeout(400); await page.reload(); await page.waitForSelector('#za-next');
        const p2 = await page.evaluate(() => ZA.state().pos); p2 === 16 ? (pi === 0 && pass('persistência: progresso recuperado após recarregar')) : fail('persistência falhou após reload (pos=' + p2 + ')'); }
    }
    const atReport = await page.evaluate(() => ZA.screens[ZA.state().pos].kind === 'report');
    if (!atReport) { fail(`perfil ${prof.name}: não chegou ao relatório`); }
    else {
      const t = await page.locator('#za-root').innerText();
      /NaN|undefined|Infinity|\[object/.test(t) ? fail(`perfil ${prof.name}: relatório contém valor inválido`) : pass(`perfil ${prof.name}: relatório gerado sem valores inválidos`);
      if (prof.expect) {
        const c = await page.evaluate(() => ZA.calc().c);
        for (const [k, exp] of Object.entries(prof.expect)) {
          const got = k.split('.').reduce((o, x) => o == null ? o : o[x], c);
          const ok = (exp === null) ? got === null : (typeof exp === 'number' ? (typeof got === 'number' && Math.abs(got - exp) <= Math.max(0.01, Math.abs(exp) * 0.001)) : got === exp);
          ok ? pass(`perfil ${prof.name}: ${k} = ${JSON.stringify(got)}`) : fail(`perfil ${prof.name}: ${k} esperado ${exp}, obtido ${got}`);
        }
      }
      for (const txt of (prof.reportContains || [])) (t.toLowerCase().includes(txt.toLowerCase()) ? pass : fail)(`perfil ${prof.name}: relatório contém “${txt}”`);
      await page.screenshot({ path: path.join(out, `relatorio-perfil${pi + 1}${pi === 1 ? '-mobile' : ''}.png`), fullPage: false });
      if (pi !== 1) { await page.emulateMedia({ media: 'print' }); await page.pdf({ path: path.join(out, `relatorio-perfil${pi + 1}.pdf`), format: 'A4', printBackground: true }); pass(`perfil ${prof.name}: PDF exportado`); }
    }
    errs.length ? fail(`perfil ${prof.name}: erros JS: ${errs.slice(0, 3).join(' | ')}`) : pass(`perfil ${prof.name}: sem erros de JavaScript`);
    await ctx.close();
  }
  fs.writeFileSync(path.join(out, 'resultado.txt'), log.join('\n') + '\n');
  return log;
}
let BASE;
(async () => {
  let ids = process.argv.slice(2); if (!ids.length || ids[0] === 'all') ids = fs.readdirSync(path.join(__dirname, 'profiles')).map(f => f.replace('.json', '')).sort();
  const srv = await serve(); BASE = `http://127.0.0.1:${srv.address().port}`;
  const browser = await chromium.launch(); let bad = 0; const summary = {};
  for (const id of ids) {
    try { const log = await runProduct(browser, id); const f = log.filter(l => l.startsWith('FAIL')).length; bad += f; summary[id] = { checks: log.length, falhas: f };
      console.log(`\n== ${id} == ${log.length - f}/${log.length} ok`); log.forEach(l => console.log('  ' + l)); }
    catch (e) { bad++; summary[id] = { erro: String(e) }; console.log(`\n== ${id} == ERRO ${e.message}`); }
  }
  fs.mkdirSync(OUT, { recursive: true }); fs.writeFileSync(path.join(OUT, 'summary.json'), JSON.stringify(summary, null, 2));
  await browser.close(); srv.close(); process.exit(bad ? 1 : 0);
})();

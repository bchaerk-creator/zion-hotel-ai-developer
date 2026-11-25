// Grava a demonstração real da plataforma (perfil de EXEMPLO, dados fictícios) e as telas do celular. Uso: node landing/gravar_demo.js <jspdf.umd.min.js>
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs'), cp = require('child_process');
const A = path.resolve(__dirname, '..'), IMG = path.join(__dirname, 'img'), URL = 'file://' + path.join(A, 'dist/index.html'), JSPDF = fs.readFileSync(process.argv[2], 'utf8');
const tmp = fs.mkdtempSync('/tmp/claude-0/demo-'); fs.mkdirSync(IMG, { recursive: true });
const PERFIL = () => { const P = RX_APP.state().P; P.identificacao = { nome: 'Pousada Exemplo (dados fictícios)', tipo: 'Pousada', municipio: 'Cidade Exemplo', unidades: '4' }; };
(async () => {
  const b = await chromium.launch();
  // 1) telas estáticas (celular, @2x)
  const c = await b.newContext({ viewport: { width: 390, height: 780 }, deviceScaleFactor: 2 }); await c.route('**/jspdf.umd.min.js', r => r.fulfill({ contentType: 'application/javascript', body: JSPDF })); const p = await c.newPage(); await p.goto(URL);
  await p.fill('#nomePf', 'Exemplo (dados fictícios)'); await p.click('#criaPf'); await p.evaluate(PERFIL);
  await p.evaluate(() => { const P = RX_APP.state().P; const o = ['2', '1', '0', '1', '2', 'unknown', '1', '0', '2', '1']; for (let m = 1; m <= 7; m++) for (let i = 1; i <= 10; i++) P.respostas['m' + m + 'q' + i] = o[(i + m) % 10]; P.respostas.m3q9 = '1';
    P.calculadoras.C4 = { disponiveis: '300', vendidas: '150', receita: '45000', fixos: [{ nome: 'Aluguel', valor: '6000' }, { nome: 'Equipe e sistemas', valor: '4000' }], limpeza: '80', insumos: '20', comissoes: '100', outrosVar: '0', noitesPorEstadia: '2', quedaOcupacaoPct: '20', quedaPrecoPct: '10', altaCustosPct: '10' };
    P.calculadoras.C3 = { receita: '24000', vendidas: '100', disponiveis: '200' }; });
  const shot = async (v, nome, y, fn) => { await p.evaluate(v => RX_APP.ir(v), v); await p.waitForTimeout(250); if (fn) await p.evaluate(fn); await p.evaluate(y => window.scrollTo(0, y), y || 0); await p.waitForTimeout(150); await p.screenshot({ path: path.join(IMG, nome + '.jpg'), type: 'jpeg', quality: 88 }); };
  await shot('aula3', 'tela-formulario', 560); await shot('aula4', 'tela-calculadora', 0, () => document.querySelector('#calcRes').scrollIntoView()); await shot('diag', 'tela-diagnostico', 0); await shot('plano', 'tela-plano', 520);
  await p.evaluate(() => RX_APP.ir('dossie')); const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#pdf')]); const pdf = path.join(tmp, 'dossie.pdf'); await dl.saveAs(pdf); await c.close();
  cp.execSync(`pdftoppm -r 70 -jpeg -f 1 -l 4 ${pdf} ${tmp}/dos`); fs.readdirSync(tmp).filter(f => f.startsWith('dos')).forEach((f, i) => fs.copyFileSync(path.join(tmp, f), path.join(IMG, `dossie-${i + 1}.jpg`)));
  // 2) vídeo: uso real, do início ao PDF
  const v = await b.newContext({ viewport: { width: 390, height: 780 }, recordVideo: { dir: tmp, size: { width: 390, height: 780 } }, acceptDownloads: true }); await v.route('**/jspdf.umd.min.js', r => r.fulfill({ contentType: 'application/javascript', body: JSPDF })); const q = await v.newPage(); await q.goto(URL);
  const leg = async t => q.evaluate(t => { let d = document.getElementById('__leg'); if (!d) { d = document.createElement('div'); d.id = '__leg'; d.style.cssText = 'position:fixed;left:8px;right:8px;bottom:10px;z-index:99;background:rgba(4,6,5,.88);color:#FEF5F0;font:14px/1.35 system-ui;padding:9px 12px;border-radius:8px;text-align:center;border:1px solid #C9B37E'; document.body.appendChild(d); } d.textContent = t; }, t);
  const w = ms => q.waitForTimeout(ms);
  await w(900); await q.fill('#nomePf', 'Exemplo'); await q.click('#criaPf'); await w(1200); await leg('Demonstração real da plataforma · dados fictícios'); await q.evaluate(PERFIL); await w(1200);
  await q.evaluate(() => RX_APP.ir('aula3')); await w(900); await leg('1. Responda ao formulário do módulo'); await q.evaluate(() => window.scrollTo(0, 640)); await w(700);
  for (const [n, val] of [['m3q1', '2'], ['m3q2', '1'], ['m3q3', '0']]) { await q.locator(`label:has(input[name=${n}][value="${val}"])`).scrollIntoViewIfNeeded(); await q.locator(`label:has(input[name=${n}][value="${val}"])`).click(); await w(800); }
  await q.evaluate(() => RX_APP.ir('aula4')); await w(700); await leg('2. Use a calculadora com os seus números'); await q.evaluate(() => document.querySelector('#calcBox').scrollIntoView()); await w(500);
  for (const [k, val] of [['disponiveis', '300'], ['vendidas', '150'], ['receita', '45000']]) { await q.fill(`[data-p="${k}"]`, val); await w(450); }
  for (const [k, val] of [['limpeza', '80'], ['insumos', '20'], ['comissoes', '100'], ['outrosVar', '0'], ['noitesPorEstadia', '2']]) { await q.fill(`[data-p="${k}"]`, val); await w(250); }
  await q.fill('[data-p="fixos.0.valor"]', '10000'); await w(500); await q.evaluate(() => document.querySelector('#calcRes').scrollIntoView()); await w(2200);
  await leg('3. Veja o diagnóstico por pilar, com a cobertura'); await q.evaluate(() => { const P = RX_APP.state().P; const o = ['2', '1', '0', '1', '2', 'unknown', '1', '0', '2', '1']; for (let m = 1; m <= 7; m++) for (let i = 1; i <= 10; i++) P.respostas['m' + m + 'q' + i] = o[(i + m) % 10]; RX_APP.ir('diag'); }); await w(2600);
  await leg('4. Receba o plano de ação para 7, 30, 60 e 90 dias'); await q.evaluate(() => { RX_APP.ir('plano'); window.scrollTo(0, 420); }); await w(2600);
  await leg('5. Gere o dossiê em PDF'); await q.evaluate(() => RX_APP.ir('dossie')); await w(900); const [d2] = await Promise.all([q.waitForEvent('download'), q.click('#pdf')]); await w(1600);
  await v.close(); const webm = fs.readdirSync(tmp).filter(f => f.endsWith('.webm'))[0];
  cp.execSync(`ffmpeg -y -loglevel error -i ${path.join(tmp, webm)} -vf "scale=720:-2" -c:v libx264 -pix_fmt yuv420p -crf 26 -movflags +faststart -an ${path.join(IMG, 'demo.mp4')}`); await b.close(); console.log('demo ok', fs.statSync(path.join(IMG, 'demo.mp4')).size);
})();

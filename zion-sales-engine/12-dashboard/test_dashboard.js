// Teste de ponta a ponta do dashboard.html com Playwright (390x844 e 1366x800).
// Uso: node test_dashboard.js [pasta_de_capturas]   (usa dados_exemplo.json FICTICIO via servidor local)
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const DIR = __dirname, OUT = process.argv[2] || path.join(require('os').tmpdir(), 'dash_caps');
fs.mkdirSync(OUT, { recursive: true });
let falhas = 0;
const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALHA') + ' ' + m); if (!c) falhas++; };

const srv = http.createServer((req, res) => {
  let u = decodeURIComponent(req.url.split('?')[0]); if (u === '/') u = '/dashboard.html';
  // /docs/... emula o caminho relativo ../../docs/ do repositório (logo oficial)
  const REPO = path.resolve(DIR, '..', '..');
  const f = u.startsWith('/docs/') ? path.join(REPO, u) : path.join(DIR, u);
  if (!(f.startsWith(DIR) || f.startsWith(path.join(REPO, 'docs', 'brand'))) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('nao'); }
  const t = f.endsWith('.html') ? 'text/html; charset=utf-8' : f.endsWith('.json') ? 'application/json' : 'application/octet-stream';
  res.writeHead(200, { 'Content-Type': t }); res.end(fs.readFileSync(f));
});

(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const base = 'http://127.0.0.1:' + srv.address().port + '/dashboard.html';
  const D = JSON.parse(fs.readFileSync(path.join(DIR, 'dados_exemplo.json'), 'utf8'));
  const browser = await chromium.launch();
  for (const [nome, vw] of [['mobile-390x844', { width: 390, height: 844 }], ['desktop-1366x800', { width: 1366, height: 800 }]]) {
    const ctx = await browser.newContext({ viewport: vw, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const erros = [];
    // 404 de dados.json é esperado no repositório (só existe dados_exemplo.json): o painel cai para o exemplo
    page.on('console', m => { if (m.type() === 'error' && !/dados\.json$/.test(m.location().url || '')) erros.push(m.text() + ' @' + m.location().url); });
    page.on('pageerror', e => erros.push('pageerror: ' + e.message));
    await page.goto(base); await page.waitForSelector('body[data-pronto="1"]');
    console.log('== ' + nome + ' ==');
    // rótulo e dados do exemplo
    const faixa = await page.textContent('#faixa');
    ok(/DADOS FICTÍCIOS/.test(faixa), 'faixa mostra DADOS FICTÍCIOS');
    ok(await page.title() === 'Painel comercial Zion (dados fictícios)', 'título marca dados fictícios');
    // sem overflow horizontal
    const ov = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
    ok(ov.sw <= ov.cw, 'sem overflow horizontal (' + ov.sw + ' <= ' + ov.cw + ')');
    // KPIs: CPA do topo = valor do JSON
    const T = D.analise.totais;
    const brl = v => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v).replace(/ /g, ' ');
    const kv = async (t) => (await page.textContent(`[data-kpi="${t}"] .v`)).trim();
    ok(await kv('CPA (custo por comprador)') === brl(T.cpa), 'KPI CPA = ' + brl(T.cpa));
    ok(await kv('Gasto de mídia') === brl(T.gasto), 'KPI gasto = ' + brl(T.gasto));
    ok(await kv('Vendas aprovadas') === String(T.compras), 'KPI vendas = ' + T.compras);
    ok((await page.textContent('[data-kpi="Margem de contribuição"] .chip')).trim() === 'Estimado', 'margem marcada como Estimado (parcial)');
    // funil 7 etapas
    ok(await page.locator('#funil .et').count() === 7, 'funil com 7 etapas');
    // tabela: uma linha por anúncio, decisões e perfis
    const linhas = D.analise.criativos.length;
    ok(await page.locator('#tab tbody tr').count() === linhas, 'tabela com ' + linhas + ' linhas');
    for (const c of D.analise.criativos) {
      const tr = page.locator(`#tab tbody tr[data-anuncio="${c.criativo}"]`);
      const txt = await tr.textContent();
      ok(txt.includes(c.decisao), c.criativo + ' decisão ' + c.decisao + ' na tabela');
      if (c.perfil) ok(txt.includes(c.perfil), c.criativo + ' perfil ' + c.perfil);
    }
    ok((await page.textContent('#tab tbody')).includes('★'), 'vencedor marcado com ★');
    ok(await page.locator('#sem .card.venc').count() === 1, 'um card vencedor no semáforo');
    ok((await page.textContent('#cxc')).includes('menor custo por checkout, mas não é o menor CPA'), 'alerta de armadilha visível');
    ok(await page.locator('#serie svg').count() === 1, 'gráfico SVG da série diária');
    ok(await page.locator('#qual .card').count() === 4, 'seção qualidade dos dados com 4 cartões');
    ok((await page.textContent('#qual')).includes('TX-X-099'), 'divergência de conciliação aparece');
    // funil híbrido (exemplo FICTÍCIO): quente x frio x global, coortes, CPL, tempo até a compra
    const Hb = D.hibrido;
    ok(await page.isVisible('#hib-sec'), 'seção Funil híbrido visível');
    ok((await page.textContent('#hib-rotulo')).includes('EXEMPLO FICTÍCIO'), 'funil híbrido rotulado como exemplo fictício');
    for (const k of ['quente', 'frio', 'global']) {
      const t = await page.textContent(`[data-caminho="${k}"] [data-campo="CPA"]`);
      ok(t.includes(brl(Hb.caminhos[k].cpa)), 'CPA ' + k + ' = ' + brl(Hb.caminhos[k].cpa));
    }
    ok((await page.textContent('[data-kpi="CPL (custo por lead)"] .v')).trim() === brl(Hb.cpl), 'KPI CPL = ' + brl(Hb.cpl));
    ok(await page.locator('#tab-coortes tbody tr').count() === Hb.coortes.length, 'tabela de coortes com ' + Hb.coortes.length + ' linhas');
    const pctf = v => new Intl.NumberFormat('pt-BR', { style: 'percent', minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(v);
    ok((await page.textContent(`#tab-coortes tr[data-coorte="${Hb.coortes[0].data}"]`)).includes(pctf(Hb.coortes[0].conv_7d)), 'conversão 7d da coorte 1 = ' + pctf(Hb.coortes[0].conv_7d));
    ok((await page.textContent(`#tab-coortes tr[data-coorte="${Hb.coortes[3].data}"]`)).includes('indisponível'), 'coorte imatura aparece "indisponível" (não zero)');
    ok((await page.textContent('[data-kpi="Conversão lead → comprador 7d"] .v')).trim() === pctf(Hb.coortes_total.conv_7d), 'KPI conversão 7d agregada só de coortes maduras');
    ok((await page.textContent('[data-kpi="Tempo até a compra (dias, média)"] .v')).trim().length > 0, 'KPI tempo até a compra presente');
    const thc = await page.evaluate(() => getComputedStyle(document.querySelector('#tab-coortes thead')).display);
    ok(nome.startsWith('mobile') ? thc === 'none' : thc !== 'none', 'tabela de coortes responsiva');
    // mobile: cartões (thead oculto); desktop: tabela
    const thead = await page.evaluate(() => getComputedStyle(document.querySelector('#tab thead')).display);
    ok(nome.startsWith('mobile') ? thead === 'none' : thead !== 'none', 'tabela responsiva (' + (nome.startsWith('mobile') ? 'cartões' : 'tabela') + ')');
    // alvo de toque mínimo no mobile (botão de arquivo existe oculto até necessário)
    await page.screenshot({ path: path.join(OUT, nome + '.png'), fullPage: true });
    ok(erros.length === 0, 'sem erros de console' + (erros.length ? ': ' + erros.join(' | ') : ''));
    await ctx.close();
  }
  // estado vazio: sem dados.json nem exemplo -> pede arquivo; carrega pelo seletor
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await ctx.newPage(); const erros = [];
  page.on('pageerror', e => erros.push(e.message));
  await page.route('**/dados*.json', r => r.fulfill({ status: 404, body: 'x' }));
  await page.goto(base); await page.waitForSelector('#carrega:not([hidden])');
  console.log('== estado sem dados ==');
  ok(await page.isHidden('#app'), 'sem dados: painel escondido e pedido de arquivo visível');
  await page.setInputFiles('#arq', path.join(DIR, 'dados_exemplo.json'));
  await page.waitForSelector('body[data-pronto="1"]');
  ok(await page.isVisible('#app') && await page.isHidden('#carrega'), 'carrega pelo seletor de arquivo');
  await page.screenshot({ path: path.join(OUT, 'carregado-pelo-seletor-390.png') });
  // indisponível não vira zero: remove eventos e confere
  const sem = JSON.parse(JSON.stringify(D));
  for (const c of sem.analise.criativos) { c.visitas = c.checkouts = c.cliques_cta = c.cp_chk = c.cpv = c.conv_landing = c.conv_checkout = c.perfil = null; }
  for (const k of ['visitas', 'checkouts', 'cliques_cta', 'cpv', 'cp_chk', 'conv_landing', 'conv_checkout']) sem.analise.totais[k] = null;
  for (const e of sem.analise.funil) if (['visitas','ofertas','cliques_cta','checkouts','pix_gerados'].includes(e.campo)) { e.quantidade = null; e.taxa_anterior = null; e.taxa_visitas = null; }
  const tmp = path.join(OUT, 'sem_eventos.json'); fs.writeFileSync(tmp, JSON.stringify(sem));
  await page.setInputFiles('#arq', tmp);
  await page.waitForTimeout(200);
  ok((await page.textContent('[data-kpi="Visitas à landing"] .v')).trim() === 'indisponível', 'visitas ausentes aparecem como "indisponível" (não zero)');
  ok((await page.textContent('[data-etapa="Início efetivo de checkout"]')).includes('indisponível'), 'etapa sem dado aparece "indisponível"');
  const semh = JSON.parse(JSON.stringify(D)); delete semh.hibrido;
  const tmph = path.join(OUT, 'sem_hibrido.json'); fs.writeFileSync(tmph, JSON.stringify(semh));
  await page.setInputFiles('#arq', tmph); await page.waitForTimeout(200);
  ok(await page.isHidden('#hib-sec'), 'sem dados do funil híbrido, a seção fica escondida (nada de zeros)');
  ok(erros.length === 0, 'sem erros de página no estado vazio/seletor');
  await ctx.close(); await browser.close(); srv.close();
  console.log(falhas ? '\nRESULTADO: ' + falhas + ' FALHA(S)' : '\nRESULTADO: TODOS OS TESTES DO DASHBOARD PASSARAM');
  console.log('Capturas em ' + OUT);
  process.exit(falhas ? 1 : 0);
})();

/* Teste das 8 fichas "Faça agora" (Playwright, 390x844), ANTES (docs/) e DEPOIS (patch/docs/ sobre docs/).
   Uso (da raiz do repositório):  NODE_PATH=$(npm root -g) node zion-sales-engine/15-correcoes-produto/testes/teste_fichas.js [antes|depois|ambos]
   Nenhuma requisição sai de verdade: tudo que não é 127.0.0.1 é interceptado e respondido localmente
   (jsPDF vem do pacote npm; fontes recebem CSS vazio; qualquer outra coisa recebe 200 {} e fica REGISTRADA como "saída").
   Todos os dados são fictícios. Sai com código 1 se o DEPOIS falhar em algum critério. */
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const RAIZ = path.resolve(__dirname, '../../..');
const PATCH = path.join(RAIZ, 'zion-sales-engine/15-correcoes-produto/patch/docs');
const DOCS = path.join(RAIZ, 'docs');
let JSPDF = process.env.JSPDF;
if (!JSPDF) { try { JSPDF = require.resolve('jspdf/dist/jspdf.umd.min.js'); } catch (e) {} }
if (!JSPDF) { const g = '/tmp/claude-0/-home-user-zion-hotel-ai-developer/20b679d3-1387-56c1-a153-2b815cdf3664/scratchpad/npmlib/node_modules/jspdf/dist/jspdf.umd.min.js'; if (fs.existsSync(g)) JSPDF = g; }
if (!JSPDF) { console.error('jsPDF não encontrado: defina JSPDF=/caminho/jspdf.umd.min.js (pacote npm jspdf)'); process.exit(2); }

const FICHAS = (process.env.FICHAS ? process.env.FICHAS.split(',') : ['marco-zero', 'aula1', 'aula2', 'aula3', 'pilar4', 'pilar5', 'pilar6', 'pilar7']);
const NOME = { 'marco-zero': 'Diagnóstico prévio', aula1: 'Pilar 1 · Território', aula2: 'Pilar 2 · Mercado', aula3: 'Pilar 3 · Produto', pilar4: 'Pilar 4 · Modelo de negócio', pilar5: 'Pilar 5 · Masterplan', pilar6: 'Pilar 6 · Pré-viabilidade', pilar7: 'Pilar 7 · Dossiê' };
const PERMITIDOS = [/^fonts\.googleapis\.com$/, /^fonts\.gstatic\.com$/, /^cdnjs\.cloudflare\.com$/]; // só GET de biblioteca/fonte
const PROIBIDOS = /Land Bank|Land Members|banco de áreas|Banco de áreas|Enviar ao|monta o seu estudo|montar o seu estudo|vai para a equipe|lovable\.app|api\.clickmax\.io|zx-lead|cxs\(/i;

function servidor(raizes) {
  return new Promise((ok) => {
    const s = http.createServer((q, r) => {
      let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
      for (const raiz of raizes) {
        const f = path.join(raiz, p);
        if (f.startsWith(raiz) && fs.existsSync(f) && fs.statSync(f).isFile()) {
          const tipo = f.endsWith('.js') ? 'text/javascript' : f.endsWith('.html') ? 'text/html;charset=utf-8' : 'application/octet-stream';
          r.writeHead(200, { 'content-type': tipo }); return r.end(fs.readFileSync(f));
        }
      }
      r.writeHead(404); r.end();
    }).listen(0, '127.0.0.1', () => ok(s));
  });
}

/* preenche a tela atual de forma genérica, com dados fictícios */
async function preencheTela(pg, modo) {
  await pg.evaluate((modo) => {
    const numerico = modo > 0; const VALOR = ['100', '5', '100', '1'][modo % 4];
    const vis = (e) => !!(e.offsetParent || e.getClientRects().length);
    const grupos = {};
    document.querySelectorAll('input,textarea,select').forEach((e) => {
      if (e.closest('#zlb,#anexos-zion,#reuniao-zion')) return;
      if (e.type === 'file' || e.type === 'hidden') return;
      if (e.type === 'radio') { const g = e.name || '_'; (grupos[g] = grupos[g] || []).push(e); return; }
      if (!vis(e) && e.type !== 'range') return;
      const set = (v) => { e.value = v; e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); };
      if (e.tagName === 'SELECT') { if (e.selectedIndex <= 0 && e.options.length > 1) { e.selectedIndex = 1; e.dispatchEvent(new Event('change', { bubbles: true })); } return; }
      if (e.type === 'checkbox') return;
      if (e.value && !(numerico && e.id === 'resp')) return;
      if (e.type === 'number' || e.inputMode === 'numeric' || e.inputMode === 'decimal') set(VALOR); else if (e.type === 'email') set('teste@exemplo.invalid'); else if (e.type === 'date') set('2027-03-01'); else set(numerico ? VALOR : 'Dado fictício de teste');
    });
    const cks = [...document.querySelectorAll('input[type=checkbox]')].filter((e) => !e.closest('#zlb,#anexos-zion,#reuniao-zion') && vis(e));
    if (cks.length && !cks.some((x) => x.checked)) { cks[0].click(); }
    Object.values(grupos).forEach((g) => { if (!g.some((x) => x.checked)) { const e = g[0]; e.checked = true; e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); e.click(); } });
  }, modo);
}

async function percorre(pg) {
  // identificação (se houver) e avanço até a tela do resultado (#pdf)
  let ultimo = '', parado = 0;
  for (let i = 0; i < 160; i++) {
    const agora = await pg.evaluate(() => document.body.innerText.slice(0, 400)); parado = agora === ultimo ? parado + 1 : 0; ultimo = agora;
    if (await pg.locator('#pdf').first().isVisible().catch(() => false)) return true;
    const id = await pg.locator('#nome').first().isVisible().catch(() => false);
    if (id) {
      await pg.fill('#nome', 'Teste Fictício'); if (await pg.locator('#email').count()) await pg.fill('#email', 'teste@exemplo.invalid');
      if (await pg.locator('#cidade').count()) await pg.fill('#cidade', 'Cidade Fictícia');
      if (await pg.locator('#uf').count()) await pg.selectOption('#uf', { index: 1 }).catch(() => {});
    }
    await preencheTela(pg, parado % 4);
    const alvo = pg.locator('#comecar:visible, #continuar:visible, #avancar:visible, #vai:visible, #ver:visible, #prox:visible, button.btn-p:visible').first();
    if (!(await alvo.count())) { await pg.waitForTimeout(150); continue; }
    await alvo.click({ timeout: 3000 }).catch(() => {});
    await pg.waitForTimeout(60);
  }
  if (process.env.DEPURA) console.log('PARADO:', await pg.evaluate(() => document.body.innerText.slice(0, 700)), await pg.evaluate(() => [...document.querySelectorAll('button,input,select,textarea')].filter((e) => e.offsetParent).map((e) => e.tagName + '#' + e.id + '.' + e.className + ':' + (e.type || '') + ':' + (e.innerText || '').slice(0, 20)).join(' | ')));
  return await pg.locator('#pdf').first().isVisible().catch(() => false);
}

async function rodaAmbiente(rotulo, raizes) {
  const srv = await servidor(raizes); const porta = srv.address().port; const base = `http://127.0.0.1:${porta}`;
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, acceptDownloads: true });
  let fase = 'carga'; const saidas = [];
  await ctx.route((u) => u.hostname !== '127.0.0.1', async (route) => {
    const rq = route.request(); const u = new URL(rq.url());
    saidas.push({ fase, metodo: rq.method(), host: u.hostname, url: u.origin + u.pathname, tipo: rq.resourceType(), corpo: rq.postData() ? rq.postData().length : 0 });
    if (/jspdf/i.test(u.pathname)) return route.fulfill({ status: 200, contentType: 'text/javascript', body: fs.readFileSync(JSPDF) });
    if (/fonts\.googleapis/.test(u.hostname)) return route.fulfill({ status: 200, contentType: 'text/css', body: '' });
    if (/fonts\.gstatic/.test(u.hostname)) return route.fulfill({ status: 200, contentType: 'font/woff2', body: '' });
    if (rq.resourceType() === 'script') return route.fulfill({ status: 200, contentType: 'text/javascript', body: '' });
    if (rq.resourceType() === 'image') return route.fulfill({ status: 200, contentType: 'image/gif', body: Buffer.from('R0lGODlhAQABAAAAACw=', 'base64') });
    return route.fulfill({ status: 200, contentType: 'application/json', headers: { 'access-control-allow-origin': '*' }, body: '{"ok":true}' }); // bloqueada aqui: nunca chega ao host real
  });
  const res = [];
  for (const f of FICHAS) {
    const pg = await ctx.newPage(); const erros = []; pg.on('pageerror', (e) => erros.push(String(e).slice(0, 120)));
    const r = { ficha: f, nome: NOME[f] };
    fase = 'carga:' + f; const n0 = saidas.length;
    await pg.goto(`${base}/trilha1/${f}/`, { waitUntil: 'load' }); await pg.waitForTimeout(600);
    r.carregou = (await pg.locator('#comecar, #avancar, button').count()) > 0;
    r.nadaInicio = ((await pg.evaluate(() => document.body.innerText)).match(/[^.\n]*Nada é enviado[^.\n]*\./g) || []).map((x) => x.trim());
    fase = 'preenche+salva:' + f;
    r.chegouResultado = await percorre(pg);
    await pg.waitForTimeout(500);
    r.salvoNoNavegador = await pg.evaluate(() => Object.keys(localStorage).filter((k) => /^zion/.test(k)));
    const tela = await pg.evaluate(() => document.body.innerText);
    r.lbBloco = await pg.locator('#zlb').count(); r.lbBotao = await pg.locator('#zlb-btn').count();
    r.anexosBloco = await pg.locator('#anexos-zion').count(); r.reuniaoBloco = await pg.locator('#reuniao-zion').count();
    r.anexosTemUpload = await pg.locator('#anexos-zion input[type=file]').count();
    r.nadaEEnviado = (tela.match(/[^.\n]*Nada é enviado[^.\n]*\./g) || []);
    r.termosNaTela = [...new Set((tela.match(new RegExp(PROIBIDOS.source, 'gi')) || []).map((x) => x.toLowerCase()))];
    r.blocoTexto = await pg.evaluate(() => { const e = document.querySelector('#zlb,#anexos-zion,#reuniao-zion'); return e ? e.innerText.replace(/\s+/g, ' ').slice(0, 260) : ''; });
    r.saidasAteResultado = saidas.slice(n0).filter((s) => s.fase.startsWith('carga') || s.fase.startsWith('preenche')).map((s) => ({ ...s }));
    // PDF
    fase = 'pdf:' + f; const n1 = saidas.length;
    try {
      const [dl] = await Promise.all([pg.waitForEvent('download', { timeout: 15000 }), pg.click('#pdf')]);
      const p = await dl.path(); const buf = fs.readFileSync(p);
      r.pdf = { arquivo: dl.suggestedFilename(), bytes: buf.length, valido: buf.slice(0, 5).toString() === '%PDF-', paginas: (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length };
    } catch (e) { r.pdf = { erro: String(e).slice(0, 100) }; }
    await pg.waitForTimeout(2500);
    r.saidasAoBaixarPdf = saidas.slice(n1).filter((s) => s.fase === 'pdf:' + f).map((s) => ({ ...s }));
    // clique em "Enviar ao Land Bank" (só existe no ANTES): mostra o que o botão faz
    r.lbClique = null;
    if (r.lbBotao) {
      fase = 'lb-clique:' + f; const n2 = saidas.length;
      await pg.evaluate(() => { const c = document.getElementById('zlb-ok'); if (c) c.click(); const e = document.getElementById('zlb-email'); if (e && e.offsetParent) { e.value = 'teste@exemplo.invalid'; e.dispatchEvent(new Event('input', { bubbles: true })); } });
      await pg.click('#zlb-btn').catch(() => {}); await pg.waitForTimeout(1200);
      r.lbClique = saidas.slice(n2).filter((s) => s.fase === fase).map((s) => `${s.metodo} ${s.url}`);
    }
    // mentor virtual: pedido só por clique (opt-in), registrado à parte
    r.mentor = null;
    if (await pg.locator('#mentor-pedir').count()) {
      fase = 'mentor:' + f; const n3 = saidas.length;
      await pg.click('#mentor-pedir').catch(() => {}); await pg.waitForTimeout(1200);
      r.mentor = saidas.slice(n3).filter((s) => s.fase === fase).map((s) => `${s.metodo} ${s.host}${new URL(s.url).pathname}`);
    }
    r.errosJs = erros;
    res.push(r); await pg.close();
  }
  // varredura do código servido (texto dos arquivos), independente da tela
  const fonte = {};
  for (const arq of [...FICHAS.map((f) => `trilha1/${f}/index.html`), 'trilha1/_landbank.js', 'trilha1/_anexos.js', 'trilha1/_reuniao.js']) {
    let txt = ''; for (const raiz of raizes) { const f = path.join(raiz, arq); if (fs.existsSync(f)) { txt = fs.readFileSync(f, 'utf8'); break; } }
    const lins = txt.split('\n').map((l, i) => [i + 1, l]).filter(([, l]) => PROIBIDOS.test(l) && !/^\s*(\/\/|\/\*)/.test(l) && !/FEEDBACK_URL\s*=|Endereço do mentor virtual/.test(l)); // FEEDBACK_URL = mentor virtual (clique opcional do aluno): resíduo conhecido, ver NF-1c
    fonte[arq] = { achados: [...new Set(lins.map(([, l]) => (l.match(new RegExp(PROIBIDOS.source, 'i')) || [''])[0].toLowerCase()))], chamaFetchPost: /fetch\([^)]*POST|method:\s*"POST"|sendBeacon|XMLHttpRequest/.test(txt), soMentor: (txt.match(/method: "POST"/g) || []).length };
  }
  await browser.close(); srv.close();
  return { rotulo, res, saidas, fonte };
}

function relata(a) {
  const L = []; const p = (s = '') => L.push(s);
  p(`===== ${a.rotulo} =====`);
  p('ficha | resultado | salvo | PDF (páginas/bytes) | Land Bank (bloco/botão) | anexos/reunião | req. de SAÍDA ao baixar PDF | req. de saída carga+preenchimento');
  const fora = (s) => !PERMITIDOS.some((r) => r.test(s.host)) || s.metodo !== 'GET';
  for (const r of a.res) {
    const pdf = r.pdf && r.pdf.valido ? `${r.pdf.paginas}p/${r.pdf.bytes}B` : 'FALHOU ' + JSON.stringify(r.pdf);
    const sPdf = r.saidasAoBaixarPdf.filter(fora).map((s) => `${s.metodo} ${s.host}`);
    const sCar = r.saidasAteResultado.filter(fora).map((s) => `${s.metodo} ${s.host}`);
    p(`${r.ficha} | ${r.chegouResultado ? 'ok' : 'NÃO CHEGOU'} | ${r.salvoNoNavegador.length} chave(s) | ${pdf} | ${r.lbBloco}/${r.lbBotao} | ${r.anexosBloco}(upload ${r.anexosTemUpload})/${r.reuniaoBloco} | ${sPdf.length ? sPdf.join('; ') : '0'} | ${sCar.length ? [...new Set(sCar)].join('; ') : '0'}`);
  }
  p(); p('-- frase "Nada é enviado" (tela inicial da ficha / tela do resultado):');
  for (const r of a.res) p(`  ${r.ficha}: inicial: ${r.nadaInicio.length ? r.nadaInicio.join(' | ') : '(não aparece)'} ; resultado: ${r.nadaEEnviado.length ? r.nadaEEnviado.map((x) => x.trim()).join(' | ') : '(não aparece)'}`);
  p('-- termos antigos na tela:'); for (const r of a.res) p(`  ${r.ficha}: ${r.termosNaTela.length ? r.termosNaTela.join(', ') : 'limpo'}`);
  p('-- bloco de anexos/reunião/Land Bank na tela:'); for (const r of a.res) if (r.blocoTexto) p(`  ${r.ficha}: ${r.blocoTexto}`);
  p('-- clique em "Enviar ao Land Bank" (requisições geradas):'); for (const r of a.res) if (r.lbBotao) p(`  ${r.ficha}: ${r.lbClique && r.lbClique.length ? r.lbClique.join('; ') : '(nenhuma)'}`);
  p('-- mentor virtual (clique opcional do aluno; fora do critério de aprovação):'); for (const r of a.res) if (r.mentor) p(`  ${r.ficha}: ${r.mentor.length ? r.mentor.join('; ') : '(nenhuma)'}`);
  p('-- varredura do código servido (termos antigos / envio):'); for (const [k, v] of Object.entries(a.fonte)) p(`  ${k}: ${v.achados.length ? v.achados.join(', ') : 'limpo'}${v.chamaFetchPost ? ` [fetch POST: ${v.soMentor}; no DEPOIS o único é pedirMentor, por clique]` : ''}`);
  const perm = a.saidas.filter((s) => !fora(s)); const sai = a.saidas.filter(fora);
  const uniq = (arr) => [...new Set(arr.map((s) => `${s.metodo} ${s.host}`))];
  p(); p(`-- total de requisições externas interceptadas: ${a.saidas.length} (estáticas permitidas GET fontes/jsPDF: ${perm.length}; DEMAIS: ${sai.length})`);
  p(`   hosts das demais: ${sai.length ? uniq(sai).join('; ') : 'nenhum'}`);
  p(`   erros de JS: ${a.res.map((r) => r.errosJs.length ? r.ficha + ':' + r.errosJs.join('|') : '').filter(Boolean).join(' ; ') || 'nenhum'}`);
  return L.join('\n');
}

function criterios(a) {
  const f = (s) => !PERMITIDOS.some((r) => r.test(s.host)) || s.metodo !== 'GET';
  const falhas = [];
  for (const r of a.res) {
    if (!r.carregou) falhas.push(`${r.ficha}: não carregou`);
    if (!r.chegouResultado) falhas.push(`${r.ficha}: não chegou à tela do resultado`);
    if (!r.salvoNoNavegador.length) falhas.push(`${r.ficha}: não salvou no navegador`);
    if (!(r.pdf && r.pdf.valido)) falhas.push(`${r.ficha}: PDF inválido`);
    if (r.lbBloco || r.lbBotao) falhas.push(`${r.ficha}: bloco/botão Land Bank presente`);
    if (r.anexosTemUpload) falhas.push(`${r.ficha}: bloco de anexos ainda tem upload`);
    if (r.saidasAoBaixarPdf.filter(f).length) falhas.push(`${r.ficha}: requisição de saída ao baixar o PDF`);
    if (r.saidasAteResultado.filter(f).length) falhas.push(`${r.ficha}: requisição de saída na carga/preenchimento`);
    if (r.termosNaTela.length) falhas.push(`${r.ficha}: termo antigo na tela: ${r.termosNaTela}`);
    if (r.errosJs.length) falhas.push(`${r.ficha}: erro de JS ${r.errosJs}`);
  }
  for (const [k, v] of Object.entries(a.fonte)) { if (v.achados.length) falhas.push(`${k}: termo antigo no código: ${v.achados}`); }
  for (const k of ['trilha1/_landbank.js', 'trilha1/_anexos.js', 'trilha1/_reuniao.js']) if (a.fonte[k].chamaFetchPost) falhas.push(`${k}: contém fetch POST/XHR/beacon`);
  // "Nada é enviado" só pode aparecer se não houver saída (já coberto acima) 
  return falhas;
}

(async () => {
  const modo = process.argv[2] || 'ambos'; let codigo = 0;
  if (modo === 'antes' || modo === 'ambos') { const a = await rodaAmbiente('ANTES (arquivos originais em docs/)', [DOCS]); console.log(relata(a)); const fl = criterios(a); console.log(`\nANTES: ${fl.length} falha(s) de critério (esperado: várias, é a prova do achado)\n  - ${fl.slice(0, 40).join('\n  - ')}\n`); }
  if (modo === 'depois' || modo === 'ambos') { const a = await rodaAmbiente('DEPOIS (patch/docs/ sobre docs/)', [PATCH, DOCS]); console.log(relata(a)); const fl = criterios(a); console.log(`\nDEPOIS: ${fl.length ? 'REPROVADO' : 'APROVADO'} (${fl.length} falha(s))` + (fl.length ? '\n  - ' + fl.join('\n  - ') : '')); if (fl.length) codigo = 1; }
  process.exit(codigo);
})();

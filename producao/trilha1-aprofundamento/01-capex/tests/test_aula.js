/* Teste de ponta a ponta da aula interativa do Aprofundamento 6A · CAPEX (docs/trilha1/apresentacao/pilar6a-aula/).
   Uso: node producao/trilha1-aprofundamento/01-capex/tests/test_aula.js
   Sobe um servidor local (python3 -m http.server servindo docs/), abre a aula no Chromium em
   390x844 (celular) e 1280x800 (computador), percorre os 38 slides e confere: zero erros de JS na aula,
   sem rolagem horizontal, nenhum texto transbordando do slide, número de slides igual ao do roteiro,
   data-bloco sem sigla interna e sem «Bloco 3» a «Bloco 7», interações (retomada, página 6 × 6A,
   previsão, quiz, cartões, calculadora com o limite da página 6, nome, ficha embutida), teclado, toque,
   notas, modo apresentador, leitura da página 6 (zion-t1-pilar6) e salvamento local depois de recarregar,
   gravando só respostas.pagina6Total, respostas.d3 e respostas.nome na chave da ficha.
   Qualquer domínio externo é bloqueado e anotado. As mensagens da ficha embutida (../../pilar6a/,
   testada pelo test_e2e.js) são anotadas à parte e não contam como erro da aula.
   Salva 3 capturas a 1x em ../demonstracao/aula-*.png. */
'use strict';
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const http = require('http');

const RAIZ = path.resolve(__dirname, '../../../..');
const DOCS = path.join(RAIZ, 'docs');
const ROTEIRO = path.resolve(__dirname, '../ROTEIRO_APRESENTACAO.md');
const DEMO = path.resolve(__dirname, '../demonstracao');
const PORTA = 8000 + Math.floor(Math.random() * 900);
const BASE = `http://127.0.0.1:${PORTA}`;
const URL_AULA = `${BASE}/trilha1/apresentacao/pilar6a-aula/`;
const URL_FICHA = `${BASE}/trilha1/pilar6a/`;
const N_SLIDES = 38;

const resultado = { ok: 0, falhas: [], bloqueados: new Set(), erros: [], daFicha: [] };
function confere(cond, nome, detalhe) {
  if (cond) resultado.ok++;
  else { resultado.falhas.push(nome + (detalhe !== undefined ? ' · ' + JSON.stringify(detalhe) : '')); }
}
const espera = (ms) => new Promise((r) => setTimeout(r, ms));

function sobeServidor() {
  const srv = spawn('python3', ['-m', 'http.server', String(PORTA), '--bind', '127.0.0.1', '--directory', DOCS], { stdio: 'ignore' });
  return new Promise((resolve, reject) => {
    let n = 0;
    const tenta = () => http.get(BASE + '/', (r) => { r.resume(); resolve(srv); }).on('error', () => { if (++n > 50) reject(new Error('servidor não subiu')); else setTimeout(tenta, 100); });
    tenta();
  });
}

function slidesDoRoteiro() {
  const md = fs.readFileSync(ROTEIRO, 'utf8');
  const nums = new Set();
  for (const m of md.matchAll(/^#{3,4} Slide (\d+)\b/gm)) nums.add(+m[1]);
  return nums.size;
}

async function novoContexto(browser, vp, extra) {
  const ctx = await browser.newContext(Object.assign({ viewport: vp, deviceScaleFactor: 1 }, extra || {}));
  await ctx.route('**/*', (route) => {
    const u = new URL(route.request().url());
    if (u.hostname === '127.0.0.1' || u.protocol === 'data:' || u.protocol === 'blob:') return route.continue();
    resultado.bloqueados.add(u.hostname);
    return route.abort();
  });
  return ctx;
}
function vigia(page, rotulo) {
  page.on('pageerror', (e) => {
    const daFicha = /\/trilha1\/pilar6a\//.test(String(e.stack || ''));
    (daFicha ? resultado.daFicha : resultado.erros).push(`[${rotulo}] pageerror: ${e.message}`);
  });
  page.on('console', (m) => {
    if (m.type() !== 'error') return;
    const u = (m.location() && m.location().url) || '';
    const daFicha = u.startsWith(URL_FICHA) || (/Failed to load resource/.test(m.text()) && !u.startsWith(BASE));
    (daFicha ? resultado.daFicha : resultado.erros).push(`[${rotulo}] console: ${m.text()} ${u}`);
  });
}

/* Mede um slide já revelado por inteiro. */
async function medeSlide(page, i, celular) {
  return page.evaluate(({ i, celular }) => {
    const slides = Array.from(document.querySelectorAll('.s'));
    const s = slides[i];
    const out = { on: slides.filter((x) => x.classList.contains('on')).length === 1 && s.classList.contains('on'), probs: [] };
    const de = document.documentElement;
    out.hscroll = Math.max(de.scrollWidth, document.body.scrollWidth) - innerWidth;
    // o número grande ao fundo dos slides de bloco (.num-bg, do motor) vaza de propósito e fica cortado: não conta
    const nb = s.querySelector('.num-bg'); if (nb) nb.style.display = 'none';
    out.sh = s.scrollHeight - s.clientHeight; out.sw = s.scrollWidth - s.clientWidth;
    if (nb) nb.style.display = '';
    const R = s.getBoundingClientRect();
    const tol = 2;
    for (const el of s.querySelectorAll('*')) {
      if (el.closest('aside, .bg, .num-bg')) continue;
      const cs = getComputedStyle(el);
      if (cs.display === 'none') continue;
      const r = el.getBoundingClientRect();
      if (!r.width && !r.height) continue;
      const nome = (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : el.tagName.toLowerCase()) + ' "' + (el.textContent || '').trim().slice(0, 40) + '"';
      if (celular) {
        if (r.right > innerWidth + tol || r.left < -tol) out.probs.push('fora na largura: ' + nome);
      } else if (r.bottom > R.bottom + tol || r.top < R.top - tol || r.right > R.right + tol || r.left < R.left - tol) out.probs.push('fora do slide: ' + nome);
      const corta = ['hidden', 'auto', 'scroll', 'clip'];
      if (el.tagName !== 'INPUT' && el.tagName !== 'SELECT' && el.tagName !== 'TEXTAREA') {
        if (corta.includes(cs.overflowY) && el.scrollHeight > el.clientHeight + tol) out.probs.push('texto cortado na altura: ' + nome);
        if (corta.includes(cs.overflowX) && el.scrollWidth > el.clientWidth + tol) out.probs.push('texto cortado na largura: ' + nome);
      }
    }
    // faces dos cartões que viram (absolutas): o texto precisa caber
    for (const f of s.querySelectorAll('.pq .fr, .pq .vs')) {
      const hIn = Array.from(f.children).reduce((a, c) => a + c.getBoundingClientRect().height, 0);
      if (f.scrollHeight > f.clientHeight + tol || hIn > f.getBoundingClientRect().height + tol) out.probs.push('cartão transbordando: "' + f.textContent.trim().slice(0, 40) + '"');
    }
    return out;
  }, { i, celular });
}

async function percorre(page, rotulo, celular) {
  const total = await page.evaluate(() => document.querySelectorAll('.s').length);
  for (let i = 0; i < total; i++) {
    await page.evaluate((i) => ZD.vai(i, 'tudo'), i);
    await espera(750);
    const m = await medeSlide(page, i, celular);
    confere(m.on, `${rotulo} slide ${i + 1}: é o único visível`);
    confere(m.hscroll <= 1, `${rotulo} slide ${i + 1}: sem rolagem horizontal`, m.hscroll);
    if (!celular) confere(m.sh <= 1 && m.sw <= 1, `${rotulo} slide ${i + 1}: conteúdo cabe no slide (scrollHeight/clientHeight)`, { sh: m.sh, sw: m.sw });
    confere(m.probs.length === 0, `${rotulo} slide ${i + 1}: nenhum texto transbordando`, m.probs.slice(0, 5));
  }
  return total;
}

async function interacoes(page, rotulo, celular) {
  const vai = (i) => page.evaluate((i) => ZD.vai(i), i);
  const atual = () => page.evaluate(() => Array.from(document.querySelectorAll('.s')).findIndex((s) => s.classList.contains('on')));
  const est = () => page.evaluate(() => JSON.parse(localStorage.getItem('zion-t1-pilar6a')));
  const fb = () => page.locator('.s.on .fb').innerText();

  // navegação pelo botão Avançar: o slide 11 tem 4 itens; o 5º clique troca de slide
  await vai(10);
  for (let k = 0; k < 5; k++) await page.click('#n-prox');
  confere(await atual() === 11, `${rotulo}: botão Avançar revela os itens e troca de slide`);
  await page.click('#n-ant');
  confere(await atual() === 10, `${rotulo}: botão Voltar volta um slide`);

  // slide 4: retomada do Pilar 6 (quiz que grava em aulaExtras)
  await vai(3);
  await page.click('.s.on .opc[data-v="a"]');
  confere(/a resposta é outra/i.test(await fb()) && /infraestrutura comum e o terreno/.test(await fb()), `${rotulo}: retomada errada mostra a certa`, await fb());
  await page.click('.s.on .opc[data-v="b"]');
  confere(/^isso/i.test(await fb()), `${rotulo}: retomada certa confirma`, await fb());

  // slide 7: página 6 × 6A (grava em respostas.pagina6Total)
  await vai(6);
  const inp = page.locator('.s.on input.resp');
  await inp.fill('690.529,18');
  await espera(150);
  const fb7 = await fb();
  confere(/guardado/i.test(fb7) && /R\$ 690\.529,18/.test(fb7), `${rotulo}: número da página 6 gravado com feedback`, fb7);
  confere((await est()).respostas.pagina6Total === '690.529,18', `${rotulo}: vai para respostas.pagina6Total`);
  await page.click('.s.on .opc[data-v="nao_sei"]');
  confere(await page.locator('.s.on input.resp').isDisabled() && (await est()).respostas.pagina6Total === 'nao_sei', `${rotulo}: "Não sei" desativa o campo e grava nao_sei`);
  await page.click('.s.on .opc[data-v="nao_fiz"]');
  let e7 = await est();
  confere(e7.respostas.pagina6Total === undefined && e7.aulaExtras.pagina6 === 'nao_fiz' && /página irmã/i.test(await fb()), `${rotulo}: "Ainda não fiz" fica só na aula`, e7);
  await page.click('.s.on .opc[data-v="nao_fiz"]');
  await page.locator('.s.on input.resp').fill('690.529,18');
  await espera(100);

  // slide 8: previsão (aulaExtras), que volta no slide 31
  await vai(7);
  await page.click('.s.on .opc[data-v="sobe_passa"]');
  confere(/previsão guardada/i.test(await fb()), `${rotulo}: previsão guardada`, await fb());
  await vai(30); await espera(100);
  const eco = await page.locator('#prev-eco').innerText();
  confere(/sobe e passa de R\$ 870 mil/.test(eco) && /errada também ensina/.test(eco), `${rotulo}: a previsão volta no slide Página 6 × 6A`, eco);

  // slide 21: cartões viram no clique
  await vai(20);
  await page.locator('.s.on .pq').nth(1).click();
  confere(await page.locator('.s.on .pq.aberto').count() === 1, `${rotulo}: cartão vira no toque`);
  // slide 22: dois verdadeiro ou falso, um por clique do motor
  await vai(21);
  await page.click('#n-prox');
  await page.click('#n-prox');
  confere(await page.locator('.s.on .quiz.resp').count() === 2, `${rotulo}: slide 22 revela as duas respostas, uma por clique`);
  confere(await page.locator('.s.on .quiz.resp .exp').first().isVisible(), `${rotulo}: verdadeiro ou falso revela a explicação`);
  // slide 33: resposta errada fica marcada e a certa aparece
  await vai(32);
  await page.locator('.s.on .op:not([data-certa])').first().click();
  confere(await page.locator('.s.on .op.errada').count() === 1 && await page.locator('.s.on .op.certa').count() === 1, `${rotulo}: quiz marca a errada e mostra a certa`);

  // slide 27: calculadora com o giro e o limite da página 6 da Marina
  await vai(26);
  const poe = (nome, v) => page.evaluate(({ nome, v }) => { const el = document.querySelector(`.s.on [name="${nome}"]`); el.value = v; el.dispatchEvent(new Event(el.tagName === 'SELECT' ? 'change' : 'input', { bubbles: true })); el.dispatchEvent(new Event('input', { bubbles: true })); }, { nome, v });
  const leSim = () => page.evaluate(() => { const s = document.querySelector('.s.on .sim'); const t = (k) => s.querySelector(`[data-r=${k}]`).textContent; return { res: t('res'), capex: t('capex'), total: t('total'), folga: t('folga'), peso: t('peso'), aviso: s.querySelector('[data-aviso]').className, txt: s.querySelector('[data-aviso]').textContent }; });
  let r = await leSim();
  confere(r.res === 'R$ 103.191' && r.capex === 'R$ 791.131' && r.total === 'R$ 831.918' && r.folga === 'folga de R$ 38.212' && r.peso === '13,0%' && /\bok\b/.test(r.aviso), `${rotulo}: calculadora começa na Marina (15%, verde, folga de R$ 38.212)`, r);
  await poe('pct', '10'); r = await leSim();
  confere(r.res === 'R$ 68.794' && r.capex === 'R$ 756.734' && /\bat\b/.test(r.aviso), `${rotulo}: 10% com primeira obra = amarelo`, r);
  await poe('risco', '0'); r = await leSim();
  confere(/\bok\b/.test(r.aviso), `${rotulo}: 10% sem fator de risco = verde`, r);
  await poe('risco', '1'); await poe('pct', '8'); r = await leSim();
  confere(r.res === 'R$ 55.035' && r.capex === 'R$ 742.975' && /\ber\b/.test(r.aviso), `${rotulo}: 8% = vermelho`, r);
  await poe('pct', '0'); r = await leSim();
  confere(/\ber\b/.test(r.aviso) && /nunca é zero/.test(r.txt), `${rotulo}: 0% = "A reserva nunca é zero"`, r);
  await poe('pct', '20'); r = await leSim();
  confere(r.folga === 'folga de R$ 3.815' && /\bok\b/.test(r.aviso), `${rotulo}: 20% ainda cabe, com folga de R$ 3.815`, r);
  await poe('pct', '21'); r = await leSim();
  confere(r.folga === 'passa R$ 3.064' && /\ber\b/.test(r.aviso) && /Passou do limite/.test(r.txt), `${rotulo}: 21% passa do limite da página 6`, r);
  await poe('sub', '500000'); await poe('pct', '30'); r = await leSim();
  confere(/\bat\b/.test(r.aviso) && /Acima de todas/.test(r.txt), `${rotulo}: 30% dentro do limite = amarelo (acima das faixas)`, r);
  confere(await page.locator('.s.on .sim.mexeu').count() === 1, `${rotulo}: aparece "Ajustado por você"`);
  await page.click('.s.on .reset'); r = await leSim();
  confere(r.capex === 'R$ 791.131' && r.folga === 'folga de R$ 38.212', `${rotulo}: botão volta à conta da Marina`, r);

  // slide 35: critério de conclusão (grava em respostas.d3)
  await vai(34);
  await page.click('.s.on .opc[data-v="algumas"]');
  confere(/deixe em branco/.test(await fb()), `${rotulo}: "cotadas" grava com feedback`, await fb());
  const nav = await page.locator('#n-resp').innerText();
  confere(/4 de 6/.test(nav), `${rotulo}: barra mostra 4 de 6 respondidas`, nav);

  // slide 36: o nome (respostas.nome)
  await vai(35);
  await page.locator('#p-nome').fill('Ana Teste');
  await espera(100);
  confere((await est()).respostas.nome === 'Ana Teste', `${rotulo}: nome gravado em respostas.nome`);

  // slide 37: a ficha dentro da aula
  await vai(36); await espera(400);
  const src = await page.evaluate(() => document.getElementById('diag-fr').src);
  confere(src === URL_FICHA, `${rotulo}: a ficha embutida abre ../../pilar6a/`, src);

  // teclado (computador) e toque (celular)
  await vai(1);
  if (!celular) {
    await page.keyboard.press('ArrowRight');
    confere(await atual() === 2, `${rotulo}: seta para a direita avança`);
    await page.keyboard.press('ArrowLeft');
    confere(await atual() === 1, `${rotulo}: seta para a esquerda volta`);
    await page.keyboard.press('End');
    confere(await atual() === N_SLIDES - 1, `${rotulo}: End vai ao último slide`);
    await page.keyboard.press('Home');
    confere(await atual() === 0, `${rotulo}: Home vai ao primeiro slide`);
    await page.keyboard.press('n');
    const notas = await page.locator('.zd-notas').innerText();
    confere(/Esta aula aprofunda uma linha da página 6/.test(notas), `${rotulo}: tecla N mostra as notas do apresentador`);
    await page.keyboard.press('n');
  } else {
    const swipe = (dx) => page.evaluate((dx) => {
      const t0 = new Touch({ identifier: 1, target: document.body, clientX: 200, clientY: 400 });
      const t1 = new Touch({ identifier: 1, target: document.body, clientX: 200 + dx, clientY: 405 });
      document.body.dispatchEvent(new TouchEvent('touchstart', { touches: [t0], changedTouches: [t0], bubbles: true }));
      document.body.dispatchEvent(new TouchEvent('touchend', { touches: [], changedTouches: [t1], bubbles: true }));
    }, dx);
    await swipe(-150);
    confere(await atual() === 2, `${rotulo}: deslizar para a esquerda avança`);
    await swipe(150);
    confere(await atual() === 1, `${rotulo}: deslizar para a direita volta`);
  }

  // último slide: link da ficha e botão final
  await vai(N_SLIDES - 1);
  const href = await page.evaluate(() => document.getElementById('abrir-ficha').href);
  confere(href === URL_FICHA, `${rotulo}: último slide leva a ../../pilar6a/`, href);
  confere((await page.locator('#n-prox').innerText()).includes('Abrir a ficha'), `${rotulo}: botão final vira "Abrir a ficha"`);
  const txtProx = await page.locator('.s.on').innerText();
  confere(/Meu Dossiê/.test(txtProx) && /cerca de R\$ 690 mil/.test(txtProx) && /não envia nada/.test(txtProx), `${rotulo}: slide Próximo lembra a pasta Meu Dossiê e avisa do Pilar 7`);

  // persistência: recarrega e confere
  await vai(34);
  await espera(200);
  const antes = await est();
  confere(antes.respostas.pagina6Total === '690.529,18' && antes.respostas.d3 === 'algumas' && antes.respostas.nome === 'Ana Teste' && antes.aulaExtras.slide === 34 && antes.aulaExtras.r_fora === 'b' && antes.aulaExtras.previsao === 'sobe_passa', `${rotulo}: estado gravado na chave zion-t1-pilar6a`, antes);
  await page.reload();
  await espera(800);
  confere(await atual() === 34, `${rotulo}: depois de recarregar, volta ao mesmo slide`);
  confere(await page.locator('.s.on .opc[data-v="algumas"]').getAttribute('aria-pressed') === 'true', `${rotulo}: escolha continua marcada depois de recarregar`);
  confere(/4 de 6/.test(await page.locator('#n-resp').innerText()), `${rotulo}: contagem de respondidas persiste`);
  await page.goto(URL_AULA); // sem número no endereço: usa o slide salvo
  await espera(800);
  confere(await atual() === 34, `${rotulo}: abrindo sem # no endereço, volta ao slide salvo`);
  await vai(6); await espera(200);
  confere(await page.locator('.s.on input.resp').inputValue() === '690.529,18', `${rotulo}: número da página 6 continua no campo depois de recarregar`);
  await vai(35); await espera(200);
  confere(await page.locator('#p-nome').inputValue() === 'Ana Teste', `${rotulo}: nome continua no campo depois de recarregar`);
}

/* A estrutura da aula: título, data-bloco e textos proibidos. */
async function estrutura(page, rotulo) {
  const e = await page.evaluate(() => ({
    titulo: document.title, deck: document.body.dataset.titulo,
    blocos: Array.from(document.querySelectorAll('.s')).map((s) => s.dataset.bloco || ''),
    html: document.documentElement.outerHTML,
  }));
  confere(e.titulo === 'Aprofundamento 6A · CAPEX' && e.deck === 'Aprofundamento 6A · CAPEX', `${rotulo}: título «Aprofundamento 6A · CAPEX»`, [e.titulo, e.deck]);
  confere(!/ECROI/i.test(e.html), `${rotulo}: nenhuma sigla ECROI na página`);
  confere(!e.blocos.some((b) => /Bloco [3-7]/.test(b)), `${rotulo}: data-bloco sem «Bloco 3» a «Bloco 7»`);
  const esperados = ['Abertura', 'Como funciona esta aula', 'Retomada · Pilar 6', 'Bloco 1 · As sete partes do custo', 'Bloco 2 · A Marina abre a página 6', 'Quiz relâmpago', 'Resumo', 'A sua página 6A', 'Próximo'];
  const unicos = Array.from(new Set(e.blocos));
  confere(JSON.stringify(unicos.filter((b) => esperados.includes(b))) === JSON.stringify(unicos) && esperados.every((b) => unicos.includes(b)), `${rotulo}: data-bloco na lista do plano`, unicos);
  confere(!/Helena|Ribeir/.test(e.html), `${rotulo}: sem a Helena e os Chalés do Ribeirão`);
  confere(/Método Zion · Etapa 4 · Fechar a conta/.test(e.html) && /O 6A em cinco frases/.test(e.html) && /Parte 7 de 7/.test(e.html), `${rotulo}: selo da Etapa 4, «O 6A em cinco frases» e «Parte 1 a 7»`);
  const partes = Array.from({ length: 7 }, (_, k) => `Parte ${k + 1} de 7`).every((t) => e.html.includes(t));
  confere(partes, `${rotulo}: as sete partes numeradas «Parte N de 7»`);
}

(async () => {
  const srv = await sobeServidor();
  const browser = await chromium.launch();
  fs.mkdirSync(DEMO, { recursive: true });
  try {
    const nRoteiro = slidesDoRoteiro();
    for (const [rotulo, vp, celular, extra] of [
      ['celular 390x844', { width: 390, height: 844 }, true, { hasTouch: true, isMobile: true }],
      ['computador 1280x800', { width: 1280, height: 800 }, false, {}],
    ]) {
      const ctx = await novoContexto(browser, vp, extra);
      const page = await ctx.newPage(); vigia(page, rotulo);
      const resp = await page.goto(URL_AULA);
      confere(resp && resp.ok(), `${rotulo}: página abre (HTTP 200)`);
      await espera(600);
      const nPagina = await page.evaluate(() => document.querySelectorAll('.s').length);
      confere(nPagina === nRoteiro && nPagina === N_SLIDES, `${rotulo}: número de slides igual ao do roteiro`, { pagina: nPagina, roteiro: nRoteiro });
      const img = await page.evaluate(() => Array.from(document.images).filter((i) => i.complete && i.naturalWidth === 0).map((i) => i.src));
      confere(img.length === 0, `${rotulo}: todas as imagens carregam`, img);
      await estrutura(page, rotulo);
      await percorre(page, rotulo, celular);
      await interacoes(page, rotulo, celular);
      await page.evaluate(() => { const t = document.getElementById('toast'); if (t) t.classList.remove('on'); }); // o aviso de retomada não entra nas capturas
      if (celular) {
        await page.evaluate(() => ZD.vai(6)); await espera(700);
        await page.screenshot({ path: path.join(DEMO, 'aula-celular-pagina6.png') });
      } else {
        await page.evaluate(() => { ZD.vai(26); const el = document.querySelector('.s.on [name=pct]'); el.value = '10'; el.dispatchEvent(new Event('input', { bubbles: true })); });
        await espera(700);
        await page.screenshot({ path: path.join(DEMO, 'aula-calculadora.png') });
        await page.evaluate(() => ZD.vai(29, 'tudo')); await espera(900);
        await page.screenshot({ path: path.join(DEMO, 'aula-semaforo.png') });
      }
      await ctx.close();
    }

    // a página 6 já feita neste aparelho: o número aparece e a aula não apaga o que a ficha guardou
    {
      const ctx = await novoContexto(browser, { width: 390, height: 844 }, { hasTouch: true, isMobile: true });
      await ctx.addInitScript(() => {
        if (sessionStorage.getItem('semeado')) return; sessionStorage.setItem('semeado', '1');
        localStorage.setItem('zion-t1-pilar6', JSON.stringify({ resumo: { data: '2026-11-20', dados: { total: 690529.18, inv8: 870130.8 } } }));
        localStorage.setItem('zion-t1-pilar6a', JSON.stringify({ versao: 2, respostas: { projeto: 'Cabanas da Serra', d1: 'estimativa' }, partes: { 1: [{ nome: 'Topografia' }] } }));
      });
      const page = await ctx.newPage(); vigia(page, 'página 6 semeada');
      await page.goto(URL_AULA + '#7'); await espera(700);
      const vx = await page.locator('.s.on [data-veio]').innerText();
      confere(/R\$ 690\.529,18/.test(vx) && /20\/11\/2026/.test(vx), 'página 6 semeada: o número e a data aparecem («Veio da sua página 6»)', vx);
      await page.click('.s.on .usar-veio'); await espera(150);
      const d = await page.evaluate(() => JSON.parse(localStorage.getItem('zion-t1-pilar6a')));
      confere(await page.locator('.s.on input.resp').inputValue() === '690.529,18' && d.respostas.pagina6Total === '690.529,18', 'página 6 semeada: "Usar este número" grava em respostas.pagina6Total', d.respostas);
      confere(d.respostas.projeto === 'Cabanas da Serra' && d.respostas.d1 === 'estimativa' && d.partes && d.partes[1][0].nome === 'Topografia' && d.versao === 2, 'a aula não apaga o que a ficha guardou', d);
      confere(await page.locator('.s.on [data-veio]').isHidden(), 'página 6 semeada: a caixa some depois de usar o número');
      // as outras perguntas da aula, sem abrir a ficha: só três campos novos em respostas
      await page.evaluate(() => ZD.vai(3)); await page.click('.s.on .opc[data-v="b"]');
      await page.evaluate(() => ZD.vai(7)); await page.click('.s.on .opc[data-v="sobe_cabe"]');
      await page.evaluate(() => ZD.vai(34)); await page.click('.s.on .opc[data-v="nenhuma"]');
      await page.evaluate(() => ZD.vai(35)); await page.locator('#p-nome').fill('Marina'); await espera(150);
      const d2 = await page.evaluate(() => JSON.parse(localStorage.getItem('zion-t1-pilar6a')));
      const chaves = Object.keys(d2.respostas).sort().join(',');
      confere(chaves === 'd1,d3,nome,pagina6Total,projeto' && d2.respostas.d3 === 'nenhuma' && d2.respostas.nome === 'Marina', 'a aula grava só respostas.pagina6Total, d3 e nome', d2.respostas);
      confere(d2.aulaExtras.r_fora === 'b' && d2.aulaExtras.previsao === 'sobe_cabe', 'retomada e previsão ficam em aulaExtras', d2.aulaExtras);
      await ctx.close();
    }

    // turma de acompanhamento
    {
      const ctx = await novoContexto(browser, { width: 1280, height: 800 });
      const page = await ctx.newPage(); vigia(page, 'turma');
      await page.goto(URL_AULA + '?turma=acompanhamento#38'); await espera(500);
      const t = await page.evaluate(() => ({ passo: document.getElementById('passo2').textContent, href: document.getElementById('abrir-ficha').href }));
      confere(/encontro do Pilar 6/.test(t.passo) && t.href === `${URL_FICHA}?turma=acompanhamento`, 'turma de acompanhamento: passo 2 e link trocados', t);
      await ctx.close();
    }

    // modo apresentador: a outra janela recebe as notas do slide atual
    {
      const ctx = await novoContexto(browser, { width: 1280, height: 800 });
      const page = await ctx.newPage(); vigia(page, 'aula com apresentador');
      await page.goto(URL_AULA + '#1'); await espera(500);
      const apr = await ctx.newPage(); vigia(apr, 'janela do apresentador');
      await apr.goto(URL_AULA + '?apresentador'); await espera(1500);
      await page.evaluate(() => ZD.vai(26)); await espera(800);
      const nt = await apr.locator('#nt').innerText();
      const pos = await apr.locator('#pos').innerText();
      confere(/Peça que alguém diga um percentual/.test(nt) && /Slide 27 de 38/.test(pos), 'modo apresentador mostra o slide e as notas certas', { pos, nt: nt.slice(0, 60) });
      await apr.click('#prox'); await espera(500);
      const i2 = await page.evaluate(() => Array.from(document.querySelectorAll('.s')).findIndex((s) => s.classList.contains('on')));
      confere(i2 === 27, 'botão Avançar do apresentador troca o slide da aula', i2);
      await ctx.close();
    }

    // sem armazenamento (navegação privada que bloqueia): a aula segue funcionando
    {
      const ctx = await novoContexto(browser, { width: 390, height: 844 }, { hasTouch: true, isMobile: true });
      await ctx.addInitScript(() => { const erro = () => { throw new Error('bloqueado'); }; Storage.prototype.getItem = erro; Storage.prototype.setItem = erro; });
      const page = await ctx.newPage(); vigia(page, 'sem armazenamento');
      await page.goto(URL_AULA + '#7'); await espera(600);
      await page.locator('.s.on input.resp').fill('500000'); await espera(150);
      confere(/guardado/i.test(await page.locator('.s.on .fb').innerText()), 'sem armazenamento: a pergunta responde e não quebra');
      await ctx.close();
    }
  } finally {
    await browser.close();
    srv.kill();
  }
  confere(resultado.erros.length === 0, 'zero erros de JS na aula', resultado.erros.slice(0, 10));
  if (resultado.daFicha.length) console.log('Mensagens da ficha embutida (não contam como erro da aula): ' + resultado.daFicha.length + ' · ' + Array.from(new Set(resultado.daFicha.map((x) => x.replace(/^\[[^\]]*\] /, '')))).slice(0, 5).join(' | '));
  console.log('Domínios externos bloqueados no teste: ' + (resultado.bloqueados.size ? Array.from(resultado.bloqueados).join(', ') : 'nenhum pedido externo'));
  console.log(`Verificações aprovadas: ${resultado.ok} · reprovadas: ${resultado.falhas.length}`);
  resultado.falhas.forEach((f) => console.log('FALHA · ' + f));
  process.exit(resultado.falhas.length ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });

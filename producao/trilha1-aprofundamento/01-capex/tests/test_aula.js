/* Teste de ponta a ponta da aula interativa do CAPEX (docs/trilha1/apresentacao/capex-aula/).
   Uso: node producao/trilha1-aprofundamento/01-capex/tests/test_aula.js
   Sobe um servidor local (python3 -m http.server servindo docs/), abre a aula no Chromium em
   390x844 (celular) e 1280x800 (computador), percorre os 34 slides e confere: zero erros de JS,
   sem rolagem horizontal, nenhum texto transbordando do slide, número de slides igual ao do roteiro,
   interações (quiz, cartões, calculadora, perguntas que gravam), teclado, toque, notas, modo
   apresentador e salvamento local depois de recarregar. Qualquer domínio externo é bloqueado e anotado.
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
const URL_AULA = `${BASE}/trilha1/apresentacao/capex-aula/`;

const resultado = { ok: 0, falhas: [], bloqueados: new Set(), erros: [] };
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
  page.on('pageerror', (e) => resultado.erros.push(`[${rotulo}] pageerror: ${e.message}`));
  page.on('console', (m) => { if (m.type() === 'error') resultado.erros.push(`[${rotulo}] console: ${m.text()}`); });
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
  // navegação pelo botão Avançar: do slide 1 ao 2 passando pelos 3 itens
  await vai(1);
  for (let k = 0; k < 4; k++) await page.click('#n-prox');
  confere(await atual() === 2, `${rotulo}: botão Avançar revela os itens e troca de slide`);
  await page.click('#n-ant');
  confere(await atual() === 1, `${rotulo}: botão Voltar volta um slide`);

  // slide 3: palpite que grava
  await vai(2);
  const inp = page.locator('.s.on input.resp');
  await inp.fill('700.000');
  await espera(150);
  const fb3 = await page.locator('.s.on .fb').innerText();
  confere(/guardado/i.test(fb3) && /R\$ 700\.000/.test(fb3), `${rotulo}: palpite gravado com feedback`, fb3);
  await page.click('.s.on .opc.ns');
  confere(await page.locator('.s.on input.resp').isDisabled(), `${rotulo}: "não tenho" desativa o campo`);
  await page.click('.s.on .opc.ns');
  await page.locator('.s.on input.resp').fill('700.000');
  await espera(100);

  // slide 7: verdadeiro ou falso, clicando na resposta certa
  await vai(6);
  await page.click('.s.on .op[data-certa]');
  confere(await page.locator('.s.on .quiz.resp .exp').isVisible(), `${rotulo}: quiz V ou F revela a explicação`);
  // slide 12: resposta errada fica marcada e a certa aparece
  await vai(11);
  await page.locator('.s.on .op:not([data-certa])').first().click();
  confere(await page.locator('.s.on .op.errada').count() === 1 && await page.locator('.s.on .op.certa').count() === 1, `${rotulo}: quiz marca a errada e mostra a certa`);
  // slide 10: cartões viram no clique
  await vai(9);
  await page.locator('.s.on .pq').nth(1).click();
  confere(await page.locator('.s.on .pq.aberto').count() === 1, `${rotulo}: cartão vira no toque`);
  // slide 21: dois quizzes, um por clique do motor
  await vai(20);
  await page.click('#n-prox');
  await page.click('#n-prox');
  confere(await page.locator('.s.on .quiz.resp').count() === 2, `${rotulo}: slide 21 revela as duas respostas, uma por clique`);

  // slide 24: calculadora + semáforo
  await vai(23);
  const poe = (nome, v) => page.evaluate(({ nome, v }) => { const el = document.querySelector(`.s.on [name="${nome}"]`); el.value = v; el.dispatchEvent(new Event(el.tagName === 'SELECT' ? 'change' : 'input', { bubbles: true })); el.dispatchEvent(new Event('input', { bubbles: true })); }, { nome, v });
  const leSim = () => page.evaluate(() => { const s = document.querySelector('.s.on .sim'); return { res: s.querySelector('[data-r=res]').textContent, capex: s.querySelector('[data-r=capex]').textContent, peso: s.querySelector('[data-r=peso]').textContent, aviso: s.querySelector('[data-aviso]').className, txt: s.querySelector('[data-aviso]').textContent }; });
  let r = await leSim();
  confere(r.res === 'R$ 151.575' && r.capex === 'R$ 1.162.075' && r.peso === '13,0%' && /\bok\b/.test(r.aviso), `${rotulo}: calculadora começa na Helena (15%, verde)`, r);
  await poe('pct', '12'); r = await leSim();
  confere(r.res === 'R$ 121.260' && r.capex === 'R$ 1.131.760' && /\bat\b/.test(r.aviso), `${rotulo}: 12% com primeira obra = amarelo`, r);
  await poe('risco', '0'); r = await leSim();
  confere(/\bok\b/.test(r.aviso), `${rotulo}: 12% sem fator de risco = verde`, r);
  await poe('risco', '1'); await poe('pct', '8'); r = await leSim();
  confere(r.res === 'R$ 80.840' && r.capex === 'R$ 1.091.340' && /\ber\b/.test(r.aviso), `${rotulo}: 8% = vermelho`, r);
  await poe('pct', '0'); r = await leSim();
  confere(/\ber\b/.test(r.aviso) && /nunca é zero/.test(r.txt), `${rotulo}: 0% = "A reserva nunca é zero"`, r);
  await poe('pct', '30'); r = await leSim();
  confere(/\bat\b/.test(r.aviso) && /Acima de todas/.test(r.txt), `${rotulo}: 30% = amarelo (acima das faixas)`, r);
  confere(await page.locator('.s.on .sim.mexeu').count() === 1, `${rotulo}: aparece "Ajustado por você"`);
  await page.click('.s.on .reset'); r = await leSim();
  confere(r.capex === 'R$ 1.162.075', `${rotulo}: botão volta à conta da Helena`, r);

  // slide 30: escolha que grava
  await vai(29);
  await page.click('.s.on .opc[data-v="algumas"]');
  const fb30 = await page.locator('.s.on .fb').innerText();
  confere(/deixe em branco/.test(fb30), `${rotulo}: "cotadas" grava com feedback`, fb30);
  const nav = await page.locator('#n-resp').innerText();
  confere(/2 de 2/.test(nav), `${rotulo}: barra mostra 2 de 2 respondidas`, nav);

  // teclado (computador) e toque (celular)
  await vai(4);
  if (!celular) {
    await page.keyboard.press('ArrowRight');
    confere(await atual() === 5, `${rotulo}: seta para a direita avança`);
    await page.keyboard.press('ArrowLeft');
    confere(await atual() === 4, `${rotulo}: seta para a esquerda volta`);
    await page.keyboard.press('End');
    confere(await atual() === 33, `${rotulo}: End vai ao último slide`);
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
    confere(await atual() === 5, `${rotulo}: deslizar para a esquerda avança`);
    await swipe(150);
    confere(await atual() === 4, `${rotulo}: deslizar para a direita volta`);
  }

  // último slide: link da ficha e botão final
  await vai(33);
  const href = await page.evaluate(() => document.getElementById('abrir-ficha').href);
  confere(href === `${BASE}/trilha1/capex/`, `${rotulo}: último slide leva a ../../capex/`, href);
  confere((await page.locator('#n-prox').innerText()).includes('Abrir a ficha'), `${rotulo}: botão final vira "Abrir a ficha"`);

  // persistência: recarrega e confere
  await vai(29);
  await espera(200);
  const antes = await page.evaluate(() => JSON.parse(localStorage.getItem('zion-t1-pilar6a')));
  const hoje = new Date(); const hojeISO = hoje.getFullYear() + '-' + String(hoje.getMonth() + 1).padStart(2, '0') + '-' + String(hoje.getDate()).padStart(2, '0');
  confere(antes && antes.respostas.palpite === '700.000' && antes.respostas.dataPalpite === hojeISO && antes.respostas.d3 === 'algumas' && antes.aulaExtras.slide === 29, `${rotulo}: estado gravado na chave zion-t1-pilar6a`, antes);
  await page.reload();
  await espera(800);
  confere(await atual() === 29, `${rotulo}: depois de recarregar, volta ao mesmo slide`);
  confere(await page.locator('.s.on .opc[data-v="algumas"]').getAttribute('aria-pressed') === 'true', `${rotulo}: escolha continua marcada depois de recarregar`);
  confere(/2 de 2/.test(await page.locator('#n-resp').innerText()), `${rotulo}: contagem de respondidas persiste`);
  await page.goto(URL_AULA); // sem número no endereço: usa o slide salvo
  await espera(800);
  confere(await atual() === 29, `${rotulo}: abrindo sem # no endereço, volta ao slide salvo`);
  await vai(2); await espera(200);
  confere(await page.locator('.s.on input.resp').inputValue() === '700.000', `${rotulo}: palpite continua no campo depois de recarregar`);
  const depois = await page.evaluate(() => JSON.parse(localStorage.getItem('zion-t1-pilar6a')).respostas.dataPalpite);
  confere(depois === hojeISO, `${rotulo}: data do palpite não muda`);
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
      confere(nPagina === nRoteiro && nPagina === 34, `${rotulo}: número de slides igual ao do roteiro`, { pagina: nPagina, roteiro: nRoteiro });
      const img = await page.evaluate(() => Array.from(document.images).filter((i) => i.complete && i.naturalWidth === 0).map((i) => i.src));
      confere(img.length === 0, `${rotulo}: todas as imagens carregam`, img);
      const fundo = await page.evaluate(() => new Promise((ok) => { const i = new Image(); i.onload = () => ok(i.naturalWidth); i.onerror = () => ok(0); i.src = '../fotos/c4b7d4ee48.jpg'; }));
      confere(fundo > 0, `${rotulo}: a foto do slide 33 carrega`);
      await percorre(page, rotulo, celular);
      await interacoes(page, rotulo, celular);
      await page.evaluate(() => { const t = document.getElementById('toast'); if (t) t.classList.remove('on'); }); // o aviso de retomada não entra nas capturas
      if (celular) {
        await page.evaluate(() => ZD.vai(2)); await espera(700);
        await page.screenshot({ path: path.join(DEMO, 'aula-celular-palpite.png') });
      } else {
        await page.evaluate(() => { ZD.vai(23); const el = document.querySelector('.s.on [name=pct]'); el.value = '12'; el.dispatchEvent(new Event('input', { bubbles: true })); });
        await espera(700);
        await page.screenshot({ path: path.join(DEMO, 'aula-calculadora.png') });
        await page.evaluate(() => ZD.vai(26, 'tudo')); await espera(900);
        await page.screenshot({ path: path.join(DEMO, 'aula-semaforo.png') });
      }
      await ctx.close();
    }

    // turma de acompanhamento
    {
      const ctx = await novoContexto(browser, { width: 1280, height: 800 });
      const page = await ctx.newPage(); vigia(page, 'turma');
      await page.goto(URL_AULA + '?turma=acompanhamento#32'); await espera(500);
      const t = await page.evaluate(() => ({ passo: document.getElementById('passo3').textContent, href: document.getElementById('abrir-ficha').href }));
      confere(/encontro do Pilar 6/.test(t.passo) && t.href === `${BASE}/trilha1/capex/?turma=acompanhamento`, 'turma de acompanhamento: passo 3 e link trocados', t);
      await ctx.close();
    }

    // modo apresentador: a outra janela recebe as notas do slide atual
    {
      const ctx = await novoContexto(browser, { width: 1280, height: 800 });
      const page = await ctx.newPage(); vigia(page, 'aula com apresentador');
      await page.goto(URL_AULA + '#1'); await espera(500);
      const apr = await ctx.newPage(); vigia(apr, 'janela do apresentador');
      await apr.goto(URL_AULA + '?apresentador'); await espera(1500);
      await page.evaluate(() => ZD.vai(23)); await espera(800);
      const nt = await apr.locator('#nt').innerText();
      const pos = await apr.locator('#pos').innerText();
      confere(/Peça que um aluno diga um percentual/.test(nt) && /Slide 24 de 34/.test(pos), 'modo apresentador mostra o slide e as notas certas', { pos, nt: nt.slice(0, 60) });
      await apr.click('#prox'); await espera(500);
      const i2 = await page.evaluate(() => Array.from(document.querySelectorAll('.s')).findIndex((s) => s.classList.contains('on')));
      confere(i2 === 24, 'botão Avançar do apresentador troca o slide da aula', i2);
      await ctx.close();
    }

    // sem armazenamento (navegação privada que bloqueia): a aula segue funcionando
    {
      const ctx = await novoContexto(browser, { width: 390, height: 844 }, { hasTouch: true, isMobile: true });
      await ctx.addInitScript(() => { const erro = () => { throw new Error('bloqueado'); }; Storage.prototype.getItem = erro; Storage.prototype.setItem = erro; });
      const page = await ctx.newPage(); vigia(page, 'sem armazenamento');
      await page.goto(URL_AULA + '#3'); await espera(600);
      await page.locator('.s.on input.resp').fill('500000'); await espera(150);
      confere(/guardado/i.test(await page.locator('.s.on .fb').innerText()), 'sem armazenamento: a pergunta responde e não quebra');
      await ctx.close();
    }
  } finally {
    await browser.close();
    srv.kill();
  }
  confere(resultado.erros.length === 0, 'zero erros de JS em todas as páginas', resultado.erros.slice(0, 10));
  console.log('Domínios externos bloqueados no teste: ' + (resultado.bloqueados.size ? Array.from(resultado.bloqueados).join(', ') : 'nenhum pedido externo'));
  console.log(`Verificações aprovadas: ${resultado.ok} · reprovadas: ${resultado.falhas.length}`);
  resultado.falhas.forEach((f) => console.log('FALHA · ' + f));
  process.exit(resultado.falhas.length ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });

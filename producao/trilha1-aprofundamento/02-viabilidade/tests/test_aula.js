/* Teste de ponta a ponta da aula interativa do Aprofundamento 6B · Viabilidade (docs/trilha1/apresentacao/pilar6b-aula/).
   Uso: node producao/trilha1-aprofundamento/02-viabilidade/tests/test_aula.js
   Sobe um servidor local (python3 -m http.server servindo docs/), abre a aula no Chromium em
   390x844 (celular) e 1280x800 (computador), percorre os 40 slides e confere: zero erros de JS na aula,
   sem rolagem horizontal, nenhum texto transbordando do slide, número de slides igual ao do roteiro,
   data-bloco na lista do plano, sem sigla interna (ECROI) nem siglas técnicas na tela (NOI, EBITDA, VPL,
   TIR, payback, ROI), sem «Bloco 3» a «Bloco 7», os números do caso da Marina (PLANO, seção 7), a nota
   respeitosa sobre a margem de referência, interações (retomada, previsão que volta, quizzes, cartões,
   simulador das alavancas, resposta do contador, nome, ficha embutida), teclado, toque, notas, modo
   apresentador e salvamento local depois de recarregar, gravando só respostas.d2 e respostas.nome na
   chave da ficha (zion-t1-pilar6b), sem apagar o que a ficha guardou.
   Qualquer domínio externo é bloqueado e anotado. As mensagens da ficha embutida (../../pilar6b/, que está
   sendo construída em paralelo) são anotadas à parte e não contam como erro da aula.
   Salva capturas a 1x em ../demonstracao/aula-*.png. */
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
const URL_AULA = `${BASE}/trilha1/apresentacao/pilar6b-aula/`;
const URL_FICHA = `${BASE}/trilha1/pilar6b/`;
const N_SLIDES = 40;

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
    const daFicha = /\/trilha1\/pilar6b\//.test(String(e.stack || ''));
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
  const est = () => page.evaluate(() => JSON.parse(localStorage.getItem('zion-t1-pilar6b')));
  const fb = () => page.locator('.s.on .fb').innerText();

  // navegação pelo botão Avançar: o slide 11 (Degrau 1) tem 3 itens; o 4º clique troca de slide
  await vai(10);
  for (let k = 0; k < 4; k++) await page.click('#n-prox');
  confere(await atual() === 11, `${rotulo}: botão Avançar revela os itens e troca de slide`);
  await page.click('#n-ant');
  confere(await atual() === 10, `${rotulo}: botão Voltar volta um slide`);

  // slides 4 a 6: retomada (quiz que grava em aulaExtras)
  await vai(3);
  await page.click('.s.on .opc[data-v="a"]');
  confere(/a resposta é outra/i.test(await fb()) && /40%, a margem de referência/.test(await fb()), `${rotulo}: retomada errada mostra a certa`, await fb());
  await page.click('.s.on .opc[data-v="b"]');
  confere(/^isso/i.test(await fb()) && /simplificação, não promessa/.test(await fb()), `${rotulo}: retomada certa confirma`, await fb());
  await vai(4); await page.click('.s.on .opc[data-v="b"]');
  confere(/^isso/i.test(await fb()) && /R\$ 791\.131/.test(await fb()), `${rotulo}: retomada da 6A (cerca de R$ 832 mil)`, await fb());
  await vai(5); await page.click('.s.on .opc[data-v="c"]');
  confere(/a resposta é outra/i.test(await fb()) && /Cerca de R\$ 870 mil/.test(await fb()), `${rotulo}: retomada do limite`, await fb());

  // slide 7: previsão (aulaExtras), que volta no slide 31
  await vai(6);
  await page.click('.s.on .opc[data-v="perto"]');
  confere(/previsão guardada/i.test(await fb()), `${rotulo}: previsão guardada`, await fb());
  await vai(30); await espera(100);
  let eco = await page.locator('#prev-eco').innerText();
  confere(/perto de 40%/.test(eco) && /errada também ensina/.test(eco) && /21,3%/.test(eco), `${rotulo}: a previsão volta no slide do critério`, eco);
  await vai(6); await page.click('.s.on .opc[data-v="abaixo_cai"]');
  await vai(30); await espera(100);
  eco = await page.locator('#prev-eco').innerText();
  confere(/Foi isso/.test(eco), `${rotulo}: previsão certa confirmada`, eco);

  // slide 17: cartões viram no clique
  await vai(16);
  await page.locator('.s.on .pq').nth(2).click();
  confere(await page.locator('.s.on .pq.aberto').count() === 1, `${rotulo}: cartão vira no toque`);
  // slide 21: quiz antes ou depois da reserva
  await vai(20);
  await page.locator('.s.on .op[data-certa]').click();
  confere(await page.locator('.s.on .op.certa').count() === 1 && await page.locator('.s.on .quiz.resp .exp').isVisible(), `${rotulo}: quiz 2 revela a explicação`);
  // slide 35: resposta errada fica marcada e a certa aparece
  await vai(34);
  await page.locator('.s.on .op:not([data-certa])').first().click();
  confere(await page.locator('.s.on .op.errada').count() === 1 && await page.locator('.s.on .op.certa').count() === 1, `${rotulo}: quiz 3 marca a errada e mostra a certa`);

  // slide 33: simulador das alavancas (os números do PLANO 7.10)
  await vai(32);
  const poe = (nome, v) => page.evaluate(({ nome, v }) => { const el = document.querySelector(`.s.on [name="${nome}"]`); el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); }, { nome, v });
  const leSim = () => page.evaluate(() => { const s = document.querySelector('.s.on .sim'); const t = (k) => s.querySelector(`[data-r=${k}]`).textContent; return { noite: t('noite'), sobra: t('sobra'), margem: t('margem'), ano1: t('ano1'), volta: t('volta'), passo: t('passo'), aviso: s.querySelector('[data-aviso]').className, txt: s.querySelector('[data-aviso]').textContent }; });
  let r = await leSim();
  confere(r.noite === 'R$ 404,31' && r.sobra === 'R$ 57.820' && r.margem === '21,3%' && r.ano1 === '−R$ 18.992' && r.volta === '15,0 anos' && r.passo === 'redesenhar' && /\ber\b/.test(r.aviso), `${rotulo}: simulador começa na conta da Marina (15,0 anos, vermelho)`, r);
  await poe('diaria', '695'); r = await leSim();
  confere(r.noite === 'R$ 443,21' && r.sobra === 'R$ 74.219' && r.ano1 === '−R$ 9.983' && r.volta === '11,8 anos' && r.passo === 'ajustar' && /\bat\b/.test(r.aviso) && /Testar/.test(r.txt), `${rotulo}: diária + R$ 50 = 11,8 anos, ajustar, premissa a provar`, r);
  await poe('diaria', '810'); r = await leSim();
  confere(r.volta === '8,0 anos' && r.passo === 'passa' && /\bok\b/.test(r.aviso), `${rotulo}: diária de R$ 810 cabe em 8 anos (verde)`, r);
  await poe('diaria', '645'); await poe('ocup', '43.5'); r = await leSim();
  confere(r.sobra === 'R$ 79.956' && r.volta === '11,0 anos' && r.passo === 'ajustar', `${rotulo}: ocupação + 5 pontos = 11,0 anos`, r);
  await poe('ocup', '38.5'); await poe('fixo', '-10'); r = await leSim();
  confere(r.sobra === 'R$ 69.083' && r.ano1 === '−R$ 7.729' && r.volta === '12,6 anos' && r.passo === 'redesenhar', `${rotulo}: custo fixo − 10% = 12,6 anos`, r);
  await poe('fixo', '0'); await poe('capex', '-10'); r = await leSim();
  confere(r.sobra === 'R$ 57.820' && r.volta === '13,6 anos' && r.passo === 'redesenhar', `${rotulo}: CAPEX − 10% = 13,6 anos`, r);
  await poe('diaria', '695'); r = await leSim();
  confere(/mais de uma alavanca/.test(r.txt), `${rotulo}: duas alavancas de uma vez = aviso "uma por vez"`, r);
  await poe('capex', '0'); await poe('diaria', '545'); await poe('ocup', '28.5'); r = await leSim();
  confere(r.volta === 'não se paga' || /mais de 100/.test(r.volta), `${rotulo}: diária e ocupação baixas = não se paga`, r);
  confere(await page.locator('.s.on .sim.mexeu').count() === 1, `${rotulo}: aparece "Ajustado por você"`);
  await page.click('.s.on .reset'); r = await leSim();
  confere(r.volta === '15,0 anos' && r.sobra === 'R$ 57.820', `${rotulo}: botão volta à conta da Marina`, r);

  // slide 37: critério de conclusão (grava em respostas.d2)
  await vai(36);
  await page.click('.s.on .opc[data-v="nao"]');
  confere(/em branco/.test(await fb()) && /Testar/.test(await fb()), `${rotulo}: "contador" grava com feedback`, await fb());
  const nav = await page.locator('#n-resp').innerText();
  confere(/5 de 5/.test(nav), `${rotulo}: barra mostra 5 de 5 respondidas`, nav);

  // slide 38: o nome (respostas.nome)
  await vai(37);
  await page.locator('#p-nome').fill('Ana Teste');
  await espera(100);
  confere((await est()).respostas.nome === 'Ana Teste', `${rotulo}: nome gravado em respostas.nome`);

  // slide 39: a ficha dentro da aula
  await vai(38); await espera(400);
  const src = await page.evaluate(() => document.getElementById('diag-fr').src);
  confere(src === URL_FICHA, `${rotulo}: a ficha embutida abre ../../pilar6b/`, src);

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
    confere(/abre a linha que a página 6 fechou/.test(notas), `${rotulo}: tecla N mostra as notas do apresentador`);
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
  confere(href === URL_FICHA, `${rotulo}: último slide leva a ../../pilar6b/`, href);
  confere((await page.locator('#n-prox').innerText()).includes('Abrir a ficha'), `${rotulo}: botão final vira "Abrir a ficha"`);
  const txtProx = await page.locator('.s.on').innerText();
  confere(/Meu Dossiê/.test(txtProx) && /páginas 6 e 6A/.test(txtProx) && /não envia nada/.test(txtProx) && /Pilar 7/.test(txtProx) && /Material educativo/.test(txtProx), `${rotulo}: slide Próximo lembra a pasta Meu Dossiê, o Pilar 7 e o aviso educativo`);

  // persistência: recarrega e confere
  await vai(36);
  await espera(200);
  const antes = await est();
  confere(antes.respostas.d2 === 'nao' && antes.respostas.nome === 'Ana Teste' && antes.aulaExtras.slide === 36 && antes.aulaExtras.r_margem === 'b' && antes.aulaExtras.r_invest === 'b' && antes.aulaExtras.r_limite === 'c' && antes.aulaExtras.previsao === 'abaixo_cai', `${rotulo}: estado gravado na chave zion-t1-pilar6b`, antes);
  await page.reload();
  await espera(800);
  confere(await atual() === 36, `${rotulo}: depois de recarregar, volta ao mesmo slide`);
  confere(await page.locator('.s.on .opc[data-v="nao"]').getAttribute('aria-pressed') === 'true', `${rotulo}: escolha continua marcada depois de recarregar`);
  confere(/5 de 5/.test(await page.locator('#n-resp').innerText()), `${rotulo}: contagem de respondidas persiste`);
  await page.goto(URL_AULA); // sem número no endereço: usa o slide salvo
  await espera(800);
  confere(await atual() === 36, `${rotulo}: abrindo sem # no endereço, volta ao slide salvo`);
  await vai(3); await espera(200);
  confere(await page.locator('.s.on .opc[data-v="b"]').getAttribute('aria-pressed') === 'true', `${rotulo}: retomada continua marcada depois de recarregar`);
  await vai(37); await espera(200);
  confere(await page.locator('#p-nome').inputValue() === 'Ana Teste', `${rotulo}: nome continua no campo depois de recarregar`);
}

/* A estrutura da aula: título, data-bloco, números do caso e textos proibidos. */
async function estrutura(page, rotulo) {
  const e = await page.evaluate(() => {
    const semNotas = document.querySelector('.zd-stage').cloneNode(true);
    semNotas.querySelectorAll('aside').forEach((a) => a.remove());
    return {
      titulo: document.title, deck: document.body.dataset.titulo,
      blocos: Array.from(document.querySelectorAll('.s')).map((s) => s.dataset.bloco || ''),
      html: document.documentElement.outerHTML,
      tela: semNotas.textContent,
    };
  });
  confere(e.titulo === 'Aprofundamento 6B · Viabilidade' && e.deck === 'Aprofundamento 6B · Viabilidade', `${rotulo}: título «Aprofundamento 6B · Viabilidade»`, [e.titulo, e.deck]);
  confere(!/ECROI/i.test(e.html), `${rotulo}: nenhuma sigla ECROI na página (tela, notas e atributos)`);
  confere(!/\b(NOI|EBITDA|VPL|TIR|ROI)\b|payback/i.test(e.html.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<style[\s\S]*?<\/style>/g, '')) , `${rotulo}: sem NOI, EBITDA, VPL, TIR, payback e ROI`);
  confere(!e.blocos.some((b) => /Bloco [3-9]/.test(b)) && !/Bloco [3-9]/.test(e.tela), `${rotulo}: sem «Bloco 3» em diante`);
  // ordem de primeira aparição (o «Quiz relâmpago» aparece no fim do Bloco 1, no meio e no fim do Bloco 2)
  const esperados = ['Abertura', 'Como funciona esta aula', 'Retomada · Pilar 6 e 6A', 'Bloco 1 · Os seis degraus da conta', 'Quiz relâmpago', 'Bloco 2 · A conta da Marina', 'Resumo', 'A sua página 6B', 'Próximo'];
  const unicos = Array.from(new Set(e.blocos));
  confere(JSON.stringify(unicos) === JSON.stringify(esperados), `${rotulo}: data-bloco na ordem do plano`, unicos);
  confere(!/Helena|Ribeir|Rodrigo/.test(e.html), `${rotulo}: sem Helena, Chalés do Ribeirão nem Rodrigo e Priscila`);
  confere(!/—/.test(e.tela), `${rotulo}: sem travessão no texto da tela`);
  confere(!/inflad|estava errad|otimista demais/i.test(e.html), `${rotulo}: sem desmerecer a margem do Pilar 6`);
  confere(/Método Zion · Etapa 4 · Fechar a conta/.test(e.html) && /O 6B em cinco frases/.test(e.html) && /Retomada · Pilar 6 e 6A/.test(e.html), `${rotulo}: selo da Etapa 4, «Retomada · Pilar 6 e 6A» e «O 6B em cinco frases»`);
  confere(Array.from({ length: 6 }, (_, k) => `Degrau ${k + 1} de 6`).every((t) => e.html.includes(t)), `${rotulo}: os seis degraus numerados «Degrau N de 6»`);
  confere(/Exemplo ilustrativo · dados fictícios\. Não são preços de referência\./.test(e.tela) && /referência orientativa da página 6, não confirmada; a Zion também vende esse tipo de estrutura/.test(e.tela) && /resposta fictícia do contador dela/.test(e.tela) && /Cenários, não promessas/.test(e.tela), `${rotulo}: rótulos fixos (exemplo ilustrativo, referência da página 6, contador fictício, cenários)`);
  confere(/simplificação, não promessa/.test(e.tela) && /agora a resposta vem da lista/.test(e.tela), `${rotulo}: nota respeitosa sobre a margem de referência da página 6`);
  const numeros = ['271.915,88', '108.766,35', '791.131', '831.918,38', '222.427,19', '178.604,46', '112.627,20', '16.627,20', '65.977,26', '8.157,48', '57.819,79', '21,3%', '25,4%', '13,1 pontos', '507,85', '468,71', '22.356,81', '18.992,04', '53.524,02', '50.513,61', '844.655,02', '31.167,21', '3,9%', '101.469,91', '15,0 anos', '14,6 anos', '25,4 anos', '462.558,31', '6.806,35', '106.638,40', '8,3 anos', '7,4%', '28/12/2026'];
  const faltam = numeros.filter((n) => !e.tela.includes(n));
  confere(faltam.length === 0, `${rotulo}: os números do caso da Marina (PLANO, seção 7) aparecem na tela`, faltam);
  confere(/Redesenhar/.test(e.tela) && /Testar/.test(e.tela), `${rotulo}: veredito Redesenhar e o ajustado em Testar`);
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
      if (celular) {
        await page.evaluate(() => ZD.vai(0, 'tudo')); await espera(700);
        await page.screenshot({ path: path.join(DEMO, 'aula-celular-capa.png') });
      }
      await percorre(page, rotulo, celular);
      await interacoes(page, rotulo, celular);
      await page.evaluate(() => { const t = document.getElementById('toast'); if (t) t.classList.remove('on'); }); // o aviso de retomada não entra nas capturas
      if (celular) {
        await page.evaluate(() => ZD.vai(23, 'tudo')); await espera(700);
        await page.screenshot({ path: path.join(DEMO, 'aula-celular-conta.png') });
        await page.evaluate(() => ZD.vai(6)); await espera(700);
        await page.screenshot({ path: path.join(DEMO, 'aula-celular-previsao.png') });
      } else {
        await page.evaluate(() => ZD.vai(24, 'tudo')); await espera(900);
        await page.screenshot({ path: path.join(DEMO, 'aula-diferenca-pagina6.png') });
        await page.evaluate(() => ZD.vai(26, 'tudo')); await espera(900);
        await page.screenshot({ path: path.join(DEMO, 'aula-primeiro-ano.png') });
        await page.evaluate(() => ZD.vai(29, 'tudo')); await espera(900);
        await page.screenshot({ path: path.join(DEMO, 'aula-cinco-passos.png') });
        await page.evaluate(() => { ZD.vai(32); const el = document.querySelector('.s.on [name=diaria]'); el.value = '695'; el.dispatchEvent(new Event('input', { bubbles: true })); });
        await espera(700);
        await page.screenshot({ path: path.join(DEMO, 'aula-alavancas.png') });
      }
      await ctx.close();
    }

    // a ficha já tem dados neste aparelho: a aula não apaga nada e grava só respostas.d2 e respostas.nome
    {
      const ctx = await novoContexto(browser, { width: 390, height: 844 }, { hasTouch: true, isMobile: true });
      await ctx.addInitScript(() => {
        if (sessionStorage.getItem('semeado')) return; sessionStorage.setItem('semeado', '1');
        localStorage.setItem('zion-t1-pilar6a', JSON.stringify({ atualizado: '2026-11-27T10:00:00Z', respostas: { nome: 'Marina Exemplo' } }));
        localStorage.setItem('zion-t1-pilar6b', JSON.stringify({ versao: 1, respostas: { projeto: 'Cabanas da Serra', d1: 'em_parte' }, resumo: { dados: { sobra: [1, 2, 3] } } }));
      });
      const page = await ctx.newPage(); vigia(page, 'ficha semeada');
      await page.goto(URL_AULA + '#38'); await espera(700);
      confere(await page.locator('#p-nome').inputValue() === 'Marina Exemplo', 'ficha semeada: o nome vem de outra página do Dossiê (6A)');
      await page.evaluate(() => ZD.vai(3)); await page.click('.s.on .opc[data-v="b"]');
      await page.evaluate(() => ZD.vai(6)); await page.click('.s.on .opc[data-v="abaixo_pe"]');
      await page.evaluate(() => ZD.vai(36)); await page.click('.s.on .opc[data-v="sim"]');
      await espera(150);
      const d = await page.evaluate(() => JSON.parse(localStorage.getItem('zion-t1-pilar6b')));
      const chaves = Object.keys(d.respostas).sort().join(',');
      confere(chaves === 'd1,d2,nome,projeto' && d.respostas.d2 === 'sim' && d.respostas.nome === 'Marina Exemplo', 'a aula grava só respostas.d2 e respostas.nome', d.respostas);
      confere(d.respostas.projeto === 'Cabanas da Serra' && d.respostas.d1 === 'em_parte' && d.versao === 1 && d.resumo && d.resumo.dados.sobra.length === 3, 'a aula não apaga o que a ficha guardou', d);
      confere(d.aulaExtras.r_margem === 'b' && d.aulaExtras.previsao === 'abaixo_pe' && d.aulaExtras.contador === 'sim', 'retomada e previsão ficam em aulaExtras', d.aulaExtras);
      await ctx.close();
    }

    // JSON quebrado na chave: a aula abre e responde
    {
      const ctx = await novoContexto(browser, { width: 1280, height: 800 });
      await ctx.addInitScript(() => { if (!sessionStorage.getItem('q')) { sessionStorage.setItem('q', '1'); localStorage.setItem('zion-t1-pilar6b', '{quebrado'); } });
      const page = await ctx.newPage(); vigia(page, 'JSON quebrado');
      await page.goto(URL_AULA + '#4'); await espera(600);
      await page.click('.s.on .opc[data-v="b"]');
      confere(/^isso/i.test(await page.locator('.s.on .fb').innerText()), 'JSON quebrado: a pergunta responde e não quebra');
      await ctx.close();
    }

    // turma de acompanhamento
    {
      const ctx = await novoContexto(browser, { width: 1280, height: 800 });
      const page = await ctx.newPage(); vigia(page, 'turma');
      await page.goto(URL_AULA + '?turma=acompanhamento#40'); await espera(500);
      const t = await page.evaluate(() => ({ passo: document.getElementById('passo2').textContent, href: document.getElementById('abrir-ficha').href }));
      confere(/páginas 6A e 6B ao encontro do Pilar 6/.test(t.passo) && t.href === `${URL_FICHA}?turma=acompanhamento`, 'turma de acompanhamento: passo 2 e link trocados', t);
      await ctx.close();
    }

    // modo apresentador: a outra janela recebe as notas do slide atual
    {
      const ctx = await novoContexto(browser, { width: 1280, height: 800 });
      const page = await ctx.newPage(); vigia(page, 'aula com apresentador');
      await page.goto(URL_AULA + '#1'); await espera(500);
      const apr = await ctx.newPage(); vigia(apr, 'janela do apresentador');
      await apr.goto(URL_AULA + '?apresentador'); await espera(1500);
      await page.evaluate(() => ZD.vai(32)); await espera(800);
      const nt = await apr.locator('#nt').innerText();
      const pos = await apr.locator('#pos').innerText();
      confere(/Peça que alguém escolha uma alavanca/.test(nt) && /Slide 33 de 40/.test(pos), 'modo apresentador mostra o slide e as notas certas', { pos, nt: nt.slice(0, 60) });
      await apr.click('#prox'); await espera(500);
      const i2 = await page.evaluate(() => Array.from(document.querySelectorAll('.s')).findIndex((s) => s.classList.contains('on')));
      confere(i2 === 33, 'botão Avançar do apresentador troca o slide da aula', i2);
      await ctx.close();
    }

    // sem armazenamento (navegação privada que bloqueia): a aula segue funcionando
    {
      const ctx = await novoContexto(browser, { width: 390, height: 844 }, { hasTouch: true, isMobile: true });
      await ctx.addInitScript(() => { const erro = () => { throw new Error('bloqueado'); }; Storage.prototype.getItem = erro; Storage.prototype.setItem = erro; });
      const page = await ctx.newPage(); vigia(page, 'sem armazenamento');
      await page.goto(URL_AULA + '#37'); await espera(600);
      await page.click('.s.on .opc[data-v="nao"]'); await espera(150);
      confere(/em branco/.test(await page.locator('.s.on .fb').innerText()), 'sem armazenamento: a pergunta responde e não quebra');
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

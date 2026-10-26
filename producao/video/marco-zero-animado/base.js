// Base comum dos vídeos animados da Marco Zero: fontes, selo, barra de progresso, relógio de pausa e o
// helper W(fala, 'palavras') que devolve o instante em que aquelas palavras começam na narração.
// Cada cena (V01.html...) monta a sua linha do tempo GSAP em cena(tl) e a base cuida do resto.
// gravar.py chama window.seek(t) quadro a quadro.

const plano = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9 ]/g, ' ')
  .split(/\s+/).filter(Boolean);

let DADOS;
function W(nf, frase, depois = 0) {
  const f = DADOS.falas[nf - 1], alvo = frase.split(/\s+/).map(w => plano(w).join('')).filter(Boolean);
  const pal = f.palavras.map(p => plano(p.p).join(''));
  for (let i = 0; i < pal.length; i++) {
    if (f.palavras[i].a < depois) continue;
    if (alvo.every((w, k) => pal[i + k] === w)) return f.palavras[i].a;
  }
  console.error(`palavra não encontrada na fala ${nf}: "${frase}"`);
  return f.a;
}
const FALA = n => DADOS.falas[n - 1];
const E = 'power2.out';

// texto com a parte de destaque entre *asteriscos* vira itálico
const rico = t => t.replace(/\*(.+?)\*/g, '<em>$1</em>');

function el(html, css = {}, pai = document.querySelector('#cena')) {
  const d = document.createElement('div');
  d.innerHTML = html.trim();
  const n = d.firstElementChild;
  Object.assign(n.style, css);
  pai.appendChild(n);
  return n;
}

// foto em tela cheia com movimento lento; o degradê verde fica por baixo do texto
function foto(arq, { lado = 'esq', zoom = [1, 1.08], x = [0, 0], pos = '50% 50%' } = {}) {
  const f = el(`<div class="foto"><img src="fotos/${arq}.jpg" alt=""><div class="degrade ${lado}"></div></div>`);
  Object.assign(f.querySelector('img').style, { transform: `scale(${zoom[0]})`, objectPosition: pos, transformOrigin: pos });
  f.zoom = zoom; f.x = x;
  return f;
}
function mover(tl, f, a, b) {
  tl.fromTo(f.querySelector('img'), { scale: f.zoom[0], xPercent: f.x[0] },
            { scale: f.zoom[1], xPercent: f.x[1], duration: b - a, ease: 'none' }, a);
}

function pausa(tl, a, dur) {
  // relógio circular dourado se fechando e "Pause e anote" no canto inferior esquerdo
  const r = el(`<div class="relogio"><svg width="120" height="120" viewBox="0 0 120 120">
      <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(245,241,232,.18)" stroke-width="8"/>
      <circle class="anel" cx="60" cy="60" r="50" fill="none" stroke="#E0BE5E" stroke-width="8" stroke-linecap="round"
              transform="rotate(-90 60 60)" stroke-dasharray="314.16" stroke-dashoffset="0"/></svg>
      <span>Pause e anote</span></div>`);
  tl.fromTo(r, { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.5, ease: E }, a);
  tl.fromTo(r.querySelector('.anel'), { attr: { 'stroke-dashoffset': 0 } },
            { attr: { 'stroke-dashoffset': 314.16 }, duration: dur - 0.4, ease: 'none' }, a + 0.2);
  tl.to(r, { autoAlpha: 0, duration: 0.4 }, a + dur - 0.4);
}

window.seek = t => { window.TL.seek(t, true); };

async function iniciar(video, cena) {
  DADOS = await (await fetch(`audio/${video}.json?${Date.now()}`)).json();
  const tl = gsap.timeline({ paused: true });
  window.TL = tl;
  document.querySelector('#selo').textContent = `Marco Zero · Bloco ${DADOS.bloco}`;
  tl.set('#selo', { autoAlpha: 1 }, 0).to('#selo', { autoAlpha: 0, duration: 0.5 }, 3.5);
  tl.fromTo('#barra', { scaleX: 0 }, { scaleX: 1, duration: DADOS.total, ease: 'none' }, 0);
  cena(tl);
  tl.set({}, {}, DADOS.total);
  const imgs = [...document.images];
  await Promise.all(imgs.map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; })));
  await document.fonts.ready;
  window.DURACAO = DADOS.total;
  window.pronto = true;
}

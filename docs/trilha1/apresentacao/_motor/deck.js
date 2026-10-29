/* Zion · motor das apresentações ao vivo (29/10/2026)
   Teclas: → espaço clique = avança · ← volta · N notas · P apresentador · F tela cheia
   O visão geral · L laser · D caneta · C limpa caneta · B tela preta · R volta o simulador · ? ajuda */
(function(){
'use strict';
const ZD = window.ZD = window.ZD || {};
ZD.sims = ZD.sims || {};
const Q = new URLSearchParams(location.search);
const VISTA = Q.has('vista');            // dentro do modo apresentador (miniatura)
const APR = Q.has('apresentador');       // janela do apresentador
const deckId = (document.body.dataset.deck || location.pathname).replace(/[^a-z0-9]/gi,'');
let ch = null; try { ch = new BroadcastChannel('zd-' + deckId); } catch(e) {}

/* ---------- formatos ---------- */
const nf0 = new Intl.NumberFormat('pt-BR',{maximumFractionDigits:0});
const nf1 = new Intl.NumberFormat('pt-BR',{minimumFractionDigits:1,maximumFractionDigits:1});
const nf2 = new Intl.NumberFormat('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2});
ZD.fmt = function(v, f){
  if (v === null || v === undefined) return '';
  if (typeof v === 'number' && !isFinite(v)) return 'sem volta';
  if (typeof v === 'string') return v;
  switch(f){
    case 'brl': return 'R$ ' + nf0.format(Math.round(v));
    case 'mil': return 'R$ ' + nf0.format(Math.round(v/1000)) + ' mil';
    case 'pct': return nf1.format(v) + '%';
    case 'pct0': return nf0.format(v) + '%';
    case 'anos': return nf2.format(v) + ' anos';
    case 'm2': return nf0.format(v) + ' m²';
    case 'dec1': return nf1.format(v);
    case 'dec2': return nf2.format(v);
    case 'x': return nf0.format(v) + '×';
    default: return nf0.format(v);
  }
};

if (APR) { montaApresentador(); return; }

/* ---------- palco ---------- */
const slides = Array.from(document.querySelectorAll('.s'));
const stage = document.querySelector('.zd-stage');
function escala(){
  const k = Math.min(innerWidth/1920, innerHeight/1080);
  stage.style.transform = 'scale(' + k + ')';
}
addEventListener('resize', escala); escala();

/* fundo de foto */
slides.forEach(s => {
  if (s.dataset.bg) {
    const d = document.createElement('div'); d.className = 'bg';
    d.style.backgroundImage = 'url(' + s.dataset.bg + ')';
    if (s.dataset.pos) d.style.backgroundPosition = s.dataset.pos;
    s.prepend(d);
  }
  if (!s.querySelector('.topo') && !s.classList.contains('sem-topo')) {
    const t = document.createElement('div'); t.className = 'topo';
    const esc = s.classList.contains('esc') || s.classList.contains('foto');
    t.innerHTML = '<span>' + (s.dataset.bloco || document.body.dataset.titulo || '') + '</span><img alt="Zion" src="' + (esc ? ZD.logoClaro : ZD.logoEscuro) + '">';
    s.prepend(t);
  }
  if (s.classList.contains('bloco') && s.dataset.num) {
    const n = document.createElement('div'); n.className = 'num-bg'; n.textContent = s.dataset.num; s.prepend(n);
  }
});

/* ---------- passos (o que aparece a cada clique) ---------- */
function passosDe(s){
  const out = [];
  s.querySelectorAll('.f, .pq.passo, .fases.passo .bt, .quiz.passo, [data-passo]').forEach(el => {
    if (el.classList.contains('f')) out.push({el, faz(){el.classList.add('vis'); foca(el);}, desfaz(){el.classList.remove('vis');}});
    else if (el.classList.contains('pq')) out.push({el, faz(){el.classList.add('aberto');}, desfaz(){el.classList.remove('aberto');}});
    else if (el.classList.contains('bt')) out.push({el, faz(){abreFase(el);}, desfaz(){voltaFase(el);}});
    else if (el.classList.contains('quiz')) out.push({el, faz(){respondeQuiz(el);}, desfaz(){limpaQuiz(el);}});
  });
  return out;
}
function foca(el){ if (el.dataset.foco !== undefined){ el.classList.remove('foco'); void el.offsetWidth; el.classList.add('foco'); } }
const P = slides.map(passosDe);

let i = 0, k = 0; // slide atual e passos já feitos nele
function vai(n, passos){
  n = Math.max(0, Math.min(slides.length-1, n));
  slides.forEach((s,j)=> s.classList.toggle('on', j===n));
  if (n !== i) salvaTinta(i);
  i = n;
  P[i].slice().reverse().forEach(p=>p.desfaz());
  k = 0;
  const alvo = passos === 'tudo' ? P[i].length : (passos||0);
  while (k < alvo) { P[i][k].faz(); k++; }
  atualiza();
  carregaTinta(i);
}
function proximo(){ if (k < P[i].length){ P[i][k].faz(); k++; atualiza(); } else if (i < slides.length-1) vai(i+1); }
function anterior(){ if (k > 0){ k--; P[i][k].desfaz(); atualiza(); } else if (i > 0) vai(i-1,'tudo'); }
ZD.vai = vai; ZD.proximo = proximo; ZD.anterior = anterior;

/* ---------- interface ---------- */
const bar = document.createElement('div'); bar.className = 'zd-bar';
const ui = document.createElement('div'); ui.className = 'zd-ui';
ui.innerHTML = '<button data-a="ant" title="Voltar (←)">‹</button><span class="cnt"></span><button data-a="prox" title="Avançar (→)">›</button>'+
 '<button data-a="notas" title="Notas do apresentador (N)">N</button><button data-a="apr" title="Modo apresentador (P)">P</button>'+
 '<button data-a="geral" title="Visão geral (O)">▦</button><button data-a="laser" title="Laser (L)">●</button><button data-a="caneta" title="Caneta (D)">✎</button>'+
 '<button data-a="cheia" title="Tela cheia (F)">⛶</button><button data-a="ajuda" title="Atalhos (?)">?</button>';
const notas = document.createElement('div'); notas.className = 'zd-notas';
const geral = document.createElement('div'); geral.className = 'zd-geral';
const ajuda = document.createElement('div'); ajuda.className = 'zd-ajuda';
ajuda.innerHTML = '<b style="color:#C9A84C">Atalhos</b><br><kbd>→</kbd>avança (clique, espaço ou passador)<br><kbd>←</kbd>volta<br><kbd>N</kbd>notas do apresentador<br><kbd>P</kbd>modo apresentador (outra janela)<br><kbd>F</kbd>tela cheia<br><kbd>O</kbd>visão geral dos slides<br><kbd>L</kbd>laser<br><kbd>D</kbd>caneta · <kbd>C</kbd>limpa<br><kbd>B</kbd>tela preta<br><kbd>R</kbd>volta o simulador ao exemplo<br><kbd>Home</kbd>primeiro · <kbd>End</kbd>último<br>Digite o número e <kbd>Enter</kbd> para ir ao slide';
const laser = document.createElement('div'); laser.className = 'zd-laser';
if (!VISTA) document.body.append(bar, ui, notas, geral, ajuda, laser);

function atualiza(){
  bar.style.width = ((i+1)/slides.length*100) + '%';
  ui.querySelector('.cnt').textContent = (i+1) + ' / ' + slides.length;
  const a = slides[i].querySelector('aside');
  notas.innerHTML = '<b>' + (i+1) + ' · ' + (slides[i].dataset.bloco || '') + (P[i].length ? ' · clique ' + k + ' de ' + P[i].length : '') + '</b>' + (a ? a.innerHTML : '<i>Sem notas.</i>');
  if (!VISTA) history.replaceState(null,'','#' + (i+1));
  if (ch && !VISTA) ch.postMessage({t:'estado', i, k, total:slides.length, passos:P[i].length, notas:a?a.innerHTML:'', prox: slides[i+1] ? (slides[i+1].querySelector('aside')||{}).innerHTML||'' : ''});
  geral.querySelectorAll('.mini').forEach((m,j)=>m.classList.toggle('at', j===i));
}
geral.innerHTML = slides.map((s,j)=>{
  const t = (s.querySelector('h1,h2,h3,.q,.citacao')||{}).textContent || s.dataset.titulo || ('Slide ' + (j+1));
  return '<div class="mini" data-i="'+j+'"><small>'+(j+1)+' · '+(s.dataset.bloco||'')+'</small>'+t.trim().slice(0,110)+'</div>';
}).join('');
geral.addEventListener('click', e=>{ const m = e.target.closest('.mini'); if (m){ vai(+m.dataset.i); geral.classList.remove('on'); }});

function cheia(){ if (!document.fullscreenElement) document.documentElement.requestFullscreen && document.documentElement.requestFullscreen().catch(()=>{}); else document.exitFullscreen(); }
function abreApr(){ const u = location.pathname + '?apresentador#' + (i+1); window.open(u, 'zd-apr-' + deckId, 'width=1300,height=800'); }
let laserOn = false, pretaOn = false;
function toggleLaser(){ laserOn = !laserOn; laser.style.display = laserOn ? 'block':'none'; document.body.style.cursor = laserOn ? 'none':''; ui.querySelector('[data-a=laser]').classList.toggle('on', laserOn); }
addEventListener('mousemove', e=>{ if (laserOn){ laser.style.left = e.clientX+'px'; laser.style.top = e.clientY+'px'; } ui.classList.add('mostra'); clearTimeout(ui._t); ui._t = setTimeout(()=>ui.classList.remove('mostra'), 1800); });
const preta = document.createElement('div'); preta.style.cssText = 'position:fixed;inset:0;background:#000;z-index:35;display:none';
document.body.append(preta);
function togglePreta(){ pretaOn = !pretaOn; preta.style.display = pretaOn ? 'block':'none'; }

ui.addEventListener('click', e=>{
  const b = e.target.closest('button'); if (!b) return; e.stopPropagation();
  ({ant:anterior, prox:proximo, notas:()=>notas.classList.toggle('on'), apr:abreApr, geral:()=>geral.classList.toggle('on'),
    laser:toggleLaser, caneta:toggleCaneta, cheia, ajuda:()=>ajuda.classList.toggle('on')})[b.dataset.a]();
});

/* ---------- teclado, clique e toque ---------- */
let digitado = '';
function interativo(t){ return t.closest('button, input, select, textarea, a, label, .pq, .op, .bt, .sim, .zd-ui, .zd-notas, .zd-geral, .zd-tinta.ativa, [data-sem-clique]'); }
function tecla(e){
  if (e.target.matches && e.target.matches('input[type=text], input[type=number], textarea')) return;
  const key = e.key;
  if (/^[0-9]$/.test(key)) { digitado += key; return; }
  if (key === 'Enter' && digitado) { vai(+digitado-1); digitado=''; return; }
  digitado = '';
  if (e.target.matches && e.target.matches('input[type=range]') && (key==='ArrowLeft'||key==='ArrowRight')) return;
  switch(key){
    case 'ArrowRight': case ' ': case 'PageDown': case 'ArrowDown': e.preventDefault(); proximo(); break;
    case 'ArrowLeft': case 'PageUp': case 'ArrowUp': e.preventDefault(); anterior(); break;
    case 'Home': vai(0); break; case 'End': vai(slides.length-1); break;
    case 'n': case 'N': notas.classList.toggle('on'); break;
    case 'p': case 'P': abreApr(); break;
    case 'f': case 'F': cheia(); break;
    case 'o': case 'O': case 'Escape': geral.classList.toggle('on', key!=='Escape' && !geral.classList.contains('on')); ajuda.classList.remove('on'); break;
    case 'l': case 'L': toggleLaser(); break;
    case 'd': case 'D': toggleCaneta(); break;
    case 'c': case 'C': limpaTinta(); break;
    case 'b': case 'B': case '.': togglePreta(); break;
    case 'r': case 'R': slides[i].querySelectorAll('.sim').forEach(s=>s._reset && s._reset()); break;
    case '?': ajuda.classList.toggle('on'); break;
  }
}
if (!VISTA) {
  addEventListener('keydown', tecla);
  stage.addEventListener('click', e=>{ if (canetaOn || interativo(e.target)) return; proximo(); });
  let tx=null, ty=null;
  addEventListener('touchstart', e=>{ tx=e.touches[0].clientX; ty=e.touches[0].clientY; }, {passive:true});
  addEventListener('touchend', e=>{ if (tx===null) return; const dx=e.changedTouches[0].clientX-tx, dy=e.changedTouches[0].clientY-ty; if (Math.abs(dx)>60 && Math.abs(dx)>Math.abs(dy)) (dx<0?proximo:anterior)(); tx=null; }, {passive:true});
  if (ch) ch.onmessage = m => { const d = m.data||{}; if (d.t==='cmd'){ if (d.c==='prox') proximo(); else if (d.c==='ant') anterior(); else if (d.c==='ir') vai(d.i); else if (d.c==='pede') atualiza(); } };
}

/* ---------- POR QUÊ (cartões que viram) ---------- */
document.querySelectorAll('.pq').forEach(c=>{
  c.addEventListener('click', e=>{ e.stopPropagation(); c.classList.toggle('aberto'); });
});

/* ---------- FASES ---------- */
document.querySelectorAll('.fases').forEach(f=>{
  const bts = Array.from(f.querySelectorAll('.bt'));
  const painel = f.querySelector('.painel');
  const vazio = painel.innerHTML;
  f._mostra = bt => {
    bts.forEach(b=>{ b.classList.toggle('on', b===bt); });
    if (!bt) { painel.innerHTML = vazio; return; }
    const fx = bt.querySelector('.fx');
    painel.innerHTML = fx ? fx.innerHTML : '';
    painel.animate([{opacity:0},{opacity:1}],{duration:350});
  };
  bts.forEach((b,j)=>b.addEventListener('click', e=>{ e.stopPropagation(); bts.forEach((x,m)=>x.classList.toggle('feito', m<j)); f._mostra(b); }));
});
function abreFase(bt){ const f = bt.closest('.fases'); const bts = Array.from(f.querySelectorAll('.bt')); const j = bts.indexOf(bt); bts.forEach((x,m)=>x.classList.toggle('feito', m<j)); f._mostra(bt); }
function voltaFase(bt){ const f = bt.closest('.fases'); const bts = Array.from(f.querySelectorAll('.bt')); const j = bts.indexOf(bt); bts.forEach((x,m)=>x.classList.toggle('feito', m<j-1)); f._mostra(bts[j-1]||null); }

/* ---------- QUIZ ---------- */
document.querySelectorAll('.quiz').forEach(q=>{
  const L = 'ABCDEFG';
  q.querySelectorAll('.op').forEach((o,j)=>{
    if (!o.querySelector('.l')) o.insertAdjacentHTML('afterbegin','<span class="l">'+L[j]+'</span>');
    o.addEventListener('click', e=>{ e.stopPropagation(); if (o.dataset.certa===undefined) o.classList.add('errada'); respondeQuiz(q); });
  });
});
function respondeQuiz(q){ q.classList.add('resp'); q.querySelectorAll('.op').forEach(o=>{ if (o.dataset.certa!==undefined) o.classList.add('certa'); }); }
function limpaQuiz(q){ q.classList.remove('resp'); q.querySelectorAll('.op').forEach(o=>o.classList.remove('certa','errada')); }

/* ---------- SIMULADORES (equalizar) ---------- */
const estadoSim = {}, padraoSim = {};
document.querySelectorAll('.sim').forEach(sim=>{
  const nome = sim.dataset.sim; padraoSim[nome] = padraoSim[nome] || {};
  sim.querySelectorAll('input[type=range], input[type=number], select').forEach(n=>{ if (!(n.name in padraoSim[nome])) padraoSim[nome][n.name] = n.value; });
});
Object.keys(padraoSim).forEach(n=> estadoSim[n] = Object.assign({}, padraoSim[n]));
function recalc(nome){ document.querySelectorAll('.sim[data-sim="'+nome+'"]').forEach(s=>s._calc()); }
ZD.estado = estadoSim;
document.querySelectorAll('.sim').forEach(sim=>{
  const nome = sim.dataset.sim;
  const ins = Array.from(sim.querySelectorAll('input[type=range], input[type=number], select'));
  function calcula(){
    const fn = ZD.sims[nome];
    const v = {}; Object.keys(estadoSim[nome]).forEach(key=> v[key] = isNaN(+estadoSim[nome][key]) ? estadoSim[nome][key] : +estadoSim[nome][key]);
    ins.forEach(n=>{ if (n.value != estadoSim[nome][n.name]) n.value = estadoSim[nome][n.name]; });
    sim.querySelectorAll('output[data-for]').forEach(o=> o.textContent = ZD.fmt(+estadoSim[nome][o.dataset.for], o.dataset.fmt));
    const r = fn ? fn(v) : {};
    sim.querySelectorAll('[data-r]').forEach(el=> el.textContent = ZD.fmt(r[el.dataset.r], el.dataset.fmt));
    sim.querySelectorAll('[data-bar]').forEach(el=> el.style.width = Math.max(0, Math.min(100, r[el.dataset.bar]||0)) + '%');
    sim.querySelectorAll('[data-ponteiro]').forEach(el=> el.style.left = Math.max(0, Math.min(100, r[el.dataset.ponteiro]||0)) + '%');
    sim.querySelectorAll('[data-aviso]').forEach(av=>{ const a = r[av.dataset.aviso || '_aviso']; if (a){ av.className = 'aviso ' + (a[0]||''); av.innerHTML = a[1]; } });
    if (ZD.desenha && ZD.desenha[nome]) { try { ZD.desenha[nome](sim, r, v); } catch(e){} }
    const mexeu = ins.map(n=>n.name).some(key=> String(estadoSim[nome][key]) !== String(padraoSim[nome][key]));
    sim.classList.toggle('mexeu', mexeu);
  }
  ins.forEach(n=> n.addEventListener('input', ()=>{ estadoSim[nome][n.name] = n.value; recalc(nome); }));
  sim._calc = calcula;
  sim._reset = ()=>{ Object.assign(estadoSim[nome], padraoSim[nome]); recalc(nome); };
  sim.querySelectorAll('.reset').forEach(rb=> rb.addEventListener('click', e=>{ e.stopPropagation(); sim._reset(); }));
  sim.addEventListener('click', e=> e.stopPropagation());
});
document.querySelectorAll('.sim').forEach(s=>s._calc());

/* ---------- CRONÔMETRO ---------- */
document.querySelectorAll('.crono').forEach(c=>{
  const min = +(c.dataset.min||3); let resta = min*60, t = null;
  const out = c.querySelector('.tempo'); const bt = c.querySelector('button.ir'); const zr = c.querySelector('button.sec');
  const mostra = ()=>{ out.textContent = Math.floor(resta/60) + ':' + String(resta%60).padStart(2,'0'); c.classList.toggle('fim', resta<=0); };
  bt.addEventListener('click', e=>{ e.stopPropagation(); if (t){ clearInterval(t); t=null; bt.textContent='Continuar'; return; } bt.textContent='Pausar'; t=setInterval(()=>{ if (resta>0){ resta--; mostra(); } else { clearInterval(t); t=null; bt.textContent='Começar'; } },1000); });
  zr && zr.addEventListener('click', e=>{ e.stopPropagation(); clearInterval(t); t=null; resta=min*60; bt.textContent='Começar'; mostra(); });
  mostra();
});

/* ---------- QR ---------- */
document.querySelectorAll('.qr[data-url]').forEach(q=>{
  try { if (window.QRCode) new QRCode(q, {text:q.dataset.url, width:296, height:296, colorDark:'#16261C', colorLight:'#ffffff'}); } catch(e){}
});

/* ---------- CANETA ---------- */
const tinta = document.createElement('canvas'); tinta.className = 'zd-tinta'; tinta.width = 1920; tinta.height = 1080;
stage.append(tinta);
const cx = tinta.getContext('2d'); const tintas = {}; let canetaOn = false, riscando = false;
function toggleCaneta(){ canetaOn = !canetaOn; tinta.classList.toggle('ativa', canetaOn); ui.querySelector('[data-a=caneta]').classList.toggle('on', canetaOn); }
function ponto(e){ const r = tinta.getBoundingClientRect(); const p = e.touches ? e.touches[0] : e; return [(p.clientX-r.left)*1920/r.width, (p.clientY-r.top)*1080/r.height]; }
function ini(e){ if (!canetaOn) return; riscando = true; const [x,y] = ponto(e); cx.beginPath(); cx.moveTo(x,y); cx.strokeStyle = '#E2342A'; cx.lineWidth = 7; cx.lineCap = 'round'; cx.lineJoin='round'; e.preventDefault(); }
function mov(e){ if (!riscando) return; const [x,y] = ponto(e); cx.lineTo(x,y); cx.stroke(); e.preventDefault(); }
function fim(){ riscando = false; }
tinta.addEventListener('mousedown', ini); tinta.addEventListener('mousemove', mov); addEventListener('mouseup', fim);
tinta.addEventListener('touchstart', ini, {passive:false}); tinta.addEventListener('touchmove', mov, {passive:false}); tinta.addEventListener('touchend', fim);
function salvaTinta(j){ try { tintas[j] = cx.getImageData(0,0,1920,1080); } catch(e){} }
function carregaTinta(j){ cx.clearRect(0,0,1920,1080); if (tintas[j]) cx.putImageData(tintas[j],0,0); }
function limpaTinta(){ cx.clearRect(0,0,1920,1080); delete tintas[i]; }

/* ---------- início ---------- */
const h = (location.hash.match(/^#(\d+)(?:\.(\d+|t))?/)||[]);
const ini0 = h[1] ? (+h[1]-1) : 0;
if (VISTA) { document.documentElement.style.cursor='default'; }
vai(ini0, h[2]==='t' ? 'tudo' : (h[2] ? +h[2] : 0));
if (VISTA) addEventListener('hashchange', ()=>{ const m = location.hash.match(/^#(\d+)(?:\.(\d+|t))?/)||[]; vai(+m[1]-1, m[2]==='t'?'tudo':(+m[2]||0)); });

/* ---------- modo apresentador ---------- */
function montaApresentador(){
  document.body.className = 'zd-apr';
  const base = location.pathname + '?vista';
  document.body.innerHTML = '<div class="zd-apr-wrap"><div class="zd-apr-top"><span class="rel">0:00</span><span id="pos">conectando…</span>'+
   '<button class="zd-bt" id="ant">‹ Voltar</button><button class="zd-bt" id="prox">Avançar ›</button><button class="zd-bt" id="zera" style="background:transparent;color:#F5F1E8">Zerar tempo</button>'+
   '<span style="opacity:.6">Use as setas aqui ou na janela da apresentação.</span></div>'+
   '<div><iframe id="atual" src="'+base+'#1"></iframe><div style="margin:10px 0 6px;color:#C9A84C;font-size:13px;letter-spacing:3px">PRÓXIMO SLIDE</div><iframe id="prox-f" src="'+base+'#2" style="width:55%"></iframe></div>'+
   '<div class="zd-apr-notas"><h4>Notas · o que falar</h4><div id="nt"></div><h4 style="margin-top:22px">Depois</h4><div id="np" style="opacity:.6"></div></div></div>';
  let t0 = Date.now();
  setInterval(()=>{ const s = Math.floor((Date.now()-t0)/1000); document.querySelector('.rel').textContent = Math.floor(s/60)+':'+String(s%60).padStart(2,'0'); }, 1000);
  document.getElementById('zera').onclick = ()=> t0 = Date.now();
  const cmd = c => ch && ch.postMessage({t:'cmd', c});
  document.getElementById('ant').onclick = ()=>cmd('ant');
  document.getElementById('prox').onclick = ()=>cmd('prox');
  addEventListener('keydown', e=>{ if (['ArrowRight',' ','PageDown','ArrowDown'].includes(e.key)){ e.preventDefault(); cmd('prox'); } if (['ArrowLeft','PageUp','ArrowUp'].includes(e.key)){ e.preventDefault(); cmd('ant'); } });
  if (ch) ch.onmessage = m => { const d = m.data||{}; if (d.t!=='estado') return;
    document.getElementById('pos').textContent = 'Slide ' + (d.i+1) + ' de ' + d.total + (d.passos ? ' · clique ' + d.k + ' de ' + d.passos : '');
    document.getElementById('atual').contentWindow.location.hash = '#' + (d.i+1) + '.' + d.k;
    document.getElementById('prox-f').contentWindow.location.hash = d.k < d.passos ? '#' + (d.i+1) + '.' + (d.k+1) : '#' + (d.i+2) + '.0';
    document.getElementById('nt').innerHTML = d.notas || '<i>Sem notas.</i>';
    document.getElementById('np').innerHTML = d.prox || '';
  };
  setTimeout(()=>cmd('pede'), 600);
}
})();

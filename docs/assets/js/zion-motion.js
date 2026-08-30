/*
 * Zion — camada de movimento
 * Aprimoramento progressivo sobre a base CSS. Se este arquivo (ou o bundle do
 * Motion) não carregar, o fallback em cada página revela o conteúdo via
 * IntersectionObserver + transições CSS. Conteúdo nunca fica invisível.
 */
(function () {
  'use strict';

  var M = window.Motion;
  if (!M || !window.ZION_MOTION) return;

  // Sinaliza ao watchdog da página que assumimos os reveals.
  window.ZION_MOTION_READY = true;

  var EASE = [0.16, 1, 0.3, 1]; // mesma curva das transições CSS originais

  // ---------------------------------------------------------------- reveals
  // Agrupa os .fade por elemento-pai para escalonar irmãos (stagger).
  var groups = new Map();
  document.querySelectorAll('.fade').forEach(function (el) {
    var parent = el.parentElement || document.body;
    if (!groups.has(parent)) groups.set(parent, []);
    groups.get(parent).push(el);
  });

  groups.forEach(function (items) {
    items.forEach(function (el, i) {
      M.inView(
        el,
        function () {
          M.animate(
            el,
            { opacity: [0, 1], transform: ['translateY(26px)', 'translateY(0px)'] },
            { duration: 1.2, ease: EASE, delay: Math.min(i, 4) * 0.08 }
          );
          // Neutraliza o estado inicial do CSS para o elemento não voltar a sumir.
          el.classList.add('vis');
          return false; // anima uma vez só
        },
        { amount: 0.12, margin: '0px 0px -40px 0px' }
      );
    });
  });

  // ------------------------------------------------------------- contadores
  var fmt = function (el, v) {
    if (el.dataset.format === 'mil') { el.textContent = Math.round(v).toLocaleString('pt-BR'); return; }
    if (el.dataset.decimal) { el.textContent = v.toFixed(1).replace('.', ','); return; }
    el.textContent = el.dataset.pad
      ? String(Math.round(v)).padStart(+el.dataset.pad, '0')
      : String(Math.round(v));
  };

  document.querySelectorAll('[data-count]').forEach(function (el) {
    var target = +el.dataset.count;
    M.inView(el, function () {
      M.animate(0, target, {
        duration: 1.8,
        ease: [0, 0, 0.2, 1],
        onUpdate: function (v) { fmt(el, v); }
      });
      return false;
    }, { amount: 0.5 });
  });

  // ------------------------------------------- parallax das linhas do relevo
  // Scroll-linked de verdade: acompanha a posição da rolagem, não é um loop.
  var terrain = document.querySelector('.hero .terrain');
  if (terrain && M.scroll) {
    M.scroll(
      M.animate(terrain, { transform: ['translateY(0px)', 'translateY(60px)'] }, { ease: 'linear' }),
      { target: document.querySelector('.hero'), offset: ['start start', 'end start'] }
    );
  }
})();

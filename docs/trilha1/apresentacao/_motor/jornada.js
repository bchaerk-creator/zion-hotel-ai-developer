/* Zion · jornada fluida das aulas interativas (31/10/2026)
   No último slide de cada aula, o botão "Fim" vira "Próximo bloco ›" e leva direto à aula seguinte.
   Só segue sem aviso quando a Ficha deste bloco já foi guardada na Zion (marca gravada pela
   ferramenta, em _landbank.js). Se não foi, o primeiro toque avisa e o segundo toque segue:
   ninguém fica travado por causa de internet ou de e-mail. Nunca envia nada sozinho. */
(function () {
  "use strict";
  var ORDEM = [
    { slug: "marco-zero-aula", pagina: "t1-marco-zero", nome: "Marco Zero" },
    { slug: "pilar1-aula", pagina: "t1-aula-1", nome: "Pilar 1 · Território e destino" },
    { slug: "pilar2-aula", pagina: "t1-aula-2", nome: "Pilar 2 · Mercado e demanda" },
    { slug: "pilar3-aula", pagina: "t1-aula-3", nome: "Pilar 3 · Produto e tipologias" },
    { slug: "pilar4-aula", pagina: "t1-pilar-4", nome: "Pilar 4 · Modelo de negócio" },
    { slug: "pilar5-aula", pagina: "t1-pilar-5", nome: "Pilar 5 · Masterplan faseado" },
    { slug: "pilar6-aula", pagina: "t1-pilar-6", nome: "Pilar 6 · Pré-viabilidade" },
    { slug: "pilar7-aula", pagina: "t1-pilar-7", nome: "Pilar 7 · Capital e Dossiê" }
  ];
  var partes = location.pathname.split("/").filter(Boolean);
  var idx = -1;
  for (var i = 0; i < ORDEM.length; i++) if (partes.indexOf(ORDEM[i].slug) >= 0) idx = i;
  if (idx < 0) return;
  var aqui = ORDEM[idx], prox = ORDEM[idx + 1] || null;
  var destino = prox ? "../" + prox.slug + "/" : "../../index.html";
  var rotulo = prox ? "Próximo bloco ›" : "Concluir o dossiê ›";
  var armado = 0;

  function guardada() {
    try { return !!localStorage.getItem("zion-lb-ok-" + aqui.pagina); } catch (e) { return false; }
  }
  function ultimo() {
    var tela = document.querySelectorAll(".s");
    return tela.length && tela[tela.length - 1].classList.contains("on");
  }
  function aviso(txt) {
    var t = document.getElementById("zj-aviso");
    if (!t) {
      t = document.createElement("div");
      t.id = "zj-aviso";
      t.setAttribute("role", "status");
      t.setAttribute("style", "position:fixed;left:50%;bottom:96px;transform:translateX(-50%);width:calc(100vw - 32px);max-width:640px;box-sizing:border-box;background:#16261C;color:#F5F1E8;border:1.5px solid #B08D3A;border-radius:14px;padding:14px 18px;font:600 16px/1.45 system-ui,sans-serif;z-index:99999;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,.35)");
      document.body.appendChild(t);
    }
    t.textContent = txt;
    t.style.display = "block";
    clearTimeout(t._h);
    t._h = setTimeout(function () { t.style.display = "none"; }, 9000);
  }
  function rotular() {
    var b = document.getElementById("n-prox");
    if (!b) return;
    if (ultimo()) {
      if (b.textContent !== rotulo) b.textContent = rotulo;
      b.setAttribute("aria-label", prox ? "Ir para o próximo bloco: " + prox.nome : "Concluir a jornada");
    }
  }
  document.addEventListener("click", function (e) {
    var b = e.target && e.target.closest && e.target.closest("#n-prox");
    if (!b || !ultimo()) return;
    e.stopImmediatePropagation();
    e.preventDefault();
    if (guardada()) { location.href = destino; return; }
    if (!prox) { aviso("O seu dossiê só está completo depois de enviado à Zion. Volte um slide, gere o dossiê e toque em Enviar ao Land Bank da Zion."); return; }
    if (Date.now() < armado) { location.href = destino; return; }
    armado = Date.now() + 9000;
    aviso("A sua Ficha deste bloco ainda não foi guardada na Zion. Volte um slide, gere a Ficha e toque em Enviar ao Land Bank. Se preferir seguir assim mesmo, toque de novo em " + rotulo.replace(" ›", "") + ".");
  }, true);
  function iniciar() {
    var b = document.getElementById("n-prox");
    if (!b) return;
    new MutationObserver(rotular).observe(b, { childList: true, characterData: true, subtree: true });
    setInterval(rotular, 400);
    rotular();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();

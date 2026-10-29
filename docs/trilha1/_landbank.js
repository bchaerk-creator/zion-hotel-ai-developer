/* Zion · botão "Enviar ao Land Bank" nas ferramentas Faça agora.
   Aparece ao lado do botão do PDF (#pdf), quando ele existir na tela.
   1) Envia a página do Dossiê para o cadastro do aluno (mesmo envio do PDF: enviarParaZion),
      que chega ao Land Bank (Airtable) pelo e-mail.
   2) Mostra o link para completar o cadastro do terreno na Zion Land Members, já com nome e e-mail.
   Nunca trava a ferramenta: qualquer erro só aparece no console. */
(function () {
  "use strict";
  var FORM = "https://airtable.com/appNazhHg9mqWAt9h/pageylHbg89JNYm81/form";
  var PRIVACIDADE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/land-members/privacidade/";
  var emailOk = function (e) { return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(e || "").trim()); };

  function payloadAtual() {
    try {
      if (typeof window.montarPayload === "function" && typeof window.ler === "function") return window.montarPayload(window.ler());
    } catch (e) { console.log("[Zion LB] montarPayload falhou", e); }
    try { // Marco Zero: estado salvo direto no navegador
      var s = JSON.parse(localStorage.getItem("zion-t1-marco-zero") || "null");
      if (s) return { nome: s.nome || "", email: s.email || "", estado: s };
    } catch (e) {}
    return { nome: "", email: "" };
  }

  function linkForm(nome, email) {
    var q = [];
    if (nome) q.push("prefill_" + encodeURIComponent("LM · Nome do membro") + "=" + encodeURIComponent(nome));
    if (email) q.push("prefill_" + encodeURIComponent("LM · E-mail do membro") + "=" + encodeURIComponent(email));
    return FORM + (q.length ? "?" + q.join("&") : "");
  }

  function montar(btnPdf) {
    if (document.getElementById("zlb")) return;
    var box = document.createElement("div");
    box.id = "zlb";
    box.setAttribute("style", "margin-top:18px;padding:16px 18px;border:1.5px solid #B08D3A;border-radius:14px;background:#FBF6E8;color:#16261C;font-size:15px;line-height:1.5");
    box.innerHTML =
      '<strong style="display:block;font-size:17px;margin-bottom:4px">Zion Land Members</strong>' +
      '<span>Guarde esta página do seu Dossiê no seu cadastro do banco de áreas da Zion. A Zion avalia cada caso: não é promessa de investimento, crédito, compra ou sociedade.</span>' +
      '<div id="zlb-email-box" style="display:none;margin-top:10px"><label for="zlb-email" style="display:block;font-weight:600;margin-bottom:4px">O seu e-mail</label>' +
      '<input id="zlb-email" type="email" autocomplete="email" style="width:100%;min-height:44px;border:1.5px solid #B9AE95;border-radius:10px;padding:10px;font:inherit"></div>' +
      '<label style="display:flex;gap:8px;align-items:flex-start;margin-top:10px;font-size:14px"><input id="zlb-ok" type="checkbox" style="margin-top:4px">' +
      '<span>Autorizo a Zion a guardar esta página no meu cadastro do Zion Land Members, conforme o <a href="' + PRIVACIDADE + '" target="_blank" rel="noopener">Aviso de Privacidade</a>.</span></label>' +
      '<button type="button" id="zlb-btn" class="btn" style="margin-top:12px;background:#16261C;color:#F5F1E8;border:0;border-radius:999px;padding:12px 20px;font:inherit;font-weight:600;cursor:pointer">Enviar ao Land Bank da Zion</button>' +
      '<p id="zlb-msg" role="status" style="margin:10px 0 0;font-size:14px"></p>';
    var ancora = btnPdf.closest(".acoes") || btnPdf.parentElement;
    ancora.parentNode.insertBefore(box, ancora.nextSibling);

    var p0 = payloadAtual();
    if (!emailOk(p0.email)) document.getElementById("zlb-email-box").style.display = "block";

    document.getElementById("zlb-btn").addEventListener("click", function () {
      var msg = document.getElementById("zlb-msg");
      if (!document.getElementById("zlb-ok").checked) { msg.textContent = "Marque a autorização para enviar."; return; }
      var p = payloadAtual();
      var campo = document.getElementById("zlb-email");
      if (!emailOk(p.email) && campo && emailOk(campo.value)) p.email = String(campo.value).trim();
      if (!emailOk(p.email)) { document.getElementById("zlb-email-box").style.display = "block"; msg.textContent = "Confira o seu e-mail."; return; }
      p.land_bank = { autorizado: true, quando: new Date().toISOString() };
      msg.textContent = "Enviando...";
      var envio = (typeof window.enviarParaZion === "function") ? window.enviarParaZion(p) : Promise.resolve({ enviado: false });
      Promise.resolve(envio).then(function (r) {
        var ok = r && r.enviado;
        msg.innerHTML = (ok ? "Enviado. Esta página já está no seu cadastro do Land Bank. " : "Não conseguimos enviar agora; baixe o PDF e anexe no cadastro. ") +
          '<a href="' + linkForm(p.nome, p.email) + '" target="_blank" rel="noopener" style="font-weight:700;color:#7A5E12">Completar o cadastro do meu terreno</a>';
      }).catch(function () {
        msg.innerHTML = 'Não conseguimos enviar agora. <a href="' + linkForm(p.nome, p.email) + '" target="_blank" rel="noopener">Completar o cadastro do meu terreno</a>';
      });
    });
  }

  function procurar() {
    var b = document.getElementById("pdf");
    if (b) { try { montar(b); } catch (e) { console.log("[Zion LB]", e); } }
  }
  var obs = new MutationObserver(procurar);
  function iniciar() { procurar(); obs.observe(document.body, { childList: true, subtree: true }); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();

/* Zion · bloco "Agende a sua reunião de direcionamento" no fim da ficha do Pilar 7.
   Leva à agenda pública da Zion (ClickMax), a mesma dos lembretes automáticos. */
(function () {
  "use strict";
  var URL_AGENDA = "https://app.clickmax.io/book/projeto-de-bruno-25763216/xpfd5s9qv4gbiywp-mjuwbwt";
  function montar() {
    if (document.getElementById("reuniao-zion")) return;
    var st = document.createElement("style");
    st.textContent = ".zrn{max-width:760px;margin:36px auto;padding:22px;border:1px solid #C9B37E;border-radius:14px;background:#1B2117;color:#FEF5F0;font-family:Jost,Arial,sans-serif}" +
      ".zrn h3{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:28px;margin:0 0 6px;color:#FEF5F0}" +
      ".zrn p{margin:6px 0;line-height:1.55;font-size:15.5px;color:#E8DFD2}" +
      ".zrn a{display:flex;align-items:center;justify-content:center;margin-top:16px;min-height:52px;border-radius:999px;background:#C9B37E;color:#1B2117;font-weight:600;font-size:17px;text-decoration:none}" +
      ".zrn small{display:block;margin-top:10px;color:#DED6BF}";
    document.head.appendChild(st);
    var box = document.createElement("section");
    box.id = "reuniao-zion"; box.className = "zrn";
    box.innerHTML = "<h3>Agende a sua reunião de direcionamento</h3>" +
      "<p>Com o seu Dossiê de Viabilidade em mãos, converse com a equipe Zion sobre os próximos passos do seu projeto.</p>" +
      "<a href='" + URL_AGENDA + "' target='_blank' rel='noopener'>Agendar a minha reunião</a>" +
      "<small>A reunião ajuda a definir os próximos passos. Ela não garante investimento nem parceria: a Zion avalia cada projeto, caso a caso.</small>";
    (document.querySelector("main") || document.body).appendChild(box);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", montar); else montar();
})();

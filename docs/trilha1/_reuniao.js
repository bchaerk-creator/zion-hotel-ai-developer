/* Zion · bloco de próximo passo no fim da ficha do Pilar 7.
   Desde 22/11/2026 não leva mais à agenda pública: a sessão é agendada dentro da área de membros do Clube. */
(function () {
  "use strict";
  function montar() {
    if (document.getElementById("reuniao-zion")) return;
    var st = document.createElement("style");
    st.textContent = ".zrn{max-width:760px;margin:36px auto;padding:22px;border:1px solid #C9B37E;border-radius:14px;background:#1B2117;color:#FEF5F0;font-family:Jost,Arial,sans-serif}" +
      ".zrn h3{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:28px;margin:0 0 6px;color:#FEF5F0}" +
      ".zrn p{margin:6px 0;line-height:1.55;font-size:15.5px;color:#E8DFD2}" +
      ".zrn small{display:block;margin-top:10px;color:#DED6BF}";
    document.head.appendChild(st);
    var box = document.createElement("section");
    box.id = "reuniao-zion"; box.className = "zrn";
    box.innerHTML = "<h3>Leve o seu Dossiê para a Sessão de onboarding e estratégia</h3>" +
      "<p>Com o seu Dossiê de Viabilidade em mãos, converse com a equipe Zion sobre os próximos passos do seu projeto. O agendamento da sessão fica dentro da área de membros do Clube Zion Collection.</p>" +
      "<small>A sessão ajuda a definir os próximos passos. Ela não garante investimento nem parceria: a Zion avalia cada projeto, caso a caso.</small>";
    (document.querySelector("main") || document.body).appendChild(box);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", montar); else montar();
})();

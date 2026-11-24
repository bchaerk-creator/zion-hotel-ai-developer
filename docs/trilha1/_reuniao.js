/* Zion · bloco de próximo passo no fim da ficha do Pilar 7.
   Desde 24/11/2026 não fala mais em reunião: o Clube de R$ 97 não inclui sessão. Leva ao cadastro do terreno. */
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
    box.innerHTML = "<h3>Envie o seu Dossiê ao banco de áreas da Zion</h3>" +
      "<p>Preencha os formulários e envie as páginas do seu dossiê para a Zion conhecer o seu projeto. O cadastro do terreno fica na área de membros do Clube Zion Collection, no Pilar 7.</p>" +
      "<small>A Zion avalia cada ideia, cada região e cada terreno. O envio não garante investimento nem parceria.</small>";
    (document.querySelector("main") || document.body).appendChild(box);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", montar); else montar();
})();

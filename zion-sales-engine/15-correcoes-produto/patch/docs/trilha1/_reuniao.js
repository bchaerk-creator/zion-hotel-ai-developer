/* Zion · correção de 25/11/2026. Este arquivo NÃO envia nada: sem fetch, sem upload, sem formulário.
   Texto estático com o próximo passo honesto (Sessão de diagnóstico estratégico, depois de concluir o Dossiê). */
(function () {
  "use strict";
  function montar() {
    if (document.getElementById("reuniao-zion")) return;
    var st = document.createElement("style");
    st.textContent = ".zan{max-width:760px;margin:36px auto;padding:22px;border:1px solid #C9B37E;border-radius:14px;background:#1B2117;color:#FEF5F0;font-family:Jost,Arial,sans-serif}" +
      ".zan h3{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:28px;margin:0 0 6px;color:#FEF5F0}" +
      ".zan p{margin:6px 0;line-height:1.55;font-size:15.5px;color:#E8DFD2}" +
      ".zan small{display:block;margin-top:10px;color:#DED6BF}";
    document.head.appendChild(st);
    var box = document.createElement("section");
    box.id = "reuniao-zion"; box.className = "zan";
    box.innerHTML = "<h3>Depois do Dossiê: solicite a Sessão de diagnóstico estratégico</h3>" +
      "<p>Ao concluir o Dossiê, você pode solicitar a Sessão de diagnóstico estratégico com a nossa equipe para apresentar o seu projeto, terreno ou empreendimento. É a sua oportunidade de buscar parceiros e investimentos para tirar o plano do papel*.</p>" +
      "<small>*Gratuita para quem concluiu o Dossiê, mediante solicitação. Sujeita à análise e à agenda. Não é consultoria contínua. Parceria e investimento não são garantidos. Esta ferramenta não envia as suas respostas nem arquivos para a Zion: guarde o PDF do seu Dossiê.</small>";
    (document.querySelector("main") || document.body).appendChild(box);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", montar); else montar();
})();

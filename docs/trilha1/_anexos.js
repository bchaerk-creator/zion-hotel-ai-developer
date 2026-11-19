/* Zion · bloco "Anexos do seu terreno" nas fichas Faça agora.
   Fotos, vídeos e documentos vão direto para o armazenamento privado da Zion (URL assinada),
   sem passar pelo servidor. Entra só nas fichas que carregam este arquivo (Pilar 1 e Pilar 5).
   Uso: <script src="../_anexos.js" data-ficha="pilar1"></script>
   Rotas: POST {API}/iniciar  ->  PUT em cada url_upload  ->  POST {API}/concluir. */
(function () {
  "use strict";
  var script = document.currentScript;
  var FICHA = (script && script.getAttribute("data-ficha")) || "";
  var API = (script && script.getAttribute("data-api")) || "https://zion-dossie-aulas.lovable.app/api/anexo";
  if (FICHA !== "pilar1" && FICHA !== "pilar5") return;

  var LIM = { foto: 15, video: 100, documento: 20 }; // MB
  var TIPOS = {
    "image/jpeg": "foto", "image/png": "foto", "image/webp": "foto", "image/heic": "foto",
    "video/mp4": "video", "video/quicktime": "video",
    "application/pdf": "documento",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "documento",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "documento",
    "application/vnd.google-earth.kml+xml": "documento"
  };
  var EXT = { jpg: "image/jpeg", jpeg: "image/jpeg", png: "image/png", webp: "image/webp", heic: "image/heic", mp4: "video/mp4", mov: "video/quicktime", pdf: "application/pdf", docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document", xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", kml: "application/vnd.google-earth.kml+xml" };
  var MAX_POR_ENVIO = 10;

  function tipoDe(f) {
    if (f.type && TIPOS[f.type]) return f.type;
    var m = /\.([a-z0-9]+)$/i.exec(f.name || "");
    return m && EXT[m[1].toLowerCase()] ? EXT[m[1].toLowerCase()] : "";
  }
  function mb(n) { return n < 1048576 ? Math.max(1, Math.round(n / 1024)) + " KB" : (n / 1048576).toFixed(n >= 10485760 ? 0 : 1).replace(".", ",") + " MB"; }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function emailValido(e) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(e); }

  var css = ".zan{max-width:760px;margin:36px auto;padding:22px;border:1px solid #DED6BF;border-radius:14px;background:#FEF5F0;color:#14170F;font-family:Jost,Arial,sans-serif}" +
    ".zan h3{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:28px;margin:0 0 6px;color:#14170F}" +
    ".zan p{margin:6px 0;line-height:1.55;font-size:15.5px;color:#3a352f}" +
    ".zan label{display:block;margin-top:14px;font-size:14px;font-weight:500}" +
    ".zan input[type=email]{width:100%;padding:12px;border:1px solid #bfb79f;border-radius:8px;font-size:16px;background:#fff}" +
    ".zan .zan-drop{margin-top:14px;border:2px dashed #8B714E;border-radius:12px;padding:18px;text-align:center;background:#fff;cursor:pointer}" +
    ".zan .zan-drop b{color:#8B714E}" +
    ".zan ul{list-style:none;margin:12px 0 0;padding:0}" +
    ".zan li{display:flex;gap:10px;align-items:center;justify-content:space-between;padding:9px 0;border-bottom:1px solid #e6dfcc;font-size:14.5px}" +
    ".zan li small{color:#6b645c}" +
    ".zan .zan-ok{color:#2e6b3a;font-weight:600}.zan .zan-erro{color:#9b2c2c;font-weight:600}" +
    ".zan button{font:inherit;cursor:pointer}" +
    ".zan .zan-rm{background:none;border:0;color:#9b2c2c;font-size:20px;line-height:1}" +
    ".zan .zan-enviar{margin-top:16px;width:100%;min-height:50px;border:0;border-radius:999px;background:#1B2117;color:#C9B37E;font-size:17px;font-weight:600}" +
    ".zan .zan-enviar[disabled]{opacity:.5;cursor:not-allowed}" +
    ".zan .zan-aceite{display:flex;gap:10px;align-items:flex-start;margin-top:14px;font-size:13.5px;font-weight:400}" +
    ".zan .zan-msg{margin-top:12px;font-size:15px}" +
    ".zan progress{width:90px;height:8px}";

  function montar() {
    if (document.getElementById("anexos-zion")) return;
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    var box = document.createElement("section");
    box.id = "anexos-zion"; box.className = "zan";
    box.innerHTML =
      "<h3>Anexos do seu terreno</h3>" +
      "<p>Envie fotos, vídeos e documentos do terreno e da região para a equipe Zion montar o seu estudo com você. Isso é opcional e você pode enviar mais depois.</p>" +
      "<p><small>Aceitamos fotos (JPG, PNG, WEBP, HEIC, até " + LIM.foto + " MB), vídeos (MP4, MOV, até " + LIM.video + " MB) e documentos (PDF, DOCX, XLSX, KML, até " + LIM.documento + " MB). No máximo " + MAX_POR_ENVIO + " arquivos por envio.</small></p>" +
      "<label for='zan-email'>Seu e-mail (o mesmo da ficha)</label>" +
      "<input id='zan-email' type='email' autocomplete='email' placeholder='voce@email.com'>" +
      "<div class='zan-drop' id='zan-drop' tabindex='0' role='button' aria-label='Escolher arquivos'><b>Toque para escolher os arquivos</b><br><small>ou arraste para cá</small></div>" +
      "<input id='zan-file' type='file' multiple style='display:none' accept='image/jpeg,image/png,image/webp,image/heic,video/mp4,video/quicktime,application/pdf,.docx,.xlsx,.kml,.heic'>" +
      "<ul id='zan-lista'></ul>" +
      "<label class='zan-aceite'><input id='zan-aceite' type='checkbox'><span>Autorizo a Zion a usar estes arquivos para montar o meu estudo de viabilidade. Não envie CPF, RG nem documentos pessoais além do necessário.</span></label>" +
      "<button class='zan-enviar' id='zan-enviar' disabled>Enviar arquivos</button>" +
      "<div class='zan-msg' id='zan-msg' role='status' aria-live='polite'></div>";
    var alvo = document.querySelector("main") || document.body;
    alvo.appendChild(box);

    var fila = []; // {file, tipo, categoria, estado, el}
    var emailEl = box.querySelector("#zan-email"), fileEl = box.querySelector("#zan-file"), lista = box.querySelector("#zan-lista");
    var aceite = box.querySelector("#zan-aceite"), btn = box.querySelector("#zan-enviar"), msg = box.querySelector("#zan-msg"), drop = box.querySelector("#zan-drop");
    try { var salvo = window.localStorage.getItem("zion_anexos_email"); if (salvo) emailEl.value = salvo; } catch (e) { /* sem armazenamento */ }

    function atualizar() {
      lista.innerHTML = "";
      fila.forEach(function (it, i) {
        var li = document.createElement("li");
        var estado = it.estado === "ok" ? "<span class='zan-ok'>enviado</span>" : it.estado === "erro" ? "<span class='zan-erro'>falhou</span>" : it.estado === "enviando" ? "<progress max='100' value='" + (it.pct || 0) + "'></progress>" : "";
        li.innerHTML = "<span>" + esc(it.file.name) + " <small>(" + mb(it.file.size) + ")</small></span><span>" + estado + (it.estado === "pendente" || it.estado === "erro" ? " <button class='zan-rm' aria-label='Remover' data-i='" + i + "'>×</button>" : "") + "</span>";
        lista.appendChild(li);
      });
      var podeEnviar = fila.some(function (x) { return x.estado === "pendente" || x.estado === "erro"; }) && aceite.checked && emailValido(emailEl.value.trim());
      btn.disabled = !podeEnviar || btn.getAttribute("data-busy") === "1";
    }
    function adicionar(files) {
      var avisos = [];
      Array.prototype.forEach.call(files, function (f) {
        var pend = fila.filter(function (x) { return x.estado !== "ok"; }).length;
        var t = tipoDe(f), cat = TIPOS[t];
        if (!t) { avisos.push(f.name + ": tipo não aceito."); return; }
        if (f.size > LIM[cat] * 1048576) { avisos.push(f.name + ": passa de " + LIM[cat] + " MB."); return; }
        if (f.size === 0) { avisos.push(f.name + ": arquivo vazio."); return; }
        if (pend >= MAX_POR_ENVIO) { avisos.push("Máximo de " + MAX_POR_ENVIO + " arquivos por envio. Envie estes e depois adicione mais."); return; }
        fila.push({ file: f, tipo: t, categoria: cat, estado: "pendente", pct: 0 });
      });
      msg.textContent = avisos.join(" ");
      atualizar();
    }
    drop.addEventListener("click", function () { fileEl.click(); });
    drop.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); fileEl.click(); } });
    drop.addEventListener("dragover", function (e) { e.preventDefault(); });
    drop.addEventListener("drop", function (e) { e.preventDefault(); if (e.dataTransfer && e.dataTransfer.files) adicionar(e.dataTransfer.files); });
    fileEl.addEventListener("change", function () { adicionar(fileEl.files); fileEl.value = ""; });
    lista.addEventListener("click", function (e) { var i = e.target && e.target.getAttribute && e.target.getAttribute("data-i"); if (i !== null && i !== undefined) { fila.splice(Number(i), 1); atualizar(); } });
    aceite.addEventListener("change", atualizar);
    emailEl.addEventListener("input", atualizar);

    function post(rota, corpo) {
      return fetch(API + "/" + rota, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corpo) }).then(function (r) {
        return r.json().catch(function () { return { ok: false }; }).then(function (j) { j.__status = r.status; return j; });
      });
    }
    function subir(it, url) {
      return new Promise(function (resolve) {
        var x = new XMLHttpRequest();
        x.open("PUT", url);
        x.setRequestHeader("Content-Type", it.tipo);
        x.upload.onprogress = function (e) { if (e.lengthComputable) { it.pct = Math.round((e.loaded / e.total) * 100); atualizar(); } };
        x.onload = function () { resolve(x.status >= 200 && x.status < 300); };
        x.onerror = function () { resolve(false); };
        x.send(it.file);
      });
    }
    btn.addEventListener("click", function () {
      var email = emailEl.value.trim().toLowerCase();
      var itens = fila.filter(function (x) { return x.estado === "pendente" || x.estado === "erro"; });
      if (!itens.length || !aceite.checked || !emailValido(email)) return;
      btn.setAttribute("data-busy", "1"); msg.textContent = "Preparando o envio…"; atualizar();
      post("iniciar", { email: email, ficha: FICHA, aceite: true, arquivos: itens.map(function (x) { return { nome: x.file.name, tipo: x.tipo, tamanho: x.file.size, categoria: x.categoria }; }) })
        .then(function (r) {
          if (!r || !r.ok || !r.envios || r.envios.length !== itens.length) { throw new Error((r && r.erro) || "Não foi possível enviar agora. Tente de novo."); }
          try { window.localStorage.setItem("zion_anexos_email", email); } catch (e) { /* ok */ }
          itens.forEach(function (x) { x.estado = "enviando"; x.pct = 0; });
          atualizar(); msg.textContent = "Enviando…";
          return Promise.all(itens.map(function (it, i) {
            it.id = r.envios[i].id;
            return subir(it, r.envios[i].url_upload).then(function (ok) { it.estado = ok ? "enviado" : "erro"; atualizar(); return ok; });
          }));
        })
        .then(function () {
          var enviados = itens.filter(function (x) { return x.estado === "enviado"; });
          if (!enviados.length) { throw new Error("Nenhum arquivo foi enviado. Confira a internet e tente de novo."); }
          return post("concluir", { email: email, ids: enviados.map(function (x) { return x.id; }) }).then(function (r2) {
            if (!r2 || !r2.ok) { throw new Error((r2 && r2.erro) || "Não foi possível confirmar o envio."); }
            var falt = {}; (r2.faltando || []).forEach(function (id) { falt[id] = 1; });
            enviados.forEach(function (x) { x.estado = falt[x.id] ? "erro" : "ok"; });
            var ok = enviados.filter(function (x) { return x.estado === "ok"; }).length, falhou = itens.length - ok;
            msg.innerHTML = ok ? "<span class='zan-ok'>Recebemos " + ok + (ok === 1 ? " arquivo." : " arquivos.") + "</span>" + (falhou ? " <span class='zan-erro'>" + falhou + " não foi(ram) enviado(s): tente de novo.</span>" : "") : "<span class='zan-erro'>Não conseguimos confirmar o envio. Tente de novo.</span>";
          });
        })
        .catch(function (e) {
          itens.forEach(function (x) { if (x.estado === "enviando" || x.estado === "pendente") x.estado = "erro"; });
          msg.innerHTML = "<span class='zan-erro'>" + esc(e && e.message ? e.message : "Não foi possível enviar agora. Tente de novo.") + "</span>";
        })
        .then(function () { btn.removeAttribute("data-busy"); atualizar(); });
    });
    atualizar();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", montar); else montar();
})();

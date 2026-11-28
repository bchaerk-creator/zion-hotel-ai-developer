/* Zion · Fotos da propriedade (Trilha 1).
   Módulo compartilhado: a ficha do Território (aula1) coloca as fotos; o Dossiê (pilar7) lê e põe no PDF.
   NÃO envia nada: sem fetch, sem upload, sem formulário. As fotos ficam só neste aparelho (localStorage),
   já reduzidas e recomprimidas no navegador (o canvas descarta EXIF e geolocalização). */
(function (raiz, fabrica) {
  "use strict";
  var api = fabrica();
  if (typeof module === "object" && module.exports) { module.exports = api; return; }
  raiz.ZionFotos = api;
  // Na ficha: <script src="../_fotos.js" data-montar="1"></script> desenha o bloco. No Dossiê, só lê.
  var tag = document.currentScript;
  if (tag && tag.getAttribute("data-montar") === "1") {
    var iniciar = function () { api.montar(document.querySelector("main") || document.body); };
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
  }
})(typeof window !== "undefined" ? window : this, function () {
  "use strict";

  var CHAVE = "zion-t1-fotos";
  var MAX_FOTOS = 6;
  var MAX_BYTES = 5 * 1024 * 1024;
  var MAX_LADO = 1200;
  var QUALIDADE = 0.8;
  var MAX_LEGENDA = 100;
  var MAX_CHARS_FOTO = 600000; // teto de texto por foto salva, para caber no armazenamento do navegador
  var TIPOS = ["image/jpeg", "image/png", "image/webp"];
  var EXT = { jpg: "image/jpeg", jpeg: "image/jpeg", png: "image/png", webp: "image/webp" };

  /* ---------- lógica pura (testada em Node) ---------- */
  function tipoDoArquivo(arq) {
    var t = String((arq && arq.type) || "").toLowerCase();
    if (t) return t === "image/jpg" ? "image/jpeg" : t;
    var m = /\.([a-z0-9]+)$/i.exec(String((arq && arq.name) || ""));
    return m && EXT[m[1].toLowerCase()] ? EXT[m[1].toLowerCase()] : "";
  }
  // Devolve {ok:true} ou {ok:false, erro:"mensagem em português"}.
  function validarArquivo(arq, qtdAtual) {
    var nome = (arq && arq.name) ? '"' + arq.name + '"' : "Este arquivo";
    if (!arq) return { ok: false, erro: "Não foi possível ler o arquivo." };
    if ((qtdAtual || 0) >= MAX_FOTOS) return { ok: false, erro: "Você já tem " + MAX_FOTOS + " fotos, que é o limite. Remova uma para enviar outra." };
    if (TIPOS.indexOf(tipoDoArquivo(arq)) < 0) return { ok: false, erro: nome + " não foi aceito: use uma foto em JPG, PNG ou WEBP." };
    if (!(arq.size > 0)) return { ok: false, erro: nome + " está vazio." };
    if (arq.size > MAX_BYTES) return { ok: false, erro: nome + " tem mais de 5 MB. Escolha uma foto menor ou reduza o tamanho dela." };
    return { ok: true };
  }
  // Mantém a proporção; nunca aumenta a imagem.
  function dimensoesFinais(w, h, max) {
    max = max || MAX_LADO;
    w = Number(w); h = Number(h);
    if (!(w > 0) || !(h > 0)) return { w: 0, h: 0 };
    var maior = Math.max(w, h);
    if (maior <= max) return { w: Math.round(w), h: Math.round(h) };
    var f = max / maior;
    return { w: Math.max(1, Math.round(w * f)), h: Math.max(1, Math.round(h * f)) };
  }
  // Cabe a imagem dentro de uma caixa (mm), sem distorcer.
  function encaixar(w, h, caixaW, caixaH) {
    if (!(w > 0) || !(h > 0)) return { w: 0, h: 0 };
    var f = Math.min(caixaW / w, caixaH / h);
    return { w: w * f, h: h * f };
  }
  function limparLegenda(t) {
    return String(t == null ? "" : t).replace(/[\u0000-\u001F\u007F]+/g, " ").replace(/\s+/g, " ").trim().slice(0, MAX_LEGENDA);
  }
  // Quantas das n fotos novas cabem agora.
  function vagas(qtdAtual) { return Math.max(0, MAX_FOTOS - (qtdAtual || 0)); }
  function itemValido(f) {
    return !!f && typeof f.dataUrl === "string" && /^data:image\/jpeg;base64,[A-Za-z0-9+\/=]+$/.test(f.dataUrl) &&
      f.w > 0 && f.h > 0;
  }
  // Lê o texto salvo e devolve só itens íntegros, no máximo 6.
  function interpretar(raw) {
    try {
      var d = JSON.parse(raw);
      var lista = d && Array.isArray(d.fotos) ? d.fotos : [];
      return lista.filter(itemValido).slice(0, MAX_FOTOS).map(function (f) {
        return { id: String(f.id || ""), legenda: limparLegenda(f.legenda), dataUrl: f.dataUrl, w: Number(f.w), h: Number(f.h) };
      });
    } catch (e) { return []; }
  }
  function serializar(fotos) { return JSON.stringify({ v: 1, fotos: fotos }); }

  /* ---------- armazenamento ---------- */
  function ler() {
    try { var raw = window.localStorage.getItem(CHAVE); return raw ? interpretar(raw) : []; } catch (e) { return []; }
  }
  function salvar(fotos) {
    try { window.localStorage.setItem(CHAVE, serializar(fotos)); return true; } catch (e) { return false; }
  }

  /* ---------- navegador: reduzir e comprimir ---------- */
  function carregarImagem(arq) {
    return new Promise(function (ok, falha) {
      var url = URL.createObjectURL(arq), img = new Image();
      img.onload = function () { URL.revokeObjectURL(url); ok(img); };
      img.onerror = function () { URL.revokeObjectURL(url); falha(new Error("ilegivel")); };
      img.src = url;
    });
  }
  function reduzir(arq) {
    return carregarImagem(arq).then(function (img) {
      var tam = dimensoesFinais(img.naturalWidth, img.naturalHeight, MAX_LADO);
      if (!tam.w) throw new Error("ilegivel");
      var c = document.createElement("canvas");
      c.width = tam.w; c.height = tam.h;
      var g = c.getContext("2d");
      g.fillStyle = "#ffffff"; g.fillRect(0, 0, tam.w, tam.h); // PNG com fundo transparente vira fundo branco
      g.drawImage(img, 0, 0, tam.w, tam.h);
      var q = QUALIDADE, url = c.toDataURL("image/jpeg", q);
      while (url.length > MAX_CHARS_FOTO && q > 0.45) { q -= 0.1; url = c.toDataURL("image/jpeg", q); }
      return { dataUrl: url, w: tam.w, h: tam.h };
    });
  }

  /* ---------- interface (só na ficha) ---------- */
  function montar(destino) {
    if (!destino || document.getElementById("fotos-zion")) return;
    var st = document.createElement("style");
    st.textContent =
      ".zfo{margin-top:22px}.zfo h3{margin:0 0 6px}.zfo .grade{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:14px 0}" +
      ".zfo figure{margin:0;border:1px solid var(--linha,#D6CDB8);border-radius:10px;padding:8px;background:#fff;min-width:0}" +
      ".zfo img{display:block;width:100%;height:120px;object-fit:cover;border-radius:6px}" +
      ".zfo figcaption{margin-top:6px}.zfo figcaption input{width:100%;min-height:40px;padding:8px;font-size:.9rem}" +
      ".zfo .rm{margin-top:6px;width:100%;min-height:40px;padding:8px 12px;font-size:.9rem}" +
      ".zfo .msg{margin:8px 0 0;font-size:.92rem}.zfo .msg.erro{color:var(--critico,#9B2C1F);font-weight:600}" +
      ".zfo input[type=file]{position:absolute;width:1px;height:1px;opacity:0;overflow:hidden}";
    document.head.appendChild(st);
    var sec = document.createElement("section");
    sec.id = "fotos-zion"; sec.className = "card zfo";
    sec.innerHTML =
      '<div class="eyebrow">Fotos da propriedade</div>' +
      "<h3>Anexe até " + MAX_FOTOS + " fotos do terreno</h3>" +
      '<p class="lead">Elas entram numa página do seu Dossiê em PDF. Aceitamos JPG, PNG ou WEBP, até 5 MB cada. A legenda é opcional.</p>' +
      '<input type="file" id="fotos-arq" accept="image/jpeg,image/png,image/webp" multiple aria-label="Escolher fotos do terreno">' +
      '<button type="button" class="btn btn-s" id="fotos-btn">Escolher fotos</button>' +
      '<p class="msg" id="fotos-msg" role="status" aria-live="polite"></p>' +
      '<div class="grade" id="fotos-grade"></div>' +
      '<p class="dica" style="font-size:.85rem">As fotos ficam só neste aparelho: não são enviadas à Zion nem a ninguém. Elas são reduzidas aqui mesmo e perdem dados ocultos, como o local onde foram tiradas. No PDF vão com o aviso: fotos enviadas pelo próprio empreendedor, sem verificação da Zion. Não use fotos de pessoas.</p>';
    destino.appendChild(sec);

    var fotos = ler();
    var msg = sec.querySelector("#fotos-msg"), grade = sec.querySelector("#fotos-grade"), entrada = sec.querySelector("#fotos-arq");
    function aviso(t, erro) { msg.textContent = t || ""; msg.className = "msg" + (erro ? " erro" : ""); }
    function persistir() {
      if (!salvar(fotos)) { aviso("O aparelho não tem espaço para guardar todas as fotos. Remova uma foto ou use fotos menores.", true); return false; }
      return true;
    }
    function desenhar() {
      grade.innerHTML = "";
      fotos.forEach(function (f, i) {
        var fig = document.createElement("figure");
        var im = document.createElement("img"); im.src = f.dataUrl; im.alt = f.legenda || "Foto " + (i + 1) + " da propriedade";
        var cap = document.createElement("figcaption");
        var inp = document.createElement("input"); inp.type = "text"; inp.maxLength = MAX_LEGENDA; inp.placeholder = "Legenda (opcional)"; inp.value = f.legenda;
        inp.setAttribute("aria-label", "Legenda da foto " + (i + 1));
        inp.addEventListener("change", function () { f.legenda = limparLegenda(inp.value); inp.value = f.legenda; persistir(); });
        cap.appendChild(inp);
        var rm = document.createElement("button"); rm.type = "button"; rm.className = "btn btn-s rm"; rm.textContent = "Remover foto";
        rm.addEventListener("click", function () { fotos.splice(i, 1); persistir(); desenhar(); aviso("Foto removida."); });
        fig.appendChild(im); fig.appendChild(cap); fig.appendChild(rm); grade.appendChild(fig);
      });
      sec.querySelector("#fotos-btn").disabled = fotos.length >= MAX_FOTOS;
    }
    sec.querySelector("#fotos-btn").addEventListener("click", function () { entrada.click(); });
    entrada.addEventListener("change", function () {
      var arqs = Array.prototype.slice.call(entrada.files || []);
      entrada.value = "";
      var erros = [], fila = [];
      arqs.forEach(function (a) {
        var v = validarArquivo(a, fotos.length + fila.length);
        if (v.ok) fila.push(a); else erros.push(v.erro);
      });
      var seq = Promise.resolve(), adicionadas = 0;
      fila.forEach(function (a) {
        seq = seq.then(function () { return reduzir(a); }).then(function (r) {
          fotos.push({ id: String(Date.now()) + "-" + fotos.length, legenda: "", dataUrl: r.dataUrl, w: r.w, h: r.h });
          adicionadas++;
        }).catch(function () { erros.push('Não foi possível ler "' + a.name + '". Ela pode estar corrompida.'); });
      });
      seq.then(function () {
        var ok = persistir();
        desenhar();
        if (!ok) { fotos.splice(fotos.length - adicionadas, adicionadas); salvar(fotos); desenhar(); return; }
        if (erros.length) aviso(erros.join(" ") + (adicionadas ? " " + adicionadas + " foto(s) adicionada(s)." : ""), true);
        else aviso(adicionadas ? adicionadas + " foto(s) adicionada(s) e salva(s) neste aparelho." : "");
      });
    });
    desenhar();
  }

  return {
    CHAVE: CHAVE, MAX_FOTOS: MAX_FOTOS, MAX_BYTES: MAX_BYTES, MAX_LADO: MAX_LADO, QUALIDADE: QUALIDADE, MAX_LEGENDA: MAX_LEGENDA, TIPOS: TIPOS,
    AVISO_PDF: "Fotos enviadas pelo próprio empreendedor, sem verificação da Zion.",
    tipoDoArquivo: tipoDoArquivo, validarArquivo: validarArquivo, dimensoesFinais: dimensoesFinais, encaixar: encaixar,
    limparLegenda: limparLegenda, vagas: vagas, interpretar: interpretar, serializar: serializar,
    ler: ler, salvar: salvar, montar: montar
  };
});

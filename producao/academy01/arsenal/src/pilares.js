/* Interface dos Pilares 2 a 7 e da conclusão (telas 09 a 40). Usa window.ZA (app base) e window.ZionLogic2. */
(function () {
  "use strict";
  var P = window.ZionLogic2, A = function () { return window.ZA; };
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var brl = function (v) { if (v == null) return "–"; var n = Math.round(v); return (n < 0 ? "−" : "") + "R$ " + Math.abs(n).toLocaleString("pt-BR"); };
  var pct = function (v) { return v == null ? "–" : (Math.round(v * 10) / 10).toLocaleString("pt-BR") + "%"; };

  var TELAS = { 9: "Para todo mundo é para ninguém", 10: "Exemplos de públicos", 11: "Características do imóvel", 12: "Perfil prioritário", 13: "Perfil validado",
    14: "Característica não é benefício", 15: "Genérica × diferenciada", 16: "Diferenciais reais", 17: "Proposta de valor", 18: "Proposta final",
    19: "Títulos genéricos", 20: "Como montar título e descrição", 21: "Seu anúncio hoje", 22: "Três títulos e uma descrição", 23: "Versão final",
    24: "Preço sem custo", 25: "Os números do dinheiro", 26: "Seus custos", 27: "Margem e simulação", 28: "Diagnóstico financeiro",
    29: "A experiência começa antes", 30: "Melhorias simples", 31: "Auditoria da jornada", 32: "Impacto, custo e esforço", 33: "Checklist da experiência",
    34: "Uma mudança por vez", 35: "Matriz impacto × esforço", 36: "Ações prioritárias", 37: "Cronograma", 38: "Plano de 30 dias",
    39: "Painel dos sete resultados", 40: "Dossiê final" };

  /* ---------- estado ---------- */
  function E() { var e = A().estado; ["p2", "p3", "p4", "p5", "p6", "p7"].forEach(function (k) { if (!e[k] || typeof e[k] !== "object") e[k] = {}; }); return e; }
  function get(path) { return path.split(".").reduce(function (o, k) { return o == null ? undefined : o[k]; }, E()); }
  function set(path, v) { var ks = path.split("."), o = E(); for (var i = 0; i < ks.length - 1; i++) { if (o[ks[i]] == null || typeof o[ks[i]] !== "object") o[ks[i]] = /^\d+$/.test(ks[i + 1]) ? [] : {}; o = o[ks[i]]; } o[ks[ks.length - 1]] = v; }
  function arr(path) { var v = get(path); return Array.isArray(v) ? v : []; }
  function preencher(raiz) {
    (raiz || document).querySelectorAll("[data-k]").forEach(function (el) {
      var v = get(el.getAttribute("data-k"));
      if (el.type === "checkbox") el.checked = !!v;
      else if (el.type === "radio") el.checked = (v != null && String(v) === el.value);
      else el.value = v == null ? "" : v;
    });
    (raiz || document).querySelectorAll("[data-arr]").forEach(function (el) { el.checked = arr(el.getAttribute("data-arr")).indexOf(el.value) >= 0; });
  }
  document.addEventListener("input", function (ev) {
    var el = ev.target, k = el.getAttribute && el.getAttribute("data-k"), a = el.getAttribute && el.getAttribute("data-arr");
    if (k) set(k, el.type === "checkbox" ? el.checked : el.value);
    if (a) { var l = arr(a).slice(); var i = l.indexOf(el.value); if (el.checked && i < 0) l.push(el.value); if (!el.checked && i >= 0) l.splice(i, 1); set(a, l); }
    if (k || a) { A().salvar(); vivo(); }
  });
  function telaAtual() { var t = document.querySelector(".tela.ativa"); return t ? +t.getAttribute("data-t") : 0; }
  function vivo() {
    var n = telaAtual();
    if (n === 12) { sugerirP2(); pintarEssenciais(); }
    if (n === 17) pintarChecksProposta();
    if (n === 21 || n === 22) pintarChecksAnuncio();
    if (n === 26) { var f = P.financeiro(get("p5") || {}); mostrarErrosP5(f); }
    if (n === 27) pintarSim();
    if (n === 23) pintarP4Fb();
    if (n === 35) pintarMatriz();
    if (n === 37) pintarAvisosCrono();
  }

  /* ---------- contexto compartilhado ---------- */
  function publicoNome() { var p2 = E().p2; return p2.publico === "outro" ? (p2.publicoOutro || "") : (P.PUBLICOS[p2.publico] ? P.PUBLICOS[p2.publico].nome : ""); }
  function difs() { return [0, 1, 2, 3, 4, 5].map(function (i) { return get("p3.dif." + i) || {}; }).filter(function (d) { return d.caracteristica && String(d.caracteristica).trim(); }); }
  function ctxAnuncio() { return { diferenciais: difs(), publicoNome: publicoNome() }; }
  function proposta() { return (get("p3.proposta") || "").trim(); }
  function tituloFinal() { var i = get("p4.final"); return i == null || i === "" ? "" : (get("p4.t" + i) || "").trim(); }
  function bloco(b) {
    var tipo = b.tipo || "pendencia", ROT = { resultado: "Seu resultado", significado: "O que isso significa", atencao: "O que merece atenção", fazer: "O que fazer agora", verificar: "Como verificar" };
    return '<article class="fb"><header><span class="etq ' + tipo + '">' + ({ fato: "Fato", hipotese: "Hipótese", pendencia: "Pendência" }[tipo]) + '</span><h4>' + esc(b.titulo) + '</h4></header><dl>' +
      Object.keys(ROT).map(function (k) { return '<div><dt>' + ROT[k] + '</dt><dd' + (k === "fazer" ? ' class="forte"' : '') + '>' + esc(b[k]) + '</dd></div>'; }).join("") + '</dl></article>';
  }
  function checksHtml(av, extra) { return av.checks.concat(extra || []).map(function (c) { return '<li class="' + (c.ok ? "ok" : "") + '">' + esc(c.txt) + '</li>'; }).join(""); }
  function erro(id, msg) { var el = $(id); if (el) el.textContent = msg || ""; return !msg; }

  /* ================= PILAR 2 ================= */
  function montarP2() {
    $("p2exemplos").innerHTML = Object.keys(P.PUBLICOS).map(function (id) { var p = P.PUBLICOS[id];
      return '<div class="cartao"><h4 style="font-family:var(--f-display);font-weight:400;font-size:26px;margin:0 0 6px;color:var(--creme)">' + esc(p.nome) + '</h4><p style="margin:0 0 6px"><b style="color:var(--creme);font-weight:600">Procura:</b> ' + esc(p.necessidade) + '.</p><p style="margin:0 0 6px"><b style="color:var(--creme);font-weight:600">Costuma travar com:</b> ' + esc(p.objecao) + '.</p><p class="small" style="margin:0">Itens que valoriza: ' + p.precisa.map(P.nomeCarac).join(", ") + '</p></div>'; }).join("");
    $("p2caracs").innerHTML = P.CARACTERISTICAS.map(function (c) { return '<label><input type="checkbox" data-arr="p2.caracs" value="' + c[0] + '">' + esc(c[1]) + '</label>'; }).join("");
  }
  function pintarP2Afinidade() {
    var cap = (A().estado.perfil || {}).capacidade, af = P.afinidade(arr("p2.caracs"), cap);
    $("p2afinidade").innerHTML = af.map(function (a) {
      return '<label class="opcao"><input type="radio" name="p2pub" data-k="p2.publico" value="' + a.id + '"><span><b>' + esc(a.nome) + '</b><small>' + (a.bate.length ? "Tem: " + a.bate.map(P.nomeCarac).join(", ") : "Nenhum dos itens marcados") + (a.cabe === false ? " · capacidade menor do que esse perfil costuma precisar" : "") + '</small><span class="barra-af"><i style="width:' + a.pct + '%"></i></span></span><span class="pct-af">' + a.pct + '%</span></label>';
    }).join("") + '<label class="opcao"><input type="radio" name="p2pub" data-k="p2.publico" value="outro"><span><b>Outro perfil</b><input type="text" data-k="p2.publicoOutro" placeholder="Descreva o perfil" style="margin-top:8px"></span><span></span></label>';
    preencher($("p2afinidade"));
    sugerirP2();
    pintarEssenciais();
  }
  function sugerirP2() {
    var pub = P.PUBLICOS[get("p2.publico")]; if (!pub) return;
    var mudou = false;
    if (!get("p2.necessidade")) { set("p2.necessidade", pub.necessidade); mudou = true; }
    if (!get("p2.objecao")) { set("p2.objecao", pub.objecao); mudou = true; }
    if (mudou) { document.querySelectorAll('[data-k="p2.necessidade"],[data-k="p2.objecao"]').forEach(function (el) { el.value = get(el.getAttribute("data-k")); }); A().salvar(); }
  }
  function pintarEssenciais() {
    var marc = arr("p2.caracs"), lista = P.CARACTERISTICAS.filter(function (c) { return marc.indexOf(c[0]) >= 0; });
    if (!lista.length) lista = P.CARACTERISTICAS;
    var box = $("p2essenciais"); if (!box) return;
    var atual = box.getAttribute("data-ids"), ids = lista.map(function (c) { return c[0]; }).join(",");
    if (atual !== ids) { box.innerHTML = lista.map(function (c) { return '<label><input type="checkbox" data-arr="p2.essenciais" value="' + c[0] + '">' + esc(c[1]) + '</label>'; }).join(""); box.setAttribute("data-ids", ids); preencher(box); }
    var n = arr("p2.essenciais").length; erro("e_p2_essenciais", n > 3 ? "Você marcou " + n + ". Deixe só 3." : "");
  }
  function perfilAtual() { var p2 = E().p2; return { publico: p2.publico === "outro" ? (p2.publicoOutro ? "outro" : "") : p2.publico, ocasiao: p2.ocasiao, pessoas: p2.pessoas, necessidade: p2.necessidade, objecao: p2.objecao, essenciais: arr("p2.essenciais") }; }
  function validarP2(mostrar) {
    var v = P.validarPerfil(perfilAtual(), arr("p2.caracs"), (A().estado.perfil || {}).capacidade);
    if (mostrar) ["publico", "ocasiao", "pessoas", "necessidade", "objecao", "essenciais"].forEach(function (k) { erro("e_p2_" + k, v.erros[k]); });
    return v;
  }
  function pintarP2Fb() {
    var v = validarP2(false), p2 = E().p2, nome = publicoNome();
    $("p2fb").innerHTML = bloco({ tipo: v.avisos.length ? "hipotese" : "fato", titulo: "Seu hóspede prioritário: " + nome,
      resultado: "Ocasião: " + p2.ocasiao + ". " + p2.pessoas + " pessoa(s). Essenciais: " + arr("p2.essenciais").map(P.nomeCarac).join(", ") + ".",
      significado: "A partir de agora, a primeira foto, o título e as melhorias devem responder à necessidade desse hóspede: " + p2.necessidade + ".",
      atencao: v.avisos.length ? v.avisos.join(" ") : "Os essenciais escolhidos existem no imóvel. A objeção principal é: " + p2.objecao + ".",
      fazer: "Deixe a resposta à objeção visível no anúncio, em foto ou na primeira linha da descrição.",
      verificar: "Se as próximas mensagens de interessados ainda trazem essa mesma dúvida." });
    $("p2resumo").innerHTML = [["Perfil", nome], ["Necessidade", p2.necessidade], ["Objeção principal", p2.objecao]].map(function (x) { return '<p style="margin:10px 0 0"><span class="small" style="display:block;letter-spacing:.12em;text-transform:uppercase">' + x[0] + '</span><span style="color:var(--creme)">' + esc(x[1]) + '</span></p>'; }).join("");
  }

  /* ================= PILAR 3 ================= */
  function montarP3() {
    $("p3difs").innerHTML = [0, 1, 2, 3, 4, 5].map(function (i) {
      return '<div class="linha-dif"><div class="small" style="letter-spacing:.14em;text-transform:uppercase;color:var(--champanhe)">Diferencial ' + (i + 1) + (i > 1 ? " · opcional" : "") + '</div>' +
        '<label class="campo"><span class="rot">Característica</span><input type="text" data-k="p3.dif.' + i + '.caracteristica" placeholder="Ex.: Ofurô com vista para o vale"></label>' +
        '<label class="campo"><span class="rot">Benefício para o hóspede</span><input type="text" data-k="p3.dif.' + i + '.beneficio" placeholder="Ex.: relaxar a dois ao entardecer"></label>' +
        '<label class="semdado"><input type="checkbox" data-k="p3.dif.' + i + '.verdadeiro"> É verdade e dá para mostrar em foto ou descrição</label></div>';
    }).join("");
    $("p3trazer").addEventListener("click", function () {
      var marc = arr("p2.caracs").map(P.nomeCarac), i = 0;
      marc.forEach(function (nome) { while (i < 6 && get("p3.dif." + i + ".caracteristica")) i++; if (i < 6 && !difs().some(function (d) { return d.caracteristica === nome; })) { set("p3.dif." + i + ".caracteristica", nome); i++; } });
      preencher($("p3difs")); A().salvar();
    });
    $("p3usar").addEventListener("click", function () { set("p3.proposta", sugestaoP3()); preencher($("p3usar").closest(".tela")); A().salvar(); pintarChecksProposta(); });
  }
  function ctxP3() { return { hospedagem: (A().estado.perfil || {}).nome, publicoNome: publicoNome(), necessidade: get("p2.necessidade"), diferenciais: difs() }; }
  function sugestaoP3() { return P.montarProposta(ctxP3()); }
  function pintarChecksProposta() { var av = P.avaliarProposta(proposta(), ctxP3()); $("p3checks").innerHTML = proposta() ? checksHtml(av) : '<li>Escreva a sua versão para ver a avaliação.</li>'; return av; }
  function validarP3(n, mostrar) {
    if (n === 16) { var d = difs(), ver = d.filter(function (x) { return x.verdadeiro; });
      var msg = !d.length ? "Escreva ao menos um diferencial." : (!ver.length ? "Confirme ao menos um diferencial como verdadeiro." : (d.some(function (x) { return !x.beneficio || !String(x.beneficio).trim(); }) ? "Escreva o benefício de cada diferencial." : ""));
      if (mostrar) erro("e_p3_difs", msg); return !msg; }
    if (n === 17) { var m = proposta().length < 40 ? "Escreva a proposta com pelo menos 40 caracteres." : ""; if (mostrar) erro("e_p3_proposta", m); return !m; }
    return true;
  }
  function pintarP3Fb() {
    var av = P.avaliarProposta(proposta(), ctxP3()), falhas = av.checks.filter(function (c) { return !c.ok; });
    $("p3fb").innerHTML = bloco({ tipo: falhas.length ? "hipotese" : "fato", titulo: "Sua proposta passou em " + av.aprovados + " de " + av.total + " critérios",
      resultado: av.checks.map(function (c) { return (c.ok ? "✓ " : "✗ ") + c.txt; }).join(" "),
      significado: "Uma proposta clara diz para quem é, o que é diferente e por que isso importa para o hóspede.",
      atencao: falhas.length ? "Revise: " + falhas.map(function (c) { return c.txt; }).join(" ") : "Todos os critérios foram atendidos. Confira se a frase soa como você fala com o hóspede.",
      fazer: "Use esta frase como primeira linha da descrição e como guia para escolher a primeira foto.",
      verificar: "Consultas por visualização depois de publicar a nova descrição." });
    $("p3final").textContent = proposta();
  }

  /* ================= PILAR 4 ================= */
  function montarP4() {
    $("p4titulos").innerHTML = [0, 1, 2].map(function (i) { return '<label class="campo"><span class="rot">Título ' + (i + 1) + '</span><input type="text" data-k="p4.t' + i + '" maxlength="80" placeholder="Até 50 caracteres"><span class="cont" id="p4c' + i + '"></span></label><ul class="checks" id="p4ct' + i + '"></ul>'; }).join("");
    $("p4rascunho").addEventListener("click", function () {
      var p2 = E().p2, d = difs().filter(function (x) { return x.verdadeiro; });
      var txt = (proposta() || "[Sua proposta de valor]") + "\n\nPara quem é: " + (publicoNome() || "[seu hóspede]").toLowerCase() + (p2.ocasiao ? ", em " + p2.ocasiao : "") + ".\n\nO que você vai encontrar:\n" +
        (d.length ? d.map(function (x) { return "• " + x.caracteristica + (x.beneficio ? ": " + x.beneficio : ""); }).join("\n") : "• [seus diferenciais]") +
        "\n\nChegada e acesso: [explique o caminho, o estacionamento e como é o check-in].\n\nRegras da casa: [horário de silêncio, número de hóspedes, pets, festas].";
      set("p4.descNova", txt); preencher($("p4rascunho").closest(".tela")); A().salvar(); pintarChecksAnuncio();
    });
  }
  function pintarChecksAnuncio() {
    var ctx = ctxAnuncio();
    if ($("p4checkTit")) $("p4checkTit").innerHTML = get("p4.tituloAtual") ? checksHtml(P.avaliarTitulo(get("p4.tituloAtual"), ctx)) : "";
    if ($("p4checkDesc")) $("p4checkDesc").innerHTML = get("p4.descAtual") ? checksHtml(P.avaliarDescricao(get("p4.descAtual"), ctx)) : "";
    [0, 1, 2].forEach(function (i) { var t = get("p4.t" + i) || "", c = $("p4c" + i), l = $("p4ct" + i); if (!c) return;
      c.textContent = t.length + "/" + P.LIMITE_TITULO; c.className = "cont" + (t.length > P.LIMITE_TITULO ? " estoura" : "");
      l.innerHTML = t ? checksHtml(P.avaliarTitulo(t, ctx)) : ""; });
    var dn = get("p4.descNova") || "";
    if ($("p4checkNova")) $("p4checkNova").innerHTML = dn ? checksHtml(P.avaliarDescricao(dn, ctx), [{ ok: dn.indexOf("[") < 0, txt: dn.indexOf("[") < 0 ? "Sem trechos para completar." : "Complete os trechos entre colchetes." }]) : "";
  }
  function validarP4(n, mostrar) {
    if (n === 22) { var ts = [0, 1, 2].map(function (i) { return (get("p4.t" + i) || "").trim(); }).filter(Boolean), dn = get("p4.descNova") || "";
      var m = !ts.length ? "Escreva ao menos um título." : (ts.some(function (t) { return t.length > P.LIMITE_TITULO; }) ? "Há título com mais de " + P.LIMITE_TITULO + " caracteres." : (dn.trim().length < 100 ? "Escreva a nova descrição (pelo menos 100 caracteres)." : (dn.indexOf("[") >= 0 ? "Complete os trechos entre colchetes na descrição." : "")));
      if (mostrar) erro("e_p4", m); return !m; }
    if (n === 23) { var m2 = tituloFinal() ? "" : "Escolha o título final."; if (mostrar) erro("e_p4_final", m2); return !m2; }
    return true;
  }
  function pintarP4Escolha() {
    var ctx = ctxAnuncio();
    $("p4escolha").innerHTML = [0, 1, 2].map(function (i) { var t = (get("p4.t" + i) || "").trim(); if (!t) return ""; var av = P.avaliarTitulo(t, ctx);
      return '<label class="opcao"><input type="radio" name="p4final" data-k="p4.final" value="' + i + '"><span><b>' + esc(t) + '</b><small>' + av.aprovados + ' de ' + av.total + ' critérios · ' + t.length + ' caracteres</small></span></label>'; }).join("");
    preencher($("p4escolha")); pintarP4Fb();
  }
  function pintarP4Fb() {
    var t = tituloFinal(); if (!t) { $("p4fb").innerHTML = ""; return; }
    var av = P.avaliarTitulo(t, ctxAnuncio()), antes = get("p4.tituloAtual") ? P.avaliarTitulo(get("p4.tituloAtual"), ctxAnuncio()) : null;
    $("p4fb").innerHTML = bloco({ tipo: "fato", titulo: "Título escolhido",
      resultado: "\"" + t + "\": " + av.aprovados + " de " + av.total + " critérios" + (antes ? " (o título atual passava em " + antes.aprovados + ")" : "") + ".",
      significado: "Os critérios verificam clareza e fidelidade ao que você informou. Eles não preveem cliques: só o teste mostra o efeito.",
      atencao: "Publique primeiro o título e, uma semana depois, a descrição. Mudando um de cada vez, você sabe o que funcionou.",
      fazer: "Anote a data em que publicar o novo título.", verificar: "Visualizações e consultas por visualização nas duas semanas seguintes, comparadas com as anteriores." });
  }

  /* ================= PILAR 5 ================= */
  var CAMPOS5 = [["receita", "Receita de hospedagem no período (R$)", "Do Pilar 1: noites ocupadas × diária efetiva.", true], ["noites", "Noites ocupadas", "Do Pilar 1.", false], ["reservas", "Reservas no período", "Do Pilar 1.", false],
    ["taxaPlataforma", "Taxa da plataforma (%)", "A comissão que a plataforma desconta de você. Veja no extrato de pagamentos.", true], ["impostos", "Impostos sobre a receita (%)", "Opcional. Pergunte ao seu contador.", true],
    ["limpezaPorReserva", "Custo de limpeza por reserva (R$)", "O que você paga por limpeza, não o que cobra do hóspede.", true], ["variavelPorNoite", "Outros custos por noite ocupada (R$)", "Lavanderia, amenities, energia e gás extras, café da manhã.", true],
    ["fixosPeriodo", "Custos fixos do período (R$)", "Condomínio, IPTU, internet, manutenção, contador. Proporcional ao período.", true]];
  function montarP5() {
    $("p5campos").innerHTML = CAMPOS5.map(function (c) { return '<label class="campo"><span class="rot">' + c[1] + '</span><span class="ajuda">' + c[2] + '</span><input type="text" inputmode="' + (c[3] ? "decimal" : "numeric") + '" data-k="p5.' + c[0] + '" placeholder="0"><span class="msg-erro" id="e_p5_' + c[0] + '"></span></label>'; }).join("");
  }
  function prefillP5() {
    var r = A().calcular();
    if (r.valido) {
      if (!get("p5.receita") && r.receita != null) set("p5.receita", String(Math.round(r.receita * 100) / 100).replace(".", ","));
      if (!get("p5.noites") && r.ocupadas != null) set("p5.noites", String(r.ocupadas));
      if (!get("p5.reservas") && r.reservas != null) set("p5.reservas", String(r.reservas));
    }
    preencher($("p5campos"));
  }
  function mostrarErrosP5(f) { CAMPOS5.forEach(function (c) { erro("e_p5_" + c[0], f.erros[c[0]]); }); var n = Object.keys(f.erros).length; $("p5erros").hidden = !n; if (n) $("p5erros").textContent = n + " campo(s) precisam de correção."; }
  function pintarP5Calc() {
    var f = P.financeiro(get("p5") || {});
    if (!f.valido) { $("p5calc").innerHTML = '<div class="cartao"><span class="etq pendencia">Pendência</span><p>Corrija os custos na tela anterior.</p></div>'; return; }
    $("p5calc").innerHTML = '<div class="cartao"><span class="etq fato">Estimativa</span><div class="small">Margem de contribuição</div><div class="numero">' + brl(f.margem).replace("R$ ", "<small>R$ </small>") + '</div>' +
      '<div class="formula">' + brl(f.receita) + ' − taxas ' + brl(f.taxas) + ' − impostos ' + brl(f.impostos) + ' − variáveis ' + brl(f.variaveis) + '</div>' +
      '<div class="linhas"><div><span>Margem por noite</span><span>' + brl(f.margemPorNoite) + '</span></div><div><span>Custos fixos do período</span><span>' + brl(f.fixos) + '</span></div>' +
      '<div><span>Resultado operacional simplificado</span><span>' + brl(f.resultado) + '</span></div>' + (f.equilibrioNoites ? '<div><span>Noites para cobrir os fixos</span><span>' + f.equilibrioNoites + '</span></div>' : '') + '</div></div>' +
      '<div class="cartao"><span class="etq fato">Fato</span><div class="small">Custos, do maior para o menor</div><div class="linhas">' + f.itens.map(function (i) { return '<div><span>' + esc(i.nome) + '</span><span>' + brl(i.valor) + ' · ' + pct(i.pctReceita) + '</span></div>'; }).join("") + '</div></div>' +
      '<h3>Premissas</h3><ul class="premissas">' + f.premissas.map(function (p) { return '<li>' + esc(p) + '</li>'; }).join("") + '</ul><h3>O que não entrou</h3><ul class="premissas">' + f.foraDoCalculo.map(function (p) { return '<li>' + esc(p) + '</li>'; }).join("") + '</ul>';
    pintarSim();
  }
  function pintarSim() {
    var f = P.financeiro(get("p5") || {}), s = P.simular(f, get("p5.simDiaria"), get("p5.simNoites"));
    if (!$("p5sim")) return;
    $("p5sim").innerHTML = !s ? '<p class="small">Preencha a diária e as noites simuladas.</p>' :
      '<div class="cartao"><span class="etq hipotese">Simulação</span><div class="linhas"><div><span>Receita simulada</span><span>' + brl(s.receita) + '</span></div><div><span>Reservas estimadas</span><span>' + s.reservas + '</span></div><div><span>Margem de contribuição</span><span>' + brl(s.margem) + '</span></div><div><span>Resultado operacional simplificado</span><span>' + brl(s.resultado) + '</span></div><div><span>Diferença para o atual</span><span>' + (s.resultado - f.resultado >= 0 ? "+" : "") + brl(s.resultado - f.resultado) + '</span></div></div><p class="formula">Supõe ' + (Math.round(s.estadiaMedia * 10) / 10).toLocaleString("pt-BR") + ' noites por reserva e os mesmos custos por noite. Não prevê se essa quantidade de noites será vendida.</p></div>';
  }

  /* ================= PILAR 6 ================= */
  var ORDEM_M = [];
  function montarP6() {
    $("p6exemplos").innerHTML = P.ETAPAS.map(function (e) { var ms = P.MELHORIAS.filter(function (m) { return m[0] === e[0]; });
      return '<div class="cartao"><div class="small" style="letter-spacing:.14em;text-transform:uppercase;color:var(--champanhe)">' + esc(e[1]) + ' · ' + esc(e[2]) + '</div><ul class="premissas">' + ms.map(function (m) { return '<li>' + esc(m[1]) + '</li>'; }).join("") + '</ul></div>'; }).join("");
    $("p6auditoria").innerHTML = P.ETAPAS.map(function (e) { var nm = "p6a_" + e[0];
      return '<div class="linha-dif"><b style="color:var(--creme);font-weight:600">' + esc(e[1]) + '</b> <span class="small">· ' + esc(e[2]) + '</span><div class="opcoes" style="grid-template-columns:repeat(3,minmax(0,1fr))">' +
        [["funciona", "Funciona"], ["medio", "Mais ou menos"], ["falha", "Falha"]].map(function (o) { return '<label class="opcao" style="grid-template-columns:auto 1fr;padding:10px"><input type="radio" name="' + nm + '" data-k="p6.aud.' + e[0] + '" value="' + o[0] + '"><span style="font-size:13px">' + o[1] + '</span></label>'; }).join("") + '</div></div>'; }).join("");
  }
  function pintarP6Melhorias() {
    var frag = {}; P.ETAPAS.forEach(function (e) { frag[e[0]] = get("p6.aud." + e[0]); });
    ORDEM_M = P.MELHORIAS.map(function (m, i) { return { i: i, etapa: m[0], texto: m[1], peso: frag[m[0]] === "falha" ? 0 : (frag[m[0]] === "medio" ? 1 : 2) }; }).sort(function (a, b) { return a.peso - b.peso || a.i - b.i; });
    var nomeEt = {}; P.ETAPAS.forEach(function (e) { nomeEt[e[0]] = e[1]; });
    var sel = function (k, rot) { return '<label>' + rot + '<select data-k="' + k + '"><option value="">–</option><option value="1">1 · baixo</option><option value="2">2</option><option value="3">3 · alto</option></select></label>'; };
    $("p6melhorias").innerHTML = ORDEM_M.map(function (m) { var b = "p6.m." + m.i;
      return '<div class="item-mel"><label><input type="checkbox" data-k="' + b + '.sel"><span>' + esc(m.texto) + '<small>' + esc(nomeEt[m.etapa]) + (m.peso === 0 ? " · etapa com falha" : "") + '</small></span></label><div class="mini">' + sel(b + ".impacto", "Impacto") + sel(b + ".custo", "Custo") + sel(b + ".esforco", "Esforço") + '</div></div>'; }).join("");
    preencher($("p6melhorias"));
  }
  function melhoriasEscolhidas() {
    var l = P.MELHORIAS.map(function (m, i) { var x = get("p6.m." + i) || {}; return x.sel ? { texto: m[1], etapa: m[0], impacto: x.impacto, custo: x.custo, esforco: x.esforco } : null; }).filter(Boolean);
    var o = get("p6.outra") || {}; if (o.texto && String(o.texto).trim()) l.push({ texto: String(o.texto).trim(), etapa: "outra", impacto: o.impacto, custo: o.custo, esforco: o.esforco });
    return l;
  }
  function validarP6(n, mostrar) {
    if (n === 31) { var falta = P.ETAPAS.filter(function (e) { return !get("p6.aud." + e[0]); }); var m = falta.length ? "Avalie todas as etapas. Faltam: " + falta.map(function (e) { return e[1]; }).join(", ") + "." : ""; if (mostrar) erro("e_p6_aud", m); return !m; }
    if (n === 32) { var es = melhoriasEscolhidas(); var m2 = !es.length ? "Escolha ao menos uma melhoria." : (es.some(function (x) { return P.prioridade(x.impacto, x.custo, x.esforco) == null; }) ? "Dê nota de impacto, custo e esforço para cada melhoria escolhida." : ""); if (mostrar) erro("e_p6_mel", m2); return !m2; }
    return true;
  }
  function pintarP6Fb() {
    var rank = P.rankMelhorias(melhoriasEscolhidas()), frageis = P.etapasFrageis(get("p6.aud") || {});
    $("p6fb").innerHTML = bloco({ tipo: frageis.length ? "hipotese" : "fato", titulo: "Sua jornada do hóspede",
      resultado: frageis.length ? "Etapas que você marcou com falha: " + frageis.join(", ") + "." : "Você não marcou nenhuma etapa com falha.",
      significado: "As melhorias foram ordenadas pela prioridade que você deu (impacto × 2 − custo − esforço).",
      atencao: rank.length ? "A primeira da lista é: " + rank[0].texto + " (" + rank[0].pontos + " pontos)." : "Nenhuma melhoria escolhida.",
      fazer: "Comece pela primeira da lista e só passe para a próxima quando ela estiver funcionando.",
      verificar: "O que os hóspedes comentam nas avaliações e mensagens sobre essa etapa." });
    $("p6lista").innerHTML = rank.map(function (m) { return '<li>' + esc(m.texto) + ' <span class="small">· ' + m.pontos + ' pontos</span></li>'; }).join("");
  }

  /* ================= PILAR 7 ================= */
  function acoesBase() {
    var l = [], fb = A().feedback(), h = fb.filter(function (b) { return b.tipo === "hipotese" || b.id === "funil"; })[0];
    if (h && h.fazer && !/^Volte e informe/.test(h.fazer)) { var ind = { V0: "Visualizações", A: "Consultas por visualização", B: "Conversão de consultas em reservas" }[h.id] || (h.verificar || "").split(/ no | nos /)[0].replace(/\.$/, "");
      if (!ind || /^Os mesmos/.test(ind)) ind = "Visualizações, consultas e reservas";
      l.push({ id: "p1", texto: h.fazer, origem: "Pilar 1", indicador: ind }); }
    if (tituloFinal()) l.push({ id: "p4t", texto: "Publicar o novo título: " + tituloFinal(), origem: "Pilar 4", indicador: "Consultas por visualização" });
    if ((get("p4.descNova") || "").trim()) l.push({ id: "p4d", texto: "Publicar a nova descrição", origem: "Pilar 4", indicador: "Consultas por visualização" });
    var f = P.financeiro(get("p5") || {}); if (f.valido) { var ff = P.feedbackFinanceiro(f)[0]; l.push({ id: "p5", texto: ff.fazer, origem: "Pilar 5", indicador: "Margem por noite" }); }
    P.rankMelhorias(melhoriasEscolhidas()).forEach(function (m, i) { l.push({ id: "p6_" + i + "_" + m.texto.normalize("NFD").replace(/[^A-Za-z0-9]/g, "").slice(0, 12), texto: m.texto, origem: "Pilar 6", indicador: "Avaliações dos hóspedes" }); });
    var ex = (get("p7.extra") || "").trim(); if (ex) l.push({ id: "extra", texto: ex, origem: "Você", indicador: null });
    return l.map(function (a) { var s = (get("p7.a") || {})[a.id] || {}; return Object.assign(a, { impacto: s.impacto || "", esforco: s.esforco || "", selecionada: !!s.sel, semana: s.semana || "", quadrante: P.quadrante(s.impacto, s.esforco) }); });
  }
  function kA(id, campo) { return "p7.a." + id + "." + campo; }
  function pintarP7Acoes() {
    var l = acoesBase();
    $("p7acoes").innerHTML = l.length ? l.map(function (a) {
      var r = function (campo, rot) { return '<div><span class="small">' + rot + '</span><div class="opcoes" style="grid-template-columns:1fr 1fr;margin-top:4px">' + ["alto", "baixo"].map(function (v) { return '<label class="opcao" style="padding:8px;grid-template-columns:auto 1fr"><input type="radio" name="' + esc(a.id) + campo + '" data-k="' + kA(a.id, campo) + '" value="' + v + '"><span style="font-size:13px">' + v[0].toUpperCase() + v.slice(1) + '</span></label>'; }).join("") + '</div></div>'; };
      return '<div class="item-mel"><span style="color:var(--creme)">' + esc(a.texto) + '<small style="display:block;color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.06em">' + esc(a.origem) + '</small></span><div class="dupla" style="margin-top:8px">' + r("impacto", "Impacto esperado") + r("esforco", "Esforço") + '</div></div>'; }).join("")
      : '<p class="small">Ainda não há ações dos pilares anteriores. Complete-os ou escreva uma ação abaixo.</p>';
    preencher($("p7acoes")); pintarMatriz();
  }
  function pintarMatriz() {
    var l = acoesBase(), Q = ["Fazer primeiro", "Planejar", "Encaixar", "Deixar para depois"];
    if (!$("p7matriz")) return;
    $("p7matriz").innerHTML = Q.map(function (q) { var it = l.filter(function (a) { return a.quadrante === q; }); return '<div><b>' + q + '</b><ul>' + it.map(function (a) { return '<li>' + esc(a.texto) + '</li>'; }).join("") + '</ul></div>'; }).join("");
  }
  function pintarP7Sel() {
    var l = acoesBase().slice().sort(function (a, b) { var o = { "Fazer primeiro": 0, "Planejar": 1, "Encaixar": 2, "Deixar para depois": 3 }; return (o[a.quadrante] || 0) - (o[b.quadrante] || 0); });
    $("p7selecao").innerHTML = l.map(function (a) { return '<div class="item-mel"><label><input type="checkbox" data-k="' + kA(a.id, "sel") + '"><span>' + esc(a.texto) + '<small>' + esc(a.quadrante || "") + ' · ' + esc(a.origem) + '</small></span></label></div>'; }).join("");
    preencher($("p7selecao"));
  }
  function pintarP7Semanas() {
    var l = acoesBase().filter(function (a) { return a.selecionada; });
    $("p7semanas").innerHTML = l.map(function (a) { return '<label class="campo"><span class="rot" style="font-weight:500">' + esc(a.texto) + '</span><select data-k="' + kA(a.id, "semana") + '"><option value="">Escolha a semana</option><option value="1">Semana 1 · dias 1 a 7</option><option value="2">Semana 2 · dias 8 a 14</option><option value="3">Semana 3 · dias 15 a 21</option><option value="4">Semana 4 · dias 22 a 30</option></select></label>'; }).join("");
    preencher($("p7semanas")); pintarAvisosCrono();
  }
  function pintarAvisosCrono() { var v = P.validarCronograma(acoesBase()); if ($("p7avisos")) $("p7avisos").innerHTML = v.erros.concat(v.avisos).map(function (a) { return '<div class="aviso">' + esc(a) + '</div>'; }).join(""); return v; }
  function indicadores() {
    var base = ["Taxa de ocupação", "Consultas por visualização", "Conversão de consultas em reservas", "Margem por noite"];
    P.validarCronograma(acoesBase()).selecionadas.forEach(function (a) { if (a.indicador && base.indexOf(a.indicador) < 0) base.push(a.indicador); });
    return base;
  }
  function pintarP7Plano() {
    var v = P.validarCronograma(acoesBase());
    $("p7plano").innerHTML = [1, 2, 3, 4].map(function (s) { var it = v.selecionadas.filter(function (a) { return +a.semana === s; }); var dias = ["1 a 7", "8 a 14", "15 a 21", "22 a 30"][s - 1];
      return '<div class="s"><b>Semana ' + s + '</b> <span class="small">· dias ' + dias + '</span><ul>' + (it.length ? it.map(function (a) { return '<li>' + esc(a.texto) + '</li>'; }).join("") : '<li class="small">Sem ações: use para medir.</li>') + '</ul></div>'; }).join("");
    $("p7indicadores").innerHTML = indicadores().map(function (i) { return '<li>' + esc(i) + '</li>'; }).join("");
    $("p7fb").innerHTML = bloco({ tipo: v.avisos.length ? "hipotese" : "fato", titulo: "Seu plano tem " + v.selecionadas.length + " ação(ões) em quatro semanas",
      resultado: [1, 2, 3, 4].map(function (s) { return "Semana " + s + ": " + v.selecionadas.filter(function (a) { return +a.semana === s; }).length; }).join(" · ") + ".",
      significado: "Cada ação está ligada a um indicador. Assim, no fim do mês, você consegue ver o que mudou.",
      atencao: v.avisos.length ? v.avisos.join(" ") : "Nenhum conflito: cada semana mexe em indicadores diferentes.",
      fazer: "Anote a data de cada mudança assim que fizer.", verificar: "Refaça o Raio-X ao fim dos 30 dias, com um período de mesma duração." });
  }
  function validarP7(n, mostrar) {
    var l = acoesBase();
    if (n === 35) { var m = !l.length ? "Inclua ao menos uma ação." : (l.some(function (a) { return !a.quadrante; }) ? "Marque impacto e esforço de todas as ações." : ""); if (mostrar) erro("e_p7_matriz", m); return !m; }
    if (n === 36) { var s = l.filter(function (a) { return a.selecionada; }).length; var m2 = !s ? "Selecione ao menos uma ação." : (s > 8 ? "Selecione no máximo 8 ações." : ""); if (mostrar) erro("e_p7_sel", m2); return !m2; }
    if (n === 37) { var v = pintarAvisosCrono(); return v.valido; }
    return true;
  }

  /* ================= CONCLUSÃO ================= */
  function status() {
    var r = A().calcular(), f = P.financeiro(get("p5") || {});
    return [
      { n: 1, nome: "Raio-X da Oferta", tela: 6, ok: r.valido && r.ocupacao != null },
      { n: 2, nome: "Perfil Prioritário de Hóspede", tela: 12, ok: validarP2(false).valido },
      { n: 3, nome: "Proposta de Valor", tela: 17, ok: proposta().length >= 40 },
      { n: 4, nome: "Anúncio Revisado", tela: 22, ok: !!tituloFinal() && (get("p4.descNova") || "").trim().length >= 100 },
      { n: 5, nome: "Diagnóstico Financeiro Inicial", tela: 26, ok: f.valido },
      { n: 6, nome: "Plano de Melhoria da Experiência", tela: 32, ok: validarP6(32, false) },
      { n: 7, nome: "Plano de Ação de 30 Dias", tela: 37, ok: P.validarCronograma(acoesBase()).valido }
    ];
  }
  function pintar39() {
    $("painel7").innerHTML = status().map(function (s) { return '<button type="button" data-sum="' + s.tela + '"><b>' + s.n + '</b><span>' + esc(s.nome) + '<small>' + (s.ok ? "Concluído" : "Faltam respostas") + '</small></span><span class="st ' + (s.ok ? "ok" : "pend") + '">' + (s.ok ? "Pronto" : "Pendente") + '</span></button>'; }).join("");
  }

  /* Modelo único do dossiê: usado na pré-visualização (tela 40) e no PDF. */
  function modelo() {
    var e = E(), perf = A().estado.perfil || {}, r = A().calcular(), fb1 = A().feedback(), f = P.financeiro(get("p5") || {}), st = status(), pend = [];
    var S = [];
    var dif = { visualizacoes: "Pouca gente vê o anúncio", semConsultas: "Veem, mas não perguntam", semReservas: "Perguntam, mas não reservam", dinheiro: "Reservas, mas sobra pouco dinheiro", naosei: "Não sabia dizer" }[perf.dificuldade];
    S.push({ t: "Identificação e características da hospedagem", tela: 3, itens: [{ k: "Dados fornecidos" },
      ["Hospedagem", perf.nome], ["Tipo", perf.tipo], ["Cidade ou região", perf.cidade], ["Capacidade", perf.capacidade ? perf.capacidade + " hóspedes" : ""], ["Unidades", perf.unidades],
      ["Principal dificuldade", dif], ["Características", arr("p2.caracs").map(P.nomeCarac).join(", ")], ["Outras comodidades", e.p2.outras]] });
    var r1 = [{ k: "Dados fornecidos" }, ["Período", r.dias ? r.dias + " dias" : ""], ["Noites disponíveis", r.disponiveis], ["Noites ocupadas", r.ocupadas], ["Diária média efetiva", r.diaria != null ? brl(r.diaria) : ""],
      ["Visualizações", r.visualizacoes], ["Consultas", r.consultas], ["Reservas", r.reservas], { k: "Estimativas" },
      ["Taxa de ocupação", r.ocupacao != null ? pct(r.ocupacao) : ""], ["Receita estimada", r.receita != null ? brl(r.receita) : ""], ["Consultas por visualização", r.taxaConsulta != null ? pct(r.taxaConsulta) : ""], ["Conversão em reservas", r.taxaReserva != null ? pct(r.taxaReserva) : ""], { k: "Recomendações" }];
    fb1.forEach(function (b) { r1.push({ p: b.titulo + ": " + b.fazer }); });
    S.push({ t: "Diagnóstico inicial e principais indicadores", tela: 6, itens: r1 });
    S.push({ t: "Público prioritário", tela: 12, itens: [{ k: "Suas escolhas" }, ["Perfil", publicoNome()], ["Ocasião", e.p2.ocasiao], ["Pessoas", e.p2.pessoas], ["Necessidade", e.p2.necessidade], ["Objeção principal", e.p2.objecao], ["Essenciais", arr("p2.essenciais").map(P.nomeCarac).join(", ")]] });
    S.push({ t: "Proposta de valor", tela: 17, itens: [{ k: "Sua proposta" }, { p: proposta() || "" }, { k: "Diferenciais confirmados" }].concat(difs().filter(function (d) { return d.verdadeiro; }).map(function (d) { return { li: d.caracteristica + (d.beneficio ? ": " + d.beneficio : "") }; })) });
    S.push({ t: "Título e descrição revisados", tela: 22, itens: [{ k: "Antes" }, ["Título atual", e.p4.tituloAtual], { k: "Depois" }, ["Título escolhido", tituloFinal()], { p: e.p4.descNova || "" }] });
    var s5 = [{ k: "Dados fornecidos" }];
    if (f.valido) {
      s5 = s5.concat([["Receita do período", brl(f.receita)], ["Noites ocupadas", f.noites], ["Reservas", f.reservas], ["Custos fixos do período", brl(f.fixos)], { k: "Estimativas" },
        ["Taxa da plataforma", brl(f.taxas)], ["Impostos", brl(f.impostos)], ["Custos variáveis", brl(f.variaveis)], ["Margem de contribuição", brl(f.margem)], ["Margem por noite", brl(f.margemPorNoite)], ["Resultado operacional simplificado", brl(f.resultado)]]);
      if (f.equilibrioNoites) s5.push(["Noites para cobrir os fixos", f.equilibrioNoites]);
      var sim = P.simular(f, get("p5.simDiaria"), get("p5.simNoites")); if (sim) s5.push({ k: "Simulação" }, ["Diária × noites", brl(sim.diaria) + " × " + sim.noites], ["Resultado simulado", brl(sim.resultado)]);
      s5.push({ k: "Recomendação" }, { p: P.feedbackFinanceiro(f)[0].fazer }, { p: "Premissas: " + f.premissas.join(" ") + " " + f.foraDoCalculo.join(" "), pequeno: true });
    } else s5.push({ p: "" });
    S.push({ t: "Diagnóstico financeiro e simulações", tela: 26, itens: s5 });
    var rank = P.rankMelhorias(melhoriasEscolhidas());
    S.push({ t: "Melhorias propostas para a experiência do hóspede", tela: 32, itens: [{ k: "Etapas com falha" }, { p: P.etapasFrageis(get("p6.aud") || {}).join(", ") || "Nenhuma marcada" }, { k: "Recomendações, por prioridade" }].concat(rank.map(function (m) { return { li: m.texto + " (" + m.pontos + " pontos)" }; })).concat(rank.length ? [] : [{ p: "" }]) });
    var v7 = P.validarCronograma(acoesBase()), s7 = [{ k: "Recomendações" }];
    [1, 2, 3, 4].forEach(function (s) { var it = v7.selecionadas.filter(function (a) { return +a.semana === s; }); if (it.length) { s7.push({ k: "Semana " + s }); it.forEach(function (a) { s7.push({ li: a.texto }); }); } });
    if (!v7.selecionadas.length) s7.push({ p: "" });
    S.push({ t: "Plano de ação de 30 dias", tela: 37, itens: s7 });
    S.push({ t: "Indicadores para acompanhar", tela: 38, itens: indicadores().map(function (i) { return { li: i }; }) });
    st.forEach(function (s) { if (!s.ok) pend.push("Pilar " + s.n + " · " + s.nome + ": faltam respostas."); });
    r.pendencias.concat(r.avisos).forEach(function (x) { pend.push(x); });
    v7.avisos.forEach(function (x) { pend.push(x); });
    S.push({ t: "Pendências e informações não verificadas", tela: 39, itens: (pend.length ? pend : ["Nenhuma pendência registrada."]).map(function (x) { return { li: x }; }).concat([{ p: "Todos os números foram informados por você e não foram conferidos com a plataforma.", pequeno: true }]) });
    return { nome: perf.nome || "Minha hospedagem", secoes: S, data: new Date() };
  }
  function pintar40() {
    var m = modelo(), h = '<div class="cab"><span>Zion Hotel Academy | Bruno Chaerk</span><b>Meu Plano de Melhoria do Airbnb</b><span>' + esc(m.nome) + ' · gerado em ' + m.data.toLocaleDateString("pt-BR") + '</span></div>';
    m.secoes.forEach(function (s, i) {
      h += '<h4>' + (i + 1) + '. ' + esc(s.t) + '<button type="button" data-sum="' + s.tela + '">Editar</button></h4>';
      var ul = false;
      s.itens.forEach(function (it) {
        if (it.li != null) { if (!ul) { h += "<ul>"; ul = true; } h += "<li>" + esc(it.li) + "</li>"; return; }
        if (ul) { h += "</ul>"; ul = false; }
        if (Array.isArray(it)) h += '<p><span style="color:#5F5F55">' + esc(it[0]) + ':</span> ' + (it[1] == null || it[1] === "" ? '<span class="pend">não informado</span>' : esc(it[1])) + '</p>';
        else if (it.k) h += '<span class="k">' + esc(it.k) + '</span>';
        else if (it.p != null) h += it.p === "" ? '<p class="pend">Pendente: complete este pilar.</p>' : '<p' + (it.pequeno ? ' style="font-size:12px;color:#5F5F55"' : '') + '>' + esc(it.p).replace(/\n/g, "<br>") + '</p>';
      });
      if (ul) h += "</ul>";
    });
    $("dossie").innerHTML = h;
  }
  function pdf(stEl, previa) {
    if (!window.jspdf) { stEl.textContent = "Não foi possível carregar o gerador de PDF. Verifique a internet e tente de novo."; return; }
    var m = modelo(), doc = new window.jspdf.jsPDF({ unit: "mm", format: "a4", compress: true });
    /* A fonte padrão do PDF (WinAnsi) não tem alguns sinais: troca por equivalentes antes de medir e escrever. */
    var limpar = function (t) { return Array.isArray(t) ? t.map(limpar) : String(t).replace(/\u2212/g, "-").replace(/\u2192/g, "->").replace(/\u2713/g, "ok").replace(/\u2717/g, "x").replace(/[\u2018\u2019]/g, "'").replace(/[\u201C\u201D]/g, '"'); };
    var _text = doc.text.bind(doc), _split = doc.splitTextToSize.bind(doc);
    doc.text = function (t) { var a = Array.prototype.slice.call(arguments); a[0] = limpar(t); return _text.apply(null, a); };
    doc.splitTextToSize = function (t, w, o) { return _split(limpar(t), w, o); };
    var W = 210, M = 18, y = 0, TXT = [27, 33, 23], CINZA = [95, 95, 85], OURO = [150, 124, 62], TERRA = [139, 113, 78], PEND = [155, 44, 31];
    function cabe(h) { if (y + h > 278) { doc.addPage(); y = 22; } }
    function para(t, est, tam, cor) { doc.setFont("helvetica", est || "normal"); doc.setFontSize(tam || 10); doc.setTextColor.apply(doc, cor || TXT); var l = doc.splitTextToSize(String(t), W - 2 * M); cabe(l.length * 4.6 + 1); doc.text(l, M, y); y += l.length * 4.6 + 1.2; }
    doc.setFillColor(4, 6, 5); doc.rect(0, 0, W, 70, "F");
    var logo = document.querySelector(".topo img"); try { doc.addImage(logo.src, "PNG", M, 14, 57, 15, "logo", "FAST"); } catch (e) {}
    doc.setFont("helvetica", "normal"); doc.setFontSize(8); doc.setTextColor(201, 179, 126); doc.text("ZION HOTEL ACADEMY  |  BRUNO CHAERK", M, 42, { charSpace: .5 });
    doc.setFont("times", "normal"); doc.setFontSize(24); doc.setTextColor(254, 245, 240); doc.text("Meu Plano de Melhoria do Airbnb", M, 54);
    doc.setFont("helvetica", "normal"); doc.setFontSize(9); doc.setTextColor(222, 214, 191); doc.text(m.nome + "  ·  " + (previa ? "prévia  ·  " : "") + "gerado em " + m.data.toLocaleDateString("pt-BR") + " às " + m.data.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" }), M, 62);
    y = 82; para("Legenda: DADOS FORNECIDOS = informados por você. ESTIMATIVAS = calculadas a partir dos seus dados. RECOMENDAÇÕES = sugestões de ação ou hipóteses a investigar.", "normal", 8.5, CINZA);
    m.secoes.forEach(function (s, i) {
      cabe(24); y += 3; doc.setFont("times", "normal"); doc.setFontSize(15); doc.setTextColor.apply(doc, TXT); doc.text((i + 1) + ". " + s.t, M, y); y += 2.5; doc.setDrawColor.apply(doc, TERRA); doc.setLineWidth(.3); doc.line(M, y, W - M, y); y += 6;
      s.itens.forEach(function (it) {
        if (it.li != null) { para("•  " + it.li); return; }
        if (Array.isArray(it)) { var val = it[1] == null || it[1] === "" ? "não informado" : String(it[1]); var l = doc.splitTextToSize(val, 95); cabe(5.6 * l.length + 1);
          doc.setFont("helvetica", "normal"); doc.setFontSize(10); doc.setTextColor.apply(doc, CINZA); doc.text(String(it[0]), M, y);
          doc.setFont("helvetica", "bold"); doc.setTextColor.apply(doc, val === "não informado" ? PEND : TXT); doc.text(l, W - M, y, { align: "right" }); y += 5.6 * l.length; return; }
        if (it.k) { cabe(18); y += 1.5; doc.setFont("helvetica", "bold"); doc.setFontSize(7); doc.setTextColor.apply(doc, OURO); doc.text(it.k.toUpperCase(), M, y, { charSpace: .5 }); y += 4.2; return; }
        if (it.p != null) { if (it.p === "") para("Pendente: complete este pilar.", "italic", 10, PEND); else para(it.p, "normal", it.pequeno ? 8.5 : 10, it.pequeno ? CINZA : TXT); }
      });
    });
    var n = doc.getNumberOfPages();
    for (var p = 1; p <= n; p++) { doc.setPage(p); doc.setFont("helvetica", "normal"); doc.setFontSize(7.5); doc.setTextColor(130, 125, 110);
      doc.text("Zion Hotel Academy · Seu Airbnb Está Vazio? · Material educativo. Não garante reservas, ocupação nem faturamento.", M, 289); doc.text(p + "/" + n, W - M, 289, { align: "right" }); }
    var arq = "Meu-Plano-de-Melhoria-" + m.nome.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^A-Za-z0-9]+/g, "-").replace(/^-|-$/g, "") + ".pdf";
    try { doc.save(arq); stEl.textContent = "PDF gerado: " + arq + "."; } catch (e) { stEl.textContent = "Este navegador bloqueou o download. Abra no Chrome ou no Safari."; }
  }

  /* ---------- registro ---------- */
  var VAL = { 12: function (m) { return validarP2(m).valido; }, 16: function (m) { return validarP3(16, m); }, 17: function (m) { return validarP3(17, m); },
    22: function (m) { return validarP4(22, m); }, 23: function (m) { return validarP4(23, m); },
    26: function (m) { var f = P.financeiro(get("p5") || {}); if (m) mostrarErrosP5(f); return f.valido; },
    31: function (m) { return validarP6(31, m); }, 32: function (m) { return validarP6(32, m); },
    35: function (m) { return validarP7(35, m); }, 36: function (m) { return validarP7(36, m); }, 37: function (m) { return validarP7(37, m); } };
  var RENDER = { 12: pintarP2Afinidade, 13: pintarP2Fb, 17: function () { $("p3sugestao").textContent = sugestaoP3(); pintarChecksProposta(); }, 18: pintarP3Fb,
    21: pintarChecksAnuncio, 22: pintarChecksAnuncio, 23: pintarP4Escolha, 26: prefillP5, 27: pintarP5Calc, 28: function () { $("p5fb").innerHTML = P.feedbackFinanceiro(P.financeiro(get("p5") || {})).map(bloco).join(""); },
    32: pintarP6Melhorias, 33: pintarP6Fb, 35: pintarP7Acoes, 36: pintarP7Sel, 37: pintarP7Semanas, 38: pintarP7Plano, 39: pintar39, 40: pintar40 };

  montarP2(); montarP3(); montarP4(); montarP5(); montarP6();
  $("pdfFinal").addEventListener("click", function () { pdf($("statusPdfFinal"), false); });
  window.ZP = { TELAS: TELAS, render: function (n) { if (RENDER[n]) RENDER[n](); preencher(document.querySelector('.tela[data-t="' + n + '"]')); vivo(); },
    validar: function (n) { return VAL[n] ? VAL[n](true) : true; }, aplicar: function () { E(); preencher(document); }, pdf: pdf, modelo: modelo, status: status };
})();

/* Jornada 2 · Gestão · Módulo 7 · Qualidade, reputação e plano de crescimento
   Lógica pura da ficha "O Montador do Plano de Gestão Profissional". Sem DOM: roda no navegador (window.ZQ) e no Node (testes).
   Regra: tudo o que a ficha afirma sai daqui, para ser testado. Nenhuma nota de gestão: só contagens, as regras das fontes
   e aritmética declarada no PLANO (seção 11).
   Fontes: Panorama (Trilha B, G7; Trilha A, Pilar 07 Lançamento); Método Zion 360° Volume 07 (Protocolo da Primeira Avaliação™);
   Jornada do COMO, Etapa 07 (Sistema de Avaliações™, resposta em menos de uma hora), Etapa 09 P13 (Rotina Financeira),
   Etapa 10 P10, P12 e P13 (painel por exceção, Teste de Prontidão, Plano de Saída da Operação™). Mapa de fontes fora do repositório. */
(function (raiz) {
  "use strict";

  var SITUACOES = [
    { v: "abrir", r: "Ainda vou abrir a minha hospedagem", t: "O Plano vira o desenho da gestão antes do primeiro hóspede." },
    { v: "dono", r: "Já opero e quero profissionalizar a gestão", t: "O Plano junta o que você já fez e marca a saída da operação." },
    { v: "operador", r: "Cuido do dia a dia de uma hospedagem de outra pessoa", t: "O Plano vira a sua prestação de contas ao dono." },
  ];
  var SIMNAO = [{ v: "sim", r: "Sim" }, { v: "nao", r: "Não" }];
  var ESCALAS = [{ v: "5", r: "De 0 a 5" }, { v: "10", r: "De 0 a 10" }];
  var DIMENSOES = [
    { v: "limpeza", r: "Limpeza" }, { v: "comunicacao", r: "Comunicação" }, { v: "checkin", r: "Chegada (check-in)" }, { v: "precisao", r: "Fidelidade ao anúncio" },
    { v: "localizacao", r: "Localização" }, { v: "custo", r: "Custo-benefício" }, { v: "conforto", r: "Conforto e estrutura" }, { v: "naosei", r: "O canal não separa por dimensão" },
  ];
  var DIAS = [{ v: "segunda", r: "Segunda-feira" }, { v: "terca", r: "Terça-feira" }, { v: "quarta", r: "Quarta-feira" }, { v: "quinta", r: "Quinta-feira" }, { v: "sexta", r: "Sexta-feira" }, { v: "sabado", r: "Sábado" }, { v: "domingo", r: "Domingo" }];
  var TEMPO_SOBRA = [
    { v: "negocio", r: "Trabalhar sobre o negócio", t: "Preço, marca, base própria de hóspedes e relações: o que as Etapas 05, 07 e 08 pedem e quase nunca recebem." },
    { v: "segunda", r: "Construir a segunda unidade", t: "Só se a conta e o teste permitirem: as quatro condições abaixo." },
    { v: "viver", r: "Simplesmente viver", t: "Uma resposta legítima, e a razão real de muita gente ter começado." },
  ];
  var CONDICOES = [
    { id: "teste", p: "agendar o teste de prontidão", r: "O teste das duas semanas passou", t: "Sem isso, a segunda unidade cria duas operações sem dono." },
    { id: "retirada", r: "A primeira gera resultado depois de pagar a minha retirada", t: "A Folha Única do Módulo 2 responde." },
    { id: "reserva", r: "Existe reserva para a rampa da segunda", t: "Costuma levar de doze a dezoito meses até maturar." },
    { id: "supervisao", r: "Existe quem supervisione as duas", t: "A mesma pessoa ou uma estrutura mínima acima dela." },
  ];
  // As oito páginas do Plano de Gestão Profissional: uma por módulo (a 7 é feita nesta ficha)
  var PAGINAS = [
    { n: 0, slug: "marco-zero", chave: "zion-t2-marco-zero", glob: "ZG", r: "Diagnóstico de Gestão", m: "Marco Zero · O gestor e o diagnóstico" },
    { n: 1, slug: "planejamento", chave: "zion-t2-planejamento", glob: "ZP", r: "Painel de Gestão", m: "Planejamento, metas e indicadores" },
    { n: 2, slug: "financas", chave: "zion-t2-financas", glob: "ZF", r: "Folha Única do Mês", m: "Finanças, fluxo de caixa e fechamento" },
    { n: 3, slug: "preco", chave: "zion-t2-preco", glob: "ZP", r: "Tabela de Preço e Canais", m: "Preço, reservas e distribuição" },
    { n: 4, slug: "marketing", chave: "zion-t2-marketing", glob: "ZM", r: "Marca e Captação", m: "Marketing e vendas" },
    { n: 5, slug: "pessoas", chave: "zion-t2-pessoas", glob: "ZP", r: "Mapa de Pessoas e Alçadas", m: "Pessoas e organização das áreas" },
    { n: 6, slug: "compras", chave: "zion-t2-compras", glob: "ZC", r: "Matriz de Compras e Manutenção", m: "Compras, estoque e manutenção" },
    { n: 7, slug: "qualidade", chave: "zion-t2-qualidade", glob: "ZQ", r: "Qualidade, reputação e plano de crescimento", m: "Qualidade, reputação e plano de crescimento" },
  ];
  // Os seis indicadores da leitura semanal (Etapa 10, Passo 10)
  var INDICADORES = ["Nota das avaliações da semana, e qualquer avaliação abaixo do padrão", "Ocupação da semana contra a projeção", "Tempo médio de resposta a mensagem",
    "Ocorrências registradas: problema durante a estadia, reclamação, manutenção acionada", "Decisões tomadas dentro da alçada, listadas", "Gasto da semana contra o previsto"];
  var MEDIR = ["Ocupação do período contra a projeção", "Nota das avaliações do período contra a média dos três meses anteriores", "Número de contatos por exceção, e se eram de fato exceções",
    "Ocorrências registradas e como foram resolvidas", "Gasto do período contra o previsto"];
  var REGRAS_TESTE = ["Catorze dias corridos, com pelo menos um fim de semana cheio", "Sem atender mensagem de hóspede, sem entrar no painel do canal, sem conferir unidade",
    "Contato apenas pelas quatro exceções do painel", "Sem aviso especial à equipe de que é um teste: a operação roda como roda"];
  var TELAS = ["abertura", "paginas", "nota", "protocolo", "rotina", "prontidao", "resultado"];
  var TITULOS = { paginas: "As páginas que você já fez", nota: "A nota e as avaliações", protocolo: "Resposta às avaliações e padrão mínimo", rotina: "A rotina semanal", prontidao: "O teste de prontidão e o plano de crescimento" };
  var PROXIMO = { t: "Jornada 3 · Operação", d: "o Manual Operacional Personalizado: limpeza, chegada e saída, manutenção e experiência do hóspede com padrão escrito, a parte que mais mexe na nota." };

  // Exemplo didático · dados fictícios (Cabanas do Vale, continuação dos módulos 0 a 6)
  function exemplo() {
    return {
      tela: 0, situacao: "dono", hospedagem: "Cabanas do Vale (exemplo)",
      escala: "5", notaAtual: "4,7", notaMeta: "4,8", prazoMeta: "2027-10-31", avaliacoes: "38", estadias3m: "72", avaliacoes3m: "25",
      dimensao: "limpeza", dimensaoNota: "4,6", concorrentes: "4,6", criticas3m: "7", criticaRepetida: "Ralo do chuveiro com cheiro na cabana 3", repeticoes: "3", tempoResposta: "40",
      pedido: "Avaliações são o que faz uma casa pequena ser encontrada. Se a estadia foi boa, a sua ajudaria muito.",
      naoPedir: "sim",
      respPositiva: "Obrigada pela visita! Que bom que a lareira e o café na varanda marcaram a estadia. Vamos esperar vocês de volta no inverno.",
      respNegativa: "Obrigada por contar. Você tem razão sobre o ralo do chuveiro: trocamos a peça e o ralo entrou no checklist de limpeza de cada troca.",
      regra24: "sim", quemResponde: "Ana (dona)",
      notaMin: "4,7", respostaMax: "60", taxaMin: "40", auditoria: "sim",
      ajuste: "Trocar o sifão do chuveiro da cabana 3 e incluir o ralo no checklist de limpeza", ajustePrazo: "2026-11-30",
      reuniaoDia: "segunda", reuniaoHora: "08:00", painelDia: "segunda", folhaDia: "5", trimestral1: "2027-01-11", anual: "2027-11-08",
      inicioF1: "2026-11-16", semanasF1: "8", semanasF2: "8", inicioTeste: "2027-06-14", responsavel: "Diarista, com o auxiliar de manutenção",
      ocupProjetada: "50", notaMedia3m: "4,7", periodoMedio: "sim", feito: "nao", ocupReal: "", notaPeriodo: "", contatos: "", causaExterna: "",
      tempoSobra: "negocio", tempoSobraTxt: "Duas horas por semana para preço e venda direta (módulos 3 e 4).",
      cond: { teste: "nao", retirada: "sim", reserva: "nao", supervisao: "nao" },
    };
  }
  var EXEMPLO = exemplo();
  function base() {
    return { tela: 0, nome: "", email: "", hospedagem: "", situacao: "", escala: "5", notaAtual: "", notaMeta: "", prazoMeta: "", avaliacoes: "", estadias3m: "", avaliacoes3m: "",
      dimensao: "", dimensaoNota: "", concorrentes: "", criticas3m: "", criticaRepetida: "", repeticoes: "", tempoResposta: "",
      pedido: "", naoPedir: "", respPositiva: "", respNegativa: "", regra24: "", quemResponde: "", notaMin: "", respostaMax: "60", taxaMin: "40", auditoria: "", ajuste: "", ajustePrazo: "",
      reuniaoDia: "", reuniaoHora: "", painelDia: "", folhaDia: "", trimestral1: "", anual: "",
      inicioF1: "", semanasF1: "8", semanasF2: "8", inicioTeste: "", responsavel: "", ocupProjetada: "", notaMedia3m: "", periodoMedio: "", feito: "nao", ocupReal: "", notaPeriodo: "", contatos: "", causaExterna: "",
      tempoSobra: "", tempoSobraTxt: "", cond: { teste: "", retirada: "", reserva: "", supervisao: "" } };
  }
  function completar(S) { var b = base(); S = S || {}; for (var k in b) if (S[k] == null) S[k] = b[k]; var c = S.cond || {}; S.cond = { teste: c.teste || "", retirada: c.retirada || "", reserva: c.reserva || "", supervisao: c.supervisao || "" }; S.tela = +S.tela || 0; return S; }

  // ---------- utilidades ----------
  // Converte "1.234,56", "1234.56", "13.000", 1234 em número; vazio ou inválido vira null (correção do Módulo 1: "13.000" = treze mil)
  function num(v) {
    if (v == null) return null;
    if (typeof v === "number") return isFinite(v) ? v : null;
    var s = String(v).trim(); if (!s) return null;
    s = s.replace(/\s|R\$|%|min/gi, "").replace(/−/g, "-");
    if (/,/.test(s)) s = s.replace(/\./g, "").replace(",", ".");
    else if (/^-?\d{1,3}(\.\d{3})+$/.test(s)) s = s.replace(/\./g, "");
    if (!/^-?\d*\.?\d+$/.test(s)) return null;
    var n = Number(s); return isFinite(n) ? n : null;
  }
  function informado(v) { return v != null && String(v).trim() !== ""; }
  function letras(s) { return String(s || "").replace(/[^A-Za-zÀ-ÿ]/g, "").length; }
  function brl(v) { if (v == null || !isFinite(v)) return "a definir"; var neg = v < 0; var s = Math.abs(v).toFixed(2).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, "."); return (neg ? "−R$ " : "R$ ") + s; }
  function pct(v, d) { if (v == null || !isFinite(v)) return "a definir"; return (v * 100).toFixed(d == null ? 1 : d).replace(".", ",") + "%"; }
  function dec(v, d) { if (v == null || !isFinite(v)) return "a definir"; return v.toFixed(d == null ? 1 : d).replace(".", ","); }
  function notaTxt(v, esc) { if (v == null) return "sem nota"; return dec(v, Math.abs(Math.round(v * 10) - v * 10) < 1e-9 ? 1 : 2) + " de " + esc; }
  function diaUTC(iso) { var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso || "")); if (!m) return null; var t = Date.UTC(+m[1], +m[2] - 1, +m[3]); var d = new Date(t); return d.getUTCMonth() === +m[2] - 1 ? t : null; }
  function somaDias(iso, n) { var t = diaUTC(iso); if (t == null) return null; return new Date(t + n * 864e5).toISOString().slice(0, 10); }
  function difDias(a, b) { var x = diaUTC(a), y = diaUTC(b); if (x == null || y == null) return null; return Math.round((y - x) / 864e5); }
  function somaMeses(iso, k) { var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso || "")); if (!m || diaUTC(iso) == null) return null; var a = +m[1], mes = +m[2] - 1 + k, d = +m[3]; a += Math.floor(mes / 12); mes = ((mes % 12) + 12) % 12; var ult = new Date(Date.UTC(a, mes + 1, 0)).getUTCDate(); return new Date(Date.UTC(a, mes, Math.min(d, ult))).toISOString().slice(0, 10); }
  function br(iso) { if (!iso || diaUTC(iso) == null) return "sem data"; var p = String(iso).split("-"); return p[2] + "/" + p[1] + "/" + p[0]; }
  function diaSemana(iso) { var t = diaUTC(iso); if (t == null) return null; return ["domingo", "segunda", "terca", "quarta", "quinta", "sexta", "sabado"][new Date(t).getUTCDay()]; }
  function nomeDia(v) { var d = DIAS.filter(function (x) { return x.v === v; })[0]; return d ? d.r : ""; }
  function escala(S) { return String(S && S.escala) === "10" ? 10 : 5; }

  // ---------- as páginas anteriores (lidas do mesmo aparelho) ----------
  // estados: { "marco-zero": objeto salvo ou null, ... }. Página presente = a ficha gerou o PDF (campo pdf gravado).
  function paginas(estados) {
    estados = estados || {};
    return PAGINAS.slice(0, 7).map(function (p) {
      var s = estados[p.slug];
      var tem = !!(s && typeof s === "object" && Object.keys(s).length);
      var quando = tem && s.pdf ? String(s.pdf).slice(0, 10) : null;
      return { n: p.n, slug: p.slug, chave: p.chave, r: p.r, m: p.m, estado: !tem ? "falta" : quando ? "pronta" : "andamento", quando: quando, link: "../" + p.slug + "/" };
    });
  }
  function rotuloEstado(p) { return p.estado === "pronta" ? "Pronta · PDF de " + br(p.quando) : p.estado === "andamento" ? "Em andamento · falta chegar ao PDF" : "Página ainda não feita"; }
  // O que vem das páginas anteriores para sugerir respostas nesta ficha
  function daAnteriores(estados) {
    estados = estados || {}; var o = {};
    var ordem = ["marco-zero", "planejamento", "financas", "preco", "marketing", "pessoas", "compras"];
    ["nome", "email", "hospedagem", "situacao"].forEach(function (k) { for (var i = 0; i < ordem.length; i++) { var s = estados[ordem[i]]; if (s && informado(s[k])) { o[k] = String(s[k]); break; } } });
    var pl = estados.planejamento, pe = estados.pessoas, pr = estados.preco;
    if (pl) {
      if (informado(pl.escalaNota)) o.escala = String(pl.escalaNota) === "10" ? "10" : "5";
      if (informado(pl.base_nota)) o.notaAtual = String(pl.base_nota).replace(".", ",");
      if (informado(pl.meta_nota)) o.notaMeta = String(pl.meta_nota).replace(".", ",");
      if (informado(pl.reuniaoDia)) { var d = DIAS.filter(function (x) { return x.r === pl.reuniaoDia || x.v === pl.reuniaoDia; })[0]; if (d) o.reuniaoDia = d.v; }
      if (informado(pl.reuniaoHora)) o.reuniaoHora = String(pl.reuniaoHora);
    }
    if (pe) {
      if (informado(pe.notaMin)) o.notaMin = String(pe.notaMin).replace(".", ",");
      if (informado(pe.diaSemanal)) o.painelDia = String(pe.diaSemanal);
      if (informado(pe.inicio)) o.inicioF1 = String(pe.inicio);
    }
    if (pr) { var md = num(pr.metaDireta); if (md != null) o.metaDireta = md; if (informado(pr.prazoMeta)) o.prazoDireta = String(pr.prazoMeta); }
    return o;
  }

  // ---------- validação por tela ----------
  function validar(S, tela) {
    S = S || {}; var e = [], a = [], E = escala(S);
    var nota = function (k, rot, obrig) { var v = num(S[k]); if (!informado(S[k])) { if (obrig) e.push("Informe " + rot + "."); return null; } if (v == null) { e.push(rot.charAt(0).toUpperCase() + rot.slice(1) + ": use só números (ex.: 4,7)."); return null; } if (v < 0 || v > E) e.push(rot.charAt(0).toUpperCase() + rot.slice(1) + " precisa estar entre 0 e " + E + "."); return v; };
    var inteiro = function (k, rot, obrig) { var v = num(S[k]); if (!informado(S[k])) { if (obrig) e.push("Informe " + rot + "."); return null; } if (v == null || v < 0 || Math.round(v) !== v) { e.push(rot.charAt(0).toUpperCase() + rot.slice(1) + ": use um número inteiro, zero ou maior."); return null; } return v; };
    var data = function (k, rot, obrig) { if (!informado(S[k])) { if (obrig) e.push("Marque " + rot + "."); return null; } if (diaUTC(S[k]) == null) { e.push(rot.charAt(0).toUpperCase() + rot.slice(1) + ": data inválida."); return null; } return S[k]; };
    var abrir = S.situacao === "abrir";
    if (tela === "abertura") { if (!S.situacao) e.push("Escolha a frase que mais parece com você."); }
    if (tela === "nota") {
      var na = nota("notaAtual", "a nota média atual", !abrir), nm = nota("notaMeta", "a meta da nota", true);
      if (na != null && nm != null && nm < na) a.push("A meta está abaixo da nota atual. Se a ideia é manter, escreva a meta igual à nota de hoje.");
      var nav = inteiro("avaliacoes", "o número de avaliações acumuladas", !abrir);
      var es = inteiro("estadias3m", "as estadias dos últimos três meses", false), av = inteiro("avaliacoes3m", "as avaliações recebidas nos últimos três meses", false);
      if (es != null && av != null && av > es) e.push("As avaliações dos três meses passam das estadias do período: confira os dois números.");
      if (nav != null && av != null && av > nav) e.push("As avaliações dos três meses passam do total acumulado.");
      if (informado(S.prazoMeta)) data("prazoMeta", "o prazo da meta", false);
      nota("dimensaoNota", "a nota da dimensão mais baixa", false); nota("concorrentes", "a nota dos concorrentes diretos", false);
      var rep = inteiro("repeticoes", "as repetições da crítica", false); inteiro("criticas3m", "as críticas registradas", false);
      if (rep != null && rep > 0 && letras(S.criticaRepetida) < 3) e.push("Escreva qual é a crítica que se repetiu.");
      var tr = num(S.tempoResposta); if (informado(S.tempoResposta) && (tr == null || tr < 0)) e.push("Tempo de resposta: use minutos, zero ou mais.");
    }
    if (tela === "protocolo") {
      if (letras(S.pedido) < 10) e.push("Escreva a frase do pedido de avaliação na saída.");
      if (!S.naoPedir) e.push("Responda se você usa a regra de não pedir quando houve problema não resolvido.");
      else if (S.naoPedir === "nao") a.push("Pedir avaliação a quem teve problema não resolvido é pedir a avaliação ruim por escrito. Resolva primeiro, peça depois, ou não peça.");
      if (letras(S.respPositiva) < 10) e.push("Escreva o modelo de resposta à avaliação positiva.");
      if (letras(S.respNegativa) < 10) e.push("Escreva o modelo de resposta à avaliação negativa.");
      if (!S.regra24) e.push("Responda se você adota a regra das 24 horas.");
      else if (S.regra24 === "nao") a.push("Resposta escrita com a irritação fresca é defensiva, e quem lê percebe. A fonte pede 24 horas antes de responder uma negativa.");
      var nmi = nota("notaMin", "a nota mínima", true), nme = num(S.notaMeta);
      if (nmi != null && nme != null && nmi > nme) e.push("A nota mínima não pode passar da meta da nota.");
      var rm = num(S.respostaMax); if (!informado(S.respostaMax)) e.push("Informe o tempo máximo de resposta a mensagem, em minutos."); else if (rm == null || rm <= 0) e.push("Tempo máximo de resposta: use minutos, maior que zero."); else if (rm > 60) a.push("A fonte pede resposta em menos de uma hora, sempre, inclusive para quem só pergunta.");
      var tm = num(S.taxaMin); if (!informado(S.taxaMin)) e.push("Informe a taxa mínima de avaliação (%)."); else if (tm == null || tm <= 0 || tm > 100) e.push("Taxa mínima de avaliação: de 1 a 100%."); else if (tm < 40) a.push("Abaixo de 40% de hóspedes avaliando, a fonte lê que o pedido não está sendo feito ou não está funcionando.");
      if (!S.auditoria) e.push("Responda se haverá auditoria de uma unidade por semana.");
      if ((num(S.repeticoes) || 0) >= 3) { if (letras(S.ajuste) < 10) e.push("A crítica se repetiu três vezes ou mais: escreva o ajuste de produto."); data("ajustePrazo", "o prazo do ajuste", true); }
    }
    if (tela === "rotina") {
      if (!S.reuniaoDia) e.push("Escolha o dia da reunião semanal."); if (!/^\d{2}:\d{2}$/.test(String(S.reuniaoHora || ""))) e.push("Marque a hora da reunião semanal.");
      if (!S.painelDia) e.push("Escolha o dia da leitura do painel por exceção.");
      var fd = num(S.folhaDia); if (!informado(S.folhaDia)) e.push("Informe o dia do mês da Folha Única."); else if (fd == null || fd < 1 || fd > 28 || Math.round(fd) !== fd) e.push("Dia da Folha Única: de 1 a 28, para existir em todo mês.");
      data("trimestral1", "a data da primeira revisão trimestral", true); var an = data("anual", "a data da revisão anual", true);
      if (an && informado(S.trimestral1) && diaUTC(S.trimestral1) != null && difDias(S.trimestral1, an) < 0) a.push("A revisão anual está antes da primeira trimestral: confira as datas.");
      if (S.reuniaoDia && S.painelDia && S.reuniaoDia !== S.painelDia) a.push("A leitura do painel e a reunião semanal caem em dias diferentes. Funciona, mas o mesmo dia economiza uma conversa.");
    }
    if (tela === "prontidao") {
      var i1 = data("inicioF1", "o início da Fase 1", true);
      var s1 = num(S.semanasF1), s2 = num(S.semanasF2);
      if (!informado(S.semanasF1) || s1 == null || s1 < 1 || Math.round(s1) !== s1) e.push("Semanas da Fase 1: um número inteiro de semanas."); else if (s1 < 6 || s1 > 10) a.push("A fonte prevê de seis a dez semanas para escrever o manual mínimo.");
      if (!informado(S.semanasF2) || s2 == null || s2 < 1 || Math.round(s2) !== s2) e.push("Semanas da Fase 2: um número inteiro de semanas.");
      var it = data("inicioTeste", "o início do teste das duas semanas", true);
      if (i1 && it && s1 > 0 && s2 > 0) { var f3 = difDias(somaDias(i1, 7 * (s1 + s2)), it); if (f3 < 0) e.push("O teste começa antes do fim da Fase 2: mova a data do teste."); else if (f3 < 56) a.push("O painel por exceção precisa rodar pelo menos oito semanas antes do teste. Hoje são " + Math.floor(f3 / 7) + "."); }
      if (letras(S.responsavel) < 3) e.push("Diga quem fica responsável durante o teste.");
      var op = num(S.ocupProjetada); if (!informado(S.ocupProjetada)) e.push("Informe a ocupação projetada para o período do teste (%)."); else if (op == null || op < 0 || op > 100) e.push("Ocupação projetada: de 0 a 100%.");
      nota("notaMedia3m", "a nota média dos três meses anteriores", !abrir);
      if (!S.periodoMedio) e.push("Responda se o período do teste é de ocupação média."); else if (S.periodoMedio === "nao") a.push("Escolha um período de ocupação média: vale fácil não testa nada, e pico concentra risco demais na primeira tentativa.");
      if (!S.tempoSobra) e.push("Escolha o que você vai fazer com o tempo que sobrar.");
      CONDICOES.forEach(function (c) { if (!S.cond || !S.cond[c.id]) e.push("Responda a condição: " + c.r.toLowerCase() + "."); });
      if (S.feito === "sim") {
        var or = num(S.ocupReal); if (!informado(S.ocupReal) || or == null || or < 0 || or > 100) e.push("Informe a ocupação do período do teste (%).");
        nota("notaPeriodo", "a nota do período do teste", true);
        inteiro("contatos", "os contatos por exceção durante o teste", true);
        if (or != null && op != null && or < op && !S.causaExterna) e.push("A ocupação caiu: responda se houve causa externa.");
      }
    }
    return { ok: e.length === 0, erros: e, avisos: a };
  }

  // ---------- cálculos ----------
  function fases(S) {
    var i1 = diaUTC(S.inicioF1) != null ? S.inicioF1 : null, s1 = num(S.semanasF1), s2 = num(S.semanasF2), it = diaUTC(S.inicioTeste) != null ? S.inicioTeste : null;
    var F = [{ n: 1, r: "Escrever", o: "O manual mínimo: os procedimentos e a tabela de critérios, em menos de duas horas por semana.", sinal: "Manual em nuvem e impresso", ref: "6 a 10 semanas" },
      { n: 2, r: "Contratar e treinar", o: "A primeira contratação e as quatro semanas de treino do Módulo 5.", sinal: "Padrão mantido com autonomia", ref: "cerca de 8 semanas" },
      { n: 3, r: "Acompanhar por exceção", o: "O painel de seis indicadores rodando, com leitura semanal e conversa mensal.", sinal: "Dúvidas raras, critérios em uso", ref: "pelo menos 8 semanas" },
      { n: 4, r: "Testar", o: "Catorze dias fora, sem atender, com contato só pelas quatro exceções.", sinal: "Ocupação e nota mantidas", ref: "2 semanas" }];
    if (i1 && s1 > 0) { F[0].de = i1; F[0].ate = somaDias(i1, 7 * s1 - 1); F[0].semanas = s1; }
    if (F[0].ate && s2 > 0) { F[1].de = somaDias(F[0].ate, 1); F[1].ate = somaDias(F[1].de, 7 * s2 - 1); F[1].semanas = s2; }
    if (it) { F[3].de = it; F[3].ate = somaDias(it, 13); F[3].semanas = 2; }
    if (F[1].ate && it && difDias(F[1].ate, it) > 1) { F[2].de = somaDias(F[1].ate, 1); F[2].ate = somaDias(it, -1); F[2].semanas = Math.floor((difDias(F[2].de, F[2].ate) + 1) / 7); }
    var total = i1 && F[3].ate ? difDias(i1, F[3].ate) + 1 : null;
    var meses = total != null ? Math.round((total / 30.4375) * 10) / 10 : null;
    return { lista: F, totalDias: total, meses: meses, noPrazo: meses != null ? meses >= 6 && meses <= 8 : null, f3ok: F[2].semanas != null ? F[2].semanas >= 8 : false };
  }
  // Leitura do teste das duas semanas (Etapa 10, Passo 12). Tolerância da nota: elaboração declarada (0,1 em 5; 0,2 em 10).
  function veredito(S) {
    if (S.feito !== "sim") return null;
    var E = escala(S), op = num(S.ocupProjetada), or = num(S.ocupReal), nm = num(S.notaMedia3m), np = num(S.notaPeriodo), c = num(S.contatos);
    if (op == null || or == null || np == null || c == null) return null;
    var tol = E === 10 ? 0.2 : 0.1;
    var notaOk = nm == null ? true : np >= nm - tol - 1e-9, ocupOk = or >= op;
    if (!notaOk) return { id: "nota", r: "A nota caiu", t: "Falta padrão ou falta treino. Volte ao procedimento e às quatro semanas de treino do Módulo 5 (Etapa 10, Passos 05 e 09).", passou: false };
    if (!ocupOk && S.causaExterna !== "sim") return { id: "ocupacao", r: "A ocupação caiu sem causa externa", t: "Falta quem trabalhe a demanda: pode ser uma segunda contratação ou a sua própria função, de fora. Reveja os Módulos 3 e 4.", passou: false };
    if (!ocupOk) return { id: "externa", r: "A ocupação caiu por causa externa", t: "A causa não está na operação. Repita o teste num período de ocupação média, sem a causa externa.", passou: false };
    if (c > 2) return { id: "criterio", r: "Ocupação e nota mantidas, com muitos contatos", t: "Falta critério, não falta procedimento. Volte à tabela de critérios e às alçadas do Módulo 5 (Etapa 10, Passo 06).", passou: false };
    return { id: "passou", r: "Passou", t: "Ocupação e nota mantidas, com no máximo dois contatos por exceção: a operação roda sem você.", passou: true };
  }

  function calcular(S, pags) {
    S = S || {}; var E = escala(S); pags = pags || paginas({});
    var na = num(S.notaAtual), nm = num(S.notaMeta), nmin = num(S.notaMin), n = num(S.avaliacoes);
    var es = num(S.estadias3m), av3 = num(S.avaliacoes3m), taxa = es > 0 && av3 != null ? av3 / es : null;
    var taxaMin = num(S.taxaMin), respMax = num(S.respostaMax), tr = num(S.tempoResposta), conc = num(S.concorrentes), dimN = num(S.dimensaoNota), rep = num(S.repeticoes) || 0;
    // A matemática da média pequena (Volume 07, Cap. 18), generalizada: média depois de uma avaliação de 3
    var apos3 = na != null && n > 0 ? (na * n + 3 * (E / 5)) / (n + 1) : null;
    var dim = DIMENSOES.filter(function (d) { return d.v === S.dimensao; })[0] || null;
    var padrao = [
      { id: "nota", r: "Nota mínima das avaliações (abaixo dela, contato na hora)", v: nmin != null ? notaTxt(nmin, E) : "a definir", ok: nmin != null },
      { id: "meta", r: "Meta da nota" + (informado(S.prazoMeta) ? " até " + br(S.prazoMeta) : ""), v: nm != null ? notaTxt(nm, E) : "a definir", ok: nm != null },
      { id: "resposta", r: "Resposta a mensagem de hóspede", v: respMax != null ? "em até " + dec(respMax, 0) + " minutos" : "a definir", ok: respMax != null && respMax > 0 && respMax <= 60 },
      { id: "taxa", r: "Hóspedes que avaliam (taxa mínima)", v: taxaMin != null ? dec(taxaMin, 0) + "%" : "a definir", ok: taxaMin != null && taxaMin >= 40 },
      { id: "todas", r: "Toda avaliação respondida; a negativa, só depois de 24 horas", v: S.regra24 === "sim" ? "sim" : S.regra24 === "nao" ? "não" : "a definir", ok: S.regra24 === "sim" },
      { id: "repetida", r: "Crítica repetida três vezes no trimestre vira ajuste de produto com prazo", v: rep >= 3 ? (S.ajuste ? S.ajuste + (informado(S.ajustePrazo) ? " · até " + br(S.ajustePrazo) : "") : "ajuste a escrever") : "regra valendo (nenhuma crítica repetida três vezes)", ok: rep < 3 || (letras(S.ajuste) >= 10 && diaUTC(S.ajustePrazo) != null) },
      { id: "auditoria", r: "Auditoria por amostragem: uma unidade sorteada por semana, contra a foto do padrão", v: S.auditoria === "sim" ? "sim" : S.auditoria === "nao" ? "não" : "a definir", ok: S.auditoria === "sim" },
    ];
    var tri = diaUTC(S.trimestral1) != null ? [0, 3, 6, 9].map(function (k) { return somaMeses(S.trimestral1, k); }) : [];
    var rotina = {
      semanal: [
        { r: "Reunião de gestão com os cinco números do painel", q: S.reuniaoDia ? nomeDia(S.reuniaoDia) + (S.reuniaoHora ? ", " + S.reuniaoHora : "") : "a definir", d: "30 min", f: "Panorama · G7" },
        { r: "Leitura dos seis indicadores do painel por exceção", q: S.painelDia ? nomeDia(S.painelDia) : "a definir", d: "15 min", f: "Etapa 10 · Passo 10" },
        { r: "Conferir o saldo, as entradas e as transferências para as reservas", q: S.painelDia ? nomeDia(S.painelDia) : "a definir", d: "5 min", f: "Etapa 09 · Passo 13" },
        { r: "Responder as avaliações da semana e registrar toda crítica, mesmo em avaliação boa", q: S.quemResponde ? S.quemResponde : "a definir", d: "15 min", f: "Etapa 07 · Volume 07" },
        { r: "Auditoria de uma unidade sorteada, contra a foto do padrão", q: S.auditoria === "sim" ? "uma por semana" : "a decidir", d: "15 min", f: "Etapa 10 · Passo 10" },
      ],
      mensal: [
        { r: "Folha Única do mês, comparada com o mesmo mês do ano anterior", q: num(S.folhaDia) ? "dia " + num(S.folhaDia) : "a definir", d: "10 min" },
        { r: "Conversa mensal com quem opera, com a Folha ao lado", q: "junto da Folha", d: "40 min" },
        { r: "Taxa de avaliação, nota por dimensão e críticas que se repetiram", q: "junto da Folha", d: "15 min" },
      ],
      trimestral: tri, anual: diaUTC(S.anual) != null ? S.anual : null,
    };
    var F = fases(S), V = veredito(S);
    var condOk = CONDICOES.filter(function (c) { return S.cond && S.cond[c.id] === "sim"; }).length;
    var condResp = CONDICOES.filter(function (c) { return S.cond && S.cond[c.id]; }).length;
    var segunda = condResp < 4 ? { r: "a decidir", t: "Responda as quatro condições." } : condOk === 4 ? { r: "Pode estudar a segunda unidade", t: "As quatro condições estão presentes: a segunda unidade multiplica um acerto." } : { r: "Agora não", t: "Faltam " + (4 - condOk) + " de 4 condições. Faltando qualquer uma, a segunda unidade antecipa um problema em vez de multiplicar um acerto." };
    var presentes = pags.filter(function (p) { return p.estado === "pronta"; });
    var faltam = pags.filter(function (p) { return p.estado !== "pronta"; });
    var v = function (t) { return validar(S, t).ok; };
    var testeOk = diaUTC(S.inicioTeste) != null && letras(S.responsavel) >= 3 && num(S.ocupProjetada) != null && (S.situacao === "abrir" || num(S.notaMedia3m) != null) && S.periodoMedio === "sim";
    var itens = [
      { id: "paginas", p: "terminar as páginas " + faltam.map(function (x) { return x.n; }).join(", ") + " (fichas dos módulos)", r: "As páginas 0 a 6 presentes (PDF de cada ficha gerado neste aparelho): " + presentes.length + " de 7", ok: presentes.length === 7 },
      { id: "nota", p: "informar a nota e as avaliações", r: "A nota, o volume de avaliações e a meta informados", ok: v("nota") },
      { id: "protocolo", p: "escrever o protocolo de resposta", r: "O protocolo de resposta escrito: pedido, quando não pedir, resposta positiva, resposta negativa e regra das 24 horas", ok: letras(S.pedido) >= 10 && S.naoPedir === "sim" && letras(S.respPositiva) >= 10 && letras(S.respNegativa) >= 10 && S.regra24 === "sim" },
      { id: "padrao", p: "definir o padrão mínimo", r: "O padrão mínimo definido: nota mínima, resposta, taxa de avaliação, auditoria e ajuste da crítica repetida", ok: v("protocolo") },
      { id: "rotina", p: "marcar a rotina semanal", r: "A rotina semanal marcada: reunião, painel, Folha do mês e as revisões trimestrais e anual", ok: v("rotina") },
      { id: "teste", p: "agendar o teste de prontidão", r: "O teste de prontidão agendado: data, responsável, ocupação projetada, nota de referência e período de ocupação média", ok: testeOk },
      { id: "saida", p: "datar o plano de saída", r: "O plano de saída com as quatro fases datadas e a decisão sobre o tempo que sobra", ok: v("prontidao") && F.lista.every(function (f) { return !!f.de; }) },
    ];
    return {
      escala: E, notaAtual: na, notaMeta: nm, notaMin: nmin, avaliacoes: n, gapMeta: na != null && nm != null ? Math.round((nm - na) * 100) / 100 : null,
      abaixoMin: na != null && nmin != null && na < nmin, apos3: apos3, queda: apos3 != null ? na - apos3 : null,
      taxa: taxa, taxaMin: taxaMin, taxaBaixa: taxa != null && taxaMin != null && taxa < taxaMin / 100,
      tempoResposta: tr, respostaMax: respMax, respostaLenta: tr != null && respMax != null && tr > respMax,
      concorrentes: conc, difConc: na != null && conc != null ? Math.round((na - conc) * 100) / 100 : null,
      dimensao: dim, dimensaoNota: dimN, repeticoes: rep, produto: rep >= 3,
      padrao: padrao, rotina: rotina, fases: F, veredito: V, segunda: segunda, condOk: condOk,
      tempoSobra: TEMPO_SOBRA.filter(function (t) { return t.v === S.tempoSobra; })[0] || null,
      teste: { de: diaUTC(S.inicioTeste) != null ? S.inicioTeste : null, ate: diaUTC(S.inicioTeste) != null ? somaDias(S.inicioTeste, 13) : null, ocup: num(S.ocupProjetada), nota: num(S.notaMedia3m) },
      paginas: pags, presentes: presentes.length, faltam: faltam, itens: itens, prontos: itens.filter(function (i) { return i.ok; }).length,
    };
  }

  // ---------- leituras (resultado em cinco partes) ----------
  function leituras(r, S) {
    S = S || {}; var E = r.escala, L = {};
    L.titulo = r.presentes === 7 ? "As oito páginas do seu Plano estão juntas" : "Faltam " + (7 - r.presentes) + " de 8 páginas para fechar o Plano";
    L.nota = r.notaAtual == null ? "Sem nota ainda: você vai abrir. A meta de " + notaTxt(r.notaMeta, E) + " vale para as primeiras avaliações, e elas são permanentes." :
      "Nota " + notaTxt(r.notaAtual, E) + ", com " + (r.avaliacoes != null ? r.avaliacoes + " avaliações" : "volume a informar") + "; meta de " + notaTxt(r.notaMeta, E) + (r.gapMeta > 0 ? " (faltam " + dec(r.gapMeta, 1) + " ponto)" : "") + ".";
    L.volume = r.apos3 != null ? "Com " + r.avaliacoes + " avaliações e nota " + dec(r.notaAtual, 1) + ", uma única avaliação de " + (E === 10 ? "6" : "3") + " leva a média para " + dec(r.apos3, 2) + ". A média é lenta para subir e rápida para cair quando o volume é pequeno: acumular avaliações boas é a defesa." : "Sem volume informado, não dá para medir quanto uma avaliação ruim pesa.";
    L.taxa = r.taxa != null ? "De cada 100 hóspedes, " + dec(r.taxa * 100, 0) + " avaliam" + (r.taxaBaixa ? ": abaixo do seu mínimo de " + dec(r.taxaMin, 0) + "%. O pedido não está sendo feito ou não está funcionando." : ", dentro do seu mínimo.") : "Informe estadias e avaliações dos três meses para ver a taxa de avaliação.";
    L.dimensao = r.dimensao && r.dimensao.v !== "naosei" ? "A dimensão mais baixa é " + r.dimensao.r.toLowerCase() + (r.dimensaoNota != null ? " (" + dec(r.dimensaoNota, 1) + ")" : "") + ": é onde está o trabalho." : "Se o canal separar a nota por dimensão, a mais baixa mostra onde está o trabalho.";
    L.concorrentes = r.difConc != null ? (r.difConc >= 0 ? "Você está " + dec(r.difConc, 1) + " ponto acima" : "Você está " + dec(-r.difConc, 1) + " ponto abaixo") + " dos concorrentes diretos. Compare com eles, não com o ideal." : "";
    L.rotina = "Rotina: " + r.rotina.semanal[0].q + " (reunião de 30 min) e " + r.rotina.semanal[1].q + " (painel de 15 min). Folha Única " + r.rotina.mensal[0].q + "." + (r.rotina.trimestral.length ? " Revisões trimestrais: " + r.rotina.trimestral.map(br).join(", ") + "." : "");
    L.saida = r.fases.meses != null ? "Do início da Fase 1 ao fim do teste: " + dec(r.fases.meses, 1) + " meses (" + br(r.fases.lista[0].de) + " a " + br(r.fases.lista[3].ate) + ")" + (r.fases.noPrazo ? ", dentro dos seis a oito meses da fonte." : r.fases.meses < 6 ? ", mais curto que os seis a oito meses da fonte: confira se cada fase cabe." : ", mais longo que os seis a oito meses da fonte. Tudo bem, desde que cada data esteja marcada.") : "Marque o início da Fase 1 e do teste para ver o plano inteiro.";
    // Atenção, em ordem
    var A = [];
    if (r.faltam.length) A.push({ id: "paginas", t: "Faltam páginas: " + r.faltam.map(function (p) { return p.n + " · " + p.r + " (" + (p.estado === "andamento" ? "em andamento" : "ainda não feita") + ")"; }).join("; ") + ". Abra a ficha de cada uma neste aparelho e chegue ao PDF." });
    if (r.abaixoMin) A.push({ id: "minima", t: "A nota de hoje está abaixo da sua nota mínima: pelo seu painel, isso já é exceção. Leia as últimas avaliações antes de qualquer outra coisa." });
    if (r.produto) A.push({ id: "produto", t: "\"" + (S.criticaRepetida || "A crítica") + "\" apareceu " + r.repeticoes + " vezes no trimestre: é problema de produto, não de hóspede. Ajuste com prazo" + (diaUTC(S.ajustePrazo) != null ? " (" + br(S.ajustePrazo) + ")" : "") + "." });
    if (r.taxaBaixa) A.push({ id: "taxa", t: "Taxa de avaliação de " + pct(r.taxa, 0) + ", abaixo do mínimo de " + dec(r.taxaMin, 0) + "%: peça pessoalmente, na saída, a todo hóspede que teve boa estadia." });
    if (r.respostaLenta) A.push({ id: "resposta", t: "Tempo médio de resposta de " + dec(r.tempoResposta, 0) + " minutos, acima do seu máximo de " + dec(r.respostaMax, 0) + ". Responder rápido é o fator mais rápido de melhorar." });
    if (r.fases.lista[2].semanas != null && !r.fases.f3ok) A.push({ id: "fase3", t: "O painel por exceção roda só " + r.fases.lista[2].semanas + " semanas antes do teste; a fonte pede pelo menos oito." });
    if (S.periodoMedio === "nao") A.push({ id: "periodo", t: "Mude o teste para um período de ocupação média: vale fácil não testa nada." });
    if (S.tempoSobra === "segunda" && r.condOk < 4) A.push({ id: "segunda", t: "Você escolheu a segunda unidade, mas faltam " + (4 - r.condOk) + " das 4 condições. Sem elas, a segunda antecipa um problema." });
    if (r.dimensao && r.dimensao.v !== "naosei" && !r.produto) A.push({ id: "dimensao", t: "Comece pela dimensão mais baixa: " + r.dimensao.r.toLowerCase() + "." });
    if (!A.length) A.push({ id: "ok", t: "Nenhum alerta das regras da fonte. Mantenha a rotina: o valor vem da série, e série exige repetir o mesmo número." });
    L.atencao = A;
    // O que fazer: próximos 30 dias + fases
    var fazer = [];
    if (r.faltam.length) fazer.push("Terminar as páginas que faltam: " + r.faltam.map(function (p) { return p.n; }).join(", ") + ".");
    if (r.produto) fazer.push("Fazer o ajuste de produto: " + (S.ajuste || "a definir") + (diaUTC(S.ajustePrazo) != null ? " até " + br(S.ajustePrazo) : "") + ".");
    fazer.push("Usar o protocolo em toda saída e responder todas as avaliações; a negativa, depois de 24 horas.");
    fazer.push("Começar a rotina na próxima " + (nomeDia(S.reuniaoDia) || "semana").toLowerCase() + (S.reuniaoHora ? " às " + S.reuniaoHora : "") + ", com a planilha de qualidade aberta.");
    if (r.fases.lista[0].de) fazer.push("Fase 1 de " + br(r.fases.lista[0].de) + " a " + br(r.fases.lista[0].ate) + ": escrever o manual mínimo.");
    L.fazer = fazer;
    L.verificar = "Daqui a quatro semanas: a nota e a taxa de avaliação foram anotadas toda semana na planilha? Toda avaliação recebeu resposta? A reunião aconteceu as quatro vezes? O teste continua marcado para " + br(r.teste.de) + "? No teste, a leitura é da fonte: ocupação e nota mantidas, com no máximo dois contatos por exceção, passou.";
    return L;
  }

  function pendencias(S, pags) { var r = calcular(S, pags), p = r.itens.filter(function (i) { return !i.ok; }).map(function (i) { return i.p; }); if (!S || !S.pdf) p.push("baixar o PDF do Plano completo"); return p; }
  function concluido(S, pags) { return pendencias(S, pags).length === 0; }
  function proximaVazia(S) { for (var k = 1; k < TELAS.length - 1; k++) if (!validar(S, TELAS[k]).ok) return TELAS[k]; return "resultado"; }

  // ---------- resumo de cada página anterior (para o Plano em PDF) ----------
  // api = a lógica do módulo (window.ZG, ZP, ZF...), se carregou. Tudo protegido: se algo mudar num módulo, cai no resumo mínimo.
  function seguro(f) { try { var x = f(); return x && x.length ? x : null; } catch (e) { return null; } }
  function resumoPagina(n, S, api, fin) {
    var P = PAGINAS[n]; if (!S) return { n: n, r: P.r, m: P.m, linhas: ["Página ainda não feita. Abra a ficha do módulo: trilha2/" + P.slug + "/"], feita: false };
    var L = null, A = api;
    if (A) {
      if (n === 0) L = seguro(function () { var r = A.calcular(S); var ac = S.acao != null ? S.acao : A.acaoSugerida(r); return ["Nota de gestão: " + r.nota + " de 100 · " + r.faixa.rot, "Área mais frágil: " + (r.fragil ? r.fragil.n + " · " + r.fragil.r : "nenhuma em branco"), "Ação de 30 dias: " + ac + (S.prazo ? " (até " + br(S.prazo) + ")" : "")]; });
      if (n === 1) L = seguro(function () { var r = A.calcular(S); return A.painel(r).map(function (l) { return l.r + ": " + l.base + " → " + l.meta + " (" + l.dono + ")"; }).concat(S.reuniaoDia ? ["Reunião semanal: " + S.reuniaoDia + (S.reuniaoHora ? ", " + S.reuniaoHora : "")] : []); });
      if (n === 2) L = seguro(function () { var r = A.calcular(S); return [(r.N && r.N.mes ? r.N.mes + " · " : "") + "Resultado do mês: " + brl(r.resultadoOperacional), "Receita real: " + brl(r.receitaReal) + " · ocupação " + pct(r.ocupacao), "Custo por noite vendida: " + brl(r.custoPorNoiteVendida) + " · ocupação de equilíbrio " + pct(r.ocupacaoEquilibrio), "Fôlego de caixa: " + dec(r.mesesFolego, 1) + " meses"]; });
      if (n === 3) L = seguro(function () { var r = A.calcular(S); return ["Piso escrito: " + brl(num(S.pisoDeclarado)) + " · diária de referência " + brl(num(S.referencia)), "Diária média do calendário: " + brl(r.mediaAno) + " (não é previsão)", "Venda direta: " + dec(r.diretaAtual, 0) + "% hoje, meta de " + dec(num(S.metaDireta), 0) + "% até " + br(S.prazoMeta)]; });
      if (n === 4) L = seguro(function () { var r = A.calcular(S); return [S.promessa ? "Promessa: " + S.promessa : null, r.custoPorReserva != null ? "Custo médio por reserva: " + brl(r.custoPorReserva) : null, r.vendaDireta != null ? "Venda direta: " + pct(r.vendaDireta, 0) + (r.metaDireta != null ? " · meta " + dec(r.metaDireta, 0) + "%" + (r.prazoMeta ? " até " + r.prazoMeta : "") : "") : null, r.contatos != null ? "Lista própria: " + r.contatos + " contatos" + (r.metaLista ? " de " + r.metaLista : "") : null].filter(Boolean); });
      if (n === 5) L = seguro(function () { var r = A.calcular(S, fin); return [r.horasTotal + " horas por semana passam pelo gestor · " + r.prontos + " de 7 itens prontos", "Primeira atividade a delegar: " + (r.primeira ? r.primeira.r : "a definir") + (S.pessoa ? " · para " + S.pessoa : ""), "Alçada inicial: " + brl(r.alcadaInicial) + (r.alcada2mes ? " · no segundo mês " + brl(r.alcada2mes) : ""), "Semana 1 em " + br(S.inicio) + " · avaliação em " + br(r.avaliacao)]; });
      if (n === 6) L = seguro(function () { var r = A.calcular(S); return [r.itens ? "Matriz: " + r.itens.length + " itens, " + (r.comTres != null ? r.comTres : "?") + " com três cotações" : null, r.variavelNoite != null ? "Custo variável por noite: " + brl(r.variavelNoite) : null, r.pedirAgora ? "Itens para pedir agora: " + r.pedirAgora.length : null, r.totalAno != null ? "Manutenção preventiva no ano: " + brl(r.totalAno) + (r.mesMaisPesado && r.mesMaisPesado.nome ? " · mês mais pesado: " + r.mesMaisPesado.nome : "") : null].filter(Boolean); });
    }
    if (!L) L = ["Página feita neste aparelho" + (S.pdf ? " (PDF de " + br(String(S.pdf).slice(0, 10)) + ")" : ", ainda sem PDF") + ". Resumo indisponível nesta versão: anexe o PDF da ficha."];
    if (S.acao && n > 0 && n !== 5) L.push("Ação escolhida: " + S.acao + (S.prazo ? " (até " + br(S.prazo) + ")" : ""));
    return { n: n, r: P.r, m: P.m, linhas: L, feita: true, pronta: !!S.pdf };
  }

  var api = { SITUACOES: SITUACOES, SIMNAO: SIMNAO, ESCALAS: ESCALAS, DIMENSOES: DIMENSOES, DIAS: DIAS, TEMPO_SOBRA: TEMPO_SOBRA, CONDICOES: CONDICOES, PAGINAS: PAGINAS,
    INDICADORES: INDICADORES, MEDIR: MEDIR, REGRAS_TESTE: REGRAS_TESTE, TELAS: TELAS, TITULOS: TITULOS, PROXIMO: PROXIMO, EXEMPLO: EXEMPLO,
    exemplo: exemplo, base: base, completar: completar, num: num, letras: letras, validar: validar, paginas: paginas, rotuloEstado: rotuloEstado, daAnteriores: daAnteriores,
    fases: fases, veredito: veredito, calcular: calcular, leituras: leituras, pendencias: pendencias, concluido: concluido, proximaVazia: proximaVazia, resumoPagina: resumoPagina,
    brl: brl, pct: pct, dec: dec, notaTxt: notaTxt, br: br, somaDias: somaDias, somaMeses: somaMeses, difDias: difDias, diaSemana: diaSemana, nomeDia: nomeDia };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else raiz.ZQ = api;
})(typeof window !== "undefined" ? window : this);

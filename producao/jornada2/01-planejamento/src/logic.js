/* Jornada 2 · Gestão · Módulo 1 · Planejamento, metas e indicadores
   Lógica pura da ficha "O meu Painel de Gestão". Sem DOM: roda no navegador (window.ZP) e no Node (testes).
   Regra: tudo que a ficha afirma sai daqui, para ser testado. Sem nota e sem régua de mercado:
   os cinco indicadores e a reunião semanal vêm do Pilar G7 do Panorama; as leituras de meta são aritmética declarada. */
(function (raiz) {
  "use strict";

  var SITUACOES = [
    { v: "abrir", r: "Ainda vou abrir a minha hospedagem (vou usar números previstos)", curto: "vai abrir" },
    { v: "dono", r: "Já opero a minha hospedagem e quero metas e um painel", curto: "dono que opera" },
    { v: "operador", r: "Cuido da hospedagem de outra pessoa e presto contas ao dono", curto: "operador" },
  ];
  var QUEM = [
    { v: "so", r: "Eu, sozinho" },
    { v: "dupla", r: "Eu e mais uma pessoa" },
    { v: "equipe", r: "Tenho gerente ou equipe" },
  ];

  // Diagnóstico de abertura: o nível do painel (4 perguntas Sim/Não → nível 1 a 4). Elaboração declarada no PLANO.
  var DIAG = [
    { id: "painel", r: "Você olha os mesmos números todo mês, sempre na mesma ordem?" },
    { id: "metas", r: "Existem metas escritas para os próximos 12 meses?" },
    { id: "donos", r: "Cada número tem uma pessoa que responde por ele?" },
    { id: "reuniao", r: "Existe um horário fixo, toda semana, para olhar esses números?" },
  ];
  var SIMNAO = [{ v: "sim", r: "Sim" }, { v: "nao", r: "Não" }];
  var NIVEIS = [
    { n: 1, r: "Sem painel", t: "Hoje os números aparecem quando alguém pergunta. O Painel de Gestão é o primeiro corte: cinco números, cinco donos, trinta minutos por semana." },
    { n: 2, r: "Números soltos", t: "Alguma coisa já é olhada, mas sem meta, sem dono ou sem dia. O Painel junta as peças numa página." },
    { n: 3, r: "Quase lá", t: "Falta uma peça: a meta, o dono ou a reunião. O Painel mostra qual." },
    { n: 4, r: "Painel com rotina", t: "Números, metas, donos e reunião existem. Use a ficha para escrever tudo numa página e revisar as metas." },
  ];
  function nivelPainel(S) {
    var d = (S && S.diag) || {}, sim = 0;
    DIAG.forEach(function (q) { if (d[q.id] === "sim") sim++; });
    return NIVEIS[Math.max(0, sim - 1)];
  }

  // Os cinco indicadores do Pilar G7 ("Ocupação, diária média, resultado, nota e taxa de venda direta cobrem quase todo caso")
  // tipo: pct (0 a 100), brl (R$ ≥ 0), brlneg (R$, aceita negativo), nota (0 a escala)
  var IND = [
    { id: "ocupacao", r: "Ocupação", tipo: "pct", un: "%", def: "Noites vendidas ÷ noites disponíveis do mês.", onde: "Calendário das plataformas: some as noites vendidas e divida pelas noites disponíveis (unidades × dias).", ex: "46,8", exMeta: "50", mz: "ocupacao" },
    { id: "diaria", r: "Diária média", tipo: "brl", un: "R$", def: "Receita de hospedagem ÷ noites vendidas.", onde: "Relatório de ganhos das plataformas + reservas diretas, sem a taxa de limpeza, dividido pelas noites vendidas.", ex: "280,00", exMeta: "300,00", mz: "diaria" },
    { id: "resultado", r: "Resultado do mês (quanto sobrou)", tipo: "brlneg", un: "R$", def: "Tudo o que entrou menos tudo o que saiu, com a sua retirada dentro (Folha Única, Módulo 2).", onde: "Folha Única do Mês (Módulo 2) ou Painel do Mês (Marco Zero). Pode ser negativo.", ex: "11.890,00 (antes da retirada)", exMeta: "13.000,00", mz: "sobrou" },
    { id: "nota", r: "Nota das avaliações", tipo: "nota", un: "", def: "Média das avaliações do mês no seu principal canal (definição-padrão de hotelaria).", onde: "Painel de avaliações do canal onde você mais vende. Use sempre o mesmo canal.", ex: "4,7 (escala de 5)", exMeta: "4,8", mz: null },
    { id: "vendaDireta", r: "Taxa de venda direta", tipo: "pct", un: "%", def: "Parte da receita de hospedagem que entrou sem plataforma: site, WhatsApp, indicação, hóspede que volta (definição-padrão de hotelaria).", onde: "Some a receita das reservas diretas do mês e divida pela receita de hospedagem.", ex: "12", exMeta: "20", mz: null },
  ];
  var IND_ID = {}; IND.forEach(function (i) { IND_ID[i.id] = i; });

  var DIAS = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"];
  var ONDE = ["Planilha Painel de Gestão", "Caderno", "Quadro na parede", "Outro"];

  // Opções do plano de seis semanas: os outros módulos da Jornada 2 e a ponte para a Jornada 3
  var PILARES = [
    { v: "2", r: "Módulo 2 · Finanças, fluxo de caixa e fechamento" },
    { v: "3", r: "Módulo 3 · Preço, reservas e distribuição" },
    { v: "4", r: "Módulo 4 · Marketing e vendas" },
    { v: "5", r: "Módulo 5 · Pessoas e organização das áreas" },
    { v: "6", r: "Módulo 6 · Compras, estoque e manutenção" },
    { v: "7", r: "Módulo 7 · Qualidade, reputação e plano de crescimento" },
    { v: "J3", r: "Jornada 3 · Operação (limpeza, manutenção e padrão)" },
  ];
  var PILAR = {}; PILARES.forEach(function (p) { PILAR[p.v] = p.r; });
  var SEMANAS = [
    { id: "s12", r: "Semanas 1 e 2 · o pilar mais fraco", p: "Qual é, e qual exercício você vai fazer primeiro?" },
    { id: "s34", r: "Semanas 3 e 4 · o pilar que destrava o seguinte", p: "Qual pilar está impedindo outro de avançar?" },
    { id: "s56", r: "Semanas 5 e 6 · o pilar que te dá um número", p: "Qual deles substitui um achismo por um dado?" },
  ];

  // Exemplo didático · dados fictícios (Cabanas do Vale, continuação do Marco Zero: área frágil = Planejamento e metas)
  var EXEMPLO = {
    situacao: "dono", quem: "so", hospedagem: "Cabanas do Vale (exemplo)", diag: { painel: "nao", metas: "nao", donos: "nao", reuniao: "nao" },
    mesBase: "Outubro de 2026", dias: 31, unidades: 4,
    base_ocupacao: 46.8, base_diaria: 280, base_resultado: 11890, resultadoSemRetirada: true, base_nota: 4.7, escalaNota: "5", base_vendaDireta: 12,
    meta_ocupacao: 50, meta_diaria: 300, meta_resultado: 13000, meta_nota: 4.8, meta_vendaDireta: 20, numeroCorte: "", ocupacaoEquilibrio: "",
    dono_ocupacao: "Ana", dono_diaria: "Ana", dono_resultado: "Ana", dono_nota: "Ana", dono_vendaDireta: "Ana",
    reuniaoDia: "Segunda-feira", reuniaoHora: "08:00", reuniaoDuracao: 30, reuniaoQuem: "Ana, sozinha, com a planilha", reuniaoOnde: "Planilha Painel de Gestão",
    sumisse: "As respostas aos hóspedes e a liberação das cabanas depois da limpeza.",
    s12: "2", s34: "3", s56: "4",
    s12Por: "Fechar outubro na Folha Única e lançar a minha retirada.", s34Por: "Calcular o piso da diária antes de subir para R$ 300.", s56Por: "Anotar o canal de cada reserva para medir a venda direta.",
    depois: "Compras e estoque: já funciona com lista; fica para depois da alta temporada.",
  };

  // Converte "1.234,56", "1234.56", "-500", 1234 em número; vazio ou inválido vira null
  function num(v) {
    if (v == null) return null;
    if (typeof v === "number") return isFinite(v) ? v : null;
    var s = String(v).trim(); if (!s) return null;
    s = s.replace(/\s|R\$|%/g, "").replace(/−/g, "-");
    if (/,/.test(s)) s = s.replace(/\./g, "").replace(",", ".");
    else if (/^-?\d{1,3}(\.\d{3})+$/.test(s)) s = s.replace(/\./g, ""); // "13.000" = treze mil
    if (!/^-?\d*\.?\d+$/.test(s)) return null;
    var n = Number(s); return isFinite(n) ? n : null;
  }
  function informado(v) { return v != null && String(v).trim() !== ""; }
  function escala(S) { return String(S && S.escalaNota) === "10" ? 10 : 5; }

  // Erros de um valor de indicador conforme o tipo (rotulo para a mensagem)
  function errosValor(ind, bruto, S, rotulo) {
    var e = []; if (!informado(bruto)) return e;
    var n = num(bruto);
    if (n == null) { e.push(rotulo + ": escreva só números (use vírgula para centavos)."); return e; }
    if (ind.tipo === "pct" && (n < 0 || n > 100)) e.push(rotulo + ": use um percentual de 0 a 100.");
    if (ind.tipo === "brl" && n < 0) e.push(rotulo + ": não pode ser negativo.");
    if (ind.tipo === "nota" && (n < 0 || n > escala(S))) e.push(rotulo + ": use uma nota de 0 a " + escala(S) + ".");
    return e;
  }

  // Bloqueios por tela (impedem avançar) e avisos (não impedem)
  function validar(S, tela) {
    S = S || {}; var erros = [], avisos = [];
    var t = function (x) { return !tela || tela === x; };
    if (t("partida")) {
      if (!informado(S.mesBase)) erros.push("Falta o mês de partida.");
      var d = num(S.dias), u = num(S.unidades);
      if (!informado(S.dias)) erros.push("Faltam os dias do mês."); else if (d == null || d !== Math.floor(d) || d < 28 || d > 31) erros.push("Dias do mês: use 28, 29, 30 ou 31.");
      if (!informado(S.unidades)) erros.push("Faltam as unidades à venda."); else if (u == null || u !== Math.floor(u) || u < 1 || u > 999) erros.push("Unidades à venda: use um número inteiro de 1 a 999.");
      IND.forEach(function (i) { erros = erros.concat(errosValor(i, S["base_" + i.id], S, "Ponto de partida · " + i.r)); });
      var sem = IND.filter(function (i) { return !informado(S["base_" + i.id]); });
      if (sem.length) avisos.push("Sem ponto de partida em: " + sem.map(function (i) { return i.r.toLowerCase(); }).join(", ") + ". Tudo bem: \"não sei\" é informação. O primeiro mês do painel vira o ponto de partida.");
    }
    if (t("metas")) {
      IND.forEach(function (i) {
        if (!informado(S["meta_" + i.id])) erros.push("Falta a meta de " + i.r.toLowerCase() + ".");
        erros = erros.concat(errosValor(i, S["meta_" + i.id], S, "Meta · " + i.r));
      });
      if (informado(S.meta_ocupacao) && num(S.meta_ocupacao) === 0) erros.push("Meta · Ocupação: precisa ser maior que zero.");
      if (informado(S.meta_diaria) && num(S.meta_diaria) === 0) erros.push("Meta · Diária média: precisa ser maior que zero.");
      if (informado(S.numeroCorte) && num(S.numeroCorte) == null) erros.push("Número de corte: escreva só números.");
      erros = erros.concat(errosValor({ tipo: "pct" }, S.ocupacaoEquilibrio, S, "Ocupação de equilíbrio"));
    }
    if (t("donos")) {
      IND.forEach(function (i) { if (String(S["dono_" + i.id] || "").trim().length < 2) erros.push("Falta o dono de " + i.r.toLowerCase() + "."); });
    }
    if (t("reuniao")) {
      if (DIAS.indexOf(S.reuniaoDia) < 0) erros.push("Escolha o dia da reunião semanal.");
      if (!/^([01]\d|2[0-3]):[0-5]\d$/.test(String(S.reuniaoHora || ""))) erros.push("Escolha a hora da reunião (ex.: 08:00).");
      var m = num(S.reuniaoDuracao);
      if (!informado(S.reuniaoDuracao)) erros.push("Falta a duração da reunião."); else if (m == null || m !== Math.floor(m) || m < 10 || m > 120) erros.push("Duração: use de 10 a 120 minutos.");
      else if (m > 30) avisos.push("A fonte pede trinta minutos. Reunião longa costuma ser a primeira a cair da agenda.");
    }
    if (t("seis")) {
      var esc = SEMANAS.map(function (s) { return S[s.id]; });
      SEMANAS.forEach(function (s, k) { if (!PILAR[esc[k]]) erros.push("Escolha o pilar de " + s.r.split(" · ")[0].toLowerCase() + "."); });
      var vistos = {}; esc.forEach(function (v) { if (PILAR[v]) { if (vistos[v]) erros.push("Escolha três pilares diferentes: \"Escolha três e faça bem\"."); vistos[v] = 1; } });
      if (!informado(S.depois)) avisos.push("Escreva o que vai deixar para depois, de propósito: evita culpa e evita dispersão.");
    }
    var unicos = []; erros.forEach(function (x) { if (unicos.indexOf(x) < 0) unicos.push(x); });
    return { erros: unicos, avisos: avisos, ok: unicos.length === 0 };
  }

  function div(a, b) { return b ? a / b : null; }

  // O painel: ponto de partida, meta, variação e o que as metas pedem
  function calcular(S) {
    S = S || {};
    var dias = num(S.dias) || 0, un = num(S.unidades) || 0, disp = dias * un;
    var linhas = IND.map(function (i) {
      var b = num(S["base_" + i.id]), m = num(S["meta_" + i.id]);
      var dono = String(S["dono_" + i.id] || "").trim();
      var v = b != null && m != null ? m - b : null;
      var sit = m == null ? "sem-meta" : b == null ? "sem-base" : m > b + 1e-9 ? "acima" : Math.abs(m - b) <= 1e-9 ? "igual" : "abaixo";
      return { id: i.id, r: i.r, tipo: i.tipo, base: b, meta: m, dono: dono, variacao: v, variacaoPct: b != null && m != null && b !== 0 ? (m - b) / Math.abs(b) : null, situacao: sit };
    });
    var L = {}; linhas.forEach(function (l) { L[l.id] = l; });
    var noitesMeta = L.ocupacao.meta != null && disp ? L.ocupacao.meta / 100 * disp : null;
    var receitaMeta = noitesMeta != null && L.diaria.meta != null ? noitesMeta * L.diaria.meta : null;
    var rpdBase = L.ocupacao.base != null && L.diaria.base != null ? L.ocupacao.base / 100 * L.diaria.base : null;
    var rpdMeta = L.ocupacao.meta != null && L.diaria.meta != null ? L.ocupacao.meta / 100 * L.diaria.meta : null;
    var varReceita = rpdBase && rpdMeta != null ? rpdMeta / rpdBase - 1 : null;
    var sabidos = linhas.filter(function (l) { return l.base != null; }).length;
    var corte = num(S.numeroCorte), equil = num(S.ocupacaoEquilibrio);
    return { noitesDisponiveis: disp, linhas: linhas, L: L, noitesMeta: noitesMeta, receitaMeta: receitaMeta, receitaPorNoiteDispBase: rpdBase, receitaPorNoiteDispMeta: rpdMeta,
      variacaoReceita: varReceita, sabidos: sabidos, numeroCorte: corte, ocupacaoEquilibrio: equil, escala: escala(S), duracao: num(S.reuniaoDuracao) };
  }

  // Formatação (sem DOM)
  function brl(v) { if (v == null || !isFinite(v)) return "—"; var neg = v < 0; var s = Math.abs(v).toFixed(2).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, "."); return (neg ? "−R$ " : "R$ ") + s; }
  function dec(v, d) { if (v == null || !isFinite(v)) return "—"; var neg = v < 0; var s = Math.abs(v).toFixed(d == null ? 1 : d).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d)(?=,|$))/g, "."); return (neg ? "−" : "") + s; }
  function pct(v, d) { if (v == null || !isFinite(v)) return "—"; return dec(v * 100, d == null ? 1 : d) + "%"; }
  function valor(tipo, v, esc) {
    if (v == null) return "não sei";
    if (tipo === "pct") return dec(v, 1) + "%";
    if (tipo === "nota") return dec(v, 1) + " de " + (esc || 5);
    return brl(v);
  }
  function variacaoTxt(l, esc) {
    if (l.variacao == null) return l.base == null ? "sem ponto de partida" : "";
    var sinal = l.variacao > 1e-9 ? "+" : l.variacao < -1e-9 ? "−" : "";
    var a = Math.abs(l.variacao);
    var base = l.tipo === "pct" || l.tipo === "nota" ? dec(a, 1) + (a < 2 ? " ponto" : " pontos") : brl(a);
    if (!sinal) return "manter";
    return sinal + " " + base + (l.variacaoPct != null && l.tipo !== "pct" ? " (" + (sinal === "−" ? "−" : "+") + pct(Math.abs(l.variacaoPct)) + ")" : "");
  }

  // As leituras (o que isso significa)
  var LEIT_SIT = {
    acima: "meta acima do ponto de partida",
    igual: "manter o número: é uma meta válida, desde que escrita",
    abaixo: "meta abaixo do ponto de partida",
    "sem-base": "sem ponto de partida: o primeiro mês do painel vira a base",
    "sem-meta": "sem meta",
  };
  function leituras(r, S) {
    var out = [];
    out.push(r.sabidos === 5 ? "Você tem os cinco números do ponto de partida. Agora o painel compara cada mês com a meta e com o mesmo mês do ano anterior."
      : "Você sabe " + r.sabidos + " de 5 números do ponto de partida. Os que faltam não impedem o painel: eles entram na primeira reunião.");
    if (r.receitaMeta != null) out.push("As metas de ocupação e de diária pedem cerca de " + dec(r.noitesMeta, 0) + " noites vendidas e " + brl(r.receitaMeta) + " de hospedagem no mês de chegada" +
      (r.variacaoReceita != null ? ", " + pct(Math.abs(r.variacaoReceita)) + (r.variacaoReceita >= 0 ? " acima" : " abaixo") + " do ponto de partida (ocupação × diária)." : "."));
    out.push("Cada meta vale para o mesmo mês daqui a 12 meses" + (S && S.mesBase ? " (o mês de partida é " + String(S.mesBase).trim() + ")" : "") + ". Em hospedagem sazonal, compare sempre o mesmo mês: junho contra junho, nunca contra maio.");
    return out;
  }

  // Atenção: regras em ordem (ids testados)
  function atencao(r, S) {
    S = S || {}; var a = [];
    if (S.resultadoSemRetirada) a.push({ id: "semRetirada", r: "Resultado sem a sua retirada", t: "O ponto de partida do resultado está antes da sua retirada, e a meta também. Quando fizer a Folha Única (Módulo 2), refaça as duas com a retirada dentro: sem ela, o resultado mente." });
    if (r.ocupacaoEquilibrio != null && r.L.ocupacao.meta != null && r.L.ocupacao.meta < r.ocupacaoEquilibrio) a.push({ id: "equilibrio", r: "Meta de ocupação abaixo do ponto de equilíbrio", t: "A meta de ocupação (" + dec(r.L.ocupacao.meta, 1) + "%) fica abaixo da ocupação de equilíbrio (" + dec(r.ocupacaoEquilibrio, 1) + "%): nesse mês, as noites vendidas não pagariam o custo fixo. Suba a meta ou reveja diária e custos." });
    if (r.numeroCorte != null && r.L.resultado.meta != null && r.L.resultado.meta < r.numeroCorte) a.push({ id: "corte", r: "Meta de resultado abaixo do número de corte", t: "A meta de resultado (" + brl(r.L.resultado.meta) + ") fica abaixo do seu número de corte (" + brl(r.numeroCorte) + "), o resultado mínimo abaixo do qual você muda alguma coisa. A meta precisa ficar acima do corte." });
    var semBase = r.linhas.filter(function (l) { return l.situacao === "sem-base"; });
    if (semBase.length) a.push({ id: "semBase", r: "Números sem ponto de partida", t: "Sem ponto de partida em " + semBase.map(function (l) { return l.r.toLowerCase(); }).join(", ") + ". Anote esses números na primeira reunião: eles viram a base e a meta é revista no fim do primeiro mês." });
    var abaixo = r.linhas.filter(function (l) { return l.situacao === "abaixo"; });
    if (abaixo.length) a.push({ id: "abaixo", r: "Meta abaixo do ponto de partida", t: "Meta menor que o ponto de partida em " + abaixo.map(function (l) { return l.r.toLowerCase(); }).join(", ") + ". Pode ser decisão (trocar ocupação por diária: ocupação é vaidade, margem é sobrevivência). Se for, escreva o porquê ao lado; se não for, revise." });
    var donos = IND.map(function (i) { return String(S["dono_" + i.id] || "").trim().toLowerCase(); });
    if ((S.quem === "dupla" || S.quem === "equipe") && donos[0] && donos.every(function (d) { return d === donos[0]; })) a.push({ id: "donoUnico", r: "Os cinco números com a mesma pessoa", t: "Você tem com quem dividir e os cinco números estão com uma pessoa só. Dar um número a quem cuida daquela área tira você do caminho das decisões pequenas." });
    if (r.duracao != null && r.duracao > 30) a.push({ id: "longa", r: "Reunião acima de trinta minutos", t: "A fonte pede trinta minutos, mesmos cinco números, mesma hora. Reunião longa é a primeira a cair da agenda." });
    return a;
  }
  var ERRO_COMUM = "Não troque de indicador antes de completar 12 semanas. O valor vem da série histórica, e série histórica exige repetir o mesmo número.";

  // O que fazer: o plano sugerido (vira o texto editável da ação)
  function planoSugerido(S, r) {
    S = S || {}; r = r || calcular(S); var p = [];
    p.push("Marcar na agenda a reunião semanal: toda " + String(S.reuniaoDia || "semana").toLowerCase() + (S.reuniaoHora ? " às " + S.reuniaoHora : "") + ", " + (num(S.reuniaoDuracao) || 30) + " minutos, com os mesmos cinco números na mesa.");
    var semBase = r.linhas.filter(function (l) { return l.situacao === "sem-base"; });
    if (semBase.length) p.push("Na primeira reunião, anotar o ponto de partida que falta: " + semBase.map(function (l) { return l.r.toLowerCase(); }).join(", ") + ".");
    SEMANAS.forEach(function (s) { if (PILAR[S[s.id]]) p.push(s.r.split(" · ")[0] + ": " + PILAR[S[s.id]] + (informado(S[s.id + "Por"]) ? ". " + String(S[s.id + "Por"]).trim().replace(/\.$/, "") + "." : ".")); });
    return p.map(function (x, k) { return (k + 1) + ". " + x; }).join("\n");
  }
  function comoVerificar(r, S) {
    var t = "Daqui a quatro semanas, a aba Reunião semanal da planilha tem quatro linhas com os mesmos cinco números e um dono em cada um. No fim das seis semanas, os três pilares do plano têm o exercício feito.";
    if (r && r.linhas.some(function (l) { return l.situacao === "sem-base"; })) t += " Os números que faltavam já têm ponto de partida.";
    if (S && S.resultadoSemRetirada) t += " O resultado foi refeito com a retirada dentro.";
    return t + " Daqui a 12 meses, compare o mesmo mês com a meta.";
  }

  // Painel preenchido (dá para mostrar o resultado) e lição concluída (selo)
  var TELAS = ["abertura", "partida", "metas", "donos", "reuniao", "seis", "resultado"];
  var TITULOS = { partida: "O ponto de partida", metas: "As metas de 12 meses", donos: "Quem olha cada número", reuniao: "A reunião semanal", seis: "O plano de seis semanas" };
  function completo(S) {
    S = S || {};
    if (!S.situacao || !S.quem) return false;
    return ["partida", "metas", "donos", "reuniao", "seis"].every(function (t) { return validar(S, t).ok; });
  }
  function acaoOk(S) { return !!(S && S.acao && String(S.acao).trim().length >= 10); }
  function concluido(S) { return completo(S) && acaoOk(S) && !!(S && S.prazo) && !!(S && S.pdf); }
  function pendencias(S) {
    var p = [];
    if (!completo(S)) p.push("o painel preenchido (cinco metas, cinco donos, a reunião e o plano de seis semanas)");
    if (!acaoOk(S)) p.push("o plano com pelo menos 10 letras");
    if (!(S && S.prazo)) p.push("a data da primeira reunião");
    if (!(S && S.pdf)) p.push("o PDF baixado");
    return p;
  }
  function proximaVazia(S) {
    for (var k = 1; k < TELAS.length - 1; k++) if (!validar(S, TELAS[k]).ok) return TELAS[k];
    return "resultado";
  }

  // Linhas do painel para a tabela e o PDF
  function painel(r) {
    return r.linhas.map(function (l) {
      return { id: l.id, r: l.r, dono: l.dono || "sem dono", base: valor(l.tipo, l.base, r.escala), meta: valor(l.tipo, l.meta, r.escala), variacao: variacaoTxt(l, r.escala), leitura: LEIT_SIT[l.situacao] };
    });
  }

  // Lê a Folha Única do Módulo 2 (se existir) para sugerir o ponto de partida. ZF = window.ZF (logic do módulo 2).
  function daFolha(folha, ZF) {
    if (!folha || !ZF || !ZF.completo || !ZF.completo(folha)) return null;
    var f = ZF.calcular(folha), N = f.N;
    return {
      mesBase: N.mes || "", dias: N.dias, unidades: N.unidades,
      base_ocupacao: Math.round(f.ocupacao * 1000) / 10, base_diaria: f.diariaMediaBruta == null ? "" : Math.round(f.diariaMediaBruta * 100) / 100,
      base_resultado: Math.round(f.resultadoOperacional * 100) / 100, resultadoSemRetirada: false,
      ocupacaoEquilibrio: f.ocupacaoEquilibrio == null ? "" : Math.round(f.ocupacaoEquilibrio * 1000) / 10,
    };
  }

  var PROXIMO = { n: 2, t: "Finanças, fluxo de caixa e fechamento" };
  var api = { SITUACOES: SITUACOES, QUEM: QUEM, DIAG: DIAG, SIMNAO: SIMNAO, NIVEIS: NIVEIS, IND: IND, IND_ID: IND_ID, DIAS: DIAS, ONDE: ONDE, PILARES: PILARES, PILAR: PILAR, SEMANAS: SEMANAS,
    EXEMPLO: EXEMPLO, TELAS: TELAS, TITULOS: TITULOS, PROXIMO: PROXIMO, ERRO_COMUM: ERRO_COMUM, LEIT_SIT: LEIT_SIT,
    num: num, validar: validar, calcular: calcular, leituras: leituras, atencao: atencao, planoSugerido: planoSugerido, comoVerificar: comoVerificar,
    completo: completo, concluido: concluido, pendencias: pendencias, proximaVazia: proximaVazia, nivelPainel: nivelPainel, painel: painel, daFolha: daFolha,
    brl: brl, dec: dec, pct: pct, valor: valor, variacaoTxt: variacaoTxt };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else raiz.ZP = api;
})(typeof window !== "undefined" ? window : this);

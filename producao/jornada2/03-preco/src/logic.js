/* Jornada 2 · Gestão · Módulo 3 · Preço, reservas e distribuição
   Lógica pura da ficha "A minha Tabela de Preço e Canais". Sem DOM: roda no navegador (window.ZP) e no Node (testes).
   Regra: tudo que a ficha afirma sai daqui, para ser testado. Nenhuma nota: só as regras das fontes.
   Fontes: Panorama · Trilha B · G2 e G3; Jornada do COMO · Etapa 08 (diária de referência, cinco faixas, datas de pico,
   política de desconto) e Etapa 09 (custo por noite vendida, três faixas do desconto, margem por canal).
   Fatores das faixas são "ponto de partida" da fonte, sempre ajustáveis pelo levantamento do destino. */
(function (raiz) {
  "use strict";

  // Faixas e fatores de partida (Etapa 08 · Passo 05). Base é sempre 1,00.
  var FAIXAS = [
    { id: "vale", r: "Vale", min: 0.70, max: 0.80, padrao: 0.75, t: "Meses de baixa, meio de semana" },
    { id: "baixa", r: "Baixa", min: 0.85, max: 0.95, padrao: 0.90, t: "Baixa no fim de semana e meio de semana de meses médios" },
    { id: "base", r: "Base", min: 1, max: 1, padrao: 1, t: "A própria diária de referência: fim de semana comum" },
    { id: "alta", r: "Alta", min: 1.35, max: 1.60, padrao: 1.50, t: "Temporada e feriados simples" },
    { id: "pico", r: "Pico", min: 1.90, max: 2.60, padrao: 2.20, t: "Réveillon, carnaval, feriados prolongados e eventos" },
  ];
  var FAIXA = {}; FAIXAS.forEach(function (f) { FAIXA[f.id] = f; });
  var FAIXAS_MES = ["vale", "baixa", "base", "alta"]; // o pico entra como data própria
  var TERCOS = [
    { v: "baixo", r: "Terço de baixo (cerca de 15% abaixo da média)", f: 0.85 },
    { v: "meio", r: "Meio (a própria média)", f: 1 },
    { v: "cima", r: "Terço de cima (cerca de 20% acima da média)", f: 1.20 },
  ];
  var MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
  var MESES_C = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];

  var SITUACOES = [
    { v: "abrir", r: "Ainda vou abrir a minha hospedagem (vou preencher com os números previstos)", curto: "vai abrir" },
    { v: "dono", r: "Já opero a minha hospedagem e quero acertar o preço e os canais", curto: "dono que opera" },
    { v: "operador", r: "Cuido da hospedagem de outra pessoa e preciso propor a tabela ao dono", curto: "operador" },
  ];
  var DIAG = [
    { id: "varia", r: "O seu preço muda ao longo do ano, com faixas definidas antes de a data chegar?" },
    { id: "piso", r: "Existe um piso escrito, que todo mundo que atende conhece?" },
    { id: "liquido", r: "Você sabe quanto sobra de uma noite em cada canal, depois da comissão?" },
    { id: "direta", r: "Você tem uma meta de venda direta, com número e prazo?" },
  ];
  var SIMNAO = [{ v: "sim", r: "Sim" }, { v: "nao", r: "Não" }];
  var NIVEIS = [
    { n: 1, r: "Preço no improviso", t: "Hoje o preço é decidido na hora, sem piso e sem saber quanto cada canal deixa. A Tabela é o primeiro corte." },
    { n: 2, r: "Começando a organizar", t: "Uma parte existe, mas faltam números para decidir. A Tabela mostra o piso, o calendário e o líquido por canal." },
    { n: 3, r: "Quase organizado", t: "Falta pouco: uma regra ou um número. A Tabela mostra qual e onde ele entra." },
    { n: 4, r: "Preço com método", t: "Faixas, piso, líquido por canal e meta existem. A Tabela serve para revisar a cada trimestre." },
  ];
  function nivel(S) {
    var d = (S && S.diag) || {}, sim = 0;
    DIAG.forEach(function (q) { if (d[q.id] === "sim") sim++; });
    return NIVEIS[Math.max(0, sim - 1)];
  }

  // Campos simples (os canais, os meses e as datas de pico são listas à parte)
  var CAMPOS = [
    { id: "custoVariavelNoite", tela: "custo", tipo: "brl", obrig: true, r: "Custo variável por noite", pq: "O que cada noite leva embora ao ser vendida: limpeza por estadia, enxoval, amenidades, energia da unidade, quebra.", onde: "Na sua Folha Única do Mês (Módulo 2), linha \"custo variável por noite\".", ex: "28,32" },
    { id: "custoNoiteVendida", tela: "custo", tipo: "brl", obrig: true, r: "Custo por noite vendida", pq: "Variável por noite mais todo o custo fixo dividido pelas noites vendidas. Abaixo dele, vender não paga tudo.", onde: "Na sua Folha Única do Mês (Módulo 2). Para decidir a tabela do ano, o ideal é a média do ano.", ex: "153,03" },
    { id: "diariaAtual", tela: "custo", tipo: "brl", r: "Diária média que você pratica hoje", pq: "Para comparar com a diária média do calendário que você vai montar.", onde: "Receita de hospedagem ÷ noites vendidas de um mês comum.", ex: "280,00" },
    { id: "noitesPorEstadia", tela: "custo", tipo: "dec", r: "Noites por estadia (média)", pq: "Custos por reserva, como uma taxa fixa de canal, se dividem pelas noites da estadia.", onde: "Noites vendidas ÷ número de estadias do mês.", ex: "2,32" },
    { id: "receitaMes", tela: "custo", tipo: "brl", r: "Receita de hospedagem de um mês comum", pq: "Serve só para mostrar, em reais, o que a meta de venda direta muda na comissão.", onde: "Na Folha Única do Mês: receita de hospedagem (bruta).", ex: "16.240,00" },
    { id: "impostoPct", tela: "canais", tipo: "pct", r: "Imposto sobre a receita (%)", pq: "Sai de toda reserva, em qualquer canal.", onde: "Guia do mês ou o seu contador.", ex: "6" },
    { id: "referencia", tela: "referencia", tipo: "brl", obrig: true, r: "A minha diária de referência", pq: "O preço cheio, sem desconto e sem condição. Todo o calendário sai dele.", onde: "A média dos concorrentes diretos sem o mais caro e o mais barato, ajustada à posição que você escolheu.", ex: "300,00" },
    { id: "margemMinima", tela: "piso", tipo: "pct", r: "Margem mínima que justifica abrir a porta (%)", pq: "O piso não é o custo: é o custo mais uma margem mínima. Quem decide esta margem é você.", onde: "Uma decisão sua. No exemplo didático, 10%.", ex: "10" },
    { id: "pisoDeclarado", tela: "piso", tipo: "brl", obrig: true, r: "O meu piso, por escrito (R$)", pq: "O menor valor pelo qual você vende, em qualquer situação, inclusive na véspera.", onde: "O piso calculado acima, arredondado para cima.", ex: "225,00" },
    { id: "quemConhece", tela: "piso", tipo: "texto", r: "Quem já sabe do piso", pq: "Piso que só existe na sua cabeça não é piso.", onde: "Todo mundo que responde hóspede: você, a recepção, quem atende o WhatsApp.", ex: "Eu e quem responde o WhatsApp" },
    { id: "ano", tela: "calendario", tipo: "int", min: 2024, max: 2099, obrig: true, r: "Ano em que o calendário começa", pq: "Para contar as sextas e os sábados de cada mês.", onde: "O próximo ano de vendas.", ex: "2027" },
    { id: "metaDireta", tela: "picos", tipo: "pct", obrig: true, r: "Meta de venda direta (% da receita)", pq: "Um número, não uma intenção. Na venda direta, a comissão fica com você.", onde: "Hoje você vende o percentual que aparece abaixo. Escolha onde quer chegar.", ex: "40" },
    { id: "prazoMeta", tela: "picos", tipo: "data", obrig: true, r: "Até quando", pq: "Meta sem prazo vira intenção.", onde: "Uma data realista, de três a doze meses.", ex: "30/06/2027" },
  ];
  var CAMPO = {}; CAMPOS.forEach(function (c) { CAMPO[c.id] = c; });

  // Exemplo didático · dados fictícios (Cabanas do Vale, a mesma do Marco Zero e da Folha Única)
  var EXEMPLO = {
    situacao: "dono", hospedagem: "Cabanas do Vale (exemplo)", diag: { varia: "nao", piso: "nao", liquido: "nao", direta: "sim" },
    custoVariavelNoite: 28.32, custoNoiteVendida: 153.03, diariaAtual: 280, noitesPorEstadia: 2.32, receitaMes: 16240,
    impostoPct: 6, gestorCanais: true, motorReservas: false,
    canais: [
      { nome: "Plataforma A", mix: 50, comissao: 16, pagamento: 1.5, extra: 0, direta: false },
      { nome: "Plataforma B", mix: 20, comissao: 15, pagamento: 1.5, extra: 0, direta: false },
      { nome: "Venda direta (site e WhatsApp)", mix: 30, comissao: 0, pagamento: 1.5, extra: 0, direta: true },
    ],
    concorrentes: [270, 280, 290, 300, 310, 320, 360], terco: "meio", referencia: 300,
    margemMinima: 10, pisoDeclarado: 225, quemConhece: "Eu e quem responde o WhatsApp",
    condicoes: ["Terceira noite com café da manhã incluso", "Saída tardia até as 14 h", "Cesta de boas-vindas com produtos da região"],
    fatores: { vale: 0.75, baixa: 0.90, alta: 1.50, pico: 2.20 },
    ano: 2027, mesInicio: 1,
    meses: [["baixa", "base"], ["baixa", "base"], ["vale", "baixa"], ["vale", "baixa"], ["vale", "base"], ["base", "alta"], ["alta", "alta"], ["base", "alta"], ["baixa", "base"], ["baixa", "base"], ["vale", "baixa"], ["baixa", "base"]]
      .map(function (m) { return { sem: m[0], fds: m[1] }; }),
    picos: [
      { nome: "Carnaval", mes: 2, noites: 4, fator: 2.2, minimo: 4 },
      { nome: "Corpus Christi (feriado prolongado)", mes: 5, noites: 4, fator: 1.9, minimo: 3 },
      { nome: "Festival de inverno (evento local)", mes: 7, noites: 3, fator: 2.0, minimo: 2 },
      { nome: "Réveillon", mes: 12, noites: 5, fator: 2.4, minimo: 5 },
    ],
    metaDireta: 40, prazoMeta: "2027-06-30",
  };

  function num(v) {
    if (v == null) return null;
    if (typeof v === "number") return isFinite(v) ? v : null;
    var s = String(v).trim(); if (!s) return null;
    s = s.replace(/\s|R\$|%/g, "");
    if (/,/.test(s)) s = s.replace(/\./g, "").replace(",", ".");
    var n = Number(s); return isFinite(n) ? n : null;
  }
  function informado(v) { return v != null && String(v).trim() !== ""; }
  function r2(v) { return Math.round(v * 100) / 100; }

  // Noites de um mês: total, fim de semana (noites de sexta e de sábado) e meio de semana
  function noitesDoMes(ano, mes) {
    var dias = new Date(Date.UTC(ano, mes, 0)).getUTCDate(), fds = 0;
    for (var d = 1; d <= dias; d++) { var w = new Date(Date.UTC(ano, mes - 1, d)).getUTCDay(); if (w === 5 || w === 6) fds++; }
    return { dias: dias, fds: fds, sem: dias - fds };
  }
  // Os doze meses da janela: [{ano, mes}]
  function janela(ano, mesInicio) {
    var a = []; for (var i = 0; i < 12; i++) { var m = mesInicio - 1 + i; a.push({ ano: ano + Math.floor(m / 12), mes: (m % 12) + 1 }); } return a;
  }

  function normalizar(S) {
    S = S || {}; var N = { informado: {} };
    CAMPOS.forEach(function (c) {
      var v = S[c.id]; N.informado[c.id] = informado(v);
      if (c.tipo === "texto" || c.tipo === "data") N[c.id] = v == null ? "" : String(v).trim();
      else { var n = num(v); N[c.id] = n == null ? 0 : n; }
    });
    N.mesInicio = Math.min(12, Math.max(1, Math.floor(num(S.mesInicio) || 1)));
    N.nE = N.noitesPorEstadia > 0 ? N.noitesPorEstadia : 1;
    N.gestorCanais = !!S.gestorCanais; N.motorReservas = !!S.motorReservas;
    N.canais = (S.canais || []).map(function (c) {
      c = c || {};
      return { nome: String(c.nome == null ? "" : c.nome).trim(), mix: num(c.mix) || 0, comissao: num(c.comissao) || 0, pagamento: num(c.pagamento) || 0, extra: num(c.extra) || 0, direta: !!c.direta,
        informado: informado(c.nome) || informado(c.mix) || informado(c.comissao), mixInf: informado(c.mix), bruto: c };
    }).filter(function (c) { return c.informado; });
    N.concorrentes = (S.concorrentes || []).map(num).filter(function (v) { return v != null && v > 0; });
    N.terco = S.terco || "meio";
    var fz = S.fatores || {};
    N.fatores = { base: 1 };
    ["vale", "baixa", "alta", "pico"].forEach(function (k) { var n = num(fz[k]); N.fatores[k] = n == null ? FAIXA[k].padrao : n; });
    N.meses = []; for (var i = 0; i < 12; i++) { var m = (S.meses || [])[i] || {}; N.meses.push({ sem: FAIXA[m.sem] ? m.sem : "", fds: FAIXA[m.fds] ? m.fds : "" }); }
    N.picos = (S.picos || []).map(function (p) {
      p = p || {}; return { nome: String(p.nome == null ? "" : p.nome).trim(), mes: Math.floor(num(p.mes) || 0), noites: num(p.noites) || 0, fator: num(p.fator), minimo: num(p.minimo) || 0, informado: informado(p.nome) || informado(p.noites) };
    }).filter(function (p) { return p.informado; });
    N.condicoes = (S.condicoes || []).map(function (c) { return String(c == null ? "" : c).trim(); }).filter(Boolean);
    N.vaiAbrir = S.situacao === "abrir";
    return N;
  }

  function dedCanal(c, N) { return c.comissao + c.pagamento + N.impostoPct; }

  // Bloqueios por tela e avisos
  function validar(S, tela) {
    var N = normalizar(S), erros = [], avisos = [];
    CAMPOS.forEach(function (c) {
      if (tela && c.tela !== tela) return;
      if (c.tipo === "texto") return;
      if (c.tipo === "data") { if (c.obrig && !N[c.id]) erros.push("Falta " + c.r.toLowerCase() + "."); return; }
      var bruto = S ? S[c.id] : null;
      if (c.obrig && !N.informado[c.id]) erros.push("Falta " + c.r.toLowerCase() + ".");
      if (informado(bruto) && num(bruto) == null) erros.push(c.r + ": escreva só números (use vírgula para centavos).");
      if (N[c.id] < 0) erros.push(c.r + ": não pode ser negativo.");
      if (c.tipo === "pct" && N[c.id] > 99.9) erros.push(c.r + ": use um percentual de 0 a 99,9.");
      if (c.tipo === "int" && N.informado[c.id] && N[c.id] !== Math.floor(N[c.id])) erros.push(c.r + ": use um número inteiro.");
      if (c.min != null && N.informado[c.id] && N[c.id] < c.min) erros.push(c.r + ": o mínimo é " + c.min + ".");
      if (c.max != null && N.informado[c.id] && N[c.id] > c.max) erros.push(c.r + ": o máximo é " + c.max + ".");
    });
    if (!tela || tela === "custo") {
      if (N.informado.custoVariavelNoite && N.informado.custoNoiteVendida && N.custoNoiteVendida < N.custoVariavelNoite) erros.push("O custo por noite vendida não pode ser menor que o custo variável por noite: ele é o variável mais o fixo.");
      if (!N.informado.noitesPorEstadia) avisos.push("Sem as noites por estadia, a ficha divide os custos por reserva por uma noite. Confira na Folha do Módulo 2.");
    }
    if (!tela || tela === "canais") {
      if (!N.canais.length) erros.push("Informe pelo menos um canal de venda.");
      var soma = 0;
      N.canais.forEach(function (c, i) {
        var nm = c.nome || "Canal " + (i + 1);
        if (!c.nome) erros.push("Canal " + (i + 1) + ": falta o nome.");
        ["mix", "comissao", "pagamento", "extra"].forEach(function (k) { var b = c.bruto[k]; if (informado(b) && num(b) == null) erros.push(nm + ": escreva só números."); });
        if (c.mix < 0 || c.comissao < 0 || c.pagamento < 0 || c.extra < 0) erros.push(nm + ": nenhum valor pode ser negativo.");
        if (dedCanal(c, N) >= 100) erros.push(nm + ": comissão, pagamento e imposto somam 100% ou mais.");
        if (c.direta && c.comissao > 0) avisos.push(nm + ": marcado como venda direta, mas com comissão. Confira.");
        soma += c.mix;
      });
      if (N.canais.length && Math.abs(soma - 100) > 0.05) erros.push("O mix de canais soma " + dec(soma, 1) + "%: precisa somar 100%.");
      if (!N.canais.some(function (c) { return c.direta; })) avisos.push("Nenhum canal está marcado como venda direta. Se você não vende direto hoje, inclua a linha com 0%.");
    }
    if (!tela || tela === "referencia") {
      if (N.concorrentes.length > 0 && N.concorrentes.length < 3) avisos.push("Com menos de três concorrentes não dá para descartar o mais caro e o mais barato. A fonte pede de seis a nove.");
      else if (N.concorrentes.length >= 3 && N.concorrentes.length < 6) avisos.push("A fonte pede de seis a nove concorrentes diretos. Com " + N.concorrentes.length + ", a média é frágil.");
      (S && S.concorrentes || []).forEach(function (v, i) { if (informado(v) && (num(v) == null || num(v) < 0)) erros.push("Concorrente " + (i + 1) + ": escreva um valor válido."); });
    }
    if (!tela || tela === "piso") {
      var c0 = calcularBase(N);
      if (N.informado.pisoDeclarado && c0.pisoCusto != null && N.pisoDeclarado < c0.pisoCusto - 0.005) avisos.push("O seu piso (" + brl(N.pisoDeclarado) + ") fica abaixo do custo da noite no canal mais caro (" + brl(c0.pisoCusto) + "). Cada venda no piso não paga tudo.");
      if (N.informado.pisoDeclarado && N.informado.referencia && N.pisoDeclarado > N.referencia) erros.push("O piso não pode ser maior que a diária de referência.");
    }
    if (!tela || tela === "calendario") {
      ["vale", "baixa", "alta", "pico"].forEach(function (k) {
        var b = S && S.fatores ? S.fatores[k] : null;
        if (informado(b) && (num(b) == null || num(b) <= 0)) erros.push("Fator " + FAIXA[k].r.toLowerCase() + ": use um número maior que zero.");
        else if (num(b) != null && num(b) > 5) erros.push("Fator " + FAIXA[k].r.toLowerCase() + ": o máximo é 5.");
        else { var f = N.fatores[k]; if (f < FAIXA[k].min - 1e-9 || f > FAIXA[k].max + 1e-9) avisos.push("Fator " + FAIXA[k].r.toLowerCase() + " (" + dec(f, 2) + ") fora do ponto de partida da fonte (" + dec(FAIXA[k].min, 2) + " a " + dec(FAIXA[k].max, 2) + "). Vale se o seu levantamento mostrar isso."); }
      });
      var faltam = N.meses.filter(function (m) { return !m.sem || !m.fds; }).length;
      if (faltam) erros.push("Escolha a faixa de meio de semana e de fim de semana dos doze meses (faltam " + faltam + ").");
    }
    if (!tela || tela === "picos") {
      var J = N.informado.ano ? janela(N.ano, N.mesInicio) : null;
      var porMes = {};
      N.picos.forEach(function (p, i) {
        var nm = p.nome || "Data " + (i + 1);
        if (!p.nome) erros.push("Data de pico " + (i + 1) + ": falta o nome.");
        if (p.mes < 1 || p.mes > 12) erros.push(nm + ": escolha o mês.");
        if (!(p.noites >= 1) || p.noites !== Math.floor(p.noites)) erros.push(nm + ": noites precisa ser um número inteiro a partir de 1.");
        if (p.fator == null || p.fator <= 0 || p.fator > 5) erros.push(nm + ": fator de 0,01 a 5.");
        if (p.minimo < 0 || p.minimo !== Math.floor(p.minimo)) erros.push(nm + ": mínimo de noites inteiro.");
        if (p.minimo > p.noites && p.noites >= 1) avisos.push(nm + ": o mínimo de noites passa das noites da data.");
        porMes[p.mes] = (porMes[p.mes] || 0) + p.noites;
      });
      if (J) Object.keys(porMes).forEach(function (m) { var a = J.filter(function (x) { return x.mes === +m; })[0]; if (a && porMes[m] > noitesDoMes(a.ano, a.mes).dias) erros.push("As datas de pico de " + MESES[m - 1] + " passam dos dias do mês."); });
      if (!N.picos.length) avisos.push("Nenhuma data de pico: réveillon, carnaval, feriados prolongados e eventos locais pedem preço próprio.");
    }
    return { erros: erros, avisos: avisos, ok: erros.length === 0 };
  }

  function div(a, b) { return b > 0 ? a / b : null; }

  // Canais e piso (precisa só do custo, dos canais e da margem)
  function calcularBase(N) {
    var r = {};
    r.canais = N.canais.map(function (c) {
      var ded = dedCanal(c, N), fator = 1 - ded / 100;
      var liq = N.referencia > 0 ? N.referencia * fator - c.extra / N.nE : null;
      return { nome: c.nome, mix: c.mix, comissao: c.comissao, pagamento: c.pagamento, extra: c.extra, direta: c.direta, ded: ded,
        liquidoNoite: liq, margemNoite: liq == null ? null : liq - N.custoVariavelNoite,
        pisoCusto: fator > 0 ? (N.custoNoiteVendida + c.extra / N.nE) / fator : null,
        limiteVariavel: fator > 0 ? (N.custoVariavelNoite + c.extra / N.nE) / fator : null };
    });
    var ativos = r.canais.filter(function (c) { return c.mix > 0; });
    if (!ativos.length) ativos = r.canais;
    r.canalCritico = null;
    ativos.forEach(function (c) { if (c.pisoCusto != null && (!r.canalCritico || c.pisoCusto > r.canalCritico.pisoCusto)) r.canalCritico = c; });
    r.pisoCusto = r.canalCritico ? r.canalCritico.pisoCusto : (N.custoNoiteVendida > 0 ? N.custoNoiteVendida / (1 - N.impostoPct / 100) : null);
    r.limiteVariavel = r.canalCritico ? r.canalCritico.limiteVariavel : null;
    r.pisoCalculado = r.pisoCusto == null ? null : r.pisoCusto * (1 + N.margemMinima / 100);
    r.comissaoMedia = r.canais.reduce(function (s, c) { return s + c.mix * c.comissao / 100; }, 0);
    r.dedMedia = r.canais.reduce(function (s, c) { return s + c.mix * c.ded / 100; }, 0);
    r.diretaAtual = r.canais.filter(function (c) { return c.direta; }).reduce(function (s, c) { return s + c.mix; }, 0);
    var pagos = r.canais.filter(function (c) { return !c.direta && c.mix > 0; }), mixPagos = pagos.reduce(function (s, c) { return s + c.mix; }, 0);
    r.comissaoMediaPagos = mixPagos > 0 ? pagos.reduce(function (s, c) { return s + c.mix * c.comissao; }, 0) / mixPagos : 0;
    r.canaisPagosAtivos = pagos.length;
    r.melhorCanal = null; r.piorCanal = null;
    r.canais.forEach(function (c) { if (c.margemNoite == null) return; if (!r.melhorCanal || c.margemNoite > r.melhorCanal.margemNoite) r.melhorCanal = c; if (!r.piorCanal || c.margemNoite < r.piorCanal.margemNoite) r.piorCanal = c; });
    r.diferencaMelhorPior = r.melhorCanal && r.piorCanal ? r.melhorCanal.margemNoite - r.piorCanal.margemNoite : null;
    return r;
  }

  // Média do mercado: descarta o mais caro e o mais barato (Etapa 08 · Passo 03)
  function mercado(N) {
    var v = N.concorrentes.slice().sort(function (a, b) { return a - b; });
    if (v.length < 3) return { media: null, usados: v.length, descartados: [] };
    var usados = v.slice(1, -1), media = usados.reduce(function (s, x) { return s + x; }, 0) / usados.length;
    var t = TERCOS.filter(function (x) { return x.v === N.terco; })[0] || TERCOS[1];
    return { media: media, usados: usados.length, descartados: [v[0], v[v.length - 1]], sugerida: media * t.f, terco: t };
  }

  function calcular(S) {
    var N = normalizar(S), v = validar(S);
    var r = calcularBase(N); r.N = N; r.bloqueios = v.erros; r.avisos = v.avisos;
    r.mercado = mercado(N);
    r.diaria = {}; FAIXAS.forEach(function (f) { r.diaria[f.id] = N.referencia * N.fatores[f.id]; });
    // Calendário de doze meses
    var J = N.informado.ano && N.ano >= 2024 ? janela(N.ano, N.mesInicio) : [];
    r.meses = []; r.noitesFaixa = { vale: 0, baixa: 0, base: 0, alta: 0, pico: 0 }; var somaR = 0, somaN = 0;
    J.forEach(function (a, i) {
      var nm = noitesDoMes(a.ano, a.mes), m = N.meses[i];
      var ps = N.picos.filter(function (p) { return p.mes === a.mes; }), pn = ps.reduce(function (s, p) { return s + p.noites; }, 0);
      pn = Math.min(pn, nm.dias);
      var semR = Math.max(0, nm.sem - pn), fdsR = Math.max(0, nm.fds - Math.max(0, pn - nm.sem));
      var dS = m.sem ? r.diaria[m.sem] : null, dF = m.fds ? r.diaria[m.fds] : null;
      var rp = ps.reduce(function (s, p) { return s + p.noites * N.referencia * (p.fator || 0); }, 0);
      var rec = (dS == null || dF == null) ? null : semR * dS + fdsR * dF + rp;
      if (m.sem) r.noitesFaixa[m.sem] += semR; if (m.fds) r.noitesFaixa[m.fds] += fdsR; r.noitesFaixa.pico += pn;
      if (rec != null) { somaR += rec; somaN += nm.dias; }
      r.meses.push({ ano: a.ano, mes: a.mes, nome: MESES[a.mes - 1], curto: MESES_C[a.mes - 1], dias: nm.dias, fds: nm.fds, sem: nm.sem, picoNoites: pn, semR: semR, fdsR: fdsR,
        faixaSem: m.sem, faixaFds: m.fds, diariaSem: dS, diariaFds: dF, media: rec == null ? null : rec / nm.dias, picos: ps.map(function (p) { return p.nome; }) });
    });
    r.totalNoites = J.reduce(function (s, a) { return s + noitesDoMes(a.ano, a.mes).dias; }, 0);
    r.calendarioCompleto = r.meses.length === 12 && r.meses.every(function (m) { return m.media != null; });
    r.mediaAno = r.calendarioCompleto ? somaR / somaN : null;
    r.picos = N.picos.map(function (p) { return { nome: p.nome, mes: p.mes, noites: p.noites, fator: p.fator, minimo: p.minimo, diaria: p.fator == null ? null : N.referencia * p.fator }; });
    // Faixas usadas no calendário abaixo do piso
    var usadas = {}; N.meses.forEach(function (m) { if (m.sem) usadas[m.sem] = 1; if (m.fds) usadas[m.fds] = 1; });
    r.faixasUsadas = FAIXAS_MES.filter(function (k) { return usadas[k]; });
    r.abaixoDoPiso = [];
    if (N.pisoDeclarado > 0) {
      r.faixasUsadas.forEach(function (k) { if (r.diaria[k] < N.pisoDeclarado - 0.005) r.abaixoDoPiso.push(FAIXA[k].r + " (" + brl(r.diaria[k]) + ")"); });
      r.picos.forEach(function (p) { if (p.diaria != null && p.diaria < N.pisoDeclarado - 0.005) r.abaixoDoPiso.push(p.nome + " (" + brl(p.diaria) + ")"); });
    }
    var ds = r.meses.map(function (m) { return m.faixaSem + "/" + m.faixaFds; });
    r.precoFixo = r.meses.length === 12 && ds.every(function (x) { return x === ds[0]; }) && r.meses[0].faixaSem === r.meses[0].faixaFds && !N.picos.length;
    r.semDiferencaFds = r.meses.length === 12 && r.meses.every(function (m) { return m.faixaSem === m.faixaFds; });
    var usadosDia = r.faixasUsadas.map(function (k) { return r.diaria[k]; }).concat(r.picos.map(function (p) { return p.diaria || 0; })).filter(function (x) { return x > 0; });
    r.amplitude = usadosDia.length ? Math.max.apply(null, usadosDia) / Math.min.apply(null, usadosDia) : null;
    r.picosSemRegra = N.picos.filter(function (p) { return p.minimo < 2; }).map(function (p) { return p.nome; });
    // Meta de venda direta
    r.metaDireta = N.metaDireta; r.deltaDireta = N.metaDireta - r.diretaAtual;
    r.comissaoQueFica = N.receitaMes > 0 && r.deltaDireta > 0 ? N.receitaMes * r.deltaDireta / 100 * r.comissaoMediaPagos / 100 : null;
    r.diferencaMedia = r.mediaAno != null && N.diariaAtual > 0 ? r.mediaAno - N.diariaAtual : null;
    return r;
  }

  // Leituras (só regras das fontes)
  function leituras(r) {
    var N = r.N, L = {};
    if (r.pisoCusto == null) L.custo = { k: "na", t: "Sem custo por noite, não dá para ler a referência." };
    else if (N.referencia < r.pisoCusto - 0.005) L.custo = { k: "estrutura", t: "A diária de referência (" + brl(N.referencia) + ") não cobre o custo da noite no canal mais caro (" + brl(r.pisoCusto) + "). Pela fonte, quando a referência não cobre o custo com margem, o problema não é preço: é estrutura de custo." };
    else L.custo = { k: "cobre", t: "A diária de referência (" + brl(N.referencia) + ") cobre o custo da noite no canal mais caro (" + brl(r.pisoCusto) + ") e sobra " + brl(N.referencia - r.pisoCusto) + " antes da margem." };
    if (!N.pisoDeclarado) L.piso = { k: "na", t: "Sem piso escrito ainda." };
    else if (r.pisoCusto != null && N.pisoDeclarado < r.pisoCusto - 0.005) L.piso = { k: "abaixo", t: "O piso de " + brl(N.pisoDeclarado) + " fica abaixo do custo da noite no canal mais caro (" + brl(r.pisoCusto) + "): vendida no piso, a noite não paga tudo." };
    else if (r.pisoCalculado != null && N.pisoDeclarado < r.pisoCalculado - 0.005) L.piso = { k: "sem-margem", t: "O piso de " + brl(N.pisoDeclarado) + " cobre o custo (" + brl(r.pisoCusto) + "), mas fica abaixo do piso com a sua margem mínima (" + brl(r.pisoCalculado) + ")." };
    else L.piso = { k: "ok", t: "O piso de " + brl(N.pisoDeclarado) + " cobre o custo da noite no canal mais caro (" + brl(r.pisoCusto) + ") com a sua margem mínima de " + dec(N.margemMinima, 1) + "%. Abaixo dele, não se vende, nem na véspera." };
    L.desconto = r.limiteVariavel == null ? { k: "na", t: "" } : { k: "faixas", t: "Antes de qualquer desconto, no canal mais caro: acima de " + brl(r.pisoCusto) + " a noite paga tudo; entre " + brl(r.limiteVariavel) + " e " + brl(r.pisoCusto) + " ela só paga o variável e ajuda no fixo; abaixo de " + brl(r.limiteVariavel) + " ela consome valor." + (N.pisoDeclarado > 0 ? (N.pisoDeclarado >= r.pisoCusto - 0.005 ? " O seu piso está na primeira faixa: nenhum desconto passa dele." : " O seu piso ainda está abaixo da primeira faixa.") : "") };
    if (!r.calendarioCompleto) L.calendario = { k: "na", t: "Calendário ainda incompleto." };
    else if (r.precoFixo) L.calendario = { k: "fixo", t: "Preço fixo o ano inteiro: o mesmo valor de janeiro a dezembro erra nas duas direções, baixo nas datas de demanda e alto nos meses vazios." };
    else L.calendario = { k: "faixas", t: "Diária média do calendário, ponderada pelas noites do ano: " + brl(r.mediaAno) + (r.diferencaMedia != null ? " (a diária média que você pratica hoje é " + brl(N.diariaAtual) + ")" : "") + ". É a média das diárias-alvo, não uma previsão de receita." };
    L.fds = r.semDiferencaFds ? { k: "igual", t: "Meio de semana e fim de semana com a mesma faixa em todos os meses. Em destino de escapada curta, o fim de semana costuma valer de 25% a 60% mais: confira no levantamento." } : { k: "dif", t: "Fim de semana com faixa própria em " + r.meses.filter(function (m) { return m.faixaSem !== m.faixaFds; }).length + " dos 12 meses." };
    L.canais = !r.melhorCanal ? { k: "na", t: "Sem referência ou sem canais, não há líquido por canal." } : { k: "canais", t: "Na diária de referência, o canal que mais deixa por noite é " + r.melhorCanal.nome + " (" + brl(r.melhorCanal.margemNoite) + " depois do custo variável) e o que menos deixa é " + r.piorCanal.nome + " (" + brl(r.piorCanal.margemNoite) + "). Comissão média ponderada do seu mix: " + pct(r.comissaoMedia / 100) + "." };
    if (r.deltaDireta > 0) L.direta = { k: "meta", t: "Venda direta hoje: " + dec(r.diretaAtual, 1) + "% da receita; meta: " + dec(N.metaDireta, 1) + "% até " + dataBR(N.prazoMeta) + "." + (r.comissaoQueFica != null ? " Com a mesma receita de " + brl(N.receitaMes) + " num mês, essa mudança deixaria de pagar cerca de " + brl(r.comissaoQueFica) + " de comissão. É uma conta com os seus números, não uma previsão." : "") };
    else L.direta = { k: "sem-meta", t: "A meta de venda direta (" + dec(N.metaDireta, 1) + "%) não passa do que você já vende direto (" + dec(r.diretaAtual, 1) + "%). Uma meta precisa de um número acima do atual e de um prazo." };
    return L;
  }

  // Causa principal e prioridades, na ordem: custo → piso → calendário → canais → piso conhecido
  var REGRAS = [
    { id: "estrutura", r: "Referência abaixo do custo da noite", acao: "Voltar à Folha Única do Mês (Módulo 2) e rever o custo antes de mexer no preço: pela fonte, quando a referência não cobre o custo, o problema é estrutura de custo.", verifica: "A diária de referência fica acima do custo da noite no canal mais caro.", dispara: function (r) { return r.pisoCusto != null && r.N.referencia > 0 && r.N.referencia < r.pisoCusto - 0.005; } },
    { id: "piso", r: "Piso abaixo do custo da noite", acao: "Subir o piso para pelo menos o custo da noite no canal mais caro, mais a sua margem mínima, e reescrever a folha do piso.", verifica: "O piso escrito é igual ou maior que o piso calculado na ficha.", dispara: function (r) { return r.pisoCusto != null && r.N.pisoDeclarado > 0 && r.N.pisoDeclarado < r.pisoCusto - 0.005; } },
    { id: "faixa", r: "Faixa do calendário abaixo do piso", acao: "Subir o fator da faixa (ou da data) que ficou abaixo do piso, ou rever o piso. Nenhuma diária do calendário fica abaixo dele.", verifica: "Todas as faixas usadas e todas as datas de pico ficam no piso ou acima.", dispara: function (r) { return r.abaixoDoPiso.length > 0; } },
    { id: "fixo", r: "Preço fixo o ano inteiro", acao: "Ler o calendário de seis a nove concorrentes por doze meses e distribuir as cinco faixas pelos meses.", verifica: "O calendário tem pelo menos duas faixas e as datas de pico em linha própria.", dispara: function (r) { return r.precoFixo; } },
    { id: "pico", r: "Datas de pico sem regra", acao: "Mapear réveillon, carnaval, feriados prolongados e eventos locais, com preço próprio, mínimo de noites e data de abertura, e bloquear as datas até terem preço.", verifica: "Cada data de pico tem preço, mínimo de noites (2 ou mais) e está bloqueada até a abertura.", dispara: function (r) { return r.calendarioCompleto && (r.N.picos.length === 0 || r.picosSemRegra.length > 0); } },
    { id: "dependencia", r: "Sem venda direta", acao: "Abrir um canal de venda direta (site ou WhatsApp com pagamento) e registrar quanto entra por ele a cada mês.", verifica: "O mix do trimestre seguinte tem venda direta acima de zero.", dispara: function (r) { return r.canais.length > 0 && r.diretaAtual === 0; } },
    { id: "overbooking", r: "Vários canais sem gestor de canais", acao: "Ligar os calendários com um gestor de canais antes de abrir em mais plataformas.", verifica: "Uma reserva em qualquer canal fecha a data em todos os outros, sem ação manual.", dispara: function (r) { return r.canaisPagosAtivos >= 2 && !r.N.gestorCanais; } },
    { id: "motor", r: "Venda direta sem motor de reservas", acao: "Instalar um motor de reservas no site (ou um link de reserva com pagamento) ligado ao calendário.", verifica: "Um hóspede consegue reservar e pagar direto sem você responder à mão.", dispara: function (r) { return r.diretaAtual > 0 && !r.N.motorReservas; } },
    { id: "cabeca", r: "Piso só na sua cabeça", acao: "Imprimir a folha do piso e combinar com todo mundo que atende, inclusive para a véspera.", verifica: "Quem atende sabe dizer o piso sem consultar você.", dispara: function (r) { return r.N.pisoDeclarado > 0 && !r.N.quemConhece; } },
  ];
  var DENTRO = { id: "ok", r: "Tabela dentro das regras da fonte", acao: "Marcar as quatro revisões trimestrais, de três a quatro semanas antes de cada trimestre, e manter doze meses de calendário abertos.", verifica: "As quatro revisões estão no calendário e a próxima já tem data." };

  function prioridades(r) {
    var lista = [];
    REGRAS.forEach(function (g) { if (lista.length < 3 && g.dispara(r)) lista.push({ id: g.id, r: g.r, acao: g.acao, verifica: g.verifica }); });
    return lista.length ? lista : [Object.assign({}, DENTRO)];
  }
  function planoSugerido(P) { return P.map(function (p, i) { return (P.length > 1 ? (i + 1) + ". " : "") + p.acao; }).join("\n"); }
  function comoVerificar(P) { return P.map(function (p) { return p.verifica; }).join(" "); }

  // Tabela completa (dá para mostrar o resultado) e lição concluída (selo)
  function completo(S) {
    S = S || {}; if (!S.situacao) return false;
    var v = validar(S); if (!v.ok) return false;
    var r = calcular(S), N = r.N;
    if (!(N.referencia > 0 && N.pisoDeclarado > 0)) return false;
    if (!r.calendarioCompleto) return false;
    if (!(N.canais.length && N.canais.every(function (c) { return c.mixInf; }))) return false;
    if (!(N.metaDireta > r.diretaAtual && N.prazoMeta)) return false;
    return true;
  }
  function concluido(S) { return completo(S) && !!(S.acao && String(S.acao).trim().length >= 10) && !!S.prazo && !!S.pdf; }
  function pendencias(S) {
    var p = [];
    if (!completo(S)) p.push("a Tabela preenchida (piso, referência, doze meses, mix de canais e meta de venda direta acima da atual, com prazo)");
    if (!(S && S.acao && String(S.acao).trim().length >= 10)) p.push("uma ação com pelo menos 10 letras");
    if (!(S && S.prazo)) p.push("um prazo");
    if (!(S && S.pdf)) p.push("o PDF baixado");
    return p;
  }

  function brl(v) { if (v == null || !isFinite(v)) return "—"; var neg = v < 0; var s = Math.abs(v).toFixed(2).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, "."); return (neg ? "−R$ " : "R$ ") + s; }
  function pct(v, d) { if (v == null || !isFinite(v)) return "—"; return (v * 100).toFixed(d == null ? 1 : d).replace(".", ",") + "%"; }
  function dec(v, d) { if (v == null || !isFinite(v)) return "—"; return v.toFixed(d == null ? 1 : d).replace(".", ","); }
  function dataBR(s) { return s ? String(s).split("-").reverse().join("/") : "—"; }

  var TELAS = ["abertura", "custo", "canais", "referencia", "piso", "calendario", "picos", "resultado"];
  var TITULOS = { custo: "O custo da noite", canais: "Os seus canais", referencia: "A diária de referência", piso: "O piso e as condições", calendario: "As cinco faixas e os doze meses", picos: "Datas de pico e meta de venda direta" };
  var PROXIMO = { n: 4, t: "Marketing e vendas" };

  var api = { FAIXAS: FAIXAS, FAIXA: FAIXA, FAIXAS_MES: FAIXAS_MES, TERCOS: TERCOS, MESES: MESES, MESES_C: MESES_C, SITUACOES: SITUACOES, DIAG: DIAG, SIMNAO: SIMNAO, NIVEIS: NIVEIS,
    CAMPOS: CAMPOS, CAMPO: CAMPO, EXEMPLO: EXEMPLO, REGRAS: REGRAS, DENTRO: DENTRO, TELAS: TELAS, TITULOS: TITULOS, PROXIMO: PROXIMO,
    num: num, r2: r2, noitesDoMes: noitesDoMes, janela: janela, normalizar: normalizar, validar: validar, calcular: calcular, mercado: mercado, leituras: leituras,
    prioridades: prioridades, planoSugerido: planoSugerido, comoVerificar: comoVerificar, completo: completo, concluido: concluido, pendencias: pendencias, nivel: nivel,
    brl: brl, pct: pct, dec: dec, dataBR: dataBR };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else raiz.ZP = api;
})(typeof window !== "undefined" ? window : this);

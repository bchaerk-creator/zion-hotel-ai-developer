/* Jornada 2 · Gestão · Módulo 6 · Compras, estoque e manutenção
   Lógica pura da ficha "A minha Matriz de Compras e Manutenção". Sem DOM: roda no navegador (window.ZC) e no Node (testes).
   Regra: tudo que a ficha afirma sai daqui, para ser testado. Nenhuma nota: só as regras das fontes.
   Fontes: Panorama · Trilha B · G5 Compras e Fornecedores (lista por valor, três cotações, contrato nos recorrentes,
   consumo por hóspede, três jogos por cama); Jornada do COMO · Etapa 09 (consumo em três meses ÷ diárias vendidas,
   reserva de manutenção de 3% a 6% da receita) e Etapa 10 (compras semanal, manutenção preventiva com o calendário do ano,
   alçada de compra fora do previsto); Bíblia Operacional Zion (contagem do estoque toda segunda-feira, acionar o fornecedor
   no mínimo, ronda técnica diária, revisar fornecedores e custos todo mês, obra em baixa ocupação).
   Ponto de pedido e estoque mínimo: definição-padrão de gestão de estoque (a fonte não define), declarada como tal. */
(function (raiz) {
  "use strict";

  var MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
  var MESES_C = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
  var FREQS = [
    { v: "mensal", r: "Mensal", passo: 1 }, { v: "bimestral", r: "Bimestral", passo: 2 }, { v: "trimestral", r: "Trimestral", passo: 3 },
    { v: "semestral", r: "Semestral", passo: 6 }, { v: "anual", r: "Anual", passo: 12 },
  ];
  var FREQ = {}; FREQS.forEach(function (f) { FREQ[f.v] = f; });
  var TIPOS = [{ v: "variavel", r: "Custo variável da hospedagem" }, { v: "outras", r: "Vendido à parte (café, cestas, frigobar)" }];
  var CONTRATOS = [{ v: "sim", r: "Tem contrato" }, { v: "fechar", r: "Vou fechar contrato" }, { v: "nao", r: "Sem contrato" }];
  var DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"];
  var JOGOS_POR_CAMA = 3; // Panorama · G5 · "Na prática"
  var DIAS_MES = 30;      // convenção: consumo diário = uso do mês ÷ 30

  var SITUACOES = [
    { v: "abrir", r: "Ainda vou abrir a minha hospedagem (vou preencher com o consumo previsto)", curto: "vai abrir" },
    { v: "dono", r: "Já opero a minha hospedagem e quero organizar compras, estoque e manutenção", curto: "dono que opera" },
    { v: "operador", r: "Cuido da hospedagem de outra pessoa e preciso propor a Matriz ao dono", curto: "operador" },
  ];
  var DIAG = [
    { id: "lista", r: "Você sabe quais são os cinco itens que mais pesam nas suas compras, por valor?" },
    { id: "cotacao", r: "Você pede três cotações antes de comprar o que compra todo mês?" },
    { id: "minimo", r: "Cada item do estoque tem um mínimo escrito, que dispara o pedido?" },
    { id: "calendario", r: "Existe um calendário de manutenção preventiva para os próximos doze meses?" },
  ];
  var SIMNAO = [{ v: "sim", r: "Sim" }, { v: "nao", r: "Não" }];
  var NIVEIS = [
    { n: 1, r: "Compra no susto", t: "Hoje se compra quando acaba e se conserta quando quebra. A Matriz é o primeiro corte." },
    { n: 2, r: "Começando a organizar", t: "Uma parte existe, mas faltam números para decidir. A Matriz mostra o que pesa, o que cotar e quando pedir." },
    { n: 3, r: "Quase organizado", t: "Falta pouco: uma regra ou um número. A Matriz mostra qual e onde ele entra." },
    { n: 4, r: "Compras com método", t: "Lista, cotações, mínimos e calendário existem. A Matriz serve para revisar todo mês." },
  ];
  function nivel(S) {
    var d = (S && S.diag) || {}, sim = 0;
    DIAG.forEach(function (q) { if (d[q.id] === "sim") sim++; });
    return NIVEIS[Math.max(0, sim - 1)];
  }

  // Campos simples (itens, estoque e tarefas são listas à parte)
  var CAMPOS = [
    { id: "mesesPeriodo", tela: "consumo", tipo: "int", min: 1, max: 12, obrig: true, r: "Meses do levantamento", pq: "A fonte manda somar o gasto de cada item em três meses: um mês só engana.", onde: "Os três últimos meses com notas e extratos.", ex: "3" },
    { id: "noitesPeriodo", tela: "consumo", tipo: "int", min: 1, obrig: true, r: "Noites vendidas no período", pq: "O consumo por noite é o gasto dividido pelas noites vendidas no mesmo período.", onde: "Na Folha Única de cada mês (Módulo 2) ou no calendário dos canais.", ex: "174" },
    { id: "hospedesPeriodo", tela: "consumo", tipo: "int", r: "Hóspedes no período", pq: "Amenidades e café se gastam por pessoa: o consumo por hóspede mostra isso.", onde: "Soma das pessoas de cada reserva do período.", ex: "150" },
    { id: "unidades", tela: "consumo", tipo: "int", min: 1, obrig: true, r: "Unidades à venda", pq: "Para mostrar quanto os itens custam num mês com todas as noites vendidas.", onde: "Quantas casas, cabanas ou quartos você vende.", ex: "4" },
    { id: "custoVariavelNoite", tela: "consumo", tipo: "brl", r: "Custo variável por noite da sua Folha", pq: "Para conferir quanto do custo variável a Matriz explica.", onde: "Na sua Folha Única do Mês (Módulo 2), linha \"custo variável por noite\".", ex: "28,32" },
    { id: "prazoContratos", tela: "matriz", tipo: "data", r: "Até quando fechar os contratos marcados", pq: "Contrato sem data vira intenção.", onde: "Uma data realista, de um a três meses.", ex: "31/03/2027" },
    { id: "camas", tela: "estoque", tipo: "int", r: "Camas (de todas as unidades)", pq: "O enxoval se dimensiona por cama.", onde: "Conte as camas de casal e de solteiro.", ex: "4" },
    { id: "jogos", tela: "estoque", tipo: "int", r: "Jogos de cama completos em uso", pq: "A fonte recomenda três jogos por cama: um na cama, um lavando, um descansando.", onde: "Conte os jogos completos, sem os furados ou manchados.", ex: "10" },
    { id: "ano", tela: "manutencao", tipo: "int", min: 2024, max: 2099, obrig: true, r: "Ano em que o calendário começa", pq: "Para montar os doze meses.", onde: "O próximo ano de operação.", ex: "2027" },
    { id: "receitaReserva", tela: "manutencao", tipo: "brl", obrig: true, r: "Receita real de um mês comum (R$)", pq: "A reserva de manutenção sai da receita, todo mês.", onde: "Na Folha Única do Mês (Módulo 2): receita real (depois de comissão, taxas e imposto).", ex: "13.565,60" },
    { id: "reservaPct", tela: "manutencao", tipo: "pct", obrig: true, r: "Reserva de manutenção e reposição (% da receita)", pq: "Pintura, telhado, equipamento: a fonte manda separar de 3% a 6% da receita por mês.", onde: "Uma decisão sua dentro da faixa da fonte. No exemplo didático, 3%.", ex: "3" },
    { id: "quemCompra", tela: "rotina", tipo: "texto", r: "Quem faz as compras", pq: "Compra sem dono vira compra no susto.", onde: "Uma pessoa, com nome.", ex: "Ana (dona)" },
    { id: "alcada", tela: "rotina", tipo: "brl", r: "Até quanto a equipe compra fora do previsto sem perguntar (R$)", pq: "Um limite escrito evita esperar você para comprar uma lâmpada, e evita a compra grande sem conversa.", onde: "Uma decisão sua. Na fonte, o exemplo é R$ 300.", ex: "300,00" },
  ];
  var CAMPO = {}; CAMPOS.forEach(function (c) { CAMPO[c.id] = c; });

  // Exemplo didático · dados fictícios (Cabanas do Vale, a mesma dos módulos 0, 2 e 3)
  var EXEMPLO = {
    situacao: "dono", hospedagem: "Cabanas do Vale (exemplo)", diag: { lista: "nao", cotacao: "nao", minimo: "sim", calendario: "nao" },
    mesesPeriodo: 3, noitesPeriodo: 174, hospedesPeriodo: 150, unidades: 4, custoVariavelNoite: 28.32,
    itens: [
      { nome: "Café da manhã e cestas (insumos)", unidade: "cesta montada", gasto: 1260, tipo: "outras", precoAtual: 28, cot: [28, 25.5, 26.9], contrato: "fechar" },
      { nome: "Lavanderia do enxoval", unidade: "kg lavado", gasto: 900, tipo: "variavel", precoAtual: 3, cot: [3, 2.6, 3.2], contrato: "sim" },
      { nome: "Amenidades (sabonete, xampu, papel, água)", unidade: "kit por estadia", gasto: 780, tipo: "variavel", precoAtual: 10.4, cot: [10.4, 8.9, 9.8], contrato: "fechar" },
      { nome: "Gás do aquecimento da água", unidade: "botijão de 13 kg", gasto: 720, tipo: "variavel", precoAtual: 120, cot: [120, 112, 118], contrato: "nao" },
      { nome: "Reposição de enxoval", unidade: "jogo de cama de casal", gasto: 240, tipo: "variavel", precoAtual: 120, cot: [120, 98, 135], contrato: "fechar" },
    ],
    prazoContratos: "2027-03-31",
    estoque: [
      { nome: "Kit de amenidades", unidade: "kit", usoMes: 25, entrega: 7, seguranca: 7, atual: 14, ciclo: 30 },
      { nome: "Papel higiênico", unidade: "rolo", usoMes: 100, entrega: 5, seguranca: 7, atual: 30, ciclo: 30 },
      { nome: "Botijão de gás de 13 kg", unidade: "botijão", usoMes: 2, entrega: 2, seguranca: 7, atual: 2, ciclo: 15 },
      { nome: "Café em pó (pacote de 500 g)", unidade: "pacote", usoMes: 8, entrega: 3, seguranca: 7, atual: 6, ciclo: 15 },
    ],
    camas: 4, jogos: 10,
    ano: 2027, mesInicio: 1, receitaReserva: 13565.6, reservaPct: 3, casaCheia: [6, 7, 8, 12],
    tarefas: [
      { nome: "Limpar os filtros do ar-condicionado", freq: "trimestral", inicio: 1, custo: 0, quem: "Equipe" },
      { nome: "Controle de pragas", freq: "trimestral", inicio: 2, custo: 180, quem: "Empresa contratada" },
      { nome: "Revisão do aquecedor a gás", freq: "anual", inicio: 3, custo: 280, quem: "Técnico de aquecimento" },
      { nome: "Revisão elétrica (quadro e tomadas)", freq: "anual", inicio: 4, custo: 350, quem: "Eletricista" },
      { nome: "Limpeza das calhas", freq: "semestral", inicio: 4, custo: 150, quem: "Equipe" },
      { nome: "Limpeza da caixa d'água", freq: "semestral", inicio: 5, custo: 250, quem: "Empresa contratada" },
      { nome: "Revisão do ar-condicionado por técnico", freq: "anual", inicio: 9, custo: 480, quem: "Técnico de ar-condicionado" },
      { nome: "Inspeção e recarga dos extintores", freq: "anual", inicio: 10, custo: 160, quem: "Empresa credenciada" },
      { nome: "Tratamento do deck (óleo e vedação)", freq: "anual", inicio: 11, custo: 900, quem: "Marceneiro" },
    ],
    ronda: true, ocorrencias: true, diaContagem: "segunda-feira", quemCompra: "Ana (dona)", alcada: 300,
  };

  // "1.234,56", "1234.56", "13.000" (treze mil), 1234 → número; vazio ou inválido → null
  function num(v) {
    if (v == null) return null;
    if (typeof v === "number") return isFinite(v) ? v : null;
    var s = String(v).trim(); if (!s) return null;
    s = s.replace(/\s|R\$|%/g, "").replace(/−/g, "-");
    if (/,/.test(s)) s = s.replace(/\./g, "").replace(",", ".");
    else if (/^-?\d{1,3}(\.\d{3})+$/.test(s)) s = s.replace(/\./g, "");
    if (!/^-?\d*\.?\d+$/.test(s)) return null;
    var n = Number(s); return isFinite(n) ? n : null;
  }
  function informado(v) { return v != null && String(v).trim() !== ""; }
  function r2(v) { return Math.round(v * 100) / 100; }
  function teto(x) { return Math.ceil(x - 1e-9); }
  function div(a, b) { return b > 0 ? a / b : null; }

  function janela(ano, mesInicio) {
    var a = []; for (var i = 0; i < 12; i++) { var m = mesInicio - 1 + i; a.push({ ano: ano + Math.floor(m / 12), mes: (m % 12) + 1 }); } return a;
  }
  // A tarefa cai neste mês do ano? (mês de início da tarefa e passo da frequência, contados dentro do ano)
  function cai(t, mes) { var f = FREQ[t.freq]; if (!f || !(t.inicio >= 1 && t.inicio <= 12)) return false; return (((mes - t.inicio) % 12 + 12) % 12) % f.passo === 0; }

  function normalizar(S) {
    S = S || {}; var N = { informado: {} };
    CAMPOS.forEach(function (c) {
      var v = S[c.id]; N.informado[c.id] = informado(v);
      if (c.tipo === "texto" || c.tipo === "data") N[c.id] = v == null ? "" : String(v).trim();
      else { var n = num(v); N[c.id] = n == null ? 0 : n; }
    });
    N.mesInicio = Math.min(12, Math.max(1, Math.floor(num(S.mesInicio) || 1)));
    N.itens = (S.itens || []).map(function (it) {
      it = it || {};
      var cotB = (it.cot || []).slice(0, 3);
      return { nome: String(it.nome == null ? "" : it.nome).trim(), unidade: String(it.unidade == null ? "" : it.unidade).trim(), gasto: num(it.gasto), tipo: it.tipo === "outras" ? "outras" : (it.tipo === "variavel" ? "variavel" : ""),
        precoAtual: num(it.precoAtual), cot: cotB.map(num).filter(function (x) { return x != null && x > 0; }), contrato: it.contrato || "",
        informado: informado(it.nome) || informado(it.gasto), bruto: it };
    }).filter(function (it) { return it.informado; });
    N.estoque = (S.estoque || []).map(function (e) {
      e = e || {};
      return { nome: String(e.nome == null ? "" : e.nome).trim(), unidade: String(e.unidade == null ? "" : e.unidade).trim(), usoMes: num(e.usoMes), entrega: num(e.entrega), seguranca: num(e.seguranca), atual: num(e.atual), ciclo: num(e.ciclo),
        informado: informado(e.nome) || informado(e.usoMes), bruto: e };
    }).filter(function (e) { return e.informado; });
    N.tarefas = (S.tarefas || []).map(function (t) {
      t = t || {};
      return { nome: String(t.nome == null ? "" : t.nome).trim(), freq: FREQ[t.freq] ? t.freq : "", inicio: Math.floor(num(t.inicio) || 0), custo: num(t.custo), quem: String(t.quem == null ? "" : t.quem).trim(),
        informado: informado(t.nome) || informado(t.custo), bruto: t };
    }).filter(function (t) { return t.informado; });
    N.casaCheia = (S.casaCheia || []).map(function (m) { return Math.floor(num(m) || 0); }).filter(function (m) { return m >= 1 && m <= 12; });
    N.ronda = !!S.ronda; N.ocorrencias = !!S.ocorrencias; N.diaContagem = DIAS.indexOf(S.diaContagem) >= 0 ? S.diaContagem : "";
    N.vaiAbrir = S.situacao === "abrir";
    return N;
  }

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
    if (!tela || tela === "consumo") {
      if (N.informado.mesesPeriodo && N.mesesPeriodo > 0 && N.mesesPeriodo < 3) avisos.push("A fonte pede três meses de notas: com menos, um mês atípico distorce o consumo.");
      if (!N.informado.custoVariavelNoite) avisos.push("Sem o custo variável por noite da Folha (Módulo 2), a ficha não confere quanto do custo a Matriz explica.");
      if (N.informado.hospedesPeriodo && N.informado.noitesPeriodo && N.hospedesPeriodo > 0 && N.unidades > 0 && N.hospedesPeriodo > N.noitesPeriodo * 20) avisos.push("Hóspedes muito acima das noites vendidas: confira se não somou noites por pessoa.");
    }
    if (!tela || tela === "matriz") {
      if (!N.itens.length) erros.push("Informe pelo menos um item que você compra.");
      N.itens.forEach(function (it, i) {
        var nm = it.nome || "Item " + (i + 1);
        if (!it.nome) erros.push("Item " + (i + 1) + ": falta o nome.");
        if (!(it.gasto > 0)) erros.push(nm + ": falta o gasto no período.");
        if (!it.tipo) erros.push(nm + ": escolha se é custo variável ou vendido à parte.");
        ["gasto", "precoAtual"].forEach(function (k) { var b = it.bruto[k]; if (informado(b) && num(b) == null) erros.push(nm + ": escreva só números."); });
        (it.bruto.cot || []).forEach(function (b) { if (informado(b) && (num(b) == null || num(b) < 0)) erros.push(nm + ": cotação inválida."); });
        if ((it.gasto != null && it.gasto < 0) || (it.precoAtual != null && it.precoAtual < 0)) erros.push(nm + ": nenhum valor pode ser negativo.");
        if (it.cot.length && !(it.precoAtual > 0)) erros.push(nm + ": informe o preço que você paga hoje, para comparar com as cotações.");
        if (it.cot.length > 0 && it.cot.length < 3) avisos.push(nm + ": " + it.cot.length + " de 3 cotações.");
      });
      if (N.itens.length > 0 && N.itens.length < 5) avisos.push("A fonte pede os cinco itens que mais pesam, por valor. Você listou " + N.itens.length + ".");
      if (N.itens.some(function (it) { return it.contrato === "fechar"; }) && !N.prazoContratos) erros.push("Marque até quando vai fechar os contratos.");
    }
    if (!tela || tela === "estoque") {
      if (!N.estoque.length) erros.push("Informe pelo menos um item do estoque.");
      N.estoque.forEach(function (e, i) {
        var nm = e.nome || "Estoque " + (i + 1);
        if (!e.nome) erros.push("Estoque " + (i + 1) + ": falta o nome.");
        ["usoMes", "entrega", "seguranca", "atual", "ciclo"].forEach(function (k) { var b = e.bruto[k]; if (informado(b) && num(b) == null) erros.push(nm + ": escreva só números."); });
        if (!(e.usoMes > 0)) erros.push(nm + ": falta o uso por mês.");
        if (e.entrega == null) erros.push(nm + ": falta o prazo de entrega (dias).");
        if (e.seguranca == null) erros.push(nm + ": faltam os dias de segurança.");
        if (e.atual == null) erros.push(nm + ": falta o estoque de hoje.");
        if (!(e.ciclo > 0)) erros.push(nm + ": falta de quanto em quanto tempo você compra (dias).");
        if ([e.usoMes, e.entrega, e.seguranca, e.atual, e.ciclo].some(function (x) { return x != null && x < 0; })) erros.push(nm + ": nenhum valor pode ser negativo.");
      });
      if (N.camas > 0 && !N.informado.jogos) erros.push("Informe quantos jogos de cama você tem.");
    }
    if (!tela || tela === "manutencao") {
      if (N.informado.reservaPct && (N.reservaPct < 3 || N.reservaPct > 6)) avisos.push("A fonte indica separar de 3% a 6% da receita por mês para manutenção e reposição.");
      if (!N.tarefas.length) erros.push("Informe pelo menos uma tarefa de manutenção preventiva.");
      N.tarefas.forEach(function (t, i) {
        var nm = t.nome || "Tarefa " + (i + 1);
        if (!t.nome) erros.push("Tarefa " + (i + 1) + ": falta o nome.");
        if (!t.freq) erros.push(nm + ": escolha a frequência.");
        if (!(t.inicio >= 1 && t.inicio <= 12)) erros.push(nm + ": escolha o primeiro mês.");
        var b = t.bruto.custo; if (informado(b) && num(b) == null) erros.push(nm + ": escreva só números no custo.");
        if (t.custo != null && t.custo < 0) erros.push(nm + ": o custo não pode ser negativo.");
      });
      if (N.tarefas.length && N.tarefas.length < 3) avisos.push("Um calendário do ano costuma ter mais de três tarefas: aquecimento, elétrica, caixa d'água, pragas, extintores, telhado e calhas.");
    }
    return { erros: erros, avisos: avisos, ok: erros.length === 0 };
  }

  function calcular(S) {
    var N = normalizar(S), v = validar(S), r = { N: N, bloqueios: v.erros, avisos: v.avisos };
    // Matriz de Compras
    var total = N.itens.reduce(function (s, it) { return s + (it.gasto > 0 ? it.gasto : 0); }, 0);
    r.totalPeriodo = total;
    r.itens = N.itens.map(function (it) {
      var g = it.gasto > 0 ? it.gasto : 0, menor = it.cot.length ? Math.min.apply(null, it.cot) : null;
      var qtd = it.precoAtual > 0 ? g / it.precoAtual : null;
      var dif = qtd != null && menor != null ? Math.max(0, qtd * (it.precoAtual - menor)) : null;
      return { nome: it.nome, unidade: it.unidade, gasto: g, tipo: it.tipo, precoAtual: it.precoAtual, cot: it.cot, contrato: it.contrato, menor: menor, quantidade: qtd, diferenca: dif,
        porNoite: div(g, N.noitesPeriodo), porHospede: div(g, N.hospedesPeriodo), porMes: div(g, N.mesesPeriodo), peso: div(g, total), tresCotacoes: it.cot.length >= 3 };
    }).sort(function (a, b) { return b.gasto - a.gasto; });
    r.itens.forEach(function (it, i) { it.posicao = i + 1; });
    var varG = r.itens.filter(function (it) { return it.tipo === "variavel"; }).reduce(function (s, it) { return s + it.gasto; }, 0);
    r.variavelPeriodo = varG;
    r.variavelNoite = div(varG, N.noitesPeriodo);
    r.cobertura = r.variavelNoite != null && N.custoVariavelNoite > 0 ? r.variavelNoite / N.custoVariavelNoite : null;
    r.restoNoite = r.variavelNoite != null && N.custoVariavelNoite > 0 ? N.custoVariavelNoite - r.variavelNoite : null;
    r.mesCheio = r.variavelNoite != null && N.unidades > 0 ? r.variavelNoite * N.unidades * DIAS_MES : null;
    r.diferencaPeriodo = r.itens.reduce(function (s, it) { return s + (it.diferenca || 0); }, 0);
    r.diferencaAno = N.mesesPeriodo > 0 ? r.diferencaPeriodo * 12 / N.mesesPeriodo : null;
    r.semTres = r.itens.filter(function (it) { return !it.tresCotacoes; }).map(function (it) { return it.nome; });
    r.semContrato = r.itens.filter(function (it) { return it.contrato === "nao"; }).map(function (it) { return it.nome; });
    r.aFechar = r.itens.filter(function (it) { return it.contrato === "fechar"; }).map(function (it) { return it.nome; });
    r.comTres = r.itens.filter(function (it) { return it.tresCotacoes && it.precoAtual > 0; }).length;
    r.cinco = r.itens.slice(0, 5); r.pesoCinco = div(r.cinco.reduce(function (s, it) { return s + it.gasto; }, 0), total);
    // Estoque mínimo e ponto de pedido
    r.estoque = N.estoque.map(function (e) {
      var dia = (e.usoMes || 0) / DIAS_MES, ent = e.entrega || 0, seg = e.seguranca || 0, at = e.atual || 0, cic = e.ciclo || 0;
      var ppB = dia * (ent + seg), pp = teto(ppB), minimo = teto(dia * seg), pedir = at <= pp && e.usoMes > 0;
      return { nome: e.nome, unidade: e.unidade, usoMes: e.usoMes, entrega: ent, seguranca: seg, atual: at, ciclo: cic, diario: dia, minimo: minimo, pontoPedido: pp,
        pedir: pedir, pedido: pedir ? Math.max(0, teto(ppB + dia * cic - at)) : 0, diasCobertos: dia > 0 ? at / dia : null };
    });
    r.pedirAgora = r.estoque.filter(function (e) { return e.pedir; });
    // Enxoval
    r.porCama = N.camas > 0 ? N.jogos / N.camas : null;
    r.jogosFaltam = N.camas > 0 ? Math.max(0, JOGOS_POR_CAMA * N.camas - N.jogos) : 0;
    // Calendário de manutenção
    var J = N.informado.ano && N.ano >= 2024 ? janela(N.ano, N.mesInicio) : [];
    r.reservaMes = N.receitaReserva * N.reservaPct / 100; r.reservaAno = r.reservaMes * 12;
    var acumR = 0, acumG = 0; r.meses = []; r.ocorrencias = 0; r.primeiroDescoberto = null; r.pesadaCasaCheia = [];
    J.forEach(function (a, i) {
      var ts = N.tarefas.filter(function (t) { return cai(t, a.mes); });
      var custo = ts.reduce(function (s, t) { return s + (t.custo || 0); }, 0);
      acumR += r.reservaMes; acumG += custo; r.ocorrencias += ts.length;
      var cheia = N.casaCheia.indexOf(a.mes) >= 0;
      ts.forEach(function (t) { if (cheia && (t.freq === "anual" || t.freq === "semestral")) r.pesadaCasaCheia.push(t.nome + " (" + MESES_C[a.mes - 1] + ")"); });
      if (r.primeiroDescoberto == null && acumG > acumR + 0.005) r.primeiroDescoberto = { ano: a.ano, mes: a.mes, nome: MESES[a.mes - 1], falta: acumG - acumR };
      r.meses.push({ ano: a.ano, mes: a.mes, nome: MESES[a.mes - 1], curto: MESES_C[a.mes - 1], tarefas: ts.map(function (t) { return t.nome; }), custo: custo, casaCheia: cheia, reservaAcumulada: acumR, gastoAcumulado: acumG });
    });
    r.totalAno = acumG;
    r.calendarioCompleto = r.meses.length === 12 && N.tarefas.length > 0;
    r.mesMaisPesado = null; r.meses.forEach(function (m) { if (m.custo > 0 && (!r.mesMaisPesado || m.custo > r.mesMaisPesado.custo)) r.mesMaisPesado = m; });
    r.sobraReserva = r.reservaAno - r.totalAno;
    r.tarefas = N.tarefas.map(function (t) {
      var n = r.meses.filter(function (m) { return cai(t, m.mes); }).length;
      return { nome: t.nome, freq: t.freq, freqR: FREQ[t.freq] ? FREQ[t.freq].r : "", inicio: t.inicio, custo: t.custo || 0, quem: t.quem, vezes: n, custoAno: n * (t.custo || 0),
        meses: r.meses.filter(function (m) { return cai(t, m.mes); }).map(function (m) { return m.curto; }) };
    });
    return r;
  }

  // Leituras (só regras das fontes)
  function leituras(r) {
    var N = r.N, L = {};
    if (!r.itens.length) L.peso = { k: "na", t: "Sem itens na Matriz ainda." };
    else L.peso = { k: "peso", t: "Os " + r.itens.length + " itens somam " + brl(r.totalPeriodo) + " em " + N.mesesPeriodo + (N.mesesPeriodo === 1 ? " mês" : " meses") + ". O que mais pesa é " + r.itens[0].nome + ", com " + pct(r.itens[0].peso) + " do total. Compra se organiza por valor, não por frequência." };
    if (r.variavelNoite == null) L.consumo = { k: "na", t: "Sem noites vendidas, não há consumo por noite." };
    else if (r.cobertura == null) L.consumo = { k: "sem-folha", t: "Os itens variáveis da Matriz somam " + brl(r.variavelNoite) + " por noite vendida. Com o custo variável por noite da Folha (Módulo 2), a ficha mostraria quanto disso a Matriz explica." };
    else if (r.cobertura > 1.005) L.consumo = { k: "acima", t: "Os itens variáveis da Matriz somam " + brl(r.variavelNoite) + " por noite vendida, mais que o custo variável por noite da Folha (" + brl(N.custoVariavelNoite) + "). Confira se algum item é custo fixo ou se a Folha está desatualizada." };
    else L.consumo = { k: "cobre", t: "Os itens variáveis da Matriz somam " + brl(r.variavelNoite) + " por noite vendida: " + pct(r.cobertura) + " do custo variável por noite da Folha (" + brl(N.custoVariavelNoite) + "). Os outros " + brl(r.restoNoite) + " estão em custos fora desta Matriz, como a limpeza por estadia e a reserva para quebra." };
    L.mesCheio = r.mesCheio == null ? { k: "na", t: "" } : { k: "cheio", t: "Num mês de 30 dias com as " + N.unidades + " unidades vendidas todas as noites, esses itens custariam cerca de " + brl(r.mesCheio) + ". É o número para não ser pego de surpresa no mês cheio, não uma previsão de ocupação." };
    if (!r.itens.some(function (it) { return it.diferenca != null; })) L.cotacao = { k: "na", t: "Sem preço atual e cotações, não dá para comparar." };
    else if (r.diferencaPeriodo > 0.005) L.cotacao = { k: "dif", t: "Na mesma quantidade, a diferença entre o que você paga hoje e a menor cotação soma " + brl(r.diferencaPeriodo) + " no período, cerca de " + brl(r.diferencaAno) + " em doze meses. É uma conta com os seus números, não uma previsão: diluída no ano, essa diferença nunca aparece numa linha só do extrato." };
    else L.cotacao = { k: "igual", t: "O que você paga hoje já é a menor cotação em todos os itens comparados. Guarde as cotações: elas são a base para negociar." };
    L.contrato = r.semContrato.length ? { k: "sem", t: "Sem contrato: " + r.semContrato.join(", ") + ". Preço e prazo acordados para o que se compra todo mês: fornecedor com contrato entrega melhor e cobra menos." } : { k: "ok", t: "Todos os itens recorrentes têm contrato" + (r.aFechar.length ? " ou data para fechar (" + r.aFechar.length + " até " + dataBR(N.prazoContratos) + ")" : "") + "." };
    if (!r.estoque.length) L.estoque = { k: "na", t: "Sem itens no estoque ainda." };
    else if (r.pedirAgora.length) L.estoque = { k: "pedir", t: r.pedirAgora.length + " de " + r.estoque.length + (r.pedirAgora.length === 1 ? " itens está" : " itens estão") + " no ponto de pedido ou abaixo: " + r.pedirAgora.map(function (e) { return e.nome + " (pedir " + e.pedido + ")"; }).join("; ") + ". Pela rotina da Zion, chegou no ponto, aciona o fornecedor." };
    else L.estoque = { k: "ok", t: "Nenhum item no ponto de pedido. Conte o estoque toda semana, no mesmo dia." };
    if (r.porCama == null) L.enxoval = { k: "na", t: "Sem camas informadas, o enxoval não foi dimensionado." };
    else if (r.porCama < JOGOS_POR_CAMA - 1e-9) L.enxoval = { k: "abaixo", t: dec(r.porCama, 1) + " jogos por cama (" + N.jogos + " jogos, " + N.camas + " camas). A fonte recomenda três: a peça descansa, o desgaste cai e a virada não depende da lavanderia. Faltam " + r.jogosFaltam + " jogos." };
    else L.enxoval = { k: "ok", t: dec(r.porCama, 1) + " jogos por cama: dentro dos três que a fonte recomenda." };
    if (!r.calendarioCompleto) L.manutencao = { k: "na", t: "Calendário ainda incompleto." };
    else L.manutencao = { k: "cal", t: r.ocorrencias + " tarefas no ano, " + brl(r.totalAno) + (r.mesMaisPesado ? "; o mês mais pesado é " + r.mesMaisPesado.nome + " (" + brl(r.mesMaisPesado.custo) + ")" : "") + "." };
    if (!r.calendarioCompleto) L.reserva = { k: "na", t: "" };
    else if (r.primeiroDescoberto) L.reserva = { k: "descoberto", t: "Reserva de " + dec(N.reservaPct, 1) + "% de " + brl(N.receitaReserva) + " = " + brl(r.reservaMes) + " por mês. Em " + r.primeiroDescoberto.nome + ", o gasto acumulado do plano passa a reserva acumulada em " + brl(r.primeiroDescoberto.falta) + ": mude a tarefa de mês ou suba a reserva." };
    else L.reserva = { k: "cobre", t: "Reserva de " + dec(N.reservaPct, 1) + "% de " + brl(N.receitaReserva) + " = " + brl(r.reservaMes) + " por mês, " + brl(r.reservaAno) + " no ano. A reserva acumulada cobre o plano em todos os meses e sobra " + brl(r.sobraReserva) + " para reposição (pintura, telhado, equipamento)." };
    L.casaCheia = r.pesadaCasaCheia.length ? { k: "cheia", t: "Manutenção pesada marcada em mês de casa cheia: " + r.pesadaCasaCheia.join(", ") + ". A regra da Zion é trabalhar na baixa ocupação, de preferência de segunda a quinta." } : { k: "ok", t: N.casaCheia.length ? "Nenhuma tarefa semestral ou anual cai nos meses de casa cheia." : "Marque os meses de casa cheia para a ficha conferir se a manutenção pesada fica na baixa." };
    return L;
  }

  // Causa principal e prioridades, na ordem dos passos da fonte: cotar → contratar → estoque → enxoval → manutenção → rotina
  var REGRAS = [
    { id: "cotacao", r: "Item sem três cotações", acao: "Pedir três cotações para cada item da Matriz, na mesma quantidade e com o mesmo prazo de entrega, e anotar na planilha.", verifica: "Cada item da Matriz tem o preço atual e três cotações anotadas com a data.", dispara: function (r) { return r.semTres.length > 0; } },
    { id: "contrato", r: "Compra recorrente sem contrato", acao: "Fechar contrato com preço e prazo para o que se compra todo mês, começando pelo item sem contrato que mais pesa.", verifica: "Os itens recorrentes têm contrato escrito, com preço, prazo de entrega e validade.", dispara: function (r) { return r.semContrato.length > 0; } },
    { id: "pedido", r: "Item no ponto de pedido", acao: "Fazer hoje o pedido dos itens que chegaram ao ponto de pedido e anotar no histórico de compras.", verifica: "Na próxima contagem, nenhum item está abaixo do estoque mínimo.", dispara: function (r) { return r.pedirAgora.length > 0; } },
    { id: "enxoval", r: "Menos de três jogos por cama", acao: "Completar o enxoval até três jogos por cama, comprando pela menor cotação.", verifica: "A contagem de enxoval mostra três jogos completos por cama.", dispara: function (r) { return r.porCama != null && r.porCama < JOGOS_POR_CAMA - 1e-9; } },
    { id: "casa", r: "Manutenção pesada na casa cheia", acao: "Mudar as tarefas semestrais e anuais que caem em meses de casa cheia para meses de baixa, de segunda a quinta.", verifica: "Nenhuma tarefa semestral ou anual cai em mês de casa cheia.", dispara: function (r) { return r.pesadaCasaCheia.length > 0; } },
    { id: "reserva", r: "A reserva não cobre o plano", acao: "Separar a reserva de manutenção todo mês numa conta própria e ajustar o percentual ou a data das tarefas até a reserva acumulada cobrir o plano.", verifica: "Em todos os meses do calendário, a reserva acumulada é maior que o gasto acumulado.", dispara: function (r) { return r.calendarioCompleto && !!r.primeiroDescoberto; } },
    { id: "ronda", r: "Sem ronda diária ou sem registro de ocorrências", acao: "Começar a ronda técnica diária com uma lista curta e registrar cada problema num quadro de ocorrências.", verifica: "Há ronda anotada todos os dias da semana e cada problema tem registro com data e solução.", dispara: function (r) { return !r.N.ronda || !r.N.ocorrencias; } },
    { id: "rotina", r: "Estoque sem dia de contagem ou compra sem limite", acao: "Escolher o dia fixo da contagem semanal do estoque e escrever até quanto a equipe compra fora do previsto sem perguntar.", verifica: "A contagem acontece no mesmo dia toda semana e o limite está escrito para a equipe.", dispara: function (r) { return !r.N.diaContagem || !(r.N.alcada > 0); } },
  ];
  var DENTRO = { id: "ok", r: "Compras e manutenção dentro das regras da fonte", acao: "Manter a contagem semanal, revisar fornecedores e custos todo mês e refazer as cotações antes de renovar cada contrato.", verifica: "A revisão mensal de fornecedores e custos está no calendário e a próxima já tem data." };

  function prioridades(r) {
    var lista = [];
    REGRAS.forEach(function (g) { if (lista.length < 3 && g.dispara(r)) lista.push({ id: g.id, r: g.r, acao: g.acao, verifica: g.verifica }); });
    return lista.length ? lista : [Object.assign({}, DENTRO)];
  }
  function planoSugerido(P) { return P.map(function (p, i) { return (P.length > 1 ? (i + 1) + ". " : "") + p.acao; }).join("\n"); }
  function comoVerificar(P) { return P.map(function (p) { return p.verifica; }).join(" "); }

  // Matriz completa (dá para mostrar o resultado) e lição concluída (selo)
  function completo(S) {
    S = S || {}; if (!S.situacao) return false;
    var v = validar(S); if (!v.ok) return false;
    var r = calcular(S);
    if (r.comTres < 3) return false;
    if (!r.estoque.length) return false;
    if (!r.calendarioCompleto || r.N.tarefas.length < 3) return false;
    return true;
  }
  function concluido(S) { return completo(S) && !!(S.acao && String(S.acao).trim().length >= 10) && !!S.prazo && !!S.pdf; }
  function pendencias(S) {
    var p = [];
    if (!completo(S)) p.push("a Matriz preenchida (pelo menos três itens com preço atual e três cotações, um item de estoque e três tarefas no calendário)");
    if (!(S && S.acao && String(S.acao).trim().length >= 10)) p.push("uma ação com pelo menos 10 letras");
    if (!(S && S.prazo)) p.push("um prazo");
    if (!(S && S.pdf)) p.push("o PDF baixado");
    return p;
  }

  function brl(v) { if (v == null || !isFinite(v)) return "—"; var neg = v < -0.004; var s = Math.abs(v).toFixed(2).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, "."); return (neg ? "−R$ " : "R$ ") + s; }
  function pct(v, d) { if (v == null || !isFinite(v)) return "—"; return (v * 100).toFixed(d == null ? 1 : d).replace(".", ",") + "%"; }
  function dec(v, d) { if (v == null || !isFinite(v)) return "—"; return v.toFixed(d == null ? 1 : d).replace(".", ","); }
  function dataBR(s) { return s ? String(s).split("-").reverse().join("/") : "—"; }

  var TELAS = ["abertura", "consumo", "matriz", "estoque", "manutencao", "rotina", "resultado"];
  var TITULOS = { consumo: "O período e o consumo", matriz: "A Matriz de Compras", estoque: "Estoque mínimo e ponto de pedido", manutencao: "O calendário de manutenção", rotina: "A rotina de compras e manutenção" };
  var PROXIMO = { n: 7, t: "Qualidade, reputação e plano de crescimento" };

  var api = { MESES: MESES, MESES_C: MESES_C, FREQS: FREQS, FREQ: FREQ, TIPOS: TIPOS, CONTRATOS: CONTRATOS, DIAS: DIAS, JOGOS_POR_CAMA: JOGOS_POR_CAMA, DIAS_MES: DIAS_MES,
    SITUACOES: SITUACOES, DIAG: DIAG, SIMNAO: SIMNAO, NIVEIS: NIVEIS, CAMPOS: CAMPOS, CAMPO: CAMPO, EXEMPLO: EXEMPLO, REGRAS: REGRAS, DENTRO: DENTRO, TELAS: TELAS, TITULOS: TITULOS, PROXIMO: PROXIMO,
    num: num, r2: r2, teto: teto, janela: janela, cai: cai, normalizar: normalizar, validar: validar, calcular: calcular, leituras: leituras,
    prioridades: prioridades, planoSugerido: planoSugerido, comoVerificar: comoVerificar, completo: completo, concluido: concluido, pendencias: pendencias, nivel: nivel,
    brl: brl, pct: pct, dec: dec, dataBR: dataBR };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else raiz.ZC = api;
})(typeof window !== "undefined" ? window : this);

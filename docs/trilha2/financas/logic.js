/* Jornada 2 · Gestão · Módulo 2 · Finanças, fluxo de caixa e fechamento
   Lógica pura da ficha "A minha Folha Única do Mês". Sem DOM: roda no navegador (window.ZF) e no Node (testes).
   Regra: tudo que a ficha afirma sai daqui, para ser testado. Nenhuma pontuação ou nota: só as réguas da fonte.
   Parâmetros Zion (17% = 15% + 2%, quebra 1%, reserva 4% entre 3 e 6) são referência ajustável, nunca universal. */
(function (raiz) {
  "use strict";

  var REF = {
    deducoesPct: 15, cancelamentosPct: 2, quebraPct: 1, reservaPct: 4, reservaMin: 3, reservaMax: 6, semanasPorMes: 4.33,
    nota: "referência Zion, ajuste com o seu extrato",
  };

  var SITUACOES = [
    { v: "abrir", r: "Ainda vou abrir a minha hospedagem (vou preencher com os números previstos)", curto: "vai abrir" },
    { v: "dono", r: "Já opero a minha hospedagem e quero fechar o mês passado", curto: "dono que opera" },
    { v: "operador", r: "Cuido da hospedagem de outra pessoa e preciso prestar contas", curto: "operador" },
  ];

  // Diagnóstico de abertura: a Linha de Separação (4 perguntas → nível 1 a 4)
  var DIAG = [
    { id: "conta", r: "O dinheiro da hospedagem fica numa conta separada do seu dinheiro pessoal?" },
    { id: "custo", r: "Você sabe quanto custa cada noite vendida, somando o que sai com a noite e o que sai todo mês?" },
    { id: "retirada", r: "A sua retirada (o que você paga a você mesmo) tem valor fixo e entra como custo todo mês?" },
    { id: "reserva", r: "Existe uma reserva guardada para os meses de baixa?" },
  ];
  var SIMNAO = [{ v: "sim", r: "Sim" }, { v: "nao", r: "Não" }];
  var NIVEIS = [
    { n: 1, r: "Tudo junto", t: "Hoje o dinheiro da hospedagem e o seu se misturam e o mês não tem fechamento. A Folha Única é o primeiro corte." },
    { n: 2, r: "Começando a separar", t: "Uma parte já está separada, mas faltam números para decidir. A Folha vai mostrar o custo por noite e o que sobra." },
    { n: 3, r: "Quase separado", t: "Falta pouco: um número ou uma reserva. A Folha mostra qual deles e o tamanho da diferença." },
    { n: 4, r: "Separado", t: "Conta, custo, retirada e reserva existem. A Folha serve para fechar o mês com método e comparar com o ano anterior." },
  ];
  function nivelSeparacao(S) {
    var d = (S && S.diag) || {}, sim = 0;
    DIAG.forEach(function (q) { if (d[q.id] === "sim") sim++; });
    return NIVEIS[Math.max(0, sim - 1)];
  }

  // Campos numéricos da ficha, por tela, com "por que", "onde conseguir" e exemplo (Cabanas do Vale, dados fictícios)
  // tipo: brl (R$), pct (0 a 99,9), int (número inteiro), texto
  var CAMPOS = [
    { id: "mes", tela: "mes", tipo: "texto", r: "Mês e ano", pq: "A Folha fecha um mês por vez.", onde: "O mês passado inteiro, do dia 1 ao último dia.", ex: "Outubro de 2026", obrig: true },
    { id: "dias", tela: "mes", tipo: "int", min: 28, max: 31, r: "Dias do mês", pq: "Junto com as unidades, dá as noites que você tinha para vender.", onde: "28, 29, 30 ou 31.", ex: "31", obrig: true },
    { id: "unidades", tela: "mes", tipo: "int", min: 1, max: 999, r: "Unidades à venda", pq: "Só as que estavam disponíveis para reserva no mês.", onde: "Quartos, cabanas ou casas abertas no mês.", ex: "4", obrig: true },
    { id: "noites", tela: "mes", tipo: "int", min: 0, r: "Noites vendidas", pq: "É o divisor de quase todos os indicadores: diária média e custo por noite.", onde: "Some as noites de todas as reservas do mês, em todas as unidades. Está no calendário das plataformas.", ex: "58", obrig: true },
    { id: "estadias", tela: "mes", tipo: "int", min: 0, r: "Estadias (reservas)", pq: "Dá a média de noites por estadia: limpeza e enxoval saem por estadia, não por noite.", onde: "Conte as reservas com entrada no mês.", ex: "25" },

    { id: "receitaHospedagem", tela: "entrou", tipo: "brl", r: "Receita de hospedagem (só diárias, bruta)", pq: "É o faturamento das diárias, antes de qualquer desconto, comissão ou imposto.", onde: "Relatório de ganhos das plataformas + reservas diretas, sem a taxa de limpeza.", ex: "16.240,00", obrig: true },
    { id: "taxaLimpezaCobrada", tela: "entrou", tipo: "brl", r: "Taxa de limpeza cobrada do hóspede", pq: "Não é receita de hospedagem: é repasse. Ela abate a limpeza que você paga.", onde: "Número de estadias × taxa de limpeza cobrada.", ex: "1.500,00 (25 × 60)" },
    { id: "outrasReceitas", tela: "entrou", tipo: "brl", r: "Outras receitas", pq: "Café, cestas, experiências, venda de produtos. Entram no faturamento, mas não na diária.", onde: "Extrato e maquininha.", ex: "980,00" },
    { id: "custoOutrasReceitas", tela: "entrou", tipo: "brl", r: "Custo das outras receitas", pq: "O que você gastou para entregar o café, a cesta ou a experiência.", onde: "Notas de compra do mês.", ex: "420,00" },
    { id: "descontos", tela: "entrou", tipo: "brl", r: "Descontos dados", pq: "Promoções e descontos saem da receita antes de qualquer conta.", onde: "Relatório de reservas: diferença entre o preço cheio e o pago.", ex: "650,00" },
    { id: "comissoesPct", tela: "entrou", tipo: "pct", r: "Comissões dos canais (%)", pq: "A plataforma fica com uma parte de cada reserva.", onde: "Extrato de repasses de cada canal. Se não sabe, use a referência Zion.", ex: "11" },
    { id: "processamentoPct", tela: "entrou", tipo: "pct", r: "Taxa de processamento do pagamento (%)", pq: "Cartão, Pix com taxa e antecipação também saem da receita.", onde: "Extrato da maquininha ou do gateway.", ex: "1,5" },
    { id: "impostoPct", tela: "entrou", tipo: "pct", r: "Imposto sobre a receita (%)", pq: "O imposto sobre o que você fatura não é custo: é dedução.", onde: "Guia do mês ou o seu contador.", ex: "6" },
    { id: "cancelamentos", tela: "entrou", tipo: "brl", r: "Cancelamentos e não comparecimento (R$ perdidos)", pq: "Receita que você contava e não entrou.", onde: "Relatório de cancelamentos. Se não sabe, a referência Zion é 2% da receita.", ex: "0,00" },

    { id: "limpezaPaga", tela: "variaveis", tipo: "brl", r: "Limpeza paga", pq: "Sai por estadia. A taxa de limpeza cobrada abate daqui.", onde: "Pagamentos à equipe ou à empresa de limpeza no mês.", ex: "2.000,00 (25 × 80)" },
    { id: "enxoval", tela: "variaveis", tipo: "brl", r: "Enxoval e lavanderia", pq: "Lavagem, reposição de toalhas e roupa de cama.", onde: "Notas da lavanderia e compras do mês.", ex: "380,00" },
    { id: "amenidades", tela: "variaveis", tipo: "brl", r: "Amenidades", pq: "Sabonete, papel, café de cortesia, mimos.", onde: "Compras do mês.", ex: "260,00" },
    { id: "energiaVariavel", tela: "variaveis", tipo: "brl", r: "Energia, água e gás das unidades", pq: "A parte que sobe quando a unidade está ocupada.", onde: "Conta de luz, água e gás das unidades (a parte comum vai em fixos).", ex: "340,00" },
    { id: "cafe", tela: "variaveis", tipo: "brl", r: "Café da manhã", pq: "Só se o café está incluído na diária. Se é vendido à parte, já está em outras receitas.", onde: "Compras do mês.", ex: "0,00 (está em outras)" },
    { id: "quebra", tela: "variaveis", tipo: "brl", r: "Quebra e perda", pq: "Louça, toalha, controle, decoração que quebra ou some.", onde: "Se não mede, use a referência Zion: 1% da receita de hospedagem.", ex: "referência 1% = 162,40" },
    { id: "outrosVariaveis", tela: "variaveis", tipo: "brl", r: "Outros custos por noite", pq: "O que mais sai só quando há hóspede.", onde: "Extrato.", ex: "0,00" },

    { id: "equipe", tela: "fixos", tipo: "brl", r: "Equipe (salários, diárias fixas, encargos)", pq: "Sai todo mês, com ou sem hóspede.", onde: "Folha ou recibos.", ex: "1.800,00" },
    { id: "comuns", tela: "fixos", tipo: "brl", r: "Energia, água e internet das áreas comuns", pq: "A parte que não muda com a ocupação.", onde: "Contas do mês.", ex: "620,00" },
    { id: "software", tela: "fixos", tipo: "brl", r: "Sistemas e assinaturas", pq: "Gestor de canais, site, aplicativos.", onde: "Cartão de crédito.", ex: "190,00" },
    { id: "contador", tela: "fixos", tipo: "brl", r: "Contador", pq: "Honorário mensal.", onde: "Boleto do contador.", ex: "300,00" },
    { id: "marketingFixo", tela: "fixos", tipo: "brl", r: "Marketing fixo", pq: "Anúncio recorrente, fotógrafo, site.", onde: "Extrato.", ex: "150,00" },
    { id: "duodecimos", tela: "fixos", tipo: "brl", r: "Despesas anuais ÷ 12", pq: "Imposto predial, seguro, licenças e décimo terceiro chegam uma vez por ano, mas são custo todo mês.", onde: "Some as despesas anuais e divida por 12.", ex: "460,00" },
    { id: "manutencaoContratada", tela: "fixos", tipo: "brl", r: "Manutenção contratada", pq: "Jardim, piscina, contrato de manutenção.", onde: "Recibos.", ex: "250,00" },
    { id: "retirada", tela: "fixos", tipo: "brl", r: "A sua retirada (Conta da Retirada)", pq: "O que custaria pagar alguém para fazer o que você faz. Sem ela, o resultado mente.", onde: "Horas por semana × valor da hora × 4,33 semanas, ou um valor direto.", ex: "20 h × R$ 40 × 4,33 = 3.464,00" },
    { id: "outrosFixos", tela: "fixos", tipo: "brl", r: "Outros custos fixos", pq: "O que mais sai todo mês.", onde: "Extrato.", ex: "0,00" },

    { id: "aluguel", tela: "modelo", tipo: "brl", r: "Aluguel ou arrendamento do imóvel", pq: "É custo do modelo, não da operação: muda se o imóvel fosse seu.", onde: "Contrato.", ex: "0,00" },
    { id: "taxaGestao", tela: "modelo", tipo: "brl", r: "Taxa de gestão ou administração", pq: "Quando alguém administra por você.", onde: "Contrato.", ex: "0,00" },
    { id: "marca", tela: "modelo", tipo: "brl", r: "Marca, franquia ou rede", pq: "Taxas de uso de marca.", onde: "Contrato.", ex: "0,00" },
    { id: "reservaPct", tela: "modelo", tipo: "pct", r: "Reserva de reposição (% da receita real)", pq: "Guarda dinheiro para trocar colchão, ar-condicionado e eletrodomésticos quando chegar a hora.", onde: "Referência Zion: 3 a 6%, padrão 4%.", ex: "4" },
    { id: "depreciacao", tela: "modelo", tipo: "brl", r: "Depreciação (só informativa)", pq: "Conta contábil. Nunca entra junto com a reserva na mesma conta.", onde: "O seu contador.", ex: "0,00" },

    { id: "saldoInicial", tela: "caixa", tipo: "brl", r: "Saldo no dia 1", pq: "O caixa começa aqui.", onde: "Extrato da conta da hospedagem no primeiro dia do mês.", ex: "9.800,00", obrig: true },
    { id: "entradasCaixa", tela: "caixa", tipo: "brl", r: "Tudo que entrou na conta", pq: "Caixa é o que caiu, já líquido do que a plataforma reteve.", onde: "Soma dos créditos do extrato.", ex: "18.470,00", obrig: true },
    { id: "saidasCaixa", tela: "caixa", tipo: "brl", r: "Tudo que saiu da conta", pq: "Inclui pagamentos de meses anteriores e compras grandes.", onde: "Soma dos débitos do extrato.", ex: "14.650,00", obrig: true },
    { id: "reservasSeparadas", tela: "caixa", tipo: "brl", r: "Reservas já guardadas", pq: "Baixa temporada, reposição, manutenção e despesas anuais, somadas.", onde: "Saldo da conta de reservas.", ex: "0,00" },
    { id: "aReceber", tela: "caixa", tipo: "brl", r: "A receber (repasses ainda não caídos)", pq: "Explica a diferença entre resultado e caixa.", onde: "Painel de pagamentos das plataformas.", ex: "0,00" },
  ];
  var CAMPO = {}; CAMPOS.forEach(function (c) { CAMPO[c.id] = c; });

  // Exemplo didático · dados fictícios (Cabanas do Vale, outubro)
  var EXEMPLO = {
    situacao: "dono", hospedagem: "Cabanas do Vale (exemplo)", diag: { conta: "sim", custo: "nao", retirada: "sim", reserva: "nao" },
    mes: "Outubro de 2026", dias: 31, unidades: 4, noites: 58, estadias: 25,
    receitaHospedagem: 16240, taxaLimpezaCobrada: 1500, outrasReceitas: 980, custoOutrasReceitas: 420,
    descontos: 650, comissoesPct: 11, processamentoPct: 1.5, impostoPct: 6, cancelamentos: 0,
    limpezaPaga: 2000, enxoval: 380, amenidades: 260, energiaVariavel: 340, cafe: 0, quebra: "", quebraRef: true, outrosVariaveis: 0,
    equipe: 1800, comuns: 620, software: 190, contador: 300, marketingFixo: 150, duodecimos: 460, manutencaoContratada: 250,
    retiradaModo: "horas", retiradaHoras: 20, retiradaValorHora: 40, retirada: "", retiradaDecidida: false, outrosFixos: 0,
    aluguel: 0, taxaGestao: 0, marca: 0, reservaPct: 4, depreciacao: "",
    saldoInicial: 9800, entradasCaixa: 18470, saidasCaixa: 14650, reservasSeparadas: 0, aReceber: 0,
  };

  // Converte "1.234,56", "1234.56", 1234 em número; vazio ou inválido vira null
  function num(v) {
    if (v == null) return null;
    if (typeof v === "number") return isFinite(v) ? v : null;
    var s = String(v).trim(); if (!s) return null;
    s = s.replace(/\s|R\$|%/g, "");
    if (/,/.test(s)) s = s.replace(/\./g, "").replace(",", "."); // formato brasileiro
    var n = Number(s); return isFinite(n) ? n : null;
  }
  function informado(v) { return v != null && String(v).trim() !== ""; }

  // Normaliza o estado: números, vazio = 0 onde permitido, retirada e referências resolvidas; devolve também o que foi informado
  function normalizar(S) {
    S = S || {}; var N = { informado: {} };
    CAMPOS.forEach(function (c) {
      var v = S[c.id];
      N.informado[c.id] = informado(v);
      if (c.tipo === "texto") N[c.id] = v == null ? "" : String(v).trim();
      else { var n = num(v); N[c.id] = n == null ? 0 : n; }
    });
    if (!N.informado.reservaPct) N.reservaPct = REF.reservaPct;
    N.vaiAbrir = S.situacao === "abrir" || !!S.vaiAbrir;
    N.cancelamentosRef = !!S.cancelamentosRef; N.deducoesRef = !!S.deducoesRef; N.quebraRef = !!S.quebraRef;
    N.retiradaDecidida = !!S.retiradaDecidida;
    N.retiradaModo = S.retiradaModo === "horas" ? "horas" : "valor";
    N.retiradaHoras = num(S.retiradaHoras) || 0; N.retiradaValorHora = num(S.retiradaValorHora) || 0;
    if (N.retiradaModo === "horas") { N.retirada = N.retiradaHoras * N.retiradaValorHora * REF.semanasPorMes; N.informado.retirada = informado(S.retiradaHoras) && informado(S.retiradaValorHora); }
    if (N.retiradaDecidida) { N.retirada = 0; N.informado.retirada = true; }
    if (N.cancelamentosRef) N.cancelamentos = N.receitaHospedagem * REF.cancelamentosPct / 100;
    if (N.quebraRef) N.quebra = N.receitaHospedagem * REF.quebraPct / 100;
    return N;
  }

  // Aplica a referência Zion às deduções: comissões + processamento + imposto = 15% e cancelamentos = 2% da receita
  function aplicarReferenciaDeducoes(S) {
    var T = Object.assign({}, S);
    T.comissoesPct = REF.deducoesPct; T.processamentoPct = 0; T.impostoPct = 0; T.cancelamentosRef = true; T.cancelamentos = ""; T.deducoesRef = true;
    return T;
  }

  // Bloqueios (impedem avançar) por tela, e avisos (não impedem)
  function validar(S, tela) {
    var N = normalizar(S), erros = [], avisos = [];
    CAMPOS.forEach(function (c) {
      if (tela && c.tela !== tela) return;
      if (c.tipo === "texto") { if (c.obrig && !N[c.id]) erros.push("Falta " + c.r.toLowerCase() + "."); return; }
      var bruto = S ? S[c.id] : null;
      if (c.obrig && !N.informado[c.id] && !(c.id === "retirada")) erros.push("Falta " + c.r.toLowerCase() + ".");
      if (informado(bruto) && num(bruto) == null) erros.push(c.r + ": escreva só números (use vírgula para centavos).");
      if (N[c.id] < 0) erros.push(c.r + ": não pode ser negativo.");
      if (c.tipo === "pct" && N[c.id] > 99.9) erros.push(c.r + ": use um percentual de 0 a 99,9.");
      if (c.tipo === "int" && N.informado[c.id] && N[c.id] !== Math.floor(N[c.id])) erros.push(c.r + ": use um número inteiro.");
      if (c.min != null && N.informado[c.id] && N[c.id] < c.min) erros.push(c.r + ": o mínimo é " + c.min + ".");
      if (c.max != null && N.informado[c.id] && N[c.id] > c.max) erros.push(c.r + ": o máximo é " + c.max + ".");
    });
    if (!tela || tela === "mes") {
      if (N.informado.noites && N.unidades > 0 && N.dias > 0 && N.noites > N.unidades * N.dias) erros.push("Noites vendidas (" + N.noites + ") passam das noites disponíveis (" + N.unidades * N.dias + ").");
      if (N.noites > 0 && N.estadias === 0) avisos.push("Sem o número de estadias, a Folha assume uma estadia por noite (" + N.noites + " estadias). Confira: limpeza e enxoval saem por estadia.");
    }
    if (!tela || tela === "entrou") {
      var ded = deducoesDe(N);
      if (ded > N.receitaHospedagem + 0.005) erros.push("As deduções (" + brl(ded) + ") passam da receita de hospedagem (" + brl(N.receitaHospedagem) + "). Confira descontos, percentuais e cancelamentos.");
      if (N.informado.receitaHospedagem && N.receitaHospedagem === 0 && !N.vaiAbrir) avisos.push("Receita de hospedagem zero: a Folha vai mostrar o custo de um mês sem venda.");
      if (N.taxaLimpezaCobrada > 0 && N.taxaLimpezaCobrada > N.limpezaPaga && N.informado.limpezaPaga) avisos.push("Você cobra mais de limpeza do que paga: o excedente entra em outras receitas.");
    }
    if (!tela || tela === "fixos") {
      if (num(S && S.retiradaHoras) != null && num(S.retiradaHoras) < 0) erros.push("Horas por semana: não pode ser negativo.");
      if (num(S && S.retiradaValorHora) != null && num(S.retiradaValorHora) < 0) erros.push("Valor da hora: não pode ser negativo.");
      if (N.retiradaModo === "horas" && N.retiradaHoras > 168) erros.push("Horas por semana: o máximo é 168.");
    }
    return { erros: erros, avisos: avisos, ok: erros.length === 0 };
  }
  function deducoesDe(N) { return N.descontos + N.receitaHospedagem * (N.comissoesPct + N.processamentoPct + N.impostoPct) / 100 + N.cancelamentos; }

  function div(a, b) { return b > 0 ? a / b : null; }

  // A cascata completa e os indicadores (PLANO 6.2). Divisões por zero devolvem null.
  function calcular(S) {
    var N = normalizar(S), v = validar(S);
    var r = { N: N, bloqueios: v.erros, avisos: v.avisos };
    r.noitesDisponiveis = N.unidades * N.dias;
    r.ocupacao = div(N.noites, r.noitesDisponiveis);
    r.estadiasUsadas = N.estadias > 0 ? N.estadias : N.noites; r.estadiasAssumidas = N.estadias === 0 && N.noites > 0;
    r.mediaNoitesPorEstadia = r.estadiasUsadas > 0 ? N.noites / r.estadiasUsadas : null;
    r.deducoes = deducoesDe(N);
    r.deducoesAcimaDaReceita = r.deducoes > N.receitaHospedagem + 0.005;
    r.receitaRealHospedagem = Math.max(0, N.receitaHospedagem - r.deducoes);
    r.limpezaLiquida = Math.max(0, N.limpezaPaga - N.taxaLimpezaCobrada);
    r.excedenteLimpeza = Math.max(0, N.taxaLimpezaCobrada - N.limpezaPaga);
    r.outrasReceitasTotal = N.outrasReceitas + r.excedenteLimpeza;
    r.margemOutras = r.outrasReceitasTotal - N.custoOutrasReceitas;
    r.receitaBrutaTotal = N.receitaHospedagem + r.outrasReceitasTotal;
    r.receitaReal = r.receitaRealHospedagem + r.outrasReceitasTotal;
    r.quebraValor = N.quebra;
    r.variaveis = r.limpezaLiquida + N.enxoval + N.amenidades + N.energiaVariavel + N.cafe + r.quebraValor + N.outrosVariaveis + N.custoOutrasReceitas;
    r.margemContribuicao = r.receitaReal - r.variaveis;
    r.retirada = N.retirada;
    r.fixosOperacionais = N.equipe + N.comuns + N.software + N.contador + N.marketingFixo + N.duodecimos + N.manutencaoContratada + N.retirada + N.outrosFixos;
    r.resultadoOperacional = r.margemContribuicao - r.fixosOperacionais;
    r.custosModelo = N.aluguel + N.taxaGestao + N.marca;
    r.ebitda = r.resultadoOperacional - r.custosModelo;
    r.reservaReposicao = r.receitaReal * N.reservaPct / 100;
    r.geracaoCaixa = r.ebitda - r.reservaReposicao;
    r.resultadoContabilIndicativo = N.informado.depreciacao ? r.ebitda - N.depreciacao : null;
    // Caixa
    r.saldoFinal = N.saldoInicial + N.entradasCaixa - N.saidasCaixa;
    r.variacaoCaixa = r.saldoFinal - N.saldoInicial;
    r.fixoTotalMes = r.fixosOperacionais + r.custosModelo;
    r.mesesFolego = div(r.saldoFinal + N.reservasSeparadas, r.fixoTotalMes);
    // Indicadores
    r.diariaMediaBruta = div(N.receitaHospedagem, N.noites);
    r.diariaMediaReal = div(r.receitaRealHospedagem, N.noites);
    r.taxaDeducaoReal = div(r.deducoes, N.receitaHospedagem);
    r.custoVariavelPorNoite = div(r.variaveis - N.custoOutrasReceitas, N.noites);
    r.custoFixoPorNoite = div(r.fixoTotalMes, N.noites);
    r.custoPorNoiteVendida = r.custoVariavelPorNoite == null ? null : r.custoVariavelPorNoite + r.custoFixoPorNoite;
    r.margemPorNoite = r.diariaMediaReal == null ? null : r.diariaMediaReal - r.custoVariavelPorNoite;
    r.pontoEquilibrioNoites = r.margemPorNoite != null && r.margemPorNoite > 0 ? Math.max(0, (r.fixoTotalMes - r.margemOutras) / r.margemPorNoite) : null;
    r.naoFecha = r.margemPorNoite != null && r.margemPorNoite <= 0;
    r.ocupacaoEquilibrio = r.pontoEquilibrioNoites == null ? null : div(r.pontoEquilibrioNoites, r.noitesDisponiveis);
    r.margemOperacionalPct = div(r.resultadoOperacional, r.receitaBrutaTotal);
    r.receitaPorNoiteDisponivel = div(N.receitaHospedagem, r.noitesDisponiveis);
    r.sobrouPct = r.margemOperacionalPct;
    return r;
  }

  // Leituras só com as réguas da fonte (PLANO 6.3)
  function leituras(r) {
    var L = {};
    if (r.N.noites === 0) L.noite = { k: "sem", t: "Sem noite vendida, cada real que saiu é prejuízo. Os indicadores por noite não existem neste mês." };
    else if (r.diariaMediaReal >= r.custoPorNoiteVendida) L.noite = { k: "paga", t: "Cada noite vendida paga tudo e sobra: a diária média real (" + brl(r.diariaMediaReal) + ") está acima do custo por noite vendida (" + brl(r.custoPorNoiteVendida) + ")." };
    else if (r.diariaMediaReal >= r.custoVariavelPorNoite) L.noite = { k: "ajuda", t: "Cada noite paga o variável e ajuda no fixo, mas o mês não fecha: a diária média real (" + brl(r.diariaMediaReal) + ") fica entre o custo variável por noite (" + brl(r.custoVariavelPorNoite) + ") e o custo por noite vendida (" + brl(r.custoPorNoiteVendida) + ")." };
    else L.noite = { k: "consome", t: "Cada noite vendida consome valor: a diária média real (" + brl(r.diariaMediaReal) + ") está abaixo do custo variável por noite (" + brl(r.custoVariavelPorNoite) + ")." };

    var o = r.ocupacaoEquilibrio;
    if (r.naoFecha) L.equilibrio = { k: "naofecha", t: "Não fecha: a diária média real não cobre nem o custo variável por noite. Nenhuma ocupação resolve; a correção é na diária ou no variável." };
    else if (o == null) L.equilibrio = { k: "na", t: "Ponto de equilíbrio não calculável neste mês (sem noite vendida ou sem receita)." };
    else if (o > 0.70) L.equilibrio = { k: "alerta", t: "Ocupação de equilíbrio de " + pct(o) + ": alerta. Acima de 70%, a correção é estrutural: diária, custo variável ou custo fixo." };
    else if (o > 0.65) L.equilibrio = { k: "limite", t: "Ocupação de equilíbrio de " + pct(o) + ": no limite. Entre 65 e 70%, qualquer mês fraco deixa o resultado negativo." };
    else if (o >= 0.45) L.equilibrio = { k: "saudavel", t: "Ocupação de equilíbrio de " + pct(o) + ": saudável. Entre 45 e 65%, a hospedagem fecha o mês com ocupação que o destino costuma entregar." };
    else L.equilibrio = { k: "folgada", t: "Ocupação de equilíbrio de " + pct(o) + ": folgada. Abaixo de 45%, sobra margem para a baixa temporada." };

    var f = r.mesesFolego;
    if (f == null) L.folego = { k: "na", t: "Meses de fôlego não calculável: não há custo fixo lançado." };
    else if (f < 2) L.folego = { k: "risco", t: "Fôlego de " + dec(f, 1) + " meses: zona de risco. Abaixo de 2 meses de custo fixo guardado, um mês fraco vira dívida." };
    else if (f < 4) L.folego = { k: "apertado", t: "Fôlego de " + dec(f, 1) + " meses: apertado. Entre 2 e 4 meses, dá para atravessar uma baixa curta." };
    else if (f <= 6) L.folego = { k: "confortavel", t: "Fôlego de " + dec(f, 1) + " meses: confortável. Entre 4 e 6 meses, a baixa temporada não assusta." };
    else L.folego = { k: "muito", t: "Fôlego de " + dec(f, 1) + " meses: muito confortável. Acima de 6, confira se há dinheiro parado que poderia virar reposição ou melhoria." };

    var m = r.margemOperacionalPct;
    if (m == null) L.margem = { k: "na", t: "Sem receita no mês, não há margem para ler: tudo que saiu é resultado negativo." };
    else if (m > 0.30) L.margem = { k: "boa", t: "Quanto sobrou do mês: " + pct(m) + " do faturamento. Acima de 30%, margem boa (régua anual, usada aqui como referência indicativa)." };
    else if (m >= 0.20) L.margem = { k: "viavel", t: "Quanto sobrou do mês: " + pct(m) + " do faturamento. Entre 20 e 30%, margem viável (régua anual, usada aqui como referência indicativa)." };
    else if (m >= 0.10) L.margem = { k: "apertada", t: "Quanto sobrou do mês: " + pct(m) + " do faturamento. Entre 10 e 20%, margem apertada (régua anual, usada aqui como referência indicativa)." };
    else L.margem = { k: "naofecha", t: "Quanto sobrou do mês: " + pct(m) + " do faturamento. Abaixo de 10%, o mês não fecha (régua anual, usada aqui como referência indicativa)." };

    var subiu = r.variacaoCaixa > 0, positivo = r.resultadoOperacional >= 0;
    if (subiu && !positivo) L.caixa = { k: "caixa-bom", t: "Caixa bom e resultado ruim: o saldo subiu " + brl(r.variacaoCaixa) + ", mas o mês deu " + brl(r.resultadoOperacional) + ". Típico de alta temporada ou de repasse que ainda vai sair." };
    else if (!subiu && positivo) L.caixa = { k: "resultado-bom", t: "Caixa ruim e resultado bom: o mês deu " + brl(r.resultadoOperacional) + ", mas o saldo " + (r.variacaoCaixa === 0 ? "não se mexeu" : "caiu " + brl(-r.variacaoCaixa)) + ". Investimento ou pagamento concentrado." };
    else if (!subiu && !positivo) L.caixa = { k: "dois", t: "Os dois alertas ao mesmo tempo: o saldo caiu " + brl(-r.variacaoCaixa) + " e o mês deu " + brl(r.resultadoOperacional) + ". Faturamento, lucro, caixa e margem são quatro coisas diferentes, e aqui as quatro pedem atenção." };
    else L.caixa = { k: "juntos", t: "Caixa e resultado andam juntos: o saldo subiu " + brl(r.variacaoCaixa) + " e o mês deu " + brl(r.resultadoOperacional) + ". Confira se parte do saldo é repasse de reserva futura." };
    if (r.N.aReceber > 0) L.caixa.t += " Há " + brl(r.N.aReceber) + " a receber que ainda não caiu na conta.";
    return L;
  }

  // Regra do desconto em três faixas (Etapa 09): a diária com desconto comparada ao custo por noite
  function faixaDesconto(diaria, r) {
    var d = num(diaria);
    if (d == null || r.custoPorNoiteVendida == null) return { k: "na", t: "Sem custo por noite vendida, não dá para avaliar o desconto." };
    if (d >= r.custoPorNoiteVendida) return { k: "pode", t: "Pode dar: " + brl(d) + " cobre o custo por noite vendida (" + brl(r.custoPorNoiteVendida) + ") e ainda sobra." };
    if (d >= r.custoVariavelPorNoite) return { k: "so-vazia", t: "Só para noite que ficaria vazia: " + brl(d) + " paga o variável (" + brl(r.custoVariavelPorNoite) + ") e ajuda no fixo, mas não cobre o custo por noite vendida (" + brl(r.custoPorNoiteVendida) + ")." };
    return { k: "nao", t: "Não dê: " + brl(d) + " fica abaixo do custo variável por noite (" + brl(r.custoVariavelPorNoite) + "). Cada noite assim consome valor." };
  }

  // Causa principal e prioridades, na ordem de correção da fonte (PLANO 6.4)
  var REGRAS = [
    { id: "duodecimos", r: "Despesas anuais sem provisão", acao: "Dividir imposto predial, seguro, licenças e décimo terceiro por 12 e lançar o valor todo mês como custo fixo.", verifica: "A linha \"despesas anuais ÷ 12\" da Folha do mês seguinte tem valor maior que zero.", dispara: function (r) { return r.N.duodecimos === 0; } },
    { id: "reserva", r: "Sem reserva para a baixa", acao: "Abrir uma conta separada para as reservas e programar a transferência para o dia em que a receita entra.", verifica: "A conta existe e a primeira transferência foi feita no dia do repasse.", dispara: function (r) { return r.N.reservasSeparadas === 0; } },
    { id: "retirada", r: "Retirada não lançada", acao: "Fazer a Conta da Retirada (horas por semana × valor da hora × 4,33) e lançar o valor como custo fixo todo mês.", verifica: "A Folha do mês seguinte tem a retirada lançada ou a decisão de retirada zero escrita.", dispara: function (r) { return r.N.retirada === 0 && !r.N.retiradaDecidida; } },
    { id: "diaria", r: "Diária abaixo do custo real", acao: "Calcular o piso da diária com o custo por noite vendida e revisar a diária no módulo 3 · Preço.", verifica: "A diária média real do mês seguinte está acima do custo por noite vendida.", dispara: function (r) { return r.diariaMediaReal != null && r.diariaMediaReal < r.custoPorNoiteVendida; } },
    { id: "variavel", r: "Custo variável mal medido ou alto", acao: "Guardar três meses de notas por item e medir a limpeza por estadia.", verifica: "Cada linha de custo variável tem nota ou recibo nos três meses.", dispara: function (r) { return r.custoVariavelPorNoite != null && r.diariaMediaReal != null && r.custoVariavelPorNoite >= 0.5 * r.diariaMediaReal; } },
    { id: "deducoes", r: "Deduções acima da faixa da fonte (15 a 25%)", acao: "Conciliar os repasses por canal e rever a mistura de canais no módulo 3.", verifica: "A taxa de dedução real do mês seguinte está dentro de 15 a 25%.", dispara: function (r) { return r.taxaDeducaoReal != null && r.taxaDeducaoReal > 0.25; } },
    { id: "equilibrio", r: "Modelo exige ocupação que o destino não entrega", acao: "Corrigir na ordem: primeiro a diária, depois o custo variável, depois o custo fixo.", verifica: "A ocupação de equilíbrio do mês seguinte está abaixo de 70%.", dispara: function (r) { return r.ocupacaoEquilibrio != null && r.ocupacaoEquilibrio > 0.70; } },
  ];
  var DENTRO = { id: "ok", r: "Mês dentro das réguas", acao: "Comparar com o mesmo mês do ano anterior e manter a rotina: 5 minutos por semana, 10 minutos por mês.", verifica: "A Folha do mês seguinte está preenchida e comparada com o mesmo mês do ano anterior." };

  function prioridades(r, S) {
    var lista = [];
    REGRAS.forEach(function (g) { if (lista.length < 3 && g.dispara(r, S)) lista.push({ id: g.id, r: g.r, acao: g.acao, verifica: g.verifica }); });
    return lista.length ? lista : [Object.assign({}, DENTRO)];
  }
  function causaPrincipal(r, S) { return prioridades(r, S)[0]; }
  function planoSugerido(prios) {
    return prios.map(function (p, i) { return (prios.length > 1 ? (i + 1) + ". " : "") + p.acao; }).join("\n");
  }
  function comoVerificar(prios) { return prios.map(function (p) { return p.verifica; }).join(" "); }

  // Folha preenchida (dá para mostrar o resultado) e lição concluída (selo), PLANO 6.5
  function completo(S) {
    S = S || {}; var N = normalizar(S), v = validar(S);
    if (!v.ok) return false;
    if (!S.situacao) return false;
    if (!(N.mes && N.informado.dias && N.informado.unidades && N.informado.noites)) return false;
    if (!(N.receitaHospedagem > 0 || N.vaiAbrir)) return false;
    var temVariavel = ["limpezaPaga", "enxoval", "amenidades", "energiaVariavel", "cafe", "quebra", "outrosVariaveis"].some(function (k) { return N.informado[k] || (k === "quebra" && N.quebraRef); });
    var temFixo = ["equipe", "comuns", "software", "contador", "marketingFixo", "duodecimos", "manutencaoContratada", "retirada", "outrosFixos"].some(function (k) { return N.informado[k]; });
    if (!temVariavel || !temFixo) return false;
    if (!N.informado.retirada) return false;
    if (!(N.informado.saldoInicial && N.informado.entradasCaixa && N.informado.saidasCaixa)) return false;
    return true;
  }
  function concluido(S) {
    return completo(S) && !!(S.acao && String(S.acao).trim().length >= 10) && !!S.prazo && !!S.pdf;
  }
  function pendencias(S) {
    var p = [];
    if (!completo(S)) p.push("a Folha preenchida (receita, noites, um custo variável, um fixo, a retirada e o caixa)");
    if (!(S && S.acao && String(S.acao).trim().length >= 10)) p.push("uma ação com pelo menos 10 letras");
    if (!(S && S.prazo)) p.push("um prazo");
    if (!(S && S.pdf)) p.push("o PDF baixado");
    return p;
  }

  // Formatação (sem DOM)
  function brl(v) { if (v == null || !isFinite(v)) return "—"; var neg = v < 0; var s = Math.abs(v).toFixed(2).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, "."); return (neg ? "−R$ " : "R$ ") + s; }
  function pct(v, d) { if (v == null || !isFinite(v)) return "—"; return (v * 100).toFixed(d == null ? 1 : d).replace(".", ",") + "%"; }
  function dec(v, d) { if (v == null || !isFinite(v)) return "—"; return v.toFixed(d == null ? 1 : d).replace(".", ","); }

  // Linhas da cascata para a tabela e o PDF
  function cascata(r) {
    return [
      { r: "Receita de hospedagem (bruta)", v: r.N.receitaHospedagem },
      { r: "− Deduções (descontos, comissões, processamento, imposto, cancelamentos)", v: -r.deducoes },
      { r: "= Receita real de hospedagem", v: r.receitaRealHospedagem, forte: true },
      { r: "+ Outras receitas (inclui excedente da taxa de limpeza)", v: r.outrasReceitasTotal },
      { r: "= Receita real total", v: r.receitaReal, forte: true },
      { r: "− Custos variáveis (o que sai com cada noite)", v: -r.variaveis },
      { r: "= Margem de contribuição", v: r.margemContribuicao, forte: true },
      { r: "− Custos fixos operacionais (com a sua retirada de " + brl(r.retirada) + ")", v: -r.fixosOperacionais },
      { r: "= Quanto sobrou do mês (resultado operacional)", v: r.resultadoOperacional, forte: true, destaque: true },
      { r: "− Custos do modelo (aluguel, gestão, marca)", v: -r.custosModelo },
      { r: "= Resultado antes de juros, impostos sobre o lucro e depreciação", v: r.ebitda, forte: true },
      { r: "− Reserva de reposição (" + dec(r.N.reservaPct, 1) + "% da receita real)", v: -r.reservaReposicao },
      { r: "= O que ficou no caixa para o negócio (geração de caixa)", v: r.geracaoCaixa, forte: true, destaque: true },
    ];
  }
  function indicadores(r) {
    return [
      { id: "ocupacao", r: "Ocupação", v: pct(r.ocupacao), n: r.noitesDisponiveis ? r.N.noites + " de " + r.noitesDisponiveis + " noites" : "" },
      { id: "diariaBruta", r: "Diária média bruta", v: brl(r.diariaMediaBruta) },
      { id: "diariaReal", r: "Diária média real", v: brl(r.diariaMediaReal), n: "taxa de dedução real " + pct(r.taxaDeducaoReal) },
      { id: "custoVar", r: "Custo variável por noite", v: brl(r.custoVariavelPorNoite) },
      { id: "custoNoite", r: "Custo por noite vendida", v: brl(r.custoPorNoiteVendida), n: "variável + fixo ÷ noites" },
      { id: "margemNoite", r: "Margem por noite", v: brl(r.margemPorNoite) },
      { id: "pe", r: "Ponto de equilíbrio", v: r.naoFecha ? "não fecha" : r.pontoEquilibrioNoites == null ? "—" : dec(r.pontoEquilibrioNoites, 1) + " noites", n: r.ocupacaoEquilibrio == null ? "" : "ocupação de equilíbrio " + pct(r.ocupacaoEquilibrio) },
      { id: "margemOp", r: "Quanto sobrou, em % do faturamento", v: pct(r.margemOperacionalPct) },
      { id: "rnd", r: "Receita por noite disponível", v: brl(r.receitaPorNoiteDisponivel) },
      { id: "folego", r: "Meses de fôlego", v: r.mesesFolego == null ? "não calculável" : dec(r.mesesFolego, 1) + " meses", n: "saldo final " + brl(r.saldoFinal) + " + reservas " + brl(r.N.reservasSeparadas) },
    ];
  }

  var TELAS = ["abertura", "mes", "entrou", "variaveis", "fixos", "modelo", "caixa", "resultado"];
  var TITULOS = { mes: "O mês", entrou: "O que entrou", variaveis: "O que saiu com cada noite", fixos: "O que sai todo mês", modelo: "Custos do modelo, reserva e depreciação", caixa: "O caixa do mês" };
  var PROXIMO = { n: 3, t: "Preço, reservas e distribuição" };

  var api = { REF: REF, SITUACOES: SITUACOES, DIAG: DIAG, SIMNAO: SIMNAO, NIVEIS: NIVEIS, CAMPOS: CAMPOS, CAMPO: CAMPO, EXEMPLO: EXEMPLO, REGRAS: REGRAS, DENTRO: DENTRO, TELAS: TELAS, TITULOS: TITULOS, PROXIMO: PROXIMO,
    num: num, normalizar: normalizar, aplicarReferenciaDeducoes: aplicarReferenciaDeducoes, validar: validar, calcular: calcular, leituras: leituras, faixaDesconto: faixaDesconto,
    prioridades: prioridades, causaPrincipal: causaPrincipal, planoSugerido: planoSugerido, comoVerificar: comoVerificar, completo: completo, concluido: concluido, pendencias: pendencias, nivelSeparacao: nivelSeparacao,
    brl: brl, pct: pct, dec: dec, cascata: cascata, indicadores: indicadores };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else raiz.ZF = api;
})(typeof window !== "undefined" ? window : this);

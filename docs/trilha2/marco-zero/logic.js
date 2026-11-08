/* Jornada 2 · Gestão · Marco Zero · Diagnóstico de Gestão
   Lógica pura da ficha "Faça agora". Sem DOM: roda no navegador e no Node (testes).
   Regra: tudo que a ficha afirma sai daqui, para ser testado. */
(function (raiz) {
  "use strict";

  // Situações do membro (públicos A, B e C do comando 01)
  var SITUACOES = [
    { v: "abrir", r: "Ainda vou abrir a minha hospedagem", curto: "vai abrir" },
    { v: "dono", r: "Já opero e quero profissionalizar a gestão", curto: "dono que opera" },
    { v: "operador", r: "Cuido do dia a dia de uma hospedagem de outra pessoa", curto: "operador" },
  ];
  var TIPOS = ["Casa ou apartamento de temporada", "Cabanas ou chalés", "Glamping", "Pousada", "Hotel", "Outro"];
  var QUEM = [
    { v: "so", r: "Eu, sozinho" },
    { v: "dupla", r: "Eu e mais uma pessoa" },
    { v: "equipe", r: "Tenho gerente ou equipe que responde pela gestão" },
    { v: "fora", r: "Uma empresa ou administradora cuida para mim" },
  ];

  // As cinco perguntas do gestor: números do mês passado
  var CINCO = [
    { id: "entrou", r: "Quanto entrou", p: "A receita do mês passado, somando todos os canais." },
    { id: "sobrou", r: "Quanto sobrou", p: "O resultado do mês: o que entrou menos tudo o que saiu." },
    { id: "ocupacao", r: "A ocupação", p: "Quantas noites você vendeu, de quantas estavam disponíveis." },
    { id: "diaria", r: "A diária média", p: "A receita de hospedagem dividida pelas noites vendidas." },
    { id: "custo", r: "O custo por noite vendida", p: "Tudo o que saiu no mês dividido pelas noites vendidas." },
  ];
  var NIV5 = [{ v: 2, r: "Sei, com número" }, { v: 1, r: "Tenho uma ideia" }, { v: 0, r: "Não sei" }];

  // As oito áreas da gestão (a jornada inteira, uma por módulo)
  var AREAS = [
    { id: "metas", n: 1, r: "Planejamento e metas", p: "Sei onde quero chegar em 12 meses e tenho metas escritas", s: "Objetivo do ano, metas de ocupação, diária e resultado, revisadas a cada mês.",
      acao: "Escrever, em uma página, a meta de ocupação, de diária média e de resultado para os próximos 12 meses, e a data de revisão de cada mês.", verifica: "A página existe, tem três números e uma data de revisão por mês." },
    { id: "financas", n: 2, r: "Finanças e fluxo de caixa", p: "Sei o que entra e o que sai, e fecho o mês", s: "Registro de entradas e saídas, fechamento mensal, separação entre o dinheiro da hospedagem e o pessoal.",
      acao: "Fechar o mês passado em uma folha: tudo que entrou, tudo que saiu por categoria, e o que sobrou. Depois, separar a conta da hospedagem da conta pessoal.", verifica: "O fechamento do mês passado existe, com as saídas em categorias e o resultado no fim." },
    { id: "preco", n: 3, r: "Preço, reservas e distribuição", p: "Defino a diária com conta e controlo o calendário e os canais", s: "Diária mínima calculada, calendário de reservas em um lugar só, regras por canal, sem reserva duplicada.",
      acao: "Calcular a diária mínima que cobre os custos e as taxas, e colocar todas as reservas num único calendário.", verifica: "A diária mínima está escrita, com a conta ao lado, e o calendário único tem todas as reservas do mês." },
    { id: "vendas", n: 4, r: "Marketing e vendas", p: "Sei como o hóspede me encontra e por que escolhe a minha hospedagem", s: "De onde vêm as reservas, anúncio atualizado, resposta rápida, motivo de escolha claro.",
      acao: "Anotar, para as últimas 20 reservas, por onde cada hóspede chegou e o que ele disse que buscava.", verifica: "A lista das 20 reservas existe, com canal e motivo em cada linha." },
    { id: "pessoas", n: 5, r: "Pessoas", p: "Cada pessoa sabe o que faz, quando e como", s: "Quem faz o quê, escala, treinamento de entrada e padrão de cada tarefa, mesmo quando a equipe é você.",
      acao: "Listar todas as tarefas da semana e escrever ao lado quem faz cada uma, em que dia e em quanto tempo.", verifica: "A lista existe e nenhuma tarefa está sem nome ao lado." },
    { id: "compras", n: 6, r: "Compras, fornecedores e estoque", p: "Compro com planejamento e sei o que tenho em estoque", s: "Lista de fornecedores, compra por lista, estoque mínimo do que não pode faltar.",
      acao: "Fazer a lista do que não pode faltar, com a quantidade mínima de cada item e o fornecedor ao lado.", verifica: "A lista existe e tem quantidade mínima e fornecedor para cada item." },
    { id: "operacao", n: 7, r: "Limpeza, manutenção e padrão", p: "A unidade é entregue sempre do mesmo jeito e os problemas têm dono", s: "Checklist de limpeza e liberação, controle de enxoval, quadro de ocorrências e manutenção preventiva.",
      acao: "Escrever o checklist de limpeza e liberação da unidade e usar em todas as trocas de hóspede do mês.", verifica: "O checklist existe e foi preenchido em todas as trocas do mês." },
    { id: "qualidade", n: 8, r: "Qualidade, reputação e indicadores", p: "Olho os números e as avaliações toda semana e ajo sobre eles", s: "Painel com os cinco números do mês, leitura das avaliações, uma decisão por semana a partir deles.",
      acao: "Montar o painel do mês com os cinco números do gestor e marcar na agenda um horário fixo por semana para olhar os números e as avaliações.", verifica: "O painel do mês passado está preenchido e o horário semanal está na agenda." },
  ];
  var NIVA = [{ v: 2, r: "Funciona, com padrão e registro" }, { v: 1, r: "Funciona, mas só na minha cabeça" }, { v: 0, r: "Não existe ou não sei" }];

  var ROTINA = [
    { v: "dia", r: "Todo dia" }, { v: "semana", r: "Toda semana" }, { v: "mes", r: "Todo mês" }, { v: "as-vezes", r: "Quando dá" }, { v: "nunca", r: "Nunca olhei" },
  ];
  // A pergunta que liga lucro e saída da operação (Etapa 10 do Método Zion)
  var SAIDA = [
    { v: "sim-num", r: "Sim, e sei quanto" }, { v: "acho", r: "Acho que sim, mas nunca fiz a conta" }, { v: "nao", r: "Não sobraria nada" }, { v: "ns", r: "Não sei" },
  ];
  var TEMPO = [
    { v: "operacao", r: "Quase todo na operação: atender, limpar, resolver" },
    { v: "meio", r: "Metade na operação, metade na gestão" },
    { v: "gestao", r: "Quase todo na gestão: números, pessoas e decisões" },
  ];

  // Os módulos da Jornada 2 (um por área; o Marco Zero é a entrada)
  var MODULOS = [
    { n: 0, t: "Marco Zero · O gestor e o diagnóstico", area: null },
    { n: 1, t: "Planejamento, metas e indicadores", area: "metas" },
    { n: 2, t: "Finanças, fluxo de caixa e fechamento", area: "financas" },
    { n: 3, t: "Preço, reservas e distribuição", area: "preco" },
    { n: 4, t: "Marketing e vendas", area: "vendas" },
    { n: 5, t: "Pessoas e organização das áreas", area: "pessoas" },
    { n: 6, t: "Compras, estoque e manutenção", area: "compras" },
    { n: 7, t: "Qualidade, reputação e plano de crescimento", area: "qualidade" },
  ];
  // A área "operação" (limpeza, manutenção, padrão) é a ponte para a Jornada 3 · Operação
  var MODULO_DA_AREA = { metas: 1, financas: 2, preco: 3, vendas: 4, pessoas: 5, compras: 6, operacao: 6, qualidade: 7 };

  var FAIXAS = [
    { min: 0, max: 34, rot: "Gestão no improviso", leitura: "A hospedagem funciona porque você resolve tudo na hora. Isso cansa e não dá para medir. O primeiro passo não é fazer mais: é escrever o que já existe e começar a olhar os números do mês." },
    { min: 35, max: 64, rot: "Gestão em construção", leitura: "Boa parte já funciona, mas depende da sua memória. O que está na sua cabeça não dá para delegar nem para comparar com o mês passado. O passo agora é transformar o que funciona em padrão e registro." },
    { min: 65, max: 100, rot: "Gestão com método", leitura: "Você já gere com registro e com número. O que falta é fechar as áreas fracas e transformar o painel em decisão toda semana. Daqui, o caminho é o Plano de Gestão Profissional completo." },
  ];

  function completo(S) {
    S = S || {};
    var c = CINCO.every(function (q) { return S.cinco && S.cinco[q.id] != null; });
    var a = AREAS.every(function (q) { return S.areas && S.areas[q.id] != null; });
    return !!(S.situacao && c && a);
  }

  function calcular(S) {
    S = S || {}; var cinco = S.cinco || {}, areas = S.areas || {};
    var pCinco = 0, nsCinco = [];
    CINCO.forEach(function (q) { var v = cinco[q.id]; if (v == null) v = 0; pCinco += v; if (v === 0) nsCinco.push(q); });
    var pAreas = 0, zero = [], meio = [], ok = [];
    AREAS.forEach(function (a) { var v = areas[a.id]; if (v == null) v = 0; pAreas += v; (v === 0 ? zero : v === 1 ? meio : ok).push(a); });
    // 60% as áreas (0 a 16), 40% as cinco perguntas (0 a 10)
    var nota = Math.round((pAreas / 16) * 60 + (pCinco / 10) * 40);
    if (nota < 0) nota = 0; if (nota > 100) nota = 100;
    var faixa = FAIXAS.filter(function (f) { return nota >= f.min && nota <= f.max; })[0];
    // A área mais frágil: a primeira com 0; se não houver, a primeira com 1; se tudo 2, nenhuma
    var fragil = zero[0] || meio[0] || null;
    // Quando a fragilidade está só nos números (todas as áreas em 2, mas "Não sei" nas cinco), a área a atacar é a 8
    if (!fragil && nsCinco.length) fragil = AREAS[7];
    var modulo = fragil ? MODULO_DA_AREA[fragil.id] : 7;
    var inicio = MODULOS[modulo];
    return { nota: nota, faixa: faixa, pCinco: pCinco, pAreas: pAreas, nsCinco: nsCinco, zero: zero, meio: meio, ok: ok, fragil: fragil, inicio: inicio };
  }

  function textoFragil(r) {
    if (!r.fragil) return "Nenhuma área em branco. Confira se cada resposta tem registro por trás: o que não está escrito ainda está só na sua cabeça.";
    var nivel = r.zero.indexOf(r.fragil) >= 0 ? "você marcou que não existe ou não sabe" : (r.meio.indexOf(r.fragil) >= 0 ? "funciona, mas só na sua cabeça" : "é onde os números faltam");
    return "Área " + r.fragil.n + " · " + r.fragil.r + ": " + nivel + ". " + r.fragil.s;
  }

  function acaoSugerida(r) { return r.fragil ? r.fragil.acao : AREAS[7].acao; }
  function comoVerificar(r) { return r.fragil ? r.fragil.verifica : AREAS[7].verifica; }

  function leituraTempo(S) {
    if (!S || !S.tempo) return "";
    if (S.tempo === "operacao") return "Hoje o seu tempo vai quase todo para a operação. Gestão precisa de hora marcada: sem ela, os números nunca são olhados.";
    if (S.tempo === "meio") return "Você já divide o tempo entre operar e gerir. A próxima virada é fazer a gestão caber num horário fixo da semana.";
    return "Você já passa a maior parte do tempo na gestão. O desafio agora é que cada hora de gestão vire decisão com número.";
  }
  function leituraSaida(S) {
    if (!S || !S.saida) return "";
    return { "sim-num": "Você já fez a conta da sua própria retirada: é o sinal de que a hospedagem é um negócio, e não um emprego que você criou para si.",
      acho: "Achar que sobraria não é saber. Essa conta, a do que sobra depois de pagar alguém para fazer o que você faz, é a que separa renda de emprego próprio. O módulo 2 a faz com você.",
      nao: "Se não sobraria nada, hoje a hospedagem paga o seu trabalho, não o seu negócio. Não é um veredito: é o ponto de partida para rever preço, custo e quem faz o quê.",
      ns: "Essa é a pergunta que a jornada vai responder com número: se você contratasse alguém para fazer o que faz e saísse da operação, sobraria alguma coisa?" }[S.saida] || "";
  }
  function leituraRotina(S) {
    if (!S || !S.rotina) return "";
    return { dia: "Você olha os números todo dia: ótimo, desde que exista um painel com os mesmos cinco números todo mês.",
      semana: "Olhar os números toda semana é a frequência certa para uma hospedagem pequena.",
      mes: "Uma vez por mês é o mínimo. Com um painel simples, dá para passar a olhar toda semana.",
      "as-vezes": "Olhar os números quando dá é o mesmo que não olhar: a decisão chega tarde.",
      nunca: "Você nunca olhou os números. Não há culpa nisso: ninguém ensinou. É por aqui que a jornada começa." }[S.rotina] || "";
  }

  // Critério objetivo de conclusão do Marco Zero
  function concluido(S) {
    return completo(S) && !!(S.acao && String(S.acao).trim().length >= 10) && !!S.prazo;
  }

  var api = { SITUACOES: SITUACOES, TIPOS: TIPOS, QUEM: QUEM, CINCO: CINCO, NIV5: NIV5, AREAS: AREAS, NIVA: NIVA, ROTINA: ROTINA, SAIDA: SAIDA, TEMPO: TEMPO, MODULOS: MODULOS, MODULO_DA_AREA: MODULO_DA_AREA, FAIXAS: FAIXAS,
    completo: completo, calcular: calcular, textoFragil: textoFragil, acaoSugerida: acaoSugerida, comoVerificar: comoVerificar, leituraTempo: leituraTempo, leituraSaida: leituraSaida, leituraRotina: leituraRotina, concluido: concluido };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else raiz.ZG = api;
})(typeof window !== "undefined" ? window : this);

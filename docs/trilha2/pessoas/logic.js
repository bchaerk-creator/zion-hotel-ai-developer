/* Jornada 2 · Gestão · Módulo 5 · Pessoas e organização das áreas
   Lógica pura da ficha "O meu Mapa de Pessoas e Alçadas". Sem DOM: roda no navegador (window.ZP) e no Node (testes).
   Regra: tudo o que a ficha afirma sai daqui, para ser testado. Nenhuma nota: só contagens e as réguas da fonte.
   Fontes: Panorama (Trilha B, G7: alçadas e governança); Jornada do COMO, Etapa 10 (P01 a P11);
   Bíblia Operacional Zion (seis setores, onboarding em seis etapas, rotina do gestor). Mapa de fontes fora do repositório. */
(function (raiz) {
  "use strict";

  var SITUACOES = [
    { v: "abrir", r: "Ainda vou abrir: quero desenhar quem faz o quê antes do primeiro hóspede", curto: "vai abrir" },
    { v: "dono", r: "Já opero a minha hospedagem e quase tudo passa por mim", curto: "dono que opera" },
    { v: "operador", r: "Cuido da hospedagem de outra pessoa e quero combinar alçadas com o dono", curto: "operador" },
  ];
  var SETE_DIAS = [
    { v: "nunca", r: "Nunca, desde que abri" },
    { v: "mais12", r: "Faz mais de 12 meses" },
    { v: "menos12", r: "Nos últimos 12 meses" },
  ];

  // Seis setores (Bíblia Operacional Zion: um manual por setor)
  var SETORES = [
    { id: "hosp", r: "Hospitalidade e experiência" },
    { id: "gov", r: "Governança e limpeza" },
    { id: "man", r: "Manutenção" },
    { id: "ger", r: "Gerencial e administrativo" },
    { id: "com", r: "Comercial e reservas" },
    { id: "cul", r: "Cultura e marca" },
  ];

  // Oito atividades (Etapa 10, P08, lista do Passo 07 da Etapa 09, + manutenção e avaliações), com o julgamento sugerido
  // julgamento: baixo (segue roteiro), medio (parcial, com modelos), alto (exige decisão: fica com o dono por mais tempo)
  var ATIVIDADES = [
    { id: "limpeza", r: "Limpeza e preparação da unidade", setor: "gov", julg: "baixo", ex: { resp: "Diarista", horas: 0 } },
    { id: "checkin", r: "Check-in e check-out", setor: "hosp", julg: "baixo", ex: { resp: "Eu", horas: 5 } },
    { id: "mensagens", r: "Resposta a mensagem dos hóspedes", setor: "hosp", julg: "medio", ex: { resp: "Eu", horas: 6 } },
    { id: "manutencao", r: "Manutenção e ronda técnica", setor: "man", julg: "medio", ex: { resp: "Auxiliar de manutenção", horas: 1 } },
    { id: "compras", r: "Compras, estoque e fornecedores", setor: "ger", julg: "alto", ex: { resp: "Eu", horas: 2 } },
    { id: "financeiro", r: "Financeiro e administrativo", setor: "ger", julg: "alto", ex: { resp: "Eu", horas: 2 } },
    { id: "preco", r: "Preço, calendário e canais", setor: "com", julg: "alto", ex: { resp: "Eu", horas: 2 } },
    { id: "avaliacoes", r: "Pedido e resposta de avaliações", setor: "cul", julg: "medio", ex: { resp: "Eu", horas: 2 } },
  ];
  var JULG = [
    { v: "baixo", r: "Segue roteiro", curto: "Baixo", entra: "Sim" },
    { v: "medio", r: "Parcial, com modelos", curto: "Médio", entra: "Parcial, com modelos" },
    { v: "alto", r: "Exige decisão", curto: "Alto", entra: "Não, fica com você por mais tempo" },
  ];

  // Quatro dependências (Etapa 10, P02 · Mapa das Quatro Dependências™)
  var DEPENDENCIAS = [
    { id: "decisao", r: "Decisão", frase: "Tudo fora do padrão me procura", resolve: "critério escrito e alçada definida", prazo: "duas semanas", passo: "a tela de alçadas desta ficha" },
    { id: "acesso", r: "Acesso", frase: "Está tudo no meu nome e no meu celular", resolve: "cofre de senhas compartilhado, acessos nominais por pessoa e um telefone da operação separado do pessoal", prazo: "uma tarde", passo: "esta semana" },
    { id: "conhecimento", r: "Conhecimento", frase: "Só eu sei como se faz", resolve: "procedimento escrito, de uma página, nos seis blocos", prazo: "seis a dez semanas para o manual mínimo", passo: "o procedimento da atividade que você vai delegar" },
    { id: "relacao", r: "Relação", frase: "Fornecedores e parceiros só falam comigo", resolve: "apresentar a pessoa e fazer a transição visível para o outro lado", prazo: "seis meses a dois anos", passo: "levar a pessoa às próximas conversas com fornecedores" },
  ];
  var FORCA = [{ v: "fraca", r: "Fraca", n: 1 }, { v: "media", r: "Média", n: 2 }, { v: "forte", r: "Forte", n: 3 }];

  // Tabela de Critérios™ (Etapa 10, P06): as sete situações que toda hospedagem precisa ter
  var SITUACOES_CRITERIO = [
    { id: "ultimaHora", r: "Reserva de última hora", dica: "Até quanto tempo antes aceitar, e com que condição.", ex: { quem: "Quem estiver no plantão", regra: "Aceita até 2 horas antes do check-in, se a unidade estiver pronta e houver alguém para receber.", alcada: "" } },
    { id: "cortesia", r: "Cortesia e compensação", dica: "Em que situação oferecer, até que valor, sem consultar.", ex: { quem: "Diarista", regra: "Problema reconhecido na unidade: oferece cortesia de até 15% da diária.", alcada: "42" } },
    { id: "cancelamento", r: "Cancelamento e reembolso fora da política", dica: "Quando flexibilizar, até quanto.", ex: { quem: "Eu", regra: "Motivo de saúde com comprovação: devolve até 50%. Qualquer outro motivo: consulta a dona.", alcada: "" } },
    { id: "manutencao", r: "Manutenção", dica: "O que resolver na hora, o que agendar, o que é emergência que para a unidade.", ex: { quem: "Auxiliar de manutenção", regra: "Resolve na hora o que não para a unidade. O que para a unidade: avisa a dona na hora.", alcada: "100" } },
    { id: "compra", r: "Compra fora do previsto", dica: "Até que valor a equipe compra sem perguntar.", ex: { quem: "Diarista", regra: "Item de reposição da lista padrão compra sem perguntar. Fora da lista: consulta.", alcada: "100" } },
    { id: "hospede", r: "Hóspede com comportamento problemático", dica: "O que tolerar, quando advertir, quando encerrar a estadia.", ex: { quem: "Quem estiver no plantão", regra: "Faz a advertência verbal e registra. Encerrar a estadia, só com a dona.", alcada: "" } },
    { id: "calendario", r: "Erro de calendário e realocação", dica: "Realocar ou compensar, e com que limite de gasto.", ex: { quem: "Eu", regra: "", alcada: "" } },
  ];

  // Níveis de presença (Etapa 10, P10 · Painel de Acompanhamento™)
  var NIVEIS = [
    { n: 1, r: "Operando", t: "Você faz. Nenhuma delegação: é o ponto de partida e é onde a maior parte das hospedagens pequenas está." },
    { n: 2, r: "Supervisionando tudo", t: "Você confere cada item. Parece delegação e não é: a execução saiu, a aprovação ficou. É aqui que a maioria para e conclui que delegar não funciona." },
    { n: 3, r: "Acompanhando por exceção", t: "Você olha indicadores. Relatório semanal, conversa mensal, contato só nas quatro exceções definidas. É o nível que permite sair." },
    { n: 4, r: "Dirigindo", t: "Você decide o rumo. Olha resultado, preço, expansão e marca. A operação roda e você trabalha sobre ela, não dentro dela." },
  ];
  var INDICADORES = [
    "Nota das avaliações da semana, e qualquer avaliação abaixo do padrão",
    "Ocupação da semana contra a projeção",
    "Tempo médio de resposta a mensagem",
    "Ocorrências registradas: problema durante a estadia, reclamação, manutenção acionada",
    "Decisões tomadas dentro da alçada, listadas",
    "Gasto da semana contra o previsto",
  ];
  var DIAS_SEMANA = [
    { v: "segunda", r: "Segunda-feira" }, { v: "terca", r: "Terça-feira" }, { v: "quarta", r: "Quarta-feira" }, { v: "quinta", r: "Quinta-feira" },
    { v: "sexta", r: "Sexta-feira" }, { v: "sabado", r: "Sábado" }, { v: "domingo", r: "Domingo" },
  ];
  var FORMATOS = [
    { v: "diarista", r: "Diarista por estadia", t: "Paga por tarefa feita, custo totalmente variável. Boa para operação sazonal e pequena. É quase sempre o primeiro formato." },
    { v: "meio", r: "Meio período fixo", t: "Cobre limpeza, preparação e parte do atendimento. Faz sentido a partir de quatro a seis unidades." },
    { v: "integral", r: "Integral", t: "Só quando a operação sustenta, e normalmente já com a segunda unidade no horizonte." },
  ];
  var SIMNAO = [{ v: "sim", r: "Sim" }, { v: "nao", r: "Ainda não" }];
  var EQUILIBRIO = [{ v: "nao", r: "Não passa de 70%" }, { v: "sim", r: "Passa de 70%" }, { v: "naosei", r: "Não sei" }];

  // Plano de Quatro Semanas™ (Etapa 10, P09)
  var SEMANAS = [
    { n: 1, r: "Sombra", faz: "A pessoa acompanha você executando, com o procedimento impresso na mão, e marca o que não estava escrito. Nenhuma execução sozinha.", conversa: "20 minutos no fim da semana", sinal: "Procedimento corrigido com o que faltava" },
    { n: 2, r: "Execução acompanhada", faz: "A pessoa executa e você observa sem interferir. Corrija depois, não durante. Confira o resultado contra a foto do padrão, todo dia.", conversa: "20 minutos por dia", sinal: "O resultado bate com a foto do padrão" },
    { n: 3, r: "Sozinha, com conferência", faz: "A pessoa executa sozinha e você confere o resultado, não o processo. Entram a tabela de critérios e a alçada inicial.", conversa: "20 minutos por dia", sinal: "Dúvidas caindo, critérios sendo usados" },
    { n: 4, r: "Autonomia com alçada", faz: "A pessoa executa e decide dentro da alçada. Você olha os seis indicadores do painel.", conversa: "Duas vezes na semana", sinal: "Padrão mantido e decisões razoáveis" },
  ];
  var AVALIACAO = ["O padrão está sendo mantido?", "As decisões dentro da alçada foram razoáveis?", "As dúvidas diminuíram?"];

  // Onboarding em seis etapas (Bíblia Operacional Zion), adaptado a qualquer hospedagem
  var ONBOARDING = [
    "Visita guiada pelas unidades (10 minutos)",
    "A cultura e o padrão da casa (20 minutos)",
    "O vídeo ou a demonstração da função (30 a 60 minutos)",
    "A leitura do procedimento da função (40 minutos)",
    "A primeira execução acompanhada",
    "A confirmação do padrão, com você (5 minutos)",
  ];

  var TELAS = ["abertura", "cabeca", "mapa", "alcadas", "painel", "plano", "resultado"];
  var TITULOS = { cabeca: "O que só você sabe", mapa: "Quem faz o quê", alcadas: "Até quanto cada um decide", painel: "Como acompanhar de fora", plano: "As quatro semanas" };
  var PROXIMO = { n: 6, t: "Compras, estoque e manutenção" };

  // Exemplo didático · dados fictícios (Cabanas do Vale, 4 unidades, a dona opera; continuação dos módulos 0 e 2)
  function exemplo() {
    var ativ = {}, crit = {};
    ATIVIDADES.forEach(function (a) { ativ[a.id] = { resp: a.ex.resp, horas: String(a.ex.horas), julg: a.julg }; });
    SITUACOES_CRITERIO.forEach(function (s) { crit[s.id] = { quem: s.ex.quem, regra: s.ex.regra, alcada: s.ex.alcada }; });
    return {
      situacao: "dono", hospedagem: "Cabanas do Vale (exemplo)", unidades: "4", equipeHoje: "2", feriasDias: "0", seteDias: "nunca",
      dep: { conhecimento: "media", decisao: "forte", relacao: "media", acesso: "forte" }, acessoData: "2026-11-14",
      invTotal: "52", invSimples: "18", invDecisao: "14", invAcesso: "9",
      ativ: ativ, crit: crit, alcadaInicial: "100", alcada2mes: "300",
      notaMin: "4,7", gastoPct: "10", diaSemanal: "segunda", conversaMensal: "Primeira segunda-feira do mês, 40 minutos, com a Folha Única", nivel: "1", quemEnvia: "Diarista, por mensagem, toda segunda de manhã",
      ativPlano: "checkin", pessoa: "Diarista, que já faz a limpeza", formato: "diarista", inicio: "2026-11-16", cobertura: "Eu (dona), nas folgas da diarista",
      preAcesso: "nao", preProc: "nao", preCrit: "sim", custoMes: "500", equilibrio: "nao",
      tempoLivre: "Duas horas por semana para preço e venda direta (módulos 3 e 4).",
    };
  }
  var EXEMPLO = exemplo();

  // ---------- utilidades ----------
  function num(v) {
    if (v == null) return null;
    if (typeof v === "number") return isFinite(v) ? v : null;
    var s = String(v).trim(); if (!s) return null;
    s = s.replace(/\s|R\$|%|h/gi, "");
    if (/,/.test(s)) s = s.replace(/\./g, "").replace(",", ".");
    var n = Number(s); return isFinite(n) ? n : null;
  }
  function informado(v) { return v != null && String(v).trim() !== ""; }
  function letras(s) { return String(s || "").replace(/[^A-Za-zÀ-ÿ]/g, "").length; }
  function ehDono(resp) { var s = String(resp || "").trim().toLowerCase(); return s === "eu" || s === "eu mesma" || s === "eu mesmo"; }
  function brl(v) { if (v == null || !isFinite(v)) return "a definir"; var neg = v < 0; var s = Math.abs(v).toFixed(2).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, "."); return (neg ? "−R$ " : "R$ ") + s; }
  function pct(v, d) { if (v == null || !isFinite(v)) return "a definir"; return (v * 100).toFixed(d == null ? 1 : d).replace(".", ",") + "%"; }
  function dec(v, d) { if (v == null || !isFinite(v)) return "a definir"; return v.toFixed(d == null ? 1 : d).replace(".", ","); }
  function horasTxt(h) { var n = Math.round(h * 10) / 10; return dec(n, n % 1 ? 1 : 0).replace(/,0$/, "") + (n === 1 ? " hora" : " horas"); }
  // Datas sem fuso: "AAAA-MM-DD" ↔ dias
  function diaUTC(iso) { var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso || "")); if (!m) return null; var t = Date.UTC(+m[1], +m[2] - 1, +m[3]); var d = new Date(t); return d.getUTCMonth() === +m[2] - 1 ? t : null; }
  function somaDias(iso, n) { var t = diaUTC(iso); if (t == null) return null; return new Date(t + n * 864e5).toISOString().slice(0, 10); }
  function br(iso) { if (!iso) return "sem data"; var p = String(iso).split("-"); return p.length === 3 ? p[2] + "/" + p[1] + "/" + p[0] : "sem data"; }
  function brCurto(iso) { if (!iso) return "sem data"; var p = String(iso).split("-"); return p.length === 3 ? p[2] + "/" + p[1] : "sem data"; }

  function base() {
    var ativ = {}, crit = {};
    ATIVIDADES.forEach(function (a) { ativ[a.id] = { resp: "", horas: "", julg: a.julg }; });
    SITUACOES_CRITERIO.forEach(function (s) { crit[s.id] = { quem: "", regra: "", alcada: "" }; });
    return { tela: 0, nome: "", email: "", hospedagem: "", situacao: "", unidades: "", equipeHoje: "", feriasDias: "", seteDias: "", dep: {}, acessoData: "",
      invTotal: "", invSimples: "", invDecisao: "", invAcesso: "", ativ: ativ, crit: crit, alcadaInicial: "", alcada2mes: "",
      notaMin: "", gastoPct: "", diaSemanal: "", conversaMensal: "", nivel: "", quemEnvia: "",
      ativPlano: "", pessoa: "", formato: "", inicio: "", cobertura: "", preAcesso: "", preProc: "", preCrit: "", custoMes: "", equilibrio: "", tempoLivre: "" };
  }
  // Garante a estrutura completa (estado antigo ou parcial)
  function completar(S) {
    var b = base(); S = S || {};
    var out = {}; Object.keys(b).forEach(function (k) { out[k] = S[k] != null ? S[k] : b[k]; });
    Object.keys(S).forEach(function (k) { if (!(k in out)) out[k] = S[k]; });
    out.dep = Object.assign({}, S.dep || {});
    out.ativ = {}; ATIVIDADES.forEach(function (a) { out.ativ[a.id] = Object.assign({}, b.ativ[a.id], (S.ativ || {})[a.id] || {}); });
    out.crit = {}; SITUACOES_CRITERIO.forEach(function (s) { out.crit[s.id] = Object.assign({}, b.crit[s.id], (S.crit || {})[s.id] || {}); });
    return out;
  }

  // ---------- validação por tela ----------
  function validar(S, tela) {
    S = completar(S); var erros = [], avisos = [];
    var neg = function (v, r) { var n = num(v); if (informado(v) && n == null) erros.push(r + ": use só números."); else if (n != null && n < 0) erros.push(r + ": não pode ser negativo."); return n; };
    if (tela === "abertura") {
      if (!S.situacao) erros.push("Escolha a frase que mais parece com você.");
      var u = neg(S.unidades, "Unidades"); if (u != null && (u < 1 || u % 1)) erros.push("Unidades: um número inteiro, 1 ou mais.");
      if (!informado(S.unidades)) erros.push("Informe quantas unidades a hospedagem tem (ou terá).");
      neg(S.feriasDias, "Dias de férias");
      if (!S.seteDias) erros.push("Responda quando foi a última vez que você ficou 7 dias sem atender mensagem.");
    }
    if (tela === "cabeca") {
      DEPENDENCIAS.forEach(function (d) { if (!S.dep[d.id]) erros.push("Marque a força da dependência de " + d.r.toLowerCase() + "."); });
      var t = neg(S.invTotal, "Total de linhas"), s1 = neg(S.invSimples, "Diárias e simples"), s2 = neg(S.invDecisao, "Decisões sem critério"), s3 = neg(S.invAcesso, "Acessos e contatos");
      if (t != null && (s1 || 0) + (s2 || 0) + (s3 || 0) > t) erros.push("As três classes somadas passam do total de linhas do inventário.");
      if (!informado(S.invTotal) && (informado(S.invSimples) || informado(S.invDecisao) || informado(S.invAcesso))) erros.push("Informe o total de linhas do inventário.");
      if (S.dep.acesso && S.dep.acesso !== "fraca" && !S.acessoData) avisos.push("A dependência de acesso não é fraca: marque a tarde desta semana em que você resolve. A fonte manda resolver esta primeiro, seja qual for a mais forte.");
      if (S.acessoData && diaUTC(S.acessoData) == null) erros.push("Data do acesso inválida.");
    }
    if (tela === "mapa") {
      var tot = 0;
      ATIVIDADES.forEach(function (a) {
        var x = S.ativ[a.id];
        if (!String(x.resp || "").trim()) erros.push(a.r + ": diga quem faz hoje (escreva Eu se for você).");
        var h = neg(x.horas, a.r + " (horas)"); if (h != null && h > 100) erros.push(a.r + ": mais de 100 horas por semana não cabe numa semana de trabalho.");
        if (h != null) tot += h;
        if (!x.julg) erros.push(a.r + ": marque o julgamento que a atividade exige.");
      });
      if (tot > 80) avisos.push("Você soma " + horasTxt(tot) + " por semana na hospedagem. Confira se não contou a mesma hora em duas atividades.");
    }
    if (tela === "alcadas") {
      SITUACOES_CRITERIO.forEach(function (s) { neg(S.crit[s.id].alcada, s.r + " (alçada)"); });
      var ai = neg(S.alcadaInicial, "Alçada inicial"), a2 = neg(S.alcada2mes, "Alçada do segundo mês");
      if (!informado(S.alcadaInicial) || ai === 0) erros.push("Defina a alçada inicial em reais, maior que zero: toda decisão precisa de um valor até o qual a pessoa decide sozinha.");
      if (ai != null && a2 != null && a2 < ai) avisos.push("A alçada do segundo mês está abaixo da inicial. A fonte sobe a alçada conforme a confiança, não desce.");
      var ruins = SITUACOES_CRITERIO.filter(function (s) { var r = S.crit[s.id].regra; return informado(r) && letras(r) < 10; });
      if (ruins.length) avisos.push("Regra curta demais em: " + ruins.map(function (s) { return s.r; }).join(", ") + ". Escreva quando é sim, quando é não e quando consulta.");
    }
    if (tela === "painel") {
      var nm = neg(S.notaMin, "Nota mínima"); if (!informado(S.notaMin)) erros.push("Defina a nota mínima das avaliações: abaixo dela, você é acionado na hora.");
      if (nm != null && nm > 10) erros.push("Nota mínima: use a escala da sua plataforma (até 5 ou até 10).");
      var gp = neg(S.gastoPct, "Percentual do gasto"); if (!informado(S.gastoPct)) erros.push("Defina o percentual de gasto acima do previsto que aciona você.");
      if (gp != null && gp > 100) erros.push("Percentual do gasto: use de 0 a 100.");
      if (!S.diaSemanal) erros.push("Escolha o dia da leitura semanal.");
      if (!S.nivel) erros.push("Marque em que nível de presença você está hoje.");
    }
    if (tela === "plano") {
      if (!S.ativPlano) erros.push("Escolha a atividade que entra no plano.");
      if (!String(S.pessoa || "").trim()) erros.push("Diga quem vai assumir (nome ou função; se ainda vai contratar, escreva \"a contratar\").");
      if (!S.formato) erros.push("Escolha o formato.");
      if (!S.inicio) erros.push("Marque a data de início da semana 1.");
      else if (diaUTC(S.inicio) == null) erros.push("Data de início inválida.");
      if (!String(S.cobertura || "").trim()) erros.push("Defina quem substitui se a pessoa faltar.");
      neg(S.custoMes, "Custo a mais por mês");
      var u2 = num(S.unidades);
      if (S.formato === "meio" && u2 != null && u2 < 4) avisos.push("A fonte indica meio período a partir de quatro a seis unidades. Com " + u2 + ", confira se diarista por estadia não resolve.");
      if (S.formato === "integral" && u2 != null && u2 < 6) avisos.push("A fonte indica integral só quando a operação sustenta, normalmente com a segunda unidade no horizonte.");
    }
    return { ok: erros.length === 0, erros: erros, avisos: avisos };
  }

  // ---------- cálculo ----------
  // fin (opcional): números da Folha Única do Módulo 2 { fixoTotalMes, margemOutras, margemPorNoite, noitesDisponiveis, ocupacaoEquilibrio }
  function calcular(S, fin) {
    S = completar(S);
    var r = { horasTotal: 0, horasPorJulg: { baixo: 0, medio: 0, alto: 0 }, atividades: [], soDono: [], setores: [] };
    ATIVIDADES.forEach(function (a, i) {
      var x = S.ativ[a.id], h = num(x.horas) || 0;
      var item = { id: a.id, r: a.r, setor: a.setor, i: i, resp: String(x.resp || "").trim(), horas: h, julg: x.julg || a.julg, dono: ehDono(x.resp) };
      item.entra = (JULG.filter(function (j) { return j.v === item.julg; })[0] || JULG[2]).entra;
      r.atividades.push(item); r.horasTotal += h; r.horasPorJulg[item.julg] += h;
      if (item.dono) r.soDono.push(item);
    });
    // Primeira contratação: mais horas e menos julgamento (baixo antes de médio; alto nunca); empate: a primeira da lista
    var cand = r.atividades.filter(function (a) { return a.horas > 0 && a.julg !== "alto"; }).sort(function (a, b) {
      var ka = (a.julg === "baixo" ? 1000 : 0) + a.horas, kb = (b.julg === "baixo" ? 1000 : 0) + b.horas; return kb - ka || a.i - b.i; });
    r.primeira = cand[0] || null; r.segunda = cand[1] || null;
    SETORES.forEach(function (s) {
      var at = r.atividades.filter(function (a) { return a.setor === s.id; });
      var resp = []; at.forEach(function (a) { if (a.resp && resp.indexOf(a.resp) < 0) resp.push(a.resp); });
      r.setores.push({ id: s.id, r: s.r, atividades: at, responsaveis: resp, horas: at.reduce(function (t, a) { return t + a.horas; }, 0), soDono: at.length > 0 && at.every(function (a) { return a.dono; }) });
    });
    r.setoresSoDono = r.setores.filter(function (s) { return s.soDono; });
    // Dependências: a mais forte (empate na ordem: decisão, acesso, conhecimento, relação)
    var mx = 0; DEPENDENCIAS.forEach(function (d) { var f = FORCA.filter(function (x) { return x.v === S.dep[d.id]; })[0]; if (f && f.n > mx) mx = f.n; });
    r.depMaisForte = mx ? DEPENDENCIAS.filter(function (d) { var f = FORCA.filter(function (x) { return x.v === S.dep[d.id]; })[0]; return f && f.n === mx; })[0] : null;
    r.depForca = mx;
    // Inventário da Cabeça™
    var it = num(S.invTotal), is = num(S.invSimples) || 0, id = num(S.invDecisao) || 0, ia = num(S.invAcesso) || 0;
    r.inventario = it ? { total: it, simples: is, decisao: id, acesso: ia, rapidas: is + id + ia, parteRapida: (is + id + ia) / it, parteDecisao: id / it } : null;
    // Critérios e alçadas
    r.criterios = SITUACOES_CRITERIO.map(function (s) { var c = S.crit[s.id]; return { id: s.id, r: s.r, quem: String(c.quem || "").trim(), regra: String(c.regra || "").trim(), alcada: num(c.alcada), escrito: letras(c.regra) >= 10 }; });
    r.criteriosEscritos = r.criterios.filter(function (c) { return c.escrito; }).length;
    r.alcadaInicial = num(S.alcadaInicial); r.alcada2mes = num(S.alcada2mes);
    r.alcadasPorPessoa = {};
    r.criterios.forEach(function (c) { if (c.quem && c.alcada != null && c.alcada > 0) { var k = c.quem; r.alcadasPorPessoa[k] = Math.max(r.alcadasPorPessoa[k] || 0, c.alcada); } });
    // Painel
    r.notaMin = num(S.notaMin); r.gastoPct = num(S.gastoPct);
    r.nivel = NIVEIS.filter(function (n) { return String(n.n) === String(S.nivel); })[0] || null;
    r.excecoes = [
      "Avaliação abaixo da nota mínima" + (r.notaMin != null ? " (" + dec(r.notaMin, 1) + ")" : ""),
      "Decisão fora da alçada que precisou ser tomada" + (r.alcadaInicial ? " (acima de " + brl(r.alcadaInicial) + " na largada)" : ""),
      "Ocorrência de segurança ou dano",
      "Gasto acima do previsto" + (r.gastoPct != null ? " em mais de " + dec(r.gastoPct, 0) + "%" : ""),
    ];
    // Plano de quatro semanas
    r.ativPlano = r.atividades.filter(function (a) { return a.id === S.ativPlano; })[0] || null;
    r.semanas = SEMANAS.map(function (s, k) { return { n: s.n, r: s.r, faz: s.faz, conversa: s.conversa, sinal: s.sinal, de: somaDias(S.inicio, 7 * k), ate: somaDias(S.inicio, 7 * k + 6) }; });
    r.avaliacao = somaDias(S.inicio, 27);
    r.horasLiberadas = r.ativPlano ? r.ativPlano.horas : 0;
    r.parteLiberada = r.horasTotal > 0 ? r.horasLiberadas / r.horasTotal : null;
    r.formato = FORMATOS.filter(function (f) { return f.v === S.formato; })[0] || null;
    r.custoMes = num(S.custoMes);
    // Teste de viabilidade (Etapa 10, P08): o ponto de equilíbrio com o custo a mais passa de 70%?
    r.equilibrio = null;
    if (fin && fin.margemPorNoite > 0 && fin.noitesDisponiveis > 0 && r.custoMes != null) {
      var pe = Math.max(0, (fin.fixoTotalMes + r.custoMes - (fin.margemOutras || 0)) / fin.margemPorNoite);
      r.equilibrio = { calculado: true, antes: fin.ocupacaoEquilibrio, depois: pe / fin.noitesDisponiveis, noites: pe };
      r.equilibrio.k = r.equilibrio.depois > 0.7 ? "sim" : "nao";
    } else if (S.equilibrio) r.equilibrio = { calculado: false, k: S.equilibrio };
    r.preReq = [
      { id: "preAcesso", r: "Acessos resolvidos: cofre de senhas, acessos nominais e telefone da operação", ok: S.preAcesso === "sim" },
      { id: "preProc", r: "Procedimento da atividade escrito nos seis blocos e testado por quem não sabe", ok: S.preProc === "sim" },
      { id: "preCrit", r: "Tabela de critérios impressa e entregue a quem opera", ok: S.preCrit === "sim" },
    ];
    // Prontidão do mapa: itens prontos (contagem, não nota)
    var acessoOk = S.dep.acesso === "fraca" || (!!S.dep.acesso && diaUTC(S.acessoData) != null);
    r.itens = [
      { id: "acesso", r: "Dependência de acesso resolvida ou com data marcada", ok: acessoOk },
      { id: "mapa", r: "Quem faz o quê: as oito atividades com responsável", ok: r.atividades.every(function (a) { return !!a.resp; }) },
      { id: "criterios", r: "Pelo menos cinco das sete situações com regra escrita", ok: r.criteriosEscritos >= 5 },
      { id: "alcada", r: "Alçada inicial em reais", ok: r.alcadaInicial != null && r.alcadaInicial > 0 },
      { id: "painel", r: "Painel por exceção: nota mínima, percentual do gasto e dia da leitura semanal", ok: r.notaMin != null && r.gastoPct != null && !!S.diaSemanal },
      { id: "pessoa", r: "Atividade, pessoa e cobertura de falta definidas", ok: !!r.ativPlano && !!String(S.pessoa || "").trim() && !!String(S.cobertura || "").trim() },
      { id: "inicio", r: "Data de início da semana 1 marcada", ok: diaUTC(S.inicio) != null },
    ];
    r.prontos = r.itens.filter(function (i) { return i.ok; }).length;
    return r;
  }

  // ---------- leituras (texto da ficha e do PDF) ----------
  function leituras(r, S) {
    S = completar(S); var L = {};
    L.nivel = r.nivel ? "Nível " + r.nivel.n + " de 4 · " + r.nivel.r + ". " + r.nivel.t : "Nível de presença não informado.";
    L.dependencia = r.depMaisForte ? "A dependência mais forte hoje é a de " + r.depMaisForte.r.toLowerCase() + " (\"" + r.depMaisForte.frase + "\"). Resolve com " + r.depMaisForte.resolve + ". Prazo da fonte: " + r.depMaisForte.prazo + "."
      : "Marque a força das quatro dependências.";
    if (r.depMaisForte && r.depMaisForte.id === "decisao") L.dependencia += " É a mais incapacitante, porque persegue você mesmo de férias.";
    if (r.inventario) {
      L.inventario = "O seu inventário tem " + r.inventario.total + " linhas. Diárias e simples, decisões sem critério e acessos somam " + r.inventario.rapidas + " (" + pct(r.inventario.parteRapida, 0) + "): " +
        (r.inventario.parteRapida > 0.7 ? "como a fonte prevê, a maior parte se resolve rápido, com procedimento curto, critério escrito ou cofre de senhas." : "a parte que exige treino longo é maior do que a fonte costuma ver. Comece pelo que é diário e de alto risco.");
    } else L.inventario = "Você ainda não fez o Inventário da Cabeça. Anote durante uma semana tudo o que só você sabe: costuma dar de 40 a 80 linhas.";
    L.horas = r.horasTotal > 0 ? horasTxt(r.horasTotal) + " por semana passam por você: " + horasTxt(r.horasPorJulg.baixo) + " seguem roteiro, " + horasTxt(r.horasPorJulg.medio) + " saem com modelos prontos e " + horasTxt(r.horasPorJulg.alto) + " exigem decisão e ficam com você por mais tempo."
      : "Nenhuma hora sua informada nas oito atividades.";
    L.primeira = r.primeira ? "Primeira a delegar: " + r.primeira.r.toLowerCase() + " (" + horasTxt(r.primeira.horas) + " por semana, " + (r.primeira.julg === "baixo" ? "segue roteiro" : "parcial, com modelos") + "). A regra da fonte: a atividade com mais horas e menos julgamento, não a mais pesada." +
      (r.segunda ? " Depois: " + r.segunda.r.toLowerCase() + "." : "")
      : "Nenhuma atividade sua de baixo ou médio julgamento tem horas. Comece pelos critérios e alçadas: é a dependência de decisão que prende.";
    L.setores = r.setoresSoDono.length + " dos 6 setores dependem só de você" + (r.setoresSoDono.length ? ": " + r.setoresSoDono.map(function (s) { return s.r.toLowerCase(); }).join(", ") + "." : ".");
    L.criterios = r.criteriosEscritos + " das 7 situações têm regra escrita. Procedimento permite executar; critério permite resolver.";
    // Atenção (alertas na ordem da fonte)
    var A = [];
    if (S.seteDias === "nunca") A.push({ id: "nunca", t: "Você nunca ficou sete dias sem atender mensagem desde que abriu. Na fonte, esse é o sinal de que sair da operação é a mais urgente das dez etapas." });
    if (S.dep.acesso && S.dep.acesso !== "fraca") A.push({ id: "acesso", t: "A dependência de acesso é risco de continuidade, não só de delegação: se o seu celular sumir, a operação para." + (S.acessoData ? " Data marcada: " + br(S.acessoData) + "." : " Marque uma tarde desta semana.") });
    if (S.nivel === "2") A.push({ id: "supervisiona", t: "Supervisionar tudo não é delegar. Troque a conferência de cada item por indicador semanal e auditoria por amostragem: uma unidade sorteada por semana." });
    if (r.equilibrio && r.equilibrio.k === "sim") A.push({ id: "equilibrio", t: "Com o custo da pessoa, o ponto de equilíbrio passa de 70% de ocupação. Pela fonte, a ordem muda: primeiro sobe a diária ou corta custo (módulos 2 e 3), depois contrata." });
    if (r.equilibrio && r.equilibrio.k === "naosei") A.push({ id: "equilibrio-nao-sei", t: "Você não sabe se o custo da pessoa cabe no ponto de equilíbrio. Faça a conta na Folha Única do Módulo 2 antes de fechar a contratação." });
    r.preReq.forEach(function (p) { if (!p.ok) A.push({ id: p.id, t: "Antes da semana 1: " + p.r.charAt(0).toLowerCase() + p.r.slice(1) + "." }); });
    if (r.criteriosEscritos < 7) A.push({ id: "criterios", t: (7 - r.criteriosEscritos === 1 ? "Falta a regra de 1 situação" : "Faltam as regras de " + (7 - r.criteriosEscritos) + " situações") + ". Quem escreveu todos os procedimentos e nenhum critério continua atendendo o telefone nas férias." });
    var u = num(S.unidades);
    if (S.formato === "meio" && u != null && u < 4) A.push({ id: "formato", t: "Meio período faz sentido a partir de quatro a seis unidades. Começar pelo formato errado é a causa mais comum de contratação que não se paga." });
    if (S.formato === "integral" && u != null && u < 6) A.push({ id: "formato", t: "Integral só quando a operação sustenta, normalmente com a segunda unidade no horizonte." });
    A.push({ id: "pular", t: "O erro mais comum é pular da semana 1 direto para a 4. Corrija depois, não durante: corrigir no meio ensina a pessoa a esperar você." });
    L.atencao = A;
    L.verificar = "Na data da avaliação (" + br(r.avaliacao) + "), responda: " + AVALIACAO.join(" ") + " Três sim: a pessoa está operando. Algum não: repita a semana 3, em vez de concluir que a contratação falhou.";
    return L;
  }

  // Critério de conclusão: os sete itens prontos e o PDF baixado
  function pendencias(S, fin) {
    S = completar(S); var r = calcular(S, fin), p = [];
    r.itens.forEach(function (i) { if (!i.ok) p.push(i.r.charAt(0).toLowerCase() + i.r.slice(1)); });
    if (!S.pdf) p.push("o PDF baixado");
    return p;
  }
  function concluido(S, fin) { return pendencias(S, fin).length === 0; }
  // Telas que ainda não validam (para "continuar de onde parei")
  function proximaVazia(S) { for (var k = 0; k < TELAS.length - 1; k++) { if (!validar(S, TELAS[k]).ok) return TELAS[k]; } return "resultado"; }
  // Sugestão de atividade quando o membro ainda não escolheu
  function sugerirAtividade(S) { var r = calcular(S); return r.primeira ? r.primeira.id : ""; }

  // Linhas do mapa de quem faz o quê com alçada (tabela da ficha e do PDF)
  function mapa(r, S) {
    S = completar(S);
    return r.atividades.map(function (a) {
      var setor = SETORES.filter(function (s) { return s.id === a.setor; })[0].r;
      var alc = a.resp && r.alcadasPorPessoa[a.resp] != null ? brl(r.alcadasPorPessoa[a.resp]) : a.dono ? "decide tudo hoje" : r.alcadaInicial ? "inicial " + brl(r.alcadaInicial) : "sem alçada";
      var depois = a.id === S.ativPlano && String(S.pessoa || "").trim() ? String(S.pessoa).trim() + (r.alcadaInicial ? " · alçada inicial " + brl(r.alcadaInicial) : "") : "";
      return { id: a.id, atividade: a.r, setor: setor, resp: a.resp || "a definir", horas: a.horas, entra: a.entra, alcada: alc, depois: depois };
    });
  }

  var api = { SITUACOES: SITUACOES, SETE_DIAS: SETE_DIAS, SETORES: SETORES, ATIVIDADES: ATIVIDADES, JULG: JULG, DEPENDENCIAS: DEPENDENCIAS, FORCA: FORCA,
    SITUACOES_CRITERIO: SITUACOES_CRITERIO, NIVEIS: NIVEIS, INDICADORES: INDICADORES, DIAS_SEMANA: DIAS_SEMANA, FORMATOS: FORMATOS, SIMNAO: SIMNAO, EQUILIBRIO: EQUILIBRIO,
    SEMANAS: SEMANAS, AVALIACAO: AVALIACAO, ONBOARDING: ONBOARDING, TELAS: TELAS, TITULOS: TITULOS, PROXIMO: PROXIMO, EXEMPLO: EXEMPLO,
    exemplo: exemplo, base: base, completar: completar, num: num, letras: letras, ehDono: ehDono, validar: validar, calcular: calcular, leituras: leituras,
    pendencias: pendencias, concluido: concluido, proximaVazia: proximaVazia, sugerirAtividade: sugerirAtividade, mapa: mapa,
    brl: brl, pct: pct, dec: dec, horasTxt: horasTxt, somaDias: somaDias, br: br, brCurto: brCurto };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else raiz.ZP = api;
})(typeof window !== "undefined" ? window : this);

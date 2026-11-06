/* Zion Hotel Academy · Arsenal Interativo 01 · Motor de cálculo e feedback (Bloco 01: Raio-X)
   Regras: cálculos determinísticos, sem benchmarks de mercado, sem classificar como bom ou ruim sem referência,
   separando FATO (calculado dos dados do aluno), HIPÓTESE (algo a investigar) e RECOMENDAÇÃO (ação). */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.ZionLogic = factory();
})(this, function () {
  "use strict";

  var PERIODOS = { "30": 30, "60": 60, "90": 90 };

  /* Lê um valor digitado. Retorna {ok, valor, erro, semDado}. Aceita vírgula decimal e ponto de milhar. */
  function lerNumero(bruto, opcoes) {
    opcoes = opcoes || {};
    if (bruto && typeof bruto === "object" && bruto.semDado) return { ok: true, valor: null, semDado: true };
    var s = bruto == null ? "" : String(bruto).trim();
    if (s === "") return { ok: true, valor: null, vazio: true };
    s = s.replace(/\s/g, "").replace(/^R\$/i, "");
    if (/^-?\d{1,3}(\.\d{3})+(,\d+)?$/.test(s)) s = s.replace(/\./g, "").replace(",", ".");
    else s = s.replace(",", ".");
    if (!/^-?\d+(\.\d+)?$/.test(s)) return { ok: false, erro: "Use só números." };
    var v = parseFloat(s);
    if (v < 0) return { ok: false, erro: "O valor não pode ser negativo." };
    if (opcoes.inteiro && Math.floor(v) !== v) return { ok: false, erro: "Use um número inteiro." };
    return { ok: true, valor: v };
  }

  function arred(v, casas) { var f = Math.pow(10, casas || 0); return Math.round(v * f) / f; }
  function taxa(a, b) { return b > 0 ? (a / b) * 100 : null; }

  /* Calcula o Raio-X a partir das respostas brutas da tela 06.
     d: {periodo:"30"|"60"|"90"|"outro", periodoDias, disponiveis, ocupadas, diaria, visualizacoes, consultas, reservas,
         mesmoPeriodo:bool, reservaInstantanea:"sim"|"nao"|"naosei", meta, anterior:{visualizacoes,consultas,reservas,ocupadas,disponiveis}|null}
     Campos de métricas podem ser {semDado:true}. */
  function calcular(d) {
    d = d || {};
    var erros = {}, avisos = [], pendencias = [], premissas = [], fora = [];
    function campo(nome, rotulo, opc) {
      var r = lerNumero(d[nome], opc);
      if (!r.ok) erros[nome] = r.erro;
      else if (r.vazio && !(opc && opc.opcional)) pendencias.push(rotulo + ": não preenchido");
      else if (r.semDado) pendencias.push(rotulo + ": marcado como \"Não tenho esse dado\"");
      return r.ok ? r.valor : null;
    }

    var dias = null;
    if (PERIODOS[d.periodo]) dias = PERIODOS[d.periodo];
    else if (d.periodo === "outro") {
      var p = lerNumero(d.periodoDias, { inteiro: true });
      if (!p.ok) erros.periodoDias = p.erro;
      else if (p.valor == null || p.valor < 1) erros.periodoDias = "Informe quantos dias tem o período.";
      else if (p.valor > 366) erros.periodoDias = "Use um período de até 366 dias.";
      else dias = p.valor;
    } else pendencias.push("Período analisado: não escolhido");

    var disp = campo("disponiveis", "Noites disponíveis", { inteiro: true });
    var ocup = campo("ocupadas", "Noites ocupadas", { inteiro: true });
    var diaria = campo("diaria", "Diária média efetiva");
    var vis = campo("visualizacoes", "Visualizações", { inteiro: true });
    var con = campo("consultas", "Consultas", { inteiro: true });
    var res = campo("reservas", "Reservas confirmadas", { inteiro: true });

    if (dias != null && disp != null && disp > dias) erros.disponiveis = "Há mais noites disponíveis (" + disp + ") do que dias no período (" + dias + ").";
    if (disp != null && ocup != null && ocup > disp) erros.ocupadas = "Noites ocupadas (" + ocup + ") não podem passar das disponíveis (" + disp + ").";
    if (disp === 0) erros.disponiveis = "Com 0 noites disponíveis não há o que analisar. Confira se o calendário está todo bloqueado.";

    var mesmo = d.mesmoPeriodo !== false;
    if (!mesmo) avisos.push("Você indicou que os números não são do mesmo período. As taxas entre visualizações, consultas e reservas não foram calculadas, porque comparariam períodos diferentes.");

    var r = { dias: dias, disponiveis: disp, ocupadas: ocup, diaria: diaria, visualizacoes: vis, consultas: con, reservas: res };
    var valido = Object.keys(erros).length === 0;

    // FATOS
    r.ocupacao = (valido && disp != null && ocup != null) ? taxa(ocup, disp) : null;
    r.noitesVazias = (valido && disp != null && ocup != null) ? disp - ocup : null;
    r.receita = (valido && ocup != null && diaria != null) ? ocup * diaria : null;

    r.taxaConsulta = null; r.taxaReserva = null; r.estadiaMedia = null;
    if (valido && mesmo) {
      if (vis != null && con != null) {
        if (vis === 0) { if (con > 0) avisos.push("Há consultas registradas com 0 visualizações. Confira se as consultas vieram de outros canais (WhatsApp, Instagram) ou se o número de visualizações está certo."); }
        else if (con > vis) avisos.push("Há mais consultas (" + con + ") do que visualizações (" + vis + "). Isso costuma indicar consultas vindas de outros canais ou métricas de períodos diferentes. A taxa de consultas por visualização não foi calculada.");
        else r.taxaConsulta = taxa(con, vis);
      }
      if (con != null && res != null) {
        if (d.reservaInstantanea === "sim") avisos.push("Com a Reserva Instantânea ligada, muitas reservas não passam por consulta. A conversão de consultas em reservas não foi calculada para não misturar os dois caminhos.");
        else if (con === 0) { /* sem consultas: taxa indefinida, tratado no feedback */ }
        else if (res > con) avisos.push("Há mais reservas (" + res + ") do que consultas (" + con + "). Se parte das reservas foi instantânea, isso é esperado. A conversão de consultas em reservas não foi calculada.");
        else r.taxaReserva = taxa(res, con);
      }
      if (ocup != null && res != null && res > 0) r.estadiaMedia = ocup / res;
      if (ocup != null && res != null && res > ocup) avisos.push("Há mais reservas (" + res + ") do que noites ocupadas (" + ocup + "). Cada reserva ocupa ao menos uma noite: confira os números.");
      if (ocup != null && ocup > 0 && res === 0) avisos.push("Há noites ocupadas, mas 0 reservas no período. Confira se as noites vêm de reservas feitas antes do período ou de outro canal.");
    }

    // Comparação opcional com período anterior (referência válida: o próprio histórico do aluno)
    r.anterior = null;
    if (valido && mesmo && d.anterior && d.anterior.ativo) {
      var a = {}, okA = true;
      ["visualizacoes", "consultas", "reservas", "ocupadas", "disponiveis"].forEach(function (k) {
        var x = lerNumero(d.anterior[k], { inteiro: true });
        if (!x.ok) { erros["anterior_" + k] = x.erro; okA = false; } else a[k] = x.valor;
      });
      if (okA && a.disponiveis != null && a.ocupadas != null && a.ocupadas > a.disponiveis) { erros.anterior_ocupadas = "No período anterior, as ocupadas passam das disponíveis."; okA = false; }
      if (okA) {
        a.ocupacao = (a.disponiveis != null && a.ocupadas != null && a.disponiveis > 0) ? taxa(a.ocupadas, a.disponiveis) : null;
        a.taxaConsulta = (a.visualizacoes > 0 && a.consultas != null && a.consultas <= a.visualizacoes) ? taxa(a.consultas, a.visualizacoes) : null;
        a.taxaReserva = (d.reservaInstantanea !== "sim" && a.consultas > 0 && a.reservas != null && a.reservas <= a.consultas) ? taxa(a.reservas, a.consultas) : null;
        r.anterior = a;
        premissas.push("O período anterior informado tem a mesma duração do período atual.");
      }
    }

    // Meta opcional do aluno (referência válida: o objetivo dele)
    r.meta = null;
    var m = lerNumero(d.meta, { inteiro: true });
    if (!m.ok) erros.meta = m.erro;
    else if (m.valor != null && disp != null && m.valor > disp) erros.meta = "A meta (" + m.valor + ") passa das noites disponíveis (" + disp + ").";
    else if (m.valor != null) r.meta = m.valor;

    r.necessario = null;
    if (Object.keys(erros).length === 0 && r.meta != null && ocup != null && r.meta > ocup && r.estadiaMedia && r.taxaConsulta && r.taxaReserva) {
      var faltam = r.meta - ocup;
      var resN = faltam / r.estadiaMedia;
      var conN = resN / (r.taxaReserva / 100);
      var visN = conN / (r.taxaConsulta / 100);
      r.necessario = { noites: faltam, reservas: Math.ceil(resN), consultas: Math.ceil(conN), visualizacoes: Math.ceil(visN), multiplicador: vis > 0 ? (vis + visN) / vis : null };
      premissas.push("A conta da meta supõe que a estadia média e as duas taxas continuem iguais. É uma conta de referência, não uma previsão.");
    }

    premissas.push("Receita estimada = noites ocupadas × diária média efetiva (o valor recebido por noite, não o preço anunciado).");
    premissas.push("Ocupação = noites ocupadas ÷ noites disponíveis × 100. Noites bloqueadas por você não entram como disponíveis.");
    fora.push("Taxa de limpeza, taxas da plataforma, impostos e custos não entram na receita estimada. Eles serão tratados no Pilar 5.");
    fora.push("Sazonalidade, eventos e concorrência não são medidos aqui. Só os números que você informou.");

    r.erros = erros; r.valido = Object.keys(erros).length === 0;
    r.avisos = avisos; r.pendencias = pendencias; r.premissas = premissas; r.foraDoCalculo = fora;
    return r;
  }

  /* Motor de feedback: devolve uma lista de blocos com as 5 partes exigidas.
     Cada bloco: {id, titulo, resultado, significado, atencao, fazer, verificar, tipo} */
  function feedback(r, perfil) {
    perfil = perfil || {};
    var out = [];
    function pct(v) { return v == null ? "–" : (arred(v, 1).toLocaleString ? arred(v, 1).toLocaleString("pt-BR") : String(arred(v, 1))) + "%"; }

    if (!r.valido) {
      out.push({ id: "corrigir", titulo: "Alguns números precisam de correção", resultado: "Encontramos " + Object.keys(r.erros).length + " campo(s) com problema.",
        significado: "Com números inconsistentes, qualquer conta sairia errada.", atencao: Object.keys(r.erros).map(function (k) { return r.erros[k]; }).join(" "),
        fazer: "Volte à tela anterior e corrija os campos marcados.", verificar: "Os avisos em vermelho somem quando os números fecham." });
      return out;
    }

    var faltaBase = [];
    if (r.disponiveis == null) faltaBase.push("noites disponíveis");
    if (r.ocupadas == null) faltaBase.push("noites ocupadas");
    var funilConhecido = r.visualizacoes != null && r.consultas != null && r.reservas != null;

    if (faltaBase.length) {
      out.push({ id: "D", titulo: "Ainda faltam dados", resultado: "Sem " + faltaBase.join(" e ") + ", não é possível calcular a ocupação.",
        significado: "Ainda não temos dados suficientes para identificar o principal ponto de atenção.",
        atencao: "Veja o que falta: " + r.pendencias.join("; ") + ".",
        fazer: "Abra o calendário do anúncio, conte as noites do período e volte para preencher.",
        verificar: "Quando os dois números estiverem preenchidos, a ocupação aparece nesta tela." });
      return out;
    }

    // Bloco base: ocupação (fato) sem juízo de valor
    var base = { id: "ocupacao", titulo: "Sua ocupação no período", tipo: "fato",
      resultado: r.ocupadas + " de " + r.disponiveis + " noites ocupadas: " + pct(r.ocupacao) + " de ocupação, com " + r.noitesVazias + " noites vazias." + (r.receita != null ? " Receita estimada de diárias: R$ " + Math.round(r.receita).toLocaleString("pt-BR") + "." : ""),
      significado: "Este é o seu ponto de partida. Sozinha, a ocupação não é uma nota: o que ela significa depende da sua meta, da época e do seu histórico.",
      atencao: r.meta != null ? (r.meta > r.ocupadas ? "Sua meta é " + r.meta + " noites: faltam " + (r.meta - r.ocupadas) + " para chegar lá." : "Você já atingiu a meta de " + r.meta + " noites neste período.") : "Você não informou uma meta. Sem ela ou sem o período anterior, não há referência para comparar.",
      fazer: "Guarde este número. Ele é a linha de base para medir qualquer mudança que você fizer.",
      verificar: "Ocupação e noites vazias no próximo período de mesma duração." };
    if (r.anterior && r.anterior.ocupacao != null) {
      var dif = r.ocupacao - r.anterior.ocupacao;
      base.atencao = "No período anterior a ocupação foi " + pct(r.anterior.ocupacao) + ". Agora é " + pct(r.ocupacao) + " (" + (dif >= 0 ? "+" : "") + arred(dif, 1).toLocaleString("pt-BR") + " pontos). " + base.atencao.replace(/^Você não informou.*$/, "");
    }
    out.push(base);

    if (!funilConhecido) {
      var faltam = [];
      if (r.visualizacoes == null) faltam.push("visualizações");
      if (r.consultas == null) faltam.push("consultas");
      if (r.reservas == null) faltam.push("reservas");
      out.push({ id: "D", titulo: "O caminho do hóspede está incompleto", tipo: "pendencia",
        resultado: "Sem " + faltam.join(", ") + ", não dá para ver em que etapa o hóspede desiste.",
        significado: "Ainda não temos dados suficientes para identificar o principal ponto de atenção.",
        atencao: "No Airbnb, esses números ficam em Menu → Insights → Desempenho do anúncio. Em outras plataformas, procure por estatísticas ou desempenho.",
        fazer: "Se a sua plataforma mostra esses números, preencha. Se não mostra, comece a anotar consultas e reservas a partir de hoje.",
        verificar: "Com os três números do mesmo período, esta análise passa a mostrar onde o hóspede para." });
      return out.concat(dificuldade(perfil, null));
    }

    if (r.avisos.length && r.taxaConsulta == null && r.taxaReserva == null && r.visualizacoes > 0 && r.consultas > 0) {
      // períodos ou definições incompatíveis: não interpretar
      out.push({ id: "D", titulo: "Os números não são comparáveis entre si", tipo: "pendencia", resultado: r.avisos.join(" "),
        significado: "Comparar números de períodos ou canais diferentes levaria a conclusões erradas.",
        atencao: "Confira se visualizações, consultas e reservas vêm da mesma plataforma e do mesmo período.",
        fazer: "Ajuste os números ou marque \"Não tenho esse dado\" no que não for compatível.",
        verificar: "As taxas aparecem quando os três números forem do mesmo período e canal." });
      return out.concat(dificuldade(perfil, null));
    }

    var etapa = null;
    if (r.visualizacoes === 0) {
      etapa = "visibilidade";
      out.push({ id: "V0", titulo: "Nenhuma visualização registrada", tipo: "hipotese",
        resultado: "O anúncio teve 0 visualizações no período.",
        significado: "Sem visualizações, o hóspede nem chega a ver a oferta. O ponto de atenção está antes das fotos e do preço.",
        atencao: "Vale investigar se o anúncio está ativo, se há datas abertas no calendário, se a estadia mínima não está bloqueando buscas e se o preço exibido na busca está muito distante do que o hóspede filtra.",
        fazer: "Confira hoje: anúncio publicado, calendário aberto nos próximos 60 dias e regras de estadia mínima.",
        verificar: "Visualizações nos próximos 7 dias, comparadas com estes.",
      });
    } else if (r.consultas === 0) {
      etapa = "atratividade";
      out.push({ id: "A", titulo: "Visualizações sem consultas", tipo: "hipotese",
        resultado: r.visualizacoes.toLocaleString("pt-BR") + " visualizações e nenhuma consulta registrada" + (r.reservas > 0 ? " (" + r.reservas + " reserva(s), possivelmente instantâneas)" : "") + ".",
        significado: "Seu anúncio está recebendo visualizações, mas não há consultas registradas.",
        atencao: "Vale investigar se as fotos, a descrição, o preço total, as regras e a disponibilidade estão alinhados ao que o hóspede procura. Isso é uma hipótese: os números mostram onde o hóspede para, não o motivo.",
        fazer: "Escolha um único item para revisar primeiro, por exemplo a primeira foto ou o título, e anote a data da mudança.",
        verificar: "Consultas por visualização no próximo período de mesma duração." });
    } else if (r.reservas === 0 && r.reservaInstantanea !== "sim") {
      etapa = "conversao";
      out.push({ id: "B", titulo: "Consultas sem reservas", tipo: "hipotese",
        resultado: r.consultas + " consulta(s) e nenhuma reserva confirmada no período.",
        significado: "As pessoas demonstram interesse, mas não estão concluindo a reserva.",
        atencao: "Vamos investigar atendimento (tempo e qualidade da resposta), condições (regras, cancelamento, estadia mínima), preço final com taxas e possíveis objeções que aparecem nas mensagens.",
        fazer: "Releia as últimas consultas e anote, para cada uma, o motivo provável de não ter reservado.",
        verificar: "Conversão de consultas em reservas no próximo período." });
    } else {
      // Funil completo e com valores > 0: só interpretamos com referência (período anterior ou meta)
      var bloco = { id: "funil", titulo: "Onde o hóspede para", tipo: "fato",
        resultado: "De " + r.visualizacoes.toLocaleString("pt-BR") + " visualizações saíram " + r.consultas + " consultas" + (r.taxaConsulta != null ? " (" + pct(r.taxaConsulta) + ")" : "") + " e " + r.reservas + " reservas" + (r.taxaReserva != null ? " (" + pct(r.taxaReserva) + " das consultas)" : "") + "." + (r.estadiaMedia ? " Estadia média: " + arred(r.estadiaMedia, 1).toLocaleString("pt-BR") + " noites por reserva." : ""),
        significado: "", atencao: "", fazer: "", verificar: "" };
      var a = r.anterior;
      if (a) {
        var quedas = [];
        if (a.visualizacoes != null && r.visualizacoes < a.visualizacoes) quedas.push({ etapa: "visibilidade", txt: "visualizações caíram de " + a.visualizacoes + " para " + r.visualizacoes, peso: (a.visualizacoes - r.visualizacoes) / a.visualizacoes });
        if (a.taxaConsulta != null && r.taxaConsulta != null && r.taxaConsulta < a.taxaConsulta) quedas.push({ etapa: "atratividade", txt: "consultas por visualização caíram de " + pct(a.taxaConsulta) + " para " + pct(r.taxaConsulta), peso: (a.taxaConsulta - r.taxaConsulta) / a.taxaConsulta });
        if (a.taxaReserva != null && r.taxaReserva != null && r.taxaReserva < a.taxaReserva) quedas.push({ etapa: "conversao", txt: "conversão de consultas em reservas caiu de " + pct(a.taxaReserva) + " para " + pct(r.taxaReserva), peso: (a.taxaReserva - r.taxaReserva) / a.taxaReserva });
        quedas.sort(function (x, y) { return y.peso - x.peso; });
        if (quedas.length) {
          etapa = quedas[0].etapa;
          bloco.significado = "Comparando com o seu período anterior: " + quedas.map(function (q) { return q.txt; }).join("; ") + ".";
          bloco.atencao = "A maior queda relativa está em " + nomeEtapa(etapa) + ". " + investigar(etapa) + " A comparação mostra onde mudou, não prova o motivo: época e eventos também influenciam.";
          bloco.fazer = acao(etapa);
          bloco.verificar = indicador(etapa) + " no próximo período de mesma duração.";
        } else {
          bloco.significado = "Comparado ao período anterior, nenhuma etapa do caminho caiu.";
          bloco.atencao = "Se mesmo assim há noites vazias, vale olhar disponibilidade e preço, que entram no Pilar 5.";
          bloco.fazer = "Mantenha o que está funcionando e siga para o Pilar 2.";
          bloco.verificar = "Os mesmos três números no próximo período.";
        }
      } else if (r.necessario) {
        etapa = "visibilidade";
        var n = r.necessario;
        bloco.significado = "Para chegar à sua meta mantendo as taxas atuais, você precisaria de cerca de " + n.reservas + " reservas a mais, " + n.consultas + " consultas a mais e " + n.visualizacoes.toLocaleString("pt-BR") + " visualizações a mais" + (n.multiplicador ? ", ou seja, cerca de " + arred(n.multiplicador, 1).toLocaleString("pt-BR") + " vezes as visualizações de hoje" : "") + ".";
        bloco.atencao = "A distância até a meta pode ser fechada trazendo mais gente (visibilidade e disponibilidade) ou convertendo melhor quem já vê o anúncio (apresentação da oferta). Os números não dizem qual caminho é o certo para você: são hipóteses a testar.";
        bloco.fazer = "Comece conferindo visibilidade e disponibilidade (datas abertas, estadia mínima, preço exibido na busca) e a apresentação (primeira foto e título). Mude uma coisa por vez.";
        bloco.verificar = "Visualizações e consultas por visualização no próximo período.";
      } else {
        bloco.significado = "Estes números viram a sua linha de base. Sem uma referência (o seu período anterior ou uma meta), não é possível dizer qual etapa está abaixo do esperado.";
        bloco.atencao = "Não usamos médias de mercado: elas variam muito por cidade, tipo de imóvel e época, e poderiam te levar a corrigir a coisa errada.";
        bloco.fazer = "Volte e informe o período anterior ou uma meta de noites. Se não tiver, siga em frente e use estes números como ponto de partida.";
        bloco.verificar = "Os mesmos três números no próximo período de mesma duração.";
      }
      out.push(bloco);
    }
    return out.concat(dificuldade(perfil, etapa));
  }

  function nomeEtapa(e) { return { visibilidade: "visibilidade (quantas pessoas veem o anúncio)", atratividade: "atratividade (quem vê e pergunta)", conversao: "conversão (quem pergunta e reserva)" }[e]; }
  function investigar(e) {
    return {
      visibilidade: "Vale investigar disponibilidade do calendário, estadia mínima, preço exibido na busca e se houve mudança no anúncio.",
      atratividade: "Vale investigar fotos, título, descrição, preço total e regras.",
      conversao: "Vale investigar atendimento, preço final com taxas, condições de cancelamento e objeções nas mensagens."
    }[e];
  }
  function acao(e) {
    return {
      visibilidade: "Confira o calendário dos próximos 60 dias e as regras de estadia mínima. Anote o que mudar.",
      atratividade: "Revise um item da apresentação, começando pela primeira foto ou pelo título.",
      conversao: "Releia as últimas consultas e liste as objeções que aparecem."
    }[e];
  }
  function indicador(e) { return { visibilidade: "Visualizações", atratividade: "Consultas por visualização", conversao: "Conversão de consultas em reservas" }[e]; }

  /* Confronta a percepção do aluno (tela 03) com o que os dados mostram. */
  function dificuldade(perfil, etapa) {
    var mapa = { visualizacoes: "visibilidade", semConsultas: "atratividade", semReservas: "conversao", dinheiro: "financeiro" };
    var p = mapa[perfil.dificuldade];
    if (!p) return [];
    var nomes = { visibilidade: "poucas visualizações", atratividade: "visualizações sem consultas", conversao: "consultas sem reservas", financeiro: "reservas, mas pouco dinheiro no fim do mês" };
    if (p === "financeiro") return [{ id: "percepcao", titulo: "O que você sentia", tipo: "hipotese", resultado: "Na tela 3 você apontou: " + nomes[p] + ".", significado: "Isso será medido no Pilar 5, com custos, taxas e margem.", atencao: "O Raio-X mede a procura. O resultado financeiro depende de números que ainda não foram pedidos.", fazer: "Separe os custos do último mês: limpeza, lavanderia, energia, taxas da plataforma.", verificar: "Margem de contribuição estimada, no Pilar 5." }];
    if (!etapa) return [];
    return [{ id: "percepcao", titulo: "O que você sentia e o que os dados mostram", tipo: "hipotese",
      resultado: "Você apontou " + nomes[p] + ". " + (p === etapa ? "Os dados apontam para a mesma etapa." : "Os dados apontam para " + nomes[etapa] + "."),
      significado: p === etapa ? "Sua percepção e os números concordam, o que dá mais segurança para começar por aí." : "É comum a percepção e os números apontarem lugares diferentes. Os números mostram onde o hóspede para.",
      atencao: "Mesmo com os números, a causa continua sendo uma hipótese até você testar.",
      fazer: "Comece pela etapa que os números apontam.", verificar: indicador(etapa) + "." }];
  }

  return { lerNumero: lerNumero, calcular: calcular, feedback: feedback, taxa: taxa, arred: arred };
});

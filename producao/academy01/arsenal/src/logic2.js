/* Zion Hotel Academy · Arsenal Interativo 01 · Pilares 2 a 7
   Regras determinísticas e testáveis. Sem benchmarks de mercado; toda interpretação vem dos dados do aluno
   ou de critérios explícitos mostrados na tela. */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory(require("./logic.js"));
  else root.ZionLogic2 = factory(root.ZionLogic);
})(this, function (L) {
  "use strict";
  var num = function (v, o) { return L.lerNumero(v, o); };
  function arred(v, c) { return L.arred(v, c); }

  /* ---------------- PILAR 2 · Perfil de hóspede ---------------- */
  var CARACTERISTICAS = [
    ["banheira", "Banheira ou ofurô"], ["lareira", "Lareira"], ["vista", "Vista bonita"], ["isolamento", "Privacidade, sem vizinhos à vista"],
    ["cozinha", "Cozinha completa"], ["quartos2", "Dois quartos ou mais"], ["berco", "Berço ou itens para bebê"], ["areaExterna", "Área externa ou jardim"],
    ["wifi", "Wi-Fi rápido e estável"], ["mesaTrabalho", "Mesa para trabalhar"], ["churrasqueira", "Churrasqueira ou área gourmet"], ["piscina", "Piscina"],
    ["pet", "Aceita animais"], ["quintal", "Quintal cercado"], ["trilhas", "Trilhas ou natureza por perto"], ["estacionamento", "Estacionamento"],
    ["centro", "Perto do centro ou de restaurantes"], ["climatizacao", "Ar-condicionado ou aquecimento"]
  ];
  var PUBLICOS = {
    casal: { nome: "Casal em escapada", precisa: ["banheira", "lareira", "vista", "isolamento"], necessidade: "privacidade e tempo a dois, sem interrupções", objecao: "medo de que o lugar não seja tão reservado quanto parece nas fotos", minPessoas: 2 },
    familia: { nome: "Família com crianças", precisa: ["cozinha", "quartos2", "berco", "areaExterna", "estacionamento"], necessidade: "espaço, segurança e praticidade para as crianças", objecao: "dúvida se a casa é segura e equipada para crianças", minPessoas: 4 },
    remoto: { nome: "Quem trabalha remoto", precisa: ["wifi", "mesaTrabalho", "climatizacao", "cozinha"], necessidade: "internet confiável e um canto para trabalhar", objecao: "medo de a internet cair no meio de uma reunião", minPessoas: 1 },
    amigos: { nome: "Grupo de amigos", precisa: ["quartos2", "churrasqueira", "piscina", "areaExterna"], necessidade: "espaço para conviver e se divertir juntos", objecao: "regras rígidas sobre barulho e número de pessoas", minPessoas: 4 },
    pet: { nome: "Quem viaja com o pet", precisa: ["pet", "quintal", "areaExterna"], necessidade: "levar o animal sem preocupação", objecao: "cobranças extras ou restrições escondidas para o pet", minPessoas: 1 },
    natureza: { nome: "Quem busca natureza", precisa: ["trilhas", "vista", "areaExterna", "isolamento"], necessidade: "desconectar e ficar perto da natureza", objecao: "acesso difícil ou falta de informação sobre como chegar", minPessoas: 1 }
  };
  /* Afinidade = itens do público que o imóvel tem ÷ itens que o público procura. Critério explícito, não pesquisa de mercado. */
  function afinidade(caracs, capacidade) {
    var tem = {}; (caracs || []).forEach(function (c) { tem[c] = true; });
    var cap = num(capacidade, { inteiro: true }).valor;
    return Object.keys(PUBLICOS).map(function (id) {
      var p = PUBLICOS[id], bate = p.precisa.filter(function (c) { return tem[c]; });
      var cabe = cap == null ? null : cap >= p.minPessoas;
      return { id: id, nome: p.nome, bate: bate, faltam: p.precisa.filter(function (c) { return !tem[c]; }), total: p.precisa.length,
        pct: Math.round(bate.length / p.precisa.length * 100), cabe: cabe };
    }).sort(function (a, b) { return (b.cabe === false ? -1 : 0) - (a.cabe === false ? -1 : 0) || b.pct - a.pct || a.nome.localeCompare(b.nome); });
  }
  function nomeCarac(id) { for (var i = 0; i < CARACTERISTICAS.length; i++) if (CARACTERISTICAS[i][0] === id) return CARACTERISTICAS[i][1]; return id; }

  function validarPerfil(perfil, caracs, capacidade) {
    var erros = {}, avisos = [];
    if (!perfil.publico) erros.publico = "Escolha um perfil prioritário.";
    if (!perfil.ocasiao || !perfil.ocasiao.trim()) erros.ocasiao = "Descreva a ocasião da viagem.";
    var pes = num(perfil.pessoas, { inteiro: true });
    if (!pes.ok) erros.pessoas = pes.erro; else if (pes.valor == null || pes.valor < 1) erros.pessoas = "Informe quantas pessoas costumam vir.";
    var cap = num(capacidade, { inteiro: true }).valor;
    if (pes.ok && pes.valor != null && cap != null && pes.valor > cap) erros.pessoas = "São " + pes.valor + " pessoas, mas a capacidade informada é " + cap + ".";
    if (!perfil.necessidade || !perfil.necessidade.trim()) erros.necessidade = "Escreva a principal necessidade desse hóspede.";
    if (!perfil.objecao || !perfil.objecao.trim()) erros.objecao = "Escreva a principal objeção ou dúvida.";
    var ess = (perfil.essenciais || []).filter(Boolean);
    if (ess.length !== 3) erros.essenciais = "Marque exatamente 3 comodidades essenciais.";
    var tem = {}; (caracs || []).forEach(function (c) { tem[c] = true; });
    var semImovel = ess.filter(function (c) { return !tem[c]; });
    if (semImovel.length) avisos.push("Você marcou como essencial algo que não indicou ter no imóvel: " + semImovel.map(nomeCarac).join(", ") + ". Se o hóspede precisa disso e não encontra, a objeção cresce.");
    if (perfil.publico && PUBLICOS[perfil.publico]) {
      var a = afinidade(caracs, capacidade).filter(function (x) { return x.id === perfil.publico; })[0];
      if (a && a.cabe === false) avisos.push("A capacidade informada é menor do que esse perfil costuma precisar (" + PUBLICOS[perfil.publico].minPessoas + " pessoas ou mais).");
      if (a && a.faltam.length) avisos.push("Para esse perfil, o imóvel não tem: " + a.faltam.map(nomeCarac).join(", ") + ". Isso não impede a escolha, mas vale deixar claro no anúncio o que existe e o que não existe.");
    }
    return { valido: Object.keys(erros).length === 0, erros: erros, avisos: avisos };
  }

  /* ---------------- PILAR 3 · Proposta de valor ---------------- */
  var VAGAS = ["aconchegante", "incrível", "incrivel", "perfeito", "perfeita", "maravilhoso", "maravilhosa", "lindo", "linda", "único", "unico", "especial", "inesquecível", "inesquecivel", "top", "show"];
  function palavrasVagas(t) {
    var s = " " + String(t || "").toLowerCase().replace(/[^a-zà-ú0-9 ]/gi, " ") + " ";
    return VAGAS.filter(function (w) { return s.indexOf(" " + w + " ") >= 0; });
  }
  function montarProposta(d) {
    var difs = (d.diferenciais || []).filter(function (x) { return x && x.verdadeiro && x.caracteristica && x.caracteristica.trim(); });
    var nome = (d.hospedagem || "A hospedagem").trim();
    var publico = (d.publicoNome || "o seu hóspede").toLowerCase();
    var nec = (d.necessidade || "").trim();
    var dd = difs.slice(0, 2).map(function (x) { return x.caracteristica.trim(); });
    var ben = difs.length && difs[0].beneficio ? difs[0].beneficio.trim() : "";
    var t = "Para " + publico + (nec ? " que busca " + nec : "") + ", " + nome + " oferece " + (dd.length ? dd.join(" e ") : "[seus diferenciais]") + (ben ? ", para " + ben : "") + ".";
    return t.replace(/\s+/g, " ");
  }
  function avaliarProposta(texto, d) {
    var t = String(texto || "").trim(), checks = [];
    var difs = (d.diferenciais || []).filter(function (x) { return x && x.verdadeiro && x.caracteristica; });
    checks.push({ ok: t.length >= 40 && t.length <= 240, txt: "Tem entre 40 e 240 caracteres (" + t.length + ")." });
    checks.push({ ok: !!d.publicoNome && t.toLowerCase().indexOf(String(d.publicoNome).toLowerCase().split(" ")[0]) >= 0, txt: "Diz para quem é (o perfil do Pilar 2)." });
    var citados = difs.filter(function (x) { return t.toLowerCase().indexOf(x.caracteristica.trim().toLowerCase().split(" ")[0]) >= 0; });
    checks.push({ ok: citados.length >= 1, txt: "Cita ao menos um diferencial que você marcou como verdadeiro." });
    var vag = palavrasVagas(t);
    checks.push({ ok: vag.length === 0, txt: vag.length ? "Troque palavras vagas por fatos: " + vag.join(", ") + "." : "Não usa palavras vagas como \"aconchegante\" ou \"incrível\"." });
    var falsos = (d.diferenciais || []).filter(function (x) { return x && x.caracteristica && !x.verdadeiro && t.toLowerCase().indexOf(x.caracteristica.trim().toLowerCase()) >= 0; });
    checks.push({ ok: falsos.length === 0, txt: falsos.length ? "Cita algo que você não confirmou como verdadeiro: " + falsos.map(function (x) { return x.caracteristica; }).join(", ") + "." : "Só usa o que você confirmou como verdadeiro." });
    return { checks: checks, aprovados: checks.filter(function (c) { return c.ok; }).length, total: checks.length };
  }

  /* ---------------- PILAR 4 · Anúncio ---------------- */
  var LIMITE_TITULO = 50; /* limite de caracteres do título no Airbnb */
  function avaliarTitulo(t, ctx) {
    t = String(t || "").trim(); ctx = ctx || {};
    var c = [];
    c.push({ ok: t.length > 0 && t.length <= LIMITE_TITULO, txt: t.length + " de " + LIMITE_TITULO + " caracteres" + (t.length > LIMITE_TITULO ? ": o Airbnb corta o que passar disso." : ".") });
    var low = t.toLowerCase();
    var temDif = (ctx.diferenciais || []).some(function (x) { return x && x.verdadeiro && x.caracteristica && low.indexOf(x.caracteristica.trim().toLowerCase().split(" ")[0]) >= 0; });
    c.push({ ok: temDif, txt: "Mostra um diferencial real." });
    var pub = ctx.publicoNome ? ctx.publicoNome.toLowerCase().split(" ")[0] : "";
    var palavrasPub = { casal: ["casal", "casais", "romant", "dois"], família: ["famíl", "famil", "crian"], quem: ["trabalh", "remot", "home"], grupo: ["grupo", "amigos", "turma"] };
    var lista = palavrasPub[pub] || (pub ? [pub] : []);
    c.push({ ok: lista.some(function (w) { return low.indexOf(w) >= 0; }) || !pub, txt: "Fala com o seu hóspede prioritário." });
    var vag = palavrasVagas(t);
    c.push({ ok: !vag.length, txt: vag.length ? "Evite palavras vagas: " + vag.join(", ") + "." : "Sem palavras vagas." });
    var letras = t.replace(/[^A-Za-zÀ-ú]/g, "");
    c.push({ ok: !(letras.length > 6 && letras === letras.toUpperCase()), txt: "Não está todo em letras maiúsculas." });
    return { checks: c, aprovados: c.filter(function (x) { return x.ok; }).length, total: c.length };
  }
  function avaliarDescricao(t, ctx) {
    t = String(t || "").trim(); ctx = ctx || {};
    var primeiras = t.split(/\n/)[0] || "";
    var c = [];
    c.push({ ok: t.length >= 300, txt: "Tem pelo menos 300 caracteres (" + t.length + ")." });
    c.push({ ok: primeiras.length > 0 && primeiras.length <= 200, txt: "A primeira frase resume a proposta em até 200 caracteres." });
    var low = t.toLowerCase();
    c.push({ ok: /(check-?in|chegada|acesso|como chegar|estrada)/.test(low), txt: "Explica a chegada ou o acesso." });
    c.push({ ok: /(regra|não é permitido|nao e permitido|proibid|silêncio|silencio|horário|horario)/.test(low), txt: "Deixa as regras claras." });
    var vag = palavrasVagas(t);
    c.push({ ok: vag.length <= 1, txt: vag.length > 1 ? "Muitas palavras vagas: " + vag.join(", ") + "." : "Usa fatos em vez de adjetivos vagos." });
    return { checks: c, aprovados: c.filter(function (x) { return x.ok; }).length, total: c.length };
  }

  /* ---------------- PILAR 5 · Financeiro ---------------- */
  function financeiro(d) {
    var erros = {}, premissas = [], fora = [];
    function campo(k, opc) { var r = num(d[k], opc); if (!r.ok) erros[k] = r.erro; return r.ok ? r.valor : null; }
    var receita = campo("receita"), noites = campo("noites", { inteiro: true }), reservas = campo("reservas", { inteiro: true });
    var tp = campo("taxaPlataforma"), imp = campo("impostos"), limpeza = campo("limpezaPorReserva"), varN = campo("variavelPorNoite"), fixos = campo("fixosPeriodo");
    [["taxaPlataforma", tp], ["impostos", imp]].forEach(function (x) { if (x[1] != null && x[1] > 100) erros[x[0]] = "Use um percentual entre 0 e 100."; });
    if (receita == null && !erros.receita) erros.receita = "Informe a receita de hospedagem do período.";
    if (noites == null && !erros.noites) erros.noites = "Informe as noites ocupadas.";
    if (noites === 0) erros.noites = "Com 0 noites ocupadas não há margem para calcular.";
    if (reservas == null && !erros.reservas) erros.reservas = "Informe o número de reservas.";
    if (reservas != null && noites != null && reservas > noites) erros.reservas = "Há mais reservas do que noites ocupadas.";
    var r = { erros: erros, valido: Object.keys(erros).length === 0 };
    if (!r.valido) return r;
    tp = tp || 0; imp = imp || 0; limpeza = limpeza || 0; varN = varN || 0; fixos = fixos || 0;
    r.receita = receita; r.noites = noites; r.reservas = reservas;
    r.taxas = receita * tp / 100; r.impostos = receita * imp / 100;
    r.custoLimpeza = limpeza * reservas; r.custoVariavelNoites = varN * noites;
    r.variaveis = r.custoLimpeza + r.custoVariavelNoites;
    r.margem = receita - r.taxas - r.impostos - r.variaveis;
    r.margemPct = receita > 0 ? r.margem / receita * 100 : null;
    r.margemPorNoite = r.margem / noites;
    r.fixos = fixos; r.resultado = r.margem - fixos;
    r.equilibrioNoites = (fixos > 0 && r.margemPorNoite > 0) ? Math.ceil(fixos / r.margemPorNoite) : null;
    var itens = [["Taxa da plataforma", r.taxas], ["Impostos", r.impostos], ["Limpeza", r.custoLimpeza], ["Outros custos por noite", r.custoVariavelNoites], ["Custos fixos do período", fixos]];
    r.itens = itens.map(function (i) { return { nome: i[0], valor: i[1], pctReceita: receita > 0 ? i[1] / receita * 100 : null }; }).sort(function (a, b) { return b.valor - a.valor; });
    premissas.push("Margem de contribuição = receita − taxa da plataforma − impostos − limpeza (por reserva) − outros custos por noite.");
    premissas.push("Resultado operacional simplificado = margem de contribuição − custos fixos do período. Não é lucro líquido.");
    if (r.equilibrioNoites) premissas.push("Ponto de equilíbrio = custos fixos ÷ margem por noite, supondo a mesma diária e os mesmos custos por noite.");
    fora.push("Depreciação, financiamento do imóvel, imposto de renda pessoal e o seu tempo de trabalho não entram, a menos que você os tenha somado nos custos fixos.");
    fora.push("Taxa de limpeza cobrada do hóspede não entra na receita, a menos que você a tenha somado na receita informada.");
    r.premissas = premissas; r.foraDoCalculo = fora;
    return r;
  }
  function simular(base, novaDiaria, novasNoites) {
    var nd = num(novaDiaria).valor, nn = num(novasNoites, { inteiro: true }).valor;
    if (!base || !base.valido || nd == null || nn == null || nn <= 0) return null;
    var estadia = base.noites / base.reservas;
    var reservas = Math.max(1, Math.round(nn / estadia));
    var tp = base.receita > 0 ? base.taxas / base.receita : 0, imp = base.receita > 0 ? base.impostos / base.receita : 0;
    var limpezaUnit = base.reservas > 0 ? base.custoLimpeza / base.reservas : 0, varN = base.custoVariavelNoites / base.noites;
    var receita = nd * nn;
    var margem = receita - receita * tp - receita * imp - limpezaUnit * reservas - varN * nn;
    return { diaria: nd, noites: nn, reservas: reservas, receita: receita, margem: margem, resultado: margem - base.fixos, estadiaMedia: estadia };
  }
  function feedbackFinanceiro(r) {
    if (!r || !r.valido) return [{ id: "corrigir", tipo: "pendencia", titulo: "Faltam números", resultado: "Alguns campos precisam de correção.", significado: "Sem eles, a conta de margem sairia errada.", atencao: r ? Object.keys(r.erros).map(function (k) { return r.erros[k]; }).join(" ") : "", fazer: "Corrija os campos marcados.", verificar: "Os avisos somem quando os números fecham." }];
    var brl = function (v) { var n = Math.round(v); return (n < 0 ? "−" : "") + "R$ " + Math.abs(n).toLocaleString("pt-BR"); };
    var maior = r.itens[0], out = [];
    if (r.margem <= 0) {
      out.push({ id: "C1", tipo: "hipotese", titulo: "Cada noite custa mais do que rende", resultado: "Margem de contribuição de " + brl(r.margem) + " em " + r.noites + " noites (" + brl(r.margemPorNoite) + " por noite).",
        significado: "Com esses números, vender mais noites aumenta o prejuízo, porque cada noite não cobre os próprios custos.",
        atencao: "O maior custo informado é " + maior.nome.toLowerCase() + " (" + brl(maior.valor) + "). Vale revisar taxas, despesas variáveis e a diária antes de buscar mais reservas.",
        fazer: "Use o simulador para ver qual diária deixa a margem por noite acima de zero.", verificar: "Margem por noite no próximo período." });
    } else if (r.resultado < 0) {
      out.push({ id: "C2", tipo: "hipotese", titulo: "A margem não cobre os custos fixos", resultado: "Margem de contribuição de " + brl(r.margem) + " e custos fixos de " + brl(r.fixos) + ": resultado operacional simplificado de " + brl(r.resultado) + ".",
        significado: "Sua hospedagem está gerando receita, mas os custos informados podem estar comprometendo o resultado.",
        atencao: "Com a margem atual de " + brl(r.margemPorNoite) + " por noite, seriam necessárias cerca de " + r.equilibrioNoites + " noites no período para cobrir os custos fixos. O maior custo informado é " + maior.nome.toLowerCase() + ".",
        fazer: "Revise taxas, despesas variáveis e margem: comece pelo maior item da lista.", verificar: "Resultado operacional simplificado no próximo período." });
    } else {
      out.push({ id: "C3", tipo: "fato", titulo: "A margem cobre os custos informados", resultado: "Resultado operacional simplificado de " + brl(r.resultado) + " no período (margem de " + arred(r.margemPct, 1).toLocaleString("pt-BR") + "% da receita).",
        significado: "Com os custos que você informou, o período fechou positivo. Isso não é lucro líquido: veja o que ficou fora do cálculo.",
        atencao: "O maior custo informado é " + maior.nome.toLowerCase() + " (" + arred(maior.pctReceita, 1).toLocaleString("pt-BR") + "% da receita).",
        fazer: "Antes de baixar a diária para atrair reservas, simule o efeito na margem.", verificar: "Margem por noite e resultado no próximo período." });
    }
    return out;
  }

  /* ---------------- PILAR 6 · Experiência ---------------- */
  var ETAPAS = [
    ["antes", "Antes da reserva", "Resposta às perguntas"], ["confirmacao", "Confirmação", "Mensagem depois da reserva"], ["prechegada", "Pré-chegada", "Instruções e expectativa"],
    ["chegada", "Chegada", "Check-in e primeira impressão"], ["estadia", "Estadia", "Conforto e suporte"], ["checkout", "Check-out", "Saída sem atrito"], ["pos", "Pós-estadia", "Agradecimento e avaliação"]
  ];
  var MELHORIAS = [
    ["antes", "Responder consultas em até 1 hora, com mensagem-modelo"], ["confirmacao", "Mensagem de boas-vindas com o que esperar"], ["prechegada", "Guia de chegada com fotos do caminho e da entrada"],
    ["prechegada", "Perguntar a ocasião da viagem para preparar um detalhe"], ["chegada", "Check-in sem espera, com fechadura de senha ou cofre"], ["chegada", "Primeira impressão: luz acesa, cheiro bom, cama arrumada"],
    ["estadia", "Manual da casa curto, com Wi-Fi, regras e contatos"], ["estadia", "Kit simples de boas-vindas (café, água, algo local)"], ["estadia", "Lista de passeios e restaurantes testados por você"],
    ["checkout", "Check-out em 3 passos, sem tarefas pesadas"], ["pos", "Mensagem de agradecimento no dia da saída"], ["pos", "Pedido de avaliação com lembrete do que foi especial"]
  ];
  /* Prioridade = impacto × 2 − custo − esforço (cada um de 1 a 3). Critério explícito, de −4 a 4. */
  function prioridade(i, c, e) { i = +i; c = +c; e = +e; if (![i, c, e].every(function (x) { return x >= 1 && x <= 3; })) return null; return i * 2 - c - e; }
  function rankMelhorias(lista) {
    return (lista || []).map(function (m) { return Object.assign({}, m, { pontos: prioridade(m.impacto, m.custo, m.esforco) }); })
      .filter(function (m) { return m.pontos != null; }).sort(function (a, b) { return b.pontos - a.pontos || a.texto.localeCompare(b.texto); });
  }
  function etapasFrageis(aud) { return ETAPAS.filter(function (e) { return aud && aud[e[0]] === "falha"; }).map(function (e) { return e[1]; }); }

  /* ---------------- PILAR 7 · Plano de 30 dias ---------------- */
  function quadrante(impacto, esforco) {
    if (!impacto || !esforco) return null;
    if (impacto === "alto" && esforco === "baixo") return "Fazer primeiro";
    if (impacto === "alto" && esforco === "alto") return "Planejar";
    if (impacto === "baixo" && esforco === "baixo") return "Encaixar";
    return "Deixar para depois";
  }
  var ORDEM_Q = { "Fazer primeiro": 0, "Planejar": 1, "Encaixar": 2, "Deixar para depois": 3 };
  function validarCronograma(acoes) {
    var sel = (acoes || []).filter(function (a) { return a.selecionada; });
    var avisos = [], erros = [];
    if (!sel.length) erros.push("Selecione ao menos uma ação para o plano.");
    if (sel.length > 8) erros.push("Selecione no máximo 8 ações. Um plano com muitas frentes costuma não sair do papel.");
    var semSemana = sel.filter(function (a) { return !a.semana; });
    if (semSemana.length) erros.push("Defina a semana de: " + semSemana.map(function (a) { return a.texto; }).join("; ") + ".");
    [1, 2, 3, 4].forEach(function (s) {
      var da = sel.filter(function (a) { return +a.semana === s; });
      if (da.length > 3) avisos.push("A semana " + s + " tem " + da.length + " ações. Considere mover alguma para outra semana.");
      var porInd = {};
      da.forEach(function (a) { if (a.indicador) (porInd[a.indicador] = porInd[a.indicador] || []).push(a.texto); });
      Object.keys(porInd).forEach(function (k) { if (porInd[k].length > 1) avisos.push("Na semana " + s + ", " + porInd[k].length + " ações mexem no mesmo indicador (" + k + "). Separe em semanas diferentes para saber qual mudança funcionou."); });
    });
    var adiadas = sel.filter(function (a) { return a.quadrante === "Deixar para depois"; });
    if (adiadas.length) avisos.push("Você selecionou ação(ões) do quadrante \"Deixar para depois\": " + adiadas.map(function (a) { return a.texto; }).join("; ") + ".");
    return { valido: !erros.length, erros: erros, avisos: avisos, selecionadas: sel.slice().sort(function (a, b) { return (+a.semana || 9) - (+b.semana || 9) || (ORDEM_Q[a.quadrante] || 0) - (ORDEM_Q[b.quadrante] || 0); }) };
  }

  return { CARACTERISTICAS: CARACTERISTICAS, PUBLICOS: PUBLICOS, afinidade: afinidade, nomeCarac: nomeCarac, validarPerfil: validarPerfil,
    palavrasVagas: palavrasVagas, montarProposta: montarProposta, avaliarProposta: avaliarProposta, LIMITE_TITULO: LIMITE_TITULO,
    avaliarTitulo: avaliarTitulo, avaliarDescricao: avaliarDescricao, financeiro: financeiro, simular: simular, feedbackFinanceiro: feedbackFinanceiro,
    ETAPAS: ETAPAS, MELHORIAS: MELHORIAS, prioridade: prioridade, rankMelhorias: rankMelhorias, etapasFrageis: etapasFrageis,
    quadrante: quadrante, validarCronograma: validarCronograma };
});

/* Jornada 2 · Gestão · Módulo 4 · Marketing e vendas
   Lógica pura da ficha "A minha Marca e Captação". Sem DOM: roda no navegador (window.ZM) e no Node (testes).
   Regra: tudo que a ficha afirma sai daqui, para ser testado. Fontes: Panorama, Trilha B, Pilares G1 (Marca) e G4 (Captação),
   e Jornada do COMO, Etapas 05 (marca em uma folha, tom) e 07 (base de hóspedes, medição). Sem régua de mercado:
   custo por reserva, venda direta e ritmo da lista são aritmética declarada no PLANO. */
(function (raiz) {
  "use strict";

  var SITUACOES = [
    { v: "abrir", r: "Ainda vou abrir a minha hospedagem (vou usar números previstos)" },
    { v: "dono", r: "Já opero a minha hospedagem e quero vender mais sem depender só das plataformas" },
    { v: "operador", r: "Cuido da hospedagem de outra pessoa e presto contas ao dono" },
  ];

  // Diagnóstico de abertura: 4 perguntas Sim/Não → nível 1 a 4 (elaboração declarada no PLANO)
  var DIAG = [
    { id: "promessa", r: "A sua hospedagem tem uma promessa escrita em uma frase?" },
    { id: "lista", r: "Você guarda o contato dos hóspedes, com autorização, fora do celular?" },
    { id: "canal", r: "Você sabe por qual canal veio cada reserva do mês passado?" },
    { id: "custo", r: "Você sabe quanto custa, em média, uma reserva em cada canal?" },
  ];
  var SIMNAO = [{ v: "sim", r: "Sim" }, { v: "nao", r: "Não" }];
  var NIVEIS = [
    { n: 1, r: "Audiência alugada", t: "Hoje quem traz o hóspede é a plataforma, e ela decide quem vê você. Este módulo começa a sua audiência própria: uma promessa, uma lista com autorização e o custo de cada reserva." },
    { n: 2, r: "Começando", t: "Uma peça já existe. A ficha junta promessa, lista e custo por reserva numa página." },
    { n: 3, r: "Quase lá", t: "Falta uma peça: a promessa, a lista, o canal de cada reserva ou o custo. A ficha mostra qual." },
    { n: 4, r: "Captação com número", t: "Promessa, lista e números existem. Use a ficha para escrever tudo numa página e conferir a meta de venda direta." },
  ];
  function nivel(S) {
    var d = (S && S.diag) || {}, sim = 0;
    DIAG.forEach(function (q) { if (d[q.id] === "sim") sim++; });
    return NIVEIS[Math.max(0, sim - 1)];
  }

  // Os quatro testes da promessa (Etapa 05, Passo 02) e o teste das cinco pessoas (G1, passo 02)
  var TESTES = [
    { id: "recusa", r: "Recusa", p: "Alguém entende que não é para ele?" },
    { id: "cumprimento", r: "Cumprimento", p: "A hospedagem entrega isso toda vez?" },
    { id: "diferenca", r: "Diferença", p: "O vizinho poderia dizer a mesma frase? (Responda Sim se ele não poderia)" },
    { id: "memoria", r: "Memória", p: "Alguém repetiria essa frase ao recomendar?" },
  ];
  var CINCO = [{ v: "nt", r: "Ainda não testei" }, { v: "0", r: "0 de 5" }, { v: "1", r: "1 de 5" }, { v: "2", r: "2 de 5" }, { v: "3", r: "3 de 5" }, { v: "4", r: "4 de 5" }, { v: "5", r: "5 de 5" }];

  // Pontos de contato da promessa (G1, passo 04; Kit de Mensagens, Ferramenta 11)
  var PONTOS = [
    { id: "anuncio", r: "Anúncio das plataformas (título e foto de capa)", c: "o anúncio" },
    { id: "site", r: "Site ou página própria", c: "o site" },
    { id: "redes", r: "Perfil nas redes sociais", c: "as redes sociais" },
    { id: "whatsapp", r: "Resposta de WhatsApp", c: "a resposta de WhatsApp" },
    { id: "boasvindas", r: "Mensagem de boas-vindas (Kit de Mensagens, M04)", c: "a mensagem de boas-vindas" },
    { id: "placa", r: "Placa na entrada", c: "a placa na entrada" },
  ];
  var PONTO_OP = [{ v: "sim", r: "Já aparece" }, { v: "nao", r: "Não aparece" }, { v: "na", r: "Não tenho" }];

  var ONDE = [
    { v: "nuvem", r: "Planilha no computador ou na nuvem, com cópia" },
    { v: "semcopia", r: "Planilha, mas sem cópia de segurança" },
    { v: "celular", r: "Só no meu celular" },
    { v: "plataforma", r: "Só dentro das plataformas" },
    { v: "caderno", r: "Caderno ou papel" },
  ];
  var ONDE_R = {}; ONDE.forEach(function (o) { ONDE_R[o.v] = o.r; });
  var CANAIS_LISTA = ["WhatsApp", "E-mail"];
  var TIPOS = [{ v: "plataforma", r: "Plataforma (cobra comissão)" }, { v: "direto", r: "Direto (sem plataforma)" }];
  var NCANAIS = 6;

  // Adjetivos genéricos que a Etapa 05 manda cortar da promessa
  var ADJ = /\b(aconchegantes?|unic[oa]s?|especia(l|is)|exclusiv[oa]s?|inesquecive(l|is)|incrive(l|is)|perfeit[oa]s?)\b/g;
  function semAcento(s) { return String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function adjetivos(txt) { var m = semAcento(txt).match(ADJ) || []; var u = []; m.forEach(function (x) { if (u.indexOf(x) < 0) u.push(x); }); return u; }

  // Exemplo didático · dados fictícios (Cabanas do Vale, outubro de 2026, coerente com os Módulos 0, 1 e 2:
  // 25 reservas, R$ 16.240,00 de hospedagem; mix do Módulo 3: Plataforma A 50% (16%), Plataforma B 20% (15%), venda direta 30%;
  // comissão média 11,0% sobre o total, como no Módulo 2; meta de venda direta 30% → 40% até 30/06/2027, como nos Módulos 1 e 3)
  var EXEMPLO = {
    situacao: "dono", hospedagem: "Cabanas do Vale (exemplo)", diag: { promessa: "nao", lista: "nao", canal: "nao", custo: "nao" },
    publico: "Casais que vêm de carro, de até três horas de distância, para duas ou três noites.",
    naoPublico: "Grupos, festas e quem procura agito à noite.",
    promessa: "Duas noites a dois, com a lareira acesa e o vale na janela da cama, sem vizinho à vista.",
    testes: { recusa: "sim", cumprimento: "sim", diferenca: "sim", memoria: "sim" }, cinco: "4",
    prova: "Foto de capa: a cama de frente para a janela do vale, com a lareira acesa ao lado.",
    tom: "Próximo, concreto, calmo.",
    banidas: "aconchegante, único, inesquecível, refúgio, experiência única",
    nunca: "Não aceitamos festas nem mais de duas pessoas por cabana.",
    pontos: { anuncio: "sim", site: "nao", redes: "sim", whatsapp: "nao", boasvindas: "nao", placa: "nao" },
    contatos: 64, autorizados: 0, onde: "celular", acesso: "Só a Ana", canalLista: "WhatsApp",
    frase: "Posso guardar o seu WhatsApp e o seu e-mail para avisar quando abrirmos datas e condições? Você pode sair quando quiser.",
    metaLista: 120, estadiasMes: 25,
    mesCanais: "Outubro de 2026",
    canais: [
      { nome: "Plataforma A", tipo: "plataforma", comissao: 16, gasto: 0, reservas: 12, receita: 8120 },
      { nome: "Plataforma B", tipo: "plataforma", comissao: 15, gasto: 0, reservas: 5, receita: 3248 },
      { nome: "Instagram com impulsionamento", tipo: "direto", comissao: 0, gasto: 150, reservas: 2, receita: 1120 },
      { nome: "Hóspede que volta (WhatsApp)", tipo: "direto", comissao: 0, gasto: 0, reservas: 3, receita: 1848 },
      { nome: "Indicação", tipo: "direto", comissao: 0, gasto: 0, reservas: 3, receita: 1904 },
      { nome: "", tipo: "", comissao: "", gasto: "", reservas: "", receita: "" },
    ],
    metaDireta: 40, prazoMeta: "2027-06-30",
  };

  // Converte "1.234,56", "1234.56", "13.000", "-500", 1234 em número; vazio ou inválido vira null (versão corrigida do Módulo 1)
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
  function dataValida(v) { var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(v || "")); if (!m) return false; var d = new Date(+m[1], +m[2] - 1, +m[3]); return d.getFullYear() === +m[1] && d.getMonth() === +m[2] - 1 && d.getDate() === +m[3]; }
  function dataBR(v) { return dataValida(v) ? String(v).split("-").reverse().join("/") : ""; }
  function juntar(a) { return a.length < 2 ? a.join("") : a.slice(0, -1).join(", ") + " e " + a[a.length - 1]; }
  function letras(v) { return String(v == null ? "" : v).replace(/[^A-Za-zÀ-ÿ]/g, "").length; }
  function inteiro(v) { var n = num(v); return n != null && n === Math.floor(n); }

  function canaisPreenchidos(S) {
    return ((S && S.canais) || []).filter(function (c) { return c && informado(c.nome); });
  }
  function linhaTocada(c) { return c && ["tipo", "comissao", "gasto", "reservas", "receita"].some(function (k) { return informado(c[k]); }); }

  // Bloqueios por tela (impedem avançar) e avisos (não impedem)
  function validar(S, tela) {
    S = S || {}; var erros = [], avisos = [];
    var t = function (x) { return !tela || tela === x; };
    if (t("marca")) {
      if (letras(S.publico) < 3) erros.push("Escreva para quem é a sua hospedagem.");
      if (!informado(S.naoPublico)) avisos.push("Escreva também quem não é o seu hóspede: uma hospedagem que aceita tudo não promete nada.");
      if (letras(S.promessa) < 10) erros.push("Escreva a promessa em uma frase (pelo menos 10 letras).");
      var ts = S.testes || {};
      TESTES.forEach(function (q) { if (!ts[q.id]) erros.push("Responda o teste da " + q.r.toLowerCase() + "."); });
      if (!informado(S.cinco)) erros.push("Diga quantas de cinco pessoas de fora entenderam a frase (ou que ainda não testou).");
      var adj = adjetivos(S.promessa);
      if (adj.length) avisos.push("A promessa tem adjetivo genérico (" + adj.join(", ") + "). Troque por uma coisa concreta.");
    }
    if (t("prova")) {
      if (letras(S.prova) < 3) erros.push("Escreva a foto (ou a prova) que mostra a promessa.");
      if (letras(S.tom) < 3) erros.push("Escreva o tom de voz em três palavras.");
      if (!informado(S.banidas)) avisos.push("Liste as palavras que você nunca escreve: comece pelos adjetivos genéricos.");
      var p = S.pontos || {};
      if (PONTOS.some(function (x) { return !p[x.id]; })) erros.push("Marque, em cada ponto de contato, se a promessa já aparece.");
    }
    if (t("lista")) {
      var ct = num(S.contatos), au = num(S.autorizados), me = num(S.metaLista), es = num(S.estadiasMes);
      if (!informado(S.contatos)) erros.push("Falta quantos contatos de hóspedes você tem hoje (0 vale)."); else if (!inteiro(S.contatos) || ct < 0) erros.push("Contatos: use um número inteiro, 0 ou mais.");
      if (!informado(S.autorizados)) erros.push("Falta quantos desses têm autorização (0 vale)."); else if (!inteiro(S.autorizados) || au < 0) erros.push("Com autorização: use um número inteiro, 0 ou mais.");
      else if (ct != null && au > ct) erros.push("Com autorização não pode passar do total de contatos.");
      if (!ONDE_R[S.onde]) erros.push("Escolha onde a lista fica guardada.");
      if (letras(S.frase) < 10) erros.push("Escreva a frase que você vai usar para pedir a autorização (pelo menos 10 letras).");
      if (CANAIS_LISTA.indexOf(S.canalLista) < 0) erros.push("Escolha um canal para fazer bem: WhatsApp ou e-mail.");
      if (!informado(S.metaLista)) erros.push("Falta a meta de contatos com autorização daqui a 12 meses."); else if (!inteiro(S.metaLista) || me < 1) erros.push("Meta da lista: use um número inteiro a partir de 1.");
      else if (au != null && me < au) erros.push("A meta da lista não pode ser menor que os contatos com autorização de hoje.");
      if (!informado(S.estadiasMes)) erros.push("Faltam as estadias de um mês típico."); else if (!inteiro(S.estadiasMes) || es < 1 || es > 9999) erros.push("Estadias por mês: use um número inteiro de 1 a 9999.");
      if (!informado(S.acesso)) avisos.push("Escreva quem mais tem acesso à lista (ou \"só eu\").");
    }
    if (t("canais")) {
      if (!informado(S.mesCanais)) erros.push("Falta o mês dos números de canais.");
      var cs = (S.canais || []);
      cs.forEach(function (c, k) { if (c && !informado(c.nome) && linhaTocada(c)) erros.push("Canal " + (k + 1) + ": dê um nome ao canal ou apague a linha."); });
      var ok = canaisPreenchidos(S);
      if (!ok.length) erros.push("Preencha pelo menos um canal.");
      ok.forEach(function (c) {
        var n = String(c.nome).trim();
        if (!c.tipo || (c.tipo !== "plataforma" && c.tipo !== "direto")) erros.push(n + ": escolha se é plataforma ou direto.");
        if (!informado(c.reservas)) erros.push(n + ": faltam as reservas do mês (0 vale)."); else if (!inteiro(c.reservas) || num(c.reservas) < 0) erros.push(n + ": reservas é um número inteiro, 0 ou mais.");
        if (!informado(c.receita)) erros.push(n + ": falta a receita de hospedagem do canal (0 vale)."); else if (num(c.receita) == null || num(c.receita) < 0) erros.push(n + ": receita não pode ser negativa.");
        if (informado(c.comissao) && (num(c.comissao) == null || num(c.comissao) < 0 || num(c.comissao) >= 100)) erros.push(n + ": comissão de 0 a 99%.");
        if (informado(c.gasto) && (num(c.gasto) == null || num(c.gasto) < 0)) erros.push(n + ": gasto não pode ser negativo.");
        if (c.tipo === "plataforma" && !informado(c.comissao)) avisos.push(n + ": sem a comissão, o custo da plataforma fica zerado.");
        if (num(c.reservas) === 0 && num(c.receita) > 0) erros.push(n + ": tem receita sem reserva. Confira.");
      });
      var r = calcular(S);
      if (ok.length && r.reservas === 0) erros.push("Nenhuma reserva no mês: lance as reservas de cada canal.");
      if (ok.length && r.reservas > 0 && !(r.receita > 0)) erros.push("A receita de hospedagem do mês precisa ser maior que zero.");
      if (ok.length && !ok.some(function (c) { return c.tipo === "direto"; })) avisos.push("Nenhum canal direto: a venda direta hoje é zero, e tudo bem anotar isso.");
    }
    if (t("meta")) {
      var m = num(S.metaDireta);
      if (!informado(S.metaDireta)) erros.push("Falta a meta de venda direta."); else if (m == null || m <= 0 || m > 100) erros.push("Meta de venda direta: de 0 a 100%, maior que zero.");
      if (!informado(S.prazoMeta)) erros.push("Falta o prazo da meta (a data)."); else if (!dataValida(S.prazoMeta)) erros.push("Prazo: escolha uma data válida.");
    }
    var unicos = []; erros.forEach(function (x) { if (unicos.indexOf(x) < 0) unicos.push(x); });
    return { erros: unicos, avisos: avisos, ok: unicos.length === 0 };
  }

  function div(a, b) { return b ? a / b : null; }

  function calcular(S) {
    S = S || {};
    var linhas = canaisPreenchidos(S).map(function (c) {
      var rec = num(c.receita) || 0, res = num(c.reservas) || 0, com = num(c.comissao) || 0, gas = num(c.gasto) || 0;
      var comV = c.tipo === "plataforma" ? rec * com / 100 : 0;
      var custo = comV + gas;
      return { nome: String(c.nome).trim(), tipo: c.tipo, receita: rec, reservas: res, comissaoPct: com, comissaoValor: comV, gasto: gas, custo: custo,
        custoPorReserva: res > 0 ? custo / res : null, pctReceita: rec > 0 ? custo / rec : null };
    });
    var soma = function (f, filtro) { return linhas.filter(filtro || function () { return true; }).reduce(function (a, l) { return a + f(l); }, 0); };
    var receita = soma(function (l) { return l.receita; }), reservas = soma(function (l) { return l.reservas; }), custo = soma(function (l) { return l.custo; });
    var dir = function (l) { return l.tipo === "direto"; }, plat = function (l) { return l.tipo === "plataforma"; };
    var receitaDireta = soma(function (l) { return l.receita; }, dir), reservasDiretas = soma(function (l) { return l.reservas; }, dir);
    var receitaPlat = soma(function (l) { return l.receita; }, plat), comissaoPlat = soma(function (l) { return l.comissaoValor; }, plat);
    var custoDireto = soma(function (l) { return l.custo; }, dir);
    var vendaDireta = div(receitaDireta, receita);
    var meta = num(S.metaDireta);
    var receitaDiretaMeta = meta != null && receita > 0 ? receita * meta / 100 : null;
    var difMeta = receitaDiretaMeta != null ? receitaDiretaMeta - receitaDireta : null;
    var comissaoMediaPlat = div(comissaoPlat, receitaPlat);
    var comissaoEvitada = difMeta != null && difMeta > 0 && comissaoMediaPlat != null ? difMeta * comissaoMediaPlat : null;
    var comReserva = linhas.filter(function (l) { return l.reservas > 0; });
    var maisBarato = null, maisCaro = null;
    comReserva.forEach(function (l) { if (!maisBarato || l.custoPorReserva < maisBarato.custoPorReserva - 1e-9) maisBarato = l; if (!maisCaro || l.custoPorReserva > maisCaro.custoPorReserva + 1e-9) maisCaro = l; });
    // lista própria
    var ct = num(S.contatos), au = num(S.autorizados), ml = num(S.metaLista), es = num(S.estadiasMes);
    var faltam = ml != null && au != null ? Math.max(0, ml - au) : null;
    var porMes = faltam != null ? faltam / 12 : null;
    var pctEstadias = porMes != null && es ? porMes / es : null;
    // marca
    var ts = S.testes || {}, p = S.pontos || {};
    var testesSim = TESTES.filter(function (q) { return ts[q.id] === "sim"; }).length;
    var pontosFaltando = PONTOS.filter(function (x) { return p[x.id] === "nao"; });
    var pontosSim = PONTOS.filter(function (x) { return p[x.id] === "sim"; });
    return { linhas: linhas, receita: receita, reservas: reservas, custo: custo, custoPorReserva: div(custo, reservas), custoSobreReceita: div(custo, receita),
      receitaDireta: receitaDireta, reservasDiretas: reservasDiretas, custoDireto: custoDireto, custoPorReservaDireta: div(custoDireto, reservasDiretas),
      vendaDireta: vendaDireta, vendaDiretaReservas: div(reservasDiretas, reservas), receitaPlataformas: receitaPlat, comissaoPlataformas: comissaoPlat,
      comissaoMediaPlataformas: comissaoMediaPlat, metaDireta: meta, prazoMeta: dataBR(S.prazoMeta), receitaDiretaMeta: receitaDiretaMeta, difMeta: difMeta, comissaoEvitada: comissaoEvitada,
      maisBarato: maisBarato, maisCaro: maisCaro,
      contatos: ct, autorizados: au, pctAutorizados: ct ? au / ct : null, metaLista: ml, estadiasMes: es, faltamLista: faltam, porMesLista: porMes, pctEstadiasLista: pctEstadias,
      adjetivos: adjetivos(S.promessa), testesSim: testesSim, cinco: S.cinco, pontosFaltando: pontosFaltando, pontosSim: pontosSim };
  }

  // Formatação (sem DOM)
  function brl(v) { if (v == null || !isFinite(v)) return "sem dado"; var neg = v < 0; var s = Math.abs(v).toFixed(2).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, "."); return (neg ? "−R$ " : "R$ ") + s; }
  function dec(v, d) { if (v == null || !isFinite(v)) return "sem dado"; var neg = v < 0; var s = Math.abs(v).toFixed(d == null ? 1 : d).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d)(?=,|$))/g, "."); return (neg ? "−" : "") + s; }
  function pct(v, d) { if (v == null || !isFinite(v)) return "sem dado"; return dec(v * 100, d == null ? 1 : d) + "%"; }

  // Leituras (o que isso significa)
  function leituras(r, S) {
    S = S || {}; var out = [];
    if (r.maisBarato && r.maisCaro) out.push("Custo por reserva no mês: do mais barato, " + r.maisBarato.nome + " (" + brl(r.maisBarato.custoPorReserva) + "), ao mais caro, " + r.maisCaro.nome + " (" + brl(r.maisCaro.custoPorReserva) + "). Na média, cada reserva custou " + brl(r.custoPorReserva) + " para chegar, " + pct(r.custoSobreReceita) + " da receita de hospedagem.");
    out.push("Venda direta hoje: " + pct(r.vendaDireta) + " da receita de hospedagem (" + brl(r.receitaDireta) + " de " + brl(r.receita) + ", " + dec(r.reservasDiretas, 0) + " de " + dec(r.reservas, 0) + " reservas). A meta de " + dec(r.metaDireta, 1) + "%" + (r.prazoMeta ? " até " + r.prazoMeta : "") + " pede " + brl(r.receitaDiretaMeta) + " de venda direta num mês com a mesma receita" +
      (r.comissaoEvitada != null ? "; nesse mês, deixariam de sair cerca de " + brl(r.comissaoEvitada) + " de comissão (conta com os seus números, não previsão)." : "."));
    if (r.faltamLista != null) out.push("Lista própria: " + dec(r.autorizados, 0) + " contatos com autorização hoje, de " + dec(r.contatos, 0) + ". Chegar a " + dec(r.metaLista, 0) + " em 12 meses pede cerca de " + dec(r.porMesLista, 0) + " autorizações por mês" + (r.pctEstadiasLista != null ? ", " + pct(r.pctEstadiasLista, 0) + " das " + dec(r.estadiasMes, 0) + " estadias de um mês típico." : "."));
    out.push("Marca: a promessa passou em " + r.testesSim + " de 4 testes" + (r.cinco && r.cinco !== "nt" ? " e " + r.cinco + " de 5 pessoas de fora entenderam" : " e ainda não foi testada em cinco pessoas de fora") + ". Ela já aparece em " + r.pontosSim.length + " pontos de contato" + (r.pontosFaltando.length ? "; falta em " + r.pontosFaltando.length + ": " + juntar(r.pontosFaltando.map(function (x) { return x.c; })) + "." : "."));
    return out;
  }

  // Lê o Painel de Gestão do Módulo 1 (zion-t2-planejamento), se existir: ponto de partida e meta de venda direta
  function daPainel(P) {
    if (!P) return null;
    var b = num(P.base_vendaDireta), m = num(P.meta_vendaDireta);
    if (b == null && m == null) return null;
    return { base: b, meta: m };
  }

  // Atenção: regras em ordem (ids testados)
  function atencao(r, S, painel) {
    S = S || {}; var a = [];
    if (r.autorizados === 0) a.push({ id: "semAutorizacao", r: "A lista ainda não existe", t: (r.contatos ? "Você tem " + dec(r.contatos, 0) + " contatos, mas nenhum com autorização: eles não podem receber comunicação. " : "") + "Peça e-mail e WhatsApp no próximo check-in, com autorização explícita, e registre a resposta." });
    if (S.onde === "celular" || S.onde === "plataforma" || S.onde === "semcopia" || S.onde === "caderno") a.push({ id: "guardada", r: "A lista mora num lugar que você pode perder", t: S.onde === "plataforma" ? "Contato que só existe dentro da plataforma não é seu e pode deixar de ser acessível. Registre em paralelo, numa planilha com cópia." : "A fonte pede guardar a lista num lugar que não seja o seu celular, com cópia de segurança. Uma base perdida é anos de trabalho perdidos." });
    if (r.adjetivos.length) a.push({ id: "adjetivo", r: "Promessa com adjetivo genérico", t: "A promessa usa " + r.adjetivos.join(", ") + ". Esses adjetivos aparecem em quase todo anúncio e não distinguem nada: troque por uma coisa concreta, o que acontece ali." });
    var ts = S.testes || {}; var falhou = TESTES.filter(function (q) { return ts[q.id] === "nao"; });
    if (falhou.length) a.push({ id: "testes", r: "A promessa falhou em " + falhou.length + " " + (falhou.length > 1 ? "testes" : "teste"), t: "Falhou em: " + falhou.map(function (q) { return q.r.toLowerCase(); }).join(", ") + ". Se qualquer um dos quatro testes falhar, reescreva a frase." });
    if (S.cinco === "nt") a.push({ id: "cinco", r: "Promessa ainda não testada", t: "Mostre a frase a cinco pessoas que não conhecem a hospedagem. Se precisarem perguntar o que é, a frase ainda não existe." });
    else if (informado(S.cinco) && num(S.cinco) < 5) a.push({ id: "cinco", r: "Nem todos entenderam a promessa", t: S.cinco + " de 5 pessoas de fora entenderam sem perguntar. Se precisarem perguntar o que é, a frase ainda não existe: reescreva e teste de novo." });
    var platMin = null; r.linhas.forEach(function (l) { if (l.tipo === "plataforma" && l.reservas > 0 && (platMin == null || l.custoPorReserva < platMin.custoPorReserva)) platMin = l; });
    var caros = r.linhas.filter(function (l) { return l.tipo === "direto" && l.gasto > 0 && l.reservas > 0 && platMin && l.custoPorReserva > platMin.custoPorReserva + 1e-9; });
    if (caros.length) a.push({ id: "caroDireto", r: "Esforço direto mais caro que a plataforma", t: caros.map(function (l) { return l.nome + " custou " + brl(l.custoPorReserva) + " por reserva"; }).join("; ") + ", mais que " + platMin.nome + " (" + brl(platMin.custoPorReserva) + "). Meça mais um mês antes de aumentar o gasto: sem o custo por reserva, investir em captação é aposta." });
    var semRes = r.linhas.filter(function (l) { return l.custo > 0 && l.reservas === 0; });
    if (semRes.length) a.push({ id: "gastoSemReserva", r: "Gasto sem reserva", t: semRes.map(function (l) { return l.nome + " (" + brl(l.custo) + ")"; }).join(", ") + ": houve gasto e nenhuma reserva no mês. Confira se a reserva foi anotada no canal certo; se foi, reveja esse esforço." });
    if (r.metaDireta != null && r.vendaDireta != null && r.metaDireta / 100 <= r.vendaDireta + 1e-9) a.push({ id: "metaAbaixo", r: "Meta de venda direta não passa da atual", t: "A meta (" + dec(r.metaDireta, 1) + "%) não passa da venda direta de hoje (" + pct(r.vendaDireta) + "). Manter pode ser decisão; se for, escreva o porquê. Se não, suba a meta." });
    if (painel && painel.meta != null && r.metaDireta != null && Math.abs(painel.meta - r.metaDireta) > 0.05) a.push({ id: "painel", r: "Meta diferente do seu Painel de Gestão", t: "No Painel do Módulo 1 a meta de venda direta é " + dec(painel.meta, 1) + "%; aqui está " + dec(r.metaDireta, 1) + "%. Use o mesmo número nos dois, para a reunião semanal olhar uma meta só." });
    if (r.pctEstadiasLista != null && r.pctEstadiasLista > 1 + 1e-9) a.push({ id: "ritmo", r: "Meta da lista maior que o número de hóspedes", t: "A meta pede " + dec(r.porMesLista, 0) + " autorizações por mês, mais que as " + dec(r.estadiasMes, 0) + " estadias de um mês típico. Reduza a meta ou conte com outra entrada além do check-in." });
    return a;
  }
  var ERRO_COMUM = "Trocar a lista própria por seguidores. Seguidor é audiência emprestada: a plataforma decide quantos deles veem você, e essa decisão muda sem aviso.";

  // O que fazer: o plano sugerido (texto editável da ação)
  function planoSugerido(S, r) {
    S = S || {}; r = r || calcular(S); var p = [];
    p.push("No próximo check-in, pedir o contato com a autorização: \"" + String(S.frase || "").trim().replace(/"/g, "'").replace(/\.$/, "") + "\". Registrar na aba Lista própria da planilha (oito campos), num lugar que não seja o celular, com cópia de segurança.");
    p.push("Perguntar a todo hóspede como chegou e anotar o canal de cada reserva. No fim do mês, recalcular o custo por reserva na aba Captação do mês.");
    if (r.pontosFaltando.length) p.push("Levar a promessa para " + juntar(r.pontosFaltando.map(function (x) { return x.c; })) + (r.pontosFaltando.some(function (x) { return x.id === "boasvindas" || x.id === "whatsapp"; }) ? " (o Kit de Mensagens, Ferramenta 11, já tem as mensagens de boas-vindas e de agradecimento para ajustar ao seu tom)" : "") + ".");
    if (S.cinco !== "5") p.push("Testar a promessa com cinco pessoas de fora e reescrever até ninguém precisar perguntar o que é.");
    p.push("Fazer bem um canal só, o " + (S.canalLista || "WhatsApp") + ": os quatro contatos do ano para quem autorizou (agradecimento, aniversário da estadia, abertura de temporada e oferta de baixa), sempre com o caminho de reserva direta.");
    var a = atencao(r, S);
    var caro = a.filter(function (x) { return x.id === "caroDireto"; })[0];
    if (caro) p.push("Não aumentar o gasto do esforço mais caro antes de medir mais um mês.");
    p.push("Na reunião semanal do Painel (Módulo 1), olhar a venda direta contra a meta de " + dec(r.metaDireta, 1) + "%.");
    return p.map(function (x, k) { return (k + 1) + ". " + x; }).join("\n");
  }
  function comoVerificar(r, S) {
    var t = "Daqui a 30 dias, a aba Lista própria tem uma linha por estadia do mês, com a autorização registrada (sim ou não), e a aba Captação do mês tem o canal de cada reserva e o custo por reserva calculado.";
    if (r && r.pontosFaltando.length) t += " A promessa já aparece nos pontos de contato que faltavam.";
    t += " Todo mês, lance o mês na aba Captação 12 meses: a venda direta do mesmo mês do ano seguinte é comparada com a meta.";
    return t;
  }

  // Ficha preenchida e lição concluída (selo)
  var TELAS = ["abertura", "marca", "prova", "lista", "canais", "meta", "resultado"];
  var TITULOS = { marca: "Para quem e a promessa", prova: "A prova e o tom", lista: "A lista própria", canais: "Os canais e o custo por reserva", meta: "A meta de venda direta" };
  function completo(S) {
    S = S || {};
    if (!S.situacao) return false;
    return ["marca", "prova", "lista", "canais", "meta"].every(function (t) { return validar(S, t).ok; });
  }
  function acaoOk(S) { return !!(S && S.acao && letras(S.acao) >= 10); }
  function concluido(S) { return completo(S) && acaoOk(S) && !!(S && S.prazo) && !!(S && S.pdf); }
  function pendencias(S) {
    var p = [];
    if (!completo(S)) p.push("a ficha preenchida (marca, lista, canais e meta)");
    if (!acaoOk(S)) p.push("o plano com pelo menos 10 letras");
    if (!(S && S.prazo)) p.push("a data do primeiro check-in com o pedido de autorização");
    if (!(S && S.pdf)) p.push("o PDF baixado");
    return p;
  }
  function proximaVazia(S) {
    for (var k = 1; k < TELAS.length - 1; k++) if (!validar(S, TELAS[k]).ok) return TELAS[k];
    return "resultado";
  }

  // A marca em uma folha (quatro linhas obrigatórias e uma opcional)
  function folha(S) {
    S = S || {};
    var f = [
      { id: "publico", r: "Para quem", t: String(S.publico || "").trim() + (informado(S.naoPublico) ? " Não é para: " + String(S.naoPublico).trim() : "") },
      { id: "promessa", r: "Promessa", t: String(S.promessa || "").trim() },
      { id: "prova", r: "Prova", t: String(S.prova || "").trim() },
      { id: "tom", r: "Tom", t: String(S.tom || "").trim() + (informado(S.banidas) ? " Nunca escrevemos: " + String(S.banidas).trim() + "." : "") },
    ];
    if (informado(S.nunca)) f.push({ id: "nunca", r: "O que nunca fazemos", t: String(S.nunca).trim() });
    return f;
  }

  var PROXIMO = { n: 5, t: "Pessoas e organização das áreas" };
  var api = { SITUACOES: SITUACOES, DIAG: DIAG, SIMNAO: SIMNAO, NIVEIS: NIVEIS, TESTES: TESTES, CINCO: CINCO, PONTOS: PONTOS, PONTO_OP: PONTO_OP, ONDE: ONDE, ONDE_R: ONDE_R,
    CANAIS_LISTA: CANAIS_LISTA, TIPOS: TIPOS, NCANAIS: NCANAIS, EXEMPLO: EXEMPLO, TELAS: TELAS, TITULOS: TITULOS, PROXIMO: PROXIMO, ERRO_COMUM: ERRO_COMUM,
    num: num, dataBR: dataBR, adjetivos: adjetivos, validar: validar, calcular: calcular, leituras: leituras, atencao: atencao, planoSugerido: planoSugerido, comoVerificar: comoVerificar,
    completo: completo, concluido: concluido, pendencias: pendencias, proximaVazia: proximaVazia, nivel: nivel, folha: folha, daPainel: daPainel,
    brl: brl, dec: dec, pct: pct };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else raiz.ZM = api;
})(typeof window !== "undefined" ? window : this);

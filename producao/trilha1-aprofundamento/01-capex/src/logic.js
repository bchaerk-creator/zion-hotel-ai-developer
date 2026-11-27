/* Trilha 1 · Aprofundamento do Pilar 6 · Lição 01 · CAPEX
   Ficha "Faça agora · O meu CAPEX" (página 6A do Dossiê de Desenvolvimento).
   Lógica pura, sem DOM: roda no navegador (window.ZCAPEX) e no Node (testes).
   Regra: toda conta, alerta e texto de leitura que a ficha mostra sai daqui, para ser testado.
   Fonte das regras: producao/trilha1-aprofundamento/01-capex/PLANO.md, seção 6.
   "Não sei" é sempre o texto "nao_sei", nunca um zero escondido. */
(function (raiz) {
  "use strict";

  /* ------------------------------------------------------------------
     1. Leitura e formatação pt-BR (as mesmas regras da ficha do Pilar 6)
     ------------------------------------------------------------------ */
  var NS = "nao_sei";
  function falta(v) {
    if (v === undefined || v === null) return true;
    if (v === NS) return true;
    if (typeof v === "string") return v.trim() === "" || v.trim().toLowerCase() === NS;
    if (Array.isArray(v)) return v.length === 0;
    if (typeof v === "number") return !Number.isFinite(v);
    return false;
  }
  function paraNumero(v) {
    if (falta(v)) return null;
    if (typeof v === "number") return Number.isFinite(v) ? v : null;
    if (typeof v !== "string") return null;
    var s = v.replace(/R\$|%|\s/g, "");
    if (s === "") return null;
    if (s.indexOf(",") >= 0) s = s.replace(/\./g, "").replace(",", ".");
    else { var pontos = (s.match(/\./g) || []).length; if (pontos > 1 || /^-?\d{1,3}\.\d{3}$/.test(s)) s = s.replace(/\./g, ""); }
    if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
    var n = Number(s);
    return Number.isFinite(n) ? n : null;
  }
  /** Arredonda sem o erro de vírgula flutuante e, no empate exato, para o par (como o Pilar 6). */
  function arred(x, casas) {
    if (casas === undefined) casas = 2;
    var f = Math.pow(10, casas); var y = Number((Math.abs(x) * f).toPrecision(12));
    var i = Math.floor(y); var d = y - i;
    if (Math.abs(d - 0.5) < 1e-7) { if (i % 2 !== 0) i += 1; } else i = Math.round(y);
    var r = i / f; var res = x < 0 ? -r : r; return Object.is(res, -0) ? 0 : res;
  }
  function agrupar(i) { return i.replace(/\B(?=(\d{3})+(?!\d))/g, "."); }
  function fmtNum(x, casas) { if (casas === undefined) casas = 2; var r = arred(x, casas); var p = Math.abs(r).toFixed(casas).split("."); return (r < 0 ? "-" : "") + agrupar(p[0]) + (casas > 0 ? "," + p[1] : ""); }
  function fmtN(x, casasMax) { var s = fmtNum(x, casasMax === undefined ? 2 : casasMax); return s.indexOf(",") >= 0 ? s.replace(/,?0+$/, "") : s; }
  function brl(x) { if (typeof x !== "number" || !Number.isFinite(x)) return "em branco"; var r = arred(x, 2); return (r < 0 ? "-" : "") + "R$ " + fmtNum(Math.abs(r), 2); }
  function brl0(x) { if (typeof x !== "number" || !Number.isFinite(x)) return "em branco"; var r = arred(x, 0); return (r < 0 ? "-" : "") + "R$ " + fmtNum(Math.abs(r), 0); }
  function fmtPct(frac, casas) { if (typeof frac !== "number" || !Number.isFinite(frac)) return "não se calcula"; return fmtNum(frac * 100, casas === undefined ? 1 : casas) + "%"; }
  function juntar(itens) { if (!itens.length) return ""; if (itens.length === 1) return itens[0]; return itens.slice(0, -1).join(", ") + " e " + itens[itens.length - 1]; }
  function div(a, b) { if (typeof a !== "number" || typeof b !== "number" || !Number.isFinite(a) || !Number.isFinite(b) || b === 0) return null; var q = a / b; return Number.isFinite(q) ? q : null; }
  function ehNS(v) { return v === NS; }
  function txt(v) { return typeof v === "string" ? v.trim() : ""; }
  function inteiro(v) { var n = paraNumero(v); return n !== null && Math.floor(n) === n ? n : null; }
  var EPS = 1e-12;
  function entre(x, lo, hi) { return x >= lo - EPS && x <= hi + EPS; }
  function minusculaInicial(s) { s = txt(s); return s ? s.charAt(0).toLowerCase() + s.slice(1) : s; }

  /* Datas em "AAAA-MM-DD"; a lógica recebe "hoje" como parâmetro. */
  function dataOk(iso) { return typeof iso === "string" && /^\d{4}-\d{2}-\d{2}$/.test(iso) && !isNaN(Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10))); }
  function diaUTC(iso) { return Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10)); }
  function diasEntre(de, ate) { if (!dataOk(de) || !dataOk(ate)) return null; return Math.round((diaUTC(ate) - diaUTC(de)) / 86400000); }
  function somaDias(iso, n) { var d = new Date(diaUTC(iso) + n * 86400000); return d.toISOString().slice(0, 10); }
  function dataBR(iso) { return dataOk(iso) ? iso.split("-").reverse().join("/") : ""; }

  /* ------------------------------------------------------------------
     2. Dados da ficha (perguntas, opções, blocos, linhas sugeridas)
     ------------------------------------------------------------------ */
  var SITUACOES = [
    { v: "abrir", r: "Tenho terreno e ainda não construí", jornada: "Quero começar" },
    { v: "ampliar", r: "Já opero e vou ampliar (nova unidade, fase dois ou área comum)", jornada: "Já opero" },
    { v: "operador", r: "Cuido da hospedagem de outra pessoa e vou preparar o custo para o dono", jornada: "Já opero" },
  ];
  var TIPOS = [
    { v: "casa", r: "Casa ou apartamento" }, { v: "cabanas", r: "Cabanas ou chalés" }, { v: "glamping", r: "Glamping" },
    { v: "pousada", r: "Pousada" }, { v: "outro", r: "Outro" },
  ];
  var DIAG = [
    { id: "d1", p: "Você já tem um número para o custo do projeto?", op: [{ v: "numero", r: "Tenho um número com cotações" }, { v: "palpite", r: "Tenho um palpite" }, { v: "nao", r: "Não tenho" }] },
    { id: "d2", p: "Esse número inclui infraestrutura, mobília, enxoval, pré-abertura e reserva?", op: [{ v: "tudo", r: "Inclui tudo" }, { v: "alguns", r: "Inclui alguns" }, { v: "soUnidade", r: "Só a unidade" }, { v: "naoSei", r: "Não sei" }] },
    { id: "d3", p: "Quantas linhas do seu orçamento têm cotação escrita?", op: [{ v: "maioria", r: "A maioria" }, { v: "algumas", r: "Algumas" }, { v: "nenhuma", r: "Nenhuma" }] },
    { id: "d4", p: "Você tem uma regra escrita para usar a reserva do imprevisto?", op: [{ v: "sim", r: "Sim" }, { v: "nao", r: "Não" }] },
  ];
  var FATORES = [
    { v: "remoto", r: "Território remoto" },
    { v: "sistemaNovo", r: "Sistema construtivo novo para a equipe" },
    { v: "importados", r: "Itens importados" },
    { v: "areaSensivel", r: "Licenciamento em área sensível" },
    { v: "prazoTemporada", r: "Prazo apertado pela temporada" },
  ];
  var ORIGENS = [
    { v: "cotacao", r: "Cotação escrita", notaP6: 3 },
    { v: "estimativa", r: "Estimativa minha, sem cotação", notaP6: 1 },
    { v: "branco", r: "Em branco, ainda sem número", notaP6: 0 },
    { v: "naoAplica", r: "Não se aplica", notaP6: null },
  ];
  var MODOS = [
    { v: "valor", r: "Valor total" },
    { v: "qtdUnit", r: "Quantidade × valor de cada" },
    { v: "area", r: "Quantidade × área × custo do m²" },
  ];
  var FORMAS = [
    { v: "construida", r: "Construída (por área × custo do m²)", modo: "area" },
    { v: "pronta", r: "Estrutura pronta (preço por unidade)", modo: "qtdUnit" },
    { v: "adequacao", r: "Imóvel existente a adequar (por unidade)", modo: "qtdUnit" },
  ];
  var TAGS = ["unidade", "deck", "piso", "luz", "agua", "mobilia"];
  var TERRENO = [
    { v: "meu", r: "Já é meu" }, { v: "comprar", r: "Vou comprar" },
    { v: "parceria", r: "Permuta, sociedade ou arrendamento" }, { v: "naoSei", r: "Não sei" },
  ];
  var BLOCOS = [
    { n: 1, nome: "Projetos, licenças e documentação" },
    { n: 2, nome: "Infraestrutura" },
    { n: 3, nome: "Unidades e áreas comuns", nomePronto: "Adequação e reforma" },
    { n: 4, nome: "Mobiliário e equipamentos" },
    { n: 5, nome: "Enxoval, utensílios e suprimentos" },
    { n: 6, nome: "Pré-abertura" },
    { n: 7, nome: "Reserva do imprevisto" },
  ];
  function nomeBloco(n, E) { var b = BLOCOS[n - 1]; return n === 3 && E && E.imovelPronto === true ? b.nomePronto : b.nome; }
  var REGUA = [
    { v: "Sonhador", t: "Ainda é um sonho com preço: falta montar a conta bloco por bloco." },
    { v: "Estimador", t: "A conta existe, mas a maior parte dela ainda é estimativa ou está em branco." },
    { v: "Calculista", t: "A maioria das linhas tem cotação escrita, e as três maiores também." },
    { v: "Developer", t: "Não é atribuído nesta ficha: ele pede cronograma de desembolso e captação, que ficam no Pilar 7." },
  ];
  var LIMITES = { dinheiroMax: 100000000, unidadesMax: 200, linhasMax: 15, tipologiasMax: 3, areaMin: 0.1, areaMax: 10000, distMax: 50000, redeMax: 999, giroMesesMax: 24, camasMax: 10, reservaMax: 50, validadeDias: 90, prazoDias: 30 };

  /* Linhas sugeridas: somente nomes, nunca valor (PLANO 6.1). */
  var _seq = 0;
  function novaLinha(o) {
    _seq += 1;
    var l = { id: o.id || ("l" + Date.now().toString(36) + _seq), nome: o.nome || "", modo: o.modo || "valor", qtd: "", valor: "", valorUnit: "", areaM2: "", custoM2: "", origem: null, nCotacoes: null, mesmaEspec: false, dataCotacao: "", tagP6: o.tagP6 || null };
    if (o.porUnidade) l.porUnidade = true;
    if (o.tipologia) { l.tipologia = true; l.forma = o.forma || "construida"; l.modo = (FORMAS.filter(function (f) { return f.v === l.forma; })[0] || FORMAS[0]).modo; l.tagP6 = "unidade"; l.porUnidade = true; l.freteMontagemConfirmados = false; }
    if (o.enxoval) { l.enxoval = true; l.modo = "enxoval"; l.camasPorUnidade = ""; l.custoJogo = ""; }
    return l;
  }
  function linhasSugeridas(b, E) {
    E = E || {};
    var pu = function (nome, tag) { return { nome: nome, modo: "qtdUnit", porUnidade: true, tagP6: tag || null }; };
    var v = function (nome) { return { nome: nome, modo: "valor" }; };
    var L;
    if (b === 1) L = [v("Arquitetura"), v("Engenharias (estrutural, elétrica, hidrossanitária)"), v("Levantamento do terreno"), v("Aprovações e taxas da prefeitura"), v("Licença ambiental, se houver")];
    else if (b === 2) {
      L = [v("Acesso e caminhos"), v("Energia (rede comum até as unidades)"), v("Água"), v("Esgoto e tratamento"), v("Drenagem"), v("Internet"), v("Estacionamento"), pu("Ligação de luz de cada unidade", "luz"), pu("Água e esgoto de cada unidade", "agua")];
      if (E.situacao === "ampliar" || E.situacao === "operador") L.unshift(v("Reforço da rede existente"));
    } else if (b === 3) {
      if (E.imovelPronto === true) L = [{ nome: "Adequação de cada unidade", tipologia: true, forma: "adequacao" }, v("Áreas comuns a adequar")];
      else L = [{ nome: "Unidade tipo 1", tipologia: true, forma: E.tipo === "glamping" ? "pronta" : "construida" }, pu("Deck de cada unidade", "deck"), pu("Piso de cada unidade (se não estiver no m²)", "piso"),
        { nome: "Apoio e lavanderia", modo: "area" }, v("Recepção"), v("Cozinha"), v("Deck comum"), v("Trilhas"), v("Casa de máquinas")];
    } else if (b === 4) L = [pu("Cama e colchão (unidade-modelo)", "mobilia"), pu("Mobiliário (unidade-modelo)", "mobilia"), pu("Iluminação (unidade-modelo)", "mobilia"), pu("Cozinha compacta e eletrodomésticos (unidade-modelo)", "mobilia"), pu("Banheiro (unidade-modelo)", "mobilia"), v("Equipamentos da lavanderia e das áreas comuns")];
    else if (b === 5) L = [{ nome: "Enxoval (três jogos por cama)", enxoval: true, tagP6: "mobilia" }, pu("Utensílios de cozinha de cada unidade", "mobilia"), v("Governança e limpeza"), v("Recepção"), v("Manutenção"), v("Segurança")];
    else if (b === 6) L = [v("Licença de funcionamento e cadastros"), v("Fotos e site"), v("Identidade e marketing de lançamento"), v("Treinamento e contratação"), v("Seguro do primeiro ano"), v("Abertura de teste")];
    else L = [];
    return L.map(function (o) { if (b === 5 && !o.tagP6) o.tagP6 = "mobilia"; return novaLinha(o); });
  }
  function estadoInicial(hoje) {
    return {
      nome: "", projeto: "", situacao: null, tipo: null, imovelPronto: false, d1: null, d2: null, d3: null, d4: null, turma: "autonomo",
      palpite: "", dataPalpite: "", unidadesFase: "", unidadesProjeto: "", fatoresRisco: [], primeiraObra: null,
      blocos: { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [] },
      distanciaEnergiaM: "", infraDimensionadaPara: "", infraProjetoCompleto: "", enxovalNaoDuplicado: false,
      contingenciaPct: "", regraParaQue: "", regraQuemAutoriza: "", regraComoRegistra: "", regraQuandoConfere: "",
      giro: "", giroMeses: "", giroCustoMensal: "", giroZeroJustificativa: "", terrenoSituacao: null, terrenoValor: "",
      acao30: "", acaoEditada: false, prazo: "", verificacao: "", pdfBaixado: false, exemplo: false, hoje: hoje || "",
    };
  }

  /* ------------------------------------------------------------------
     3. Linhas: valor, validação, contagens
     ------------------------------------------------------------------ */
  function comValor(l) { return !!l && (l.origem === "cotacao" || l.origem === "estimativa"); }
  function ativa(l) { return !!l && l.origem !== "naoAplica"; }
  function dinheiroOk(x) { return x !== null && x > 0 && x <= LIMITES.dinheiroMax; }
  function qtdDe(l, E) {
    var q = inteiro(l.qtd);
    if (q === null && falta(l.qtd) && l.porUnidade) q = inteiro(E.unidadesFase);
    return q;
  }
  function areaDe(l) { var a = paraNumero(l.areaM2); return a !== null && a >= LIMITES.areaMin && a <= LIMITES.areaMax ? a : null; }
  /** Valor de uma linha (PLANO 6.2). Em branco e não se aplica valem 0. Dado inválido devolve null. */
  function valorLinha(l, E) {
    if (!comValor(l)) return 0;
    if (l.enxoval) {
      var u = inteiro(E.unidadesFase), c = inteiro(l.camasPorUnidade), j = paraNumero(l.custoJogo);
      if (u === null || u < 1 || c === null || c < 1 || c > LIMITES.camasMax || !dinheiroOk(j)) return null;
      return u * c * 3 * j;
    }
    if (l.modo === "valor") { var v = paraNumero(l.valor); return dinheiroOk(v) ? v : null; }
    var q = qtdDe(l, E);
    if (q === null || q < 1 || q > LIMITES.unidadesMax) return null;
    if (l.modo === "qtdUnit") { var vu = paraNumero(l.valorUnit); return dinheiroOk(vu) ? q * vu : null; }
    if (l.modo === "area") { var a = areaDe(l), m = paraNumero(l.custoM2); return a !== null && dinheiroOk(m) ? q * a * m : null; }
    return null;
  }
  /** Mensagem de erro de uma linha, ou "" se ela está em ordem. */
  function erroLinha(l, E, hoje) {
    var n = txt(l.nome);
    if (n.length < 2 || n.length > 80) return "Dê um nome à linha (2 a 80 letras).";
    if (!l.origem) return "Diga de onde vem o número de \"" + n + "\": cotação, estimativa, em branco ou não se aplica.";
    if (!comValor(l)) return "";
    if (l.enxoval) {
      var c = inteiro(l.camasPorUnidade);
      if (c === null || c < 1 || c > LIMITES.camasMax) return "Em \"" + n + "\": escreva quantas camas cada unidade tem (1 a 10).";
      if (!dinheiroOk(paraNumero(l.custoJogo))) return "Em \"" + n + "\": escreva o custo de um jogo (lençóis, toalhas e capa).";
      if (inteiro(E.unidadesFase) === null) return "Volte à tela da fase e escreva quantas unidades ela abre.";
    } else if (l.modo === "valor") {
      if (!dinheiroOk(paraNumero(l.valor))) return "Em \"" + n + "\": escreva um valor maior que zero e até R$ 100 milhões, ou marque Em branco.";
    } else {
      var q = qtdDe(l, E);
      if (q === null || q < 1 || q > LIMITES.unidadesMax) return "Em \"" + n + "\": a quantidade vai de 1 a 200, sem casas decimais.";
      if (l.modo === "qtdUnit" && !dinheiroOk(paraNumero(l.valorUnit))) return "Em \"" + n + "\": escreva o valor de cada um, maior que zero.";
      if (l.modo === "area") {
        if (areaDe(l) === null) return "Em \"" + n + "\": escreva a área em m² (0,1 a 10.000).";
        if (!dinheiroOk(paraNumero(l.custoM2))) return "Em \"" + n + "\": escreva o custo do m², maior que zero.";
      }
    }
    if (!falta(l.areaM2) && !ehNS(l.areaM2) && areaDe(l) === null) return "Em \"" + n + "\": a área vai de 0,1 a 10.000 m², ou marque Não sei.";
    if (l.origem === "cotacao") {
      if ([1, 2, 3].indexOf(Number(l.nCotacoes)) < 0) return "Em \"" + n + "\": diga quantas cotações você tem (1, 2 ou 3 ou mais).";
      if (!falta(l.dataCotacao)) {
        if (!dataOk(l.dataCotacao)) return "Em \"" + n + "\": a data da cotação não está no formato certo.";
        if (hoje && diasEntre(l.dataCotacao, hoje) < 0) return "Em \"" + n + "\": a data da cotação não pode ser no futuro.";
      }
    }
    return "";
  }
  function cotacaoCompleta(l) { return l.origem === "cotacao" && Number(l.nCotacoes) >= 3 && l.mesmaEspec === true; }
  function cotacaoVencida(l, hoje) { if (l.origem !== "cotacao" || !dataOk(l.dataCotacao) || !dataOk(hoje)) return false; return diasEntre(l.dataCotacao, hoje) > LIMITES.validadeDias; }
  function linhasDe(E, b) { return (E && E.blocos && Array.isArray(E.blocos[b])) ? E.blocos[b] : []; }
  function todasLinhas(E) { var r = []; for (var b = 1; b <= 6; b++) linhasDe(E, b).forEach(function (l) { r.push({ b: b, l: l }); }); return r; }
  function tipologias(E) { return linhasDe(E, 3).filter(function (l) { return l.tipologia && ativa(l); }); }
  function somaTipologias(E) { return tipologias(E).reduce(function (s, l) { var q = qtdDe(l, E); return s + (q || 0); }, 0); }
  function blocoInteiroNA(E, b) { var L = linhasDe(E, b); return L.length > 0 && L.every(function (l) { return l.origem === "naoAplica"; }); }
  function bloco2Ativo(E) { return linhasDe(E, 2).some(ativa); }
  /** A17: as tipologias precisam somar as unidades da fase (salvo imóvel pronto sem tipologia). */
  function tipologiasConferem(E) {
    var u = inteiro(E.unidadesFase);
    var tip = tipologias(E);
    if (E.imovelPronto === true && tip.length === 0) return true;
    if (u === null) return false;
    return somaTipologias(E) === u;
  }
  function giroUsado(E) {
    var m = paraNumero(E.giroMeses), c = paraNumero(E.giroCustoMensal);
    if (m !== null && c !== null) return m * c;
    if (ehNS(E.giro)) return null;
    return paraNumero(E.giro);
  }
  function reservaPct(E) { var p = paraNumero(E.contingenciaPct); return p !== null && p > 0 ? p : 0; }
  function temFator(E) { return Array.isArray(E.fatoresRisco) && E.fatoresRisco.length > 0; }

  /* ------------------------------------------------------------------
     4. O cálculo (PLANO 6.2)
     ------------------------------------------------------------------ */
  function calcular(E, hoje) {
    E = E || {};
    hoje = hoje || E.hoje || "";
    var C = { totalBloco: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0 }, linhasInvalidas: [] };
    var todas = todasLinhas(E);
    var valorados = [];
    var nLinhas = 0, nCotadas = 0, nEstimadas = 0, nBranco = 0, valorCotado = 0, valorEstimado = 0;
    var n3 = 0, nInc = 0, vencidas = [], incompletas = [], brancos = [];
    var porBloco = {};
    for (var b = 1; b <= 6; b++) porBloco[b] = { nLinhas: 0, nCotadas: 0, nComValor: 0, nAtivas: 0 };
    todas.forEach(function (x) {
      var l = x.l, pb = porBloco[x.b];
      var v = valorLinha(l, E);
      if (v === null) { C.linhasInvalidas.push({ b: x.b, nome: txt(l.nome) }); v = 0; }
      C.totalBloco[x.b] += v;
      if (ativa(l) && l.origem) pb.nAtivas += 1;
      if (l.origem === "cotacao" || l.origem === "estimativa" || l.origem === "branco") { nLinhas += 1; pb.nLinhas += 1; }
      if (comValor(l) && v > 0) { pb.nComValor += 1; valorados.push({ b: x.b, nome: txt(l.nome), valor: v, origem: l.origem }); }
      if (l.origem === "cotacao") {
        nCotadas += 1; pb.nCotadas += 1; valorCotado += v;
        if (cotacaoCompleta(l)) n3 += 1; else { nInc += 1; incompletas.push({ b: x.b, nome: txt(l.nome), n: Number(l.nCotacoes) || 0 }); }
        if (cotacaoVencida(l, hoje)) vencidas.push({ b: x.b, nome: txt(l.nome), dias: diasEntre(l.dataCotacao, hoje) });
      } else if (l.origem === "estimativa") { nEstimadas += 1; valorEstimado += v; }
      else if (l.origem === "branco") { nBranco += 1; brancos.push({ b: x.b, nome: txt(l.nome) }); }
    });
    var subtotal = 0; for (b = 1; b <= 6; b++) subtotal += C.totalBloco[b];
    var pct = reservaPct(E);
    var contingencia = subtotal * pct / 100;
    C.totalBloco[7] = contingencia;
    var capexFase = subtotal + contingencia;
    var pctBloco = {}; for (b = 1; b <= 7; b++) pctBloco[b] = capexFase > 0 ? C.totalBloco[b] / capexFase : null;
    var obra = C.totalBloco[2] + C.totalBloco[3];
    var u = inteiro(E.unidadesFase);
    var giro = giroUsado(E);
    var investimentoTotal = giro === null ? null : capexFase + giro;
    // área total do bloco 3 (tipologias, extras com área e áreas comuns)
    var areaTotal = 0, faltaAreaTip = false, temArea = false;
    linhasDe(E, 3).forEach(function (l) {
      if (!ativa(l)) return;
      var a = areaDe(l), q = l.modo === "valor" ? (inteiro(l.qtd) || 1) : qtdDe(l, E);
      if (a !== null && q !== null) { areaTotal += q * a; temArea = true; }
      else if (l.tipologia) faltaAreaTip = true;
    });
    if (faltaAreaTip || !temArea) areaTotal = null;
    var palpite = paraNumero(E.palpite);
    var top3 = valorados.slice().sort(function (a, c) { return c.valor - a.valor; }).slice(0, 3);
    var pctLinhasCotadas = div(nCotadas, nLinhas);
    var degrau;
    var soBloco3 = capexFase > 0 && [1, 2, 4, 5, 6].every(function (k) { return C.totalBloco[k] === 0; });
    if (capexFase === 0 || soBloco3) degrau = "Sonhador";
    else if (pctLinhasCotadas !== null && pctLinhasCotadas > 0.5 + EPS && top3.length > 0 && top3.every(function (x) { return x.origem === "cotacao"; })) degrau = "Calculista";
    else degrau = "Estimador";
    var infraPC = paraNumero(E.infraProjetoCompleto);
    var infraFutura = infraPC !== null && infraPC - C.totalBloco[2] >= 0 ? infraPC - C.totalBloco[2] : null;

    C.subtotal = subtotal; C.contingenciaPct = pct; C.contingencia = contingencia; C.capexFase = capexFase;
    C.pctBloco = pctBloco; C.obra = obra; C.pctObra = div(obra, capexFase);
    C.custoPorUnidade = u ? div(capexFase, u) : null;
    C.giro = giro; C.investimentoTotal = investimentoTotal; C.investimentoPorUnidade = u && investimentoTotal !== null ? div(investimentoTotal, u) : null;
    C.areaTotal = areaTotal; C.custoPorM2 = areaTotal ? div(capexFase, areaTotal) : null;
    C.nLinhas = nLinhas; C.nCotadas = nCotadas; C.nEstimadas = nEstimadas; C.nBranco = nBranco;
    C.pctLinhasCotadas = pctLinhasCotadas; C.valorCotado = valorCotado; C.valorEstimado = valorEstimado; C.pctValorCotado = div(valorCotado, subtotal);
    C.n3Cotacoes = n3; C.nCotacoesIncompletas = nInc; C.incompletas = incompletas; C.cotacoesVencidas = vencidas.length; C.vencidas = vencidas; C.brancos = brancos;
    C.osePctFFE = div(C.totalBloco[5], C.totalBloco[4]); C.preAberturaPctObra = div(C.totalBloco[6], obra);
    C.palpite = palpite; C.palpiteCobre = palpite !== null ? div(palpite, capexFase) : null; C.diferencaPalpite = palpite !== null ? capexFase - palpite : null;
    C.infraFutura = infraFutura; C.top3 = top3; C.degrau = degrau; C.degrauDiagnostico = degrauDiagnostico(E);
    C.porBloco = porBloco; C.terreno = ehNS(E.terrenoValor) ? null : paraNumero(E.terrenoValor);
    C.transposicao = transposicao(E, C);
    return C;
  }
  /** Degrau pelas respostas do diagnóstico (elaboração própria, rotulada). */
  function degrauDiagnostico(E) {
    if (!E || !E.d1) return null;
    if (E.d1 === "nao") return "Sonhador";
    if (E.d1 === "numero" && E.d3 === "maioria") return "Calculista";
    return "Estimador";
  }
  function notaP6(origem) { var o = ORIGENS.filter(function (x) { return x.v === origem; })[0]; return o ? o.notaP6 : null; }

  /** Quadro "Como levar para a página 6" (PLANO 6.2). Nada é gravado na ficha do Pilar 6. */
  function transposicao(E, C) {
    var u = inteiro(E.unidadesFase);
    if (!u) return null;
    var soma = { unidade: 0, deck: 0, piso: 0, luz: 0, agua: 0, mobilia4: 0 };
    var temPiso = false;
    todasLinhas(E).forEach(function (x) {
      var v = valorLinha(x.l, E) || 0, t = x.l.tagP6;
      if (t === "unidade" && x.b === 3) soma.unidade += v;
      else if (t === "deck") soma.deck += v;
      else if (t === "piso") { soma.piso += v; if (comValor(x.l) && v > 0) temPiso = true; }
      else if (t === "luz") soma.luz += v;
      else if (t === "agua") soma.agua += v;
      else if (t === "mobilia" && x.b === 4) soma.mobilia4 += v;
    });
    var T = {
      unidades: u,
      l_unidade: soma.unidade / u, l_deck: soma.deck / u, l_piso: soma.piso / u, l_luz: soma.luz / u, l_agua: soma.agua / u,
      l_mobilia: (soma.mobilia4 + C.totalBloco[5]) / u, pisoNoM2: !temPiso,
      licencas: C.totalBloco[1], reserva_pct: C.contingenciaPct,
    };
    T.pronta = T.l_unidade + T.l_deck + T.l_luz + T.l_agua + T.l_mobilia + T.l_piso;
    var unidadesProntas = u * T.pronta;
    T.infra = (C.subtotal - unidadesProntas - C.totalBloco[1]) + C.contingenciaPct / 100 * (C.subtotal - unidadesProntas);
    T.conferencia = unidadesProntas * (1 + C.contingenciaPct / 100) + T.licencas + T.infra;
    T.confere = Math.abs(T.conferencia - C.capexFase) <= 0.01;
    T.giro = C.giro; T.terreno = C.terreno;
    return T;
  }

  /* ------------------------------------------------------------------
     5. Alertas (PLANO 6.4): a ordem da lista é a prioridade
     ------------------------------------------------------------------ */
  var NOTA_FAIXA = "Faixa de conferência citada pela fonte; não é preço nem regra fixa.";
  var ORDEM_ALERTAS = ["A17", "A3z", "A1", "A6", "A7", "A8", "A2", "A11", "A12", "A3", "A4", "A5", "A9", "A10", "A15", "A13", "A14", "A16", "A18", "A19", "A20"];
  var INFO = {
    id: "INFO", tit: "Pergunte ao seu engenheiro e ao seu contador",
    engenheiro: ["O preço inclui mão de obra, encargos, administração e lucro (Benefícios e Despesas Indiretas, o BDI)?", "Quanto o frete e a montagem acrescentam neste terreno?", "Como o preço pode mudar até a compra (reajuste)?", "A rede está dimensionada para quantas unidades?", "Quem assina a responsabilidade técnica (Anotação ou Registro de Responsabilidade Técnica, ART ou RRT)?"],
    contador: ["Quais são os custos de aquisição do terreno (escritura, Imposto de Transmissão, o ITBI, registro e certidões)?", "Quais impostos incidem sobre a obra e a compra de equipamentos?", "Compra, permuta, sociedade ou arrendamento: o que muda em cada forma de entrada do terreno (com o advogado)?"],
    concessionaria: ["Concessionária: qual é o ponto e a tensão de energia mais próximos?", "Prefeitura: qual é a lista e o custo das licenças?"],
  };
  function alertas(E, C) {
    E = E || {}; C = C || calcular(E);
    var A = [];
    var add = function (id, tipo, tit, txt, fonte, extra) { var a = { id: id, tipo: tipo, tit: tit, txt: txt, fonte: fonte }; if (extra) for (var k in extra) a[k] = extra[k]; A.push(a); };
    var u = inteiro(E.unidadesFase), up = inteiro(E.unidadesProjeto);
    // A17
    if (!tipologiasConferem(E)) add("A17", "bloqueia", "As tipologias não somam a fase", "As tipologias somam " + somaTipologias(E) + " unidades, e a fase tem " + (u === null ? "um número ainda não informado de" : u) + " unidades. Ajuste as quantidades na tela das unidades.", "validação");
    // A3z
    var pctBruto = paraNumero(E.contingenciaPct);
    if (pctBruto === null || pctBruto <= 0) add("A3z", "bloqueia", "A reserva nunca é zero", ehNS(E.contingenciaPct) ? "Você marcou Não sei na reserva do imprevisto. Confira os fatores de risco e escolha uma porcentagem: a reserva nunca é zero." : "A reserva do imprevisto está vazia ou em zero. Toda obra tem imprevisto: a reserva nunca é zero.", "Mapa de fontes 1.2 (A05, VOL05, P6, F01, B06, F05)");
    // A1 e A2
    var a1 = [], a2 = [];
    for (var b = 1; b <= 6; b++) {
      var L = linhasDe(E, b), pb = C.porBloco[b];
      var temNaoNA = L.some(function (l) { return l.origem !== "naoAplica"; });
      if (temNaoNA && pb.nComValor === 0) a1.push(b);
      if (pb.nComValor > 0 && pb.nCotadas === 0) a2.push(b);
    }
    if (a1.length) add("A1", "critico", a1.length === 1 ? "Bloco " + a1[0] + " em branco" : "Blocos em branco", (a1.length === 1 ? "O bloco " + a1[0] + " · " + nomeBloco(a1[0], E) + " não tem nenhuma linha com valor." : "Os blocos " + juntar(a1.map(String)) + " não têm nenhuma linha com valor.") + " Bloco em branco só pode aumentar a conta.", "P6 (ficha, infraestrutura); erros do A05 cap. 2", { blocos: a1 });
    var ativo2 = bloco2Ativo(E);
    var infraD = inteiro(E.infraDimensionadaPara);
    if (ativo2 && infraD !== null && up !== null && infraD < up) add("A6", "critico", "A rede ficou menor que o projeto", "A rede está dimensionada para " + infraD + " unidades, e o projeto completo tem " + up + ". Refazer vala e caminho na fase dois é a forma mais cara de economizar.", "R14 (A05 cap. 12; P6 cap. 04; F01 cap. 6)");
    if (ehNS(E.unidadesProjeto) || falta(E.unidadesProjeto) || (ativo2 && (ehNS(E.infraDimensionadaPara) || falta(E.infraDimensionadaPara)))) add("A7", "bloqueia", "Para quantas unidades a rede é pensada?", "Falta dizer quantas unidades o projeto completo terá e para quantas a rede é dimensionada. Sem isso, a infraestrutura da fase um não se confere.", "R11, R14");
    if (ativo2 && ehNS(E.distanciaEnergiaM)) add("A8", "ns", "Qual a distância até o ponto de energia?", "É a primeira pergunta do orçamento da infraestrutura. A concessionária local informa o ponto e a tensão.", "R12 (confirmar com a concessionária local)");
    if (a2.length) add("A2", "atencao", a2.length === 1 ? "Bloco " + a2[0] + " sem nenhuma cotação" : "Blocos sem nenhuma cotação", (a2.length === 1 ? "O bloco " + a2[0] + " · " + nomeBloco(a2[0], E) + " tem valor, mas nenhuma linha com cotação escrita." : "Os blocos " + juntar(a2.map(String)) + " têm valor, mas nenhuma linha com cotação escrita.") + " Por enquanto, ele é estimativa.", "R3, R5", { blocos: a2 });
    if (C.preAberturaPctObra !== null && C.preAberturaPctObra < 0.05 - EPS) add("A11", "atencao", "Pré-abertura abaixo da faixa citada", "A pré-abertura é " + fmtPct(C.preAberturaPctObra) + " da obra (infraestrutura mais unidades); a faixa citada vai de 5% a 10%. Esquecer a pré-abertura é o quinto erro do orçamento amador. " + NOTA_FAIXA, "R21; quinto erro do A05 cap. 2", { blocos: [6] });
    if (C.pctObra !== null && C.pctObra > 0.8 + EPS) add("A12", "atencao", "A obra passa de 80% do custo", "Infraestrutura e unidades somam " + fmtPct(C.pctObra) + " do custo de abrir a porta: provavelmente faltou algo nos outros blocos. " + NOTA_FAIXA, "R29 (A05 cap. 3; F01 cap. 6)", { blocos: [1, 4, 5, 6] });
    var p = pctBruto;
    var piso = E.imovelPronto === true ? 15 : 10;
    if (p !== null && p > 0 && p < piso - EPS) add("A3", "atencao", "Reserva abaixo da faixa citada", "A reserva está em " + fmtN(p, 2) + "%. A faixa citada vai de " + (E.imovelPronto === true ? "15% a 25% para imóvel pronto" : "10% a 15% do subtotal") + ". " + NOTA_FAIXA, "A05 cap. 3 e 7; VOL05 cap. 4; P6 cap. 03; PL1; JC02 P11; JC04 P04", { blocos: [7] });
    if (p !== null && p > 0 && p < 15 - EPS && (E.primeiraObra === true || temFator(E))) add("A4", "atencao", "Com fator de risco, a fonte pede o teto", "Com " + (E.primeiraObra === true ? "a primeira obra" : "fator de risco") + (E.primeiraObra === true && temFator(E) ? " e fator de risco" : "") + ", a fonte pede a reserva no teto da faixa (15%) ou acima. Hoje ela está em " + fmtN(p, 2) + "%.", "A05 cap. 7; R22", { blocos: [7] });
    if (p !== null && p > 25 + EPS) add("A5", "atencao", "Reserva acima de todas as faixas citadas", "A reserva está em " + fmtN(p, 2) + "%. Confira se ela não está cobrindo linha esquecida ou escopo novo: isso é linha nova, com decisão.", "R23", { blocos: [7] });
    if (C.osePctFFE !== null && !entre(C.osePctFFE, 0.10, 0.15)) add("A9", "atencao", C.osePctFFE < 0.10 ? "Enxoval e utensílios abaixo da faixa" : "Enxoval e utensílios acima da faixa", "O bloco 5 é " + fmtPct(C.osePctFFE) + " do bloco 4; a faixa citada vai de 10% a 15%. " + (C.osePctFFE < 0.10 ? "Algum item de um dia de operação pode ter ficado de fora." : "Confira se o enxoval não está contado duas vezes.") + " " + NOTA_FAIXA, "R16, R28", { blocos: [4, 5] });
    var temB5 = linhasDe(E, 5).some(ativa);
    if (temB5 && E.enxovalNaoDuplicado !== true) add("A10", "atencao", "O enxoval está contado uma vez só?", "Confirme que o enxoval não está também na cotação do mobiliário. Cada item mora numa linha só.", "R28", { blocos: [5] });
    var prontas = tipologias(E).filter(function (l) { return l.forma === "pronta" && l.freteMontagemConfirmados !== true; });
    if (prontas.length) add("A15", "atencao", "Frete, fundação e montagem confirmados?", "Na estrutura pronta (" + juntar(prontas.map(function (l) { return txt(l.nome); })) + "), confirme por escrito se frete, fundação e montagem estão incluídos.", "R33");
    if (C.cotacoesVencidas > 0) add("A13", "atencao", C.cotacoesVencidas === 1 ? "1 cotação com mais de 90 dias" : C.cotacoesVencidas + " cotações com mais de 90 dias", (C.cotacoesVencidas === 1 ? "A cotação de " : "As cotações de ") + juntar(C.vencidas.map(function (x) { return minusculaInicial(x.nome) + " (" + x.dias + " dias)"; })) + " passou de 90 dias: refaça antes de usar.", "R8");
    if (C.nCotacoesIncompletas > 0) add("A14", "atencao", C.nCotacoesIncompletas === 1 ? "1 linha com cotação incompleta" : C.nCotacoesIncompletas + " linhas com cotação incompleta", (C.nCotacoesIncompletas === 1 ? "Uma linha tem" : C.nCotacoesIncompletas + " linhas têm") + " menos de três cotações ou escopos diferentes. Compare três propostas com a mesma especificação e peça o que cada uma não inclui.", "R5, R6");
    var gm = paraNumero(E.giroMeses);
    if (gm !== null && gm < 3 - EPS) add("A16", "atencao", "Giro abaixo do piso de três meses", "Você calculou " + fmtN(gm, 2) + " meses de giro. Três meses são o piso citado; a conta completa do giro é a do Pilar 6. " + NOTA_FAIXA, "A05 cap. 7 e 10; VOL05 cap. 4; P6 cap. 06; PL2");
    if (E.terrenoSituacao === "comprar") add("A18", "info", "Custos de compra do terreno ficam fora", "Escritura, imposto de transmissão e registro não estão nesta conta: pergunte ao contador. A necessidade de capital fica no Pilar 7.", "Lacuna 5; R27");
    if (E.situacao === "ampliar") add("A19", "critico", "Não pague a obra com o caixa da operação", "A ampliação precisa de dinheiro separado. O caixa da operação paga a operação.", "F01 cap. 1 e 7");
    var regra = [E.regraParaQue, E.regraQuemAutoriza, E.regraComoRegistra, E.regraQuandoConfere];
    if (regra.some(function (r) { return txt(r).length < 10; })) add("A20", "bloqueia", "A regra de uso da reserva está incompleta", "Escreva as quatro linhas da regra (para quê, quem autoriza, como se registra e quando se confere), com pelo menos 10 letras cada.", "R24", { blocos: [7] });
    A.sort(function (x, y) { return ORDEM_ALERTAS.indexOf(x.id) - ORDEM_ALERTAS.indexOf(y.id); });
    return A;
  }
  function tresPrimeiros(A) { return A.slice(0, 3); }

  /* ------------------------------------------------------------------
     6. O que fazer em 30 dias e como verificar (PLANO 6.5)
     ------------------------------------------------------------------ */
  function acaoSugerida(E, C, A) {
    C = C || calcular(E); A = A || alertas(E, C);
    var tem = function (ids) { return A.some(function (a) { return ids.indexOf(a.id) >= 0; }); };
    var dono = E.situacao === "operador";
    var a1 = A.filter(function (a) { return a.id === "A1"; })[0];
    if (a1) {
      var bs = a1.blocos.map(function (b) { return b + " · " + nomeBloco(b, E); });
      return { ordem: 1, acao: "Listar as linhas do bloco " + juntar(bs) + " e pedir as primeiras cotações.", verificacao: "As linhas listadas na ficha e os pedidos enviados, com data e destinatário." };
    }
    if (tem(["A6", "A7", "A8"])) {
      var up = inteiro(E.unidadesProjeto);
      return { ordem: 2, acao: "Pedir à concessionária o ponto de energia e ao projetista o dimensionamento da rede para " + (up ? "as " + up + " unidades" : "todas as unidades") + " do projeto completo.", verificacao: "A resposta da concessionária e a proposta do projetista, com o número de unidades escrito." };
    }
    if (C.brancos.length) {
      return { ordem: 3, acao: "Pedir cotação escrita das linhas em branco: " + juntar(C.brancos.map(function (x) { return minusculaInicial(x.nome); })) + ".", verificacao: C.brancos.length === 1 ? "A proposta recebida, com data e escopo, lançada na ficha." : "As " + C.brancos.length + " propostas recebidas, com data e escopo, lançadas na ficha." };
    }
    if (C.degrau !== "Calculista") {
      var nomes = C.top3.map(function (x) { return minusculaInicial(x.nome); });
      return { ordem: 4, acao: "Pedir três cotações com a mesma especificação para as " + (nomes.length === 3 ? "três maiores linhas" : "maiores linhas") + (nomes.length ? ": " + juntar(nomes) : "") + ".", verificacao: "Três propostas por linha, com a mesma especificação anexada." };
    }
    if (tem(["A13", "A14"])) return { ordem: 5, acao: "Refazer as cotações vencidas e completar as que têm menos de três propostas comparáveis.", verificacao: "Datas novas e três propostas comparáveis por linha." };
    var rev = A.filter(function (a) { return ["A3", "A4", "A5", "A9", "A11", "A12"].indexOf(a.id) >= 0; })[0];
    if (rev) {
      var bl = (rev.blocos || []).map(function (b) { return b + " · " + nomeBloco(b, E); });
      return { ordem: 6, acao: "Revisar linha a linha, com o checklist, o bloco " + juntar(bl) + ".", verificacao: "O bloco revisado e uma nota do que mudou." };
    }
    return { ordem: 7, acao: dono ? "Levar a página 6A ao dono, voltar à ficha do Pilar 6, refazer a página 6 com este custo e abrir a Planilha 2." : "Voltar à ficha do Pilar 6, refazer a página 6 com este custo e abrir a Planilha 2.", verificacao: "A página 6 refeita, com a data das cotações." };
  }
  /** As verificações da lista (o membro escolhe uma ou escreve a sua). */
  var VERIFICACOES = [
    "As linhas listadas na ficha e os pedidos enviados, com data e destinatário.",
    "A resposta da concessionária e a proposta do projetista, com o número de unidades escrito.",
    "As propostas recebidas, com data e escopo, lançadas na ficha.",
    "Três propostas por linha, com a mesma especificação anexada.",
    "Datas novas e três propostas comparáveis por linha.",
    "O bloco revisado e uma nota do que mudou.",
    "A página 6 refeita, com a data das cotações.",
  ];
  function proximaEtapa(E) {
    var dono = E && E.situacao === "operador";
    if (E && E.turma === "acompanhamento") return dono ? "Leve a página 6A ao dono e ao encontro do Pilar 6 e refaça a página 6 depois do comentário da equipe." : "Leve a página 6A ao encontro do Pilar 6 e refaça a página 6 depois do comentário da equipe.";
    return dono ? "Leve a página 6A ao dono. Depois, volte ao Pilar 6 e refaça a página 6 com estes números." : "Volte ao Pilar 6 e refaça a página 6 com estes números. Depois, abra a Planilha 2 · Investimento.";
  }

  /* ------------------------------------------------------------------
     7. Leituras (significado) e faixas (PLANO 6.3)
     ------------------------------------------------------------------ */
  function leituraLinhasCotadas(pct) {
    if (pct === null || pct === undefined) return "Ainda não há linhas com origem.";
    if (pct <= EPS) return "Nenhuma linha tem cotação: por enquanto, a ficha é um mapa do que cotar.";
    if (pct <= 0.5 + EPS) return "A maior parte das linhas ainda é estimativa ou está em branco.";
    return "A maioria das linhas tem cotação escrita.";
  }
  function leituraReserva(E) {
    var p = paraNumero(E.contingenciaPct);
    if (p === null || p <= 0) return "Sem reserva: ela nunca é zero.";
    var lo = E.imovelPronto === true ? 15 : 10, hi = E.imovelPronto === true ? 25 : 15;
    if (p < lo - EPS) return "Abaixo da faixa citada (" + lo + "% a " + hi + "%).";
    if (p > 25 + EPS) return "Acima de 25%: confira se não está cobrindo linha esquecida.";
    if (p > hi + EPS) return "Acima da faixa citada (" + lo + "% a " + hi + "%), o que a fonte aceita com fator de risco.";
    return "Dentro da faixa citada (" + lo + "% a " + hi + "%).";
  }
  function leituraPalpite(C) {
    if (C.palpite === null || C.palpiteCobre === null) return "Sem palpite para comparar.";
    return "O seu palpite cobria " + fmtPct(C.palpiteCobre) + " da conta; a diferença é de " + brl(C.diferencaPalpite) + ".";
  }
  function leituraDegrau(C) {
    var r = REGUA.filter(function (x) { return x.v === C.degrau; })[0];
    var t = "Degrau " + C.degrau + ": " + r.t;
    if (C.degrauDiagnostico && C.degrauDiagnostico !== C.degrau) t += " No diagnóstico, você estava em " + C.degrauDiagnostico + ".";
    else if (C.degrauDiagnostico) t += " É o mesmo degrau do diagnóstico.";
    return t;
  }

  /* ------------------------------------------------------------------
     8. Validação de cada tela (bloqueia o Avançar) e critério de conclusão
     ------------------------------------------------------------------ */
  var TELAS = ["abertura", "palpite", "fase", "b1", "b2", "b3", "b4", "b5", "b6", "reserva", "giro", "resultado", "acao"];
  function validarTela(tela, E, hoje) {
    E = E || {}; hoje = hoje || E.hoje;
    var n;
    if (tela === "abertura") {
      var p = txt(E.projeto), nm = txt(E.nome);
      if (nm && (nm.length < 2 || nm.length > 60)) return "O nome vai de 2 a 60 letras (ou deixe em branco).";
      if (p.length < 2 || p.length > 60) return "Dê um nome ao projeto (2 a 60 letras).";
      if (!E.situacao) return "Escolha a frase que descreve a sua situação.";
      if (!E.tipo) return "Escolha o tipo de hospedagem.";
      for (var i = 0; i < DIAG.length; i++) if (!E[DIAG[i].id]) return "Responda às quatro perguntas do diagnóstico.";
      return "";
    }
    if (tela === "palpite") {
      if (ehNS(E.palpite)) return "";
      n = paraNumero(E.palpite);
      if (n === null) return "Escreva o seu palpite em reais ou toque em Não sei.";
      if (n < 0 || n > LIMITES.dinheiroMax) return "O palpite vai de R$ 0 a R$ 100 milhões.";
      return "";
    }
    if (tela === "fase") {
      var u = inteiro(E.unidadesFase);
      if (u === null || u < 1 || u > LIMITES.unidadesMax) return "As unidades da fase vão de 1 a 200, sem casas decimais.";
      if (!ehNS(E.unidadesProjeto)) {
        var up = inteiro(E.unidadesProjeto);
        if (up === null) return "Escreva as unidades do projeto completo ou toque em Não sei.";
        if (up < u || up > LIMITES.unidadesMax) return "O projeto completo tem de " + u + " a 200 unidades (nunca menos que a fase).";
      }
      if (E.primeiraObra !== true && E.primeiraObra !== false) return "Diga se esta é a sua primeira obra.";
      return "";
    }
    var m = /^b([1-6])$/.exec(tela);
    if (m) {
      var b = Number(m[1]), L = linhasDe(E, b);
      if (L.length < 1) return "O bloco precisa de pelo menos uma linha (se não se aplica, marque Não se aplica).";
      if (L.length > LIMITES.linhasMax) return "Cada bloco vai até 15 linhas.";
      for (var k = 0; k < L.length; k++) { var er = erroLinha(L[k], E, hoje); if (er) return er; }
      if (b === 6 && L.every(function (l) { return l.origem === "naoAplica"; })) return "A pré-abertura nunca é inteira \"não se aplica\": toda hospedagem abre com licença, fotos e treinamento.";
      if ((b === 2 || b === 3) && E.imovelPronto !== true && L.every(function (l) { return l.origem === "naoAplica"; })) return "Este bloco só pode ficar inteiro em \"não se aplica\" quando o imóvel já existe.";
      if (b === 2 && bloco2Ativo(E)) {
        if (!ehNS(E.distanciaEnergiaM)) { n = paraNumero(E.distanciaEnergiaM); if (n === null || n < 0 || n > LIMITES.distMax) return "Escreva a distância até o ponto de energia (0 a 50.000 m) ou toque em Não sei."; }
        if (!ehNS(E.infraDimensionadaPara)) { n = inteiro(E.infraDimensionadaPara); if (n === null || n < 1 || n > LIMITES.redeMax) return "Diga para quantas unidades a rede é dimensionada (1 a 999) ou toque em Não sei."; }
        if (!falta(E.infraProjetoCompleto)) { n = paraNumero(E.infraProjetoCompleto); if (n === null || n < 0 || n > LIMITES.dinheiroMax) return "O valor da rede inteira vai de R$ 0 a R$ 100 milhões (ou deixe em branco)."; }
      }
      if (b === 3) {
        var tip = linhasDe(E, 3).filter(function (l) { return l.tipologia; });
        if (tip.length > LIMITES.tipologiasMax) return "São até 3 tipologias.";
        if (E.imovelPronto !== true && tipologias(E).length < 1) return "Inclua pelo menos uma tipologia de unidade.";
        if (!tipologiasConferem(E)) return "As tipologias somam " + somaTipologias(E) + " unidades, e a fase tem " + inteiro(E.unidadesFase) + ". Ajuste as quantidades.";
      }
      return "";
    }
    if (tela === "reserva") {
      if (ehNS(E.contingenciaPct)) return "";
      n = paraNumero(E.contingenciaPct);
      if (n === null || n <= 0 || n > LIMITES.reservaMax) return "A reserva vai de mais de 0% até 50%, ou toque em Não sei.";
      var rg = [E.regraParaQue, E.regraQuemAutoriza, E.regraComoRegistra, E.regraQuandoConfere];
      if (rg.some(function (r) { return txt(r).length > 200; })) return "Cada linha da regra vai até 200 letras.";
      return "";
    }
    if (tela === "giro") {
      var gm = paraNumero(E.giroMeses), gc = paraNumero(E.giroCustoMensal);
      if (!falta(E.giroMeses) && (gm === null || gm < 0 || gm > LIMITES.giroMesesMax)) return "Os meses de giro vão de 0 a 24.";
      if (!falta(E.giroCustoMensal) && (gc === null || gc < 0 || gc > LIMITES.dinheiroMax)) return "O custo de um mês vai de R$ 0 a R$ 100 milhões.";
      if (!ehNS(E.giro) || (gm !== null && gc !== null)) {
        var g = giroUsado(E);
        if (g === null) return "Escreva o capital de giro em reais, use a calculadora ou toque em Não sei.";
        if (g < 0 || g > LIMITES.dinheiroMax) return "O giro vai de R$ 0 a R$ 100 milhões.";
        if (g === 0) {
          if (E.situacao === "abrir") return "Quem vai abrir precisa de capital de giro maior que zero. Se ainda não sabe, toque em Não sei.";
          var j = txt(E.giroZeroJustificativa);
          if (j.length < 10 || j.length > 200) return "Com giro zero, escreva por quê (10 a 200 letras).";
        }
      }
      if (!E.terrenoSituacao) return "Diga a situação do terreno.";
      if (!falta(E.terrenoValor) && !ehNS(E.terrenoValor)) { n = paraNumero(E.terrenoValor); if (n === null || n < 0 || n > LIMITES.dinheiroMax) return "O valor do terreno vai de R$ 0 a R$ 100 milhões, ou toque em Não sei."; }
      return "";
    }
    if (tela === "acao") {
      var a = txt(E.acao30);
      if (a.length < 10 || a.length > 300) return "Escreva a ação de 30 dias (10 a 300 letras).";
      if (!prazoOk(E.prazo, hoje)) return "O prazo vai de hoje até 30 dias a partir de hoje.";
      if (txt(E.verificacao).length < 10) return "Escreva como você vai verificar (10 letras ou mais).";
      return "";
    }
    return "";
  }
  function prazoOk(prazo, hoje) { if (!dataOk(prazo) || !dataOk(hoje)) return false; var d = diasEntre(hoje, prazo); return d >= 0 && d <= LIMITES.prazoDias; }

  /** Critério de conclusão (selo "Pronto para levar à página 6"), PLANO 6.6. */
  function criterio(E, C, hoje) {
    E = E || {}; hoje = hoje || E.hoje; C = C || calcular(E, hoje);
    var u = inteiro(E.unidadesFase), up = inteiro(E.unidadesProjeto);
    var linhasOk = true, blocosOk = true;
    for (var b = 1; b <= 6; b++) {
      var L = linhasDe(E, b);
      if (L.some(function (l) { return !l.origem || erroLinha(l, E, hoje) !== ""; })) linhasOk = false;
      var temAtiva = L.some(ativa);
      var podeNA = E.imovelPronto === true && (b === 2 || b === 3) && blocoInteiroNA(E, b);
      if (!temAtiva && !podeNA) blocosOk = false;
    }
    var rg = [E.regraParaQue, E.regraQuemAutoriza, E.regraComoRegistra, E.regraQuandoConfere].every(function (r) { return txt(r).length >= 10 && txt(r).length <= 200; });
    var pctR = paraNumero(E.contingenciaPct);
    var infraOk = !bloco2Ativo(E) || (function () { var d = inteiro(E.infraDimensionadaPara); return d !== null && d >= 1 && d <= LIMITES.redeMax; })();
    var g = giroUsado(E);
    var giroOk = g !== null && (g > 0 || (g === 0 && E.situacao !== "abrir" && E.situacao && txt(E.giroZeroJustificativa).length >= 10));
    var itens = [
      { n: 1, ok: u !== null && u >= 1 && up !== null && up >= u && tipologiasConferem(E), txt: "As unidades da fase e do projeto completo informadas, e as tipologias somando a fase." },
      { n: 2, ok: linhasOk && blocosOk, txt: "Os blocos 1 a 6 com a origem de cada linha escolhida e pelo menos uma linha que se aplica em cada bloco." },
      { n: 3, ok: C.capexFase > 0, txt: "O custo de abrir a porta maior que zero." },
      { n: 4, ok: pctR !== null && pctR > 0 && pctR <= LIMITES.reservaMax && rg, txt: "A reserva maior que zero e as quatro linhas da regra de uso escritas." },
      { n: 5, ok: infraOk, txt: "Para quantas unidades a rede é dimensionada." },
      { n: 6, ok: giroOk, txt: "O capital de giro maior que zero (ou zero com a justificativa, só para quem já opera)." },
      { n: 7, ok: !!E.terrenoSituacao, txt: "A situação do terreno respondida." },
      { n: 8, ok: txt(E.acao30).length >= 10 && txt(E.acao30).length <= 300 && prazoOk(E.prazo, hoje), txt: "A ação de 30 dias escrita, com prazo de até 30 dias." },
      { n: 9, ok: E.pdfBaixado === true, txt: "A página 6A baixada em PDF." },
    ];
    return { ok: itens.every(function (x) { return x.ok; }), antesDoPdf: itens.slice(0, 8).every(function (x) { return x.ok; }), itens: itens, faltas: itens.filter(function (x) { return !x.ok; }).map(function (x) { return x.txt; }) };
  }

  /** O que fica salvo em resumo.dados (para a página 7 e um futuro montador do Dossiê). */
  function resumoDados(E, C) {
    var T = C.transposicao || {};
    var r = function (x) { return typeof x === "number" && Number.isFinite(x) ? arred(x, 2) : null; };
    return {
      unidades: inteiro(E.unidadesFase), unidades_projeto: inteiro(E.unidadesProjeto),
      bloco1: r(C.totalBloco[1]), bloco2: r(C.totalBloco[2]), bloco3: r(C.totalBloco[3]), bloco4: r(C.totalBloco[4]), bloco5: r(C.totalBloco[5]), bloco6: r(C.totalBloco[6]),
      subtotal: r(C.subtotal), reserva_pct: C.contingenciaPct, reserva: r(C.contingencia), capex_fase: r(C.capexFase),
      giro: r(C.giro), investimento_total: r(C.investimentoTotal), custo_por_unidade: r(C.custoPorUnidade), investimento_por_unidade: r(C.investimentoPorUnidade),
      area_total: r(C.areaTotal), custo_por_m2: r(C.custoPorM2), terreno: r(C.terreno), terreno_situacao: E.terrenoSituacao || null,
      pct_linhas_cotadas: r(C.pctLinhasCotadas === null ? null : C.pctLinhasCotadas * 100), pct_valor_cotado: r(C.pctValorCotado === null ? null : C.pctValorCotado * 100),
      degrau: C.degrau, unidade_pronta: r(T.pronta), licencas: r(T.licencas), infra_comum: r(T.infra), exemplo: E.exemplo === true,
    };
  }

  /* ------------------------------------------------------------------
     9. O exemplo: Chalés do Ribeirão (dados fictícios), PLANO seção 7
     ------------------------------------------------------------------ */
  var ROTULO_EXEMPLO = "Exemplo com dados fictícios. Não são preços de referência.";
  function exemplo(hoje) {
    hoje = hoje || "2026-11-27";
    var c = function (nome, valor, n, mesma, extra) { var l = novaLinha({ nome: nome, modo: "valor" }); l.valor = valor; l.origem = "cotacao"; l.nCotacoes = n; l.mesmaEspec = !!mesma; if (extra) for (var k in extra) l[k] = extra[k]; return l; };
    var e = function (nome, valor) { var l = novaLinha({ nome: nome, modo: "valor" }); l.valor = valor; l.origem = "estimativa"; return l; };
    var br = function (nome) { var l = novaLinha({ nome: nome, modo: "valor" }); l.origem = "branco"; return l; };
    var pu = function (nome, q, vu, origem, tag, n, mesma) { var l = novaLinha({ nome: nome, modo: "qtdUnit", porUnidade: true, tagP6: tag }); l.qtd = q; l.valorUnit = vu; l.origem = origem; if (origem === "cotacao") { l.nCotacoes = n; l.mesmaEspec = !!mesma; } return l; };
    var chale = novaLinha({ nome: "Chalé de 32 m²", tipologia: true, forma: "construida" });
    Object.assign(chale, { qtd: 4, areaM2: 32, custoM2: 4500, origem: "cotacao", nCotacoes: 3, mesmaEspec: true });
    var deck = pu("Deck de cada chalé", 4, 9000, "cotacao", "deck", 2, true); deck.areaM2 = 10;
    var apoio = novaLinha({ nome: "Área de apoio e lavanderia", modo: "area" });
    Object.assign(apoio, { qtd: 1, areaM2: 20, custoM2: 3500, origem: "cotacao", nCotacoes: 1 });
    var enx = novaLinha({ nome: "Enxoval (três jogos por cama)", enxoval: true, tagP6: "mobilia" });
    Object.assign(enx, { camasPorUnidade: 1, custoJogo: 700, origem: "cotacao", nCotacoes: 3, mesmaEspec: true });
    var recepcao = novaLinha({ nome: "Recepção", modo: "valor", tagP6: "mobilia" }); recepcao.origem = "naoAplica";
    var E = estadoInicial(hoje);
    Object.assign(E, {
      nome: "Helena (exemplo)", projeto: "Chalés do Ribeirão", situacao: "abrir", tipo: "cabanas", imovelPronto: false,
      d1: "palpite", d2: "soUnidade", d3: "algumas", d4: "nao",
      palpite: 700000, dataPalpite: hoje, unidadesFase: 4, unidadesProjeto: 6, fatoresRisco: [], primeiraObra: true,
      distanciaEnergiaM: 180, infraDimensionadaPara: 6, infraProjetoCompleto: "", enxovalNaoDuplicado: true,
      contingenciaPct: 15,
      regraParaQue: "Imprevisto da obra orçada (solo, chuva, reajuste, exigência da licença).",
      regraQuemAutoriza: "Helena, depois de ouvir o engenheiro.",
      regraComoRegistra: "Planilha com data, motivo e valor.",
      regraQuandoConfere: "A cada medição da obra.",
      giro: 45000, giroMeses: 3, giroCustoMensal: 15000, terrenoSituacao: "meu", terrenoValor: 300000,
      prazo: somaDias(hoje, 30), exemplo: true,
    });
    E.blocos = {
      1: [c("Arquitetura", 18000, 3, true), c("Engenharias (estrutural, elétrica, hidrossanitária)", 14000, 2, true), c("Levantamento do terreno", 3500, 3, true), e("Aprovações e taxas da prefeitura", 4500), br("Licença ambiental")],
      2: [c("Acesso e caminhos", 36000, 3, true), c("Energia (rede comum até as unidades)", 42000, 1, false), c("Água (poço e reservatório)", 28000, 2, true, { dataCotacao: "2026-07-20" }), c("Esgoto e tratamento", 32000, 2, true),
        pu("Ligação de luz de cada unidade", 4, 3500, "estimativa", "luz"), pu("Água e esgoto de cada unidade", 4, 2500, "estimativa", "agua"), c("Estacionamento", 8000, 2, true), br("Internet")],
      3: [chale, deck, apoio],
      4: [pu("Cama e colchão (unidade-modelo)", 4, 4800, "cotacao", "mobilia", 3, true), pu("Mobiliário (unidade-modelo)", 4, 7200, "cotacao", "mobilia", 2, true), pu("Iluminação (unidade-modelo)", 4, 1800, "estimativa", "mobilia"),
        pu("Cozinha compacta e eletrodomésticos (unidade-modelo)", 4, 5400, "cotacao", "mobilia", 3, true), c("Equipamentos da lavanderia", 9000, 2, true)],
      5: [enx, pu("Utensílios de cozinha de cada unidade", 4, 500, "estimativa", "mobilia"), e("Governança e limpeza", 800), e("Manutenção", 500), br("Segurança"), recepcao],
      6: [br("Licença de funcionamento e cadastros"), c("Fotos e site", 6500, 2, true), e("Identidade e marketing de lançamento", 8000), e("Treinamento e contratação", 4000), br("Seguro do primeiro ano"), e("Abertura de teste", 2500)],
    };
    var C = calcular(E, hoje);
    var s = acaoSugerida(E, C, alertas(E, C));
    E.acao30 = s.acao; E.verificacao = s.verificacao;
    return E;
  }

  /* ------------------------------------------------------------------
     10. Textos fixos e varredura de promessas proibidas
     ------------------------------------------------------------------ */
  var TEXTOS = {
    promessa: "Aprenda o passo a passo para calcular quanto custa o seu projeto inteiro, bloco por bloco e com a origem de cada número, antes de assinar qualquer obra.",
    aviso: "Material educativo. Não é orçamento, projeto nem estudo de viabilidade definitivo. Custos, licenças e impostos se confirmam com engenheiro, arquiteto, prefeitura e contador. Esta ficha não substitui engenheiro, arquiteto ou contador.",
    capex: "CAPEX é o custo de abrir a porta: tudo o que se gasta para a fase começar a receber hóspedes.",
    tempo: "Em uma tarde você termina a primeira versão, com estimativas e linhas em branco. Trocar as linhas por cotação leva o tempo dos fornecedores.",
    naoPromete: "A lição não promete aprovação, crédito, parceria, retorno nem prazo de obra.",
    exemplo: ROTULO_EXEMPLO,
  };
  var PROIBIDAS = [/garant/i, /lucro certo/i, /retorno garantido/i, /sucesso garantido/i, /vai faturar/i, /renda (certa|garantida|passiva)/i, /ocupa[cç][aã]o garantida/i, /valoriza[cç][aã]o (certa|garantida)/i, /sem risco/i, /enriquec/i, /fique rico/i];
  function textoSeguro(s) { return !PROIBIDAS.some(function (re) { return re.test(String(s)); }); }

  var api = {
    NS: NS, LIMITES: LIMITES, SITUACOES: SITUACOES, TIPOS: TIPOS, DIAG: DIAG, FATORES: FATORES, ORIGENS: ORIGENS, MODOS: MODOS, FORMAS: FORMAS, TAGS: TAGS, TERRENO: TERRENO, BLOCOS: BLOCOS, REGUA: REGUA,
    ORDEM_ALERTAS: ORDEM_ALERTAS, INFO: INFO, VERIFICACOES: VERIFICACOES, TELAS: TELAS, TEXTOS: TEXTOS, PROIBIDAS: PROIBIDAS, NOTA_FAIXA: NOTA_FAIXA,
    falta: falta, paraNumero: paraNumero, arred: arred, fmtNum: fmtNum, fmtN: fmtN, brl: brl, brl0: brl0, fmtPct: fmtPct, juntar: juntar, div: div, ehNS: ehNS,
    dataOk: dataOk, diasEntre: diasEntre, somaDias: somaDias, dataBR: dataBR,
    nomeBloco: nomeBloco, novaLinha: novaLinha, linhasSugeridas: linhasSugeridas, estadoInicial: estadoInicial,
    valorLinha: valorLinha, erroLinha: erroLinha, cotacaoCompleta: cotacaoCompleta, cotacaoVencida: cotacaoVencida, tipologias: tipologias, somaTipologias: somaTipologias, tipologiasConferem: tipologiasConferem,
    giroUsado: giroUsado, calcular: calcular, degrauDiagnostico: degrauDiagnostico, notaP6: notaP6, transposicao: transposicao,
    alertas: alertas, tresPrimeiros: tresPrimeiros, acaoSugerida: acaoSugerida, proximaEtapa: proximaEtapa,
    leituraLinhasCotadas: leituraLinhasCotadas, leituraReserva: leituraReserva, leituraPalpite: leituraPalpite, leituraDegrau: leituraDegrau,
    validarTela: validarTela, prazoOk: prazoOk, criterio: criterio, resumoDados: resumoDados, exemplo: exemplo, textoSeguro: textoSeguro,
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else raiz.ZCAPEX = api;
})(typeof window !== "undefined" ? window : this);

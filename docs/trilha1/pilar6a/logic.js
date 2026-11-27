/* Trilha 1 · Pilar 6 · Aprofundamento 6A · CAPEX
   Ficha "Faça agora · O seu CAPEX" (página 6A do Dossiê de Desenvolvimento, irmã da página 6).
   Lógica pura, sem DOM: roda no navegador (window.ZCAPEX) e no Node (testes).
   Regra: toda conta, alerta e texto de leitura que a ficha mostra sai daqui, para ser testado.
   Fonte das regras: producao/trilha1-aprofundamento/01-capex/PLANO.md (versão 2), seções 6 e 7.
   "Não sei" é sempre o texto "nao_sei", nunca um zero escondido. A ficha nunca insere valor de referência.
   No código e na tela: "parte" (1 a 7), não "bloco". */
(function (raiz) {
  "use strict";

  /* ------------------------------------------------------------------
     1. Leitura e formatação pt-BR (as mesmas regras da ficha do Pilar 6)
     ------------------------------------------------------------------ */
  var NS = "nao_sei";
  var NAO_FIZ = "nao_fiz";
  function falta(v) {
    if (v === undefined || v === null) return true;
    if (v === NS || v === NAO_FIZ) return true;
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
  function ehNaoFiz(v) { return v === NAO_FIZ; }
  function txt(v) { return typeof v === "string" ? v.trim() : ""; }
  function inteiro(v) { var n = paraNumero(v); return n !== null && Math.floor(n) === n ? n : null; }
  var EPS = 1e-12;
  function entre(x, lo, hi) { return x >= lo - EPS && x <= hi + EPS; }
  function minusculaInicial(s) { s = txt(s); return s ? s.charAt(0).toLowerCase() + s.slice(1) : s; }
  var POR_EXTENSO = ["zero", "uma", "duas", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez"];
  function extenso(n) { return n >= 0 && n <= 10 ? POR_EXTENSO[n] : String(n); }

  /* Datas em "AAAA-MM-DD"; a lógica recebe "hoje" como parâmetro. */
  function dataOk(iso) { return typeof iso === "string" && /^\d{4}-\d{2}-\d{2}$/.test(iso) && !isNaN(Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10))); }
  function diaUTC(iso) { return Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10)); }
  function diasEntre(de, ate) { if (!dataOk(de) || !dataOk(ate)) return null; return Math.round((diaUTC(ate) - diaUTC(de)) / 86400000); }
  function somaDias(iso, n) { var d = new Date(diaUTC(iso) + n * 86400000); return d.toISOString().slice(0, 10); }
  /** Número em texto pt-BR para um campo de digitação ("690.529,18", "3", "600.000"). */
  function numTexto(v) { var r = arred(v, 2); return Math.floor(r) === r ? fmtNum(r, 0) : fmtNum(r, 2); }
  function dataBR(iso) { return dataOk(iso) ? iso.split("-").reverse().join("/") : ""; }

  /* ------------------------------------------------------------------
     2. Dados da ficha (perguntas, opções, partes, linhas sugeridas)
     ------------------------------------------------------------------ */
  /* As três situações com as palavras exatas do Marco Zero (docs/trilha1/marco-zero, chave zion-t1-marco-zero). */
  var SITUACOES = [
    { v: "terreno", r: "Tenho um terreno e ainda não hospedo ninguém", duas: "Se você ainda não hospeda" },
    { v: "ideia", r: "Tenho uma ideia, ou o capital, e ainda não tenho o terreno", duas: "Se você ainda não hospeda" },
    { v: "opero", r: "Já opero uma hospedagem e quero crescer", duas: "Se você já opera e quer crescer" },
  ];
  var TIPOS = [
    { v: "casa", r: "Casa ou apartamento" }, { v: "cabanas", r: "Cabanas ou chalés" }, { v: "glamping", r: "Glamping (bolha, domo, tenda)" },
    { v: "pousada", r: "Pousada" }, { v: "outro", r: "Outro" },
  ];
  /* Diagnóstico sobre a página 6 (PLANO 6.1, tela 0). */
  var DIAG = [
    { id: "d1", p: "A sua página 6 tem:", op: [{ v: "cotacao", r: "A maioria das linhas com cotação" }, { v: "referencia", r: "Referência ou estimativa" }, { v: "naoFiz", r: "Ainda não fiz a página 6" }] },
    { id: "d2", p: "A página 6 já inclui infraestrutura comum, áreas comuns e pré-abertura?", op: [{ v: "todas", r: "Todas" }, { v: "algumas", r: "Algumas" }, { v: "nenhuma", r: "Nenhuma" }, { v: "naoSei", r: "Não sei" }] },
    { id: "d3", p: "Quantas linhas têm cotação escrita?", op: [{ v: "maioria", r: "A maioria" }, { v: "algumas", r: "Algumas" }, { v: "nenhuma", r: "Nenhuma" }] },
    { id: "d4", p: "A reserva do imprevisto tem regra de uso escrita?", op: [{ v: "sim", r: "Sim" }, { v: "nao", r: "Não" }] },
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
    { v: "branco", r: "Em branco, ainda sem número", notaP6: NS },
    { v: "naoAplica", r: "Não se aplica", notaP6: null },
  ];
  var MODOS = [
    { v: "valor", r: "Valor total" },
    { v: "qtdUnit", r: "Quantidade × valor de cada" },
    { v: "area", r: "Quantidade × área × custo do m²" },
  ];
  var FORMAS = [
    { v: "construida", r: "Construída (por área × custo do m²)", modo: "area" },
    { v: "pronta", r: "Estrutura pronta (bolha, domo, cabana pré-fabricada: preço por unidade)", modo: "qtdUnit" },
    { v: "adequacao", r: "Imóvel existente a adequar (por unidade)", modo: "qtdUnit" },
  ];
  var TAGS = ["unidade", "deck", "piso", "luz", "agua", "mobilia"];
  var TERRENO = [
    { v: "meu", r: "Já é meu" }, { v: "comprar", r: "Vou comprar" },
    { v: "parceria", r: "Permuta, sociedade ou arrendamento" }, { v: "naoSei", r: "Não sei" },
  ];
  var PARTES = [
    { n: 1, nome: "Projetos, licenças e documentação" },
    { n: 2, nome: "Infraestrutura" },
    { n: 3, nome: "Unidades e áreas comuns", nomePronto: "Adequação e reforma" },
    { n: 4, nome: "Mobiliário e equipamentos" },
    { n: 5, nome: "Enxoval, utensílios e suprimentos" },
    { n: 6, nome: "Pré-abertura" },
    { n: 7, nome: "Reserva do imprevisto" },
  ];
  function nomeParte(n, E) { var b = PARTES[n - 1]; return n === 3 && E && E.imovelPronto === true ? b.nomePronto : b.nome; }
  var REGUA = [
    { v: "Sonhador", t: "Ainda é um sonho com preço: falta montar a conta parte por parte." },
    { v: "Estimador", t: "A conta existe, mas a maior parte das linhas ainda é estimativa ou está em branco." },
    { v: "Calculista", t: "A maioria das linhas tem cotação escrita, e as três maiores também." },
    { v: "Developer", t: "Não é atribuído nesta ficha: ele pede cronograma de desembolso e captação, que ficam no Pilar 7." },
  ];
  var LIMITES = { dinheiroMax: 100000000, unidadesMax: 200, qtdMax: 999, linhasMax: 15, tipologiasMax: 3, areaMin: 0.1, areaMax: 10000, distMax: 50000, redeMax: 999, giroMesesMax: 24, camasMax: 10, reservaMax: 50, validadeDias: 90, prazoDias: 30, regraMin: 10, regraMax: 200 };

  /* Linhas sugeridas: somente nomes, nunca valor (PLANO 6.1). */
  var _seq = 0;
  function novaLinha(o) {
    _seq += 1;
    var l = { id: o.id || ("l" + Date.now().toString(36) + _seq), nome: o.nome || "", modo: o.modo || "valor", qtd: "", valor: "", valorUnit: "", areaM2: "", custoM2: "", origem: null, nCotacoes: null, mesmaEspec: false, dataCotacao: "", tagP6: o.tagP6 || null };
    if (o.curto) l.curto = o.curto;
    if (o.porUnidade) l.porUnidade = true;
    if (o.comum) l.comum = true;
    if (o.geral) l.geral = true;
    if (o.tipologia) { l.tipologia = true; l.forma = o.forma || "construida"; l.modo = (FORMAS.filter(function (f) { return f.v === l.forma; })[0] || FORMAS[0]).modo; l.tagP6 = "unidade"; l.porUnidade = true; l.freteMontagemConfirmados = false; }
    if (o.enxoval) { l.enxoval = true; l.modo = "enxoval"; l.camasPorUnidade = ""; l.custoJogo = ""; }
    return l;
  }
  function linhasSugeridas(p, E) {
    E = E || {};
    var pu = function (nome, tag) { return { nome: nome, modo: "qtdUnit", porUnidade: true, tagP6: tag || null }; };
    var v = function (nome, o) { var x = { nome: nome, modo: "valor" }; if (o) for (var k in o) x[k] = o[k]; return x; };
    var L;
    if (p === 1) L = [v("Levantamento topográfico e sondagem"), v("Arquitetura"), v("Projetos complementares (estrutural, elétrico, hidrossanitário)"), v("Aprovação na prefeitura e taxas"), v("Licença ambiental, se houver"), v("Responsabilidade técnica e registros")];
    else if (p === 2) {
      L = [v("Acesso interno"), v("Estacionamento e vaga de serviço"), v("Caminhos"), v("Energia (rede comum até as unidades)"), v("Água"), v("Esgoto e tratamento"), v("Drenagem"), v("Internet"), pu("Ligação de luz de cada unidade", "luz"), pu("Água e esgoto de cada unidade", "agua")];
      if (E.situacao === "opero") L.unshift(v("Reforço da rede existente"));
    } else if (p === 3) {
      if (E.imovelPronto === true) L = [{ nome: "Adequação de cada unidade", tipologia: true, forma: "adequacao" }, v("Áreas comuns a adequar", { comum: true })];
      else L = [{ nome: "Unidade tipo 1", tipologia: true, forma: E.tipo === "glamping" ? "pronta" : "construida" }, pu("Deck de cada unidade", "deck"), pu("Piso de cada unidade (se não estiver no m²)", "piso"),
        { nome: "Apoio (rouparia, depósito, lixo, copa e vestiário)", modo: "area", comum: true }, v("Lavanderia", { comum: true }), v("Recepção", { comum: true }), v("Deck comum", { comum: true }), v("Trilhas", { comum: true }), v("Casa de máquinas", { comum: true })];
    } else if (p === 4) L = [pu("Cama e colchão (unidade-modelo)", "mobilia"), pu("Mobiliário (unidade-modelo)", "mobilia"), pu("Iluminação (unidade-modelo)", "mobilia"), pu("Cozinha compacta e eletrodomésticos (unidade-modelo)", "mobilia"), pu("Banheiro (unidade-modelo)", "mobilia"), pu("Mobiliário do deck (unidade-modelo)", "mobilia"), v("Equipamentos gerais (apoio, lavanderia, áreas comuns)", { geral: true })];
    else if (p === 5) L = [{ nome: "Enxoval (três jogos por cama)", enxoval: true, tagP6: "mobilia" }, pu("Utensílios de cada unidade", "mobilia"), v("Governança e limpeza"), v("Recepção"), v("Manutenção"), v("Segurança"), v("Amenidades e suprimentos iniciais")];
    else if (p === 6) L = [v("Licença de funcionamento e cadastros"), v("Fotos e anúncio"), v("Identidade e lançamento"), v("Treinamento e manual de operação"), v("Seguro do primeiro ano"), v("Abertura de teste")];
    else L = [];
    return L.map(function (o) { if (p === 5 && !o.tagP6) o.tagP6 = "mobilia"; return novaLinha(o); });
  }
  function estadoInicial(hoje) {
    return {
      nome: "", projeto: "", cidadeUF: "", situacao: null, paraOutro: false, tipo: null, imovelPronto: false, d1: null, d2: null, d3: null, d4: null, turma: "autonomo",
      pagina6Total: "", pagina6Data: "", pagina6Infra: "", limite6: "", pagina6ResultadoCons: "", pagina6GiroMeses: "",
      unidadesFase: "", unidadesProjeto: "", fatoresRisco: [], primeiraObra: null,
      partes: { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [] },
      distanciaEnergiaM: "", infraDimensionadaPara: "", infraProjetoCompleto: "", enxovalNaoDuplicado: false,
      reservaPct: "", regraParaQue: "", regraQuemAutoriza: "", regraComoRegistra: "", regraQuandoConfere: "",
      giro: "", giroMeses: "", giroCustoMensal: "", giroZeroJustificativa: "", terrenoSituacao: null, terrenoValor: "",
      acao30: "", acaoEditada: false, prazo: "", verificacao: "", pdfBaixado: false, exemplo: false, hoje: hoje || "",
    };
  }
  /** Converte respostas salvas pela versão 1 desta ficha (blocos, contingência, situações antigas). */
  function migrar(r) {
    if (!r || typeof r !== "object") return r;
    if (r.blocos && !r.partes) { r.partes = r.blocos; }
    delete r.blocos;
    if (r.contingenciaPct !== undefined && (r.reservaPct === undefined || r.reservaPct === "")) r.reservaPct = r.contingenciaPct;
    delete r.contingenciaPct;
    var sit = { abrir: "terreno", ampliar: "opero", operador: "terreno" };
    if (sit[r.situacao]) { if (r.situacao === "operador") r.paraOutro = true; r.situacao = sit[r.situacao]; }
    var d1 = { numero: "cotacao", palpite: "referencia", nao: "naoFiz" }; if (d1[r.d1]) r.d1 = d1[r.d1];
    var d2 = { tudo: "todas", alguns: "algumas", soUnidade: "nenhuma" }; if (d2[r.d2]) r.d2 = d2[r.d2];
    return r;
  }

  /* ------------------------------------------------------------------
     3. Leituras de outras páginas do Dossiê (tolerantes: se falhar, fica vazio)
     ------------------------------------------------------------------ */
  function objetoDe(raw) {
    var d = raw;
    if (typeof raw === "string") { try { d = JSON.parse(raw); } catch (e) { d = null; } }
    return d && typeof d === "object" && !Array.isArray(d) ? d : null;
  }
  /** Página 6 (chave zion-t1-pilar6): resumo.dados (ou dados na raiz) e resumo.data. */
  function lerPagina6(raw) {
    var d = objetoDe(raw);
    if (!d) return null;
    var dados = (d.resumo && typeof d.resumo === "object" && d.resumo.dados) || (d.dados && typeof d.dados === "object" ? d.dados : null) || {};
    var resp = d.respostas && typeof d.respostas === "object" ? d.respostas : {};
    var num = function (k) { return paraNumero(dados[k]); };
    var data = String((d.resumo && d.resumo.data) || d.data || "").slice(0, 10);
    var rc = num("resultado_cons"), inv8 = num("inv8");
    var perfil = d.perfil && typeof d.perfil === "object" ? d.perfil : {};
    var P = {
      total: num("total"), total_sem_giro: num("total_sem_giro"), soma_folha: num("soma_folha"), infra: num("infra"),
      giro: num("giro"), giro_meses: num("giro_meses"), terreno: num("terreno"), unidades: inteiro(dados.unidades),
      resultado_cons: rc, inv8: inv8, limite: inv8 !== null ? inv8 : (rc !== null ? 8 * rc : null),
      reserva_pct: paraNumero(dados.reserva_pct) !== null ? paraNumero(dados.reserva_pct) : paraNumero(resp.reserva_pct),
      data: dataOk(data) ? data : "", nome: txt(perfil.nome), cidade: txt(perfil.cidade), uf: txt(perfil.uf),
    };
    P.temDados = ["total", "total_sem_giro", "soma_folha", "giro", "inv8", "resultado_cons"].some(function (k) { return P[k] !== null; });
    return P;
  }
  /** Marco Zero (chave zion-t1-marco-zero): situação e nome. */
  function lerMarcoZero(raw) {
    var d = objetoDe(raw);
    if (!d) return null;
    var s = d.situacao || (d.respostas && d.respostas.situacao) || "";
    return { situacao: SITUACOES.some(function (x) { return x.v === s; }) ? s : null, nome: txt(d.nome || (d.perfil && d.perfil.nome)) };
  }
  /** Preenche só os campos vazios com o que veio da página 6. Devolve { campo: "página 6" } do que foi preenchido. */
  function aplicarPagina6(E, P, hoje) {
    var veio = {};
    if (!E || !P) return veio;
    var poe = function (campo, v) { if (v === null || v === undefined || v === "") return; if (!falta(E[campo]) || ehNS(E[campo]) || ehNaoFiz(E[campo])) return; E[campo] = typeof v === "number" ? numTexto(v) : v; veio[campo] = "página 6"; };
    poe("pagina6Total", P.total);
    if (P.data && (!hoje || diasEntre(P.data, hoje) >= 0)) poe("pagina6Data", P.data);
    poe("pagina6Infra", P.infra);
    poe("limite6", P.limite);
    poe("pagina6ResultadoCons", P.resultado_cons);
    poe("pagina6GiroMeses", P.giro_meses);
    poe("unidadesFase", P.unidades);
    poe("giro", P.giro);
    poe("terrenoValor", P.terreno);
    poe("reservaPct", P.reserva_pct);
    if (P.cidade) poe("cidadeUF", P.cidade + (P.uf ? "/" + P.uf : ""));
    return veio;
  }
  /** O limite da página 6: o número digitado; se faltar (sem "Não sei"), 8 × o resultado conservador. */
  function limiteEfetivo(E) {
    if (!E || ehNS(E.limite6)) return null;
    var l = paraNumero(E.limite6);
    if (l !== null) return l;
    var rc = paraNumero(E.pagina6ResultadoCons);
    return rc !== null ? 8 * rc : null;
  }

  /* ------------------------------------------------------------------
     4. Linhas: valor, validação, contagens
     ------------------------------------------------------------------ */
  function comValor(l) { return !!l && (l.origem === "cotacao" || l.origem === "estimativa"); }
  function ativa(l) { return !!l && l.origem !== "naoAplica"; }
  function dinheiroOk(x) { return x !== null && x > 0 && x <= LIMITES.dinheiroMax; }
  function qtdDe(l, E) {
    var q = inteiro(l.qtd);
    if (q === null && falta(l.qtd) && l.porUnidade) q = inteiro(E.unidadesFase);
    return q;
  }
  function qtdMaxDe(l) { return l.tipologia ? LIMITES.unidadesMax : LIMITES.qtdMax; }
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
    if (q === null || q < 1 || q > qtdMaxDe(l)) return null;
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
      var q = qtdDe(l, E), mx = qtdMaxDe(l);
      if (q === null || q < 1 || q > mx) return "Em \"" + n + "\": a quantidade vai de 1 a " + fmtNum(mx, 0) + ", sem casas decimais.";
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
  function linhasDe(E, p) { return (E && E.partes && Array.isArray(E.partes[p])) ? E.partes[p] : []; }
  function todasLinhas(E) { var r = []; for (var p = 1; p <= 6; p++) linhasDe(E, p).forEach(function (l) { r.push({ p: p, l: l }); }); return r; }
  function tipologias(E) { return linhasDe(E, 3).filter(function (l) { return l.tipologia && ativa(l); }); }
  function somaTipologias(E) { return tipologias(E).reduce(function (s, l) { var q = qtdDe(l, E); return s + (q || 0); }, 0); }
  function parteInteiraNA(E, p) { var L = linhasDe(E, p); return L.length > 0 && L.every(function (l) { return l.origem === "naoAplica"; }); }
  function parte2Ativa(E) { return linhasDe(E, 2).some(ativa); }
  /** A17: as tipologias precisam somar as unidades da fase (salvo imóvel pronto sem tipologia). */
  function tipologiasConferem(E) {
    var u = inteiro(E.unidadesFase);
    var tip = tipologias(E);
    if (E.imovelPronto === true && tip.length === 0) return true;
    if (u === null) return false;
    return somaTipologias(E) === u;
  }
  function calculadoraGiroUsada(E) { return paraNumero(E.giroMeses) !== null && paraNumero(E.giroCustoMensal) !== null; }
  function giroUsado(E) {
    if (calculadoraGiroUsada(E)) return paraNumero(E.giroMeses) * paraNumero(E.giroCustoMensal);
    if (ehNS(E.giro)) return null;
    return paraNumero(E.giro);
  }
  function reservaPctDe(E) { var p = paraNumero(E.reservaPct); return p !== null && p > 0 ? p : 0; }
  function temFator(E) { return Array.isArray(E.fatoresRisco) && E.fatoresRisco.length > 0; }
  function nomeCurto(l) { return txt(l.curto) || minusculaInicial(l.nome); }

  /* ------------------------------------------------------------------
     5. O cálculo (PLANO 6.2)
     ------------------------------------------------------------------ */
  function calcular(E, hoje) {
    E = E || {};
    hoje = hoje || E.hoje || "";
    var C = { totalParte: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0 }, linhasInvalidas: [] };
    var valorados = [];
    var nLinhas = 0, nCotadas = 0, nEstimadas = 0, nBranco = 0, nNaoAplica = 0, valorCotado = 0, valorEstimado = 0;
    var n3 = 0, nInc = 0, vencidas = [], incompletas = [], brancos = [];
    var porParte = {};
    for (var p = 1; p <= 6; p++) porParte[p] = { nLinhas: 0, nCotadas: 0, nEstimadas: 0, nBranco: 0, nNaoAplica: 0, nComValor: 0, nAtivas: 0, cotado: 0, estimado: 0 };
    todasLinhas(E).forEach(function (x) {
      var l = x.l, pp = porParte[x.p];
      var v = valorLinha(l, E);
      if (v === null) { C.linhasInvalidas.push({ p: x.p, nome: txt(l.nome) }); v = 0; }
      C.totalParte[x.p] += v;
      if (ativa(l) && l.origem) pp.nAtivas += 1;
      if (l.origem === "cotacao" || l.origem === "estimativa" || l.origem === "branco") { nLinhas += 1; pp.nLinhas += 1; }
      if (comValor(l) && v > 0) { pp.nComValor += 1; valorados.push({ p: x.p, nome: txt(l.nome), valor: v, origem: l.origem, curto: nomeCurto(l) }); }
      if (l.origem === "cotacao") {
        nCotadas += 1; pp.nCotadas += 1; valorCotado += v; pp.cotado += v;
        if (cotacaoCompleta(l)) n3 += 1; else { nInc += 1; incompletas.push({ p: x.p, nome: txt(l.nome), n: Number(l.nCotacoes) || 0 }); }
        if (cotacaoVencida(l, hoje)) vencidas.push({ p: x.p, nome: txt(l.nome), curto: nomeCurto(l), dias: diasEntre(l.dataCotacao, hoje) });
      } else if (l.origem === "estimativa") { nEstimadas += 1; pp.nEstimadas += 1; valorEstimado += v; pp.estimado += v; }
      else if (l.origem === "branco") { nBranco += 1; pp.nBranco += 1; brancos.push({ p: x.p, nome: txt(l.nome), curto: nomeCurto(l) }); }
      else if (l.origem === "naoAplica") { nNaoAplica += 1; pp.nNaoAplica += 1; }
    });
    var subtotal = 0; for (p = 1; p <= 6; p++) subtotal += C.totalParte[p];
    var pct = reservaPctDe(E);
    var reserva = subtotal * pct / 100;
    C.totalParte[7] = reserva;
    var capexFase = subtotal + reserva;
    var pctParte = {}; for (p = 1; p <= 7; p++) pctParte[p] = capexFase > 0 ? C.totalParte[p] / capexFase : null;
    var obra = C.totalParte[2] + C.totalParte[3];
    var u = inteiro(E.unidadesFase);
    var giro = giroUsado(E);
    var investimentoTotal = giro === null ? null : capexFase + giro;
    // área total da Parte 3 (tipologias, extras com área e áreas comuns)
    var areaTotal = 0, faltaAreaTip = false, temArea = false;
    linhasDe(E, 3).forEach(function (l) {
      if (!ativa(l)) return;
      var a = areaDe(l), q = l.modo === "valor" ? (inteiro(l.qtd) || 1) : qtdDe(l, E);
      if (a !== null && q !== null) { areaTotal += q * a; temArea = true; }
      else if (l.tipologia) faltaAreaTip = true;
    });
    if (faltaAreaTip || !temArea) areaTotal = null;
    var top3 = valorados.slice().sort(function (a, c) { return c.valor - a.valor; }).slice(0, 3);
    var pctLinhasCotadas = div(nCotadas, nLinhas);
    var degrau;
    var soParte3 = capexFase > 0 && [1, 2, 4, 5, 6].every(function (k) { return C.totalParte[k] === 0; });
    if (capexFase === 0 || soParte3) degrau = "Sonhador";
    else if (pctLinhasCotadas !== null && pctLinhasCotadas > 0.5 + EPS && top3.length > 0 && top3.every(function (x) { return x.origem === "cotacao"; })) degrau = "Calculista";
    else degrau = "Estimador";
    var infraPC = paraNumero(E.infraProjetoCompleto);
    var infraFutura = infraPC !== null && infraPC - C.totalParte[2] >= 0 ? infraPC - C.totalParte[2] : null;
    // página 6 × 6A e o limite da página 6
    var p6 = ehNaoFiz(E.pagina6Total) ? null : paraNumero(E.pagina6Total);
    var limite = limiteEfetivo(E);
    var folga6 = limite !== null && investimentoTotal !== null ? limite - investimentoTotal : null;
    var dentro = folga6 !== null ? folga6 >= -EPS : null;

    C.subtotal = subtotal; C.reservaPct = pct; C.reserva = reserva; C.capexFase = capexFase;
    C.pctParte = pctParte; C.obra = obra; C.pctObra = div(obra, capexFase);
    C.custoPorUnidade = u ? div(capexFase, u) : null;
    C.giro = giro; C.investimentoTotal = investimentoTotal; C.investimentoPorUnidade = u && investimentoTotal !== null ? div(investimentoTotal, u) : null;
    C.areaTotal = areaTotal; C.custoPorM2 = areaTotal ? div(capexFase, areaTotal) : null;
    C.nLinhas = nLinhas; C.nCotadas = nCotadas; C.nEstimadas = nEstimadas; C.nBranco = nBranco; C.nNaoAplica = nNaoAplica;
    C.pctLinhasCotadas = pctLinhasCotadas; C.faltamParaMaioria = Math.max(0, Math.floor(nLinhas / 2) + 1 - nCotadas);
    C.valorCotado = valorCotado; C.valorEstimado = valorEstimado; C.pctValorCotado = div(valorCotado, subtotal);
    C.n3Cotacoes = n3; C.nCotacoesIncompletas = nInc; C.incompletas = incompletas; C.cotacoesVencidas = vencidas.length; C.vencidas = vencidas; C.brancos = brancos;
    C.oseSobreFFE = div(C.totalParte[5], C.totalParte[4]);
    C.preAberturaSobreObra = div(C.totalParte[6], obra);
    C.faltaPreAbertura = obra > 0 ? Math.max(0, 0.05 * obra - C.totalParte[6]) : null;
    C.pagina6Total = p6; C.pagina6Cobre = p6 !== null && investimentoTotal !== null ? div(p6, investimentoTotal) : null;
    C.difPagina6 = p6 !== null && investimentoTotal !== null ? investimentoTotal - p6 : null;
    C.limite6 = limite; C.folga6 = folga6; C.dentroLimite = dentro;
    C.folgaEmSubtotal = dentro === true ? folga6 / (1 + pct / 100) : null;
    C.folgaPctCapex = folga6 !== null ? div(folga6, capexFase) : null;
    C.infraFutura = infraFutura; C.top3 = top3; C.degrau = degrau; C.degrauDiagnostico = degrauDiagnostico(E);
    C.porParte = porParte; C.terreno = ehNS(E.terrenoValor) ? null : paraNumero(E.terrenoValor);
    C.transposicao = transposicao(E, C);
    C.planilha1 = planilha1(E, C);
    return C;
  }
  /** Degrau pelas respostas do diagnóstico sobre a página 6 (elaboração própria, rotulada). */
  function degrauDiagnostico(E) {
    if (!E || !E.d1) return null;
    if (E.d1 === "naoFiz") return "Sonhador";
    if (E.d1 === "cotacao" && E.d3 === "maioria") return "Calculista";
    return "Estimador";
  }
  function notaP6(origem) { var o = ORIGENS.filter(function (x) { return x.v === origem; })[0]; return o ? o.notaP6 : null; }

  /** Em que campo da ficha do Pilar 6 cada linha entra (o resto vai para a infraestrutura comum). */
  function campoP6(x) {
    var t = x.l.tagP6;
    if (x.p === 1) return "licencas";
    if (t === "unidade" && x.p === 3) return "l_unidade";
    if (t === "deck") return "l_deck";
    if (t === "piso") return "l_piso";
    if (t === "luz") return "l_luz";
    if (t === "agua") return "l_agua";
    if ((t === "mobilia" && x.p === 4) || x.p === 5) return "l_mobilia";
    return "infra";
  }
  var CAMPOS_P6 = ["l_unidade", "l_deck", "l_luz", "l_agua", "l_mobilia", "l_piso", "licencas", "infra"];
  /** Quadro "Como levar para a página 6" (PLANO 6.2). Nada é gravado na ficha do Pilar 6. */
  function transposicao(E, C) {
    var u = inteiro(E.unidadesFase);
    if (!u) return null;
    var soma = {}, grupo = {};
    CAMPOS_P6.forEach(function (k) { soma[k] = 0; grupo[k] = []; });
    todasLinhas(E).forEach(function (x) {
      var k = campoP6(x);
      soma[k] += valorLinha(x.l, E) || 0;
      if (ativa(x.l) && x.l.origem) grupo[k].push(x.l.origem);
    });
    var temPiso = grupo.l_piso.some(function (o) { return o === "cotacao" || o === "estimativa"; }) && soma.l_piso > 0;
    var T = {
      unidades: u,
      l_unidade: soma.l_unidade / u, l_deck: soma.l_deck / u, l_piso: soma.l_piso / u, l_luz: soma.l_luz / u, l_agua: soma.l_agua / u,
      l_mobilia: soma.l_mobilia / u, pisoNoM2: !temPiso,
      licencas: C.totalParte[1], reserva_pct: C.reservaPct,
      giro_meses: paraNumero(E.pagina6GiroMeses), giro: C.giro, terreno: C.terreno,
    };
    T.pronta = T.l_unidade + T.l_deck + T.l_luz + T.l_agua + T.l_mobilia + T.l_piso;
    var unidadesProntas = u * T.pronta;
    T.infra = (C.subtotal - unidadesProntas - C.totalParte[1]) + C.reservaPct / 100 * (C.subtotal - unidadesProntas);
    T.conferencia = unidadesProntas * (1 + C.reservaPct / 100) + T.licencas + T.infra;
    T.confere = Math.abs(T.conferencia - C.capexFase) <= 0.01;
    // nota de cada campo: 3 só se todas as linhas forem cotação; "Não sei" se houver linha em branco e o campo valer 0; senão 1
    T.notas = {};
    var valorCampo = { l_unidade: T.l_unidade, l_deck: T.l_deck, l_luz: T.l_luz, l_agua: T.l_agua, l_mobilia: T.l_mobilia, l_piso: T.l_piso, licencas: T.licencas, infra: T.infra };
    CAMPOS_P6.forEach(function (k) {
      var g = grupo[k];
      if (!g.length) T.notas[k] = null;
      else if (g.indexOf("branco") >= 0 && Math.abs(valorCampo[k]) < 0.005) T.notas[k] = NS;
      else if (g.every(function (o) { return o === "cotacao"; })) T.notas[k] = 3;
      else T.notas[k] = 1;
    });
    return T;
  }
  /** Resumo "Se você usa a Planilha 1" (PLANO 6.2; elaboração própria a partir do gerador da Planilha 1). */
  function planilha1(E, C) {
    var R = { premissas: 0, infraestrutura: 0, ffe: 0, ose: 0 };
    todasLinhas(E).forEach(function (x) {
      var v = valorLinha(x.l, E) || 0, l = x.l;
      if (x.p === 1 || x.p === 2 || x.p === 6) R.infraestrutura += v;
      else if (x.p === 3) {
        if (l.tipologia) { if (l.forma === "pronta") R.ffe += v; else R.premissas += v; }
        else if (l.tagP6 === "deck" || l.tagP6 === "piso") R.premissas += v;
        else R.infraestrutura += v;
      } else if (x.p === 4) { if (l.tagP6 === "mobilia") R.ffe += v; else R.ose += v; }
      else if (x.p === 5) R.ose += v;
    });
    R.subtotal = R.premissas + R.infraestrutura + R.ffe + R.ose;
    R.contingenciaPct = C.reservaPct; R.contingencia = C.reserva;
    R.total = R.subtotal + C.reserva;
    R.confere = Math.abs(R.subtotal - C.subtotal) <= 0.01 && Math.abs(R.total - C.capexFase) <= 0.01;
    R.contingenciaPctTotal = div(C.reserva, R.total);
    return R;
  }
  /** Quadro fixo "partes da 6A → abas da Planilha 1". */
  var PL1_MAPA = [
    { parte: "Parte 1 · Projetos, licenças e documentação", aba: "Infraestrutura (grupo 1)" },
    { parte: "Parte 2 · Infraestrutura", aba: "Infraestrutura (grupos 2 a 6)" },
    { parte: "Parte 3 · unidades construídas, decks e piso", aba: "Premissas (área, deck e custo do m² de cada tipologia)" },
    { parte: "Parte 3 · áreas comuns", aba: "Infraestrutura (grupo 7)" },
    { parte: "Parte 3 · estrutura pronta (bolha, domo, cabana pré-fabricada)", aba: "FF&E, linha «Bolha ou cabana (estrutura principal)»" },
    { parte: "Parte 4 · mobiliário da unidade-modelo", aba: "FF&E (mobiliário e equipamentos)" },
    { parte: "Parte 4 · equipamentos gerais", aba: "OS&E (itens de operação)" },
    { parte: "Parte 5 · Enxoval, utensílios e suprimentos", aba: "OS&E (enxoval, utensílios e suprimentos)" },
    { parte: "Parte 6 · Pré-abertura", aba: "Sem aba própria: linhas livres no fim da aba Infraestrutura, grupo 9, com «Pré-abertura · …» na coluna B" },
    { parte: "Parte 7 · Reserva do imprevisto", aba: "Premissas, célula B15 (contingência)" },
  ];
  var PL1_AVISO = "A Planilha 1 divide o CAPEX pela área das unidades (coberta mais deck, aba Premissas B16); a 6A divide pela área total da Parte 3, com as áreas comuns. Os dois números são diferentes e os dois estão certos: diga qual usou.";

  /* ------------------------------------------------------------------
     6. Alertas (PLANO 6.4): a ordem da lista é a prioridade
     ------------------------------------------------------------------ */
  var NOTA_FAIXA = "Faixa de conferência citada pela fonte; não é preço nem regra fixa.";
  var ORDEM_ALERTAS = ["A17", "A3z", "A21", "A1", "A22", "A6", "A7", "A8", "A2", "A11", "A12", "A3", "A4", "A5", "A9", "A10", "A15", "A13", "A14", "A23", "A16", "A18", "A19", "A20"];
  var INFO = {
    id: "INFO", tit: "Pergunte ao seu engenheiro e ao seu contador",
    engenheiro: ["O preço inclui mão de obra, encargos, administração e lucro (Benefícios e Despesas Indiretas, o BDI)?", "Quanto o frete e a montagem acrescentam neste terreno?", "Como o preço pode mudar até a compra (reajuste)?", "A rede está dimensionada para quantas unidades?", "Quem assina a responsabilidade técnica (Anotação ou Registro de Responsabilidade Técnica, ART ou RRT)?"],
    contador: ["Quais são os custos de aquisição do terreno (escritura, Imposto de Transmissão, o ITBI, registro e certidões)?", "Quais impostos incidem sobre a obra e a compra de equipamentos?", "Compra, permuta, sociedade ou arrendamento: o que muda em cada forma de entrada do terreno (com o advogado)?"],
    concessionaria: ["Concessionária: qual é o ponto e a tensão de energia mais próximos?", "Prefeitura: qual é a lista e o custo das licenças?"],
    naoEnvia: "Esta ficha não envia nada: o PDF fica só com você.",
  };
  function rotParte(p, E) { return "Parte " + p + " · " + nomeParte(p, E); }
  function alertas(E, C) {
    E = E || {}; C = C || calcular(E);
    var A = [];
    var add = function (id, tipo, tit, txt, fonte, extra) { var a = { id: id, tipo: tipo, tit: tit, txt: txt, fonte: fonte }; if (extra) for (var k in extra) a[k] = extra[k]; A.push(a); };
    var u = inteiro(E.unidadesFase), up = inteiro(E.unidadesProjeto);
    if (!tipologiasConferem(E)) add("A17", "bloqueia", "As tipologias não somam a fase", "As tipologias somam " + somaTipologias(E) + " unidades, e a fase tem " + (u === null ? "um número ainda não informado de" : u) + " unidades. Ajuste as quantidades na tela da Parte 3.", "validação");
    var pctBruto = paraNumero(E.reservaPct);
    if (pctBruto === null || pctBruto <= 0) add("A3z", "bloqueia", "A reserva nunca é zero", ehNS(E.reservaPct) ? "Você marcou Não sei na reserva do imprevisto. Confira os fatores de risco e escolha uma porcentagem: a reserva nunca é zero." : "A reserva do imprevisto está vazia ou em zero. Toda obra tem imprevisto: a reserva nunca é zero.", "Mapa de fontes 1.2 (A05, VOL05, P6, F01)");
    if (C.dentroLimite === false) add("A21", "critico", "Passou do limite da sua página 6", "O investimento total (" + brl(C.investimentoTotal) + ") passou do limite que a sua página 6 escreveu (" + brl(C.limite6) + ") em " + brl(-C.folga6) + ". O Pilar 7 diz o caminho: voltar à conta antes de assinar e ajustar o tamanho, o produto ou a fase.", "P6 cap. 07; P7");
    var a1 = [], a2 = [];
    for (var p = 1; p <= 6; p++) {
      var L = linhasDe(E, p), pp = C.porParte[p];
      var temNaoNA = L.some(function (l) { return l.origem !== "naoAplica"; });
      if (temNaoNA && pp.nComValor === 0) a1.push(p);
      if (pp.nComValor > 0 && pp.nCotadas === 0) a2.push(p);
    }
    if (a1.length) add("A1", "critico", a1.length === 1 ? "Parte " + a1[0] + " em branco" : "Partes em branco", (a1.length === 1 ? "A " + rotParte(a1[0], E) + " não tem nenhuma linha com valor." : "As Partes " + juntar(a1.map(String)) + " não têm nenhuma linha com valor.") + " Parte em branco só pode aumentar a conta.", "P6 (infraestrutura à parte); erros do A05 cap. 2", { partes: a1 });
    if (ehNaoFiz(E.pagina6Total)) add("A22", "atencao", "Falta a página 6", "A 6A é a página irmã da 6. Faça a página 6 no Pilar 6 para ter o limite e comparar. Você pode seguir aqui mesmo assim.", "GUIA 5.1");
    var ativo2 = parte2Ativa(E);
    var infraD = inteiro(E.infraDimensionadaPara);
    if (ativo2 && infraD !== null && up !== null && infraD < up) add("A6", "critico", "A rede ficou menor que o projeto", "A rede está dimensionada para " + infraD + " unidades, e o projeto completo tem " + up + ". Refazer vala e caminho na fase dois é a forma mais cara de economizar.", "R14 (A05 cap. 12; P6 cap. 04; F01 cap. 6)");
    if (ehNS(E.unidadesProjeto) || falta(E.unidadesProjeto) || (ativo2 && (ehNS(E.infraDimensionadaPara) || falta(E.infraDimensionadaPara)))) add("A7", "bloqueia", "Para quantas unidades a rede é pensada?", "Falta dizer quantas unidades o projeto completo terá e para quantas a rede é dimensionada. Sem isso, a infraestrutura da fase um não se confere.", "R11, R14");
    if (ativo2 && ehNS(E.distanciaEnergiaM)) add("A8", "ns", "Qual a distância até o ponto de energia?", "É a primeira pergunta do orçamento da infraestrutura. A concessionária local informa o ponto e a tensão.", "R12 (confirmar com a concessionária local)");
    if (a2.length) add("A2", "atencao", a2.length === 1 ? "Parte " + a2[0] + " sem nenhuma cotação" : "Partes sem nenhuma cotação", (a2.length === 1 ? "A " + rotParte(a2[0], E) + " tem valor, mas nenhuma linha com cotação escrita." : "As Partes " + juntar(a2.map(String)) + " têm valor, mas nenhuma linha com cotação escrita.") + " Por enquanto, é estimativa.", "R3, R5", { partes: a2 });
    if (C.preAberturaSobreObra !== null && C.preAberturaSobreObra < 0.05 - EPS) add("A11", "atencao", "Pré-abertura abaixo da faixa citada", "A pré-abertura é " + fmtPct(C.preAberturaSobreObra) + " da obra (Partes 2 e 3); a faixa citada vai de 5% a 10%. Faltam cerca de " + brl0(C.faltaPreAbertura) + " para os 5% da obra. Esquecer a pré-abertura é um dos cinco erros do orçamento amador. " + NOTA_FAIXA, "R21 (A05 caps. 2 e 7; F01 caps. 2 e 4)", { partes: [6] });
    if (C.pctObra !== null && C.pctObra > 0.8 + EPS) add("A12", "atencao", "A obra passa de 80% do custo", "Infraestrutura e unidades somam " + fmtPct(C.pctObra) + " do custo de abrir a porta: provavelmente faltou algo nas outras partes. " + NOTA_FAIXA, "R29 (A05 cap. 3; F01 cap. 6)", { partes: [1, 4, 5, 6] });
    var pr = pctBruto;
    var piso = E.imovelPronto === true ? 15 : 10;
    if (pr !== null && pr > 0 && pr < piso - EPS) add("A3", "atencao", "Reserva abaixo da faixa citada", "A reserva está em " + fmtN(pr, 2) + "%. A faixa citada vai de " + (E.imovelPronto === true ? "15% a 25% para imóvel pronto" : "10% a 15% do subtotal") + ". " + NOTA_FAIXA, "A05 caps. 3 e 7; VOL05 cap. 4; P6 cap. 03; PL1; JC02 P11; JC04 P04", { partes: [7] });
    if (pr !== null && pr > 0 && pr < 15 - EPS && (E.primeiraObra === true || temFator(E))) add("A4", "atencao", "Com primeira obra ou fator de risco, a fonte pede o teto", "Com " + (E.primeiraObra === true ? "a primeira obra" : "fator de risco") + (E.primeiraObra === true && temFator(E) ? " e fator de risco" : "") + ", a fonte pede a reserva no teto da faixa (15%) ou acima. Hoje ela está em " + fmtN(pr, 2) + "%.", "A05 cap. 7; R22; P6 cap. 03", { partes: [7] });
    if (pr !== null && pr > 25 + EPS) add("A5", "atencao", "Reserva acima de todas as faixas citadas", "A reserva está em " + fmtN(pr, 2) + "%. Confira se ela não está cobrindo linha esquecida ou escopo novo: isso é linha nova, com decisão.", "R23", { partes: [7] });
    if (C.oseSobreFFE !== null && !entre(C.oseSobreFFE, 0.10, 0.15)) add("A9", "atencao", C.oseSobreFFE < 0.10 ? "Enxoval e utensílios abaixo da faixa" : "Enxoval e utensílios acima da faixa", "A Parte 5 é " + fmtPct(C.oseSobreFFE) + " da Parte 4; a faixa citada vai de 10% a 15%. " + (C.oseSobreFFE < 0.10 ? "Algum item de um dia de operação pode ter ficado de fora." : "Confira se o enxoval não está contado duas vezes.") + " " + NOTA_FAIXA, "R16, R28", { partes: [4, 5] });
    var temP5 = linhasDe(E, 5).some(ativa);
    if (temP5 && E.enxovalNaoDuplicado !== true) add("A10", "atencao", "O enxoval está contado uma vez só?", "Confirme que o enxoval não está também na cotação do mobiliário. Cada item mora numa linha só.", "R28", { partes: [5] });
    var prontas = tipologias(E).filter(function (l) { return l.forma === "pronta" && l.freteMontagemConfirmados !== true; });
    if (prontas.length) add("A15", "atencao", "Frete, fundação e montagem confirmados?", "Na estrutura pronta (" + juntar(prontas.map(function (l) { return txt(l.nome); })) + "), confirme por escrito se frete, fundação e montagem estão incluídos.", "R33");
    if (C.cotacoesVencidas > 0) add("A13", "atencao", C.cotacoesVencidas === 1 ? "1 cotação com mais de 90 dias" : C.cotacoesVencidas + " cotações com mais de 90 dias", (C.cotacoesVencidas === 1 ? "A cotação de " : "As cotações de ") + juntar(C.vencidas.map(function (x) { return x.curto + " (" + x.dias + " dias)"; })) + (C.cotacoesVencidas === 1 ? " passou" : " passaram") + " de 90 dias: refaça antes de usar.", "R8 (Volume 05 · Investimento, cap. 4)");
    if (C.nCotacoesIncompletas > 0) add("A14", "atencao", C.nCotacoesIncompletas === 1 ? "1 linha com cotação incompleta" : C.nCotacoesIncompletas + " linhas com cotação incompleta", (C.nCotacoesIncompletas === 1 ? "Uma linha tem" : C.nCotacoesIncompletas + " linhas têm") + " menos de três cotações ou escopos diferentes. Compare três propostas com a mesma especificação e peça o que cada uma não inclui.", "R5, R6");
    var p6Feita = ehNS(E.pagina6Total) || paraNumero(E.pagina6Total) !== null;
    if (p6Feita && C.limite6 === null) { add("A23", "ns", "Sem o limite da página 6", "Sem o limite da página 6, a 6A não diz se a conta cabe. Ele está na página 6, em \"o que precisa ser verdade\".", "P6 cap. 07"); }
    var gm = paraNumero(E.giroMeses);
    if (calculadoraGiroUsada(E) && gm < 3 - EPS) add("A16", "atencao", "Giro abaixo do piso de três meses", "Você calculou " + fmtN(gm, 2) + " meses de giro. Três meses são o piso citado; a conta completa do giro é a do Pilar 6. " + NOTA_FAIXA, "A05 caps. 7 e 10; VOL05 cap. 4; P6 cap. 06; PL2");
    if (E.terrenoSituacao === "comprar") add("A18", "info", "Custos de compra do terreno ficam fora", "Escritura, imposto de transmissão e registro não estão nesta conta: pergunte ao contador. A necessidade de capital fica no Pilar 7.", "Lacuna 3; R27");
    if (E.situacao === "opero") add("A19", "critico", "Não pague a obra com o caixa da operação", "A ampliação precisa de dinheiro separado. O caixa da operação paga a operação.", "F01 caps. 1 e 7");
    var regra = [E.regraParaQue, E.regraQuemAutoriza, E.regraComoRegistra, E.regraQuandoConfere];
    if (regra.some(function (r) { return txt(r).length < LIMITES.regraMin; })) add("A20", "bloqueia", "A regra de uso da reserva está incompleta", "Escreva as quatro linhas da regra (para quê, quem autoriza, como se registra e quando se confere), com pelo menos 10 letras cada.", "R24", { partes: [7] });
    A.sort(function (x, y) { return ORDEM_ALERTAS.indexOf(x.id) - ORDEM_ALERTAS.indexOf(y.id); });
    return A;
  }
  function tresPrimeiros(A) { return A.slice(0, 3); }

  /* ------------------------------------------------------------------
     7. O que fazer em 30 dias e como verificar (PLANO 6.5)
     ------------------------------------------------------------------ */
  function acaoSugerida(E, C, A) {
    C = C || calcular(E); A = A || alertas(E, C);
    var tem = function (ids) { return A.some(function (a) { return ids.indexOf(a.id) >= 0; }); };
    var dono = E.paraOutro === true;
    if (tem(["A21"])) return { ordem: 1, acao: (dono ? "Levar a página 6A ao dono, refazer" : "Refazer") + " a página 6 com estes números e listar, com o arquiteto ou o engenheiro, três ajustes possíveis (tamanho, produto ou fase) antes de assinar.", verificacao: "A página 6 refeita e a lista dos ajustes, com data." };
    var a1 = A.filter(function (a) { return a.id === "A1"; })[0];
    if (a1) return { ordem: 2, acao: "Listar as linhas da " + juntar(a1.partes.map(function (p) { return rotParte(p, E); })) + " e pedir as primeiras cotações.", verificacao: "As linhas na ficha e os pedidos enviados, com data e destinatário." };
    if (tem(["A6", "A7", "A8"])) {
      var up = inteiro(E.unidadesProjeto);
      return { ordem: 3, acao: "Pedir à concessionária o ponto de energia e ao projetista o dimensionamento da rede para " + (up ? "as " + up + " unidades" : "todas as unidades") + " do projeto completo.", verificacao: "A resposta da concessionária e a proposta do projetista, com o número de unidades escrito." };
    }
    if (C.brancos.length) {
      var n = C.brancos.length;
      return { ordem: 4, acao: "Pedir cotação escrita das linhas em branco: " + juntar(C.brancos.map(function (x) { return x.curto; })) + ".", verificacao: n === 1 ? "A proposta, com data e escopo, lançada na ficha." : "As " + extenso(n) + " propostas, com data e escopo, lançadas na ficha." };
    }
    if (C.degrau !== "Calculista") {
      var nomes = C.top3.map(function (x) { return x.curto; });
      return { ordem: 5, acao: "Pedir três cotações com a mesma especificação para as " + (nomes.length === 3 ? "três maiores linhas" : "maiores linhas") + (nomes.length ? ": " + juntar(nomes) : "") + ".", verificacao: "Três propostas por linha, com a mesma especificação anexada." };
    }
    if (tem(["A13", "A14"])) return { ordem: 6, acao: "Refazer as cotações vencidas e completar as que têm menos de três propostas comparáveis.", verificacao: "Datas novas e três propostas comparáveis por linha." };
    var rev = A.filter(function (a) { return ["A3", "A4", "A5", "A9", "A11", "A12"].indexOf(a.id) >= 0; })[0];
    if (rev) return { ordem: 7, acao: "Revisar linha a linha, com o checklist, a " + juntar((rev.partes || []).map(function (p) { return rotParte(p, E); })) + ".", verificacao: "A parte revisada e uma nota do que mudou." };
    return { ordem: 8, acao: (dono ? "Levar a página 6A ao dono. " : "") + "Refazer a página 6 com o quadro «Como levar para a página 6»; se preferir planilha, passar para a Planilha 1; colar o CAPEX na Planilha 2, aba Investimento, célula B5.", verificacao: "A página 6 refeita, com a data das cotações, e a Planilha 2 com o CAPEX na B5." };
  }
  /** As verificações da lista (você escolhe uma ou escreve a sua). */
  var VERIFICACOES = [
    "A página 6 refeita e a lista dos ajustes, com data.",
    "As linhas na ficha e os pedidos enviados, com data e destinatário.",
    "A resposta da concessionária e a proposta do projetista, com o número de unidades escrito.",
    "As propostas, com data e escopo, lançadas na ficha.",
    "Três propostas por linha, com a mesma especificação anexada.",
    "Datas novas e três propostas comparáveis por linha.",
    "A parte revisada e uma nota do que mudou.",
    "A página 6 refeita, com a data das cotações, e a Planilha 2 com o CAPEX na B5.",
  ];
  function proximaEtapa(E) {
    var dono = E && E.paraOutro === true;
    if (E && E.turma === "acompanhamento") return (dono ? "Leve a página 6A ao dono e ao encontro do Pilar 6" : "Leve a página 6A ao encontro do Pilar 6") + " e refaça a página 6 depois do comentário da equipe.";
    return dono ? "Salve o PDF na pasta Meu Dossiê e leve a página 6A ao dono. Depois, refaça a página 6 e siga para a Planilha 1 ou a Planilha 2." : "Salve o PDF na pasta Meu Dossiê, refaça a página 6 e siga para a Planilha 1 ou a Planilha 2.";
  }
  /** A ordem do Mapa de direcionamento (etapa 6), PLANO seção 9. */
  var PROXIMOS = [
    "Salve o PDF da página 6A na pasta Meu Dossiê, ao lado da página 6.",
    "Refaça a página 6 na ficha do Pilar 6 com o quadro «Como levar para a página 6», campo a campo, digitando 0 onde for zero.",
    "Planilha 1 · Orçamento de Abertura (se preferir planilha): lance pelo quadro «Se você usa a Planilha 1» e confira se o Resumo, linha TOTAL (B12), bate com o CAPEX da 6A.",
    "Planilha 2 · Estudo de Massas e Viabilidade, aba Investimento: cole o CAPEX da fase na célula B5, deixe o terreno em zero na B6 (fora da conta, como na 6A) e confira se o giro da B9 bate com o da 6A.",
    "Sensibilidade do Mapa (diária −15%, ocupação −10 pontos, CAPEX +20%) e volte à ficha do Pilar 6 para refazer a página 6.",
    "Pilar 7: a necessidade de capital, o custo da captação e o pedido. No plano de 90 dias: «Dias 61 a 90 · Decidir: refaz a página 6 com os números cotados».",
  ];

  /* ------------------------------------------------------------------
     8. Leituras (significado) e faixas (PLANO 6.3)
     ------------------------------------------------------------------ */
  function leituraLinhasCotadas(pct) {
    if (pct === null || pct === undefined) return "Ainda não há linhas com origem.";
    if (pct <= EPS) return "Nenhuma linha tem cotação: por enquanto, a ficha é um mapa do que cotar.";
    if (pct <= 0.5 + EPS) return "A maior parte das linhas ainda é estimativa ou está em branco.";
    return "A maioria das linhas tem cotação escrita.";
  }
  function leituraReserva(E) {
    var p = paraNumero(E.reservaPct);
    if (p === null || p <= 0) return "Sem reserva: ela nunca é zero.";
    var lo = E.imovelPronto === true ? 15 : 10, hi = E.imovelPronto === true ? 25 : 15;
    if (p < lo - EPS) return "Abaixo da faixa citada (" + lo + "% a " + hi + "%).";
    if (p > 25 + EPS) return "Acima de 25%: confira se não está cobrindo linha esquecida.";
    if (p > hi + EPS) return "Acima da faixa citada (" + lo + "% a " + hi + "%), o que a fonte aceita com fator de risco.";
    return "Dentro da faixa citada (" + lo + "% a " + hi + "%).";
  }
  function leituraPagina6(C, E) {
    if (E && ehNaoFiz(E.pagina6Total)) return "Você ainda não fez a página 6: sem ela não há o que comparar.";
    if (C.pagina6Total === null || C.pagina6Cobre === null) return C.pagina6Total !== null ? "Falta o giro para comparar com a página 6." : "Sem o número da página 6 para comparar.";
    return "A sua página 6 cobria " + fmtPct(C.pagina6Cobre) + " da 6A; a diferença é de " + brl(C.difPagina6) + ".";
  }
  function leituraLimite(C) {
    if (C.limite6 === null) return "Sem o limite da página 6, a 6A não diz se a conta cabe.";
    if (C.folga6 === null) return "Falta o giro para conferir o limite da página 6.";
    if (C.dentroLimite) return "Cabe no limite da página 6 (" + brl(C.limite6) + "), com folga de " + brl(C.folga6) + " (cerca de " + fmtPct(C.folgaPctCapex) + " do CAPEX). Já com a reserva, a folga paga " + brl(C.folgaEmSubtotal) + " de linhas novas: as linhas em branco ainda precisam caber nela.";
    return "Passou do limite da página 6 (" + brl(C.limite6) + ") em " + brl(-C.folga6) + ": volte à conta antes de assinar.";
  }
  function leituraDegrau(C) {
    var r = REGUA.filter(function (x) { return x.v === C.degrau; })[0];
    var t = "Degrau " + C.degrau + ": " + r.t;
    if (C.degrauDiagnostico && C.degrauDiagnostico !== C.degrau) t += " No diagnóstico, você estava em " + C.degrauDiagnostico + ".";
    else if (C.degrauDiagnostico) t += " É o mesmo degrau do diagnóstico.";
    if (C.degrau !== "Calculista" && C.nLinhas > 0) t += " Faltam " + C.faltamParaMaioria + " " + (C.faltamParaMaioria === 1 ? "linha cotada" : "linhas cotadas") + " para a maioria.";
    return t;
  }

  /* ------------------------------------------------------------------
     9. Validação de cada tela (bloqueia o Avançar) e critério de conclusão
     ------------------------------------------------------------------ */
  var TELAS = ["abertura", "pagina6", "fase", "p1", "p2", "p3", "p4", "p5", "p6", "reserva", "giro", "resultado", "acao"];
  function dinheiroCampoOk(v) { var n = paraNumero(v); return n !== null && n >= 0 && n <= LIMITES.dinheiroMax; }
  function validarTela(tela, E, hoje) {
    E = E || {}; hoje = hoje || E.hoje;
    var n;
    if (tela === "abertura") {
      var pj = txt(E.projeto), nm = txt(E.nome), cid = txt(E.cidadeUF);
      if (nm && (nm.length < 2 || nm.length > 60)) return "O nome vai de 2 a 60 letras (ou deixe em branco).";
      if (pj.length < 2 || pj.length > 60) return "Dê um nome ao projeto (2 a 60 letras).";
      if (cid && (cid.length < 2 || cid.length > 60)) return "A cidade vai de 2 a 60 letras (ou deixe em branco).";
      if (!E.situacao) return "Escolha a frase que descreve a sua situação.";
      if (!E.tipo) return "Escolha o tipo de hospedagem.";
      for (var i = 0; i < DIAG.length; i++) if (!E[DIAG[i].id]) return "Responda às quatro perguntas sobre a sua página 6.";
      return "";
    }
    if (tela === "pagina6") {
      if (!ehNS(E.pagina6Total) && !ehNaoFiz(E.pagina6Total)) {
        n = paraNumero(E.pagina6Total);
        if (n === null) return "Escreva o investimento total da fase um da sua página 6, ou toque em Não fiz a página 6 ou em Não sei.";
        if (n < 0 || n > LIMITES.dinheiroMax) return "O investimento da página 6 vai de R$ 0 a R$ 100 milhões.";
      }
      if (!falta(E.pagina6Data)) { if (!dataOk(E.pagina6Data)) return "A data da página 6 não está no formato certo."; if (hoje && diasEntre(E.pagina6Data, hoje) < 0) return "A data da página 6 não pode ser no futuro."; }
      if (!falta(E.pagina6Infra) && !dinheiroCampoOk(E.pagina6Infra)) return "A infraestrutura comum da página 6 vai de R$ 0 a R$ 100 milhões (ou deixe em branco se ficou à parte, a cotar).";
      if (!falta(E.limite6) && !ehNS(E.limite6) && !dinheiroCampoOk(E.limite6)) return "O limite da página 6 vai de R$ 0 a R$ 100 milhões, ou toque em Não sei.";
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
    var m = /^p([1-6])$/.exec(tela);
    if (m) {
      var p = Number(m[1]), L = linhasDe(E, p);
      if (L.length < 1) return "A parte precisa de pelo menos uma linha (se não se aplica, marque Não se aplica).";
      if (L.length > LIMITES.linhasMax) return "Cada parte vai até 15 linhas.";
      for (var k = 0; k < L.length; k++) { var er = erroLinha(L[k], E, hoje); if (er) return er; }
      if (p === 6 && L.every(function (l) { return l.origem === "naoAplica"; })) return "A pré-abertura nunca é inteira \"não se aplica\": toda hospedagem abre com licença, fotos e treinamento.";
      if ((p === 2 || p === 3) && E.imovelPronto !== true && L.every(function (l) { return l.origem === "naoAplica"; })) return "Esta parte só pode ficar inteira em \"não se aplica\" quando o imóvel já existe.";
      if (p === 2 && parte2Ativa(E)) {
        if (!ehNS(E.distanciaEnergiaM)) { n = paraNumero(E.distanciaEnergiaM); if (n === null || n < 0 || n > LIMITES.distMax) return "Escreva a distância até o ponto de energia (0 a 50.000 m) ou toque em Não sei."; }
        if (!ehNS(E.infraDimensionadaPara)) { n = inteiro(E.infraDimensionadaPara); if (n === null || n < 1 || n > LIMITES.redeMax) return "Diga para quantas unidades a rede é dimensionada (1 a 999) ou toque em Não sei."; }
        if (!falta(E.infraProjetoCompleto)) { n = paraNumero(E.infraProjetoCompleto); if (n === null || n < 0 || n > LIMITES.dinheiroMax) return "O valor da rede inteira vai de R$ 0 a R$ 100 milhões (ou deixe em branco)."; }
      }
      if (p === 3) {
        var tip = linhasDe(E, 3).filter(function (l) { return l.tipologia; });
        if (tip.length > LIMITES.tipologiasMax) return "São até 3 tipologias.";
        if (E.imovelPronto !== true && tipologias(E).length < 1) return "Inclua pelo menos uma tipologia de unidade.";
        if (!tipologiasConferem(E)) return "As tipologias somam " + somaTipologias(E) + " unidades, e a fase tem " + inteiro(E.unidadesFase) + ". Ajuste as quantidades.";
      }
      return "";
    }
    if (tela === "reserva") {
      var rg = [E.regraParaQue, E.regraQuemAutoriza, E.regraComoRegistra, E.regraQuandoConfere];
      if (rg.some(function (r) { return txt(r).length > LIMITES.regraMax; })) return "Cada linha da regra vai até 200 letras.";
      if (ehNS(E.reservaPct)) return "";
      n = paraNumero(E.reservaPct);
      if (n === null || n <= 0 || n > LIMITES.reservaMax) return "A reserva vai de mais de 0% até 50%, ou toque em Não sei.";
      return "";
    }
    if (tela === "giro") {
      var gm = paraNumero(E.giroMeses), gc = paraNumero(E.giroCustoMensal);
      if (!falta(E.giroMeses) && (gm === null || gm < 0 || gm > LIMITES.giroMesesMax)) return "Os meses de giro vão de 0 a 24.";
      if (!falta(E.giroCustoMensal) && (gc === null || gc < 0 || gc > LIMITES.dinheiroMax)) return "O custo de um mês vai de R$ 0 a R$ 100 milhões.";
      if (!ehNS(E.giro) || calculadoraGiroUsada(E)) {
        var g = giroUsado(E);
        if (g === null) return "Escreva o capital de giro em reais, use a calculadora ou toque em Não sei.";
        if (g < 0 || g > LIMITES.dinheiroMax) return "O giro vai de R$ 0 a R$ 100 milhões.";
        if (g === 0) {
          if (E.situacao !== "opero" && E.paraOutro !== true) return "Quem ainda não hospeda precisa de capital de giro maior que zero. Se ainda não sabe, toque em Não sei.";
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
  function pagina6Respondida(E) { return ehNS(E.pagina6Total) || ehNaoFiz(E.pagina6Total) || (paraNumero(E.pagina6Total) !== null && paraNumero(E.pagina6Total) >= 0 && paraNumero(E.pagina6Total) <= LIMITES.dinheiroMax); }

  /** Critério de conclusão (selo "Pronto para levar à página 6"), PLANO 6.6. */
  function criterio(E, C, hoje) {
    E = E || {}; hoje = hoje || E.hoje; C = C || calcular(E, hoje);
    var u = inteiro(E.unidadesFase), up = inteiro(E.unidadesProjeto);
    var linhasOk = true, partesOk = true;
    for (var p = 1; p <= 6; p++) {
      var L = linhasDe(E, p);
      if (L.some(function (l) { return !l.origem || erroLinha(l, E, hoje) !== ""; })) linhasOk = false;
      var temAtiva = L.some(ativa);
      var podeNA = E.imovelPronto === true && (p === 2 || p === 3) && parteInteiraNA(E, p);
      if (!temAtiva && !podeNA) partesOk = false;
    }
    var rg = [E.regraParaQue, E.regraQuemAutoriza, E.regraComoRegistra, E.regraQuandoConfere].every(function (r) { return txt(r).length >= LIMITES.regraMin && txt(r).length <= LIMITES.regraMax; });
    var pctR = paraNumero(E.reservaPct);
    var infraOk = !parte2Ativa(E) || (function () { var d = inteiro(E.infraDimensionadaPara); return d !== null && d >= 1 && d <= LIMITES.redeMax; })();
    var g = giroUsado(E);
    var giroOk = g !== null && (g > 0 || (g === 0 && (E.situacao === "opero" || E.paraOutro === true) && txt(E.giroZeroJustificativa).length >= 10));
    var itens = [
      { n: 1, ok: pagina6Respondida(E), txt: "A tela da página 6 respondida: o número, Não fiz a página 6 ou Não sei." },
      { n: 2, ok: u !== null && u >= 1 && up !== null && up >= u && tipologiasConferem(E), txt: "As unidades da fase e do projeto completo informadas, e as tipologias somando a fase." },
      { n: 3, ok: linhasOk && partesOk, txt: "As Partes 1 a 6 com a origem de cada linha escolhida e pelo menos uma linha que se aplica em cada parte." },
      { n: 4, ok: C.capexFase > 0, txt: "O custo de abrir a porta maior que zero." },
      { n: 5, ok: pctR !== null && pctR > 0 && pctR <= LIMITES.reservaMax && rg, txt: "A reserva maior que zero e as quatro linhas da regra de uso escritas." },
      { n: 6, ok: infraOk, txt: "Para quantas unidades a rede é dimensionada." },
      { n: 7, ok: giroOk, txt: "O capital de giro maior que zero (ou zero com a justificativa, só para quem já opera ou faz para outra pessoa)." },
      { n: 8, ok: !!E.terrenoSituacao, txt: "A situação do terreno respondida." },
      { n: 9, ok: txt(E.acao30).length >= 10 && txt(E.acao30).length <= 300 && prazoOk(E.prazo, hoje) && txt(E.verificacao).length >= 10, txt: "A ação de 30 dias escrita, com prazo de até 30 dias e como verificar." },
      { n: 10, ok: E.pdfBaixado === true, txt: "A página 6A baixada em PDF." },
    ];
    return { ok: itens.every(function (x) { return x.ok; }), antesDoPdf: itens.slice(0, 9).every(function (x) { return x.ok; }), itens: itens, faltas: itens.filter(function (x) { return !x.ok; }).map(function (x) { return x.txt; }) };
  }

  /** O que fica salvo em resumo.dados (no formato das outras páginas do Dossiê). */
  function resumoDados(E, C) {
    var T = C.transposicao || {}, P = C.planilha1 || {};
    var r = function (x) { return typeof x === "number" && Number.isFinite(x) ? arred(x, 2) : null; };
    return {
      unidades: inteiro(E.unidadesFase), unidades_projeto: inteiro(E.unidadesProjeto),
      parte1: r(C.totalParte[1]), parte2: r(C.totalParte[2]), parte3: r(C.totalParte[3]), parte4: r(C.totalParte[4]), parte5: r(C.totalParte[5]), parte6: r(C.totalParte[6]),
      subtotal: r(C.subtotal), reserva_pct: C.reservaPct, reserva: r(C.reserva), capex_fase: r(C.capexFase),
      giro: r(C.giro), investimento_total: r(C.investimentoTotal), custo_por_unidade: r(C.custoPorUnidade), investimento_por_unidade: r(C.investimentoPorUnidade),
      area_total: r(C.areaTotal), custo_por_m2: r(C.custoPorM2), terreno: r(C.terreno), terreno_situacao: E.terrenoSituacao || null,
      pagina6_total: r(C.pagina6Total), pagina6_cobre_pct: r(C.pagina6Cobre === null ? null : C.pagina6Cobre * 100), limite6: r(C.limite6), folga6: r(C.folga6), dentro_limite: C.dentroLimite,
      pct_linhas_cotadas: r(C.pctLinhasCotadas === null ? null : C.pctLinhasCotadas * 100), pct_valor_cotado: r(C.pctValorCotado === null ? null : C.pctValorCotado * 100),
      degrau: C.degrau, unidade_pronta: r(T.pronta), licencas: r(T.licencas), infra_comum: r(T.infra),
      pl1_premissas: r(P.premissas), pl1_infraestrutura: r(P.infraestrutura), pl1_ffe: r(P.ffe), pl1_ose: r(P.ose), exemplo: E.exemplo === true,
    };
  }

  /* ------------------------------------------------------------------
     10. O exemplo: a Marina abre a página 6 dela (PLANO seção 7)
     Exemplo ilustrativo · dados fictícios. As datas andam junto com "hoje",
     para o exemplo mostrar sempre os mesmos números (o "hoje" do plano é 27/11/2026).
     ------------------------------------------------------------------ */
  var ROTULO_EXEMPLO = "Exemplo ilustrativo · dados fictícios. Não são preços de referência.";
  var ROTULO_REFERENCIA = "Referência orientativa da página 6, não confirmada; a Zion também vende esse tipo de estrutura.";
  var HOJE_EXEMPLO = "2026-11-27";
  function exemplo(hoje) {
    hoje = dataOk(hoje) ? hoje : HOJE_EXEMPLO;
    var desloc = diasEntre(HOJE_EXEMPLO, hoje);
    var dt = function (iso) { return somaDias(iso, desloc); };
    var mk = function (o, campos) { var l = novaLinha(o); for (var k in campos) l[k] = campos[k]; return l; };
    var C3 = function (data) { return { origem: "cotacao", nCotacoes: 3, mesmaEspec: true, dataCotacao: dt(data) }; };
    var C2 = function (data) { return { origem: "cotacao", nCotacoes: 2, mesmaEspec: true, dataCotacao: dt(data) }; };
    var C1 = function (data) { return { origem: "cotacao", nCotacoes: 1, mesmaEspec: false, dataCotacao: dt(data) }; };
    var ES = { origem: "estimativa" }, BR = { origem: "branco" }, NA = { origem: "naoAplica" };
    var junta = function (a, b) { var r = {}; for (var k in a) r[k] = a[k]; for (k in b) r[k] = b[k]; return r; };
    var val = function (nome, valor, o, extra) { return mk(junta({ nome: nome, modo: "valor" }, extra || {}), junta(o, { valor: valor })); };
    var pu = function (nome, q, vu, o, tag) { return mk({ nome: nome, modo: "qtdUnit", porUnidade: true, tagP6: tag }, junta(o, { qtd: q, valorUnit: vu })); };
    var ar = function (nome, q, a, m2, o, extra) { return mk(junta({ nome: nome, modo: "area" }, extra || {}), junta(o, { qtd: q, areaM2: a, custoM2: m2 })); };
    var cabanas = novaLinha({ nome: "Cabanas de madeira (tipologia única; piso incluído no m²)", tipologia: true, forma: "construida" });
    Object.assign(cabanas, { qtd: 3, areaM2: 38, custoM2: 2800 }, C3("2026-10-28"));
    var enx = novaLinha({ nome: "Enxoval (lavanderia terceirizada, três jogos mesmo assim)", enxoval: true, tagP6: "mobilia" });
    Object.assign(enx, { camasPorUnidade: 1, custoJogo: 780 }, C3("2026-11-06"));
    var E = estadoInicial(hoje);
    Object.assign(E, {
      nome: "Marina (exemplo)", projeto: "Cabanas da Marina", cidadeUF: "", situacao: "terreno", paraOutro: false, tipo: "cabanas", imovelPronto: false,
      d1: "referencia", d2: "nenhuma", d3: "nenhuma", d4: "nao",
      pagina6Total: "690.529,18", pagina6Data: dt("2026-11-13"), pagina6Infra: "", limite6: "870.130,80", pagina6ResultadoCons: "108.766,35", pagina6GiroMeses: "3",
      unidadesFase: 3, unidadesProjeto: 5, fatoresRisco: [], primeiraObra: true,
      distanciaEnergiaM: 260, infraDimensionadaPara: 5, infraProjetoCompleto: "", enxovalNaoDuplicado: true,
      reservaPct: 15,
      regraParaQue: "Imprevisto da obra orçada (solo, chuva, reajuste, exigência da licença).",
      regraQuemAutoriza: "A Marina, depois de ouvir o engenheiro.",
      regraComoRegistra: "Planilha com data, motivo e valor.",
      regraQuandoConfere: "A cada medição da obra.",
      giro: "40.787,38", giroMeses: "", giroCustoMensal: "", terrenoSituacao: "meu", terrenoValor: "600.000",
      prazo: somaDias(hoje, 30), exemplo: true,
    });
    E.partes = {
      1: [val("Levantamento topográfico e sondagem do solo", 6200, C3("2026-10-02")), val("Projeto de arquitetura (3 cabanas, apoio e implantação da fase um)", 16500, C3("2026-10-09")),
        val("Projetos complementares (estrutural, elétrico, hidrossanitário)", 9800, C2("2026-10-14")), val("Aprovação na prefeitura e taxas", 2500, ES), val("Responsabilidade técnica e registros", 1000, ES),
        val("Licença ambiental, se houver (aguarda a resposta da prefeitura)", "", BR, { curto: "licença ambiental" })],
      2: [val("Acesso interno até a clareira (cascalho e drenagem lateral)", 24000, C3("2026-10-20")), val("Estacionamento na clareira (5 vagas de hóspede e 1 de serviço)", 7200, C2("2026-10-20")),
        mk({ nome: "Caminho do hóspede pela mata, com luz baixa (metros)", modo: "qtdUnit" }, junta(C2("2026-10-22"), { qtd: 120, valorUnit: 140 })),
        val("Energia: padrão de entrada e rede enterrada até as 5 posições, com duto vazio", 31500, C1("2026-11-05")),
        val("Água: poço com teste de vazão, reservatório e rede para 5", 19800, C2("2026-07-15"), { curto: "água" }),
        val("Esgoto: tratamento dimensionado para 5", 14500, ES), val("Drenagem das plataformas e do caminho", 4200, ES),
        val("Internet para o hóspede que trabalha de domingo a quinta", "", BR, { curto: "internet" }),
        pu("Ligação de luz de cada cabana", 3, 1800, ES, "luz"), pu("Água e esgoto de cada cabana", 3, 1600, ES, "agua")],
      3: [cabanas, mk({ nome: "Deck de cada cabana", modo: "area", porUnidade: true, tagP6: "deck" }, junta(C2("2026-10-28"), { qtd: 3, areaM2: 16, custoM2: 700 })),
        ar("Apoio de 30 m² (rouparia 12, depósito 6, lixo 4, copa e vestiário 8)", 1, 30, 2200, C1("2026-10-30"), { comum: true }),
        ar("Deck leve da crista", 1, 16, 600, ES, { comum: true })],
      4: [pu("Cama e colchão de hotel", 3, 5200, C3("2026-11-03"), "mobilia"), pu("Mobiliário (sofá, mesa de trabalho e cadeira, armário, cabeceiras)", 3, 7400, C2("2026-11-03"), "mobilia"),
        pu("Iluminação", 3, 1900, ES, "mobilia"), pu("Cozinha compacta e eletrodomésticos", 3, 4300, C3("2026-11-06"), "mobilia"),
        pu("Banheiro (metais, espelho, acessórios)", 3, 2600, ES, "mobilia"), pu("Mobiliário do deck (o café na varanda)", 3, 1800, ES, "mobilia"),
        val("Equipamentos do apoio (carrinho de camareira, prateleiras da rouparia)", 2400, ES, { geral: true })],
      5: [enx, pu("Utensílios de cozinha", 3, 400, ES, "mobilia"), val("Governança e limpeza", 900, ES, { tagP6: "mobilia" }),
        val("Recepção (nenhuma recepção construída, decisão do Pilar 5)", "", NA), val("Manutenção (ferramentas básicas)", 600, ES, { tagP6: "mobilia" }),
        val("Segurança (extintores, primeiros socorros, lanternas)", "", BR, { tagP6: "mobilia", curto: "segurança" }), val("Amenidades e suprimentos do primeiro mês", 1020, ES, { tagP6: "mobilia" })],
      6: [val("Licença de funcionamento e cadastros", "", BR, { curto: "licença de funcionamento" }), val("Fotos profissionais e anúncio", 4800, C2("2026-11-10")),
        val("Identidade e lançamento", 3500, ES), val("Treinamento da pessoa local e manual de operação", 2500, ES),
        val("Seguro do primeiro ano", "", BR, { curto: "seguro do primeiro ano" }), val("Abertura de teste (noites com convidados, consumo e ajustes)", 1800, ES)],
    };
    var C = calcular(E, hoje);
    var s = acaoSugerida(E, C, alertas(E, C));
    E.acao30 = s.acao; E.verificacao = s.verificacao;
    return E;
  }

  /* ------------------------------------------------------------------
     11. Textos fixos e varredura de promessas proibidas
     ------------------------------------------------------------------ */
  var TEXTOS = {
    titulo: "O seu CAPEX",
    tituloCompleto: "Faça agora · O seu CAPEX",
    pagina: "Página 6A · CAPEX",
    promessa: "Aprenda o passo a passo para abrir, linha por linha, quanto custa abrir a porta do seu projeto, com a origem de cada número, e conferir se a conta ainda cabe no limite da sua página 6 antes de assinar qualquer obra.",
    retomada: "Você já fez a página 6 no Pilar 6. Aqui ela ganha uma página irmã, a 6A, que abre as linhas da página 6 uma por uma.",
    capex: "O nome técnico é CAPEX, do inglês capital expenditure: é o custo de abrir a porta, tudo o que se gasta para a fase um começar a receber hóspedes.",
    assinatura: "«Não é quanto custa a cabana. É quanto custa abrir a porta.» (Pilar 6)",
    linhaBranco: "«Uma linha em branco vale mais do que um número inventado.» (Pilar 6)",
    naoSei: "«Onde não souber, marque \"Não sei\": vira a sua tarefa da semana.» (Comece aqui)",
    aviso: "Material educativo. Não é orçamento, projeto nem estudo de viabilidade definitivo. Custos, licenças e impostos se confirmam com engenheiro, arquiteto, prefeitura e contador. A Zion avalia cada caso.",
    naoEnvia: "Esta ficha não envia nada: o PDF fica só com você.",
    dossie: "Salve o PDF da página 6A na pasta Meu Dossiê, ao lado da página 6.",
    tempo: "Em uma tarde sai a primeira versão, com estimativas e linhas em branco nomeadas. Trocar as linhas por cotação leva o tempo dos fornecedores.",
    naoPromete: "A lição não promete aprovação, crédito, parceria, retorno, ocupação nem prazo de obra.",
    exemplo: ROTULO_EXEMPLO,
    referencia: ROTULO_REFERENCIA,
    transposicao: "Digite 0 onde for zero. Em branco, a ficha do Pilar 6 usa a referência da Zion no lugar.",
    transposicaoInfra: "A ficha do Pilar 6 não tem linha própria para áreas comuns, equipamentos gerais, pré-abertura e a parte da reserva que não é unidade. Por isso tudo isso vai no campo «infraestrutura comum», com uma nota escrita.",
    pl1Aviso: PL1_AVISO,
    sensibilidade: "A 6A não calcula o teste «CAPEX +20%» do Mapa: ele é a próxima etapa, a reserva já está dentro do CAPEX e a decisão é do Pilar 7.",
  };
  /* Textos de cada tela: pergunta, explicação, "por que", "onde conseguir" e a caixa da Marina (exemplo ilustrativo). */
  var AJUDA = {
    pagina6: { titulo: "A sua página 6: o número de onde a 6A parte", explica: "Escreva o investimento total da fase um da sua página 6 e a data. No fim, a ficha compara a página 6 com a 6A e confere se a conta ainda cabe no limite que a própria página 6 escreveu.", porque: "No Pilar 6 você fez a conta pela folha de oito linhas, com referência onde ainda não havia cotação e com a infraestrutura comum à parte, a cotar. Aqui cada linha vira cotação, estimativa ou linha em branco, e o que estava à parte entra. A comparação mostra quanto a página 6 cobria, sem julgamento.", onde: "Na página 6 do seu Dossiê, o PDF da pasta Meu Dossiê: o investimento total da fase um, a data e, em «o que precisa ser verdade», o investimento até onde a conta aguenta dentro de 8 anos no conservador. Se você fez a ficha do Pilar 6 neste aparelho, os números já vêm preenchidos.", exemplo: "A página 6 da Marina diz R$ 690.529,18 (cerca de R$ 690 mil), com a infraestrutura comum à parte, a cotar. O limite dela é de R$ 870.130,80: 8 × R$ 108.766,35. A unidade pronta daquela página é referência orientativa, não confirmada; a Zion também vende esse tipo de estrutura." },
    fase: { titulo: "Quantas unidades a fase um abre, e quantas o projeto completo terá?", explica: "Toda a conta é da fase um: o que se constrói agora. O projeto completo serve para dimensionar a rede uma vez só.", porque: "«O que não se constrói não se orça.» (Pilar 6). Mas a rede de energia, água e caminhos precisa caber no projeto completo.", onde: "No masterplan do Pilar 5 (fase um e projeto completo) e na página 6 do seu Dossiê.", exemplo: "A Marina abre com 3 cabanas e desenha para 5, como no masterplan do Pilar 5. É a primeira obra dela; nenhum outro fator de risco marcado." },
    p1: { explica: "Só entra o que aprova o projeto e a obra. A licença para operar vai para a Parte 6, a pré-abertura.", porque: "É uma das linhas pequenas que mais somem dos orçamentos, e a primeira a trocar por proposta escrita.", onde: "Nas propostas escritas do arquiteto, do engenheiro e de quem faz o levantamento do terreno, e na lista de taxas da prefeitura.", exemplo: "Levantamento e sondagem R$ 6.200 e arquitetura R$ 16.500 (3 cotações cada), projetos complementares R$ 9.800 (2), prefeitura R$ 2.500 e responsabilidade técnica R$ 1.000 (estimativas), licença ambiental em branco. Total: R$ 36.000." },
    p2: { explica: "O que leva acesso, energia, água, esgoto e internet até as unidades. Ela se orça por distância e capacidade. Na página 6 ela ficou à parte, a cotar: aqui ela entra.", porque: "É a parte que mais varia entre terrenos. Dimensione a rede para o projeto completo e construa uma vez: refazer vala e caminho na fase dois é a forma mais cara de economizar.", onde: "A concessionária informa o ponto e a tensão de energia. O projetista habilitado define água e esgoto. A construtora orça acesso e caminhos.", exemplo: "Energia a 260 m e rede para 5, com duto vazio. Acesso, estacionamento, caminho de 120 m, energia, água, esgoto, drenagem e as ligações de cada cabana; internet em branco. Total: R$ 128.200. A cotação da água, de julho, passou de 90 dias." },
    p3: { explica: "Cada tipologia com a quantidade, a área e o custo do m², ou com o preço por unidade se for estrutura pronta. Depois, os extras de cada unidade e as áreas comuns.", porque: "O metro quadrado inteiro custa, inclusive o das áreas comuns que o Pilar 5 desenhou (o apoio). A estrutura pronta conta como unidade, como no Pilar 6, e frete, fundação e montagem precisam estar confirmados por escrito.", onde: "Na cotação da construtora ou do fabricante, com a especificação e a lista do que não está incluído.", exemplo: "3 cabanas × 38 m² × R$ 2.800 = R$ 319.200 (piso no m²); decks 3 × 16 m² × R$ 700 = R$ 33.600; apoio de 30 m² × R$ 2.200 = R$ 66.000; deck leve da crista 16 m² × R$ 600 = R$ 9.600. Total: R$ 428.400, em 208 m²." },
    p4: { explica: "Monte a lista de uma unidade-modelo e multiplique pelas unidades. Os equipamentos gerais (apoio, lavanderia, áreas comuns) entram à parte.", porque: "Na unidade-modelo você erra barato, antes de comprar para todas.", onde: "Na especificação escrita de cada item e nas cotações das lojas.", exemplo: "Unidade-modelo de R$ 23.200 × 3 = R$ 69.600, mais R$ 2.400 de equipamentos do apoio. Total: R$ 72.000." },
    p5: { explica: "O enxoval segue a regra dos três jogos por cama: um na cama, um na lavanderia e um no estoque. Depois vêm as listas de um dia de operação.", porque: "Cada item mora numa linha só: se a cotação do mobiliário já trouxer o enxoval, não some de novo.", onde: "Nas cotações de enxoval e nas listas de governança, recepção, manutenção e segurança.", exemplo: "Enxoval 3 cabanas × 1 cama × 3 jogos × R$ 780 = R$ 7.020 (lavanderia terceirizada, três jogos mesmo assim); utensílios, limpeza, manutenção e amenidades estimados; segurança em branco; recepção não se aplica. Total: R$ 10.740." },
    p6: { explica: "O que acontece entre a obra pronta e o primeiro hóspede: licença de funcionamento, fotos, lançamento, treinamento, seguro e abertura de teste. Ela não estava na página 6.", porque: "Esquecer a pré-abertura é um dos cinco erros do orçamento amador que você viu no Pilar 6.", onde: "Na prefeitura (licença), no fotógrafo, na corretora de seguros e no seu plano de lançamento.", exemplo: "Fotos R$ 4.800 (2 cotações); identidade, treinamento e abertura de teste estimados; licença de funcionamento e seguro em branco. Total: R$ 12.600." },
    reserva: { titulo: "Parte 7 · Reserva do imprevisto", explica: "Uma porcentagem sobre o subtotal das Partes 1 a 6, com a regra de uso escrita em quatro linhas. Atenção: a base mudou. No Pilar 6 eram 10% das unidades prontas; aqui é o subtotal das Partes 1 a 6.", porque: "Você não sabe qual imprevisto virá; sabe que algum virá. A reserva cobre a obra orçada (solo, chuva, reajuste, exigência da licença), e não escopo novo nem o caixa dos primeiros meses. A reserva que sobra vira giro.", onde: "Conte os seus fatores de risco. A faixa citada pelas fontes vai de 10% a 15% do subtotal, no teto ou acima com fator de risco ou primeira obra, e de 15% a 25% no imóvel pronto. É faixa de conferência, não regra fixa.", exemplo: "A Marina começa com os 10% da página 6 (R$ 68.794), vê o alerta da primeira obra e sobe para 15%: R$ 103.191. O ofurô na crista, se aparecer no meio da obra, é linha nova e decisão, não reserva." },
    giro: { titulo: "Capital de giro e terreno", explica: "O giro paga a operação enquanto a receita não cobre o custo: ele se soma ao custo de abrir a porta no investimento total. O terreno fica ao lado e não se soma: fora da conta não quer dizer de graça.", porque: "Projeto não quebra por prejuízo no ano; quebra por falta de caixa num mês. Três meses de custo são o piso citado; a conta completa do giro é a do Pilar 6.", onde: "Na página 6 do seu Dossiê (Pilar 6). O valor do terreno, na página 1 ou num laudo de avaliação.", exemplo: "Giro de R$ 40.787,38, que veio da página 6 (três meses de custo). O terreno já é dela, R$ 600.000, e fica fora da soma." },
  };
  var PROIBIDAS = [/garant/i, /lucro certo/i, /sucesso/i, /vai faturar/i, /renda (certa|passiva)/i, /sem risco/i, /enriquec/i, /fique rico/i, /payback/i, /\bmembro\b/i, /\baluno\b/i, /ECROI/, /\bBloco [1-7]\b/];
  function textoSeguro(s) { return !PROIBIDAS.some(function (re) { return re.test(String(s)); }); }

  var api = {
    NS: NS, NAO_FIZ: NAO_FIZ, LIMITES: LIMITES, SITUACOES: SITUACOES, TIPOS: TIPOS, DIAG: DIAG, FATORES: FATORES, ORIGENS: ORIGENS, MODOS: MODOS, FORMAS: FORMAS, TAGS: TAGS, TERRENO: TERRENO, PARTES: PARTES, REGUA: REGUA,
    ORDEM_ALERTAS: ORDEM_ALERTAS, INFO: INFO, AJUDA: AJUDA, VERIFICACOES: VERIFICACOES, PROXIMOS: PROXIMOS, TELAS: TELAS, TEXTOS: TEXTOS, PROIBIDAS: PROIBIDAS, NOTA_FAIXA: NOTA_FAIXA, PL1_MAPA: PL1_MAPA, HOJE_EXEMPLO: HOJE_EXEMPLO,
    falta: falta, paraNumero: paraNumero, arred: arred, fmtNum: fmtNum, fmtN: fmtN, brl: brl, brl0: brl0, fmtPct: fmtPct, juntar: juntar, div: div, ehNS: ehNS, ehNaoFiz: ehNaoFiz, extenso: extenso,
    numTexto: numTexto, dataOk: dataOk, diasEntre: diasEntre, somaDias: somaDias, dataBR: dataBR,
    nomeParte: nomeParte, novaLinha: novaLinha, linhasSugeridas: linhasSugeridas, estadoInicial: estadoInicial, migrar: migrar,
    lerPagina6: lerPagina6, lerMarcoZero: lerMarcoZero, aplicarPagina6: aplicarPagina6, limiteEfetivo: limiteEfetivo,
    valorLinha: valorLinha, erroLinha: erroLinha, cotacaoCompleta: cotacaoCompleta, cotacaoVencida: cotacaoVencida, tipologias: tipologias, somaTipologias: somaTipologias, tipologiasConferem: tipologiasConferem,
    giroUsado: giroUsado, calculadoraGiroUsada: calculadoraGiroUsada, calcular: calcular, degrauDiagnostico: degrauDiagnostico, notaP6: notaP6, transposicao: transposicao, planilha1: planilha1,
    alertas: alertas, tresPrimeiros: tresPrimeiros, acaoSugerida: acaoSugerida, proximaEtapa: proximaEtapa,
    leituraLinhasCotadas: leituraLinhasCotadas, leituraReserva: leituraReserva, leituraPagina6: leituraPagina6, leituraLimite: leituraLimite, leituraDegrau: leituraDegrau,
    validarTela: validarTela, prazoOk: prazoOk, criterio: criterio, resumoDados: resumoDados, exemplo: exemplo, textoSeguro: textoSeguro,
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else raiz.ZCAPEX = api;
})(typeof window !== "undefined" ? window : this);

/* Trilha 1 · Pilar 6 · Aprofundamento 6B · Viabilidade
   Ficha "Faça agora · A sua conta" (página 6B do Dossiê de Desenvolvimento, irmã das páginas 6 e 6A).
   Lógica pura, sem DOM: roda no navegador (window.ZVIAB) e no Node (testes).
   Regra: toda conta, alerta, régua e texto de leitura que a ficha mostra sai daqui, para ser testado.
   Fonte das regras: producao/trilha1-aprofundamento/02-viabilidade/PLANO.md, seções 6, 7 e 13.
   "Não sei" é sempre o texto "nao_sei", nunca um zero escondido. A ficha nunca insere valor de referência
   (imposto, reserva, valor-hora, cancelamento, taxa): só o múltiplo da régua entra, e só pelo botão. */
(function (raiz) {
  "use strict";

  /* ------------------------------------------------------------------
     1. Leitura e formatação pt-BR (as mesmas regras das fichas 6 e 6A)
     ------------------------------------------------------------------ */
  var NS = "nao_sei";
  var BRANCO = "branco";
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
  /** Arredonda sem o erro de vírgula flutuante; no empate exato, para cima (como as tabelas do PLANO, seção 7). */
  function arred(x, casas) {
    if (casas === undefined) casas = 2;
    var f = Math.pow(10, casas); var y = Number((Math.abs(x) * f).toPrecision(12));
    var i = Math.floor(y); var d = y - i;
    if (Math.abs(d - 0.5) < 1e-7) i += 1; else i = Math.round(y);
    var r = i / f; var res = x < 0 ? -r : r; return Object.is(res, -0) ? 0 : res;
  }
  function agrupar(i) { return i.replace(/\B(?=(\d{3})+(?!\d))/g, "."); }
  function fmtNum(x, casas) { if (casas === undefined) casas = 2; var r = arred(x, casas); var p = Math.abs(r).toFixed(casas).split("."); return (r < 0 ? "-" : "") + agrupar(p[0]) + (casas > 0 ? "," + p[1] : ""); }
  function fmtN(x, casasMax) { var s = fmtNum(x, casasMax === undefined ? 2 : casasMax); return s.indexOf(",") >= 0 ? s.replace(/,?0+$/, "") : s; }
  function ok(x) { return typeof x === "number" && Number.isFinite(x); }
  function brl(x) { if (!ok(x)) return "em branco"; var r = arred(x, 2); return (r < 0 ? "-" : "") + "R$ " + fmtNum(Math.abs(r), 2); }
  function brl0(x) { if (!ok(x)) return "em branco"; var r = arred(x, 0); return (r < 0 ? "-" : "") + "R$ " + fmtNum(Math.abs(r), 0); }
  function fmtPct(frac, casas) { if (!ok(frac)) return "não se calcula"; return fmtNum(frac * 100, casas === undefined ? 1 : casas) + "%"; }
  function fmtPontos(frac) { if (!ok(frac)) return "não se calcula"; return fmtNum(frac * 100, 1) + (Math.abs(arred(frac * 100, 1)) === 1 ? " ponto" : " pontos"); }
  function fmtVolta(v) { if (v === null || v === undefined || (typeof v === "number" && isNaN(v))) return "não se calcula"; if (v === Infinity) return "não se paga"; if (v > 100) return "mais de 100 anos"; return fmtNum(v, 1) + " anos"; }
  function juntar(itens) { if (!itens.length) return ""; if (itens.length === 1) return itens[0]; return itens.slice(0, -1).join(", ") + " e " + itens[itens.length - 1]; }
  function div(a, b) { if (!ok(a) || !ok(b) || b === 0) return null; var q = a / b; return Number.isFinite(q) ? q : null; }
  function ehNS(v) { return v === NS; }
  function txt(v) { return typeof v === "string" ? v.trim() : ""; }
  function inteiro(v) { var n = paraNumero(v); return n !== null && Math.floor(n) === n ? n : null; }
  var EPS = 1e-9;
  function numTexto(v) { var r = arred(v, 2); return Math.floor(r) === r ? fmtNum(r, 0) : fmtNum(r, 2); }
  function dataOk(iso) { return typeof iso === "string" && /^\d{4}-\d{2}-\d{2}$/.test(iso) && !isNaN(Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10))); }
  function diaUTC(iso) { return Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10)); }
  function diasEntre(de, ate) { if (!dataOk(de) || !dataOk(ate)) return null; return Math.round((diaUTC(ate) - diaUTC(de)) / 86400000); }
  function somaDias(iso, n) { var d = new Date(diaUTC(iso) + n * 86400000); return d.toISOString().slice(0, 10); }
  function dataBR(iso) { return dataOk(iso) ? iso.split("-").reverse().join("/") : ""; }
  function clone(x) { return JSON.parse(JSON.stringify(x)); }

  /* ------------------------------------------------------------------
     2. Dados da ficha (perguntas, opções, linhas sugeridas só com o nome)
     ------------------------------------------------------------------ */
  var SITUACOES = [
    { v: "terreno", r: "Tenho um terreno e ainda não hospedo ninguém" },
    { v: "ideia", r: "Tenho uma ideia, ou o capital, e ainda não tenho o terreno" },
    { v: "opero", r: "Já opero uma hospedagem e quero crescer" },
  ];
  var DIAG = [
    { id: "d1", p: "Você tem a lista dos custos fixos?", op: [{ v: "sim", r: "Sim" }, { v: "parte", r: "Em parte" }, { v: "nao", r: "Não" }] },
    { id: "d2", p: "O contador já respondeu o imposto sobre a receita?", op: [{ v: "sim", r: "Sim" }, { v: "nao", r: "Não" }] },
    { id: "d3", p: "O seu trabalho está na conta?", op: [{ v: "sim", r: "Sim" }, { v: "nao", r: "Não" }, { v: "naoTrabalho", r: "Não trabalho na operação" }] },
    { id: "d4", p: "Você tem a curva do ano do Pilar 2?", op: [{ v: "sim", r: "Sim" }, { v: "nao", r: "Não" }] },
  ];
  var MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
  var MESES_LONGOS = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
  var TIPOS_MES = [{ v: "alta", r: "Alta" }, { v: "medio", r: "Médio" }, { v: "fraco", r: "Fraco" }];
  var ORIGENS = [{ v: "cotacao", r: "Cotação" }, { v: "estimativa", r: "Estimativa" }, { v: "branco", r: "Em branco" }];
  var BASES = [{ v: "porNoite", r: "R$ por noite" }, { v: "porEstadia", r: "R$ por estadia" }, { v: "pctReceita", r: "% da receita de hospedagem" }];
  /* Os sete grupos de custo fixo da Planilha 2, aba Modelo de renda, linhas 18 a 24. */
  var GRUPOS_P2 = [
    { v: "equipe", r: "Equipe (B18)", cel: "B18" }, { v: "energia", r: "Energia, água e gás (B19)", cel: "B19" },
    { v: "internet", r: "Internet e sistema de reservas (B20)", cel: "B20" }, { v: "manutencao", r: "Manutenção e jardinagem (B21)", cel: "B21" },
    { v: "marketing", r: "Marketing e fotos (B22)", cel: "B22" }, { v: "contabilidade", r: "Contabilidade, seguros e taxas (B23)", cel: "B23" },
    { v: "outros", r: "Outros fixos (B24)", cel: "B24" },
  ];
  var VEREDITOS = [
    { v: "Avançar", t: "A conta fecha na régua, com os números medidos." },
    { v: "Testar", t: "A conta depende de número que falta ou de premissa ainda não provada: prove antes de decidir." },
    { v: "Ajustar", t: "A conta fecha com folga curta em algum passo: mexa em uma alavanca e refaça." },
    { v: "Pausar", t: "Escolha sua, nunca sugerida: o risco não cabe na sua vida agora." },
    { v: "Redesenhar", t: "Neste desenho a conta não fecha: não assine a obra e redesenhe tamanho, produto ou fase." },
  ];
  var ALAVANCAS = [
    { v: "diaria", r: "Diária", un: "R$", min: -300, max: 300, passo: 10, dica: "De R$ 300 a menos até R$ 300 a mais." },
    { v: "ocupacao", r: "Ocupação", un: "pontos", min: -15, max: 15, passo: 1, dica: "De 15 pontos a menos até 15 a mais." },
    { v: "fixo", r: "Custo fixo", un: "%", min: -30, max: -5, passo: 5, dica: "De 5% a 30% a menos." },
    { v: "capex", r: "CAPEX", un: "%", min: -30, max: -5, passo: 5, dica: "De 5% a 30% a menos." },
    { v: "unidades", r: "Unidades da fase", un: "unidades", min: 1, max: 200, passo: 1, dica: "Menos unidades, com o CAPEX de cada unidade que sai digitado." },
    { v: "extras", r: "Outras receitas", un: "", min: 0, max: 1, passo: 1, dica: "Liga ou desliga as outras receitas que você listou." },
  ];
  var LIMITES = { dinheiroMax: 100000000, unidadesMax: 200, diariaMax: 100000, varMax: 100000, varPctMax: 20, varLinhasMax: 10, fixLinhasMax: 15, extrasMax: 4,
    impostoMax: 40, comissaoMax: 50, cartaoMax: 10, cancelMax: 20, horasMax: 80, valorHoraMax: 1000, gestaoMax: 50, royaltyMax: 30, reservaMax: 20,
    taxaMax: 30, multiploMax: 15, estadiaMax: 30, textoMin: 10, textoMax: 300, prazoDias: 30, quemMin: 2, quemMax: 80 };
  var SEMANAS_MES = 4.33;
  var MULTIPLO_REGUA = 6;

  var _seq = 0;
  function novoId(p) { _seq += 1; return p + Date.now().toString(36) + _seq; }
  function novaLinhaVar(o) { o = o || {}; return { id: o.id || novoId("v"), nome: o.nome || "", base: o.base || "porNoite", valor: o.valor === undefined ? "" : o.valor, origem: o.origem || null }; }
  function novaLinhaFixa(o) { o = o || {}; return { id: o.id || novoId("f"), nome: o.nome || "", valor: o.valor === undefined ? "" : o.valor, periodo: o.periodo || "mensal", origem: o.origem || null, grupo: o.grupo || "outros", jaExiste: o.jaExiste === true }; }
  function novoExtra(o) { o = o || {}; return { id: o.id || novoId("x"), nome: o.nome || "", captura: o.captura === undefined ? "" : o.captura, ticket: o.ticket === undefined ? "" : o.ticket, custoDireto: o.custoDireto === undefined ? "" : o.custoDireto, naConta: o.naConta !== false }; }
  /* Linhas sugeridas: somente o nome e a forma de contar, nunca valor (PLANO 6.1, telas 4 e 5). */
  function linhasVarSugeridas() {
    return [["Lavanderia ou enxoval", "porEstadia"], ["Amenidades e boas-vindas", "porEstadia"], ["Energia, água e gás da noite", "porNoite"], ["Produtos de limpeza e reposição", "porNoite"], ["Perdas e quebras de material", "pctReceita"]]
      .map(function (x) { return novaLinhaVar({ nome: x[0], base: x[1] }); });
  }
  function linhasFixasSugeridas() {
    return [["Pessoa local (salário e encargos)", "equipe"], ["13º e férias", "equipe"], ["Folguista", "equipe"], ["Energia das áreas comuns e bomba", "energia"], ["Internet e sistema de reservas", "internet"], ["Contador", "contabilidade"],
      ["Seguro", "contabilidade"], ["Imposto do imóvel, taxas e licença anual", "contabilidade"], ["Manutenção preventiva e jardinagem", "manutencao"], ["Marketing e fotos", "marketing"], ["Tarifas e outros", "outros"]]
      .map(function (x) { return novaLinhaFixa({ nome: x[0], grupo: x[1] }); });
  }
  function estadoInicial(hoje) {
    return {
      nome: "", projeto: "", cidadeUF: "", situacao: null, paraOutro: false, contaAmpliacao: false, extrato: false, d1: null, d2: null, d3: null, d4: null, turma: "autonomo",
      capex: "", giro6A: "", terreno: "", unidades: "", margem6: "", margem6Origem: "", limite6: "", resultado6: "", origemCapex: "digitado",
      diaria: "", diariaMedida: "", calendario: [null, null, null, null, null, null, null, null, null, null, null, null], ocupAlta: "", ocupMedia: "", ocupFraco: "", ocupBase: "", ocupOtim: "",
      mesAbertura: "", estadiaMedia: "", extras: [], p2MesesAlta: "", p2MesesFraco: "", p2OcupAno: "", ocup6: "",
      imposto: "", impostoQuem: "", impostoData: "", impostoRegime: "", pPlataforma: "", comissaoPlataforma: "", cartaoDireto: "", cancelamento: "", comissaoNaoDuplicada: false,
      varLinhas: [], fixLinhas: [], duodecimos: false, horasSemana: "", valorHora: "", naoTrabalho: false, aluguelMes: "", gestaoPct: "", royaltyPct: "", semModelo: false,
      reservaRep: "", giro6B: "", giroJustificativa: "", taxa: "", taxaAntes: false, multiploSaida: "", multiploRef: false, capexPorUnidade: "",
      ajustado: { diaria: "", ocup: "", fixoPct: "", capexPct: "", extras: false },
      vereditoPessoa: null, criterioParar: "", acao30: "", acaoEditada: false, prazo: "", verificacao: "", pdfBaixado: false, exemplo: false, hoje: hoje || "",
    };
  }

  /* ------------------------------------------------------------------
     3. Leituras das outras páginas do Dossiê (tolerantes: se falhar, fica vazio)
     ------------------------------------------------------------------ */
  function objetoDe(raw) {
    var d = raw;
    if (typeof raw === "string") { try { d = JSON.parse(raw); } catch (e) { d = null; } }
    return d && typeof d === "object" && !Array.isArray(d) ? d : null;
  }
  function dadosDe(d) { return (d.resumo && typeof d.resumo === "object" && d.resumo.dados && typeof d.resumo.dados === "object" && d.resumo.dados) || (d.dados && typeof d.dados === "object" ? d.dados : null) || {}; }
  /** Página 6A (zion-t1-pilar6a): CAPEX, giro, investimento, terreno, unidades, limite. */
  function lerPagina6A(raw) {
    var d = objetoDe(raw); if (!d) return null;
    var x = dadosDe(d), n = function (k) { return paraNumero(x[k]); };
    var P = { capex: n("capex_fase"), giro: n("giro"), investimento: n("investimento_total"), terreno: n("terreno"), terrenoSituacao: typeof x.terreno_situacao === "string" ? x.terreno_situacao : null,
      unidades: inteiro(x.unidades), unidadesProjeto: inteiro(x.unidades_projeto), limite6: n("limite6") };
    P.temDados = P.capex !== null && P.capex > 0;
    return P;
  }
  /** Página 6 (zion-t1-pilar6): diária, ocupações, margem e a origem dela, resultado e limite. */
  function lerPagina6(raw) {
    var d = objetoDe(raw); if (!d) return null;
    var x = dadosDe(d), n = function (k) { return paraNumero(x[k]); };
    var fonteMargem = d.fontes && typeof d.fontes === "object" ? d.fontes.margem : null;
    var P = { diaria: n("diaria"), ocupCons: n("ocup_cons"), ocupBase: n("ocup_base"), ocupOtim: n("ocup_otim"), margem: n("margem"), resultadoCons: n("resultado_cons"), inv8: n("inv8"),
      unidades: inteiro(x.unidades), giro: n("giro"), terreno: n("terreno"), fonteMargem: typeof fonteMargem === "string" ? fonteMargem : null };
    P.margemOrigem = P.margem === null ? "" : (P.fonteMargem === "lista" ? "lista de custos ou extrato (página 6)" : P.fonteMargem === "falado" ? "alguém que opera falou (página 6)" : "referência da Zion (página 6)");
    P.temDados = ["diaria", "ocupCons", "margem", "resultadoCons", "inv8"].some(function (k) { return P[k] !== null; });
    return P;
  }
  /** Página 2 (zion-t1-aula2): diária média, ocupação do ano e as respostas da curva do ano. */
  function lerPagina2(raw) {
    var d = objetoDe(raw); if (!d) return null;
    var x = dadosDe(d), r = d.respostas && typeof d.respostas === "object" ? d.respostas : {};
    var n = function (k) { return paraNumero(r[k]); };
    var P = { diariaMedia: paraNumero(x.diaria_media), ocupAno: paraNumero(x.ocup_ano), mesesAlta: inteiro(r.meses_alta), mesesFraco: inteiro(r.meses_fraco), ocupAlta: n("ocup_alta"), ocupMedia: n("ocup_media"), ocupFraco: n("ocup_fraco") };
    P.temDados = ["diariaMedia", "ocupAno", "mesesAlta", "ocupAlta"].some(function (k) { return P[k] !== null; });
    return P;
  }
  function lerMarcoZero(raw) {
    var d = objetoDe(raw); if (!d) return null;
    var s = d.situacao || (d.respostas && d.respostas.situacao) || "";
    return { situacao: SITUACOES.some(function (x) { return x.v === s; }) ? s : null, nome: txt(d.nome || (d.perfil && d.perfil.nome)) };
  }
  /** Preenche só os campos vazios. Devolve { campo: "página 6A" | "página 6" | "página 2" } do que foi preenchido. */
  function aplicarLeituras(E, L) {
    var veio = {};
    if (!E || !L) return veio;
    var PCT = { margem6: 1, ocup6: 1, ocupBase: 1, ocupOtim: 1, ocupAlta: 1, ocupMedia: 1, ocupFraco: 1, p2OcupAno: 1 };
    var poe = function (campo, v, origem) { if (v === null || v === undefined || v === "") return; if (!falta(E[campo]) || ehNS(E[campo])) return; E[campo] = typeof v === "number" ? (PCT[campo] ? fmtN(v, 2) : numTexto(v)) : v; veio[campo] = origem; };
    var A = L.p6a, P6 = L.p6, P2 = L.p2;
    if (A && A.temDados) {
      poe("capex", A.capex, "página 6A"); poe("giro6A", A.giro, "página 6A"); poe("terreno", A.terreno, "página 6A"); poe("unidades", A.unidades, "página 6A"); poe("limite6", A.limite6, "página 6A");
      E.origemCapex = "6A";
    }
    if (P6) {
      poe("unidades", P6.unidades, "página 6"); poe("giro6A", P6.giro, "página 6"); poe("terreno", P6.terreno, "página 6");
      poe("margem6", P6.margem, "página 6"); if (veio.margem6) E.margem6Origem = P6.margemOrigem;
      poe("limite6", P6.inv8, "página 6"); poe("resultado6", P6.resultadoCons, "página 6"); poe("ocup6", P6.ocupCons, "página 6");
      poe("diaria", P6.diaria, "página 6"); poe("ocupBase", P6.ocupBase, "página 6"); poe("ocupOtim", P6.ocupOtim, "página 6");
    }
    if (P2) {
      if (P2.diariaMedia !== null) { poe("diaria", Math.round(P2.diariaMedia), "página 2"); poe("diariaMedida", P2.diariaMedia, "página 2"); }
      poe("ocupAlta", P2.ocupAlta, "página 2"); poe("ocupMedia", P2.ocupMedia, "página 2"); poe("ocupFraco", P2.ocupFraco, "página 2");
      poe("p2MesesAlta", P2.mesesAlta, "página 2"); poe("p2MesesFraco", P2.mesesFraco, "página 2"); poe("p2OcupAno", P2.ocupAno, "página 2");
    }
    return veio;
  }

  /* ------------------------------------------------------------------
     4. Linhas e validação dos números de cada linha
     ------------------------------------------------------------------ */
  function entreN(n, lo, hi) { return n !== null && n >= lo - EPS && n <= hi + EPS; }
  function valorVar(l) {
    if (!l || l.origem === BRANCO || !l.origem) return 0;
    var v = paraNumero(l.valor);
    if (l.base === "pctReceita") return entreN(v, 0, LIMITES.varPctMax) ? v / 100 : null;
    return v !== null && v > 0 && v <= LIMITES.varMax ? v : null;
  }
  function erroVar(l) {
    var n = txt(l.nome);
    if (n.length < 2 || n.length > 80) return "Dê um nome à linha (2 a 80 letras).";
    if (!l.origem) return "Diga de onde vem o número de \"" + n + "\": cotação, estimativa ou em branco.";
    if (l.origem === BRANCO) return "";
    if (valorVar(l) === null) return l.base === "pctReceita" ? "Em \"" + n + "\": a porcentagem vai de 0% a 20%." : "Em \"" + n + "\": escreva um valor maior que zero (até R$ 100 mil), ou marque Em branco.";
    return "";
  }
  /** Valor mensal equivalente de uma linha fixa (anual ÷ 12, o duodécimo). */
  function valorFixoMes(l) {
    if (!l || l.origem === BRANCO || !l.origem) return 0;
    var v = paraNumero(l.valor);
    if (v === null || v <= 0 || v > LIMITES.dinheiroMax) return null;
    return l.periodo === "anual" ? v / 12 : v;
  }
  function erroFixa(l) {
    var n = txt(l.nome);
    if (n.length < 2 || n.length > 80) return "Dê um nome à linha (2 a 80 letras).";
    if (!l.origem) return "Diga de onde vem o número de \"" + n + "\": cotação, estimativa ou em branco.";
    if (l.origem === BRANCO) return "";
    if (valorFixoMes(l) === null) return "Em \"" + n + "\": escreva um valor maior que zero, ou marque Em branco.";
    return "";
  }
  function fixaConta(E, l) { return !(E.contaAmpliacao === true && E.situacao === "opero" && l.jaExiste === true); }
  function erroExtra(x) {
    var n = txt(x.nome);
    if (n.length < 2 || n.length > 60) return "Dê um nome à outra receita (2 a 60 letras).";
    var c = paraNumero(x.captura), t = paraNumero(x.ticket), cd = falta(x.custoDireto) ? 0 : paraNumero(x.custoDireto);
    if (!entreN(c, 0, 100)) return "Em \"" + n + "\": quantas estadias compram, de 0% a 100%.";
    if (t === null || t <= 0 || t > LIMITES.varMax) return "Em \"" + n + "\": escreva o preço de cada venda, maior que zero.";
    if (cd === null || cd < 0 || cd > LIMITES.varMax) return "Em \"" + n + "\": o custo direto vai de R$ 0 para cima.";
    return "";
  }
  /** Outras receitas com preço menor ou igual ao custo direto: não fecham nem a própria venda. */
  function extrasSemGanho(E) { return (E.extras || []).filter(function (x) { var t = paraNumero(x.ticket), cd = falta(x.custoDireto) ? 0 : paraNumero(x.custoDireto); return t !== null && cd !== null && t <= cd + EPS; }); }

  /* ------------------------------------------------------------------
     5. Parâmetros (E → números) e as contas (PLANO 6.2)
     ------------------------------------------------------------------ */
  function ocupMes(E, tipo) { var v = tipo === "alta" ? E.ocupAlta : tipo === "medio" ? E.ocupMedia : tipo === "fraco" ? E.ocupFraco : null; var n = paraNumero(v); return entreN(n, 0, 100) ? n : null; }
  function calendarioCompleto(E) { return Array.isArray(E.calendario) && E.calendario.length === 12 && E.calendario.every(function (t) { return t === "alta" || t === "medio" || t === "fraco"; }); }
  function contagens(E) { var c = { alta: 0, medio: 0, fraco: 0 }; (E.calendario || []).forEach(function (t) { if (c[t] !== undefined) c[t] += 1; }); return c; }
  /** Ocupação de cada mês do calendário (pontos percentuais), ou null se faltar. */
  function ocupacoesDoCalendario(E) {
    if (!calendarioCompleto(E)) return null;
    var o = E.calendario.map(function (t) { return ocupMes(E, t); });
    return o.some(function (x) { return x === null; }) ? null : o;
  }
  function ocupConsDe(E) { var o = ocupacoesDoCalendario(E); return o ? o.reduce(function (s, x) { return s + x; }, 0) / 12 : null; }
  function impostoValido(E) {
    if (E.imposto === BRANCO) return false;
    var n = paraNumero(E.imposto);
    if (!entreN(n, 0, LIMITES.impostoMax)) return false;
    var q = txt(E.impostoQuem);
    if (q.length < LIMITES.quemMin || q.length > LIMITES.quemMax) return false;
    if (!dataOk(E.impostoData)) return false;
    if (dataOk(E.hoje) && diasEntre(E.impostoData, E.hoje) < 0) return false;
    return true;
  }
  function retiradaMes(E) {
    if (E.naoTrabalho === true) return 0;
    var h = paraNumero(E.horasSemana), v = paraNumero(E.valorHora);
    if (!entreN(h, 0, LIMITES.horasMax) || !entreN(v, 0, LIMITES.valorHoraMax)) return null;
    return h * v * SEMANAS_MES;
  }
  function pctOuZero(v, max) { if (falta(v)) return 0; var n = paraNumero(v); return entreN(n, 0, max) ? n / 100 : null; }
  /** Converte as respostas em números. Devolve { P, faltas }: P só vem se as contas forem possíveis. */
  function parametros(E) {
    E = E || {};
    var faltas = [];
    var u = inteiro(E.unidades), capex = paraNumero(E.capex), diaria = paraNumero(E.diaria), est = paraNumero(E.estadiaMedia), mes = inteiro(E.mesAbertura);
    var o = ocupacoesDoCalendario(E);
    if (!(u !== null && u >= 1 && u <= LIMITES.unidadesMax)) faltas.push("as unidades da fase");
    if (!(capex !== null && capex > 0 && capex <= LIMITES.dinheiroMax)) faltas.push("o CAPEX da fase");
    if (!(diaria !== null && diaria >= 1 && diaria <= LIMITES.diariaMax)) faltas.push("a diária");
    if (!o) faltas.push("o calendário dos 12 meses com as ocupações");
    if (!(mes !== null && mes >= 1 && mes <= 12)) faltas.push("o mês de abertura");
    if (!(est !== null && est >= 1 && est <= LIMITES.estadiaMax)) faltas.push("a estadia média");
    var ocupBase = paraNumero(E.ocupBase), ocupOtim = paraNumero(E.ocupOtim);
    var oc = o ? o.reduce(function (s, x) { return s + x; }, 0) / 12 : null;
    if (!(entreN(ocupBase, 0, 100))) faltas.push("a ocupação do cenário base");
    if (!(entreN(ocupOtim, 0, 100))) faltas.push("a ocupação do cenário otimista");
    var pPlat = pctOuZero(E.pPlataforma, 100), comPlat = pctOuZero(E.comissaoPlataforma, LIMITES.comissaoMax), cartao = pctOuZero(E.cartaoDireto, LIMITES.cartaoMax), canc = pctOuZero(E.cancelamento, LIMITES.cancelMax);
    if ([pPlat, comPlat, cartao, canc].some(function (x) { return x === null; })) faltas.push("as deduções");
    var vNoite = 0, vEstadia = 0, vPct = 0, varRuim = false;
    (E.varLinhas || []).forEach(function (l) { var v = valorVar(l); if (v === null) { varRuim = true; return; } if (l.base === "porEstadia") vEstadia += v; else if (l.base === "pctReceita") vPct += v; else vNoite += v; });
    if (varRuim) faltas.push("o valor de alguma linha do custo de cada noite");
    var fixoLinhas = 0, fixRuim = false;
    (E.fixLinhas || []).forEach(function (l) { if (!fixaConta(E, l)) return; var v = valorFixoMes(l); if (v === null) { fixRuim = true; return; } fixoLinhas += v; });
    if (fixRuim) faltas.push("o valor de alguma linha do custo de cada mês");
    var ret = retiradaMes(E);
    var aluguel = E.semModelo === true || falta(E.aluguelMes) ? 0 : paraNumero(E.aluguelMes), gestao = E.semModelo === true ? 0 : pctOuZero(E.gestaoPct, LIMITES.gestaoMax), royalty = E.semModelo === true ? 0 : pctOuZero(E.royaltyPct, LIMITES.royaltyMax);
    if (aluguel === null || aluguel < 0 || gestao === null || royalty === null) faltas.push("os custos do modelo");
    var reserva = paraNumero(E.reservaRep);
    var extrasTodos = (E.extras || []).filter(function (x) { return erroExtra(x) === ""; }).map(function (x) { return { nome: txt(x.nome), captura: paraNumero(x.captura) / 100, ticket: paraNumero(x.ticket), custo: falta(x.custoDireto) ? 0 : paraNumero(x.custoDireto), naConta: x.naConta !== false }; });
    var imp = impostoValido(E) ? paraNumero(E.imposto) / 100 : 0;
    var terreno = ehNS(E.terreno) || falta(E.terreno) ? null : paraNumero(E.terreno);
    var taxa = ehNS(E.taxa) || falta(E.taxa) ? null : paraNumero(E.taxa);
    var mult = falta(E.multiploSaida) ? null : paraNumero(E.multiploSaida);
    var p2o = paraNumero(E.p2OcupAno);
    var P = {
      u: u, noitesAno: u === null ? null : u * 365, diaria: diaria, oCal: o, somaO: o ? o.reduce(function (s, x) { return s + x; }, 0) : null, ocupCons: oc === null ? null : oc / 100,
      ocupBase: ocupBase === null ? null : ocupBase / 100, ocupOtim: ocupOtim === null ? null : ocupOtim / 100, estadia: est, mesAbertura: mes,
      extras: extrasTodos.filter(function (x) { return x.naConta; }), extrasTodos: extrasTodos,
      imposto: imp, impostoBranco: !impostoValido(E), pPlat: pPlat, comPlat: comPlat, cartao: cartao, canc: canc,
      vNoite: vNoite, vEstadia: vEstadia, vPct: vPct, fixoLinhas: fixoLinhas, retirada: ret === null ? 0 : ret, fixoMes: fixoLinhas + (ret === null ? 0 : ret), aluguel: aluguel || 0, gestao: gestao || 0, royalty: royalty || 0,
      reserva: reserva !== null && reserva > 0 && reserva <= LIMITES.reservaMax ? reserva / 100 : 0, capex: capex, terreno: terreno !== null && terreno >= 0 ? terreno : null,
      giro6A: paraNumero(E.giro6A), giro6B: paraNumero(E.giro6B), taxa: taxa !== null && taxa >= 0 && taxa <= LIMITES.taxaMax ? taxa / 100 : null, multiplo: mult !== null && mult > 0 && mult <= LIMITES.multiploMax ? mult : null,
      diariaMedida: paraNumero(E.diariaMedida), ocupMedida: p2o !== null ? p2o / 100 : (oc === null ? null : oc / 100),
    };
    return { P: faltas.length ? null : P, faltas: faltas, parcial: P };
  }
  function rampa(i) { return i <= 3 ? 0.40 : i <= 6 ? 0.50 : i <= 12 ? 0.75 : 1; }
  /** Os seis degraus de um cenário (uma ocupação e uma diária; tudo o mais igual). */
  function cenario(P, ocup, diaria) {
    if (diaria === undefined) diaria = P.diaria;
    var N = P.noitesAno * ocup, est = N / P.estadia;
    var hosp = N * diaria;
    var extras = P.extras.reduce(function (s, x) { return s + est * x.captura * x.ticket; }, 0);
    var bruta = hosp + extras;
    var imp = P.imposto * bruta, com = P.pPlat * P.comPlat * hosp, cart = (1 - P.pPlat) * P.cartao * hosp, canc = P.canc * hosp;
    var deducoes = imp + com + cart + canc, real = bruta - deducoes;
    var vEst = P.vEstadia * est, vNoite = P.vNoite * N, vPct = P.vPct * hosp, vExtras = P.extras.reduce(function (s, x) { return s + x.custo * est * x.captura; }, 0);
    var variaveis = vEst + vNoite + vPct + vExtras, contrib = real - variaveis;
    var fixoAno = 12 * P.fixoMes, antes = contrib - fixoAno;
    var modelo = 12 * P.aluguel + P.gestao * real + P.royalty * bruta, depoisModelo = antes - modelo;
    var reserva = P.reserva * bruta, sobra = depoisModelo - reserva;
    var fixoEq = fixoAno + 12 * P.aluguel;
    return { ocup: ocup, diaria: diaria, N: N, estadias: est, hosp: hosp, extras: extras, bruta: bruta, imposto: imp, comissao: com, cartao: cart, cancelamento: canc, deducoes: deducoes, real: real,
      vEstadia: vEst, vNoite: vNoite, vPct: vPct, vExtras: vExtras, variaveis: variaveis, contrib: contrib, fixoAno: fixoAno, antes: antes, modelo: modelo, depoisModelo: depoisModelo,
      reserva: reserva, sobra: sobra, margem: div(sobra, bruta), fixoEq: fixoEq, X: sobra + fixoEq };
  }
  /** Tempo de volta em escada: CAPEX no ano zero, o primeiro ano com a rampa, depois o que sobra por ano. */
  function escada(capex, ano1, sobra) {
    if (!ok(capex) || !ok(ano1) || !ok(sobra)) return null;
    if (capex <= 0) return 0;
    if (ano1 >= capex - EPS) return capex / ano1;
    if (sobra <= 0) return Infinity;
    return 1 + (capex - ano1) / sobra;
  }
  function vp(fluxos, capex, i, saidaValor) {
    var s = -capex;
    for (var t = 1; t <= fluxos.length; t++) s += fluxos[t - 1] / Math.pow(1 + i, t);
    if (saidaValor) s += saidaValor / Math.pow(1 + i, fluxos.length);
    return s;
  }
  /** A taxa em que o valor presente vira negativo (só para leitura), por bissecção. */
  function taxaVirada(fluxos, capex, saidaValor) {
    if (vp(fluxos, capex, 0, saidaValor) <= 0) return null;
    var lo = 0, hi = 10;
    if (vp(fluxos, capex, hi, saidaValor) > 0) return null;
    for (var k = 0; k < 200; k++) { var m = (lo + hi) / 2; if (vp(fluxos, capex, m, saidaValor) > 0) lo = m; else hi = m; }
    return (lo + hi) / 2;
  }
  /* As cinco réguas (ZAIOS 1.2): os passos usam o valor sem arredondar; a borda fica na faixa melhor. */
  function classPasso1(sobra) { return ok(sobra) ? (sobra >= -EPS ? "passa" : "redesenhar") : null; }
  function classPasso2(sobraQueda, fixoMes) { if (!ok(sobraQueda)) return null; if (sobraQueda >= -EPS) return "passa"; return -sobraQueda <= 3 * fixoMes + 1e-6 ? "ajustar" : "redesenhar"; }
  function classPasso3(volta) { if (volta === null || volta === undefined) return null; if (volta <= 8 + EPS) return "passa"; if (volta <= 12 + EPS) return "ajustar"; return "redesenhar"; }
  function classPasso5(pct) { if (!ok(pct)) return null; if (pct >= 0.10 - EPS) return "passa"; if (pct >= -EPS) return "ajustar"; return "redesenhar"; }
  /** Passo 4: valor presente de dez anos, com a taxa da pessoa; sem taxa, a soma simples decide quando pode. */
  function classPasso4(fluxos, capex, taxa, saidaValor) {
    var somaSem = fluxos.reduce(function (s, x) { return s + x; }, 0);
    if (taxa === null || taxa === undefined) {
      if (somaSem > capex + 1e-6) return { status: "pendente", decidido: false, motivo: "semTaxa" };
      if (!(saidaValor > 0)) return { status: "redesenhar", decidido: true, motivo: "somaSimples" };
      if (somaSem + saidaValor <= capex + 1e-6) return { status: "redesenhar", decidido: true, motivo: "somaSimplesComSaida" };
      return { status: "pendente", decidido: false, motivo: "semTaxaComSaida" };
    }
    var sem = vp(fluxos, capex, taxa, 0), com = saidaValor > 0 ? vp(fluxos, capex, taxa, saidaValor) : sem;
    if (sem >= -1e-6) return { status: "passa", decidido: true, vpSem: sem, vpCom: com };
    if (saidaValor > 0 && com >= -1e-6) return { status: "ajustar", decidido: true, vpSem: sem, vpCom: com, dependeSaida: true };
    return { status: "redesenhar", decidido: true, vpSem: sem, vpCom: com };
  }
  function mesDoCalendario(mesAbertura, i) { return ((mesAbertura - 1 + i - 1) % 12) + 1; }

  /** A análise completa de um conjunto de parâmetros (a conta, uma alavanca ou o cenário ajustado). */
  function analise(P, opt) {
    opt = opt || {};
    var ocupCons = opt.ocupCons !== undefined ? opt.ocupCons : P.ocupCons;
    var A = { ocupCons: ocupCons };
    var cons = cenario(P, ocupCons), base = cenario(P, Math.max(P.ocupBase, 0)), otim = cenario(P, Math.max(P.ocupOtim, 0));
    A.cons = cons; A.base = base; A.otim = otim; A.cen = { cons: cons, base: base, otim: otim };
    var fixoEq = cons.fixoEq; A.fixoEq = fixoEq; A.fixoMesEq = fixoEq / 12; A.fixoMes = P.fixoMes;
    // equilíbrio, custo por diária, diária de equilíbrio e piso
    A.cNoite = div(cons.X, cons.N);
    A.cadaNoitePiora = A.cNoite !== null && A.cNoite <= EPS;
    A.Neq = A.cNoite !== null && A.cNoite > EPS ? fixoEq / A.cNoite : null;
    A.ocupEq = A.Neq === null ? null : A.Neq / P.noitesAno;
    A.folga = A.ocupEq === null ? null : ocupCons - A.ocupEq;
    A.custoPorDiaria = div(cons.bruta - cons.sobra, cons.N);
    var c1 = cenario(P, ocupCons, P.diaria + 1);
    A.efeito1 = c1.sobra - cons.sobra;
    A.diariaEq = A.efeito1 > EPS ? P.diaria - cons.sobra / A.efeito1 : null;
    var cn1 = div(c1.X, c1.N);
    A.piso = A.cNoite !== null && cn1 !== null && cn1 - A.cNoite > EPS ? P.diaria - A.cNoite / (cn1 - A.cNoite) : null;
    // o ano mês a mês (36 meses), com a rampa no calendário
    var somaO = P.somaO;
    var r = null, meses = [], acum = 0, menor = null, menorMes = null;
    if (somaO > 0) {
      var sr = 0;
      for (var i = 1; i <= 36; i++) {
        var m = mesDoCalendario(P.mesAbertura, i), o = P.oCal[m - 1], ra = rampa(i);
        var share = o * ra / somaO;
        var noites = cons.N * share, contrib = cons.X * share, res = contrib - fixoEq / 12;
        acum += res;
        if (i <= 12) sr += o * ra;
        meses.push({ i: i, mes: m, nome: MESES[m - 1], tipo: P.tipos ? P.tipos[m - 1] : null, ocup: o, rampa: ra, noites: noites, contrib: contrib, res: res, acum: acum });
        if (menor === null || acum < menor - 1e-9) { menor = acum; menorMes = i; }
      }
      r = sr / somaO;
    }
    A.r = r; A.meses = meses; A.menorAcum = menor; A.menorMes = menorMes;
    var ano1 = function (c) { return r === null ? null : c.X * r - c.fixoEq; };
    A.ano1 = { cons: ano1(cons), base: ano1(base), otim: ano1(otim) };
    A.ano1Resultado = meses.slice(0, 12).reduce(function (s, x) { return s + x.res; }, 0);
    // o ano em regime e a reserva de sazonalidade
    var regime = meses.slice(12, 24);
    A.regime = regime;
    A.somaRegime = regime.reduce(function (s, x) { return s + x.res; }, 0);
    A.deficitVale = regime.reduce(function (s, x) { return s + (x.res < 0 ? -x.res : 0); }, 0);
    A.mesesAlta = P.tipos ? P.tipos.filter(function (t) { return t === "alta"; }).length : 0;
    A.porMesAlta = A.mesesAlta > 0 ? A.deficitVale / A.mesesAlta : null;
    // giro pelas duas contas do Pilar 6, investimento e colchão
    A.giroA = 3 * (cons.bruta - cons.sobra) / 12;
    A.giroB = menor === null ? null : Math.abs(Math.min(0, menor)) + 3 * fixoEq / 12;
    var cands = [A.giroA]; if (A.giroB !== null) cands.push(A.giroB); if (ok(P.giro6A)) cands.push(P.giro6A);
    A.giroMinimo = Math.max.apply(null, cands);
    A.giro6AInsuficiente = ok(P.giro6A) && P.giro6A < A.giroMinimo - 0.005;
    A.giro6BOk = ok(P.giro6B) && P.giro6B >= A.giroMinimo - 0.005;
    A.giroUsado = A.giro6BOk ? P.giro6B : A.giroMinimo;
    A.investimento = P.capex + A.giroUsado;
    A.colchao = menor === null ? null : A.giroUsado + Math.min(0, menor);
    A.colchaoPct = A.colchao === null ? null : A.colchao / P.capex;
    A.giro10 = menor === null ? null : 0.10 * P.capex - Math.min(0, menor);
    A.folego = div(A.giroUsado, A.fixoMesEq);
    // tempo de volta
    A.volta = { cons: escada(P.capex, A.ano1.cons, cons.sobra), base: escada(P.capex, A.ano1.base, base.sobra), otim: escada(P.capex, A.ano1.otim, otim.sobra) };
    A.voltaP6 = { cons: cons.sobra > 0 ? A.investimento / cons.sobra : Infinity, base: base.sobra > 0 ? A.investimento / base.sobra : Infinity, otim: otim.sobra > 0 ? A.investimento / otim.sobra : Infinity };
    A.voltaTerreno = P.terreno === null ? null : escada(P.capex + P.terreno, A.ano1.cons, cons.sobra);
    A.retorno = div(cons.sobra, P.capex);
    A.retornoTerreno = P.terreno === null ? null : div(cons.sobra, P.capex + P.terreno);
    A.limiteNovo = 8 * Math.max(0, cons.sobra);
    // valor presente de dez anos
    A.fluxos = A.ano1.cons === null ? null : [A.ano1.cons].concat([cons.sobra, cons.sobra, cons.sobra, cons.sobra, cons.sobra, cons.sobra, cons.sobra, cons.sobra, cons.sobra]);
    A.somaSimples = A.fluxos ? A.fluxos.reduce(function (s, x) { return s + x; }, 0) : null;
    A.saida = P.multiplo ? P.multiplo * Math.max(0, cons.depoisModelo) : 0;
    A.vpSem = A.fluxos && P.taxa !== null ? vp(A.fluxos, P.capex, P.taxa, 0) : null;
    A.vpCom = A.fluxos && P.taxa !== null && A.saida > 0 ? vp(A.fluxos, P.capex, P.taxa, A.saida) : null;
    A.taxaViradaSem = A.fluxos ? taxaVirada(A.fluxos, P.capex, 0) : null;
    A.taxaViradaCom = A.fluxos && A.saida > 0 ? taxaVirada(A.fluxos, P.capex, A.saida) : null;
    // teste de queda e sensibilidade do Mapa
    A.queda = cenario(P, ocupCons * 0.80, P.diaria * 0.90);
    A.sobraQueda = A.queda.sobra;
    var voltaCom = function (P2, oc) { var c = cenario(P2, oc); var a1 = r === null ? null : c.X * r - c.fixoEq; return { sobra: c.sobra, ano1: a1, volta: escada(P2.capex, a1, c.sobra) }; };
    var Pd = Object.assign({}, P, { diaria: P.diaria * 0.85 }), Pk = Object.assign({}, P, { capex: P.capex * 1.2 });
    A.sens = { diaria: voltaCom(Pd, ocupCons), ocupacao: voltaCom(P, Math.max(0, ocupCons - 0.10)), capex: voltaCom(Pk, ocupCons) };
    // o que precisa ser verdade (uma premissa por vez), para 8 e 12 anos
    A.verdade = {};
    [8, 12].forEach(function (T) {
      if (r === null) { A.verdade[T] = null; return; }
      var xT = (P.capex + T * fixoEq) / (T - 1 + r);
      var efX = c1.X - cons.X;
      A.verdade[T] = { x: xT, ocup: A.cNoite > EPS ? xT / A.cNoite / P.noitesAno : null, diaria: efX > EPS ? P.diaria + (xT - cons.X) / efX : null, capex: (T - 1) * cons.sobra + A.ano1.cons };
    });
    // a régua da Zion em cinco passos, no cenário medido
    var p4 = A.fluxos ? classPasso4(A.fluxos, P.capex, P.taxa, A.saida) : { status: null, decidido: false };
    A.p4 = p4;
    A.passos = [
      { n: 1, nome: "O ano em regime, no cenário medido", status: classPasso1(cons.sobra) },
      { n: 2, nome: "Teste de queda (diária −10%, ocupação −20%)", status: classPasso2(A.sobraQueda, P.fixoMes) },
      { n: 3, nome: "Tempo de volta em escada", status: classPasso3(A.volta.cons) },
      { n: 4, nome: "Valor presente de dez anos", status: p4.status },
      { n: 5, nome: "Colchão no pior mês", status: classPasso5(A.colchaoPct) },
    ];
    var st = A.passos.map(function (x) { return x.status; });
    A.regua = st.indexOf("redesenhar") >= 0 ? "Redesenhar" : st.indexOf("ajustar") >= 0 ? "Ajustar" : st.indexOf(null) >= 0 ? null : "Avançar";
    if (st.indexOf("redesenhar") < 0 && st.indexOf(null) >= 0) A.regua = null;
    // premissas não provadas (regra do Pilar 6): Testar no lugar de Avançar ou Ajustar
    var prem = [];
    if (P.impostoBranco) prem.push("imposto");
    if (p4.status === "pendente") prem.push("taxa");
    var d = opt.diaria !== undefined ? opt.diaria : P.diaria;
    if (ok(P.diariaMedida) && P.diariaMedida > 0 && d > 1.05 * P.diariaMedida + 1e-6) prem.push("diaria");
    if (ok(P.ocupMedida) && ocupCons > P.ocupMedida + 0.001 + EPS) prem.push("ocupacao");
    if (ocupCons > 0.65 + EPS) prem.push("ocupacao65");
    A.premissas = prem;
    if (A.regua === "Redesenhar") A.sugerido = "Redesenhar";
    else if (prem.length && (A.regua === "Avançar" || A.regua === "Ajustar" || A.regua === null)) A.sugerido = "Testar";
    else A.sugerido = A.regua;
    return A;
  }
  /** Tudo o que a ficha mostra (PLANO 6.2), a partir das respostas. */
  function calcular(E, hoje) {
    E = E || {};
    var pr = parametros(E);
    var C = { pronto: !!pr.P, faltas: pr.faltas, parcial: pr.parcial };
    var P = pr.P;
    if (!P) return C;
    P.tipos = E.calendario.slice();
    C.P = P;
    C.A = analise(P);
    var A = C.A;
    C.ocupCons = P.ocupCons;
    C.retiradaMes = P.retirada;
    C.impostoBranco = P.impostoBranco;
    // de onde vem a diferença com a página 6
    var m6 = paraNumero(E.margem6);
    C.margem6 = m6 === null ? null : m6 / 100;
    C.resultado6 = C.margem6 === null ? null : C.margem6 * A.cons.hosp;
    C.difPontos = C.margem6 === null || A.cons.margem === null ? null : C.margem6 - A.cons.margem;
    var b = A.cons.bruta;
    C.pesos = b > 0 ? { deducoes: A.cons.deducoes / b, variaveis: A.cons.variaveis / b, fixos: (A.cons.fixoAno + A.cons.modelo) / b, reserva: A.cons.reserva / b } : null;
    // B13: a conta só passa no passo 1 ou 3 com as outras receitas
    C.dependeExtras = false;
    if (P.extras.length) {
      var Ps = Object.assign({}, P, { extras: [] }), As = analise(Ps);
      C.dependeExtras = (A.passos[0].status === "passa" && As.passos[0].status !== "passa") || (A.passos[2].status === "passa" && As.passos[2].status !== "passa");
    }
    C.transposicao = transposicao(E, C);
    C.planilha2 = planilha2(E, C);
    return C;
  }

  /* ------------------------------------------------------------------
     6. Alavancas e cenário ajustado (nunca gravam por cima da conta)
     ------------------------------------------------------------------ */
  function aplicarAlavanca(P, tipo, valor, E) {
    var Q = Object.assign({}, P), opt = {};
    if (tipo === "diaria") { if (!entreN(valor, -300, 300) || P.diaria + valor < 1) return null; Q.diaria = P.diaria + valor; opt.diaria = Q.diaria; }
    else if (tipo === "ocupacao") { if (!entreN(valor, -15, 15)) return null; opt.ocupCons = Math.max(0, Math.min(1, P.ocupCons + valor / 100)); }
    else if (tipo === "fixo") { if (!entreN(valor, -30, 0)) return null; Q.fixoMes = P.fixoMes * (1 + valor / 100); Q.fixoLinhas = P.fixoLinhas * (1 + valor / 100); Q.retirada = P.retirada * (1 + valor / 100); }
    else if (tipo === "capex") { if (!entreN(valor, -30, 0)) return null; Q.capex = P.capex * (1 + valor / 100); }
    else if (tipo === "unidades") {
      var cpu = E ? paraNumero(E.capexPorUnidade) : null;
      if (inteiro(valor) === null || valor < 1 || valor >= P.u || cpu === null || cpu <= 0) return null;
      Q.u = valor; Q.noitesAno = valor * 365; Q.capex = P.capex - (P.u - valor) * cpu; if (Q.capex <= 0) return null;
    } else if (tipo === "extras") { Q.extras = valor ? P.extrasTodos.slice() : []; }
    else return null;
    return { P: Q, opt: opt };
  }
  /** Uma alavanca por vez: o que sobra, o primeiro ano, o tempo de volta e o passo 3. */
  function alavanca(E, tipo, valor, hoje) {
    var C = calcular(E, hoje);
    if (!C.pronto) return { ok: false, motivo: "Complete a conta antes de mexer nas alavancas." };
    var x = aplicarAlavanca(C.P, tipo, typeof valor === "boolean" ? valor : paraNumero(valor), E);
    if (!x) return { ok: false, motivo: tipo === "unidades" ? "Escreva quantas unidades ficam (menos que hoje) e o CAPEX de cada unidade que sai." : "Valor fora da faixa desta alavanca." };
    var A = analise(x.P, x.opt);
    return { ok: true, tipo: tipo, valor: valor, sobra: A.cons.sobra, ano1: A.ano1.cons, volta: A.volta.cons, passo3: A.passos[2].status, margem: A.cons.margem, capex: x.P.capex, diaria: x.P.diaria, ocup: A.ocupCons, fixoMes: x.P.fixoMes, A: A };
  }
  function ajustadoDefinido(E) { var a = E.ajustado || {}; return !falta(a.diaria) || !falta(a.ocup) || !falta(a.fixoPct) || !falta(a.capexPct) || a.extras === true; }
  /** O cenário ajustado: uma combinação salva à parte, «o que precisaria ser verdade», pela mesma régua. */
  function ajustado(E, hoje) {
    var C = calcular(E, hoje);
    if (!C.pronto || !ajustadoDefinido(E)) return null;
    var a = E.ajustado, Q = Object.assign({}, C.P), opt = {};
    var d = paraNumero(a.diaria), o = paraNumero(a.ocup), f = paraNumero(a.fixoPct), k = paraNumero(a.capexPct);
    if (!falta(a.diaria)) { if (d === null || d < 1 || d > LIMITES.diariaMax) return { ok: false, motivo: "A diária do ajustado vai de R$ 1 a R$ 100 mil." }; Q.diaria = d; opt.diaria = d; }
    if (!falta(a.ocup)) { if (!entreN(o, 0, 100)) return { ok: false, motivo: "A ocupação do ajustado vai de 0% a 100%." }; opt.ocupCons = o / 100; }
    if (!falta(a.fixoPct)) { if (!entreN(f, -30, 0)) return { ok: false, motivo: "O custo fixo do ajustado muda de 0% a 30% a menos." }; Q.fixoMes = C.P.fixoMes * (1 + f / 100); }
    if (!falta(a.capexPct)) { if (!entreN(k, -30, 0)) return { ok: false, motivo: "O CAPEX do ajustado muda de 0% a 30% a menos." }; Q.capex = C.P.capex * (1 + k / 100); }
    if (a.extras === true) Q.extras = C.P.extrasTodos.slice();
    var A = analise(Q, opt);
    return { ok: true, A: A, P: Q, veredito: A.sugerido, regua: A.regua };
  }

  /* ------------------------------------------------------------------
     7. A volta: página 6 e Planilha 2 (PLANO 6.7). Nada é gravado nelas.
     ------------------------------------------------------------------ */
  function linhaEmBranco(E) { return (E.varLinhas || []).concat(E.fixLinhas || []).some(function (l) { return l.origem === BRANCO; }); }
  function transposicao(E, C) {
    var A = C.A;
    if (!A || A.cons.margem === null) return null;
    var margem = arred(A.cons.margem * 100, 2);
    var nota = !C.impostoBranco && !linhaEmBranco(E) ? 3 : 1;
    var custoMes = (1 - margem / 100) * A.cons.hosp / 12;
    return { margem: margem, nota: nota, notaTxt: nota === 3 ? "Lista de custos ou extrato (nota 3)" : "Referência ou estimativa (nota 1)", giroMeses: custoMes > 0 ? arred(A.giroUsado / custoMes, 2) : null, giro: A.giroUsado };
  }
  function planilha2(E, C) {
    var P = C.P, A = C.A, c = A.cons;
    var grupos = {}; GRUPOS_P2.forEach(function (g) { grupos[g.v] = 0; });
    (E.fixLinhas || []).forEach(function (l) { if (!fixaConta(E, l)) return; var v = valorFixoMes(l) || 0; var g = grupos[l.grupo] !== undefined ? l.grupo : "outros"; grupos[g] += v; });
    grupos.outros += P.retirada + P.aluguel;
    var custoDiretoNoite = P.extras.reduce(function (s, x) { return s + x.custo * x.captura / P.estadia; }, 0);
    var b12 = P.vNoite + P.vEstadia / P.estadia + P.vPct * P.diaria + P.reserva * P.diaria + custoDiretoNoite;
    var b11 = P.pPlat * P.comPlat + (1 - P.pPlat) * P.cartao + P.canc;
    var cel = GRUPOS_P2.map(function (g) { return { cel: g.cel, nome: g.r, valor: grupos[g.v] }; });
    return { unidades: P.u, b5: P.capex, b6: 0, b7: "=" + numTexto(A.giroUsado) + "/B8", diaria: P.diaria, ocup: [P.ocupCons, P.ocupBase, P.ocupOtim], b10: c.hosp > 0 ? c.extras / c.hosp : 0, b11: b11, b12: b12,
      b13: P.impostoBranco ? null : P.imposto, b14: P.gestao, b15: 0, fixos: cel, c25: cel.reduce(function (s, x) { return s + x.valor; }, 0), b50: P.taxa, b65: 0,
      porNoite: P.diaria * (1 - b11 - P.imposto) - b12 };
  }
  var AVISO_P6 = "A página 6 mantém a margem igual nos três cenários e calcula o tempo de volta sem rampa: é a simplificação dela. Os números da página 6 refeita e os da 6B ficam próximos, não iguais. Os dois estão certos dentro da regra de cada um.";
  var AVISO_P2 = "A Planilha 2 põe o giro no ano zero e não tem rampa; a 6B põe o primeiro ano com rampa e testa o giro no colchão. Não misture as duas: compare cada uma com a régua dela.";

  /* ------------------------------------------------------------------
     8. Faixas de leitura (PLANO 6.3) e alertas (PLANO 6.4)
     ------------------------------------------------------------------ */
  var NOTA_FAIXA = "Faixa citada pela fonte; não é meta nem promessa.";
  function leituraMargem(m) {
    if (!ok(m)) return { faixa: null, t: "A margem não se calcula." };
    if (m >= 0.30 - EPS) return { faixa: "boa", t: "Margem de 30% ou mais: boa." };
    if (m >= 0.20 - EPS) return { faixa: "atencao", t: "Margem entre 20% e 30%: atenção." };
    if (m >= 0.10 - EPS) return { faixa: "risco", t: "Margem entre 10% e 20%: risco." };
    return { faixa: "naoFecha", t: "Margem abaixo de 10%: o modelo não fecha." };
  }
  function leituraEquilibrio(A) {
    if (A.cadaNoitePiora) return { faixa: "critico", t: "Cada noite vendida aumenta o prejuízo: o que fica de cada noite não paga nem o custo dela." };
    if (A.folga === null) return { faixa: null, t: "O equilíbrio não se calcula." };
    var est = A.ocupEq > 0.70 + EPS ? " Equilíbrio acima de 70%: problema estrutural, não comercial." : "";
    if (A.folga < -EPS) return { faixa: "critico", t: "O equilíbrio está acima da ocupação medida." + est };
    if (A.folga < 0.05 - EPS) return { faixa: "fina", t: "Folga fina, de 0 a 5 pontos." + est };
    return { faixa: "folga", t: "Com folga: mais de 5 pontos acima do equilíbrio." + est };
  }
  function leituraVolta(v) {
    if (v === null || v === undefined) return "O tempo de volta não se calcula.";
    if (v === Infinity) return "Não se paga: o que sobra no ano é zero ou negativo.";
    if (v <= 5 + EPS) return "Até 5 anos: muito bom, e raro em construção do zero (Pilar 6).";
    if (v <= 8 + EPS) return "De 5 a 8 anos: bom (Pilar 6).";
    if (v <= 12 + EPS) return "De 8 a 12 anos: aceitável quando há valorização relevante (Pilar 6).";
    return "Acima de 12 anos: só com uma razão escrita (Pilar 6).";
  }
  function leituraCancelamento(E) { var c = paraNumero(E.cancelamento); if (c === null) return ""; return c < 1 - EPS || c > 3 + EPS ? "Fora de 1% a 3%, faixa citada pela fonte: confira." : "Dentro de 1% a 3%, faixa citada pela fonte."; }
  var ORDEM_ALERTAS = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15", "B16"];
  var INFO = {
    id: "INFO", tit: "Pergunte ao seu contador",
    contador: ["Qual é o regime mais adequado para o meu caso e qual imposto incide sobre a receita de hospedagem e sobre as outras receitas, com que alíquota efetiva?", "Em que ponto do crescimento (fase dois, fase três) essa resposta muda?", "Quais encargos incidem sobre a minha retirada e sobre o salário da pessoa local?", "Imposto sobre o lucro e distribuição ao sócio: como entram?"],
    advogado: "Contratos de gestão, arrendamento ou sociedade (degrau 5): pergunte ao seu advogado.",
    anote: "Anote a data e o nome de quem respondeu.",
    naoEnvia: "Esta ficha não envia nada: o PDF fica só com você.",
  };
  function alertas(E, C) {
    E = E || {}; C = C || calcular(E);
    var L = [];
    var add = function (id, tipo, tit, t, fonte) { L.push({ id: id, tipo: tipo, tit: tit, txt: t, fonte: fonte }); };
    if (!impostoValido(E)) add("B1", "critico", "O imposto está em branco", "A linha do imposto está em branco. O resultado é antes do imposto sobre a receita, e a régua fica em Testar. Leve a conta ao contador.", "R7; Pilar 6 (compromisso de 7 dias)");
    if (E.origemCapex !== "6A") add("B2", "atencao", "Sem a página 6A", "A 6B parte do CAPEX da 6A. Faça a 6A, ou digite o CAPEX e o giro com a origem.", "Guia de coerência 5.1");
    var A = C.A;
    if (A) {
      var c = A.cons;
      if (c.sobra < -EPS) add("B3", "critico", "No cenário medido, não sobra nada", "No cenário medido, a operação não deixa nada depois da reserva: faltam " + brl(-c.sobra) + " no ano.", "ZAIOS, passo 1");
      if (A.cadaNoitePiora) add("B4", "critico", "Cada noite vendida aumenta o prejuízo", "O que fica de cada noite não paga o custo dela. Não há ocupação que equilibre esta conta.", "R13; JC09");
      else if (A.folga !== null && (A.folga < -EPS || A.ocupEq > 0.70 + EPS)) add("B4", "critico", A.ocupEq > 0.70 + EPS ? "Problema estrutural, não comercial" : "O equilíbrio está acima da ocupação medida", "O equilíbrio pede " + fmtPct(A.ocupEq) + " de ocupação, e o cenário medido tem " + fmtPct(A.ocupCons) + "." + (A.ocupEq > 0.70 + EPS ? " Acima de 70%, é problema estrutural, não comercial." : ""), "R13; JC09");
      if (A.giro6AInsuficiente) add("B5", "atencao", "O giro da 6A sobe", "Com o custo aberto, três meses de custo passam a " + brl(A.giroMinimo) + ": o giro da 6A (" + brl(C.P.giro6A) + ") sobe.", "Pilar 6, cap. 06");
    }
    var p2a = inteiro(E.p2MesesAlta), p2f = inteiro(E.p2MesesFraco), p2o = paraNumero(E.p2OcupAno);
    if (calendarioCompleto(E)) {
      var ct = contagens(E), oc = ocupConsDe(E);
      var difC = (p2a !== null && ct.alta !== p2a) || (p2f !== null && ct.fraco !== p2f);
      var difO = p2o !== null && oc !== null && Math.abs(oc - p2o) > 0.1 + EPS;
      if (difC || difO) add("B6", "atencao", "O calendário não bate com o Pilar 2", (difC ? "O calendário tem " + ct.alta + " meses de alta e " + ct.fraco + " fracos; a página 2 tem " + (p2a === null ? "?" : p2a) + " e " + (p2f === null ? "?" : p2f) + ". " : "") + (difO ? "A ocupação do ano dá " + fmtN(oc, 2) + "%, e a página 2 mediu " + fmtN(p2o, 2) + "%." : ""), "Pilar 2");
    }
    if (A) {
      if (A.colchaoPct !== null && A.colchaoPct < 0.10 - EPS) add("B7", "critico", "Colchão abaixo de 10% do CAPEX", "No pior mês do primeiro ano, sobra " + brl(A.colchao) + " no banco: " + fmtPct(A.colchaoPct) + " do CAPEX, abaixo de 10%. O giro que daria 10% é " + brl(A.giro10) + ".", "ZAIOS 10; Volume 05 · Investimento, cap. 8");
    }
    if (E.naoTrabalho !== true && retiradaMes(E) === 0) add("B8", "critico", "O seu trabalho ficou fora", "«Se o negócio não paga quem o opera, ele não é um negócio.» (Jornada do COMO, Etapa 09) Escreva as suas horas e o valor-hora, ou marque que não trabalha na operação.", "JC09; R10");
    var rr = paraNumero(E.reservaRep);
    if (rr !== null && rr > 0 && rr < 3 - EPS) add("B9", "atencao", "Reserva de reposição abaixo das fontes", "A reserva de reposição está em " + fmtN(rr, 2) + "%. As fontes citam de 3% a 6% da receita bruta. " + NOTA_FAIXA, "R11 (A05 cap. 9; JC09; ZAIOS 4)");
    if (E.comissaoNaoDuplicada !== true || E.duodecimos !== true) add("B10", "bloqueia", "Falta confirmar duas contas", (E.comissaoNaoDuplicada !== true ? "Confirme que a comissão não está também nos custos de cada noite. " : "") + (E.duodecimos !== true ? "Confirme que os gastos anuais estão divididos por 12." : ""), "Erros 5 e 8 do mapa de fontes");
    if (A) {
      var l6 = paraNumero(E.limite6);
      if (l6 !== null && A.investimento > A.limiteNovo + 0.005) add("B11", "critico", "O limite da página 6 era premissa", "O limite da página 6 (" + brl(l6) + ") foi feito com a margem de referência. Com a margem aberta, ele passa a " + brl(A.limiteNovo) + " (8 × o que sobra), e o investimento refeito é " + brl(A.investimento) + ".", "Pilar 6, cap. 07");
      if (A.p4.status === "ajustar" && A.p4.dependeSaida) add("B12", "critico", "Só a venda do negócio salva a conta", "Sem a venda do negócio, o valor presente é negativo. A decisão é ajustar, nunca avançar.", "R23; ZAIOS 3");
      if (C.dependeExtras) add("B13", "atencao", "A conta depende das outras receitas", "Sem as outras receitas, a conta não passa no passo 1 ou no passo 3. Outras receitas são complemento, não fundação.", "R6 (A05; F02)");
      if (P_taxaVazia(E) && A.p4.status === "pendente") add("B14", "ns", "Escreva a sua taxa antes de ver o resultado", "A soma simples dos dez anos não decide o passo 4. A Zion não sugere taxa: escreva o quanto o seu dinheiro renderia em outro lugar, mais o que você pede pelo risco.", "R22; ZAIOS 2");
      if (A.voltaTerreno !== null && A.voltaTerreno > 12 + EPS) add("B15", "atencao", "Com o terreno, passa de 12 anos", "Com o terreno no ano zero, o tempo de volta vai a " + fmtVolta(A.voltaTerreno) + ": escreva a razão (patrimônio, família, projeto de vida).", "R31; Pilar 6");
    }
    if (E.situacao === "opero" && E.extrato !== true) add("B16", "atencao", "Use o extrato de doze meses", "Quem já opera usa o extrato de doze meses: dado real vence estimativa.", "R30");
    L.sort(function (x, y) { return ORDEM_ALERTAS.indexOf(x.id) - ORDEM_ALERTAS.indexOf(y.id); });
    return L;
  }
  function P_taxaVazia(E) { return falta(E.taxa) || ehNS(E.taxa); }
  function tresPrimeiros(L) { return L.slice(0, 3); }

  /* ------------------------------------------------------------------
     9. Significado, o que fazer em 30 dias e como verificar (PLANO 6.5)
     ------------------------------------------------------------------ */
  var NOME_PREMISSA = { imposto: "o imposto está em branco", taxa: "a taxa do seu dinheiro não foi escrita e a soma simples não decide", diaria: "a diária passa de 5% acima da medida no Pilar 2", ocupacao: "a ocupação passa da medida no Pilar 2", ocupacao65: "a ocupação passa de 65%" };
  function motivoVeredito(A) {
    if (!A) return "Complete a conta para ver a régua.";
    var nos = function (st) { var n = A.passos.filter(function (p) { return p.status === st; }).map(function (p) { return String(p.n); }); return n.length === 1 ? "no passo " + n[0] : "nos passos " + juntar(n); };
    if (A.sugerido === "Redesenhar") return "Redesenhar " + nos("redesenhar") + ": neste desenho a conta não fecha.";
    if (A.sugerido === "Testar") return "A régua dá " + (A.regua || "um resultado ainda pendente") + ", mas " + juntar(A.premissas.map(function (k) { return NOME_PREMISSA[k]; })) + ": prove antes de decidir.";
    if (A.sugerido === "Ajustar") return "Ajustar " + nos("ajustar") + ": a conta fecha com folga curta.";
    if (A.sugerido === "Avançar") return "Os cinco passos passam, com os números medidos.";
    return "A régua ainda está pendente.";
  }
  var ACOES = {
    1: { acao: "Levar a conta ao contador com as perguntas do checklist e anotar o imposto sobre a receita.", verificacao: "A alíquota anotada, com a data e o nome de quem respondeu." },
    2: { acao: "Rodar a 6B com três redesenhos, uma alavanca por vez, e não assinar contrato de obra.", verificacao: "As três versões da 6B salvas, com data." },
    3: { acao: "Provar a premissa: teste de preço ou pesquisa de comparáveis para a diária; calendário dos comparáveis para a ocupação (Pilar 2).", verificacao: "A pesquisa anotada, com data e fonte." },
    4: { acao: "Recalcular o pedido de capital com o giro que dá 10% de colchão e levar ao Pilar 7.", verificacao: "O número escrito na página 7." },
    5: { acao: "Escolher uma alavanca e escrever a razão, se o tempo de volta ficar acima de 8 anos.", verificacao: "A 6B refeita e a razão escrita." },
    6: { acao: "Pedir proposta escrita das três maiores despesas fixas.", verificacao: "As propostas, com data." },
    7: { acao: "Refazer a página 6 e a Planilha 2 pelos quadros e seguir ao Pilar 7.", verificacao: "A página 6 refeita e a Planilha 2 preenchida." },
  };
  var VERIFICACOES = [1, 2, 3, 4, 5, 6, 7].map(function (k) { return ACOES[k].verificacao; });
  function acaoSugerida(E, C) {
    C = C || calcular(E);
    var dono = E.paraOutro === true;
    var pega = function (n) { var a = ACOES[n]; return { ordem: n, acao: (dono && n === 7 ? "Levar a página 6B ao dono. " : "") + a.acao, verificacao: a.verificacao }; };
    if (!impostoValido(E)) return pega(1);
    var A = C.A;
    if (!A) return pega(6);
    if (A.sugerido === "Redesenhar") return pega(2);
    if (A.sugerido === "Testar" && A.premissas.some(function (k) { return k === "diaria" || k === "ocupacao" || k === "ocupacao65"; })) return pega(3);
    if (A.passos[4].status === "ajustar") return pega(4);
    if (A.passos[2].status === "ajustar") return pega(5);
    if ((E.fixLinhas || []).some(function (l) { return l.origem !== "cotacao"; })) return pega(6);
    return pega(7);
  }
  function proximaEtapa(E) {
    var dono = E && E.paraOutro === true;
    if (E && E.turma === "acompanhamento") return (dono ? "Leve as páginas 6A e 6B ao dono e ao encontro do Pilar 6" : "Leve as páginas 6A e 6B ao encontro do Pilar 6") + " e refaça a página 6 depois do comentário da equipe.";
    return (dono ? "Salve o PDF na pasta Meu Dossiê e leve a página 6B ao dono. Depois, refaça a página 6" : "Salve o PDF na pasta Meu Dossiê, refaça a página 6") + " com a margem aberta, preencha a Planilha 2 e siga ao Pilar 7.";
  }
  var PROXIMOS = [
    "Salve o PDF da página 6B na pasta Meu Dossiê, ao lado das páginas 6 e 6A.",
    "Refaça a página 6 na ficha do Pilar 6 com o quadro «Como levar para a página 6»: a margem e os meses de giro.",
    "Planilha 1 (opcional, se ainda não fez pela 6A) e Planilha 2 · Estudo de Massas e Viabilidade, pelo quadro «Planilha 2, célula a célula».",
    "Pilar 7: leve o veredito, o critério para parar e, se for Avançar ou Ajustar, o investimento refeito (CAPEX + giro da 6B). Se for Redesenhar ou Testar, os 90 dias do Pilar 7 servem para provar a premissa e refazer as páginas 6, 6A e 6B.",
  ];

  /* ------------------------------------------------------------------
     10. Validação de cada tela (bloqueia o Avançar) e critério de conclusão (PLANO 6.6)
     ------------------------------------------------------------------ */
  var TELAS = ["abertura", "parte", "entra", "real", "noite", "mes", "reserva", "caixa", "vale", "resultado", "alavancas", "veredito", "acao"];
  var NOMES_TELAS = ["Abertura", "De onde você parte", "Quanto entra", "Do bruto ao real", "O custo de cada noite", "O custo de cada mês", "A reserva de reposição", "O primeiro ano e o caixa", "Vale a pena", "Resultado", "Alavancas", "Veredito e critério", "Ação de 30 dias e PDF"];
  function dinheiroOk(v, min) { var n = paraNumero(v); return n !== null && n >= (min === undefined ? 0 : min) && n <= LIMITES.dinheiroMax; }
  function prazoOk(prazo, hoje) { if (!dataOk(prazo) || !dataOk(hoje)) return false; var d = diasEntre(hoje, prazo); return d >= 0 && d <= LIMITES.prazoDias; }
  function erroImposto(E, hoje) {
    if (E.imposto === BRANCO) return "";
    var n = paraNumero(E.imposto);
    if (n === null) return "Escreva o imposto que o seu contador respondeu, com quem e a data, ou marque «em branco, aguardando o contador».";
    if (!entreN(n, 0, LIMITES.impostoMax)) return "O imposto vai de 0% a 40% da receita bruta.";
    var q = txt(E.impostoQuem);
    if (q.length < LIMITES.quemMin || q.length > LIMITES.quemMax) return "Escreva quem respondeu o imposto (2 a 80 letras).";
    if (!dataOk(E.impostoData)) return "Escreva a data da resposta do contador.";
    if (hoje && diasEntre(E.impostoData, hoje) < 0) return "A data da resposta do contador não pode ser no futuro.";
    return "";
  }
  function erroRetirada(E) {
    if (E.naoTrabalho === true) return "";
    var h = paraNumero(E.horasSemana), v = paraNumero(E.valorHora);
    if (!entreN(h, 0, LIMITES.horasMax)) return "Escreva as suas horas por semana na operação (0 a 80), ou marque que não trabalha na operação.";
    if (!entreN(v, 0, LIMITES.valorHoraMax)) return "Escreva o valor-hora (R$ 0 a R$ 1.000): quanto você pagaria a alguém para fazer o que você faz.";
    return "";
  }
  function erroModelo(E) {
    if (E.semModelo === true) return "";
    var a = paraNumero(E.aluguelMes), g = paraNumero(E.gestaoPct), r = paraNumero(E.royaltyPct);
    if (a === null || a < 0 || a > LIMITES.dinheiroMax || !entreN(g, 0, LIMITES.gestaoMax) || !entreN(r, 0, LIMITES.royaltyMax)) return "Nos custos do modelo, escreva aluguel (R$), gestão (0% a 50%) e royalty (0% a 30%), ou marque «não há».";
    if (a === 0 && g === 0 && r === 0) return "Se os três custos do modelo são zero, marque «não há».";
    return "";
  }
  function validarTela(tela, E, hoje) {
    E = E || {}; hoje = hoje || E.hoje;
    var n, i;
    if (tela === "abertura") {
      var nm = txt(E.nome), pj = txt(E.projeto), cid = txt(E.cidadeUF);
      if (nm && (nm.length < 2 || nm.length > 60)) return "O nome vai de 2 a 60 letras (ou deixe em branco).";
      if (pj.length < 2 || pj.length > 60) return "Dê um nome ao projeto (2 a 60 letras).";
      if (cid && (cid.length < 2 || cid.length > 60)) return "A cidade vai de 2 a 60 letras (ou deixe em branco).";
      if (!E.situacao) return "Escolha a frase que descreve a sua situação.";
      for (i = 0; i < DIAG.length; i++) if (!E[DIAG[i].id]) return "Responda às quatro perguntas do diagnóstico.";
      return "";
    }
    if (tela === "parte") {
      n = paraNumero(E.capex); if (n === null || n <= 0 || n > LIMITES.dinheiroMax) return "Escreva o CAPEX da fase (maior que zero, até R$ 100 milhões).";
      if (!dinheiroOk(E.giro6A)) return "Escreva o capital de giro da 6A (R$ 0 a R$ 100 milhões).";
      if (!ehNS(E.terreno) && !falta(E.terreno) && !dinheiroOk(E.terreno)) return "O terreno vai de R$ 0 a R$ 100 milhões, ou toque em Não sei.";
      n = inteiro(E.unidades); if (n === null || n < 1 || n > LIMITES.unidadesMax) return "As unidades da fase vão de 1 a 200, sem casas decimais.";
      if (!falta(E.margem6) && !entreN(paraNumero(E.margem6), 0, 90)) return "A margem da página 6 vai de 0% a 90% (ou deixe em branco).";
      if (!falta(E.limite6) && !dinheiroOk(E.limite6)) return "O limite da página 6 vai de R$ 0 a R$ 100 milhões (ou deixe em branco).";
      return "";
    }
    if (tela === "entra") {
      if (!ehNS(E.diaria)) { n = paraNumero(E.diaria); if (n === null || n < 1 || n > LIMITES.diariaMax) return "Escreva a diária média do ano (R$ 1 a R$ 100 mil), ou toque em Não sei."; }
      if (!calendarioCompleto(E)) return "Marque os 12 meses do calendário: alta, médio ou fraco.";
      var ct = contagens(E);
      var tipos = [["alta", "ocupAlta", "da alta"], ["medio", "ocupMedia", "dos meses médios"], ["fraco", "ocupFraco", "dos meses fracos"]];
      for (i = 0; i < 3; i++) if (ct[tipos[i][0]] > 0 && !entreN(paraNumero(E[tipos[i][1]]), 0, 100)) return "Escreva a ocupação " + tipos[i][2] + " (0% a 100%).";
      var oc = ocupConsDe(E);
      var ob = paraNumero(E.ocupBase), oo = paraNumero(E.ocupOtim);
      if (ob === null || ob < oc - 1e-6 || ob > 100) return "A ocupação do cenário base vai da do conservador (" + fmtN(oc, 2) + "%) a 100%.";
      if (oo === null || oo < oc - 1e-6 || oo > 100) return "A ocupação do cenário otimista vai da do conservador (" + fmtN(oc, 2) + "%) a 100%.";
      n = inteiro(E.mesAbertura); if (n === null || n < 1 || n > 12) return "Escolha o mês de abertura.";
      if (!ehNS(E.estadiaMedia)) { n = paraNumero(E.estadiaMedia); if (n === null || n < 1 || n > LIMITES.estadiaMax) return "A estadia média vai de 1 a 30 noites, ou toque em Não sei."; }
      if ((E.extras || []).length > LIMITES.extrasMax) return "São até 4 outras receitas.";
      for (i = 0; i < (E.extras || []).length; i++) { var ex = erroExtra(E.extras[i]); if (ex) return ex; }
      return "";
    }
    if (tela === "real") {
      var ei = erroImposto(E, hoje); if (ei) return ei;
      n = paraNumero(E.pPlataforma); if (!entreN(n, 0, 100)) return "Escreva quantas noites você vende pela plataforma (0% a 100%).";
      if (n > 0 && !entreN(paraNumero(E.comissaoPlataforma), 0, LIMITES.comissaoMax)) return "Escreva a comissão da plataforma por reserva (0% a 50%).";
      if (!entreN(paraNumero(E.cartaoDireto), 0, LIMITES.cartaoMax)) return "Escreva a taxa do cartão nas vendas diretas (0% a 10%).";
      if (!entreN(paraNumero(E.cancelamento), 0, LIMITES.cancelMax)) return "Escreva cancelamento e não comparecimento (0% a 20% da receita de hospedagem).";
      return "";
    }
    if (tela === "noite") {
      var V = E.varLinhas || [];
      if (V.length < 1) return "Escreva pelo menos uma linha do custo de cada noite.";
      if (V.length > LIMITES.varLinhasMax) return "São até 10 linhas.";
      for (i = 0; i < V.length; i++) { var ev = erroVar(V[i]); if (ev) return ev; }
      return "";
    }
    if (tela === "mes") {
      var F = E.fixLinhas || [];
      if (F.length < 1) return "Escreva pelo menos uma linha do custo de cada mês.";
      if (F.length > LIMITES.fixLinhasMax) return "São até 15 linhas.";
      for (i = 0; i < F.length; i++) { var ef = erroFixa(F[i]); if (ef) return ef; }
      var er = erroRetirada(E); if (er) return er;
      var em = erroModelo(E); if (em) return em;
      return "";
    }
    if (tela === "reserva") {
      if (ehNS(E.reservaRep)) return "";
      n = paraNumero(E.reservaRep); if (n === null || n <= 0 || n > LIMITES.reservaMax) return "A reserva de reposição vai de mais de 0% até 20% da receita bruta, ou toque em Não sei.";
      return "";
    }
    if (tela === "caixa") {
      var C = calcular(E, hoje);
      if (!C.pronto) return "";
      var g = paraNumero(E.giro6B);
      if (g === null) return "Confirme o giro da 6B: escreva o valor ou toque em «Usar o giro mínimo».";
      if (g < C.A.giroMinimo - 0.005) return "O giro da 6B vai de " + brl(C.A.giroMinimo) + " (a maior das três contas) para cima.";
      if (g > LIMITES.dinheiroMax) return "O giro vai até R$ 100 milhões.";
      if (g > C.A.giroMinimo + 0.005 && txt(E.giroJustificativa).length < LIMITES.textoMin) return "Com o giro acima do mínimo, escreva por quê (10 letras ou mais).";
      return "";
    }
    if (tela === "vale") {
      if (!ehNS(E.taxa) && !falta(E.taxa) && !entreN(paraNumero(E.taxa), 0, LIMITES.taxaMax)) return "A taxa vai de 0% a 30% ao ano, ou toque em Não sei.";
      if (!falta(E.multiploSaida)) { n = paraNumero(E.multiploSaida); if (n === null || n < 0 || n > LIMITES.multiploMax) return "O múltiplo de saída vai de 0 a 15 vezes (ou deixe em branco)."; }
      return "";
    }
    if (tela === "veredito") {
      if (!VEREDITOS.some(function (v) { return v.v === E.vereditoPessoa; })) return "Escolha o seu veredito.";
      var cp = txt(E.criterioParar); if (cp.length < LIMITES.textoMin || cp.length > LIMITES.textoMax) return "Escreva o critério para parar (10 a 300 letras).";
      return "";
    }
    if (tela === "acao") {
      var a = txt(E.acao30); if (a.length < LIMITES.textoMin || a.length > LIMITES.textoMax) return "Escreva a ação de 30 dias (10 a 300 letras).";
      if (!prazoOk(E.prazo, hoje)) return "O prazo vai de hoje até 30 dias a partir de hoje.";
      if (txt(E.verificacao).length < LIMITES.textoMin) return "Escreva como você vai verificar (10 letras ou mais).";
      return "";
    }
    return "";
  }
  function criterio(E, C, hoje) {
    E = E || {}; hoje = hoje || E.hoje; C = C || calcular(E, hoje);
    var u = inteiro(E.unidades), capex = paraNumero(E.capex);
    var dedOk = validarTela("real", Object.assign({}, E, { imposto: BRANCO }), hoje) === "";
    var V = E.varLinhas || [], F = E.fixLinhas || [];
    var linhasOk = V.length >= 1 && F.length >= 1 && V.every(function (l) { return erroVar(l) === ""; }) && F.every(function (l) { return erroFixa(l) === ""; });
    var rr = paraNumero(E.reservaRep);
    var giroOk = C.pronto && C.A.giro6BOk;
    var p4ok = C.pronto && (C.A.p4.decidido || !P_taxaVazia(E));
    var itens = [
      { n: 1, ok: capex !== null && capex > 0 && u !== null && u >= 1, txt: "O CAPEX maior que zero e as unidades da fase." },
      { n: 2, ok: validarTela("entra", E, hoje) === "" && paraNumero(E.diaria) !== null && paraNumero(E.estadiaMedia) !== null, txt: "Diária, calendário dos 12 meses, ocupações, mês de abertura e estadia média." },
      { n: 3, ok: E.imposto === BRANCO || impostoValido(E), txt: "O imposto respondido, com quem e a data, ou marcado em branco, aguardando o contador." },
      { n: 4, ok: dedOk && E.comissaoNaoDuplicada === true && E.duodecimos === true, txt: "As deduções informadas, e confirmado que a comissão não está nos custos de cada noite e que os anuais estão divididos por 12." },
      { n: 5, ok: linhasOk, txt: "Toda linha de custo com a origem, e pelo menos uma linha fixa." },
      { n: 6, ok: erroRetirada(E) === "", txt: "A sua retirada informada, ou marcado que você não trabalha na operação." },
      { n: 7, ok: rr !== null && rr > 0 && rr <= LIMITES.reservaMax, txt: "A reserva de reposição maior que zero." },
      { n: 8, ok: giroOk, txt: "O giro da 6B igual ou maior que a maior das três contas." },
      { n: 9, ok: p4ok, txt: "O passo 4 decidido, ou a sua taxa escrita." },
      { n: 10, ok: validarTela("veredito", E, hoje) === "", txt: "O seu veredito e o critério para parar escritos." },
      { n: 11, ok: validarTela("acao", E, hoje) === "", txt: "A ação de 30 dias, com prazo de até 30 dias e como verificar." },
      { n: 12, ok: E.pdfBaixado === true, txt: "A página 6B baixada em PDF." },
    ];
    return { ok: itens.every(function (x) { return x.ok; }), antesDoPdf: itens.slice(0, 11).every(function (x) { return x.ok; }), itens: itens, faltas: itens.filter(function (x) { return !x.ok; }).map(function (x) { return x.txt; }) };
  }

  /* ------------------------------------------------------------------
     11. O que fica salvo em resumo.dados (PLANO 6.8)
     ------------------------------------------------------------------ */
  function resumoDados(E, C) {
    var r = function (x) { return ok(x) ? arred(x, 2) : null; };
    var rv = function (x) { return x === Infinity ? null : r(x); };
    var base = { unidades: inteiro(E.unidades), exemplo: E.exemplo === true, imposto_pct: impostoValido(E) ? paraNumero(E.imposto) : null, imposto_quem: impostoValido(E) ? txt(E.impostoQuem) : "", imposto_data: impostoValido(E) ? E.impostoData : "",
      veredito_pessoa: E.vereditoPessoa || null, criterio_parar: txt(E.criterioParar), taxa: P_taxaVazia(E) ? null : paraNumero(E.taxa) };
    if (!C || !C.pronto) return base;
    var A = C.A, P = C.P, cen = ["cons", "base", "otim"];
    var lista = function (k) { return cen.map(function (s) { return r(A.cen[s][k]); }); };
    var T = C.transposicao || {};
    return Object.assign(base, {
      diaria: r(P.diaria), ocup_cons: r(P.ocupCons * 100), ocup_base: r(P.ocupBase * 100), ocup_otim: r(P.ocupOtim * 100), estadia_media: r(P.estadia),
      bruta: lista("bruta"), deducoes: lista("deducoes"), real: lista("real"), variaveis: lista("variaveis"), contribuicao: lista("contrib"), fixo_ano: r(A.cons.fixoAno), retirada_mes: r(P.retirada),
      antes_reserva: lista("antes"), modelo: lista("modelo"), reserva_rep: lista("reserva"), sobra: lista("sobra"), margem_pct: cen.map(function (s) { return A.cen[s].margem === null ? null : r(A.cen[s].margem * 100); }),
      ocup_eq: A.ocupEq === null ? null : r(A.ocupEq * 100), folga_pontos: A.folga === null ? null : r(A.folga * 100), custo_por_diaria: r(A.custoPorDiaria), diaria_eq: r(A.diariaEq),
      ano1: r(A.ano1.cons), menor_acum: r(A.menorAcum), giro_6a: r(P.giro6A), giro_a: r(A.giroA), giro_b: r(A.giroB), giro_6b: r(A.giroUsado), investimento_6b: r(A.investimento),
      colchao: r(A.colchao), colchao_pct: A.colchaoPct === null ? null : r(A.colchaoPct * 100), volta_escada: cen.map(function (s) { return rv(A.volta[s]); }), volta_p6: rv(A.voltaP6.cons), volta_com_terreno: rv(A.voltaTerreno),
      retorno_simples: A.retorno === null ? null : r(A.retorno * 100), vp_sem_saida: r(A.vpSem), vp_com_saida: r(A.vpCom), passos: A.passos.map(function (p) { return p.status; }), veredito_sugerido: A.sugerido,
      margem_para_p6: T.margem === undefined ? null : T.margem, giro_meses_para_p6: T.giroMeses === undefined ? null : T.giroMeses,
    });
  }

  /* ------------------------------------------------------------------
     12. O exemplo: a Marina monta a conta dela (PLANO seção 7)
     Exemplo ilustrativo · dados fictícios. As datas andam junto com "hoje" (o "hoje" do plano é 28/11/2026).
     ------------------------------------------------------------------ */
  var ROTULO_EXEMPLO = "Exemplo ilustrativo · dados fictícios. Não são preços de referência.";
  var ROTULO_REFERENCIA = "Referência orientativa da página 6, não confirmada; a Zion também vende esse tipo de estrutura.";
  var ROTULO_CONTADOR = "Resposta fictícia do contador dela, para o caso dela; não vale para você.";
  var HOJE_EXEMPLO = "2026-11-28";
  var CALENDARIO_MARINA = ["fraco", "fraco", "fraco", "medio", "medio", "alta", "alta", "alta", "medio", "medio", "fraco", "fraco"];
  function exemplo(hoje) {
    hoje = dataOk(hoje) ? hoje : HOJE_EXEMPLO;
    var desloc = diasEntre(HOJE_EXEMPLO, hoje);
    var E = estadoInicial(hoje);
    var V = function (nome, base, valor, origem) { return novaLinhaVar({ nome: nome, base: base, valor: valor, origem: origem }); };
    var F = function (nome, valor, origem, grupo, periodo) { return novaLinhaFixa({ nome: nome, valor: valor, origem: origem, grupo: grupo, periodo: periodo || "mensal" }); };
    Object.assign(E, {
      nome: "Marina (exemplo)", projeto: "Cabanas da Marina", cidadeUF: "", situacao: "terreno", paraOutro: false, d1: "parte", d2: "sim", d3: "sim", d4: "sim",
      capex: "791.131", giro6A: "40.787,38", terreno: "600.000", unidades: "3", margem6: "40", margem6Origem: "referência da Zion (página 6)", limite6: "870.130,80", resultado6: "108.766,35", origemCapex: "6A",
      diaria: "645", diariaMedida: "645", calendario: CALENDARIO_MARINA.slice(), ocupAlta: "64", ocupMedia: "40", ocupFraco: "22", ocupBase: "50", ocupOtim: "65", ocup6: "38,5",
      mesAbertura: "6", estadiaMedia: "2", p2MesesAlta: "3", p2MesesFraco: "5", p2OcupAno: "38,5",
      extras: [novoExtra({ nome: "Cesta de café (ideia, ainda fora da conta)", captura: "60", ticket: "140", custoDireto: "70", naConta: false })],
      imposto: "6", impostoQuem: "Contador dela (resposta fictícia)", impostoData: somaDias("2026-11-20", desloc), impostoRegime: "",
      pPlataforma: "60", comissaoPlataforma: "15", cartaoDireto: "3", cancelamento: "2", comissaoNaoDuplicada: true,
      varLinhas: [V("Lavanderia terceirizada do enxoval", "porEstadia", "70", "cotacao"), V("Amenidades e boas-vindas", "porEstadia", "45", "estimativa"), V("Energia, água e gás da noite", "porNoite", "28", "estimativa"),
        V("Produtos de limpeza e reposição", "porNoite", "12", "estimativa"), V("Perdas e quebras de material", "pctReceita", "1", "estimativa")],
      fixLinhas: [F("Pessoa local: salário e encargos (a confirmar com o contador)", "3.600", "estimativa", "equipe"), F("13º e férias (duodécimo)", "600", "estimativa", "equipe"), F("Folguista nas folgas da pessoa local", "400", "estimativa", "equipe"),
        F("Energia das áreas comuns e bomba do poço", "500", "estimativa", "energia"), F("Internet e sistema de reservas", "350", "cotacao", "internet"), F("Contador", "650", "cotacao", "contabilidade"),
        F("Seguro", "3.600", "estimativa", "contabilidade", "anual"), F("Imposto do imóvel, taxas e licença anual", "1.800", "estimativa", "contabilidade", "anual"), F("Manutenção preventiva e jardinagem", "800", "estimativa", "manutencao"),
        F("Marketing, fotos e anúncios", "450", "estimativa", "marketing"), F("Tarifas bancárias e outros", "200", "estimativa", "outros")],
      duodecimos: true, horasSemana: "8", valorHora: "40", naoTrabalho: false, semModelo: true, reservaRep: "3", giro6B: "53.524,02", giroJustificativa: "", taxa: "", taxaAntes: false, multiploSaida: "", capexPorUnidade: "168.981",
      ajustado: { diaria: "716", ocup: "42", fixoPct: "", capexPct: "", extras: true },
      vereditoPessoa: "Redesenhar", criterioParar: "Se nenhum redesenho passar de 12 para 8 anos com premissas provadas, eu não assino a obra.",
      prazo: somaDias(hoje, 30), exemplo: true,
    });
    var s = acaoSugerida(E, calcular(E, hoje));
    E.acao30 = s.acao; E.verificacao = s.verificacao;
    return E;
  }

  /* ------------------------------------------------------------------
     13. Textos fixos, ajuda de cada tela e varredura de promessas proibidas
     ------------------------------------------------------------------ */
  var TEXTOS = {
    titulo: "A sua conta",
    tituloCompleto: "Faça agora · A sua conta",
    pagina: "Página 6B · Viabilidade",
    promessa: "Aprenda o passo a passo para saber se a conta do seu projeto fecha: da receita bruta ao que sobra depois da reserva de reposição, o primeiro ano mês a mês, o tempo de volta e a decisão por escrito antes de assinar a obra.",
    retomada: "Você já fez a página 6 no Pilar 6 e a 6A. Aqui a página 6 ganha mais uma irmã, a 6B, que abre a linha que faltava: quanto sobra.",
    notaP6: "A página 6 fez a primeira conta, com a margem de referência, que o próprio Pilar 6 chama de simplificação, não promessa. A 6B é o passo que o Pilar 6 pediu: «A margem real sai da sua lista de custos, com o seu trabalho e a reserva de reposição dentro.» Quando as duas diferem, é a conta aberta que decide.",
    assinatura: "«Faturamento não é lucro, e o custo fixo não diminui na baixa.» (Pilar 6)",
    lucroRetorno: "«Lucro e retorno são coisas diferentes.» (Pilar 6)",
    naoFecha: "«Quando a conta não fecha, a conta está certa.» (Jornada do COMO, Etapa 02)",
    operador: "«Se o negócio não paga quem o opera, ele não é um negócio.» (Jornada do COMO, Etapa 09)",
    linhaBranco: "«Uma linha em branco vale mais do que um número inventado.» (Pilar 6)",
    naoSei: "«Onde não souber, marque \"Não sei\": vira a sua tarefa da semana.» (Comece aqui)",
    cenarios: "Cenários, não promessas.",
    aviso: "Material educativo. Não é estudo de viabilidade, projeção nem promessa de retorno. Impostos se confirmam com o contador; contratos, com o advogado. A Zion avalia cada caso.",
    naoEnvia: "Esta ficha não envia nada: o PDF fica só com você.",
    dossie: "Salve o PDF da página 6B na pasta Meu Dossiê, ao lado das páginas 6 e 6A.",
    tempo: "A primeira versão sai em uma tarde, com a linha do imposto em branco se o contador ainda não respondeu. A resposta do contador e as cotações dos custos fixos levam o tempo deles.",
    naoPromete: "A lição não promete retorno, renda, ocupação, crédito, parceria nem aprovação.",
    exemplo: ROTULO_EXEMPLO, referencia: ROTULO_REFERENCIA, contador: ROTULO_CONTADOR,
    taxa: "A Zion não sugere taxa. A sua taxa é o quanto o seu dinheiro renderia em outro lugar, mais o que você pede pelo risco.",
    multiplo: "O múltiplo de saída é a venda do negócio no ano 10: fica ao lado da conta sem ele, nunca como valor do negócio.",
    reserva: "3% a 6% citados pelas fontes (Volume A05: 3% a 5%; Jornada do COMO: 3% a 6%; a régua da Zion usa 3%). Reserva ou depreciação, nunca as duas.",
    cancelamento: "1% a 3%, faixa citada pela fonte.",
    imposto: "Nenhuma alíquota é sugerida aqui. O imposto sobre a receita só se preenche com a resposta do seu contador, com o nome de quem respondeu e a data. Sem ela, a linha fica em branco.",
    avisoP6: AVISO_P6, avisoP2: AVISO_P2,
    ajustado: "O que precisaria ser verdade: uma combinação a provar, salva à parte. Ela nunca grava por cima da sua conta.",
    pilar7: "No Pilar 7, a Marina decide com a página 6 de referência. Com a 6B, o critério que ela mesma escreveu dispara: antes de pedir dinheiro a alguém, ela redesenha e prova preço e semana.",
    moedaConstante: "Moeda constante: sem crescimento de receita nem de custo nos dez anos. O mês tem 365 ÷ 12 noites por unidade, para os doze meses somarem o ano do Pilar 4.",
  };
  var AJUDA = {
    parte: { titulo: "De onde você parte", explica: "O CAPEX e o giro da sua 6A, as unidades da fase e o que a sua página 6 escreveu: a margem e o limite de 8 anos.", porque: "A 6B não recomeça: ela abre a linha «quanto sobra» sobre o custo de abrir a porta que você fez na 6A e sobre a primeira conta da página 6.", onde: "Nas páginas 6 e 6A do seu Dossiê, na pasta Meu Dossiê. Se você fez as fichas neste aparelho, os números já vêm preenchidos.", exemplo: "A Marina parte da 6A dela: CAPEX de R$ 791.131, giro de R$ 40.787,38, 3 cabanas, terreno dela de R$ 600.000 ao lado. Na página 6, a margem de referência de 40% deu R$ 108.766,35 por ano e o limite de cerca de R$ 870 mil." },
    entra: { titulo: "Quanto entra: a receita se mede, não se deseja", explica: "Unidades × ocupação × diária × dias. A diária é a média do ano; a ocupação sai dos doze meses do Pilar 2; o primeiro ano começa no mês de abertura, com a rampa.", porque: "«Ninguém abre na ocupação do destino.» (Pilar 6) A rampa da régua da Zion é de 40% da ocupação nos meses 1 a 3, 50% nos meses 4 a 6 e 75% nos meses 7 a 12.", onde: "Na página 2 do seu Dossiê (diária média, meses de alta e fracos e as ocupações) e na página 6 (cenários base e otimista).", exemplo: "R$ 645 de diária; alta de junho a agosto a 64%; setembro, outubro, abril e maio médios a 40%; novembro a março fracos a 22%: média de 38,5%. Abre em junho. Estadia média de 2 noites." },
    real: { titulo: "Do bruto ao real: o que sai antes de você ver o dinheiro", explica: "O imposto sobre a receita, a comissão da plataforma, a taxa do cartão nas vendas diretas e o cancelamento. A comissão, o cartão e o cancelamento incidem sobre a hospedagem.", porque: "«Imposto sobre a receita é a omissão mais frequente e a mais cara.» (Jornada do COMO, Etapa 02) Comissão por reserva não é comissão sobre a receita total: 60% das noites a 15% dá 9% da hospedagem.", onde: "O imposto, com o seu contador. A comissão, no contrato da plataforma. O cartão, na sua maquininha. O cancelamento, no seu histórico ou numa estimativa escrita.", exemplo: "Imposto de 6% (resposta fictícia do contador dela, para o caso dela; não vale para você), 60% das noites pela plataforma a 15%, cartão de 3% nas vendas diretas, cancelamento de 2%. Deduções: 18,2% da receita." },
    noite: { titulo: "O custo de cada noite", explica: "O que só existe quando há hóspede: por noite, por estadia ou em % da receita de hospedagem.", porque: "Cada noite vendida tem custo. Sem ele, a diária de equilíbrio e o piso saem errados.", onde: "Nas cotações da lavanderia, nas contas de energia e água e nas suas compras de reposição.", exemplo: "Lavanderia R$ 70 por estadia (cotação), amenidades R$ 45 por estadia, energia, água e gás R$ 28 por noite, limpeza R$ 12 por noite, perdas e quebras 1%. O que fica de cada noite: R$ 645 × 77,8% − R$ 97,50 = R$ 404,31." },
    mes: { titulo: "O custo de cada mês, com o seu trabalho dentro", explica: "O que se paga com ou sem hóspede. Os gastos anuais entram divididos por 12 (o duodécimo). O seu trabalho entra como custo: horas por semana × valor-hora × 4,33.", porque: "«Faturamento não é lucro, e o custo fixo não diminui na baixa.» (Pilar 6) «Se o negócio não paga quem o opera, ele não é um negócio.» (Jornada do COMO, Etapa 09)", onde: "Na folha da pessoa local (com o contador), nas propostas de internet, contador e seguro, e no carnê do imposto do imóvel. O valor-hora é quanto você pagaria a alguém para fazer o que você faz.", exemplo: "Onze linhas somam R$ 8.000 por mês (seguro de R$ 3.600 e taxas de R$ 1.800 no ano, divididos por 12). Retirada: 8 horas × R$ 40 × 4,33 = R$ 1.385,60. Fixo do mês: R$ 9.385,60; no ano, R$ 112.627,20. Sem aluguel, gestão nem royalty: ela opera." },
    reserva: { titulo: "A reserva de reposição", explica: "Uma porcentagem da receita bruta, separada desde o primeiro ano, para trocar o que se gasta: colchões, enxoval, deck, equipamentos.", porque: "Sem ela, o que sobra parece maior do que é, e o tempo de volta sai curto demais.", onde: "Na sua lista de itens com vida útil. Faixa citada pelas fontes: 3% a 6% da receita bruta. A ficha não preenche por você.", exemplo: "A Marina usa 3%, o número que a régua da Zion usa: R$ 8.157,48 no cenário medido. Sobram R$ 57.819,79 no ano, margem de 21,3%." },
    caixa: { titulo: "O primeiro ano e o caixa", explica: "O ano mês a mês, com a rampa no calendário, o menor saldo, o colchão e o giro pelas duas contas do Pilar 6.", porque: "«Projeto não quebra por prejuízo. Quebra por falta de caixa num mês específico.» (Volume 05 · Investimento, cap. 8)", onde: "Tudo aqui é calculado das telas anteriores. Você só confirma o giro, que nunca fica abaixo da maior das três contas.", exemplo: "Abrindo em junho, o menor saldo cai em março do primeiro ano: −R$ 22.356,81. Giro da 6B: R$ 53.524,02 (três meses de custo aberto). Colchão de R$ 31.167,21, 3,9% do CAPEX." },
    vale: { titulo: "Vale a pena? Lucro e retorno são coisas diferentes", explica: "O tempo de volta em escada sobre o que sobra, o valor presente dos próximos dez anos com a taxa que você escreve antes de ver o resultado, e a venda do negócio só ao lado.", porque: "«Lucro e retorno são coisas diferentes.» (Pilar 6) A operação pode se pagar com folga e o investimento não voltar.", onde: "A taxa é sua: quanto o seu dinheiro renderia em outro lugar, mais o que você pede pelo risco. A Zion não sugere taxa.", exemplo: "A Marina não precisou escrever a taxa: a soma simples dos dez anos (R$ 501.386,06) já é menor que o CAPEX, e o valor presente é negativo a qualquer taxa de zero para cima. Múltiplo de saída em branco." },
    alavancas: { titulo: "Quando a conta não fecha: uma alavanca por vez", explica: "Mexa em uma alavanca de cada vez e veja o que sobra, o tempo de volta e o passo 3. Nada aqui grava por cima da sua conta.", porque: "Mexer em tudo junto esconde qual premissa sustenta a conta. «Primeiro prove a conta. Depois escolha como crescer.» (Pilar 6)", onde: "Diária e ocupação, no Pilar 2; custo fixo, nas propostas; CAPEX e fase, na 6A e no masterplan do Pilar 5.", exemplo: "Diária R$ 50 maior: 11,8 anos. Ocupação 5 pontos maior: 11,0 anos. Custo fixo 10% menor: 12,6 anos. CAPEX 10% menor: 13,6 anos. Duas cabanas: mais de 100 anos, porque o custo fixo não cai junto. O ajustado (R$ 716, 42% e a cesta de café) dá Testar." },
    veredito: { titulo: "O seu veredito e o critério para parar", explica: "A régua sugere; quem decide é você. Escreva o veredito e o fato que faz você não assinar a obra.", porque: "O critério escrito antes protege a decisão da vontade de seguir em frente.", onde: "No critério que você escreveu na página 6 e no resultado desta ficha.", exemplo: "Veredito da Marina: Redesenhar. Critério: «Se nenhum redesenho passar de 12 para 8 anos com premissas provadas, eu não assino a obra.»" },
  };
  var PROIBIDAS = [/garant/i, /lucro certo/i, /sucesso/i, /vai faturar/i, /renda (certa|passiva)/i, /sem risco/i, /enriquec/i, /fique rico/i, /payback/i, /\bNOI\b/, /EBITDA/, /\bVPL\b/, /\bTIR\b/, /\bROI\b/, /\bmembro\b/i, /\baluno\b/i, /ECROI/, /\bBloco [1-7]\b/,
    /inflad/i, /otimista demais/i, /estava errad/i, /não é estresse/i];
  function textoSeguro(s) { return !PROIBIDAS.some(function (re) { return re.test(String(s)); }); }

  var api = {
    NS: NS, BRANCO: BRANCO, LIMITES: LIMITES, SITUACOES: SITUACOES, DIAG: DIAG, MESES: MESES, MESES_LONGOS: MESES_LONGOS, TIPOS_MES: TIPOS_MES, ORIGENS: ORIGENS, BASES: BASES, GRUPOS_P2: GRUPOS_P2, VEREDITOS: VEREDITOS, ALAVANCAS: ALAVANCAS,
    ORDEM_ALERTAS: ORDEM_ALERTAS, INFO: INFO, AJUDA: AJUDA, ACOES: ACOES, VERIFICACOES: VERIFICACOES, PROXIMOS: PROXIMOS, TELAS: TELAS, NOMES_TELAS: NOMES_TELAS, TEXTOS: TEXTOS, PROIBIDAS: PROIBIDAS, NOTA_FAIXA: NOTA_FAIXA,
    HOJE_EXEMPLO: HOJE_EXEMPLO, MULTIPLO_REGUA: MULTIPLO_REGUA, SEMANAS_MES: SEMANAS_MES, CALENDARIO_MARINA: CALENDARIO_MARINA,
    falta: falta, paraNumero: paraNumero, arred: arred, fmtNum: fmtNum, fmtN: fmtN, brl: brl, brl0: brl0, fmtPct: fmtPct, fmtPontos: fmtPontos, fmtVolta: fmtVolta, juntar: juntar, div: div, ehNS: ehNS,
    numTexto: numTexto, dataOk: dataOk, diasEntre: diasEntre, somaDias: somaDias, dataBR: dataBR, clone: clone,
    novaLinhaVar: novaLinhaVar, novaLinhaFixa: novaLinhaFixa, novoExtra: novoExtra, linhasVarSugeridas: linhasVarSugeridas, linhasFixasSugeridas: linhasFixasSugeridas, estadoInicial: estadoInicial,
    lerPagina6A: lerPagina6A, lerPagina6: lerPagina6, lerPagina2: lerPagina2, lerMarcoZero: lerMarcoZero, aplicarLeituras: aplicarLeituras,
    valorVar: valorVar, erroVar: erroVar, valorFixoMes: valorFixoMes, erroFixa: erroFixa, erroExtra: erroExtra, extrasSemGanho: extrasSemGanho,
    calendarioCompleto: calendarioCompleto, contagens: contagens, ocupConsDe: ocupConsDe, impostoValido: impostoValido, retiradaMes: retiradaMes, parametros: parametros, rampa: rampa, cenario: cenario,
    escada: escada, vp: vp, taxaVirada: taxaVirada, classPasso1: classPasso1, classPasso2: classPasso2, classPasso3: classPasso3, classPasso4: classPasso4, classPasso5: classPasso5, mesDoCalendario: mesDoCalendario,
    analise: analise, calcular: calcular, alavanca: alavanca, ajustado: ajustado, ajustadoDefinido: ajustadoDefinido, transposicao: transposicao, planilha2: planilha2,
    leituraMargem: leituraMargem, leituraEquilibrio: leituraEquilibrio, leituraVolta: leituraVolta, leituraCancelamento: leituraCancelamento,
    alertas: alertas, tresPrimeiros: tresPrimeiros, motivoVeredito: motivoVeredito, acaoSugerida: acaoSugerida, proximaEtapa: proximaEtapa,
    validarTela: validarTela, prazoOk: prazoOk, criterio: criterio, resumoDados: resumoDados, exemplo: exemplo, textoSeguro: textoSeguro,
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else raiz.ZVIAB = api;
})(typeof window !== "undefined" ? window : this);

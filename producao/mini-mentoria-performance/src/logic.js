/* Raio-X da Hospedagem · motor de diagnóstico, 7 calculadoras, plano de ação e dossiê (lógica pura, testada em Node).
   Regras do pacote Zion Performance 47: desconhecido NÃO é zero; "não se aplica" não pontua; pontuação do pilar =
   soma das respostas válidas ÷ (2 × quantidade de respostas válidas); cobertura sempre exibida.
   Pesos, faixas e estimativas de impacto/esforço são HIPÓTESES EDITORIAIS iniciais, a validar pela equipe. */
(function (root) {
  'use strict';
  var HIPOTESES = {
    faixas: { construir: 40, desenvolvimento: 70 },        // <40 base a construir · 40-69 em desenvolvimento · >=70 consolidado
    confianca: { baixa: 50, media: 80 },                    // cobertura <50 baixa · 50-79 média · >=80 alta
    pesoPilar: 1,                                           // todos os pilares com o mesmo peso (a validar)
    caps: { 7: 6, 30: 5, 60: 4, 90: 4 }                     // máximo de ações por horizonte; o resto vai para o backlog
  };
  var ROTULO = { '2': 'implementado e comprovado', '1': 'parcial', '0': 'ausente', unknown: 'não sei', na: 'não se aplica' };

  /* ---------- números ---------- */
  // Aceita "1.234,56", "1234,56", "1234.56", "R$ 1.234". Vazio -> null (desconhecido). Texto inválido -> NaN.
  function lerNum(v) {
    if (v === null || v === undefined) return null;
    if (typeof v === 'number') return isFinite(v) ? v : NaN;
    var s = String(v).replace(/R\$|\s|%/g, '');
    if (s === '') return null;
    if (/,/.test(s)) s = s.replace(/\./g, '').replace(',', '.');
    else if (/^-?\d{1,3}(\.\d{3})+$/.test(s)) s = s.replace(/\./g, '');
    if (!/^-?\d+(\.\d+)?$/.test(s)) return NaN;
    return parseFloat(s);
  }
  function mediana(a) {
    if (!a.length) return null; var b = a.slice().sort(function (x, y) { return x - y; }), m = Math.floor(b.length / 2);
    return b.length % 2 ? b[m] : (b[m - 1] + b[m]) / 2;
  }
  function soma(a) { return a.reduce(function (s, x) { return s + x; }, 0); }
  function r2(x) { return x === null || x === undefined ? null : Math.round(x * 100) / 100; }
  function div(a, b) { return (a === null || b === null || b === 0 || !isFinite(a) || !isFinite(b)) ? null : a / b; }
  // Lê um campo: devolve {v, erro}. v = null se vazio; erro se inválido/negativo/fora do limite
  function campo(obj, k, rot, o, avisos) {
    o = o || {}; var x = lerNum(obj ? obj[k] : null);
    if (x === null) return null;
    if (isNaN(x)) { avisos.push(rot + ': valor inválido, ignorado (não foi tratado como zero)'); return null; }
    if (x < 0 && !o.neg) { avisos.push(rot + ': valor negativo não é aceito, ignorado'); return null; }
    if (o.max !== undefined && x > o.max) { avisos.push(rot + ': acima de ' + o.max + ', ignorado'); return null; }
    return x;
  }

  /* ---------- diagnóstico ---------- */
  function normResp(v) { if (v === 0 || v === '0') return '0'; if (v === 1 || v === '1') return '1'; if (v === 2 || v === '2') return '2'; if (v === 'unknown' || v === 'na') return v; return null; }
  function pontuarPilar(m, questoes, resp) {
    var qs = questoes.filter(function (q) { return q.module === m; });
    var c = { '0': 0, '1': 0, '2': 0, unknown: 0, na: 0, pendente: 0 };
    qs.forEach(function (q) { var r = normResp(resp[q.id]); c[r === null ? 'pendente' : r]++; });
    var validos = c['0'] + c['1'] + c['2'], aplicaveis = qs.length - c.na, pontos = c['1'] + 2 * c['2'];
    var score = validos ? Math.round(pontos / (2 * validos) * 1000) / 10 : null;
    var cobertura = aplicaveis ? Math.round(validos / aplicaveis * 1000) / 10 : null;
    var nivel = score === null ? 'sem_dados' : score < HIPOTESES.faixas.construir ? 'construir' : score < HIPOTESES.faixas.desenvolvimento ? 'desenvolvimento' : 'consolidado';
    var conf = cobertura === null ? 'sem_dados' : cobertura < HIPOTESES.confianca.baixa ? 'baixa' : cobertura < HIPOTESES.confianca.media ? 'media' : 'alta';
    return { modulo: m, total: qs.length, validos: validos, naoAplica: c.na, desconhecidos: c.unknown, pendentes: c.pendente, aplicaveis: aplicaveis, pontos: pontos, score: score, cobertura: cobertura, nivel: nivel, confianca: conf };
  }
  function diagnostico(questoes, resp) {
    var mods = []; questoes.forEach(function (q) { if (mods.indexOf(q.module) < 0) mods.push(q.module); });
    var pilares = mods.map(function (m) { return pontuarPilar(m, questoes, resp || {}); });
    var vs = soma(pilares.map(function (p) { return p.validos; })), pts = soma(pilares.map(function (p) { return p.pontos; })), ap = soma(pilares.map(function (p) { return p.aplicaveis; }));
    var score = vs ? Math.round(pts / (2 * vs) * 1000) / 10 : null, cob = ap ? Math.round(vs / ap * 1000) / 10 : null;
    var forca = [], lacunas = [], coletar = [];
    questoes.forEach(function (q) {
      var r = normResp((resp || {})[q.id]);
      if (r === '2') forca.push(q.id); else if (r === '0' || r === '1') lacunas.push(q.id); else if (r === 'unknown') coletar.push(q.id);
    });
    return { pilares: pilares, geral: { score: score, cobertura: cob, validos: vs, aplicaveis: ap }, pontosFortes: forca, lacunas: lacunas, aColetar: coletar };
  }

  /* ---------- plano de ação ---------- */
  function addDias(iso, d) { var t = new Date(iso + 'T12:00:00Z'); t.setUTCDate(t.getUTCDate() + d); return t.toISOString().slice(0, 10); }
  function plano(questoes, meta, resp, opts) {
    opts = opts || {}; var inicio = opts.inicio || new Date().toISOString().slice(0, 10), edits = opts.edits || {};
    var cand = [];
    questoes.forEach(function (q) {
      var r = normResp((resp || {})[q.id]); if (r !== '0' && r !== '1' && r !== 'unknown') return;
      var mt = meta[q.id] || { impacto: 2, esforco: 2, critico: false, responsavel: '' };
      var gap = r === '0' ? 2 : 1;
      var score = Math.round(gap * mt.impacto / mt.esforco * 100) / 100;
      var coleta = r === 'unknown';
      cand.push({
        id: q.id, modulo: q.module, topico: q.topic, pergunta: q.question, status: r, statusRotulo: ROTULO[r], critico: !!mt.critico,
        tipo: coleta ? 'coletar' : 'agir',
        acao: coleta ? 'Coletar a evidência antes de decidir: ' + q.evidence + '. Como: ' + q.procedure : q.action,
        motivo: coleta ? 'Você marcou "não sei" em "' + q.question + '" (' + q.topic + '). Sem o dado não dá para avaliar este ponto, e ele não foi tratado como zero.'
          : 'Você marcou "' + ROTULO[r] + '" em "' + q.question + '" (' + q.topic + ').' + (mt.critico ? ' É um ponto de segurança, legalidade ou conformidade: procure profissional habilitado ou órgão competente.' : ''),
        responsavel: mt.responsavel, indicador: q.evidence, evidencia: q.evidence + ' — ' + q.procedure,
        impacto: mt.impacto, esforco: mt.esforco, prioridade: score
      });
    });
    cand.sort(function (a, b) {
      if (a.critico !== b.critico) return a.critico ? -1 : 1;
      if (b.prioridade !== a.prioridade) return b.prioridade - a.prioridade;
      return a.id < b.id ? -1 : a.id > b.id ? 1 : 0;
    });
    // OP3D: foco em três níveis aninhados (heurística; os percentuais orientam o foco e não são proporção comprovada)
    var N = cand.length, n1 = N ? Math.ceil(N * 0.20) : 0, n2 = N ? Math.ceil(N * 0.04) : 0, n3 = N ? Math.max(1, Math.ceil(N * 0.008)) : 0;
    cand.forEach(function (c, i) { c.op3d = i < n3 ? 3 : i < n2 ? 2 : i < n1 ? 1 : 0; });
    var cap = { 7: 0, 30: 0, 60: 0, 90: 0 }, saida = { 7: [], 30: [], 60: [], 90: [] }, backlog = [], rapido = false;
    cand.forEach(function (c) {
      var minimo;
      if (c.critico) minimo = c.status === '1' ? 30 : 7;
      else if (!rapido && c.esforco <= 2) { minimo = 7; rapido = true; }
      else minimo = 30;
      var hs = [7, 30, 60, 90].filter(function (h) { return h >= minimo; }), alvo = null;
      for (var i = 0; i < hs.length; i++) if (cap[hs[i]] < HIPOTESES.caps[hs[i]]) { alvo = hs[i]; break; }
      if (alvo === null) { backlog.push(c); return; }
      cap[alvo]++; c.horizonte = alvo; c.prazo = addDias(inicio, alvo);
      var e = edits[c.id] || {}; if (e.responsavel) c.responsavel = e.responsavel; if (e.prazo) c.prazo = e.prazo;
      saida[alvo].push(c);
    });
    return { inicio: inicio, horizontes: saida, backlog: backlog, total: N, op3d: { nivel1: n1, nivel2: n2, nivel3: n3, nota: 'Heurística de foco (20% · 4% · 0,8%): orienta onde começar e não é proporção comprovada de resultado.' } };
  }

  /* ---------- calculadoras ---------- */
  var MOTIVOS = ['Lazer em casal', 'Lazer em família', 'Viagem com amigos', 'Trabalho ou evento', 'Outro motivo', 'Não informado'];
  // C1 · Posicionamento: motivo da viagem, preço frente a comparáveis, conversão
  function c1(inp) {
    inp = inp || {}; var av = [], faltam = [];
    var q = (inp.motivos || []).map(function (x, i) { return { motivo: MOTIVOS[i] || 'Motivo ' + (i + 1), qtd: campo({ v: x }, 'v', MOTIVOS[i] || 'motivo', {}, av) }; });
    var classif = q.slice(0, 5).filter(function (x) { return x.qtd !== null; }), totClass = soma(classif.map(function (x) { return x.qtd; }));
    var ni = q[5] ? q[5].qtd : null, amostra = totClass + (ni || 0);
    var dist = totClass > 0 ? classif.map(function (x) { return { motivo: x.motivo, qtd: x.qtd, pct: r2(x.qtd / totClass * 100) }; }) : null;
    if (!dist) faltam.push('motivos das reservas');
    if (amostra > 0 && amostra !== 20) av.push('Amostra de ' + amostra + ' reservas; o roteiro pede as últimas 20.');
    var dominante = null; if (dist) { dominante = dist.slice().sort(function (a, b) { return b.qtd - a.qtd; })[0]; if (dist.filter(function (d) { return d.qtd === dominante.qtd; }).length > 1) { av.push('Empate no motivo mais frequente: escolha um segmento para testar com base em outras evidências.'); dominante = null; } }
    var meu = campo(inp, 'meuPreco', 'Seu preço total', {}, av), comp = (inp.concorrentes || []).map(function (x, i) { return campo({ v: x }, 'v', 'Concorrente ' + (i + 1), {}, av); }).filter(function (x) { return x !== null && x > 0; });
    var med = mediana(comp), indice = null;
    if (meu === null || meu <= 0) faltam.push('seu preço total'); else if (comp.length < 3) av.push('Compare ao menos 3 hospedagens equivalentes (informadas: ' + comp.length + ').'); else indice = r2(meu / med);
    var vis = campo(inp, 'visitas', 'Visitas', {}, av), res = campo(inp, 'reservas', 'Reservas', {}, av), taxa = null;
    if (vis === null || res === null) faltam.push('visitas e reservas do mesmo canal e período');
    else if (vis === 0) av.push('Visitas igual a zero: não há taxa de conversão.');
    else if (res > vis) av.push('Reservas maiores que visitas: confira o período e o canal; a taxa não foi calculada.');
    else taxa = r2(res / vis * 100);
    return { id: 'C1', distribuicao: dist, amostra: amostra, naoInformado: ni, dominante: dominante, precoMediano: med === null ? null : r2(med), indicePreco: indice, nComparaveis: comp.length, conversaoPct: taxa, avisos: av, faltam: faltam };
  }
  // C2 · Ocupação e canais
  function c2(inp) {
    inp = inp || {}; var av = [], faltam = []; var meses = [];
    for (var i = 0; i < 12; i++) {
      var m = (inp.meses || [])[i] || {}, d = campo(m, 'disponiveis', 'Mês ' + (i + 1) + ' · noites disponíveis', {}, av), v = campo(m, 'vendidas', 'Mês ' + (i + 1) + ' · noites vendidas', {}, av), rec = campo(m, 'receita', 'Mês ' + (i + 1) + ' · receita', {}, av);
      var occ = null, inval = false;
      if (d !== null && v !== null) { if (d === 0) { av.push('Mês ' + (i + 1) + ': noites disponíveis iguais a zero; ocupação não calculada.'); } else if (v > d) { inval = true; av.push('Mês ' + (i + 1) + ': noites vendidas acima das disponíveis (ocupação > 100%). Confira bloqueios e unidades; mês fora do total.'); } else occ = r2(v / d * 100); }
      meses.push({ mes: i + 1, disponiveis: d, vendidas: v, receita: rec, ocupacaoPct: occ, invalido: inval });
    }
    var ok = meses.filter(function (x) { return x.ocupacaoPct !== null; });
    var D = soma(ok.map(function (x) { return x.disponiveis; })), V = soma(ok.map(function (x) { return x.vendidas; }));
    var anual = D > 0 ? r2(V / D * 100) : null; if (anual === null) faltam.push('noites disponíveis e vendidas por mês');
    if (ok.length && ok.length < 12) av.push('Ocupação anual calculada com ' + ok.length + ' de 12 meses.');
    var baixos = ok.length >= 3 ? ok.slice().sort(function (a, b) { return a.ocupacaoPct - b.ocupacaoPct || a.mes - b.mes; }).slice(0, 3).map(function (x) { return x.mes; }) : [];
    var canais = (inp.canais || []).map(function (c, i) {
      c = c || {}; var nome = (c.nome || '').toString().trim(); var rec = campo(c, 'receita', 'Canal ' + (i + 1) + ' · receita bruta', {}, av), com = campo(c, 'comissaoPct', 'Canal ' + (i + 1) + ' · comissão (%)', { max: 100 }, av), aq = campo(c, 'custoAquisicao', 'Canal ' + (i + 1) + ' · custo de aquisição', {}, av);
      if (!nome && rec === null) return null;
      var falta = []; if (rec === null) falta.push('receita'); if (com === null) falta.push('comissão'); if (aq === null) falta.push('custo de aquisição');
      var liq = falta.length ? null : r2(rec * (1 - com / 100) - aq);
      return { nome: nome || 'Canal ' + (i + 1), receita: rec, comissaoPct: com, custoAquisicao: aq, liquida: liq, margemPct: liq !== null && rec > 0 ? r2(liq / rec * 100) : null, falta: falta };
    }).filter(Boolean);
    var tot = soma(canais.map(function (c) { return c.receita || 0; }));
    canais.forEach(function (c) { c.participacaoPct = tot > 0 && c.receita !== null ? r2(c.receita / tot * 100) : null; if (c.falta.length) av.push(c.nome + ': faltam ' + c.falta.join(', ') + '; receita líquida não calculada (não foi tratado como zero).'); });
    var jan = (inp.janela || []).map(function (x) { return lerNum(x); }).filter(function (x) { return x !== null; }), janBad = jan.filter(function (x) { return isNaN(x) || x < 0; }).length; jan = jan.filter(function (x) { return !isNaN(x) && x >= 0; });
    if (janBad) av.push('Janela de compra: ' + janBad + ' valor(es) inválido(s) ou negativo(s) ignorado(s).');
    return { id: 'C2', meses: meses, ocupacaoAnualPct: anual, mesesValidos: ok.length, mesesBaixos: baixos, canais: canais, janelaMediana: jan.length ? mediana(jan) : null, janelaN: jan.length, avisos: av, faltam: faltam };
  }
  // C3 · Diária (ADR), RevPAR e margem dos extras
  function c3(inp) {
    inp = inp || {}; var av = [], faltam = [];
    var rec = campo(inp, 'receita', 'Receita de hospedagem', {}, av), v = campo(inp, 'vendidas', 'Noites vendidas', {}, av), d = campo(inp, 'disponiveis', 'Noites disponíveis', {}, av);
    var adr = null, revpar = null, occ = null;
    if (rec === null || v === null) faltam.push('receita e noites vendidas'); else if (v === 0) av.push('Noites vendidas igual a zero: a diária realizada não existe neste período.'); else adr = r2(rec / v);
    if (rec === null || d === null) faltam.push('receita e noites disponíveis'); else if (d === 0) av.push('Noites disponíveis igual a zero.'); else revpar = r2(rec / d);
    if (v !== null && d !== null && d > 0) { if (v > d) av.push('Noites vendidas acima das disponíveis (ocupação > 100%): confira os dados. RevPAR não é confiável.'); else occ = r2(v / d * 100); }
    var extras = (inp.extras || []).map(function (e, i) {
      e = e || {}; var nome = (e.nome || '').toString().trim(), p = campo(e, 'preco', 'Extra ' + (i + 1) + ' · preço', {}, av), c = campo(e, 'custo', 'Extra ' + (i + 1) + ' · custo incremental', {}, av), q = campo(e, 'qtd', 'Extra ' + (i + 1) + ' · vendas no mês', {}, av);
      if (!nome && p === null && c === null) return null;
      var f = []; if (p === null) f.push('preço'); if (c === null) f.push('custo incremental');
      var mu = f.length ? null : r2(p - c), flag = null; if (mu !== null && mu < 0) flag = 'margem negativa'; else if (q === 0) flag = 'sem demanda no mês';
      return { nome: nome || 'Extra ' + (i + 1), preco: p, custo: c, qtd: q, margemUnit: mu, margemPct: mu !== null && p > 0 ? r2(mu / p * 100) : null, margemMes: mu !== null && q !== null ? r2(mu * q) : null, alerta: flag, falta: f };
    }).filter(Boolean);
    extras.forEach(function (e) { if (e.falta.length) av.push(e.nome + ': faltam ' + e.falta.join(' e ') + '; margem não calculada.'); });
    return { id: 'C3', adr: adr, revpar: revpar, ocupacaoPct: occ, extras: extras, avisos: av, faltam: faltam };
  }
  // C4 · Contribuição, ocupação de equilíbrio e cenários
  function c4(inp) {
    inp = inp || {}; var av = [], faltam = [];
    var d = campo(inp, 'disponiveis', 'Noites disponíveis', {}, av), v = campo(inp, 'vendidas', 'Noites vendidas', {}, av), rec = campo(inp, 'receita', 'Receita de hospedagem', {}, av);
    var fixos = (inp.fixos || []).map(function (f, i) { f = f || {}; return { nome: (f.nome || '').toString().trim() || 'Custo fixo ' + (i + 1), valor: campo(f, 'valor', 'Custo fixo ' + (i + 1), {}, av) }; }).filter(function (f) { return f.valor !== null; });
    var totFixo = fixos.length ? soma(fixos.map(function (f) { return f.valor; })) : null; if (totFixo === null) faltam.push('custos fixos do período');
    var l = campo(inp, 'limpeza', 'Limpeza por estadia', {}, av), ins = campo(inp, 'insumos', 'Insumos por estadia', {}, av), com = campo(inp, 'comissoes', 'Comissões e taxas por estadia', {}, av), ou = campo(inp, 'outrosVar', 'Outros custos por estadia', {}, av), npe = campo(inp, 'noitesPorEstadia', 'Noites por estadia', {}, av);
    var parc = [l, ins, com, ou], varEstadia = null, cvn = null;
    if (parc.some(function (x) { return x === null; })) faltam.push('custos variáveis por estadia (limpeza, insumos, comissões, outros: use 0 só se o custo realmente não existe)');
    else varEstadia = soma(parc);
    if (npe === null || npe === 0) { if (npe === 0) av.push('Noites por estadia igual a zero.'); faltam.push('noites por estadia'); } else if (varEstadia !== null) cvn = r2(varEstadia / npe);
    var adr = (rec !== null && v !== null && v > 0) ? rec / v : null; if (adr === null) faltam.push('receita e noites vendidas');
    if (v !== null && d !== null && v > d) av.push('Noites vendidas acima das disponíveis (ocupação > 100%): confira os dados.');
    var contrib = (adr !== null && cvn !== null) ? r2(adr - cvn) : null, margemPct = contrib !== null && adr > 0 ? r2(contrib / adr * 100) : null;
    var eq = null, eqMsg = null;
    if (contrib !== null && totFixo !== null && d !== null) {
      if (contrib <= 0) eqMsg = 'A contribuição por noite é zero ou negativa: cada noite vendida não cobre o próprio custo, então não existe ocupação de equilíbrio. Revise preço e custos antes de vender mais noites.';
      else if (d === 0) eqMsg = 'Sem noites disponíveis no período.';
      else { eq = r2(totFixo / (contrib * d) * 100); if (eq > 100) eqMsg = 'A ocupação de equilíbrio passa de 100%: com esses preços e custos, os custos fixos superam a capacidade. Revise preço, custos ou estrutura.'; }
    }
    var res = (contrib !== null && v !== null && totFixo !== null) ? r2(v * contrib - totFixo) : null;
    var occ = (v !== null && d !== null && d > 0 && v <= d) ? r2(v / d * 100) : null;
    // cenário adverso (hipóteses do próprio usuário)
    var qo = campo(inp, 'quedaOcupacaoPct', 'Queda de ocupação (%)', { max: 100 }, av), qp = campo(inp, 'quedaPrecoPct', 'Queda de diária (%)', { max: 100 }, av), ac = campo(inp, 'altaCustosPct', 'Alta de custos (%)', {}, av), adv = null;
    if (res !== null && qo !== null && qp !== null && ac !== null) {
      var v2 = v * (1 - qo / 100), adr2 = adr * (1 - qp / 100), cvn2 = cvn * (1 + ac / 100), fx2 = totFixo * (1 + ac / 100), c2n = adr2 - cvn2;
      adv = { vendidas: r2(v2), adr: r2(adr2), contribuicao: r2(c2n), resultado: r2(v2 * c2n - fx2), deficit: (v2 * c2n - fx2) < 0 };
    } else faltam.push('hipóteses do cenário adverso (queda de ocupação, queda de diária, alta de custos)');
    var rep = (inp.ativos || []).map(function (a, i) { a = a || {}; var c = campo(a, 'custo', 'Ativo ' + (i + 1) + ' · custo de reposição', {}, av), vu = campo(a, 'vidaAnos', 'Ativo ' + (i + 1) + ' · vida útil (anos)', {}, av); if (c === null && vu === null && !(a.nome || '').toString().trim()) return null; if (c === null || vu === null || vu === 0) { av.push('Ativo ' + (i + 1) + ': custo e vida útil (maior que zero) são necessários para a provisão.'); return { nome: (a.nome || 'Ativo ' + (i + 1)).toString(), mensal: null }; } return { nome: (a.nome || 'Ativo ' + (i + 1)).toString(), mensal: r2(c / (vu * 12)) }; }).filter(Boolean);
    var provisao = rep.length && rep.every(function (x) { return x.mensal !== null; }) ? r2(soma(rep.map(function (x) { return x.mensal; }))) : null;
    return { id: 'C4', adr: adr === null ? null : r2(adr), custoVarNoite: cvn, contribuicaoNoite: contrib, margemContribPct: margemPct, custoFixoTotal: totFixo, ocupacaoPct: occ, equilibrioPct: eq, equilibrioMsg: eqMsg, resultado: res, adverso: adv, provisaoReposicaoMensal: provisao, ativos: rep, avisos: av, faltam: faltam };
  }
  // C5 · Capacidade de trabalho, estoque mínimo e divergências de conciliação
  function c5(inp) {
    inp = inp || {}; var av = [], faltam = [];
    var h = campo(inp, 'horasDisponiveis', 'Horas disponíveis no turno', {}, av), tarefas = (inp.tarefas || []).map(function (t, i) {
      t = t || {}; var mn = campo(t, 'minutos', 'Tarefa ' + (i + 1) + ' · minutos', {}, av), q = campo(t, 'qtd', 'Tarefa ' + (i + 1) + ' · quantidade por turno', {}, av); if (mn === null && q === null && !(t.nome || '').toString().trim()) return null;
      return { nome: (t.nome || 'Tarefa ' + (i + 1)).toString(), minutos: mn, qtd: q, horas: mn !== null && q !== null ? r2(mn * q / 60) : null };
    }).filter(Boolean), incompletas = tarefas.filter(function (t) { return t.horas === null; });
    incompletas.forEach(function (t) { av.push(t.nome + ': faltam minutos ou quantidade; fora do cálculo.'); });
    var necessarias = tarefas.filter(function (t) { return t.horas !== null; }), hn = necessarias.length ? r2(soma(necessarias.map(function (t) { return t.horas; }))) : null, carga = null;
    if (h === null || hn === null) faltam.push('horas disponíveis e tarefas'); else if (h === 0) av.push('Horas disponíveis igual a zero: carga não calculada.'); else { carga = r2(hn / h * 100); if (carga > 100) av.push('Carga acima de 100%: há mais trabalho do que horas no turno. Redistribua ou reveja o padrão sem violar direitos trabalhistas.'); }
    var itens = (inp.estoque || []).map(function (e, i) {
      e = e || {}; var nome = (e.nome || '').toString().trim(), cd = campo(e, 'consumoDia', 'Item ' + (i + 1) + ' · consumo diário', {}, av), pz = campo(e, 'prazoDias', 'Item ' + (i + 1) + ' · prazo de reposição (dias)', {}, av), mg = campo(e, 'margemDias', 'Item ' + (i + 1) + ' · margem de segurança (dias)', {}, av), sd = campo(e, 'saldo', 'Item ' + (i + 1) + ' · saldo atual', {}, av);
      if (!nome && cd === null && pz === null) return null;
      var minimo = cd !== null && pz !== null ? r2(cd * pz) : null, pedido = minimo !== null && mg !== null ? r2(cd * (pz + mg)) : null, st = null;
      if (pedido === null && minimo !== null) pedido = minimo;
      if (sd !== null && pedido !== null) st = sd <= pedido ? 'repor' : 'ok';
      return { nome: nome || 'Item ' + (i + 1), estoqueMinimo: minimo, pontoPedido: pedido, saldo: sd, situacao: st };
    }).filter(Boolean);
    var dv = (inp.divergencias || []).map(function (x, i) { x = x || {}; var a = campo(x, 'pms', 'Reserva ' + (i + 1) + ' · valor no sistema', {}, av), b = campo(x, 'extrato', 'Reserva ' + (i + 1) + ' · valor no extrato', {}, av); if (a === null && b === null && !(x.ref || '').toString().trim()) return null; return { ref: (x.ref || 'Reserva ' + (i + 1)).toString(), pms: a, extrato: b, diferenca: a !== null && b !== null ? r2(a - b) : null }; }).filter(Boolean);
    var comp = dv.filter(function (x) { return x.diferenca !== null; }), divergentes = comp.filter(function (x) { return Math.abs(x.diferenca) > 0.005; });
    return { id: 'C5', horasNecessarias: hn, cargaPct: carga, tarefas: tarefas, estoque: itens, conciliacao: { comparadas: comp.length, divergentes: divergentes.length, totalAbsoluto: r2(soma(divergentes.map(function (x) { return Math.abs(x.diferenca); }))), itens: divergentes }, avisos: av, faltam: faltam };
  }
  // C6 · Custo total instalado e retorno simples da expansão
  function c6(inp) {
    inp = inp || {}; var av = [], faltam = [];
    var p = ['unidade', 'obras', 'licencas', 'mobiliario'].map(function (k, i) { return campo(inp, k, ['Unidade', 'Obras', 'Licenças e projetos', 'Mobiliário e equipamentos'][i], {}, av); });
    var cont = campo(inp, 'contingenciaPct', 'Contingência (%)', { max: 100 }, av);
    var base = p.some(function (x) { return x === null; }) ? null : soma(p); if (base === null) faltam.push('unidade, obras, licenças e mobiliário (use 0 só se o item realmente não existe)'); if (cont === null) faltam.push('contingência');
    var total = (base !== null && cont !== null) ? r2(base * (1 + cont / 100)) : null;
    var mensais = ['limpeza', 'energia', 'equipe', 'manutencao', 'outros'].map(function (k, i) { return campo(inp, k, ['Limpeza', 'Energia e água', 'Equipe', 'Manutenção', 'Outros'][i] + ' (mensal)', {}, av); });
    var cvn = campo(inp, 'custoVarNoite', 'Custo variável por noite', {}, av), mensal = mensais.some(function (x) { return x === null; }) ? null : soma(mensais); if (mensal === null) faltam.push('custos adicionais mensais (limpeza, energia, equipe, manutenção, outros)'); if (cvn === null) faltam.push('custo variável por noite');
    var un = campo(inp, 'unidades', 'Unidades novas', {}, av), adr = campo(inp, 'diaria', 'Diária média esperada', {}, av), oc = campo(inp, 'ocupacaoPct', 'Ocupação esperada (%)', { max: 100 }, av);
    if (un === null || adr === null || oc === null) faltam.push('unidades, diária e ocupação esperadas');
    function cen(ocPct, adrV) { if (un === null || adrV === null || ocPct === null || mensal === null || cvn === null || total === null) return null; var noites = un * 365 * Math.min(Math.max(ocPct, 0), 100) / 100, receita = noites * adrV, custos = mensal * 12 + noites * cvn, res = receita - custos; return { ocupacaoPct: r2(Math.min(Math.max(ocPct, 0), 100)), diaria: r2(adrV), receitaAnual: r2(receita), custosAnuais: r2(custos), resultadoAnual: r2(res), retornoPct: total > 0 ? r2(res / total * 100) : null, paybackAnos: res > 0 && total > 0 ? r2(total / res) : null, semRetorno: res <= 0 }; }
    var dOc = campo(inp, 'deltaOcPontos', 'Variação de ocupação (pontos percentuais)', { max: 100 }, av), dAd = campo(inp, 'deltaDiariaPct', 'Variação de diária (%)', { max: 100 }, av);
    var base_ = cen(oc, adr), pess = null, otim = null;
    if (dOc !== null && dAd !== null && oc !== null && adr !== null) { pess = cen(oc - dOc, adr * (1 - dAd / 100)); otim = cen(oc + dOc, adr * (1 + dAd / 100)); }
    else faltam.push('variação dos cenários (pontos de ocupação e % de diária)');
    if (base_ && base_.semRetorno) av.push('No cenário-base o resultado anual é zero ou negativo: com esses números a expansão não se paga.');
    av.push('Cenários são ilustrativos e definidos por você; projeção não é garantia de resultado.');
    return { id: 'C6', custoTotalInstalado: total, custosAdicionaisMensais: mensal, base: base_, pessimista: pess, otimista: otim, avisos: av, faltam: faltam };
  }
  // C7 · Necessidade de capital
  function c7(inp) {
    inp = inp || {}; var av = [], faltam = [];
    var inv = campo(inp, 'investimento', 'Investimento total previsto', {}, av), cont = campo(inp, 'contingenciaPct', 'Contingência (%)', { max: 100 }, av), giro = campo(inp, 'capitalGiro', 'Capital de giro', {}, av), prop = campo(inp, 'recursosProprios', 'Recursos próprios disponíveis', {}, av);
    if (inv === null) faltam.push('investimento total'); if (cont === null) faltam.push('contingência'); if (giro === null) faltam.push('capital de giro'); if (prop === null) faltam.push('recursos próprios disponíveis');
    var total = (inv !== null && cont !== null && giro !== null) ? r2(inv * (1 + cont / 100) + giro) : null, nec = (total !== null && prop !== null) ? r2(total - prop) : null, cob = (total !== null && total > 0 && prop !== null) ? r2(prop / total * 100) : null;
    if (nec !== null && nec <= 0) av.push('Seus recursos próprios cobrem o total previsto: não há necessidade de capital externo com estes números.');
    av.push('Esta conta não atribui valor ao empreendimento nem sugere formato de parceria: isso depende de avaliação e de revisão jurídica independente.');
    return { id: 'C7', totalComContingencia: total, necessidadeCapital: nec, coberturaPropriaPct: cob, avisos: av, faltam: faltam };
  }
  var CALCS = { C1: c1, C2: c2, C3: c3, C4: c4, C5: c5, C6: c6, C7: c7 };
  var CALC_NOMES = { C1: 'Calculadora de Posicionamento', C2: 'Calculadora de Ocupação e Canais', C3: 'Calculadora de Diária e RevPAR', C4: 'Calculadora de Contribuição e Equilíbrio', C5: 'Calculadora de Capacidade e Estoque', C6: 'Calculadora de Custo e Retorno da Expansão', C7: 'Calculadora de Necessidade de Capital' };
  function calcular(id, inp) { return CALCS[id](inp); }

  /* ---------- dossiê ---------- */
  function montarDossie(perfil, questoes, meta, opts) {
    perfil = perfil || {}; opts = opts || {};
    var resp = perfil.respostas || {}, dx = diagnostico(questoes, resp), pl = plano(questoes, meta, resp, { inicio: opts.inicio, edits: perfil.edicoesPlano });
    var calcs = {}; Object.keys(CALCS).forEach(function (k) { var i = (perfil.calculadoras || {})[k]; if (i && Object.keys(i).length) calcs[k] = calcular(k, i); });
    var limitacoes = ['Diagnóstico orientativo, baseado apenas nos dados que você declarou. Não é auditoria, parecer jurídico, contábil, sanitário ou de engenharia.',
      'Pesos, faixas de nota e estimativas de impacto e esforço são hipóteses iniciais da Zion, ainda em validação pela equipe.',
      'Respostas "não sei" não foram tratadas como zero: reduzem a cobertura e viram ações de coleta.',
      'Cenários e projeções são ilustrativos e definidos por você; não são garantia de reservas, ocupação, renda, investimento ou valorização.'];
    var baixa = dx.pilares.filter(function (p) { return p.confianca === 'baixa'; }).map(function (p) { return p.modulo; });
    if (baixa.length) limitacoes.push('Pilares com cobertura baixa (menos de 50% das perguntas aplicáveis respondidas com dados): ' + baixa.join(', ') + '. A pontuação deles é provisória.');
    var avisosDados = []; Object.keys(calcs).forEach(function (k) { calcs[k].avisos.forEach(function (a) { if (!/^Cenários são ilustrativos|^Esta conta não atribui/.test(a)) avisosDados.push(CALC_NOMES[k] + ': ' + a); }); });
    var id = perfil.identificacao || {};
    return {
      identificacao: { nome: id.nome || '', tipo: id.tipo || '', municipio: id.municipio || '', estagio: id.estagio || '', objetivo: id.objetivo || '', unidades: id.unidades || '', periodo: id.periodo || '', fonte: id.fonte || '' },
      geradoEm: opts.inicio || new Date().toISOString().slice(0, 10), diagnostico: dx, plano: pl, calculos: calcs, alertasDeDados: avisosDados, limitacoes: limitacoes,
      convite: { consentimento: !!perfil.consentimento, texto: 'Convite opcional: se você autorizar, poderá enviar este dossiê à Zion para avaliação de possíveis soluções e parcerias. Não há garantia de investimento ou de parceria, e nada é enviado automaticamente.' },
      recomendacoesEducacionais: pl.horizontes
    };
  }

  var API = { HIPOTESES: HIPOTESES, ROTULO: ROTULO, MOTIVOS: MOTIVOS, CALC_NOMES: CALC_NOMES, lerNum: lerNum, mediana: mediana, pontuarPilar: pontuarPilar, diagnostico: diagnostico, plano: plano, calcular: calcular, c1: c1, c2: c2, c3: c3, c4: c4, c5: c5, c6: c6, c7: c7, montarDossie: montarDossie, addDias: addDias };
  if (typeof module !== 'undefined' && module.exports) module.exports = API; else root.RX = API;
})(typeof window !== 'undefined' ? window : this);

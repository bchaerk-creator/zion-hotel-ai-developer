// Lógica pura do Produto 01 · Você tem terra. Falta capital? (valores sempre ilustrativos)
(function (root) {
  const n = (x) => { x = Number(x); return Number.isFinite(x) && x > 0 ? x : 0; };
  const pct = (x) => Math.min(100, n(x));
  const r2 = (x) => Math.round((x + Number.EPSILON) * 100) / 100;

  // 1. Patrimônio não é caixa
  function patrimonio({ valorTerra, dividas, caixa }) {
    const v = n(valorTerra), d = n(dividas), c = n(caixa);
    return { valorEstimado: v, liquido: Math.max(0, v - d), caixaDisponivel: c, dividas: d, totalNaoEhCaixa: v + c, aviso: 'Valor do imóvel não é dinheiro disponível.' };
  }

  // 2. Lacuna de capital (sem contar valorização futura)
  function lacuna({ investimento, reserva, proprios }) {
    const necessario = n(investimento) + n(reserva), p = n(proprios);
    const l = Math.max(0, necessario - p);
    return { necessario, proprios: p, lacuna: l, sobra: Math.max(0, p - necessario), coberturaPropria: necessario ? Math.min(1, p / necessario) : 0 };
  }

  // CAPEX e capital de giro
  function capex(itens) { return r2(Object.values(itens || {}).reduce((s, v) => s + n(v), 0)); }
  function reservaGiro({ despesaMensal, meses }) { return r2(n(despesaMensal) * n(meses)); }

  // 3. Operação mensal
  function operacao({ unidades, noites, ocupacao, diaria, varPct, fixos }) {
    const disp = n(unidades) * n(noites);
    const vendidas = disp * pct(ocupacao) / 100;
    const receita = vendidas * n(diaria);
    const variaveis = receita * pct(varPct) / 100;
    const margem = receita - variaveis;
    const caixaAntesDivida = margem - n(fixos);
    const margemNoite = vendidas ? margem / vendidas : n(diaria) * (1 - pct(varPct) / 100);
    const equilibrioNoites = margemNoite > 0 ? n(fixos) / margemNoite : Infinity;
    return { noitesDisponiveis: disp, noitesVendidas: vendidas, receita: r2(receita), variaveis: r2(variaveis), margem: r2(margem), caixaAntesDivida: r2(caixaAntesDivida), margemPorNoite: r2(margemNoite), equilibrioNoites: Number.isFinite(equilibrioNoites) ? r2(equilibrioNoites) : null, equilibrioOcupacao: disp && Number.isFinite(equilibrioNoites) ? r2(equilibrioNoites / disp * 100) : null, revPAN: r2(n(diaria) * pct(ocupacao) / 100) };
  }

  // 4. Dívida: Price e SAC (juros efetivos mensais; sem tarifas, seguros ou indexação)
  function price({ principal, taxaMensalPct, meses }) {
    const P = n(principal), t = Math.max(1, Math.round(n(meses))), i = n(taxaMensalPct) / 100;
    const pmt = i ? P * i / (1 - Math.pow(1 + i, -t)) : P / t;
    return { parcela: r2(pmt), total: r2(pmt * t), jurosTotais: r2(pmt * t - P), meses: t };
  }
  function sac({ principal, taxaMensalPct, meses }) {
    const P = n(principal), t = Math.max(1, Math.round(n(meses))), i = n(taxaMensalPct) / 100, am = P / t;
    let saldo = P, total = 0, primeira = 0, ultima = 0;
    for (let k = 1; k <= t; k++) { const j = saldo * i, pm = am + j; if (k === 1) primeira = pm; if (k === t) ultima = pm; total += pm; saldo -= am; }
    return { primeiraParcela: r2(primeira), ultimaParcela: r2(ultima), total: r2(total), jurosTotais: r2(total - P), meses: t };
  }
  function cobertura(caixa, parcela) {
    const p = n(parcela);
    if (!p) return { indice: null, nivel: 'sem dívida' };
    const idx = Number(caixa) / p; // pode ser negativo
    return { indice: r2(idx), nivel: idx < 1 ? 'insuficiente' : idx < 1.3 ? 'apertada' : 'folgada' };
  }
  function cenarioDivida(o) {
    const op = operacao(o), pr = price(o), cv = cobertura(op.caixaAntesDivida, pr.parcela);
    return { ...op, parcela: pr.parcela, totalParcelas: pr.total, caixaAposParcela: r2(op.caixaAntesDivida - pr.parcela), cobertura: cv };
  }
  // cenário adverso: ocupação e diária caem, obra sobe, atraso em meses sem receita
  function adverso(base, { quedaDiariaPct, quedaOcupacaoPontos, altaObraPct, atrasoMeses }) {
    const op = { ...base, diaria: n(base.diaria) * (1 - pct(quedaDiariaPct) / 100), ocupacao: Math.max(0, n(base.ocupacao) - n(quedaOcupacaoPontos)) };
    const invAdv = n(base.investimento) * (1 + n(altaObraPct) / 100);
    const res = operacao(op);
    const giroExtra = n(atrasoMeses) * n(base.fixos);
    return { ...res, investimentoAdverso: r2(invAdv), capitalExtra: r2(invAdv - n(base.investimento) + giroExtra) };
  }

  // 5. Parceria: simulador de proporções (ponto de negociação, não divisão definitiva)
  function parceria({ valorTerra, aporte }) {
    const t = n(valorTerra), a = n(aporte), tot = t + a;
    return { total: tot, partTerra: tot ? r2(t / tot * 100) : 0, partAporte: tot ? r2(a / tot * 100) : 0, aviso: 'Proporção de referência para conversa; a divisão real depende de contrato, controle, prazo e saída.' };
  }
  function arrendamento({ aluguelMensal, meses, reajustePctAno }) {
    const m = Math.round(n(meses)), a = n(aluguelMensal), g = n(reajustePctAno) / 100; let tot = 0;
    for (let k = 0; k < m; k++) tot += a * Math.pow(1 + g, Math.floor(k / 12));
    return { totalContrato: r2(tot), mediaMensal: m ? r2(tot / m) : 0 };
  }

  // 6. Checklist
  function progresso(marcados, total) { const t = Math.max(1, total); const m = Math.min(marcados, t); return { marcados: m, total: t, pct: Math.round(m / t * 100) }; }

  // 7. Pareto progressivo 20% / 4% / 0,8% (heurística de priorização, não promessa)
  // Priorização por impacto(1-5), urgência(1-5), dependência (0/1: destrava outras)
  function priorizar(acoes) {
    const clamp = (x) => Math.min(5, Math.max(1, Math.round(n(x)) || 1));
    const lista = acoes.map(a => ({ ...a, score: clamp(a.impacto) * 3 + clamp(a.urgencia) * 2 + (a.destrava ? 5 : 0) }));
    lista.sort((x, y) => y.score - x.score || String(x.nome).localeCompare(String(y.nome)));
    const N = lista.length;
    const f = (p) => Math.max(1, Math.ceil(N * p));
    return { ordenadas: lista, faixa20: lista.slice(0, N ? f(0.2) : 0), faixa4: lista.slice(0, N ? Math.min(f(0.04), f(0.2)) : 0), critica: lista[0] || null };
  }

  // Dossiê: seções com status pronto/parcial/pendente
  function statusDossie(secoes) {
    const peso = { pronto: 1, parcial: 0.5, pendente: 0 };
    const t = secoes.length || 1;
    const s = secoes.reduce((a, x) => a + (peso[x.status] ?? 0), 0);
    return { pct: Math.round(s / t * 100), pendentes: secoes.filter(x => x.status !== 'pronto').map(x => x.nome) };
  }

  // Decisão sugerida (apoio, nunca laudo)
  function decisao({ lacunaValor, coberturaIdx, itensCheck, itensTotal, adversoCapitalExtra, proprios }) {
    const motivos = [];
    const cl = itensTotal ? itensCheck / itensTotal : 0;
    if (cl < 0.7) motivos.push('Checklist abaixo de 70%: faltam evidências.');
    if (coberturaIdx !== null && coberturaIdx !== undefined && coberturaIdx < 1) motivos.push('Cobertura da dívida abaixo de 1 no cenário.');
    if (n(adversoCapitalExtra) > n(proprios)) motivos.push('Capital extra do cenário adverso maior que seus recursos próprios.');
    if (motivos.length === 0) return { rotulo: 'avançar com cautela', motivos: ['Evidências mínimas atingidas; confirme com profissionais.'] };
    return { rotulo: cl < 0.4 ? 'interromper e reorganizar' : 'investigar mais', motivos };
  }

  // Economia comercial (ilustrativa): taxa e imposto são premissas do usuário, nada de mercado
  function economia({ preco, provisaoPct, fixosMensais, compradoresMes, cpl, reembolsoPct }) {
    const liq = n(preco) * (1 - pct(provisaoPct) / 100);
    const cpaMax = compradoresMes ? liq - n(fixosMensais) / n(compradoresMes) : liq;
    const convNecessaria = cpaMax > 0 ? n(cpl) / cpaMax : null; // lead→compra necessária
    const liqReemb = liq * (1 - pct(reembolsoPct) / 100);
    return { liquidoPorVenda: r2(liq), liquidoAposReembolsoEsperado: r2(liqReemb), cpaMaximo: r2(cpaMax), conversaoLeadCompraNecessariaPct: convNecessaria === null ? null : r2(convNecessaria * 100), cplNaoEhCpa: true };
  }

  const api = { patrimonio, lacuna, capex, reservaGiro, operacao, price, sac, cobertura, cenarioDivida, adverso, parceria, arrendamento, progresso, priorizar, statusDossie, decisao, economia };
  if (typeof module !== 'undefined') module.exports = api; else root.ZL = api;
})(typeof window !== 'undefined' ? window : globalThis);

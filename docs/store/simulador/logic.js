/* Simulador de investimento · Zion Glamping Store · lógica pura (sem DOM) */
(function (root) {
  'use strict';

  /** Converte texto em número no padrão brasileiro ("1.550", "1.550,50", "65"). Inválido vira 0. */
  function parseBR(v) {
    if (typeof v === 'number') return isFinite(v) ? v : 0;
    var s = String(v == null ? '' : v).trim().replace(/R\$|\s|%/g, '');
    if (!s) return 0;
    if (s.indexOf(',') >= 0) s = s.replace(/\./g, '').replace(',', '.');
    else if (/^\d{1,3}(\.\d{3})+$/.test(s)) s = s.replace(/\./g, '');
    var n = parseFloat(s);
    return isFinite(n) && n >= 0 ? n : 0;
  }

  /**
   * p = { diaria (R$), ocupacao (0..1), margem (0..1, EBITDA sobre a receita),
   *       unidades (inteiro >= 1), itens: [R$ por unidade], contingencia (0..1) }
   * Sem impostos sobre o lucro, depreciação, financiamento nem curva de ocupação.
   */
  function simular(p) {
    var diaria = Math.max(0, p.diaria || 0);
    var ocup = Math.min(1, Math.max(0, p.ocupacao || 0));
    var margem = Math.min(1, Math.max(0, p.margem || 0));
    var un = Math.max(1, Math.floor(p.unidades || 1));
    var cont = Math.max(0, p.contingencia || 0);
    var base = (p.itens || []).reduce(function (a, b) { return a + Math.max(0, b || 0); }, 0);

    var noites = 365 * ocup * un;
    var receita = noites * diaria;
    var ebitda = receita * margem;
    var capexUn = base * (1 + cont);
    var capex = capexUn * un;
    return {
      noitesVendidas: noites,
      receitaAno: receita,
      ebitdaAno: ebitda,
      ebitdaMes: ebitda / 12,
      capexUnidadeBase: base,
      capexUnidade: capexUn,
      capexTotal: capex,
      rentabilidade: capex > 0 ? ebitda / capex : null, // ao ano
      payback: capex > 0 && ebitda > 0 ? capex / ebitda : null // em anos
    };
  }

  /** Tabela de sensibilidade: linhas = ocupações, colunas = diárias. Devolve rentabilidade anual. */
  function sensibilidade(p, diarias, ocupacoes) {
    return ocupacoes.map(function (o) {
      return diarias.map(function (d) {
        var q = {}; for (var k in p) q[k] = p[k];
        q.diaria = d; q.ocupacao = o;
        return simular(q).rentabilidade;
      });
    });
  }

  var api = { parseBR: parseBR, simular: simular, sensibilidade: sensibilidade };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.ZionSim = api;
})(typeof window !== 'undefined' ? window : this);

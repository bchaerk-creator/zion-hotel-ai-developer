// Tabela de economia unitária. Premissas do ZIP/Bruno; provisão de taxas e imposto é ILUSTRATIVA (15%), confirme com o extrato real.
const L = require('../src/logic.js');
const base = { provisaoPct: 15, fixosMensais: 1500, cpl: 7, reembolsoPct: 0 };
const linhas = [];
for (const preco of [47, 67]) for (const comp of [30, 75, 150, 300]) {
  const e = L.economia({ preco, compradoresMes: comp, ...base });
  linhas.push(`| R$ ${preco} | ${comp} | R$ ${e.liquidoPorVenda.toFixed(2)} | R$ ${e.cpaMaximo.toFixed(2)} | ${e.conversaoLeadCompraNecessariaPct === null ? 'inviável' : e.conversaoLeadCompraNecessariaPct.toFixed(1) + '%'} |`);
}
console.log('| Preço | Compradores/mês | Líquido/venda | CPA máximo | Conversão lead→compra necessária (CPL R$ 7) |\n|---|---|---|---|---|\n' + linhas.join('\n'));

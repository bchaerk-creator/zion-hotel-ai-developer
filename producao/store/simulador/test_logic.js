// Testes da lógica do simulador contra contas independentes (feitas de outro jeito).
const assert = require('assert');
const { parseBR, simular, sensibilidade } = require('../../../docs/store/simulador/logic.js');
const near = (a, b, m) => assert.ok(Math.abs(a - b) < 1e-6, `${m}: ${a} != ${b}`);
let n = 0; const t = (nome, f) => { f(); n++; console.log('ok  ' + nome); };

t('parseBR', () => {
  assert.strictEqual(parseBR('1.550'), 1550);
  assert.strictEqual(parseBR('1.550,50'), 1550.5);
  assert.strictEqual(parseBR('R$ 80.000'), 80000);
  assert.strictEqual(parseBR('65'), 65);
  assert.strictEqual(parseBR('12,5'), 12.5);
  assert.strictEqual(parseBR(''), 0);
  assert.strictEqual(parseBR('abc'), 0);
  assert.strictEqual(parseBR('-5'), 0);
});

// Premissas de Bruno (14/11): diária 1.550, 65% de ocupação, 40% de EBITDA, bolha R$ 80 mil.
// Itens além da bolha: os valores orientativos já publicados na Store (12.500 + 10.000 + 8.500 + 25.915 + 3.931).
const base = { diaria: 1550, ocupacao: 0.65, margem: 0.40, unidades: 1,
  itens: [80000, 12500, 10000, 8500, 25915, 3931], contingencia: 0 };

t('receita pela conta de noites', () => {
  const r = simular(base);
  const noites = 365 * 0.65;                 // 237,25 noites
  near(r.noitesVendidas, noites, 'noites');
  near(r.receitaAno, noites * 1550, 'receita'); // 367.737,50
  near(r.receitaAno, 367737.5, 'receita literal');
});
t('EBITDA = 40% da receita', () => {
  const r = simular(base);
  near(r.ebitdaAno, 147095.0, 'ebitda');
  near(r.ebitdaMes, 147095.0 / 12, 'ebitda mês');
});
t('capex e rentabilidade', () => {
  const r = simular(base);
  near(r.capexUnidade, 140846, 'capex'); // 80.000 + 60.846
  near(r.capexTotal, 140846, 'capex total');
  near(r.rentabilidade, 147095 / 140846, 'rentabilidade'); // ~104,4% ao ano
  near(r.payback, 140846 / 147095, 'payback');             // ~0,96 ano
});
t('contingência de 10% aumenta o capex e reduz o retorno', () => {
  const r = simular({ ...base, contingencia: 0.10 });
  near(r.capexUnidade, 140846 * 1.1, 'capex');
  near(r.rentabilidade, 147095 / (140846 * 1.1), 'rent');
});
t('2 unidades: receita, EBITDA e capex dobram; rentabilidade igual', () => {
  const a = simular(base), b = simular({ ...base, unidades: 2 });
  near(b.receitaAno, 2 * a.receitaAno, 'receita');
  near(b.capexTotal, 2 * a.capexTotal, 'capex');
  near(b.rentabilidade, a.rentabilidade, 'rent');
});
t('capex zero não divide por zero', () => {
  const r = simular({ ...base, itens: [] });
  assert.strictEqual(r.rentabilidade, null);
  assert.strictEqual(r.payback, null);
});
t('ocupação e margem ficam entre 0 e 100%', () => {
  const r = simular({ ...base, ocupacao: 1.5, margem: 2 });
  near(r.noitesVendidas, 365, 'noites'); near(r.ebitdaAno, 365 * 1550, 'ebitda');
});
t('EBITDA zero: sem payback', () => {
  const r = simular({ ...base, margem: 0 });
  assert.strictEqual(r.payback, null); near(r.rentabilidade, 0, 'rent');
});
t('sensibilidade bate com a simulação célula a célula', () => {
  const diarias = [1240, 1395, 1550, 1705], ocup = [0.45, 0.55, 0.65, 0.75];
  const m = sensibilidade(base, diarias, ocup);
  ocup.forEach((o, i) => diarias.forEach((d, j) =>
    near(m[i][j], (d * 365 * o * 0.4) / 140846, `cel ${i},${j}`)));
});
console.log(`\n${n} testes passaram`);

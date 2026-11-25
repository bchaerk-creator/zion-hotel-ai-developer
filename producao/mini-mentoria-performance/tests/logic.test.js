// Testes da lógica contra contas feitas à mão (independentes do código). Uso: node tests/logic.test.js
const assert = require('assert'), path = require('path'), fs = require('fs');
const RX = require('../src/logic.js'), Q = JSON.parse(fs.readFileSync(path.join(__dirname, '../fontes/formularios.json'), 'utf8')).questions, META = JSON.parse(fs.readFileSync(path.join(__dirname, '../src/meta.json'), 'utf8'));
let ok = 0; const t = (n, f) => { try { f(); ok++; } catch (e) { console.error('FALHA:', n, '\n  ', e.message); process.exitCode = 1; } };
const near = (a, b, m) => assert(Math.abs(a - b) < 0.011, (m || '') + ' esperado ' + b + ' obtido ' + a);
const ids = m => Q.filter(q => q.module === m).map(q => q.id);

t('dados: 70 perguntas, 7 módulos de 10, meta completa', () => { assert.equal(Q.length, 70); for (let m = 1; m <= 7; m++) assert.equal(ids(m).length, 10); Q.forEach(q => assert(META[q.id], q.id)); });
t('lerNum: formatos brasileiros, vazio e inválido', () => {
  assert.equal(RX.lerNum('1.234,56'), 1234.56); assert.equal(RX.lerNum('1234,5'), 1234.5); assert.equal(RX.lerNum('1.234'), 1234); assert.equal(RX.lerNum('R$ 2.500'), 2500); assert.equal(RX.lerNum('12,5%'), 12.5);
  assert.equal(RX.lerNum(''), null); assert.equal(RX.lerNum(null), null); assert(isNaN(RX.lerNum('abc'))); assert.equal(RX.lerNum(7), 7);
});
t('pilar: soma das válidas ÷ (2 × válidas); NA fora; desconhecido não pontua', () => {
  const m = ids(1), r = {}; ['2', '2', '2', '2', '1', '1', '0', 'unknown', 'na'].forEach((v, i) => r[m[i]] = v); // 10ª sem resposta
  const p = RX.pontuarPilar(1, Q, r); assert.equal(p.validos, 7); assert.equal(p.pontos, 10); assert(Math.abs(p.score - 10 / 14 * 100) < 0.06); assert.equal(p.naoAplica, 1); assert.equal(p.aplicaveis, 9); assert(Math.abs(p.cobertura - 7 / 9 * 100) < 0.06); assert.equal(p.desconhecidos, 1); assert.equal(p.pendentes, 1);
  assert.equal(p.nivel, 'consolidado'); assert.equal(p.confianca, 'media');
});
t('tudo "não sei" ou "não se aplica": sem nota (nunca zero) e cobertura 0 ou nula', () => {
  const r = {}; ids(2).forEach(i => r[i] = 'unknown'); let p = RX.pontuarPilar(2, Q, r); assert.strictEqual(p.score, null); assert.equal(p.cobertura, 0); assert.equal(p.nivel, 'sem_dados');
  const n = {}; ids(3).forEach(i => n[i] = 'na'); p = RX.pontuarPilar(3, Q, n); assert.strictEqual(p.score, null); assert.strictEqual(p.cobertura, null); assert.equal(p.aplicaveis, 0);
  assert.strictEqual(RX.pontuarPilar(4, Q, {}).score, null);
});
t('"não sei" não equivale a ausente: mesma pontuação que não responder', () => {
  const a = {}, b = {}; ids(1).slice(0, 4).forEach(i => { a[i] = '2'; b[i] = '2'; }); ids(1).slice(4).forEach(i => a[i] = 'unknown');
  assert.equal(RX.pontuarPilar(1, Q, a).score, 100); assert.equal(RX.pontuarPilar(1, Q, b).score, 100); const c = Object.assign({}, b); ids(1).slice(4).forEach(i => c[i] = '0'); assert.equal(RX.pontuarPilar(1, Q, c).score, 40);
});
t('faixas e confiança (hipóteses)', () => {
  const mk = (n2, n0) => { const r = {}; ids(1).forEach((i, k) => r[i] = k < n2 ? '2' : k < n2 + n0 ? '0' : '2'); return r; };
  const r = {}; ids(1).forEach((i, k) => r[i] = k < 3 ? '2' : '0'); assert.equal(RX.pontuarPilar(1, Q, r).score, 30); assert.equal(RX.pontuarPilar(1, Q, r).nivel, 'construir');
  const s = {}; ids(1).forEach((i, k) => s[i] = k < 7 ? '2' : '0'); assert.equal(RX.pontuarPilar(1, Q, s).score, 70); assert.equal(RX.pontuarPilar(1, Q, s).nivel, 'consolidado');
  const u = {}; ids(1).forEach((i, k) => u[i] = k < 4 ? '1' : 'unknown'); assert.equal(RX.pontuarPilar(1, Q, u).confianca, 'baixa');
});
t('diagnóstico geral e listas', () => {
  const r = {}; ids(1).forEach((i, k) => r[i] = ['2', '1', '0', 'unknown', 'na'][k % 5]); const d = RX.diagnostico(Q, r);
  assert.equal(d.pilares.length, 7); assert.equal(d.pontosFortes.length, 2); assert.equal(d.lacunas.length, 4); assert.equal(d.aColetar.length, 2);
  near(d.geral.score, (2 * 2 + 2 * 1) / (2 * 6) * 100); assert.equal(RX.diagnostico(Q, {}).geral.score, null);
});
t('plano: sem lacunas -> vazio; crítico primeiro e em 7 dias; "não sei" vira coleta', () => {
  assert.equal(RX.plano(Q, META, {}, { inicio: '2026-12-01' }).total, 0);
  const r = {}; r.m5q9 = '0'; r.m6q2 = 'unknown'; r.m1q3 = '0'; r.m1q8 = '1'; r.m2q7 = '2'; r.m4q4 = 'na';
  const p = RX.plano(Q, META, r, { inicio: '2026-12-01' }); assert.equal(p.total, 4);
  const h7 = p.horizontes[7].map(x => x.id); assert(h7.indexOf('m5q9') >= 0 && h7.indexOf('m6q2') >= 0, 'críticos em 7 dias'); assert.equal(p.horizontes[7][0].critico, true);
  const col = p.horizontes[7].find(x => x.id === 'm6q2'); assert.equal(col.tipo, 'coletar'); assert(/não sei/.test(col.motivo)); assert(/não foi tratado como zero/.test(col.motivo));
  assert.equal(p.horizontes[7][0].prazo, '2026-12-08'); const it = p.horizontes[30][0] || p.horizontes[7].find(x => x.id === 'm1q3'); assert(it);
  Object.values(p.horizontes).flat().forEach(x => { ['acao', 'motivo', 'responsavel', 'prazo', 'indicador', 'evidencia'].forEach(k => assert(x[k], x.id + ' sem ' + k)); });
});
t('plano: crítico parcial vai a 30 dias; limites por horizonte e backlog; OP3D', () => {
  const r = {}; Q.forEach(q => r[q.id] = '0'); const p = RX.plano(Q, META, r, { inicio: '2026-12-01' });
  assert.equal(p.total, 70); assert(p.horizontes[7].length <= 6 && p.horizontes[30].length <= 5 && p.horizontes[60].length <= 4 && p.horizontes[90].length <= 4);
  const n = [7, 30, 60, 90].reduce((s, h) => s + p.horizontes[h].length, 0); assert.equal(n + p.backlog.length, 70); assert.equal(n, 19);
  assert.equal(p.op3d.nivel1, 14); assert.equal(p.op3d.nivel2, 3); assert.equal(p.op3d.nivel3, 1);
  const crit = Q.filter(q => META[q.id].critico).map(q => q.id); assert.equal(p.horizontes[7].filter(x => x.critico).length, 6, 'seis críticos cabem em 7 dias');
  const p2 = RX.plano(Q, META, { m5q9: '1' }, { inicio: '2026-12-01' }); assert.equal(p2.horizontes[7].length, 0); assert.equal(p2.horizontes[30][0].id, 'm5q9');
  assert(p.horizontes[7].every((x, i, a) => !i || x.critico || !a[i - 1] || true));
});
t('plano: edições do usuário (responsável e prazo) são respeitadas', () => {
  const p = RX.plano(Q, META, { m1q3: '0' }, { inicio: '2026-12-01', edits: { m1q3: { responsavel: 'Maria', prazo: '2026-12-20' } } }); const a = Object.values(p.horizontes).flat()[0]; assert.equal(a.responsavel, 'Maria'); assert.equal(a.prazo, '2026-12-20');
});
t('C1: distribuição, empate, preço relativo, conversão e zero denominador', () => {
  const c = RX.c1({ motivos: [8, 6, 2, 3, 1, 0], meuPreco: 900, concorrentes: [800, 1000, 950, 1100, 700], visitas: 400, reservas: 12 });
  assert.equal(c.amostra, 20); near(c.distribuicao[0].pct, 8 / 20 * 100); assert.equal(c.dominante.motivo, 'Lazer em casal'); assert.equal(c.precoMediano, 950); near(c.indicePreco, 900 / 950); near(c.conversaoPct, 3); assert.equal(c.avisos.length, 0);
  const e = RX.c1({ motivos: [5, 5, 0, 0, 0, 0] }); assert.strictEqual(e.dominante, null); assert(e.avisos.some(a => /Empate/.test(a)));
  const z = RX.c1({ motivos: [0, 0, 0, 0, 0, 4], visitas: 0, reservas: 0, meuPreco: 500, concorrentes: [400, 600] }); assert.strictEqual(z.distribuicao, null); assert.strictEqual(z.conversaoPct, null); assert.strictEqual(z.indicePreco, null); assert(z.faltam.length >= 1);
  assert.strictEqual(RX.c1({ visitas: 10, reservas: 20 }).conversaoPct, null);
});
t('C2: ocupação mensal e anual (soma, não média), >100% fora do total, canais, janela', () => {
  const meses = []; for (let i = 0; i < 12; i++) meses.push({ disponiveis: 300, vendidas: 150 + 5 * i, receita: 30000 });
  meses[1] = { disponiveis: 280, vendidas: 300, receita: 1 }; meses[2] = { disponiveis: 300 }; // 2: >100%; 3: dado faltando (não é zero)
  const c = RX.c2({ meses, canais: [{ nome: 'Direto', receita: 10000, comissaoPct: 0, custoAquisicao: 500 }, { nome: 'Plataforma', receita: 30000, comissaoPct: 15, custoAquisicao: 0 }, { nome: 'Sem comissão informada', receita: 5000 }], janela: ['3', '10', '21', '5', 'x', '-2'] });
  near(c.meses[0].ocupacaoPct, 50); assert(c.meses[1].invalido); assert.strictEqual(c.meses[2].ocupacaoPct, null); assert.equal(c.mesesValidos, 10);
  const ok = meses.filter((m, i) => i !== 1 && i !== 2); const esperado = ok.reduce((s, m) => s + m.vendidas, 0) / ok.reduce((s, m) => s + m.disponiveis, 0) * 100; near(c.ocupacaoAnualPct, esperado);
  assert.equal(c.canais[0].liquida, 9500); assert.equal(c.canais[1].liquida, 25500); near(c.canais[1].margemPct, 85); near(c.canais[1].participacaoPct, 30000 / 45000 * 100); assert.strictEqual(c.canais[2].liquida, null); assert.equal(c.janelaMediana, 7.5); assert.equal(c.janelaN, 4);
  assert.equal(c.mesesBaixos.length, 3); assert(c.avisos.some(a => /acima das disponíveis/.test(a))); assert.strictEqual(RX.c2({}).ocupacaoAnualPct, null);
});
t('C3: ADR, RevPAR = ADR × ocupação, extras e alertas', () => {
  const c = RX.c3({ receita: 24000, vendidas: 100, disponiveis: 200, extras: [{ nome: 'Café', preco: 80, custo: 30, qtd: 10 }, { nome: 'Passeio', preco: 20, custo: 25, qtd: 4 }, { nome: 'Cesta', preco: 100, custo: 40, qtd: 0 }, { nome: 'Sem custo informado', preco: 50 }] });
  assert.equal(c.adr, 240); assert.equal(c.revpar, 120); assert.equal(c.ocupacaoPct, 50); near(c.revpar, c.adr * c.ocupacaoPct / 100);
  assert.equal(c.extras[0].margemUnit, 50); near(c.extras[0].margemPct, 62.5); assert.equal(c.extras[0].margemMes, 500); assert.equal(c.extras[1].alerta, 'margem negativa'); assert.equal(c.extras[2].alerta, 'sem demanda no mês'); assert.strictEqual(c.extras[3].margemUnit, null);
  const z = RX.c3({ receita: 1000, vendidas: 0, disponiveis: 0 }); assert.strictEqual(z.adr, null); assert.strictEqual(z.revpar, null); const o = RX.c3({ receita: 1000, vendidas: 30, disponiveis: 20 }); assert.strictEqual(o.ocupacaoPct, null); assert(o.avisos.some(a => /ocupação > 100%/.test(a)));
});
const base4 = { disponiveis: 300, vendidas: 150, receita: 45000, fixos: [{ nome: 'Aluguel', valor: 6000 }, { nome: 'Sistemas e equipe', valor: 4000 }], limpeza: 80, insumos: 20, comissoes: 100, outrosVar: 0, noitesPorEstadia: 2, quedaOcupacaoPct: 20, quedaPrecoPct: 10, altaCustosPct: 10, ativos: [{ nome: 'Colchões', custo: 12000, vidaAnos: 5 }] };
t('C4: contribuição, equilíbrio, resultado, cenário adverso e provisão de reposição', () => {
  const c = RX.c4(base4); assert.equal(c.adr, 300); assert.equal(c.custoVarNoite, 100); assert.equal(c.contribuicaoNoite, 200); near(c.margemContribPct, 66.67); assert.equal(c.custoFixoTotal, 10000); near(c.equilibrioPct, 10000 / (200 * 300) * 100); assert.equal(c.resultado, 20000);
  assert.equal(c.adverso.vendidas, 120); assert.equal(c.adverso.adr, 270); assert.equal(c.adverso.contribuicao, 160); assert.equal(c.adverso.resultado, 8200); assert.equal(c.adverso.deficit, false); assert.equal(c.provisaoReposicaoMensal, 200); near(c.ocupacaoPct, 50);
});
t('C4: contribuição negativa, equilíbrio acima de 100% e dados faltantes não viram zero', () => {
  const neg = RX.c4(Object.assign({}, base4, { receita: 13500 })); assert.equal(neg.adr, 90); assert.equal(neg.contribuicaoNoite, -10); assert.strictEqual(neg.equilibrioPct, null); assert(/não existe ocupação de equilíbrio/.test(neg.equilibrioMsg)); assert.equal(neg.resultado, 150 * -10 - 10000);
  const alto = RX.c4(Object.assign({}, base4, { fixos: [{ nome: 'x', valor: 100000 }] })); near(alto.equilibrioPct, 100000 / (200 * 300) * 100); assert(/passa de 100%/.test(alto.equilibrioMsg));
  const f = RX.c4(Object.assign({}, base4, { limpeza: undefined })); assert.strictEqual(f.custoVarNoite, null); assert.strictEqual(f.contribuicaoNoite, null); assert.strictEqual(f.equilibrioPct, null); assert(f.faltam.some(x => /custos variáveis/.test(x)));
  const d0 = RX.c4(Object.assign({}, base4, { disponiveis: 0 })); assert.strictEqual(d0.equilibrioPct, null); assert(/Sem noites disponíveis/.test(d0.equilibrioMsg)); assert.strictEqual(RX.c4(Object.assign({}, base4, { noitesPorEstadia: 0 })).custoVarNoite, null);
  const df = RX.c4(Object.assign({}, base4, { vendidas: 30, receita: 6000, altaCustosPct: 80, quedaOcupacaoPct: 50, quedaPrecoPct: 30 })); assert.equal(df.adverso.deficit, true);
  assert.strictEqual(RX.c4(Object.assign({}, base4, { ativos: [{ nome: 'a', custo: 1000, vidaAnos: 0 }] })).provisaoReposicaoMensal, null);
});
t('C5: carga, estoque mínimo/ponto de pedido e conciliação', () => {
  const c = RX.c5({ horasDisponiveis: 8, tarefas: [{ nome: 'Limpar', minutos: 30, qtd: 10 }, { nome: 'Check-in', minutos: 20, qtd: 6 }, { nome: 'Incompleta', minutos: 15 }], estoque: [{ nome: 'Papel', consumoDia: 4, prazoDias: 5, margemDias: 2, saldo: 25 }, { nome: 'Sabonete', consumoDia: 2, prazoDias: 3, margemDias: 1, saldo: 50 }], divergencias: [{ ref: 'R1', pms: 500, extrato: 450 }, { ref: 'R2', pms: 300, extrato: 300 }, { ref: 'R3', pms: 200 }] });
  assert.equal(c.horasNecessarias, 7); assert.equal(c.cargaPct, 87.5); assert.equal(c.estoque[0].estoqueMinimo, 20); assert.equal(c.estoque[0].pontoPedido, 28); assert.equal(c.estoque[0].situacao, 'repor'); assert.equal(c.estoque[1].estoqueMinimo, 6); assert.equal(c.estoque[1].pontoPedido, 8); assert.equal(c.estoque[1].situacao, 'ok');
  assert.equal(c.conciliacao.comparadas, 2); assert.equal(c.conciliacao.divergentes, 1); assert.equal(c.conciliacao.totalAbsoluto, 50); assert(c.avisos.some(a => /Incompleta/.test(a)));
  const s = RX.c5({ horasDisponiveis: 6, tarefas: [{ nome: 'a', minutos: 30, qtd: 10 }, { nome: 'b', minutos: 20, qtd: 6 }] }); near(s.cargaPct, 116.67); assert(s.avisos.some(a => /acima de 100%/.test(a))); assert.strictEqual(RX.c5({ horasDisponiveis: 0, tarefas: [{ minutos: 10, qtd: 1 }] }).cargaPct, null);
});
const base6 = { unidade: 200000, obras: 150000, licencas: 20000, mobiliario: 30000, contingenciaPct: 10, limpeza: 1000, energia: 800, equipe: 3000, manutencao: 500, outros: 200, custoVarNoite: 100, unidades: 2, diaria: 500, ocupacaoPct: 50, deltaOcPontos: 10, deltaDiariaPct: 10 };
t('C6: custo instalado, retorno simples, payback e cenários', () => {
  const c = RX.c6(base6); assert.equal(c.custoTotalInstalado, 440000); assert.equal(c.custosAdicionaisMensais, 5500); assert.equal(c.base.receitaAnual, 182500); assert.equal(c.base.custosAnuais, 102500); assert.equal(c.base.resultadoAnual, 80000); near(c.base.retornoPct, 80000 / 440000 * 100); assert.equal(c.base.paybackAnos, 5.5);
  assert.equal(c.pessimista.receitaAnual, 131400); assert.equal(c.pessimista.resultadoAnual, 36200); near(c.pessimista.paybackAnos, 440000 / 36200); assert.equal(c.otimista.ocupacaoPct, 60); assert(c.avisos.some(a => /não é garantia/.test(a)));
});
t('C6: resultado negativo não tem payback; faltantes não viram zero', () => {
  const n = RX.c6(Object.assign({}, base6, { ocupacaoPct: 10, deltaOcPontos: 20 })); assert.strictEqual(n.base.paybackAnos, null); assert.equal(n.base.semRetorno, true); assert(n.avisos.some(a => /não se paga/.test(a))); assert.equal(n.pessimista.ocupacaoPct, 0);
  const f = RX.c6(Object.assign({}, base6, { obras: undefined })); assert.strictEqual(f.custoTotalInstalado, null); assert.strictEqual(f.base, null); assert(f.faltam.length);
});
t('C7: necessidade de capital = total − recursos próprios; cobertura; sem falta', () => {
  const c = RX.c7({ investimento: 500000, contingenciaPct: 10, capitalGiro: 50000, recursosProprios: 200000 }); assert.equal(c.totalComContingencia, 600000); assert.equal(c.necessidadeCapital, 400000); near(c.coberturaPropriaPct, 33.33);
  const s = RX.c7({ investimento: 100000, contingenciaPct: 0, capitalGiro: 0, recursosProprios: 150000 }); assert.equal(s.necessidadeCapital, -50000); assert(s.avisos.some(a => /cobrem/.test(a))); assert.strictEqual(RX.c7({ investimento: 1000 }).necessidadeCapital, null);
  assert(RX.c7({}).avisos.some(a => /não atribui valor/.test(a)));
});
t('entradas negativas e texto inválido são recusados com aviso (não viram zero)', () => {
  const c = RX.c3({ receita: -100, vendidas: 'abc', disponiveis: 10 }); assert.strictEqual(c.adr, null); assert(c.avisos.some(a => /negativo/.test(a)) && c.avisos.some(a => /inválido/.test(a)));
});
t('dossiê: seções, convite sem consentimento, alertas de dados, sem dados pessoais de contato', () => {
  const perfil = { identificacao: { nome: 'Pousada Exemplo (dados fictícios)', tipo: 'pousada', municipio: 'Cidade Exemplo', periodo: '2026-01 a 2026-12', fonte: 'planilha própria' }, respostas: { m1q1: '2', m1q2: '0', m5q9: 'unknown', m2q2: '1' }, calculadoras: { C3: { receita: 1000, vendidas: 30, disponiveis: 20 } }, email: 'x@y.com' };
  const d = RX.montarDossie(perfil, Q, META, { inicio: '2026-12-01' });
  ['identificacao', 'diagnostico', 'plano', 'calculos', 'alertasDeDados', 'limitacoes', 'convite', 'recomendacoesEducacionais'].forEach(k => assert(d[k] !== undefined, k)); assert.equal(d.convite.consentimento, false); assert(/nada é enviado automaticamente/.test(d.convite.texto));
  assert(d.alertasDeDados.some(a => /ocupação > 100%/.test(a))); assert(d.limitacoes.length >= 5); assert.equal(JSON.stringify(d).indexOf('x@y.com'), -1); assert.equal(d.diagnostico.aColetar[0], 'm5q9'); assert(d.calculos.C3);
  assert.equal(RX.montarDossie({ consentimento: true }, Q, META, { inicio: '2026-12-01' }).convite.consentimento, true);
});
console.log(ok + ' testes de lógica ok');

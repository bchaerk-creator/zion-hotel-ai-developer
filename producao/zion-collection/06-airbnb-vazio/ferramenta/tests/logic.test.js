// Testes da lógica do Diagnóstico Zion de Oferta. Uso: node tests/logic.test.js
const L = require("../src/logic.js");
let ok = 0, fal = 0;
const t = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
const ids = L.DIMENSOES.map(d => d.id);
const resp = (notas, ev = "evidência") => Object.fromEntries(ids.map((id, i) => [id, { nota: notas[i], evidencia: ev }]));
// regra independente: soma/35*100 arredondado; faixa por limites; 3 menores com desempate pela ordem
const ref = (notas) => {
  const s = notas.reduce((a, b) => a + b, 0), p = Math.round(s * 100 / 35);
  const f = p >= 85 ? "Oferta consistente" : p >= 70 ? "Boa base com pontos de melhoria" : p >= 50 ? "Ajustes prioritários" : "Lacunas relevantes";
  const pri = notas.map((n, i) => [n, i]).sort((a, b) => a[0] - b[0] || a[1] - b[1]).slice(0, 3).map(x => ids[x[1]]);
  return { p, f, pri };
};

t(L.DIMENSOES.length === 7, "sete dimensões");
t(L.DIMENSOES.map(d => d.nome).join("|") === "Fotos e apresentação|Título e descrição|Preço e posicionamento|Diferenciais e experiência|Avaliações e confiança|Atendimento e comunicação|Conforto e infraestrutura", "nomes e ordem das dimensões iguais ao e-book");

// todas 0
let d = L.calcular(resp([0, 0, 0, 0, 0, 0, 0]));
t(d.completo && d.pontuacao === 0 && d.faixa.nome === "Lacunas relevantes", "todas as notas 0 → 0, lacunas relevantes");
t(d.prioridades.map(x => x.id).join() === "fotos,titulo,preco", "empate total: prioridades pela ordem das dimensões");
// todas 5
d = L.calcular(resp([5, 5, 5, 5, 5, 5, 5]));
t(d.pontuacao === 100 && d.faixa.nome === "Oferta consistente" && d.todasMaximas, "todas 5 → 100, oferta consistente, aviso de notas máximas");
// limites das faixas
[[[3, 3, 3, 3, 3, 3, 2], 57], [[5, 5, 4, 4, 4, 4, 4], 86], [[4, 4, 4, 4, 4, 4, 4], 80], [[3, 3, 3, 3, 2, 2, 2], 51], [[2, 2, 2, 2, 3, 3, 3], 49]].forEach(([n, esperado]) => {
  const r = ref(n), x = L.calcular(resp(n));
  t(x.pontuacao === r.p && r.p === esperado && x.faixa.nome === r.f, `notas ${n.join(",")} → ${esperado} (${r.f})`);
});
// 30 cenários aleatórios contra a regra independente
let s = 7; const rnd = () => (s = (s * 1103515245 + 12345) % 2147483648) % 6;
let iguais = 0;
for (let k = 0; k < 300; k++) { const n = ids.map(rnd), r = ref(n), x = L.calcular(resp(n)); if (x.pontuacao === r.p && x.faixa.nome === r.f && x.prioridades.map(p => p.id).join() === r.pri.join()) iguais++; }
t(iguais === 300, "300 combinações aleatórias batem com a regra independente (pontuação, faixa e prioridades)");

d = L.calcular(resp([0, 5, 5, 5, 5, 5, 5]));
t(d.pontuacao === 86 && d.criticas.join() === "Fotos e apresentação" && d.prioridades[0].id === "fotos", "nota 0 com pontuação alta: alerta de nota crítica e fotos em 1º");
t(L.calcular(resp([2, 2, 2, 2, 2, 2, 2])).criticas.length === 0, "sem nota 0 ou 1: sem alerta crítico");
// exemplo fictício
const ex = L.exemplo(); d = L.calcular(ex.respostas);
t(d.pontuacao === 63 && d.faixa.nome === "Ajustes prioritários", "exemplo: 22 de 35 → 63, ajustes prioritários");
t(d.prioridades.map(x => x.id).join() === "fotos,atendimento,titulo", "exemplo: prioridades fotos, atendimento, título");
t(/dados fictícios/.test(ex.perfil.nome), "exemplo marcado como dados fictícios");

// entradas inválidas e ausentes
d = L.calcular({});
t(!d.completo && d.faltam === 7 && d.pontuacao === null && d.prioridades.length === 0, "nada preenchido: sem pontuação nem prioridades");
d = L.calcular({ ...resp([3, 3, 3, 3, 3, 3, 3]), conforto: { nota: "" } });
t(!d.completo && d.faltam === 1 && d.erros.conforto, "uma nota vazia bloqueia a pontuação e aponta o campo");
t(!L.nota(6).ok && !L.nota(-1).ok && !L.nota("abc").ok && !L.nota("2.5").ok && !L.nota("3,5").ok, "recusa 6, -1, texto e nota quebrada");
t(L.nota("4").valor === 4 && L.nota(" 0 ").valor === 0, "aceita texto numérico com espaços");
d = L.calcular(resp([3, 3, 3, 3, 3, 3, 3], ""));
t(d.completo && d.semEvidencia === 7 && d.avisos.length === 7, "sem evidência: calcula, mas avisa que a nota é hipótese");

// plano
const plano = L.sugestaoPlano(L.calcular(ex.respostas));
t(plano.length === 3 && plano[0].dimensao === "Fotos e apresentação" && plano.every(l => l.acao && l.indicador && l.status === "A fazer"), "plano sugerido com 3 ações, indicador e status");
t(!L.validarPlano(plano).valido, "plano sem responsável e prazo não passa");
plano.forEach((l, i) => { l.responsavel = "Ana"; l.prazo = "2026-12-0" + (i + 1); l.custo = i ? "150,50" : ""; });
t(L.validarPlano(plano).valido, "plano completo passa (custo opcional)");
t(!L.validarPlano([{ ...plano[0], prazo: "2026-02-30" }]).valido, "data impossível recusada");
t(!L.validarPlano([{ ...plano[0], custo: "-20" }]).valido && !L.validarPlano([{ ...plano[0], custo: "abc" }]).valido, "custo negativo ou texto recusado");
t(L.custo("R$ 1.250,00").valor === 1250 && L.custo("150").valor === 150, "custo aceita R$ 1.250,00 e 150");
t(!L.validarPlano([]).valido, "plano vazio não passa");

// CSV
const csv = L.gerarCSV({ nome: 'Casa "Sol"; Mar', periodo: "90 dias" }, L.calcular(ex.respostas), [{ ...plano[0], acao: "=HYPERLINK(\"x\")" }]);
t(csv.charCodeAt(0) === 0xFEFF, "CSV com BOM (acentos no Excel)");
t(csv.includes('"Casa ""Sol""; Mar"'), "CSV escapa aspas e ponto e vírgula");
t(csv.includes("'=HYPERLINK"), "CSV neutraliza fórmula injetada");
t(/Fotos e apresentação;2;/.test(csv) && /Pontuação geral \(0 a 100\);63/.test(csv), "CSV traz notas e pontuação");
t(/Não é previsão/.test(csv), "CSV traz o aviso de indicador orientativo");
t(L.csvCampo("ação ç ã é") === "ação ç ã é", "caracteres especiais preservados");

console.log(`\n${ok} ok, ${fal} falhas`); process.exit(fal ? 1 : 0);

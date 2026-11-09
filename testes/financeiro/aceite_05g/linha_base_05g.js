// Comando 05G-A · Linha de base: roda os testes de aceite O8 a O14 contra a ZAIOS ATUAL (cópia local, commit ec21ad5).
// Antes da implementação, os testes devem FALHAR onde a decisão ainda não está implementada. Nada é alterado na ZAIOS.
// Uso: ZAIOS_SRC_DIR=<raiz da cópia> node testes/financeiro/aceite_05g/linha_base_05g.js --saida <pasta>
"use strict";
const fs = require("fs"), path = require("path");
const { carregarComposicao } = require("../lib/zaios_comp");
const RAIZ = path.resolve(__dirname, "..");
const ENT = JSON.parse(fs.readFileSync(path.join(RAIZ, "composicao_05f", "cenarios_05f.json"), "utf8"));
const ESP05F = JSON.parse(fs.readFileSync(path.join(RAIZ, "independente", "esperados_05f.json"), "utf8"));
const X = JSON.parse(fs.readFileSync(path.join(__dirname, "esperados_aceite_05g.json"), "utf8")).testes;
const R = (x) => Math.round(x * 100), COM = ENT.comum_adotado, C = Object.fromEntries(ENT.cenarios.map((c) => [c.id, c]));
function valores(c, outrasPct) {
  const linhas = Object.fromEntries(Object.entries(COM.linhas_capex_proporcao).map(([k, p]) => [`${k}_valor`, R(c.investimento * p)]));
  const s = c.sazonalidade, rv = { unidades: c.unidades, meses_alta: s ? s.meses_alta : [], meses_baixa: s ? s.meses_baixa : [], deducoes_pct: c.tributos_pct, variavel_noite: 0,
    custo_estadia: R(c.custo_estadia), permanencia: c.permanencia, quebra_pct: 0, custo_fixo: R(c.fixo_mensal), horas_semana: 0, custo_hora: 0, aluguel: R(c.aluguel_mensal),
    gestao_pct: c.gestao_pct, royalty_pct: c.royalty_pct, reserva_pct: 0, mes_abertura: c.mes_abertura, outras_pct: outrasPct ?? ESP05F.cenarios[c.id].R2_zaios.outras_pct };
  for (const t of s ? ["alta", "media", "baixa"] : ["media"]) { rv[`diaria_${t}`] = R(s ? s.diaria[t] : c.diaria); rv[`ocupacao_${t}`] = s ? s.ocupacao[t] : c.ocupacao; }
  return { capexV: { unidades: c.unidades, ...linhas, perfil_risco: "primeira", contingencia_pct: 0, custo_fixo: R(c.fixo_mensal), terreno: 0 }, rv };
}
function rodar(K, c, outrasPct) {
  const { capexV, rv } = valores(c, outrasPct), cap = K["exercicios/capex-calculo"];
  const mapa = cap.lerMapaCapex(cap.calcularCapex(capexV).paraSalvar);
  const r6 = K["exercicios/receitas-calculo"].calcularReceitas(rv, {}, { custoFixoCapex: R(c.fixo_mensal) });
  const vb = K["exercicios/viabilidade-calculo"].calcularViabilidade({ taxa_desconto: 0.1, multiplo_saida: 6 }, {}, { mapaCapex: mapa, valoresReceitas: rv, custoFixoCapex: R(c.fixo_mensal) });
  return { r6, vb, e: vb.estudoViabilidade, m: r6.modeloP6, rv };
}
(async () => {
  const a = process.argv.slice(2), i = a.indexOf("--saida"), saida = path.resolve(i >= 0 ? a[i + 1] : path.join(RAIZ, "resultados", "ultima-05g"));
  const K = await carregarComposicao(["exercicios/capex-calculo", "exercicios/receitas-calculo", "exercicios/viabilidade-calculo"]);
  if (!K.ok) { console.error(K.motivo); process.exit(2); }
  const r1 = rodar(K, C.C1), r2 = rodar(K, C.C2), r3 = rodar(K, C.C3), r3e = rodar(K, C.C3E), r3ePct = rodar(K, C.C3E, ESP05F.cenarios.C3.R2_zaios.outras_pct);
  const ok = (b) => (b ? "PASSA" : "FALHA");
  const T = [
    ["O8-1", "P6 sem selo de aprovação (C2)", X["O8-1"].esperado.selos_proibidos_no_p6.includes(r2.r6.veredito.selo) ? "FALHA" : "PASSA", `selo do P6 = "${r2.r6.veredito.selo}"`],
    ["O8-2", "Conflito P6 x viabilidade explicitado (C3E)", ok(r3e.r6.veredito.selo !== "Avançar" && !!r3e.vb.alertas.find((t) => /conflit|contradi/i.test(t))), `P6 "${r3e.r6.veredito.selo}" x viabilidade "${r3e.e.decisao}"; alertas da viabilidade: ${r3e.vb.alertas.length}`],
    ["O8-3", "Margem antes e depois dos custos do modelo com nomes distintos (C1)", ok("margemEbitda" in r1.m), `modelo do P6 expõe só margemOperacional = ${r1.m.margemOperacional.toFixed(6)}`],
    ["O9-1", "Saída não negativa com EBITDA < 0 (C1)", ok(r1.e.saida >= 0 && Math.abs(r1.e.vplCom / 100 - X["O9-1"].esperado.vpl_com_saida) <= 0.01), `saída = R$ ${(r1.e.saida / 100).toFixed(2)}; VPL com saída = R$ ${(r1.e.vplCom / 100).toFixed(2)}`],
    ["O9-2", "Saída inalterada com EBITDA > 0 (C2)", ok(Math.abs(r2.e.saida / 100 - X["O9-2"].esperado.valor_saida) <= 0.01), `saída = R$ ${(r2.e.saida / 100).toFixed(2)}`],
    ["O10-1", "Necessidade de caixa no ano 5 aparece (C1)", ok(r1.e.curva.com.pontos.length >= 120 && r1.e.curva.com.pontos.some((p) => p.saldo < 0)), `curva com ${r1.e.curva.com.pontos.length} meses; menor saldo R$ ${(r1.e.curva.com.menor / 100).toFixed(2)}; esperado: 1º mês negativo ${X["O10-1"].esperado.primeiro_mes_negativo}`],
    ["O10-2", "Atraso não melhora o projeto sem explicação (C2)", ok(r2.e.estresse.atraso.com.menor <= r2.e.curva.com.menor), `menor saldo com atraso R$ ${(r2.e.estresse.atraso.com.menor / 100).toFixed(2)} > sem atraso R$ ${(r2.e.curva.com.menor / 100).toFixed(2)}`],
    ["O11-1", "Bases de gestão e royalties configuráveis (C2)", ok("gestao_base" in r2.rv || "base_gestao" in r2.r6.parametrosP6), `sem campo de base; EBITDA = R$ ${(r2.m.ano.ebitda / 100).toFixed(2)} (= combinação bruta/bruta ${X["O11-1"].esperado["gestao_bruta__royalty_bruta"].ebitda.toFixed(2)})`],
    ["O12-1", "Aluguel na base do giro (C1)", ok(Math.abs(r1.m.giro.a / 100 - 6 * X["O12-1"].esperado.C1) <= 0.01), `giro A = R$ ${(r1.m.giro.a / 100).toFixed(2)} (6 × fixo sem aluguel)`],
    ["O13-1", "Necessário x disponível com déficit (C1)", ok("giroDisponivel" in r1.e || "deficitGiro" in r1.e), `sem campo de capital disponível; captação = R$ ${(r1.e.captacao / 100).toFixed(2)}`],
    ["O14-1", "Receita independente não cai com a ocupação (C3 → C3E, percentual mantido)", ok(Math.abs(r3ePct.m.ano.outras / 100 - 480000) <= 0.01), `outras no C3E com o mesmo percentual = R$ ${(r3ePct.m.ano.outras / 100).toFixed(2)} (esperado R$ 480.000,00 para a categoria C)`],
  ];
  fs.mkdirSync(saida, { recursive: true });
  let md = `# Linha de base dos testes de aceite O8 a O14\n\nGerado em ${new Date().toISOString()} contra a cópia da ZAIOS (commit ec21ad5). **Antes da implementação, FALHA é o resultado esperado** onde a decisão ainda não existe no código. PASSA indica um comportamento que já atende à decisão.\n\n| Teste | Verificação | Resultado atual | Evidência |\n|---|---|---|---|\n`;
  for (const [id, d, r, ev] of T) md += `| ${id} | ${d} | ${r} | ${ev} |\n`;
  fs.writeFileSync(path.join(saida, "LINHA_BASE_05G.md"), md);
  fs.writeFileSync(path.join(saida, "linha_base_05g.json"), JSON.stringify(T.map(([id, verificacao, resultado, evidencia]) => ({ id, verificacao, resultado, evidencia })), null, 1));
  console.log(md);
})();

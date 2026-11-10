// Comando Mestre · Testes de aceite O8 a O14 depois da implementação, por valor (não por nome de campo).
// Usa os esperados independentes do 05G-A quando a regra não depende de outra decisão, e os do Comando Mestre quando depende.
// Uso: ZAIOS_SRC_DIR=<raiz da cópia dev> node testes/financeiro/mestre/aceite_mestre.js --saida <pasta>
"use strict";
const fs = require("fs"), path = require("path");
const { carregarComposicao } = require("../lib/zaios_comp");
const { obter } = require("./run_mestre");
const X = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "aceite_05g", "esperados_aceite_05g.json"), "utf8")).testes;
const M = JSON.parse(fs.readFileSync(path.join(__dirname, "esperados_mestre.json"), "utf8")).casos;
const perto = (a, b, t = 0.01) => a != null && b != null && Math.abs(a - b) <= t;
(async () => {
  const a = process.argv.slice(2), i = a.indexOf("--saida"), saida = path.resolve(i >= 0 ? a[i + 1] : "aceite-mestre");
  const K = await carregarComposicao(["exercicios/capex-calculo", "exercicios/receitas-calculo", "exercicios/viabilidade-calculo"]);
  if (!K.ok) { console.error(K.motivo); process.exit(2); }
  const z = (id, extra = {}) => obter(K, { ...M[id].entrada, ...extra });
  const c1 = z("M-C1"), c2 = z("M-C2"), c3 = z("M-C3"), c3e = z("M-C3E"), abc = z("M-C3-ABC"), abce = z("M-C3E-ABC");
  const combos = { gestao_hospedagem__royalty_hospedagem: ["hospedagem", "hospedagem"], gestao_hospedagem__royalty_bruta: ["hospedagem", "bruta"], gestao_bruta__royalty_hospedagem: ["bruta", "hospedagem"], gestao_bruta__royalty_bruta: ["bruta", "bruta"] };
  const d1 = z("M-C1-disp"), d2 = z("M-C2-disp"), dup = z("M-C1-aluguel-no-fixo");
  const T = [
    ["O8-1", "P6 sem selo de aprovação; texto de indicação inicial (C2)", c2.selo_p6 === "Indicação preliminar" && c2._motivo_p6.includes(X["O8-1"].esperado.texto_obrigatorio)],
    ["O8-2", "Conflito P6 positivo x viabilidade Redesenhar explicitado (C3E)", c3e.indicacao === "positiva" && c3e.decisao === "Redesenhar" && c3e._alertas_viab.some((t) => t.startsWith("Conflito entre etapas") && t.includes("Prevalece a análise financeira completa"))],
    ["O8-3", "Margem antes e depois dos custos do modelo (C1, valores do 05G-A)", perto(c1.margem_operacional, X["O8-3"].esperado.margem_operacional_antes_custos_modelo, 1e-9) && perto(c1.margem_ebitda, X["O8-3"].esperado.margem_ebitda, 1e-9)],
    ["O9-1", "EBITDA negativo: saída 0 e VPL com = sem (C1, 05G-A)", c1.valor_saida === 0 && perto(c1.vpl_com, X["O9-1"].esperado.vpl_com_saida) && perto(c1.vpl_com, c1.vpl_sem)],
    ["O9-2", "EBITDA positivo: saída inalterada (C2, 05G-A)", perto(c2.valor_saida, X["O9-2"].esperado.valor_saida) && perto(c2.vpl_com, X["O9-2"].esperado.vpl_com_saida)],
    ["O10-1", "Horizonte de 120 meses mostra a queima depois do mês 36 (C1)", c1.curva_meses === 120 && c1.curva_menor36 > 0 && c1.curva_primeiro_negativo > 36 && perto(c1.capital_adicional, -c1.curva_menor) && perto(c1.curva_final, M["M-C1"].esperado.curva_final)],
    ["O10-2", "Atraso reduz saldo final e VPL, com explicação (C2)", c2.atraso_perda_saldo_final > 0 && c2.atraso_perda_vpl > 0 && c2.atraso_receita_nao_realizada > 0 && /CAPEX no cronograma original/.test(c2._explicacao_atraso)],
    ["O10-3", "Saldos de fim de ano 1 a 10 (C2)", c2.saldos_anuais.length === 10 && c2.saldos_anuais.every((s, k) => perto(s, M["M-C2"].esperado.saldos_anuais[k]))],
    ...Object.entries(combos).map(([k, [g, r]]) => { const o = z("M-C2", { gestao_base: g, royalty_base: r }); return [`O11-1 ${k}`, "EBITDA com bases independentes (C2, 05G-A)", perto(o.ebitda, X["O11-1"].esperado[k].ebitda) && perto(o.gestao, X["O11-1"].esperado[k].gestao) && perto(o.royalty, X["O11-1"].esperado[k].royalty)]; }),
    ["O11-2", "Sem contrato: premissa marcada como hipótese, com base e percentual", c2._alertas_p6.some((t) => t.includes("hipótese") && t.includes("%") && t.includes("receita bruta"))],
    ["O12-1", "Base mensal do giro com aluguel uma vez (C1, C2, C3; 05G-A)", perto(c1.giro_base_mensal, X["O12-1"].esperado.C1) && perto(c2.giro_base_mensal, X["O12-1"].esperado.C2) && perto(c3.giro_base_mensal, X["O12-1"].esperado.C3)],
    ["O12-2", "Giro = déficit + sazonalidade + 3 × base com aluguel (C1, 05G-A)", perto(c1.giro, X["O12-2"].esperado.giro_b)],
    ["O12-3", "Aluguel dentro do custo fixo: alerta e uma contagem", dup._alertas_p6.some((t) => t.includes("duas vezes")) && perto(dup.giro_base_mensal, 9000)],
    ["O13-1", "C1, disponível 45 mil: déficit = necessário − disponível; usos = CAPEX + necessário", perto(d1.giro_deficit, d1.giro - 45000) && d1.giro_excedente === 0 && perto(d1.usos_totais, d1.captacao)],
    ["O13-3", "C2, disponível 200 mil: excedente", perto(d2.giro_excedente, 200000 - d2.giro) && d2.giro_deficit === 0],
    ["O13-4", "Disponível não muda a curva técnica (C1)", perto(d1.curva_menor, c1.curva_menor) && perto(d1.captacao, c1.captacao)],
    ["O14-1", "A e B caem com a ocupação; C fica constante (C3 → C3E, 05G-A)", ["C3", "C3E"].every((k, j) => { const o = [abc, abce][j], e = X["O14-1"].esperado[k]; return perto(o.compl_a, e.A) && perto(o.compl_b, e.B) && perto(o.compl_c, e.C) && perto(o.receita_bruta, e.receita_bruta) && perto(o.deducoes, e.tributos) && perto(o.custos_complementares, e.custos_complementares); })],
    ["O14-2", "Hospedagem não muda com as complementares (C3, 05G-A)", perto(abc.hospedagem, X["O14-2"].esperado.hospedagem_C3) && perto(c3.hospedagem, abc.hospedagem)],
    ["O14-3", "Cenário conservador não reduz a categoria C", perto(abc.conservador_compl_c, abc.compl_c)],
  ].map(([id, verificacao, ok]) => ({ id, verificacao, resultado: ok ? "PASSA" : "FALHA" }));
  const p = T.filter((t) => t.resultado === "PASSA").length;
  fs.mkdirSync(saida, { recursive: true });
  fs.writeFileSync(path.join(saida, "aceite_mestre.json"), JSON.stringify(T, null, 1));
  fs.writeFileSync(path.join(saida, "ACEITE_MESTRE.md"), `# Aceite O8 a O14 depois da implementação\n\n${p} de ${T.length} passam.\n\n| Teste | Verificação | Resultado |\n|---|---|---|\n` + T.map((t) => `| ${t.id} | ${t.verificacao} | ${t.resultado} |`).join("\n") + "\n");
  console.log(`aceite: ${p}/${T.length} passam` + T.filter((t) => t.resultado !== "PASSA").map((t) => `; FALHA ${t.id}`).join(""));
})();

// Comando Mestre · Compara a versão de desenvolvimento da ZAIOS (cópia local, ZAIOS_SRC_DIR) com os esperados
// independentes das regras aprovadas (esperados_mestre.json). Não altera a ZAIOS. O código da ZAIOS não fica no repositório.
// Uso: ZAIOS_SRC_DIR=<raiz da cópia dev> node testes/financeiro/mestre/run_mestre.js --saida <pasta>
"use strict";
const fs = require("fs"), path = require("path");
const { carregarComposicao } = require("../lib/zaios_comp");
const RAIZ = path.resolve(__dirname, "..");
const F05 = JSON.parse(fs.readFileSync(path.join(RAIZ, "composicao_05f", "cenarios_05f.json"), "utf8"));
const E05 = JSON.parse(fs.readFileSync(path.join(RAIZ, "independente", "esperados_05f.json"), "utf8"));
const ESP = JSON.parse(fs.readFileSync(path.join(__dirname, "esperados_mestre.json"), "utf8")).casos;
const COM = F05.comum_adotado, BASE = Object.fromEntries(F05.cenarios.map((c) => [c.id, c]));
const R = (x) => Math.round(x * 100);
const BASES = { hospedagem: "Percentual da receita de hospedagem", bruta: "Percentual da receita bruta total", fixo: "Valor fixo mensal" };
function entradas(cs) {
  const c = BASE[cs.base], s = c.sazonalidade, k = cs.compl || {};
  const linhas = Object.fromEntries(Object.entries(COM.linhas_capex_proporcao).map(([q, p]) => [`${q}_valor`, R(c.investimento * p)]));
  const capexV = { unidades: c.unidades, ...linhas, perfil_risco: "primeira", contingencia_pct: 0, custo_fixo: R(c.fixo_mensal), terreno: 0 };
  const rv = { unidades: c.unidades, meses_alta: s ? s.meses_alta : [], meses_baixa: s ? s.meses_baixa : [], deducoes_pct: c.tributos_pct, variavel_noite: 0, custo_estadia: R(c.custo_estadia),
    permanencia: c.permanencia, quebra_pct: 0, custo_fixo: R(c.fixo_mensal), horas_semana: 0, custo_hora: 0, aluguel: R(c.aluguel_mensal), gestao_pct: c.gestao_pct, royalty_pct: c.royalty_pct,
    reserva_pct: 0, mes_abertura: c.mes_abertura, outras_pct: cs.outras_pct_zero ? 0 : E05.cenarios[c.id].R2_zaios.outras_pct };
  for (const t of s ? ["alta", "media", "baixa"] : ["media"]) { rv[`diaria_${t}`] = R(s ? s.diaria[t] : c.diaria); rv[`ocupacao_${t}`] = s ? s.ocupacao[t] : c.ocupacao; }
  if (cs.gestao_base) rv.gestao_base = BASES[cs.gestao_base];
  if (cs.royalty_base) rv.royalty_base = BASES[cs.royalty_base];
  if (cs.gestao_fixo != null) rv.gestao_fixo = R(cs.gestao_fixo);
  if (cs.gestao_contrato) rv.gestao_contrato = "Sim, definida em contrato";
  if (cs.reserva_meses != null) rv.reserva_meses = cs.reserva_meses;
  if (cs.outras_obrigacoes != null) rv.outras_obrigacoes = R(cs.outras_obrigacoes);
  if (cs.fixo_inclui_aluguel) rv.fixo_inclui_aluguel = "Sim";
  if (k.a_noite != null) Object.assign(rv, { compl_a_noite: R(k.a_noite), compl_a_custo: k.a_custo, compl_b_ticket: R(k.b_ticket), compl_b_adesao: k.b_adesao, compl_b_custo: k.b_custo, compl_c_anual: R(k.c_anual), compl_c_custo: k.c_custo });
  if (k.c_meses) rv.compl_c_meses = k.c_meses;
  if (k.c_rampa) rv.compl_c_rampa = "Sim";
  if (k.aliquota != null) rv.compl_aliquota = k.aliquota;
  const viab = { taxa_desconto: COM.taxa_desconto, multiplo_saida: COM.multiplo_saida };
  if (cs.giro_disponivel != null) viab.giro_disponivel = R(cs.giro_disponivel);
  return { capexV, rv, viab, fixo: R(c.fixo_mensal) };
}
function obter(K, cs) {
  const en = entradas(cs), cap = K["exercicios/capex-calculo"], mapa = cap.lerMapaCapex(cap.calcularCapex(en.capexV).paraSalvar);
  const r6 = K["exercicios/receitas-calculo"].calcularReceitas(en.rv, {}, { custoFixoCapex: en.fixo });
  const vb = K["exercicios/viabilidade-calculo"].calcularViabilidade(en.viab, {}, { mapaCapex: mapa, valoresReceitas: en.rv, custoFixoCapex: en.fixo });
  const m = r6.modeloP6, a = m.ano, e = vb.estudoViabilidade, d = (x) => (x == null ? null : x / 100), at = e.estresse.atraso, ga = e.giroAnalise;
  // Versões anteriores às decisões não têm alguns campos: ficam null (o teste falha, não quebra).
  const o = { hospedagem: d(a.diarias), compl_a: d(a.complA), compl_b: d(a.complB), compl_c: d(a.complC), receita_bruta: d(a.receitaBruta), deducoes: d(a.deducoes), custos_complementares: d(a.custosComplementares),
    custos_variaveis: d(a.custosVariaveis), gestao: d(a.gestao), royalty: d(a.royalty), custos_modelo: d(a.custosModelo), ebitda: d(a.ebitda), geracao_regime: d(a.geracaoCaixa), geracao_ano1: d(e.geracaoAno1),
    margem_operacional: m.margemOperacional, margem_ebitda: m.margemEbitda, indicacao: m.indicacao, equilibrio_noites: m.equilibrio.noites, deficit_rampa: d(m.deficit), sazonalidade: d(m.giro.sazonalidade),
    giro_tecnica: d(m.giro.tecnica), giro_base_mensal: d(m.giro.baseMensal), giro_reserva: d(m.giro.reserva), giro: d(e.giro), captacao: d(e.captacao), valor_saida: d(e.saida), vpl_sem: d(e.vplSem), vpl_com: d(e.vplCom),
    tir_sem: e.tirSem.taxa, payback_simples: e.paybackSimples.anos, conservador_vpl_sem: d(e.cenarios[0].vplSem), otimista_vpl_sem: d(e.cenarios[2].vplSem), conservador_compl_c: null,
    curva_meses: e.curva.com.pontos.length, curva_menor: d(e.curva.com.menor), curva_mes_menor: e.curva.com.mesMenor, curva_final: d(e.curva.com.final), curva_menor36: d(e.curva.com.menor36),
    curva_primeiro_negativo: e.curva.com.primeiroNegativo, capital_adicional: d(e.curva.com.capitalAdicional), saldos_anuais: (e.curva.com.anuais || []).map(d), atraso_custos_mantidos: d(at.custosMantidos),
    atraso_receita_nao_realizada: d(at.receitaNaoRealizada), atraso_perda_saldo_final: d(at.perdaSaldoFinal), atraso_vpl_sem: d(at.vplSem), atraso_perda_vpl: d(at.perdaVpl), atraso_menor: d(at.com.menor),
    colchao: e.colchao, passos: e.passos.map((p) => p.resultado), decisao: e.decisao, selo_p6: r6.veredito.selo,
    _motivo_p6: r6.veredito.motivo, _alertas_p6: r6.alertas || [], _alertas_viab: vb.alertas || [], _explicacao_atraso: at.explicacao || "" };
  if (ga) Object.assign(o, { giro_disponivel: d(ga.disponivel), giro_diferenca: d(ga.diferenca), giro_deficit: d(ga.deficit), giro_excedente: d(ga.excedente), usos_totais: d(e.usosTotais) });
  // Categoria C no cenário conservador: recalcula o P6 com ocupação e diária do conservador (a viabilidade não expõe o detalhe).
  const rvC = JSON.parse(JSON.stringify(en.rv));
  for (const t of ["alta", "media", "baixa"]) { if (rvC[`diaria_${t}`] != null) rvC[`diaria_${t}`] *= 0.9; if (rvC[`ocupacao_${t}`] != null) rvC[`ocupacao_${t}`] = Math.min(1, rvC[`ocupacao_${t}`] * 0.8); }
  o.conservador_compl_c = d(K["exercicios/receitas-calculo"].calcularReceitas(rvC, {}, { custoFixoCapex: en.fixo }).modeloP6.ano.complC);
  return o;
}
const tol = (k) => (/margem|tir_|colchao/.test(k) ? 1e-7 : /payback|noites|mes_|meses|negativo/.test(k) ? 1e-6 : 0.01);
const igual = (a, b, t) => (a == null || b == null) ? a == null && b == null : Array.isArray(a) ? a.length === b.length && a.every((x, i) => igual(x, b[i], t)) : typeof a === "number" ? Math.abs(a - b) <= t : a === b;
if (require.main === module) (async () => {
  const a = process.argv.slice(2), i = a.indexOf("--saida"), saida = path.resolve(i >= 0 ? a[i + 1] : path.join(RAIZ, "resultados", "ultima-mestre"));
  const K = await carregarComposicao(["exercicios/capex-calculo", "exercicios/receitas-calculo", "exercicios/viabilidade-calculo"]);
  if (!K.ok) { console.error(K.motivo); process.exit(2); }
  const linhas = [];
  for (const [id, { entrada, esperado }] of Object.entries(ESP)) {
    const z = obter(K, entrada);
    for (const [k, v] of Object.entries(esperado)) linhas.push({ caso: id, campo: k, esperado: v, zaios: z[k], resultado: igual(v, z[k], tol(k)) ? "OK" : "DIVERGE" });
    linhas.push({ caso: id, campo: "selo_p6 (O8)", esperado: "Indicação preliminar", zaios: z.selo_p6, resultado: z.selo_p6 === "Indicação preliminar" ? "OK" : "DIVERGE" });
  }
  const ok = linhas.filter((l) => l.resultado === "OK").length;
  fs.mkdirSync(saida, { recursive: true });
  fs.writeFileSync(path.join(saida, "resultado_mestre.json"), JSON.stringify({ campos: linhas.length, ok, divergencias: linhas.length - ok, linhas }, null, 1));
  let md = `# Esperados independentes x versão de desenvolvimento\n\nGerado em ${new Date().toISOString()}. ${Object.keys(ESP).length} casos, ${linhas.length} campos: **${ok} OK, ${linhas.length - ok} divergências**.\n\n`;
  const div = linhas.filter((l) => l.resultado !== "OK");
  if (div.length) { md += "| Caso | Campo | Esperado | ZAIOS dev |\n|---|---|---|---|\n"; for (const l of div) md += `| ${l.caso} | ${l.campo} | ${JSON.stringify(l.esperado)} | ${JSON.stringify(l.zaios)} |\n`; }
  fs.writeFileSync(path.join(saida, "RESULTADO_MESTRE.md"), md);
  console.log(`mestre: ${Object.keys(ESP).length} casos, ${linhas.length} campos: ${ok} OK, ${linhas.length - ok} divergências`);
  for (const l of div.slice(0, 30)) console.log("  ", l.caso, l.campo, JSON.stringify(l.esperado).slice(0, 60), "x", JSON.stringify(l.zaios).slice(0, 60));
})();
module.exports = { entradas, obter };

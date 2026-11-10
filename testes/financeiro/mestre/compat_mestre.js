// Comando Mestre · Compatibilidade com projetos existentes. Roda a versão de base (ZAIOS_BASE_DIR, commit ec21ad5)
// e a de desenvolvimento (ZAIOS_SRC_DIR) com respostas antigas, sem os campos novos, e separa:
// (1) campos que precisam ficar idênticos (regras não alteradas); (2) campos que mudam por decisão aprovada.
// Também abre resultados salvos pela versão de base com os leitores da versão nova.
// Uso: ZAIOS_BASE_DIR=<cópia ec21ad5> ZAIOS_SRC_DIR=<cópia dev> node testes/financeiro/mestre/compat_mestre.js --saida <pasta>
"use strict";
const fs = require("fs"), path = require("path");
const { carregarComposicao } = require("../lib/zaios_comp");
const RAIZ = path.resolve(__dirname, "..");
const F05 = JSON.parse(fs.readFileSync(path.join(RAIZ, "composicao_05f", "cenarios_05f.json"), "utf8"));
const G05 = JSON.parse(fs.readFileSync(path.join(RAIZ, "composicao_05g", "cenarios_05g.json"), "utf8"));
const E05F = JSON.parse(fs.readFileSync(path.join(RAIZ, "independente", "esperados_05f.json"), "utf8"));
const COM = F05.comum_adotado, BASE = Object.fromEntries(F05.cenarios.map((c) => [c.id, c]));
const R = (x) => Math.round(x * 100);
const MODS = ["exercicios/capex-calculo", "exercicios/receitas-calculo", "exercicios/viabilidade-calculo"];
function entradas(id, p = {}) {
  const c = BASE[id], s = c.sazonalidade;
  const linhas = Object.fromEntries(Object.entries(COM.linhas_capex_proporcao).map(([k, q]) => [`${k}_valor`, R(c.investimento * q)]));
  const capexV = { unidades: c.unidades, ...linhas, perfil_risco: "primeira", contingencia_pct: p.contingencia_pct ?? 0, custo_fixo: R(c.fixo_mensal), terreno: 0 };
  const rv = { unidades: c.unidades, meses_alta: s ? s.meses_alta : [], meses_baixa: s ? s.meses_baixa : [], deducoes_pct: c.tributos_pct, variavel_noite: 0, custo_estadia: R(c.custo_estadia), permanencia: c.permanencia,
    quebra_pct: p.quebra_pct ?? 0, custo_fixo: R(c.fixo_mensal), horas_semana: p.horas_semana ?? 0, custo_hora: R(p.custo_hora ?? 0), aluguel: R(c.aluguel_mensal), gestao_pct: c.gestao_pct, royalty_pct: c.royalty_pct,
    reserva_pct: p.reserva_pct ?? 0, mes_abertura: c.mes_abertura, outras_pct: E05F.cenarios[c.id].R2_zaios.outras_pct };
  for (const t of s ? ["alta", "media", "baixa"] : ["media"]) { rv[`diaria_${t}`] = R(s ? s.diaria[t] : c.diaria); rv[`ocupacao_${t}`] = s ? s.ocupacao[t] : c.ocupacao; }
  return { capexV, rv, viab: { taxa_desconto: p.taxa_desconto ?? 0.1, multiplo_saida: p.multiplo_saida ?? 6 }, fixo: R(c.fixo_mensal) };
}
function rodar(K, en) {
  const cap = K["exercicios/capex-calculo"], mapa = cap.lerMapaCapex(cap.calcularCapex(en.capexV).paraSalvar);
  const r6 = K["exercicios/receitas-calculo"].calcularReceitas(en.rv, {}, { custoFixoCapex: en.fixo });
  const vb = K["exercicios/viabilidade-calculo"].calcularViabilidade(en.viab, {}, { mapaCapex: mapa, valoresReceitas: en.rv, custoFixoCapex: en.fixo });
  return { r6, vb, mapa };
}
const IGUAIS = (r) => {
  const m = r.r6.modeloP6, a = m.ano, e = r.vb.estudoViabilidade;
  const o = { margemOperacional: m.margemOperacional, ocupacaoMedia: m.ocupacaoMedia, deficit: m.deficit, equilibrio_noites: m.equilibrio.noites, equilibrio_contrib: m.equilibrio.contribuicaoPorNoite,
    primeiro_ano: m.primeiro.map((x) => x.geracaoCaixa), regime: m.regime.map((x) => x.geracaoCaixa), capex: e.capex, fluxo: e.fluxo, vplSem: e.vplSem, tirSem: e.tirSem.taxa,
    paybackSimples: e.paybackSimples.anos, paybackDescontado: e.paybackDescontado.anos, retorno: e.retorno, cenarios_vplSem: e.cenarios.map((c) => c.vplSem), cenarios_payback: e.cenarios.map((c) => c.payback.anos),
    sensibilidade: e.sensibilidade.map((s) => [s.id, s.vpl]), estresse_vpl_capex: e.estresse.vplCapexMaior };
  for (const k of ["noitesVendidas", "diarias", "outras", "receitaBruta", "deducoes", "receitaReal", "custosVariaveis", "margemContribuicao", "custosFixos", "resultadoOperacional", "custosModelo", "ebitda", "reserva", "geracaoCaixa"]) o["ano." + k] = a[k];
  return o;
};
const MUDAM = (r) => { const m = r.r6.modeloP6, e = r.vb.estudoViabilidade; return { selo_p6: r.r6.veredito.selo, giro: m.giro.recomendado, captacao: e.captacao, saida: e.saida, vplCom: e.vplCom, curva_meses: e.curva.com.pontos.length, curva_menor: e.curva.com.menor, colchao: e.colchao, decisao: e.decisao }; };
const igual = (a, b) => JSON.stringify(a, (k, v) => (typeof v === "number" ? Math.round(v * 1e6) / 1e6 : v)) === JSON.stringify(b, (k, v) => (typeof v === "number" ? Math.round(v * 1e6) / 1e6 : v));
(async () => {
  const a = process.argv.slice(2), i = a.indexOf("--saida"), saida = path.resolve(i >= 0 ? a[i + 1] : "resultado-compat");
  const dev = process.env.ZAIOS_SRC_DIR; process.env.ZAIOS_SRC_DIR = process.env.ZAIOS_BASE_DIR;
  const KB = await carregarComposicao(MODS); process.env.ZAIOS_SRC_DIR = dev;
  const KD = await carregarComposicao(MODS);
  if (!KB.ok || !KD.ok) { console.error(KB.motivo || KD.motivo); process.exit(2); }
  const casos = [...["C1", "C2", "C3", "C3E"].map((id) => [id, entradas(id)]), ...G05.cenarios.map((p) => [p.id, entradas(p.base, p)])];
  const linhas = []; let falhasIguais = 0;
  for (const [id, en] of casos) {
    const b = rodar(KB, en), d = rodar(KD, en), ib = IGUAIS(b), id_ = IGUAIS(d);
    for (const k of Object.keys(ib)) { const ok = igual(ib[k], id_[k]); if (!ok) falhasIguais++; linhas.push({ caso: id, campo: k, grupo: "deve ficar igual", resultado: ok ? "IGUAL" : "DIFERENTE" }); }
    const mb = MUDAM(b), md = MUDAM(d);
    for (const k of Object.keys(mb)) linhas.push({ caso: id, campo: k, grupo: "muda por decisão aprovada", base: mb[k], dev: md[k], resultado: igual(mb[k], md[k]) ? "IGUAL" : "MUDOU" });
  }
  // Resultados salvos pela base, lidos pela versão nova (sem recalcular): leitores e dossiê.
  const en = entradas("C2"), b = rodar(KB, en);
  const salvoP6 = JSON.parse(JSON.stringify(b.r6.paraSalvar)), salvoV = JSON.parse(JSON.stringify(b.vb.paraSalvar));
  const leitura = { lerModeloP6: !!KD["exercicios/receitas-calculo"].lerModeloP6(salvoP6), lerEstudoViabilidade: !!KD["exercicios/viabilidade-calculo"].lerEstudoViabilidade(salvoV) };
  // O dossiê depende do cliente Supabase; a leitura de resultados antigos pelo dossiê é conferida no Vitest (compat-dossie.test.ts).
  const dossie = "conferido no Vitest";
  const mudaram = linhas.filter((l) => l.resultado === "MUDOU").length, iguais = linhas.filter((l) => l.grupo === "deve ficar igual");
  fs.mkdirSync(saida, { recursive: true });
  fs.writeFileSync(path.join(saida, "compat_mestre.json"), JSON.stringify({ casos: casos.length, deve_ficar_igual: { total: iguais.length, diferentes: falhasIguais }, mudam_por_decisao: mudaram, leitura, dossie, linhas }, null, 1));
  console.log(`compat: ${casos.length} casos; campos que devem ficar iguais: ${iguais.length - falhasIguais}/${iguais.length} iguais; campos que mudam por decisão: ${mudaram} mudaram; leitores ${JSON.stringify(leitura)}; dossiê: ${dossie}`);
  if (falhasIguais) for (const l of linhas.filter((x) => x.resultado === "DIFERENTE")) console.log("  DIFERENTE:", l.caso, l.campo);
})();

// Comando 05G-B · Teste B · roda a composição da ZAIOS (cópia local, somente leitura) com pró-labore, reserva,
// quebra, contingência, taxas e múltiplos alternativos, e compara com esperados_05g.json. Não altera a ZAIOS.
// Uso: ZAIOS_SRC_DIR=<raiz da cópia> node testes/financeiro/composicao_05g/run_05g.js --saida <pasta>
"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const { carregarComposicao } = require("../lib/zaios_comp");
const RAIZ = path.resolve(__dirname, "..");
const F05 = JSON.parse(fs.readFileSync(path.join(RAIZ, "composicao_05f", "cenarios_05f.json"), "utf8"));
const ENT = JSON.parse(fs.readFileSync(path.join(__dirname, "cenarios_05g.json"), "utf8"));
const ESP = JSON.parse(fs.readFileSync(path.join(__dirname, "esperados_05g.json"), "utf8"));
const E05F = JSON.parse(fs.readFileSync(path.join(RAIZ, "independente", "esperados_05f.json"), "utf8"));
const COM = F05.comum_adotado, BASE = Object.fromEntries(F05.cenarios.map((c) => [c.id, c]));
const R = (x) => Math.round(x * 100);
const TOL = { reais: 0.01, fracao: 1e-6, anos: 1e-6 };
function rodar(K, p) {
  const c = BASE[p.base], s = c.sazonalidade;
  const linhas = Object.fromEntries(Object.entries(COM.linhas_capex_proporcao).map(([k, q]) => [`${k}_valor`, R(c.investimento * q)]));
  const capexV = { unidades: c.unidades, ...linhas, perfil_risco: "primeira", contingencia_pct: p.contingencia_pct, custo_fixo: R(c.fixo_mensal), terreno: 0 };
  const rv = { unidades: c.unidades, meses_alta: s ? s.meses_alta : [], meses_baixa: s ? s.meses_baixa : [], deducoes_pct: c.tributos_pct, variavel_noite: 0,
    custo_estadia: R(c.custo_estadia), permanencia: c.permanencia, quebra_pct: p.quebra_pct, custo_fixo: R(c.fixo_mensal), horas_semana: p.horas_semana, custo_hora: R(p.custo_hora),
    aluguel: R(c.aluguel_mensal), gestao_pct: c.gestao_pct, royalty_pct: c.royalty_pct, reserva_pct: p.reserva_pct, mes_abertura: c.mes_abertura, outras_pct: E05F.cenarios[c.id].R2_zaios.outras_pct };
  for (const t of s ? ["alta", "media", "baixa"] : ["media"]) { rv[`diaria_${t}`] = R(s ? s.diaria[t] : c.diaria); rv[`ocupacao_${t}`] = s ? s.ocupacao[t] : c.ocupacao; }
  const cap = K["exercicios/capex-calculo"];
  const mapa = cap.lerMapaCapex(cap.calcularCapex(capexV).paraSalvar);
  const r6 = K["exercicios/receitas-calculo"].calcularReceitas(rv, {}, { custoFixoCapex: R(c.fixo_mensal) });
  const e = K["exercicios/viabilidade-calculo"].calcularViabilidade({ taxa_desconto: p.taxa_desconto, multiplo_saida: p.multiplo_saida }, {}, { mapaCapex: mapa, valoresReceitas: rv, custoFixoCapex: R(c.fixo_mensal) }).estudoViabilidade;
  const m = r6.modeloP6, a = m.ano, d = (x) => (x == null ? null : x / 100), sens = Object.fromEntries(e.sensibilidade.map((x) => [x.id, d(x.vpl)]));
  return { retirada_mensal: d(m.retirada), receita_bruta: d(a.receitaBruta), custos_variaveis: d(a.custosVariaveis), custos_fixos: d(a.custosFixos), resultado_operacional: d(a.resultadoOperacional),
    custos_modelo: d(a.custosModelo), ebitda: d(a.ebitda), reserva: d(a.reserva), geracao_regime: d(a.geracaoCaixa), geracao_ano1: d(e.geracaoAno1), margem_operacional: m.margemOperacional,
    equilibrio_noites: m.equilibrio.noites, contingencia: d(mapa.contingencia), capex: d(e.capex), deficit_rampa: d(m.deficit), sazonalidade_giro: d(m.giro.sazonalidade), giro_a: d(m.giro.a), giro_b: d(m.giro.b),
    giro: d(e.giro), captacao: d(e.captacao), retorno_anual: e.retorno, retorno_ebitda: e.retornoEbitda, payback_simples: e.paybackSimples.anos, payback_descontado: e.paybackDescontado.anos,
    valor_saida: d(e.saida), vpl_sem: d(e.vplSem), vpl_com: d(e.vplCom), tir_sem: e.tirSem.taxa, tir_com: e.tirCom.taxa, curva_sem_menor: d(e.curva.sem.menor), curva_com_menor: d(e.curva.com.menor),
    curva_com_mes_menor: e.curva.com.mesMenor, curva_com_final: d(e.curva.com.final), colchao: e.colchao, atraso_com_menor: d(e.estresse.atraso.com.menor), estresse_receita_menor: d(e.estresse.geracaoReceitaMenor),
    estresse_vpl_capex_maior: d(e.estresse.vplCapexMaior), conservador: { geracaoRegime: d(e.cenarios[0].geracaoRegime), payback: e.cenarios[0].payback.anos, vplSem: d(e.cenarios[0].vplSem), vplCom: d(e.cenarios[0].vplCom) },
    sensibilidade: sens, passos: e.passos.map((x) => x.resultado), decisao: e.decisao };
}
const plano = (o, pre = "") => Object.entries(o).flatMap(([k, v]) => (v && typeof v === "object" && !Array.isArray(v)) ? plano(v, `${pre}${k}.`) : [[pre + k, v]]);
const tol = (k) => (/margem|retorno|tir_|colchao/.test(k) ? TOL.fracao : /payback/.test(k) ? TOL.anos : /noites|mes_/.test(k) ? 1e-6 : TOL.reais);
const igual = (a, b, t) => (a == null || b == null) ? a == null && b == null : typeof a === "number" ? Math.abs(a - b) <= t : JSON.stringify(a) === JSON.stringify(b);
(async () => {
  const a = process.argv.slice(2), i = a.indexOf("--saida"), saida = path.resolve(i >= 0 ? a[i + 1] : path.join(RAIZ, "resultados", "ultima-05g"));
  const K = await carregarComposicao(["exercicios/capex-calculo", "exercicios/receitas-calculo", "exercicios/viabilidade-calculo"]);
  if (!K.ok) { console.error(K.motivo); process.exit(2); }
  const linhas = [], cont = {};
  for (const p of ENT.cenarios) {
    const ob = Object.fromEntries(plano(rodar(K, p))), es = Object.fromEntries(plano(ESP.cenarios[p.id]));
    for (const [k, v] of Object.entries(ob)) {
      if (!(k in es)) continue;
      const cls = !igual(v, es[k], tol(k)) ? "DIVERGÊNCIA MATEMÁTICA" : es[k] == null ? "NÃO APLICÁVEL" : "OK";
      linhas.push({ cenario: p.id, campo: k, esperado: es[k], zaios: v, diferenca: typeof v === "number" && typeof es[k] === "number" ? v - es[k] : null, classificacao: cls });
      cont[p.id] = cont[p.id] || {}; cont[p.id][cls] = (cont[p.id][cls] || 0) + 1;
    }
  }
  const h = (s) => crypto.createHash("sha256").update(s).digest("hex");
  fs.mkdirSync(saida, { recursive: true });
  fs.writeFileSync(path.join(saida, "resultado_05g.json"), JSON.stringify({ geradoEm: new Date().toISOString(), tolerancias: TOL, fontesZaios: Object.fromEntries(Object.entries(K.fontes).map(([k, s]) => [k, h(s)])), contagem: cont, linhas }, null, 1));
  let md = `# Resultado · Comando 05G-B · Teste B\n\nGerado em ${new Date().toISOString()}. Tolerâncias: R$ 0,01; frações, anos e noites 0,000001.\n\n| Cenário | OK | Divergência matemática | Não aplicável |\n|---|---|---|---|\n`;
  for (const [c, n] of Object.entries(cont)) md += `| ${c} | ${n["OK"] || 0} | ${n["DIVERGÊNCIA MATEMÁTICA"] || 0} | ${n["NÃO APLICÁVEL"] || 0} |\n`;
  const f = (v) => v == null ? "nulo" : typeof v === "number" ? (Math.abs(v) < 10 ? v.toFixed(6) : v.toFixed(2)) : Array.isArray(v) ? v.join(", ") : String(v);
  for (const p of ENT.cenarios) { md += `\n## ${p.id} · ${p.descricao}\n\n| Campo | Esperado (independente) | ZAIOS | Diferença | Classificação |\n|---|---|---|---|---|\n`;
    for (const l of linhas.filter((x) => x.cenario === p.id)) md += `| ${l.campo} | ${f(l.esperado)} | ${f(l.zaios)} | ${l.diferenca == null ? "—" : l.diferenca.toExponential(1)} | ${l.classificacao} |\n`; }
  fs.writeFileSync(path.join(saida, "RESULTADO_05G_TESTE_B.md"), md);
  console.log(JSON.stringify(cont)); for (const l of linhas) if (l.classificacao === "DIVERGÊNCIA MATEMÁTICA") console.log("DIV", l.cenario, l.campo, l.esperado, l.zaios);
})();

// Comando 05F · Executa a composição da ZAIOS (cópia local, somente leitura) nos 3 cenários + estresse
// e compara com os esperados independentes (independente/esperados_05f.json). Não altera a ZAIOS.
// Uso: ZAIOS_SRC_DIR=<raiz da cópia> node testes/financeiro/composicao_05f/run_05f.js --saida <pasta>
"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const { carregarComposicao } = require("../lib/zaios_comp");
const RAIZ = path.resolve(__dirname, "..");
const ENT = JSON.parse(fs.readFileSync(path.join(__dirname, "cenarios_05f.json"), "utf8"));
const ESP = JSON.parse(fs.readFileSync(path.join(RAIZ, "independente", "esperados_05f.json"), "utf8"));
const TOL = { reais: 0.01, fracao: 1e-6, anos: 1e-6, noites: 1e-6 };
const R = (x) => Math.round(x * 100); // reais → centavos (todas as entradas são exatas em centavos)
const COM = ENT.comum_adotado;

function valores(c) {
  const linhas = Object.fromEntries(Object.entries(COM.linhas_capex_proporcao).map(([k, p]) => [`${k}_valor`, R(c.investimento * p)]));
  const capexV = { unidades: c.unidades, ...linhas, perfil_risco: COM.perfil_risco, contingencia_pct: COM.contingencia_pct, custo_fixo: R(c.fixo_mensal), terreno: R(COM.terreno) };
  const s = c.sazonalidade;
  const temp = (t) => (s ? s : { diaria: { [t]: c.diaria }, ocupacao: { [t]: c.ocupacao } });
  const receitasV = {
    unidades: c.unidades, meses_alta: s ? s.meses_alta : [], meses_baixa: s ? s.meses_baixa : [],
    deducoes_pct: c.tributos_pct, variavel_noite: R(COM.variavel_noite), custo_estadia: R(c.custo_estadia), permanencia: c.permanencia,
    quebra_pct: COM.quebra_pct, custo_fixo: R(c.fixo_mensal), horas_semana: COM.horas_semana, custo_hora: R(COM.custo_hora),
    aluguel: R(c.aluguel_mensal), gestao_pct: c.gestao_pct, royalty_pct: c.royalty_pct, reserva_pct: COM.reserva_pct, mes_abertura: c.mes_abertura,
    outras_pct: ESP.cenarios[c.id].R2_zaios.outras_pct,
  };
  for (const t of s ? ["alta", "media", "baixa"] : ["media"]) { receitasV[`diaria_${t}`] = R(temp(t).diaria[t]); receitasV[`ocupacao_${t}`] = temp(t).ocupacao[t]; }
  return { capexV, receitasV, viabV: { taxa_desconto: COM.taxa_desconto, multiplo_saida: COM.multiplo_saida } };
}

function executar(K, c) {
  const { capexV, receitasV, viabV } = valores(c);
  const cap = K["exercicios/capex-calculo"], rec = K["exercicios/receitas-calculo"], via = K["exercicios/viabilidade-calculo"];
  const mapa = cap.lerMapaCapex(cap.calcularCapex(capexV).paraSalvar);
  const r6 = rec.calcularReceitas(receitasV, {}, { custoFixoCapex: R(c.fixo_mensal) });
  const vb = via.calcularViabilidade(viabV, {}, { mapaCapex: mapa, valoresReceitas: receitasV, custoFixoCapex: R(c.fixo_mensal) });
  const m = r6.modeloP6, a = m.ano, p1 = m.totalPrimeiro, e = vb.estudoViabilidade, d = (x) => (x == null ? null : x / 100);
  const sens = Object.fromEntries(e.sensibilidade.map((s) => [s.id, d(s.vpl)]));
  const cen = (i) => ({ geracaoRegime: d(e.cenarios[i].geracaoRegime), geracaoAno1: d(e.cenarios[i].geracaoAno1), ebitdaRegime: d(e.cenarios[i].ebitdaRegime), payback: e.cenarios[i].payback.anos, vplSem: d(e.cenarios[i].vplSem), vplCom: d(e.cenarios[i].vplCom) });
  return {
    obtido: {
      receita_hospedagem: d(a.diarias), noites_vendidas: a.noitesVendidas, outras: d(a.outras), receita_bruta: d(a.receitaBruta), tributos: d(a.deducoes),
      custos_variaveis: d(a.custosVariaveis), estadias: c.custo_estadia > 0 ? a.custosVariaveis / R(c.custo_estadia) : null,
      custos_fixos: d(a.custosFixos), resultado_operacional: d(a.resultadoOperacional), custos_modelo: d(a.custosModelo),
      aluguel: d(R(c.aluguel_mensal) * 12), gestao_royalty: d(a.custosModelo - R(c.aluguel_mensal) * 12),
      ebitda: d(a.ebitda), geracao_regime: d(a.geracaoCaixa),
      receita_bruta_ano1: d(p1.receitaBruta), ebitda_ano1: d(p1.ebitda), geracao_ano1: d(p1.geracaoCaixa),
      meses_negativos_regime: m.regime.filter((x) => x.geracaoCaixa < 0).length, pior_mes_regime: d(Math.min(...m.regime.map((x) => x.geracaoCaixa))),
      ocupacao_media: m.ocupacaoMedia, margem_operacional: m.margemOperacional, regua_margem: m.regua, selo_p6: r6.veredito.selo,
      equilibrio_contribuicao_noite: d(m.equilibrio.contribuicaoPorNoite), equilibrio_noites: m.equilibrio.noites, equilibrio_ocupacao: m.equilibrio.ocupacao, equilibrio_folga: m.equilibrio.folga,
      capex: d(e.capex), deficit_rampa: d(m.deficit), sazonalidade_giro: d(m.giro.sazonalidade), giro_a: d(m.giro.a), giro_b: d(m.giro.b), giro: d(e.giro), captacao: d(e.captacao),
      retorno_anual: e.retorno, retorno_ebitda: e.retornoEbitda, payback_simples: e.paybackSimples.anos, payback_descontado: e.paybackDescontado.anos,
      valor_saida: d(e.saida), vpl_sem: d(e.vplSem), vpl_com: d(e.vplCom), tir_sem: e.tirSem.taxa, tir_com: e.tirCom.taxa, tir_com_varias: e.tirCom.podeTerMaisDeUma,
      mes_abertura_projeto: e.mesAberturaProjeto, curva_menor: d(e.curva.com.menor), curva_mes_menor: e.curva.com.mesMenor, curva_final: d(e.curva.com.final), colchao: e.colchao,
      atraso_menor: d(e.estresse.atraso.com.menor), estresse_receita_menor: d(e.estresse.geracaoReceitaMenor), estresse_capex_maior: d(e.estresse.capexMaior),
      estresse_vpl_capex_maior: d(e.estresse.vplCapexMaior), estresse_payback_capex_maior: e.estresse.paybackCapexMaior.anos,
      conservador: cen(0), otimista: cen(2), sensibilidade: sens, passos: e.passos.map((p) => p.resultado), decisao: e.decisao,
    },
    textos: {
      veredito_viabilidade: vb.veredito, veredito_p6: r6.veredito, payback_motivo: e.paybackSimples.motivo, payback_desc_motivo: e.paybackDescontado.motivo,
      tir_sem_motivo: e.tirSem.motivo, tir_com_motivo: e.tirCom.motivo, alertas_viabilidade: vb.alertas, alertas_p6: r6.alertas, curva_sem_menor: d(e.curva.sem.menor),
      retorno_com_terreno: e.retornoComTerreno, contingencia: d(mapa.contingencia), cronograma: mapa.cronograma.map((x) => d(x.valor)),
    },
  };
}

const ROTULO = {
  receita_hospedagem: "Receita de hospedagem", noites_vendidas: "Diárias ocupadas (noites vendidas)", estadias: "Estadias (derivado: custos variáveis ÷ custo por estadia)",
  outras: "Outras receitas", receita_bruta: "Receita bruta consolidada", tributos: "Tributos sobre vendas (deduções)", custos_variaveis: "Custos variáveis",
  custos_fixos: "Custos fixos", resultado_operacional: "Resultado operacional (antes dos custos do modelo)", aluguel: "Aluguel (12 × mensal)",
  gestao_royalty: "Gestão + royalties (derivado: custos do modelo − aluguel)", custos_modelo: "Custos do modelo", ebitda: "EBITDA do regime", geracao_regime: "Geração de caixa do regime",
  receita_bruta_ano1: "Receita bruta do 1º ano (rampa)", ebitda_ano1: "EBITDA do 1º ano", geracao_ano1: "Geração do 1º ano", meses_negativos_regime: "Meses com geração negativa no regime",
  pior_mes_regime: "Pior mês do regime", ocupacao_media: "Ocupação média anual (ponderada pelos dias)", margem_operacional: "Margem operacional (antes dos custos do modelo)",
  regua_margem: "Régua de margem do P6", selo_p6: "Selo do P6 Receitas", equilibrio_contribuicao_noite: "Equilíbrio: contribuição por noite", equilibrio_noites: "Equilíbrio: noites/ano",
  equilibrio_ocupacao: "Equilíbrio: ocupação", equilibrio_folga: "Equilíbrio: folga de ocupação", capex: "Capital investido (CAPEX)", deficit_rampa: "Déficit acumulado da rampa",
  sazonalidade_giro: "Soma dos meses negativos do regime (giro)", giro_a: "Capital de giro A (6 × fixo)", giro_b: "Capital de giro B", giro: "Capital de giro usado",
  captacao: "Captação (CAPEX + giro)", retorno_anual: "Retorno anual (geração ÷ CAPEX)", retorno_ebitda: "Retorno do EBITDA", payback_simples: "Payback simples (anos)",
  payback_descontado: "Payback descontado (anos)", valor_saida: "Valor de saída (6 × EBITDA)", vpl_sem: "VPL sem saída (10%)", vpl_com: "VPL com saída", tir_sem: "TIR sem saída",
  tir_com: "TIR com saída", tir_com_varias: "Aviso de mais de uma TIR (com saída)", mes_abertura_projeto: "Mês do projeto em que abre", curva_menor: "Menor saldo da curva (36 meses)",
  curva_mes_menor: "Mês do menor saldo", curva_final: "Saldo no mês 36", colchao: "Colchão (menor saldo ÷ CAPEX)", atraso_menor: "Menor saldo com atraso de 6 meses",
  estresse_receita_menor: "Estresse interno: geração com receita 30% menor", estresse_capex_maior: "Estresse interno: CAPEX +25%", estresse_vpl_capex_maior: "VPL com CAPEX +25%",
  estresse_payback_capex_maior: "Payback com CAPEX +25%", passos: "Régua: 5 passos", decisao: "Régua: decisão",
};
const R1_CAMPOS = new Set(["receita_hospedagem", "outras", "receita_bruta", "tributos", "custos_variaveis", "custos_fixos", "aluguel", "gestao_royalty", "custos_modelo", "ebitda", "geracao_regime", "giro", "captacao", "retorno_anual", "vpl_sem", "payback_simples", "tir_sem"]);
function tolDe(k) {
  if (/ocupacao|margem|retorno|tir_|colchao|folga/.test(k)) return TOL.fracao;
  if (/payback/.test(k)) return TOL.anos;
  if (/noites|estadias|meses_|mes_/.test(k)) return TOL.noites;
  return TOL.reais;
}
const igual = (a, b, t) => (a == null || b == null) ? a == null && b == null : (typeof a === "number" && typeof b === "number") ? Math.abs(a - b) <= t : JSON.stringify(a) === JSON.stringify(b);
const dif = (a, b) => (typeof a === "number" && typeof b === "number") ? a - b : null;

function comparar(id, ob) {
  const r2 = ESP.cenarios[id].R2_zaios, r1 = ESP.cenarios[id].R1_comando, linhas = [];
  const plano = (o, pre = "") => Object.entries(o).flatMap(([k, v]) => (v && typeof v === "object" && !Array.isArray(v)) ? plano(v, `${pre}${k}.`) : [[pre + k, v]]);
  const e2 = Object.fromEntries(plano(r2)), e1 = Object.fromEntries(plano(r1));
  for (const [k, v] of plano(ob)) {
    if (!(k in e2)) continue;
    const t = tolDe(k), okR2 = igual(v, e2[k], t);
    let cls;
    if (!okR2) cls = "DIVERGÊNCIA MATEMÁTICA";
    else if (e2[k] == null) cls = "NÃO APLICÁVEL";
    else if (R1_CAMPOS.has(k) && !igual(v, e1[k], t)) cls = "DIVERGÊNCIA METODOLÓGICA";
    else cls = "OK";
    linhas.push({ cenario: id, campo: k, rotulo: ROTULO[k] || k, tolerancia: typeof v === "number" || v == null ? t : null, esperado_R2: e2[k], esperado_R1: R1_CAMPOS.has(k) ? e1[k] : "(não definido pelo comando)", zaios: v, diferenca_R2: dif(v, e2[k]), diferenca_R1: R1_CAMPOS.has(k) ? dif(v, e1[k]) : null, classificacao: cls });
  }
  return linhas;
}

(async () => {
  const args = process.argv.slice(2), i = args.indexOf("--saida");
  const saida = path.resolve(i >= 0 ? args[i + 1] : path.join(RAIZ, "resultados", "ultima-05f"));
  const K = await carregarComposicao(["exercicios/capex-calculo", "exercicios/receitas-calculo", "exercicios/viabilidade-calculo"]);
  if (!K.ok) { console.error("Composição da ZAIOS indisponível: " + K.motivo); process.exit(2); }
  const hash = (s) => crypto.createHash("sha256").update(s).digest("hex");
  const out = { geradoEm: new Date().toISOString(), comando: "05F", tolerancias: TOL, fontesZaios: Object.fromEntries(Object.entries(K.fontes).map(([k, s]) => [k, hash(s)])), entradas: hash(fs.readFileSync(path.join(__dirname, "cenarios_05f.json"))), esperados: hash(fs.readFileSync(path.join(RAIZ, "independente", "esperados_05f.json"))), cenarios: {}, linhas: [] };
  for (const c of ENT.cenarios) {
    const r = executar(K, c);
    out.cenarios[c.id] = { textos: r.textos, entradas_zaios: valores(c) };
    out.linhas.push(...comparar(c.id, r.obtido));
  }
  const cont = {};
  for (const l of out.linhas) { cont[l.cenario] = cont[l.cenario] || {}; cont[l.cenario][l.classificacao] = (cont[l.cenario][l.classificacao] || 0) + 1; }
  out.contagem = cont;
  fs.mkdirSync(saida, { recursive: true });
  fs.writeFileSync(path.join(saida, "resultado_05f.json"), JSON.stringify(out, null, 1));
  const f = (v) => v == null ? "nulo" : typeof v === "number" ? (Number.isInteger(v) ? String(v) : v.toFixed(Math.abs(v) < 10 ? 6 : 2)) : Array.isArray(v) ? `[${v.join(", ")}]` : String(v);
  let md = `# Resultado da execução · Comando 05F\n\nGerado por \`run_05f.js\` em ${out.geradoEm}. Tolerâncias: R$ 0,01; frações, anos e noites 0,000001.\n\n`;
  md += "Hashes SHA-256 das fontes da ZAIOS carregadas (cópia local, fora do repositório):\n\n" + Object.entries(out.fontesZaios).map(([k, h]) => `- \`src/${k}.ts\`: \`${h.slice(0, 16)}\``).join("\n") + `\n\nEntradas: \`${out.entradas.slice(0, 16)}\` · Esperados: \`${out.esperados.slice(0, 16)}\`\n\n## Contagem\n\n| Cenário | ${["OK", "DIVERGÊNCIA METODOLÓGICA", "DIVERGÊNCIA MATEMÁTICA", "NÃO APLICÁVEL"].join(" | ")} |\n|---|---|---|---|---|\n`;
  for (const [c, n] of Object.entries(cont)) md += `| ${c} | ${["OK", "DIVERGÊNCIA METODOLÓGICA", "DIVERGÊNCIA MATEMÁTICA", "NÃO APLICÁVEL"].map((k) => n[k] || 0).join(" | ")} |\n`;
  for (const c of ENT.cenarios) {
    md += `\n## ${c.id} · ${c.nome}\n\n| Campo | Esperado R2 (regra da ZAIOS) | Esperado R1 (regra do comando) | ZAIOS | Diferença (R2) | Diferença (R1) | Classificação |\n|---|---|---|---|---|---|---|\n`;
    for (const l of out.linhas.filter((x) => x.cenario === c.id)) md += `| ${l.rotulo} | ${f(l.esperado_R2)} | ${typeof l.esperado_R1 === "string" ? "—" : f(l.esperado_R1)} | ${f(l.zaios)} | ${l.diferenca_R2 == null ? "—" : l.diferenca_R2.toExponential(1)} | ${l.diferenca_R1 == null ? "—" : f(l.diferenca_R1)} | ${l.classificacao} |\n`;
  }
  fs.writeFileSync(path.join(saida, "RESULTADO_05F.md"), md);
  console.log(JSON.stringify(cont, null, 1));
})();

// Testes complementares da ZAIOS (Comando 05E): composição (src/exercicios), EBITDA com custos do modelo,
// outras receitas, custo por estadia, sazonalidade, G2/G3. Esperados: independente/esperados_complementares.json
// e exemplos documentados no FORMULAS.md da ZAIOS (texto). Só dados de entrada aparecem aqui; nenhum código da ZAIOS.
"use strict";
const path = require("path"), fs = require("fs");
const { TOL, TIPO } = require("../lib/base"), U = require("./_util");
const X = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "independente", "esperados_complementares.json"), "utf8"));
const R = U.R;
module.exports = (D) => {
  const c = [], Z = D.zaios, C = () => D.zaiosComp;
  const add = (o) => c.push(Object.assign({ teste: "C" }, o));
  // ---------- Primitivas: EBITDA com custos do modelo, outras receitas, estadia, sazonalidade ----------
  const pm = (o) => Object.assign(U.paramsP6(Object.assign({}, E0, o)), o.extra || {});
  const E0 = { unidades: 3, diaria: 680, ocupacao: 0.38, deducoes: 0.17, variavelNoite: 80, fixoMensal: 6000 };
  const ano = (p) => Z.receitas.somarMeses(Z.receitas.anoRegime(p));
  const pModelo = () => pm({ quebra: 0.01, reserva: 0.04, extra: { aluguel: R(1000), gestaoPct: 0.10, royaltyPct: 0.03 } });
  for (const [k, ind] of [["custosModelo", "Custos do modelo (aluguel R$ 1.000/mês + gestão 10% + royalty 3%)"], ["ebitda", "EBITDA com custos do modelo"], ["geracaoCaixa", "Geração de caixa com custos do modelo e reserva de 4%"], ["resultadoOperacional", "Resultado operacional (antes dos custos do modelo)"]])
    add({ id: `C-ZAIOS-M-${k}`, ferramenta: "ZAIOS", indicador: ind, decisao: "v0", tipo: TIPO.FORMULA, esperado: X.zaios_modelo[k === "geracaoCaixa" ? "geracao" : k], tol: TOL.reais, requer: "zaios", obter: () => ano(pModelo())[k] / 100 });
  const pOE = () => pm({ extra: { outrasPct: 0.10, custoEstadia: R(60), permanencia: 2.5 } });
  for (const [k, ind] of [["receitaBruta", "Receita bruta com outras receitas de 10%"], ["custosVariaveis", "Custos variáveis com custo por estadia (R$ 60, permanência 2,5)"], ["resultadoOperacional", "Resultado operacional com outras receitas e estadia"]])
    add({ id: `C-ZAIOS-O-${k}`, ferramenta: "ZAIOS", indicador: ind, decisao: "v0", tipo: TIPO.FORMULA, esperado: X.zaios_outras_estadia[k === "receitaBruta" ? "receitaBruta" : k === "custosVariaveis" ? "custosVariaveis" : "resultadoOperacional"], tol: TOL.reais, requer: "zaios", obter: () => ano(pOE())[k] / 100 });
  const pSaz = () => { const p = pm({}); p.temporadaDoMes = ["alta", "alta", "media", "baixa", "baixa", "baixa", "media", "media", "media", "media", "media", "alta"]; p.diaria = { alta: R(900), media: R(680), baixa: R(500) }; p.ocupacao = { alta: 0.6, media: 0.38, baixa: 0.2 }; return p; };
  add({ id: "C-ZAIOS-S-1", ferramenta: "ZAIOS", indicador: "Receita bruta com sazonalidade (alta dez–fev, baixa abr–jun)", decisao: "v0", tipo: TIPO.FORMULA, esperado: X.zaios_sazonal.bruta, tol: TOL.reais, requer: "zaios", obter: () => ano(pSaz()).receitaBruta / 100 });
  add({ id: "C-ZAIOS-S-2", ferramenta: "ZAIOS", indicador: "Resultado operacional com sazonalidade", decisao: "v0", tipo: TIPO.FORMULA, esperado: X.zaios_sazonal.op, tol: TOL.reais, requer: "zaios", obter: () => ano(pSaz()).resultadoOperacional / 100 });
  // ---------- Composição: P5 + P6 Receitas + P6 Viabilidade (entradas dos testes da própria ZAIOS) ----------
  const capexV = { unidades: 3, infra_valor: R(250000), projeto_valor: R(70000), obra_valor: R(390000), apoio_valor: R(90000), ffe_valor: R(195000), ose_valor: R(23400), pre_valor: R(36500), perfil_risco: "primeira", contingencia_pct: 0.25, custo_fixo: R(10500), terreno: R(200000) };
  const receitasV = { unidades: 3, meses_alta: [], meses_baixa: [], diaria_media: R(680), ocupacao_media: 0.38, outras_pct: 0, deducoes_pct: 0.17, variavel_noite: 0, custo_estadia: 0, quebra_pct: 0, custo_fixo: R(10500), horas_semana: 0, custo_hora: 0, reserva_pct: 0, mes_abertura: "Janeiro" };
  const viab = { taxa_desconto: 0.1, multiplo_saida: 6 };
  const estudo = () => { const K = C(); const ctx = { mapaCapex: K["exercicios/capex-calculo"].lerMapaCapex(K["exercicios/capex-calculo"].calcularCapex(capexV).paraSalvar), valoresReceitas: receitasV, custoFixoCapex: R(10500) };
    return K["exercicios/viabilidade-calculo"].calcularViabilidade(viab, {}, ctx); };
  const e = () => estudo().estudoViabilidade, Xc = X.zaios_composicao;
  const comp = [
    ["mesAberturaProjeto", "Mês de abertura sugerido pelo cronograma do P5", () => e().mesAberturaProjeto, Xc.mesAberturaSugerido, 0],
    ["geracaoAno1", "Geração do 1º ano (rampa a partir de janeiro)", () => e().geracaoAno1 / 100, Xc.geracaoAno1, TOL.reais],
    ["geracaoRegime", "Geração do ano de regime", () => e().geracaoRegime / 100, Xc.geracaoRegime, TOL.reais],
    ["giro", "Capital de giro recomendado (o maior entre A = 6 × fixo e B)", () => e().giro / 100, Xc.giroRecomendado, TOL.reais],
    ["captacao", "Captação = CAPEX + capital de giro", () => e().captacao / 100, Xc.captacao, TOL.reais],
    ["retorno", "Retorno anual sobre o investimento", () => e().retorno, Xc.retornoAnual, TOL.pct],
    ["vplSem", "VPL sem saída a 10%", () => e().vplSem / 100, Xc.vplSem10, TOL.reais],
    ["vplCom", "VPL com saída 6× EBITDA", () => e().vplCom / 100, Xc.vplCom10, TOL.reais],
    ["payback", "Payback simples (estendido)", () => e().paybackSimples.anos, Xc.paybackSimples, TOL.anos],
    ["conservador", "Geração do regime no cenário conservador", () => e().cenarios[0].geracaoRegime / 100, Xc.geracaoConservador, TOL.reais],
    ["estresseReceita", "Estresse: geração com receita 30% menor", () => e().estresse.geracaoReceitaMenor / 100, Xc.estresseReceitaMenor, TOL.reais],
    ["capexMaior", "Estresse: CAPEX 25% maior", () => e().estresse.capexMaior / 100, Xc.capexMaior, TOL.reais],
    ["menorSaldo", "Menor saldo da curva de caixa com a contingência usada", () => e().curva.com.menor / 100, Xc.menorSaldoComContingencia, TOL.reais],
    ["colchao", "Colchão = menor saldo ÷ CAPEX", () => e().colchao, Xc.colchao, TOL.pct],
    ["passos", "Resultado dos 5 passos", () => e().passos.map((p) => p.resultado), Xc.passos, 0],
    ["decisao", "Decisão pela regra dos 5 passos", () => e().decisao, Xc.decisao, 0],
  ];
  for (const [k, ind, f, esp, tol] of comp) add({ id: `C-ZAIOS-C-${k}`, ferramenta: "ZAIOS (composição)", indicador: ind, decisao: k === "passos" || k === "decisao" ? "D11-A (lógica)" : "v0", tipo: TIPO.FORMULA, esperado: esp, tol, requer: "zaiosComp", obter: f });
  add({ id: "C-ZAIOS-C-veredito", ferramenta: "ZAIOS (composição)", indicador: "Veredito só após homologação (o selo hoje é exibido)", decisao: "D11-A", tipo: TIPO.DIVERGENCIA, esperado: "sem selo antes da homologação", requer: "zaiosComp",
    nota: "calcularViabilidade devolve o selo Avançar/Ajustar/Redesenhar sem trava de homologação.", obter: () => estudo().veredito.selo });
  // ---------- G2 e G3 (exemplos documentados no FORMULAS.md da ZAIOS) ----------
  const L = (m, tipo, categoria, v) => ({ mes: m, tipo, categoria, valor_centavos: v });
  const lancs = [L("2026-10", "receita", "hospedagem", 100000), L("2026-10", "receita", "taxa_limpeza", 10000), L("2026-10", "receita", "extras", 20000),
    L("2026-10", "despesa", "comissoes", 13000), L("2026-10", "despesa", "equipe", 30000), L("2026-10", "despesa", "limpeza", 7000)];
  const G = () => C()["exercicios/financas-calculo"];
  const r = () => G().resumoMes(lancs, "2026-10");
  for (const [k, ind, esp, tol] of [["receitaBruta", "G2 · Receita bruta (centavos)", 130000, 0.5], ["comissoes", "G2 · Comissões (centavos)", 13000, 0.5], ["receitaLiquida", "G2 · Receita líquida de distribuição (centavos)", 117000, 0.5], ["fixas", "G2 · Despesas fixas (centavos)", 30000, 0.5], ["variaveis", "G2 · Despesas variáveis sem comissões (centavos)", 7000, 0.5], ["despesas", "G2 · Despesas totais (centavos)", 50000, 0.5], ["resultado", "G2 · Resultado gerencial (centavos)", 80000, 0.5]])
    add({ id: `C-G2-${k}`, ferramenta: "ZAIOS (G2)", indicador: ind, decisao: "v0", tipo: TIPO.FORMULA, esperado: esp, tol, requer: "zaiosComp", obter: () => r()[k] });
  add({ id: "C-G2-margem", ferramenta: "ZAIOS (G2)", indicador: "G2 · Margem gerencial (80.000 ÷ 130.000)", decisao: "v0", tipo: TIPO.FORMULA, esperado: 80000 / 130000, tol: 1e-9, requer: "zaiosComp", obter: () => r().margem.valor });
  const lancsRes = [L("2026-08", "despesa", "equipe", 20000), L("2026-09", "despesa", "equipe", 30000), L("2026-10", "despesa", "equipe", 40000)];
  add({ id: "C-G2-cobertura", ferramenta: "ZAIOS (G2)", indicador: "G2 · Cobertura da reserva (90.000 ÷ média de 20.000, 30.000, 40.000)", decisao: "v0 (D12 pendente)", tipo: TIPO.FORMULA, esperado: 3, tol: 1e-9, requer: "zaiosComp", obter: () => G().reservaCobre(lancsRes, 90000).valor });
  const ocup = [{ mes: "2026-10", noites_vendidas: 20, dias_abertos: 30, unidades: 2 }];
  const ind = () => G().indicadoresMes(lancs, ocup, "2026-10");
  for (const [k, txt, esp, tol] of [["noitesDisponiveis", "G3 · Noites disponíveis (2 × 30)", 60, 1e-9], ["ocupacao", "G3 · Ocupação (20 ÷ 60)", 20 / 60, 1e-9], ["diariaMedia", "G3 · Diária média (hospedagem 100.000 ÷ 20, sem taxa de limpeza)", 5000, 0.5], ["revpar", "G3 · RevPAR (100.000 ÷ 60)", 100000 / 60, 0.5], ["trevpar", "G3 · TRevPAR (130.000 ÷ 60)", 130000 / 60, 0.5], ["despesaPorNoite", "G3 · Despesa por noite vendida (50.000 ÷ 20)", 2500, 0.5]])
    add({ id: `C-G3-${k}`, ferramenta: "ZAIOS (G3)", indicador: txt, decisao: "v0", tipo: TIPO.FORMULA, esperado: esp, tol, requer: "zaiosComp", obter: () => ind()[k].valor });
  add({ id: "C-G3-bissexto", ferramenta: "ZAIOS (G3)", indicador: "Dias de fevereiro de 2028 (ano bissexto)", decisao: "v0", tipo: TIPO.FORMULA, esperado: 29, requer: "zaiosComp", obter: () => C()["calc/operacao"].diasNoMes("2028-02") });
  add({ id: "C-G2-impostos", ferramenta: "ZAIOS (G2)", indicador: "Impostos sobre a receita tratados como dedução (dicionário), não como despesa variável", decisao: "O7 (a classificar)", tipo: TIPO.LIMITACAO, esperado: "deducao", requer: "zaiosComp",
    nota: "Na G2 a categoria 'impostos' tem natureza variável.", obter: () => G().natureza("impostos") === "variavel" ? "despesa variável" : "deducao" });
  return c;
};

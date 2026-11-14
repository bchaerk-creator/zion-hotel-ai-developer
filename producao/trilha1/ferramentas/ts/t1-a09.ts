// Trilha 1 · Aula 9 · Viabilidade (slug 1-9). Fonte: exercicios/aula-09.json.
import type { Calculo, ResultadoCalculos, Respostas, Veredito } from "./types";
import { MESES, MESES_NOME, brl, div, escolha, fechar, fmtN, fmtPct, juntar, lista, num, pct, tetoMultiplo } from "./util";

const RAMPAS: Record<string, [number, number, number]> = {
  escola: [0.4, 0.5, 0.75],
  piso: [0.25, 0.45, 0.65],
  teto: [0.4, 0.6, 0.85],
};
const FATOR = 0.82; // 1 - 17% de deduções - 1% de quebra, como na fonte

export function calcular(r: Respostas): ResultadoCalculos {
  const calculos: Calculo[] = [];
  const cP = num(r, "capex_piso"), cT = num(r, "capex_teto");
  const u = num(r, "unidades"), d = num(r, "diaria_media");
  const contrib = num(r, "contribuicao_noite"), fixo = num(r, "fixo_completo_mes");
  const oA = pct(r, "ocup_alta"), oM = pct(r, "ocup_media"), oV = pct(r, "ocup_vale");
  const alta = lista(r, "meses_alta", MESES), vale = lista(r, "meses_vale", MESES);
  const abertura = escolha(r, "mes_abertura");
  const iAbre = abertura === null ? -1 : (MESES as readonly string[]).indexOf(abertura);
  const rampa = escolha(r, "rampa");
  const fat = rampa !== null && RAMPAS[rampa] ? RAMPAS[rampa] : null;

  // 1. regime
  const base = u !== null && contrib !== null && fixo !== null && oA !== null && oM !== null && oV !== null;
  const noitesReg: (number | null)[] = [];
  const resReg: (number | null)[] = [];
  const conflito = alta.filter((m) => vale.includes(m));
  for (let m = 0; m < 12; m++) {
    const k = MESES[m];
    const oc = alta.includes(k) ? oA : vale.includes(k) ? oV : oM; // mês marcado nas duas listas conta como alta
    const n = base ? (u as number) * 30 * (oc as number) : null;
    noitesReg.push(n);
    resReg.push(n !== null ? n * (contrib as number) - (fixo as number) : null);
  }
  const sobra = base ? (resReg as number[]).reduce((s, x) => s + x, 0) : null;
  const noitesRegAno = base ? (noitesReg as number[]).reduce((s, x) => s + x, 0) : null;
  {
    let t: string;
    if (!base) t = "Faltam unidades, contribuição por noite, fixo completo ou as ocupações de regime.";
    else {
      t = `No ano de regime, a operação deixa ${brl(sobra as number)} depois do fixo completo (${fmtN(noitesRegAno as number, 1)} noites).`;
      const neg = MESES.filter((_, i) => (resReg[i] as number) < 0);
      t += neg.length ? ` Meses que não fecham: ${juntar(neg.map((k) => k))}.` : " Todos os meses fecham.";
      if (conflito.length) t += ` Aviso: ${juntar(conflito)} marcado(s) como alta e vale; contou como alta.`;
    }
    const det: Record<string, number | null> = {};
    MESES.forEach((k, i) => { det[`resultado_${k}`] = resReg[i]; });
    calculos.push({ id: "regime", rotulo: "O ano de regime, mês a mês", valor: sobra, texto: t, alerta: sobra !== null && sobra < 0 ? "critico" : undefined, detalhes: { noites_regime_ano: noitesRegAno, ...det } });
  }

  // 2. ano1
  const okAno1 = base && fat !== null && iAbre >= 0;
  const noites1: number[] = [], res1: number[] = [], mesIdx: number[] = [];
  if (okAno1) {
    for (let i = 1; i <= 12; i++) {
      const m = (iAbre + i - 1) % 12;
      const f = i <= 3 ? fat![0] : i <= 6 ? fat![1] : fat![2];
      const n = (noitesReg[m] as number) * f;
      noites1.push(n); res1.push(n * (contrib as number) - (fixo as number)); mesIdx.push(m);
    }
  }
  const ano1 = okAno1 ? res1.reduce((s, x) => s + x, 0) : null;
  let fundo: number | null = null, fundoMes = "";
  if (okAno1) { fundo = Math.min(...res1); fundoMes = MESES_NOME[mesIdx[res1.indexOf(fundo)]]; }
  calculos.push({
    id: "ano1", rotulo: "O ano 1 com a rampa", valor: ano1,
    texto: ano1 === null
      ? `Para o ano 1 falta ${juntar([!base && "o ano de regime", fat === null && "a rampa", iAbre < 0 && "o mês de abertura"].filter(Boolean) as string[])}.`
      : `Com a rampa ${rampa} (${fat!.map((x) => fmtPct(x, 0)).join(", ")} do regime) e abertura em ${MESES_NOME[iAbre]}, o ano 1 fecha em ${brl(ano1)}. Mês mais fundo: ${fundoMes}, ${brl(fundo as number)}.`,
    alerta: ano1 !== null && ano1 < 0 ? "atencao" : undefined,
    detalhes: { mes_mais_fundo: fundo, noites_ano1: okAno1 ? noites1.reduce((s, x) => s + x, 0) : null },
  });

  // 3. ano1_vs_regime
  const queda = okAno1 && noitesRegAno ? 1 - noites1.reduce((s, x) => s + x, 0) / noitesRegAno : null;
  calculos.push({
    id: "ano1_vs_regime", rotulo: "Quanto a receita do ano 1 fica abaixo da de regime", valor: queda === null ? null : queda * 100,
    texto: queda === null ? "Falta o ano 1 ou o regime." : `A receita do ano 1 fica ${fmtPct(queda)} abaixo da de regime. A fonte espera de 35% a 45% abaixo${queda < 0.35 - 1e-12 || queda > 0.45 + 1e-12 ? ": fora disso, confira a rampa." : "."}`,
    alerta: queda === null ? undefined : queda < 0.35 - 1e-12 || queda > 0.45 + 1e-12 ? "atencao" : "ok",
  });

  // 4. retorno_simples
  const rsP = div(sobra, cP), rsT = div(sobra, cT);
  calculos.push({
    id: "retorno_simples", rotulo: "Retorno simples", valor: rsP === null ? null : rsP * 100,
    texto: rsP === null && rsT === null ? "Falta o regime ou o CAPEX." : `Retorno simples: ${rsP === null ? "em branco" : fmtPct(rsP, 2)} ao ano no CAPEX piso e ${rsT === null ? "em branco" : fmtPct(rsT, 2)} no teto. A fonte não traz taxa de comparação: compare com a sua alternativa para o mesmo dinheiro.`,
    detalhes: { retorno_piso_pct: rsP === null ? null : rsP * 100, retorno_teto_pct: rsT === null ? null : rsT * 100 },
  });

  // 5. giro
  const buraco = okAno1 ? -res1.filter((x) => x < 0).reduce((s, x) => s + x, 0) : null;
  const reservaVale = base ? -(resReg as number[]).filter((x) => x < 0).reduce((s, x) => s + x, 0) : null;
  const seg = fixo !== null ? 3 * fixo : null;
  const et02 = buraco !== null && reservaVale !== null && seg !== null ? buraco + reservaVale + seg : null;
  const et01 = fixo !== null ? 6 * fixo : null;
  const giro = et02 !== null && et01 !== null ? tetoMultiplo(Math.max(et02, et01, 0), 500) : null;
  calculos.push({
    id: "giro", rotulo: "Capital de giro pelas duas regras", valor: giro,
    texto: giro === null ? "Faltam o ano 1, o regime ou o fixo para o capital de giro."
      : `Capital de giro: ${brl(giro)}, a maior das duas regras (buraco do ano 1 ${brl(buraco as number)} + reserva do vale ${brl(reservaVale as number)} + três meses de fixo ${brl(seg as number)} = ${brl(et02 as number)}; ou seis meses de fixo, ${brl(et01 as number)}), arredondada para cima a múltiplo de R$ 500. Piso: três meses de fixo no dia da abertura, nunca a conta inteira.`,
    detalhes: { buraco_ano1: buraco, reserva_vale: reservaVale, seguranca: seg, etapa02: et02, etapa01: et01 },
  });

  // 6. reserva_sazonalidade
  const resSaz = div(reservaVale, alta.length);
  calculos.push({
    id: "reserva_sazonalidade", rotulo: "Reserva por mês de alta", valor: resSaz,
    texto: resSaz === null ? "Falta o regime ou os meses de alta." : `Guarde ${brl(resSaz)} em cada um dos ${alta.length} meses de alta para atravessar o vale.`,
  });

  // 7. curva_caixa
  let menor: number | null = null, menorT = 0, folego: number | null = null;
  const saldos: number[] = [];
  if (giro !== null && okAno1) {
    let s = giro; saldos.push(s);
    for (let t = 1; t <= 24; t++) {
      if (t <= 12) s += res1[t - 1];
      else s += resReg[(iAbre + t - 1) % 12] as number;
      saldos.push(s);
    }
    menor = Math.min(...saldos); menorT = saldos.indexOf(menor);
    folego = div(menor, fixo);
  }
  {
    let t: string, alerta: Calculo["alerta"];
    const regua = "Régua do fôlego: abaixo de 2 meses, zona de risco; de 4 a 6, confortável.";
    if (menor === null) t = `Falta o giro ou o ano 1 para a curva de caixa. ${regua}`;
    else {
      const quando = menorT === 0 ? "no dia da abertura" : `no mês ${menorT} (${MESES_NOME[(iAbre + menorT - 1) % 12]} do ano ${menorT <= 12 ? 1 : 2})`;
      t = `Com o giro de ${brl(giro as number)}, o menor saldo dos 24 meses é ${brl(menor)}, ${quando}: fôlego de ${folego === null ? "em branco" : fmtN(folego, 1) + " meses de fixo"}. ${regua}`;
      if (folego !== null) alerta = folego < 2 ? "critico" : folego >= 4 && folego <= 6 ? "ok" : undefined;
      if (menor < 0) { t += " O giro acaba antes do fim do ano 2."; alerta = "critico"; }
    }
    calculos.push({ id: "curva_caixa", rotulo: "Saldo do giro nos 24 meses e o menor saldo", valor: menor, texto: t, alerta, detalhes: { folego_meses: folego, mes_do_menor_saldo: menor === null ? null : menorT } });
  }

  // 8. colchao
  const colP = div(menor, cP), colT = div(menor, cT);
  const falP = menor !== null && cP !== null ? 0.1 * cP - menor : null;
  const falT = menor !== null && cT !== null ? 0.1 * cT - menor : null;
  const colPior = colP !== null && colT !== null ? Math.min(colP, colT) : colP ?? colT;
  calculos.push({
    id: "colchao", rotulo: "Colchão sobre o CAPEX", valor: colP === null ? null : colP * 100,
    texto: colPior === null ? "Falta o menor saldo ou o CAPEX."
      : `O menor saldo é ${colP === null ? "em branco" : fmtPct(colP)} do CAPEX piso e ${colT === null ? "em branco" : fmtPct(colT)} do teto. ` +
        (colPior < 0.1 ? `Abaixo de 10%: recalcule quanto captar na Aula 10. Para chegar a 10% faltam ${falP === null ? "em branco" : brl(Math.max(0, falP))} (piso) e ${falT === null ? "em branco" : brl(Math.max(0, falT))} (teto).` : "Colchão de pelo menos 10% do CAPEX.") +
        " Hipótese: obra paga até a abertura e giro intacto no dia 1.",
    alerta: colPior === null ? undefined : colPior < 0.1 ? "critico" : "ok",
    detalhes: { colchao_piso_pct: colP === null ? null : colP * 100, colchao_teto_pct: colT === null ? null : colT * 100, falta_para_10_piso: falP, falta_para_10_teto: falT },
  });

  // 9. payback
  let pbP: number | null = null, pbT: number | null = null, naoVolta = false;
  if (sobra !== null && ano1 !== null) {
    if (sobra <= 0) naoVolta = true;
    else { pbP = cP !== null ? 1 + (cP - ano1) / sobra : null; pbT = cT !== null ? 1 + (cT - ano1) / sobra : null; }
  }
  const pbPior = pbP !== null && pbT !== null ? Math.max(pbP, pbT) : pbP ?? pbT;
  {
    const regua = "Régua: até 5 anos, muito bom; 5 a 8, bom; 8 a 12, aceitável com valorização relevante; acima de 12, só com patrimônio, uso próprio ou projeto de vida declarados.";
    let t: string, alerta: Calculo["alerta"];
    if (naoVolta) { t = `O regime não sobra nada: o investimento não volta. ${regua}`; alerta = "critico"; }
    else if (pbPior === null) t = `Falta o regime, o ano 1 ou o CAPEX para o payback. ${regua}`;
    else {
      const leitura = (x: number) => (x <= 5 ? "muito bom" : x <= 8 ? "bom" : x <= 12 ? "aceitável com valorização relevante" : "acima de 12, só com patrimônio, uso próprio ou projeto de vida declarados");
      t = `Payback acumulado: ${pbP === null ? "em branco" : fmtN(pbP, 1) + " anos"} no piso e ${pbT === null ? "em branco" : fmtN(pbT, 1) + " anos"} no teto. Leitura do teto da conta: ${leitura(pbPior)}. ${regua}`;
      alerta = pbPior > 12 ? "critico" : pbPior > 8 ? "atencao" : "ok";
    }
    calculos.push({ id: "payback", rotulo: "Payback acumulado", valor: naoVolta ? "não volta" : pbP, texto: t, alerta, detalhes: { payback_piso_anos: pbP, payback_teto_anos: pbT } });
  }

  // 10. cenarios
  const variavel = d !== null && contrib !== null ? FATOR * d - contrib : null;
  const cons = variavel !== null && noitesRegAno !== null && fixo !== null && d !== null ? noitesRegAno * 0.8 * (FATOR * 0.9 * d - variavel) - 12 * fixo : null;
  const otim = variavel !== null && noitesRegAno !== null && fixo !== null && d !== null ? noitesRegAno * 1.15 * (FATOR * 1.1 * d - variavel) - 12 * fixo : null;
  const razao = div(cons, sobra);
  {
    let t: string, alerta: Calculo["alerta"];
    if (cons === null || sobra === null) t = "Falta a diária, a contribuição ou o regime para os cenários.";
    else {
      t = `Conservador (ocupação 20% menor e diária 10% menor): ${brl(cons)} por ano. Otimista: ${brl(otim as number)}. Base: ${brl(sobra)}. `;
      if (sobra < 0) { t += "Base negativo: o modelo não fecha."; alerta = "critico"; }
      else if (cons >= 0) { t += "Conservador positivo: pode seguir com segurança."; alerta = "ok"; }
      else { t += `Conservador negativo com base positivo: se for leve, siga com reserva maior; se for muito, mude alguma coisa antes. A fonte não dá número para "leve" e "muito": a razão conservador sobre base é ${razao === null ? "em branco" : fmtN(razao, 2)}.`; alerta = "atencao"; }
    }
    calculos.push({ id: "cenarios", rotulo: "Conservador e otimista no regime", valor: cons, texto: t, alerta, detalhes: { conservador: cons, otimista: otim, razao_conservador_base: razao, variavel_noite: variavel } });
  }

  // 11. diaria_conservador_fecha
  const dCons = variavel !== null && fixo !== null && noitesRegAno !== null && noitesRegAno > 0 ? ((12 * fixo) / (0.8 * noitesRegAno) + variavel) / (FATOR * 0.9) : null;
  calculos.push({
    id: "diaria_conservador_fecha", rotulo: "A diária que faz o conservador fechar", valor: dCons,
    texto: dCons === null ? "Faltam números para a diária do conservador." : `O conservador fecha com diária média de ${brl(dCons)}. É o que o teste de preço precisa mostrar. Não é premissa: é hipótese a testar.`,
  });

  // 12. ruptura
  const rup = contrib !== null && contrib > 0 && fixo !== null && u !== null ? div((12 * fixo) / contrib, u * 360) : null;
  calculos.push({
    id: "ruptura", rotulo: "Ponto de ruptura", valor: rup === null ? null : rup * 100,
    texto: rup === null ? (contrib !== null && contrib <= 0 ? "Cada noite não deixa nada: não existe ocupação que pague o fixo." : "Faltam números para o ponto de ruptura.") : `Abaixo de ${fmtPct(rup, 2)} de ocupação média no ano, a operação não paga o fixo completo.`,
  });

  // 13. dor
  const pD = noitesRegAno !== null && d !== null ? noitesRegAno * 0.1 * d * FATOR : null;
  const pO = noitesRegAno !== null && contrib !== null ? 0.1 * noitesRegAno * contrib : null;
  calculos.push({
    id: "dor", rotulo: "O que dói mais: diária ou ocupação 10% pior", valor: pD !== null && pO !== null ? (pD >= pO ? "diária" : "ocupação") : null,
    texto: pD === null || pO === null ? "Faltam números para comparar." : `Diária 10% pior tira ${brl(pD)} por ano; ocupação 10% pior tira ${brl(pO)}. Dói mais ${pD >= pO ? "a diária" : "a ocupação"}.`,
    detalhes: { perda_diaria: pD, perda_ocupacao: pO },
  });

  // 14. veredito_sugerido (colchão e payback lidos pelo lado mais exigente, piso ou teto)
  const testada = escolha(r, "diaria_testada");
  let v: Veredito, motivo: string;
  if (sobra !== null && sobra < 0) {
    v = "pausar"; motivo = "O base é negativo: o modelo não fecha. Pausa e redesenha, ou declara por escrito que é projeto de patrimônio e de vida.";
  } else if (sobra === null || cons === null) {
    v = "testar"; motivo = "Testar: faltam números para o regime ou os cenários.";
  } else if (cons < 0 && testada !== "testada") {
    v = "testar"; motivo = `O base fecha, mas o conservador não (${brl(cons)}), e a diária ainda não foi testada: teste o preço antes de qualquer contrato. A diária que faz o conservador fechar é ${dCons === null ? "em branco" : brl(dCons)}.`;
  } else if (colPior === null || folego === null || (pbPior === null && !naoVolta)) {
    v = "testar"; motivo = "Testar: falta o colchão, o fôlego ou o payback para fechar a leitura.";
  } else if (cons < 0 || colPior < 0.1 || folego < 2 || naoVolta || (pbPior as number) > 12) {
    v = "ajustar";
    motivo = `Ajustar: ${juntar([cons < 0 && "o conservador continua negativo com a diária testada", colPior < 0.1 && "o colchão ficou abaixo de 10% do CAPEX", folego < 2 && "o fôlego ficou abaixo de 2 meses", (naoVolta || (pbPior as number) > 12) && "o payback passa de 12 anos sem razão declarada"].filter(Boolean) as string[])}.`;
  } else {
    v = "avancar"; motivo = "Conservador positivo, colchão de pelo menos 10% do CAPEX, fôlego fora da zona de risco e payback dentro da régua.";
  }
  calculos.push({ id: "veredito_sugerido", rotulo: "Veredito sugerido pela página", valor: v, texto: motivo });

  return { calculos: calculos.map((c) => fechar(c)), veredito_sugerido: v, motivo_veredito: motivo };
}

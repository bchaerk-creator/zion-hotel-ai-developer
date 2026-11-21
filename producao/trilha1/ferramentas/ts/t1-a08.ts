// Trilha 1 · Aula 8 · Receitas e custos (slug 1-8). Fonte: exercicios/aula-08.json.
import type { Calculo, ResultadoCalculos, Respostas, Veredito } from "./types";
import { brl, div, fechar, fmtN, fmtPct, juntar, num, pct } from "./util";

const QUEBRA = 0.01; // 1% da diária por noite, na fórmula da fonte

export function calcular(r: Respostas): ResultadoCalculos {
  const calculos: Calculo[] = [];
  const u = num(r, "unidades"), d = num(r, "diaria_media");
  const mA = num(r, "meses_alta"), mV = num(r, "meses_vale");
  const oA = pct(r, "ocup_alta"), oV = pct(r, "ocup_vale"), oM = pct(r, "ocup_media");
  const ded = pct(r, "deducoes_pct");

  // 1. noites
  let mM: number | null = null, nA: number | null = null, nM: number | null = null, nV: number | null = null, noitesAno: number | null = null, ocupAno: number | null = null;
  {
    let t: string;
    if (u === null || mA === null || mV === null || oA === null || oM === null || oV === null) t = "Faltam unidades, meses ou ocupações para contar as noites.";
    else if (12 - mA - mV < 0 || mA < 0 || mV < 0) t = "Meses de alta mais meses de vale passam de 12: confira.";
    else {
      mM = 12 - mA - mV;
      nA = u * 30 * oA; nM = u * 30 * oM; nV = u * 30 * oV;
      noitesAno = mA * nA + mM * nM + mV * nV;
      ocupAno = div(noitesAno, u * 360);
      t = `Noites vendidas por mês: ${fmtN(nA, 1)} na alta, ${fmtN(nM, 1)} nos meses médios, ${fmtN(nV, 1)} no vale. No ano: ${fmtN(noitesAno, 1)} noites, ${ocupAno === null ? "ocupação em branco" : fmtPct(ocupAno) + " de ocupação"} (meses de 30 dias).`;
    }
    calculos.push({ id: "noites", rotulo: "Noites por mês e no ano", valor: noitesAno, texto: t, detalhes: { meses_medios: mM, noites_mes_alta: nA, noites_mes_media: nM, noites_mes_vale: nV, ocup_ano_pct: ocupAno === null ? null : ocupAno * 100 } });
  }

  // 2. receita
  const bruta = noitesAno !== null && d !== null ? noitesAno * d : null;
  const real = bruta !== null && ded !== null ? bruta * (1 - ded) : null;
  calculos.push({
    id: "receita", rotulo: "Receita bruta e real", valor: bruta,
    texto: bruta === null ? "Faltam as noites ou a diária média." : `Receita bruta no ano: ${brl(bruta)}. Receita real, depois de impostos, comissões e cancelamento: ${real === null ? "em branco (falta o percentual)" : brl(real)}.`,
    detalhes: { receita_bruta: bruta, receita_real: real },
  });

  // 3. variavel_por_noite
  const vn = num(r, "variavel_noite"), limp = num(r, "limpeza_estadia"), est = num(r, "estadia_media");
  const limpNoite = div(limp, est);
  const variavel = vn !== null && limpNoite !== null && d !== null ? vn + limpNoite + QUEBRA * d : null;
  calculos.push({
    id: "variavel_por_noite", rotulo: "Custo variável por noite vendida", valor: variavel,
    texto: variavel === null
      ? `Em branco: falta ${juntar([vn === null && "o que cada noite consome", limp === null && "a limpeza por estadia", (est === null || est === 0) && "a estadia média", d === null && "a diária média"].filter(Boolean) as string[])}. Peça o orçamento; não use número de exemplo sem marcar "provisório".`
      : `Cada noite vendida custa ${brl(variavel)}: ${brl(vn as number)} de consumo, ${brl(limpNoite as number)} de limpeza por noite e ${brl(QUEBRA * (d as number))} de quebra (1% da diária).`,
  });

  // 4. contribuicao_noite
  const contrib = d !== null && ded !== null && variavel !== null ? d * (1 - ded) - variavel : null;
  calculos.push({
    id: "contribuicao_noite", rotulo: "Quanto cada noite vendida deixa", valor: contrib,
    texto: contrib === null ? "Falta a diária, as deduções ou o custo variável." : `Cada noite vendida deixa ${brl(contrib)} para pagar o fixo.`,
    alerta: contrib !== null && contrib <= 0 ? "critico" : undefined,
  });

  // 5. fixo_completo
  const resPct = pct(r, "reserva_pct");
  const fixos = num(r, "fixos_operacionais_mes"), ret = num(r, "retirada_mes");
  const reservaMes = resPct !== null && bruta !== null ? (resPct * bruta) / 12 : null;
  const fixo = fixos !== null && ret !== null && reservaMes !== null ? fixos + ret + reservaMes : null;
  {
    let t = fixo === null
      ? `Em branco: falta ${juntar([fixos === null && "os fixos operacionais", ret === null && "o custo do seu trabalho", reservaMes === null && "a reserva de reposição (ou a receita)"].filter(Boolean) as string[])}.`
      : `Fixo completo do mês: ${brl(fixo)} (${brl(fixos as number)} de operação, ${brl(ret as number)} do seu trabalho e ${brl(reservaMes as number)} de reserva).`;
    let alerta: Calculo["alerta"];
    if (resPct !== null && (resPct < 0.03 - 1e-12 || resPct > 0.05 + 1e-12)) { t += ` Aviso: reserva de ${fmtPct(resPct)}, fora de 3% a 5%.`; alerta = "atencao"; }
    calculos.push({ id: "fixo_completo", rotulo: "Fixo completo do mês", valor: fixo, texto: t, alerta, detalhes: { reserva_mes: reservaMes } });
  }

  // 6. cascata
  const mc = noitesAno !== null && contrib !== null ? noitesAno * contrib : null;
  const resOp = mc !== null && fixos !== null && ret !== null ? mc - 12 * (fixos + ret) : null;
  const depois = resOp !== null && reservaMes !== null ? resOp - 12 * reservaMes : null;
  const margem = div(depois, bruta);
  {
    let t: string, alerta: Calculo["alerta"];
    const regua = "Régua: acima de 30% boa; 20% a 30% viável; 10% a 20% apertada; abaixo de 10% o modelo não fecha.";
    if (margem === null) t = `Faltam números para a cascata. ${regua}`;
    else {
      const leitura = margem > 0.3 ? "boa" : margem >= 0.2 ? "viável" : margem >= 0.1 ? "apertada" : "o modelo não fecha";
      alerta = margem >= 0.2 ? "ok" : margem >= 0.1 ? "atencao" : "critico";
      t = `Margem de contribuição no ano: ${brl(mc as number)}. Resultado operacional: ${brl(resOp as number)}. Depois da reserva: ${brl(depois as number)}, margem de ${fmtPct(margem, 2)}: ${leitura}. ${regua}`;
    }
    calculos.push({ id: "cascata", rotulo: "A cascata do ano de regime", valor: margem === null ? null : margem * 100, texto: t, alerta, detalhes: { margem_contrib: mc, resultado_operacional: resOp, depois_reserva: depois } });
  }

  // 7. mes_a_mes
  const rm = (n: number | null) => (n !== null && contrib !== null && fixo !== null ? n * contrib - fixo : null);
  const rA = rm(nA), rM = rm(nM), rV = rm(nV);
  const faltaVale = rV !== null && mV !== null && rV < 0 ? mV * rV : rV !== null ? 0 : null;
  {
    let t: string;
    if (rA === null || rM === null || rV === null) t = "Faltam números para o mês a mês.";
    else {
      const neg = ([[rA, mA, "alta"], [rM, mM, "médios"], [rV, mV, "vale"]] as [number, number, string][]).filter(([x, m]) => x < 0 && m > 0);
      t = `Resultado de cada mês: alta ${brl(rA)}, médio ${brl(rM)}, vale ${brl(rV)}.`;
      t += neg.length ? ` Não fecham: ${juntar(neg.map(([, m, n]) => `${fmtN(m)} mês(es) de ${n}`))}.` : " Todos os meses fecham.";
      if (faltaVale !== null && faltaVale < 0) t += ` O vale deixa um buraco de ${brl(faltaVale)} no ano.`;
    }
    calculos.push({ id: "mes_a_mes", rotulo: "Resultado de cada estação e os meses que não fecham", valor: faltaVale, texto: t, alerta: faltaVale !== null && faltaVale < 0 ? "atencao" : undefined, detalhes: { resultado_mes_alta: rA, resultado_mes_media: rM, resultado_mes_vale: rV, falta_vale: faltaVale } });
  }

  // 8. equilibrio
  const nEq = contrib !== null && contrib > 0 && fixo !== null ? (12 * fixo) / contrib : null;
  const oEq = u !== null ? div(nEq, u * 360) : null;
  const folga = ocupAno !== null && oEq !== null ? (ocupAno - oEq) * 100 : null;
  calculos.push({
    id: "equilibrio", rotulo: "Ponto de equilíbrio e folga", valor: folga,
    texto: folga === null
      ? contrib !== null && contrib <= 0 ? "Cada noite não deixa nada: não existe ponto de equilíbrio com esta diária." : "Faltam números para o equilíbrio."
      : `Equilíbrio: ${fmtN(nEq as number, 1)} noites no ano, ${fmtPct(oEq as number, 2)} de ocupação, contra ${fmtPct(ocupAno as number)} esperados. Folga de ${fmtN(folga, 2)} pontos.${folga < 10 ? " Folga abaixo de 10 pontos: projeto apertado." : ""}`,
    alerta: folga === null ? (contrib !== null && contrib <= 0 ? "critico" : undefined) : folga < 0 ? "critico" : folga < 10 ? "atencao" : "ok",
    detalhes: { noites_equilibrio_ano: nEq, ocup_equilibrio_pct: oEq === null ? null : oEq * 100 },
  });

  // 9. custo_por_diaria
  const cd = (n: number | null) => (variavel !== null && fixo !== null && n !== null && n > 0 ? variavel + fixo / n : null);
  const cA = cd(nA), cM = cd(nM), cV = cd(nV);
  const cAno = variavel !== null && fixo !== null && noitesAno !== null && noitesAno > 0 ? variavel + (12 * fixo) / noitesAno : null;
  calculos.push({
    id: "custo_por_diaria", rotulo: "Custo por diária vendida", valor: cAno,
    texto: cAno === null ? "Faltam números para o custo por diária." : `Cada diária vendida custa ${brl(cAno)} na média do ano: ${cA === null ? "alta em branco" : brl(cA) + " na alta"}, ${cM === null ? "médio em branco" : brl(cM) + " nos meses médios"}, ${cV === null ? "vale em branco" : brl(cV) + " no vale"}.`,
    detalhes: { custo_alta: cA, custo_media: cM, custo_vale: cV, custo_ano: cAno },
  });

  // 10. diaria_criterio
  const parteFixa = vn !== null && limpNoite !== null ? vn + limpNoite : null;
  const den = ded !== null ? 1 - ded - QUEBRA - 0.1 : null;
  const d10 = parteFixa !== null && fixo !== null && noitesAno !== null && noitesAno > 0 && den !== null && den > 0 ? ((12 * fixo) / noitesAno + parteFixa) / den : null;
  calculos.push({
    id: "diaria_criterio", rotulo: "Diária mínima para a margem chegar a 10%", valor: d10,
    texto: d10 === null ? "Faltam números para a diária de 10% de margem." : `Diária média mínima para a margem chegar a 10%: ${brl(d10)}. É a diária que o teste de preço precisa mostrar para sair de "não fecha".`,
  });

  // 11. taxa_que_empata
  const taxa = ret !== null ? div(12 * ret, bruta) : null;
  calculos.push({
    id: "taxa_que_empata", rotulo: "Taxa de gestão que só empata (se a proposta assumir o seu trabalho)", valor: taxa === null ? null : taxa * 100,
    texto: taxa === null ? "Falta o custo do seu trabalho ou a receita bruta." : `Uma taxa de gestão de ${fmtPct(taxa, 2)} da receita bruta só empata com o custo do seu trabalho. Não é taxa de mercado: é a régua para ler propostas escritas.`,
  });

  // 12. veredito_sugerido
  let v: Veredito, motivo: string;
  if (margem === null) {
    v = "testar"; motivo = "Testar: faltam números para a margem. Peça os orçamentos que estão em branco.";
  } else if (margem < 0 && ((folga !== null && folga < 0) || (contrib !== null && contrib <= 0))) {
    // contribuição zero ou negativa: não existe equilíbrio, conta como folga negativa
    v = "pausar"; motivo = "A operação não paga nem o fixo na ocupação esperada: pausa e volta ao produto ou ao fixo antes de assinar a obra.";
  } else if (margem < 0.1) {
    v = "testar"; motivo = `Margem de ${fmtPct(margem, 2)}, abaixo de 10%: pela régua o modelo não fecha com a diária de hoje. Antes da obra, teste se o produto sustenta uma diária de pelo menos ${d10 === null ? "a mínima para 10%" : brl(d10)}.`;
  } else if (folga === null) {
    v = "testar"; motivo = "Testar: falta a folga sobre o equilíbrio.";
  } else if (margem < 0.2 || folga < 10) {
    v = "ajustar"; motivo = `Ajustar: ${juntar([margem < 0.2 && `margem de ${fmtPct(margem, 2)} (apertada)`, folga < 10 && `folga de ${fmtN(folga, 2)} pontos`].filter(Boolean) as string[])}. Mexa no fixo, no produto ou no número de unidades antes de seguir.`;
  } else {
    v = "avancar"; motivo = `Margem de ${fmtPct(margem, 2)} depois da reserva e folga de ${fmtN(folga, 2)} pontos.`;
  }
  calculos.push({ id: "veredito_sugerido", rotulo: "Veredito sugerido pela página", valor: v, texto: motivo });

  return { calculos: calculos.map((c) => fechar(c)), veredito_sugerido: v, motivo_veredito: motivo };
}

// Trilha 1 · Aula 7 · CAPEX (slug 1-7). Fonte: exercicios/aula-07.json.
import type { Calculo, ResultadoCalculos, Respostas, Veredito } from "./types";
import { brl, div, escolha, falta, fechar, fmtN, fmtPct, juntar, lista, num, pct } from "./util";

const FATORES = ["remoto", "sistema_inedito", "importados", "area_sensivel", "prazo_apertado"];
const DEGRAU: Record<string, string> = { palpite: "estimador", faixa: "estimador, saindo", cotacao: "calculista" };

type Lado = { obra: number | null; ffe: number | null; ose: number | null; hard: number | null; pre: number | null; base: number | null; cont: number | null; capex: number | null };

const faixaBrl = (a: number | null, b: number | null) =>
  a !== null && b !== null ? `${brl(a)} a ${brl(b)}` : a !== null ? `${brl(a)} (piso; teto em branco)` : b !== null ? `${brl(b)} (teto; piso em branco)` : "em branco";

export function calcular(r: Respostas): ResultadoCalculos {
  const calculos: Calculo[] = [];
  const u = num(r, "unidades");
  const afu = num(r, "area_fechada_unidade");
  const deckNS = num(r, "area_deck_unidade") === null;
  const apoioNS = num(r, "area_apoio") === null;
  const deck = num(r, "area_deck_unidade") ?? 0;
  const apoio = num(r, "area_apoio") ?? 0;

  // 1. area_total
  const areaTotal = u !== null && afu !== null ? u * (afu + deck) + apoio : null;
  const esquecida = areaTotal !== null ? areaTotal - (u as number) * (afu as number) : null;
  const pEsq = div(esquecida, areaTotal);
  {
    let t: string;
    if (areaTotal === null) t = "Falta o número de unidades ou a área fechada de cada uma.";
    else {
      t = `Área construída total: ${fmtN(areaTotal)} m². Orçando só as unidades fechadas, ficariam de fora ${fmtN(esquecida as number)} m² (${pEsq === null ? "em branco" : fmtPct(pEsq)}).`;
      const m = [deckNS && "deck", apoioNS && "apoio"].filter(Boolean) as string[];
      if (m.length) t += ` Provisória: ${juntar(m)} em Não sei entrou como zero, e a obra sai subestimada.`;
    }
    calculos.push({ id: "area_total", rotulo: "Área construída total, e quanto ficaria de fora orçando só as unidades", valor: areaTotal, texto: t, alerta: deckNS || apoioNS ? "atencao" : undefined, detalhes: { esquecida_m2: esquecida, pct_esquecida: pEsq === null ? null : pEsq * 100 } });
  }

  // 2. obra
  const cP = num(r, "custo_m2_piso"), cT = num(r, "custo_m2_teto");
  const L: { piso: Lado; teto: Lado } = {
    piso: { obra: areaTotal !== null && cP !== null ? areaTotal * cP : null, ffe: null, ose: null, hard: null, pre: null, base: null, cont: null, capex: null },
    teto: { obra: areaTotal !== null && cT !== null ? areaTotal * cT : null, ffe: null, ose: null, hard: null, pre: null, base: null, cont: null, capex: null },
  };
  calculos.push({
    id: "obra", rotulo: "Obra pela área total", valor: L.piso.obra,
    texto: L.piso.obra === null && L.teto.obra === null ? "Falta a área total ou o custo por m²." : `Obra pela área total: ${faixaBrl(L.piso.obra, L.teto.obra)}.`,
    detalhes: { obra_piso: L.piso.obra, obra_teto: L.teto.obra },
  });

  // 3. ffe_ose
  const fP = num(r, "ffe_unidade_piso"), fT = num(r, "ffe_unidade_teto");
  L.piso.ffe = u !== null && fP !== null ? u * fP : null;
  L.teto.ffe = u !== null && fT !== null ? u * fT : null;
  L.piso.ose = L.piso.ffe !== null ? 0.1 * L.piso.ffe : null;
  L.teto.ose = L.teto.ffe !== null ? 0.15 * L.teto.ffe : null;
  calculos.push({
    id: "ffe_ose", rotulo: "FF&E e OS&E", valor: L.piso.ffe,
    texto: L.piso.ffe === null && L.teto.ffe === null ? "Falta o FF&E por unidade." : `Mobiliário e equipamentos (FF&E): ${faixaBrl(L.piso.ffe, L.teto.ffe)}. Enxoval e operação (OS&E, 10% a 15% do FF&E): ${faixaBrl(L.piso.ose, L.teto.ose)}.`,
    detalhes: { ffe_piso: L.piso.ffe, ffe_teto: L.teto.ffe, ose_piso: L.piso.ose, ose_teto: L.teto.ose },
  });

  // 4. pre_abertura
  const infraNS = falta(r["infraestrutura"]);
  const projNS = falta(r["projetos_consultas"]);
  const infra = num(r, "infraestrutura") ?? 0;
  const proj = num(r, "projetos_consultas") ?? 0;
  L.piso.hard = L.piso.obra !== null ? L.piso.obra + infra : null;
  L.teto.hard = L.teto.obra !== null ? L.teto.obra + infra : null;
  L.piso.pre = L.piso.hard !== null ? 0.05 * L.piso.hard : null;
  L.teto.pre = L.teto.hard !== null ? 0.1 * L.teto.hard : null;
  calculos.push({
    id: "pre_abertura", rotulo: "Pré-abertura", valor: L.piso.pre,
    texto: (L.piso.pre === null && L.teto.pre === null ? "Falta a obra para calcular a pré-abertura." : `Pré-abertura (5% a 10% da obra com infraestrutura): ${faixaBrl(L.piso.pre, L.teto.pre)}.`) +
      (infraNS ? " Infraestrutura em branco, cotação pedida: a pré-abertura sobe quando ela entrar." : ""),
    detalhes: { hard_piso: L.piso.hard, hard_teto: L.teto.hard, pre_piso: L.piso.pre, pre_teto: L.teto.pre, infraestrutura_em_branco: infraNS },
  });

  // 5. contingencia
  const cPct = pct(r, "contingencia_pct");
  for (const lado of [L.piso, L.teto]) {
    if (lado.hard !== null && lado.ffe !== null && lado.ose !== null && lado.pre !== null) {
      lado.base = lado.hard + proj + lado.ffe + lado.ose + lado.pre;
      if (cPct !== null) { lado.cont = cPct * lado.base; lado.capex = lado.base + lado.cont; }
    }
  }
  const parcial = infraNS || projNS;
  {
    let t: string;
    if (cPct === null) t = "Falta a contingência escolhida.";
    else if (L.piso.capex === null && L.teto.capex === null) t = "Faltam linhas para fechar o CAPEX (obra ou FF&E).";
    else {
      t = `Contingência de ${fmtPct(cPct)} sobre a soma: ${faixaBrl(L.piso.cont, L.teto.cont)}. CAPEX ${parcial ? "parcial" : ""}: ${faixaBrl(L.piso.capex, L.teto.capex)}.`.replace("CAPEX :", "CAPEX:");
      if (parcial) t += ` Linhas em branco: ${juntar([infraNS && "infraestrutura", projNS && "projetos e consultas"].filter(Boolean) as string[])}.`;
    }
    calculos.push({
      id: "contingencia", rotulo: "Contingência e CAPEX", valor: L.piso.capex, texto: t, alerta: parcial ? "atencao" : undefined,
      detalhes: { base_piso: L.piso.base, base_teto: L.teto.base, cont_piso: L.piso.cont, cont_teto: L.teto.cont, capex_piso: L.piso.capex, capex_teto: L.teto.capex, parcial },
    });
  }

  // 6. sanidade
  const prop = (lado: Lado) => ({
    hard: div(lado.hard, lado.capex), ffe: div(lado.ffe, lado.capex), ose: div(lado.ose, lado.capex), pre: div(lado.pre, lado.capex), cont: div(lado.cont, lado.capex),
  });
  const pP = prop(L.piso), pT = prop(L.teto);
  {
    let t: string, alerta: Calculo["alerta"];
    if (pP.hard === null && pT.hard === null) t = "Sem o CAPEX não dá para conferir as proporções.";
    else {
      const linha = (nome: string, p: ReturnType<typeof prop>) =>
        p.hard === null ? `${nome}: em branco` :
          `${nome}: obra e infraestrutura ${fmtPct(p.hard)}, FF&E ${fmtPct(p.ffe as number)}, OS&E ${fmtPct(p.ose as number)}, pré-abertura ${fmtPct(p.pre as number)}, contingência ${fmtPct(p.cont as number)}`;
      t = `${linha("No piso", pP)}. ${linha("No teto", pT)}. Tabela de sanidade: obra 60% a 70% (acima de 80%, faltou algo); FF&E 15% a 20% (abaixo de 10%, alerta em produto premium); OS&E 2% a 4%; pré-abertura 3% a 5%; contingência 10% a 15%.`;
      const avisos: string[] = [];
      for (const p of [pP, pT]) {
        if (p.hard !== null && p.hard > 0.8) avisos.push("obra acima de 80%: faltou algo");
        if (p.ffe !== null && p.ffe < 0.1) avisos.push("FF&E abaixo de 10%");
      }
      if (avisos.length) { t += ` Aviso: ${juntar(Array.from(new Set(avisos)))}.`; alerta = "atencao"; }
      if (parcial) t += " Com linhas em branco, isto é aviso, não veredito.";
    }
    calculos.push({
      id: "sanidade", rotulo: "As proporções contra a tabela de sanidade", valor: pP.hard === null ? null : pP.hard * 100, texto: t, alerta,
      detalhes: {
        pct_hard_piso: pP.hard === null ? null : pP.hard * 100, pct_ffe_piso: pP.ffe === null ? null : pP.ffe * 100, pct_ose_piso: pP.ose === null ? null : pP.ose * 100, pct_pre_piso: pP.pre === null ? null : pP.pre * 100, pct_cont_piso: pP.cont === null ? null : pP.cont * 100,
        pct_hard_teto: pT.hard === null ? null : pT.hard * 100, pct_ffe_teto: pT.ffe === null ? null : pT.ffe * 100, pct_ose_teto: pT.ose === null ? null : pT.ose * 100, pct_pre_teto: pT.pre === null ? null : pT.pre * 100, pct_cont_teto: pT.cont === null ? null : pT.cont * 100,
      },
    });
  }

  // 7. contingencia_faixa
  const fatores = lista(r, "fatores_risco", FATORES).length;
  const naFaixa = cPct === null ? null : cPct >= 0.1 - 1e-12 && cPct <= 0.15 + 1e-12;
  {
    let t: string, alerta: Calculo["alerta"];
    if (cPct === null) t = "Falta a contingência escolhida. Régua: 10% a 15%.";
    else {
      t = naFaixa ? `Contingência de ${fmtPct(cPct)}: dentro da faixa de 10% a 15%.` : `Contingência de ${fmtPct(cPct)}: fora da faixa de 10% a 15%, ajustar.`;
      alerta = naFaixa ? "ok" : "critico";
      t += ` Fatores de risco: ${fatores}.`;
      if (fatores >= 2 && cPct < 0.15 - 1e-12) { t += " Dois ou mais fatores com contingência abaixo de 15%: considere o teto da faixa."; alerta = alerta === "ok" ? "atencao" : alerta; }
    }
    calculos.push({ id: "contingencia_faixa", rotulo: "Contingência na faixa e fatores de risco", valor: naFaixa, texto: t, alerta, detalhes: { fatores } });
  }

  // 8. custo_por_unidade
  const cuP = div(L.piso.capex, u), cuT = div(L.teto.capex, u), cuI = infraNS ? null : div(infra, u);
  calculos.push({
    id: "custo_por_unidade", rotulo: "Custo por unidade (custo por chave)", valor: cuP,
    texto: cuP === null && cuT === null ? "Sem CAPEX ou sem unidades, o custo por unidade fica em branco." : `Custo por unidade: ${faixaBrl(cuP, cuT)}.` + (cuI === null ? " Infraestrutura por unidade em branco, até a cotação." : ` Infraestrutura por unidade: ${brl(cuI)}.`),
    detalhes: { custo_unidade_piso: cuP, custo_unidade_teto: cuT, infra_por_unidade: cuI },
  });

  // 9. teto_briefing
  const obraU = afu !== null && cT !== null ? (afu + deck) * cT : null;
  calculos.push({
    id: "teto_briefing", rotulo: "Teto provisório por unidade para o briefing", valor: obraU,
    texto: obraU === null && fT === null ? "Falta o custo por m² de teto ou o FF&E de teto." : `Teto por unidade para o briefing: obra ${obraU === null ? "em branco" : brl(obraU)} e FF&E ${fT === null ? "em branco" : brl(fT)}. Não é preço: é o limite acima do qual uma cotação precisa vir com explicação escrita.`,
    detalhes: { obra_unidade: obraU, ffe_unidade: fT },
  });

  // 10. degrau
  const origem = escolha(r, "origem_numeros");
  const degrau = origem !== null && DEGRAU[origem] ? DEGRAU[origem] : null;
  calculos.push({ id: "degrau", rotulo: "Degrau na régua de maturidade", valor: degrau, texto: degrau === null ? "Falta de onde vem a maior parte dos seus números." : `Pela origem dos seus números, você está no degrau: ${degrau}.` });

  // 11. veredito_sugerido
  const corte = escolha(r, "corte_experiencia");
  let v: Veredito, motivo: string;
  if (corte === "sim") {
    v = "pausar"; motivo = "Para caber, seria preciso cortar um item que move a diária ou a vista: pausa e volta ao masterplan. Corta metros, nunca a experiência.";
  } else if (corte === null || corte === "nao_sei") {
    v = "testar"; motivo = "Testar: falta saber se, para caber, algum item que move a diária ou a vista teria que sair.";
  } else if (naFaixa === false || (pP.ffe !== null && pP.ffe < 0.1)) {
    v = "ajustar";
    motivo = `Ajustar: ${juntar([naFaixa === false && "a contingência está fora de 10% a 15%", pP.ffe !== null && pP.ffe < 0.1 && "o mobiliário ficou abaixo de 10% do CAPEX"].filter(Boolean) as string[])}.`;
  } else if (origem === null || origem === "palpite" || naFaixa === null || pP.ffe === null) {
    v = "testar"; motivo = origem === "palpite" || origem === null ? "Testar: os números ainda são palpite. Abra as linhas e escreva a origem de cada uma." : "Testar: falta dado para fechar o CAPEX no piso.";
  } else {
    v = "avancar"; motivo = "As linhas têm origem escrita, a contingência está na faixa e nada da experiência precisa ser cortado. Peça as cotações das maiores linhas, com o escopo congelado anexado.";
  }
  calculos.push({ id: "veredito_sugerido", rotulo: "Veredito sugerido pela página", valor: v, texto: motivo });

  return { calculos: calculos.map((c) => fechar(c)), veredito_sugerido: v, motivo_veredito: motivo };
}

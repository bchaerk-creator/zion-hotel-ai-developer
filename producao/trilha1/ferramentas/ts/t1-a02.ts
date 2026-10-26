// Trilha 1 · Aula 2 · Território (slug 1-2). Fonte: exercicios/aula-02.json.
import type { Calculo, ResultadoCalculos, Respostas, Veredito } from "./types";
import { brl, div, escolha, falta, fechar, fmtN, fmtPct, juntar, lista, num } from "./util";

const SUBS: [string, string][] = [
  ["sub_preservacao", "preservação"],
  ["sub_reserva_legal", "reserva legal"],
  ["sub_encosta", "encosta forte"],
  ["sub_recuos", "recuos e faixas"],
  ["sub_servico", "área de serviço"],
];
const LIMITES: [string, string][] = [
  ["limite_fisico", "físico"],
  ["limite_infra", "de infraestrutura"],
  ["limite_experiencia", "de experiência"],
  ["limite_mercado", "de mercado"],
];
const DOCS: [string, string][] = [
  ["matricula", "matrícula atualizada"],
  ["car", "CAR"],
  ["zoneamento", "zoneamento"],
  ["consulta_previa", "consulta prévia"],
];
/** Campos que aceitam "Não sei" (todos, menos a área da matrícula e a lista de documentos). */
const CAMPOS_NS = [
  "sub_preservacao", "sub_reserva_legal", "sub_encosta", "sub_recuos", "sub_servico",
  "preco_terreno", "investimento_total",
  "limite_fisico", "limite_infra", "limite_experiencia", "limite_mercado",
  "caminho_leitura",
];

const m2 = (x: number) => `${fmtN(x, 2)} m²`;

export function calcular(r: Respostas): ResultadoCalculos {
  const calculos: Calculo[] = [];

  // 1. area_usavel
  const areaMat = num(r, "area_matricula");
  const subsFaltando = SUBS.filter(([id]) => num(r, id) === null).map(([, n]) => n);
  const somaSubs = SUBS.reduce((s, [id]) => s + (num(r, id) ?? 0), 0);
  const areaUsavel = areaMat !== null && areaMat > 0 ? areaMat - somaSubs : null;
  const provisoria = subsFaltando.length > 0;
  {
    let t: string;
    let alerta: Calculo["alerta"];
    if (areaUsavel === null) {
      t = "Falta a área da matrícula: sem ela não dá para subtrair nada.";
    } else {
      t = `Área que você pode usar: ${m2(areaMat as number)} da matrícula menos ${m2(somaSubs)} de subtrações = ${m2(areaUsavel)}.`;
      if (provisoria) t += ` No máximo e provisória: ${juntar(subsFaltando)} em Não sei entrou como zero. Cada Não sei vira tarefa.`;
      if (areaUsavel <= 0) {
        t += " As subtrações passam da área da matrícula: confira os números com o CAR e o topógrafo.";
        alerta = "critico";
      }
    }
    calculos.push({
      id: "area_usavel", rotulo: "Área que você pode usar", valor: areaUsavel, texto: t, alerta,
      detalhes: { subtracoes_m2: somaSubs, provisoria, em_nao_sei: subsFaltando },
    });
  }
  const usavelPos = areaUsavel !== null && areaUsavel > 0 ? areaUsavel : null;

  // 2. pct_usavel
  const pctUsavel = div(usavelPos, areaMat);
  calculos.push({
    id: "pct_usavel",
    rotulo: "Quanto da matrícula vira negócio",
    valor: pctUsavel === null ? null : pctUsavel * 100,
    texto: pctUsavel === null
      ? "Sem a área usável, a porcentagem fica em branco."
      : `${fmtPct(pctUsavel)} da matrícula vira negócio${provisoria ? " (no máximo, provisório)" : ""}.`,
  });

  // capacidade é usada pelos três preços: calcula antes, mostra na ordem do JSON.
  const lims = LIMITES.map(([id, nome]) => ({ id, nome, v: num(r, id) }));
  const conhecidos = lims.filter((l) => l.v !== null) as { id: string; nome: string; v: number }[];
  const faltamLim = lims.filter((l) => l.v === null);
  const capacidade = conhecidos.length ? Math.min(...conhecidos.map((l) => l.v)) : null;
  const mandam = capacidade === null ? [] : conhecidos.filter((l) => l.v === capacidade);

  // 3. tres_precos
  const preco = num(r, "preco_terreno");
  const pM2Total = div(preco, areaMat);
  const pM2Usavel = div(preco, usavelPos);
  const pUnidade = div(preco, capacidade);
  {
    let t: string;
    if (preco === null) t = "Falta o valor do terreno: os três preços ficam em branco.";
    else {
      const partes = [
        pM2Total !== null ? `${brl(pM2Total)} por m² total` : "por m² total em branco",
        pM2Usavel !== null ? `${brl(pM2Usavel)} por m² que você pode usar` : "por m² usável em branco (falta a área usável)",
        pUnidade !== null ? `${brl(pUnidade)} por unidade possível` : "por unidade em branco (falta a capacidade)",
      ];
      t = `O mesmo terreno de ${brl(preco)}: ${partes.join("; ")}. O preço por m² usável é o número da negociação; o preço por unidade conversa com o investimento.`;
    }
    calculos.push({
      id: "tres_precos", rotulo: "Os três preços do terreno", valor: pM2Usavel, texto: t,
      detalhes: { preco_m2_total: pM2Total, preco_m2_usavel: pM2Usavel, preco_por_unidade: pUnidade },
    });
  }

  // 4. capacidade
  {
    let t: string;
    if (capacidade === null) t = "Nenhum dos quatro limites foi preenchido: a capacidade fica em branco. O de mercado se mede na Aula 3.";
    else {
      t = `O lugar aguenta ${fmtN(capacidade)} unidades: é o menor dos limites. Quem manda é o limite ${juntar(mandam.map((l) => l.nome))}.`;
      if (faltamLim.length) {
        t += ` Provisória: falta o limite ${juntar(faltamLim.map((l) => l.nome))}.`;
        if (faltamLim.some((l) => l.id === "limite_mercado")) t += " O de mercado, medir na Aula 3.";
      }
    }
    calculos.push({
      id: "capacidade", rotulo: "Quantas unidades o lugar aguenta, e qual limite manda", valor: capacidade, texto: t,
      detalhes: { limite_que_manda: mandam.map((l) => l.id), provisoria: faltamLim.length > 0, limites_faltando: faltamLim.map((l) => l.id) },
    });
  }

  // 5. ilusao_preco
  const fisico = num(r, "limite_fisico");
  const ilusao = div(fisico, capacidade);
  calculos.push({
    id: "ilusao_preco",
    rotulo: "Quanto o terreno parece mais barato se contar pelo que cabe",
    valor: ilusao,
    texto: ilusao === null
      ? "Falta o limite físico ou a capacidade para comparar."
      : `Contar pelo limite físico (${fmtN(fisico as number)} unidades) em vez da capacidade (${fmtN(capacidade as number)}) faz o terreno parecer ${fmtN(ilusao, 2)} vezes mais barato do que é.`,
  });

  // 6. peso_terreno
  const invest = num(r, "investimento_total");
  const peso = div(preco, invest);
  {
    let t: string;
    let alerta: Calculo["alerta"];
    const regra = "Regra de bolso: até 10% fora do alerta; de 10% a 20% sensível; acima de 20% alerta aceso.";
    if (peso === null) t = `Peso a calcular: falta ${preco === null ? "o valor do terreno" : "o investimento total"}. ${regra}`;
    else if (peso > 0.2) { t = `O terreno pesa ${fmtPct(peso)} do investimento total: alerta aceso. ${regra}`; alerta = "critico"; }
    else if (peso > 0.1) { t = `O terreno pesa ${fmtPct(peso)} do investimento total: zona da regra de bolso, sensível. ${regra}`; alerta = "atencao"; }
    else { t = `O terreno pesa ${fmtPct(peso)} do investimento total: fora do alerta. ${regra}`; alerta = "ok"; }
    calculos.push({ id: "peso_terreno", rotulo: "Quanto o terreno pesa no investimento total", valor: peso === null ? null : peso * 100, texto: t, alerta });
  }

  // 7. documentos_faltando
  const temDocs = lista(r, "documentos", DOCS.map(([v]) => v));
  const faltamDocs = DOCS.filter(([v]) => !temDocs.includes(v));
  calculos.push({
    id: "documentos_faltando",
    rotulo: "Documentos que faltam",
    valor: faltamDocs.length ? faltamDocs.map(([, n]) => n).join(", ") : "nenhum",
    texto: faltamDocs.length ? `Faltam ${faltamDocs.length} de 4 documentos: ${juntar(faltamDocs.map(([, n]) => n))}.` : "Os quatro documentos estão na mão.",
    alerta: faltamDocs.some(([v]) => v === "matricula" || v === "car") ? "atencao" : faltamDocs.length ? undefined : "ok",
    detalhes: { faltam: faltamDocs.map(([v]) => v) },
  });

  // 8. conta_nao_sei
  const ns = CAMPOS_NS.filter((id) => falta(r[id]));
  calculos.push({
    id: "conta_nao_sei",
    rotulo: "Quantos Não sei",
    valor: ns.length,
    texto: ns.length ? `${ns.length} Não sei (ou em branco). Cada um vira uma tarefa: em leitura de terreno, não saber custa igual a estar errado.` : "Nenhum Não sei.",
    detalhes: { campos: ns },
  });

  // 9. veredito_sugerido
  const caminho = escolha(r, "caminho_leitura");
  const faltaMatCar = faltamDocs.some(([v]) => v === "matricula" || v === "car");
  let v: Veredito;
  let motivo: string;
  if (caminho === "trocar") {
    v = "pausar"; motivo = "Caminho \"trocar de terreno\": existe um limite que não se resolve. Muda-se o terreno, não o projeto.";
  } else if (caminho === "renegociar" || (peso !== null && peso > 0.2)) {
    v = "ajustar";
    motivo = caminho === "renegociar"
      ? "Caminho \"renegociar\": o terreno pesa demais no investimento."
      : `O terreno pesa ${fmtPct(peso as number)} do investimento, acima de 20% pela regra de bolso.`;
  } else if (peso === null || caminho === "investigar" || ns.length > 0 || faltaMatCar) {
    v = "testar";
    const m: string[] = [];
    if (caminho === "investigar") m.push("o caminho é investigar antes");
    if (ns.length > 0) m.push(`há ${ns.length} Não sei`);
    if (faltaMatCar) m.push("falta matrícula ou CAR");
    if (peso === null && ns.length === 0) m.push("o peso do terreno está em branco");
    motivo = `Testar: ${juntar(m)}. Não desenha nem põe dinheiro antes de medir.`;
  } else {
    v = "avancar";
    motivo = "Caminho \"seguir\": área usável com fonte, os quatro limites preenchidos e o peso do terreno fora do alerta.";
  }
  calculos.push({ id: "veredito_sugerido", rotulo: "Veredito sugerido pela página", valor: v, texto: motivo });

  return { calculos: calculos.map((c) => fechar(c)), veredito_sugerido: v, motivo_veredito: motivo };
}

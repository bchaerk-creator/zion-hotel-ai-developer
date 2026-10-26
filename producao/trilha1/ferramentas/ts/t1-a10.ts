// Trilha 1 · Aula 10 · Capital e captação (slug 1-10). Fonte: exercicios/aula-10.json.
import type { Calculo, ResultadoCalculos, Respostas, Veredito } from "./types";
import { brl, div, escolha, fechar, fmtN, fmtPct, juntar, num } from "./util";

const NOTAS: [string, string][] = [
  ["nota_capex", "CAPEX"],
  ["nota_receita", "Receita"],
  ["nota_ebitda", "EBITDA"],
  ["nota_tir", "TIR"],
  ["nota_viabilidade", "Viabilidade"],
];
const PERG: [string, string][] = [
  ["p1_construir", "o que construir, quantas unidades e para quem"],
  ["p2_diaria", "qual diária o projeto precisa, com dado testado"],
  ["p3_retorno", "em quanto tempo o investimento retorna, nos três cenários"],
];

function faixaScore(s: number): string {
  if (s >= 85) return "excepcional";
  if (s >= 70) return "forte: avançar ajustando as dimensões mais fracas";
  if (s >= 55) return "não captar ainda";
  if (s >= 40) return "repensar o modelo";
  return "reprovado nesta forma";
}

export function calcular(r: Respostas): ResultadoCalculos {
  const calculos: Calculo[] = [];

  // 1. tres_perguntas
  const resp = PERG.map(([id, n]) => ({ id, n, v: escolha(r, id) }));
  const nao = resp.filter((p) => p.v === "nao");
  const semResp = resp.filter((p) => p.v === null || p.v === "nao_sei");
  const algumNao = nao.length > 0;
  calculos.push({
    id: "tres_perguntas", rotulo: "As três perguntas do capital", valor: algumNao,
    texto: algumNao
      ? `Você respondeu não para: ${juntar(nao.map((p) => p.n))}. Qualquer não: falta a decisão anterior ao capital, não o capital.`
      : semResp.length
        ? `Em aberto: ${juntar(semResp.map((p) => p.n))}. Só com três sim falta capital, e o caminho é captação estruturada.`
        : "Três sim: falta capital, e o caminho é captação estruturada.",
    alerta: algumNao ? "critico" : semResp.length ? "atencao" : "ok",
  });

  // 2. score
  const notas = NOTAS.map(([id, n]) => ({ id, n, v: num(r, id) }));
  const validas = notas.every((x) => x.v !== null && x.v >= 0 && x.v <= 100);
  const score = validas ? 0.2 * notas.reduce((s, x) => s + (x.v as number), 0) : null;
  {
    const lista = notas.map((x) => `${x.n} ${x.v === null ? "em branco" : fmtN(x.v, 1)}`).join("; ");
    const regua = "Faixas: 85 a 100 excepcional; 70 a 84 forte; 55 a 69 não captar ainda; 40 a 54 repensar o modelo; abaixo de 40 reprovado nesta forma.";
    calculos.push({
      id: "score", rotulo: "Zion Score de Investimento", valor: score === null ? "em branco" : score,
      texto: score === null
        ? `Notas uma a uma: ${lista}. Sem as cinco notas (de 0 a 100), o score fica em branco. ${regua}`
        : `Notas uma a uma: ${lista}. Score: ${fmtN(score, 1)}, ${faixaScore(score)}. ${regua}`,
      alerta: score === null ? undefined : score >= 70 ? "ok" : score >= 40 ? "atencao" : "critico",
      detalhes: Object.fromEntries(notas.map((x) => [x.id, x.v])),
    });
  }

  // 3. regra_prevalece
  const cons = escolha(r, "conservador_fecha");
  calculos.push({
    id: "regra_prevalece", rotulo: "A regra do conservador", valor: cons === "nao" ? "não captar ainda" : null,
    texto: cons === "nao" ? "O conservador não fecha: não captar ainda, qualquer que seja o score." : cons === "sim" ? "O conservador fecha: a regra não trava a captação." : "Em aberto: o conservador da Aula 9 fecha? Se não fechar, não captar ainda, qualquer que seja o score.",
    alerta: cons === "nao" ? "critico" : cons === "sim" ? "ok" : undefined,
  });

  // 4. colchao
  const capex = num(r, "capex"), giro = num(r, "giro"), menor = num(r, "menor_saldo");
  const reforco = capex !== null && menor !== null ? Math.max(0, 0.1 * capex - menor) : null;
  const giroAj = reforco !== null && giro !== null ? giro + reforco : null;
  calculos.push({
    id: "colchao", rotulo: "Reforço de giro para o colchão de 10%", valor: reforco,
    texto: reforco === null ? "Falta o CAPEX ou o menor saldo." : reforco > 0
      ? `Para o menor saldo chegar a 10% do CAPEX, o giro precisa de mais ${brl(reforco)}: giro ajustado de ${giroAj === null ? "em branco (falta o giro)" : brl(giroAj)}.`
      : `O menor saldo já passa de 10% do CAPEX: sem reforço. Giro de ${giro === null ? "em branco" : brl(giro)}.`,
    alerta: reforco === null ? undefined : reforco > 0 ? "atencao" : "ok",
    detalhes: { giro_ajustado: giroAj },
  });

  // 5. regua
  const nec = capex !== null && giroAj !== null ? capex + 0 + giroAj + 0 : null;
  const proprio = num(r, "capital_proprio");
  const externo = nec !== null && proprio !== null ? nec - proprio : null;
  const ext0 = externo !== null ? Math.max(0, externo) : null;
  const c2 = ext0 !== null ? ext0 / (1 - 0.02) : null;
  const c5 = ext0 !== null ? ext0 / (1 - 0.05) : null;
  {
    let t: string;
    if (nec === null) t = "Falta o CAPEX, o giro ou o menor saldo para a Régua do Quanto Captar.";
    else if (externo === null) t = `Necessidade antes do capital próprio: ${brl(nec)} (CAPEX + giro ajustado; terreno já pago e reserva já no CAPEX). Sem o capital próprio, o pedido não pode ser escrito.`;
    else if (externo <= 0) t = `Necessidade: ${brl(nec)}. O capital próprio cobre a necessidade: não há valor a captar.`;
    else t = `Necessidade: ${brl(nec)}. Menos o capital próprio de ${brl(proprio as number)}, faltam ${brl(externo)} de fora. Com o custo da captação: ${brl(c2 as number)} (2%) a ${brl(c5 as number)} (5%).`;
    calculos.push({ id: "regua", rotulo: "Régua do Quanto Captar", valor: externo === null ? nec : ext0, texto: t, detalhes: { necessidade_antes: nec, externo, com_custo_2: c2, com_custo_5: c5, antes_do_capital_proprio: proprio === null } });
  }

  // 6. participacao
  const contribDoc = num(r, "contribuicao_documentada");
  const part = ext0 !== null && contribDoc !== null ? div(ext0, contribDoc + ext0) : null;
  calculos.push({
    id: "participacao", rotulo: "Quanto ficaria com quem aporta (conta do tamanho do problema)", valor: part === null ? null : part * 100,
    texto: part === null
      ? `Falta ${juntar([ext0 === null && "o valor a captar", contribDoc === null && "o que você põe no projeto, documentado"].filter(Boolean) as string[]) || "dado"} para a conta.`
      : `Se ${brl(ext0 as number)} viessem de fora contra ${brl(contribDoc as number)} seus, quem aporta ficaria com ${fmtPct(part, 2)}. Não é proposta nem valuation: mostra o custo de captar antes de o projeto estar pronto.`,
  });

  // 7. veredito_sugerido
  const p2 = escolha(r, "p2_diaria");
  let v: Veredito, motivo: string;
  if ((score !== null && score < 40) || (p2 === "sim" && cons === "nao")) {
    v = "pausar"; motivo = score !== null && score < 40 ? `Nota ${fmtN(score, 1)}, abaixo de 40: reprovado nesta forma. Pausa e redesenha.` : "A diária já foi testada e o conservador continua sem fechar: não procura capital para este desenho. Pausa e redesenha, ou declara projeto de patrimônio e de vida.";
  } else if (algumNao || semResp.length > 0 || cons === null || cons === "nao_sei") {
    v = "testar";
    motivo = algumNao ? "Alguma das três perguntas é não: não falta capital, falta a decisão anterior. Testa, e não capta." : "Testar: há pergunta do capital ou o conservador em aberto.";
  } else if (cons === "nao" || score === null || score < 70) {
    v = "ajustar";
    motivo = `Ajustar: ${juntar([cons === "nao" && "o conservador ainda não fecha", score === null && "a nota está em branco", score !== null && score < 70 && `a nota é ${fmtN(score, 1)} (${faixaScore(score)})`].filter(Boolean) as string[])}.`;
  } else {
    v = "avancar"; motivo = "Três sim, conservador que fecha e nota de 70 ou mais: procurar capital estruturado, com a necessidade exata na frase do pedido.";
  }
  calculos.push({ id: "veredito_sugerido", rotulo: "Veredito sugerido pela página", valor: v, texto: motivo });

  return { calculos: calculos.map((c) => fechar(c)), veredito_sugerido: v, motivo_veredito: motivo };
}

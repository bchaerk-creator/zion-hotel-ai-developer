// Trilha 1 · Aula 6 · Masterplan (slug 1-6). Fonte: exercicios/aula-06.json.
import type { Calculo, ResultadoCalculos, Respostas, Veredito } from "./types";
import { div, escolha, fechar, fmtN, fmtPct, juntar, lista, num } from "./util";

const GESTOS: [string, string][] = [
  ["marcado", "marcado no desenho"],
  ["fotografado", "terreno fotografado com data"],
  ["clausula", "cláusula pedida ao advogado"],
];
const APOIO: [string, string][] = [
  ["rouparia_lavanderia", "rouparia e lavanderia"],
  ["deposito", "depósito seco"],
  ["residuo", "resíduo com acesso externo"],
  ["copa_vestiario", "copa e vestiário da equipe"],
  ["estac_servico", "estacionamento de serviço"],
  ["oficina", "oficina e ferramentas"],
  ["gas_reservatorio", "abrigo de gás e reservatório"],
];
const GATILHO = ["demanda", "caixa", "maturidade"];

export function calcular(r: Respostas): ResultadoCalculos {
  const calculos: Calculo[] = [];

  // 1. pct_apoio
  const u = num(r, "unidades_fase1"), afu = num(r, "area_fechada_unidade"), apoio = num(r, "area_apoio");
  const total = u !== null && afu !== null && apoio !== null ? u * afu + apoio : null;
  const pApoio = div(apoio, total);
  {
    let t: string, alerta: Calculo["alerta"];
    const regua = "Régua: entre 15% e 25% da área fechada.";
    if (pApoio === null) t = `Falta ${apoio === null ? "a área de apoio" : "unidades ou área fechada por unidade"}. ${regua}`;
    else {
      t = `Apoio de ${fmtN(apoio as number)} m² sobre ${fmtN(total as number)} m² de área fechada: ${fmtPct(pApoio)}. `;
      if (pApoio < 0.15) { t += "Abaixo de 15%: o apoio vai faltar e virar puxadinho."; alerta = "critico"; }
      else if (pApoio > 0.25) { t += "Acima de 25%: conferir a base."; alerta = "atencao"; }
      else { t += "Dentro da faixa de 15% a 25%."; alerta = "ok"; }
    }
    calculos.push({ id: "pct_apoio", rotulo: "Área de apoio sobre a área fechada", valor: pApoio === null ? null : pApoio * 100, texto: t, alerta, detalhes: { area_fechada_total_m2: total } });
  }

  // 2. rede_vs_projeto
  const rede = num(r, "rede_para"), completo = num(r, "unidades_projeto_completo");
  const redeAlerta = rede !== null && completo !== null ? rede < completo : null;
  calculos.push({
    id: "rede_vs_projeto", rotulo: "Rede contra o projeto completo", valor: redeAlerta,
    texto: redeAlerta === null
      ? "Falta para quantas unidades a rede está dimensionada ou quantas tem o projeto completo."
      : redeAlerta
        ? `Alerta: rede para ${fmtN(rede as number)} unidades e projeto completo de ${fmtN(completo as number)}. A fase dois vai reabrir vala e refazer caminho com hóspede ao lado.`
        : `A rede atende as ${fmtN(completo as number)} unidades do projeto completo.`,
    alerta: redeAlerta ? "critico" : redeAlerta === false ? "ok" : undefined,
  });

  // 3. gestos
  const g = lista(r, "tres_gestos", GESTOS.map(([v]) => v));
  const gFaltam = GESTOS.filter(([v]) => !g.includes(v));
  calculos.push({
    id: "gestos", rotulo: "Gestos do nunca",
    valor: gFaltam.length ? gFaltam.map(([, n]) => n).join(", ") : "nenhum",
    texto: gFaltam.length ? `Falta: ${juntar(gFaltam.map(([, n]) => n))}. Faltando qualquer um, preservar ainda é só intenção.` : "Os três gestos do nunca estão feitos.",
    alerta: gFaltam.length ? "atencao" : "ok",
    detalhes: { faltam: gFaltam.map(([v]) => v) },
  });

  // 4. esquecidos
  const res = lista(r, "apoio_resolvido", APOIO.map(([v]) => v));
  const esq = APOIO.filter(([v]) => !res.includes(v));
  calculos.push({
    id: "esquecidos", rotulo: "Itens de apoio sem decisão", valor: esq.length,
    texto: esq.length ? `${esq.length} de 7 itens de apoio ainda sem decisão: ${juntar(esq.map(([, n]) => n))}.` : "Os sete itens de apoio têm lugar ou foram deixados de fora por decisão.",
    alerta: esq.length ? "atencao" : "ok",
    detalhes: { faltam: esq.map(([v]) => v) },
  });

  // 5. gatilho
  const esc = lista(r, "gatilho_escrito", GATILHO).length;
  calculos.push({
    id: "gatilho", rotulo: "Condições do gatilho escritas", valor: esc,
    texto: esc < 3 ? `${esc} de 3 condições do gatilho escritas. Menos de 3: uma ou duas não bastam.` : "As três condições do gatilho da fase dois estão escritas.",
    alerta: esc < 3 ? "atencao" : "ok",
  });

  // 6. veredito_sugerido
  const consulta = escolha(r, "consulta_previa");
  const caminhos = escolha(r, "caminhos");
  const dia = escolha(r, "dia_simulado");
  const estacas = escolha(r, "caminhada_estacas");
  const cond = num(r, "condicionantes");
  let v: Veredito, motivo: string;
  if (consulta === "tira") {
    v = "pausar"; motivo = "A consulta prévia ou o mapa ambiental tiraram as unidades do ponto que sustenta a promessa: pausa e volta ao produto.";
  } else if (caminhos === "cruzam" || (pApoio !== null && pApoio < 0.15) || redeAlerta === true) {
    v = "ajustar";
    const m = [caminhos === "cruzam" && "os caminhos se cruzam", pApoio !== null && pApoio < 0.15 && "o apoio ficou abaixo de 15%", redeAlerta && "a rede foi feita só para a fase um"].filter(Boolean) as string[];
    motivo = `Ajustar: ${juntar(m)}.`;
  } else if (dia !== "sim" || estacas !== "sim" || caminhos !== "nao_cruzam" || cond === null || cond === 0 || pApoio === null || redeAlerta === null || consulta === null || consulta === "nao_sei") {
    v = "testar";
    const m = [
      dia !== "sim" && "o dia de troca de hóspede simulado no papel",
      estacas !== "sim" && "a caminhada com estacas",
      caminhos !== "nao_cruzam" && "desenhar os dois caminhos",
      (cond === null || cond === 0) && "as condicionantes numeradas no briefing",
      pApoio === null && "a área de apoio",
      redeAlerta === null && "a rede contra o projeto completo",
      (consulta === null || consulta === "nao_sei") && "a situação da consulta prévia",
    ].filter(Boolean) as string[];
    motivo = `Testar: falta pôr à prova ${juntar(m)}.`;
  } else {
    v = "avancar"; motivo = "O apoio está na faixa, os caminhos não se cruzam, a rede é para o projeto completo e o briefing tem as condicionantes. Leva o briefing ao arquiteto, com as pendências nomeadas.";
  }
  calculos.push({ id: "veredito_sugerido", rotulo: "Veredito sugerido pela página", valor: v, texto: motivo });

  return { calculos: calculos.map((c) => fechar(c)), veredito_sugerido: v, motivo_veredito: motivo };
}

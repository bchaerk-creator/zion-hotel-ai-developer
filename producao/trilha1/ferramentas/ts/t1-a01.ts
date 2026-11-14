// Trilha 1 · Aula 1 · Marco Zero (slug 1-1). Fonte: exercicios/aula-01.json.
import type { Calculo, ResultadoCalculos, Respostas } from "./types";
import { escolha, fechar, fmtN, fmtPct, juntar, lista, num, pct } from "./util";

const PERGUNTAS: Record<string, string> = {
  produto: "qual é o melhor produto para o meu terreno",
  custo: "quanto custa",
  retorno: "quanto retorna",
  lucro: "quanto de lucro dá",
  tempo: "em quanto tempo",
};

const FAIXAS: Record<string, { min: number; max: number; nome: string }> = {
  fds: { min: 0.35, max: 0.4, nome: "só nos fins de semana" },
  fds_feriados: { min: 0.5, max: 0.6, nome: "fins de semana, feriados, festas e datas festivas" },
  extraordinaria: { min: 0.65, max: 0.85, nome: "procura extraordinária, comprovada pelo mercado" },
};

const REGUA_TXT =
  "Régua da média do ano: 35% a 40% vende só nos fins de semana; 50% a 60% com fins de semana, feriados, festas e datas festivas; 65% a 85% só com procura extraordinária comprovada.";

function letraOuNaoSei(v: string | null): string {
  return v === null || v === "nao_sei" ? "não sei" : v;
}

export function calcular(r: Respostas): ResultadoCalculos {
  const calculos: Calculo[] = [];

  // 1. respostas_investidor
  const respondidas = lista(r, "perguntas_investidor", Object.keys(PERGUNTAS));
  const n = respondidas.length;
  const faltam = Object.keys(PERGUNTAS).filter((k) => !respondidas.includes(k)).map((k) => PERGUNTAS[k]);
  calculos.push({
    id: "respostas_investidor",
    rotulo: "Quantas das cinco perguntas você responde",
    valor: n,
    texto:
      `Você responde ${n} de 5 perguntas do investidor com número.` +
      (faltam.length ? ` Faltam: ${juntar(faltam)}. Valem até para quem vai investir sozinho.` : " As cinco têm resposta: confira de onde veio cada número."),
    detalhes: { respondidas, faltam },
  });

  // 2. linha_ficha
  const sit = escolha(r, "situacao_letra");
  const vit = escolha(r, "vitrine");
  const etapa = escolha(r, "etapa_ordem");
  const linha = `${letraOuNaoSei(sit)}, ${n} de 5, ${letraOuNaoSei(vit)}, etapa ${letraOuNaoSei(etapa)}`;
  calculos.push({
    id: "linha_ficha",
    rotulo: "A sua ficha em uma linha",
    valor: linha,
    texto: `A sua ficha em uma linha, no formato do chat: "${linha}".`,
  });

  // 3. comeco_recomendado
  const nota = num(r, "nota_21_pontos");
  let comeco: string | null = null;
  let txtComeco: string;
  if (nota === null) {
    txtComeco = "Sem nota: abra o diagnóstico de 21 pontos pelo link do chat e escreva a sua nota. A página não sugere etapa sem ela.";
  } else if (nota < 10) {
    comeco = "Começar pela etapa 1 da Ordem, Ler o terreno";
    txtComeco = `A sua nota é ${fmtN(nota)} de 21. Quem tirou menos de 10 começa pela primeira etapa da Ordem: Ler o terreno.`;
  } else {
    comeco = "Seguir a etapa marcada, conferindo a anterior";
    txtComeco = `A sua nota é ${fmtN(nota)} de 21. Siga a etapa que você marcou, conferindo a anterior: nenhuma etapa avança sem a anterior concluída.`;
  }
  calculos.push({ id: "comeco_recomendado", rotulo: "Por onde começar pela nota de 21 pontos", valor: comeco, texto: txtComeco });

  // 4. regua_ocupacao
  const perfil = escolha(r, "perfil_demanda");
  const ocup = pct(r, "ocupacao_imaginada");
  const faixa = perfil && FAIXAS[perfil] ? FAIXAS[perfil] : null;
  if (!faixa || ocup === null) {
    const falt = [!faixa ? "quando o movimento acontece" : "", ocup === null ? "a ocupação média imaginada" : ""].filter(Boolean);
    calculos.push({
      id: "regua_ocupacao",
      rotulo: "A sua ocupação imaginada contra a régua",
      valor: null,
      texto: `${REGUA_TXT} Para comparar, falta ${juntar(falt)}. Regra de ouro: use a média dos 12 meses, nunca o mês mais cheio.`,
    });
  } else {
    const alertaAlto = ocup > faixa.max + 1e-12;
    const alertaExtra = ocup >= 0.65 - 1e-12 && perfil !== "extraordinaria";
    const faixaTxt = `${fmtPct(faixa.min, 0)} a ${fmtPct(faixa.max, 0)}`;
    let t = `Você imagina ${fmtPct(ocup)} de ocupação média no ano, e o seu movimento é ${faixa.nome} (faixa de ${faixaTxt}). `;
    if (alertaExtra) {
      t += "Alerta: 65% ou mais só com procura extraordinária comprovada pelo mercado. ";
    }
    if (alertaAlto) {
      t += "Acima da faixa: provavelmente é o mês mais cheio, não a média do ano. Quatro meses cheios não querem dizer o ano todo cheio.";
    } else if (ocup < faixa.min - 1e-12) {
      t += "Abaixo da faixa da régua para esse movimento.";
    } else {
      t += "Dentro da faixa: coerente.";
    }
    calculos.push({
      id: "regua_ocupacao",
      rotulo: "A sua ocupação imaginada contra a régua",
      valor: alertaAlto || alertaExtra,
      texto: t.trim(),
      alerta: alertaExtra ? "critico" : alertaAlto ? "atencao" : "ok",
      detalhes: { ocupacao_pct: ocup * 100, faixa_min_pct: faixa.min * 100, faixa_max_pct: faixa.max * 100, alerta_alto: alertaAlto, alerta_extra: alertaExtra },
    });
  }

  return {
    calculos: calculos.map((c) => fechar(c)),
    veredito_sugerido: "nao_se_aplica",
    motivo_veredito:
      "A página 0 não tem veredito na fonte. Ela mostra a etapa de início pela nota de 21 pontos e pela Ordem Zion; o primeiro veredito da trilha nasce na Aula 2.",
  };
}

// Trilha 1 · Aula 4 · Produto (slug 1-4). Fonte: exercicios/aula-04.json.
import type { Calculo, ResultadoCalculos, Respostas, Veredito } from "./types";
import { div, escolha, fechar, fmtN, fmtPct, juntar, lista, num, texto } from "./util";

/** Lista negra da fonte, com plural e feminino, comparada sem acento e sem maiúscula. */
const LISTA_NEGRA: [string, RegExp][] = [
  ["único", /\bunic(o|a|os|as)\b/],
  ["incrível", /\bincrive(l|is)\b/],
  ["exclusivo", /\bexclusiv(o|a|os|as)\b/],
  ["inesquecível", /\binesquecive(l|is)\b/],
  ["encantador", /\bencantador(a|as|es)?\b/],
  ["premium", /\bpremiums?\b/],
];
const REQUISITOS: [string, string][] = [
  ["so_aqui", "só existe aqui"],
  ["sem_voce", "acontece sem você presente"],
  ["uma_frase", "cabe numa frase"],
  ["foto", "é fotografável"],
];

function semAcento(s: string): string {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
}

export function calcular(r: Respostas): ResultadoCalculos {
  const calculos: Calculo[] = [];

  // 1. lista_negra
  const frase = texto(r, "frase_produto");
  const achadas = frase === null ? [] : LISTA_NEGRA.filter(([, re]) => re.test(semAcento(frase))).map(([p]) => p);
  calculos.push({
    id: "lista_negra", rotulo: "Palavras da lista negra na frase",
    valor: frase === null ? null : achadas.join(", "),
    texto: frase === null
      ? "Falta a frase em três partes."
      : achadas.length
        ? `Achei ${juntar(achadas)} na sua frase: reescreva. Se a frase morrer sem a palavra, ela não tinha conteúdo.`
        : "Nenhuma palavra da lista negra na frase.",
    alerta: frase === null ? undefined : achadas.length ? "atencao" : "ok",
    detalhes: { achadas },
  });

  // 2. momento_ok
  const req = lista(r, "requisitos_momento", REQUISITOS.map(([v]) => v));
  const momentoOk = req.length === 4;
  const faltamReq = REQUISITOS.filter(([v]) => !req.includes(v)).map(([, n]) => n);
  calculos.push({
    id: "momento_ok", rotulo: "O momento passa nos quatro requisitos?", valor: momentoOk,
    texto: momentoOk ? "O momento passa nos quatro requisitos." : `O momento passa em ${req.length} de 4. Falta: ${juntar(faltamReq)}.`,
    alerta: momentoOk ? "ok" : "atencao",
  });

  // 3. conta_provas
  const provasTxt = texto(r, "provas");
  const contaProvas = provasTxt === null ? null : provasTxt.split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== "").length;
  calculos.push({
    id: "conta_provas", rotulo: "Quantas provas", valor: contaProvas,
    texto: contaProvas === null
      ? "Nenhuma prova escrita. Menos de 3: a promessa é maior que o produto."
      : contaProvas < 3
        ? `${contaProvas} prova(s). Menos de 3: a promessa é maior que o produto. Reduza a promessa ou aumente o produto.`
        : `${contaProvas} provas: a promessa tem sustentação.`,
    alerta: (contaProvas ?? 0) < 3 ? "atencao" : "ok",
  });

  // 4. faixa_area
  const area = num(r, "area_interna");
  let faixa: string | null = null;
  if (area !== null) {
    if (area >= 22 && area <= 30) faixa = "suíte de casal (22 a 30 m²)";
    else if (area >= 32 && area <= 45) faixa = "cabana de casal com sala (32 a 45 m²)";
    else if (area >= 60 && area <= 85) faixa = "familiar de dois quartos (60 a 85 m²)";
    else faixa = "fora das faixas da fonte";
  }
  calculos.push({
    id: "faixa_area", rotulo: "Em que faixa de tamanho a unidade cai", valor: faixa,
    texto: area === null ? "Falta a área interna da unidade." : `${fmtN(area)} m² internos: ${faixa}.`,
    alerta: faixa === "fora das faixas da fonte" ? "atencao" : undefined,
  });

  // 5. mix
  const u = num(r, "unidades_abertura");
  let mix: string | null = null;
  const det: Record<string, number | null> = { principal: null, semana: null };
  if (u !== null) {
    if (u <= 4) mix = "tudo igual; o segundo público entra por produto e preço";
    else {
      const principal = Math.round((u * 2) / 3);
      det.principal = principal; det.semana = u - principal;
      mix = `${principal} para o público principal e ${u - principal} para o público da semana`;
    }
  }
  calculos.push({
    id: "mix", rotulo: "O mix pela regra de partida", valor: mix,
    texto: u === null ? "Falta quantas unidades abrem na primeira fase." : `Com ${fmtN(u)} unidades na abertura: ${mix}.`,
    detalhes: det,
  });

  // 6. hipotese_vs_regiao
  const reg = num(r, "diaria_regiao"), hip = num(r, "diaria_hipotese");
  const q = div(hip, reg);
  calculos.push({
    id: "hipotese_vs_regiao", rotulo: "Quanto a hipótese fica acima da região", valor: q === null ? null : (q - 1) * 100,
    texto: q === null
      ? "Falta a diária da região ou a sua hipótese."
      : `A sua hipótese fica ${fmtPct(Math.abs(q - 1))} ${q - 1 >= 0 ? "acima" : "abaixo"} da diária média da região. É nota 1 na escala de evidência: opinião, até ser testada no anúncio e na reserva. Não é promessa de diária.`,
  });

  // 7. veredito_sugerido
  const viz = escolha(r, "teste_vizinho") ?? "nao_fiz";
  const cinco = escolha(r, "teste_cinco_segundos") ?? "nao_fiz";
  let v: Veredito, motivo: string;
  if (viz === "verdadeira_para_algum" || cinco === "diferentes") {
    v = "pausar"; motivo = "A frase continua verdadeira para algum vizinho, ou cada pessoa imaginou uma coisa diferente: pausa e volta ao DNA do destino antes de chamar o arquiteto.";
  } else if (viz === "nao_fiz" || cinco === "nao_fiz" || viz === "nao_sei" || cinco === "nao_sei") {
    v = "testar"; motivo = "Os testes do vizinho e dos cinco segundos ainda não foram feitos: a frase é só hipótese.";
  } else if (achadas.length > 0 || frase === null || (contaProvas ?? 0) < 3 || !momentoOk) {
    v = "ajustar";
    const m = [achadas.length > 0 && "a frase tem palavra da lista negra", frase === null && "falta a frase", (contaProvas ?? 0) < 3 && "faltam provas", !momentoOk && "o momento falha em algum requisito"].filter(Boolean) as string[];
    motivo = `Ajustar: ${juntar(m)}.`;
  } else {
    v = "avancar"; motivo = "A frase passou nos dois testes, o momento cumpre os quatro requisitos e há três provas. Leva o Conceito de Produto ao modelo de negócio, com o preço em teste (nota 1).";
  }
  calculos.push({ id: "veredito_sugerido", rotulo: "Veredito sugerido pela página", valor: v, texto: motivo });

  return { calculos: calculos.map((c) => fechar(c)), veredito_sugerido: v, motivo_veredito: motivo };
}

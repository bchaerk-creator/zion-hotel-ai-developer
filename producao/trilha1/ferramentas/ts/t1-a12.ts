// Trilha 1 · Aula 12 · Dossiê final (slug 1-12). Fonte: exercicios/aula-12.json.
import type { Calculo, ResultadoCalculos, Respostas, Veredito } from "./types";
import { escolha, fechar, juntar, lista } from "./util";

type V = "avancar" | "testar" | "ajustar" | "pausar" | "nao_fiz";
const VALIDOS: V[] = ["avancar", "testar", "ajustar", "pausar", "nao_fiz"];
/** Ordem de restrição da página: pausar > testar > ajustar > avançar. Página não feita conta como testar. */
const PESO: Record<Exclude<Veredito, "nao_se_aplica">, number> = { pausar: 3, testar: 2, ajustar: 1, avancar: 0 };
const NOME: Record<string, string> = { avancar: "avançar", testar: "testar", ajustar: "ajustar", pausar: "pausar", nao_fiz: "não feita" };
const PAGINAS = ["Ficha de entrada", "Território", "Mercado", "Produto", "Modelo de negócio", "Masterplan", "CAPEX", "Receitas e custos", "Viabilidade", "Nota e capital", "Lançamento"];
const ETAPAS: [string, number[]][] = [
  ["Etapa 1 · Ler o terreno", [0, 1, 2]],
  ["Etapa 2 · Desenhar o negócio", [3, 4]],
  ["Etapa 3 · Estruturar o capital", [5, 6, 7, 8, 9]],
  ["Etapa 4 · Lançar", [10]],
];

const efetivo = (v: V): Exclude<Veredito, "nao_se_aplica"> => (v === "nao_fiz" ? "testar" : v);
function maisRestritivo(vs: V[]): Exclude<Veredito, "nao_se_aplica"> | null {
  if (!vs.length) return null;
  return vs.map(efetivo).reduce((a, b) => (PESO[b] > PESO[a] ? b : a));
}

export function calcular(r: Respostas): ResultadoCalculos {
  const calculos: Calculo[] = [];
  const vered: V[] = [];
  for (let p = 1; p <= 10; p++) {
    const e = escolha(r, `veredito_p${p}`);
    vered.push(e !== null && (VALIDOS as string[]).includes(e) ? (e as V) : "nao_fiz");
  }

  // 1. contagem
  const conta: Record<V, number> = { avancar: 0, testar: 0, ajustar: 0, pausar: 0, nao_fiz: 0 };
  vered.forEach((v) => conta[v]++);
  calculos.push({
    id: "contagem", rotulo: "Quantas páginas em cada veredito", valor: VALIDOS.map((v) => `${NOME[v]} ${conta[v]}`).join("; "),
    texto: `Das 10 páginas com veredito: avançar ${conta.avancar}, testar ${conta.testar}, ajustar ${conta.ajustar}, pausar ${conta.pausar}, não feitas ${conta.nao_fiz}.`,
    detalhes: { ...conta },
  });

  // 2. veredito_projeto
  const proj = maisRestritivo(vered) as Exclude<Veredito, "nao_se_aplica">;
  calculos.push({
    id: "veredito_projeto", rotulo: "Veredito do projeto pela página mais fraca", valor: proj,
    texto: `O veredito do projeto é ${NOME[proj]}: o da página mais restritiva, não uma votação. Ordem: pausar, testar, ajustar, avançar; página não feita conta como testar (lacuna a escrever).`,
    alerta: proj === "avancar" ? "ok" : proj === "ajustar" ? "atencao" : "critico",
  });

  // 3. paginas_mais_fracas
  const fracas = vered.map((v, i) => ({ p: i + 1, v })).filter((x) => efetivo(x.v) === proj);
  calculos.push({
    id: "paginas_mais_fracas", rotulo: "Quais páginas dão o ritmo", valor: fracas.map((x) => String(x.p)).join(", "),
    texto: `Dão o ritmo as páginas ${juntar(fracas.map((x) => `${x.p} (${PAGINAS[x.p]}${x.v === "nao_fiz" ? ", não feita" : ""})`))}.`,
    detalhes: { paginas: fracas.map((x) => String(x.p)) },
  });

  // 4. completas
  const todas = Array.from({ length: 11 }, (_, i) => String(i));
  const comp = lista(r, "paginas_completas", todas);
  const faltam = todas.filter((p) => !comp.includes(p));
  calculos.push({
    id: "completas", rotulo: "Páginas completas", valor: comp.length,
    texto: faltam.length ? `${comp.length} de 11 páginas completas (escritas, com data e fonte de cada número). Faltam: ${juntar(faltam.map((p) => `${p} (${PAGINAS[+p]})`))}.` : "As 11 páginas estão completas.",
    alerta: faltam.length ? "atencao" : "ok",
    detalhes: { faltam },
  });

  // 5. por_etapa (a página 0 não tem veredito: entra só na contagem de completas)
  const linhas = ETAPAS.map(([nome, pags]) => {
    const vs = pags.filter((p) => p >= 1).map((p) => vered[p - 1]);
    return { nome, v: maisRestritivo(vs) };
  });
  calculos.push({
    id: "por_etapa", rotulo: "O Dossiê nas quatro etapas da Ordem Zion", valor: linhas.map((l) => `${l.nome}: ${l.v ? NOME[l.v] : "sem veredito"}`).join("; "),
    texto: linhas.map((l) => `${l.nome}: ${l.v ? NOME[l.v] : "sem veredito"}`).join(". ") + ".",
    detalhes: Object.fromEntries(linhas.map((l, i) => [`etapa${i + 1}`, l.v])),
  });

  // 6. veredito_sugerido = veredito_projeto
  let motivo: string;
  if (proj === "pausar") motivo = "Uma página diz pausar: o projeto pausa, mesmo que as outras avancem. Decidir não fazer é um resultado válido.";
  else if (proj === "testar") motivo = conta.nao_fiz ? "Há página que ainda não existe ou diz testar: o projeto está pronto para a decisão, não para a obra. Nenhuma obra, captação, venda ou gasto de lançamento antes do teste." : "A página mais fraca diz testar: o projeto está pronto para a decisão, não para a obra. Nenhuma obra, captação, venda ou gasto de lançamento antes do teste.";
  else if (proj === "ajustar") motivo = "A página mais fraca diz ajustar: mexa no que ela aponta antes de seguir.";
  else motivo = "Todas as páginas dizem avançar.";
  if (proj === "avancar" && faltam.length) motivo += ` Atenção: ${faltam.length} página(s) ainda não estão completas, e avançar pede todas completas, com critério para parar escrito em cada uma.`;
  calculos.push({ id: "veredito_sugerido", rotulo: "Veredito sugerido pela página", valor: proj, texto: motivo });

  return { calculos: calculos.map((c) => fechar(c)), veredito_sugerido: proj, motivo_veredito: motivo };
}

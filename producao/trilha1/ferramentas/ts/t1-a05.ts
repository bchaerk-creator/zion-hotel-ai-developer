// Trilha 1 · Aula 5 · Modelo de negócio (slug 1-5). Fonte: exercicios/aula-05.json.
import type { Calculo, ResultadoCalculos, Respostas, Veredito } from "./types";
import { escolha, fechar, fmtN, juntar, lista, num } from "./util";

const DECISOES: [string, string][] = [
  ["preco", "o preço"],
  ["excecao", "a resposta ao hóspede numa exceção"],
  ["produto", "a decisão de produto"],
];
const REQ_LIC: [string, string][] = [
  ["processos", "processos escritos"],
  ["marca", "marca registrada"],
  ["numeros", "números provados, 12 meses reais"],
  ["suporte", "suporte estruturado"],
];
const SOZINHO = ["eu", "eu_com_local"];

export function calcular(r: Respostas): ResultadoCalculos {
  const calculos: Calculo[] = [];
  const quem = escolha(r, "quem_opera");
  const opSozinho = quem !== null && SOZINHO.includes(quem);
  const u = num(r, "unidades_fase1");

  // 1. alerta_escala
  {
    let valor: boolean | null, t: string;
    if (quem === null || quem === "nao_sei") { valor = null; t = "Falta decidir quem opera a fase um."; }
    else if (!opSozinho) { valor = false; t = "Quem opera não é você: o alerta de escala não se aplica."; }
    else if (u === null) { valor = null; t = "Falta quantas unidades tem a fase um."; }
    else if (u > 4) { valor = true; t = `Alerta aceso: você operando ${fmtN(u)} unidades. Acima de quatro, ou contrata gente e vira gestor, ou o negócio para no tamanho da sua semana.`; }
    else { valor = false; t = `Você operando ${fmtN(u)} unidades: dentro do limite de quatro.`; }
    calculos.push({ id: "alerta_escala", rotulo: "Você mesmo, acima de quatro unidades", valor, texto: t, alerta: valor ? "critico" : valor === false ? "ok" : undefined });
  }
  const alertaEscala = opSozinho && u !== null && u > 4;

  // 2. tres_decisoes
  const fica = lista(r, "fica_comigo", DECISOES.map(([v]) => v));
  const faltam = DECISOES.filter(([v]) => !fica.includes(v));
  calculos.push({
    id: "tres_decisoes", rotulo: "O que fica com o dono no primeiro ano",
    valor: faltam.length ? faltam.map(([, n]) => n).join(", ") : "nenhuma",
    texto: faltam.length ? `Saem da sua mão: ${juntar(faltam.map(([, n]) => n))}. Delegar cedo é delegar o aprendizado.` : "As três decisões ficam com você no primeiro ano.",
    alerta: faltam.length ? "atencao" : "ok",
    detalhes: { faltam: faltam.map(([v]) => v) },
  });

  // 3. adequacao
  const quer = escolha(r, "quer_operar");
  const adequacao = quer === "nao" && opSozinho;
  calculos.push({
    id: "adequacao", rotulo: "Quer operar contra quem opera", valor: adequacao,
    texto: adequacao ? "Alerta: você não quer estar dentro da operação, mas o plano é você operar. O modelo não combina com a vida." : quer === null || quer === "nao_sei" ? "Você ainda não respondeu se quer operar nos próximos cinco anos." : "Quem opera combina com o que você quer.",
    alerta: adequacao ? "critico" : quer === null || quer === "nao_sei" ? undefined : "ok",
  });

  // 4. valorizacao
  const val = escolha(r, "valorizacao_na_conta");
  const valAlerta = val === null || val === "nao_sei" ? null : val === "sim";
  calculos.push({
    id: "valorizacao", rotulo: "Valorização como premissa", valor: valAlerta,
    texto: valAlerta === null ? "Em aberto: a conta depende da valorização do terreno? Se só fecha contando valorização, não fecha." : valAlerta ? "Alerta: a conta depende da valorização. Se só fecha contando valorização, não fecha." : "A conta não depende da valorização do terreno.",
    alerta: valAlerta ? "critico" : valAlerta === false ? "ok" : undefined,
  });

  // 5. portas_saida
  const formal = escolha(r, "receita_formal");
  const informal = formal === null || formal === "nao_sei" ? null : formal === "parte";
  calculos.push({
    id: "portas_saida", rotulo: "Informalidade e portas de saída", valor: informal,
    texto: informal === null ? "Em aberto: a receita vai ser toda formal desde a primeira reserva?" : informal ? "Alerta: parte da receita fica informal, e isso fecha portas de saída (vender, refinanciar, trazer sócio)." : "A receita é toda formal desde a primeira reserva.",
    alerta: informal ? "atencao" : informal === false ? "ok" : undefined,
  });

  // 6. licenciar
  const tem = lista(r, "requisitos_licenciar", REQ_LIC.map(([v]) => v));
  const pode = tem.length === 4;
  calculos.push({
    id: "licenciar", rotulo: "Requisitos para licenciar", valor: tem.length,
    texto: pode ? "Você tem os quatro requisitos para licenciar." : `Você tem ${tem.length} de 4 requisitos. Menos de 4: licenciar não é opção hoje. Falta: ${juntar(REQ_LIC.filter(([v]) => !tem.includes(v)).map(([, n]) => n))}.`,
    detalhes: { pode_licenciar: pode },
  });

  // 7. veredito_sugerido
  const horas = escolha(r, "horas_anotadas");
  const rotina = escolha(r, "rotina_escrita");
  let v: Veredito, motivo: string;
  if ((opSozinho && horas === "sim_nao_cobrem") || rotina === "falhou") {
    v = "pausar"; motivo = "As horas anotadas não cobrem o horário de hóspede, ou a rotina escrita não foi repetida: não opera sozinho. Pausa e volta ao Quadrante antes de abrir.";
  } else if (
    horas === null || horas === "nao_anotei" || rotina === null || rotina === "nao_testada" || rotina === "cabeca" || quem === null || quem === "nao_sei" ||
    // dado que falta para checar o "ajustar" nunca vira "avançar" (ver ts/README.md, regra geral R2)
    val === null || val === "nao_sei" || formal === null || formal === "nao_sei" || (opSozinho && u === null) || (opSozinho && (quer === null || quer === "nao_sei"))
  ) {
    v = "testar";
    const m = [
      (horas === null || horas === "nao_anotei") && "as horas ainda não foram anotadas",
      (rotina === null || rotina === "nao_testada" || rotina === "cabeca") && "a rotina do momento não foi escrita e testada com outra pessoa",
      (quem === null || quem === "nao_sei") && "falta decidir quem opera",
      (val === null || val === "nao_sei") && "falta saber se a conta depende da valorização",
      (formal === null || formal === "nao_sei") && "falta saber se a receita é toda formal",
      opSozinho && u === null && "falta o número de unidades da fase um",
      opSozinho && (quer === null || quer === "nao_sei") && "falta dizer se você quer operar",
    ].filter(Boolean) as string[];
    motivo = `Testar: ${juntar(m)}.`;
  } else if (val === "sim" || adequacao || alertaEscala || formal === "parte") {
    v = "ajustar";
    const m = [val === "sim" && "a conta conta com valorização", adequacao && "o modelo não combina com a vida", alertaEscala && "passa de quatro unidades operando sozinho", formal === "parte" && "deixa receita informal"].filter(Boolean) as string[];
    motivo = `Ajustar: ${juntar(m)}.`;
  } else {
    v = "avancar"; motivo = "Quem opera está decidido, as horas cobrem o horário de hóspede, a rotina escrita foi repetida por outra pessoa e a conta não depende de valorização.";
  }
  calculos.push({ id: "veredito_sugerido", rotulo: "Veredito sugerido pela página", valor: v, texto: motivo });

  return { calculos: calculos.map((c) => fechar(c)), veredito_sugerido: v, motivo_veredito: motivo };
}

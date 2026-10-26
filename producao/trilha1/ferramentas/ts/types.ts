// Zion Exercícios · Trilha 1 · tipos comuns das calculadoras.
// As calculadoras são determinísticas: mesmas respostas, mesmo resultado. Sem IA, sem rede.

/** O que o formulário grava em cada campo. "nao_sei" é o botão "Não sei". */
export type Resposta = number | string | string[] | "nao_sei" | null;

/** Respostas do formulário, pelo `id` de cada campo do JSON da aula. */
export type Respostas = Record<string, Resposta>;

/** Valores auxiliares de um cálculo (extensão opcional, para a tela e para a IA). */
export type ValorDetalhe = number | string | boolean | null | string[];

export type Alerta = "ok" | "atencao" | "critico";

export type Calculo = {
  /** Mesmo `id` do cálculo no JSON da aula. */
  id: string;
  /** O `nome` do cálculo no JSON. */
  rotulo: string;
  /** O número principal (percentuais vêm em pontos: 38,5% = 38.5), texto, sim/não ou null quando falta dado. */
  valor: number | string | boolean | null;
  /** Leitura em português simples, com a régua da fonte. */
  texto: string;
  alerta?: Alerta;
  /** Extensão opcional: os outros números da conta (piso e teto, mês a mês etc.). */
  detalhes?: Record<string, ValorDetalhe>;
};

export type Veredito = "avancar" | "testar" | "ajustar" | "pausar" | "nao_se_aplica";

export type ResultadoCalculos = {
  calculos: Calculo[];
  veredito_sugerido: Veredito;
  motivo_veredito: string;
};

/** Formatação apenas. Nenhum número nasce aqui. */
export function brl(value: number): string {
  return "R$\u00a0" + new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 0 }).format(value);
}

/** Valor já em R$ milhões, com duas casas, vírgula decimal. */
export function mi(value: number): string {
  return new Intl.NumberFormat("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value);
}

export function hectares(value: number): string {
  return new Intl.NumberFormat("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value) + " ha";
}

export function intBR(value: number): string {
  return new Intl.NumberFormat("pt-BR").format(value);
}

/** Troca espaços por espaços não separáveis em valores curtos, como "R$ 75 mi". */
export function nbsp(text: string): string {
  return text.replace(/ /g, "\u00a0");
}

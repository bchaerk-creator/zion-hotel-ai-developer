/** Formatação apenas. Nenhum número nasce aqui. */
export function brl(value: number): string {
  return "R$ " + new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 0 }).format(value);
}

export function hectares(value: number): string {
  return new Intl.NumberFormat("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value) + " ha";
}

export function intBR(value: number): string {
  return new Intl.NumberFormat("pt-BR").format(value);
}

// Funções de apoio das calculadoras: leitura das respostas, contas seguras e formatação pt-BR.
import type { Calculo, Respostas, Resposta, ValorDetalhe } from "./types";

// ---------------------------------------------------------------------------
// Leitura das respostas
// ---------------------------------------------------------------------------

/** "nao_sei", null, undefined, texto vazio e lista vazia contam como resposta que falta. */
export function falta(v: Resposta | undefined): boolean {
  if (v === undefined || v === null) return true;
  if (v === "nao_sei") return true;
  if (typeof v === "string") return v.trim() === "" || v.trim().toLowerCase() === "nao_sei";
  if (Array.isArray(v)) return v.length === 0;
  if (typeof v === "number") return !Number.isFinite(v);
  return false;
}

/** Converte número digitado (aceita "1.234,56", "1234.56", "R$ 600 mil" não; só dígitos e separadores). */
export function paraNumero(v: Resposta | undefined): number | null {
  if (falta(v)) return null;
  if (typeof v === "number") return Number.isFinite(v) ? v : null;
  if (typeof v !== "string") return null;
  let s = v.replace(/R\$|%|\s/g, "");
  if (s === "") return null;
  const temVirgula = s.includes(",");
  if (temVirgula) {
    s = s.replace(/\./g, "").replace(",", ".");
  } else {
    const pontos = (s.match(/\./g) || []).length;
    // "1.500" e "1.500.000" são milhar (pt-BR); "3.5" ou "1234.56" são decimal.
    if (pontos > 1 || /^-?\d{1,3}\.\d{3}$/.test(s)) s = s.replace(/\./g, "");
  }
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

export function num(r: Respostas, id: string): number | null {
  return paraNumero(r[id]);
}

/** Campo percentual: o formulário grava em pontos (78 = 78%). Devolve a fração (0,78). */
export function pct(r: Respostas, id: string): number | null {
  const n = num(r, id);
  return n === null ? null : n / 100;
}

/** Campo de escolha: o `valor` da opção, ou null se falta. "nao_sei" volta como "nao_sei". */
export function escolha(r: Respostas, id: string): string | null {
  const v = r[id];
  if (v === "nao_sei") return "nao_sei";
  if (typeof v === "number") return String(v);
  if (typeof v !== "string") return null;
  const t = v.trim();
  return t === "" ? null : t;
}

/** Campo múltiplo: lista sem repetição, só com valores permitidos (se a lista for dada). */
export function lista(r: Respostas, id: string, permitidos?: readonly string[]): string[] {
  const v = r[id];
  let arr: string[] = [];
  if (Array.isArray(v)) arr = v.map((x) => String(x).trim());
  else if (typeof v === "string" && v !== "nao_sei" && v.trim() !== "") arr = v.split(/[,;\n]/).map((x) => x.trim());
  else if (typeof v === "number") arr = [String(v)];
  arr = arr.filter((x) => x !== "" && x !== "nao_sei");
  if (permitidos) arr = arr.filter((x) => permitidos.includes(x));
  return Array.from(new Set(arr));
}

export function texto(r: Respostas, id: string): string | null {
  const v = r[id];
  if (falta(v)) return null;
  if (Array.isArray(v)) return v.join("\n");
  return String(v).trim();
}

// ---------------------------------------------------------------------------
// Contas seguras (nunca NaN, nunca divisão por zero)
// ---------------------------------------------------------------------------

export function ok(...xs: (number | null | undefined)[]): boolean {
  return xs.every((x) => typeof x === "number" && Number.isFinite(x));
}

export function div(a: number | null | undefined, b: number | null | undefined): number | null {
  if (!ok(a, b) || b === 0) return null;
  const q = (a as number) / (b as number);
  return Number.isFinite(q) ? q : null;
}

export function soma(...xs: (number | null | undefined)[]): number | null {
  return ok(...xs) ? (xs as number[]).reduce((s, x) => s + x, 0) : null;
}

export function mult(...xs: (number | null | undefined)[]): number | null {
  return ok(...xs) ? (xs as number[]).reduce((s, x) => s * x, 1) : null;
}

export function sub(a: number | null | undefined, b: number | null | undefined): number | null {
  return ok(a, b) ? (a as number) - (b as number) : null;
}

/** Arredondamento comercial (meio para longe do zero), estável para 2 casas. */
export function arred(x: number, casas = 2): number {
  const f = Math.pow(10, casas);
  const y = Math.abs(x) * f;
  const r = Math.round(y + 1e-7) / f;
  const res = x < 0 ? -r : r;
  return Object.is(res, -0) ? 0 : res;
}

/** Arredonda para cima até o múltiplo dado (ex.: R$ 500). */
export function tetoMultiplo(x: number, m: number): number {
  return Math.ceil(x / m - 1e-9) * m;
}

/** Arredonda para baixo, com tolerância de ponto flutuante. */
export function pisoSeguro(x: number): number {
  return Math.floor(x + 1e-9);
}

// ---------------------------------------------------------------------------
// Formatação pt-BR (sem travessão)
// ---------------------------------------------------------------------------

function agrupar(inteiro: string): string {
  return inteiro.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

/** 1234.5 → "1.234,50" (casas fixas). */
export function fmtNum(x: number, casas = 2): string {
  const r = arred(x, casas);
  const neg = r < 0;
  const [i, d] = Math.abs(r).toFixed(casas).split(".");
  return (neg ? "-" : "") + agrupar(i) + (casas > 0 ? "," + d : "");
}

/** Número com casas variáveis: tira zeros finais ("415,8", "3", "2,4"). */
export function fmtN(x: number, casasMax = 2): string {
  const s = fmtNum(x, casasMax);
  if (!s.includes(",")) return s;
  return s.replace(/,?0+$/, "");
}

/** 60943.02 → "R$ 60.943,02"; negativo → "-R$ 60.943,02". */
export function brl(x: number): string {
  const r = arred(x, 2);
  return (r < 0 ? "-" : "") + "R$ " + fmtNum(Math.abs(r), 2);
}

/** Fração → percentual: 0.385 → "38,5%". */
export function fmtPct(frac: number, casas = 1): string {
  return fmtNum(frac * 100, casas) + "%";
}

/** Data UTC → "03/03/2027". */
export function fmtData(d: Date): string {
  const dd = String(d.getUTCDate()).padStart(2, "0");
  const mm = String(d.getUTCMonth() + 1).padStart(2, "0");
  return `${dd}/${mm}/${d.getUTCFullYear()}`;
}

/** Aceita "2027-06-01", "01/06/2027" ou Date em texto ISO. Devolve data UTC à meia-noite. */
export function data(r: Respostas, id: string): Date | null {
  const v = r[id];
  if (falta(v) || typeof v !== "string") return null;
  const s = v.trim();
  let y: number, m: number, d: number;
  let mt = s.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (mt) {
    y = +mt[1]; m = +mt[2]; d = +mt[3];
  } else {
    mt = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
    if (!mt) return null;
    d = +mt[1]; m = +mt[2]; y = +mt[3];
  }
  const dt = new Date(Date.UTC(y, m - 1, d));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== m - 1 || dt.getUTCDate() !== d) return null;
  return dt;
}

export function somaDias(d: Date, dias: number): Date {
  return new Date(d.getTime() + dias * 86400000);
}

export function difDias(a: Date, b: Date): number {
  return Math.round((a.getTime() - b.getTime()) / 86400000);
}

/** Junta itens: "a", "a e b", "a, b e c". */
export function juntar(itens: string[]): string {
  if (itens.length === 0) return "";
  if (itens.length === 1) return itens[0];
  return itens.slice(0, -1).join(", ") + " e " + itens[itens.length - 1];
}

// ---------------------------------------------------------------------------
// Fechamento: arredonda os números de saída e garante que não sobra NaN nem travessão
// ---------------------------------------------------------------------------

function limpaNumero(x: number, casas: number): number | null {
  return Number.isFinite(x) ? arred(x, casas) : null;
}

function limpaTexto(s: string): string {
  // Nenhum travessão nos textos (em dash e en dash viram vírgula ou hífen simples).
  return s.replace(/\s*\u2014\s*/g, ", ").replace(/\u2013/g, "-");
}

function limpaDetalhe(v: ValorDetalhe, casas: number): ValorDetalhe {
  if (typeof v === "number") return limpaNumero(v, casas);
  if (typeof v === "string") return limpaTexto(v);
  if (Array.isArray(v)) return v.map(limpaTexto);
  return v;
}

/** Arredonda valores (dinheiro e percentuais em 2 casas, demais em 4) e troca NaN/Infinity por null. */
export function fechar(c: Calculo, casas = 2): Calculo {
  const out: Calculo = {
    id: c.id,
    rotulo: limpaTexto(c.rotulo),
    valor: typeof c.valor === "number" ? limpaNumero(c.valor, casas) : typeof c.valor === "string" ? limpaTexto(c.valor) : c.valor,
    texto: limpaTexto(c.texto),
  };
  if (c.alerta) out.alerta = c.alerta;
  if (c.detalhes) {
    out.detalhes = {};
    for (const [k, v] of Object.entries(c.detalhes)) out.detalhes[k] = limpaDetalhe(v, 4);
  }
  return out;
}

/** Fração em pontos percentuais para o `valor` (0.385 → 38.5). */
export function pontos(frac: number | null): number | null {
  return frac === null ? null : frac * 100;
}

export const MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"] as const;
export const MESES_NOME = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];

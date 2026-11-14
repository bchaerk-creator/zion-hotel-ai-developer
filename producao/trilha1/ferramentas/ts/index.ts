// Zion Exercícios · Trilha 1 · as 12 calculadoras, pela chave do link curto ("1-1" a "1-12").
import type { ResultadoCalculos, Respostas } from "./types";
import { calcular as a01 } from "./t1-a01";
import { calcular as a02 } from "./t1-a02";
import { calcular as a03 } from "./t1-a03";
import { calcular as a04 } from "./t1-a04";
import { calcular as a05 } from "./t1-a05";
import { calcular as a06 } from "./t1-a06";
import { calcular as a07 } from "./t1-a07";
import { calcular as a08 } from "./t1-a08";
import { calcular as a09 } from "./t1-a09";
import { calcular as a10 } from "./t1-a10";
import { calcular as a12 } from "./t1-a12";

export * from "./types";

export const calculadoras: Record<string, (r: Respostas) => ResultadoCalculos> = {
  "1-1": a01,
  "1-2": a02,
  "1-3": a03,
  "1-4": a04,
  "1-5": a05,
  "1-6": a06,
  "1-7": a07,
  "1-8": a08,
  "1-9": a09,
  "1-10": a10,
  "1-12": a12,
};

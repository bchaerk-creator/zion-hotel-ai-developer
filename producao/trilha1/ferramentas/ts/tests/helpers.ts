// Apoio dos testes: checagens comuns a todas as aulas.
import assert from "node:assert/strict";
import type { Calculo, ResultadoCalculos } from "../types";

/** Nenhum NaN/Infinity, nenhum travessão, todo cálculo com texto, veredito válido. */
export function saneamento(res: ResultadoCalculos, idsEsperados: string[]): void {
  assert.deepEqual(res.calculos.map((c) => c.id), idsEsperados, "ids e ordem dos cálculos iguais ao JSON");
  const json = JSON.stringify(res);
  assert.ok(!/NaN|Infinity/.test(json), "sem NaN nem Infinity no resultado");
  assert.ok(!/[\u2013\u2014]/.test(json), "sem travessão (en dash ou em dash) nos textos");
  for (const c of res.calculos) {
    assert.ok(typeof c.texto === "string" && c.texto.length > 10, `texto preenchido em ${c.id}`);
    if (typeof c.valor === "number") assert.ok(Number.isFinite(c.valor), `valor finito em ${c.id}`);
    for (const v of Object.values(c.detalhes ?? {})) if (typeof v === "number") assert.ok(Number.isFinite(v), `detalhe finito em ${c.id}`);
  }
  assert.ok(["avancar", "testar", "ajustar", "pausar", "nao_se_aplica"].includes(res.veredito_sugerido));
  assert.ok(res.motivo_veredito.length > 10);
}

export function calc(res: ResultadoCalculos, id: string): Calculo {
  const c = res.calculos.find((x) => x.id === id);
  assert.ok(c, `cálculo ${id} existe`);
  return c as Calculo;
}

export function det(res: ResultadoCalculos, id: string, chave: string): unknown {
  return calc(res, id).detalhes?.[chave];
}

/** Compara com tolerância (padrão: meio centavo / meio centésimo de ponto). */
export function perto(real: unknown, esperado: number, tol = 0.006, msg = ""): void {
  assert.equal(typeof real, "number", `${msg} deveria ser número, veio ${JSON.stringify(real)}`);
  assert.ok(Math.abs((real as number) - esperado) <= tol, `${msg} esperado ${esperado}, veio ${real}`);
}

/** Lê os ids dos cálculos direto do JSON da aula (a fonte da ordem). */
export async function idsDoJson(n: string): Promise<string[]> {
  const fs = await import("node:fs");
  const path = await import("node:path");
  const url = await import("node:url");
  const aqui = path.dirname(url.fileURLToPath(import.meta.url));
  const j = JSON.parse(fs.readFileSync(path.join(aqui, "..", "..", `aula-${n}.json`), "utf8"));
  return j.calculos.map((c: { id: string }) => c.id);
}

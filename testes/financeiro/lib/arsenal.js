// Carregador SOMENTE LEITURA das mini mentorias (B06, B08, A09) do Zion Arsenal.
// Executa o compute() de producao/zion-arsenal/app/products/<ID>.js num contexto isolado,
// com um stub mínimo do objeto ZA do motor (sem navegador, sem alterar arquivos).
"use strict";
const fs = require("fs"), vm = require("vm"), path = require("path");

const RAIZ = path.resolve(__dirname, "..", "..", "..");
const APP = path.join(RAIZ, "producao", "zion-arsenal", "app");

function carregarProduto(id) {
  const arq = path.join(APP, "products", id + ".js");
  if (!fs.existsSync(arq)) return null;
  const ZA = {};
  const isNum = (x) => typeof x === "number" && isFinite(x);
  const sum = (a) => { let t = 0; (a || []).forEach((x) => { if (isNum(x)) t += x; }); return t; };
  Object.assign(ZA, {
    isNum, sum, listSum: (r) => sum((r || []).map((x) => (x && isNum(x.value) ? x.value : 0))),
    clamp: (v, a, b) => Math.max(a, Math.min(b, v)), esc: (s) => String(s),
    fmt: { brl: String, brl0: String, pct: String, num: String, meses: String },
    table: () => "", op3d: () => ({ l1: [] }), register: (c) => { ZA.cfg = c; },
  });
  const sb = { window: { ZA }, ZA, console };
  vm.createContext(sb);
  vm.runInContext(fs.readFileSync(arq, "utf8"), sb);
  return { cfg: ZA.cfg, fonte: fs.readFileSync(arq, "utf8"), arquivo: arq };
}

function contexto(v, u = {}) {
  const isNum = (x) => typeof x === "number" && isFinite(x);
  return {
    v, u, checks: {}, notes: {},
    has: (id) => { const x = v[id]; if (u[id]) return false; if (Array.isArray(x)) return x.length > 0; return x !== undefined && x !== null && x !== ""; },
    n: (id, d) => { const x = v[id]; return !u[id] && isNum(x) ? x : d === undefined ? null : d; },
    t: (id, d) => { const x = v[id]; return !u[id] && x != null && x !== "" ? x : d || ""; },
    unknown: (id) => !!u[id], checked: () => false,
  };
}

function rodar(id, valores, desconhecidos) {
  const p = carregarProduto(id);
  if (!p) return null;
  return p.cfg.compute(contexto(valores, desconhecidos));
}

const pegar = (obj, caminho) => caminho.split(".").reduce((a, k) => (a == null ? a : a[k]), obj);

module.exports = { carregarProduto, rodar, pegar, APP, RAIZ };

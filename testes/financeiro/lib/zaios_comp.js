// Carregador SOMENTE LEITURA da camada de composição da ZAIOS (src/exercicios, src/calc/operacao.ts...).
// Aponte ZAIOS_SRC_DIR para uma cópia local da raiz do projeto (contendo src/). O código não fica no repositório.
// A cópia vai para uma pasta temporária; só os especificadores de import são ajustados para o Node
// ("@/x" → caminho relativo; ".ts" acrescentado). O conteúdo das fórmulas não é alterado.
"use strict";
const fs = require("fs"), os = require("os"), path = require("path");
const { pathToFileURL } = require("url");

function copiarArvore(origem, destino) {
  for (const e of fs.readdirSync(origem, { withFileTypes: true })) {
    const o = path.join(origem, e.name), d = path.join(destino, e.name);
    if (e.isDirectory()) { fs.mkdirSync(d, { recursive: true }); copiarArvore(o, d); }
    else if (e.name.endsWith(".ts")) fs.writeFileSync(d, fs.readFileSync(o, "utf8"));
  }
}
function resolver(arquivo, spec, raizSrc) {
  let alvo;
  if (spec.startsWith("@/")) alvo = path.join(raizSrc, spec.slice(2));
  else if (spec.startsWith(".")) alvo = path.resolve(path.dirname(arquivo), spec);
  else return spec;
  if (fs.existsSync(alvo + ".ts")) alvo += ".ts";
  else if (fs.existsSync(path.join(alvo, "index.ts"))) alvo = path.join(alvo, "index.ts");
  let rel = path.relative(path.dirname(arquivo), alvo).split(path.sep).join("/");
  if (!rel.startsWith(".")) rel = "./" + rel;
  return rel;
}
function ajustar(dir, raizSrc) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) { ajustar(p, raizSrc); continue; }
    if (!p.endsWith(".ts")) continue;
    const src = fs.readFileSync(p, "utf8").replace(/(from\s+|import\s*\()(["'])([^"']+)\2/g, (m, pre, q, spec) => pre + q + resolver(p, spec, raizSrc) + q);
    fs.writeFileSync(p, src);
  }
}
async function carregarComposicao(modulos) {
  const dir = process.env.ZAIOS_SRC_DIR;
  if (!dir || !fs.existsSync(path.join(dir, "src"))) return { ok: false, motivo: "Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS)." };
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "zaios-comp-"));
  fs.mkdirSync(path.join(tmp, "src"), { recursive: true });
  copiarArvore(path.join(dir, "src"), path.join(tmp, "src"));
  fs.writeFileSync(path.join(tmp, "package.json"), '{"type":"module"}');
  ajustar(path.join(tmp, "src"), path.join(tmp, "src"));
  const out = { ok: true, fontes: {} };
  try {
    for (const m of modulos) {
      out[m] = await import(pathToFileURL(path.join(tmp, "src", m + ".ts")).href);
      out.fontes[m] = fs.readFileSync(path.join(dir, "src", m + ".ts"), "utf8");
    }
    return out;
  } catch (e) { return { ok: false, motivo: "Falha ao carregar a composição da ZAIOS: " + e.message.split("\n")[0] }; }
}
module.exports = { carregarComposicao };

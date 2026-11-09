// Carregador SOMENTE LEITURA do motor de cálculo da ZAIOS.
// O código da ZAIOS não fica neste repositório (que é público). Para executar os casos
// da ZAIOS, aponte ZAIOS_CALC_DIR para uma cópia local de src/calc com os arquivos
// tipos.ts, capex.ts, receitas.ts e viabilidade.ts (exportada do projeto Lovable sem gastar créditos:
// leitura de arquivos pelo editor/MCP do Lovable ou pelo repositório GitHub sincronizado).
// A cópia é feita para uma pasta temporária, onde só os caminhos de import recebem ".ts"
// (exigência do Node para TypeScript); o conteúdo das fórmulas não é tocado.
"use strict";
const fs = require("fs"), os = require("os"), path = require("path");
const { pathToFileURL } = require("url");

const ARQUIVOS = ["tipos.ts", "capex.ts", "receitas.ts", "viabilidade.ts"];

async function carregarZaios() {
  const dir = process.env.ZAIOS_CALC_DIR;
  if (!dir) return { ok: false, motivo: "Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS)." };
  const faltando = ARQUIVOS.filter((a) => !fs.existsSync(path.join(dir, a)));
  if (faltando.length) return { ok: false, motivo: "Faltam em ZAIOS_CALC_DIR: " + faltando.join(", ") };
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "zaios-calc-"));
  for (const a of ARQUIVOS) {
    const src = fs.readFileSync(path.join(dir, a), "utf8").replace(/from "\.\/([a-z]+)"/g, 'from "./$1.ts"');
    fs.writeFileSync(path.join(tmp, a), src);
  }
  fs.writeFileSync(path.join(tmp, "package.json"), '{"type":"module"}');
  try {
    const imp = (a) => import(pathToFileURL(path.join(tmp, a)).href);
    const [tipos, capex, receitas, viabilidade] = await Promise.all(ARQUIVOS.map(imp));
    const fontes = Object.fromEntries(ARQUIVOS.map((a) => [a.replace(".ts", ""), fs.readFileSync(path.join(dir, a), "utf8")]));
    return { ok: true, tipos, capex, receitas, viabilidade, origem: dir, fontes };
  } catch (e) {
    return { ok: false, motivo: "Falha ao carregar a ZAIOS (Node 22.6+ com suporte a TypeScript é necessário): " + e.message };
  }
}

module.exports = { carregarZaios, ARQUIVOS };

// Carregador SOMENTE LEITURA da Folha Única do Mês (Jornada 2 · Módulo 2).
"use strict";
const fs = require("fs"), path = require("path");
const RAIZ = path.resolve(__dirname, "..", "..", "..");
const ARQ = path.join(RAIZ, "producao", "jornada2", "02-financas", "src", "logic.js");
function carregarFolha() {
  if (!fs.existsSync(ARQ)) return null;
  const api = require(ARQ);
  return { api, fonte: fs.readFileSync(ARQ, "utf8"), arquivo: ARQ };
}
module.exports = { carregarFolha };

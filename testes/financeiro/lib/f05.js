// Executa a recalculação da Ferramenta 05 (precisa de python3 + openpyxl + LibreOffice/soffice).
"use strict";
const { spawnSync } = require("child_process"), fs = require("fs"), path = require("path");
const RAIZ = path.resolve(__dirname, "..", "..", "..");
const XLSX = path.join(RAIZ, "docs", "p", "adbc67069af26ae0", "orcamento-05", "Orcamento-Cabana-Zion-EXEMPLO.xlsx");
let cache;
function resumoF05() {
  if (cache !== undefined) return cache;
  if (!fs.existsSync(XLSX)) return (cache = { ok: false, motivo: "Planilha EXEMPLO da Ferramenta 05 não encontrada." });
  const soffice = spawnSync("soffice", ["--version"], { encoding: "utf8" });
  if (soffice.error) return (cache = { ok: false, motivo: "LibreOffice (soffice) não instalado." });
  const r = spawnSync("python3", ["-I", path.join(__dirname, "f05_recalc.py"), XLSX], { encoding: "utf8", timeout: 240000 });
  if (r.status !== 0) return (cache = { ok: false, motivo: "Falha na recalculação: " + (r.stderr || "").slice(0, 300) });
  return (cache = { ok: true, valores: JSON.parse(r.stdout.trim().split("\n").pop()) });
}
module.exports = { resumoF05, XLSX };

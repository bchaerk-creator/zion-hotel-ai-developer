// Valida os arquivos de /data contra as regras de docs/MASTER.md.
// Uso: node scripts/validate-data.mjs
import { readFileSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const dataDir = join(root, "data");
const errors = [];
const files = readdirSync(dataDir).filter((f) => f.endsWith(".json"));
const data = {};
for (const f of files) {
  try {
    data[f] = JSON.parse(readFileSync(join(dataDir, f), "utf8"));
  } catch (e) {
    errors.push(`${f}: JSON inválido (${e.message})`);
  }
}

const expected = ["company","operations","revenue","brand","model","capex","program","raise","returns","platform","landBank","market","documents","sources","legal"];
for (const name of expected) if (!data[`${name}.json`]) errors.push(`falta data/${name}.json`);

const sourceIds = new Set((data["sources.json"]?.sources ?? []).map((s) => s.id));
const statuses = new Set(["validated", "estimate", "pending"]);

function walk(file, node, path = "") {
  if (Array.isArray(node)) return node.forEach((n, i) => walk(file, n, `${path}[${i}]`));
  if (node && typeof node === "object") {
    if ("sourceId" in node && !sourceIds.has(node.sourceId)) errors.push(`${file}${path}: sourceId desconhecido "${node.sourceId}"`);
    if ("status" in node && typeof node.status === "string" && "sourceId" in node && !statuses.has(node.status)) errors.push(`${file}${path}: status inválido "${node.status}"`);
    const isMetric = "value" in node && "label" in node && "sourceId" in node;
    if (isMetric) for (const k of ["period", "status"]) if (!(k in node)) errors.push(`${file}${path}: métrica sem ${k}`);
    for (const [k, v] of Object.entries(node)) walk(file, v, `${path}.${k}`);
  }
}
for (const [file, node] of Object.entries(data)) walk(file, node);

// Palavras proibidas e número errado em qualquer texto de /data.
// Os campos que listam os termos para proibi-los ficam fora da varredura.
const allowListKeys = new Set(["neverSay", "rules", "forbidden", "forbiddenWord", "doNotUse"]);
function stripAllowed(node) {
  if (Array.isArray(node)) return node.map(stripAllowed);
  if (node && typeof node === "object") {
    const out = {};
    for (const [k, v] of Object.entries(node)) if (!allowListKeys.has(k)) out[k] = stripAllowed(v);
    return out;
  }
  return node;
}
const forbidden = [/\bpayback\b/i, /rede de hot[ée]is/i, /hectares da zion/i, /11,2 mi/];
for (const [f, node] of Object.entries(data)) {
  const text = JSON.stringify(stripAllowed(node));
  for (const re of forbidden) {
    const m = text.match(re);
    if (m) errors.push(`${f}: termo proibido "${m[0]}"`);
  }
  if (/\u2014/.test(text)) errors.push(`${f}: travessão longo encontrado`);
}

// Retorno só em arquivos investorOnly.
const returnKeys = ["yieldOnCapital", "multiple7y", "capitalReturnCycle", "irr"];
for (const [file, node] of Object.entries(data)) {
  const text = JSON.stringify(node);
  const hasReturn = returnKeys.some((k) => text.includes(`"${k}"`));
  if (hasReturn && node.investorOnly !== true) errors.push(`${file}: contém dado de retorno sem investorOnly: true`);
}

// Consistência aritmética do CAPEX.
const c = data["capex.json"];
if (c) {
  const sum = c.blocks.reduce((a, b) => a + b.total, 0);
  if (sum !== c.implementationSubtotal) errors.push(`capex.json: soma dos blocos ${sum} difere do subtotal ${c.implementationSubtotal}`);
  const total = c.implementationSubtotal + c.contingency.value + c.workingCapital.value;
  if (total !== c.implementationTotal.value) errors.push(`capex.json: total de implantação ${total} difere de ${c.implementationTotal.value}`);
  const allIn = c.implementationTotal.value + c.fees.value + c.siteWorks.value;
  if (allIn !== c.allIn.value) errors.push(`capex.json: all-in ${allIn} difere de ${c.allIn.value}`);
}

// Consistência do faturamento acumulado.
const r = data["revenue.json"];
if (r) {
  const sum = r.periods.reduce((a, p) => a + p.valueNumber, 0);
  if (Math.abs(sum - 9880000) > 10000) errors.push(`revenue.json: soma dos períodos ${sum} difere de 9,88 mi`);
  if (r.total.value !== "R$ 9,88 mi") errors.push("revenue.json: total deve ser R$ 9,88 mi");
}

// Programa: 23 destinos.
const p = data["program.json"];
if (p) {
  const n = p.waves.reduce((a, w) => a + w.destinations.length, 0);
  if (n !== 23) errors.push(`program.json: ${n} destinos, esperado 23`);
  const corr = p.corridors.reduce((a, x) => a + x.count, 0);
  if (corr !== 22) errors.push(`program.json: corredores somam ${corr}, esperado 22 (23 menos o destino em definição)`);
}

// Land bank: camadas somam o total.
const lb = data["landBank.json"];
if (lb) {
  const layers = lb.layers.reduce((a, l) => a + (l.hectares ?? 0), 0);
  if (Math.abs(layers - 6521.09) > 0.01) errors.push(`landBank.json: camadas somam ${layers.toFixed(2)}, esperado 6521,09`);
  const regions = lb.regions.reduce((a, x) => a + x.hectares, 0);
  if (Math.abs(regions - 6521.09) > 0.01) errors.push(`landBank.json: regiões somam ${regions.toFixed(2)}, esperado 6521,09`);
  for (const cap of lb.module.capacity) if (cap.modules * lb.module.suites !== cap.suites) errors.push(`landBank.json: capacidade ${cap.modules} módulos deveria dar ${cap.modules * lb.module.suites} suítes`);
}

// Cluster de VPs.
const pl = data["platform.json"];
if (pl) {
  const total = pl.organization.cluster.reduce((a, v) => a + v.annualCost, 0);
  if (total !== pl.organization.matureTotal) errors.push(`platform.json: cluster soma ${total}, esperado ${pl.organization.matureTotal}`);
  for (const v of pl.organization.cluster) {
    const s = v.allocation.collection + v.allocation.store + v.allocation.management;
    if (s !== 100) errors.push(`platform.json: alocação de ${v.label} soma ${s}%`);
  }
}

if (errors.length) {
  console.error(`✗ ${errors.length} problema(s):`);
  for (const e of errors) console.error("  " + e);
  process.exit(1);
}
console.log(`✓ ${files.length} arquivos de /data válidos, ${sourceIds.size} fontes registradas.`);

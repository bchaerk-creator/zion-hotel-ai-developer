#!/usr/bin/env node
// Suíte de homologação financeira Zion (Comando 05C) · T1 a T12.
// Uso: node testes/financeiro/run.js [--saida <pasta>]   (ZAIOS: defina ZAIOS_CALC_DIR)
// Somente leitura: nenhum arquivo de produção é alterado. Não consome créditos Lovable.
"use strict";
const fs = require("fs"), path = require("path");
const { TIPO, STATUS, iguais, fmt } = require("./lib/base");
const E = require("./esperados");
const { carregarZaios } = require("./lib/zaios");
const arsenal = require("./lib/arsenal");
const { carregarFolha } = require("./lib/folha_j2");
const { resumoF05 } = require("./lib/f05");

const ARQS = ["t01_zbase", "t02_zcompleto", "t03_referencia", "t04_orcamento", "t05_mes_real", "t06_limites", "t07_regua", "t08_omissoes", "t09_reserva_quebra", "t10_prolabore", "t11_saida", "t12_parametros"];

function classificar(caso, obtido) {
  const passou = iguais(obtido, caso.esperado, caso.tol);
  if (caso.tipo === TIPO.FORMULA) return passou ? STATUS.OK : STATUS.FALHOU;
  if (caso.tipo === TIPO.DIVERGENCIA) return passou ? STATUS.DIV_NAO_REPRODUZIDA : STATUS.DIV_CONFIRMADA;
  if (caso.tipo === TIPO.LIMITACAO) return passou ? STATUS.LIM_NAO_REPRODUZIDA : STATUS.LIM_CONFIRMADA;
  return STATUS.PENDENTE;
}

async function main() {
  const iSaida = process.argv.indexOf("--saida");
  const saida = iSaida > 0 ? process.argv[iSaida + 1] : path.join(__dirname, "resultados", "ultima");
  const z = await carregarZaios();
  const folha = carregarFolha();
  const deps = {
    zaios: z.ok ? z : null, zaiosFontes: z.ok ? z.fontes : {},
    arsenal: fs.existsSync(arsenal.APP) ? arsenal : null,
    folha, f05: resumoF05,
  };
  const disponivel = {
    zaios: !!deps.zaios, arsenal: !!deps.arsenal, folha: !!folha,
    "folha+zaios": !!folha && !!deps.zaios, f05: (() => { const r = resumoF05(); return r.ok; })(),
  };
  const motivo = { zaios: z.ok ? "" : z.motivo, arsenal: "Pasta do Zion Arsenal ausente.", folha: "Folha Única J2 ausente.", "folha+zaios": "Precisa da Folha J2 e da ZAIOS.", f05: resumoF05().ok ? "" : resumoF05().motivo };

  const linhas = [];
  for (const a of ARQS) {
    for (const caso of require("./casos/" + a)(deps)) {
      const r = Object.assign({}, caso);
      delete r.obter;
      if (caso.requer && !disponivel[caso.requer]) { r.status = STATUS.NAO_EXECUTADO; r.obtido = null; r.motivo = motivo[caso.requer]; linhas.push(r); continue; }
      try {
        r.obtido = caso.obter();
        r.status = classificar(caso, r.obtido);
      } catch (e) { r.status = STATUS.ERRO; r.obtido = null; r.motivo = e.message; }
      linhas.push(r);
    }
  }

  const cont = {};
  for (const l of linhas) cont[l.status] = (cont[l.status] || 0) + 1;
  const agora = new Date().toISOString();
  fs.mkdirSync(saida, { recursive: true });
  fs.writeFileSync(path.join(saida, "resultado.json"), JSON.stringify({ geradoEm: agora, plano: E.PLANO, dicionario: E.DICIONARIO, dependencias: disponivel, zaiosOrigem: z.ok ? "cópia local em ZAIOS_CALC_DIR" : null, contagem: cont, casos: linhas }, null, 2));

  const md = [];
  md.push("# Resultado da suíte de homologação financeira (T1 a T12)", "");
  md.push(`Gerado em ${agora} · Plano: ${E.PLANO} · Dicionário: ${E.DICIONARIO}`, "");
  md.push("**Nada foi homologado por esta execução.** OK significa só que a fórmula reproduz o valor esperado do plano.", "");
  md.push("## Dependências", "", "| Dependência | Disponível | Observação |", "|---|---|---|");
  for (const k of Object.keys(disponivel)) md.push(`| ${k} | ${disponivel[k] ? "sim" : "não"} | ${disponivel[k] ? "" : motivo[k]} |`);
  md.push("", "## Contagem", "", "| Status | Casos |", "|---|---|");
  for (const [k, v] of Object.entries(cont)) md.push(`| ${k} | ${v} |`);
  md.push("", "## Casos", "", "| ID | Teste | Ferramenta | Indicador | Decisão | Tipo | Esperado | Obtido | Status | Nota |", "|---|---|---|---|---|---|---|---|---|---|");
  for (const l of linhas) {
    const obt = l.tipo === TIPO.ECONOMICO ? Object.entries(l.obtido || {}).filter(([, v]) => v !== undefined && v !== null && v !== false).map(([k, v]) => `${k}: ${fmt(v)}`).join("; ") || "—" : fmt(l.obtido);
    const esp = fmt(l.esperado) + (l.faixa ? ` (faixa ${fmt(l.faixa)})` : "");
    md.push(`| ${l.id} | ${l.teste} | ${l.ferramenta} | ${l.indicador} | ${l.decisao} | ${l.tipo} | ${esp} | ${obt} | ${l.status} | ${(l.nota || l.motivo || "").replace(/\|/g, "/")} |`);
  }
  fs.writeFileSync(path.join(saida, "RESULTADO.md"), md.join("\n") + "\n");

  console.log(`Suíte financeira: ${linhas.length} casos`);
  for (const [k, v] of Object.entries(cont)) console.log(`  ${k}: ${v}`);
  for (const l of linhas.filter((x) => [STATUS.FALHOU, STATUS.ERRO, STATUS.DIV_NAO_REPRODUZIDA, STATUS.LIM_NAO_REPRODUZIDA].includes(x.status)))
    console.log(`  ! ${l.id} ${l.status}: esperado ${fmt(l.esperado)}, obtido ${fmt(l.obtido)} ${l.motivo || ""}`);
  console.log(`Relatório: ${path.join(saida, "RESULTADO.md")}`);
  // Código de saída: 1 se alguma fórmula falhou ou deu erro. Divergências confirmadas não reprovam a execução.
  process.exitCode = linhas.some((x) => x.status === STATUS.FALHOU || x.status === STATUS.ERRO) ? 1 : 0;
}
main();

// T4 · Orçamento: B06, F05 e ZAIOS P5. Escopos diferentes: testa-se a regra, não o mesmo total.
"use strict";
const fs = require("fs"), path = require("path");
const E = require("../esperados"), { TOL, TIPO } = require("../lib/base");
module.exports = (D) => {
  const c = [];
  const add = (o) => c.push(Object.assign({ teste: "T4" }, o));
  const perfil = () => {
    const arq = path.join(D.arsenal.APP, "..", "tests", "profiles", "B06.json");
    const p = JSON.parse(fs.readFileSync(arq, "utf8")).profiles.find((x) => x.name === "iniciante");
    const u = {}; (p.unknown || []).forEach((k) => (u[k] = true));
    return { v: p.values, r: D.arsenal.rodar("B06", p.values, u) };
  };
  add({ id: "T4-B06-01", ferramenta: "B06", indicador: "CAPEX (perfil oficial iniciante)", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T4.B06iniciante.capex, tol: TOL.reais, requer: "arsenal", obter: () => perfil().r.capex });
  add({ id: "T4-B06-02", ferramenta: "B06", indicador: "Cenário intermediário (perfil iniciante)", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T4.B06iniciante.inter, tol: TOL.reais, requer: "arsenal", obter: () => perfil().r.inter });
  add({ id: "T4-B06-03", ferramenta: "B06", indicador: "Cenário conservador (perfil iniciante)", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T4.B06iniciante.cons, tol: TOL.reais, requer: "arsenal", obter: () => perfil().r.cons });
  add({ id: "T4-B06-04", ferramenta: "B06", indicador: "Contingência fora do capital de giro (intermediário − giro = CAPEX × (1 + contingência))", decisao: "v0", tipo: TIPO.FORMULA, esperado: 0, tol: TOL.reais, requer: "arsenal",
    obter: () => { const { v, r } = perfil(); return (r.inter - r.giro) - r.capex * (1 + (v.contingencia || 0) / 100); } });
  // Mesmas linhas do F01 lançadas no B06, contingência de 25%: compara a BASE da contingência com a da ZAIOS.
  add({ id: "T4-B06-05", ferramenta: "B06", indicador: "Contingência sobre as linhas do F01 (base ZAIOS: infra + obra + apoio = 182.500)", decisao: "D6 (pendente)", tipo: TIPO.LIMITACAO, esperado: 182500, tol: TOL.reais, requer: "arsenal",
    nota: "O B06 aplica a contingência sobre todo o CAPEX (inclui projeto e equipamentos).",
    obter: () => D.arsenal.rodar("B06", { unidades: 3, hospedes_unid: 2, custo_unid: 130000, frete_unid: 0, projetos: [{ name: "Projeto e licenças", value: 70000 }], infra: [{ name: "Infraestrutura", value: 250000 }], comuns: [{ name: "Apoio e áreas comuns", value: 90000 }], mob_unid: 65000, equip_gerais: 23400, pre_op: 36500, cf_mensal: 0, meses_giro: 0, contingencia: 25, variacao: 0, prazo_obra: 10, area_unid: 30 }, {}).contValor });
  // F05
  const f = () => { const r = D.f05(); if (!r.ok) throw new Error(r.motivo); return r.valores; };
  add({ id: "T4-F05-01", ferramenta: "F05", indicador: "Subtotal do exemplo", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T4.F05exemplo.subtotal, tol: TOL.reais, requer: "f05", obter: () => f().subtotal });
  add({ id: "T4-F05-02", ferramenta: "F05", indicador: "Reserva para imprevistos (contingência) do exemplo", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T4.F05exemplo.reserva, tol: TOL.reais, requer: "f05", obter: () => f().reserva });
  add({ id: "T4-F05-03", ferramenta: "F05", indicador: "Total com reserva do exemplo", decisao: "v0", tipo: TIPO.FORMULA, esperado: E.T4.F05exemplo.total, tol: TOL.reais, requer: "f05", obter: () => f().total });
  return c;
};

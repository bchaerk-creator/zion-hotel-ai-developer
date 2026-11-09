// T8 · Indicadores omitidos nas ferramentas simplificadas: precisam aparecer com o rótulo do dicionário.
"use strict";
const { TIPO } = require("../lib/base"), U = require("./_util");
module.exports = (D) => {
  const c = [];
  const add = (o) => c.push(Object.assign({ teste: "T8", requer: "arsenal", tipo: TIPO.DIVERGENCIA, esperado: true }, o));
  const f = (id) => D.arsenal.carregarProduto(id).fonte;
  const campos = (id) => U.camposDe(f(id));
  for (const id of ["B08", "A09"]) {
    add({ id: `T8-${id}-01`, ferramenta: id, decisao: "D3-A", indicador: "Quebra e perdas: campo próprio ou rótulo 'Resultado antes de quebra e perdas'",
      obter: () => campos(id).some((x) => /quebra/.test(x)) || U.contem(f(id), /antes de quebra/i) });
    add({ id: `T8-${id}-02`, ferramenta: id, decisao: "D4", indicador: "Pró-labore: campo próprio ou rótulo 'Resultado antes do seu pró-labore'",
      obter: () => campos(id).some((x) => /pro_?labore|retirada/.test(x)) || U.contem(f(id), /antes do seu pr[óo]-labore/i) });
    add({ id: `T8-${id}-03`, ferramenta: id, decisao: "D1", indicador: "Sem 'ROI' sem qualificador (usa 'retorno anual' / 'retorno acumulado em 10 anos')",
      obter: () => !U.contem(f(id), /\bROI\b/) });
  }
  add({ id: "T8-A09-04", ferramenta: "A09", decisao: "D2-C", indicador: "Reserva de reposição: campo próprio ou rótulo 'Antes da reserva de reposição'",
    obter: () => campos("A09").some((x) => /reserva/.test(x)) || U.contem(f("A09"), /antes da reserva de reposi/i) });
  add({ id: "T8-B08-04", ferramenta: "B08", decisao: "D7-C", indicador: "Valor de saída com método identificado (múltiplo do EBITDA, avaliação patrimonial ou valor informado)",
    obter: () => U.contem(f("B08"), /m[úu]ltiplo do EBITDA|avalia[çc][ãa]o patrimonial/i) });
  return c;
};

// Estados de exemplo das oito fichas (dados fictícios) para as telas do vídeo e o tutorial. Uso: require("./estado_exemplo.js")()
const path = require("path"); const D = path.resolve(__dirname, "../../../../docs/trilha2");
module.exports = function () {
  const Z = require(path.join(D, "qualidade/logic.js")); const st = {};
  st["zion-t2-marco-zero"] = { situacao: "dono", quem: "so", tipo: "Cabanas ou chalés", unidades: "4", nome: "Ana Exemplo", email: "ana@exemplo.com", hospedagem: "Cabanas do Vale (exemplo)", cinco: { entrou: 2, sobrou: 0, ocupacao: 1, diaria: 2, custo: 0 },
    areas: { metas: 0, financas: 1, preco: 1, vendas: 2, pessoas: 1, compras: 2, operacao: 1, qualidade: 0 }, rotina: "as-vezes", tempo: "operacao", saida: "acho", prazo: "2026-12-15", pdf: "2026-11-09T10:00:00.000Z", tela: 6 };
  Z.PAGINAS.slice(1, 7).forEach((p) => { const m = require(path.join(D, p.slug, "logic.js")); st[p.chave] = Object.assign({}, m.EXEMPLO || m.exemplo(), { nome: "Ana Exemplo", email: "ana@exemplo.com", hospedagem: "Cabanas do Vale (exemplo)", pdf: "2026-11-09T12:00:00.000Z" }); });
  return st;
};

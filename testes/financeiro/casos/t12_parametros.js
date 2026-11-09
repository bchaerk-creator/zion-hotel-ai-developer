// T12 · Parâmetros pendentes de validação econômica (não é teste de fórmula).
// Cada caso mostra o valor em uso hoje em cada ferramenta e fica PENDENTE até haver evidência
// por tipo de hospedagem, porte e perfil.
"use strict";
const E = require("../esperados"), { TIPO } = require("../lib/base");
module.exports = (D) => {
  const Z = D.zaios, Fz = () => D.folha.api.REF;
  const atual = {
    "Deduções sobre a receita": () => ({ ZAIOS: Z && Z.receitas.REF_DEDUCOES, "Folha J2": D.folha && (Fz().deducoesPct + Fz().cancelamentosPct) / 100 }),
    "Quebra e perdas": () => ({ ZAIOS: Z && Z.receitas.REF_QUEBRA, "Folha J2": D.folha && Fz().quebraPct / 100 }),
    "Reserva de reposição": () => ({ ZAIOS: Z && Z.receitas.REF_RESERVA, "Folha J2": D.folha && Fz().reservaPct / 100 }),
    "Valor da hora do pró-labore (R$)": () => ({ "Folha J2 (exemplo)": D.folha && D.folha.api.EXEMPLO.retiradaValorHora }),
    "Rampa do 1º ano (meses 1–3, 4–6, 7–12)": () => ({ ZAIOS: Z && [Z.receitas.fatorRampa(1), Z.receitas.fatorRampa(4), Z.receitas.fatorRampa(7)] }),
    "OS&E sobre FF&E": () => ({ ZAIOS: Z && Z.capex.OSE_REFERENCIA }),
    "Pré-abertura sobre a base": () => ({ ZAIOS: Z && Z.capex.PRE_REFERENCIA }),
    "Contingência primeira obra": () => ({ ZAIOS: Z && Z.capex.CONTINGENCIA_FAIXA.primeira }),
    "Contingência com experiência": () => ({ ZAIOS: Z && Z.capex.CONTINGENCIA_FAIXA.experiente }),
    "Cenário conservador (diária, ocupação)": () => ({ ZAIOS: Z && [Z.viabilidade.CENARIOS.conservador.diaria, Z.viabilidade.CENARIOS.conservador.ocupacao] }),
    "Cenário otimista (diária, ocupação)": () => ({ ZAIOS: Z && [Z.viabilidade.CENARIOS.otimista.diaria, Z.viabilidade.CENARIOS.otimista.ocupacao] }),
    "Múltiplo de saída (método 1)": () => ({ ZAIOS: Z && Z.viabilidade.REF_MULTIPLO_SAIDA }),
    "Régua: payback passa / ajustar (anos)": () => ({ ZAIOS: Z && [Z.viabilidade.passoPayback(8) === "passa" ? 8 : "?", Z.viabilidade.passoPayback(12) === "ajustar" ? 12 : "?"] }),
    "Régua: colchão mínimo sobre o CAPEX": () => ({ ZAIOS: Z && Z.viabilidade.COLCHAO_MINIMO }),
    "Régua: déficit conservador aceito (meses de fixo)": () => ({ ZAIOS: Z && (Z.viabilidade.passoConservador(-300, 100) === "ajustar" ? 3 : "?") }),
  };
  return E.T12.map((p, i) => ({
    teste: "T12", id: `T12-${String(i + 1).padStart(2, "0")}`, ferramenta: "todas", indicador: p.parametro, decisao: p.decisao,
    tipo: TIPO.ECONOMICO, esperado: p.referencia, faixa: p.faixa, requer: null, obter: atual[p.parametro] || (() => ({})),
  }));
};

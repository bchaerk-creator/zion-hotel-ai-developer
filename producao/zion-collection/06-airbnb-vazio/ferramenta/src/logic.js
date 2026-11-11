/* Diagnóstico Zion de Oferta · lógica pura (sem dependências; roda no navegador e no Node).
   Regras documentadas em ../REGRAS.md. Indicador orientativo: não prevê reservas nem faturamento. */
(function (root) {
  "use strict";
  var DIMENSOES = [
    { id: "fotos", nome: "Fotos e apresentação", pergunta: "A primeira foto e a sequência mostram com clareza o que o hóspede vai viver?", acao: "Refazer a ordem das 10 primeiras fotos: a primeira mostra a oferta, as seguintes respondem às dúvidas (quarto, banheiro, cozinha, área externa).", indicador: "Taxa de consulta (consultas ÷ visualizações)" },
    { id: "titulo", nome: "Título e descrição", pergunta: "O título diz para quem é e o que tem de diferente, e a descrição traz fatos verificáveis?", acao: "Reescrever o título com público + diferencial + localização e abrir a descrição com 3 fatos que o hóspede procura.", indicador: "Taxa de consulta e perguntas repetidas no chat" },
    { id: "preco", nome: "Preço e posicionamento", pergunta: "A diária respeita o piso de custo e está coerente com anúncios realmente comparáveis?", acao: "Calcular o piso da diária e comparar com 3 concorrentes da mesma região, capacidade e padrão para as mesmas datas.", indicador: "Ocupação e diária média nas mesmas datas" },
    { id: "diferenciais", nome: "Diferenciais e experiência", pergunta: "Os diferenciais são percebidos pelo hóspede e aparecem no anúncio com prova?", acao: "Listar 3 diferenciais, transformar cada um em benefício e mostrar a prova (foto, detalhe, regra).", indicador: "Menções aos diferenciais nas avaliações" },
    { id: "avaliacoes", nome: "Avaliações e confiança", pergunta: "As avaliações e as respostas públicas passam segurança para quem ainda não conhece você?", acao: "Ler as últimas avaliações, achar o padrão de crítica, responder com respeito e corrigir a causa.", indicador: "Nota média e número de críticas repetidas" },
    { id: "atendimento", nome: "Atendimento e comunicação", pergunta: "As respostas são rápidas, completas e iguais para todo hóspede?", acao: "Criar respostas-padrão para as 5 perguntas mais frequentes e definir o prazo máximo de primeira resposta.", indicador: "Tempo de primeira resposta e taxa de reserva (reservas ÷ consultas)" },
    { id: "conforto", nome: "Conforto e infraestrutura", pergunta: "Cama, banho, limpeza, internet e itens básicos entregam o que o anúncio promete?", acao: "Fazer uma vistoria como hóspede e corrigir primeiro o que aparece em reclamações ou fotos.", indicador: "Críticas sobre conforto e itens corrigidos" }
  ];
  var ESCALA = ["Ausente", "Muito fraco", "Fraco", "Parcial", "Bom", "Consistente e comprovado"];
  var FAIXAS = [
    { min: 85, nome: "Oferta consistente", texto: "Mantenha o que funciona e acompanhe os indicadores. Revise a cada 30 dias." },
    { min: 70, nome: "Boa base com pontos de melhoria", texto: "A oferta tem base. Concentre energia nas três prioridades antes de mexer no resto." },
    { min: 50, nome: "Ajustes prioritários", texto: "Há pontos que pesam na decisão do hóspede. Comece pelas prioridades, uma por semana." },
    { min: 0, nome: "Lacunas relevantes", texto: "Antes de mexer no preço, resolva as lacunas básicas de apresentação, informação e confiança." }
  ];
  var STATUS = ["A fazer", "Em andamento", "Feito"];

  function nota(v) {
    if (v === null || v === undefined) return { ok: false, vazio: true, erro: "Dê uma nota de 0 a 5." };
    var s = String(v).trim().replace(",", ".");
    if (s === "") return { ok: false, vazio: true, erro: "Dê uma nota de 0 a 5." };
    if (!/^-?\d+(\.\d+)?$/.test(s)) return { ok: false, erro: "Use só números de 0 a 5." };
    var n = Number(s);
    if (n < 0 || n > 5) return { ok: false, erro: "A nota vai de 0 a 5." };
    if (n !== Math.floor(n)) return { ok: false, erro: "Use nota inteira (0, 1, 2, 3, 4 ou 5)." };
    return { ok: true, valor: n };
  }

  function custo(v) {
    if (v === null || v === undefined || String(v).trim() === "") return { ok: true, valor: null };
    var s = String(v).trim().replace(/^R\$\s*/i, "").replace(/\./g, "").replace(",", ".");
    if (!/^\d+(\.\d{1,2})?$/.test(s)) return { ok: false, erro: "Use um valor em reais, por exemplo 150 ou 150,00." };
    return { ok: true, valor: Number(s) };
  }

  function dataISO(v) {
    if (!v) return { ok: true, valor: "" };
    if (!/^\d{4}-\d{2}-\d{2}$/.test(v)) return { ok: false, erro: "Data inválida." };
    var d = new Date(v + "T12:00:00Z");
    if (isNaN(d) || d.toISOString().slice(0, 10) !== v) return { ok: false, erro: "Data inválida." };
    return { ok: true, valor: v };
  }

  /* respostas: { fotos: {nota, evidencia}, ... } */
  function calcular(respostas) {
    respostas = respostas || {};
    var itens = [], erros = {}, avisos = [], soma = 0, completos = 0;
    DIMENSOES.forEach(function (d, i) {
      var r = respostas[d.id] || {}, n = nota(r.nota), ev = String(r.evidencia || "").trim();
      if (!n.ok) erros[d.id] = n.erro; else { soma += n.valor; completos++; }
      if (n.ok && !ev) avisos.push("Sem evidência em " + d.nome + ": a nota vira hipótese até você registrar uma prova.");
      itens.push({ id: d.id, nome: d.nome, ordem: i, nota: n.ok ? n.valor : null, evidencia: ev, temEvidencia: !!ev, pct: n.ok ? n.valor * 20 : null });
    });
    var completo = completos === DIMENSOES.length;
    var pontuacao = completo ? Math.round(soma / 35 * 100) : null;
    var faixa = completo ? FAIXAS.filter(function (f) { return pontuacao >= f.min; })[0] : null;
    var prioridades = completo ? itens.slice().sort(function (a, b) { return a.nota - b.nota || a.ordem - b.ordem; }).slice(0, 3) : [];
    var todasMaximas = completo && soma === 35;
    return { completo: completo, faltam: DIMENSOES.length - completos, soma: soma, pontuacao: pontuacao, faixa: faixa,
      itens: itens, prioridades: prioridades, erros: erros, avisos: avisos, todasMaximas: todasMaximas,
      semEvidencia: itens.filter(function (x) { return x.nota !== null && !x.temEvidencia; }).length,
      criticas: itens.filter(function (x) { return x.nota !== null && x.nota <= 1; }).map(function (x) { return x.nome; }) };
  }

  function sugestaoPlano(diag) {
    return diag.prioridades.map(function (p) {
      var d = DIMENSOES[p.ordem];
      return { dimensao: d.nome, acao: d.acao, responsavel: "", prazo: "", custo: "", indicador: d.indicador, status: "A fazer" };
    });
  }

  function validarPlano(linhas) {
    var erros = [];
    (linhas || []).forEach(function (l, i) {
      var n = i + 1;
      if (!String(l.acao || "").trim()) erros.push("Ação " + n + ": descreva a ação.");
      if (!String(l.responsavel || "").trim()) erros.push("Ação " + n + ": defina o responsável.");
      var dt = dataISO(l.prazo); if (!l.prazo) erros.push("Ação " + n + ": defina o prazo."); else if (!dt.ok) erros.push("Ação " + n + ": " + dt.erro);
      var c = custo(l.custo); if (!c.ok) erros.push("Ação " + n + ": " + c.erro);
      if (!String(l.indicador || "").trim()) erros.push("Ação " + n + ": defina como vai medir.");
      if (STATUS.indexOf(l.status) < 0) erros.push("Ação " + n + ": status inválido.");
    });
    return { valido: erros.length === 0 && (linhas || []).length > 0, erros: erros };
  }

  function csvCampo(v) {
    var s = v === null || v === undefined ? "" : String(v);
    if (/^[=+\-@\t\r]/.test(s)) s = "'" + s; // evita fórmula ao abrir na planilha
    return /[";\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
  }
  function gerarCSV(perfil, diag, plano) {
    var L = [];
    L.push(["Diagnóstico Zion de Oferta"].map(csvCampo).join(";"));
    L.push(["Hospedagem", perfil && perfil.nome || ""].map(csvCampo).join(";"));
    L.push(["Período de referência", perfil && perfil.periodo || ""].map(csvCampo).join(";"));
    L.push(["Pontuação geral (0 a 100)", diag.pontuacao === null ? "incompleto" : diag.pontuacao].map(csvCampo).join(";"));
    L.push(["Faixa", diag.faixa ? diag.faixa.nome : ""].map(csvCampo).join(";"));
    L.push("");
    L.push(["Dimensão", "Nota (0 a 5)", "Evidência"].join(";"));
    diag.itens.forEach(function (x) { L.push([x.nome, x.nota === null ? "" : x.nota, x.evidencia].map(csvCampo).join(";")); });
    L.push("");
    L.push(["Prioridade", "Dimensão", "Ação", "Responsável", "Prazo", "Custo estimado (R$)", "Indicador", "Status"].join(";"));
    (plano || []).forEach(function (l, i) { L.push([i + 1, l.dimensao, l.acao, l.responsavel, l.prazo, l.custo, l.indicador, l.status].map(csvCampo).join(";")); });
    L.push("");
    L.push(csvCampo("Indicador orientativo. Não é previsão de reservas, ocupação ou faturamento."));
    return "﻿" + L.join("\r\n");
  }

  function exemplo() {
    return {
      perfil: { nome: "Apartamento Exemplo (dados fictícios)", periodo: "Últimos 90 dias", obs: "Exemplo para aprender a usar a ferramenta." },
      respostas: {
        fotos: { nota: 2, evidencia: "Primeira foto é da fachada; quarto só aparece na 7ª foto." },
        titulo: { nota: 3, evidencia: "Título diz 'Lindo apê', sem público nem diferencial." },
        preco: { nota: 3, evidencia: "Diária igual todos os dias; não conheço meu piso de custo." },
        diferenciais: { nota: 4, evidencia: "Varanda com vista citada em 4 avaliações." },
        avaliacoes: { nota: 4, evidencia: "Nota alta; 2 críticas sobre barulho sem resposta." },
        atendimento: { nota: 2, evidencia: "Respondo em até 6 horas; cada hóspede recebe um texto diferente." },
        conforto: { nota: 4, evidencia: "Cama e limpeza elogiadas; chuveiro fraco citado uma vez." }
      }
    };
  }

  var API = { DIMENSOES: DIMENSOES, ESCALA: ESCALA, FAIXAS: FAIXAS, STATUS: STATUS, nota: nota, custo: custo, dataISO: dataISO,
    calcular: calcular, sugestaoPlano: sugestaoPlano, validarPlano: validarPlano, gerarCSV: gerarCSV, csvCampo: csvCampo, exemplo: exemplo };
  if (typeof module !== "undefined" && module.exports) module.exports = API; else root.DZO = API;
})(typeof window !== "undefined" ? window : this);

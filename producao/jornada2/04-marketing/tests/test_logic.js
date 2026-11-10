// Testes da lógica pura da ficha "A minha Marca e Captação". Uso: node tests/test_logic.js
const Z = require("../src/logic.js");
let ok = 0, fal = 0;
const t = (b, m) => { b ? ok++ : fal++; console.log((b ? "  ok  " : "  FALHOU  ") + m); };
const perto = (a, b, tol = 1e-6) => a != null && Math.abs(a - b) <= tol;
const EX = Z.EXEMPLO;
const clone = (o) => JSON.parse(JSON.stringify(o));
const com = (o) => Object.assign(clone(EX), o);
const comCanal = (k, o) => { const s = clone(EX); Object.assign(s.canais[k], o); return s; };

console.log("Conversão de números (versão corrigida do Módulo 1)");
t(Z.num("16.240,00") === 16240 && Z.num("1234.56") === 1234.56 && Z.num(" R$ 280 ") === 280, "aceita formato brasileiro, ponto decimal e R$");
t(Z.num("13.000") === 13000 && Z.num("1.234.567") === 1234567 && Z.num("8.120") === 8120, "ponto de milhar sem vírgula: 13.000 = treze mil");
t(Z.num("4.7") === 4.7 && Z.num("12.5") === 12.5 && Z.num("40%") === 40, "ponto decimal mantido; símbolo de percentual aceito");
t(Z.num("") === null && Z.num("abc") === null && Z.num("12a") === null && Z.num(null) === null, "vazio e texto viram null");
t(Z.dataBR("2027-06-30") === "30/06/2027" && Z.dataBR("2027-02-30") === "", "data no formato brasileiro; data inexistente é rejeitada");

console.log("Nível de abertura (4 perguntas)");
t(Z.nivel({ diag: {} }).n === 1 && Z.nivel(EX).r === "Audiência alugada", "zero sim = nível 1 (exemplo: Audiência alugada)");
t(Z.nivel({ diag: { promessa: "sim", lista: "sim" } }).n === 2 && Z.nivel({ diag: { promessa: "sim", lista: "sim", canal: "sim" } }).n === 3, "dois sim = 2; três sim = 3");
t(Z.nivel({ diag: { promessa: "sim", lista: "sim", canal: "sim", custo: "sim" } }).r === "Captação com número", "quatro sim = Captação com número");

console.log("Adjetivos genéricos (Etapa 05)");
t(Z.adjetivos(EX.promessa).length === 0, "a promessa do exemplo não tem adjetivo genérico");
t(Z.adjetivos("Cabana aconchegante com vista incrível").join(",") === "aconchegante,incrivel", "acha aconchegante e incrível");
t(Z.adjetivos("Experiência ÚNICA e Inesquecível, lugar perfeito").join(",") === "unica,inesquecivel,perfeito", "ignora acento e maiúscula");
t(Z.adjetivos("especialmente perto da unicidade").length === 0, "não confunde palavra maior (especialmente)");

console.log("Exemplo didático · dados fictícios (Cabanas do Vale, coerente com os Módulos 1, 2 e 3)");
const r = Z.calcular(EX);
t(r.linhas.length === 5, "cinco canais preenchidos (a sexta linha vazia é ignorada)");
t(perto(r.receita, 16240) && r.reservas === 25, "receita de hospedagem R$ 16.240,00 e 25 reservas (Módulo 2)");
t(perto(r.linhas[0].custo, 1299.2) && perto(r.linhas[0].custoPorReserva, 108.2666667, 1e-6) && Z.brl(r.linhas[0].custoPorReserva) === "R$ 108,27", "Plataforma A: 16% de R$ 8.120 = R$ 1.299,20; R$ 108,27 por reserva");
t(perto(r.linhas[1].custo, 487.2) && perto(r.linhas[1].custoPorReserva, 97.44), "Plataforma B: 15% de R$ 3.248 = R$ 487,20; R$ 97,44 por reserva");
t(perto(r.linhas[2].custoPorReserva, 75) && r.linhas[3].custoPorReserva === 0 && r.linhas[4].custoPorReserva === 0, "Instagram R$ 150 ÷ 2 = R$ 75,00; hóspede que volta e indicação R$ 0,00");
t(perto(r.custo, 1936.4) && perto(r.custoPorReserva, 77.456) && Z.brl(r.custoPorReserva) === "R$ 77,46", "custo total R$ 1.936,40; média R$ 77,46 por reserva");
t(Z.pct(r.custoSobreReceita) === "11,9%", "captação = 11,9% da receita de hospedagem");
t(perto(r.comissaoPlataformas / r.receita, 0.11), "comissão das plataformas = 11,0% da receita total (igual ao Módulo 2)");
t(perto(r.vendaDireta, 0.30) && perto(r.receitaDireta, 4872) && r.reservasDiretas === 8 && perto(r.vendaDiretaReservas, 0.32), "venda direta 30% da receita (R$ 4.872,00), 8 de 25 reservas (Módulo 3)");
t(perto(r.receitaDiretaMeta, 6496) && perto(r.comissaoEvitada, 255.2, 1e-6), "meta 40%: R$ 6.496,00 de venda direta; comissão que deixaria de sair R$ 255,20 (igual ao Módulo 3)");
t(perto(r.comissaoMediaPlataformas, 1786.4 / 11368), "comissão média das plataformas = 15,7%");
t(r.maisBarato.nome.startsWith("Hóspede que volta") && r.maisCaro.nome === "Plataforma A", "mais barato: hóspede que volta; mais caro: Plataforma A");
t(perto(r.custoPorReservaDireta, 18.75), "custo por reserva dos canais diretos = R$ 18,75");
t(r.faltamLista === 120 && perto(r.porMesLista, 10) && perto(r.pctEstadiasLista, 0.4), "lista: 120 em 12 meses = 10 autorizações por mês, 40% das 25 estadias");
t(r.testesSim === 4 && r.pontosSim.length === 2 && r.pontosFaltando.map((x) => x.id).join() === "site,whatsapp,boasvindas,placa", "marca: 4 de 4 testes; aparece em 2 pontos e falta em 4");
const le = Z.leituras(r, EX);
t(le.length === 4 && /R\$ 108,27/.test(le[0]) && /R\$ 77,46/.test(le[0]) && /11,9%/.test(le[0]), "leitura 1: custo por reserva do mais barato ao mais caro");
t(/30,0%/.test(le[1]) && /40,0% até 30\/06\/2027/.test(le[1]) && /R\$ 6\.496,00/.test(le[1]) && /R\$ 255,20/.test(le[1]) && /não previsão/.test(le[1]), "leitura 2: venda direta, meta com prazo e comissão (não previsão)");
t(/0 contatos com autorização hoje, de 64/.test(le[2]) && /10 autorizações por mês, 40% das 25/.test(le[2]), "leitura 3: ritmo da lista");
t(/4 de 4 testes e 4 de 5/.test(le[3]) && /o site, a resposta de WhatsApp, a mensagem de boas-vindas e a placa na entrada/.test(le[3]), "leitura 4: marca e pontos de contato");
const at = Z.atencao(r, EX);
t(at.map((a) => a.id).join() === "semAutorizacao,guardada,cinco", "atenção no exemplo: lista sem autorização, guardada no celular, 4 de 5 entenderam");
t(/64 contatos/.test(at[0].t) && /4 de 5/.test(at[2].t), "textos das atenções usam os números do exemplo");
const pl = Z.planoSugerido(EX, r).split("\n");
t(pl.length === 6 && /^1\. No próximo check-in/.test(pl[0]) && /Você pode sair quando quiser"\. Registrar/.test(pl[0]), "plano: 6 passos, começa pelo pedido de autorização com a frase");
t(/Kit de Mensagens, Ferramenta 11/.test(pl[2]) && /cinco pessoas/.test(pl[3]) && /WhatsApp: os quatro contatos do ano/.test(pl[4]) && /40,0%/.test(pl[5]), "plano: pontos de contato com o Kit 11, teste das cinco pessoas, canal único, reunião semanal");
const F = Z.folha(EX);
t(F.map((f) => f.r).join("|") === "Para quem|Promessa|Prova|Tom|O que nunca fazemos" && /Não é para: Grupos/.test(F[0].t) && /Nunca escrevemos: aconchegante/.test(F[3].t), "marca em uma folha: para quem, promessa, prova, tom e o que nunca fazemos");
t(Z.folha(com({ nunca: "" })).length === 4, "sem 'o que nunca fazemos', a folha tem as quatro linhas obrigatórias");
t(/30 dias/.test(Z.comoVerificar(r, EX)) && /pontos de contato que faltavam/.test(Z.comoVerificar(r, EX)), "como verificar: 30 dias e pontos de contato");
t(Z.completo(EX) && !Z.concluido(EX), "exemplo completo, mas não concluído sem plano, data e PDF");
t(Z.concluido(com({ acao: "Pedir a autorização no check-in.", prazo: "2026-11-20", pdf: "x" })), "concluído com plano, data e PDF");
t(Z.pendencias(com({ acao: "curto" })).join("|").includes("10 letras"), "plano curto fica pendente");

console.log("Validação · marca e prova");
t(!Z.validar(com({ publico: "" }), "marca").ok && !Z.validar(com({ promessa: "curta" }), "marca").ok, "público e promessa obrigatórios");
t(/teste da memória/.test(Z.validar(com({ testes: { recusa: "sim", cumprimento: "sim", diferenca: "sim" } }), "marca").erros.join()), "os quatro testes precisam de resposta");
t(!Z.validar(com({ cinco: "" }), "marca").ok && Z.validar(com({ cinco: "nt" }), "marca").ok, "teste das cinco pessoas: escolha obrigatória, 'ainda não testei' vale");
const va = Z.validar(com({ promessa: "Cabana aconchegante com vista incrível para casais" }), "marca");
t(va.ok && /adjetivo genérico/.test(va.avisos.join()), "adjetivo genérico vira aviso, não bloqueio");
t(/quem não é/.test(Z.validar(com({ naoPublico: "" }), "marca").avisos.join()), "sem 'para quem não é': aviso");
t(!Z.validar(com({ prova: "" }), "prova").ok && !Z.validar(com({ tom: "" }), "prova").ok, "prova e tom obrigatórios");
t(/ponto de contato/.test(Z.validar(com({ pontos: { anuncio: "sim" } }), "prova").erros.join()), "todos os pontos de contato precisam de resposta");

console.log("Validação · lista própria");
t(Z.validar(com({ contatos: "0", autorizados: "0" }), "lista").ok, "zero contatos é aceito (a lista começa hoje)");
t(/não pode passar/.test(Z.validar(com({ contatos: "10", autorizados: "12" }), "lista").erros.join()), "autorizados acima do total bloqueia");
t(!Z.validar(com({ contatos: "3,5" }), "lista").ok && !Z.validar(com({ autorizados: "-1" }), "lista").ok, "contatos fracionados ou negativos bloqueiam");
t(!Z.validar(com({ onde: "" }), "lista").ok && !Z.validar(com({ frase: "oi" }), "lista").ok && !Z.validar(com({ canalLista: "Instagram" }), "lista").ok, "lugar, frase e canal (WhatsApp ou e-mail) obrigatórios");
t(/menor que/.test(Z.validar(com({ autorizados: "30", metaLista: "20" }), "lista").erros.join()), "meta da lista menor que os autorizados de hoje bloqueia");
t(!Z.validar(com({ estadiasMes: "0" }), "lista").ok && !Z.validar(com({ metaLista: "0" }), "lista").ok, "estadias e meta a partir de 1");

console.log("Validação · canais e meta");
t(/dê um nome/.test(Z.validar(comCanal(5, { reservas: "2" }), "canais").erros.join()), "linha com número e sem nome bloqueia");
t(/plataforma ou direto/.test(Z.validar(comCanal(0, { tipo: "" }), "canais").erros.join()), "tipo obrigatório");
t(/negativa/.test(Z.validar(comCanal(1, { receita: "-10" }), "canais").erros.join()) && /0 a 99/.test(Z.validar(comCanal(1, { comissao: "120" }), "canais").erros.join()), "receita negativa e comissão fora da faixa bloqueiam");
t(/receita sem reserva/.test(Z.validar(comCanal(2, { reservas: "0" }), "canais").erros.join()), "receita sem reserva bloqueia");
const sem = clone(EX); sem.canais = sem.canais.map(() => ({ nome: "", tipo: "", comissao: "", gasto: "", reservas: "", receita: "" }));
t(/pelo menos um canal/.test(Z.validar(sem, "canais").erros.join()), "nenhum canal bloqueia");
const soPlat = clone(EX); soPlat.canais = [soPlat.canais[0], soPlat.canais[1]];
const vp = Z.validar(soPlat, "canais");
t(vp.ok && /Nenhum canal direto/.test(vp.avisos.join()) && Z.calcular(soPlat).vendaDireta === 0, "só plataformas: aceito, com aviso, venda direta 0%");
t(/comissão/.test(Z.validar(comCanal(0, { comissao: "" }), "canais").avisos.join()), "plataforma sem comissão: aviso");
t(!Z.validar(com({ metaDireta: "0" }), "meta").ok && !Z.validar(com({ metaDireta: "120" }), "meta").ok && !Z.validar(com({ prazoMeta: "" }), "meta").ok && !Z.validar(com({ prazoMeta: "2027-13-01" }), "meta").ok, "meta de 0 a 100 e prazo com data válida");

console.log("Regras de atenção (ordem e disparo)");
const ruim = com({ autorizados: 5, onde: "plataforma", promessa: "Experiência única e inesquecível na serra", testes: { recusa: "nao", cumprimento: "sim", diferenca: "nao", memoria: "sim" }, cinco: "nt", metaDireta: 25, metaLista: 2000 });
ruim.canais[2].gasto = 400; ruim.canais[5] = { nome: "Anúncio pago", tipo: "direto", comissao: 0, gasto: 200, reservas: 0, receita: 0 };
const ra = Z.atencao(Z.calcular(ruim), ruim, { base: 30, meta: 40 });
t(ra.map((a) => a.id).join() === "guardada,adjetivo,testes,cinco,caroDireto,gastoSemReserva,metaAbaixo,painel,ritmo", "cenário ruim dispara 9 regras na ordem: " + ra.map((a) => a.id).join());
t(/Só dentro|não é seu/.test(ra[0].t) && /recusa, diferença/.test(ra[2].t) && /R\$ 200,00 por reserva/.test(ra[4].t) && /Plataforma B \(R\$ 97,44\)/.test(ra[4].t), "textos: plataforma, testes que falharam, esforço direto R$ 200 contra Plataforma B R$ 97,44");
t(/40,0%/.test(ra[7].t) && /25,0%/.test(ra[7].t) && /mais que as 25 estadias/.test(ra[8].t), "meta diferente do Painel e ritmo maior que as estadias");
t(Z.atencao(Z.calcular(EX), EX, { base: 30, meta: 40 }).every((a) => a.id !== "painel"), "mesma meta do Painel: sem alerta");
t(Z.daPainel({ base_vendaDireta: "30", meta_vendaDireta: "40" }).meta === 40 && Z.daPainel({}) === null && Z.daPainel(null) === null, "lê o Painel do Módulo 1 (ou nada)");
const limpo = com({ autorizados: 40, onde: "nuvem", cinco: "5" });
t(Z.atencao(Z.calcular(limpo), limpo).length === 0, "tudo em ordem: nenhuma atenção");
t(Z.planoSugerido(limpo).split("\n").length === 5, "promessa testada em 5 de 5: plano sem o passo do teste");
t(/Não aumentar o gasto/.test(Z.planoSugerido(ruim)), "esforço direto caro entra no plano");

console.log("Telas");
t(Z.TELAS.join() === "abertura,marca,prova,lista,canais,meta,resultado" && Z.proximaVazia(com({ frase: "" })) === "lista", "seis telas + resultado; continuar leva à primeira tela incompleta");
t(Z.PROXIMO.n === 5, "próxima etapa: Módulo 5");

console.log(`\n${ok} ok, ${fal} falhou`); process.exit(fal ? 1 : 0);

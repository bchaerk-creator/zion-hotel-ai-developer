# Trilha 1 · Pilar 6 · Aprofundamento 6B · Viabilidade · Plano da lição

Status: plano de produção, versão 1 (28/11/2026), escrito pelo arquiteto pedagógico para o roteirista, o construtor e o designer. Nada foi produzido nem publicado. O ClickMax não foi tocado. As decisões marcadas **[a confirmar por Bruno]** já orientam a produção, mas Bruno pode trocá-las antes do "aprovado". A lista completa está na seção 12.

Base lida: `CLAUDE.md`; `producao/fabrica/FABRICA.md` (seção 3); skill `zion-learning-design` (`SKILL.md`); `producao/trilha1-aprofundamento/GUIA_COERENCIA.md` (inteiro); o plano v2 e o relatório da 6A (`01-capex/PLANO.md`, `RELATORIO.md`), usados como molde de estrutura, nomes e caso; o mapa de fontes `exportacao-zion/lições/viabilidade/MAPA_FONTES_VIABILIDADE.md` (fora do repositório público; só ele como fonte de regras de viabilidade); a ficha do Pilar 6 (`docs/trilha1/pilar6/index.html`: `REF`, `calcular`, `vereditoSugerido`, `criterioSug`, `compromisso`); a ficha do Pilar 2 (`docs/trilha1/aula2/index.html`: textos `marina:` e campos do calendário); a ficha da 6A (`docs/trilha1/pilar6a/logic.js`: `resumoDados`); a Planilha 2 pelo gerador `producao/clube/planilhas/src/build.py` (função `planilha_viabilidade`, abas e células); as decisões da ZAIOS de 08/11/2026 (`docs/zaios/PREMISSAS_FINANCEIRAS_E_VERIFICACOES.md`); o formato dos tutoriais (`producao/clube/tutoriais-video/specs/ficha-pilar6.json`).

**Uma divergência com o mapa de fontes, resolvida pelo pedido de Bruno:** o mapa (seções 5.1 e 8.2) recomendava não usar a Marina e seguir com a Helena. Bruno exige coerência total com a linha do curso, e a 6A v2 já trocou a Helena pela Marina. Esta lição usa **a Marina**, partindo da 6A dela. Os números de custo dela nesta lição são novos, fictícios e rotulados; nenhum número da Marina do F02, do F03 ou do A08 é reaproveitado.

Códigos de fonte (os do mapa e os do curso): **P2, P3, P4, P5, P6, P7** e-books e fichas dos Pilares; **6A** a lição CAPEX; **MZ** Marco Zero; **CA** Comece aqui; **MAPA** Mapa de direcionamento (etapa 6); **PL2** Planilha 2; **F02** e-book "Receitas, Custos e Modelos de Rentabilidade"; **F03** e-book "Viabilidade e Análise de Investimentos"; **ZAIOS** decisões de 08/11/2026; **A05** Volume A05 · Investimento; **VOL05** Volume 05 · Investimento; **JC02, JC08, JC09** Jornada do COMO (JC02 só "via F02/F03", como no mapa); **VOL04** Volume 04 · Estratégia (só a pergunta ao contador); **A08** Volume A08; **R1…R34** regras numeradas do mapa; **GUIA** guia de coerência. O resto é **elaboração própria** e está marcado assim.

---

## 0. Encaixe na sequência do curso

| Item | Valor |
|---|---|
| Nome da lição | «Aprofundamento 6B · Viabilidade · Aprenda o passo a passo para saber se a conta do seu projeto fecha» |
| Página do Dossiê | «Página 6B · Viabilidade» (irmã das páginas 6 e 6A; não muda a contagem de sete páginas, GUIA 3.4) |
| Ferramenta | «Faça agora · A sua conta» em `docs/trilha1/pilar6b/` |
| Chave salva | `zion-t1-pilar6b` |
| Aula | `docs/trilha1/apresentacao/pilar6b-aula/` |
| PDFs | `docs/trilha1/materiais/Pilar-6B-Viabilidade-ebook.pdf`, `Pilar-6B-Viabilidade-checklist.pdf` |
| Capas | `docs/trilha1/capas/p6b-c-aula.jpg`, `p6b-c-faca.jpg`, `p6b-c-tutorial.jpg`, `p6b-c-ebook.jpg`, `p6b-c-check.jpg` |
| Tutorial | `docs/trilha1/videos/tutoriais/tutorial-ficha-pilar6b.mp4` (roteiro em `02-viabilidade/tutorial/ficha-pilar6b.json`) |
| Pergunta do pilar (continua a mesma, GUIA 5.3) | «O negócio se paga?», abrindo a linha que a página 6 fechou com uma margem de referência: **quanto sobra** |
| Recebe | da 6A (`zion-t1-pilar6a`, `resumo.dados`): `capex_fase`, `giro`, `investimento_total`, `terreno`, `terreno_situacao`, `unidades`, `unidades_projeto`, `limite6`; da página 6 (`zion-t1-pilar6`): `diaria`, `ocup_cons`, `ocup_base`, `ocup_otim`, `margem`, `resultado_cons`, `inv8`; da página 2 (`zion-t1-aula2`): `diaria_media`, `ocup_ano` e as respostas `meses_alta`, `meses_fraco`, `ocup_alta`, `ocup_media`, `ocup_fraco`; do Marco Zero: a situação |
| Devolve | a página 6 refeita (campo «Margem operacional» com a margem aberta e a nota certa; «Capital de giro» em meses que reproduzem o giro da 6B) e a Planilha 2 (abas Massas, Investimento e Modelo de renda, células na seção 6.7) |
| Prepara | o Pilar 7: a decisão (avançar, ajustar, redesenhar) com o critério para parar escrito, que o Pilar 7 transforma em pedido ou em redesenho |
| Ordem do Mapa (GUIA 1.3) | página 6 → **6A** (o custo de abrir a porta) → **6B** (quanto sobra e se vale a pena, com a sensibilidade do Mapa feita na conta aberta) → Planilha 1 (opcional) → Planilha 2 → refazer a página 6 → Pilar 7 |

---

## 1. A lição em uma frase e o entregável

**Frase (promessa):** Aprenda o passo a passo para saber se a conta do seu projeto fecha: montar, linha por linha, da receita bruta ao que sobra depois da reserva de reposição, ler o tempo de volta e o caixa do primeiro ano, e decidir por escrito se avança, ajusta ou redesenha antes de assinar a obra.

**Começar a usar × resultado externo:** a primeira versão sai em uma tarde, com a linha do imposto em branco se o contador ainda não respondeu. A resposta do contador e as cotações dos custos fixos levam o tempo deles. A lição não promete retorno, renda, ocupação, crédito, parceria nem aprovação: **cenários, não promessas**.

**Entregável:** a **«Página 6B · Viabilidade»** do Dossiê de Desenvolvimento, PDF de uma página (mais o anexo opcional «Alavancas e cenário ajustado»). Ela serve sozinha numa conversa com o contador, a família ou um sócio. Traz:
- a conta em seis degraus, com a origem de cada número (cotação, estimativa, resposta do contador, em branco);
- a margem aberta, ao lado da margem de referência da página 6, com a explicação da diferença;
- o ponto de equilíbrio com a folga, o custo por diária vendida e a diária de equilíbrio;
- o primeiro ano mês a mês (rampa no calendário), o menor saldo e o colchão;
- o giro pelas duas contas do Pilar 6, e o investimento total refeito;
- o tempo de volta em escada (régua da Zion) e como o Pilar 6 o calcula;
- os três cenários do curso, o teste de queda e a sensibilidade do Mapa;
- "o que precisa ser verdade" com a conta aberta;
- os cinco passos da régua, o veredito sugerido, o veredito escrito pela pessoa e o critério para parar;
- a ação de 30 dias com verificação;
- o quadro «Como levar para a página 6» e o quadro «Planilha 2, célula a célula».

**Termos na tela (sem sigla):** receita bruta, receita real, margem de contribuição, resultado antes da reserva, o que sobra, reserva de reposição, ponto de equilíbrio, folga, tempo de volta, colchão, taxa do seu dinheiro (para o valor presente), valor presente dos próximos dez anos. NOI, EBITDA, VPL, TIR, payback e ROI não aparecem na tela da aula nem da ficha; o e-book cita cada um uma vez, explicado, como o Pilar 6 faz com CAPEX (GUIA 3.2), porque a Planilha 2 usa esses nomes. Os nomes com ™ das fontes (Ponto de Equilíbrio Zion™, Conta da Retirada™ etc.) não vão para a tela; o e-book cita no máximo dois, com a grafia da fonte, nas notas.

---

## 2. Públicos e situações: o que muda para cada um

A primeira tela usa as palavras do Marco Zero, pré-marcadas de `zion-t1-marco-zero`. O curso não usa "Jornada A/B" na tela (GUIA 3.2).

| Situação (texto do Marco Zero) | Jornada (interna) | Público | O que a lição faz | O que muda na ficha |
|---|---|---|---|---|
| «Tenho um terreno e ainda não hospedo ninguém» | quero começar | desenvolvedor | Monta a conta da fase um sobre a 6A, a diária e a ocupação do Pilar 2 e os cenários do Pilar 4 | Fluxo completo; rampa do primeiro ano obrigatória |
| «Tenho uma ideia, ou o capital, e ainda não tenho o terreno» | quero começar | desenvolvedor | Igual, com o aviso de que a 6A só se fecha com o terreno escolhido | Aviso fixo; terreno «vou comprar» lido da 6A; alerta do terreno no tempo de volta |
| «Já opero uma hospedagem e quero crescer» | já opero | gestor | Troca estimativa por extrato de doze meses (R30) e faz a conta **da ampliação**: receita e custos que a ampliação acrescenta | Interruptor «conta da ampliação»: linhas fixas marcadas «já existe» ou «novo»; só as novas entram no fixo da ampliação; rampa só para as unidades novas; alerta «não pague a obra com o caixa da operação» (6A, A19) |
| Caixa extra: «Estou fazendo para o projeto de outra pessoa» | ambas | operador | Prepara a 6B para levar ao dono | O trabalho do operador entra como custo fixo (salário) ou como custo do modelo (taxa de gestão, degrau 5); a retirada é a do dono, se ele também trabalhar |

No e-book e na aula, cada capítulo traz as duas aplicações com as frases do curso: «Se você ainda não hospeda: …» e «Se você já opera e quer crescer: troque cada estimativa de receita e custo pelo seu extrato de doze meses…» (P6 cap. 00; GUIA 5.7).

Reversão pela expertise: quem já tem lista de custos com o contador e extrato marca isso no diagnóstico e vê «pule para a ficha; o tutorial fica de consulta».

---

## 3. Objetivos (verbos observáveis) e onde a ficha mede cada um

| # | Objetivo | Nível | Onde a ficha mede |
|---|---|---|---|
| O1 | Explicar por que faturamento não é lucro, lucro não é retorno, e por que a margem de referência da página 6 é uma simplificação | compreender | Tela 1 (página 6 × conta aberta) e o quadro «De onde vem a diferença» no resultado. Exercício E3 |
| O2 | Classificar cada saída de dinheiro no degrau certo (dedução, variável, fixo, custo do modelo, reserva ou fora da conta), sem contar a mesma coisa duas vezes | analisar | Telas 3 a 6 e as confirmações «a comissão não está nos variáveis» e «despesas anuais em duodécimos». Exercício E3 |
| O3 | Calcular os seis degraus, a margem, o ponto de equilíbrio com a folga e o custo por diária vendida | aplicar | Resultado (fórmulas 6.2). Exercícios E2 e E4 |
| O4 | Calcular o primeiro ano mês a mês com a rampa, o menor saldo, o colchão e o giro pelas duas contas | aplicar | Tela 7 e resultado |
| O5 | Avaliar o projeto pela régua da Zion em cinco passos, com três cenários, teste de queda e sensibilidade, e ler "o que precisa ser verdade" | avaliar | Tela 8 e o painel dos cinco passos. Exercício E4 |
| O6 | Propor um redesenho mexendo uma alavanca por vez e dizer o que precisaria ser provado | criar | Simulador de alavancas e cenário ajustado. Exercício E5 |
| O7 | Produzir a página 6B com veredito escrito, critério para parar e ação de 30 dias verificável, e devolvê-la à página 6 e à Planilha 2 | criar | Critério de conclusão (6.6), PDF baixado, quadros de transposição |

---

## 4. As seis etapas

| Etapa | O que a pessoa faz | Peça | Duração alvo | Fonte |
|---|---|---|---|---|
| **1 · Diagnosticar** | Abre com a 6A e a página 6 dela («veio da página 6A», «veio da página 6») e responde 4 perguntas: tem lista de custos fixos? o contador já respondeu o imposto? o seu trabalho está na conta? tem a curva do ano do Pilar 2? | Telas 0 e 1; na aula, «Retomada · Pilar 6 e 6A» e um slide de previsão («com os custos abertos, a margem da Marina fica perto dos 40%, acima ou abaixo?») | 3 min | P6 cap. 05 (margem de referência); 6A; GUIA 5.2 (retomar, não repetir) |
| **2 · Compreender** | Entende os seis degraus, a rampa, o colchão, a escada e a régua | Aula (15 a 20 min); e-book (caps. 00 a 09) | 20 min de aula; 60 a 80 min de leitura | R1 a R34; F02; F03; ZAIOS |
| **3 · Observar** | Vê a Marina montar a conta dela na ficha e chegar a «Redesenhar» | Tutorial (roteiro 5.7); cap. 10 do e-book; Bloco 2 da aula | 4 a 5 min de vídeo | Exemplo ilustrativo (seção 7) |
| **4 · Executar** | Resolve os exercícios e preenche a ficha com os próprios números; usa o checklist para levar a conta ao contador | Cap. 12 do e-book; ficha; checklist | 15 a 20 min de exercícios; ficha com 30 a 45 min na primeira passada **[a confirmar por Bruno]** | R7, R10 a R13, R18 a R24 |
| **5 · Validar** | Lê o feedback em cinco partes, mexe nas alavancas uma por vez, escreve o veredito e o critério para parar | Resultado da ficha, simulador, selo «Pronto para levar à página 6» | 5 a 8 min | FABRICA 3.2; R32, R33 |
| **6 · Entregar** | Baixa a página 6B, salva na pasta Meu Dossiê ao lado das páginas 6 e 6A, refaz a página 6 com a margem aberta, preenche a Planilha 2 e leva a decisão ao Pilar 7 | PDF; quadros 6.7; próxima etapa | 2 min (mais refazer a página 6) | MAPA etapa 6; PL2; P7 («Dias 61 a 90 · Decidir: refaz a página 6 com os números cotados») |

---

## 5. Pacote da lição: especificação de cada peça

### 5.1 Identidade e voz comuns (GUIA 1.4 e 4; igual à 6A)
- Identidade da Trilha 1: Playfair Display (títulos, ênfase em itálico dourado) e Inter (texto, `font-variant-numeric: lining-nums`); paleta das fichas (`#16261C`, `#22382A`, `#F5F1E8`, `#EBE4D4`, `#E0BE5E`, `#7A5E12`, `#46564B`, `#D6CDB8`, `#FFFDF8`, ok `#1F5A33`/`#E1EFE3`, crítico `#9B2C1F`/`#F8E3DE`); aula com os tokens de `_motor/deck.css`. O construtor reaproveita `01-capex/src/estilo.py`, `build_ebook.py`, `build_checklist.py`, `render.js` e `build_capas.js` da 6A (já na identidade do curso).
- Voz: "você", "nós", "a Zion"; frases curtas; "cerca de" antes de número arredondado; toda conta fecha com «Conferência: … Bate.».
- **Rótulos fixos:**
  - números novos da Marina: «Exemplo ilustrativo · dados fictícios. Não são preços de referência.»;
  - a margem de 40% e os números da Zion Glamping Store só aparecem como **o ponto de partida da página 6 da Marina**, com «referência orientativa da página 6, não confirmada; a Zion também vende esse tipo de estrutura» (GUIA 2.1, regras 1 a 4). Nunca como referência a seguir, faixa ou meta;
  - a resposta do contador da Marina: «resposta fictícia do contador dela, para o caso dela; não vale para você»;
  - todo resultado: «Cenários, não promessas.»
- **Como falar da diferença com o Pilar 6, sem desmerecê-lo** (regra de redação, elaboração própria): o Pilar 6 fez a primeira conta, com uma margem de referência que ele mesmo chama de «simplificação, não promessa» (P6 cap. 05) e que «acerta a ordem de grandeza do ano e não mostra o mês que aperta» (ficha do Pilar 6, campo «margem»). A 6B é o passo que o próprio Pilar 6 pediu: «A margem real sai da sua lista de custos, com o seu trabalho e a reserva de reposição dentro.» Proibido: "a margem do Pilar 6 estava errada", "inflada", "otimista demais". Usar: "a página 6 respondeu com a margem de referência; agora a resposta vem da sua lista".
- **Frases-assinatura citadas com a origem** (mapa, seção 9; GUIA 1.4): «Faturamento não é lucro, e o custo fixo não diminui na baixa.» (Pilar 6, cap. 05) · «É simplificação, não promessa.» (Pilar 6, cap. 05) · «Ninguém abre na ocupação do destino.» (Pilar 6, cap. 06) · «Lucro e retorno são coisas diferentes.» (Pilar 6, cap. 07) · «Se o conservador não paga as contas, o empreendimento ainda não está pronto.» (Pilar 6, cap. 07) · «Primeiro prove a conta. Depois escolha como crescer.» (Pilar 6, cap. 08) · «Uma linha em branco vale mais do que um número inventado.» (Pilar 6) · «Receita bruta não é lucro» e «O número em que você confia é o do cenário mais fraco» (Pilar 4) · «Se o negócio não paga quem o opera, ele não é um negócio.» (Jornada do COMO, Etapa 09) · «Imposto sobre a receita é a omissão mais frequente e a mais cara.» (Jornada do COMO, Etapa 02, citada no F02) · «Quando a conta não fecha, a conta está certa» (Jornada do COMO, Etapa 02, citada no F02 e no F03) · «Receita é vaidade. Margem é sanidade. Caixa é realidade.» (Volume A05 · Investimento, cap. 09) · «Nenhuma das três decide sozinha.» (Volume A05, cap. 11) · «Projeto não quebra por prejuízo. Quebra por falta de caixa num mês específico» (Volume 05 · Investimento, cap. 08) · «Nada aqui substitui contador» (Volume 04 · Estratégia, cap. 13) · «Onde não souber, marque "Não sei": vira a sua tarefa da semana.» (Comece aqui) · «A Zion avalia cada caso.»
- **Não usar** (mapa 9.21, por desmerecer o Pilar 6, cujos cenários só mexem na ocupação): «Cenário que só mexe na ocupação não é estresse, é desconto.»
- **Aviso educativo** (e-book em «Como ler» e nas notas, checklist, ficha, aula): «Material educativo. Não é estudo de viabilidade, projeção nem promessa de retorno. Impostos se confirmam com o contador; contratos, com o advogado. A Zion avalia cada caso.» (mapa, seção 10, rodapé sugerido). Sem rodapé corrido no e-book (GUIA O1). Sem travessão no texto das peças.

### 5.2 E-book (PDF A4, molde do Pilar 6)
- **Capa:** verde `#16261C` com margem branca, sem logo e sem foto; sobretítulo «TRILHA 1 · PILAR 6 · APROFUNDAMENTO 6B · MÉTODO ZION»; título «Viabilidade: *a conta do seu projeto fecha?*» (ênfase `#E0BE5E`); deck: «Com as páginas 6 e 6A na mão, a conta aberta linha por linha, da receita bruta ao que sobra depois da reserva, o primeiro ano mês a mês e a régua para decidir. Ao fim deste e-book você está pronto para a página 6B do seu Dossiê, Viabilidade.»; numeral gigante «6B»; rodapé «Zion Hospitality Business · Transforme Seu Terreno em um Projeto de Hospedagem de Sucesso · Aprenda o passo a passo com o Método Zion».
- **Anatomia de cada capítulo** (GUIA I10): «CAPÍTULO NN · RÓTULO», título que afirma com ênfase em itálico, deck, régua dourada, numeral, tabela «Por que fazer isso / Como vamos fazer / Para que serve», «Neste capítulo», capitular, «Exemplo ilustrativo», «Pare e pense» com «Ver a resposta», «Aplicação · No seu caso» (as duas situações), «Faça agora», «Para levar».
- **Tamanho:** 50 a 60 páginas no tamanho de letra do Pilar 6 (a 6A saiu com 56) **[a confirmar por Bruno]**.

| Cap. | Título que afirma | Conteúdo | Fontes |
|---|---|---|---|
| — | Capa e sumário | como acima | P6 (molde) |
| 00 | Como usar este aprofundamento | «Este pilar em três respostas»; capitular: «Seja bem-vindo ao aprofundamento 6B. Você já fez a página 6 no Pilar 6 e abriu o custo de abrir a porta na 6A. Aqui a página 6 ganha mais uma irmã, a 6B, que abre a linha que faltava: quanto sobra.»; «Antes que você pense» («Já fiz a página 6, a conta não fechou?» · «Não tenho a resposta do contador.» · «E se a conta não fechar?» → «Quando a conta não fecha, a conta está certa»); «Duas situações, o mesmo método»; «Como ler» (rótulos e aviso educativo); «Revisite · Pilares 2, 4, 6 e 6A» (diária e curva do ano; receita bruta nos três cenários; margem de referência e tempo de volta; CAPEX e investimento total) | P6 cap. 00; P2; P4; 6A; MZ; CA |
| 01 | A página 6 da Marina é o ponto de partida | A conta do Pilar 6 da Marina, com o rótulo da referência: R$ 271.915,88 × 40% = R$ 108.766,35; o tempo de volta e o limite de cerca de R$ 870 mil; a 6A dela (CAPEX R$ 791.131, investimento total R$ 831.918,38, dentro do limite com folga de R$ 38.212,42); o que o Pilar 6 deixou escrito: «A margem real sai da sua lista de custos»; «Faça agora: escreva a margem da sua página 6 e de onde ela veio» | P6 caps. 05 e 07; ficha do P6; 6A |
| 02 | Seis degraus da receita ao que sobra | A cascata única (seção 6.2) em diagrama de escada; o nome de cada degrau e o que está dentro; a caixa **«Do Pilar 6 para a 6B»** (tabela abaixo); onde cada coisa não entra (parcela do empréstimo, imposto sobre o lucro, terreno: Pilar 7, contador, ao lado) | F02 caps. 1 a 5; mapa 1.3; P6 cap. 05 |
| 03 | Quanto entra: a receita se mede, não se deseja | Unidades × ocupação × diária × dias; diária média do ano (R2); ocupação pelos doze meses (R3, a média do Pilar 2 da Marina: 38,5%, e não 42%); «Ninguém abre na ocupação do destino» (R4, R5): a rampa no calendário, a partir do mês de abertura; outras receitas por captura × ticket, com custo próprio, fora da base (R6); taxa de limpeza fora da receita (ZAIOS 11) | P2; P4; P6 cap. 06; F02 cap. 2; A05 cap. 08; VOL05 cap. 7; ZAIOS |
| 04 | Do bruto ao real: o que sai antes de você ver o dinheiro | Imposto sobre a receita: linha própria, **em branco até o contador responder**, com data e nome (R7; compromisso de 7 dias do P6); a pergunta ao contador do VOL04 cap. 13 (R34); comissão por reserva × sobre a receita total (R8); taxa do cartão; cancelamento e não comparecimento (R9); «não conte a comissão duas vezes» (erro 5) | F02 caps. 2 e 4; VOL04 cap. 13; P6 cap. 05 |
| 05 | Quanto sai: o custo de cada noite e o custo de cada mês | Variáveis por noite, por estadia e em % da receita; perdas e quebras (F02, com o aviso de que a ZAIOS usa a mesma palavra para outra coisa); fixos com duodécimos (R12); a lista do que se esquece (erro 9); o seu trabalho é custo (R10; «Se o negócio não paga quem o opera…»); custos do modelo (aluguel, gestão, royalty) | F02 caps. 3 e 4; JC09; A05 cap. 9 |
| 06 | Quanto sobra: a margem que sai da sua lista | Reserva de reposição desde o primeiro ano, reserva **ou** depreciação (R11); a margem aberta; a régua de margem da ZAIOS (30/20/10) e por que ela não se compara com as outras (mapa 1.4, erro 20); ponto de equilíbrio lido com a folga (R13, mapa 1.7); custo por diária vendida e as três zonas (R14); diária de equilíbrio; piso por escrito (R15) | F02 caps. 4 e 5; JC09; JC08; ZAIOS |
| 07 | O primeiro ano e o caixa | O ano mês a mês: rampa × calendário; o mês que aperta; reserva de sazonalidade (R16); o menor saldo e o colchão (R19; ZAIOS passo 5); o giro pelas duas contas que o Pilar 6 ensina (R18) e por que o giro da 6A muda; fôlego (R17) | P6 cap. 06; F02 cap. 5; F03 cap. 2; VOL05 cap. 8; ZAIOS |
| 08 | Vale a pena? Lucro e retorno são coisas diferentes | Retorno simples sobre o que sobra, nunca sobre o resultado antes da reserva (R20); a escada do tempo de volta com o primeiro ano de rampa (R21); a mesma conta como o Pilar 6 faz (investimento total ÷ resultado) e por que as duas não se misturam (mapa 1.5); valor presente dos dez anos explicado sem fórmula, com a **taxa que você declara antes** (R22; a Zion não sugere taxa, ZAIOS 2); a venda do negócio sempre ao lado da conta sem ela (R23; ZAIOS 3); o terreno ao lado, com a razão escrita (R31) | F03 caps. 1 a 4; A05 caps. 10 e 11; ZAIOS; P6 cap. 07 |
| 09 | Onde a conta quebra | Os três cenários do curso com custo aberto (a margem muda de um para outro, porque o fixo não muda); o teste de queda da régua (diária −10%, ocupação −20%); a sensibilidade do Mapa (diária −15%, ocupação −10 pontos, CAPEX +20%); a hierarquia da dor (R26); "o que precisa ser verdade" com a conta aberta (R27) | P4; P6 cap. 07; F03 cap. 5; ZAIOS 5 e 12; MAPA; A05 cap. 12 |
| 10 | A conta da Marina, inteira | Exemplo resolvido (seção 7) com as conferências «Bate.», os cinco passos e o veredito «Redesenhar»; o critério que ela mesma escreveu na página 6 dispara | Exemplo ilustrativo; ficha do P6 (`criterioSug`) |
| 11 | Quando a conta não fecha: uma alavanca por vez | As alavancas (diária, ocupação, custo fixo, CAPEX, fase menor, outras receitas), cada uma sozinha (R32); "fase um paga fase dois"; o cenário ajustado da Marina e por que ele dá «Testar»; o que ela vai provar nos 90 dias do Pilar 7 | F03 cap. 6; P6 caps. 08 e 09; B09 (só como fonte do faseamento); P7 |
| 12 | Pratique com a Marina | Exercícios E2 a E5 com gabarito comentado (5.4) | Exemplo ilustrativo |
| 13 | A página 6B e a volta | Como preencher a ficha; **«Como levar para a página 6»**; **«Planilha 2, célula a célula»** (onde a Planilha 2 não tem linha e como contornar); o Pilar 7; perguntas ao contador e ao advogado | MAPA; PL2; P6; P7; mapa 7.2 |
| ✓ | Confira o que ficou | «Pare e pense» com «Ver a resposta»; «O 6B em dez linhas»; «Faça agora · A minha página 6B»; notas e fontes, com o aviso educativo | — |

- **Caixa «Do Pilar 6 para a 6B»** (cap. 02):

| Na página 6 | Na página 6B |
|---|---|
| Resultado = receita bruta × margem de referência de 40% (P6 cap. 05) | Resultado = a escada de seis degraus, com a sua lista |
| A mesma margem nos três cenários | Custo fixo igual nos três; a margem sobe com a ocupação |
| Giro = três meses de custo pela margem | Giro = a maior de duas contas do próprio Pilar 6 (cap. 06), com o custo aberto |
| Tempo de volta = investimento total ÷ resultado do conservador, sem rampa | Escada: o CAPEX no ano zero, o primeiro ano com rampa, o giro testado à parte no colchão (régua da Zion). A conta do Pilar 6 aparece ao lado |
| Régua 5 / 8 / 12 e vereditos avançar, testar, ajustar, pausar | Régua da Zion em cinco passos (8 e 12 anos, colchão de 10%, valor presente) e vereditos Avançar, Testar, Ajustar, Pausar ou Redesenhar (ZAIOS 7). O «ajustar» acima de 12 anos do Pilar 6 se chama aqui «Redesenhar» |
| "O que precisa ser verdade" com a margem fixa | A mesma pergunta com o custo aberto: cada real de diária a mais fica quase inteiro |

### 5.3 Aula interativa (molde `pilar6-aula/` + `_motor/`, igual à 6A)
- `docs/trilha1/apresentacao/pilar6b-aula/index.html`; título «Aprofundamento 6B · Viabilidade»; 36 a 40 slides; 15 a 20 min; até cerca de 40 palavras por slide; texto nas notas.
- `data-bloco`, na ordem: «Abertura», «Como funciona esta aula», «Retomada · Pilar 6 e 6A», «Bloco 1 · Os seis degraus da conta», «Bloco 2 · A conta da Marina», «Quiz relâmpago», «Resumo», «A sua página 6B», «Próximo». Nenhuma sigla interna na barra.
- **Sequência:**
  1. Capa com o selo «Método Zion · Etapa 4 · Fechar a conta».
  2. «O que você vai fazer aqui»: Assistir · Responder · Sair com a página 6B.
  3. «Você já fez a página 6 no Pilar 6 e a 6A. Aqui a página 6 ganha mais uma irmã, a 6B.»
  4. «Retomada · Pilar 6 e 6A» («Responda de cabeça. Errar aqui também ensina.»): que margem a página 6 da Marina usou e de onde ela veio? (40%, referência, simplificação); qual é o investimento total da 6A dela? (cerca de R$ 832 mil); até quanto a página 6 dizia que o investimento aguentava? (cerca de R$ 870 mil, em 8 anos no conservador).
  5. Previsão: «Com os custos abertos, a margem da Marina fica perto dos 40%, acima ou abaixo? E o limite de R$ 870 mil continua de pé?»
  6. Bloco 1: «Do Pilar 6 para a 6B»; os seis degraus, um slide cada, com a pergunta-chave e o erro típico; Quiz relâmpago 1 (classificar 6 itens no degrau); a rampa no calendário; o colchão; a escada; Quiz relâmpago 2 («o tempo de volta se calcula sobre o resultado antes ou depois da reserva?»).
  7. Bloco 2: a conta da Marina revelada clique a clique (receita → deduções → variáveis → fixos com a retirada → reserva → 21,3% → equilíbrio 25,4% com folga de 13 pontos → primeiro ano → colchão → escada 15 anos → cinco passos → Redesenhar); «O critério que ela escreveu na página 6 dispara»; semáforo das alavancas; o cenário ajustado e por que dá «Testar»; Quiz relâmpago 3 («qual é a ação de 30 dias?»).
  8. «O 6B em cinco frases».
  9. «A sua página 6B»: nome (sem e-mail, nada é enviado) e a ficha embutida **[a confirmar por Bruno, como na 6A]**.
  10. «Próximo · a página 6 refeita, a Planilha 2 e o Pilar 7», com «Lembre: salve o PDF da página 6B na pasta Meu Dossiê, ao lado das páginas 6 e 6A», «Esta ficha não envia nada: o PDF fica só com você.» e o aviso educativo.
- Simuladores do motor: escolha, marcar, calculadora (a escada com uma alavanca) e semáforo (os cinco passos). Selo «Exemplo ilustrativo · dados fictícios» em todo número da Marina.

### 5.4 Exercícios (dentro do e-book, cap. 12, com gabarito comentado)
- **E1 · Resolvido:** a conta da Marina (cap. 10).
- **E2 · Parcialmente resolvido (deduções):** a Marina passa a vender 80% das noites pela plataforma, com 15% de comissão (em vez de 60%). O resto fica igual. Pede-se:
  - a comissão sobre a receita total: 0,80 × 15% = **12%**; o cartão: 0,20 × 3% = **0,6%**; deduções: 6% + 12% + 0,6% + 2% = **20,6%**;
  - o que fica de cada noite: 645 × (1 − 0,206 − 0,01 − 0,03) − 97,50 = 645 × 0,754 − 97,50 = 486,33 − 97,50 = **R$ 388,83**;
  - o que sobra no ano: 421,575 × 388,83 − 112.627,20 = 163.921,01 − 112.627,20 = **R$ 51.293,81**;
  - a margem: 51.293,81 ÷ 271.915,88 = **18,9%** → faixa «risco» da régua (10% a 20%);
  - o equilíbrio: 112.627,20 ÷ 388,83 = **289,66 noites** = **26,5%**; folga **12,0 pontos**.
  - Conferência: 421,575 × 388 = 163.571,10; 421,575 × 0,83 = 349,91; soma 163.921,01. 51.293,81 + 112.627,20 = 163.921,01. Bate.
- **E3 · Classificação intercalada** (14 itens, com a explicação de cada erro): comissão da plataforma → degrau 2; imposto sobre a receita → degrau 2 (contador); cancelamento → degrau 2; lavanderia por estadia → degrau 3; perdas e quebras de material → degrau 3; salário da pessoa local → degrau 4; 13º e férias → degrau 4, em duodécimos; seguro anual → degrau 4, em duodécimos; as horas da Marina → degrau 4 (retirada); taxa de uma administradora → degrau 5; troca dos colchões daqui a seis anos → degrau 6 (reserva); depreciação somada à reserva → nunca as duas (R11); parcela do empréstimo da obra → fora desta conta, Pilar 7; taxa de limpeza cobrada à parte do hóspede → fora da receita de hospedagem (ZAIOS 11).
- **E4 · Uma alavanca e a escada:** com a diária de R$ 695 (R$ 50 a mais), pede-se:
  - o que fica de cada noite: 695 × 0,778 − 97,50 = **R$ 443,21**;
  - o que sobra no ano: 421,575 × 443,21 − 112.627,20 = **R$ 74.219,06**;
  - o primeiro ano: 0,549351 × 186.846,26 − 112.627,20 = **−R$ 9.983,09**;
  - o tempo de volta: 1 + (791.131 + 9.983,09) ÷ 74.219,06 = **11,79 anos** → passo 3 «ajustar»;
  - quanto valem os R$ 50 por ano: 50 × 421,575 × 0,778 = **R$ 16.399,27** (na margem de referência da página 6, R$ 8.431,50): por que a diferença? (com o custo aberto, só as deduções e a reserva crescem com a diária; o custo da noite e o fixo não).
- **E5 · Em branco:** escrever a sua lista de custos fixos em até 15 linhas, com os anuais em duodécimos e as suas horas na operação; escrever a pergunta ao contador (seção 5.6, item 4). É a ponte para a ficha.

### 5.5 Ficha «Faça agora · A sua conta» (gera a página 6B)
- **Caminhos:** lógica pura em `producao/trilha1-aprofundamento/02-viabilidade/src/logic.js` (sem DOM; testes em `tests/test_logic.js`, escritos antes da interface); interface em `docs/trilha1/pilar6b/index.html` + `logic.js`, no molde da `pilar6a/`; o caso da Marina num só arquivo de dados (`src/caso.py` → `EXEMPLO` de `logic.js` gerado ou conferido a partir dele), para que ficha, e-book, aula e tutorial usem os mesmos números.
- **Título e cabeçalhos:** «Faça agora · A sua conta»; tela «Zion · Método Zion / Pilar 6 / Aprofundamento 6B · Viabilidade»; PDF «Zion · Dossiê de Desenvolvimento · Página 6B · Viabilidade», nome e «Terreno em cidade/UF», rodapé educativo e "k/n".
- **Leituras do aparelho** (origem escrita ao lado; leitura tolerante; campo vazio se falhar): as chaves da seção 0. Sem a 6A, a pessoa digita o CAPEX e o giro, com o alerta B2.
- **Salvamento:** `zion-t1-pilar6b`, com `respostas` e `resumo.dados` (6.8).
- **Sem envio de dados.** Tela final e PDF: «Esta ficha não envia nada: o PDF fica só com você.» e «Salve o PDF da página 6B na pasta Meu Dossiê, ao lado das páginas 6 e 6A.» O montador do Pilar 7 não lê `zion-t1-pilar6b`: a volta é pelos quadros de transposição.
- **Telas:** 0 Abertura · 1 De onde você parte · 2 Quanto entra · 3 Do bruto ao real · 4 O custo de cada noite · 5 O custo de cada mês · 6 A reserva de reposição · 7 O primeiro ano e o caixa · 8 Vale a pena · Resultado · Alavancas · Veredito e critério · Ação de 30 dias · PDF.
- **Nunca insere valor de referência no lugar do "Não sei"** (igual à 6A). Onde a régua da Zion tem botão de referência (múltiplo de saída), ele só entra se a pessoa tocar no botão «Usar a referência da régua», e fica marcado como referência.
- Campo `turma` (`?turma=acompanhamento`): muda só o texto da próxima etapa (seção 8).

### 5.6 Checklist em PDF (1 a 2 páginas, A4)
«Checklist da página 6B · antes de mostrar a conta a alguém». Paleta e fontes do e-book; sobretítulo «TRILHA 1 · PILAR 6 · APROFUNDAMENTO 6B»; `Pilar-6B-Viabilidade-checklist.pdf`. Nenhum percentual e nenhum preço.
1. **Receita:** diária média do ano, não a de alta; ocupação pelos doze meses; rampa a partir do mês de abertura; outras receitas por captura × ticket, com custo; taxa de limpeza fora.
2. **Deduções:** imposto com a resposta do contador (data e nome); comissão separada da plataforma e do total; cartão; cancelamento; a comissão não está também nos variáveis.
3. **Custos:** variáveis por noite e por estadia; fixos com 13º, férias, encargos, seguro, taxas e licenças em duodécimos; manutenção preventiva; o seu trabalho com horas e valor-hora.
4. **Pergunte ao seu contador** (VOL04 cap. 13; R34): «Qual é o regime mais adequado para o meu caso e qual imposto incide sobre a receita de hospedagem e sobre as outras receitas, com que alíquota efetiva?»; «Em que ponto do crescimento (fase dois, fase três) essa resposta muda?»; «Quais encargos incidem sobre a minha retirada e sobre o salário da pessoa local?»; «Imposto sobre o lucro e distribuição ao sócio: como entram?». Anote a data e o nome de quem respondeu.
5. **Pergunte ao seu advogado**, se houver: contratos de gestão, arrendamento ou sociedade (degrau 5).
6. **Antes de decidir:** a reserva de reposição está na conta; o tempo de volta foi calculado sobre o que sobra; o colchão foi conferido; o terreno está ao lado, com a razão escrita; a taxa do seu dinheiro foi escrita antes de ver o resultado; o critério para parar está escrito.
7. **Depois da 6B:** refaça a página 6 com a margem aberta (digite a margem e os meses de giro do quadro); preencha a Planilha 2 pelo quadro célula a célula; leve a decisão ao Pilar 7.

### 5.7 Roteiro do tutorial da ficha (só o roteiro; sem gravar)
- Formato de `producao/clube/tutoriais-video/specs/ficha-pilar6.json` (`voice`: `pt-BR-FranciscaNeural`; cenas com `say` e `actions`: `card`, `goto`, `show`, `fillStart`, `click`, `wait`). Arquivos: `02-viabilidade/tutorial/ficha-pilar6b.json` e `ROTEIRO.md`; servidor local como no Pilar 6 (`http://localhost:8790/trilha1/pilar6b/`), com o `localStorage` semeado com as páginas 2, 6 e 6A da Marina. 16:9; **alvo de 4 min, teto de 5**. Entra logo depois do Faça agora. Selo «Exemplo ilustrativo · dados fictícios» em toda cena com número.

| # | Ação na tela | Narração (ideia; o roteirista escreve o texto final) |
|---|---|---|
| 1 | Card «Aprofundamento 6B · Viabilidade · A conta em seis degraus, o primeiro ano e a decisão» | O que você leva: a página 6B, irmã das páginas 6 e 6A |
| 2 | Abertura; situação «Tenho um terreno e ainda não hospedo ninguém» (veio do Marco Zero) | Esta ficha não envia nada |
| 3 | Tela 1: aparecem CAPEX R$ 791.131, giro R$ 40.787,38, a margem de 40% «referência da página 6» | De onde a Marina parte, e o que a página 6 pediu: a margem da sua lista |
| 4 | Tela 2: 3 cabanas, R$ 645, 38,5%, o calendário de 12 meses (alta jun a ago), abertura em junho | A receita se mede: a curva do Pilar 2 e a rampa |
| 5 | Tela 3: imposto «6%, contador, data»; 60% pela plataforma a 15%; cartão; cancelamento | A linha do imposto só se preenche com a resposta do contador. Sem ela, fica em branco |
| 6 | Telas 4 e 5: variáveis por estadia e por noite; os fixos; os anuais em duodécimos; 8 horas × R$ 40 | O custo de cada noite, o de cada mês, e o trabalho dela |
| 7 | Tela 6: reserva de 3%; resultado: R$ 57.819,79, margem de 21,3% | O que sobra, e por que não é 40% |
| 8 | Equilíbrio 25,4%, folga de 13 pontos | A operação se paga. Agora: e o investimento? |
| 9 | Tela 7: o primeiro ano mês a mês; menor saldo em março; giro de R$ 53.524,02; colchão de 3,9% | O mês que aperta e o caixa |
| 10 | Tela 8 e o painel dos cinco passos: escada de 15 anos → Redesenhar | A régua; o critério da página 6 dispara |
| 11 | Alavancas: diária +50 → 11,8 anos; ajustado → «Testar» | Uma alavanca por vez; o que precisa ser provado |
| 12 | Veredito escrito, critério, ação de 30 dias, PDF, quadros da página 6 e da Planilha 2 | Salvar na pasta Meu Dossiê; refazer a página 6; Planilha 2; Pilar 7 |

- Gravação só depois do "aprovado". Voz sintética como a do tutorial da 6A, aprovado por Bruno em 27/11.

### 5.8 Capas das aulas (ClickMax)
1280 × 720; Playfair + Inter; logo Zion no topo; ícone à direita; código de cor por tipo, igual à 6A: aula `#0F1A14`, Faça agora `#F5F1E8`, e-book `#5B3A29`, checklist `#EBE4D4`, tutorial `#22382A`, dourado `#E0BC64`. Sobretítulo «PILAR 6 · APROFUNDAMENTO 6B»; selos «COMECE POR AQUI», «FERRAMENTA · PDF», «VÍDEO · PASSO A PASSO», «PDF · LEITURA», «PDF · CHECKLIST». Arquivos `p6b-c-*.jpg`, gerados pelo `build_capas.js` da 6A.

### 5.9 Onde cada peça entra no ClickMax (para o publicador; nada é feito agora)
- **Trilha 1** (conteúdo `fa9a6c54`), módulo **Pilar 6** `6e06c29d`: cinco aulas novas, **`enabled=false`**, logo depois das cinco aulas da 6A (`8e98bed7`, `bccdfac4`, `b17d795c`, `f1918e33`, `758e9b1c`) e antes da Planilha 1.
- **Cópia Plataforma** (conteúdo `79d3e792`), módulo Pilar 6 `b2800aa7`: as mesmas cinco, **`enabled=false`**, depois das aulas da 6A (`62ec25cd`, `e0cc4ceb`, `a4047a7a`, `97c017e0`, `78611d74`) e antes da Planilha 1. Lembrete: essa cópia é entregue pela Mini Mentoria (R$ 47) e pelo Club; ligar só com o "aprovado".
- Nomes, na ordem: «Aprofundamento 6B · Viabilidade · Aula interativa» (link externo `pilar6b-aula/`) · «Aprofundamento 6B · Viabilidade · Faça agora · A sua conta» (link externo `pilar6b/`, comentários ligados) · «Aprofundamento 6B · Viabilidade · Tutorial da ficha» (vídeo, depois de gravado) · «Aprofundamento 6B · Viabilidade · E-book (PDF)» · «Aprofundamento 6B · Viabilidade · Checklist (PDF)». Capas `p6b-c-*.jpg`.
- As aulas atuais (Pilar 6 e 6A) ficam intocadas. Ligar só com o "aprovado" de Bruno.

---

## 6. Regras da ferramenta (testáveis)

Convenções:
- Dinheiro em reais, até 2 casas; contas internas sem arredondar; percentuais exibidos com 1 casa; comparações com faixas usam o valor sem arredondar e incluem as bordas na faixa melhor (≤ 8 passa; ≥ 10% passa).
- Divisão por zero devolve `null` com o motivo escrito.
- `hoje` entra como parâmetro.
- **"Não sei" é estado explícito, nunca zero escondido.**
- Ano de 365 noites por unidade; o mês tem 365 ÷ 12 noites por unidade, para que os doze meses somem o ano do Pilar 4 (**padrão assumido**; o F02 usa 30 dias e declara a diferença).
- Moeda constante: sem crescimento de receita nem de custo nos dez anos (R29: crescimento só com causa nomeada; F03 trabalha em moeda constante) **[a confirmar por Bruno]**.

### 6.1 Entradas

**Tela 0 · Abertura:** `nome` (2 a 60, do perfil salvo), `projeto` (2 a 60, obrigatório), `cidadeUF` (2 a 60), `situacao` (`terreno` / `ideia` / `opero`, textos do Marco Zero, pré-marcada), `paraOutro` (booleano), `contaAmpliacao` (booleano, só se `opero`), diagnóstico `d1` a `d4` («tenho lista de custos fixos: sim / em parte / não»; «o contador já respondeu o imposto: sim / não»; «o meu trabalho está na conta: sim / não / não trabalho na operação»; «tenho a curva do ano do Pilar 2: sim / não»), `turma`.

**Tela 1 · De onde você parte** (todos com «veio da página 6A / 6», editáveis)

| Campo | Unidade | Obrigatório | Faixa e "não sei" |
|---|---|---|---|
| `capex` | R$ | sim | > 0 e ≤ 100.000.000; de `capex_fase` |
| `giro6A` | R$ | sim | 0 a 100.000.000; de `giro` da 6A |
| `terreno` | R$ ou "não sei" | não | 0 a 100.000.000; de `terreno`; fica ao lado, nunca somado |
| `unidades` | inteiro | sim | 1 a 200; de `unidades` |
| `margem6` | % ou ausente | não | 0 a 90; de `margem` da página 6, com a origem («referência da Zion» se nota 1) |
| `limite6` | R$ ou ausente | não | de `inv8` da página 6 |

**Tela 2 · Quanto entra**

| Campo | Unidade | Obrigatório | Faixa e "não sei" |
|---|---|---|---|
| `diaria` | R$ por noite | sim ("não sei" bloqueia o selo) | 1 a 100.000; padrão: página 6, senão página 2 arredondada ao real |
| `diariaMedida` | R$ | não | de `diaria_media` da página 2 (só para o teste «premissa não provada») |
| `calendario[12]` | alta / médio / fraco, de janeiro a dezembro | sim | as contagens são conferidas com `meses_alta` e `meses_fraco` da página 2 (alerta B6 se diferirem) |
| `ocupAlta`, `ocupMedia`, `ocupFraco` | % | sim | 0 a 100; da página 2 |
| `ocupCons` | % | calculado | Σ ocupação dos 12 meses ÷ 12; confere com `ocup_ano` da página 2 (tolerância 0,1 ponto) e com `ocup_cons` da página 6 |
| `ocupBase`, `ocupOtim` | % | sim | `ocupCons` a 100; da página 6 (ou do Pilar 4) |
| `mesAbertura` | mês | sim | 1 a 12 |
| `estadiaMedia` | noites | sim | 1 a 30, aceita decimal; "não sei" bloqueia o selo |
| `extras[k]` (até 4) | nome; `captura` % das estadias (0 a 100); `ticket` R$; `custoDireto` R$ por venda | não | ticket > custo direto, senão alerta |

**Tela 3 · Do bruto ao real**

| Campo | Unidade | Obrigatório | Faixa e "não sei" |
|---|---|---|---|
| `imposto` | % da receita bruta, ou «em branco, aguardando o contador» | sim (um dos dois) | 0 a 40; o número só vale com `impostoQuem` (2 a 80 caracteres) e `impostoData` (data, não futura); sem os dois, a linha é tratada como em branco. `impostoRegime` texto opcional. **Nenhuma alíquota sugerida, nem faixa** |
| `pPlataforma` | % das noites vendidas por plataforma | sim | 0 a 100 |
| `comissaoPlataforma` | % por reserva | sim se `pPlataforma` > 0 | 0 a 50 |
| `cartaoDireto` | % nas vendas diretas | sim | 0 a 10 |
| `cancelamento` | % da receita de hospedagem | sim | 0 a 20; texto da faixa citada: «1% a 3%, faixa citada pela fonte» (F02, via JC02) |
| `comissaoNaoDuplicada` | confirmação | sim | «a comissão não está também nos custos de cada noite» |

**Tela 4 · O custo de cada noite** (1 a 10 linhas): `nome`; `base` = `porNoite` / `porEstadia` / `pctReceita` (sobre a receita de hospedagem); `valor` (R$ > 0 ou % 0 a 20); `origem` = `cotacao` / `estimativa` / `branco`. Linhas sugeridas só com o nome: lavanderia ou enxoval; amenidades e boas-vindas; energia, água e gás da noite; produtos de limpeza e reposição; perdas e quebras de material.

**Tela 5 · O custo de cada mês** (1 a 15 linhas): `nome`; `valor` com `periodo` = `mensal` ou `anual` (anual ÷ 12, o duodécimo, R12); `origem`; no modo ampliação, `jaExiste` (booleano). Linhas sugeridas só com o nome: pessoa local (salário e encargos); 13º e férias; folguista; energia das áreas comuns e bomba; internet e sistema de reservas; contador; seguro; imposto do imóvel, taxas e licença anual; manutenção preventiva e jardinagem; marketing e fotos; tarifas e outros. Confirmação `duodecimos` («os gastos anuais estão divididos por 12»).
- **Retirada** (R10): `horasSemana` (0 a 80) × `valorHora` (R$ 0 a 1.000) × 4,33; ou `naoTrabalho` («não trabalho na operação; quem opera está nos fixos ou no degrau 5»). Zero horas sem `naoTrabalho` dispara B8. O valor-hora não é sugerido: «quanto você pagaria a alguém para fazer o que você faz».
- **Custos do modelo** (degrau 5): `aluguelMes` R$; `gestaoPct` % da receita real; `royaltyPct` % da receita bruta. Todos 0 só se a pessoa marcar «não há».

**Tela 6 · A reserva de reposição:** `reservaRep` (% da receita bruta, > 0 e ≤ 20; "não sei" bloqueia o selo). Texto da faixa: «3% a 6% citados pelas fontes (A05: 3% a 5%; JC09: 3% a 6%; a régua da Zion usa 3%)». Aviso fixo: «reserva **ou** depreciação, nunca as duas» (R11).

**Tela 7 · O primeiro ano e o caixa:** calculada; a pessoa confirma o giro (`giro6B`), que só pode ser **maior ou igual** ao maior das três contas (6.2), com justificativa escrita se maior.

**Tela 8 · Vale a pena:** `taxa` (% ao ano, 0 a 30, ou "não sei"); `taxaAntes` («escrevi a taxa antes de ver o resultado», R22); texto: «A Zion não sugere taxa. A sua taxa é o quanto o seu dinheiro renderia em outro lugar, mais o que você pede pelo risco.» (ZAIOS 2); `multiploSaida` (0 a 15, vazio por padrão; botão «Usar a referência da régua: 6 vezes», marcado como referência, ZAIOS 3).

**Veredito e ação:** `vereditoPessoa` (Avançar, Testar, Ajustar, Pausar, Redesenhar); `criterioParar` (10 a 300 caracteres; molde do Pilar 6: «Se [o fato], eu não assino a obra: volto à conta e redesenho o tamanho, o produto ou a fase.»); `acao30` (10 a 300); `prazo` (hoje a hoje + 30); `verificacao` (10 caracteres ou mais); `pdfBaixado`.

### 6.2 Cálculo (cada cenário s ∈ {conservador, base, otimista} usa a sua ocupação; tudo o mais igual)
- `noitesAno = unidades × 365`; `N_s = noitesAno × ocup_s`; `estadias_s = N_s / estadiaMedia`.
- **Degrau 1 · Receita bruta:** `hosp_s = N_s × diaria`; `extras_s = Σ_k estadias_s × captura_k × ticket_k`; `bruta_s = hosp_s + extras_s`.
- **Degrau 2 · Receita real:** `imp_s = imposto × bruta_s` (0 se em branco, e o resultado leva o rótulo «antes do imposto sobre a receita»); `com_s = pPlataforma × comissaoPlataforma × hosp_s`; `cart_s = (1 − pPlataforma) × cartaoDireto × hosp_s`; `canc_s = cancelamento × hosp_s`; `deducoes_s` = soma; `real_s = bruta_s − deducoes_s`. A comissão, o cartão e o cancelamento incidem só sobre a hospedagem (as outras receitas são vendidas direto) **[padrão assumido]**.
- **Degrau 3 · Margem de contribuição:** `var_s = Σ porNoite × N_s + Σ porEstadia × estadias_s + Σ pctReceita × hosp_s + Σ_k custoDireto_k × estadias_s × captura_k`; `contrib_s = real_s − var_s`.
- **Degrau 4 · Resultado antes da reserva:** `retirada = horasSemana × valorHora × 4,33` (mês); `fixoMes = Σ mensais + Σ anuais / 12 + retirada`; `fixoAno = 12 × fixoMes`; `antes_s = contrib_s − fixoAno`.
- **Degrau 5 · Depois do modelo:** `modelo_s = 12 × aluguelMes + gestaoPct × real_s + royaltyPct × bruta_s`; `depoisModelo_s = antes_s − modelo_s` (é o resultado que a régua usa para o valor de saída).
- **Degrau 6 · O que sobra:** `reserva_s = reservaRep × bruta_s`; `sobra_s = depoisModelo_s − reserva_s`; `margem_s = sobra_s / bruta_s`.
- **Equilíbrio** (R13, lido com folga): `fixoEq = fixoAno + 12 × aluguelMes`; `X_s = sobra_s + fixoEq` (tudo o que varia com as noites); `cNoite = X_cons / N_cons`; `Neq = fixoEq / cNoite`; `ocupEq = Neq / noitesAno`; `folga = ocupCons − ocupEq` (pontos). Se `cNoite ≤ 0`: «cada noite vendida aumenta o prejuízo».
- **Custo por diária vendida** (R14): `(bruta_cons − sobra_cons) / N_cons`. **Diária de equilíbrio:** calcular `sobra_cons` com `diaria` e com `diaria + 1`; `efeito1 = diferença`; `diariaEq = diaria − sobra_cons / efeito1`. **Piso que ainda paga a noite:** a diária em que `cNoite` = 0, pelo mesmo método.
- **O ano mês a mês** (R4, R16): `o_m` = ocupação do tipo do mês m no calendário; `Σo = Σ o_m`. Rampa (ZAIOS 6: 40%, 50%, 75% da ocupação; lida nas janelas do P6 e do F02, meses 1 a 3, 4 a 6 e 7 a 12 **[padrão assumido]**): `rampa_i` = 0,40 (i = 1 a 3), 0,50 (4 a 6), 0,75 (7 a 12), 1 a partir do mês 13. Mês i do primeiro ano = mês do calendário `(mesAbertura + i − 2) mod 12 + 1`. Resultado do mês i: `X_s × o_m × rampa_i / Σo − fixoEq / 12`. Acumulado de 36 meses (ZAIOS 18). `ano1_s = X_s × Σ(o × rampa) / Σo − fixoEq`; `menorAcum` = menor acumulado dos 36 meses (cenário conservador).
- **Reserva de sazonalidade** (R16): `deficitVale` = soma dos meses negativos do ano em regime; `porMesAlta = deficitVale / meses de alta`.
- **Giro pelas duas contas do Pilar 6** (R18; P6 cap. 06; ficha do P6, campo giro): `giroA = 3 × (bruta_cons − sobra_cons) / 12` (três meses de custo do conservador); `giroB = |min(0, menorAcum)| + 3 × fixoEq / 12` (o buraco do primeiro ano com a rampa e os meses fracos, mais três meses de fixo); `giroMinimo = max(giro6A, giroA, giroB)`; `giro6B` ≥ `giroMinimo`. `investimento6B = capex + giro6B`.
- **Colchão** (R19; ZAIOS passo 5; leitura **elaboração própria**: caixa inicial = o giro, porque a reserva do imprevisto está dentro do CAPEX e é dada como toda usada): `colchao = giro6B + min(0, menorAcum)`; `colchaoPct = colchao / capex`.
- **Tempo de volta em escada** (R21; F03; ZAIOS): fluxo do ano 0 = −`capex` (sem giro, sem terreno); ano 1 = `ano1_s`; anos 2 em diante = `sobra_s`. Tempo de volta = (t − 1) + |acumulado(t − 1)| / fluxo(t), no primeiro t com acumulado ≥ 0. `sobra_s ≤ 0` → «não se paga». Acima de 100 anos → «mais de 100 anos». **Ao lado, a conta do Pilar 6:** `voltaP6 = investimento6B / sobra_cons`. **Com o terreno** (R31): a escada com `capex + terreno` no ano 0.
- **Retorno simples** (R20): `sobra_cons / capex`; com terreno, `sobra_cons / (capex + terreno)`.
- **Valor presente de dez anos** (R22, R23): `VP(i) = Σ_{t=1..10} fluxo_t / (1 + i)^t − capex`; com saída: `+ multiploSaida × depoisModelo_s / (1 + i)^10`. Sem taxa: se `Σ fluxos ≤ capex`, «negativo a qualquer taxa de zero para cima»; se `Σ fluxos + saída ≤ capex`, idem com a saída; senão, «pendente: escreva a sua taxa».
- **Teste de queda** (ZAIOS 12, passo 2): `sobraQueda` com `diaria × 0,90` e `ocupCons × 0,80` (outras receitas com a mesma captura).
- **Sensibilidade do Mapa** (mostrada, fora dos passos): escada do conservador com `diaria × 0,85`; com `ocupCons − 10 pontos`; com `capex × 1,20`.
- **O que precisa ser verdade** (R27), com o custo aberto, uma premissa por vez: o `X` mínimo para a escada caber em T anos é `x_T = (capex + T × fixoEq) / (T − 1 + r)`, com `r = Σ(o × rampa) / Σo`; daí a ocupação mínima (`x_T / cNoite / noitesAno`), a diária mínima (pelo efeito de R$ 1) e o CAPEX máximo (`(T − 1) × sobra_cons + ano1_cons`). Calcular para T = 8 e T = 12.
- **Régua da Zion em cinco passos** (ZAIOS 1.2, decisão 4), aplicada ao **cenário medido** (o conservador do curso; ver 11, padrão 3):
  1. `sobra_cons ≥ 0` passa; negativa, redesenhar.
  2. `sobraQueda ≥ 0` passa; déficit de até `3 × fixoMes` (com a retirada), ajustar; maior, redesenhar.
  3. Tempo de volta em escada ≤ 8 passa; ≤ 12 ajustar; acima ou «não se paga», redesenhar.
  4. VP sem saída ≥ 0 passa; negativo sem e positivo com saída, ajustar («o projeto depende da venda do ativo»); negativo nos dois, redesenhar; pendente se a taxa faltar e a soma simples não decidir.
  5. `colchaoPct ≥ 10%` passa; de 0 a 10%, ajustar; negativo, redesenhar.
  - **Veredito sugerido:** algum redesenhar → **Redesenhar**; senão algum ajustar → **Ajustar**; senão **Avançar**.
  - **Testar** substitui Avançar ou Ajustar (nunca Redesenhar) quando falta número ou a conta depende de premissa não provada (P6, `vereditoSugerido`): imposto em branco; passo 4 pendente; `diaria > 1,05 × diariaMedida`; `ocupCons` acima da ocupação medida no Pilar 2; `ocupCons > 65%`.
  - **Pausar** nunca é sugerido: é escolha da pessoa («o risco não cabe na sua vida», P6).
- **Alavancas** (R32; simulador; nunca grava por cima da conta): uma por vez, mostrando `sobra`, tempo de volta e passo 3: diária (± R$ 10 a R$ 300), ocupação (± 1 a 15 pontos), custo fixo (−5% a −30%), CAPEX (−5% a −30%), unidades da fase (com o CAPEX por unidade digitado), outras receitas (liga e desliga). O **cenário ajustado** é uma combinação salva à parte, com o rótulo «o que precisaria ser verdade», e passa pela mesma régua.

### 6.3 Faixas de leitura (com a fonte)
Todas como «faixa citada pela fonte; não é meta nem promessa».

| Leitura | Faixa | Fonte |
|---|---|---|
| Margem do que sobra (conservador) | ≥ 30% boa · 20% a 30% atenção · 10% a 20% risco · < 10% «o modelo não fecha» | ZAIOS 16 (30/20/10); JC02 via F02 (definição: depois de imposto, cancelamento, reserva e trabalho do dono) |
| Ponto de equilíbrio | folga < 0 crítico · 0 a 5 pontos fina · > 5 pontos com folga; equilíbrio > 70% «estrutural, não comercial» | F02 (ler com a folga); JC09 Passo 09 (70%); corte de 5 pontos **elaboração própria** |
| Tempo de volta (escada) | ≤ 8 · 8 a 12 · > 12 | ZAIOS 9 e F03; os textos do Pilar 6 (até 5 «muito bom, e raro em construção do zero»; 5 a 8 «bom»; 8 a 12 «aceitável quando há valorização relevante»; acima de 12 «só com uma razão escrita») acompanham como leitura |
| Colchão | ≥ 10% do CAPEX | ZAIOS 10; VOL05 cap. 8 |
| Reserva de reposição | < 3% abaixo das fontes | A05 cap. 9; JC09; ZAIOS 4 |
| Cancelamento | fora de 1% a 3%: «confira» | F02 via JC02 |
| Giro | `giro6A < giroMinimo`: «o giro da 6A não cobre a conta aberta» | P6 cap. 06 |
| Premissa não provada | diária > 1,05 × medida; ocupação > medida; > 65% | ficha do Pilar 6 (`vereditoSugerido`); régua do Pilar 2 |
| Outras receitas | a conta só passa no passo 1 ou 3 com elas | A05 («upside, não fundação»); F02 («a conta fecha com as diárias») |

### 6.4 Alertas (ordem = prioridade; a tela «Atenção» e o PDF mostram os três primeiros)

| Id | Condição | Mensagem (ideia) | Fonte |
|---|---|---|---|
| B1 | `imposto` em branco | «A linha do imposto está em branco. O resultado é antes do imposto sobre a receita, e a régua fica em Testar. Leve a conta ao contador.» | R7; P6 (compromisso de 7 dias) |
| B2 | sem a página 6A | «A 6B parte do CAPEX da 6A. Faça a 6A, ou digite o CAPEX e o giro com a origem.» (não bloqueia) | GUIA 5.1 |
| B3 | `sobra_cons < 0` | «No cenário medido, a operação não deixa nada depois da reserva.» | ZAIOS passo 1 |
| B4 | `folga < 0` ou `ocupEq > 70%` | «O equilíbrio está acima da ocupação medida» / «problema estrutural, não comercial» | R13; JC09 |
| B5 | `giro6A < giroMinimo` | «Com o custo aberto, três meses de custo passam a R$ X: o giro da 6A sobe» | P6 cap. 06 |
| B6 | contagens do calendário ≠ página 2, ou `ocupCons` ≠ `ocup_ano` | «O calendário não bate com o Pilar 2» | P2 |
| B7 | `colchaoPct < 10%` | «No pior mês do primeiro ano, sobra R$ X no banco: abaixo de 10% do CAPEX» | ZAIOS 10; VOL05 |
| B8 | retirada = 0 sem `naoTrabalho` | «Se o negócio não paga quem o opera, ele não é um negócio.» | JC09; R10 |
| B9 | `reservaRep < 3%` | «Reserva de reposição abaixo das fontes» | R11 |
| B10 | `comissaoNaoDuplicada` ou `duodecimos` falsos | bloqueia o selo | erros 5 e 8 do mapa |
| B11 | `limite6` presente e `investimento6B >` novo limite (8 × `sobra_cons`) | «O limite da página 6 foi feito com a margem de referência. Com a margem aberta, ele passa a R$ Y» | P6 cap. 07 |
| B12 | passo 4 «ajustar» por depender da saída | «Só a venda do negócio salva a conta: a decisão é ajustar, nunca avançar» | R23; ZAIOS 3 |
| B13 | passos 1 ou 3 só passam com outras receitas | «A conta depende das outras receitas» | R6 |
| B14 | `taxa` vazia e passo 4 pendente | «Escreva a sua taxa antes de ver o resultado» | R22 |
| B15 | tempo de volta com terreno > 12 | «Com o terreno, passa de 12 anos: escreva a razão (patrimônio, família, projeto de vida)» | R31; P6 |
| B16 | `situacao = opero` sem extrato | «Quem já opera usa o extrato de doze meses: dado real vence estimativa» | R30 |
| INFO | sempre | «Pergunte ao seu contador» e «Esta ficha não envia nada: o PDF fica só com você.» | mapa 7.2 |

### 6.5 Feedback em cinco partes e ação de 30 dias
1. **Resultado:** os seis degraus; a margem aberta ao lado da margem da página 6; equilíbrio e folga; o primeiro ano e o colchão; giro e investimento refeitos; tempo de volta (escada, Pilar 6, com terreno); três cenários; teste de queda; sensibilidade; o que precisa ser verdade.
2. **Significado:** os cinco passos em semáforo e o veredito sugerido, com o motivo em uma frase.
3. **Atenção:** os três primeiros alertas e o INFO.
4. **O que fazer:** a primeira situação verdadeira (ordem **elaboração própria**, a partir das prioridades das fontes):

| Ordem | Situação | Ação sugerida de 30 dias | Como verificar |
|---|---|---|---|
| 1 | B1 (imposto em branco) | Levar a conta ao contador com as perguntas do checklist | A alíquota anotada, com a data e o nome de quem respondeu (P6) |
| 2 | Redesenhar | Escrever três redesenhos, cada um mexendo uma alavanca, rodar a 6B para cada um e não assinar nenhum contrato de obra até um deles passar | As três versões da 6B salvas, com data |
| 3 | Testar por premissa não provada | Provar a premissa: teste de preço ou pesquisa de comparáveis para a diária; calendário dos comparáveis para a ocupação (Pilar 2) | A pesquisa anotada, com data e fonte |
| 4 | Ajustar pelo colchão | Recalcular o pedido de capital com o giro que dá 10% de colchão e levar ao Pilar 7 | O número escrito na página 7 |
| 5 | Ajustar pelo tempo de volta (8 a 12) | Escolher uma alavanca e escrever a razão, se ficar acima de 8 | A 6B refeita e a razão escrita |
| 6 | Linhas fixas sem cotação | Pedir proposta escrita das três maiores despesas fixas | As propostas, com data |
| 7 | Avançar | Refazer a página 6 e a Planilha 2 pelos quadros e seguir ao Pilar 7 | A página 6 refeita e a Planilha 2 preenchida |

5. **Como verificar:** o critério da linha escolhida ou o escrito pela pessoa.

### 6.6 Critério de conclusão (selo «Pronto para levar à página 6»)
1. CAPEX > 0 e unidades ≥ 1.
2. Diária, calendário completo (12 meses), ocupações, mês de abertura e estadia média informados.
3. Imposto respondido (com quem e data) **ou** marcado «em branco, aguardando o contador» **[a confirmar por Bruno: o selo sai com o imposto em branco, como a primeira versão honesta da 6A]**.
4. Deduções informadas; `comissaoNaoDuplicada` e `duodecimos` confirmados.
5. Toda linha de custo com origem; ao menos uma linha fixa.
6. Retirada informada ou `naoTrabalho`.
7. `reservaRep` > 0.
8. `giro6B` ≥ `giroMinimo`.
9. Passo 4 decidido ou `taxa` escrita.
10. `vereditoPessoa` e `criterioParar` escritos (R33).
11. `acao30`, `prazo` (até hoje + 30) e `verificacao` válidos.
12. `pdfBaixado`.

O selo **não exige** veredito Avançar. Enquanto falta algo, a tela lista o que falta, um item por linha.

### 6.7 Como levar para a página 6 e para a Planilha 2 (a volta)

**Página 6** (ficha `docs/trilha1/pilar6/`; nada é gravado nela):

| Campo da ficha do Pilar 6 | O que digitar | Nota |
|---|---|---|
| Margem operacional | `margem_cons × 100`, com 2 casas | «Lista de custos ou extrato» (nota 3) só se o imposto tiver a resposta do contador e nenhuma linha estiver em branco; senão «Referência ou estimativa» (nota 1) |
| Capital de giro (meses de custo) | `giro6B ÷ ((1 − margem digitada) × receita do conservador ÷ 12)`, com 2 casas | — |
| Diária, ocupações, unidades, linhas da folha, infraestrutura comum, terreno | não mudam (vêm dos Pilares 2 e 4 e da 6A) | — |

Aviso fixo: «A página 6 mantém a margem igual nos três cenários e calcula o tempo de volta sem rampa: é a simplificação dela. Os números da página 6 refeita e os da 6B ficam próximos, não iguais. Os dois estão certos dentro da regra de cada um.»

**Planilha 2 · Estudo de Massas e Viabilidade** (gerador `build.py`, `planilha_viabilidade`):

| Aba e célula | O que vai | Por quê |
|---|---|---|
| Massas B9, B10, B11 (unidades por tipologia), C e D (área coberta e deck) | as unidades da fase na tipologia certa; B12 tem de dar `unidades` | a aba Modelo de renda lê as unidades de Massas!B12 |
| Investimento B5 | `capex` | igual à 6A |
| Investimento B6 | 0 | terreno fora da conta |
| Investimento B7 | a fórmula `=giro6B/B8` (sem arredondar) | a Planilha 2 calcula o giro como meses × custo fixo; assim a B9 reproduz o giro da 6B |
| Modelo de renda B7:D7 | `diaria` nos três | a 6B usa a mesma diária nos três cenários |
| Modelo de renda B8, C8, D8 | `ocupCons`, `ocupBase`, `ocupOtim` | — |
| Modelo de renda B10:D10 | outras receitas ÷ receita de hospedagem, se houver; senão 0 | a Planilha 2 só aceita extras em % da diária e sem custo: o custo direto vai somado na B12 por noite |
| Modelo de renda B11:D11 | comissão + cartão + cancelamento, em % da hospedagem | a Planilha 2 tem uma linha só para o que sai da hospedagem além do imposto |
| Modelo de renda B12:D12 | variáveis por noite + (variáveis por estadia ÷ estadia média) + (perdas % × diária) + **reserva de reposição % × diária** | a Planilha 2 não tem linha de reserva: lançada por noite, ela sai certa nos três cenários, e a linha NOI passa a ser **o que sobra** (R20: o tempo de volta sobre o que sobra) |
| Modelo de renda B13:D13 | `imposto` (em branco → deixe vazio e anote) | — |
| Modelo de renda B14:D14 | `gestaoPct` (0 se você opera) | — |
| Modelo de renda B15:D15 | 0% | moeda constante, como a 6B |
| Modelo de renda B18 a B24 | os fixos agrupados nas sete linhas da planilha; a retirada e o aluguel do degrau 5 em B24 «Outros fixos» | a Planilha 2 não tem linha de retirada |
| Modelo de renda B50 | a sua taxa | a dica da planilha («10% a 15% é comum») é da planilha, não uma sugestão da Zion (ZAIOS 2) |
| Modelo de renda B65 | deixe 0 | o valor de saída da 6B já aparece ao lado, pela régua |

Aviso fixo: «A Planilha 2 põe o giro no ano zero e não tem rampa; a 6B põe o primeiro ano com rampa e testa o giro no colchão. Não misture as duas: compare cada uma com a régua dela.» (mapa 1.5 e 8.3).

### 6.8 `resumo.dados` salvos em `zion-t1-pilar6b`
`unidades`, `diaria`, `ocup_cons`, `ocup_base`, `ocup_otim`, `estadia_media`, `bruta`, `deducoes`, `real`, `variaveis`, `contribuicao`, `fixo_ano`, `retirada_mes`, `antes_reserva`, `modelo`, `reserva_rep`, `sobra`, `margem_pct` (os três cenários em listas), `imposto_pct` (ou `null`), `imposto_quem`, `imposto_data`, `ocup_eq`, `folga_pontos`, `custo_por_diaria`, `diaria_eq`, `ano1`, `menor_acum`, `giro_6a`, `giro_a`, `giro_b`, `giro_6b`, `investimento_6b`, `colchao`, `colchao_pct`, `volta_escada` (três cenários), `volta_p6`, `volta_com_terreno`, `retorno_simples`, `taxa`, `vp_sem_saida`, `vp_com_saida`, `passos` (1 a 5), `veredito_sugerido`, `veredito_pessoa`, `criterio_parar`, `margem_para_p6`, `giro_meses_para_p6`, `exemplo`.

### 6.9 Testes mínimos para o construtor
Pelo menos 60 testes em Node antes da interface:
- **o caso da Marina inteiro, campo a campo** (seção 7), inclusive os 12 meses, o colchão, a escada dos três cenários, os cinco passos, o veredito, as alavancas, o ajustado, E2 e E4 e os dois quadros de transposição;
- bordas: escada exatamente 8 (passa) e 8,0001 (ajustar); 12 e 12,0001; colchão exatamente 10% (passa), 0 (ajustar) e −0,01 (redesenhar); déficit do teste de queda exatamente 3 × `fixoMes` (ajustar) e um centavo acima (redesenhar); `sobra` = 0 (passa no passo 1; escada «não se paga»); diária = 1,05 × medida (sem Testar) e um centavo acima (Testar); imposto com número e sem `impostoData` (tratado como em branco); `cNoite ≤ 0`; folga exatamente 0; soma simples dos fluxos = CAPEX; taxa vazia com soma simples abaixo do CAPEX (passo 4 decidido); calendário com contagens diferentes da página 2; mês de abertura em dezembro (virada do ano); estadia média 1; outras receitas com ticket ≤ custo; modo ampliação; prazo em hoje + 30 e + 31;
- leitura tolerante de `zion-t1-pilar6a`, `zion-t1-pilar6` e `zion-t1-aula2` (com `resumo.dados`, com `dados` na raiz e com JSON quebrado);
- identidades: a soma dos 12 meses do ano em regime = `sobra_cons`; a Planilha 2 recalculada no LibreOffice com o quadro 6.7 dá a linha NOI do conservador = `sobra_cons` (tolerância R$ 0,01) e a ocupação de equilíbrio = `ocupEq`.
- Depois: ponta a ponta no iPhone 13 (Playwright), como na 6A, e o teste da aula (`data-bloco` sem sigla interna).

---

## 7. Exemplo didático · a Marina monta a conta dela (exemplo ilustrativo)

Rótulo em toda tela e página com número novo: **«Exemplo ilustrativo · dados fictícios. Não são preços de referência.»** Estes são os únicos números do caso: ficha, e-book, aula, tutorial e checklist usam exatamente estes valores (arquivo único, 5.5). As contas foram feitas sem arredondar; nas tabelas, diferenças de R$ 0,01 vêm do arredondamento dos centavos.

### 7.1 De onde ela parte
- **Fatos de continuidade** (GUIA 2.1, regra 4): 3 cabanas para casal, 38 m² + 16 m² de deck (P3), abre com 3 e desenha para 5 (P5), opera com uma pessoa local, terreno dela de R$ 600 mil (P1), primeira obra.
- **Pilar 2:** diária média R$ 645 (1.846 ÷ 2,86); alta no inverno, 3 meses a 64%; 4 meses médios a 40%; 5 meses fracos a 22%; média do ano (3 × 64 + 4 × 40 + 5 × 22) ÷ 12 = 462 ÷ 12 = **38,5%**.
- **Pilar 4:** 3 × 365 = 1.095 noites; × 38,5% = 421,575; × 645 = **R$ 271.915,88**; base 50% (R$ 353.137,50) e otimista 65% (R$ 459.078,75).
- **Pilar 6, ponto de partida** («referência orientativa da página 6, não confirmada; a Zion também vende esse tipo de estrutura»): margem de referência 40% → R$ 108.766,35 por ano; tempo de volta pouco mais de seis anos; limite de 8 anos: até cerca de R$ 870 mil. Critério escrito na página 6 (texto da ficha do Pilar 6): «Se o investimento total, com a infraestrutura comum e as cotações, passar de cerca de R$ 870 mil, ou se a lista de custos mostrar uma margem que leve o conservador acima de 8 anos, eu não assino a obra: volto à conta e redesenho o tamanho, o produto ou a fase.»
- **6A:** CAPEX da fase **R$ 791.131**; giro R$ 40.787,38 (da página 6); investimento total **R$ 831.918,38**; folga de R$ 38.212,42 até o limite.
- **Novo nesta lição (fictício):** calendário na ordem jun a ago alta; set e out médios; nov a mar fracos; abr e mai médios (o Pilar 2 deu só quantos meses de cada tipo); abertura em **junho**, o começo da alta (P6 cap. 06); estadia média de **2 noites**; "hoje" do exemplo: 28/11/2026.

### 7.2 As entradas dela (todas fictícias, salvo as de continuidade)

| Grupo | Linha | Valor | Origem |
|---|---|---|---|
| Deduções | Imposto sobre a receita | 6% da receita bruta | resposta fictícia do contador dela, com data (20/11/2026) e nome; não vale para você |
| | Plataforma | 60% das noites, comissão de 15% → 9% da hospedagem | estimativa dela |
| | Cartão nas vendas diretas | 40% × 3% → 1,2% | estimativa |
| | Cancelamento e não comparecimento | 2% | estimativa (dentro da faixa citada de 1% a 3%) |
| Por estadia | Lavanderia terceirizada do enxoval | R$ 70 | cotação (P5: lavanderia terceirizada) |
| | Amenidades e boas-vindas | R$ 45 | estimativa |
| Por noite | Energia, água e gás da noite | R$ 28 | estimativa |
| | Produtos de limpeza e reposição | R$ 12 | estimativa |
| % da receita | Perdas e quebras de material | 1% | estimativa |
| Fixos (por mês) | Pessoa local: salário e encargos | 3.600 | estimativa, a confirmar com o contador |
| | 13º e férias (duodécimo) | 600 | estimativa |
| | Folguista nas folgas da pessoa local | 400 | estimativa |
| | Energia das áreas comuns e bomba do poço | 500 | estimativa |
| | Internet e sistema de reservas | 350 | cotação |
| | Contador | 650 | cotação |
| | Seguro (R$ 3.600 no ano ÷ 12) | 300 | estimativa |
| | Imposto do imóvel, taxas e licença anual (duodécimos) | 150 | estimativa |
| | Manutenção preventiva e jardinagem | 800 | estimativa |
| | Marketing, fotos e anúncios | 450 | estimativa |
| | Tarifas bancárias e outros | 200 | estimativa |
| | **Subtotal dos fixos** | **8.000** | |
| | Retirada: 8 h por semana × R$ 40 × 4,33 | 1.385,60 | o valor-hora é o que ela pagaria a alguém (fictício) |
| | **Fixo do mês** | **9.385,60** → **112.627,20 no ano** | |
| Modelo | Aluguel, gestão, royalty | não há (ela opera) | |
| Reserva | Reserva de reposição | 3% da receita bruta | a régua da Zion usa 3% |
| Vale a pena | Taxa | a Marina não precisou: a soma simples já decide (7.7) | |

O que fica de cada noite vendida: 645 × (1 − 0,182 − 0,01 − 0,03) − (70 + 45) ÷ 2 − 28 − 12 = 645 × 0,778 − 57,50 − 40 = 501,81 − 97,50 = **R$ 404,31**.

### 7.3 A conta em seis degraus (os três cenários do curso)

| Degrau | Conservador 38,5% (o medido) | Base 50% | Otimista 65% |
|---|---|---|---|
| Noites vendidas | 421,575 | 547,5 | 711,75 |
| Estadias | 210,79 | 273,75 | 355,88 |
| **1 · Receita bruta** (só hospedagem) | **271.915,88** | **353.137,50** | **459.078,75** |
| Imposto 6% | 16.314,95 | 21.188,25 | 27.544,73 |
| Comissão 9% | 24.472,43 | 31.782,38 | 41.317,09 |
| Cartão 1,2% | 3.262,99 | 4.237,65 | 5.508,95 |
| Cancelamento 2% | 5.438,32 | 7.062,75 | 9.181,58 |
| Deduções (18,2%) | 49.488,69 | 64.271,03 | 83.552,33 |
| **2 · Receita real** | **222.427,19** | **288.866,48** | **375.526,42** |
| Lavanderia (R$ 70 × estadias) | 14.755,13 | 19.162,50 | 24.911,25 |
| Amenidades (R$ 45 × estadias) | 9.485,44 | 12.318,75 | 16.014,38 |
| Energia, água e gás (R$ 28 × noites) | 11.804,10 | 15.330,00 | 19.929,00 |
| Limpeza e reposição (R$ 12 × noites) | 5.058,90 | 6.570,00 | 8.541,00 |
| Perdas e quebras (1%) | 2.719,16 | 3.531,38 | 4.590,79 |
| Custos de cada noite | 43.822,72 | 56.912,63 | 73.986,41 |
| **3 · Margem de contribuição** | **178.604,46** | **231.953,85** | **301.540,01** |
| Fixos com a retirada | 112.627,20 | 112.627,20 | 112.627,20 |
| **4 · Resultado antes da reserva** (o "resultado operacional" do F02; EBITDA ou NOI na linguagem técnica) | **65.977,26** | **119.326,65** | **188.912,81** |
| 5 · Custos do modelo | 0 | 0 | 0 |
| Reserva de reposição (3%) | 8.157,48 | 10.594,13 | 13.772,36 |
| **6 · O que sobra** | **57.819,79** | **108.732,53** | **175.140,44** |
| **Margem (o que sobra ÷ receita bruta)** | **21,3%** (atenção) | 30,8% | 38,2% |
| Por mês, em média | 4.818,32 | 9.061,04 | 14.595,04 |

Conferência pelo caminho da noite: 421,575 × 404,31 = 170.446,99; − 112.627,20 = 57.819,79. Base: 547,5 × 404,31 = 221.359,73; − 112.627,20 = 108.732,53. Otimista: 711,75 × 404,31 = 287.767,64; − 112.627,20 = 175.140,44. Bate.

**De onde vem a diferença com a página 6** (para o cap. 10, sem adjetivo): na página 6, R$ 271.915,88 × 40% = R$ 108.766,35. Com a lista dela, sobram R$ 57.819,79 (21,3%). Os 18,7 pontos que faltam estão nas linhas que a margem de referência resumia: deduções 18,2%, custos de cada noite 16,1%, fixos com o trabalho dela 41,4%, reserva 3,0% (soma 78,7%; 100% − 78,7% = 21,3%). Conferência: 49.488,69 + 43.822,72 + 112.627,20 + 8.157,48 = 214.096,09; 271.915,88 − 214.096,09 = 57.819,79. Bate.

### 7.4 Equilíbrio, custo por diária e piso
- **Ponto de equilíbrio:** 112.627,20 ÷ 404,31 = **278,57 noites** = 278,57 ÷ 1.095 = **25,4%** de ocupação. **Folga: 38,5 − 25,4 = 13,1 pontos** (com folga). Conferência: 278,5665 × 404,31 = 112.627,20. Bate.
- **Custo por diária vendida:** 214.096,09 ÷ 421,575 = **R$ 507,85**.
- **Diária de equilíbrio** (com 38,5%): cada R$ 1 de diária vale 421,575 × 0,778 = R$ 327,99 por ano; 645 − 57.819,79 ÷ 327,99 = 645 − 176,29 = **R$ 468,71**. Conferência: 468,71 × 0,778 − 97,50 = 267,16; × 421,575 = 112.627,2. Bate.
- **Piso que ainda paga a noite:** 97,50 ÷ 0,778 = **R$ 125,32**. Leitura das três zonas (R14): acima de R$ 507,85 a noite paga tudo; entre R$ 125,32 e R$ 507,85 paga a noite e parte do fixo (melhor que vazio no mês fraco, nunca nas datas de pico, R15); abaixo de R$ 125,32 destrói valor.
- **Leitura para o e-book:** «A operação se paga com folga. A pergunta seguinte é outra: e o investimento?» (R1: lucro não é retorno.)

### 7.5 O ano mês a mês (cenário conservador)
Cada mês tem 1.095 ÷ 12 = 91,25 noites possíveis. Rampa: 40% nos meses 1 a 3, 50% nos meses 4 a 6, 75% nos meses 7 a 12.

| Mês do ano 1 | Mês | Tipo | Ocupação do mês × rampa | Noites | Contribuição (× 404,31) | Resultado do mês (− 9.385,60) | Acumulado |
|---|---|---|---|---|---|---|---|
| 1 | jun | alta | 64% × 0,40 = 25,6% | 23,36 | 9.444,68 | 59,08 | 59,08 |
| 2 | jul | alta | 25,6% | 23,36 | 9.444,68 | 59,08 | 118,16 |
| 3 | ago | alta | 25,6% | 23,36 | 9.444,68 | 59,08 | 177,24 |
| 4 | set | médio | 40% × 0,50 = 20% | 18,25 | 7.378,66 | −2.006,94 | −1.829,70 |
| 5 | out | médio | 20% | 18,25 | 7.378,66 | −2.006,94 | −3.836,64 |
| 6 | nov | fraco | 22% × 0,50 = 11% | 10,04 | 4.058,26 | −5.327,34 | −9.163,98 |
| 7 | dez | fraco | 22% × 0,75 = 16,5% | 15,06 | 6.087,39 | −3.298,21 | −12.462,19 |
| 8 | jan | fraco | 16,5% | 15,06 | 6.087,39 | −3.298,21 | −15.760,39 |
| 9 | fev | fraco | 16,5% | 15,06 | 6.087,39 | −3.298,21 | −19.058,60 |
| 10 | mar | fraco | 16,5% | 15,06 | 6.087,39 | −3.298,21 | **−22.356,81** (menor saldo) |
| 11 | abr | médio | 40% × 0,75 = 30% | 27,38 | 11.067,99 | 1.682,39 | −20.674,42 |
| 12 | mai | médio | 30% | 27,38 | 11.067,99 | 1.682,39 | **−18.992,04** |
| **Ano 1** | | | média 21,15% | **231,59** | **93.635,16** | **−18.992,04** | |

Conferência: Σ(ocupação × rampa) = 3 × 25,6 + 2 × 20 + 11 + 4 × 16,5 + 2 × 30 = 253,8 pontos; r = 253,8 ÷ 462 = 0,549351; 170.446,99 × 0,549351 = 93.635,16; − 112.627,20 = −18.992,04. Bate (as duas contas).

**Ano em regime** (do mês 13 em diante): mês de alta 58,4 noites → 23.611,70 − 9.385,60 = **+14.226,10**; mês médio 36,5 noites → **+5.371,72**; mês fraco 20,075 noites → **−1.269,08**. Ano: 3 × 14.226,10 + 4 × 5.371,72 − 5 × 1.269,08 = 42.678,31 + 21.486,86 − 6.345,38 = **57.819,79**. Bate. Do mês 13 ao 36 o acumulado não volta abaixo de −22.356,81 (nos fracos do segundo ano ele fica acima de R$ 28 mil positivos).

**Reserva de sazonalidade** (R16): 6.345,38 ÷ 3 meses de alta = **R$ 2.115,13** separados em cada mês de alta.

### 7.6 Giro, investimento e colchão
- Giro da 6A (três meses pela margem de referência): 40.787,38.
- Conta A do Pilar 6 (três meses de custo, agora aberto): 214.096,09 ÷ 12 × 3 = **53.524,02**.
- Conta B do Pilar 6 (buraco do primeiro ano + três meses de fixo): 22.356,81 + 3 × 9.385,60 = 22.356,81 + 28.156,80 = **50.513,61**.
- **Giro da 6B: R$ 53.524,02** (a maior). Investimento total refeito: 791.131 + 53.524,02 = **R$ 844.655,02** (na 6A, R$ 831.918,38; diferença de R$ 12.736,64, só do giro).
- **Colchão:** 53.524,02 − 22.356,81 = **R$ 31.167,21** = 31.167,21 ÷ 791.131 = **3,9%** do CAPEX → abaixo de 10% (B7). Giro que daria 10%: 79.113,10 + 22.356,81 = **R$ 101.469,91**.
- Fôlego no dia da abertura (R17): 53.524,02 ÷ 9.385,60 = 5,7 meses de fixo.

### 7.7 Vale a pena
- **Retorno simples:** 57.819,79 ÷ 791.131 = **7,3% ao ano**; com o terreno, 57.819,79 ÷ 1.391.131 = **4,2%**.
- **Tempo de volta em escada** (ano 0 −791.131; ano 1 −18.992,04; depois 57.819,79 por ano): acumulado depois do ano 1 = −810.123,04; 810.123,04 ÷ 57.819,79 = 14,01; **tempo de volta 15,0 anos**. Conferência: no fim do ano 15, −810.123,04 + 14 × 57.819,79 = −646,00; no ano 16 vira; 15 + 646,00 ÷ 57.819,79 = 15,01. Bate.
- **Como o Pilar 6 calcula** (investimento total ÷ o que sobra, sem rampa): 844.655,02 ÷ 57.819,79 = **14,6 anos**. As duas passam de 12.
- **Com o terreno** (escada): (791.131 + 600.000 + 18.992,04) ÷ 57.819,79 = 24,39 → **25,4 anos**.
- **Base e otimista em escada:** base, ano 1 = 221.359,73 × 0,549351 − 112.627,20 = +8.976,91 → 1 + (791.131 − 8.976,91) ÷ 108.732,53 = **8,2 anos**; otimista, ano 1 = 287.767,64 × 0,549351 − 112.627,20 = +45.458,14 → 1 + 745.672,86 ÷ 175.140,44 = **5,3 anos**. (Como o Pilar 6 calcula: 7,8 e 4,8 anos.)
- **Valor presente de dez anos:** soma simples dos fluxos = −18.992,04 + 9 × 57.819,79 = 501.386,06, menor que 791.131 → **negativo a qualquer taxa de zero para cima**. Com a venda do negócio no ano 10 pela referência da régua (6 × 65.977,26 = 395.863,59): soma simples 897.249,65; o valor presente fica negativo a partir de cerca de **1,6% ao ano** (a 1%: +38.816,74; a 2%: −22.319,65). A Marina não precisou escolher taxa: com qualquer taxa razoável para o dinheiro dela, o passo 4 dá redesenhar.

### 7.8 Onde quebra
- **Teste de queda** (diária R$ 580,50; ocupação 30,8%): cada noite deixa 580,50 × 0,778 − 97,50 = 354,13; 337,26 noites × 354,13 = 119.433,55; − 112.627,20 = **+6.806,35** → passa.
- **Sensibilidade do Mapa** (escada): diária −15% (R$ 548,25): sobra 26.087,21 → **32,7 anos**; ocupação −10 pontos (28,5%): sobra 13.547,84 → **62,6 anos**; CAPEX +20% (R$ 949.357,20): **17,7 anos**.
- **O que precisa ser verdade** (uma premissa por vez): para 8 anos, ocupação de **50,6%** (com R$ 645), ou diária de **R$ 808,72** (com 38,5%), ou CAPEX de até **R$ 385.746,48**; para sair do redesenhar (12 anos), ocupação de **41,9%**, ou diária de **R$ 690,96**, ou CAPEX de até **R$ 617.025,63**. Conferência (8 anos): x₈ = (791.131 + 8 × 112.627,20) ÷ (7 + 0,549351) = 1.692.148,60 ÷ 7,549351 = 224.144,92; ÷ 404,31 = 554,39 noites = 50,6%; 224.144,92 ÷ 421,575 = 531,68 por noite; (531,68 + 97,50) ÷ 0,778 = 808,72; CAPEX: 7 × 57.819,79 − 18.992,04 = 385.746,48. Bate.
- **O limite da página 6 também era premissa:** o "até cerca de R$ 870 mil" foi calculado com a margem de 40% (8 × 108.766,35). Com a margem aberta, 8 × 57.819,79 = **R$ 462.558,31** (conta do Pilar 6).

### 7.9 Os cinco passos e o veredito

| Passo | Conta | Resultado |
|---|---|---|
| 1 · O ano em regime, no medido | 57.819,79 ≥ 0 | passa |
| 2 · Teste de queda | +6.806,35 ≥ 0 | passa |
| 3 · Tempo de volta em escada | 15,0 anos > 12 | **redesenhar** |
| 4 · Valor presente | negativo sem saída a qualquer taxa; com saída, negativo acima de cerca de 1,6% ao ano | **redesenhar** |
| 5 · Colchão | 3,9% do CAPEX | ajustar |
| **Veredito sugerido** | | **Redesenhar** |

- O critério que ela escreveu na página 6 dispara: «se a lista de custos mostrar uma margem que leve o conservador acima de 8 anos, eu não assino a obra».
- Veredito escrito pela Marina: **Redesenhar**. Critério para parar: «Se nenhum redesenho passar de 12 para 8 anos com premissas provadas, eu não assino a obra.»
- **Ação de 30 dias** (ordem 2): «Rodar a 6B com três redesenhos, uma alavanca por vez, e não assinar contrato de obra.» Prazo: **28/12/2026**. Verificação: «as três versões da 6B salvas, com data».
- Alertas que disparam, na ordem de prioridade: **B5** (giro da 6A), **B7** (colchão), **B11** (limite da página 6 com a margem aberta) (os três que aparecem na tela e no PDF) e B15 (com o terreno, 25,4 anos; a razão escrita da Marina no Dossiê precisa ser revista). Não disparam: B1 (o contador respondeu), B2, B3, B4, B6, B8, B9, B10, B12 (o passo 4 é negativo também com a saída), B13, B14, B16.

### 7.10 As alavancas, uma por vez (cap. 11)

| Alavanca | O que muda | O que sobra no ano | Ano 1 | Tempo de volta | Passo 3 |
|---|---|---|---|---|---|
| Nenhuma (a conta dela) | — | 57.819,79 | −18.992,04 | 15,0 | redesenhar |
| Diária + R$ 50 | R$ 695 | 74.219,06 | −9.983,09 | 11,8 | ajustar |
| Diária da hipótese do Pilar 3 | cerca de R$ 716 (P3, hipótese, a provar) | 81.106,75 | −6.199,33 | 10,8 | ajustar |
| Ocupação + 5 pontos | 43,5% | 79.955,76 | −6.831,63 | 11,0 | ajustar |
| Custo fixo − 10% | R$ 8.447,04 por mês | 69.082,51 | −7.729,32 | 12,6 | redesenhar |
| CAPEX − 10% | R$ 712.017,90 | 57.819,79 | −18.992,04 | 13,6 | redesenhar |
| Outras receitas: cesta de café | 60% das estadias × R$ 140, custo R$ 70 (deixa R$ 57,40 por cesta) | 65.079,31 | −15.004,01 | 13,4 | redesenhar |
| Fase menor: 2 cabanas | CAPEX R$ 622.150 (sai uma cabana com as linhas dela); fixos iguais | 1.004,13 | −50.203,76 | mais de 100 anos | redesenhar |

Leituras para o e-book: a diária é a alavanca que mais pesa (R26, hierarquia da dor), porque cada real fica quase inteiro (77,8%); custo e CAPEX ajudam pouco sozinhos; as outras receitas não sustentam a conta (R6); a fase menor piora, porque o custo fixo não cai junto (elaboração própria a partir de R32 e do PL2, «a infraestrutura dilui com mais unidades»).

Conferências: diária R$ 695: 421,575 × 443,21 = 186.846,26; − 112.627,20 = 74.219,06; 1 + (791.131 + 9.983,09) ÷ 74.219,06 = 11,79. Ocupação 43,5%: 476,325 × 404,31 = 192.582,96; − 112.627,20 = 79.955,76; 1 + 797.962,63 ÷ 79.955,76 = 10,98. Fixo −10%: 170.446,99 − 101.364,48 = 69.082,51; 1 + 798.860,32 ÷ 69.082,51 = 12,56. CAPEX −10%: 1 + 731.009,94 ÷ 57.819,79 = 13,64. Cesta: 126,47 cestas × 57,40 = 7.259,52; 57.819,79 + 7.259,52 = 65.079,31; 1 + 806.135,01 ÷ 65.079,31 = 13,39. Duas cabanas: 730 × 0,385 = 281,05 noites × 404,31 = 113.631,33; − 112.627,20 = 1.004,13; CAPEX (687.940 − 146.940) × 1,15 = 622.150, em que 146.940 = cabana 106.400 + deck 11.200 + luz 1.800 + água 1.600 + unidade-modelo 23.200 + enxoval 2.340 + utensílios 400 (tabela da 6A). Bate.

### 7.11 O cenário ajustado (fictício, «o que precisaria ser verdade»)
Três alavancas que o curso já anunciou, todas **a provar**: a diária de cerca de **R$ 716** (hipótese do produto, P3; «fica como folga, não como condição», ficha do P6); **42%** de ocupação com um pacote de domingo a quinta para quem trabalha (a semana está em 26% no Pilar 2 e a internet para esse hóspede já está na lista da 6A); a **cesta de café** (60% das estadias, R$ 140, custo R$ 70). CAPEX e custos fixos iguais.

| Linha | Valor |
|---|---|
| Noites (1.095 × 42%) / estadias | 459,9 / 229,95 |
| Receita de hospedagem (459,9 × 716) | 329.288,40 |
| Cestas (137,97 × 140) | 19.315,80 |
| Receita bruta | 348.604,20 |
| Deduções da hospedagem (18,2%) | 59.930,49 |
| Imposto das cestas (6%) | 1.158,95 |
| Custos de cada noite (estadias × 115 + noites × 40 + 1% da hospedagem) | 48.133,13 |
| Custo das cestas (137,97 × 70) | 9.657,90 |
| Fixos com a retirada | 112.627,20 |
| Resultado antes da reserva | 117.096,53 |
| Reserva de reposição (3% de 348.604,20) | 10.458,13 |
| **O que sobra** | **106.638,40** (margem 30,6%) |
| Ano 1 com a rampa | +7.826,50 |
| Menor saldo do primeiro ano (março) | −1.878,35 |
| Tempo de volta em escada | 1 + (791.131 − 7.826,50) ÷ 106.638,40 = **8,3 anos** |
| Giro (conta A: 241.965,80 ÷ 4) / colchão | 60.491,45 / 58.613,10 = **7,4%** do CAPEX |
| Teste de queda (R$ 644,40; 33,6%) | +42.290,37 |
| Valor presente sem saída / com saída (6 × 117.096,53) | a 8%: −167.071,13 / +158.358,97 · a 10%: −225.713,19 / +45.161,50 · a 12%: −276.825,15 / −50.613,40 |

Passos: 1 passa; 2 passa; 3 **ajustar** (8,3); 4 **ajustar** até cerca de 10,9% ao ano (positivo só com a saída), redesenhar acima; 5 **ajustar** (7,4%; com giro de R$ 80.991,45 passaria). Pela régua: **Ajustar**. Como a conta depende de diária acima de 1,05 × 645 = R$ 677,25 e de ocupação acima da medida, a ficha mostra **«Testar»**: «a conta chega a Ajustar só com premissas que ainda não foram provadas». O e-book liga isso ao Pilar 7: os 90 dias servem para provar preço e semana antes de decidir de novo («Dias 61 a 90 · Decidir: refaz a página 6 com os números cotados»). Os valores presentes do ajustado são mostrados nas três taxas só para ensinar que a taxa muda a decisão (ZAIOS, achado principal); a ficha calcula com a taxa da pessoa.

Conferência do ajustado pela cascata completa: 348.604,20 − 59.930,49 − 1.158,95 − 3.292,88 − 26.444,25 − 18.396,00 − 9.657,90 − 10.458,13 − 112.627,20 = 106.638,40; pela noite: 459,9 × 459,548 + 137,97 × 57,40 − 112.627,20 = 211.346,13 + 7.919,48 − 112.627,20 = 106.638,41 (diferença de arredondamento). Bate.

### 7.12 Os quadros de volta, com os números dela

**Página 6 refeita:** «Margem operacional» = **21,26**, nota 3 (o imposto tem a resposta do contador e nenhuma linha está em branco); «Capital de giro» = 3 meses (53.524,02 ÷ (0,7874 × 271.915,88 ÷ 12) = 3,00). A ficha do Pilar 6 vai mostrar (contas dela, com 21,26%, conferidas aqui; para o roteirista): resultado do conservador **R$ 57.809,32**; giro **R$ 53.526,64**; investimento total **R$ 844.657,64**; tempo de volta **14,6 anos**; limite de 8 anos **R$ 462.474,52** (passou em R$ 382.183,12); base e otimista 11,3 e 8,7 anos (a margem fica igual nos três); veredito sugerido pela página 6: **«Ajustar»** (acima de 12 no conservador, abaixo de 12 no otimista). Na 6B o nome é «Redesenhar»: as duas dizem «não assine a obra neste desenho». Diferenças de alguns reais vêm da margem com duas casas.

**Planilha 2:** Massas B11 = 3, C11 = 38, D11 = 16 (B9 e B10 em zero); Investimento B5 = 791.131, B6 = 0, B7 = `=53524,02/B8`; Modelo de renda B7:D7 = 645; B8 = 38,5%, C8 = 50%, D8 = 65%; B10:D10 = 0; B11:D11 = 12,2% (9 + 1,2 + 2); B12:D12 = 123,30 (57,50 + 40 + 6,45 de perdas + 19,35 de reserva); B13:D13 = 6%; B14:D14 = 0; B15:D15 = 0; B18 = 4.600 (pessoa local, 13º e férias, folguista); B19 = 500; B20 = 350; B21 = 800; B22 = 450; B23 = 1.100 (contador, seguro, taxas); B24 = 1.585,60 (tarifas + retirada); C25 = 9.385,60. Resultado esperado: NOI B41/C41/D41 = **57.819,79 / 108.732,53 / 175.140,44**; margem B43 = 21,3%; ocupação de equilíbrio B44 = 25,4%; investimento B45 = 844.655,02; payback B47 = 14,6 anos (sem rampa, giro no ano zero); TIR negativa; VPL negativo com qualquer taxa digitada na B50. Conferência: 645 × (1 − 0,122 − 0,06) − 123,30 = 404,31. Bate.

### 7.13 Nexo com a sequência (para o roteirista)
- **De onde vem:** do Pilar 6, que deixou escrito «A margem real sai da sua lista de custos, com o seu trabalho e a reserva de reposição dentro», e da 6A.
- **O que muda na história:** na 6A, a Marina ficou dentro do limite de R$ 870 mil. A 6B mostra que esse limite foi feito com a margem de referência. Com a lista dela, a operação se paga com folga (equilíbrio 25,4%), mas o investimento não volta em 12 anos. O e-book diz isso sem drama: «Quando a conta não fecha, a conta está certa.»
- **Pilar 7:** no Pilar 7 você vê a Marina decidir «avançar» com a página 6 de referência, porque ele foi escrito antes da conta aberta. Aviso no cap. 13 e no slide «Próximo» (ideia): «No Pilar 7, a Marina decide com a página 6 de referência. Com a 6B, o critério que ela mesma escreveu dispara: antes de pedir dinheiro a alguém, ela redesenha e prova preço e semana.»

---

## 8. Versão autônoma e versão do acompanhamento Zion 360°

| Camada | Autônomo (Trilha 1) | Acompanhamento Zion 360° |
|---|---|---|
| Conteúdo e ferramentas | As cinco peças | Idênticas |
| Ritmo | Liberado com o Pilar 6, depois da 6A e antes da Planilha 1; primeira versão em uma semana; 30 dias para a resposta do contador e as propostas das maiores despesas fixas | Na semana do Pilar 6 do calendário da turma; a 6B é levada ao encontro do Pilar 6 junto com a 6A |
| Modelagem | Tutorial e exemplo da Marina | E mais: a equipe Zion preenche ao vivo um caso real anonimizado |
| Marcos | Selo e PDF | Dois marcos comentados pela equipe Zion: a primeira versão (todas as linhas com origem, imposto pode estar em branco) e a versão com o contador (antes de refazer a página 6) |
| Comentário da equipe | Feedback automático; comentários da aula lidos como insumo de melhoria | Comentário escrito nos dois marcos, sobre coerência, premissas e riscos, sem dar alíquota nem taxa |
| Rubrica (FABRICA seção 7, adaptada) | Autoavaliação de 4 perguntas: os seis degraus completos? o meu trabalho e a reserva estão dentro? o primeiro ano foi feito mês a mês? veredito e critério escritos? | **Coerência 40** (seis degraus fecham, giro e colchão certos, transposições conferem); **Justificativa 30** (origem de cada número, contador com data, premissas da receita ligadas ao Pilar 2); **Riscos 20** (três cenários, teste de queda, sensibilidade, o que precisa ser verdade, terreno ao lado); **Clareza 10** (a página lida por um terceiro sem explicação) |
| Conclusão | Selo e PDF | Selo, PDF e revisão da equipe no segundo marco |
| Na ficha (`turma`) | «Salve o PDF na pasta Meu Dossiê, refaça a página 6 com a margem aberta, preencha a Planilha 2 e siga ao Pilar 7» | «Leve as páginas 6A e 6B ao encontro do Pilar 6 e refaça a página 6 depois do comentário da equipe» |
| O que não se promete | Retorno, renda, ocupação, aprovação | Idem; nem parecer contábil, crédito, parceria ou investidor |

---

## 9. Próxima etapa (ficha, e-book e aula)
1. **Salvar** o PDF da página 6B na pasta Meu Dossiê, ao lado das páginas 6 e 6A.
2. **Refazer a página 6** com o quadro 6.7 (margem e meses de giro).
3. **Planilha 1** (opcional, se ainda não fez pela 6A) e **Planilha 2** pelo quadro célula a célula.
4. **Pilar 7:** levar o veredito, o critério para parar e, se for Avançar ou Ajustar, o investimento refeito (CAPEX + giro da 6B) para o pedido. Se for Redesenhar ou Testar: os 90 dias do Pilar 7 servem para provar a premissa e refazer as páginas 6, 6A e 6B.
- **Fora do próximo passo** (GUIA 5.10): B08, B09, Ferramenta 01 · Diária Mínima e Ferramenta 10 · Fechamento Mensal (produtos avulsos ou bônus fora da turma) não aparecem nas peças. Ficam só como fonte neste plano.

---

## 10. Arquivos que a produção vai criar
`producao/trilha1-aprofundamento/02-viabilidade/`: `PLANO.md`; `src/caso.py`, `src/logic.js`, `tests/test_logic.js`, `tests/test_planilha2.py` (recalcula a Planilha 2 da Marina no LibreOffice e compara com a 6B), `tests/test_e2e.js`, `tests/test_aula.js`; `src/build_ebook.py`, `src/build_checklist.py`, `src/render.js`, `src/build_capas.js` (a partir da 6A); `tutorial/ficha-pilar6b.json` e `ROTEIRO.md`; `ROTEIRO_APRESENTACAO.md`; `RELATORIO.md`.
Publicação: `docs/trilha1/pilar6b/index.html` e `logic.js`; `docs/trilha1/apresentacao/pilar6b-aula/index.html`; `docs/trilha1/materiais/Pilar-6B-Viabilidade-ebook.pdf` e `Pilar-6B-Viabilidade-checklist.pdf`; `docs/trilha1/capas/p6b-c-*.jpg`; `docs/trilha1/videos/tutoriais/tutorial-ficha-pilar6b.mp4` (depois de gravado).

---

## 11. Lacunas de fonte e padrões assumidos

**Lacunas (declaradas, não preenchidas):**
1. **Alíquota do imposto sobre a receita:** só o contador. A ficha não sugere número nem faixa; a faixa de 6% a 16% citada via F02 fica fora das peças. Os 6% da Marina são resposta fictícia do contador dela.
2. **Faixas de custo fixo e variável por porte** (1 a 6 unidades): nenhuma fonte com base. Todos os custos da Marina são fictícios.
3. **Valor-hora do trabalho do dono:** os R$ 40 são ilustrativos (F02; ZAIOS 5 pede confirmação); a ficha não sugere.
4. **Taxa de desconto:** nenhuma fonte Zion dá número; a Zion não sugere (ZAIOS 2). Falta texto simples sobre "o custo do seu dinheiro mais o prêmio pelo risco": escrito como elaboração própria, sem número.
5. **Inflação:** a lição trabalha em moeda constante (F03); a Planilha 2 cresce a receita e usa taxa nominal. O e-book explica a diferença em uma caixa, sem número.
6. **Financiamento, parcelas e imposto sobre o lucro:** fora (Pilar 7 e contador).
7. **Estadia média, ordem dos meses do calendário e mês de abertura da Marina:** o Pilar 2 não traz; fictícios.
8. **Múltiplo de saída 6×:** botão de referência da régua (ZAIOS 3), sem origem estatística nas fontes; aparece só ao lado da conta sem ele e nunca como valor do negócio.
9. **Rampa:** a ZAIOS dá 40%, 50% e 75% sem dizer as janelas; a leitura nas janelas 1 a 3, 4 a 6 e 7 a 12 meses vem do P6 e do F02 (via JC02).
10. **"Quebra":** o F02 usa para perda de material (variável, 1%) e a ZAIOS para inadimplência, cancelamento e estorno (1%). A lição chama de «perdas e quebras de material» e põe o cancelamento nas deduções.
11. **Imóvel comprado pronto ou apartamento:** as fontes de viabilidade são de construção do zero; a ficha aceita, sem lista própria.
12. **A ZAIOS registra o "caso P6" com R$ 108.846,84** (não R$ 108.766,35): só a diferença é registrada; a lição usa o número do e-book do Pilar 6.

**Padrões assumidos (elaboração própria, rotulada):**
1. Os seis degraus do F02 com nomes de tela próprios («resultado antes da reserva», «o que sobra») para não colidir com o «resultado operacional» do Pilar 6, que equivale ao que sobra.
2. Três cenários do curso (P4/P6: 38,5%, 50%, 65%, mesma diária) com custo aberto, em vez dos cenários percentuais da ZAIOS; os percentuais da ZAIOS entram como teste de queda (passo 2).
3. A régua da ZAIOS aplicada ao **cenário medido** (o conservador do curso), que faz na Trilha o papel do "base" da ZAIOS (o número calculado a partir da medida), seguindo «O número em que você confia é o do cenário mais fraco» (Pilar 4).
4. Tempo de volta em escada sem o giro no ano zero (F03/ZAIOS), com a conta do Pilar 6 ao lado.
5. Giro = a maior de três contas (6A, conta A e conta B do Pilar 6), em vez dos 6 meses de fixo da ZAIOS 15 (elaboração da ZAIOS).
6. Colchão = giro + menor acumulado de 36 meses, com a reserva do imprevisto dada como toda usada.
7. Comissão, cartão e cancelamento só sobre a hospedagem; reserva de reposição sobre a receita bruta inteira.
8. Mês de 365 ÷ 12 noites por unidade; moeda constante.
9. «Testar» por premissa não provada (regra do Pilar 6) sobreposto à régua da ZAIOS; «Pausar» só por escolha.
10. Corte de 5 pontos na folga do equilíbrio; ordem das ações de 30 dias; validações de faixa.
11. Os mapeamentos para a página 6 e para a Planilha 2 (reserva na B12, comissão + cartão + cancelamento na B11, retirada na B24, giro pela fórmula na B7).
12. Todos os números novos do caso da Marina (seção 7).

---

## 12. A confirmar por Bruno
1. **A tensão central: a margem de referência de 40% do Pilar 6 × a conta aberta.** Com custos fictícios mas coerentes com as fontes, a margem da Marina cai para 21,3%, o tempo de volta passa de pouco mais de seis anos para cerca de 15, o limite de "cerca de R$ 870 mil" cai para cerca de R$ 463 mil e o veredito passa de «avançar» (Pilar 6 e Pilar 7) para «Redesenhar». O mapa já registrava que nenhuma fonte justifica os 40% com uma lista de custos. A lição trata os 40% como «simplificação, não promessa» do próprio Pilar 6, sem desmerecê-lo. Bruno decide: (a) aceitar a 6B assim; (b) revisar depois o Pilar 6 (margem e números da Zion Glamping Store na ficha, `REF`) e o Pilar 7 (decisão «avançar» da Marina), o que mexe em material existente e exige "aprovado"; (c) incluir no Pilar 7 uma caixa «E a 6B?».
2. A Marina como caso (com custos fictícios rotulados) e o resultado «Redesenhar» na conta dela, «Testar» no ajustado.
3. A resposta fictícia do contador da Marina em 6% (o número aparece só no caso, nunca como sugestão), ou mostrar o caso com a linha em branco e a régua em «Testar».
4. A régua da ZAIOS aplicada ao cenário medido (padrão 3), os três cenários do curso com custo aberto e o teste de queda da ZAIOS como passo 2.
5. O tempo de volta em escada (CAPEX no ano zero, rampa, giro no colchão) como número principal, com a conta do Pilar 6 ao lado.
6. Giro pela maior das contas do Pilar 6 (R$ 53.524,02 na Marina), e não 6 meses de fixo (ZAIOS 15); o investimento total da Marina passa de R$ 831.918,38 (6A) para R$ 844.655,02.
7. O colchão de 10% (ZAIOS 10) na leitura «giro + menor saldo», que deixa a Marina em 3,9% e pede R$ 101.469,91 de giro para passar.
8. O múltiplo de saída 6× como botão de referência (ZAIOS 3), contra a recomendação do mapa de não mostrar múltiplo.
9. Nenhum valor de referência inserido pela ficha (imposto, reserva de reposição, valor-hora, cancelamento), só faixas citadas em texto; reserva de reposição sem preenchimento automático dos 3%.
10. O selo com o imposto em branco (régua em «Testar»).
11. Vereditos da ZAIOS (Avançar, Testar, Ajustar, Pausar, Redesenhar) e a explicação de que o «ajustar» acima de 12 anos do Pilar 6 se chama «Redesenhar» na 6B.
12. Os contornos da Planilha 2 (reserva na B12, deduções agrupadas na B11, retirada na B24, giro por fórmula na B7, crescimento 0%) em vez de alterar a planilha; e as dicas da Planilha 2 sem fonte (margem de 30% a 45%, taxa de 10% a 15%, cap rate de 8% a 12%), que contradizem a lição e exigiriam mexer em material existente para sair.
13. Fora das alavancas: «antecipar a fase dois (as cinco cabanas de uma vez)», que o F03 usa no redesenho e o PL2 sugere («a infraestrutura dilui com mais unidades»), mas pede prova de mercado (Pilar 2: limite de mercado 5; 18 unidades em obra na região) e mais capital. Entra ou não como alavanca?
14. A 6A diz no slide «Próximo» e no cap. 11 que a decisão da Marina «continua de pé» dentro do limite. Com a 6B, essa frase pede um complemento («até a conta aberta da 6B»): mexe em peça existente e ligada.
15. Cinco aulas desligadas nos dois módulos (Trilha 1 `6e06c29d` e cópia Plataforma `b2800aa7`), depois da 6A e antes da Planilha 1, com os nomes «Aprofundamento 6B · Viabilidade · …».
16. E-book de 50 a 60 páginas; ficha com 30 a 45 min; aula pedindo só o nome; ficha sem envio de dados.
17. Moeda constante (sem crescimento) e mês de 365 ÷ 12 noites.
18. O nome do curso nas peças («Transforme Seu Terreno em um Projeto de Hospedagem de Sucesso») enquanto o nome comercial «… em um destino turístico» não for decidido (GUIA 1.1).

---

## 13. Decisões de Bruno (28/11)
1. **A 6B mostra a conta real.** Com os custos abertos, a Marina chega a «Redesenhar»; a lição ensina as alavancas e mostra o cenário ajustado (fictício). Os Pilares 6 e 7 ficam como estão; a 6B traz uma nota curta explicando que a página 6 era a primeira conta, com a margem de referência, e que a conta aberta é a que decide (sem desmerecer o Pilar 6).
2. **Imposto da Marina:** 6% como resposta fictícia do contador dela, rotulada «Exemplo ilustrativo». O aluno deixa em branco até falar com o contador dele.
3. Os demais itens da seção 12 seguem como propostos no plano até nova decisão.

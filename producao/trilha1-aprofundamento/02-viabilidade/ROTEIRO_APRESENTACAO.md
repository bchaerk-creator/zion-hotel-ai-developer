# Trilha 1 · Pilar 6 · Aprofundamento 6B · Viabilidade · Roteiro da aula interativa

Status: versão 1 (28/11/2026), construída em `docs/trilha1/apresentacao/pilar6b-aula/index.html`. Nada foi publicado; o ClickMax não foi tocado.
Base: `PLANO.md` desta pasta, seção 5.3 (sequência), seção 7 (o caso da Marina, os únicos números do caso) e seção 13 (decisões de Bruno de 28/11: a 6B mostra a conta real, com «Redesenhar»; nota curta e respeitosa sobre a margem de referência da página 6; imposto de 6% como resposta fictícia do contador dela); `GUIA_COERENCIA.md`, seções 1 a 5 e itens I7 a I9 e I14.
Molde: a aula da 6A (`docs/trilha1/apresentacao/pilar6a-aula/index.html` e `01-capex/ROTEIRO_APRESENTACAO.md`) e o motor `docs/trilha1/apresentacao/_motor/` (sem mudança no motor).
Título: «Aprofundamento 6B · Viabilidade» (`<title>`, `data-titulo`; `data-deck="t1-pilar6b-aula"`).
Saída da aula: a ficha **«Faça agora · A sua conta»** em `docs/trilha1/pilar6b/` (em construção em paralelo), aberta dentro da aula (slide 39) e pelo último botão.
Teste: `tests/test_aula.js` (celular 390 × 844 e computador 1280 × 800). Capturas: `demonstracao/aula-*.png`.

---

## 0. Regras que valem para todos os slides

- **Tamanho:** até cerca de 40 palavras na tela; o resto nas notas (`<aside>`). 40 slides, cerca de 19 minutos.
- **Caso:** a Marina, sempre (GUIA 2.4), partindo das páginas 6 e 6A dela.
  - Números novos da 6B: selo «Exemplo ilustrativo · dados fictícios. Não são preços de referência.»
  - A margem de 40% e o resultado de R$ 108.766,35 só aparecem como o ponto de partida da página 6 dela, com «referência orientativa da página 6, não confirmada; a Zion também vende esse tipo de estrutura» (GUIA 2.1).
  - O imposto de 6%: «resposta fictícia do contador dela; não vale para você» (decisão 2 de Bruno). O aluno deixa a linha em branco até falar com o contador dele.
  - Todo resultado: «Cenários, não promessas.»
- **Como falar da página 6** (PLANO 5.1; decisão 1 de Bruno): «a página 6 respondeu com a margem de referência; agora a resposta vem da sua lista». Proibido: "estava errada", "inflada", "otimista demais" (o teste reprova).
- **Sem sigla:** nenhum «ECROI» na tela, nas notas ou nos atributos. NOI, EBITDA, VPL, TIR, payback e ROI não aparecem (o teste reprova). «CAPEX» aparece como o nome que a 6A já explicou.
- **«Bloco 1» e «Bloco 2»** são as duas partes da aula, no sentido do curso (Comece aqui; aulas do Pilar 6 e da 6A; GUIA 3.2 e I8): «Bloco 1 · Os seis degraus da conta» e «Bloco 2 · A conta da Marina». Nenhum «Bloco 3» em diante e nenhum «Bloco» com outro sentido (o teste reprova). Os seis degraus da conta são «Degrau 1 a 6 de 6» (vocabulário do PLANO, da ficha e do e-book), com a classe `parte` (número grande ao fundo, como na 6A).
- **`data-bloco`**, na ordem: «Abertura», «Como funciona esta aula», «Retomada · Pilar 6 e 6A», «Bloco 1 · Os seis degraus da conta», «Quiz relâmpago», «Bloco 2 · A conta da Marina», «Quiz relâmpago», «Resumo», «A sua página 6B», «Próximo».
- **Faixas** (margem 30/20/10, reserva 3% a 6%, tempo de volta 8 e 12, colchão 10%) sempre como «faixa citada pela fonte; não é meta nem promessa».
- **Sem promessa** de retorno, renda, ocupação, crédito, parceria ou aprovação. Nenhuma alíquota sugerida; nenhuma taxa sugerida.
- **Fotos:** nenhuma. Sem produto avulso nem bônus fora da turma (GUIA 5.10).
- **Sem travessão** no texto da tela. **Toda conta fecha com «Bate.»** nas notas.

## 1. O que a aula grava (combinado com a ficha)

Chave `zion-t1-pilar6b`, a mesma da ficha. Cada gravação relê a chave antes de escrever, para não desfazer o que a ficha salvou.

| Campo | Slide | Valores | Observação |
|---|---|---|---|
| `respostas.d2` | 37 | `"sim"` ou `"nao"` | o item 2 do diagnóstico da ficha (PLANO 6.1, tela 0): «o contador já respondeu o imposto: sim / não» |
| `respostas.nome` | 38 | texto, até 60 caracteres | trazido do perfil de outra página do Dossiê (6A, 6, 5…), se houver |
| `aulaExtras.*` | 4 a 7, 37, todos | `r_margem`, `r_invest`, `r_limite`, `previsao`, `contador` (cópia), `slide` | só da aula |

Só esses dois campos de `respostas` são gravados. Os valores `"sim"` e `"nao"` seguem o texto do PLANO; se a ficha fixar outro código para `d2`, basta trocar as duas chaves do objeto `contador.opcoes` no script da aula. Nada é enviado. Sem e-mail.

## 2. Mapa dos slides

| # | `data-bloco` | Função | Interação | Min |
|---|---|---|---|---|
| 1 | Abertura | capa com o selo da Etapa 4 | — | 0,3 |
| 2 | Como funciona esta aula | Assistir · Responder · Sair com a página 6B | — | 0,4 |
| 3 | Retomada · Pilar 6 e 6A | «Você já fez a página 6… mais uma irmã, a 6B» | — | 0,5 |
| 4 a 6 | Retomada · Pilar 6 e 6A | três perguntas de cabeça | quiz que grava | 1,5 |
| 7 | Retomada · Pilar 6 e 6A | previsão | escolha que grava | 0,7 |
| 8 | Bloco 1 · Os seis degraus da conta | «Faturamento não é lucro…» | — | 0,5 |
| 9 | Bloco 1 | Do Pilar 6 para a 6B | tabela clique a clique | 1,0 |
| 10 | Bloco 1 | os seis degraus | — | 0,4 |
| 11 a 16 | Bloco 1 | Degrau 1 a Degrau 6 | — | 0,6 cada |
| 17 | Quiz relâmpago | classificar 6 itens no degrau | cartões | 1,0 |
| 18 | Bloco 1 | a rampa no calendário | — | 0,8 |
| 19 | Bloco 1 | o giro e o colchão | — | 0,8 |
| 20 | Bloco 1 | a escada do tempo de volta | — | 0,8 |
| 21 | Quiz relâmpago | antes ou depois da reserva? | escolha | 0,5 |
| 22 | Bloco 2 · A conta da Marina | de onde ela parte | tabela clique a clique | 1,0 |
| 23 | Bloco 2 | degraus 1 a 3 | tabela clique a clique | 1,0 |
| 24 | Bloco 2 | degraus 4 a 6: 21,3% | tabela clique a clique | 1,2 |
| 25 | Bloco 2 | de onde vem a diferença (nota sobre a página 6) | tabela clique a clique | 1,0 |
| 26 | Bloco 2 | equilíbrio e folga | — | 1,0 |
| 27 | Bloco 2 | o primeiro ano mês a mês | tabela clique a clique | 1,2 |
| 28 | Bloco 2 | giro e colchão | — | 1,0 |
| 29 | Bloco 2 | a escada da Marina: 15,0 anos | tabela clique a clique | 1,0 |
| 30 | Bloco 2 | os cinco passos → Redesenhar | semáforo (cartões) | 1,2 |
| 31 | Bloco 2 | o critério da página 6 dispara; a previsão volta | — | 1,0 |
| 32 | Bloco 2 | semáforo das alavancas | cartões | 1,0 |
| 33 | Bloco 2 | mexa você: uma alavanca por vez | simulador | 1,2 |
| 34 | Bloco 2 | o cenário ajustado e por que dá Testar | tabela clique a clique | 1,0 |
| 35 | Quiz relâmpago | a ação de 30 dias | escolha | 0,5 |
| 36 | Resumo | O 6B em cinco frases | — | 0,7 |
| 37 | A sua página 6B | critério de conclusão; o contador | escolha que grava | 0,6 |
| 38 | A sua página 6B | o nome | campo que grava | 0,3 |
| 39 | A sua página 6B | a ficha embutida | ficha | — |
| 40 | Próximo | a página 6 refeita, a Planilha 2 e o Pilar 7 | botão «Abrir a ficha» | 0,5 |

Total: cerca de 19 minutos de aula, mais a ficha.

---

## 3. Slide a slide

### Slide 1 · Abertura
- **Molde:** `section.s.esc.sem-topo`, logo claro, sem foto.
- **Tela:** `p.k` «Método Zion · Etapa 4 · Fechar a conta»; `h1` «Aprofundamento 6B<br><i>Viabilidade</i>»; lead «Com as páginas 6 e 6A na mão: a conta aberta linha por linha, da receita bruta ao que sobra, o primeiro ano mês a mês e a régua para decidir se avança, ajusta ou redesenha.»
- **Notas:** 20 s. A aula abre a linha que a página 6 fechou com a margem de referência: quanto sobra. Cenários, não promessas; a primeira versão sai em uma tarde, com o imposto em branco se o contador não respondeu.
- **Fonte:** PLANO 1 e 5.3 item 1; GUIA 1.4.

### Slide 2 · Como funciona esta aula
- **Tela:** «O que você vai fazer aqui» · «Assistir, responder *e sair com a página 6B*»; três cartões; dica: ter à mão as páginas 6 e 6A e a curva do ano do Pilar 2.
- **Fonte:** PLANO 5.3 item 2.

### Slide 3 · Retomada · Pilar 6 e 6A
- **Tela:** «Você já fez a página 6 no Pilar 6 e a 6A. *Aqui a página 6 ganha mais uma irmã, a 6B.*»; lead: a 6B abre a linha que a página 6 fechou com uma margem de referência, quanto sobra; a pergunta continua «o negócio se paga?»; «Responda de cabeça. Errar aqui também ensina.»
- **Fonte:** PLANO 5.3 item 3; GUIA 5.1 a 5.3.

### Slide 4 · Retomada · a margem (`aulaExtras.r_margem`)
- **Pergunta:** «Que margem a página 6 da Marina usou, e de onde ela veio?» · A) 21%, da lista de custos dela · **B) 40%, a margem de referência: simplificação, não promessa** · C) 60%, a média do destino.
- **Feedback:** a margem de referência acerta a ordem de grandeza do ano e não mostra o mês que aperta.
- **Fonte:** P6 cap. 05; ficha do Pilar 6 (campo margem).

### Slide 5 · Retomada · o investimento da 6A (`aulaExtras.r_invest`)
- **Pergunta:** «Qual é o investimento total da 6A da Marina?» · A) Cerca de R$ 690 mil · **B) Cerca de R$ 832 mil** · C) Cerca de R$ 1,2 milhão.
- **Notas:** 791.131 + 40.787,38 = 831.918,38. Bate.
- **Fonte:** 6A; PLANO 7.1.

### Slide 6 · Retomada · o limite (`aulaExtras.r_limite`)
- **Pergunta:** «Até quanto a página 6 dizia que o investimento aguentava, em 8 anos no conservador?» · A) Cerca de R$ 690 mil · **B) Cerca de R$ 870 mil** · C) Cerca de R$ 1,2 milhão.
- **Notas:** 8 × 108.766,35 = 870.130,80. Bate. Feito com a margem de 40%: volta no Bloco 2.
- **Fonte:** P6 cap. 07; PLANO 5.3 item 4.

### Slide 7 · Previsão (`aulaExtras.previsao`)
- **Pergunta:** «Com os custos abertos, a margem da Marina fica perto dos 40%, acima ou abaixo?» · «E o limite de R$ 870 mil continua de pé?»
- **Opções:** Abaixo de 40%, e o limite de R$ 870 mil cai · Abaixo de 40%, e o limite continua de pé · Perto de 40% · Acima de 40%. Sem certo ou errado aqui; a previsão volta no slide 31.
- **Fonte:** PLANO 4 (etapa 1) e 5.3 item 5.

### Slide 8 · Bloco 1 · Os seis degraus da conta (abertura)
- **Tela:** citação «"Faturamento não é lucro, e o custo fixo *não diminui na baixa.*"» · «Pilar 6 · Pré-viabilidade, capítulo 05» · lead (clique): «O Pilar 6 deixou escrito: "A margem real sai da sua lista de custos, com o seu trabalho e a reserva de reposição dentro." A 6B é esse passo.»
- **Fonte:** P6 cap. 05; ficha do Pilar 6; PLANO 5.1.

### Slide 9 · Do Pilar 6 para a 6B
- **Tela:** tabela clique a clique (caixa «Do Pilar 6 para a 6B» do PLANO 5.2): margem de referência → escada de seis degraus; mesma margem nos três cenários → custo fixo igual e margem que sobe; giro pela margem → maior de duas contas do Pilar 6; tempo de volta sem rampa → escada; régua 5/8/12 → cinco passos e Avançar, Testar, Ajustar, Pausar ou Redesenhar; "o que precisa ser verdade" com a margem fixa → com o custo aberto.
- **Notas:** o «ajustar» acima de 12 anos do Pilar 6 se chama «Redesenhar»; Pausar só por escolha.
- **Fonte:** PLANO 5.2 (caixa) e 6.2.

### Slide 10 · Os seis degraus
- **Tela:** «Da receita bruta *ao que sobra*»: Receita bruta · Receita real · Margem de contribuição · Resultado antes da reserva · Depois dos custos do modelo · O que sobra. «Fora desta conta: a parcela do empréstimo (Pilar 7), o imposto sobre o lucro (contador) e o terreno, que fica ao lado.»
- **Fonte:** PLANO 5.2 cap. 02; 6.2.

### Slide 11 · Degrau 1 de 6 · Receita bruta
- **Molde (11 a 16):** `section.s.parte` com `div.num-bg` (1 a 6), «Degrau N de 6», cartão «A pergunta-chave», cartão «O erro típico», «O que entra».
- **Tela:** quantas noites você vende de verdade, e a que diária média do ano? · erro: diária da alta e ocupação do destino · entra: unidades × ocupação dos doze meses × diária média × 365; outras receitas com custo; taxa de limpeza fora.
- **Fonte:** PLANO 5.2 cap. 03; R2 a R6; ZAIOS 11; P4.

### Slide 12 · Degrau 2 de 6 · Receita real
- **Tela:** o que sai antes de o dinheiro chegar? · erro: esquecer o imposto, ou contar a comissão duas vezes · citação «"Imposto sobre a receita é a omissão mais frequente e a mais cara."» · entra: imposto (contador, senão em branco), comissão, cartão, cancelamento.
- **Fonte:** PLANO 5.2 cap. 04; R7 a R9; Jornada do COMO, Etapa 02.

### Slide 13 · Degrau 3 de 6 · Margem de contribuição
- **Tela:** quanto custa cada noite e cada estadia? · erro: esquecer a lavanderia por estadia, ou pôr a comissão de novo · entra: lavanderia, amenidades, energia da noite, limpeza, perdas e quebras de material.
- **Fonte:** PLANO 5.2 cap. 05.

### Slide 14 · Degrau 4 de 6 · Resultado antes da reserva
- **Tela:** quanto custa o mês, com hóspede ou sem? · erro: deixar o seu trabalho de fora · citação «"Se o negócio não paga quem o opera, ele não é um negócio."» · entra: pessoa local, 13º e férias, contador, anuais em duodécimos, manutenção, marketing e a sua retirada.
- **Fonte:** PLANO 5.2 cap. 05; R10, R12; Jornada do COMO, Etapa 09.

### Slide 15 · Degrau 5 de 6 · Custos do modelo
- **Tela:** alguém fica com uma parte? · erro: esquecer a taxa de quem administra · entra: aluguel, gestão, royalty; zero se você opera.
- **Fonte:** PLANO 6.1 (tela 5) e 6.2.

### Slide 16 · Degrau 6 de 6 · O que sobra
- **Tela:** quanto você separa por ano para trocar o que se gasta? · erro: não separar nada, ou somar reserva e depreciação · faixa de 3% a 6% citada pelas fontes; a régua da Zion usa 3%.
- **Notas:** faixas de margem 30/20/10, citadas pela fonte.
- **Fonte:** PLANO 5.2 cap. 06; R11; 6.3.

### Slide 17 · Quiz relâmpago · em que degrau?
- **Interação:** seis cartões que viram: comissão da plataforma (Degrau 2) · lavanderia por estadia (Degrau 3) · as horas da Marina (Degrau 4) · taxa de uma administradora (Degrau 5) · troca dos colchões daqui a seis anos (Degrau 6) · parcela do empréstimo da obra (fora desta conta, Pilar 7).
- **Fonte:** PLANO 5.3 item 6 e 5.4 (E3).

### Slide 18 · A rampa no calendário
- **Tela:** citação «"Ninguém abre na ocupação do destino."» · degraus 40% (meses 1 a 3) · 50% (4 a 6) · 75% (7 a 12) · 100% (do mês 13) · como se lê.
- **Fonte:** P6 cap. 06; ZAIOS 6; PLANO 6.2 e 11 (lacuna 9).

### Slide 19 · O giro e o colchão
- **Tela:** conta A do Pilar 6 (três meses de custo) · conta B (buraco do primeiro ano + três meses de fixo) · colchão (giro − o buraco; a régua da Zion pede 10% do CAPEX) · citação «"Projeto não quebra por prejuízo. Quebra por falta de caixa num mês específico."»
- **Fonte:** P6 cap. 06; ZAIOS 10; Volume 05 · Investimento, cap. 08.

### Slide 20 · A escada do tempo de volta
- **Tela:** ano zero (CAPEX da 6A, sem giro e sem terreno) · ano 1 com a rampa · ano 2 em diante o que sobra · citação «"Lucro e retorno são coisas diferentes."» · 8 / 12 anos.
- **Fonte:** P6 cap. 07; F03; ZAIOS 9; PLANO 6.2.

### Slide 21 · Quiz relâmpago · antes ou depois da reserva?
- **Interação:** «O tempo de volta se calcula sobre o resultado antes ou depois da reserva de reposição?» · Antes · **Depois: sobre o que sobra**.
- **Fonte:** PLANO 5.3 item 6; R20.

### Slide 22 · Bloco 2 · A conta da Marina
- **Tela:** selo «Exemplo ilustrativo»; tabela clique a clique: Pilar 2 R$ 645 · 38,5% · Pilar 4 R$ 271.915,88 · página 6, 40% → R$ 108.766,35 · 6A CAPEX R$ 791.131,00 · investimento total R$ 831.918,38. Rótulo da referência; novo e fictício: abertura em junho e estadia de 2 noites.
- **Notas:** 1.095 × 0,385 × 645 = 271.915,88; × 0,40 = 108.766,35; 791.131 + 40.787,38 = 831.918,38. Bate.
- **Fonte:** PLANO 7.1.

### Slide 23 · Da receita bruta à contribuição
- **Tela:** receita bruta R$ 271.915,88 · imposto 6% (resposta fictícia do contador dela) − R$ 16.314,95 · comissão 9% − R$ 24.472,43 · cartão 1,2% e cancelamento 2% − R$ 8.701,31 · receita real R$ 222.427,19 · custos de cada noite − R$ 43.822,72 · **margem de contribuição R$ 178.604,46**.
- **Notas:** deduções 49.488,69 (18,2%); custos de cada noite linha a linha; diferença de R$ 0,01 do arredondamento. Bate.
- **Fonte:** PLANO 7.2 e 7.3; decisão 2 de Bruno.

### Slide 24 · Dos fixos ao que sobra
- **Tela:** contribuição R$ 178.604,46 · fixos R$ 8.000 × 12 − R$ 96.000,00 · retirada 8 h × R$ 40 × 4,33 − R$ 16.627,20 · resultado antes da reserva R$ 65.977,26 · custos do modelo R$ 0 · reserva 3% − R$ 8.157,48 · **o que sobra R$ 57.819,79 · 21,3%** · base 30,8%, otimista 38,2%; «Cenários, não promessas.»
- **Notas:** pelo caminho da noite: 645 × 0,778 − 97,50 = 404,31; 421,575 × 404,31 − 112.627,20 = 57.819,79. Bate.
- **Fonte:** PLANO 7.2 e 7.3.

### Slide 25 · De onde vem a diferença (a nota sobre a página 6)
- **Tela:** caixa «Uma nota sobre a página 6. Ela fez a primeira conta, com a margem de referência que ela mesma chama de "simplificação, não promessa". A página 6 respondeu com a margem de referência; agora a resposta vem da lista da Marina.»; tabela: deduções 18,2% · custos de cada noite 16,1% · fixos com o trabalho dela 41,4% · reserva 3,0% · **o que sobra 21,3%** (na página 6, 40%, R$ 108.766,35).
- **Notas:** sem adjetivo; 100 − 78,7 = 21,3; 214.096,09 e 57.819,79. Bate.
- **Fonte:** PLANO 5.1 (regra de redação) e 7.3; decisão 1 de Bruno.

### Slide 26 · A operação se paga?
- **Tela:** o que fica de cada noite R$ 404,31 · equilíbrio 278,57 noites = 25,4% · **folga 13,1 pontos** · custo por diária vendida R$ 507,85 · diária de equilíbrio R$ 468,71 · «A operação se paga com folga. A pergunta seguinte é outra: e o investimento?»
- **Notas:** piso R$ 125,32. Bate.
- **Fonte:** PLANO 7.4.

### Slide 27 · O primeiro ano, mês a mês
- **Tela:** jun a ago (64% × 40%) + R$ 59,08 · set e out − R$ 2.006,94 · nov − R$ 5.327,34 · dez a mar − R$ 3.298,21, **menor saldo em março − R$ 22.356,81** · abr e mai + R$ 1.682,39 · ano 1 − R$ 18.992,04 · ano em regime por tipo de mês.
- **Notas:** r = 253,8 ÷ 462 = 0,549351; 93.635,16 − 112.627,20 = −18.992,04. Bate. Reserva de sazonalidade R$ 2.115,13.
- **Fonte:** PLANO 7.5.

### Slide 28 · O giro e o colchão da Marina
- **Tela:** giro da 6A R$ 40.787,38 · conta A R$ 53.524,02 · conta B R$ 50.513,61 · **giro da 6B R$ 53.524,02 · investimento refeito R$ 844.655,02** · colchão R$ 31.167,21 · 3,9% · para 10%, giro de R$ 101.469,91.
- **Fonte:** PLANO 7.6.

### Slide 29 · A escada da Marina
- **Tela:** ano zero − R$ 791.131,00 · ano 1 − R$ 18.992,04 · por ano + R$ 57.819,79 · **15,0 anos** · como o Pilar 6 calcula 14,6 anos · com o terreno 25,4 anos · base 8,2 e otimista 5,3 anos.
- **Notas:** 15 + 646,00 ÷ 57.819,79 = 15,01. Bate. Retorno simples 7,3% (4,2% com o terreno).
- **Fonte:** PLANO 7.7.

### Slide 30 · A régua em cinco passos
- **Interação:** seis cartões: 1 passa (R$ 57.819,79) · 2 passa (+ R$ 6.806,35) · 3 redesenhar (15,0 anos) · 4 redesenhar (negativo a qualquer taxa sem a venda) · 5 ajustar (3,9%) · **veredito sugerido: Redesenhar**.
- **Fonte:** PLANO 7.8 e 7.9; 6.2 (régua).

### Slide 31 · O critério que ela escreveu na página 6 dispara
- **Tela:** citação do critério da Marina na página 6 · limite da página 6 cerca de R$ 870 mil → com a margem aberta R$ 462.558,31 · «"Quando a conta não fecha, a conta está certa." Veredito escrito por ela: Redesenhar.» · abaixo, a previsão do slide 7 («Foi isso» ou «a previsão errada também ensina»).
- **Notas:** critério para parar da 6B: «Se nenhum redesenho passar de 12 para 8 anos com premissas provadas, eu não assino a obra.»
- **Fonte:** PLANO 7.1, 7.8 e 7.9; Jornada do COMO, Etapa 02.

### Slide 32 · Qual alavanca pesa mais?
- **Interação:** seis cartões (cor do passo 3): diária + R$ 50 (11,8 anos, amarelo) · ocupação + 5 pontos (11,0, amarelo) · custo fixo − 10% (12,6, vermelho) · CAPEX − 10% (13,6, vermelho) · cesta de café (13,4, vermelho) · fase menor de 2 cabanas (mais de 100 anos, vermelho).
- **Fonte:** PLANO 7.10.

### Slide 33 · Mexa você · uma alavanca por vez (simulador)
- **Interação:** `.sim[data-sim=alavancas]`: diária (R$ 545 a R$ 945, começa em R$ 645), ocupação (28,5% a 53,5%, começa em 38,5%), custo fixo (0 a − 30%), CAPEX (0 a − 30%). Saídas: o que fica de cada noite, o que sobra e a margem, ano 1, tempo de volta em escada e o passo 3. Aviso verde (até 8), amarelo (até 12), vermelho; aviso «mexa uma por vez» se duas alavancas mudarem; aviso de premissa a provar (diária acima de 1,05 × R$ 645 ou ocupação acima de 38,5%). Botão «Voltar à conta da Marina»; tecla R.
- **Conferência (testada):** R$ 404,31 · R$ 57.820 · 21,3% · − R$ 18.992 · 15,0 anos (vermelho) · diária R$ 695 → R$ 74.219, 11,8 anos (amarelo) · diária R$ 810 → 8,0 anos (verde) · ocupação 43,5% → R$ 79.956, 11,0 anos · fixo − 10% → R$ 69.083, 12,6 anos · CAPEX − 10% → 13,6 anos.
- **Fonte:** PLANO 6.2 (alavancas) e 7.10.

### Slide 34 · O cenário ajustado e por que dá Testar
- **Tela:** selo «… o que precisaria ser verdade»; diária de R$ 716 (hipótese do Pilar 3), 42% com pacote de domingo a quinta e a cesta de café · o que sobra R$ 106.638,40 (30,6%) · ano 1 + R$ 7.826,50 · 8,3 anos · colchão 7,4% · passos 3, 4 e 5 ajustar · **pela régua Ajustar; com premissas não provadas, a ficha mostra Testar**.
- **Notas:** cascata conferida; os 90 dias do Pilar 7 provam preço e semana.
- **Fonte:** PLANO 7.11.

### Slide 35 · Quiz relâmpago · a ação de 30 dias
- **Interação:** **«Rodar a 6B com três redesenhos, uma alavanca por vez, e não assinar contrato de obra.»** Prazo 28/12/2026; verificação: as três versões da 6B salvas, com data.
- **Fonte:** PLANO 6.5 (ordem 2) e 7.9.

### Slide 36 · Resumo · O 6B em cinco frases
- **Tela:** (1) A 6B não começa do zero: abre a margem de referência da página 6 com a sua lista de custos. (2) Seis degraus, da receita bruta ao que sobra; o seu trabalho e a reserva de reposição ficam dentro. (3) Passar do equilíbrio com folga paga a operação; o investimento é outra pergunta: lucro e retorno são coisas diferentes. (4) O primeiro ano tem rampa e um mês que aperta; o giro e o colchão saem dele. (5) A régua decide em cinco passos; se a conta não fecha, mexa uma alavanca por vez e escreva o critério para parar.
- **Fonte:** PLANO 5.3 item 8; GUIA 1.4.

### Slide 37 · A sua página 6B · critério de conclusão (`respostas.d2`)
- **Tela:** «Pronto *para levar à página 6*»: quatro critérios, um por clique; pergunta «O seu contador já respondeu qual imposto incide sobre a receita?» (Sim, com data e nome · Ainda não).
- **Feedback:** Ainda não → «Deixe a linha em branco: o resultado sai antes do imposto e a régua fica em Testar. Leve a conta ao contador com as perguntas do checklist.»
- **Fonte:** PLANO 6.6 (selo com o imposto em branco) e 6.4 (B1); decisão 2 de Bruno.

### Slide 38 · A sua página 6B · o nome (`respostas.nome`)
- **Tela:** «O seu nome *na página 6B*», opcional. «Sem e-mail: esta ficha não envia nada, o PDF fica só com você.»
- **Fonte:** PLANO 5.3 item 9; GUIA I14.

### Slide 39 · A sua página 6B · a ficha embutida
- **Molde:** o encaixe `s.diag` da 6A: `iframe` com `../../pilar6b/` (`?turma=acompanhamento` quando a aula vier com esse parâmetro), carregado só ao chegar no slide e recarregado ao voltar; link «Abrir em tela cheia».
- **Tela:** «Faça agora · A sua conta. As páginas 6 e 6A, a resposta do contador e o seu nome já estão na ficha. Monte os seis degraus e baixe a página 6B.»

### Slide 40 · Próximo · a página 6 refeita, a Planilha 2 e o Pilar 7
- **Tela:** baixe a página 6B · refaça a página 6 (margem e meses de giro do quadro «Como levar para a página 6») · Planilha 2 pelo quadro célula a célula (Planilha 1 opcional) · leve o veredito e o critério para parar ao Pilar 7. Caixa «Lembre»: «Salve o PDF da página 6B na pasta Meu Dossiê, ao lado das páginas 6 e 6A. Esta ficha não envia nada: o PDF fica só com você.» Aviso do Pilar 7: «No Pilar 7, a Marina decide com a página 6 de referência. Com a 6B, o critério que ela mesma escreveu dispara: antes de pedir dinheiro a alguém, ela redesenha e prova preço e semana.» Botão «Abrir a ficha» → `../../pilar6b/`; aviso educativo do PLANO 5.1, com «Cenários, não promessas.»
- **Último botão da barra:** «Abrir a ficha ›» → `../../pilar6b/`.
- **Turma de acompanhamento:** o passo 2 vira «Leve as páginas 6A e 6B ao encontro do Pilar 6 e refaça a página 6 depois do comentário da equipe.»
- **Fonte:** PLANO 5.3 item 10, 7.13, 8 e 9; GUIA 5.9.

---

## 4. Citações literais usadas

| Slide | Citação | Fonte |
|---|---|---|
| 8 | "Faturamento não é lucro, e o custo fixo não diminui na baixa." | Pilar 6 · Pré-viabilidade, cap. 05 |
| 8 | "A margem real sai da sua lista de custos, com o seu trabalho e a reserva de reposição dentro." | Pilar 6 (ficha, campo margem) |
| 12 | "Imposto sobre a receita é a omissão mais frequente e a mais cara." | Jornada do COMO, Etapa 02 |
| 14 | "Se o negócio não paga quem o opera, ele não é um negócio." | Jornada do COMO, Etapa 09 |
| 11 (notas) | "Receita bruta não é lucro." | Pilar 4 |
| 18 | "Ninguém abre na ocupação do destino." | Pilar 6, cap. 06 |
| 19 | "Projeto não quebra por prejuízo. Quebra por falta de caixa num mês específico." | Volume 05 · Investimento, cap. 08 |
| 20 | "Lucro e retorno são coisas diferentes." | Pilar 6, cap. 07 |
| 4, 25 | "simplificação, não promessa" | Pilar 6, cap. 05 |
| 31 | "Quando a conta não fecha, a conta está certa." | Jornada do COMO, Etapa 02 |
| 34 (notas) | "Primeiro prove a conta. Depois escolha como crescer." | Pilar 6, cap. 08 |
| 37 (pergunta) | "Uma linha em branco vale mais do que um número inventado." | Pilar 6 |

## 5. Pendências
1. A ficha `docs/trilha1/pilar6b/` está sendo construída em paralelo: o slide 39 e o último botão apontam para ela; até ela existir, o iframe mostra a página de erro do servidor (o teste anota à parte, sem contar como erro da aula). Conferir, quando a ficha existir, que ela lê `respostas.d2` com os códigos `"sim"` e `"nao"` e `respostas.nome`.
2. O nome sem e-mail (slide 38) segue a 6A (**a confirmar por Bruno**, PLANO 12, item 16).
3. Os itens da seção 12 do PLANO que não foram decididos em 28/11 seguem como propostos (decisão 3 de Bruno).

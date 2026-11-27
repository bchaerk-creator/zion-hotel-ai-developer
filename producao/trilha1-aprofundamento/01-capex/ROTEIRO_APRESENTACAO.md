# Trilha 1 · Pilar 6 · Aprofundamento 6A · CAPEX · Roteiro da aula interativa

Status: versão 2 (27/11/2026), construída em `docs/trilha1/apresentacao/pilar6a-aula/index.html` (pasta movida de `capex-aula/`). Substitui a versão 1 (34 slides, caso da Helena). O ClickMax não foi tocado.
Base: `PLANO.md` desta pasta, seção 5.3 (sequência) e seção 7 (o caso da Marina, os únicos números do caso); `GUIA_COERENCIA.md`, itens I7 a I9 e seções 1 e 2 (narrativa e personagens).
Molde: `docs/trilha1/apresentacao/pilar6-aula/index.html` e o motor `docs/trilha1/apresentacao/_motor/deck.js` + `deck.css` (sem mudança no motor).
Título: «Aprofundamento 6A · CAPEX» (`<title>`, `data-titulo`; `data-deck="t1-pilar6a-aula"`).
Saída da aula: a ficha **«Faça agora · O seu CAPEX»** em `docs/trilha1/pilar6a/`, aberta dentro da aula (slide 37) e pelo último botão.
Teste: `tests/test_aula.js` (celular 390 × 844 e computador 1280 × 800).

---

## 0. Regras que valem para todos os slides

- **Tamanho:** até cerca de 40 palavras na tela; o resto nas notas (`<aside>`). 38 slides, cerca de 18 minutos.
- **Caso:** a Marina, sempre (GUIA 2.4). A Helena e os Chalés do Ribeirão saíram de todas as telas e notas.
  - Números novos da 6A: selo «Exemplo ilustrativo · dados fictícios. Não são preços de referência.»
  - Números da página 6 dela (R$ 577.038, R$ 690.529,18): rótulo «Referência orientativa da página 6, não confirmada; a Zion também vende esse tipo de estrutura.» Nunca como preço.
  - Página 6 × 6A só pelo total, explicado pelo escopo, sem "mais caro" ou "mais barato" (PLANO 5.1).
- **Sem sigla interna:** nenhum «ECROI» na tela, nas notas, nos atributos ou nos comentários. «CAPEX» só no nome da aula e da página, explicado uma vez («O nome técnico é CAPEX…», slide 9). Sem FF&E e OS&E na tela.
- **«Parte 1 a 7»** para as sete partes do custo (I8). «Bloco» só no sentido do curso: «Bloco 1 · As sete partes do custo» e «Bloco 2 · A Marina abre a página 6». As sete partes usam a classe `parte` (número grande ao fundo desenhado pela própria aula).
- **`data-bloco`** (I7), na ordem: «Abertura», «Como funciona esta aula», «Retomada · Pilar 6», «Bloco 1 · As sete partes do custo», «Quiz relâmpago», «Bloco 2 · A Marina abre a página 6», «Quiz relâmpago», «Resumo», «A sua página 6A», «Próximo». O teste reprova «ECROI» e «Bloco 3» a «Bloco 7».
- **Percentuais** (reserva, enxoval ÷ mobília, pré-abertura ÷ obra, obra acima de 80%) sempre como «faixa de conferência citada pela fonte; não é preço nem regra fixa».
- **Sem promessa** de aprovação, crédito, parceria, retorno, ocupação, renda ou prazo de obra.
- **Fotos:** nenhuma nesta versão (a capa é escura, sem foto). Ferramenta 05 e Calculadora de Implantação não aparecem (I6).
- **Toda conta fecha com «Bate.»** nas notas.

## 1. O que a aula grava (combinado com a ficha)

Chave `zion-t1-pilar6a`, a mesma da ficha. Cada gravação relê a chave antes de escrever, para não desfazer o que a ficha salvou (ela pode estar aberta dentro da aula ou em outra aba).

| Campo | Slide | Valores | Observação |
|---|---|---|---|
| `respostas.pagina6Total` | 7 | o número digitado, como texto (ex.: `"690.529,18"`), ou `"nao_sei"` | lido pela tela 1 da ficha; a aula oferece o `resumo.dados.total` de `zion-t1-pilar6` com «Veio da sua página 6» e «Usar este número» |
| `respostas.d3` | 35 | `"maioria"`, `"algumas"`, `"nenhuma"` | a mesma pergunta do diagnóstico da ficha |
| `respostas.nome` | 36 | texto, até 60 caracteres | trazido do perfil de outra página do Dossiê, se houver |
| `aulaExtras.*` | 4 a 8, todos | `r_fora`, `r_reserva`, `r_limite`, `previsao`, `pagina6` (cópia, ou `"nao_fiz"`), `cotadas` (cópia), `slide` | só da aula; «Ainda não fiz a página 6» fica aqui, não em `respostas` |

Nada é enviado. Sem e-mail (a ficha não envia nada).

## 2. Mapa dos slides

| # | `data-bloco` | Função | Interação | Min |
|---|---|---|---|---|
| 1 | Abertura | capa com o selo da Etapa 4 | — | 0,3 |
| 2 | Como funciona esta aula | Assistir · Responder · Sair com a página 6A | — | 0,4 |
| 3 | Retomada · Pilar 6 | «Você já fez a página 6… a 6A» | — | 0,5 |
| 4 a 6 | Retomada · Pilar 6 | três perguntas de cabeça | quiz que grava | 1,5 |
| 7 | Retomada · Pilar 6 | o número de partida: página 6 × 6A | número que grava | 1,0 |
| 8 | Retomada · Pilar 6 | previsão | escolha que grava | 0,7 |
| 9 | Bloco 1 · As sete partes do custo | «abrir a porta» e a sigla, uma vez | — | 0,5 |
| 10 | Bloco 1 | Do Pilar 6 para a 6A | tabela clique a clique | 1,0 |
| 11 | Bloco 1 | dentro, ao lado, à parte | — | 1,0 |
| 12 | Bloco 1 | as três origens | — | 0,8 |
| 13 | Bloco 1 | as sete partes | — | 0,3 |
| 14 a 20 | Bloco 1 | Parte 1 a Parte 7 | — | 0,6 cada |
| 21 | Quiz relâmpago | classificar 6 itens | marcar (cartões) | 1,0 |
| 22 | Quiz relâmpago | a reserva (o ofurô na crista; a sobra) | verdadeiro ou falso (2) | 0,6 |
| 23 | Bloco 2 · A Marina abre a página 6 | os fatos dela | — | 0,7 |
| 24 | Bloco 2 | a página 6 dela | tabela clique a clique | 1,0 |
| 25 | Bloco 2 | as Partes 1 a 6 | tabela clique a clique | 1,0 |
| 26 | Bloco 2 | da reserva ao limite | tabela clique a clique | 1,2 |
| 27 | Bloco 2 | mexa você: a reserva, o investimento e a folga | calculadora + semáforo | 1,2 |
| 28 | Bloco 2 | quanto tem papel; a régua | — | 0,7 |
| 29 | Bloco 2 | o número lido de quatro jeitos | — | 0,8 |
| 30 | Bloco 2 | o semáforo dos alertas | semáforo (cartões) | 1,0 |
| 31 | Bloco 2 | página 6 × página 6A; a previsão volta | — | 1,0 |
| 32 | Bloco 2 | cabe, mas a folga é fina | — | 0,8 |
| 33 | Quiz relâmpago | a ação de 30 dias | escolha | 0,5 |
| 34 | Resumo | O 6A em cinco frases | — | 0,7 |
| 35 | A sua página 6A | critério de conclusão | escolha que grava | 0,6 |
| 36 | A sua página 6A | o nome | campo que grava | 0,3 |
| 37 | A sua página 6A | a ficha embutida | ficha | — |
| 38 | Próximo | Planilha 1, Planilha 2 e a página 6 refeita | botão «Abrir a ficha» | 0,5 |

Total: cerca de 18 minutos de aula, mais a ficha.

---

## 3. Slide a slide

### Slide 1 · Abertura
- **Molde:** `section.s.esc.sem-topo`, logo claro no topo, sem foto.
- **Tela:** `p.k` «Método Zion · Etapa 4 · Fechar a conta»; `h1` «Aprofundamento 6A<br><i>CAPEX</i>»; `p.lead` «Com a página 6 na mão: quanto custa abrir a porta, em sete partes, com a origem de cada número, e se a conta ainda cabe no limite da sua página 6.»
- **Notas:** 20 s. A aula aprofunda uma linha da página 6; no fim, a ficha abre aqui dentro. A primeira versão sai com estimativas e linhas em branco.
- **Fonte:** PLANO 1 (promessa) e 5.3 item 1; GUIA I9.

### Slide 2 · Como funciona esta aula
- **Molde:** `section.s` com três `.card` e `.sv` de dica, como no Pilar 6.
- **Tela:** «O que você vai fazer aqui» · «Assistir, responder *e sair com a página 6A*»; cartões Assistir (um trecho por vez), Responder (uma pergunta por tela, salva neste aparelho), Sair com a página 6A (a ficha abre aqui dentro). Dica: ter à mão a página 6 (Pilar 6) e o Masterplan faseado (Pilar 5).
- **Fonte:** PLANO 5.3 item 2; `pilar6-aula`, slide 2.

### Slide 3 · Retomada · Pilar 6
- **Molde:** `section.s.esc`.
- **Tela:** «Antes de começar · sem olhar as anotações»; `h2` «Você já fez a página 6 no Pilar 6. *Aqui ela ganha uma página irmã, a 6A.*»; lead: a 6A abre as linhas uma por uma; a pergunta continua «o negócio se paga?»; «Responda de cabeça. Errar aqui também ensina.»
- **Fonte:** GUIA 5.1 a 5.3; PLANO 5.3 itens 3 e 4.

### Slide 4 · Retomada · o que ficou à parte (quiz que grava, `aulaExtras.r_fora`)
- **Pergunta:** «O que ficou à parte na página 6 da Marina?» · A) O capital de giro e as licenças · **B) A infraestrutura comum e o terreno** · C) A mobília e o enxoval.
- **Feedback:** «A infraestrutura comum ficou "a cotar" e o terreno, fora da conta, mas não de graça. O giro entrou somado no investimento total.»
- **Fonte:** P6 caps. 02 a 04.

### Slide 5 · Retomada · a base da reserva (`aulaExtras.r_reserva`)
- **Pergunta:** «Sobre o que a base simplificada da página 6 calcula a reserva do imprevisto?» · A) Sobre tudo, com o giro · **B) 10% sobre as unidades prontas** · C) Um valor fixo para a fase.
- **Feedback:** na 6A a base muda: o percentual vai sobre o subtotal das Partes 1 a 6.
- **Fonte:** P6 cap. 03; PLANO 5.2 (caixa «Do Pilar 6 para a 6A»).

### Slide 6 · Retomada · o limite (`aulaExtras.r_limite`)
- **Pergunta:** «Até quanto o investimento total da Marina aguenta, dentro de 8 anos no conservador?» · A) Cerca de R$ 690 mil · **B) Até cerca de R$ 870 mil** · C) Até cerca de R$ 1,2 milhão.
- **Notas:** 8 × R$ 108.766,35 = R$ 870.130,80. Bate.
- **Fonte:** P6 cap. 07 («o que precisa ser verdade»); P7 (critério da Marina).

### Slide 7 · A sua página 6 · página 6 × 6A (número que grava, `respostas.pagina6Total`)
- **No lugar do palpite** (I2). **Pergunta:** «Na sua página 6, qual é o investimento total da fase um?» Explicação: copiar da página 6 o investimento total, com o giro; no fim, a ficha compara a página 6 com a 6A.
- **Campo:** R$ (texto pt-BR, ex. «690.529,18»), «Não sei» (`nao_sei`) e «Ainda não fiz a página 6» (só em `aulaExtras.pagina6`). Se `zion-t1-pilar6` tiver `resumo.dados.total`, aparece a caixa «Veio da sua página 6: R$ X, de dd/mm/aaaa» com o botão «Usar este número».
- **Caixa Marina:** «A página 6 da Marina diz R$ 690.529,18, cerca de R$ 690 mil. É referência orientativa da página 6, não confirmada; a Zion também vende esse tipo de estrutura.»
- **Feedback:** número → «Guardado · R$ X. Ele já está na ficha.» · Não sei → tarefa da semana (abrir o PDF na pasta Meu Dossiê) · Não fiz → «A 6A é a página irmã da 6… Faça a página 6 no Pilar 6 para comparar» (alerta A22 da ficha).
- **Fonte:** PLANO 4 (etapa 1), 6.1 (tela 1), 6.4 (A22).

### Slide 8 · Previsão (escolha que grava, `aulaExtras.previsao`)
- **No lugar de «Talvez você esteja aqui» e «A crença que trava»** (I9). **Pergunta:** «A página 6 da Marina diz cerca de R$ 690 mil, sem a infraestrutura comum. Com tudo dentro e cotado, o número sobe, desce ou fica?» · «E passa do limite de cerca de R$ 870 mil?»
- **Opções:** Sobe e passa de R$ 870 mil · Sobe, mas fica abaixo de R$ 870 mil · Fica perto de R$ 690 mil · Desce. Sem certo ou errado aqui: «A resposta vem no Bloco 2.» A previsão volta no slide 31.
- **Fonte:** PLANO 5.3 item 5.

### Slide 9 · Bloco 1 · As sete partes do custo (abertura)
- **Molde:** `section.s.esc`.
- **Tela:** citação «"Não é quanto custa a cabana. É quanto custa *abrir a porta.*"» · «Pilar 6 · Pré-viabilidade» · lead (clique): «O nome técnico é CAPEX, do inglês capital expenditure: tudo o que se gasta uma vez para que o primeiro hóspede entre.»
- **Notas:** única vez em que a sigla é explicada; os cinco erros do Pilar 6 retomados com «No Pilar 6 você…», sem refazer.
- **Fonte:** P6 caps. 02 e 03; GUIA 3.1 e 5.2.

### Slide 10 · Do Pilar 6 para a 6A
- **Tela:** `h2` «A folha de oito linhas *vira sete partes*»; tabela, uma linha por clique: linhas 1 a 6 → Partes 2, 3, 4 e 5; linha 7 → Parte 1 (licença de operar na Parte 6); linha 8 → Parte 7 (% do subtotal, com regra de uso); infraestrutura comum «a cotar» → **entra** (Parte 2 e áreas comuns na Parte 3); «não estava» → Parte 6; giro somado e terreno fora → iguais.
- **Fonte:** PLANO 5.2 (caixa I3); P5 (o que não se constrói não se orça).

### Slide 11 · Dentro, ao lado, à parte
- **Tela:** três cartões: Dentro · As sete partes; Somado à parte · O capital de giro (custo de abrir a porta + giro = investimento total da fase um); Ao lado, sem somar · O terreno («fora da conta não quer dizer de graça»). Juros e captação: Pilar 7.
- **Fonte:** P6 cap. 02; PLANO 5.2 cap. 02.

### Slide 12 · As três origens
- **Tela:** Cotação escrita · Estimativa minha · Em branco; citação «"Uma linha em branco vale mais do que um número inventado."»; `p.sm` com «"A frase “não inclui” é a mais importante de qualquer proposta."» e «"Cotação de mais de noventa dias precisa ser refeita."»
- **Notas:** a ficha nunca põe valor no lugar do «Não sei».
- **Fonte:** P6; JC04 P09; VOL05 cap. 4.

### Slide 13 · As sete partes
- **Tela:** lista numerada em duas colunas: Projetos, licenças e documentação · Infraestrutura · Unidades e áreas comuns · Mobiliário e equipamentos · Enxoval, utensílios e suprimentos · Pré-abertura · Reserva do imprevisto.

### Slide 14 · Parte 1 · Projetos, licenças e documentação
- **Molde (14 a 20):** `section.s.parte` com `div.num-bg` (1 a 7), `p.k` «Parte N de 7», cartão «A pergunta-chave», cartão «O erro típico» e «O que entra».
- **Tela:** o que aprova o projeto e a obra? · erro: pôr aqui a licença de operar (vai para a Parte 6).
- **Fonte:** PLANO 5.2 cap. 04; R11 a R13.

### Slide 15 · Parte 2 · Infraestrutura
- **Tela:** a que distância está o ponto de energia, e para quantas unidades a rede é pensada? · erro: rede só para a fase um · citação A05 cap. 12.
- **Notas:** na página 6 era a infraestrutura comum «a cotar»; aqui entra. Refazer vala e caminho na fase dois é a forma mais cara de economizar.
- **Fonte:** PLANO 5.2 cap. 04; R11 a R14; P5.

### Slide 16 · Parte 3 · Unidades e áreas comuns
- **Tela:** quantos m² existem de verdade, com deck, apoio e áreas comuns? · erro: orçar só as unidades · estrutura pronta conta como unidade (na Planilha 1, aba FF&E).
- **Fonte:** PLANO 5.2 cap. 05; R9, R10, R20, R33.

### Slide 17 · Parte 4 · Mobiliário e equipamentos
- **Tela:** existe uma unidade-modelo completa, item por item? · erro: cortar a mobília no fim da obra.
- **Fonte:** PLANO 5.2 cap. 06; R17 a R19.

### Slide 18 · Parte 5 · Enxoval, utensílios e suprimentos
- **Tela:** você simulou um dia inteiro de operação? · erro: contar o enxoval duas vezes, ou nenhuma.
- **Fonte:** PLANO 5.2 cap. 06; R16, R28.

### Slide 19 · Parte 6 · Pré-abertura
- **Tela:** o que acontece entre a obra pronta e o primeiro hóspede? · erro: esquecer (ela não estava na página 6).
- **Fonte:** PLANO 5.2 cap. 07; R21.

### Slide 20 · Parte 7 · Reserva do imprevisto
- **Tela:** para quê, quem autoriza, como se registra, quando se confere? · erro: usá-la para pagar o que não estava no projeto · faixa de 10% a 15% sobre o subtotal das Partes 1 a 6, teto com primeira obra · citação A05 cap. 7.
- **Fonte:** PLANO 5.2 cap. 07; R22 a R25.

### Slide 21 · Quiz relâmpago · dentro, ao lado ou fora?
- **Interação:** seis cartões `.pq` que viram: jogo de lençol (Dentro · Parte 5), terreno (Ao lado), giro (Somado à parte), juros (Fora · Pilar 7), fotos do anúncio (Dentro · Parte 6), **rede de energia até as cinco posições** (Dentro · Parte 2; na página 6, estava à parte).

### Slide 22 · Quiz relâmpago · a reserva
- **Interação:** dois verdadeiro ou falso, um por clique: «No meio da obra, a Marina decide pôr um ofurô na crista. A reserva cobre.» (Falso: escopo novo é linha nova e decisão) · «A reserva que sobrar no fim da obra vira capital de giro.» (Verdadeiro).
- **Fonte:** P6 (o ofurô na crista); PLANO 7.3 (regra de uso).

### Slide 23 · Bloco 2 · A Marina abre a página 6
- **Tela:** selo «Exemplo ilustrativo»; três itens: 3 cabanas para casal, 38 m² + 16 m² de deck, abre com 3 e desenha para 5 · apoio de 30 m², deck leve na crista, caminho de cerca de 120 m, primeira obra · ponto de energia a 260 m, rede pensada para as 5. Caixa «No Pilar 6»: «"Antes de assinar, ela troca cada linha por cotação escrita, soma a infraestrutura comum do terreno e confere os dois limites."»
- **Fonte:** P3, P5, P6 cap. 07; PLANO 7.1 e 7.2.

### Slide 24 · De onde ela parte: a página 6
- **Tela:** tabela clique a clique: unidades prontas R$ 577.038,00 · licenças R$ 15.000,00 · reserva 10% R$ 57.703,80 · giro R$ 40.787,38 · **investimento total R$ 690.529,18** · infraestrutura comum «a cotar» · limite «até R$ 870.130,80». Rótulo da referência e «terreno fora da conta (R$ 600 mil)».
- **Notas:** 577.038 + 15.000 + 57.703,80 = 649.741,80; + 40.787,38 = 690.529,18. Bate. 8 × 108.766,35 = 870.130,80. Bate.
- **Fonte:** PLANO 7.1.

### Slide 25 · As seis partes, cotadas e estimadas
- **Tela:** selo dos dados fictícios; Partes 1 a 6 com valor e peso: 36.000 (4,6%) · 128.200 (16,2%) · 428.400 (54,2%) · 72.000 (9,1%) · 10.740 (1,4%) · 12.600 (1,6%) · **subtotal R$ 687.940**.
- **Notas:** pelas partes e pela origem (613.120 cotados + 74.820 estimados) = 687.940. Bate.
- **Fonte:** PLANO 7.3 e 7.4.

### Slide 26 · Da reserva ao limite
- **Tela:** subtotal R$ 687.940,00 · reserva a 10%, como na página 6, com o aviso da primeira obra: R$ 68.794,00 · reserva a 15%: R$ 103.191,00 · **custo de abrir a porta R$ 791.131,00** · giro, veio da página 6: R$ 40.787,38 · **investimento total R$ 831.918,38** · limite R$ 870.130,80 · **folga R$ 38.212,42**.
- **Notas:** 687.940 × 0,15 = 103.191; + 687.940 = 791.131; + 40.787,38 = 831.918,38; + 38.212,42 = 870.130,80. Bate.
- **Fonte:** PLANO 7.3 (Parte 7) e 7.4; P6 cap. 03 («subir para o teto da faixa»).

### Slide 27 · Mexa você · a reserva (calculadora + semáforo)
- **Interação:** `.sim[data-sim=reserva]`: subtotal (R$ 687.940), reserva (15%), primeira obra (Sim). Saídas: reserva, custo de abrir a porta, **investimento total com o giro da página 6** e **folga até o limite da página 6**, peso da reserva. Aviso: vermelho (0% ou abaixo de 10%, ou passou do limite), amarelo (abaixo de 15% com primeira obra; acima de 25%), verde. Botão «Voltar à conta da Marina»; tecla R.
- **Conferência:** 15% → R$ 103.191 · R$ 791.131 · R$ 831.918 · folga de R$ 38.212 · 13,0% (verde) · 10% com primeira obra → R$ 68.794 · R$ 756.734 (amarelo) · 20% → folga de R$ 3.815 · 21% → passa R$ 3.064 (vermelho).

### Slide 28 · Quanto do número tem papel?
- **Tela:** 39 linhas: 16 com cotação, 18 estimativas, 5 em branco · 41,0% das linhas e 89,1% do valor com cotação; as três maiores cotadas · régua Sonhador, **Estimador (a Marina)**, Calculista, Developer · faltam 4 linhas cotadas para a maioria; com as cinco em branco cotadas, Calculista.
- **Fonte:** PLANO 7.4 (linhas e cotações); régua do P6.

### Slide 29 · O número, lido de quatro jeitos
- **Tela:** custo por unidade R$ 263.710,33 · investimento por unidade (o custo por chave do Pilar 6) R$ 277.306,13 · custo por m², em 208 m², R$ 3.803,51 · obra (Partes 2 e 3) 70,4% do custo.
- **Notas:** na página 6, o custo por chave era R$ 230.176,39; sem alerta abaixo de 80%.
- **Fonte:** PLANO 7.4 (medidas).

### Slide 30 · O semáforo dos alertas
- **Interação:** seis cartões: reserva de 15% na primeira obra (verde) · rede para 5 (verde) · enxoval e utensílios = 14,9% da mobília (verde) · **pré-abertura = 2,3% da obra (vermelho, faltam R$ 15.230)** · **cotação da água com 135 dias (vermelho)** · **9 linhas com menos de três propostas (amarelo)**. Os três últimos são os alertas A11, A13 e A14 da ficha.
- **Fonte:** PLANO 7.4 (alertas); 6.3 e 6.4.

### Slide 31 · Página 6 × página 6A
- **Tela:** tabela clique a clique: entrou o que estava à parte ou não estava (+ R$ 208.600) · licenças (+ R$ 21.000) · reserva (+ R$ 45.487,20) · as seis linhas por cabana, com outro escopo (− R$ 133.698) · giro (0) · **total R$ 690.529,18 → R$ 831.918,38 (+ R$ 141.389,20)**. «A página 6 cobria 83,0% da 6A. Sobe, e fica abaixo do limite de R$ 870 mil.» Abaixo, a previsão do slide 8 («A sua previsão: … Foi isso.» ou «… a previsão errada também ensina.»).
- **Notas:** explicação de escopo, sem adjetivo. 208.600 + 21.000 + 45.487,20 − 133.698 = 141.389,20. Bate.
- **Fonte:** PLANO 7.4 (página 6 × página 6A) e 5.1 (regra de redação).

### Slide 32 · Cabe, mas a folga é fina
- **Tela:** folga R$ 38.212,42 · com a reserva de 15%, paga R$ 33.228,19 de linhas novas · pré-abertura até 5% da obra R$ 15.230,00 · sobra para as cinco linhas em branco R$ 17.998,19 · «As linhas em branco só podem aumentar a conta.»
- **Notas:** a sensibilidade do Mapa (CAPEX +20%) é a etapa seguinte; a 6A não a calcula nem antecipa o veredito; a decisão é do Pilar 7.
- **Fonte:** PLANO 7.4 (leitura do limite) e 7.8.

### Slide 33 · Quiz relâmpago · a ação de 30 dias
- **Interação:** escolha: **pedir cotação escrita das cinco linhas em branco** (licença ambiental, internet, segurança, licença de funcionamento, seguro do primeiro ano); prazo 27/12/2026; verificação: as cinco propostas lançadas na ficha.
- **Fonte:** PLANO 7.4 (ação sugerida) e 6.5.

### Slide 34 · Resumo · O 6A em cinco frases
- **Tela:** (1) A 6A não começa do zero: abre, linha por linha, a página 6 que você já fez. (2) Sete partes, cada gasto numa só; entra o que estava à parte: infraestrutura comum, áreas comuns e pré-abertura. (3) Cada número tem origem: cotação, estimativa ou em branco; uma linha em branco vale mais do que um número inventado. (4) A reserva vai sobre o subtotal das Partes 1 a 6, com regra de uso; na primeira obra, o teto da faixa. (5) Custo de abrir a porta + giro = investimento total, conferido contra o limite da página 6; o terreno fica ao lado.
- **Fonte:** GUIA I9; `pilar6-aula`, «O Pilar 6 em cinco frases».

### Slide 35 · A sua página 6A · critério de conclusão (escolha que grava, `respostas.d3`)
- **Tela:** «Pronto *para levar à página 6*»: os quatro critérios, um por clique; pergunta «Hoje, quantas linhas do seu projeto têm cotação escrita?» (A maioria · Algumas · Nenhuma).
- **Notas:** o selo não exige percentual mínimo de cotação nem estar dentro do limite.
- **Fonte:** PLANO 6.6.

### Slide 36 · A sua página 6A · o nome (`respostas.nome`)
- **Tela:** «O seu nome *na página 6A*», um campo, opcional. «Sem e-mail: esta ficha não envia nada, o PDF fica só com você.» **[a confirmar por Bruno: o curso pede nome e e-mail; aqui só o nome]**.
- **Fonte:** PLANO 5.3 item 9; I14.

### Slide 37 · A sua página 6A · a ficha embutida
- **Molde:** o encaixe `s.diag` da aula do Pilar 6: `iframe` com `../../pilar6a/` (`?turma=acompanhamento` quando a aula vier com esse parâmetro), carregado só ao chegar no slide e recarregado ao voltar; link «Abrir em tela cheia».
- **Tela:** «Faça agora · O seu CAPEX. O número da sua página 6, as linhas com cotação e o seu nome já estão na ficha. Preencha as sete partes e baixe a página 6A.»

### Slide 38 · Próximo · Planilha 1, Planilha 2 e a página 6 refeita
- **Tela:** lista: baixe a página 6A em PDF, na ficha · refaça a página 6 na ficha do Pilar 6, campo a campo, com o quadro «Como levar para a página 6» · Planilha 1 · Orçamento de Abertura (se preferir planilha) e Planilha 2 · Estudo de Massas e Viabilidade, aba Investimento, célula B5 · a sensibilidade do Mapa e, então, o Pilar 7. Caixa «Lembre»: «Salve o PDF da página 6A na pasta Meu Dossiê, ao lado da página 6. Esta ficha não envia nada: o PDF fica só com você.» Aviso: «No Pilar 7 você vai ver a Marina com o número da página 6 de referência, cerca de R$ 690 mil, porque ele foi escrito antes das cotações. Com a 6A, o investimento dela passa a ser cerca de R$ 832 mil, e o critério de R$ 870 mil continua de pé.» Botão «Abrir a ficha» → `../../pilar6a/`; aviso educativo.
- **Último botão da barra:** «Abrir a ficha ›» → `../../pilar6a/`.
- **Turma de acompanhamento:** o passo 2 vira «Leve a página 6A ao encontro do Pilar 6 e refaça a página 6 depois do comentário da equipe.»
- **Fonte:** PLANO 5.3 item 10, 7.8 (aviso do Pilar 7), 8 e 9; GUIA 5.9.

---

## 4. Citações literais usadas

| Slide | Citação | Fonte |
|---|---|---|
| 9 | "Não é quanto custa a cabana. É quanto custa abrir a porta." | Pilar 6 · Pré-viabilidade |
| 11 | "fora da conta não quer dizer de graça" | Pilar 6 · Pré-viabilidade |
| 12 | "Uma linha em branco vale mais do que um número inventado." | Pilar 6 · Pré-viabilidade |
| 12 | "A frase “não inclui” é a mais importante de qualquer proposta." | Jornada do COMO, Etapa 04, Passo 09 |
| 12 | "Cotação de mais de noventa dias precisa ser refeita." | Volume 05 · Investimento, cap. 4 |
| 15 | "Nunca desenhe um projeto que só funciona inteiro. Desenhe um organismo que cresce." | Volume A05 · Investimento, cap. 12 |
| 16 (notas) | "Corte metros quadrados no projeto. Nunca corte a experiência dentro deles." | Pilar 6 · Pré-viabilidade |
| 20 | "A contingência não é pessimismo. É maturidade." | Volume A05 · Investimento, cap. 7 |
| 23 | "Antes de assinar, ela troca cada linha por cotação escrita, soma a infraestrutura comum do terreno e confere os dois limites." | Pilar 6, cap. 07 |

## 5. Pendências
1. O nome sem e-mail (slide 36) e o selo sem percentual mínimo de cotação (slide 35): **a confirmar por Bruno** (PLANO, seção 12).
2. O valor que a ficha usa para «ainda não fiz a página 6» em `respostas.pagina6Total` não está fixado no PLANO; por isso a aula guarda essa resposta só em `aulaExtras.pagina6`. Se a ficha definir o valor, a aula pode passar a gravá-lo.
3. A aula antiga (`capex-aula/`) foi movida; as aulas do ClickMax que apontarem para ela precisam ser reapontadas na sessão de publicação (PLANO 10).

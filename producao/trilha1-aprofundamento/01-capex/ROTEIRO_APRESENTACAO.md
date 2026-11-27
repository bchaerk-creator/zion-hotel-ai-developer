# Aprofundamento do Pilar 6 · CAPEX · Roteiro da aula interativa

Status: roteiro para o construtor (27/11/2026). Nada foi construído, gravado ou publicado. O ClickMax não foi tocado.
Base: `PLANO.md` desta pasta (seções 1, 4, 5.2, 6.3, 6.4, 7 e 9) e o mapa de fontes do CAPEX (fora do repositório público; aqui só aparecem os códigos de fonte e as citações curtas autorizadas).
Molde: `docs/trilha1/apresentacao/pilar6-aula/index.html` e motor `docs/trilha1/apresentacao/_motor/deck.js` + `deck.css`.
Destino sugerido: `docs/trilha1/apresentacao/pilar6-capex/index.html` (`data-deck="t1-pilar6-capex"`, `data-titulo="Pilar 6 · Aprofundamento · CAPEX"`).
Saída da aula: a ficha **"Faça agora · O meu CAPEX"** em `docs/trilha1/capex/` (caminho pedido nesta rodada; o `PLANO.md` 5.4 fala em `docs/trilha1/pilar6-capex/`; o construtor confirma qual vale e ajusta o link do slide 34).

---

## 0. Regras que valem para todos os slides

- **Tamanho:** até cerca de 40 palavras na tela; o resto vai nas notas (`<aside>`). 34 slides, 17 a 19 minutos.
- **Sem sigla na tela.** "CAPEX" aparece só como nome da aula e da página 6A, sempre explicado como "o custo de abrir a porta". Nada de FF&E, OS&E, BDI, ITBI na tela. Os nomes na tela são "Mobiliário e equipamentos" e "Enxoval, utensílios e suprimentos".
- **Números:** só os do caso fictício dos Chalés do Ribeirão (PLANO, seção 7). Todo slide com número leva o selo `<span class="selo">Exemplo com dados fictícios. Não são preços de referência.</span>`. Nenhum preço de referência (nem da A05, nem do P6, nem da Planilha 1), nenhum número da Marina e nenhum número da Zion Bubble.
- **Percentuais** (reserva, enxoval ÷ mobília, pré-abertura ÷ obra, obra acima de 80%) aparecem sempre como "faixa de conferência citada pela fonte; não é preço nem regra fixa".
- **Sem promessa** de aprovação, crédito, parceria, retorno, ocupação, renda ou prazo de obra.
- **Fotos:** só da pasta `docs/trilha1/apresentacao/fotos/`, sem pessoas, e só no slide 33 ("de onde vem o método"), com legenda. Não usar `1c46550f59.jpg`: é ilustração de masterplan (render), não foto.
- **Interações usadas** (todas já existem no motor ou no molde do Pilar 6):
  - **escolha**: `.quiz.passo` com `.op` e `data-certa`, e `.exp` com a explicação (o clique seguinte revela);
  - **verdadeiro ou falso**: o mesmo `.quiz.passo`, com duas opções;
  - **marcar**: cartões `.pq` que viram (frente = item, verso = resposta), o aluno marca a resposta no chat ou no papel antes de virar;
  - **calculadora**: `.sim` com `input[type=range]`, `output`, `[data-r]` e `.aviso` (slide 24);
  - **semáforo**: cartões `.pq` coloridos no verso (verde, amarelo, vermelho) e o `.aviso` da calculadora (classes `ok`, `at` e uma classe vermelha a criar no CSS da aula, se o `deck.css` não tiver);
  - **perguntas que gravam** (`section.s.q` + objeto `DQ`, tipos `numero` e `escolha`), salvas no aparelho.
- **Rodapé educativo** (slide 34 e notas): "Material educativo. Não é orçamento, projeto nem estudo de viabilidade definitivo. Custos, licenças e impostos se confirmam com engenheiro, arquiteto, prefeitura e contador."

## 1. Mapa dos slides

| # | Bloco (`data-bloco`) | Função | Interação | Min |
|---|---|---|---|---|
| 1 | Abertura | título e promessa | — | 0,3 |
| 2 | Abertura · ECROI | **E** espelhar a situação | — | 0,7 |
| 3 | Abertura · O seu palpite | previsão | número que grava | 1,0 |
| 4 | Abertura · ECROI | **C** derrubar a crença que trava | — | 0,8 |
| 5 | Como funciona esta aula | mapa da aula | — | 0,4 |
| 6 | Problema · O preço que chegou | os cinco erros | — | 0,8 |
| 7 | Problema · Quiz relâmpago | — | verdadeiro ou falso | 0,4 |
| 8 | Conceito · Abrir a porta | a troca da pergunta | — | 0,5 |
| 9 | Conceito · Dentro, ao lado, à parte | o diagrama | — | 1,0 |
| 10 | Conceito · Quiz relâmpago 1 | classificar 5 itens | marcar (cartões) | 1,0 |
| 11 | Conceito · A origem de cada número | cotação, estimativa, em branco | — | 0,8 |
| 12 | Conceito · Quiz relâmpago | — | escolha | 0,4 |
| 13 | Os sete blocos | abertura do trecho | — | 0,3 |
| 14 a 20 | Bloco 1 a Bloco 7 | um slide por bloco | — | 0,6 cada |
| 21 | Bloco 7 · Quiz relâmpago 2 | a reserva | verdadeiro ou falso (2) | 0,6 |
| 22 | Exemplo · A Helena | premissas do caso | — | 0,5 |
| 23 | Exemplo · A conta | revelada clique a clique | — | 1,0 |
| 24 | Exemplo · Mexa você | subtotal × reserva | calculadora + semáforo | 1,2 |
| 25 | Exemplo · Como ler o número | palpite, por unidade, por m² | — | 0,8 |
| 26 | Exemplo · O quanto está cotado | linhas e régua | — | 0,6 |
| 27 | Exemplo · O semáforo | os alertas do exemplo | semáforo (cartões) | 1,0 |
| 28 | Exemplo · Quiz relâmpago 3 | a ação de 30 dias | escolha | 0,5 |
| 29 | Ferramenta · O que a ficha pede | as telas e o tempo | — | 0,6 |
| 30 | Ferramenta · Critério de conclusão | o selo | escolha que grava | 0,6 |
| 31 | Fechamento · ECROI | **R** reencadrar | — | 0,5 |
| 32 | Fechamento · ECROI | **O** o caminho | — | 0,6 |
| 33 | Fechamento · ECROI | **I** resultado educacional + de onde vem o método | — | 0,5 |
| 34 | Faça agora | chamada para a ficha | botão | 0,3 |

Total: cerca de 18 minutos.

---

## 2. Slide a slide

### Slide 1 · Abertura
- **Molde:** `section.s.esc.sem-topo` (fundo musgo, sem foto), logo claro no topo.
- **Tela:**
  - `p.k`: Pilar 6 · Aprofundamento
  - `h1`: CAPEX<br><i>Quanto custa o seu projeto inteiro</i>
  - `p.lead`: Aprenda o passo a passo para calcular o custo de abrir a porta, bloco por bloco e com a origem de cada número, antes de assinar qualquer obra.
- **Notas:** 20 s. "Esta aula aprofunda uma linha da página 6: o custo de abrir a porta. No fim, você abre a ficha O meu CAPEX e sai com a página 6A do seu Dossiê." Não prometa número certo: a primeira versão sai com estimativas e linhas em branco, e isso é o esperado.
- **Fonte:** promessa do PLANO, seção 1; expressão "abrir a porta" do P6 cap. 02.

### Slide 2 · ECROI · Espelhar
- **Molde:** `section.s` com `ul.lista`, itens `.f` (um por clique).
- **Tela:**
  - `p.k`: Talvez você esteja aqui
  - `h2`: Você tem um número. <i>E uma dúvida.</i>
  - `li.f`: Um construtor falou um preço por unidade. Você multiplicou.
  - `li.f`: A família pergunta: "quanto vai custar tudo?"
  - `li.f`: Você não é engenheiro, e tem medo de esquecer alguma coisa.
- **Notas:** 40 s. Espelhe sem julgar: quase todo mundo começa assim, pelo preço da unidade. "Se você já opera e vai ampliar, troque construtor por fornecedor da nova unidade. Se cuida do imóvel de outra pessoa, pense no projeto do dono." Peça que guardem a dúvida: ela é o motivo da aula.
- **Fonte:** elaboração própria a partir do erro comum "planejar pelo orçamento do construtor" (JC01 P02, JC02 P11, JC04 P09) e dos públicos do PLANO, seção 2.

### Slide 3 · O seu palpite (previsão)
- **Molde:** `section.s.q` com `data-q="palpite"`; objeto em `DQ`:
  - `tipo: "numero"`, `unidade: "R$"`, `caminho: ["aulaExtras","palpite"]`, `curto: "O meu palpite"`;
  - `pergunta`: "Antes de qualquer conta: quanto custa abrir a porta da sua fase um?"
  - `explica`: "Escreva o número que está na sua cabeça hoje, sem pesquisar. A data fica gravada. No fim, a ficha compara o palpite com a conta."
  - `ns`: "Não tenho nenhum número ainda"; `ondeCurto`: "escrever o primeiro palpite na ficha O meu CAPEX";
  - `porque`: "Comparar o palpite com a conta mostra o tamanho do que ficou de fora. A diferença ensina mais do que o número."
- **Interação:** número que grava (não há resposta certa). Feedback fixo depois de gravar: "Guardado, com a data de hoje. Você vai ver esse número de novo no fim."
- **Notas:** 1 min. Dê 30 segundos de silêncio. Quem não tem número marca "não tenho": é uma resposta honesta. **Para o construtor:** se a ficha `docs/trilha1/capex/` ler `zion-t1-pilar6a.respostas.palpite`, gravar também lá (com `dataPalpite`), para o aluno não digitar duas vezes. **TODO:** confirmar o nome do campo com quem constrói a ficha.
- **Fonte:** R2 (A05 cap. 1 e 2; P6 cap. 01; F01 cap. 1).

### Slide 4 · ECROI · A crença que trava
- **Molde:** `section.s.esc`, `p.citacao` + `p.lead.f`.
- **Tela:**
  - `p.k`: A crença que trava
  - `h2`: "Só vou ter número <i>quando alguém me der o preço."</i>
  - `p.lead.f`: Você não precisa saber preço. Precisa saber a lista do que existe até o primeiro hóspede, e de onde vem cada número.
  - `p.citacao.f`: "Uma linha em branco vale mais do que um número inventado."
- **Notas:** 50 s. A crença tem duas formas: "preciso de um preço de referência" e "não sou técnico, não consigo orçar". As duas paralisam. Nesta aula não existe tabela de preço: existe a lista, a cotação escrita e a linha em branco, declarada. O preço vem do fornecedor; a lista e a origem são suas. Cite a fonte da frase: P6, capítulo 00.
- **Fonte:** citação literal P6 cap. 00; R3 (P6 cap. 02); lacuna 1 do PLANO, seção 11 (sem preço de referência).

### Slide 5 · Como funciona esta aula
- **Molde:** `section.s` com `div.grid.g3` de `div.card`.
- **Tela:**
  - `h2`: Três passos <i>e uma página</i>
  - card 1 · **O que entra e o que fica à parte** · O custo de abrir a porta, o giro e o terreno.
  - card 2 · **Os sete blocos** · Um por um, com a pergunta-chave e o erro típico.
  - card 3 · **A conta da Helena** · Um caso fictício, do palpite à ação de 30 dias.
  - `p.sv` (dica): Tenha à mão a sua página 6 do Pilar 6 e o seu Masterplan do Pilar 5.
- **Notas:** 25 s. Cerca de 18 minutos. No fim, a ficha "Faça agora · O meu CAPEX" gera a página 6A.
- **Fonte:** PLANO, seções 4 e 5.2.

### Slide 6 · O preço que chegou não é o projeto
- **Molde:** `section.s` com `ol.lista.num`, itens `.f`.
- **Tela:**
  - `p.k`: Os cinco erros do orçamento amador
  - `h2`: O preço que chegou <i>não é o projeto</i>
  - 1 · Orçar só as unidades, sem áreas comuns, apoio e infraestrutura.
  - 2 · Usar o custo do metro quadrado de outra região ou de outro ano.
  - 3 · Esquecer o enxoval, os utensílios e os suprimentos.
  - 4 · Tratar a reserva do imprevisto como opcional.
  - 5 · Esquecer a pré-abertura.
- **Notas:** 50 s. Leia um por clique e pergunte no chat: "qual destes você já cometeu?". O Pilar 6 troca o quinto por "esquecer o caixa dos primeiros meses": os dois cabem aqui, o giro aparece no slide 9.
- **Fonte:** A05 cap. 2; P6 cap. 01; F01 cap. 2.

### Slide 7 · Quiz relâmpago · verdadeiro ou falso
- **Molde:** `section.s` com `div.quiz.passo`.
- **Tela:**
  - `p.q`: "Se eu orçar bem as unidades, o resto é detalhe."
  - `.op` Verdadeiro
  - `.op[data-certa]` Falso
  - `p.exp`: Falso. As unidades são só uma parte. Infraestrutura, áreas comuns, mobília, enxoval, pré-abertura e reserva também custam. "O amador orça o chalé. O developer orça o que faz o chalé funcionar."
- **Notas:** 25 s. Letra no chat, depois clique para revelar. Fonte da frase: A05, capítulo 4.
- **Fonte:** citação literal A05 cap. 4; mapa 1.2 (todas as fontes concordam que o preço da unidade não é o investimento).

### Slide 8 · Abrir a porta
- **Molde:** `section.s.esc`, `p.citacao` + `p.lead.f`.
- **Tela:**
  - `p.k`: Então troque a pergunta
  - `p.citacao`: "Não é quanto custa a cabana. É quanto custa <i>abrir a porta.</i>"
  - `p.lead.f`: CAPEX é o nome técnico desse custo: tudo o que se gasta uma vez para que o primeiro hóspede entre.
- **Notas:** 30 s. Esta é a única vez em que a sigla é explicada em voz alta. Daqui para a frente, diga "o custo de abrir a porta". Fonte da frase: P6, capítulo 02.
- **Fonte:** citação literal P6 cap. 02; R1 (P6 cap. 02; A05 cap. 1).

### Slide 9 · Dentro, ao lado, à parte
- **Molde:** `section.s` com `div.grid.g3` (ou três colunas do diagrama), cada card `.f`.
- **Tela:**
  - `h2`: Dentro, ao lado, <i>à parte</i>
  - card **Dentro** · Os sete blocos = o custo de abrir a porta da fase.
  - card **Somado à parte** · O capital de giro. Custo de abrir a porta + giro = investimento total.
  - card **Ao lado, sem somar** · O terreno. É capital empregado: "fora da conta não quer dizer de graça".
  - `p.sm.f`: Juros e custo de captar o dinheiro ficam fora desta conta: são do Pilar 7.
- **Notas:** 1 min. As fontes divergem sobre giro e terreno; a aula segue a regra do Pilar 6: giro dentro do investimento, terreno fora, anotado à parte. Se o terreno ainda vai ser comprado, escritura, imposto de transmissão e registro são perguntas para o contador, sem número aqui. O giro precisa estar no banco no dia da abertura, em conta separada.
- **Fonte:** R26 (F01 cap. 1 e 2; P6 cap. 02 e 06), R27 (A05 cap. 2; P6 cap. 02; F01 cap. 2); citação literal P6 cap. 02; lacuna 10 do mapa (juros no Pilar 7).

### Slide 10 · Quiz relâmpago 1 · marcar: dentro, ao lado ou fora
- **Molde:** `section.s` com `div.grid.g3` (5 cartões `.pq.passo`; frente = item, verso = resposta). Cada clique vira um cartão.
- **Tela:**
  - `p.k`: Quiz relâmpago · marque antes de virar
  - `h2`: Dentro, ao lado <i>ou fora?</i>
- **Cartões (frente → verso):**
  1. Jogo de lençol e toalhas → **Dentro**, bloco 5 (enxoval, utensílios e suprimentos).
  2. O terreno, que já é seu → **Ao lado, sem somar**: capital empregado.
  3. O capital de giro → **Somado à parte**: entra no investimento total.
  4. Juros do empréstimo da obra → **Fora desta conta**: Pilar 7.
  5. Fotos do anúncio → **Dentro**, bloco 6 (pré-abertura).
- **Notas:** 1 min. Peça que escrevam D, A ou F para os cinco antes de virar. O erro mais comum é somar o terreno, ou esquecer o giro. O exercício E3 do caderno tem doze itens.
- **Fonte:** PLANO 5.3 (E3); R26, R27; lacuna 10 do mapa.

### Slide 11 · A origem de cada número
- **Molde:** `section.s.esc` com `div.grid.g3` + `p.citacao.f` + `p.sm.f`.
- **Tela:**
  - `p.k`: Ao lado de cada linha, de onde veio o número
  - `h2`: Três origens. <i>Nenhuma tabela de preço.</i>
  - card 1 · **Cotação escrita** · Com especificação, data e o que não inclui.
  - card 2 · **Estimativa minha** · Entra na soma, mas conta como sem cotação.
  - card 3 · **Em branco** · Vale zero e aparece como risco. Vira tarefa.
  - `p.citacao.f`: "A frase “não inclui” é a mais importante de qualquer proposta."
  - `p.sm.f`: "Cotação de mais de noventa dias precisa ser refeita."
- **Notas:** 50 s. Três propostas com a mesma especificação: material, medidas, quantidade, frete, instalação, entulho, prazo e garantia. O mesmo pacote para todos. A mais barata só ganha se o escopo for igual. Fontes das frases: Jornada do COMO, Etapa 04, Passo 09; e Volume 05, capítulo 4. **A confirmar por Bruno:** a origem "estimativa minha" (PLANO, 12.4); se ele preferir a regra estrita, o card 2 sai e ficam duas origens.
- **Fonte:** R3 (P6 cap. 02), R5 (F05 passo 2; JC04 P09), R6 (JC04 P09), R7 (JC04 P01 e P09), R8 (VOL05 cap. 4 e 5); citações literais JC04 P09 e VOL05 cap. 4.

### Slide 12 · Quiz relâmpago · escolha
- **Molde:** `div.quiz.passo`.
- **Tela:**
  - `p.q`: A proposta mais barata para o acesso não inclui o frete nem a retirada do entulho. O que você faz?
  - `.op` Fecho com ela: é a mais barata.
  - `.op[data-certa]` Peço a todos a mesma especificação e a lista do que não inclui, e comparo de novo.
  - `.op` Faço a média das três propostas.
- **`p.exp`:** Proposta que deixa itens de fora não é mais barata: é outra coisa. Compare três com a mesma especificação. Média de escopos diferentes não é número.
- **Notas:** 25 s.
- **Fonte:** R5, R6 (JC04 P09); erro comum "comparar cotações com escopos diferentes" (F05 passo 2; JC04 P09; VOL06 cap. 6).

### Slide 13 · Os sete blocos
- **Molde:** `section.s.esc` com `ol.lista.num` (7 itens `.f`, em duas colunas).
- **Tela:**
  - `p.k`: O custo de abrir a porta, em sete blocos
  - `h2`: Na ordem <i>de quem vai construir</i>
  - 1 Projetos, licenças e documentação · 2 Infraestrutura · 3 Unidades e áreas comuns · 4 Mobiliário e equipamentos · 5 Enxoval, utensílios e suprimentos · 6 Pré-abertura · 7 Reserva do imprevisto
- **Notas:** 20 s. Cada item numa linha só, em um bloco só. Os próximos sete slides trazem, para cada bloco, a pergunta-chave e o erro típico.
- **Fonte:** mapa, seção 10 (ordem recomendada); PLANO 6.1; R28 (P6 cap. 02; F01 cap. 4).

### Slides 14 a 20 · Um slide por bloco
Molde comum: `section.s.bloco` com `data-num` (o número grande ao fundo), `p.k` = "Bloco N de 7", `h2` = nome do bloco, dois cards `.f`: **A pergunta-chave** e **O erro típico**, e `p.sm.f` com "O que entra".

#### Slide 14 · Bloco 1 · Projetos, licenças e documentação
- **Pergunta-chave:** O que aprova o projeto e a obra?
- **Erro típico:** Pôr aqui a licença de operar. Ela vai para a pré-abertura.
- **O que entra:** arquitetura; engenharias; levantamento do terreno; aprovações e taxas da prefeitura; licença ambiental, se houver.
- **Notas:** 35 s. O que vale de licença no seu terreno, quem confirma é a prefeitura e o arquiteto; se houver dúvida, o advogado.
- **Fonte:** F01 (licença de projeto e obra aqui, de operação na pré-abertura; mapa 1.3, item 3); PLANO 6.1; mapa 7.2.

#### Slide 15 · Bloco 2 · Infraestrutura
- **Pergunta-chave:** A que distância está o ponto de energia? E para quantas unidades a rede é pensada?
- **Erro típico:** Fazer a rede só para a fase um e refazer na fase dois.
- **`p.citacao.f`** (menor, 44 px): "Nunca desenhe um projeto que só funciona inteiro. Desenhe um organismo que cresce."
- **O que entra:** acesso e caminhos, energia, água, esgoto e tratamento, drenagem, internet, estacionamento, ligações de cada unidade.
- **Notas:** 45 s. Infraestrutura se orça por distância e capacidade, não por unidade. Antes de cotar, as perguntas do terreno: distância da energia, água (vazão, poço, outorga), fundação, acesso de caminhão na chuva, declividade, prazo de licença. A distância até o ponto de energia, a concessionária informa (confirme com a sua). Dimensione para o projeto completo, construa a rede uma vez e abra por fases. Fonte da frase: A05, capítulo 12.
- **Fonte:** R11, R12 (P6 cap. 03), R13 (A05 cap. 4), R14 (A05 cap. 12; P6 cap. 04; F01 cap. 6); citação literal A05 cap. 12.

#### Slide 16 · Bloco 3 · Unidades e áreas comuns
- **Pergunta-chave:** Quantos metros quadrados existem de verdade, contando apoio, deck e lavanderia?
- **Erro típico:** Orçar só os chalés. Área comum também custa.
- **O que entra:** área construída total × custo do metro quadrado cotado na sua região e no seu ano; deck; apoio e lavanderia; recepção, se houver.
- **`p.sm.f`:** Estrutura pronta (bolha, domo, cabana pré-fabricada) conta como unidade. Confirme por escrito se frete, fundação e montagem estão incluídos.
- **Notas:** 40 s. Nunca use custo de metro quadrado de outra região ou de outro ano. Se a conta passar do que você pode: "Corte metros quadrados no projeto. Nunca corte a experiência dentro deles." (A05, capítulo 5). Em imóvel pronto, este bloco vira "Adequação e reforma". **A confirmar por Bruno:** estrutura pronta como unidade (PLANO, 12.7).
- **Fonte:** R9 (A05 cap. 2 e 4; F01 cap. 2), R10 (A05 cap. 4; P6 cap. 03), R20, R33 (B06 pilar 5); citação literal A05 cap. 5.

#### Slide 17 · Bloco 4 · Mobiliário e equipamentos
- **Pergunta-chave:** Já existe uma unidade-modelo completa, item por item?
- **Erro típico:** Cortar a mobília no fim da obra porque o caixa apertou, ou comprar tarde e abrir com o que tinha na loja.
- **O que entra:** cama e colchão, mobiliário, iluminação, cozinha compacta e eletrodomésticos, banheiro; equipamentos gerais, como os da lavanderia.
- **Notas:** 35 s. Monte a unidade-modelo antes de comprar as demais; cote em lote; compre com antecedência pelo prazo de fornecimento.
- **Fonte:** R19 (A05 cap. 5; P6 cap. 03; F01 cap. 4); mapa, seção 4 (cortar e comprar tarde, A05 cap. 5).

#### Slide 18 · Bloco 5 · Enxoval, utensílios e suprimentos
- **Pergunta-chave:** Você simulou um dia inteiro de operação, objeto por objeto?
- **Erro típico:** Contar o enxoval duas vezes, ou nenhuma.
- **O que entra:** três jogos por cama (um em uso, um na lavanderia, um no estoque); utensílios; as listas de governança, cozinha, recepção, manutenção e segurança.
- **Notas:** 35 s. Se a cotação da mobília já trouxe enxoval, não some de novo. A ficha pede a confirmação "o enxoval não está na cotação do mobiliário".
- **Fonte:** R17 (A05 cap. 6; P6 cap. 03; PL1; F05), R18 (A05 cap. 6), R28 (P6 cap. 02; F01 cap. 4).

#### Slide 19 · Bloco 6 · Pré-abertura
- **Pergunta-chave:** O que precisa acontecer entre a obra pronta e o primeiro hóspede?
- **Erro típico:** Esquecer. É o quinto erro do orçamento amador.
- **O que entra:** licença de funcionamento e cadastros; fotos e site; identidade e lançamento; treinamento e contratação; seguro do primeiro ano; abertura de teste.
- **Notas:** 35 s. Licença de operar mora aqui, não no bloco 1. Seguro do primeiro ano entra como linha, sem regra de valor nas fontes.
- **Fonte:** R21 (A05 cap. 2 e 7; F01 cap. 2 e 4); F05 (seguro); PLANO 6.1 e lacuna 4.

#### Slide 20 · Bloco 7 · Reserva do imprevisto
- **Pergunta-chave:** Para quê, quem autoriza, como se registra e quando se confere?
- **Erro típico:** Tratar a reserva como opcional, ou usá-la para pagar o que não estava no projeto.
- **`p.sm.f`:** Faixa de conferência citada pelas fontes: 10% a 15% sobre a soma dos blocos 1 a 6. Primeira obra ou fator de risco: o teto ou acima. Imóvel pronto: régua de reforma. Não é regra fixa.
- **`p.citacao.f`** (44 px): "A contingência não é pessimismo. É maturidade."
- **Notas:** 45 s. Contingência é o nome técnico da reserva. Fatores de risco: território remoto, sistema construtivo novo para a equipe, itens importados, licenciamento em área sensível, prazo apertado pela temporada. Em reforma, a Jornada do COMO cita de 15% a 25%. A reserva nunca é zero. Fonte da frase: A05, capítulos 1 e 7. **A confirmar por Bruno:** base da reserva no subtotal dos blocos 1 a 6 (PLANO, 12.8).
- **Fonte:** R22 (F01 cap. 5; JC02 P11; A05 cap. 7), R24 (P6 cap. 03; F01 cap. 5); PLANO 6.3; JC04 P04; citação literal A05 cap. 1 e 7.

### Slide 21 · Quiz relâmpago 2 · verdadeiro ou falso sobre a reserva
- **Molde:** dois `div.quiz.passo` no mesmo slide (o motor revela um por clique).
- **Pergunta 1** · `p.q`: "No meio da obra, decidi pôr um ofurô em cada chalé. A reserva cobre."
  - `.op` Verdadeiro · `.op[data-certa]` Falso
  - `p.exp`: Falso. A reserva cobre o imprevisto da obra orçada: solo, chuva, reajuste, exigência da licença. Ofurô novo é escopo novo: vira linha nova e decisão.
- **Pergunta 2** · `p.q`: "A reserva que sobrar no fim da obra vira capital de giro."
  - `.op[data-certa]` Verdadeiro · `.op` Falso
  - `p.exp`: Verdadeiro. O que sobra da reserva reforça o caixa da abertura. Também não cobre linha esquecida nem o caixa dos primeiros meses.
- **Notas:** 35 s.
- **Fonte:** R23 (P6 cap. 03; F01 cap. 5; VOL05 cap. 4), R25 (JC02 P11); PLANO 5.3 (E3, ofurô).

### Slide 22 · A Helena (o caso)
- **Molde:** `section.s` com `span.selo` + `div.grid.g2` (lista de premissas + `p.sv`).
- **Tela:**
  - `span.selo`: Exemplo com dados fictícios. Não são preços de referência.
  - `h2`: Os Chalés <i>do Ribeirão</i>
  - `li.f`: Terreno herdado. Projeto completo: 6 chalés. Fase um: 4.
  - `li.f`: Primeira obra da Helena. Rede pensada para os 6.
  - `li.f`: Ponto de energia a 180 m, informado pela concessionária.
  - `p.sv.f`: **O palpite:** R$ 700.000, 4 × R$ 175.000 que um construtor falou.
- **Notas:** 30 s. Helena é personagem fictícia; os números foram inventados para a aula e não servem como preço. Nenhum município. **A confirmar por Bruno:** nome do caso e da personagem (PLANO, 12.5).
- **Fonte:** PLANO, seção 7 (exemplo próprio, dados fictícios).

### Slide 23 · A conta, clique a clique
- **Molde:** `section.s` com `span.selo` + `table.t` (cada `tr.f` aparece num clique; a linha final com `data-foco`).
- **Tela:**
  - `span.selo`: Exemplo com dados fictícios. Não são preços de referência.
  - `h2`: A conta <i>da Helena</i>

| Linha (`tr.f`) | Valor |
|---|---|
| 1 · Projetos, licenças e documentação | R$ 40.000 |
| 2 · Infraestrutura | R$ 170.000 |
| 3 · Unidades e áreas comuns | R$ 682.000 |
| 4 · Mobiliário e equipamentos | R$ 85.800 |
| 5 · Enxoval, utensílios e suprimentos | R$ 11.700 |
| 6 · Pré-abertura | R$ 21.000 |
| **Soma dos blocos 1 a 6** | **R$ 1.010.500** |
| 7 · Reserva do imprevisto, 15% | R$ 151.575 |
| **Custo de abrir a porta da fase** | **R$ 1.162.075** |
| Capital de giro, da página 6 | R$ 45.000 |
| **Investimento total** | **R$ 1.207.075** |
| Terreno, ao lado e sem somar | R$ 300.000 |

- **Notas:** 1 min. Revele devagar. A Helena começou com 12% de reserva, viu o aviso da primeira obra e subiu para 15% (o próximo slide deixa o aluno mexer). O giro vem da página 6 dela: 3 meses × R$ 15.000, fictício. O terreno aparece, mas não é somado.
- **Fonte:** PLANO, seção 7 (conta e conferência dupla).

### Slide 24 · Mexa você · a reserva (calculadora + semáforo)
- **Molde:** `section.s` com `div.sim[data-sim="reserva"]` em duas colunas (`.ctl` e `.res`), botões `.reset` e `span.ajustado`, como o slide "A margem" do Pilar 6.
- **Tela:**
  - `p.k`: Mexa você · a reserva · `span.selo`: Começa na conta da Helena · dados fictícios
  - `h2`: Quanto a reserva <i>muda o número?</i>
  - Controles:
    - `Soma dos blocos 1 a 6` · `input[type=range] name="sub" min="100000" max="3000000" step="500" value="1010500"` · `output data-fmt="brl"`
    - `Reserva do imprevisto` · `input[type=range] name="pct" min="0" max="35" step="1" value="15"` · `output data-fmt="pct0"`
    - `Primeira obra ou fator de risco?` · `select name="risco"` com `1` = Sim (padrão) e `0` = Não
  - Resultados: `Reserva` (`data-r="res"`, brl) · `Custo de abrir a porta` (`data-r="capex"`, brl, linha `.tot`) · `Peso da reserva no custo` (`data-r="peso"`, pct) · `div.aviso[data-aviso]`
  - Botão `.reset`: Voltar à conta da Helena
- **Função para o construtor** (`ZD.sims.reserva`):
  - `res = sub × pct / 100`; `capex = sub + res`; `peso = pct / (100 + pct) × 100`;
  - `_aviso` (semáforo, na ordem):
    - `pct = 0` → vermelho: "A reserva nunca é zero."
    - `pct < 10` → vermelho: "Abaixo da faixa citada pelas fontes (10% a 15%)."
    - `pct < 15` e `risco = 1` → amarelo (`at`): "Com primeira obra ou fator de risco, a fonte pede o teto ou acima."
    - `pct > 25` → amarelo (`at`): "Acima de todas as faixas citadas: confira se a reserva não está cobrindo linha esquecida ou escopo novo."
    - demais → verde (`ok`): "Dentro da faixa citada. Agora escreva a regra de uso em quatro linhas."
- **Respostas de conferência** (para as notas e para o teste do construtor):
  - 15% → reserva R$ 151.575; custo R$ 1.162.075; peso 13,0%; verde.
  - 12% com primeira obra → reserva R$ 121.260; custo R$ 1.131.760; amarelo.
  - 8% (exercício E4) → reserva R$ 80.840; custo R$ 1.091.340; vermelho. Diferença para 15%: R$ 70.735.
- **Notas:** 1 min 10 s. Peça que um aluno diga um percentual e mexa ao vivo. Mostre os 12% da Helena (amarelo) e volte aos 15%. Repita: a faixa é de conferência, não regra fixa, e quem valida a reserva do seu projeto é o engenheiro. A tecla R volta ao exemplo.
- **Fonte:** PLANO 6.2 (fórmula), 6.3 e 6.4 (A3z, A3, A4, A5), 5.3 (E4) e seção 7.

### Slide 25 · Como ler o número
- **Molde:** `section.s` com `span.selo` + `div.conta` (linhas `.eq.f`).
- **Tela:**
  - `span.selo`: Exemplo com dados fictícios. Não são preços de referência.
  - `h2`: O número, <i>lido de quatro jeitos</i>
  - `.eq.f` O palpite cobria · 60,2% da conta · faltavam R$ 462.075
  - `.eq.f` Custo por unidade, sem giro e sem terreno · R$ 290.518,75
  - `.eq.f` Investimento por unidade, com o giro · R$ 301.768,75
  - `.eq.f` Custo por m², em 188 m² · R$ 6.181,25
- **Notas:** 50 s. O palpite não estava errado por descuido: ele cobria só o que foi pedido. As duas medidas por unidade têm nome diferente; diga sempre qual está usando. A segunda é a que o Pilar 6 chama de custo por chave. A obra (blocos 2 e 3) é 73,3% do custo: abaixo de 80%, sem alerta. Acima de 80%, a fonte diz que provavelmente faltou algo. **A confirmar por Bruno:** as duas medidas por unidade (PLANO, 12.9).
- **Fonte:** PLANO 6.2 e seção 7; R29 (A05 cap. 3; F01 cap. 6), R30 (P6 cap. 04; F01 cap. 6), R31 (PL1).

### Slide 26 · O quanto está cotado
- **Molde:** `section.s` com `span.selo`, `div.regua` (4 degraus) e `ul.lista`.
- **Tela:**
  - `span.selo`: dados fictícios
  - `h2`: Quanto do número <i>tem papel?</i>
  - `li.f`: 32 linhas: 17 com cotação, 10 estimativas, 5 em branco.
  - `li.f`: 53,1% das linhas e 94,7% do valor têm cotação. As três maiores linhas estão cotadas.
  - `div.regua.f`: Sonhador · Estimador · **Calculista** (a Helena) · Developer
- **Notas:** 35 s. No diagnóstico, a Helena estava em Estimador; com a ficha, chegou a Calculista: a maioria das linhas cotada e as três maiores com cotação. O degrau Developer pede cronograma de desembolso e captação: fica para o Pilar 7. **A confirmar por Bruno:** régua com três degraus na ficha (PLANO, 12.12).
- **Fonte:** régua de maturidade (A05 cap. 1; P6 cap. 02, sem ™); critério de Calculista do F01 cap. 1 (R4); PLANO, seção 7.

### Slide 27 · O semáforo dos alertas do exemplo
- **Molde:** `section.s` com `span.selo` + `div.grid.g3` de 6 cartões `.pq.passo`. Frente: a situação. Verso: a cor (fundo verde, amarelo ou vermelho) e a leitura. O aluno vota a cor no chat antes de cada virada.
- **Tela:**
  - `p.k`: Semáforo · vote a cor antes de virar
  - `h2`: O que a ficha <i>avisou à Helena</i>
- **Cartões (frente → verso):**
  1. Reserva de 15% na primeira obra → **Verde**: dentro da faixa citada.
  2. Rede dimensionada para 6, o projeto completo → **Verde**: construída uma vez.
  3. Enxoval e utensílios = 13,6% da mobília → **Verde**: dentro da faixa citada de 10% a 15%.
  4. Pré-abertura = 2,5% da obra → **Vermelho**: abaixo da faixa citada de 5% a 10%. Revisar o bloco 6.
  5. Cotação do poço com 130 dias → **Vermelho**: mais de 90 dias, refazer.
  6. 10 linhas com menos de três propostas → **Amarelo**: completar até três com a mesma especificação.
- **Notas:** 1 min. Na ficha, os três alertas que aparecem são justamente estes: pré-abertura, cotação vencida e cotações incompletas. As cores do semáforo são uma leitura da aula (elaboração própria): verde = dentro; amarelo = completar; vermelho = corrigir antes de mostrar o número a alguém. Todas as faixas são de conferência, não preço.
- **Fonte:** PLANO 6.3, 6.4 (A11, A13, A14) e seção 7 (conferências e alertas na ordem); R8, R14, R16, R21.

### Slide 28 · Quiz relâmpago 3 · a ação de 30 dias
- **Molde:** `div.quiz.passo` + `span.selo` (dados fictícios).
- **Tela:**
  - `p.q`: Qual é a ação de 30 dias da Helena?
  - `.op` Subir a reserva para 25%, para garantir.
  - `.op[data-certa]` Pedir cotação escrita das cinco linhas em branco: licença ambiental, internet, segurança, licença de funcionamento e seguro do primeiro ano.
  - `.op` Começar a obra e cotar o resto durante.
  - `.op` Trocar as estimativas por preços achados na internet.
- **`p.exp`:** Linha em branco vem primeiro: é o que ainda pode crescer a conta. Prazo: 27/12/2026. Como verificar: as cinco propostas, com data e escopo, lançadas na ficha.
- **Notas:** 30 s. A ficha sugere a ação pela primeira situação verdadeira numa ordem fixa: bloco em branco, rede, linhas em branco, degrau, cotações vencidas, faixas. Reserva alta não substitui cotação, e preço de internet não é cotação escrita.
- **Fonte:** PLANO 6.5 (ordem 3) e seção 7 (ação sugerida).

### Slide 29 · O que a ficha pede
- **Molde:** `section.s` com `div.fases` (botões `.bt` em sequência) ou `ol.lista.num` em duas colunas.
- **Tela:**
  - `p.k`: Faça agora · O meu CAPEX
  - `h2`: Uma pergunta <i>por tela</i>
  - Sequência: A sua situação · O palpite · A fase · Blocos 1 a 6 · A reserva e a regra de uso · Giro e terreno · Resultado em cinco partes · Ação de 30 dias · PDF da página 6A
  - `p.sv.f`: A primeira passada leva de 30 a 45 minutos. Ela sai com estimativas e linhas em branco. As cotações chegam depois, no tempo dos fornecedores.
- **Notas:** 35 s. A ficha salva no aparelho: volte a cada cotação que chegar e refaça o PDF. Ela nunca põe preço de referência; o botão de exemplo mostra a Helena, com dados fictícios. Quem já tem cotação da maioria das linhas pode pular o tutorial.
- **Fonte:** PLANO 4 (etapas 4 a 6), 5.4 (telas) e 2 (atalho por expertise).

### Slide 30 · Critério de conclusão (escolha que grava)
- **Molde:** `section.s` com `ul.lista` curta + pergunta `section.s.q` incorporada (`data-q="cotadas"`) ou slide próprio, se o construtor preferir (então a aula fica com 35 slides).
- **Tela:**
  - `h2`: Pronto <i>para levar à página 6</i>
  - `li.f`: Toda linha com origem escolhida, em todos os blocos.
  - `li.f`: Reserva maior que zero, com a regra de uso nas quatro linhas.
  - `li.f`: Rede: para quantas unidades. Giro e terreno respondidos.
  - `li.f`: Ação de 30 dias com prazo, e o PDF baixado.
- **Pergunta que grava** (`DQ.cotadas`, `tipo: "escolha"`, `caminho: ["aulaExtras","cotadas"]`):
  - `pergunta`: "Hoje, quantas linhas do seu projeto têm cotação escrita?"
  - opções e feedback:
    - `maioria` · "A maioria" → `ok`: "Comece pela ficha. Confira se as três maiores linhas estão cotadas e se as cotações têm menos de 90 dias."
    - `algumas` · "Algumas" → `at`: "Na ficha, deixe em branco o que não tem cotação. A ação de 30 dias vai apontar por onde começar."
    - `nenhuma` · "Nenhuma" → `at`: "Normal na primeira versão. A ficha vira o seu mapa do que cotar."
  - `porque`: "O selo não exige percentual mínimo de cotação. A primeira versão honesta, com as linhas em branco nomeadas, conclui a lição."
- **Notas:** 35 s. **A confirmar por Bruno:** selo sem percentual mínimo de linhas cotadas (PLANO, 12.11).
- **Fonte:** PLANO 6.6; diagnóstico d3 (PLANO 6.1).

### Slide 31 · ECROI · Reencadrar
- **Molde:** `section.s.esc`, `p.citacao` + `p.lead.f`.
- **Tela:**
  - `p.k`: O que mudou desde o primeiro slide
  - `p.citacao`: "Um projeto hoteleiro não morre quando falta dinheiro. Morre quando os números nunca foram feitos."
  - `p.lead.f`: O seu número não precisa ser perfeito. Precisa ser inteiro, com a origem de cada linha e o que falta cotar escrito.
- **Notas:** 30 s. Volte ao palpite do slide 3: quem escreveu um número vai compará-lo com a conta na ficha. O palpite não era burrice: era só a unidade. Agora você sabe o que mais existe até o primeiro hóspede. Fonte da frase: A05, capítulo 1.
- **Fonte:** citação literal A05 cap. 1; R2.

### Slide 32 · ECROI · O caminho
- **Molde:** `section.s` com `ol.lista.num`, itens `.f`.
- **Tela:**
  - `h2`: O caminho <i>a partir de hoje</i>
  - 1 · Hoje: a primeira versão na ficha O meu CAPEX.
  - 2 · Nos próximos 30 dias: as cotações, com o checklist.
  - 3 · Depois: volte à ficha do Pilar 6 e refaça a página 6.
  - 4 · Em seguida: a Planilha 2 · Investimento.
  - 5 · A necessidade de capital fica para o Pilar 7.
- **Notas:** 35 s. Na página 6, as linhas com cotação levam nota 3; as estimativas, nota 1; as em branco, "Não sei". O quadro "Como levar para a página 6" da ficha diz o que copiar em cada campo. Ferramentas extras, se quiser: Planilha 1 · Orçamento de Abertura, Ferramenta 05 · Orçamento da Cabana e a Calculadora de Implantação. **Turma de acompanhamento** (`?turma=acompanhamento`): troque o passo 3 por "leve a página 6A ao encontro do Pilar 6 e refaça a página 6 depois do comentário da equipe".
- **Fonte:** PLANO, seções 8 e 9.

### Slide 33 · ECROI · Resultado educacional e de onde vem o método
- **Molde:** `section.s.foto` com `data-bg="../fotos/c4b7d4ee48.jpg"` (foto real, sem pessoas; o construtor confere antes de publicar).
- **Tela:**
  - `p.k`: O que você leva desta aula
  - `h2`: Um número inteiro, <i>com origem</i>
  - `li.f`: Separar o custo de abrir a porta, o giro e o terreno.
  - `li.f`: Pôr cada gasto em um dos sete blocos, uma vez só.
  - `li.f`: Ler o número: o quanto está cotado, o que falta e a reserva com regra.
  - `p.sm` (legenda da foto): Foto real de uma unidade da Zion Bubble Glamping. O método desta aula vem dos materiais da Zion; os números da aula são fictícios e não vêm desta unidade.
- **Notas:** 30 s. O resultado é de aprendizagem: você sabe montar e ler o número. Ele não garante preço, aprovação, crédito nem prazo de obra; quem confirma custos, licenças e impostos é o engenheiro, o arquiteto, a prefeitura e o contador.
- **Fonte:** objetivos O1, O2, O5 e O6 (PLANO, seção 3); regra de fotos (PLANO 5.2; CLAUDE.md, seção 2).

### Slide 34 · Faça agora · O meu CAPEX
- **Molde:** `section.s.esc` com botão `a.btn` grande.
- **Tela:**
  - `p.k`: Agora é a sua vez
  - `h2`: Faça agora · <i>O meu CAPEX</i>
  - `p.lead`: A primeira versão da sua página 6A, com os seus números. Linha em branco é permitida.
  - `a.btn` "Abrir a ficha" → `href="../../capex/"` (acrescentar `?turma=acompanhamento` quando a aula vier com esse parâmetro). **TODO:** confirmar o caminho final da ficha (`docs/trilha1/capex/` × `docs/trilha1/pilar6-capex/`).
  - `p.sm`: Material educativo. Não é orçamento, projeto nem estudo de viabilidade definitivo. Custos, licenças e impostos se confirmam com engenheiro, arquiteto, prefeitura e contador. A Helena e os Chalés do Ribeirão são fictícios.
- **Notas:** 20 s. Peça que abram a ficha agora, com a aula ainda fresca, e façam ao menos a tela do palpite e a da fase. Lembre de salvar o PDF na pasta Meu Dossiê.
- **Fonte:** PLANO 5.4 e 9; rodapé do PLANO 5.1.

---

## 3. Citações literais usadas (todas da lista autorizada do PLANO 5.1)

| Slide | Citação | Fonte |
|---|---|---|
| 4 | "Uma linha em branco vale mais do que um número inventado." | P6, cap. 00 |
| 7 | "O amador orça o chalé. O developer orça o que faz o chalé funcionar." | A05, cap. 4 |
| 8 | "Não é quanto custa a cabana. É quanto custa abrir a porta." | P6, cap. 02 |
| 9 | "fora da conta não quer dizer de graça" | P6, cap. 02 |
| 11 | "A frase “não inclui” é a mais importante de qualquer proposta." | JC04, Passo 09 |
| 11 | "Cotação de mais de noventa dias precisa ser refeita." | VOL05, cap. 4 |
| 15 | "Nunca desenhe um projeto que só funciona inteiro. Desenhe um organismo que cresce." | A05, cap. 12 |
| 16 (notas) | "Corte metros quadrados no projeto. Nunca corte a experiência dentro deles." | A05, cap. 5 |
| 20 | "A contingência não é pessimismo. É maturidade." | A05, cap. 1 e 7 |
| 31 | "Um projeto hoteleiro não morre quando falta dinheiro. Morre quando os números nunca foram feitos." | A05, cap. 1 |

O construtor copia as frases exatamente como estão aqui (inclusive aspas e pontuação) e não acrescenta outras.

## 4. Pendências para o construtor (TODO)
1. Caminho da ficha: `docs/trilha1/capex/` (pedido nesta rodada) × `docs/trilha1/pilar6-capex/` (PLANO 5.4). Ajustar o link do slide 34 e o `diag` final, se a aula embutir a ficha em `iframe` como no Pilar 6.
2. Nome dos campos que a aula grava (`palpite`, `dataPalpite`, `cotadas`) e se a ficha os lê da chave `zion-t1-pilar6a`.
3. Classe vermelha do `.aviso` e do verso dos cartões do semáforo (conferir no `deck.css`; se não houver, criar na própria aula).
4. Conferir visualmente que `c4b7d4ee48.jpg` não tem pessoas (conferido nesta rodada: só a estrutura entre as araucárias).
5. Itens **a confirmar por Bruno** citados nos slides 11, 16, 20, 22, 25, 26 e 30 (PLANO, seção 12).

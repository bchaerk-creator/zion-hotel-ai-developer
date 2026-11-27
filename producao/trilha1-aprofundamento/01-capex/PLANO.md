# Trilha 1 · Pilar 6 · Aprofundamento 6A · CAPEX · Plano da lição

Status: plano de produção, versão 2 (27/11/2026), escrito pelo arquiteto pedagógico para o roteirista, o construtor e o designer. Substitui a versão 1 do mesmo dia. Nada foi produzido nem publicado com esta versão. O ClickMax não foi tocado. As decisões marcadas **[a confirmar por Bruno]** já orientam a produção, mas Bruno pode trocá-las antes do "aprovado". A lista completa está na seção 12.

Base lida: `CLAUDE.md`; `producao/fabrica/FABRICA.md` (seções 3 e 7); skill `zion-learning-design` (`SKILL.md` e `references/`); `producao/jornada2/PLANO_G00.md` (molde de plano); **`producao/trilha1-aprofundamento/GUIA_COERENCIA.md` (inteiro; decisão: Opção A do item I1)**; mapa de fontes `exportacao-zion/lições/capex/MAPA_FONTES_CAPEX.md` (fora do repositório público, sem texto bruto); e-book do Pilar 6 (`docs/trilha1/materiais/Pilar-6-Pre-viabilidade-ebook.pdf`, caps. 00 a 04, 07 e 08); ficha do Pilar 6 (`docs/trilha1/pilar6/index.html`: `REF`, `calcular`, `resumo.dados`); fichas do Pilar 3, do Pilar 5 e do Pilar 7 (textos `marina:`); Planilha 1 e Planilha 2 pelo gerador `producao/clube/planilhas/src/build.py` (abas, linhas e células).

Códigos de fonte usados neste plano (os mesmos do mapa, mais os do curso): **A05** Volume A05 · Investimento; **F01** e-book da escola F01; **P3, P5, P6, P7** e-books e fichas dos Pilares 3, 5, 6 e 7 da Trilha 1; **MZ** ficha do Marco Zero; **CA** Comece aqui; **MAPA** Mapa de direcionamento (etapa 6); **PL1/PL2** Planilhas 1 e 2 da Trilha 1; **F05** Ferramenta 05 (só como fonte de nome de linha, nunca como próximo passo); **B06** Calculadora de Implantação (idem); **JC01, JC02, JC04** Jornada do COMO; **VOL05** Volume 05 · Investimento; **R1…R40** regras numeradas no mapa de fontes; **GUIA** guia de coerência. Qualquer outra coisa é **elaboração própria** e está marcada assim.

---

## 0. O que mudou nesta versão (para quem já produziu a versão 1)

| Item do GUIA | O que muda | Onde neste plano |
|---|---|---|
| I1 (Opção A) | O caso deixa de ser Helena e os Chalés do Ribeirão. **A Marina é o caso**, partindo da página 6 dela. Helena some de todas as peças | 7 (tabela completa), 5 |
| I2 | O "palpite" vira **"página 6 × página 6A"**: o número de partida é o investimento da fase um da página 6, lido de `zion-t1-pilar6` | 4, 6.1 (tela 1), 6.2 |
| I3, I4 | Caixa "Do Pilar 6 para a 6A": folha de oito linhas → sete partes; infraestrutura comum entra na Parte 2 e as áreas comuns na Parte 3; base da reserva muda; Pilar 5 citado | 5.2 (caps. 00, 01, 02, 05) |
| I8 | **"Parte 1 a 7"** no lugar de "Bloco 1 a 7" em todas as peças, inclusive no código (`parte`, não `bloco`). "Bloco" fica só no sentido do curso (as duas partes da aula) | todas |
| B3, I5, I6 | A Planilha 1 é o caminho do curso: quadro "partes da 6A → abas da Planilha 1"; nome certo da Planilha 2 e das células B5, B6 e B9; Ferramenta 05 e Calculadora de Implantação fora do próximo passo | 5.2 (cap. 11), 6.2, 9 |
| I7, I9 | Aula sem sigla interna; selo da Etapa 4; "Retomada · Pilar 6"; "O 6A em cinco frases"; slide "Próximo" com a pasta Meu Dossiê; sem slides com tom de página de venda | 5.3 |
| I10 | E-book com a anatomia do curso (três respostas, capitular, Antes que você pense, Duas situações, Revisite, Pare e pense, O 6A em dez linhas) | 5.2 |
| I11, I14 | "Faça agora · O seu CAPEX"; situações com as palavras do Marco Zero; pasta Meu Dossiê; "Esta ficha não envia nada" | 5.5, 6.1 |
| I12 | Nomes "Aprofundamento 6A · CAPEX · …" e posição antes da Planilha 1 | 5.9 |
| I13 | Atribuição correta das citações | 5.2 (tabela de citações) |
| B1, B2, O1 a O7 | Identidade da Trilha 1 (Playfair Display + Inter, `#16261C`, `#F5F1E8`, `#E0BE5E`), cor de capa por tipo de peça, nomes de arquivo `Pilar-6A-…` e `p6a-c-…`, exercícios dentro do e-book | 5.1, 5.8, 10 |
| novo | Fecho com o **limite da página 6** ("até cerca de R$ 870 mil" na Marina): a ficha lê `inv8` da página 6, calcula a folga e alerta se passar | 6.2, 6.3, 6.4 |

---

## 1. A lição em uma frase e o entregável

**Frase (promessa):** Aprenda o passo a passo para abrir, linha por linha, quanto custa abrir a porta do seu projeto, com a origem de cada número, e conferir se a conta ainda cabe no limite da sua página 6 antes de assinar qualquer obra.

**A pergunta do pilar continua a mesma** (GUIA 5.3): a 6A ainda responde «O negócio se paga?», abrindo a linha «quanto custa abrir a porta» (P6 cap. 02).

**Entregável:** a **«Página 6A · CAPEX»** do Dossiê de Desenvolvimento, página irmã da página 6, em PDF de uma página (mais o anexo opcional «Lista de cotações a pedir»). Ela não muda a contagem de sete páginas do Dossiê (GUIA 3.4). Traz:
- as sete partes do custo com valor, peso e quantas linhas têm cotação;
- o custo de abrir a porta da fase (CAPEX da fase), o capital de giro e o investimento total da fase um (CAPEX + giro);
- o limite da página 6 («o que precisa ser verdade») e a folga ou o excesso;
- o custo por unidade, o investimento por unidade (o "custo por chave" do Pilar 6) e o custo por metro quadrado;
- o terreno anotado à parte («fora da conta não quer dizer de graça», P6 cap. 02);
- a comparação **página 6 × página 6A**;
- a regra de uso da reserva do imprevisto;
- três pontos de atenção, a ação de 30 dias e como verificar;
- o quadro «Como levar para a página 6» (campo a campo) e o resumo «Se você usa a Planilha 1» (os quatro totais por aba).

A página serve sozinha: mostra o custo da fase, quanto dele está apoiado em cotação, o que falta cotar e se a conta ainda cabe no limite que a própria pessoa escreveu. Basta para uma conversa com o engenheiro, a família ou um sócio.

**Começar a usar × resultado externo:** em uma tarde sai a primeira versão (com estimativas e linhas em branco nomeadas). Trocar as linhas por cotação leva o tempo dos fornecedores e não depende da lição. A lição não promete aprovação, crédito, parceria, retorno, ocupação nem prazo de obra.

**Termos na tela (sem sigla):**
- "CAPEX" aparece só como nome da lição e da página, sempre explicado na primeira vez como no Pilar 6 («O nome técnico é CAPEX, do inglês capital expenditure…», P6) e como «o custo de abrir a porta» **[a confirmar por Bruno: manter a sigla no nome]**.
- FF&E e OS&E não aparecem na tela: «Mobiliário e equipamentos» e «Enxoval, utensílios e suprimentos». O e-book cita os nomes técnicos uma vez, como o P6 cap. 02 («As siglas que você vai ouvir…»), e explica que a Planilha 1 usa esses nomes nas abas.
- Tempo de volta, nunca payback. Sem "membro" e sem "aluno" no texto de tela; "você" para quem estuda, "nós" e "a Zion" para a escola (GUIA 1.4).
- No checklist, BDI, ITBI, ART e RRT aparecem por extenso, com a sigla entre parênteses, porque a pessoa vai ouvir a sigla do profissional (elaboração própria).

---

## 2. Públicos e situações: o que muda para cada um

A primeira tela da ficha usa **as palavras do Marco Zero** (MZ, `marco-zero/index.html`) e vem pré-marcada a partir de `zion-t1-marco-zero` quando existir. Na tela, o curso não usa "Jornada A/B" (GUIA 3.2). O conteúdo e as contas são os mesmos para todos.

| Situação (tela 0, texto exato do Marco Zero) | Jornada (interna) | Público do comando 01 | O que a lição faz | O que muda na ficha |
|---|---|---|---|---|
| «Tenho um terreno e ainda não hospedo ninguém» | quero começar | desenvolvedor | Abre as linhas da página 6 sobre o masterplan do Pilar 5 (fase um e projeto completo) | Fluxo completo; rede dimensionada para o projeto completo; terreno "já é meu" ou "vou comprar" |
| «Tenho uma ideia, ou o capital, e ainda não tenho o terreno» | quero começar | desenvolvedor | Monta o CAPEX sobre o terreno candidato, ou deixa a Parte 2 nomeada e em branco | Aviso fixo: «a infraestrutura só se fecha com o terreno escolhido»; terreno pré-marcado "vou comprar" (A18) |
| «Já opero uma hospedagem e quero crescer» | já opero | gestor | Monta o CAPEX da ampliação (unidade nova, fase dois, área comum), com a rede existente como ponto de partida | Parte 2 sugere «reforço da rede existente»; alerta fixo «não pague a obra com o caixa da operação» (F01 caps. 1 e 7); giro pode ser zero com justificativa escrita **[a confirmar por Bruno]**; e-book troca estimativas pelo extrato de doze meses (P6 cap. 00) |
| Caixa extra, em qualquer situação: «Estou fazendo para o projeto de outra pessoa» | ambas | operador | Prepara a 6A para levar ao dono | Textos em terceira pessoa («o projeto do dono»); próxima etapa: «leve a página 6A ao dono» |
| Interruptor, em qualquer situação: «O imóvel já existe e será adequado» | ambas | todos | Monta o CAPEX da adequação | A Parte 3 vira «Adequação e reforma»; Partes 2 e 3 aceitam "não se aplica" linha a linha; reserva na régua de reforma (JC04 P04: 15% a 25%; JC02 P11: imóvel pronto 15% a 20%) |

No e-book e na aula, cada capítulo traz as duas aplicações com as frases do curso: «Se você ainda não hospeda: …» e «Se você já opera e quer crescer: …» (P6 cap. 00; GUIA 5.7).

Reversão pela expertise: quem responde no diagnóstico que a página 6 já tem a maioria das linhas cotadas vê o atalho «pule para a ficha; o tutorial fica de consulta».

---

## 3. Objetivos (verbos observáveis) e onde a ficha mede cada um

| # | Objetivo | Nível | Onde a ficha mede |
|---|---|---|---|
| O1 | Distinguir CAPEX da fase, investimento total (CAPEX + giro), terreno (fora da conta, mas não de graça) e custo da captação (Pilar 7) | compreender | Tela 10: giro e terreno, com os totais separados no resultado. Exercício E3 (terreno, giro, juros) |
| O2 | Classificar cada gasto numa das sete partes, sem contar o mesmo item duas vezes, e dizer onde ele estava na folha de oito linhas da página 6 | analisar | Telas 3 a 8; confirmação «o enxoval não está na cotação do mobiliário» (R28); quadro «Como levar para a página 6». Exercício E3 |
| O3 | Orçar a infraestrutura por distância e capacidade, dimensionada para o projeto completo do Pilar 5 e paga na fase | aplicar | Tela 4: distância até o ponto de energia, «para quantas unidades a rede é dimensionada» e alerta A6 |
| O4 | Calcular o total de cada parte, o CAPEX da fase, o peso de cada parte, o custo por unidade, o custo por m², o investimento total e a folga até o limite da página 6 | aplicar | Resultado (fórmulas 6.2). Exercícios E2 e E4 |
| O5 | Avaliar a qualidade do próprio número: linhas com cotação, valor cotado, cotações vencidas ou incompletas, faixas de conferência e página 6 × 6A | avaliar | Resultado: % de linhas e de valor cotado, régua de maturidade, alertas |
| O6 | Escrever a regra de uso da reserva do imprevisto nas quatro linhas | criar | Tela 9: quatro campos obrigatórios (R24) |
| O7 | Produzir a página 6A com uma ação de 30 dias verificável e devolvê-la à página 6 e à Planilha 2 | criar | Critério de conclusão (6.6), PDF baixado, quadro de transposição |

---

## 4. As seis etapas

| Etapa | O que a pessoa faz | Peça | Duração alvo | Fonte |
|---|---|---|---|---|
| **1 · Diagnosticar** | Abre com a **página 6 dela** (o investimento da fase um e a data, lidos de `zion-t1-pilar6`, ou digitados) e responde 4 perguntas sobre a página 6: tem cotação? inclui infraestrutura comum, áreas comuns e pré-abertura? quantas linhas cotadas? reserva com regra escrita? Vê o degrau na régua | Telas 0 e 1 da ficha; na aula, «Retomada · Pilar 6» e o slide de previsão («a página 6 da Marina diz cerca de R$ 690 mil: com a infraestrutura comum e as cotações, o número sobe, desce ou fica?») | 2 a 3 min | P6 cap. 04 (a conta e as duas observações), cap. 07 (o limite); régua Sonhador, Estimador, Calculista, Developer (P6 cap. 02, A05 cap. 1, sem ™). **Não repete o palpite nem os cinco erros do Pilar 6 do zero: retoma com «No Pilar 6 você…»** (GUIA 5.2) |
| **2 · Compreender** | Entende as sete partes, o que a folha de oito linhas deixou de fora, a origem de cada número e as conferências | Aula interativa (15 a 20 min) e e-book de 30 a 40 páginas | 20 min de aula; 50 a 70 min de leitura | R1, R3, R5 a R14, R16 a R29; P5 (apoio, rede para 5); P6 caps. 02 a 04 |
| **3 · Observar** | Vê a Marina abrir a página 6 dela na ficha, do começo ao fim | Tutorial em vídeo da ficha (roteiro 5.7); cap. 09 do e-book (exemplo resolvido); Bloco 2 da aula | 4 a 5 min de vídeo | Exemplo ilustrativo (seção 7) |
| **4 · Executar** | Resolve os exercícios (parcial e em branco) e preenche a ficha com os próprios números; usa o checklist para pedir cotações | Cap. 10 do e-book (exercícios); ficha «Faça agora · O seu CAPEX»; checklist em PDF | 15 a 20 min de exercícios; ficha com 30 a 45 min na primeira passada **[a confirmar por Bruno: acima das referências da FABRICA, por causa das sete partes]** | R5 a R8, R17, R19, R24 |
| **5 · Validar** | Lê o feedback em cinco partes, corrige o que os alertas apontam e cumpre o critério de conclusão | Resultado da ficha e selo «Pronto para levar à página 6» | 3 a 5 min | Domínio (FABRICA 3.2); alertas com fonte (6.4) |
| **6 · Entregar** | Baixa a página 6A, salva na pasta Meu Dossiê ao lado da página 6, refaz a página 6 campo a campo e segue a ordem do Mapa: Planilha 1 (se preferir planilha) → Planilha 2 → sensibilidade → página 6 | PDF 6A; quadro «Como levar para a página 6»; resumo «Se você usa a Planilha 1»; próxima etapa | 2 min (mais o tempo de refazer a página 6) | MAPA etapa 6; PL1 Resumo; PL2 aba Investimento; P7 («Dias 61 a 90 · Decidir: refaz a página 6 com os números cotados») |

A ficha salva no aparelho: a pessoa volta a cada cotação que chega e refaz o PDF. A primeira versão sai com estimativas e linhas em branco; as seguintes vão trocando linha por cotação.

---

## 5. Pacote da lição: especificação de cada peça

### 5.1 Identidade e voz comuns a todas as peças (GUIA 1.4 e 4)
- **A identidade da Trilha 1 manda** nesta lição, não a do `CLAUDE.md`: **Playfair Display** (títulos; ênfase em itálico dourado) e **Inter** (texto, com `font-variant-numeric: lining-nums`). Paleta das fichas e do e-book: verde `#16261C`, verde 2 `#22382A`, creme `#F5F1E8`, creme 2 `#EBE4D4`, dourado `#E0BE5E`, dourado escuro `#7A5E12`, texto 2 `#46564B`, linha `#D6CDB8`, branco `#FFFDF8`, ok `#1F5A33`/`#E1EFE3`, crítico `#9B2C1F`/`#F8E3DE`. Aula: tokens de `apresentacao/_motor/deck.css` (tinta `#16261C`, ouro `#C9A84C`, creme `#F5F1E8`, erro `#B5452F`). Cormorant, Aventa, `#1B2117`, `#FEF5F0`, `#DED6BF` e `#8B714E` **saem** das peças desta lição (B1). **[a confirmar por Bruno: registrar a exceção da Trilha 1 no `CLAUDE.md`]**.
- **Voz:** "você" para quem estuda, "nós" e "a Zion" para a escola; frases curtas e afirmativas; "cerca de" antes de número arredondado; toda conta fecha com **«Conferência: … Bate.»** (O4).
- **Rótulos fixos:**
  - números novos da Marina: **«Exemplo ilustrativo · dados fictícios. Não são preços de referência.»** (O3);
  - números da página 6 dela que vêm da Zion Glamping Store (R$ 129.000, R$ 192.346, subitens da unidade, margem de 40%): só como ponto de partida, sempre com **«referência orientativa da página 6, não confirmada; a Zion também vende esse tipo de estrutura»** (GUIA 2.1, regras 1 a 4). Nunca como preço, faixa ou argumento para escolher estrutura;
  - **regra de redação:** nenhuma peça compara linha a linha a cotação da Marina com a referência da Zion (sem "ficou mais barato" ou "mais caro"). Compara-se só o **total** da página 6 com o total da 6A, e a explicação é de escopo: «a referência era de uma unidade pronta genérica; a cotação é da cabana do projeto dela, com a rede comum e as áreas comuns orçadas à parte, nas Partes 2 e 3» (elaboração própria).
- **Frases-assinatura citadas com o pilar de origem** (GUIA 1.4): «Não é quanto custa a cabana. É quanto custa abrir a porta.» (Pilar 6); «Uma linha em branco vale mais do que um número inventado.» (Pilar 6); «O que não se constrói não se orça.» (Pilar 6); «fora da conta não quer dizer de graça» (Pilar 6); «Primeiro prove a conta, depois escolha como crescer» (Pilar 6); «Onde não souber, marque "Não sei": vira a sua tarefa da semana.» (Comece aqui); «A Zion avalia cada caso.» (fecho).
- **Aviso educativo** (e-book, checklist, ficha, aula): «Material educativo. Não é orçamento, projeto nem estudo de viabilidade definitivo. Custos, licenças e impostos se confirmam com engenheiro, arquiteto, prefeitura e contador. A Zion avalia cada caso.» No e-book, ele vai para «Como ler» e para as notas finais, **sem rodapé corrido** (O1).
- **Sem travessão** no texto das peças; sinal de menos com hífen se a fonte não tiver o glifo (O2).

### 5.2 E-book (30 a 40 páginas, A4, PDF)
- **Molde:** o e-book do Pilar 6 (HTML → Chromium, A4 595 × 842 pt). O construtor reaproveita `src/estilo.py` e `src/build_ebook.py` desta lição, trocando fontes, cores e capa (B1).
- **Capa** (formato do Pilar 6): verde `#16261C` com margem branca, sem logo e sem foto; sobretítulo «TRILHA 1 · PILAR 6 · APROFUNDAMENTO 6A · MÉTODO ZION»; título «CAPEX: *quanto custa abrir a porta, linha por linha*» (ênfase `#E0BE5E`); deck: «Com a página 6 na mão, a conta aberta em sete partes: o que tinha ficado à parte entra, cada referência vira cotação ou linha em branco, e o limite da página 6 confere se ainda cabe. Ao fim deste e-book você está pronto para a página 6A do seu Dossiê, CAPEX.»; numeral gigante «6A» em verde mais claro; rodapé «Zion Hospitality Business · Transforme Seu Terreno em um Projeto de Hospedagem de Sucesso · Aprenda o passo a passo com o Método Zion». A linha «Para Airbnb, casas, apartamentos, pousadas e glampings» sai da capa (O6) e entra na caixa «Duas situações».
- **Anatomia de cada capítulo** (I10): «CAPÍTULO NN · RÓTULO», título com ênfase em itálico, deck itálico, régua dourada, numeral grande, tabela «Por que fazer isso / Como vamos fazer / Para que serve», caixa «Neste capítulo», primeiro parágrafo com capitular, caixas «Exemplo ilustrativo», «Pare e pense» (com «Ver a resposta»), «Aplicação · No seu caso» (as duas situações), «Faça agora» e «Para levar».
- **Estrutura:**

| Cap. | Título que afirma | Conteúdo | Fontes | Pág. |
|---|---|---|---|---|
| — | Capa e sumário | como acima | P6 (molde) | 2 |
| 00 | Como usar este aprofundamento | «Este pilar em três respostas»; capitular: «Seja bem-vindo ao aprofundamento 6A. Você já fez a página 6 no Pilar 6. Aqui ela ganha uma página irmã, a 6A, que abre as linhas da página 6 uma por uma.»; I4: «As unidades da fase um e do projeto completo, e as áreas de apoio, vêm do masterplan do Pilar 5. O que não se constrói não se orça.»; «Antes que você pense» (três dúvidas: «Já fiz a página 6. Preciso disso?» · «Não tenho cotação nenhuma.» · «E se a conta passar do limite?»); «Duas situações, o mesmo método» (as três frases do Marco Zero e a linha de público); «Como ler» (rótulos e aviso educativo); «Revisite · Pilar 6» (três perguntas e os cinco erros do orçamento amador, retomados, não refeitos) | P6 caps. 00 a 02; P5; MZ; CA | 4 |
| 01 | A página 6 da Marina é o ponto de partida | A folha de oito linhas da Marina, com o rótulo da referência; as duas observações do Pilar 6 («orientativa, sem cotação ainda, e sem a infraestrutura comum do terreno»); o limite «até cerca de R$ 870 mil»; «Faça agora: escreva o investimento da fase um da sua página 6 e a data»; citação «Um projeto hoteleiro não morre quando falta dinheiro. Morre quando os números nunca foram feitos.» | P6 caps. 04 e 07; P7 (critério da Marina); A05 cap. 1 | 3 |
| 02 | Da folha de oito linhas às sete partes do custo | Caixa **«Do Pilar 6 para a 6A»** (I3, tabela abaixo); diagrama «dentro, ao lado, à parte»: sete partes = CAPEX da fase; + giro = investimento total; terreno ao lado, não somado; custo da captação no Pilar 7; **a base da reserva muda** (Pilar 6: 10% das unidades; 6A: % do subtotal das Partes 1 a 6; primeira obra no teto da faixa ou acima); FF&E e OS&E nomeados uma vez | R26, R27; P6 caps. 02 e 03; A05 cap. 2; F01 caps. 1 e 2 | 3 |
| 03 | Cada número tem origem: cotação, estimativa ou em branco | Na 6A a referência não entra: a ficha nunca põe valor no lugar do "Não sei"; três cotações com a mesma especificação; a lista do que «não inclui»; o mesmo pacote para todos; validade de 90 dias | R3, R5 a R8; JC04 P01 e P09; VOL05 caps. 4 e 5; P6 cap. 02 | 3 |
| 04 | Parte 1 e Parte 2: o que aprova a obra e o que leva a obra até o terreno | Parte 1 (só o que aprova projeto e obra; a licença de operar vai para a Parte 6); Parte 2 (perguntas do terreno; ponto de energia; dimensionar para o projeto completo e construir uma vez; «refazer vala e caminho na fase dois é a forma mais cara de economizar»); a Marina: rede para 5 com duto vazio, caminho do hóspede de cerca de 120 m (P5) | R11 a R14; P5; P6 caps. 03 e 04; A05 caps. 4 e 12; F01 caps. 2 e 6 | 4 |
| 05 | Parte 3: o metro quadrado inteiro | Área construída total × custo do m² cotado; estrutura pronta (bolha, domo, cabana pré-fabricada) conta como unidade na Parte 3 (na Planilha 1 ela fica na aba FF&E); áreas comuns custam: o apoio de 30 m² da Marina (rouparia 12, depósito 6, lixo 4, copa e vestiário 8, P5) e o deck leve da crista | R9, R10, R20, R33; P5; P6 cap. 03; A05 caps. 2, 4 e 5 | 3 |
| 06 | Partes 4 e 5: a unidade-modelo e um dia de operação | Unidade-modelo antes de comprar as demais; três jogos por cama; um dia de operação em cinco listas; cada item numa linha só; na Marina, lavanderia terceirizada e nenhuma recepção construída (decisões do P5) | R16 a R19, R28; P5; P6 cap. 03; A05 caps. 5 e 6; F01 cap. 4 | 3 |
| 07 | Parte 6 e Parte 7: a abertura e o imprevisto | A pré-abertura não estava na página 6; o que ela cobre; a reserva cobre o imprevisto da obra orçada, não escopo novo (o ofurô na crista, P6) nem o caixa; fatores de risco; regra de uso em quatro linhas; a Marina parte dos 10% da página 6, vê o alerta da primeira obra e sobe para 15%; a reserva que sobra vira giro | R21 a R25; P6 cap. 03; A05 cap. 7; F01 cap. 5; JC02 P11 | 3 |
| 08 | Ler o número antes de mostrá-lo | Peso de cada parte; custo por unidade e investimento por unidade (o "custo por chave" do Pilar 6), com nome e definição; custo por m²; faixas de conferência, que **não são preço**; página 6 × 6A; o limite e a folga | R29 a R31; P6 caps. 04 e 07; A05 cap. 3; F01 cap. 6 | 3 |
| 09 | A conta da Marina, inteira | Exemplo resolvido completo (seção 7), com as conferências «Bate.» e o fecho no limite | Exemplo ilustrativo | 4 |
| 10 | Pratique com a Marina | Exercícios E2 a E5 (5.4) com gabarito comentado no fim do capítulo (O7: não há caderno separado) | Exemplo ilustrativo | 3 |
| 11 | A página 6A e a volta | Como preencher a ficha; quadro **«Como levar para a página 6»** campo a campo; quadro **«Se você usa a Planilha 1»** (B3); Planilha 2 (I5); a sensibilidade do Mapa; o Pilar 7 («Dias 61 a 90 · Decidir: refaz a página 6 com os números cotados»); perguntas ao engenheiro, ao contador, à concessionária e à prefeitura | MAPA etapa 6; PL1; PL2; P6; P7; mapa 7.2 | 3 |
| ✓ | Confira o que ficou | «Pare e pense» com «Ver a resposta»; «O 6A em dez linhas»; «Faça agora · A minha página 6A»; notas e fontes (com o aviso educativo) | — | 3 |

- **Caixa «Do Pilar 6 para a 6A»** (cap. 02, I3):

| Na página 6 (folha de oito linhas) | Na página 6A |
|---|---|
| Linhas 1 a 6 · unidade pronta (unidade, deck, luz, água e esgoto, mobiliário com enxoval, piso) | Unidade, deck e piso → Parte 3; luz e água de cada unidade → Parte 2 (linhas por unidade); mobiliário → Parte 4; enxoval e utensílios → Parte 5 |
| Linha 7 · licenças e projetos | Parte 1 (o que aprova projeto e obra); licença de operar → Parte 6 |
| Linha 8 · reserva do imprevisto (10% das unidades) | Parte 7 (% do subtotal das Partes 1 a 6, com regra de uso) |
| À parte · infraestrutura comum («a cotar») | **Entra**: rede, acesso, caminhos e estacionamento → Parte 2; apoio e deck da crista → Parte 3 (áreas comuns) |
| Não estava | Parte 6 · pré-abertura |
| À parte · capital de giro (somado) | Igual: ao lado, somado no investimento total |
| À parte · terreno (fora da conta) | Igual: ao lado, não somado |

- **Citações literais** (curtas, com fonte na página; I13):

| Citação | Atribuição na peça |
|---|---|
| «Um projeto hoteleiro não morre quando falta dinheiro. Morre quando os números nunca foram feitos.» | Volume A05 · Investimento, cap. 1 |
| «O amador orça o chalé. O developer orça o que faz o chalé funcionar.» | Volume A05 · Investimento, cap. 4 |
| «A contingência não é pessimismo. É maturidade.» | Volume A05 · Investimento, cap. 7 |
| «Corte metros quadrados no projeto. Nunca corte a experiência dentro deles.» | Pilar 6 · Pré-viabilidade |
| «Cotação de mais de noventa dias precisa ser refeita.» | Volume 05 · Investimento, cap. 4 |
| «A frase "não inclui" é a mais importante de qualquer proposta.» | Jornada do COMO, Etapa 04, Passo 09 |
| «Não é quanto custa a cabana. É quanto custa abrir a porta.» · «Uma linha em branco vale mais do que um número inventado.» · «O que não se constrói não se orça.» · «fora da conta não quer dizer de graça» | Pilar 6 · Pré-viabilidade |

- **Proibido no e-book:** valor de custo de referência (A05, P6 ou PL1) como preço; os números da Zion Glamping Store fora do ponto de partida rotulado; comparação linha a linha cotação × referência; o município da sede; fotos com pessoas; Helena e os Chalés do Ribeirão; Rodrigo e Priscila (GUIA 2.2).

### 5.3 Aula interativa (molde `docs/trilha1/apresentacao/pilar6-aula/` + `_motor/`)
- Caminho: `docs/trilha1/apresentacao/pilar6a-aula/index.html` (renomear a pasta `capex-aula/`, O5). 1920 px, tokens do `deck.css`, Playfair + Inter locais de `_motor/fonts`. Título: «Aprofundamento 6A · CAPEX». Entre 32 e 38 slides, 15 a 20 min, até cerca de 40 palavras por slide, explicação nas notas.
- **`data-bloco`** (I7, I8), na ordem: «Abertura», «Como funciona esta aula», «Retomada · Pilar 6», «Bloco 1 · As sete partes do custo», «Bloco 2 · A Marina abre a página 6», «Quiz relâmpago», «Resumo», «A sua página 6A», «Próximo». Nenhum «ECROI» nem «Bloco 3 a 7» na barra.
- **Sequência:**
  1. Capa com o selo «Método Zion · Etapa 4 · Fechar a conta» (I9).
  2. «O que você vai fazer aqui»: Assistir · Responder · Sair com a página 6A.
  3. «Você já fez a página 6 no Pilar 6. Aqui ela ganha uma página irmã, a 6A.» (GUIA 5.1).
  4. «Retomada · Pilar 6», três perguntas de cabeça («Responda de cabeça. Errar aqui também ensina.»): o que ficou à parte na página 6 da Marina? (infraestrutura comum e terreno); sobre o que a base simplificada calcula a reserva? (10% das unidades); até quanto o investimento total dela aguenta dentro de 8 anos no conservador? (até cerca de R$ 870 mil).
  5. Previsão, no lugar de «Talvez você esteja aqui» e «A crença que trava» (I9): «A página 6 da Marina diz cerca de R$ 690 mil, sem a infraestrutura comum. Com tudo dentro e cotado, o número sobe, desce ou fica? Passa de R$ 870 mil?»
  6. Bloco 1: «Do Pilar 6 para a 6A» (a tabela de 5.2); o diagrama dentro, ao lado, à parte; as três origens; um slide por parte («Parte 1 · Projetos, licenças e documentação» … «Parte 7 · Reserva do imprevisto»), cada um com a pergunta-chave e o erro típico; Quiz relâmpago 1 (classificar 6 itens); Quiz relâmpago 2 («o ofurô na crista sai da reserva?»).
  7. Bloco 2: a conta da Marina revelada clique a clique (partes → subtotal → reserva a 10% → alerta da primeira obra → 15% → CAPEX → giro da página 6 → investimento total → limite de R$ 870 mil → folga); semáforo dos alertas (A11, A13, A14); página 6 × 6A; Quiz relâmpago 3 («qual é a ação de 30 dias?»).
  8. «O 6A em cinco frases» (I9).
  9. «A sua página 6A»: nome (sem e-mail, porque nada é enviado) e a ficha embutida, como o curso faz **[a confirmar por Bruno: o curso pede nome e e-mail; aqui proponho só o nome]**.
  10. «Próximo · Planilha 1, Planilha 2 e a página 6 refeita», com «Lembre: salve o PDF da página 6A na pasta Meu Dossiê, ao lado da página 6», «Esta ficha não envia nada: o PDF fica só com você.» (I14) e o aviso educativo.
- Simuladores do motor: escolha, marcar, calculadora (subtotal × % de reserva) e semáforo. Todo número da Marina leva o selo «Exemplo ilustrativo · dados fictícios».
- Fotos: só de `docs/trilha1/apresentacao/fotos/` já usadas no curso, sem pessoas, e só no trecho "de onde vem o método", com legenda.

### 5.4 Exercícios (dentro do e-book, cap. 10, com gabarito comentado)
Do resolvido ao em branco (esmaecimento):
- **E1 · Resolvido:** a conta da Marina (cap. 09).
- **E2 · Parcialmente resolvido:** a cotação da água (19.800, de 15/07/2026) venceu. A nova, com a mesma especificação, chega a **R$ 22.400**. Pede-se:
  - a Parte 2: 128.200 − 19.800 + 22.400 = **R$ 130.800**;
  - o subtotal: 687.940 + 2.600 = **R$ 690.540**;
  - a reserva a 15%: **R$ 103.581**;
  - o CAPEX: **R$ 794.121** (conferência: 791.131 + 2.600 × 1,15 = 791.131 + 2.990 = 794.121. Bate.);
  - o investimento total: 794.121 + 40.787,38 = **R$ 834.908,38**;
  - a folga: 870.130,80 − 834.908,38 = **R$ 35.222,42**;
  - qual alerta some: A13 (não há mais cotação vencida).
- **E3 · Classificação (intercalada):** 13 itens, com explicação de cada erro possível:
  - jogo de lençol e toalhas → Parte 5;
  - colchão → Parte 4;
  - projeto elétrico → Parte 1;
  - poço → Parte 2;
  - licença de funcionamento → Parte 6 (o que autoriza operar, F01);
  - fotos do anúncio → Parte 6;
  - deck de cada cabana → Parte 3;
  - prateleiras da rouparia do apoio → Parte 4 (equipamentos gerais);
  - bolha ou cabana pronta → Parte 3 (na Planilha 1, aba FF&E);
  - terreno → à parte, não somado;
  - capital de giro → à parte, somado no investimento total;
  - ofurô na crista decidido no meio da obra → escopo novo: linha nova e decisão, não reserva (P6, R23);
  - juros do empréstimo da obra → fora desta conta, Pilar 7 (lacuna 5).
- **E4 · A base da reserva:** quanto a reserva da Marina muda só por trocar a base e o percentual? Pede-se:
  - 10% das seis linhas por cabana, como na base simplificada do Pilar 6: 0,10 × 443.340 = **R$ 44.334**;
  - 10% do subtotal das Partes 1 a 6: 0,10 × 687.940 = **R$ 68.794**;
  - 15% do subtotal (primeira obra): **R$ 103.191**;
  - a diferença entre 10% e 15% do subtotal: 103.191 − 68.794 = **R$ 34.397**;
  - quais alertas aparecem a 10%: A4 (primeira obra abaixo de 15%);
  - a regra de uso em quatro linhas, escrita por quem estuda.
- **E5 · Em branco:** listar as linhas da própria Parte 2 e escrever a quem pede cada cotação. É a ponte para a ficha.

### 5.5 Ficha «Faça agora · O seu CAPEX» (gera a página 6A)
- **Caminhos:**
  - lógica pura em `producao/trilha1-aprofundamento/01-capex/src/logic.js`, sem DOM; testes em `tests/test_logic.js`, escritos antes da interface;
  - interface em `docs/trilha1/pilar6a/index.html` (renomear `docs/trilha1/capex/`, O5, antes de ligar as aulas), no molde de `docs/trilha1/pilar6/`: uma pergunta por tela, «por que», «onde conseguir», caixa «Marina» com o rótulo, PDF com jsPDF;
  - o caso da Marina (seção 7) num só arquivo de dados (`src/caso.py` → reescrever, e o `EXEMPLO` de `logic.js` gerado ou conferido a partir dele), para que ficha, e-book, aula e tutorial usem exatamente os mesmos números.
- **Título e cabeçalhos (I11):** título «Faça agora · O seu CAPEX»; cabeçalho da tela «Zion · Método Zion / Pilar 6 / Aprofundamento 6A · CAPEX»; PDF com cabeçalho «Zion · Dossiê de Desenvolvimento · Página 6A · CAPEX», nome e «Terreno em cidade/UF» (como a página 6), rodapé educativo e "k/n".
- **Leituras do aparelho** (com a origem escrita ao lado, «veio da página 6», como o `VEIO` do Pilar 6; leitura tolerante, campo vazio se falhar):
  - situação, de `zion-t1-marco-zero`;
  - nome, do perfil já salvo nas outras fichas (o construtor confere a chave usada pelo Pilar 6);
  - unidades da fase e do projeto completo, de `zion-t1-pilar5` ou `zion-t1-pilar6` (`resumo.dados.unidades`);
  - da página 6 (`zion-t1-pilar6`, `resumo.dados` e `resumo.data`): `total` (investimento total da fase um), `total_sem_giro`, `soma_folha`, `infra` (nulo = «à parte, a cotar»), `giro`, `giro_meses`, `terreno`, `inv8` (o limite de 8 anos) e `resultado_cons`.
- **Salvamento:** chave `zion-t1-pilar6a`, com `respostas` e `resumo.dados`, no formato das outras páginas.
- **Sem envio de dados** (FABRICA seção 7). A tela final e o PDF dizem: «Esta ficha não envia nada: o PDF fica só com você.» (I14) e «Salve o PDF da página 6A na pasta Meu Dossiê, ao lado da página 6.» (GUIA 5.9). O montador do Pilar 7 hoje não lê `zion-t1-pilar6a`: a volta é pelo quadro de transposição.
- **Telas:** 0 Abertura · 1 A sua página 6 · 2 A fase · 3 a 8 Partes 1 a 6 · 9 Parte 7, a reserva · 10 Giro e terreno · Resultado · Ação de 30 dias · PDF. Regras na seção 6.
- **Campo `turma`** (`?turma=acompanhamento`): muda só o texto da próxima etapa (seção 8).

### 5.6 Checklist em PDF (1 a 2 páginas, A4)
«Checklist da página 6A · antes de pedir cotação e antes de fechar o número». Fontes e paleta do e-book do Pilar 6, sobretítulo «TRILHA 1 · PILAR 6 · APROFUNDAMENTO 6A», a caixa «Faça agora» como molde (GUIA 4). Arquivo `Pilar-6A-CAPEX-checklist.pdf`.
1. **Antes de pedir cotação:** as perguntas do terreno (R13): distância da energia, água (vazão, poço, outorga), fundação, acesso de caminhão na chuva, declividade, prazo de licença; o mesmo pacote para todos (R7); a especificação escrita: material, medidas, quantidade, frete, instalação, entulho, prazo e garantia (R5); pedir a lista do que «não inclui» (R6).
2. **Ao receber:** três propostas com a mesma especificação; data anotada e validade de 90 dias (R8); na estrutura pronta, frete, fundação e montagem confirmados por escrito (R33).
3. **Por parte, o que costuma ficar de fora** (e que a página 6 deixava à parte): infraestrutura comum dimensionada para o projeto completo; áreas comuns e de apoio; unidade-modelo; três jogos por cama; pré-abertura; reserva com regra escrita; giro à parte.
4. **Pergunte ao seu engenheiro**, sem número: «o preço inclui mão de obra, encargos, administração e lucro (BDI)?»; «quanto o frete e a montagem acrescentam neste terreno?»; «como o preço pode mudar até a compra (reajuste)?»; «a rede está dimensionada para quantas unidades?»; «quem assina a responsabilidade técnica (ART ou RRT)?».
5. **Pergunte ao seu contador** (e ao advogado, na forma de entrada do terreno): custos de aquisição do terreno (escritura, imposto de transmissão ITBI, registro, certidões); impostos sobre a obra e a compra de equipamentos; compra, permuta, sociedade ou arrendamento (R27).
6. **Pergunte à concessionária e à prefeitura:** o ponto e a tensão de energia (R12); a lista e o custo das licenças.
7. **Depois da 6A:** refaça a página 6 campo a campo (digite 0 onde for zero: em branco, a ficha do Pilar 6 usa a referência); se preferir planilha, passe para a Planilha 1; cole o CAPEX na Planilha 2, aba Investimento, célula B5.
- **Nenhum percentual e nenhum preço no checklist.** Aviso educativo no fim.

### 5.7 Roteiro do tutorial da ficha (só o roteiro; sem gravar)
- Formato das specs de `producao/clube/tutoriais-video/`: cenas com ação na tela, destaque e narração. 16:9, **alvo de 4 min, teto de 5** (os tutoriais do curso têm de 3 min 26 s a 3 min 52 s). Arquivos: `producao/trilha1-aprofundamento/01-capex/tutorial/ficha-pilar6a.json` e `ROTEIRO.md`; vídeo final `docs/trilha1/videos/tutoriais/tutorial-ficha-pilar6a.mp4`. Entra logo depois do Faça agora (GUIA 4).
- Selo «Exemplo ilustrativo · dados fictícios» visível em toda cena com número. Voz "nós" e "você", frases curtas, "CAPEX" explicado na primeira vez.

| # | Ação na tela | Narração (ideia; o roteirista escreve o texto final) |
|---|---|---|
| 1 | Abertura; situação já marcada «Tenho um terreno e ainda não hospedo ninguém» (veio do Marco Zero) | O que você leva: a página 6A, irmã da página 6 |
| 2 | Tela «A sua página 6»: aparecem R$ 690.529,18, a data e o limite de R$ 870.130,80, com «veio da página 6» | A Marina parte do número dela, que era referência e não tinha a infraestrutura comum |
| 3 | Tela da fase: 3 agora, 5 no projeto completo (veio da página 5); primeira obra | Toda a conta é da fase um; a rede é pensada para 5 |
| 4 | Parte 1: linhas com «3 cotações», «estimativa minha» e a licença ambiental «em branco» | As três origens; a linha em branco aparece como tarefa |
| 5 | Parte 2: energia a 260 m, «dimensionada para 5»; a água com data de julho | Distância e capacidade; a cotação de julho vai aparecer como vencida |
| 6 | Parte 3: cabanas por área × m²; decks; apoio de 30 m²; deck da crista | O metro quadrado inteiro, com as áreas comuns do Pilar 5 |
| 7 | Partes 4 e 5: unidade-modelo × 3; enxoval com três jogos; recepção «não se aplica»; confirmar «não contei duas vezes» | Unidade-modelo e três jogos; cada item numa linha só |
| 8 | Parte 6 e Parte 7: reserva em 10% → alerta → 15%; regra de uso nas quatro linhas | Primeira obra pede o teto; a reserva não paga o ofurô |
| 9 | Giro e terreno: giro da página 6; terreno «já é meu» | O que se soma e o que fica ao lado |
| 10 | Resultado: R$ 831.918,38 contra o limite; folga de R$ 38.212,42; alertas A11, A13, A14 | Dentro, com folga fina: as cinco linhas em branco e a pré-abertura ainda precisam caber nela |
| 11 | Ação de 30 dias, prazo, baixar o PDF, quadro «Como levar para a página 6» | Salvar na pasta Meu Dossiê; refazer a página 6; depois a Planilha 1, se quiser, e a Planilha 2 |

- Gravação só depois do "aprovado". Voz sintética ainda sem licença registrada **[a confirmar por Bruno]**.

### 5.8 Capas das aulas (ClickMax)
- Referência: `docs/trilha1/capas/p6-c-ebook.jpg`, `p6-c-faca.jpg`, `p6-c-aula.jpg`. 1280 × 720, Playfair + Inter, logo Zion no topo como nas capas do curso, ícone à direita, sem cabeçalho nem rodapé.
- **Código de cor por tipo** (B2): aula verde quase preto `#0F1A14`; Faça agora creme `#F5F1E8`; e-book marrom `#5B3A29`; checklist creme 2 `#EBE4D4`; tutorial verde 2 `#22382A`; dourado `#E0BC64` nos detalhes.
- Sobretítulo «PILAR 6 · APROFUNDAMENTO 6A»; título da peça; subtítulo itálico; selos: aula «COMECE POR AQUI»; Faça agora «FERRAMENTA · PDF» (sem «mentor de IA», porque esta ficha não envia nada); tutorial «VÍDEO · PASSO A PASSO»; e-book «PDF · LEITURA»; checklist «PDF · CHECKLIST».
- Arquivos: `p6a-c-aula.jpg`, `p6a-c-faca.jpg`, `p6a-c-tutorial.jpg`, `p6a-c-ebook.jpg`, `p6a-c-check.jpg` (substituem `capex-c-*.jpg`). Gerador: `src/build_capas.js`, refeito a partir do gerador das capas `p6-c-*`.

### 5.9 Onde cada peça entra no ClickMax (para o publicador; nada é feito agora)
- Conteúdo `fa9a6c54-e40c-4ee0-99cc-ee6ec70e68fb`, módulo **Pilar 6** `6e06c29d…` (conferir com `modules_list`). As aulas atuais do Pilar 6 ficam intocadas.
- **Cinco aulas, todas `enabled=false`**, depois do tutorial da ficha do Pilar 6 e **antes da Planilha 1** (GUIA 5.8; I12), na ordem:
  1. «Aprofundamento 6A · CAPEX · Aula interativa» (link externo para `pilar6a-aula/`);
  2. «Aprofundamento 6A · CAPEX · Faça agora · O seu CAPEX» (link externo para `pilar6a/`, com os comentários ligados);
  3. «Aprofundamento 6A · CAPEX · Tutorial da ficha» (vídeo, só depois de gravado);
  4. «Aprofundamento 6A · CAPEX · E-book (PDF)» (`Pilar-6A-CAPEX-ebook.pdf`);
  5. «Aprofundamento 6A · CAPEX · Checklist (PDF)» (`Pilar-6A-CAPEX-checklist.pdf`).
- As quatro aulas já criadas e desligadas (`8e98bed7`, `bccdfac4`, `f1918e33`, `758e9b1c`) são renomeadas, reapontadas para os arquivos novos e reposicionadas; a do tutorial é nova. **Mexe em aulas existentes: só com o "aprovado" de Bruno.** Ligar também só com o "aprovado"; o curso está em 5 turmas.
- Capas `p6a-c-*.jpg` em cada aula.

---

## 6. Regras da ferramenta (testáveis)

Convenções:
- Dinheiro em reais, com até 2 casas. Percentuais exibidos com 1 casa; comparações com faixas usam o valor sem arredondar e incluem as bordas (lo ≤ x ≤ hi).
- Divisão por zero devolve `null`, e a tela explica o motivo.
- A lógica recebe `hoje` como parâmetro (datas determinísticas nos testes).
- **"Não sei" é sempre um estado explícito, nunca um zero escondido.** A ficha nunca insere valor de referência.
- No código e na tela: **`parte`** (1 a 7), não `bloco`.

### 6.1 Entradas

**Tela 0 · Abertura**

| Campo | Tipo | Obrigatório | Faixa e "não sei" |
|---|---|---|---|
| `nome` | texto | não | 2 a 60 caracteres; pré-preenchido do perfil salvo |
| `projeto` | texto | sim | 2 a 60 caracteres |
| `cidadeUF` | texto | não | 2 a 60 caracteres (vai para o PDF, como na página 6) |
| `situacao` | escolha | sim | `terreno` = «Tenho um terreno e ainda não hospedo ninguém»; `ideia` = «Tenho uma ideia, ou o capital, e ainda não tenho o terreno»; `opero` = «Já opero uma hospedagem e quero crescer». Pré-marcada de `zion-t1-marco-zero` |
| `paraOutro` | booleano | sim | «Estou fazendo para o projeto de outra pessoa»; padrão `false` |
| `tipo` | escolha | sim | casa ou apartamento; cabanas ou chalés; glamping (bolha, domo, tenda); pousada; outro |
| `imovelPronto` | booleano | sim | padrão `false` |
| `d1` | escolha | sim | «A minha página 6 tem: a maioria das linhas com cotação / referência ou estimativa / ainda não fiz a página 6» |
| `d2` | escolha | sim | «A página 6 já inclui infraestrutura comum, áreas comuns e pré-abertura? todas / algumas / nenhuma / não sei» |
| `d3` | escolha | sim | «Quantas linhas têm cotação escrita? a maioria / algumas / nenhuma» |
| `d4` | escolha | sim | «A reserva tem regra de uso escrita? sim / não» |
| `turma` | texto (URL) | não | `autonomo` (padrão) ou `acompanhamento` |

**Tela 1 · A sua página 6** (I2; substitui o palpite)

| Campo | Tipo | Obrigatório | Faixa e "não sei" |
|---|---|---|---|
| `pagina6Total` | R$, "não fiz" ou "não sei" | sim | 0 a 100.000.000; padrão `resumo.dados.total` de `zion-t1-pilar6`, com «veio da página 6» |
| `pagina6Data` | data | não | lida de `resumo.data`; não pode ser futura |
| `pagina6Infra` | R$ ou «à parte, a cotar» | não | lida de `resumo.dados.infra`; nulo = à parte |
| `limite6` | R$, "não sei" | não | 0 a 100.000.000; padrão `resumo.dados.inv8`; se faltar e houver `resultado_cons`, `8 × resultado_cons`. Texto: «o investimento total até onde a sua conta aguenta, dentro de 8 anos no conservador (página 6, o que precisa ser verdade)» |

**Tela 2 · A fase**

| Campo | Tipo | Obrigatório | Faixa |
|---|---|---|---|
| `unidadesFase` | inteiro | sim | 1 a 200; lido da página 5 ou 6 |
| `unidadesProjeto` | inteiro ou "não sei" | sim ("não sei" bloqueia o selo) | `unidadesFase` a 200; lido da página 5 |
| `fatoresRisco` | marcar vários | não | território remoto; sistema construtivo novo para a equipe; itens importados; licenciamento em área sensível; prazo apertado pela temporada (R22) |
| `primeiraObra` | booleano | sim | — |

**Telas 3 a 8 · Linhas das Partes 1 a 6.** Cada parte tem de 1 a 15 linhas. As linhas sugeridas vêm só com o nome (nunca com valor) e podem ser renomeadas, apagadas ou acrescentadas.

| Campo | Tipo | Regra |
|---|---|---|
| `nome` | texto | 2 a 80 caracteres |
| `modo` | escolha | `valor` (R$ total), `qtdUnit` (quantidade × valor unitário), `area` (quantidade × área em m² × custo do m²) |
| `qtd` | inteiro | 1 a 999 (metros de caminho cabem aqui); nas linhas por unidade, o padrão é `unidadesFase` |
| `valorUnit`, `valor`, `custoM2` | R$ | > 0 e ≤ 100.000.000 se a origem é `cotacao` ou `estimativa`; ignorados se `branco` ou `naoAplica` |
| `areaM2` | número | 0,1 a 10.000, ou "não sei" (só afeta o custo por m²) |
| `origem` | escolha | `cotacao` (cotação escrita), `estimativa` (estimativa minha, sem cotação), `branco` (em branco), `naoAplica` |
| `nCotacoes` | escolha | 1, 2 ou "3 ou mais"; obrigatório se `cotacao` |
| `mesmaEspec` | booleano | só se `nCotacoes` ≥ 2: «as propostas têm a mesma especificação e eu sei o que cada uma não inclui» |
| `dataCotacao` | data | opcional; não pode ser futura |
| `tagP6` | escolha | só para a transposição: `unidade`, `deck`, `piso`, `luz`, `agua`, `mobilia` ou nenhuma |

- **Origem:** `branco` vale 0 e conta como risco; `estimativa` vale na soma, conta como "sem cotação" e é risco **[a confirmar por Bruno: permitir "estimativa minha"; a alternativa estrita é só cotação ou em branco, R3]**.
- **Equivalência com a nota do Pilar 6** (para levar a nota à página 6): `cotacao` = 3; `estimativa` = 1 (o Pilar 6 chama a nota 1 de «referência ou estimativa»); `branco` = «Não sei». O nível 2 do Pilar 6 («falado, sem papel») entra aqui como `estimativa`.

**Linhas sugeridas por parte (somente nomes)**, das fontes (PL1 `build.py`, F05 `dados.py`, B06), sem valores:
- **Parte 1 · Projetos, licenças e documentação:** levantamento topográfico e sondagem; arquitetura; projetos complementares (estrutural, elétrico, hidrossanitário); aprovação na prefeitura e taxas; licença ambiental, se houver; responsabilidade técnica e registros. Só o que aprova projeto e obra (F01).
- **Parte 2 · Infraestrutura:** acesso interno; estacionamento e vaga de serviço; caminhos; energia (rede comum até as unidades); água; esgoto e tratamento; drenagem; internet; ligação de luz de cada unidade (`tagP6=luz`); água e esgoto de cada unidade (`tagP6=agua`). Quem já opera vê também «reforço da rede existente».
- **Parte 2, campos próprios:** `distanciaEnergiaM` (0 a 50.000, ou "não sei"); `infraDimensionadaPara` (1 a 999, ou "não sei"; obrigatório se a Parte 2 tiver linha que não seja `naoAplica`); `infraProjetoCompleto` (R$ opcional, informativo; a diferença para o que se paga agora aparece como «fica para as próximas fases» e não entra no CAPEX da fase).
- **Parte 3 · Unidades e áreas comuns** («Adequação e reforma» se `imovelPronto`):
  - de 1 a 3 **tipologias**, cada uma com `nome`, `qtd`, `modo` (`area` para unidade construída; `qtdUnit` para estrutura pronta, que conta como unidade, como no Pilar 6) e `tagP6=unidade`. A soma das quantidades **tem de ser igual** a `unidadesFase` (bloqueia a tela);
  - na estrutura pronta: `freteMontagemConfirmados` (R33);
  - extras por unidade: deck (`tagP6=deck`), piso (`tagP6=piso`);
  - áreas comuns: apoio (rouparia, depósito, lixo, copa e vestiário), lavanderia, recepção, deck comum, trilhas, casa de máquinas (R9; P5). A caixa «por que» cita o apoio do Pilar 5.
- **Parte 4 · Mobiliário e equipamentos:** unidade-modelo, uma por tipologia, com itens em `qtdUnit` e `qtd` = unidades da tipologia (`tagP6=mobilia`): cama e colchão, mobiliário, iluminação, cozinha compacta e eletrodomésticos, banheiro, mobiliário do deck; equipamentos gerais (apoio, lavanderia, áreas comuns), sem tag.
- **Parte 5 · Enxoval, utensílios e suprimentos** (`tagP6=mobilia`): enxoval (unidades × `camasPorUnidade` 1 a 10 × **3 jogos** fixos, R17 × `custoJogo`); utensílios por unidade; governança e limpeza; recepção; manutenção; segurança; amenidades e suprimentos iniciais (R18). Campo `enxovalNaoDuplicado` (R28).
- **Parte 6 · Pré-abertura:** licença de funcionamento e cadastros (F01); fotos e anúncio; identidade e lançamento; treinamento e manual de operação; seguro do primeiro ano (F05); abertura de teste.

**Tela 9 · Parte 7, a reserva do imprevisto**

| Campo | Tipo | Obrigatório | Faixa |
|---|---|---|---|
| `reservaPct` | percentual | sim | > 0 e ≤ 50; padrão: o `reserva_pct` da página 6, se existir; "não sei" bloqueia o selo e mostra os fatores de risco |
| `regraParaQue`, `regraQuemAutoriza`, `regraComoRegistra`, `regraQuandoConfere` | texto | sim | 10 a 200 caracteres cada (R24) |

**Tela 10 · Giro e terreno**

| Campo | Tipo | Obrigatório | Faixa |
|---|---|---|---|
| `giro` | R$ | sim ("não sei" bloqueia o selo) | 0 a 100.000.000; padrão `resumo.dados.giro` da página 6, com «veio da página 6» |
| `giroMeses`, `giroCustoMensal` | número e R$ | não (calculadora de apoio) | meses 0 a 24; se usados, `giro = giroMeses × giroCustoMensal` |
| `giroZeroJustificativa` | texto | só se `giro = 0` | 10 a 200 caracteres; aceito só se `situacao = opero` ou `paraOutro` **[a confirmar por Bruno]** |
| `terrenoSituacao` | escolha | sim | já é meu; vou comprar; permuta, sociedade ou arrendamento; não sei (pré-marcado "vou comprar" se `situacao = ideia`) |
| `terrenoValor` | R$ | não | 0 a 100.000.000, ou "não sei"; padrão `resumo.dados.terreno` da página 6 |

**Tela final · Ação**

| Campo | Tipo | Obrigatório | Faixa |
|---|---|---|---|
| `acao30` | texto | sim | 10 a 300 caracteres; pré-preenchido com a ação sugerida (6.5), editável |
| `prazo` | data | sim | de `hoje` a `hoje` + 30 dias |
| `verificacao` | texto | sim | da lista de 6.5 ou escrita (10 caracteres ou mais) |
| `pdfBaixado` | booleano | — | marcado pela interface ao gerar o PDF |

### 6.2 Cálculo (saídas)
Seja `L` o conjunto de linhas das Partes 1 a 6 com origem `cotacao` ou `estimativa`.
- `valorLinha`: `valor` (modo `valor`); `qtd × valorUnit` (`qtdUnit`); `qtd × areaM2 × custoM2` (`area`); enxoval: `unidadesFase × camasPorUnidade × 3 × custoJogo`. Linhas `branco` e `naoAplica` valem 0.
- `totalParte[p] = Σ valorLinha` da parte p (p = 1 a 6); `subtotal = Σ totalParte[1..6]`.
- `reserva = subtotal × reservaPct / 100` (Parte 7) **[a confirmar por Bruno: base = subtotal das Partes 1 a 6, como PL1, F05 e o exemplo do A05; o Pilar 6 usa as unidades prontas]**.
- `capexFase = subtotal + reserva`.
- `pctParte[p] = totalParte[p] / capexFase` (p = 1 a 7; `null` se `capexFase` = 0).
- `obra = totalParte[2] + totalParte[3]`; `pctObra = obra / capexFase`.
- `custoPorUnidade = capexFase / unidadesFase` («custo por unidade, sem terreno e sem giro», F01 cap. 6 e PL1).
- `investimentoTotal = capexFase + giro`; `investimentoPorUnidade = investimentoTotal / unidadesFase` («investimento por unidade, com o giro», igual ao custo por chave do Pilar 6) **[a confirmar por Bruno: as duas medidas, com nome]**.
- `areaTotal = Σ (qtd × areaM2)` das linhas da Parte 3 com área (tipologias, extras e áreas comuns); `null` se alguma tipologia estiver sem área. `custoPorM2 = capexFase / areaTotal` (R31).
- **Contagem de linhas** (sem `naoAplica` e sem a reserva): `nLinhas` = cotacao + estimativa + branco; `nCotadas`; `pctLinhasCotadas = nCotadas / nLinhas`; `faltamParaMaioria = max(0, floor(nLinhas / 2) + 1 − nCotadas)`.
- `valorCotado = Σ valorLinha` com cotação; `pctValorCotado = valorCotado / subtotal`.
- `n3Cotacoes` = cotação com `nCotacoes` ≥ 3 e `mesmaEspec`; `nCotacoesIncompletas` = as demais com cotação.
- `cotacoesVencidas` = linhas com `hoje − dataCotacao > 90 dias` (R8; 90 dias ainda vale).
- `oseSobreFFE = totalParte[5] / totalParte[4]` (`null` se a Parte 4 = 0).
- `preAberturaSobreObra = totalParte[6] / obra` (`null` se `obra` = 0); `faltaPreAbertura = max(0, 0,05 × obra − totalParte[6])`.
- **Página 6 × 6A** (só se `pagina6Total` for número): `pagina6Cobre = pagina6Total / investimentoTotal`; `difPagina6 = investimentoTotal − pagina6Total`. Texto: «A sua página 6 cobria X% da 6A; a diferença é de R$ Y.» Nenhum julgamento.
- **Limite da página 6** (só se `limite6` for número): `folga6 = limite6 − investimentoTotal`; `dentroLimite = folga6 ≥ 0`; se dentro, `folgaEmSubtotal = folga6 / (1 + reservaPct / 100)` («quanto ainda cabe de linhas novas, já com a reserva»); `folgaPctCapex = folga6 / capexFase`.
- `infraFutura = infraProjetoCompleto − totalParte[2]`, só se informado e ≥ 0.
- **Régua de maturidade** (rótulos do P6 cap. 02 e A05 cap. 1; o critério de Calculista vem do F01 cap. 1, que se declara elaboração do módulo; os demais critérios são **elaboração própria**):
  - `Sonhador`: `capexFase` = 0, ou só a Parte 3 tem valor;
  - `Calculista`: `pctLinhasCotadas` > 0,5 **e** as três linhas de maior `valorLinha` têm cotação;
  - `Estimador`: os demais casos;
  - Developer não é atribuído aqui: pede cronograma de desembolso e captação (Pilar 7) **[a confirmar por Bruno]**.
- **Transposição para a página 6** (quadro «Como levar para a página 6»; nada é gravado na ficha do Pilar 6):
  - `unidades = unidadesFase`;
  - `l_unidade = Σ tipologias / unidadesFase`; `l_deck = Σ tag deck / unidadesFase`; `l_piso = Σ tag piso / unidadesFase` (0 com a nota «incluído no custo do m²»); `l_luz`, `l_agua` = Σ da tag / `unidadesFase`; `l_mobilia = (Σ tag mobilia da Parte 4 + totalParte[5]) / unidadesFase`;
  - `pronta = l_unidade + l_deck + l_luz + l_agua + l_mobilia + l_piso`;
  - `licencas = totalParte[1]`; `reserva_pct = reservaPct`;
  - `infra = (subtotal − unidadesFase × pronta − totalParte[1]) + reservaPct/100 × (subtotal − unidadesFase × pronta)`;
  - `giro_meses` e `terreno`: copiados da página 6 (não mudam);
  - `nota` de cada campo: 3 só se todas as linhas que o compõem forem cotação; senão 1; "Não sei" se alguma for `branco` e o campo valer 0;
  - **aviso fixo no quadro: «Digite 0 onde for zero. Em branco, a ficha do Pilar 6 usa a referência da Zion no lugar»** (conferido em `pilar6/index.html`: campos em branco recebem `REF`);
  - o texto explica que a ficha do Pilar 6 não tem linha própria para áreas comuns, equipamentos gerais, pré-abertura e a parte da reserva que não é unidade, e por isso tudo vai no campo «infraestrutura comum», com nota escrita;
  - **identidade obrigatória:** `unidadesFase × pronta × (1 + reserva_pct/100) + licencas + infra = capexFase` (tolerância R$ 0,01).
- **Resumo «Se você usa a Planilha 1»** (B3; elaboração própria a partir de `build.py`):
  - `pl1Premissas` (aba Premissas, coluna H, construção) = tipologias em modo `area` + linhas `tagP6=deck`;
  - `pl1Infraestrutura` (aba Infraestrutura, TOTAL) = Parte 1 + Parte 2 + áreas comuns da Parte 3 + Parte 6 (lançada nas linhas livres do fim da aba, com o grupo «9 · Mão de obra e gestão da obra» escolhido na coluna A e «Pré-abertura · …» escrito na coluna B, para entrar no subtotal e na contingência);
  - `pl1FFE` (aba FF&E) = linhas `tagP6=mobilia` da Parte 4 + tipologias em modo `qtdUnit` (a estrutura pronta, que a Planilha 1 põe na FF&E, linha «Bolha ou cabana (estrutura principal)»);
  - `pl1OSE` (aba OS&E) = Parte 5 + equipamentos gerais da Parte 4 (a Planilha 1 os lista em «itens de operação do projeto»);
  - contingência na aba Premissas, célula B15 = `reservaPct`;
  - **identidade obrigatória:** `pl1Premissas + pl1Infraestrutura + pl1FFE + pl1OSE = subtotal`, e o Resumo, linha TOTAL (B12), = `capexFase`.
  - Aviso: «a Planilha 1 divide o CAPEX pela área das unidades (coberta + deck, aba Premissas B16); a 6A divide pela área total da Parte 3, com as áreas comuns. Os dois números são diferentes e os dois estão certos: diga qual usou.»

### 6.3 Faixas de leitura (com a fonte de cada uma)
Todas aparecem como **«faixa de conferência citada pela fonte; não é preço nem regra fixa»** (A05 cap. 3: «não são regras fixas. São faixas de sanidade»). O e-book avisa que projeto pequeno pode cair fora delas.

| Leitura | Faixa | Fonte | Texto (ideia) |
|---|---|---|---|
| Limite da página 6 | dentro (folga ≥ 0) / acima | P6 cap. 07 (o que precisa ser verdade); P7 (critério: «se passar de cerca de R$ 870 mil… ela volta à conta antes de assinar») | dentro: «cabe, com folga de R$ X; ela ainda precisa pagar as linhas em branco»; acima: A21 |
| Reserva do imprevisto | 10% a 15% sobre o subtotal; teto ou acima com fator de risco ou primeira obra; imóvel pronto 15% a 25% | A05 caps. 3 e 7; VOL05 cap. 4; P6 cap. 03; PL1; JC02 P11; JC04 P04 | dentro / abaixo / acima de 25% (R23) |
| Enxoval, utensílios e suprimentos ÷ mobiliário e equipamentos | 10% a 15% | R16 (A05 caps. 2 e 6; F01 caps. 2 e 4) | abaixo: algo de um dia de operação ficou de fora; acima: enxoval contado duas vezes? |
| Pré-abertura ÷ obra (Partes 2 + 3) | 5% a 10% | R21 (A05 caps. 2 e 7; F01 caps. 2 e 4) | abaixo de 5%: esquecer a pré-abertura é um dos cinco erros do orçamento amador |
| Obra ÷ CAPEX | acima de 80% = «faltou algo» | R29 (A05 cap. 3; F01 cap. 6) | só o alerta de 80%; a faixa de 60% a 70% fica no e-book |
| Linhas com cotação | 0% / até 50% / mais de 50% | «maioria» do F01 cap. 1; cortes em 0 e 50% são **elaboração própria** | «um mapa do que cotar» / «a maior parte ainda é estimativa ou está em branco» / «a maioria das linhas tem cotação escrita» |
| Giro (se a calculadora for usada) | menos de 3 meses = abaixo do piso | A05 caps. 7 e 10; VOL05 cap. 4; P6 cap. 06; PL2 («3 é o mínimo prudente») | três meses são o piso citado; a conta completa do giro é a do Pilar 6 |
| Página 6 × 6A | sem faixa | P6 cap. 04 | «a sua página 6 cobria X% da 6A»; nenhum julgamento |

### 6.4 Mensagens de alerta (id, condição, fonte)
A ordem é a prioridade. A tela «Atenção» e o PDF mostram os três primeiros que dispararem.

| Id | Condição | Mensagem (ideia) | Fonte |
|---|---|---|---|
| A17 | Σ das tipologias ≠ `unidadesFase` | Bloqueia a tela 5: «as tipologias somam N, a fase tem M» | validação |
| A3z | `reservaPct` vazio ou 0 | Bloqueia o selo: «a reserva nunca é zero» | mapa 1.2 |
| A21 | `limite6` número e `investimentoTotal > limite6` | «O investimento total passou do limite que a sua página 6 escreveu (R$ X). O Pilar 7 diz o caminho: voltar à conta antes de assinar e ajustar o tamanho, o produto ou a fase.» | P6 cap. 07; P7 |
| A1 | Parte de 1 a 6 sem nenhuma linha com valor (e com alguma linha que não seja `naoAplica`) | «Parte X em branco: ela só pode aumentar a conta» | P6 (infraestrutura à parte); erros do A05 cap. 2 |
| A22 | `pagina6Total` = "não fiz" | «A 6A é a página irmã da 6. Faça a página 6 no Pilar 6 para ter o limite e comparar» (não bloqueia) | GUIA 5.1 |
| A6 | `infraDimensionadaPara` < `unidadesProjeto` | «A rede está dimensionada para menos unidades do que o projeto completo. Refazer vala e caminho na fase dois é a forma mais cara de economizar» | R14 (P6 cap. 04; A05 cap. 12; F01 cap. 6) |
| A7 | `infraDimensionadaPara` ou `unidadesProjeto` = "não sei" | «Falta dizer para quantas unidades a rede é pensada» (bloqueia o selo) | R11, R14 |
| A8 | `distanciaEnergiaM` = "não sei" | «A primeira pergunta do orçamento: a distância até o ponto de energia; a concessionária informa» | R12 (confirmar com a concessionária local) |
| A2 | Parte com valor e nenhuma linha com cotação | «Parte X sem nenhuma cotação» | R3, R5 |
| A11 | `preAberturaSobreObra` < 0,05 (inclui 0) | «Pré-abertura abaixo da faixa citada: faltam cerca de R$ X para os 5% da obra» | R21 |
| A12 | `pctObra` > 0,80 | «A obra passa de 80% do custo: provavelmente faltou algo» | R29 |
| A3 | 0 < `reservaPct` < 10 (ou < 15 se `imovelPronto`) | «Reserva abaixo da faixa citada» | 6.3 |
| A4 | `reservaPct` < 15 e (`primeiraObra` ou algum fator de risco) | «Com fator de risco ou primeira obra, a fonte pede o teto ou acima» | A05 cap. 7; R22; P6 cap. 03 (a nota da Marina: «subir para o teto da faixa») |
| A5 | `reservaPct` > 25 | «Acima de todas as faixas citadas: a reserva não está cobrindo linha esquecida ou escopo novo?» | R23 |
| A9 | `oseSobreFFE` fora de 0,10 a 0,15 | Abaixo ou acima, com a explicação de 6.3 | R16, R28 |
| A10 | `enxovalNaoDuplicado` = falso | «Confirme que o enxoval não está também na cotação do mobiliário» | R28 |
| A15 | Tipologia de estrutura pronta com `freteMontagemConfirmados` = falso | «Confirme por escrito se frete, fundação e montagem estão incluídos» | R33 (sem os 15%, que não têm fonte) |
| A13 | `cotacoesVencidas` > 0 | «N cotações com mais de 90 dias: refaça antes de usar» | R8 |
| A14 | `nCotacoesIncompletas` > 0 | «N linhas com menos de três cotações ou com escopos diferentes» | R5, R6 |
| A23 | `limite6` = "não sei" ou ausente, com página 6 feita | «Sem o limite da página 6, a 6A não diz se a conta cabe. Ele está na página 6, em "o que precisa ser verdade"» (não bloqueia) | P6 cap. 07 |
| A16 | `giroMeses` < 3 (calculadora usada) | «Giro abaixo do piso de três meses citado» | 6.3 |
| A18 | `terrenoSituacao` = vou comprar | «Escritura, imposto de transmissão e registro não estão nesta conta: pergunte ao contador. A necessidade de capital fica no Pilar 7» | lacuna 3; R27 |
| A19 | `situacao` = opero | «Não pague a obra com o caixa da operação» | F01 caps. 1 e 7 |
| A20 | Campo da regra de uso com menos de 10 caracteres | Bloqueia o selo | R24 |
| INFO | Sempre | «Pergunte ao seu engenheiro e ao seu contador» (as perguntas do checklist, sem número) e «Esta ficha não envia nada: o PDF fica só com você.» | mapa 7.1 e 7.2; GUIA I14 |

### 6.5 Feedback em cinco partes e ação de 30 dias por situação
1. **Resultado:** CAPEX da fase; investimento total; limite da página 6 e folga (ou excesso); custo por unidade e investimento por unidade; custo por m²; as sete partes com valor e peso; o terreno ao lado («fora da conta, mas não de graça»); `infraFutura`, se houver.
2. **Significado:** o degrau na régua (comparado com o do diagnóstico) e quantas linhas faltam para a maioria; linhas e valor com cotação; página 6 × 6A.
3. **Atenção:** os três primeiros alertas de 6.4 e o bloco INFO.
4. **O que fazer:** a primeira situação verdadeira, na ordem abaixo (elaboração própria, a partir das prioridades das fontes):

| Ordem | Situação | Ação sugerida de 30 dias | Como verificar |
|---|---|---|---|
| 1 | A21 (acima do limite) | Refazer a página 6 com estes números e listar, com o arquiteto ou o engenheiro, três ajustes possíveis (tamanho, produto ou fase) antes de assinar | A página 6 refeita e a lista dos ajustes, com data |
| 2 | A1 (parte em branco) | Listar as linhas da Parte X e pedir as primeiras cotações | As linhas na ficha e os pedidos enviados, com data e destinatário |
| 3 | A6, A7 ou A8 | Pedir à concessionária o ponto de energia e ao projetista o dimensionamento da rede para as N unidades do projeto completo | A resposta da concessionária e a proposta do projetista, com o número de unidades escrito |
| 4 | Há linhas `branco` | Pedir cotação escrita das linhas em branco (listadas pelo nome) | As propostas, com data e escopo, lançadas na ficha |
| 5 | Degrau ≠ Calculista | Pedir três cotações com a mesma especificação para as três maiores linhas | Três propostas por linha, com a mesma especificação anexada |
| 6 | A13 ou A14 | Refazer as cotações vencidas e completar as que têm menos de três | Datas novas e três propostas comparáveis por linha |
| 7 | A3, A4, A5, A9, A11 ou A12 | Revisar a parte apontada linha a linha, com o checklist | A parte revisada e uma nota do que mudou |
| 8 | Nada disparou | Refazer a página 6 com o quadro de transposição; se preferir planilha, passar para a Planilha 1; colar o CAPEX na Planilha 2 | A página 6 refeita, com a data das cotações, e a Planilha 2 com o CAPEX na B5 |

5. **Como verificar:** o critério da linha escolhida (ou o escrito pela pessoa, com 10 caracteres ou mais).

### 6.6 Critério de conclusão (selo «Pronto para levar à página 6»)
Todos verdadeiros:
1. Tela 1 respondida: `pagina6Total` com número, "não fiz" ou "não sei", declarado.
2. `unidadesFase` ≥ 1, `unidadesProjeto` conhecido e ≥ `unidadesFase`, e as tipologias somando `unidadesFase`.
3. Partes 1 a 6: toda linha com origem escolhida, e cada parte com pelo menos uma linha que não seja `naoAplica`. Exceção: com `imovelPronto`, as Partes 2 e 3 podem estar inteiras em `naoAplica`. A Parte 6 nunca pode.
4. `capexFase` > 0.
5. `reservaPct` > 0 e as quatro linhas da regra de uso com 10 caracteres ou mais.
6. `infraDimensionadaPara` informado (salvo Parte 2 inteira em `naoAplica`).
7. `giro` > 0, ou `giro = 0` com justificativa válida (só com `situacao = opero` ou `paraOutro`).
8. `terrenoSituacao` respondida.
9. `acao30`, `prazo` (até hoje + 30) e `verificacao` válidos.
10. `pdfBaixado` = verdadeiro.

**O selo não exige percentual mínimo de cotação nem estar dentro do limite.** A primeira versão honesta, com estimativas e linhas em branco nomeadas, conclui a lição; o degrau, o limite e a ação apontam o que falta **[a confirmar por Bruno]**. Enquanto falta algo, a tela lista o que falta, um item por linha.

### 6.7 Testes mínimos para o construtor
Pelo menos 55 testes em Node antes da interface, incluindo:
- **o caso da Marina inteiro, campo a campo** (seção 7), inclusive pesos, contagens, régua, alertas na ordem, ação, transposição, resumo da Planilha 1, página 6 × 6A e folga;
- E2 (água refeita) e E4 (as três bases da reserva);
- bordas: tipologias ≠ fase; `capexFase` = 0; Parte 4 = 0 (`oseSobreFFE` nulo); obra = 0; área ausente; reserva em 0, 10, 15, 25 e 25,01; enxoval ÷ mobiliário exatamente 10% e 15%; pré-abertura exatamente 5%; obra exatamente 80% (não alerta) e 80,01%; cotação com 90 dias (válida) e 91 (vencida); `pctLinhasCotadas` exatamente 50% (não é Calculista); `folga6` exatamente 0 (dentro, sem A21) e −0,01 (A21); `limite6` ausente com `resultado_cons` presente (usa 8 × resultado); `giroMeses` = 3; prazo em hoje + 30 (válido) e hoje + 31 (inválido); "não sei" em cada campo que o aceita; página 6 ausente (A22);
- as duas identidades (transposição e Planilha 1);
- leitura tolerante de `zion-t1-pilar6` com `resumo.dados` e com `dados` na raiz, e com JSON quebrado (campo vazio, sem erro).

Depois, o teste de ponta a ponta no celular (iPhone 13 no Playwright) mostra: sem erro de JS, sem rolagem horizontal, estado que persiste ao recarregar, leitura da página 6 semeada no `localStorage` com os números da Marina, PDF gerado com o jsPDF servido localmente e altura de uma página conferida. Teste da aula: `data-bloco` sem «ECROI» e sem «Bloco 3» a «Bloco 7».

---

## 7. Exemplo didático · a Marina abre a página 6 dela (exemplo ilustrativo)

Rótulo em todas as telas e páginas com número novo: **«Exemplo ilustrativo · dados fictícios. Não são preços de referência.»** Os números da página 6 de partida levam o rótulo da referência (5.1). **Estes são os únicos números do caso: ficha, e-book, aula, tutorial e checklist usam exatamente estes valores.** O construtor grava tudo num só arquivo de dados (5.5).

### 7.1 De onde ela parte: a página 6 da Marina (P6 cap. 04; P7)
Fatos de continuidade (GUIA 2.1, regra 4): 3 cabanas de madeira para casal, 38 m² internos + 16 m² de deck (P3), abre com 3 e desenha para 5 (P5), apoio de 30 m² = rouparia 12 + depósito 6 + lixo 4 + copa e vestiário 8 (P5), rede para 5 com duto vazio (P5), caminho do hóspede de cerca de 120 m da clareira do estacionamento (P5), deck leve na crista (P5), lavanderia terceirizada e «nunca: recepção construída» (P5), terreno dela de R$ 600 mil (P1), diária R$ 645 e 38,5% (P2), primeira obra (P6 cap. 03), opera com uma pessoa local.

| Linha da página 6 | Valor | Origem (como está no Pilar 6) |
|---|---|---|
| 1 a 6 · Três unidades prontas, com mobília | 577.038,00 | Referência orientativa da página 6, não confirmada (3 × 192.346); a Zion também vende esse tipo de estrutura |
| 7 · Licenças e projetos | 15.000,00 | Estimativa, propostas pedidas |
| 8 · Reserva do imprevisto | 57.703,80 | 10% das unidades |
| **Soma da folha** | **649.741,80** | |
| Capital de giro | 40.787,38 | Três meses de custo (60% × 271.915,88 ÷ 12 × 3) |
| **Investimento total da fase um** | **690.529,18** | Cerca de R$ 690 mil |
| À parte · terreno | fora da conta (R$ 600 mil) | Da Marina |
| À parte · infraestrutura comum | «a cotar» | Acesso, caminhos, estacionamento e vaga de serviço, apoio de 30 m², deck da crista, rede para cinco (P6 cap. 03) |
| O que precisa ser verdade | investimento total até 8 × 108.766,35 = **870.130,80** | «Até cerca de R$ 870 mil» (P6 cap. 07); folga de 179.601,62 «para a infraestrutura comum e para as cotações» |

Conferência (P6): 577.038 + 15.000 = 592.038; + 57.703,80 = 649.741,80; + 40.787,38 = 690.529,18. Bate. Limite: 1.095 × 0,385 × 645 = 271.915,875; × 0,40 = 108.766,35; × 8 = 870.130,80. Bate.

### 7.2 Premissas da 6A
- Situação «Tenho um terreno e ainda não hospedo ninguém»; tipo cabanas ou chalés; imóvel novo; não é para outra pessoa.
- Diagnóstico: d1 «referência ou estimativa»; d2 «nenhuma»; d3 «nenhuma»; d4 «não» → degrau de partida **Estimador**.
- Tela 1: `pagina6Total` 690.529,18 (data da página 6 dela); `pagina6Infra` «à parte, a cotar»; `limite6` 870.130,80.
- Fase um: 3 unidades; projeto completo: 5; primeira obra: sim; fatores de risco: nenhum marcado.
- Distância até o ponto de energia: **260 m** (informada pela concessionária, no exemplo; o pedido foi feito no Pilar 5). Rede dimensionada para **5**. `infraProjetoCompleto` em branco (a rede para 5 já está nas linhas da fase um).
- "Hoje" do exemplo: **27/11/2026**.

Legenda: C = cotação (número de propostas; «=» = mesma especificação); E = estimativa; B = em branco; NA = não se aplica. «Aba PL1» = onde a linha vai na Planilha 1.

### 7.3 A tabela completa

**Parte 1 · Projetos, licenças e documentação**

| Linha | Modo e conta | Origem | Data | Valor (R$) | Tag P6 | Aba PL1 |
|---|---|---|---|---|---|---|
| Levantamento topográfico e sondagem do solo | valor | C3= | 02/10/2026 | 6.200 | — | Infraestrutura · 1 |
| Projeto de arquitetura (3 cabanas, apoio e implantação da fase um) | valor | C3= | 09/10/2026 | 16.500 | — | Infraestrutura · 1 |
| Projetos complementares (estrutural, elétrico, hidrossanitário) | valor | C2= | 14/10/2026 | 9.800 | — | Infraestrutura · 1 |
| Aprovação na prefeitura e taxas | valor | E | — | 2.500 | — | Infraestrutura · 1 |
| Responsabilidade técnica e registros | valor | E | — | 1.000 | — | Infraestrutura · 1 |
| Licença ambiental, se houver (aguarda a resposta da prefeitura, P5) | — | B | — | 0 | — | Infraestrutura · 1 |
| **Total da Parte 1** | | | | **36.000** | | |

**Parte 2 · Infraestrutura** (rede para 5; energia a 260 m)

| Linha | Modo e conta | Origem | Data | Valor (R$) | Tag P6 | Aba PL1 |
|---|---|---|---|---|---|---|
| Acesso interno até a clareira (cascalho e drenagem lateral) | valor | C3= | 20/10/2026 | 24.000 | — | Infraestrutura · 3 |
| Estacionamento na clareira (5 vagas de hóspede + 1 de serviço) | valor | C2= | 20/10/2026 | 7.200 | — | Infraestrutura · 3 |
| Caminho do hóspede pela mata, com luz baixa | 120 m × 140 | C2= | 22/10/2026 | 16.800 | — | Infraestrutura · 3 |
| Energia: padrão de entrada e rede enterrada até as 5 posições, com duto vazio para a 4ª e a 5ª | valor | C1 | 05/11/2026 | 31.500 | — | Infraestrutura · 4 |
| Água: poço com teste de vazão, reservatório e rede para 5 | valor | C2= | 15/07/2026 (**vencida**, 135 dias) | 19.800 | — | Infraestrutura · 5 |
| Esgoto: tratamento dimensionado para 5 (sistema definido pelo projetista) | valor | E | — | 14.500 | — | Infraestrutura · 5 |
| Drenagem das plataformas e do caminho | valor | E | — | 4.200 | — | Infraestrutura · 2 |
| Internet para o hóspede que trabalha de domingo a quinta (P3) | — | B | — | 0 | — | Infraestrutura · 6 |
| Ligação de luz de cada cabana | 3 × 1.800 | E | — | 5.400 | `luz` | Infraestrutura · 4 |
| Água e esgoto de cada cabana | 3 × 1.600 | E | — | 4.800 | `agua` | Infraestrutura · 5 |
| **Total da Parte 2** | | | | **128.200** | | |

**Parte 3 · Unidades e áreas comuns**

| Linha | Modo e conta | Origem | Data | Valor (R$) | Tag P6 | Aba PL1 |
|---|---|---|---|---|---|---|
| Cabanas de madeira (tipologia única; piso incluído no m²) | 3 × 38 m² × 2.800 | C3= | 28/10/2026 | 319.200 | `unidade` | Premissas linha 11 (C 38, E 2.800) |
| Deck de cada cabana | 3 × 16 m² × 700 | C2= | 28/10/2026 | 33.600 | `deck` | Premissas linha 11 (D 16, F 700) |
| Apoio de 30 m² (rouparia 12, depósito 6, lixo 4, copa e vestiário 8) | 1 × 30 m² × 2.200 | C1 | 30/10/2026 | 66.000 | — | Infraestrutura · 7 |
| Deck leve da crista | 1 × 16 m² × 600 | E | — | 9.600 | — | Infraestrutura · 7 |
| **Total da Parte 3** | | | | **428.400** | | |

Área total da Parte 3: 3 × 38 + 3 × 16 + 30 + 16 = 114 + 48 + 30 + 16 = **208 m²**. `freteMontagemConfirmados` não se aplica (cabana construída, não estrutura pronta).

**Parte 4 · Mobiliário e equipamentos** (unidade-modelo × 3)

| Linha | Modo e conta | Origem | Data | Valor (R$) | Tag P6 | Aba PL1 |
|---|---|---|---|---|---|---|
| Cama e colchão de hotel | 3 × 5.200 | C3= | 03/11/2026 | 15.600 | `mobilia` | FF&E |
| Mobiliário (sofá pequeno, mesa de trabalho e cadeira, armário, mesas de cabeceira) | 3 × 7.400 | C2= | 03/11/2026 | 22.200 | `mobilia` | FF&E |
| Iluminação | 3 × 1.900 | E | — | 5.700 | `mobilia` | FF&E |
| Cozinha compacta e eletrodomésticos | 3 × 4.300 | C3= | 06/11/2026 | 12.900 | `mobilia` | FF&E |
| Banheiro (metais, espelho, acessórios) | 3 × 2.600 | E | — | 7.800 | `mobilia` | FF&E |
| Mobiliário do deck (o café na varanda, P3) | 3 × 1.800 | E | — | 5.400 | `mobilia` | FF&E |
| Equipamentos do apoio (carrinho de camareira, prateleiras da rouparia) | valor | E | — | 2.400 | — | OS&E (itens de operação) |
| **Total da Parte 4** | unidade-modelo 23.200 × 3 = 69.600; + 2.400 | | | **72.000** | | |

**Parte 5 · Enxoval, utensílios e suprimentos** (`enxovalNaoDuplicado` = sim)

| Linha | Modo e conta | Origem | Data | Valor (R$) | Tag P6 | Aba PL1 |
|---|---|---|---|---|---|---|
| Enxoval (lavanderia terceirizada, três jogos mesmo assim) | 3 cabanas × 1 cama × 3 jogos × 780 | C3= | 06/11/2026 | 7.020 | `mobilia` | OS&E |
| Utensílios de cozinha | 3 × 400 | E | — | 1.200 | `mobilia` | OS&E |
| Governança e limpeza | valor | E | — | 900 | `mobilia` | OS&E |
| Recepção | — | NA (nenhuma recepção construída, P5) | — | 0 | — | — |
| Manutenção (ferramentas básicas) | valor | E | — | 600 | `mobilia` | OS&E |
| Segurança (extintores, primeiros socorros, lanternas) | — | B | — | 0 | `mobilia` | OS&E |
| Amenidades e suprimentos do primeiro mês | valor | E | — | 1.020 | `mobilia` | OS&E |
| **Total da Parte 5** | | | | **10.740** | | |

**Parte 6 · Pré-abertura** (não estava na página 6)

| Linha | Modo e conta | Origem | Data | Valor (R$) | Tag P6 | Aba PL1 |
|---|---|---|---|---|---|---|
| Licença de funcionamento e cadastros | — | B | — | 0 | — | Infraestrutura · linha livre (grupo 9) |
| Fotos profissionais e anúncio | valor | C2= | 10/11/2026 | 4.800 | — | idem |
| Identidade e lançamento | valor | E | — | 3.500 | — | idem |
| Treinamento da pessoa local e manual de operação | valor | E | — | 2.500 | — | idem |
| Seguro do primeiro ano | — | B | — | 0 | — | idem |
| Abertura de teste (noites com convidados, consumo e ajustes) | valor | E | — | 1.800 | — | idem |
| **Total da Parte 6** | | | | **12.600** | | |

**Parte 7 · Reserva do imprevisto**
- A Marina começa com os 10% da página 6 → reserva de 68.794 → aparece **A4** (primeira obra abaixo de 15%) → ela sobe para **15%**, como a própria página 6 já anotava («se as cotações vierem com muita incerteza, subir para o teto da faixa», P6 cap. 03).
- 687.940 × 0,15 = **R$ 103.191**.
- Regra de uso, nas quatro linhas: para quê: imprevisto da obra orçada (solo, chuva, reajuste, exigência da licença); quem autoriza: a Marina, depois de ouvir o engenheiro; como se registra: planilha com data, motivo e valor; quando se confere: a cada medição da obra. O ofurô na crista, se aparecer no meio da obra, é linha nova e decisão, não reserva (P6).

### 7.4 A conta

| Parte | Total (R$) | Peso no CAPEX (sem arredondar) | Peso exibido | Cotado (R$) | Estimado (R$) | Linhas C / E / B / NA |
|---|---|---|---|---|---|---|
| 1 · Projetos, licenças e documentação | 36.000 | 0,045504 | 4,6% | 32.500 | 3.500 | 3 / 2 / 1 / 0 |
| 2 · Infraestrutura | 128.200 | 0,162047 | 16,2% | 99.300 | 28.900 | 5 / 4 / 1 / 0 |
| 3 · Unidades e áreas comuns | 428.400 | 0,541503 | 54,2% | 418.800 | 9.600 | 3 / 1 / 0 / 0 |
| 4 · Mobiliário e equipamentos | 72.000 | 0,091009 | 9,1% | 50.700 | 21.300 | 3 / 4 / 0 / 0 |
| 5 · Enxoval, utensílios e suprimentos | 10.740 | 0,013576 | 1,4% | 7.020 | 3.720 | 1 / 4 / 1 / 1 |
| 6 · Pré-abertura | 12.600 | 0,015927 | 1,6% | 4.800 | 7.800 | 1 / 3 / 2 / 0 |
| **Subtotal (Partes 1 a 6)** | **687.940** | | | **613.120** | **74.820** | **16 / 18 / 5 / 1** |
| 7 · Reserva do imprevisto (15%) | 103.191 | 0,130435 (= 0,15 ÷ 1,15) | 13,0% | | | |
| **CAPEX da fase** | **791.131** | 1,000001 | 100,1% (nota: «a soma arredondada pode dar 99,9% ou 100,1%») | | | |
| Capital de giro (veio da página 6) | 40.787,38 | | | | | |
| **Investimento total da fase um** | **831.918,38** | | | | | |
| Limite da página 6 | 870.130,80 | | | | | |
| **Folga** | **38.212,42** | dentro do limite | | | | |
| À parte · terreno (já é dela) | 600.000 | não somado | | | | |

Medidas:
- **Custo por unidade** (sem giro e sem terreno): 791.131 ÷ 3 = **R$ 263.710,33**.
- **Investimento por unidade** (com o giro; o "custo por chave" do Pilar 6): 831.918,38 ÷ 3 = **R$ 277.306,13** (na página 6 era R$ 230.176,39).
- **Custo por m²**: 791.131 ÷ 208 = **R$ 3.803,51**. (Na Planilha 1, dividindo só pela área das cabanas e decks, 162 m²: 791.131 ÷ 162 = R$ 4.883,52.)
- **Obra** (Partes 2 + 3) = 556.600 → 556.600 ÷ 791.131 = **70,4%** do CAPEX: menos de 80%, sem alerta (o e-book comenta que fica um pouco acima dos 60% a 70% citados pelo A05, comum em projeto pequeno).
- **Enxoval, utensílios e suprimentos ÷ mobiliário**: 10.740 ÷ 72.000 = **14,9%** → dentro da faixa.
- **Pré-abertura ÷ obra**: 12.600 ÷ 556.600 = **2,3%** → **A11**. Para os 5%: 0,05 × 556.600 = 27.830; faltam **R$ 15.230**.
- **Reserva de 15% com primeira obra** → dentro. **Rede para 5 = projeto completo** → sem A6.

Linhas e cotações:
- 39 linhas contadas (a recepção, NA, fica fora): **16 com cotação, 18 estimativas, 5 em branco**. `pctLinhasCotadas` = 16 ÷ 39 = **41,0%**.
- Valor cotado: 613.120 ÷ 687.940 = **89,1%** do subtotal.
- As três maiores linhas (cabanas 319.200, apoio 66.000, decks 33.600) têm cotação, mas as linhas cotadas não são a maioria → degrau **Estimador** (o mesmo do diagnóstico). Faltam **4 linhas cotadas** para a maioria (20 ÷ 39 = 51,3%). Se as cinco linhas em branco virarem cotação, ficam 21 ÷ 39 = 53,8% e ela chega a **Calculista**.
- Cotações completas (3 ou mais, mesma especificação): **7** (levantamento, arquitetura, acesso, cabanas, cama e colchão, cozinha compacta, enxoval). Incompletas: **9** (energia e apoio com 1; complementares, estacionamento, caminho, água, decks, mobiliário e fotos com 2). Vencidas: **1** (água, 135 dias).

**Página 6 × página 6A:** 690.529,18 ÷ 831.918,38 = **83,0%**; diferença de **R$ 141.389,20**. De onde vem a diferença (para o e-book, cap. 09, sem adjetivo, regra 5.1):

| O que mudou da página 6 para a 6A | Página 6 (R$) | Página 6A (R$) | Diferença (R$) |
|---|---|---|---|
| Entrou o que estava à parte ou não estava (infraestrutura comum 118.000; áreas comuns 75.600; equipamentos do apoio 2.400; pré-abertura 12.600) | 0 | 208.600 | + 208.600 |
| Licenças e projetos | 15.000 | 36.000 | + 21.000 |
| Reserva do imprevisto (base e percentual novos) | 57.703,80 | 103.191,00 | + 45.487,20 |
| As seis linhas por cabana, agora com cotação e estimativa (escopo diferente: a rede comum foi para a Parte 2) | 577.038 | 443.340 | − 133.698 |
| Capital de giro | 40.787,38 | 40.787,38 | 0 |
| **Total** | **690.529,18** | **831.918,38** | **+ 141.389,20** |

**Leitura do limite:** dentro, com folga de **R$ 38.212,42** (cerca de 4,8% do CAPEX). Já com a reserva de 15%, a folga paga **R$ 33.228,19** de linhas novas (38.212,42 ÷ 1,15). Desse valor, R$ 15.230 vão para a pré-abertura chegar aos 5% da obra, e sobram **R$ 17.998,19** para as cinco linhas em branco (licença ambiental, internet, segurança, licença de funcionamento e seguro do primeiro ano). Frase do e-book (ideia): «Cabe, mas a folga é fina, e as linhas em branco só podem aumentar a conta.»

**Alertas, na ordem:** A11 (pré-abertura), A13 (água vencida), A14 (9 linhas com menos de três cotações). Não disparam: A21 (dentro do limite), A1, A2, A3, A4 (já em 15%), A6, A7, A8, A9, A12, A22, A23.

**Ação sugerida** (ordem 4, há linhas em branco): «Pedir cotação escrita da licença ambiental, da internet, da segurança, da licença de funcionamento e do seguro do primeiro ano.» Prazo: **27/12/2026**. Verificação: «as cinco propostas, com data e escopo, lançadas na ficha». (Com elas, a Marina passa a Calculista.)

### 7.5 Quadro «Como levar para a página 6» (ficha do Pilar 6, campo a campo)

| Campo da ficha do Pilar 6 | Valor | Nota | Conta |
|---|---|---|---|
| Unidades | 3 | — | — |
| 1 · A unidade (`l_unidade`) | 106.400 | 3 | 319.200 ÷ 3 |
| 2 · Deck (`l_deck`) | 11.200 | 3 | 33.600 ÷ 3 |
| 3 · Luz (`l_luz`) | 1.800 | 1 | 5.400 ÷ 3 |
| 4 · Água e esgoto (`l_agua`) | 1.600 | 1 | 4.800 ÷ 3 |
| 5 · Mobiliário, equipamentos e enxoval (`l_mobilia`) | 26.780 | 1 | (69.600 + 10.740) ÷ 3 = 80.340 ÷ 3 |
| 6 · Piso interno (`l_piso`) | **0, digitado** | — | incluído no custo do m² (em branco, a ficha usaria a referência) |
| Unidade pronta (calculada pela ficha) | 147.780 | — | 106.400 + 11.200 + 1.800 + 1.600 + 26.780 + 0 |
| 7 · Licenças e projetos (`licencas`) | 36.000 | 1 | Parte 1 (tem estimativa e uma linha em branco) |
| 8 · Reserva do imprevisto (`reserva_pct`) | 15% | — | — |
| À parte · Infraestrutura comum (`infra`) | 245.290 | 1 | (687.940 − 443.340 − 36.000) + 0,15 × (687.940 − 443.340) = 208.600 + 36.690 |
| Capital de giro (`giro_meses`) | 3 (não muda) | — | a ficha recalcula 40.787,38 |
| Terreno | 600.000 (não muda) | — | — |

Conferência: 3 × 147.780 = 443.340; × 1,15 = 509.841; + 36.000 = 545.841; + 245.290 = **791.131** = CAPEX. Bate. Pelo outro caminho: reserva das unidades 0,15 × 443.340 = 66.501; reserva do resto 36.690; 66.501 + 36.690 = 103.191. Bate.

**O que a página 6 refeita vai mostrar** (contas da própria ficha do Pilar 6, conferidas aqui; para o roteirista, sem mexer na ficha): soma da folha 545.841; infraestrutura comum 245.290; investimento total **831.918,38**; custo por chave 277.306,13; tempo de volta no conservador 831.918,38 ÷ 108.766,35 = **7,65 anos** (7 anos e 8 meses), dentro da régua de 8; limite 870.130,80 e folga 38.212,42 (iguais aos da 6A); diária até onde aguenta: 831.918,38 ÷ 8 ÷ 0,40 = 259.974,49; ÷ 421,575 = **cerca de R$ 617** (antes, cerca de R$ 512); com o terreno somado, (831.918,38 + 600.000) ÷ 108.766,35 = **13,17 anos** (antes, 11,87): a razão escrita da Marina no Dossiê («com o terreno somado, perto de doze») passa a «cerca de treze», e a regra do Pilar 6 («acima de 12 anos, só com uma razão escrita») continua atendida porque a razão existe. Peso do terreno: 600.000 ÷ 1.431.918,38 = 41,9%.

### 7.6 Resumo «Se você usa a Planilha 1» (caso da Marina)

| Aba da Planilha 1 | Partes da 6A | Valor (R$) |
|---|---|---|
| Premissas, linha 11 «Bolha ou cabana de glamping» (B11 = 3; C11 = 38; D11 = 16; E11 = 2.800; F11 = 700 → G11 = 117.600; H11 = 352.800). Linhas 9 e 10 em zero | cabanas + decks da Parte 3 | 352.800 |
| Infraestrutura (grupos 1 a 7 e linhas livres do grupo 9 para a pré-abertura) | Parte 1 + Parte 2 + áreas comuns da Parte 3 + Parte 6 = 36.000 + 128.200 + 75.600 + 12.600 | 252.400 |
| FF&E (lista «Bolha ou cabana»: zerar «Bolha ou cabana (estrutura principal)» e «Base plana ou deck de apoio», porque a cabana construída e o deck já estão na Premissas) | unidade-modelo da Parte 4 | 69.600 |
| OS&E | Parte 5 + equipamentos do apoio = 10.740 + 2.400 | 13.140 |
| Resumo · Subtotal (B10) | | 687.940 |
| Premissas B15 · contingência | 15% | 103.191 |
| **Resumo · TOTAL (B12)** | = CAPEX da 6A | **791.131** |

Conferência: 352.800 + 252.400 + 69.600 + 13.140 = 687.940. Bate. A Resumo mostra a contingência em 13,0% do total (103.191 ÷ 791.131), o mesmo peso da Parte 7.

**Planilha 2 · Estudo de Massas e Viabilidade, aba Investimento** (I5): B5 = **791.131** (o CAPEX da fase; «CAPEX de abertura (Planilha 1 · Resumo)»); B6 = **0** (terreno fora da conta, como na 6A); B7 = 3 meses; B9 = B7 × B8 (custo fixo mensal da aba Modelo de renda). Se o giro da B9 não bater com os R$ 40.787,38 da 6A, é porque a Planilha 2 usa meses × custo fixo e o Pilar 6 usa meses × custo do cenário conservador: anote os dois e fique com o maior, como o Pilar 6 faz com as duas contas de giro no cap. 06 (elaboração própria a partir de P6 cap. 06).

### 7.7 Conferência dupla (feita duas vezes, por caminhos diferentes)
- Subtotal por partes: 36.000 + 128.200 = 164.200 → + 428.400 = 592.600 → + 72.000 = 664.600 → + 10.740 = 675.340 → + 12.600 = **687.940**.
- Subtotal por origem: 613.120 cotado + 74.820 estimado = **687.940**. Bate.
- Cotado por parte: 32.500 + 99.300 + 418.800 + 50.700 + 7.020 + 4.800 = 613.120. Estimado por parte: 3.500 + 28.900 + 9.600 + 21.300 + 3.720 + 7.800 = 74.820. Bate.
- Subtotal pelas abas da Planilha 1: 352.800 + 252.400 + 69.600 + 13.140 = 687.940. Bate.
- Linhas: Parte 1 = 6.200 + 16.500 + 9.800 + 2.500 + 1.000 = 36.000; Parte 2 = 24.000 + 7.200 + 16.800 + 31.500 + 19.800 + 14.500 + 4.200 + 5.400 + 4.800 = 128.200; Parte 3 = 319.200 + 33.600 + 66.000 + 9.600 = 428.400; Parte 4 = (5.200 + 7.400 + 1.900 + 4.300 + 2.600 + 1.800) × 3 + 2.400 = 23.200 × 3 + 2.400 = 72.000; Parte 5 = 7.020 + 1.200 + 900 + 600 + 1.020 = 10.740; Parte 6 = 4.800 + 3.500 + 2.500 + 1.800 = 12.600. Bate.
- Reserva: 10% de 687.940 = 68.794; metade = 34.397; soma = **103.191**. Bate.
- CAPEX: 687.940 + 103.191 = 791.131; e 687.940 × 1,15 = 791.131. Bate.
- Investimento total: 791.131 + 40.787,38 = 831.918,38; folga: 831.918,38 + 38.212,42 = 870.130,80. Bate.
- Página 6 × 6A: 208.600 + 21.000 + 45.487,20 − 133.698 = 141.389,20; 690.529,18 + 141.389,20 = 831.918,38. Bate.
- Pesos: 0,045504 + 0,162047 + 0,541503 + 0,091009 + 0,013576 + 0,015927 + 0,130435 = 1,000001 (arredondamento de 6 casas). Bate.
- Custo por m²: 3.803,51 × 208 = 791.130,08 (R$ 0,92 de arredondamento dos centavos). Custo por unidade: 263.710,33 × 3 = 791.130,99. Investimento por unidade: 277.306,13 × 3 = 831.918,39. Bate.
- Folga em subtotal: 33.228,19 × 1,15 = 38.212,42. Bate.
- Dias da água: 15/07 → 27/11/2026 = 16 + 31 + 30 + 31 + 27 = 135. Bate.
- E2: 690.540 × 1,15 = 794.121; 794.121 + 40.787,38 = 834.908,38; 870.130,80 − 834.908,38 = 35.222,42. Bate. E4: 443.340 × 0,10 = 44.334; 103.191 − 68.794 = 34.397. Bate.
- Página 6 refeita: 831.918,38 ÷ 108.766,35 = 7,6487; (831.918,38 + 600.000) ÷ 108.766,35 = 13,1651; 259.974,49 ÷ 421,575 = 616,67. Bate.

### 7.8 Nexo com a sequência do curso (para o roteirista)
- **De onde vem:** do Pilar 6, que deixou escrito «Antes de assinar, ela troca cada linha por cotação escrita, soma a infraestrutura comum do terreno e confere os dois limites» (P6 cap. 07), e do Pilar 5 (fase um congelada, apoio, rede para 5).
- **Para onde vai:** Planilha 1 (se preferir planilha) → Planilha 2, aba Investimento → sensibilidade do Mapa (diária −15%, ocupação −10 pontos, CAPEX +20%) → refazer a página 6 → Pilar 7.
- **Pilar 7:** a decisão da Marina no Pilar 7 é «Avançar com a fase um de três cabanas. O próximo passo: trocar cada referência por cotação escrita e orçar a infraestrutura comum do terreno», com o critério «se o investimento total, com as cotações e a infraestrutura comum, passar de cerca de R$ 870 mil… ela volta à conta» (ficha do Pilar 7). A 6A é esse passo: o total fica em R$ 831.918,38, dentro do critério, e a decisão continua de pé. O plano de 90 dias termina com «Dias 61 a 90 · Decidir: refaz a página 6 com os números cotados»: a 6A é a ferramenta desse passo, que você pode fazer já e refazer a cada cotação.
- **Aviso no cap. 11 e no slide «Próximo»** (ideia): «No Pilar 7 você vai ver a Marina com o número da página 6 de referência, cerca de R$ 690 mil, porque ele foi escrito antes das cotações. Com a 6A, o investimento dela passa a ser cerca de R$ 832 mil, e o critério de R$ 870 mil continua de pé.»
- **Sensibilidade (alerta de coerência):** o teste «CAPEX +20%» do Mapa, feito na etapa seguinte, leva a Marina a 791.131 × 1,2 = 949.357,20; + 40.787,38 = **990.144,58**, acima do limite. A 6A **não** calcula esse teste nem antecipa o veredito: diz que ele é a próxima etapa, que a reserva de 15% já está dentro do CAPEX e que a decisão é do Pilar 7 **[a confirmar por Bruno: como o curso trata o resultado do teste de estresse da Marina]**.

---

## 8. Versão autônoma e versão do acompanhamento Zion 360°

| Camada | Autônomo (Trilha 1) | Acompanhamento Zion 360° |
|---|---|---|
| Conteúdo e ferramentas | As cinco peças (aula, ficha, tutorial, e-book com exercícios, checklist) | Idênticas |
| Ritmo | Liberado com o Pilar 6, depois do tutorial da ficha e antes da Planilha 1; sugestão: uma semana para a primeira versão e 30 dias para trocar as linhas por cotação | Na semana do Pilar 6 do calendário da turma; a página 6A é levada ao encontro do Pilar 6 |
| Modelagem | Tutorial e exemplo resolvido da Marina | E mais: a equipe Zion preenche ao vivo um caso real anonimizado com a ficha |
| Comentário da equipe | Feedback automático da ficha; comentários da aula lidos como insumo de melhoria | A equipe Zion comenta a 6A em dois marcos: a primeira versão (todas as linhas com origem) e a versão cotada (antes de refazer a página 6) |
| Rubrica (FABRICA seção 7, adaptada) | Autoavaliação de 4 perguntas no fim da ficha: partes completas? origem de cada número? reserva com regra? ação verificável? | **Coerência 40** (sete partes completas, a conta fecha, as duas identidades conferem, a comparação com o limite está certa); **Justificativa 30** (origem de cada número, três cotações com a mesma especificação); **Riscos 20** (linhas em branco nomeadas, reserva e regra, infraestrutura para o projeto completo, perguntas ao engenheiro e ao contador); **Clareza 10** (a página lida por um terceiro sem explicação) |
| Conclusão | Selo e PDF | Selo, PDF e revisão aprovada da equipe no marco |
| Na ficha (`turma`) | Próxima etapa: «Salve o PDF na pasta Meu Dossiê, refaça a página 6 e siga para a Planilha 1 ou a Planilha 2» | Próxima etapa: «Leve a página 6A ao encontro do Pilar 6 e refaça a página 6 depois do comentário da equipe» |
| O que não se promete | Resultado, preço certo, aprovação | Idem; nem revisão técnica de engenharia, aprovação de projeto, crédito ou parceria |

---

## 9. Próxima etapa (na ficha, no e-book e na aula), na ordem do Mapa (MAPA etapa 6; GUIA 5.4)
1. **Salvar** o PDF da página 6A na pasta Meu Dossiê, ao lado da página 6.
2. **Refazer a página 6** na ficha do Pilar 6 (`docs/trilha1/pilar6/`) com o quadro «Como levar para a página 6», campo a campo, com a nota de cada campo, e **digitando 0 onde for zero**.
3. **Planilha 1 · Orçamento de Abertura** (opcional, se preferir planilha): lançar pelo resumo «Se você usa a Planilha 1» e conferir se o Resumo, linha TOTAL (B12), bate com o CAPEX da 6A.
4. **Planilha 2 · Estudo de Massas e Viabilidade, aba Investimento:** colar o CAPEX da fase na célula **B5**, deixar o terreno em zero na **B6** (para mantê-lo fora da conta, como na 6A) e conferir se o giro da **B9** bate com o da 6A.
5. **Sensibilidade do Mapa** (diária −15%, ocupação −10 pontos, CAPEX +20%) e voltar à ficha para refazer a página 6.
6. **Pilar 7:** a necessidade de capital, o custo da captação e o pedido. O plano de 90 dias: «Dias 61 a 90 · Decidir: refaz a página 6 com os números cotados».

**Fora do próximo passo** (I6, GUIA 5.10): Ferramenta 05 · Orçamento da Cabana (produto avulso) e Calculadora de Implantação (bônus que não está em todas as turmas) não aparecem em nenhuma peça. Ficam só como fonte de nomes de linha neste plano.

---

## 10. Arquivos que a produção vai criar ou refazer (resumo para o orquestrador)
`producao/trilha1-aprofundamento/01-capex/`:
- `PLANO.md` (este arquivo);
- `src/caso.py` (o caso da Marina, fonte única dos números), `src/logic.js`, `tests/test_logic.js`, `tests/test_e2e.js`, `tests/test_aula.js`;
- `src/estilo.py` (Playfair + Inter e paleta da Trilha 1), `src/build_ebook.py`, `src/build_checklist.py`, `src/render.js`, `src/build_capas.js`;
- `tutorial/ficha-pilar6a.json` e `ROTEIRO.md` (substituem `tutorial/capex.json`);
- `ROTEIRO_APRESENTACAO.md` (refeito com a Marina e os `data-bloco` novos);
- `RELATORIO.md`, com testes e ids.

Publicação (renomeações antes de ligar as aulas, O5 **[a confirmar por Bruno]**):
- `docs/trilha1/pilar6a/index.html` (era `docs/trilha1/capex/`);
- `docs/trilha1/apresentacao/pilar6a-aula/index.html` (era `capex-aula/`);
- `docs/trilha1/materiais/Pilar-6A-CAPEX-ebook.pdf` e `Pilar-6A-CAPEX-checklist.pdf` (eram `CAPEX-Aprenda-o-passo-a-passo-ebook.pdf` e `CAPEX-Checklist.pdf`);
- `docs/trilha1/capas/p6a-c-aula.jpg`, `p6a-c-faca.jpg`, `p6a-c-tutorial.jpg`, `p6a-c-ebook.jpg`, `p6a-c-check.jpg` (eram `capex-c-*.jpg`);
- `docs/trilha1/videos/tutoriais/tutorial-ficha-pilar6a.mp4` (só depois de gravado).
- Os arquivos antigos saem só na mesma sessão em que as aulas do ClickMax forem reapontadas, para nenhum link quebrar.

---

## 11. Lacunas de fonte e padrões assumidos

**Lacunas (declaradas, não preenchidas):**
1. Nenhum preço de referência confiável e datado (as faixas do A05 são ilustrativas e de rascunho; as do P6 são referência da Zion Glamping Store, não confirmadas, com conflito de interesse declarado). A lição não dá preço e ensina a cotar.
2. Custo unitário básico do estado (CUB): só a PL1 cita, sem explicar. Fica fora da ficha e entra no checklist como pergunta ao engenheiro.
3. Encargos, administração e BDI da obra; frete e montagem em área remota (o "mais de 15%" da PL1 não tem fonte); reajuste até a compra; custos de aquisição do terreno (ITBI, escritura, registro). Só como perguntas do checklist e do bloco INFO, sem número.
4. Seguro de obra e do primeiro ano: entra a linha (F05), sem regra de valor.
5. Custo financeiro durante a obra (juros): fora desta conta, remetido ao Pilar 7.
6. Tecnologia (sistema de reservas, fechaduras): sem parte própria nas fontes; entra como linha livre na Parte 2 ou 4.
7. Imóvel pronto ou apartamento: não há lista de adequação nas fontes; a ficha permite «Adequação e reforma» com linhas livres e a régua de reserva de reforma (JC04 P04).
8. Teste da Fase Mínima Viável™ (Volume 04, via F01): fonte primária não lida. Não entra.
9. Nenhuma faixa percentual tem base estatística declarada: todas aparecem como «faixa de conferência citada pela fonte».
10. A distância até o ponto de energia da Marina, as cotações, as datas e as áreas do deck da crista não existem em nenhum pilar: são números fictícios desta lição, rotulados.
11. O e-book do Pilar 6 atribui as citações do A05 a «Volume 05 · Investimento»; esta lição segue o GUIA (I13) e atribui ao «Volume A05 · Investimento». A diferença fica registrada para Bruno.

**Padrões assumidos (elaboração própria, rotulada):**
- base da reserva no subtotal das Partes 1 a 6;
- estrutura pronta como unidade (Parte 3), seguindo o P6 contra a PL1, com o aviso de onde ela fica na Planilha 1;
- pré-abertura conferida contra a obra (Partes 2 + 3);
- critérios de Sonhador e Estimador e os cortes de 0 e 50% nas linhas cotadas;
- ordem das ações de 30 dias, incluindo o A21 em primeiro;
- a transposição para a página 6 e o mapeamento para as abas da Planilha 1 (pré-abertura nas linhas livres do grupo 9; equipamentos gerais na OS&E);
- a leitura «folga em subtotal» e a regra «fique com o maior giro» entre a Planilha 2 e a página 6;
- enxoval com três jogos fixos;
- giro zero só para quem já opera ou faz para outra pessoa;
- validações de faixa dos campos;
- a caixa «Estou fazendo para o projeto de outra pessoa» (o Marco Zero não tem essa opção);
- todos os números novos do caso da Marina (seção 7).

---

## 12. A confirmar por Bruno
1. Terreno fora do CAPEX (anotado à parte); giro ao lado e somado no investimento total; custo da captação no Pilar 7.
2. Sete partes (como o F01), chamadas «Parte 1 a 7»; nomes na tela sem sigla; «CAPEX» mantido no nome da lição e da página, sempre explicado.
3. Percentuais só como faixa de conferência citada pela fonte, nunca como preço.
4. Nenhum preço de referência; linha sem cotação em branco e contada como risco; permissão para «estimativa minha».
5. **A Marina como caso (Opção A), com os números fictícios da seção 7**, incluindo o resultado «dentro do limite, com folga de R$ 38.212,42».
6. A comparação página 6 × 6A mostra as seis linhas por cabana passando de 577.038 (referência) para 443.340 (cotação e estimativa, com a rede comum em outra parte). A regra de redação proíbe comparar linha a linha e dar adjetivo. Bruno confirma se aceita essa linha na tabela do cap. 09 ou se prefere mostrar só os totais.
7. Itens sem fonte (BDI, frete remoto, reajuste, ITBI e escritura) só como perguntas ao engenheiro e ao contador.
8. Estrutura pronta contada como unidade (Parte 3), não como mobiliário (Planilha 1).
9. Base da reserva = subtotal das Partes 1 a 6.
10. Duas medidas por unidade, com nome: «custo por unidade» (sem giro) e «investimento por unidade» (com giro, igual ao custo por chave do Pilar 6).
11. Transposição manual para a página 6, em vez de alterar a ficha do Pilar 6 (que mexe em ferramenta existente).
12. O selo não exige percentual mínimo de linhas cotadas nem estar dentro do limite.
13. Régua com Sonhador, Estimador e Calculista (Developer fora desta ficha).
14. Cinco aulas no módulo Pilar 6 do conteúdo `fa9a6c54`, desligadas, com os nomes «Aprofundamento 6A · CAPEX · …», depois do tutorial da ficha do Pilar 6 e antes da Planilha 1; renomear, reapontar e reposicionar as quatro já criadas (mexe em existente).
15. Identidade visual da Trilha 1 (Playfair + Inter e paleta) nas peças desta lição, com a exceção registrada no `CLAUDE.md`.
16. Voz sintética no tutorial (sem licença registrada) ou gravação por Bruno.
17. Ficha sem envio de dados (diferente do `FEEDBACK_URL` do Pilar 6) e aula pedindo só o nome, sem e-mail.
18. Giro igual a zero aceito para quem já opera ou faz para outra pessoa, com justificativa.
19. Ficha com 30 a 45 min na primeira passada.
20. Renomear pastas e arquivos para `pilar6a`, `Pilar-6A-…` e `p6a-c-…` antes de ligar as aulas.
21. Como o curso trata o teste de estresse «CAPEX +20%» da Marina (990.144,58, acima do limite), que a 6A não calcula.
22. Registrar, fora desta lição: o Pilar 7 mostra a Marina com cerca de R$ 690 mil (antes das cotações); uma caixa futura no Pilar 7 poderia citar a 6A (mexe em existente). A capa sem a linha «Para Airbnb, casas, apartamentos, pousadas e glampings» (O6).

# Relatório · Aula 5 · Viabilidade e capital (Etapa 3, fecha a etapa)

26/10/2026 · Rascunho para aprovação do Bruno. Nada publicado. Nenhum arquivo fora de `aula5/` alterado.

## Arquivos
- `aula5/ebook-aula5-viabilidade-capital.txt` (code `zion-t1-a5`, bignum 05)
- `aula5/aula5-gravada.txt` (45 slides, 7 blocos, `@escala = grande`)
- Conferência: `gen_ebook.py` e `gen_deck.py` rodam sem erro; os 45 slides renderizados com `preview.py` + `pshot.js`, nenhum estouro de 1920 × 1080.

## E-book: 9 capítulos + ✓
| Cap. | Título | Palavras |
|---|---|---|
| 00 | Antes de começar (mapa, `@big`, "O que você leva", caminho, dúvidas, duas situações, como ler) | 741 |
| 01 | Onde você está: "E em quanto tempo isso volta?" | 552 |
| 02 | Parte 1 · O resultado não é retorno | 708 |
| 03 | O primeiro ano tem rampa | 792 |
| 04 | O dinheiro atravessa? (capital de giro) | 915 |
| 05 | Quando volta, e o pior cenário | 1.063 |
| 06 | Parte 2 · O número exato (três perguntas do capital, régua do quanto captar) | 975 |
| 07 | A due diligence começa por você | 508 |
| 08 | Existem mil maneiras de fazer acontecer (sozinho, banco, garantia, parceiro, pool da família, outras portas, o que cada real cobra) | 1.209 |
| 09 | O seu Dossiê 3 (ferramenta `etapa-3`, nota, duas metades, veredito, critério para parar, reunião, Land Bank Zion, compromisso de 7 dias, próxima aula) | 1.115 |
| ✓ | Autoavaliação (7 quizzes) e glossário | 503 |

Total: **9.364 palavras no arquivo (`wc`)**, **9.988 pela contagem do `gen_ebook.py`** (a Aula 1 dá 9.816 no mesmo gerador). 41 campos, 15 quizzes.

## Apresentação: 7 blocos, 45 slides, 3.741 palavras de fala
| Bloco | Slides | Fala | Minutos (135 ppm) |
|---|---|---|---|
| 1 · Abertura (capa, tres, jornada `aqui: 6`, espelho, troca) | 5 | 396 | 2,9 |
| 2 · O resultado não é retorno | 5 | 373 | 2,8 |
| 3 · O caminho e o fôlego | 7 | 555 | 4,1 |
| 4 · Quando volta e o pior cenário | 7 | 569 | 4,2 |
| 5 · O número exato | 6 | 512 | 3,8 |
| 6 · De onde vem o dinheiro | 8 | 706 | 5,2 |
| 7 · O seu Dossiê 3 (`faca` com `[domínio do app]/*etapa-3*`, `proxima` com `aqui: 7`) | 7 | 630 | 4,7 |

Três quizzes `PAUSA` (`pior`, `redondo`, `jurozero`) e mais o `faca`. Fotos: 12 IDs; só `e7db84e4…` aparece duas vezes (opener do Bloco 5 e `garantia`).

## Contas conferidas (Python com Decimal, e pela outra ordem)
Todas ilustrativas, a partir dos números da Marina das fontes antigas (Aulas 7 e 8, que viram a nova Aula 4) e da Aula 1:
- Cada noite deixa 645 × 0,82 − 120 = 408,90. Noites no ano normal: 3 × 90 × 64% + 4 × 90 × 40% + 5 × 90 × 22% = 415,8. Receita 268.191. Sobra 415,8 × 408,90 − 156.000 = 14.020,62. Equilíbrio 156.000 ÷ 408,90 ÷ 1.080 = 35,3%.
- Retorno simples: 14.020,62 ÷ 963.240 = 1,46%; ÷ 1.531.800 = 0,92%; com terreno 0,90% e 0,66%; antes da reserva 2,83%.
- Ano 1 (junho, rampa de 40/50/75): 232,47 noites; −60.943,02, mês a mês e por 232,47 × 408,90 − 156.000. Receita 149.943,15 (44,1% abaixo). Desconto de 15%: −66.426,66. Rampa no piso: −79.932,33.
- Giro: 60.943,02 + 24.518,90 + 39.000 = 124.461,92 → 124.500; Etapa 01 = 78.000. Menor saldo 63.556,98 (4,9 meses). Reserva do vale 8.172,97 por mês de alta; ficam 2.379,67.
- Colchão 6,6% e 4,1%; reforço 32.767,02 e 89.623,02; giro com colchão 157.267,02 e 214.123,02.
- Payback 1 + 1.024.183,02 ÷ 14.020,62 = 74,05 anos; teto 114,60.
- Cenários: conservador 580,50 × 0,82 − 120 = 356,01; 332,64 noites; −37.576,83 por ano; ano 1 −89.790,68; saldo 34.709,32; abril do ano 2 −120,61 (mês a mês). Otimista +64.814,12; ano 1 −32.544,83; payback 16,4 e 25,1; saldo 91.955,17.
- Dor: diária −10% = 21.991,66; ocupação −10% = 17.002,06; R$ 50 = 17.047,80. Escada: R$ 716 → 38.228,50, payback 27,4, conservador −20.147,16; empate do conservador em R$ 798,07.
- Régua: 963.240 + 124.500 + 32.767,02 = 1.120.507,02; 1.531.800 + 124.500 + 89.623,02 = 1.745.923,02. Participação com só o terreno: 65,1% e 74,4%. Fluxo por mês 1.168,39.
- Pool de R$ 50 mil (exemplo do Bruno): 1.120.507,02 ÷ 50.000 = 22,4 → 23 pessoas; teto 34,9 → 35. Conta derivada, não dado novo.

## O que entrou e o que saiu das fontes antigas
- Entrou da seção 10 das notas do Bruno: viabilidade a partir da rentabilidade; capital com número exato (quanto precisa, quanto retorna, quando retorna); due diligence de documentação (capítulo 7 novo, montado com os documentos da Aula 1 e as regras da Régua e das "seis coisas"); fazer sozinho (limite de perda); banco pede business plan, viabilidade, produto e garantia; "a garantia é o meu terreno"; parceiro, amigo, círculo; pool da família com R$ 50 mil cada; "mil maneiras"; "o foco sempre está na construção...".
- Do ebook-09: retorno simples, valorização, custo de oportunidade, rampa, mês de abertura, ano 1, giro pelas duas regras, reserva do vale, fôlego, colchão, payback e régua, três cenários, conservador no caixa, hierarquia da dor, "o que precisa ser verdade", veredito e frase da decisão.
- Do ebook-10: crença "o que falta é dinheiro", três perguntas do capital, Régua do Quanto Captar, contratado não esperado, frase do pedido e marcos, mapa das fontes, garantia real e aval, círculo com contrato, custo real do capital (em uma frase), as quatro coisas do sócio, o que você aceita ceder, piso e melhor alternativa.
- Saiu (Pareto, para caber em 10 mil palavras e 7 minutos por bloco): Modelo Zion de Viabilidade em oito abas, tribunal dos números, VPL e TIR, Conta do Custo Invisível da espera, a régua do Volume 05 para payback (ficou só a da Etapa 02), teste de queda da ocupação, as três perguntas brutais (viraram uma frase), Zion Score de Investimento com as cinco dimensões e faixas (a nota agora é a da ferramenta da Etapa 3, com a regra "nenhuma nota passa por cima do conservador"), Faixa de Negociação completa, roteiro das três mesas, quatro camadas, finalidades do Manual, governança, SPE e SCP, Score de Captação, figuras SVG e todas as caixas `[HISTÓRIA DO BRUNO]`.
- Lançamento e pré-venda: só referência à Trilha 2 (venda de unidades como fonte "fora" para primeira operação; estruturar a venda é Trilha 2).
- Numeração corrigida: Aulas 2/3 antigas → Aula 1; Aula 4 antiga (produto) → Aula 2; Aula 6 → Aula 3; Aulas 7 e 8 → Aula 4; Aula 12 → Aula 6. Sem "quatro etapas" nem "lançar". "Projeto" só para projetos de arquitetura e engenharia; citações das fontes com "projeto" foram reescritas como paráfrase ("a partir do Volume 05", "a partir do Panorama").

## Pendente de confirmação com o Bruno
1. **Caso Zion (slide `sozinho`, só na fala):** "em Urubici nós tínhamos o dinheiro, mesmo assim tivemos muitos contratempos". Vem da segunda revisão das notas (não da seção 10). Marcado na nota do slide.
2. Frases na voz do Bruno vindas das cartas dos e-books antigos: "vi empreendimento bonito que nunca devolveu o capital..." (slide `bruno`) e "empreendimento modesto e bem documentado conseguiu condição melhor..." (slide `dinheiro`). Confirmar que ele assina.
3. A ferramenta da Etapa 3 (`[domínio do app]/*etapa-3*`): tempo estimado de 15 minutos e o que ela pergunta foram escritos por analogia com a Aula 1. Confirmar com o app.
4. "Plano de vida" no lugar de "projeto de vida" (régua do payback e veredito), para respeitar a regra do "projeto".

## Divergências e dependências
- **Depende da Aula 4 nova.** Todos os números de CAPEX e receita (963.240 a 1.531.800; 408,90; 13.000; 14.020,62; −24.518,90; 35,3%) vêm das Aulas 7 e 8 antigas. Se a Aula 4 nova mudar qualquer um, a Aula 5 inteira precisa ser recalculada.
- **R$ 716** ("hipótese do produto") vem da Aula 4 antiga (produto), agora Aula 2. Se a nova Aula 2 não trouxer esse número, tirar a linha da escada da diária (e-book, capítulo 5; slide `verdade`).
- **27% do terreno (Aula 1):** não recalculado. Com os números da fase um, o terreno pesaria 26,6% do investimento total no teto (600 ÷ (1.531,8 + 600 + 124,5)) e 35,5% no piso. Os 27% batem com o teto; o piso não. Fica para decidir com o Bruno se a Aula 1 explica de onde vem o total.
- O quiz `redondo` (R$ 1.043.163) é o exemplo do próprio e-book de captação da escola, apresentado como "um empreendimento", não como a Marina.

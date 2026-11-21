# Auditoria do ZIP "Zion_Produto01_v2" (21/11/2026)

Arquivos lidos por inteiro: `01_ebook.pdf` (60 p.), `02_gamma.md` (60 telas), `03_microaulas.md` (20 roteiros), `04_ferramentas.html`, `05_comercial.md`, `06_implementacao.md`, `07_jornada.md`, `08_landing.md`. Originais preservados (o ZIP não foi alterado; tudo novo está em `producao/produto-01-terra-capital/`).

## O que foi mantido
Promessa "Aprenda o passo a passo…", sete pilares, 20 microaulas, ECROI, OP3D (20% · 4% · 0,8% como heurística), dez temas, exemplos numéricos (todos conferidos nos testes: R$ 220 mil + R$ 30 mil − R$ 50 mil = lacuna de R$ 200 mil; 0,8x de cobertura; R$ 6 mil de receita; 9 noites de equilíbrio; 60/40 de sociedade), economia R$ 47 × R$ 67.

## Problemas encontrados e o que foi feito
| # | Achado | Tratamento |
|---|---|---|
| 1 | **Paleta do prompt (#304332, #F5F1E7, #B6A477, #19221A) difere da oficial do repositório** (`CLAUDE.md`: #1B2117, #FEF5F0, #DED6BF, #C9B37E, #040605). | Usei a **oficial do repositório** + logo oficial em todas as peças. Troca em um bloco `:root` se Bruno preferir a do prompt. **Decisão pendente de Bruno.** |
| 2 | As 20 microaulas do ZIP têm 25 a 50 s de fala (≈ 11 min no total), não 60 a 120 s. | Mantive o texto (é o aprovado). Os 70 a 100 min vêm das tarefas e ferramentas. Roteiros em `aulas/ROTEIROS.md` com estimativa por aula. Se Bruno quiser aulas de ~2 min, é preciso aprofundar o roteiro. |
| 3 | A jornada de 7 pilares (07) não coincide exatamente com os temas das aulas (a aula 4 mistura infraestrutura e mercado; a 5, diária, experiência e modelo). | Mantive o mapeamento do ZIP (aulas 1–2, 3–4, 5, 6, 7–9, 10–16, 17–20) e distribuí os 55 temas do guia pelos pilares pelo conteúdo. |
| 4 | E-book do ZIP: 60 "páginas" de cerca de 35 palavras (formato slide). | Reescrito como guia editorial de 60 páginas: por que importa, exemplo (dados fictícios), como fazer, erro comum, atividade e anotações (+2.850 palavras, sem números de mercado). Capa, sumário, fechamento, checklist, roteiro de reunião, referências e comparação de caminhos. |
| 5 | Ferramenta do ZIP: uma página só, sem salvar, sem SAC, sem cenário adverso, sem evidência no checklist; cobertura mostrava valor negativo sem aviso; custos misturados. | Reconstruída: 10 ferramentas, lógica separada e testada (23 testes de lógica contra contas independentes), PDF do dossiê, backup. |
| 6 | Atividade do ZIP pede "anotar número da matrícula". | Troquei por "certidão de dd/mm, arquivo X": não coletar dado pessoal desnecessário. |
| 7 | "Avaliações de concorrentes podem indicar demanda por privacidade" (aula 14) é uma hipótese solta. | Mantida como "podem indicar" (aprovada pelo ZIP). **Bruno: manter ou cortar.** |
| 8 | ZIP cita "Clube Zion R$ 970" e "encontro VIP" no pós-compra. | **Não incluí**: o prompt proíbe oferta complementar de produto não finalizado. Sequência pós-compra (dias 0/2/5/10) depende de automação e exige "aprovado" de Bruno: não criada. |
| 9 | ZIP pede foto real no topo da landing; `CLAUDE.md` (decisão de 06/11) proíbe foto de hospedagem no topo. | Topo com telas reais da ferramenta; foto real (Zion Bubble Glamping, com legenda) só na seção de autoridade. |
| 10 | Criativo 2 do ZIP usa documento de matrícula fictício. | Não produzi criativos nem campanhas (R$ 0, pedido do prompt). Copies em `OFERTA.md`. |
| 11 | Economia do ZIP: números conferem (testados), mas a provisão de 15% é "ilustrativa" e o CPA depende de conversão desconhecida. | Mantido como premissa rotulada; tabela com conversão lead→compra necessária. CPL ≠ CPA. |
| 12 | **Sobreposição com produtos que já existem no ClickMax** (ver abaixo). | Não mexi neles. **Decisão pendente de Bruno.** |

## Sobreposição (só leitura)
No projeto Infoprodutos Zion já existem, entre outros: "Tenho Terra, mas Não Tenho Dinheiro. E Agora?" (mini mentoria, incompleto), "Como Atrair Investimentos para Minha Terra que Está Parada?" (incompleto), "Terreno Parado, Projeto com Sócio — E-book + Kit" (aprovado), "Do Terreno ao Airbnb" (aprovado), "Transforme seu terreno em um destino turístico · Curso passo a passo" (aprovado). O Produto 01 trata do mesmo público; convém decidir se substitui, complementa ou concorre. Também há o nome "01" em Arsenal 01 e Academy 01.

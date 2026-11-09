# Decisões aprovadas O8 a O14

Comando 05G-A · 09/11/2026 · Responsável: Bruno Chaerk · **Sete decisões metodológicas aprovadas. Implementação não autorizada.**

- **Fonte:** texto do Comando 05G-A, seção 4, enviado pelo Bruno em 09/11/2026. As decisões estão transcritas abaixo sem alteração de sentido.
- **Origem das observações:** `docs/academy/comando-05f/RESSALVAS_E_CLASSIFICACAO_05F.md`, seção 2. Commit `2255189`, conferido na main; hashes dos documentos do 05F conferidos com `HASHES_05F.txt` (8 de 8).

## Registro

| Decisão | Observação do 05F (o que foi achado) | Diretriz aprovada (resumo fiel) | Situação |
|---|---|---|---|
| **O8 · Avaliação preliminar do P6** | A margem e a régua do P6 são calculadas antes de aluguel, gestão e royalties. O selo do P6 dizia "Avançar" enquanto a viabilidade dizia "Redesenhar" (C3E) | O P6 pode mostrar indicadores e uma avaliação preliminar, mas: sem selo de aprovação definitiva; sem antecipar conclusão de viabilidade; subordinado à análise financeira completa; o usuário distingue indicação inicial de diagnóstico consolidado; contradições entre etapas tratadas de forma explícita | Aprovada. Não implementada |
| **O9 · Valor de saída com EBITDA negativo** | 6 × EBITDA negativo gerava um valor de venda negativo, somado ao ano 10 (C1: −R$ 92.517,75) | **Valor de saída por múltiplo = MAX(0, EBITDA × múltiplo).** Vale para o valor estimado por múltiplos, não para o valor econômico total. Dívidas, obrigações e custos de encerramento ficam separados, quando aplicáveis. Nunca apresentar valor negativo mecânico como preço de venda | Aprovada. Não implementada |
| **O10 · Horizonte do fluxo de caixa** | A curva de 36 meses escondia a queima de caixa depois do mês 36, e o atraso podia "melhorar" o caixa | Horizonte total de **10 anos**: mensal nos primeiros 36 meses e anual do 4º ao 10º ano; alertas de caixa negativo; identificação de capital adicional; análise explícita do atraso. Indicadores coerentes com o horizonte. Um atraso nunca pode parecer melhorar o projeto sem explicar o efeito em receitas, despesas, investimento, financiamento e valor presente | Aprovada. Não implementada |
| **O11 · Bases de gestão e royalties** | A ZAIOS aplica gestão e royalties sobre a receita bruta; o comando usou a hospedagem (C2: R$ 19.800/ano; C3: R$ 62.400/ano) | Bases **configuráveis e independentes** para gestão e para royalties/licenciamento: receita de hospedagem ou receita bruta total, conforme o contrato. Sem base contratual, a premissa aparece como **hipótese**. Bases e percentuais explícitos nos relatórios. Sem dupla incidência nem base equivocada | Aprovada. Não implementada |
| **O12 · Base do capital de giro** | O giro A (6 × fixo) não incluía o aluguel | A necessidade de giro considera custos fixos recorrentes, **aluguel, quando aplicável**, e outras obrigações fixas recorrentes, sem duplicidade. Distinguir despesas fixas, variáveis, investimentos, reservas específicas e capital de giro. **Não aprova seis meses como prazo universal.** A metodologia deve ser compatível com o fluxo de caixa e com a necessidade real de financiamento | Aprovada. Não implementada |
| **O13 · Giro necessário x disponível** | A ZAIOS não aceitava capital de giro informado | **A. Necessário:** calculado pela plataforma. **B. Disponível:** informado pelo empreendedor. **C. Diferença = disponível − necessário:** negativa = déficit, positiva = excedente. O déficit entra no diagnóstico e na necessidade de captação. O disponível não substitui silenciosamente o necessário. Sem dupla contagem no investimento, nas fontes ou no fluxo | Aprovada. Não implementada |
| **O14 · Receitas complementares** | As "outras receitas" eram só % das diárias e acompanhavam ocupação, rampa e cenários | Categorias com fórmulas e premissas próprias: **A** vinculadas à ocupação (café da manhã, serviços por hóspede, experiências das reservas); **B** vinculadas ao consumo (restaurante, massagens, produtos, consumo adicional); **C** independentes da ocupação (eventos, day use, atividades externas, outras fontes). Sem presumir que tudo acompanha a ocupação. Integração com receita bruta, tributos, custos, EBITDA, fluxo e indicadores. Sem duplicidade com a hospedagem | Aprovada. Não implementada |

## O que estas decisões não fazem

- **Não encerram** nenhuma pendência anterior: O6, O7, B08, A09, B06, H4, D5 a D14, integridade, segunda transcrição, pró-labore, reservas, quebra, contingência e conferência externa. Ver `PENDENCIAS_METODOLOGICAS.md`.
- **Não aprovam** os parâmetros de teste usados nos cenários (taxa de 10%, múltiplo de 6×, prazos de giro, percentuais das categorias de receita). Esses continuam H4 ou hipóteses de teste.
- **Não autorizam** nenhuma alteração na ZAIOS. A implementação depende de autorização expressa (ver `PLANO_IMPLEMENTACAO_FUTURA.md`).

## Itens que as decisões deixam em aberto (precisam de definição antes ou durante a implementação)

| Decisão | Ponto em aberto | Por quê |
|---|---|---|
| O8 | Nome e forma da indicação preliminar (texto, faixa, ícone) e se o P6 mantém a régua de margem | A decisão proíbe selo de aprovação, mas não define o rótulo substituto |
| O10 | Convenção de desconto com fluxo mensal (36 meses) + anual (anos 4 a 10); tratamento do atraso no VPL (deslocamento de meses ou de anos) | Hoje o VPL é anual, com desconto no fim do ano |
| O12 | Prazo ou método do componente "meses de custos fixos" (hoje 6 no giro A e 3 no giro B) | A decisão diz explicitamente que 6 meses não estão aprovados como regra universal |
| O13 | Onde o disponível entra nas fontes (capital próprio x giro) e como aparece na curva | Para evitar dupla contagem, é preciso uma convenção única de fontes e usos |
| O14 | Lista de categorias por tipo de hospedagem, fatores de cada uma, custo associado padrão, alíquota por fonte (D14) e efeito da rampa sobre as categorias B e C | A decisão exige fórmulas próprias, mas não fixa os fatores |

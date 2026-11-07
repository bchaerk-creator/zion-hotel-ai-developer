# ZAIOS · Registro de decisões

| Data | Decisão | Quem decidiu |
|---|---|---|
| 05/11/2026 | O MVP atende as jornadas Desenvolvimento e Operação desde o lançamento | Bruno Chaerk |
| 05/11/2026 | A base do projeto é o prompt mestre, o Super Prompt das 4 trilhas e o adendo v2. O PDF "Zion AI Operating System" fica fora do escopo | Bruno Chaerk |
| 05/11/2026 | O MVP sai sem IA generativa: as fichas funcionam como exercícios guiados, com cálculos determinísticos e veredito por regras. A IA entra na fase seguinte, começando por P5 (CAPEX) e P6 (Viabilidade) | Bruno Chaerk |
| 06/11/2026 | Seguir para a Etapa 2 com as fórmulas como "Versão 0, a validar pela Zion" | Bruno Chaerk |
| 06/11/2026 | Iniciar a Etapa 3 por P1, P2 e P3, que não dependem das planilhas | Bruno Chaerk |
| 06/11/2026 | Fazer o Dossiê preliminar antes da Jornada Operação | Bruno Chaerk |
| 07/11/2026 | Construir P5 e P6 com a metodologia dos planos F01 a F03 como versão 0 | Bruno Chaerk ("pode começar") |

## Decisões pendentes
- Fonte oficial das fórmulas financeiras (planilhas e simuladores Zion de referência).
- Definição de "receita de hospedagem": inclui ou não a taxa de limpeza; antes ou depois dos impostos. Hoje a taxa de limpeza está fora.
- P5 e P6 foram construídos sobre a metodologia dos planos F01, F02 e F03 (ainda marcados para revisão do Bruno). Validar as faixas e regras de referência quando os planos forem aprovados.

## Andamento
| Data | Etapa | Resultado | Créditos |
|---|---|---|---|
| 05/11/2026 | Etapa 1 · Fundação | Login por link, lista de associados, cadastro, Pasta, admin. 8 testes passaram. Projeto Lovable "Zion Empreendimentos" (id 51fa7ea5-6cb2-4867-9bf7-6e1cbb3e71dc), não publicado | 12 |
| 06/11/2026 | Etapa 2 · Motor | Ajustes da Etapa 1, motor de cálculo (versão 0), motor de exercícios, exercício-modelo "Potencial de faturamento", base de custos | 13,4 |
| 06/11/2026 | Etapa 2 · Correções | Revisão do código encontrou 4 defeitos (leitura de reais com ponto, campos sem limite, concluído voltando a rascunho, recálculo com valor antigo). Corrigidos. 74 testes passaram e o fluxo foi conferido em 390px | 3,9 |
| 06/11/2026 | Etapa 3 · Parte 1 | Motor com blocos, escolha múltipla, listas, veredito e aba Pendências. P1 Território com semáforo por tema. 139 testes | 8,7 |
| 06/11/2026 | Etapa 3 · Parte 2 | Ajustes no P1 (servidão e faixa de rodovia em amarelo; frase por tema). P2 Mercado e P3 Produto. Faixa dos concorrentes no exercício de faturamento. 198 testes | 7,2 |
| 06/11/2026 | Etapa 3 · Parte 3 | Dossiê preliminar: aba Dossiê, 12 seções, selo de qualidade, versões imutáveis no banco, PDF A4 com texto selecionável. CAPEX e viabilidade como "Em breve" | 8,9 |
| 06/11/2026 | Etapa 4 · Parte 1 | Jornada Operação: V1 Raio-X da casa (nota por critério, 5 correções) e V2 Posicionamento. Dossiê de Operação. 227 testes | 9,3 |
| 06/11/2026 | Etapa 4 · Parte 2 | G1 Maturidade da gestão e Plano de Melhoria (sincronizado com as pendências). 260 testes | 13,3 |
| 06/11/2026 | Etapa 4 · Parte 3 | INCOMPLETA. G2 Finanças e G3 Indicadores construídos, mas com erro de build: a prévia não abre. Testes desta parte não escritos. Parou porque o workspace ficou sem créditos | 8,8 |
| 07/11/2026 | Etapa 4 · Parte 3 (continuação) | Testes de G2 e G3 escritos (50 de cálculo e dossiê, 18 de segurança, todos passando) e FORMULAS.md atualizado. Ainda resta 1 erro de compilação na tela de Finanças (campo opcional id). Parou de novo por falta de créditos | 5,0 |
| 07/11/2026 | Etapa 4 · Parte 3 (fechamento) | Erro de compilação corrigido, prévia abrindo. 315 testes passando (inclui segurança). Finanças e Indicadores conferidos em 390px. PDF do Dossiê de Operação baixado e conferido (seções 8, 9, 10 e Plano) | 3,4 |
| 07/11/2026 | Etapa 5 · P5 CAPEX | Sete linhas com evidência, contingência por perfil, giro mínimo, necessidade total, cronograma de desembolso, faixas de referência Zion (F01). Caso de referência F01 conferido (CAPEX 1.237.400). 332 testes | 12,3 |
| 07/11/2026 | Etapa 5 · P6 Receitas | Cascata F02 (receita bruta até geração de caixa), retirada do dono, régua de margem, ponto de equilíbrio, primeiro ano com rampa, capital de giro pelas duas regras. Caso conferido à mão. 352 testes | 10,6 |
| 07/11/2026 | Etapa 5 · P6 Viabilidade | Fluxo de 10 anos, paybacks, VPL e TIR com e sem saída, três cenários, sensibilidade, estresse, curva de caixa de 36 meses, regra de decisão Zion em 5 passos (selo Redesenhar). Casos do F03 conferidos. Dossiê seção 10. 361 testes | 18,4 |
| | **Total até aqui** | | **135,2** |

## Ainda não verificado
- Entrada real pelo link no e-mail (teste do Bruno).

## Ao publicar
- Incluir o endereço publicado na lista fixa de origens do link de acesso.

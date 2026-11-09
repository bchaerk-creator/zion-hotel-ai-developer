# Plano de implementação futura · O8 a O14

Comando 05G-A · 09/11/2026 · **Proposta. Nada foi implementado.** Cada etapa só começa com autorização expressa do Bruno.

## 1. Pré-requisitos (antes de qualquer alteração)

| # | Pré-requisito | Por quê | Responsável |
|---|---|---|---|
| PR-1 | Responder às perguntas P-O8, P-O10a/b/c, P-O11, P-O12, P-O13 e P-O14a/b/c/d (`PENDENCIAS_METODOLOGICAS.md`) | Sem elas, a implementação inventaria premissas | Bruno |
| PR-2 | Decidir o canal de implementação: (a) mensagens ao agente do Lovable, que **consomem créditos**; ou (b) conectar a ZAIOS a um repositório GitHub privado e editar o código por lá. A opção (b) também resolve a integridade (hash na origem) | A escolha muda custo, controle de versão e prova de integridade | Bruno |
| PR-3 | Fechar a integridade, ou registrar formalmente que a implementação parte de um código não conferido por hash | As linhas e fórmulas deste plano são do commit `ec21ad5` | Bruno |
| PR-4 | Conferir que o projeto continua no commit `ec21ad5` no início da implementação. Se mudou, refazer a matriz de impacto | Edições paralelas invalidam o mapa | Executor |
| PR-5 | Congelar a versão das suítes (05E, 05F, aceite 05G) usada como referência | Para medir as mudanças previstas | Executor |

## 2. Sequência proposta

Ordem pensada para reduzir risco: primeiro as mudanças pequenas e isoladas, depois as que mexem no modelo de receitas, por último o horizonte, que depende do giro.

| Etapa | Decisões | O que muda | Risco | Depende de | Créditos / custo |
|---|---|---|---|---|---|
| 1 | **O9** | `valorSaida` com MAX(0); nota na tela e no dossiê | Baixo | PR-2 | Baixo |
| 2 | **O8** (junto com D11-A: veredito só após homologação) | Indicação preliminar no P6, fim do selo de aprovação, aviso de conflito, margem antes e depois dos custos do modelo | Médio (tipo `Veredito` compartilhado) | P-O8, D11-A | Baixo a médio |
| 3 | **O11** | Bases independentes de gestão e royalties; linhas separadas no demonstrativo; padrão = receita bruta (preserva o atual) | Médio | P-O11, O6 | Médio |
| 4 | **O14** | Categorias A, B e C; custos associados; migração do `outras_pct` | Alto | P-O14a–d, D9, D10, D14, etapa 3 | Médio a alto |
| 5 | **O12** | Base do giro com aluguel e obrigações fixas; prazo ou método parametrizado; um único conceito de giro (P5, P6, dossiê) | Médio a alto | P-O12, D12 | Médio |
| 6 | **O13** | Giro disponível, diferença, déficit e excedente; fontes e usos | Médio | Etapa 5, P-O13 | Baixo a médio |
| 7 | **O10** | Curva de 120 meses (36 mensais + anos 4 a 10), alertas, capital adicional, atraso com decomposição, indicadores no mesmo horizonte | Alto | Etapas 5 e 6, P-O10a/b/c, D8, D6 | Médio a alto |
| 8 | Consolidação | Dossiê e PDF com todas as mudanças; textos de ajuda; regressão completa | Médio | Etapas 1 a 7 | Baixo |

**Em cada etapa:**
1. rodar a linha de base (os testes da decisão devem falhar);
2. implementar só aquela decisão;
3. rodar os testes de aceite (devem passar);
4. rodar a regressão (`PLANO_TESTES_REGRESSAO.md`, seção 4) e comparar com a lista de mudanças previstas;
5. registrar a evidência numa pasta nova;
6. aguardar a aprovação do Bruno.

## 3. Alterações técnicas propostas (resumo)

| Decisão | Cálculo | Interface | Dados | Relatórios |
|---|---|---|---|---|
| O8 | Margem EBITDA; estado "indicação preliminar"; detecção de conflito P6 x viabilidade | Fim do selo de aprovação no P6; aviso de conflito; texto de subordinação | Novo estado no tipo do veredito (ou campo separado). Respostas antigas mantêm o selo gravado até o recálculo | Dossiê: margem, régua e resumo |
| O9 | `max(0, múltiplo × EBITDA)` + sinal de "saída zerada" | Nota abaixo do valor de saída | — | Dossiê: frase da saída |
| O10 | Curva de 120 meses; agregação anual; menor saldo e capital adicional; atraso no mesmo horizonte | Gráfico e tabela em duas escalas; alertas por período negativo; quadro do atraso | Estudo salvo maior (JSON) | Dossiê: curva, alertas e atraso |
| O11 | Gestão e royalties, cada um na sua base, também no equilíbrio | 2 seletores de base + marca de hipótese; linhas separadas | 2 a 4 valores novos nas respostas | Dossiê: bases e percentuais |
| O12 | Base mensal = fixos + aluguel + obrigações fixas listadas; prazo ou método parametrizado; definição única | Composição da base exibida; alerta de duplicidade | Valores novos nas respostas (obrigações, prazo) | Dossiê: um só giro (P5 e P6 coerentes) |
| O13 | Necessário, disponível, diferença, déficit e excedente; fontes e usos | Campo do giro disponível; quadro do déficit ou excedente | 1 valor novo nas respostas | Dossiê: diagnóstico e captação |
| O14 | Categorias A, B e C com fatores, custos e alíquota; rampa e cenários por categoria | Lista de receitas complementares | Estrutura de lista nas respostas; conversão do `outras_pct` | Dossiê: receitas por categoria |

## 4. O que fica fora deste plano

- B08, A09, B06, F05 e Folha J2. As decisões O8 a O14 foram aprovadas para a ZAIOS. Aplicar a mesma lógica às ferramentas do Arsenal e à Folha exige decisão própria (ver O6).
- G2/G3 (gestão mensal real).
- Pendências D5 a D14, salvo onde o plano cita dependência.
- Homologação matemática ou econômica.

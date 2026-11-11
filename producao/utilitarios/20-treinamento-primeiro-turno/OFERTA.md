# Ferramenta 20 · Kit de Treinamento do Primeiro Turno

Status: arquivos prontos e testados; **oferta enviada para aprovação em 10/11/2026** (rodada diária automática). **Oferta aprovada e página publicada em 11/11/2026.**

**ClickMax:** produto `fcb2b52e-b4ec-4bfb-8cb9-516294255a38`; oferta `e1cda5e6-af69-4c0e-84cf-12245e07022a` (R$ 19, checkout `AzLhCjcBtK`, status `pending` desde 10/11 04h57 UTC, sem erro de sincronização); página `c3670c67-fe99-4ca1-8522-ef50d204577e` em `/treinamento-primeiro-turno` (rascunho). Entrega: 4 arquivos e página de acesso em `docs/p/adbc67069af26ae0/treinamento-20/`, ligados à oferta.

## 1. Tarefa concreta
Treinar a primeira pessoa da equipe (limpeza, manutenção ou recepção) do jeito da casa e saber quando ela pode fazer o turno sozinha.
- **Base Zion:** "Onboarding · Novos Colaboradores" (Bíblia Operacional, Notion): seis etapas (tour, cultura, vídeo da função, manual, primeira execução acompanhada, confirmação). A copy diz que **as seis etapas partem da trilha de onboarding usada nas unidades da Zion** (verdadeiro; autorização de 06/11).
- **Sobreposição verificada:** a Jornada 2 · Módulo 5 (Pessoas e alçadas) trata de quem faz o quê e até quanto decide; esta ferramenta trata só de como ensinar e liberar a primeira pessoa. O guia diz que alçadas são "outra conversa, à parte".

## 2. Promessa
"Aprenda o passo a passo para treinar a primeira pessoa da sua equipe: o que mostrar, o que fazer junto, quando ela pode trabalhar sozinha e quem conferiu cada tarefa."
Tempo para começar: cerca de 20 minutos para ajustar a lista. O desempenho da pessoa não depende só da planilha.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Treinamento-Primeiro-Turno-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Treinamento (60 linhas, 16 tarefas sugeridas em 6 etapas, data de hoje com HOJE()) e Painel |
| `Treinamento-Primeiro-Turno-Zion-EXEMPLO.xlsx` | Pessoa fictícia, início 02/11, hoje 05/11: 6 de 14 obrigatórias prontas, 4 atrasadas, 1 com datas fora de ordem, ainda não liberada |
| `Ficha-do-Primeiro-Turno.pdf` | Roteiro do primeiro dia (6 momentos), tarefas com os três passos e assinaturas |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: 4 passos, 3 exercícios, critérios, checklist, limitações |
| `Ferramenta20-Treinamento-Primeiro-Turno-Zion.zip` | Pacote completo |

Regras: prazo = início + dias; passo atual (Nenhum, Mostrado, Feito junto, Fez sozinha); situação: Datas fora de ordem (passo pulado ou data anterior à do passo anterior), Data futura, Falta quem conferiu, Pronta, Atrasada (não pronta e hoje depois do prazo), Feita junto, Mostrada, Não começou. Liberada para o turno sozinha = todas as obrigatórias prontas e nenhuma linha para conferir.

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **30 de 30**. Prazo, situação e passo de cada linha, os 10 resultados do Painel e as 6 linhas por etapa comparados com uma conta independente em Python: exemplo, versão em branco, 10 cenários aleatórios com erros, 5 cenários aleatórios limpos e 9 casos de borda (vazio, sem obrigatórias, tudo pronto, falta quem conferiu, passo pulado, data futura, prazo hoje não atrasa, prazo de ontem atrasa, sem início e sem hoje). Exemplo conferido à mão. Nenhuma célula com erro em 26 arquivos. Uma falha corrigida na primeira rodada: a contagem por etapa incluía linhas com etapa e sem tarefa.
Revisão visual do guia, da ficha, das telas, da capa e da página no celular.
**Não testado:** Excel e Google Sheets reais; celular de verdade.

## 5. Copy (ECROI)
- **Espelhamento:** "Ela já pode fazer o turno sozinha?"
- **Colapso de crença:** explicar uma vez não é treinar.
- **Reencadramento:** de "já mostrei" para "mostrei, fizemos junto, ela fez sozinha e eu conferi".
- **Inevitabilidade:** seis etapas + três passos + conferência = critério claro para liberar.
- **Resultado educacional:** você aprende a ensinar em ordem, registrar e decidir quando liberar.
Botão: "Quero o kit de treinamento" · R$ 19, pagamento único, reembolso em 7 dias. Vendido sozinho (Comando 05A).

## 6. Perguntas frequentes
Serve para qualquer função. · Não substitui contrato nem treinamentos exigidos por lei. · Não avalia a pessoa. · Um arquivo por pessoa. · Funciona no celular pelos apps.

## 7. Três anúncios (1080×1350, "Saiba mais", `utm_campaign=ferramenta20`)
1. **c20a · Turno sozinha:** "Ela já pode fazer o turno sozinha?" + tela do Painel. Primeira linha: "Um critério claro para liberar a pessoa nova."
2. **c20b · Três passos:** "Mostrar, fazer junto, fazer sozinha." + tela Tarefas. Primeira linha: "Explicar uma vez não é treinar."
3. **c20c · Ficha do primeiro dia:** ficha impressa. Primeira linha: "O roteiro do primeiro turno, a partir do onboarding das unidades da Zion."

## 8. Preço, custos e entrega
R$ 19. Custos por venda: taxa do checkout, impostos, reembolsos. Entrega: 4 arquivos + página de acesso. Manutenção baixa.

## 9. Execução
```
python3 -I src/build_planilha.py dist && python3 -I tests/test_planilha.py dist
python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist
bash src/empacotar.sh && python3 -I landing/build_landing.py
```

## Publicação (11/11/2026)
Oferta aprovada (`canSell` true, sem erro de sincronização). Página publicada e conferida no ar com Playwright: https://infoprodutos-zion.clickmax.space/treinamento-primeiro-turno (conteúdo correto; o checkout é um iframe bloqueado neste ambiente, então a compra não foi testada).

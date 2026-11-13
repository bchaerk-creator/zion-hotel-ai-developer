# Ferramenta 19 · Controle de Compras e Consumo Interno

Status: arquivos prontos e testados (rodada diária automática, 13/11/2026). Oferta e página: ver "ClickMax" e "Envio para aprovação".

**ClickMax:** produto `be520313-e490-4764-bccb-7cb60181d987`; oferta `6c4de218-736d-4cd0-a6b2-a0e84b49d159` (R$ 19, checkout `Ni8Incw1xB`); página `3182a2d0-36e2-4b72-b30c-60ca0a275f8b` em `/controle-compras` (rascunho). Entrega: 4 arquivos e página de acesso em `docs/p/adbc67069af26ae0/compras-19/`, ligados à oferta.

**Por que a 19 nesta rodada:** 01, 21 e E08 aguardam decisão de Bruno (PENDENCIAS_BRUNO.md); a 19 é a próxima da ordem do catálogo ("Depois: 19, E05, E06").
**Sobreposição verificada:** a Ferramenta 13 controla quantidades (saldo, mínimo, o que comprar); a 15 compara fornecedores antes de comprar; a 01 calcula a diária mínima. A 19 controla o dinheiro gasto em compras: categoria contra orçamento do mês, comprovante, custo de insumos por noite ocupada e visão do ano. O item 10 do catálogo (planilha financeira completa por imóvel) continua separado: a 19 não trata receitas, conciliação nem fechamento. Nenhuma alegação de que vem da rotina das unidades da Zion.

## 1. Tarefa concreta
Registrar cada compra da hospedagem (inclusive o consumo interno da equipe), comparar o gasto de cada categoria com o orçamento do mês e acompanhar o custo de insumos por noite ocupada.
- **Evidência:** item 19 do Catálogo. Nenhuma pesquisa de mercado e nenhum preço real: todos os valores do exemplo são fictícios.

## 2. Promessa
"Aprenda o passo a passo para registrar as compras da sua hospedagem, comparar cada categoria com o orçamento do mês e saber quanto os insumos custam por noite ocupada."
Tempo para começar: cerca de 10 minutos para ajustar as categorias. Gastar menos depende das decisões do comprador.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Controle-Compras-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Orçamento (8 categorias prontas, até 15), Compras (400 linhas), Mês e Ano |
| `Controle-Compras-Zion-EXEMPLO.xlsx` | Pousada fictícia, compras de outubro e novembro de 2026; novembro: R$ 2.741,70 de R$ 4.150,00, 68 noites, R$ 40,32 por noite; 2 categorias acima, 1 em atenção (enxoval em exatamente 90%); 2 compras com problema, 4 sem comprovante |
| `Folha-de-Compras.pdf` | Folha do mês para anotar compras no papel (1 página, paisagem) |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: 4 passos, 2 exercícios, critérios, checklist, limitações |
| `demonstracao/` | Telas de Compras e do Mês |
| `Ferramenta19-Controle-Compras-Zion.zip` | Pacote completo |

Regras: compra sem data → "Informe a data"; categoria fora da aba Orçamento → "Categoria não cadastrada"; valor zero, negativo ou texto → "Confira o valor"; sem "Sim" no comprovante → "Sem comprovante" (entra nas somas); demais → "OK". Mês: soma das compras válidas da categoria entre o 1º e o último dia do mês da data escolhida; diferença = orçamento − gasto; % = gasto ÷ orçamento; situação: Acima do orçamento (> orçamento), Atenção: 90% ou mais (≥ 90%), Dentro, Sem orçamento (gasto sem orçamento); custo por noite = gasto ÷ noites ocupadas (> 0). Ano: soma por categoria e mês no ano da data escolhida; orçamento do ano = 12 × mensal.

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **24 de 24**. Situação de cada compra, contagens, as 6 colunas da aba Mês por categoria, o total, as contagens do mês e os 12 meses da aba Ano por categoria comparados com uma regra independente em Python: exemplo, versão em branco, 8 cenários aleatórios com erros, 4 cenários aleatórios limpos (até 80 compras, até 10 categorias) e 6 casos de borda (limite de 90%, virada de mês, sem orçamento, orçamento zero, sem mês escolhido, 29 de fevereiro de 2028). Exemplo conferido à mão (2.741,70 ÷ 68 = 40,32). Nenhuma célula com erro em 20 arquivos. Uma falha na primeira rodada foi do próprio teste (endereço de célula errado), não da planilha.
Revisão visual do guia, da folha, das telas, da capa e da página no celular (390 px, sem rolagem lateral).
**Não testado:** Excel e Google Sheets reais; celular de verdade; compra no checkout.

## 5. Copy (ECROI)
- **Espelhamento:** "Para onde foi o dinheiro das compras?"
- **Colapso de crença:** "é só compra pequena" — somadas, viram a maior despesa variável que ninguém acompanha.
- **Reencadramento:** de gastar e ver no extrato para decidir um limite por categoria e acompanhar toda semana.
- **Inevitabilidade:** uma linha por compra + orçamento por categoria + custo por noite = você sabe onde ajustar.
- **Resultado educacional:** você aprende a categorizar, orçar, lançar e ler o mês e o ano.
Botão: "Quero o controle de compras" · R$ 19, pagamento único, reembolso em 7 dias. Vendido sozinho (Comando 05A); a página cita a Ferramenta 13 como produto separado.

## 6. Perguntas frequentes
Não substitui o contador. · Não controla estoque (Ferramenta 13). · Sem orçamento, use 1 ou 2 meses de gasto real como base. · Serve para mais de um imóvel (coluna Unidade). · Funciona no celular pelos apps.

## 7. Três anúncios (1080×1350, "Saiba mais", `utm_campaign=ferramenta19`)
1. **c19a · Dinheiro das compras:** "Para onde foi o dinheiro das compras?" + tela do Mês (dados fictícios). Primeira linha: "Cada categoria contra o orçamento do mês."
2. **c19b · Compra pequena:** "Compra pequena some." + tela de Compras. Primeira linha: "Detergente, café da equipe, lâmpada: tudo num lugar só."
3. **c19c · Por noite:** "Quanto custa cada noite vendida em insumos?" Primeira linha: "Compare meses cheios e vazios pelo custo por noite."

## 8. Preço, custos e entrega
R$ 19. Custos por venda: taxa do checkout, impostos, reembolsos. Entrega: 4 arquivos + página de acesso. Manutenção baixa.
Indicadores: visitas à página, conversão do checkout, reembolsos, custo por venda (quando houver anúncio aprovado).

## 9. Execução
```
python3 -I src/build_planilha.py dist && python3 -I tests/test_planilha.py dist
python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist
bash src/empacotar.sh && python3 -I landing/build_landing.py
```

## Envio para aprovação
13/11/2026 (rodada diária): 4 arquivos e página de acesso conferidos no ar (status 200) e ligados à oferta; `offers_get_incomplete_reason` vazio; oferta enviada para aprovação, status `pending`, sem erro de sincronização. Página segue em rascunho até a oferta ficar ativa.

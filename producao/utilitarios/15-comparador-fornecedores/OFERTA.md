# Ferramenta 15 · Comparador de Fornecedores

Status: arquivos prontos e testados (rodada diária automática, 12/11/2026). Oferta e página: ver "ClickMax" e "Envio para aprovação".

**ClickMax:** produto `ee019a14-1a5a-4ee7-9ef0-227dc9164185`; oferta `8b5e30b2-2b7d-49e6-bc55-b97d8ed1db96` (R$ 19, checkout `CDr4NA5HC6`); página `ac3388c6-0079-4aab-8798-56c39c45a526` em `/comparador-fornecedores` (rascunho). Entrega: 4 arquivos e página de acesso em `docs/p/adbc67069af26ae0/fornecedores-15/`, ligados à oferta.

**Por que a 15 nesta rodada:** a fila do catálogo seguia com 01, 21 e o e-book E08, que dependem de decisão de Bruno (sobreposições registradas em PENDENCIAS_BRUNO.md). A 15 é a próxima da ordem ("Depois: 18, 20, 15, 19") e preenche a lacuna de Compras da auditoria (`docs/zaios/AUDITORIA_ACADEMY_ZAIOS.md`: "Compras · Nenhum · Catálogo 15 (a fazer)").
**Sobreposição verificada:** a Ferramenta 05 compara 3 cotações de itens de obra uma única vez (orçamento da cabana). A 15 compara fornecedores recorrentes da operação (lavanderia, limpeza, papel, amenities, café, serviços), com custo por unidade comparável, frete, pedido mínimo, pesos e custo por mês. Nenhuma alegação de que vem da rotina das unidades da Zion.

## 1. Tarefa concreta
Comparar fornecedores do que a hospedagem compra ou contrata com frequência e escolher com critério: mesmo produto, mesma unidade, frete e pedido mínimo na conta, prazo, qualidade, atendimento, pagamento e confiabilidade com os pesos do comprador.
- **Evidência:** item 15 do Catálogo; lacuna de Compras na auditoria da Academy. Nenhuma pesquisa de mercado nova e nenhum preço real: todos os valores do exemplo são fictícios.

## 2. Promessa
"Aprenda o passo a passo para comparar fornecedores da sua hospedagem pelo custo real, pelo prazo e pelo que importa para você, e escolher com critério."
Tempo para começar: cerca de 15 minutos para ajustar os pesos e listar 3 necessidades. A economia real depende das cotações e da decisão do comprador.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Comparador-Fornecedores-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Critérios (6 critérios com peso 0–5), Necessidades (30), Cotações (150) e Resumo |
| `Comparador-Fornecedores-Zion-EXEMPLO.xlsx` | Pousada fictícia: 5 necessidades, 14 cotações (1 com nota inválida); 3 prontas para decidir; na lavanderia, melhor nota (R$ 10,90/kg) ≠ menor custo (R$ 9,50/kg), diferença de R$ 448,00 por mês com 320 kg |
| `Roteiro-de-Cotacao.pdf` | O que pedir a todos os fornecedores, mensagem modelo e tabela para anotar respostas e notas (1 página) |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: 4 passos, 3 exercícios, critérios, checklist, limitações |
| `demonstracao/` | Telas de Cotações (lavanderia) e Resumo |
| `Ferramenta15-Comparador-Fornecedores-Zion.zip` | Pacote completo |

Regras: custo comparável = (preço × pedido mínimo + frete) ÷ (quantidade × pedido mínimo), pedido mínimo vazio = 1, frete vazio = 0; nota de preço = 5 × menor custo da necessidade ÷ custo; nota de prazo = 5 × (menor prazo + 1) ÷ (prazo + 1); nota final = média ponderada só das notas preenchidas, 2 casas; melhor nota = maior nota final, empate pelo menor custo; situação da cotação: necessidade não cadastrada, falta o fornecedor, confira quantidade e preço, confira frete e pedido mínimo, confira o prazo, confira as notas (1 a 5), OK; resumo: sem cotações válidas, peça mais cotações (menos de 3), pronto para decidir; diferença por mês = (custo da melhor nota − menor custo) × consumo.

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **29 de 29**. Situação, custo comparável, notas de preço e de prazo, nota final, resultado, custo por mês e meses cobertos de cada cotação, e as 8 colunas do Resumo, comparados com uma regra independente em Python: exemplo, versão em branco, 8 cenários aleatórios com erros (cerca de metade das cotações com problema), 4 cenários aleatórios limpos (até 25 cotações, pesos variados) e 8 casos de borda (pesos zerados, só preço, empate total, empate de nota desempatado pelo custo, frete com pedido mínimo, nenhum prazo, uma cotação, necessidade sem cotação). Contas do exemplo conferidas à mão (9,65 por litro; R$ 448 por mês). Nenhuma célula com erro em 22 arquivos. Uma falha corrigida na primeira rodada: a contagem de necessidades cadastradas usava COUNTA − COUNTBLANK e dava −20.
Revisão visual do guia, do roteiro, das telas, da capa e da página no celular (390 px, sem rolagem lateral).
**Não testado:** Excel e Google Sheets reais (MAXIFS/MINIFS funcionam no LibreOffice; exigem Excel 2019 ou mais novo); celular de verdade; compra no checkout.

## 5. Copy (ECROI)
- **Espelhamento:** "O mais barato saiu mais caro?"
- **Colapso de crença:** preço de embalagem engana; frete, pedido mínimo e atraso não aparecem nele.
- **Reencadramento:** de "quem cobra menos" para "quem entrega o que eu preciso pelo menor custo real".
- **Inevitabilidade:** mesma especificação + mesma unidade + pesos claros = escolha que dá para explicar.
- **Resultado educacional:** você aprende a pedir cotações comparáveis, converter o custo, dar notas e decidir com o resumo.
Botão: "Quero o comparador" · R$ 19, pagamento único, reembolso em 7 dias. Vendido sozinho (Comando 05A).

## 6. Perguntas frequentes
Não indica fornecedores nem preços. · Serve para serviços (kg lavado, visita, mês). · Nota em branco não conta. · Não garante economia. · Funciona no celular pelos apps.

## 7. Três anúncios (1080×1350, "Saiba mais", `utm_campaign=ferramenta15`)
1. **c15a · Mais barato:** "O mais barato saiu mais caro?" + tela da lavanderia (dados fictícios). Primeira linha: "Compare pelo custo real, com frete e pedido mínimo."
2. **c15b · Embalagem:** "Frasco de 1 L ou galão de 5 L?" + tabela do detergente. Primeira linha: "Preço de embalagem engana."
3. **c15c · Resumo:** tela do Resumo. Primeira linha: "Melhor nota, menor custo e a diferença por mês, para cada compra."

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
12/11/2026 (rodada diária): 4 arquivos e página de acesso conferidos no ar (status 200) e ligados à oferta; `offers_get_incomplete_reason` vazio; oferta enviada para aprovação, status `pending`, sem erro de sincronização. Página segue em rascunho até a oferta ficar ativa.

## Publicação (13/11/2026)
Oferta aprovada (`status` approved, sem erro de sincronização). Página publicada; no primeiro acesso deu 404 (propagação) e, minutos depois, status 200 com título e reembolso: https://infoprodutos-zion.clickmax.space/comparador-fornecedores. O checkout é um iframe bloqueado neste ambiente, então a compra não foi testada.

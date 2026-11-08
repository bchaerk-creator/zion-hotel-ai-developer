# Ferramenta 05 · Orçamento da Cabana

Status: arquivos prontos e testados. Nada publicado nem anunciado (pedido de Bruno em 08/11/2026, fora da rodada diária).

**ClickMax (rascunhos):** produto `49a1249e-e66d-43f0-91a8-cec46e0425c4`; oferta `a09778db-bc80-4b2a-bf32-be27e7c4a9e5` (R$ 19, checkout `aQxGaFEShH`; pendência: `sellerStatus`); página `618d5a9b-fd2f-401f-953c-c35f762787c5` em `/orcamento-cabana` (rascunho). Entrega: 4 arquivos e página de acesso em `docs/p/adbc67069af26ae0/orcamento-05/`, ligados à oferta.

## 1. Tarefa concreta
Montar o orçamento da primeira cabana de hospedagem (ou chalé, bubble, tiny house, módulo, imóvel convertido), do projeto à abertura, comparar cotações, ver se cabe na verba e quanto sai em cada mês.
- **Base Zion:** procuramos no Drive e no Notion em 08/11 e não há planilha real de orçamento das Cabanas Zion (só uma cotação de enxoval de 2021 e o estudo de plantas). Por isso a copy **não** diz que parte do orçamento usado na Zion.
- **Evidência:** item 05 do Catálogo (público A). O Mapa de Oportunidades (E9) registra que não há orçamento em reais confiável para construir: daí nenhum preço de mercado no produto.

## 2. Promessa
"Aprenda o passo a passo para montar o orçamento da sua cabana de Airbnb, do projeto à abertura, com 3 cotações por item, reserva para imprevistos e cronograma de pagamentos."
Tempo para começar: cerca de 30 minutos para revisar a lista; as cotações dependem dos fornecedores. Resultado externo (custo real da obra) não depende da planilha.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Orcamento-Cabana-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Orçamento (80 linhas, lista sugerida de 39 itens em 10 etapas), Resumo e Cronograma (12 meses) |
| `Orcamento-Cabana-Zion-EXEMPLO.xlsx` | Cabana fictícia de 30 m² + 12 m² de deck: subtotal R$ 197.040, reserva 10%, total R$ 216.744, verba R$ 200.000 (passa em R$ 16.744) |
| `Ficha-de-Cotacao.pdf` | Uma ficha por item: especificação comum e 3 cotações lado a lado |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: 4 passos, 3 exercícios, critérios, checklist, limitações |
| `demonstracao/` | Telas de Itens e cotações e de Resumo com valores calculados |
| `Ferramenta05-Orcamento-Cabana-Zion.zip` | Pacote completo |

Regras: preço escolhido = cotação marcada em Escolhida (1, 2 ou 3) ou a menor; total = preço × quantidade (vazio = 1; 0 = não se aplica); diferença entre cotações = maior ÷ menor − 1; subtotal = soma; reserva = subtotal × %; diferença = verba − total com reserva; custo por m² = total com reserva ÷ área. Situação por linha: Escolha a etapa, Valor negativo, Escolhida inválida, Não se aplica, Sem cotação, Cotação escolhida vazia, Pago acima do orçado, Só 1 cotação (sem escolha), OK. Cronograma soma por mês, com "sem mês" e reserva à parte.

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **33 de 33**. Cada linha (preço, total, diferença, situação, falta pagar), o resumo (14 resultados), os totais por etapa, "etapa fora da lista", os 12 meses, "sem mês" e os totais do cronograma comparados com uma conta independente em Python: exemplo, versão em branco, 10 cenários aleatórios com erros, 6 cenários aleatórios limpos e 11 casos de borda. Exemplo conferido à mão (197.040 / 216.744 / −16.744; janelas usam a cotação 2; 30 × 1.320 = 39.600). Nenhuma célula com erro em 29 arquivos.
Revisão visual do guia, da ficha, das telas, da capa e da página no celular.
**Não testado:** Excel e Google Sheets reais (a lista de etapas usa validação que aponta para outra aba; funciona no LibreOffice); celular de verdade.

## 5. Copy (ECROI)
- **Espelhamento:** "Quanto vai custar a sua cabana?"
- **Colapso de crença:** o orçamento não estoura no preço da estrutura, e sim no que ficou fora da lista.
- **Reencadramento:** de "quanto custa uma cabana" para "o que eu preciso pagar, do projeto à abertura, com cotações comparáveis".
- **Inevitabilidade:** lista completa + 3 cotações + reserva + cronograma = você sabe antes do primeiro pagamento.
- **Resultado educacional:** você aprende a listar, cotar, comparar com a verba e planejar os pagamentos.
Botão: "Quero a planilha de orçamento" · R$ 19, pagamento único, reembolso em 7 dias.

## 6. Perguntas frequentes
Não informa preços de mercado. · Serve para cabana, chalé, bubble, tiny house, módulo ou reforma. · Não substitui arquiteto ou engenheiro. · Não diz se pode construir no terreno. · Não calcula diária nem retorno. · Funciona no celular pelos apps.

## 7. Três anúncios (1080×1350, "Saiba mais", `utm_campaign=ferramenta05`)
1. **c05a · Fora da lista:** "O orçamento estoura no que ficou fora da lista." + tela Itens e cotações. Primeira linha: "Licença, acesso, fossa, enxoval, fotos: está tudo na sua conta?"
2. **c05b · Cabe na verba?:** tela Resumo (passa em R$ 16.744, dados fictícios). Primeira linha: "Saiba antes do primeiro pagamento se o total cabe na sua verba."
3. **c05c · 3 cotações:** "Três fornecedores, três preços, três coisas diferentes." Primeira linha: "Compare cotações com a mesma especificação."

## 8. Preço, custos e entrega
R$ 19. Custos por venda: taxa do checkout, impostos, reembolsos. Entrega: 4 arquivos ligados à oferta + página de acesso. Manutenção baixa.

## 9. Execução
```
python3 -I src/build_planilha.py dist && python3 -I tests/test_planilha.py dist
python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist
bash src/empacotar.sh && python3 -I landing/build_landing.py
```

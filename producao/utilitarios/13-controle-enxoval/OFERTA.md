# Ferramenta 13 · Controle de Enxoval e Reposição

Status: arquivos prontos e testados. Nada publicado nem anunciado (rodada diária automática, 06/11/2026).

**ClickMax (rascunhos):** produto `59742f6f-5a15-4fca-be7e-ee8727e9ba33`; oferta `b667369e-f024-47b8-a8d9-46020897b95b` (R$ 19, checkout `aIN6h2A0bT`; pendência: `sellerStatus`); página `d816d6db-9283-43f7-b493-ea3afbc419cc` em `/controle-enxoval` (rascunho). Entrega por arquivo e página de acesso em `docs/p/adbc67069af26ae0/enxoval-13/`.

## 1. Tarefa concreta
Saber quanto enxoval e quantos itens de reposição existem, quanto deveria existir e o que comprar, antes que falte na troca de hóspede.
- **Base real Zion:** "Controle de Estoque — Zion" (Notion, Manual Gerencial): categorias (limpeza, enxoval, amenities), mínimo por item, atualização semanal, acionar o fornecedor ao atingir o mínimo. Generalizado; os mínimos da Zion não são usados como recomendação.
- **Evidência pública:** nenhuma fonte nova consultada nesta rodada (o acesso à web é limitado neste ambiente). **Hipótese:** falta de enxoval e de amenities na troca é dor frequente de pequenas hospedagens (Mapa de Oportunidades, item 13, já marcado como hipótese).

## 2. Promessa
"Aprenda o passo a passo para saber quanto enxoval e quantos itens de reposição você tem, quanto deveria ter e o que precisa comprar."
Tempo para começar: cerca de 20 minutos (lista, mínimos e contagem inicial). Resultado externo (não faltar item) depende dos lançamentos e da contagem semanal.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Controle-Enxoval-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Itens (13 itens comuns, mínimo calculado ou digitado), Movimentos (500 linhas), Saldo |
| `Controle-Enxoval-Zion-EXEMPLO.xlsx` | Hospedagem fictícia com 4 unidades: 5 itens para comprar, R$ 425,80 estimados |
| `Ficha-de-Contagem.pdf` | Folha de contagem semanal (armário + lavanderia) |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: 4 passos, 2 exercícios, critérios, checklist, limitações |
| `demonstracao/` | Telas de Saldo e de Movimentos com valores calculados |
| `Ferramenta13-Controle-Enxoval-Zion.zip` | Pacote completo |

Regras: saldo = entradas válidas − saídas válidas; lançamento sem item cadastrado, sem tipo ou com quantidade ≤ 0 não conta e fica marcado; COMPRAR se saldo < mínimo, "No mínimo" se igual; comprar = mínimo − saldo; mínimo digitado vale no lugar do calculado; saldo negativo pede conferência; diferença = contagem física − saldo.

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **18 de 18**. Saldo, mínimo, quantidade a comprar, situação, custo e diferença de cada item comparados com uma conta independente em Python no exemplo, em 6 cenários aleatórios (com itens fora do cadastro, quantidade zero, negativa e texto) e em 3 casos de borda; contagem de lançamentos com problema; custo total (R$ 425,80, conferido à mão); versão em branco; nenhuma célula com erro em 11 arquivos. Uma falha na primeira rodada era da minha conta à mão (6 itens no mínimo, não 1); o exemplo foi ajustado para compras acima do mínimo.
Revisão visual do guia, da ficha, das telas, da capa e da página no celular (uma linha de demonstração que não existia no exemplo foi removida).
**Não testado:** Excel e Google Sheets reais; uso no celular de verdade.

## 5. Copy (ECROI)
- **Espelhamento:** "Faltou toalha na hora da troca?"
- **Colapso de crença:** você não precisa de sistema caro; precisa de um número mínimo e de um lançamento simples.
- **Reencadramento:** compra no susto → compra no ponto certo.
- **Inevitabilidade:** mínimo definido + lançamentos + contagem semanal = a lista do que comprar aparece sozinha.
- **Resultado educacional:** você aprende a definir o mínimo de cada item e a conferir o estoque.
Título: "Faltou toalha na hora da troca?" · Botão: "Quero o meu controle" · Público: Airbnb, casas, apartamentos, pousadas e glampings · Preço: R$ 19, pagamento único, reembolso em 7 dias.

## 6. Perguntas frequentes
Serve para apartamento? Sim. · Quem define o mínimo? Você, com o passo a passo do guia. · Controla a lavanderia? Não peça por peça; a ficha tem coluna para a lavanderia. · Celular? Pelo app do Google Sheets ou Excel. · Não é para quem quer código de barras ou integração com fornecedor.

## 7. Três anúncios (1080×1350, "Saiba mais", `utm_campaign=ferramenta13`)
1. **c13a · A falta:** arte "Faltou toalha na hora da troca?" + tela Saldo. Primeira linha: "Defina o mínimo e saiba o que comprar antes de faltar."
2. **c13b · O número:** arte "Quantos jogos de lençol você tem de verdade?". Primeira linha: "Uma contagem por semana mostra o que sumiu sem ninguém lançar."
3. **c13c · A lista pronta:** arte com a lista COMPRAR · 2 / 3 / 6. Primeira linha: "A lista de compras sai da planilha, com quantidade e custo."

## 8. Preço, custos e entrega
R$ 19 (degrau das ferramentas). Custos por venda: taxa do checkout, impostos, reembolsos; comprador sem custo extra. Entrega: 4 arquivos ligados à oferta + página de acesso. Manutenção baixa.

## 9. Execução
```
python3 -I src/build_planilha.py dist && python3 -I tests/test_planilha.py dist
python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist
bash src/empacotar.sh && python3 -I landing/build_landing.py
python3 -I ../build_entrega.py && node ../render_capas.js     # a partir de producao/utilitarios
```

# Ferramenta 29 · Calculadora de Custos de Experiências

Status: arquivos prontos e testados. Nada publicado nem anunciado (rodada diária automática, 08/11/2026).

**ClickMax (rascunhos):** produto `8ac4c7b3-9da1-43b0-8933-66fae63d97c7`; oferta `a52ce33e-5340-43df-9318-bc6f4803145f` (R$ 19, checkout `zMFmcFiYq_`; pendência: `sellerStatus`); página `9aadd649-0b23-4755-a7c7-cc083b344290` em `/custos-experiencias` (rascunho). Entrega por arquivo e página de acesso em `docs/p/adbc67069af26ae0/experiencias-29/`.

## 1. Tarefa concreta
Calcular quanto custa cada sessão de uma experiência vendida junto com a hospedagem, quanto sobra depois das taxas e a partir de quantos participantes ela se paga.
- **Base Zion:** não há no Notion uma rotina de custo de experiências (só o cardápio do Bubble Service). Por isso esta ferramenta **não** diz que parte da rotina da Zion.
- **Evidência:** item 29 do Mapa de Oportunidades, marcado como **hipótese** (sem fonte de demanda). Nenhuma pesquisa nova nesta rodada.

## 2. Promessa
"Aprenda o passo a passo para calcular quanto custa cada sessão de uma experiência, quanto sobra depois das taxas e a partir de quantos participantes ela se paga."
Tempo para começar: cerca de 20 minutos com os custos em mãos. Resultado externo (vendas, procura) não depende da planilha.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Custos-Experiencias-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Calculadora (15 custos da sessão, 15 por participante, resultados) e Cenários (até 40 participantes ou a capacidade) |
| `Custos-Experiencias-Zion-EXEMPLO.xlsx` | Trilha guiada com café colonial (fictícia): 8 participantes, contribuição de R$ 31,60, mínimo de 8, preço mínimo de R$ 175,56 |
| `Ficha-da-Experiencia.pdf` | Folha para levantar custos, taxas, capacidade, responsável e regra de confirmação |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: 4 passos, 2 exercícios, critérios, checklist, limitações |
| `demonstracao/` | Telas de Resultado e de Cenários com valores calculados |
| `Ferramenta29-Custos-Experiencias-Zion.zip` | Pacote completo |

Regras: receita = preço × participantes; taxas e impostos = receita × (taxa + impostos); contribuição = receita − taxas − custos por participante − custos da sessão; mínimo = arredondar para cima (custos da sessão ÷ (preço × (1 − taxa − impostos) − custo por participante)); preço mínimo = (custos da sessão ÷ participantes + custo por participante) ÷ (1 − taxa − impostos). Bloqueia sem preço, sem participantes, com taxa + impostos ≥ 100%, com valor negativo e com participantes acima da capacidade informada. Contribuição não é lucro.

## 4. Testes
`python3 -I tests/test_planilha.py dist` → **22 de 22**, de primeira. Situação, receita, taxas, custos, contribuição, contribuição por participante, leitura, margem unitária, mínimo de participantes, "cabe na capacidade" e preço mínimo comparados com uma conta independente em Python no exemplo, em 10 cenários aleatórios e em 7 casos de borda (sem preço, taxa 100%, acima da capacidade, preço que não cobre o custo por pessoa, sem custo fixo, valor negativo, mínimo maior que a capacidade); tabela de cenários linha a linha; exemplo conferido à mão (R$ 31,60, 8 participantes, R$ 175,56); versão em branco; nenhuma célula com erro em 19 arquivos.
Revisão visual do guia, da ficha, das telas, da capa e da página no celular.
**Não testado:** Excel e Google Sheets reais; celular de verdade.

## 5. Copy (ECROI)
- **Espelhamento:** "A experiência vende. Mas ela se paga?"
- **Colapso de crença:** cobrar "o que parece justo" esquece taxa, transporte e o custo de cada pessoa.
- **Reencadramento:** de preço no olho para preço com conta e mínimo de inscritos.
- **Inevitabilidade:** custos separados + taxa real + cenários = você sabe antes de anunciar.
- **Resultado educacional:** você aprende a separar custos, calcular a contribuição e definir o mínimo para confirmar a saída.
Botão: "Quero a calculadora" · Público: hospedagens e quem oferece experiências · R$ 19, pagamento único, reembolso em 7 dias.

## 6. Perguntas frequentes
Serve para qualquer experiência vendida por pessoa e por sessão. · Contribuição não é lucro. · Não prevê procura. · Não calcula capacidade (segurança e regras locais). · Funciona no celular pelos apps.

## 7. Três anúncios (1080×1350, "Saiba mais", `utm_campaign=ferramenta29`)
1. **c29a · Se paga?** "A experiência vende. Mas ela se paga?" + tela Resultado. Primeira linha: "Some guia, transporte, comida e taxas antes de definir o preço."
2. **c29b · O mínimo:** tela Cenários (7 não cobre, 8 cobre). Primeira linha: "Saiba quantos inscritos são precisos para confirmar a saída."
3. **c29c · A taxa esquecida:** "A maquininha também participa do passeio." Primeira linha: "Coloque taxa e impostos na conta e veja o preço mínimo."

## 8. Preço, custos e entrega
R$ 19. Custos por venda: taxa do checkout, impostos, reembolsos. Entrega: 4 arquivos ligados à oferta + página de acesso. Manutenção baixa.

## 9. Execução
```
python3 -I src/build_planilha.py dist && python3 -I tests/test_planilha.py dist
python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist
bash src/empacotar.sh && python3 -I landing/build_landing.py
```

## Envio para aprovação
10/11/2026 (rodada diária): `offers_get_incomplete_reason` vazio; oferta enviada para aprovação, status `pending`. O ClickMax devolveu erro de sincronização do gateway ("Não autorizado. Token inválido ou ausente."); registrado em PENDENCIAS_BRUNO.md. Página segue em rascunho até a oferta ficar ativa.

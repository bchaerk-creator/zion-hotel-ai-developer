# MODELO FINANCEIRO · Mini Mentoria R$ 47 e demais preços

Agente: ZION FINANCE · Fase 03 · 25/11/2026 · Arquivos: `modelo_financeiro.xlsx` (planilha-molde), `build_modelo.py` (gera a planilha), `test_modelo.py` (teste).
Este arquivo não traz resultado real de venda, gasto, CPA ou conversão (repositório público). Parâmetros, fórmulas e cenários rotulados apenas. Etiquetas: [E] evidência, [H] hipótese, [NC] não confirmado.

## 1. Regra de decisão (escrita)
1. A venda do infoproduto precisa financiar a própria aquisição. Não se aceita perda inicial justificada por LTV hipotético.
2. O LTV da decisão é só o de compra única comprovada. Segundo produto aparece apenas como cenário rotulado [H] e nunca entra na decisão.
3. Faturamento não é lucro. Imposto e custos variáveis sem valor definido ficam como "a definir" (valor 0 só para a conta rodar; não é custo zero comprovado).
4. Escalar, manter ou pausar só vale com amostra mínima (parâmetros: 100 checkouts efetivos e 5 vendas, [H] ajustáveis). Abaixo disso: manter o teto e coletar.
5. Escalar ou pausar campanha só com "aprovado" de Bruno. O modelo recomenda, não executa.

## 2. Parâmetros (aba Parâmetros)
| Parâmetro | Padrão | Etiqueta | Origem |
|---|---|---|---|
| Preço Mini Mentoria | R$ 47,00 | [E] | oferta 0c71eeba |
| Taxa fixa Pix | R$ 2,49 | [E] | líquido R$ 44,51 em R$ 47 e R$ 16,51 em R$ 19 |
| Taxa % Pix neste produto | 0% | [E] | R$ 47 − 2,49 = 44,51 |
| Taxa % Pix observada em R$ 97 e R$ 270 | 6,99% | [E] ajuste de 2 pontos | R$ 97 → 87,73 e R$ 270 → 248,64 batem com 2,49 + 6,99% do preço; regra por faixa não documentada [NC] |
| Líquido Pix de referência | R$ 44,51 (R$ 47) e R$ 87,73 (R$ 97) | [E] | comissão informada pelo ClickMax |
| Mix Pix | 100% | [E] | nenhuma venda no cartão registrada até hoje |
| Taxa do cartão (fixa e %) | 0 "a definir" | [NC] | sem transação de cartão; com mix de cartão o modelo avisa que o líquido fica superestimado |
| Imposto, custos variáveis, reembolso | 0 "a definir" | a definir | sem valor definido; reembolso 7 dias (CDC), taxa a preencher |
| Margem alvo | 30% | [H] | decisão de Bruno |
| Teto de mídia | R$ 60/dia | [E] | teto da fase de teste |
| Custo por clique, por visualização, por checkout efetivo | vazio | dado real | preencher fora do repositório |
| Conversão checkout → venda | vazio | dado real | não inventar |
| Prazo de recebimento Pix e cartão | vazio | [NC] | confirmar com a Ticto |

## 3. Fórmulas (aba Mini Mentoria 47)
- Líquido médio = mix Pix × líquido Pix + (1 − mix) × líquido cartão.
- Margem de contribuição (antes da mídia) = líquido médio − imposto% × preço − custos variáveis − reembolso% × líquido médio.
- **CPA máximo** = margem de contribuição (= líquido − custos variáveis − reserva de reembolso, mais imposto quando definido).
- **CPA desejado** = CPA máximo × (1 − margem alvo).
- Ticket médio = preço (sem order bump nem upsell comprovados).
- **ROAS de equilíbrio** = preço ÷ CPA máximo.
- **CPA projetado** = custo por checkout iniciado efetivo ÷ conversão real do checkout. Sem os dois dados reais: "indisponível".
- Custo máximo por checkout = CPA desejado × conversão do checkout (e CPA máximo × conversão, no equilíbrio).
- Vendas/dia de equilíbrio no teto = teto diário ÷ margem de contribuição. Para a margem alvo: teto ÷ CPA desejado.
- Capital de giro = teto diário × prazo médio de recebimento (indisponível sem prazo).
- LTV conservador = margem de contribuição da compra única. LTV de 30, 60, 90, 180 e 365 dias é o mesmo valor, porque nenhuma recompra está comprovada.

Valores com os padrões (sem imposto, custos e reembolso definidos; Pix 100%), Mini Mentoria R$ 47: CPA máximo R$ 44,51 (teto superior, não é lucro); ROAS de equilíbrio 1,06; equilíbrio de 1,35 vendas/dia para cobrir R$ 60/dia; com margem alvo de 30%, CPA desejado R$ 31,16 e 1,93 vendas/dia. Cenário de estresse com 6,99% de taxa: CPA máximo R$ 41,22.

## 4. Tabela de decisão por faixa de CPA projetado
| Faixa | Decisão | Regra |
|---|---|---|
| Sem dado ou amostra abaixo do mínimo | NÃO DECIDIR | manter o teto de R$ 60/dia e coletar |
| CPA projetado ≤ CPA desejado | ESCALAR | subir em degraus, um por vez, com "aprovado" de Bruno |
| CPA desejado < CPA projetado ≤ CPA máximo | MANTER | cobre a mídia sem a margem alvo; otimizar criativo e checkout |
| CPA projetado > CPA máximo | PAUSAR | cada venda perde dinheiro; pausar com "aprovado" e corrigir antes |

## 5. Outros produtos (aba Outros produtos)
Preços lidos das ofertas do ClickMax em 25/11/2026 [E]. Regra de taxa 1 (só taxa fixa) vale onde há venda de R$ 19 e R$ 47; regra 2 (2,49 + 6,99%) onde há venda de R$ 97 e R$ 270. Para R$ 13, R$ 27 e R$ 67 não há venda para medir: regra 1 como [H] (taxa fixa de R$ 2,49 estimada), regra 2 mostrada como conservadora. Taxa variável do cartão: [NC].

| Preço | Ofertas | Regra | Líquido | CPA máx. (sem imposto/custos) | ROAS de equilíbrio | Vendas/dia p/ R$ 60 |
|---|---|---|---|---|---|---|
| R$ 13 | 3 e-books | 1 [H] | 10,51 | 10,51 | 1,24 | 5,71 |
| R$ 19 | ~20 ferramentas e combos | 1 [E] | 16,51 | 16,51 | 1,15 | 3,63 |
| R$ 27 | Arsenal (oferta incompleta) e ~20 microofertas do Clube | 1 [H] | 24,51 | 24,51 | 1,10 | 2,45 |
| R$ 47 | Mini Mentoria, ZC06, terra-capital A, Kit de Captação | 1 [E] | 44,51 | 44,51 | 1,06 | 1,35 |
| R$ 67 | terra-capital B | 1 [H] | 64,51 | 64,51 | 1,04 | 0,93 |
| R$ 97 | legado (Clube, acesso) e Kit de Captação do Clube (pendente de correções) | 2 [E] | 87,73 | 87,73 | 1,11 | 0,68 |
| R$ 270 | Clube inscrição + Land Bank (oferta incompleta) | 2 [E] | 248,64 | 248,64 | 1,09 | 0,24 |

O ROAS de equilíbrio fica perto de 1 em todos os preços porque o líquido é quase o preço; o que muda é o **valor absoluto** do CPA máximo, que decide se o anúncio consegue comprar uma venda.

**Por que R$ 19 é difícil de financiar com anúncio direto (matemática):**
- CPA máximo de R$ 16,51 contra R$ 44,51 do R$ 47: o teto de pagamento por venda é 2,7 vezes menor.
- A taxa fixa de R$ 2,49 consome 13,1% do R$ 19 e 5,3% do R$ 47.
- Para cobrir os mesmos R$ 60/dia, o R$ 19 precisa de 3,63 vendas/dia e o R$ 47 de 1,35 (2,7 vezes mais).
- O custo máximo por clique que fecha a conta é CPA máximo × conversão clique→venda: com qualquer conversão igual, o R$ 19 aceita 63% menos por clique que o R$ 47 (a conversão de 1% da planilha é só ilustração [H]).
- Cada venda de R$ 47 contribui como 2,7 vendas de R$ 19.

**Ranking de viabilidade para tráfego pago direto** (maior CPA máximo = mais folga): 1 R$ 270 · 2 R$ 97 · 3 R$ 67 · 4 R$ 47 · 5 R$ 27 · 6 R$ 19 · 7 R$ 13. Dentro da faixa de R$ 47, Mini Mentoria, ZC06, terra-capital A e Kit de Captação empatam no financeiro; a escolha depende de conversão e entrega, não de taxa. R$ 19 e R$ 13 servem melhor como degrau de entrada para base própria e orgânico (Ladeira de preços); como aquisição paga direta só fecham com custo por venda muito baixo. R$ 270 e R$ 97 têm mais folga, mas dependem de oferta aprovada e de condição comercial própria (R$ 270 incompleta, Kit R$ 97 pendente). O Clube é produto existente: nada foi alterado.

## 6. Cenários (aba Cenários), todos [H]
- Matriz de CPA projetado: custo por checkout (R$ 2 a R$ 15) × conversão (3% a 20%), com a letra da faixa (E, M, P) contra o CPA máximo e o desejado da aba Mini Mentoria 47. Eixos editáveis. É o mapa do que o teste precisa entregar, não previsão.
- Cenário A (evidência), B (30% cartão simulado) e C (estresse: 6,99% de taxa, imposto 6%, custos R$ 1, reembolso 5%): 6%, R$ 1 e 5% são simulações, **não são** a alíquota nem o custo da Zion.
- Capital de giro por prazo de 1, 2, 7, 14 e 30 dias (teto × prazo).

## 7. Conciliação (aba Conciliação)
Colunas: gasto Meta, vendas externas confirmadas (ClickMax), vendas na Ticto, receita bruta, líquido, divergência de vendas, CPA real, ROAS realizado, resultado de mídia e CPA real contra CPA máximo. Compras de teste internas ficam fora. Sem origem (UTM) confirmada, o CPA é limite superior de atribuição, não prova.

## 8. Teste (executado em 25/11/2026)
`python3 -I test_modelo.py`: recalcula no LibreOffice (`soffice --headless --convert-to xlsx`) e compara com conta independente em Python. Quatro rodadas: (1) modelo em branco, (2) dados fictícios com imposto, custos, reembolso, cartão e conciliação, (3) amostra pequena, (4) faixas Escalar e Manter. Resultado: 137 conferências OK, 0 falhas.

## 9. Pendências e limites
- Imposto, custos variáveis e taxa de reembolso: sem valor definido (Bruno/contador).
- Taxa do cartão e prazos de recebimento: pedir à Ticto (extrato). Confirmar também a regra de taxa por faixa de preço (2,49 até R$ 47; 2,49 + 6,99% em R$ 97 e R$ 270 [NC]).
- Conversão real do checkout: depende de corrigir o evento de início de checkout (hoje dispara no carregamento) e de UTM nas vendas.
- A planilha não decide preço nem orçamento; qualquer mudança depende de "aprovado" de Bruno.

## 10. Versão 2: aba Funil P0 (25/11/2026)
`python3 -I build_modelo.py --v2` gera `modelo_financeiro_v2.xlsx` (a v1 `modelo_financeiro.xlsx` fica intacta). Nova aba **Funil P0**: funil de 7 eventos (landing, oferta, clique no CTA com preço, início efetivo de checkout, Pix gerado, pagamento aprovado, entrega) com quantidades observadas e taxas de projeção em **amarelo, vazias** (sem dado real); em **verde**: custo por visita, por clique qualificado, por checkout efetivo e por compra (CPA), conversões, taxa Pix gerado → pago, reembolso, receita líquida, margem de contribuição, resultado de mídia, ROAS, ponto de equilíbrio, projeção (CPA projetado, ROAS, resultado) e quadro **curioso × comprador** com 3 criativos. Referência mantida: líquido R$ 44,51 (Pix R$ 47) [E]; a taxa pode seguir regra por faixa (R$ 2,49 + 6,99% em R$ 97/R$ 270 [E]; regra [NC]: confirmar no extrato da Ticto). Definições: `../12-dashboard/INDICADORES_P0.md`.
Teste: `python3 -I test_modelo.py` (testes 1 a 5 do v1 + 6 e 7 da aba Funil P0, em branco e com dados fictícios, recalculando no LibreOffice e comparando com conta independente em Python).

## 11. Versão 3: aba Funil Híbrido (25/11/2026)
`python3 -I build_modelo.py --v3` gera `modelo_financeiro_v3.xlsx` (v2 + aba **Funil Híbrido**; v1 e v2 ficam intactas, `--v2` gera o mesmo arquivo de antes). Parâmetros [H]: teto R$ 60/dia × 14 dias = R$ 840, captação R$ 30, venda quente R$ 15, venda fria R$ 15, k do limite de perda. Entradas em **amarelo, vazias**: gastos (captação, quente, fria), leads, compradores atribuídos ao quente, ao frio, não atribuídos, compradores únicos, reembolsos e a tabela de 14 coortes (leads, compradores até 7 e 14 dias, até hoje, soma de dias até a compra). Em **verde**: CPL; CPA quente = (captação + venda quente) ÷ compradores quentes; CPA frio = venda fria ÷ compradores frios; CPA global = investimento total ÷ compradores únicos; receita líquida (R$ 44,51 no Pix [E]), margem de contribuição e resultado por caminho; ROAS; ponto de equilíbrio; faixa do CPA; limite de perda (k × CPA máximo); orçamento consumido; conversão 7 e 14 dias por coorte madura; conferência de duplicidade (quente + frio + não atribuído = únicos). Protocolo: `../10-trafego/PROTOCOLO_VALIDACAO_14_DIAS.md`.
Teste: `python3 -I test_modelo.py` (testes 8 a 10 novos: em branco, dados fictícios, duplicidade, limite de perda e teto), recalculando no LibreOffice e comparando com conta independente. Imposto, custos, reembolso e taxa do cartão seguem [NC].

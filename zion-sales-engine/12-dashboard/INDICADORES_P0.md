# INDICADORES COMERCIAIS P0 · ZION SALES ENGINE

Versão 1 · 25/11/2026 · Dono: ZION FINANCE (com DATA para as fontes). Vale junto com `REGRAS_P0_COERENCIA` (ordem de Bruno): nenhum cliente chega ao checkout sem saber o que compra, quanto paga e o que recebe. Este arquivo define **como medir** isso. Nenhum número real mora aqui (repositório público).

Etiquetas: **[E]** evidência · **[H]** hipótese/parâmetro que Bruno ajusta · **[NC]** não confirmado.

## 1. O funil de 7 eventos

A ordem de Bruno separa o que antes se misturava. Cada etapa é um **evento próprio**; nenhuma substitui a outra.

| # | Etapa | Nome proposto do evento [H] | Conta quando | NÃO conta |
|---|---|---|---|---|
| 1 | Visualização da landing | `landing_view` | a página de vendas carrega, 1 por visitante por dia | clique do anúncio sem página carregada |
| 2 | Visualização da oferta | `offer_view` | o bloco da oferta (preço, entregáveis) entra na tela | rolar até o topo |
| 3 | Clique no CTA com preço | `cta_price_click` | clique no botão que mostra o preço (padrão "QUERO ACESSAR A PLATAFORMA POR R$47") | clique em botão que só rola a página |
| 4 | Início efetivo de checkout | `checkout_start` | o comprador interage com o checkout (primeiro campo preenchido ou método escolhido) [NC: a regra exata depende do que o ClickMax expõe] | **carregamento do iframe** |
| 5 | Pix gerado | `pix_generated` | o código/QR do Pix foi emitido | não é compra |
| 6 | Pagamento aprovado | `purchase_approved` | gateway confirma, conciliado ClickMax × Ticto, sem teste | Pix gerado, pendente, recusado |
| 7 | Entrega do produto | `product_delivered` | acesso liberado e login possível | e-mail enviado sem acesso funcionando |

Estado hoje [E]: o pixel roda no iframe do checkout, `ViewContent` está desligado e `InitiateCheckout` dispara **no carregamento** do iframe. Portanto o número de "checkouts iniciados" do Meta **superestima intenção** e não pode alimentar CPA nem decisão. Os eventos 2, 3 e 4 ainda **não existem** [NC]: o TRACKING define os nomes finais e a implementação; este documento só fixa o significado. Até lá, o indicador que depende deles fica **indisponível** (nunca zero, nunca substituído pelo `InitiateCheckout`).

## 2. Indicadores

Convenções: período e fuso iguais em todas as fontes; compras de teste fora; "aprovadas" = `paid` conciliado (reembolsada conta como aprovada e como reembolso). Faltou dado = **indisponível**.

| Indicador | Definição | Fórmula | Fonte do dado | Limitação |
|---|---|---|---|---|
| **Custo por visita** | Quanto a mídia paga por uma pessoa que de fato viu a página | gasto ÷ visualizações da landing (evento 1) | gasto: Meta/Windsor · visitas: ClickMax (visitantes) | Clique no link ≠ visita (perda por lentidão, bot, bloqueio). Mostrar também o CPC como auxiliar, nunca como critério. |
| **Conversão da landing** | Parte das visitas que mostra intenção real: clica no CTA com preço | cliques qualificados (evento 3) ÷ visitas (evento 1) | ClickMax/GTM [NC: evento 3 não existe] | Sem o evento 3, usar o "clique no botão" genérico mistura rolagem com intenção: não usar. |
| **Cliques qualificados no CTA** | Cliques no botão que mostra o preço, 1 por visitante por dia | contagem do evento 3 | ClickMax/GTM [NC] | Só mede intenção de ir ao checkout; quem clica já viu o preço, por isso tende a ser menos "curioso". |
| **Custo por checkout efetivo** | Quanto a mídia paga por alguém que começou o checkout de verdade | gasto ÷ início efetivo (evento 4) | Meta (gasto) + evento 4 [NC] | **Não usar o `InitiateCheckout` atual** (dispara no carregamento do iframe). Pode ser baixo e enganoso: ver quadro curioso × comprador. |
| **Conversão do checkout em pagamento aprovado** | Dos que começaram, quantos pagaram | aprovadas (evento 6) ÷ início efetivo (evento 4), mesmo período | ClickMax + Ticto + evento 4 [NC] | Atraso do Pix (pago depois do período) distorce janelas curtas: usar janela de 24 h de tolerância ou coorte por dia de início. |
| **CPA** (custo por comprador) | Quanto custa **uma venda aprovada** | gasto ÷ aprovadas | gasto: Meta · vendas: ClickMax/Ticto conciliadas | Só atribui a anúncio a venda com UTM/`ad_id`. Venda sem origem fica em "sem atribuição" e **não** é distribuída (CPA do anúncio sai maior que o real, nunca menor). Variante líquida: gasto ÷ (aprovadas − reembolsadas). |
| **Receita líquida** | O que entra depois da taxa do gateway e dos reembolsos | (aprovadas − reembolsadas) × líquido por venda | Ticto (comissão) / ClickMax | Líquido Pix de R$ 47 = **R$ 44,51** [E] (taxa fixa R$ 2,49). A taxa pode seguir regra por faixa (R$ 2,49 + 6,99% em R$ 97 e R$ 270 [E]; regra por faixa [NC]): **confirmar no extrato da Ticto**. Cartão: sem dado [NC]. Faturamento não é lucro. |
| **Margem de contribuição** | O que sobra de cada venda antes da mídia | líquido − imposto − custo variável − (reembolso realizado) | modelo financeiro (`08-financeiro/`) | Imposto e custo variável **a definir** (Bruno/contador): enquanto valerem 0, o resultado é **teto superior**, e o painel mostra "parcial". |
| **ROAS** | Receita por real de mídia | receita bruta aprovada ÷ gasto (e ROAS líquido = receita líquida ÷ gasto) | Meta + ClickMax/Ticto | Receita do Meta (pixel) subnotifica sem UTM/CAPI: usar a receita conciliada, não a do Meta. Comparar sempre com o **ROAS de equilíbrio** = preço ÷ CPA máximo. |
| **Reembolsos** | Compras devolvidas na janela de 7 dias | reembolsadas ÷ aprovadas; valor reembolsado | Ticto / ClickMax | Compras recentes (menos de 7 dias) ainda podem ser reembolsadas: taxa subestimada nos primeiros dias. Perda da taxa do gateway no reembolso [NC]. |
| **Taxa Pix gerado → pago** | Dos Pix emitidos, quantos foram pagos | Pix aprovados ÷ Pix gerados (evento 5) | Ticto (todos os status) / ClickMax só vê o repassado | O ClickMax não vê Pix expirado sem repasse [E]; sem o extrato da Ticto a taxa fica indisponível. Pix gerado **não** é Purchase. |

Indicadores auxiliares: custo por clique no link (CPC), custo por clique qualificado, taxa visita → compra, ponto de equilíbrio (vendas e visitas necessárias para cobrir o gasto), ticket médio (= preço, sem bump comprovado).

Cálculo de referência (planilha): `08-financeiro/modelo_financeiro_v2.xlsx`, aba **Funil P0**. Cálculo no painel: `12-dashboard/dashboard.html`. Os dois usam as mesmas fórmulas e são testados contra conta independente.

## 3. Regra de decisão: quem é vencedor

**Anúncio NÃO é vencedor por CPC baixo, por CTR alto nem por muitos checkouts.** Vencedor = **menor custo por comprador (CPA)**, com a conversão do checkout em aprovado e o reembolso sob controle, e com amostra mínima.

Parâmetros (todos **[H]**, Bruno ajusta; valem por anúncio/criativo; ficam em `meta.limiares` do `dados.json`):

| Parâmetro | Valor inicial [H] | Para quê |
|---|---|---|
| Visitas mínimas | 300 | sem isso a conversão da landing é ruído |
| Checkouts efetivos mínimos | 30 | sem isso a conversão do checkout é ruído |
| Compras mínimas para competir | 5 | mesmo mínimo do modelo financeiro; abaixo disso o CPA varia demais |
| Conversão mínima checkout → aprovado | 10% | piso para chamar de vencedor |
| Reembolso máximo | 10% | acima disso a venda não "ficou" |
| Corte de perda (stop-loss) | gasto ≥ 3 × CPA máximo sem atingir o CPA máximo | não esperar amostra para parar de perder |
| Índice de curiosidade | ≥ 1,5 curioso · ≤ 0,67 comprador | quadro curioso × comprador |

Referências financeiras (planilha): **CPA máximo** = margem de contribuição por venda (com imposto e custo a definir em 0, é o líquido R$ 44,51: teto superior [E]); **CPA desejado** = CPA máximo × (1 − margem alvo, 30% [H]).

Ordem de avaliação do semáforo (a primeira regra que se aplica vence):

1. **Linha "sem atribuição"**: sem decisão (não é anúncio).
2. **PAUSAR por corte de perda**: gasto ≥ 3 × CPA máximo e (nenhuma compra **ou** CPA > CPA máximo).
3. **SEM DECISÃO (amostra)**: visitas < mínimo, **ou** checkouts efetivos < mínimo, **ou** compras < mínimo.
4. **PAUSAR**: CPA > CPA máximo (cada venda perde dinheiro).
5. **ESCALAR**: CPA ≤ CPA desejado **e** conversão checkout → aprovado ≥ mínimo **e** reembolso ≤ máximo. O anúncio de menor CPA entre os que escalam é o **vencedor**.
6. **MANTER**: todo o resto (cobre a mídia, mas sem a margem, ou com conversão/reembolso fora do piso).

Escalar e pausar são **recomendação**. Executar (subir orçamento, ligar, pausar campanha) só com **"aprovado"** de Bruno. O teto de anúncio hoje é R$ 0 (campanhas só pausadas).

## 4. Quadro curioso × comprador

Mostra, por anúncio, o que ele **atrai** (cliques, visitas, checkouts) ao lado do que ele **vende** (compras). Anúncio que enche o funil e não vende é "curioso"; o que vende com menos barulho é "comprador".

- **Participação nos checkouts** = checkouts do anúncio ÷ checkouts de todos. **Participação nas compras** = compras do anúncio ÷ compras de todos.
- **Índice de curiosidade** = participação nos checkouts ÷ participação nas compras.
- **CURIOSO**: índice ≥ 1,5 [H] (ou checkouts suficientes e nenhuma compra). **COMPRADOR**: índice ≤ 0,67 [H]. **MISTO**: no meio. **AMOSTRA PEQUENA**: checkouts abaixo do mínimo.
- **Alerta de armadilha**: o anúncio tem o menor custo por checkout (ou o menor CPC) e **não** tem o menor CPA.
- O quadro compara anúncios entre si **na mesma janela e conta**; não classifica um anúncio isolado.

Limite: depende do evento 4 (início efetivo) e de atribuição por UTM. Sem eles o quadro mostra "indisponível" e o painel não finge classificação.

## 5. Qualidade do dado (o painel mostra, sem esconder)

| Verificação | Regra | Status se faltar |
|---|---|---|
| Pixel / eventos | os 7 eventos chegam e o 4 não é o carregamento do iframe | "evento ausente" por etapa |
| UTM | % das compras aprovadas com `utm_content`/`ad_id` | abaixo de 90% [H]: CPA por anúncio marcado como limite superior |
| Conciliação | ClickMax × Ticto × Meta dentro de ±10% (`09-tracking/conciliacao/conciliar.py`) | "ALERTA" com a divergência |
| Amostra | compras < 10 na base | "amostra pequena" |

## 6. Pendências e limites

- Eventos 2, 3 e 4 não existem em produção [NC]; sem eles, custo por checkout efetivo, conversão da landing e quadro curioso × comprador ficam indisponíveis (a versão com dados reais do painel deixa isso explícito).
- Imposto, custo variável e taxa de reembolso: sem valor definido (Bruno/contador).
- Taxa por faixa, taxa do cartão e prazo de recebimento: confirmar no extrato da Ticto [NC].
- Parâmetros [H] acima são ponto de partida de prudência, não benchmark de mercado.

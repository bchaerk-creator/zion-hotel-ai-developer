# Teste comercial A/B · estrutura final para autorização (27/11)
Conta Zion Collection 2 `1271873041294684`, página `576944608845537`. **Tudo PAUSADO.** Nada foi ativado e nada do que já existe foi alterado.

## 1. IDs
| Campanha | Conjunto | Anúncio | Criativo |
|---|---|---|---|
| A `120250606891890016` ZC2 \| A \| VENDA DIRETA \| QUENTE+REMARKETING | `120250606936870016` | A1 `120250607336290016` | Vídeo V17C (`1758647026274663`) |
| | | A2 `120250607339110016` | Carrossel 01 (5 cards) |
| B `120250606931740016` ZC2 \| B \| FORMULARIO \| LAL1%+FORM | `120250607328680016` | B1 `120250607340000016` | Vídeo V06 (`2410954612991521`) |
| | | B2 `120250607343490016` | Carrossel 02 (5 cards) |

## 2. Prévias
- V17C: https://bchaerk-creator.github.io/zion-hotel-ai-developer/p/adbc67069af26ae0/zc47-videos/zc47-v17c.mp4
- V06: https://bchaerk-creator.github.io/zion-hotel-ai-developer/p/adbc67069af26ae0/zc47-videos/zc47-v06.mp4
- Carrossel 01: `.../zc47-videos/zc2-car-a1.jpg` … `a5.jpg` · Carrossel 02: `zc2-car-b1.jpg` … `b5.jpg` (telas reais da plataforma; fotos aéreas reais da Zion, sem pessoas).

## 3. Públicos
- **A, incluídos:** Top Collection campeão `120250592796030016`, Collection campeão `120250592617440016`, Público Zion 90 `120250455830270016`, Público vídeo novo `120250592676910016`, Público vídeo antigo `120250455897500016`, Público Instagram `120250592672940016`, Zion Collection 365 `120250455931010016`. Excluídos: nenhum (não existe público de compradores).
- **B, incluídos:** Lookalike verdadeiro 1% `120250593921040016`, "Look a like formulário" `120250593835770016`, "Público similar personalizado" `120250592781330016`. **Excluídos:** os 7 públicos do A, para não haver sobreposição.
- Ambos: Brasil, 25 a 65 anos, Advantage+ público **desligado** (sem expansão), posicionamentos automáticos.
- Fora do teste: Base Zion Meta Email (origem não confirmada) e Público salvo amplo.

## 4. Formulário
`1959234188381295` "ZC2 | FORM | Cadastro de área | 27-11" (PT-BR, "Maior intenção" ligado). Pede nome, WhatsApp, e-mail, cidade e estado do terreno e momento do projeto (4 opções). Tela de introdução com o aviso "Parceria sujeita à análise. Não é garantida". O botão final abre `https://www.zionhotelgroup.com/inscricao?utm_source=meta&utm_medium=lead_form&utm_campaign=zc2-b-formulario&utm_content=form-obrigado`. Política de privacidade: página Privacidade Zion Land Members.
**Teste:** o envio de teste é feito na Ferramenta de Teste de Anúncios de Cadastro do Meta (developers.facebook.com/tools/lead-ads-testing), com o login do Bruno. Não tenho acesso a ela por aqui, então ainda **não está testado**. Os leads ficam na Central de Leads da página e não entram no ClickMax, na Bela nem nas automações (nenhuma integração foi criada ou alterada).

## 5. Landing e preço
`https://www.zionhotelgroup.com/inscricao`: Plataforma Zion Collection, R$ 47, checkout `/checkout-zion-47`. O anúncio diz "Adesão inicial R$ 47". A página diz pagamento único / acesso por 12 meses (mantido por decisão do Bruno).

## 6. Evento de otimização
- **A: Tráfego → visualização da página de destino**, a mesma métrica que já entrega na campanha fria ativa. Não usa Purchase (não chega ao Meta) nem InitiateCheckout (contaminado).
- **B: Cadastros → lead no formulário nativo** (evento medido pelo próprio Meta, sem pixel).
- Passar A para Vendas/Purchase só depois de configurar a CAPI no ClickMax e fazer o teste de compra.

## 7. UTMs
- A1: `utm_source=meta&utm_medium=paid_social&utm_campaign=zc2-a-venda-direta&utm_term=quente-remarketing&utm_content=a-v17c`
- A2: igual, com `utm_content=a-carrossel01` e `a-carrossel01-c1…c5` por card.
- B: leads medidos pelo formulário; quem clica no botão final chega com `utm_medium=lead_form&utm_campaign=zc2-b-formulario&utm_content=form-obrigado`.
- A landing repassa utm_* ao checkout, e o ClickMax grava source/medium/campaign/term/content na venda.

## 8. Orçamento consolidado
| Campanha | Diário | 72 h |
|---|---|---|
| Fria ativa `120250595856880016` (zc47) | R$ 30 | R$ 90 |
| A, venda direta (nova) | R$ 30 | R$ 90 |
| B, formulário (nova) | R$ 30 | R$ 90 |
| **Total** | **R$ 90/dia** | **R$ 270** |
Atenção: os públicos do A têm menos de 1.000 pessoas cada (exceto Instagram/365, com cerca de 45 mil). Com R$ 30/dia a frequência sobe rápido, então conferir frequência acima de 3 em 24 h.
**Teto (CLAUDE.md):** hoje o teto vale só para a venda fria (R$ 30/dia, R$ 420). As campanhas A e B precisam do "aprovado" do Bruno com o valor de R$ 60/dia por 72 h.

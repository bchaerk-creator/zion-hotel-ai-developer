# Conciliação ClickMax × gateway × Meta (critério R7)

Script: `conciliar.py` (Python 3, só biblioteca padrão). Testes: `python3 -I test_conciliar.py`. Os `MODELO_*.csv` têm **dados fictícios**. Dados reais ficam fora do repositório.

## Como alimentar (dados reais, fora do repositório)
| Fonte | Como obter | Colunas |
|---|---|---|
| ClickMax | Vendas > exportar CSV (colunas `src` e `sck` entram na exportação, segundo a doc) ou leitura por ferramenta | `order_id, paid_at, value_brl, status, is_test, utm_campaign, utm_content, ad_id, campaign_id, adset_id` |
| Gateway (Ticto) | Extrato de vendas com todos os status [NC: nome exato da exportação, ver tutorial C] | `order_id, paid_at, value_brl, status, payment_method` |
| Meta | Gerenciador de Anúncios > relatório por dia e campanha (Compras e Valor de conversão de compras), janela de atribuição anotada | `date, campaign_id, campaign_name, purchases, purchase_value_brl` |

Alinhe o fuso das três fontes (diga qual usou). Valor em reais com ponto (o ClickMax exporta centavos: divida **uma** vez antes).

## Regras
- Base = vendas `paid` ou `refunded` (foram pagas), sem `is_test=1`. Pendente, Pix gerado e falha ficam fora.
- Diferença % = (Meta − ClickMax) ÷ ClickMax. **Tolerância ±10%**. Zero e zero = OK; ClickMax zero e Meta maior que zero = ALERTA.
- Menos de 10 compras na base: marcado como amostra pequena; a diferença precisa ser explicada venda a venda.
- Compra do ClickMax sem `campaign_id` entra em "sem atribuição" e não é jogada em campanha nenhuma.
- ClickMax × gateway: lista ordem ausente de um lado, status diferente e valor diferente.

```bash
python3 -I conciliar.py --clickmax /fora/do/repo/clickmax.csv --gateway /fora/do/repo/ticto.csv --meta /fora/do/repo/meta.csv --json /fora/do/repo/resultado.json
```
Saída 1 se houver ALERTA. O resultado vai para o relatório de rotina de `13-relatorios/` **sem dados pessoais e sem números reais de vendas no repositório público** (guardar o relatório real fora).

## Funil P0: 7 eventos e motivo de divergência (`--funil`)
Entrada `MODELO_funil.csv` (dados **fictícios**): `date, campaign_id, landing_view, offer_view, qualified_click, checkout_effective, pix_generated, approved, delivered`. **Célula vazia = indisponível (n/d), nunca zero.** Uma linha por dia (e campanha, se houver).

| Coluna | Etapa | De onde vem |
|---|---|---|
| `landing_view` | visualização da landing | ClickMax visitantes/funil (PageView, tráfego de servidor filtrado) |
| `offer_view` | visualização da oferta | `element_visible` da seção da oferta ou ViewContent da página de oferta (ver `../FUNIL_DE_EVENTOS_P0.md`) |
| `qualified_click` | clique no CTA com preço | `button_click` dos CTAs com preço (ClickMax) |
| `checkout_effective` | início efetivo | Abriu o checkout com "Só contar depois dos dados pessoais" (histórico de envio / Meta) |
| `pix_generated` | Pix gerado | evento `pix_generated` do ClickMax ou `PixGenerated` (opcional) |
| `approved` | pagamento aprovado | vazio = usa a base do ClickMax; preenchido = conferido contra ela |
| `delivered` | entrega | membros novos na turma com e-mail de acesso enviado |

Saída: contagens, **taxas entre etapas** (oferta/visita, clique/visita, checkout/clique, aprovado/checkout, entregue/aprovado) e **motivo de divergência** quando a conta não fecha (etapa posterior maior que a anterior, aprovado diferente do ClickMax, entregue menor ou maior que aprovado, aprovado sem Pix). Pix gerado não entra na base de compras. Teste: `python3 -I test_conciliar.py` (13 testes).
```bash
python3 -I conciliar.py --clickmax /fora/do/repo/clickmax.csv --funil /fora/do/repo/funil.csv
```

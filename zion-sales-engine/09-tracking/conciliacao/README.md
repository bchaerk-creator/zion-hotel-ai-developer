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

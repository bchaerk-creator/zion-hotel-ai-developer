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

## Lead × comprador (funil híbrido): `lead_comprador.py`
Script (Python 3, só biblioteca padrão) + `test_lead_comprador.py` (14 testes, dados **fictícios**: `python3 -I test_lead_comprador.py`). Cruza leads e compras por **e-mail normalizado** e responde: quantos compradores únicos vieram do **funil quente** (lead anterior à compra, com origem/criativo/campanha/coorte), do **frio** (UTM de venda fria, sem lead) ou ficaram **não atribuídos**.

```bash
python3 -I lead_comprador.py --leads /fora/do/repo/leads.csv --compras /fora/do/repo/compras.csv --as-of 2026-12-10 --json /fora/do/repo/saida.json [--gmail-rules] [--cohort-by week] [--revisao-out /fora/do/repo/revisao.json]
```
| Regra | Valor |
|---|---|
| Correspondência | E-mail em minúsculas, sem espaços nas pontas; **só igualdade exata**. Divergiu = não casa |
| Regra opcional rotulada | `--gmail-rules`: em gmail.com/googlemail.com ignora pontos e `+tag`. Quem casa **só** por ela aparece em `match_regra_gmail_opcional` (conferir à mão) |
| Telefone | **Nunca casa sozinho.** E-mail diferente + telefone igual = `possiveis_correspondencias_para_revisao_humana` (contagem; `--revisao-out` grava só ids de pedido) |
| Precedência | 1) lead **anterior** à compra → quente; 2) senão, `utm_campaign=venda-fria` → frio; 3) senão não atribuída (com motivo). Quente com UTM fria conta **uma vez**, como quente, e aparece em `sobreposicao_quente_e_frio` |
| Comprador único | Mesmo e-mail normalizado = 1 comprador; classifica pela **primeira** compra válida |
| Base | `paid` e `refunded` (reembolsado conta e é marcado em `reembolsados_entre_compradores`); fora: teste (`is_test`), pendente, falha |
| Tempo até a compra | Dias entre a entrada do lead e o pagamento (mediana, mín., máx.); só para quentes |
| Coortes | Data de entrada do lead (ou semana); `conv_7d`/`conv_14d` só aparecem quando **todos** os leads da coorte já tiveram 7/14 dias; senão "imatura". Coorte com menos de 10 leads = `amostra_pequena` |
| Privacidade | Recusa CSV dentro do repositório; saída agregada, sem e-mail, telefone, nome nem id de pedido |

Fórmulas do financeiro (com a saída do script): CPA quente = (gasto captação + gasto venda quente) ÷ `quente`; CPA frio = gasto venda fria ÷ `frio`; CPA global = investimento total ÷ `compradores_unicos`; `nao_atribuida` entra só no global.

### Como exportar do ClickMax sem expor PII no repositório
Tudo roda na sua máquina ou no chat do ChatGPT/Claude; os CSVs ficam **fora do Git** (`~/zion-privado/`). Workspace `e87e8ba9…`. [E] = ferramenta lida/testada nesta sessão.
| Dado | Consulta (ferramenta) | Observação |
|---|---|---|
| **Leads da captação** | `leads_search` com `filters`: `tagId equals <etiqueta do formulário>` e `createdAt greaterThan <início>`; ou `leads_export_csv` com os mesmos `filters` e `columns` `["email","phone","createdAt","origin","tags"]` [E] | O **export não tem colunas de UTM** [E, lista de colunas]. Para ter criativo/campanha: faça **um export por criativo** com filtro `utmContent equals <nome do anúncio>` (e `utmCampaign`), e acrescente as colunas `utm_*` na planilha antes de juntar. `leads_get` por contato mostra `submissions[]` com `utmSource/Medium/Campaign/Content/Term` [E] |
| **Criativos existentes** | `leads_payments_utm_autocomplete` (valores distintos de utm_* já gravados) [E] | Serve para listar os nomes exatos a filtrar |
| **Contagem por criativo/coorte** (sem PII) | `leads_search` com `perPage:1` e `light:true`: o `meta.countItens` é a contagem [E] | Não precisa baixar contatos |
| **Compras** (pagas, reembolsadas) | Vendas > exportar CSV no painel (traz `src`/`sck`); ou `reports_transactions` (`startDate`/`endDate`) e `sales_get_details` por venda | Em 25/11 `reports_transactions` devolveu **erro de validação** do esquema (campos de repasse com data inválida) e `transactions_list` voltou vazio [E]: use o CSV do painel. Valor: ClickMax exporta centavos, divida **uma** vez |
| **UTM da venda** | `sales_get_utms` com o `id` da **venda** (não o do contato) [E] | É a UTM gravada na venda; sem ela a compra só atribui por lead |
| **Compras de um contato** | `leads_payments` (`leadId`), `leads_xray` (intenção, pedidos pendentes) [E] | Para conferir caso a caso |
| **Etiquetas** | `tags_manual_list` (contagem por etiqueta, `orderBy leadsCount`), `tags_list`, `tags_insights` [E] | |
| ⚠ `buyers_purchases_list` | **Não use para compradores**: a ferramenta lista a **assinatura do próprio ClickMax (plano e add-ons)**, não as compras dos seus clientes [E, descrição] | Compradores = vendas/transações |
Colunas dos CSVs de entrada: no cabeçalho do `lead_comprador.py`. Mapeie: `email`, `telefone`, `created_at` (ISO), `utm_*`; compras: `order_id`, `paid_at`, `value_brl`, `status`, `is_test`, `email`, `telefone`, `utm_*`.

# Preços · mini mentorias Zion Collection Club

Decisões de Bruno em 16/11/2026 (perguntas com opções, todas na recomendada).

## Decisões
| Tema | Decisão |
|---|---|
| Produtos | Mini mentorias à venda: A02–A08, A10, B03, B07, B09 (em aprovação). A09 e B06 entram depois das correções do Comando 05B |
| Preço de cada mini mentoria | **R$ 27**, pagamento único, Pix e cartão à vista (sem mudança: páginas e criativos já dizem R$ 27) |
| Ticket médio | **Order bump de R$ 19**: uma ferramenta-planilha por tema, ao preço normal dela (sem desconto artificial) |
| Lançamento | **Preço cheio, sem promoção** (sem preço "de" e sem urgência) |
| Teste de anúncio | **R$ 30/dia no total**: 3 produtos por vez, R$ 10/dia cada, 7 dias (cerca de R$ 210). Campanhas criadas pausadas; ativar exige "aprovado" e libera o teto |
| Regra de corte | Pausar o anúncio com **custo por venda acima de R$ 25**, avaliando depois de cerca de R$ 50 gastos por anúncio |

## Order bump por tema (R$ 19)
| Mini mentoria | Ferramenta no bump | Oferta da ferramenta | Status da ferramenta (16/11) |
|---|---|---|---|
| A02 Precificador | Ferramenta 01 · Planilha Diária Mínima | `974727ce-d051-4c86-99b6-c3b04fdf9d8e` | incompleta (não enviada) |
| A03 Custos e Rentabilidade | Ferramenta 19 · Controle de Compras e Consumo | `6c4de218-736d-4cd0-a6b2-a0e84b49d159` | página publicada |
| A04 Anúncios | Ferramenta 12 · Checklist de Fotos e Comodidades | `1651f122-ea41-417d-abb1-2838c6b793d3` | **aprovada** |
| A05 Experiências e Valor | Ferramenta 30 · Briefing de Experiência | `f28b840b-cd7d-457f-bff5-6fd6636212e2` | página publicada |
| A06 Auditor da Experiência | Ferramenta 17 · Checklist de Limpeza | `08ad22e8-9f9a-4244-856f-1bca05234924` | a conferir |
| A07 Conversão de Reservas | Ferramenta 11 · Kit de Mensagens | `fad5df5a-49fa-442e-aed7-c08cf2f6f92f` | a conferir |
| A08 Receitas Extras | Ferramenta 29 · Custos de Experiências | `a52ce33e-5340-43df-9318-bc6f4803145f` | a conferir |
| A10 Organizador Operacional | Ferramenta 14 · Quadro de Ocorrências | `74460a23-4459-4b82-8d45-70d683d02002` | a conferir |
| B03, B07, B09 (e B06 depois) | Ferramenta 05 · Orçamento da Cabana | `a09778db-bc80-4b2a-bf32-be27e7c4a9e5` | a conferir |

**Como aplicar:** `checkouts_set_order_bump` na oferta da mini mentoria, quando **as duas** ofertas (mini mentoria e ferramenta) estiverem aprovadas. As ferramentas são da sessão "Zion infoprodutos catálogo": só usamos as ofertas, sem alterá-las.

## Conta de referência (a confirmar com as taxas reais do ClickMax)
- **Receita por venda:** R$ 27 sem bump; R$ 46 com bump. O ticket médio depende da adesão real ao bump, que só se conhece testando.
- **Margem:** o valor líquido é R$ 27 menos a taxa do checkout e os impostos. A taxa exata do ClickMax/Ticto ainda não foi verificada.
- **Corte em R$ 25:** fica perto do equilíbrio sem bump e com folga quando há bump. Faturamento não é lucro.

## Observação sobre o "Token inválido"
As ofertas ainda não aprovadas mostram `providerSyncError: "Não autorizado. Token inválido ou ausente."`. A Ferramenta 12, já aprovada, mostra `gatewayName: ticto` e erro vazio. O aviso parece só refletir que a oferta ainda não foi sincronizada com o gateway, e não um bloqueio.

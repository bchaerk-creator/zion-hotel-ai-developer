# Produto 01 · Você tem terra. Falta capital? · Oferta A (R$ 47) × Oferta B (R$ 67)

**Estado (21/11): ofertas A e B ENVIADAS PARA APROVAÇÃO por ordem de Bruno (status `pending`; `providerSyncError` vazio nas duas). Páginas e portal seguem em rascunho; campanha e 14 anúncios no Meta pausados.** A página só deve ser publicada quando a oferta estiver `active`.

## Público, dor, promessa
- **Público:** quem tem terreno em destino turístico e não tem capital para desenvolver.
- **Dor:** não sabe quanto falta, se o terreno pode receber hospedagem, nem como pedir recursos sem prometer o que não pode.
- **Promessa:** "Aprenda o passo a passo de como transformar seu terreno em um projeto turístico e preparar seu patrimônio para buscar recursos, investidores e parceiros." Sem promessa de crédito, sócio, investidor ou rentabilidade. Tempo para começar a usar ≠ resultado externo.
- **Entregáveis (idênticos nas duas ofertas):** 20 microaulas (conteúdo pronto; vídeos a gravar), guia PDF de 60 p., simuladores (lacuna, operação, dívida Price/SAC), checklist documental, priorização 20·4·0,8, plano de 30 dias, mapa mental, mapa de desenvolvimento, Gerador de Dossiê (PDF).

## ClickMax (workspace e projeto padrão)
| Item | Id |
|---|---|
| Produto | `ff15b3c0-16fe-4edd-a505-0dd43f638fb0` |
| Oferta A · R$ 47 (principal, checkout `Yqp_fxiRJl`) | `1eb339a6-ba7e-4e01-b252-4694d0b53e6d` |
| Oferta B · R$ 67 (checkout `k5ETStF7A7`) | `338c9ed8-051b-4b56-80b2-a36faa2be6e0` |
| Página A (rascunho, `/terra-capital-a`) | `bd7bf43d-5c0c-4bb4-b751-cd91faf782f0` |
| Página B (rascunho, `/terra-capital-b`) | `de068af2-af72-4cf5-9f10-179198b8e6b1` |
| Portal "Zion Hotel Academy" (não publicado, `zion-hotel-academy`) | `fef2773f-754a-4b36-91c2-8cb220614cb9` |
| Turma | `c050fbc6-0c3e-43c7-af62-cef20f673a1c` (entrega ligada às duas ofertas) |
| Curso (desativado, 8 módulos, 23 aulas) | `52e9e258-60a7-48a0-860e-fd6de67c5997` |
Padrão: pagamento único, Pix e cartão à vista, sem boleto, `ZIONACADEMY`, +55 48 6137-1061, reembolso em 7 dias. `offers_get_incomplete_reason` voltou **vazio** nas duas (prontas para enviar à aprovação; **não enviei**, pois o prompt pede aguardar a aprovação de Bruno antes de vender).
Os dois checkouts têm os mesmos entregáveis; as páginas A e B são idênticas (sem preço no texto; o valor aparece no checkout), então a única diferença do teste é o preço.

## Economia (premissas do ZIP; provisão de 15% para taxas e imposto é ilustrativa)
Custos fixos: Claude Code R$ 900 + ClickMax R$ 600 = R$ 1.500/mês. CPL histórico ≈ R$ 7 (custo por lead, **não** por venda).
| Preço | Compradores/mês | Líquido/venda | CPA máximo | Conversão lead→compra necessária (CPL R$ 7) |
|---|---|---|---|---|
| R$ 47 | 30 | R$ 39.95 | R$ -10.05 | inviável |
| R$ 47 | 75 | R$ 39.95 | R$ 19.95 | 35.1% |
| R$ 47 | 150 | R$ 39.95 | R$ 29.95 | 23.4% |
| R$ 47 | 300 | R$ 39.95 | R$ 34.95 | 20.0% |
| R$ 67 | 30 | R$ 56.95 | R$ 6.95 | 100.7% |
| R$ 67 | 75 | R$ 56.95 | R$ 36.95 | 18.9% |
| R$ 67 | 150 | R$ 56.95 | R$ 46.95 | 14.9% |
| R$ 67 | 300 | R$ 56.95 | R$ 51.95 | 13.5% |

Leitura: CPA máximo = líquido por venda − fixos ÷ compradores no mês. Conversão acima de 100% = inviável com esse volume. Com poucos compradores por mês, os fixos não fecham em nenhum dos preços. Teste por **receita líquida por real investido** e por margem por criativo; não escale antes de validar. Reembolso esperado reduz o líquido (campo no `logic.js`). Os números reais vêm do extrato ClickMax/Asaas.

## Primeira venda
O objetivo é adquirir cliente e recuperar parte do investimento comercial. Nenhuma oferta complementar foi criada (Clube Zion e "encontro VIP" ficam fora até existirem e serem aprovados).

## Anúncios (somente texto; não criados, gasto R$ 0)
Formato: cada criativo 1080×1350 = um anúncio, mesma landing, `utm_source=meta&utm_medium=paid&utm_campaign=p01_terra_capital&utm_content=<criativo>&price_version=<A47|B67>`, botão "Saiba mais".
1. **Terra sem capital** — "Você tem terra. Falta capital?" Mostre o cálculo da lacuna (tela real da ferramenta, dados fictícios).
2. **Matrícula** — "Sua matrícula é um ponto de partida, não uma aprovação de crédito." (sem documento real; sem dados pessoais)
3. **Projeto** — "Antes de pedir dinheiro, descubra quanto seu projeto precisa." (gravação da ferramenta)
4. **Parceria** — "Não tem capital? Conheça alternativas antes de comprometer seu patrimônio." (mapa de responsabilidades)
Campanha só pausada, conta a confirmar com Bruno, ativar só com "aprovado".

## Indicadores
Visita à página, início de checkout, compra paga (por versão de preço), reembolso, CPA real, receita líquida por real investido, aula iniciada/concluída, ferramenta aberta, dossiê exportado (só contadores, sem valores).

# Auditoria de públicos · Zion Collection 2 (27/11) · somente leitura
Regra permanente de Bruno: nenhuma campanha com público totalmente aberto; aquisição fria priorizando o Lookalike 1% do Top Collection campeão (`120250593921040016`). Fonte: Windsor (`adset_targeting`, 30 dias). Conjuntos sem gasto em 30 dias não aparecem nessa leitura (é o caso do conjunto B `120250607328680016`, descrito pela configuração que eu mesmo criei).

## Públicos: o que é Lookalike de verdade
- **Lookalike real (único):** `120250593921040016` "Público similar (1%) - Público Top Collection campeão" (Brasil).
- **Personalizados, apesar do nome:** "Look a like formulário" `120250593835770016` e "Público similar personalizado" `120250592781330016` (interação com formulários de lead).
- Personalizados quentes: Top Collection campeão `…796030016`, Collection campeão `…617440016`, Zion 90 `…455830270016`, vídeo antigo `…455897500016`, vídeo novo `…592676910016`, Instagram `…592672940016`, Zion Collection 365 `…455931010016`.

## Matriz · campanhas ATIVAS
| Campanha / conjunto | R$/dia | Inclui | Exclui | Expansão | Criativos | Conforme? |
|---|---|---|---|---|---|---|
| ZC2 A Venda direta `120250606891890016` / `120250606936870016` | 30 | 7 quentes (Top, Collection, Zion 90, vídeo ×2, Instagram, 365) | — | Advantage+ público OFF; **expansão de público personalizado LIGADA** (`custom_audience: 1`) | V17C, V15, V14, V12b (carrossel 01 pausado) | **Não**: a expansão deixa o Meta sair dos públicos quentes |
| ZC2 B Formulário `120250606931740016` / `120250607328680016` | 10 | LAL 1% real + 2 personalizados de formulário | os 7 da A | Advantage+ OFF; expansão de LAL **a confirmar** (sem gasto ainda, o Windsor não mostra) | V06 + form Land Bank Terreno `1627911948376725` | Parcial: **mesmo LAL 1% da C3** (sobreposição) |
| [ZC47][3 TERRENO] `120250606268260016` / `120250606282700016` (carrosséis, outra conversa) | 20 | LAL 1% real | Zion 90, Collection, Top | **expansão de Lookalike LIGADA** (`lookalike: 1`) | carrosséis | **Não**: a expansão descaracteriza o LAL; não exclui vídeo/Instagram/365 (sobreposição com A) |
| [ZC47][4 POUSADA/AIRBNB] `120250606245620016` / `120250606978700016` (carrosséis, outra conversa) | 10 | **só interesses** (aluguel por temporada, B&B, Airbnb, VRBO, hotelaria + empresário) | Zion 90, Collection, Top | Advantage+ OFF | carrosséis | **Não**: frio sem base em dados próprios (interesses) |
| **Total ativo** | **70** | | | | | |

Observação: a outra conversa informou R$ 40/dia para os carrosséis; no Windsor os conjuntos ativos com gasto somam R$ 30 (C3 R$ 20 + C4 R$ 10). Se houver um terceiro conjunto de carrossel sem gasto ainda, ele não aparece aqui.

## Matriz · conjuntos PAUSADOS (31 lidos)
- **Abertos / Advantage+ (violam a regra):** `120250502488990016` (TESTE B aberto Advantage+), `120250575383730016` (venda fria carrosséis Advantage+), `120250595901940016` (ZC47 frio amplo BR, só exclusões), `120250558001040016` e `120248809133400016` (interesses com Advantage+ ligado = expansão).
- **Só interesses, sem dado próprio (não conformes para reativar):** 20 conjuntos (investidor/empresário, imobiliário, 67 destinos turísticos etc.).
- **Conformes:** `120250456017510016` e `120250555057580016` (remarketing Zion 90 + vídeo + 365); o primeiro tem expansão de personalizado ligada.

## Sobreposição
1. **B × C3:** as duas usam o mesmo LAL 1% → disputam o mesmo leilão.
2. **A × C3/C4:** C3 e C4 excluem só Top, Collection e Zion 90; quem está em vídeo/Instagram/365 pode receber A e C3/C4.
3. A × B: sem sobreposição (B exclui os 7 da A).

## Correções propostas (nada executado)
| # | Onde | Correção | Quem executa |
|---|---|---|---|
| 1 | A `120250606936870016` | Desligar a expansão de público personalizado (`custom_audience: 0`), mantendo públicos e orçamento | esta conversa |
| 2 | B `120250607328680016` | Confirmar e travar `lookalike: 0`, `custom_audience: 0` | esta conversa |
| 3 | B × C3 | Escolher: (a) B fica só com os 2 públicos de formulário e o LAL 1% fica com C3; ou (b) B mantém o LAL e C3 passa a excluir os públicos de formulário | decisão de Bruno |
| 4 | C3 `120250606282700016` | Desligar a expansão de Lookalike (`lookalike: 0`); excluir vídeo ×2, Instagram e 365 | outra conversa |
| 5 | C4 `120250606978700016` | Trocar interesses por LAL 1% (ou por um público de dados próprios) ou pausar | outra conversa / Bruno |
| 6 | Pausados abertos/Advantage+ e só interesses | Não reativar sem ajuste; renomear com o prefixo "NÃO REATIVAR" (arquivar só com aprovação) | esta conversa, se aprovado |
| 7 | Persona | Hoje a persona vem do criativo e do formulário; nenhum público separa dono de terreno × dono de pousada. Sugestão futura: LAL de leads qualificados do Land Bank quando houver volume | planejamento |

Orçamento: ativo R$ 70/dia (A 30 + B 10 + C3 20 + C4 10), dentro do teto global de R$ 80. As correções 1 a 6 não mudam orçamento.

# Auditoria de públicos · Zion Collection 2 (27/11/2026) · SOMENTE LEITURA

Conta `1271873041294684`. Nada foi alterado. Fonte: Windsor (campanhas, conjuntos, segmentação) e `list_audiences` (13 públicos: 11 personalizados, 1 lookalike, 1 salvo). O Windsor só devolve conjuntos com entrega recente: os conjuntos sem impressões nos últimos 7 a 30 dias não aparecem (ver "Não verificado").

## Regra permanente (Bruno, 27/11)
Nenhuma campanha com público totalmente aberto. Frio = Lookalike 1% do Top Collection campeão `120250593921040016`. "Similar" no nome não é lookalike: só `120250593921040016` é lookalike real (os outros "similar"/"Look a like formulário" `120250592781330016` e `120250593835770016` são personalizados).

## Matriz · campanhas no ar (ACTIVE)
| Campanha | Conjunto | Público incluído | Excluídos | Expansão | Orçamento | Termina | Conforme a regra? |
|---|---|---|---|---|---|---|---|
| C3 Terreno · Formulário `120250606268260016` | A Aquisição `120250606282700016` | **Lookalike real 1% Top Collection** `120250593921040016` (BR) | Zion 90, Collection campeão, Top Collection campeão | `advantage_audience` 0 (ok). **`targeting_relaxation_types.lookalike = 1`**: expansão do lookalike LIGADA | R$ 20/dia | 02/12 17h | Público sim; **expansão não** |
| C3 Terreno · Formulário | B Recuperação `120250606283690016` | previsto: "Look a like formulário" + "similar personalizado" (personalizados) | Top Collection, Collection campeão | não verificado | previsto R$ 10/dia | 02/12 | **Não apareceu no Windsor**: conferir no Gerenciador |
| C4 Pousada/Airbnb · Formulário `120250606245620016` | `120250606978700016` | **só interesses** (aluguel por temporada, B&B, Airbnb, hospitalidade, VRBO) + cargos (empreendedorismo, empresário); BR 25-65. Sem público de dados | Zion 90, Collection campeão, Top Collection campeão | `advantage_audience` 0 | R$ 10/dia | 02/12 | **Não**: segmentação por interesse, sem lookalike nem personalizado |
Total ativo: R$ 40/dia (A 20 + B 10 + C4 10), teto da fase ~R$ 200. Dentro do aprovado.

## Matriz · campanhas pausadas relevantes
| Campanha | Público | Expansão | Observação |
|---|---|---|---|
| ZC47 \| Frio \| Fase 1 `120250595856880016` (Tráfego, teto R$ 420) | **Frio amplo BR 25-65**, só exclui Zion 90, vídeo, 365 | 0 | **Viola a regra** (aberto, sem lookalike). Manter pausada |
| C1 Terreno · Direto, C2 Pousada · Direto (Vendas) | previstos: quente, remarketing, lookalike 1% `120250593921040016` | n/v | Conjuntos sem entrega: **não verificado** |
| [CURSO TERRENO] TESTE B `120250502488990016` | "Público aberto (Advantage+) Brasil", 18-65 | Advantage+ **1** | Aberto: nunca religar |
| [ZC2][SALES][LT47] `120250558001040016` | Advantage, 18-65 | **1** | Aberto: nunca religar |
| [ZION COLLECTION][VENDA FRIA][MM47] `120250575383730016` | Advantage, 18-65, sem interesse | **1** | Aberto: nunca religar |
| Bubble — Formulário — Validação (IMOB Advantage) `120248809133400016` | interesse + Advantage | **1** | Aberto: nunca religar |
| Demais históricos (Land Bank, Parceiro, Clube, R$ 97, MM47, Venda Urubici/Floripa, "Destinos turísticos") | interesse "Inversiones inmobiliarias" + comportamentos, BR inteiro ou 67 cidades; **sem lookalike**; só 2 usam personalizados (remarketing Zion 90 + vídeo + 365) | 0 | Segmentação por interesse; não atendem à regra nova se religados |

## Sobreposição
- C3-A (lookalike 1%) e C4 (interesses) disputam o mesmo público frio brasileiro 25-65 em hospedagem/empreendedorismo: alto risco de sobreposição e de leilão entre as duas.
- C3-B (recuperação) usa os mesmos personalizados que os conjuntos pausados de remarketing; ao religar C1/C2, excluir todos os públicos entre campanhas.
- Compradores (R$ 47 e R$ 97): **não há público de compradores** para excluir. O frio hoje pode reimpactar quem já comprou.
- C3-A e C4 excluem Zion 90, Collection campeão e Top Collection, mas **não** excluem Público vídeo `120250455897500016`, Zion collection 365 `120250455931010016` nem Instagram `120250592672940016`.

## Correções propostas (NADA executado, aguardam "aprovado")
1. **C3-A:** desligar a expansão do lookalike (`targeting_relaxation_types.lookalike` → 0) para manter o 1% estrito. Sem mudar orçamento, criativo, formulário ou data final.
2. **C4:** hoje é público de interesse. Opções: (a) pausar até existir público de dados da pousada (quem abriu/enviou o formulário `1127602653227754`, compradores com perfil pousada); (b) trocar para o Lookalike 1% `120250593921040016` com exclusão do que o C3-A já cobre (não há como excluir um lookalike de outro: sobreposição total, então o orçamento teria de sair do C3-A); (c) manter só até 02/12 como teste de exceção, por decisão de Bruno. Recomendo (a).
3. **Adicionar exclusões** a C3-A, C3-B e C4: Público vídeo, Zion collection 365 e Instagram.
4. **Criar público de compradores** (lista do ClickMax, R$ 47 e R$ 97) e excluir de todo o frio. A subida da lista exige e-mails com hash; o Windsor não tem ação para lista de clientes, então seria pelo Gerenciador, por Bruno.
5. **Frio amplo Fase 1:** manter pausada e marcar como "NÃO LIGAR" (renomear, sem apagar). Idem os 4 conjuntos Advantage+/abertos acima.
6. **Regra de bloqueio:** antes de qualquer `enable`, checar `advantage_audience = 0`, ausência de `targeting_relaxation_types`, lookalike `120250593921040016` ou personalizado nomeado, e exclusões completas.
7. **Orçamento:** manter R$ 40/dia e o teto de ~R$ 200 até 02/12; teto global de R$ 80/dia (R$ 400 em 5 dias) preservado.

## Não verificado (limites da leitura)
- Conjuntos C1, C2 e C3-B (sem entrega, não retornados pelo Windsor).
- Regras, origem e retenção de cada público personalizado, e o tamanho do lookalike: o `list_audiences` devolve só o total (13), não os campos. A origem do lookalike `120250593921040016` consta no nome ("Público Top Collection campeao").
- Preferências de posicionamento e expansão de criativo no nível do anúncio.

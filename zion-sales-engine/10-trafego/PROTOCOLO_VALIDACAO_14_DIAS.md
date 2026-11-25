# Protocolo de validação de 14 dias · funil híbrido · Mini Mentoria de Estruturação Zion (R$ 47)

ZION FINANCE · 25/11/2026 · **PROPOSTA para aprovação de Bruno. Nada foi ligado, criado ou alterado no Meta, no ClickMax ou na Ticto.** Repositório público: sem números reais (gasto, vendas, leads, CPA ou ROAS reais ficam fora). Todo valor em R$ abaixo é **parâmetro**.
Marcação: **[E]** evidência, **[H]** hipótese/parâmetro que Bruno ajusta, **[NC]** não confirmado, **[BRUNO]** só Bruno decide.
Complementa `PLANO_PROVA_FUNIL_DUAS_ETAPAS.md` (hipótese H0, holdout, consultas) com o desenho de 14 dias, limites de perda e regra de decisão. Cálculo: `../08-financeiro/modelo_financeiro_v3.xlsx`, aba **Funil Híbrido** (testada contra conta independente). Painel: `../12-dashboard/dashboard.html`, seção **Funil híbrido**.

## 1. Dois caminhos e orçamento
| Caminho | Fluxo | Orçamento planejado [H] |
|---|---|---|
| **A · quente** | anúncio de captação → formulário → CRM → educação → remarketing → landing → checkout → compra → entrega | captação R$ 30/dia + venda quente R$ 15/dia |
| **B · frio** | anúncio de venda direta → landing → checkout → compra → entrega | venda fria R$ 15/dia |
| Total | | **teto R$ 60/dia × 14 dias = R$ 840 (máximo planejado)** |

O teto é **parâmetro** (aba Funil Híbrido, linhas de parâmetros). O que está configurado hoje no Meta diverge dele e do CLAUDE.md: ver `../08-financeiro/DIVERGENCIAS_ORCAMENTO.md`. Nenhum valor passa de R$ 840 sem novo "aprovado".

## 2. Condição de início (nada começa antes)
O dia 1 só existe depois de **todos** os itens, registrados no LOG:
1. **Validação técnica** do rastreamento: Lead, Visita, Visualização da oferta, Clique no CTA com preço, Início efetivo de checkout, Pix gerado, Compra aprovada e Reembolso são eventos distintos; Purchase só após pagamento aprovado; UTM gravada na venda (compra de teste interna conferida em `sales_get_utms`); conciliação lead × comprador funcionando (`../09-tracking/conciliacao/`).
2. **Captação corrigida** no ar (cadastro gratuito, sem promessa de investimento, consultoria ou parceria) e modelo de WhatsApp substituto aprovado (o atual cita R$ 97): [NC] até Bruno confirmar.
3. **Landing v2 e checkout limpo** conferidos no celular por Bruno.
4. **Base legal e consentimentos separados** (comunicação comercial × personalização de anúncio) [BRUNO + jurídico].
5. **Autorização expressa de Bruno** ("aprovado") para ativar, com teto, escopo e data de início.
Antes disso, a contagem de dias é zero e nenhuma decisão de escala é lida.

## 3. Métricas (todas por comprador único, pagamento aprovado, sem testes e sem equipe)
| Métrica | Fórmula | Onde |
|---|---|---|
| CPL | gasto de captação ÷ leads | modelo v3 |
| Conversão lead → comprador em 7 e 14 dias | compradores pagos até 7 (14) dias após a entrada ÷ leads da coorte, só coortes com a idade completa | tabela de coortes |
| CPA quente | (captação + venda quente) ÷ compradores atribuídos ao quente | |
| CPA frio | venda fria ÷ compradores atribuídos ao frio | |
| CPA global | investimento total ÷ compradores únicos (inclui não atribuídos) | |
| Compras aprovadas | por caminho, únicos e não atribuídas | |
| Margem de contribuição e resultado de mídia | (compradores − reembolsos) × (líquido − imposto − custo variável) − investimento | faturamento não é lucro |
| Reembolsos | reembolsos em 7 dias ÷ compradores | só compras com 7 dias completos |
| Tempo até a compra | dias médios entre entrada do lead e pagamento, por coorte (frio: da primeira visita) | |
Referências: líquido Pix R$ 44,51 [E]; CPA máximo preliminar = R$ 44,51 antes dos demais custos; CPA desejado preliminar até R$ 31,16 [H] (margem alvo de 30%). Ambos são **teto superior** enquanto imposto, custos e reembolso estiverem sem valor.

## 4. Regra de atribuição e não duplicidade
Comprador único conta uma vez. Precedência: (a) última campanha paga com clique (UTM/`sck`) → frio ou quente conforme a campanha; (b) sem UTM, lead da coorte que entrou antes da compra e dentro de 14 dias → quente "por etiqueta"; (c) senão, **não atribuído** (não é distribuído). Conferência obrigatória: quente + frio + não atribuído = compradores únicos (o modelo sinaliza duplicidade ou falta). E-mail ou telefone diferente do lead: não presumir correspondência [NC].

## 5. Coortes diárias e comparação com a mesma idade
- Cada dia de entrada de leads forma uma **coorte** (14 coortes no máximo, tabela no modelo).
- A conversão de **7 dias** só é lida para coorte com **7 dias completos**; a de **14 dias** só com 14. Coorte mais nova mostra "indisponível", nunca zero e nunca é comparada com coorte mais velha.
- Comparar coortes só pela **mesma idade** (a de 7 dias da coorte do dia 3 com a de 7 dias da coorte do dia 5). Nunca comparar a conversão atual de um lead novo com a de um lead que já teve tempo de comprar.
- O dia 14 da campanha **não** fecha a leitura de 14 dias das últimas coortes: a última coorte só amadurece 14 dias depois. Janela de leitura total: até 28 dias após o início, **sem gasto adicional** nesse período (o gasto só vai até R$ 840).
- Taxa por coorte pequena é descrita com intervalo (Wilson 95%; zero compras em n leads: limite superior aproximado 3 ÷ n).

## 6. Limites de perda e critérios de interrupção
Parâmetros: `k` (múltiplo, proposta 3 [H]) e CPA máximo (modelo). **Limite de perda = k × CPA máximo** (com k = 3 e CPA máximo preliminar: R$ 133,53 por caminho). O modelo mostra "LIMITE ATINGIDO" por caminho e global. **O modelo e este protocolo só propõem: pausar exige "aprovado" de Bruno** (execução pelo ChatGPT; reversão = reativar).

| Gatilho | Por caminho | Global |
|---|---|---|
| Gasto acumulado ≥ k × CPA máximo **sem nenhuma compra atribuída** | propor pausar esse caminho (quente: captação + venda quente; frio: venda fria) | gasto total ≥ k × CPA máximo sem nenhum comprador único: propor pausar tudo |
| Reembolso acima do limite (parâmetro, proposta 10% [H]) com amostra mínima de compradores | propor pausar o caminho | idem se global |
| Rastreamento quebrado (venda sem origem acima do limite `U`, Purchase duplicado, evento de checkout voltando a disparar no carregamento) | corrigir antes de ler qualquer CPA | idem |
| Reprovação de anúncio, queda de qualidade da conta ou reclamação acima do limite | propor pausar o anúncio ou conjunto | |
| Gasto total chega a R$ 840 | o teste acaba; sem novo gasto sem novo "aprovado" | idem |
| Sinais de promessa fora do produto (lead pergunta por reunião, investimento, parceria) | revisar criativo e texto; propor pausar o anúncio | |
Interromper por perda **não** é declarar que o caminho "não funciona": é limitar o prejuízo. O relatório diz "interrompido por limite de perda, amostra insuficiente para concluir".

## 7. Condições de sucesso (todas, ao fim do teste)
1. **CPA global ≤ CPA desejado** (R$ 31,16 preliminar [H]) com o **mínimo de compras** definido na seção 8, e CPA global **≤ CPA máximo** no limite inferior do intervalo (não só no ponto).
2. **Margem de contribuição positiva** no global (e informada por caminho), com imposto, custos e reembolso **já definidos**; enquanto estiverem sem valor, o resultado é "provisório".
3. Reembolso dentro do limite; entrega fiel (compradores acessaram a plataforma).
4. Cobertura de atribuição aceitável (venda com origem ≥ 1 − `U`).
5. Conversões por coorte lidas só em coortes maduras.
O caminho quente e o frio são comparados **entre si** só se ambos atingirem o mínimo; senão, ficam descritos separadamente.

## 8. Não declarar vencedor com amostra insuficiente
**Amostra mínima.** Duas camadas, como no plano de prova:
- **Mínimo de compradores por caminho** `Nmin` (proposta 30 [H], parâmetro). Com R$ 840 no total, sobra pouco para chegar lá: o caminho frio tem R$ 210 e o quente R$ 630 (captação inclusa). Compras necessárias para só empatar com a mídia: gasto do caminho ÷ margem por venda (modelo: "ponto de equilíbrio"). **Quantas compras R$ 210 comprarão não se sabe** (depende do custo por visita e da conversão medidos): sem medida, não há previsão de prazo, só o dado ao fim.
- **Para dizer que uma taxa é maior que outra** (duas proporções, alfa 5%, poder 80%, `../11-testes-ab/amostra.py`). Cenários **hipotéticos**, não são taxas do negócio; a taxa base real vem do ClickMax:

| Taxa base (hipotética) | Efeito relativo | n por grupo | compras esperadas no grupo base |
|---|---|---|---|
| 1% | +100% | 2.319 | 23,2 |
| 2% | +100% | 1.141 | 22,8 |
| 3% | +100% | 749 | 22,5 |
| 2% | +50% | 3.826 | 76,5 |
| 3% | +50% | 2.518 | 75,5 |
| 5% | +50% | 1.471 | 73,6 |

Leitura honesta: provar diferença entre quente e frio em proporção exige **centenas a milhares de pessoas por grupo**, quase certamente além do que R$ 840 e uma base de leads de centenas entregam. Por isso a conclusão provável do teste é **descritiva** (CPA observado com intervalo e viabilidade), não "vencedor".

**Regra.** Se `Nmin` compradores por caminho não for atingido, ou se o intervalo do CPA cruzar o CPA máximo, o veredito é **INCONCLUSIVO**. Nunca se declara vencedor pelo menor CPA de poucas vendas, por CPC baixo, CPL baixo ou muitos checkouts.

**Comunicação de "inconclusivo" (modelo de texto, sem número):** "Terminamos os 14 dias com o orçamento planejado. Com as compras que tivemos, não dá para dizer qual caminho é melhor: a amostra é pequena e o custo por comprador pode variar muito. O que sabemos: [CPA e conversões observados, com intervalo]. O que NÃO sabemos: [taxa do cartão, impostos, reembolso, custos]. Recomendação: [manter / pausar / ampliar a amostra com novo orçamento], decisão de Bruno."

## 9. Tabela de cenários de decisão (quem decide: **Bruno**; o protocolo recomenda, não executa)
| Cenário | Condições | Recomendação | Execução |
|---|---|---|---|
| **Escalar** | Nmin atingido em ao menos um caminho; CPA do caminho ≤ CPA desejado e limite superior do intervalo ≤ CPA máximo; margem positiva com custos definidos; reembolso e rastreamento OK; estável em duas leituras | subir em degraus (≤ 20% do orçamento do caminho por vez, intervalo de 3 a 4 dias, "aprovado" a cada degrau) [H] | ChatGPT, com "aprovado" |
| **Manter** | CPA entre desejado e máximo, ou bom mas com amostra incompleta e sem sinal de perda | manter orçamento, corrigir criativo/checkout/rastreamento, coletar mais coortes maduras | nada a executar |
| **Pausar** | CPA do caminho > CPA máximo com amostra mínima; ou limite de perda atingido; ou reembolso alto; ou rastreamento quebrado | pausar o caminho (não apagar), corrigir antes de gastar | ChatGPT, com "aprovado" (reversão: reativar) |
| **Inconclusivo** | amostra abaixo de Nmin, intervalo cruza o CPA máximo, atribuição abaixo do mínimo, ou coortes ainda imaturas | dizer "inconclusivo" (seção 8); decidir entre encerrar, manter pausado ou novo teste com orçamento novo | Bruno |
Prioridade em conflito: **Pausar (perda) > Inconclusivo > Manter > Escalar**.

## 10. O que NÃO está confirmado [NC]
- **Taxa do cartão** (fixa e %) e prazos de recebimento: sem transação de cartão para medir; o líquido de cartão no modelo é superestimado enquanto estiver em 0.
- **Regra de taxa por faixa de preço** na Ticto (R$ 2,49 até R$ 47; R$ 2,49 + 6,99% em R$ 97/R$ 270): confirmar no extrato.
- **Impostos** (regime e alíquota), **custos variáveis** e **taxa de reembolso**/perda da taxa do gateway no reembolso: sem valor definido; CPA máximo e margem são teto superior.
- Orçamento **vigente** autorizado (CLAUDE.md × campanhas ativas) e escopo do teto (só Mini Mentoria ou conta toda).
- Campanha `120250560823800016` (não aparece no Windsor), formulários do Meta (não legíveis por MCP) e se leads de formulário gravam UTM/criativo.
- Eventos de clique com preço e início efetivo de checkout em produção; `numberOfPurchases` do ClickMax.
- Base legal para público personalizado a partir de leads; exclusões aplicáveis no Meta (Windsor só lê; criação de públicos é no Gerenciador/ChatGPT).

## 11. Registro durante o teste
Diário: gasto por papel, leads, compradores por grupo (modelo v3, **fora do repositório** com dados reais), coortes, anotações de mudanças. Nenhuma alteração de criativo, público, página ou checkout no meio (cada edição invalida a comparação e reinicia aprendizado); se for inevitável, registrar e tratar como novo teste.

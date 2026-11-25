# Divergências de orçamento · estrutura (sem valores reais)

ZION FINANCE · 25/11/2026. Repositório público: os números lidos do Meta ficam fora (scratchpad). Este arquivo diz **o que comparar** e **o que recomendar**. Marcação: [E] evidência, [H] hipótese, [NC] não confirmado.

## 1. Fonte da leitura [E]
Windsor `facebook`, conta Zion Collection 2, campos `campaign_daily_budget`, `adset_daily_budget`, `effective_status`, `adset_effective_status`, `campaign_effective_status`. O Windsor devolve o orçamento em centavos (1500 = R$ 15). Leitura só; o cache atrasa. Outras contas: só listar o que está ativo; a Zion Bubble não é tocada.

## 2. Tabela de comparação (preencher a cada leitura, fora do repositório)
| Papel no funil híbrido | Proposta de Bruno (parâmetro) | Atual configurado e ativo | Divergência |
|---|---|---|---|
| Captação (leads) | R$ 30/dia | lido do Meta | atual − proposto |
| Venda quente | R$ 15/dia | lido do Meta | atual − proposto |
| Venda fria | R$ 15/dia | lido do Meta | atual − proposto |
| Total | R$ 60/dia (R$ 840 em 14 dias) | soma dos ativos | atual − teto |

Regras de leitura: somar só conjuntos com status efetivo ativo; separar o conjunto ativo **sem anúncio ativo** (não gasta, mas conta como orçamento configurado); campanha pausada vale R$ 0; listar campanhas que o Windsor não devolve como [NC].

## 3. Divergências a verificar a cada leitura
1. Captação ativa maior que a proposta.
2. Campanhas de venda quente e fria ainda inexistentes ou pausadas (esperado antes da autorização).
3. Soma ativa acima do teto de teste.
4. Campanhas ativas **versus** o CLAUDE.md, que registra teto de anúncio R$ 0 e campanhas só pausadas.
5. Ambiguidade do teto: só a Mini Mentoria ou a conta toda.
6. Captação com texto de formulário ou destino antigo (inscrição, taxa, reunião) [NC: formulário do Meta não é legível por MCP].

## 4. Recomendação (sem editar o CLAUDE.md)
- Bruno confirma por escrito o **teto vigente** (valor, escopo e período) e quem pode ativar.
- Depois da confirmação, **atualizar o CLAUDE.md** (§1, linha "gastar com anúncio") para refletir o teto real, o escopo e a regra "campanhas novas nascem pausadas". O CLAUDE.md é do dono do repositório: este agente não o edita.
- Enquanto não houver confirmação, o orçamento de planejamento é o do modelo v3 (aba Funil Híbrido, parâmetro de R$ 60/dia) e o início da contagem dos 14 dias depende de validação técnica e de "aprovado".
- Qualquer mudança no Meta (reduzir, pausar, criar) é executada pelo ChatGPT com "aprovado" de Bruno; reversão: restaurar o orçamento anterior registrado fora do repositório.

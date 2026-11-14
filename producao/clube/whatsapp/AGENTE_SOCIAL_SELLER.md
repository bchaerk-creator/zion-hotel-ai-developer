# Agente "Social Seller Zion · Limpeza da base" (14/11/2026)

Criado no ClickMax como **rascunho**: não responde ninguém até ser publicado e colocado num canal (precisa do "aprovado" de Bruno).

| Item | Valor |
|---|---|
| Agente | `42065d48-f083-4918-b23a-b44415877abc` (status `draft`, versão 1) |
| Modelo / chave | `claude-sonnet-4-6`, chave Anthropic já cadastrada, temperatura 0,3 |
| Zaya (existente, não alterada) | `db450d9a-3298-44c8-9007-298e8855c3f8`, ativa, WhatsApp "Zion Collection" |

## Regra de Bruno (14/11)
Limpar a lista: qualificar ou descartar. Ninguém pode ficar sem venda e sem ativação.

## As quatro saídas de cada contato
1. Qualificado + reunião agendada (ativação). Tags `TRIAGEM | QUALIFICADO` + `REUNIÃO | AGENDADA`.
2. Condicional com data para retomar. Tag `TRIAGEM | CONDICIONAL`.
3. Não agora (motivo perguntado uma vez). Tag `OBJEÇÃO | NÃO AGORA`.
4. Descartado ou pediu para parar. Tag `TRIAGEM | NAO QUALIFICADO` com o motivo na nota.
Sem resposta depois das tentativas do fluxo: registrar "sem retorno".

A venda (Club) acontece na reunião, como já decidido; o agente não fala preço nem manda checkout.
Capital não é motivo de descarte; a temperatura (quente, morno, frio) só ajuda o Bruno a priorizar.

## Pendente (precisa de "aprovado")
1. Publicar o agente e criar o posto (deployment). Sugestão: funil "Base antiga · Reativação → Reunião", etapa "Respondeu · Zaya conversando"; follow-up em 4 tentativas.
2. Definir quem responde o quê: hoje a Zaya responde quem escreve no mesmo número. Sugestão: o novo agente atende só contatos com a tag de reativação e a Zaya fica de fora deles.
3. O posto da Zaya e a rotina de leads do Meta ainda apontam para o funil "Parceria Zion", arquivado em 13/11. Trocar para o "Funil Zion · Novo lead → Reunião → Venda", etapa "1 · Novos leads" (`50d19a87-4c52-41e1-81be-bcfba8d3f7f9`).
4. Teste de conversa com número do Bruno antes de ligar para a base.

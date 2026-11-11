# Automação · lead do formulário do Meta que não comprou (11/11/2026)

Dois fluxos no ClickMax (projeto Infoprodutos Zion), em **rascunho**, prontos para ativar quando o Bruno confirmar os textos:

| Fluxo | Dispara com a tag | Toques |
|---|---|---|
| Clube · Lead do formulário (terreno) sem compra `5a8e7d04-fb11-401f-b320-bfde9f6e1538` | META \| FORM CLUBE (`c9764f7c`) | 10 min · 24 h · 72 h |
| Parceiro · Lead do formulário sem compra `de4a391a-00ed-4a1e-ba45-ac7faa1a5a43` | META \| FORM PARCEIRO (`f050ffa8`) | 10 min · 24 h · 72 h |

A sincronização horária já aplica META | FORM CLUBE aos leads do "Clube Zion Collection Adesão Terreno" e META | FORM PARCEIRO aos do "Zion Collection Copy". Os leads do Diagnóstico antigo continuam com a Zaya.

**Parada ao comprar:** a venda paga aplica a tag "INSCRIÇÃO R$97 PAGA" (fluxo pós-compra). A condição "só envia se não tem a tag" e o passo "remover de outras automações" não aceitaram o formato pela API; o Bruno adiciona no canvas, no fluxo pós-compra, o passo **Remover de outras automações** (seção Ações) depois da tarefa, e assim quem compra sai das sequências.

**Créditos:** cada mensagem consome 60 créditos; o saldo em 10/11 era 873 (≈14 mensagens). Antes de ativar, comprar créditos.

## Templates (rascunho; vão ao Meta só com a confirmação do Bruno)
### Clube (botão → zionhotelgroup.com/clube)
1. `zion_clube_form_1` (10 min): Oi, {nome}! Aqui é a equipe Zion. Recebemos as suas respostas sobre o terreno, obrigado. O próximo passo para transformar o seu terreno em um destino turístico é entrar para o Zion Collection Club: formação completa, sessão estratégica com a equipe, acesso aos produtos e ao Radar do Land Bank, onde a Zion e investidores olham os terrenos inscritos. O acesso é liberado na hora, pelo site. Toque no botão para conhecer e entrar. [Entrar para o clube] [Tenho uma dúvida]
2. `zion_clube_form_2` (24 h): Oi, {nome}! Terreno parado quase nunca é falta de dinheiro. É falta de projeto no papel. Investidor não coloca dinheiro em terreno: coloca em projeto que ele entende. No Zion Collection Club você aprende as cinco etapas para estruturar o seu, do potencial do terreno ao Dossiê, e inscreve a área no Radar do Land Bank. Em 2 minutos, no vídeo da página, a gente mostra como funciona. [Ver como funciona] [Tenho uma dúvida]
3. `zion_clube_form_3` (72 h): Oi, {nome}! Última mensagem sobre isso, prometo. A Zion está em busca dos melhores destinos do Brasil, e o seu terreno pode ser o próximo. Se quiser dar o primeiro passo com a nossa equipe ao lado, a porta é o Zion Collection Club. Se preferir conversar antes, responda aqui que a equipe te chama. [Entrar para o clube] [Quero conversar] [Não quero receber]

### Parceiro (botão → zionhotelgroup.com/parceiro)
1. `zion_parceiro_form_1` (10 min): Oi, {nome}! Aqui é a equipe Zion. Recebemos as suas respostas sobre a sua área, obrigado. Na parceria Zion, você entra com a área e a infraestrutura, e a Zion entra com a bubble, a marca, a gestão das reservas e a formação da equipe. Quem opera é um gerente local, formado pela Zion. Todo parceiro entra pelo Zion Collection Club: é por ele que vêm a formação, o radar de expansão e a reunião em que desenhamos a parceria no seu local. Toque no botão para conhecer e entrar. [Ver a parceria] [Tenho uma dúvida]
2. `zion_parceiro_form_2` (24 h): Oi, {nome}! Sabe aquela área de natureza na sua pousada ou no seu terreno que hoje não rende nada? É o lugar certo para experiências de glamping, com a marca que o hóspede já procura. Pare de vender quartos. Comece a vender experiência. Em 1 minuto, no vídeo da página, mostramos o que você entra, o que a Zion entra e quem opera. [Ver como funciona] [Tenho uma dúvida]
3. `zion_parceiro_form_3` (72 h): Oi, {nome}! Última mensagem sobre isso, prometo. A Zion está em plena expansão pelo Brasil, e o seu local pode ser a próxima sede. O primeiro passo é entrar para o clube e agendar a reunião de parceria com a equipe. Se preferir conversar antes, responda aqui que a equipe te chama. [Entrar e agendar] [Quero conversar] [Não quero receber]

Quem toca "Tenho uma dúvida" ou "Quero conversar" cai na caixa da Zaya (tag TRIAGEM | ZAYA ASSUMIR pelo fluxo de botões, a configurar após a aprovação dos templates). Sem preço em nenhuma mensagem.

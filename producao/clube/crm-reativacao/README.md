# CRM de reativação · WhatsApp manual (14/11/2026)

Pedido do Bruno: um CRM com todos os leads, mensagem pronta por oferta, e um botão que abre o WhatsApp dele com o texto colado, para reativar um por um. Três ofertas: **agendamento** (agenda nativa do ClickMax), **Bubble** (página "Comprar a Bubble Zion") e **Clube** (Zion Collection Club).

**Nada foi disparado.** O envio é manual, uma pessoa por vez, pelo WhatsApp do Bruno; não passa por automação nem por disparo do ClickMax.

## Como usa
1. Abra `index.html` (com o `leads-data.js` na mesma pasta, ou importe um CSV do ClickMax na aba **Dados**).
2. Na **Fila**, escolha a oferta (Agendamento, Bubble ou Clube), leia ou edite a mensagem e toque em **Abrir WhatsApp com a mensagem**. O lead vira "contatado" e a fila avança.
3. Marque o resultado: Respondeu, Agendou, Comprou, Sem interesse ou Número errado. Quem é "sem interesse", "comprou" ou "número errado" sai da fila.
4. **Dados → Baixar CSV** guarda o andamento.

Os links levam UTM (`utm_source=whatsapp&utm_medium=reativacao_manual&utm_campaign=reativacao-<oferta>&utm_content=<id curto>`). Os textos e links se editam na aba **Textos**.

## Privacidade (importante)
- Este repositório é público. **Os leads não entram nele**: `leads-data.js` e `dados/` estão no `.gitignore`.
- Os dados ficam só no navegador (localStorage) de quem abre a página. Não hospede a página com os leads em endereço público.
- Os textos têm uma linha para quem não quiser mais receber mensagens. Quem pedir para sair deve ser marcado "Sem interesse" na hora.

## Ordem da fila
1. Entrou nos últimos 14 dias por formulário ou página (os mais novos primeiro). 2. Quentes pela etiqueta (lead quente, potencial alto, 5 mil ou mais, respondeu). 3. Entrou por formulário ou página antes disso. 4. Base antiga importada, por temperatura. A data só entra na mensagem para o grupo 1, porque nos importados por CSV a data não é a do cadastro.

## Regras de texto
Sem promessa de reserva, renda ou valorização, sem preço "de" e sem urgência falsa. As mensagens só convidam para conversar, ver a Bubble ou conhecer o Clube.

## Testes
`node tests/e2e.js` (dados fictícios): normalização de telefone, CSV, importação sem duplicar, mensagem e link do WhatsApp por oferta, abertura do WhatsApp, avanço da fila, persistência e exportação. Resultado em 14/11: 18 de 18.

## Marcar o que já foi enviado e levar para o ClickMax
- Tocar em **Abrir WhatsApp** já marca o lead como contatado, com data e hora. **Já mandei** marca sem abrir o WhatsApp (para quem você chamou por outro caminho). **Voltar para novo** desfaz.
- **Dados → Baixar CSV** exporta com o `id` do ClickMax, status, oferta e data de envio. Reimportar esse CSV restaura o andamento.
- Organização no ClickMax (tags e lista a partir desse CSV): só depois do "aprovado" do Bruno, porque altera contatos que já existem.

## Pipeline de reuniões no ClickMax (14/11/2026)
- Criado o pipeline **Reuniões agendadas · Zion** (`0983f37b-572b-443c-8f7b-d31170c1a556`, grupo "Reuniões"), separado dos funis existentes. Etapas: 1 · Agendada, 2 · Passou do horário · marcar resultado, 3 · Reunião feita, 4 · Não compareceu · reagendar, 5 · Cancelada ou remarcada.
- 9 cards, um por reunião real da agenda "Equipe Zion": 2 em Agendada (16/11 e 23/11), 6 em "Passou do horário" (reuniões de 05 a 13/11 ainda com status "agendada" na agenda) e 1 em "Não compareceu". Ficaram de fora os testes, as reuniões do próprio Bruno e as canceladas.
- Sem automação nem disparo: conferido que as automações que escutam entrada em etapa são restritas a etapas de outros pipelines. As reuniões da agenda e os cards dos funis originais não foram alterados.

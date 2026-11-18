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

## 18/11/2026 · Ligações e dois links de agendamento
- Fila com **Ligar agora** (`tel:`), **Liguei · não atendeu** (conta a ligação; a mensagem passa a começar com "Tentei te ligar agora há pouco…") e **Liguei · falamos**.
- Ofertas: **Diagnóstico prévio** (página /raio-x do site, "Diagnóstico prévio gratuito"), **Agendar reunião** (calendário nativo do ClickMax, reunião de 45 min), Bubble e Clube.
- Topo da fila: botões para copiar os dois links com UTM (`utm_medium=ligacao_manual`).
- Quem já tem reunião na agenda "Equipe Zion" (21 leads em 18/11) entra como "Já agendaram" e sai da fila, para não receber convite de novo. Quem não compareceu continua na fila.
- Base atualizada em 18/11: 2.733 leads com telefone (30 novos desde 14/11).

## 18/11/2026 · Páginas novas do diagnóstico prévio (em construção)
- O diagnóstico prévio **é a reunião** (45 min, agenda "Equipe Zion", sem custo para agendar). O CRM ainda aponta a oferta "Diagnóstico prévio" para `/raio-x/`; trocar para a página nova quando ela estiver no ar.
- Página 1 pronta: `docs/diagnostico-previo/` (descrição + calendário do ClickMax embutido + fallback + WhatsApp). Testada em celular (sem rolagem lateral, sem erro). O calendário não carrega neste ambiente de teste (SDK bloqueado), então falta conferir no ar.
- Página 2 (estruturação + checkout, R$ 470): aguarda o nome completo, o que inclui e o link de pagamento. Não existe oferta de R$ 470 no ClickMax.
- Publicação no Lovable (rotas novas): só com "aprovado" do Bruno.

## 18/11/2026 · Fila "Ligar hoje": confirmar reuniões primeiro
- A fila abre em **"Ligar hoje: reuniões e novos"**. Primeiro vêm as reuniões futuras da agenda "Equipe Zion", por horário (rótulo "0 · Confirmar reunião · hoje às 14h"); depois os novos e quentes, na ordem de prioridade.
- Card da reunião: banner com dia e hora (Brasília), **Ligar agora**, mensagem de confirmação pronta e botões **Confirmou ✓**, **Quer remarcar** e **Cancelou**. "Liguei · não atendeu" põe "Tentei te ligar agora há pouco" na mensagem.
- Reunião que já passou não entra na fila. Confirmadas e canceladas saem da fila.
- 18/11 12h30: 7 reuniões à frente (4 hoje, 2 amanhã, 1 em 23/11). As reuniões da agenda saem sem link de vídeo.

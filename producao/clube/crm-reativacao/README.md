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

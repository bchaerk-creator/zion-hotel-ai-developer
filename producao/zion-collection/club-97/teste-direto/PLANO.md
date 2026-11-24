# Plano de execução · teste de venda direta (R$ 97)

24/11/2026. Só plano: nada foi publicado, enviado ou criado. As ferramentas do ClickMax estavam sem conexão ao preparar isto. Oferta: `c298aaed-88ac-46dd-b6f3-f3c07ae08513` (checkout `1ApwIsdYSy`). Página atual longa: `/inscricao` (`77c286e6-c3d2-4492-8fd9-8d5db7921ef8`), não mexer.

## Parte 1 · ClickMax (na ordem)

| # | Passo | Ferramenta | Precisa de "aprovado"? |
|---|---|---|---|
| 0 | Conferir a conta e o estado da oferta | `sellers_status`, `offers_get` | Não (só leitura) |
| 1 | Resolver as 4 dúvidas de MINI_FICHA.md (formulário na mesma página, pré-preenchimento do checkout, redirecionar para `#pagar`, validação do HTML) | `pages_generation_context_get`, `pages_validate_html` | Não (só leitura) |
| 2 | Criar o rascunho da página curta, a partir da página atual para herdar projeto e domínio | `pages_clone` (origem `77c286e6…`, novo caminho sugerido `/inscricao-curta`) | Sim (cria coisa nova no ClickMax) |
| 3 | Validar e importar o HTML da página curta no rascunho clonado, com `pageId` do clone e `offerId` `c298aaed-88ac-46dd-b6f3-f3c07ae08513` (o clone herda o checkout da original: reimportar com o `offerId` certo e conferir o checkout `1ApwIsdYSy`) | `pages_validate_html` → `pages_import_html_draft` | Sim, junto com o passo 2 |
| 4 | Criar a mini-ficha (3 campos de escolha, mapeados para `falta_papel_meta`, `investimento`, `operador`) e embutir na página curta e, se Bruno quiser, na longa (aí é mexer no que existe: "aprovado" à parte) | `forms_create`, depois novo `pages_import_html_draft` | Sim |
| 5 | Criar o formulário pós-compra (FORMULARIO_POS_COMPRA.md, 9 campos) | `forms_create` | Sim |
| 6 | Fluxo "compra aprovada": gatilho de compra aprovada da oferta `c298aaed…`; ações: etiqueta (ex.: `Club 97 | Comprou`), e-mail de boas-vindas, WhatsApp `clube_pos_compra`. Criar DESLIGADO, testar com um contato de teste do próprio Bruno | `flows_create` | Sim para criar; outro "aprovado" para ATIVAR (ativar automação e disparar mensagem exigem "aprovado") |
| 7 | Modelo de WhatsApp `clube_pos_compra` (UTILITY, corpo e botão de MENSAGENS_POS_COMPRA.md) | `gupshup_templates_create`, depois `gupshup_templates_submit` | Sim para criar; outro "aprovado" para submeter ao Meta |
| 8 | Publicar a página curta (só com a oferta ativa/aprovada e o checkout conferido) | `pages_publish` | Sim |
| 9 | Teste de compra real e conferência do caminho completo: pagamento → acesso → formulário → mensagens. Registrar no `OFERTA.md` | (manual, Bruno) | Sim |

Antes do passo 8: abrir a página no ar em 390×780 e desktop (`node pagina-curta/teste.js`), conferir 1 checkout, botões para `#pagar`, 0 `<span>` sem cor, nenhum "270". Lembrete: o domínio de pagamento é bloqueado no ambiente de teste, então o formulário de pagamento só se confere no celular de Bruno.

## Parte 2 · Anúncios no Meta (tudo PAUSADO)

Conta Zion Collection 2. Campanha de vendas `120250538576770016`, conjunto `120250538578280016`. Usar o Windsor.ai (conector `facebook`). Confirmar a conta com Bruno antes.

Duplicar, exatamente como estão (texto original, sem editar nada):
- Carrossel C original: anúncio `120250522199990016`.
- Vídeo 02: anúncio `120250521991370016`.

Versões (duas por criativo), `url_tags` sempre com `utm_source=meta&utm_medium=paid&utm_campaign=plataforma97_vendas&utm_content=<valor>`:

| Anúncio | Destino | utm_content |
|---|---|---|
| Carrossel C | página atual `/inscricao` | `carrosselC_longa` |
| Carrossel C | página curta | `carrosselC_curta` |
| Vídeo 02 | página atual `/inscricao` | `video02_longa` |
| Vídeo 02 | página curta | `video02_curta` |

Os anúncios que já existem na campanha/conjunto (por exemplo os de `utm_campaign=plataforma97`) que forem duplicados para a outra página ganham o sufixo `_longa` ou `_curta` no `utm_content`, para o relatório não misturar as páginas. Ao duplicar para a outra página, só mudam o endereço de destino e o `utm_content`.

Botão: "Saiba mais" (lista fixa do Meta). Estado: todos criados pausados. Ativar só com "aprovado" de Bruno, e orçamento só dentro do teto aprovado (o teto atual de anúncio é R$ 0 até Bruno liberar; o conjunto foi montado com R$ 30/dia provisório).

### Alerta: não dilua o teste
Com R$ 30/dia, cada anúncio extra divide a verba e demora mais para aparecer uma venda. Com preço de R$ 97, poucas vendas por semana já são um bom sinal; quatro anúncios dividem os R$ 30 em cerca de R$ 7,50 cada.

Sugestão: manter ligados só 4 anúncios, 2 criativos × 2 páginas (os quatro da tabela acima), e deixar os demais pausados. Se Bruno quiser a resposta mais limpa sobre "qual página vende mais", comece só com UM criativo (Carrossel C) nas duas páginas (2 anúncios, R$ 15/dia cada) e só depois entre o Vídeo 02. Não comparar páginas com poucos cliques: espere pelo menos algumas vendas por página antes de concluir.

A medição é por `utm_content` e por compra confirmada no ClickMax. O custo por venda se compara com R$ 97 menos taxas e impostos; faturamento não é lucro.

## Pendências de Bruno
1. "Aprovado" para os passos 2 a 9 (cada um acima).
2. Escolha: formulário (mini-ficha) também na página longa? (mexe no que existe.)
3. Confirmar o texto exato das opções das perguntas marcadas "a conferir com o Meta".
4. Liberar `docs.clickmax.io` na rede ou conectar o ClickMax na próxima sessão, para fechar as 4 dúvidas do passo 1.
5. "Aprovado" para ativar anúncios e o teto de verba.

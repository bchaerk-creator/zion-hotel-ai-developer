# Pós-compra da oferta de R$ 97 · status (24/11/2026)

Tudo abaixo foi criado DESLIGADO (rascunho). Nenhum fluxo ativado, nenhuma mensagem enviada. Nada de dados pessoais aqui.

Oferta `c298aaed-88ac-46dd-b6f3-f3c07ae08513` (checkout `1ApwIsdYSy`, status `approved`), produto `072083e8-88c6-46bd-9e6c-5b851b6ac1c4`.

## O que foi criado
| Item | Id |
|---|---|
| Tag CLUB 97 \| COMPROU | `b552bd62-5ccf-4ce0-bf2e-500887e018c8` |
| Tag CLUB 97 \| FICHA PREENCHIDA | `54c06a96-9e96-4373-b085-eb2d0f3c3652` |
| Tag CLUB 97 \| PIX NÃO PAGO | `90c52835-1f02-498c-ac0d-d1838cc4692c` |
| Tag CLUB 97 \| CHECKOUT ABANDONADO | `c0688149-79f5-4541-91d8-c1d5ed65c36b` |
| Modelo de e-mail (rascunho) | `fc12138a-5379-47df-82d8-3d640fd10236` |
| Fluxo Compra aprovada (rascunho) | `fcc14b4d-ff0f-433c-ad9e-655e76519cd1` |
| Fluxo Pix gerado e não pago (rascunho, só etiqueta) | `01b4967a-dcf9-4962-ac6e-1dd95bf652b3` |
| Fluxo Checkout abandonado (rascunho, só etiqueta) | `deb2de62-0d9d-4da4-8dd7-9d29ad6ba9fc` |

## Fluxo de compra aprovada (ordem)
Gatilho: compra aprovada, só da oferta de R$ 97 →
1. adiciona tag COMPROU;
2. duplica o card do lead para "Inscritos · Plataforma Zion Collection" (`8b4405c0…`), etapa "1 · Comprou · falta preencher a ficha" (`779d2fa8…`);
3. transfere o card do Funil Zion (`40529cf1…`) para "8 · Comprou" (`887a445d…`);
4. concede a turma `087479a3…` do portal `3ef7a340…`;
5. e-mail de boas-vindas (remetente verificado da Zion; sem WhatsApp);
6. tarefa "Conferir acesso e ficha do inscrito".

Validação (`flows_validate`): válido nos 3 fluxos; só o aviso normal de "último passo sem próximo".

Limites a conferir antes de ligar:
- Não existe ação "criar card" no catálogo; usei duplicar + transferir. Se o lead não tiver card no Funil Zion, as etapas 2 e 3 podem falhar ou ser ignoradas. Testar com um lead de teste.
- Os campos dessas três ações (duplicar, transferir, conceder turma) foram aceitos pelo sistema, mas só um teste de execução confirma o comportamento.
- Os links do e-mail: acesso `https://zion-plataforma.clickmax.space` (confere com o subdomínio do portal) e ficha `https://infoprodutos-zion.clickmax.space/obrigado-plataforma` (página em criação por outro agente).

## Como a oferta entrega o acesso
A oferta tem 2 entregas de área de membros:
- nova: portal `3ef7a340…` / turma `087479a3…` (entrega `58bf36fb…`, criada em 24/11 05:00);
- antiga: portal `a8e2157a…` / turma `69345987…` (entrega `dbab19bc…`, criada em 24/11 00:08).
O portal novo está publicado (24/11 04:52), com primeiro acesso sem senha. Compras feitas antes das 05:00 de 24/11 não passaram pela entrega nova; o fluxo acima cobre esse caso ao conceder a turma explicitamente. Nenhuma transação aparece nesta oferta pela API de transações.

## O que Bruno precisa fazer no painel
1. Remover a entrega do portal antigo (`a8e2157a…` / `69345987…`) em Produtos → oferta → Entregas (sem ferramenta para isso).
2. Aprovar e ligar o fluxo de compra aprovada depois de um teste com um lead de teste.
3. Recuperação (Pix e checkout): só há etiqueta. Falta modelo de WhatsApp aprovado e texto antes de qualquer mensagem.
4. WhatsApp pós-compra (`clube_pos_compra`): não existe; só com aprovação.
5. Confirmar que a página `/obrigado-plataforma` está publicada.

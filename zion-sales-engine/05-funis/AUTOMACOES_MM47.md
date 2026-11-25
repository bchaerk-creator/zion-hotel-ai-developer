# Automações em RASCUNHO · Mini Mentoria R$ 47 (oferta `0c71eeba`)

Agente: FUNNEL · 25/11/2026. Tudo abaixo está em **rascunho (`draft`)**, nada ativo, nada enviado, nenhum modelo de WhatsApp criado ou submetido.
Workspace `e87e8ba9…`, projeto Infoprodutos Zion `8d1152a4…`. Marcação: **[E]** evidência, **[NC]** não confirmado.

## 1. O que foi criado (ids)

| Item | Id | Modo |
|---|---|---|
| Fluxo `[RASCUNHO] MM47 · Pós-compra` | `50e32512-e263-4074-ada4-8f3d3d347ed7` | draft |
| Fluxo `[RASCUNHO] MM47 · Pix não pago` | `d98795db-2653-4077-a0d0-ed8743259b89` | draft |
| Fluxo `[RASCUNHO] MM47 · Carrinho abandonado` | `845e3b70-ca71-4de9-923a-ee19f4cd7e73` | draft |
| Modelo de e-mail `[RASCUNHO] MM47 · Boas-vindas e acesso` | `97330e1d-0975-4ef2-99e9-a836a7750465` | biblioteca, sem envio |
| Modelo de e-mail `[RASCUNHO] MM47 · Pix expirado` | `0f78a232-d2e3-490c-b848-6e8243fbad47` | biblioteca, sem envio |
| Modelo de e-mail `[RASCUNHO] MM47 · Carrinho abandonado` | `95a66dbe-2bf4-4811-9efa-2e1ede11fa98` | biblioteca, sem envio |
| Tag `MM47 \| COMPROU` | `0366905f-2860-485c-92b8-666b1df77450` | criada (necessária aos fluxos) |
| Tag `MM47 \| PIX NÃO PAGO` | `f4ddcfc8-2c6a-4dc7-ab47-87d0ffeb89a6` | criada |
| Tag `MM47 \| CARRINHO ABANDONADO` | `44b6b5a9-a571-4e2e-88bd-92766d8046ab` | criada |

Remetente dos e-mails: assinatura confirmada `6a8925fb-0de4-4fcd-ad52-b12d796d5131` (Zion Hotel Group) [E, `email_sender_signatures_list`].

## 2. Desenho de cada fluxo

**Pós-compra** (`50e32512`): gatilho "Purchase approved" (`checkout.transaction.paid.v1`) com escopo `offerId = 0c71eeba…` → adiciona tag `MM47 | COMPROU` → duplica a oportunidade para o quadro **Alunos Zion** (`5f7000a7…`), etapa "1 · Comprou · liberar acesso" (`691189a9…`) → e-mail de boas-vindas ("Seu acesso à Mini Mentoria de Estruturação": como acessar, por onde começar, suporte, reembolso 7 dias, sem reunião, sem promessa de parceria ou investimento).
- Não há passo de "conceder acesso": a oferta já tem entrega `internal_membership` (portal `3ef7a340`, turma `087479a3`) [E]. Repetir a concessão seria redundante. A diferença para o rascunho do R$ 97 (`fcc14b4d`), que concede acesso no fluxo, é intencional.
- **Não criei tarefa para a equipe.** A venda é direta e sem atendimento individual; uma tarefa por compra cria fila que ninguém prometeu atender. Se Bruno quiser, uma tarefa só para conferir o **primeiro acesso em 24 h** (`createLeadTask`) é o único caso que faz sentido, e só durante as primeiras vendas, para validar a entrega. Fica como opção, não incluída.

**Pix não pago** (`d98795db`): gatilho "Pix expired" (`pix.expired.v1`, escopo `offerId`) → tag `MM47 | PIX NÃO PAGO` → espera 1 h → e-mail curto ("Seu Pix da Mini Mentoria expirou": nada foi cobrado, link da página com preço, sem urgência, "se já pagou, ignore").

**Carrinho abandonado** (`845e3b70`): gatilho "Cart abandoned" (`cart.abandonment.v1`, escopo `offerId`) → tag `MM47 | CARRINHO ABANDONADO` → espera 2 h → e-mail curto com o resumo da oferta e o preço, sem urgência.

Cada fluxo é **standalone**, com o escopo de oferta no gatilho, para não disparar em compras de outras ofertas. Os fluxos de pós-compra já existentes (Inscrição 270, Consultoria 360, Inscrição de Terreno) também têm escopo por oferta [E, `flows_structure_get`], então não colidem com os novos.

## 3. Validação (`flows_validate`)

Os três: `valid: true`, `hasEntryTrigger: true`, sem órfãos, sem gatilho sem saída. Único aviso: `stepWithoutNext` no e-mail final (esperado, é o fim do fluxo) [E, executado em 25/11].
**Não rodei teste com contato real** (`flows_test_runs_start`) porque enviaria e-mail de verdade.

## 4. Limitações e pontos [NC]

1. **Gatilhos existem para a oferta específica.** `checkout.transaction.paid.v1`, `pix.expired.v1`, `cart.abandonment.v1` e `checkout.pix.generated.v1` aceitam escopo `offerId` e `productId` [E, `flows_triggers_catalog`]. Os eventos `ticto-webhook.*` existem, mas só filtram por produto da Ticto e não são necessários.
2. **Sem condição "já comprou" nos fluxos de recuperação.** Tentei inserir uma condição (`tagApplied` com `MM47 | COMPROU` "is-not") entre a espera e o e-mail, para não mandar recuperação a quem pagou nesse intervalo. A API recusou o formato do passo de condição em quatro tentativas. Mitigação aplicada: o texto dos dois e-mails diz "se já pagou, pode ignorar". **Pendência:** quem for ligar os fluxos deve inserir essa condição no editor do ClickMax (passo "Condição" → tag aplicada → `MM47 | COMPROU` → "não" segue para o e-mail) ou usar o encerramento por meta do fluxo.
3. **Cartão do pipeline:** o passo "duplicar oportunidade" copia uma oportunidade que já exista. Se o comprador não tiver card em nenhum quadro, o passo pode não criar nada [NC]. O rascunho de R$ 97 (`fcc14b4d`) usa o mesmo desenho, que nunca rodou (0 execuções). Teste: compra de teste de Bruno e conferência do quadro. Alternativa se falhar: criar o card pela ferramenta de cards (`cards_create`) fora do fluxo.
4. **Variável `{name}`** usada nos e-mails como no fluxo existente; conferir a renderização no teste.
5. **Debounce:** os fluxos criados herdam 3600 s de debounce por contato. Para recuperação, 1 mensagem por contato por 7 dias é mais seguro (o fluxo da Inscrição 270 usa 604800 s). Ajustar `executionDebounceSeconds` antes de ligar.
6. **WhatsApp:** nenhum modelo foi criado ou submetido. Textos propostos estão em `MM47_WHATSAPP_TEXTOS_PROPOSTOS.md`, para aprovação.
7. O e-mail de boas-vindas diz "No primeiro acesso, siga as instruções da tela" porque o portal permite primeiro acesso sem senha [E], mas **o passo exato do login não foi visto** (login bloqueado neste ambiente) [NC]. Confirmar no teste e ajustar o texto.

## 5. Pipeline recomendado: **Alunos Zion** (`5f7000a7-2afa-40d0-9202-b1683fa43e6f`)

Por quê:
- Etapas feitas para aluno: "1 · Comprou · liberar acesso", "2 · Acesso liberado · enviar boas-vindas", "3 · Fez o primeiro acesso", "4 · Estudando", "5 · Concluiu o conteúdo", "6 · Travado · precisa de ajuda", "7 · Pediu reembolso" [E]. Cabe exatamente à entrega da Mini Mentoria, que é curso gravado.
- Está vazio e sem automação [E]: não mistura com ninguém e permite medir a Mini Mentoria isolada.
- "Inscritos · Plataforma Zion Collection" (`8b4405c0`) foi desenhado para o R$ 97: descrição fala em "ficha completa" e as etapas incluem "3 · Em avaliação pela Zion", "4 · Precisa de investimento" e "5 · Quer fazer sozinho" [E]. Para a Mini Mentoria isso **sugere avaliação e investimento que o produto não promete**. Além disso, os 2 compradores de R$ 97 estão lá; deixá-los separados evita misturar duas ofertas.

## 6. Como reverter

| Item | Reversão |
|---|---|
| Os 3 fluxos | `flows_delete` em cada id (rascunho sem execução) |
| Os 3 modelos de e-mail | `email_templates_delete` em cada id |
| As 3 tags | `tags_delete` em cada id (não aplicadas a ninguém) |
| Se um fluxo for ligado e der problema | `flows_close` (pausar) e depois `flows_delete`; tags aplicadas saem com `tags_remove_from_leads` |

Tudo acima só com "aprovado" de Bruno, exceto o que está dentro do mandato (apagar o próprio rascunho recém-criado).

## 7. Aprovação necessária para ligar

1. Teste de compra de Bruno (entrega e quadro).
2. Inserir condição "já comprou" nos dois fluxos de recuperação.
3. Ajustar debounce.
4. "Aprovado" de Bruno para `flows_activate` em cada fluxo (um de cada vez, começando por Pós-compra).

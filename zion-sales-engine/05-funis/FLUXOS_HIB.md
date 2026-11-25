# Fluxos em rascunho do funil híbrido · ClickMax

Agente: FUNNEL · 25/11/2026. Tudo em **rascunho (`draft`)**, 0 execuções, 0 contatos, nada ativado, nada enviado. Workspace `e87e8ba9…`, projeto Infoprodutos Zion `8d1152a4…`. Remetente: assinatura confirmada `6a8925fb…` (Zion Hotel Group). Marcação: **[E]**, **[NC]**.

## 1. O que foi criado

| Item | Id | Observação |
|---|---|---|
| Fluxo `[RASCUNHO] HIB · Educação do funil quente (4 e-mails)` | `e2e90fdc-1bec-49f5-9cef-25ccbf87da02` | Gatilho: etiqueta `HIB \| EDUCAÇÃO · INÍCIO`. E-mail 1 → espera 48 h → e-mail 2 → 48 h → e-mail 3 → 72 h → e-mail 4. Debounce 30 dias. `flows_validate`: válido; único aviso `stepWithoutNext` no último e-mail (esperado) [E] |
| Etiqueta `HIB \| EDUCAÇÃO · INÍCIO` | `aaf465a6-15f9-4813-bff5-1ff037e866bb` | Sem uso. Quem aplicar a etiqueta inicia o fluxo (hoje ninguém) |
| Fluxo `[RASCUNHO] HIB · Reembolso e encerramento (somente desenho)` | `0a1c9de9-ab3b-470c-a217-b947c8546f29` | **Vazio de propósito** (só desenho, seção 5). `flows_validate` acusaria falta de gatilho |
| Modelo `[RASCUNHO] HIB · Educação 3 · Mini Mentoria por dentro (R$47)` | `7f1b65d5-76f9-4236-9752-2854d9f4a5d9` | Biblioteca, versão resumida do e-mail 3 |
| Modelo `[RASCUNHO] HIB · Reembolso recebido (desenho, sem ligação a fluxo)` | `69ea3c7b-25ab-4200-884a-a5f98bb4da54` | Biblioteca, sem ligação |
| Os 3 fluxos existentes `[RASCUNHO] MM47` (Pós-compra `50e32512…`, Pix não pago `d98795db…`, Carrinho abandonado `845e3b70…`) | — | Reaproveitados **sem alteração**; revalidados em 25/11: os três `valid: true`, todos `draft` [E] |

Os e-mails da educação estão **dentro dos passos do fluxo** (HTML próprio, cores e fonte Zion). Ids dos passos do fluxo de educação: gatilho `8867a4e8…`; e-mail 1 `a6e5f2f9…`; espera `77786f57…`; e-mail 2 `73ae50c7…`; espera `663360fc…`; e-mail 3 `412c0b21…`; espera `bb01590b…`; e-mail 4 `1fa54320…`.

## 2. Educação do funil quente (e-mail primeiro)

| # | Quando | Assunto | Função | CTA |
|---|---|---|---|---|
| 1 | na entrada | "{name}, seu cadastro foi recebido (e é gratuito)" | Contrato: cadastro gratuito, o que vem, formações pagas existem e são opcionais, o cadastro não garante reunião, investimento nem parceria | nenhum |
| 2 | +48 h | "Antes de pensar em investidor, pense em estrutura" | Educação: as quatro frentes do Método Zion 360° (Desenvolvimento, Gestão, Operação, Identidade e Vendas); pergunta para pensar | nenhum |
| 3 | +96 h | "O que tem dentro da Mini Mentoria de Estruturação Zion (R$47)" | Oferta: o que inclui, o que não inclui, preço, pagamento único, garantia de 7 dias | "QUERO ACESSAR A PLATAFORMA POR R$47" → landing (nunca direto ao checkout) |
| 4 | +168 h (7 dias) | "Dúvidas comuns antes de decidir sobre a Mini Mentoria" | Objeções: precisa comprar? reunião? investimento? reembolso? acesso? | mesmo botão |

Links: `https://infoprodutos-zion.clickmax.space/mini-mentoria?utm_source=email&utm_medium=crm&utm_campaign=hib-educacao&utm_content=<e3-por-dentro|e4-duvidas>`. [NC] **Trocar** pelo endereço da landing v2 quando for publicada (hoje `/mini-mentoria` é a versão antiga, no ar).
Revisão manual do texto dos 4 e-mails (sem script; os termos "reunião", "investimento" e "parceria" aparecem só negados): sem "R$ 97", "270", "reunião" como oferta (só aparece negada), "taxa de inscrição", "equipe entrará em contato", "banco de áreas", urgência falsa, depoimento ou número de mercado.
WhatsApp: **somente texto proposto** em `FUNIL_HIBRIDO.md` seção 5 e em `MM47_WHATSAPP_TEXTOS_PROPOSTOS.md`. Nenhum modelo criado.

Limitações [NC]: o nome da variável `{name}` e o rodapé de descadastro precisam ser conferidos no teste (o HTML próprio não traz link de descadastro; confirmar se o ClickMax acrescenta um; sem ele, **não ligar**).

## 3. Recuperação e pós-compra (reaproveitados)

Sem mudança nos três fluxos existentes. O que muda é a **ordem de ligação**: Pós-compra primeiro; recuperação só depois da exclusão de compradores (seção 4).

## 4. Exclusão de compradores antes de qualquer recuperação

Tentativas desta sessão no fluxo de educação (a API recusou todas, mensagem "Expected union value") [E]:
1. `flows_steps_create` `conditional` com `statements:[{type:'leadFilter', field:'tagId', operator:'equals', negation:true, valueUuid}]`.
2. `input.conditions:[{statements:[tagApplied is-not]}]`.
3. `input:{type:'tagApplied', tagId, operator:'is-not'}`.
4. `input:{statement:{...}}`; `action:'tagApplied'` com `input:{tagId, operator}`; `statements` + `matchType:'all'`.
5. `statements` como lista aninhada; `input:{type:'statements', statements:[leadFilter]}`.
Somam-se às 5 formas já recusadas na sessão anterior (`JORNADA_ENTREGA_MM47.md` seção 7). **Conclusão: o MCP não monta passo de condição; só o editor.** A saída por evento (`triggerExit`) é só leitura. Também não há ferramenta para a "meta" do fluxo.

**Alternativa sem condição, avaliada e NÃO aplicada:** passo "Remover de outros fluxos" (`removeFromOtherFlows`) logo no início do fluxo Pós-compra. Pararia as execuções do comprador nos fluxos de recuperação e educação, mas também em **todos** os outros fluxos do workspace (Club, Land Bank etc.), o que é efeito colateral demais. Não usar sem decisão de Bruno.

**Tutorial para Bruno, no editor do ClickMax** (rótulos podem variar, [NC]); fazer nos 4 fluxos: Educação (`e2e90fdc…`), Pix não pago (`d98795db…`), Carrinho abandonado (`845e3b70…`) e, quando houver, qualquer fluxo novo de remarketing.

Opção 1 (preferida, a meta do fluxo):
1. Automações → abrir o fluxo → configurações do fluxo → **Meta**.
2. Meta = evento **Compra aprovada** (`checkout.transaction.paid.v1`) com restrição **Oferta = Mini Mentoria de Estruturação**. Manter "encerrar ao atingir a meta" ligado (já está).
3. Salvar. Quem pagar durante a espera sai do fluxo sem receber o próximo e-mail.

Opção 2 (condição antes de cada e-mail, mais robusta para educação):
1. Passe o mouse sobre a linha entre **Espera** e **E-mail** → **+** → **Condição**.
2. Tipo **Filtro de campo do lead** (ou **Pertence à lista**): etiqueta **não** contém `MM47 | COMPROU`. Se o editor aceitar a lista, usar o segmento `[HIB] 13 EXCLUSÃO` (`147d145f…`): contato **não** pertence a ele.
3. Saída **Sim** vai ao e-mail; saída **Não** fica sem destino (encerra).
4. Repetir antes dos e-mails 2, 3 e 4 e do e-mail do Pix e do carrinho.
Observação: a etiqueta `MM47 | COMPROU` só é aplicada pelo fluxo Pós-compra (desligado); por isso a Opção 2 com o segmento `[HIB] 13` (que também enxerga a turma e a transação paga) é mais segura.

Teste de prova antes de ligar (**não executado**, exige compra real): gerar um Pix, deixar expirar, pagar um novo Pix antes de a espera acabar e conferir em `flows_executions_list` que o fluxo saiu sem enviar.

## 5. Reembolso e encerramento (somente desenho)

Fluxo `0a1c9de9…` está vazio. Desenho proposto:
1. **Gatilho:** hoje [NC] — o checkout não emite evento de reembolso conhecido. Opção A: Bruno aplica manualmente a etiqueta `MM47 | REEMBOLSO` ao estornar (etiqueta a criar); opção B: evento do gateway (`ticto-webhook.*`), a verificar no catálogo quando houver o primeiro reembolso real.
2. Mover o card do quadro Alunos Zion para a etapa "7 · Pediu reembolso".
3. E-mail "Reembolso recebido" (modelo `69ea3c7b…`): confirma garantia de 7 dias, devolução pela mesma forma de pagamento, prazo depende do banco ou cartão, acesso encerrado quando concluir.
4. Encerrar: aplicar etiqueta `HIB | ENCERRADO`, **parar** educação e recuperação (por meta/condição acima) e **não** enviar mais oferta. A revogação do acesso à turma é manual (`member_users_remove_from_classroom`) por Bruno, depois do estorno confirmado; nunca automática.
5. Contar o reembolso na métrica (segmento 12 é só proxy).

## 6. Reversão

| Item | Como desfazer |
|---|---|
| Fluxo de educação `e2e90fdc…` e o de reembolso `0a1c9de9…` | `flows_delete` (rascunho sem execução) |
| Modelos `7f1b65d5…` e `69ea3c7b…` | `email_templates_delete` |
| Etiqueta `aaf465a6…` | `tags_delete` |
| Segmentos | `SEGMENTACOES_HIB.md` seção 4 |
| Os 3 fluxos MM47 | não foram tocados nesta tarefa |

## 7. Para ligar, nesta ordem (tudo com "aprovado" de Bruno)

1. Teste de compra de ponta a ponta e conferir o rodapé de descadastro dos e-mails.
2. Pós-compra `50e32512…`.
3. Exclusão de compradores nos fluxos (seção 4) e teste de prova.
4. Pausar `bc86b069` e ligar a etiqueta de entrada do lead de captação (novo fluxo pequeno, ainda por criar quando o nome da campanha corrigida existir).
5. Educação `e2e90fdc…`, depois Pix e carrinho.

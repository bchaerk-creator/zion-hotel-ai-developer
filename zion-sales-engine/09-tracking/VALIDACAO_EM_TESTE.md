# Validação em ambiente de teste · receptor `capi-webhook`

Autor: DATA · 25/11/2026 · **Sem token real, sem envio à Meta, sem dado de cliente.** Servidor do receptor **real** (HTTP) + servidor **Graph simulado** local, com payloads **fictícios** (`example.com`, ids `PEDIDO-E2E-000x`, pixel `111222333444555`).
Legenda: **[E]** provado por teste executado · **[H]** hipótese · **[NC]** não confirmado.

## 1. Como rodar
```bash
cd zion-sales-engine/09-tracking/capi-webhook
node --test tests/e2e_ciclo.test.js      # a suíte e2e (9 testes)
node --test tests/*.test.js              # tudo (43 testes)
```
Arquivo: `capi-webhook/tests/e2e_ciclo.test.js`. O Graph simulado é **mais rigoroso** que o dos testes unitários: devolve erro 400 se faltar `access_token`, se o evento tiver mais de 7 dias ou estiver no futuro, se `website` vier sem `event_source_url`, se `em/ph/fn/ln` não forem SHA-256 de 64 hex, ou se `Purchase` vier sem `value` numérico e `currency`.

## 2. Saída da execução (25/11/2026)
```
ok 1 - E2E ciclo completo: lead, Pix gerado, aprovado, reentregas e reembolso (um Purchase só, nunca no Pix gerado nem no reembolso)
ok 2 - E2E Purchase aprovado: valor em reais, event_id = id do pedido, hash do e-mail normalizado, UTMs e conteudo
ok 3 - E2E pedido sem UTM: nenhuma atribuicao inventada (fica "nao atribuida" na conciliacao)
ok 4 - E2E Pix gerado nunca e Purchase, mesmo com o evento opcional ligado (evento proprio, id proprio)
ok 5 - E2E reembolso antes de qualquer pagamento ou sem Purchase enviado: registra e nao envia Purchase
ok 6 - E2E reentrega depois de reinicio do servidor continua idempotente (armazenamento em arquivo so com ids)
ok 7 - E2E pagamento com mais de 7 dias e rejeitado pelo receptor antes do Graph (200 rejected, sem nova tentativa)
ok 8 - E2E seguranca e privacidade: sem segredo 401; logs sem e-mail, telefone, nome nem token
ok 9 - E2E achado de configuracao: sem EVENT_SOURCE_URL_DEFAULT o payload do ClickMax (sem URL) e recusado pelo contrato da CAPI para action_source=website
# tests 9   # pass 9   # fail 0
(suíte completa: # tests 43   # pass 43   # fail 0)
```

## 3. O que foi provado [E] (no receptor e no Graph simulado)
| Pedido | Prova |
|---|---|
| Lead | Webhook de formulário (`form.submitted`) → `ignored`, **0 chamadas** ao Graph. O Lead do Meta nasce no anúncio de cadastro/formulário; o receptor **não** envia Lead (evita duplicar) |
| Pix gerado ≠ Purchase | `pix_generated` pendente → `ignored`, 0 chamadas. Com `SEND_PIX_GENERATED=true` sai **`PixGenerated`** com `event_id=pix-<pedido>`; o Purchase seguinte continua único |
| Aprovado → Purchase **uma vez** | 1 chamada, 1 evento `Purchase` |
| Reentrega do mesmo pedido | 3 reentregas → `duplicate`, total de chamadas continua 1; **também após reiniciar o servidor** (arquivo só com ids, sem dado pessoal) |
| Reembolso registrado sem Purchase | `refund_registered`, `purchase_had_been_sent=true`, nenhum evento novo; 2ª notificação = `duplicate`; reembolso sem compra enviada também não gera Purchase |
| Valor em reais | `transaction.amount=4700` (centavos do ClickMax) → `custom_data.value = 47` (número), nunca 4700 nem 0,47; `currency=BRL` |
| `event_id` = id do pedido | `event_id` e `order_id` = `PEDIDO-E2E-0002` |
| Hash do e-mail normalizado | `"  Carla.Exemplo@Example.COM "` → SHA-256 de `carla.exemplo@example.com` (e `external_id` igual); telefone `(48) 99999-0001` → `5548999990001`; **nenhum dado pessoal em texto puro** no corpo enviado |
| UTMs preservadas | `utm_source/medium/campaign/content/term` e `sck` em `custom_data`, mais `content_name` e `content_ids=["mm47"]` |
| Pedido sem UTM | nenhuma chave `utm_*`, `sck`, `ad_id`, `campaign_id`, `adset_id` inventada → na conciliação vira **"não atribuída"** |
| `event_time` | hora do pagamento (≈5 min antes), não a do recebimento; pagamento com mais de 7 dias é rejeitado antes do Graph |
| Segurança | sem segredo = 401; logs sem e-mail, telefone, nome, token ou segredo |

### Achado novo do teste
**`EVENT_SOURCE_URL_DEFAULT` é obrigatório na prática.** O webhook de entrega do ClickMax não traz a URL da página; sem ela o evento `website` é recusado (502 do Graph simulado). Configurar `EVENT_SOURCE_URL_DEFAULT=https://infoprodutos-zion.clickmax.space/mini-mentoria`. Registrado no `capi-webhook/README.md`. A regra reproduzida é a da CAPI; o texto exato da Meta: **[NC]** (site bloqueado nesta sessão); a conferência real é o teste com `META_TEST_EVENT_CODE`.

## 4. O que NÃO pode ser provado sem compra real [NC]
1. Se o **Purchase nativo** do ClickMax chega ao Meta (token CAPI, Pix marcado em "Comprou", `value`/`event_id` que ele usa). O teste local só prova o receptor.
2. O **formato real** do payload do webhook de entrega/saída (campos `transaction.*`, `datetime`, `utm.*`): os caminhos usados vêm da documentação das variáveis [E doc], mas o JSON real só aparece em **Enviar teste › Ver payload**.
3. **Quando** o ClickMax dispara cada evento (pago, Pix gerado, reembolso) e se a lista de eventos oferece reembolso.
4. Se a **UTM chega à venda** (gravação em `sales_get_utms`) e se `sck`/`utm_term` com as macros do Meta vêm preenchidos.
5. **Deduplicação navegador × servidor** (cartão "Deduplicação" do Gerenciador de Eventos) e **EMQ** (qualidade de correspondência).
6. A **aceitação real pela Meta** (versão da Graph API, permissões do token, `event_source_url`, janela de 7 dias): só com `META_TEST_EVENT_CODE` na aba Testar eventos.
7. **Atribuição ao anúncio** (se o Meta casa o comprador): depende de dados reais.
8. **Taxa real, Pix expirado, cartão recusado, chargeback** no gateway (Ticto): comportamento real dos status.
9. **Entrega** (e-mail de acesso, turma, login) e o evento `AccessDelivered`.
10. **Idempotência em hospedagem serverless** (memória some): exige KV/arquivo persistente na hospedagem escolhida.

## 5. Checklist da compra de teste de Bruno (**só quando ele autorizar**)
Pré-condições: Bruno diz "aprovado" por escrito; o receptor **não** está ligado ao mesmo tempo que o Purchase nativo (um dos dois, nunca os dois); `META_TEST_EVENT_CODE` preenchido no receptor **e/ou** no pixel; compra de **uma** unidade, com dados do próprio Bruno, reembolsável.
- [ ] 1. Abrir a página por link com UTM de teste (`utm_source=teste&utm_medium=manual&utm_campaign=mm47&utm_content=checklist`, `PADRAO_UTM.md` §5). Ver a UTM na barra.
- [ ] 2. **Testar eventos**: `PageView` aparece; **nenhum** `InitiateCheckout` antes de nome e e-mail (se a opção A4 estiver ligada).
- [ ] 3. Informar nome e e-mail → `InitiateCheckout` aparece **uma vez**.
- [ ] 4. **Gerar o Pix e não pagar**: esperado **nenhum Purchase**; venda `pending` com UTMs; (se ligado) `PixGenerated`.
- [ ] 5. **Pagar o Pix** (R$ 47): **um** Purchase, `value 47,00`, `BRL`, `event_id` = id do pedido, origem servidor (e navegador no nativo, **mesmo** id). Histórico de envio "Enviado".
- [ ] 6. `sales_get_utms` da venda: `utm_source/medium/campaign/content` (e `sck`) gravados.
- [ ] 7. Entrega: e-mail de acesso, contato na turma, login; obrigado sem R$ 97/R$ 270/reunião.
- [ ] 8. **Reembolsar** a compra de teste: venda `refunded`; **nenhum Purchase novo**; registro no receptor (`refund_registered`).
- [ ] 9. **Reenviar** o webhook (Enviar teste ou reentrega): `duplicate`, sem 2º Purchase.
- [ ] 10. Rodar `conciliacao/conciliar.py` e `lead_comprador.py` com os dados do teste (a compra de teste fica fora por `is_test`); limpar o código de teste.
Critérios R1 a R8 e prints: `tutorial/` (capítulos D, E e F).

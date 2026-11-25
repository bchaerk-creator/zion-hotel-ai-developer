# Receptor de webhook → Purchase na Conversions API (opção C do plano)

Estado: **código pronto e testado localmente com payloads fictícios e servidor Graph simulado. NÃO implantado. Nada foi enviado à Meta. Nenhum token real foi usado.** Para usar, Bruno precisa dizer "aprovado" (configurar webhook e CAPI em produção está fora do que o agente DATA pode fazer sozinho).

Quando usar: só se o roteiro de teste da opção A (config nativa do ClickMax) provar que o Purchase pago **não** chega ao Meta. Se a nativa funcionar, **não ligue este receptor** (evita Purchase em dobro). Ver `../PLANO_EXECUTAVEL.md`, seção 4.

## O que ele faz
1. Recebe `POST /webhook` do ClickMax (ou da Ticto).
2. Confere o segredo (header `cm-token`, query ou campo do corpo) em tempo constante. Sem segredo certo: 401.
3. Classifica (pago = status `paid` ou `approved` por padrão; `authorized`, `completed` e `captured` só entram se a variável `PAID_STATUSES` os listar, com evidência do payload real; nome com `pending` nunca vira compra): **pago** → Purchase; **reembolso/chargeback/cancelamento** → só registra (e, se ligado, envia o evento próprio `ZionRefund`, nunca `Purchase`); **Pix gerado, pendente, aguardando, expirado, falho, recusado, carrinho abandonado, renovação de assinatura** → ignora (responde 200 `ignored`).
4. Monta o evento: `event_name=Purchase`, `event_id` = id da transação, `event_time` = hora do pagamento (nunca no futuro; barra mais de 7 dias), `action_source=website`, `event_source_url`, `custom_data.value` em **reais com ponto decimal** (dividido uma única vez; faixa de segurança `MIN_VALUE`/`MAX_VALUE` barra 0,97 e 9700), `currency=BRL`, UTMs/src/sck/ad_id/campaign_id/adset_id em `custom_data`.
5. `user_data`: e-mail, telefone, nome e sobrenome normalizados e com **SHA-256**; `external_id` = hash do e-mail; `fbc`, `fbp`, IP e user-agent **sem hash**, só se vierem. Sem nenhuma chave de correspondência o evento não é enviado.
6. Idempotência por `event_id`: o mesmo pedido enviado de novo não gera nova chamada. Só marca "enviado" depois que o Meta confirma (`events_received`). Falha do Meta devolve 502, e o ClickMax tenta de novo (até 3 vezes).
7. Respostas de rejeição por regra (valor fora da faixa, sem dado de correspondência, evento antigo) voltam **200** de propósito: o ClickMax desativa a integração depois de 15 falhas seguidas, e tentar de novo não resolve.
8. Logs só com `event_id`, motivo, valor e moeda. **Sem e-mail, telefone, nome ou token** (teste automático confere).

## Funil P0: o que vira Purchase e os eventos opcionais (atualizado em 25/11/2026)
Ver `../FUNIL_DE_EVENTOS_P0.md`. Resumo do que o código garante (34 testes automáticos):
- **Só pagamento aprovado vira `Purchase`** (`paid`/`approved`, `value` em reais com ponto, `currency=BRL`, `event_id` = id do pedido, UTMs, `content_name`, `content_ids`). Pix gerado, pendente, autorizado e `paid_pending` não.
- **Pix gerado**: ignorado por padrão. Com `SEND_PIX_GENERATED=true` envia o evento **custom** `PixGenerated` (nome em `PIX_GENERATED_EVENT_NAME`; o servidor **recusa** o nome `Purchase`), com `event_id` próprio `pix-<id do pedido>`, `value` do pedido (informativo, não é receita) e as mesmas UTMs. **DESLIGADO por padrão.** Serve para medir "gerou Pix e não pagou"; não otimize campanha por ele.
- **Acesso entregue**: ignorado por padrão. Com `SEND_ACCESS_DELIVERED=true` envia o evento custom `AccessDelivered` (`event_id` = `access-<id>`). **DESLIGADO por padrão.** Só faz sentido se a entrega (ou outro webhook) avisar o receptor com um nome de evento contendo `access.delivered`/`acesso entregue`, ou se você acrescentar `?evento=access.delivered` na URL: o momento em que o ClickMax dispara esse aviso **[NC]**, confirme com **Enviar teste** e uma compra de teste.
- Variáveis novas: `CONTENT_NAME` (padrão "Mini Mentoria de Estruturação Zion") e `CONTENT_ID` (padrão `mm47`).
- Os dois eventos opcionais usam `event_id` diferente do `Purchase`, então não se deduplicam entre si nem inflam compras.

## Rodar os testes (sem rede, sem token)
```bash
cd zion-sales-engine/09-tracking/capi-webhook
node --test tests/*.test.js     # Node 18+; sem npm install
```

## Configurar o ClickMax (caminho recomendado: webhook de entrega com payload personalizado)
As variáveis desse webhook estão documentadas (docs.clickmax.io, "Quais dados posso enviar no payload do webhook de entrega?"). Valores em dinheiro vêm em centavos. [E]

1. ClickMax > **Produtos** > abra o produto > a **oferta** > **entrega** do tipo **webhook** (mesma tela das entregas de arquivo, link e área de membros). [E: caminho citado na doc; nome exato do botão para adicionar: [NC], procure "webhook" na lista de tipos de entrega]
2. **URL do Webhook**: `https://SEU-ENDERECO/webhook` (precisa ser https público). **Método HTTP**: POST.
3. **Adicionar autenticação personalizada?** > cabeçalho `cm-token` com o segredo que você gerou (o mesmo valor de `WEBHOOK_SECRET`).
4. **Selecione os eventos para disparo**: marque o evento de **transação paga** (e o de reembolso, se existir na lista). Quais eventos a lista oferece: [NC], envie print.
5. Marque **Personalizar payload deste evento** e cole:
```json
{
  "id": "{{id}}",
  "event": "{{event}}",
  "datetime": "{{datetime}}",
  "offerId": "{{offerId}}",
  "buyerName": "{{buyerName}}",
  "buyerEmail": "{{buyerEmail}}",
  "buyerPhone": "{{buyerPhone}}",
  "transaction": {
    "amount": "{{transaction.amount}}",
    "status": "{{transaction.status}}",
    "currency": "{{transaction.currency}}",
    "paymentMethod": "{{transaction.paymentMethod}}",
    "isSubscriptionInvoice": "{{transaction.isSubscriptionInvoice}}"
  },
  "utm": {
    "source": "{{utm.source}}", "medium": "{{utm.medium}}", "campaign": "{{utm.campaign}}",
    "content": "{{utm.content}}", "term": "{{utm.term}}", "src": "{{utm.src}}", "sck": "{{utm.sck}}"
  }
}
```
6. **Enviar teste** > **Ver payload** (mostra o JSON enviado e a resposta do seu servidor). Com `META_TEST_EVENT_CODE` preenchido, o evento aparece só em Gerenciador de Eventos > Testar eventos.
7. `datetime` é a hora do evento no ClickMax. Se o payload não trouxer a hora do pagamento, o receptor usa a hora do recebimento (`EVENT_TIME_FALLBACK_NOW`).

Observações do ClickMax: o webhook de entrega dispara **uma vez por oferta do pedido** (principal e cada order bump); `id` é o da transação, então o `event_id` repete e a idempotência segura. A integração de saída (Integrações > Criar webhook de saída, gatilho `SALE_MADE`) também serve: use `ADAPTER=clickmax-out`, **uma integração por gatilho** com `?evento=SALE_MADE` / `?evento=REFUND_MADE` na URL (o corpo não traz o nome do gatilho), e confira os nomes dos campos no botão de teste (ajuste com `FIELD_MAP_JSON`) [NC].

## Ticto (alternativa, só se for necessária)
O ClickMax já recebe os webhooks da Ticto. Para apontar a Ticto direto ao receptor: Ticto > **Tictools > Webhooks** > **+ Adicionar**, versão **2.0**, formato **JSON**, e a URL do receptor [E: caminho citado na doc do ClickMax]. Os campos do corpo da Ticto não foram lidos em documentação oficial: `ADAPTER=ticto` traz caminhos candidatos [NC]. **Confirme com um webhook de teste e ajuste `FIELD_MAP_JSON`.** O token que a Ticto exibe vai em `WEBHOOK_SECRET` + `WEBHOOK_SECRET_BODY_PATH` ou o header que ela usar [NC].

## Guia de implantação (baixo custo)
Nada abaixo foi executado. Preços e limites mudam: confira a página de preços do provedor antes [NC].
| Opção | Quando serve | Cuidados |
|---|---|---|
| Função serverless (Vercel, Netlify, Cloudflare com compatibilidade Node) usando `api/webhook.js` | Volume baixo (poucas vendas por dia); em geral cabe na faixa gratuita | Memória não persiste entre execuções: use `DEDUPE_STORE` em armazenamento persistente do provedor (KV) ou aceite que a idempotência dependa do `event_id` no Meta. Veja abaixo |
| Google Cloud Run (container com `node server.js`) | Cobrança por uso, com cota gratuita mensal | Disco efêmero: mesmo cuidado de idempotência |
| VPS pequeno ou serviço de container com disco persistente | Idempotência em arquivo (`DEDUPE_STORE=/dados/ids.jsonl`) funciona | Mantenha o sistema atualizado, firewall e HTTPS (proxy reverso) |

Passos genéricos:
1. Crie o projeto na hospedagem e publique **só esta pasta** (`capi-webhook/`). Ela não tem dependências.
2. Cadastre as variáveis do `.env.example` **no painel da hospedagem** (cofre de segredos). Bruno cola o token lá. **Nunca** no chat, no Git ou em print.
3. Primeiro com `META_TEST_EVENT_CODE` preenchido (eventos só na aba Testar eventos, não contam).
4. `GET https://SEU-ENDERECO/health` deve devolver `{"ok":true}`.
5. Enviar teste do ClickMax; ler os logs da hospedagem (`purchase_enviado` com `test_mode: true`).
6. Compra de teste real com reembolso (roteiro D do tutorial). Só então limpar `META_TEST_EVENT_CODE`.
7. **Desligar o Purchase nativo do ClickMax** (Comprou: navegador e servidor) para não contar em dobro. Os nomes de evento dos dois lados têm de bater, mas o `event_id` do navegador do ClickMax é gerado por ele e **não é igual** ao id da transação: sem desligar um dos lados, a Meta conta duas compras. Reverter = religar os dois interruptores.

### Idempotência em serverless
Em hospedagem sem disco, a memória some entre execuções. Duas defesas: (a) o ClickMax só repete o envio quando recebe erro ou quando alguém reenvia à mão; (b) `event_id` fixo no Meta. Para garantia forte, troque `src/store.js` por um KV (a interface é só `get(key)` e `set(key, status)`).

## Checklist de segurança
- [ ] `WEBHOOK_SECRET` com 32 caracteres aleatórios ou mais; diferente de qualquer outra senha; trocado se vazar.
- [ ] Endereço só `https`. Nenhum endpoint de leitura de dados (só `POST /webhook` e `GET /health`).
- [ ] `META_ACCESS_TOKEN` só no cofre da hospedagem. Token de sistema do Gerenciador de Negócios com a permissão mínima para o dataset. Trocar o token se aparecer em log ou print.
- [ ] Logs sem dados pessoais (já garantido pelo código e por teste); não ligar log de corpo bruto na hospedagem.
- [ ] `DEDUPE_STORE` guarda só `event_id` e status (sem e-mail, telefone ou nome).
- [ ] Limite de corpo (`MAX_BODY_BYTES`, 256 KB) e comparação de segredo em tempo constante.
- [ ] LGPD: o e-mail/telefone só sai da hospedagem **já com hash**, direto para a Meta. Atualizar a política de privacidade e a base legal conforme a orientação jurídica de Zion [NC, não é parecer jurídico].
- [ ] Revisar o repositório antes de cada commit: sem `.env`, token, payload real.

## Limites conhecidos
- Nomes de campos de `clickmax-out` e `ticto` são candidatos [NC]; o caminho `clickmax-delivery` usa só variáveis documentadas.
- Pixel do navegador e este receptor não se deduplicam entre si (ids diferentes). Use um só lado para Purchase.
- `META_GRAPH_VERSION` padrão `v21.0`: confirme a versão vigente na documentação da Meta [NC, o site developers.facebook.com estava bloqueado nesta sessão].
- Sem fbc/fbp, a atribuição depende de e-mail/telefone com hash (o Meta atribui por correspondência). Nunca há atribuição a anúncio sem dado.

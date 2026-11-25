# Recuperação das compras reais sem UTM (Meta sem Purchase atribuído)

Escrito em 25/11/2026 por DATA. **Nada foi enviado.** Reenviar evento ao Meta é escrita em produção do pixel: exige "aprovado" de Bruno, e quem roda é Bruno, com o token dele em variável de ambiente.
Legenda: [E] evidência · [H] hipótese · [NC] não confirmado.

## 1. O que está em jogo
- As compras reais recentes (Pix, de uma oferta antiga; a quantidade e os valores ficam no ClickMax, fora do repositório) vieram sem UTM e o Meta não registrou compra atribuída para elas (janela 7d clique + 1d visualização, leitura do Windsor) [E, auditoria H].
- O Meta só aceita evento com **até 7 dias** de `event_time`. O limite de cada compra é a hora do pagamento + 7 dias. **Prazo prático: enviar com pelo menos 1 dia de margem antes de pagamento + 7 dias.** Bruno calcula a data de cada compra no ClickMax; o limite é duro [E].
- Isso não conserta o passado dos anúncios: o objetivo é (a) a conta de anúncios aprender que houve compra e (b) a conciliação deixar de mostrar "100% de diferença" sem explicação.

## 2. Passo 0 (antes de reenviar): o Meta realmente não tem essas compras?
O Windsor mostra só o que o Meta **atribuiu a anúncios**. Um Purchase sem atribuição existe no Gerenciador de Eventos e não aparece lá [E+H]. Se o Purchase nativo do ClickMax já chegou, reenviar duplica.
1. Gerenciador de Eventos do Meta > pixel `903918118859018` > **Visão geral** > evento **Purchase**, intervalo da data da primeira compra real até hoje. Há Purchase? De que origem (Navegador/Servidor)? [passo B3 do tutorial]
2. ClickMax > Tráfego > Pixel e trackeamento > pixel > **Histórico de envio**, linhas das datas das compras reais com evento Purchase: **Enviado**, **Falhou** ou **Não enviado** (e o motivo) [passo A5 do tutorial].
3. **Se já houver Purchase dessas compras, com o valor da venda, no Meta: PARE.** Não reenvie. Registre e use a conciliação.

## 3. Opções honestas
| Opção | O que é | Prós | Contras |
|---|---|---|---|
| **1. Reenvio por CAPI com `event_id` próprio** (script `reenviar_compras.py`) | `Purchase`, `value=97.00`, `BRL`, `event_time` = hora real do pagamento, `action_source=website`, `user_data` com e-mail/telefone em SHA-256 | Rápido, auditável, idempotente; o Meta tenta casar a conta que clicou | Sem `fbc`/`fbp` a correspondência fica só por e-mail/telefone; sem garantia de atribuição |
| **2. Upload manual de conversões (arquivo CSV) no Gerenciador de Eventos** | O Meta tem importação de eventos offline por arquivo [NC: nome atual do menu e se continua disponível; procure "Carregar eventos" ou "Importar" em Fontes de dados] | Sem token, tudo no painel | Menu pode ter mudado; mesmos limites de correspondência |
| **3. Não reenviar; registrar como "venda sem atribuição"** | Entra na conciliação com a explicação "sem UTM, sem fbc/fbp, origem desconhecida" | Zero risco de duplicar ou de atribuição indevida | A conta de anúncios continua sem esses sinais |

Recomendação: passo 0 → se o Meta não tem, opção 1 em **modo teste primeiro** → depois real. Opção 3 vale para qualquer compra que não passe nas regras do script.

## 4. O que é possível sem `fbc`/`fbp`
- O Meta atribui por **correspondência**: e-mail e telefone com hash comparados com as contas que viram/clicaram em anúncios na janela. Funciona quando o e-mail/telefone da compra é o mesmo da conta Meta [H]; muitas vezes não é.
- `fbc` (clique) e `fbp` (navegador) não foram guardados pelo ClickMax nessas compras (`clickIds` vazio e página-mãe sem pixel) [E]. Não há como reconstruí-los: **não invente**.
- Não preencha UTM, campanha, conjunto ou anúncio sem dado. Uma das compras teve, na primeira sessão, UTM de campanha de formulário, mas a **venda** não guardou UTM [E]. O script só leva UTM que estiver no CSV, e o CSV só deve ter o que a venda gravou. **Nunca atribua a anúncio por dedução.**
- Resultado possível: o Meta atribui a um anúncio, a nenhum, ou conta como compra sem atribuição. Qualquer um desses é aceitável e precisa ser registrado como é.

## 5. Como preparar o CSV (Bruno, fora do repositório)
1. Crie a pasta fora do repositório (exemplo: `~/zion-privado/recuperacao/`) e copie `compras.csv.example` para `compras.csv`.
2. Para cada compra, preencha: `event_id` = **ID da transação no ClickMax** (o mesmo id aparece em Vendas; não use outro, para uma futura conferência), `paid_at` = hora do pagamento em ISO 8601 UTC (exemplo fictício: `2026-11-23T10:05:00Z`; a hora está na ficha do contato e em Vendas), `value_brl` = o valor da venda, ex.: `97.00` no exemplo (reais com ponto; **não** use 9700 nem 0,97), `email`, `phone`, `fullname` (da ficha da compra). Deixe `fbc`, `fbp` e UTMs **vazios** se a venda não os tem.
3. Nunca coloque esse CSV no Git, no chat ou em print.

## 6. Rodar (sem enviar → teste → real)
```bash
cd zion-sales-engine/09-tracking/recuperacao
python3 -I reenviar_compras.py --csv ~/zion-privado/recuperacao/compras.csv            # dry-run: mostra o que iria, hashes truncados
```
Esperado: cada linha `OK value=97.00 BRL idade=...h`, e `DRY-RUN: 2 pronta(s), 0 bloqueada(s)`. Linhas com mais de 7 dias saem `BLOQUEADA`.

Envio de teste (não conta como compra): no Gerenciador de Eventos > **Testar eventos** copie o código de teste (`TEST...`) e rode com ele:
```bash
export META_PIXEL_ID=903918118859018
export META_ACCESS_TOKEN=...          # cole só no seu terminal; nunca no chat
export META_TEST_EVENT_CODE=TEST...
python3 -I reenviar_compras.py --csv ~/zion-privado/recuperacao/compras.csv --send
```
Confira na aba Testar eventos: **Purchase, Servidor, value 97,00, BRL, `event_id` = id da transação**. Depois, sem `META_TEST_EVENT_CODE` (`unset META_TEST_EVENT_CODE`), rode de novo com `--send`. O arquivo `compras.csv.enviados` (ao lado do CSV, só ids) impede reenvio em dobro.
Confirmação final: Visão geral > Purchase na data real da compra e, em até 24 a 48 h, Gerenciador de Anúncios.

## 7. Critérios e riscos
- Aceite: um evento `Purchase` por compra, com o valor real da venda em BRL na data real da compra no Gerenciador de Eventos; nenhum duplicado; nenhum UTM inventado.
- Risco de duplicidade: se o ClickMax enviar o Purchase depois (reenvio do histórico dele): ele só reenvia até 7 dias e com o id dele; confira o Histórico de envio. Se houver dois, o Meta mostra em Diagnóstico e a conciliação explica.
- Risco legal: e-mail/telefone saem com hash; a base legal e a política de privacidade precisam cobrir o uso para mensuração [NC, orientação jurídica de Zion].
- Reversão: um Purchase enviado não é apagado pelo script. Por isso o teste vem antes.

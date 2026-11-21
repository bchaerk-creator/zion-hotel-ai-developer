# Relatório de rastreamento · Produto 01 (21/11/2026)

**Resumo honesto:** as regras foram especificadas e **testadas em um modelo de referência** (`comercial/rastreamento.js`, 11 testes). **Nada foi validado com tráfego, pixel, CAPI, Asaas ou webhook reais**: o vendedor está `pending`, as ofertas não foram aprovadas, não existe compra real. Uma tag isolada não prova pagamento; só vale o caminho completo: pagamento confirmado → identificação única → evento → acesso.

| Requisito | Estado | Como foi verificado / o que falta |
|---|---|---|
| UTMs e versão de preço | Especificado e testado (parseUtm) | Links dos anúncios com \`price_version=A47\|B67\`; falta conferir se o ClickMax grava as UTMs na venda (\`sales_get_utms\`) numa compra real. |
| Meta Pixel | **Não configurado** | O repositório cita um pixel \`903918118859018\` (contexto de reservas); **Bruno confirma qual pixel usar**. As páginas estão com \`pixelViewContent=false\`. |
| Conversions API | **Não validado** | Depende de token e do pixel. O modelo mostra o desenho: mesmo \`event_id\` no navegador e no servidor. |
| Eventos (visualização, início de checkout, compra) | Especificados | \`ViewContent\`, \`InitiateCheckout\`, \`Purchase\` (só pago). Eventos do portal (aula/ferramenta/dossiê) são contadores sem valores (teste e2e confirma que não vazam valores). |
| Identificação do produto e versão | Testado no modelo | \`custom_data: produto, versao_preco, offer_id\`; ofertas A e B com ids distintos. |
| Prevenção de duplicados | Testado | \`event_id = p01_terra_capital:purchase:<paymentId>\`; webhook repetido e segundo "confirmado" não geram 2º evento. |
| Validação de webhook | Testado (HMAC SHA-256, comparação em tempo constante) | Falta o segredo real do webhook do ClickMax/Asaas e o endpoint. |
| Identificação única do pagamento | Regra definida (paymentId) | Conferir o campo real no payload. |
| Acesso após confirmação | Testado no modelo; **no ClickMax não testado** | Entrega por turma está ligada às duas ofertas. Teste real exige compra de teste. |
| Reembolso | Testado no modelo (revoga acesso, status) | Conferir no ClickMax (\`transactions_refund\`/relatório) numa compra real. |
| Conciliação ClickMax × Asaas | Testada a rotina (acha só-em-um, status e valor diferentes) | Precisa de export real dos dois lados; sem acesso ao Asaas nesta sessão. |
| Progresso do aluno | Parcial | Portal guarda no aparelho; o ClickMax registra a conclusão das aulas da turma (\`member_users_get_progress\`). Unificar exige decisão de Bruno. |

## Passo a passo para validar (depois do "aprovado")
1. Bruno confirma pixel/conta e autoriza enviar as ofertas para aprovação.
2. Aprovada a oferta, compra de teste de R$ 47 (e de R$ 67) com Pix: conferir pagamento confirmado → acesso à turma → 1 evento Purchase com o \`event_id\` esperado → UTMs na venda.
3. Reenviar o webhook (ou repetir o evento) e confirmar que não dobra.
4. Reembolsar a compra de teste e confirmar revogação e registro.
5. Conciliar o extrato do dia entre ClickMax e Asaas com \`conciliar()\`.

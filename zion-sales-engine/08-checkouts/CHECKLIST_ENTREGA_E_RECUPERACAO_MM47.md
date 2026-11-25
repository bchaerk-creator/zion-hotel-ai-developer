# Checklist · compra real de teste, entrega dos acessos e recuperação (Mini Mentoria R$ 47)

Agente: ZION CONVERSION · 25/11/2026. Para Bruno executar (compra real exige "aprovado" específico dele). Sem dados pessoais neste arquivo: use a conta de teste de Bruno e **não** anote e-mail, CPF ou telefone aqui. Uma tag isolada não prova pagamento nem entrega: conferir o caminho inteiro.

## A. Antes da compra
1. Conferir no painel (celular) as páginas `/mini-mentoria-a`, `/mini-mentoria-b` e `/obrigado-mini-mentoria` (rascunhos) pelo "Visualizar".
2. Oferta `0c71eeba…`: `status approved`, preço R$ 47, entrega portal `3ef7a340…`/turma `087479a3…` [E em 25/11].
3. Decidir o valor do campo **Página de obrigado** (ver `CHECKOUT_E_AGRADECIMENTO_MM47.md`, seção 4) e se a página já está publicada.
4. Combinar com TRACKING/DATA: conciliação e envio ao Meta (`09-tracking/`); compra de teste deve ser reembolsada e **excluída** da métrica de teste A/B.

## B. Compra real de teste (Bruno)
Usar o link com UTM de teste: `…/mini-mentoria?utm_source=teste&utm_medium=manual&utm_campaign=mm47&utm_content=checklist` (e depois `-a`/`-b` quando publicadas). Pix primeiro; depois, se possível, cartão.
| # | Conferir | Como | Esperado | Resultado |
|---|---|---|---|---|
| 1 | Página abre no celular, preço e botão visíveis | olhar | CTA com "R$47"; sem rolagem lateral | |
| 2 | Checkout carrega (iframe) | olhar | produto, R$ 47, Pix e cartão; só campos necessários | |
| 3 | Pix gera e é pago | pagar | tela confirma | |
| 4 | Redireciona ao agradecimento | olhar a URL | `/obrigado-mini-mentoria` (ou a padrão do ClickMax se não ligado) | |
| 5 | **E-mail de acesso chega** | caixa de entrada e spam | e-mail do portal/ClickMax com como entrar [NC: chegada e prazo nunca provados nesta oferta] | |
| 6 | Turma | painel: `member_users_get_by_lead` ou lista da turma `087479a3…` | comprador na turma, acesso de 12 meses, `enabled` | |
| 7 | **Login** | abrir `zion-plataforma.clickmax.space` com o e-mail da compra | primeiro acesso sem criar senha, entra | |
| 8 | Conteúdo | abrir Comece aqui, Marco Zero, uma ficha, o Dossiê | carrega; sem reunião/Land Bank visíveis | |
| 9 | Venda registrada com UTM | painel Vendas ou `sales_get_utms` | `utmSource/Medium/Campaign/Content` iguais ao link [NC: gravação de UTM não provada] | |
| 10 | Evento no Meta | Gerenciador de Eventos | Purchase só após pago; value R$ 47, BRL [NC: CAPI/pixel ilegíveis por MCP] | |
| 11 | Reembolso | painel Vendas → reembolsar | reembolso concluído; acesso removido (se for compra de teste) | |
Se qualquer item falhar, parar e avisar o DIRECTOR; **não** prometer entrega em anúncio até o 5, 6 e 7 passarem.

## C. Diagnóstico se o acesso não chegar
Pagamento aprovado mas sem acesso: (1) venda está `paid`? (`transactions_get`); (2) comprador está na turma? (`member_users_get_by_lead`); (3) se está, reenviar o link de acesso (`member_users_send_access_link`, com "aprovado": é mensagem a cliente); (4) se não está, adicionar à turma (`member_users_add_to_classroom`, com "aprovado"); (5) conferir spam e o e-mail digitado. Atendimento: WhatsApp +55 48 6137-1061.

## D. Recuperação de Pix pendente / carrinho (coordenado com ZION FUNNEL; não duplicar)
Os fluxos são do FUNNEL e estão em **rascunho** (`05-funis/AUTOMACOES_MM47.md`): `MM47 · Pix não pago` (gatilho `pix.expired.v1`, espera 1 h, e-mail curto), `MM47 · Carrinho abandonado` (`cart.abandonment.v1`, espera 2 h) e `MM47 · Pós-compra`. CONVERSION **não cria** fluxo; só verifica:
1. **Antes de ligar** (com "aprovado" de Bruno): enviar teste real a um contato de teste e ver o e-mail (FUNNEL não rodou teste com contato real).
2. Pix gerado e não pago: conferir que o e-mail chega só **depois** da expiração, não menciona urgência falsa e traz o link da página **com a mesma versão (A ou B) vigente**; se o teste A/B estiver rodando, o link do e-mail deve apontar para a URL do teste (slug `teste-ab-…`) ou para a variante de controle, para não contaminar a medição [H].
3. Quem pagou depois do Pix expirado não pode receber o e-mail de recuperação (checar condição de compra aprovada no fluxo) [NC].
4. Meta/TRACKING: `Purchase` só em `purchase_approved`; Pix gerado ≠ compra (`09-tracking/recuperacao/`).
5. Indicador: Pix gerado → Pix pago, antes e depois de ligar a recuperação (DATA).

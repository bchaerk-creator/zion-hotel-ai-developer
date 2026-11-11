# Funil de R$ 97 com adesão ao clube · o que a pesquisa indica e o que foi aplicado (12/11/2026)

## O que as fontes convergem (números são de blogs de plataformas, não de estudos; usar como faixa, não como meta)
1. **Produto de entrada barato + ofertas no mesmo checkout.** Low ticket entre R$ 27 e R$ 97; order bump no checkout a 25–40% do preço principal, com aceite estimado entre 15% e 40%; upsell de um clique depois do pagamento, aceite 5–15%.
2. **Recuperação de abandono nas primeiras 24 h**, por WhatsApp e e-mail; Pix gerado e não pago é o maior vazamento no Brasil.
3. **Checkout sem atrito:** sem cadastro, sem custo surpresa, Pix e cartão, garantia visível.
4. **Sequência pós-compra** com próximo passo claro (aqui: alinhamento + sessão), conversão 5–10% para o próximo degrau.
5. **Medir junto:** custo por lead, conversão da página, ticket médio com bump, reembolso.

## Aplicado hoje (sem urgência falsa, sem bônus inventado)
- **Recuperação de Pix pendente:** fluxo `11e8b263` (rascunho): Pix gerado → 30 min → WhatsApp `zion_clube_pix_pendente` com o link do checkout.
- **Recuperação de checkout abandonado:** fluxo `c5092264` (rascunho): contato deixado no checkout → 1 h → WhatsApp `zion_clube_carrinho`.
- **Recuperação de lead de formulário sem compra:** fluxos `5a8e7d04` (terreno) e `de4a391a` (parceiro), 3 toques.
- **Landing:** junto ao botão, "Acesso liberado na hora… Próxima masterclass ao vivo: quinta-feira, 20h" (urgência real, é o evento semanal). Reembolso de 7 dias e Pix/cartão já estavam.
- **Pós-compra:** tag + tarefa + alinhamento + sessão (fluxo `575dd0b9`, Bruno ativa).

## Não aplicado ainda (depende do Bruno)
- **Order bump no checkout de R$ 97:** candidato "Ferramenta 05 · Orçamento da Cabana" (R$ 19, oferta incompleta) para quem tem terreno; "Checklist de Limpeza" ou "Kit de Mensagens" (R$ 19, aprovadas) para operadores. O checkout nativo do ClickMax configura o bump em Produtos → oferta → Order bump; pela API só em páginas de checkout do construtor.
- **Upsell pós-compra:** a sessão estratégica já é o próximo degrau (mentoria). Página de obrigado com o alinhamento cumpre o papel.
- **E-mail:** sequência paralela ao WhatsApp (sem créditos). A montar quando o remetente estiver configurado.
- **Remarketing no Meta:** público de quem visitou /clube e não comprou, 7 dias, com o vídeo. Precisa do público personalizado no Gerenciador.
- **Templates** pendentes de confirmação do texto e envio ao Meta; **créditos** de WhatsApp a comprar.

Fontes: Panda Video (low ticket funnel), Focus Digital (upsell 2025), winmassiveimpact (playbook 2026), HeroSpark (funil de vendas), Outsider School (checkout), Estúdio Site (low ticket R$ 27–97).

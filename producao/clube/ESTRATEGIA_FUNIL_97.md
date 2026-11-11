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

## 12/11 ~01h30 · "Vamos aplicar" (Bruno)
- 9 templates enviados ao Meta para aprovação (status pending): zion_clube_form_1/2/3, zion_parceiro_form_1/2/3, zion_clube_pix_pendente, zion_clube_carrinho, zion_clube_boas_vindas.
- Boas-vindas adicionado ao fluxo pós-compra `575dd0b9` (depois da tarefa).
- Fluxos a ativar quando os templates forem aprovados: pós-compra, Pix pendente, checkout abandonado, formulário terreno, formulário parceiro. Antes: comprar créditos de WhatsApp e adicionar no canvas do pós-compra o passo "Remover de outras automações".

## 12/11 ~01h45 · Downsell R$ 47 definido pelo Bruno
- Produto novo: **"Aprenda o passo a passo para trazer um sócio, investidor ou parceiro · Kit Inicial de Captação (R$ 47)"** · produto `8ff3f7b3-2c42-41aa-a58f-3bb5b3b2ad6a`, oferta `50fd0b0a-09d3-4ada-9608-30d288166902`, checkout `https://payments.clickmax.io/ylYvvUTnVq`. Pix e cartão à vista, reembolso 7 dias, ZIONACADEMY. Enviada para aprovação (incomplete reason vazio).
- Entrega por link: `docs/p/adbc67069af26ae0/kit-captacao-47/` (mesmos guia, planilhas e vídeo do kit; sem o bloco da sessão; com convite para o clube). Não inclui sessão estratégica nem Radar do Land Bank.
- Fluxo "Checkout abandonado" (`c5092264`): 1 h → lembrete do clube; +23 h → template `zion_clube_downsell_47` (enviado ao Meta) com botão para o checkout de R$ 47 e "Prefiro o clube".
- Decisões do Bruno: preço aparece na landing e no checkout, não no anúncio; sem botão de WhatsApp na landing; WhatsApp só na recuperação.

## 11/11 · Remarketing 180d + reativação da base por e-mail (pedido de Bruno)

### Remarketing no Meta (180 dias)
- O conector do Windsor.ai não cria públicos personalizados. Bruno cria no Gerenciador de Anúncios (Públicos → Criar público personalizado), todos com 180 dias:
  1. Site: visitantes do pixel 903918118859018 (todos, 180d) e visitantes de /clube, /parceiro, /land-members, /metodo, /raio-x.
  2. Vídeo: quem assistiu 25%+ dos vídeos das campanhas Zion Collection (filme, tours, clube v3, parceiro).
  3. Engajamento: página 576944608845537 + Instagram Zion (180d).
  4. Formulários de lead: abriu ou enviou os formulários Meta (Land Bank, Clube, Parceiro) — 90d é o máximo do Meta para esse tipo.
- Com os IDs dos públicos, criamos (pausado) um conjunto de remarketing em cada campanha nova (Clube e Parceiro), com os vídeos de 2 min, excluindo compradores (pixel Purchase 180d) e inscritos.
- Orçamento sugerido: R$ 15/dia por conjunto; só liga com "aprovado".

### Reativação da base do ClickMax por e-mail
- Base: 2761 contatos. Listas: Lote 1 base quente `90a53d73…` (258 e-mails válidos), Lote 2 restante `90379a6a…` (2400 válidos), total 2658.
- Bloqueio: nenhum remetente verificado (`email_sender_signatures_list` vazio) e nenhuma caixa de e-mail conectada. Sem isso o ClickMax não envia.
- Modelo salvo no ClickMax: "Clube · Reativação da base · E-mail 1 (clube + parceiro)" (fonte: `producao/clube/email/reativacao_clube.html`). Links com UTM `email/broadcast/reativacao-clube` e `reativacao-parceiro`.
- Plano de envio (rascunhos, Bruno aprova cada disparo): E-mail 1 Lote 1 → 48h → E-mail 1 Lote 2 (lotes de 300 a cada 30 min) → dia 4: E-mail 2 "Como funciona a parceria" (vídeo) → dia 7: E-mail 3 kit R$47 para quem abriu e não comprou.

## 11/11 · Isca "Diagnóstico gratuito" (aprovado) — ver `producao/clube/diagnostico/README.md`
Campanha 3 (Leads, formulário Meta Adesão Terreno) → classificação em 3 níveis → devolutiva por WhatsApp e e-mail → página de resultado → checkout R$ 97. Campanha `120250335430180016` e conjunto `120250335463470016` criados pausados; anúncios aguardam o ID do formulário.

# Funil canônico de venda direta · Mini Mentoria de Estruturação (R$ 47)

Agente: FUNNEL · Fase 03 · 25/11/2026. Marcação: **[E]** evidência lida agora, **[H]** hipótese, **[NC]** não confirmado.
Nada neste documento foi publicado ou ativado. O que foi criado em rascunho está em `AUTOMACOES_MM47.md`.

## 1. A sequência

Anúncio → Landing page → VSL → Demonstração → Oferta → Preço → Checkout → Compra aprovada → Entrega → CRM → Relacionamento.

Regras do funil (do Manual Mestre e do CLAUDE.md):
- **Sem formulário obrigatório antes da compra.** O comprador clica e paga. Qualquer ficha (por exemplo `/obrigado-plataforma`) vem **depois** do pagamento e é opcional.
- **Sem reunião obrigatória** e sem reunião prometida. A oferta diz "sem acompanhamento individual e sem reunião" [E, descrição da oferta `0c71eeba`].
- **Separado da captação high ticket.** Ver seção 3.
- Promessa padrão: "Aprenda o passo a passo para...". Sem promessa de reservas, renda, investimento ou parceria.
- O botão que leva ao pagamento mostra o preço.

Dados fixos [E]: oferta `0c71eeba-2654-432c-9701-0a31e6113a08`, produto `cbbb5fb1-550f-4a8d-b269-5122c17b7780`, checkout `yhyiqUB9OF`, página `be23f04a-fa2e-4fc6-91ee-51a9aeb915d1` (`/mini-mentoria`, publicada), portal `3ef7a340`, turma `087479a3`. Oferta `approved`, gateway Ticto, sem erro de sincronização, Pix e cartão 1x, reembolso 7 dias, acesso 12 meses.

## 2. Etapa por etapa

| # | Etapa | Objetivo | Sistema / ferramenta | Estado atual | O que falta | Dono | Métrica |
|---|---|---|---|---|---|---|---|
| 1 | Anúncio | Levar quem tem terreno e quer entender o passo a passo até a página, sem prometer resultado | Meta Ads (Windsor, conta a confirmar com Bruno), criativos 1080×1350, UTM `utm_source=meta&utm_medium=paid&utm_campaign=<produto>&utm_content=<criativo>` | [NC] estado das campanhas da Mini Mentoria não lido nesta sessão (regra: só pausadas, teto R$ 0). As 2 vendas reais de 24/11 (oferta de R$ 97) vieram sem UTM [E, fatos-chave] | Confirmar que todo anúncio aponta para `/mini-mentoria` e leva UTM; nada de anúncio apontando para as páginas antigas (ver `CONSOLIDACAO_OFERTA_97.md`) | TRAFFIC (execução), CREATIVE (arte e texto) | CTR, custo por clique, custo por visita à página, custo por venda (comparar com R$ 44,51 líquido do Pix) |
| 2 | Landing page | Explicar a dor e o caminho em poucas telas, celular primeiro | ClickMax, página `/mini-mentoria` | [E] publicada em 25/11 (03:51Z); `pixelViewContent` desligado | Ligar ViewContent (decisão do TRACKING); conferir que a página não repete frases de contato, reunião ou investimento (as páginas antigas repetem; esta, segundo a auditoria, não) | CONVERSION | Visitas únicas, rolagem, clique no botão |
| 3 | VSL | Vídeo curto que faz o ECROI (espelhar a dor, quebrar a crença, reconhecer o problema, mostrar o método, mostrar a aplicação) | ClickMax tem integração Vturb (ferramentas `vturb_*`) | [NC] não encontrei VSL ligada à `/mini-mentoria`; status do Vturb não verificado | Decidir se haverá VSL. Sem ela o funil continua válido (a página faz o papel). Roteiro sem promessa e sem depoimento inventado | CREATIVE (roteiro), CONVERSION (inserção) | Tempo assistido, % que chega ao botão |
| 4 | Demonstração | Mostrar a plataforma por dentro, com telas reais | Telas reais em `docs/zion-collection/club/telas/` (prints do portal) | [NC] não conferi se a página já mostra as telas; as telas existem no repositório [E, CLAUDE.md] | Inserir 3 a 5 telas reais (módulos, ficha "Faça agora", Dossiê) na página, sem texto por cima de foto | CONVERSION, CREATIVE | Rolagem até o bloco de demonstração |
| 5 | Oferta | Dizer exatamente o que entra e o que não entra | ClickMax, oferta `0c71eeba` (descrição) e bloco de entregáveis da página | [E] descrição honesta: aulas gravadas, fichas, e-books, 2 planilhas em branco, kit de modelos, kit de prompts, Dossiê; sem reunião; parcerias e investimentos são possibilidades sujeitas à análise | Garantir que o bloco da página repita o mesmo texto da oferta. O nome "Mentoria" ainda pode sugerir acompanhamento (pendência de decisão de Bruno) | CONVERSION | Cliques no botão por visita |
| 6 | Preço | Mostrar R$ 47, pagamento único, Pix ou cartão à vista, reembolso 7 dias | Página e oferta | [E] oferta em R$ 47. Os botões da página têm o texto "QUERO TRANSFORMAR MEU TERRENO" (mapa de gatilhos da página), **sem o preço**. Isso foge da regra "CTA que leva ao pagamento mostra o preço" | Trocar o texto dos 3 botões para "QUERO ACESSAR A MINI MENTORIA POR R$47". Precisa de "aprovado" (é edição de página publicada) | CONVERSION | Taxa de clique no botão antes e depois |
| 7 | Checkout | Pagar sem atrito, sem formulário extra | Checkout nativo do ClickMax embutido (iframe `payments.clickmax.io`, bloqueado neste ambiente), gateway Ticto | [E] Pix ativo, cartão 1x, boleto desligado, recorrência nenhuma. `initiate_checkout` dispara no carregamento do iframe (inflaciona a métrica) [E, fatos-chave]. Checkout em si nunca foi visto daqui | Teste de compra real feito por Bruno (compra de teste e reembolso). Rastreamento do evento certo (TRACKING) | CONVERSION (fluxo), TRACKING (eventos) | Visita → checkout → Pix gerado → pago; taxa de Pix gerado que paga |
| 8 | Compra aprovada | Reconhecer o pagamento e acionar tudo o que vem depois | Gatilho `checkout.transaction.paid.v1` com escopo `offerId` | [E] hoje **não existe automação ativa** para a oferta `0c71eeba` (lista de fluxos por nome vazia; os demais fluxos de pós-compra estão presos a outras ofertas). Rascunhos criados agora | Aprovação de Bruno para ligar os 3 fluxos; teste com um contato de teste | FUNNEL (desenho), CONVERSION (teste) | Compras aprovadas; fluxos disparados = compras |
| 9 | Entrega | Dar o acesso na hora e dizer como entrar | Entrega `internal_membership`: portal `zion-plataforma`, turma `087479a3` (9 módulos, 70 aulas e materiais). Primeiro acesso sem senha habilitado no portal [E] | [E] entrega ligada à oferta. [NC] caminho completo "pagamento confirmado até acesso" **não testado de ponta a ponta** (a oferta tem 0 vendas) | Compra de teste de Bruno e conferência do acesso (a "tag isolada não comprova entrega", CLAUDE.md). E-mail de boas-vindas (rascunho pronto) | CONVERSION | % de compradores que entram em até 24 h; pedidos de ajuda de acesso |
| 10 | CRM | Registrar quem comprou e acompanhar o aluno, sem fingir que é lead de reunião | Tag `MM47 \| COMPROU` (criada); quadro **Alunos Zion** `5f7000a7`, etapa "1 · Comprou · liberar acesso" | [E] tag criada e card previsto no rascunho. Quadro Alunos Zion está vazio e sem automação [E] | Aprovação para ligar. Recomendação e justificativa em `AUTOMACOES_MM47.md` (por que não usar o quadro "Inscritos · Plataforma") | FUNNEL, DATA | Alunos por etapa (comprou, acesso, primeiro acesso, estudando, concluiu, travado, reembolso) |
| 11 | Relacionamento | Fazer o aluno usar o material, concluir o Dossiê e, só depois, ver oferta complementar real | E-mails em rascunho; sequência em `RELACIONAMENTO_BASE.md`; oferta complementar em `BUMP_UPSELL_DOWNSELL.md` | [E] só o e-mail de boas-vindas existe (rascunho). Nenhuma sequência ativa | Aprovação para a sequência; depoimento real só com consentimento; webinário depende do módulo desligado | FUNNEL, CONVERSION | Primeiro acesso, % do Dossiê concluído, satisfação, pedidos de reembolso, depoimentos autorizados |

## 3. Fronteira com a captação high ticket (só descrição, nada alterado)

Venda direta (este funil): anúncio → página → pagamento de R$ 47 → entrega. Não pede ficha, não marca reunião, não promete parceria.

Captação high ticket (Land Bank, Club Zion Collection, parceiro): tem funil próprio, pipelines próprios ("Funil Zion · Novo lead → Reunião → Venda", "Club Zion Collection", "Parceria Zion"), reunião com closer e agentes de atendimento (Zaya e Bela). **Nada disso é tocado.**

Regras para não misturar:
1. Quem compra a Mini Mentoria **não entra** nos pipelines de reunião. Entra no quadro Alunos Zion.
2. Quem quiser conversar sobre parceria ou investimento procura a captação por outro caminho; a Mini Mentoria não promete isso.
3. Nenhuma página de venda direta leva a formulário de agendamento como etapa obrigatória.

**Ponto de mistura encontrado [E]:** a página `/parceiro-zion` está ligada à oferta antiga de R$ 47 (`668391e7`), e o nome sugere captação de parceiro. É um cruzamento entre venda direta e high ticket. Tratar em `CONSOLIDACAO_OFERTA_97.md` (só com aprovação).

## 4. Prioridade do que falta (menor passo que corrige)

1. Teste de compra de ponta a ponta (Bruno). Sem isso, "entrega funciona" é [NC].
2. Aprovar e ligar os 3 fluxos de rascunho (depois do teste).
3. Texto do botão com o preço.
4. Ligar ViewContent e acertar `initiate_checkout` (TRACKING).
5. Consolidar as ofertas e redirecionar o tráfego (plano em `CONSOLIDACAO_OFERTA_97.md`).
6. Demonstração com telas reais e decisão sobre VSL.

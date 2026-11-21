# Auditoria somente leitura · Zion Expansão Brasil (21/11/2026)

## Insumos recebidos
- `PROMPT_MASTER.md`, `QUIZZES.md`, `COPY_ANUNCIOS.md`, `README.md` (cópias em `insumos/`).
- **Faltam no pacote:** `criativos/` (vídeo `00_VIDEO_ORIGINAL.mp4` e 6 JPG 1080×1350), `marca/`, `referencias/`. O ZIP recebido (`Zion_Expansao_Brasil_PROMPTS.zip`) só tem os 4 textos.
- O repositório tem `docs/assets/video/expansao-zion.mp4` (89 s, 848×480, "enviado por Bruno" em 19/11): é um filme da Zion Glamping Collection (logo, cabana, paisagens); nos 6 quadros vistos não aparece o Bruno e não há transcrição. **Não está confirmado que seja o vídeo original.** Não foi usado.
- Divergência: `QUIZZES.md` fala em "dez entregáveis"; o `PROMPT_MASTER.md` lista nove. Usei os nove.

## ClickMax (workspace Bruno's Workspace)
- **Não existe projeto "Zion Collection".** Projetos: Infoprodutos Zion, Zion Reservas, Projeto de Bruno. "Zion Collection" é um portal de membros e o nome da conta Meta. Usei **Infoprodutos Zion** (regra do CLAUDE.md).
- Vendedor: `sellerStatus` **pending**, `bankAccountStatus` approved, gateway **ticto** (o checkout do ClickMax é nativo; Asaas não faz parte deste caminho).
- Já existe oferta de R$ 270 (Club Zion Collection + Land Bank, `c627c32e…`, status incomplete) e o formulário "Diagnóstico gratuito Zion". Não foram tocados.
- Agenda atual "Equipe Zion" (45 min, **gratuita, link público**): ~18 reuniões marcadas pelo funil gratuito, usada pela Zaya. Conflita com "sem reuniões grátis" e **não foi alterada**.
- Zaya (`db450d9a…`, ativa, v57): oferece reunião gratuita e envia o link público da agenda; diz "nunca falar de preço". Precisa de nova persona para a Sessão de R$ 270. **Mudança só com "aprovado".**
- Triggers de fluxo disponíveis: `checkout.transaction.paid.v1` (compra aprovada), `pix.expired.v1`, `card.refused.v1`, `cart.abandonment.v1`, `checkout.refund.requested.v1`, `checkout.chargeback.requested.v1`, `crm.scheduling.booked/cancelled/no_show/completed`.
- A agenda do ClickMax só funciona por link público; não há ferramenta (MCP) para criar agenda, nem verificação de pagamento nativa na reserva.

## Meta · conta Zion Collection 2 (`1271873041294684`, confirmada)
13 campanhas nos últimos 90 dias. **Só uma está ativa:**
- `120250113109820016` · [LAND BANK][LEADS][FORM → DIAGNÓSTICO GRÁTIS → REUNIÃO] [03/11] · ACTIVE · conflita com a nova estratégia (reunião grátis).

Já pausadas (nada a fazer, só preservar): 120248742070580016, 120248809006140016, 120249218934280016, 120250173411950016 (form → checkout R$ 270), 120250257012540016, 120250330194890016, 120250332392690016, 120250343378940016, 120250421516840016, 120250438713460016, 120250439943320016, 120250455991130016.
A campanha do Produto 01 (`120250503993280016`) não aparece no relatório de 90 dias (sem gasto); conferir no Gerenciador.
**Nenhuma campanha foi alterada.** A pausa da 120250113109820016 fica pronta para executar com "aprovado".

## Atualização 21/11 (Bruno)
Não haverá Raio-X gratuito: só compra direta. Quiz apagado; botão "Fazer meu Raio-X gratuito" removido da landing. O `QUIZZES.md` em `insumos/` ficou só como registro do pacote recebido (a seção do formulário Meta e o formulário privado pós-compra continuam úteis).

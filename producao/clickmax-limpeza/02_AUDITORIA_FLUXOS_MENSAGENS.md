# Auditoria de fluxos, disparos e modelos de WhatsApp · ClickMax Zion

Data: 13/11/2026 · Workspace `e87e8ba9-37cf-4c54-9a97-3e4e1b01827a` · **Somente leitura: nada foi criado, alterado, ativado, enviado ou arquivado.** Sem dados pessoais (só contagens).

## Resumo (10 linhas)

1. **Achado mais grave:** o fluxo que dá a primeira mensagem ao lead do formulário Meta (`Club · Lead do formulário Meta → Zaya abre a conversa`) teve **74 de 101 execuções falhas por "insufficient credits" (HTTP 402)**; só 25 terminaram e 2 estão agendadas. Na prática, a maioria dos leads do Land Bank/Parceiro não recebeu o `zion_destino_turistico`. Saldo atual de créditos: **não verificado**.
2. Há 93 fluxos: **45 ativos, 44 rascunho, 4 fechados**. Só 31 têm execução real; **62 têm 0 execuções** (41 rascunhos, 18 ativos, 3 fechados).
3. Os 3 fluxos "Diagnóstico · Devolutiva" (Em preparação / Potencial com ajustes / Potencial alto) estão em **rascunho**; as tags DIAG já estão em 10 leads (1 + 5 + 4) que nunca recebem a devolutiva, embora os 6 modelos `zion_diag_*` estejam aprovados.
4. **Colisão:** a mesma tag `FUNIL A | REUNIÃO GRÁTIS` dispara dois fluxos ao mesmo tempo (`[CRM] Entrada 2` e `[CRM] Passagem 2`), e `crm.scheduling.booked.v1` dispara 3 fluxos ativos (2 movem card, 1 avisa o Bruno) e 4 rascunhos esperando.
5. **Lembretes de reunião e mensagem de no-show estão em rascunho** (grupo "★ EM USO AGORA" engana: o nome diz "em uso", o modo diz rascunho), apesar de 6 modelos aprovados (`lembrete_reuniao_*`, `confirmacao_reuniao`, `noshow_reuniao`, `reagendar_reuniao`).
6. Fluxos órfãos/vazios: `Entrada de Lead — Meta → CRM → Funil` está **ativo só com gatilho, sem nenhuma ação**; vários rascunhos sem gatilho (Aquecimento ×2, Menu de parceiros, Cadência Noite Mágica, Página do Dossiê).
7. Disparos: 25 (7 WhatsApp enviados, 9 WhatsApp em rascunho, 9 áudios de voz de 1 destinatário cada, 0 de e-mail). Terra parada, Conheça a Zion e os 2 Trailers (rascunhos) miram os mesmos 77 leads do Meta; o fluxo manual `Land Members · Disparo inscrição` já mandou o `zion_destino_turistico` para 172 contatos sem falhas de crédito.
8. Modelos: 123 (96 aprovados, 25 rascunho, 1 rejeitado, 1 falhou). **40 levam mídia no cabeçalho** (22 imagem, 18 vídeo). Há muitas versões do mesmo texto (`_v2`, `_foto`, `_arte`, `_form`).
9. Proposta: uma jornada única com **11 modelos** (seção 4.4).
10. Limpeza em 4 fases, sempre **arquivar, não excluir**; a primeira fase arquiva só o que tem 0 execuções e 0 contatos (seção 6). Antes de tudo: **recarregar créditos** e **decidir** se a jornada real é a da Zaya (pipeline Mentoria) ou a do Parceria.

Não verificado (limite desta leitura): saldo de créditos; conteúdo da Zaya (agente de IA, fora dos fluxos); `stage_automations_list` e `managed_flows_*` (não consultados, ver seção 5); nome das listas de público de cada disparo (só ids); qual modelo cada fluxo usa, exceto onde o objetivo do fluxo o cita; texto completo de cada mensagem.

---

## 1. Inventário dos 93 fluxos

Legenda: "exec." = execuções reais; "contatos" = contatos distintos (a API conta também execuções de teste). "o que faz" vem da estrutura do fluxo (WhatsApp, e-mail, tag, card, aviso). Onde diz "cria/move card" foi lido em `flows_structure_get` nos 14 fluxos conferidos (`assignOpportunity`) e inferido nos demais pelo nome e pelo objetivo. Contagem por modo: 45 ativos, 44 rascunho, 4 fechados.

### 1. CRM Entrada e Passagem (pipelines Parceria e Mentoria) (31 fluxos)

| id | modo | nome | gatilho | o que faz | exec. / contatos |
|---|---|---|---|---|---|
| a5154cbe | active | 3b · Liguei, não atendeu → áudio + template agendar (10 min) | opportunity.entered.column | 1x WhatsApp, aplica tag | 7 / 7 |
| e7e2dbd9 | active | Entrada de Lead — Meta → CRM → Funil | lead.captured | so gatilho (sem acao) | 0 / 0 |
| 4c7cff2c | closed | TAG AUTOMÁTICA · BASE / BASE ANTIGA (FUNIL SDR) | opportunity.entered.column | aplica tag | 0 / 0 |
| c7cf60de | active | TAG AUTOMÁTICA · BASE ANTIGA / BASE (FUNIL SDR) v2 | opportunity.entered.column | aplica tag | 0 / 0 |
| 0fad1d14 | active | TAG AUTOMÁTICA · PREENCHEU FORMULÁRIO (META) | opportunity.entered.column | aplica tag | 16 / 16 |
| 55fd665c | active | [CRM] Entrada — 1 · Novo lead (formulário) | wa.message.received | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 28 / 21 |
| 92aac82a | active | [CRM] Entrada — 1 · Novo lead (formulário) | tag.lead.apply | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 101 / 101 |
| a473a722 | active | [CRM] Entrada — 1 · Preencheu a ficha de adesão | tag.lead.apply | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 3 / 3 |
| 1d6a3b2e | active | [CRM] Entrada — 2 · Zaya qualificando | tag.lead.apply | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 7 / 7 |
| dc620101 | active | [CRM] Entrada — Diagnóstico concluído | lead.captured | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 0 / 0 |
| 8a151ef7 | closed | [CRM] Entrada — Novo Lead | flow_webhook.received | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 0 / 0 |
| 5ecc76c8 | active | [CRM] Entrada — PREENCHEU FORMULÁRIO | flow_webhook.received | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 16 / 16 |
| ab29d9bf | active | [CRM] Entrada — Pagamento pendente | tag.lead.apply | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 0 / 0 |
| fbaa7d96 | active | [CRM] Entrada — Pagou o Kit R$ 270 · falta agendar | tag.lead.apply | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 3 / 3 |
| fbbb47e0 | active | [CRM] Entrada — Sessão agendada | tag.lead.apply | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 0 / 0 |
| 5a2f2910 | active | [CRM] Passagem — 2 · Pendentes de agendamento (acumulados) | scheduling.cancelled | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 0 / 0 |
| 90aeb59c | active | [CRM] Passagem — 2 · Pendentes de agendamento (acumulados) | scheduling.no_show | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 0 / 0 |
| e3408d29 | active | [CRM] Passagem — 2 · Zaya qualificando | tag.lead.apply | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 7 / 7 |
| 4cf03b0c | active | [CRM] Passagem — 3 · Pagou · acesso liberado | tag.lead.apply | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 0 / 0 |
| a376eb54 | active | [CRM] Passagem — 3 · Reunião agendada | scheduling.confirmed | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 0 / 0 |
| dfe7fb8e | active | [CRM] Passagem — 3 · Reunião agendada | scheduling.booked | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 3 / 3 |
| 78434648 | active | [CRM] Passagem — 4 · Diagnóstico inicial · Boas-vindas | scheduling.completed | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 0 / 0 |
| a92fc133 | active | [CRM] Passagem — 5 · Entrou para o clube | tag.lead.apply | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 0 / 0 |
| 8cd9c31f | active | [CRM] Passagem — 5 · Reunião agendada | tag.lead.apply | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 2 / 2 |
| e5a1cf3e | active | [CRM] Passagem — 6 · Agora não / Sem retorno | tag.lead.apply | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 0 / 0 |
| b811f4e3 | active | [CRM] Passagem — 8 · Comprou (Mentoria · Clube · Land Bank) | asaas.payment.confirmed | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 0 / 0 |
| b1711a88 | active | [CRM] Passagem — Agora não · nutrir | tag.lead.apply | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 1 / 1 |
| 43c54992 | active | [CRM] Passagem — Pagou o Kit R$ 270 · falta agendar | scheduling.no_show | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 1 / 1 |
| bc4347bb | active | [CRM] Passagem — Reunião agendada | scheduling.booked | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 19 / 11 |
| 03fb727f | active | [CRM] Passagem — Reunião feita | scheduling.completed | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 0 / 0 |
| 80aa9c22 | active | [CRM] Tarefa: registrar resultado da reunião — Reunião feita | opportunity.entered.column | cria/move card (assignOpportunity nos 14 verificados; demais inferido) | 3 / 3 |

### 2. Land Bank / Parceria / Club (leads Meta, Zaya, diagnóstico, reunião) (27 fluxos)

| id | modo | nome | gatilho | o que faz | exec. / contatos |
|---|---|---|---|---|---|
| 957bf574 | active | Alerta · Reunião Land Bank agendada | scheduling.booked | avisa equipe | 21 / 11 |
| 7b96dc6b | draft | Ativação · envio · Sem capital | tag.lead.apply | 1x WhatsApp | 2 / 1 |
| a41cea5c | draft | Ativação · reunião agendada → etapa 5 | scheduling.booked | cria/move card | 0 / 0 |
| 0d1dab25 | draft | Bubble · Orçamento no WhatsApp → preço → aula | wa.message.received | 2x WhatsApp, aplica tag, debug, avisa equipe | 0 / 0 |
| a90448b6 | active | Club · Lead do formulário Meta → Zaya abre a conversa (menu) + lembrete em 48h | tag.lead.apply | aplica tag (2x), 2x WhatsApp | 101 / 101 |
| c5092264 | draft | Clube R$ 97 · Checkout abandonado → lembrete no WhatsApp | cart.abandonment | 2x WhatsApp | 0 / 0 |
| 11e8b263 | draft | Clube R$ 97 · Pix gerado e não pago → lembrete no WhatsApp | checkout.pix.generated | 1x WhatsApp | 0 / 0 |
| 575dd0b9 | draft | Clube R$ 97 · Pós-compra (tag + aviso à equipe) | checkout.transaction.paid | 1x WhatsApp, aplica tag, createLeadTask | 0 / 0 |
| 5a8e7d04 | draft | Clube · Lead do formulário (terreno) sem compra → 3 toques no WhatsApp | tag.lead.apply | 3x WhatsApp | 0 / 0 |
| 794fee82 | draft | Diagnóstico · Devolutiva · Em preparação | tag.lead.apply | 2x e-mail+WhatsApp | 0 / 0 |
| b77f2f33 | draft | Diagnóstico · Devolutiva · Potencial alto | tag.lead.apply | 2x e-mail+WhatsApp | 0 / 0 |
| d39e1d37 | draft | Diagnóstico · Devolutiva · Potencial com ajustes | tag.lead.apply | 2x e-mail+WhatsApp | 0 / 0 |
| 28b8e1bf | active | Land Members · Disparo inscrição (terra parada) | manual | 1x WhatsApp, aplica tag | 175 / 173 |
| 0c37f32b | draft | Leads novos · chamou no WhatsApp → Zaya | wa.message.received | cria/move card | 0 / 0 |
| 86c40978 | draft | Leads novos · resposta R$ 5 mil+ → card + WhatsApp reserva | tag.lead.apply | aplica tag, 1x WhatsApp, cria/move card | 0 / 0 |
| 212684a2 | draft | Leads novos · resposta menos de R$ 5 mil → card + WhatsApp reserva | tag.lead.apply | aplica tag, 1x WhatsApp, cria/move card | 0 / 0 |
| e1d1e7d3 | draft | Leads novos · reunião agendada → etapa 4 | scheduling.booked | cria/move card | 0 / 0 |
| 16be7020 | draft | Lembretes da reunião · Zaya (lead) | scheduling.booked, scheduling.rescheduled | 2x WhatsApp | 0 / 0 |
| 4710faed | draft | No-show · reunião → Zaya remarca | scheduling.no_show | 1x WhatsApp | 0 / 0 |
| ab84f8ac | active | Objeção · Não agora → sequência de reativação (72h) | tag.lead.apply | 3x WhatsApp | 1 / 1 |
| 785b91d1 | active | Objeção · Quero saber mais → Zion por dentro (foto) + reativação | wa.template.button | 3x WhatsApp | 0 / 0 |
| d7ebafa3 | closed | Oferta apresentada → cartão visual dos 4 entregáveis | tag.lead.apply | 1x WhatsApp | 0 / 0 |
| 08a59f14 | active | Pagamento inscrição R$ 97 confirmado → agenda da sessão + aviso | tag.lead.apply | avisa equipe, 1x WhatsApp | 0 / 0 |
| de4a391a | draft | Parceiro · Lead do formulário sem compra → 3 toques no WhatsApp | tag.lead.apply | 3x WhatsApp | 0 / 0 |
| a2c00030 | draft | Partnership · Avaliação recebida | lead.captured | so gatilho (sem acao) | 0 / 0 |
| 728a1a3d | draft | Sessão concluída → entregáveis (mapa + e-book Vol. 1) | scheduling.completed | 1x WhatsApp | 0 / 0 |
| fb690d5e | draft | Teste A · Lead Meta → convite Zaya | tag.lead.apply | 1x WhatsApp | 0 / 0 |

### 3. Funil Terreno (WhatsApp Zion Collection, botões, consultoria, dossiê) (16 fluxos)

| id | modo | nome | gatilho | o que faz | exec. / contatos |
|---|---|---|---|---|---|
| 9f26cb61 | draft | Consultoria R$ 490 · Comprou → aviso + WhatsApp com agenda | tag.lead.apply | avisa equipe, 1x WhatsApp | 0 / 0 |
| e8307aee | draft | Curso · Dossiê completo (troféu) → aviso ao Bruno | tag.lead.apply | avisa equipe | 0 / 0 |
| 14a72edf | draft | Curso · Página do Dossiê recebida → campos e etiquetas do aluno | - | so gatilho (sem acao) | 0 / 0 |
| 9cfb8d6b | active | Funil Land Members · Comprar uma Bubble → Glamping Store | wa.template.button | 1x WhatsApp, aplica tag | 9 / 9 |
| b28ba703 | active | Funil Land Members · Fazer parte do clube → página do clube | wa.template.button | 1x WhatsApp, aplica tag | 25 / 24 |
| c5658d80 | active | Funil Land Members · Inscrever meu projeto → link | wa.template.button | aplica tag, 1x WhatsApp | 2 / 1 |
| 549f7f99 | draft | Funil Terreno · 0 Disparo (menu) com lembrete D1 e última chamada D4 | manual | 3x WhatsApp, debug (2x), aplica tag | 0 / 0 |
| d79b5457 | draft | Funil Terreno · 0b Disparo (bolha) com lembrete D1 e última chamada D4 | manual | 3x WhatsApp, debug (2x), aplica tag | 0 / 0 |
| 23b7831b | closed | Funil Terreno · 1 Clicou Jornada R$ 270 → link de pagamento | wa.template.button | aplica tag (2x), 1x WhatsApp | 8 / 7 |
| 50e49eb1 | draft | Funil Terreno · 2 Clicou Consultoria prévia → link R$ 490 | wa.template.button | aplica tag (2x), avisa equipe, 1x WhatsApp | 0 / 0 |
| e1adb52d | draft | Funil Terreno · 3 Mentorias e Premium → formulário e reunião | wa.template.button | aplica tag (2x), avisa equipe, 1x WhatsApp | 0 / 0 |
| ce384dbd | active | Funil Terreno · 4 Falar com a equipe → aviso | wa.template.button | 1x WhatsApp, avisa equipe, aplica tag (2x) | 5 / 5 |
| 56545fb9 | active | Funil Terreno · 5 Não quero receber / Agora não | wa.template.button | aplica tag (2x), 1x WhatsApp | 0 / 0 |
| f57f8ea1 | active | Funil Terreno · 6 Agora não → só etiqueta | wa.template.button | aplica tag (2x) | 0 / 0 |
| f524a310 | draft | Funil Terreno · Boas-vindas e menu de gatilhos (clique para WhatsApp) | whatsapp.window.opened | aplica tag | 0 / 0 |
| 5eca2173 | draft | Funil Terreno · Menu de parceiros (1 a 4) → tag e aviso | - | so gatilho (sem acao) | 0 / 0 |

### 4. Mentoria / Método Zion / Jornada (5 fluxos)

| id | modo | nome | gatilho | o que faz | exec. / contatos |
|---|---|---|---|---|---|
| 2c56ddfb | active | Método Zion · Comprou Jornada → WhatsApp de acesso | tag.lead.apply | 1x WhatsApp | 1 / 1 |
| 5cf1deeb | active | Método Zion · Comprou Trilha 1 ou Pacote → aviso + boas-vindas | tag.lead.apply | avisa equipe | 2 / 2 |
| 5c193886 | active | Método Zion · Novo aluno (tag CLUB / MEMBRO) → boas-vindas | tag.lead.apply | 1x WhatsApp, avisa equipe, cria/move card | 1 / 1 |
| 69c42dbf | draft | Método Zion · Pagamento Asaas (nativo) → aluno | asaas.payment.confirmed, asaas.payment.received | avisa equipe, aplica tag, addContactToList | 0 / 0 |
| cf5baba4 | draft | Método Zion · Pós-diagnóstico (resultado + Zaya) | lead.captured | aplica tag, 2x WhatsApp | 0 / 0 |

### 5. Bubble / Noite Mágica / Hospedagem (7 fluxos)

| id | modo | nome | gatilho | o que faz | exec. / contatos |
|---|---|---|---|---|---|
| 89bf530a | draft | Ebook Glamping Vol. 2 — Entrega e Nutrição | - | 1x e-mail | 0 / 0 |
| 4728bdd8 | draft | HOSP · Cadência Reativação · Cotou e não reservou | tag.lead.apply | aplica tag, 3x WhatsApp | 0 / 0 |
| 72313f86 | draft | HOSP · Noite Mágica · Email onda 1 · Florianópolis | manual | 1x e-mail | 0 / 0 |
| d6dff126 | draft | HOSP · Noite Mágica · Email onda 1 · Urubici | manual | 1x e-mail | 0 / 0 |
| e057932c | draft | Lançamento · Bubble → Raio-X (reativação da base) | manual | aplica tag, 1x WhatsApp | 2 / 1 |
| 9cf7fd35 | draft | NM · Cadência Noite Mágica · Entrega do cupom | - | so gatilho (sem acao) | 0 / 0 |
| d2f8619a | active | NM · Caminho A · Lead capturado → tags + card Cupom revelado | lead.captured | aplica tag (4x), cria/move card | 2 / 1 |

### 6. Raio-X (4 fluxos)

| id | modo | nome | gatilho | o que faz | exec. / contatos |
|---|---|---|---|---|---|
| 0e08225f | draft | Raio-X · 1 Fez o Raio-X → oferta R$ 270 (e-mails D0/D1/D3/D7) | tag.lead.apply | 4x e-mail | 0 / 0 |
| 3b44273d | draft | Raio-X · 2 Pagou R$ 270 → liberar sessão | tag.lead.apply | avisa equipe | 0 / 0 |
| 0679fd95 | draft | Raio-X · 3 Sessão agendada → confirmação | scheduling.booked | avisa equipe, aplica tag | 0 / 0 |
| 09827a53 | draft | Raio-X · 5 Pós-sessão → registrar resultado | scheduling.completed | avisa equipe | 0 / 0 |

### 7. Outros / testes (3 fluxos)

| id | modo | nome | gatilho | o que faz | exec. / contatos |
|---|---|---|---|---|---|
| 476b84af | draft | Aquecimento  | - | so gatilho (sem acao) | 0 / 0 |
| dc0860f7 | draft | Aquecimento do Lead via WhatsApp | - | 2x e-mail | 0 / 0 |
| b246e870 | draft | TESTE · Nome Zion Collection (48 6137-1061) → Bruno | manual | 1x WhatsApp | 1 / 1 |
Fluxos fechados (4): `Funil Terreno · 1 Clicou Jornada R$ 270` (8 exec., o único fechado com uso), `Oferta apresentada → cartão visual dos 4 entregáveis`, `TAG AUTOMÁTICA · BASE / BASE ANTIGA` (v1, substituído pelo v2) e `[CRM] Entrada — Novo Lead` (webhook antigo).

---

## 2. O caminho real hoje de um lead novo do formulário Meta (Land Bank / Parceiro)

### 2.1 Em ordem, o que dispara

| # | Quando | Fluxo | O que acontece | Situação real |
|---|---|---|---|---|
| 1 | A integração Tráfego → Formulários aplica a tag `META \| FORM LAND BANK` (101 leads) | `Club · Lead do formulário Meta → Zaya abre a conversa (menu) + lembrete em 48h` (ativo) | Aplica `FUNIL TERRENO \| DISPARO ENVIADO`, manda o modelo `zion_destino_turistico` (imagem + 5 botões), espera resposta; se responder, aplica tag; se não responder em 48h, manda `zion_terreno_lembrete` (lembrete citado no objetivo do fluxo) | **74 de 101 falharam (HTTP 402, créditos)**. Só 25 terminaram, 2 aguardando. Os demais erros são da Meta (#131026, #131049, #130472), 1 cada |
| 1b | Mesma tag, no mesmo instante | `[CRM] Entrada — 1 · Novo lead (formulário)` (ativo, 101 exec.) | Cria o card do lead no pipeline (assignOpportunity) | Funciona |
| 2 | Lead toca num botão do menu | `Funil Land Members · Fazer parte do clube` (25 exec.), `Comprar uma Bubble` (9), `Inscrever meu projeto` (2) (ativos) | Manda o link/texto da resposta (ex.: página do clube) e pergunta se tem terreno, projeto ou hospedagem | Funciona (25/25 terminaram, no exemplo lido) |
| 2b | Lead toca em "Falar com a equipe" | `Funil Terreno · 4 Falar com a equipe → aviso` (5 exec.) | Confirma e avisa a equipe | Funciona |
| 3 | Lead escreve qualquer mensagem no número Zion Collection | `[CRM] Entrada — 1 · Novo lead (formulário)` **segundo** (gatilho `mensagem recebida`, 28 exec.) | Cria/move card, para qualquer pessoa que escreva, não só para lead novo | Funciona, mas é um segundo fluxo com o mesmo nome |
| 4 | Zaya (agente de IA) conversa e qualifica | fora dos fluxos | Qualifica, aplica tags como `FUNIL A \| REUNIÃO GRÁTIS`, `OBJEÇÃO \| NÃO AGORA` | **Não verificado** (o agente não foi lido) |
| 5 | Tag `FUNIL A \| REUNIÃO GRÁTIS` (16 leads) | `[CRM] Entrada — 2 · Zaya qualificando` **e** `[CRM] Passagem — 2 · Zaya qualificando` (ativos, 7 exec. cada) | Os dois movem o card (um por pipeline) | **Colisão**: mesma tag, 2 fluxos, 2 cards (Mentoria e Parceria) |
| 6 | Lead agenda a reunião (`scheduling.booked`) | 3 ativos: `Alerta · Reunião Land Bank agendada` (21 exec., avisa o Bruno por notificação), `[CRM] Passagem — Reunião agendada` (19), `[CRM] Passagem — 3 · Reunião agendada` (3) | Dois movem o card, um avisa o Bruno | **Colisão** (3 ativos). Mais 4 rascunhos do mesmo gatilho: `Lembretes da reunião · Zaya (lead)`, `Ativação · reunião agendada`, `Leads novos · reunião agendada`, `Raio-X · 3 Sessão agendada` |
| 7 | 1 h / 15 min antes | `Lembretes da reunião · Zaya (lead)` | **Rascunho, 0 exec.**: ninguém recebe lembrete por fluxo | **Lacuna** (ver 2.3). Pode haver lembrete nativo da agenda ClickMax: **não verificado** |
| 8 | No-show | `[CRM] Passagem — 2 · Pendentes` (no_show/cancelled, ativos, só movem card) e `No-show · reunião → Zaya remarca` (**rascunho**) | O card volta para pendentes, nenhuma mensagem sai | **Lacuna** |
| 9 | Reunião concluída | `[CRM] Passagem — 4 · Diagnóstico inicial · Boas-vindas` e `Reunião feita` (ativos, 0 exec.) + `Sessão concluída → entregáveis` (**fechado/rascunho**) | Só movem card; nenhum envia os entregáveis | **Lacuna** |
| 10 | Pagamento | `Pagamento inscrição R$ 97 confirmado → agenda da sessão + aviso` (ativo, 0 exec.), `[CRM] Passagem — 8 · Comprou` (asaas, 0 exec.) | Manda `zion_inscricao_ok` + aviso | Nunca disparou (nenhuma compra pelo caminho Asaas desde que existe) |

Observações sobre o caminho do lead:
- **Tempo:** a primeira mensagem sai no mesmo minuto (tag aplicada, sem espera), por isso o erro de créditos derruba o contato logo na entrada.
- **Dois "funis em uso":** o pipeline Mentoria (grupo "★ EM USO AGORA", 104 cards) e o pipeline Parceria (110 cards) recebem os mesmos eventos. O Mentoria tem o Funil A/B e a ligação do Bruno; o Parceria acabou de ser criado (11/11).
- `3b · Liguei, não atendeu → áudio + template agendar (10 min)` (7 exec.): em 2 de 7 a mensagem **virou rascunho** porque havia atendente ativo na conversa (comportamento esperado, não é erro).
- `TAG AUTOMÁTICA · PREENCHEU FORMULÁRIO (META)` (16 exec.) e `[CRM] Entrada — PREENCHEU FORMULÁRIO` (webhook, 16 exec.) pertencem ao **FUNIL SDR antigo** ("z · Antigos") e ainda rodam.

### 2.2 Colisões

| Gatilho | Fluxos ativos que disparam juntos | Risco |
|---|---|---|
| `tag FUNIL A \| REUNIÃO GRÁTIS` | `[CRM] Entrada — 2 · Zaya qualificando`, `[CRM] Passagem — 2 · Zaya qualificando` | Dois cards por lead em pipelines diferentes |
| `crm.scheduling.booked.v1` | `Alerta`, `Passagem — Reunião agendada`, `Passagem — 3 · Reunião agendada` + 4 rascunhos | Se algum rascunho for ativado, soma lembrete, etapa e tag em paralelo |
| `crm.tag.lead.apply.v1` | 33 dos 93 fluxos usam esse evento; só a tag diferencia | Uma tag nova mal escolhida dispara dois fluxos sem aviso |
| `hermes...message.received.v1` | Dois ativos (`[CRM] Entrada — 1 · Novo lead` e o rascunho `Leads novos · chamou no WhatsApp → Zaya`) | Se o rascunho for ativado, move o card duas vezes |
| `crm.scheduling.no_show.v1` | `Passagem — 2 · Pendentes`, `Passagem — Pagou o Kit R$ 270 · falta agendar` (ativos) e `No-show → Zaya remarca` (rascunho) | O ativo "Pagou o Kit" roda para qualquer no-show, não só quem pagou |
| Nomes iguais | `[CRM] Entrada — 1 · Novo lead (formulário)` ×2; `[CRM] Passagem — 2 · Pendentes de agendamento (acumulados)` ×2; `Passagem — 3 · Reunião agendada` ×2 | Confunde quem edita |

### 2.3 Lacunas

1. **Sem crédito** (acima): o primeiro toque falha para ~73% dos leads do Meta.
2. **Devolutiva do diagnóstico em rascunho** (`Em preparação` tag DIAG, `Potencial com ajustes`, `Potencial alto`): 10 leads com a tag e nenhum envio, apesar de 6 modelos `zion_diag_*` aprovados (3 + 3 versões `_v2`).
3. **Lembretes e no-show em rascunho**, com modelos aprovados e parados.
4. **Entregáveis após a sessão** (`zion_entregaveis` aprovado): fluxo fechado.
5. **Pós-compra do Clube R$ 97 e recuperação de carrinho/Pix**: 3 fluxos em rascunho, com modelos `zion_clube_*` aprovados (carrinho, pix, boas-vindas).
6. **Sequência de 3 toques para quem preencheu o formulário e não comprou** (Parceiro, Clube/terreno): rascunho (2 fluxos), com os modelos `zion_parceiro_form_*` e `zion_clube_form_*` aprovados.
7. **Entrada de Lead — Meta → CRM → Funil** ativa, mas **vazia**: vira uma falsa segurança.
8. Pagamento por Asaas nativo (`Método Zion · Pagamento Asaas`) em rascunho: a compra do Método só aciona pelo site.

### 2.4 Fluxos órfãos (sem gatilho útil ou sem nenhuma ação)

- Vazio: `Entrada de Lead — Meta → CRM → Funil` (ativo).
- Rascunho sem gatilho: `Aquecimento ` (0 passos úteis), `Aquecimento do Lead via WhatsApp`, `Ebook Glamping Vol. 2 — Entrega e Nutrição`, `Curso · Página do Dossiê recebida`, `Funil Terreno · Menu de parceiros (1 a 4)`, `NM · Cadência Noite Mágica · Entrega do cupom`.
- Ativos que nunca rodaram (0 exec.): `[CRM] Entrada — Diagnóstico concluído`, `Pagamento pendente`, `Sessão agendada`, `Passagem — 3 · Pagou`, `4 · Diagnóstico inicial`, `5 · Entrou para o clube`, `6 · Agora não / Sem retorno`, `8 · Comprou`, `Reunião feita`, `Passagem — 3 · Reunião agendada (confirmed)`, `Funil Terreno · 5 e 6 (Não quero receber / Agora não)`, `Pagamento inscrição R$ 97`, `Objeção · Quero saber mais`, `TAG AUTOMÁTICA v2`. São estágios do pipeline, não necessariamente erro; mas ninguém os viu rodar.
- Duplicados por função: `Funil Terreno · 5` e `6` (ambos "Agora não").
- Segunda geração do mesmo caminho: `Clube · Lead do formulário (terreno)` e `Parceiro · Lead do formulário` (rascunhos) repetem o que o `Club · Lead do formulário Meta` (ativo) já faz.

---

## 3. Disparos (broadcasts): 25

Fonte: `broadcasts_list` (todos); detalhes de dois por `broadcasts_get`. O ClickMax só traz `sourceListIds`; **nome das listas: não verificado**.

### 3.1 WhatsApp enviados (7)

| Data | Disparo | Público | Entregues | Abertos | Cliques | Falhas |
|---|---|---|---|---|---|---|
| 10/11 | Ativação 10/11 · Por onde começar + sem dor (`zion_ativ_comecar`, vídeo) | 34 | 30 | 19 | 1 | 4 |
| 10/11 | Ativação 10/11 · Quer parceiro | 21 | 18 | 9 | 0 | 3 |
| 10/11 | Ativação 10/11 · Quer acompanhamento | 8 | 6 | 2 | 0 | 2 |
| 10/11 | Ativação 10/11 · Sem capital | 14 | 14 | 10 | 0 | 0 |
| 05/11 | Reunião hoje 05/11 · 14h-17h · leads 03-04/11 | 12 | 12 | 10 | 4 | 0 |
| 04/11 | Funil B · primeira mensagem com foto | 2 | 2 | 2 | 1 | 0 |
| 04/11 | Funil A · convite reunião · leads 03-04/11 | 8 | 8 | 6 | 2 | 0 |

Total das 4 ativações de 10/11: 77 enviados, 68 entregues, 40 abertos, 1 clique, 9 falhas. **O mesmo dia teve disparos e a falha de créditos nos fluxos; as falhas de entrega (4+3+2) são da Meta/telefone, não de crédito.**

### 3.2 WhatsApp em rascunho (9), nunca enviados

| Disparo | Público (previsto) | Modelo (onde lido) |
|---|---|---|
| Piloto triagem Zaya · 9 leads quentes 09/11 (foto) | 9 | `zion_triagem_zaya` (imagem), não conferido |
| Dor · Por onde começar · leads do form Meta | 9 | não conferido |
| Dor · Medo de errar · leads do form Meta | 12 | não conferido |
| Dor · Quero um parceiro · leads do form Meta | 31 | não conferido |
| Dor · Falta capital · leads do form Meta | 22 | não conferido |
| Dor · Terra parada · leads do form Meta | 77 | `zion_dor_terra_parada` (vídeo), lote 20 a cada 10 min |
| Conheça a Zion · leads do form Meta | 77 | `zion_conheca_a_zion` (não conferido) |
| Trailer Club Zion Collection · leads do form Meta | 77 | `zion_club_ecossistema`? (não conferido) |
| Trailer Trilha de Desenvolvimento · leads do form Meta | 77 | `zion_trailer_trilha`? (não conferido) |

Sobreposição: as 4 "Ativação 10/11" já cobriram as 4 dores (comecar, parceiro, acompanhamento, sem capital) para essa base; os rascunhos `Dor · ...` repetem as mesmas dores com outros modelos (`zion_dor_*`) e se somam a 3 broadcasts de 77 leads. Se os 5 + 3 forem disparados, o mesmo lead recebe até 4 mensagens de marketing em sequência.

### 3.3 Áudios gravados (voz), 9

Todos de 1 destinatário (ligação do Bruno, "3b · Liguei e não atendeu"): 7 em 10/11, 1 em 09/11, 1 em 05/11. Abertura 1/1 em 8 dos 9. Não são campanhas, são mensagens avulsas gravadas como disparo; podem ficar como estão.

---

## 4. Modelos de WhatsApp (123)

Fonte: `gupshup_templates_list` (123 de 123). Status: **96 aprovados, 25 rascunho, 1 rejeitado, 1 falhou, 0 pendentes**. Categoria: 98 marketing e 25 utilidade. Mídia no cabeçalho: **40** (22 imagem, 18 vídeo; 32 aprovados, 8 rascunho). "Qualidade" voltou `UNKNOWN` em todos.

### 4.1 Por finalidade (nome do modelo, status; A = aprovado, R = rascunho)

| Finalidade | Modelos |
|---|---|
| **Primeiro toque do formulário Meta, por dor (vídeo)** | `zion_ativ_comecar` A, `zion_ativ_parceiro` A, `zion_ativ_acompanhamento` A, `zion_ativ_sem_capital` A (os 4 vídeo, usados nas Ativações de 10/11); `zion_dor_capital`, `zion_dor_comecar`, `zion_dor_medo`, `zion_dor_parceiro`, `zion_dor_terra_parada` (A, vídeo); `zion_dor_*_form` ×5 (R, vídeo, cópia dos anteriores) |
| **Primeiro toque (Land / destino turístico)** | `zion_destino_turistico` A (imagem, em uso), `zion_land_inscricao` A, `zion_land_inscricao_arte` A, `zion_land_inscricao_foto` A, `zion_land_caminhos` A, `zion_land_bolha` A, `zion_terreno_caminhos` A, `zion_terreno_bolha` A, `zion_land_parceiro` A, `zion_terreno_parceiro` A |
| **Lembretes/última chamada do funil** | `zion_terreno_lembrete` A, `zion_terreno_ultima` A, `zion_land_lembrete_arte` A, `zion_land_lembrete_foto` A, `zion_land_ultima_foto` A, `zion_land_lembrete` R, `zion_land_ultima` R, `zion_opera_lembrete` A |
| **Qualificação do formulário (rascunho)** | `zion_qualif_capital/comecar/medo/parceiro` R, `zion_reuniao_qualificado` R |
| **Sequência 3 toques após formulário (Clube e Parceiro)** | `zion_clube_form_1/2/3` A, `zion_parceiro_form_1/2/3` A |
| **Agendar a reunião** | `zion_agende_reuniao` A (imagem), `zion_convite_reuniao` A, `zion_reuniao_hoje` A, `agendamento_diagnostico` A, `agendamento_diag_foto` R (imagem), `zion_sessao_bolha` A (imagem), `zion_convite_projeto` A, `zion_pos_audio_agendar` A, `reativ_operador_p1` R (imagem) |
| **Confirmação e lembretes da reunião** | `confirmacao_reuniao` A, `lembrete_reuniao_dia` A, `lembrete_reuniao_1h` A, `lembrete_reuniao_15min` A, `zion_lembrete_bubble` A (imagem), `zion_reuniao_15min` A (imagem), `zion_lembrete_reuniao` R |
| **No-show e reagendamento** | `noshow_reuniao` A, `zion_faltou_reuniao` A (imagem), `reagendar_reuniao` A, `zion_reagendar` R |
| **Pós-reunião e entregáveis** | `zion_pos_reuniao` A, `zion_entregaveis` A, `zion_followup_duvida` A |
| **Devolutiva do diagnóstico** | `zion_diag_preparacao`, `zion_diag_ajustes`, `zion_diag_alto` e as 3 versões `_v2` (todos A, texto); `club_resultado_pronto`, `club_lembrete_24h`, `club_convite_diagnostico` A |
| **Inscrição / Land Bank / pagamento** | `zion_inscricao_passos` A (imagem), `zion_o_que_recebe` A (imagem), `zion_inscricao_ok` A, `zion_inscricao_paga` A, `zion_sessao_agendar` A, `zion_lembrete_inscricao` R, `zion_acesso_jornada` A |
| **Clube R$ 97 / Kit** | `zion_clube_boas_vindas` A, `zion_clube_carrinho` A, `zion_clube_pix_pendente` A, `zion_clube_downsell_47` A, `zion_clube_kit_captacao` A (vídeo), `zion_club_ecossistema` A (vídeo), `zion_trailer_trilha` A (vídeo), `zion_conheca_a_zion` A (vídeo), `zion_trilha1_inscricao` R (imagem) |
| **Objeção "não agora"** | `zion_nao_agora` A, `zion_deu_uma_olhada` A, `zion_ultima_destino` A (imagem), `zion_por_dentro` A (imagem) |
| **Bubble / Raio-X / Noite Mágica** | `zion_bubble_raiox` A (imagem), `zion_bubble_raiox_arte` A (imagem), `store_bubble_condicao` A (imagem), `bubble_aula_quinta` A, `zion_raiox_resultado` A, `nm_condicao_entrega/relax_24h/romantico_72h/ultima_chamada` R |
| **Triagem Zaya / lead novo** | `zion_triagem` A, `zion_triagem_zaya` A (imagem), `zion_produto_terreno` R |
| **Aulas e masterclass** | `zion_aula_hoje` A, `club_aula_marco_zero` A, `zion_terreno_aula` A, `zion_masterclass_aviso` **falhou** (variável no início/fim), `masterclass_link_dia` **rejeitado** (categoria incorreta) |
| **Método / Hub / pós-compra** | `metodo_boas_vindas` A, `metodo_zion_boas_vindas` R, `hub_boas_vindas` A, `club_boas_vindas` A, `zion_consultoria_paga` R |
| **Prospecção fria (corretor/operador)** | `zion_corretor` A, `zion_opera_parceria` A, `zion_terreno_capital` A |

### 4.2 Com foto ou vídeo no cabeçalho (40)

- **Vídeo (18; 13 aprovados + 5 rascunho):** `zion_ativ_acompanhamento`, `zion_ativ_comecar`, `zion_ativ_parceiro`, `zion_ativ_sem_capital`, `zion_club_ecossistema`, `zion_clube_kit_captacao`, `zion_conheca_a_zion`, `zion_dor_capital`, `zion_dor_comecar`, `zion_dor_medo`, `zion_dor_parceiro`, `zion_dor_terra_parada`, `zion_trailer_trilha` (aprovados); `zion_dor_capital_form`, `zion_dor_comecar_form`, `zion_dor_medo_form`, `zion_dor_parceiro_form`, `zion_dor_parada_form` (rascunho).
- **Imagem (22; 19 aprovados + 3 rascunho):** `store_bubble_condicao`, `zion_agende_reuniao`, `zion_bubble_raiox`, `zion_bubble_raiox_arte`, `zion_destino_turistico`, `zion_faltou_reuniao`, `zion_inscricao_passos`, `zion_land_inscricao_arte`, `zion_land_inscricao_foto`, `zion_land_lembrete_arte`, `zion_land_lembrete_foto`, `zion_land_ultima_foto`, `zion_lembrete_bubble`, `zion_o_que_recebe`, `zion_por_dentro`, `zion_reuniao_15min`, `zion_sessao_bolha`, `zion_triagem_zaya`, `zion_ultima_destino` (aprovados); `agendamento_diag_foto`, `reativ_operador_p1`, `zion_trilha1_inscricao` (rascunho).
- **Nenhum `zion_diag_*` leva mídia** (todos texto). Os `zion_ativ_*` aprovados são os 4 que levam vídeo, mas `zion_ativ_resp_agendar` e `zion_ativ_resp_nutrir` são texto.
- Dos modelos com "bolha" no nome: `zion_land_bolha` e `zion_terreno_bolha` são **texto**; os que mostram a Bubble com foto são `zion_bubble_raiox`, `zion_bubble_raiox_arte`, `store_bubble_condicao`, `zion_sessao_bolha`, `zion_lembrete_bubble`. A foto da cabeçalho do `reativ_operador_p1` usa a imagem `whatsapp-bubble.jpg` num texto para **operadores de hospedagem**, o que choca com a regra de não dar a entender que é só bubble/glamping (rascunho: ajustar antes de qualquer envio). A URL das mídias não foi conferida visualmente aqui.

### 4.3 Redundantes (candidatos a arquivar)

| Grupo | Mantém | Redundantes |
|---|---|---|
| Devolutiva do diagnóstico | `zion_diag_*_v2` (3, versão mais recente) | `zion_diag_preparacao/ajustes/alto` (3, mesma finalidade; qual a Meta aprovou como definitiva: **não verificado**) |
| Primeiro toque por dor | `zion_ativ_*` (4, já usados) | `zion_dor_*` (5 aprovados) e `zion_dor_*_form` (5 rascunhos), `zion_qualif_*` (4 rascunhos) |
| Lembrete/última do funil | `zion_terreno_lembrete`, `zion_terreno_ultima` | `zion_land_lembrete`(R), `zion_land_ultima`(R) e as versões `_arte`/`_foto` |
| Destino turístico/land | `zion_destino_turistico` | `zion_land_inscricao` + `_arte` + `_foto`, `zion_land_caminhos`, `zion_terreno_caminhos`, `zion_land_bolha`, `zion_terreno_bolha`, `zion_land_parceiro`, `zion_terreno_parceiro` |
| Bubble/raio-x | `zion_bubble_raiox_arte` | `zion_bubble_raiox` (mesma finalidade) |
| Lembretes da reunião | `lembrete_reuniao_dia/1h/15min` | `zion_lembrete_reuniao` (R), `zion_lembrete_bubble`, `zion_reuniao_15min` |
| No-show | `noshow_reuniao` + `reagendar_reuniao` | `zion_faltou_reuniao`, `zion_reagendar` (R) |
| Agendar reunião | `agendamento_diagnostico` | `zion_agende_reuniao`, `zion_convite_reuniao`, `zion_reuniao_hoje`, `agendamento_diag_foto` (R), `zion_sessao_bolha`, `zion_convite_projeto` |
| Boas-vindas do Método/Clube | `zion_clube_boas_vindas` | `club_boas_vindas`, `hub_boas_vindas`, `metodo_boas_vindas`, `metodo_zion_boas_vindas` (R) |
| Quebrados | nenhum | `zion_masterclass_aviso` (falhou), `masterclass_link_dia` (rejeitado) |

Cuidado: ao arquivar modelo, conferir antes se algum fluxo ou disparo em rascunho o usa (os modelos citados nos objetivos dos fluxos ativos são `zion_destino_turistico`, `zion_terreno_lembrete`, `zion_nao_agora`, `zion_deu_uma_olhada`, `zion_ultima_destino`, `zion_por_dentro`, `zion_inscricao_ok`, `zion_o_que_recebe` e `zion_acesso_jornada`: **não arquivar esses**).

### 4.4 Conjunto enxuto proposto (11 modelos) para uma única jornada

Jornada: lead do formulário Meta (Land Bank/Parceiro) → conversa → reunião de diagnóstico → devolutiva → entrada no Clube/Kit. Só há 1 modelo por função, todos já aprovados:

| # | Função | Modelo (aprovado) | Observação |
|---|---|---|---|
| 1 | Primeiro toque (menu) | `zion_destino_turistico` (imagem) | Já em uso. Tem foto de hospedagem: confirmar que não é só bubble |
| 2 | Primeiro toque por dor, se for segmentar | `zion_ativ_comecar` (vídeo) | Um por dor só se compensar; senão fica o 1 |
| 3 | Lembrete 48h | `zion_terreno_lembrete` | Já em uso |
| 4 | Convite para agendar | `agendamento_diagnostico` | Texto, utilidade da reunião |
| 5 | Confirmação da reunião | `confirmacao_reuniao` | Utilidade |
| 6 | Lembrete (dia, 1 h, 15 min) | `lembrete_reuniao_1h` (+ `_dia`, `_15min`, se quiser 3 toques) | Contados como 1 modelo de função |
| 7 | No-show + reagendar | `noshow_reuniao` | `reagendar_reuniao` só se mudar o horário |
| 8 | Devolutiva (3 níveis) | `zion_diag_preparacao_v2`, `zion_diag_ajustes_v2`, `zion_diag_alto_v2` | 3 modelos (1 por nível), levam ao checkout do Clube |
| 9 | Objeção "não agora" | `zion_nao_agora` | Já em uso |
| 10 | Última chamada | `zion_ultima_destino` (imagem) | Já em uso |
| 11 | Pós-compra | `zion_clube_boas_vindas` | Utilidade |

Contando as 3 devolutivas e os 3 lembretes como 1 função cada, são **11 funções e 15 nomes de modelo**; sem os 3 toques de lembrete e sem a segmentação por dor, são 11 modelos. Os demais ficam arquivados (seção 6, fase 3). Antes de aposentar qualquer um, a Zaya precisa ser conferida (ela pode usar modelos por nome, **não verificado**).

---

## 5. Os 8 funis (pipelines)

Fonte: `pipelines_list`. `stage_automations_list` e `managed_flows_*` **não foram consultados** (exigem um id de etapa; ver nota ao final). Contagens são de cards (um card por lead).

| Pipeline | Grupo | Propósito | Cards | Último movimento | Em uso? | Recomendação |
|---|---|---|---|---|---|---|
| **Mentoria Zion · Ativação → Ligação → Reunião → Venda** | ★ EM USO AGORA | Funil atual desde 05/11: formulário → Zaya → reunião estratégica → venda (Mentoria R$ 2.900, Trilha+Clube R$ 490, Land Bank R$ 270). 16 etapas, R$ 27 mil em aberto | 104 | 12/11 | **Sim** | **Manter** (é o funil principal) |
| **Parceria Zion · Todos até a reunião → Diagnóstico → Clube** | Parceria Zion | Todo lead segue até agendar a reunião de diagnóstico; 6 etapas; 100 cards "acumulados" | 110 | 12/11 | **Sim** (novo, 11/11) | **Fundir com Mentoria** ou assumir como o único: hoje os dois recebem os mesmos eventos (colisões da seção 2.2). Decisão do Bruno |
| **Club Zion Collection · Adesão → Pagamento → Membro** | — | Quem aderiu ao Club pela página da Jornada: ficha → pagamento → membro | 3 | 13/11 | Pouco (3 cards em "preencheu a ficha") | **Manter** (é o único para a venda do Club); revisar junto com o Parceria |
| **Base antiga · Reativação → Reunião** | — | Reativação da base antiga: P1 operadores, P2/P3 terreno, P4 triagem, corretores | 1.657 | 12/11 | **Sim, sem movimento** (nenhum respondeu, 0 em "Respondeu"/"Sem retorno") | **Manter** (ativo, é a fila dos disparos de reativação); revisar se P4 (562) e corretores (190) valem disparo |
| **FUNIL SDR** | z · Antigos (não usar agora) | Funil SDR antigo (set/2026): base, ligação 1 a 3, reunião marcada, no-show | 1.735 (1.548 em "BASE ANTIGA") | 01/10 | **Não** (mas 2 fluxos "TAG AUTOMÁTICA" ainda disparam com `PREENCHEU FORMULÁRIO`: 16 exec.) | **Arquivar** depois de migrar a base para "Base antiga · Reativação" (os 1.548 cards parecem duplicar os 1.657) |
| **0 · LIGAÇÕES BRUNO** | z · Antigos | Fila diária de ligações do fundador (terra grande, capital alto) | 40 (todos em "Ligar Hoje") | 10/09 | **Não** | **Arquivar** (substituído pela etapa "3 · Ligar hoje (Bruno)" da Mentoria) |
| **Funil Terreno · Zion Collection** | z · Antigos | Cliques para WhatsApp e disparos (Jornada R$ 270, Consultoria R$ 490); 12 etapas | 4 (todos "Novo contato") | 05/11 | **Não** | **Arquivar** (mas 8 fluxos ativos de botão ainda disparam no número Zion Collection: manter os fluxos até desligar os botões) |
| **Reserva Direta Zion** | Zion Reservas | Hospedagem B2C (Noite Mágica, recuperação de reservas) | 32 (todos "Cupom revelado") | 28/10 | **Parado** desde 28/10 | **Manter separado** (é outra linha de negócio), sem fundir. Parado por falta de campanha |

Notas: o **FUNIL SDR** carrega o valor de R$ 1,5 milhão em "REUNIÃO MARCADA" (10 cards): verificar antes de arquivar para não perder o histórico de oportunidade. As etapas **sem cards e sem fluxo** (ex.: Club "4 · Entrou na área de membros", Mentoria "7 · Oferta feita") são normais num funil novo.
**Não verificado:** automações por etapa (`stage_automations_list`) e fluxos geridos (`managed_flows_list_by_pipeline`); o `flows_list` já mostra que **nenhum dos 93 fluxos tem tipo de gestão** (`managementType` vazio em todos), então as automações de etapa estão fora desta contagem.

---

## 6. Recomendações de limpeza em fases (arquivar, não excluir)

**Fase 0, antes de arquivar qualquer coisa (urgente e não destrutiva)**
1. Recarregar créditos do ClickMax e reenviar o primeiro toque para os 74 leads que falharam. Disparar mensagem exige "aprovado" do Bruno.
2. Decidir se a jornada real é Mentoria (★) ou Parceria, para saber qual pipeline cada gatilho alimenta.
3. Tirar o nome "★ EM USO AGORA" dos fluxos que estão em rascunho (`Lembretes da reunião · Zaya`, `No-show`, `Teste A`). Só nome de grupo, sem mexer em lógica.

**Fase 1: arquivar rascunhos com 0 execuções (41 fluxos; lista aproximada por grupo, conferir no inventário da seção 1)**: Aquecimento ×2, Ebook Glamping Vol. 2, Raio-X 1/2/3/5, Clube R$ 97 ×3 (só se a venda do Club for pelo pipeline Club e os modelos continuarem como estão: manter os 3 se forem ativar), Consultoria R$ 490, Curso Dossiê ×2, Funil Terreno 0/0b/2/3/Boas-vindas/Menu parceiros, HOSP ×3, NM Cadência, Leads novos ×4, Partnership, Método (Asaas nativo, Pós-diagnóstico), Parceiro e Clube/terreno (3 toques), Ativação ×2, Bubble Orçamento, TESTE Nome Zion Collection. **Antes de arquivar, conferir se algum será ativado**: as 3 devolutivas do diagnóstico, os lembretes da reunião e o no-show **não** entram nesta fase (são lacunas que se resolvem ativando).
**Fase 2: ativos que nunca rodaram (18)** e o fechado `[CRM] Entrada — Novo Lead`: arquivar só os que não correspondem a nenhuma etapa viva; manter os de pagamento (`Passagem 3 · Pagou`, `8 · Comprou`, `Pagamento inscrição R$ 97`) até a primeira venda. Arquivar `Entrada de Lead — Meta → CRM → Funil` (vazio) e `TAG AUTOMÁTICA` v1 (fechado).
**Fase 3: modelos** (tabela 4.3): arquivar os redundantes e os 2 quebrados; manter o conjunto da seção 4.4 e os modelos em uso (4.3, cuidado).
**Fase 4: disparos e pipelines**: arquivar disparos de voz antigos (9) se a lista pesar; manter o histórico dos 7 enviados. Arquivar os 9 rascunhos "Dor/Trailer" se a jornada enxuta for adotada. Pipelines: FUNIL SDR, 0 · LIGAÇÕES BRUNO e Funil Terreno (depois de desligar os fluxos de botão ativos).

**Ordem de risco:** fase 1 e 3 são seguras (rascunho, 0 uso). A fase 2 e a de pipelines pedem conferir se há automação de etapa apontando para eles (não verificado).

*Nada foi alterado. Próxima ação sugerida: Bruno aprova a Fase 0 (créditos e decisão de funil) e a Fase 1.*

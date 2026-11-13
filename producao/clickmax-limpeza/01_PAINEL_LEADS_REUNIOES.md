# 01 · Painel de leads e reuniões · auditoria somente leitura

Data da leitura: 13/11/2026. Relógio da máquina na leitura: 13/11 02:33 UTC = **12/11 23:33 BRT** (ou seja, pelo relógio o "hoje 13/11" ainda não começou em BRT). Workspace `e87e8ba9…`. Nada foi criado, alterado ou enviado. Só primeiro nome; sem telefone, e-mail ou documento.

## RESUMO (10 linhas)
1. Leads criados HOJE (13/11 desde 00h BRT): **0**. O último lead entrou em 12/11 21:44 BRT e é teste ("Teste Adesão Club 3").
2. Últimos 7 dias (07/11 a 13/11): **38 contatos, 34 reais e 4 de teste**. Origem dos reais: CxExternalPages 31, CxCalendar 1, CxQuizzes 1, CxPages 1.
3. Antigos (antes de 07/11): **2.737** (CxClients 2.614, CxExternalPages 55, CxPages 43, CxFlows 20, CxClub 5). Base total: 2.775.
4. UTM dos 34 reais: 32 vêm de campanhas Land Bank (Meta lead_ads); 9 delas são "FORM → DIAGNÓSTICO GRÁTIS → REUNIÃO" (de 11/11 em diante); 1 vem do e-mail Brevo (Noite Mágica); 2 são formulário sem UTM.
5. **Reunião amanhã (sábado 14/11): NENHUMA.** Entre 13/11 e 30/11 só existem 3 agendamentos: Lead 22 (13/11 14h, real), um teste do Bruno (13/11 16h) e Lead 09 (23/11 14h, real).
6. **Próximas reuniões reais: só 2** (Lead 22 13/11 14h BRT e Lead 09 23/11 14h BRT). Não existem 5.
7. Reuniões passadas ainda "scheduled" sem desfecho (reais, de 05/11 a 12/11): **5** (Lead 19, Lead 16 x2, Lead 05, Lead 13). No-show registrado: **1** (Lead 12, 11/11).
8. Dos 34 leads reais da semana, **31 não têm nenhuma reunião**; **8 estão sem nenhum contato registrado**, entre eles Lead 20, Lead 21, Lead 24, Lead 03, Lead 06 N. e Lead 14 (Land Bank diagnóstico com REUNIÃO, entraram em 11/11 e 12/11), parados entre 15 e 27 h.
9. Duplicidade: **22 de 31** leads sem reunião estão ao mesmo tempo em "Parceria Zion" e em "Mentoria Zion" (2 cards por pessoa).
10. Taxa lead→reunião (7 dias): **3/34 = 8,8%**; nenhuma reunião com desfecho "completed" no período. Diagnóstico geral 6/76 (7,9%) e checkout direto 3/34 (8,8%) são equivalentes; amostra pequena demais para concluir.

## 1. Leads por período
| Período | Total | Reais | Teste |
|---|---|---|---|
| Hoje (13/11 desde 00h BRT) | 0 | 0 | 0 |
| 7 dias (07/11 a 13/11) | 38 | 34 | 4 |
| Antigos (antes de 07/11) | 2.737 | não separado | não verificado |

Critério de teste: nome com "Teste" (3, origem CxForms, e-mails example.com ou b.chaerk+) e o contato do próprio Bruno (b.chaerk@, CxCalendar, 11/11). Não contados como leads reais.

Reais dos 7 dias por dia de entrada (BRT): 07/11 7 · 08/11 9 · 09/11 5 · 10/11 2 · 11/11 7 · 12/11 4 · 13/11 0.

Origem dos 34 reais: CxExternalPages 31 · CxCalendar 1 (Lead 13) · CxQuizzes 1 (Lead 17) · CxPages 1 (Lead 06 S.). Teste: CxForms 3, CxCalendar 1.

UTM dos reais (utmSource/utmMedium/utmCampaign/utmContent):
- **facebook / lead_ads / "[LAND BANK][LEADS][FORM → DIAGNÓSTICO GRÁTIS → REUNIÃO] [03/11]"**, conteúdo "DIAG · CAMPEÃO VIDEO Investidores · Form Diagnóstico": Lead 20, Lead 21, Lead 24, Lead 03, Lead 06 N., Lead 10, Lead 14, Lead 05 (8 lidos individualmente) + Lead 13 (consta no filtro por contagem). Total da campanha "→ REUNIÃO": 9.
- **facebook / lead_ads / "[LAND BANK][LEADS][FORM → DIAGNÓSTICO GRÁTIS] [03/11]"**: conteúdos "CLUB · CARROSSEL v3 · Versão E · Trazer um sócio e atrair investimentos" (Lead 15, Lead 23, Gustavo, Zi) e "DIAG · CARROSSEL v3 · Fotos novas + Land Bank" (Lead 08). Lidos individualmente.
- Outros 17 leads Land Bank de 07/11 a 09/11 (João Salamir, Maria, Lead 07, Alexandrina, Rubens, Delzuita, Stanis, Lead 11, Fatima, Valéria, Gabriel, Lead 04, Ana, Lead 02, Arivaldo, Eduardo, Lead 09): **UTM não lida lead a lead**. O total de 32 com "LAND BANK" no utmCampaign (filtro) fecha com os 15 lidos mais Lead 13 mais estes 17 (o 32º pode ser o contato de teste do Bruno; não verificado).
- **brevo / email / noite_magica_hospedes** (utmContent geral): Lead 06 S. (Zion Reservas, não é Land Bank).
- Sem UTM, formulário Clickmax (formId 53edb1df…): Lead 17 (CxQuizzes) e Elvio (nota: Elvio entrou em 09/11 e tem 2 registros de captura; um deles por esse formulário).
- Nenhum lead dos últimos 7 dias veio de campanha com "CHECKOUT" no nome (filtro devolveu 0).

Land Bank, todos os tempos (filtro utmCampaign): 109 leads; "DIAGNÓSTICO" 76; "CHECKOUT" 34 (todos os 34 também contêm "LAND BANK"). Um lead pode ter mais de uma captura, por isso 76 + 34 = 110 > 109.

## 2. Reuniões (13/11 a 30/11)
| Data/hora BRT | Primeiro nome | Status | Origem | Teste? |
|---|---|---|---|---|
| 13/11 14:00 | Lead 22 | scheduled | crm | não (diagnóstico de parceria, lead de 04/11) |
| 13/11 16:00 | Bruno (b.chaerk+teste97) | scheduled | public_booking | **TESTE** |
| 23/11 14:00 | Lead 09 | scheduled | public_booking | não (lead de 07/11; card em Mentoria) |

**Tem reunião amanhã (sábado 14/11)? Não.** A agenda "Equipe Zion" não tem nenhum registro entre 14/11 e 22/11.
**Próximas 5 reuniões reais:** só existem 2 (Lead 22 13/11 14h, Lead 09 23/11 14h). Não há 3ª.

Passadas ainda "scheduled", sem desfecho (janela 01/10 a 12/11):
| Quando (BRT) | Nome | Origem | Observação |
|---|---|---|---|
| 05/11 14:00 | Lead 19 | crm | real (reagendada de 04/11) |
| 05/11 16:00 | Lead 16 | ai | real, remarcada de 17h |
| 09/11 11:50 | Lead 16 | crm | real, segunda marcação do mesmo lead |
| 12/11 13:30 | Lead 05 | crm | real; marcado por Bruno em 12/11 12:59 BRT; já passou, sem desfecho |
| 12/11 15:00 | Lead 13 | public_booking | real; já passou, sem desfecho |
| 25/10 15:45 | Eliete | crm | teste ("Reuniao teste") |
| 03/11 14:00 · 11/11 10:00 · 12/11 14:00 | Bruno | public_booking/crm | TESTE (3 registros) |
Fora da janela: 5 de setembro (22/09 Rodrigo, 23/09 Dieter, 24/09 Fabiano, 25/09 Samuel, 29/09 Cleire), todas "scheduled" sem desfecho, do funil SDR antigo (a de Rodrigo é teste). Antes de 01/09: não verificado.

No-show: Lead 12, 11/11 17:00 BRT, origem public_booking, status `no_show` com nota (Bruno ligou às 17h sem resposta).
Canceladas reais: Lead 20 Q. (05/11) e Lead 18 (05/11). Oito cancelamentos de teste do Bruno (09/11) e os de setembro foram ignorados.
Nenhuma reunião com status `completed` na janela lida.

## 3. Leads reais dos últimos 7 dias SEM nenhuma reunião (31)
Referência de "parado": hora da leitura (13/11 02:33 UTC) menos a última atividade de sistema registrada. Tag e etapa lidas ao vivo. "Contato" = mensagem/atendimento no histórico (Message/Chat). Com reunião e fora desta lista: Lead 05, Lead 13, Lead 09.

| # | Nome | Entrou (BRT) | Campanha (UTM) | Tag | Funil · etapa | Última atividade | Contato | Parado (h) |
|---|---|---|---|---|---|---|---|---|
| 1 | Lead 20 Lead 01 | 12/11 08:19 | LAND BANK · FORM → DIAGNÓSTICO GRÁTIS → REUNIÃO [03/11] (con | DIAG | EM PREPARAÇÃO | Parceria Zion: 1 · Leads novos | e-mail validado | SEM CONTATO (verificado) | 15 |
| 2 | Lead 21 | 12/11 08:19 | LAND BANK · FORM → DIAGNÓSTICO GRÁTIS → REUNIÃO [03/11] (con | DIAG | POTENCIAL COM AJUSTES | Parceria Zion: 1 · Leads novos | e-mail validado | SEM CONTATO (verificado) | 15 |
| 3 | Lead 24 | 11/11 22:27 | LAND BANK · FORM → DIAGNÓSTICO GRÁTIS → REUNIÃO [03/11] (con | DIAG | POTENCIAL ALTO | Parceria Zion: 1 · Leads novos | e-mail validado | SEM CONTATO (verificado) | 25 |
| 4 | Lead 03 | 11/11 21:18 | LAND BANK · FORM → DIAGNÓSTICO GRÁTIS → REUNIÃO [03/11] (con | DIAG | POTENCIAL ALTO | Parceria Zion: 1 · Leads novos | e-mail validado | SEM CONTATO (verificado) | 26 |
| 5 | Lead 06 N. | 11/11 20:09 | LAND BANK · FORM → DIAGNÓSTICO GRÁTIS → REUNIÃO [03/11] (con | DIAG | POTENCIAL COM AJUSTES | Parceria Zion: 1 · Leads novos | e-mail validado | SEM CONTATO (verificado) | 27 |
| 6 | Lead 10 | 11/11 20:09 | LAND BANK · FORM → DIAGNÓSTICO GRÁTIS → REUNIÃO [03/11] (con | DIAG | POTENCIAL COM AJUSTES | Parceria Zion: 1 · Leads novos | msg WhatsApp entregue + atendimento do Bruno (12/11 22:22 BRT) | COM CONTATO (verificado) | 1 |
| 7 | Lead 14 | 11/11 20:09 | LAND BANK · FORM → DIAGNÓSTICO GRÁTIS → REUNIÃO [03/11] (con | DIAG | POTENCIAL COM AJUSTES | Parceria Zion: 1 · Leads novos | e-mail validado | SEM CONTATO (verificado) | 27 |
| 8 | Lead 15 | 11/11 02:32 | LAND BANK · FORM → DIAGNÓSTICO GRÁTIS [03/11] (CLUB CARROSSE | FUNIL TERRENO | DISPARO ENVIADO | Parceria Zion: 2 · Pendentes de agendamento (acumulados); Mentoria Zion: 1 · Novos leads | msg FALHOU (11/11 08:24 BRT) | SÓ ENVIO FALHO | 39 |
| 9 | Lead 23 | 11/11 02:32 | LAND BANK · FORM → DIAGNÓSTICO GRÁTIS [03/11] (CLUB CARROSSE | FUNIL TERRENO | DISPARO ENVIADO | Parceria Zion: 2 · Pendentes de agendamento (acumulados); Mentoria Zion: 1 · Novos leads | msg FALHOU (11/11 08:24 BRT) | SÓ ENVIO FALHO | 39 |
| 10 | Lead 08 | 10/11 21:20 | LAND BANK · FORM → DIAGNÓSTICO GRÁTIS [03/11] (DIAG CARROSSE | FUNIL TERRENO | RESPONDEU | Parceria Zion: 2 · Pendentes de agendamento (acumulados); Mentoria Zion: 1 · Novos leads | lead respondeu no WhatsApp (11/11 07:22 BRT) | LEAD RESPONDEU | 40 |
| 11 | Lead 17 | 10/11 09:30 | formulário Clickmax sem UTM (formId 53edb1df…) | ATIVAÇÃO | MENOS DE 5 MIL · NUTRIR | (sem card) | e-mail validado | SEM CONTATO (inferido) | 62 |
| 12 | Lead 06 S. | 09/11 20:45 | utm brevo/email · noite_magica_hospedes (Zion Reservas, não  | (sem tag) | (sem card) | e-mail validado | SEM CONTATO (inferido) | 75 |
| 13 | Gustavo | 09/11 08:22 | LAND BANK · FORM → DIAGNÓSTICO GRÁTIS [03/11] (CLUB CARROSSE | FUNIL TERRENO | DISPARO ENVIADO | Mentoria Zion: 1 · Novos leads; Parceria Zion: 2 · Pendentes de agendamento (acumulados) | msg entregue (10/11 07:27 BRT) | MSG ENVIADA | 64 |
| 14 | Elvio | 09/11 08:22 | formulário Clickmax sem UTM (formId 53edb1df…) | ATIVAÇÃO | MENOS DE 5 MIL · NUTRIR | Mentoria Zion: Formulário · menos de R$ 5 mil → nutrir; Parceria Zion: 2 · Pendentes de agendamento (acumulados) | msg lida (10/11 10:05 BRT) | MSG ENVIADA/LIDA | 61 |
| 15 | Zi | 09/11 08:22 | LAND BANK · FORM → DIAGNÓSTICO GRÁTIS [03/11] (CLUB CARROSSE | FUNIL TERRENO | DISPARO ENVIADO | Mentoria Zion: 3 · Ligar hoje (Bruno); Parceria Zion: 2 · Pendentes de agendamento (acumulados) | msg lida (10/11 07:53 BRT) | MSG ENVIADA/LIDA | 64 |
| 16 | João Salamir | 09/11 01:16 | Land Bank (UTM não lida individualmente; consta nos 32 por c | ATIVAÇÃO | MENOS DE 5 MIL · NUTRIR | Mentoria Zion: Formulário · menos de R$ 5 mil → nutrir; Parceria Zion: 2 · Pendentes de agendamento (acumulados) | msg lida (10/11 07:30 BRT) | MSG ENVIADA/LIDA | 64 |
| 17 | Maria | 08/11 21:18 | Land Bank (UTM não lida individualmente; consta nos 32 por c | FUNIL TERRENO | DISPARO ENVIADO | Parceria Zion: 2 · Pendentes de agendamento (acumulados); Mentoria Zion: 3 · Ligar hoje (Bruno) | msg lida (10/11 08:57 BRT) | MSG ENVIADA/LIDA | 63 |
| 18 | Lead 07 | 08/11 19:21 | Land Bank (UTM não lida individualmente; consta nos 32 por c | FUNIL TERRENO | DISPARO ENVIADO | Mentoria Zion: 3 · Ligar hoje (Bruno); Parceria Zion: 2 · Pendentes de agendamento (acumulados) | msg FALHOU (10/11 07:22 BRT) | SÓ ENVIO FALHO | 64 |
| 19 | Alexandrina | 08/11 19:21 | Land Bank (UTM não lida individualmente; consta nos 32 por c | ATIVAÇÃO | MENOS DE 5 MIL · NUTRIR | Parceria Zion: 2 · Pendentes de agendamento (acumulados); Mentoria Zion: 1 · Novos leads | conversa reclassificada (11/11 14:08 BRT) | CONVERSA REGISTRADA | 33 |
| 20 | Rubens | 08/11 19:21 | Land Bank (UTM não lida individualmente; consta nos 32 por c | FUNIL TERRENO | DISPARO ENVIADO | Parceria Zion: 2 · Pendentes de agendamento (acumulados); Mentoria Zion: 1 · Novos leads | msg lida (11/11 17:45 BRT) | MSG ENVIADA/LIDA | 30 |
| 21 | Delzuita | 08/11 15:32 | Land Bank (UTM não lida individualmente; consta nos 32 por c | FUNIL TERRENO | DISPARO ENVIADO | Mentoria Zion: 1 · Novos leads; Parceria Zion: 2 · Pendentes de agendamento (acumulados) | msg entregue (10/11 15:32 BRT) | MSG ENVIADA | 56 |
| 22 | Stanis | 08/11 15:32 | Land Bank (UTM não lida individualmente; consta nos 32 por c | FUNIL TERRENO | DISPARO ENVIADO | Mentoria Zion: 1 · Novos leads; Parceria Zion: 2 · Pendentes de agendamento (acumulados) | msg entregue (10/11 15:33 BRT) | MSG ENVIADA | 56 |
| 23 | Lead 11 | 08/11 13:18 | Land Bank (UTM não lida individualmente; consta nos 32 por c | FUNIL TERRENO | RESPONDEU | Mentoria Zion: 1 · Novos leads; Parceria Zion: 2 · Pendentes de agendamento (acumulados) | msg entregue (10/11 07:54 BRT) | LEAD RESPONDEU (tag) | 64 |
| 24 | Fatima | 08/11 10:11 | Land Bank (UTM não lida individualmente; consta nos 32 por c | FUNIL TERRENO | DISPARO ENVIADO | Parceria Zion: 2 · Pendentes de agendamento (acumulados); Mentoria Zion: 1 · Novos leads | msg entregue (10/11 10:11 BRT) | MSG ENVIADA | 61 |
| 25 | Valéria | 08/11 07:18 | Land Bank (UTM não lida individualmente; consta nos 32 por c | FUNIL TERRENO | DISPARO ENVIADO | Parceria Zion: 2 · Pendentes de agendamento (acumulados); Mentoria Zion: 1 · Novos leads | msg lida (10/11 18:37 BRT) | MSG ENVIADA/LIDA | 53 |
| 26 | Gabriel | 07/11 23:18 | Land Bank (UTM não lida individualmente; consta nos 32 por c | FUNIL TERRENO | DISPARO ENVIADO | Parceria Zion: 2 · Pendentes de agendamento (acumulados); Mentoria Zion: 3 · Ligar hoje (Bruno) | msg lida (10/11 08:22 BRT) | MSG ENVIADA/LIDA | 63 |
| 27 | Lead 04 | 07/11 23:18 | Land Bank (UTM não lida individualmente; consta nos 32 por c | FUNIL TERRENO | RESPONDEU | Mentoria Zion: 1 · Novos leads; Parceria Zion: 2 · Pendentes de agendamento (acumulados) | msg entregue (10/11 07:22 BRT) | LEAD RESPONDEU (tag) | 64 |
| 28 | Ana Caroline | 07/11 23:18 | Land Bank (UTM não lida individualmente; consta nos 32 por c | FUNIL TERRENO | DISPARO ENVIADO | Parceria Zion: 2 · Pendentes de agendamento (acumulados); Mentoria Zion: 1 · Novos leads | conversa reclassificada (10/11 09:22 BRT) | CONVERSA REGISTRADA | 62 |
| 29 | Lead 02 | 07/11 23:18 | Land Bank (UTM não lida individualmente; consta nos 32 por c | FUNIL TERRENO | DISPARO ENVIADO | Mentoria Zion: 3 · Ligar hoje (Bruno); Parceria Zion: 2 · Pendentes de agendamento (acumulados) | msg FALHOU (10/11 08:19 BRT) | SÓ ENVIO FALHO | 63 |
| 30 | Arivaldo | 07/11 23:17 | Land Bank (UTM não lida individualmente; consta nos 32 por c | FUNIL TERRENO | DISPARO ENVIADO | Parceria Zion: 2 · Pendentes de agendamento (acumulados); Mentoria Zion: 1 · Novos leads | msg entregue (10/11 08:19 BRT) | MSG ENVIADA | 63 |
| 31 | Eduardo | 07/11 08:27 | Land Bank (UTM não lida individualmente; consta nos 32 por c | FUNIL TERRENO | DISPARO ENVIADO | Mentoria Zion: 1 · Novos leads; Parceria Zion: 2 · Pendentes de agendamento (acumulados) | msg lida (10/11 12:07 BRT) | MSG ENVIADA/LIDA | 59 |

Legenda de contato: verificado = consultei o histórico do lead (Message/Chat) e não há nada; inferido = deduzido pela última atividade (só e-mail validado, poucas atividades); "só envio falho" = a única tentativa de WhatsApp falhou (hermes.message.failed), nunca entregue.

Resumo: 8 sem contato (6 verificados), 4 só com envio falho, 1 com atendimento do Bruno (Lead 10, ontem 22:22 BRT, 1 mensagem), 3 responderam, 2 com conversa registrada, 13 com mensagem enviada/lida e sem resposta.
**Prioridade do painel**: os 6 de Land Bank diagnóstico "→ REUNIÃO" sem contato (Lead 20 15h, Lead 21 15h, Lead 24 25h, Lead 03 26h, Lead 06 N. 27h, Lead 14 27h), mais os 4 com envio falho (39 a 64 h) e os 3 que responderam e não agendaram (Lead 08, Lead 11, Lead 04).

## 4. Distribuição por funil (cards abertos, contagem ao vivo)
| Funil | Cards | Observação |
|---|---|---|
| Mentoria Zion · Ativação → Ligação → Reunião → Venda (★ em uso) | 104 | 1 Novos leads 17; 3 Ligar hoje (Bruno) 28; Formulário <5 mil 12; Zaya qualificando 11; Dor (4 etapas) 19; 5 Reunião agendada 4; 6 Reunião feita 1; 3b 7; Já pagou 2; Agora não 2 |
| Parceria Zion · Todos até a reunião → Diagnóstico → Clube | 110 | 1 Leads novos 8; 2 Pendentes (acumulados) 100; 3 Reunião agendada 2; etapas 4 a 6 vazias |
| Base antiga · Reativação → Reunião | 1.657 | P1 589; P2 99; P3 217; P4 562; Corretores 190 |
| FUNIL SDR (antigo, "não usar") | 1.735 | BASE ANTIGA 1.548; REUNIÃO MARCADA 10; etc. |
| 0 · LIGAÇÕES BRUNO (antigo) | 40 | Ligar Hoje 40 |
| Reserva Direta Zion | 32 | Cupom revelado 32 |
| Club Zion Collection · Adesão | 3 | todos são testes ("Teste Adesão Club") |
| Funil Terreno · Zion Collection (antigo) | 4 | Novo contato 4 |

**Duplicidade (medida nos 31 leads reais sem reunião, não por amostra):** 22 (71%) têm card aberto em Parceria Zion e em Mentoria Zion ao mesmo tempo; 7 só em Parceria (os mais novos, 11 e 12/11); 2 sem card algum (Lead 17 e Lead 06 S.). Logo, o total de cards (104 + 110) conta várias pessoas duas vezes. Os 100 "Pendentes (acumulados)" da Parceria são em grande parte as mesmas pessoas dos cards da Mentoria. Duplicidade nas bases antigas (FUNIL SDR vs Base antiga): não verificado.
Inconsistência: Lead 05 (reunião 12/11) está só em Parceria "3 · Reunião agendada"; Lead 13 tem 2 cards; Lead 09 está em Mentoria e Parceria.

## 5. Taxa lead → reunião (só o comprovável)
- Últimos 7 dias, reais: **3 de 34 = 8,8%** tiveram reunião marcada (Lead 05 12/11, Lead 13 12/11, Lead 09 23/11). Nenhuma realizada e registrada.
- Campanha "DIAGNÓSTICO GRÁTIS → REUNIÃO" (9 leads, de 11/11): 2 reuniões (Lead 05, Lead 13) = 22%. Amostra de 9; Lead 13 entrou pelo agendamento público (CxCalendar), não pelo formulário; leads de 11 e 12/11 ainda têm menos de 2 dias.
- Land Bank diagnóstico, todos os tempos (76): 6 com reunião (Lead 13, Lead 05, Lead 09, Lead 22, Lead 19, Lead 18) = 7,9%.
- Land Bank "CHECKOUT" (34, todos criados antes de 07/11; nenhum nos últimos 7 dias): 3 com reunião (Lead 12 no_show, Lead 16, Lead 20 Q. cancelada) = 8,8%. Dos 3, só Lead 16 tem reunião ainda viva, sem desfecho.
- Ressalvas: um lead pode ter mais de uma UTM e janelas diferentes; os 3 com reunião no checkout vieram de captura de 03 a 06/11. Sem custo por lead/reunião (Meta não consultado). Conclusão: sem diferença provável entre diagnóstico e checkout direto com essas amostras.

## 6. Painel simples: blocos e colunas
Blocos: **Hoje** · **Esta semana (7 dias)** · **Antigos (resumo)** · **Reuniões** · **Parados sem contato**.
- Hoje: nº de leads reais criados desde 00h BRT, por origem e campanha; reuniões do dia com hora, nome e status.
- Esta semana: reais x teste, por dia, origem e campanha (utmCampaign/utmContent); quantos agendaram; taxa lead→reunião.
- Antigos: só total por origem e quantos têm reunião; sem lista.
- Reuniões: próximas (data/hora BRT, primeiro nome, status, origem), "amanhã", vencidas sem desfecho, no-show. Marcar teste.
- Parados sem contato: primeiro nome, entrou em, campanha, tag DIAG, funil·etapa, última atividade, contato (sem/falhou/enviada/respondeu), horas parado, ordenado do maior parado, destacando Land Bank diagnóstico com REUNIÃO.
Regra de teste sugerida: nome contém "Teste" ou e-mail com `b.chaerk` ou `example.com`; reuniões do lead `b.chaerk+teste97`.

Dados que **não dá para obter** (ou não verifiquei):
- UTM de 17 leads individualmente (o filtro dá só contagem); utm de leads antigos além dos totais Land Bank.
- Custo por lead e por reunião (Meta/Windsor não consultado nesta auditoria).
- Se mensagem do Zaya/flow foi respondida: só a última atividade e tags (RESPONDEU), sem leitura do conteúdo.
- Desfecho das reuniões vencidas: o campo `outcomeNote` só existe quando alguém preenche; Lead 05, Lead 13, Lead 19, Lead 16 seguem em branco.
- Teste x real nas 2.737 antigas; duplicidade entre FUNIL SDR e Base antiga; agendamentos antes de 01/09.
- Relógio: o horário "agora" vem da máquina (12/11 23:33 BRT). Se o usuário considera 13/11 de dia, "horas parado" sobe em torno de 8 a 14 h.
- Pelo ClickMax não há campo "origem do agendamento" para o Calendário do Bruno fora de public_booking/crm/ai (origem vazia em registros de setembro).
- Fraude: `suspectedFraud` aparece true em vários leads reais por e-mail sem relação com o nome; não usado para filtrar.

Arquivo de dados: `producao/clickmax-limpeza/01_painel_dados.json`.

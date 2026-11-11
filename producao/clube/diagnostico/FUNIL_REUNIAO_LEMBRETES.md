# Funil da reunião: agendar, lembrar, no-show, reagendar (11/11/2026)

Meta: todo lead chega à reunião de diagnóstico prévio e comparece. Nenhum preço em nenhuma mensagem. Nada é enviado sem o "aprovado" de Bruno.

## Funil no CRM (criado)
Pipeline `24ee754c-a883-4b35-b314-c26b41c42c96` "Parceria Zion · Todos até a reunião → Diagnóstico → Clube":
1 Leads novos `cf79a691…` · 2 Pendentes de agendamento (acumulados) `2bb339fa…` · 3 Reunião agendada `95dcb737…` · 4 Diagnóstico inicial · Boas-vindas `514b03b2…` · 5 Entrou para o clube `101dec5e…` · 6 Agora não / Sem retorno `02638c5f…`.
Os 101 leads do Land Bank (tag META | FORM LAND BANK) entraram na etapa 2.

## Tags (criadas)
REUNIÃO | AGENDADA `2d67f01c…` · CONFIRMADA `6d00c8fc…` · NO-SHOW `a0024106…` · REAGENDAR `d4cd7016…` · REALIZADA `3ceffc88…` · CLUBE | ENTROU `9e16e143…`.

## Linha do tempo
| Quando | O que acontece | Canal / template |
|---|---|---|
| Ao agendar | Confirmação com data e hora, e o que levar (localização do terreno, documentação). Tag AGENDADA. Card vai para a etapa 3. | WhatsApp `confirmacao_reuniao` |
| Dia anterior, 10h (opcional) | Lembrete leve | `lembrete_reuniao_dia` (ajustar o texto para "amanhã") ou mensagem da Zaya |
| Dia da reunião, 8h | Lembrete com pedido de confirmação ("SIM"). A Zaya marca CONFIRMADA se responder SIM | `lembrete_reuniao_dia` |
| 1 hora antes | Lembrete | `lembrete_reuniao_1h` |
| 15 minutos antes | Lembrete final | `lembrete_reuniao_15min` |
| 10 min após o horário sem entrar | No-show: mensagem com botão para novo horário. Tag NO-SHOW. Card volta à etapa 2 | `noshow_reuniao` (botão para a agenda) |
| No-show + 1 dia | A Zaya oferece 2 novos horários | conversa da Zaya |
| No-show + 3 dias | Última tentativa. Sem resposta: card vai à etapa 6 | Zaya |
| Cancelou ou remarcou | Tag REAGENDAR. Mensagem com botão e a Zaya oferece 2 horários | `reagendar_reuniao` |
| Reunião realizada | Tag REALIZADA. Card na etapa 4 (diagnóstico inicial, boas-vindas) | Bruno |
| Entrou para o clube | Tag CLUBE | ENTROU. Card na etapa 5 | Bruno |

## Onde cada peça é configurada no ClickMax
- **Lembretes e confirmação:** na aba **Notificações da agenda** (ver docs "Como mandar o lembrete da reunião"). Criar notificações: ao agendar, 1 dia antes às 10:00, no dia às 08:00, 1 hora antes e 15 minutos antes, usando os templates acima. Inserir "Data da reunião" e "Horário da reunião" nas variáveis.
- **No-show:** ligar **No-Show Automático** nas configurações de agendamento. O gatilho "Contato não entrou" dispara 10 minutos após o horário.
- **Automações de tag e etapa (fluxos):** gatilhos "Reunião agendada", "reagendada", "cancelada", "não compareceu" e "realizada" aplicam as tags e movem o card. Só são ativadas com "aprovado".

## Templates de WhatsApp (rascunhos, ainda não enviados à Meta)
confirmacao_reuniao `032aad9e…` · lembrete_reuniao_dia `f3d1a6a8…` · lembrete_reuniao_1h `024f0c8c…` · lembrete_reuniao_15min `12409387…` · noshow_reuniao `dff8c406…` · reagendar_reuniao `5882bc9f…` · agendamento_diagnostico (enviado, pendente na Meta) `f4e1d47b…`.

## Regras
Sem preço. Sem promessa de parceria, investimento ou resultado. Quem pedir para parar, para. Horário de silêncio 22h às 8h (Brasília).

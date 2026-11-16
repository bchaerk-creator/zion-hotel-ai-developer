# Ajustes na Zaya · 16/11/2026 (aprovado por Bruno)

Diagnóstico (ClickMax, 3 a 15/11): 42 leads, 211 decisões, 133 respostas, 2 chamadas de agendar_reuniao, 27 de consultar_agenda (4 com SDR_TOOL_BAD_ARGS), 47 erros. Todos os 39 follow-ups falharam com AxiosError 400 no Gupshup (modelo zion_followup_duvida aprovado, 1 variável, atualizado em 16/11 03:46). Causa do 400 ainda não confirmada.

Feito:
1. Persona da Zaya (agente db450d9a): nova regra "VELOCIDADE PARA AGENDAR": enviar o link da agenda já na 1ª ou 2ª resposta, nunca encerrar sem o link, perguntas de conhecimento depois do convite; horários de manhã preferidos. Resto da persona intacto.
2. Conhecimento: FAQ "Club Zion Collection · estruturação, jornada e objeções (16/11)" (19 itens, sem preço), id b1fe0c13-dbee-4fdd-b24c-8cede23aa3b8.

Pendente: descobrir a causa do 400 nos follow-ups (testar um follow-up real após a atualização do modelo) e do erro de consultar_agenda; medir agendamentos da Zaya nos próximos dias.

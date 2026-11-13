# Briefing · Reativação por WhatsApp (diagnóstico gratuito → calendário)

Para colar na outra conversa. Responsável: Bruno Chaerk. Escrito em 13/11/2026.

## 1. Objetivo
Reativar a base antiga (~2.775 leads) pelo WhatsApp e **agendar o máximo de diagnósticos gratuitos** (sessão estratégica). O Club Zion Collection / Jornada do Desenvolvimento (R$ 970, Asaas) **só é vendido na reunião**. Nada de link de checkout na mensagem.

## 2. O que já existe (feito na conversa do e-mail)
- Fluxo: mensagem → **formulário de qualificação** (18 perguntas, "Pré-Diagnóstico de Terrenos e Parcerias") → **calendário**.
- Link do formulário (use com utm): `https://api.clickmax.io/forms/NBtaL1Il2wrs1YM6eEu1Bv87?utm_source=whatsapp&utm_medium=broadcast&utm_campaign=<campanha>&utm_content=<mensagem>`
- Tag ao preencher: **"DIAGNÓSTICO | FORMULÁRIO SITE PREENCHIDO"**. Um fluxo gerenciado cria o card na etapa 1 do funil.
- **Pergunta 11 (capacidade de começar) é a chave de priorização.** Segmentos A/B/C por ela estão em `producao/catalogo/FORM_DIAGNOSTICO_SITE.md`.
- Segmentos de público no ClickMax: terreno (lote de segunda, 286) e operadores (17 e 18/11). Ver `producao/clube/emails/DISPARO_13-11.md`.
- E-mails enviados/agendados: 13/11 9h (45), 16/11 (286), 17–18/11 (547 + operadores). **Não mandar WhatsApp e e-mail para a mesma pessoa no mesmo dia.**
- Link de adesão (depois da reunião): https://www.zionhotelgroup.com/jornada-desenvolvimento
- Os 9 contatos com a tag DIAG já receberam convite por WhatsApp: **não repetir** para eles; eles podem ir direto ao calendário.

## 3. Recomendação: sequência de 4 toques (não um disparo só)
Ideia central: cada mensagem tem **um único pedido** e uma resposta de um toque.

| Dia | Para quem | Mensagem | Ação pedida |
|---|---|---|---|
| D0 | Lote do dia | Gancho curto: "Já imaginou ter um hotel bolha no seu terreno?" + convite do Bruno para o diagnóstico gratuito | Botão "Quero meu diagnóstico" (formulário) e botão "Não tenho interesse" |
| D+1 | Quem recebeu e não clicou | Lembrete leve, pergunta simples ("Você tem terreno ou já opera hospedagem?") | Responder 1 ou 2 |
| D+2 | Quem preencheu o formulário e **não agendou** | "Falta só escolher o horário" + link do calendário | Agendar |
| D+3 | Quem não respondeu a nada | Última mensagem, sem pressão | Sair da lista ou agendar |
| Agendados | Quem marcou | Confirmação na hora, lembrete 24h antes e 1h antes | Comparecer |

Quem respondeu "sim" ou "quero" vai para atendimento humano (ou agente de IA) com o link do calendário. Prioridade de atendimento: Q11 mais forte primeiro.

## 4. Ordem do público (do mais quente ao mais frio)
1. Operadores de hospedagem (mensagem própria: "Você já opera hospedagem. E se a Zion crescesse com você?").
2. Tem terreno em destino turístico (segmentos A/B/C pela Q11).
3. Corretores (170 e-mails válidos), triagem/pesquisando (553), demais sem tag de terreno (~1.600): cada grupo com texto próprio.

## 5. Regras de segurança do canal (muito importantes)
- Base antiga e fria: o risco é **perder a qualidade do número** do WhatsApp. Comece com um **lote-teste pequeno** (Bruno + ~20 contatos conhecidos), olhe respostas e bloqueios e só então suba.
- Em canal oficial (API), mensagem fora da janela de 24h exige **modelo (template) aprovado pela Meta**. Aprovação leva tempo: submeta já. No ClickMax: `gupshup_templates_*`. Conferir também o conector LetsBot, se esse for o número usado.
- Ritmo: lotes de poucas centenas por dia, com intervalo entre lotes.
- Toda mensagem com opção clara de sair ("Responda SAIR para não receber mais"). Quem sair recebe tag e **nunca mais entra em disparo**.
- Texto sem promessa de renda, investimento, sócio, parceria garantida, reservas ou valorização. Usar "diagnóstico gratuito com a equipe Zion". Risco CVM em "sócio/investimento": recomendo revisão de advogado.
- Sem número, depoimento ou urgência inventada.

## 6. O que o Claude precisa confirmar logo no início (e não sei de cabeça)
1. **Qual número/canal de WhatsApp** será usado: ClickMax (Gupshup) ou LetsBot.
2. Se há **templates já aprovados** utilizáveis ou se é preciso criar e submeter.
3. **Custo por mensagem** e saldo disponível para esse canal.
4. Se o calendário abre corretamente depois do formulário (Bruno ainda não confirmou o teste 15 do e-mail).

## 7. Autorizações (CLAUDE.md)
- Montar segmentos, modelos e rascunhos: pode fazer.
- **Disparar mensagens para leads e ativar automações: só com o "aprovado" de Bruno**, por lote. Gastar com anúncio: teto R$ 0.

## 8. Como medir
Por mensagem e por lote: entregues, respostas, cliques, formulários preenchidos, agendamentos, comparecimentos, bloqueios/saídas. Meta real é **agendamento**, não clique. Registrar tudo em um `DISPARO_WHATSAPP_<data>.md` nesta pasta.

## 9. Prompt sugerido para abrir a outra conversa
> Leia `CLAUDE.md` e `producao/clube/whatsapp/BRIEFING_WHATSAPP.md`. Monte a campanha de reativação por WhatsApp (sequência de 4 toques) para a base antiga, começando pelos operadores e donos de terreno. Confirme canal, templates e custo, prepare os modelos e os segmentos, e me mostre o lote-teste para eu dizer "aprovado" antes de qualquer envio.

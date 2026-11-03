# Jornada Zion Land Bank · implementação (03/11/2026)

Branch: `claude/land-bank-jornada`, criado a partir do `main` atual. Nada foi publicado no site, e nenhuma automação que manda mensagem foi ligada.

## 0. Inspeção · o caminho real hoje

| Recurso existente | Decisão | Motivo | Dependências |
|---|---|---|---|
| Home `docs/index.html` (site do Zion Hotel Group, 7 portas) | **manter + ajustar o botão** | É a página institucional. Proposta: o CTA "Solicitar Diagnóstico" passa a levar a `/landbank/`, em vez da HubSpot. **Pede decisão** porque troca uma página pública. | Publicação no `main` |
| Raio-X `docs/raio-x/` (no `main`) | **ajustar depois / não usar como página 1** | Envia o diagnóstico para `/api/public/raio-x-lead`, que **não existe no GitHub Pages**. O diagnóstico do site provavelmente se perde hoje. A página ainda mostra R$ 270 e pede faixa de capital e valor do terreno. | Decidir se ela vira redirecionamento para `/landbank/` |
| `/agendar` (widget de agenda ClickMax `projeto-de-bruno-25763216/xpfd5s9qv4gbiywp-mjuwbwt`) | **manter** | Agenda nativa do ClickMax, com Google Meet. | Liberar só para quem pagou (seção 6) |
| Formulários Meta 1779605203334486, 1679964956911881, 3609977235810279 | **ajustar (Bruno)** | Os IDs **não aparecem no ClickMax**. Não existe a origem "Formulário de anúncio (Meta)". A integração nativa nunca recebeu leads. | Tráfego → Formulários de anúncio → ligar e mapear |
| Campos "Forms Meta" (10) | **manter** | Servem para o mapeamento dos formulários Meta. | idem |
| Flow "Entrada de Lead — Meta → CRM → Funil" `e7e2dbd9` | **ajustar** | Está ativo, mas sem nenhum passo. | Decidir se vira a entrada da jornada |
| Zaya `db450d9a…` · atendimento `a3852ba2…` · canal 554861371061 (GREEN, verificado) | **manter, ajustar a configuração** | É a única agente. **Sem funil em "Abre oportunidade em"** (erro SDR_TOOL_NO_PIPELINE). 47 erros em 30 dias, a maioria retomadas fora da janela de 24 h, sem template. | Bruno: colar o prompt v2, escolher o funil, escolher o template de retomada |
| Pipeline `40529cf1` (Raio-X) | **adaptado** (seção 9) | Já tinha as entradas por tag, as passagens pela agenda e o playbook da reunião. | — |
| Pipeline "Funil Terreno" `efd7ef51` | **manter** | É do Funil Terreno e da Bubble. Não mexi. | — |
| Ofertas ClickMax (9, nenhuma ativa; conta de vendedor pendente) | **não usar** | O pagamento da jornada é o Asaas. | — |
| Link Asaas `zrhq4rk88iyta3id` (R$ 97, segundo o Bruno) | **manter** | É o checkout oficial. | Confirmar que a integração Asaas está conectada ao ClickMax |
| Flow "Pagamento Asaas (nativo) → aluno" `69c42dbf` (rascunho, sem filtro de produto) | **não ativar como está** | Sem filtro, ele trataria qualquer pagamento como Land Bank. Os gatilhos do Asaas **não têm escopo**: o filtro precisa ser uma condição dentro do flow. | Decisão C (seção 12) |
| Portal "Zion Land Bank" `6d7ceb1c…` (12 aulas, turma "Candidatos" sem produto) | **manter** | É a área de membros do Land Bank. | Liberação de acesso depois do pagamento |
| Closer (tipo de atendente `72e6e611…`) | **ajustar** | Está com 0 membros. | Indicar quem é o closer |
| Referência chatgpt.site | **não usada** | O proxy do ambiente bloqueia o acesso. Não é prova de integração. | — |

## 1. Links das duas páginas (depois de publicadas)

- Página 1 · diagnóstico: `https://bchaerk-creator.github.io/zion-hotel-ai-developer/landbank/`, arquivo `docs/landbank/index.html`
- Página 2 · inscrição: `https://bchaerk-creator.github.io/zion-hotel-ai-developer/landbank/inscricao/`, arquivo `docs/landbank/inscricao/index.html` (noindex)
- As duas já estão cadastradas no ClickMax como páginas externas, com o loader do SDK instalado: `057f5d15-3596-479b-938a-6dd852beac81` e `159794c5-a97a-4a8d-bea4-3364cf31ab91`.

## 2. Mapeamento de campos e identificadores

| Identificador | Onde fica | Observação |
|---|---|---|
| Formulário de origem | `lb_origem` ("site-diagnostico") · formulário Meta nos campos "Forms Meta" | |
| Contato | id do lead no ClickMax (criado ou atualizado por `cxs('lead')` pelo telefone ou e-mail) | |
| Submissão / diagnóstico | `lb_diag_ref` (ZLB-XXXXXXXX, aleatório e opaco) + `lb_diag_data` + `lb_diag_versao` | Um diagnóstico novo do mesmo contato gera uma ref nova; o histórico fica na atividade do contato |
| Oportunidade | card no pipeline `40529cf1` | |
| Cobrança | id do pagamento no Asaas (evento) | |
| Reunião | agendamento ClickMax (`crm.scheduling.*`) | |

Campos do diagnóstico (grupo "Land Bank · Diagnóstico v1"):
- `lb_perfil`, `lb_local`, `lb_objetivo`, `lb_dificuldade`
- `lb_tempo`, `lb_infra`, `lb_plano`, `lb_estimativas`, `lb_apresentacao`
- `lb_score`, `lb_resumo`, `lb_consentimento`

Campos da jornada (grupo "Land Bank · Jornada"):
- `lb_status_pagamento`, `lb_status_preparacao`, `lb_status_reuniao`
- `lb_pendencias`, `lb_objecao`, `lb_proxima_acao`, `lb_briefing`

São 23 campos no total. O agente recebe até 25 campos preenchidos, dos mais recentes para os mais antigos. Por isso, o `lb_resumo` concentra o essencial.

**Privacidade:**
- A URL do WhatsApp leva só o primeiro nome e a ref opaca: nada de telefone, e-mail ou respostas.
- O site guarda as respostas só no navegador da pessoa (localStorage) e no ClickMax.

## 3. Regras do diagnóstico (`diag-landbank-v1 · 2026-11-03`)

- **Perguntas:**
  1. Contato (nome, WhatsApp, e-mail opcional, autorização de contato com a finalidade explicada)
  2. Ponto de partida (ideia / terreno ou projeto / em operação)
  3. Local (para quem está na ideia, a região pretendida)
  4. Objetivo, com opções adaptadas ao perfil
  5. Dificuldade (6 opções; em "outra", um texto curto)
  6. As 5 perguntas de preparação
- **Pontuação:**
  - plano, estimativas e apresentação valem 0, 1 ou 2 cada;
  - a soma vai de 0 a 6 e é convertida para 0 a 100 (`round(soma/6*100)`).
  - Perfil, local, infraestrutura e tempo só personalizam a leitura, sem tirar pontos.
- **O resultado mostra:**
  - o estágio;
  - o que já está organizado e o que merece atenção;
  - o próximo passo;
  - a pontuação, com a explicação do cálculo e a versão.
  - A pontuação **não** mede o valor da área, a viabilidade, a rentabilidade nem a chance de conseguir parceiro.
- **Gravação:**
  - `cxs('lead', …)` com os `customFields` e timeout de 12 s.
  - **O botão "Inscrever meu projeto com a Zaya" só aparece quando o ClickMax confirma a gravação.**
  - Se a gravação falhar, a página avisa, oferece "Tentar de novo" e um botão para falar com a Zaya, que vai confirmar os dados.
- **Não pergunta:** capital, patrimônio ou valor do terreno.

## 4. Prompt final da Zaya
→ `zaya-prompt-v2.md` (para colar na agente existente).

## 5. Matriz de objeções
→ seção 6 do `zaya-prompt-v2.md`: 20 casos, cada um com a pergunta de esclarecimento e a direção. A fala do cliente é registrada em `lb_objecao`. As "objeções escondidas" do relatório de leads ficam como hipóteses, não como fatos.

## 6. Cadências (a construir como rascunho; ligar só com o ok do Bruno)

| Situação | Quando | Canal | Saída |
|---|---|---|---|
| Diagnóstico feito, a pessoa **abriu o WhatsApp e mandou mensagem** | imediato | Zaya, dentro da janela de 24 h | segue o roteiro |
| Diagnóstico feito, **não mandou mensagem** | +30 min, +24 h | template aprovado de "diagnóstico pronto", só com autorização (`lb_consentimento = sim`) | respondeu → Zaya; 2 sem resposta → nutrição |
| Diagnóstico incompleto | não há (o site não grava parcial) | — | — |
| Link de R$ 97 enviado, sem pagamento | +4 h dentro da janela; +24 h com template | Zaya / template | pagou, pediu para parar ou 2 tentativas |
| Pagamento pendente (PIX/boleto) | evento "vencido" do Asaas | template | confirmado → onboarding |
| Preparação pendente | +48 h depois do acesso | template | ficha concluída ou agendou |
| Reunião agendada | −24 h, −1 h | lembrete nativo da agenda | — |
| Ausência | +15 min | template de reagendamento | reagendou ou 24 h |

**Regras:**
- Nada de urgência fictícia.
- Não vender de novo para quem já pagou.
- `zlb-optout` ou "humano assumiu" encerram todas as cadências.
- Retomada fora das 24 h só com template aprovado. É isso que explica os 34 erros "AxiosError 400" atuais.

## 7. Pagamento e onboarding (a construir como rascunho)

**Flow "Land Bank · Pagamento confirmado":**
1. **Gatilho:** "Asaas payment received" e "Asaas payment confirmed". Esses gatilhos não têm escopo.
2. **Condição:** valor = 97 e descrição/link = Adesão Land Bank. Os campos exatos do evento precisam ser confirmados com um pagamento de teste.
3. **Deduplicação:** se a tag `LAND BANK | INSCRIÇÃO R$97 PAGA` já existe, termina sem fazer nada (evento duplicado não duplica nada).
4. **Ações:**
   - tag `INSCRIÇÃO R$97 PAGA`;
   - `lb_status_pagamento = confirmado`;
   - `lb_status_reuniao = liberada`;
   - move o card para "Inscrição confirmada";
   - libera o acesso no portal "Zion Land Bank" e `lb_status_preparacao = acesso enviado`, **só depois que a liberação responder com sucesso**;
   - envia o welcome.

**Welcome:**
> "{nome}, sua inscrição no Zion Land Bank foi confirmada! Já temos seu diagnóstico prévio. Agora vamos aproveitar essas informações para organizar os próximos passos do seu projeto."
>
> "Você receberá acesso aos materiais de preparação e às orientações para sua reunião de direcionamento."

- Depois do welcome vem o link de acesso e o da agenda.
- O texto "acesso liberado" só aparece depois que a liberação acontecer de verdade.

**Falha de acesso:** cria uma tarefa para o suporte e envia a mensagem "estamos liberando seu acesso" (sem dizer que já foi liberado).

## 8. Regras de agenda
- Usar a agenda nativa que já existe ("Equipe Zion" `2c00db1e…`, link público).
- A Zaya só envia o link de agenda se `lb_status_pagamento = confirmado` (rota Land Bank) **ou** se o contato tiver o direito herdado da masterclass, guardado à parte.
- A Zaya só confirma depois do evento `crm.scheduling.booked`, que já move o card.
- Reagendamento e cancelamento: as passagens nativas (`booked`, `completed`, `no_show`) já estão ativas.
- Sempre convidar o outro decisor.
- Nunca prometer reunião pessoal com o Bruno.

## 9. Briefing do closer (modelo para `lb_briefing`)

```
[FATOS INFORMADOS]
Nome · diagnóstico {lb_diag_ref} ({lb_diag_data}) · origem {lb_origem} · oferta: inscrição R$ 97 ({lb_status_pagamento})
Situação: {lb_perfil} em {lb_local} · objetivo: {lb_objetivo} · dificuldade: {lb_dificuldade}
Organizado: plano {lb_plano}; projeções {lb_estimativas}; apresentação {lb_apresentacao}; infraestrutura {lb_infra}; tempo {lb_tempo}
Pontuação de preparação: {lb_score}/100 ({lb_diag_versao})
Objeções confirmadas (fala do cliente): {lb_objecao}
Quem decide / prazo: {informado na conversa ou "pendente"}
Preparação: {lb_status_preparacao} · pendências: {lb_pendencias}
[INTERPRETAÇÃO DA ZAYA]
Expectativa sobre parceria/investimento: …
[PENDENTE]
…
Próxima pergunta recomendada: …
Caminhos possíveis (hipóteses): você faz / com você / para você
```

## 10. Adaptações feitas no pipeline `40529cf1` (estado anterior em `rollback-clickmax.md`)

| Ordem | Etapa | Entrada automática |
|---|---|---|
| 0 | Diagnóstico concluído | **nova:** contato capturado na página do diagnóstico, e a entrada antiga pela tag RAIOX continua |
| 1 | Atendimento Zaya · inscrição apresentada | |
| 2 | **Pagamento pendente** (nova) | **nova:** tag `LINK R$97 ENVIADO` |
| 3 | Inscrição confirmada · onboarding e agenda | entrada antiga pela tag RAIOX \| PAGOU R$270, mantida para os compradores antigos |
| 4 | Reunião agendada | passagem nativa pela agenda |
| 5 | Reunião feita | passagem nativa + tarefa de registrar o resultado |
| 6 | Proposta de acompanhamento | |
| 7 | Ganho · acompanhamento fechado | |
| 8 | Em dúvida · follow-up | tarefas nos dias 2, 5, 9 e 14 |
| 9 | Agora não · nutrir | |

Também foram alterados o nome e a descrição do pipeline. Pagamento, preparação e reunião ficam em campos separados da etapa comercial. Nenhuma automação existente foi alterada ou desligada.

## 11. Testes e evidências

| # | Teste | Resultado |
|---|---|---|
| 3, 4 | Visitante direto completa o diagnóstico em tela de celular (390 px) | ✅ fluxo completo, 0 erros de JavaScript |
| 5 | Gravação falha (SDK devolve erro / SDK ausente) | ✅ mostra aviso, "Tentar de novo" e não diz "registrado" |
| — | Payload enviado ao ClickMax | ✅ 16 campos `lb_*` corretos; telefone normalizado para 55DDD… |
| 11 | Pontuação e leitura | ✅ exemplo: plano 1 + projeções 0 + apresentação 1 = 33/100 |
| — | URL do WhatsApp sem dados pessoais | ✅ só o primeiro nome e a ref |
| 1, 2, 6–10, 12–22 | Gravação real, Zaya, pagamento, acesso, agenda, briefing | ⏳ **não executados.** O ambiente não alcança `api.clickmax.io` (proxy). Dependem da publicação da página e das decisões abaixo. Roteiro de teste controlado na seção 13. |

## 12. Decisões e pendências

**Decisões do Bruno:**
- **A. Publicar as duas páginas** (merge do branch no `main`) e trocar o botão da home para `/landbank/`.
- **B. Raio-X atual:** redirecionar para `/landbank/` (recomendado, porque hoje ele não grava) ou manter como está.
- **C. Pagamento:** confirmar que o Asaas está conectado ao ClickMax (Configurações → Integrações). Depois disso, eu monto o flow com filtro de valor 97 como rascunho e testamos com um pagamento real de R$ 97 seu.

**Configurações que só o app permite (Bruno):**
1. Zaya: colar o `zaya-prompt-v2.md`. Em "Abre oportunidade em", escolher o pipeline `40529cf1`. Escolher um template aprovado para as retomadas.
2. Formulários Meta: Tráfego → Formulários de anúncio → ligar os 3 e mapear as perguntas para os campos "Forms Meta".
3. Closer: incluir a pessoa no tipo de atendente Closer.
4. Template de WhatsApp "diagnóstico pronto", para quem não mandou mensagem.

## 13. Roteiro de teste controlado (depois de publicar)
1. Abrir `/landbank/?novo=1` com um WhatsApp e um e-mail de teste seus (o contato recebe a tag `LAND BANK | TESTE CONTROLADO`).
2. Conferir no ClickMax: contato criado, os 16 campos `lb_*` preenchidos e o card em "Diagnóstico concluído".
3. Clicar em "Inscrever meu projeto com a Zaya" e enviar a mensagem. Conferir se a Zaya cita o diagnóstico sem repetir perguntas.
4. Fazer o diagnóstico de novo com o mesmo telefone. Conferir se os campos são atualizados num contato que já existe. A documentação avisa que links de captação não atualizam campos de contatos existentes; o SDK precisa ser verificado.
5. Pagamento de teste de R$ 97, depois de C, e conferir o fluxo da seção 7.

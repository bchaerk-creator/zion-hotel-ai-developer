# Reativação por dor · vídeo → formulário → reunião (preparado em 09/11/2026)

Pedido do Bruno (09/11): disparar para a base um vídeo por dor, com link para um formulário que qualifica se o lead tem recurso; o qualificado marca reunião; quem não tem paga R$ 97 para entrar na reunião (ou vai para o Club).
**Nada foi enviado, ativado nem submetido à Meta.** Tudo abaixo é rascunho. Disparo, ativação do formulário e da automação só com "aprovado".

Base usada: `REATIVACAO_DORES_BASE.md` (objeções e números da base) e o que a sessão de marketing já deixou pronto no ClickMax em 07 e 09/11 (vídeos aprovados, listas por dor, formulário de qualificação em rascunho, disparos em rascunho que levam ao Club).

## 1. O funil
1. **WhatsApp com o vídeo da dor** (número Zion Collection, +55 48 6137-1061) → botão "Ver se meu caso encaixa".
2. **Formulário de qualificação** (ClickMax, rascunho): `https://api.clickmax.io/forms/bVZEDJfzWY3lyQ0KlN0PKiQy` · id `5c51d939-0b71-4c02-91fb-a01f01ea4800`. 3 telas: dados; dor, terreno, estágio, quando; capital disponível para começar e disposição para estruturar. Grava os campos `qual_capital`, `qual_terreno`, `qual_estruturar` etc. e a tag de origem `form_qualificacao_estruturacao`.
3. **Roteamento pela resposta** (automação a criar e ativar com "aprovado"):

| Resposta | Caminho | Mensagem |
|---|---|---|
| Capital "Acima de R$ 100 mil" **e** terreno regularizado ou já opera | Reunião de 30 min com o Bruno, sem custo, na **agenda nativa do ClickMax** ("Equipe Zion", link público `app.clickmax.io/book/projeto-de-bruno-25763216/xpfd5s9qv4gbiywp-mjuwbwt`) | `zion_reuniao_qualificado` (rascunho, corrigido em 09/11: sai o Calendly) |
| Capital de R$ 10 mil a R$ 100 mil, ou terreno sem documentação completa | Reunião de diagnóstico com a equipe por R$ 97 | Texto da seção 3 (falta o link de pagamento) |
| "Ainda não tenho capital" ou até R$ 10 mil, ou "prefiro seguir sozinho" | Conteúdo e Club Base (Asaas), sem reunião | Disparo `zion_club_ecossistema` (já aprovado) |

Regra de corte proposta: R$ 100 mil (última faixa do formulário). Pelas contagens da base, 72% declararam R$ 150 a 400 mil para o projeto todo, mas o formulário pergunta o que a pessoa tem **para começar**, que é a pergunta que separa quem decide de quem pesquisa.

## 2. Modelos de WhatsApp criados (rascunho local, não submetidos à Meta)
Número: Zion Collection (`96346b98-f801-4d5c-a1a1-ff97aa9ba348`). Cada um tem o vídeo da dor no topo, o texto que espelha a resposta do formulário Meta, o botão "Ver se meu caso encaixa" (formulário) e "Agora não".

| Modelo | Id | Vídeo | Lista no ClickMax (leads) |
|---|---|---|---|
| `zion_dor_capital_form` | `6a311acd-32c5-4b85-8196-9c83e8d7f836` | video-dor-capital.mp4 | Dor · Falta capital (22) |
| `zion_dor_parceiro_form` | `ef2f1733-0bed-4f81-861e-0a4f9e4b1db1` | video-dor-parceiro.mp4 | Dor · Quero um parceiro (31) |
| `zion_dor_comecar_form` | `b3c166af-9ece-4da2-b5a1-fec02867461a` | video-dor-comecar.mp4 | Dor · Por onde começar (9) |
| `zion_dor_medo_form` | `70d12bc8-4b78-42ca-8b01-81f2cae0478a` | video-dor-medo.mp4 | Dor · Medo de errar (12) |
| `zion_dor_parada_form` | `50d3a3b1-2697-4084-84f1-6c15fcf713a7` | video-dor-parada.mp4 | Trailer Trilha · leads do form Meta (77) |
| `zion_reuniao_qualificado` | `f1b5fdd9-1b9d-4793-85af-a4da61593ed3` | (texto) | quem passar no corte |

Diferença para os modelos já aprovados (`zion_dor_*`): o botão leva ao formulário, não à página do Club; tirei a frase "operando em até 90 dias" (é promessa de prazo que não temos como garantir para o caso de cada um).
Os disparos em rascunho que a sessão de marketing criou em 07/11 (`Dor · … · leads do form Meta`, levando ao Club) continuam lá, intocados. Usar **ou** eles **ou** os novos, nunca os dois para a mesma lista.

## 3. Mensagem para quem fica na faixa de R$ 97 (texto pronto; o modelo só é criado quando houver o link)
> Oi, {{1}}! Aqui é a equipe Zion. Recebemos o seu formulário, obrigado.
>
> Pelo que você contou, o melhor próximo passo é uma reunião de diagnóstico de 45 minutos com a equipe Zion: olhamos o seu terreno, o estágio do projeto e o que falta para ele ficar de pé. Ela custa R$ 97, e esse valor serve para reservarmos o tempo para quem vai mesmo levar o projeto adiante.
>
> Toque no botão para reservar o seu horário.

Botões: "Reservar diagnóstico" (link de pagamento) e "Tenho uma dúvida". Rodapé: "A Zion avalia cada caso".
**Falta:** o link de pagamento de R$ 97. O checkout do ClickMax não vende enquanto o vendedor estiver em análise; o caminho que funciona hoje é um link do Asaas criado pelo Bruno (não mexemos na integração existente).

## 4. Para disparar (checklist)
1. Bruno aprova os textos e o corte de R$ 100 mil.
2. Submeter os 6 modelos à Meta (`gupshup_templates_submit`); aprovação leva de minutos a um dia.
3. Ativar o formulário de qualificação (hoje em rascunho).
4. Criar e ativar a automação de roteamento (seção 1).
5. Link do Asaas para os R$ 97 e criar o modelo da seção 3.
6. Conferir créditos (09/11: 5.473 disponíveis, com o extra) e criar os 5 disparos em rascunho, um por lista, com envio em lotes.
7. Disparar com "aprovado". Medir: entregues, cliques no formulário, formulários enviados, reuniões marcadas, pagamentos de R$ 97.

## 5. Auditoria do ClickMax (09/11, só leitura)
- **Agenda:** nativa do ClickMax, "Equipe Zion" (`2c00db1e-89bc-468b-bf17-4bf2a21fe443`), atendente Bruno, reuniões de 30 min com Google Meet. A grade de horários não aparece pela integração e a página pública de agendamento é bloqueada neste ambiente: **não deu para confirmar seg a sex, 14h às 17h**. Indício contra: há agendamento público para 11/11 às 10h (Brasília). Há dois bloqueios "Time Zion" do próprio Bruno (11/11 10h–12h e 13/11 16h–18h).
- **Teste de agendamento (feito com "prossiga" do Bruno, 09/11, no contato dele "Bruno Ch"):** terça 10/11, horário de Brasília: 10h **recusado** (fora da agenda); 14h, 15h, 16h e 17h **aceitos**; 18h recusado; sábado 14/11 às 14h recusado. Leitura: a agenda abre em dias úteis e vai **pelo menos das 14h até 17h30** (a 13h não deu para testar). As duas reuniões de teste foram **canceladas** em seguida.
- **Achado importante:** as reuniões criadas pela agenda saem **sem link de vídeo** (`meetingLink` vazio). As que têm Google Meet receberam o link à mão ou pela Zaya. Antes do disparo, colocar o link do Meet na agenda "Equipe Zion" (Configurações → Agenda), senão o lead marca e não tem onde entrar.
- **Zaya (SDR, ativa):** qualifica por capital e agenda na agenda nativa, nunca Calendly. **O corte dela é R$ 5 mil** para ser qualificado, bem abaixo do filtro que o Bruno quer. 69 conversas, 0 reuniões marcadas por ela, 20 escaladas.
- **Roteiro da reunião (playbook "Reunião Estratégica Zion Land Bank"):** escrito para quem pagou os R$ 97 do Land Bank; apresenta a mentoria com o "valor oficial" e a Trilha gravada de R$ 970 como plano B. **As ofertas de mentoria no ClickMax estão arquivadas** e a Mentoria de Desenvolvimento aguarda o Blueprint: falta preço e link para vender na reunião.
- **Inscrição Club + Land Bank R$ 270 no ClickMax:** incompleta (vendedor em análise). O pagamento hoje é pelo Asaas.
- **Créditos:** 5.473 disponíveis.

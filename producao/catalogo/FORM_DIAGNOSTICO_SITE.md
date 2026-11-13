# Formulário · Diagnóstico gratuito com a equipe Zion (13/11/2026)

Fluxo do e-mail "hotel bolha": e-mail → este formulário (perguntas de qualificação e de objeção) → calendário da sessão estratégica. Não há link de checkout: o Club é apresentado na reunião.

| Item | Valor |
|---|---|
| Formulário (ClickMax) | `34d1196b-4792-4923-983e-c9e89c61f7dc` · público `https://api.clickmax.io/forms/NBtaL1Il2wrs1YM6eEu1Bv87` |
| Depois de enviar | redireciona (2 s) para o calendário `https://app.clickmax.io/book/projeto-de-bruno-25763216/xpfd5s9qv4gbiywp-mjuwbwt` |
| Etiqueta aplicada (nova) | `DIAGNÓSTICO \| FORMULÁRIO SITE PREENCHIDO` `947275a3-2263-4608-b26a-6a06514c9bf0` (sem automação ligada) |
| Cartão | funil Parceria Zion, etapa "1 · Leads novos" (regra gerenciada `75aec554-d696-47c9-8f85-bce28c70aa18`: entra quando a etiqueta nova é aplicada) |

## 5 telas, 19 perguntas (todas obrigatórias) e onde cada resposta é gravada
**1 · Seus dados:** nome, e-mail, WhatsApp.
**2 · Sobre o seu terreno:** tem terreno? (`diag_possui_terreno`) · onde fica (`localizacao`) · tamanho (`area`) · documentação (`documentacao_meta`).
**3 · Estrutura e atrativo:** o que já está construído (`zion_infraestrutura`) · infraestrutura: água, energia, internet (`diag_infra`) · acesso (`diag_acesso`) · principal atrativo (`diag_atrativo`) · restrição ambiental ou de uso do solo (`diag_restricao_ambiental`).
**4 · Onde você está no projeto (objeções):** clareza do que pode fazer na área (`diag_clareza_uso`) · projeto aprovado? (`diag_projeto_aprovado`) · já buscou ajuda? (`diag_buscou_ajuda`) · principal obstáculo hoje (`diag_maior_obstaculo`) · quem decide sobre a área (`diag_decisor`).
**5 · Seu próximo passo:** sabe quanto de investimento vai exigir? (`investimento`) · disposto a estruturar com a Zion? (`diag_estruturar_zion`) · aceita receber um direcionamento? (`diag_aceita_direcionamento`) · investimento mínimo de R$ 5 mil disponível? (`diag_invest_minimo_5k`, com o apoio "pergunta de alinhamento, não é cobrança") · quando pretende começar (`diag_prazo`).

Campos novos: grupo "Diagnóstico Zion" (texto). Os ids de campo usados no formulário estão em `forms_get` (mapeamento por id, não por nome).

## Teste de 13/11/2026 (celular 390 px, lead de teste)
As 19 respostas gravaram, a etiqueta foi aplicada e o cartão entrou na etapa 1. O redirecionamento ao calendário disparou, mas a página do calendário não abre dentro do ambiente de teste (rede bloqueada); conferir no celular de Bruno.
Leads de teste a apagar: `zion.teste.diagnostico1@example.com`, `…2@…`, `…3@example.com`.

## Pendências
- Classificar as respostas em níveis (alto, ajustes, preparação) para priorizar as sessões: hoje só ficam gravadas.
- A ficha de adesão existente (`7495df8b…`) grava `localizacao` e `perfil_area` pelo nome do campo, e não pelo id; as respostas não aparecem no cadastro. Não alterei (mexe no que já existe): corrigir só com "aprovado".

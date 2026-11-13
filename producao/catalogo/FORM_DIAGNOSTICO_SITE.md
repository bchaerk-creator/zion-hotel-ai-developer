# Formulário · Diagnóstico gratuito com a equipe Zion (13/11/2026)

Fluxo do e-mail "hotel bolha": e-mail → este formulário (perguntas de qualificação) → calendário da sessão estratégica. Não há link de checkout: o Club é apresentado na reunião.

| Item | Valor |
|---|---|
| Formulário (ClickMax) | `34d1196b-4792-4923-983e-c9e89c61f7dc` · público `https://api.clickmax.io/forms/NBtaL1Il2wrs1YM6eEu1Bv87` |
| Depois de enviar | redireciona (2 s) para o calendário `https://app.clickmax.io/book/projeto-de-bruno-25763216/xpfd5s9qv4gbiywp-mjuwbwt` |
| Etiqueta aplicada (nova) | `DIAGNÓSTICO \| FORMULÁRIO SITE PREENCHIDO` `947275a3-2263-4608-b26a-6a06514c9bf0` |
| Cartão | funil Parceria Zion, etapa "1 · Leads novos" (regra gerenciada `75aec554-d696-47c9-8f85-bce28c70aa18`: entra quando a etiqueta nova é aplicada) |

## Perguntas (todas obrigatórias) e onde a resposta é gravada
1. Nome, e-mail, WhatsApp (contato).
2. Tem terreno ou área? → `diag_possui_terreno` (novo)
3. Onde fica? → `localizacao`
4. Tamanho aproximado → `area`
5. Documentação → `documentacao_meta`
6. Já existe algo construído ou estruturado? → `zion_infraestrutura`
7. Sabe quanto de investimento o projeto vai exigir? → `investimento`
8. Disposto a estruturar o projeto com a Zion? → `diag_estruturar_zion` (novo)
9. Tem disponível um investimento mínimo de R$ 5 mil? → `diag_invest_minimo_5k` (novo; texto de apoio: "pergunta de alinhamento, não é cobrança")

## Teste de 13/11/2026
Enviado pelo navegador (celular 390 px) com lead de teste: as 8 respostas gravaram, a etiqueta foi aplicada e o cartão entrou na etapa 1. O redirecionamento ao calendário disparou, mas a página do calendário não abre dentro do ambiente de teste (rede bloqueada); conferir no celular de Bruno.
Leads de teste a apagar: `zion.teste.diagnostico1@example.com` (sem cartão, antes da regra) e `zion.teste.diagnostico2@example.com`.

## Pendências
- Classificar as respostas em níveis (alto, ajustes, preparação) para o time priorizar as sessões: hoje só ficam gravadas.
- A ficha de adesão existente (`7495df8b…`) grava `localizacao` e `perfil_area` pelo nome do campo, e não pelo id; as respostas não aparecem no cadastro. Não alterei (mexe no que já existe): corrigir só com "aprovado".

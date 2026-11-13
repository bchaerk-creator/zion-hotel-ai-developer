# Formulário · Pré-Diagnóstico de Terrenos e Parcerias (13/11/2026)

Fluxo do e-mail "hotel bolha": e-mail → este formulário → calendário da sessão estratégica gratuita. Não há link de checkout: o Club é apresentado na reunião.

| Item | Valor |
|---|---|
| Formulário (ClickMax) | `34d1196b-4792-4923-983e-c9e89c61f7dc` · público `https://api.clickmax.io/forms/NBtaL1Il2wrs1YM6eEu1Bv87` |
| Título (tela) | Pré-Diagnóstico de Terrenos e Parcerias \| Zion Collection |
| Depois de enviar | redireciona (2 s) para o calendário `https://app.clickmax.io/book/projeto-de-bruno-25763216/xpfd5s9qv4gbiywp-mjuwbwt` |
| Etiqueta aplicada (nova) | `DIAGNÓSTICO \| FORMULÁRIO SITE PREENCHIDO` `947275a3-2263-4608-b26a-6a06514c9bf0` (sem automação ligada) |
| Cartão | funil Parceria Zion, etapa "1 · Leads novos" (regra gerenciada `75aec554-d696-47c9-8f85-bce28c70aa18`: entra quando a etiqueta nova é aplicada) |

## 5 telas · 6 campos de contato/terreno + 18 perguntas (72 alternativas), todas obrigatórias
1. **Seus dados:** nome, WhatsApp, e-mail, cidade (`city`), estado (`state`), tamanho aproximado (`area`).
2. **Perfil e terreno (P1–5):** situação atual · região · situação documental · infraestrutura · projeto para o terreno.
3. **Viabilidade e investimento (P6–10):** custo de implantação · rentabilidade · proposta a um investidor · quanto investiria pessoalmente · divisão do resultado.
4. **Capacidade e intenção (P11–13):** capacidade para iniciar (até R$ 5 mil … acima de R$ 50 mil) · principal obstáculo · próximo passo se houver potencial.
5. **Conscientização e decisão, ECROI (P14–18):** espelhamento · colapso de crença · reconhecimento · orientação · implementação.

Cada pergunta grava em um campo próprio (grupo "Pré-diagnóstico Zion", `pd_*`, nomes "Pré-diagnóstico 01…18"). Textos e alternativas exatamente como aprovados por Bruno em 13/11.
LGPD: "Concordo em receber contato da Zion Hotel Group International e com o uso das minhas respostas para preparar o meu atendimento e a sessão estratégica."

## Teste de 13/11/2026 (celular 390 px, lead de teste)
Todas as 18 respostas + tamanho gravaram, cidade e estado foram para o cadastro, a etiqueta foi aplicada e o cartão entrou na etapa 1. O redirecionamento ao calendário disparou, mas a página do calendário não abre no ambiente de teste (rede bloqueada); conferir no celular de Bruno.
Leads de teste a apagar: `zion.teste.diagnostico1` a `4` (@example.com).

## Pendências
- Classificar as respostas em níveis para priorizar as sessões (hoje só ficam gravadas).
- Campos `diag_*` (14 campos) ficaram sem uso após a troca do formulário; podem ser desativados.
- A ficha de adesão existente (`7495df8b…`) grava `localizacao` e `perfil_area` pelo nome do campo, e não pelo id; as respostas não aparecem no cadastro. Não alterei (mexe no que já existe): corrigir só com "aprovado".

# Diagnóstico gratuito · isca do Zion Collection Club (aprovado por Bruno em 11/11/2026)

Caminho: criativo → formulário Meta "Clube Zion Collection Adesão Terreno" → sincronização horária → classificação → tag → devolutiva (WhatsApp + e-mail) → página de resultado → checkout R$ 97 → área de membros → alinhamento → reunião.

## Peças
- `classificar.py` · regra fixa (0 a 8 pontos): documentação (0/1/2), perfil da área (0/1/2), área > 5.000 m² (1), investimento previsto (0/1/2), valor da área > R$ 500 mil (1). Níveis: alto ≥ 7, ajustes 3–6, preparação ≤ 2. Na base de 74 leads reais: 25 alto, 47 ajustes, 2 preparação. Teste: `python3 -I producao/clube/diagnostico/test_classificar.py`.
- Página de resultado: `docs/diagnostico/index.html` (`?n=alto|ajustes|preparacao`), noindex, CTA para o checkout `payments.clickmax.io/v_4pU5zNYj` com UTM. Pública em https://bchaerk-creator.github.io/zion-hotel-ai-developer/diagnostico/?n=alto
- Card verde do anúncio: `docs/ads/diagnostico/01.jpg` ("Faça o diagnóstico gratuito do seu terreno" / "Diagnóstico gratuito").

## ClickMax
- Tags: DIAG | POTENCIAL ALTO `c8867c45-e440-4e78-8d2c-c4933fc30cc8` · DIAG | POTENCIAL COM AJUSTES `b12ab070-cb50-4f42-bd27-ba85d3d32b21` · DIAG | EM PREPARAÇÃO `8b65d297-158a-46e3-9f32-6264c5afd386`.
- Templates WhatsApp (enviados à Meta, pendentes): zion_diag_alto `e0b2fdf9-09bd-491e-afcb-503cb5c5f22f`, zion_diag_ajustes `bf07349f-4d32-4cdc-aa29-ee280ded6d45`, zion_diag_preparacao `d9fa8e38-19e3-49ac-b98d-8d705ddaa2f0`. Botão "Ver meu resultado" → página de resultado.
- Fluxos (rascunho; tag aplicada → WhatsApp → e-mail): alto `b77f2f33-a259-494f-8038-3072ee22d0e6`, ajustes `d39e1d37-fe15-4fac-855d-9289eb39aff1`, preparação `794fee82-5f28-42a8-8632-7ea31f84dd92`. Validação: pendente de aprovação do template e de remetente de e-mail verificado.
- A rotina horária aplica a tag DIAG antes da META | FORM CLUBE para os leads do formulário "Adesão Terreno".

## Meta (conta 1271873041294684)
- Campanha `120250335430180016` "[CLUB][LEADS][DIAGNÓSTICO GRATUITO → FORM META → CLUBE R$97] [11/11]", objetivo Leads, PAUSADA.
- Conjunto `120250335463470016` (Brasil, 25–65, mesma segmentação das campanhas Clube/Parceiro, R$ 30/dia, otimização LEAD_GENERATION, destino formulário no anúncio), PAUSADO.
- Anúncios: aguardam o ID do formulário "Clube Zion Collection Adesão Terreno" (Meta Business Suite → Formulários instantâneos). Planejados: card verde 01.jpg + vídeo clube v3 (1805169497317625).

## Depende de Bruno
1. ID do formulário Meta "Clube Zion Collection Adesão Terreno".
2. Remetente de e-mail verificado no ClickMax.
3. Ativar os três fluxos de devolutiva depois da aprovação dos templates (e os fluxos anteriores).
4. "Aprovado" para ligar a campanha.

## 11/11 · Narrativa "Descubra e receba" (correção de Bruno)
Regra: o lead só avança se descobre algo e recebe algo. Frase oficial (Bruno, 11/11): "Receba acesso e tenha a possibilidade de ter investimentos e parceria com a Zion." O que ele descobre (o potencial do terreno / se o local pode receber uma unidade) é o que ele recebe ao entrar para o clube.
- Heros das landings `/clube`, `/parceiro` e `/parceiro/inscricao` (parágrafo "Descubra … Receba …" e a linha "O que você descobre aqui é o que você recebe lá dentro").
- Página de resultado do diagnóstico ("Você descobriu …" → "Agora receba").
- Card verde do diagnóstico: botão amarelo "Seja um parceiro Zion" (`docs/ads/diagnostico/01.jpg`).
- Cards verdes v2 para as campanhas ligadas: `docs/ads/clube-campeao/01-v2.jpg` e `docs/ads/parceiro-campeao/01-v2.jpg` (troca nos anúncios ativos só com "aprovado", porque reinicia o aprendizado do conjunto).
- Templates WhatsApp v2 (enviados à Meta, pendentes): zion_diag_alto_v2 `2e513115-4701-4c34-9e6c-16cec6455cf9`, zion_diag_ajustes_v2 `2a9990c3-9881-47f1-b78f-95197e9f76e9`, zion_diag_preparacao_v2 `a974760e-a91c-48a1-acbc-c10a7cf2c02d`; os fluxos já apontam para eles. Os v1 ficam sem uso.
- E-mails de devolutiva dos três fluxos reescritos ("Você descobriu" → "Agora receba").

### Copy do anúncio do diagnóstico (para quando o ID do formulário chegar)
Texto principal: "Descubra o potencial do seu terreno. Faça o diagnóstico gratuito: 8 perguntas, e a equipe Zion devolve em que ponto o seu projeto está e qual é o próximo passo.\n\nO que você descobre aqui é o que você recebe ao entrar para o Zion Collection Club: a formação em cinco etapas, uma sessão estratégica com a equipe, acesso aos melhores produtos de glamping do Brasil, o seu terreno no Radar do Land Bank e a possibilidade de parceria e investimento.\n\nCom mais de 20 anos no mercado internacional e 5 no Brasil, a Zion é referência em glamping no país e busca os próximos destinos. Seja um parceiro Zion."
Título: "Descubra o potencial do seu terreno" · Descrição: "Diagnóstico gratuito. Seja um parceiro Zion." · Botão: Saiba mais.

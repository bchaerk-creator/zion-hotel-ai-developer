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

## 11/11 (tarde) · Fórmula "Diagnóstico grátis → reunião → venda na reunião" (pedido de Bruno)
Volta ao que dava certo: os criativos campeões da campanha de Diagnóstico (pausada hoje) pedindo o diagnóstico gratuito, e a devolutiva leva à reunião. A oferta (clube R$ 97, parceria, investimento) é feita na reunião, não no chat.
- Campanha nova, PAUSADA: `120250343378940016` "[LAND BANK][LEADS][DIAGNÓSTICO GRÁTIS → REUNIÃO] [11/11]", objetivo Leads, formulário Meta "Land Bank | Diagnóstico do terreno" (1779605203334486, o mesmo que trouxe 57 leads a R$ 6,70 em 7 dias).
  - Conjunto `120250343393440016` (Brasil 25–65, mesma segmentação, R$ 30/dia), PAUSADO.
  - Anúncios pausados: `120250343405660016` CAMPEÃO VÍDEO Investidores (vídeo 1475116091178850) e `120250343406610016` CARROSSEL v3 Fotos novas (7 cards; 25 leads a R$ 4,68 na campanha antiga). Copy: "Comece pelo diagnóstico gratuito: 8 perguntas… Se tiver potencial, você agenda uma reunião com a equipe, sem custo."
- Caminho do lead: formulário → sync horária → classificação → tag DIAG (só ela; sem a tag da Zaya, para não vender R$ 97 no chat) → WhatsApp + e-mail de devolutiva → página de resultado → botão "Agendar minha reunião com a equipe Zion" → formulário de alinhamento (7 perguntas) → agenda. Link secundário na página: "Conhecer o Zion Collection Club".
- Página de resultado e os três e-mails já apontam para a reunião. Os templates de WhatsApp v2 (pendentes na Meta) apontam para a página, que leva à reunião.
- A campanha antiga de Diagnóstico (120250113109820016) segue pausada; seus leads antigos continuam com a Zaya.
- Depende de Bruno: ativar os três fluxos de devolutiva (quando os templates aprovarem) e dar "aprovado" para ligar a campanha nova.

### 11/11 (tarde) · Caminho rápido: o formulário do Meta é o diagnóstico, e a tela final já agenda a conversa
- Página de agendamento direto: `docs/diagnostico/agendar/index.html` → https://bchaerk-creator.github.io/zion-hotel-ai-developer/diagnostico/agendar/ (botão para a agenda da equipe, sem formulário intermediário).
- Tela de conclusão do formulário Meta "Land Bank | Diagnóstico do terreno" (Bruno configura no Business Suite): título "Diagnóstico recebido. Agende uma conversa com a nossa equipe.", descrição "Na conversa, a equipe Zion olha o seu terreno, mostra o caminho e as formas de entrar. Seja um parceiro Zion e aprenda o passo a passo.", botão "Agendar minha conversa" → a página acima.
- Anúncios da campanha `120250343378940016` atualizados: "Faça o seu diagnóstico gratuito aqui mesmo, em 8 perguntas, e já agende uma conversa com a nossa equipe. Seja um parceiro Zion e aprenda o passo a passo."
- A devolutiva por WhatsApp/e-mail vira reforço (para quem não agenda na hora), não o caminho principal.

### 11/11 (tarde) · Diagnóstico no site, com quiz do ClickMax (pedido de Bruno)
- Quiz "Diagnóstico gratuito · Zion (site, antes da conversa)" `1e8726ee-cd53-48ca-a731-a2d1cf1366da` · https://api.clickmax.io/forms/yQKzJ18d-G2LklTVamZ9Nqir · ativo.
  - 8 perguntas com pontuação 0–2: situação hoje (ativ_terreno), maior dificuldade (falta_papel_meta), disposto a aprender e estruturar (lb_status_preparacao), quer ser parceiro (busca), entraria com a infraestrutura (zion_aporte_dividido), capital para a estrutura inicial (investimento), investiria em conhecimento até R$ 5 mil (zion_investe_estruturacao), entraria no clube. Depois: nome, WhatsApp, e-mail, cidade do terreno (zion_localizacao).
  - Devolutiva por faixa (0–16): quente ≥ 11 "potencial alto para a parceria e o Land Bank", morno 6–10 "potencial com ajustes", frio ≤ 5 "projeto em preparação". Botões: "Agendar minha conversa" (agenda da equipe) e "Conhecer o clube". Tags automáticas por resultado (prefixo "DIAG QUIZ"); regras: quer ser parceiro + entra com infra → CLUBE | PERFIL PARCERIA ZION + DIAG | POTENCIAL ALTO; sem capital + sem infra → DIAG | EM PREPARAÇÃO.
- Landing `docs/diagnostico/index.html` (molde da landing do parceiro, todos os botões → quiz): https://bchaerk-creator.github.io/zion-hotel-ai-developer/diagnostico/ . Página de resultado dos templates de WhatsApp movida para `docs/diagnostico/resultado/` (a landing redireciona `?n=`).
- Lovable: rota /diagnostico (+ /agendar e /resultado) pedida, para www.zionhotelgroup.com/diagnostico.
- A devolutiva "com IA" é por regra de pontuação, não por modelo: é previsível, auditável e não inventa. Um agente de IA do ClickMax pode entrar depois no WhatsApp, se Bruno quiser.

### 11/11 (tarde) · Campanha de tráfego para o diagnóstico no site (PAUSADA)
- Campanha `120250344201770016` "[LAND BANK][TRÁFEGO][DIAGNÓSTICO NO SITE → QUIZ → REUNIÃO] [11/11]", conjunto `120250344204390016` (Brasil 25–65, R$ 30/dia), anúncios `120250344215460016` (card verde) e `120250344217930016` (vídeo campeão). Destino: https://bchaerk-creator.github.io/zion-hotel-ai-developer/diagnostico/ (landing → quiz ClickMax → devolutiva → agenda). UTM `diagnostico-site`.
- Lovable: o agente concluiu as rotas /diagnostico/agendar e /diagnostico/resultado (nada publicado). `/diagnostico` já existe no site (página atual dos anúncios, com formulário nome/WhatsApp), então NÃO foi substituída: depende de Bruno escolher outro endereço (sugestão: /diagnostico-gratuito) ou autorizar a troca. O Lovable ainda precisa de "publicar" para as rotas novas irem ao ar.
- Para anunciar hoje, o link do GitHub Pages funciona (200). Quando o endereço do site estiver definido, trocar o link dos anúncios.

### 11/11 (tarde) · Correção de rumo (Bruno): a landing NÃO muda; muda só o processo (reunião em vez de pagar)
- `docs/diagnostico/index.html` agora é a landing do parceiro, com a mesma narrativa, e só troca o destino dos 7 botões: vão para o quiz (https://api.clickmax.io/forms/yQKzJ18d-G2LklTVamZ9Nqir) e as UTMs são repassadas. Único ajuste de texto: "6 perguntas" virou "algumas perguntas". SDK do funil Parceiros removido da cópia, para não poluir o funil.
- Quiz renomeado "Parceiro/Clube · Quiz de agendamento da reunião (site)", abertura "Queremos saber um pouco mais sobre você para fazer o seu agendamento", e duas perguntas novas para a reunião: documentação (documentacao_meta) e quem decide (sem pontuação, só para o roteiro). 10 perguntas + dados.
- Roteiro da reunião, objeções e perfis: `ROTEIRO_REUNIAO.md`. Resumo automático por lead: `brief_reuniao.py` (testado em 4 perfis: `test_brief.py`).
- Removido da página de agendamento "por vídeo, 30 minutos" (sem fonte).
- Pendente de Bruno: escopo e preço da mentoria; duração e formato da reunião; quem conduz.
- A landing do clube (R$ 97) segue como está; uma versão "clube → reunião" depende de tirar o preço dos blocos e do FAQ.

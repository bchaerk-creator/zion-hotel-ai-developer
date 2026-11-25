# Pacote para o ChatGPT v2 · P0 de coerência · Mini Mentoria de Estruturação Zion (R$ 47)

Substitui `PACOTE_PARA_CHATGPT.md` (v1 vira histórico). **Sem execução:** nada foi enviado ao Meta. Subir qualquer anúncio exige "aprovado" de Bruno; criar sempre **pausado**. URLs públicas abrem depois do deploy do GitHub Pages.

## 1. Dados fixos
- Produto (mesmo nome no anúncio, página e checkout): **Mini Mentoria de Estruturação Zion**. R$ 47, pagamento único, sem mensalidade, Pix ou cartão à vista, 12 meses de acesso, reembolso em 7 dias.
- Destino: `https://infoprodutos-zion.clickmax.space/mini-mentoria` (sem parâmetros e sem `#pagar`). **Nunca** `/inscricao`, `/inscricao-47`, `/inscricao-curta`, `/parceiro-zion`.
- Botão do Meta: **Saiba mais**. Chamada com preço na arte e na primeira linha: **Acesse a plataforma por R$ 47**.
- Descrição: "Mini Mentoria Zion · R$ 47 · pagamento único".
- UTM: Tags de URL coladas **uma vez** (`09-tracking/PADRAO_UTM.md`): `utm_source=meta&utm_medium=paid&utm_campaign=mm47&utm_content=<id>&utm_term={{ad.id}}&sck={{campaign.id}}&ad_id={{ad.id}}&campaign_id={{campaign.id}}&adset_id={{adset.id}}`. As tags prontas por anúncio estão no `manifesto.json`.
- Otimização: a campanha deve ser Vendas/Purchase só quando o Purchase chegar ao Meta (ver DATA); enquanto isso, tráfego para visita qualificada. Não ativar sem "aprovado".

## 2. Criativos para usar (todos com textos e tags em `docs/ads/mm47-p0/manifesto.json`; URL base `https://bchaerk-creator.github.io/zion-hotel-ai-developer/ads/mm47-p0/<arquivo>`)
| id (utm_content) | Conceito | Arquivos | Título |
|---|---|---|---|
| mm47p0-vp0-a3-saiba-o-custo | v-P0 Curso Terreno A3 (custo) | vp0-a3-saiba-o-custo-1..5.jpg | Saiba quanto custa o seu projeto |
| mm47p0-vp0-a1-dor-direta | v-P0 Curso Terreno A1 (dor direta) | vp0-a1-dor-direta-1..5.jpg | Tem terreno? Estruture primeiro |
| mm47p0-vp0-carrossel-c-narrativa | v-P0 Carrossel C campeão | vp0-carrossel-c-narrativa-1..7.jpg | Terreno + projeto = destino |
| mm47p0-n01-autoridade-operacao | Autoridade | n01-autoridade-operacao.jpg | O método vem da operação |
| mm47p0-n02-dossie-passeio | Passeio pela plataforma | n02-dossie-passeio-1..4.jpg | Veja a plataforma por dentro |
| mm47p0-n03-exemplo-ficticio | Exemplo (dados fictícios) | n03-exemplo-ficticio.jpg | Exemplo resolvido (dados fictícios) |
| mm47p0-n04-tres-perguntas | Tutorial 3 perguntas | n04-tres-perguntas.jpg | 3 perguntas antes da obra |
| mm47p0-n05-ponto-de-partida | Transformação | n05-ponto-de-partida.jpg | Do terreno ao Dossiê |
| mm47p0-n06-entregaveis-numeros | Entregáveis em números | n06-entregaveis-numeros.jpg | O que vem dentro, em números |
| mm47p0-n07-para-quem-e | Para quem é | n07-para-quem-e.jpg | É para você? |
Mais as 7 peças da Fase 03 em `docs/ads/mm47-fase03/` (c03, c06, c08, c09, c10, c02, c04), ainda válidas. Textos: `COPIES_P0.md` (curto, longo, títulos, remarketing). Ordem de teste: `CONCEITOS_DIFERENTES.md` (atualização P0).
Vídeo: `vp0-v02-passeio-mm47-sem-audio.mp4` (52 s, 9 MB, fora do repositório; Bruno decide onde hospedar) e roteiro com voz em `ROTEIRO_VSL_v2.md` (depende de Bruno gravar).

## 3. NÃO USAR (reprovados em `AUDITORIA_COERENCIA_P0.md`)
- **Todos os vídeos "Vendas R$97" (VIDEO 01 narrativa, VIDEO 02 longa e curta, os 2 remarketing) e VIDEO 02 FORM 47:** a fala vende bubbles, "agende a tua consultoria" e investimento; o texto diz "taxa de inscrição", "equipe entrará em contato"; os de `#pagar` pulam a explicação.
- **Carrossel 10 A/B (R$ 97), Carrossel C Form 47 como está** ("Faça a sua inscrição", "possibilidade de parcerias e investimentos", "A Zion conhece e avalia").
- **MM47-03 (participação), 04 (Airbnb), 05 (parceiro).** MM47-01 e 02 só depois de refazer os cartões 4, 6 e 7 e a copy (têm "da inscrição", "conectar a investidores" e botão "Quero transformar meu terreno" sem preço).
- **Carrossel C campeão original, A1 v2 e A3 v2 originais** (R$ 270 e sessão; "curso"; "apresentar a sócios"; "poder de negociação"; "20 anos de experiência" sem prova; foto com pessoa; botão desenhado): usar só as versões `vp0-*`.
- Peças R$ 270 (vídeos 01 a 06, carrosséis A, B, C), Parceiro Zion 11/11, Land Bank/Diagnóstico → Reunião, Clube (vídeo 2 min), Urubici/Floripa, Bubble Black Friday, e-book "Glamping Lucrativo", LT47 03/04/05.
- Telas da plataforma `agendar`, `mapa`, `raiox`, `implantacao` em qualquer peça.
- A aula 1 do Onboarding (`plataforma-v02.mp4`) mostra Land Bank e investimento: não mostrar em anúncio.

## 4. Antes de ligar (depende de Bruno)
1. Aprovar as peças e a frase "potenciais parceiros e investidores".
2. Decidir pausar os anúncios ativos reprovados (VIDEO 01/02 e VIDEO 02 FORM 47). É escrita no Meta; o CREATIVE não fez.
3. Confirmar o nome exato único no checkout (`CHECKOUT_LIMPO_MM47.md`) e que a página do destino já está com a versão P0 (ZION CONVERSION).
4. Confirmar anos de experiência e títulos do fundador antes de qualquer afirmação [NC]; gravar o vídeo de autoridade.
5. Conferir no Gerenciador qual mídia está em cada anúncio ativo (ligação feita por nome e tema [H]).

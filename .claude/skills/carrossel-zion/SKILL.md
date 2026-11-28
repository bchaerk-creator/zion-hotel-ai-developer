---
name: carrossel-zion
description: Cria e exporta os carrosséis diários de Instagram da Zion Collection e de Bruno Chaerk sobre glamping, desenvolvimento hoteleiro e hotéis. Use quando Bruno pedir "carrossel", "post de hoje", "ideia de post", ou colar um comando com TIPO (passo a passo, opinião, lista, estudo de caso, notícia...) e SLIDEs. Gera roteiro slide a slide, arte em HTML 1080x1350 na identidade Zion e PNGs slide-01.png em diante, mais um molde HTML reaproveitável.
---

# Carrossel Zion

Rotina de postagem diária (glamping, desenvolvimento hoteleiro, hotéis) da conta **Zion Collection e Bruno**. Cada comando que Bruno colar vira um **tipo** em `tipos/`. Este arquivo é o fluxo; o que muda por tipo fica no arquivo do tipo.

## Tipos gravados
| Tipo | Slides | Objetivo | Arquivo |
|---|---|---|---|
| Passo a passo | 8 | Salvamento | `tipos/passo-a-passo.md` |

Ao receber um comando novo (outro `TIPO:` ou novos SLIDEs), grave-o como `tipos/<nome>.md`, na mesma estrutura, e acrescente a linha na tabela acima. Não apague tipos existentes.

## Regras fixas (valem para todo tipo)
1. **Identidade Zion** (CLAUDE.md §2): fundo preto `#040605`, creme `#FEF5F0`, **uma cor de destaque só: dourado champanhe `#C9B37E`**; Cormorant nos títulos, Aventa no texto (`docs/assets/fonts/`). Logo só os oficiais de `docs/brand/`.
2. **Formato:** 1080 × 1350 px por slide (feed 4:5), no máximo **30 palavras por slide**, uma ideia por slide, texto grande, celular primeiro.
3. **Sem invenção:** nada de número de mercado, resultado, depoimento ou prazo sem fonte. Exemplos marcados "dados fictícios" ou "exemplo". Sem promessa de reserva, ocupação, renda, investimento ou valorização.
4. **Números da Bubble** (diária, EBITDA, anos de operação) só com confirmação de Bruno registrada (mapa de sessões, pendência 6).
5. **Fotos:** só reais da Zion (`docs/assets/operacoes/`, `docs/assets/store/`); fotos com pessoas só com autorização; nunca imagem gerada como foto real. O campo VISUAL do comando é mockup em HTML (tabela, tela de chat, pasta), nunca foto inventada.
6. **Postar é com Bruno.** A skill gera roteiro, arte, PNGs e legenda. Publicar, agendar ou pagar impulsionamento só com "aprovado" de Bruno (anúncio continua com teto R$ 0 fora da Fase 1).
7. **CTA com palavra-chave** (ex.: "comenta PROMPT"): o envio no direct é manual de Bruno; não dispare mensagens a leads.

## Fluxo de cada carrossel
1. Ler o comando (tipo, slides, VISUAL). Se faltar tema, propor 3 ideias do dia (glamping, desenvolvimento hoteleiro, hotel) e seguir com a escolhida por Bruno.
2. Montar `slides.json` (formato em `tipos/passo-a-passo.md`) em `producao/instagram/carrosseis/<nnn>-<tema>/`.
3. Exportar: `node .claude/skills/carrossel-zion/scripts/build.js producao/instagram/carrosseis/<pasta>`
   Gera `slide-01.png` a `slide-NN.png`, `carrossel.html` (molde: só troca o texto do `slides.json`) e `legenda.md`.
4. Conferir visualmente pelo menos a capa, um slide com VISUAL e o CTA (Read nas imagens) e corrigir texto cortado.
5. Entregar: pasta, legenda e pendências. Registrar a linha na tabela de `producao/instagram/README.md`.

## Reuso
`carrossel.html` e `scripts/build.js` leem o `slides.json` da pasta; para o próximo carrossel basta copiar a pasta e trocar o texto.

# Carrossel Editorial Zion

Sistema que transforma um tema em um carrossel com aparência de capa e páginas
de revista internacional de luxo. Três peças:

| Peça | Arquivo | Função |
|---|---|---|
| Diretor Editorial | `src/prompts/editorial_carousel.py` | System prompt: essência da marca, arquitetura psicológica dos cards, regras de copy, fotografia, autoridade do Bruno e formato de entrega |
| Template | `scripts/editorial_carousel/template.html.j2` | 10 layouts editoriais em 1080×1350 (4:5, formato nativo do carrossel do Instagram) |
| Renderizador | `scripts/editorial_carousel/render.py` | Lê a especificação JSON, monta o HTML autocontido e captura cada card em JPG via Playwright |

## Fluxo

1. O Diretor Editorial (prompt) recebe o tema e devolve, nesta ordem: conceito,
   ideia central, gatilho principal, gatilhos secundários, headline do card 1,
   estrutura completa dos cards e a especificação JSON.
2. A especificação é salva em `scripts/editorial_carousel/carrosseis/NNN-slug.json`.
3. Fotografias reais entram em `image.src` (caminho relativo ao JSON). Sem foto,
   o card renderiza um slot editorial marcado **"Fotografia real a inserir"** com
   o briefing da imagem, para que nada seja publicado sem a foto verdadeira.
4. Renderizar:

```bash
pip install playwright jinja2   # Chromium: playwright install chromium (ou ZION_CHROMIUM_PATH)
python scripts/editorial_carousel/render.py scripts/editorial_carousel/carrosseis/001-alem-da-hospedagem.json
# saída: output/editorial/<slug>/preview.html + card_01.jpg ... card_10.jpg
```

Opções: `--out pasta`, `--quality 90`, `--scale 2` (2160×2700), `--no-capture`
(apenas o HTML de preview).

## Arquitetura dos cards

| # | Função | Layout | O leitor pensa |
|---|---|---|---|
| 1 | Atenção | `cover` | "O que é isso?" |
| 2 | Curiosidade | `typographic` | "Como assim?" |
| 3 | Lacuna | `photo-quote` | "Interessante..." |
| 4 | Autoridade | `portrait` | "Quem está falando?" |
| 5 | Insight | `insight` | "Agora entendi." |
| 6 | Prova / exemplo | `destination` | "Isso faz sentido." |
| 7 | Visão | `manifesto` | "Eu nunca tinha pensado assim." |
| 8 | Desejo | `emotional` | "Quero saber mais." |
| 9 | Posicionamento | `positioning` | "Essa empresa realmente atua nisso." |
| 10 | CTA | `cta` | "Vou acompanhar / conhecer / entrar em contato." |

Entre 6 e 10 cards. O primeiro é sempre `cover`, o último sempre `cta`, e o
mesmo layout nunca se repete em sequência. O renderizador valida isso.

## Identidade

- Títulos: Playfair Display (Regular e Italic). Textos e microtipografia: Hanken Grotesk.
  Subsets latinos (licença OFL) vendorizados em `docs/assets/fonts/` e embutidos no HTML.
- Paleta: preto profundo `#040605`, verde musgo `#1B2117`, off-white `#FEF5F0`,
  branco quente `#F3ECE1`, areia `#DED6BF`, terra `#8B714E`, dourado discreto `#B39A6C`.
- Cada card carrega o cabeçalho editorial (marca e conceito), número de página
  e edição. Linhas finas, muito respiro, zero ícones, zero gradientes decorativos.

## Campos da especificação

```json
{
  "slug": "001-alem-da-hospedagem",
  "edition": "Edição 01",
  "date_label": "MMXXVI",
  "theme": "...",
  "brand": {"name": "ZION GLAMPING COLLECTION", "tagline": "SOUL LUXURY RETREATS", "handle": "@brunochaerkofc"},
  "cards": [
    {
      "layout": "cover",
      "function": "ATENÇÃO",
      "kicker": "Leitura de mercado",
      "headline": "Texto com *itálico* e\nquebra de linha",
      "subhead": "...",
      "body": "...",
      "footnote": "...",
      "pause": "pausa",
      "image": {"src": null, "brief": "descrição da foto", "credit": "opcional"},
      "meta": {"name": "Bruno\nChaerk", "role": "Founder · CEO · Zion Hotel Group International", "facts": ["..."]},
      "stats": [{"value": "R$ 1.571", "label": "..."}],
      "items": [{"title": "...", "text": "..."}]
    }
  ]
}
```

`*texto*` vira itálico Playfair; `\n` quebra linha. `meta` é do layout
`portrait`, `stats` do `insight`, `items` do `positioning`, `pause` do
`typographic`. Números e fatos entram somente quando fornecidos e comprováveis.

## Exemplo publicado

`docs/editorial/001-alem-da-hospedagem/` contém o preview e os 10 cards da
Edição 01, renderizados com slots de fotografia (as fotos reais da Zion e do
Bruno ainda precisam ser inseridas via `image.src`).

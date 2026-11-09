# Prompts de geração · 3 fundos-piloto (sem texto)

**Não executados.** A geração depende de uma ferramenta externa (gerador de imagens do ChatGPT/OpenAI) e só será usada com a autorização do Bruno.

## Como usar (para quem vai gerar)

1. Envie ao gerador, junto com o prompt, o guia de área segura do formato (`guia-area-segura-horizontal-1536x1024.jpg` ou `guia-area-segura-vertical-1024x1536.jpg`). Ele mostra onde fica o assunto principal e onde a imagem precisa ficar calma, para receber o texto depois.
2. Gere **duas versões de cada capa**:
   - horizontal, **1536×1024**;
   - vertical, **1024×1536**.
   - Use a maior qualidade disponível.
3. Devolva os arquivos com estes nomes exatos, num zip:
   - `01-desenvolvimento-h.png` e `01-desenvolvimento-v.png`;
   - `02-gestao-h.png` e `02-gestao-v.png`;
   - `03-land-bank-h.png` e `03-land-bank-v.png`.
4. Se uma imagem vier com qualquer letra, número, placa, logotipo ou marca d'água, gere de novo. Não corrija à mão.

Depois, a composição final é feita pelo script `compor_pilotos.js`. Ele recorta para 1920×1080 e 1080×1620 e aplica o logo oficial, o título e os detalhes dourados.

## Bloco comum (colar no fim de todos os prompts)

```
Visual identity: Zion Hotel Group — premium editorial hospitality. Palette: deep moss green, sand and warm beige, natural wood, a few discreet warm-gold highlights; low saturation, natural contrast. Cinematic realistic photography, full-frame camera look, natural sophisticated light (golden hour or soft overcast), subtle atmospheric depth, fine-grain film feel. Contemporary architecture integrated with nature: timber, glass, stone, low-profile volumes that respect the terrain.
Composition: follow the attached safe-area guide — keep the reserved area calm, darker and free of detail (it will receive the title and the logo later); place the main subject in the other area.
Strictly NO text, NO letters, NO numbers, NO words, NO signage, NO logos, NO watermarks, NO captions, NO UI, NO frames or borders. Not a stock-photo look, no illustration, no cartoon, no 3D-render plastic look, no HDR, no oversaturated colors, no lens flare effects, no fantasy elements.
```

## Capa 1 · Desenvolvimento Hoteleiro

**Conceito:** transformar um terreno em empreendimento turístico.

```
Cinematic aerial drone photograph, oblique view at about 35 degrees, of a large natural plot in a Brazilian highland forest with araucaria pines and rolling green hills. In the right part of the frame, a small contemporary boutique hotel is carefully integrated into the landscape: a few low timber-and-glass pavilions connected by elevated wooden walkways, natural roofs, a discreet natural pool, most of the forest preserved around them. The scene conveys planning, entrepreneurial vision, tourism real-estate development and investment potential. Early morning golden light, soft mist in the valleys, long gentle shadows. The left part of the frame is calm forest canopy and sky in deep moss tones, without strong details.
[BLOCO COMUM]
```

## Capa 2 · Gestão Hoteleira

**Conceito:** administrar um empreendimento turístico de forma profissional.

```
Cinematic interior photograph of a refined boutique hotel lounge-office: natural wood, linen, stone, warm brass details, large window open to a green forest landscape. A hospitality manager (seen from behind or in three-quarter profile, face not the focus, elegant casual attire) works at a solid wood table with an open laptop and a printed report; the laptop screen shows only soft abstract chart shapes in green and gold, with no legible text or numbers. A cup of coffee, a small plant, an orderly desk. The scene conveys organization, leadership, profitability and professionalism. Soft natural window light, calm late-afternoon atmosphere. The person and the desk are in the right part of the frame; the left part is a calm, darker wall or out-of-focus interior in moss and sand tones.
[BLOCO COMUM]
```

## Capa 3 · Zion Land Bank

**Conceito:** transformar o potencial de um terreno em projeto turístico estruturado.

```
Cinematic wide landscape photograph of the Brazilian highlands (Serra Catarinense style): a large undeveloped plot with gentle slopes, native grassland, araucaria pines, mountains on the horizon and a river valley with morning mist. On a natural terrace of the plot, a very subtle and light proposal of tourism implantation: two or three minimal low-profile timber pavilions and a thin wooden path, few and small, clearly respecting and blending with the land (an early-stage vision, not a finished resort). The scene conveys opportunity, vision of the future and territorial value. Sunrise light from the side, layered atmosphere, wide horizon. The main subject (terrace and pavilions) in the right part of the frame; the left part is open sky and soft distant hills, calm and low in detail.
[BLOCO COMUM]
```

## Variação vertical (para as três)

Acrescentar ao prompt da capa:

```
Vertical 2:3 framing. Place the main subject in the upper 40% of the frame; keep the lower 60% calm, darker and low in detail (ground, foliage, shadow or soft interior), because it will receive the title and the logo.
```

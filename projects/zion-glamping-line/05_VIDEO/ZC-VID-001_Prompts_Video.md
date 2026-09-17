# ZC-VID-001 · VÍDEO DO ZION CASULO NA NATUREZA · REV 00

**ZION GLAMPING COLLECTION · ZION HOTEL GROUP INTERNATIONAL** · documento de direção e prompts para geração de vídeo por IA · setembro de 2026

## 1. O que existe no repositório

| Arquivo | O que é | Uso |
|---|---|---|
| `cocoon/renders/zion-casulo-orbita.webm` | Órbita de 360° em torno do modelo 3D do Casulo (14 s, 1280 x 720), gerada por `tools/turntable.js` a partir do visualizador Three.js | Vídeo técnico de apresentação (forma, Bico, deck, Janelas Olho); base de câmera para "video-to-video" |
| `cocoon/renders/web/*.jpg` | 10 renders com a marca Zion (frente, lateral, fundos, aérea, estar, suíte, banho, noite, estrutura, corte) | **Imagem de partida** para "image-to-video" (mantém a forma exata do produto) |
| `cocoon/3d/zion-cocoon.glb` | Modelo 3D | Composição em Blender / Unreal / Twinmotion se o vídeo for feito por um estúdio |

Para o vídeo cinematográfico "Casulo no meio da natureza", o caminho recomendado é **imagem → vídeo**: parte-se do render do produto (para que a forma, o Bico e as Janelas Olho apareçam certos) e a IA anima câmera, luz, vento e paisagem. Texto → vídeo puro tende a inventar outra cabana.

## 2. Ferramentas recomendadas (setembro de 2026)

| Ferramenta | Melhor para | Como usar com o Casulo |
|---|---|---|
| **Google Veo 3** (Gemini / Flow) | Fotorrealismo de paisagem, luz e som ambiente sincronizado | Modo *image-to-video* com `cocoon_ext_front.jpg`; prompt da cena 1 ou 2; 8 s por clipe, encadear em Flow |
| **OpenAI Sora** (ChatGPT) | Storyboard com várias cenas, remix de um clipe | Colar o roteiro da seção 4 no *storyboard*; usar o render como primeira imagem |
| **Runway Gen-4** | Consistência do objeto entre cenas ("references") e controle de câmera | Registrar o render como *reference* @casulo; prompts curtos por cena; câmera dolly/orbit |
| **Kling 2.x** | Movimentos de câmera longos (até 10 s) e *start + end frame* | Início: `cocoon_ext_front.jpg`; fim: `cocoon_night.jpg` para o "dia → noite" |
| **Luma Dream Machine (Ray)** | Loops e keyframes; rápido para testes | Keyframe inicial com o render; *loop* para material de site |
| **Pika / Hailuo MiniMax** | Alternativas econômicas para testes rápidos | Mesmo fluxo imagem → vídeo |

Regra prática: gerar 4 a 6 variações de cada cena, escolher a melhor, montar em CapCut / DaVinci Resolve com a trilha e o logo (`assets/` do repositório, símbolo e logotipo horizontal em vetor).

## 3. Descrição de referência do produto (colar em qualquer ferramenta)

> **ZION CASULO**: a biomorphic cocoon-shaped glamping cabin, 9.6 m long, 6 m wide, 4.2 m high, sitting on a raised timber deck (cumaru wood) over helical piles. The shell is a smooth cream-white tensioned PVDF membrane over hidden elliptical steel arches, full and rounded at the front, tapering to a pointed tail at the back. At the front, the membrane extends 2.4 m beyond the shell as a cantilevered pointed "beak" (visor) whose tip rises to 4.4 m, sheltering the deck like a wing. Under the beak, a tilted floor-to-ridge glass facade with slim bronze aluminium mullions and a pivot door. Along the ridge, a continuous 4.7 m glass "spine of light" skylight. On the sides, six elliptical lens-shaped "eye" windows with deep warm laminated-wood frames. Warm interior light: king bed under the skylight, a chaise facing the glass, a built-in mini kitchen along the curved wall, a bathtub in the tail. Brand palette: cream #FEF5F0, sand #DED6BF, earth #8B714E, deep green #1B2117. No visible seams, no logos on the membrane, no other buildings.

Em português, para ferramentas que aceitam PT:

> **ZION CASULO**: cabana de glamping em forma de casulo, 9,6 x 6,0 x 4,2 m, sobre deck elevado de cumaru. Concha lisa em membrana creme tensionada sobre arcos elípticos ocultos, cheia na frente e afilada em ponta na cauda. Na frente, a membrana avança 2,4 m em balanço como um bico apontado, com a ponta erguida a 4,4 m, abrigando o deck como uma asa. Sob o bico, fachada de vidro inclinada do piso à cumeeira com montantes finos de alumínio bronze e porta pivotante. Na cumeeira, claraboia contínua de 4,7 m (Espinha de Luz). Nas laterais, seis janelas elípticas em forma de olho com requadros profundos de madeira. Interior aconchegante: cama king sob a claraboia, chaise voltada ao vidro, mini cozinha embutida na curva, banheira na cauda. Sem emendas visíveis, sem logotipos na membrana, sem outras construções.

## 4. Roteiro · 6 cenas · 45 a 60 s

Formato 16:9 (e recorte 9:16 para redes). Luz preferida: fim de tarde (golden hour) e "blue hour" para a cena noturna. Trilha: piano e cordas suaves, sons de mata, vento na membrana.

| # | Cena | Duração | Imagem de partida | Movimento de câmera |
|---|---|---|---|---|
| 1 | Chegada: drone desce entre araucárias e a mata atlântica, o Casulo aparece num claro com névoa baixa | 8 s | `cocoon_ext_aerial.jpg` | Descida lenta em arco (crane down + orbit) |
| 2 | O Bico: câmera baixa no deck, contra-luz de fim de tarde, a ponta do bico recorta o céu; vento leve ondula a borda da membrana | 8 s | `cocoon_ext_front.jpg` | Dolly lateral lento, lente 35 mm |
| 3 | Lateral: travelling ao longo da concha revelando as Janelas Olho com luz interna acesa | 6 s | `cocoon_ext_side.jpg` | Travelling lateral, altura de olhos |
| 4 | Interior: da porta de vidro ao estar, chaise, mini cozinha na curva, a Espinha de Luz por cima | 8 s | `cocoon_int_living.jpg` | Steadicam lento para dentro |
| 5 | Suíte e cauda: cama sob a claraboia, banheira na ponta sob a janela baixa, vapor, vela | 6 s | `cocoon_int_bed.jpg` / `cocoon_int_bath.jpg` | Pan lento + dolly in |
| 6 | Noite: drone afasta-se; o Casulo brilha como uma lanterna no meio da mata, céu estrelado, fogueira no deck | 10 s | `cocoon_night.jpg` | Crane up + recuo, fade para o logo Zion |

## 5. Prompts prontos (inglês, por cena)

Cada prompt já inclui o essencial do produto. Nas ferramentas com *image-to-video*, anexar a imagem indicada na tabela acima e colar o prompt.

**Cena 1 · chegada aérea**
> Cinematic aerial drone shot descending slowly through a misty Atlantic-forest clearing at golden hour, revealing a single ZION CASULO glamping cabin: a smooth cream-white cocoon-shaped tensioned-membrane shell on a raised cumaru timber deck, with a cantilevered pointed beak at the front sheltering the deck and a tilted glass facade beneath it, six elliptical eye-shaped windows with warm wood frames along the sides, a glass skylight along the ridge, tapering to a pointed tail. Low fog over ferns, araucaria pines, warm light inside the cabin. Photorealistic, 35 mm, shallow depth of field, slow crane-down and gentle orbit, no people, no text, no other buildings.

**Cena 2 · o bico**
> Low camera on the timber deck of the ZION CASULO glamping cabin, backlit by late-afternoon sun: the cream-white membrane beak cantilevers 2.4 m over the deck with its tip rising against the sky, edge gently rippling in a light breeze; beneath it the tilted floor-to-ridge glass facade with slim bronze mullions reflects the forest. Slow lateral dolly, lens flare, dust motes in the light, photorealistic architectural film, 8 seconds, no people, no text.

**Cena 3 · lateral e Janelas Olho**
> Slow lateral tracking shot along the side of the ZION CASULO glamping cabin at dusk: a seamless cream tensioned-membrane cocoon on hidden elliptical arches, three elliptical eye-shaped windows with deep warm laminated-wood frames glowing from inside, forest and ferns in the foreground, soft blue-hour light. Photorealistic, steady camera, 50 mm, no people, no text.

**Cena 4 · interior estar**
> Steadicam shot moving slowly from the pivot glass door into the living area of the ZION CASULO cabin: curved cream fabric ceiling with a continuous glass skylight along the ridge, oak floor, a linen chaise facing the glass wall and the forest, a built-in oak mini kitchen with quartzite top along the curved wall (two-burner induction cooktop, compact oven, under-counter fridge, air fryer on the counter), warm 2700 K lighting, eye-shaped window framing trees. Photorealistic interior film, warm and calm, no people, no text.

**Cena 5 · suíte e banheira**
> Slow pan across the bedroom of the ZION CASULO cabin: king bed under the ridge skylight, curved upholstered headboard, floating nightstands with brass reading lights; then dolly toward the tail where a freestanding bathtub sits under a low eye-shaped window looking into the forest, steam rising, candles, oak and quartzite finishes, cream tensioned ceiling. Photorealistic, warm, intimate, no people, no text.

**Cena 6 · noite**
> Night aerial shot rising and pulling back from the ZION CASULO glamping cabin in a forest clearing: the cream cocoon glows softly from inside like a lantern, the skylight ridge and the eye-shaped windows lit warm, the pointed beak over the deck, a small fire pit on the deck, starry sky, fireflies, mist between the trees. Slow crane up and retreat, photorealistic, cinematic, no people, no text, ends on a wide shot.

## 6. Prompt único (texto → vídeo, quando não houver imagem de partida)

> A 30-second cinematic film of the ZION CASULO, a biomorphic glamping cabin in an Atlantic-forest clearing in southern Brazil. [colar a descrição de referência da seção 3]. Sequence: aerial descent through mist at golden hour; low deck shot of the cantilevered pointed membrane beak against the sky; lateral tracking past the eye-shaped windows glowing at dusk; interior steadicam into the living area with the built-in mini kitchen and the ridge skylight; the bathtub in the tail under a low window; night aerial retreat with the cabin glowing like a lantern. Photorealistic, 35 to 50 mm lenses, slow smooth camera moves, warm natural light, no people, no text, no logos on the building.

## 7. Prompt para o ChatGPT / Gemini gerar o vídeo por você

> Você é diretor de fotografia. Gere um vídeo cinematográfico de 8 segundos (16:9, fotorrealista) a partir da imagem anexa, que é o render de referência do ZION CASULO, uma cabana de glamping em forma de casulo. Mantenha exatamente a forma do objeto (concha creme lisa, bico em balanço apontado na frente sobre o deck de madeira, fachada de vidro inclinada, janelas elípticas com moldura de madeira, cauda em ponta). Cena: [colar a cena escolhida da seção 5]. Não adicione pessoas, texto, logotipos nem outras construções. Câmera lenta e suave; luz natural quente.

## 8. Negativos e cuidados

- Negativos úteis: `people, text, watermark, logo on the building, extra buildings, tents, domes, seams on the membrane, straight ridge, flat roof, RV, camper, distorted windows`.
- A forma do Bico é o traço de identidade: nas variações em que a IA "achata" a ponta, descartar e regerar com a imagem de partida `cocoon_ext_side.jpg`, que mostra a silhueta lateral.
- Para consistência entre cenas no Runway, registrar `cocoon_ext_front.jpg` como referência @casulo e citá-la em todos os prompts.
- Marca: aplicar o símbolo e o logotipo Zion na montagem final (vetores em `tools/svgkit.py`, funções `zion_mark`/`zion_logo`), nunca pedir à IA para desenhar o logo.
- Direitos de uso: verificar os termos comerciais da ferramenta escolhida antes de publicar o vídeo em campanha.

## 9. Próximos passos

1. Gerar as 6 cenas na ferramenta escolhida (recomendação: Veo 3 para as externas, Runway Gen-4 para as internas).
2. Montar 45 a 60 s com trilha, lettering e logo; exportar 16:9 (site, apresentação) e 9:16 (redes).
3. Quando o modelo evoluir (REV 01 com os interiores das outras cabanas), refazer os renders com `bash tools/regen.sh` e repetir o fluxo.

---
REV 00 · setembro de 2026 · ZION GLAMPING COLLECTION · sem preços

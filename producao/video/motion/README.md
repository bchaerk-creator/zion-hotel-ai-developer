# Vídeos em código · Zion

Vídeos animados feitos inteiramente em código (HTML + canvas), no estilo da coleção
[awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) (703 prompts, licença MIT).
Cada vídeo é um único arquivo `index.html` que desenha qualquer quadro a partir do tempo `t`.
Isso permite revisar quadro a quadro, corrigir texto em segundos e gravar o mesmo vídeo em 9:16 e 16:9.

## O que já existe

| Vídeo | Duração | Formatos | Uso sugerido |
|---|---|---|---|
| [`01-terreno-destino`](01-terreno-destino/index.html) | 20 s | 9:16 e 16:9 | Reel e anúncio de topo de funil, abertura da aula Z00, página do Hub |

**01 · Do terreno ao destino.** Um terreno é desenhado, a pergunta "Quanto ele rende?" é riscada,
a câmera se afasta e o terreno vira um lote dentro de um lugar (morros, sol, água, estrada).
Entra a pergunta do Developer: "Que negócio ele sustenta, e para quem?". Depois a Pirâmide Invertida©
monta as 7 etapas em palavras simples, e o vídeo fecha com a marca, "Desenvolvemos Destinos" e a
chamada "Descubra a nota da sua terra" (Zion Score). Sem números, sem siglas, sem promessa de renda.

Os MP4 prontos ficam em `01-terreno-destino/saida/`. O vídeo é mudo de propósito: a trilha entra
na plataforma (Instagram, Reels) ou na edição da aula.

## Como usar

```bash
# assistir: abra no navegador (toca em loop)
producao/video/motion/01-terreno-destino/index.html              # 9:16
producao/video/motion/01-terreno-destino/index.html?formato=16x9 # 16:9
producao/video/motion/01-terreno-destino/index.html?t=12         # congela no segundo 12

# revisar antes de gravar: folha de contato com alguns instantes (PNG em saida/)
node producao/video/motion/render.js producao/video/motion/01-terreno-destino --quadros 2,6,10,15,19

# gravar o MP4 (1080x1920 ou 1920x1080, 30 fps, H.264)
node producao/video/motion/render.js producao/video/motion/01-terreno-destino --formato 9x16
node producao/video/motion/render.js producao/video/motion/01-terreno-destino --formato 16x9
```

Precisa de Node, `playwright` (`npm i -g playwright`) e `ffmpeg`.

Para trocar um texto, edite a função `legendas()` do `index.html`, confira com `?t=` e grave de novo.

## Regras de todo vídeo Zion

As mesmas da aula simples (`producao/aula_simples/REGRAS.md`), adaptadas ao vídeo:

- Uma ideia por cena. Frases curtas, com "você".
- Sem siglas na tela (RevPAR, CAPEX, TIR...). Diga o que é em palavras simples.
- Nenhum travessão (—).
- Número só como exemplo e marcado como exemplo. Nunca números reais da Zion, nunca promessa de renda.
- Paleta e fontes da marca: fundo `#121814`, verde `#16261C`, dourado `#D9B865`, texto `#EEE8DD`;
  Cormorant Garamond (títulos, itálico nas perguntas) e Aventa (rótulos). As fontes vêm de `docs/assets/fonts/`.
- Termine com a marca e uma chamada concreta.

## Bloco técnico (cole no fim de qualquer prompt)

Junta as regras dos prompts de [verbove](https://x.com/verbove/status/2103483957266268381) e
[_koushikde_](https://x.com/_koushikde_/status/2105730717455937635), que são o que faz esses vídeos parecerem de estúdio:

```text
Um arquivo HTML. Um canvas. Uma função seek(t) que desenha o quadro do instante t.
Sem timers, sem transições CSS, sem estado guardado entre quadros.
Molas em forma fechada com overshoot pequeno; nada linear.
O texto entra depois que o elemento começa a se mover e sai antes do próximo movimento, nunca sobreposto.
Um único acento (dourado #D9B865) conduz as transições.
Formatos: 9:16 (1080x1920) e 16:9 (1920x1080) com a mesma linha do tempo; o layout se adapta.
Siga o modelo de producao/video/motion/01-terreno-destino/index.html e grave com render.js.
Antes de gravar tudo, gere uma folha de contato com um quadro por cena e corrija o que estiver apertado ou quebrado.
```

## Prompts escolhidos da coleção, adaptados para a Zion

Selecionados entre os 703 por servirem a aulas, lançamento e Instagram. Cada um aponta para o post original.

### 1. Explainer do negócio em 5 cenas
Base: [alex_prompter](https://x.com/alex_prompter/status/2103499977632997524). Uso: vídeo do Hub, da Glamping Store ou da mentoria.

```text
Você é um motion designer experiente. Faça um explainer animado de 30 segundos em um único HTML, 5 cenas:
o problema do cliente, o que a Zion faz, como funciona em 3 passos, uma prova e a marca no final.
Negócio: <Hub Zion | Zion Glamping Store | Mentoria Zion 360°>, para <dono de terreno | dono de Airbnb | pequeno empreendedor>.
Texto grande, transições suaves, cores da marca Zion.
A prova precisa ser real e aprovada; se não houver, use uma pergunta no lugar.
```

### 2. Do esboço à obra pronta
Base: [RetropunkAI](https://x.com/RetropunkAI/status/2103237989065277590) (história da Sphere, "de uma arquitetura mínima ao local pronto").
Uso: história de um projeto do portfólio.

```text
Faça uma animação explainer de 30 a 45 segundos contando a história do <Zion Bubble Glamping>,
começando por um traço mínimo do terreno até o empreendimento em operação.
Use só os fatos e imagens desta pasta: <pasta com fotos e textos aprovados>. Não invente datas nem números.
Mostre as etapas da Pirâmide Invertida© pelas quais o projeto passou. Feche com a marca e "Desenvolvemos Destinos".
```

### 3. Abertura de aula com pergunta e analogia
Base: [Cryptoxorz](https://x.com/Cryptoxorz/status/2106632900049359201). Uso: os 60 segundos iniciais de cada módulo da escola.

```text
Faça um explainer de 45 segundos para abrir a aula <D01>. Público: pessoa simples, sem formação em hotelaria.
Explique uma única pergunta central do módulo com um gancho de curiosidade, um ponto que contraria o senso comum
e uma analogia do dia a dia. Tudo tirado do e-book do módulo: <caminho do e-book>. Nada fora dele.
Siga producao/aula_simples/REGRAS.md (sem siglas, sem histórias, sem travessão, números só como exemplo).
```

### 4. Filme de produto em dois formatos
Base: [GabZoFar](https://x.com/GabZoFar/status/2105657821475852359). Uso: Zion Score ou ferramentas da escola.

```text
Faça um filme de produto de 30 segundos, estilo Apple, para o <Zion Score: diagnóstico do território com nota de 0 a 10>,
em duas versões com a mesma linha do tempo: 16:9 (1920x1080) e 9:16 (1080x1920) para Reels.
Mostre a pessoa respondendo, a nota sendo calculada (nota de exemplo, marcada como exemplo) e a chamada
"Descubra a nota da sua terra".
```

### 5. Uma frase em tipografia cinética
Base: [Gdgtify](https://x.com/Gdgtify/status/2105570411870130294) ("BUILD THE FLOOR"). Uso: posts curtos com frases do método.

```text
Faça um filme de 15 segundos de tipografia cinética com a frase: "<Primeiro o lugar e os números. A obra vem por último.>"
Cada trecho da frase reorganiza o quadro. A palavra final fica sozinha, em dourado, sobre fundo calmo.
Cormorant Garamond itálico para a frase, Aventa para rótulos. Formato 9:16.
```

### 6. Explainer longo e autônomo, com voz e legenda
Base: [AstroTheWizard](https://x.com/AstroTheWizard/status/2103629247751618782). Uso: quando houver narração (voz sintética, como no roteiro da Z00).

```text
Faça um explainer de 60 segundos, do início ao fim, sem me perguntar nada: <tema do módulo>.
Narração a partir de <producao/video/<código>/roteiro.json>, legendas gravadas no vídeo,
trilha discreta que abaixa sob a voz. Revise cada cena em quadros parados e corrija antes de entregar.
Entregue o código-fonte para ser regravado.
```

## Créditos

Técnica e prompts de referência: [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos)
(MIT) e os autores linkados acima. Os textos adaptados e o vídeo 01 são da Zion.

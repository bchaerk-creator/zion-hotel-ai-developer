# PROMPT · Claude Code · Aulas em vídeo 3D interativas da Zion

Cole este prompt no Claude Code, na pasta onde você descompactou `zion-aulas-3d.zip`.

---

Você vai produzir as aulas em vídeo do **Método Zion 360° de Desenvolvimento de Hospedagens**, no mesmo padrão do Marco Zero da Trilha 1 (os dois exemplos estão em `exemplos/`). As aulas são animações 3D interativas, com narração, legendas, mapa da trilha, capítulos e pausas para o aluno. Trabalhe uma aula por vez e pare para aprovação nos pontos marcados com **[APROVAÇÃO]**.

## 0. Regras que nunca mudam

**Voz e conteúdo**
1. A narração fala como **"nós, da Zion"**. Abertura padrão: "Olá! Nós somos da Zion, e esta é a [aula]." Nunca "aqui é o Bruno Chaerk", e nada em primeira pessoa do singular (eu, comigo, te vejo). O Bruno aparece só em terceira pessoa, como "o nosso fundador, Bruno Chaerk".
2. Não citar cidades nem operações específicas (Florianópolis, Urubici, Vargem Pequena). Usar "modelos testados e operações próprias da Zion".
3. Não inventar números, casos nem dados. Use só o que está no pacote da aula. Números de terceiros aparecem na tela com a fonte e o ano.
4. Sem travessão em nenhum texto.
5. **Aula dentro do curso não tem pitch.** Nada de formatos de mentoria, formulário ou "agende uma conversa". O pitch é outro vídeo, para vendas.
6. Marcas de terceiros (Meliá, Barceló, Wyndham, Airbnb, Booking, Bloomberg) aparecem só escritas, nunca com logotipo.
7. Fotos reais só da Zion ou de casos autorizados (Rodrigo e Priscila, Chalés Magia do Campeche). O resto é 3D.
8. Rodapé da tela final: "Conteúdo educacional. Não é oferta de investimento nem promessa de renda, retorno, ocupação, crédito ou sociedade."

**Continuidade (obrigatória em toda aula)**
1. **Abertura da aula:** "Na aula anterior, nós vimos A, B, C." Depois, o resumo da aula de hoje com os blocos ("Hoje nós vamos ver... No bloco um... no bloco dois..."). Na tela, o mapa da trilha com o ponto atual aceso. No Marco Zero não há aula anterior: ele situa o aluno na trilha.
2. **Fim de cada bloco:** "Neste bloco, você viu... No próximo bloco, nós vamos ver..." Os itens vistos ganham ✓ e os próximos entram um a um.
3. **Começo do bloco seguinte:** "No bloco anterior, você viu... Agora, nós vamos ver..."
4. **Fechamento da aula:** "Nós terminamos aqui a Aula N. A próxima aula é sobre A, B, C. Não perca." Na tela final: próxima aula, ferramenta da aula ("link abaixo deste vídeo"), site, @zionbubble, @brunochaerkofc e o rodapé.

**Formato**
- 1920x1080, 30 fps, um vídeo por bloco, com no máximo 7 minutos cada.
- Paleta: verde #16261C (fundo), creme #F5F1E8, dourado #E0BE5E, dourado escuro #8A6D2F, bege #D9CFBC, vermelho de alerta #D0573F.
- Fontes: Playfair Display para títulos e Inter para textos e chips.
- Topo: barra de capítulos à esquerda e "TRILHA · AULA" com o logo à direita. Embaixo: legendas centralizadas em duas linhas, no máximo. Barra de progresso dourada na base.
- Nome do arquivo: `AAAA-MM-DD - [Trilha/Aula] Bloco N - [Título do bloco] - Zion.mp4`

## 1. Preparar o ambiente (uma vez)
1. Verifique que estão instalados: Python 3.11 ou mais novo, Node 18 ou mais novo e ffmpeg.
2. `npm install` na raiz, que instala three 0.160 e as fontes.
3. `pip install playwright sherpa-onnx soundfile numpy scipy pillow`, depois `python -m playwright install chromium`.
4. Baixe dos releases do GitHub do sherpa-onnx (`k2-fsa/sherpa-onnx`, em tts-models e asr-models):
   - a voz provisória `vits-piper-pt_BR-faber-medium`;
   - o Whisper `sherpa-onnx-whisper-small`, usado para alinhar a voz real.
5. Coloque os dois em `models/`.

## 2. Estrutura de pastas
```
raiz/
  node_modules/         (npm install)
  engine/               (scripts e biblioteca)
  assets/img, assets/lib
  t1-aula1-bloco1/      (uma pasta por bloco, direto na raiz)
     scene.html  script.py  script.json  marks.json  voice.wav  img/  lib/  out/  saida/
```
Cada pasta de bloco fica direto na raiz, porque o `scene.html` busca `../node_modules`. Copie `assets/img` para `img/` e `assets/lib` para `lib/` dentro da pasta.

## 3. Entrada: o pacote de edição da aula
Leia no Projeto "MENTORIA BRUNO CHAERK" o pacote de edição da aula (`claude/pacote-edicao-*.md`) e o padrão `claude/padrao-producao-e-continuidade-26-10-2026.md`. O pacote traz:
- ficha da aula;
- roteiro falado por bloco;
- capítulos com a frase de início;
- mapa de cenas (frase-gatilho → figura 3D → chip → tipo);
- números na tela;
- pausas interativas;
- gancho de abertura;
- fechamento.

Se faltar alguma das pontes de continuidade da seção 0, escreva-as seguindo o modelo em `claude/marco-zero-pontes-entre-blocos-26-10-2026.md`.

**[APROVAÇÃO 1]** Mostre o roteiro final do bloco, já com as pontes, e espere o OK.

## 4. Roteiro com marcas de tempo (`script.py` → `script.json`)
1. Quebre o roteiro em frases. Cada linha tem o formato `(bloco, "cue_id" ou None, "texto exato", pausa_depois_em_s)`.
2. Dê um `cue_id` a toda frase-gatilho do mapa de cenas e a cada item que aparece na tela.
3. Pausas interativas: uma linha `(n, "p1", "[PAUSE 5]", 0)` logo depois da frase "Pausa e anota...".
4. O gancho de abertura entra no início, com bloco 0. O bloco 0 não gera legenda, porque o texto já está na tela.

Veja `exemplos/marco-zero-bloco1/script.py`.

## 5. Voz
- **Voz provisória:** `python3 -I engine/tts.py <pasta> models/vits-piper-pt_BR-faber-medium`. Gera `voice.wav` e `marks.json`, com o tempo de cada cue.
- **Voz real (gravação do Bruno ou avatar do Captions/HeyGen):**
  1. Extraia o áudio em 16 kHz.
  2. Transcreva com o Whisper em pedaços de 3 a 5 s, cortando nos silêncios (o Whisper trunca acima de 30 s).
  3. Calcule o tempo de cada palavra proporcionalmente às letras, dentro dos limites de fala de cada pedaço.
  4. Encontre cada frase-gatilho e gere o mesmo `marks.json` (`cues` e `marks` com o texto real).
  5. Normalize a voz em -16 LUFS e salve como `voice.wav`.

  A cena não muda. Ela só lê os novos tempos.

## 6. Construir a cena (`scene.html`)
1. Monte assim: `engine/template_head.html` + o conteúdo de `engine/roadmap.js` + as suas cenas + `engine/template_tail.html`.
2. No `template_tail`, ajuste a lista `CH` (capítulos) e a numeração.
3. No `template_head`, ajuste a constante `END_T` (fim da fala) e o `TOTAL`. A tela final dura de 5 a 8 s.

**A biblioteca já pronta, no template_head**
- Modelos 3D:
  - `terrain(w,d,seed,amp,{c1,c2,soil})`, que é um diorama de terreno, e `plant(T,obj,x,z)`;
  - `arauc`, `palm`, `cone`, `dome` (a Bubble), `tent`, `cabin`, `ofuro`;
  - `coin`, `coinStack`, `bulb`, `folder(label)`, `badge(size,ok)` (✓ ou ✗);
  - `halo`, `txtTex`, `plane`;
  - `extrudeRings`, que extruda mapas (Brasil e Espanha em `lib/geo.json`).
- DOM:
  - `el(cls,html,style,parent)`;
  - `chipIn(el,t,t0,x,y,anchor)`, um chip que entra com pop e registra o som;
  - `fadeUp`, `counter`, `pauseEl` / `pauseUp`, que é o anel de pausa com contagem.
- Mapa da trilha: `roadmap(sc)` + `roadmapUp(R,t,t0,feitos,atual)` e `topicList` / `topicUp` (itens com ✓).
- Cenas: `def(id,cue,{flat})` cria a cena, que vai do seu cue até o cue da próxima. `s.up=(t,u)=>{...}` anima tudo em função do tempo `t`. **Defina as cenas na ordem do tempo.**
- Câmera: `camSet(px,py,pz,lx,ly,lz)` dentro de cada `s.up`. Padrão `CAM0()`.
- Efeitos sonoros: `sfx(t,'whoosh'|'whoosh_in'|'pop'|'blip'|'tick'|'boom'|'shutter',vol)`. Registre uma vez só por cena (flag `s.sf`).

**Linguagem visual que funcionou**
- Cada ideia vira objeto. Terreno para terra, moedas para dinheiro, pasta para plano, ✗ vermelho para erro, caminho dourado para jornada, contador animado para número e rosca para porcentagem.
- Títulos no topo (Playfair, com a palavra-chave em itálico dourado), chips perto do objeto, nunca em cima da legenda (y < 900) nem do topo (y > 130).
- No começo de cada aula, use o padrão "O que você vai aprender / Por que importa / O resultado".
- Pausas interativas: anel com contagem, cartões destacando em sequência, tique a cada segundo.
- Fotos reais com leve zoom lento (Ken Burns).

## 7. Testar antes de renderizar
1. Rode `PORT=8811 python3 engine/render3d.py <pasta> test t1 t2 ...`, com um tempo por cena (cue + 2,5 s).
2. Monte uma folha de contato com as imagens.
3. Confira:
   - sobreposição de chips;
   - texto em cima de objeto;
   - objeto cortado na borda;
   - chip colado no topo ou na legenda;
   - cena vazia.
4. Corrija e teste de novo.

**[APROVAÇÃO 2]** Mostre a folha de contato.

## 8. Renderizar, sonorizar e montar
1. Render em duas metades paralelas, com portas diferentes: `PORT=8841 python3 engine/render3d.py <pasta> all 0 N/2` e `PORT=8842 ... all N/2 99999`. Rode em segundo plano e acompanhe pelo log.
2. Efeitos: `python3 engine/sfxpass.py <pasta>`, depois `python3 engine/sfx.py <pasta>`, que gera `sfx.wav`.
3. Montagem: `python3 engine/encode.py <pasta> "<nome do arquivo>"`.
4. Confira:
   - quadros pretos ou vazios (média de brilho < 8);
   - folha de contato com 12 quadros espalhados;
   - duração igual à do áudio.

**[APROVAÇÃO 3]** Entregue o vídeo.

## 9. Opção: Bruno ou avatar na bolinha
Quando houver o vídeo do avatar falando o mesmo roteiro:
1. Gere o `marks.json` a partir do áudio dele (seção 5).
2. Renderize a aula.
3. Rode `python3 engine/bolinha.py <pasta> avatar.mp4 [cx cy]`. Ele cria um círculo de 300 px no canto inferior direito, com borda dourada e sombra.
4. Monte com o áudio do avatar como `voice.wav`.

A boca e a voz vêm do mesmo arquivo, então ficam sincronizadas. Nunca coloque na bolinha um vídeo com outra fala.

## 10. Armadilhas já resolvidas (não repita)
- Antes de projetar um ponto 3D para a tela (`.project(cam)`), a câmera precisa de `updateMatrixWorld()`. O `camSet` do template já faz isso.
- `topicUp` com ✓: só troque o marcador se ele ainda existir. Já corrigido no `roadmap.js`.
- Os efeitos sonoros só saem certos numa passada única (`sfxpass.py`). Renders em pedaços não registram tudo.
- Cada render paralelo precisa de uma porta diferente.
- Não use `pkill` no mesmo comando que outras tarefas, porque ele derruba o terminal.
- O Whisper trunca acima de 30 s: transcreva em pedaços.
- Um vídeo com legendas gravadas na imagem (Captions) atrapalha o recorte. Peça sempre a exportação sem legenda e com fundo liso.
- Rótulos projetados a partir de objetos animados podem sair do quadro. Na dúvida, use posição fixa em px.

## 11. Ao terminar cada aula
- Salve no Projeto um resumo: o roteiro final com as pontes, os tempos e as decisões.
- Gere a legenda do Instagram para o corte vertical:
  - gancho de até 125 caracteres;
  - sem travessão;
  - um CTA;
  - de 3 a 5 hashtags.
- O corte vertical é opcional: o horizontal escalado para 1080 de largura sobre o fundo verde, com legendas grandes queimadas.

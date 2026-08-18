# Fotografia do site Zion

Cada slot abaixo já existe no código. Assim que o arquivo entrar nesta pasta com o nome exato, a foto aparece — nenhuma alteração de HTML é necessária. Enquanto o arquivo não existir, o slot mostra o próprio briefing na tela, em vez de uma imagem quebrada.

## Como nomear

Cada slot precisa de **três larguras**, todas em `.jpg`:

```
nome-do-slot-960.jpg     · telas pequenas
nome-do-slot-1600.jpg    · padrão (é o src)
nome-do-slot-2400.jpg    · telas grandes e retina
```

O `srcset` já está escrito nas páginas: o navegador escolhe sozinho a largura certa. Se você subir só a versão `-1600`, o site funciona igual — as outras duas são otimização.

## Receita de otimização

```bash
# a partir do original, para cada largura
for w in 960 1600 2400; do
  ffmpeg -i original.jpg -vf "scale=${w}:-2" -q:v 4 nome-do-slot-${w}.jpg
done
```

Alvo de peso: até 180 KB na `-960`, 400 KB na `-1600` e 800 KB na `-2400`.

## Direção de arte comum a todos os slots

- Fotografia documental de operação real. Nunca banco de imagens.
- Luz natural. Início da manhã e fim de tarde rendem mais do que meio-dia.
- Espaço negativo generoso: parte do quadro existe para a tipografia respirar por cima.
- Pessoas aparecem vivendo a experiência, nunca posando para a câmera.
- Sem marca d'água, sem logotipo aplicado, sem moldura.

## Os slots

### `hero-urubici-noite`

**index.html** · Hero · tela cheia · 21:9 ou mais largo

Bubble ao anoitecer, luz quente por dentro, céu ainda azul. Plano aberto, horizonte baixo. Sem pessoas no enquadramento.

*Texto alternativo já no código:* Bubble Suite iluminada por dentro ao anoitecer, na Serra Catarinense

### `territorio-serra`

**index.html** · Banda full bleed · 21:9 panorâmico

Paisagem ampla ao amanhecer: camadas de serra na neblina, sem construção visível. Horizonte no terço inferior, muito céu.

*Texto alternativo já no código:* Serra catarinense ao amanhecer, camadas de montanha na neblina

### `development-terreno`

**index.html** · Duo editorial · 3:4 retrato

Terreno bruto com vocação turística: campo aberto, relevo, luz rasante de fim de tarde. Sem construção. Sensação de potencial adormecido.

*Texto alternativo já no código:* Território ainda sem construção, ao entardecer

### `management-servico`

**index.html** · Duo editorial · 3:4 retrato

Detalhe de serviço em operação: café da manhã sendo servido, mãos, textura de madeira e cerâmica. Luz natural lateral.

*Texto alternativo já no código:* Detalhe do serviço em operação, luz natural

### `collection-bubble-interior`

**index.html** · Duo editorial · 3:4 retrato

Interior da Bubble Suite ao amanhecer: cama desfeita, névoa do lado de fora, ninguém precisa acordar cedo. Sem pessoas ou apenas silhueta.

*Texto alternativo já no código:* Interior da Bubble Suite ao amanhecer, com névoa do lado de fora

### `detalhe-textura`

**index.html** · Tríptico · 1:1 quadrado

Macro de textura natural: pedra molhada, casca de árvore ou musgo. Preenche o quadro inteiro.

*Texto alternativo já no código:* Textura natural em detalhe macro

### `pessoa-contemplacao`

**index.html** · Tríptico · 3:4 retrato

Pessoa de costas contemplando a paisagem, em silêncio. Escala humana pequena diante do território.

*Texto alternativo já no código:* Pessoa de costas diante da paisagem

### `arquitetura-modulo`

**index.html** · Tríptico · 4:3 paisagem

Arquitetura modular vista de fora, integrada à vegetação. Linha limpa, sem excesso de deque ou mobiliário.

*Texto alternativo já no código:* Módulo de hospedagem integrado à vegetação

### `paisagem-amanhecer`

**index.html** · Banda full bleed · 21:9 panorâmico

Primeira luz sobre o vale, névoa baixa, contraluz. Muito espaço negativo na metade superior para a headline respirar.

*Texto alternativo já no código:* Amanhecer sobre o vale, primeira luz atravessando a névoa

### `hero-terreno`

**development.html** · Hero · tela cheia · 21:9 ou mais largo

Terreno com vocação turística, luz rasante, relevo desenhado pela sombra. Nenhuma construção no quadro.

*Texto alternativo já no código:* Território aberto ao entardecer, antes de qualquer construção

### `banda-implantacao`

**development.html** · Banda full bleed · 21:9 panorâmico

Implantação em curso: estrutura modular sendo montada no terreno, sem poeira de canteiro pesado. Mostra baixo impacto.

*Texto alternativo já no código:* Obra de implantação integrada ao terreno, estrutura modular sendo montada

### `development-masterplan`

**development.html** · Duo editorial · 3:4 retrato

Master plan sobre a mesa, com o território ao fundo pela janela. Papel, lápis, luz natural. O projeto e a terra no mesmo quadro.

*Texto alternativo já no código:* Master plan impresso sobre a mesa, com o território visível ao fundo

### `hero-servico`

**management.html** · Hero · tela cheia · 21:9 ou mais largo

Serviço acontecendo: mesa posta ao amanhecer, vapor do café, textura de linho e madeira. Escala íntima.

*Texto alternativo já no código:* Mesa posta ao amanhecer, serviço em operação

### `banda-operacao`

**management.html** · Banda full bleed · 21:9 panorâmico

Experiência, não equipamento: pessoa em silêncio na água quente olhando a montanha. Vapor, contraluz, fim de tarde.

*Texto alternativo já no código:* Hóspede na jacuzzi olhando as montanhas ao entardecer

### `management-equipe`

**management.html** · Duo editorial · 3:4 retrato

Equipe em operação, gesto de serviço real — arrumação, preparo, recepção. Pessoas de verdade, sem pose.

*Texto alternativo já no código:* Equipe da operação em serviço, gesto real de trabalho

### `hero-collection`

**collection.html** · Hero · tela cheia · 21:9 ou mais largo

A bandeira em uma imagem: Bubble Suite sob céu estrelado, luz quente por dentro, silhueta da mata em volta.

*Texto alternativo já no código:* Bubble Suite sob céu estrelado, luz quente por dentro

### `banda-collection`

**collection.html** · Banda full bleed · 21:9 panorâmico

A bandeira vista de longe: unidade acesa entre a mata ao anoitecer. Escala pequena dentro do território.

*Texto alternativo já no código:* Bubble Suite ao anoitecer entre a vegetação, luz interna quente

### `collection-detalhe`

**collection.html** · Duo editorial · 3:4 retrato

Detalhe material da bandeira: enxoval, amenidade, madeira, cerâmica. Macro, luz suave, fundo escuro.

*Texto alternativo já no código:* Detalhe de enxoval e amenidades no padrão da bandeira

### `hero-capital`

**capital.html** · Hero · tela cheia · 21:9 ou mais largo

Vista aérea baixa da operação: unidades pequenas dentro do território, mostrando escala e baixo impacto.

*Texto alternativo já no código:* Vista aérea da operação integrada à paisagem

### `banda-preservacao`

**capital.html** · Banda full bleed · 21:9 panorâmico

Área de preservação com a estrutura leve pousada nela, sem fundação aparente. Vegetação intacta no primeiro plano.

*Texto alternativo já no código:* Vegetação preservada em volta da estrutura leve, vista do solo

### `capital-operacao`

**capital.html** · Duo editorial · 3:4 retrato

Operação cheia em alta temporada: unidades acesas ao anoitecer, vista de drone baixo. Prova de ocupação.

*Texto alternativo já no código:* Unidades acesas ao anoitecer em alta temporada

### `hero-bruno`

**bruno.html** · Hero · tela cheia · 21:9 ou mais largo

Retrato de Bruno em campo — não em escritório. Luz natural, meio corpo, território ao fundo desfocado.

*Texto alternativo já no código:* Bruno Chaerk em campo, no território

### `banda-territorio`

**bruno.html** · Banda full bleed · 21:9 panorâmico

Leitura territorial acontecendo: figura caminhando na paisagem, escala humana pequena, luz do início da manhã.

*Texto alternativo já no código:* Bruno caminhando no território em leitura de campo

### `bruno-campo`

**bruno.html** · Duo editorial · 3:4 retrato

Bruno em campo com o cliente ou a equipe, conversa acontecendo no terreno. Documental, sem pose.

*Texto alternativo já no código:* Bruno Chaerk em conversa de campo no território

## Vídeo do hero (opcional)

`hero.mp4` e `hero.webm` nesta pasta ligam o vídeo da home automaticamente, por cima da fotografia. Sem eles, a fotografia assume; sem fotografia, ficam as curvas de nível.

```bash
ffmpeg -i original.mp4 -t 20 -vf "scale=1920:-2" -an -c:v libx264 -crf 29 -preset slow -movflags +faststart hero.mp4
```

Duração de 10 a 25s em loop, sem áudio, sem corte brusco entre fim e início.

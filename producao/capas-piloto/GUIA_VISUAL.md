# Guia visual · capas dos conteúdos Zion (piloto)

Versão piloto de 09/11/2026 · Para aprovação do Bruno. Nada publicado.

## 1. Princípio

Uma coleção, três peças:
- a **imagem** muda conforme o tema;
- a **moldura** (logo, tipografia, dourado, degradê musgo e posição dos textos) é sempre a mesma.

As imagens não trazem texto. Todo texto é aplicado pelo script de composição, com as fontes oficiais.

## 2. Cores

| Uso | Cor | Código |
|---|---|---|
| Fundo e degradê (verde musgo profundo) | Musgo | `#16261C` (degradê de 97% a 12% de opacidade) |
| Títulos | Areia clara | `#F5F1E8` |
| Linha de apoio, subtítulo, rodapé, barra | Dourado discreto | `#E0BE5E` |
| Áreas claras (capas de aula, se houver) | Bege | `#F5F1E8` / `#ECE6DA` |

As cores vêm das capas atuais da Trilha 1 e da Jornada 2 (`producao/jornada2/00-marco-zero/src/build_capas.js`) e do tema dos portais no ClickMax (dourado de destaque `#C9A84C`).

## 3. Tipografia

| Elemento | Fonte | Estilo |
|---|---|---|
| Título (2 linhas) | Cormorant | 1ª linha regular, 2ª linha itálica |
| Subtítulo | Cormorant | Itálico, dourado |
| Linha de apoio (trilha ou produto) e rodapé | Aventa | Maiúsculas, negrito, espaçamento de 0,2 em, dourado |

As fontes ficam em `docs/assets/fonts/` e vão embutidas na composição.

## 4. Composição

| Elemento | Horizontal 1920×1080 | Vertical 1080×1620 |
|---|---|---|
| Margem | 110 px (topo e base) e 128 px (laterais) | 100 px e 84 px |
| Logo oficial (`docs/brand/zion-logo-claro.png`) | Canto superior esquerdo, 96 px de altura | Canto superior esquerdo, 88 px |
| Bloco de texto | Esquerda, centralizado na altura | Centro-baixo |
| Título | 172 px | 122 px |
| Barra dourada | 150 × 5 px | 150 × 5 px |
| Subtítulo | 58 px | 50 px |
| Rodapé "Zion Hospitality Business" | Base esquerda, 22 px | Base esquerda, 21 px |
| Degradê musgo | Da esquerda (escuro) para a direita (foto aparente) | De baixo (escuro) para cima (foto aparente) |
| Assunto da imagem | Metade direita | 40% superiores |

**Código do módulo** (D01, F03…), quando houver: na linha de apoio, antes do nome da trilha (ex.: "D01 · Trilha 1 · Desenvolvimento"). Nas três capas-piloto não se aplica.

## 5. Regras das imagens

- Fotografia realista e cinematográfica, luz natural (golden hour ou nublado suave), baixa saturação.
- Arquitetura contemporânea integrada à natureza: madeira, vidro, pedra, volumes baixos.
- Temas do setor: terreno, paisagem, hospedagem, gestão.
- Nada de texto, números, placas, logotipos, marcas d'água, molduras ou interface na imagem.
- Evitar: aparência de banco de imagens, ilustração, render 3D artificial, HDR, cores saturadas, efeitos.
- Pessoas, quando houver: de costas ou de perfil, sem foco no rosto.
- Área reservada calma e escura: metade esquerda (horizontal) ou 60% inferiores (vertical).

## 6. Formatos (medidos nos arquivos atuais)

| Uso no ClickMax | Tamanho atual medido | Exemplo |
|---|---|---|
| Capa de curso, horizontal | 1920×1080 | `docs/trilha1/capas/curso-h.jpg` |
| Capa de curso, vertical | 1080×1620 | `docs/trilha1/capas/curso-v.jpg` |
| Capa de módulo, horizontal | 1280×720 | `docs/trilha1/capas/mz-h.jpg`, `docs/trilha2/capas/g0-h.jpg` |
| Capa de módulo, vertical | 720×1080 | `docs/trilha1/capas/mz-v.jpg`, `docs/trilha2/capas/g0-v.jpg` |
| Capa de e-book, vertical | 800×1200 | `docs/escola/capas/d01-v.png` |

- Todos usam as proporções 16:9 (horizontal) e 2:3 (vertical).
- A documentação pública do ClickMax não informa dimensões obrigatórias: a busca na central de ajuda não encontrou nada. Por isso, valem as medidas dos arquivos já em uso.
- As capas-piloto saem no tamanho de curso (1920×1080 e 1080×1620). Para módulo e e-book, basta reduzir, porque a proporção é a mesma.

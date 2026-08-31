# DESIGN.md — Site Zion Hotel Group International

> Contexto de design do site em `docs/`. O detector do Impeccable lê este arquivo.
> Verificar com: `impeccable detect docs/`

---

## Lane

**Brand.** Site institucional de um grupo de desenvolvimento hoteleiro. O público é
proprietário de terra, investidor e parceiro — não usuário de produto. A página existe para
criar autoridade e gerar diagnóstico, não para operar tarefas.

## Voz

Direta e proprietária. Frase curta, afirmação sem hedge. Nada de linguagem de release.
Referência de tom: "Enquanto o mercado constrói hotéis, nós estruturamos ativos."

## Anti-referências

Nada de SaaS genérico: sem gradiente roxo-azul, sem card dentro de card, sem ícone em
quadradinho arredondado acima de cada título, sem Inter em tudo, sem eyebrow chip em caixa
alta acima do H1.

---

## Cor

| Token | Valor | Uso |
|---|---|---|
| `--black` | `#040605` | Fundo principal |
| `--green` | `#1B2117` | Fundo secundário escuro |
| `--cream` | `#FEF5F0` | Texto sobre escuro · fundo claro |
| `--sand` | `#DED6BF` | Texto de apoio sobre escuro |
| `--earth` | `#866D4B` | **Fundo** dourado (botão, seleção) com creme em cima |
| `--earth-light` | `#A0825A` | **Texto** dourado sobre fundo escuro · bordas |
| `--earth-deep` | `#6F5A3E` | **Texto** dourado sobre fundo claro (creme, areia) |

### Por que três dourados

O site tinha um `--earth: #8B714E` único, usado ao mesmo tempo como texto sobre preto, texto
sobre creme e fundo de botão. Ele falhava WCAG AA nos **quatro** usos — 4,42 · 4,27 · 4,27 ·
3,17 contra o mínimo de 4,5:1.

Não era erro de escolha, era erro de estrutura: texto claro sobre dourado quer dourado
escuro, e dourado como texto sobre preto quer dourado claro. Um token só não serve os dois.
Os três tons ficam no mesmo matiz (34,4°), então a marca não muda — o que muda é a
luminância, por função.

Contraste verificado:

| Combinação | Razão |
|---|---|
| `--earth-light` sobre preto | 5,65:1 |
| `--earth-light` sobre verde | 4,57:1 |
| creme sobre `--earth` | 4,54:1 |
| `--earth-deep` sobre creme | 6,09:1 |
| `--earth-deep` sobre areia | 4,51:1 |

Ao criar qualquer combinação nova, calcular antes. O piso é 4,5:1 para texto e 3:1 para
contorno.

---

## Tipografia

**Cormorant Garamond** para títulos e números de destaque. **Aventa** para texto e interface.

### Escala

Degraus distintos, não uma faixa contínua de tamanhos quase iguais:

- **12px** — rótulo, meta, navegação, legenda
- **16px** — texto corrido
- **20px** — destaque, lead
- **`clamp()`** — títulos, de 34px a 120px conforme a viewport

Piso absoluto: **12px** para qualquer texto funcional ou de corpo. Não existe 10,5px, nem
9,5px, nem 11px. Adicionar um tamanho menor à escala não resolve o problema de leitura —
apenas registra o problema como token.

### Caixa alta e tracking andam juntos

A regra que organiza a identidade tipográfica do site:

> **Caixa alta é para rótulo curto.** Até cerca de 26 caracteres — "MODALIDADES", "CONTATO",
> "MÉTODO". Aí o tracking largo (0,26em a 0,34em) é obrigatório: maiúscula precisa de ar.
>
> **Frase não leva caixa alta.** Acima de 26 caracteres, texto normal com tracking de no
> máximo 0,04em. Reconhecemos palavra pela forma — ascendente e descendente — e a caixa alta
> apaga essa forma.

As duas propriedades são acopladas. Remover o `text-transform: uppercase` e deixar o
`letter-spacing: 0.34em` produz texto pior que o original: o tracking existia para dar ar à
maiúscula, e sem ela vira ruído entre as letras. Ao mexer em uma, mexa na outra.

Classes:

- `.label` — rótulo curto, caixa alta, tracking largo
- `.label-line` — linha longa, caixa normal, tracking 0,04em, mesma cor e peso
- `.sig-line` — assinatura institucional, abaixo do bloco do herói

---

## Layout

- Contêiner: `1140px`, com `6vw` de respiro lateral
- Seção: `150px` de respiro vertical
- Bloco com borda ou fundo visível: mínimo `24px` de inset. Filho encostado na linha da borda
  é erro, não densidade.

## Herói

Sem eyebrow acima do H1. A assinatura institucional ("Zion Hotel Group International ·
Florianópolis · Barcelona") vive **depois** do bloco de CTAs, como `.sig-line`. Um rótulo em
caixa alta com tracking imediatamente acima de um título grande é o herói padrão de SaaS
gerado por IA — e a informação já está no nav e no rodapé.

## Hierarquia de títulos

Sem pular nível: `h2` é seguido de `h3`, nunca de `h4`. O nível do título é estrutura de
documento, não escolha de tamanho — para tamanho existe classe.

## Movimento

Fade de entrada com `cubic-bezier(.16,1,.3,1)`, 1,2s. Deriva lenta das linhas topográficas,
26s. Tudo respeita `prefers-reduced-motion`.

---

## Exceção registrada

`bruno.html` desliga `flat-type-hierarchy` com ignore inline documentado. A escala real da
página vai de 12px a 120px via `clamp()` nos títulos; a regra só enxerga os px fixos
(12/16/20) e por isso a lê como plana. Inflar um tamanho fixo para satisfazer a métrica
maquiaria o token sem mudar a hierarquia.

Toda exceção futura segue o mesmo padrão: ignore inline, no arquivo, com a razão escrita.
Ignore sem justificativa é dívida silenciosa.

---

## Estado

`impeccable detect docs/` passa com zero achados nas cinco páginas. Rodar antes de cada
publicação — o detector é determinístico e não precisa de chave de API.

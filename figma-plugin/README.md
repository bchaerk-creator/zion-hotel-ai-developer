# Zion · Site Generator (plugin de Figma)

Desenha o site institucional da Zion Hotel Group International **dentro do Figma**:
design system completo + as 5 páginas em Desktop 1440 e Mobile 390, em auto-layout
nativo e 100% editável.

Não é screenshot, nem imagem importada: cada headline é um nó de texto, cada CTA é
uma instância de componente, e as bandas territoriais são os mesmos vetores de curva
de nível usados em `docs/`.

---

## Como instalar (2 minutos)

O plugin roda no **app de desktop do Figma** (o navegador não abre plugins locais).

1. Baixe esta pasta `figma-plugin/` para o seu computador.
2. Abra o Figma Desktop → menu **Plugins → Development → Import plugin from manifest…**
3. Selecione o arquivo `figma-plugin/manifest.json`.
4. Abra (ou crie) um arquivo do Figma e rode **Plugins → Development → Zion · Site Generator**.
5. Escolha as páginas e os breakpoints e clique em **Gerar Site**.

O plugin cria uma página nova chamada **Zion · Site** e leva a tela até ela quando termina.

---

## O que é gerado

### `00 · Fundamentos`
- **Paleta oficial** publicada como *paint styles* (`Zion/Zion Black`, `Zion/Zion Cream`, …)
  e também como **variáveis de cor** na coleção `Zion · Cores`. Os estilos ficam
  amarrados às variáveis: trocar a variável repinta o site inteiro.
- **11 estilos de texto** (`Zion/Display/Hero`, `Zion/Texto/Corpo`, `Zion/Rótulo/Overline`, …)
  com espécime lado a lado das specs.

### `01 · Componentes`
23 componentes, com variantes onde o layout muda de verdade:

| Componente | Variantes |
|---|---|
| Botão | Estilo (Sólido · Contorno) × Tema (Escuro · Claro) |
| Nav | Tipo (Home · Interna · Mobile) |
| Rodapé | Tipo (Institucional · Simples) × Breakpoint |
| Bloco de Processo | Breakpoint (Desktop · Mobile) |
| Ato da Jornada | Breakpoint |
| Etapa do Método | Breakpoint |
| Projeto | Breakpoint |
| Indicador, Linha de Especificação, Célula, Item de FAQ | — |

As páginas usam **instâncias** desses componentes. Editar o componente-mestre
propaga para as 10 páginas de uma vez.

### `02 · Páginas · Desktop 1440` e `03 · Páginas · Mobile 390`
- Home · Grupo (hero, números vivos, manifesto, banda territorial, 3 modalidades,
  jornada em 6 atos, ecossistema, método Pirâmide Invertida©, Zion Score,
  projetos, founder, FAQ, CTA final com o form do HubSpot desenhado)
- Modalidade 01 · Development
- Modalidade 02 · Management
- Modalidade 03 · Collection
- Founder · Bruno Chaerk

Toda a copy vem de `docs/*.html` — o Figma e o site publicado dizem exatamente a
mesma coisa.

---

## Fontes

| Papel | Fonte do site | No Figma |
|---|---|---|
| Display | Cormorant Garamond | vem do Google Fonts, já disponível |
| Texto | **Aventa** | fonte comercial (Fontfabric) |

Se a Aventa não estiver instalada na sua máquina, o plugin cai automaticamente
para **DM Sans** — o mesmo fallback declarado no CSS do site — e avisa isso na
mensagem final. Para ter fidelidade total, instale a Aventa no sistema antes de
rodar (o Figma Desktop lê as fontes locais) e gere de novo.

A pilha completa, na ordem de tentativa:

- Display: Cormorant Garamond → Cormorant → EB Garamond → Playfair Display → Georgia
- Texto: Aventa → DM Sans → Outfit → Jost → Inter

---

## Equivalências entre o CSS e o Figma

O gerador traduz as regras do site, não aproxima no olho:

- `clamp(min, Xvw, max)` vira o valor calculado para a largura de cada frame
  (por exemplo, a H1 do hero: 110px no 1440 e 46px no 390)
- `.wrap{max-width:1140px; padding:0 6vw}` vira padding de `max(6vw, (W-1140)/2)`
- `line-height` e `letter-spacing` viram porcentagem do corpo da fonte
- Grades de 2 colunas viram 1 coluna abaixo de 700px, como nas media queries
- Caixa alta é aplicada como propriedade (`textCase`), não no conteúdo: o texto
  continua editável na forma original

---

## Limites conhecidos

- Sem fotografia: os heros usam as curvas de nível, iguais ao site. Os slots estão
  prontos para receber a fotografia editorial (drone, bubble ao anoitecer) por cima.
- As animações do site (fade ao rolar, contagem dos números, deriva das curvas,
  vídeo do hero) não existem no Figma — o estado desenhado é o estado final.
- O formulário do HubSpot é desenhado como mock; no site é um embed.
- Estilos de texto são publicados no arquivo, mas não aplicados nó a nó, porque o
  mesmo papel tipográfico muda de corpo entre desktop e mobile.

---

## Desenvolvimento

`code.js` não tem etapa de build: é JavaScript puro, lido direto pelo Figma.

A estrutura segue a ordem: tokens → fontes → helpers de nó → design system →
componentes → seções → páginas → `run()`.

Para mudar a copy, edite o objeto `PAGES` (e as constantes `MODALIDADES`,
`JORNADA`, `ECOSSISTEMA`, `METODO`, `PROJETOS`, `FAQ`) no topo do arquivo:
é a mesma fonte de verdade usada por todas as seções.

# Relação dos arquivos · capas-piloto

09/11/2026 · **Prévias para aprovação. Nada foi publicado nem enviado ao ClickMax.**

## No repositório (só documentação e script)

| Arquivo | O que é |
|---|---|
| `producao/capas-piloto/compor_pilotos.js` | Script novo de composição das capas-piloto. Segue o método das capas atuais (HTML + Playwright, Cormorant, Aventa, musgo e dourado, logo oficial) **sem alterar** os programas existentes (`producao/jornada2/*/src/build_capas.js`, `producao/utilitarios/render_capas.js`, `producao/ferramentas/gerar_capas.py`) |
| `producao/capas-piloto/PROMPTS_GERACAO.md` | Prompts das 3 imagens de fundo para o gerador externo (não executados) |
| `producao/capas-piloto/GUIA_VISUAL.md` | Cores, tipografia, composição, regras das imagens e formatos |
| `producao/capas-piloto/RELACAO_ARQUIVOS.md` | Esta relação |

## Fora do repositório (entregues ao Bruno para revisão)

As imagens ficam fora do repositório público e fora de `docs/`, que vai para o GitHub Pages, para não serem publicadas antes da aprovação.

| Arquivo | Tamanho | Conteúdo |
|---|---|---|
| `01-desenvolvimento-h-provisoria.jpg` | 1920×1080 | Capa composta, fundo provisório |
| `01-desenvolvimento-v-provisoria.jpg` | 1080×1620 | idem |
| `02-gestao-h-provisoria.jpg` | 1920×1080 | idem |
| `02-gestao-v-provisoria.jpg` | 1080×1620 | idem |
| `03-land-bank-h-provisoria.jpg` | 1920×1080 | idem |
| `03-land-bank-v-provisoria.jpg` | 1080×1620 | idem |
| `*-fundo-sem-texto-provisorio.jpg` (6) | mesmos tamanhos | Só o fundo, no mesmo enquadramento (é o que o gerador deve entregar, sem texto) |
| `lado-a-lado-horizontal.jpg`, `lado-a-lado-vertical.jpg` | — | As três capas lado a lado, para comparar a consistência |
| `pacote-capas-piloto-gpt.zip` | — | Pacote para o gerador: prompts, guia visual, guias de área segura e referência da composição final |

## Fundos provisórios (fotos próprias da Zion já existentes no repositório)

| Capa | Foto usada | Resolução original | Observação |
|---|---|---|---|
| Desenvolvimento | `docs/trilha1/apresentacao/fotos/c8d0eb086b.jpg` (aérea de uma unidade no meio da floresta) | 1200×800 | Ampliada 1,6× para 1920×1080: serve para a prévia, não para a versão final |
| Gestão | `docs/land-members/img/zion-bubble-interior-original.jpg` (interior de hospedagem boutique) | 1280×1600 | **Não atende ao conceito** (não há gestor nem notebook). Precisa da imagem gerada |
| Land Bank | `docs/trilha1/apresentacao/fotos/901904223c.jpg` (vale com araucárias e montanhas) | 1179×1362 | A vertical mostra uma pessoa deitada no deck, no terço inferior. Precisa da imagem gerada ou de outra foto |

**Os fundos provisórios só mostram a moldura.** As imagens definitivas dependem do gerador externo (`PROMPTS_GERACAO.md`), que só será usado com autorização.

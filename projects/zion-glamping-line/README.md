# ZION COCOON e ZION ZENITH · Linha de hospedagens glamping de luxo

Projeto conceitual, arquitetônico e técnico de dois produtos proprietários da Zion Glamping Collection (Zion Hotel Group International), desenvolvidos como unidades de hospedagem premium para glampings, boutique hotels e destinos de natureza.

| Produto | Conceito | Dimensões | Área |
|---|---|---|---|
| **ZION COCOON** | Cabana biomórfica em casulo: superelipse assimétrica com lábio frontal inclinado, Espinha de Luz na cumeeira e seis Janelas Olho em lente | Piso 9,00 x 5,74 m · concha 9,55 x 5,90 x 3,95 m | 41 m² internos + vestíbulo 2,5 m² + deck 26 m² = 71,5 m² |
| **ZION ZENITH** | Cabana escultural de dois cumes assimétricos em diagonal (5,80 e 4,60 m), Óculo do Zênite sobre a cama e chaminé do Respiro | Corpo 9,50 x 5,40 x 2,75 m · cobertura 12,90 x 7,40 m | 48,4 m² internos + terraço 20,4 m² + passarela 7,6 m² = 79,3 m² |

## Documento principal

- **`ZION_COCOON_ZENITH_Caderno_Tecnico.html`** — Caderno Técnico com os 27 entregáveis (abrir no navegador; referencia os desenhos e renders das pastas abaixo).
- **`ZION_COCOON_ZENITH_Caderno_Tecnico.pdf`** — a mesma publicação em PDF (A4 paisagem).
- **`ESPECIFICACAO_TECNICA.md`** — especificação-fonte compartilhada (dimensões, materiais, estrutura, sistemas, transporte e montagem).

## Estrutura de pastas

```
projects/zion-glamping-line/
├── cocoon/
│   ├── desenhos/   02 planta humanizada · 03 planta técnica · 04 elevação frontal · 05 elevação lateral
│   │               06 corte longitudinal · 07 corte transversal · 08 isométrica · 12 estrutura (isométrica)
│   ├── 3d/         zion-cocoon-3d.html (visualizador interativo Three.js) · zion-cocoon.glb
│   └── renders/    renders externos (frontal, lateral, cauda, aérea, noite), internos (estar, cama, banho), estrutura, corte
├── zenith/         mesma estrutura
├── detalhes/       DET-01 a DET-11: cobertura, ancoragem, fundação, esquadrias, drenagem, elétrica, hidráulica,
│                   climatização, arcos (Cocoon), mastros (Zenith)
├── tools/          geradores: geometry.py (fonte única da geometria), drawings_*.py, iso.py, details.py, bom.py,
│                   build_viewer.py, render.js, build_dossier.py, export_pdf.js
└── assets/         fontes Aventa e Cormorant Garamond (identidade Zion)
```

## Mapa dos 27 entregáveis

| # | Entregável | Onde |
|---|---|---|
| 1 | Conceito arquitetônico | Caderno, seção 01 · `ESPECIFICACAO_TECNICA.md` |
| 2 | Planta baixa humanizada | `*/desenhos/02_planta_humanizada.svg` |
| 3 | Planta técnica com dimensões | `*/desenhos/03_planta_tecnica.svg` |
| 4 | Elevação frontal | `*/desenhos/04_elevacao_frontal.svg` |
| 5 | Elevação lateral | `*/desenhos/05_elevacao_lateral.svg` |
| 6 | Corte longitudinal | `*/desenhos/06_corte_longitudinal.svg` |
| 7 | Corte transversal | `*/desenhos/07_corte_transversal.svg` |
| 8 | Vista isométrica | `*/desenhos/08_isometrica.svg` |
| 9 | Modelo 3D | `*/3d/*.html` (interativo) e `*/3d/*.glb` |
| 10 | Renderizações externas | `*/renders/*_ext_*.png`, `*_night.png` |
| 11 | Renderizações internas | `*/renders/*_int_*.png` |
| 12 | Estudo da estrutura metálica | `*/desenhos/12_estrutura_isometrica.svg` + Caderno, seção 12 |
| 13 | Sistema de arcos / perfis | `detalhes/DET-10_arcos_cocoon.svg`, `detalhes/DET-11_mastros_zenith.svg` |
| 14 | Detalhe do sistema de cobertura | `detalhes/DET-01_cobertura_cocoon.svg`, `DET-02_cobertura_zenith.svg` |
| 15 | Detalhe de ancoragem | `detalhes/DET-03_ancoragem.svg` |
| 16 | Sistema de fundação | `detalhes/DET-04_fundacao.svg` |
| 17 | Detalhe de portas e janelas | `detalhes/DET-05_esquadrias.svg` |
| 18 | Sistema de drenagem | `detalhes/DET-06_drenagem.svg` |
| 19 | Instalação elétrica | `detalhes/DET-07_eletrica.svg` |
| 20 | Sistema hidráulico | `detalhes/DET-08_hidraulica.svg` |
| 21 | Ar-condicionado e aquecimento | `detalhes/DET-09_climatizacao.svg` |
| 22 | Lista preliminar de materiais | Caderno, seção 22 (gerada por `tools/bom.py`) |
| 23 | Componentes para fabricação | Caderno, seção 23 |
| 24 | Estimativa de peso | Caderno, seção 24 |
| 25 | Sistema de transporte | Caderno, seção 25 |
| 26 | Sequência de montagem | Caderno, seção 26 |
| 27 | Tempo estimado de instalação | Caderno, seção 27 |

## Regenerar tudo

```bash
cd projects/zion-glamping-line/tools
pip install numpy            # única dependência Python
python3 drawings_cocoon.py && python3 drawings_zenith.py && python3 iso.py && python3 details.py
python3 build_viewer.py      # visualizadores 3D
NODE_PATH=/opt/node22/lib/node_modules node render.js      # renders PNG + GLB (Playwright + Chromium)
python3 build_dossier.py     # Caderno Técnico HTML
python3 build_dossier.py --inline   # versão autônoma com imagens embutidas
NODE_PATH=/opt/node22/lib/node_modules node export_pdf.js   # PDF
```

Toda a geometria (planta, seções, arcos, cumes, layout) vem de `tools/geometry.py`. Alterar um parâmetro ali e regenerar atualiza desenhos, isométricas, modelo 3D, renders e listas de materiais de forma consistente.

## Estado do projeto

Estudo preliminar / projeto conceitual. Antes da fabricação: cálculo estrutural com ART, form-finding da membrana com o fabricante, projeto executivo de esquadrias e instalações, protótipo no Zion Bubble Glamping. Ver Caderno, anexo A.

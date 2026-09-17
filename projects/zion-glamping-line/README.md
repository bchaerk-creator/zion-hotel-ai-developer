# ZION CASULO, ZION SAFARI, ZION LODGE (38, 24 e 28) e ZION CÁPSULA · Linha de hospedagens glamping de luxo

Projeto conceitual, arquitetônico e técnico de seis unidades proprietárias da Zion Glamping Collection (Zion Hotel Group International), desenvolvidos como unidades de hospedagem premium para glampings, boutique hotels e destinos de natureza.

| Produto | Conceito | Dimensões | Área |
|---|---|---|---|
| **ZION CASULO** | Cabana biomórfica em casulo: superelipse assimétrica com lábio frontal inclinado, Espinha de Luz na cumeeira e seis Janelas Olho em lente | Piso 9,60 x 5,86 m · concha 9,75 x 6,00 x 4,20 m | 45,6 m² internos + vestíbulo 2,4 m² = 48 m² + deck 29,9 m² = 78 m² |
| **ZION SAFARI** | Cabana escultural de dois cumes assimétricos em diagonal (5,80 e 4,60 m), Óculo do Zênite sobre a cama e chaminé do Respiro | Corpo 9,50 x 5,40 x 2,75 m · cobertura 12,90 x 7,40 m | 48,4 m² internos + terraço 20,4 m² + passarela 7,6 m² = 79,3 m² |
| **ZION LODGE 38** | Pavilhão octogonal com Lanterna Zion (luz zenital sobre a cama), cinco faces de vidro, banho no segmento posterior e vela de sombra sobre o deck | Octógono 6,80 m entre faces · beiral 2,70 m · lanterna 5,20 m | 38,3 m² internos + deck 30,4 m² = 68,7 m² |
| **ZION LODGE 24** (conceito) | Octógono compacto para casal: três faces de vidro voltadas à paisagem, cinco opacas, lanterna Ø1,20, deck de uma face | Octógono 5,40 m entre faces · beiral 2,60 m · lanterna 4,70 m | 24,2 m² internos + deck 6,1 m² = 30,3 m² |
| **ZION LODGE 28** (conceito) | Octógono alongado com duas Lanternas Zion em cumeeira (cama e estar), cinco faces de vidro, banho no fundo, terraço em três faces | 4,20 x 7,80 m · beiral 2,60 m · lanternas a 4,45 m | 29,7 m² internos + terraço 17,5 m² = 47,2 m² |
| **ZION CÁPSULA** (conceito) | Cápsula monocoque transportável: casca de alumínio composto sobre 12 anéis, Visor (calota frontal inteira em vidro curvo), Anel de Luz sobre a cama, dois Olhos, compartimento técnico na cauda; chega pronta da fábrica e pousa em quatro pés | 8,40 x 3,20 x 3,20 m · piso a 1,05 m · topo a 3,50 m | 19,9 m² internos + deck 8,3 m² = 28,2 m² |

Nomes comerciais: **Zion Casulo** (código interno `cocoon`, prefixo ZC), **Zion Safari** (código interno `zenith`, prefixo ZS), **Zion Lodge** (`lodge`) e **Zion Cápsula** (`capsule`, prefixo ZK). As pastas e identificadores de código mantêm os nomes internos; títulos, carimbos e documentos usam os nomes comerciais. O Lodge 38 tem desenhos, pranchas PA, DXF, isométricas, modelo 3D, renders e orçamento peça a peça; o Lodge 24 e o Lodge 28 são variantes paramétricas da mesma classe (`geometry.Lodge24`, `geometry.Lodge28`) com prancha de conceito e isométrica (`tools/lodge_family.py`) e estimativa paramétrica de custo. A Cápsula (`geometry.Capsule`, `tools/capsule.py`) tem prancha de conceito (planta, corte, seção, fachada), isométrica, FF&E e lista de materiais estimados a partir da geometria.

**Marca.** O símbolo Z da Zion (anel + Z, `svgkit.zion_mark`) aparece em todos os desenhos: cabeçalho e carimbo de cada folha SVG e detalhe, capa PA-00, títulos dos DXF, capas dos documentos e canto inferior direito dos renders (`tools/brand_renders.py`).

## Método de trabalho (Cabin Design & Engineering System)

O projeto segue o master prompt arquivado em `00_BRIEFING/MASTER_PROMPT.md`, resumido em `CLAUDE.md` (regras do projeto): 12 fases, pacote final em 23 pastas, códigos `<modelo>-<disciplina>-<nnn>`, revisões REV 00 a REV 04, avisos `⚠️ VALIDAÇÃO OBRIGATÓRIA — ENGENHEIRO/ARQUITETO` e `PREÇO A COTAR`. A Fase 01 está em **`00_BRIEFING/ZG-BRF-001_ZION_CABIN_DESIGN_BRIEF.md`** (`.pdf`): ficha técnica das seis unidades, informações necessárias, mapa das 23 pastas contra o que já existe e as 15 perguntas objetivas que destravam as fases seguintes.

## Documentos principais

> **Documentos sem preços.** Todos os HTML/PDF desta pasta são documentos técnicos para a fábrica e para cotação: projeto arquitetônico, camadas, especificação e quantidades estimadas de materiais e FF&E, sem valores. As referências de preço ficam apenas nos arquivos internos da pasta `interno/`.

- **`ZION_CATALOGO_LINHA.pdf`** e **`.html`** — Catálogo da linha: as seis unidades com dados, imagens, desenhos, as 13 camadas com especificação de materiais, quadro de materiais estimados (quantidades) e **FF&E completo (tudo o que vai dentro: mobiliário, luminárias, equipamentos, enxoval, deck e banho)** por unidade. `ZION_MATERIAIS_FFE_Linha.xlsx` traz as mesmas listas em planilha (materiais por produto + FF&E por unidade + catálogo de itens); a base de dados do FF&E está em `tools/ffe.py`.
- **`ZION_PROJETO_ARQUITETONICO.pdf`** (vetorial) e **`.html`** — Projeto arquitetônico como um projetista entrega, para Casulo, Safari e Lodge 38: 24 pranchas por produto (PA-00 capa/índice/quadro de áreas/notas · PA-01 implantação 1:200 · PA-02 planta cotada · PA-03 layout · PA-04 cobertura · PA-05 forro e iluminação · PA-06 cortes A-A e B-B · PA-07 fachadas frontal e traseira · PA-08 fachadas laterais · PA-09 quadro de esquadrias · PA-10 planta estrutural · PA-11 detalhes construtivos · PA-12 isométrica, explodida, camadas e estrutura) mais **PA-13 camadas construtivas e especificação de materiais** e **PA-14 quadro de materiais estimados (quantidades, sem preços)**, uma por página A3 paisagem. `ZION_PROJETO_ARQUITETONICO_standalone.html` é a versão autônoma (tudo embutido, com hachuras).
- **`cocoon/projeto/dxf/` e `zenith/projeto/dxf/`** — 21 arquivos DXF (AutoCAD 2010, metros, layers PAREDES / ESQUADRIAS / MOBILIARIO / ESTRUTURA / COBERTURA / DECK / FUNDACAO / COTAS / TEXTO / EIXOS): plantas cotada e de layout, cobertura, cortes, fachadas, planta estrutural e modelo 3D (3DFACE + polilinhas 3D) de cada produto.
- **`ZION_ARCHITECTURAL_PRODUCT_BOOK.html`** e **`.pdf`** — Product Book industrial em três volumes (Casulo, Safari e Lodge 38): conceito, master plan, engenharia peça a peça, sistema de encaixe, camadas, memorial, BOM com quantidades estimadas, manual de montagem em 17 passos, horas por função, cronograma e escala industrial. Sem preços.
- **`ZION_ARCHITECTURAL_PRODUCT_BOOK_leve.pdf`** — mesma edição com imagens recomprimidas (≈ 9,5 MB) para envio por e-mail/WhatsApp; gerada com `python3 tools/pdf_leve.py`.
- **`interno/referencias/`** e **`interno/ZION_REFERENCIA_NOMASTRA_H28.{html,pdf,xlsx}`** — cotação de fornecedor (NOMASTRA H28, mai/2025) usada como referência de mercado da Zion Lodge 28, com análise interna de custo posto (câmbio, frete e tributos como premissas ajustáveis em `tools/referencias.py`). O comparativo técnico sem preços aparece no catálogo (página do Lodge 28) e na apresentação.
- **`interno/ZION_ORCAMENTO_SC_Casulo_Safari_Lodge.xlsx`** — planilha interna de orçamento (com preços de referência SC): peças, conexões, BOM em 3 cenários, mão de obra, resumo, escala e premissas. Não faz parte dos documentos enviados à fábrica.

- **`ZION_CASULO_SAFARI_Caderno_Tecnico.html`** — Caderno Técnico com os 27 entregáveis (abrir no navegador; referencia os desenhos e renders das pastas abaixo).
- **`ZION_CASULO_SAFARI_Caderno_Tecnico.pdf`** — a mesma publicação em PDF (A4 paisagem).
- **`ESPECIFICACAO_TECNICA.md`** — especificação-fonte compartilhada (dimensões, materiais, estrutura, sistemas, transporte e montagem).

## Estrutura de pastas

```
projects/zion-glamping-line/
├── cocoon/
│   ├── desenhos/   02 planta humanizada · 03 planta técnica · 03b planta estrutural · 04 elevação frontal · 04b fachada traseira
│   │               05 elevação lateral · 06 corte longitudinal · 07 corte transversal · 08 isométrica · 10 modelo explodido
│   │               12 estrutura (isométrica) · 13 camadas construtivas (explodida)
│   ├── projeto/    pranchas PA-00, PA-01, PA-04, PA-05, PA-08b, PA-09 (SVG) e dxf/ (ZC-*.dxf editáveis em CAD)
├── lodge/          mesma estrutura (ZL-*.dxf) · lodge24/ e lodge28/: desenhos/01_conceito.svg e 08_isometrica.svg
├── capsule/        desenhos/01_conceito.svg (planta, corte A-A, seção B-B, fachada do Visor) e 08_isometrica.svg
│   ├── 3d/         zion-cocoon-3d.html (visualizador interativo Three.js) · zion-cocoon.glb
│   └── renders/    renders externos (frontal, lateral, cauda, aérea, noite), internos (estar, cama, banho), estrutura, corte
├── zenith/         mesma estrutura
├── detalhes/       DET-01 a DET-11: cobertura, ancoragem, fundação, esquadrias, drenagem, elétrica, hidráulica,
│                   climatização, arcos (Casulo), mastros (Safari)
├── tools/          geradores: geometry.py (fonte única da geometria), drawings_*.py, iso.py, details.py, bom.py,
│                   build_viewer.py, render.js, build_dossier.py, export_pdf.js, pa_sheets.py, export_dxf.py,
│                   build_projeto_arquitetonico.py
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
python3 drawings_extra.py && python3 exploded.py   # planta estrutural, fachada traseira, explodidas
python3 build_dossier.py     # Caderno Técnico HTML
python3 build_product_book.py   # Product Book HTML (sem preços; --precos gera a versão interna) + planilha interna XLSX
NODE_PATH=/opt/node22/lib/node_modules node export_pdf.js   # PDF do Caderno
NODE_PATH=/opt/node22/lib/node_modules node export_pdf.js ../ZION_ARCHITECTURAL_PRODUCT_BOOK.html ../ZION_ARCHITECTURAL_PRODUCT_BOOK.pdf
pip install ezdxf            # para os DXF
python3 pa_sheets.py         # pranchas complementares do projeto arquitetônico (capa, implantação, cobertura, forro, fachada esq., esquadrias)
python3 export_dxf.py        # DXF editáveis (plantas, cortes, fachadas, estrutura, 3D)
python3 build_projeto_arquitetonico.py && python3 build_projeto_arquitetonico.py --inline   # conjunto de pranchas HTML (impressão + autônomo)
NODE_PATH=/opt/node22/lib/node_modules node export_pdf.js ../ZION_PROJETO_ARQUITETONICO.html ../ZION_PROJETO_ARQUITETONICO.pdf
bash regen.sh                # ou tudo de uma vez (inclui renders e PDFs)
```

Toda a geometria (planta, seções, arcos, cumes, layout) vem de `tools/geometry.py`. Alterar um parâmetro ali e regenerar atualiza desenhos, isométricas, modelo 3D, renders e listas de materiais de forma consistente.

## Estado do projeto

Estudo preliminar / projeto conceitual. Antes da fabricação: cálculo estrutural com ART, form-finding da membrana com o fabricante, projeto executivo de esquadrias e instalações, protótipo no Zion Bubble Glamping. Ver Caderno, anexo A.

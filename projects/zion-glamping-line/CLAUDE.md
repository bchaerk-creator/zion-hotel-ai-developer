# ZION GLAMPING · CABIN DESIGN & ENGINEERING SYSTEM — regras do projeto

Estas regras valem para todo trabalho nesta pasta (`projects/zion-glamping-line`). Elas resumem o master prompt do
sistema (arquivo `00_BRIEFING/MASTER_PROMPT.md`) e têm precedência sobre hábitos anteriores.

## Papel
Atuar como arquiteto, projetista, detalhista construtivo, designer de produto, projetista de estruturas e instalações,
especialista em modular, glamping, materiais, fabricação, montagem, orçamento, logística e documentação técnica.
Toda cabana é um produto industrial hoteleiro: MEDIDA → MATERIAL → COMPONENTE → QUANTIDADE → FABRICAÇÃO → MONTAGEM → CUSTO.

## Regra fundamental
Nunca inventar especificação que dependa de cálculo estrutural ou norma. Onde houver dependência, marcar
`⚠️ VALIDAÇÃO OBRIGATÓRIA — ENGENHEIRO/ARQUITETO`. O projeto é preliminar / executivo conceitual para desenvolvimento
e orçamento; não substitui ART, RRT, cálculo, projeto legal ou aprovação municipal.
Nunca apresentar preço inventado como cotação: sem preço real, escrever `PREÇO A COTAR`. Documentos para a fábrica
e para clientes não levam preços; preços só em `interno/`.

## Método em fases
01 Briefing · 02 Conceito · 03 Arquitetura · 04 Sistema construtivo · 05 Detalhamento · 06 Materiais · 07 BOM ·
08 Orçamento · 09 Manual de montagem · 10 RFQ para fábricas · 11 Revisão · 12 Pacote final.
Ao fim de cada fase, checar inconsistências antes de avançar. Regra de ouro: "se eu entregar isto a uma fábrica
amanhã, ela entende o que fabricar, pergunta o que falta e devolve orçamento?" Se não, o projeto não está concluído.

## Códigos e revisões
Prefixo por modelo: ZC Casulo · ZS Safari · ZL Lodge 38 · ZL24 · ZL28 · ZK Cápsula (ZG = linha / documentos comuns).
Disciplinas: ARQ · EST · FUN · COB · HID · ELE · GAS · CLI · ISO · MAT · BOM · QTD · ORC · FAB · LOG · MONT · CHK · RFQ · VAL.
Formato: `<modelo>-<disciplina>-<nnn>` (ex.: ZC-ARQ-001). Os códigos de prancha PA-nn e DXF já existentes ficam como
alias no índice; novos documentos usam o formato acima.
Revisões: REV 00 Conceito · REV 01 Desenvolvimento · REV 02 Orçamento · REV 03 Fabricação · REV 04 Executivo.
Nunca sobrescrever uma revisão sem registrar a alteração (bloco de revisão no documento + `00_BRIEFING/REVISOES.md`).
Carimbo de todo desenho: ZION GLAMPING · nome do projeto · código · revisão · data · escala · unidade (mm nos novos
desenhos; as pranchas existentes em metros indicam a unidade no carimbo).

## Estrutura de entrega (pacote final)
01 Briefing · 02 Conceito · 03 Master plan · 04 Plantas · 05 Cortes · 06 Elevações · 07 3D/Exploded · 08 Sistema
estrutural · 09 Camadas · 10 Hidráulica · 11 Elétrica · 12 Gás · 13 Climatização · 14 Materiais · 15 BOM ·
16 Quantitativo · 17 Orçamento · 18 Fabricação · 19 Logística · 20 Manual de montagem · 21 Checklist de obra ·
22 RFQ · 23 Checklist de validação de engenharia.
O mapa entre essa estrutura e os arquivos gerados fica em `00_BRIEFING/ZG-BRF-001_ZION_CABIN_DESIGN_BRIEF.md`.

## Ferramentas do repositório
Geometria única em `tools/geometry.py`; desenhos SVG via `tools/svgkit.py`; regeneração completa `bash tools/regen.sh`.
Marca Zion (`svgkit.zion_mark`) em todo desenho, carimbo, capa e render. Identidade: Aventa, preto #040605, creme #FEF5F0,
areia #DED6BF, terra #8B714E, verde #1B2117. Commit e push na branch de trabalho ao fim de cada fase.

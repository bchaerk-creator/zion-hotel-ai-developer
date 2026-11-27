"""Estilo comum do e-book e do checklist do CAPEX (Trilha 1 · Pilar 6 · Aprofundamento).
Paleta oficial do CLAUDE.md; fontes da marca (Cormorant e Aventa) de docs/assets/fonts.
Para usar as fontes dos e-books da Trilha 1 (Playfair Display e Inter), rode com ZION_FONTES=trilha1."""
import os, pathlib

SRC = pathlib.Path(__file__).resolve().parent
REPO = SRC.parents[3]
DOCS = REPO / "docs"
FONTS = DOCS / "assets/fonts"
BRAND = DOCS / "brand"

RODAPE = ("Material educativo. Não é orçamento, projeto nem estudo de viabilidade definitivo. "
          "Custos, licenças e impostos se confirmam com engenheiro, arquiteto, prefeitura e contador.")


def rel(destino, base):
    """Caminho relativo de base (pasta do HTML) até destino, para o HTML funcionar em qualquer máquina."""
    return os.path.relpath(destino, base).replace(os.sep, "/")


def fontes_css(base):
    if os.environ.get("ZION_FONTES") == "trilha1":
        pf = DOCS / "trilha1/apresentacao/_motor/fonts"
        return (f"@font-face{{font-family:Titulo;font-weight:400 900;src:url('{rel(pf/'playfair-display-latin-wght-normal.woff2', base)}')}}"
                f"@font-face{{font-family:Titulo;font-style:italic;font-weight:400 900;src:url('{rel(pf/'playfair-display-latin-wght-italic.woff2', base)}')}}"
                "@font-face{font-family:Texto;src:local('Inter')}")
    return (f"@font-face{{font-family:Titulo;font-weight:300 700;src:url('{rel(FONTS/'cormorant.woff2', base)}')}}"
            f"@font-face{{font-family:Titulo;font-style:italic;font-weight:300 700;src:url('{rel(FONTS/'cormorant-italic.woff2', base)}')}}"
            f"@font-face{{font-family:Texto;font-weight:100 900;src:url('{rel(FONTS/'aventa.woff2', base)}')}}")


def css(base):
    return fontes_css(base) + """
:root{--preto:#040605;--musgo:#1B2117;--creme:#FEF5F0;--areia:#DED6BF;--terra:#8B714E;--ouro:#C9B37E;--cinza:#5E6158}
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:Texto,Arial,sans-serif;color:var(--musgo);background:#fff;font-size:10.6pt;line-height:1.5;font-variant-numeric:lining-nums}
.pg{width:210mm;height:297mm;padding:19mm 19mm 24mm;position:relative;page-break-after:always;background:#fff;overflow:visible}
.pg:last-child{page-break-after:auto}
.in{height:100%;}
h1,h2,h3{font-family:Titulo,Georgia,serif;font-weight:500;line-height:1.08;margin:0}
h2{font-size:27pt;margin:1mm 0 2mm} h2 i{color:var(--terra)}
h3{font-size:15.5pt;margin:5mm 0 2mm}
p{margin:0 0 2.6mm} ul,ol{margin:0 0 3mm;padding-left:5.5mm} li{margin-bottom:1.3mm}
b{font-weight:700}
.k{font-size:8pt;letter-spacing:.2em;text-transform:uppercase;color:var(--terra);font-weight:700}
.cab{position:relative;border-top:1px solid var(--areia);padding-top:3mm;margin-bottom:4mm}
.cab h2{max-width:138mm}
.cab .n{position:absolute;right:0;top:-2mm;font-family:Titulo,serif;font-size:78pt;line-height:1;color:var(--ouro);opacity:.32}
.lead{font-family:Titulo,serif;font-style:italic;font-size:14pt;line-height:1.3;color:var(--cinza);max-width:140mm;margin:0 0 3mm}
.regua{width:22mm;height:2px;background:var(--ouro);margin:3mm 0 4mm}
.cita{font-family:Titulo,serif;font-style:italic;font-size:16pt;line-height:1.25;border-left:3px solid var(--ouro);padding:1mm 0 1mm 6mm;margin:4mm 0;color:var(--musgo)}
.cita small{display:block;font-family:Texto,sans-serif;font-style:normal;font-size:7.8pt;color:var(--cinza);margin-top:1.8mm;letter-spacing:.12em;text-transform:uppercase}
.box{background:var(--creme);border:1px solid var(--areia);border-radius:3mm;padding:4mm 5mm;margin:3.5mm 0}
.box .k{display:block;margin-bottom:1.5mm}
.box.escuro{background:var(--musgo);color:var(--creme);border-color:var(--musgo)} .box.escuro .k{color:var(--ouro)}
.box.linha{background:#fff;border:1px dashed var(--terra)}
.box.ex{border-left:4px solid var(--terra)}
.box.ex .k{color:var(--terra)}
.neste{display:grid;grid-template-columns:1fr 1fr;gap:1mm 6mm;font-size:9.6pt;margin:0;padding-left:5mm}
.rev{font-size:9.6pt} .rev .resp{font-size:8.6pt;color:var(--cinza);margin-top:1.5mm}
table{width:100%;border-collapse:collapse;font-size:9.3pt;margin:2.5mm 0 3.5mm}
th,td{text-align:left;padding:1.45mm 2.4mm;border-bottom:1px solid var(--areia);vertical-align:top}
th{background:var(--musgo);color:var(--creme);font-weight:600;font-size:8.8pt}
td.v,th.v{text-align:right;white-space:nowrap}
tr.tot td{font-weight:700;border-top:1.5px solid var(--musgo);background:var(--creme)}
.cap{font-size:8pt;color:var(--cinza);margin-top:-2mm}
.fict{display:inline-block;font-size:7.6pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--creme);background:var(--terra);border-radius:99px;padding:.6mm 3mm;margin-bottom:2mm}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:3.5mm} .grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm}
.card{border:1px solid var(--areia);border-radius:3mm;padding:3mm 3.5mm;font-size:9.4pt;background:#fff}
.card b.t{display:block;font-family:Titulo,serif;font-weight:600;font-size:13pt;margin-bottom:1mm}
.campo{border-bottom:1px solid #b9b19b;height:8mm}
.num{font-family:Titulo,serif;font-size:30pt;line-height:1;color:var(--terra)}
.rod{position:absolute;left:19mm;right:19mm;bottom:9mm;font-size:7.3pt;line-height:1.35;color:var(--cinza);border-top:1px solid var(--areia);padding-top:2mm;display:flex;gap:6mm;justify-content:space-between}
.rod .p{white-space:nowrap;font-weight:700;color:var(--terra)}
.chk{list-style:none;padding-left:0} .chk li{position:relative;padding-left:7mm} .chk li:before{content:"";position:absolute;left:0;top:.6mm;width:3.6mm;height:3.6mm;border:1.3px solid var(--musgo);border-radius:.8mm;background:#fff}
"""

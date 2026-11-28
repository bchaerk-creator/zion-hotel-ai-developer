"""Estilo do e-book e do checklist do Aprofundamento 6B · Viabilidade (o mesmo da 6A · CAPEX), copiado do e-book do Pilar 6 da Trilha 1
(docs/trilha1/materiais/Pilar-6-Pre-viabilidade-ebook.pdf): Playfair Display nos títulos (ênfase em itálico dourado),
Inter no texto, paleta da Trilha 1 (PLANO.md 5.1; GUIA_COERENCIA.md, seção 4). Fontes locais de _motor/fonts.
O miolo do e-book corre em páginas A4 sem rodapé corrido nem número de página, como no Pilar 6."""
import os, pathlib

SRC = pathlib.Path(__file__).resolve().parent
REPO = SRC.parents[3]
DOCS = REPO / "docs"
FONTS = DOCS / "trilha1/apresentacao/_motor/fonts"

AVISO = ("Material educativo. Não é estudo de viabilidade, projeção nem promessa de retorno. "
         "Impostos se confirmam com o contador; contratos, com o advogado. A Zion avalia cada caso.")
FICT = "Exemplo ilustrativo · dados fictícios. Não são preços de referência."
CURSO = "Zion Hospitality Business · Transforme Seu Terreno em um Projeto de Hospedagem de Sucesso · Aprenda o passo a passo com o Método Zion"


def rel(destino, base):
    return os.path.relpath(destino, base).replace(os.sep, "/")


def fontes_css(base):
    f = lambda n: rel(FONTS / n, base)
    return (f"@font-face{{font-family:'Playfair Display';font-weight:400 900;src:url('{f('playfair-display-latin-wght-normal.woff2')}') format('woff2')}}"
            f"@font-face{{font-family:'Playfair Display';font-style:italic;font-weight:400 900;src:url('{f('playfair-display-latin-wght-italic.woff2')}') format('woff2')}}"
            f"@font-face{{font-family:Inter;font-weight:100 900;src:url('{f('inter-latin-wght-normal.woff2')}') format('woff2')}}"
            f"@font-face{{font-family:Inter;font-style:italic;font-weight:100 900;src:url('{f('inter-latin-wght-italic.woff2')}') format('woff2')}}"
            "@font-face{font-family:'Inter Sistema';src:local('Inter'),local('Inter Regular')}")


CORES = """:root{--verde:#16261C;--verde2:#22382A;--escuro:#1F3328;--creme:#F5F1E8;--creme2:#EBE4D4;--caixa:#FBF8F2;--bege:#ECE5D8;
--ouro:#E0BE5E;--ouro-t:#8A6D2F;--ouro-l:#B39865;--ouro-p:#CDBB9A;--texto:#16261C;--texto2:#46564B;--linha:#E2DBCB;--linha2:#D9D3C4;
--mata:#2F5F52;--crit:#B03A2E;--ok:#1F5A33}"""

BASE = """
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font-family:Inter,'Inter Sistema',Arial,sans-serif;color:var(--texto);background:#fff;font-size:9.2pt;line-height:1.56;font-variant-numeric:lining-nums}
h1,h2,h3,h4{font-family:'Playfair Display',Georgia,serif;font-weight:400;margin:0;line-height:1.15;color:var(--texto)}
h1 i,h2 i,h3 i,h4 i{color:var(--ouro-t)}
p{margin:0 0 2.6mm} b{font-weight:650}
ul,ol{margin:0 0 2.6mm;padding-left:5mm} li{margin-bottom:1mm}
.k{font-size:6.6pt;letter-spacing:.22em;text-transform:uppercase;font-weight:700;color:var(--ouro-t)}
table{width:100%;border-collapse:collapse;font-size:7.9pt;line-height:1.4;margin:2mm 0 1.2mm}
th{background:var(--verde);color:#fff;font-weight:600;text-align:left;padding:2.2mm 2.4mm}
td{padding:1.6mm 2.2mm;border-bottom:1px solid var(--linha);vertical-align:top}
td.v,th.v{text-align:right;white-space:nowrap}
tr{break-inside:avoid}
thead{display:table-header-group}
tr.tot td{font-weight:700;border-top:1.2px solid var(--verde);background:var(--caixa)}
tr.sub td{color:var(--texto2);font-style:italic}
.leg{font-size:7pt;color:var(--texto2);margin:0 0 4mm}
"""


ESCALA = float(os.environ.get("ZION_ESCALA", "1.28"))  # 1,28: o corpo do texto fica do tamanho do e-book do Pilar 6


def escala(txt, f):
    """Multiplica tamanhos em pt e mm (fontes, respiros, caixas) para chegar à escala do e-book do Pilar 6.
    Ficam de fora as linhas marcadas com /*fixo*/ (margens da página e geometria da capa)."""
    import re
    out = []
    for linha in txt.split("\n"):
        if "/*fixo*/" in linha:
            out.append(linha); continue
        out.append(re.sub(r"(-?\d*\.?\d+)(pt|mm)\b", lambda m: f"{float(m.group(1)) * f:.2f}{m.group(2)}", linha))
    return "\n".join(out)


def css(base):
    return fontes_css(base) + CORES + escala(BASE + EBOOK, ESCALA)


EBOOK = """
@page{size:A4;margin:18mm 19mm 17mm 19mm} /*fixo*/
/* capa: bloco verde com margem branca, sem logo e sem foto, numeral gigante (como o Pilar 6) */
.capa{background:var(--verde);color:#fff;margin:0;height:204mm;padding:27mm 8mm 0 8mm;position:relative;overflow:hidden;break-after:page} /*fixo*/
.capa .k{color:var(--ouro);font-size:7pt;letter-spacing:.3em}
.capa h1{color:#fff;font-size:31pt;line-height:1.12;margin:5mm 0 4mm}
.capa h1 i{color:var(--ouro)}
.capa .deck{font-size:10.6pt;line-height:1.62;color:var(--creme);max-width:104mm}
.capa .pe{position:absolute;left:8mm;right:8mm;top:136mm;/*fixo*/font-size:9pt;letter-spacing:.04em;line-height:1.7;color:#C9C6B8;max-width:140mm}
.capa .num{/*fixo*/position:absolute;right:-3mm;bottom:-24mm;font-family:'Playfair Display',serif;font-size:235pt;line-height:1;color:var(--escuro)}
/* sumário */
.sum{break-after:page;padding-top:16mm}
.sum h2{font-size:24pt;margin:2mm 0 6mm}
.sum table{font-size:9.6pt;margin:0}
.sum td{border-bottom:1px solid var(--linha2);padding:2.9mm 0}
.sum td.n{width:12mm;font-family:'Playfair Display',serif;color:var(--ouro-t)}
/* abertura de capítulo */
.cap{break-before:page}
.cab{position:relative;border-top:1px solid var(--linha2);padding-top:2mm;margin:0}
.cab .k b{color:var(--texto2);font-weight:700;margin-left:2mm}
.cab h2{font-size:23pt;margin:2.6mm 0 2mm;max-width:132mm;position:relative;z-index:2}
.cab .deck{font-family:'Playfair Display',serif;font-style:italic;font-size:11.4pt;line-height:1.55;color:var(--texto2);max-width:138mm;margin:0;position:relative;z-index:2}
.cab .n{position:absolute;right:0;top:4mm;font-family:'Playfair Display',serif;font-size:88pt;line-height:1;color:var(--bege);z-index:1}
.regua{width:21mm;height:1.6px;background:var(--ouro-l);margin:5mm 0 4mm}
.porque{border:1px solid var(--bege);border-left:3px solid var(--ouro);background:var(--caixa);border-radius:1.5mm;padding:1.6mm 3mm;margin:0 0 3mm;break-inside:avoid}
.porque div{display:grid;grid-template-columns:32mm 1fr;gap:3mm;font-size:7.2pt;line-height:1.4;padding:1mm 0;border-bottom:1px solid var(--bege)}
.porque div:last-child{border-bottom:0}
.neste{font-size:7.6pt;line-height:1.5;margin:0 0 1mm}
.porque span{font-size:5.9pt;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:var(--ouro-t);padding-top:.4mm}
/* parágrafo de abertura com capitular */
.abre{font-size:11.2pt;line-height:1.6;margin:4mm 0 3mm}
.abre:first-letter{font-family:'Playfair Display',serif;color:var(--ouro-t);float:left;font-size:40pt;line-height:.9;padding:1.2mm 2.2mm 0 0}
h3{font-size:15pt;margin:5mm 0 2.2mm;break-after:avoid}
h3+p{break-before:avoid}
/* caixas (Pilar 6) */
.bx{background:var(--caixa);border:1px solid var(--bege);border-left:3px solid var(--ouro-l);border-radius:1.5mm;padding:3.2mm 4.4mm 2mm;margin:2.6mm 0 3mm;break-inside:avoid}
.bx>.k{display:block;margin-bottom:1.6mm}
.bx h4{font-size:12.4pt;margin:0 0 2mm;break-after:avoid}
.bx p,.bx li{font-size:8.2pt}
.bx.escuro-b{border-left-color:var(--escuro)}
.bx.crit{border-left-color:var(--crit)}
.bx.faca{border-left-color:var(--ouro)}
.bx.ex.longa,.bx.quebra,.bx.solta{break-inside:auto}
.bx p,.bx li{orphans:2;widows:2}
.bx.ex{background:var(--bege);border-color:var(--bege);border-left:3px solid var(--mata)}
.bx.pare{background:#fff;border:1px dashed var(--ouro-p);border-left:1px dashed var(--ouro-p)}
.bx.pare .op{margin:0 0 1.4mm;font-size:8.6pt} .bx.pare .op b{margin-right:1.2mm}
.bx.pare .ver{color:var(--ouro-t);font-weight:700;font-size:8.4pt;margin:2mm 0 .6mm}
.bx.pare .resp{font-size:8pt;color:var(--texto2)}
.bx.levar{background:var(--escuro);border-color:var(--escuro);color:#fff}
.bx.levar .k{color:var(--ouro)} .bx.levar h4{color:#fff}
.bx.levar li,.bx.levar p{font-size:8.4pt;color:#F2EFE6}
.bx table{margin:1.5mm 0 1mm;font-size:7.4pt;line-height:1.34}
.bx td{padding:1.35mm 2mm}.bx th{padding:1.7mm 2mm}
.bx .leg{margin:0 0 1.6mm}
.bx.ex table td{border-bottom-color:#D8CFBC}
.campo{background:var(--creme);border:1px solid var(--linha2);border-radius:1mm;height:13mm;margin:1mm 0 3mm}
.campo.alto{height:22mm}
.nota{font-size:7pt;color:var(--texto2);margin-top:1mm}
.tres{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2mm;margin-top:1mm}
.tres>div{background:var(--caixa);border-top:2px solid var(--ouro-l);padding:2mm 2.6mm;font-size:7.3pt;line-height:1.42;background:#F5F2EB}
.tres>div:last-child{background:var(--escuro);color:#fff;border-top-color:var(--ouro)}
.tres .nn{font-family:'Playfair Display',serif;font-size:13pt;color:var(--ouro-t);line-height:1}
.tres>div:last-child .nn{color:var(--ouro)}
.tres b{display:block;margin:1mm 0 1mm;font-size:7.6pt}
.tres ul{padding-left:3.6mm;margin:0} .tres li{font-size:7.1pt;margin-bottom:.6mm}
.pergunta{background:var(--caixa);padding:5mm 6mm;margin:4mm 0;display:flex;gap:5mm;align-items:center;font-size:8.6pt;break-inside:avoid}
.pergunta span{font-family:'Playfair Display',serif;font-size:24pt;color:var(--ouro-t);line-height:1}
.cita{border-left:2px solid var(--ouro-l);padding:.6mm 0 .6mm 5mm;margin:3.6mm 0 3.6mm;break-inside:avoid}
.cita q{display:block;font-family:'Playfair Display',serif;font-size:14.6pt;line-height:1.32;color:var(--ouro-t);quotes:none}
.cita small{display:block;font-size:7pt;color:var(--texto2);letter-spacing:.04em;margin-top:1.6mm}
.conf{font-size:8.3pt;color:var(--texto2)}
.dia{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2.5mm;margin:3mm 0 4mm;break-inside:avoid}
.dia>div{border:1px solid var(--bege);border-radius:1.5mm;padding:2.6mm 3mm;font-size:8pt;line-height:1.45;background:#fff}
.dia>div.on{background:var(--verde);color:#fff;border-color:var(--verde)}
.dia h4{font-size:11pt;margin-bottom:1mm} .dia .on h4{color:var(--ouro)}
.dez li{margin-bottom:1.3mm}
/* 6B: a escada de seis degraus, as barras do ano mês a mês e o semáforo dos cinco passos */
.degraus{margin:3mm 0 4mm;break-inside:avoid}
.degraus .d{display:grid;grid-template-columns:44mm 1fr 24mm;align-items:center;gap:2.4mm;margin-bottom:1.3mm;font-size:7.8pt;line-height:1.3}
.degraus .d .bar{height:6.2mm;background:var(--verde);border-radius:.8mm;position:relative}
.degraus .d .bar.sai{background:transparent;border:1px dashed var(--ouro-l)}
.degraus .d .bar.fim{background:var(--ouro)}
.degraus .d .v{text-align:right;white-space:nowrap;font-weight:650}
.degraus .d .t b{display:block;font-family:'Playfair Display',serif;font-weight:400;font-size:9.6pt;color:var(--texto)}
.degraus .d .t{color:var(--texto2)}
.meses{display:grid;grid-template-columns:repeat(12,1fr);gap:1.2mm;height:30mm;align-items:center;margin:3mm 0 1mm;border-top:1px solid var(--linha2);border-bottom:1px solid var(--linha2);position:relative;break-inside:avoid}
.meses .c{position:relative;height:100%}
.meses .c i{position:absolute;left:12%;right:12%;background:var(--mata);border-radius:.6mm}
.meses .c i.neg{background:var(--crit)}
.meses .c span{position:absolute;left:0;right:0;bottom:-4.6mm;text-align:center;font-size:6.6pt;color:var(--texto2)}
.meses:after{content:"";position:absolute;left:0;right:0;top:50%;border-top:1px solid var(--texto2)}
.passos{display:grid;grid-template-columns:repeat(5,1fr);gap:1.6mm;margin:3mm 0;break-inside:avoid}
.passos>div{border-radius:1.4mm;padding:2.2mm 2.4mm;font-size:7.2pt;line-height:1.35;border:1px solid var(--bege);background:#fff}
.passos>div b{display:block;font-family:'Playfair Display',serif;font-weight:400;font-size:10pt;margin-bottom:.8mm}
.passos .s{display:inline-block;margin-top:1.2mm;padding:.5mm 1.8mm;border-radius:9mm;font-size:6.4pt;letter-spacing:.1em;text-transform:uppercase;font-weight:700}
.passos .ok .s{background:#E1EFE3;color:var(--ok)} .passos .aj .s{background:#F6EBCB;color:#7A5E12} .passos .rd .s{background:#F8E3DE;color:#9B2C1F}
.veredito{background:var(--verde);color:#fff;border-radius:1.5mm;padding:3mm 4.6mm;margin:1mm 0 4mm;display:flex;gap:4mm;align-items:center;break-inside:avoid}
.veredito .k{color:var(--ouro)} .veredito b{font-family:'Playfair Display',serif;font-weight:400;font-size:17pt;color:var(--ouro)}
.veredito p{margin:0;font-size:8.4pt;color:#F2EFE6}
.fim{font-size:7.4pt;line-height:1.55;color:var(--texto2);border-top:1px solid var(--linha2);padding-top:3mm;margin-top:6mm;break-inside:avoid}
"""

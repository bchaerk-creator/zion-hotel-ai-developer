# -*- coding: utf-8 -*-
"""Monta o PROJETO ARQUITETÔNICO (conjunto de pranchas, uma por página A3 paisagem) de ZION CASULO e ZION SAFARI.
Reúne as pranchas PA-xx (pa_sheets.py) com os desenhos existentes (desenhos/, detalhes/) e lista os DXF (export_dxf.py).
Saídas: ZION_PROJETO_ARQUITETONICO.html (links relativos, para PDF), ZION_PROJETO_ARQUITETONICO_standalone.html (--inline, tudo embutido).
Uso: python3 build_projeto_arquitetonico.py [--inline]"""
import os, sys, base64, html
from pa_sheets import SHEETS, AREAS, ESQUADRIAS, NOTAS

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ARTIFACT = "--artifact" in sys.argv   # versão sem esqueleto html/head/body (publicação como artefato)
INLINE = "--inline" in sys.argv or ARTIFACT
NAME = {"cocoon": "ZION CASULO", "zenith": "ZION SAFARI", "lodge": "ZION LODGE"}
TAG = {"cocoon": "ZC", "zenith": "ZS", "lodge": "ZL"}
PRODUCTS = ("cocoon", "zenith", "lodge")

# sequência de pranchas: (código, título, escala, arquivo relativo, observação)
def sheets(p):
    d = f"{p}/desenhos"; j = f"{p}/projeto"; det = "detalhes"
    S = [("PA-00", "Capa · índice · quadro de áreas · notas gerais", "s/ escala", f"{j}/PA-00_capa_indice_areas_notas.svg", ""),
         ("PA-01", "Planta de situação e implantação", "1:200", f"{j}/PA-01_implantacao.svg", "implantação genérica de referência; adaptar ao sítio"),
         ("PA-02", "Planta baixa cotada", "1:50", f"{d}/03_planta_tecnica.svg", "cotas gerais, parciais e níveis"),
         ("PA-03", "Planta de layout (humanizada)", "1:50", f"{d}/02_planta_humanizada.svg", "mobiliário fixo e solto, acabamentos"),
         ("PA-04", "Planta de cobertura", "1:50", f"{j}/PA-04_planta_cobertura.svg", "escoamento, calhas, tubos de queda, claraboia / óculo"),
         ("PA-05", "Planta de forro refletido e iluminação", "1:50", f"{j}/PA-05_forro_iluminacao.svg", "forro tensionado, LED, difusores, comandos"),
         ("PA-06a", "Corte longitudinal A-A", "1:50", f"{d}/06_corte_longitudinal.svg", "pé-direito, forro, ático técnico, fundação"),
         ("PA-06b", "Corte transversal B-B", "1:50", f"{d}/07_corte_transversal.svg", "seção da concha / dos cumes"),
         ("PA-07a", "Fachada frontal", "1:50", f"{d}/04_elevacao_frontal.svg", "fachada de vidro e deck"),
         ("PA-07b", "Fachada traseira", "1:50", f"{d}/04b_fachada_traseira.svg", ""),
         ("PA-08a", "Fachada lateral direita", "1:50", f"{d}/05_elevacao_lateral.svg", "olhar para +y"),
         ("PA-08b", "Fachada lateral esquerda", "1:50", f"{j}/PA-08b_fachada_lateral_esquerda.svg", "olhar para -y"),
         ("PA-09", "Quadro de esquadrias", "1:50", f"{j}/PA-09_quadro_esquadrias.svg", "vistas, dimensões, especificação e localização"),
         ("PA-10", "Planta estrutural", "1:50", f"{d}/03b_planta_estrutural.svg", "eixos, arcos / pilares, vigas, estacas"),
         ]
    dets = {"cocoon": ["DET-01_cobertura_cocoon", "DET-10_arcos_cocoon"], "zenith": ["DET-02_cobertura_zenith", "DET-11_mastros_zenith"], "lodge": ["DET-12_lanterna_lodge", "DET-13_caibros_lodge"]}[p]
    dets = [dets[0], "DET-03_ancoragem", "DET-04_fundacao", "DET-05_esquadrias", "DET-06_drenagem", dets[1]]
    if p == "lodge": dets = [d for d in dets if os.path.exists(os.path.join(ROOT, "detalhes", d + ".svg"))]
    for k, f in enumerate(dets):
        S.append((f"PA-11{'abcdef'[k]}", "Detalhe construtivo " + f.split("_", 1)[0] + " · " + f.split("_", 1)[1].replace("_", " "), "1:5 a 1:20", f"{det}/{f}.svg", ""))
    S += [("PA-12a", "Vista isométrica", "s/ escala", f"{d}/08_isometrica.svg", ""), ("PA-12b", "Modelo explodido da estrutura", "s/ escala", f"{d}/10_modelo_explodido.svg", ""),
          ("PA-12c", "Camadas construtivas", "s/ escala", f"{d}/13_camadas_construtivas.svg", ""), ("PA-12d", "Estudo da estrutura metálica (isométrica)", "s/ escala", f"{d}/12_estrutura_isometrica.svg", "")]
    return S

def src(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): return None
    if not INLINE: return rel
    ext = rel.rsplit(".", 1)[-1].lower(); mime = {"svg": "image/svg+xml", "png": "image/png", "jpg": "image/jpeg", "woff2": "font/woff2"}[ext]
    return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()

def dxf_list(p):
    d = os.path.join(ROOT, p, "projeto", "dxf")
    return sorted(os.listdir(d)) if os.path.isdir(d) else []

# hachuras SVG (<pattern>) viram imagens de página inteira no PDF do Chromium (~1 MB cada); na versão de impressão
# substituímos por tons chapados equivalentes para manter o PDF vetorial e leve.
FLAT = {"hatch": "#D9D4C7", "hatch2": "#CFC9BA", "wood": "#D9C4A3", "deck": "#B99A73", "tile": "#D8D6CF", "insul": "#EFE8DA", "soil": "#E6DFD2", "grass": "#DDE1CC",
        "p-steel": "#BDBDB8", "p-wood": "#D9C4A3", "p-ply": "#E3D3B6", "p-pir": "#F1E8C8", "p-gravel": "#DCD8CE", "p-ins": "#F0E9DA", "p-osb": "#E0CFA9", "p-dots": "#E4DED2", "p-cem": "#D6D4CC"}

def svg_inline(rel):
    """SVG embutido como marcação (vetorial no PDF, sem rasterização), com hachuras achatadas."""
    t = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    if t.startswith("<?xml"): t = t[t.index("?>") + 2:]
    t = t.replace(' width="1600" height="1000"', "", 1).replace('width="1600" height="1000" ', "", 1)
    for pid, col in FLAT.items(): t = t.replace(f"url(#{pid})", col)
    return t

def page(code, title, scale, rel, product, note=""):
    s = src(rel)
    if not s: img = f'<div class="missing">[{rel} não gerado]</div>'
    elif INLINE: img = f'<img src="{s}" alt="{code} {html.escape(title)}">'
    else: img = svg_inline(rel)
    return f'''<section class="sheet" id="{product}-{code}">
<div class="strip"><span class="code">{code}</span><span class="ttl">{html.escape(title)}</span><span class="scl">{html.escape(scale)}</span><span class="prod">{NAME[product]}</span><span class="note">{html.escape(note)}</span></div>
<div class="art">{img}</div>
</section>'''

def cover():
    rows = ""
    for p in PRODUCTS:
        for (code, t, sc, rel, note) in sheets(p):
            rows += f'<tr><td>{TAG[p]}-{code}</td><td>{html.escape(t)}</td><td>{sc}</td><td>{NAME[p]}</td></tr>'
    dx = ""
    for p in PRODUCTS:
        dx += "".join(f'<li><code>{p}/projeto/dxf/{f}</code></li>' for f in dxf_list(p))
    return f'''<section class="sheet cover">
<div class="coverl"><div class="brand">ZION</div><div class="sub">GLAMPING COLLECTION · ZION HOTEL GROUP INTERNATIONAL</div>
<h1>PROJETO<br>ARQUITETÔNICO</h1><h2>ZION CASULO · ZION SAFARI · ZION LODGE</h2>
<p class="lead">Conjunto de pranchas de estudo preliminar / anteprojeto de produto industrializado: implantação, plantas cotadas e de layout, cobertura, forro e iluminação, cortes, fachadas, quadro de esquadrias, planta estrutural, detalhes construtivos e vistas isométricas. Arquivos DXF editáveis em CAD anexos.</p>
<dl><dt>Proprietário</dt><dd>Zion Hotel Group International Ltda</dd><dt>Fase</dt><dd>Estudo preliminar / anteprojeto · R00 · setembro de 2026</dd><dt>Formato</dt><dd>Pranchas A1 (impressão A3 em escala reduzida 1:2 → 1:100 e 1:400)</dd><dt>Pranchas</dt><dd>{" + ".join(str(len(sheets(p))) for p in PRODUCTS)} = {sum(len(sheets(p)) for p in PRODUCTS)} no total</dd></dl>
<p class="warn">Pré-dimensionamento: bitolas, espessuras, fundações e form-finding da membrana a validar por engenheiros habilitados (ART/RRT) antes da fabricação.</p></div>
<div class="coverr"><h3>ÍNDICE GERAL</h3><div class="tw"><table><tr><th>Prancha</th><th>Título</th><th>Escala</th><th>Produto</th></tr>{rows}</table></div>
<h3>ARQUIVOS CAD (DXF, unidades em metros)</h3><ul class="dxf">{dx}</ul></div>
</section>'''

def build():
    fonts = ""
    for f, fam, style in (("assets/aventa.woff2", "Aventa", "normal"), ("assets/cormorant.woff2", "Cormorant Garamond", "normal")):
        s = src(f)
        if s: fonts += f"@font-face{{font-family:'{fam}';src:url({s}) format('woff2');font-weight:100 900;font-style:{style};font-display:swap;}}\n"
    css = fonts + """
:root{--cream:#FEF5F0;--ink:#1B2117;--earth:#8B714E;--sand:#DED6BF;--black:#040605}
*{box-sizing:border-box} body{margin:0;background:#E9E2D6;font-family:'Aventa','DM Sans',Helvetica,Arial,sans-serif;color:var(--ink)}
nav{position:sticky;top:0;background:var(--black);color:var(--cream);padding:8px 16px;font-size:12px;display:flex;gap:14px;flex-wrap:wrap;z-index:5}
nav a{color:var(--sand);text-decoration:none} nav b{letter-spacing:.3em}
.sheet{width:420mm;height:297mm;margin:10mm auto;background:var(--cream);box-shadow:0 8px 30px rgba(0,0,0,.18);display:flex;flex-direction:column;overflow:hidden;page-break-after:always;break-after:page}
.strip{display:flex;gap:14px;align-items:baseline;padding:5mm 8mm 0;font-size:11px;color:var(--earth)}
.strip .code{font-weight:800;color:var(--ink);letter-spacing:.1em;font-size:13px} .strip .ttl{font-weight:600;color:var(--ink);font-size:13px} .strip .prod{margin-left:auto;letter-spacing:.2em;font-size:10px}
.art{flex:1;display:flex;align-items:center;justify-content:center;padding:2mm 6mm 5mm} .art img,.art svg{width:100%;height:auto;max-height:100%;display:block}
.missing{border:1px dashed var(--earth);padding:20px;color:var(--earth)}
.cover{flex-direction:row;padding:0} .coverl{width:40%;background:var(--black);color:var(--cream);padding:18mm 14mm} .coverr{flex:1;padding:14mm 12mm;font-size:10px}
.brand{font-size:44px;font-weight:800;letter-spacing:.4em} .sub{font-size:9px;letter-spacing:.3em;color:var(--sand);margin-bottom:26mm}
.coverl h1{font-weight:300;font-size:34px;letter-spacing:.12em;line-height:1.15;margin:0 0 8mm} .coverl h2{font-family:'Cormorant Garamond',Georgia,serif;font-weight:400;font-size:26px;margin:0 0 8mm;color:var(--sand)}
.lead{font-size:11.5px;line-height:1.5;color:var(--sand)} dl{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;font-size:11px;margin:8mm 0} dt{color:var(--earth);letter-spacing:.15em;font-size:9px;text-transform:uppercase}
.warn{font-size:10px;color:var(--sand);border-top:1px solid var(--earth);padding-top:4mm;margin-top:10mm}
.coverr h3{font-size:12px;letter-spacing:.3em;margin:0 0 4mm} table{border-collapse:collapse;width:100%;font-size:9.5px} th,td{text-align:left;padding:2px 6px;border-bottom:1px solid var(--sand)} th{color:var(--earth);font-weight:600;letter-spacing:.1em;font-size:8.5px}
.tw{max-height:180mm;overflow:hidden;column-count:2;column-gap:8mm;margin-bottom:6mm} .dxf{columns:2;font-size:8.5px;list-style:none;padding:0;margin:0;color:var(--earth)} .dxf li{margin:1px 0}
@media print{@page{size:A3 landscape;margin:0} body{background:#fff} nav{display:none} .sheet{margin:0;box-shadow:none;width:420mm;height:297mm}}
"""
    if ARTIFACT:
        css += """
body{padding-block:0 24px;padding-inline:16px}
.sheet{width:100%;max-width:1400px;height:auto;aspect-ratio:420/297;margin:16px auto}
.strip{padding:12px 16px 0;flex-wrap:wrap} .art{padding:4px 12px 12px}
.cover{flex-direction:row} .coverl{padding:36px 28px} .coverr{padding:28px 24px;overflow:auto}
@media (max-width:760px){.sheet{aspect-ratio:auto} .cover{flex-direction:column} .coverl{width:100%} .brand{font-size:32px} .coverl h1{font-size:26px} .tw{column-count:1;max-height:none} .dxf{columns:1}}
nav{top:env(safe-area-inset-top,0px)}
"""
    navs = "".join(f'<a href="#{p}-{c}">{TAG[p]}-{c}</a>' for p in ("cocoon", "zenith") for (c, *_r) in sheets(p))
    body = cover()
    for p in PRODUCTS:
        for (code, t, sc, rel, note) in sheets(p): body += page(code, t, sc, rel, p, note)
    if ARTIFACT:
        doc = f'<title>Projeto Arquitetônico Zion Casulo &amp; Safari</title><style>{css}</style><nav><b>ZION</b> Projeto arquitetônico · {navs}</nav>{body}'
        out = sys.argv[sys.argv.index("--artifact") + 1] if len(sys.argv) > sys.argv.index("--artifact") + 1 else os.path.join(ROOT, "ZION_PROJETO_ARQUITETONICO_artifact.html")
    else:
        doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · Projeto Arquitetônico · Casulo &amp; Safari</title><meta name="viewport" content="width=device-width,initial-scale=1"><style>{css}</style></head><body><nav><b>ZION</b> Projeto arquitetônico · {navs}</nav>{body}</body></html>'
        out = os.path.join(ROOT, "ZION_PROJETO_ARQUITETONICO" + ("_standalone" if INLINE else "") + ".html")
    open(out, "w", encoding="utf-8").write(doc)
    print(out, round(os.path.getsize(out) / 1e6, 1), "MB")

if __name__ == "__main__":
    build()

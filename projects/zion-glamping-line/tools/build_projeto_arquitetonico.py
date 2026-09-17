# -*- coding: utf-8 -*-
"""Monta o PROJETO ARQUITETÔNICO (conjunto de pranchas, uma por página A3 paisagem) de ZION CASULO e ZION SAFARI.
Reúne as pranchas PA-xx (pa_sheets.py) com os desenhos existentes (desenhos/, detalhes/) e lista os DXF (export_dxf.py).
Saídas: ZION_PROJETO_ARQUITETONICO.html (links relativos, para PDF), ZION_PROJETO_ARQUITETONICO_standalone.html (--inline, tudo embutido).
Uso: python3 build_projeto_arquitetonico.py [--inline]"""
import os, sys, base64, html
from svgkit import zion_mark_html, zion_logo_html
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

INDEX_EXTRA = [("PA-13", "Camadas construtivas e especificação de materiais", "s/ escala"), ("PA-14", "Quadro de materiais estimados (quantidades, sem preços)", "s/ escala")]

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

LAYERS = {
 "cocoon": [("01", "Fundação", "44 estacas helicoidais Ø76 galvanizadas, hélice Ø300, L 1,5 a 2,5 m, cabeçotes ajustáveis (malha 1,20 x 1,30 m)"), ("02", "Quadro do deck e piso", "Vigas U 150 x 60 x 3,0 galvanizadas; vigotas 50 x 150 tratadas a cada 400 mm; trilhos de base curvados 100 x 50 x 3,0"),
            ("03", "Piso", "PIR 50 mm + manta; compensado naval 18 mm; carvalho de engenharia 14 mm; porcelanato 60 x 120 no banho; deck de cumaru 20 x 140"), ("04", "Estrutura principal", "Anel frontal A0 Ø101,6 x 4,0 inclinado 8°; 7 arcos elípticos B01-B07 Ø88,9 x 3,6 em 3 segmentos com luvas Ø76; quadro da cauda Ø60,3; aço ASTM A500 galvanizado a fogo + pó"),
            ("05", "Travamentos", "7 terças Ø48,3 x 3,0 em trechos de 1,20 m; Espinha de Luz em treliça Ø42,4 / Ø26,9; cabos inox Ø8 em X com esticadores"), ("06", "Membrana externa", "PVDF 1050 g/m² tipo III em 7 painéis entre arcos + tampas, deslizada em perfil duplo keder de alumínio sobre cada arco; pré-tensão 2,5 kN/m"),
            ("07", "Câmara de ventilação", "60 mm entre membrana e isolamento; entrada no rodapé, saída no respiro de cumeeira x 7,0 a 8,2"), ("08", "Isolamento", "Lã de PET 50 mm, 25 kg/m³, sobre malha"), ("09", "Barreira de condensação", "Manta refletiva de alumínio com emendas fitadas"),
            ("10", "Forro", "Forro tensionado acústico classe M1 seguindo a concha; forro plano a 2,40 no banho com ático técnico"), ("11", "Fechamentos", "Fachada V1 em anel de alumínio curvo com 8 painéis de vidro insulado 6 lam + 12 Ar + 6 temp low-e; porta pivotante PV1 1,00 x 2,40; 6 Janelas Olho em requadro de madeira laminada 220 mm; Espinha de Luz em vidro laminado 8 + 8"),
            ("12", "Instalações", "Quadro 220 V no ático; fitas LED 2700 K nos rodapés e requadros; PEX Ø25; esgoto Ø100 sob o deck; evaporadora dutada 12k BTU; exaustor com recuperador"), ("13", "Acabamento e FF&E", "Parede da cabeceira/banho em LSF + painel + ripado; marcenaria em carvalho; louças e metais; mobiliário, luminárias e enxoval conforme FF&E")],
 "zenith": [("01", "Fundação", "30 estacas helicoidais Ø76 sob o piso + 7 estacas de tração sob os postes; cabeçotes ajustáveis"), ("02", "Quadro do deck e piso", "Vigas U 150 x 60 x 3,0; vigotas 50 x 150 a cada 400 mm; terraço e passarela em cumaru"),
            ("03", "Piso", "PIR 50 mm + manta; compensado naval 18 mm; carvalho 14 mm; porcelanato 60 x 120 no banho; deck de cumaru 20 x 140"), ("04", "Estrutura principal", "2 mastros Ø139,7 x 4,5 com bases articuladas e coroas de 3 braços Ø48,3; 10 pilares Ø101,6; anel de beiral 150 x 100 x 4,0 em 4 segmentos parafusados; aço A500 galvanizado + pó"),
            ("05", "Travamentos", "7 postes externos Ø76,1 x 3,6 inclinados 8° com estais Ø10 inox; cabo de borda Ø12 em bolsa; diafragma SIP"), ("06", "Membrana externa", "PVDF 1050 g/m² em gomos radiais soldados por RF; anéis de cume Ø1,20 e Ø0,70; i mín. 14° no vale; pré-tensão 2,5 kN/m"),
            ("07", "Câmara de ventilação", "60 mm; saída pela chaminé do Respiro com veneziana motorizada"), ("08", "Isolamento", "Lã de PET 50 mm sobre malha"), ("09", "Barreira de condensação", "Manta refletiva de alumínio"),
            ("10", "Forro", "Forro tensionado seguindo os cumes, a 0,30 m da membrana; forro plano a 2,50 no banho"), ("11", "Fechamentos", "Fachada de correr PC1 4 folhas 1,35 x 2,75 em vidro insulado low-e; 4 vidros laterais fixos VF1; painéis SIP 100 mm + ripado termotratado 40 x 40 nas faces opacas; janelas J1-J4; Óculo OC1 em cúpula de vidro laminado curvo"),
            ("12", "Instalações", "Quadro no ático; LED no anel de beiral e rodapés; PEX; esgoto Ø100; evaporadora dutada 18k BTU; hidromassagem no terraço (opcional)"), ("13", "Acabamento e FF&E", "Parede da cabeceira com o mastro M1; totem do mastro M2 na Ilha do Café; marcenaria; louças e metais; FF&E")],
 "lodge": [("01", "Fundação", "22 estacas helicoidais Ø76 (20 sob piso e deck + 2 sob os postes da vela), cabeçotes ajustáveis"), ("02", "Quadro do deck e piso", "Grelha de vigas U 150 x 60 x 3,0 com anel de borda octogonal; vigotas LSF Ue 150 x 40 x 1,25 (ou 50 x 150 tratadas); deck em três faces"),
            ("03", "Piso", "PIR 50 mm + manta; compensado naval 18 mm; carvalho 14 mm; porcelanato no banho; deck de cumaru 20 x 140"), ("04", "Estrutura principal", "8 pilares Ø101,6 x 4,0 revestidos em madeira 44 mm; anel de beiral 150 x 100 x 4,0 em 8 segmentos; 8 caibros Ø76,1 x 3,6; anel de compressão da lanterna Ø60,3 x 3,0 calandrado; aço A500 galvanizado + pó"),
            ("05", "Travamentos", "Cabos inox Ø8 em X nas 3 faces opacas; vela de sombra em 2 postes Ø76,1 x 3,6 com estais Ø8"), ("06", "Membrana externa", "PVDF 1050 g/m² em 8 gomos com keder sobre os caibros, beiral 0,90 m; tampa da lanterna Ø2,10; pré-tensão 2,5 kN/m"),
            ("07", "Câmara de ventilação", "60 mm; saída pela veneziana da Lanterna Zion (efeito chaminé)"), ("08", "Isolamento", "Lã de PET 50 mm sobre malha, cônica"), ("09", "Barreira de condensação", "Manta refletiva de alumínio"),
            ("10", "Forro", "Forro tensionado cônico com anel de LED na lanterna; forro plano a 2,40 no banho"), ("11", "Fechamentos", "5 faces de vidro insulado 6 lam + 12 Ar + 6 temp low-e em alumínio bronze RPT com porta de correr PC1 2,00 x 2,40; 3 faces em SIP 100 mm + ripado; fresta da banheira J1; lanterna LZ1 em vidro laminado curvo 8 + 8 h 0,45"),
            ("12", "Instalações", "Quadro no ático; LED no anel de beiral, rodapés e lanterna; PEX; esgoto Ø100; evaporadora dutada 9k BTU"), ("13", "Acabamento e FF&E", "Parede-corda do banho em LSF + painel; marcenaria em carvalho; louças e metais; FF&E")],
}

def materials_pages(p):
    """PA-13 camadas e materiais · PA-14 quantidades estimadas (sem preços)."""
    if p not in LAYERS: return ""
    try:
        from product_book_data import bom_priced
        groups = bom_priced(p)
    except Exception:
        groups = []
    trs = "".join(f'<tr><td class="num">{n}</td><td><b>{html.escape(t)}</b></td><td>{html.escape(d)}</td></tr>' for n, t, d in LAYERS[p])
    pg1 = f'''<section class="sheet doc" id="{p}-PA-13"><div class="strip"><span class="code">PA-13</span><span class="ttl">Camadas construtivas e especificação de materiais</span><span class="scl">s/ escala</span><span class="prod">{NAME[p]}</span></div>
<div class="docbody"><table class="mat"><tr><th></th><th>Camada</th><th>Material e especificação</th></tr>{trs}</table>
<p class="docnote">Aço ASTM A500 grau B galvanizado a fogo (NBR 6323); ligações parafusadas classe 8.8, sem solda em campo; vento V0 = 45 m/s (NBR 6123); verificação estrutural NBR 8800. Pré-dimensionamento a validar por engenheiro habilitado (ART/RRT); form-finding da membrana com o fabricante; fundação definitiva após sondagem.</p></div></section>'''
    if not groups: return pg1
    rows = ""
    for g, items in groups:
        rows += f'<tr class="grp"><td colspan="3">{html.escape(g)}</td></tr>'
        for (desc, un, qtd, key) in items:
            q = f"{qtd:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".").rstrip("0").rstrip(",") if isinstance(qtd, float) else str(qtd)
            rows += f'<tr><td>{html.escape(desc)}</td><td>{html.escape(un)}</td><td class="num">{q}</td></tr>'
    pg2 = f'''<section class="sheet doc" id="{p}-PA-14"><div class="strip"><span class="code">PA-14</span><span class="ttl">Quadro de materiais estimados (quantidades)</span><span class="scl">s/ escala</span><span class="prod">{NAME[p]}</span></div>
<div class="docbody cols"><table class="mat small"><tr><th>Material / componente</th><th>Un.</th><th class="num">Qtd</th></tr>{rows}</table></div>
<p class="docnote">Quantidades estimadas a partir da geometria (perdas e emendas incluídas onde indicado), organizadas nos 18 grupos do kit de fábrica. Lista sem preços, para cotação e pedido de fabricação; peça a peça (código, dimensões, perfil, aço, espessura, peso, processo) no Product Book.</p></section>'''
    return pg1 + pg2

def cover():
    rows = ""
    for p in PRODUCTS:
        for (code, t, sc, rel, note) in sheets(p):
            rows += f'<tr><td>{TAG[p]}-{code}</td><td>{html.escape(t)}</td><td>{sc}</td><td>{NAME[p]}</td></tr>'
        for (code, t, sc) in INDEX_EXTRA:
            rows += f'<tr><td>{TAG[p]}-{code}</td><td>{html.escape(t)}</td><td>{sc}</td><td>{NAME[p]}</td></tr>'
    dx = ""
    for p in PRODUCTS:
        dx += "".join(f'<li><code>{p}/projeto/dxf/{f}</code></li>' for f in dxf_list(p))
    return f'''<section class="sheet cover">
<div class="coverl"><div class="brand">{zion_mark_html('13mm', style='margin-right:6mm')}{zion_logo_html('13mm')}</div><div class="sub">ZION GLAMPING COLLECTION</div>
<h1>PROJETO<br>ARQUITETÔNICO</h1><h2>ZION CASULO · ZION SAFARI · ZION LODGE</h2>
<p class="lead">Conjunto de pranchas de estudo preliminar / anteprojeto de produto industrializado: implantação, plantas cotadas e de layout, cobertura, forro e iluminação, cortes, fachadas, quadro de esquadrias, planta estrutural, detalhes construtivos, vistas isométricas, camadas construtivas e quadro de materiais estimados (sem preços). Arquivos DXF editáveis em CAD anexos.</p>
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
.sheet.doc{padding-bottom:6mm} .docbody{padding:4mm 8mm 0;flex:1;overflow:hidden} .docbody.cols{column-count:2;column-gap:10mm} table.mat{border-collapse:collapse;width:100%;font-size:11px;font-variant-numeric:tabular-nums} table.mat th{text-align:left;font-size:9px;letter-spacing:.14em;color:var(--earth);text-transform:uppercase;padding:2px 6px 6px;border-bottom:1px solid var(--earth)} table.mat td{padding:4px 6px;border-bottom:1px solid var(--sand);vertical-align:top;line-height:1.45} table.mat td.num{text-align:right;white-space:nowrap;color:var(--earth);font-weight:600} table.mat.small{font-size:9.5px} table.mat.small td{padding:2px 5px} table.mat tr.grp td{background:#F1EAE0;font-weight:600;letter-spacing:.1em;font-size:8.5px;text-transform:uppercase;color:var(--earth);break-after:avoid} table.mat tr{break-inside:avoid} .docnote{font-size:9.5px;color:var(--earth);padding:3mm 8mm 0;line-height:1.5}
.cover{flex-direction:row;padding:0} .coverl{width:40%;background:var(--black);color:var(--cream);padding:18mm 14mm} .coverr{flex:1;padding:14mm 12mm;font-size:10px}
.brand{display:flex;align-items:center} .sub{font-size:9px;letter-spacing:.3em;color:var(--sand);margin-bottom:26mm}
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
        body += materials_pages(p)
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

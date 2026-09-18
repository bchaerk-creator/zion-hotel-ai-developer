# -*- coding: utf-8 -*-
"""ZC-ARQ-002 · ZION CASULO SENSORIAL — variante do Casulo (sem sobrescrever o original).
Cinturão transparente nos vãos P3 e P4 (dos dois lados, do trilho de base a 1,85 m) com três camadas (cristal com zíper,
tela mosquiteira, cortina de voile + blackout), cama king com dossel no meio do cinturão olhando a fachada e o Bico,
lounge de chão sob o Bico, mini cozinha em L atrás junto ao banho, closet à direita; coleção de mobiliário Boho / Bali.
Saídas: cocoon_s/desenhos/*.svg (planta, elevação, corte, isométrica) e 07_VARIANTES/ZC-ARQ-002_Casulo_Sensorial.html (PDF via export_pdf.js)."""
import math, os, html
import numpy as np
from geometry import Cocoon, CocoonSensorial
from svgkit import *
from svgkit import zion_mark_html, zion_logo_html
import drawings_cocoon as DC, iso as ISO, lona, ffe
from build_projeto_arquitetonico import svg_inline
from build_tecnico import CSS as BASE_CSS

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "cocoon_s", "desenhos"); os.makedirs(OUT, exist_ok=True)
DOC_DIR = os.path.join(ROOT, "07_VARIANTES"); os.makedirs(DOC_DIR, exist_ok=True)
CS = CocoonSensorial(); CO = Cocoon()
DOC = "ZC-ARQ-002"; REV = "REV 00 — CONCEITO (VARIANTE)"; DATE = "18/09/2026"
CRYSTAL = "#BFD8E8"; CRYSTAL_L = "#4E8BB8"; VOILE = "#F1E8DA"
WARN = '<span class="warn">⚠️ VALIDAÇÃO OBRIGATÓRIA — ENGENHEIRO/ARQUITETO</span>'
COTAR = '<span class="cotar">PREÇO A COTAR</span>'

def esc(s): return html.escape(str(s))
def fmt(v, n=1):
    if isinstance(v, str): return esc(v)
    return f"{v:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ============================================================================ pranchas (com a geometria trocada em drawings_cocoon e iso)
def with_variant(fn, *a, **k):
    old_dc, old_iso = DC.C, ISO.C
    DC.C = CS; ISO.C = CS
    try: return fn(*a, **k)
    finally: DC.C, ISO.C = old_dc, old_iso

def planta_s():
    sh = Sheet(1600, 1000, scale=78, ox=390, oy=520)
    sh.header("Zion Casulo Sensorial · Planta de layout", "Variante: cinturão transparente nos vãos A2-A4 · cama com dossel olhando a fachada e o Bico · lounge de chão · mini cozinha em L junto ao banho · 1:50")
    outline, ring = with_variant(DC.shell_plan_pts); D = CS.DECK
    sh.rect(D["x1"], D["y1"], D["x2"], D["y2"], fill=sh.pattern("deck"), stroke=GREEN, sw=1.1)
    for i in range(3): sh.rect(D["x1"] - 0.3 * (i + 1), -1.2, D["x1"] - 0.3 * i, 1.2, fill=WOOD2, stroke=GREEN, sw=0.7)
    sh.poly(outline, fill=MEMB, stroke=GREEN, sw=1.6); sh.poly(with_variant(DC.bico_plan), fill=MEMB, stroke=GREEN, sw=1.4)
    floor = CS.floor_outline(100); sh.poly(floor, fill=sh.pattern("wood"), stroke=GREEN, sw=0.9)
    bath = [(x, y) for (x, y) in floor if x >= 6.3]; sh.poly(bath, fill=sh.pattern("tile"), stroke="none")
    for i, x in enumerate(CS.ARCH_X):
        pts = with_variant(DC.arch_plan, x); sh.poly(pts, close=False, stroke=EARTH, sw=0.8, dash="6 4", opacity=0.8); sh.text(pts[-1][0], pts[-1][1] + 0.18, f"A{i}", 10, EARTH)
    # cinturão transparente (projeção) nos dois lados
    cl = CS.CLEAR
    for s in (-1, 1):
        pts = [(x, s * (CS.a(x) + 0.03)) for x in np.linspace(cl["x1"], cl["x2"], 12)]
        sh.poly(pts, close=False, stroke=CRYSTAL, sw=9, opacity=0.95); sh.poly(pts, close=False, stroke=CRYSTAL_L, sw=1.2)
        inner = [(x, s * (CS.floor_hw(x) - 0.12)) for x in np.linspace(cl["x1"], cl["x2"], 12)]
        sh.poly(inner, close=False, stroke=EARTH, sw=1.0, dash="6 3")   # trilho curvo da cortina
    x1, x2, ht = CS.SPINE; hw = ht * CS.B_MAX
    sh.poly([(CS.shear(x1, 4.15), -hw), (CS.shear(x2, 4.15), -hw), (CS.shear(x2, 4.15), hw), (CS.shear(x1, 4.15), hw)], fill=GLASS, stroke=GREEN, sw=0.8, dash="3 3", opacity=0.9)
    for w in CS.WINDOWS:
        side = -1 if w["tc"] < math.pi / 2 else 1; xs = [w["xc"] - w["lx"], w["xc"] + w["lx"]]
        pts = [(CS.shear(x, 1.6), side * (CS.a(x) + 0.02)) for x in np.linspace(xs[0], xs[1], 11)]
        sh.poly(pts, close=False, stroke=GLASS, sw=5); sh.poly(pts, close=False, stroke=GREEN, sw=0.8)
    gr = [(x, y) for (x, y, z) in CS.glass_ring(60)]; sh.poly(gr, close=False, stroke=GLASS, sw=6, opacity=0.9); sh.poly(gr, close=False, stroke=GREEN, sw=1.0)
    sh.line(0.9, 0.6, 1.9, 0.6, GREEN, 1.2); sh.add(f'<path d="M{sh.X(1.9):.1f},{sh.Y(0.6):.1f} A{sh.s:.1f},{sh.s:.1f} 0 0 0 {sh.X(0.9):.1f},{sh.Y(1.6):.1f}" fill="none" stroke="{GREEN}" stroke-width="0.6" stroke-dasharray="3 3"/>')
    sh.rect(6.6, -2.85, 6.7, 0.95, fill=GREEN, stroke=GREEN, sw=0.5); sh.rect(6.6, 1.85, 6.7, 2.85, fill=GREEN, stroke=GREEN, sw=0.5); sh.line(6.65, 0.95, 6.65, 1.85, GREEN, 0.6, dash="4 3")
    sh.rect(7.3, 0.9, 7.35, 1.85, fill=GREEN, stroke=GREEN, sw=0.4)
    DC.draw_furniture(sh, CS.furniture(), True, skip=("ceiling", "hvac", "wall", "opening", "glass", "pillow", "cooktop", "appliance"))
    # dossel: colunas e véu
    for (x, y) in ((2.5, -1.15), (2.5, 1.15), (4.75, -1.15), (4.75, 1.15)): sh.circle(x, y, 0.045, fill=WOOD2, stroke=GREEN, sw=0.6)
    sh.rect(2.5, -1.15, 4.75, 1.15, fill="none", stroke=EARTH, sw=0.8, dash="2 2")
    sh.line(7.65, -1.75, 7.65, -0.8, GLASS, 4); sh.line(7.65, -1.75, 7.65, -0.8, GREEN, 0.8)
    for t, x, y, a in (("LOUNGE", 1.6, 0.0, "sob o Bico"), ("SUÍTE · DOSSEL", 3.6, 0.0, "cinturão transparente"), ("COZINHA", 5.9, 2.45, ""), ("CLOSET", 5.95, -2.5, ""), ("BANHO", 8.8, 1.1, "13,2 m²"), ("DECK", -1.5, 2.2, "29,9 m²")):
        sh.text(x, y, t, 11, GREEN, weight=700, spacing=0.2, dy=(0 if not a else -4))
        if a: sh.text(x, y, a, 9, EARTH, dy=10)
    sh.leader(4.0, 3.0, 1.2, 4.35, "Cinturão transparente T3/T4: cristal com zíper + tela mosquiteira + cortina de voile e blackout em trilho curvo", 11, anchor="start")
    sh.leader(3.6, 1.1, 3.6, -3.9, "Cama king com dossel em teca, véu de voile, pés para o vidro e o Bico", 11, anchor="start")
    sh.leader(5.9, 2.5, 6.6, 3.9, "Mini cozinha em L (1,35 + 0,65 m): geladeira, forno + cooktop de indução, cuba, air fryer", 11, anchor="start")
    sh.leader(1.5, -1.5, 0.2, -4.4, "Lounge de chão: futons, mesa de tronco, cadeira suspensa", 11, anchor="end")
    sh.leader(5.95, -2.5, 8.9, -3.35, "Closet 1,10 m contra a parede do banho", 11, anchor="start")
    sh.dim(2.85, 3.55, 5.25, 3.55, 0.75, label="2,40 (cinturão)", color=CRYSTAL_L)
    sh.dim(0.45, -3.55, 9.6, -3.55, -0.75, color=EARTH); sh.dim(-3.7, -3.55, 0.9, -3.55, -0.75, color=EARTH); sh.dim(10.9, -3.0, 10.9, 3.0, 0.55, label="6,00", color=EARTH)
    sh.north(1500, 140, angle=-90); sh.scalebar(-3.7, -5.55, 5)
    sh.title_block("ZION CASULO SENSORIAL", "Planta de layout · variante", "1:50 (A1) · cotas em metros", "VS-01", "Cinturão transparente A2-A4 · dossel · cozinha em L atrás · closet")
    return sh

def elev_s():
    sh = with_variant(DC.elev_lateral)
    cl = CS.CLEAR
    pts = [(CS.shear(cl["x1"], 0), 0), (CS.shear(cl["x2"], 0), 0), (CS.shear(cl["x2"], cl["z"]), cl["z"]), (CS.shear(cl["x1"], cl["z"]), cl["z"])]
    sh.poly(pts, fill=CRYSTAL, stroke=CRYSTAL_L, sw=1.4, opacity=0.9)
    for x in (CS.ARCH_X[3],): sh.line(CS.shear(x, 0), 0, CS.shear(x, cl["z"]), cl["z"], GREEN, 1.2)
    sh.line(CS.shear(cl["x1"], 0.12), 0.12, CS.shear(cl["x2"], 0.12), 0.12, "#C2734A", 3)
    sh.text((cl["x1"] + cl["x2"]) / 2, 0.9, "T3 · T4 · CRISTAL", 11, "#2F5F80", weight=700)
    sh.leader(4.6, 1.85, 6.4, 5.2, "Costura HF lona / cristal na linha da terça T5 (z 1,85)", 12)
    sh.leader(3.2, 0.12, 1.4, -1.5, "Zíper #10 na base: a parede abre; keder no trilho", 12, anchor="end")
    return sh

def corte_s():
    xc = 3.8
    sh = Sheet(1600, 1000, scale=120, ox=800, oy=720, flip_x=True)
    sh.header("Zion Casulo Sensorial · Corte transversal pelo cinturão", f"Plano x = {fmt(xc)} (suíte) · olhar para +x · as três camadas da lateral: cristal, tela, cortina · dossel · 1:40")
    sh.rect(-6.0, -0.9, 6.0, -0.02, fill=sh.pattern("soil"), stroke="none"); sh.line(-6.0, -0.02, 6.0, -0.02, GREEN, 1.0)
    for py in [-2.6, -1.3, 0.0, 1.3, 2.6]: sh.rect(py - 0.04, -0.9, py + 0.04, -0.22, fill=STEEL, stroke="none")
    sh.rect(-3.3, -0.2, 3.3, -0.05, fill=sh.pattern("insul"), stroke=GREEN, sw=0.9); sh.rect(-3.3, -0.05, 3.3, 0.0, fill=WOOD2, stroke=GREEN, sw=0.5)
    outer = CS.section_local(xc, 100); t0, t1 = CS.theta_range(xc)
    a, b = CS.a(xc) - 0.13, CS.b(xc) - 0.13
    inner = [(a * math.cos(t0 + (t1 - t0) * i / 100), max(0, CS.ZC + b * math.sin(t0 + (t1 - t0) * i / 100))) for i in range(101)]
    sh.poly(outer + inner[::-1], fill=sh.pattern("insul"), stroke=GREEN, sw=1.6)
    # cinturão transparente: o envelope vira uma folha só (cristal) abaixo de z 1,85
    zc = CS.CLEAR["z"]
    for s in (-1, 1):
        seg = [(y, z) for (y, z) in outer if s * y > 0 and z <= zc + 0.02]
        sh.poly(seg, close=False, stroke=CRYSTAL, sw=10, opacity=0.95); sh.poly(seg, close=False, stroke=CRYSTAL_L, sw=1.4)
        segi = [(y * 0.955, z) for (y, z) in seg if z > 0.15]
        sh.poly(segi, close=False, stroke="#7A7A7A", sw=1.0, dash="2 2")   # tela mosquiteira
        segc = [(y * 0.91, z) for (y, z) in seg if z > 0.15]
        sh.poly(segc, close=False, stroke=VOILE, sw=7, opacity=0.9); sh.poly(segc, close=False, stroke=EARTH, sw=0.8)   # cortina
        sh.circle(s * (CS.floor_hw(xc) - 0.12), zc - 0.05, 0.03, fill=STEEL, stroke="none")
    sh.rect(-0.35, CS.top(xc) - 0.14, 0.35, CS.top(xc) + 0.02, fill=GLASS, stroke=GREEN, sw=0.9)
    # tablado, cama, dossel
    sh.rect(-1.25, 0, 1.25, 0.15, fill=WOOD2, stroke=GREEN, sw=0.7); sh.rect(-0.97, 0.15, 0.97, 0.45, fill=WOOD2, stroke=GREEN, sw=0.8); sh.rect(-0.97, 0.45, 0.97, 0.77, fill="#FFFFFF", stroke=GREEN, sw=0.8)
    for y in (-1.15, 1.15): sh.rect(y - 0.045, 0.15, y + 0.045, 2.4, fill=WOOD2, stroke=GREEN, sw=0.7)
    sh.rect(-1.19, 2.36, 1.19, 2.4, fill=WOOD2, stroke=GREEN, sw=0.7)
    for y in (-1.15, 1.15): sh.line(y, 0.2, y, 2.35, VOILE, 5); sh.line(y, 0.2, y, 2.35, EARTH, 0.6, dash="3 2")
    sh.add(f'<g transform="translate({sh.X(-2.4):.1f},{sh.Y(0):.1f}) scale({sh.s / 100:.3f})"><circle cx="0" cy="-165" r="11" fill="none" stroke="{GREEN}" stroke-width="1.5"/><path d="M0 -152 V-70 M0 -70 L-16 0 M0 -70 L16 0 M-22 -100 L0 -135 L22 -100" fill="none" stroke="{GREEN}" stroke-width="1.5" stroke-linecap="round"/></g>')
    sh.leader(-2.75, 1.2, -4.2, 2.4, "1 · PVC cristal 0,7 mm (ou ETFE) soldado à lona, zíper na base", 12, anchor="start")
    sh.leader(-2.6, 0.9, -4.2, 1.7, "2 · tela mosquiteira no trilho de harpão", 12, anchor="start")
    sh.leader(-2.45, 0.6, -4.2, 1.0, "3 · voile de linho + blackout motorizado em trilho curvo", 12, anchor="start")
    sh.leader(2.75, 1.9, 4.2, 3.0, "costura HF lona / cristal na terça T5 (z 1,85)", 12, anchor="end")
    sh.leader(1.15, 2.4, 3.0, 3.8, "dossel em teca 2,40 m com véu de voile nas 4 faces", 12, anchor="end")
    sh.leader(0.0, CS.top(xc) + 0.02, 1.0, 4.6, "Espinha de Luz", 12, anchor="end")
    sh.leader(-1.25, 0.15, -3.2, -0.6, "tablado 0,15 com LED indireto", 12, anchor="start")
    sh.dim(-3.4, 0, -3.4, zc, -0.55, label=f"{fmt(zc, 2)} (cristal)", color=CRYSTAL_L); sh.dim(3.4, 0, 3.4, 2.4, 0.5, label="2,40 (dossel)")
    sh.scalebar(5.8, -2.0, 4)
    sh.title_block("ZION CASULO SENSORIAL", "Corte transversal pelo cinturão", "1:40 (A1)", "VS-03", "Três camadas: cristal com zíper, tela, cortina de voile + blackout")
    return sh

def build_sheets():
    planta_s().save(os.path.join(OUT, "02_planta_sensorial.svg"))
    elev_s().save(os.path.join(OUT, "05_elevacao_lateral_sensorial.svg"))
    corte_s().save(os.path.join(OUT, "07_corte_cinturao.svg"))
    with_variant(ISO.cocoon_iso, False).save(os.path.join(OUT, "08_isometrica_sensorial.svg"))
    print("sensorial sheets ok ->", OUT)

# ============================================================================ documento ZC-ARQ-002
pages = []
def sheet(rel): return f'<div class="sheet">{svg_inline(rel)}</div>' if os.path.exists(os.path.join(ROOT, rel)) else f'<div class="missing">[{esc(rel)}]</div>'
def img(rel): return f'<img src="../{rel.replace("/renders/web/", "/renders/web/deck/")}" alt="">' if os.path.exists(os.path.join(ROOT, rel)) else f'<div class="missing">[{esc(rel)}]</div>'
def table(head, rows, cls=""):
    th = "".join(f"<th>{esc(h)}</th>" for h in head)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="t {cls}"><tr>{th}</tr>{body}</table>'
def h(t, sub=""): return f'<h2>{esc(t)}{f"<small>{esc(sub)}</small>" if sub else ""}</h2>'
def page(body, label, cls="", code=""):
    n = len(pages) + 1
    pages.append(f'<section class="page {cls}"><div class="head"><span>{zion_mark_html("14px", color="#1B2117")} ZION CASULO SENSORIAL · {DOC} · {REV}</span><span>{esc(code or DOC)}</span><span>{esc(label)}</span></div>{body}<div class="foot"><span>ZION GLAMPING COLLECTION · VARIANTE SENSORIAL · SEM PREÇOS</span><span>UNIDADE: m</span><span>{DATE} · {n:02d}</span></div></section>')
def sheet_page(rel, code, title, note=""):
    n = len(pages) + 1
    pages.append(f'<section class="page sheetpage"><div class="strip"><span class="code">{esc(code)}</span><span class="ttl">{esc(title)}</span><span class="scl">ver prancha</span><span class="prod">{esc(note)}</span></div>{sheet(rel)}<div class="foot"><span>{DOC} · {REV} · {esc(code)}</span><span>{esc(title)}</span><span>{DATE} · {n:02d}</span></div></section>')

def build_doc():
    pats = lona.dedupe(lona.PATTERNS["cocoon_s"]())
    T = [p for p in pats if p.id.startswith("T")]
    clear = CS.clear_area(); memb_s, glass_s = CS.membrane_area(); memb_o, glass_o = CO.membrane_area()
    pages.append(f'''<section class="page cover"><div class="coverbox"><div class="brand">{zion_mark_html("13mm", color="#FEF5F0", style="margin-right:6mm")}{zion_logo_html("13mm", color="#FEF5F0")}</div><div class="sub">ZION GLAMPING COLLECTION · VARIANTE DO ZION CASULO</div>
<h1>CASULO<br>SENSORIAL</h1><h3>{DOC} · {REV} · {DATE}</h3>
<p class="lead">A mesma concha, os mesmos arcos, o mesmo Bico e o mesmo banho do Casulo. Muda o que se vê e onde se dorme: um cinturão transparente nos vãos da suíte, com cortina, que abre por zíper; uma cama com dossel e véu no meio dele, olhando a fachada de vidro e o Bico; um lounge de chão sob o Bico; a mini cozinha em L atrás, junto ao banho. Duas coleções de mobiliário: Zion New Luxury e Boho / Bali.</p>
<div class="stats"><div><b>{fmt(clear, 1)} m²</b><span>de cinturão transparente</span></div><div><b>4</b><span>painéis de cristal T3/T4</span></div><div><b>0</b><span>arcos alterados</span></div><div><b>{ffe.totals("cocoon_s")["n_items"]}</b><span>itens FF&amp;E Bali</span></div></div>
<p class="rule">Variante conceitual: não substitui o Casulo (ZC-ARQ-001 / ZG-TEC-001); reaproveita 100 % da estrutura, da fundação e do banho. Onde depende de cálculo ou norma, {WARN}. Sem preços: {COTAR}.</p></div></section>''')
    # 1 conceito e sistema
    body = h("O QUE MUDA E POR QUÊ", "sensorial com a natureza: ver, ouvir, sentir o ar; privacidade em camadas")
    body += f'''<div class="two"><div><h4>OS QUATRO MOVIMENTOS</h4>{table(["#", "Movimento", "Como"], [("1", "<b>Cinturão transparente</b>", "vãos A2-A3 e A3-A4 (x 2,85 a 5,25), dos dois lados, do trilho de base a z 1,85: a lona vira PVC cristal (ou ETFE), soldada por HF na linha da terça T5; zíper #10 na base abre a parede inteira"), ("2", "<b>Cama olhando a paisagem</b>", "king com dossel de teca a 2,40 m e véu de voile nas 4 faces (também mosquiteiro), sobre tablado de 0,15 m, no meio do cinturão; pés para o vidro e o Bico; sem cabeceira na parede"), ("3", "<b>Lounge de chão sob o Bico</b>", "futons, almofadas em kilim, mesa baixa de tronco, cadeira suspensa de rattan: leve, para sentar no chão e olhar a mata"), ("4", "<b>Cozinha atrás, junto ao banho</b>", "mini cozinha em L (1,35 m na concha + 0,65 m na parede do banho): geladeira, forno + cooktop de indução, cuba, air fryer; closet de 1,10 m do lado direito da mesma parede: água, esgoto e energia na mesma parede molhada")], "small")}
<h4>AS TRÊS CAMADAS DA LATERAL</h4>{table(["Camada", "Material", "Função"], [("1 · Cristal", "PVC cristal 0,7 mm (M2) ou ETFE 250 µm em 2 folhas (melhor no frio); keder Ø10 nos arcos, zíper na base", "vista, chuva, vento; abre nos dias bons"), ("2 · Tela", "tela mosquiteira poliéster 18 x 16 fios no trilho de harpão", "abrir a parede sem entrar bicho"), ("3 · Cortina", "voile de linho com barra de macramê + blackout motorizado em trilho curvo de alumínio a 0,12 m do forro", "privacidade e luz em camadas; blackout à noite e no inverno")], "small")}</div>
<div><h4>O QUE NÃO MUDA</h4><ul class="chk"><li>Concha, arcos A0 a A7, Bico, Espinha de Luz, fachada de vidro, banho na cauda, fundação, grelha, deck</li><li>Lotes 1 e 2 idênticos ao Casulo (mesma estrutura metálica e mesma infraestrutura)</li><li>Lote 3: 4 painéis de lona viram cristal (T3D/E, T4D/E); os demais são iguais</li><li>Lote 4: nova coleção de mobiliário (Bali) ou a atual (New Luxury), sobre a mesma marcenaria acoplada</li></ul>
<h4>NÚMEROS</h4>{table(["", "Casulo", "Sensorial"], [("Membrana opaca (m²)", fmt(memb_o, 1), fmt(memb_s, 1)), ("Vidro + cristal na concha (m²)", fmt(glass_o, 1), fmt(glass_s, 1)), ("Cinturão transparente (m²)", "—", fmt(clear, 1)), ("Janelas Olho", "6", "3 (as 3 da suíte viram cinturão)"), ("Cama", "x 4,50 a 6,55, cabeceira no banho", "x 2,60 a 4,65, dossel, pés para o vidro"), ("Cozinha", "x 1,20 a 3,20 (estar)", "x 5,25 a 6,60 em L (junto ao banho)"), ("Closet", "x 3,40 a 4,50", "x 5,40 a 6,50 (dir.)")], "small")}
<h4>ATENÇÃO</h4><p class="lede">Sem isolamento nas laterais do cinturão: carga térmica de inverno maior (climatização 12k → 18k BTU a confirmar), risco de condensação no cristal em noites frias (ETFE duplo reduz), e o blackout cumpre a privacidade à noite. {WARN} para o balanço térmico e para a fixação do dossel (peso próprio + cadeira suspensa no arco A1).</p></div></div>'''
    page(body, "Conceito e sistema", code="ZC-ARQ-002")
    sheet_page("cocoon_s/desenhos/02_planta_sensorial.svg", "VS-01", "Planta de layout · variante sensorial", "1:50")
    sheet_page("cocoon_s/desenhos/05_elevacao_lateral_sensorial.svg", "VS-02", "Elevação lateral com o cinturão transparente", "1:50")
    sheet_page("cocoon_s/desenhos/07_corte_cinturao.svg", "VS-03", "Corte transversal pelo cinturão: as três camadas e o dossel", "1:40")
    sheet_page("cocoon_s/desenhos/08_isometrica_sensorial.svg", "VS-04", "Isométrica da variante", "s/ escala")
    # renders comparativos (2 páginas, 2 x 2)
    for title, views in (("EXTERIOR", (("ext_front", "Exterior frontal"), ("ext_side", "Exterior lateral"))), ("INTERIOR", (("int_bed", "Interior · suíte"), ("int_living", "Interior · estar / lounge")))):
        body = h(f"RENDERS {title} · CASULO E CASULO SENSORIAL LADO A LADO", "modelo 3D da variante (cocoon_s/3d) · mesma câmera nas duas versões") + '<div class="grid2">'
        for v, lab in views:
            body += f'<div><h4>{lab.upper()} · CASULO</h4>{img(f"cocoon/renders/web/cocoon_{v}.jpg")}</div><div><h4>{lab.upper()} · SENSORIAL</h4>{img(f"cocoon_s/renders/web/cocoon_s_{v}.jpg")}</div>'
        body += '</div>'
        page(body, f"Renders comparativos · {title.lower()}", code="ZC-ARQ-002-R")
    # lona
    body = h("LONA · O QUE MUDA NO LOTE 3", f"{len(T)} padrões de cristal (T) substituem a parte baixa dos painéis P3 e P4 · costura HF lona / cristal na terça T5 · zíper na base · mapa e padrões em cocoon_s/lona/")
    rows = [(p.id, p.qty, fmt(p.w, 2) + " x " + fmt(p.h, 2), fmt(p.area, 2), esc(p.material[:110])) for p in pats if p.id[0] in "TP" and p.id[1] in "34"]
    body += table(["Cód.", "Qtd", "Caixa (m)", "m²", "Material"], rows, "small")
    body += '<p class="note">Os demais painéis (P0 a P2, P5 a P8, forros F1 a F8) são os mesmos do Casulo. O confeccionista solda o cristal à lona em fábrica; o painel chega como uma peça só por lado e vão, com o zíper e os keders prontos.</p>'
    page(body, "Lona: painéis de cristal", code="ZCS-LON-001")
    sheet_page("cocoon_s/lona/LN-01_mapa_paineis.svg", "LN-01", "Mapa dos painéis · variante sensorial", "cristal em azul")
    for f in sorted(os.listdir(os.path.join(ROOT, "cocoon_s", "lona"))):
        if f.startswith("LN-") and "_T" in f: sheet_page(f"cocoon_s/lona/{f}", f.split("_")[0], f.split("_", 1)[1].replace(".svg", "") + " · padrão de corte do cristal", "ver malha (m)")
    # mobiliário Bali
    R = ffe.rows("cocoon_s"); cats = {}
    for r in R: cats.setdefault(r["cat_name"], []).append(r)
    body = h("COLEÇÃO BOHO / BALI · FF&E DA VARIANTE", f"{len(R)} itens · dossel, tablado, rattan, futons, voile, juta, macramê, cerâmica, lanternas de latão · sem preços ({COTAR})")
    body += f'<div class="two"><div><h4>DIREÇÃO DE ARTE</h4>{table(["Tema", "Escolha"], [("Paleta", "creme, areia, terracota, oliva, madeira clara de teca"), ("Materiais", "teca e bambu laminado, rattan natural (sintético no deck), linho, algodão cru, juta, kilim, cerâmica artesanal, latão"), ("Luz", "2700 K, pendentes de rattan, lanternas de vela LED, LED indireto no tablado e no rodapé; nenhuma luz direta sobre a cama"), ("Umidade de montanha", "tecidos antimofo, madeira tratada, rattan sintético nas peças externas, ventilação cruzada com o cinturão aberto"), ("Ritual", "chá e café na cozinha atrás, banho de banheira sob o Olho baixo, deck com daybed suspenso sob o Bico")], "small")}<h4>A OUTRA COLEÇÃO</h4><p class="lede">Zion New Luxury (carvalho, quartzito, latão, linho cru) continua disponível para a variante: só o mobiliário solto muda; a marcenaria acoplada (cozinha, closet, bancada) é a mesma.</p></div><div>'
    for c, rs in cats.items():
        body += f"<h4>{esc(c.upper())}</h4>" + table(["Cód.", "Item", "Un.", "Qtd", "Ambiente"], [(r["code"], esc(r["desc"]), esc(r["un"]), fmt(r["qty"], 1).rstrip("0").rstrip(","), esc(r["amb"] + (" · " + r["obs"] if r["obs"] else ""))) for r in rs], "xsmall")
    body += "</div></div>"
    page(body, "Coleção Bali · FF&E", "flow", code="ZCS-FFE-001")
    # próximos passos
    body = h("IMPACTOS NOS LOTES E PRÓXIMOS PASSOS", "como a variante entra no master plan sem duplicar contratos")
    body += table(["Lote", "Casulo", "Sensorial: o que muda"], [("1 · Deck e infra", "igual", "pontos de água / esgoto da cozinha passam para a parede do banho (mesma parede molhada: mais simples); circuito da cortina motorizada"), ("2 · Estrutura", "igual", "talões para o trilho curvo da cortina e para a cadeira suspensa (arco A1); cantoneiras da cozinha em A5 / A6 em vez de A1 / A2"), ("3 · Lonas e vidros", "P3D/E, P4D/E em lona", "T3D/E, T4D/E em cristal soldado; zíperes; tela mosquiteira; trilhos curvos de cortina; 3 Olhos a menos"), ("4 · Mobílias", "New Luxury", "coleção Bali (dossel, tablado, rattan, futons, voile, juta) ou New Luxury; mesma marcenaria acoplada")], "small")
    body += f'<h4>PRÓXIMOS PASSOS</h4><ol class="num"><li>Aprovar a variante como produto (Casulo Sensorial) ou como opção de configuração do Casulo.</li><li>Balanço térmico e escolha entre PVC cristal e ETFE duplo por região (frio de montanha: ETFE). {WARN}</li><li>Detalhar o dossel (fixação no tablado, carga da cadeira suspensa) e o trilho curvo da cortina.</li><li>Gerar IN-01 a IN-06 da variante e os lotes 3 e 4 específicos.</li><li>Render fotorrealista (imagem → vídeo) com a coleção Bali para o material comercial.</li></ol>'
    page(body, "Impactos e próximos passos", code="ZC-ARQ-002-N")
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · {DOC} · Casulo Sensorial</title><style>{BASE_CSS} .page img{{width:100%;height:auto;display:block;border:1px solid var(--sand)}} .grid2{{display:grid;grid-template-columns:1fr 1fr;gap:10px 14px}} .grid2 h4{{margin:4px 0}}</style></head><body>{"".join(pages)}</body></html>'
    out = os.path.join(DOC_DIR, "ZC-ARQ-002_Casulo_Sensorial.html"); open(out, "w", encoding="utf-8").write(doc)
    print(out, len(pages), "páginas")

if __name__ == "__main__":
    build_sheets(); build_doc()

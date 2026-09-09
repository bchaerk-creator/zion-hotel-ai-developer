# -*- coding: utf-8 -*-
"""Desenhos técnicos 2D do ZION COCOON: plantas, elevações e cortes (SVG)."""
import math, os
from geometry import Cocoon
from svgkit import *

C = Cocoon()
OUT = os.path.join(os.path.dirname(__file__), "..", "cocoon", "desenhos")

# ------------------------------------------------------------------ símbolos
def sym_bed(sh, x1, x2, y1, y2, human):
    sh.rect(x1, y1, x2, y2, fill="#FFFFFF" if human else "none", stroke=GREEN, sw=1.0)
    # travesseiros junto à cabeceira (x2)
    for yy in (y1 + 0.12, (y1 + y2) / 2 + 0.06):
        sh.rect(x2 - 0.55, yy, x2 - 0.12, yy + (y2 - y1) / 2 - 0.18, fill="#F4EFE8" if human else "none", stroke=GREEN, sw=0.7)
    # dobra do lençol
    sh.line(x1 + 0.5, y1, x1 + 0.5, y2, GREEN, 0.6)
    sh.line(x1 + 0.5, y1, x1 + 0.35, y1 + 0.35, GREEN, 0.6)
def sym_table(sh, x1, x2, y1, y2, human):
    sh.rect(x1, y1, x2, y2, fill=WOOD2 if human else "none", stroke=GREEN, sw=0.8)
def sym_cabinet(sh, x1, x2, y1, y2, human):
    sh.rect(x1, y1, x2, y2, fill=WOOD2 if human else "none", stroke=GREEN, sw=0.9)
    sh.line(x1, y1, x2, y2, GREEN, 0.5); sh.line(x1, y2, x2, y1, GREEN, 0.5)
def sym_sofa(sh, x1, x2, y1, y2, human, back="y1"):
    sh.rect(x1, y1, x2, y2, fill=SAND if human else "none", stroke=GREEN, sw=0.9)
    if back == "y1": sh.rect(x1, y1, x2, y1 + 0.18, fill="#CFC3A8" if human else "none", stroke=GREEN, sw=0.6)
    elif back == "x2": sh.rect(x2 - 0.18, y1, x2, y2, fill="#CFC3A8" if human else "none", stroke=GREEN, sw=0.6)
    elif back == "x1": sh.rect(x1, y1, x1 + 0.18, y2, fill="#CFC3A8" if human else "none", stroke=GREEN, sw=0.6)
def sym_chair(sh, x1, x2, y1, y2, human):
    sh.rect(x1, y1, x2, y2, fill=SAND if human else "none", stroke=GREEN, sw=0.9)
    sh.rect(x1, y1, x2, y1 + 0.15, fill="#CFC3A8" if human else "none", stroke=GREEN, sw=0.6)
def sym_vanity(sh, x1, x2, y1, y2, human):
    sh.rect(x1, y1, x2, y2, fill="#EFEDE6" if human else "none", stroke=GREEN, sw=0.9)
    sh.circle((x1 + x2) / 2, (y1 + y2) / 2, 0.19, fill="#FFFFFF" if human else "none", stroke=GREEN, sw=0.8)
def sym_wc(sh, x1, x2, y1, y2, human):
    cx = (x1 + x2) / 2; cy = (y1 + y2) / 2
    sh.add(f'<ellipse cx="{sh.X(cx):.1f}" cy="{sh.Y(cy - 0.05):.1f}" rx="{0.19 * sh.s:.1f}" ry="{0.25 * sh.s:.1f}" fill="{"#FFFFFF" if human else "none"}" stroke="{GREEN}" stroke-width="0.9"/>')
    sh.rect(cx - 0.22, y2 - 0.16, cx + 0.22, y2, fill="#FFFFFF" if human else "none", stroke=GREEN, sw=0.8)
def sym_shower(sh, x1, x2, y1, y2, human):
    sh.rect(x1, y1, x2, y2, fill=sh.pattern("tile") if human else "none", stroke=GREEN, sw=0.9)
    sh.line(x1, y1, x2, y2, GREEN, 0.4); sh.line(x1, y2, x2, y1, GREEN, 0.4)
    sh.circle((x1 + x2) / 2, (y1 + y2) / 2, 0.05, stroke=GREEN, sw=0.7)
def sym_tub(sh, x1, x2, y1, y2, human):
    rx = 0.3 * sh.s
    sh.add(f'<rect x="{sh.X(x1):.1f}" y="{sh.Y(y2):.1f}" width="{(x2 - x1) * sh.s:.1f}" height="{(y2 - y1) * sh.s:.1f}" rx="{rx}" fill="{"#FFFFFF" if human else "none"}" stroke="{GREEN}" stroke-width="1.0"/>')
    sh.add(f'<rect x="{sh.X(x1 + 0.1):.1f}" y="{sh.Y(y2 - 0.1):.1f}" width="{(x2 - x1 - 0.2) * sh.s:.1f}" height="{(y2 - y1 - 0.2) * sh.s:.1f}" rx="{rx * 0.8}" fill="none" stroke="{GREEN}" stroke-width="0.5"/>')

def draw_furniture(sh, items, human, skip=("ceiling", "hvac", "wall", "opening", "glass", "pillow")):
    for f in items:
        k = f["kind"]
        if k in skip: continue
        if "r" in f:
            sh.circle(f["x"], f["y"], f["r"], fill=WOOD2 if human else "none", stroke=GREEN, sw=0.8); continue
        a = (sh, f["x1"], f["x2"], f["y1"], f["y2"], human)
        if k == "bed": sym_bed(*a)
        elif k == "table" or k == "bench": sym_table(*a)
        elif k == "cabinet" or k == "totem": sym_cabinet(*a)
        elif k == "sofa": sym_sofa(*a, back="y1" if f["y1"] < -1 else "x2")
        elif k == "chair": sym_chair(*a)
        elif k == "vanity": sym_vanity(*a)
        elif k == "wc": sym_wc(*a)
        elif k == "shower": sym_shower(*a)
        elif k == "tub": sym_tub(*a)
        elif k == "condenser":
            sh.rect(f["x1"], f["y1"], f["x2"], f["y2"], fill="#E5E1D8" if human else "none", stroke=GREEN, sw=0.8)
            sh.text((f["x1"] + f["x2"]) / 2, (f["y1"] + f["y2"]) / 2, "COND.", 8, dy=3)

# ------------------------------------------------------------------ contornos
def shell_plan_pts():
    """contorno externo da concha em planta (projeção), incluindo lábio frontal."""
    ring = [(x, y) for (x, y, z) in C.front_ring(80)]     # já cisalhado
    right = [(x, -C.a(x)) for x in [0.5 + (C.L - 0.5) * i / 120 for i in range(121)]]
    left = [(x, C.a(x)) for x in [0.5 + (C.L - 0.5) * i / 120 for i in range(121)]]
    # anel: começa em (0.5,-2.47) -> topo (-0.05,0) -> (0.5, 2.47) (ordem do theta: de -t0 até pi+t0)
    ring_front = [(x, y) for (x, y) in ring if True]
    return right + left[::-1], ring_front

def arch_plan(x):
    return [(px, py) for (px, py, pz) in C.section_curve(x, 40)]

# ------------------------------------------------------------------ PLANTA
def planta(human=True):
    sh = Sheet(1600, 1000, scale=78, ox=390, oy=520)
    sh.header("Zion Cocoon · Planta baixa " + ("humanizada" if human else "técnica"),
              "Cabana biomórfica em casulo · 9,60 x 6,00 x 4,20 m · piso interno 45,6 m² + vestíbulo 2,4 m² = 48 m² · deck 29,9 m² · total 78 m²")
    outline, ring = shell_plan_pts()
    D = C.DECK
    # deck
    sh.rect(D["x1"], D["y1"], D["x2"], D["y2"], fill=sh.pattern("deck") if human else "none", stroke=GREEN, sw=1.1)
    # escada
    for i in range(3):
        sh.rect(D["x1"] - 0.3 * (i + 1), -1.2, D["x1"] - 0.3 * i, 1.2, fill=WOOD2 if human else "none", stroke=GREEN, sw=0.7)
    # sombra da concha sobre o deck (projeção)
    sh.poly(outline, fill=MEMB if human else "none", stroke=GREEN, sw=1.6, opacity=1.0)
    # piso interno
    floor = C.floor_outline(100)
    sh.poly(floor, fill=sh.pattern("wood") if human else "none", stroke=GREEN, sw=0.9)
    # banho (piso porcelanato)
    if human:
        bath = [(x, y) for (x, y) in floor if x >= 6.3]
        sh.poly(bath, fill=sh.pattern("tile"), stroke="none")
    # arcos (projeção)
    for i, x in enumerate(C.ARCH_X):
        pts = arch_plan(x)
        sh.poly(pts, close=False, stroke=STEEL if not human else EARTH, sw=0.8, dash="6 4", opacity=0.8)
        if not human:
            sh.text(pts[-1][0], pts[-1][1] + 0.18, f"A{i}", 10, EARTH)
    # espinha de luz
    x1, x2, ht = C.SPINE
    hw = ht * C.B_MAX
    spine = [(C.shear(x1, 4.15), -hw), (C.shear(x2, 4.15), -hw), (C.shear(x2, 4.15), hw), (C.shear(x1, 4.15), hw)]
    sh.poly(spine, fill=GLASS if human else "none", stroke=GREEN, sw=0.8, dash="3 3", opacity=0.9)
    # janelas olho: marcar no contorno com traço grosso de vidro
    for w in C.WINDOWS:
        side = -1 if w["tc"] < math.pi / 2 else 1
        xs = [w["xc"] - w["lx"], w["xc"] + w["lx"]]
        pts = [(C.shear(x, 1.6), side * (C.a(x) + 0.02)) for x in [xs[0] + (xs[1] - xs[0]) * i / 10 for i in range(11)]]
        sh.poly(pts, close=False, stroke=GLASS if human else GREEN, sw=5 if human else 3, opacity=1)
        sh.poly(pts, close=False, stroke=GREEN, sw=0.8)
    # fachada de vidro (anel inclinado) e porta pivotante
    gr = [(x, y) for (x, y, z) in C.glass_ring(60)]
    sh.poly(gr, close=False, stroke=GLASS, sw=6, opacity=0.9 if human else 0.6)
    sh.poly(gr, close=False, stroke=GREEN, sw=1.0)
    # porta pivotante 1,00 m (y 0,60 a 1,60) girando para dentro
    sh.line(0.9, 0.6, 0.9 + 1.0, 0.6, GREEN, 1.2)
    sh.add(f'<path d="M{sh.X(1.9):.1f},{sh.Y(0.6):.1f} A{sh.s:.1f},{sh.s:.1f} 0 0 0 {sh.X(0.9):.1f},{sh.Y(1.6):.1f}" fill="none" stroke="{GREEN}" stroke-width="0.6" stroke-dasharray="3 3"/>')
    # parede do banho e porta de correr
    sh.rect(6.6, -2.85, 6.7, 0.95, fill=GREEN, stroke=GREEN, sw=0.5)
    sh.rect(6.6, 1.85, 6.7, 2.85, fill=GREEN, stroke=GREEN, sw=0.5)
    sh.line(6.65, 0.95, 6.65, 1.85, GREEN, 0.6, dash="4 3")
    sh.rect(6.72, 0.1, 6.78, 0.98, fill="none", stroke=GREEN, sw=0.8)  # folha de correr recolhida
    # divisória da bacia
    sh.rect(7.3, 0.9, 7.35, 1.85, fill=GREEN, stroke=GREEN, sw=0.4)
    # mobiliário
    draw_furniture(sh, C.furniture(), human)
    # box do chuveiro (vidro)
    sh.line(7.65, -1.75, 7.65, -0.8, GLASS, 4); sh.line(7.65, -1.75, 7.65, -0.8, GREEN, 0.8)
    # rótulos
    lab = [("VESTÍ-​BULO", 0.68, 0.0, ""), ("ESTAR", 2.6, 0.25, "20,4 m²"), ("SUÍTE", 5.5, 0.0, "12,0 m²"),
           ("BANHO", 8.8, 1.1, "13,2 m²"), ("DECK", -1.5, 2.2, "29,9 m²")]
    for t, x, y, a in lab:
        sh.text(x, y, t, 12, GREEN, weight=700, spacing=0.22, dy=(0 if not a else -4))
        if a: sh.text(x, y, a, 10, EARTH, dy=10)
    if human:
        sh.text(2.05, -0.95, "", 8)
        sh.leader(1.9, 1.9, 1.6, 3.6, "Console café / minibar 1,40 m", 11, anchor="end")
        sh.leader(3.8, 1.9, 5.2, 3.6, "Armário baixo embutido na curva", 11)
        sh.leader(4.9, -3.05, 4.5, -3.95, "Janelas Olho 1,60 x 0,95 (basculantes)", 11)
        sh.leader(4.3, 0.0, 4.8, -3.6, "Espinha de Luz 0,70 x 4,70 m", 11)
        sh.leader(8.3, 0.0, 9.4, 2.0, "Banheira na cauda 1,60 x 0,76", 11)
        sh.leader(0.95, 1.1, -1.6, 3.6, "Porta pivotante 1,00 x 2,40", 11, anchor="end")
        sh.leader(10.3, -0.05, 10.0, -2.7, "Condensadora oculta por ripado", 11)
        sh.leader(0.2, -2.0, -0.9, -3.95, "Lábio frontal inclinado 8° (beiral)", 11)
        sh.leader(1.9, -1.85, 1.3, -3.65, "Chaise de contemplação", 11)
    # cotas gerais
    sh.dim(0.45, -3.55, 9.6, -3.55, -0.75, color=EARTH)
    sh.dim(-3.7, -3.55, 0.9, -3.55, -0.75, color=EARTH)
    sh.dim(-3.7, -3.55, 9.6, -3.55, -1.35, label="13,30 (deck + concha)", color=EARTH)
    sh.dim(10.9, -3.0, 10.9, 3.0, 0.55, label="6,00", color=EARTH)
    sh.dim(-4.1, -3.25, -4.1, 3.25, -0.4, label="6,50", color=EARTH)
    if not human:
        # cadeia dos arcos
        xs = [0.45, 1.65, 2.85, 4.05, 5.25, 6.45, 7.65, 8.75, 9.6]
        sh.dim_chain(xs, 3.5, 0.45)
        sh.dim(0.9, 3.5, 6.6, 3.5, 1.05, label="5,70 (estar + suíte)")
        sh.dim(6.6, 3.5, 9.4, 3.5, 1.05, label="2,80 (banho)")
        sh.dim(0.45, 3.5, 0.9, 3.5, 1.05, label="0,45")
        sh.dim(-3.7, 3.5, 0.9, 3.5, 1.05, label="4,60 (deck)")
        # larguras internas
        sh.dim(3.4, -2.93, 3.4, 2.93, 0, label="5,86", color=EARTH)
        sh.dim(8.0, -2.40, 8.0, 2.40, 0, label="4,80", color=EARTH)
        sh.dim(2.0, -2.91, 2.0, 2.91, 0, label="5,82", color=EARTH)
        # janelas
        for w in C.WINDOWS[:3]:
            sh.dim(w["xc"] - w["lx"], -3.05, w["xc"] + w["lx"], -3.05, -0.35, color=EARTH, size=10)
        # estacas (malha 2,4 m)
        npiles = 0
        for px in [-3.3, -1.1, 0.9, 2.1, 3.3, 4.5, 5.7, 6.9, 8.1, 9.0]:
            for py in [-2.6, -1.3, 0.0, 1.3, 2.6]:
                if px < 0.9 and abs(py) > 2.9: continue
                if px >= 1.0 and abs(py) > C.floor_hw(px) - 0.1 and abs(py) > 0.1: continue
                npiles += 1
                sh.add(f'<g transform="translate({sh.X(px):.1f},{sh.Y(py):.1f})"><circle r="4" fill="none" stroke="{STEEL}" stroke-width="0.9"/><line x1="-4" y1="0" x2="4" y2="0" stroke="{STEEL}" stroke-width="0.7"/><line x1="0" y1="-4" x2="0" y2="4" stroke="{STEEL}" stroke-width="0.7"/></g>')
        sh.text(-3.7, 5.0, f"○+ estaca helicoidal Ø76 / hélice Ø300 (malha 1,20 x 1,30 m, {npiles} un.)", 10, STEEL, anchor="start")
        # marcas de corte
        for (x, y1, y2, lbl) in [(5.0, -3.4, 3.4, "B")]:
            sh.line(x, y1, x, y2, GREEN, 1.4, dash="10 4")
            sh.text(x, y2 + 0.2, lbl, 12, weight=700); sh.text(x, y1 - 0.35, lbl, 12, weight=700)
        sh.line(-4.0, 0.0, 11.0, 0.0, GREEN, 1.4, dash="10 4")
        sh.text(-4.25, 0.0, "A", 12, weight=700, dy=4); sh.text(11.25, 0.0, "A", 12, weight=700, dy=4)
    sh.north(1500, 140, angle=-90)
    sh.scalebar(-3.7, -5.55, 5)
    sh.title_block("ZION COCOON", "Planta baixa " + ("humanizada" if human else "técnica cotada"), "1:50 (A1) · cotas em metros", "02/27" if human else "03/27",
                   "Layout: vestíbulo, estar, suíte king, banho com banheira na cauda")
    return sh

# ------------------------------------------------------------------ ELEVAÇÃO FRONTAL
def elev_frontal():
    sh = Sheet(1600, 1000, scale=110, ox=800, oy=720, flip_x=True)
    sh.header("Zion Cocoon · Elevação frontal", "Vista da fachada panorâmica (olhar para +x) · largura 6,00 m · altura 4,20 m")
    # solo e deck
    sh.rect(-6.5, -0.6, 6.5, -0.02, fill=sh.pattern("soil"), stroke="none")
    sh.line(-6.5, -0.02, 6.5, -0.02, GREEN, 1.0)
    # estacas e vigas
    for py in [-2.6, -1.3, 0.0, 1.3, 2.6]:
        sh.rect(py - 0.04, -0.6, py + 0.04, -0.2, fill=STEEL, stroke="none")
    sh.rect(-3.25, -0.2, 3.25, -0.05, fill=WOOD2, stroke=GREEN, sw=0.9)   # deck (borda)
    sh.rect(-3.25, -0.05, 3.25, 0.0, fill=GREEN, stroke="none")
    # silhueta máxima (seção em x = 3,2)
    sil = [(y, z) for (y, z) in C.section_local(C.XMAX, 90)]
    sh.poly(sil, fill=MEMB, stroke=GREEN, sw=1.8)
    # anel do lábio (A0)
    ring = [(y, z) for (x, y, z) in C.front_ring(90)]
    sh.poly(ring, fill="#E4DCCB", stroke=GREEN, sw=1.4)
    # fachada de vidro no anel interno
    gr = [(y, z) for (x, y, z) in C.glass_ring(90)]
    sh.poly(gr, fill=GLASS, stroke=GREEN, sw=1.2, opacity=0.9)
    # montantes e travessa
    for yy in (-1.6, -0.5, 0.5, 1.6):
        zt = C.ZC + (C.b(C.X_GLASS) - 0.06) * math.sqrt(max(0, 1 - (yy / (C.a(C.X_GLASS) - 0.06)) ** 2))
        sh.line(yy, 0, yy, zt, GREEN, 1.2)
    sh.line(-2.3, 2.4, 2.3, 2.4, GREEN, 1.2)
    # porta pivotante (y 0,6..1,6)
    sh.rect(0.6, 0.0, 1.6, 2.4, fill="none", stroke=GREEN, sw=1.6)
    sh.circle_px(1.45, 1.05, 3, fill=GREEN)
    # interior visível: cama (sugerida), parede do fundo
    sh.rect(-0.97, 0.0, 0.97, 0.62, fill="#FFFFFF", stroke=GREEN, sw=0.6, opacity=0.8)
    sh.rect(-0.97, 0.62, 0.97, 1.0, fill="none", stroke=GREEN, sw=0.5, opacity=0.5)
    # espinha de luz no topo
    sh.rect(-0.35, C.top(C.XMAX) - 0.1, 0.35, C.top(C.XMAX) + 0.02, fill=GLASS, stroke=GREEN, sw=0.8)
    # rótulo de material
    sh.leader(-2.6, 2.7, -4.2, 3.4, "Membrana PVDF 1050 g/m² tensionada", 12, anchor="start")
    sh.leader(-2.45, 1.4, -4.2, 2.2, "Anel do lábio Ø101,6 inclinado 8°", 12, anchor="start")
    sh.leader(0.0, 4.17, 1.6, 4.7, "Espinha de Luz (claraboia 0,70 m)", 12, anchor="end")
    sh.leader(-1.05, 1.9, -4.2, 1.1, "Vidro duplo 6 lam + 12 Ar + 6 temp, low-e", 12, anchor="start")
    sh.leader(1.1, 1.2, 3.6, 1.9, "Porta pivotante 1,00 x 2,40", 12, anchor="end")
    sh.leader(2.6, 0.7, 3.9, 0.3, "Esquadria de alumínio bronze, ruptura térmica", 12, anchor="end")
    sh.leader(2.6, -0.4, 3.9, -1.1, "Deck cumaru sobre vigas U 150 e estacas helicoidais", 12, anchor="end")
    # cotas
    sh.dim(-3.0, -0.9, 3.0, -0.9, -0.35, label="6,00")
    sh.dim(-2.44, -0.9, 2.44, -0.9, -0.9, label="4,88 (anel frontal)")
    sh.dim(-3.25, -0.9, 3.25, -0.9, -1.45, label="6,50 (deck)")
    sh.dim(-3.6, 0, -3.6, 4.2, -0.5, label="4,20")
    sh.dim(-3.6, 0, -3.6, 2.4, -1.15, label="2,40 (porta)")
    sh.dim(3.6, -0.6, 3.6, 0, 0.5, label="0,60")
    sh.scalebar(6.3, -1.9, 4)
    sh.title_block("ZION COCOON", "Elevação frontal", "1:50 (A1)", "04/27", "Fachada panorâmica em anel inclinado 8°, 8 arcos elípticos")
    return sh

# ------------------------------------------------------------------ ELEVAÇÃO LATERAL
def top_profile():
    return [(C.shear(x, C.top(x)), C.top(x)) for x in [0.5 + (C.L - 0.5) * i / 160 for i in range(161)]]
def bottom_profile():
    """base da concha na lateral: z=0 até onde a concha toca o piso; depois a cauda sobe."""
    pts = []
    for x in [0.5 + (C.L - 0.5) * i / 160 for i in range(161)]:
        b = C.b(x)
        zb = 0.0 if b >= C.ZC else C.ZC - b
        pts.append((C.shear(x, zb), zb))
    return pts

def elev_lateral():
    sh = Sheet(1600, 1000, scale=100, ox=470, oy=720)
    sh.header("Zion Cocoon · Elevação lateral direita", "Vista do lado das Janelas Olho (olhar para +y) · comprimento 9,75 m com lábio · deck 4,60 m")
    # solo
    sh.rect(-4.0, -0.6, 11.0, -0.02, fill=sh.pattern("soil"), stroke="none")
    sh.line(-4.0, -0.02, 11.0, -0.02, GREEN, 1.0)
    for px in [-3.3, -1.1, 0.9, 2.1, 3.3, 4.5, 5.7, 6.9, 8.1, 9.0]:
        sh.rect(px - 0.04, -0.6, px + 0.04, -0.2, fill=STEEL, stroke="none")
    sh.rect(-3.7, -0.2, 9.6, -0.05, fill=WOOD2, stroke=GREEN, sw=0.9)
    sh.rect(-3.7, -0.05, 9.6, 0.0, fill=GREEN, stroke="none")
    for i in range(3):
        sh.rect(-3.7 - 0.3 * (i + 1), -0.2 + 0.05 * (i + 1) - 0.15, -3.7 - 0.3 * i, -0.2 + 0.05 * (i + 1), fill=WOOD2, stroke=GREEN, sw=0.7)
    # concha: topo + base
    top = top_profile(); bot = bottom_profile()
    sh.poly(top + bot[::-1], fill=MEMB, stroke=GREEN, sw=1.8)
    # arcos sugeridos (linhas leves)
    for x in C.ARCH_X[1:]:
        sh.line(C.shear(x, 0), 0, C.shear(x, C.top(x)), C.top(x), EARTH, 0.6, dash="4 4", opacity=0.6)
    # lábio frontal (anel A0 inclinado)
    sh.line(0.45, 0, C.shear(0.45, 4.13), 4.13, GREEN, 2.0)
    # vidro da fachada (recuado)
    sh.line(0.9, 0, C.shear(0.9, 4.15), 4.15, GLASS, 5); sh.line(0.9, 0, C.shear(0.9, 4.15), 4.15, GREEN, 0.9)
    # espinha de luz
    x1, x2, _ = C.SPINE
    spine = [(C.shear(x, C.top(x)), C.top(x)) for x in [x1 + (x2 - x1) * i / 30 for i in range(31)]]
    sh.poly(spine, close=False, stroke=GLASS, sw=6); sh.poly(spine, close=False, stroke=GREEN, sw=0.8)
    # janelas olho (lado direito: tc < pi/2)
    for w in C.WINDOWS:
        if w["tc"] > math.pi / 2: continue
        pts = [(x, z) for (x, y, z) in C.window_outline(w, 48)]
        sh.poly(pts, fill=GLASS, stroke=GREEN, sw=1.0)
        sh.poly([(x, z) for (x, y, z) in C.window_outline(dict(w, lx=w["lx"] + 0.11, lt=w["lt"] + 0.03), 48)], fill="none", stroke=WOOD2, sw=3)
    # condensadora na cauda
    sh.rect(9.95, 0.0, 10.7, 0.62, fill="#E5E1D8", stroke=GREEN, sw=0.8)
    for xx in [10.0 + 0.12 * i for i in range(6)]:
        sh.line(xx, 0.0, xx, 1.3, WOOD2, 2.2)
    # legendas
    sh.leader(3.4, 4.2, 2.0, 4.85, "Cumeeira 4,20 m · Espinha de Luz 1,90 a 6,60", 12)
    sh.leader(0.05, 3.5, -1.5, 4.3, "Lábio frontal: anel inclinado 8°, avanço 0,60 m", 12, anchor="end")
    sh.leader(4.9, 1.5, 3.4, -1.15, "Janela Olho 1,60 x 0,95 com requadro de madeira 220 mm", 12, anchor="end")
    sh.leader(7.9, 2.0, 7.6, 3.9, "Olho do banho 1,10 x 0,60 (alto)", 12, anchor="end")
    sh.leader(9.55, 1.15, 8.7, 4.6, "Cauda: fecha em ponta a 1,10 m", 12, anchor="end")
    sh.leader(10.4, 0.8, 9.8, 2.8, "Painel ripado da condensadora", 12, anchor="end")
    sh.leader(6.4, 0.35, 6.9, -1.0, "Calha oculta no rodapé da concha, queda Ø75 nas extremidades", 12)
    # cotas
    sh.dim(0.45, -0.95, 9.6, -0.95, -0.35, label="9,60 (piso)")
    sh.dim(-0.15, -0.95, 9.6, -0.95, -0.95, label="9,75 (concha com lábio)")
    sh.dim(-3.7, -0.95, 0.9, -0.95, -0.35, label="4,60 (deck)")
    sh.dim(10.8, 0, 10.8, 4.2, 0.5, label="4,20")
    sh.dim(-4.2, -0.6, -4.2, 0, -0.4, label="0,60")
    sh.scalebar(-4.4, -2.5, 5)
    sh.title_block("ZION COCOON", "Elevação lateral", "1:50 (A1)", "05/27", "Concha assimétrica: frente cheia, cauda afilada, 6 Janelas Olho")
    return sh

# ------------------------------------------------------------------ CORTE LONGITUDINAL
def corte_long():
    sh = Sheet(1600, 1000, scale=100, ox=470, oy=720)
    sh.header("Zion Cocoon · Corte longitudinal A-A", "Plano y = 0 (eixo) · olhar para +y · envelope: membrana + câmara ventilada + isolamento + forro")
    sh.rect(-4.0, -0.9, 11.0, -0.02, fill=sh.pattern("soil"), stroke="none")
    sh.line(-4.0, -0.02, 11.0, -0.02, GREEN, 1.0)
    # estacas / vigas / piso
    for px in [-3.3, -1.1, 0.9, 2.1, 3.3, 4.5, 5.7, 6.9, 8.1, 9.0]:
        sh.rect(px - 0.04, -0.9, px + 0.04, -0.22, fill=STEEL, stroke="none")
        sh.rect(px - 0.12, -0.24, px + 0.12, -0.2, fill=STEEL, stroke="none")
    sh.rect(-3.7, -0.2, 9.6, -0.05, fill=sh.pattern("insul"), stroke=GREEN, sw=0.9)   # vigotas + isolamento
    sh.rect(-3.7, -0.05, 9.6, 0.0, fill=WOOD2, stroke=GREEN, sw=0.5)
    sh.rect(-3.7, -0.2, 0.9, -0.05, fill=sh.pattern("deck"), stroke=GREEN, sw=0.9)
    # concha cortada: externa e interna (espessura 0,13)
    top = top_profile(); bot = bottom_profile()
    inner = [(C.shear(x, C.top(x) - 0.13), C.top(x) - 0.13) for x in [0.5 + (C.L - 0.5) * i / 160 for i in range(161)]]
    sh.poly(top + inner[::-1], fill=sh.pattern("insul"), stroke=GREEN, sw=1.6)
    sh.poly(top, close=False, stroke=EARTH, sw=3)  # membrana externa
    sh.poly([p for p in bot if p[0] > 8.6], close=False, stroke=GREEN, sw=1.6)
    # anel frontal e vidro
    sh.line(0.45, 0, C.shear(0.45, 4.13), 4.13, GREEN, 2.4)
    sh.line(0.9, 0, C.shear(0.9, 4.15), 4.15, GLASS, 5); sh.line(0.9, 0, C.shear(0.9, 4.15), 4.15, GREEN, 1.0)
    sh.line(0.9, 2.4, C.shear(0.9, 2.4), 2.4, GREEN, 1.0)
    # espinha de luz
    x1, x2, _ = C.SPINE
    spine = [(C.shear(x, C.top(x)), C.top(x)) for x in [x1 + (x2 - x1) * i / 30 for i in range(31)]]
    sh.poly(spine, close=False, stroke=GLASS, sw=7); sh.poly(spine, close=False, stroke=GREEN, sw=0.9)
    # parede do banho / forro / ático
    sh.rect(6.6, 0, 6.7, C.top(6.65) - 0.13, fill=sh.pattern("hatch"), stroke=GREEN, sw=0.9)
    sh.line(6.7, 2.4, 9.3, 2.4, GREEN, 1.2)
    sh.rect(7.0, 2.5, 8.0, 2.78, fill="#E5E1D8", stroke=GREEN, sw=0.8); sh.text(7.5, 2.64, "AC", 9, dy=3)
    sh.rect(8.3, 2.45, 8.7, 2.7, fill="#E5E1D8", stroke=GREEN, sw=0.8); sh.text(8.5, 2.57, "AQ", 8, dy=3)
    # difusor
    sh.rect(6.52, 2.05, 6.6, 2.25, fill=GREEN, stroke="none")
    # mobiliário em corte/vista: cama, cabeceira, chaise, banheira, bacia (vista), bancada
    sh.rect(4.5, 0.0, 6.55, 0.35, fill=WOOD2, stroke=GREEN, sw=0.8)
    sh.rect(4.5, 0.35, 6.55, 0.62, fill="#FFFFFF", stroke=GREEN, sw=0.8)
    sh.rect(6.0, 0.62, 6.5, 0.8, fill="#F4EFE8", stroke=GREEN, sw=0.6)
    sh.rect(6.55, 0.0, 6.6, 1.3, fill=WOOD, stroke=GREEN, sw=0.6)
    sh.rect(1.15, 0.0, 2.75, 0.45, fill=SAND, stroke=GREEN, sw=0.8)   # chaise (vista)
    sh.rect(7.55, 0.0, 9.15, 0.58, fill="#FFFFFF", stroke=GREEN, sw=0.9)   # banheira (corte)
    sh.rect(6.75, 0.0, 7.3, 0.85, fill="#EFEDE6", stroke=GREEN, sw=0.8, opacity=0.6)
    # janelas olho do lado esquerdo (vista de fundo)
    for w in C.WINDOWS:
        if w["tc"] < math.pi / 2: continue
        pts = [(x, z) for (x, y, z) in C.window_outline(w, 48)]
        sh.poly(pts, fill=GLASS, stroke=GREEN, sw=0.9, opacity=0.9)
    # pessoa (escala)
    sh.add(f'<g transform="translate({sh.X(3.5):.1f},{sh.Y(0):.1f}) scale({sh.s / 100:.3f})"><circle cx="0" cy="-165" r="11" fill="none" stroke="{GREEN}" stroke-width="1.5"/><path d="M0 -152 V-70 M0 -70 L-16 0 M0 -70 L16 0 M-22 -100 L0 -135 L22 -100" fill="none" stroke="{GREEN}" stroke-width="1.5" stroke-linecap="round"/></g>')
    # legendas
    sh.leader(2.2, C.top(2.2) + 0.02, 1.2, 4.7, "1 Membrana PVDF · 2 câmara ventilada 60 mm · 3 lã PET 50 mm + refletiva · 4 forro tensionado", 12)
    sh.leader(4.3, 4.17, 5.1, 4.8, "Espinha de Luz: 4 painéis de vidro laminado sobre treliça", 12)
    sh.leader(6.65, 3.2, 7.4, 4.1, "Parede da cabeceira / banho até a concha", 12)
    sh.leader(7.5, 2.64, 9.6, 3.9, "Ático técnico: evaporadora 12k BTU, aquecedor, quadro", 12, anchor="end")
    sh.leader(6.56, 2.15, 5.4, 3.1, "Difusor linear na cabeceira", 12, anchor="end")
    sh.leader(0.35, 3.2, -0.7, 3.9, "Anel A0 Ø101,6 · vidro recuado 0,45 m", 12, anchor="end")
    sh.leader(-1.0, -0.12, -3.9, 1.2, "Deck cumaru · vigas U 150 x 60 · PIR 50 mm", 12, anchor="start")
    sh.leader(8.3, 0.4, 9.9, 1.9, "Banheira na cauda sob o Olho baixo", 12, anchor="end")
    sh.leader(8.1, -0.5, 7.6, -1.5, "Estacas helicoidais Ø76 · cabeçote ajustável", 12, anchor="end")
    # cotas
    sh.dim(0.9, -1.05, 6.6, -1.05, -0.35, label="5,70")
    sh.dim(6.6, -1.05, 9.4, -1.05, -0.35, label="2,80")
    sh.dim(0.45, -1.05, 0.9, -1.05, -0.35, label="0,45")
    sh.dim(-3.7, -1.05, 0.45, -1.05, -0.35, label="4,15")
    sh.dim(10.8, 0, 10.8, 4.2, 0.5, label="4,20")
    sh.dim(9.9, 0, 9.9, 2.4, 0.4, label="2,40 forro")
    sh.dim(-4.2, -0.9, -4.2, 0, -0.4, label="0,90 (máx.)")
    sh.scalebar(-4.4, -2.5, 5)
    sh.title_block("ZION COCOON", "Corte longitudinal A-A", "1:50 (A1)", "06/27", "Envelope em 4 camadas, ático técnico sobre o banho, Espinha de Luz")
    return sh

# ------------------------------------------------------------------ CORTE TRANSVERSAL
def corte_transv():
    xc = 5.0
    sh = Sheet(1600, 1000, scale=120, ox=800, oy=720, flip_x=True)
    sh.header("Zion Cocoon · Corte transversal B-B", f"Plano x = {fmt(xc)} (suíte) · olhar para +x (cabeceira e banho ao fundo) · escala 1:40")
    sh.rect(-6.0, -0.9, 6.0, -0.02, fill=sh.pattern("soil"), stroke="none")
    sh.line(-6.0, -0.02, 6.0, -0.02, GREEN, 1.0)
    for py in [-2.6, -1.3, 0.0, 1.3, 2.6]:
        sh.rect(py - 0.04, -0.9, py + 0.04, -0.22, fill=STEEL, stroke="none")
        sh.rect(py - 0.12, -0.24, py + 0.12, -0.2, fill=STEEL, stroke="none")
    hw = C.floor_hw(xc)
    sh.rect(-3.3, -0.2, 3.3, -0.05, fill=sh.pattern("insul"), stroke=GREEN, sw=0.9)
    sh.rect(-3.3, -0.05, 3.3, 0.0, fill=WOOD2, stroke=GREEN, sw=0.5)
    # concha cortada (externa + interna)
    outer = C.section_local(xc, 100)
    t0, t1 = C.theta_range(xc)
    a, b = C.a(xc) - 0.13, C.b(xc) - 0.13
    inner = [(a * math.cos(t0 + (t1 - t0) * i / 100), C.ZC + b * math.sin(t0 + (t1 - t0) * i / 100)) for i in range(101)]
    inner = [(y, max(z, 0)) for (y, z) in inner]
    sh.poly(outer + inner[::-1], fill=sh.pattern("insul"), stroke=GREEN, sw=1.6)
    sh.poly(outer, close=False, stroke=EARTH, sw=3)
    # arco em corte (tubo Ø88,9 na camada)
    for th in [t0 + (t1 - t0) * i / 12 for i in range(13)]:
        y = (C.a(xc) - 0.065) * math.cos(th); z = C.ZC + (C.b(xc) - 0.065) * math.sin(th)
        if z > 0.05: sh.circle(y, z, 0.045, fill=STEEL, stroke="none")
    # espinha de luz (topo)
    sh.rect(-0.35, C.top(xc) - 0.14, 0.35, C.top(xc) + 0.02, fill=GLASS, stroke=GREEN, sw=0.9)
    # fundo: parede da cabeceira com porta e difusores, banho ao fundo
    sh.poly([(y, max(0, z - 0.13)) for (y, z) in inner], fill="#F3EDE3", stroke="none")
    sh.rect(-2.85, 0, 2.85, 1.3, fill=WOOD, stroke=GREEN, sw=0.7)  # painel de cabeceira
    sh.rect(1.0, 0, 1.85, 2.1, fill="#F7F3EC", stroke=GREEN, sw=0.8)  # porta de correr
    sh.rect(-1.2, 2.05, 0.9, 2.15, fill=GREEN, stroke="none")     # difusor linear
    # cama cortada, criados
    sh.rect(-0.97, 0.0, 0.97, 0.35, fill=WOOD2, stroke=GREEN, sw=0.8)
    sh.rect(-0.97, 0.35, 0.97, 0.62, fill="#FFFFFF", stroke=GREEN, sw=0.8)
    sh.rect(-1.55, 0, -1.05, 0.5, fill=WOOD2, stroke=GREEN, sw=0.7)
    sh.rect(1.05, 0, 1.55, 0.5, fill=WOOD2, stroke=GREEN, sw=0.7)
    # armário embutido esquerdo (vista, y 1,55..2,15)
    sh.rect(1.6, 0, 2.2, 1.5, fill=WOOD2, stroke=GREEN, sw=0.8)
    # janela olho direita em corte (x=4,55): abertura na concha
    w = C.WINDOWS[1]
    zc = C.ZC + C.b(xc) * math.sin(w["tc"]); dz = w["lt"] * C.b(xc)
    yv = -(C.a(xc)) * math.cos(w["tc"])
    sh.rect(yv - 0.16, zc - dz, yv + 0.02, zc + dz, fill=GLASS, stroke=GREEN, sw=1.0)
    sh.rect(yv - 0.26, zc - dz - 0.02, yv - 0.16, zc + dz + 0.02, fill=WOOD2, stroke=GREEN, sw=0.7)
    # iluminação indireta no rodapé
    for y in (-2.6, 2.6):
        sh.circle(y, 0.12, 0.04, fill="#F2C14E", stroke="none")
    # pessoa
    sh.add(f'<g transform="translate({sh.X(-2.1):.1f},{sh.Y(0):.1f}) scale({sh.s / 100:.3f})"><circle cx="0" cy="-165" r="11" fill="none" stroke="{GREEN}" stroke-width="1.5"/><path d="M0 -152 V-70 M0 -70 L-16 0 M0 -70 L16 0 M-22 -100 L0 -135 L22 -100" fill="none" stroke="{GREEN}" stroke-width="1.5" stroke-linecap="round"/></g>')
    # legendas
    sh.leader(0.0, C.top(xc) + 0.02, 0.9, 4.5, "Espinha de Luz 0,70 m (vidro laminado sobre treliça)", 12, anchor="end")
    sh.leader(-2.2, 2.5, -4.0, 3.5, "Arco elíptico Ø88,9 x 3,6 (A4, x 5,25)", 12, anchor="start")
    sh.leader(-2.85, 1.3, -4.0, 2.4, "Membrana · câmara 60 mm · lã PET 50 mm · forro", 12, anchor="start")
    sh.leader(yv - 0.1, zc, -4.0, 1.3, "Janela Olho basculante em corte", 12, anchor="start")
    sh.leader(2.6, 0.12, 4.0, 1.0, "Fita LED 2700 K no rodapé (indireta)", 12, anchor="end")
    sh.leader(1.85, 1.5, 4.0, 2.2, "Armário baixo embutido na curva (h 1,50)", 12, anchor="end")
    sh.leader(0.0, 2.1, 1.2, 3.4, "Difusor linear do ar-condicionado", 12, anchor="end")
    sh.leader(2.85, 0.3, 4.0, 0.3, "Trilho de base 100 x 50 + calha oculta", 12, anchor="end")
    sh.leader(-0.8, -0.12, 2.4, -1.5, "Piso: carvalho 14 mm + compensado 18 mm + PIR 50 mm", 12, anchor="start")
    sh.dim(-hw, -1.05, hw, -1.05, -0.35, label=f"{fmt(2 * hw)} (piso)")
    sh.dim(-C.a(xc), -1.05, C.a(xc), -1.05, -0.9, label=f"{fmt(2 * C.a(xc))} (concha)")
    sh.dim(-3.4, 0, -3.4, C.top(xc), -0.55, label=fmt(C.top(xc)))
    sh.dim(-3.4, 0, -3.4, 2.1, -1.15, label="2,10 (porta)")
    sh.dim(3.5, -0.9, 3.5, 0, 0.55, label="0,90")
    sh.scalebar(5.8, -2.0, 4)
    sh.title_block("ZION COCOON", "Corte transversal B-B", "1:40 (A1)", "07/27", "Seção elíptica com centro a 0,75 m: a concha abraça o piso")
    return sh


def build():
    os.makedirs(OUT, exist_ok=True)
    planta(True).save(os.path.join(OUT, "02_planta_humanizada.svg"))
    planta(False).save(os.path.join(OUT, "03_planta_tecnica.svg"))
    elev_frontal().save(os.path.join(OUT, "04_elevacao_frontal.svg"))
    elev_lateral().save(os.path.join(OUT, "05_elevacao_lateral.svg"))
    corte_long().save(os.path.join(OUT, "06_corte_longitudinal.svg"))
    corte_transv().save(os.path.join(OUT, "07_corte_transversal.svg"))
    print("cocoon drawings ok ->", OUT)

if __name__ == "__main__":
    build()

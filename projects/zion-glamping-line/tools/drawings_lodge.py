# -*- coding: utf-8 -*-
"""Desenhos técnicos 2D do ZION LODGE: plantas (humanizada, técnica, estrutural), elevações, fachada traseira e cortes (SVG).
Geometria única em geometry.Lodge; estilo em svgkit.py; símbolos compartilhados com drawings_cocoon / drawings_extra."""
import math, os
from geometry import Lodge
from svgkit import *
from drawings_cocoon import sym_bed, sym_table, sym_cabinet, sym_sofa, sym_chair, sym_vanity, sym_wc, sym_shower, sym_tub
from drawings_zenith import slats, ground, person
from drawings_extra import dline, pile_symbol, code_tag, arrow2, code_legend

L = Lodge()
OUT = os.path.join(os.path.dirname(__file__), "..", "lodge", "desenhos")
V = L.vertices(); R = L.r_corner(); HF = L.F / 2                      # vértices, raio de vértice (3,68), meia-face (3,40)
RO = R + L.OVER / math.cos(math.pi / 8)                               # raio de vértice da cobertura (com balanço)
VO = L.vertices(RO)                                                   # vértices da cobertura
R_EDGE = HF + L.OVER                                                  # meia-largura da cobertura entre faces (4,30)
Z_EDGE = L.Z_EAVE - 0.35                                              # borda da membrana (2,35)
YC = math.sqrt(R ** 2 - L.X_PART ** 2)                                # meia-corda da parede do banho (3,34)
PX = L.sail_posts()[0][0]                                             # x dos postes da vela (-6,28)
DECK = L.deck_pts()
A_INT, A_BATH = L.floor_area(), 6.9
A_DECK = L.deck_area()
J1 = dict(y1=-1.2, y2=0.4, z1=1.6, z2=2.2)                            # fresta da banheira (face 7-0)
PC1 = L.DOOR

# ------------------------------------------------------------------ geometria auxiliar
def oct_x(y):
    """meia-largura em x do octógono na ordenada y (|y| <= 3,40)."""
    y = abs(y)
    return HF if y <= HF * math.tan(math.pi / 8) + 1e-9 else HF - (y - V[0][1])

def deck_x_out(y):
    """x da borda externa do deck na ordenada y."""
    y = abs(y)
    return -(HF + L.DECK_D) if y <= DECK[4][1] * -1 + 1e-9 else -(HF + L.DECK_D) + (y - abs(DECK[4][1]))

def roof_profile(n=48):
    """perfil da membrana (d, z) do anel da lanterna até a borda (entre faces, d = 4,30), com queda de tensão até 2,35."""
    d0, d1 = L.R_LANTERN, R_EDGE
    pts = []
    for i in range(n + 1):
        d = d0 + (d1 - d0) * i / n
        t = (d - d0) / (d1 - d0)
        z = L.roof_z(d) - (L.roof_z(d1) - Z_EDGE) * t ** 3
        pts.append((d, z))
    return pts

def roof_silhouette():
    """silhueta simétrica (u, z) da cobertura para elevações (u = -4,30 .. 4,30)."""
    p = roof_profile()
    left = [(-d, z) for (d, z) in p][::-1]
    return left + [(d, z) for (d, z) in p]

def inward(i, j, t):
    """quadrilátero da face i-j deslocado t para dentro (parede com espessura)."""
    (x1, y1), (x2, y2) = V[i], V[j]
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    n = math.hypot(mx, my); ux, uy = -mx / n * t, -my / n * t
    return [(x1, y1), (x2, y2), (x2 + ux, y2 + uy), (x1 + ux, y1 + uy)]

def lantern(sh, u=0.0, z_ring=None):
    """lanterna em elevação/corte: anel de compressão, vidro 0,45 e tampa (centro em u)."""
    r = L.R_LANTERN
    sh.rect(u - r - 0.05, L.Z_LANTERN - 0.12, u + r + 0.05, L.Z_LANTERN, fill=STEEL, stroke="none")
    sh.rect(u - r, L.Z_LANTERN, u + r, L.Z_TOP - 0.15, fill=GLASS, stroke=GREEN, sw=0.9)
    for k in range(1, 4):
        sh.line(u - r + 2 * r * k / 4, L.Z_LANTERN, u - r + 2 * r * k / 4, L.Z_TOP - 0.15, GREEN, 0.6)
    sh.rect(u - r - 0.25, L.Z_TOP - 0.15, u + r + 0.25, L.Z_TOP, fill=MEMB, stroke=GREEN, sw=1.2)
    sh.line(u - r - 0.25, L.Z_TOP - 0.15, u - r - 0.4, L.Z_TOP - 0.35, GREEN, 0.7)
    sh.line(u + r + 0.25, L.Z_TOP - 0.15, u + r + 0.4, L.Z_TOP - 0.35, GREEN, 0.7)

def column(sh, u, z2=None, wood=True):
    """pilar em elevação: tubo Ø101,6 com revestimento de madeira (largura 0,24)."""
    z2 = z2 or L.Z_EAVE
    if wood: sh.rect(u - 0.12, 0, u + 0.12, z2, fill=WOOD2, stroke=GREEN, sw=0.7)
    else: sh.rect(u - 0.05, 0, u + 0.05, z2, fill=STEEL, stroke="none")

def eave_ring(sh, u1, u2):
    sh.rect(u1, L.Z_EAVE - 0.15, u2, L.Z_EAVE, fill=STEEL, stroke=GREEN, sw=0.5)

def draw_furniture_lodge(sh, human):
    for f in L.furniture():
        k = f["kind"]
        if k in ("ceiling", "hvac", "wall", "opening", "pillow"): continue
        if "r" in f:
            sh.circle(f["x"], f["y"], f["r"], fill=WOOD2 if human else "none", stroke=GREEN, sw=0.8); continue
        a = (sh, f["x1"], f["x2"], f["y1"], f["y2"], human)
        if k == "bed": sym_bed(*a)
        elif k == "table": sym_table(*a)
        elif k == "cabinet": sym_cabinet(*a)
        elif k == "sofa": sym_sofa(*a, back="x2")
        elif k == "chair": sym_chair(*a)
        elif k == "vanity": sym_vanity(*a)
        elif k == "wc": sym_wc(*a)
        elif k == "shower": sym_shower(*a)
        elif k == "tub": sym_tub(*a)
        elif k == "glass":
            sh.line(f["x1"], f["y1"], f["x1"], f["y2"], GLASS, 4); sh.line(f["x1"], f["y1"], f["x1"], f["y2"], GREEN, 0.8)
        elif k == "condenser":
            sh.rect(f["x1"], f["y1"], f["x2"], f["y2"], fill="#E5E1D8" if human else "none", stroke=GREEN, sw=0.8)
            sh.text((f["x1"] + f["x2"]) / 2, (f["y1"] + f["y2"]) / 2, "COND.", 8, dy=3)

# ------------------------------------------------------------------ PLANTA (humanizada / técnica)
def planta(human=True):
    sh = Sheet(1600, 1000, scale=52, ox=600, oy=505)
    sh.header("Zion Lodge · Planta baixa " + ("humanizada" if human else "técnica"),
              f"Pavilhão octogonal · 6,80 m entre faces (7,36 entre vértices) · piso interno {fmt(A_INT)} m² (banho {fmt(A_BATH)} m²) · deck {fmt(A_DECK)} m² · total {fmt(A_INT + A_DECK)} m²")
    xd = -(HF + L.DECK_D)
    # cobertura (projeção do beiral)
    sh.poly(VO, fill="none", stroke=GREEN, sw=0.9, dash="10 5")
    # deck em três faces + escada frontal
    sh.poly(DECK, fill=sh.pattern("deck") if human else "none", stroke=GREEN, sw=1.1)
    for i in range(3):
        sh.rect(xd - 0.3 * (i + 1), -1.2, xd - 0.3 * i, 1.2, fill=WOOD2 if human else "none", stroke=GREEN, sw=0.7)
    # vela de sombra (projeção) e postes
    sh.poly([V[3], (PX, 2.4), (PX, -2.4), V[4]], fill=MEMB if human else "none", stroke=GREEN, sw=0.8, dash="6 3", opacity=0.8 if human else 1)
    for (px, py) in L.sail_posts():
        sh.circle(px, py, 0.05, fill=STEEL, stroke="none"); sh.circle(px, py, 0.14, fill="none", stroke=STEEL, sw=0.6)
    # piso interno e banho
    sh.poly(V, fill=sh.pattern("wood") if human else "none", stroke=GREEN, sw=1.4)
    if human:
        sh.poly([(L.X_PART, -YC), V[7], V[0], (L.X_PART, YC)], fill=sh.pattern("tile"), stroke="none")
    # faces de vidro (linha grossa) e faces opacas (SIP 100 mm)
    for (i, j) in L.GLASS_FACES:
        sh.line(V[i][0], V[i][1], V[j][0], V[j][1], GLASS, 6, opacity=0.9 if human else 0.6)
        sh.line(V[i][0], V[i][1], V[j][0], V[j][1], GREEN, 1.0)
    for (i, j) in L.WALL_FACES:
        sh.poly(inward(i, j, 0.10), fill="#B29A78" if human else sh.pattern("hatch"), stroke=GREEN, sw=0.9)
    # fresta da banheira J1 (face 7-0, x = 3,40)
    sh.rect(HF - 0.06, J1["y1"], HF + 0.06, J1["y2"], fill=GLASS, stroke=GREEN, sw=0.7)
    # pilares nos vértices (tubo Ø101,6 + revestimento de madeira 240 mm)
    for (x, y) in V:
        sh.rect(x - 0.12, y - 0.12, x + 0.12, y + 0.12, fill=WOOD2 if human else "none", stroke=GREEN, sw=0.7)
        sh.circle(x, y, 0.05, fill=STEEL, stroke="none")
    # porta de correr PC1 na face frontal (folha fixa y 0..1, folha móvel y -1..0)
    sh.line(-HF, PC1["y1"], -HF, PC1["y2"], CREAM, 7)
    sh.line(-HF - 0.02, 0.0, -HF - 0.02, PC1["y2"], GREEN, 1.6)
    sh.line(-HF + 0.08, PC1["y1"], -HF + 0.08, 0.0, GREEN, 1.6)
    sh.line(-HF + 0.08, PC1["y1"], -HF + 0.08, PC1["y1"] - 0.6, GREEN, 0.6, dash="3 2")
    sh.add(f'<path d="M{sh.X(-HF + 0.08):.1f},{sh.Y(-0.12):.1f} l-5,7 l10,0 z" fill="{GREEN}"/>')
    # parede-corda do banho (x 1,55) com porta de correr (y -0,5..0,4)
    for (ya, yb) in [(-YC, -0.5), (0.4, YC)]:
        sh.rect(L.X_PART, ya, L.X_PART + 0.1, yb, fill="#B29A78" if human else sh.pattern("hatch"), stroke=GREEN, sw=0.9)
    sh.line(L.X_PART + 0.05, -0.5, L.X_PART + 0.05, 0.4, GREEN, 0.6, dash="4 3")
    sh.rect(L.X_PART + 0.12, 0.4, L.X_PART + 0.17, 1.3, fill="none", stroke=GREEN, sw=0.8)
    # mobiliário
    draw_furniture_lodge(sh, human)
    # lanterna (projeção)
    sh.circle(0, 0, L.R_LANTERN, fill="none", stroke=GREEN, sw=0.8, dash="4 3")
    # rótulos de ambientes
    lab = [("SUÍTE", 0.45, -1.55, "central, sob a lanterna"), ("ESTAR", -2.1, -1.75, f"{fmt(A_INT - A_BATH)} m² (estar + suíte)"),
           ("BANHO", 2.55, 0.2, f"{fmt(A_BATH)} m²"), ("DECK", -4.6, -3.6, f"{fmt(A_DECK)} m²")]
    for t, x, y, a in lab:
        sh.text(x, y, t, 12, GREEN, weight=700, spacing=0.22, dy=-4)
        sh.text(x, y, a, 9.5, EARTH, dy=10)
    if human:
        sh.text(0.45, 0.0, "cama king 1,93 x 2,03", 8, EARTH, dy=3)
        sh.text(xd - 0.45, -1.6, "3 degraus", 8, EARTH)
        sh.text(PX + 1.1, 3.0, "vela de sombra", 9, EARTH, rotate=-38)
        LX, RX = -9.9, 8.8
        sh.leader(0.0, L.R_LANTERN, 0.0, 4.95, "Lanterna Zion Ø1,50: luz zenital sobre a cama", 11)
        sh.leader(1.0, R_EDGE, 2.4, 6.3, "Beiral da membrana 0,90 m em todo o perímetro", 11, anchor="start")
        sh.leader(V[2][0] - 0.35, V[2][1] + 0.35, -1.5, 6.3, "Cinco faces de vidro insulado (alumínio bronze RPT)", 11, anchor="end")
        sh.leader(1.05, 2.57, 2.6, 5.55, "Café / minibar 1,70 m embutido", 11, anchor="start")
        sh.leader(-2.9, 0.0, LX, 2.3, "Sofá 2,40 voltado para o deck + mesa lateral", 11, anchor="start")
        sh.leader(-HF - 0.02, 0.5, LX, 3.2, "PC1 porta de correr 2,00 x 2,40", 11, anchor="start")
        sh.leader(-2.4, 2.1, LX, 4.1, "Poltrona de leitura junto ao vidro", 11, anchor="start")
        sh.leader(PX, 1.8, LX, 5.0, "Postes Ø76 da vela de sombra (h 2,40)", 11, anchor="start")
        sh.leader(-4.5, -4.5, LX, -5.6, "Deck cumaru em três faces sobre estacas helicoidais", 11, anchor="start")
        sh.leader(1.05, -2.57, 1.4, -5.4, "Closet 1,70 x 0,75 (h 2,20)", 11, anchor="start")
        sh.leader(V[6][0] + 0.4, V[6][1] - 0.4, 3.9, -4.7, "Faces opacas: painel SIP 100 mm + ripado termotratado", 11, anchor="start")
        sh.leader(2.1, 1.7, RX, 3.9, "Bancada 1,40 com cuba de apoio", 11, anchor="end")
        sh.leader(3.05, 1.95, RX, 3.1, "Bacia com caixa acoplada", 11, anchor="end")
        sh.leader(HF, -0.4, RX, 2.3, "J1 fresta alta 1,60 x 0,60 (z 1,60 a 2,20)", 11, anchor="end")
        sh.leader(L.X_PART + 0.05, -0.05, RX, 1.4, "Porta de correr do banho 0,90 x 2,10", 11, anchor="end")
        sh.leader(2.9, -1.15, RX, -1.4, "Chuveiro 0,95 x 0,90 com box de vidro", 11, anchor="end")
        sh.leader(2.25, -2.1, RX, -2.3, "Banheira de sentar 0,90 x 0,75 sob a fresta J1", 11, anchor="end")
        sh.leader(4.65, -1.85, RX, -3.2, "Condensadora 9k BTU atrás do ripado", 11, anchor="end")
    # cotas gerais
    yb = -6.5
    sh.dim(xd, yb, -HF, yb, -0.45, label=fmt(L.DECK_D) + " (deck)")
    sh.dim(-HF, yb, HF, yb, -0.45, label=fmt(L.F) + " (entre faces)")
    sh.dim(xd - 0.9, yb, HF, yb, -1.05, label=fmt(0.9 + L.DECK_D + L.F) + " (escada + deck + pavilhão)")
    sh.dim(9.4, -HF, 9.4, HF, 0.0, label=fmt(L.F) + " (entre faces)")
    sh.dim(10.1, -R_EDGE, 10.1, R_EDGE, 0.0, label=fmt(2 * R_EDGE) + " (cobertura)")
    sh.dim(-7.6, -6.0, -7.6, 6.0, 0.0, label="12,00 (deck)")
    if not human:
        # eixos dos pilares P1..P8
        for k, (x, y) in enumerate(V):
            ang = math.atan2(y, x); ex, ey = x + 0.55 * math.cos(ang), y + 0.55 * math.sin(ang)
            sh.line(x, y, ex, ey, EARTH, 0.6)
            sh.callout(ex + 0.24 * math.cos(ang), ey + 0.24 * math.sin(ang), f"P{k + 1}", r=11, color=EARTH)
        # caibros (projeção)
        for (a, b) in L.rafters():
            sh.line(a[0], a[1], b[0], b[1], EARTH, 0.6, dash="4 3", opacity=0.7)
        # esquadrias codificadas
        codes = {(1, 2): "VF1", (2, 3): "VF2", (4, 5): "VF3", (5, 6): "VF4"}
        for (i, j), c in codes.items():
            mx, my = (V[i][0] + V[j][0]) / 2, (V[i][1] + V[j][1]) / 2
            n = math.hypot(mx, my)
            code_tag(sh, mx * (n + 0.32) / n, my * (n + 0.32) / n, c, size=8)
        code_tag(sh, -HF - 0.5, -1.55, "PC1", size=8)
        code_tag(sh, HF + 0.35, -0.4, "J1", size=8, dy=14)
        code_tag(sh, 0.0, L.R_LANTERN + 0.2, "LZ1", size=8)
        # níveis
        sh.text(-0.9, 1.9, "▽ +0,00 piso", 9, EARTH, anchor="start")
        sh.text(-5.4, 0.6, "▽ -0,02 deck", 9, EARTH, anchor="start")
        sh.text(1.8, 2.95, "▽ -0,01 banho", 8.5, EARTH, anchor="start")
        # cotas parciais (acima do deck) e lanterna
        sh.dim(-HF, 6.5, -V[2][0], 6.5, 0.0, label=fmt(HF - V[2][0]) + " (canto)", size=10)
        sh.dim(-V[2][0], 6.5, V[1][0], 6.5, 0.0, label=fmt(2 * V[1][0]) + " (face)", size=10)
        sh.dim(V[1][0], 6.5, HF, 6.5, 0.0, label=fmt(HF - V[1][0]) + " (canto)", size=10)
        sh.dim(-HF, 7.1, L.X_PART, 7.1, 0.0, label=fmt(HF + L.X_PART) + " (estar + suíte)", size=10)
        sh.dim(L.X_PART, 7.1, HF, 7.1, 0.0, label=fmt(HF - L.X_PART) + " (banho)", size=10)
        sh.dim(-HF - 1.0, PC1["y1"], -HF - 1.0, PC1["y2"], 0.0, label="2,00 (PC1)", size=10)
        sh.dim(HF + 1.0, J1["y1"], HF + 1.0, J1["y2"], 0.0, label="1,60 (J1)", size=10)
        sh.dim(-L.R_LANTERN, -0.95, L.R_LANTERN, -0.95, 0.0, label="Ø1,50", size=9, ext=False)
        # estacas (referência): malha 2,40 x 1,70
        for (px, py) in L.piles():
            sh.add(f'<g transform="translate({sh.X(px):.1f},{sh.Y(py):.1f})"><circle r="4" fill="none" stroke="{STEEL}" stroke-width="0.9"/><line x1="-4" y1="0" x2="4" y2="0" stroke="{STEEL}" stroke-width="0.7"/><line x1="0" y1="-4" x2="0" y2="4" stroke="{STEEL}" stroke-width="0.7"/></g>')
        sh.text(-7.0, -8.15, f"○+ estaca helicoidal Ø76 / hélice Ø300 (malha 2,40 x 1,70 m, {len(L.piles())} un.: piso, deck e postes da vela)", 10, STEEL, anchor="start")
        # marcas de corte
        sh.line(-8.4, 0.0, 8.4, 0.0, GREEN, 1.4, dash="10 4")
        sh.text(-8.65, 0.0, "A", 12, weight=700, dy=4); sh.text(8.65, 0.0, "A", 12, weight=700, dy=4)
        sh.line(0.0, -6.1, 0.0, 5.9, GREEN, 1.4, dash="10 4")
        sh.text(0.0, 6.05, "B", 12, weight=700); sh.text(0.0, -6.4, "B", 12, weight=700)
        sh.text_px(1290, 182, "ESQUADRIAS E EIXOS", size=10, weight=700, spacing=0.2, anchor="start")
        code_legend(sh, 1290, 210, [("VF1-VF4", "Vidro insulado fixo 6 lam + 12 Ar + 6 temp, low-e"), ("PC1", "Porta de correr 2,00 x 2,40, alumínio bronze RPT"),
                                    ("J1", "Fresta fixa 1,60 x 0,60 sobre a banheira"), ("LZ1", "Lanterna: anel Ø1,50, vidro 0,45 m, tampa ventilada"),
                                    ("P1-P8", "Pilares Ø101,6 x 4,0 revestidos em madeira")], size=9.0, pitch=21)
    sh.north(1500, 140, angle=-90)
    sh.scalebar(-7.0, -8.7, 5)
    sh.title_block("ZION LODGE", "Planta baixa " + ("humanizada" if human else "técnica cotada"), "1:60 (A1) · cotas em metros", "02/LG" if human else "03/LG",
                   "Estar e suíte sob a lanterna, banho no fundo, deck em três faces")
    return sh

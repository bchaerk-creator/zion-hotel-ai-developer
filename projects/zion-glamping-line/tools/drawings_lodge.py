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

def eave_ring(sh, u1, u2, far=False):
    sh.rect(u1, L.Z_EAVE - 0.15, u2, L.Z_EAVE, fill="#B9B7B0" if far else STEEL, stroke=GREEN, sw=0.5)
    if far:
        for u in (u1 + 0.12, u2 - 0.12): sh.rect(u - 0.075, L.Z_EAVE - 0.15, u + 0.075, L.Z_EAVE, fill=STEEL, stroke="none")

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
        sh.text(1.75, 0.6, "▽ -0,01 banho", 8.5, EARTH, anchor="start")
        # cotas parciais (acima do deck) e lanterna
        sh.dim(-HF, 6.5, V[2][0], 6.5, 0.0, label=fmt(HF + V[2][0]) + " (canto)", size=10)
        sh.dim(V[2][0], 6.5, V[1][0], 6.5, 0.0, label=fmt(2 * V[1][0]) + " (face)", size=10)
        sh.dim(V[1][0], 6.5, HF, 6.5, 0.0, label=fmt(HF - V[1][0]) + " (canto)", size=10)
        sh.dim(-HF, 7.1, L.X_PART, 7.1, 0.0, label=fmt(HF + L.X_PART) + " (estar + suíte)", size=10)
        sh.dim(L.X_PART, 7.1, HF, 7.1, 0.0, label=fmt(HF - L.X_PART) + " (banho)", size=10)
        sh.dim(-HF - 1.0, PC1["y1"], -HF - 1.0, PC1["y2"], 0.0, label="2,00 (PC1)", size=10)
        sh.dim(HF + 1.0, J1["y1"], HF + 1.0, J1["y2"], 0.0, label="1,60 (J1)", size=10)
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

# ------------------------------------------------------------------ PLANTA ESTRUTURAL
def dline2(sh, p1, p2, w=0.06, color=STEEL, sw=0.8):
    """viga em planta em qualquer direção: duas linhas paralelas com fechamento nas pontas."""
    (x1, y1), (x2, y2) = p1, p2
    n = math.hypot(x2 - x1, y2 - y1); nx, ny = -(y2 - y1) / n * w / 2, (x2 - x1) / n * w / 2
    sh.poly([(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)], fill="none", stroke=color, sw=sw)

def planta_estrutural():
    sh = Sheet(1600, 1000, scale=52, ox=600, oy=505)
    sh.header("Zion Lodge · Planta estrutural", "Fundações, quadro do piso, 8 pilares, anel de beiral, 8 caibros, anel da lanterna, cabos e postes da vela · códigos conforme a lista de materiais")
    xd = -(HF + L.DECK_D)
    # contornos de referência
    sh.poly(DECK, fill="none", stroke=GREEN, sw=0.9)
    sh.poly(VO, fill="none", stroke=GREEN, sw=0.9, dash="10 5")
    sh.poly(V, fill="none", stroke=GREEN, sw=0.8)
    sh.poly([V[3], (PX, 2.4), (PX, -2.4), V[4]], fill="none", stroke=EARTH, sw=0.8, dash="4 3")
    # quadro do piso: A01 longitudinais, A02 transversais, A03 bordas do octógono, A04 deck
    YR = [-2.55, -0.85, 0.85, 2.55]; XR = [-2.4, 0.0, 2.4]
    for y in YR: dline(sh, -oct_x(y), y, oct_x(y), y)
    for x in XR: dline(sh, x, -oct_x(x), x, oct_x(x))
    for k in range(8): dline2(sh, V[k], V[(k + 1) % 8])
    for y in (-3.2, -1.1, 1.1, 3.2): dline(sh, deck_x_out(y), y, -oct_x(y), y)
    dline(sh, -4.7, -3.79, -4.7, 3.79)
    for a, b in [(DECK[3], DECK[4]), (DECK[4], DECK[5]), (DECK[5], DECK[6]), (DECK[6], DECK[7]), (DECK[7], DECK[0])]: dline2(sh, a, b)
    # anel de beiral VB01..VB08 (150 x 100) e emendas nos pilares
    for k in range(8):
        i, j = k, (k + 1) % 8
        sh.poly(inward(i, j, 0.10), fill="#B9B7B0", stroke=GREEN, sw=0.7)
        mx, my = (V[i][0] + V[j][0]) / 2, (V[i][1] + V[j][1]) / 2; n = math.hypot(mx, my)
        code_tag(sh, mx * (n + 0.42) / n, my * (n + 0.42) / n, f"VB{k + 1:02d}", size=8, dy=(-14 if abs(my) < 0.1 else 0))
    # pilares P01..P08
    for k, (x, y) in enumerate(V):
        sh.circle(x, y, 0.06, fill=STEEL, stroke="none"); sh.circle(x, y, 0.15, fill="none", stroke=STEEL, sw=0.7)
        ang = math.atan2(y, x)
        code_tag(sh, x + 0.95 * math.cos(ang), y + 0.95 * math.sin(ang), f"P{k + 1:02d}", size=8)
    # caibros C01..C08 e anel da lanterna AL01
    for k, (a, b) in enumerate(L.rafters()):
        sh.line(a[0], a[1], b[0], b[1], STEEL, 2.2)
        if k in (0, 2, 4, 6):
            code_tag(sh, a[0] * 0.58 + b[0] * 0.42, a[1] * 0.58 + b[1] * 0.42, f"C{k + 1:02d}", size=8)
    sh.circle(0, 0, L.R_LANTERN, fill="none", stroke=STEEL, sw=2.6)
    code_tag(sh, 0.0, 0.0, "AL01", size=8)
    # cabos de contraventamento CB01..CB03 nas faces opacas (X em planta esquemática)
    for k, (i, j) in enumerate(L.WALL_FACES):
        q = inward(i, j, 0.22)
        sh.line(q[0][0], q[0][1], q[2][0], q[2][1], EARTH, 0.9, dash="2 2"); sh.line(q[1][0], q[1][1], q[3][0], q[3][1], EARTH, 0.9, dash="2 2")
        mx, my = (V[i][0] + V[j][0]) / 2, (V[i][1] + V[j][1]) / 2; n = math.hypot(mx, my)
        code_tag(sh, mx * (n - 0.55) / n, my * (n - 0.55) / n, f"CB{k + 1:02d}", size=8, dy=(14 if abs(my) < 0.1 else 0))
    # parede-corda do banho (diafragma W01)
    sh.rect(L.X_PART, -YC, L.X_PART + 0.1, YC, fill=sh.pattern("hatch"), stroke=GREEN, sw=0.7)
    code_tag(sh, L.X_PART + 0.05, 3.05, "W01", size=8, anchor="start", dy=-6)
    # postes da vela PV01/PV02 sobre as estacas F21/F22
    for k, (px, py) in enumerate(L.sail_posts()):
        sh.circle(px, py, 0.06, fill=STEEL, stroke="none"); sh.circle(px, py, 0.2, fill="none", stroke=STEEL, sw=1.0)
        code_tag(sh, px - 0.6, py, f"PV{k + 1:02d}", size=8)
    # estacas F01..Fnn
    piles = L.piles()
    for i, (px, py) in enumerate(piles):
        pile_symbol(sh, px, py, f"F{i + 1:02d}")
    # etiquetas de vigas
    code_tag(sh, -1.2, 0.85, "A01", size=8, dy=-12); code_tag(sh, 1.2, -2.55, "A01", size=8, dy=14)
    code_tag(sh, -2.4, 1.7, "A02", size=8, anchor="start", dy=0); code_tag(sh, 2.4, -1.7, "A02", size=8, anchor="end")
    code_tag(sh, -2.55, -2.55, "A03", size=8, anchor="end", dy=14)
    code_tag(sh, -4.7, 1.1, "A04", size=8, anchor="start", dy=-12); code_tag(sh, -5.6, -3.2, "A04", size=8, dy=14)
    arrow2(sh, -1.9, -0.3, -0.5, -0.3, "vigotas c/ 400", EARTH)
    arrow2(sh, -5.3, 2.7, -3.9, 2.7, "vigotas c/ 400", EARTH)
    # marcas de corte
    sh.line(-8.4, 0.0, 8.4, 0.0, GREEN, 1.4, dash="10 4")
    sh.text(-8.65, 0.0, "A", 12, weight=700, dy=4); sh.text(8.65, 0.0, "A", 12, weight=700, dy=4)
    sh.line(0.0, -6.1, 0.0, 6.4, GREEN, 1.4, dash="10 4")
    sh.text(0.0, 6.6, "B", 12, weight=700); sh.text(0.0, -6.4, "B", 12, weight=700)
    # cotas: eixos das estacas
    sh.dim_chain([PX + 0.2, -4.7, -2.4, 0.0, 2.4, HF], -6.5, -0.45, size=10)
    sh.dim(xd - 0.9, -6.5, HF, -6.5, -1.15, label=fmt(0.9 + L.DECK_D + L.F) + " (escada + deck + pavilhão)")
    sh.dim_chain([-HF, -2.55, -0.85, 0.85, 2.55, HF], 9.4, 0.0, vertical=True, size=10)
    sh.dim(10.1, -R_EDGE, 10.1, R_EDGE, 0.0, label=fmt(2 * R_EDGE) + " (cobertura)")
    sh.dim_chain([-3.2, -1.1, 1.1, 3.2], -7.6, 0.0, vertical=True, size=10)
    sh.dim(-8.3, -6.0, -8.3, 6.0, 0.0, label="12,00 (deck)")
    # legenda
    sh.north(1520, 120, angle=-90)
    sh.text_px(1300, 190, "CÓDIGOS ESTRUTURAIS", size=10, weight=700, spacing=0.2, anchor="start")
    items = [(f"F01-F{len(piles):02d}", "Estaca helicoidal Ø76 / hélice Ø300, L 1,5 a 2,5 m"),
             ("A01", "Vigas longitudinais U 150 x 60 x 3,0 galv. (4 linhas)"),
             ("A02", "Vigas transversais U 150 x 60 x 3,0 galv. (3 linhas)"),
             ("A03", "Vigas de borda do octógono U 150 x 60 x 3,0 (8)"),
             ("A04", "Vigas do deck U 150 x 60 x 3,0 + bordas"),
             ("P01-P08", "Pilares Ø101,6 x 4,0, h 2,70, revestidos em madeira"),
             ("VB01-VB08", "Anel de beiral 150 x 100 x 4,0 (emendas nos pilares)"),
             ("C01-C08", "Caibros radiais Ø76,1 x 3,6, beiral -> lanterna"),
             ("AL01", "Anel de compressão da lanterna Ø1,50 (150 x 100)"),
             ("CB01-CB03", "Cabos em X Ø8 inox nas três faces opacas"),
             ("W01", "Parede-corda do banho LSF 90 (diafragma)"),
             ("PV01-PV02", "Postes da vela Ø76,1 x 3,6, h 2,40, estaiados")]
    code_legend(sh, 1300, 218, items, size=8.6, pitch=21)
    sh.text_px(1300, 482, f"{len(piles)} estacas: 16 sob o piso, 4 sob o deck, 2 sob os postes da vela", size=8.6, fill=EARTH, anchor="start")
    sh.text_px(1300, 498, "Membrana em 8 gomos tensionada entre VB e AL01", size=8.6, fill=EARTH, anchor="start")
    sh.scalebar(-7.0, -8.7, 5)
    sh.title_block("ZION LODGE", "Planta estrutural", "1:60 (A1) · cotas em metros", "03b/LG",
                   "Estacas, quadro U 150, 8 pilares, anel de beiral, caibros, lanterna e vela")
    return sh

# ------------------------------------------------------------------ ELEVAÇÕES
def roof_elev(sh, seams):
    """cobertura em elevação: silhueta da membrana + costuras dos gomos (caibros projetados) + lanterna."""
    sh.poly(roof_silhouette(), fill=MEMB, stroke=GREEN, sw=1.8)
    sh.line(-R_EDGE, Z_EDGE, R_EDGE, Z_EDGE, EARTH, 2.4)
    for (u0, u1) in seams:
        sh.line(u0, L.Z_EAVE - 0.05, u1, L.Z_LANTERN - 0.05, EARTH, 0.6, dash="4 3", opacity=0.7)
    lantern(sh)

def sail_side(sh, u_post, u_wall):
    sh.line(u_post, 0, u_post, L.SAIL["z_post"], STEEL, 4)
    sh.line(u_post, L.SAIL["z_post"] + 0.05, u_wall, L.Z_EAVE + 0.15, GREEN, 1.8)

def deck_base(sh, u1, u2, piles):
    """solo, estacas, quadro do piso e deck em elevação (entre u1 e u2)."""
    ground(sh, -7.6, 7.6)
    for u in piles: sh.rect(u - 0.04, -0.6, u + 0.04, -0.2, fill=STEEL, stroke="none")
    sh.rect(u1, -0.2, u2, -0.05, fill=WOOD2, stroke=GREEN, sw=0.9); sh.rect(u1, -0.05, u2, 0.0, fill=GREEN, stroke="none")

def dims_elev(sh, side_dims):
    """cotas horizontais de base (acima do carimbo) e verticais laterais [(u, z1, z2, label)]."""
    yb = -0.85
    sh.dim(-HF, yb, HF, yb, -0.3, label="6,80 (entre faces)")
    sh.dim(-R_EDGE, yb, R_EDGE, yb, -0.75, label="8,60 (cobertura)")
    sh.dim(-6.0, yb, 6.0, yb, -1.2, label="12,00 (deck)")
    for (u, z1, z2, lab) in side_dims: sh.dim(u, z1, u, z2, 0.0, label=lab)

def elev_frontal():
    sh = Sheet(1600, 1000, scale=84, ox=800, oy=690, flip_x=True)
    sh.header("Zion Lodge · Elevação frontal", "Vista do deck (olhar para +x) · três faces de vidro sob o beiral · cobertura 8,60 m · lanterna a 5,20 m · vela de sombra sobre o deck")
    deck_base(sh, -6.0, 6.0, (-5.2, -3.2, -1.1, 1.1, 3.2, 5.2))
    # corpo: três faces de vidro (as duas laterais em escorço) e pilares
    for (y1, y2) in [(-HF, V[4][1]), (V[4][1], V[3][1]), (V[3][1], HF)]:
        sh.rect(y1, 0, y2, L.Z_EAVE - 0.15, fill=GLASS, stroke=GREEN, sw=1.0)
    for yy in (-2.4, 2.4): sh.line(yy, 0, yy, L.Z_EAVE - 0.15, GREEN, 0.9)
    sh.rect(-0.97, 0.0, 0.97, 0.62, fill="#FFFFFF", stroke=GREEN, sw=0.6, opacity=0.7)
    sh.rect(-1.2, 0.0, 1.2, 0.8, fill=SAND, stroke=GREEN, sw=0.6, opacity=0.6)
    sh.rect(PC1["y1"], 0, PC1["y2"], PC1["h"], fill="none", stroke=GREEN, sw=1.6); sh.line(0, 0, 0, PC1["h"], GREEN, 0.9)
    sh.rect(-0.12, 0.9, -0.06, 1.3, fill=GREEN, stroke="none")
    for yy in (-HF, V[4][1], V[3][1], HF): column(sh, yy)
    eave_ring(sh, -HF - 0.12, HF + 0.12)
    roof_elev(sh, [(-HF, -0.69), (-V[4][1], -0.29), (V[3][1], 0.29), (HF, 0.69)])
    # vela de sombra (vista de frente): pano entre os postes e o beiral
    sh.poly([(-2.4, L.SAIL["z_post"] + 0.05), (2.4, L.SAIL["z_post"] + 0.05), (V[3][1], L.Z_EAVE + 0.15), (V[4][1], L.Z_EAVE + 0.15)], fill=shade(MEMB, 0.94), stroke=GREEN, sw=1.0)
    sh.line(-2.4, L.SAIL["z_post"] + 0.05, 2.4, L.SAIL["z_post"] + 0.05, GREEN, 2.2)
    for py in (-1.8, 1.8): sh.line(py, -0.05, py, L.SAIL["z_post"], STEEL, 4)
    person(sh, -4.6)
    # rótulos (com flip_x, +u fica à esquerda): longos acima da cobertura, curtos nas faixas laterais
    Lu, Ru = 4.9, -5.0
    sh.leader(0.5, L.Z_TOP, 2.2, 5.85, "Lanterna Zion: anel Ø1,50, vidro 0,45 m, tampa ventilada", 12, anchor="end")
    sh.leader(-2.0, L.roof_z(2.0), -3.0, 5.25, "Membrana PVDF 1050 g/m² em 8 gomos", 12, anchor="start")
    sh.leader(3.6, L.roof_z(3.6) - 0.05, 3.9, 4.35, "Borda tensionada: cabo Ø10 na bainha, queda 0,35", 12, anchor="end")
    sh.leader(-1.9, 2.9, -3.9, 4.35, "Vela de sombra: 2 postes Ø76 h 2,40", 12, anchor="start")
    sh.leader(2.9, 2.62, 4.5, 3.3, "Anel de beiral 150 x 100", 12, anchor="end")
    sh.leader(2.9, 1.6, Lu, 2.4, "VF2 vidro insulado low-e", 12, anchor="end")
    sh.leader(V[3][1] + 0.1, 1.0, Lu, 1.5, "Pilar P4 Ø101,6 + madeira", 12, anchor="end")
    sh.leader(4.2, -0.12, Lu, 0.6, "Deck cumaru, vigas U 150", 12, anchor="end")
    sh.leader(-0.6, 1.4, Ru, 2.3, "PC1 porta 2,00 x 2,40", 12, anchor="start")
    sh.leader(-2.9, 1.2, Ru, 1.4, "VF3 em escorço (45°)", 12, anchor="start")
    sh.leader(-5.2, -0.45, Ru, 0.4, "Estacas helicoidais Ø76", 12, anchor="start")
    dims_elev(sh, [(6.7, 0, L.Z_TOP, "5,20"), (7.3, 0, L.Z_EAVE, "2,70 (beiral)"), (-6.7, 0, L.Z_LANTERN, "4,60 (anel)"), (-7.3, 0, L.SAIL["z_post"], "2,40 (vela)")])
    sh.scalebar(7.4, -2.0, 4)
    sh.title_block("ZION LODGE", "Elevação frontal", "1:50 (A1)", "04/LG", "Três faces de vidro, porta de correr, vela de sombra e lanterna no cume")
    return sh

def fachada_traseira():
    sh = Sheet(1600, 1000, scale=84, ox=800, oy=690, flip_x=False)
    sh.header("Zion Lodge · Fachada traseira", "Vista dos fundos (olhar para -x, +y à direita) · três faces opacas ripadas · fresta J1 da banheira · condensadora oculta")
    deck_base(sh, -6.0, 6.0, (-3.2, -2.55, -0.85, 0.0, 0.85, 2.55, 3.2))
    for (y1, y2) in [(-HF, V[7][1]), (V[7][1], V[0][1]), (V[0][1], HF)]:
        sh.rect(y1, 0, y2, L.Z_EAVE - 0.15, fill="#C9B08C", stroke=GREEN, sw=1.0)
        slats(sh, y1 + 0.04, y2, 0, L.Z_EAVE - 0.15, 0.08 if abs(y1 + y2) < 0.1 else 0.057)
    sh.rect(J1["y1"], J1["z1"], J1["y2"], J1["z2"], fill=GLASS, stroke=GREEN, sw=0.9)
    for yy in (-HF, V[7][1], V[0][1], HF): column(sh, yy)
    eave_ring(sh, -HF - 0.12, HF + 0.12)
    roof_elev(sh, [(-HF, -0.69), (V[7][1], -0.29), (V[0][1], 0.29), (HF, 0.69)])
    # condensadora atrás do ripado (x 4,30 a 5,00 · y -2,2 a -1,5)
    sh.rect(-2.2, 0.0, -1.5, 0.62, fill="#E5E1D8", stroke=GREEN, sw=0.8)
    sh.rect(-2.3, 0.0, -1.4, 1.3, fill="none", stroke=GREEN, sw=0.8)
    slats(sh, -2.27, -1.4, 0.0, 1.3, 0.1); sh.line(-2.3, 1.3, -1.4, 1.3, GREEN, 1.0)
    person(sh, 4.6)
    Lu, Ru = -4.9, 5.0
    sh.leader(0.4, L.Z_TOP, 1.8, 5.85, "Lanterna Zion: tampa ventilada sobre o anel de compressão", 12, anchor="start")
    sh.leader(-2.0, L.roof_z(2.0), -3.0, 5.25, "Membrana PVDF em 8 gomos · lã PET", 12, anchor="end")
    sh.leader(3.6, L.roof_z(3.6) - 0.05, 3.9, 4.35, "Beiral 0,90 m com borda tensionada", 12, anchor="start")
    sh.leader(-2.9, 2.62, -4.5, 3.3, "Anel de beiral 150 x 100", 12, anchor="end")
    sh.leader(-0.4, 1.9, 3.9, 3.7, "J1 fresta fixa 1,60 x 0,60 sobre a banheira", 12, anchor="start")
    sh.leader(2.4, 1.3, Ru, 2.2, "SIP 100 mm + ripado 40 x 40", 12, anchor="start")
    sh.leader(V[7][1] - 0.1, 0.9, Lu, 2.3, "Pilar P8 Ø101,6 + madeira", 12, anchor="end")
    sh.leader(-1.85, 0.5, Lu, 1.4, "Condensadora 9k BTU oculta", 12, anchor="end")
    sh.leader(-4.2, -0.12, Lu, 0.5, "Asa do deck além do corpo", 12, anchor="end")
    sh.leader(5.4, -0.12, Ru, 0.6, "Quadro do piso U 150 x 60", 12, anchor="start")
    dims_elev(sh, [(-6.7, 0, L.Z_TOP, "5,20"), (-7.3, 0, L.Z_EAVE, "2,70 (beiral)"), (7.3, 0, L.Z_LANTERN, "4,60 (anel)")])
    sh.dim(7.9, J1["z1"], 7.9, J1["z2"], 0.0, label="0,60 (J1)", size=10)
    sh.dim(J1["y1"], 1.3, J1["y2"], 1.3, 0.0, label="1,60 (J1)", size=10, ext=False)
    sh.scalebar(-7.5, -2.0, 4)
    sh.title_block("ZION LODGE", "Fachada traseira", "1:50 (A1)", "04b/LG", "Faces opacas ripadas, fresta da banheira, condensadora oculta, lanterna")
    return sh

def elev_lateral():
    sh = Sheet(1600, 1000, scale=84, ox=830, oy=690)
    sh.header("Zion Lodge · Elevação lateral direita", "Vista do lado -y (olhar para +y) · duas faces de vidro e uma opaca · deck 2,60 m com vela de sombra · cobertura 8,60 m")
    xd = -(HF + L.DECK_D)
    ground(sh, -8.4, 6.8)
    for px in (PX + 0.2, -4.7, -2.4, 0.0, 2.4, HF): sh.rect(px - 0.04, -0.6, px + 0.04, -0.2, fill=STEEL, stroke="none")
    sh.rect(xd, -0.2, V[5][0], -0.05, fill=WOOD2, stroke=GREEN, sw=0.9); sh.rect(xd, -0.05, V[5][0], 0.0, fill=GREEN, stroke="none")
    for i in range(3):
        sh.rect(xd - 0.3 * (i + 1), -0.2 + 0.05 * (i + 1) - 0.15, xd - 0.3 * i, -0.2 + 0.05 * (i + 1), fill=WOOD2, stroke=GREEN, sw=0.7)
    # corpo: vidro (faces 4-5 em escorço e 5-6), opaca (6-7)
    sh.rect(-HF, 0, V[5][0], L.Z_EAVE - 0.15, fill=GLASS, stroke=GREEN, sw=1.0)
    sh.rect(V[5][0], 0, V[6][0], L.Z_EAVE - 0.15, fill=GLASS, stroke=GREEN, sw=1.0)
    sh.line(-2.4, 0, -2.4, L.Z_EAVE - 0.15, GREEN, 0.9); sh.line(0, 0, 0, L.Z_EAVE - 0.15, GREEN, 0.9)
    sh.rect(-0.55, 0.0, 1.45, 0.62, fill="#FFFFFF", stroke=GREEN, sw=0.6, opacity=0.7)
    sh.rect(-2.7, 0.0, -1.5, 0.8, fill=SAND, stroke=GREEN, sw=0.6, opacity=0.6)
    sh.rect(V[6][0], 0, HF, L.Z_EAVE - 0.15, fill="#C9B08C", stroke=GREEN, sw=1.0)
    slats(sh, V[6][0] + 0.04, HF, 0, L.Z_EAVE - 0.15, 0.057)
    for xx in (-HF, V[5][0], V[6][0], HF): column(sh, xx)
    eave_ring(sh, -HF - 0.12, HF + 0.12)
    roof_elev(sh, [(-HF, -0.69), (V[5][0], -0.29), (V[6][0], 0.29), (HF, 0.69)])
    sail_side(sh, PX, -HF)
    sh.rect(4.3, 0.0, 5.0, 0.62, fill="#E5E1D8", stroke=GREEN, sw=0.8)
    sh.rect(4.2, 0.0, 5.1, 1.3, fill="none", stroke=GREEN, sw=0.8); slats(sh, 4.23, 5.1, 0.0, 1.3, 0.1); sh.line(4.2, 1.3, 5.1, 1.3, GREEN, 1.0)
    person(sh, -4.9)
    Lu, Ru = -6.8, 5.3
    sh.leader(0.4, L.Z_TOP, 1.6, 5.85, "Lanterna Zion 4,60 a 5,20 m: luz zenital sobre a cama", 12, anchor="start")
    sh.leader(-2.2, L.roof_z(2.2), -3.4, 5.25, "Membrana PVDF em 8 gomos sobre caibros radiais", 12, anchor="end")
    sh.leader(2.2, L.roof_z(2.2), Ru, 5.0, "Beiral 0,90 m, borda tensionada", 12, anchor="end")
    sh.leader(HF + 0.1, 2.62, Ru, 4.4, "Anel de beiral 150 x 100 sobre 8 pilares", 12, anchor="end")
    sh.leader(2.5, 1.3, Ru, 3.8, "Face opaca: SIP 100 mm + ripado 40 x 40", 12, anchor="end")
    sh.leader(4.65, 0.8, Ru, 1.75, "Condensadora oculta", 12, anchor="end")
    sh.leader(PX + 1.0, 2.6, Lu, 4.3, "Vela: 2 postes Ø76 h 2,40", 12, anchor="end")
    sh.leader(-3.9, L.roof_z(3.9) - 0.05, Lu, 3.5, "Beiral 0,90 m em todo o perímetro", 12, anchor="end")
    sh.leader(-2.4, 1.5, Lu, 2.7, "VF3 / VF4 vidro insulado", 12, anchor="end")
    sh.leader(-5.0, -0.12, Lu, 1.0, "Deck cumaru, vigas U 150", 12, anchor="end")
    sh.leader(xd - 0.5, -0.25, Lu, 0.25, "3 degraus de acesso", 12, anchor="end")
    yb = -0.85
    sh.dim(-HF, yb, HF, yb, -0.3, label="6,80 (entre faces)")
    sh.dim(xd, yb, -HF, yb, -0.3, label="2,60 (deck)")
    sh.dim(-R_EDGE, yb, R_EDGE, yb, -0.75, label="8,60 (cobertura)")
    sh.dim(PX, yb, HF, yb, -1.2, label=fmt(HF - PX) + " (vela + deck + pavilhão)")
    sh.dim(5.8, 0, 5.8, L.Z_TOP, 0.0, label="5,20"); sh.dim(6.4, 0, 6.4, L.Z_EAVE, 0.0, label="2,70 (beiral)")
    sh.dim(7.0, 0, 7.0, L.SAIL["z_post"], 0.0, label="2,40 (postes da vela)")
    sh.scalebar(-8.3, -2.0, 5)
    sh.title_block("ZION LODGE", "Elevação lateral", "1:50 (A1)", "05/LG", "Vidro na frente, ripado no fundo: silhueta cônica igual em todos os ângulos")
    return sh

# ------------------------------------------------------------------ CORTES
def roof_section(sh, u_lim=HF):
    """membrana cortada (perfil real no plano), câmara isolada até o forro tensionado, caibros projetados e lanterna."""
    prof = roof_profile()
    outer = [(-d, z) for (d, z) in prof][::-1] + [(d, z) for (d, z) in prof]
    liner = [(d, L.roof_z(d) - 0.22) for (d, z) in prof if d <= u_lim]
    liner = [(-d, z) for (d, z) in liner][::-1] + liner
    inner_prof = [(u, z) for (u, z) in outer if abs(u) <= u_lim]
    sh.poly(inner_prof + liner[::-1], fill=sh.pattern("insul"), stroke="none")
    sh.poly(outer, close=False, stroke=EARTH, sw=3.2)
    sh.poly(liner, close=False, stroke=GREEN, sw=1.2)

def rafters_section(sh, pairs):
    for (u0, u1) in pairs:
        sh.line(u0, L.Z_EAVE, u1, L.Z_LANTERN, STEEL, 2.4)

def corte_long():
    sh = Sheet(1600, 1000, scale=84, ox=830, oy=690)
    sh.header("Zion Lodge · Corte longitudinal A-A", "Plano y = 0 (eixo da porta e da lanterna) · olhar para +y · deck, vela, pilares, caibros, membrana, forro tensionado, banho e ático técnico")
    xd = -(HF + L.DECK_D)
    ground(sh, -8.4, 6.8, 0.9)
    for px in (PX + 0.2, -4.7, -2.4, 0.0, 2.4, -HF, HF):
        sh.rect(px - 0.04, -0.9, px + 0.04, -0.22, fill=STEEL, stroke="none"); sh.rect(px - 0.12, -0.24, px + 0.12, -0.2, fill=STEEL, stroke="none")
    sh.rect(-HF, -0.2, HF, -0.05, fill=sh.pattern("insul"), stroke=GREEN, sw=0.9); sh.rect(-HF, -0.05, HF, 0.0, fill=WOOD2, stroke=GREEN, sw=0.5)
    sh.rect(xd, -0.2, -HF, -0.05, fill=sh.pattern("deck"), stroke=GREEN, sw=0.9)
    for i in range(3):
        sh.rect(xd - 0.3 * (i + 1), -0.2 + 0.05 * (i + 1) - 0.15, xd - 0.3 * i, -0.2 + 0.05 * (i + 1), fill=WOOD2, stroke=GREEN, sw=0.7)
    # fundo (além do plano, y > 0): faces 2-3 (vidro, escorço), 1-2 (vidro), 0-1 (parede do banho)
    sh.rect(-HF, 0, V[2][0], L.Z_EAVE - 0.15, fill=GLASS, stroke=GREEN, sw=0.7, opacity=0.8)
    sh.rect(V[2][0], 0, V[1][0], L.Z_EAVE - 0.15, fill=GLASS, stroke=GREEN, sw=0.7, opacity=0.8)
    sh.rect(V[1][0], 0, HF, L.Z_EAVE - 0.15, fill="#EDE3D3", stroke=GREEN, sw=0.7)
    for xx in (V[2][0], V[1][0]): column(sh, xx)
    sh.rect(0.2, 0.0, 1.9, 0.9, fill=WOOD2, stroke=GREEN, sw=0.7, opacity=0.7)          # café / minibar ao fundo
    sh.rect(-2.9, 0.0, -1.9, 0.75, fill=SAND, stroke=GREEN, sw=0.7, opacity=0.7)         # poltrona
    sh.rect(-0.55, 0.0, 0.05, 0.5, fill=WOOD2, stroke=GREEN, sw=0.7)                     # criado-mudo
    sh.rect(1.75, 0.0, 2.45, 0.85, fill="#EFEDE6", stroke=GREEN, sw=0.7)                 # bancada
    sh.rect(2.7, 0.0, 3.3, 0.42, fill="#FFFFFF", stroke=GREEN, sw=0.7)                   # bacia
    # pilares no plano (vértices 3 e 0, y = +1,41) e anel de beiral
    for xx in (-HF, HF): column(sh, xx)
    eave_ring(sh, -HF - 0.12, HF + 0.12, far=True)
    # paredes cortadas: PC1 (vidro) na frente, SIP + J1 no fundo, parede-corda do banho com a porta
    sh.rect(-HF - 0.03, 0, -HF + 0.03, PC1["h"], fill=GLASS, stroke=GREEN, sw=1.0)
    sh.rect(-HF - 0.03, PC1["h"], -HF + 0.03, L.Z_EAVE - 0.15, fill=GLASS, stroke=GREEN, sw=0.8)
    sh.line(-HF - 0.1, PC1["h"], -HF + 0.1, PC1["h"], GREEN, 1.2)
    sh.rect(HF - 0.1, 0, HF, L.Z_EAVE - 0.15, fill=sh.pattern("hatch"), stroke=GREEN, sw=1.0)
    sh.rect(HF - 0.1, J1["z1"], HF, J1["z2"], fill=GLASS, stroke=GREEN, sw=0.8)
    sh.rect(L.X_PART, 0, L.X_PART + 0.1, 2.4, fill="#EDE3D3", stroke=GREEN, sw=0.8)     # parede vista (o plano passa na porta)
    sh.rect(L.X_PART, 2.1, L.X_PART + 0.1, 2.4, fill=sh.pattern("hatch"), stroke=GREEN, sw=0.9)   # verga cortada
    sh.rect(L.X_PART + 0.12, 0, L.X_PART + 0.17, 2.1, fill="#F7F3EC", stroke=GREEN, sw=0.7)        # folha recolhida (vista)
    # forro do banho, ático técnico, difusor
    sh.rect(L.X_PART, 2.4, HF - 0.1, 2.45, fill=SAND, stroke=GREEN, sw=0.6)
    sh.rect(2.0, 2.5, 3.0, 2.7, fill="#E5E1D8", stroke=GREEN, sw=0.8); sh.text(2.5, 2.6, "AC", 9, dy=3)
    sh.rect(L.X_PART - 0.08, 2.05, L.X_PART, 2.25, fill=GREEN, stroke="none")
    # cobertura: membrana + forro + caibros (y > 0) + lanterna
    roof_section(sh)
    rafters_section(sh, [(-HF, -0.69), (V[2][0], -0.29), (V[1][0], 0.29), (HF, 0.69)])
    lantern(sh)
    # vela (poste além do plano) e mobiliário cortado
    sail_side(sh, PX, -HF)
    sh.rect(-0.55, 0.0, 1.45, 0.35, fill=WOOD2, stroke=GREEN, sw=0.8); sh.rect(-0.55, 0.35, 1.45, 0.62, fill="#FFFFFF", stroke=GREEN, sw=0.8)
    sh.rect(0.95, 0.62, 1.4, 0.8, fill="#F4EFE8", stroke=GREEN, sw=0.6)
    sh.rect(1.45, 0.0, 1.5, 1.1, fill=WOOD, stroke=GREEN, sw=0.6)
    sh.rect(-2.7, 0.0, -1.5, 0.8, fill=SAND, stroke=GREEN, sw=0.8)
    sh.rect(-1.45, 0.0, -0.85, 0.45, fill=WOOD2, stroke=GREEN, sw=0.7)
    person(sh, -4.3)
    # rótulos
    Lu, Ru = -6.8, 5.3
    sh.leader(0.0, L.Z_TOP, 1.6, 5.85, "Lanterna Zion: anel de compressão Ø1,50, vidro claro 0,45 m, tampa ventilada", 12, anchor="start")
    sh.leader(-2.0, L.roof_z(2.0), -3.4, 5.25, "Membrana PVDF · câmara ventilada · lã PET 50 mm · forro tensionado", 12, anchor="end")
    sh.leader(2.6, L.roof_z(2.6) - 0.25, Ru, 4.5, "Forro tensionado a 0,22 m da membrana", 12, anchor="end")
    sh.leader(2.2, L.Z_EAVE + (L.Z_LANTERN - L.Z_EAVE) * 0.45, Ru, 3.95, "Caibro C1 Ø76,1 (beiral -> lanterna)", 12, anchor="end")
    sh.leader(HF + 0.05, 2.62, Ru, 3.4, "Anel de beiral 150 x 100 a 2,70 m", 12, anchor="end")
    sh.leader(2.5, 2.6, Ru, 1.75, "Ático técnico (AC, quadro)", 12, anchor="end")
    sh.leader(HF - 0.05, 1.9, Ru, 2.2, "J1 fresta 1,60 x 0,60 em corte", 12, anchor="end")
    sh.leader(HF - 0.05, 0.8, Ru, 1.3, "Painel SIP 100 mm + ripado", 12, anchor="end")
    sh.text(2.45, 2.2, "porta de correr 0,90 x 2,10", 8.5, EARTH, dy=3)
    sh.text(2.45, 1.95, "(o plano corta o vão)", 8.5, EARTH, dy=3)
    sh.leader(-HF - 0.03, 1.5, Lu, 3.4, "PC1 porta de correr em corte", 12, anchor="end")
    sh.leader(PX + 1.1, 2.6, Lu, 4.2, "Vela: postes Ø76 h 2,40 + cabo", 12, anchor="end")
    sh.leader(-HF, 2.2, Lu, 2.7, "Pilar P4 Ø101,6 + madeira", 12, anchor="end")
    sh.leader(-5.5, -0.12, Lu, 1.3, "Deck cumaru · vigas U 150", 12, anchor="end")
    sh.leader(-4.7, -0.55, Lu, 0.5, "Estacas Ø76, cabeçote ajustável", 12, anchor="end")
    sh.leader(0.4, 0.62, 0.0, 1.55, "Cama king sob a lanterna", 11, anchor="end")
    # cotas
    yb = -1.05
    sh.dim(xd, yb, -HF, yb, -0.3, label="2,60 (deck)")
    sh.dim(-HF, yb, L.X_PART, yb, -0.3, label="4,95 (estar + suíte)")
    sh.dim(L.X_PART, yb, HF, yb, -0.3, label="1,85 (banho)")
    sh.dim(PX, yb, HF, yb, -0.85, label=fmt(HF - PX) + " (vela + deck + pavilhão)")
    sh.dim(5.8, 0, 5.8, L.Z_TOP, 0.0, label="5,20"); sh.dim(6.4, 0, 6.4, L.Z_LANTERN, 0.0, label="4,60 (anel)"); sh.dim(7.0, 0, 7.0, L.Z_EAVE, 0.0, label="2,70 (beiral)")
    sh.dim(4.2, 0, 4.2, 2.4, 0.0, label="2,40 (forro)", size=10)
    sh.dim(-7.5, 0, -7.5, PC1["h"], 0.0, label="2,40 (PC1)", size=10)
    sh.dim(-7.5, -0.9, -7.5, 0, 0.0, label="0,90 (máx.)", size=10)
    sh.scalebar(-8.3, -2.2, 5)
    sh.title_block("ZION LODGE", "Corte longitudinal A-A", "1:50 (A1)", "06/LG", "Deck e vela, cama sob a lanterna, banho com ático técnico, envelope em 4 camadas"[:70])
    return sh

def corte_transv():
    sh = Sheet(1600, 1000, scale=88, ox=800, oy=690, flip_x=True)
    sh.header("Zion Lodge · Corte transversal B-B", "Plano x = 0 (centro da cama e da lanterna) · olhar para +x (parede do banho ao fundo) · vidro cortado nas faces laterais")
    ground(sh, -7.2, 7.2, 0.9)
    for py in (-HF, -2.55, -0.85, 0.85, 2.55, HF):
        sh.rect(py - 0.04, -0.9, py + 0.04, -0.22, fill=STEEL, stroke="none"); sh.rect(py - 0.12, -0.24, py + 0.12, -0.2, fill=STEEL, stroke="none")
    sh.rect(-HF, -0.2, HF, -0.05, fill=sh.pattern("insul"), stroke=GREEN, sw=0.9); sh.rect(-HF, -0.05, HF, 0.0, fill=WOOD2, stroke=GREEN, sw=0.5)
    # fundo: parede-corda do banho (x 1,55) com a porta, pilares P1/P8 acima dela, parede do fundo e anel
    sh.rect(-YC, 0, YC, 2.4, fill="#EDE3D3", stroke=GREEN, sw=0.8)
    sh.rect(-0.5, 0, 0.4, 2.1, fill="#D9D3C6", stroke=GREEN, sw=0.8)                       # vão da porta (banho ao fundo)
    sh.rect(-0.45, 1.6, 0.35, 2.05, fill=GLASS, stroke=GREEN, sw=0.5, opacity=0.6)          # J1 vista pelo vão
    sh.rect(0.42, 0, 1.32, 2.1, fill="#F7F3EC", stroke=GREEN, sw=0.7)                       # folha recolhida
    sh.rect(-YC, 2.4, YC, L.Z_EAVE - 0.15, fill="#EDE3D3", stroke=GREEN, sw=0.6)            # parede do fundo (face 7-0) acima do forro
    for yy in (V[0][1], V[7][1]): column(sh, yy)
    sh.rect(-0.5, 2.5, 0.5, 2.7, fill="#E5E1D8", stroke=GREEN, sw=0.8); sh.text(0.0, 2.6, "AC", 9, dy=3)
    sh.rect(2.2, 0.0, 2.95, 0.9, fill=WOOD2, stroke=GREEN, sw=0.7, opacity=0.8)             # café / minibar (vista)
    sh.rect(-2.95, 0.0, -2.2, 2.2, fill=WOOD2, stroke=GREEN, sw=0.8, opacity=0.8)           # closet (vista)
    sh.text(-2.57, 1.1, "closet", 9, EARTH, rotate=-90)
    for yy in (-HF, HF): column(sh, yy)
    eave_ring(sh, -HF - 0.12, HF + 0.12, far=True)
    # vidros cortados (faces 1-2 e 5-6)
    for yy in (-HF, HF):
        sh.rect(yy - 0.03, 0, yy + 0.03, L.Z_EAVE - 0.15, fill=GLASS, stroke=GREEN, sw=1.0)
    # cobertura + caibros (x > 0: vértices 0, 1, 6, 7) + lanterna
    roof_section(sh)
    rafters_section(sh, [(-HF, -0.69), (V[7][1], -0.29), (V[0][1], 0.29), (HF, 0.69)])
    lantern(sh)
    # mobiliário cortado: cama e criados-mudos
    sh.rect(-0.97, 0.0, 0.97, 0.35, fill=WOOD2, stroke=GREEN, sw=0.8); sh.rect(-0.97, 0.35, 0.97, 0.62, fill="#FFFFFF", stroke=GREEN, sw=0.8)
    sh.rect(-1.7, 0, -1.1, 0.5, fill=WOOD2, stroke=GREEN, sw=0.7); sh.rect(1.1, 0, 1.7, 0.5, fill=WOOD2, stroke=GREEN, sw=0.7)
    for y in (-3.2, 3.2): sh.circle(y, 0.12, 0.04, fill="#F2C14E", stroke="none")
    person(sh, 1.95)
    # rótulos (com flip_x, +y fica à esquerda): longos acima da cobertura, curtos nas faixas laterais
    Lu, Ru = 5.2, -5.2
    sh.leader(0.0, L.Z_TOP, 1.6, 5.85, "Lanterna Zion: luz zenital no centro geométrico, sobre a cama", 12, anchor="end")
    sh.leader(-2.0, L.roof_z(2.0), -3.2, 5.25, "Membrana PVDF em 8 gomos · câmara ventilada", 12, anchor="start")
    sh.leader(2.4, L.roof_z(2.4) - 0.25, Lu, 4.5, "Forro + lã PET 50 mm", 12, anchor="end")
    sh.leader(2.1, L.Z_EAVE + (L.Z_LANTERN - L.Z_EAVE) * 0.45, Lu, 3.95, "Caibro Ø76,1 (8 radiais)", 12, anchor="end")
    sh.leader(HF + 0.05, 2.62, Lu, 3.4, "Anel de beiral 150 x 100", 12, anchor="end")
    sh.leader(HF, 1.5, Lu, 2.5, "VF1 vidro insulado", 12, anchor="end")
    sh.leader(2.57, 0.7, Lu, 1.7, "Café / minibar ao fundo", 12, anchor="end")
    sh.leader(3.2, 0.12, Lu, 0.8, "LED 2700 K no rodapé", 12, anchor="end")
    sh.leader(-0.5, 2.6, Ru, 4.5, "Ático técnico do banho", 12, anchor="start")
    sh.leader(-HF - 0.05, 2.62, Ru, 3.7, "Anel de beiral sobre P6", 12, anchor="start")
    sh.leader(-2.57, 2.1, Ru, 2.9, "Closet 1,70 x 0,75", 12, anchor="start")
    sh.leader(-0.05, 1.3, Ru, 2.1, "Porta do banho 0,90 x 2,10", 12, anchor="start")
    sh.leader(-1.5, 1.8, Ru, 1.3, "Parede-corda do banho", 12, anchor="start")
    sh.leader(-2.55, -0.55, Ru, 0.45, "Estacas Ø76 · quadro U 150", 12, anchor="start")
    sh.leader(0.4, 0.62, 1.3, 1.3, "Cama king 1,93 x 2,03", 11, anchor="end")
    # cotas
    yb = -1.05
    sh.dim(-HF, yb, HF, yb, -0.3, label="6,80 (entre faces)")
    sh.dim(-R_EDGE, yb, R_EDGE, yb, -0.85, label="8,60 (cobertura)")
    sh.dim(6.6, 0, 6.6, L.Z_TOP, 0.0, label="5,20"); sh.dim(7.2, 0, 7.2, L.Z_EAVE, 0.0, label="2,70 (beiral)")
    sh.dim(-7.2, 0, -7.2, L.Z_LANTERN, 0.0, label="4,60 (anel)"); sh.dim(-7.8, 0, -7.8, 2.4, 0.0, label="2,40 (forro do banho)")
    sh.dim(-7.8, -0.9, -7.8, 0, 0.0, label="0,90", size=10)
    sh.scalebar(7.2, -2.2, 4)
    sh.title_block("ZION LODGE", "Corte transversal B-B", "1:45 (A1)", "07/LG", "Cama no centro geométrico sob a lanterna; parede do banho ao fundo")
    return sh


def build():
    os.makedirs(OUT, exist_ok=True)
    planta(True).save(os.path.join(OUT, "02_planta_humanizada.svg"))
    planta(False).save(os.path.join(OUT, "03_planta_tecnica.svg"))
    planta_estrutural().save(os.path.join(OUT, "03b_planta_estrutural.svg"))
    elev_frontal().save(os.path.join(OUT, "04_elevacao_frontal.svg"))
    fachada_traseira().save(os.path.join(OUT, "04b_fachada_traseira.svg"))
    elev_lateral().save(os.path.join(OUT, "05_elevacao_lateral.svg"))
    corte_long().save(os.path.join(OUT, "06_corte_longitudinal.svg"))
    corte_transv().save(os.path.join(OUT, "07_corte_transversal.svg"))
    print("lodge drawings ok ->", OUT)

if __name__ == "__main__":
    build()

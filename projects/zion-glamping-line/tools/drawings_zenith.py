# -*- coding: utf-8 -*-
"""Desenhos técnicos 2D do ZION ZENITH: plantas, elevações e cortes (SVG)."""
import math, os
from geometry import Zenith
from svgkit import *
from drawings_cocoon import draw_furniture, sym_tub

Z = Zenith()
OUT = os.path.join(os.path.dirname(__file__), "..", "zenith", "desenhos")
PERSON = '<circle cx="0" cy="-165" r="11" fill="none" stroke="{c}" stroke-width="1.5"/><path d="M0 -152 V-70 M0 -70 L-16 0 M0 -70 L16 0 M-22 -100 L0 -135 L22 -100" fill="none" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>'

def person(sh, x, z=0):
    sh.add(f'<g transform="translate({sh.X(x):.1f},{sh.Y(z):.1f}) scale({sh.s / 100:.3f})">{PERSON.format(c=GREEN)}</g>')

def slats(sh, x1, x2, z1, z2, step=0.08):
    """ripado vertical em elevação"""
    x = x1
    while x < x2:
        sh.line(x, z1, x, z2, WOOD2, 1.4, opacity=0.9)
        x += step

def roof_outline_pts():
    x0, x1, y0, y1 = Z.roof_bounds()
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

def peaks_plan(sh, human):
    for p in Z.PEAKS:
        sh.circle(p["x"], p["y"], p["r"], fill="none", stroke=GREEN, sw=1.0, dash="5 3")
        sh.circle(p["x"], p["y"], 0.07, fill=STEEL, stroke="none")
        for k in range(3):
            ang = math.pi / 2 + 2 * math.pi * k / 3
            sh.line(p["x"], p["y"], p["x"] + p["r"] * math.cos(ang), p["y"] + p["r"] * math.sin(ang), STEEL, 0.9)

def contours(sh, levels=(3.0, 3.4, 3.8, 4.2, 4.6, 5.0, 5.4), color=EARTH):
    """curvas de nível da membrana (marching squares simplificado) para leitura da forma em planta"""
    x0, x1, y0, y1 = Z.roof_bounds()
    nx, ny = 120, 72
    import numpy as np
    xs = np.linspace(x0, x1, nx + 1); ys = np.linspace(y0, y1, ny + 1)
    G = np.array([[Z.roof_z(x, y) for y in ys] for x in xs])
    for lv in levels:
        segs = []
        for i in range(nx):
            for j in range(ny):
                sq = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
                pts = []
                for (a, b) in [(0, 1), (1, 2), (2, 3), (3, 0)]:
                    (ia, ja), (ib, jb) = sq[a], sq[b]
                    va, vb = G[ia, ja] - lv, G[ib, jb] - lv
                    if (va < 0) != (vb < 0):
                        t = va / (va - vb)
                        pts.append((xs[ia] + (xs[ib] - xs[ia]) * t, ys[ja] + (ys[jb] - ys[ja]) * t))
                if len(pts) >= 2:
                    segs.append((pts[0], pts[1]))
        for (p, q) in segs:
            sh.line(p[0], p[1], q[0], q[1], color, 0.55, opacity=0.75)

# ------------------------------------------------------------------ PLANTA
def planta(human=True):
    sh = Sheet(1600, 1000, scale=82, ox=390, oy=520)
    sh.header("Zion Zenith · Planta baixa " + ("humanizada" if human else "técnica"),
              "Cabana escultural de dois cumes · corpo 9,50 x 5,40 m · piso interno 48,4 m² · terraço 20,4 m² + passarela 7,6 m² · total 79,3 m²")
    D, Wk = Z.DECK, Z.WALK
    # deck e passarela
    sh.rect(D["x1"], D["y1"], D["x2"], D["y2"], fill=sh.pattern("deck") if human else "none", stroke=GREEN, sw=1.1)
    sh.rect(Wk["x1"], Wk["y1"], Wk["x2"], Wk["y2"], fill=sh.pattern("deck") if human else "none", stroke=GREEN, sw=1.1)
    for i in range(3):
        sh.rect(D["x1"] - 0.3 * (i + 1), -1.2, D["x1"] - 0.3 * i, 1.2, fill=WOOD2 if human else "none", stroke=GREEN, sw=0.7)
    # hidromassagem
    H = Z.HOTTUB
    sh.circle(H["x"], H["y"], H["r"], fill="#CBDCE0" if human else "none", stroke=GREEN, sw=1.0)
    sh.circle(H["x"], H["y"], H["r"] - 0.12, fill="none", stroke=GREEN, sw=0.5)
    # projeção da cobertura
    sh.poly(roof_outline_pts(), fill="none", stroke=GREEN, sw=1.0, dash="10 5")
    # bordas em catenária (planta: leve recorte)
    # corpo: piso interno
    sh.rect(0.1, -2.6, 9.4, 2.6, fill=sh.pattern("wood") if human else "none", stroke="none")
    if human:
        sh.rect(6.45, -2.6, 9.4, 2.6, fill=sh.pattern("tile"), stroke="none")
    # paredes (espessura 0,10) e vidros
    for w in Z.walls():
        (xa, ya), (xb, yb) = w["p1"], w["p2"]
        if w["kind"] == "window": continue
        vert = abs(xa - xb) < 1e-6
        if w["kind"] == "glass":
            if vert: sh.rect(xa - 0.03, ya, xa + 0.03, yb, fill=GLASS, stroke=GREEN, sw=0.8)
            else: sh.rect(xa, ya - 0.03, xb, ya + 0.03, fill=GLASS, stroke=GREEN, sw=0.8)
        else:
            inward = -1 if (vert and xa > 5) or (not vert and ya > 0) else 1
            if vert: sh.rect(xa, ya, xa + inward * 0.10, yb, fill=sh.pattern("hatch") if not human else "#B29A78", stroke=GREEN, sw=0.9)
            else: sh.rect(xa, ya, xb, ya + inward * 0.10, fill=sh.pattern("hatch") if not human else "#B29A78", stroke=GREEN, sw=0.9)
    # janelas em paredes de madeira (marcar)
    for w in Z.walls():
        if w["kind"] != "window": continue
        (xa, ya), (xb, yb) = w["p1"], w["p2"]
        if abs(xa - xb) < 1e-6: sh.rect(xa - 0.06, ya, xa + 0.06, yb, fill=GLASS, stroke=GREEN, sw=0.7)
        else: sh.rect(xa, ya - 0.06, xb, ya + 0.06, fill=GLASS, stroke=GREEN, sw=0.7)
    # folhas de correr da fachada (2 centrais)
    for (ya, yb) in [(-1.35, 0.0), (0.0, 1.35)]:
        sh.line(0.12, ya, 0.12, yb, GREEN, 1.4)
    sh.add(f'<path d="M{sh.X(0.12):.1f},{sh.Y(-0.1):.1f} l-8,-6 l0,12 z" fill="{GREEN}"/>')
    sh.add(f'<path d="M{sh.X(0.12):.1f},{sh.Y(0.1):.1f} l-8,6 l0,-12 z" fill="{GREEN}"/>')
    # parede da cabeceira (mastro) + divisória WC
    sh.rect(6.2, -2.6, 6.45, 1.5, fill=sh.pattern("hatch") if not human else "#B29A78", stroke=GREEN, sw=0.9)
    sh.rect(6.45, 1.55, 6.5, 2.6, fill="none", stroke=GREEN, sw=0.8)  # porta de correr
    sh.line(6.32, 1.5, 6.32, 2.6, GREEN, 0.6, dash="4 3")
    sh.rect(7.2, -2.6, 7.25, -1.3, fill=GREEN, stroke=GREEN, sw=0.4)
    # pilares
    for (cx, cy) in Z.columns():
        sh.circle(cx, cy, 0.05, fill=STEEL, stroke="none")
    # postes externos
    for (px, py) in Z.posts():
        sh.circle(px, py, 0.04, fill=STEEL, stroke="none")
        sh.circle(px, py, 0.16, fill="none", stroke=STEEL, sw=0.6)
    # mastros, anéis, coroas
    peaks_plan(sh, human)
    # mobiliário
    draw_furniture(sh, Z.furniture(), human)
    sh.line(8.3, -2.6, 8.3, -1.4, GLASS, 4); sh.line(8.3, -2.6, 8.3, -1.4, GREEN, 0.8)
    # rótulos
    lab = [("ESTAR", 1.6, -0.5, "16,2 m²"), ("SUÍTE", 5.0, 0.0, "14,3 m²"), ("BANHO", 7.9, 0.4, "15,3 m²"),
           ("TERRAÇO", -1.6, 1.4, "20,4 m²"), ("CLOSET", 4.8, 2.3, ""), ("CAFÉ", 1.6, 2.24, "")]
    for t, x, y, a in lab:
        sh.text(x, y, t, 12 if a else 9, GREEN, weight=700, spacing=0.22, dy=(0 if not a else -4))
        if a: sh.text(x, y, a, 10, EARTH, dy=10)
    if human:
        sh.leader(6.3, 0.4, 6.9, 4.45, "Óculo do Zênite Ø1,20 sobre a cama (cume 5,80 m)", 11, anchor="start")
        sh.leader(1.6, 1.6, 1.0, 4.45, "Respiro: cume secundário 4,60 m com chaminé de ventilação", 11, anchor="end")
        sh.leader(H["x"], H["y"], -2.6, -4.2, "Hidromassagem Ø1,90 sob o beiral", 11)
        sh.leader(0.0, -1.35, 0.6, -4.2, "Fachada 5,40 x 2,75: 2 fixas + 2 de correr", 11)
        sh.leader(3.5, -2.7, 4.4, -4.2, "Vidro lateral da suíte 6,40 m", 11)
        sh.leader(8.8, -3.7, 8.2, -4.55, "Postes externos Ø76 inclinados 8°", 11)
        sh.leader(9.0, 0.35, 10.8, 1.3, "Banheira com fresta de vidro", 11)
        sh.leader(10.25, -1.8, 10.8, -2.6, "Condensadora oculta", 11)
        sh.leader(1.6, 1.6, 1.6, 1.6, "", 8, dot=False)
    # cotas gerais
    sh.dim(0.0, -3.9, 9.5, -3.9, -0.7, label="9,50 (corpo)")
    sh.dim(-3.0, -3.9, 0.0, -3.9, -0.7, label="3,00")
    sh.dim(Z.roof_bounds()[0], -3.9, Z.roof_bounds()[1], -3.9, -1.3, label="12,90 (cobertura)")
    sh.dim(10.7, -2.7, 10.7, 2.7, 0.6, label="5,40")
    sh.dim(10.7, -3.7, 10.7, 3.7, 1.25, label="7,40 (cobertura)")
    sh.dim(-3.5, -3.4, -3.5, 3.4, -0.4, label="6,80")
    if not human:
        sh.dim_chain([0, 3.2, 6.4, 9.5], 3.75, 0.45)
        sh.dim(0.1, 3.75, 6.2, 3.75, 1.0, label="6,10 (estar + suíte)")
        sh.dim(6.45, 3.75, 9.4, 3.75, 1.0, label="2,95 (banho)")
        sh.dim(-2.4, 3.75, 0, 3.75, 1.0, label="2,40 (beiral)")
        sh.dim(6.3, -2.7, 6.3, 0.4, 0, label="", color=EARTH)
        sh.text(6.55, -1.1, "y = +0,40", 9, EARTH, rotate=-90)
        sh.text(1.85, 0.55, "x 1,60 · y +1,60", 9, EARTH)
        sh.text(6.55, 0.95, "x 6,30", 9, EARTH)
        contours(sh)
        sh.text(9.9, 3.3, "curvas de nível da membrana a cada 0,40 m", 9, EARTH, anchor="start")
        # estacas
        npiles = 0
        for px in [-2.6, -0.2, 2.2, 4.6, 7.0, 9.4]:
            for py in [-2.6, -1.3, 0.0, 1.3, 2.6]:
                if px < 0 and abs(py) > 3.0: continue
                npiles += 1
                sh.add(f'<g transform="translate({sh.X(px):.1f},{sh.Y(py):.1f})"><circle r="4" fill="none" stroke="{STEEL}" stroke-width="0.9"/><line x1="-4" y1="0" x2="4" y2="0" stroke="{STEEL}" stroke-width="0.7"/><line x1="0" y1="-4" x2="0" y2="4" stroke="{STEEL}" stroke-width="0.7"/></g>')
        for (px, py) in Z.posts():
            npiles += 1
        sh.text(-3.0, -4.75, f"○+ estaca helicoidal Ø76 / hélice Ø300 (malha 2,40 x 1,30 m: {npiles - 7} sob o piso + 7 estacas de tração dos postes)", 10, STEEL, anchor="start")
        for (x, y1, y2, lbl) in [(6.3, -4.1, 4.1, "B")]:
            sh.line(x, y1, x, y2, GREEN, 1.4, dash="10 4")
            sh.text(x, y2 + 0.2, lbl, 12, weight=700); sh.text(x, y1 - 0.35, lbl, 12, weight=700)
        sh.line(-3.3, 0.4, 11.0, 0.4, GREEN, 1.4, dash="10 4")
        sh.text(-3.55, 0.4, "A", 12, weight=700, dy=4); sh.text(11.2, 0.4, "A", 12, weight=700, dy=4)
    sh.north(1500, 140, angle=-90)
    sh.scalebar(-3.0, -5.55, 5)
    sh.title_block("ZION ZENITH", "Planta baixa " + ("humanizada" if human else "técnica cotada"), "1:50 (A1) · cotas em metros", "02/27" if human else "03/27",
                   "Estar, suíte sob o Óculo, banho com banheira, terraço com hidromassagem")
    return sh

# ------------------------------------------------------------------ ELEVAÇÕES
def ground(sh, x1, x2, depth=0.6):
    sh.rect(x1, -depth, x2, -0.02, fill=sh.pattern("soil"), stroke="none")
    sh.line(x1, -0.02, x2, -0.02, GREEN, 1.0)

def elev_frontal():
    sh = Sheet(1600, 1000, scale=92, ox=800, oy=740, flip_x=True)
    sh.header("Zion Zenith · Elevação frontal", "Vista da fachada panorâmica (olhar para +x) · cobertura 7,40 m · cume 5,80 m")
    ground(sh, -6.5, 6.5)
    for py in [-2.6, -1.3, 0.0, 1.3, 2.6]:
        sh.rect(py - 0.04, -0.6, py + 0.04, -0.2, fill=STEEL, stroke="none")
    sh.rect(-3.4, -0.2, 3.5, -0.05, fill=WOOD2, stroke=GREEN, sw=0.9); sh.rect(-3.4, -0.05, 3.5, 0.0, fill=GREEN, stroke="none")
    # silhueta da cobertura
    sil = Z.silhouette_front(120)
    x0, x1, y0, y1 = Z.roof_bounds()
    # borda frontal (catenária vista de frente)
    front_edge = [(y, Z.edge_height(x0, y)) for y in [y0 + (y1 - y0) * i / 60 for i in range(61)]]
    sh.poly(sil + front_edge[::-1], fill=MEMB, stroke=GREEN, sw=1.8)
    # corpo (atrás): paredes e vidro
    sh.rect(-2.7, 0, 2.7, 2.75, fill=GLASS, stroke=GREEN, sw=1.2)
    for yy in (-1.35, 0.0, 1.35):
        sh.line(yy, 0, yy, 2.75, GREEN, 1.2)
    sh.rect(-2.7, 2.75, 2.7, 2.9, fill=STEEL, stroke=GREEN, sw=0.6)   # anel de beiral
    # interior sugerido: cama e sofá
    sh.rect(-0.97, 0.0, 0.97, 0.62, fill="#FFFFFF", stroke=GREEN, sw=0.6, opacity=0.7)
    sh.rect(-1.05, 0.0, 1.15, 0.8, fill=SAND, stroke=GREEN, sw=0.6, opacity=0.6)
    # postes externos frontais
    for py in (y0, y1):
        top = Z.edge_height(x0, py)
        lean = 0.08 * (1 if py > 0 else -1)
        sh.line(py, -0.05, py + lean * top / 0.9, top, STEEL, 4)
    # hidromassagem no terraço (vista)
    sh.rect(-3.0, 0.0, -1.1, 0.55, fill="#CBDCE0", stroke=GREEN, sw=0.8)
    # mastros (tracejado, atrás)
    for p in Z.PEAKS:
        sh.line(p["y"], 0, p["y"], p["mast_top"], STEEL, 1.0, dash="6 4", opacity=0.6)
        sh.circle(p["y"], p["h"], 0.08, fill="none", stroke=GREEN, sw=0.8)
    # rótulos
    sh.leader(0.4, 5.8, 1.6, 6.45, "Cume principal 5,80 m: Óculo do Zênite Ø1,20", 12, anchor="end")
    sh.leader(1.6, 4.6, 3.2, 5.4, "Cume secundário 4,60 m: chaminé do Respiro", 12, anchor="end")
    sh.leader(-3.2, 3.3, -4.4, 4.2, "Membrana PVDF em balanço 2,40 m", 12, anchor="start")
    sh.leader(-3.7, 2.4, -4.6, 3.1, "Borda em catenária, cabo Ø12", 12, anchor="start")
    sh.leader(-2.0, 1.5, -4.6, 1.6, "Fachada 5,40 x 2,75, 2 de correr", 12, anchor="start")
    sh.leader(3.75, 1.3, 4.6, 1.0, "Poste externo Ø76 inclinado 8°, estaiado", 12, anchor="end")
    sh.leader(-2.0, 0.3, -4.6, 0.5, "Hidromassagem Ø1,90 no terraço", 12, anchor="start")
    sh.leader(-1.0, 2.82, -4.6, 2.35, "Anel de beiral 150 x 100 a 2,90 m", 12, anchor="start")
    sh.dim(-2.7, -0.9, 2.7, -0.9, -0.35, label="5,40 (corpo)")
    sh.dim(y0, -0.9, y1, -0.9, -0.95, label="7,40 (cobertura)")
    sh.dim(-3.4, -0.9, 3.5, -0.9, -1.55, label="6,90 (deck + passarela)")
    sh.dim(-4.2, 0, -4.2, 5.8, -0.6, label="5,80")
    sh.dim(-4.2, 0, -4.2, 2.75, -1.15, label="2,75")
    sh.dim(4.2, 0, 4.2, 4.6, 0.6, label="4,60")
    sh.scalebar(6.3, -2.2, 4)
    sh.title_block("ZION ZENITH", "Elevação frontal", "1:50 (A1)", "04/27", "Silhueta assimétrica de dois cumes; fachada de vidro sob o beiral")
    return sh

def elev_lateral():
    sh = Sheet(1600, 1000, scale=96, ox=470, oy=730)
    sh.header("Zion Zenith · Elevação lateral direita", "Vista do vidro da suíte (olhar para +y) · comprimento da cobertura 12,90 m")
    ground(sh, -4.5, 12.0)
    for px in [-2.6, -0.2, 2.2, 4.6, 7.0, 9.4]:
        sh.rect(px - 0.04, -0.6, px + 0.04, -0.2, fill=STEEL, stroke="none")
    sh.rect(-3.0, -0.2, 9.5, -0.05, fill=WOOD2, stroke=GREEN, sw=0.9); sh.rect(-3.0, -0.05, 9.5, 0.0, fill=GREEN, stroke="none")
    for i in range(3):
        sh.rect(-3.0 - 0.3 * (i + 1), -0.2 + 0.05 * (i + 1) - 0.15, -3.0 - 0.3 * i, -0.2 + 0.05 * (i + 1), fill=WOOD2, stroke=GREEN, sw=0.7)
    x0, x1, y0, y1 = Z.roof_bounds()
    sil = Z.silhouette_side(160)
    side_edge = [(x, Z.edge_height(x, y0)) for x in [x0 + (x1 - x0) * i / 80 for i in range(81)]]
    sh.poly(sil + side_edge[::-1], fill=MEMB, stroke=GREEN, sw=1.8)
    # corpo: vidro 0..6,4, madeira 6,4..9,5
    sh.rect(0, 0, 6.4, 2.75, fill=GLASS, stroke=GREEN, sw=1.2)
    for xx in (1.6, 3.2, 4.8):
        sh.line(xx, 0, xx, 2.75, GREEN, 1.0)
    sh.rect(6.4, 0, 9.5, 2.75, fill="#C9B08C", stroke=GREEN, sw=1.0)
    slats(sh, 6.44, 9.5, 0, 2.75)
    sh.rect(8.3, 1.9, 9.3, 2.4, fill=GLASS, stroke=GREEN, sw=0.8)
    sh.rect(0, 2.75, 9.5, 2.9, fill=STEEL, stroke=GREEN, sw=0.6)
    # interior sugerido
    sh.rect(4.1, 0.0, 6.15, 0.62, fill="#FFFFFF", stroke=GREEN, sw=0.6, opacity=0.7)
    sh.rect(0.5, 0.0, 2.4, 0.45, fill=SAND, stroke=GREEN, sw=0.6, opacity=0.7)
    # postes externos laterais
    for px in (x0, 4.0, x1):
        top = Z.edge_height(px, y0)
        sh.line(px, -0.05, px, top, STEEL, 4)
    # mastros tracejados
    for p in Z.PEAKS:
        sh.line(p["x"], 0, p["x"], p["mast_top"], STEEL, 1.0, dash="6 4", opacity=0.6)
        sh.circle(p["x"], p["h"], 0.08, fill="none", stroke=GREEN, sw=0.8)
    # condensadora
    sh.rect(9.85, 0.0, 10.65, 0.62, fill="#E5E1D8", stroke=GREEN, sw=0.8)
    slats(sh, 9.8, 10.7, 0, 1.3, 0.1)
    # rótulos
    sh.leader(6.3, 5.8, 7.6, 6.35, "Cume principal 5,80 m sobre a parede da cabeceira (x 6,30)", 12)
    sh.leader(1.6, 4.6, 0.2, 5.6, "Cume secundário 4,60 m sobre a Ilha do Café (x 1,60)", 12, anchor="end")
    sh.leader(-1.5, 2.3, -2.4, 3.6, "Balanço 2,40 m sobre o terraço", 12, anchor="end")
    sh.leader(3.2, 1.4, 2.6, -1.1, "Vidro lateral da suíte 6,40 x 2,75 (4 painéis)", 12)
    sh.leader(8.0, 1.2, 8.6, -1.1, "Painel SIP 100 mm + ripado termotratado 40 x 40", 12)
    sh.leader(4.0, 2.0, 5.6, -1.1, "Poste externo Ø76 estaiado", 12)
    sh.leader(10.3, 0.8, 10.0, 2.2, "Condensadora", 12, anchor="end")
    sh.dim(0, -0.95, 9.5, -0.95, -0.35, label="9,50 (corpo)")
    sh.dim(-3.0, -0.95, 0, -0.95, -0.35, label="3,00 (terraço)")
    sh.dim(x0, -0.95, x1, -0.95, -0.95, label="12,90 (cobertura)")
    sh.dim(10.9, 0, 10.9, 5.8, 0.4, label="5,80")
    sh.dim(10.9, 0, 10.9, 2.9, 0.85, label="2,90 (beiral)")
    sh.dim(-3.9, -0.6, -3.9, 0, -0.5, label="0,60")
    sh.scalebar(-4.3, -2.4, 5)
    sh.title_block("ZION ZENITH", "Elevação lateral", "1:50 (A1)", "05/27", "Dois cumes deslocados em diagonal: a silhueta muda a cada ângulo")
    return sh

# ------------------------------------------------------------------ CORTES
def corte_long():
    yc = 0.4
    sh = Sheet(1600, 1000, scale=96, ox=470, oy=730)
    sh.header("Zion Zenith · Corte longitudinal A-A", "Plano y = +0,40 (eixo do mastro principal) · olhar para +y · membrana externa, câmara, forro isolado")
    ground(sh, -4.5, 12.0, 0.9)
    for px in [-2.6, -0.2, 2.2, 4.6, 7.0, 9.4]:
        sh.rect(px - 0.04, -0.9, px + 0.04, -0.22, fill=STEEL, stroke="none")
        sh.rect(px - 0.12, -0.24, px + 0.12, -0.2, fill=STEEL, stroke="none")
    sh.rect(-3.0, -0.2, 9.5, -0.05, fill=sh.pattern("insul"), stroke=GREEN, sw=0.9)
    sh.rect(-3.0, -0.05, 9.5, 0.0, fill=WOOD2, stroke=GREEN, sw=0.5)
    sh.rect(-3.0, -0.2, 0.0, -0.05, fill=sh.pattern("deck"), stroke=GREEN, sw=0.9)
    x0, x1, y0, y1 = Z.roof_bounds()
    prof = Z.ridge_profile(yc, 160)
    liner = [(x, Z.liner_z(x, yc)) for x in [0 + 9.5 * i / 120 for i in range(121)]]
    # câmara entre membrana e forro (dentro do corpo)
    inner_prof = [(x, z) for (x, z) in prof if 0 <= x <= 9.5]
    sh.poly(inner_prof + liner[::-1], fill=sh.pattern("insul"), stroke="none")
    sh.poly(prof, close=False, stroke=EARTH, sw=3.2)
    sh.poly(liner, close=False, stroke=GREEN, sw=1.2)
    # paredes cortadas (frente vidro, fundos madeira)
    sh.rect(-0.03, 0, 0.03, 2.75, fill=GLASS, stroke=GREEN, sw=1.0)
    sh.rect(9.4, 0, 9.5, 2.75, fill=sh.pattern("hatch"), stroke=GREEN, sw=1.0)
    sh.rect(9.4, 1.5, 9.5, 2.15, fill=GLASS, stroke=GREEN, sw=0.8)
    sh.rect(-0.03, 2.75, 0.03, 2.9, fill=STEEL, stroke="none"); sh.rect(9.4, 2.75, 9.5, 2.9, fill=STEEL, stroke="none")
    # parede da cabeceira com mastro
    sh.rect(6.2, 0, 6.45, 2.75, fill=sh.pattern("hatch"), stroke=GREEN, sw=1.0)
    p1 = Z.PEAKS[0]
    sh.rect(p1["x"] - 0.07, 0, p1["x"] + 0.07, p1["mast_top"], fill=STEEL, stroke="none")
    for k in range(3):
        ang = math.pi / 2 + 2 * math.pi * k / 3
        sh.line(p1["x"], p1["mast_top"], p1["x"] + p1["r"] * math.cos(ang), p1["h"] - 0.05, STEEL, 2.4)
    sh.rect(p1["x"] - p1["r"], p1["h"] - 0.08, p1["x"] + p1["r"], p1["h"], fill=STEEL, stroke="none")
    sh.add(f'<path d="M{sh.X(p1["x"] - p1["r"]):.1f},{sh.Y(p1["h"]):.1f} Q{sh.X(p1["x"]):.1f},{sh.Y(p1["h"] + 0.35):.1f} {sh.X(p1["x"] + p1["r"]):.1f},{sh.Y(p1["h"]):.1f}" fill="{GLASS}" stroke="{GREEN}" stroke-width="1"/>')
    # mastro 2 (atrás do plano, tracejado) e chaminé
    p2 = Z.PEAKS[1]
    sh.line(p2["x"], 0, p2["x"], p2["mast_top"], STEEL, 1.2, dash="6 4", opacity=0.7)
    sh.rect(p2["x"] - p2["r"], p2["h"] - 0.05, p2["x"] + p2["r"], p2["h"] + 0.3, fill="none", stroke=GREEN, sw=0.8, dash="4 3")
    sh.line(p2["x"], p2["mast_top"], p2["x"], p2["h"] - 0.05, STEEL, 1.0, dash="6 4", opacity=0.7)
    # forro do banho e ático
    sh.line(6.45, 2.5, 9.4, 2.5, GREEN, 1.2)
    sh.rect(7.2, 2.6, 8.2, 2.88, fill="#E5E1D8", stroke=GREEN, sw=0.8); sh.text(7.7, 2.74, "AC", 9, dy=3)
    sh.rect(6.12, 2.05, 6.2, 2.25, fill=GREEN, stroke="none")
    # mobiliário em vista
    sh.rect(4.1, 0.0, 6.15, 0.35, fill=WOOD2, stroke=GREEN, sw=0.8); sh.rect(4.1, 0.35, 6.15, 0.62, fill="#FFFFFF", stroke=GREEN, sw=0.8)
    sh.rect(5.6, 0.62, 6.1, 0.8, fill="#F4EFE8", stroke=GREEN, sw=0.6)
    sh.rect(2.55, 0.0, 3.45, 0.8, fill=SAND, stroke=GREEN, sw=0.8)
    sh.rect(1.35, 0.0, 1.95, 0.35, fill=WOOD2, stroke=GREEN, sw=0.7)
    sh.rect(0.6, 0.0, 2.6, 0.9, fill=WOOD2, stroke=GREEN, sw=0.7, opacity=0.5)
    sh.rect(1.32, 0.9, 1.88, 2.75, fill=WOOD, stroke=GREEN, sw=0.7, opacity=0.6)
    sh.rect(6.5, 0.0, 7.05, 0.85, fill="#EFEDE6", stroke=GREEN, sw=0.8)
    sh.rect(8.6, 0.0, 9.35, 0.58, fill="#FFFFFF", stroke=GREEN, sw=0.9)
    sh.rect(3.8, 0.0, 5.8, 2.4, fill=WOOD2, stroke=GREEN, sw=0.7, opacity=0.18)  # closet ao fundo
    sh.text(4.8, 1.6, "closet ao fundo", 9, EARTH)
    person(sh, 3.3)
    # postes externos (frente e fundos)
    for px in (x0, x1):
        sh.line(px, -0.05, px, Z.edge_height(px, y0) + 0.15, STEEL, 4, opacity=0.5)
    # rótulos
    sh.leader(p1["x"], p1["h"] + 0.3, 7.8, 6.4, "Óculo do Zênite: anel Ø1,20 + cúpula de vidro laminado", 12)
    sh.leader(p1["x"] + 0.05, p1["mast_top"], 8.2, 5.4, "Coroa de 3 braços Ø48,3 sobre o mastro Ø139,7 x 4,5", 12)
    sh.leader(p2["x"], p2["h"] + 0.3, 0.8, 5.5, "Respiro: chaminé com veneziana motorizada (mastro 2 atrás do plano)", 12, anchor="end")
    sh.leader(4.5, Z.roof_z(4.5, yc), 3.4, 5.9, "Membrana PVDF · câmara ventilada · forro isolado (lã PET 50 mm + tecido)", 12, anchor="end")
    sh.leader(7.7, 2.74, 9.6, 3.6, "Ático técnico: evaporadora 18k BTU, aquecedor, quadro", 12, anchor="end")
    sh.leader(6.32, 1.5, 5.0, 3.4, "Parede da cabeceira contém o mastro M1", 12, anchor="end")
    sh.leader(6.16, 2.15, 4.4, 2.9, "Difusor linear", 12, anchor="end")
    sh.leader(-1.5, Z.roof_z(-1.5, yc), -2.4, 3.6, "Balanço sobre o terraço 2,40 m", 12, anchor="end")
    sh.leader(-1.0, -0.12, -3.9, 1.2, "Deck cumaru · vigas U 150 · PIR 50 mm", 12, anchor="start")
    sh.leader(8.95, 0.3, 11.4, 1.5, "Banheira 1,70 com fresta de vidro nos fundos", 12, anchor="end")
    sh.leader(7.0, -0.5, 8.9, -1.6, "Estacas helicoidais Ø76 · cabeçote ajustável", 12, anchor="end")
    sh.dim(0.1, -1.0, 6.2, -1.0, -0.3, label="6,10")
    sh.dim(6.45, -1.0, 9.4, -1.0, -0.3, label="2,95")
    sh.dim(-3.0, -1.0, 0.0, -1.0, -0.3, label="3,00")
    sh.dim(10.9, 0, 10.9, 5.8, 0.45, label="5,80")
    sh.dim(10.4, 0, 10.4, 2.75, 0.4, label="2,75")
    sh.dim(-3.9, -0.9, -3.9, 0, -0.5, label="0,90 (máx.)")
    sh.scalebar(-4.3, -2.5, 5)
    sh.title_block("ZION ZENITH", "Corte longitudinal A-A", "1:50 (A1)", "06/27", "Mastro e coroa do Zênite, óculo sobre a cama, ático técnico")
    return sh

def corte_transv():
    xc = 6.3
    sh = Sheet(1600, 1000, scale=92, ox=800, oy=740, flip_x=True)
    sh.header("Zion Zenith · Corte transversal B-B", "Plano x = 6,30 (mastro principal) · olhar para +x (banho ao fundo) · escala 1:45")
    ground(sh, -6.0, 6.0, 0.9)
    for py in [-2.6, -1.3, 0.0, 1.3, 2.6]:
        sh.rect(py - 0.04, -0.9, py + 0.04, -0.22, fill=STEEL, stroke="none")
        sh.rect(py - 0.12, -0.24, py + 0.12, -0.2, fill=STEEL, stroke="none")
    sh.rect(-2.7, -0.2, 3.5, -0.05, fill=sh.pattern("insul"), stroke=GREEN, sw=0.9)
    sh.rect(-2.7, -0.05, 3.5, 0.0, fill=WOOD2, stroke=GREEN, sw=0.5)
    sh.rect(2.7, -0.2, 3.5, -0.05, fill=sh.pattern("deck"), stroke=GREEN, sw=0.9)
    x0, x1, y0, y1 = Z.roof_bounds()
    prof = Z.cross_profile(xc, 120)
    liner = [(y, Z.liner_z(xc, y)) for y in [-2.7 + 5.4 * i / 100 for i in range(101)]]
    inner_prof = [(y, z) for (y, z) in prof if -2.7 <= y <= 2.7]
    sh.poly(inner_prof + liner[::-1], fill=sh.pattern("insul"), stroke="none")
    sh.poly(prof, close=False, stroke=EARTH, sw=3.2)
    sh.poly(liner, close=False, stroke=GREEN, sw=1.2)
    # paredes cortadas: direita (y=-2,7) madeira no banho; esquerda (y=+2,7) madeira
    sh.rect(-2.7, 0, -2.6, 2.75, fill=sh.pattern("hatch"), stroke=GREEN, sw=1.0)
    sh.rect(2.6, 0, 2.7, 2.75, fill=sh.pattern("hatch"), stroke=GREEN, sw=1.0)
    sh.rect(-2.7, 2.75, -2.6, 2.9, fill=STEEL, stroke="none"); sh.rect(2.6, 2.75, 2.7, 2.9, fill=STEEL, stroke="none")
    # parede da cabeceira cortada (y -2,6..1,5) com o mastro, passagem
    sh.rect(-2.6, 0, 1.5, 2.75, fill="#EDE3D3", stroke=GREEN, sw=0.8)   # face da parede cortada (vista frontal do plano de corte)
    sh.rect(-2.6, 0, 1.5, 2.75, fill=sh.pattern("hatch"), stroke="none", opacity=0.25)
    p1 = Z.PEAKS[0]
    sh.rect(p1["y"] - 0.07, 0, p1["y"] + 0.07, p1["mast_top"], fill=STEEL, stroke="none")
    for k in range(3):
        ang = math.pi / 2 + 2 * math.pi * k / 3
        sh.line(p1["y"], p1["mast_top"], p1["y"] + p1["r"] * math.sin(ang), p1["h"] - 0.05, STEEL, 2.4)
    sh.rect(p1["y"] - p1["r"], p1["h"] - 0.08, p1["y"] + p1["r"], p1["h"], fill=STEEL, stroke="none")
    sh.add(f'<path d="M{sh.X(p1["y"] - p1["r"]):.1f},{sh.Y(p1["h"]):.1f} Q{sh.X(p1["y"]):.1f},{sh.Y(p1["h"] + 0.35):.1f} {sh.X(p1["y"] + p1["r"]):.1f},{sh.Y(p1["h"]):.1f}" fill="{GLASS}" stroke="{GREEN}" stroke-width="1"/>')
    # passagem (y 1,5..2,6) com porta de correr; banho ao fundo (bancada, banheira)
    sh.rect(1.5, 0, 2.6, 2.2, fill="#F7F3EC", stroke=GREEN, sw=0.8)
    sh.rect(1.55, 0.0, 2.55, 0.85, fill="#EFEDE6", stroke=GREEN, sw=0.7, opacity=0.6)  # bancada vista pela passagem
    # difusores
    sh.rect(-1.2, 2.05, 0.9, 2.15, fill=GREEN, stroke="none")
    # deck lateral e poste externo
    for py in (y0, y1):
        sh.line(py, -0.05, py, Z.edge_height(4.0, py) + 0.1 if False else Z.roof_z(xc, py), STEEL, 4)
    sh.line(y1, Z.roof_z(xc, y1), y1 + 0.9, -0.05, STEEL, 1.0, dash="5 3")   # estai
    person(sh, 2.05)
    # rótulos
    sh.leader(p1["y"], p1["h"] + 0.3, 2.2, 6.4, "Óculo do Zênite Ø1,20 (vidro laminado)", 12, anchor="end")
    sh.leader(p1["y"] + 0.05, p1["mast_top"], 2.6, 5.5, "Coroa de 3 braços + capitel usinado", 12, anchor="end")
    sh.leader(p1["y"], 3.5, 2.6, 4.6, "Mastro M1 Ø139,7 x 4,5 embutido na parede da cabeceira", 12, anchor="end")
    sh.leader(-2.2, Z.roof_z(xc, -2.2), -3.4, 4.8, "Membrana PVDF · pré-tensão 2,5 kN/m", 12, anchor="start")
    sh.leader(-1.5, Z.liner_z(xc, -1.5), -3.4, 4.1, "Forro isolado: lã PET 50 mm + tecido", 12, anchor="start")
    sh.leader(-2.65, 2.82, -3.4, 3.4, "Anel de beiral 150 x 100 sobre pilares", 12, anchor="start")
    sh.leader(-2.65, 1.3, -3.4, 1.9, "Painel SIP 100 mm PIR + ripado externo", 12, anchor="start")
    sh.leader(y1, 1.0, 4.2, 1.7, "Poste Ø76 estaiado", 12, anchor="end")
    sh.leader(3.1, -0.12, 3.6, -1.4, "Passarela 0,80 m", 12, anchor="end")
    sh.leader(2.05, 1.1, 3.4, 2.7, "Passagem 1,10 m ao banho", 12, anchor="end")
    sh.dim(-2.7, -1.05, 2.7, -1.05, -0.35, label="5,40")
    sh.dim(y0, -1.05, y1, -1.05, -0.95, label="7,40 (cobertura)")
    sh.dim(-4.1, 0, -4.1, 5.8, -0.5, label="5,80")
    sh.dim(-4.1, 0, -4.1, 2.75, -1.1, label="2,75")
    sh.dim(4.3, -0.9, 4.3, 0, 0.5, label="0,90")
    sh.scalebar(5.8, -2.2, 4)
    sh.title_block("ZION ZENITH", "Corte transversal B-B", "1:45 (A1)", "07/27", "Mastro, coroa e óculo; envelope de membrana + forro isolado")
    return sh


def build():
    os.makedirs(OUT, exist_ok=True)
    planta(True).save(os.path.join(OUT, "02_planta_humanizada.svg"))
    planta(False).save(os.path.join(OUT, "03_planta_tecnica.svg"))
    elev_frontal().save(os.path.join(OUT, "04_elevacao_frontal.svg"))
    elev_lateral().save(os.path.join(OUT, "05_elevacao_lateral.svg"))
    corte_long().save(os.path.join(OUT, "06_corte_longitudinal.svg"))
    corte_transv().save(os.path.join(OUT, "07_corte_transversal.svg"))
    print("zenith drawings ok ->", OUT)

if __name__ == "__main__":
    build()

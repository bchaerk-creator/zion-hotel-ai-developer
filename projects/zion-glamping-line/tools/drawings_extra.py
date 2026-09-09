# -*- coding: utf-8 -*-
"""Desenhos complementares 2D (SVG): fachada traseira (04b) e planta estrutural (03b) do ZION COCOON e do ZION ZENITH.
Importa a geometria de geometry.py e o estilo de svgkit.py / drawings_*.py; nao altera esses modulos."""
import math, os
import numpy as np
from geometry import Cocoon, Zenith
from svgkit import *
from drawings_cocoon import arch_plan
from drawings_zenith import slats, roof_outline_pts, ground

C, Z = Cocoon(), Zenith()
OUTC = os.path.join(os.path.dirname(__file__), "..", "cocoon", "desenhos")
OUTZ = os.path.join(os.path.dirname(__file__), "..", "zenith", "desenhos")

# ------------------------------------------------------------------ malhas de estacas / vigas (compartilhadas com exploded.py)
C_PX = [-3.3, -1.1, 0.9, 2.1, 3.3, 4.5, 5.7, 6.9, 8.1, 9.0]
C_PY = [-2.6, -1.3, 0.0, 1.3, 2.6]
Z_PX = [-2.6, -0.2, 2.2, 4.6, 7.0, 9.4]
Z_PY = [-2.6, -1.3, 0.0, 1.3, 2.6]

def cocoon_pile_grid():
    """estacas do Cocoon: malha 1,20 x 1,30 m recortada pelo deck e pelo contorno do piso."""
    pts = []
    for px in C_PX:
        for py in C_PY:
            if px < 0.9 and abs(py) > 2.9: continue
            if px >= 0.9 and not (abs(py) <= C.floor_hw(px) - 0.1 or abs(py) < 1e-9): continue
            pts.append((px, py))
    return pts

def cocoon_floor_x_end(py):
    """x final da viga longitudinal em y = py (recorte pelo contorno do piso)."""
    if abs(py) < 1e-9: return C.X_FLOOR_END
    ok = [x for x in np.linspace(C.X_GLASS, C.X_FLOOR_END, 400) if C.floor_hw(x) >= abs(py) + 0.05]
    return float(max(ok)) if ok else C.X_GLASS

def cocoon_girders():
    """segmentos (x1,y1,x2,y2) do quadro do piso: longitudinais, transversais e bordas do deck."""
    D = C.DECK
    longi = [(D["x1"], py, cocoon_floor_x_end(py), py) for py in C_PY]
    trans = []
    for px in C_PX:
        hw = (D["y2"] if px < 0.9 else C.floor_hw(px))
        trans.append((px, -hw, px, hw))
    rim = [(D["x1"], D["y1"], D["x1"], D["y2"]), (D["x1"], D["y1"], D["x2"], D["y1"]), (D["x1"], D["y2"], D["x2"], D["y2"])]
    return longi, trans, rim

def zenith_pile_grid():
    return [(px, py) for px in Z_PX for py in Z_PY]

def zenith_tension_piles():
    """estacas de tracao: uma sob cada um dos 7 postes externos."""
    return list(Z.posts())

def zenith_stay_anchors():
    """chumbadores dos estais: 1,0 m para fora de cada poste, na direcao da inclinacao."""
    out = []
    for (px, py) in Z.posts():
        dx = -1.0 if px < 0 else (1.0 if px > 9 else 0.0)
        dy = -1.0 if py < 0 else (1.0 if py > 0 else 0.0)
        out.append((px + dx, py + dy))
    return out

def zenith_girders():
    D, Wk = Z.DECK, Z.WALK
    longi = [(D["x1"], py, Z.L, py) for py in Z_PY]
    trans = []
    for px in Z_PX:
        if px < 0: trans.append((px, D["y1"], px, D["y2"]))
        else: trans.append((px, -2.7, px, Wk["y2"]))
    rim = [(D["x1"], D["y1"], D["x1"], D["y2"]), (D["x1"], D["y1"], 0.0, D["y1"]), (D["x1"], D["y2"], 0.0, D["y2"]),
           (0.0, -2.7, Z.L, -2.7), (0.0, Wk["y2"], Z.L, Wk["y2"]), (Z.L, -2.7, Z.L, Wk["y2"]), (0.0, D["y1"], 0.0, Wk["y2"])]
    return longi, trans, rim

# ------------------------------------------------------------------ utilitarios de desenho
def dline(sh, x1, y1, x2, y2, w=0.06, color=STEEL, sw=0.8):
    """viga em planta: duas linhas paralelas (perfil U 150 x 60 visto de cima) com fechamento nas pontas."""
    if abs(y2 - y1) < 1e-9:
        sh.line(x1, y1 - w / 2, x2, y1 - w / 2, color, sw); sh.line(x1, y1 + w / 2, x2, y1 + w / 2, color, sw)
        sh.line(x1, y1 - w / 2, x1, y1 + w / 2, color, sw); sh.line(x2, y1 - w / 2, x2, y1 + w / 2, color, sw)
    else:
        sh.line(x1 - w / 2, y1, x1 - w / 2, y2, color, sw); sh.line(x1 + w / 2, y1, x1 + w / 2, y2, color, sw)
        sh.line(x1 - w / 2, y1, x1 + w / 2, y1, color, sw); sh.line(x1 - w / 2, y2, x1 + w / 2, y2, color, sw)

def pile_symbol(sh, px, py, code=None, size=7.5, r=4):
    sh.add(f'<g transform="translate({sh.X(px):.1f},{sh.Y(py):.1f})"><circle r="{r}" fill="{CREAM}" stroke="{STEEL}" stroke-width="0.9"/>'
           f'<line x1="-{r}" y1="0" x2="{r}" y2="0" stroke="{STEEL}" stroke-width="0.7"/><line x1="0" y1="-{r}" x2="0" y2="{r}" stroke="{STEEL}" stroke-width="0.7"/></g>')
    if code:
        sh.text_px(sh.X(px) + r + 2, sh.Y(py) - r + 1, code, size=size, fill=EARTH, anchor="start")

def code_tag(sh, x, y, code, size=9, color=GREEN, anchor="middle", dy=0):
    """etiqueta de codigo estrutural (caixa pequena)."""
    X, Y = sh.X(x), sh.Y(y) + dy
    w = 7 + 5.6 * len(code)
    X0 = X - w / 2 if anchor == "middle" else (X if anchor == "start" else X - w)
    sh.add(f'<rect x="{X0:.1f}" y="{Y - 7:.1f}" width="{w:.1f}" height="13" rx="1.5" fill="{CREAM}" stroke="{color}" stroke-width="0.6"/>')
    sh.text_px(X0 + w / 2, Y + 3.2, code, size=size, weight=700, fill=color, spacing=0.04)

def arrow2(sh, x1, y1, x2, y2, label="", color=EARTH, size=9):
    """seta de duas pontas (direcao das vigotas)."""
    sh.line(x1, y1, x2, y2, color, 0.8)
    for (xa, ya, xb, yb) in [(x1, y1, x2, y2), (x2, y2, x1, y1)]:
        ang = math.atan2(sh.Y(yb) - sh.Y(ya), sh.X(xb) - sh.X(xa))
        X, Y = sh.X(xa), sh.Y(ya)
        p1 = (X + 8 * math.cos(ang + 0.4), Y + 8 * math.sin(ang + 0.4)); p2 = (X + 8 * math.cos(ang - 0.4), Y + 8 * math.sin(ang - 0.4))
        sh.add(f'<polygon points="{X:.1f},{Y:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{color}"/>')
    if label:
        sh.text((x1 + x2) / 2, (y1 + y2) / 2, label, size, color, dy=-5)

def code_legend(sh, X, Y, items, size=9.5, pitch=21, wrap=None):
    """legenda de codigos: [(codigo, descricao)]"""
    for i, (code, desc) in enumerate(items):
        y = Y + i * pitch
        w = 7 + 5.6 * len(code)
        sh.add(f'<rect x="{X}" y="{y - 9}" width="{w:.1f}" height="13" rx="1.5" fill="{CREAM}" stroke="{GREEN}" stroke-width="0.6"/>')
        sh.text_px(X + w / 2, y + 1.2, code, size=9, weight=700, spacing=0.04)
        sh.text_px(X + 62, y + 1.2, desc, size=size, anchor="start")

# ==================================================================================
# COCOON: fachada traseira
# ==================================================================================
def cocoon_fachada_traseira():
    sh = Sheet(1600, 1000, scale=100, ox=800, oy=720, flip_x=False)
    sh.header("Zion Cocoon · Fachada traseira", "Vista da cauda (olhar para -x, +y a direita) · largura 6,00 m · altura 4,20 m · a cauda fecha em ponta a 1,10 m")
    # solo, estacas e quadro do piso
    sh.rect(-6.8, -0.6, 6.8, -0.02, fill=sh.pattern("soil"), stroke="none")
    sh.line(-6.8, -0.02, 6.8, -0.02, GREEN, 1.0)
    for py in C_PY:
        sh.rect(py - 0.04, -0.6, py + 0.04, -0.2, fill=STEEL, stroke="none")
    sh.rect(-3.25, -0.2, 3.25, -0.05, fill=WOOD2, stroke=GREEN, sw=0.9)
    sh.rect(-3.25, -0.05, 3.25, 0.0, fill=GREEN, stroke="none")
    # silhueta maxima (secao em x = 3,40)
    sil = C.section_local(C.XMAX, 120)
    sh.poly(sil, fill=MEMB, stroke=GREEN, sw=1.8)
    # cauda: secoes em x = 8,75 (arco A7), 9,30 (quadro da cauda) e 9,50; ponta em z = 1,10
    for x, k, col, swv in [(8.75, 0.965, EARTH, 1.0), (9.3, 0.935, EARTH, 0.9), (9.5, 0.905, EARTH, 0.8)]:
        pts = C.section_local(x, 100)
        sh.poly(pts, fill=shade(MEMB, k), stroke=col, sw=swv)
    tip = C.section_local(9.58, 60)
    sh.poly(tip, fill=shade(MEMB, 0.88), stroke=GREEN, sw=0.8)
    sh.circle_px(0.0, C.top(C.L), 3, fill=GREEN, stroke=GREEN)
    # linha do piso (base da concha)
    hw = C.floor_hw(C.XMAX)
    sh.line(-hw, 0.0, hw, 0.0, GREEN, 1.2)
    # janelas olho do banho (indices 2 e 5), em escorco
    for idx in (2, 5):
        w = C.WINDOWS[idx]
        frame = [(y, z) for (x, y, z) in C.window_outline(dict(w, lx=w["lx"] + 0.11, lt=w["lt"] + 0.03), 48)]
        pts = [(y, z) for (x, y, z) in C.window_outline(w, 48)]
        sh.poly(frame, fill=WOOD2, stroke=GREEN, sw=0.7)
        sh.poly(pts, fill=GLASS, stroke=GREEN, sw=0.8)
    # condensadora com painel ripado (x 9,95 a 10,70)
    sh.rect(-0.45, 0.0, 0.35, 0.62, fill="#E5E1D8", stroke=GREEN, sw=0.8)
    sh.rect(-0.55, 0.0, 0.45, 1.3, fill="none", stroke=GREEN, sw=0.8)
    slats(sh, -0.52, 0.45, 0.0, 1.3, 0.08)
    sh.line(-0.55, 1.3, 0.45, 1.3, GREEN, 1.0)
    # rotulos: textos sempre para fora do desenho
    L = -3.7; R = 5.4
    sh.leader(-2.75, 2.6, L, 3.5, "Membrana PVDF 1050 g/m² (silhueta maxima em x 3,40)", 12, anchor="end")
    sh.leader(-1.95, 2.3, L, 2.85, "Arco A7 Ø88,9 x 3,6 (x 8,75)", 12, anchor="end")
    sh.leader(-1.2, 1.75, L, 2.25, "Quadro da cauda Ø60,3 + 3 barras (x 9,30)", 12, anchor="end")
    sh.leader(-2.0, 1.4, L, 1.65, "Olho da banheira 0,90 x 0,50 (lateral, em escorco)", 12, anchor="end")
    sh.leader(-2.6, 0.5, L, 0.95, "Tubo de queda Ø75 na extremidade da calha oculta", 12, anchor="end")
    sh.leader(-2.9, 0.15, L, 0.35, "Trilho de base 100 x 50 + calha oculta 80 mm", 12, anchor="end")
    sh.leader(0.0, 1.1, R, 3.5, "Ponta da cauda a 1,10 m", 12, anchor="start")
    sh.leader(2.25, 1.95, R, 2.85, "Olho do banho 1,10 x 0,60 (escorco)", 12, anchor="start")
    sh.leader(0.3, 0.9, R, 2.25, "Painel ripado 40 x 40 da condensadora", 12, anchor="start")
    sh.leader(-0.05, 0.4, R, 1.65, "Condensadora 12k BTU oculta", 12, anchor="start")
    sh.leader(2.6, -0.12, R, 0.95, "Quadro do piso U 150 x 60", 12, anchor="start")
    sh.leader(2.6, -0.45, R, 0.35, "Estacas helicoidais Ø76", 12, anchor="start")
    # cotas
    sh.dim(-3.0, -0.9, 3.0, -0.9, -0.35, label="6,00")
    sh.dim(-C.floor_hw(8.75), -0.9, C.floor_hw(8.75), -0.9, -0.9, label=fmt(2 * C.floor_hw(8.75)) + " (base do arco A7)")
    sh.dim(-3.25, -0.9, 3.25, -0.9, -1.45, label="6,50 (deck)")
    sh.dim(3.7, 0, 3.7, 4.2, 0.4, label="4,20")
    sh.dim(3.7, 0, 3.7, C.top(8.75), 0.9, label=fmt(C.top(8.75)) + " (A7)")
    sh.dim(3.7, 0, 3.7, 1.1, 1.4, label="1,10 (ponta)")
    sh.dim(-3.7, -0.6, -3.7, 0, -0.4, label="0,60")
    sh.scalebar(-7.0, -2.0, 4)
    sh.title_block("ZION COCOON", "Fachada traseira", "1:50 (A1)", "04b/27", "Cauda afilada: arco A7, quadro da cauda, olhos do banho, condensadora oculta")
    return sh

# ==================================================================================
# ZENITH: fachada traseira
# ==================================================================================
def zenith_fachada_traseira():
    sh = Sheet(1600, 1000, scale=84, ox=800, oy=740, flip_x=False)
    sh.header("Zion Zenith · Fachada traseira", "Vista dos fundos (olhar para -x, +y a direita) · painel ripado com a fresta da banheira · cobertura 7,40 m · cume 5,80 m")
    ground(sh, -7.5, 7.5)
    for py in Z_PY:
        sh.rect(py - 0.04, -0.6, py + 0.04, -0.2, fill=STEEL, stroke="none")
    for (px, py) in zenith_tension_piles():
        if px > 10: sh.rect(py - 0.04, -0.6, py + 0.04, -0.02, fill=STEEL, stroke="none", opacity=0.6)
    for (px, py) in zenith_stay_anchors():
        if px > 10 and abs(py) > 1: sh.rect(py - 0.03, -0.45, py + 0.03, -0.02, fill=EARTH, stroke="none", opacity=0.8)
    sh.rect(-3.4, -0.2, 3.5, -0.05, fill=WOOD2, stroke=GREEN, sw=0.9); sh.rect(-3.4, -0.05, 3.5, 0.0, fill=GREEN, stroke="none")
    # cobertura: silhueta + borda dos fundos (2 catenarias entre 3 postes)
    x0, x1, y0, y1 = Z.roof_bounds()
    sil = Z.silhouette_front(120)
    rear_edge = [(y, Z.edge_height(x1, y)) for y in np.linspace(y0, y1, 81)]
    sh.poly(sil + rear_edge[::-1], fill=MEMB, stroke=GREEN, sw=1.8)
    # corpo: painel ripado dos fundos com a fresta da banheira
    sh.rect(-2.7, 0, 2.7, 2.75, fill="#C9B08C", stroke=GREEN, sw=1.2)
    slats(sh, -2.66, 2.7, 0, 2.75)
    sh.rect(-0.8, 1.5, 1.6, 2.15, fill=GLASS, stroke=GREEN, sw=0.9)
    sh.rect(-2.7, 2.75, 2.7, 2.9, fill=STEEL, stroke=GREEN, sw=0.6)
    # postes dos fundos (3): cantos inclinados 8 graus, central vertical
    for py in (y0, 0.0, y1):
        top = Z.edge_height(x1, py)
        lean = 0.08 * (1 if py > 0 else (-1 if py < 0 else 0))
        sh.line(py, -0.05, py + lean * top / 0.9, top, STEEL, 4)
        if abs(py) > 1: sh.line(py + lean * top / 0.9, top, py + lean * 12, -0.02, EARTH, 0.9, dash="5 3")
    # mastros (tracejado, atras)
    for p in Z.PEAKS:
        sh.line(p["y"], 0, p["y"], p["mast_top"], STEEL, 1.0, dash="6 4", opacity=0.6)
        sh.circle(p["y"], p["h"], 0.08, fill="none", stroke=GREEN, sw=0.8)
    # condensadora (y -2,2 a -1,4) atras do ripado
    sh.rect(-2.2, 0.0, -1.4, 0.62, fill="#E5E1D8", stroke=GREEN, sw=0.8)
    sh.rect(-2.3, 0.0, -1.3, 1.3, fill="none", stroke=GREEN, sw=0.8)
    slats(sh, -2.27, -1.3, 0.0, 1.3, 0.1)
    # rotulos: textos para fora
    L = -5.5; R = 5.5
    sh.leader(0.4, 5.8, 1.9, 6.45, "Cume principal 5,80 m: Oculo do Zenite Ø1,20 (x 6,30; y +0,40)", 12, anchor="start")
    sh.leader(1.6, 4.6, 3.2, 5.45, "Cume secundario 4,60 m: chamine do Respiro (x 1,60; y +1,60)", 12, anchor="start")
    sh.leader(-3.0, 3.35, L, 4.3, "Membrana PVDF em balanco 1,00 m nos fundos", 12, anchor="end")
    sh.leader(-1.85, 2.37, L, 3.55, "Borda em catenaria, flecha 0,28 m, cabo Ø12 inox", 12, anchor="end")
    sh.leader(-2.1, 2.82, L, 2.9, "Anel de beiral 150 x 100 a 2,90 m", 12, anchor="end")
    sh.leader(-2.0, 1.0, L, 2.2, "Painel SIP 100 mm + ripado termotratado 40 x 40", 12, anchor="end")
    sh.leader(-1.8, 0.45, L, 1.4, "Condensadora 18k BTU atras do ripado", 12, anchor="end")
    sh.leader(-3.2, -0.12, L, 0.6, "Terraco frontal (atras) sobre vigas U 150", 12, anchor="end")
    sh.leader(-3.7, -0.5, L, -0.9, "Estaca de tracao sob o poste", 12, anchor="end")
    sh.leader(4.66, -0.3, R, -0.9, "Chumbador do estai Ø10 inox", 12, anchor="start")
    sh.leader(0.4, 1.83, R, 3.55, "Fresta da banheira 2,40 x 0,65 (vidro fixo)", 12, anchor="start")
    sh.leader(0.0, 1.4, R, 2.9, "Poste central dos fundos Ø76,1 (vertical)", 12, anchor="start")
    sh.leader(3.75, 1.3, R, 2.2, "Poste de canto Ø76,1 inclinado 8°, estaiado", 12, anchor="start")
    sh.leader(2.2, 0.7, R, 1.4, "Ripado 40 x 40 termotratado, junta 40 mm", 12, anchor="start")
    sh.leader(3.1, -0.12, R, 0.6, "Passarela lateral 0,80 m", 12, anchor="start")
    # cotas
    sh.dim(-2.7, -0.9, 2.7, -0.9, -0.35, label="5,40 (corpo)")
    sh.dim(y0, -0.9, y1, -0.9, -0.95, label="7,40 (cobertura)")
    sh.dim(-3.4, -0.9, 3.5, -0.9, -1.55, label="6,90 (terraco + passarela)")
    sh.dim(-4.3, 0, -4.3, 5.8, -0.45, label="5,80")
    sh.dim(-4.3, 0, -4.3, 2.75, -0.95, label="2,75")
    sh.dim(4.3, 0, 4.3, 4.6, 0.45, label="4,60")
    sh.dim(4.3, 0, 4.3, 2.65, 0.95, label="2,65 (postes)")
    sh.scalebar(-7.6, -2.3, 4)
    sh.title_block("ZION ZENITH", "Fachada traseira", "1:50 (A1)", "04b/27", "Painel ripado, fresta da banheira, tres postes e borda em catenaria")
    return sh

# ==================================================================================
# COCOON: planta estrutural
# ==================================================================================
def cocoon_planta_estrutural():
    sh = Sheet(1600, 1000, scale=72, ox=440, oy=520)
    sh.header("Zion Cocoon · Planta estrutural", "Fundacoes, quadro do piso, trilhos de base, arcos e travamentos · codigos conforme a lista de materiais")
    D = C.DECK
    # contornos de referencia
    sh.rect(D["x1"], D["y1"], D["x2"], D["y2"], fill="none", stroke=GREEN, sw=0.9)
    sh.poly(C.shell_plan_outline(120), fill="none", stroke=EARTH, sw=0.7, dash="8 4", opacity=0.7)
    sh.poly(C.floor_outline(120), fill="none", stroke=GREEN, sw=0.8)
    # vigas do quadro do piso (A01 longitudinais, A02 transversais, A05 bordas do deck)
    longi, trans, rim = cocoon_girders()
    for (x1, y1, x2, y2) in longi + trans + rim:
        dline(sh, x1, y1, x2, y2)
    # trilhos de base curvos A03 (esq., +y) e A04 (dir., -y)
    xs = np.linspace(C.X_GLASS, 9.35, 80)
    sh.poly([(x, C.floor_hw(x) - 0.03) for x in xs], close=False, stroke=STEEL, sw=2.4)
    sh.poly([(x, -C.floor_hw(x) + 0.03) for x in xs], close=False, stroke=STEEL, sw=2.4)
    # arcos B00..B07 (projecao) e chapas de base D01
    for i, x in enumerate(C.ARCH_X):
        pts = arch_plan(x)
        sh.poly(pts, close=False, stroke=GREEN if i else STEEL, sw=0.9, dash="6 4", opacity=0.85)
        hw = C.floor_hw(x)
        for s in (-1, 1):
            sh.rect(x - 0.1, s * hw - 0.075, x + 0.1, s * hw + 0.075, fill=STEEL, stroke=GREEN, sw=0.4)
        code_tag(sh, pts[-1][0], pts[-1][1] - 0.32, f"B0{i}", size=8)
    # quadro da cauda (x 9,30)
    sh.poly(arch_plan(9.3), close=False, stroke=STEEL, sw=1.2, dash="3 3")
    # tercas C01 (7 linhas)
    for pl in C.purlins(40):
        sh.poly([(x, y) for (x, y, z) in pl], close=False, stroke=EARTH, sw=0.6, dash="3 3", opacity=0.9)
    # espinha C02
    x1, x2, ht = C.SPINE
    hws = ht * C.B_MAX
    sh.poly([(C.shear(x1, 4.15), -hws), (C.shear(x2, 4.15), -hws), (C.shear(x2, 4.15), hws), (C.shear(x1, 4.15), hws)], fill="none", stroke=GREEN, sw=0.9, dash="3 3")
    for xx in np.linspace(x1, x2, 9)[1:-1]:
        sh.line(C.shear(xx, 4.15), -hws, C.shear(xx, 4.15), hws, GREEN, 0.5, opacity=0.6)
    # cabos em X C03 (vaos B00-B01 e B05-B06)
    for (xa, xb) in [(0.45, 1.65), (6.45, 7.65)]:
        for th in (0.35, math.pi - 0.35):
            pa = C.section_point(xa, th); pb = C.section_point(xb, th + 0.5); pc = C.section_point(xa, th + 0.5); pd = C.section_point(xb, th)
            sh.line(pa[0], pa[1], pb[0], pb[1], EARTH, 0.9, dash="2 2"); sh.line(pc[0], pc[1], pd[0], pd[1], EARTH, 0.9, dash="2 2")
    # estacas F01..Fnn
    piles = cocoon_pile_grid()
    for i, (px, py) in enumerate(piles):
        pile_symbol(sh, px, py, f"F{i + 1:02d}")
    # etiquetas de codigos
    code_tag(sh, -3.55, 2.6, "A01", size=8, anchor="start", dy=-12)
    code_tag(sh, -3.55, 0.0, "A01", size=8, anchor="start", dy=-12)
    code_tag(sh, -1.1, 3.25, "A02", size=8, dy=-12)
    code_tag(sh, 5.7, 2.9, "A02", size=8, dy=-12)
    code_tag(sh, 4.5, 3.05, "A03", size=8, dy=-10)
    code_tag(sh, 4.5, -3.05, "A04", size=8, dy=12)
    code_tag(sh, -2.2, -3.25, "A05", size=8, dy=12)
    code_tag(sh, 2.85, 2.95, "D01", size=8, anchor="start", dy=-16)
    code_tag(sh, 8.4, -1.05, "C01", size=8, anchor="start")
    code_tag(sh, 2.35, 0.62, "C02", size=8)
    code_tag(sh, 7.05, 2.35, "C03", size=8)
    code_tag(sh, 1.05, -2.35, "C03", size=8)
    code_tag(sh, 9.3, 1.75, "E01", size=8, anchor="start", dy=-8)
    # direcao das vigotas
    arrow2(sh, -3.5, 1.9, -1.5, 1.9, "vigotas 50 x 150 c/ 400", EARTH)
    arrow2(sh, 2.2, -0.65, 4.4, -0.65, "vigotas 50 x 150 c/ 400", EARTH)
    # marcas de corte
    sh.line(5.0, -3.4, 5.0, 3.4, GREEN, 1.4, dash="10 4")
    sh.text(5.0, 3.6, "B", 12, weight=700); sh.text(5.0, -3.75, "B", 12, weight=700)
    sh.line(-4.0, 0.0, 10.3, 0.0, GREEN, 1.4, dash="10 4")
    sh.text(-4.25, 0.0, "A", 12, weight=700, dy=4); sh.text(10.5, 0.0, "A", 12, weight=700, dy=4)
    # cotas: eixos das estacas
    sh.dim_chain(C_PX, -3.55, -0.5, size=10)
    sh.dim(-3.7, -3.55, 9.6, -3.55, -1.15, label="13,30 (deck + concha)")
    sh.dim_chain(C_PY, -4.0, -0.4, vertical=True, size=10)
    sh.dim(-4.0, -3.25, -4.0, 3.25, -0.95, label="6,50 (deck)")
    sh.dim(10.3, -3.0, 10.3, 3.0, 0.5, label="6,00")
    # legenda de codigos
    sh.north(1520, 120, angle=-90)
    sh.text_px(1290, 205, "CODIGOS ESTRUTURAIS", size=10, weight=700, spacing=0.2, anchor="start")
    items = [(f"F01-F{len(piles):02d}", "Estaca helicoidal Ø76 / helice Ø300, L 1,5 a 2,5 m"),
             ("A01", "Vigas longitudinais U 150 x 60 x 3,0 galv. (5 linhas)"),
             ("A02", "Vigas transversais U 150 x 60 x 3,0 galv. (10 linhas)"),
             ("A03/A04", "Trilhos de base 100 x 50 x 3,0 curvados (esq. / dir.)"),
             ("A05", "Vigas de borda do deck U 150 x 60 x 3,0"),
             ("B00", "Anel do labio Ø101,6 x 4,0 inclinado 8°"),
             ("B01-B07", "Arcos elipticos Ø88,9 x 3,6 em 3 segmentos"),
             ("C01", "7 tercas longitudinais Ø48,3 x 3,0"),
             ("C02", "Espinha de Luz: trelica plana 300 mm"),
             ("C03", "Cabos em X Ø8 inox nos vaos B00-B01 e B05-B06"),
             ("D01", f"Chapa de base 200 x 150 x 10 + 4 M16 ({2 * len(C.ARCH_X)} un.)"),
             ("E01", "Quadro da cauda Ø60,3 x 3,0 + 3 barras")]
    code_legend(sh, 1290, 232, items, size=9.0, pitch=21)
    sh.text_px(1290, 495, f"Malha de estacas 1,20 x 1,30 m · {len(piles)} estacas sob o deck e o piso", size=9, fill=EARTH, anchor="start")
    sh.text_px(1290, 511, "Arcos: pes engastados nos trilhos A03/A04 via D01", size=9, fill=EARTH, anchor="start")
    sh.scalebar(-3.7, -5.55, 5)
    sh.title_block("ZION COCOON", "Planta estrutural", "1:50 (A1) · cotas em metros", "03b/27",
                   "Estacas, quadro do piso U 150, trilhos curvos, 8 arcos, tercas e cabos")
    return sh

# ==================================================================================
# ZENITH: planta estrutural
# ==================================================================================
def zenith_planta_estrutural():
    sh = Sheet(1600, 1000, scale=76, ox=400, oy=480)
    sh.header("Zion Zenith · Planta estrutural", "Fundacoes, quadro do piso, pilares, anel de beiral, mastros, postes e estais · codigos conforme a lista de materiais")
    D, Wk = Z.DECK, Z.WALK
    x0, x1, y0, y1 = Z.roof_bounds()
    # contornos de referencia
    sh.rect(D["x1"], D["y1"], D["x2"], D["y2"], fill="none", stroke=GREEN, sw=0.9)
    sh.rect(Wk["x1"], Wk["y1"], Wk["x2"], Wk["y2"], fill="none", stroke=GREEN, sw=0.9)
    H = Z.HOTTUB
    sh.circle(H["x"], H["y"], H["r"], fill="none", stroke=GREEN, sw=0.6, dash="4 3", opacity=0.7)
    sh.poly(roof_outline_pts(), fill="none", stroke=GREEN, sw=1.0, dash="10 5")
    # cabo de borda (bolsa 80 mm para dentro)
    sh.rect(x0 + 0.08, y0 + 0.08, x1 - 0.08, y1 - 0.08, fill="none", stroke=EARTH, sw=1.1)
    # paredes SIP (linha do corpo)
    sh.rect(0.0, -2.7, 9.5, 2.7, fill="none", stroke=GREEN, sw=0.8)
    sh.rect(6.2, -2.6, 6.45, 1.5, fill=sh.pattern("hatch"), stroke=GREEN, sw=0.8)
    # vigas do quadro do piso
    longi, trans, rim = zenith_girders()
    for (xa, ya, xb, yb) in longi + trans + rim:
        dline(sh, xa, ya, xb, yb)
    # anel de beiral VB01..VB08 (150 x 100 em planta = 0,10 de largura)
    segs = [((0.0, 3.2), -2.7, "VB01"), ((3.2, 6.4), -2.7, "VB02"), ((6.4, 9.5), -2.7, "VB03"),
            ((0.0, 3.2), 2.7, "VB04"), ((3.2, 6.4), 2.7, "VB05"), ((6.4, 9.5), 2.7, "VB06")]
    for (xa, xb), yy, code in segs:
        sh.rect(xa, yy - 0.05, xb, yy + 0.05, fill="#B9B7B0", stroke=GREEN, sw=0.7)
        code_tag(sh, (xa + xb) / 2, yy, code, size=8, dy=(14 if yy < 0 else -14))
    for xx, code in [(0.0, "VB07"), (9.5, "VB08")]:
        sh.rect(xx - 0.05, -2.75, xx + 0.05, 2.75, fill="#B9B7B0", stroke=GREEN, sw=0.7)
        code_tag(sh, xx, -1.9, code, size=8, anchor=("start" if xx < 1 else "end"), dy=0)
    for xx in (3.2, 6.4):
        for yy in (-2.7, 2.7):
            sh.line(xx, yy - 0.12, xx, yy + 0.12, GREEN, 1.4)   # emenda parafusada
    # pilares P01..P10
    for i, (cx, cy) in enumerate(Z.columns()):
        sh.circle(cx, cy, 0.06, fill=STEEL, stroke="none")
        sh.circle(cx, cy, 0.14, fill="none", stroke=STEEL, sw=0.6)
        dxl = 0.2 if cx < 5 else -0.2
        code_tag(sh, cx + dxl, cy + (0.33 if cy >= 0 else -0.33), f"P{i + 1:02d}", size=8)
    # mastros M1 / M2 com chapas de base e coroas
    for p, code, b in [(Z.PEAKS[0], "M1", 0.25), (Z.PEAKS[1], "M2", 0.2)]:
        sh.rect(p["x"] - b / 2, p["y"] - b / 2, p["x"] + b / 2, p["y"] + b / 2, fill="none", stroke=STEEL, sw=1.0)
        sh.circle(p["x"], p["y"], 0.07, fill=STEEL, stroke="none")
        sh.circle(p["x"], p["y"], p["r"], fill="none", stroke=GREEN, sw=1.0, dash="5 3")
        for k in range(3):
            ang = math.pi / 2 + 2 * math.pi * k / 3
            sh.line(p["x"], p["y"], p["x"] + p["r"] * math.cos(ang), p["y"] + p["r"] * math.sin(ang), STEEL, 0.9)
        code_tag(sh, p["x"] + p["r"] + 0.15, p["y"] + 0.4, code, size=8, anchor="start")
    # estacas: malha F01..F30 e estacas de tracao FT01..FT07
    grid = zenith_pile_grid()
    for i, (px, py) in enumerate(grid):
        pile_symbol(sh, px, py, f"F{i + 1:02d}")
    tens = zenith_tension_piles(); anchors = zenith_stay_anchors()
    # postes PE01..PE07 sobre estacas de tracao FT, estais ate chumbadores EA (1,0 m para fora)
    for i, ((px, py), (tx, ty)) in enumerate(zip(tens, anchors)):
        sh.line(px, py, tx, ty, EARTH, 0.9, dash="4 3")
        pile_symbol(sh, px, py, None, r=6)
        sh.circle(px, py, 0.2, fill="none", stroke=STEEL, sw=1.0)
        sh.text_px(sh.X(px) + 9, sh.Y(py) - 8, f"FT{i + 1:02d}", size=7.5, fill=EARTH, anchor="start")
        ax_, ay_ = sh.X(tx), sh.Y(ty)
        sh.add(f'<polygon points="{ax_:.1f},{ay_ - 5:.1f} {ax_ - 4.5:.1f},{ay_ + 3:.1f} {ax_ + 4.5:.1f},{ay_ + 3:.1f}" fill="{EARTH}"/>')
        oy_ = 0.45 if py > 0 else -0.45
        code_tag(sh, px, py + oy_, f"PE{i + 1:02d}", size=8)
    # etiquetas de vigas
    code_tag(sh, -2.9, 2.6, "A01", size=8, anchor="start", dy=-12)
    code_tag(sh, -2.9, 0.0, "A01", size=8, anchor="start", dy=-12)
    code_tag(sh, 2.2, 3.5, "A02", size=8, dy=-12)
    code_tag(sh, -0.2, 3.4, "A02", size=8, dy=-12)
    code_tag(sh, -1.5, -3.4, "A03", size=8, dy=12)
    code_tag(sh, 8.4, 3.5, "A03", size=8, dy=-12)
    code_tag(sh, 8.0, 2.0, "W01", size=8, anchor="start")
    code_tag(sh, x1 - 0.5, y0 + 0.08, "CB01", size=8, anchor="end", dy=12)
    arrow2(sh, -2.5, 1.9, -0.3, 1.9, "vigotas 50 x 150 c/ 400", EARTH)
    arrow2(sh, 2.35, -0.65, 4.45, -0.65, "vigotas 50 x 150 c/ 400", EARTH)
    # marcas de corte
    sh.line(6.3, -4.2, 6.3, 4.3, GREEN, 1.4, dash="10 4")
    sh.text(6.3, 4.5, "B", 12, weight=700); sh.text(6.3, -4.55, "B", 12, weight=700)
    sh.line(-4.0, 0.4, 11.2, 0.4, GREEN, 1.4, dash="10 4")
    sh.text(-4.25, 0.4, "A", 12, weight=700, dy=4); sh.text(11.45, 0.4, "A", 12, weight=700, dy=4)
    # cotas
    sh.dim_chain(Z_PX, -3.9, -0.4, size=10)
    sh.dim(x0, -3.9, x1, -3.9, -1.2, label="12,90 (cobertura)")
    sh.dim_chain(Z_PY, -3.9, -0.3, vertical=True, size=10)
    sh.dim(-3.9, -3.4, -3.9, 3.4, -0.8, label="6,80 (terraco)")
    sh.dim(11.6, -2.7, 11.6, 2.7, 0.4, label="5,40")
    sh.dim(11.6, y0, 11.6, y1, 0.9, label="7,40 (cobertura)")
    # legenda
    sh.north(1520, 120, angle=-90)
    sh.text_px(1362, 205, "CODIGOS ESTRUTURAIS", size=10, weight=700, spacing=0.2, anchor="start")
    items = [(f"F01-F{len(grid)}", "Estaca helicoidal Ø76 (piso)"),
             ("FT01-FT07", "Estaca de tracao sob cada poste"),
             ("EA", "Chumbador do estai, 1,0 m fora do poste"),
             ("A01", "Vigas longitudinais U 150x60x3"),
             ("A02", "Vigas transversais U 150x60x3"),
             ("A03", "Vigas de borda U 150x60x3"),
             ("P01-P10", "Pilares Ø101,6x4,0 h 2,90"),
             ("VB01-VB08", "Anel de beiral 150x100x4,0"),
             ("M1", "Mastro Ø139,7x4,5 + anel Ø1,20"),
             ("M2", "Mastro Ø114,3x4,0 + anel Ø0,70"),
             ("PE01-PE07", "Postes Ø76,1x3,6 inclinados 8°"),
             ("CB01", "Cabo de borda Ø12 inox"),
             ("W01", "Paineis SIP 100 mm (diafragma)")]
    code_legend(sh, 1362, 232, items, size=8.4, pitch=21)
    sh.text_px(1362, 516, f"{len(grid)} estacas sob o piso + {len(tens)} de tracao", size=8.5, fill=EARTH, anchor="start")
    sh.text_px(1362, 532, "Estais Ø10 inox dos postes aos chumbadores EA", size=8.5, fill=EARTH, anchor="start")
    sh.scalebar(-3.0, -5.7, 5)
    sh.title_block("ZION ZENITH", "Planta estrutural", "1:50 (A1) · cotas em metros", "03b/27",
                   "Estacas, quadro U 150, 10 pilares, anel de beiral, 2 mastros, 7 postes estaiados")
    return sh


def build():
    os.makedirs(OUTC, exist_ok=True); os.makedirs(OUTZ, exist_ok=True)
    cocoon_fachada_traseira().save(os.path.join(OUTC, "04b_fachada_traseira.svg"))
    cocoon_planta_estrutural().save(os.path.join(OUTC, "03b_planta_estrutural.svg"))
    zenith_fachada_traseira().save(os.path.join(OUTZ, "04b_fachada_traseira.svg"))
    zenith_planta_estrutural().save(os.path.join(OUTZ, "03b_planta_estrutural.svg"))
    print("drawings_extra ok")

if __name__ == "__main__":
    build()

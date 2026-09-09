# -*- coding: utf-8 -*-
"""Isometricas explodidas (SVG) do ZION COCOON e do ZION ZENITH:
 - 10_modelo_explodido.svg: modelo explodido da estrutura (paisagem 1600 x 1000)
 - 13_camadas_construtivas.svg: as 13 camadas construtivas em pilha explodida (retrato 1200 x 2000)
Reutiliza geometry.py (geometria), svgkit.py (folha) e iso.py (cena com algoritmo do pintor)."""
import math, os
import numpy as np
from geometry import Cocoon, Zenith
from svgkit import *
from iso import Scene, add_furniture
from drawings_extra import (cocoon_pile_grid, cocoon_girders, zenith_pile_grid, zenith_tension_piles, zenith_stay_anchors, zenith_girders)

C, Z = Cocoon(), Zenith()
OUTC = os.path.join(os.path.dirname(__file__), "..", "cocoon", "desenhos")
OUTZ = os.path.join(os.path.dirname(__file__), "..", "zenith", "desenhos")
SAND2 = "#E2D5BE"; SILVER = "#C9C4B8"; BEIGE = "#EBDFCB"; COLD = "#4E6E8B"; HOT = "#B1543A"
FLOOR = "#C9AA7D"; FLOOR_LIGHT = "#F4ECE0"; STEEL_DARK = "#5A5B5A"; GLASS_ISO = "#9FB7C2"

# ------------------------------------------------------------------ utilidades
def mix(c1, c2, t):
    """mistura c1 com c2 (t = peso de c1). Usado para simular opacidade em linhas."""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{int(round(a[i] * t + b[i] * (1 - t))):02x}" for i in range(3))

def lift(pts, dz):
    return [(p[0], p[1], p[2] + dz) for p in pts]

def lift_items(items, dz):
    return [dict(f, z1=f["z1"] + dz, z2=f["z2"] + dz) for f in items]

def arrow3d(sc, pts, color, width=1.0):
    """seta em 3D (haste ao longo de pts, ponta no ultimo ponto), sempre por cima."""
    sc.polyline(pts, color, width, on_top=True)
    a, b = sc.proj(pts[-2]), sc.proj(pts[-1])
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for da in (0.55, -0.55):
        sc.lines.append((1e9, (b[0], b[1]), (b[0] - 7 * math.cos(ang + da), b[1] - 7 * math.sin(ang + da)), color, width, None))

def ground_plate(sc, x1, x2, y1, y2, z, color="#EFE5D8"):
    pts = [sc.proj(p) for p in [(x1, y1, z), (x2, y1, z), (x2, y2, z), (x1, y2, z)]]
    d = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
    sc.pre.append(f'<polygon points="{d}" fill="{color}" fill-opacity="0.8" stroke="{EARTH}" stroke-width="0.5" stroke-opacity="0.5"/>')

def fit(layers, box, smax):
    """escala e origem para que todas as camadas (caixas envolventes deslocadas) caibam no retangulo box (px)."""
    bx0, by0, bx1, by1 = box
    sx, sy = [], []
    for L in layers:
        x1, x2, y1, y2, z1, z2 = L["bb"]
        for x in (x1, x2):
            for y in (y1, y2):
                for z in (z1 + L["dz"], z2 + L["dz"]):
                    u, v, _ = iso_project((x, y, z), 1.0, 0, 0)
                    sx.append(u); sy.append(v)
    du, dv = max(sx) - min(sx), max(sy) - min(sy)
    s = min((bx1 - bx0) / du, (by1 - by0) / dv, smax)
    ox = bx0 + ((bx1 - bx0) - du * s) / 2 - min(sx) * s
    oy = by0 + ((by1 - by0) - dv * s) / 2 - min(sy) * s
    return s, ox, oy

# ------------------------------------------------------------------ malhas da concha (Cocoon)
_SHELL = {}
def shell_mesh(nu=40, nv=20):
    key = (nu, nv)
    if key not in _SHELL: _SHELL[key] = C.shell_mesh(nu, nv)
    return _SHELL[key]

SHELL_CENTER = (5.0, 0.0, 1.4)
def scale_pt(p, f, c=SHELL_CENTER):
    return (c[0] + f * (p[0] - c[0]), c[1] + f * (p[1] - c[1]), c[2] + f * (p[2] - c[2]))

def shell_scaled(f, nu=36, nv=18):
    m = shell_mesh(nu, nv)
    return [scale_pt(p, f) for p in m["vertices"]], m["membrane"] + m["glass"]

def shell_wire(f, nx=18, nl=9):
    lines = []
    for x in np.linspace(C.X_FRONT, C.L - 0.03, nx):
        lines.append([scale_pt(p, f) for p in C.section_curve(float(x), 32)])
    for v in np.linspace(0.0, 1.0, nl):
        pts = []
        for x in np.linspace(C.X_FRONT, C.L - 0.03, 48):
            t0, t1 = C.theta_range(float(x)); pts.append(C.section_point(float(x), t0 + (t1 - t0) * v))
        lines.append([scale_pt(p, f) for p in pts])
    return lines

def floor_tris(sc, dz, color, outline=True, n=40):
    fl = C.floor_outline(n)
    for i in range(1, len(fl) - 1):
        sc.tri((fl[0][0], fl[0][1], dz), (fl[i][0], fl[i][1], dz), (fl[i + 1][0], fl[i + 1][1], dz), color, shade_on=False)
    if outline: sc.polyline([(x, y, dz + 0.005) for (x, y) in fl] + [(fl[0][0], fl[0][1], dz + 0.005)], GREEN, 0.7)

def floor_grid(sc, dz, color, step=0.5, n=12):
    """piso em malha de quadrilateros (ordenacao de profundidade local) para as camadas de instalacoes."""
    xs = list(np.arange(C.X_GLASS, C.X_FLOOR_END - 1e-6, step)) + [C.X_FLOOR_END]
    for xa, xb in zip(xs[:-1], xs[1:]):
        hwa, hwb = C.floor_hw(float(xa)), C.floor_hw(float(xb))
        for i in range(n):
            ya0, ya1 = -hwa + 2 * hwa * i / n, -hwa + 2 * hwa * (i + 1) / n
            yb0, yb1 = -hwb + 2 * hwb * i / n, -hwb + 2 * hwb * (i + 1) / n
            sc.quad((xa, ya0, dz), (xb, yb0, dz), (xb, yb1, dz), (xa, ya1, dz), color, shade_on=False, stroke=color)
    fl = C.floor_outline(40)
    sc.polyline([(x, y, dz + 0.005) for (x, y) in fl] + [(fl[0][0], fl[0][1], dz + 0.005)], GREEN, 0.7)

def rect_grid(sc, dz, x1, x2, y1, y2, color, step=0.5):
    xs = list(np.arange(x1, x2 - 1e-6, step)) + [x2]; ys = list(np.arange(y1, y2 - 1e-6, step)) + [y2]
    for xa, xb in zip(xs[:-1], xs[1:]):
        for ya, yb in zip(ys[:-1], ys[1:]):
            sc.quad((xa, ya, dz), (xb, ya, dz), (xb, yb, dz), (xa, yb, dz), color, shade_on=False, stroke=color)
    sc.polyline([(x1, y1, dz + 0.005), (x2, y1, dz + 0.005), (x2, y2, dz + 0.005), (x1, y2, dz + 0.005), (x1, y1, dz + 0.005)], GREEN, 0.7)

def seg_polyline(sc, pts, color, width=1.0, dash=None, step=0.4):
    """polilinha subdividida em trechos curtos (ordenacao de profundidade correta sobre o piso em malha)."""
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(1, int(math.ceil(math.dist(a, b) / step)))
        for i in range(1, n + 1):
            out.append(tuple(a[k] + (b[k] - a[k]) * i / n for k in range(3)))
    sc.polyline(out, color, width, dash)

def bump_from(sc, nf, nl, bump=0.35):
    """empurra para a frente (na ordenacao do pintor) tudo o que foi desenhado apos os indices nf/nl:
    garante que cabos, tubos e caixas fiquem sobre o piso em malha sem interferir na camada de cima."""
    sc.faces[nf:] = [(f[0] + bump,) + tuple(f[1:]) for f in sc.faces[nf:]]
    sc.lines[nl:] = [(l[0] + bump,) + tuple(l[1:]) for l in sc.lines[nl:]]

def floor_guide(sc, dz):
    fl = C.floor_outline(40)
    sc.polyline([(x, y, dz) for (x, y) in fl] + [(fl[0][0], fl[0][1], dz)], mix(EARTH, CREAM, 0.55), 0.6, "4 3")

# ------------------------------------------------------------------ COCOON: componentes
def c_piles(sc, dz):
    ground_plate(sc, -4.3, 10.2, -3.8, 3.8, -0.62 + dz)
    for (px, py) in cocoon_pile_grid():
        sc.cylinder(px, py, -0.6 + dz, -0.02 + dz, 0.045, STEEL, n=8)
        sc.box(px - 0.1, px + 0.1, py - 0.1, py + 0.1, -0.02 + dz, 0.0 + dz, STEEL_DARK)

def c_girders(sc, dz, deck=True):
    D = C.DECK
    longi, trans, rim = cocoon_girders()
    for (x1, y1, x2, y2) in longi + trans + rim:
        sc.polyline([(x1, y1, -0.12 + dz), (x2, y2, -0.12 + dz)], STEEL, 1.8)
    if deck:
        sc.box(D["x1"], D["x2"], D["y1"], D["y2"], -0.05 + dz, 0.0 + dz, WOOD2)
        for i in range(3):
            sc.box(D["x1"] - 0.3 * (i + 1), D["x1"] - 0.3 * i, -1.2, 1.2, -0.2 + dz, -0.05 * (i + 1) + dz, WOOD2)

def c_floor(sc, dz, wall=True, deck=False):
    D = C.DECK
    if deck:
        sc.box(D["x1"], D["x2"], D["y1"], D["y2"], -0.05 + dz, 0.0 + dz, WOOD2)
    floor_tris(sc, dz, FLOOR)
    # espessura do piso (compensado + PIR): borda escura ao longo do contorno
    fl = C.floor_outline(40)
    sc.polyline([(x, y, dz - 0.07) for (x, y) in fl] + [(fl[0][0], fl[0][1], dz - 0.07)], mix(EARTH, CREAM, 0.7), 0.6)
    if wall:
        sc.box(6.6, 6.7, -2.8, 2.8, dz, 2.6 + dz, "#E6DCC8")

def c_arches(sc, dz, faint=False, rails=True):
    col = mix(STEEL, CREAM, 0.18) if faint else STEEL
    for a in C.arches():
        sc.polyline(lift(a["pts"], dz), col, 1.3 if faint else 2.2)
    sc.polyline(lift(C.front_ring(60), dz), col, 1.5 if faint else 2.8)
    if faint: return
    # quadro da cauda: anel em x 9,30 + 3 barras ate a ponta
    ring = C.section_curve(9.3, 40)
    sc.polyline(lift(ring, dz), STEEL, 1.6)
    tip = (C.L, 0.0, C.ZC + dz)
    for th in (math.pi / 2, 0.2, math.pi - 0.2):
        p = C.section_point(9.3, th)
        sc.polyline([(p[0], p[1], p[2] + dz), tip], STEEL, 1.2)
    if rails:
        for s in (-1, 1):
            sc.polyline([(x, s * C.floor_hw(x), 0.02 + dz) for x in np.linspace(C.X_GLASS, C.X_FLOOR_END - 0.05, 40)], STEEL, 1.8)
        for x in C.ARCH_X:
            hw = C.floor_hw(x)
            for s in (-1, 1):
                sc.box(x - 0.1, x + 0.1, s * hw - 0.075, s * hw + 0.075, dz, 0.012 + dz, STEEL_DARK)

def c_bracing(sc, dz):
    c_arches(sc, dz, faint=True)
    for pl in C.purlins(40):
        sc.polyline(lift(pl, dz), "#6B6B6B", 1.2)
    x1, x2, ht = C.SPINE
    xs = np.linspace(x1, x2, 20)
    for th in (math.pi / 2 - ht, math.pi / 2 + ht):
        sc.polyline(lift([C.section_point(float(x), th) for x in xs], dz), STEEL, 1.6)
        sc.polyline(lift([C.section_point(float(x), th, -0.3) for x in xs], dz), STEEL, 1.1)
    for x in np.linspace(x1, x2, 9):
        for th in (math.pi / 2 - ht, math.pi / 2 + ht):
            sc.polyline(lift([C.section_point(float(x), th), C.section_point(float(x), th, -0.3)], dz), STEEL, 0.9)
    for (xa, xb) in [(0.45, 1.65), (6.45, 7.65)]:
        for th in (0.35, math.pi - 0.35):
            pa = C.section_point(xa, th); pb = C.section_point(xb, th + 0.5); pc = C.section_point(xa, th + 0.5); pd = C.section_point(xb, th)
            sc.polyline(lift([pa, pb], dz), EARTH, 1.0, "4 3"); sc.polyline(lift([pc, pd], dz), EARTH, 1.0, "4 3")

def c_membrane(sc, dz, opacity=1.0, mark_glass=True):
    m = shell_mesh()
    V = lift(m["vertices"], dz)
    sc.mesh(V, m["membrane"], MEMB, opacity)
    sc.mesh(V, m["glass"], shade(MEMB, 0.94) if mark_glass else MEMB, opacity)

def c_shell_scaled(sc, dz, f, color, opacity=1.0):
    V, F = shell_scaled(f)
    sc.mesh(lift(V, dz), F, color, opacity)

def c_shell_wire(sc, dz, f, color):
    for pts in shell_wire(f):
        sc.polyline(lift(pts, dz), color, 0.7)

def c_chamber(sc, dz):
    """camara de ventilacao: contorno tracejado da concha + setas de fluxo (sobe pelas laterais, sai na cumeeira)."""
    for x in C.ARCH_X + [9.3]:
        sc.polyline(lift(C.section_curve(x, 40), dz), EARTH, 0.8, "4 3")
    xs = np.linspace(C.X_FRONT, C.L - 0.02, 60)
    sc.polyline([(C.shear(float(x), C.top(float(x))), 0.0, C.top(float(x)) + dz) for x in xs], EARTH, 0.8, "4 3")
    for s in (-1, 1):
        sc.polyline([(float(x), s * C.floor_hw(float(x)), dz) for x in np.linspace(C.X_GLASS, C.X_FLOOR_END, 40)], EARTH, 0.8, "4 3")
    for x in (2.2, 4.6, 7.0):
        t0, t1 = C.theta_range(x)
        ths = np.linspace(math.pi + t0 - 0.12, math.pi / 2 + 0.22, 12)
        arrow3d(sc, lift([C.section_point(x, float(t), 0.06) for t in ths], dz), COLD, 1.1)
    for x in (3.4, 5.6):
        top = C.top(x)
        arrow3d(sc, [(C.shear(x, top), 0.0, top + 0.05 + dz), (C.shear(x, top), 0.0, top + 0.6 + dz)], COLD, 1.1)

def c_windows(sc, dz, faint_shell=True):
    if faint_shell: c_membrane(sc, dz, 0.12, mark_glass=False)
    gr = lift(C.glass_ring(48), dz)
    cen = tuple(np.mean(np.array(gr), axis=0))
    for a, b in zip(gr[:-1], gr[1:]):
        sc.tri(cen, a, b, GLASS_ISO, 0.5, shade_on=False)
    for yy in (-1.6, -0.5, 0.5, 1.6):
        zt = C.ZC + (C.b(C.X_GLASS) - 0.06) * math.sqrt(max(0, 1 - (yy / (C.a(C.X_GLASS) - 0.06)) ** 2))
        sc.polyline([(C.shear(C.X_GLASS, 0), yy, dz), (C.shear(C.X_GLASS, zt), yy, zt + dz)], STEEL, 1.6)
    sc.polyline([(C.shear(C.X_GLASS, 2.4), y, 2.4 + dz) for y in (-2.3, 2.3)], STEEL, 1.4)
    sc.polyline(gr, "#6B5B45", 1.6)
    # porta pivotante (y 0,6 a 1,6)
    sc.polyline([(C.shear(C.X_GLASS, 0), 0.6, dz), (C.shear(C.X_GLASS, 2.4), 0.6, 2.4 + dz), (C.shear(C.X_GLASS, 2.4), 1.6, 2.4 + dz), (C.shear(C.X_GLASS, 0), 1.6, dz)], GREEN, 1.0)
    # janelas olho: requadro + vidro
    for w in C.WINDOWS:
        wo = lift(C.window_outline(w, 40), dz)
        cen = tuple(np.mean(np.array(wo), axis=0))
        for a, b in zip(wo, wo[1:] + wo[:1]):
            sc.tri(cen, a, b, GLASS_ISO, 0.55, shade_on=False)
        wf = lift([C.section_point(x, th, 0.07) for (x, th) in [(w["xc"] + (w["lx"] + 0.1) * ((abs(math.cos(a)) ** 1.5 + abs(math.sin(a)) ** 1.5) ** (-1 / 1.5)) * math.cos(a), w["tc"] + (w["lt"] + 0.03) * ((abs(math.cos(a)) ** 1.5 + abs(math.sin(a)) ** 1.5) ** (-1 / 1.5)) * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 41)]], dz)
        sc.polyline(wf, "#8B6B4A", 2.4)
    # espinha de luz: 4 paineis de vidro entre arcos
    x1, x2, ht = C.SPINE
    xs = np.linspace(x1, x2, 9)
    for xa, xb in zip(xs[:-1], xs[1:]):
        pa = C.section_point(float(xa), math.pi / 2 - ht, 0.02); pb = C.section_point(float(xb), math.pi / 2 - ht, 0.02)
        pc = C.section_point(float(xb), math.pi / 2 + ht, 0.02); pd = C.section_point(float(xa), math.pi / 2 + ht, 0.02)
        sc.quad(lift([pa], dz)[0], lift([pb], dz)[0], lift([pc], dz)[0], lift([pd], dz)[0], GLASS_ISO, 0.6, stroke="#6B7C84")

def c_finishes(sc, dz):
    floor_guide(sc, dz)
    add_furniture(sc, lift_items(C.furniture(), dz))

def outlet(sc, x, y, dz, color=EARTH, s=0.08):
    sc.box(x - s, x + s, y - s, y + s, dz + 0.005, dz + 0.05, color)

def c_electrical(sc, dz):
    floor_grid(sc, dz, FLOOR_LIGHT)
    nf, nl = len(sc.faces), len(sc.lines)
    seg_polyline(sc, [(6.65, -2.8, dz + 0.1), (6.65, 2.8, dz + 0.1)], GREEN, 0.7)
    z = dz + 0.1
    # quadro de distribuicao (QD) junto a parede do banho
    sc.box(6.72, 7.02, 2.05, 2.15, dz, dz + 0.45, EARTH)
    runs = [
        [(6.87, 2.1), (6.87, 0.0), (1.95, 0.0)],                                  # espinha: fita LED na cumeeira
        [(6.87, 2.1), (6.5, 2.1), (6.5, 2.35), (1.1, 2.35), (1.1, 0.0)],           # rodape esquerdo (LED indireta)
        [(6.87, 2.1), (6.87, -2.4), (6.5, -2.4), (1.1, -2.4), (1.1, 0.0)],         # rodape direito
        [(6.5, 2.35), (6.45, 1.3)], [(6.5, -2.4), (6.45, -1.3)],                   # tomadas dos criados
        [(1.1, 2.35), (1.9, 1.9)], [(3.5, 2.35), (3.5, 1.9)],                       # cafe / armario
        [(1.1, -2.4), (1.95, -1.9)], [(3.5, -2.4), (3.5, -1.9)],                    # chaise / poltrona
        [(6.87, 2.1), (7.4, 2.1), (7.4, 0.0), (8.6, 0.0)],                          # atico: evaporadora e aquecedor
        [(7.4, 2.1), (7.4, -1.3), (7.0, -1.3)],                                     # bancada do banho
        [(8.6, 0.0), (9.6, 0.0), (10.3, 0.0)],                                       # condensadora
    ]
    for r in runs:
        seg_polyline(sc, [(x, y, z) for (x, y) in r], EARTH, 1.2)
    for (x, y) in [(6.45, 1.3), (6.45, -1.3), (1.9, 1.9), (3.5, 1.9), (1.95, -1.9), (3.5, -1.9), (7.0, -1.3), (10.3, 0.0)]:
        outlet(sc, x, y, dz)
    sc.box(7.3, 7.9, -0.35, 0.35, dz, dz + 0.18, "#D9D9D6")   # evaporadora (posicao em planta)
    sc.box(8.4, 8.8, -0.2, 0.2, dz, dz + 0.22, "#D9D9D6")     # aquecedor
    sc.box(9.95, 10.7, -0.45, 0.35, dz, dz + 0.3, "#D9D9D6")   # condensadora
    bump_from(sc, nf, nl)

def pipe(sc, pts, dz, color, width=1.4, dash=None):
    seg_polyline(sc, [(x, y, dz + 0.1) for (x, y) in pts], color, width, dash)

def c_hydraulic(sc, dz):
    floor_grid(sc, dz, FLOOR_LIGHT)
    nf, nl = len(sc.faces), len(sc.lines)
    seg_polyline(sc, [(6.65, -2.8, dz + 0.1), (6.65, 2.8, dz + 0.1)], GREEN, 0.7)
    # pontos: bancada (7,0;-1,3), chuveiro (8,1;-1,3), banheira (8,35;0), bacia (7,75;1,3), aquecedor (8,6;1,6)
    sc.box(8.4, 8.8, 1.4, 1.8, dz, dz + 0.25, "#D9D9D6")
    cold = [[(9.7, 1.6), (8.8, 1.6)], [(9.7, 1.6), (9.7, -1.0), (7.0, -1.0), (7.0, -1.3)], [(8.1, -1.0), (8.1, -1.3)],
            [(8.35, -1.0), (8.35, 0.0)], [(7.75, -1.0), (7.75, 1.3)]]
    hot = [[(8.6, 1.4), (8.6, 0.85), (8.35, 0.85), (8.35, 0.15)], [(8.6, 0.85), (8.6, -0.8), (8.1, -0.8), (8.1, -1.2)], [(8.6, -0.8), (7.1, -0.8), (7.1, -1.2)]]
    for r in cold: pipe(sc, r, dz, COLD)
    for r in hot: pipe(sc, r, dz, HOT)
    drain = [[(7.0, -1.3), (7.0, -0.5), (9.7, -0.5)], [(8.1, -1.3), (8.1, -0.5)], [(8.35, 0.0), (8.35, -0.5)], [(7.75, 1.3), (7.75, -0.5)]]
    for r in drain: pipe(sc, r, dz - 0.04, STEEL, 2.6, "6 4")
    for (x, y) in [(7.0, -1.3), (8.1, -1.3), (8.35, 0.0), (7.75, 1.3)]:
        sc.cylinder(x, y, dz + 0.02, dz + 0.1, 0.07, COLD, n=8)
    arrow3d(sc, [(9.7, -0.5, dz), (10.4, -0.5, dz)], STEEL, 1.4)
    arrow3d(sc, [(10.4, 1.6, dz), (9.75, 1.6, dz)], COLD, 1.2)
    bump_from(sc, nf, nl)

# ------------------------------------------------------------------ ZENITH: componentes
def z_piles(sc, dz):
    ground_plate(sc, -4.2, 12.3, -5.3, 5.3, -0.62 + dz)
    for (px, py) in zenith_pile_grid():
        sc.cylinder(px, py, -0.6 + dz, -0.02 + dz, 0.045, STEEL, n=8)
        sc.box(px - 0.1, px + 0.1, py - 0.1, py + 0.1, -0.02 + dz, 0.0 + dz, STEEL_DARK)
    for (px, py) in zenith_tension_piles():
        sc.cylinder(px, py, -0.6 + dz, -0.02 + dz, 0.045, EARTH, n=8)
        sc.cylinder(px, py, -0.02 + dz, 0.06 + dz, 0.1, EARTH, n=8)
    for (px, py) in zenith_stay_anchors():
        sc.cylinder(px, py, -0.4 + dz, 0.02 + dz, 0.03, EARTH, n=6)

def z_girders(sc, dz, deck=True):
    D, Wk = Z.DECK, Z.WALK
    longi, trans, rim = zenith_girders()
    for (x1, y1, x2, y2) in longi + trans + rim:
        sc.polyline([(x1, y1, -0.12 + dz), (x2, y2, -0.12 + dz)], STEEL, 1.8)
    if deck:
        sc.box(D["x1"], D["x2"], D["y1"], D["y2"], -0.05 + dz, 0.0 + dz, WOOD2)
        sc.box(Wk["x1"], Wk["x2"], Wk["y1"], Wk["y2"], -0.05 + dz, 0.0 + dz, WOOD2)
        for i in range(3):
            sc.box(D["x1"] - 0.3 * (i + 1), D["x1"] - 0.3 * i, -1.2, 1.2, -0.2 + dz, -0.05 * (i + 1) + dz, WOOD2)
        H = Z.HOTTUB
        sc.cylinder(H["x"], H["y"], dz, 0.55 + dz, H["r"], "#DDD6C8")
        sc.cylinder(H["x"], H["y"], dz, 0.5 + dz, H["r"] - 0.1, GLASS_ISO)

def z_floor(sc, dz, walls=True, columns=True, deck=False):
    D, Wk = Z.DECK, Z.WALK
    if deck:
        sc.box(D["x1"], D["x2"], D["y1"], D["y2"], -0.05 + dz, 0.0 + dz, WOOD2)
        sc.box(Wk["x1"], Wk["x2"], Wk["y1"], Wk["y2"], -0.05 + dz, 0.0 + dz, WOOD2)
    sc.box(0.05, 9.45, -2.65, 2.65, -0.07 + dz, 0.0 + dz, FLOOR)
    if columns:
        for (cx, cy) in Z.columns():
            sc.polyline([(cx, cy, dz), (cx, cy, 2.9 + dz)], STEEL, 3.0)
    if walls: z_walls(sc, dz)

def z_walls(sc, dz, opacity=1.0):
    h = Z.H_WALL
    for w in Z.walls():
        (xa, ya), (xb, yb) = w["p1"], w["p2"]
        if w["kind"] == "glass":
            sc.quad((xa, ya, dz), (xb, yb, dz), (xb, yb, h + dz), (xa, ya, h + dz), GLASS_ISO, 0.35 * opacity, stroke="#6B7C84")
        elif w["kind"] == "wood":
            sc.quad((xa, ya, dz), (xb, yb, dz), (xb, yb, h + dz), (xa, ya, h + dz), "#B08A5E", opacity)
        else:
            dx = 0.02 if abs(xa - xb) < 1e-6 else 0.0
            dy = 0.02 if (ya > 0 and abs(ya - yb) < 1e-6) else 0.0
            sc.quad((xa + dx, ya + dy, w["z1"] + dz), (xb + dx, yb + dy, w["z1"] + dz), (xb + dx, yb + dy, w["z2"] + dz), (xa + dx, ya + dy, w["z2"] + dz), GLASS_ISO, 0.6)

def z_eave_ring(sc, dz, color=STEEL):
    for (a, b, c, d) in [(0, 9.5, -2.8, -2.65), (0, 9.5, 2.65, 2.8), (-0.05, 0.1, -2.8, 2.8), (9.4, 9.55, -2.8, 2.8)]:
        sc.box(a, b, c, d, 2.75 + dz, 2.9 + dz, color)

def z_masts(sc, dz, faint=False):
    col = mix(STEEL, CREAM, 0.2) if faint else STEEL
    for mst in Z.masts():
        sc.polyline([(mst["x"], mst["y"], dz), (mst["x"], mst["y"], mst["z2"] + dz)], col, 4.0)
        sc.box(mst["x"] - 0.125, mst["x"] + 0.125, mst["y"] - 0.125, mst["y"] + 0.125, dz, 0.012 + dz, STEEL_DARK)
    for cr in Z.crowns():
        for arm in cr["arms"]:
            sc.polyline(lift(arm, dz), col, 2.2)
        sc.polyline(lift(cr["ring"], dz), col, 2.4)

def z_posts(sc, dz, stays=True, edge=True):
    x0, x1, y0, y1 = Z.roof_bounds()
    for (px, py) in Z.posts():
        top = Z.edge_height(px, py)
        lean = 0.12
        dx = -lean if px < 0 else (lean if px > 9 else 0); dy = -lean if py < 0 else (lean if py > 0 else 0)
        sc.polyline([(px, py, -0.05 + dz), (px + dx, py + dy, top + dz)], STEEL, 3.2)
        if stays: sc.polyline([(px + dx, py + dy, top + dz), (px + dx * 8, py + dy * 8, -0.05 + dz)], EARTH, 0.9, "4 3")
    if edge:
        for pts in ([(x, y0, Z.edge_height(x, y0)) for x in np.linspace(x0, x1, 40)], [(x, y1, Z.edge_height(x, y1)) for x in np.linspace(x0, x1, 40)],
                    [(x0, y, Z.edge_height(x0, y)) for y in np.linspace(y0, y1, 40)], [(x1, y, Z.edge_height(x1, y)) for y in np.linspace(y0, y1, 40)]):
            sc.polyline(lift(pts, dz), STEEL, 1.5)

_ROOF = {}
def roof_mesh(nx=34, ny=20, liner=False):
    key = (nx, ny, liner)
    if key not in _ROOF: _ROOF[key] = Z.roof_mesh(nx, ny, liner=liner)
    return _ROOF[key]

def z_roof(sc, dz, opacity=1.0):
    rm = roof_mesh()
    sc.mesh(lift(rm["vertices"], dz), rm["faces"], MEMB, opacity)

def z_liner(sc, dz, color=SAND2, opacity=1.0, drop=0.0):
    rm = roof_mesh(28, 16, liner=True)
    sc.mesh(lift(rm["vertices"], dz - drop), rm["faces"], color, opacity)

def z_liner_wire(sc, dz, color, drop=0.0):
    for y in np.linspace(-2.7, 2.7, 10):
        sc.polyline([(float(x), float(y), Z.liner_z(float(x), float(y)) + dz - drop) for x in np.linspace(0, 9.5, 40)], color, 0.7)
    for x in np.linspace(0, 9.5, 16):
        sc.polyline([(float(x), float(y), Z.liner_z(float(x), float(y)) + dz - drop) for y in np.linspace(-2.7, 2.7, 24)], color, 0.7)

def z_chamber(sc, dz):
    x0, x1, y0, y1 = Z.roof_bounds()
    for pts in ([(x, y0, Z.edge_height(x, y0)) for x in np.linspace(x0, x1, 40)], [(x, y1, Z.edge_height(x, y1)) for x in np.linspace(x0, x1, 40)],
                [(x0, y, Z.edge_height(x0, y)) for y in np.linspace(y0, y1, 40)], [(x1, y, Z.edge_height(x1, y)) for y in np.linspace(y0, y1, 40)]):
        sc.polyline(lift(pts, dz), EARTH, 0.8, "4 3")
    for y in (0.4, 1.6, -2.0):
        sc.polyline([(x, y, z + dz) for (x, z) in Z.ridge_profile(y, 80)], EARTH, 0.8, "4 3")
    for x in (1.6, 6.3, 4.0):
        sc.polyline([(x, y, z + dz) for (y, z) in Z.cross_profile(x, 60)], EARTH, 0.8, "4 3")
    # setas: ar entra pelo beiral, sobe entre membrana e forro e sai pela chamine do Respiro / oculo
    for (xa, ya, xb, yb) in [(2.4, -2.6, 1.8, 1.3), (7.2, -2.6, 6.45, 0.2), (9.3, 0.6, 6.9, 0.5)]:
        pts = [(xa + (xb - xa) * t, ya + (yb - ya) * t, Z.roof_z(xa + (xb - xa) * t, ya + (yb - ya) * t) + 0.05 + dz) for t in np.linspace(0, 1, 12)]
        arrow3d(sc, pts, COLD, 1.1)
    for p in Z.PEAKS:
        arrow3d(sc, [(p["x"], p["y"], p["h"] + 0.05 + dz), (p["x"], p["y"], p["h"] + 0.7 + dz)], COLD, 1.1)

def z_finishes(sc, dz):
    sc.polyline([(0.05, -2.65, dz), (9.45, -2.65, dz), (9.45, 2.65, dz), (0.05, 2.65, dz), (0.05, -2.65, dz)], mix(EARTH, CREAM, 0.55), 0.6, "4 3")
    add_furniture(sc, lift_items(Z.furniture(), dz))

def z_electrical(sc, dz):
    rect_grid(sc, dz, 0.05, 9.45, -2.65, 2.65, FLOOR_LIGHT)
    nf, nl = len(sc.faces), len(sc.lines)
    seg_polyline(sc, [(6.32, -2.6, dz + 0.1), (6.32, 1.5, dz + 0.1)], GREEN, 0.7)
    z = dz + 0.1
    sc.box(6.5, 6.8, 2.45, 2.55, dz, dz + 0.45, EARTH)   # QD junto a parede da cabeceira
    runs = [
        [(6.65, 2.5), (6.65, 0.4), (6.3, 0.4)],                                       # mastro M1: luz do oculo
        [(6.65, 2.5), (2.2, 2.5), (1.6, 1.6)],                                        # totem / mastro M2
        [(2.2, 2.5), (0.4, 2.5), (0.4, -2.4), (9.2, -2.4), (9.2, 2.4), (7.0, 2.4)],   # perimetro: LED no anel de beiral
        [(0.4, 2.5), (1.6, 2.3)], [(4.8, 2.5), (4.8, 2.3)],                            # cafe / closet
        [(6.65, 1.3), (5.9, 1.3)], [(6.65, -1.3), (5.9, -1.3)],                        # criados
        [(0.4, -1.4), (2.6, -1.4)],                                                   # sofa / chaise
        [(6.65, 0.4), (7.7, 0.4), (7.7, 0.8)], [(7.7, 0.4), (7.7, -0.7), (6.8, -0.7)], # atico (AC, aquecedor) e bancada
        [(9.2, -1.8), (10.25, -1.8)],                                                 # condensadora
        [(0.4, -2.4), (-1.55, -2.4), (-1.55, -2.05)],                                  # bomba da hidromassagem
    ]
    for r in runs:
        seg_polyline(sc, [(x, y, z) for (x, y) in r], EARTH, 1.2)
    for (x, y) in [(1.6, 2.3), (4.8, 2.3), (5.9, 1.3), (5.9, -1.3), (2.6, -1.4), (6.8, -0.7), (10.25, -1.8), (-1.55, -2.05)]:
        outlet(sc, x, y, dz)
    sc.box(7.2, 8.2, 0.3, 1.3, dz, dz + 0.18, "#D9D9D6")
    sc.box(9.85, 10.65, -2.2, -1.4, dz, dz + 0.3, "#D9D9D6")
    bump_from(sc, nf, nl)

def z_hydraulic(sc, dz):
    rect_grid(sc, dz, 0.05, 9.45, -2.65, 2.65, FLOOR_LIGHT)
    nf, nl = len(sc.faces), len(sc.lines)
    seg_polyline(sc, [(6.32, -2.6, dz + 0.1), (6.32, 1.5, dz + 0.1)], GREEN, 0.7)
    # pontos: bancada dupla (6,8;-0,7), bacia (7,7;-2,2), chuveiro (8,85;-2,0), banheira (9,0;0,35), aquecedor (7,6;1,4), ducha externa (5,0;3,1), hidro (-1,55;-2,05)
    sc.box(7.4, 7.9, 1.2, 1.6, dz, dz + 0.25, "#D9D9D6")
    cold = [[(9.7, 1.4), (7.9, 1.4)], [(9.7, 1.4), (9.7, -1.0), (6.8, -1.0), (6.8, -0.7)], [(7.7, -1.0), (7.7, -2.2)], [(8.85, -1.0), (8.85, -2.0)],
            [(9.0, -1.0), (9.0, 0.2)], [(7.9, 1.4), (5.0, 1.4), (5.0, 3.1)], [(6.8, -1.0), (0.3, -1.0), (0.3, -2.05), (-1.55, -2.05)]]
    hot = [[(7.65, 1.2), (7.65, 0.9), (9.1, 0.9), (9.1, 0.25)], [(9.1, 0.9), (9.1, -0.8), (8.95, -0.8), (8.95, -1.9)], [(9.1, -0.8), (6.9, -0.8), (6.9, -0.6)],
           [(7.65, 0.9), (5.1, 0.9), (5.1, 3.1)]]
    for r in cold: pipe(sc, r, dz, COLD)
    for r in hot: pipe(sc, r, dz, HOT)
    drain = [[(6.8, -0.7), (6.8, -1.6), (9.7, -1.6)], [(7.7, -2.2), (7.7, -1.6)], [(8.85, -2.0), (8.85, -1.6)], [(9.0, 0.35), (9.3, 0.35), (9.3, -1.6)],
             [(5.0, 3.1), (5.0, 2.8), (9.7, 2.8)], [(-1.55, -2.05), (-1.55, -2.9), (0.0, -2.9)]]
    for r in drain: pipe(sc, r, dz - 0.04, STEEL, 2.6, "6 4")
    for (x, y) in [(6.8, -0.7), (7.7, -2.2), (8.85, -2.0), (9.0, 0.35), (5.0, 3.1)]:
        sc.cylinder(x, y, dz + 0.02, dz + 0.1, 0.07, COLD, n=8)
    arrow3d(sc, [(9.7, -1.6, dz), (10.4, -1.6, dz)], STEEL, 1.4)
    arrow3d(sc, [(10.4, 1.4, dz), (9.75, 1.4, dz)], COLD, 1.2)
    bump_from(sc, nf, nl)

# ------------------------------------------------------------------ definicao das camadas
def layer(num, name, sub, draw, bb, dz, func=""):
    return dict(num=num, name=name, sub=sub, draw=draw, bb=bb, dz=dz, func=func)

C_BB_BASE = (-4.3, 10.2, -3.8, 3.8, -0.62, 0.0)
C_BB_DECK = (-4.6, 9.6, -3.25, 3.25, -0.2, 0.0)
C_BB_FLOOR = (0.9, 9.4, -3.0, 3.0, -0.1, 2.6)
C_BB_SHELL = (-0.2, 9.6, -3.0, 3.0, 0.0, 4.2)
C_BB_FURN = (1.0, 10.7, -3.0, 3.0, 0.0, 2.8)

def cocoon_exploded_layers(dzs):
    return [
        dict(layer(1, "Fundacao", "44 estacas helicoidais Ø76, helice Ø300, cabecote ajustavel", c_piles, C_BB_BASE, dzs[0]), anchor_pt=(10.2, -3.8, -0.62)),
        layer(2, "Quadro do deck", "Vigas U 150 x 60 x 3,0 galv. + vigotas 50 x 150; deck cumaru 4,60 x 6,50", lambda sc, dz: c_girders(sc, dz, True), C_BB_DECK, dzs[1]),
        layer(3, "Piso", "Compensado 18 mm + PIR 50 mm + carvalho 14 mm; parede do banho em x 6,60", lambda sc, dz: c_floor(sc, dz, True), C_BB_FLOOR, dzs[2]),
        layer(4, "Arcos", "Anel A0 Ø101,6 + 7 arcos Ø88,9 x 3,6 + quadro da cauda; trilhos 100 x 50 e chapas D01", lambda sc, dz: c_arches(sc, dz), C_BB_SHELL, dzs[3]),
        layer(5, "Travamentos", "7 tercas Ø48,3, Espinha de Luz (trelica 300 mm) e cabos em X Ø8 inox", c_bracing, C_BB_SHELL, dzs[4]),
        layer(6, "Membrana externa", "PVDF 1050 g/m² tensionada (2,5 kN/m), 118 m², aberturas dos Olhos", lambda sc, dz: c_membrane(sc, dz), C_BB_SHELL, dzs[5]),
        layer(7, "Isolamento e forro", "Camara ventilada 60 mm, la PET 50 mm + manta refletiva, forro tensionado", lambda sc, dz: c_shell_scaled(sc, dz, 0.92, SAND2, 0.9), C_BB_SHELL, dzs[6]),
        layer(8, "Esquadrias", "Anel de vidro frontal com porta pivotante, 6 Olhos em lente, 4 paineis da Espinha", lambda sc, dz: c_windows(sc, dz), C_BB_SHELL, dzs[7]),
        layer(9, "Acabamentos", "Mobiliario fixo, banho com banheira na cauda, evaporadora e condensadora", c_finishes, C_BB_FURN, dzs[8]),
    ]

Z_BB_BASE = (-4.2, 12.3, -5.3, 5.3, -0.62, 0.1)
Z_BB_DECK = (-3.9, 9.5, -3.4, 3.5, -0.2, 0.55)
Z_BB_BODY = (0.0, 9.5, -2.7, 2.7, -0.1, 2.9)
Z_BB_ROOF = (-2.4, 10.5, -3.7, 3.7, 0.0, 5.8)
Z_BB_LINER = (0.0, 9.5, -2.7, 2.7, 2.4, 5.5)
Z_BB_FURN = (0.0, 10.7, -2.7, 2.7, 0.0, 2.9)

def zenith_exploded_layers(dzs):
    return [
        dict(layer(1, "Fundacao", "30 estacas helicoidais Ø76 sob o piso + 7 de tracao sob os postes + chumbadores dos estais", z_piles, Z_BB_BASE, dzs[0]), anchor_pt=(12.3, -5.3, -0.62)),
        layer(2, "Quadro do deck", "Vigas U 150 x 60 x 3,0; terraco 3,00 x 6,80 com hidromassagem; passarela 0,80", lambda sc, dz: z_girders(sc, dz, True), Z_BB_DECK, dzs[1]),
        layer(3, "Piso e paineis SIP", "Piso 9,50 x 5,40; paineis SIP 100 mm e vidros; 10 pilares Ø101,6 embutidos", lambda sc, dz: z_floor(sc, dz, True, True), Z_BB_BODY, dzs[2]),
        layer(4, "Mastros, anel e postes", "M1 Ø139,7 e M2 Ø114,3 com coroas e aneis; anel de beiral 150 x 100; 7 postes Ø76,1 e cabos", lambda sc, dz: (z_eave_ring(sc, dz), z_masts(sc, dz), z_posts(sc, dz)), Z_BB_ROOF, dzs[3]),
        layer(5, "Membrana externa", "PVDF 1050 g/m², 95 m², em balanco 2,40 m na frente e 1,00 m nos lados", lambda sc, dz: z_roof(sc, dz), Z_BB_ROOF, dzs[4]),
        layer(6, "Forro isolado", "La PET 50 mm + tecido tensionado a 300 mm da membrana; oculo e chamine", lambda sc, dz: z_liner(sc, dz), Z_BB_LINER, dzs[5]),
        layer(7, "Acabamentos", "Mobiliario fixo, parede da cabeceira, Ilha do Cafe, banho com banheira", z_finishes, Z_BB_FURN, dzs[6]),
    ]

FUNC = {
    1: "Estacas helicoidais transferem as cargas ao solo sem escavacao",
    2: "Vigas U 150 x 60 galvanizadas formam o quadro nivelado",
    3: "Vigotas, PIR 50 mm e piso de carvalho sobre compensado",
    6: "PVDF 1050 g/m² tensionada: pele estanque e refletiva",
    7: "Ventila a face interna da membrana e seca a condensacao",
    8: "La PET 50 mm + manta refletiva controlam ganho e perda de calor",
    9: "Filme de controle de vapor protege o isolamento da umidade",
    10: "Forro tensionado acustico define a superficie interna",
    11: "Quadro no atico, circuitos embutidos e iluminacao indireta",
    12: "PEX Ø25 agua fria e quente, esgoto Ø100 por gravidade",
    13: "Mobiliario fixo, divisorias e revestimentos",
}

def cocoon_camadas_layers(dzs):
    L = [
        dict(layer(1, "Fundacao", "44 estacas helicoidais Ø76", c_piles, C_BB_BASE, dzs[0], FUNC[1]), anchor_pt=(10.2, -3.8, -0.62)),
        layer(2, "Estrutura do deck", "Vigas U 150 x 60 x 3,0 + bordas", lambda sc, dz: c_girders(sc, dz, False), C_BB_DECK, dzs[1], FUNC[2]),
        layer(3, "Piso e isolamento", "Deck cumaru + piso interno isolado", lambda sc, dz: c_floor(sc, dz, False, True), (-4.6, 9.4, -3.25, 3.25, -0.1, 0.0), dzs[2], FUNC[3]),
        layer(4, "Estrutura metalica principal", "Anel A0 + 7 arcos Ø88,9 + quadro da cauda", lambda sc, dz: c_arches(sc, dz), C_BB_SHELL, dzs[3], "Oito arcos elipticos sustentam a concha e ancoram nos trilhos"),
        layer(5, "Travamentos", "Tercas Ø48,3, espinha e cabos em X", c_bracing, C_BB_SHELL, dzs[4], "Tercas, espinha e cabos em X impedem a ovalizacao"),
        layer(6, "Membrana externa", "PVDF 1050 g/m² tensionada", lambda sc, dz: c_membrane(sc, dz), C_BB_SHELL, dzs[5], FUNC[6]),
        layer(7, "Camara de ventilacao", "Lamina de ar 60 mm entre membrana e isolamento", c_chamber, C_BB_SHELL, dzs[6], FUNC[7]),
        layer(8, "Isolamento termico", "La PET 50 mm + manta refletiva", lambda sc, dz: c_shell_scaled(sc, dz, 0.95, SAND2, 1.0), C_BB_SHELL, dzs[7], FUNC[8]),
        layer(9, "Barreira de condensacao", "Filme de controle de vapor", lambda sc, dz: c_shell_wire(sc, dz, 0.93, mix(SILVER, CREAM, 0.6)), C_BB_SHELL, dzs[8], FUNC[9]),
        layer(10, "Membrana interna", "Forro tensionado acustico (tecido)", lambda sc, dz: c_shell_scaled(sc, dz, 0.90, BEIGE, 1.0), C_BB_SHELL, dzs[9], FUNC[10]),
        layer(11, "Instalacoes eletricas", "QD 12 modulos, 6,5 kW instalados", c_electrical, (0.9, 10.7, -3.0, 3.0, 0.0, 0.5), dzs[10], FUNC[11]),
        layer(12, "Instalacoes hidraulicas", "PEX Ø25, aquecedor no atico, esgoto Ø100", c_hydraulic, (0.9, 10.4, -3.0, 3.0, -0.1, 0.3), dzs[11], FUNC[12]),
        layer(13, "Acabamento interno", "Mobiliario fixo e parede do banho", c_finishes, C_BB_FURN, dzs[12], FUNC[13]),
    ]
    return L

def zenith_camadas_layers(dzs):
    L = [
        dict(layer(1, "Fundacao", "30 estacas Ø76 + 7 estacas de tracao", z_piles, Z_BB_BASE, dzs[0], FUNC[1]), anchor_pt=(12.3, -5.3, -0.62)),
        layer(2, "Estrutura do deck", "Vigas U 150 x 60 x 3,0 + bordas", lambda sc, dz: z_girders(sc, dz, False), Z_BB_DECK, dzs[1], FUNC[2]),
        layer(3, "Piso e isolamento", "Terraco, passarela e piso interno isolado", lambda sc, dz: z_floor(sc, dz, False, False, True), (-3.9, 9.5, -3.4, 3.5, -0.1, 0.0), dzs[2], FUNC[3]),
        layer(4, "Estrutura principal", "Mastros, 10 pilares, anel de beiral e SIP", lambda sc, dz: (z_walls(sc, dz, 0.6), z_eave_ring(sc, dz), z_masts(sc, dz), [sc.polyline([(cx, cy, dz), (cx, cy, 2.9 + dz)], STEEL, 3.0) for (cx, cy) in Z.columns()]), Z_BB_ROOF, dzs[3], "Mastros, pilares, anel de beiral e paineis SIP formam o esqueleto"),
        layer(5, "Travamentos", "7 postes estaiados + cabo de borda Ø12", lambda sc, dz: (z_masts(sc, dz, faint=True), z_posts(sc, dz)), Z_BB_ROOF, dzs[4], "Postes estaiados e cabo de borda tensionam a membrana"),
        layer(6, "Membrana externa", "PVDF 1050 g/m² tensionada, 95 m²", lambda sc, dz: z_roof(sc, dz), Z_BB_ROOF, dzs[5], FUNC[6]),
        layer(7, "Camara de ventilacao", "Lamina de ar 300 mm ate o forro", z_chamber, Z_BB_ROOF, dzs[6], "Ventila a face interna da membrana e sai pela chamine do Respiro"),
        layer(8, "Isolamento termico", "La PET 50 mm sobre o forro", lambda sc, dz: z_liner(sc, dz, SAND2, 1.0), Z_BB_LINER, dzs[7], FUNC[8]),
        layer(9, "Barreira de condensacao", "Filme de controle de vapor", lambda sc, dz: z_liner_wire(sc, dz, mix(SILVER, CREAM, 0.6), 0.05), Z_BB_LINER, dzs[8], FUNC[9]),
        layer(10, "Membrana interna", "Forro tensionado acustico (tecido)", lambda sc, dz: z_liner(sc, dz, BEIGE, 1.0, 0.1), Z_BB_LINER, dzs[9], FUNC[10]),
        layer(11, "Instalacoes eletricas", "QD 12 modulos, 8,5 kW instalados", z_electrical, (-1.7, 10.7, -2.7, 2.7, 0.0, 0.5), dzs[10], FUNC[11]),
        layer(12, "Instalacoes hidraulicas", "PEX Ø25, aquecedor no atico, esgoto Ø100", z_hydraulic, (-1.7, 10.4, -3.0, 3.2, -0.1, 0.3), dzs[11], FUNC[12]),
        layer(13, "Acabamento interno", "Mobiliario fixo e parede da cabeceira", z_finishes, Z_BB_FURN, dzs[12], FUNC[13]),
    ]
    return L

# ------------------------------------------------------------------ folhas
def draw_layers(sh, layers, box, smax, guides):
    s, ox, oy = fit(layers, box, smax)
    sc = Scene(sh, s, ox, oy)
    for L in layers:
        nf, nl = len(sc.faces), len(sc.lines)
        L["draw"](sc, L["dz"])
        pts = [p for f in sc.faces[nf:] for p in f[1]] + [l[1] for l in sc.lines[nl:]] + [l[2] for l in sc.lines[nl:]]
        if L.get("anchor_pt"):
            ap = L["anchor_pt"]; p = sc.proj((ap[0], ap[1], ap[2] + L["dz"])); pts.append((p[0], p[1]))
        L["anchor"] = min(pts, key=lambda p: p[0])
    ztop = layers[-1]["dz"] + layers[-1]["bb"][5] + 0.8
    for (gx, gy) in guides:
        sc.polyline([(gx, gy, -0.7), (gx, gy, ztop)], mix(EARTH, CREAM, 0.6), 0.8, "6 4", on_top=True)
    sc.render()
    return sc

def label_positions(sc, layers, ymin, ymax, pitch):
    """y de tela para cada rotulo (ponto de ancoragem = canto esquerdo da camada), sem sobreposicao."""
    anchors = [L["anchor"] for L in layers]
    ys = [a[1] for a in anchors]
    # de baixo para cima: garante espacamento minimo
    for i in range(1, len(ys)):
        ys[i] = min(ys[i], ys[i - 1] - pitch)
    ys[0] = min(ys[0], ymax)
    for i in range(1, len(ys)):
        ys[i] = min(ys[i], ys[i - 1] - pitch)
    if ys[-1] < ymin:   # empurra tudo para baixo se estourou o topo
        d = ymin - ys[-1]
        ys = [y + d for y in ys]
    return anchors, ys

def modelo_explodido(product):
    coc = product == "cocoon"
    name = "ZION COCOON" if coc else "ZION ZENITH"
    sh = Sheet(1600, 1000)
    sh.header(("Zion Cocoon" if coc else "Zion Zenith") + " · Modelo explodido da estrutura",
              "Isometrica explodida · grupos construtivos separados na vertical, da fundacao aos acabamentos · sem escala")
    if coc:
        dzs = [0.0, 1.3, 2.5, 4.0, 7.4, 10.8, 14.4, 18.0, 20.6]
        layers = cocoon_exploded_layers(dzs); guides = [(9.0, -1.3), (-3.3, 2.6)]
    else:
        dzs = [0.0, 1.6, 3.2, 6.4, 10.0, 15.0, 19.0]
        layers = zenith_exploded_layers(dzs); guides = [(10.5, -3.7), (-2.4, 3.7)]
    sc = draw_layers(sh, layers, (370, 100, 1040, 870), 46, guides)
    anchors, ys = label_positions(sc, layers, 120, 850, 46)
    for L, (ax, ay), y in zip(layers, anchors, ys):
        sh.add(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="336" y2="{y:.1f}" stroke="{GREEN}" stroke-width="0.7"/>')
        sh.add(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="2.2" fill="{GREEN}"/>')
        sh.callout_px(46, y - 4, L["num"], r=9)
        sh.text_px(62, y, L["name"].upper(), size=11.5, weight=700, spacing=0.16, anchor="start")
        sh.text_px(62, y + 14, L["sub"], size=9, fill=EARTH, anchor="start")
    # coluna direita: sequencia de montagem (ESPECIFICACAO_TECNICA, item 4)
    X = 1215
    sh.text_px(X, 118, "SEQUENCIA DE MONTAGEM", size=11, weight=700, spacing=0.22, anchor="start")
    seq = ([("1", "Fundacao: estacas + cabecotes", "1 dia"), ("2-3", "Deck + piso", "2 dias"), ("4-5", "Estrutura metalica", "2 dias"),
            ("6-7", "Membrana + isolamento + forro", "2 dias"), ("8", "Vidros + paineis", "1,5 dia"), ("9", "Instalacoes + acabamentos", "3,5 dias"),
            ("", "Total (dias uteis)", "12"), ("", "Desmontagem", "4 dias")] if coc else
           [("1", "Fundacao: estacas + cabecotes", "1,5 dia"), ("2-3", "Deck + piso + paineis SIP", "3 dias"), ("4", "Pilares, anel, mastros + postes", "2,5 dias"),
            ("5-6", "Membrana + forro isolado", "2,5 dias"), ("3", "Vidros", "2 dias"), ("7", "Instalacoes + acabamentos", "3,5 dias"),
            ("", "Total (dias uteis)", "15"), ("", "Desmontagem", "5 dias")])
    for i, (n, t, d) in enumerate(seq):
        y = 146 + i * 22
        if n: sh.callout_px(X + 8, y - 4, n, r=8) if len(n) == 1 else sh.text_px(X + 8, y, n, size=9, weight=700)
        sh.text_px(X + 26, y, t, size=10, anchor="start", weight=(700 if not n else 400))
        sh.text_px(X + 345, y, d, size=10, anchor="end", fill=EARTH)
        sh.add(f'<line x1="{X}" y1="{y + 7}" x2="{X + 345}" y2="{y + 7}" stroke="{GREEN}" stroke-width="0.4" opacity="0.4"/>')
    y0 = 146 + len(seq) * 22 + 20
    sh.text_px(X, y0, "PESOS E LOGISTICA", size=11, weight=700, spacing=0.22, anchor="start")
    notes = (["Estrutura metalica: ≈ 1.200 kg de aco + 200 kg de aluminio", "Peso total embarcado: ≈ 8,6 t em 1 conteiner 40' HC",
              "Equipe: 4 montadores + 1 lider; guincho manual 1 t", "Estacas instaladas com motor hidraulico portatil", "Todas as ligacoes parafusadas (classe 8.8, zincadas)"] if coc else
             ["Estrutura metalica: ≈ 1.230 kg de aco + 95 kg de aluminio", "Peso total embarcado: ≈ 10,8 t em 1 conteiner 40' HC",
              "Equipe: 4 montadores + 1 lider; talha para icar os mastros", "Postes estaiados a 7 estacas de tracao", "Paineis SIP formam diafragma rigido; anel de beiral comprimido"])
    for i, t in enumerate(notes):
        sh.text_px(X, y0 + 24 + i * 18, t, size=9.5, fill=EARTH, anchor="start")
    sh.text_px(X, y0 + 24 + len(notes) * 18 + 14, "Linhas tracejadas verticais: eixos de referencia da malha de estacas.", size=8.5, fill=EARTH, anchor="start")
    sh.title_block(name, "Modelo explodido da estrutura", "sem escala", "10/27",
                   ("Nove grupos, da fundacao aos acabamentos, com sequencia de montagem" if coc else
                    "Sete grupos, da fundacao aos acabamentos, com sequencia de montagem"))
    return sh

def camadas_construtivas(product):
    coc = product == "cocoon"
    name = "ZION COCOON" if coc else "ZION ZENITH"
    sh = Sheet(1200, 2000)
    sh.header(("Zion Cocoon" if coc else "Zion Zenith") + " · Camadas construtivas",
              "Pilha explodida das 13 camadas, da fundacao ao acabamento interno · isometrica · sem escala")
    step = 3.0
    dzs = [0.0]
    heights = ([0.6, 0.9, 1.0, 3.2, 3.2, 3.2, 3.2, 3.0, 3.0, 2.9, 0.9, 0.9, 2.6] if coc else
               [0.7, 0.9, 1.1, 4.4, 4.4, 4.4, 4.4, 2.6, 2.6, 2.6, 0.9, 0.9, 2.6])
    for h in heights[:-1]:
        dzs.append(dzs[-1] + step + 0.35 * h)
    if coc:
        layers = cocoon_camadas_layers(dzs); guides = [(9.0, -1.3), (-3.3, 2.6)]
    else:
        layers = zenith_camadas_layers(dzs); guides = [(10.5, -3.7), (-2.4, 3.7)]
    sc = draw_layers(sh, layers, (350, 100, 1170, 1860), 44, guides)
    anchors, ys = label_positions(sc, layers, 130, 1840, 64)
    for L, (ax, ay), y in zip(layers, anchors, ys):
        sh.add(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="322" y2="{y:.1f}" stroke="{GREEN}" stroke-width="0.7"/>')
        sh.add(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="2.2" fill="{GREEN}"/>')
        sh.callout_px(46, y - 4, L["num"], r=9)
        sh.text_px(64, y - 12, f"CAMADA {L['num']:02d}", size=8.5, fill=EARTH, spacing=0.28, anchor="start")
        sh.text_px(64, y + 2, L["name"].upper(), size=11.5, weight=700, spacing=0.14, anchor="start")
        sh.text_px(64, y + 16, L["func"], size=8.8, fill=EARTH, anchor="start")
        sh.add(f'<line x1="64" y1="{y + 24}" x2="310" y2="{y + 24}" stroke="{GREEN}" stroke-width="0.4" opacity="0.35"/>')
    sh.title_block(name, "Camadas construtivas (explodida)", "sem escala", "13/27",
                   "Da fundacao ao acabamento: envelope em cinco camadas e instalacoes")
    return sh


def build():
    os.makedirs(OUTC, exist_ok=True); os.makedirs(OUTZ, exist_ok=True)
    modelo_explodido("cocoon").save(os.path.join(OUTC, "10_modelo_explodido.svg"))
    modelo_explodido("zenith").save(os.path.join(OUTZ, "10_modelo_explodido.svg"))
    camadas_construtivas("cocoon").save(os.path.join(OUTC, "13_camadas_construtivas.svg"))
    camadas_construtivas("zenith").save(os.path.join(OUTZ, "13_camadas_construtivas.svg"))
    print("exploded ok")

if __name__ == "__main__":
    build()

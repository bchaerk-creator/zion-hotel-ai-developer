# -*- coding: utf-8 -*-
"""Isométricas sombreadas (algoritmo do pintor) e isométricas estruturais em SVG para Casulo, Safari e Lodge."""
import math, os
import numpy as np
from geometry import Cocoon, Zenith, Lodge
from svgkit import *

C, Z, L = Cocoon(), Zenith(), Lodge()
VIEW = np.array([-1.0, -1.0, 1.0]) / math.sqrt(3)     # direção para o observador (mundo)
LIGHT = np.array([-0.35, -0.75, 0.75]); LIGHT /= np.linalg.norm(LIGHT)

class Scene:
    def __init__(self, sheet, scale, ox, oy):
        self.sh, self.s, self.ox, self.oy = sheet, scale, ox, oy
        self.faces = []   # (depth, pts2d, color, opacity, stroke)
        self.lines = []   # (depth, p2d_a, p2d_b, color, width, dash)
        self.pre = []     # desenhado antes de tudo (sombra do solo)
    def proj(self, p):
        return iso_project(p, self.s, self.ox, self.oy)
    def tri(self, a, b, c, color, opacity=1.0, stroke=None, shade_on=True, two_sided=True):
        a, b, c = np.array(a), np.array(b), np.array(c)
        n = np.cross(b - a, c - a); ln = np.linalg.norm(n)
        if ln < 1e-12: return
        n /= ln
        if two_sided and np.dot(n, VIEW) < 0: n = -n
        k = 0.6 + 0.4 * max(0.0, float(np.dot(n, LIGHT))) if shade_on else 1.0
        P = [self.proj(p) for p in (a, b, c)]
        depth = sum(p[2] for p in P) / 3
        self.faces.append((depth, [(p[0], p[1]) for p in P], shade(color, k), opacity, stroke))
    def quad(self, a, b, c, d, color, opacity=1.0, stroke=None, shade_on=True):
        a, b, c, d = [np.array(p) for p in (a, b, c, d)]
        n = np.cross(b - a, c - a); ln = np.linalg.norm(n)
        if ln < 1e-12: return
        n /= ln
        if np.dot(n, VIEW) < 0: n = -n
        k = 0.6 + 0.4 * max(0.0, float(np.dot(n, LIGHT))) if shade_on else 1.0
        P = [self.proj(p) for p in (a, b, c, d)]
        depth = sum(p[2] for p in P) / 4
        self.faces.append((depth, [(p[0], p[1]) for p in P], shade(color, k), opacity, stroke))
    def box(self, x1, x2, y1, y2, z1, z2, color, opacity=1.0, stroke=None):
        v = lambda i, j, k: ((x2 if i else x1), (y2 if j else y1), (z2 if k else z1))
        # apenas faces visíveis (viewer em -x, -y, +z)
        self.quad(v(0,0,0), v(0,1,0), v(0,1,1), v(0,0,1), color, opacity, stroke)   # x1
        self.quad(v(0,0,0), v(1,0,0), v(1,0,1), v(0,0,1), color, opacity, stroke)   # y1
        self.quad(v(0,0,1), v(1,0,1), v(1,1,1), v(0,1,1), color, opacity, stroke)   # topo
        if opacity < 1.0:
            self.quad(v(1,0,0), v(1,1,0), v(1,1,1), v(1,0,1), color, opacity, stroke)
            self.quad(v(0,1,0), v(1,1,0), v(1,1,1), v(0,1,1), color, opacity, stroke)
    def cylinder(self, x, y, z1, z2, r, color, n=18, opacity=1.0):
        pts = [(x + r * math.cos(2 * math.pi * i / n), y + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
        for i in range(n):
            (ax, ay), (bx, by) = pts[i], pts[(i + 1) % n]
            self.quad((ax, ay, z1), (bx, by, z1), (bx, by, z2), (ax, ay, z2), color, opacity)
        for i in range(1, n - 1):
            self.tri((pts[0][0], pts[0][1], z2), (pts[i][0], pts[i][1], z2), (pts[i + 1][0], pts[i + 1][1], z2), color, opacity)
    def mesh(self, verts, faces, color, opacity=1.0, stroke=None):
        V = np.array(verts)
        for f in faces:
            self.tri(V[f[0]], V[f[1]], V[f[2]], color, opacity, stroke)
    def polyline(self, pts, color, width=1.0, dash=None, on_top=False):
        P = [self.proj(p) for p in pts]
        for a, b in zip(P[:-1], P[1:]):
            d = 1e9 if on_top else (a[2] + b[2]) / 2
            self.lines.append((d, (a[0], a[1]), (b[0], b[1]), color, width, dash))
    def render(self):
        items = [("f", f[0], f) for f in self.faces] + [("l", l[0], l) for l in self.lines]
        items.sort(key=lambda t: t[1])
        out = list(self.pre)
        for kind, depth, it in items:
            if kind == "f":
                _, pts, col, op, st = it
                d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
                stroke = f'stroke="{st}" stroke-width="0.35"' if st else f'stroke="{col}" stroke-width="0.5" stroke-opacity="{op}"'
                out.append(f'<polygon points="{d}" fill="{col}" fill-opacity="{op}" {stroke} stroke-linejoin="round"/>')
            else:
                _, a, b, col, w, dash = it
                ds = f' stroke-dasharray="{dash}"' if dash else ""
                out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-width="{w}"{ds} stroke-linecap="round"/>')
        self.sh.add("\n".join(out))

FURN_COLORS = dict(bed="#F5F1EA", pillow="#FFFFFF", table="#A8865E", cabinet="#A8865E", sofa="#CDBFA3", chair="#CDBFA3",
                   vanity="#E8E4DC", wc="#F4F4F2", shower="#D8D6CF", tub="#F7F7F5", wall="#E6DCC8", totem="#A8865E",
                   bench="#A8865E", hvac="#D9D9D6", condenser="#D9D9D6", ceiling="#E8DCC6")

def add_furniture(sc, items, skip=("opening", "glass", "ceiling")):
    for f in items:
        if f["kind"] in skip: continue
        col = FURN_COLORS.get(f["kind"], "#CCCCCC")
        if "r" in f: sc.cylinder(f["x"], f["y"], f["z1"], f["z2"], f["r"], col)
        else: sc.box(f["x1"], f["x2"], f["y1"], f["y2"], f["z1"], f["z2"], col)

def ground_shadow(sc, cx, cy, rx, ry):
    n = 48
    pts = [sc.proj((cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n), -0.02)) for i in range(n)]
    d = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
    sc.pre.append(f'<polygon points="{d}" fill="#DCCFBF" fill-opacity="0.55" stroke="none"/>')

# ------------------------------------------------------------------ CASULO
def cocoon_iso(structural=False):
    sh = Sheet(1600, 1000)
    sh.header("Zion Casulo · " + ("Estudo da estrutura metálica (isométrica)" if structural else "Vista isométrica"),
              "Projeção isométrica a partir da frente e da lateral direita · sem escala" + (" · membrana a 15% para leitura dos arcos, terças e espinha" if structural else ""))
    sc = Scene(sh, 78, 760, 640)
    ground_shadow(sc, 3.6, 0, 7.6, 4.5)
    D = C.DECK
    sc.box(D["x1"], D["x2"], D["y1"], D["y2"], -0.2, 0.0, "#B99A73")
    for i in range(3):
        sc.box(D["x1"] - 0.3 * (i + 1), D["x1"] - 0.3 * i, -1.2, 1.2, -0.2, -0.05 * (i + 1) - 0.0, "#B99A73")
    # piso interno (visível pela fachada)
    fl = C.floor_outline(40)
    for i in range(1, len(fl) - 1):
        sc.tri((fl[0][0], fl[0][1], 0), (fl[i][0], fl[i][1], 0), (fl[i + 1][0], fl[i + 1][1], 0), "#C9AA7D", shade_on=False)
    add_furniture(sc, C.furniture())
    m = C.shell_mesh(52, 26)
    op = 0.15 if structural else 1.0
    sc.mesh(m["vertices"], m["membrane"], "#EDE6D6", op)
    sc.mesh(m["vertices"], m["glass"], "#9FB7C2", 0.45 if not structural else 0.15)
    # Bico em balanço sobre o deck (membrana + cumeeira + bordas + costela + tirantes)
    bm = C.bico_mesh(24, 8); sc.mesh(bm["vertices"], bm["faces"], "#EDE6D6", op)
    bx = C.bico_export()
    sc.polyline(bx["ridge"], "#3A3B3A", 2.6 if structural else 1.6)
    for e in bx["edges"]: sc.polyline(e, "#3A3B3A", 2.0 if structural else 1.4)
    if structural:
        for rb in bx["ribs"]: sc.polyline(rb, "#6B6B6B", 1.3)
        for t in bx["ties"]: sc.polyline(t, "#8B714E", 0.9, "4 3")
    # fachada de vidro (leque)
    gr = C.glass_ring(48)
    cen = np.mean(np.array(gr), axis=0)
    for a, b in zip(gr[:-1], gr[1:]):
        sc.tri(cen, a, b, "#9FB7C2", 0.35, shade_on=False)
    # montantes
    for yy in (-1.6, -0.5, 0.5, 1.6):
        zt = C.ZC + (C.b(C.X_GLASS) - 0.06) * math.sqrt(max(0, 1 - (yy / (C.a(C.X_GLASS) - 0.06)) ** 2))
        sc.polyline([(C.shear(C.X_GLASS, 0), yy, 0), (C.shear(C.X_GLASS, zt), yy, zt)], "#3A3B3A", 1.6)
    sc.polyline([(C.shear(C.X_GLASS, 2.4), y, 2.4) for y in (-2.3, 2.3)], "#3A3B3A", 1.4)
    # anéis e estrutura
    sc.polyline(C.front_ring(60), "#3A3B3A", 3.0 if structural else 2.2)
    sc.polyline(gr, "#6B5B45", 1.6)
    if structural:
        for i, a in enumerate(C.arches()):
            sc.polyline(a["pts"], "#3A3B3A", 2.6)
            top = a["pts"][len(a["pts"]) // 2]
            p = sc.proj(top); sh.text_px(p[0], p[1] - 10, f"A{i}", size=11, weight=700, fill=EARTH)
        for pl in C.purlins(40):
            sc.polyline(pl, "#6B6B6B", 1.3)
        # espinha (treliça) e cabos em X
        x1, x2, ht = C.SPINE
        for th in (math.pi / 2 - ht, math.pi / 2 + ht):
            sc.polyline([C.section_point(x, th, 0.0) for x in np.linspace(x1, x2, 20)], "#3A3B3A", 1.8)
        for (xa, xb) in [(0.45, 1.65), (6.45, 7.65)]:
            for th in (0.35, math.pi - 0.35):
                pa = C.section_point(xa, th); pb = C.section_point(xb, th + 0.5); pc = C.section_point(xa, th + 0.5); pd = C.section_point(xb, th)
                sc.polyline([pa, pb], "#8B714E", 0.9, "4 3"); sc.polyline([pc, pd], "#8B714E", 0.9, "4 3")
        # trilhos de base
        sc.polyline([(x, -C.floor_hw(x), 0) for x in np.linspace(C.X_GLASS, C.X_FLOOR_END - 0.05, 40)], "#3A3B3A", 2.0)
        sc.polyline([(x, C.floor_hw(x), 0) for x in np.linspace(C.X_GLASS, C.X_FLOOR_END - 0.05, 40)], "#3A3B3A", 2.0)
    else:
        for w in C.WINDOWS:
            wo = [C.section_point(x, th, 0.07) for (x, th) in [(w["xc"] + w["lx"] * ((abs(math.cos(a)) ** 1.5 + abs(math.sin(a)) ** 1.5) ** (-1 / 1.5)) * math.cos(a), w["tc"] + w["lt"] * ((abs(math.cos(a)) ** 1.5 + abs(math.sin(a)) ** 1.5) ** (-1 / 1.5)) * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 41)]]
            sc.polyline(wo, "#8B6B4A", 2.4)
    sc.render()
    # legenda
    if structural:
        items = [(1, "Anel A0 Ø101,6 + Bico: cumeeira Ø114,3 em balanço 2,40 m, bordas Ø60,3, costela, 2 tirantes"), (2, "Arcos elípticos A1 a A7 Ø88,9 x 3,6 mm, 3 segmentos com luvas"),
                 (3, "7 terças longitudinais Ø48,3 x 3,0 em trechos de 1,20 m"), (4, "Espinha de Luz: treliça plana 300 mm sob 4 painéis de vidro"),
                 (5, "Cabos em X Ø8 inox nos vãos A0-A1 e A5-A6"), (6, "Trilhos de base 100 x 50 x 3 curvados, chumbados ao piso"),
                 (7, "Quadro da cauda Ø60,3 + 3 barras"), (8, "Peso da estrutura metálica: ≈ 1.140 kg de aço + 200 kg de alumínio")]
        sh.legend(60, 720, items, size=12)
    else:
        items = [(1, "Concha em membrana PVDF tensionada sobre 8 arcos elípticos"), (2, "Bico: membrana em balanço 2,40 m sobre o deck, ponta erguida a 4,42 m"),
                 (3, "Espinha de Luz na cumeeira (4,70 m)"), (4, "6 Janelas Olho em lente com requadro de madeira"),
                 (5, "Deck frontal 4,60 x 6,50 m em cumaru"), (6, "Cauda afilada com a banheira e a condensadora oculta")]
        sh.legend(60, 760, items, size=12)
    sh.title_block("ZION CASULO", "Estudo da estrutura metálica" if structural else "Vista isométrica", "sem escala", "12/27" if structural else "08/27",
                   "Arcos, terças, espinha e contraventamento" if structural else "Volumetria do casulo com deck e fachada panorâmica")
    return sh

# ------------------------------------------------------------------ SAFARI
def zenith_iso(structural=False):
    sh = Sheet(1600, 1000)
    sh.header("Zion Safari · " + ("Estudo da estrutura metálica (isométrica)" if structural else "Vista isométrica"),
              "Projeção isométrica a partir da frente e da lateral direita · sem escala" + (" · membrana a 15% para leitura de mastros, coroas, anel de beiral e postes" if structural else ""))
    sc = Scene(sh, 66, 780, 660)
    ground_shadow(sc, 4.2, 0.2, 8.2, 5.0)
    D, Wk = Z.DECK, Z.WALK
    sc.box(D["x1"], D["x2"], D["y1"], D["y2"], -0.2, 0.0, "#B99A73")
    sc.box(Wk["x1"], Wk["x2"], Wk["y1"], Wk["y2"], -0.2, 0.0, "#B99A73")
    for i in range(3):
        sc.box(D["x1"] - 0.3 * (i + 1), D["x1"] - 0.3 * i, -1.2, 1.2, -0.2, -0.05 * (i + 1), "#B99A73")
    H = Z.HOTTUB
    sc.cylinder(H["x"], H["y"], 0.0, 0.55, H["r"], "#DDD6C8")
    sc.cylinder(H["x"], H["y"], 0.0, 0.5, H["r"] - 0.1, "#9FC3CC")
    # piso
    sc.box(0.05, 9.45, -2.65, 2.65, -0.05, 0.0, "#C9AA7D")
    add_furniture(sc, Z.furniture())
    # paredes
    h = Z.H_WALL
    for w in Z.walls():
        (xa, ya), (xb, yb) = w["p1"], w["p2"]
        if w["kind"] == "glass":
            sc.quad((xa, ya, 0), (xb, yb, 0), (xb, yb, h), (xa, ya, h), "#9FB7C2", 0.35 if not structural else 0.15, stroke="#6B7C84")
        elif w["kind"] == "wood":
            sc.quad((xa, ya, 0), (xb, yb, 0), (xb, yb, h), (xa, ya, h), "#B08A5E", 1.0 if not structural else 0.25)
        else:
            # janela: leve deslocamento para fora
            dx = -0.02 if abs(xa - xb) < 1e-6 and xa > 5 else (0.0)
            dy = 0.02 if ya > 0 else 0.0
            if abs(xa - xb) < 1e-6: dx = 0.02
            sc.quad((xa + dx, ya + dy, w["z1"]), (xb + dx, yb + dy, w["z1"]), (xb + dx, yb + dy, w["z2"]), (xa + dx, ya + dy, w["z2"]), "#9FB7C2", 0.6)
    # anel de beiral
    for (a, b, c, d) in [(0, 9.5, -2.8, -2.65), (0, 9.5, 2.65, 2.8), (-0.05, 0.1, -2.8, 2.8), (9.4, 9.55, -2.8, 2.8)]:
        sc.box(a, b, c, d, 2.75, 2.9, "#3A3B3A")
    # cobertura
    rm = Z.roof_mesh(44, 26)
    sc.mesh(rm["vertices"], rm["faces"], "#EDE6D6", 0.15 if structural else 1.0)
    # cabos de borda (contorno recortado)
    x0, x1, y0, y1 = Z.roof_bounds()
    edge = [(x, y0, Z.edge_height(x, y0)) for x in np.linspace(x0, x1, 40)]
    sc.polyline(edge, "#3A3B3A", 1.4)
    edge = [(x0, y, Z.edge_height(x0, y)) for y in np.linspace(y0, y1, 40)]
    sc.polyline(edge, "#3A3B3A", 1.4)
    # postes externos
    for (px, py) in Z.posts():
        top = Z.edge_height(px, py) if (abs(px - x0) < 1e-6 or abs(px - x1) < 1e-6 or abs(abs(py) - y1) < 1e-6) else Z.Z_EDGE
        lean = 0.12
        dx = -lean if px < 0 else (lean if px > 9 else 0); dy = -lean if py < 0 else (lean if py > 0 else 0)
        sc.polyline([(px, py, -0.05), (px + dx, py + dy, top)], "#3A3B3A", 3.2)
        # estai
        sc.polyline([(px + dx, py + dy, top), (px + dx * 8, py + dy * 8, -0.05)], "#8B714E", 0.8, "4 3")
    # mastros, coroas, anéis
    for mst in Z.masts():
        sc.polyline([(mst["x"], mst["y"], 0), (mst["x"], mst["y"], mst["z2"])], "#3A3B3A", 4.0 if structural else 2.0, on_top=structural)
    for cr in Z.crowns():
        for arm in cr["arms"]:
            sc.polyline(arm, "#3A3B3A", 2.2, on_top=structural)
        sc.polyline(cr["ring"], "#3A3B3A", 2.4, on_top=structural)
    if structural:
        for (cx, cy) in Z.columns():
            sc.polyline([(cx, cy, 0), (cx, cy, 2.9)], "#3A3B3A", 3.0, on_top=True)
        # quadro do piso: vigas
        for yy in (-2.7, -1.35, 0.0, 1.35, 2.7):
            sc.polyline([(-3.0, yy, -0.12), (9.5, yy, -0.12)], "#6B6B6B", 1.4)
        for xx in (-3.0, -0.6, 1.8, 4.2, 6.6, 9.5):
            sc.polyline([(xx, -3.4 if xx < 0 else -2.7, -0.12), (xx, 3.4 if xx < 0 else 3.5, -0.12)], "#6B6B6B", 1.4)
    sc.render()
    if structural:
        items = [(1, "Mastro M1 Ø139,7 x 4,5 (5,05 m) + coroa de 3 braços + anel Ø1,20 com óculo"),
                 (2, "Mastro M2 Ø114,3 x 4,0 (4,00 m) + coroa + anel Ø0,70 com chaminé"),
                 (3, "Anel de beiral 150 x 100 x 4,0 em 6 segmentos sobre 10 pilares Ø101,6"),
                 (4, "7 postes externos Ø76,1 inclinados 8°, estaiados a estacas de tração"),
                 (5, "Cabo de borda Ø12 inox em bolsa, esticadores nos postes"),
                 (6, "Quadro de piso: vigas U 150 x 60 sobre estacas helicoidais"),
                 (7, "Painéis SIP 100 mm formam diafragma rígido"), (8, "Peso da estrutura metálica: ≈ 1.230 kg de aço + 95 kg de alumínio")]
        sh.legend(60, 720, items, size=12)
    else:
        items = [(1, "Dois cumes deslocados em diagonal: 5,80 m e 4,60 m"), (2, "Membrana em balanço 2,40 m sobre o terraço e 1,00 m nas laterais"),
                 (3, "Fachada de vidro 5,40 x 2,75 e vidro lateral da suíte"), (4, "Painéis ripados nas faces de serviço"),
                 (5, "Terraço 3,00 x 6,80 com hidromassagem e passarela lateral"), (6, "Óculo do Zênite sobre a cama; Respiro sobre o café")]
        sh.legend(60, 760, items, size=12)
    sh.title_block("ZION SAFARI", "Estudo da estrutura metálica" if structural else "Vista isométrica", "sem escala", "12/27" if structural else "08/27",
                   "Mastros, coroas, anel de beiral, postes e cabos" if structural else "Volumetria dos dois cumes sobre o corpo de vidro e madeira")
    return sh

# ------------------------------------------------------------------ LODGE: geometria auxiliar
LV = L.vertices(); LR = L.r_corner()
LVO = L.vertices(LR + L.OVER / math.cos(math.pi / L.N))          # vértices do beiral da membrana (balanço 0,90)
LVD = L.vertices(LR + L.DECK_D / math.cos(math.pi / L.N))        # vértices externos do deck
LZ_EDGE = L.Z_EAVE - 0.35                                        # cota da borda da membrana
WOOD_COL = "#8B6B4A"; SAIL_COL = "#E4D9C3"

def lodge_halfwidth(t):
    """meia-largura do octógono (faces a 3,40 dos eixos; |x|+|y| <= 3,40·√2) numa coordenada t."""
    return max(0.0, min(L.F / 2, L.F / 2 * math.sqrt(2) - abs(t)))

def _seg_at_x(p, q, x):
    t = (x - p[0]) / (q[0] - p[0]); return p[1] + t * (q[1] - p[1])

def lodge_girders():
    """grelha de vigas U 150 x 60 sob o piso e o deck: lista de segmentos (x1, y1, x2, y2)."""
    S = []
    for x in (-2.4, 0.0, 2.4):
        hw = lodge_halfwidth(x); S.append((x, -hw, x, hw))
    for y in (-2.55, -0.85, 0.85, 2.55):
        hl = lodge_halfwidth(y); S.append((-hl, y, hl, y))
    for i in range(L.N):
        j = (i + 1) % L.N; S.append((LV[i][0], LV[i][1], LV[j][0], LV[j][1]))
    for i in (2, 3, 4, 5):
        S.append((LV[i][0], LV[i][1], LVD[i][0], LVD[i][1]))
    for i in (2, 3, 4):
        S.append((LVD[i][0], LVD[i][1], LVD[i + 1][0], LVD[i + 1][1]))
    yy = _seg_at_x(LVD[3], LVD[2], -4.7)
    S.append((-4.7, -yy, -4.7, yy))
    for y in (-1.8, 1.8):
        S.append((-lodge_halfwidth(y), y, LVD[3][0], y))
    return S

def lodge_deck(sc, dz, color="#B99A73", z1=-0.2, stairs=True, opacity=1.0):
    """deck em três faces (trapézios) com a escada frontal."""
    nb = 16   # tábuas paralelas a cada face (ordenação de profundidade local)
    for i in (2, 3, 4):
        j = i + 1
        a, b, c, d = LV[i], LV[j], LVD[j], LVD[i]
        for k in range(nb):
            t0, t1 = k / nb, (k + 1) / nb
            p0 = (a[0] + (d[0] - a[0]) * t0, a[1] + (d[1] - a[1]) * t0); p1 = (a[0] + (d[0] - a[0]) * t1, a[1] + (d[1] - a[1]) * t1)
            q0 = (b[0] + (c[0] - b[0]) * t0, b[1] + (c[1] - b[1]) * t0); q1 = (b[0] + (c[0] - b[0]) * t1, b[1] + (c[1] - b[1]) * t1)
            sc.quad((p0[0], p0[1], dz), (q0[0], q0[1], dz), (q1[0], q1[1], dz), (p1[0], p1[1], dz), color if k % 2 else shade(color, 0.95), opacity)
        sc.quad((d[0], d[1], z1 + dz), (c[0], c[1], z1 + dz), (c[0], c[1], dz), (d[0], d[1], dz), color, opacity)
    for i in (2, 5):
        a, b = LV[i], LVD[i]
        sc.quad((a[0], a[1], z1 + dz), (b[0], b[1], z1 + dz), (b[0], b[1], dz), (a[0], a[1], dz), color, opacity)
    if stairs:
        x0 = LVD[3][0]
        for i in range(3):
            sc.box(x0 - 0.3 * (i + 1), x0 - 0.3 * i, -1.2, 1.2, z1 + dz, -0.05 * (i + 1) + dz, color, opacity)

def lodge_floor(sc, dz, color="#C9AA7D", outline=False):
    for i in range(1, L.N - 1):
        sc.tri((LV[0][0], LV[0][1], dz), (LV[i][0], LV[i][1], dz), (LV[i + 1][0], LV[i + 1][1], dz), color, shade_on=False)
    if outline:
        sc.polyline([(x, y, dz + 0.005) for (x, y) in LV] + [(LV[0][0], LV[0][1], dz + 0.005)], GREEN, 0.7)

def _outward(p1, p2):
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2; ln = math.hypot(mx, my)
    return (mx / ln, my / ln)

def lodge_walls(sc, dz, opacity=1.0, glass_op=0.35, slats=True, mullions=True):
    """cinco faces de vidro, três opacas ripadas, fresta alta e porta de correr frontal."""
    for w in L.walls():
        (xa, ya), (xb, yb) = w["p1"], w["p2"]; z1, z2 = w["z1"] + dz, w["z2"] + dz
        if w["kind"] == "glass":
            sc.quad((xa, ya, z1), (xb, yb, z1), (xb, yb, z2), (xa, ya, z2), "#9FB7C2", glass_op * opacity, stroke="#6B7C84")
            if mullions:
                for t in (1 / 3, 2 / 3):
                    x, y = xa + (xb - xa) * t, ya + (yb - ya) * t
                    sc.polyline([(x, y, z1), (x, y, z2)], STEEL, 1.1)
        elif w["kind"] == "wood":
            sc.quad((xa, ya, z1), (xb, yb, z1), (xb, yb, z2), (xa, ya, z2), "#B08A5E", opacity)
            if slats and opacity >= 0.99:
                nx, ny = _outward(w["p1"], w["p2"])
                for k in range(1, int((z2 - z1) / 0.12)):
                    z = z1 + 0.12 * k
                    sc.polyline([(xa + 0.012 * nx, ya + 0.012 * ny, z), (xb + 0.012 * nx, yb + 0.012 * ny, z)], "#8B6B4A", 0.5)
        elif w["kind"] == "window":
            nx, ny = _outward(w["p1"], w["p2"])
            sc.quad((xa + 0.03 * nx, ya + 0.03 * ny, z1), (xb + 0.03 * nx, yb + 0.03 * ny, z1), (xb + 0.03 * nx, yb + 0.03 * ny, z2), (xa + 0.03 * nx, ya + 0.03 * ny, z2), "#9FB7C2", 0.6)
    if mullions:
        # porta de correr PC1 2,00 x 2,40 na face frontal (x = -3,40)
        xf = LV[3][0] + 0.01; d = L.DOOR
        sc.polyline([(xf, d["y1"], dz), (xf, d["y1"], d["h"] + dz), (xf, d["y2"], d["h"] + dz), (xf, d["y2"], dz)], GREEN, 1.0)
        sc.polyline([(xf, 0.0, dz), (xf, 0.0, d["h"] + dz)], GREEN, 0.7)

def lodge_columns(sc, dz, wood=True, on_top=False, z2=None):
    z2 = L.Z_EAVE if z2 is None else z2
    for (x, y) in LV:
        if wood: sc.cylinder(x, y, dz, z2 + dz, 0.09, WOOD_COL, n=10)
        else:
            sc.polyline([(x, y, dz), (x, y, z2 + dz)], STEEL, 3.0, on_top=on_top)
            sc.box(x - 0.11, x + 0.11, y - 0.11, y + 0.11, dz, 0.012 + dz, "#5A5B5A")

def beam(sc, p1, p2, z1, z2, w, color, opacity=1.0, n=6):
    """prisma retangular horizontal (viga) entre p1 e p2, largura w, entre as cotas z1 e z2.
    Subdividida em n trechos para que a ordenação de profundidade (pintor) seja local."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]; ln = math.hypot(dx, dy)
    nx, ny = -dy / ln * w / 2, dx / ln * w / 2
    for k in range(n):
        q1 = (p1[0] + dx * k / n, p1[1] + dy * k / n); q2 = (p1[0] + dx * (k + 1) / n, p1[1] + dy * (k + 1) / n)
        a = (q1[0] + nx, q1[1] + ny); b = (q2[0] + nx, q2[1] + ny); c = (q2[0] - nx, q2[1] - ny); d = (q1[0] - nx, q1[1] - ny)
        sc.quad((a[0], a[1], z2), (b[0], b[1], z2), (c[0], c[1], z2), (d[0], d[1], z2), color, opacity)
        sc.quad((a[0], a[1], z1), (b[0], b[1], z1), (b[0], b[1], z2), (a[0], a[1], z2), color, opacity)
        sc.quad((d[0], d[1], z1), (c[0], c[1], z1), (c[0], c[1], z2), (d[0], d[1], z2), color, opacity)
        if k == 0: sc.quad((a[0], a[1], z1), (d[0], d[1], z1), (d[0], d[1], z2), (a[0], a[1], z2), color, opacity)
        if k == n - 1: sc.quad((b[0], b[1], z1), (c[0], c[1], z1), (c[0], c[1], z2), (b[0], b[1], z2), color, opacity)

def lodge_eave_ring(sc, dz, color=STEEL):
    for i in range(L.N):
        beam(sc, LV[i], LV[(i + 1) % L.N], L.Z_EAVE - 0.15 + dz, L.Z_EAVE + dz, 0.10, color)

def lodge_rafters(sc, dz, color=STEEL, width=2.2, on_top=False):
    for r in L.rafters():
        sc.polyline([(p[0], p[1], p[2] + dz) for p in r], color, width, on_top=on_top)

def lodge_lantern(sc, dz, glass=True, glass_op=0.45, cap=True, ring=True, mullions=True):
    r = L.R_LANTERN; z1 = L.Z_LANTERN + dz; z2 = z1 + 0.45; zt = L.Z_TOP + dz
    if glass: sc.cylinder(0, 0, z1, z2, r, "#9FB7C2", n=16, opacity=glass_op)
    if mullions:
        for k in range(8):
            a = math.pi / 8 + k * math.pi / 4
            sc.polyline([(r * math.cos(a), r * math.sin(a), z1), (r * math.cos(a), r * math.sin(a), z2)], STEEL, 1.2)
    if ring:
        sc.polyline([(r * math.cos(2 * math.pi * i / 32), r * math.sin(2 * math.pi * i / 32), z1) for i in range(33)], STEEL, 2.4)
    if cap: sc.cylinder(0, 0, z2, zt, r + 0.12, "#4A4B4A", n=16)

def lodge_membrane(sc, dz, opacity=1.0, seams=True, edge=True, nr=12, na=64):
    rm = L.roof_mesh(nr, na)
    sc.mesh([(v[0], v[1], v[2] + dz) for v in rm["vertices"]], rm["faces"], MEMB, opacity)
    if seams and opacity > 0.5:
        for (x, y) in LV:
            ang = math.atan2(y, x); re = LR + L.OVER / math.cos(math.pi / L.N)
            pts = [((L.R_LANTERN + (re - L.R_LANTERN) * t) * math.cos(ang), (L.R_LANTERN + (re - L.R_LANTERN) * t) * math.sin(ang),
                    (L.roof_z(L.R_LANTERN + (re - L.R_LANTERN) * t) if t < 1 else LZ_EDGE) + 0.02 + dz) for t in np.linspace(0, 1, 16)]
            sc.polyline(pts, shade(MEMB, 0.82), 0.9)
    if edge:
        sc.polyline([(x, y, LZ_EDGE + dz) for (x, y) in LVO] + [(LVO[0][0], LVO[0][1], LZ_EDGE + dz)], STEEL, 1.3)

def lodge_liner_mesh(drop=0.3, nr=8, na=48, r_in=None):
    """forro cônico interno (sem balanço): mesma lei da membrana, rebaixada 'drop'."""
    r0 = (L.R_LANTERN + 0.05) if r_in is None else r_in
    verts, faces = [], []
    for i in range(nr + 1):
        t = i / nr
        for j in range(na):
            ang = 2 * math.pi * j / na
            k = (ang - math.pi / 8) % (2 * math.pi / L.N) - math.pi / L.N
            r_edge = (LR - 0.08) * math.cos(math.pi / L.N) / math.cos(k)
            r = r0 + (r_edge - r0) * t
            verts.append((r * math.cos(ang), r * math.sin(ang), L.roof_z(r) - drop))
    for i in range(nr):
        for j in range(na):
            a0 = i * na + j; a1 = i * na + (j + 1) % na; b0 = a0 + na; b1 = a1 + na
            faces.append((a0, b0, b1)); faces.append((a0, b1, a1))
    return dict(vertices=verts, faces=faces)

def lodge_sail_curves(n=12, bow=0.3, bow_side=0.22):
    """quatro curvas de borda da vela (Coons): u = poste -> beiral, v = -y -> +y."""
    P = L.sail_posts(); zp = L.SAIL["z_post"]
    A = (P[1][0], P[1][1], zp); B = (LVO[3][0], LVO[3][1], LZ_EDGE)     # lado +y
    D = (P[0][0], P[0][1], zp); C = (LVO[4][0], LVO[4][1], LZ_EDGE)     # lado -y
    def curve(p, q, inward, k):
        return [tuple(p[i] + (q[i] - p[i]) * t + inward[i] * k * math.sin(math.pi * t) for i in range(3)) for t in np.linspace(0, 1, n + 1)]
    side_m = curve(D, C, (0, 1, 0), bow_side)      # v = 0 (y negativo), bojo para +y
    side_p = curve(A, B, (0, -1, 0), bow_side)     # v = 1 (y positivo), bojo para -y
    front = curve(D, A, (1, 0, 0), bow)            # u = 0 (postes), bojo para +x
    back = curve(C, B, (0, 0, 0), 0.0)             # u = 1 (beiral), reta
    return side_m, side_p, front, back

def lodge_sail_mesh(n=12, sag=0.10):
    side_m, side_p, front, back = lodge_sail_curves(n)
    P00, P10, P01, P11 = side_m[0], side_m[-1], side_p[0], side_p[-1]
    verts = []
    for i in range(n + 1):
        u = i / n
        for j in range(n + 1):
            v = j / n
            p = [(1 - v) * side_m[i][k] + v * side_p[i][k] + (1 - u) * front[j][k] + u * back[j][k]
                 - ((1 - u) * (1 - v) * P00[k] + u * (1 - v) * P10[k] + (1 - u) * v * P01[k] + u * v * P11[k]) for k in range(3)]
            p[2] -= sag * math.sin(math.pi * u) * math.sin(math.pi * v)
            verts.append(tuple(p))
    faces = []
    for i in range(n):
        for j in range(n):
            a0 = i * (n + 1) + j; a1 = a0 + 1; b0 = a0 + n + 1; b1 = b0 + 1
            faces.append((a0, b0, b1)); faces.append((a0, b1, a1))
    return dict(vertices=verts, faces=faces)

def lodge_sail(sc, dz, opacity=1.0, membrane=True, posts=True, cables=True, stays=True):
    side_m, side_p, front, back = lodge_sail_curves()
    if membrane:
        m = lodge_sail_mesh()
        sc.mesh([(v[0], v[1], v[2] + dz) for v in m["vertices"]], m["faces"], SAIL_COL, opacity)
    if cables:
        for cv in (side_m, side_p, front):
            sc.polyline([(p[0], p[1], p[2] + 0.01 + dz) for p in cv], STEEL, 1.2)
    if posts:
        for (px, py) in L.sail_posts():
            sc.polyline([(px, py, -0.05 + dz), (px, py, L.SAIL["z_post"] + dz)], STEEL, 3.0)
            if stays:
                sy = 1 if py > 0 else -1
                sc.polyline([(px, py, L.SAIL["z_post"] + dz), (px - 1.3, py + sy * 0.9, -0.05 + dz)], EARTH, 0.9, "4 3")

def lodge_bracing(sc, dz, color=EARTH):
    """cabos em X Ø8 nas três faces opacas."""
    for (i, j) in L.WALL_FACES:
        (xa, ya), (xb, yb) = LV[i], LV[j]
        sc.polyline([(xa, ya, 0.1 + dz), (xb, yb, L.Z_EAVE - 0.2 + dz)], color, 0.9, "4 3")
        sc.polyline([(xb, yb, 0.1 + dz), (xa, ya, L.Z_EAVE - 0.2 + dz)], color, 0.9, "4 3")

def lodge_piles(sc, dz):
    for (px, py) in L.piles():
        sc.cylinder(px, py, -0.6 + dz, -0.02 + dz, 0.045, STEEL, n=8)
        sc.box(px - 0.1, px + 0.1, py - 0.1, py + 0.1, -0.02 + dz, 0.0 + dz, "#5A5B5A")

def lodge_iso(structural=False):
    sh = Sheet(1600, 1000)
    sh.header("Zion Lodge · " + ("Estudo da estrutura metálica (isométrica)" if structural else "Vista isométrica"),
              "Projeção isométrica a partir da frente e da lateral direita · sem escala" + (" · membrana a 15% para leitura de pilares, anel de beiral, caibros e lanterna" if structural else ""))
    sc = Scene(sh, 68, 790, 590)
    ground_shadow(sc, -1.2, 0.0, 7.2, 6.2)
    if structural:
        lodge_piles(sc, 0.0)
        for (x1, y1, x2, y2) in lodge_girders():
            sc.polyline([(x1, y1, -0.12), (x2, y2, -0.12)], STEEL, 1.8)
        lodge_deck(sc, 0.0, stairs=True, opacity=0.35)
        lodge_floor(sc, 0.0, outline=True)
    else:
        lodge_deck(sc, 0.0)
        lodge_floor(sc, 0.0)
    add_furniture(sc, L.furniture())
    lodge_walls(sc, 0.0, opacity=1.0 if not structural else 0.25, glass_op=0.35 if not structural else 0.15, slats=not structural, mullions=not structural)
    lodge_columns(sc, 0.0, wood=not structural, on_top=structural)
    lodge_eave_ring(sc, 0.0)
    if structural:
        lodge_rafters(sc, 0.0, on_top=True, width=2.4)
        lodge_bracing(sc, 0.0)
        lodge_membrane(sc, 0.0, 0.15, seams=False, edge=True)
        lodge_lantern(sc, 0.0, glass=False, cap=False)
        lodge_sail(sc, 0.0, opacity=0.2)
    else:
        lodge_membrane(sc, 0.0, 1.0)
        lodge_lantern(sc, 0.0)
        lodge_sail(sc, 0.0)
    sc.render()
    if structural:
        items = [(1, "8 pilares Ø101,6 x 4,0 nos vértices (revestidos em madeira), h = 2,70 m"),
                 (2, "Anel de beiral 150 x 100 x 4,0 em 8 segmentos de 2,82 m, ligações parafusadas"),
                 (3, "8 caibros radiais Ø76,1 x 3,6 do anel de beiral ao anel da lanterna (4,60 m)"),
                 (4, "Anel de compressão da lanterna Ø1,50 (tubo 100 x 50) + 8 montantes do vidro"),
                 (5, "2 postes da vela Ø88,9 x 4,0 (2,40 m) estaiados; cabos de borda Ø10 inox"),
                 (6, "Cabos em X Ø8 inox nas três faces opacas (contraventamento)"),
                 (7, "Quadro de piso: vigas U 150 x 60 x 3,0 sobre 22 estacas helicoidais"),
                 (8, "Peso estimado da estrutura metálica: ≈ 1.400 kg de aço + 60 kg de alumínio")]
        sh.legend(60, 720, items, size=12)
    else:
        items = [(1, "Octógono de 6,80 m entre faces (38,3 m²) sobre 8 pilares em madeira"),
                 (2, "Membrana cônica em 8 gomos, balanço 0,90 m, lanterna de vidro no ápice (5,20 m)"),
                 (3, "Cinco faces de vidro (frente e laterais) com porta de correr 2,00 x 2,40"),
                 (4, "Três faces opacas ripadas: banho e cabeceira, fresta alta da banheira"),
                 (5, "Deck em três faces (2,60 m) com escada frontal"),
                 (6, "Vela de sombra sobre o deck em dois postes de 2,40 m")]
        sh.legend(60, 760, items, size=12)
    sh.title_block("ZION LODGE", "Estudo da estrutura metálica" if structural else "Vista isométrica", "sem escala", "12/27" if structural else "08/27",
                   "Pilares, anel de beiral, caibros, lanterna e vela" if structural else "Volumetria do octógono com membrana cônica, lanterna e deck")
    return sh

def build():
    oc = os.path.join(os.path.dirname(__file__), "..", "cocoon", "desenhos")
    oz = os.path.join(os.path.dirname(__file__), "..", "zenith", "desenhos")
    cocoon_iso(False).save(os.path.join(oc, "08_isometrica.svg"))
    cocoon_iso(True).save(os.path.join(oc, "12_estrutura_isometrica.svg"))
    zenith_iso(False).save(os.path.join(oz, "08_isometrica.svg"))
    zenith_iso(True).save(os.path.join(oz, "12_estrutura_isometrica.svg"))
    ol = os.path.join(os.path.dirname(__file__), "..", "lodge", "desenhos")
    os.makedirs(ol, exist_ok=True)
    lodge_iso(False).save(os.path.join(ol, "08_isometrica.svg"))
    lodge_iso(True).save(os.path.join(ol, "12_estrutura_isometrica.svg"))
    print("iso ok")

if __name__ == "__main__":
    build()

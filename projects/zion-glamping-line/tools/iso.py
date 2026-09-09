# -*- coding: utf-8 -*-
"""Isométricas sombreadas (algoritmo do pintor) e isométricas estruturais em SVG para Cocoon e Zenith."""
import math, os
import numpy as np
from geometry import Cocoon, Zenith
from svgkit import *

C, Z = Cocoon(), Zenith()
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

# ------------------------------------------------------------------ COCOON
def cocoon_iso(structural=False):
    sh = Sheet(1600, 1000)
    sh.header("Zion Cocoon · " + ("Estudo da estrutura metálica (isométrica)" if structural else "Vista isométrica"),
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
        items = [(1, "Anel frontal A0 Ø101,6 x 4,0 inclinado 8° (lábio)"), (2, "Arcos elípticos A1 a A7 Ø88,9 x 3,6 mm, 3 segmentos com luvas"),
                 (3, "7 terças longitudinais Ø48,3 x 3,0 em trechos de 1,20 m"), (4, "Espinha de Luz: treliça plana 300 mm sob 4 painéis de vidro"),
                 (5, "Cabos em X Ø8 inox nos vãos A0-A1 e A5-A6"), (6, "Trilhos de base 100 x 50 x 3 curvados, chumbados ao piso"),
                 (7, "Quadro da cauda Ø60,3 + 3 barras"), (8, "Peso da estrutura metálica: ≈ 1.140 kg de aço + 200 kg de alumínio")]
        sh.legend(60, 720, items, size=12)
    else:
        items = [(1, "Concha em membrana PVDF tensionada sobre 8 arcos elípticos"), (2, "Lábio frontal inclinado 8° protegendo a fachada de vidro"),
                 (3, "Espinha de Luz na cumeeira (4,70 m)"), (4, "6 Janelas Olho em lente com requadro de madeira"),
                 (5, "Deck frontal 4,60 x 6,50 m em cumaru"), (6, "Cauda afilada com a banheira e a condensadora oculta")]
        sh.legend(60, 760, items, size=12)
    sh.title_block("ZION COCOON", "Estudo da estrutura metálica" if structural else "Vista isométrica", "sem escala", "12/27" if structural else "08/27",
                   "Arcos, terças, espinha e contraventamento" if structural else "Volumetria do casulo com deck e fachada panorâmica")
    return sh

# ------------------------------------------------------------------ ZENITH
def zenith_iso(structural=False):
    sh = Sheet(1600, 1000)
    sh.header("Zion Zenith · " + ("Estudo da estrutura metálica (isométrica)" if structural else "Vista isométrica"),
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
    sh.title_block("ZION ZENITH", "Estudo da estrutura metálica" if structural else "Vista isométrica", "sem escala", "12/27" if structural else "08/27",
                   "Mastros, coroas, anel de beiral, postes e cabos" if structural else "Volumetria dos dois cumes sobre o corpo de vidro e madeira")
    return sh

def build():
    oc = os.path.join(os.path.dirname(__file__), "..", "cocoon", "desenhos")
    oz = os.path.join(os.path.dirname(__file__), "..", "zenith", "desenhos")
    cocoon_iso(False).save(os.path.join(oc, "08_isometrica.svg"))
    cocoon_iso(True).save(os.path.join(oc, "12_estrutura_isometrica.svg"))
    zenith_iso(False).save(os.path.join(oz, "08_isometrica.svg"))
    zenith_iso(True).save(os.path.join(oz, "12_estrutura_isometrica.svg"))
    print("iso ok")

if __name__ == "__main__":
    build()

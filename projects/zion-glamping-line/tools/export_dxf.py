# -*- coding: utf-8 -*-
"""Exporta o projeto arquitetônico para DXF (AutoCAD 2010) editável em CAD, a partir da geometria paramétrica.
Unidades: metros. Layers: EIXOS, PAREDES, ESQUADRIAS, MOBILIARIO, ESTRUTURA, COBERTURA, DECK, COTAS, TEXTO, 3D.
Arquivos gerados em <produto>/projeto/dxf/: planta baixa, planta estrutural, cobertura, cortes, fachadas e modelo 3D.
Uso: python3 export_dxf.py"""
import math, os
import numpy as np
import ezdxf
from ezdxf.enums import TextEntityAlignment
from geometry import Cocoon, Zenith, Lodge
from drawings_extra import cocoon_pile_grid, zenith_pile_grid, zenith_tension_piles

C, Z, L = Cocoon(), Zenith(), Lodge()
ROOT = os.path.join(os.path.dirname(__file__), "..")
LAYERS = [("EIXOS", 8, "CENTER"), ("PAREDES", 7, "CONTINUOUS"), ("ESQUADRIAS", 4, "CONTINUOUS"), ("MOBILIARIO", 9, "CONTINUOUS"), ("ESTRUTURA", 1, "CONTINUOUS"),
          ("COBERTURA", 3, "CONTINUOUS"), ("COBERTURA_OCULTA", 3, "HIDDEN"), ("DECK", 32, "CONTINUOUS"), ("FUNDACAO", 5, "CONTINUOUS"), ("COTAS", 2, "CONTINUOUS"),
          ("TEXTO", 7, "CONTINUOUS"), ("HACHURA", 8, "CONTINUOUS"), ("MEMBRANA_3D", 3, "CONTINUOUS"), ("VIDRO_3D", 4, "CONTINUOUS"), ("ACO_3D", 1, "CONTINUOUS")]

def new_doc():
    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 6   # metros
    for name, color, lt in LAYERS:
        if name not in doc.layers:
            doc.layers.add(name, color=color, linetype=lt if lt in doc.linetypes else "CONTINUOUS")
    if "ZION" not in doc.styles:
        doc.styles.add("ZION", font="arial.ttf")
    doc.dimstyles.new("ZION_M", dxfattribs={"dimtxt": 0.12, "dimasz": 0.08, "dimexo": 0.05, "dimexe": 0.06, "dimdec": 2, "dimdsep": ord(","), "dimtxsty": "ZION", "dimclrt": 2, "dimclrd": 2, "dimclre": 2, "dimtad": 1, "dimgap": 0.03})
    return doc

def pl(msp, pts, layer, close=False, lw=None):
    e = msp.add_lwpolyline([(p[0], p[1]) for p in pts], dxfattribs={"layer": layer}, close=close)
    if lw: e.dxf.const_width = lw
    return e

def rect(msp, x1, y1, x2, y2, layer):
    return pl(msp, [(x1, y1), (x2, y1), (x2, y2), (x1, y2)], layer, close=True)

def txt(msp, x, y, s, h=0.15, layer="TEXTO", align=TextEntityAlignment.MIDDLE_CENTER, rot=0):
    return msp.add_text(s, dxfattribs={"layer": layer, "height": h, "style": "ZION", "rotation": rot}).set_placement((x, y), align=align)

def dim_h(msp, x1, x2, y, off=0.6, txt_=None):
    d = msp.add_linear_dim(base=(x1, y + off), p1=(x1, y), p2=(x2, y), dimstyle="ZION_M", dxfattribs={"layer": "COTAS"}, text=txt_ or "<>")
    d.render()

def dim_v(msp, x, y1, y2, off=0.6, txt_=None):
    d = msp.add_linear_dim(base=(x + off, y1), p1=(x, y1), p2=(x, y2), angle=90, dimstyle="ZION_M", dxfattribs={"layer": "COTAS"}, text=txt_ or "<>")
    d.render()

def zion_mark(msp, x, y, size=0.6, layer="TEXTO"):
    """símbolo Z da Zion (anel + Z) com canto inferior esquerdo em (x, y), lado 'size' m."""
    from svgkit import zion_mark_lines
    (cx, cy, r), z = zion_mark_lines(size)
    msp.add_circle((x + cx, y + cy), r, dxfattribs={"layer": layer})
    e = msp.add_hatch(color=7, dxfattribs={"layer": layer}); e.paths.add_polyline_path([(x + px, y + py) for px, py in z], is_closed=True)
    pl(msp, [(x + px, y + py) for px, py in z], layer, close=True)

def title(msp, x, y, s):
    zion_mark(msp, x - 0.95, y - 0.35, 0.7)
    txt(msp, x, y, s, h=0.35, align=TextEntityAlignment.MIDDLE_LEFT)
    txt(msp, x, y - 0.32, "ZION GLAMPING COLLECTION · ZION HOTEL GROUP INTERNATIONAL", h=0.13, align=TextEntityAlignment.MIDDLE_LEFT)

def furniture_plan(msp, items):
    for it in items:
        if it["kind"] in ("ceiling", "hvac", "pillow", "opening"): continue
        if "r" in it:
            msp.add_circle((it["x"], it["y"]), it["r"], dxfattribs={"layer": "MOBILIARIO"})
        elif it["kind"] == "wall":
            rect(msp, it["x1"], it["y1"], it["x2"], it["y2"], "PAREDES")
            msp.add_hatch(color=8, dxfattribs={"layer": "HACHURA"}).paths.add_polyline_path([(it["x1"], it["y1"]), (it["x2"], it["y1"]), (it["x2"], it["y2"]), (it["x1"], it["y2"])], is_closed=True)
        elif it["kind"] == "glass":
            pl(msp, [(it["x1"], it["y1"]), (it["x2"], it["y2"])] if abs(it["x2"] - it["x1"]) < 0.06 else [(it["x1"], it["y1"]), (it["x2"], it["y1"])], "ESQUADRIAS")
        else:
            rect(msp, it["x1"], it["y1"], it["x2"], it["y2"], "MOBILIARIO")
            if it.get("name"): txt(msp, (it["x1"] + it["x2"]) / 2, (it["y1"] + it["y2"]) / 2, it["name"], h=0.07, layer="TEXTO")

# ============================================================================ CASULO
def cocoon_planta(msp, ox=0, oy=0, layout=True):
    floor = C.floor_outline(120)
    shell = [(x, -C.a(x)) for x in np.linspace(0.5, C.L, 120)] + [(x, C.a(x)) for x in np.linspace(C.L, 0.5, 120)]
    ring = [(x, y) for (x, y, z) in C.front_ring(80)]
    pl(msp, shell, "COBERTURA_OCULTA", close=True); pl(msp, ring, "COBERTURA")
    pl(msp, floor, "PAREDES", close=True)
    glass = [(x, y) for (x, y, z) in C.glass_ring(80) if z < 0.05]
    pl(msp, [(C.shear(C.X_GLASS, 0), -C.floor_hw(C.X_GLASS)), (C.shear(C.X_GLASS, 0), C.floor_hw(C.X_GLASS))], "ESQUADRIAS")
    D = C.DECK; rect(msp, D["x1"], D["y1"], D["x2"], D["y2"], "DECK")
    for i in range(1, 4): pl(msp, [(D["x1"] - 0.3 * i, D["y1"]), (D["x1"] - 0.3 * i, D["y2"])], "DECK")
    for w in C.WINDOWS:
        pts = [(x, y) for (x, y, z) in C.window_outline(w, 48)]
        pl(msp, pts, "ESQUADRIAS", close=True)
    x1, x2, ht = C.SPINE; hw = ht * C.B_MAX
    rect(msp, C.shear(x1, 4.15), -hw, C.shear(x2, 4.15), hw, "ESQUADRIAS")
    if layout: furniture_plan(msp, C.furniture())
    # eixos dos arcos
    for i, x in enumerate(C.ARCH_X):
        pl(msp, [(x, -3.9), (x, 3.9)], "EIXOS"); msp.add_circle((x, 4.15), 0.2, dxfattribs={"layer": "EIXOS"}); txt(msp, x, 4.15, f"A{i}", h=0.15)
    dim_h(msp, 0.45, 9.6, -3.6, -0.5, "9,60"); dim_h(msp, -3.7, 0.9, -3.6, -0.5, "4,60"); dim_v(msp, 10.2, -3.0, 3.0, 0.6, "6,00")
    for i in range(len(C.ARCH_X) - 1): dim_h(msp, C.ARCH_X[i], C.ARCH_X[i + 1], 3.6, 0.5)
    title(msp, -3.7, 5.6, "ZION CASULO · PLANTA BAIXA" + (" (LAYOUT)" if layout else " (COTADA)") + " · escala 1:50 · unidades em metros")

def cocoon_estrutura(msp):
    D = C.DECK
    floor = C.floor_outline(120); pl(msp, floor, "PAREDES", close=True); rect(msp, D["x1"], D["y1"], D["x2"], D["y2"], "DECK")
    for i, x in enumerate(C.ARCH_X):
        pts = [(px, py) for (px, py, pz) in C.section_curve(x, 60)]; pl(msp, pts, "ESTRUTURA"); txt(msp, x, 3.9, f"B0{i + 1}" if i else "A0", h=0.14)
    for p in C.purlins(40): pl(msp, [(x, y) for (x, y, z) in p], "ESTRUTURA")
    for s in (-1, 1): pl(msp, [(x, s * (C.floor_hw(x) - 0.05)) for x in np.linspace(0.9, 9.35, 60)], "ESTRUTURA")
    # vigas de piso e estacas (malha 2,4 m)
    piles = cocoon_pile_grid()
    for y in sorted(set(round(py, 2) for (px, py) in piles)): pl(msp, [(-3.7, y), (9.4, y)], "ESTRUTURA")
    for i, (x, y) in enumerate(piles):
        msp.add_circle((x, y), 0.15, dxfattribs={"layer": "FUNDACAO"}); msp.add_circle((x, y), 0.04, dxfattribs={"layer": "FUNDACAO"}); txt(msp, x + 0.22, y + 0.2, f"F{i + 1:02d}", h=0.08)
    txt(msp, 3.0, -4.3, f"{len(piles)} estacas helicoidais Ø76 · hélice Ø300 · malha 1,20 x 1,30 m (pré-dimensionamento)", h=0.16)
    title(msp, -3.7, 5.6, "ZION CASULO · PLANTA ESTRUTURAL (arcos, terças, trilhos, vigas de piso, estacas) · 1:50")

def cocoon_cobertura(msp):
    shell = [(x, -C.a(x)) for x in np.linspace(0.5, C.L, 120)] + [(x, C.a(x)) for x in np.linspace(C.L, 0.5, 120)]
    pl(msp, shell, "COBERTURA", close=True); pl(msp, [(x, y) for (x, y, z) in C.front_ring(80)], "COBERTURA")
    for x in C.ARCH_X: pl(msp, [(px, py) for (px, py, pz) in C.section_curve(x, 60)], "COBERTURA_OCULTA")
    x1, x2, ht = C.SPINE; hw = ht * C.B_MAX; rect(msp, C.shear(x1, 4.15), -hw, C.shear(x2, 4.15), hw, "ESQUADRIAS")
    for s in (1, -1): pl(msp, [(x, s * (C.floor_hw(x) + 0.08)) for x in np.linspace(0.9, 9.3, 60)], "ESTRUTURA")
    for (qx, qy) in [(0.95, -2.75), (0.95, 2.75), (9.25, -1.2), (9.25, 1.2)]: msp.add_circle((qx, qy), 0.06, dxfattribs={"layer": "ESTRUTURA"}); txt(msp, qx, qy + 0.3, "TQ Ø75", h=0.1)
    D = C.DECK; rect(msp, D["x1"], D["y1"], D["x2"], D["y2"], "DECK")
    dim_h(msp, -0.15, 9.6, -3.9, -0.5, "9,75"); dim_v(msp, 10.2, -3.0, 3.0, 0.6, "6,00")
    title(msp, -3.7, 5.6, "ZION CASULO · PLANTA DE COBERTURA · calha oculta no rodapé, TQ Ø75, Espinha de Luz · 1:50")

def cocoon_corte_long(msp):
    xs = np.linspace(C.X_FRONT, C.L, 160)
    top = [(C.shear(x, C.top(x)), C.top(x)) for x in xs]
    pl(msp, [(-3.7, -0.2), (9.6, -0.2), (9.6, 0), (-3.7, 0)], "DECK", close=True)
    pl(msp, top, "COBERTURA"); pl(msp, [(C.shear(C.X_FRONT, 0), 0), (C.shear(C.X_FRONT, 4.13), 4.13)], "ESTRUTURA")
    pl(msp, [(C.shear(C.X_GLASS, 0), 0), (C.shear(C.X_GLASS, 4.15), 4.15)], "ESQUADRIAS")
    for x in C.ARCH_X: pl(msp, [(C.shear(x, 0), 0), (C.shear(x, C.top(x)), C.top(x))], "EIXOS")
    for it in C.furniture():
        if it["kind"] in ("pillow",): continue
        if "r" in it: rect(msp, it["x"] - it["r"], it["z1"], it["x"] + it["r"], it["z2"], "MOBILIARIO")
        else: rect(msp, it["x1"], it["z1"], it["x2"], it["z2"], "PAREDES" if it["kind"] == "wall" else "MOBILIARIO")
    for px in [-3.3, -1.1, 0.9, 2.1, 3.3, 4.5, 5.7, 6.9, 8.1, 9.0]: pl(msp, [(px, -0.2), (px, -2.0)], "FUNDACAO")
    pl(msp, [(-4.5, -0.6), (11, -0.6)], "TEXTO")
    dim_h(msp, 0.45, 9.6, -2.3, -0.5, "9,60"); dim_v(msp, 10.5, 0, 4.2, 0.6, "4,20"); dim_v(msp, 10.5, 0, 2.45, 1.4, "2,45 (forro banho)")
    title(msp, -3.7, 5.6, "ZION CASULO · CORTE LONGITUDINAL A-A · 1:50")

def cocoon_corte_transv(msp, xc=5.0):
    sec = C.section_local(xc, 80); pl(msp, sec, "COBERTURA")
    inner = [(y * (1 - 0.12 / max(C.a(xc), 0.1)), C.ZC + (z - C.ZC) * (1 - 0.12 / C.b(xc))) for (y, z) in sec]; pl(msp, inner, "COBERTURA_OCULTA")
    hw = C.floor_hw(xc); pl(msp, [(-hw, 0), (hw, 0)], "PAREDES"); pl(msp, [(-hw - 0.1, -0.2), (hw + 0.1, -0.2), (hw + 0.1, 0), (-hw - 0.1, 0)], "DECK", close=True)
    for y in (-2.4, -1.2, 0, 1.2, 2.4): rect(msp, y - 0.075, -0.2, y + 0.075, -0.05, "ESTRUTURA")
    for y in (-2.4, 0, 2.4): pl(msp, [(y, -0.2), (y, -2.0)], "FUNDACAO")
    for it in C.furniture():
        if not (it.get("x1", 99) <= xc <= it.get("x2", -99)) or it["kind"] in ("pillow",): continue
        rect(msp, it["y1"], it["z1"], it["y2"], it["z2"], "MOBILIARIO")
    x1, x2, ht = C.SPINE
    if x1 <= xc <= x2: pl(msp, [(-ht * C.B_MAX, C.top(xc)), (ht * C.B_MAX, C.top(xc))], "ESQUADRIAS")
    pl(msp, [(-5, -0.6), (5, -0.6)], "TEXTO")
    dim_h(msp, -C.a(xc), C.a(xc), -2.3, -0.5); dim_v(msp, 4.0, 0, C.top(xc), 0.6)
    title(msp, -4.5, 5.6, f"ZION CASULO · CORTE TRANSVERSAL B-B (x = {xc:.2f} m) · 1:50".replace(".", ","))

def cocoon_fachada_frontal(msp):
    ring = [(y, z) for (x, y, z) in C.front_ring(100)]; pl(msp, ring, "COBERTURA")
    glass = [(y, z) for (x, y, z) in C.glass_ring(100)]; pl(msp, glass, "ESQUADRIAS")
    for yy in (-1.6, -0.5, 0.5, 1.6):
        zt = C.ZC + (C.b(C.X_GLASS) - 0.06) * math.sqrt(max(0, 1 - (yy / (C.a(C.X_GLASS) - 0.06)) ** 2)); pl(msp, [(yy, 0), (yy, zt)], "ESQUADRIAS")
    pl(msp, [(-2.5, 2.4), (2.5, 2.4)], "ESQUADRIAS"); rect(msp, 0.6, 0, 1.6, 2.4, "ESQUADRIAS")
    D = C.DECK; rect(msp, D["y1"], -0.2, D["y2"], 0, "DECK"); pl(msp, [(-4.5, -0.6), (4.5, -0.6)], "TEXTO")
    for y in (-2.4, 0, 2.4): pl(msp, [(y, -0.2), (y, -2.0)], "FUNDACAO")
    dim_h(msp, -3.0, 3.0, -2.3, -0.5, "6,00"); dim_v(msp, 3.8, 0, 4.13, 0.6, "4,13")
    title(msp, -4.5, 5.6, "ZION CASULO · FACHADA FRONTAL (vista de fora, y crescente para a esquerda) · 1:50")

def cocoon_fachada_lateral(msp, side=-1):
    xs = np.linspace(C.X_FRONT, C.L, 160)
    top = [(C.shear(x, C.top(x)), C.top(x)) for x in xs]; bot = [(C.shear(x, 0), 0) for x in xs]
    pl(msp, top + bot[::-1], "COBERTURA", close=True)
    pl(msp, [(C.shear(C.X_FRONT, 0), 0), (C.shear(C.X_FRONT, 4.13), 4.13)], "ESTRUTURA")
    for w in C.WINDOWS:
        if (w["tc"] < math.pi / 2) != (side < 0): continue
        pl(msp, [(x, z) for (x, y, z) in C.window_outline(w, 48)], "ESQUADRIAS", close=True)
    x1, x2, _ = C.SPINE; pl(msp, [(C.shear(x, C.top(x)), C.top(x)) for x in np.linspace(x1, x2, 30)], "ESQUADRIAS")
    pl(msp, [(-3.7, -0.2), (9.6, -0.2), (9.6, 0), (-3.7, 0)], "DECK", close=True); pl(msp, [(-4.5, -0.6), (11, -0.6)], "TEXTO")
    for px in [-3.3, -1.1, 0.9, 2.1, 3.3, 4.5, 5.7, 6.9, 8.1, 9.0]: pl(msp, [(px, -0.2), (px, -2.0)], "FUNDACAO")
    dim_h(msp, 0.45, 9.6, -2.3, -0.5, "9,60"); dim_h(msp, -3.7, 0.9, -2.3, -0.5, "4,60"); dim_v(msp, 10.5, 0, 4.2, 0.6, "4,20")
    title(msp, -3.7, 5.6, "ZION CASULO · FACHADA LATERAL " + ("DIREITA (olhar para +y)" if side < 0 else "ESQUERDA (olhar para -y; espelhar ao plotar)") + " · 1:50")

def cocoon_3d(msp):
    m = C.shell_mesh(72, 36); V = m["vertices"]
    for key, layer in (("membrane", "MEMBRANA_3D"), ("glass", "VIDRO_3D")):
        for f in m[key]:
            a, b, c = V[f[0]], V[f[1]], V[f[2]]
            msp.add_3dface([a, b, c, c], dxfattribs={"layer": layer})
    for a in C.arches(): msp.add_polyline3d(a["pts"], dxfattribs={"layer": "ACO_3D"})
    for p in C.purlins(40): msp.add_polyline3d(p, dxfattribs={"layer": "ACO_3D"})
    msp.add_polyline3d(C.front_ring(80), dxfattribs={"layer": "ACO_3D"}); msp.add_polyline3d(C.glass_ring(80), dxfattribs={"layer": "VIDRO_3D"})
    floor = [(x, y, 0.0) for (x, y) in C.floor_outline(120)]; msp.add_polyline3d(floor + [floor[0]], dxfattribs={"layer": "PAREDES"})
    D = C.DECK; msp.add_polyline3d([(D["x1"], D["y1"], 0), (D["x2"], D["y1"], 0), (D["x2"], D["y2"], 0), (D["x1"], D["y2"], 0), (D["x1"], D["y1"], 0)], dxfattribs={"layer": "DECK"})
    for it in C.furniture():
        if "r" in it or it["kind"] in ("pillow", "ceiling"): continue
        x1, x2, y1, y2, z1, z2 = it["x1"], it["x2"], it["y1"], it["y2"], it["z1"], it["z2"]
        P = [(x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1), (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2)]
        for f in ((0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            msp.add_3dface([P[i] for i in f], dxfattribs={"layer": "MOBILIARIO"})

# ============================================================================ SAFARI
def zenith_planta(msp, layout=True):
    rb = Z.roof_bounds(); rect(msp, rb[0], rb[2], rb[1], rb[3], "COBERTURA_OCULTA")
    rect(msp, 0, -2.7, 9.5, 2.7, "PAREDES"); rect(msp, 0.1, -2.6, 9.4, 2.6, "PAREDES")
    for w in Z.walls():
        if w["kind"] in ("glass", "window"):
            pl(msp, [w["p1"], w["p2"]], "ESQUADRIAS")
            if w["kind"] == "glass" and w["p1"][0] == 0 and w["p2"][0] == 0:
                for k in range(1, 4): y = -2.7 + 5.4 * k / 4; pl(msp, [(-0.05, y), (0.15, y)], "ESQUADRIAS")
    D, Wk, H = Z.DECK, Z.WALK, Z.HOTTUB
    rect(msp, D["x1"], D["y1"], D["x2"], D["y2"], "DECK"); rect(msp, Wk["x1"], Wk["y1"], Wk["x2"], Wk["y2"], "DECK")
    msp.add_circle((H["x"], H["y"]), H["r"], dxfattribs={"layer": "DECK"})
    for i in range(1, 4): pl(msp, [(D["x1"] - 0.3 * i, D["y1"]), (D["x1"] - 0.3 * i, D["y2"])], "DECK")
    for p in Z.PEAKS: msp.add_circle((p["x"], p["y"]), p["r"], dxfattribs={"layer": "COBERTURA_OCULTA"}); msp.add_circle((p["x"], p["y"]), 0.07, dxfattribs={"layer": "ESTRUTURA"})
    if layout: furniture_plan(msp, Z.furniture())
    for (x, y) in Z.columns(): rect(msp, x - 0.05, y - 0.05, x + 0.05, y + 0.05, "ESTRUTURA")
    for (x, y) in Z.posts(): msp.add_circle((x, y), 0.04, dxfattribs={"layer": "ESTRUTURA"})
    for i, x in enumerate((0, 3.2, 6.4, 9.5)): pl(msp, [(x, -4.2), (x, 4.2)], "EIXOS"); msp.add_circle((x, 4.45), 0.2, dxfattribs={"layer": "EIXOS"}); txt(msp, x, 4.45, f"{i + 1}", h=0.15)
    for k, y in enumerate((-2.7, 0, 2.7)): pl(msp, [(-3.5, y), (11.0, y)], "EIXOS"); msp.add_circle((-3.75, y), 0.2, dxfattribs={"layer": "EIXOS"}); txt(msp, -3.75, y, "ABC"[k], h=0.15)
    dim_h(msp, 0, 9.5, -3.7, -0.5, "9,50"); dim_h(msp, -3.0, 0, -3.7, -0.5, "3,00"); dim_v(msp, 10.7, -2.7, 2.7, 0.6, "5,40"); dim_v(msp, 10.7, 2.7, 3.5, 0.6, "0,80")
    for a, b in ((0, 3.2), (3.2, 6.4), (6.4, 9.5)): dim_h(msp, a, b, 3.7, 0.5)
    title(msp, -3.0, 5.8, "ZION SAFARI · PLANTA BAIXA" + (" (LAYOUT)" if layout else " (COTADA)") + " · escala 1:50 · unidades em metros")

def zenith_estrutura(msp):
    rb = Z.roof_bounds(); rect(msp, rb[0], rb[2], rb[1], rb[3], "COBERTURA_OCULTA"); rect(msp, 0, -2.7, 9.5, 2.7, "ESTRUTURA")
    for (x, y) in Z.columns(): rect(msp, x - 0.06, y - 0.06, x + 0.06, y + 0.06, "ESTRUTURA"); txt(msp, x, y + 0.3, "P", h=0.1)
    for (x, y) in Z.posts():
        msp.add_circle((x, y), 0.05, dxfattribs={"layer": "ESTRUTURA"}); pl(msp, [(x, y), (x + (0.6 if x < 5 else -0.6) * (0 if abs(y) > 3 and x not in (rb[0], rb[1]) else 1), y + (0.6 if y < 0 else -0.6) * (0 if abs(y) < 0.1 else 1))], "ESTRUTURA")
    for p in Z.PEAKS:
        msp.add_circle((p["x"], p["y"]), 0.07, dxfattribs={"layer": "ESTRUTURA"}); msp.add_circle((p["x"], p["y"]), p["r"], dxfattribs={"layer": "ESTRUTURA"})
        for k in range(3):
            ang = math.pi / 2 + 2 * math.pi * k / 3; pl(msp, [(p["x"], p["y"]), (p["x"] + p["r"] * math.cos(ang), p["y"] + p["r"] * math.sin(ang))], "ESTRUTURA")
    grid = zenith_pile_grid(); tens = zenith_tension_piles()
    for y in sorted(set(round(py, 2) for (px, py) in grid)): pl(msp, [(-3.0, y), (9.5, y)], "ESTRUTURA")
    for i, (x, y) in enumerate(grid):
        msp.add_circle((x, y), 0.15, dxfattribs={"layer": "FUNDACAO"}); txt(msp, x + 0.22, y + 0.2, f"F{i + 1:02d}", h=0.08)
    for i, (x, y) in enumerate(tens):
        msp.add_circle((x, y), 0.12, dxfattribs={"layer": "FUNDACAO"}); txt(msp, x, y - 0.3, f"FT{i + 1:02d}", h=0.08)
    txt(msp, 3.0, -4.9, f"{len(grid)} estacas helicoidais Ø76 sob o piso + {len(tens)} estacas de tração sob os postes (pré-dimensionamento)", h=0.16)
    title(msp, -3.0, 5.8, "ZION SAFARI · PLANTA ESTRUTURAL (pilares, anel de beiral, mastros, postes estaiados, vigas, estacas) · 1:50")

def zenith_cobertura(msp):
    rb = Z.roof_bounds(); rect(msp, rb[0], rb[2], rb[1], rb[3], "COBERTURA"); rect(msp, 0, -2.7, 9.5, 2.7, "COBERTURA_OCULTA")
    # curvas de nível (marching squares)
    x0, x1, y0, y1 = rb; nx, ny = 100, 60
    xs = np.linspace(x0, x1, nx + 1); ys = np.linspace(y0, y1, ny + 1); G = np.array([[Z.roof_z(x, y) for y in ys] for x in xs])
    for lv in (3.0, 3.4, 3.8, 4.2, 4.6, 5.0, 5.4, 5.7):
        for i in range(nx):
            for j in range(ny):
                sq = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]; pts = []
                for (a, b) in [(0, 1), (1, 2), (2, 3), (3, 0)]:
                    (ia, ja), (ib, jb) = sq[a], sq[b]; va, vb = G[ia, ja] - lv, G[ib, jb] - lv
                    if (va < 0) != (vb < 0):
                        t = va / (va - vb); pts.append((xs[ia] + (xs[ib] - xs[ia]) * t, ys[ja] + (ys[jb] - ys[ja]) * t))
                if len(pts) >= 2: pl(msp, pts[:2], "COBERTURA")
    for p in Z.PEAKS: msp.add_circle((p["x"], p["y"]), p["r"], dxfattribs={"layer": "ESQUADRIAS"}); txt(msp, p["x"], p["y"] + p["r"] + 0.25, f"cume +{p['h']:.2f}".replace(".", ","), h=0.12)
    for (x, y) in Z.posts(): msp.add_circle((x, y), 0.05, dxfattribs={"layer": "ESTRUTURA"})
    pl(msp, [(0, -2.78), (9.5, -2.78)], "ESTRUTURA"); pl(msp, [(0, 2.78), (9.5, 2.78)], "ESTRUTURA")
    dim_h(msp, x0, x1, y0 - 0.6, -0.5, "12,90"); dim_v(msp, x1 + 0.6, y0, y1, 0.6, "7,40")
    title(msp, -3.0, 5.8, "ZION SAFARI · PLANTA DE COBERTURA · curvas de nível a cada 0,40 m · 1:50")

def zenith_corte_long(msp, y=0.4):
    x0, x1, y0, y1 = Z.roof_bounds()
    pl(msp, Z.ridge_profile(y, 120), "COBERTURA"); pl(msp, [(x, Z.liner_z(x, y)) for x in np.linspace(0, 9.5, 80)], "COBERTURA_OCULTA")
    rect(msp, 0, 0, 9.5, 2.75, "PAREDES"); rect(msp, 0, 2.75, 9.5, 2.9, "ESTRUTURA")
    for p in Z.PEAKS: rect(msp, p["x"] - 0.07, 0, p["x"] + 0.07, p["mast_top"], "ESTRUTURA")
    for it in Z.furniture():
        if it["kind"] in ("pillow", "ceiling"): continue
        rect(msp, it["x1"], it["z1"], it["x2"], it["z2"], "PAREDES" if it["kind"] == "wall" else "MOBILIARIO")
    pl(msp, [(-3.0, -0.2), (9.5, -0.2), (9.5, 0), (-3.0, 0)], "DECK", close=True); pl(msp, [(-4.5, -0.6), (11.5, -0.6)], "TEXTO")
    for px in [-2.6, -0.2, 2.2, 4.6, 7.0, 9.4]: pl(msp, [(px, -0.2), (px, -2.0)], "FUNDACAO")
    for px in (x0, 4.0, x1): pl(msp, [(px, -0.05), (px, Z.edge_height(px, y0))], "ESTRUTURA")
    dim_h(msp, 0, 9.5, -2.3, -0.5, "9,50"); dim_v(msp, 11.0, 0, 5.8, 0.6, "5,80"); dim_v(msp, 11.0, 0, 2.9, 1.4, "2,90")
    title(msp, -3.0, 6.6, f"ZION SAFARI · CORTE LONGITUDINAL A-A (y = {y:.2f} m) · 1:50".replace(".", ","))

def zenith_corte_transv(msp, x=6.3):
    x0, x1, y0, y1 = Z.roof_bounds()
    pl(msp, Z.cross_profile(x, 80), "COBERTURA"); pl(msp, [(yy, Z.liner_z(x, yy)) for yy in np.linspace(-2.7, 2.7, 60)], "COBERTURA_OCULTA")
    rect(msp, -2.7, 0, 2.7, 2.75, "PAREDES"); rect(msp, -2.7, 2.75, 2.7, 2.9, "ESTRUTURA")
    for p in Z.PEAKS:
        if abs(p["x"] - x) < 0.3: rect(msp, p["y"] - 0.07, 0, p["y"] + 0.07, p["mast_top"], "ESTRUTURA")
    for it in Z.furniture():
        if not (it["x1"] <= x <= it["x2"]) or it["kind"] in ("pillow", "ceiling"): continue
        rect(msp, it["y1"], it["z1"], it["y2"], it["z2"], "PAREDES" if it["kind"] == "wall" else "MOBILIARIO")
    pl(msp, [(-2.7, -0.2), (3.5, -0.2), (3.5, 0), (-2.7, 0)], "DECK", close=True); pl(msp, [(-5, -0.6), (5, -0.6)], "TEXTO")
    for py in (-2.7, -1.35, 0, 1.35, 2.7): pl(msp, [(py, -0.2), (py, -2.0)], "FUNDACAO")
    for py in (y0, y1): pl(msp, [(py, -0.05), (py, Z.edge_height(x if x in (x0, x1) else 4.0, py))], "ESTRUTURA")
    dim_h(msp, -2.7, 2.7, -2.3, -0.5, "5,40"); dim_v(msp, 4.5, 0, Z.roof_z(x, 0.4), 0.6)
    title(msp, -4.5, 6.6, f"ZION SAFARI · CORTE TRANSVERSAL B-B (x = {x:.2f} m) · 1:50".replace(".", ","))

def zenith_fachada(msp, which):
    x0, x1, y0, y1 = Z.roof_bounds()
    if which in ("frontal", "traseira"):
        sil = Z.silhouette_front(100); edge = [(y, Z.edge_height(x0 if which == "frontal" else x1, y)) for y in np.linspace(y0, y1, 60)]
        pl(msp, sil + edge[::-1], "COBERTURA", close=True)
        rect(msp, -2.7, 0, 2.7, 2.75, "ESQUADRIAS" if which == "frontal" else "PAREDES"); rect(msp, -2.7, 2.75, 2.7, 2.9, "ESTRUTURA")
        if which == "frontal":
            for k in range(1, 4): pl(msp, [(-2.7 + 5.4 * k / 4, 0), (-2.7 + 5.4 * k / 4, 2.75)], "ESQUADRIAS")
        else: rect(msp, -0.8, 1.5, 1.6, 2.15, "ESQUADRIAS")
        for py in (y0, y1): pl(msp, [(py, -0.05), (py, Z.edge_height(x0 if which == "frontal" else x1, py))], "ESTRUTURA")
        pl(msp, [(-3.5, -0.2), (3.5, -0.2), (3.5, 0), (-3.5, 0)], "DECK", close=True); pl(msp, [(-5, -0.6), (5, -0.6)], "TEXTO")
        dim_h(msp, -2.7, 2.7, -2.3, -0.5, "5,40"); dim_h(msp, y0, y1, -2.3, -1.1, "7,40"); dim_v(msp, 4.5, 0, 5.8, 0.6, "5,80")
        title(msp, -4.5, 6.6, f"ZION SAFARI · FACHADA {which.upper()} · 1:50")
    else:
        side = y0 if which == "direita" else y1
        sil = Z.silhouette_side(160); edge = [(x, Z.edge_height(x, side)) for x in np.linspace(x0, x1, 80)]
        pl(msp, sil + edge[::-1], "COBERTURA", close=True)
        rect(msp, 0, 0, 9.5, 2.75, "PAREDES"); rect(msp, 0, 2.75, 9.5, 2.9, "ESTRUTURA")
        for w in Z.walls():
            if abs(w["p1"][1] - side * 2.7 / abs(side)) > 0.01 or w["p1"][1] != w["p2"][1]: continue
            if w["kind"] in ("glass", "window"): rect(msp, w["p1"][0], w["z1"], w["p2"][0], w["z2"], "ESQUADRIAS")
        for px in (x0, 4.0, x1): pl(msp, [(px, -0.05), (px, Z.edge_height(px, side))], "ESTRUTURA")
        pl(msp, [(-3.0, -0.2), (9.5, -0.2), (9.5, 0), (-3.0, 0)], "DECK", close=True); pl(msp, [(-4.5, -0.6), (11.5, -0.6)], "TEXTO")
        for px in [-2.6, -0.2, 2.2, 4.6, 7.0, 9.4]: pl(msp, [(px, -0.2), (px, -2.0)], "FUNDACAO")
        dim_h(msp, 0, 9.5, -2.3, -0.5, "9,50"); dim_h(msp, x0, x1, -2.3, -1.1, "12,90"); dim_v(msp, 11.0, 0, 5.8, 0.6, "5,80")
        title(msp, -3.0, 6.6, f"ZION SAFARI · FACHADA LATERAL {which.upper()}" + (" (olhar para -y; espelhar ao plotar)" if which == "esquerda" else " (olhar para +y)") + " · 1:50")

def zenith_3d(msp):
    m = Z.roof_mesh(56, 34); V = m["vertices"]
    for f in m["faces"]:
        a, b, c = V[f[0]], V[f[1]], V[f[2]]; msp.add_3dface([a, b, c, c], dxfattribs={"layer": "MEMBRANA_3D"})
    for w in Z.walls():
        (xa, ya), (xb, yb) = w["p1"], w["p2"]
        msp.add_3dface([(xa, ya, w["z1"]), (xb, yb, w["z1"]), (xb, yb, w["z2"]), (xa, ya, w["z2"])], dxfattribs={"layer": "VIDRO_3D" if w["kind"] in ("glass", "window") else "PAREDES"})
    for mst in Z.masts(): msp.add_polyline3d([(mst["x"], mst["y"], mst["z1"]), (mst["x"], mst["y"], mst["z2"])], dxfattribs={"layer": "ACO_3D"})
    for cr in Z.crowns():
        for arm in cr["arms"]: msp.add_polyline3d(arm, dxfattribs={"layer": "ACO_3D"})
        msp.add_polyline3d(cr["ring"], dxfattribs={"layer": "ACO_3D"})
    for (x, y) in Z.columns(): msp.add_polyline3d([(x, y, 0), (x, y, Z.Z_EAVE)], dxfattribs={"layer": "ACO_3D"})
    for (x, y) in Z.posts(): msp.add_polyline3d([(x, y, -0.05), (x, y, Z.edge_height(x, y))], dxfattribs={"layer": "ACO_3D"})
    msp.add_polyline3d([(0, -2.7, Z.Z_EAVE), (9.5, -2.7, Z.Z_EAVE), (9.5, 2.7, Z.Z_EAVE), (0, 2.7, Z.Z_EAVE), (0, -2.7, Z.Z_EAVE)], dxfattribs={"layer": "ACO_3D"})
    D = Z.DECK; msp.add_polyline3d([(D["x1"], D["y1"], 0), (D["x2"], D["y1"], 0), (D["x2"], D["y2"], 0), (D["x1"], D["y2"], 0), (D["x1"], D["y1"], 0)], dxfattribs={"layer": "DECK"})
    for it in Z.furniture():
        if it["kind"] in ("pillow", "ceiling"): continue
        x1, x2, y1, y2, z1, z2 = it["x1"], it["x2"], it["y1"], it["y2"], it["z1"], it["z2"]
        P = [(x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1), (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2)]
        for f in ((0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            msp.add_3dface([P[i] for i in f], dxfattribs={"layer": "MOBILIARIO"})

# ============================================================================ LODGE
LV = L.vertices(); LR = L.r_corner(); LRO = LR + L.OVER / math.cos(math.pi / 8); LVO = L.vertices(LRO)   # pilares / octógono do beiral
LRE = LRO * math.cos(math.pi / 8)                                                                        # 4,30: borda do beiral na direção das faces
LYC = math.sqrt(LR ** 2 - L.X_PART ** 2); LZE = L.Z_EAVE - 0.35                                          # meia-corda da parede do banho; cota da borda (2,35)
L_PX = sorted(set(round(x, 2) for (x, y) in L.piles())); L_PY = sorted(set(round(y, 2) for (x, y) in L.piles()))

def lodge_d(z):
    t = ((L.Z_LANTERN - z) / (L.Z_LANTERN - LZE)) ** (1 / 1.25)
    return L.R_LANTERN + t * (LR + L.OVER - L.R_LANTERN)

def lodge_profile(n=40):
    """perfil da membrana em elevação / corte pelo eixo (u, z), de -4,30 a +4,30, com a borda a 2,35."""
    ds = np.linspace(L.R_LANTERN, LRE, n)
    right = [(d, L.roof_z(d)) for d in ds] + [(LRE, LZE)]
    return [(-d, z) for (d, z) in right][::-1] + right

def lodge_lantern(msp):
    rect(msp, -L.R_LANTERN, L.Z_LANTERN - 0.1, L.R_LANTERN, L.Z_LANTERN, "ESTRUTURA")
    rect(msp, -L.R_LANTERN, L.Z_LANTERN, L.R_LANTERN, L.Z_TOP - 0.15, "ESQUADRIAS")
    for u in (-0.53, 0.0, 0.53): pl(msp, [(u, L.Z_LANTERN), (u, L.Z_TOP - 0.15)], "ESQUADRIAS")
    rect(msp, -L.R_LANTERN - 0.25, L.Z_TOP - 0.15, L.R_LANTERN + 0.25, L.Z_TOP, "COBERTURA")

def lodge_roof_elev(msp, axis="x", depth_sign=1):
    """cobertura em elevação: silhueta fechada, costuras dos gomos visíveis e lanterna. axis = coordenada horizontal;
    a outra é a profundidade; costuras visíveis quando profundidade * depth_sign > 0."""
    pl(msp, lodge_profile(), "COBERTURA", close=True)
    for k in range(8):
        ang = math.pi / 8 + 2 * math.pi * k / 8
        pts3 = [(d * math.cos(ang), d * math.sin(ang), max(L.roof_z(d), LZE)) for d in np.linspace(L.R_LANTERN, LRO, 20)]
        depth = pts3[0][1] if axis == "x" else pts3[0][0]
        if depth * depth_sign > 0: pl(msp, [((x if axis == "x" else y), z) for (x, y, z) in pts3], "COBERTURA_OCULTA")
    lodge_lantern(msp)

def lodge_wall_panel(msp, u1, u2, z1=0.0, z2=L.Z_EAVE - 0.15, step=0.1):
    rect(msp, u1, z1, u2, z2, "PAREDES")
    u = u1 + step
    while u < u2 - 0.01: pl(msp, [(u, z1), (u, z2)], "HACHURA"); u += step

def lodge_stairs_side(msp):
    for i in range(2): rect(msp, -6.0 - 0.3 * (i + 1), -0.2 * (i + 1) - 0.05, -6.0 - 0.3 * i, -0.2 * (i + 1), "DECK")

def lodge_sail_plan(msp):
    sp = L.sail_posts()
    for (x, y) in sp: msp.add_circle((x, y), 0.05, dxfattribs={"layer": "ESTRUTURA"})
    pl(msp, [LV[3], sp[1], sp[0], LV[4]], "COBERTURA_OCULTA", close=True)

def lodge_planta(msp, layout=True):
    pl(msp, LVO, "COBERTURA_OCULTA", close=True); msp.add_circle((0, 0), L.R_LANTERN, dxfattribs={"layer": "COBERTURA_OCULTA"})
    pl(msp, LV, "PAREDES", close=True)
    for (i, j) in L.GLASS_FACES: pl(msp, [LV[i], LV[j]], "ESQUADRIAS")
    for (i, j) in L.WALL_FACES:   # painel SIP 100 mm para dentro da linha dos pilares
        (x1, y1), (x2, y2) = LV[i], LV[j]; mx, my = (x1 + x2) / 2, (y1 + y2) / 2; mm = math.hypot(mx, my); nx, ny = -0.1 * mx / mm, -0.1 * my / mm
        quad = [(x1, y1), (x2, y2), (x2 + nx, y2 + ny), (x1 + nx, y1 + ny)]
        pl(msp, quad, "PAREDES", close=True); msp.add_hatch(color=8, dxfattribs={"layer": "HACHURA"}).paths.add_polyline_path(quad, is_closed=True)
    D = L.DOOR   # porta de correr PC1 (2 folhas) na face frontal e fresta J1 na face posterior
    pl(msp, [(-3.4 - 0.05, D["y1"]), (-3.4 - 0.05, 0.0)], "ESQUADRIAS"); pl(msp, [(-3.4 + 0.05, 0.0), (-3.4 + 0.05, D["y2"])], "ESQUADRIAS")
    pl(msp, [(3.4, -0.8), (3.4, 0.8)], "ESQUADRIAS")
    for (x, y) in L.columns(): rect(msp, x - 0.06, y - 0.06, x + 0.06, y + 0.06, "ESTRUTURA")
    pl(msp, L.deck_pts(), "DECK", close=True)
    for i in range(1, 4): pl(msp, [(-6.0 - 0.3 * i, -1.2), (-6.0 - 0.3 * i, 1.2)], "DECK")
    lodge_sail_plan(msp)
    if layout: furniture_plan(msp, L.furniture())
    else:
        for it in L.furniture():
            if it["kind"] == "wall": rect(msp, it["x1"], it["y1"], it["x2"], it["y2"], "PAREDES")
            if it["kind"] == "opening": rect(msp, it["x1"], it["y1"], it["x2"], it["y2"], "ESQUADRIAS")
    for i, x in enumerate((-3.4, 0.0, 3.4)): pl(msp, [(x, -7.0), (x, 7.0)], "EIXOS"); msp.add_circle((x, 7.25), 0.2, dxfattribs={"layer": "EIXOS"}); txt(msp, x, 7.25, f"{i + 1}", h=0.15)
    for k, y in enumerate((-3.4, 0.0, 3.4)): pl(msp, [(-7.5, y), (5.0, y)], "EIXOS"); msp.add_circle((-7.75, y), 0.2, dxfattribs={"layer": "EIXOS"}); txt(msp, -7.75, y, "ABC"[k], h=0.15)
    dim_h(msp, -6.0, -3.4, -6.6, -0.5, "2,60"); dim_h(msp, -3.4, 3.4, -6.6, -0.5, "6,80"); dim_h(msp, -3.4, L.X_PART, -6.6, -1.1, "4,95"); dim_h(msp, L.X_PART, 3.4, -6.6, -1.1, "1,85")
    dim_v(msp, 5.5, -3.4, 3.4, 0.6, "6,80"); dim_v(msp, 5.5, -6.0, 6.0, 1.4, "12,00")
    title(msp, -7.5, 8.0, "ZION LODGE · PLANTA BAIXA" + (" (LAYOUT)" if layout else " (COTADA)") + " · octógono 6,80 entre faces · escala 1:50 · unidades em metros")

def lodge_estrutura(msp):
    pl(msp, LVO, "COBERTURA_OCULTA", close=True); pl(msp, LV, "ESTRUTURA", close=True)
    for i, (x, y) in enumerate(L.columns()): rect(msp, x - 0.06, y - 0.06, x + 0.06, y + 0.06, "ESTRUTURA"); txt(msp, x * 1.09, y * 1.09, f"P{i + 1}", h=0.12)
    for r in L.rafters(): pl(msp, [(x, y) for (x, y, z) in r], "ESTRUTURA")
    msp.add_circle((0, 0), L.R_LANTERN, dxfattribs={"layer": "ESTRUTURA"}); msp.add_circle((0, 0), L.R_LANTERN + 0.25, dxfattribs={"layer": "ESTRUTURA"})
    for y in (-2.55, -0.85, 0.85, 2.55):        # vigas de piso (nas linhas de estacas)
        xw = min(3.4, 3.4 + 1.408 - abs(y)); pl(msp, [(-xw, y), (xw, y)], "ESTRUTURA")
    for y in (-3.2, -1.1, 1.1, 3.2):            # vigas do deck
        x_in = -3.4 if abs(y) <= 1.408 else -(3.4 + 1.408 - abs(y)); x_out = -6.0 if abs(y) <= 2.485 else -(6.0 + 2.485 - abs(y))
        pl(msp, [(x_out, y), (x_in, y)], "ESTRUTURA")
    pl(msp, L.deck_pts(), "DECK", close=True); lodge_sail_plan(msp)
    for i, (x, y) in enumerate(L.piles()):
        msp.add_circle((x, y), 0.15, dxfattribs={"layer": "FUNDACAO"}); msp.add_circle((x, y), 0.04, dxfattribs={"layer": "FUNDACAO"}); txt(msp, x + 0.22, y + 0.2, f"F{i + 1:02d}", h=0.08)
    txt(msp, -1.0, -7.2, f"{len(L.piles())} estacas helicoidais Ø76 · hélice Ø300 · malha ~2,40 x 1,70 m + 4 de borda + 2 sob os postes da vela (pré-dimensionamento)", h=0.16)
    title(msp, -7.5, 8.0, "ZION LODGE · PLANTA ESTRUTURAL (8 pilares, anel de beiral, 8 caibros, anel da lanterna, vigas de piso e deck, estacas) · 1:50")

def lodge_cobertura(msp):
    pl(msp, LVO, "COBERTURA", close=True); pl(msp, LV, "COBERTURA_OCULTA", close=True)
    for k in range(8):
        ang = math.pi / 8 + 2 * math.pi * k / 8; pl(msp, [(L.R_LANTERN * math.cos(ang), L.R_LANTERN * math.sin(ang)), (LRO * math.cos(ang), LRO * math.sin(ang))], "COBERTURA")
    for z in (2.6, 3.0, 3.4, 3.8, 4.2):
        d = lodge_d(z); msp.add_circle((0, 0), d, dxfattribs={"layer": "COBERTURA_OCULTA"}); txt(msp, d * math.cos(1.75) - 0.1, d * math.sin(1.75) + 0.1, f"+{z:.2f}".replace(".", ","), h=0.1, align=TextEntityAlignment.MIDDLE_RIGHT)
    msp.add_circle((0, 0), L.R_LANTERN, dxfattribs={"layer": "ESQUADRIAS"}); msp.add_circle((0, 0), L.R_LANTERN + 0.25, dxfattribs={"layer": "COBERTURA"}); txt(msp, 0, -1.25, "LZ1 · Lanterna Zion Ø1,50 · cume +5,20", h=0.12)
    pl(msp, L.vertices(LRO - 0.12), "ESTRUTURA", close=True)
    for k in (1, 3, 5, 7):
        (px, py) = LV[k]; msp.add_circle((px, py), 0.06, dxfattribs={"layer": "ESTRUTURA"}); txt(msp, px * 1.1, py * 1.1 + (0.2 if py > 0 else -0.2), "TQ Ø75", h=0.1)
    pl(msp, L.deck_pts(), "DECK", close=True); lodge_sail_plan(msp)
    dim_h(msp, -LRE, LRE, -6.6, -0.5, "8,60"); dim_v(msp, 5.5, -LRE, LRE, 0.6, "8,60"); dim_v(msp, 5.5, -6.0, 6.0, 1.4, "12,00")
    title(msp, -7.5, 8.0, "ZION LODGE · PLANTA DE COBERTURA · 8 gomos radiais, curvas a cada 0,40 m, calha oculta na borda, TQ Ø75 em 4 pilares · 1:50")

def lodge_corte_long(msp):
    """corte A-A pelo eixo y = 0 (olhar para +y): deck e vela à esquerda, banho à direita."""
    pl(msp, [(-7.5, -0.6), (6.0, -0.6)], "TEXTO")
    for px in L_PX: pl(msp, [(px, -0.2), (px, -2.0)], "FUNDACAO")
    pl(msp, [(-6.0, -0.2), (3.4, -0.2), (3.4, 0), (-6.0, 0)], "DECK", close=True); lodge_stairs_side(msp)
    for x in (-3.4, 3.4): rect(msp, x - 0.06, 0, x + 0.06, L.Z_EAVE, "ESTRUTURA")
    rect(msp, -3.4, L.Z_EAVE - 0.15, 3.4, L.Z_EAVE, "ESTRUTURA")
    for r in L.rafters():
        if r[0][1] > 0: pl(msp, [(x, z) for (x, y, z) in r], "ESTRUTURA")
    pl(msp, [(-3.4, 0), (-3.4, D_H := L.DOOR["h"])], "ESQUADRIAS"); pl(msp, [(-3.4, D_H), (-3.4, L.Z_EAVE - 0.15)], "ESQUADRIAS")
    for (z1, z2) in ((0, 1.6), (2.2, L.Z_EAVE - 0.15)):
        rect(msp, 3.3, z1, 3.4, z2, "PAREDES"); msp.add_hatch(color=8, dxfattribs={"layer": "HACHURA"}).paths.add_polyline_path([(3.3, z1), (3.4, z1), (3.4, z2), (3.3, z2)], is_closed=True)
    rect(msp, 3.3, 1.6, 3.4, 2.2, "ESQUADRIAS")
    rect(msp, L.X_PART, 0, L.X_PART + 0.1, 2.4, "PAREDES"); rect(msp, L.X_PART, 0, L.X_PART + 0.1, 2.1, "ESQUADRIAS")
    pl(msp, [(L.X_PART, 2.4), (3.4, 2.4)], "COBERTURA_OCULTA"); pl(msp, [(L.X_PART, 2.45), (3.4, 2.45)], "COBERTURA_OCULTA")
    pl(msp, lodge_profile(), "COBERTURA"); pl(msp, [(x, z - 0.22) for (x, z) in lodge_profile() if -3.4 <= x <= L.X_PART], "COBERTURA_OCULTA")
    lodge_lantern(msp)
    px = L.sail_posts()[0][0]; rect(msp, px - 0.05, 0, px + 0.05, L.SAIL["z_post"], "ESTRUTURA"); pl(msp, [(px, L.SAIL["z_post"]), (-3.4, L.Z_EAVE + 0.15)], "COBERTURA")
    for it in L.furniture():
        if it["kind"] in ("pillow", "ceiling", "wall", "opening", "glass"): continue
        if "r" in it:
            if abs(it["y"]) <= it["r"]: rect(msp, it["x"] - it["r"], it["z1"], it["x"] + it["r"], it["z2"], "MOBILIARIO")
        elif it["y1"] <= 0 <= it["y2"]: rect(msp, it["x1"], it["z1"], it["x2"], it["z2"], "MOBILIARIO")
    dim_h(msp, -6.0, -3.4, -2.3, -0.5, "2,60"); dim_h(msp, -3.4, 3.4, -2.3, -0.5, "6,80"); dim_h(msp, -LRE, LRE, -2.3, -1.1, "8,60")
    dim_v(msp, 5.2, 0, L.Z_TOP, 0.6, "5,20"); dim_v(msp, 5.2, 0, L.Z_EAVE, 1.4, "2,70"); dim_v(msp, 5.2, 0, 2.4, 2.2, "2,40 (forro banho)")
    title(msp, -7.5, 6.6, "ZION LODGE · CORTE LONGITUDINAL A-A (y = 0, olhar para +y) · 1:50")

def lodge_corte_transv(msp):
    """corte B-B pelo eixo x = 0 (olhar para -x, a frente): deck, porta PC1 e vela vistos além."""
    pl(msp, [(-7.5, -0.6), (7.5, -0.6)], "TEXTO")
    for py in (-3.4, -2.55, -0.85, 0.85, 2.55, 3.4): pl(msp, [(py, -0.2), (py, -2.0)], "FUNDACAO")
    pl(msp, [(-6.0, -0.2), (6.0, -0.2), (6.0, 0), (-6.0, 0)], "DECK", close=True)
    for s in (-1, 1): pl(msp, [(s * 3.4, 0), (s * 3.4, L.Z_EAVE - 0.15)], "ESQUADRIAS")
    for y in (-3.4, -1.408, 1.408, 3.4): rect(msp, y - 0.06, 0, y + 0.06, L.Z_EAVE, "ESTRUTURA")
    rect(msp, -3.4, L.Z_EAVE - 0.15, 3.4, L.Z_EAVE, "ESTRUTURA")
    for r in L.rafters():
        if r[0][0] < 0: pl(msp, [(y, z) for (x, y, z) in r], "ESTRUTURA")
    rect(msp, -1.0, 0, 1.0, L.DOOR["h"], "ESQUADRIAS"); pl(msp, [(0, 0), (0, L.DOOR["h"])], "ESQUADRIAS")
    pl(msp, lodge_profile(), "COBERTURA"); pl(msp, [(y, z - 0.22) for (y, z) in lodge_profile() if abs(y) <= 3.4], "COBERTURA_OCULTA")
    lodge_lantern(msp)
    for py in (-1.8, 1.8): rect(msp, py - 0.05, 0, py + 0.05, L.SAIL["z_post"], "ESTRUTURA")
    pl(msp, [(-1.8, L.SAIL["z_post"]), (1.8, L.SAIL["z_post"]), (1.408, L.Z_EAVE + 0.15), (-1.408, L.Z_EAVE + 0.15)], "COBERTURA", close=True)
    for it in L.furniture():
        if it["kind"] in ("pillow", "ceiling", "wall", "opening", "glass") or "r" in it: continue
        if it["x1"] <= 0 <= it["x2"]: rect(msp, it["y1"], it["z1"], it["y2"], it["z2"], "MOBILIARIO")
    dim_h(msp, -3.4, 3.4, -2.3, -0.5, "6,80"); dim_h(msp, -6.0, 6.0, -2.3, -1.1, "12,00 (deck)")
    dim_v(msp, 6.8, 0, L.Z_TOP, 0.6, "5,20"); dim_v(msp, 6.8, 0, L.Z_EAVE, 1.4, "2,70")
    title(msp, -7.5, 6.6, "ZION LODGE · CORTE TRANSVERSAL B-B (x = 0, olhar para -x) · 1:50")

def lodge_fachada(msp, which):
    if which in ("frontal", "traseira"):
        front = which == "frontal"
        pl(msp, [(-7.5, -0.6), (7.5, -0.6)], "TEXTO")
        for py in L_PY: pl(msp, [(py, -0.2), (py, -2.0)], "FUNDACAO")
        pl(msp, [(-6.0, -0.2), (6.0, -0.2), (6.0, 0), (-6.0, 0)], "DECK", close=True)
        for y in (-3.4, -1.408, 1.408, 3.4): rect(msp, y - 0.06, 0, y + 0.06, L.Z_EAVE, "ESTRUTURA")
        rect(msp, -3.4, L.Z_EAVE - 0.15, 3.4, L.Z_EAVE, "ESTRUTURA")
        if front:
            for i in range(1, 3): rect(msp, -1.2, -0.2 * (i + 1), 1.2, -0.2 * i, "DECK")
            rect(msp, -3.4, 0, 3.4, L.Z_EAVE - 0.15, "ESQUADRIAS")
            for y in (-1.408, 1.408): pl(msp, [(y, 0), (y, L.Z_EAVE - 0.15)], "ESQUADRIAS")
            rect(msp, -1.0, 0, 1.0, L.DOOR["h"], "ESQUADRIAS"); pl(msp, [(0, 0), (0, L.DOOR["h"])], "ESQUADRIAS")
            for py in (-1.8, 1.8): rect(msp, py - 0.05, 0, py + 0.05, L.SAIL["z_post"], "ESTRUTURA")
            pl(msp, [(-1.8, L.SAIL["z_post"]), (1.8, L.SAIL["z_post"]), (1.408, L.Z_EAVE + 0.15), (-1.408, L.Z_EAVE + 0.15)], "COBERTURA", close=True)
        else:
            lodge_wall_panel(msp, -3.4, -1.408); lodge_wall_panel(msp, -1.408, 1.408); lodge_wall_panel(msp, 1.408, 3.4)
            rect(msp, -0.8, 1.6, 0.8, 2.2, "ESQUADRIAS"); rect(msp, -2.2, 0, -1.5, 0.62, "MOBILIARIO")
        lodge_roof_elev(msp, axis="y", depth_sign=-1 if front else 1)
        dim_h(msp, -3.4, 3.4, -2.3, -0.5, "6,80"); dim_h(msp, -6.0, 6.0, -2.3, -1.1, "12,00 (deck)"); dim_v(msp, 6.8, 0, L.Z_TOP, 0.6, "5,20"); dim_v(msp, 6.8, 0, L.Z_EAVE, 1.4, "2,70")
        title(msp, -7.5, 6.6, f"ZION LODGE · FACHADA {which.upper()} · " + ("olhar para +x (vista do deck e da vela)" if front else "olhar para -x (faces opacas, fresta J1, condensadora); y crescente para a esquerda") + " · 1:50")
    else:
        side = -1 if which == "direita" else 1
        pl(msp, [(-7.5, -0.6), (6.0, -0.6)], "TEXTO")
        for px in L_PX: pl(msp, [(px, -0.2), (px, -2.0)], "FUNDACAO")
        pl(msp, [(-6.0, -0.2), (3.4, -0.2), (3.4, 0), (-6.0, 0)], "DECK", close=True); lodge_stairs_side(msp)
        rect(msp, -3.4, 0, 1.408, L.Z_EAVE - 0.15, "ESQUADRIAS"); pl(msp, [(-1.408, 0), (-1.408, L.Z_EAVE - 0.15)], "ESQUADRIAS")
        lodge_wall_panel(msp, 1.408, 3.4)
        for x in (-3.4, -1.408, 1.408, 3.4): rect(msp, x - 0.06, 0, x + 0.06, L.Z_EAVE, "ESTRUTURA")
        rect(msp, -3.4, L.Z_EAVE - 0.15, 3.4, L.Z_EAVE, "ESTRUTURA")
        lodge_roof_elev(msp, axis="x", depth_sign=side)
        px = L.sail_posts()[0][0]; rect(msp, px - 0.05, 0, px + 0.05, L.SAIL["z_post"], "ESTRUTURA")
        pl(msp, [(px, L.SAIL["z_post"]), (-3.4, L.Z_EAVE + 0.15), (-3.4, L.Z_EAVE + 0.05), (px, L.SAIL["z_post"] - 0.08)], "COBERTURA", close=True)
        rect(msp, 4.3, 0, 5.0, 0.62, "MOBILIARIO")
        dim_h(msp, -6.0, -3.4, -2.3, -0.5, "2,60"); dim_h(msp, -3.4, 3.4, -2.3, -0.5, "6,80"); dim_h(msp, -LRE, LRE, -2.3, -1.1, "8,60")
        dim_v(msp, 6.0, 0, L.Z_TOP, 0.6, "5,20"); dim_v(msp, 6.0, 0, L.Z_EAVE, 1.4, "2,70")
        title(msp, -7.5, 6.6, "ZION LODGE · FACHADA LATERAL " + ("DIREITA (olhar para +y)" if side < 0 else "ESQUERDA (olhar para -y; espelhar ao plotar)") + " · VF2 + VF3 de vidro, painel ripado da cabeceira · 1:50")

def lodge_3d(msp):
    m = L.roof_mesh(14, 64); V = m["vertices"]
    for f in m["faces"]:
        a, b, c = V[f[0]], V[f[1]], V[f[2]]; msp.add_3dface([a, b, c, c], dxfattribs={"layer": "MEMBRANA_3D"})
    for w in L.walls():
        (xa, ya), (xb, yb) = w["p1"], w["p2"]
        msp.add_3dface([(xa, ya, w["z1"]), (xb, yb, w["z1"]), (xb, yb, w["z2"]), (xa, ya, w["z2"])], dxfattribs={"layer": "VIDRO_3D" if w["kind"] in ("glass", "window") else "PAREDES"})
    for r in L.rafters(): msp.add_polyline3d(r, dxfattribs={"layer": "ACO_3D"})
    for (x, y) in L.columns(): msp.add_polyline3d([(x, y, 0), (x, y, L.Z_EAVE)], dxfattribs={"layer": "ACO_3D"})
    ring = [(x, y, L.Z_EAVE) for (x, y) in LV]; msp.add_polyline3d(ring + [ring[0]], dxfattribs={"layer": "ACO_3D"})
    ang = np.linspace(0, 2 * math.pi, 33)
    for (r, z, layer) in ((L.R_LANTERN, L.Z_LANTERN, "ACO_3D"), (L.R_LANTERN, L.Z_TOP - 0.15, "ACO_3D"), (L.R_LANTERN + 0.25, L.Z_TOP, "MEMBRANA_3D")):
        msp.add_polyline3d([(r * math.cos(a), r * math.sin(a), z) for a in ang], dxfattribs={"layer": layer})
    for i in range(32):   # anel de vidro da lanterna e tampa cônica
        a0, a1 = ang[i], ang[i + 1]
        msp.add_3dface([(L.R_LANTERN * math.cos(a0), L.R_LANTERN * math.sin(a0), L.Z_LANTERN), (L.R_LANTERN * math.cos(a1), L.R_LANTERN * math.sin(a1), L.Z_LANTERN),
                        (L.R_LANTERN * math.cos(a1), L.R_LANTERN * math.sin(a1), L.Z_TOP - 0.15), (L.R_LANTERN * math.cos(a0), L.R_LANTERN * math.sin(a0), L.Z_TOP - 0.15)], dxfattribs={"layer": "VIDRO_3D"})
        ro = L.R_LANTERN + 0.25
        msp.add_3dface([(0, 0, L.Z_TOP + 0.1), (ro * math.cos(a0), ro * math.sin(a0), L.Z_TOP), (ro * math.cos(a1), ro * math.sin(a1), L.Z_TOP), (0, 0, L.Z_TOP + 0.1)], dxfattribs={"layer": "MEMBRANA_3D"})
    sp = L.sail_posts()
    for (x, y) in sp: msp.add_polyline3d([(x, y, -0.2), (x, y, L.SAIL["z_post"])], dxfattribs={"layer": "ACO_3D"})
    msp.add_3dface([(sp[0][0], sp[0][1], L.SAIL["z_post"]), (sp[1][0], sp[1][1], L.SAIL["z_post"]), (LV[3][0], LV[3][1], L.Z_EAVE + 0.15), (LV[4][0], LV[4][1], L.Z_EAVE + 0.15)], dxfattribs={"layer": "MEMBRANA_3D"})
    deck = [(x, y, 0.0) for (x, y) in L.deck_pts()]; msp.add_polyline3d(deck + [deck[0]], dxfattribs={"layer": "DECK"})
    floor = [(x, y, 0.0) for (x, y) in LV]; msp.add_polyline3d(floor + [floor[0]], dxfattribs={"layer": "PAREDES"})
    for (x, y) in L.piles(): msp.add_polyline3d([(x, y, -0.2), (x, y, -2.0)], dxfattribs={"layer": "FUNDACAO"})
    for it in L.furniture():
        if "r" in it or it["kind"] in ("pillow", "ceiling", "opening"): continue
        x1, x2, y1, y2, z1, z2 = it["x1"], it["x2"], it["y1"], it["y2"], it["z1"], it["z2"]
        P = [(x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1), (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2)]
        for f in ((0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            msp.add_3dface([P[i] for i in f], dxfattribs={"layer": "PAREDES" if it["kind"] == "wall" else "MOBILIARIO"})

# ============================================================================ build
def save(fn, draw, **kw):
    doc = new_doc(); msp = doc.modelspace(); draw(msp, **kw)
    doc.saveas(fn); return fn

def build():
    out = []
    d = os.path.join(ROOT, "cocoon", "projeto", "dxf"); os.makedirs(d, exist_ok=True)
    out += [save(os.path.join(d, "ZC-02_planta_baixa_cotada.dxf"), cocoon_planta, layout=False), save(os.path.join(d, "ZC-03_planta_layout.dxf"), cocoon_planta, layout=True),
            save(os.path.join(d, "ZC-04_planta_cobertura.dxf"), cocoon_cobertura), save(os.path.join(d, "ZC-06a_corte_longitudinal.dxf"), cocoon_corte_long),
            save(os.path.join(d, "ZC-06b_corte_transversal.dxf"), cocoon_corte_transv), save(os.path.join(d, "ZC-07_fachada_frontal.dxf"), cocoon_fachada_frontal),
            save(os.path.join(d, "ZC-08a_fachada_lateral_direita.dxf"), cocoon_fachada_lateral, side=-1), save(os.path.join(d, "ZC-08b_fachada_lateral_esquerda.dxf"), cocoon_fachada_lateral, side=1),
            save(os.path.join(d, "ZC-10_planta_estrutural.dxf"), cocoon_estrutura), save(os.path.join(d, "ZC-3D_modelo.dxf"), cocoon_3d)]
    d = os.path.join(ROOT, "zenith", "projeto", "dxf"); os.makedirs(d, exist_ok=True)
    out += [save(os.path.join(d, "ZS-02_planta_baixa_cotada.dxf"), zenith_planta, layout=False), save(os.path.join(d, "ZS-03_planta_layout.dxf"), zenith_planta, layout=True),
            save(os.path.join(d, "ZS-04_planta_cobertura.dxf"), zenith_cobertura), save(os.path.join(d, "ZS-06a_corte_longitudinal.dxf"), zenith_corte_long),
            save(os.path.join(d, "ZS-06b_corte_transversal.dxf"), zenith_corte_transv), save(os.path.join(d, "ZS-07a_fachada_frontal.dxf"), zenith_fachada, which="frontal"),
            save(os.path.join(d, "ZS-07b_fachada_traseira.dxf"), zenith_fachada, which="traseira"), save(os.path.join(d, "ZS-08a_fachada_lateral_direita.dxf"), zenith_fachada, which="direita"),
            save(os.path.join(d, "ZS-08b_fachada_lateral_esquerda.dxf"), zenith_fachada, which="esquerda"), save(os.path.join(d, "ZS-10_planta_estrutural.dxf"), zenith_estrutura),
            save(os.path.join(d, "ZS-3D_modelo.dxf"), zenith_3d)]
    d = os.path.join(ROOT, "lodge", "projeto", "dxf"); os.makedirs(d, exist_ok=True)
    out += [save(os.path.join(d, "ZL-02_planta_baixa_cotada.dxf"), lodge_planta, layout=False), save(os.path.join(d, "ZL-03_planta_layout.dxf"), lodge_planta, layout=True),
            save(os.path.join(d, "ZL-04_planta_cobertura.dxf"), lodge_cobertura), save(os.path.join(d, "ZL-06a_corte_longitudinal.dxf"), lodge_corte_long),
            save(os.path.join(d, "ZL-06b_corte_transversal.dxf"), lodge_corte_transv), save(os.path.join(d, "ZL-07a_fachada_frontal.dxf"), lodge_fachada, which="frontal"),
            save(os.path.join(d, "ZL-07b_fachada_traseira.dxf"), lodge_fachada, which="traseira"), save(os.path.join(d, "ZL-08a_fachada_lateral_direita.dxf"), lodge_fachada, which="direita"),
            save(os.path.join(d, "ZL-08b_fachada_lateral_esquerda.dxf"), lodge_fachada, which="esquerda"), save(os.path.join(d, "ZL-10_planta_estrutural.dxf"), lodge_estrutura),
            save(os.path.join(d, "ZL-3D_modelo.dxf"), lodge_3d)]
    for f in out: print(os.path.relpath(f, ROOT), round(os.path.getsize(f) / 1024), "kB")

if __name__ == "__main__":
    build()

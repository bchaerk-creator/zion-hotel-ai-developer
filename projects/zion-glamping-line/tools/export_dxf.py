# -*- coding: utf-8 -*-
"""Exporta o projeto arquitetônico para DXF (AutoCAD 2010) editável em CAD, a partir da geometria paramétrica.
Unidades: metros. Layers: EIXOS, PAREDES, ESQUADRIAS, MOBILIARIO, ESTRUTURA, COBERTURA, DECK, COTAS, TEXTO, 3D.
Arquivos gerados em <produto>/projeto/dxf/: planta baixa, planta estrutural, cobertura, cortes, fachadas e modelo 3D.
Uso: python3 export_dxf.py"""
import math, os
import numpy as np
import ezdxf
from ezdxf.enums import TextEntityAlignment
from geometry import Cocoon, Zenith
from drawings_extra import cocoon_pile_grid, zenith_pile_grid, zenith_tension_piles

C, Z = Cocoon(), Zenith()
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

def title(msp, x, y, s):
    txt(msp, x, y, s, h=0.35, align=TextEntityAlignment.MIDDLE_LEFT)

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

# ============================================================================ COCOON
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
    title(msp, -3.7, 5.6, "ZION COCOON · PLANTA BAIXA" + (" (LAYOUT)" if layout else " (COTADA)") + " · escala 1:50 · unidades em metros")

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
    title(msp, -3.7, 5.6, "ZION COCOON · PLANTA ESTRUTURAL (arcos, terças, trilhos, vigas de piso, estacas) · 1:50")

def cocoon_cobertura(msp):
    shell = [(x, -C.a(x)) for x in np.linspace(0.5, C.L, 120)] + [(x, C.a(x)) for x in np.linspace(C.L, 0.5, 120)]
    pl(msp, shell, "COBERTURA", close=True); pl(msp, [(x, y) for (x, y, z) in C.front_ring(80)], "COBERTURA")
    for x in C.ARCH_X: pl(msp, [(px, py) for (px, py, pz) in C.section_curve(x, 60)], "COBERTURA_OCULTA")
    x1, x2, ht = C.SPINE; hw = ht * C.B_MAX; rect(msp, C.shear(x1, 4.15), -hw, C.shear(x2, 4.15), hw, "ESQUADRIAS")
    for s in (1, -1): pl(msp, [(x, s * (C.floor_hw(x) + 0.08)) for x in np.linspace(0.9, 9.3, 60)], "ESTRUTURA")
    for (qx, qy) in [(0.95, -2.75), (0.95, 2.75), (9.25, -1.2), (9.25, 1.2)]: msp.add_circle((qx, qy), 0.06, dxfattribs={"layer": "ESTRUTURA"}); txt(msp, qx, qy + 0.3, "TQ Ø75", h=0.1)
    D = C.DECK; rect(msp, D["x1"], D["y1"], D["x2"], D["y2"], "DECK")
    dim_h(msp, -0.15, 9.6, -3.9, -0.5, "9,75"); dim_v(msp, 10.2, -3.0, 3.0, 0.6, "6,00")
    title(msp, -3.7, 5.6, "ZION COCOON · PLANTA DE COBERTURA · calha oculta no rodapé, TQ Ø75, Espinha de Luz · 1:50")

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
    title(msp, -3.7, 5.6, "ZION COCOON · CORTE LONGITUDINAL A-A · 1:50")

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
    title(msp, -4.5, 5.6, f"ZION COCOON · CORTE TRANSVERSAL B-B (x = {xc:.2f} m) · 1:50".replace(".", ","))

def cocoon_fachada_frontal(msp):
    ring = [(y, z) for (x, y, z) in C.front_ring(100)]; pl(msp, ring, "COBERTURA")
    glass = [(y, z) for (x, y, z) in C.glass_ring(100)]; pl(msp, glass, "ESQUADRIAS")
    for yy in (-1.6, -0.5, 0.5, 1.6):
        zt = C.ZC + (C.b(C.X_GLASS) - 0.06) * math.sqrt(max(0, 1 - (yy / (C.a(C.X_GLASS) - 0.06)) ** 2)); pl(msp, [(yy, 0), (yy, zt)], "ESQUADRIAS")
    pl(msp, [(-2.5, 2.4), (2.5, 2.4)], "ESQUADRIAS"); rect(msp, 0.6, 0, 1.6, 2.4, "ESQUADRIAS")
    D = C.DECK; rect(msp, D["y1"], -0.2, D["y2"], 0, "DECK"); pl(msp, [(-4.5, -0.6), (4.5, -0.6)], "TEXTO")
    for y in (-2.4, 0, 2.4): pl(msp, [(y, -0.2), (y, -2.0)], "FUNDACAO")
    dim_h(msp, -3.0, 3.0, -2.3, -0.5, "6,00"); dim_v(msp, 3.8, 0, 4.13, 0.6, "4,13")
    title(msp, -4.5, 5.6, "ZION COCOON · FACHADA FRONTAL (vista de fora, y crescente para a esquerda) · 1:50")

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
    title(msp, -3.7, 5.6, "ZION COCOON · FACHADA LATERAL " + ("DIREITA (olhar para +y)" if side < 0 else "ESQUERDA (olhar para -y; espelhar ao plotar)") + " · 1:50")

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

# ============================================================================ ZENITH
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
    title(msp, -3.0, 5.8, "ZION ZENITH · PLANTA BAIXA" + (" (LAYOUT)" if layout else " (COTADA)") + " · escala 1:50 · unidades em metros")

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
    title(msp, -3.0, 5.8, "ZION ZENITH · PLANTA ESTRUTURAL (pilares, anel de beiral, mastros, postes estaiados, vigas, estacas) · 1:50")

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
    title(msp, -3.0, 5.8, "ZION ZENITH · PLANTA DE COBERTURA · curvas de nível a cada 0,40 m · 1:50")

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
    title(msp, -3.0, 6.6, f"ZION ZENITH · CORTE LONGITUDINAL A-A (y = {y:.2f} m) · 1:50".replace(".", ","))

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
    title(msp, -4.5, 6.6, f"ZION ZENITH · CORTE TRANSVERSAL B-B (x = {x:.2f} m) · 1:50".replace(".", ","))

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
        title(msp, -4.5, 6.6, f"ZION ZENITH · FACHADA {which.upper()} · 1:50")
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
        title(msp, -3.0, 6.6, f"ZION ZENITH · FACHADA LATERAL {which.upper()}" + (" (olhar para -y; espelhar ao plotar)" if which == "esquerda" else " (olhar para +y)") + " · 1:50")

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
    out += [save(os.path.join(d, "ZZ-02_planta_baixa_cotada.dxf"), zenith_planta, layout=False), save(os.path.join(d, "ZZ-03_planta_layout.dxf"), zenith_planta, layout=True),
            save(os.path.join(d, "ZZ-04_planta_cobertura.dxf"), zenith_cobertura), save(os.path.join(d, "ZZ-06a_corte_longitudinal.dxf"), zenith_corte_long),
            save(os.path.join(d, "ZZ-06b_corte_transversal.dxf"), zenith_corte_transv), save(os.path.join(d, "ZZ-07a_fachada_frontal.dxf"), zenith_fachada, which="frontal"),
            save(os.path.join(d, "ZZ-07b_fachada_traseira.dxf"), zenith_fachada, which="traseira"), save(os.path.join(d, "ZZ-08a_fachada_lateral_direita.dxf"), zenith_fachada, which="direita"),
            save(os.path.join(d, "ZZ-08b_fachada_lateral_esquerda.dxf"), zenith_fachada, which="esquerda"), save(os.path.join(d, "ZZ-10_planta_estrutural.dxf"), zenith_estrutura),
            save(os.path.join(d, "ZZ-3D_modelo.dxf"), zenith_3d)]
    for f in out: print(os.path.relpath(f, ROOT), round(os.path.getsize(f) / 1024), "kB")

if __name__ == "__main__":
    build()

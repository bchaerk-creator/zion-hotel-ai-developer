# -*- coding: utf-8 -*-
"""Família ZION LODGE (38, 24 e 28): prancha de conceito paramétrica (planta, corte, fachada, dados) e vista isométrica
para qualquer variante de geometry.Lodge. Saídas: <code>/desenhos/01_conceito.svg e <code>/desenhos/08_isometrica.svg.
Uso: python3 lodge_family.py [lodge|lodge24|lodge28 ...]"""
import math, os, sys
import numpy as np
from geometry import LODGES
from svgkit import *
from drawings_cocoon import draw_furniture

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TAGLINE = {"lodge": "Pavilhão octogonal de 6,80 m entre faces com Lanterna Zion, cinco faces de vidro, banho no segmento posterior e deck em três faces com vela de sombra",
           "lodge24": "Octógono compacto de 5,40 m entre faces, três faces de vidro voltadas à paisagem, banho no segmento posterior, deck de uma face com vela de sombra",
           "lodge28": "Octógono alongado 4,20 x 7,80 m com duas lanternas em cumeeira, cinco faces de vidro, banho no fundo e deck em três faces com vela de sombra"}
POS = {"lodge": "Unidade de entrada da linha", "lodge24": "Unidade compacta para casal", "lodge28": "Unidade alongada com terraço"}

def faces_glass(L): return L.GLASS_FACES
def faces_wall(L): return L.WALL_FACES

def x_front(L): return -(L.F / 2 + L.M / 2)
def x_rear(L): return (L.F / 2 + L.M / 2)

def roof_profile_x(L, n=60):
    """perfil da cobertura no plano y = 0 (x, z)."""
    x0 = x_front(L) - L.OVER; x1 = x_rear(L) + L.OVER; out = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        d = max(0.0, abs(x) - L.M / 2)
        out.append((x, L.roof_z(d) if d > L.R_LANTERN else L.Z_LANTERN))
    return out

def roof_profile_y(L, n=60):
    """silhueta frontal (y, z)."""
    y1 = L.F / 2 + L.OVER; out = []
    for i in range(n + 1):
        y = -y1 + 2 * y1 * i / n
        out.append((y, L.roof_z(abs(y)) if abs(y) > L.R_LANTERN else L.Z_LANTERN))
    return out

# ----------------------------------------------------------------------------- planta
def planta(sh, L):
    V = L.vertices(); R = L.r_corner(); Vo = L.vertices(R + L.OVER / math.cos(math.pi / 8))
    sh.poly(Vo, fill="none", stroke=GREEN, sw=0.8, dash="6 3")
    sh.poly(L.deck_pts(), fill=sh.pattern("deck"), stroke=GREEN, sw=1.0)
    posts = L.sail_posts(); px = posts[0][0]
    for (x, y) in posts: sh.circle(x, y, 0.06, fill=STEEL, stroke="none")
    sh.poly([V[3], posts[1], posts[0], V[4]], fill="none", stroke=GREEN, sw=0.7, dash="3 3")
    sh.text(px + 0.7, 0.0, "vela de sombra", 8.5, EARTH, rotate=-90)
    sh.poly(V, fill="#F7F1E6", stroke=GREEN, sw=1.6)
    for (i, j) in faces_glass(L): sh.line(V[i][0], V[i][1], V[j][0], V[j][1], GLASS, 6); sh.line(V[i][0], V[i][1], V[j][0], V[j][1], GREEN, 0.9)
    for (i, j) in faces_wall(L): sh.line(V[i][0], V[i][1], V[j][0], V[j][1], WOOD2, 8); sh.line(V[i][0], V[i][1], V[j][0], V[j][1], GREEN, 0.9)
    for (x, y) in V: sh.rect(x - 0.08, y - 0.08, x + 0.08, y + 0.08, fill=STEEL, stroke="none")
    xf = x_front(L); d = L.DOOR
    sh.line(xf + 0.05, d["y1"], xf + 0.05, d["y2"], CREAM, 6); sh.line(xf + 0.05, d["y1"], xf + 0.05, (d["y1"] + d["y2"]) / 2, GREEN, 2.2)
    sh.text(xf - 0.35, 0, "PC1 2,00 x 2,40", 8, GREEN, rotate=-90)
    draw_furniture(sh, L.furniture(), True)
    for it in L.furniture():
        if it["kind"] == "wall": sh.rect(it["x1"], it["y1"], it["x2"], it["y2"], fill=WOOD2, stroke=GREEN, sw=0.8)
        if it["kind"] == "opening": sh.rect(it["x1"], it["y1"], it["x2"], it["y2"], fill=CREAM, stroke="none"); sh.line((it["x1"] + it["x2"]) / 2, it["y1"], (it["x1"] + it["x2"]) / 2, it["y2"], GREEN, 0.6, dash="3 2")
    for (cx, cy) in L.lantern_centers():
        sh.circle(cx, cy, L.R_LANTERN, fill="none", stroke=GREEN, sw=0.8, dash="4 3")
    sh.text(L.lantern_centers()[-1][0], L.R_LANTERN + 0.25, f"LANTERNA Ø{fmt(2 * L.R_LANTERN)}" + (" (2 un.)" if L.M >= 0.5 else ""), 8, GREEN, spacing=0.1)
    bath = 6.9 if L.CODE == "lodge" else (5.0 if L.CODE == "lodge24" else 6.2)
    xb = (L.X_PART + x_rear(L)) / 2
    sh.text(xb, -L.F / 2 + 0.55, "BANHO", 9, GREEN, spacing=0.2); sh.text(xb, -L.F / 2 + 0.28, fmt(bath) + " m²", 7.5, EARTH)
    sh.text((xf + L.X_PART) / 2, -L.F / 2 + 0.55, "ESTAR + SUÍTE", 9, GREEN, spacing=0.2); sh.text((xf + L.X_PART) / 2, -L.F / 2 + 0.28, fmt(L.floor_area() - bath) + " m²", 7.5, EARTH)
    dk = L.deck_pts(); dx = min(p[0] for p in dk)
    sh.text((dx + xf) / 2, -0.9, "DECK", 9, GREEN, spacing=0.2); sh.text((dx + xf) / 2, -1.17, fmt(L.deck_area()) + " m²", 7.5, EARTH)
    yb = -L.F / 2 - 1.0
    sh.dim(x_front(L), yb, x_rear(L), yb, -0.4, label=fmt(x_rear(L) - x_front(L)) + (" (entre faces)" if L.M < 0.5 else " (comprimento)"))
    sh.dim(dx, yb, x_front(L), yb, -0.4, label=fmt(x_front(L) - dx) + " (deck)")
    xr = x_rear(L) + 1.2
    sh.dim(xr, -L.F / 2, xr, L.F / 2, 0.5, label=fmt(L.F))
    sh.dim(xr, L.X_PART, xr, x_rear(L), 1.2, label=fmt(x_rear(L) - L.X_PART) + " banho")
    ya = L.F / 2 + 1.2
    sh.text(dx - 0.6, ya + 0.2, "A", 12, GREEN, weight=700); sh.text(xr + 0.6, ya + 0.2, "A", 12, GREEN, weight=700)
    sh.line(dx - 0.6, ya, xr + 0.6, ya, GREEN, 0.8, dash="8 3")

# ----------------------------------------------------------------------------- corte
def corte(sh, L):
    xf, xr = x_front(L), x_rear(L); px = L.sail_posts()[0][0]
    sh.rect(px - 1.2, -0.6, xr + 1.6, -0.02, fill=sh.pattern("soil"), stroke="none"); sh.line(px - 1.2, -0.02, xr + 1.6, -0.02, GREEN, 1.0)
    for (x, y) in L.piles():
        if abs(y) < 0.3: sh.rect(x - 0.04, -0.6, x + 0.04, -0.2, fill=STEEL, stroke="none")
    sh.rect(px, -0.2, xr, -0.05, fill=WOOD2, stroke=GREEN, sw=0.9); sh.rect(px, -0.05, xr, 0.0, fill=GREEN, stroke="none")
    for x in (xf, xr): sh.rect(x - 0.06, 0, x + 0.06, L.Z_EAVE, fill=STEEL, stroke="none"); sh.rect(x - 0.12, 0, x + 0.12, L.Z_EAVE, fill="none", stroke=WOOD2, sw=1.2)
    sh.rect(xf - 0.1, L.Z_EAVE - 0.15, xr + 0.1, L.Z_EAVE, fill=STEEL, stroke="none")
    prof = roof_profile_x(L)
    sh.poly(prof, close=False, stroke=GREEN, sw=2.2)
    inner = [(x * 0.97, z - 0.22) for (x, z) in prof if xf <= x <= xr]
    sh.poly(inner, close=False, stroke=EARTH, sw=0.9, dash="4 3")
    for (cx, cy) in L.lantern_centers():
        sh.line(xf, L.Z_EAVE, cx - L.R_LANTERN, L.Z_LANTERN, STEEL, 3) if cx <= 0 else None
        sh.line(xr, L.Z_EAVE, cx + L.R_LANTERN, L.Z_LANTERN, STEEL, 3) if cx >= 0 else None
        sh.rect(cx - L.R_LANTERN, L.Z_LANTERN - 0.1, cx + L.R_LANTERN, L.Z_LANTERN, fill=STEEL, stroke="none")
        sh.rect(cx - L.R_LANTERN, L.Z_LANTERN, cx + L.R_LANTERN, L.Z_TOP - 0.15, fill=GLASS, stroke=GREEN, sw=0.9)
        sh.rect(cx - L.R_LANTERN - 0.25, L.Z_TOP - 0.15, cx + L.R_LANTERN + 0.25, L.Z_TOP, fill=MEMB, stroke=GREEN, sw=1.2)
    if L.M >= 0.5:
        c = L.lantern_centers(); sh.rect(c[0][0], L.Z_LANTERN - 0.1, c[1][0], L.Z_LANTERN, fill=STEEL, stroke="none")
    sh.line(px, 0, px, L.SAIL["z_post"], STEEL, 3); sh.line(px, L.SAIL["z_post"], xf, L.Z_EAVE + 0.15, GREEN, 1.8)
    sh.rect(xf + 0.06, 0, xf + 0.1, L.Z_EAVE - 0.15, fill=GLASS, stroke=GREEN, sw=0.6); sh.rect(xr - 0.1, 0, xr - 0.06, L.Z_EAVE - 0.15, fill=WOOD2, stroke=GREEN, sw=0.6)
    for it in L.furniture():
        if it["kind"] in ("pillow", "ceiling", "hvac", "condenser", "glass", "opening"): continue
        if "r" in it:
            if abs(it["y"]) < 0.6: sh.rect(it["x"] - it["r"], it["z1"], it["x"] + it["r"], it["z2"], fill="#FFFFFF", stroke=GREEN, sw=0.6)
            continue
        if it["y1"] <= 0.3 and it["y2"] >= -0.3:
            sh.rect(it["x1"], it["z1"], it["x2"], it["z2"], fill=WOOD2 if it["kind"] == "wall" else "#FFFFFF", stroke=GREEN, sw=0.7)
    sh.dim(xf, -1.0, xr, -1.0, -0.3, label=fmt(xr - xf)); sh.dim(px, -1.0, xf, -1.0, -0.3, label=fmt(xf - px))
    sh.dim(xr + 1.3, 0, xr + 1.3, L.Z_EAVE, 0.4, label=fmt(L.Z_EAVE) + " beiral"); sh.dim(xr + 1.3, 0, xr + 1.3, L.Z_TOP, 1.1, label=fmt(L.Z_TOP) + " lanterna")
    sh.dim(px - 0.6, 0, px - 0.6, L.SAIL["z_post"], -0.4, label=fmt(L.SAIL["z_post"]))

# ----------------------------------------------------------------------------- fachada
def fachada(sh, L):
    V = L.vertices(); yw = L.F / 2 + L.OVER
    sh.rect(-yw - 1.4, -0.6, yw + 1.4, -0.02, fill=sh.pattern("soil"), stroke="none"); sh.line(-yw - 1.4, -0.02, yw + 1.4, -0.02, GREEN, 1.0)
    dk = L.deck_pts(); ymax = max(p[1] for p in dk)
    sh.rect(-ymax, -0.2, ymax, -0.05, fill=WOOD2, stroke=GREEN, sw=0.9); sh.rect(-ymax, -0.05, ymax, 0.0, fill=GREEN, stroke="none")
    for y in (-ymax + 0.3, -L.F / 4, 0, L.F / 4, ymax - 0.3): sh.rect(y - 0.04, -0.6, y + 0.04, -0.2, fill=STEEL, stroke="none")
    ys = sorted(set(round(v[1], 3) for v in V if v[0] < 0))
    for k in range(len(ys) - 1):
        gl = any(round(V[i][1], 3) in (ys[k], ys[k + 1]) and round(V[j][1], 3) in (ys[k], ys[k + 1]) and V[i][0] < 0 and V[j][0] < 0 for (i, j) in faces_glass(L))
        sh.rect(ys[k], 0, ys[k + 1], L.Z_EAVE - 0.15, fill=GLASS if gl else "#C9B08C", stroke=GREEN, sw=0.9)
    for y in ys: sh.rect(y - 0.06, 0, y + 0.06, L.Z_EAVE, fill=STEEL, stroke="none")
    d = L.DOOR; sh.rect(d["y1"], 0, d["y2"], d["h"], fill="none", stroke=GREEN, sw=1.4); sh.line(0, 0, 0, d["h"], GREEN, 0.8)
    sh.rect(-L.F / 2 - 0.1, L.Z_EAVE - 0.15, L.F / 2 + 0.1, L.Z_EAVE, fill=STEEL, stroke="none")
    prof = roof_profile_y(L); sh.poly(prof, fill=MEMB, stroke=GREEN, sw=1.8)
    sh.rect(-L.R_LANTERN, L.Z_LANTERN, L.R_LANTERN, L.Z_TOP - 0.15, fill=GLASS, stroke=GREEN, sw=0.9)
    sh.rect(-L.R_LANTERN - 0.25, L.Z_TOP - 0.15, L.R_LANTERN + 0.25, L.Z_TOP, fill=MEMB, stroke=GREEN, sw=1.2)
    for s in (-1, 1):
        for yy in (L.F / 4, L.F / 2): sh.line(s * yy, L.Z_EAVE, s * min(yy, L.R_LANTERN * 0.7), L.Z_LANTERN - 0.05, EARTH, 0.5, dash="3 3", opacity=0.6)
    for (x, y) in L.sail_posts(): sh.line(y, 0, y, L.SAIL["z_post"], STEEL, 3)
    py = L.sail_posts()[1][1]
    sh.line(-py - 0.5, L.SAIL["z_post"] + 0.05, py + 0.5, L.SAIL["z_post"] + 0.05, GREEN, 2.0)
    sh.dim(yw + 0.9, 0, yw + 0.9, L.Z_TOP, 0.4, label=fmt(L.Z_TOP))
    sh.dim(-L.F / 2, -1.0, L.F / 2, -1.0, -0.3, label=fmt(L.F))

# ----------------------------------------------------------------------------- prancha
def concept_sheet(L, out):
    code = L.CODE
    dk = L.deck_pts(); dx = min(p[0] for p in dk); width = (x_rear(L) + 2.4) - (dx - 0.8)
    sc = min(56.0, 560.0 / width); ox = 100 - (dx - 0.8) * sc
    sh = Sheet(1600, 1000, scale=sc, ox=ox, oy=385)
    sh.header(f"{L.NAME.title()} · Conceito", TAGLINE[code] + " · estudo de conceito")
    planta(sh, L)
    sh.text_px(430, 92, "PLANTA", size=11, weight=700, spacing=0.25)
    sh.north(690, 140, angle=-90); sh.scalebar(dx - 0.6, L.F / 2 + 1.9, 5)
    sh.ox, sh.oy, sh.s = 1130, 430, 46
    corte(sh, L); sh.text_px(1130, 92, "CORTE A-A", size=11, weight=700, spacing=0.25)
    sh.ox, sh.oy, sh.s = 1330, 830, 42
    fachada(sh, L); sh.text_px(1330, 560, "FACHADA FRONTAL", size=11, weight=700, spacing=0.25)
    sh.ox, sh.oy, sh.s = ox, 385, sc
    V = L.vertices(); LX = max(p[0] for p in V) - min(p[0] for p in V)
    bath = 6.9 if code == "lodge" else (5.0 if code == "lodge24" else 6.2)
    rows = [("Planta", f"{'octógono regular' if L.M < 0.5 else 'octógono alongado'} · {fmt(L.F)} m entre faces · {fmt(LX)} m de comprimento"), ("Área interna", fmt(L.floor_area()) + f" m² (banho {fmt(bath)} m²)"),
            ("Deck frontal", fmt(L.deck_area()) + f" m² em {len(L.DECK_FACES) - 1} face(s) + vela de sombra"), ("Área total", fmt(L.floor_area() + L.deck_area()) + " m²"),
            ("Alturas", f"beiral {fmt(L.Z_EAVE)} m · lanterna {fmt(L.Z_LANTERN)} a {fmt(L.Z_TOP)} m"),
            ("Estrutura", f"8 pilares Ø101,6 revestidos em madeira · anel de beiral 150 x 100 · {len(L.rafters())} caibros Ø76 · anel de compressão da(s) lanterna(s)"),
            ("Envelope", "membrana PVDF 1050 g/m² em gomos · câmara ventilada · lã PET 50 mm · forro tensionado"),
            ("Fechamentos", f"{len(faces_glass(L))} faces de vidro insulado (alumínio bronze RPT) · {len(faces_wall(L))} faces em painel SIP + ripado"),
            ("Fundação", f"estacas helicoidais, {len(L.piles())} un. · deck em vigas U 150")]
    y0 = 640
    sh.text_px(60, y0, "DADOS DO PRODUTO", size=11, weight=700, spacing=0.25, anchor="start")
    for i, (k, v) in enumerate(rows):
        sh.text_px(60, y0 + 24 + i * 19, k.upper(), size=8.5, fill=EARTH, spacing=0.15, anchor="start"); sh.text_px(180, y0 + 24 + i * 19, v, size=10, anchor="start")
    dif = {"lodge": ["Lanterna Zion no cume: anel de vidro de 0,45 m que leva luz zenital ao centro da cama (a referência de mercado fecha o cume em ponta cega)",
                     "Vela de sombra sobre o deck: membrana independente em dois postes, prolongando a varanda sem tocar a cobertura principal",
                     "Cinco faces de vidro e três opacas: o banho ocupa o segmento posterior com banheira sob fresta alta; a cama fica no centro geométrico, sob a lanterna",
                     "Mesmo Zion Shell System das unidades Casulo e Safari: kit parafusado, sem solda em campo, 13 camadas, deck em estacas helicoidais"],
           "lodge24": ["Unidade compacta para casal: 24 m² com programa completo (cama king, café, closet, banho com chuveiro), no lugar da referência de 23 m² sem varanda",
                       "Três faces de vidro concentradas na paisagem e cinco opacas para privacidade em implantações densas (adensamento de 12 a 16 unidades/ha)",
                       "Lanterna Zion Ø1,20 sobre a cama e vela de sombra sobre um deck de uma face",
                       "Kit mais leve da linha: 8 pilares, 8 caibros, 15 estacas; montagem em 6 dias"],
           "lodge28": ["Octógono alongado de 7,80 m com duas Lanternas Zion em cumeeira: luz zenital sobre a cama e sobre o estar",
                       "Programa em sequência: deck em três faces, estar junto ao vidro, suíte ao centro, banho no fundo com fresta alta",
                       "Terraço de 17,5 m² com vela de sombra: a referência de mercado (26 m² + 17 m²) reinterpretada com beiral em balanço e sem estrutura aparente",
                       "Mesmo Zion Shell System: kit parafusado, 10 caibros, 21 estacas, montagem em 8 dias"]}[code]
    sh.text_px(760, y0, "DIFERENCIAIS · IDENTIDADE PRÓPRIA", size=11, weight=700, spacing=0.25, anchor="start")
    for i, t in enumerate(dif):
        words = t.split(); lines = []; cur = ""
        for w in words:
            if len(cur) + len(w) + 1 > 64: lines.append(cur); cur = w
            else: cur = (cur + " " + w).strip()
        lines.append(cur)
        sh.text_px(760, y0 + 24 + i * 44, f"{i + 1:02d}", size=9.5, weight=700, anchor="start")
        for k, Ln in enumerate(lines): sh.text_px(786, y0 + 24 + i * 44 + k * 13, Ln, size=9.5, anchor="start")
    sh.title_block(L.NAME, "Conceito · planta, corte, fachada", "escala gráfica (A1)", "01/LG", POS[code] + " · estudo de conceito R00")
    sh.save(out)

# ----------------------------------------------------------------------------- isométrica
def iso_sheet(L, out):
    from iso import Scene, add_furniture, ground_shadow
    sh = Sheet(1600, 1000)
    sh.header(f"{L.NAME.title()} · Vista isométrica", "Projeção isométrica a partir da frente e da lateral direita · sem escala")
    sc = Scene(sh, 78, 760, 640)
    V = L.vertices(); dk = L.deck_pts()
    ground_shadow(sc, 0.3, 0, L.r_corner() + L.M / 2 + 2.2, L.F / 2 + 1.6)
    # deck (prisma) e escada
    for i in range(1, len(dk) - 1): sc.tri((dk[0][0], dk[0][1], 0), (dk[i][0], dk[i][1], 0), (dk[i + 1][0], dk[i + 1][1], 0), "#B99A73", shade_on=False)
    for a, b in zip(dk, dk[1:] + dk[:1]): sc.quad((a[0], a[1], -0.2), (b[0], b[1], -0.2), (b[0], b[1], 0), (a[0], a[1], 0), "#A5885F")
    xmin = min(p[0] for p in dk)
    for i in range(3): sc.box(xmin - 0.3 * (i + 1), xmin - 0.3 * i, -1.0, 1.0, -0.2, -0.05 * (i + 1), "#B99A73")
    # piso
    for i in range(1, len(V) - 1): sc.tri((V[0][0], V[0][1], 0), (V[i][0], V[i][1], 0), (V[i + 1][0], V[i + 1][1], 0), "#C9AA7D", shade_on=False)
    add_furniture(sc, L.furniture())
    # paredes
    for w in L.walls():
        (xa, ya), (xb, yb) = w["p1"], w["p2"]
        col, op = {"glass": ("#9FB7C2", 0.35), "wood": ("#C9B08C", 1.0), "window": ("#9FB7C2", 0.5), "partition": ("#D9C4A3", 1.0)}[w["kind"]]
        sc.quad((xa, ya, w["z1"]), (xb, yb, w["z1"]), (xb, yb, w["z2"]), (xa, ya, w["z2"]), col, op)
    # pilares, anel, caibros
    for (x, y) in V:
        sc.cylinder(x, y, 0, L.Z_EAVE, 0.09, "#8B6B45")
    for a, b in zip(V, V[1:] + V[:1]): sc.polyline([(a[0], a[1], L.Z_EAVE), (b[0], b[1], L.Z_EAVE)], "#3A3B3A", 2.4)
    for r in L.rafters(): sc.polyline(r, "#3A3B3A", 1.8)
    # membrana e lanterna(s)
    m = L.roof_mesh(10, 48); sc.mesh(m["vertices"], m["faces"], "#EDE6D6", 0.92)
    for (cx, cy) in L.lantern_centers():
        sc.cylinder(cx, cy, L.Z_LANTERN, L.Z_TOP - 0.15, L.R_LANTERN, "#9FB7C2", opacity=0.6)
        sc.cylinder(cx, cy, L.Z_TOP - 0.15, L.Z_TOP, L.R_LANTERN + 0.25, "#E4DCCB")
    # vela
    P = L.sail_posts()
    for (x, y) in P: sc.cylinder(x, y, -0.05, L.SAIL["z_post"], 0.04, "#3A3B3A")
    sc.quad((P[0][0], P[0][1], L.SAIL["z_post"]), (P[1][0], P[1][1], L.SAIL["z_post"]), (V[3][0], V[3][1], L.Z_EAVE + 0.15), (V[4][0], V[4][1], L.Z_EAVE + 0.15), "#E9E1D0", 0.9)
    sc.render()
    notes = [f"Octógono {'alongado ' if L.M >= 0.5 else ''}de {fmt(L.F)} m entre faces · {fmt(L.floor_area())} m² internos", f"Deck de {fmt(L.deck_area())} m² com vela de sombra", f"Lanterna Zion Ø{fmt(2 * L.R_LANTERN)}" + (" (2 un.)" if L.M >= 0.5 else "") + f" · cume {fmt(L.Z_TOP)} m",
             f"{len(faces_glass(L))} faces de vidro · {len(faces_wall(L))} faces em painel ripado", "Membrana PVDF em gomos sobre caibros radiais", "8 pilares revestidos em madeira · anel de beiral"]
    for i, n in enumerate(notes):
        sh.callout_px(70, 760 + i * 22, i + 1); sh.text_px(90, 764 + i * 22, n, size=11, anchor="start")
    sh.title_block(L.NAME, "Vista isométrica", "sem escala", "08/LG", POS[L.CODE])
    sh.save(out)

def build(codes):
    for code in codes:
        L = LODGES[code](); d = os.path.join(ROOT, code, "desenhos"); os.makedirs(d, exist_ok=True)
        concept_sheet(L, os.path.join(d, "01_conceito.svg"))
        if code != "lodge": iso_sheet(L, os.path.join(d, "08_isometrica.svg"))   # o Lodge 38 tem isométrica própria em iso.py
        print(code, "ok")

if __name__ == "__main__":
    build(sys.argv[1:] or ["lodge24", "lodge28"])

# -*- coding: utf-8 -*-
"""ZION CÁPSULA: prancha de conceito (planta, corte longitudinal, seção transversal, fachada frontal, dados, diferenciais),
vista isométrica e lista de materiais estimados a partir de geometry.Capsule.
Saídas: capsule/desenhos/01_conceito.svg e capsule/desenhos/08_isometrica.svg.  Uso: python3 capsule.py"""
import math, os
import numpy as np
from geometry import Capsule
from svgkit import *
from drawings_cocoon import draw_furniture

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
C = Capsule()
TAGLINE = "Cápsula monocoque de 8,40 x 3,20 m com Visor panorâmico de vidro curvo, Anel de Luz sobre a cama e dois Olhos laterais · viaja inteira, pousa em quatro pés"
POS = "Unidade compacta transportável"
ALU = "#E6E0D4"; ALU2 = "#CFC7B8"

def rot_pts(pts): return [(x, y) for (x, y) in pts]

# ----------------------------------------------------------------------------- planta
def planta(sh):
    D = C.DECK
    sh.rect(D["x1"], D["y1"], D["x2"], D["y2"], fill=sh.pattern("deck"), stroke=GREEN, sw=1.0)
    for i in range(3): sh.rect(D["x1"] - 0.3 * (i + 1), -0.9, D["x1"] - 0.3 * i, 0.9, fill=WOOD, stroke=GREEN, sw=0.7)
    sh.text((D["x1"] + D["x2"]) / 2, -1.05, "DECK", 9, CREAM, spacing=0.2); sh.text((D["x1"] + D["x2"]) / 2, -1.32, fmt(C.deck_area()) + " m²", 7.5, CREAM)
    # casca externa e piso
    sh.poly(C.plan_outline(), fill="#F3EEE4", stroke=GREEN, sw=1.8)
    # Visor (calota de vidro)
    nose = [(x, y) for (x, y) in C.plan_outline() if x <= C.X_NOSE]
    sh.poly(nose, fill=GLASS, stroke=GREEN, sw=0.9, opacity=0.9)
    sh.text(0.55, 0.0, "VISOR", 8, GREEN, spacing=0.2, rotate=-90)
    sh.poly(C.floor_outline(), fill="#FBF8F2", stroke=GREEN, sw=0.9, dash="5 3")
    # anéis (projeção) e pés
    for x in C.RINGS: sh.line(x, -C.half_width(x), x, C.half_width(x), EARTH, 0.4, dash="2 3", opacity=0.6)
    for (x, y) in C.LEGS: sh.circle(x, y, 0.06, fill="none", stroke=STEEL, sw=1.0, dash="2 1.5")
    # Anel de Luz
    x1, x2 = C.LIGHT_RING; yr = C.A * math.sin(C.LIGHT_ANG) * 0.92
    sh.rect(x1, -yr, x2, yr, fill=GLASS, stroke=GREEN, sw=0.7, dash="4 2", opacity=0.55)
    sh.text((x1 + x2) / 2, yr + 0.3, "ANEL DE LUZ", 7.5, GREEN, spacing=0.15)
    # Olhos
    for p in C.PORTHOLES:
        y = p["side"] * (C.hw_at(p["x"], p["z"], inner=False) + 0.05)
        sh.circle(p["x"], y, p["r"] * 0.6, fill=GLASS, stroke=GREEN, sw=0.8)
        sh.text(p["x"] + 0.35, y + p["side"] * 0.12, p["name"].upper(), 7, GREEN, spacing=0.1, anchor="start")
    # mobiliário, parede e porta
    draw_furniture(sh, C.furniture(), True)
    for it in C.furniture():
        if it["kind"] == "wall": sh.rect(it["x1"], it["y1"], it["x2"], it["y2"], fill=WOOD2, stroke=GREEN, sw=0.8)
        if it["kind"] == "opening": sh.rect(it["x1"], it["y1"], it["x2"], it["y2"], fill=CREAM, stroke="none"); sh.line((it["x1"] + it["x2"]) / 2, it["y1"], (it["x1"] + it["x2"]) / 2, it["y2"], GREEN, 0.6, dash="3 2")
        if it["kind"] == "hvac": sh.rect(it["x1"], it["y1"], it["x2"], it["y2"], fill=sh.pattern("hatch"), stroke=GREEN, sw=0.6)
    d = C.DOOR; sh.line(0.22, d["y1"], 0.22, d["y2"], CREAM, 5); sh.line(0.22, 0, 0.22 + 0.9, 0, GREEN, 1.6)
    sh.add(f'<path d="M{sh.X(0.22):.1f},{sh.Y(0):.1f} A{0.9 * sh.s:.1f},{0.9 * sh.s:.1f} 0 0 0 {sh.X(0.22):.1f},{sh.Y(0.9):.1f}" fill="none" stroke="{GREEN}" stroke-width="0.6" stroke-dasharray="3 2"/>')
    sh.text(0.75, C.A + 0.32, "PV1 0,90 x 2,05 · porta pivotante", 7.5, GREEN, anchor="start")
    # ambientes
    for (x, lab, a) in ((2.0, "ESTAR", 7.6), (4.15, "SUÍTE", 6.9), (6.55, "BANHO", 4.4), (7.95, "TÉCNICO", 1.0)):
        sh.text(x, -C.A - 0.42 if x < 7.6 else 0, lab, 8.5 if x < 7.6 else 7, GREEN, spacing=0.2, rotate=0 if x < 7.6 else -90)
        if x < 7.6: sh.text(x, -C.A - 0.68, fmt(a) + " m²", 7.5, EARTH)
    # cotas
    yb = -C.A - 1.35
    sh.dim(0, yb, C.L, yb, -0.4, label=fmt(C.L)); sh.dim(D["x1"], yb, 0, yb, -0.4, label=fmt(-D["x1"]) + " (deck)")
    sh.dim(0, yb, C.X_NOSE, yb, 0.35, label="Visor " + fmt(C.X_NOSE), size=10); sh.dim(C.X_PART, yb, C.X_TECH, yb, 0.35, label="banho " + fmt(C.X_TECH - C.X_PART), size=10); sh.dim(C.X_TECH, yb, C.L, yb, 0.35, label="téc.", size=10)
    xr = C.L + 1.0
    sh.dim(xr, -C.A, xr, C.A, 0.5, label=fmt(2 * C.A)); sh.dim(xr, -C.floor_hw(4), xr, C.floor_hw(4), -0.3, label=fmt(2 * C.floor_hw(4)) + " piso")
    ya = C.A + 1.15
    sh.text(D["x1"] - 0.6, ya + 0.2, "A", 12, GREEN, weight=700); sh.text(xr + 0.5, ya + 0.2, "A", 12, GREEN, weight=700)
    sh.line(D["x1"] - 0.6, ya, xr + 0.5, ya, GREEN, 0.8, dash="8 3")
    xb = 4.15
    sh.text(xb, ya + 0.9, "B", 12, GREEN, weight=700); sh.text(xb, yb - 1.05, "B", 12, GREEN, weight=700)
    sh.line(xb, ya + 0.6, xb, yb - 0.8, GREEN, 0.8, dash="8 3")

# ----------------------------------------------------------------------------- corte longitudinal A-A
def corte(sh):
    D = C.DECK; x0 = D["x1"] - 1.4; x1 = C.L + 1.2; zg = C.Z_GROUND
    sh.rect(x0, zg - 0.6, x1, zg, fill=sh.pattern("soil"), stroke="none"); sh.line(x0, zg, x1, zg, GREEN, 1.0)
    # pés (atrás do plano de corte)
    for lg in C.legs():
        sh.rect(lg["x"] - lg["r"], zg, lg["x"] + lg["r"], lg["z2"], fill=STEEL, stroke="none"); sh.rect(lg["x"] - 0.16, zg, lg["x"] + 0.16, zg + 0.03, fill=STEEL, stroke="none")
    # deck
    sh.rect(D["x1"], -0.22, D["x2"], -0.04, fill=WOOD2, stroke=GREEN, sw=0.9); sh.rect(D["x1"], -0.04, D["x2"], 0.0, fill=GREEN, stroke="none")
    for x in (D["x1"] + 0.3, D["x2"] - 0.5): sh.rect(x - 0.04, zg, x + 0.04, -0.22, fill=STEEL, stroke="none")
    for i in range(3): sh.rect(D["x1"] - 0.3 * (i + 1), zg + 0.72 - 0.24 * i, D["x1"] - 0.3 * i, zg + 0.72 - 0.24 * i + 0.05, fill=WOOD2, stroke=GREEN, sw=0.6)
    # casca: externa e interna
    prof = C.profile(); sh.poly(prof, fill=ALU, stroke=GREEN, sw=1.8)
    n = 80; xs = [C.L * i / n for i in range(n + 1)]
    inner = [(x, C.ZC + (C.B - C.SKIN) * C.s(x)) for x in xs] + [(x, C.ZC - (C.B - C.SKIN) * C.s(x)) for x in xs[::-1]]
    sh.poly(inner, fill="#FBF8F2", stroke=GREEN, sw=0.7)
    # Visor (calota de vidro, cortada)
    vis = [(x, C.top(x)) for x in xs if x <= C.X_NOSE] + [(x, C.bottom(x)) for x in xs[::-1] if x <= C.X_NOSE and C.bottom(x) < 0]
    sh.poly(vis, fill=GLASS, stroke=GREEN, sw=1.2, opacity=0.85)
    # piso, chassi, compartimento técnico
    fx0, fx1 = C.floor_range(0.05)
    sh.rect(fx0, -0.22, C.L - 0.5, -0.02, fill=WOOD2, stroke=GREEN, sw=0.8); sh.rect(fx0, -0.02, fx1, 0.0, fill=GREEN, stroke="none")
    sh.rect(C.X_TECH, 0, C.L - 0.35, 1.6, fill=sh.pattern("hatch"), stroke=GREEN, sw=0.6); sh.text(C.X_TECH + 0.35, 0.8, "TÉCNICO", 7, GREEN, spacing=0.15, rotate=-90)
    # anéis (cortados no topo e na barriga)
    for x in C.RINGS:
        sh.rect(x - 0.03, C.top(x) - C.SKIN + 0.02, x + 0.03, C.top(x) - 0.02, fill=STEEL, stroke="none")
        sh.rect(x - 0.03, C.bottom(x) + 0.02, x + 0.03, C.bottom(x) + C.SKIN - 0.02, fill=STEEL, stroke="none")
    # Anel de Luz
    r1, r2 = C.LIGHT_RING; sh.rect(r1, C.top(r1) - C.SKIN, r2, C.top(r2), fill=GLASS, stroke=GREEN, sw=0.9)
    sh.leader(r2 + 0.05, C.top(r2) - 0.02, r2 + 1.0, C.top(r2) + 0.55, "Anel de Luz · vidro laminado curvo 6+6", 8.5)
    sh.leader(0.35, C.top(0.35), 0.9, C.top(0.35) + 0.75, "Visor · vidro curvo 8+8 em 5 gomos", 8.5)
    # porta no Visor
    sh.line(0.22, 0, 0.32, C.DOOR["h"], GREEN, 1.6)
    # parede do banho e mobiliário no plano
    for it in C.furniture():
        if it["kind"] in ("pillow", "hvac", "glass", "opening", "ceiling"): continue
        if "r" in it:
            if abs(it["y"]) < 0.5: sh.rect(it["x"] - it["r"], it["z1"], it["x"] + it["r"], it["z2"], fill="#FFFFFF", stroke=GREEN, sw=0.6)
            continue
        if it["y1"] <= 0.3 and it["y2"] >= -0.3:
            sh.rect(it["x1"], it["z1"], it["x2"], it["z2"], fill=WOOD2 if it["kind"] == "wall" else "#FFFFFF", stroke=GREEN, sw=0.7)
    sh.rect(3.15, 0.52, 5.13, 0.58, fill="#FFFFFF", stroke=GREEN, sw=0.5)
    # cotas
    sh.dim(0, zg - 0.9, C.L, zg - 0.9, -0.3, label=fmt(C.L)); sh.dim(D["x1"], zg - 0.9, 0, zg - 0.9, -0.3, label=fmt(-D["x1"]))
    sh.dim(C.L + 0.9, 0, C.L + 0.9, C.top(4), 0.35, label=fmt(C.top(4)) + " topo"); sh.dim(C.L + 0.9, zg, C.L + 0.9, 0, 0.35, label=fmt(-zg) + " piso")
    sh.dim(C.L + 0.9, C.bottom(4), C.L + 0.9, C.top(4), 1.15, label=fmt(C.top(4) - C.bottom(4)) + " casca")
    sh.text(C.X_NOSE + 0.1, C.ZC + 1.05, "ESTAR", 8, GREEN, spacing=0.2, anchor="start"); sh.text(3.6, C.ZC + 1.05, "SUÍTE", 8, GREEN, spacing=0.2); sh.text(6.55, C.ZC + 1.05, "BANHO", 8, GREEN, spacing=0.2)

# ----------------------------------------------------------------------------- seção transversal B-B (x = 4,15)
def secao(sh, x=4.15):
    zg = C.Z_GROUND
    sh.rect(-C.A - 1.2, zg - 0.5, C.A + 1.2, zg, fill=sh.pattern("soil"), stroke="none"); sh.line(-C.A - 1.2, zg, C.A + 1.2, zg, GREEN, 1.0)
    outer = [(y, z) for (_, y, z) in C.section(x, 96)]; inner = [(y, z) for (_, y, z) in C.section(x, 96, inner=True)]
    sh.poly(outer, fill=ALU, stroke=GREEN, sw=1.8); sh.poly(inner, fill="#FBF8F2", stroke=GREEN, sw=0.7)
    # anel estrutural (tubo 60 x 40 entre as camadas)
    ring = [(y * 0.955, C.ZC + (z - C.ZC) * 0.955) for (y, z) in outer]; sh.poly(ring, fill="none", stroke=STEEL, sw=2.2)
    # Anel de Luz (arco de vidro no topo)
    arc = [(y, z) for (_, y, z) in C.section(x, 192) if abs(math.atan2(y, z - C.ZC)) <= C.LIGHT_ANG and z > C.ZC]
    arc = sorted(arc, key=lambda p: math.atan2(p[0], p[1] - C.ZC))
    sh.poly(arc, close=False, stroke=GLASS, sw=6); sh.poly(arc, close=False, stroke=GREEN, sw=0.9)
    sh.text(0, C.top(x) + 0.35, "ANEL DE LUZ · 130°", 8, GREEN, spacing=0.15)
    # piso, chassi, pés
    hw = C.floor_hw(x); sh.rect(-hw, -0.22, hw, -0.02, fill=WOOD2, stroke=GREEN, sw=0.8); sh.rect(-hw, -0.02, hw, 0, fill=GREEN, stroke="none")
    for y in (-1.0, 1.0):
        sh.rect(y - 0.05, -0.22, y + 0.05, -0.07, fill=STEEL, stroke="none")
    for lg in C.legs():
        if lg["x"] > x: sh.rect(lg["y"] - lg["r"], zg, lg["y"] + lg["r"], lg["z2"], fill=STEEL, stroke="none"); sh.rect(lg["y"] - 0.16, zg, lg["y"] + 0.16, zg + 0.03, fill=STEEL, stroke="none")
    # cama e closet (cortados) e Olho
    sh.rect(-0.79, 0, 0.79, 0.52, fill="#FFFFFF", stroke=GREEN, sw=0.7); sh.rect(-0.79, 0.52, 0.79, 0.58, fill="#FFFFFF", stroke=GREEN, sw=0.5)
    sh.rect(0.95, 0, 1.35, 2.0, fill=WOOD2, stroke=GREEN, sw=0.7)
    p = C.PORTHOLES[0]; yy = -C.hw_at(x, p["z"], inner=False)
    sh.circle(yy + 0.02, p["z"], 0.07, fill=GLASS, stroke=GREEN, sw=0.8); sh.text(yy - 0.32, p["z"], "OLHO", 7, GREEN, spacing=0.1, rotate=-90)
    # cotas
    sh.dim(-C.A, zg - 0.8, C.A, zg - 0.8, -0.3, label=fmt(2 * C.A)); sh.dim(-hw, -0.5, hw, -0.5, -0.25, label=fmt(2 * hw) + " piso", size=10)
    sh.dim(C.A + 0.8, 0, C.A + 0.8, C.top(x) - C.SKIN, 0.3, label=fmt(C.top(x) - C.SKIN) + " livre"); sh.dim(C.A + 0.8, C.bottom(x), C.A + 0.8, C.top(x), 0.95, label=fmt(C.top(x) - C.bottom(x)))

# ----------------------------------------------------------------------------- fachada frontal (Visor)
def fachada(sh):
    zg = C.Z_GROUND; D = C.DECK
    sh.rect(-C.A - 1.2, zg - 0.5, C.A + 1.2, zg, fill=sh.pattern("soil"), stroke="none"); sh.line(-C.A - 1.2, zg, C.A + 1.2, zg, GREEN, 1.0)
    for lg in C.legs():
        sh.rect(lg["y"] - lg["r"], zg, lg["y"] + lg["r"], lg["z2"], fill=STEEL, stroke="none")
    outer = [(y, z) for (_, y, z) in C.section(4.0, 96)]
    sh.poly(outer, fill=ALU2, stroke=GREEN, sw=1.8)
    vis = [(y, z) for (y, z) in outer if z >= -0.02]; sh.poly(vis, fill=GLASS, stroke=GREEN, sw=1.0, opacity=0.9)
    for yj in C.VISOR_JOINTS:
        zt = C.ZC + (C.B) * (1 - (abs(yj) / C.A) ** C.N) ** (1 / C.N); sh.line(yj, 0, yj, zt, GREEN, 0.9)
    d = C.DOOR; sh.rect(d["y1"], 0, d["y2"], d["h"], fill="none", stroke=GREEN, sw=1.4); sh.circle(d["y2"] - 0.1, 1.0, 0.03, fill=GREEN, stroke="none")
    sh.line(-C.floor_hw(4), 0, C.floor_hw(4), 0, GREEN, 0.8)
    sh.rect(D["y1"], -0.22, D["y2"], 0.0, fill=WOOD2, stroke=GREEN, sw=0.9)
    sh.dim(-C.A, zg - 0.8, C.A, zg - 0.8, -0.3, label=fmt(2 * C.A)); sh.dim(C.A + 0.8, zg, C.A + 0.8, C.top(4), 0.3, label=fmt(C.top(4) - zg) + " total")
    sh.text(0, C.top(4) + 0.35, "VISOR · 5 GOMOS DE VIDRO CURVO", 8, GREEN, spacing=0.15)

# ----------------------------------------------------------------------------- prancha
def concept_sheet(out):
    D = C.DECK; width = (C.L + 2.2) - (D["x1"] - 1.2)
    sc = min(58.0, 700.0 / width); ox = 60 - (D["x1"] - 1.2) * sc
    sh = Sheet(1600, 1000, scale=sc, ox=ox, oy=300)
    sh.header(f"{C.NAME.title()} · Conceito", TAGLINE + " · estudo de conceito")
    planta(sh); sh.text_px(400, 100, "PLANTA", size=11, weight=700, spacing=0.25)
    sh.north(720, 130, angle=-90); sh.scalebar(D["x1"] - 1.0, -C.A - 3.1, 5)
    sh.ox, sh.oy, sh.s = 1000 - (D["x1"] - 1.4) * 46, 340, 46
    corte(sh); sh.text_px(1160, 100, "CORTE LONGITUDINAL A-A", size=11, weight=700, spacing=0.25)
    sh.ox, sh.oy, sh.s = 990, 730, 48
    secao(sh); sh.text_px(990, 505, "SEÇÃO B-B (x = 4,15)", size=11, weight=700, spacing=0.25)
    sh.ox, sh.oy, sh.s = 1330, 730, 48
    fachada(sh); sh.text_px(1330, 505, "FACHADA FRONTAL · VISOR", size=11, weight=700, spacing=0.25)
    sh.ox, sh.oy, sh.s = ox, 300, sc
    rows = [("Casca", f"superelipse {fmt(2 * C.A)} x {fmt(C.top(4) - C.bottom(4))} m · comprimento {fmt(C.L)} m · calotas {fmt(C.X_NOSE)} (Visor) e {fmt(C.X_TAIL)} m"),
            ("Área interna", fmt(C.floor_area()) + " m² (estar 7,6 · suíte 6,9 · banho 4,4) + compartimento técnico"),
            ("Deck frontal", fmt(C.deck_area()) + " m² sob o Visor, com escada de três degraus"), ("Área total", fmt(C.floor_area() + C.deck_area()) + " m²"),
            ("Alturas", f"pé-direito {fmt(C.top(4) - C.SKIN)} m no eixo · piso a {fmt(-C.Z_GROUND)} m do terreno · topo a {fmt(C.top(4) - C.Z_GROUND)} m"),
            ("Estrutura", f"monocoque: {len(C.RINGS)} anéis 60 x 40 x 3 a cada 0,60 m · {len(C.STRINGER_DEG)} longarinas 40 x 40 · chassi em U 150 · 4 pés telescópicos Ø101,6"),
            ("Envelope", "painéis de alumínio composto 4 mm curvados · PIR 60 mm · câmara 40 mm · compensado curvado 12 mm (aparente)"),
            ("Vidros", f"Visor: 5 gomos de laminado curvo 8+8 ({fmt(C.shell_area('visor'))} m²) · Anel de Luz laminado 6+6 ({fmt(C.shell_area('ring'))} m²) · 2 Olhos Ø0,60"),
            ("Transporte", "viaja inteira em carreta (AET para 3,20 m de largura) · descarga com guindaste de 12 t · instalação em 1 dia")]
    y0 = 596
    sh.text_px(60, y0, "DADOS DO PRODUTO", size=11, weight=700, spacing=0.25, anchor="start")
    for i, (k, v) in enumerate(rows):
        sh.text_px(60, y0 + 24 + i * 19, k.upper(), size=8.5, fill=EARTH, spacing=0.15, anchor="start"); sh.text_px(180, y0 + 24 + i * 19, v, size=10, anchor="start")
    dif = ["Visor: calota frontal inteira em vidro curvo, do piso ao topo, em cinco gomos com porta pivotante no gomo central (a referência de mercado usa uma janela plana na ponta)",
           "Anel de Luz: faixa de vidro de 0,45 m que contorna 130° da seção sobre a cama, para o céu noturno sem sair do lençol",
           "Dois Olhos laterais: lentes redondas Ø0,60 na suíte e no banho, mesma família das Janelas Olho do Casulo",
           "Compartimento técnico na calota traseira, com acesso externo: boiler, quadro, evaporadora e reservatório fora do ambiente do hóspede",
           "Chega pronta: fabricada e mobiliada em fábrica, viaja inteira e pousa em quatro pés telescópicos sobre estacas; sem obra no sítio além do deck"]
    sh.text_px(60, 800, "DIFERENCIAIS · IDENTIDADE PRÓPRIA", size=11, weight=700, spacing=0.25, anchor="start")
    yy = 824
    for i, t in enumerate(dif):
        words = t.split(); lines = []; cur = ""
        for w in words:
            if len(cur) + len(w) + 1 > 128: lines.append(cur); cur = w
            else: cur = (cur + " " + w).strip()
        lines.append(cur)
        sh.text_px(60, yy, f"{i + 1:02d}", size=9.5, weight=700, anchor="start")
        for k, Ln in enumerate(lines): sh.text_px(86, yy + k * 13, Ln, size=9.5, anchor="start")
        yy += 13 * len(lines) + 7
    sh.title_block(C.NAME, "Conceito · planta, corte, seção, fachada", "escala gráfica (A1)", "01/CP", POS + " · estudo de conceito R00")
    sh.save(out)

# ----------------------------------------------------------------------------- isométrica
def iso_sheet(out):
    from iso import Scene, add_furniture, ground_shadow
    sh = Sheet(1600, 1000)
    sh.header(f"{C.NAME.title()} · Vista isométrica", "Projeção isométrica a partir da frente (Visor) e da lateral direita · sem escala")
    sc = Scene(sh, 82, 780, 600)
    D = C.DECK; zg = C.Z_GROUND
    ground_shadow(sc, C.L / 2 - 0.6, 0, C.L / 2 + 2.6, C.A + 1.4)
    sc.pre.append("")  # marcador
    # deck e escada (nível do piso)
    sc.box(D["x1"], D["x2"], D["y1"], D["y2"], -0.22, 0.0, "#B99A73")
    for i in range(3): sc.box(D["x1"] - 0.3 * (i + 1), D["x1"] - 0.3 * i, -0.9, 0.9, zg, zg + 0.72 - 0.24 * i, "#A5885F")
    for (x, y) in ((D["x1"] + 0.25, -1.3), (D["x1"] + 0.25, 1.3), (D["x2"] - 0.5, -1.3), (D["x2"] - 0.5, 1.3)): sc.cylinder(x, y, zg, -0.22, 0.05, "#3A3B3A")
    # pés
    for lg in C.legs():
        sc.cylinder(lg["x"], lg["y"], zg, lg["z2"], lg["r"], "#3A3B3A"); sc.cylinder(lg["x"], lg["y"], zg, zg + 0.03, 0.16, "#3A3B3A")
    # piso interno e mobiliário
    fx0, fx1 = C.floor_range(0.05); nf = 40
    for i in range(nf):
        xa, xb = fx0 + (fx1 - fx0) * i / nf, fx0 + (fx1 - fx0) * (i + 1) / nf; ha, hb = C.floor_hw(xa), C.floor_hw(xb)
        sc.quad((xa, -ha, -0.01), (xb, -hb, -0.01), (xb, hb, -0.01), (xa, ha, -0.01), "#C9AA7D", shade_on=False)
    add_furniture(sc, [f for f in C.furniture() if f["kind"] != "hvac"])
    sc.box(C.X_TECH, 8.05, -0.8, 0.8, 0, 1.5, "#D9D9D6")
    # casca por região
    m = C.shell_mesh(72, 44)
    V, F = m["shell"]; sc.mesh(V, F, ALU, 1.0)
    V, F = m["ring"]; sc.mesh(V, F, "#9FB7C2", 0.55)
    V, F = m["visor"]; sc.mesh(V, F, "#9FB7C2", 0.38)
    # juntas do Visor e contorno da porta
    for yj in C.VISOR_JOINTS:
        pts = []
        for i in range(25):
            z = -0.02 + (C.ZC + C.B - 0.02 + 0.02) * i / 24
            # x da calota onde a meia-largura na altura z iguala |yj|
            best = None
            for k in range(121):
                x = C.X_NOSE * k / 120
                if C.hw_at(x, z, inner=False) >= abs(yj): best = x; break
            if best is not None: pts.append((best - 0.005, yj, z))
        if len(pts) > 2: sc.polyline(pts, "#3A3B3A", 1.1)
    d = C.DOOR; sc.polyline([(0.2, d["y1"], 0), (0.2, d["y1"], d["h"]), (0.2, d["y2"], d["h"]), (0.2, d["y2"], 0)], "#3A3B3A", 1.2)
    # Olhos
    for p in C.PORTHOLES:
        pts = []
        for i in range(20):
            ph = 2 * math.pi * i / 20; z = p["z"] + p["r"] * math.sin(ph); x = p["x"] + p["r"] * math.cos(ph)
            pts.append((x, p["side"] * (C.hw_at(x, z, inner=False) + 0.04), z))
        for i in range(1, 19): sc.tri(pts[0], pts[i], pts[i + 1], "#9FB7C2", 0.9)
    sc.render()
    notes = [f"Cápsula de {fmt(C.L)} x {fmt(2 * C.A)} m · {fmt(C.floor_area())} m² internos", f"Deck frontal de {fmt(C.deck_area())} m² sob o Visor", "Visor: calota de vidro curvo em 5 gomos com porta pivotante",
             "Anel de Luz sobre a cama · dois Olhos laterais", "Casca em alumínio composto sobre 12 anéis · compartimento técnico na cauda", "Quatro pés telescópicos sobre estacas helicoidais"]
    for i, n in enumerate(notes):
        sh.callout_px(70, 760 + i * 22, i + 1); sh.text_px(90, 764 + i * 22, n, size=11, anchor="start")
    sh.title_block(C.NAME, "Vista isométrica", "sem escala", "08/CP", POS)
    sh.save(out)

# ----------------------------------------------------------------------------- materiais estimados
def capsule_materials():
    """lista de materiais por grupo, no formato de product_book_data.bom_priced: [(grupo, [(descrição, un, qtd, chave)])]."""
    per = C.ring_perimeter(); nr = len(C.RINGS); a_shell = C.shell_area("shell"); a_vis = C.shell_area("visor"); a_ring = C.shell_area("ring")
    fl = C.floor_area(); dk = C.deck_area(); fx0, fx1 = C.floor_range(0.05); Lc = 7.75 - 0.55
    return [
        ("Estrutura monocoque (aço galvanizado a fogo)", [
            (f"Anéis da casca: tubo retangular 60 x 40 x 3,0 mm calandrado ({nr} un. x {fmt(per)} m)", "m", round(nr * per * 1.05, 1), "ring"),
            (f"Longarinas: tubo 40 x 40 x 2,0 mm curvado nas calotas ({len(C.STRINGER_DEG)} un.)", "m", round(len(C.STRINGER_DEG) * (C.RINGS[-1] - C.RINGS[0] + 1.2) * 1.05, 1), "stringer"),
            ("Chassi do piso: perfil U 150 x 50 x 3,0 mm (2 longarinas)", "m", round(2 * Lc * 1.05, 1), "chassis"),
            (f"Travessas do piso: perfil U 100 x 50 x 2,65 mm ({nr} un.)", "m", round(sum(2 * max(0.6, C.hw_at(x, -0.15) - 0.05) for x in C.RINGS) * 1.05, 1), "cross"),
            ("Pés telescópicos: tubo Ø101,6 x 4,0 em tubo Ø114,3 x 4,5, curso 0,40 m, placa base 250 x 250 x 10", "un", 4, "legs"),
            ("Chapas de nó, cantoneiras e olhais de içamento (4 un.)", "kg", 46, "plates"),
            ("Parafusos estruturais 8.8 galvanizados M10/M12 com porcas e arruelas", "un", 380, "bolts"),
            ("Aço total estimado (anéis, longarinas, chassi, pés, chapas)", "kg", round(nr * per * 1.05 * 4.4 + len(C.STRINGER_DEG) * 7.9 * 2.3 + 2 * Lc * 1.05 * 6.9 + 24 * 2.2 * 4.9 + 4 * 14 + 46), "steel_kg")]),
        ("Envelope (de fora para dentro)", [
            (f"Painel de alumínio composto 4 mm (ACM) curvado, cor champanhe fosco ({fmt(a_shell)} m² + 18 % de perdas)", "m²", round(a_shell * 1.18, 1), "acm"),
            ("Subestrutura do ACM: perfis ômega de alumínio 20 mm e fixadores ocultos", "m", round(a_shell * 1.6, 1), "omega"),
            ("Membrana de estanqueidade e barreira de vapor (manta líquida + fita butílica nas juntas)", "m²", round(a_shell * 1.1, 1), "vapor"),
            ("Isolamento PIR 60 mm em painéis curvados entre anéis (λ 0,022)", "m²", round(a_shell * 1.08, 1), "pir"),
            ("Câmara de ar ventilada 40 mm com sarrafos de PVC", "m²", round(a_shell, 1), "cavity"),
            ("Forro e paredes: compensado naval curvado 12 mm com lâmina de carvalho, verniz fosco", "m²", round((a_shell - 4) * 1.12, 1), "ply"),
            ("Selante de poliuretano e fita EPDM nas juntas dos gomos", "m", round(nr * per * 0.35 + 40, 1), "sealant")]),
        ("Vidros e esquadrias (laminado curvo, alumínio anodizado bronze)", [
            (f"Visor: laminado curvo 8 + 8 mm low-e em 5 gomos, calandrado ({fmt(a_vis)} m² + 10 %)", "m²", round(a_vis * 1.1, 1), "visor"),
            ("Porta pivotante PV1 0,90 x 2,05 m em vidro laminado 10 + 10 com pivô e fechadura", "un", 1, "door"),
            (f"Anel de Luz: laminado curvo 6 + 6 mm com controle solar, 3 gomos ({fmt(a_ring)} m²)", "m²", round(a_ring * 1.1, 1), "ring_glass"),
            ("Olhos: vidro insulado circular Ø0,60 com aro de alumínio (1 transparente, 1 acidado)", "un", 2, "portholes"),
            ("Vidro temperado 8 mm do box do chuveiro 0,90 x 2,00", "m²", 1.8, "shower_glass")]),
        ("Piso e acabamentos internos", [
            ("Painel de piso: OSB 18 mm + lã de PET 50 mm + barreira de vapor", "m²", round(fl * 1.05, 1), "subfloor"),
            ("Piso de carvalho de engenharia 14 mm (estar e suíte)", "m²", round((fl - 4.4) * 1.08, 1), "oak"),
            ("Porcelanato 60 x 60 no banho, com impermeabilização", "m²", 5.3, "tile"),
            ("Parede do banho: painel SIP 90 mm com porta de correr embutida 0,80 x 2,05", "un", 1, "partition"),
            ("Marcenaria fixa: closet, café/minibar, cabeceira curva, bancada do banho (ver FF&E)", "vb", 1, "joinery")]),
        ("Deck e fundação", [
            (f"Deck de cumaru 20 x 140 mm sobre vigas U 100 galvanizadas ({fmt(dk)} m² + 12 %)", "m²", round(dk * 1.12, 1), "deck"),
            ("Escada de três degraus em cumaru", "un", 1, "stairs"),
            ("Estacas helicoidais Ø76 galvanizadas com cabeçote ajustável (4 sob os pés + 4 sob o deck)", "un", 8, "piles")]),
        ("Instalações", [
            ("Elétrica: quadro 12 circuitos, 24 pontos, fita LED perimetral 2700 K, tomadas USB, iluminação do deck", "vb", 1, "electrical"),
            ("Hidráulica: PEX, boiler elétrico 80 L no compartimento técnico, registros, ducha, lavatório, bacia com caixa acoplada", "vb", 1, "plumbing"),
            ("Climatização: split inverter 9.000 BTU dutado a partir do compartimento técnico, exaustor do banho", "cj", 1, "hvac"),
            ("Ventilação: 2 grelhas de admissão nos Olhos + saída no Anel de Luz (abertura basculante motorizada)", "cj", 1, "vent"),
            ("Metais e louças do banho (latão escovado): ducha, misturador, cuba esculpida, bacia, acessórios", "cj", 1, "fixtures")]),
    ]

def build():
    d = os.path.join(ROOT, "capsule", "desenhos"); os.makedirs(d, exist_ok=True)
    concept_sheet(os.path.join(d, "01_conceito.svg")); iso_sheet(os.path.join(d, "08_isometrica.svg"))
    print("capsule ok ·", fmt(C.floor_area()), "m² internos ·", fmt(C.deck_area()), "m² deck")

if __name__ == "__main__":
    build()

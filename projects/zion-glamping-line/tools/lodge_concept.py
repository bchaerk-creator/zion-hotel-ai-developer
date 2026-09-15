# -*- coding: utf-8 -*-
"""ZION LODGE · prancha de conceito (planta, corte, fachada, dados e diferenciais) a partir de geometry.Lodge.
Saída: lodge/desenhos/01_conceito.svg. Uso: python3 lodge_concept.py"""
import math, os
from geometry import Lodge
from svgkit import *

L = Lodge()
OUT = os.path.join(os.path.dirname(__file__), "..", "lodge", "desenhos")
V = L.vertices(); R = L.r_corner()
GLASS_FACES = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]       # cinco faces de vidro (frente e laterais)
WALL_FACES = [(6, 7), (7, 0), (0, 1)]                        # três faces opacas (banho e cabeceira)
X_PART = 1.55                                                 # parede do banho (corda)

def face_mid(i, j):
    return ((V[i][0] + V[j][0]) / 2, (V[i][1] + V[j][1]) / 2)

def planta(sh):
    # cobertura (beiral) e deck
    Vo = L.vertices(R + L.OVER / math.cos(math.pi / 8))
    sh.poly(Vo, fill="none", stroke=GREEN, sw=0.8, dash="6 3")
    sh.poly(L.deck_pts(), fill=sh.pattern("deck"), stroke=GREEN, sw=1.0)
    # vela frontal (postes)
    px = -R - L.SAIL["reach"]
    for py in (-1.8, 1.8): sh.circle(px, py, 0.06, fill=STEEL, stroke="none")
    sh.poly([(V[3][0], V[3][1]), (px, 1.8), (px, -1.8), (V[4][0], V[4][1])], fill="none", stroke=GREEN, sw=0.7, dash="3 3")
    sh.text(px + 1.0, 0.0, "vela de sombra", 9, EARTH, rotate=-90)
    # piso, paredes de vidro e opacas
    sh.poly(V, fill="#F7F1E6", stroke=GREEN, sw=1.6)
    for (i, j) in GLASS_FACES: sh.line(V[i][0], V[i][1], V[j][0], V[j][1], GLASS, 6); sh.line(V[i][0], V[i][1], V[j][0], V[j][1], GREEN, 0.9)
    for (i, j) in WALL_FACES: sh.line(V[i][0], V[i][1], V[j][0], V[j][1], WOOD2, 8); sh.line(V[i][0], V[i][1], V[j][0], V[j][1], GREEN, 0.9)
    for (x, y) in V: sh.rect(x - 0.08, y - 0.08, x + 0.08, y + 0.08, fill=STEEL, stroke="none")
    # porta de correr na face frontal
    sh.line(-R + 0.05, -1.0, -R + 0.05, 1.0, CREAM, 6); sh.line(-R + 0.05, -1.0, -R + 0.05, 0.0, GREEN, 2.2)
    sh.text(-R - 0.35, 0, "PC1 2,00 x 2,40", 8, GREEN, rotate=-90)
    # parede do banho (corda) e banho
    yc = math.sqrt(R ** 2 - X_PART ** 2)
    ytop = min(yc, 3.4)
    sh.rect(X_PART, -ytop, X_PART + 0.1, ytop, fill=WOOD2, stroke=GREEN, sw=0.8)
    sh.rect(X_PART, -0.5, X_PART + 0.1, 0.4, fill=CREAM, stroke="none"); sh.line(X_PART + 0.05, -0.5, X_PART + 0.05, 0.4, GREEN, 0.6, dash="3 2")
    sh.text(2.5, 0.0, "BANHO", 10, GREEN, spacing=0.2); sh.text(2.5, -0.3, fmt(6.9) + " m²", 8, EARTH)
    sh.rect(1.75, 1.0, 2.45, 2.4, fill="#FFFFFF", stroke=GREEN, sw=0.7); sh.text(2.1, 1.7, "bancada", 7, EARTH, rotate=-90)
    sh.rect(2.7, 1.6, 3.4, 2.3, fill="#FFFFFF", stroke=GREEN, sw=0.7); sh.text(3.05, 1.95, "wc", 7, EARTH)
    sh.rect(2.4, -1.6, 3.35, -0.7, fill=sh.pattern("tile"), stroke=GREEN, sw=0.7); sh.text(2.9, -1.15, "chuveiro", 7, EARTH)
    sh.rect(1.8, -2.5, 2.7, -1.75, fill="#FFFFFF", stroke=GREEN, sw=0.7); sh.text(2.25, -2.1, "banheira", 7, EARTH)
    # suíte e estar
    sh.rect(-0.55, -0.97, 1.45, 0.97, fill="#FFFFFF", stroke=GREEN, sw=0.8); sh.rect(1.1, -0.97, 1.45, 0.97, fill=SAND, stroke=GREEN, sw=0.5)
    sh.text(0.4, 0.0, "CAMA KING", 8, GREEN, spacing=0.1); sh.text(0.4, -0.3, "1,93 x 2,03", 7, EARTH)
    sh.rect(-0.55, 1.1, 0.05, 1.7, fill="#FFFFFF", stroke=GREEN, sw=0.6); sh.rect(-0.55, -1.7, 0.05, -1.1, fill="#FFFFFF", stroke=GREEN, sw=0.6)
    sh.rect(0.2, 2.2, 1.9, 2.95, fill=WOOD, stroke=GREEN, sw=0.7); sh.text(1.05, 2.57, "café / minibar", 7, EARTH)
    sh.rect(0.2, -2.95, 1.9, -2.2, fill=WOOD, stroke=GREEN, sw=0.7); sh.text(1.05, -2.57, "closet", 7, EARTH)
    sh.rect(-2.7, -1.2, -1.5, 1.2, fill="#FFFFFF", stroke=GREEN, sw=0.7); sh.text(-2.1, 0.0, "estar", 8, GREEN); sh.text(-2.1, -0.3, "sofá 2,4", 7, EARTH)
    sh.circle(-1.15, 0.0, 0.3, fill=WOOD, stroke=GREEN, sw=0.6)
    sh.rect(-2.9, 1.7, -1.9, 2.5, fill="#FFFFFF", stroke=GREEN, sw=0.6); sh.text(-2.4, 2.1, "poltrona", 7, EARTH)
    sh.text(-1.6, -2.6, "ESTAR + SUÍTE", 10, GREEN, spacing=0.2); sh.text(-1.6, -2.9, fmt(L.floor_area() - 6.9) + " m²", 8, EARTH)
    sh.text(-R - 1.3, -2.6, "DECK", 10, GREEN, spacing=0.2); sh.text(-R - 1.3, -2.9, fmt(L.deck_area()) + " m²", 8, EARTH)
    # lanterna
    sh.circle(0, 0, L.R_LANTERN, fill="none", stroke=GREEN, sw=0.8, dash="4 3"); sh.text(0, L.R_LANTERN + 0.25, "LANTERNA Ø1,50", 8, GREEN, spacing=0.1)
    # cotas
    sh.dim(-R, -4.6, R, -4.6, -0.4, label=fmt(2 * R) + " (entre vértices)")
    sh.dim(-L.F / 2, -4.6, L.F / 2, -4.6, -1.0, label=fmt(L.F) + " (entre faces)")
    sh.dim(px, -4.6, -R, -4.6, -0.4, label=fmt(L.SAIL["reach"]) + " (deck)")
    sh.dim(4.6, -L.F / 2, 4.6, L.F / 2, 0.5, label=fmt(L.F))
    sh.dim(4.6, X_PART, 4.6, R, 1.2, label=fmt(R - X_PART) + " banho")
    sh.text(-R - 1.3, 4.5, "A", 12, GREEN, weight=700); sh.text(R + 1.6, 4.5, "A", 12, GREEN, weight=700)
    sh.line(-R - 1.3, 4.3, R + 1.6, 4.3, GREEN, 0.8, dash="8 3")

def corte(sh):
    # solo, estacas, deck e piso
    sh.rect(-8.0, -0.6, 6.0, -0.02, fill=sh.pattern("soil"), stroke="none"); sh.line(-8.0, -0.02, 6.0, -0.02, GREEN, 1.0)
    px = -R - L.SAIL["reach"]
    for x in (px + 0.3, -R, -1.7, 0, 1.7, R): sh.rect(x - 0.04, -0.6, x + 0.04, -0.2, fill=STEEL, stroke="none")
    sh.rect(px, -0.2, R, -0.05, fill=WOOD2, stroke=GREEN, sw=0.9); sh.rect(px, -0.05, R, 0.0, fill=GREEN, stroke="none")
    # pilares, anel de beiral, caibros, lanterna
    for x in (-R, R): sh.rect(x - 0.06, 0, x + 0.06, L.Z_EAVE, fill=STEEL, stroke="none"); sh.rect(x - 0.12, 0, x + 0.12, L.Z_EAVE, fill="none", stroke=WOOD2, sw=1.2)
    sh.rect(-R - 0.1, L.Z_EAVE - 0.15, R + 0.1, L.Z_EAVE, fill=STEEL, stroke="none")
    for s in (-1, 1): sh.line(s * R, L.Z_EAVE, s * L.R_LANTERN, L.Z_LANTERN, STEEL, 3)
    sh.rect(-L.R_LANTERN, L.Z_LANTERN - 0.1, L.R_LANTERN, L.Z_LANTERN, fill=STEEL, stroke="none")
    sh.rect(-L.R_LANTERN, L.Z_LANTERN, L.R_LANTERN, L.Z_TOP - 0.15, fill=GLASS, stroke=GREEN, sw=0.9)
    sh.rect(-L.R_LANTERN - 0.25, L.Z_TOP - 0.15, L.R_LANTERN + 0.25, L.Z_TOP, fill=MEMB, stroke=GREEN, sw=1.2)
    # membrana (perfil cônico tensionado)
    n = 40; prof = [(-(L.R_LANTERN + (R + L.OVER - L.R_LANTERN) * i / n), L.roof_z(L.R_LANTERN + (R + L.OVER - L.R_LANTERN) * i / n)) for i in range(n + 1)]
    sh.poly(prof, close=False, stroke=GREEN, sw=2.2); sh.poly([(-x, z) for (x, z) in prof], close=False, stroke=GREEN, sw=2.2)
    # forro tensionado (interno) e camada isolante
    prof_in = [(x * 0.97, z - 0.22) for (x, z) in prof if abs(x) <= R]
    sh.poly(prof_in, close=False, stroke=EARTH, sw=0.9, dash="4 3"); sh.poly([(-x, z) for (x, z) in prof_in], close=False, stroke=EARTH, sw=0.9, dash="4 3")
    # vela frontal
    sh.line(px, 0, px, L.SAIL["z_post"], STEEL, 3); sh.line(px, L.SAIL["z_post"], -R, L.Z_EAVE + 0.15, GREEN, 1.8)
    # vidros e parede do banho
    sh.rect(-R + 0.06, 0, -R + 0.1, L.Z_EAVE - 0.15, fill=GLASS, stroke=GREEN, sw=0.6); sh.rect(R - 0.1, 0, R - 0.06, L.Z_EAVE - 0.15, fill=WOOD2, stroke=GREEN, sw=0.6)
    sh.rect(X_PART, 0, X_PART + 0.1, 2.4, fill=WOOD2, stroke=GREEN, sw=0.6); sh.rect(X_PART, 2.4, R, 2.45, fill=SAND, stroke=GREEN, sw=0.5)
    sh.rect(-0.55, 0, 1.45, 0.55, fill="#FFFFFF", stroke=GREEN, sw=0.7); sh.rect(-2.7, 0, -1.5, 0.8, fill="#FFFFFF", stroke=GREEN, sw=0.7)
    sh.rect(2.4, 0, 3.35, 2.1, fill="none", stroke=GREEN, sw=0.5, dash="2 2")
    # cotas e níveis
    sh.dim(-R, -1.0, R, -1.0, -0.3, label=fmt(2 * R)); sh.dim(px, -1.0, -R, -1.0, -0.3, label=fmt(L.SAIL["reach"]))
    sh.dim(5.2, 0, 5.2, L.Z_EAVE, 0.4, label=fmt(L.Z_EAVE) + " beiral"); sh.dim(5.2, 0, 5.2, L.Z_TOP, 1.1, label=fmt(L.Z_TOP) + " lanterna")
    sh.dim(-6.9, 0, -6.9, L.SAIL["z_post"], -0.4, label=fmt(L.SAIL["z_post"]))
    sh.leader(0, L.Z_TOP, 1.6, 5.75, "Lanterna Zion: anel de compressão Ø1,50, vidro claro 0,45 m, tampa ventilada", 10)
    sh.leader(-2.2, L.roof_z(2.2), -3.6, 5.3, "membrana PVDF em 8 gomos · câmara ventilada · lã PET · forro tensionado", 10, anchor="end")
    sh.leader(px + 1.3, L.SAIL["z_post"] + 0.4, -6.6, 3.9, "vela de sombra sobre o deck (2 postes)", 10, anchor="end")

def fachada(sh):
    sh.rect(-6.0, -0.6, 6.0, -0.02, fill=sh.pattern("soil"), stroke="none"); sh.line(-6.0, -0.02, 6.0, -0.02, GREEN, 1.0)
    W = L.F / 2 + L.DECK_D * 0.55
    sh.rect(-4.6, -0.2, 4.6, -0.05, fill=WOOD2, stroke=GREEN, sw=0.9); sh.rect(-4.6, -0.05, 4.6, 0.0, fill=GREEN, stroke="none")
    for x in (-4.3, -2.2, 0, 2.2, 4.3): sh.rect(x - 0.04, -0.6, x + 0.04, -0.2, fill=STEEL, stroke="none")
    # três faces visíveis (2-3, 3-4, 4-5): projeção em y
    ys = sorted(set(round(v[1], 3) for v in [V[2], V[3], V[4], V[5]]))
    for k in range(3):
        y1, y2 = ys[k], ys[k + 1]
        sh.rect(y1, 0, y2, L.Z_EAVE - 0.15, fill=GLASS, stroke=GREEN, sw=0.9)
    for y in ys: sh.rect(y - 0.06, 0, y + 0.06, L.Z_EAVE, fill=STEEL, stroke="none")
    sh.rect(-1.0, 0, 1.0, 2.4, fill="none", stroke=GREEN, sw=1.4); sh.line(0, 0, 0, 2.4, GREEN, 0.8)
    sh.rect(-R - 0.1, L.Z_EAVE - 0.15, R + 0.1, L.Z_EAVE, fill=STEEL, stroke="none")
    # silhueta da cobertura (cone) e lanterna
    n = 30; prof = [(-(L.R_LANTERN + (R + L.OVER - L.R_LANTERN) * i / n), L.roof_z(L.R_LANTERN + (R + L.OVER - L.R_LANTERN) * i / n)) for i in range(n + 1)]
    sh.poly(prof + [(-x, z) for (x, z) in prof][::-1], fill=MEMB, stroke=GREEN, sw=1.8)
    sh.rect(-L.R_LANTERN, L.Z_LANTERN, L.R_LANTERN, L.Z_TOP - 0.15, fill=GLASS, stroke=GREEN, sw=0.9)
    sh.rect(-L.R_LANTERN - 0.25, L.Z_TOP - 0.15, L.R_LANTERN + 0.25, L.Z_TOP, fill=MEMB, stroke=GREEN, sw=1.2)
    for s in (-1, 1):
        for yy in (1.2, 2.6): sh.line(s * yy, L.Z_EAVE, s * min(yy, 0.5), L.Z_LANTERN - 0.05, EARTH, 0.5, dash="3 3", opacity=0.6)
    # vela frontal (vista de frente: postes e borda)
    for py in (-1.8, 1.8): sh.line(py, 0, py, L.SAIL["z_post"], STEEL, 3)
    sh.line(-2.4, L.SAIL["z_post"] + 0.05, 2.4, L.SAIL["z_post"] + 0.05, GREEN, 2.0)
    sh.dim(5.3, 0, 5.3, L.Z_TOP, 0.4, label=fmt(L.Z_TOP))

def build():
    os.makedirs(OUT, exist_ok=True)
    sh = Sheet(1600, 1000, scale=44, ox=430, oy=385)
    sh.header("Zion Lodge · Conceito", "Pavilhão octogonal de 6,80 m entre faces com Lanterna Zion, cinco faces de vidro, banho no segmento posterior e deck em três faces com vela de sombra · estudo de conceito")
    planta(sh)
    sh.text_px(430, 92, "PLANTA", size=11, weight=700, spacing=0.25)
    sh.north(690, 140, angle=-90); sh.scalebar(-6.3, 5.3, 5)
    # corte (direita, em cima) e fachada (direita, em baixo)
    # painéis à direita: usa um segundo sistema de coordenadas por deslocamento de ox/oy
    sh.ox, sh.oy, sh.s = 1130, 430, 46
    corte(sh); sh.text_px(1130, 92, "CORTE A-A", size=11, weight=700, spacing=0.25)
    sh.ox, sh.oy, sh.s = 1330, 830, 42
    fachada(sh); sh.text_px(1330, 560, "FACHADA FRONTAL", size=11, weight=700, spacing=0.25)
    # dados e diferenciais
    sh.ox, sh.oy, sh.s = 430, 385, 44
    rows = [("Planta", "octógono regular · 6,80 m entre faces · 7,36 m entre vértices"), ("Área interna", fmt(L.floor_area()) + " m² (banho 6,9 m²)"), ("Deck frontal", fmt(L.deck_area()) + " m² em três faces + vela de sombra"),
            ("Área total", fmt(L.floor_area() + L.deck_area()) + " m²"), ("Alturas", "beiral 2,70 m · lanterna 4,60 a 5,20 m"), ("Estrutura", "8 pilares Ø101,6 revestidos em madeira · anel de beiral 150 x 100 · 8 caibros Ø76 · anel de compressão da lanterna"),
            ("Envelope", "membrana PVDF 1050 g/m² em 8 gomos · câmara ventilada · lã PET 50 mm · forro tensionado"), ("Fechamentos", "5 faces de vidro insulado (alumínio bronze RPT) · 3 faces em painel SIP + ripado"), ("Fundação", "estacas helicoidais, ~20 un. · deck em vigas U 150")]
    y0 = 640
    sh.text_px(60, y0, "DADOS DO PRODUTO", size=11, weight=700, spacing=0.25, anchor="start")
    for i, (k, v) in enumerate(rows):
        sh.text_px(60, y0 + 24 + i * 19, k.upper(), size=8.5, fill=EARTH, spacing=0.15, anchor="start"); sh.text_px(180, y0 + 24 + i * 19, v, size=10, anchor="start")
    dif = ["Lanterna Zion no cume: anel de vidro de 0,45 m que leva luz zenital ao centro da cama (a referência de mercado fecha o cume em ponta cega)",
           "Vela de sombra sobre o deck: membrana independente em dois postes, prolongando a varanda sem tocar a cobertura principal",
           "Cinco faces de vidro e três opacas: o banho ocupa o segmento posterior com banheira sob fresta alta; a cama fica no centro geométrico, sob a lanterna",
           "Mesmo Zion Shell System das unidades Casulo e Safari: kit parafusado, sem solda em campo, 13 camadas, deck em estacas helicoidais"]
    sh.text_px(760, y0, "DIFERENCIAIS · IDENTIDADE PRÓPRIA", size=11, weight=700, spacing=0.25, anchor="start")
    for i, t in enumerate(dif):
        words = t.split(); lines = []; cur = ""
        for w in words:
            if len(cur) + len(w) + 1 > 64: lines.append(cur); cur = w
            else: cur = (cur + " " + w).strip()
        lines.append(cur)
        sh.text_px(760, y0 + 24 + i * 44, f"{i + 1:02d}", size=9.5, weight=700, anchor="start")
        for k, Ln in enumerate(lines): sh.text_px(786, y0 + 24 + i * 44 + k * 13, Ln, size=9.5, anchor="start")
    sh.title_block("ZION LODGE", "Conceito · planta, corte, fachada", "escala gráfica (A1)", "01/LG", "Terceiro produto da linha · unidade de entrada · estudo de conceito R00")
    sh.save(os.path.join(OUT, "01_conceito.svg")); print("lodge conceito ok")

if __name__ == "__main__":
    build()

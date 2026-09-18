# -*- coding: utf-8 -*-
"""ZG-FFE-002 · ZION CANOPY BED · peça hero da ZION NEW LUXURY FURNITURE COLLECTION.
Geometria paramétrica da cama queen com dossel (mm), três conceitos, seleção, pranchas FB-01 a FB-08 (frontal, lateral, superior,
posterior, isométrica, detalhes, explodido, conceitos) em SVG, BOM, fabricação, montagem, manutenção. Custo só em interno/.
Saída: 08_MOBILIARIO/cama/FB-*.svg · 08_MOBILIARIO/ZG-FFE-002_Zion_Canopy_Bed.html · PDF via export_pdf.js"""
import os, math
import numpy as np
from furniture_common import *
from svgkit import Sheet, iso_project, shade, WOOD, WOOD2
from iso import Scene
from build_projeto_arquitetonico import svg_inline

DOC = "ZG-FFE-002"; REV = "REV 00 — CONCEITO"; DATE = "18/09/2026"; CODE = "ZF-BD-01"
SVG_DIR = os.path.join(OUT_DIR, "cama"); os.makedirs(SVG_DIR, exist_ok=True)
LINEN = "#F1EBDF"; LINEN2 = "#E6DCC8"; FREIJO = "#C9A472"; FREIJO2 = "#B08A58"; BRASS = "#A48A57"; CANE = "#E4D6B8"; LED = "#F7E3B0"

# ------------------------------------------------------------------ geometria (m)  · eixo x = largura (0 no eixo), y = comprimento (0 na cabeceira), z = altura
class Bed:
    MAT_W, MAT_L, MAT_H = 1.58, 1.98, 0.25          # colchão queen
    CLEAR = 0.01                                      # folga do colchão
    POST = 0.070; POST_UP = 0.060                     # pé inferior 70 x 70 · coluna superior 60 x 60
    RAIL_T, RAIL_H = 0.040, 0.180                     # travessas laterais (esp. x altura)
    RAIL_TOP = 0.350                                  # topo da travessa (piso = 0)
    SLAT_T, SLAT_W, SLAT_N = 0.020, 0.070, 16         # ripas
    TOP_T, TOP_H = 0.040, 0.070                       # quadro do dossel 40 x 70
    H_TOTAL = 2.200                                   # topo do arco do dossel
    HEAD_H = 1.300                                    # topo do arco da cabeceira
    HEAD_T = 0.060                                    # espessura do painel da cabeceira
    UPH_H = 0.600                                     # painel estofado (altura acima da travessa)
    def __init__(self):
        self.in_w = self.MAT_W + 2 * self.CLEAR; self.in_l = self.MAT_L + 2 * self.CLEAR     # vão interno 1,60 x 2,00
        self.out_w = self.in_w + 2 * self.RAIL_T + 2 * self.POST - 2 * self.RAIL_T          # postes fora das travessas laterais → largura externa
        self.out_w = self.in_w + 2 * self.POST                                              # 1,60 + 0,14 = 1,74 → ajustar: travessa encosta no poste por dentro
        self.out_l = self.in_l + 2 * self.POST                                              # 2,14
        self.x_post = self.in_w / 2 + self.POST / 2                                         # eixo dos postes
        self.y_post = [self.POST / 2, self.in_l + self.POST * 1.5]
        self.rise_top = self.in_l / 12; self.rise_head = self.in_w / 12
        self.post_top = self.H_TOTAL - self.rise_top - 0.010                                # topo do poste sob a travessa arqueada (2,033)
        self.rail_z1 = self.RAIL_TOP - self.RAIL_H; self.slat_z = self.RAIL_TOP - 0.030
        self.mat_top = self.slat_z + self.SLAT_T + self.MAT_H
    def arc_pts(self, x1, x2, y, rise, n=24):
        """pontos (x, z) de um arco raso de x1 a x2 com apoio em y e flecha rise."""
        c = (x1 + x2) / 2; hw = (x2 - x1) / 2; R = (hw ** 2 + rise ** 2) / (2 * rise)
        return [(c + hw * t, y - R + math.sqrt(max(R ** 2 - (hw * t) ** 2, 0.0))) for t in np.linspace(-1, 1, n)]

B = Bed()

# ------------------------------------------------------------------ folhas
def sheet(w=1600, h=1000, scale=260.0, ox=800, oy=880, flip=True):
    return Sheet(w, h, scale, ox, oy, flip_y=flip)

def stamp(sh, title, sub, scale_txt, folha):
    sh.header(f"{CODE} · ZION CANOPY BED · {title}", sub)
    sh.title_block("ZION CANOPY BED", title, scale_txt, folha, "ZG-FFE-002 · REV 00 · unidade: mm")

def post_front(sh, x, z_top, upper=True):
    p = B.POST; pu = B.POST_UP
    sh.rect(x - p / 2, 0, x + p / 2, B.RAIL_TOP + 0.10, fill=FREIJO, stroke=GREEN, sw=1.1)
    sh.rect(x - 0.045, 0, x + 0.045, 0.015, fill=BRASS, stroke=GREEN, sw=0.7)          # sapata
    if upper:
        sh.rect(x - pu / 2, B.RAIL_TOP + 0.10, x + pu / 2, z_top, fill=FREIJO, stroke=GREEN, sw=1.1)
        sh.rect(x - 0.040, B.RAIL_TOP + 0.10 - 0.012, x + 0.040, B.RAIL_TOP + 0.10 + 0.012, fill=BRASS, stroke=GREEN, sw=0.7)   # anel de latão na junta

def arc_poly(sh, x1, x2, z_base, rise, depth, fill=FREIJO):
    top = B.arc_pts(x1, x2, z_base + rise, rise)
    pts = top + [(x2, z_base - depth), (x1, z_base - depth)]
    sh.poly(pts, fill=fill, stroke=GREEN, sw=1.1)

def elev_front():
    """FB-01 · vista frontal (dos pés da cama): postes, travessa dos pés, quadro do dossel arqueado, cortinas abertas, cabeceira ao fundo."""
    sh = sheet(); stamp(sh, "VISTA FRONTAL", "dos pés da cama · cortinas recolhidas nos postes · cabeceira ao fundo", "1:10", "FB-01")
    X = B.x_post
    # cabeceira ao fundo (painel + arco + palhinha)
    arc_poly(sh, -X + B.POST / 2, X - B.POST / 2, B.HEAD_H - B.rise_head, B.rise_head, 0.28, fill=CANE)
    sh.rect(-X + B.POST / 2, B.RAIL_TOP, X - B.POST / 2, B.RAIL_TOP + B.UPH_H, fill=LINEN, stroke=GREEN, sw=1.0)
    sh.rect(-X + B.POST / 2, B.RAIL_TOP + B.UPH_H, X - B.POST / 2, B.HEAD_H - B.rise_head - 0.28, fill=CANE, stroke=GREEN, sw=0.8)
    # LED indireto atrás do arco
    sh.line(-X + 0.1, B.HEAD_H - B.rise_head + 0.02, X - 0.1, B.HEAD_H - B.rise_head + 0.02, LED, 4.0, opacity=0.9)
    # colchão e travessa dos pés
    sh.rect(-B.in_w / 2, B.slat_z + B.SLAT_T, B.in_w / 2, B.mat_top, fill="#FFFFFF", stroke=GREEN, sw=0.9)
    sh.rect(-X + B.POST / 2, B.rail_z1, X - B.POST / 2, B.RAIL_TOP, fill=FREIJO, stroke=GREEN, sw=1.1)
    sh.line(-X + B.POST / 2, B.rail_z1 + B.RAIL_H / 3, X - B.POST / 2, B.rail_z1 + B.RAIL_H / 3, EARTH, 1.4)      # friso
    # cortinas recolhidas nos postes (2 por lado nesta vista)
    for sgn in (-1, 1):
        for k in (0, 1):
            x0 = sgn * (X - B.POST_UP / 2 - 0.02 - k * 0.09)
            sh.poly([(x0, B.post_top - 0.02), (x0 - sgn * 0.08, B.post_top - 0.02), (x0 - sgn * 0.10, 0.06), (x0 + sgn * 0.01, 0.06)], fill=LINEN if k else LINEN2, stroke=GREEN, sw=0.7)
    # quadro do dossel: travessa dos pés (reta) e arcos laterais vistos de topo (só a espessura)
    sh.rect(-X - B.POST_UP / 2, B.post_top, X + B.POST_UP / 2, B.post_top + B.TOP_H, fill=FREIJO, stroke=GREEN, sw=1.1)
    # arco frontal da travessa dos pés: opção com arco baixo — aqui a travessa dos pés é reta e o arco é nas laterais; mostrar o arco lateral por trás em linha tracejada
    top = B.arc_pts(-X, X, B.H_TOTAL, B.rise_head)
    sh.poly(top, fill="none", stroke=GREEN, sw=0.8, close=False, dash="4 3")
    for sgn in (-1, 1): post_front(sh, sgn * X, B.post_top)
    # cotas
    sh.dim(-B.out_w / 2, -0.12, B.out_w / 2, -0.12, -0.10, label=f"{B.out_w * 1000:.0f}")
    sh.dim(-B.in_w / 2, -0.30, B.in_w / 2, -0.30, -0.10, label=f"{B.in_w * 1000:.0f} (vão do colchão 1.580 + 2 x 10)")
    sh.dim(B.out_w / 2 + 0.15, 0, B.out_w / 2 + 0.15, B.H_TOTAL, 0.12, label=f"{B.H_TOTAL * 1000:.0f}")
    sh.dim(B.out_w / 2 + 0.15, 0, B.out_w / 2 + 0.15, B.post_top, 0.42, label=f"{B.post_top * 1000:.0f} topo do poste")
    sh.dim(-B.out_w / 2 - 0.15, 0, -B.out_w / 2 - 0.15, B.mat_top, -0.12, label=f"{B.mat_top * 1000:.0f} topo do colchão")
    sh.dim(-B.out_w / 2 - 0.15, 0, -B.out_w / 2 - 0.15, B.RAIL_TOP, -0.42, label=f"{B.RAIL_TOP * 1000:.0f}")
    sh.dim(-B.out_w / 2 - 0.15, 0, -B.out_w / 2 - 0.15, B.HEAD_H, -0.72, label=f"{B.HEAD_H * 1000:.0f} cabeceira")
    sh.leader(0, B.HEAD_H - B.rise_head + 0.02, 0.55, B.HEAD_H + 0.25, "fita LED 2700 K atrás do arco da cabeceira (luz indireta no véu)", 12)
    sh.leader(-0.5, B.RAIL_TOP + B.UPH_H + 0.15, -0.95, B.HEAD_H + 0.42, "faixa de palhinha sextavada (ZR-01) sob o Arco", 12, anchor="end")
    sh.leader(0.45, B.RAIL_TOP + 0.3, 0.95, 1.05, "painel estofado em linho hotelaria areia (ZT-02-SA), 600 mm", 12)
    sh.leader(X - 0.08, 1.5, X + 0.35, 1.70, "cortina de linho lavado (ZT-01) recolhida no poste, 2 painéis por lado", 12)
    sh.leader(-X + B.POST / 2 + 0.2, B.rail_z1 + B.RAIL_H / 3, -0.7, 0.05, "Friso Zion 4 x 4 mm a 1/3 da travessa", 12, anchor="end")
    sh.leader(X, B.RAIL_TOP + 0.10, X + 0.35, 0.62, "anel de latão: junta poste 70 → coluna 60 (parafuso de cama M10)", 12)
    sh.scalebar(-0.9, -0.55, 2, 1)
    sh.save(os.path.join(SVG_DIR, "FB-01_vista_frontal.svg"))

def elev_side():
    """FB-02 · vista lateral: arco do dossel, trilho, cortinas fechadas de um lado, cabeceira à esquerda."""
    sh = sheet(scale=230.0, ox=270, oy=880); stamp(sh, "VISTA LATERAL", "lado direito · Arco Zion no quadro do dossel (flecha = vão / 12) · cortina fechada", "1:10", "FB-02")
    Y0, Y1 = B.y_post
    # cabeceira (esp. 60) entre postes, arco ao topo visto de lado = retângulo
    sh.rect(B.POST, B.RAIL_TOP, B.POST + B.HEAD_T, B.HEAD_H, fill=FREIJO2, stroke=GREEN, sw=1.0)
    # travessa lateral e colchão
    sh.rect(B.POST, B.rail_z1, B.POST + B.in_l, B.RAIL_TOP, fill=FREIJO, stroke=GREEN, sw=1.1)
    sh.line(B.POST, B.rail_z1 + B.RAIL_H / 3, B.POST + B.in_l, B.rail_z1 + B.RAIL_H / 3, EARTH, 1.4)
    sh.rect(B.POST + B.HEAD_T, B.RAIL_TOP, B.POST + B.in_l, B.mat_top, fill="#FFFFFF", stroke=GREEN, sw=0.9)
    # cortina fechada (painel ondulado)
    xs = np.linspace(B.POST + B.POST_UP / 2 + 0.03, B.POST + B.in_l - 0.03, 40)
    pts = [(x, B.post_top - 0.01) for x in xs] + [(x, 0.06 + 0.012 * math.sin(i * 1.9)) for i, x in enumerate(reversed(xs))]
    sh.poly(pts, fill=LINEN, stroke=GREEN, sw=0.7, opacity=0.95)
    for i, x in enumerate(xs[::3]):
        sh.line(x, B.post_top - 0.05, x + 0.01, 0.08, "#D9CFBB", 0.8)
    # abas (tab top) no trilho
    for x in np.arange(B.POST + 0.12, B.POST + B.in_l, 0.15):
        sh.rect(x - 0.02, B.post_top - 0.045, x + 0.02, B.post_top + 0.005, fill=LINEN2, stroke=GREEN, sw=0.6)
    # quadro do dossel arqueado (lado)
    arc_poly(sh, B.POST_UP / 2 + 0.005, B.POST + B.in_l + B.POST - B.POST_UP / 2 - 0.005, B.H_TOTAL - B.rise_top, B.rise_top, B.TOP_H)
    for y in (Y0, Y1): post_front(sh, y, B.post_top)
    # cotas
    sh.dim(0, -0.12, B.out_l, -0.12, -0.10, label=f"{B.out_l * 1000:.0f}")
    sh.dim(B.POST, -0.30, B.POST + B.in_l, -0.30, -0.10, label=f"{B.in_l * 1000:.0f} (colchão 1.980 + 2 x 10)")
    sh.dim(B.out_l + 0.15, 0, B.out_l + 0.15, B.H_TOTAL, 0.12, label=f"{B.H_TOTAL * 1000:.0f}")
    sh.dim(B.out_l + 0.15, B.H_TOTAL - B.rise_top, B.out_l + 0.15, B.H_TOTAL, 0.42, label=f"flecha {B.rise_top * 1000:.0f}")
    sh.dim(-0.15, 0, -0.15, B.HEAD_H, -0.12, label=f"{B.HEAD_H * 1000:.0f}")
    sh.dim(-0.15, 0, -0.15, B.RAIL_TOP, -0.42, label=f"{B.RAIL_TOP * 1000:.0f}")
    sh.leader(B.out_l / 2, B.H_TOTAL - 0.02, B.out_l / 2 + 0.3, B.H_TOTAL + 0.28, f"Arco Zion: vão {B.in_l * 1000:.0f} · flecha {B.rise_top * 1000:.0f} · R ≈ {((B.in_l / 2) ** 2 + B.rise_top ** 2) / (2 * B.rise_top) * 1000:.0f} mm", 12)
    sh.leader(B.POST + 0.5, B.post_top - 0.02, B.POST + 0.2, B.post_top + 0.35, "trilho oculto no rasgo inferior do quadro (Véu Zion) · deslizadores + abas de linho a cada 150 mm", 12, anchor="start")
    sh.leader(B.POST + 1.2, 1.1, B.POST + 1.45, 1.55, "cortina de linho lavado 220 g/m² · 2 painéis de 1.100 x 2.000 por lado", 12)
    sh.scalebar(0.0, -0.55, 2, 1)
    sh.save(os.path.join(SVG_DIR, "FB-02_vista_lateral.svg"))

def plan_top():
    """FB-03 · vista superior: quadro do dossel, postes, colchão, ripas (metade), trilhos."""
    sh = sheet(scale=300.0, ox=800, oy=920); stamp(sh, "VISTA SUPERIOR", "quadro do dossel · postes · ripas (metade à esquerda) · colchão (metade à direita) · trilhos", "1:8", "FB-03")
    X = B.x_post; L = B.out_l
    # quadro do dossel
    sh.rect(-X - B.POST_UP / 2, 0, X + B.POST_UP / 2, L, fill=FREIJO, stroke=GREEN, sw=1.1)
    sh.rect(-X + B.POST_UP / 2, B.POST_UP, X - B.POST_UP / 2, L - B.POST_UP, fill=CREAM, stroke=GREEN, sw=1.1)
    # trilhos (linha tracejada dentro do quadro)
    for x in (-X, X): sh.line(x, B.POST_UP + 0.05, x, L - B.POST_UP - 0.05, EARTH, 1.2, dash="6 4")
    for y in (B.POST_UP / 2 + 0.005, L - B.POST_UP / 2 - 0.005): sh.line(-X + 0.1, y, X - 0.1, y, EARTH, 1.2, dash="6 4")
    # ripas (metade esquerda) e colchão (metade direita)
    ys = np.linspace(B.POST + 0.06, B.POST + B.in_l - 0.06, B.SLAT_N)
    for y in ys: sh.rect(-B.in_w / 2, y - B.SLAT_W / 2, 0, y + B.SLAT_W / 2, fill=WOOD, stroke=GREEN, sw=0.6)
    sh.rect(-0.04, B.POST, 0.04, B.POST + B.in_l, fill=FREIJO2, stroke=GREEN, sw=0.8)                       # longarina central
    sh.rect(0.005, B.POST + B.CLEAR, B.MAT_W / 2, B.POST + B.CLEAR + B.MAT_L, fill="#FFFFFF", stroke=GREEN, sw=0.9)
    # cabeceira
    sh.rect(-X + B.POST / 2, B.POST, X - B.POST / 2, B.POST + B.HEAD_T, fill=FREIJO2, stroke=GREEN, sw=1.0)
    # postes
    for sx in (-1, 1):
        for y in B.y_post:
            sh.rect(sx * X - B.POST / 2, y - B.POST / 2, sx * X + B.POST / 2, y + B.POST / 2, fill=FREIJO2, stroke=GREEN, sw=1.2)
            sh.rect(sx * X - B.POST_UP / 2, y - B.POST_UP / 2, sx * X + B.POST_UP / 2, y + B.POST_UP / 2, fill="none", stroke=GREEN, sw=0.6)
    # pés intermediários
    for sx in (-1, 0, 1):
        sh.rect(sx * (B.in_w / 2 - 0.05) - 0.03, L / 2 - 0.03, sx * (B.in_w / 2 - 0.05) + 0.03, L / 2 + 0.03, fill="none", stroke=GREEN, sw=0.8, dash="3 2")
    sh.dim(-B.out_w / 2, -0.12, B.out_w / 2, -0.12, -0.10, label=f"{B.out_w * 1000:.0f}")
    sh.dim(-B.in_w / 2, -0.3, B.in_w / 2, -0.3, -0.10, label=f"{B.in_w * 1000:.0f}")
    sh.dim(B.out_w / 2 + 0.15, 0, B.out_w / 2 + 0.15, L, 0.12, label=f"{L * 1000:.0f}")
    sh.dim(B.out_w / 2 + 0.15, B.POST, B.out_w / 2 + 0.15, B.POST + B.in_l, 0.42, label=f"{B.in_l * 1000:.0f}")
    sh.dim(-B.out_w / 2 - 0.15, B.POST + 0.06, -B.out_w / 2 - 0.15, B.POST + 0.06 + (ys[1] - ys[0]), -0.12, label=f"{(ys[1] - ys[0]) * 1000:.0f} (ripas 20 x 70)")
    sh.leader(-X, L / 2, -X - 0.35, L / 2 + 0.55, "trilho de cortina embutido no quadro (rasgo 30 x 14)", 12, anchor="end")
    sh.leader(0.0, L / 2, 0.4, L + 0.35, "longarina central 40 x 80 com 3 pés intermediários 60 x 60 (tracejados)", 12)
    sh.leader(0.5, B.POST + 0.03, 0.9, -0.55, "cabeceira 60 mm entre os postes da cabeceira", 12)
    sh.scalebar(-0.9, -0.62, 2, 1)
    sh.save(os.path.join(SVG_DIR, "FB-03_vista_superior.svg"))

def elev_rear():
    """FB-04 · vista posterior (da cabeceira): costas da cabeceira, régua de LED, travessa reta do dossel."""
    sh = sheet(); stamp(sh, "VISTA POSTERIOR", "da cabeceira · costas do painel · canaleta de LED · saída do cabo", "1:10", "FB-04")
    X = B.x_post
    arc_poly(sh, -X + B.POST / 2, X - B.POST / 2, B.HEAD_H - B.rise_head, B.rise_head, B.HEAD_H - B.rise_head - B.RAIL_TOP, fill=FREIJO)
    sh.rect(-X + B.POST / 2 + 0.04, B.RAIL_TOP + 0.04, X - B.POST / 2 - 0.04, B.HEAD_H - B.rise_head - 0.06, fill="#F6F1E8", stroke=GREEN, sw=0.6)   # tampo traseiro (compensado)
    sh.line(-X + 0.15, B.HEAD_H - B.rise_head - 0.03, X - 0.15, B.HEAD_H - B.rise_head - 0.03, LED, 5.0, opacity=0.9)
    sh.rect(-0.03, B.RAIL_TOP + 0.04, 0.03, B.RAIL_TOP + 0.12, fill=BRASS, stroke=GREEN, sw=0.6)     # saída de cabo
    sh.rect(-X + B.POST / 2, B.rail_z1, X - B.POST / 2, B.RAIL_TOP, fill=FREIJO, stroke=GREEN, sw=1.1)
    sh.rect(-X - B.POST_UP / 2, B.post_top, X + B.POST_UP / 2, B.post_top + B.TOP_H, fill=FREIJO, stroke=GREEN, sw=1.1)
    for sgn in (-1, 1): post_front(sh, sgn * X, B.post_top)
    for sgn in (-1, 1):
        x0 = sgn * (X - B.POST_UP / 2 - 0.02)
        sh.poly([(x0, B.post_top - 0.02), (x0 - sgn * 0.16, B.post_top - 0.02), (x0 - sgn * 0.19, 0.06), (x0 + sgn * 0.01, 0.06)], fill=LINEN, stroke=GREEN, sw=0.7)
    sh.dim(-B.out_w / 2, -0.12, B.out_w / 2, -0.12, -0.10, label=f"{B.out_w * 1000:.0f}")
    sh.dim(B.out_w / 2 + 0.15, B.RAIL_TOP, B.out_w / 2 + 0.15, B.HEAD_H, 0.12, label=f"{(B.HEAD_H - B.RAIL_TOP) * 1000:.0f}")
    sh.leader(0.3, B.HEAD_H - B.rise_head - 0.03, 0.8, B.HEAD_H + 0.3, "canaleta de alumínio com fita LED 24 V 2700 K + difusor, voltada para o véu", 12)
    sh.leader(0.0, B.RAIL_TOP + 0.08, 0.4, 0.15, "passa-cabo de latão · fonte 24 V e dimmer no criado-mudo", 12)
    sh.leader(-0.6, 0.9, -1.0, 1.55, "tampo traseiro em compensado 6 mm laminado em freijó (limpeza, sem tecido nas costas)", 12, anchor="end")
    sh.scalebar(-0.9, -0.55, 2, 1)
    sh.save(os.path.join(SVG_DIR, "FB-04_vista_posterior.svg"))

# ------------------------------------------------------------------ isométricas
def bed_scene(sc, dz=None, curtains=True, mattress=True, head=True, canopy=True, posts=True, base=True, lifted=None):
    """desenha a cama na cena; lifted = dict grupo → deslocamento z (explodido)."""
    L = lifted or {}
    X = B.x_post; Y0, Y1 = B.y_post; g = lambda k: L.get(k, 0.0)
    if base:
        z = g("base")
        # travessas laterais e dos pés/cabeceira
        for sx in (-1, 1): sc.box(sx * B.in_w / 2 + (0 if sx > 0 else -B.RAIL_T), sx * B.in_w / 2 + (B.RAIL_T if sx > 0 else 0), B.POST, B.POST + B.in_l, B.rail_z1 + z, B.RAIL_TOP + z, FREIJO)
        for y in (B.POST - B.RAIL_T, B.POST + B.in_l): sc.box(-B.in_w / 2 - B.RAIL_T, B.in_w / 2 + B.RAIL_T, y, y + B.RAIL_T, B.rail_z1 + z, B.RAIL_TOP + z, FREIJO)
        sc.box(-0.04, 0.04, B.POST, B.POST + B.in_l, B.rail_z1 + z, B.slat_z + z, FREIJO2)
        for y in np.linspace(B.POST + 0.06, B.POST + B.in_l - 0.06, B.SLAT_N): sc.box(-B.in_w / 2, B.in_w / 2, y - B.SLAT_W / 2, y + B.SLAT_W / 2, B.slat_z + z, B.slat_z + B.SLAT_T + z, WOOD)
        for sx in (-1, 0, 1): sc.box(sx * (B.in_w / 2 - 0.05) - 0.03, sx * (B.in_w / 2 - 0.05) + 0.03, B.out_l / 2 - 0.03, B.out_l / 2 + 0.03, 0 + z, B.rail_z1 + z, FREIJO2)
        # pés inferiores 70 x 70 até o anel
        for sx in (-1, 1):
            for y in (Y0, Y1):
                sc.box(sx * X - B.POST / 2, sx * X + B.POST / 2, y - B.POST / 2, y + B.POST / 2, 0 + z, B.RAIL_TOP + 0.10 + z, FREIJO2)
                sc.box(sx * X - 0.045, sx * X + 0.045, y - 0.045, y + 0.045, 0 + z, 0.015 + z, BRASS)
                sc.box(sx * X - 0.04, sx * X + 0.04, y - 0.04, y + 0.04, B.RAIL_TOP + 0.10 - 0.012 + z, B.RAIL_TOP + 0.10 + 0.012 + z, BRASS)
    if mattress:
        z = g("mattress")
        sc.box(-B.MAT_W / 2, B.MAT_W / 2, B.POST + B.CLEAR, B.POST + B.CLEAR + B.MAT_L, B.slat_z + B.SLAT_T + z, B.mat_top + z, "#FFFFFF")
        sc.box(-B.MAT_W / 2 + 0.05, B.MAT_W / 2 - 0.05, B.POST + 0.08, B.POST + 0.55, B.mat_top + z, B.mat_top + 0.14 + z, "#F7F3EC")     # travesseiros
        sc.box(-B.MAT_W / 2 + 0.02, B.MAT_W / 2 - 0.02, B.POST + 1.25, B.POST + 1.95, B.mat_top + z, B.mat_top + 0.05 + z, "#B7B58F")     # manta oliva
    if head:
        z = g("head")
        sc.box(-B.in_w / 2, B.in_w / 2, B.POST, B.POST + B.HEAD_T, B.RAIL_TOP + z, B.RAIL_TOP + B.UPH_H + z, LINEN)
        sc.box(-B.in_w / 2, B.in_w / 2, B.POST, B.POST + B.HEAD_T, B.RAIL_TOP + B.UPH_H + z, B.HEAD_H - B.rise_head - 0.28 + z, CANE)
        # arco da cabeceira (malha)
        top = B.arc_pts(-B.in_w / 2, B.in_w / 2, B.HEAD_H, B.rise_head, 16)
        for (xa, za), (xb, zb) in zip(top[:-1], top[1:]):
            sc.quad((xa, B.POST, B.HEAD_H - B.rise_head - 0.28 + z), (xb, B.POST, B.HEAD_H - B.rise_head - 0.28 + z), (xb, B.POST, zb + z), (xa, B.POST, za + z), FREIJO)
            sc.quad((xa, B.POST, za + z), (xb, B.POST, zb + z), (xb, B.POST + B.HEAD_T, zb + z), (xa, B.POST + B.HEAD_T, za + z), FREIJO2)
        sc.box(-B.in_w / 2 + 0.1, B.in_w / 2 - 0.1, B.POST + 0.02, B.POST + B.HEAD_T - 0.02, B.HEAD_H - B.rise_head - 0.02 + z, B.HEAD_H - B.rise_head + 0.005 + z, LED)
    if posts:
        z = g("posts")
        for sx in (-1, 1):
            for y in (Y0, Y1): sc.box(sx * X - B.POST_UP / 2, sx * X + B.POST_UP / 2, y - B.POST_UP / 2, y + B.POST_UP / 2, B.RAIL_TOP + 0.10 + z, B.post_top + z, FREIJO)
    if curtains:
        z = g("curtains")
        for sx in (-1, 1):
            # lado: um painel recolhido junto ao poste da cabeceira, outro meio aberto
            x0 = sx * (X - B.POST_UP / 2 - 0.01); w = 0.06 * sx
            sc.box(min(x0, x0 + w), max(x0, x0 + w), Y0 + 0.06, Y0 + 0.36, 0.06 + z, B.post_top - 0.02 + z, LINEN)
            sc.box(min(x0, x0 + w), max(x0, x0 + w), Y1 - 0.85, Y1 - 0.06, 0.06 + z, B.post_top - 0.02 + z, LINEN2)
        # pés da cama: painel fechado à esquerda, recolhido à direita
        y0 = Y1 - B.POST_UP / 2 - 0.01
        sc.box(-B.in_w / 2 + 0.03, -0.05, y0 - 0.05, y0, 0.06 + z, B.post_top - 0.02 + z, LINEN)
        sc.box(B.in_w / 2 - 0.30, B.in_w / 2 - 0.03, y0 - 0.05, y0, 0.06 + z, B.post_top - 0.02 + z, LINEN2)
    if canopy:
        z = g("canopy")
        # travessas retas da cabeceira e dos pés
        for y in (Y0 - B.POST_UP / 2, Y1 - B.POST_UP / 2): sc.box(-X - B.POST_UP / 2, X + B.POST_UP / 2, y, y + B.TOP_T, B.post_top + z, B.post_top + B.TOP_H + z, FREIJO)
        # laterais arqueadas
        top = B.arc_pts(Y0, Y1, B.H_TOTAL, B.rise_top, 18)
        for sx in (-1, 1):
            xa, xb = sx * X - B.TOP_T / 2, sx * X + B.TOP_T / 2
            for (ya, za), (yb, zb) in zip(top[:-1], top[1:]):
                zb0 = B.post_top + z
                sc.quad((xa, ya, zb0), (xa, yb, zb0), (xa, yb, zb + z), (xa, ya, za + z), FREIJO)
                sc.quad((xb, ya, zb0), (xb, yb, zb0), (xb, yb, zb + z), (xb, ya, za + z), FREIJO)
                sc.quad((xa, ya, za + z), (xb, ya, za + z), (xb, yb, zb + z), (xa, yb, zb + z), FREIJO2)

def iso_view():
    sh = Sheet(1600, 1000); stamp(sh, "VISTA ISOMÉTRICA", "render de estudo · freijó a óleo, linho lavado, palhinha, latão envelhecido, luz indireta", "s/ escala", "FB-05")
    sc = Scene(sh, 215.0, 880, 700)
    # sombra e piso
    pts = [sc.proj(p) for p in [(-1.3, -0.3, -0.005), (1.3, -0.3, -0.005), (1.3, 2.6, -0.005), (-1.3, 2.6, -0.005)]]
    sc.pre.append('<polygon points="' + " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts) + '" fill="#EFE5D8" fill-opacity="0.9"/>')
    bed_scene(sc)
    sc.render()
    sh.legend(60, 720, [(1, "Quadro do dossel 40 x 70 com Arco Zion nas laterais (flecha 167 mm)"), (2, "Colunas 60 x 60 sobre pés 70 x 70, anel de latão na junta"), (3, "Cabeceira: linho estofado + palhinha + Arco com LED indireto"), (4, "Véu Zion: linho lavado em trilho oculto, 8 painéis"), (5, "Base: travessas 40 x 180 com Friso, 16 ripas, longarina central"), (6, "Sapatas de latão 15 mm com nivelador")])
    sh.save(os.path.join(SVG_DIR, "FB-05_isometrica.svg"))

def exploded():
    sh = Sheet(1600, 1000); stamp(sh, "MODELO EXPLODIDO", "os 6 grupos de montagem · 2 pessoas · 45 minutos · parafusos de cama M10 e Minifix", "s/ escala", "FB-07")
    sc = Scene(sh, 150.0, 720, 880)
    L = dict(base=0.0, mattress=0.55, head=0.95, posts=1.35, curtains=2.15, canopy=2.75)
    bed_scene(sc, lifted=L)
    sc.render()
    labels = [("F · QUADRO DO DOSSEL · 4 travessas + 8 deslizadores", (B.x_post + 0.2, B.y_post[1], B.H_TOTAL + L["canopy"])), ("E · VÉU · 8 painéis de linho com abas", (B.x_post + 0.1, 1.0, 1.4 + L["curtains"])), ("D · 4 COLUNAS 60 x 60 · encaixe no anel de latão", (B.x_post + 0.05, B.y_post[0], 1.6 + L["posts"])), ("C · CABECEIRA · painel + arco + LED", (-0.3, B.POST, B.HEAD_H + L["head"])), ("B · COLCHÃO QUEEN 1.580 x 1.980 x 250", (0.8, 1.2, B.mat_top + L["mattress"])), ("A · BASE · 4 pés, 4 travessas, longarina, 16 ripas", (B.x_post, 1.0, B.RAIL_TOP))]
    for i, (t, p) in enumerate(labels):
        P = sc.proj(p); X, Y = 1180, 150 + i * 100
        sh.add(f'<line x1="{P[0]:.1f}" y1="{P[1]:.1f}" x2="{X}" y2="{Y}" stroke="{GREEN}" stroke-width="0.7"/><circle cx="{P[0]:.1f}" cy="{P[1]:.1f}" r="2.5" fill="{GREEN}"/>')
        sh.text_px(X + 6, Y + 4, t, size=12, anchor="start", weight=600)
    sh.save(os.path.join(SVG_DIR, "FB-07_explodido.svg"))

def details():
    """FB-06 · detalhes: junta poste/coluna, seção do quadro com trilho, seção da cabeceira com LED, parafuso de cama."""
    sh = Sheet(1600, 1000); stamp(sh, "DETALHES", "D1 junta poste / coluna · D2 quadro do dossel com trilho · D3 cabeceira com LED · D4 travessa / pé com parafuso de cama", "1:2 · 1:4", "FB-06")
    def sub(scale, ox, oy):
        t = Sheet(1600, 1000, scale, ox, oy); t.parts = sh.parts; t.defs = sh.defs; t._pattern_ids = sh._pattern_ids; return t
    for x, t in ((210, "D1 · JUNTA POSTE / COLUNA · 1:2"), (600, "D2 · QUADRO DO DOSSEL · TRILHO · 1:2"), (990, "D3 · CABECEIRA · SEÇÃO · 1:4"), (1350, "D4 · TRAVESSA / PÉ · PLANTA · 1:2")):
        sh.text_px(x, 120, t, size=12, weight=700, anchor="middle", spacing=0.08)
        sh.add(f'<line x1="{x - 150}" y1="128" x2="{x + 150}" y2="128" stroke="{SAND}" stroke-width="0.8"/>')
    # D1 · junta poste 70 → coluna 60 com anel de latão
    d = sub(1100.0, 210, 600)
    d.rect(-0.035, -0.20, 0.035, 0.0, fill=FREIJO2, stroke=GREEN, sw=1.2)
    d.rect(-0.030, 0.0, 0.030, 0.22, fill=FREIJO, stroke=GREEN, sw=1.2)
    d.rect(-0.040, -0.012, 0.040, 0.012, fill=BRASS, stroke=GREEN, sw=0.9)
    d.rect(-0.006, -0.10, 0.006, 0.10, fill="none", stroke=GREEN, sw=0.9, dash="4 3")
    d.rect(-0.018, -0.115, 0.018, -0.085, fill="none", stroke=GREEN, sw=0.9, dash="4 3")
    d.dim(-0.035, -0.23, 0.035, -0.23, -0.02, label="70"); d.dim(-0.030, 0.25, 0.030, 0.25, 0.02, label="60"); d.dim(0.06, -0.012, 0.06, 0.012, 0.03, label="24")
    d.leader(0.040, 0.0, 0.11, 0.05, "anel de latão Ø80 x 24", 11); d.leader(0.006, 0.06, 0.11, 0.11, "parafuso de cama M10 x 200", 11); d.leader(0.0, -0.10, 0.11, -0.12, "porca-tambor Ø16", 11); d.leader(0.0, -0.19, 0.11, -0.18, "pé 70 x 70 da base", 11)
    d.text_px(210, 870, "coluna encaixa no anel com folga 0,3 mm; aperto por baixo do pé", size=10, fill=EARTH)
    # D2 · seção do quadro do dossel com trilho
    d = sub(2400.0, 600, 520)
    d.poly([(-0.020, 0), (0.020, 0), (0.020, 0.070), (-0.020, 0.070)], fill=FREIJO, stroke=GREEN, sw=1.2)
    d.rect(-0.015, 0.0, 0.015, 0.014, fill=CREAM, stroke=GREEN, sw=1.0)
    d.rect(-0.012, 0.003, 0.012, 0.012, fill="#D9D9D6", stroke=GREEN, sw=0.8)
    d.circle(0.0, 0.0, 0.004, fill=BRASS, stroke=GREEN, sw=0.6)
    d.line(0.0, -0.004, 0.0, -0.05, GREEN, 1.0); d.rect(-0.012, -0.05, 0.012, -0.03, fill=LINEN2, stroke=GREEN, sw=0.8)
    d.dim(-0.020, 0.085, 0.020, 0.085, 0.01, label="40"); d.dim(0.03, 0, 0.03, 0.070, 0.012, label="70"); d.dim(-0.015, -0.065, 0.015, -0.065, -0.01, label="30")
    d.leader(0.012, 0.008, 0.055, 0.045, "trilho alu 20 x 8 embutido", 11); d.leader(0.0, -0.04, 0.055, -0.02, "aba de linho no gancho", 11); d.leader(0.0, 0.055, 0.055, 0.075, "travessa 40 x 70 (arco)", 11)
    d.text_px(600, 870, "rasgo 30 x 14 fresado; deslizadores de nylon; batentes nas pontas", size=10, fill=EARTH)
    # D3 · seção da cabeceira com LED
    d = sub(500.0, 990, 560)
    d.rect(0.0, 0.0, 0.060, 0.30, fill=FREIJO, stroke=GREEN, sw=1.2)
    d.rect(0.006, -0.30, 0.054, 0.0, fill=CANE, stroke=GREEN, sw=0.9)
    d.rect(0.0, -0.55, 0.060, -0.30, fill=LINEN, stroke=GREEN, sw=0.9)
    d.rect(0.054, -0.55, 0.060, 0.30, fill="#F6F1E8", stroke=GREEN, sw=0.6)
    d.rect(0.010, 0.27, 0.050, 0.29, fill=LED, stroke=GREEN, sw=0.6)
    d.line(-0.02, 0.28, -0.22, 0.42, "#E8B84A", 2.0, dash="3 3"); d.line(-0.02, 0.28, -0.22, 0.18, "#E8B84A", 2.0, dash="3 3")
    d.dim(0.0, 0.34, 0.060, 0.34, 0.03, label="60"); d.dim(-0.06, -0.55, -0.06, -0.30, -0.04, label="250"); d.dim(-0.06, -0.30, -0.06, 0.0, -0.04, label="300"); d.dim(-0.06, 0.0, -0.06, 0.30, -0.04, label="300 (arco)")
    d.leader(0.03, 0.28, 0.13, 0.36, "canaleta LED 24 V 2700 K + difusor", 11); d.leader(0.03, -0.15, 0.13, -0.10, "palhinha ZR-01 em quadro removível", 11); d.leader(0.03, -0.45, 0.13, -0.42, "estofado: compensado 12 + D28 30 + linho", 11); d.leader(0.057, 0.10, 0.13, 0.12, "tampo traseiro 6 mm", 11)
    d.text_px(990, 870, "luz para cima e para o véu; costas limpas", size=10, fill=EARTH)
    # D4 · encontro travessa lateral / pé com parafuso de cama (planta)
    d = sub(900.0, 1330, 600)
    d.rect(-0.035, -0.035, 0.035, 0.035, fill=FREIJO2, stroke=GREEN, sw=1.2)
    d.rect(0.035, -0.020, 0.22, 0.020, fill=FREIJO, stroke=GREEN, sw=1.2)
    d.rect(-0.02, 0.035, 0.02, 0.22, fill=FREIJO, stroke=GREEN, sw=1.2)
    d.rect(-0.03, -0.005, 0.10, 0.005, fill="none", stroke=GREEN, sw=0.9, dash="3 2")
    d.circle(0.085, 0.0, 0.008, fill="none", stroke=GREEN, sw=0.9, dash="3 2"); d.circle(0.0, 0.0, 0.008, fill="none", stroke=GREEN, sw=0.9, dash="3 2")
    d.dim(-0.035, -0.06, 0.035, -0.06, -0.02, label="70"); d.dim(0.035, -0.045, 0.085, -0.045, -0.01, label="50")
    d.callout(0.085, 0.0, 1); d.callout(0.0, 0.0, 2); d.callout(0.0, 0.15, 3); d.callout(0.15, 0.0, 4)
    d.legend(1230, 740, [(1, "porca-tambor Ø16 a 50 mm da face do pé"), (2, "furo Ø10 vertical para o parafuso da coluna"), (3, "travessa dos pés 40 x 180 (mesma ligação)"), (4, "travessa lateral 40 x 180 · parafuso M10 x 120")], size=10)
    d.text_px(1330, 870, "cabeça embutida com tampão de nogueira (ZW-03)", size=10, fill=EARTH)
    sh.save(os.path.join(SVG_DIR, "FB-06_detalhes.svg"))

def concepts():
    """FB-08 · três conceitos em isométrica simplificada."""
    sh = Sheet(1600, 1000); stamp(sh, "TRÊS CONCEITOS", "A · ARCO (selecionado) · B · PORTAL · C · NINHO · mesma base, três dosséis", "s/ escala", "FB-08")
    for i, (name, kind) in enumerate((("A · ARCO", "arc"), ("B · PORTAL", "portal"), ("C · NINHO", "nest"))):
        sc = Scene(sh, 120.0, 330 + i * 500, 640)
        pts = [sc.proj(p) for p in [(-1.3, -0.3, -0.005), (1.3, -0.3, -0.005), (1.3, 2.6, -0.005), (-1.3, 2.6, -0.005)]]
        sc.pre.append('<polygon points="' + " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts) + '" fill="#EFE5D8" fill-opacity="0.9"/>')
        if kind == "arc":
            bed_scene(sc)
        elif kind == "portal":
            bed_scene(sc, curtains=False, canopy=False, posts=False, head=False)
            X = B.x_post
            for y in B.y_post:   # dois pórticos em U de madeira laminada
                sc.box(-X - 0.03, X + 0.03, y - 0.05, y + 0.05, B.post_top, B.post_top + 0.10, FREIJO)
                for sx in (-1, 1): sc.box(sx * X - 0.05, sx * X + 0.05, y - 0.05, y + 0.05, B.RAIL_TOP + 0.1, B.post_top, FREIJO)
            sc.box(-X, X, B.y_post[0], B.y_post[1], B.post_top + 0.10, B.post_top + 0.12, LINEN)  # teto de linho
            sc.box(-B.in_w / 2, B.in_w / 2, B.POST, B.POST + 0.06, B.RAIL_TOP, 1.05, LINEN)
            for sx in (-1, 1): sc.box(sx * (X - 0.06) - 0.03 * sx, sx * (X - 0.06), B.POST + 0.3, B.POST + 1.0, 0.06, B.post_top - 0.02, LINEN2)
        else:
            bed_scene(sc, curtains=False, canopy=False, posts=False, head=False)
            X = B.x_post
            for sx in (-1, 1):
                for y in B.y_post: sc.cylinder(sx * X, y, B.RAIL_TOP + 0.1, B.post_top, 0.035, CANE, 12)
            for y in (B.y_post[0] - 0.03, B.y_post[1] - 0.03): sc.box(-X - 0.04, X + 0.04, y, y + 0.06, B.post_top, B.post_top + 0.06, CANE)
            for sx in (-1, 1): sc.box(sx * X - 0.03, sx * X + 0.03, B.y_post[0], B.y_post[1], B.post_top, B.post_top + 0.06, CANE)
            # cabeceira trançada alta em arco (rattan)
            top = B.arc_pts(-B.in_w / 2, B.in_w / 2, 1.5, 0.25, 14)
            for (xa, za), (xb, zb) in zip(top[:-1], top[1:]): sc.quad((xa, B.POST, B.RAIL_TOP), (xb, B.POST, B.RAIL_TOP), (xb, B.POST, zb), (xa, B.POST, za), CANE)
            for sx in (-1, 1): sc.box(sx * (X - 0.06) - 0.03 * sx, sx * (X - 0.06), B.POST + 0.3, B.POST + 0.9, 0.06, B.post_top - 0.02, LINEN2)
        sc.render()
        sh.text_px(330 + i * 500, 800, name, size=16, weight=700, spacing=0.2)
    sh.text_px(330, 830, "quadro arqueado, colunas finas, cabeceira linho + palhinha, véu em trilho oculto", size=11, fill=EARTH)
    sh.text_px(830, 830, "dois pórticos em U de freijó laminado, teto de linho, cortinas só nas laterais", size=11, fill=EARTH)
    sh.text_px(1330, 830, "colunas e quadro envolvidos em rattan, cabeceira alta trançada em arco, véu leve", size=11, fill=EARTH)
    sh.save(os.path.join(SVG_DIR, "FB-08_conceitos.svg"))

# ------------------------------------------------------------------ BOM
def bom_rows():
    X = B.x_post
    rows = [("A01", "Pé inferior", 4, "freijó maciço ZW-01-O", f"70 x 70 x {(B.RAIL_TOP + 0.10) * 1000:.0f}", "70", "óleo natural", "sapata latão 15 + nivelador M8 · anel latão Ø80 x 24", "R1 nas arestas; furos para 2 parafusos de cama"),
            ("A02", "Travessa lateral", 2, "freijó maciço", f"40 x 180 x {B.in_l * 1000:.0f}", "40", "óleo", "2 porcas-tambor Ø16 por ponta", "Friso 4 x 4 a 60 mm da base; rebaixo 20 x 20 interno para as ripas"),
            ("A03", "Travessa da cabeceira e dos pés", 2, "freijó maciço", f"40 x 180 x {(B.in_w + 2 * B.RAIL_T) * 1000:.0f}", "40", "óleo", "2 porcas-tambor por ponta", "Friso contínuo"),
            ("A04", "Longarina central", 1, "freijó maciço", f"40 x 80 x {B.in_l * 1000:.0f}", "40", "óleo", "cantoneiras 40 x 40 nas pontas", "recebe as ripas no centro"),
            ("A05", "Pé intermediário", 3, "freijó maciço", f"60 x 60 x {B.rail_z1 * 1000:.0f}", "60", "óleo", "sapata latão + nivelador", "sob a longarina, no meio do vão"),
            ("A06", "Ripa", B.SLAT_N, "faia ou freijó laminado curvado", f"20 x 70 x {B.in_w * 1000:.0f}", "20", "natural", "encaixe em rebaixo + 1 parafuso central", "curvatura 12 mm (flexível) " + WARN),
            ("B01", "Colchão queen", 1, "molas ensacadas, pillow top", f"{B.MAT_W * 1000:.0f} x {B.MAT_L * 1000:.0f} x {B.MAT_H * 1000:.0f}", "", "", "", "FF&E (fora do lote de marcenaria)"),
            ("C01", "Quadro da cabeceira (montantes + arco)", 1, "freijó maciço, arco em 3 peças coladas (finger joint) ou laminado", f"60 x 60 · vão {B.in_w * 1000:.0f} · arco flecha {B.rise_head * 1000:.0f}", "60", "óleo", "4 parafusos M8 nos postes", "Arco Zion R ≈ " + f"{((B.in_w / 2) ** 2 + B.rise_head ** 2) / (2 * B.rise_head) * 1000:.0f} mm"),
            ("C02", "Painel estofado", 1, "compensado 12 + espuma D28 30 mm + manta 200 g + linho ZT-02-SA", f"{(B.in_w - 0.02) * 1000:.0f} x {B.UPH_H * 1000:.0f} x 50", "12", "capa com zíper", "4 clipes de mola", "removível para lavagem"),
            ("C03", "Quadro de palhinha", 1, "freijó 20 x 40 + palhinha sextavada ZR-01", f"{(B.in_w - 0.02) * 1000:.0f} x {(B.HEAD_H - B.rise_head - 0.28 - B.RAIL_TOP - B.UPH_H) * 1000:.0f}", "20", "verniz água fosco", "4 parafusos", "removível"),
            ("C04", "Tampo traseiro", 1, "compensado 6 mm laminado freijó", f"{(B.in_w - 0.08) * 1000:.0f} x {(B.HEAD_H - B.rise_head - B.RAIL_TOP - 0.10) * 1000:.0f}", "6", "verniz", "parafusos", "costas limpas, passa-cabo de latão"),
            ("C05", "Canaleta LED + fita + difusor", 1, "alumínio 17 x 8 + LED 24 V 2700 K IRC 90 9,6 W/m + difusor opalino", f"{(B.in_w - 0.2) * 1000:.0f}", "", "", "fonte 24 V 30 W + dimmer no criado", "1,4 m de fita"),
            ("D01", "Coluna do dossel", 4, "freijó maciço", f"60 x 60 x {(B.post_top - B.RAIL_TOP - 0.10) * 1000:.0f}", "60", "óleo", "parafuso de cama M10 x 200 no pé; espiga 30 x 30 x 40 no topo", "R1; cônica 60 → 55 nas 2 faces externas (opcional Icon)"),
            ("E01", "Cortina do véu", 8, "linho lavado ZT-01 220 g/m², off-white", "1.100 x 2.000 (+ barra 60)", "", "abas de 40 x 100 a cada 150 mm", "gancho de latão por aba", "lavável 40 °C; 4 laterais + 2 pés + 2 cabeceira (opcional)"),
            ("F01", "Travessa lateral do dossel (arqueada)", 2, "freijó laminado 5 lâminas de 8 mm coladas em gabarito", f"40 x 70 (110 no centro) x {(B.out_l - B.POST_UP) * 1000:.0f}", "40", "óleo", "espiga + 1 parafuso M8 por ponta", "Arco Zion flecha " + f"{B.rise_top * 1000:.0f} · R ≈ {((B.in_l / 2) ** 2 + B.rise_top ** 2) / (2 * B.rise_top) * 1000:.0f} mm; rasgo 30 x 14 inferior"),
            ("F02", "Travessa reta do dossel", 2, "freijó maciço", f"40 x 70 x {(B.out_w + B.POST_UP) * 1000:.0f}", "40", "óleo", "espiga + 1 parafuso M8 por ponta", "rasgo 30 x 14"),
            ("F03", "Trilho embutido", 4, "alumínio anodizado 20 x 8", "conforme travessa", "", "", "16 deslizadores nylon + 2 batentes por travessa", ""),
            ("H01", "Kit de ferragens", 1, "parafusos de cama M10 (8 + 4), porcas-tambor (12), M8 (8), Minifix (8), sapatas latão (7), anéis latão (4), tampões nogueira (8)", "", "", "latão envelhecido / inox", "", "saco identificado por grupo A a F"),
            ("H02", "Logo gravado", 1, "gravação a fogo 12 mm", "", "", "", "", "face interna da travessa da cabeceira")]
    return rows

# ------------------------------------------------------------------ documento
pages = []
def page(body, label, code="", cls=""):
    n = len(pages) + 1
    pages.append(f'<section class="page {cls}"><div class="head"><span>{zion_mark_html("14px", color="#1B2117")} ZION CANOPY BED · {CODE} · {DOC} · {REV}</span><span>{esc(code or DOC)}</span><span>{esc(label)}</span></div>{body}<div class="foot"><span>ZION NEW LUXURY FURNITURE COLLECTION · PEÇA HERO · SEM PREÇOS</span><span>UNIDADE: mm</span><span>{DATE} · {n:02d}</span></div></section>')
def sheet_page(fname, code, title, note="1:10"):
    n = len(pages) + 1
    pages.append(f'<section class="page sheetpage"><div class="strip"><span class="code">{esc(code)}</span><span class="ttl">{esc(title)}</span><span class="scl">{esc(note)}</span><span class="prod">ZION CANOPY BED</span></div><div class="sheet">{svg_inline(f"08_MOBILIARIO/cama/{fname}")}</div><div class="foot"><span>{DOC} · {REV} · {esc(code)}</span><span>{esc(title)}</span><span>{DATE} · {n:02d}</span></div></section>')

def build_doc():
    R_top = ((B.in_l / 2) ** 2 + B.rise_top ** 2) / (2 * B.rise_top) * 1000; R_head = ((B.in_w / 2) ** 2 + B.rise_head ** 2) / (2 * B.rise_head) * 1000
    pages.append(f'''<section class="page cover"><div class="coverbox"><div class="brand">{zion_mark_html("13mm", color="#FEF5F0", style="margin-right:6mm")}{zion_logo_html("13mm", color="#FEF5F0")}</div><div class="sub">ZION NEW LUXURY FURNITURE COLLECTION · PEÇA HERO · {CODE}</div>
<h1>ZION<br>CANOPY BED</h1><h3>{DOC} · {REV} · {DATE} · DESCANSO + ROMANCE</h3>
<p class="lead">A cama é o coração da Bubble e a imagem mais fotografada da Zion. A Zion Canopy Bed evolui o dossel de madeira que já existe em Urubici e Florianópolis para uma peça de arquitetura: quatro colunas finas de freijó sobre pés com anel de latão, um quadro de dossel com o Arco Zion nas laterais e o trilho da cortina escondido dentro dele, uma cabeceira de linho e palhinha coroada por um arco com luz indireta, e o véu de linho lavado que fecha o quarto dentro do quarto. Desmonta em seis grupos, viaja em dois volumes e monta em 45 minutos.</p>
<p class="rule">Conceito para protótipo. Dimensões em mm; itens marcados {PROV} e {WARN} aguardam o protótipo e a validação de ergonomia e resistência (norma NBR 15413 para camas). Sem preços: custo estimado em interno/ZG-FFE-002_Custo_Estimado.md. Usa o Zion Furniture Design System ZG-FFE-001.</p></div></section>''')
    # 01 conceito · 02 story
    body = h("01 · CONCEITO · 02 · STORY DA PEÇA", "o ícone da Zion: um quarto dentro do quarto")
    body += f'<div class="two"><div><p class="quote">Na Bubble, o hóspede dorme sob o céu. A Canopy Bed dá a ele o que a Bubble não dá: um limite macio, uma sombra, um véu. É a cama que aparece em todas as fotos, a que o casal fecha à noite e abre de manhã para ver a araucária ou a palmeira. Descanso e romance no mesmo gesto.</p>'
    body += ul(["<b>Arquitetura, não decoração:</b> quatro colunas e um quadro com o Arco Zion, a mesma curva das cabanas e da cúpula da Bubble.", "<b>O véu nasce da estrutura:</b> trilho escondido no quadro, cortinas de linho com abas; nada de varão, argola ou ilhós.", "<b>Luz que não se vê:</b> uma fita LED atrás do arco da cabeceira ilumina o véu e o teto; a cama vira uma lanterna.", "<b>Cabeceira em duas texturas:</b> linho estofado onde as costas encostam, palhinha onde a luz passa.", "<b>Pés com anel de latão:</b> o encontro pé 70 / coluna 60 é assinado por um anel de latão; sapatas com nivelador para o piso da Bubble e do deck.", "<b>Feita para hotelaria:</b> capas e cortinas removíveis, costas limpas, seis grupos que desmontam com uma chave, 45 minutos."])
    body += f'</div><div><h4>O QUE O HÓSPEDE SENTE</h4>{kv([("Chegada", "vê a cama da porta: colunas finas, véu aberto, luz âmbar no arco"), ("Noite", "fecha o véu: o quarto encolhe para 1,60 x 2,00 m; a luz do arco a 10 %"), ("Manhã", "abre o véu de um lado e vê a mata; o outro lado ainda protege"), ("Toque", "freijó a óleo nas colunas, linho nas mãos, palhinha no olhar")])}<h4>OS CINCO GESTOS DA ASSINATURA</h4>{table(["Gesto", "Onde está na cama"], [("Arco Zion", f"laterais do quadro do dossel (vão {B.in_l * 1000:.0f}, flecha {B.rise_top * 1000:.0f}) e topo da cabeceira (vão {B.in_w * 1000:.0f}, flecha {B.rise_head * 1000:.0f})"), ("Pé Zion", "pés 70 x 70 com sapata de latão e nivelador; colunas 60 x 60 com anel de latão"), ("Amarração", "opcional Icon: corda cru nas quatro espigas do quadro do dossel"), ("Friso", "rebaixo 4 x 4 nas quatro travessas da base, a 1/3 da altura"), ("Véu", "8 painéis de linho em trilho oculto")], "small")}</div></div>'
    page(body, "Conceito e story", code=f"{DOC}-01")
    # 03 referências · 04 sketch (conceitos)
    body = h("03 · REFERÊNCIAS · 04 · SKETCH · 07 · TRÊS CONCEITOS · 08 · COMPARAÇÃO · 09 · SELEÇÃO", "da cama atual das Bubbles aos três conceitos e à escolha")
    figs = "".join("<figure>" + img("08_MOBILIARIO/referencias/" + f + ".jpg") + "<figcaption>" + esc(c) + "</figcaption></figure>" for f, c in (("Bubbles_Urubici8", "Cama dossel atual: pinus envernizado, travessas retas, cortinas de aba. Ponto de partida."), ("Bubbles_Urubici5", "O quadro do dossel contra a cúpula: a cama é a arquitetura da Bubble.")))
    body += f'<div class="two"><div><div class="refs" style="grid-template-columns:1fr 1fr">{figs}</div><h4>O QUE MANTER · O QUE EVOLUIR</h4>{table(["Manter", "Evoluir"], [("4 colunas e quadro superior", "seções finas (60 mm) e Arco nas laterais"), ("cortinas de aba", "linho lavado, trilho oculto, 8 painéis"), ("madeira quente", "freijó a óleo em vez de pinus envernizado"), ("cabeceira de madeira", "linho + palhinha + arco com LED"), ("altura de dormir confortável", f"colchão a {B.mat_top * 1000:.0f} mm; total {B.H_TOTAL * 1000:.0f} mm")], "small")}</div>'
    body += '<div><h4>COMPARAÇÃO DOS TRÊS CONCEITOS (10 PERGUNTAS · 0 a 3)</h4>' + table(["Pergunta", "A · Arco", "B · Portal", "C · Ninho"], [("Parece Zion?", 3, 2, 3), ("Parece luxo?", 3, 3, 2), ("Parece natural?", 3, 2, 3), ("Parece confortável?", 3, 3, 2), ("É atemporal?", 3, 3, 1), ("É fotografável?", 3, 2, 3), ("Pode ser fabricada?", 3, 2, 1), ("Pode ser replicada (50 a 500)?", 3, 2, 1), ("É adequada para hotelaria (limpeza, capas)?", 3, 3, 1), ("Melhora a experiência do hóspede?", 3, 2, 3), ("<b>Total</b>", "<b>30</b>", "<b>24</b>", "<b>20</b>")], "small")
    body += '<p class="lede"><b>Seleção: A · ARCO</b>, incorporando de C a faixa de palhinha na cabeceira e a opção de Amarração nas espigas (versão Icon), e de B a ideia do teto de linho como acessório opcional (véu de teto para a Bubble no verão).</p></div></div>'
    page(body, "Referências e conceitos", code=f"{DOC}-03")
    sheet_page("FB-08_conceitos.svg", "FB-08", "Três conceitos: A Arco (selecionado) · B Portal · C Ninho", "s/ escala")
    # 05 render (iso)
    sheet_page("FB-05_isometrica.svg", "FB-05", "05 · Render de estudo · vista isométrica", "s/ escala")
    # 06 dimensões · 07 materiais · 08 acabamentos
    body = h("06 · DIMENSÕES · 07 · MATERIAIS · 08 · ACABAMENTOS", "colchão queen 1.580 x 1.980 · proporção da Bubble · circulação · limpeza · transporte")
    dims = [("Colchão", f"{B.MAT_W * 1000:.0f} x {B.MAT_L * 1000:.0f} x {B.MAT_H * 1000:.0f} (queen brasileiro)"), ("Vão interno", f"{B.in_w * 1000:.0f} x {B.in_l * 1000:.0f} (folga 10 mm por lado)"), ("Externo (postes)", f"{B.out_w * 1000:.0f} x {B.out_l * 1000:.0f}"), ("Altura total", f"{B.H_TOTAL * 1000:.0f} no topo do arco · {B.post_top * 1000:.0f} no topo das colunas"), ("Topo da travessa / do colchão", f"{B.RAIL_TOP * 1000:.0f} / {B.mat_top * 1000:.0f}"), ("Cabeceira", f"{B.HEAD_H * 1000:.0f} (arco), painel estofado {B.UPH_H * 1000:.0f} + palhinha"), ("Arco do dossel", f"vão {B.in_l * 1000:.0f} · flecha {B.rise_top * 1000:.0f} · R ≈ {R_top:.0f}"), ("Arco da cabeceira", f"vão {B.in_w * 1000:.0f} · flecha {B.rise_head * 1000:.0f} · R ≈ {R_head:.0f}"), ("Circulação mínima", "700 mm nas laterais e 900 nos pés " + PROV), ("Bubble Ø 4,0 / 5,0 m", "cama centrada ou encostada à cauda; altura livre da cúpula ≥ 2,60 m no eixo " + PROV), ("Maior peça", f"travessa arqueada {(B.out_l - B.POST_UP) * 1000:.0f} mm · coluna {(B.post_top - B.RAIL_TOP - 0.10) * 1000:.0f} mm"), ("Volumes de transporte", "2: base + cabeceira (2.050 x 1.750 x 250, ≈ 95 kg) · colunas + quadro + véu (2.150 x 400 x 250, ≈ 45 kg) " + PROV)]
    body += f'<div class="two"><div>{kv(dims)}</div><div><h4>MATERIAIS</h4>{table(["Elemento", "Material", "Acabamento"], [("Estrutura (pés, colunas, travessas, arcos)", "freijó maciço certificado ZW-01; arcos laminados em 5 lâminas", "ZW-01-O óleo natural (Essential / Signature) · ZW-01-V verniz PU fosco (opção)"), ("Ripas", "faia ou freijó laminado curvado", "natural"), ("Cabeceira estofada", "compensado + espuma D28 + manta + linho hotelaria", "ZT-02-SA areia (Urubici: ZT-04-CA couro caramelo opcional)"), ("Faixa de palhinha", "palhinha sextavada ZR-01", "ZR-01-N verniz água fosco"), ("Véu", "linho lavado 220 g/m²", "ZT-01-OW off-white (Urubici: areia 280 g/m²)"), ("Metais", "latão envelhecido: sapatas, anéis, ganchos, passa-cabo", "ZM-01-B"), ("Luz", "fita LED 24 V 2700 K IRC 90, difusor opalino", "dimmer no criado-mudo")], "small")}<h4>ESPECIFICAÇÃO EM UMA LINHA</h4><p class="lede"><b>{CODE} Zion Canopy Bed · ZW-01-O + ZT-01-OW + ZT-02-SA + ZR-01-N + ZM-01-B</b></p></div></div>'
    page(body, "Dimensões, materiais e acabamentos", code=f"{DOC}-06")
    # 09 desenho técnico
    sheet_page("FB-01_vista_frontal.svg", "FB-01", "09 · Desenho técnico · vista frontal", "1:10")
    sheet_page("FB-02_vista_lateral.svg", "FB-02", "09 · Desenho técnico · vista lateral", "1:10")
    sheet_page("FB-03_vista_superior.svg", "FB-03", "09 · Desenho técnico · vista superior", "1:8")
    sheet_page("FB-04_vista_posterior.svg", "FB-04", "09 · Desenho técnico · vista posterior", "1:10")
    sheet_page("FB-06_detalhes.svg", "FB-06", "09 · Detalhes de encaixe, fixação, trilho e estofamento", "1:2 · 1:4")
    sheet_page("FB-07_explodido.svg", "FB-07", "10 · Modelo explodido · grupos de montagem A a F", "s/ escala")
    # 11 BOM
    rows = bom_rows()
    body = h("11 · BILL OF MATERIALS", f"{len(rows)} linhas · grupos A base · B colchão · C cabeceira · D colunas · E véu · F dossel · H ferragens · dimensões em mm · onde há premissa, marcado")
    body += table(["Cód.", "Componente", "#Qtd", "Material", "Dimensão (mm)", "Esp.", "Acabamento", "Ferragem", "Observação"], [(c, f"<b>{esc(n)}</b>", q, esc(m), esc(d), esc(e), esc(a), esc(f), o) for c, n, q, m, d, e, a, f, o in rows], "xsmall")
    vol = (4 * 0.07 * 0.07 * (B.RAIL_TOP + 0.10) + 2 * 0.04 * 0.18 * B.in_l + 2 * 0.04 * 0.18 * (B.in_w + 0.08) + 0.04 * 0.08 * B.in_l + 3 * 0.06 * 0.06 * B.rail_z1 + B.SLAT_N * 0.02 * 0.07 * B.in_w + 4 * 0.06 * 0.06 * (B.post_top - B.RAIL_TOP - 0.10) + 2 * 0.04 * 0.09 * (B.out_l) + 2 * 0.04 * 0.07 * (B.out_w + 0.06) + 0.06 * 0.06 * (B.in_w + 2 * (B.HEAD_H - B.RAIL_TOP)))
    body += f'<h4>QUANTITATIVO</h4>{kv([("Madeira maciça (líquida)", f"≈ {vol * 1000:.0f} dm³ = {vol:.3f} m³ de freijó; comprar ≈ {vol * 1.6:.2f} m³ (rendimento 60 %)"), ("Linho do véu", f"8 painéis de 1,10 x 2,06 m = {8 * 1.1 * 2.06:.1f} m² (+ 10 % de barras e abas) ≈ {8 * 1.1 * 2.06 * 1.1:.0f} m²"), ("Linho do estofado", "≈ 1,6 m² + capa"), ("Palhinha", f"≈ {(B.in_w - 0.02) * (B.HEAD_H - B.rise_head - 0.28 - B.RAIL_TOP - B.UPH_H):.2f} m²"), ("LED", "1,4 m de fita + canaleta + fonte 30 W"), ("Ferragens", "12 parafusos de cama M10, 12 porcas-tambor, 8 M8, 8 Minifix, 7 sapatas + niveladores, 4 anéis de latão, 64 ganchos, 4 trilhos")])}<p class="note">{WARN}: seção das ripas e da longarina para carga de 2 pessoas (NBR 15413) e resistência do parafuso de cama nas colunas de 60 mm a ser confirmada em protótipo com ensaio de balanço. Peso total estimado 140 kg {PROV}.</p>'
    page(body, "BOM", code=f"{DOC}-11", cls="flow")
    # 12 fabricação · 13 montagem · 14 manutenção
    body = h("12 · FABRICAÇÃO · 13 · MONTAGEM · 14 · MANUTENÇÃO", "marcenaria parceira + estofaria + confecção de linho + serralheria de latão")
    body += f'<div class="two"><div><h4>FABRICAÇÃO</h4>{ol(["Madeira: freijó seco em estufa (10 a 12 %), peças aplainadas 24 h antes da usinagem; seleção de veio contínuo para as colunas.", "Pés e colunas: esquadrejar 70 / 60, R1 em todas as arestas (fresa R12), furação com gabarito para parafusos de cama e espiga; cônico opcional nas faces externas.", "Travessas: rebaixo interno 20 x 20 para as ripas, Friso 4 x 4 na tupia, porcas-tambor por gabarito.", "Arcos (dossel e cabeceira): 5 lâminas de 8 mm coladas em gabarito curvo (R ≈ " + f"{R_top:.0f}" + " / " + f"{R_head:.0f}" + " mm), usinagem final em CNC; rasgo 30 x 14 do trilho na fresadora.", "Cabeceira: quadro + painel estofado (estofaria: compensado, espuma D28, manta, linho com zíper) + quadro de palhinha (esticar úmida, secar 24 h) + tampo traseiro laminado.", "Latão: anéis Ø80 x 24 torneados, sapatas 15 mm com rosca M8, ganchos estampados; escovar e envelhecer (pátina) sem verniz.", "Acabamento: lixa 180 / 240, óleo natural 2 demãos (ou PU fosco 3 demãos); cura 72 h.", "Véu: linho lavado pré-encolhido, abas de 40 x 100 a cada 150 mm, barra dupla 60 mm; etiqueta com posição (L1 a L4, P1, P2, C1, C2).", "Pré-montagem completa em fábrica, foto, etiquetas nos grupos, embalagem em 2 volumes com cantoneiras de papelão e manta."])}</div>'
    body += f'<div><h4>MONTAGEM (2 PESSOAS · 45 MIN · CHAVE ALLEN 6 + CHAVE 13)</h4>{ol(["Posicionar os 4 pés e as 4 travessas da base; apertar os 8 parafusos de cama M10 (grupo A); nivelar pelas sapatas.", "Longarina central e 3 pés intermediários; encaixar as 16 ripas no rebaixo (1 parafuso central cada).", "Cabeceira: encaixar o quadro C nos postes da cabeceira (4 M8); ligar o cabo do LED ao passa-cabo; fonte e dimmer no criado.", "Colunas D: encaixar no anel de latão e apertar o parafuso vertical M10 x 200 por baixo do pé.", "Quadro do dossel F: enfiar os deslizadores nos trilhos (16 por travessa), espigas nas colunas, 1 M8 por ponta.", "Véu E: pendurar as abas nos ganchos (8 painéis); conferir o deslizar.", "Colchão B, enxoval, foto de conferência e registro do número de série gravado."])}<h4>MANUTENÇÃO</h4>{ul(["Semanal: pano úmido nas madeiras; aspirar a palhinha; passar o véu recolhido.", "Mensal: reapertar parafusos de cama (1/4 de volta), conferir niveladores e o deslizar do trilho (silicone seco).", "Trimestral: lavar o véu a 40 °C (2 jogos por unidade em rotação); capa da cabeceira a seco.", "Anual: reaplicar óleo nas colunas e travessas; revisar LED e fonte; trocar ganchos gastos.", "Substituição: qualquer grupo A a F troca sem desmontar os demais; peças de reposição codificadas."])}</div></div>'
    page(body, "Fabricação, montagem e manutenção", code=f"{DOC}-12")
    # 15 custo (remissão) · escala · regra de design · revisão
    body = h("15 · CUSTO ESTIMADO · 16 · ESCALA · 23 · REGRA DE DESIGN · REVISÃO", "custo separado do preço de venda · estimativa nunca é orçamento")
    body += f'<div class="two"><div><h4>CUSTO ESTIMADO</h4><p class="lede">O custo estimado (material, mão de obra, acabamento, ferragens, embalagem, transporte, montagem) e o preço de venda sugerido ficam no documento interno <b>interno/ZG-FFE-002_Custo_Estimado.md</b>, com a base de dados do FF&amp;I 2025 e os quantitativos desta BOM. Este documento circula sem preços: {WARN.replace("PREMISSA", "PREÇO A COTAR")}.</p><h4>ESCALA</h4>{table(["Unidades", "Como produzir"], [("1 (protótipo)", "marcenaria em Florianópolis ou Urubici; arcos em gabarito de MDF; validação de dimensões e ensaio de carga"), ("10", "1 marcenaria parceira; gabaritos fixos; latão em lote; véus em confecção parceira"), ("50", "peças CNC (pés, colunas, quadros), arcos laminados em fornecedor de curvados; estofaria própria; estoque de ferragens"), ("100", "linha dedicada; colunas torneadas em série; kit de ferragens embalado; 2 volumes padrão"), ("500", "industrialização: freijó maciço nas superfícies de toque, laminado nos arcos e cabeceira, fibra e linho certificados; peças de reposição em estoque")], "small")}</div>'
    body += '<div><h4>AS 10 PERGUNTAS · RESPOSTAS DO CONCEITO A</h4>' + table(["Pergunta", "Resposta", "Por quê"], [("Parece Zion?", "Sim", "dossel + madeira + véu, agora com o Arco"), ("Parece luxo?", "Sim", "freijó, latão, linho lavado, luz indireta, proporções finas"), ("Parece natural?", "Sim", "3 texturas naturais; nenhum brilho"), ("Parece confortável?", "Sim", "colchão a 600 mm, cabeceira macia, véu"), ("É atemporal?", "Sim", "um só motivo formal; sem tema"), ("É fotografável?", "Sim", "silhueta do arco, véu, luz"), ("Pode ser fabricada?", "Sim", "marcenaria + estofaria + confecção; arcos laminados"), ("Pode ser replicada?", "Sim", "6 grupos, gabaritos, ferragens de catálogo"), ("Hotelaria?", "Sim", "capas e véus removíveis, costas limpas, niveladores"), ("Melhora a experiência?", "Sim", "descanso + romance + privacidade na Bubble")], "small") + table(["Rev", "Data", "Descrição"], [("00", DATE, "Conceito da peça hero: 3 conceitos, seleção, FB-01 a FB-08, BOM, fabricação, montagem, manutenção")], "small") + "</div></div>"
    page(body, "Custo, escala e regra de design", code=f"{DOC}-15")
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · {DOC} · Zion Canopy Bed</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    path = os.path.join(OUT_DIR, f"{DOC}_Zion_Canopy_Bed.html"); open(path, "w", encoding="utf-8").write(doc); print(os.path.relpath(path, ROOT), len(pages), "páginas")

def build_interno():
    rows = bom_rows()
    md = ["# ZG-FFE-002 · ZION CANOPY BED · CUSTO ESTIMADO (INTERNO) · REV 00 · " + DATE, "", "**Uso interno.** Estimativa de ordem de grandeza para decisão; NÃO é orçamento. Toda linha deve ser cotada com a marcenaria, a estofaria, a confecção e o fornecedor de latão antes de qualquer proposta. Referência histórica: FF&I Zion Collection 2025 registrou a cama dossel de pinus a R$ 3.500 de custo e R$ 5.250 de venda (fator 1,5).", "",
          "## Quantitativos (da BOM)", "", "| Grupo | Item | Qtd | Unidade | Custo unitário | Custo estimado |", "|---|---|---|---|---|---|",
          "| A a F | Freijó maciço seco (líquido ≈ 0,16 m³; compra ≈ 0,26 m³ com 60 % de rendimento) | 0,26 | m³ | PREÇO A COTAR | PREÇO A COTAR |", "| F01 | Arcos laminados (2 travessas de 2,08 m + 1 arco da cabeceira) em gabarito | 3 | un | PREÇO A COTAR | PREÇO A COTAR |",
          "| A06 | Ripas curvadas 20 x 70 x 1.600 | 16 | un | PREÇO A COTAR | PREÇO A COTAR |", "| C02 | Estofado (compensado, espuma D28, manta, linho hotelaria 1,6 m², capa com zíper) | 1 | un | PREÇO A COTAR | PREÇO A COTAR |",
          "| C03 | Palhinha sextavada ≈ 0,9 m² esticada em quadro | 1 | un | PREÇO A COTAR | PREÇO A COTAR |", "| C05 | LED 24 V 2700 K 1,4 m + canaleta + difusor + fonte 30 W + dimmer | 1 | kit | PREÇO A COTAR | PREÇO A COTAR |",
          "| E01 | Véu: linho lavado 220 g/m² ≈ 20 m² + confecção de 8 painéis com abas | 8 | un | PREÇO A COTAR | PREÇO A COTAR |", "| F03 | Trilhos de alumínio 4 x ≈ 2 m + 64 deslizadores + 64 ganchos de latão | 1 | kit | PREÇO A COTAR | PREÇO A COTAR |",
          "| H01 | Latão: 4 anéis Ø80 x 24 torneados, 7 sapatas com nivelador, 8 tampões de nogueira, parafusos de cama e porcas-tambor | 1 | kit | PREÇO A COTAR | PREÇO A COTAR |", "| — | Mão de obra de marcenaria (usinagem, colagem dos arcos, acabamento a óleo, pré-montagem) | ≈ 40 | h | PREÇO A COTAR | PREÇO A COTAR |",
          "| — | Embalagem em 2 volumes + transporte até Urubici / Florianópolis | 1 | vb | PREÇO A COTAR | PREÇO A COTAR |", "| — | Montagem em campo (2 pessoas x 45 min) | 1,5 | h | PREÇO A COTAR | PREÇO A COTAR |", "",
          "## Ordem de grandeza (PREMISSA para decisão, a confirmar em cotação)", "", "- Custo estimado do protótipo (1 un): entre **4 e 6 vezes** o custo da cama de pinus de 2025 (R$ 3.500), pela madeira de lei, arcos laminados, latão, LED, palhinha e véu de linho: faixa de referência R$ 14.000 a R$ 21.000. PREMISSA.",
          "- Série de 10: redução de 20 a 30 % (gabaritos, latão em lote, linho em rolo). PREMISSA.", "- Série de 50 a 100: redução de 35 a 45 % sobre o protótipo (CNC, curvados em fornecedor, estofaria própria). PREMISSA.",
          "- Preço de venda sugerido (kit de mobiliário para franqueado / cliente): custo x 1,5 (fator histórico) a x 1,8 (peça Icon, numerada). Separar SEMPRE custo estimado de preço de venda.", "",
          "## O que precisa de cotação real antes de qualquer número sair daqui", "", "1. Freijó seco certificado (m³) em Florianópolis / Urubici.", "2. Marcenaria: hora de usinagem e colagem de arcos laminados.", "3. Confecção: 8 painéis de linho lavado com abas.", "4. Latão: anéis torneados e sapatas (serralheria de latão ou torneiro).", "5. LED e trilhos (fornecedor de iluminação).", "6. Estofaria: painel com capa.", ""]
    md += ["## BOM resumida", "", "| Cód. | Componente | Qtd | Material | Dimensão |", "|---|---|---|---|---|"] + [f"| {c} | {n} | {q} | {m} | {d} |" for c, n, q, m, d, *_ in rows]
    os.makedirs(os.path.join(ROOT, "interno"), exist_ok=True)
    open(os.path.join(ROOT, "interno", "ZG-FFE-002_Custo_Estimado.md"), "w", encoding="utf-8").write("\n".join(md))

def build():
    elev_front(); elev_side(); plan_top(); elev_rear(); iso_view(); details(); exploded(); concepts()
    build_doc(); build_interno()

if __name__ == "__main__":
    build()

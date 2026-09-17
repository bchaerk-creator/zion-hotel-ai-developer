# -*- coding: utf-8 -*-
"""ZC-INT · PROJETO DE INTERIORES DO ZION CASULO com marcenaria acoplada (mobiliário fixo integrado à concha e à parede do banho).
Pranchas SVG em cocoon/interiores/: IN-01 planta de layout de interiores cotada · IN-02 paginação de pisos e acabamentos ·
IN-03 elevações internas A (cabeceira) e B (lateral esquerda) · IN-04 elevações C (banho) e D (fachada interna) ·
IN-05 detalhes da marcenaria acoplada · IN-06 quadro de mobiliário e acabamentos.  Uso: python3 interiores_cocoon.py"""
import math, os
from geometry import Cocoon
from svgkit import *
from drawings_cocoon import draw_furniture, shell_plan_pts, arch_plan

C = Cocoon()
OUT = os.path.join(os.path.dirname(__file__), "..", "cocoon", "interiores"); os.makedirs(OUT, exist_ok=True)
LINEN = "#E9E1D2"; STONE = "#CFC9BE"; RIP = "#C9AA7D"; BRASS = "#B5945A"; OAK = "#D9C4A3"; HATCH_W = "wood"
DOC = "ZC-INT-001"

# ---------------------------------------------------------------------------- programa de marcenaria acoplada (MA) e mobiliário solto (MS)
MA = [
    dict(cod="MA-01", nome="Mini cozinha acoplada", x1=1.20, x2=3.20, y1=2.15, y2=2.80, h=0.90, amb="Estar", ffe="M18 · E13 · E14 · E15 · E16 · E17 · E02",
         desc="Gabinete de 2,00 m acoplado à curva da concha (fundo recortado conforme a seção), em 4 módulos de 0,60 / 0,60 / 0,40 / 0,40: geladeira 120 L sob bancada · forno elétrico compacto 45 L sob o cooktop de indução 2 bocas · cuba 0,40 x 0,35 com torneira gourmet sobre gaveteiro · bancada de preparo com air fryer em nicho e lixeira embutida; tampo em quartzito 30 mm; prateleira flutuante 2,00 x 0,25 a 1,45 m com fita LED e depurador slim 60 cm (filtro de carvão) sob a prateleira; cafeteira e chaleira sobre o tampo",
         mat="Carvalho natural (portas ripadas) · quartzito · latão escovado · inox"),
    dict(cod="MA-02", nome="Armário baixo / closet embutido", x1=3.40, x2=4.50, y1=2.20, y2=2.85, h=1.50, amb="Estar / suíte", ffe="M10 · E03",
         desc="Armário de 1,10 m com 2 portas ripadas, cabideiro 0,80 m, 3 prateleiras, gaveta e cofre; tampo em pedra com bandeja; tampo posterior inclinado acompanhando a concha",
         mat="Carvalho natural · ripado termotratado · quartzito"),
    dict(cod="MA-03", nome="Cabeceira acoplada com criados suspensos", x1=6.42, x2=6.60, y1=-1.55, y2=1.55, h=1.30, amb="Suíte", ffe="M02 · M03 · M16 · F01",
         desc="Painel curvo estofado em linho 2,60 x 1,30 m fixado à parede do banho, criados suspensos 0,60 x 0,50 a 0,15 m do piso (gaveta com toque), arandelas de leitura, USB e LED de retroiluminação; ripado termotratado da cabeceira até o forro (2,60 m)",
         mat="Estofado linho · madeira laminada · ripado termotratado · latão"),
    dict(cod="MA-04", nome="Bancada do banho", x1=6.75, x2=7.30, y1=-2.05, y2=-0.55, h=0.85, amb="Banho", ffe="M12 · M13 · B01",
         desc="Tampo em pedra 30 mm com cuba esculpida, saia 60 mm, gabinete ripado suspenso (base a 0,25 m) com 2 portas e nicho aberto; espelho Ø0,90 com LED perimetral e antiembaçante; nicho lateral em pedra",
         mat="Quartzito · ripado termotratado · latão escovado"),
    dict(cod="MA-05", nome="Prateleira e nicho da banheira", x1=7.90, x2=9.00, y1=0.42, y2=0.78, h=0.60, amb="Banho", ffe="B02",
         desc="Prateleira em pedra 1,10 x 0,36 m a 0,60 m, acoplada à curva da cauda sobre a banheira; nicho para velas e amenities; banqueta e bandeja",
         mat="Quartzito · madeira"),
    dict(cod="MA-06", nome="Divisória da bacia e painel ripado", x1=7.30, x2=7.35, y1=0.90, y2=1.85, h=1.20, amb="Banho", ffe="M16",
         desc="Painel ripado de 1,20 m que separa a bacia da circulação, com nicho de papel e apoio; painel ripado contínuo na face do banho da parede divisória",
         mat="Ripado termotratado sobre placa cimentícia"),
    dict(cod="MA-07", nome="Rodapé técnico removível", x1=0.90, x2=9.40, y1=0, y2=0, h=0.15, amb="Todos", ffe="—",
         desc="Rodapé de 150 mm em ripado ao longo de toda a concha, removível (fixação por clipes) para acesso a eletrodutos, PEX e caixas de passagem; admissão da câmara ventilada",
         mat="Ripado termotratado · clipes inox"),
    dict(cod="MA-08", nome="Tampa do ático técnico", x1=7.0, x2=7.6, y1=-0.3, y2=0.3, h=0.0, amb="Banho (forro)", ffe="E11",
         desc="Alçapão 0,60 x 0,60 no forro do banho (2,40 m) com escada retrátil: acesso a QDC, evaporadora e boiler",
         mat="Compensado naval + ripado"),
]
MS = [
    dict(cod="MS-01", nome="Cama king box", dims="1,93 x 2,03 x 0,55", amb="Suíte", ffe="M01 · O01", pos="pés para a fachada, cabeceira em MA-03"),
    dict(cod="MS-02", nome="Banco aos pés da cama", dims="1,40 x 0,40 x 0,45", amb="Suíte", ffe="M11", pos="x 4,05"),
    dict(cod="MS-03", nome="Chaise de contemplação", dims="1,60 x 0,80 x 0,45", amb="Estar", ffe="M06", pos="junto à fachada de vidro, lado direito"),
    dict(cod="MS-04", nome="Poltrona de leitura", dims="0,70 x 0,70 x 0,75", amb="Estar", ffe="M07", pos="sob o Olho do estar (dir.)"),
    dict(cod="MS-05", nome="Mesa lateral", dims="Ø0,56 x 0,45", amb="Estar", ffe="M08", pos="entre a chaise e a poltrona"),
    dict(cod="MS-06", nome="Luminária de piso · de mesa", dims="—", amb="Estar", ffe="F02 · F03", pos="ao lado da poltrona · sobre MA-02"),
    dict(cod="MS-07", nome="Tapetes de lã", dims="2,00 x 3,00 · 1,60 x 2,30", amb="Estar · suíte", ffe="F04 · F05", pos="sob a chaise/poltrona · sob a cama"),
    dict(cod="MS-08", nome="Lareira ecológica", dims="0,60 x 0,30 x 0,35", amb="Estar", ffe="E08", pos="sobre MA-02 (opcional)"),
    dict(cod="MS-09", nome="Banqueta e bandeja da banheira", dims="0,45 x 0,30 x 0,45", amb="Banho", ffe="B02", pos="ao lado da banheira"),
]
ACAB = [("Vestíbulo", "cumaru 20 x 140 (deck)", "—", "membrana / vidro", "membrana", "—"),
        ("Estar", "carvalho de engenharia 14 mm, réguas no sentido x", "ripado técnico 150 mm", "forro tensionado Trevira CS creme · ripado junto ao piso · frontão em quartzito atrás do cooktop", "tensionado creme, Espinha de Luz", "MA-01 mini cozinha · MA-02"),
        ("Suíte", "carvalho de engenharia 14 mm", "ripado técnico 150 mm", "ripado termotratado na cabeceira", "tensionado creme", "MA-03"),
        ("Banho", "porcelanato 60 x 120 antiderrapante, paginação longitudinal", "porcelanato h 10 cm", "porcelanato na zona molhada · ripado nas demais", "forro naval pintado, 2,40 m", "MA-04 a MA-06"),
        ("Deck", "cumaru 20 x 140, réguas ⟂ à fachada", "—", "—", "—", "—")]

# ---------------------------------------------------------------------------- helpers
def hatch_rect(sh, x1, y1, x2, y2, sw=0.9):
    sh.rect(x1, y1, x2, y2, fill=sh.pattern("wood"), stroke=GREEN, sw=sw)

def tag(sh, x, y, code, size=8.5):
    X, Y = sh.X(x), sh.Y(y)
    sh.add(f'<rect x="{X - 19}" y="{Y - 7}" width="38" height="13" rx="2" fill="{CREAM}" stroke="{GREEN}" stroke-width="0.7"/>')
    sh.text_px(X, Y + 3.5, code, size=size, weight=700, spacing=0.05)

def _inner_yz(x, n=80):
    """seção interna (forro) em x: lista de (y, z) para y > 0."""
    a, b = C.a(x) - 0.16, C.b(x) - 0.16; t0, t1 = C.theta_range(x); out = []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n; y, z = a * math.cos(t), C.ZC + b * math.sin(t)
        if y >= 0 and z >= 0: out.append((y, z))
    return sorted(out, key=lambda p: p[1])

def shell_section_yz(x, n=80):
    """contorno interno (y, z) da concha em x, do piso à esquerda ao piso à direita, com 0,15 m de envelope."""
    pts = [(y, z) for (y, z) in C.section_local(x, n)]
    inner = []
    a, b = C.a(x) - 0.16, C.b(x) - 0.16
    t0, t1 = C.theta_range(x)
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        y, z = a * math.cos(t), C.ZC + b * math.sin(t)
        if z >= -0.01: inner.append((y, max(z, 0.0)))
    return inner

# ============================================================================ IN-01 planta de layout de interiores
def in01():
    sh = Sheet(1600, 1000, scale=80, ox=140, oy=470)
    sh.header("Zion Casulo · Planta de layout de interiores", "Marcenaria acoplada (MA) e mobiliário solto (MS) · cotas de mobiliário e circulação · 1:50")
    outline, ring = shell_plan_pts()
    D = C.DECK
    sh.rect(D["x1"] + 3.0, D["y1"], D["x2"], D["y2"], fill=sh.pattern("deck"), stroke=GREEN, sw=1.0)
    sh.poly(outline, fill=MEMB, stroke=GREEN, sw=1.6)
    floor = C.floor_outline(100); sh.poly(floor, fill="#FBF8F2", stroke=GREEN, sw=0.9)
    bath = [(x, y) for (x, y) in floor if x >= 6.6]; sh.poly(bath, fill=sh.pattern("tile"), stroke="none")
    for x in C.ARCH_X: sh.poly(arch_plan(x), close=False, stroke=EARTH, sw=0.5, dash="5 4", opacity=0.6)
    gr = [(x, y) for (x, y, z) in C.glass_ring(60)]; sh.poly(gr, close=False, stroke=GLASS, sw=6, opacity=0.9); sh.poly(gr, close=False, stroke=GREEN, sw=1.0)
    for w in C.WINDOWS:
        side = -1 if w["tc"] < math.pi / 2 else 1; xs = [w["xc"] - w["lx"], w["xc"] + w["lx"]]
        pts = [(C.shear(x, 1.6), side * (C.a(x) + 0.02)) for x in [xs[0] + (xs[1] - xs[0]) * i / 10 for i in range(11)]]
        sh.poly(pts, close=False, stroke=GLASS, sw=5); sh.poly(pts, close=False, stroke=GREEN, sw=0.8)
    # porta pivotante
    sh.line(0.9, 0.6, 1.9, 0.6, GREEN, 1.2); sh.add(f'<path d="M{sh.X(1.9):.1f},{sh.Y(0.6):.1f} A{sh.s:.1f},{sh.s:.1f} 0 0 0 {sh.X(0.9):.1f},{sh.Y(1.6):.1f}" fill="none" stroke="{GREEN}" stroke-width="0.6" stroke-dasharray="3 3"/>')
    # parede do banho e porta de correr
    sh.rect(6.6, -2.85, 6.7, 0.95, fill=GREEN, stroke=GREEN, sw=0.5); sh.rect(6.6, 1.85, 6.7, 2.85, fill=GREEN, stroke=GREEN, sw=0.5)
    sh.line(6.65, 0.95, 6.65, 1.85, GREEN, 0.6, dash="4 3"); sh.rect(6.72, 0.1, 6.78, 0.98, fill="none", stroke=GREEN, sw=0.8)
    # rodapé técnico (linha interna)
    inner = [(x, y * 0.965) for (x, y) in floor]; sh.poly(inner, fill="none", stroke=EARTH, sw=0.5, dash="2 2")
    # mobiliário solto
    draw_furniture(sh, [f for f in C.furniture() if f["kind"] not in ("cabinet", "vanity", "wall", "opening", "table") or f.get("r")], True)
    sh.rect(4.05, -0.7, 4.45, 0.7, fill=SAND, stroke=GREEN, sw=0.8)   # banco aos pés
    # marcenaria acoplada (hachura madeira)
    for m in MA:
        if m["cod"] in ("MA-07", "MA-08"): continue
        hatch_rect(sh, m["x1"], m["y1"], m["x2"], m["y2"])
    sh.rect(5.95, 1.05, 6.42, 1.55, fill=sh.pattern("wood"), stroke=GREEN, sw=0.8); sh.rect(5.95, -1.55, 6.42, -1.05, fill=sh.pattern("wood"), stroke=GREEN, sw=0.8)   # criados suspensos
    # mini cozinha MA-01: geladeira | forno + cooktop | cuba | preparo + air fryer
    sh.rect(1.25, 2.2, 1.75, 2.75, fill="none", stroke=GREEN, sw=0.5, dash="2 2"); sh.text(1.5, 2.47, "GELAD.", 6.5, GREEN, dy=2)
    sh.rect(1.85, 2.3, 2.35, 2.72, fill="#FFFFFF", stroke=GREEN, sw=0.6); sh.circle(1.98, 2.51, 0.09, fill="none", stroke=GREEN, sw=0.6); sh.circle(2.22, 2.51, 0.11, fill="none", stroke=GREEN, sw=0.6); sh.text(2.1, 2.2, "cooktop / forno", 5.5, GREEN)
    sh.rect(2.42, 2.3, 2.78, 2.65, fill="#FFFFFF", stroke=GREEN, sw=0.7); sh.text(2.6, 2.47, "cuba", 5.5, GREEN, dy=2)
    sh.rect(2.85, 2.3, 3.15, 2.7, fill="none", stroke=GREEN, sw=0.5, dash="2 2"); sh.text(3.0, 2.47, "AIR FR.", 5.5, GREEN, dy=2)
    sh.circle(7.02, -1.3, 0.19, fill="#FFFFFF", stroke=GREEN, sw=0.8)   # cuba esculpida
    sh.rect(7.0, -0.3, 7.6, 0.3, fill="none", stroke=GREEN, sw=0.6, dash="3 2"); sh.text(7.3, 0.0, "MA-08", 6.5, GREEN, dy=2)
    sh.line(7.65, -1.75, 7.65, -0.8, GLASS, 4); sh.line(7.65, -1.75, 7.65, -0.8, GREEN, 0.8)
    # etiquetas
    for m, (tx, ty) in zip([m for m in MA if m["cod"] not in ("MA-07", "MA-08")], [(2.2, 1.85), (3.95, 1.85), (6.9, 2.15), (6.4, -2.5), (8.9, 1.25), (7.9, 2.2)]):
        tag(sh, tx, ty, m["cod"])
    for code, (tx, ty) in (("MS-01", (5.5, 0.0)), ("MS-02", (4.25, -1.0)), ("MS-03", (1.95, -2.55)), ("MS-04", (3.55, -2.55)), ("MS-05", (1.95, -0.55)), ("MS-09", (8.5, -0.9))):
        tag(sh, tx, ty, code)
    # circulações (setas e larguras)
    for (x1, x2, y, lab) in ((1.0, 4.4, 0.55, "circulação 1,05"), (4.5, 6.4, 1.6, "passagem 0,60"), (4.5, 6.4, -1.6, "passagem 0,60")):
        sh.line(x1, y, x2, y, EARTH, 0.7, dash="6 3"); sh.text((x1 + x2) / 2, y + 0.12, lab, 7.5, EARTH)
    # cotas do mobiliário
    sh.dim(1.2, 3.0, 3.2, 3.0, 0.3, label="2,00 · MA-01", size=9); sh.dim(3.4, 3.0, 4.5, 3.0, 0.3, label="1,10 · MA-02", size=9); sh.dim(3.2, 3.0, 3.4, 3.0, 0.3, label="0,20", size=9)
    sh.dim(4.5, -3.3, 6.55, -3.3, -0.3, label="2,05 · cama", size=9); sh.dim(6.75, -2.05, 6.75, -0.55, 3.35, label="1,50 · MA-04", size=9)
    sh.dim(7.55, -3.3, 9.15, -3.3, -0.3, label="1,60 · banheira", size=9); sh.dim(1.15, -3.3, 2.75, -3.3, -0.3, label="1,60 · chaise", size=9)
    sh.dim(0.9, 3.4, 6.6, 3.4, 0.7, label="5,70 · estar + suíte"); sh.dim(6.6, 3.4, 9.4, 3.4, 0.7, label="2,80 · banho")
    sh.dim(10.9, -2.93, 10.9, 2.93, 0.5, label="5,86 · largura útil"); sh.dim(-0.2, 0.6, -0.2, 1.6, -0.4, label="1,00 · PV1", size=9)
    # rótulos de ambiente
    for t, x, y, a in (("ESTAR", 2.8, 0.2, "20,4 m²"), ("SUÍTE", 5.4, 0.55, "12,0 m²"), ("BANHO", 8.6, 1.6, "13,2 m²")):
        sh.text(x, y, t, 11, GREEN, weight=700, spacing=0.22, dy=-4); sh.text(x, y, a, 9, EARTH, dy=9)
    # legenda
    X0, Y0 = 1080, 120
    sh.text_px(X0, Y0, "LEGENDA", size=10, weight=700, spacing=0.25, anchor="start")
    sh.add(f'<rect x="{X0}" y="{Y0 + 12}" width="26" height="12" fill="{sh.pattern("wood")}" stroke="{GREEN}" stroke-width="0.7"/>'); sh.text_px(X0 + 34, Y0 + 22, "MA · marcenaria acoplada (fixa, fabricada com a cabana)", size=9, anchor="start")
    sh.add(f'<rect x="{X0}" y="{Y0 + 30}" width="26" height="12" fill="{SAND}" stroke="{GREEN}" stroke-width="0.7"/>'); sh.text_px(X0 + 34, Y0 + 40, "MS · mobiliário solto (FF&E, entregue montado)", size=9, anchor="start")
    sh.add(f'<line x1="{X0}" y1="{Y0 + 54}" x2="{X0 + 26}" y2="{Y0 + 54}" stroke="{EARTH}" stroke-width="0.6" stroke-dasharray="2 2"/>'); sh.text_px(X0 + 34, Y0 + 58, "MA-07 · rodapé técnico removível 150 mm", size=9, anchor="start")
    yy = Y0 + 84
    sh.text_px(X0, yy, "MARCENARIA ACOPLADA", size=10, weight=700, spacing=0.25, anchor="start"); yy += 16
    for m in MA:
        sh.text_px(X0, yy, m["cod"], size=8.5, weight=700, anchor="start"); sh.text_px(X0 + 46, yy, f"{m['nome']} · {m['amb']}", size=8.5, anchor="start"); yy += 13
    yy += 8; sh.text_px(X0, yy, "MOBILIÁRIO SOLTO", size=10, weight=700, spacing=0.25, anchor="start"); yy += 16
    for m in MS:
        sh.text_px(X0, yy, m["cod"], size=8.5, weight=700, anchor="start"); sh.text_px(X0 + 46, yy, f"{m['nome']} · {m['dims']}", size=8.5, anchor="start"); yy += 13
    sh.north(1500, 130, angle=-90); sh.scalebar(0.9, -4.6, 5)
    sh.title_block("ZION CASULO", "Planta de layout de interiores", "1:50 (A1) · cotas em metros", "IN-01", "Marcenaria acoplada MA-01 a MA-08 · mobiliário solto MS-01 a MS-09")
    sh.save(os.path.join(OUT, "IN-01_planta_interiores.svg"))

# ============================================================================ IN-02 paginação de pisos e acabamentos
def in02():
    sh = Sheet(1600, 1000, scale=80, ox=140, oy=470)
    sh.header("Zion Casulo · Paginação de pisos e quadro de acabamentos", "Sentido das réguas, transições, soleiras, ralo linear, tapetes · 1:50")
    outline, ring = shell_plan_pts(); D = C.DECK
    # deck: réguas perpendiculares à fachada (linhas em y)
    sh.rect(D["x1"] + 3.0, D["y1"], D["x2"], D["y2"], fill="#E6D3B3", stroke=GREEN, sw=1.0)
    y = D["y1"]
    while y < D["y2"]: sh.line(D["x1"] + 3.0, y, D["x2"], y, EARTH, 0.4); y += 0.14
    sh.poly(outline, fill="none", stroke=GREEN, sw=1.6)
    floor = C.floor_outline(100)
    living = [(x, yv) for (x, yv) in floor if x <= 6.62]; sh.poly(living, fill=OAK, stroke=GREEN, sw=0.9)
    # réguas de carvalho no sentido x (linhas em y constantes, recortadas)
    for yv in [i * 0.19 - 2.85 for i in range(31)]:
        xs = [x for (x, _) in living if abs(_) >= abs(yv)] or [0.9]
        x0 = 0.9; x1 = max([x for (x, yy2) in floor if x <= 6.6 and abs(yy2) >= abs(yv)] + [0.9])
        if x1 > x0 + 0.2: sh.line(x0, yv, x1, yv, "#B99A73", 0.45)
    bath = [(x, yv) for (x, yv) in floor if x >= 6.6]; sh.poly(bath, fill=TILE, stroke=GREEN, sw=0.9)
    for xv in [6.7 + i * 1.2 for i in range(3)]: sh.line(xv, -C.floor_hw(xv), xv, C.floor_hw(xv), "#B9B7AE", 0.6)
    for yv in [-2.4 + i * 0.6 for i in range(9)]:
        x1 = max([x for (x, yy2) in floor if x >= 6.6 and abs(yy2) >= abs(yv)] + [6.6])
        if x1 > 6.7: sh.line(6.6, yv, x1, yv, "#B9B7AE", 0.6)
    sh.rect(6.6, -2.85, 6.7, 0.95, fill=GREEN, stroke="none"); sh.rect(6.6, 1.85, 6.7, 2.85, fill=GREEN, stroke="none")
    # tapetes, ralo, soleiras
    sh.rect(1.0, -2.3, 4.0, -0.3, fill="none", stroke=EARTH, sw=0.8, dash="6 3"); sh.text(2.5, -1.3, "F04 · tapete 2,00 x 3,00", 8, EARTH)
    sh.rect(4.3, -1.3, 6.4, 1.3, fill="none", stroke=EARTH, sw=0.8, dash="6 3"); sh.text(5.35, -1.15, "F05 · tapete 1,60 x 2,30", 8, EARTH)
    sh.rect(7.65, -1.75, 8.6, -0.8, fill="none", stroke=GREEN, sw=0.8); sh.line(8.55, -1.75, 8.55, -0.8, STEEL, 2.2); sh.text(8.1, -1.28, "ralo linear", 7.5, GREEN)
    sh.line(0.9, -2.7, 0.9, 2.7, BRASS, 3); sh.text(1.05, -2.95, "soleira latão · deck → carvalho", 8, EARTH, anchor="start")
    sh.line(6.65, 0.95, 6.65, 1.85, BRASS, 3); sh.text(6.9, 2.6, "soleira latão · carvalho → porcelanato (nível -1 cm)", 8, EARTH, anchor="start")
    for t, x, yv in (("DECK · cumaru 20 x 140 ⟂ fachada", -0.2, 2.6), ("ESTAR + SUÍTE · carvalho de engenharia 14 mm, réguas no sentido longitudinal", 3.6, -3.25), ("BANHO · porcelanato 60 x 120 antiderrapante, paginação longitudinal, junta 2 mm", 8.2, -3.25)):
        sh.text(x, yv, t, 9, GREEN, weight=600, spacing=0.06)
    sh.dim(0.9, 3.4, 6.6, 3.4, 0.45, label="5,70"); sh.dim(6.6, 3.4, 9.4, 3.4, 0.45, label="2,80")
    # quadro de acabamentos
    X0, Y0 = 1010, 110; cols = [0, 62, 220, 320, 470, 600]
    sh.text_px(X0, Y0, "QUADRO DE ACABAMENTOS", size=10, weight=700, spacing=0.25, anchor="start")
    heads = ["Ambiente", "Piso", "Rodapé", "Paredes", "Forro", "Marcenaria"]
    for h_, cx in zip(heads, cols): sh.text_px(X0 + cx, Y0 + 20, h_.upper(), size=7.5, fill=EARTH, spacing=0.15, anchor="start")
    sh.add(f'<line x1="{X0}" y1="{Y0 + 26}" x2="{X0 + 540}" y2="{Y0 + 26}" stroke="{GREEN}" stroke-width="0.6"/>')
    yy = Y0 + 42
    def wrap(t, n):
        w = t.split(); out = []; cur = ""
        for x in w:
            if len(cur) + len(x) + 1 > n: out.append(cur); cur = x
            else: cur = (cur + " " + x).strip()
        return out + [cur]
    for row in ACAB:
        lines = 1
        for c, cx, n in zip(row, cols, (12, 32, 20, 28, 26, 16)):
            ls = wrap(c, n)
            for k, l in enumerate(ls): sh.text_px(X0 + cx, yy + k * 11, l, size=8, anchor="start", weight=600 if cx == 0 else 400)
            lines = max(lines, len(ls))
        yy += 11 * lines + 8
        sh.add(f'<line x1="{X0}" y1="{yy - 6}" x2="{X0 + 540}" y2="{yy - 6}" stroke="{SAND}" stroke-width="0.6"/>')
    yy += 10; sh.text_px(X0, yy, "NOTAS", size=10, weight=700, spacing=0.25, anchor="start"); yy += 16
    for n in ["Carvalho flutuante sobre manta; junta de dilatação de 10 mm sob o rodapé técnico.", "Porcelanato assentado com AC-III e rejunte epóxi sobre impermeabilização; caimento 1 % para o ralo linear.", "Soleiras em latão escovado 40 x 8 mm; degrau de 1 cm entre carvalho e porcelanato.", "Deck com clips ocultos inox e junta de 6 mm; óleo protetor.", "Cores: piso carvalho natural fosco · porcelanato areia clara · rodapé ripado no tom do carvalho."]:
        for l in wrap(n, 78): sh.text_px(X0, yy, l, size=8, anchor="start"); yy += 11
        yy += 3
    sh.north(940, 130, angle=-90); sh.scalebar(0.9, -4.6, 5)
    sh.title_block("ZION CASULO", "Paginação de pisos e acabamentos", "1:50 (A1) · cotas em metros", "IN-02", "Quadro de acabamentos por ambiente")
    sh.save(os.path.join(OUT, "IN-02_pisos_acabamentos.svg"))

# ============================================================================ elevações internas
def _ceiling_line(sh, x0, x1, n=40, drop=0.22):
    pts = [(x0 + (x1 - x0) * i / n, C.top(x0 + (x1 - x0) * i / n) - drop) for i in range(n + 1)]
    return pts

def elev_A(sh):
    """parede da cabeceira (x = 6,60) vista do estar, olhar +x; eixo u = y (esquerda -y ... direita +y)."""
    sec = shell_section_yz(6.55)
    sh.poly(sec, fill="#F6F1E8", stroke=GREEN, sw=1.4)
    sh.rect(-2.8, 0, 2.8, 2.6, fill=RIP, stroke=GREEN, sw=0.8)               # parede do banho com ripado
    for yv in [ -2.8 + i * 0.06 for i in range(94)]: sh.line(yv, 0.15, yv, 2.6, "#A8865E", 0.35)
    sh.rect(-2.8, 0, 2.8, 0.15, fill=WOOD2, stroke=GREEN, sw=0.5)          # rodapé
    sh.rect(1.0, 0, 1.85, 2.1, fill=CREAM, stroke=GREEN, sw=0.8); sh.line(1.0, 0, 1.85, 2.1, GREEN, 0.4); sh.line(1.85, 0, 1.0, 2.1, GREEN, 0.4)   # porta de correr (vão)
    sh.text(1.42, 2.25, "porta de correr 0,85 x 2,10", 7.5, GREEN)
    sh.rect(-1.3, 0.35, 1.3, 1.65, fill=LINEN, stroke=GREEN, sw=0.9)      # cabeceira estofada curva
    sh.add(f'<path d="M{sh.X(-1.3):.1f},{sh.Y(1.65):.1f} Q{sh.X(0):.1f},{sh.Y(1.85):.1f} {sh.X(1.3):.1f},{sh.Y(1.65):.1f}" fill="{LINEN}" stroke="{GREEN}" stroke-width="0.9"/>')
    for k in range(1, 5): sh.line(-1.3 + k * 0.52, 0.35, -1.3 + k * 0.52, 1.65, "#D6CCB8", 0.6)
    for s in (-1, 1):
        sh.rect(s * 1.05 if s < 0 else 1.05, 0.15, s * 1.55 if s < 0 else 1.55, 0.65, fill=sh.pattern("wood"), stroke=GREEN, sw=0.8)   # criados suspensos
        sh.circle(s * 1.3, 1.1, 0.07, fill=BRASS, stroke=GREEN, sw=0.5); sh.line(s * 1.3, 1.1, s * 1.15, 1.1, BRASS, 2)             # arandelas
    sh.rect(-0.97, 0, 0.97, 0.55, fill="#FFFFFF", stroke=GREEN, sw=0.8); sh.rect(-0.97, 0.55, 0.97, 0.62, fill="#F4EFE8", stroke=GREEN, sw=0.5)   # cama (vista)
    sh.rect(-0.85, 0.62, -0.05, 0.9, fill="#FFFFFF", stroke=GREEN, sw=0.5); sh.rect(0.05, 0.62, 0.85, 0.9, fill="#FFFFFF", stroke=GREEN, sw=0.5)
    sh.line(-1.3, 1.65, 1.3, 1.65, "#FFF3C4", 3)   # LED retroiluminação
    sh.rect(-2.93, 2.6, 2.93, 2.62, fill=STEEL, stroke="none")   # trilho do forro
    sh.dim(-1.3, 0.35, 1.3, 0.35, -0.55, label="2,60 · painel MA-03", size=9); sh.dim(-2.8, 0, 2.8, 0, -1.0, label="5,60 · parede do banho", size=9)
    sh.dim(3.2, 0, 3.2, 1.65, 0.0, label="1,65", size=9); sh.dim(3.2, 0, 3.2, 2.6, 0.55, label="2,60 · forro", size=9)
    sh.leader(-1.3, 1.5, -2.4, 3.0, "MA-03 cabeceira estofada em linho, curva", 8.5, anchor="end"); sh.leader(1.3, 0.4, 2.2, 3.0, "criados suspensos com gaveta e USB", 8.5)
    sh.leader(-2.0, 2.2, -2.6, 3.4, "ripado termotratado até o forro", 8.5, anchor="end"); sh.leader(0.0, 3.5, 1.2, 3.85, "Espinha de Luz (acima do forro)", 8.5)

def elev_B(sh):
    """parede lateral esquerda (olhar +y), eixo u = x, do vidro frontal (0,90) à parede do banho (6,60)."""
    ceil = _ceiling_line(sh, 0.9, 6.6)
    poly = [(0.9, 0)] + ceil + [(6.6, 0)]
    sh.poly(poly, fill="#F6F1E8", stroke=GREEN, sw=1.4)
    sh.line(0.9, 0, C.shear(0.9, 3.9), 3.9, GREEN, 1.4)   # fachada inclinada
    sh.rect(0.9, 0, 6.6, 0.15, fill=WOOD2, stroke=GREEN, sw=0.5)   # rodapé técnico
    # MA-01 mini cozinha: geladeira | forno + cooktop | cuba sobre gaveteiro | preparo + air fryer, lixeira
    sh.rect(1.2, 0.15, 3.2, 0.9, fill=sh.pattern("wood"), stroke=GREEN, sw=0.9); sh.rect(1.2, 0.87, 3.2, 0.9, fill=STONE, stroke=GREEN, sw=0.5)
    sh.rect(1.25, 0.15, 1.75, 0.85, fill="#FFFFFF", stroke=GREEN, sw=0.5); sh.text(1.5, 0.5, "geladeira 120 L", 6.5, GREEN)
    sh.rect(1.85, 0.25, 2.35, 0.83, fill="#FFFFFF", stroke=GREEN, sw=0.5); sh.rect(1.9, 0.32, 2.3, 0.72, fill="none", stroke=GREEN, sw=0.4); sh.text(2.1, 0.5, "forno 45 L", 6.5, GREEN)
    sh.rect(1.85, 0.9, 2.35, 0.93, fill=STEEL, stroke="none"); sh.text(2.1, 1.0, "cooktop indução 2 bocas", 6, GREEN)
    sh.rect(2.42, 0.15, 2.78, 0.85, fill="none", stroke=GREEN, sw=0.5); sh.line(2.42, 0.5, 2.78, 0.5, GREEN, 0.4); sh.text(2.6, 0.32, "gaveteiro", 6, GREEN)
    sh.line(2.6, 0.9, 2.6, 1.15, BRASS, 2); sh.line(2.6, 1.15, 2.72, 1.15, BRASS, 2)
    sh.rect(2.85, 0.15, 3.15, 0.85, fill="none", stroke=GREEN, sw=0.5); sh.text(3.0, 0.5, "lixeira", 6, GREEN)
    sh.rect(2.86, 0.9, 3.16, 1.22, fill="#E8E4DC", stroke=GREEN, sw=0.6); sh.text(3.01, 1.06, "air fryer", 6, GREEN)
    sh.rect(1.2, 1.45, 3.2, 1.5, fill=WOOD2, stroke=GREEN, sw=0.6); sh.line(1.2, 1.45, 3.2, 1.45, "#FFF3C4", 3)
    sh.rect(1.8, 1.36, 2.4, 1.45, fill="#D9D9D6", stroke=GREEN, sw=0.5); sh.text(2.1, 1.3, "depurador slim 60", 5.5, GREEN)
    sh.rect(1.28, 0.9, 1.5, 1.14, fill="none", stroke=GREEN, sw=0.5); sh.circle(1.65, 1.05, 0.06, fill="#FFFFFF", stroke=GREEN, sw=0.5)   # cafeteira / chaleira
    # MA-02 armário
    sh.rect(3.4, 0.15, 4.5, 1.5, fill=sh.pattern("wood"), stroke=GREEN, sw=0.9); sh.line(3.95, 0.15, 3.95, 1.5, GREEN, 0.5)
    for xv in [3.45 + i * 0.05 for i in range(21)]: sh.line(xv, 0.2, xv, 1.45, "#A8865E", 0.3)
    sh.rect(3.4, 1.47, 4.5, 1.5, fill=STONE, stroke=GREEN, sw=0.5)
    # Olhos esquerdos (JO2 x 3,40 · JO3 x 5,70)
    for (xc, rx, ry, zc) in ((3.4, 0.8, 0.475, 1.5), (5.7, 0.7, 0.4, 1.45)):
        sh.add(f'<ellipse cx="{sh.X(xc):.1f}" cy="{sh.Y(zc):.1f}" rx="{rx * sh.s:.1f}" ry="{ry * sh.s:.1f}" fill="{GLASS}" stroke="{GREEN}" stroke-width="0.9"/>')
        sh.add(f'<ellipse cx="{sh.X(xc):.1f}" cy="{sh.Y(zc):.1f}" rx="{(rx + 0.11) * sh.s:.1f}" ry="{(ry + 0.11) * sh.s:.1f}" fill="none" stroke="{WOOD2}" stroke-width="5"/>')
    # cama e banco (em vista, lado esquerdo)
    sh.rect(4.5, 0.15, 6.42, 0.55, fill="#FFFFFF", stroke=GREEN, sw=0.7); sh.rect(6.42, 0.35, 6.6, 1.65, fill=LINEN, stroke=GREEN, sw=0.7)
    sh.rect(5.95, 0.15, 6.42, 0.65, fill=sh.pattern("wood"), stroke=GREEN, sw=0.7); sh.rect(4.05, 0.15, 4.45, 0.45, fill=SAND, stroke=GREEN, sw=0.6)
    # forro / espinha
    sh.rect(1.9, 3.75, 6.6, 3.85, fill=GLASS, stroke=GREEN, sw=0.6); sh.text(4.2, 3.95, "Espinha de Luz 0,70 x 4,70 (no forro)", 7.5, GREEN)
    sh.dim(1.2, -0.3, 3.2, -0.3, -0.35, label="2,00 · MA-01", size=9); sh.dim(3.4, -0.3, 4.5, -0.3, -0.35, label="1,10 · MA-02", size=9); sh.dim(0.9, -0.3, 6.6, -0.3, -0.95, label="5,70", size=9)
    sh.dim(7.0, 0, 7.0, 0.9, 0.0, label="0,90", size=9); sh.dim(7.0, 0, 7.0, 1.5, 0.5, label="1,50", size=9); sh.dim(7.0, 0, 7.0, 3.9, 1.0, label="3,90 · pé-direito no eixo", size=9)
    sh.leader(1.9, 1.45, 1.0, 2.6, "prateleira flutuante com LED e depurador", 8.5, anchor="end"); sh.leader(3.95, 1.0, 3.3, 2.6, "portas ripadas · cofre · cabideiro", 8.5, anchor="end")
    sh.leader(3.4, 1.98, 4.6, 2.9, "Janela Olho JO2 1,60 x 0,95 · requadro madeira", 8.5); sh.leader(0.95, 2.6, 0.3, 3.2, "anel de vidro inclinado 8°", 8.5, anchor="end")

def elev_C(sh):
    """parede divisória, lado do banho (x = 6,70), olhar -x: eixo u = -y (bancada à esquerda)."""
    sec = shell_section_yz(6.75); sec = [(-y, z) for (y, z) in sec]
    sh.poly(sec, fill="#F6F1E8", stroke=GREEN, sw=1.4)
    sh.rect(-2.8, 0, 2.8, 2.4, fill=RIP, stroke=GREEN, sw=0.8)
    for yv in [-2.8 + i * 0.06 for i in range(94)]: sh.line(yv, 0.1, yv, 2.4, "#A8865E", 0.35)
    sh.rect(0.55, 0, 2.2, 2.4, fill=TILE, stroke=GREEN, sw=0.7)   # zona molhada (porcelanato) atrás da bancada
    for xv in [0.55 + i * 0.6 for i in range(3)]: sh.line(xv, 0, xv, 2.4, "#B9B7AE", 0.5)
    for zv in [0.6, 1.2, 1.8]: sh.line(0.55, zv, 2.2, zv, "#B9B7AE", 0.5)
    sh.rect(-2.8, 0, 2.8, 0.1, fill=TILE, stroke=GREEN, sw=0.5)
    # MA-04 bancada (y -2,05..-0,55 → u 0,55..2,05)
    sh.rect(0.55, 0.25, 2.05, 0.65, fill=sh.pattern("wood"), stroke=GREEN, sw=0.9); sh.rect(0.55, 0.79, 2.05, 0.85, fill=STONE, stroke=GREEN, sw=0.7)
    sh.rect(0.55, 0.65, 2.05, 0.79, fill="none", stroke=GREEN, sw=0.5); sh.line(1.3, 0.25, 1.3, 0.65, GREEN, 0.4)
    sh.add(f'<path d="M{sh.X(1.05):.1f},{sh.Y(0.79):.1f} Q{sh.X(1.3):.1f},{sh.Y(0.62):.1f} {sh.X(1.55):.1f},{sh.Y(0.79):.1f}" fill="#FFFFFF" stroke="{GREEN}" stroke-width="0.6"/>')
    sh.line(1.3, 0.85, 1.3, 1.05, BRASS, 2.5); sh.line(1.3, 1.05, 1.42, 1.05, BRASS, 2.5)
    sh.circle(1.3, 1.55, 0.45, fill="#E8E4DC", stroke=GREEN, sw=0.8); sh.circle(1.3, 1.55, 0.49, fill="none", stroke="#FFF3C4", sw=3)
    sh.rect(2.25, 0.85, 2.6, 1.55, fill=STONE, stroke=GREEN, sw=0.6); sh.text(2.42, 1.2, "nicho", 7, GREEN)
    # porta de correr (vão) do lado do banho: y 1,0..1,85 → u -1,85..-1,0
    sh.rect(-1.85, 0, -1.0, 2.1, fill=CREAM, stroke=GREEN, sw=0.8); sh.text(-1.42, 2.22, "vão 0,85 x 2,10", 7.5, GREEN)
    sh.rect(-2.75, 0, -1.95, 2.1, fill="none", stroke=GREEN, sw=0.6, dash="3 2"); sh.text(-2.35, 1.0, "folha recolhida", 7, GREEN, rotate=-90)
    # forro do banho e alçapão
    sh.rect(-2.9, 2.4, 2.9, 2.45, fill=WOOD2, stroke=GREEN, sw=0.5); sh.rect(-0.3, 2.4, 0.3, 2.45, fill=GREEN, stroke="none"); sh.text(0, 2.6, "MA-08 alçapão 0,60 x 0,60", 7.5, GREEN)
    sh.dim(0.55, -0.35, 2.05, -0.35, -0.3, label="1,50 · MA-04", size=9); sh.dim(3.2, 0, 3.2, 0.85, 0.0, label="0,85", size=9); sh.dim(3.2, 0, 3.2, 2.4, 0.5, label="2,40 · forro", size=9)
    sh.leader(1.3, 0.8, 0.2, 3.0, "cuba esculpida em quartzito · misturador latão", 8.5, anchor="end"); sh.leader(1.75, 1.55, 2.9, 3.0, "espelho Ø0,90 LED antiembaçante", 8.5)
    sh.leader(-2.4, 1.6, -2.9, 3.0, "ripado termotratado (zona seca)", 8.5, anchor="end")

def elev_D(sh):
    """fachada de vidro vista de dentro (olhar -x a partir de x = 3): eixo u = -y."""
    sec = [(-y, z) for (y, z) in C.section_local(0.9, 80) if z >= -0.01]
    sec = [(u, max(z, 0)) for (u, z) in sec]
    sh.poly(sec, fill=GLASS, stroke=GREEN, sw=1.6, opacity=0.9)
    for u in (-1.6, -0.6, 0.6, 1.6): sh.line(u, 0, u, 3.9, STEEL, 2.2)     # montantes
    sh.line(-2.7, 2.4, 2.7, 2.4, STEEL, 2.2)                                # travessa
    sh.rect(-1.6, 0, -0.6, 2.4, fill="none", stroke=GREEN, sw=1.2); sh.circle(-0.7, 1.05, 0.03, fill=BRASS, stroke="none"); sh.text(-1.1, 2.55, "PV1 1,00 x 2,40", 7.5, GREEN)
    sh.line(-2.75, 3.95, 2.75, 3.95, BRASS, 2.5); sh.text(0, 4.1, "trilho curvo da cortina de linho + blackout (F06)", 7.5, GREEN)
    # mobiliário visto: chaise (y -2,25..-1,45 → u 1,45..2,25), mesa, café (y 1,6..2,2 → u -2,2..-1,6)
    sh.rect(1.45, 0.15, 2.25, 0.45, fill=SAND, stroke=GREEN, sw=0.8); sh.rect(1.45, 0.45, 1.65, 0.75, fill="#CFC3A8", stroke=GREEN, sw=0.6)
    sh.circle(0.95, 0.45, 0.28, fill="none", stroke=GREEN, sw=0.7); sh.line(0.95, 0.15, 0.95, 0.45, GREEN, 1.2)
    sh.rect(-2.2, 0.15, -1.6, 0.9, fill=sh.pattern("wood"), stroke=GREEN, sw=0.8); sh.rect(-2.2, 0.87, -1.6, 0.9, fill=STONE, stroke=GREEN, sw=0.5)
    sh.rect(-2.75, 0, 2.75, 0.15, fill=WOOD2, stroke=GREEN, sw=0.5)
    sh.dim(-2.75, -0.3, 2.75, -0.3, -0.35, label="5,50 · vão do anel de vidro no piso", size=9); sh.dim(3.2, 0, 3.2, 2.4, 0.0, label="2,40", size=9); sh.dim(3.2, 0, 3.2, 4.1, 0.5, label="4,10", size=9)
    sh.leader(1.85, 0.3, 2.9, 1.6, "MS-03 chaise junto ao vidro", 8.5); sh.leader(-1.9, 0.5, -2.9, 1.6, "MA-01 mini cozinha", 8.5, anchor="end")
    sh.leader(0.0, 3.9, 0.8, 3.5, "anel de alumínio bronze RPT", 8.5)

def in03():
    sh = Sheet(1600, 1000, scale=95, ox=400, oy=520)
    sh.header("Zion Casulo · Elevações internas A e B", "A · parede da cabeceira (olhar +x) · B · lateral esquerda: mini cozinha, armário e Olhos (olhar +y) · 1:40")
    sh.text_px(400, 105, "ELEVAÇÃO A · CABECEIRA · x = 6,60", size=11, weight=700, spacing=0.25)
    elev_A(sh)
    sh.ox, sh.oy, sh.s = 830, 520, 95
    sh.text_px(1190, 105, "ELEVAÇÃO B · LATERAL ESQUERDA · y = +2,90", size=11, weight=700, spacing=0.25)
    elev_B(sh)
    sh.title_block("ZION CASULO", "Elevações internas A e B", "1:40 (A1) · cotas em metros", "IN-03", "Cabeceira acoplada MA-03 · mini cozinha MA-01 · armário MA-02")
    sh.save(os.path.join(OUT, "IN-03_elevacoes_A_B.svg"))

def in04():
    sh = Sheet(1600, 1000, scale=95, ox=400, oy=520)
    sh.header("Zion Casulo · Elevações internas C e D", "C · banho, parede da bancada (olhar -x) · D · fachada de vidro vista de dentro (olhar -x) · 1:40")
    sh.text_px(400, 105, "ELEVAÇÃO C · BANHO · x = 6,70", size=11, weight=700, spacing=0.25)
    elev_C(sh)
    sh.ox, sh.oy, sh.s = 1160, 520, 95
    sh.text_px(1160, 105, "ELEVAÇÃO D · FACHADA INTERNA · x = 0,90", size=11, weight=700, spacing=0.25)
    elev_D(sh)
    sh.title_block("ZION CASULO", "Elevações internas C e D", "1:40 (A1) · cotas em metros", "IN-04", "Bancada MA-04 · fachada, porta PV1, chaise e cortina")
    sh.save(os.path.join(OUT, "IN-04_elevacoes_C_D.svg"))

# ============================================================================ IN-05 detalhes da marcenaria acoplada
def in05():
    sh = Sheet(1600, 1000, scale=150, ox=120, oy=380)
    sh.header("Zion Casulo · Detalhes da marcenaria acoplada", "MA-01 mini cozinha · MA-03 cabeceira e criados · MA-04 bancada do banho · MA-02 armário na curva · 1:20 e 1:10")
    # ---- MA-01 corte (1:20) no módulo do forno + cooktop
    sh.text_px(120, 105, "MA-01 · MINI COZINHA · CORTE 1:20 (módulo forno + cooktop)", size=10, weight=700, spacing=0.2, anchor="start")
    sh.rect(0, 0.1, 0.65, 0.87, fill=sh.pattern("wood"), stroke=GREEN, sw=0.9); sh.rect(-0.02, 0.87, 0.67, 0.90, fill=STONE, stroke=GREEN, sw=0.8)
    sh.rect(0.05, 0.25, 0.6, 0.83, fill="#FFFFFF", stroke=GREEN, sw=0.5); sh.text(0.32, 0.56, "forno elétrico 45 L", 7, GREEN); sh.text(0.32, 0.46, "nicho ventilado (grelha no rodapé)", 6.5, EARTH)
    sh.rect(0.08, 0.9, 0.6, 0.94, fill=STEEL, stroke="none"); sh.text(0.34, 0.99, "cooktop de indução 2 bocas embutido no tampo", 6.5, GREEN)
    sh.rect(0.1, 1.31, 0.62, 1.42, fill="#D9D9D6", stroke=GREEN, sw=0.5); sh.text(0.36, 1.27, "depurador slim 60 (carvão ativado)", 6, EARTH)
    sh.rect(0.08, 0.02, 0.52, 0.1, fill=WOOD2, stroke=GREEN, sw=0.5); sh.text(0.3, -0.08, "rodapé recuado 80 mm", 6.5, EARTH)
    # fundo recortado conforme a concha
    sec = [(y - 2.15, z) for (y, z) in _inner_yz(1.9) if 2.0 <= y <= 2.9 and z <= 1.7]
    sh.poly(sec, close=False, stroke=GREEN, sw=1.4); sh.text(0.62, 1.55, "concha (forro interno)", 7, GREEN, rotate=-80)
    sh.rect(0.35, 1.45, 0.6, 1.5, fill=WOOD2, stroke=GREEN, sw=0.6); sh.line(0.35, 1.45, 0.6, 1.45, "#FFF3C4", 3); sh.text(0.3, 1.58, "prateleira 250 mm + LED", 6.5, EARTH)
    sh.dim(0, -0.25, 0.65, -0.25, -0.15, label="0,65", size=8); sh.dim(0.9, 0.1, 0.9, 0.9, 0.0, label="0,90", size=8); sh.dim(0.9, 0.1, 0.9, 1.5, 0.35, label="1,50", size=8)
    sh.leader(0.3, 0.885, -0.1, 1.15, "tampo quartzito 30 mm, borda reta", 7.5, anchor="end"); sh.leader(0.62, 0.5, 0.95, 0.6, "fundo recortado, fixado nos arcos A1-A2 por cantoneiras", 7.5)
    # ---- MA-01 vista (1:20)
    sh.ox, sh.oy = 480, 380
    sh.text_px(480, 105, "MA-01 · MINI COZINHA · VISTA FRONTAL 1:20", size=10, weight=700, spacing=0.2, anchor="start")
    sh.rect(0, 0.1, 2.0, 0.87, fill=sh.pattern("wood"), stroke=GREEN, sw=0.9); sh.rect(-0.02, 0.87, 2.02, 0.9, fill=STONE, stroke=GREEN, sw=0.8)
    sh.rect(0.03, 0.12, 0.57, 0.85, fill="#FFFFFF", stroke=GREEN, sw=0.5); sh.text(0.3, 0.55, "geladeira 120 L", 6.5, GREEN); sh.text(0.3, 0.42, "sob bancada, porta ripada", 6, EARTH)
    sh.rect(0.63, 0.25, 1.17, 0.83, fill="#FFFFFF", stroke=GREEN, sw=0.5); sh.rect(0.68, 0.32, 1.12, 0.72, fill="none", stroke=GREEN, sw=0.4); sh.text(0.9, 0.55, "forno 45 L", 6.5, GREEN); sh.rect(0.63, 0.12, 1.17, 0.22, fill="none", stroke=GREEN, sw=0.4); sh.text(0.9, 0.15, "gaveta", 5.5, GREEN)
    sh.rect(0.65, 0.9, 1.15, 0.93, fill=STEEL, stroke="none"); sh.text(0.9, 1.0, "cooktop 2 bocas", 6, GREEN)
    sh.rect(1.22, 0.12, 1.58, 0.85, fill="none", stroke=GREEN, sw=0.5); sh.line(1.22, 0.5, 1.58, 0.5, GREEN, 0.4); sh.text(1.4, 0.66, "gaveta", 6, GREEN); sh.text(1.4, 0.3, "gaveta", 6, GREEN)
    sh.rect(1.24, 0.87, 1.56, 0.9, fill="#FFFFFF", stroke=GREEN, sw=0.6); sh.line(1.4, 0.9, 1.4, 1.15, BRASS, 2); sh.line(1.4, 1.15, 1.52, 1.15, BRASS, 2); sh.text(1.4, 0.8, "cuba 0,40 x 0,35", 5.5, GREEN)
    sh.rect(1.63, 0.12, 1.97, 0.85, fill="none", stroke=GREEN, sw=0.5); sh.text(1.8, 0.5, "lixeira", 6, GREEN)
    sh.rect(1.64, 0.9, 1.96, 1.22, fill="#E8E4DC", stroke=GREEN, sw=0.6); sh.text(1.8, 1.06, "air fryer", 6, GREEN)
    sh.rect(0.6, 1.31, 1.2, 1.42, fill="#D9D9D6", stroke=GREEN, sw=0.5); sh.text(0.9, 1.27, "depurador", 5.5, EARTH)
    sh.rect(0, 1.42, 2.0, 1.47, fill=WOOD2, stroke=GREEN, sw=0.6); sh.line(0, 1.42, 2.0, 1.42, "#FFF3C4", 3)
    sh.dim(0, -0.25, 2.0, -0.25, -0.15, label="2,00", size=8); sh.dim(0, -0.25, 0.6, -0.25, 0.12, label="0,60", size=8); sh.dim(0.6, -0.25, 1.2, -0.25, 0.12, label="0,60", size=8); sh.dim(1.2, -0.25, 1.6, -0.25, 0.12, label="0,40", size=8); sh.dim(1.6, -0.25, 2.0, -0.25, 0.12, label="0,40", size=8)
    # ---- MA-03 cabeceira corte (1:10)
    sh.ox, sh.oy, sh.s = 1130, 420, 130
    sh.text_px(960, 105, "MA-03 · CABECEIRA E CRIADO SUSPENSO · CORTE 1:15", size=10, weight=700, spacing=0.2, anchor="start")
    sh.rect(-0.1, 0, 0.0, 2.6, fill=RIP, stroke=GREEN, sw=0.9); sh.text(-0.05, 2.3, "parede do banho + ripado", 6.5, GREEN, rotate=-90)
    sh.rect(-0.16, 0.35, -0.06, 1.65, fill="none", stroke=GREEN, sw=0.6); sh.rect(-0.22, 0.35, -0.16, 1.65, fill=LINEN, stroke=GREEN, sw=0.8)
    sh.text(-0.3, 1.0, "estofado 60 mm + estrutura 40 mm", 6.5, GREEN, rotate=-90)
    sh.rect(-0.7, 0.15, -0.2, 0.65, fill=sh.pattern("wood"), stroke=GREEN, sw=0.9); sh.line(-0.7, 0.4, -0.2, 0.4, GREEN, 0.5); sh.text(-0.45, 0.52, "gaveta toque", 6, GREEN); sh.text(-0.45, 0.27, "nicho aberto", 6, GREEN)
    sh.rect(-0.22, 0.15, -0.16, 0.65, fill=STEEL, stroke="none"); sh.text(-0.45, 0.72, "suporte oculto em cantoneira", 6, EARTH)
    sh.line(-0.22, 1.65, -0.06, 1.65, "#FFF3C4", 3); sh.text(-0.5, 1.72, "LED retroiluminação 2700 K", 6.5, EARTH)
    sh.circle(-0.35, 1.1, 0.05, fill=BRASS, stroke=GREEN, sw=0.5); sh.text(-0.6, 1.1, "arandela F01", 6.5, GREEN)
    sh.rect(-1.25, 0, -0.25, 0.55, fill="#FFFFFF", stroke=GREEN, sw=0.6); sh.text(-0.75, 0.3, "box king", 6.5, GREEN)
    sh.dim(-1.0, -0.2, -0.2, -0.2, -0.12, label="0,50 criado", size=8); sh.dim(0.25, 0, 0.25, 0.65, 0.0, label="0,65", size=8); sh.dim(0.25, 0, 0.25, 1.65, 0.28, label="1,65", size=8)
    # ---- MA-04 bancada corte (1:10)
    sh.ox, sh.oy, sh.s = 1380, 420, 130
    sh.text_px(1330, 105, "MA-04 · BANCADA · CORTE 1:15", size=10, weight=700, spacing=0.2, anchor="start")
    sh.rect(-0.05, 0, 0.0, 2.4, fill=TILE, stroke=GREEN, sw=0.8)
    sh.rect(0.0, 0.25, 0.55, 0.65, fill=sh.pattern("wood"), stroke=GREEN, sw=0.9); sh.rect(0.0, 0.65, 0.55, 0.79, fill="none", stroke=GREEN, sw=0.5)
    sh.rect(-0.01, 0.79, 0.57, 0.85, fill=STONE, stroke=GREEN, sw=0.8); sh.rect(0.51, 0.73, 0.57, 0.79, fill=STONE, stroke=GREEN, sw=0.6)
    sh.add(f'<path d="M{sh.X(0.12):.1f},{sh.Y(0.79):.1f} Q{sh.X(0.3):.1f},{sh.Y(0.62):.1f} {sh.X(0.48):.1f},{sh.Y(0.79):.1f}" fill="#FFFFFF" stroke="{GREEN}" stroke-width="0.6"/>')
    sh.line(0.3, 0.62, 0.3, 0.5, GREEN, 0.6); sh.text(0.3, 0.44, "sifão", 6, GREEN)
    sh.line(0.08, 0.85, 0.08, 1.05, BRASS, 2.5); sh.line(0.08, 1.05, 0.2, 1.05, BRASS, 2.5)
    sh.rect(0.0, 1.1, 0.03, 2.0, fill="#E8E4DC", stroke=GREEN, sw=0.6); sh.text(0.12, 1.55, "espelho Ø0,90 LED", 6.5, GREEN, rotate=-90)
    sh.dim(0, -0.2, 0.55, -0.2, -0.12, label="0,55", size=8); sh.dim(0.8, 0, 0.8, 0.85, 0.0, label="0,85", size=8); sh.dim(0.8, 0, 0.8, 0.25, -0.28, label="0,25", size=8)
    # ---- MA-02 armário na curva (1:20)
    sh.ox, sh.oy, sh.s = 200, 900, 150
    sh.text_px(120, 612, "MA-02 · ARMÁRIO ACOPLADO À CURVA · CORTE 1:20", size=10, weight=700, spacing=0.2, anchor="start")
    sec = [(y - 2.2, z) for (y, z) in _inner_yz(3.8) if 2.0 <= y <= 2.95 and z <= 1.75]; sh.poly(sec, close=False, stroke=GREEN, sw=1.4)
    sh.poly([(0, 0.1), (0.65, 0.1), (0.65, 0.95), (0.55, 1.47), (0, 1.47)], fill=sh.pattern("wood"), stroke=GREEN, sw=0.9); sh.rect(-0.02, 1.47, 0.57, 1.5, fill=STONE, stroke=GREEN, sw=0.8)
    for zv in (0.5, 0.85, 1.2): sh.line(0.05, zv, 0.55, zv, GREEN, 0.5)
    sh.circle(0.3, 1.3, 0.02, fill=STEEL, stroke="none"); sh.text(0.3, 1.36, "cabideiro", 6, GREEN); sh.rect(0.08, 0.15, 0.4, 0.42, fill="none", stroke=GREEN, sw=0.5); sh.text(0.24, 0.28, "cofre", 6, GREEN)
    sh.dim(0, -0.15, 0.65, -0.15, -0.12, label="0,65", size=8); sh.dim(0.85, 0.1, 0.85, 1.5, 0.0, label="1,50", size=8)
    sh.leader(0.6, 1.2, 1.0, 1.45, "fundo recortado na concha; fixação nos arcos A3-A4", 7.5)
    # notas gerais
    X0, Y0 = 700, 660
    sh.text_px(X0, Y0, "NOTAS DE MARCENARIA ACOPLADA", size=10, weight=700, spacing=0.25, anchor="start")
    notes = ["Toda a marcenaria MA é fabricada em fábrica, montada e acabada antes do embarque; em campo só se nivela e se fixa.", "Fixação à estrutura: cantoneiras de aço galvanizado parafusadas aos arcos (nunca à membrana); fundos recortados com folga de 15 mm para a concha e fechados com perfil de EPDM.",
             "Madeira: carvalho natural em lâmina sobre MDF naval 18 mm; ripado termotratado 20 x 40; verniz PU fosco 2 demãos.", "Pedra: quartzito 30 mm, bordas retas polidas; cubas esculpidas com impermeabilização de fábrica.",
             "Ferragens: dobradiças e corrediças com amortecimento; puxadores cava ou em latão escovado; fitas LED 2700 K IP20 (IP65 no banho) com perfil difusor.", "Elétrica embutida na marcenaria: cooktop (C13, 20 A) e forno (C14, 16 A) em circuitos dedicados, tomadas da mini cozinha (C5), USB nos criados; passagem pelo rodapé técnico MA-07; cuba com AF/AQ Ø20 e sifão Ø50.",
             "Tolerâncias: ± 3 mm nas dimensões; conferência com gabarito da seção da concha antes da fabricação (arcos A1 a A4)."]
    yy = Y0 + 18
    for n in notes:
        w = n.split(); cur = ""; lines = []
        for x in w:
            if len(cur) + len(x) + 1 > 120: lines.append(cur); cur = x
            else: cur = (cur + " " + x).strip()
        lines.append(cur)
        for l in lines: sh.text_px(X0, yy, "· " + l if l is lines[0] else "  " + l, size=8.5, anchor="start"); yy += 12
        yy += 3
    sh.title_block("ZION CASULO", "Detalhes da marcenaria acoplada", "1:20 / 1:10 (A1)", "IN-05", "MA-01 mini cozinha · MA-02 · MA-03 · MA-04")
    sh.save(os.path.join(OUT, "IN-05_detalhes_marcenaria.svg"))

# ============================================================================ IN-06 quadro de mobiliário
def in06():
    sh = Sheet(1600, 1000)
    sh.header("Zion Casulo · Quadro de mobiliário e marcenaria", "Marcenaria acoplada (MA) com descrição, dimensões, materiais e FF&E relacionado · mobiliário solto (MS) · 1:50 na planta IN-01")
    def wrap(t, n):
        w = t.split(); out = []; cur = ""
        for x in w:
            if len(cur) + len(x) + 1 > n: out.append(cur); cur = x
            else: cur = (cur + " " + x).strip()
        return out + [cur]
    X0, Y0 = 60, 110; cols = [0, 60, 250, 400, 470, 560, 1080]
    heads = ["Cód.", "Peça", "Dimensões (m)", "Amb.", "FF&E", "Descrição", "Materiais / acabamento"]
    sh.text_px(X0, Y0, "MARCENARIA ACOPLADA", size=10, weight=700, spacing=0.25, anchor="start")
    for h_, cx in zip(heads, cols): sh.text_px(X0 + cx, Y0 + 20, h_.upper(), size=7.5, fill=EARTH, spacing=0.15, anchor="start")
    sh.add(f'<line x1="{X0}" y1="{Y0 + 26}" x2="{X0 + 1480}" y2="{Y0 + 26}" stroke="{GREEN}" stroke-width="0.6"/>')
    yy = Y0 + 42
    for m in MA:
        dims = f"{fmt(m['x2'] - m['x1'])} x {fmt(m['y2'] - m['y1']) if m['y2'] != m['y1'] else '—'} x h {fmt(m['h'])}" if m["cod"] not in ("MA-07", "MA-08") else ("8,50 m lineares x h 0,15" if m["cod"] == "MA-07" else "0,60 x 0,60")
        cells = [m["cod"], m["nome"], dims, m["amb"], m["ffe"], m["desc"], m["mat"]]
        lines = 1
        for c, cx, n in zip(cells, cols, (8, 30, 24, 12, 16, 100, 60)):
            ls = wrap(c, n)
            for k, l in enumerate(ls): sh.text_px(X0 + cx, yy + k * 11, l, size=8, anchor="start", weight=700 if cx == 0 else 400)
            lines = max(lines, len(ls))
        yy += 11 * lines + 7; sh.add(f'<line x1="{X0}" y1="{yy - 5}" x2="{X0 + 1480}" y2="{yy - 5}" stroke="{SAND}" stroke-width="0.6"/>')
    yy += 14; sh.text_px(X0, yy, "MOBILIÁRIO SOLTO (FF&E)", size=10, weight=700, spacing=0.25, anchor="start"); yy += 20
    cols2 = [0, 60, 300, 480, 600, 760]
    for h_, cx in zip(["Cód.", "Peça", "Dimensões (m)", "Amb.", "FF&E", "Posição"], cols2): sh.text_px(X0 + cx, yy, h_.upper(), size=7.5, fill=EARTH, spacing=0.15, anchor="start")
    yy += 6; sh.add(f'<line x1="{X0}" y1="{yy}" x2="{X0 + 1480}" y2="{yy}" stroke="{GREEN}" stroke-width="0.6"/>'); yy += 14
    for m in MS:
        for c, cx in zip([m["cod"], m["nome"], m["dims"], m["amb"], m["ffe"], m["pos"]], cols2): sh.text_px(X0 + cx, yy, c, size=8, anchor="start", weight=700 if cx == 0 else 400)
        yy += 15; sh.add(f'<line x1="{X0}" y1="{yy - 5}" x2="{X0 + 1480}" y2="{yy - 5}" stroke="{SAND}" stroke-width="0.6"/>')
    sh.text_px(X0, yy + 12, "Itens de FF&E não posicionados na planta (enxoval, amenities, papelaria, kit de segurança, luminárias de deck) constam da lista completa em ffe.py / Catálogo da Linha.", size=8, fill=EARTH, anchor="start")
    sh.title_block("ZION CASULO", "Quadro de mobiliário e marcenaria", "s/ escala (A1)", "IN-06", "MA-01 a MA-08 · MS-01 a MS-09")
    sh.save(os.path.join(OUT, "IN-06_quadro_mobiliario.svg"))

def build():
    in01(); in02(); in03(); in04(); in05(); in06(); print("interiores casulo ok →", os.path.abspath(OUT))

if __name__ == "__main__":
    build()

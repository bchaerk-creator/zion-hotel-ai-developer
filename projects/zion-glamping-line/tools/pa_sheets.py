# -*- coding: utf-8 -*-
"""Pranchas complementares do PROJETO ARQUITETÔNICO (padrão de projetista):
PA-00 capa, índice, quadro de áreas e notas · PA-01 implantação · PA-04 planta de cobertura · PA-05 forro e iluminação
· PA-08b fachada lateral esquerda · PA-09 quadro de esquadrias. Para ZION CASULO e ZION SAFARI."""
import math, os
import numpy as np
from geometry import Cocoon, Zenith
from svgkit import *
from drawings_cocoon import shell_plan_pts, arch_plan, top_profile, bottom_profile
from drawings_zenith import roof_outline_pts, contours, slats, ground

C, Z = Cocoon(), Zenith()
OUT = {"cocoon": os.path.join(os.path.dirname(__file__), "..", "cocoon", "projeto"), "zenith": os.path.join(os.path.dirname(__file__), "..", "zenith", "projeto")}
NAME = {"cocoon": "ZION CASULO", "zenith": "ZION SAFARI"}

# ----------------------------------------------------------------------------- quadro de áreas
def zone_area(x1, x2, n=200):
    return sum(2 * C.floor_hw(x1 + (x2 - x1) * (i + 0.5) / n) * (x2 - x1) / n for i in range(n))

AREAS = {
    "cocoon": [("01", "Vestíbulo coberto", zone_area(0.45, 0.9), "Deck cumaru", "+0,00"), ("02", "Estar / lounge", zone_area(0.9, 4.5), "Carvalho de engenharia 14 mm", "+0,00"),
               ("03", "Suíte", zone_area(4.5, 6.6), "Carvalho de engenharia 14 mm", "+0,00"), ("04", "Banho", zone_area(6.7, 9.4), "Porcelanato 60 x 120 antiderrapante", "-0,01"),
               ("05", "Ático técnico (sobre o banho)", 9.2, "Compensado naval (manutenção)", "+2,45"), ("06", "Deck frontal", 29.9, "Cumaru 20 x 140", "-0,02"),
               ("07", "Escada de acesso (3 degraus)", 2.2, "Cumaru", "-0,60 a -0,02")],
    "zenith": [("01", "Estar / lounge", 3.45 * 5.2, "Carvalho de engenharia 14 mm", "+0,00"), ("02", "Ilha do Café", 2.0 * 0.72, "Bancada em pedra", "+0,90"),
               ("03", "Suíte", 2.65 * 5.2, "Carvalho de engenharia 14 mm", "+0,00"), ("04", "Closet", 2.0 * 0.6, "Marcenaria", "+0,00"),
               ("05", "Banho", 2.95 * 5.2, "Porcelanato 60 x 120 antiderrapante", "-0,01"), ("06", "Ático técnico (sobre o banho)", 15.3, "Compensado naval", "+2,55"),
               ("07", "Terraço frontal", 20.4, "Cumaru 20 x 140", "-0,02"), ("08", "Passarela lateral", 7.6, "Cumaru 20 x 140", "-0,02"),
               ("09", "Hidromassagem (no terraço)", 2.84, "Fibra / acrílico", "-0,02")],
}
ESQUADRIAS = {
    "cocoon": [("PV1", "Porta pivotante de vidro", 1.00, 2.40, 1, "Vidro insulado 6 lam + 12 + 6 temp low-e; pivô de piso; alumínio bronze RPT", "Fachada, à esquerda (y +0,60 a +1,60)"),
               ("V1", "Fachada panorâmica fixa (anel inclinado 8°)", 4.88, 4.13, 1, "8 painéis de vidro insulado entre 4 montantes e travessa a 2,40; anel de alumínio curvo", "Fachada frontal, x 0,90"),
               ("JO1", "Janela Olho basculante", 1.60, 0.95, 2, "Lente em requadro de madeira laminada 220 mm; vidro insulado; ferragem basculante 15°", "Estar dir. (x 2,30) e suíte dir. (x 4,90)"),
               ("JO2", "Janela Olho fixa", 1.60, 0.95, 1, "Idem, fixa", "Estar esq. (x 3,40)"),
               ("JO3", "Janela Olho fixa", 1.40, 0.80, 1, "Idem, fixa", "Suíte esq. (x 5,70)"),
               ("JO4", "Olho do banho fixo (alto)", 1.10, 0.60, 1, "Idem, vidro jateado", "Banho dir. (x 7,90), peitoril 1,60"),
               ("JO5", "Olho da banheira fixo (baixo)", 0.90, 0.50, 1, "Idem, vidro jateado", "Cauda esq. (x 8,50), peitoril 1,15"),
               ("CL1", "Espinha de Luz (claraboia)", 1.175, 0.70, 4, "Vidro laminado 8 + 8 mm sobre berços com EPDM; junta de silicone estrutural", "Cumeeira, x 1,90 a 6,60"),
               ("PC1", "Porta de correr do banho", 0.85, 2.10, 1, "Folha de madeira laminada com trilho superior embutido", "Parede da cabeceira, y +1,00 a +1,85")],
    "zenith": [("PC1", "Fachada de correr (2 fixas + 2 de correr)", 5.40, 2.75, 1, "4 folhas 1,35 x 2,75; vidro insulado low-e; trilho embutido no piso com dreno", "Fachada frontal, x 0"),
               ("VF1", "Vidro lateral fixo", 1.60, 2.75, 4, "Painéis fixos de vidro insulado; montantes de alumínio RPT bronze", "Lateral direita, x 0 a 6,40"),
               ("J1", "Janela do café (fixa)", 2.20, 1.10, 1, "Vidro insulado; peitoril 1,10", "Lateral esquerda, x 0,50 a 2,70"),
               ("J2", "Fresta alta do closet (basculante)", 2.00, 0.50, 1, "Vidro insulado; peitoril 1,90; motorizada", "Lateral esquerda, x 3,90 a 5,90"),
               ("J3", "Fresta da banheira (fixa)", 2.40, 0.65, 1, "Vidro insulado jateado; peitoril 1,50", "Fundos, y -0,80 a +1,60"),
               ("J4", "Janela alta do chuveiro (basculante)", 1.00, 0.50, 1, "Vidro insulado jateado; peitoril 1,90", "Lateral direita, x 8,30 a 9,30"),
               ("OC1", "Óculo do Zênite", 1.20, 1.20, 1, "Cúpula de vidro laminado curvo Ø1,20 sobre anel; vidro interno plano; esquadria RPT calandrada", "Cume principal, sobre a cama"),
               ("RE1", "Chaminé do Respiro", 0.70, 0.70, 1, "Tubo de alumínio Ø700 com veneziana motorizada e tela", "Cume secundário, sobre o café"),
               ("PC2", "Porta de correr do banho", 1.10, 2.20, 1, "Folha de madeira laminada, trilho superior", "Parede da cabeceira, y +1,50 a +2,60")],
}
NOTAS = [
    "Cotas em metros; níveis em metros referidos ao piso interno acabado (+0,00). Prevalecem as cotas escritas sobre as medidas tomadas na prancha.",
    "Projeto arquitetônico em nível de estudo preliminar / anteprojeto para produto industrializado. Projeto executivo, cálculo estrutural (NBR 8800 / NBR 6123) e form-finding da membrana devem ser elaborados e assinados por profissionais habilitados (ART/RRT) antes da fabricação.",
    "Fundação em estacas helicoidais galvanizadas: comprimento e quantidade final conforme sondagem SPT ou ensaio de torque no sítio. Alternativas nos modelos A, B e C do Product Book.",
    "Estrutura metálica em tubos ASTM A500 galvanizados a fogo (NBR 6323) com pintura a pó nas peças aparentes; ligações parafusadas classe 8.8; sem solda em campo.",
    "Membrana externa em poliéster/PVC com laca PVDF 1050 g/m² (tipo III), classe B1, garantia mínima de 15 anos; câmara ventilada 60 mm; isolamento em lã de PET 50 mm com manta refletiva; forro tensionado classe M1.",
    "Vidros insulados 6 mm laminado + 12 mm argônio + 6 mm temperado low-e (U ≈ 1,6 W/m²K, FS 0,40) em esquadrias de alumínio com ruptura de ponte térmica, anodizado bronze. Vidros de banho jateados.",
    "Pisos: carvalho de engenharia 14 mm sobre compensado naval 18 mm; banho em porcelanato antiderrapante sobre placa cimentícia impermeabilizada; deck em cumaru 20 x 140 com fixação oculta.",
    "Instalações: alimentação elétrica 220 V monofásica; quadro no ático técnico; água fria por PEX Ø25 com registro geral e filtro; esgoto Ø100 por gravidade a fossa séptica + filtro anaeróbio (ou estação compacta); ver DET-06 a DET-09.",
    "Climatização por evaporadora dutada inverter (quente/frio) no ático com difusores lineares; condensadora externa oculta por painel ripado. Ventilação natural por janelas basculantes e respiro de cumeeira / chaminé.",
    "Implantação genérica de referência: orientação, afastamentos, acessos e redes devem ser definidos para cada sítio conforme legislação municipal, condicionantes ambientais e projeto de implantação do empreendimento.",
]
SHEETS = {
    "cocoon": [("PA-00", "Capa, índice, quadro de áreas e notas gerais", "s/ escala"), ("PA-01", "Planta de situação e implantação", "1:200"), ("PA-02", "Planta baixa cotada", "1:50"),
               ("PA-03", "Planta de layout", "1:50"), ("PA-04", "Planta de cobertura", "1:50"), ("PA-05", "Planta de forro e iluminação", "1:50"),
               ("PA-06", "Cortes A-A e B-B", "1:50 / 1:40"), ("PA-07", "Fachada frontal e fachada traseira", "1:50"), ("PA-08", "Fachadas laterais direita e esquerda", "1:50"),
               ("PA-09", "Quadro de esquadrias", "1:50"), ("PA-10", "Planta estrutural", "1:50"), ("PA-11", "Detalhes construtivos DET-01, 03, 04, 05, 06, 10", "1:5 a 1:20"),
               ("PA-12", "Isométrica e modelo explodido", "s/ escala")],
    "zenith": [("PA-00", "Capa, índice, quadro de áreas e notas gerais", "s/ escala"), ("PA-01", "Planta de situação e implantação", "1:200"), ("PA-02", "Planta baixa cotada", "1:50"),
               ("PA-03", "Planta de layout", "1:50"), ("PA-04", "Planta de cobertura", "1:50"), ("PA-05", "Planta de forro e iluminação", "1:50"),
               ("PA-06", "Cortes A-A e B-B", "1:50 / 1:45"), ("PA-07", "Fachada frontal e fachada traseira", "1:50"), ("PA-08", "Fachadas laterais direita e esquerda", "1:50"),
               ("PA-09", "Quadro de esquadrias", "1:50"), ("PA-10", "Planta estrutural", "1:50"), ("PA-11", "Detalhes construtivos DET-02, 03, 04, 05, 06, 11", "1:5 a 1:20"),
               ("PA-12", "Isométrica e modelo explodido", "s/ escala")],
}

def tb(sh, product, title, scale, sheet, sub=""):
    sh.title_block(NAME[product], title, scale, sheet, sub)

# ----------------------------------------------------------------------------- PA-00 CAPA
def capa(product):
    sh = Sheet(1600, 1000, bg=CREAM)
    c = product == "cocoon"
    sh.add(f'<rect x="0" y="0" width="560" height="1000" fill="{BLACK}"/>')
    sh.text_px(60, 120, "ZION", size=42, weight=800, spacing=0.4, fill=CREAM, anchor="start")
    sh.text_px(60, 146, "GLAMPING COLLECTION · ZION HOTEL GROUP INTERNATIONAL", size=9.5, spacing=0.3, fill=SAND, anchor="start")
    sh.text_px(60, 300, "PROJETO", size=13, spacing=0.5, fill=SAND, anchor="start"); sh.text_px(60, 322, "ARQUITETÔNICO", size=13, spacing=0.5, fill=SAND, anchor="start")
    sh.text_px(60, 420, NAME[product], size=46, weight=200, spacing=0.12, fill=CREAM, anchor="start")
    sh.text_px(60, 456, "Cabana biomórfica em casulo" if c else "Cabana escultural de dois cumes", size=15, fill=SAND, anchor="start")
    sh.text_px(60, 484, ("9,60 x 6,00 x 4,20 m · 48 m² internos · deck 29,9 m² · total 78 m²" if c else "9,50 x 5,40 m · cume 5,80 m · 48,4 m² internos · terraço 28 m² · total 79,3 m²"), size=11.5, fill=SAND, anchor="start")
    for i, (k, v) in enumerate([("Proprietário", "Zion Hotel Group International Ltda"), ("Produto", NAME[product] + " (Zion Glamping Collection)"), ("Fase", "Estudo preliminar / anteprojeto de produto"),
                                ("Uso", "Unidade de hospedagem (glamping / boutique hotel)"), ("Sistema", "ZION SHELL SYSTEM: aço galvanizado + membrana PVDF + vidro"), ("Revisão", "R00 · setembro de 2026"), ("Pranchas", f"{len(SHEETS[product])} (PA-00 a PA-12)")]):
        sh.text_px(60, 600 + i * 28, k.upper(), size=8.5, spacing=0.25, fill=EARTH, anchor="start"); sh.text_px(200, 600 + i * 28, v, size=11.5, fill=CREAM, anchor="start")
    sh.text_px(60, 920, "Pré-dimensionamento de engenharia: bitolas, espessuras e fundações", size=9, fill=SAND, anchor="start"); sh.text_px(60, 934, "a validar por engenheiro habilitado (ART/RRT).", size=9, fill=SAND, anchor="start")
    # índice de pranchas
    X0 = 610; sh.text_px(X0, 90, "ÍNDICE DE PRANCHAS", size=12, weight=700, spacing=0.3, anchor="start")
    for i, (n, t, e) in enumerate(SHEETS[product]):
        y = 118 + i * 19
        sh.text_px(X0, y, n, size=11, weight=700, anchor="start"); sh.text_px(X0 + 70, y, t, size=11, anchor="start"); sh.text_px(X0 + 560, y, e, size=10, fill=EARTH, anchor="end")
        sh.add(f'<line x1="{X0}" y1="{y + 6}" x2="{X0 + 560}" y2="{y + 6}" stroke="{SAND}" stroke-width="0.6"/>')
    # quadro de áreas
    Y0 = 118 + len(SHEETS[product]) * 19 + 34
    sh.text_px(X0, Y0, "QUADRO DE ÁREAS", size=12, weight=700, spacing=0.3, anchor="start")
    hdr = [("N.", 0), ("Ambiente", 40), ("Área (m²)", 330), ("Piso", 400), ("Nível", 700)]
    for h, dx in hdr: sh.text_px(X0 + dx, Y0 + 26, h.upper(), size=8.5, spacing=0.15, fill=EARTH, anchor="start")
    sh.add(f'<line x1="{X0}" y1="{Y0 + 32}" x2="{X0 + 960}" y2="{Y0 + 32}" stroke="{GREEN}" stroke-width="0.8"/>')
    tot_int = 0; tot_ext = 0
    for i, (n, amb, a, piso, niv) in enumerate(AREAS[product]):
        y = Y0 + 50 + i * 18
        sh.text_px(X0, y, n, size=10.5, anchor="start"); sh.text_px(X0 + 40, y, amb, size=10.5, anchor="start"); sh.text_px(X0 + 380, y, fmt(a), size=10.5, anchor="end")
        sh.text_px(X0 + 400, y, piso, size=10, fill=EARTH, anchor="start"); sh.text_px(X0 + 700, y, niv, size=10, anchor="start")
        sh.add(f'<line x1="{X0}" y1="{y + 6}" x2="{X0 + 960}" y2="{y + 6}" stroke="{SAND}" stroke-width="0.5"/>')
        if "Deck" in amb or "Terraço" in amb or "Passarela" in amb or "Escada" in amb or "Hidro" in amb: tot_ext += a
        elif "Ático" not in amb: tot_int += a
    y = Y0 + 50 + len(AREAS[product]) * 18 + 6
    for j, (k, v) in enumerate([("Área interna (piso climatizado + vestíbulo)" if c else "Área interna (piso climatizado)", tot_int), ("Área externa (deck e terraços)", tot_ext),
                                ("Projeção da cobertura", 50.5 if c else 95.5), ("Área total (interna + externa)", tot_int + tot_ext)]):
        sh.text_px(X0 + 40, y + j * 18, k, size=10.5, weight=700 if j == 3 else 400, anchor="start"); sh.text_px(X0 + 380, y + j * 18, fmt(v), size=10.5, weight=700 if j == 3 else 400, anchor="end")
    # notas gerais em duas colunas
    Y1 = y + 4 * 18 + 26
    sh.text_px(X0, Y1, "NOTAS GERAIS", size=12, weight=700, spacing=0.3, anchor="start")
    half = (len(NOTAS) + 1) // 2
    for col in range(2):
        yy = Y1 + 22; xc = X0 + col * 490
        for i, n in enumerate(NOTAS[col * half:(col + 1) * half]):
            words = n.split(); lines = []; cur = ""
            for w in words:
                if len(cur) + len(w) + 1 > 92: lines.append(cur); cur = w
                else: cur = (cur + " " + w).strip()
            lines.append(cur)
            sh.text_px(xc, yy, f"{col * half + i + 1:02d}", size=8.6, weight=700, anchor="start")
            for L in lines:
                sh.text_px(xc + 22, yy, L, size=8.6, anchor="start"); yy += 11.2
            yy += 4
    tb(sh, product, "Capa · índice · áreas · notas", "sem escala", "PA-00", "Projeto arquitetônico · estudo preliminar R00")
    return sh

# ----------------------------------------------------------------------------- PA-01 IMPLANTAÇÃO
def implantacao(product):
    c = product == "cocoon"
    sh = Sheet(1600, 1000, scale=24, ox=560, oy=560)    # 1 m = 24 px (1:200 em A1 aprox.)
    sh.header(f"{NAME[product]} · Planta de situação e implantação", "Implantação genérica de referência · lote 30,00 x 24,00 m · curvas de nível a cada 0,50 m · escala 1:200 · orientação a definir por sítio")
    LX, LY = 30.0, 24.0; x0, y0 = -15.0, -12.0
    # lote e curvas de nível
    sh.rect(x0, y0, x0 + LX, y0 + LY, fill=sh.pattern("grass"), stroke=GREEN, sw=1.4)
    sh.rect(x0, y0, x0 + LX, y0 + LY, fill="none", stroke=GREEN, sw=1.4)
    rng = np.random.default_rng(7)
    for k, lv in enumerate(range(-3, 4)):
        pts = []
        for i in range(41):
            xx = x0 + LX * i / 40
            yy = y0 + LY * 0.5 + lv * 2.6 + 1.2 * math.sin(xx / 4.0 + lv) + 0.5 * math.cos(xx / 2.3)
            pts.append((xx, yy))
        sh.poly([(x, min(max(y, y0), y0 + LY)) for (x, y) in pts], close=False, stroke=EARTH, sw=0.7, dash="6 3", opacity=0.8)
        sh.text(x0 + LX - 0.6, pts[-1][1] + 0.35, f"{100 + lv * 0.5:.1f}".replace(".", ","), 9, EARTH, anchor="end")
    # afastamentos
    sh.rect(x0 + 5, y0 + 5, x0 + LX - 5, y0 + LY - 5, fill="none", stroke=EARTH, sw=0.8, dash="10 5")
    sh.text(x0 + 5.2, y0 + LY - 5.4, "afastamento mínimo 5,00 m (referência)", 9, EARTH, anchor="start")
    # unidade (planta girada: frente para o norte = topo). x do produto aponta para -y do lote
    def P(x, y):  # produto -> lote: frente (x=0) no topo; direita (y<0) do produto à direita do lote
        return (-y, -x + 3.0)
    if c:
        outline, ring = shell_plan_pts()
        sh.poly([P(*p) for p in outline], fill=MEMB, stroke=GREEN, sw=1.4)
        D = C.DECK
        sh.poly([P(D["x1"], D["y1"]), P(D["x2"], D["y1"]), P(D["x2"], D["y2"]), P(D["x1"], D["y2"])], fill=sh.pattern("deck"), stroke=GREEN, sw=1.0)
        sh.poly([P(*p) for p in outline], fill="none", stroke=GREEN, sw=1.4)
        sh.circle(*P(-2.2, -2.0), 0.95, fill="none", stroke=GREEN, sw=0.8, dash="4 3"); sh.text(*P(-2.2, -2.0), "hot tub opc.", 8, GREEN, dy=3)
        cond = P(10.3, 0.0); sh.rect(cond[0] - 0.4, cond[1] - 0.45, cond[0] + 0.4, cond[1] + 0.35, fill="#E5E1D8", stroke=GREEN, sw=0.7); sh.text(cond[0] + 0.6, cond[1] - 0.1, "condensadora", 8, anchor="start")
        tail = P(8.6, 1.4)
    else:
        rb = Z.roof_bounds()
        sh.poly([P(rb[0], rb[2]), P(rb[1], rb[2]), P(rb[1], rb[3]), P(rb[0], rb[3])], fill=MEMB, stroke=GREEN, sw=1.0, dash="8 4", opacity=0.9)
        D, Wk = Z.DECK, Z.WALK
        for R in (D, Wk):
            sh.poly([P(R["x1"], R["y1"]), P(R["x2"], R["y1"]), P(R["x2"], R["y2"]), P(R["x1"], R["y2"])], fill=sh.pattern("deck"), stroke=GREEN, sw=1.0)
        sh.poly([P(0, -2.7), P(9.5, -2.7), P(9.5, 2.7), P(0, 2.7)], fill="#EFE7DA", stroke=GREEN, sw=1.4)
        H = Z.HOTTUB; sh.circle(*P(H["x"], H["y"]), H["r"], fill="#CBDCE0", stroke=GREEN, sw=0.8)
        for p in Z.PEAKS: sh.circle(*P(p["x"], p["y"]), p["r"], fill="none", stroke=GREEN, sw=0.8)
        cond = P(10.25, -1.8); sh.rect(cond[0] - 0.4, cond[1] - 0.4, cond[0] + 0.4, cond[1] + 0.4, fill="#E5E1D8", stroke=GREEN, sw=0.7); sh.text(cond[0] + 0.6, cond[1] - 0.1, "condensadora", 8, anchor="start")
        tail = P(9.5, 1.5)
    # acesso (caminho do portão ao deck), via
    sh.rect(x0, y0 - 3.0, x0 + LX, y0, fill="#E6DED2", stroke=GREEN, sw=0.8); sh.text(x0 + LX / 2, y0 - 1.5, "VIA DE ACESSO INTERNA DO EMPREENDIMENTO", 10, EARTH, spacing=0.2, dy=4)
    ent = P(-3.7 if c else -3.0, 0)
    path = [(x0 + 22.0, y0), (x0 + 22.0, y0 + 3.5), (ent[0] + 6.0, ent[1] - 1.5), (ent[0] + 1.2, ent[1] - 0.6)]
    sh.poly(path, close=False, stroke=EARTH, sw=6, opacity=0.35); sh.poly(path, close=False, stroke=EARTH, sw=1.0, dash="6 4")
    sh.text(x0 + 22.6, y0 + 1.4, "acesso de pedestres 1,20 m (madeira / brita)", 9, EARTH, anchor="start")
    sh.text(x0 + 22.0, y0 - 0.9, "vaga / carrinho elétrico", 8.5, EARTH)
    # fossa e filtro, caixas de brita
    fx, fy = tail[0] - 2.0, y0 + 2.2
    sh.circle(fx, fy, 0.75, fill="#E5E1D8", stroke=GREEN, sw=0.8); sh.circle(fx + 2.0, fy, 0.75, fill="#E5E1D8", stroke=GREEN, sw=0.8)
    sh.text(fx - 1.0, fy - 0.1, "fossa séptica + filtro anaeróbio", 8.5, GREEN, anchor="end"); sh.text(fx - 1.0, fy - 0.5, "(ou estação compacta)", 8, GREEN, anchor="end")
    sh.poly([tail, (fx, fy + 0.75)], close=False, stroke=GREEN, sw=0.8, dash="3 3"); sh.text((tail[0] + fx) / 2 - 0.3, (tail[1] + fy) / 2, "esgoto Ø100 i ≥ 2%", 8, GREEN, anchor="end")
    for (bx, by) in [(ent[0] + 5.0, ent[1] - 1.2), (tail[0] + 3.2, tail[1] + 1.0)]:
        sh.rect(bx - 0.6, by - 0.4, bx + 0.6, by + 0.4, fill=sh.pattern("soil"), stroke=GREEN, sw=0.7); sh.text(bx, by - 0.75, "caixa de brita", 8, GREEN)
    # entrada de água/energia
    sh.line(x0 + 2.2, y0, x0 + 2.2, ent[1] + 2.0, "#4E6E8B", 1.0, dash="8 3"); sh.line(x0 + 2.2, ent[1] + 2.0, ent[0] - 1.0, ent[1] + 2.0, "#4E6E8B", 1.0, dash="8 3")
    sh.text(x0 + 2.6, y0 + 2.0, "água PEX Ø25 + energia 220 V", 8.5, "#4E6E8B", anchor="start", rotate=-90); sh.text(x0 + 3.5, y0 + 2.0, "(rede do empreendimento)", 8, "#4E6E8B", anchor="start", rotate=-90)
    # setas de orientação e vento
    sh.add(f'<g transform="translate({sh.X(x0 + LX + 3.5):.0f},{sh.Y(y0 + LY - 3):.0f})"><circle r="26" fill="none" stroke="{GREEN}" stroke-width="0.8"/><polygon points="0,-23 -7,15 0,8 7,15" fill="{GREEN}"/><text y="-32" text-anchor="middle" style="font-family:{FONT};font-size:11px;font-weight:600" fill="{GREEN}">N</text></g>')
    sh.text(x0 + LX + 3.5, y0 + LY - 6.4, "fachada de vidro voltada", 8.5, EARTH); sh.text(x0 + LX + 3.5, y0 + LY - 6.9, "ao norte / vista", 8.5, EARTH)
    sh.line(x0 + LX + 1.5, y0 + 6, x0 + LX + 5.5, y0 + 6, EARTH, 1.2); sh.text(x0 + LX + 3.5, y0 + 6.4, "vento predominante", 8.5, EARTH); sh.text(x0 + LX + 3.5, y0 + 5.1, "(NE / S, a confirmar)", 8, EARTH)
    sh.text(x0 + LX + 3.5, y0 + 9.5, "sol: nascente à direita,", 8.5, EARTH); sh.text(x0 + LX + 3.5, y0 + 9.0, "poente à esquerda", 8.5, EARTH)
    # cotas do lote e da unidade
    sh.dim(x0, y0 + LY, x0 + LX, y0 + LY, 0.9, label="30,00")
    sh.dim(x0, y0, x0, y0 + LY, -0.9, label="24,00")
    ux = [P(-3.7 if c else -3.0, 0)[1], P(9.6 if c else 9.5, 0)[1]]
    sh.dim(-4.6, ux[1], -4.6, ux[0], 0, label=("13,30" if c else "12,50") + " (deck + cabana)", size=10)
    sh.dim(P(0, 3.25 if c else 3.5)[0], ux[0] + 0.9, P(0, -3.25 if c else -3.5)[0], ux[0] + 0.9, 0, label="6,50" if c else "7,00", size=10)
    sh.text(x0 + 0.4, y0 + LY + 2.2, "LEGENDA:  ▭ deck cumaru   ▭ cobertura / concha   - - - curvas de nível (m)   - - - afastamentos   ○ fossa / filtro   ▦ caixa de brita", 9.5, GREEN, anchor="start")
    sh.scalebar(x0, y0 - 5.6, 10, 2)
    tb(sh, product, "Planta de situação e implantação", "1:200 (A1)", "PA-01", "Implantação genérica de referência para um sítio-tipo de 720 m²")
    return sh

# ----------------------------------------------------------------------------- PA-04 COBERTURA
def cobertura(product):
    c = product == "cocoon"
    if c:
        sh = Sheet(1600, 1000, scale=82, ox=390, oy=520)
        sh.header("Zion Casulo · Planta de cobertura", "Membrana PVDF em 7 painéis entre arcos + tampas; Espinha de Luz; calhas ocultas nos rodapés; tubos de queda Ø75 nas extremidades")
        outline, ring = shell_plan_pts()
        sh.poly(outline, fill=MEMB, stroke=GREEN, sw=1.8)
        D = C.DECK; sh.rect(D["x1"], D["y1"], D["x2"], D["y2"], fill="none", stroke=GREEN, sw=0.8, dash="6 3")
        for i, x in enumerate(C.ARCH_X):
            pts = arch_plan(x); sh.poly(pts, close=False, stroke=GREEN, sw=0.9, dash="2 3")
            sh.text(pts[0][0], pts[0][1] - 0.25, f"A{i}", 9, EARTH)
        x1, x2, ht = C.SPINE; hw = ht * C.B_MAX
        sh.rect(C.shear(x1, 4.15), -hw, C.shear(x2, 4.15), hw, fill=GLASS, stroke=GREEN, sw=1.0)
        for xx in (2.85, 4.05, 5.25): sh.line(C.shear(xx, 4.15), -hw, C.shear(xx, 4.15), hw, GREEN, 0.8)
        sh.text(4.2, 0.0, "CL1 · ESPINHA DE LUZ · 4 x (1,175 x 0,70)", 9, GREEN, spacing=0.1, dy=3)
        # respiro de cumeeira
        sh.rect(7.0, -0.25, 8.2, 0.25, fill="none", stroke=GREEN, sw=0.8, dash="3 2"); sh.text(7.6, 0.0, "respiro", 8, GREEN, dy=3)
        # setas de escoamento
        for xx in [1.4, 3.4, 5.4, 7.4]:
            for s in (1, -1):
                y1 = 0.6 * s; y2 = (C.a(xx) - 0.5) * s
                sh.line(xx, y1, xx, y2, EARTH, 1.0); sh.add(f'<polygon points="{sh.X(xx) - 4},{sh.Y(y2) + (-6 if s > 0 else 6)} {sh.X(xx) + 4},{sh.Y(y2) + (-6 if s > 0 else 6)} {sh.X(xx)},{sh.Y(y2)}" fill="{EARTH}"/>')
                sh.text(xx + 0.15, (y1 + y2) / 2, "i var.", 8, EARTH, anchor="start", rotate=-90)
        # calhas e quedas
        for s in (1, -1):
            pts = [(x, s * (C.floor_hw(x) + 0.08)) for x in np.linspace(0.9, 9.3, 60)]
            sh.poly(pts, close=False, stroke="#4E6E8B", sw=2.2);
        sh.text(5.0, -3.35, "calha oculta 80 x 60 no rodapé (i 0,5% para as extremidades)", 9, "#4E6E8B")
        for (qx, qy) in [(0.95, -2.75), (0.95, 2.75), (9.25, -1.2), (9.25, 1.2)]:
            sh.circle(qx, qy, 0.12, fill="#4E6E8B", stroke="none"); sh.text(qx + (0.25 if qx < 5 else -0.25), qy + 0.3, "TQ Ø75", 8, "#4E6E8B", anchor="start" if qx < 5 else "end")
        # lábio / anel frontal
        sh.poly(ring, close=False, stroke=GREEN, sw=2.2); sh.text(-0.2, -2.6, "lábio frontal: anel A0 inclinado 8°, beiral 0,60 m", 9, GREEN, anchor="start", rotate=-90)
        sh.text(9.0, 3.6, "cauda: tampa cônica de membrana presa no quadro B08", 9, GREEN, anchor="end")
        for w in C.WINDOWS:
            side = -1 if w["tc"] < math.pi / 2 else 1
            pts = [(C.shear(x, 1.6), side * (C.a(x) + 0.03)) for x in np.linspace(w["xc"] - w["lx"], w["xc"] + w["lx"], 8)]
            sh.poly(pts, close=False, stroke=GLASS, sw=5); sh.poly(pts, close=False, stroke=GREEN, sw=0.8)
        sh.dim(0.45, -3.9, 9.6, -3.9, -0.5, label="9,15 (projeção da concha)"); sh.dim(-0.15, -3.9, 9.6, -3.9, -1.1, label="9,75 (com lábio)")
        sh.dim(10.3, -3.0, 10.3, 3.0, 0.6, label="6,00"); sh.dim(C.shear(x1, 4.15), 3.6, C.shear(x2, 4.15), 3.6, 0.5, label="4,70 (espinha)")
        sh.leader(0.5, 2.3, -1.6, 4.5, "membrana PVDF 1050 g/m² · painéis deslizados em perfil duplo keder sobre cada arco", 10, anchor="start")
        sh.leader(2.2, -2.9, 1.0, -4.5, "Janelas Olho: recorte reforçado + clamp no anel E06", 10)
    else:
        sh = Sheet(1600, 1000, scale=82, ox=390, oy=520)
        sh.header("Zion Safari · Planta de cobertura", "Membrana PVDF de dois cumes · curvas de nível a cada 0,40 m · bordas em catenária · pingadeiras nos pontos baixos · calha oculta no anel de beiral")
        rb = Z.roof_bounds()
        sh.rect(rb[0], rb[2], rb[1], rb[3], fill=MEMB, stroke=GREEN, sw=1.8)
        sh.rect(0, -2.7, 9.5, 2.7, fill="none", stroke=GREEN, sw=1.0, dash="6 3")
        contours(sh, levels=(3.0, 3.4, 3.8, 4.2, 4.6, 5.0, 5.4, 5.7), color=EARTH)
        for p in Z.PEAKS:
            sh.circle(p["x"], p["y"], p["r"], fill=GLASS if p["oculus"] else "#E5E1D8", stroke=GREEN, sw=1.2)
            sh.text(p["x"], p["y"] + p["r"] + 0.25, f"{'OC1 · ÓCULO' if p['oculus'] else 'RE1 · CHAMINÉ'} · cume {fmt(p['h'])}", 9, GREEN, spacing=0.05)
        # setas de escoamento (radiais dos cumes)
        for p in Z.PEAKS:
            for k in range(8):
                ang = 2 * math.pi * k / 8; r1 = p["r"] + 0.3; r2 = r1 + 1.1
                ax, ay = p["x"] + r1 * math.cos(ang), p["y"] + r1 * math.sin(ang); bx, by = p["x"] + r2 * math.cos(ang), p["y"] + r2 * math.sin(ang)
                if rb[0] < bx < rb[1] and rb[2] < by < rb[3]:
                    sh.line(ax, ay, bx, by, EARTH, 0.9); sh.circle_px(bx, by, 2.2, fill=EARTH, stroke=EARTH)
        # postes, cabos de borda e pingadeiras
        for (px, py) in Z.posts(): sh.circle(px, py, 0.1, fill=STEEL, stroke="none")
        x0, x1, y0, y1 = rb
        for (ax, ay, bx, by) in [(x0, y0, x0, y1), (x1, y0, x1, 0), (x1, 0, x1, y1), (x0, y0, 4.0, y0), (4.0, y0, x1, y0), (x0, y1, 4.0, y1), (4.0, y1, x1, y1)]:
            mx, my = (ax + bx) / 2, (ay + by) / 2
            inward = (0.35 if ax == bx and ax < 0 else -0.28 if ax == bx else 0, 0.3 if ay == by and ay < 0 else -0.3 if ay == by else 0)
            sh.add(f'<path d="M{sh.X(ax):.1f},{sh.Y(ay):.1f} Q{sh.X(mx + inward[0]):.1f},{sh.Y(my + inward[1]):.1f} {sh.X(bx):.1f},{sh.Y(by):.1f}" fill="none" stroke="{GREEN}" stroke-width="1.6"/>')
            sh.circle(mx + inward[0] / 2, my + inward[1] / 2, 0.1, fill="#4E6E8B", stroke="none")
        sh.text(4.0, y0 - 0.45, "pingadeiras nos pontos baixos das catenárias sobre canaletas de brita", 9, "#4E6E8B")
        # calha oculta no anel de beiral (laterais) e quedas nos pilares
        sh.line(0, -2.78, 9.5, -2.78, "#4E6E8B", 2.2); sh.line(0, 2.78, 9.5, 2.78, "#4E6E8B", 2.2)
        for (qx, qy) in [(3.2, -2.7), (6.4, 2.7)]:
            sh.circle(qx, qy, 0.12, fill="#4E6E8B", stroke="none"); sh.text(qx, qy + (-0.45 if qy < 0 else 0.4), "TQ Ø75 no pilar", 8, "#4E6E8B")
        sh.text(4.75, 3.15, "calha oculta no perfil de borda do anel de beiral", 9, "#4E6E8B")
        sh.dim(x0, y1 + 0.3, x1, y1 + 0.3, 0.9, label="12,90"); sh.dim(0, y1 + 0.3, 9.5, y1 + 0.3, 0.35, label="9,50 (corpo)"); sh.dim(x0, y1 + 0.3, 0, y1 + 0.3, 0.35, label="2,40")
        sh.dim(x1 + 0.6, y0, x1 + 0.6, y1, 0.5, label="7,40"); sh.dim(x1 + 0.6, -2.7, x1 + 0.6, 2.7, 1.2, label="5,40")
        sh.leader(2.0, -2.2, -3.3, -5.05, "membrana PVDF 1050 g/m² em gomos radiais soldados por RF; i mín. 14° no vale", 10, anchor="start")
        sh.leader(x0, y0 + 1.2, -3.3, -4.6, "cabo de borda Ø12 inox em bolsa; postes PE inclinados 8°", 10, anchor="start")
    sh.north(1500, 140, angle=-90); sh.scalebar(-3.7 if c else 2.0, -5.6, 5)
    tb(sh, product, "Planta de cobertura", "1:50 (A1)", "PA-04", "Escoamento, calhas, tubos de queda, claraboia / óculo e respiros")
    return sh

# ----------------------------------------------------------------------------- PA-05 FORRO E ILUMINAÇÃO
def forro(product):
    c = product == "cocoon"
    sh = Sheet(1600, 1000, scale=82, ox=390, oy=520)
    sh.header(f"{NAME[product]} · Planta de forro refletido e iluminação", "Forro tensionado, difusores, fitas LED 2700 K, luminárias, arandelas, balizadores e pontos de comando · sem pendentes (padrão Zion)")
    def led(pts, label=None):
        sh.poly(pts, close=False, stroke="#C9A84C", sw=2.4, dash="7 4")
    def down(x, y, n=""):
        sh.circle(x, y, 0.09, fill="none", stroke=GREEN, sw=0.9); sh.line(x - 0.12, y, x + 0.12, y, GREEN, 0.7); sh.line(x, y - 0.12, x, y + 0.12, GREEN, 0.7)
    def arand(x, y): sh.rect(x - 0.1, y - 0.06, x + 0.1, y + 0.06, fill=GREEN, stroke="none")
    def baliz(x, y): sh.circle(x, y, 0.07, fill="#C9A84C", stroke=GREEN, sw=0.6)
    def switch(x, y, lbl): sh.text(x, y, lbl, 9, GREEN, weight=700, dy=3)
    if c:
        outline, ring = shell_plan_pts(); floor = C.floor_outline(100)
        sh.poly(outline, fill="none", stroke=GREEN, sw=1.2, dash="6 3")
        sh.poly(floor, fill="#F3EDE3", stroke=GREEN, sw=1.0)
        D = C.DECK; sh.rect(D["x1"], D["y1"], D["x2"], D["y2"], fill="none", stroke=GREEN, sw=0.8)
        # forro tensionado (hachura leve) e forro plano do banho
        sh.poly([p for p in floor if 0.9 <= p[0] <= 6.6] , fill=sh.pattern("insul"), stroke="none", opacity=0.5)
        sh.poly([p for p in floor if p[0] >= 6.7], fill="#E8E6E0", stroke=GREEN, sw=0.8)
        sh.text(7.9, -2.0, "forro plano 2,40 (ático técnico acima)", 8.5, GREEN)
        sh.text(3.6, 2.3, "forro tensionado acústico seguindo a concha (h 4,15 no eixo)", 9, GREEN)
        x1, x2, ht = C.SPINE; hw = ht * C.B_MAX
        sh.rect(C.shear(x1, 4.15), -hw, C.shear(x2, 4.15), hw, fill=GLASS, stroke=GREEN, sw=0.9); sh.text(4.2, 0.0, "CL1 claraboia", 8.5, GREEN, dy=3)
        led([(C.shear(x1, 4.15), -hw - 0.12), (C.shear(x2, 4.15), -hw - 0.12)]); led([(C.shear(x1, 4.15), hw + 0.12), (C.shear(x2, 4.15), hw + 0.12)])
        # LED rodapé (perímetro interno)
        led([(x, -(C.floor_hw(x) - 0.12)) for x in np.linspace(1.0, 9.2, 50)]); led([(x, (C.floor_hw(x) - 0.12)) for x in np.linspace(1.0, 9.2, 50)])
        # LED nos requadros das janelas
        for w in C.WINDOWS:
            side = -1 if w["tc"] < math.pi / 2 else 1
            led([(w["xc"] - w["lx"], side * (C.a(w["xc"]) - 0.35)), (w["xc"] + w["lx"], side * (C.a(w["xc"]) - 0.35))])
        # difusores lineares, retorno
        for (x, y1, y2) in [(6.56, -1.2, 0.9), (0.95, -1.4, -0.2)]:
            sh.rect(x - 0.05, y1, x + 0.05, y2, fill=GREEN, stroke="none"); sh.text(x + 0.25, (y1 + y2) / 2, "difusor linear", 8, GREEN, anchor="start", rotate=-90)
        sh.rect(7.2, 0.4, 7.9, 0.9, fill="none", stroke=GREEN, sw=0.9); sh.text(7.55, 0.65, "retorno", 8, GREEN, dy=3)
        # luminárias do banho, exaustor, arandelas, balizadores
        for (x, y) in [(7.0, -1.2), (8.0, -1.2), (7.5, 1.3)]: down(x, y)
        sh.rect(8.1, 1.0, 8.5, 1.4, fill="none", stroke=GREEN, sw=0.9, dash="2 2"); sh.text(8.3, 1.65, "exaustor", 8, GREEN)
        arand(6.5, 1.35); arand(6.5, -1.35); sh.text(6.2, 1.75, "arandelas de leitura", 8, GREEN)
        for (x, y) in [(-3.4, -3.0), (-3.4, 3.0), (-0.5, -3.0), (-0.5, 3.0), (-3.4, 0)]: baliz(x, y)
        sh.text(-2.0, 3.45, "balizadores LED no deck", 8.5, GREEN)
        sh.text(2.3, -0.9, "luz rasante da espinha", 8, GREEN)
        switch(1.2, 1.4, "a"); switch(6.3, -1.75, "b"); switch(6.9, 2.05, "c"); switch(1.05, -1.9, "d")
        sh.dim(0.9, 3.7, 6.6, 3.7, 0.5, label="5,70 forro tensionado"); sh.dim(6.7, 3.7, 9.4, 3.7, 0.5, label="2,70 forro plano")
        legend = [("- - - dourado", "fita LED 2700 K em perfil de alumínio (rodapés, requadros, espinha)"), ("⊕", "luminária embutida IP44 (banho)"), ("▬", "arandela de leitura orientável"), ("▭ preto", "difusor linear do ar-condicionado"), ("●", "balizador LED de deck"), ("a b c d", "comandos: a estar (LED + geral) · b cabeceira (cena noite) · c banho · d deck")]
        for i, (s, t) in enumerate(legend):
            sh.text_px(60, 840 + i * 18, s, size=9.5, weight=700, anchor="start"); sh.text_px(150, 840 + i * 18, t, size=9.5, anchor="start")
    else:
        rb = Z.roof_bounds()
        sh.rect(rb[0], rb[2], rb[1], rb[3], fill="none", stroke=GREEN, sw=0.8, dash="6 3")
        sh.rect(0.1, -2.6, 9.4, 2.6, fill="#F3EDE3", stroke=GREEN, sw=1.2)
        sh.rect(0.1, -2.6, 6.45, 2.6, fill=sh.pattern("insul"), stroke="none", opacity=0.5)
        sh.rect(6.45, -2.6, 9.4, 2.6, fill="#E8E6E0", stroke=GREEN, sw=0.8); sh.text(7.9, -2.0, "forro plano 2,50 (ático técnico acima)", 8.5, GREEN)
        contours(sh, levels=(3.2, 3.6, 4.0, 4.4, 4.8, 5.2), color=EARTH)
        sh.text(3.2, 2.2, "forro tensionado seguindo os cumes (curvas a cada 0,40 m, -0,30 m da membrana)", 9, GREEN)
        p1, p2 = Z.PEAKS
        sh.circle(p1["x"], p1["y"], p1["r"], fill=GLASS, stroke=GREEN, sw=1.0); sh.text(p1["x"] - 0.85, p1["y"] - 0.95, "OC1 óculo + anel LED", 8.5, GREEN, anchor="end")
        sh.circle(p2["x"], p2["y"], p2["r"], fill="#E5E1D8", stroke=GREEN, sw=1.0); sh.text(p2["x"], p2["y"] - 0.65, "RE1 chaminé", 8.5, GREEN)
        led([(p1["x"] + (p1["r"] + 0.12) * math.cos(a), p1["y"] + (p1["r"] + 0.12) * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 40)])
        # LED perímetro no anel de beiral e rodapé
        led([(0.2, -2.5), (9.3, -2.5)]); led([(0.2, 2.5), (9.3, 2.5)]); led([(0.2, -2.5), (0.2, 2.5)]); led([(9.3, -2.5), (9.3, 2.5)])
        sh.text(4.75, -2.85, "fita LED contínua no perfil do anel de beiral (luz indireta no forro) + rodapé", 8.5, GREEN)
        D = Z.DECK; sh.rect(D["x1"], D["y1"], D["x2"], D["y2"], fill="none", stroke=GREEN, sw=0.8); sh.rect(0, 2.7, 9.5, 3.5, fill="none", stroke=GREEN, sw=0.8)
        H = Z.HOTTUB; sh.circle(H["x"], H["y"], H["r"], fill="none", stroke=GREEN, sw=0.8, dash="3 2")
        for (x, y1, y2) in [(6.52, -1.2, 1.0), (3.5, 2.55, 0.9)]:
            sh.rect(x - 0.05, y1, x + 0.05, y2, fill=GREEN, stroke="none")
        sh.text(6.75, -0.1, "difusor linear", 8, GREEN, anchor="start", rotate=-90); sh.text(3.72, 1.7, "difusor linear (estar)", 8, GREEN, anchor="start", rotate=-90)
        sh.rect(7.3, 0.6, 8.0, 1.1, fill="none", stroke=GREEN, sw=0.9); sh.text(7.65, 0.85, "retorno", 8, GREEN, dy=3)
        for (x, y) in [(6.9, -1.1), (7.9, -2.0), (8.9, -2.0), (8.9, 0.4), (7.9, 1.9)]: down(x, y)
        sh.rect(8.6, -1.2, 9.0, -0.8, fill="none", stroke=GREEN, sw=0.9, dash="2 2"); sh.text(8.8, -0.55, "exaustor", 8, GREEN)
        arand(6.35, 1.3); arand(6.35, -1.3); arand(0.35, -2.1); sh.text(5.9, 1.7, "arandelas", 8, GREEN)
        led([(0.6, 2.05), (2.6, 2.05)]); sh.text(1.6, 1.85, "LED sob a bancada do café", 8, GREEN)
        led([(3.8, 1.95), (5.8, 1.95)]); sh.text(4.8, 1.75, "LED no closet", 8, GREEN)
        for (x, y) in [(-2.7, -3.1), (-2.7, 3.1), (-0.4, -3.1), (-0.4, 3.1), (2.5, 3.25), (5.0, 3.25), (7.5, 3.25), (-2.7, 0)]: baliz(x, y)
        sh.text(-1.5, 3.9, "balizadores LED (terraço e passarela)", 8.5, GREEN)
        switch(0.5, 1.4, "a"); switch(6.1, -1.9, "b"); switch(6.8, 2.2, "c"); switch(0.4, -2.35, "d")
        sh.dim(0.1, 4.1, 6.45, 4.1, 0.5, label="6,35 forro tensionado"); sh.dim(6.45, 4.1, 9.4, 4.1, 0.5, label="2,95 forro plano")
        legend = [("- - - dourado", "fita LED 2700 K em perfil de alumínio (anel de beiral, rodapés, óculo, bancadas)"), ("⊕", "luminária embutida IP44 (banho)"), ("▬", "arandela de leitura / passagem"), ("▭ preto", "difusor linear do ar-condicionado"), ("●", "balizador LED de deck"), ("a b c d", "comandos: a estar · b cabeceira (cena noite, motor da chaminé) · c banho · d terraço / hidromassagem")]
        for i, (s, t) in enumerate(legend):
            sh.text_px(60, 840 + i * 18, s, size=9.5, weight=700, anchor="start"); sh.text_px(150, 840 + i * 18, t, size=9.5, anchor="start")
    sh.north(1500, 140, angle=-90); sh.scalebar(-3.7 if c else -3.0, -5.6, 5)
    tb(sh, product, "Planta de forro refletido e iluminação", "1:50 (A1)", "PA-05", "Forro tensionado + forro plano do banho; iluminação indireta 2700 K; difusores; comandos")
    return sh

# ----------------------------------------------------------------------------- PA-08b FACHADA LATERAL ESQUERDA
def fachada_esquerda(product):
    c = product == "cocoon"
    if c:
        sh = Sheet(1600, 1000, scale=100, ox=1130, oy=720, flip_x=True)   # olhar para -y: frente à direita
        sh.header("Zion Casulo · Fachada lateral esquerda", "Vista do lado do café e do closet (olhar para -y, frente à direita) · Janelas Olho JO2, JO3 e JO5 · condensadora à esquerda")
        sh.rect(-4.0, -0.6, 11.0, -0.02, fill=sh.pattern("soil"), stroke="none"); sh.line(-4.0, -0.02, 11.0, -0.02, GREEN, 1.0)
        for px in [-3.3, -1.1, 0.9, 2.1, 3.3, 4.5, 5.7, 6.9, 8.1, 9.0]: sh.rect(px - 0.04, -0.6, px + 0.04, -0.2, fill=STEEL, stroke="none")
        sh.rect(-3.7, -0.2, 9.6, -0.05, fill=WOOD2, stroke=GREEN, sw=0.9); sh.rect(-3.7, -0.05, 9.6, 0.0, fill=GREEN, stroke="none")
        for i in range(3): sh.rect(-3.7 - 0.3 * (i + 1), -0.2 + 0.05 * (i + 1) - 0.15, -3.7 - 0.3 * i, -0.2 + 0.05 * (i + 1), fill=WOOD2, stroke=GREEN, sw=0.7)
        top = top_profile(); bot = bottom_profile(); sh.poly(top + bot[::-1], fill=MEMB, stroke=GREEN, sw=1.8)
        for x in C.ARCH_X[1:]: sh.line(C.shear(x, 0), 0, C.shear(x, C.top(x)), C.top(x), EARTH, 0.6, dash="4 4", opacity=0.6)
        sh.line(0.45, 0, C.shear(0.45, 4.13), 4.13, GREEN, 2.0)
        sh.line(0.9, 0, C.shear(0.9, 4.15), 4.15, GLASS, 5); sh.line(0.9, 0, C.shear(0.9, 4.15), 4.15, GREEN, 0.9)
        x1, x2, _ = C.SPINE; spine = [(C.shear(x, C.top(x)), C.top(x)) for x in np.linspace(x1, x2, 30)]
        sh.poly(spine, close=False, stroke=GLASS, sw=6); sh.poly(spine, close=False, stroke=GREEN, sw=0.8)
        labels = {"Olho estar (esq.)": "JO2 1,60 x 0,95", "Olho suíte (esq.)": "JO3 1,40 x 0,80", "Olho banheira (esq.)": "JO5 0,90 x 0,50"}
        for w in C.WINDOWS:
            if w["tc"] < math.pi / 2: continue
            pts = [(x, z) for (x, y, z) in C.window_outline(w, 48)]
            sh.poly([(x, z) for (x, y, z) in C.window_outline(dict(w, lx=w["lx"] + 0.11, lt=w["lt"] + 0.03), 48)], fill="none", stroke=WOOD2, sw=3)
            sh.poly(pts, fill=GLASS, stroke=GREEN, sw=1.0)
            cx = sum(p[0] for p in pts) / len(pts); cz = max(p[1] for p in pts)
            sh.text(cx, cz + 0.2, labels[w["name"]], 9.5, GREEN)
        sh.rect(9.95, 0.0, 10.7, 0.62, fill="#E5E1D8", stroke=GREEN, sw=0.8)
        for xx in [10.0 + 0.12 * i for i in range(6)]: sh.line(xx, 0.0, xx, 1.3, WOOD2, 2.2)
        sh.leader(3.4, 4.2, 4.6, 4.85, "cumeeira 4,20 · Espinha de Luz CL1", 12, anchor="end")
        sh.leader(0.05, 3.5, 1.6, 4.4, "lábio frontal A0 · PV1 e V1 na fachada", 12, anchor="end")
        sh.leader(10.4, 0.8, 9.8, 2.6, "painel ripado da condensadora", 12, anchor="start")
        sh.leader(6.4, 0.35, 6.9, -1.0, "calha oculta no rodapé · TQ Ø75 nas extremidades", 12, anchor="end")
        sh.dim(0.45, -0.95, 9.6, -0.95, -0.35, label="9,60 (piso)"); sh.dim(-3.7, -0.95, 0.9, -0.95, -0.35, label="4,60 (deck)"); sh.dim(-0.15, -0.95, 9.6, -0.95, -0.95, label="9,75 (concha com lábio)")
        sh.dim(11.0, 0, 11.0, 4.2, -0.4, label="4,20"); sh.dim(-4.1, -0.6, -4.1, 0, 0.3, label="0,60")
        sh.text(-4.4, 4.5, "+4,20", 10, EARTH, anchor="end"); sh.text(-4.4, 0.12, "+0,00", 10, EARTH, anchor="end"); sh.text(-4.4, -0.5, "-0,60", 10, EARTH, anchor="end")
        sh.scalebar(11.0, -2.5, 5)
    else:
        sh = Sheet(1600, 1000, scale=96, ox=1130, oy=730, flip_x=True)
        sh.header("Zion Safari · Fachada lateral esquerda", "Vista da passarela e dos painéis ripados (olhar para -y, frente à direita) · J1 janela do café · J2 fresta do closet · postes PE02 / PE06 / PE04")
        ground(sh, -4.5, 12.0)
        for px in [-2.6, -0.2, 2.2, 4.6, 7.0, 9.4]: sh.rect(px - 0.04, -0.6, px + 0.04, -0.2, fill=STEEL, stroke="none")
        sh.rect(-3.0, -0.2, 9.5, -0.05, fill=WOOD2, stroke=GREEN, sw=0.9); sh.rect(-3.0, -0.05, 9.5, 0.0, fill=GREEN, stroke="none")
        for i in range(3): sh.rect(-3.0 - 0.3 * (i + 1), -0.2 + 0.05 * (i + 1) - 0.15, -3.0 - 0.3 * i, -0.2 + 0.05 * (i + 1), fill=WOOD2, stroke=GREEN, sw=0.7)
        x0, x1, y0, y1 = Z.roof_bounds()
        sil = Z.silhouette_side(160); side_edge = [(x, Z.edge_height(x, y1)) for x in np.linspace(x0, x1, 80)]
        sh.poly(sil + side_edge[::-1], fill=MEMB, stroke=GREEN, sw=1.8)
        sh.rect(0, 0, 9.5, 2.75, fill="#C9B08C", stroke=GREEN, sw=1.0); slats(sh, 0.04, 9.5, 0, 2.75)
        sh.rect(0.5, 1.1, 2.7, 2.2, fill=GLASS, stroke=GREEN, sw=0.9); sh.text(1.6, 2.35, "J1 2,20 x 1,10", 9.5, GREEN)
        sh.rect(3.9, 1.9, 5.9, 2.4, fill=GLASS, stroke=GREEN, sw=0.9); sh.text(4.9, 2.55, "J2 2,00 x 0,50", 9.5, GREEN)
        sh.rect(0, 2.75, 9.5, 2.9, fill=STEEL, stroke=GREEN, sw=0.6)
        for px in (x0, 4.0, x1):
            sh.line(px, -0.05, px, Z.edge_height(px, y1), STEEL, 4)
        for p in Z.PEAKS:
            sh.line(p["x"], 0, p["x"], p["mast_top"], STEEL, 1.0, dash="6 4", opacity=0.6); sh.circle(p["x"], p["h"], 0.08, fill="none", stroke=GREEN, sw=0.8)
        sh.rect(9.85, 0.0, 10.65, 0.62, fill="#E5E1D8", stroke=GREEN, sw=0.8); slats(sh, 9.8, 10.7, 0, 1.3, 0.1)
        sh.leader(6.3, 5.8, 5.0, 6.35, "cume principal 5,80 (OC1)", 12, anchor="end"); sh.leader(1.6, 4.6, 0.6, 5.5, "cume secundário 4,60 (RE1)", 12, anchor="end")
        sh.leader(-1.5, 2.3, -2.2, 3.6, "balanço 2,40 sobre o terraço", 12, anchor="start")
        sh.leader(7.5, 1.2, 8.5, -1.1, "painel SIP 100 mm + ripado termotratado 40 x 40", 12, anchor="start")
        sh.leader(4.0, 2.0, 5.6, -1.1, "poste externo PE06 estaiado", 12, anchor="start")
        sh.dim(0, -0.95, 9.5, -0.95, -0.35, label="9,50 (corpo)"); sh.dim(-3.0, -0.95, 0, -0.95, -0.35, label="3,00 (terraço)"); sh.dim(x0, -0.95, x1, -0.95, -0.95, label="12,90 (cobertura)")
        sh.dim(11.3, 0, 11.3, 5.8, -0.4, label="5,80"); sh.dim(-4.1, 0, -4.1, 2.9, 0.3, label="2,90 (beiral)")
        sh.text(-4.6, 5.95, "+5,80", 10, EARTH, anchor="end"); sh.text(-4.6, 0.12, "+0,00", 10, EARTH, anchor="end"); sh.text(-4.6, -0.5, "-0,60", 10, EARTH, anchor="end")
        sh.scalebar(11.5, -2.4, 5)
    tb(sh, product, "Fachada lateral esquerda", "1:50 (A1)", "PA-08b", "Complementa a fachada lateral direita (PA-08a)")
    return sh

# ----------------------------------------------------------------------------- PA-09 QUADRO DE ESQUADRIAS
def esquadrias(product):
    c = product == "cocoon"
    sh = Sheet(1600, 1000, scale=50, ox=60, oy=560)
    sh.header(f"{NAME[product]} · Quadro de esquadrias", "Vistas externas em 1:50 · dimensões em metros (largura x altura) · vidro insulado 6 lam + 12 Ar + 6 temp low-e · alumínio bronze com ruptura térmica")
    E = ESQUADRIAS[product]
    # mini elevações
    X = 1.2; Y = 3.6
    for i, (cod, nome, w, h, q, spec, local) in enumerate(E):
        if X + w > 26.5: X = 1.2; Y = -1.0
        base = Y
        if cod.startswith("JO"):
            pts = []
            for k in range(48):
                a = 2 * math.pi * k / 48; r = (abs(math.cos(a)) ** 1.5 + abs(math.sin(a)) ** 1.5) ** (-1 / 1.5)
                pts.append((X + w / 2 + w / 2 * r * math.cos(a), base + h / 2 + h / 2 * r * math.sin(a)))
            sh.poly(pts, fill=GLASS, stroke=GREEN, sw=1.2)
            pts2 = [(X + w / 2 + (w / 2 + 0.11) * ((abs(math.cos(a)) ** 1.5 + abs(math.sin(a)) ** 1.5) ** (-1 / 1.5)) * math.cos(a), base + h / 2 + (h / 2 + 0.11) * ((abs(math.cos(a)) ** 1.5 + abs(math.sin(a)) ** 1.5) ** (-1 / 1.5)) * math.sin(a)) for a in [2 * math.pi * k / 48 for k in range(48)]]
            sh.poly(pts2, fill="none", stroke=WOOD2, sw=3)
            if "basculante" in nome: sh.poly([(X + 0.1, base + 0.15), (X + w / 2, base + h - 0.12), (X + w - 0.1, base + 0.15)], close=False, stroke=GREEN, sw=0.6, dash="3 2")
        elif cod in ("OC1", "RE1"):
            sh.circle(X + w / 2, base + h / 2, w / 2, fill=GLASS if cod == "OC1" else "#E5E1D8", stroke=GREEN, sw=1.2)
            if cod == "RE1":
                for k in range(5): sh.line(X + 0.1, base + 0.12 + k * 0.12, X + w - 0.1, base + 0.12 + k * 0.12, GREEN, 0.7)
        elif cod == "V1":
            ring = [(-y + w / 2 + X, z) for (xx, y, z) in C.glass_ring(64)]
            sh.poly([(p[0], max(p[1], 0) + base) for p in ring], fill=GLASS, stroke=GREEN, sw=1.2)
            for yy in (-1.6, -0.5, 0.5, 1.6):
                zt = C.ZC + (C.b(C.X_GLASS) - 0.06) * math.sqrt(max(0, 1 - (yy / (C.a(C.X_GLASS) - 0.06)) ** 2)); sh.line(X + w / 2 + yy, base, X + w / 2 + yy, base + zt, GREEN, 1.0)
            sh.line(X + w / 2 - 2.3, base + 2.4, X + w / 2 + 2.3, base + 2.4, GREEN, 1.0)
            sh.rect(X + w / 2 - 1.6, base, X + w / 2 - 0.6, base + 2.4, fill="none", stroke=GREEN, sw=1.6); sh.text(X + w / 2 - 1.1, base + 1.2, "PV1", 9, GREEN)
        else:
            sh.rect(X, base, X + w, base + h, fill=GLASS if cod not in ("PC1", "PC2") or product == "zenith" and cod == "PC1" else WOOD, stroke=GREEN, sw=1.2)
            if cod == "PC1" and product == "zenith":
                for k in range(1, 4): sh.line(X + w * k / 4, base, X + w * k / 4, base + h, GREEN, 1.0)
                sh.add(f'<path d="M{sh.X(X + w * 0.3):.1f},{sh.Y(base + 0.35):.1f} l-10,-5 v10 z" fill="{GREEN}"/><path d="M{sh.X(X + w * 0.7):.1f},{sh.Y(base + 0.35):.1f} l10,-5 v10 z" fill="{GREEN}"/>')
            if cod == "VF1": pass
            if cod in ("J2", "J4"): sh.poly([(X + 0.1, base + 0.08), (X + w / 2, base + h - 0.08), (X + w - 0.1, base + 0.08)], close=False, stroke=GREEN, sw=0.6, dash="3 2")
            if cod in ("PC1", "PC2") and not (product == "zenith" and cod == "PC1"):
                sh.add(f'<path d="M{sh.X(X + w * 0.6):.1f},{sh.Y(base + 1.05):.1f} l10,-5 v10 z" fill="{GREEN}"/>'); sh.rect(X, base, X + w, base + h, fill=sh.pattern("wood"), stroke=GREEN, sw=1.2)
        sh.dim(X, base, X + w, base, -0.35, label=fmt(w), size=10); sh.dim(X + w, base, X + w, base + h, 0.35, label=fmt(h), size=10)
        sh.text(X + w / 2, base + h + 0.45, f"{cod} · {q} un.", 11, GREEN, weight=700)
        X += w + 1.9
    # tabela
    X0, Y0 = 60, 668
    cols = [("Cód.", 0), ("Esquadria", 60), ("L x H (m)", 400), ("Qtd", 500), ("Especificação", 550), ("Localização", 1150)]
    for h_, dx in cols: sh.text_px(X0 + dx, Y0, h_.upper(), size=9, spacing=0.15, fill=EARTH, anchor="start")
    sh.add(f'<line x1="{X0}" y1="{Y0 + 6}" x2="{X0 + 1480}" y2="{Y0 + 6}" stroke="{GREEN}" stroke-width="0.8"/>')
    for i, (cod, nome, w, h, q, spec, local) in enumerate(E):
        y = Y0 + 24 + i * 19
        sh.text_px(X0, y, cod, size=10, weight=700, anchor="start"); sh.text_px(X0 + 60, y, nome, size=10, anchor="start"); sh.text_px(X0 + 400, y, f"{fmt(w)} x {fmt(h)}", size=10, anchor="start")
        sh.text_px(X0 + 500, y, str(q), size=10, anchor="start"); sh.text_px(X0 + 550, y, spec, size=9.5, anchor="start"); sh.text_px(X0 + 1150, y, local, size=9.5, fill=EARTH, anchor="start")
        sh.add(f'<line x1="{X0}" y1="{y + 6}" x2="{X0 + 1480}" y2="{y + 6}" stroke="{SAND}" stroke-width="0.5"/>')
    tb(sh, product, "Quadro de esquadrias", "1:50 (A1)", "PA-09", f"{len(E)} tipos · {sum(e[4] for e in E)} unidades")
    return sh

def build():
    for product in ("cocoon", "zenith"):
        os.makedirs(OUT[product], exist_ok=True)
        capa(product).save(os.path.join(OUT[product], "PA-00_capa_indice_areas_notas.svg"))
        implantacao(product).save(os.path.join(OUT[product], "PA-01_implantacao.svg"))
        cobertura(product).save(os.path.join(OUT[product], "PA-04_planta_cobertura.svg"))
        forro(product).save(os.path.join(OUT[product], "PA-05_forro_iluminacao.svg"))
        fachada_esquerda(product).save(os.path.join(OUT[product], "PA-08b_fachada_lateral_esquerda.svg"))
        esquadrias(product).save(os.path.join(OUT[product], "PA-09_quadro_esquadrias.svg"))
    print("pranchas PA ok")

if __name__ == "__main__":
    build()

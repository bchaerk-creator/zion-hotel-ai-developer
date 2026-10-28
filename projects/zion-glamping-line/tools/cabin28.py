# -*- coding: utf-8 -*-
"""CABIN 28 · cabana em light steel frame (LSF) 4 x 7 m · opção A "Linear" do handoff de 16/10/2026.
Geometria única + desenhos SVG (arquitetura, painéis LSF, plataforma, cobertura, detalhes, hidráulica, esgoto, elétrica, etapas de montagem).
Unidade: metros nas coordenadas; milímetros nos perfis. Origem: canto externo fundo / lado alto (x ao longo dos 7 m, y ao longo dos 4 m, z do piso acabado).
Sem preços. Tudo que depende de cálculo ou norma está marcado para validação."""
import math, os
from svgkit import Sheet, CREAM, GREEN, SAND, EARTH, WOOD, WOOD2, TILE, GLASS, MEMB, STEEL, fmt, iso_project

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "09_CABIN", "desenhos"); os.makedirs(OUT, exist_ok=True)
DATE = "OUT 2026"
PROD = "ZION CABIN 28 · LSF"

# ------------------------------------------------------------------------------------------------- geometria
LX, LY = 7.00, 4.00                      # medida externa (lado de fora das paredes)
TE = 0.15                                # parede externa total: revest. 10 + câmara 25 + OSB 11,1 + perfil 90 + gesso 12,5
TI = 0.115                               # parede interna: gesso 12,5 + perfil 90 + gesso 12,5
FO = 0.046                               # face externa do perfil (revestimento 10 + câmara 25 + OSB 11)
FI = FO + 0.090                          # face interna do perfil
IX0, IX1, IY0, IY1 = TE, LX - TE, TE, LY - TE   # faces internas acabadas: 0,15..6,85 x 0,15..3,85  → 6,70 x 3,70
H_HI, H_LO = 2.80, 2.20                  # topo das guias superiores: lado alto (y = 0) e lado baixo (y = 4)
BEIRAL_Y, BEIRAL_X = 0.35, 0.30          # beirais laterais (nas vigas) e de frente / fundo
STEP = 0.40                              # modulação: vigas de piso, montantes e vigas de cobertura alinhados (in-line framing)
GRID = [round(0.20 + STEP * k, 3) for k in range(17)]   # 0,20 … 6,60
SLOPE = (H_HI - H_LO) / (LY - 2 * FO)    # queda do telhado por metro (sobre o eixo das guias)
ANG = math.degrees(math.atan(SLOPE))

def ztop(y):
    """topo da guia superior / face inferior da viga de cobertura em y (plano inclinado do telhado)."""
    return H_HI - SLOPE * (y - FO)

# núcleo (banho + cozinha) no fundo, parede molhada compartilhada
BATH = dict(x0=IX0, x1=IX0 + 1.60, y0=IY0, y1=IY0 + 2.00)             # 1,60 x 2,00 interno
WET_Y0, WET_Y1 = BATH["y1"], BATH["y1"] + TI                            # parede molhada P-I01 (y 2,15 … 2,265)
KIT = dict(x0=IX0, x1=IX0 + 1.60, y0=WET_Y1, y1=IY1)                    # 1,60 x 1,585 interno (aberta para a sala)
PI2_X0, PI2_X1 = BATH["x1"], BATH["x1"] + TI                            # parede do banho para a sala P-I02 (x 1,75 … 1,865)

# aberturas (código, parede, posição ao longo da parede, largura, peitoril, altura)
OPEN = [
    dict(cod="J1", wall="E01", a0=1.00, w=0.60, sill=1.50, h=0.60, tipo="Maxim-ar 600 x 600", amb="Banho"),
    dict(cod="J2", wall="E01", a0=2.45, w=1.20, sill=1.15, h=0.60, tipo="Correr 2 folhas 1200 x 600", amb="Cozinha"),
    dict(cod="J3", wall="E05", a0=1.90, w=1.20, sill=0.90, h=1.00, tipo="Correr 2 folhas 1200 x 1000", amb="Quarto (lado baixo)"),
    dict(cod="J4", wall="E02", a0=1.80, w=1.20, sill=1.85, h=0.50, tipo="Fixa alta 1200 x 500", amb="Quarto (lado alto)"),
    dict(cod="P1", wall="E03", a0=2.05, w=0.90, sill=0.00, h=2.10, tipo="Porta de abrir 900 x 2100, folha maciça, com visor", amb="Entrada lateral"),
    dict(cod="V1", wall="E04", a0=0.204, w=3.50, sill=0.00, h=None, tipo="Fachada de vidro 3,50 m: correr 2 folhas 1800 x 2200 + fixos laterais 850 + bandeira fixa até o telhado", amb="Frente / deck"),
    dict(cod="P2", wall="I02", a0=0.40, w=0.70, sill=0.00, h=2.10, tipo="Porta de abrir 700 x 2100", amb="Banho"),
]

# painéis de parede: cod, descrição, (x0,y0)-(x1,y1) do eixo do perfil, comprimento do quadro, altura(s), lado
def panels():
    P = []
    # externos (quadro de 90 mm entre FO e FI). Fundo e frente têm 3,908 m; laterais 2 x 3,364 m entre eles.
    yA, yB = FO + 0.045, LY - FO - 0.045          # eixo das paredes laterais
    L_short = LY - 2 * FO                          # 3,908
    xm = LX / 2
    P.append(dict(cod="P-E01", nome="Fundo (parede técnica)", kind="ext", axis=("y", FO + 0.045, FO, LY - FO), L=L_short, h0=H_HI, h1=H_LO, slope=True, open=["J1", "J2"], peso=None))
    P.append(dict(cod="P-E02", nome="Lateral alta A (y = 0) · quarto", kind="ext", axis=("x", yA, FI, xm), L=xm - FI, h0=H_HI, h1=H_HI, slope=False, open=["J4"]))
    P.append(dict(cod="P-E03", nome="Lateral alta B (y = 0) · entrada", kind="ext", axis=("x", yA, xm, LX - FI), L=LX - FI - xm, h0=H_HI, h1=H_HI, slope=False, open=["P1"]))
    P.append(dict(cod="P-E04", nome="Frente · fachada de vidro", kind="ext", axis=("y", LX - FO - 0.045, FO, LY - FO), L=L_short, h0=H_HI, h1=H_LO, slope=True, open=["V1"]))
    P.append(dict(cod="P-E05", nome="Lateral baixa A (y = 4) · quarto", kind="ext", axis=("x", yB, FI, xm), L=xm - FI, h0=H_LO, h1=H_LO, slope=False, open=["J3"]))
    P.append(dict(cod="P-E06", nome="Lateral baixa B (y = 4) · sala", kind="ext", axis=("x", yB, xm, LX - FI), L=LX - FI - xm, h0=H_LO, h1=H_LO, slope=False, open=[]))
    # internos: altura até a face inferior das vigas de cobertura (forro inclinado); descontar 0,20 do forro + câmara não se aplica: forro fixado nas vigas
    yw = (WET_Y0 + WET_Y1) / 2; xw = (PI2_X0 + PI2_X1) / 2
    P.append(dict(cod="P-I01", nome="Parede molhada banho / cozinha", kind="int", axis=("x", yw, IX0, PI2_X1), L=PI2_X1 - IX0, h0=ztop(yw), h1=ztop(yw), slope=False, open=[]))
    P.append(dict(cod="P-I02", nome="Banho / quarto (porta P2)", kind="int", axis=("y", xw, IY0, WET_Y1), L=WET_Y1 - IY0, h0=ztop(IY0), h1=ztop(WET_Y1), slope=True, open=["P2"]))
    return P

PANELS = panels()
OPENS = {o["cod"]: o for o in OPEN}

def panel_studs(p):
    """posições dos montantes ao longo do painel (m, a partir do início do quadro): extremos + grade 400 + ombreiras."""
    ax, c, a0, a1 = p["axis"]
    s = set([0.045, p["L"] - 0.045])
    if p["kind"] == "ext":
        grid = GRID if ax == "x" else [round(0.20 + STEP * k, 3) for k in range(10)]
        for g in grid:
            u = g - a0
            if 0.20 < u < p["L"] - 0.20: s.add(round(u, 3))
    else:
        u = 0.40
        while u < p["L"] - 0.15: s.add(round(u, 3)); u += STEP
    kings = []
    for oc in p["open"]:
        o = OPENS[oc]
        for u in (o["a0"] - 0.045, o["a0"] + o["w"] + 0.045):
            if 0.0 < u < p["L"]:
                kings.append(round(u, 3))
                s = {v for v in s if abs(v - u) > 0.12 or v in (0.045, p["L"] - 0.045)}
    return sorted(s), sorted(set(kings))

# ------------------------------------------------------------------------------------------------- lista de perfis
PROFILES = {   # massa calculada pela seção desenvolvida (ZAR-275, 0,95 mm) — confirmar com o fabricante do perfil
    "Ue 90x40x12x0,95": 1.447, "U 92x40x0,95": 1.283, "Ue 150x40x12x0,95": 1.894, "U 152x40x0,95": 1.730,
    "Ue 200x40x12x0,95": 2.267, "U 203x40x0,95": 2.110, "Fita 50x0,95": 0.373, "Cantoneira 50x50x1,25": 0.98}

def members():
    """lista de perfis por elemento: (grupo, código, descrição, perfil, comp. m, qtd)."""
    M = []
    # fundação / vigas de fundação (caixão 2 x Ue 200 + U 203) sobre 15 apoios
    for i, y in enumerate((FO + 0.045, LY / 2, LY - FO - 0.045)):
        M.append(("Vigas de fundação", f"VF{i + 1:02d}", f"Viga de fundação linha y = {fmt(y)} · caixão 2 x Ue 200 + 2 x U 203 (2 segmentos de 3,50 m emendados sobre o apoio central)", "Ue 200x40x12x0,95", 3.50, 4))
        M.append(("Vigas de fundação", f"VF{i + 1:02d}g", f"Guias do caixão VF{i + 1:02d}", "U 203x40x0,95", 3.50, 4))
    # plataforma de piso: vigas Ue 150 @ 400 em y (4,0 m) + 2 bordas (U 152) + bloqueadores sobre a linha central
    n_j = len(GRID) + 2
    M.append(("Plataforma de piso", "VP01", "Viga de piso Ue 150 @ 400 (alinhada com montantes e vigas de cobertura), vão 2 x 1,93 m sobre 3 linhas", "Ue 150x40x12x0,95", LY - 2 * FO, n_j))
    M.append(("Plataforma de piso", "VP02", "Borda da plataforma (guia U 152) · lados de 7,00 m em 2 segmentos", "U 152x40x0,95", 3.50, 4))
    M.append(("Plataforma de piso", "VP03", "Borda da plataforma (guia U 152) · lados de 4,00 m", "U 152x40x0,95", LY - 2 * FO, 2))
    M.append(("Plataforma de piso", "VP04", "Bloqueador entre vigas de piso sobre VF02 (linha central) e sob as paredes internas", "Ue 150x40x12x0,95", 0.36, (n_j - 1) + 8))
    # paredes
    for p in PANELS:
        studs, kings = panel_studs(p)
        hmax = max(p["h0"], p["h1"]); hmin = min(p["h0"], p["h1"])
        M.append(("Paredes · " + p["cod"], f"{p['cod']}-M", f"Montantes {p['cod']} ({p['nome']}) @ 400 · altura {fmt(hmin)} a {fmt(hmax)} m" if p["slope"] else f"Montantes {p['cod']} ({p['nome']}) @ 400", "Ue 90x40x12x0,95", round(hmax - 0.09, 2), len(studs)))
        if kings: M.append(("Paredes · " + p["cod"], f"{p['cod']}-K", f"Montantes de abertura (king + jack) {p['cod']}", "Ue 90x40x12x0,95", round(hmax - 0.09, 2), 2 * len(kings)))
        M.append(("Paredes · " + p["cod"], f"{p['cod']}-G", f"Guias inferior e superior {p['cod']}" + (" (superior inclinada)" if p["slope"] else ""), "U 92x40x0,95", round(p["L"] * (1 / math.cos(math.radians(ANG)) if p["slope"] else 1), 2), 2))
        for oc in p["open"]:
            o = OPENS[oc]
            if oc == "V1": M.append(("Paredes · " + p["cod"], f"{p['cod']}-V", f"Verga da fachada V1 · vão {fmt(o['w'])} m · 2 x Ue 200 em caixa + guias (⚠️ cálculo)", "Ue 200x40x12x0,95", round(o["w"] + 0.18, 2), 2))
            else: M.append(("Paredes · " + p["cod"], f"{p['cod']}-V{oc}", f"Verga {oc} · 2 x Ue 90 em caixa + guia", "Ue 90x40x12x0,95", round(o["w"] + 0.18, 2), 2))
        M.append(("Paredes · " + p["cod"], f"{p['cod']}-B", f"Bloqueadores a meia altura {p['cod']}", "Ue 90x40x12x0,95", 0.36, max(1, len(studs) - 1)))
        seg = brace_segment(p)
        if seg: M.append(("Paredes · " + p["cod"], f"{p['cod']}-F", f"Fita de contraventamento em X {p['cod']} no trecho cheio de {fmt(seg[1] - seg[0])} m (2 diagonais, com chapas de canto)", "Fita 50x0,95", round(math.hypot(seg[1] - seg[0], hmax), 2), 2))
    # cobertura: vigas Ue 200 @ 400 de y = -0,35 a 4,35 ao longo da queda
    Lr = (LY + 2 * BEIRAL_Y) / math.cos(math.radians(ANG))
    M.append(("Cobertura", "VC01", f"Viga de cobertura Ue 200 @ 400 (alinhada com montantes), beirais de {fmt(BEIRAL_Y)} m, comprimento ao longo da queda", "Ue 200x40x12x0,95", round(Lr, 2), len(GRID) + 2))
    M.append(("Cobertura", "VC02", "Guias de borda das vigas (beirais de frente e fundo em 2 segmentos)", "U 203x40x0,95", round(Lr / 2, 2), 4))
    M.append(("Cobertura", "VC03", "Bloqueadores entre vigas sobre as paredes laterais e na linha central", "Ue 200x40x12x0,95", 0.36, 3 * (len(GRID) + 1)))
    M.append(("Cobertura", "VC04", "Cabeceiras dos beirais de frente e fundo (balanço 0,30 m) a cada 400", "Ue 200x40x12x0,95", 0.70, 2 * 11))
    M.append(("Cobertura", "VC05", "Ripas metálicas (telha sobre câmara ventilada) @ 500 ao longo dos 7,6 m", "Cantoneira 50x50x1,25", 3.80, 2 * 11))
    return M

def members_summary():
    tot = {}
    for g, c, d, prof, L, q in members():
        tot.setdefault(prof, [0.0, 0]); tot[prof][0] += L * q; tot[prof][1] += q
    rows = [(prof, round(m, 1), n, round(m * PROFILES[prof], 1)) for prof, (m, n) in tot.items()]
    return rows, round(sum(r[3] for r in rows), 0)

# ------------------------------------------------------------------------------------------------- fundação
PADS = [(x, y) for y in (FO + 0.045, LY / 2, LY - FO - 0.045) for x in (0.20, 1.85, 3.50, 5.15, 6.80)]
DECK = dict(x0=LX, x1=LX + 2.00, y0=0.0, y1=LY)           # deck 4,0 x 2,0 = 8 m² à parte
DECK_PADS = [(LX + 0.30, 0.20), (LX + 0.30, 2.0), (LX + 0.30, 3.80), (LX + 1.85, 0.20), (LX + 1.85, 2.0), (LX + 1.85, 3.80)]

# ------------------------------------------------------------------------------------------------- mobiliário (opção A linear)
FURN = [
    ("Cama Zion Canopy ZF-BD-01 (queen 1,60 x 2,00; externo 1,74 x 2,14)", 2.10, 1.13, 4.24, 2.87, "bed"),
    ("Mesa 0,80 x 1,20 + 2 cadeiras", 4.55, 1.40, 5.35, 2.60, "table"),
    ("Poltrona", 5.90, 3.05, 6.60, 3.75, "chair"),
    ("Poltrona", 5.90, 0.25, 6.60, 0.95, "chair"),
    ("Bancada da cozinha 0,60 x 1,58 (cuba, cooktop indução 2 bocas, frigobar e micro-ondas sob / sobre a bancada)", KIT["x0"], KIT["y0"], KIT["x0"] + 0.60, KIT["y1"], "counter"),
    ("Box 1,60 x 0,90 (chuveiro)", BATH["x0"], BATH["y1"] - 0.90, BATH["x1"], BATH["y1"], "shower"),
    ("Vaso sanitário", BATH["x0"] + 0.05, 0.37, BATH["x0"] + 0.70, 0.74, "wc"),
    ("Lavatório 0,45 x 0,50", BATH["x1"] - 0.60, BATH["y0"], BATH["x1"], BATH["y0"] + 0.45, "sink"),
]

# ------------------------------------------------------------------------------------------------- instalações
# hidráulica: (código, descrição, x, y, h, rede, diâmetro)
HID = [
    ("AF-0", "Entrada de água fria (registro geral + ponto de medição do empreendimento) · parede de fundo, externa", 0.00, 2.20, 0.60, "AF", "25 mm"),
    ("AF-1", "Chuveiro · misturador / registro (parede molhada P-I01, lado do banho)", 0.80, WET_Y0, 1.10, "AF+AQ", "20 / 16 mm"),
    ("AF-2", "Vaso sanitário (caixa acoplada) · parede de fundo", IX0, 0.55, 0.30, "AF", "20 mm"),
    ("AF-3", "Lavatório · parede lateral alta P-E02", BATH["x1"] - 0.30, IY0, 0.55, "AF+AQ", "20 / 16 mm"),
    ("AF-4", "Pia da cozinha · parede molhada P-I01, lado da cozinha", 0.45, WET_Y1, 0.55, "AF+AQ", "20 / 16 mm"),
    ("AF-5", "Torneira externa do deck (opcional)", LX, 3.60, 0.50, "AF", "20 mm"),
    ("AQ-0", "Origem da água quente: chuveiro elétrico (base) ou aquecedor de passagem no nicho externo da parede de fundo (opção)", 0.00, 2.60, 1.60, "AQ", "16 mm PEX"),
]
# esgoto: (código, descrição, x, y, diâmetro, destino)
ESG = [
    ("E-1", "Ralo linear do box", 0.95, BATH["y1"] - 0.08, "50 mm", "CS-1"),
    ("E-2", "Lavatório (sifão)", BATH["x1"] - 0.30, IY0 + 0.10, "40 mm", "CS-1"),
    ("E-3", "Vaso sanitário", IX0 + 0.35, 0.55, "100 mm", "Coletor"),
    ("E-4", "Pia da cozinha (sifão)", 0.45, WET_Y1 + 0.30, "50 mm", "Caixa de gordura externa (obra do sítio)"),
    ("CS-1", "Caixa sifonada 100 x 150 x 50 sob o piso do banho (tampa cega acessível pelo box)", 0.95, 1.55, "50 mm saída", "Coletor"),
    ("TV", "Tubo ventilador na parede molhada, saída 0,30 m acima do telhado", 1.20, (WET_Y0 + WET_Y1) / 2, "50 mm", "Atmosfera"),
    ("S", "Saída de esgoto da cabana · face de fundo, 0,25 m abaixo do piso · destino conforme terreno e prefeitura", 0.00, 1.00, "100 mm", "Rede / ETE / fossa+filtro+sumidouro"),
]
# elétrica: (código, descrição, x, y, h, circuito)
ELE = [
    ("QDC", "Quadro de distribuição 12 circuitos, DR 30 mA + DPS · parede de fundo (cozinha)", IX0, 3.70, 1.60, "—"),
    ("ENT", "Entrada de energia 220 V monofásica · eletroduto 32 mm pela parede de fundo (padrão da concessionária fica no sítio)", 0.00, 3.80, 0.60, "—"),
    ("L1", "Pendente sobre a mesa", 4.95, 2.00, 2.60, "C1"),
    ("L2", "Fita LED na cabeceira (parede P-I02)", 1.90, 2.00, 2.20, "C1"),
    ("L3", "Arandela de cabeceira (2)", 1.90, 0.95, 1.20, "C1"),
    ("L3", "Arandela de cabeceira (2)", 1.90, 3.05, 1.20, "C1"),
    ("L4", "Plafon do banho (IP44)", 0.95, 1.10, 2.40, "C1"),
    ("L5", "Fita LED sob o armário da cozinha", 0.60, 3.05, 1.50, "C1"),
    ("L6", "Arandela externa da entrada", 6.50, 0.00, 2.20, "C1"),
    ("L7", "Arandela do deck (2)", LX, 0.60, 2.20, "C1"),
    ("L7", "Arandela do deck (2)", LX, 3.40, 2.20, "C1"),
    ("S1", "Interruptor 2 teclas na entrada (L1, L6)", 6.55, IY0, 1.10, "C1"),
    ("S2", "Interruptor de cabeceira (2) (L2, L3)", 2.00, 0.95, 0.70, "C1"),
    ("S2", "Interruptor de cabeceira (2) (L2, L3)", 2.00, 3.05, 0.70, "C1"),
    ("S3", "Interruptor do banho (L4)", PI2_X1, 1.25, 1.10, "C1"),
    ("S4", "Interruptor cozinha + deck (L5, L7)", PI2_X1, 2.45, 1.10, "C1"),
    ("T1", "Tomada de cabeceira 2P+T 10 A (2)", 1.90, 0.80, 0.40, "C2"),
    ("T1", "Tomada de cabeceira 2P+T 10 A (2)", 1.90, 3.20, 0.40, "C2"),
    ("T2", "Tomada da mesa (parede baixa)", 4.95, IY1, 0.40, "C2"),
    ("T3", "Tomada da sala (parede baixa)", 6.40, IY1, 0.40, "C2"),
    ("T4", "Tomada do banho 2P+T 10 A (junto ao lavatório)", BATH["x1"] - 0.10, IY0, 1.10, "C2"),
    ("T5", "Tomada externa do deck IP55", LX, 3.60, 0.40, "C2"),
    ("T6", "Tomadas da bancada 2P+T 20 A (2)", IX0, 2.80, 1.10, "C3"),
    ("T6", "Tomadas da bancada 2P+T 20 A (2)", IX0, 3.40, 1.10, "C3"),
    ("T7", "Tomada do frigobar", IX0, 3.75, 0.40, "C3"),
    ("T8", "Tomada do micro-ondas", IX0, 3.20, 1.60, "C3"),
    ("CH", "Ponto do chuveiro elétrico 220 V (base) · 7 500 W", 0.80, WET_Y0, 2.20, "C4"),
    ("CK", "Ponto do cooktop de indução 2 bocas 220 V", IX0, 2.55, 1.10, "C5"),
    ("AC", "Split 9 000 a 12 000 BTU · evaporadora na parede baixa (sobre J3) · condensadora no fundo", 3.20, IY1, 1.95, "C6"),
    ("ACx", "Condensadora do split (externa, fundo)", -0.40, 3.40, 0.30, "C6"),
]
CIRC = [("C1", "Iluminação", "1,5 mm²", "10 A", "L1 a L7, interruptores"), ("C2", "Tomadas de uso geral (quarto, sala, banho, deck)", "2,5 mm²", "20 A · DR", "T1 a T5"),
        ("C3", "Tomadas da cozinha (bancada, frigobar, micro-ondas)", "2,5 mm²", "20 A · DR", "T6 a T8"), ("C4", "Chuveiro elétrico 7 500 W 220 V", "6 mm²", "40 A · DR", "CH"),
        ("C5", "Cooktop de indução 2 bocas", "4 mm²", "25 A", "CK"), ("C6", "Ar-condicionado split", "2,5 mm²", "20 A", "AC"), ("R", "Reserva (aquecedor a gás / bomba / iluminação externa)", "—", "—", "2 posições")]

# ------------------------------------------------------------------------------------------------- desenho · base
def new_sheet(scale=150.0, ox=170, oy=820):
    return Sheet(1600, 1000, scale, ox, oy)

def walls_plan(S, cut=True):
    """paredes em planta: externas (cheias) e internas."""
    S.rect(0, 0, LX, LY, fill=S.pattern("hatch2") if cut else "none", stroke=GREEN, sw=1.6)
    S.rect(IX0, IY0, IX1, IY1, fill=CREAM, stroke=GREEN, sw=1.6)
    # internas
    S.rect(IX0, WET_Y0, PI2_X1, WET_Y1, fill=S.pattern("hatch2") if cut else "none", stroke=GREEN, sw=1.2)
    S.rect(PI2_X0, IY0, PI2_X1, WET_Y1, fill=S.pattern("hatch2") if cut else "none", stroke=GREEN, sw=1.2)
    # aberturas
    for o in OPEN:
        p = {q["cod"]: q for q in PANELS}
        pw = p["P-" + o["wall"]]; ax, c, a0, a1 = pw["axis"]
        if pw["kind"] == "ext":
            if ax == "x":
                x0 = a0 + o["a0"]; y0, y1 = (0, TE) if c < LY / 2 else (LY - TE, LY)
                S.rect(x0, y0, x0 + o["w"], y1, fill=CREAM, stroke="none")
                if o["cod"].startswith("J"): S.line(x0, (y0 + y1) / 2, x0 + o["w"], (y0 + y1) / 2, GREEN, 1.0); S.line(x0, y0, x0 + o["w"], y0, GREEN, 0.8); S.line(x0, y1, x0 + o["w"], y1, GREEN, 0.8)
                else:   # porta P1 abre para dentro
                    S.line(x0, IY0, x0, IY0 + o["w"], GREEN, 1.0)
                    S.add(f'<path d="M{S.X(x0):.1f},{S.Y(IY0 + o["w"]):.1f} A{o["w"] * S.s:.1f},{o["w"] * S.s:.1f} 0 0 1 {S.X(x0 + o["w"]):.1f},{S.Y(IY0):.1f}" fill="none" stroke="{GREEN}" stroke-width="0.6" stroke-dasharray="3 3"/>')
            else:
                y0 = a0 + o["a0"] + (TE - FO - 0.0 if False else 0); x0, x1 = (0, TE) if c < LX / 2 else (LX - TE, LX)
                y0 = FO + o["a0"]
                S.rect(x0, y0, x1, y0 + o["w"], fill=CREAM, stroke="none")
                if o["cod"] == "V1":
                    S.rect(x0, y0, x1, y0 + o["w"], fill=GLASS, stroke=GREEN, sw=0.8)
                    S.line((x0 + x1) / 2, 1.10, (x0 + x1) / 2, 2.90, GREEN, 1.4)   # folhas de correr
                    S.text((x0 + x1) / 2, 2.0, "V1", 10, GREEN, rotate=-90)
                else:
                    S.line((x0 + x1) / 2, y0, (x0 + x1) / 2, y0 + o["w"], GREEN, 1.0); S.line(x0, y0, x0, y0 + o["w"], GREEN, 0.8); S.line(x1, y0, x1, y0 + o["w"], GREEN, 0.8)
        else:  # P2 na parede interna P-I02
            y0 = IY0 + o["a0"]; S.rect(PI2_X0, y0, PI2_X1, y0 + o["w"], fill=CREAM, stroke="none")
            S.line(PI2_X1, y0, PI2_X1 + o["w"], y0, GREEN, 1.0)
            S.add(f'<path d="M{S.X(PI2_X1 + o["w"]):.1f},{S.Y(y0):.1f} A{o["w"] * S.s:.1f},{o["w"] * S.s:.1f} 0 0 0 {S.X(PI2_X1):.1f},{S.Y(y0 + o["w"]):.1f}" fill="none" stroke="{GREEN}" stroke-width="0.6" stroke-dasharray="3 3"/>')

def deck_plan(S, light=False):
    S.rect(DECK["x0"], DECK["y0"], DECK["x1"], DECK["y1"], fill=S.pattern("deck") if not light else "none", stroke=GREEN, sw=1.0, dash="6 3" if light else None)
    S.text(DECK["x0"] + 1.0, DECK["y1"] / 2, "DECK 4,00 x 2,00 · 8 m² (à parte)", 11, GREEN, rotate=-90)

def furniture(S):
    for name, x0, y0, x1, y1, kind in FURN:
        if kind == "bed":
            S.rect(x0, y0, x1, y1, fill=SAND, stroke=GREEN, sw=0.9); S.rect(x0 + 0.07, y0 + 0.07, x1 - 0.07, y1 - 0.07, stroke=GREEN, sw=0.5)
            S.rect(x0 + 0.12, y0 + 0.15, x0 + 0.60, (y0 + y1) / 2 - 0.05, fill=CREAM, stroke=GREEN, sw=0.5); S.rect(x0 + 0.12, (y0 + y1) / 2 + 0.05, x0 + 0.60, y1 - 0.15, fill=CREAM, stroke=GREEN, sw=0.5)
            S.text((x0 + x1) / 2, (y0 + y1) / 2, "CAMA QUEEN", 10, GREEN)
        elif kind == "table":
            S.rect(x0, y0, x1, y1, fill=WOOD, stroke=GREEN, sw=0.8); S.rect(x0 - 0.45, (y0 + y1) / 2 - 0.22, x0 - 0.05, (y0 + y1) / 2 + 0.22, stroke=GREEN, sw=0.6); S.rect(x1 + 0.05, (y0 + y1) / 2 - 0.22, x1 + 0.45, (y0 + y1) / 2 + 0.22, stroke=GREEN, sw=0.6)
        elif kind == "chair": S.rect(x0, y0, x1, y1, fill=WOOD, stroke=GREEN, sw=0.7); S.line(x0 + 0.12, y0, x0 + 0.12, y1, GREEN, 0.5)
        elif kind == "counter":
            S.rect(x0, y0, x1, y1, fill=WOOD, stroke=GREEN, sw=0.8); S.circle(x0 + 0.30, y0 + 0.30, 0.18, stroke=GREEN, sw=0.7); S.circle(x0 + 0.30, y0 + 0.95, 0.13, stroke=GREEN, sw=0.6); S.circle(x0 + 0.30, y0 + 1.25, 0.13, stroke=GREEN, sw=0.6)
            S.text(x0 + 0.30, y0 + 0.30, "cuba", 7, GREEN, dy=3); S.text(x0 + 0.30, y0 + 1.10, "cooktop", 7, GREEN, rotate=-90)
        elif kind == "shower": S.rect(x0, y0, x1, y1, fill=TILE, stroke=GREEN, sw=0.7); S.line(x0, y0, x1, y0, GREEN, 0.8, dash="4 3"); S.circle(x0 + 0.95, y1 - 0.08, 0.05, stroke=GREEN, sw=0.6)
        elif kind == "wc": S.rect(x0, y0, x0 + 0.18, y1, fill=CREAM, stroke=GREEN, sw=0.7); S.add(f'<ellipse cx="{S.X(x0 + 0.42):.1f}" cy="{S.Y((y0 + y1) / 2):.1f}" rx="{0.24 * S.s:.1f}" ry="{0.17 * S.s:.1f}" fill="{CREAM}" stroke="{GREEN}" stroke-width="0.7"/>')
        elif kind == "sink": S.rect(x0, y0, x1, y1, fill=WOOD, stroke=GREEN, sw=0.7); S.circle((x0 + x1) / 2, (y0 + y1) / 2, 0.17, stroke=GREEN, sw=0.6)

def room_labels(S):
    S.text(3.2, 3.45, "QUARTO · SALA", 12, GREEN, weight=600, spacing=0.2)
    S.text(0.95, 1.15, "BANHO", 10, GREEN, weight=600, spacing=0.15); S.text(0.95, 1.00, "1,60 x 2,00", 8, EARTH)
    S.text(1.25, 3.05, "COZINHA", 10, GREEN, weight=600, spacing=0.15, rotate=-90); S.text(1.40, 3.05, "1,60 x 1,58", 8, EARTH, rotate=-90)
    S.text(5.8, 2.0, "ESTAR", 10, GREEN, weight=600, spacing=0.15)

def frame_title(S, title, sub, sheet, scale="1:50"):
    S.header("ZION CABIN 28 · " + title, sub)
    S.title_block(PROD, title, scale, sheet, "Opção A Linear · 4,00 x 7,00 m · LSF", DATE)

# ------------------------------------------------------------------------------------------------- A-01 planta baixa
def sheet_planta():
    S = new_sheet(); frame_title(S, "Planta baixa · opção A linear", "Arquitetura · mobiliário · cotas externas e internas", "A-01")
    walls_plan(S); deck_plan(S); furniture(S); room_labels(S)
    S.dim(0, 0, LX, 0, -0.55, label=fmt(LX)); S.dim(0, 0, 0, LY, -0.55, label=fmt(LY))
    S.dim(IX0, IY1, IX1, IY1, 0.9, label=fmt(IX1 - IX0)); S.dim(IX1, IY0, IX1, IY1, 2.55, label=fmt(IY1 - IY0))
    S.dim_chain([IX0, BATH["x1"], PI2_X1, 2.10, 4.24, IX1], IY1, 0.65, size=10)
    S.dim_chain([IY0, BATH["y1"], WET_Y1, IY1], -1.0, 0.0, size=10, vertical=True)
    S.dim(LX, 0, DECK["x1"], 0, -0.55, label=fmt(2.0))
    S.north(1545, 122, 22, 0); S.scalebar(0.0, -1.05, 5)
    for o in OPEN:
        p = {q["cod"]: q for q in PANELS}["P-" + o["wall"]]; ax, c, a0, a1 = p["axis"]
        if o["cod"] == "V1": continue
        if p["kind"] == "ext" and ax == "x": S.text(a0 + o["a0"] + o["w"] / 2, (-0.22 if c < LY / 2 else LY + 0.18), o["cod"], 10, EARTH, weight=600)
        elif p["kind"] == "ext": S.text((-0.3 if c < LX / 2 else LX + 0.3), FO + o["a0"] + o["w"] / 2, o["cod"], 10, EARTH, weight=600)
        else: S.text(PI2_X1 + 0.3, IY0 + o["a0"] + o["w"] / 2 + 0.15, o["cod"], 9, EARTH, weight=600)
    S.leader(0.0, 2.2, 0.3, 4.45, "parede técnica: entrada de água, saída de esgoto, energia", 10, EARTH, anchor="start")
    S.text(0.2, -0.85, "ÁREA: 28,0 m² construída (externa) · 24,8 m² útil interna · deck 8,0 m² à parte · altura interna 2,20 a 2,80 m (forro inclinado)", 10, GREEN, anchor="start")
    S.legend(960, 112, [(1, "Núcleo molhado: banho 1,60 x 2,00 + cozinha 1,60 x 1,58 com uma só parede de prumadas (P-I01)"), (2, "Cama de frente para a fachada de vidro V1 · mesa no meio · estar junto ao vidro"), (3, "Entrada lateral P1 no lado alto (y = 0) · janela J3 do quarto no lado baixo"), (4, "Ajuste em relação ao handoff: banho 2,20 → 2,00 e cozinha 1,80 → 1,58 para caber em 3,70 m internos")], size=9.5)
    S.save(os.path.join(OUT, "A-01_planta_baixa.svg"))

# ------------------------------------------------------------------------------------------------- A-02 cortes
def roof_section(S, y_lo, y_hi, x_offset=0.0):
    """corte transversal (olhando para o fundo): camadas de piso, parede e cobertura em escala."""
    pass

def sheet_cortes():
    S = Sheet(1600, 1000, 120.0, 150, 560)
    frame_title(S, "Cortes AA e BB", "Transversal (sobre a cama) e longitudinal (pelo eixo) · níveis e camadas", "A-02")
    # ---- corte AA transversal (eixo x = 3,0): olhando para o fundo, y da esquerda (lado alto) para a direita
    ox = 0.0
    def X(y): return ox + y
    # solo e fundação
    S.rect(X(-1.0), -0.95, X(LY + 1.0), -0.65, fill=S.pattern("soil"), stroke="none")
    S.line(X(-1.0), -0.65, X(LY + 1.0), -0.65, GREEN, 1.0)
    for y in (FO + 0.045, LY / 2, LY - FO - 0.045):
        S.rect(X(y - 0.25), -0.95, X(y + 0.25), -0.65, fill=TILE, stroke=GREEN, sw=0.8)      # sapata 0,50 x 0,50
        S.rect(X(y - 0.075), -0.65, X(y + 0.075), -0.38, fill=STEEL, stroke=GREEN, sw=0.6)   # pedestal metálico regulável
        S.rect(X(y - 0.05), -0.38, X(y + 0.05), -0.18, fill=TILE, stroke=GREEN, sw=0.8)       # viga de fundação (caixão 2 x Ue 200)
    S.line(X(0), -0.38, X(LY), -0.38, GREEN, 0.8); S.line(X(0), -0.18, X(LY), -0.18, GREEN, 0.8)
    # plataforma: vigas Ue 150 (em corte, transversal → vigas correm em y, logo aparecem em comprimento)
    S.rect(X(FO), -0.18, X(LY - FO), -0.03, fill=S.pattern("insul"), stroke=GREEN, sw=0.9)
    S.rect(X(FO), -0.03, X(LY - FO), 0.0, fill=WOOD, stroke=GREEN, sw=0.7)                     # OSB 18 + piso
    S.line(X(FO), -0.19, X(LY - FO), -0.19, GREEN, 1.2)                                        # placa cimentícia inferior
    # paredes
    for y0, y1, h in ((FO, FI, H_HI), (LY - FI, LY - FO, H_LO)):
        S.rect(X(y0), 0.0, X(y1), h, fill=S.pattern("insul"), stroke=GREEN, sw=1.0)
        yo = 0.0 if y0 < LY / 2 else LY - 0.0
        if y0 < LY / 2:
            S.rect(X(0.0), 0.0, X(FO), h, fill=TILE, stroke=GREEN, sw=0.6); S.rect(X(FI), 0.0, X(FI + 0.0125), h, fill=SAND, stroke=GREEN, sw=0.5)
        else:
            S.rect(X(LY - FO), 0.0, X(LY), h, fill=TILE, stroke=GREEN, sw=0.6); S.rect(X(LY - FI - 0.0125), 0.0, X(LY - FI), h, fill=SAND, stroke=GREEN, sw=0.5)
    # cobertura: vigas Ue 200 inclinadas de y = -0,35 a 4,35
    def zr(y): return ztop(y)
    pts = [(X(-BEIRAL_Y), zr(-BEIRAL_Y)), (X(LY + BEIRAL_Y), zr(LY + BEIRAL_Y)), (X(LY + BEIRAL_Y), zr(LY + BEIRAL_Y) + 0.20), (X(-BEIRAL_Y), zr(-BEIRAL_Y) + 0.20)]
    S.poly(pts, fill=S.pattern("insul"), stroke=GREEN, sw=1.0)
    pts2 = [(X(-BEIRAL_Y), zr(-BEIRAL_Y) + 0.20), (X(LY + BEIRAL_Y), zr(LY + BEIRAL_Y) + 0.20), (X(LY + BEIRAL_Y), zr(LY + BEIRAL_Y) + 0.26), (X(-BEIRAL_Y), zr(-BEIRAL_Y) + 0.26)]
    S.poly(pts2, fill=WOOD, stroke=GREEN, sw=0.7)   # OSB 18 + membrana + ripas + câmara
    pts3 = [(X(-BEIRAL_Y - 0.05), zr(-BEIRAL_Y) + 0.30), (X(LY + BEIRAL_Y + 0.05), zr(LY + BEIRAL_Y) + 0.30), (X(LY + BEIRAL_Y + 0.05), zr(LY + BEIRAL_Y) + 0.33), (X(-BEIRAL_Y - 0.05), zr(-BEIRAL_Y) + 0.33)]
    S.poly(pts3, fill=STEEL, stroke=GREEN, sw=0.7)   # telha metálica
    S.line(X(FI), 0.0, X(FI), 0.0, GREEN, 0.5)
    # forro de gesso na face inferior das vigas
    S.line(X(FI), zr(FI), X(LY - FI), zr(LY - FI), SAND, 3.0)
    # calha no lado baixo
    S.rect(X(LY + BEIRAL_Y + 0.02), zr(LY + BEIRAL_Y) + 0.05, X(LY + BEIRAL_Y + 0.14), zr(LY + BEIRAL_Y) + 0.28, fill=CREAM, stroke=GREEN, sw=0.8)
    S.line(X(LY + BEIRAL_Y + 0.10), zr(LY + BEIRAL_Y) + 0.05, X(LY + BEIRAL_Y + 0.10), -0.60, GREEN, 0.8, dash="4 3")
    # cama em corte e pessoa
    S.rect(X(1.13), 0.0, X(2.87), 0.55, fill=SAND, stroke=GREEN, sw=0.7); S.rect(X(1.13), 0.55, X(2.87), 0.60, fill=CREAM, stroke=GREEN, sw=0.5)
    S.line(X(1.13), 0.0, X(1.13), 2.10, GREEN, 0.9); S.line(X(2.87), 0.0, X(2.87), 2.10, GREEN, 0.9); S.line(X(1.13), 2.10, X(2.87), 2.10, GREEN, 0.9)
    S.text(X(2.0), 1.30, "CAMA ZION CANOPY", 9, EARTH)
    # janelas J4 (lado alto) e J3 (lado baixo) em corte
    S.rect(X(0.0), 1.85, X(TE), 2.35, fill=GLASS, stroke=GREEN, sw=0.7); S.rect(X(LY - TE), 0.90, X(LY), 1.90, fill=GLASS, stroke=GREEN, sw=0.7)
    # cotas
    S.dim(X(0), 0.0, X(0), H_HI, -0.75, label=fmt(H_HI)); S.dim(X(LY), 0.0, X(LY), H_LO, 0.75, label=fmt(H_LO))
    S.dim(X(0), -0.95, X(LY), -0.95, -0.35, label=fmt(LY)); S.dim(X(0), -0.65, X(0), 0.0, -1.25, label="0,65 vão ventilado")
    S.dim(X(-BEIRAL_Y), zr(-BEIRAL_Y) + 0.6, X(0), zr(-BEIRAL_Y) + 0.6, 0.0, label="0,35")
    S.text(X(LY / 2), zr(LY / 2) + 0.75, f"queda {SLOPE * 100:.1f} % ({ANG:.1f}°) para o lado baixo · calha + descida Ø 75", 10, EARTH)
    S.text(X(LY / 2), -1.25, "CORTE AA · transversal pelo quarto (x = 3,00) · olhando para o fundo", 12, GREEN, weight=600, spacing=0.15)
    S.legend(880, 104, [(1, "Sapata pré-moldada 0,50 x 0,50 (ou estaca helicoidal) + pedestal metálico regulável ± 50 mm"), (2, "Viga de fundação: caixão 2 x Ue 200 + 2 x U 203, 3 linhas, apoios a cada 1,65 m"), (3, "Plataforma: vigas Ue 150 @ 400 + OSB 18,3 + placa cimentícia 8 mm por baixo + lã PET 50 + piso vinílico / madeira"), (4, "Parede 150 mm: revestimento 10 + câmara ventilada 25 + membrana + OSB 11,1 + Ue 90 @ 400 com lã 90 + gesso 12,5"), (5, "Cobertura: Ue 200 @ 400 + lã 100 + câmara 100 + OSB 18,3 + membrana + ripas + telha metálica 0,50 · forro de gesso inclinado"), (6, "Beirais 0,35 m nos lados · pé-direito 2,20 a 2,80 m"), (7, "Janelas J4 (alta, lado alto) e J3 (quarto, lado baixo)")], size=8.5)
    # ---- corte BB longitudinal (eixo y = 2,0): à direita, menor escala
    S2 = Sheet(1600, 1000, 58.0, 880, 790)
    def X2(x): return x
    S2.rect(X2(-0.6), -0.95, X2(LX + 2.6), -0.65, fill=S2.pattern("soil"), stroke="none"); S2.line(X2(-0.6), -0.65, X2(LX + 2.6), -0.65, GREEN, 1.0)
    for x, y in PADS[5:10]:
        S2.rect(X2(x - 0.25), -0.95, X2(x + 0.25), -0.65, fill=TILE, stroke=GREEN, sw=0.8); S2.rect(X2(x - 0.075), -0.65, X2(x + 0.075), -0.38, fill=STEEL, stroke=GREEN, sw=0.6)
    for x, y in DECK_PADS[::3]:
        S2.rect(X2(x - 0.2), -0.95, X2(x + 0.2), -0.65, fill=TILE, stroke=GREEN, sw=0.8); S2.rect(X2(x - 0.06), -0.65, X2(x + 0.06), -0.10, fill=STEEL, stroke=GREEN, sw=0.6)
    S2.rect(X2(0.20), -0.38, X2(6.80), -0.18, fill=TILE, stroke=GREEN, sw=0.8)
    S2.rect(X2(FO), -0.18, X2(LX - FO), 0.0, fill=S2.pattern("insul"), stroke=GREEN, sw=0.9)
    S2.rect(X2(LX), -0.10, X2(LX + 2.0), -0.04, fill=WOOD, stroke=GREEN, sw=0.7)   # deck
    hz = ztop(2.0)
    S2.rect(X2(0.0), 0.0, X2(TE), hz, fill=S2.pattern("insul"), stroke=GREEN, sw=1.0)
    S2.rect(X2(LX - TE), 0.0, X2(LX), hz, fill=GLASS, stroke=GREEN, sw=1.0)
    S2.rect(X2(PI2_X0), 0.0, X2(PI2_X1), hz, fill=S2.pattern("insul"), stroke=GREEN, sw=0.9)
    S2.rect(X2(-BEIRAL_X), hz, X2(LX + BEIRAL_X), hz + 0.20, fill=S2.pattern("insul"), stroke=GREEN, sw=1.0)
    S2.rect(X2(-BEIRAL_X), hz + 0.20, X2(LX + BEIRAL_X), hz + 0.33, fill=WOOD, stroke=GREEN, sw=0.7)
    S2.rect(X2(IX0), 0.0, X2(IX0 + 0.60), 0.90, fill=WOOD, stroke=GREEN, sw=0.7)    # bancada
    S2.rect(X2(2.10), 0.0, X2(4.24), 0.55, fill=SAND, stroke=GREEN, sw=0.7); S2.rect(X2(4.55), 0.0, X2(5.35), 0.75, fill=WOOD, stroke=GREEN, sw=0.6)
    S2.rect(X2(0), 1.15, X2(TE), 1.75, fill=GLASS, stroke=GREEN, sw=0.6)
    S2.dim(X2(0), -0.95, X2(LX), -0.95, -0.35, label=fmt(LX), size=11); S2.dim(X2(LX), -0.95, X2(LX + 2.0), -0.95, -0.35, label="2,00 deck", size=11)
    S2.dim(X2(LX), 0.0, X2(LX), hz, 0.9, label=f"{fmt(hz)} no eixo", size=11)
    S2.text(X2(LX / 2), -1.3, "CORTE BB · longitudinal pelo eixo (y = 2,00) · olhando para o lado baixo", 12, GREEN, weight=600, spacing=0.15)
    S2.text(X2(LX / 2), hz + 0.95, "cobertura em uma água: caimento transversal (do lado alto y = 0 para o lado baixo y = 4) · beirais de 0,30 m na frente e no fundo", 10, EARTH)
    S2.text(X2(0.9), 1.6, "NÚCLEO", 9, EARTH); S2.text(X2(3.2), 1.6, "QUARTO", 9, EARTH); S2.text(X2(5.9), 1.6, "ESTAR", 9, EARTH); S2.text(X2(LX + 1.0), 0.4, "DECK", 9, EARTH)
    S.parts += S2.parts; S.defs += [d for d in S2.defs if d not in S.defs]
    S.save(os.path.join(OUT, "A-02_cortes.svg"))

# ------------------------------------------------------------------------------------------------- A-03 fachadas
def elev_outline(S, kind, ox):
    """silhueta da fachada no plano do desenho: kind in frente/fundo (largura 4 m, trapézio) ou alto/baixo (7 m, reta)."""
    pass

def sheet_fachadas():
    S = Sheet(1600, 1000, 72.0, 110, 470)
    frame_title(S, "Fachadas", "Frente (vidro) · lado alto (entrada) · lado baixo · fundo (técnica)", "A-03", "1:75")
    def facade(ox, oy, w, hl, hr, title, openings, roofline=True, gutter=None):
        T = Sheet(1600, 1000, 72.0, ox, oy)
        T.rect(0, -0.65, w, 0.0, fill=S.pattern("hatch"), stroke=GREEN, sw=0.6)      # vão ventilado / saia
        T.poly([(0, 0), (w, 0), (w, hr), (0, hl)], fill=TILE, stroke=GREEN, sw=1.4)
        # ripado horizontal
        n = int(max(hl, hr) / 0.15)
        for i in range(1, n + 1):
            z = i * 0.15; zz_l = min(z, hl); zz_r = min(z, hr)
            if z < min(hl, hr): T.line(0, z, w, z, EARTH, 0.4, opacity=0.6)
        for (a0, ww, sill, hh, cod) in openings:
            T.rect(a0, sill, a0 + ww, sill + hh, fill=GLASS, stroke=GREEN, sw=0.9); T.text(a0 + ww / 2, sill + hh + 0.12, cod, 9, EARTH, weight=600)
        if roofline:
            T.poly([(-0.35, hl + 0.0), (w + 0.35, hr + 0.0), (w + 0.35, hr + 0.33), (-0.35, hl + 0.33)], fill=STEEL, stroke=GREEN, sw=1.0)
        if gutter == "r": T.rect(w + 0.35, hr + 0.05, w + 0.47, hr + 0.28, fill=CREAM, stroke=GREEN, sw=0.7); T.line(w + 0.41, hr + 0.05, w + 0.41, -0.6, GREEN, 0.7, dash="3 3")
        if gutter == "full": T.rect(-0.35, hl + 0.05, w + 0.35, hl + 0.28, fill=CREAM, stroke=GREEN, sw=0.7)
        T.text(w / 2, -1.05, title, 11, GREEN, weight=600, spacing=0.15)
        T.dim(0, -0.65, w, -0.65, -0.25, label=fmt(w), size=10)
        T.dim(0, 0, 0, hl, -0.75, label=fmt(hl), size=10); T.dim(w, 0, w, hr, 0.75, label=fmt(hr), size=10)
        S.parts += T.parts; S.defs += [d for d in T.defs if d not in S.defs]
    # frente: olhando do deck para a cabana, lado alto à ESQUERDA? O observador na frente vê o lado alto (y=0) à direita. Desenhar y da direita p/ esquerda: usar espelho simples.
    ya, yb = FO + 0.204, FO + 0.204 + 3.50
    facade(110, 470, LY, H_HI, H_LO, "FACHADA FRENTE (do deck) · V1 vidro até o telhado", [(ya, 0.85, 0.0, 2.20, "fixo"), (ya + 0.85, 1.80, 0.0, 2.20, "V1 correr"), (ya + 2.65, 0.85, 0.0, 2.20, "fixo")])
    T = Sheet(1600, 1000, 72.0, 110, 470); T.poly([(ya, 2.25), (yb, 2.25), (yb, ztop(yb) - 0.12), (ya, ztop(ya) - 0.12)], fill=GLASS, stroke=GREEN, sw=0.9); T.text(2.0, 2.45, "bandeira fixa", 9, EARTH); S.parts += T.parts
    facade(560, 470, LX, H_HI, H_HI, "FACHADA LADO ALTO (y = 0) · entrada P1 · janela alta J4", [(FI + 1.80, 1.20, 1.85, 0.50, "J4"), (LX / 2 + 2.05, 0.90, 0.0, 2.10, "P1")])
    facade(110, 920, LY, H_LO, H_HI, "FACHADA FUNDO (vista de trás) · parede técnica: J1 banho, J2 cozinha, entradas", [(LY - (FO + 1.00) - 0.60, 0.60, 1.50, 0.60, "J1"), (LY - (FO + 2.45) - 1.20, 1.20, 1.15, 0.60, "J2")])
    facade(560, 920, LX, H_LO, H_LO, "FACHADA LADO BAIXO (y = 4) · janela J3 do quarto · calha", [(LX - (FI + 1.90) - 1.20, 1.20, 0.90, 1.00, "J3")], gutter="full")
    S.text(100, 104, "Revestimento externo: ripado horizontal em placa cimentícia pintada ou siding de madeira tratada sobre câmara ventilada · telha metálica galvalume pré-pintada · esquadrias de alumínio preto · vidro laminado 8 mm (⚠️ dimensionar)", 9.5, EARTH, anchor="start", px=True)
    S.save(os.path.join(OUT, "A-03_fachadas.svg"))

# ------------------------------------------------------------------------------------------------- E-01 planta de fundação e plataforma
def sheet_fundacao():
    S = new_sheet(); frame_title(S, "Fundação e vigas de fundação", "15 apoios em 3 linhas · caixão 2 x Ue 200 · deck com 6 apoios próprios", "E-01")
    S.rect(0, 0, LX, LY, stroke=GREEN, sw=0.8, dash="6 3"); deck_plan(S, light=True)
    for i, y in enumerate((FO + 0.045, LY / 2, LY - FO - 0.045)):
        S.rect(0.0, y - 0.10, LX, y + 0.10, fill=TILE, stroke=GREEN, sw=1.0); S.text(-0.45, y, f"VF0{i + 1}", 10, GREEN, weight=600)
        S.line(3.50, y - 0.10, 3.50, y + 0.10, GREEN, 1.4)   # emenda
    for i, (x, y) in enumerate(PADS):
        S.rect(x - 0.25, y - 0.25, x + 0.25, y + 0.25, fill=CREAM, stroke=GREEN, sw=1.0); S.circle(x, y, 0.07, fill=GREEN, stroke=GREEN); S.text(x, y - 0.40, f"F{i + 1:02d}", 9, EARTH, weight=600)
    for i, (x, y) in enumerate(DECK_PADS):
        S.rect(x - 0.2, y - 0.2, x + 0.2, y + 0.2, fill=CREAM, stroke=GREEN, sw=0.8, dash="3 2"); S.text(x, y - 0.35, f"D{i + 1:02d}", 8, EARTH)
    S.dim_chain([0.20, 1.85, 3.50, 5.15, 6.80], -0.0, -0.75, size=10); S.dim(0.20, -0.0, 6.80, -0.0, -1.2, label="6,60")
    S.dim_chain([FO + 0.045, LY / 2, LY - FO - 0.045], LX + 2.2, 0.55, size=10, vertical=True)
    S.north(1545, 122); S.scalebar(0.0, -1.55, 5)
    S.legend(960, 112, [(1, "F01 a F15: sapata pré-moldada 0,50 x 0,50 x 0,30 (ou estaca helicoidal Ø 76) com pedestal metálico regulável ± 50 mm"), (2, "VF01 a VF03: vigas de fundação em caixão (2 x Ue 200 + 2 x U 203), 2 segmentos de 3,50 m emendados sobre F03 / F08 / F13"), (3, "Topo das vigas de fundação a + 0,45 m do terreno (vão ventilado mínimo 0,40 m) · nivelamento ± 5 mm"), (4, "Ancoragem: chapa de base + chumbador no pedestal; plataforma presa às vigas com parafusos auto-brocantes e cantoneiras"), (5, "D01 a D06: apoios do deck (independentes da cabana)"), (6, "⚠️ VALIDAÇÃO OBRIGATÓRIA: tipo e profundidade da fundação conforme sondagem do sítio; vigas conforme cálculo")], size=8.5)
    S.text(0.0, -1.9, "Coordenadas dos apoios (m): x = 0,20 · 1,85 · 3,50 · 5,15 · 6,80  ×  y = 0,091 · 2,000 · 3,909 (eixo das paredes laterais e linha central)", 10, GREEN, anchor="start")
    S.save(os.path.join(OUT, "E-01_fundacao.svg"))

def sheet_plataforma():
    S = new_sheet(); frame_title(S, "Plataforma de piso", "Vigas Ue 150 @ 400 em y, alinhadas com montantes e vigas de cobertura · OSB 18,3 mm", "E-02")
    S.rect(FO, FO, LX - FO, LY - FO, fill="none", stroke=GREEN, sw=1.6)
    for y in (FO, LY - FO): S.rect(FO, y - 0.0, LX - FO, y + (0.04 if y < 1 else -0.04), fill=TILE, stroke=GREEN, sw=0.8)
    xs = [FO + 0.045] + GRID + [LX - FO - 0.045]
    for i, x in enumerate(xs):
        S.rect(x - 0.02, FO, x + 0.02, LY - FO, fill=TILE, stroke=GREEN, sw=0.7)
        if i % 2 == 0: S.text(x, LY - FO + 0.18, f"{i + 1}", 8, EARTH)
    for x0, x1 in zip(xs[:-1], xs[1:]):
        S.rect(x0 + 0.02, LY / 2 - 0.02, x1 - 0.02, LY / 2 + 0.02, fill=S.pattern("hatch"), stroke=GREEN, sw=0.5)
    # bloqueadores sob paredes internas
    S.rect(IX0, (WET_Y0 + WET_Y1) / 2 - 0.02, PI2_X1, (WET_Y0 + WET_Y1) / 2 + 0.02, fill=S.pattern("hatch"), stroke=GREEN, sw=0.5)
    S.line(3.50, FO, 3.50, FO + 0.04, GREEN, 1.4); S.line(3.50, LY - FO, 3.50, LY - FO - 0.04, GREEN, 1.4)
    # chapas OSB 1,20 x 2,40 (cruzadas)
    S.rect(FO, FO, LX - FO, LY - FO, stroke=EARTH, sw=0.5, dash="2 3")
    for k in range(1, 4): S.line(FO, FO + 1.20 * k - 0.0, LX - FO, FO + 1.20 * k, EARTH, 0.5, dash="2 3")
    for k in range(1, 3): S.line(FO + 2.40 * k, FO, FO + 2.40 * k, LY - FO, EARTH, 0.5, dash="2 3")
    S.dim_chain(xs[:6], LY + 0.25, 0.45, size=9); S.dim(xs[0], LY + 0.25, xs[-1], LY + 0.25, 0.95, label=fmt(xs[-1] - xs[0]))
    S.dim(FO, FO, FO, LY - FO, -0.55, label=fmt(LY - 2 * FO)); S.dim_chain([FO, LY / 2, LY - FO], -0.3, -0.3, size=9, vertical=True)
    S.north(1545, 122); S.scalebar(0.0, -1.0, 5)
    S.legend(960, 112, [(1, f"{len(xs)} vigas de piso Ue 150 x 40 x 0,95 @ 400 (comprimento {fmt(LY - 2 * FO)} m), vão 2 x 1,93 m sobre VF01 / VF02 / VF03"), (2, "Bordas: guia U 152 (7,00 m em 2 segmentos emendados em x = 3,50; 4,00 m inteiros)"), (3, "Bloqueadores Ue 150 (0,36 m) entre vigas sobre a linha central VF02 e sob as paredes internas"), (4, "OSB 18,3 mm estrutural 1,20 x 2,40 com juntas desencontradas, parafuso auto-brocante 4,2 x 32 @ 150 nas bordas / 300 no meio"), (5, "Face inferior: placa cimentícia 8 mm (proteção) · lã PET 50 mm entre vigas · banho: placa cimentícia 10 + impermeabilização + porcelanato"), (6, "⚠️ VALIDAÇÃO OBRIGATÓRIA: bitola e vão das vigas de piso conforme cálculo (sobrecarga de hospedagem)")], size=8.5)
    S.save(os.path.join(OUT, "E-02_plataforma.svg"))

# ------------------------------------------------------------------------------------------------- E-03 planta chave dos painéis
def sheet_paineis_planta():
    S = new_sheet(); frame_title(S, "Planta chave dos painéis", "6 painéis externos + 2 internos · sentido de montagem · ancoragens", "E-03")
    walls_plan(S, cut=False); deck_plan(S, light=True)
    lab = {"P-E01": (-0.6, LY / 2, -90), "P-E02": (LX / 4, -0.45, 0), "P-E03": (3 * LX / 4, -0.45, 0), "P-E04": (LX + 0.55, LY / 2, -90), "P-E05": (LX / 4, LY + 0.35, 0), "P-E06": (3 * LX / 4, LY + 0.35, 0), "P-I01": (0.95, WET_Y1 + 0.2, 0), "P-I02": (PI2_X1 + 0.25, 1.9, -90)}
    for p in PANELS:
        ax, c, a0, a1 = p["axis"]
        if ax == "x": S.line(a0, c, a1, c, EARTH, 3.0, opacity=0.7)
        else: S.line(c, a0, c, a1, EARTH, 3.0, opacity=0.7)
        x, y, r = lab[p["cod"]]; S.text(x, y, p["cod"], 12, GREEN, weight=700, rotate=r, spacing=0.1)
    S.line(LX / 2, -0.2, LX / 2, LY + 0.2, GREEN, 0.8, dash="4 3"); S.text(LX / 2, LY + 0.6, "emenda dos painéis laterais x = 3,50", 9, EARTH)
    # ordem de montagem
    order = [("P-E01", 0.55, 2.0), ("P-E02", 1.75, 0.45), ("P-E05", 1.75, 3.55), ("P-E03", 5.25, 0.45), ("P-E06", 5.25, 3.55), ("P-E04", 6.45, 2.0), ("P-I01", 1.3, 2.4), ("P-I02", 2.1, 1.0)]
    for n, (cod, x, y) in enumerate(order, 1): S.callout(x, y, n)
    # ancoragens
    for p in PANELS:
        if p["kind"] != "ext": continue
        ax, c, a0, a1 = p["axis"]
        u = a0 + 0.25
        while u < a1 - 0.2:
            if ax == "x": S.circle(u, c, 0.05, fill=GREEN, stroke=GREEN)
            else: S.circle(c, u, 0.05, fill=GREEN, stroke=GREEN)
            u += 1.20
    S.dim(0, 0, LX, 0, -0.95, label=fmt(LX)); S.dim(0, 0, 0, LY, -1.1, label=fmt(LY))
    S.north(1545, 122); S.scalebar(0.0, -1.5, 5)
    S.legend(960, 112, [(1, "Montagem: fundo P-E01 → laterais A (P-E02, P-E05) → laterais B (P-E03, P-E06) → frente P-E04 → internos P-I01, P-I02"), (2, "Painéis externos: quadro de 90 mm, OSB 11,1 pregado em fábrica (diafragma) + fita de contraventamento em X"), (3, "Ancoragem (●): parafuso auto-brocante 4,8 x 19 da guia inferior na viga de piso @ 400 + chumbador / cantoneira hold-down nos cantos e nas ombreiras de V1 e P1 a cada ≤ 1,20 m"), (4, "Cantos: montante triplo (ou montante + guia de canto) para receber o gesso e o OSB dos dois painéis"), (5, "Comprimento dos quadros: P-E01 / P-E04 = 3,908 m · P-E02 / 03 / 05 / 06 = 3,364 m · P-I01 = 1,715 m · P-I02 = 2,115 m"), (6, "Paredes com guia superior inclinada (P-E01, P-E04, P-I02) acompanham o telhado: topo 2,80 m no lado alto, 2,20 m no lado baixo")], size=8.5)
    S.save(os.path.join(OUT, "E-03_paineis_planta.svg"))

# ------------------------------------------------------------------------------------------------- E-04 / E-05 elevações dos painéis
def panel_elev(S, p, ox, oy, scale=95.0):
    T = Sheet(1600, 1000, scale, ox, oy)
    L = p["L"]; studs, kings = panel_studs(p)
    ax, c, a0, a1 = p["axis"]
    def top(u):  # altura do topo da guia na posição u do painel
        if not p["slope"]: return p["h0"]
        return p["h0"] + (p["h1"] - p["h0"]) * (u / L)
    # guias
    T.poly([(0, 0), (L, 0), (L, 0.04), (0, 0.04)], fill=TILE, stroke=GREEN, sw=0.9)
    T.poly([(0, top(0) - 0.04), (L, top(L) - 0.04), (L, top(L)), (0, top(0))], fill=TILE, stroke=GREEN, sw=0.9)
    for u in studs:
        T.rect(u - 0.02, 0.04, u + 0.02, top(u) - 0.04, fill=TILE if u not in kings else GREEN, stroke=GREEN, sw=0.6)
    for u in kings: T.rect(u - 0.03, 0.04, u + 0.03, top(u) - 0.04, fill=GREEN, stroke=GREEN, sw=0.6)
    # bloqueadores a meia altura
    for a, b in zip(studs[:-1], studs[1:]):
        if b - a > 0.15: T.rect(a + 0.02, top(a) / 2 - 0.045, b - 0.02, top(a) / 2 + 0.045, fill=S.pattern("hatch"), stroke=GREEN, sw=0.5)
    # aberturas: ombreira, verga, peitoril
    for oc in p["open"]:
        o = OPENS[oc]; a0o = o["a0"]; w = o["w"]; sill = o["sill"]; h = o["h"] if o["h"] else (top(a0o + w / 2) - 0.40)
        T.rect(a0o, sill, a0o + w, sill + h, fill=GLASS if oc[0] in "JV" else CREAM, stroke=GREEN, sw=0.9)
        T.rect(a0o - 0.045, sill + h, a0o + w + 0.045, sill + h + (0.20 if oc == "V1" else 0.09), fill=S.pattern("hatch2"), stroke=GREEN, sw=0.8)   # verga em caixa
        if sill > 0: T.rect(a0o - 0.045, sill - 0.045, a0o + w + 0.045, sill + 0.0, fill=TILE, stroke=GREEN, sw=0.7)
        T.text(a0o + w / 2, sill + h / 2, oc, 11, GREEN, weight=700); T.text(a0o + w / 2, sill + h / 2 - 0.18, f"{int(w * 1000)} x {int(h * 1000)}", 8, EARTH)
        T.dim(a0o, -0.0, a0o + w, -0.0, -0.3, label=fmt(w), size=9)
    # fita X (externos)
    seg = brace_segment(p)
    if seg:
        a, b = seg
        T.line(a, 0.04, b, top(b) - 0.04, EARTH, 1.6, dash="8 4"); T.line(a, top(a) - 0.04, b, 0.04, EARTH, 1.6, dash="8 4")
    # cotas
    T.dim(0, 0, L, 0, -0.62, label=f"{int(round(L * 1000))} mm", size=10)
    T.dim(0, 0, 0, top(0), -0.35, label=f"{int(round(top(0) * 1000))}", size=9); T.dim(L, 0, L, top(L), 0.35, label=f"{int(round(top(L) * 1000))}", size=9)
    T.text(L / 2, max(top(0), top(L)) + 0.30, f"{p['cod']} · {p['nome']}", 11, GREEN, weight=700, spacing=0.08)
    T.text(L / 2, max(top(0), top(L)) + 0.14, f"{len(studs)} montantes Ue 90 @ 400 + {2 * len(kings)} de abertura · guias U 92 · " + ("fita X no trecho cheio" if seg else ("sem fita: pórtico / painéis laterais ⚠️" if p["kind"] == "ext" else "sem fita")), 8.5, EARTH)
    S.parts += T.parts; S.defs += [d for d in T.defs if d not in S.defs]

def sheet_paineis_ext():
    S = Sheet(1600, 1000, 95.0, 0, 0); frame_title(S, "Painéis externos · elevações", "Vista pela face interna · montantes, ombreiras, vergas, bloqueadores, fita X · mm", "E-04", "1:40")
    P = {p["cod"]: p for p in PANELS}
    panel_elev(S, P["P-E01"], 90, 440); panel_elev(S, P["P-E04"], 90, 880)
    panel_elev(S, P["P-E02"], 560, 440); panel_elev(S, P["P-E03"], 560, 880)
    panel_elev(S, P["P-E05"], 1000, 440); panel_elev(S, P["P-E06"], 1000, 880)
    S.text(100, 104, "Elevações no sentido do eixo de cada parede (u = 0 à esquerda) · montantes de abertura (king + jack) em preto · verga em caixa hachurada · bloqueadores a meia altura · fita 50 x 0,95 em X no maior trecho cheio · P-E04: sem fita, contraventamento por pórtico ⚠️", 9.5, EARTH, anchor="start", px=True)
    S.save(os.path.join(OUT, "E-04_paineis_externos.svg"))

def sheet_paineis_int():
    S = Sheet(1600, 1000, 110.0, 0, 0); frame_title(S, "Painéis internos e lista dos painéis", "P-I01 parede molhada · P-I02 banho / quarto com porta P2 · quadro resumo", "E-05", "1:35")
    P = {p["cod"]: p for p in PANELS}
    panel_elev(S, P["P-I01"], 110, 520, 110.0); panel_elev(S, P["P-I02"], 420, 520, 110.0)
    # tabela resumo em SVG
    X0, Y0 = 760, 150
    S.text_px(X0, Y0, "QUADRO DOS PAINÉIS", size=11, weight=700, spacing=0.2, anchor="start")
    cols = [("Painel", 0), ("Quadro (mm)", 70), ("Altura (mm)", 190), ("Montantes", 300), ("Aberturas", 380), ("Fita X", 560), ("Peso aprox. (kg)", 630)]
    for name, dx in cols: S.text_px(X0 + dx, Y0 + 26, name.upper(), size=8, fill=EARTH, anchor="start", spacing=0.1)
    S.add(f'<line x1="{X0}" y1="{Y0 + 32}" x2="{X0 + 760}" y2="{Y0 + 32}" stroke="{GREEN}" stroke-width="0.8"/>')
    for i, p in enumerate(PANELS):
        studs, kings = panel_studs(p); y = Y0 + 52 + i * 22
        hh = f"{int(round(p['h0'] * 1000))}" + (f" → {int(round(p['h1'] * 1000))}" if p["slope"] else "")
        kg = panel_weight(p)
        for (name, dx), val in zip(cols, [p["cod"], f"{int(round(p['L'] * 1000))} x 90", hh, f"{len(studs)} + {2 * len(kings)}", ", ".join(p["open"]) or "—", "sim" if brace_segment(p) else "não", f"≈ {kg:.0f}"]):
            S.text_px(X0 + dx, y, val, size=9.5, anchor="start", weight=600 if dx == 0 else 400)
        S.add(f'<line x1="{X0}" y1="{y + 7}" x2="{X0 + 760}" y2="{y + 7}" stroke="{SAND}" stroke-width="0.6"/>')
    S.text_px(X0, Y0 + 52 + len(PANELS) * 22 + 10, "Peso = perfis + OSB 11,1 (externos) · sem gesso, sem lã · 2 pessoas por painel até 3,4 m; P-E01 / P-E04 com 3 pessoas", size=8.5, fill=EARTH, anchor="start")
    S.text_px(X0, Y0 + 52 + len(PANELS) * 22 + 28, "Paredes internas: Ue 90 @ 400 sem OSB · gesso ST 12,5 (RU no banho e na cozinha) · lã de PET 50 mm acústica", size=8.5, fill=EARTH, anchor="start")
    S.text_px(X0, Y0 + 52 + len(PANELS) * 22 + 46, "⚠️ VALIDAÇÃO OBRIGATÓRIA: vergas (em especial V1, vão 3,70 m), ombreiras e hold-downs conforme cálculo", size=8.5, fill=GREEN, anchor="start", weight=600)
    S.save(os.path.join(OUT, "E-05_paineis_internos.svg"))

def brace_segment(p):
    """maior trecho cheio (sem abertura) do painel externo para a fita X; None se < 0,80 m."""
    if p["kind"] != "ext": return None
    cuts = sorted((OPENS[o]["a0"] - 0.045, OPENS[o]["a0"] + OPENS[o]["w"] + 0.045) for o in p["open"])
    segs = []; u = 0.0
    for a, b in cuts:
        segs.append((u, max(u, a))); u = max(u, b)
    segs.append((u, p["L"]))
    a, b = max(segs, key=lambda t: t[1] - t[0])
    return (a, b) if b - a >= 0.80 else None

def panel_weight(p):
    studs, kings = panel_studs(p); hmax = max(p["h0"], p["h1"])
    kg = (len(studs) + 2 * len(kings)) * (hmax - 0.09) * PROFILES["Ue 90x40x12x0,95"] + 2 * p["L"] * PROFILES["U 92x40x0,95"] + (len(studs) - 1) * 0.36 * PROFILES["Ue 90x40x12x0,95"]
    if p["kind"] == "ext": kg += p["L"] * hmax * 6.8   # OSB 11,1 mm ≈ 6,8 kg/m²
    return kg

# ------------------------------------------------------------------------------------------------- E-06 cobertura
def sheet_cobertura():
    S = new_sheet(); frame_title(S, "Planta da cobertura (estrutura)", "Vigas Ue 200 @ 400 ao longo da queda · bloqueadores · beirais · OSB e telha", "E-06")
    S.rect(0, 0, LX, LY, stroke=GREEN, sw=0.8, dash="6 3")
    S.rect(-BEIRAL_X, -BEIRAL_Y, LX + BEIRAL_X, LY + BEIRAL_Y, stroke=GREEN, sw=1.4)
    xs = [FO + 0.045] + GRID + [LX - FO - 0.045]
    for i, x in enumerate(xs):
        S.rect(x - 0.02, -BEIRAL_Y, x + 0.02, LY + BEIRAL_Y, fill=TILE, stroke=GREEN, sw=0.7)
        if i % 2 == 0: S.text(x, LY + BEIRAL_Y + 0.18, f"{i + 1}", 8, EARTH)
    for yb in (FO + 0.045, LY / 2, LY - FO - 0.045):
        for x0, x1 in zip(xs[:-1], xs[1:]): S.rect(x0 + 0.02, yb - 0.02, x1 - 0.02, yb + 0.02, fill=S.pattern("hatch"), stroke=GREEN, sw=0.5)
    for x in (-BEIRAL_X, LX + BEIRAL_X): S.rect(x - 0.02 if x > 0 else x, -BEIRAL_Y, x + 0.02 if x > 0 else x + 0.04, LY + BEIRAL_Y, fill=TILE, stroke=GREEN, sw=0.8)
    for k in range(11):   # cabeceiras
        y = -BEIRAL_Y + 0.05 + k * 0.45
        S.rect(-BEIRAL_X + 0.04, y - 0.015, FO + 0.025, y + 0.015, fill=TILE, stroke=GREEN, sw=0.5); S.rect(LX - FO - 0.025, y - 0.015, LX + BEIRAL_X - 0.04, y + 0.015, fill=TILE, stroke=GREEN, sw=0.5)
    # setas de queda
    for x in (1.5, 3.5, 5.5):
        S.line(x, 0.6, x, 3.4, EARTH, 1.2); S.poly([(x - 0.12, 3.15), (x + 0.12, 3.15), (x, 3.45)], fill=EARTH, stroke=EARTH)
    S.text(3.5, 2.0, f"queda {SLOPE * 100:.1f} % → lado baixo", 11, EARTH, weight=600)
    S.rect(-BEIRAL_X, LY + BEIRAL_Y, LX + BEIRAL_X, LY + BEIRAL_Y + 0.12, fill=CREAM, stroke=GREEN, sw=0.8); S.text(LX + BEIRAL_X + 0.75, LY + BEIRAL_Y + 0.06, "calha Ø 75 → descida", 9, EARTH)
    S.dim_chain(xs[:6], -BEIRAL_Y - 0.25, -0.35, size=9); S.dim(-BEIRAL_X, -BEIRAL_Y - 0.25, LX + BEIRAL_X, -BEIRAL_Y - 0.25, -0.85, label=fmt(LX + 2 * BEIRAL_X))
    S.dim(LX + BEIRAL_X, -BEIRAL_Y, LX + BEIRAL_X, LY + BEIRAL_Y, 0.55, label=fmt(LY + 2 * BEIRAL_Y))
    S.north(1545, 122); S.scalebar(0.0, -1.5, 5)
    Lr = (LY + 2 * BEIRAL_Y) / math.cos(math.radians(ANG))
    S.legend(960, 112, [(1, f"{len(xs)} vigas de cobertura Ue 200 x 40 x 0,95 @ 400, comprimento {fmt(Lr)} m ao longo da queda ({ANG:.1f}°), apoiadas nas guias superiores das laterais"), (2, "Bloqueadores Ue 200 (0,36 m) sobre as duas laterais e na linha central · cabeceiras de beiral a cada 450 mm na frente e no fundo"), (3, "Sobre as vigas: OSB 18,3 + membrana hidrófuga + contra-ripa / ripa metálica (câmara ventilada 30 mm) + telha metálica trapezoidal 0,50 mm pré-pintada"), (4, "Entre as vigas: lã de vidro 100 mm + barreira de vapor + forro de gesso ST 12,5 (RU no banho) na face inferior"), (5, "Beirais: 0,35 m nas laterais · 0,30 m na frente e no fundo · calha no lado baixo com descida Ø 75 para a drenagem do sítio"), (6, "Ancoragem viga / parede: cantoneira 50 x 50 x 1,25 com 4 parafusos 4,8 x 19 em cada apoio (resistência ao vento ⚠️ cálculo)")], size=8.5)
    S.save(os.path.join(OUT, "E-06_cobertura.svg"))

# ------------------------------------------------------------------------------------------------- E-07 detalhes
def sheet_detalhes():
    S = Sheet(1600, 1000, 1.0, 0, 0); frame_title(S, "Detalhes construtivos típicos", "Base da parede · topo / cobertura · verga em caixa · canto · parede interna · abertura", "E-07", "1:10")
    def det(ox, oy, title, draw, scale=500.0, ty=None):
        T = Sheet(1600, 1000, scale, ox, oy); draw(T); T.text_px(ox - 120, ty or (oy + 150), title, size=10.5, weight=700, anchor="start", spacing=0.08)
        S.parts += T.parts; S.defs += [d for d in T.defs if d not in S.defs]
    def d1(T):   # base da parede externa sobre a plataforma (corte)
        T.rect(-0.30, -0.19, 0.30, -0.18, fill=TILE, stroke=GREEN, sw=0.5)                 # cimentícia inferior
        T.rect(-0.30, -0.18, 0.30, -0.03, fill=T.pattern("insul"), stroke=GREEN, sw=0.7)   # viga de piso / lã
        T.rect(-0.30, -0.03, 0.30, 0.0, fill=WOOD, stroke=GREEN, sw=0.6)                   # OSB 18
        T.rect(0.046, 0.0, 0.136, 0.04, fill=TILE, stroke=GREEN, sw=0.8)                    # guia inferior
        T.rect(0.046, 0.04, 0.136, 0.40, fill=T.pattern("insul"), stroke=GREEN, sw=0.8)     # montante + lã
        T.rect(0.035, 0.0, 0.046, 0.40, fill=WOOD, stroke=GREEN, sw=0.6)                    # OSB 11
        T.rect(0.010, 0.0, 0.035, 0.40, fill="none", stroke=GREEN, sw=0.5, dash="2 2")      # câmara
        T.rect(0.0, -0.10, 0.010, 0.40, fill=TILE, stroke=GREEN, sw=0.6)                    # revestimento (desce 0,10 como pingadeira)
        T.rect(0.136, 0.0, 0.1485, 0.40, fill=SAND, stroke=GREEN, sw=0.6)                   # gesso
        T.rect(0.1485, 0.0, 0.30, 0.012, fill=WOOD2, stroke=GREEN, sw=0.5)                   # piso acabado
        T.line(0.09, 0.04, 0.09, -0.18, GREEN, 1.2); T.circle(0.09, -0.07, 0.006, fill=GREEN, stroke=GREEN)
        T.leader(0.005, 0.30, -0.12, 0.42, "revestimento 10", 8, anchor="end"); T.leader(0.022, 0.25, -0.12, 0.36, "câmara 25 + membrana", 8, anchor="end"); T.leader(0.04, 0.20, -0.12, 0.30, "OSB 11,1", 8, anchor="end")
        T.leader(0.09, 0.15, 0.20, 0.36, "Ue 90 + lã 90", 8); T.leader(0.142, 0.20, 0.20, 0.30, "gesso 12,5", 8); T.leader(0.09, -0.07, 0.20, 0.10, "parafuso 4,8 x 19 @ 400", 8); T.leader(0.0, -0.1, -0.12, -0.12, "pingadeira 100", 8, anchor="end")
        T.dim(0.0, -0.25, 0.1485, -0.25, -0.03, label="150", size=8)
    def d2(T):   # topo da parede / viga de cobertura
        T.rect(0.046, -0.30, 0.136, 0.0, fill=T.pattern("insul"), stroke=GREEN, sw=0.8); T.rect(0.046, 0.0, 0.136, 0.04, fill=TILE, stroke=GREEN, sw=0.8)
        T.rect(0.035, -0.30, 0.046, 0.04, fill=WOOD, stroke=GREEN, sw=0.6); T.rect(0.0, -0.30, 0.010, 0.10, fill=TILE, stroke=GREEN, sw=0.6); T.rect(0.136, -0.30, 0.1485, 0.0, fill=SAND, stroke=GREEN, sw=0.6)
        T.poly([(-0.35, 0.04 + 0.035 * 1), (0.30, 0.04 - 0.035 * 0.9), (0.30, 0.24 - 0.035 * 0.9), (-0.35, 0.24 + 0.035)], fill=T.pattern("insul"), stroke=GREEN, sw=0.8)
        T.poly([(-0.35, 0.24 + 0.035), (0.30, 0.24 - 0.0315), (0.30, 0.26 - 0.0315), (-0.35, 0.26 + 0.035)], fill=WOOD, stroke=GREEN, sw=0.6)
        T.poly([(-0.37, 0.29 + 0.036), (0.30, 0.29 - 0.0315), (0.30, 0.30 - 0.0315), (-0.37, 0.30 + 0.036)], fill=STEEL, stroke=GREEN, sw=0.6)
        T.rect(0.046, 0.04, 0.136, 0.24 - 0.003, fill=T.pattern("hatch"), stroke=GREEN, sw=0.6)   # bloqueador
        T.poly([(0.14, 0.04), (0.19, 0.04), (0.19, 0.09)], fill="none", stroke=GREEN, sw=1.4)      # cantoneira
        T.line(0.136, -0.003, 0.30, -0.003 - 0.0315 * 0.55, SAND, 3)
        T.rect(-0.35, 0.0, -0.33, 0.04 + 0.035, fill=CREAM, stroke=GREEN, sw=0.6)   # testeira
        T.leader(0.0, -0.1, -0.2, -0.15, "beiral 350 ventilado (tela)", 8, anchor="end"); T.leader(0.09, 0.14, 0.22, 0.40, "bloqueador Ue 200", 8); T.leader(0.19, 0.06, 0.22, 0.30, "cantoneira 50 x 50 · 4 parafusos", 8)
        T.leader(-0.1, 0.27 + 0.0035, -0.2, 0.46, "OSB 18,3 + membrana", 8, anchor="end"); T.leader(-0.1, 0.30 + 0.0035, -0.2, 0.52, "ripa + telha metálica", 8, anchor="end"); T.leader(0.2, -0.01, 0.22, 0.20, "forro de gesso", 8)
    def d3(T):   # verga em caixa (corte)
        T.rect(0.0, 0.0, 0.09, 0.09, fill="none", stroke=GREEN, sw=1.2); T.rect(0.0, 0.0, 0.09, 0.09, fill=T.pattern("hatch2"), stroke="none")
        T.line(0.0, 0.0, 0.09, 0.0, GREEN, 2.0); T.line(0.0, 0.09, 0.09, 0.09, GREEN, 2.0)
        T.rect(0.0, -0.045, 0.09, 0.0, fill=TILE, stroke=GREEN, sw=0.8); T.rect(0.0, 0.09, 0.09, 0.135, fill=TILE, stroke=GREEN, sw=0.8)
        T.rect(0.0, 0.135, 0.09, 0.40, fill=T.pattern("insul"), stroke=GREEN, sw=0.7)
        T.rect(0.0, -0.30, 0.09, -0.045, fill=GLASS, stroke=GREEN, sw=0.6)
        T.leader(0.045, 0.045, 0.18, 0.12, "2 x Ue 90 em caixa (vergas ≤ 1,20 m)", 8); T.leader(0.045, 0.112, 0.18, 0.22, "guia U 92 + pernas curtas", 8); T.leader(0.045, -0.02, 0.18, -0.02, "contramarco da esquadria", 8); T.leader(0.045, -0.2, 0.18, -0.15, "vão da abertura", 8)
        T.text(0.045, 0.52, "V1 (3,70 m): 2 x Ue 200 em caixa ⚠️", 8, GREEN, weight=600)
    def d4(T):   # canto em planta
        T.rect(0.0, 0.0, 0.09, 0.30, fill="none", stroke=GREEN, sw=1.0); T.rect(0.0, 0.0, 0.30, 0.09, fill="none", stroke=GREEN, sw=1.0)
        for (x, y) in ((0.0, 0.0), (0.0, 0.05), (0.05, 0.0)):
            T.rect(x, y, x + 0.04, y + 0.09 if x == 0.05 else y + 0.04, fill=TILE, stroke=GREEN, sw=0.7)
        T.rect(0.045, 0.045, 0.09, 0.30, fill=T.pattern("insul"), stroke="none"); T.rect(0.09, 0.045, 0.30, 0.09, fill=T.pattern("insul"), stroke="none")
        T.rect(-0.011, -0.011, 0.0, 0.30, fill=WOOD, stroke=GREEN, sw=0.5); T.rect(-0.011, -0.011, 0.30, 0.0, fill=WOOD, stroke=GREEN, sw=0.5)
        T.rect(0.09, 0.09, 0.1025, 0.30, fill=SAND, stroke=GREEN, sw=0.5); T.rect(0.09, 0.09, 0.30, 0.1025, fill=SAND, stroke=GREEN, sw=0.5)
        T.leader(0.02, 0.02, 0.15, 0.20, "montante triplo de canto (ou montante + guia) · parafusos @ 300", 8); T.leader(-0.005, 0.2, -0.05, 0.28, "OSB", 8, anchor="end"); T.leader(0.096, 0.2, 0.15, 0.28, "gesso", 8)
    def d5(T):   # parede interna molhada (planta) com prumadas
        T.rect(0.0, 0.0, 0.40, 0.09, fill="none", stroke=GREEN, sw=1.0); T.rect(-0.0125, 0.0, 0.0, 0.0, fill="none")
        T.rect(0.0, -0.0125, 0.40, 0.0, fill=SAND, stroke=GREEN, sw=0.5); T.rect(0.0, 0.09, 0.40, 0.1025, fill=SAND, stroke=GREEN, sw=0.5)
        for x in (0.0, 0.40): T.rect(x - 0.02 if x else 0.0, 0.0, x + 0.02 if x else 0.04, 0.09, fill=TILE, stroke=GREEN, sw=0.7)
        T.circle(0.12, 0.045, 0.0125, stroke=GREEN, sw=0.8); T.circle(0.17, 0.045, 0.010, stroke=GREEN, sw=0.8); T.circle(0.26, 0.045, 0.025, stroke=GREEN, sw=0.8)
        T.leader(0.12, 0.045, 0.08, 0.20, "AF 25 / 20", 8); T.leader(0.17, 0.045, 0.17, 0.28, "AQ PEX 16", 8); T.leader(0.26, 0.045, 0.30, 0.20, "ventilação Ø 50", 8)
        T.text(0.20, -0.08, "gesso RU 12,5 (banho) / RU (cozinha) · furos dos montantes com anel plástico · tubos no vão de 90 mm", 8, EARTH)
    def d6(T):   # ombreira / abertura em elevação (king + jack)
        T.rect(0.0, 0.0, 0.045, 0.60, fill=GREEN, stroke=GREEN, sw=0.5); T.rect(0.045, 0.0, 0.09, 0.42, fill=GREEN, stroke=GREEN, sw=0.5)
        T.rect(0.09, 0.42, 0.40, 0.51, fill=T.pattern("hatch2"), stroke=GREEN, sw=0.8); T.rect(0.09, 0.51, 0.40, 0.60, fill=T.pattern("insul"), stroke=GREEN, sw=0.5)
        T.rect(0.09, 0.0, 0.40, 0.42, fill=GLASS, stroke=GREEN, sw=0.6)
        T.leader(0.022, 0.5, 0.10, 0.70, "king: inteiro, da guia inferior à superior", 8); T.leader(0.067, 0.3, 0.12, 0.64, "jack: apoia a verga", 8); T.leader(0.25, 0.465, 0.30, 0.58, "verga em caixa", 8)
    det(250, 420, "D1 · Base da parede externa sobre a plataforma", d1, 480.0, 585)
    det(660, 420, "D2 · Topo da parede · viga de cobertura · beiral", d2, 480.0, 585)
    det(1020, 420, "D3 · Verga em caixa (corte)", d3, 480.0, 585)
    det(1300, 400, "D4 · Canto (planta)", d4, 480.0, 585)
    det(200, 880, "D5 · Parede molhada P-I01 (planta)", d5, 480.0, 945)
    det(560, 940, "D6 · Abertura: king + jack + verga (elevação)", d6, 400.0, 975)
    S.text_px(830, 640, "REGRAS DE FABRICAÇÃO DOS PAINÉIS", size=10.5, weight=700, anchor="start", spacing=0.15)
    rules = ["Perfis ZAR-275, 0,95 mm, galvanizados (NBR 15253) · guias U 92 / U 152 / U 203 · montantes e vigas Ue",
             "Montantes encaixados nas guias com abas para dentro; 2 parafusos 4,2 x 13 cabeça lentilha por encontro",
             "Furos de passagem de instalações alinhados (puncionados de fábrica), Ø 38 x 50 mm oblongos, no terço médio da alma",
             "OSB 11,1 mm na face externa, pregado / parafusado @ 150 mm nas bordas e 300 mm no meio, juntas sobre montante",
             "Fita X 50 x 0,95 pré-tensionada com chapas de canto 150 x 150 x 1,25 · bloqueadores a meia altura",
             "Marcação a tinta no quadro: código do painel, lado interno, 'CIMA', posição das aberturas e dos pontos de instalação",
             "Tolerâncias: comprimento ± 2 mm · esquadro (diagonais) ± 3 mm · prumo na montagem 1/500",
             "Embalagem: painéis em pé, em cavaletes, com cantoneiras de proteção; perfis soltos amarrados por código",
             "⚠️ VALIDAÇÃO OBRIGATÓRIA — ENGENHEIRO/ARQUITETO: espessuras, vergas, hold-downs e fixações conforme cálculo e NBR 15253 / 6355"]
    for i, r in enumerate(rules): S.text_px(830, 665 + i * 19, ("• " if not r.startswith("⚠") else "") + r, size=9, anchor="start", fill=GREEN if r.startswith("⚠") else GREEN, weight=600 if r.startswith("⚠") else 400)
    S.save(os.path.join(OUT, "E-07_detalhes.svg"))

# ------------------------------------------------------------------------------------------------- E-00 isométrica do esqueleto
def sheet_isometrica():
    S = Sheet(1600, 1000, 1.0, 0, 0); frame_title(S, "Isométrica do esqueleto LSF", "Plataforma · painéis de parede · vigas de cobertura · sem fechamentos", "E-00", "s/ escala")
    sc, ox, oy = 95.0, 860, 760
    def L3(p, q, col=GREEN, sw=0.9, op=1.0):
        a = iso_project(p, sc, ox, oy); b = iso_project(q, sc, ox, oy)
        S.add(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-width="{sw}" opacity="{op}" stroke-linecap="round"/>')
    z0 = -0.18
    # vigas de fundação
    for y in (FO + 0.045, LY / 2, LY - FO - 0.045): L3((0.0, y, -0.38), (LX, y, -0.38), EARTH, 2.2); L3((0.0, y, -0.18), (LX, y, -0.18), EARTH, 1.2)
    for x, y in PADS: L3((x, y, -0.65), (x, y, -0.38), EARTH, 2.6)
    # plataforma
    xs = [FO + 0.045] + GRID + [LX - FO - 0.045]
    for x in xs: L3((x, FO, z0), (x, LY - FO, z0), GREEN, 0.9)
    for y in (FO, LY - FO): L3((FO, y, z0), (LX - FO, y, z0), GREEN, 1.4)
    for y in (FO, LY - FO): L3((FO, y, 0.0), (LX - FO, y, 0.0), GREEN, 0.5)
    # paredes
    for p in PANELS:
        ax, c, a0, a1 = p["axis"]; studs, kings = panel_studs(p)
        def pt(u, z): return (a0 + u, c, z) if ax == "x" else (c, a0 + u, z)
        def top(u): return p["h0"] + (p["h1"] - p["h0"]) * (u / p["L"]) if p["slope"] else p["h0"]
        col = GREEN if p["kind"] == "ext" else EARTH
        L3(pt(0, 0.0), pt(p["L"], 0.0), col, 1.4); L3(pt(0, top(0)), pt(p["L"], top(p["L"])), col, 1.4)
        for u in studs: L3(pt(u, 0.0), pt(u, top(u)), col, 0.8 if u not in kings else 1.6)
        for oc in p["open"]:
            o = OPENS[oc]; a = o["a0"]; w = o["w"]; sill = o["sill"]; hh = o["h"] if o["h"] else top(a + w / 2) - 0.40
            for u in (a, a + w): L3(pt(u, sill), pt(u, sill + hh), col, 1.6)
            L3(pt(a, sill + hh), pt(a + w, sill + hh), col, 1.6)
            if sill > 0: L3(pt(a, sill), pt(a + w, sill), col, 1.2)
    # cobertura
    for x in xs: L3((x, -BEIRAL_Y, ztop(-BEIRAL_Y) + 0.1), (x, LY + BEIRAL_Y, ztop(LY + BEIRAL_Y) + 0.1), STEEL, 1.0)
    for y in (-BEIRAL_Y, LY + BEIRAL_Y): L3((-BEIRAL_X, y, ztop(y) + 0.1), (LX + BEIRAL_X, y, ztop(y) + 0.1), STEEL, 1.4)
    L3((-BEIRAL_X, -BEIRAL_Y, ztop(-BEIRAL_Y) + 0.1), (-BEIRAL_X, LY + BEIRAL_Y, ztop(LY + BEIRAL_Y) + 0.1), STEEL, 1.4); L3((LX + BEIRAL_X, -BEIRAL_Y, ztop(-BEIRAL_Y) + 0.1), (LX + BEIRAL_X, LY + BEIRAL_Y, ztop(LY + BEIRAL_Y) + 0.1), STEEL, 1.4)
    # deck
    for (x0, y0, x1, y1) in ((LX, 0, LX + 2, 0), (LX + 2, 0, LX + 2, LY), (LX, LY, LX + 2, LY), (LX, 0, LX, LY)): L3((x0, y0, -0.05), (x1, y1, -0.05), WOOD2, 1.2)
    # rótulos
    def lab(p, s, size=10, col=GREEN):
        a = iso_project(p, sc, ox, oy); S.text_px(a[0], a[1], s, size=size, fill=col, weight=600)
    lab((LX / 2, -0.9, 0.0), "P-E02 / P-E03 · lado alto (entrada)"); lab((LX / 2, LY + 0.9, 0.0), "P-E05 / P-E06 · lado baixo"); lab((-0.9, LY / 2, 1.5), "P-E01 fundo"); lab((LX + 1.0, LY / 2, 2.9), "P-E04 vidro")
    lab((LX / 2, LY / 2, 3.6), "19 vigas de cobertura Ue 200 @ 400", 10, STEEL); lab((LX + 1.0, LY / 2, -0.4), "deck", 9, WOOD2); lab((LX / 2, LY / 2, -0.9), "15 apoios · 3 vigas de fundação", 10, EARTH)
    S.text_px(70, 130, "Esqueleto completo em aço leve galvanizado: tudo parafusado, sem solda em campo, nenhuma peça maior que 4,80 m. Fechamentos (OSB, membranas, lã, gesso, telha, revestimento) e instalações nas pranchas seguintes.", size=10, fill=EARTH, anchor="start")
    S.save(os.path.join(OUT, "E-00_isometrica.svg"))

# ------------------------------------------------------------------------------------------------- H-01 hidráulica · H-02 esgoto · L-01 elétrica
def sheet_hidraulica():
    S = new_sheet(); frame_title(S, "Hidráulica · água fria e quente", "Pontos, prumadas na parede molhada, entrada pela parede de fundo · alturas do piso acabado", "H-01")
    walls_plan(S, cut=False); deck_plan(S, light=True); furniture(S)
    # redes
    AF = "#2E6E9E"; AQ = "#B2452B"
    path_af = [(0.0, 2.20), (0.12, 2.20), (0.12, WET_Y0 + 0.05), (0.80, WET_Y0 + 0.05)]
    S.poly(path_af, fill="none", stroke=AF, sw=2.0, close=False)
    S.poly([(0.12, 2.20), (0.12, 0.55), (IX0, 0.55)], fill="none", stroke=AF, sw=1.6, close=False)                       # vaso
    S.poly([(0.12, 0.55), (0.12, 0.10), (BATH["x1"] - 0.30, 0.10), (BATH["x1"] - 0.30, IY0)], fill="none", stroke=AF, sw=1.6, close=False)   # lavatório
    S.poly([(0.12, WET_Y1 + 0.0), (0.45, WET_Y1 + 0.03), (0.45, WET_Y1)], fill="none", stroke=AF, sw=1.6, close=False)   # pia
    S.poly([(0.12, 3.70), (0.12, 3.93), (LX, 3.93), (LX, 3.60)], fill="none", stroke=AF, sw=1.2, close=False, dash="6 3")   # torneira externa (opcional)
    S.poly([(0.0, 2.60), (0.09, 2.60), (0.09, WET_Y0 + 0.08), (0.80, WET_Y0 + 0.08)], fill="none", stroke=AQ, sw=1.6, close=False, dash="5 3")   # AQ chuveiro
    S.poly([(0.09, 2.60), (0.09, 0.07), (BATH["x1"] - 0.30, 0.07), (BATH["x1"] - 0.30, IY0)], fill="none", stroke=AQ, sw=1.2, close=False, dash="5 3")
    S.poly([(0.09, 2.60), (0.45, 2.60), (0.45, WET_Y1)], fill="none", stroke=AQ, sw=1.2, close=False, dash="5 3")
    for cod, desc, x, y, hh, rede, dia in HID:
        col = AQ if rede == "AQ" else AF
        S.circle(x, y, 0.09, fill=CREAM, stroke=col, sw=1.4); S.text(x, y, cod, 7.5, col, weight=700, dy=3)
        S.text(x + (0.0 if abs(x) > 0.01 else -0.6), y + 0.22, f"h {fmt(hh)}", 7, EARTH)
    S.dim(0, 0, LX, 0, -0.55, label=fmt(LX)); S.north(1545, 122); S.scalebar(0.0, -1.05, 5)
    S.legend(960, 112, [(1, "Água fria PVC soldável 25 mm (ramal) / 20 mm (sub-ramais) dentro do vão dos montantes, furos com anel"), (2, "Água quente PEX 16 mm (tracejado) do aquecedor até chuveiro, lavatório e pia; base do kit: chuveiro elétrico (sem AQ)"), (3, "Registro geral + ponto de medição na face externa do fundo (AF-0) · pressão mínima 10 m.c.a. da rede do empreendimento (ou pressurizador)"), (4, "Sem reservatório na cabana: reservatório e tratamento ficam no sítio (projeto hidráulico do empreendimento ⚠️)"), (5, "Todos os pontos no núcleo: prumadas na parede molhada P-I01 e na parede de fundo P-E01 · uma só descida"), (6, "⚠️ VALIDAÇÃO OBRIGATÓRIA: diâmetros e pressões conforme NBR 5626 e projeto do sítio")], size=8.5)
    S.save(os.path.join(OUT, "H-01_hidraulica.svg"))

def sheet_esgoto():
    S = new_sheet(); frame_title(S, "Esgoto e ventilação", "Sob a plataforma de piso · caixa sifonada · tubo ventilador · saída única no fundo", "H-02")
    walls_plan(S, cut=False); deck_plan(S, light=True); furniture(S)
    ES = "#5B5B3C"
    S.poly([(0.95, BATH["y1"] - 0.08), (0.95, 1.55)], fill="none", stroke=ES, sw=1.8, close=False)                         # ralo → CS
    S.poly([(BATH["x1"] - 0.30, IY0 + 0.10), (BATH["x1"] - 0.30, 1.40), (0.95, 1.55)], fill="none", stroke=ES, sw=1.4, close=False)   # lavatório → CS
    S.poly([(0.95, 1.55), (0.45, 1.00), (0.0, 1.00)], fill="none", stroke=ES, sw=2.2, close=False)                           # CS → coletor
    S.poly([(IX0 + 0.35, 0.55), (0.45, 0.85), (0.45, 1.00)], fill="none", stroke=ES, sw=3.0, close=False)                     # vaso 100
    S.poly([(0.45, WET_Y1 + 0.30), (0.45, WET_Y1 + 0.60), (-0.6, WET_Y1 + 0.60), (-0.6, 1.00)], fill="none", stroke=ES, sw=1.6, close=False, dash="6 3")   # pia → caixa de gordura externa
    S.rect(-0.85, WET_Y1 + 0.40, -0.45, WET_Y1 + 0.80, fill=CREAM, stroke=ES, sw=1.0); S.text(-0.65, WET_Y1 + 1.0, "CG", 8, ES, weight=700)
    for cod, desc, x, y, dia, dest in ESG:
        S.circle(x, y, 0.10, fill=CREAM, stroke=ES, sw=1.4); S.text(x, y, cod, 7, ES, weight=700, dy=3); S.text(x, y - 0.25, dia, 7, EARTH)
    S.text(0.45, 1.25, "i ≥ 2 %", 7, EARTH); S.text(0.2, 1.12, "Ø100", 7, EARTH)
    S.poly([(-0.0, 1.00), (-1.1, 1.00)], fill="none", stroke=ES, sw=2.2, close=False); S.poly([(-1.1, 1.0), (-0.95, 1.08), (-0.95, 0.92)], fill=ES, stroke=ES)
    S.text(-1.2, 1.25, "para o destino do sítio", 8, ES, anchor="end"); S.text(-1.2, 1.05, "(rede · ETE · fossa + filtro + sumidouro, se o solo e a prefeitura permitirem)", 7, EARTH, anchor="end")
    S.dim(0, 0, LX, 0, -0.55, label=fmt(LX)); S.north(1545, 122); S.scalebar(0.0, -1.05, 5)
    S.legend(960, 112, [(1, "Tubulação de esgoto PVC branco sob a plataforma (vão ventilado de 0,65 m, acessível): vaso Ø 100 direto ao coletor; box e lavatório na caixa sifonada CS-1"), (2, "Caixa sifonada 100 x 150 x 50 com tampa cega no piso do box · caimento ≥ 2 % (Ø 40/50) e ≥ 1 % (Ø 100) conforme NBR 8160"), (3, "Pia da cozinha Ø 50 para caixa de gordura externa (obra do sítio) e desta ao coletor"), (4, "Tubo ventilador Ø 50 na parede molhada P-I01, saindo 0,30 m acima da telha com terminal"), (5, "Saída S Ø 100 na face de fundo a − 0,25 m do piso · a cabana entrega esgoto num só ponto; destino, tratamento e licenças são do sítio"), (6, "⚠️ Regra do projeto: fossa não é solução universal; depende do terreno e da prefeitura")], size=8.5)
    S.save(os.path.join(OUT, "H-02_esgoto.svg"))

def sheet_eletrica():
    S = new_sheet(); frame_title(S, "Elétrica · pontos e circuitos", "Iluminação, tomadas, chuveiro, cooktop, split · alturas do piso acabado · alimentação pela parede de fundo", "L-01")
    walls_plan(S, cut=False); deck_plan(S, light=True); furniture(S)
    EL = "#8A5A00"
    for cod, desc, x, y, hh, circ in ELE:
        if cod.startswith("L"):
            S.circle(x, y, 0.11, fill=CREAM, stroke=EL, sw=1.2); S.line(x - 0.08, y - 0.08, x + 0.08, y + 0.08, EL, 1.0); S.line(x - 0.08, y + 0.08, x + 0.08, y - 0.08, EL, 1.0)
        elif cod.startswith("S"):
            S.circle(x, y, 0.07, fill=EL, stroke=EL);
        elif cod.startswith("T") or cod in ("CH", "CK"):
            S.add(f'<path d="M{S.X(x - 0.10):.1f},{S.Y(y):.1f} A{0.10 * S.s:.1f},{0.10 * S.s:.1f} 0 0 1 {S.X(x + 0.10):.1f},{S.Y(y):.1f}" fill="{CREAM}" stroke="{EL}" stroke-width="1.3"/>'); S.line(x - 0.10, y, x + 0.10, y, EL, 1.3)
        elif cod == "QDC": S.rect(x - 0.05, y - 0.25, x + 0.12, y + 0.25, fill=EL, stroke=EL)
        elif cod in ("AC", "ACx"): S.rect(x - 0.40, y - 0.12, x + 0.40, y + 0.12, fill=CREAM, stroke=EL, sw=1.2, dash="3 2")
        elif cod == "ENT": S.circle(x, y, 0.09, fill=CREAM, stroke=EL, sw=2.0)
        S.text(x, y + 0.20, cod, 7.5, EL, weight=700); S.text(x, y - 0.26, f"{circ} · h {fmt(hh)}" if circ != "—" else f"h {fmt(hh)}", 6.5, EARTH)
    # eletrodutos (esquemático): QDC → circuitos pela parede de fundo e laterais
    S.poly([(IX0, 3.70), (0.10, 3.70), (0.10, 0.10), (6.75, 0.10)], fill="none", stroke=EL, sw=0.8, close=False, dash="2 3")
    S.poly([(0.10, 3.90), (6.80, 3.90)], fill="none", stroke=EL, sw=0.8, close=False, dash="2 3")
    S.poly([(0.10, WET_Y0 + 0.05), (PI2_X1, WET_Y0 + 0.05), (PI2_X1, 0.5)], fill="none", stroke=EL, sw=0.8, close=False, dash="2 3")
    S.dim(0, 0, LX, 0, -0.55, label=fmt(LX)); S.north(1545, 122); S.scalebar(0.0, -1.05, 5)
    S.legend(960, 112, [(1, "⊗ ponto de luz · ● interruptor · ⌓ tomada · ▮ QDC · ◎ entrada de energia · ▭ split"), (2, "Entrada 220 V monofásica (padrão Celesc no sítio) · eletroduto 32 mm pela parede de fundo até o QDC na cozinha"), (3, "QDC 12 posições: geral + DR 30 mA + DPS · 6 circuitos + 2 reservas (tabela na memória)"), (4, "Eletrodutos corrugados 25 mm nos furos dos montantes (anel plástico) · caixas 4 x 2 nas alturas indicadas · cabos flexíveis 750 V"), (5, "Chuveiro elétrico 7 500 W (C4, 6 mm²) é a base; com aquecedor a gás, C4 vira reserva · Split 9 a 12 k BTU"), (6, "⚠️ VALIDAÇÃO OBRIGATÓRIA: dimensionamento, disjuntor geral e aterramento conforme NBR 5410 e concessionária")], size=8.5)
    S.save(os.path.join(OUT, "L-01_eletrica.svg"))

# ------------------------------------------------------------------------------------------------- M-xx etapas (manual)
def sheet_etapa(n, title, sub, draw, file):
    S = new_sheet(); frame_title(S, f"Montagem · etapa {n}", sub, f"M-{n:02d}", "1:50")
    draw(S); S.north(1545, 122); S.scalebar(0.0, -1.05, 5); S.text(0.0, -0.75, title, 11, GREEN, weight=600, anchor="start", spacing=0.1)
    S.save(os.path.join(OUT, file))

def stage_sheets():
    def s1(S):
        S.rect(0, 0, LX, LY, stroke=GREEN, sw=0.8, dash="6 3"); deck_plan(S, light=True)
        for i, (x, y) in enumerate(PADS): S.rect(x - 0.25, y - 0.25, x + 0.25, y + 0.25, fill=TILE, stroke=GREEN, sw=0.9); S.text(x, y - 0.4, f"F{i + 1:02d}", 8, EARTH)
        S.line(-0.6, -0.6, LX + 2.6, -0.6, EARTH, 0.8, dash="4 3"); S.line(-0.6, -0.6, -0.6, LY + 0.6, EARTH, 0.8, dash="4 3"); S.text(-0.75, LY / 2, "linha de referência (gabarito de madeira)", 8, EARTH, rotate=-90)
        S.text(LX / 2, LY + 0.5, "diagonais iguais ± 10 mm · cota de topo das sapatas ± 5 mm", 9, EARTH)
    def s2(S):
        for i, y in enumerate((FO + 0.045, LY / 2, LY - FO - 0.045)): S.rect(0.0, y - 0.10, LX, y + 0.10, fill=TILE, stroke=GREEN, sw=1.0); S.text(-0.45, y, f"VF0{i + 1}", 9, GREEN, weight=600)
        xs = [FO + 0.045] + GRID + [LX - FO - 0.045]
        for x in xs: S.rect(x - 0.02, FO, x + 0.02, LY - FO, fill=TILE, stroke=GREEN, sw=0.6)
        S.rect(FO, FO, LX - FO, LY - FO, stroke=GREEN, sw=1.4); S.rect(FO, FO, FO + 2.40, FO + 1.20, fill=WOOD, stroke=GREEN, sw=0.8); S.text(FO + 1.2, FO + 0.6, "OSB 1", 9, GREEN)
        S.text(LX / 2, LY + 0.5, "nivelar as vigas de fundação nos pedestais · fixar as bordas · vigas @ 400 · OSB com juntas desencontradas", 9, EARTH)
    def s3(S):
        walls_plan(S, cut=False)
        order = [("P-E01", 0.55, 2.0), ("P-E02", 1.75, 0.45), ("P-E05", 1.75, 3.55), ("P-E03", 5.25, 0.45), ("P-E06", 5.25, 3.55), ("P-E04", 6.45, 2.0), ("P-I01", 1.3, 2.4), ("P-I02", 2.1, 1.0)]
        for n, (cod, x, y) in enumerate(order, 1): S.callout(x, y, n); S.text(x, y - 0.3, cod, 8, EARTH, weight=600)
        S.line(0.5, 2.0, 0.5, 1.0, EARTH, 1.0); S.text(LX / 2, LY + 0.5, "erguer na ordem 1 → 8 · escorar com mãos-francesas · prumo 1/500 · parafusar guia inferior @ 400 e cantos", 9, EARTH)
    def s4(S):
        S.rect(0, 0, LX, LY, stroke=GREEN, sw=0.8, dash="6 3"); S.rect(-BEIRAL_X, -BEIRAL_Y, LX + BEIRAL_X, LY + BEIRAL_Y, stroke=GREEN, sw=1.2)
        xs = [FO + 0.045] + GRID + [LX - FO - 0.045]
        for i, x in enumerate(xs): S.rect(x - 0.02, -BEIRAL_Y, x + 0.02, LY + BEIRAL_Y, fill=TILE if i < 10 else "none", stroke=GREEN, sw=0.7, dash=None if i < 10 else "3 2")
        S.poly([(xs[10], -0.9), (xs[10] + 1.0, -0.9)], fill="none", stroke=EARTH, sw=1.2, close=False); S.poly([(xs[10] + 1.0, -0.9), (xs[10] + 0.85, -0.82), (xs[10] + 0.85, -0.98)], fill=EARTH, stroke=EARTH)
        S.text(xs[10] + 1.3, -0.9, "sentido de colocação das vigas (do fundo para a frente)", 8, EARTH, anchor="start")
        S.text(LX / 2, LY + 0.75, "vigas Ue 200 @ 400 sobre as guias · cantoneira em cada apoio · bloqueadores · OSB 18,3 · membrana · ripas · telha · calha", 9, EARTH)
    def s5(S):
        walls_plan(S, cut=False); furniture(S)
        for cod, desc, x, y, hh, rede, dia in HID: S.circle(x, y, 0.08, fill="#2E6E9E", stroke="#2E6E9E")
        for cod, desc, x, y, hh, circ in ELE: S.circle(x, y, 0.06, fill="#8A5A00", stroke="#8A5A00")
        S.text(LX / 2, LY + 0.5, "antes do gesso: eletrodutos, caixas, tubos de água e ventilação nos furos dos montantes · teste de pressão 24 h · foto de cada parede", 9, EARTH)
    def s6(S):
        walls_plan(S, cut=False); deck_plan(S); furniture(S); room_labels(S)
        S.text(LX / 2, LY + 0.5, "lã, gesso, impermeabilização e revestimento do banho, pisos, esquadrias V1 / P1 / J1-J4, louças, metais, QDC, deck, limpeza e testes", 9, EARTH)
    sheet_etapa(1, "ETAPA 1 · LOCAÇÃO E FUNDAÇÃO · 15 apoios + 6 do deck", "Gabarito, diagonais, cota de topo, sapatas ou estacas, pedestais reguláveis", s1, "M-01_fundacao.svg")
    sheet_etapa(2, "ETAPA 2 · VIGAS DE FUNDAÇÃO E PLATAFORMA DE PISO", "Caixões nivelados, bordas, vigas @ 400, bloqueadores, OSB 18,3, fechamento inferior", s2, "M-02_plataforma.svg")
    sheet_etapa(3, "ETAPA 3 · PAINÉIS DE PAREDE · ORDEM 1 → 8", "Fundo, laterais A, laterais B, frente, internos · escoras, prumo, ancoragem", s3, "M-03_paineis.svg")
    sheet_etapa(4, "ETAPA 4 · COBERTURA", "Vigas Ue 200, bloqueadores, cabeceiras, OSB, membrana, ripas, telha, calha", s4, "M-04_cobertura.svg")
    sheet_etapa(5, "ETAPA 5 · INSTALAÇÕES DENTRO DOS PAINÉIS", "Hidráulica (azul) e elétrica (ocre) passadas antes do fechamento interno", s5, "M-05_instalacoes.svg")
    sheet_etapa(6, "ETAPA 6 · FECHAMENTOS, ESQUADRIAS, ACABAMENTOS E DECK", "Lã, gesso, banho, pisos, esquadrias, louças, QDC, deck, testes", s6, "M-06_acabamentos.svg")

def build_all():
    sheet_planta(); sheet_cortes(); sheet_fachadas(); sheet_isometrica(); sheet_fundacao(); sheet_plataforma(); sheet_paineis_planta(); sheet_paineis_ext(); sheet_paineis_int(); sheet_cobertura(); sheet_detalhes(); sheet_hidraulica(); sheet_esgoto(); sheet_eletrica(); stage_sheets()
    print("desenhos ->", OUT)

if __name__ == "__main__":
    build_all()
    rows, tot = members_summary()
    for r in rows: print(r)
    print("total kg", tot)
    for p in PANELS: print(p["cod"], round(p["L"], 3), panel_studs(p), round(panel_weight(p)))

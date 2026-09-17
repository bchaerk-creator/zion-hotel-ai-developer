# -*- coding: utf-8 -*-
"""Listas de materiais, componentes de fabricação, pesos, transporte e cronograma de montagem (calculados a partir da geometria)."""
import math, json
from geometry import Cocoon, Zenith, Lodge

C, Z, LD = Cocoon(), Zenith(), Lodge()

# massas lineares (kg/m) de tubos e perfis de aço
KG = {"Ø139,7 x 4,5": 15.0, "Ø114,3 x 4,0": 10.9, "Ø101,6 x 4,0": 9.63, "Ø88,9 x 3,6": 7.57, "Ø76,1 x 3,6": 6.44,
      "Ø60,3 x 3,0": 4.24, "Ø48,3 x 3,0": 3.35, "Ø42,4 x 3,0": 2.91, "Ø26,9 x 2,6": 1.56,
      "150 x 100 x 4,0": 15.0, "100 x 50 x 3,0": 6.71, "U 150 x 60 x 3,0": 6.5, "chapa 80 x 10": 6.28,
      "Ue 150 x 40 x 1,25": 2.5}   # vigota LSF dos módulos de piso do Lodge

def r(v, n=0):
    return round(v, n) if n else int(round(v))

def cocoon_bom():
    L = C.arch_lengths()
    memb, glass = C.membrane_area()
    bico = C.bico_area(); BT = C.bico_tube_lengths()
    memb = memb + bico
    floor = C.floor_area() + 2.4
    deck = (C.DECK["x2"] - C.DECK["x1"]) * (C.DECK["y2"] - C.DECK["y1"])
    steel = [
        ("A0", "Anel frontal inclinado 8°", "Ø101,6 x 4,0", 1, L[0], KG["Ø101,6 x 4,0"]),
        ("BC", "Bico: cumeeira em balanço (A1 → ponta), engastada em A0 e A1", "Ø114,3 x 4,0", 1, BT["ridge"], KG["Ø114,3 x 4,0"]),
        ("BB", "Bico: tubos de borda curvados (ponta → anel A0)", "Ø60,3 x 3,0", 2, 2 * BT["edge"], KG["Ø60,3 x 3,0"]),
        ("BR", "Bico: costela intermediária curvada", "Ø48,3 x 3,0", 1, BT["rib"], KG["Ø48,3 x 3,0"]),
        ("BT", "Bico: tirantes Ø12 inox + esticadores", "cabo", 2, 2 * BT["tie"], 0.7),
        ("A1-A7", "Arcos elípticos (3 segmentos cada)", "Ø88,9 x 3,6", 7, sum(L[1:]), KG["Ø88,9 x 3,6"]),
        ("T1-T7", "Terças longitudinais em trechos de 1,20 m", "Ø48,3 x 3,0", 7, 7 * 8.75, KG["Ø48,3 x 3,0"]),
        ("EL", "Espinha de Luz: banzos + diagonais", "Ø42,4 x 3,0 / Ø26,9 x 2,6", 1, 4.7 * 2 + 9.0, 2.4),
        ("TB", "Trilhos de base curvados", "100 x 50 x 3,0", 2, 2 * 9.0, KG["100 x 50 x 3,0"]),
        ("QC", "Quadro da cauda", "Ø60,3 x 3,0", 1, 7.5, KG["Ø60,3 x 3,0"]),
        ("LV", "Luvas internas Ø76 x 200 (21 un.)", "Ø76,1 x 3,6", 21, 21 * 0.2, KG["Ø76,1 x 3,6"]),
        ("CH", "Chapas de base 200 x 150 x 10 + enrijecedores (16 un.)", "chapa", 16, 16, 2.6),
        ("CB", "Cabos inox Ø8 + esticadores + olhais", "cabo", 8, 8 * 6.0, 0.35),
        ("PF", "Parafusos, chumbadores, presilhas keder", "ferragens", 1, 1, 45.0),
    ]
    steel_rows = [(c, d, s, q, r(l, 1), r(l * k)) for (c, d, s, q, l, k) in steel]
    steel_kg = sum(x[5] for x in steel_rows)
    alu = [("KD", "Perfil duplo keder de alumínio sobre arcos", 8, r(sum(L), 1), 0.9), ("AV", "Anel curvo da fachada 120 x 60", 1, 10.2, 2.5),
           ("MT", "Montantes e travessa da fachada", 5, 14.0, 1.8), ("TF", "Trilho do forro tensionado", 1, 60.0, 0.35), ("RQ", "Requadros das Janelas Olho (madeira laminada)", 6, 6, 9.0)]
    alu_rows = [(c, d, q, l, r(l * k)) for (c, d, q, l, k) in alu]
    alu_kg = sum(x[4] for x in alu_rows)
    env = [("Membrana PVDF 1050 g/m² (+15% emendas/bolsas)", "m²", r(memb * 1.15), r(memb * 1.15 * 1.05)),
           ("Lã de PET 50 mm, 25 kg/m³", "m²", r(memb), r(memb * 1.25)),
           ("Manta refletiva de alumínio (bolha)", "m²", r(memb), r(memb * 0.25)),
           ("Forro tensionado Trevira CS", "m²", r(memb * 0.95), r(memb * 0.95 * 0.3)),
           ("Painéis ripados internos (cabeceira, rodapés)", "m²", 14, 14 * 9)]
    front_glass = 0.8 * math.pi * (C.a(C.X_GLASS) - 0.06) * (C.b(C.X_GLASS) - 0.06)
    lens = 4 * 0.6 + 2 * 0.35   # 4 lentes 0,95 x 0,80 + 2 de 0,80 x 0,55 (áreas elípticas)
    spine = 4.7 * 0.7
    glz = [("Fachada de vidro duplo 6 lam + 12 Ar + 6 temp low-e (anel inclinado)", "m²", r(front_glass, 1), r(front_glass * 30)),
           ("Porta pivotante 1,00 x 2,40 (incluída na fachada)", "un", 1, 65),
           ("Janelas Olho: vidro duplo curvo-facetado, 2 basculantes", "m²", r(lens, 1), r(lens * 32)),
           ("Espinha de Luz: 4 painéis laminados 8 + 8 mm", "m²", r(spine, 1), r(spine * 40)),
           ("Esquadrias de alumínio bronze com ruptura térmica", "kg", 120, 120)]
    flr = [("Vigas U 150 x 60 x 3,0 galvanizadas (malha 2,4 m, piso + deck)", "m", 128, r(128 * 6.5)),
           ("Vigotas 50 x 150 tratadas a cada 400 mm", "m", r((floor + deck) * 2.5), r((floor + deck) * 9.4)),
           ("PIR 50 mm entre vigotas + manta inferior", "m²", r(floor), r(floor * 2.1)),
           ("Compensado naval 18 mm", "m²", r(floor), r(floor * 12)),
           ("Piso de engenharia carvalho 14 mm", "m²", r(floor - 13.2), r((floor - 13.2) * 9)),
           ("Zona molhada: placa cimentícia + impermeabilização + porcelanato", "m²", 13, 13 * 30),
           ("Deck cumaru 20 x 140 com fixação oculta", "m²", r(deck), r(deck * 20)),
           ("Estacas helicoidais Ø76, hélice Ø300, L 2,0 m + cabeçotes", "un", 44, r(44 * 18.8))]
    interiors = [("Parede da cabeceira / banho (LSF + painel + ripado)", "m²", 16, 16 * 22),
                 ("Marcenaria: console café, armário baixo, criados, bancada", "cj", 1, 260),
                 ("Cama king, chaise, poltrona, mesa", "cj", 1, 190),
                 ("Louças e metais: bacia, bancada, chuveiro, banheira 1,55", "cj", 1, 170),
                 ("Box de vidro do chuveiro", "un", 1, 35)]
    mep = [("Evaporadora dutada 12k BTU inverter + condensadora + dutos + difusores", "cj", 1, 95),
           ("Aquecedor a gás 23 L/min (ou bomba de calor 200 L)", "un", 1, 25),
           ("Quadro elétrico, cabos, fitas LED, luminárias, tomadas", "cj", 1, 70),
           ("Tubulações PEX / esgoto / ventilação / caixa de gordura", "cj", 1, 45),
           ("Exaustor com recuperação de calor + respiro de cumeeira", "cj", 1, 15)]
    groups = [("Estrutura metálica (aço galvanizado)", [(d, "kg", q, k) for (_, d, _, q, l, k) in steel_rows]),
              ("Alumínio e requadros", [(d, "un", q, k) for (_, d, q, l, k) in alu_rows]),
              ("Envelope: membrana, isolamento, forro", env), ("Vidros e esquadrias", glz), ("Piso, deck e fundação", flr),
              ("Interiores", interiors), ("Instalações", mep)]
    weights = [(g, sum(x[3] for x in rows)) for g, rows in groups]
    total = sum(w for _, w in weights)
    return dict(steel_rows=steel_rows, steel_kg=steel_kg, alu_rows=alu_rows, alu_kg=alu_kg, groups=groups, weights=weights, total=total,
                memb=memb, glass=glass, floor=floor, deck=deck, arch_lengths=L, front_glass=front_glass, bico=bico, bico_tubes=BT)

def zenith_bom():
    roof_s, roof_p = Z.roof_area()
    floor = Z.floor_area()
    deck = (Z.DECK["x2"] - Z.DECK["x1"]) * (Z.DECK["y2"] - Z.DECK["y1"]) + (Z.WALK["x2"] - Z.WALK["x1"]) * (Z.WALK["y2"] - Z.WALK["y1"])
    steel = [
        ("M1", "Mastro principal com base articulada", "Ø139,7 x 4,5", 1, 5.05, KG["Ø139,7 x 4,5"]),
        ("M2", "Mastro secundário", "Ø114,3 x 4,0", 1, 4.0, KG["Ø114,3 x 4,0"]),
        ("CR", "Coroas: 3 braços por mastro + capitéis usinados", "Ø48,3 x 3,0", 2, 3 * 0.95 + 3 * 0.7, KG["Ø48,3 x 3,0"] + 3.0),
        ("AN", "Anéis de cume Ø1,20 (óculo) e Ø0,70 (chaminé)", "chapa 80 x 10", 2, math.pi * 1.2 + math.pi * 0.7, KG["chapa 80 x 10"]),
        ("P1-P10", "Pilares do corpo embutidos nos painéis", "Ø101,6 x 4,0", 10, 10 * 2.9, KG["Ø101,6 x 4,0"]),
        ("VB", "Anel de beiral em 6 segmentos com chapas de topo", "150 x 100 x 4,0", 6, 29.8, KG["150 x 100 x 4,0"]),
        ("PE1-PE7", "Postes externos inclinados 8° com olhal", "Ø76,1 x 3,6", 7, 7 * 2.8, KG["Ø76,1 x 3,6"]),
        ("CB", "Cabo de borda Ø12 inox + esticadores + chapas de canto", "cabo", 1, 42, 0.62),
        ("ES", "Estais Ø10 inox dos postes + esticadores", "cabo", 7, 7 * 4.2, 0.42),
        ("CH", "Chapas de base, capitéis, ligações parafusadas", "chapa", 1, 1, 95.0),
        ("PF", "Parafusos, chumbadores, perfis de clamp da membrana", "ferragens", 1, 1, 60.0),
    ]
    steel_rows = [(c, d, s, q, r(l, 1), r(l * k)) for (c, d, s, q, l, k) in steel]
    steel_kg = sum(x[5] for x in steel_rows)
    alu = [("PB", "Perfil de borda arredondado do beiral + calha oculta", 1, 30.0, 1.6), ("CL", "Perfil de clamp dos anéis de cume", 2, 6.0, 1.2),
           ("TF", "Trilho do forro tensionado + cabos de suspensão", 1, 70.0, 0.4), ("EO", "Esquadria do óculo (ruptura térmica)", 1, 4.0, 3.0)]
    alu_rows = [(c, d, q, l, r(l * k)) for (c, d, q, l, k) in alu]
    alu_kg = sum(x[4] for x in alu_rows)
    env = [("Membrana PVDF 1050 g/m² (+15% emendas/bolsas)", "m²", r(roof_s * 1.15), r(roof_s * 1.15 * 1.05)),
           ("Lã de PET 50 mm + manta refletiva (forro sobre o corpo)", "m²", 54, r(54 * 1.5)),
           ("Forro tensionado Trevira CS (segue os cumes)", "m²", 58, r(58 * 0.3)),
           ("Painéis SIP 100 mm (OSB/PIR/OSB) estruturais", "m²", 36, 36 * 22),
           ("Placa cimentícia externa 10 mm + membrana hidrófuga", "m²", 36, 36 * 14),
           ("Ripado de madeira termotratada 40 x 40 mm", "m²", 36, 36 * 8),
           ("Acabamento interno das paredes (painel de madeira / tecido)", "m²", 30, 30 * 7)]
    glz = [("Fachada 5,40 x 2,75: 2 fixas + 2 de correr, vidro duplo low-e", "m²", 14.9, r(14.9 * 30)),
           ("Vidro lateral da suíte 6,40 x 2,75 (4 painéis)", "m²", 17.6, r(17.6 * 30)),
           ("Janelas: café 2,20 x 1,10, closet 2,00 x 0,50, banheira 2,40 x 0,65, chuveiro 1,00 x 0,50", "m²", 6.1, r(6.1 * 30)),
           ("Óculo do Zênite: cúpula laminada Ø1,20 + vidro interno", "m²", 1.5, 60),
           ("Esquadrias de alumínio bronze com ruptura térmica + trilhos embutidos", "kg", 165, 165)]
    flr = [("Vigas U 150 x 60 x 3,0 galvanizadas (malha 2,4 m, piso + deck)", "m", 110, r(110 * 6.5)),
           ("Vigotas 50 x 150 tratadas a cada 400 mm", "m", r((floor + deck) * 2.5), r((floor + deck) * 9.4)),
           ("PIR 50 mm entre vigotas + manta inferior", "m²", r(floor), r(floor * 2.1)),
           ("Compensado naval 18 mm", "m²", r(floor), r(floor * 12)),
           ("Piso de engenharia carvalho 14 mm", "m²", r(floor - 15.3), r((floor - 15.3) * 9)),
           ("Zona molhada: placa cimentícia + impermeabilização + porcelanato", "m²", 15, 15 * 30),
           ("Deck cumaru 20 x 140 (terraço + passarela)", "m²", r(deck), r(deck * 20)),
           ("Estacas helicoidais Ø76, hélice Ø300, L 2,0 m + cabeçotes (30 + 7 de tração)", "un", 37, r(37 * 18.8))]
    interiors = [("Parede da cabeceira com o mastro (LSF + painel + madeira)", "m²", 12, 12 * 24),
                 ("Divisória do WC + forro do banho", "m²", 18, 18 * 12),
                 ("Marcenaria: Ilha do Café, closet, criados, bancada dupla, banco", "cj", 1, 340),
                 ("Cama king, sofá 2,20, chaise, mesa de centro", "cj", 1, 230),
                 ("Louças e metais: bacia, bancada, chuveiro, banheira 1,70", "cj", 1, 180),
                 ("Box de vidro do chuveiro + porta de correr", "cj", 1, 60),
                 ("Hidromassagem Ø1,90 (vazia) com filtragem e aquecimento 3 kW", "un", 1, 350)]
    mep = [("Evaporadora dutada 18k BTU inverter + condensadora + dutos + difusores", "cj", 1, 115),
           ("Aquecedor a gás 30 L/min (ou bomba de calor 300 L)", "un", 1, 30),
           ("Quadro elétrico 16 módulos, cabos, fitas LED, luminárias, DR", "cj", 1, 85),
           ("Tubulações PEX / esgoto / ventilação", "cj", 1, 55),
           ("Chaminé do Respiro com veneziana motorizada + exaustor com recuperador", "cj", 1, 25)]
    groups = [("Estrutura metálica (aço galvanizado)", [(d, "kg", q, k) for (_, d, _, q, l, k) in steel_rows]),
              ("Alumínio e perfis", [(d, "un", q, k) for (_, d, q, l, k) in alu_rows]),
              ("Envelope: membrana, forro, painéis", env), ("Vidros e esquadrias", glz), ("Piso, deck e fundação", flr),
              ("Interiores e hidromassagem", interiors), ("Instalações", mep)]
    weights = [(g, sum(x[3] for x in rows)) for g, rows in groups]
    total = sum(w for _, w in weights)
    return dict(steel_rows=steel_rows, steel_kg=steel_kg, alu_rows=alu_rows, alu_kg=alu_kg, groups=groups, weights=weights, total=total,
                roof_s=roof_s, roof_p=roof_p, floor=floor, deck=deck)

def lodge_membrane_area():
    """área desenvolvida da membrana cônica (8 gomos, do anel da lanterna ao beiral com balanço), a partir da malha da geometria."""
    m = LD.roof_mesh(); V = m["vertices"]; A = 0.0
    for a, b, c in m["faces"]:
        ax, ay, az = V[a]; bx, by, bz = V[b]; cx, cy, cz = V[c]
        ux, uy, uz = bx - ax, by - ay, bz - az; vx, vy, vz = cx - ax, cy - ay, cz - az
        A += 0.5 * math.sqrt((uy * vz - uz * vy) ** 2 + (uz * vx - ux * vz) ** 2 + (ux * vy - uy * vx) ** 2)
    return A

def lodge_bom():
    side = LD.side(); floor = LD.floor_area(); deck = LD.deck_area()
    memb = lodge_membrane_area()                       # ≈ 73 m² desenvolvidos (≈ 60 m² em projeção)
    (x1, y1, z1), (x2, y2, z2) = LD.rafters()[0]
    rafter = math.dist((x1, y1, z1), (x2, y2, z2))     # ≈ 3,49 m
    ring = LD.N * side                                 # anel de beiral ≈ 22,5 m
    lantern = math.pi * 2 * LD.R_LANTERN               # anel da lanterna Ø1,50 ≈ 4,7 m
    wall_h = LD.Z_EAVE - 0.15                          # 2,55 m livres entre piso e anel
    clear = side - 0.14                                # vão livre entre pilares revestidos (140 mm) ≈ 2,68 m
    glass = 5 * clear * (wall_h - 0.10)                # cinco faces de vidro (vão líquido, soleira 100 mm) ≈ 33 m²
    wall_op = 3 * clear * wall_h                       # três faces opacas ≈ 20,5 m²
    forro = 44.0; ins = 46.0; sail = 14.0; bath = 6.9
    n_piles = len(LD.piles())
    steel = [
        ("P1-P8", "Pilares nos vértices, revestidos em madeira até 2,70 m", "Ø101,6 x 4,0", 8, 8 * LD.Z_EAVE, KG["Ø101,6 x 4,0"]),
        ("VB", "Anel de beiral em 8 segmentos de 2,82 m com chapas de topo a 135°", "150 x 100 x 4,0", 8, ring, KG["150 x 100 x 4,0"]),
        ("R1-R8", "Caibros radiais do vértice (z 2,70) ao anel da lanterna (r 0,75, z 4,60)", "Ø76,1 x 3,6", 8, 8 * rafter, KG["Ø76,1 x 3,6"]),
        ("AC", "Anel de compressão da lanterna Ø1,50 calandrado + 8 orelhas", "Ø60,3 x 3,0", 1, lantern, KG["Ø60,3 x 3,0"] + 1.0),
        ("LT", "Lanterna: 8 montantes de 0,60 m + anel superior Ø1,50", "Ø42,4 x 3,0", 1, 8 * 0.6 + lantern, KG["Ø42,4 x 3,0"]),
        ("PV", "Postes da vela de sombra com base articulada e olhal", "Ø76,1 x 3,6", 2, 2 * LD.SAIL["z_post"], KG["Ø76,1 x 3,6"]),
        ("CB", "Cabos inox Ø8 em X nas 3 faces opacas + esticadores + olhais", "cabo", 6, 6 * 3.8, 0.35),
        ("CV", "Cabos inox Ø8 da vela (4 vértices) + esticadores", "cabo", 4, 4 * 4.0, 0.35),
        ("CH", "Chapas de base e topo dos pilares, chapas de topo do anel, talões dos caibros, nós da lanterna, chapas de canto", "chapa", 1, 1, 78.0),
        ("PF", "Parafusos, chumbadores, perfis de clamp da membrana", "ferragens", 1, 1, 40.0),
    ]
    steel_rows = [(c, d, s, q, r(l, 1), r(l * k)) for (c, d, s, q, l, k) in steel]
    steel_kg = sum(x[5] for x in steel_rows)
    alu = [("PB", "Perfil de borda arredondado do beiral + calha oculta (8 lados)", 8, 8 * 3.0, 1.6), ("CL", "Perfil de clamp do anel da lanterna (2 metades)", 1, lantern, 1.2),
           ("EL", "Esquadria da lanterna com ruptura térmica (vidro curvo 0,45 m)", 1, lantern, 3.0), ("TL", "Tampa da lanterna Ø1,60 em chapa de alumínio 2 mm sobre quadro, com pingadeira", 1, 1, 14.0),
           ("TF", "Trilho do forro tensionado", 1, 46.0, 0.35)]
    alu_rows = [(c, d, q, l, r(l * k)) for (c, d, q, l, k) in alu]
    alu_kg = sum(x[4] for x in alu_rows)
    env = [("Membrana PVDF 1050 g/m² em 8 gomos (+15% emendas/bolsas)", "m²", r(memb * 1.15), r(memb * 1.15 * 1.05)),
           ("Vela de sombra: membrana PVDF 14 m² (+15%) com bolsas de cabo", "m²", r(sail * 1.15), r(sail * 1.15 * 1.05)),
           ("Lã de PET 50 mm, 25 kg/m³ (sobre o forro, câmara ventilada acima)", "m²", r(ins), r(ins * 1.25)),
           ("Manta refletiva de alumínio (bolha)", "m²", r(ins), r(ins * 0.25)),
           ("Forro tensionado Trevira CS (cone interno até o anel da lanterna)", "m²", r(forro), r(forro * 0.3)),
           ("Painéis SIP 100 mm (OSB/PIR/OSB) nas 3 faces opacas", "m²", r(wall_op, 1), r(wall_op * 22)),
           ("Membrana hidrófuga + ripas de ventilação (câmara ventilada da parede)", "m²", r(wall_op, 1), r(wall_op * 2)),
           ("Ripado de madeira termotratada 40 x 40 mm (externo)", "m²", r(wall_op, 1), r(wall_op * 8)),
           ("Revestimento de madeira dos pilares (2 meias-canas 140 mm, h 2,70)", "un", 8, 8 * 10),
           ("Painéis de madeira internos das faces opacas", "m²", 20, 20 * 7)]
    glz = [("Cinco faces de vidro insulado 6 lam + 12 Ar + 6 temp low-e (vão líquido 2,68 x 2,45 por face)", "m²", r(glass, 1), r(glass * 30)),
           ("Porta de correr 2,00 x 2,40 (folha incluída na fachada): trilho embutido + ferragens", "un", 1, 30),
           ("Fresta alta da banheira 1,60 x 0,60, vidro insulado", "m²", 1.0, 30),
           ("Lanterna: vidro laminado curvo 8 + 8 mm, h 0,45 m, Ø1,50", "m²", r(0.45 * lantern, 1), r(0.45 * lantern * 40)),
           ("Esquadrias de alumínio bronze com ruptura térmica (montantes nos pilares, travessas)", "kg", 130, 130)]
    flr = [("Vigas U 150 x 60 x 3,0 galvanizadas (grelha + anel de borda octogonal + deck)", "m", 100, r(100 * KG["U 150 x 60 x 3,0"])),
           ("Vigotas LSF Ue 150 x 40 x 1,25 dos módulos de piso @ 400 mm", "m", r(floor * 3.3), r(floor * 3.3 * KG["Ue 150 x 40 x 1,25"])),
           ("Vigotas LSF Ue 150 x 40 x 1,25 dos módulos de deck @ 400 mm (clipes do cumaru parafusados)", "m", r(deck * 2.5), r(deck * 2.5 * KG["Ue 150 x 40 x 1,25"])),
           ("PIR 50 mm entre vigotas + manta inferior", "m²", r(floor), r(floor * 2.1)),
           ("Compensado naval 18 mm", "m²", r(floor), r(floor * 12)),
           ("Piso de engenharia carvalho 14 mm", "m²", r(floor - bath), r((floor - bath) * 9)),
           ("Zona molhada: placa cimentícia + impermeabilização + porcelanato", "m²", bath, r(bath * 30)),
           ("Deck cumaru 20 x 140 com fixação oculta (3 faces)", "m²", r(deck), r(deck * 20)),
           ("Estacas helicoidais Ø76, hélice Ø300, L 2,0 m + cabeçotes (20 sob piso/deck + 2 sob os postes da vela)", "un", n_piles, r(n_piles * 18.8))]
    interiors = [("Parede-corda do banho (LSF + painel + porta de correr 0,90 x 2,10)", "m²", 12.5, r(12.5 * 22)),
                 ("Marcenaria: closet, café/minibar, criados, bancada 1,40", "cj", 1, 200),
                 ("Cama king, sofá 2,40, poltrona, mesa lateral", "cj", 1, 190),
                 ("Louças e metais: bacia, cuba, chuveiro, banheira de sentar 0,90 x 0,75", "cj", 1, 110),
                 ("Vidro do box do chuveiro", "un", 1, 30)]
    mep = [("Evaporadora dutada 9k BTU inverter + condensadora + dutos + difusores", "cj", 1, 75),
           ("Aquecedor a gás 23 L/min (ou bomba de calor 200 L)", "un", 1, 25),
           ("Quadro elétrico, cabos, fitas LED, luminárias, tomadas", "cj", 1, 60),
           ("Tubulações PEX / esgoto / ventilação", "cj", 1, 40),
           ("Exaustor com recuperador de calor + respiro da lanterna", "cj", 1, 12)]
    groups = [("Estrutura metálica (aço galvanizado)", [(d, "kg", q, k) for (_, d, _, q, l, k) in steel_rows]),
              ("Alumínio e lanterna", [(d, "un", q, k) for (_, d, q, l, k) in alu_rows]),
              ("Envelope: membrana, vela, isolamento, painéis", env), ("Vidros e esquadrias", glz), ("Piso, deck e fundação", flr),
              ("Interiores", interiors), ("Instalações", mep)]
    weights = [(g, sum(x[3] for x in rows)) for g, rows in groups]
    total = sum(w for _, w in weights)
    return dict(steel_rows=steel_rows, steel_kg=steel_kg, alu_rows=alu_rows, alu_kg=alu_kg, groups=groups, weights=weights, total=total,
                memb=memb, sail=sail, glass=glass, wall_op=wall_op, forro=forro, ins=ins, floor=floor, deck=deck, bath=bath, side=side,
                rafter=rafter, ring=ring, lantern=lantern, n_piles=n_piles)

# ---------------- componentes para fabricação (códigos) ----------------
def cocoon_parts():
    L = C.arch_lengths()
    P = [("ZC-A0", "Anel frontal inclinado", "Tubo Ø101,6 x 4,0 calandrado em elipse 4,88 x 4,13 m (acima do piso), 2 segmentos, com perfil de vidro soldado", 1, "Calandra CNC + solda MIG + galvanização")]
    for i, l in enumerate(L[1:], start=1):
        P.append((f"ZC-A{i}", f"Arco elíptico A{i}", f"Tubo Ø88,9 x 3,6, desenvolvido {l:.2f} m, 3 segmentos (2 pernas + coroa), 2 luvas", 1, "Calandra CNC por gabarito, furação M12, galvanização"))
    P += [("ZC-T", "Trecho de terça", "Tubo Ø48,3 x 3,0, 1.200 mm, ponteiras rosqueadas M16 nas duas extremidades", 56, "Corte + usinagem das ponteiras"),
          ("ZC-EL", "Espinha de Luz", "Treliça plana 4.700 x 300 mm, banzos Ø42,4, diagonais Ø26,9, 4 berços para vidro", 1, "Gabarito de solda"),
          ("ZC-TB", "Trilho de base", "Tubo 100 x 50 x 3,0 curvado em planta (raio variável), furos Ø14 a cada 600 mm, 2 peças de 9,0 m em 3 trechos", 2, "Calandra de perfil + furação"),
          ("ZC-QC", "Quadro da cauda", "Anel Ø60,3 + 3 barras, fechamento cônico", 1, "Solda"),
          ("ZC-CB", "Chapa de base", "200 x 150 x 10 mm, 2 enrijecedores, 4 furos Ø18", 16, "Corte plasma + solda"),
          ("ZC-LV", "Luva de emenda", "Tubo Ø76,1 x 3,6 x 200 mm, 4 furos Ø13", 21, "Corte + furação"),
          ("ZC-KD", "Perfil keder", "Alumínio duplo keder 6060-T5, curvado sobre o arco, presilhas a cada 300 mm", 8, "Extrusão + calandra"),
          ("ZC-MB", "Membrana externa", "PVDF 1050 g/m² em 7 painéis entre arcos + 2 tampas (frente/cauda), keder soldado por RF, bolsas nas bases", 1, "Corte CNC + solda RF (form-finding)"),
          ("ZC-IS", "Kit de isolamento", "Lã PET 50 mm em mantas pré-cortadas por vão + refletiva", 7, "Corte por gabarito"),
          ("ZC-FR", "Forro tensionado", "Trevira CS em 7 painéis com harpão perimetral", 7, "Costura + harpão"),
          ("ZC-FV", "Fachada de vidro", "Anel de alumínio 120 x 60 curvo + 4 montantes + travessa + 8 vidros duplos + porta pivotante 1,00 x 2,40", 1, "Esquadria sob medida"),
          ("ZC-JO", "Janela Olho", "Requadro de madeira laminada 220 mm em lente 0,95 x 0,80 (ou 0,80 x 0,55), vidro duplo, 2 basculantes", 6, "Marcenaria CNC + esquadria"),
          ("ZC-VE", "Vidro da espinha", "Laminado 8 + 8 mm, 1.175 x 700 mm, bordas polidas", 4, "Vidraçaria"),
          ("ZC-PW", "Parede do banho", "Quadro LSF 90 mm + painel + porta de correr 0,85 x 2,10, pré-montada em 2 módulos", 1, "Pré-fabricação"),
          ("ZC-PL", "Módulo de piso", "Quadros de vigotas 2,4 x 1,2 m com PIR e compensado, 18 módulos", 18, "Pré-fabricação"),
          ("ZC-DK", "Módulo de deck", "Painéis cumaru 2,0 x 1,0 m sobre vigotas", 15, "Pré-fabricação"),
          ("ZC-EH", "Estaca helicoidal", "Ø76 x 3,6, hélice Ø300, L 2,0 m, cabeçote ajustável", 44, "Compra"),
          ("ZC-MQ", "Kit de instalações", "Quadro elétrico pré-montado, chicote LED, kit PEX, evaporadora dutada", 1, "Pré-montagem em bancada")]
    return P

def zenith_parts():
    P = [("ZZ-M1", "Mastro principal", "Tubo Ø139,7 x 4,5 x 5.050 mm, base articulada com pino Ø30, capitel usinado no topo", 1, "Corte + usinagem + solda + galvanização"),
         ("ZZ-M2", "Mastro secundário", "Tubo Ø114,3 x 4,0 x 4.000 mm, idem", 1, "Idem"),
         ("ZZ-CR1", "Coroa do Zênite", "3 braços Ø48,3 x 950 mm + capitel + anel Ø1.200 em chapa 80 x 10, perfil de clamp, berço do óculo", 1, "Gabarito de solda + usinagem"),
         ("ZZ-CR2", "Coroa do Respiro", "3 braços Ø48,3 x 700 mm + anel Ø700 + chaminé com veneziana", 1, "Idem"),
         ("ZZ-P", "Pilar do corpo", "Tubo Ø101,6 x 4,0 x 2.900 mm, chapas de topo e base", 10, "Corte + solda"),
         ("ZZ-VB", "Segmento do anel de beiral", "Tubo 150 x 100 x 4,0, comprimentos 4,75 / 2,70 m, chapas de topo com 4 M16, perfil de borda", 6, "Corte + solda + furação"),
         ("ZZ-PE", "Poste externo", "Tubo Ø76,1 x 3,6 x 2.800 mm, base articulada, olhal no topo", 7, "Corte + solda"),
         ("ZZ-MB", "Membrana externa", "PVDF 1050 g/m² em 8 painéis radiais por cume + faixas de beiral, bolsas de cabo de borda, clamps nos anéis", 1, "Corte CNC + solda RF (form-finding)"),
         ("ZZ-CB", "Cabo de borda", "Inox Ø12 x 42 m em 4 trechos, terminais prensados, esticadores M20", 1, "Cabos prensados"),
         ("ZZ-ES", "Estai", "Inox Ø10 x 4,2 m com esticador M16 e olhal", 7, "Cabos prensados"),
         ("ZZ-SIP", "Painel de parede", "SIP 100 mm, alturas 2.750 mm, larguras 1.200 / 600 mm, rebaixos para pilares, revestido", 22, "Pré-fabricação"),
         ("ZZ-FV", "Fachada", "4 folhas 1.350 x 2.750 (2 fixas + 2 de correr), trilho embutido, soleira com dreno", 1, "Esquadria sob medida"),
         ("ZZ-VL", "Vidro lateral", "4 painéis fixos 1.600 x 2.750, vidro duplo low-e", 4, "Esquadria"),
         ("ZZ-OC", "Óculo do Zênite", "Cúpula laminada Ø1.200 + esquadria com ruptura térmica + vidro interno", 1, "Vidraçaria especial"),
         ("ZZ-FR", "Forro tensionado", "Trevira CS em 6 painéis seguindo os cumes, anéis internos, mantas PET", 1, "Costura + harpão"),
         ("ZZ-PW", "Parede da cabeceira", "Quadro LSF com nicho do mastro M1, painel de madeira, porta de correr 1,10 x 2,20", 1, "Pré-fabricação"),
         ("ZZ-IC", "Ilha do Café", "Totem de madeira 0,56 x 0,56 x 2,75 envolvendo M2 + bancada 2,00 x 0,72 com minibar", 1, "Marcenaria"),
         ("ZZ-PL", "Módulo de piso", "Quadros de vigotas 2,4 x 1,35 m com PIR e compensado", 16, "Pré-fabricação"),
         ("ZZ-DK", "Módulo de deck", "Painéis cumaru 2,0 x 1,0 m + recorte da hidromassagem", 15, "Pré-fabricação"),
         ("ZZ-EH", "Estaca helicoidal", "Ø76 x 3,6, hélice Ø300, L 2,0 m (30 compressão + 7 tração)", 37, "Compra"),
         ("ZZ-MQ", "Kit de instalações", "Quadro elétrico, chicote LED, kit PEX, evaporadora dutada 18k, kit da hidromassagem", 1, "Pré-montagem")]
    return P

def lodge_parts():
    b = lodge_bom()
    P = [("ZL-P", "Pilar de vértice", "Tubo Ø101,6 x 4,0 x 2.700 mm, chapa de base 200 x 200 x 10 e chapa de topo 150 x 150 x 8 soldadas, 2 talões para os montantes de vidro", 8, "Corte + solda + galvanização"),
         ("ZL-PR", "Revestimento do pilar", "2 meias-canas de madeira laminada 140 mm, h 2.700, usinadas, encaixe com clipes", 8, "Marcenaria CNC + verniz"),
         ("ZL-VB", "Segmento do anel de beiral", "Tubo 150 x 100 x 4,0 x 2.820 mm, chapas de topo dobradas a 135° com 4 M16, talão do caibro, furos do perfil de borda", 8, "Corte + solda + furação + galvanização"),
         ("ZL-R", "Caibro radial", f"Tubo Ø76,1 x 3,6 x {b['rafter'] * 1000:.0f} mm, chapa-orelha no pé (pino Ø16) e no topo (2 M16), talões do trilho do forro", 8, "Corte + solda + galvanização"),
         ("ZL-AC", "Anel de compressão da lanterna", "Tubo Ø60,3 x 3,0 calandrado Ø1.500, 8 orelhas para os caibros, perfil de clamp da membrana", 1, "Calandra + solda em gabarito"),
         ("ZL-LT", "Lanterna", "Quadro de 8 montantes Ø42,4 x 600 + anel superior Ø1.500; esquadria de alumínio RPT; vidro laminado curvo 8 + 8 h 450; tampa de alumínio Ø1.600", 1, "Solda + esquadria + vidraçaria especial"),
         ("ZL-PV", "Poste da vela", "Tubo Ø76,1 x 3,6 x 2.400 mm, base articulada com pino Ø20, olhal no topo", 2, "Corte + solda"),
         ("ZL-VS", "Vela de sombra", "PVDF 1050 g/m² ~14 m² (hipar), bolsas de cabo Ø8 nas 4 bordas, chapas de canto inox", 1, "Corte CNC + solda RF"),
         ("ZL-MB", "Membrana externa", f"PVDF 1050 g/m² em 8 gomos ({b['memb']:.0f} m² desenvolvidos), bolsa de borda com tubo Ø20, clamp no anel da lanterna", 1, "Corte CNC + solda RF (form-finding)"),
         ("ZL-CB", "Cabo de contraventamento", "Inox Ø8 x 3,8 m, terminais prensados, esticador M12 (6 nas faces opacas + 4 da vela)", 10, "Cabos prensados"),
         ("ZL-SIP", "Painel de parede", "SIP 100 mm, h 2.550, larguras 1.340 / 670 mm, rebaixo para os pilares, hidrófuga + ripas + ripado externo", 12, "Pré-fabricação"),
         ("ZL-FV", "Face de vidro", "Vidro insulado 6 lam + 12 Ar + 6 temp low-e, 2 painéis 1.320 x 2.450 por face, montantes fixados nos pilares; a face frontal com porta de correr 2,00 x 2,40", 5, "Esquadria sob medida"),
         ("ZL-FR", "Forro tensionado", "Trevira CS em 8 gomos do anel de beiral ao anel da lanterna, harpão perimetral, mantas PET 50 mm", 1, "Costura + harpão"),
         ("ZL-PW", "Parede-corda do banho", "Quadro LSF 90 mm x 5,20 x 2,40 + painel + porta de correr 0,90 x 2,10, pré-montada em 2 módulos", 1, "Pré-fabricação"),
         ("ZL-PL", "Módulo de piso", "Quadros de vigotas LSF Ue 150 x 40 x 1,25 (2,4 x 1,2 m e recortes do octógono) com PIR e compensado", 14, "Pré-fabricação"),
         ("ZL-DK", "Módulo de deck", "Painéis cumaru 2,0 x 1,0 m com fixação oculta sobre vigotas LSF Ue 150 x 40 x 1,25", 15, "Pré-fabricação"),
         ("ZL-EH", "Estaca helicoidal", "Ø76 x 3,6, hélice Ø300, L 2,0 m, cabeçote ajustável (20 sob piso/deck + 2 sob os postes da vela)", b["n_piles"], "Compra"),
         ("ZL-MQ", "Kit de instalações", "Quadro elétrico pré-montado, chicote LED, kit PEX, evaporadora dutada 9k", 1, "Pré-montagem em bancada")]
    return P

# ---------------- transporte ----------------
def transport(b, name):
    if name == "cocoon":
        items = [("Estrado de estrutura 1: arcos A0 a A3 em segmentos", "2,4 x 1,2 x 0,9 m", 5.2, 780),
                 ("Estrado de estrutura 2: arcos A4 a A7, quadro da cauda, espinha", "2,4 x 1,2 x 0,9 m", 5.2, 620),
                 ("Estrado 3: terças, trilhos de base, chapas, keder, cabos", "2,4 x 1,2 x 0,6 m", 3.5, 520),
                 ("Caixa da membrana + isolamento + forro (rolos)", "2,4 x 1,2 x 1,2 m", 6.9, 420),
                 ("Cavaletes de vidro (fachada, Olhos, espinha) x 4", "2,2 x 0,6 x 2,4 m", 12.7, 1050),
                 ("Paletes de piso (módulos) x 2", "2,4 x 1,2 x 1,0 m", 5.8, 1650),
                 ("Palete de deck", "2,0 x 1,0 x 1,2 m", 2.4, 800),
                 ("Palete de instalações + louças + marcenaria", "2,4 x 1,2 x 1,4 m", 8.1, 900),
                 ("Estacas helicoidais em feixes", "2,1 x 0,6 x 0,6 m", 0.8, 730)]
    elif name == "lodge":
        items = [("Estrado de estrutura 1: pilares, anel de beiral, caibros, anéis da lanterna, postes da vela", "3,0 x 1,2 x 0,8 m", 2.9, 900),
                 ("Estrado 2: vigas U, chapas, cabos, perfis de alumínio, tampa da lanterna", "4,8 x 1,2 x 0,6 m", 3.5, 800),
                 ("Painéis SIP + parede-corda do banho", "2,8 x 1,25 x 0,9 m", 3.2, 700),
                 ("Caixa da membrana + vela + isolamento + forro (rolos)", "2,4 x 1,2 x 1,0 m", 2.9, 300),
                 ("Cavaletes de vidro x 3 (5 faces, porta de correr, lanterna)", "2,9 x 0,6 x 2,7 m", 14.1, 1300),
                 ("Paletes de piso (módulos) x 2", "2,4 x 1,2 x 0,9 m", 5.2, 1300),
                 ("Palete de deck", "2,0 x 1,0 x 1,3 m", 2.6, 800),
                 ("Palete de instalações + louças + marcenaria + mobiliário", "2,4 x 1,2 x 1,4 m", 4.0, 800),
                 ("Estacas helicoidais em feixes", "2,1 x 0,6 x 0,5 m", 0.6, 420)]
    else:
        items = [("Estrado de estrutura 1: mastros, coroas, anéis, pilares", "5,2 x 1,2 x 0,8 m", 5.0, 760),
                 ("Estrado de estrutura 2: anel de beiral, postes, cabos, chapas", "4,8 x 1,2 x 0,8 m", 4.6, 720),
                 ("Painéis SIP em 2 pacotes", "2,8 x 1,25 x 1,3 m", 9.1, 1680),
                 ("Caixa da membrana + forro (rolos)", "2,4 x 1,2 x 1,2 m", 6.9, 460),
                 ("Cavaletes de vidro x 4 (fachada, lateral, janelas, óculo)", "2,9 x 0,6 x 2,9 m", 20.2, 1340),
                 ("Paletes de piso x 2", "2,4 x 1,35 x 1,0 m", 6.5, 1750),
                 ("Palete de deck", "2,0 x 1,0 x 1,4 m", 2.8, 900),
                 ("Palete de instalações + louças + marcenaria + hidromassagem", "2,4 x 2,0 x 1,4 m", 6.7, 1650),
                 ("Estacas helicoidais em feixes", "2,1 x 0,6 x 0,6 m", 0.8, 700)]
    raw = sum(i[3] for i in items)
    items = [(d, dim, v, int(round(k * b["total"] / raw))) for (d, dim, v, k) in items]   # pesos ajustados ao total da lista de materiais
    vol = sum(i[2] for i in items); kg = sum(i[3] for i in items)
    return dict(items=items, vol=round(vol, 1), kg=kg)

ASSEMBLY = {
    "cocoon": [
        ("Locação e fundação", "Topografia com estação total; cravação de 44 estacas helicoidais com motor hidráulico; nivelamento dos cabeçotes ajustáveis (tolerância ± 5 mm)", 1.0, "4 + operador"),
        ("Grelha de vigas e módulos de piso", "Vigas U 150 parafusadas aos cabeçotes; 18 módulos de piso e 15 módulos de deck; fechamento inferior; passagem de esgoto e PEX", 2.0, "4"),
        ("Trilhos de base e arcos", "Fixação dos trilhos curvados; montagem dos arcos A7 a A1 no chão (pernas + coroa com luvas), içamento com guincho manual e travamento provisório; anel A0 inclinado por último", 1.5, "4"),
        ("Terças, espinha e contraventamento", "Terças rosqueadas entre arcos; treliça da espinha; cabos em X tensionados a 2 kN; conferência de geometria", 0.5, "4"),
        ("Membrana externa", "Deslizamento dos painéis nos perfis keder (cauda para a frente); tensionamento das bolsas de base com esticadores; tampas de frente e cauda", 1.0, "4"),
        ("Isolamento e forro", "Mantas de PET e refletiva presas às terças; trilhos do forro; tensionamento dos 7 painéis de forro; painéis ripados", 1.0, "4"),
        ("Vidros", "Anel de alumínio da fachada no A0; vidros duplos e porta pivotante; 6 Janelas Olho; 4 vidros da espinha com selagem", 1.5, "3 + vidraceiro"),
        ("Interiores", "Parede do banho, forro e ático; louças, metais, banheira; piso de engenharia; marcenaria", 2.0, "4"),
        ("Instalações e comissionamento", "Quadro, circuitos, fitas LED; evaporadora e condensadora; aquecedor; testes de estanqueidade e climatização; limpeza", 1.5, "2 + eletricista"),
    ],
    "zenith": [
        ("Locação e fundação", "37 estacas (30 sob o piso, 7 de tração para os postes); nivelamento dos cabeçotes", 1.5, "4 + operador"),
        ("Grelha e módulos de piso e deck", "Vigas U 150; 16 módulos de piso; deck do terraço e passarela; base da hidromassagem", 2.0, "4"),
        ("Pilares, anel de beiral e mastros", "10 pilares nas chapas de base; 6 segmentos do anel parafusados; mastros M1 e M2 içados com talha e travados nas bases articuladas; coroas e anéis de cume", 2.0, "4"),
        ("Painéis SIP e parede da cabeceira", "22 painéis encaixados entre pilares, selados; parede da cabeceira envolvendo M1; Ilha do Café envolvendo M2", 1.0, "4"),
        ("Postes externos e cabos", "7 postes nas bases articuladas; cabo de borda passado nas bolsas; estais até as estacas de tração (sem tensão final)", 0.5, "4"),
        ("Membrana externa", "Içamento pelos anéis de cume; clamps nos anéis; passagem sobre o anel de beiral; tensionamento progressivo dos cantos e estais; verificação da flecha das bordas", 1.5, "4 + supervisor de membrana"),
        ("Forro isolado", "Mantas PET e refletiva; forro tensionado seguindo os cumes; anéis internos e vidro interno do óculo", 1.0, "4"),
        ("Vidros e esquadrias", "Fachada com trilho embutido; 4 painéis laterais; janelas; óculo com selagem", 2.0, "3 + vidraceiro"),
        ("Interiores", "Divisórias e forro do banho; louças, metais, banheira; piso; marcenaria; hidromassagem", 2.0, "4"),
        ("Instalações e comissionamento", "Quadro, circuitos, LED; evaporadora dutada e condensadora; aquecedor; chaminé do Respiro; testes", 1.5, "2 + eletricista"),
    ],
    "lodge": [
        ("Locação e fundação", "Locação do octógono por raios a partir do centro; cravação de 22 estacas helicoidais (20 sob piso/deck + 2 sob os postes da vela); nivelamento dos cabeçotes (± 5 mm)", 0.5, "3 + operador"),
        ("Grelha e módulos de piso e deck", "Vigas U 150 na grelha e no anel de borda octogonal; 14 módulos de piso LSF e 15 módulos de deck; passagens de esgoto e PEX", 1.5, "4"),
        ("Pilares, anel de beiral, caibros e lanterna", "8 pilares chumbados nas chapas de base; 8 segmentos do anel parafusados; anel de compressão içado com tripé e os 8 caibros pinados nos vértices; lanterna sobre o anel", 1.0, "4"),
        ("Painéis SIP, parede-corda e cabos", "12 painéis SIP encaixados entre os pilares das 3 faces opacas; parede-corda do banho; cabos em X tensionados a 2 kN", 0.5, "4"),
        ("Membrana externa", "Membrana içada pelo anel da lanterna; clamp no anel; gomos passados sobre o anel de beiral; bolsa de borda tensionada em cruz; vidro curvo e tampa da lanterna", 1.0, "3 + supervisor de membrana"),
        ("Isolamento e forro", "Mantas de PET e refletiva; trilhos do forro nos caibros; forro tensionado em 8 gomos até o anel da lanterna; revestimento de madeira dos pilares", 1.0, "4"),
        ("Vidros e esquadrias", "Montantes fixados nos pilares; 10 vidros insulados das 5 faces; porta de correr 2,00 x 2,40; fresta da banheira; selagem", 1.5, "3 + vidraceiro"),
        ("Interiores", "Banho: louças, metais, banheira de sentar, box; piso de engenharia; marcenaria (closet, café, criados, bancada); painéis internos", 1.0, "4"),
        ("Instalações, vela e comissionamento", "Quadro, circuitos, LED; evaporadora 9k e condensadora; aquecedor; postes e vela de sombra tensionada; testes de estanqueidade e climatização; limpeza", 1.0, "2 + eletricista"),
    ],
}

if __name__ == "__main__":
    for name, fn in (("cocoon", cocoon_bom), ("zenith", zenith_bom), ("lodge", lodge_bom)):
        b = fn()
        print(name.upper(), "aço:", b["steel_kg"], "kg · alumínio:", b["alu_kg"], "kg · total:", b["total"], "kg")
        for g, w in b["weights"]:
            print("   ", g, w)
        t = transport(b, name); print("    transporte:", t["vol"], "m³", t["kg"], "kg", "· montagem dias:", sum(s[2] for s in ASSEMBLY[name]))

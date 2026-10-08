# -*- coding: utf-8 -*-
"""<TAG>-CAM-001 · PROJETO POR CAMADAS de cada cabana: um só arquivo por modelo, do ferro à lona.
Camadas: C0 visão geral · C1 fundação e deck · C2 estrutura de ferro (ferro a ferro, medidas, encaixes, montagem) · C3 fixação da lona nos
ferros · C4 isolamento e câmara · C5 revestimento interno · C6 lona externa · C7 vidros e esquadrias · C8 sequência completa de montagem.
Reusa os dados de build_lotes (peças, geometria, padrões, manual). Sem preços. Saída: 06_LOTES/<TAG>-CAM-001_Projeto_por_Camadas.html"""
import os, sys
from build_lotes import *          # MODELS, LOTS, Doc, helpers, arch_table, arch_coords, parts_rows, manual_rows, bom_groups, bom_table, CSS
import build_lotes as BL
import lona

LAYER_CSS = """
.cam{display:grid;grid-template-columns:repeat(9,1fr);gap:6px;margin:6px 0 10px} .cam>div{border-top:2px solid var(--ink);padding-top:4px;font-size:7.4px;line-height:1.4} .cam b{display:block;font-size:8px;letter-spacing:.16em}
.cam i{display:block;font-style:normal;color:var(--earth);font-size:6.8px;letter-spacing:.1em;margin-bottom:2px}
.nodes td:first-child{white-space:nowrap} .lede b{font-weight:600}
"""
NODES = {
 "cocoon": [("N1 · Pé do arco", "D01 chapa 200 x 150 x 10 soldada no pé do arco (B0n-E/D) com 2 enrijecedores", "Viga de borda A05/A06 (U 150 x 60)", "4 chumbadores M16 8.8 galv. · torque 120 N·m", "Engaste: o arco não pode girar na base. Furos oblongos 18 x 25 na chapa para ajuste de ± 5 mm."),
            ("N2 · Emenda perna / coroa", "D02 luva interna Ø76,1 x 200 soldada dentro da perna (macho)", "Coroa B0n-C (fêmea, Ø88,9)", "4 M12 8.8 passantes + pino de segurança Ø6 · 45 N·m", "Encaixe de 200 mm; marcação A3-E / A3-C para não trocar; a luva fica sempre na perna."),
            ("N3 · Terça no arco", "D03 talão de chapa 8 mm com furo Ø17 soldado no arco", "Terça C01/C02 Ø48,3 com ponteira M16 soldada", "Porca + contraporca M16 · 60 N·m", "7 linhas de terças; a ponteira rosqueada compensa ± 10 mm de comprimento."),
            ("N4 · Espinha de Luz", "D06 berço de chapa 5 mm na coroa de A1 a A5", "Treliça C03 (banzos Ø42,4)", "2 M12 por berço", "A Espinha trava a cumeeira e apoia os 4 vidros da claraboia sobre EPDM (D08)."),
            ("N5 · Cabo em X", "D05 olhal de chapa 10 mm (furo Ø14) soldado no arco", "Cabo inox Ø8 C04 com terminal prensado", "Manilha + esticador M12 inox · pré-tensão 2 kN", "Nos vãos A0-A1 e A5-A6; tensionar depois do esquadro, antes da lona."),
            ("N6 · Bico na estrutura", "Chapas de engaste 10 mm soldadas na cumeeira B09", "Anéis A0 e A1 (coroa)", "4 M16 em cada anel · 120 N·m", "Nó de momento: sustenta 2,40 m de balanço. ⚠️ VALIDAÇÃO OBRIGATÓRIA. Tirantes B12 do 60 % do balanço ao anel A0."),
            ("N7 · Bordas do Bico", "Tubos B10-E/D curvados em 3D", "Ponta de B09 (nó soldado em fábrica) e anel A0 (chapa D01-B)", "2 M12 no anel A0", "Costela B11 travada por talões D03 na cumeeira e nas bordas."),
            ("N8 · Quadro da cauda", "B08 anel Ø60,3 + 3 barras radiais", "Arco A7 (luva D02) e vigas (2 chapas D01)", "4 M12 + 8 M16", "Fecha a ponta e ancora a tampa de membrana P8."),
            ("N9 · Keder no arco", "E01 perfil duplo keder de alumínio calandrado", "Dorso de cada arco", "Presilha inox E03 + M8 em inserto a cada 300 mm", "Camada 3: o perfil recebe o cordão keder da lona externa (um painel de cada lado)."),
            ("N10 · Base da lona", "A07/A08 trilho 100 x 50 calandrado + E02 perfil de arremate com calha", "Viga de borda A05/A06", "M10 @600 (trilho) · M8 inox @400 (perfil)", "O keder Ø13 da base entra no perfil de arremate; a calha oculta leva a água aos tubos de queda."),
            ("N11 · Fachada de vidro", "E07 anel de alumínio 120 x 60 (2 metades) sobre fita EPDM", "Anel frontal A0 (Ø101,6, lábio 8°)", "M8 @400", "Base da esquadria inclinada; contramarcos com ruptura térmica; vidros calçados sobre EPDM.")],
 "zenith": [("N1 · Base do mastro", "Base articulada (D09) com pino", "Chapa da grelha", "4 M16 · 120 N·m", "Içar com a base travada e 3 cordas guia."), ("N2 · Coroa do cume", "Capitel usinado (D10) + anel de cume", "Topo do mastro", "4 M16", "Clamp da membrana no anel."), ("N3 · Anel de beiral", "Chapas de topo 150 x 180 x 10", "Segmentos 150 x 100 x 4,0", "4 M16 por emenda", "6 segmentos; perímetro 29,8 m; calha oculta."), ("N4 · Pilar no anel", "Talão soldado", "Pilar Ø101,6", "4 M12", "Prumo 1/500."), ("N5 · Poste externo", "Base pinada inclinada 8°", "Estaca de tração", "Pino Ø20 + cabo", "Cabo de borda e estais."), ("N6 · Keder / bolsa de cabo", "Clamp nos cumes · bolsa de cabo Ø12 na borda", "Anéis e postes", "M8 @150 · esticadores", "Tensionar em cruz.")],
 "lodge": [("N1 · Pé do pilar", "Chapa H01", "Grelha", "4 M16", ""), ("N2 · Anel de beiral", "Chapas dobradas 135° (H03)", "8 segmentos", "4 M16 por emenda", "Raios conferidos do centro."), ("N3 · Caibro no vértice", "Talão H04", "Caibro Ø76,1", "Pino + 2 M16", "Pinar em pares opostos."), ("N4 · Caibro na lanterna", "Orelha do anel de compressão", "Caibro", "2 M16", "Anel içado a 4,60 m."), ("N5 · Membrana", "Clamp I02 na lanterna · bolsa de cabo no beiral", "Lona em 8 gomos", "M8 @150 · esticadores", "Balanço 0,90 m uniforme.")],
 "capsule": [("N1 · Anel na longarina", "Chapa gousset", "Anel 60 x 40 x 3 / longarina 40 x 40", "2 M10", "Fabricado em oficina."), ("N2 · Chassi", "U 150 x 50 + travessas", "Anéis", "M12", ""), ("N3 · Pé telescópico", "Ø101,6 em Ø114,3, curso 0,40", "Chassi e estaca", "Pino + M16", "Nivelar ± 5 mm."), ("N4 · Painel de ACM", "Perfil ômega + junta H com EPDM", "Anéis", "Rebite / M6 @300", "Junta 12 mm em todos os anéis.")]}

def build_model(m):
    M = MODELS[m]; tag = M["tag"]; g = M["geo"]; code = f"{tag}-CAM-001"; rigid = m == "capsule"
    D = Doc(code, "PROJETO POR CAMADAS", m)
    parts = M["parts"](); N = BL.model_numbers(m)
    pats = lona.dedupe(lona.PATTERNS[m]()); ext = [p for p in pats if p.group != "interna"]; inn = [p for p in pats if p.group == "interna"]
    man = {s["n"]: s for s in M["manual"]()}
    # ---------------------------------------------------------------- capa
    D.cover("PROJETO POR CAMADAS · DO FERRO À LONA", esc(M["name"]).replace("ZION ", "ZION<br>") + "<br><span style='font-size:22px;letter-spacing:.3em'>POR CAMADAS</span>",
            f"{esc(M['family'])} · {esc(M['dims'])}. Um só documento com todas as camadas da cabana na ordem em que são montadas: fundação e deck, a estrutura de ferro (cada peça com medida, perfil, peso, encaixe e sequência), a fixação da lona nos ferros, o isolamento e a câmara ventilada, o revestimento interno, a lona externa com os padrões de corte, os vidros e as esquadrias, e a sequência completa de montagem em {len(man)} etapas.",
            f'<p class="lead" style="font-size:10.5px">Fontes: lotes {tag}-LOT1 a LOT4-001, padrões {tag}-LON-001, detalhes DET-01 a DET-13, manual de montagem. Unidade: metros nas tabelas de geometria, milímetros nos perfis.</p>')
    # ---------------------------------------------------------------- C0 visão geral
    layers = [("C1", "FUNDAÇÃO E DECK", f"{N['piles']} estacas helicoidais, grelha U 150 x 60, módulos de piso, deck", "lote 1", "etapas 1 a 4"),
              ("C2", "ESTRUTURA DE FERRO", f"≈ {fmt(N['steel'], 0)} kg · {N['n_struct']} tipos de peça" if N["steel"] else "casco monocoque (anéis + longarinas)", "lote 2", "etapas 5 a 7"),
              ("C3", "FIXAÇÃO DA LONA", "perfis keder, trilho de base, clamps, cabos, presilhas", "lote 2 / 3", "com a estrutura"),
              ("C4", "ISOLAMENTO E CÂMARA", "lã de PET 50 mm + manta refletiva + câmara ventilada" if not rigid else "PIR 60 mm + barreira de vapor + câmara 40 mm", "lote 3", "etapa 9"),
              ("C5", "REVESTIMENTO INTERNO", f"forro tensionado em {N['n_inn']} painéis = {fmt(N['inn'], 0)} m², ripados, painéis, marcenaria" if not rigid else f"compensado curvado {fmt(N['inn'], 0)} m²", "lote 3 / 4", "etapa 10"),
              ("C6", "LONA EXTERNA", f"{N['n_ext']} painéis = {fmt(N['ext'], 0)} m² PVDF 1050 g/m²" if not rigid else f"{N['n_ext']} painéis de ACM = {fmt(N['ext'], 0)} m²", "lote 3", "etapa 8"),
              ("C7", "VIDROS E ESQUADRIAS", f"{N['n_esq']} esquadrias = {fmt(N['glass'], 1)} m²", "lote 3", "etapa 11"),
              ("C8", "INSTALAÇÕES E INTERIOR", "elétrica, hidráulica, banho, marcenaria, acabamentos", "lotes 1 e 4", "etapas 12 a 16"),
              ("C9", "TESTES E ENTREGA", "chuva, carga térmica, pré-tensão, as-built", "Zion", "etapa 17")]
    body = h("C0 · VISÃO GERAL DAS CAMADAS", "da fundação à entrega: o que é cada camada, de que lote vem e quando é montada") + '<div class="cam">' + "".join(f"<div><i>{a}</i><b>{b}</b>{esc(c)}<br><span style='color:var(--earth)'>{esc(d)} · {esc(e)}</span></div>" for a, b, c, d, e in layers) + "</div>"
    body += '<p class="lede">Regra do kit: nenhuma peça maior que 4,80 m nem mais pesada que 120 kg; tudo parafusado (sem solda em campo), sem concreto, sem guindaste. Cada camada só começa depois que a anterior foi conferida e liberada: fundação ± 30 mm → grelha ± 10 mm → estrutura ± 15 mm no topo → lona sem rugas → vidros medidos na estrutura montada.</p>'
    D.page(body, "C0 · Visão geral", code=f"{code}-C0")
    if not rigid: D.sheet_page(f"{m}/desenhos/13_camadas_construtivas.svg", f"{code}-C0a", "C0 · As camadas construtivas em pilha explodida", "ver prancha", M["name"])
    D.sheet_page(f"{m}/desenhos/10_modelo_explodido.svg" if not rigid else f"{m}/desenhos/08_isometrica.svg", f"{code}-C0b", "C0 · Modelo explodido", "ver prancha", M["name"])
    # ---------------------------------------------------------------- C1 fundação e deck
    piles = M["piles"]()
    rows = [(f"F{i + 1:02d}", fmt(x, 2), fmt(y, 2)) for i, (x, y) in enumerate(piles)]
    half = (len(rows) + 1) // 2
    body = h("C1 · FUNDAÇÃO E DECK", f"{len(piles)} pontos de fundação · coordenadas (x; y) em m · estaca helicoidal Ø76 com cabeçote ajustável (ou sapata pré-moldada em rocha)")
    body += f'<div class="two"><div>{table(["Ponto", "x", "y"], rows[:half], "xsmall")}</div><div>{table(["Ponto", "x", "y"], rows[half:], "xsmall")}</div></div>'
    D.page(body + f"<p class='note'>{WARN}: comprimento e torque das estacas dependem da sondagem do sítio.</p>", "C1 · Fundação", "flow", code=f"{code}-C1")
    if not rigid:
        D.page(h("C1 · GRELHA DO PISO E TRILHOS · PEÇA A PEÇA", "perfis U 150 x 60 x 3,0 galvanizados, cantoneiras, chapas de emenda, cabeçotes e estacas · comprimentos ≤ 4,80 m") + table(["Cód.", "Peça", "#Qtd", "Comp. (m)", "Perfil", "Aço", "#kg/un", "#kg", "Fabricação", "Encaixe / união"], parts_rows(parts, M["base_prefix"]), "xsmall"), "C1 · Grelha · peças", "flow", code=f"{code}-C1b")
    for i, rel in enumerate(M["lot1"][:3]): D.sheet_page(rel, f"{code}-C1-{i + 1:02d}", "C1 · " + os.path.basename(rel).replace(".svg", "").replace("_", " "), "ver prancha", M["name"])
    D.page(h("C1 · MONTAGEM DA FUNDAÇÃO, GRELHA, PISO E DECK", "etapas 1 a 4 do manual") + manual_rows(m, [1, 2, 3, 4] if not rigid else [1, 2, 5]), "C1 · Montagem", "flow", code=f"{code}-C1m")
    # ---------------------------------------------------------------- C2 estrutura de ferro
    rows = parts_rows(parts, M["struct_prefix"])
    tot = sum(p["peso_total"] for p in parts if isinstance(p["peso_total"], (int, float)) and p["cod"][0] in M["struct_prefix"])
    body = h("C2 · ESTRUTURA DE FERRO · CADA PEÇA, MEDIDA, PERFIL, PESO E ENCAIXE", f"{len(rows)} tipos de peça · ≈ {fmt(tot, 0)} kg · aço ASTM A500 Gr. B / A36 galvanizado a fogo · parafusos 8.8 galv.")
    body += table(["Cód.", "Peça", "#Qtd", "Comp. (m)", "Perfil", "Aço", "#kg/un", "#kg", "Fabricação", "Encaixe / união"], rows, "xsmall")
    D.page(body + f"<p class='note'>{WARN}: bitolas e espessuras são premissas de projeto preliminar; o cálculo estrutural confirma.</p>", "C2 · Lista ferro a ferro", "flow", code=f"{code}-C2")
    if m == "cocoon":
        D.page(h("C2 · GEOMETRIA DOS ARCOS · MEDIDAS PARA A CALANDRA", "elipses com centro a 0,75 m do piso · A0 inclinado 8° recebe o Bico") + table(["Arco", "x (m)", "Tubo", "a (m)", "b (m)", "Topo z (m)", "Vão no piso (m)", "L desenv. (m)", "Segmentos E / C / D (m)", "Plano"], arch_table(g), "small") +
               '<p class="note">Segmentação 34 % / 32 % / 34 % do comprimento desenvolvido, luvas D02 nas emendas, chapas D01 nos pés. Tolerância ± 5 mm no gabarito, ± 15 mm no topo montado.</p>', "C2 · Geometria dos arcos", code=f"{code}-C2b")
        coords = arch_coords(g); keys = list(coords.keys())
        for chunk in (keys[:4], keys[4:]):
            body = h("C2 · COORDENADAS DOS ARCOS · GABARITO 1:1", "pontos (y; z) a cada 0,50 m de desenvolvimento, da base direita ao topo e à base esquerda") + '<div class="cols4">'
            for k in chunk: body += f"<h4>ARCO {k}</h4>" + table(["s", "y", "z"], coords[k], "xsmall")
            D.page(body + "</div>", f"C2 · Coordenadas {chunk[0]} a {chunk[-1]}", "flow", code=f"{code}-C2c")
        bx = g.bico_export(); BT = g.bico_tube_lengths()
        ridge = [(fmt(x, 3), fmt(y, 3), fmt(z, 3)) for (x, y, z) in bx["ridge"]]; edge = bx["edges"][0]; er = [(fmt(x, 3), fmt(y, 3), fmt(z, 3)) for (x, y, z) in [edge[i] for i in range(0, len(edge), 4)] + [edge[-1]]]
        D.page(h("C2 · BICO · CUMEEIRA, BORDAS, COSTELA E TIRANTES", f"cumeeira Ø114,3 ({fmt(BT['ridge'], 2)} m) · bordas Ø60,3 ({fmt(BT['edge'], 2)} m) · costela Ø48,3 ({fmt(BT['rib'], 2)} m) · tirantes Ø12 ({fmt(BT['tie'], 2)} m)") + f'<div class="two"><div><h4>CUMEEIRA B09</h4>{table(["x", "y", "z"], ridge, "xsmall")}</div><div><h4>TUBO DE BORDA B10</h4>{table(["x", "y", "z"], er, "xsmall")}</div></div><p class="note">{WARN}: balanço de 2,40 m; engaste em A0 / A1 e tirantes a validar por cálculo.</p>', "C2 · Bico", code=f"{code}-C2d")
    body = h("C2 · ENCAIXES · COMO CADA FERRO LIGA NO OUTRO", "nó a nó: peça de ligação, o que recebe, parafusos e torque, regra de montagem")
    body += table(["Nó", "Peça de ligação", "Liga em", "Parafusos / torque", "Regra"], [(f"<b>{esc(a)}</b>", esc(b), esc(c), esc(d), e) for a, b, c, d, e in NODES[m]], "small nodes")
    body += f'<h4>REGRAS DE FABRICAÇÃO</h4>{kv([("Gabaritos", "bancada 1:1 impressa do DXF para cada peça curva; conferir 5 pontos antes de soldar chapas"), ("Solda", "só em fábrica, MIG/TIG qualificado; nenhuma solda depois de galvanizar"), ("Galvanização", "a fogo NBR 6323 ≥ 70 µm; furos de respiro nos tubos; roscas protegidas"), ("Fit test", "montar 1 pórtico completo em fábrica, medir, fotografar, só então galvanizar"), ("Marcação", "código gravado em cada peça (ex.: ZC-B03-C), setas de orientação, peso nas peças > 40 kg")])}'
    D.page(body, "C2 · Encaixes", "flow", code=f"{code}-C2e")
    for i, rel in enumerate(M["lot2"]): D.sheet_page(rel, f"{code}-C2-{i + 1:02d}", "C2 · " + os.path.basename(rel).replace(".svg", "").replace("_", " "), "ver prancha", M["name"])
    D.page(h("C2 · MONTAGEM DA ESTRUTURA PASSO A PASSO", "etapas 5 a 7: arcos, travamentos, conferência de esquadro") + manual_rows(m, [5, 6, 7] if not rigid else [3]), "C2 · Montagem", "flow", code=f"{code}-C2m")
    # ---------------------------------------------------------------- C3 fixação da lona
    fix = [(k, lona.KINDS[k][2]) for k in lona.KINDS if any(e[0] == k for p in pats for e in p.edges)]
    body = h("C3 · FIXAÇÃO DA LONA NOS FERROS", "tipos de borda usados neste modelo e as peças metálicas que as recebem")
    body += f'<div class="two"><div>{table(["Borda", "Como fixa"], [(f"<b>{esc(k.upper())}</b>", esc(t)) for k, t in fix], "small")}</div><div>{table(["Cód.", "Peça", "#Qtd", "Comp. (m)", "Perfil", "Encaixe"], [(p["cod"], esc(p["nome"]), p["qtd"], fmt(p["comp"], 2) if isinstance(p["comp"], (int, float)) else "", esc(p["perfil"]), esc(p["uniao"])) for p in parts if p["cod"][0] == "E" or p["cod"] in ("A07", "A08")], "xsmall") if not rigid else kv([("Perfil ômega", "subestrutura de alumínio sobre os anéis para o ACM"), ("Junta H", "alumínio com EPDM, 12 mm em todos os anéis")])}</div></div>'
    D.page(body, "C3 · Fixação da lona", "flow", code=f"{code}-C3")
    if os.path.exists(os.path.join(ROOT, m, "lona", "LN-90_fixacoes.svg")): D.sheet_page(f"{m}/lona/LN-90_fixacoes.svg", f"{code}-C3-01", "C3 · Detalhes de fixação (keder, base, clamp, bolsa, cabo, harpão)", "ver prancha", M["name"])
    # ---------------------------------------------------------------- C4 isolamento
    body = h("C4 · ISOLAMENTO E CÂMARA VENTILADA", "entre a lona externa e o forro: o que vai, em que ordem, e como respira")
    spec = [("Ordem (de fora para dentro)", "lona externa PVDF → câmara ventilada 40 a 60 mm (entrada no rodapé técnico, saída na cumeeira / lanterna) → manta refletiva com face para a câmara → lã de PET 50 mm 25 kg/m³ entre terças / caibros → barreira de vapor → forro tensionado"), ("Fixação", "mantas presas à malha das terças com arame plastificado e fitas; sem compressão (perde R); emendas com fita"), ("Umidade", "instalar só com a lona externa fechada; manta úmida é descartada"), ("Passagens", "eletrodutos e PEX passam no rodapé técnico removível, nunca pela lona"), ("Desempenho-alvo", "R ≈ 1,5 m²K/W na concha; conforto a 0 °C com a climatização dimensionada em DET-09 ⚠️ validar com projeto térmico")] if not rigid else [("Ordem", "ACM externo → câmara 40 mm → PIR 60 mm em painéis curvados → barreira de vapor (manta líquida) → compensado curvado"), ("Juntas", "PIR com encaixe macho-fêmea, fitas nas juntas")]
    body += f'<div class="two"><div>{kv(spec)}</div><div>{bom_table(bom_groups(m, ["isolamento", "envelope"]))}</div></div>'
    D.page(body, "C4 · Isolamento", "flow", code=f"{code}-C4")
    det = {"cocoon": "detalhes/DET-01_cobertura_cocoon.svg", "zenith": "detalhes/DET-02_cobertura_zenith.svg", "lodge": "lodge/desenhos/13_camadas_construtivas.svg", "capsule": "capsule/desenhos/01_conceito.svg"}[m]
    D.sheet_page(det, f"{code}-C4-01", "C4 · Corte do envelope: lona, câmara, isolamento, forro", "ver prancha", M["name"])
    D.page(h("C4 · INSTALAÇÃO DO ISOLAMENTO", "etapa 9 do manual") + manual_rows(m, [9]), "C4 · Montagem", "flow", code=f"{code}-C4m")
    # ---------------------------------------------------------------- C5 revestimento interno
    rows = [(p.id, p.qty, esc(p.name), f"{p.w:.2f} x {p.h:.2f}".replace(".", ","), round(p.area, 2), round(p.area * p.qty, 1), ", ".join(sorted({lona.KINDS[k][2].split(" ·")[0] for k, _ in p.edges}))) for p in inn]
    body = h("C5 · REVESTIMENTO INTERNO", f"forro tensionado ({'Trevira CS 210 g/m²' if not rigid else 'compensado naval curvado laminado'}) em {len(inn)} painéis = {fmt(N['inn'], 0)} m² · ripados · painéis · marcenaria acoplada")
    body += f'<div class="two"><div><h4>PAINÉIS DO FORRO</h4>{table(["Cód.", "#Qtd", "Painel", "Caixa (m)", "#m²", "#m² total", "Bordas"], rows, "xsmall")}</div><div><h4>O QUE REVESTE CADA AMBIENTE</h4>'
    if m == "cocoon":
        from interiores_cocoon import ACAB
        body += table(["Ambiente", "Piso", "Rodapé", "Paredes", "Forro", "Marcenaria"], [(f"<b>{esc(a)}</b>", esc(b), esc(c), esc(d), esc(e), esc(f)) for a, b, c, d, e, f in ACAB], "xsmall")
    else:
        body += kv([("Forro", "tensionado creme com harpão; translúcido sob claraboias / lanterna"), ("Paredes opacas", "painéis SIP ou ripado termotratado sobre placa cimentícia" if m != "capsule" else "compensado curvado laminado em carvalho"), ("Piso", "carvalho de engenharia 14 mm; porcelanato no banho"), ("Rodapé", "técnico removível 150 mm (eletrodutos, PEX)")])
    body += f'<h4>FIXAÇÃO DO FORRO</h4><p class="lede">Trilho harpão de alumínio 40 x 20 (E04) nos talões das terças / cabos; o painel entra com o harpão de PVC soldado e tensiona a quente; recortes de luminárias e difusores com anel.</p></div></div>'
    D.page(body, "C5 · Revestimento interno", "flow", code=f"{code}-C5")
    for rel, t in ((f"{m}/projeto/PA-05_forro_iluminacao.svg", "C5 · Forro e iluminação"), (f"{m}/interiores/IN-02_pisos_acabamentos.svg", "C5 · Pisos e acabamentos"), (f"{m}/interiores/IN-05_detalhes_marcenaria.svg", "C5 · Marcenaria acoplada")):
        if os.path.exists(os.path.join(ROOT, rel)): D.sheet_page(rel, f"{code}-C5-{t[-2:]}", t, "ver prancha", M["name"])
    D.page(h("C5 · INSTALAÇÃO DO FORRO", "etapa 10 do manual") + manual_rows(m, [10]), "C5 · Montagem", "flow", code=f"{code}-C5m")
    # ---------------------------------------------------------------- C6 lona externa
    rows = [(p.id, p.qty, esc(p.name), f"{p.w:.2f} x {p.h:.2f}".replace(".", ","), round(p.area, 2), round(p.area * p.qty, 1), ", ".join(sorted({lona.KINDS[k][2].split(" ·")[0] for k, _ in p.edges})), len(p.holes)) for p in ext]
    body = h("C6 · LONA EXTERNA" if not rigid else "C6 · REVESTIMENTO EXTERNO EM ACM", f"{len(ext)} padrões = {fmt(N['ext'], 0)} m² (forma final; + 12 a 15 % de sobras) · padrões DXF e XLSX em {m}/lona/")
    body += table(["Cód.", "#Qtd", "Painel", "Caixa (m)", "#m²", "#m² total", "Bordas", "#Recortes"], rows, "xsmall")
    body += kv([("Lona", "PVDF tipo II 1050 g/m², poliéster HT 1100 dtex, creme Zion, ≥ 4.200 / 4.000 N/5 cm, classe B / M2, garantia 10 anos"), ("Costuras", "solda HF 40 mm; reforços 150 mm em recortes e cantos; nenhuma costura com linha na face externa"), ("Keder", "cordão Ø10 nas bordas dos arcos, Ø13 na base"), ("Compensação", "pelo confeccionista, com laudo biaxial do tecido; padronagem em rolos de 2,50 a 3,00 m")] if not rigid else [("ACM", "4 mm PVDF champanhe fosco, curvado a frio sobre ômegas; painéis ≤ 2,80 x 1,20 m"), ("Juntas", "perfil H com EPDM e selante PU")])
    D.page(body, "C6 · Lona externa", "flow", code=f"{code}-C6")
    D.sheet_page(f"{m}/lona/LN-01_mapa_paineis.svg", f"{code}-C6-01", "C6 · Mapa de painéis", "ver prancha", M["name"])
    first = [f for f in lona.sheets(m) if f.startswith("LN-1")][:2]
    for i, f in enumerate(first): D.sheet_page(f"{m}/lona/{f}", f"{code}-C6-{i + 2:02d}", "C6 · Padrão de corte " + f.split("_", 1)[1].replace(".svg", "") + " (exemplo; os demais em LN-1n a LN-3n)", "ver prancha", M["name"])
    D.page(h("C6 · INSTALAÇÃO DA LONA EXTERNA", "etapa 8 do manual · vento > 30 km/h suspende") + manual_rows(m, [8]), "C6 · Montagem", "flow", code=f"{code}-C6m")
    # ---------------------------------------------------------------- C7 vidros
    esq = M["esq"]; KG = 30.0
    rows = [(c, esc(n), fmt(w, 2), fmt(hh, 2), nn, round(w * hh, 2), round(w * hh * KG, 0), esc(s), esc(loc)) for (c, n, w, hh, nn, s, loc) in esq]
    D.page(h("C7 · VIDROS E ESQUADRIAS", f"{fmt(N['glass'], 1)} m² · medição na estrutura montada ± 3 mm · panos ≤ 90 kg") + table(["Cód.", "Esquadria", "Larg. (m)", "Alt. (m)", "#Qtd", "#m² un.", "#kg un.", "Especificação", "Localização"], rows, "xsmall") + manual_rows(m, [11] if not rigid else [6]), "C7 · Vidros", "flow", code=f"{code}-C7")
    for rel in (f"{m}/projeto/PA-09_quadro_esquadrias.svg", "detalhes/DET-05_esquadrias.svg"):
        if os.path.exists(os.path.join(ROOT, rel)): D.sheet_page(rel, f"{code}-C7-01", "C7 · " + os.path.basename(rel).replace(".svg", "").replace("_", " "), "ver prancha", M["name"])
    # ---------------------------------------------------------------- C8 sequência completa
    ids = sorted(man.keys())
    D.page(h("C8 · SEQUÊNCIA COMPLETA DE MONTAGEM", f"{len(ids)} etapas · {M['days']} dias · equipe de 4 montadores + líder, mais especialistas") + manual_rows(m, ids[: (len(ids) + 1) // 2]), "C8 · Montagem 1", "flow", code=f"{code}-C8")
    D.page(h("C8 · SEQUÊNCIA COMPLETA DE MONTAGEM (CONTINUAÇÃO)", "instalações, interior, acabamentos, testes e entrega") + manual_rows(m, ids[(len(ids) + 1) // 2:]), "C8 · Montagem 2", "flow", code=f"{code}-C8b")
    tr = M["transport"](); tr = tr["items"] if isinstance(tr, dict) else tr
    D.page(h("C9 · TRANSPORTE E REVISÃO", "volumes do kit · registro de revisão") + table(["Volume", "Dimensões", "#m³", "#kg"], [(esc(a), esc(b), c, d) for (a, b, c, d) in tr], "small") + table(["Rev", "Data", "Descrição"], [("00", "08/10/2026", "Emissão do projeto por camadas, consolidando lotes 1 a 4, padrões de lona, detalhes e manual")], "small"), "C9 · Transporte e revisão", code=f"{code}-C9")
    html_ = D.html().replace("</style>", LAYER_CSS + "</style>", 1)
    path = os.path.join(OUT_DIR, f"{code}_Projeto_por_Camadas.html"); open(path, "w", encoding="utf-8").write(html_); print(os.path.relpath(path, ROOT), len(D.pages) + 1, "páginas")

if __name__ == "__main__":
    for m in (sys.argv[1:] or list(MODELS)): build_model(m)

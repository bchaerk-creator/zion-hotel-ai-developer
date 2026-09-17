# -*- coding: utf-8 -*-
"""ZG-TEC-001 · DOCUMENTO TÉCNICO da Zion Glamping Collection (fases 03 a 09 do método), com a ZION CASULO como piloto
detalhado e o resumo técnico da linha. Segue as seções do master prompt: ficha técnica, desenhos, exploded view em 16 camadas,
camadas construtivas por elemento, estrutura (comparativo + recomendação + malha + conexões), fundação, cobertura, hidráulica,
elétrica (cargas + unifilar), gás (abrigo), climatização (carga térmica preliminar), isolamento, material takeoff, quantitativo
mestre, BOM, pré-fabricação, manual em 15 etapas, ferramentas, logística / transportation pack, orçamento em 18 grupos
(PREÇO A COTAR), checklists de obra e de validação, anexo RFQ. Sem preços. A4 paisagem, vetorial.
Saída: 03_TECNICO/ZG-TEC-001_Documento_Tecnico.html · PDF via export_pdf.js"""
import os, html, math
from build_projeto_arquitetonico import svg_inline, sheets as pa_sheets_list, NAME, TAG, LAYERS
from pa_sheets import AREAS, ESQUADRIAS, NOTAS
from svgkit import zion_mark_html, zion_logo_html, Sheet, GREEN, EARTH, CREAM, STEEL, WOOD2, GLASS, fmt as mfmt
import bom as B, product_book_data as P, ffe
from geometry import Cocoon, Zenith, LODGES, Capsule
from capsule import capsule_materials

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(ROOT, "03_TECNICO"); os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "ZG-TEC-001_Documento_Tecnico.html")
DOC = "ZG-TEC-001"; REV = "REV 00 — CONCEITO"; DATE = "17/09/2026"; PIL = "cocoon"
WARN = '<span class="warn">⚠️ VALIDAÇÃO OBRIGATÓRIA — ENGENHEIRO/ARQUITETO</span>'
COTAR = '<span class="cotar">PREÇO A COTAR</span>'
LG = {k: v() for k, v in LODGES.items()}; CAP = Capsule(); CO = Cocoon(); ZE = Zenith()

def esc(s): return html.escape(str(s))
def fmt(v, n=1):
    if isinstance(v, str): return esc(v)
    return f"{v:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def q(v):
    if isinstance(v, float): return fmt(v, 1).rstrip("0").rstrip(",")
    return str(v)
def exists(rel): return os.path.exists(os.path.join(ROOT, rel))
def sheet(rel): return f'<div class="sheet">{svg_inline(rel)}</div>' if exists(rel) else f'<div class="missing">[{esc(rel)}]</div>'
def img(rel): return f'<img src="../{rel.replace("/renders/web/", "/renders/web/deck/")}" alt="">' if exists(rel) else ""
def table(head, rows, cls=""):
    th = "".join(f"<th{' class=num' if h.startswith('#') else ''}>{esc(h.lstrip('#'))}</th>" for h in head)
    body = "".join("<tr>" + "".join(f"<td{' class=num' if isinstance(c, (int, float)) else ''}>{q(c) if isinstance(c, (int, float)) else c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="t {cls}"><tr>{th}</tr>{body}</table>'

pages = []; toc = []
def page(body, label="", cls="", code=""):
    n = len(pages) + 1
    if label and not cls.startswith("sheetpage"): toc.append((code, label, n))
    pages.append(f'<section class="page {cls}"><div class="head"><span>{zion_mark_html("14px", color="#1B2117")} ZION GLAMPING · {DOC} · {REV}</span><span>{esc(code)}</span><span>{esc(label)}</span></div>{body}<div class="foot"><span>ZION GLAMPING COLLECTION · DOCUMENTO TÉCNICO · SEM PREÇOS</span><span>UNIDADE: m (pranchas existentes) · mm a partir da REV 01</span><span>{DATE} · {n:02d}</span></div></section>')
def h(t, sub=""): return f'<h2>{esc(t)}{f"<small>{esc(sub)}</small>" if sub else ""}</h2>'
def sheet_page(rel, code, title, scale, note=""):
    n = len(pages) + 1
    pages.append(f'<section class="page sheetpage"><div class="strip"><span class="code">{esc(code)}</span><span class="ttl">{esc(title)}</span><span class="scl">{esc(scale)}</span><span class="prod">{esc(note)}</span></div>{sheet(rel)}<div class="foot"><span>ZION GLAMPING · {DOC} · {REV} · {esc(code)}</span><span>{esc(title)}</span><span>{DATE} · {n:02d}</span></div></section>')

bc = B.cocoon_bom(); bz = B.zenith_bom(); bl = B.lodge_bom()
tc = B.transport(bc, "cocoon")
GLASS_M2 = sum(w * hh * n for (_, _, w, hh, n, _, _) in ESQUADRIAS["cocoon"])

# ============================================================================ 00 capa e índice
def capa():
    body = f'''<div class="coverbox"><div class="brand">{zion_mark_html("13mm", color="#FEF5F0", style="margin-right:6mm")}{zion_logo_html("13mm", color="#FEF5F0")}</div><div class="sub">ZION GLAMPING COLLECTION · CABIN DESIGN &amp; ENGINEERING SYSTEM</div>
<h1>DOCUMENTO<br>TÉCNICO</h1><h3>{DOC} · {REV} · {DATE}</h3>
<p class="lead">Projeto técnico conceitual da linha Zion Glamping Collection para desenvolvimento, orçamento e fabricação: piloto ZION CASULO detalhado (desenhos, camadas, estrutura, fundação, cobertura, instalações, materiais, quantitativo, BOM, pré-fabricação, manual de montagem, ferramentas, logística, orçamento em 18 grupos e checklists) e resumo técnico das outras cinco unidades.</p>
<p class="rule">REGRA FUNDAMENTAL · Nenhuma especificação que dependa de cálculo estrutural ou norma foi inventada: onde há dependência, o item está marcado {WARN}. Este documento é um projeto técnico preliminar / executivo conceitual e não substitui ART, RRT, cálculo estrutural, projeto legal ou aprovação municipal. Sem preços: onde não há cotação real, {COTAR}.</p></div>'''
    pages.append(f'<section class="page cover">{body}</section>')

def indice():
    rows = "".join(f"<tr><td>{esc(c)}</td><td>{esc(l)}</td><td class=num>{n:02d}</td></tr>" for c, l, n in toc)
    rev = table(["Rev", "Data", "Descrição", "Autor"], [["00", DATE, "Conceito · emissão inicial do documento técnico da linha, piloto Casulo", "Zion Cabin Design System"], ["01", "—", "Desenvolvimento · após respostas do brief ZG-BRF-001 (sítio, energia, água, esgoto, gás, categoria)", "—"], ["02", "—", "Orçamento · com cotações reais das fábricas (RFQ ZG-RFQ-001)", "—"]])
    codes = table(["Prefixo", "Modelo", "Disciplinas"], [["ZC", "Zion Casulo (piloto)", "ARQ · EST · FUN · COB · HID · ELE · GAS · CLI · ISO · MAT · BOM · QTD · ORC · FAB · LOG · MONT · CHK · RFQ · VAL"], ["ZS · ZL · ZL24 · ZL28 · ZK", "Safari · Lodge 38 · 24 · 28 · Cápsula", "mesmas disciplinas; documentos próprios a partir da REV 01"], ["ZG", "Linha (comum)", "BRF · ARQ (conceito) · TEC (este documento) · RFQ"]])
    return f'{h("ÍNDICE E CONTROLE DE REVISÃO")}<div class="two"><div class="tw">{"<table class=t><tr><th>Código</th><th>Seção</th><th class=num>Seq.</th></tr>" + rows + "</table>"}</div><div>{rev}<h4>SISTEMA DE CÓDIGOS</h4>{codes}<p class="note">Pranchas PA-nn e arquivos DXF ZC-nn existentes mantêm seus códigos como alias; o índice aponta o código de disciplina e a sequência de cada seção (tabelas longas ocupam mais de uma página impressa).</p></div></div>'

# ============================================================================ 01 ficha técnica
def ficha():
    U = [("ZION CASULO", "ZC", 48.0, 29.9, "2 + 1 · 1 king", "banheira + chuveiro", "mini cozinha: indução 2 bocas, forno, geladeira, air fryer", "deck 29,9 m² sob o Bico", "hot tub opcional", "split 12k dutado", "boiler elétrico", "SIGNATURE*"),
         ("ZION SAFARI", "ZS", 48.4, 28.0, "2 + 1 · 1 king", "bancada dupla + banheira", "Ilha do Café", "terraço + passarela", "hidromassagem", "split dutado", "boiler elétrico", "SIGNATURE*"),
         ("ZION LODGE 38", "ZL", LG["lodge"].floor_area(), LG["lodge"].deck_area(), "2 + 1 · 1 king", "banheira de sentar + chuveiro", "café / minibar", "deck 3 faces + vela", "fire pit opcional", "split dutado (ático)", "boiler elétrico", "PREMIUM*"),
         ("ZION LODGE 24", "ZL24", LG["lodge24"].floor_area(), LG["lodge24"].deck_area(), "2 · 1 king", "chuveiro", "café / minibar", "deck 1 face + vela", "não", "split de parede", "boiler elétrico", "STANDARD*"),
         ("ZION LODGE 28", "ZL28", LG["lodge28"].floor_area(), LG["lodge28"].deck_area(), "2 + 1 · 1 king", "chuveiro", "café / minibar", "terraço 3 faces + vela", "não", "split dutado", "boiler elétrico", "PREMIUM*"),
         ("ZION CÁPSULA", "ZK", CAP.floor_area(), CAP.deck_area(), "2 · 1 queen", "chuveiro", "café / minibar", "deck frontal 8,3 m²", "não", "split 9k dutado (técnico)", "boiler 80 L (técnico)", "PREMIUM*")]
    rows = [[f"<b>{n}</b>", c, a, e, round(a + e, 1), g, b, k, d, j, cl, aq, cat] for (n, c, a, e, g, b, k, d, j, cl, aq, cat) in U]
    t = table(["Modelo", "Código", "#Área int. m²", "#Área ext. m²", "#Total m²", "Hóspedes · camas", "Banheiro", "Cozinha", "Deck / varanda", "Banheira externa", "Climatização", "Água quente", "Categoria"], rows, "small")
    common = table(["Sistema", "Premissa da linha (brief ZG-BRF-001, seção 5)"], [
        ["Sauna · piscina · fireplace", "não previstos na base; lareira ecológica (FF&E E08) e fire pit (D07) opcionais; sauna e piscina só em configuração Ultra Luxury, a definir no brief"],
        ["Sistema elétrico", "rede bifásica 220 V, quadro por cabana (12 a 16 circuitos), DR 30 mA, aterramento; pré-instalação solar (eletroduto + espaço no quadro)"],
        ["Sistema hidráulico", "PEX Ø25/20/16; reservatório central pressurizado + reserva de 500 L por cabana; boiler elétrico; registro geral e filtro por unidade"],
        ["Esgoto", "coletor Ø100 por gravidade a biodigestor por grupo de 4 a 6 cabanas + vala de infiltração; águas cinzas separadas (opção de reuso)"],
        ["Gás", "não previsto (tudo elétrico); alternativa GLP com abrigo-tipo na seção 10"], ["Solar", "pré-instalação; geração fotovoltaica centralizada do empreendimento, a definir"],
        ["Automação", "fechadura digital, cenas de luz, termostato, blackout motorizado, sensor de presença; hub por cabana"]])
    return h("01 · FICHA TÉCNICA DE IDENTIDADE", "as seis unidades da linha · * categoria proposta, a confirmar no brief") + t + "<h4>SISTEMAS COMUNS · PREMISSAS</h4>" + common

# ============================================================================ 02 desenhos (piloto)
def desenhos():
    S = pa_sheets_list(PIL)
    rows = [[c, t, s, n] for (c, t, s, rel, n) in S]
    body = h("02 · DESENHOS DO PILOTO · ZION CASULO", "pranchas PA-00 a PA-12 (24 folhas) reproduzidas nas páginas seguintes; DXF em cocoon/projeto/dxf") + table(["Prancha", "Título", "Escala", "Conteúdo"], rows, "small") + \
        '<p class="note">O que o método pede além do que já está nas pranchas e será incorporado na REV 01: pontos hidráulicos e elétricos na planta baixa (hoje em DET-07 e DET-08), planta de cobertura com rufos e pontos de manutenção (hoje calhas, tubos de queda e claraboia), implantação com estacionamento e paisagismo do sítio real, e cotas em mm.</p>'
    page(body, "02 · Desenhos do piloto", code="ZC-ARQ-001")
    for (c, t, s, rel, n) in S: sheet_page(rel, f"ZC-ARQ · {c}", t, s, n)

# ============================================================================ 03 exploded view
def exploded():
    L16 = [("01", "Fundação", "44 estacas helicoidais Ø76 + cabeçotes ajustáveis"), ("02", "Estrutura do piso", "grelha de vigas U 150 x 60 x 3,0 + vigotas 50 x 150"), ("03", "Piso", "PIR 50 + compensado 18 + carvalho 14 / porcelanato"),
           ("04", "Estrutura das paredes", "anel A0, 7 arcos elípticos, trilhos de base, quadro da cauda (a concha é parede e cobertura)"), ("05", "Isolamento", "lã de PET 50 mm + manta refletiva, entre terças"), ("06", "Fechamento interno", "forro tensionado Trevira CS + painéis ripados"),
           ("07", "Fechamento externo", "membrana PVDF 1050 g/m² em 7 painéis com keder"), ("08", "Esquadrias", "anel de vidro V1, porta PV1, 6 Janelas Olho, Espinha de Luz CL1"), ("09", "Estrutura da cobertura", "terças Ø48,3 + treliça da espinha + cabos em X (mesma concha)"),
           ("10", "Isolamento da cobertura", "idem 05, contínuo"), ("11", "Cobertura", "idem 07, contínua; calha oculta no rodapé"), ("12", "Instalações", "kit elétrico (piso técnico + forro), kit hidráulico (PEX + esgoto), evaporadora no ático"),
           ("13", "Deck", "15 módulos de cumaru sobre vigas U e estacas + escada"), ("14", "Mobiliário", "FF&E: cama, chaise, mini cozinha, closet, bancada"), ("15", "Equipamentos", "climatização, boiler, geladeira, cooktop, forno, air fryer, automação, louças e metais"), ("16", "Acabamentos", "pintura, selantes, pedra, latão, enxoval")]
    body = h("03 · EXPLODED VIEW · 16 CAMADAS", "a cabana como sistema modular montado de baixo para cima") + f'<div class="two"><div>{sheet("cocoon/desenhos/13_camadas_construtivas.svg")}</div><div>{table(["#", "Camada do método", "No Zion Casulo"], [[a, b, c] for a, b, c in L16], "small")}<p class="note">Na concha do Casulo as camadas 04/09, 05/10 e 07/11 são o mesmo sistema contínuo (não há distinção entre parede e cobertura). O modelo explodido da estrutura está em PA-12b e o das camadas em PA-12c.</p></div></div>'
    page(body, "03 · Exploded view", code="ZC-ARQ-003")

# ============================================================================ 04 camadas por elemento
CAMADAS = {
    "ENVELOPE DA CONCHA (parede + cobertura) · exterior → interior": [
        ("Membrana PVDF 1050 g/m² tipo III, classe B1", "1,0 mm", "Serge Ferrari Précontraint 1002 / Sioen / Mehler", "estanqueidade, tensão, acabamento", "1,15 m²/m²", "painéis deslizados no keder; pré-tensão 2,5 kN/m; emendas HF 40 mm"),
        ("Perfil duplo keder de alumínio sobre os arcos", "24 x 70 mm", "extrusão sob desenho", "fixação e emenda dos painéis", "0,95 m/m²", "parafusado M8 a cada 300 mm no arco"),
        ("Câmara ventilada", "60 mm", "—", "retira o calor da membrana", "—", "admissão no rodapé, saída na espinha; tela anti-inseto"),
        ("Manta refletiva de alumínio (bolha)", "4 mm", "manta dupla face", "barreira radiante", "1,05 m²/m²", "fitada nas emendas, face refletiva para a câmara"),
        ("Lã de PET 50 mm, 25 kg/m³", "50 mm", "Trisoft / Isosoft", "isolamento térmico e acústico", "1,08 m²/m²", "entre terças, presa com fitas; não comprimir"),
        ("Terças Ø48,3 e cabos (estrutura secundária)", "—", "ASTM A500", "apoio da membrana e do forro", "—", "rosqueadas entre arcos; cabos a 2 kN"),
        ("Instalações (fitas LED, cabos, sensores)", "—", "—", "luz indireta e automação", "—", "eletrodutos flexíveis atrás do forro; caixas acessíveis"),
        ("Forro tensionado Trevira CS classe M1", "1,0 mm", "Clipso / Barrisol acústico", "acabamento, acústica, luz difusa", "1,05 m²/m²", "7 painéis tensionados em trilho; sem emendas visíveis"),
        ("Painel ripado termotratado (cabeceira, rodapés)", "20 x 40 mm", "pinus termotratado", "acabamento e proteção", "0,14 m²/m² interno", "fixação oculta em sarrafos")],
    "PISO INTERNO · superior → inferior": [
        ("Carvalho de engenharia", "14 mm", "click, verniz fosco", "acabamento", "1,08 m²/m²", "flutuante sobre manta; junta de dilatação no perímetro"),
        ("Compensado naval", "18 mm", "BR-Ply naval fenólico", "contrapiso estrutural", "1,05 m²/m²", "parafusado às vigotas a cada 200 mm"),
        ("PIR 50 mm + manta de PE", "50 mm", "PIR faceado alumínio", "isolamento térmico do piso", "1,05 m²/m²", "entre vigotas, encaixe justo, fitado"),
        ("Vigotas 50 x 150 tratadas (autoclave)", "150 mm", "pinus CCA", "estrutura do módulo de piso", "2,5 m/m²", "a cada 400 mm; módulos de 1,20 x 2,40 pré-montados"),
        ("Fechamento inferior: placa cimentícia + tela", "8 mm", "placa cimentícia", "proteção contra roedores e umidade", "1,05 m²/m²", "parafusada por baixo antes do içamento do módulo"),
        ("Vigas U 150 x 60 x 3,0 galvanizadas", "150 mm", "ZAR-230 Z275", "grelha principal", "1,9 m/m²", "parafusadas M12 aos cabeçotes"),
        ("Cabeçote ajustável + estaca helicoidal Ø76", "—", "galvanizado a fogo", "fundação", "0,9 un/m²", "nivelamento ± 5 mm; torque registrado")],
    "DECK · superior → inferior": [
        ("Régua de cumaru 20 x 140 mm", "20 mm", "cumaru KD", "piso externo", "7,1 m/m² (+10 %)", "clips ocultos inox; junta 6 mm; óleo protetor"),
        ("Vigotas 50 x 150 tratadas", "150 mm", "pinus CCA", "apoio das réguas", "2,5 m/m²", "a cada 400 mm; módulos de deck 1,20 x 2,40"),
        ("Vigas U 150 galvanizadas + estacas", "—", "ZAR-230 / galv.", "estrutura e fundação", "—", "mesma grelha do piso interno")],
    "BANHO E ÁREA MOLHADA · superior → inferior (piso) e interior → exterior (parede)": [
        ("Porcelanato 60 x 120 antiderrapante", "10 mm", "R11", "acabamento", "1,10 m²/m²", "argamassa AC-III; rejunte epóxi; caimento 1 % para o ralo linear"),
        ("Argamassa colante AC-III", "5 mm", "—", "assentamento", "5 kg/m²", "dupla colagem"),
        ("Impermeabilização em manta líquida", "2 mm", "poliuretano ou acrílica", "estanqueidade", "1,5 kg/m²", "3 demãos; subir 30 cm nas paredes; teste de lâmina 72 h"),
        ("Placa cimentícia", "10 mm", "—", "base rígida", "1,05 m²/m²", "sobre o compensado naval, juntas tratadas"),
        ("Parede do banho: porcelanato / ripado sobre placa cimentícia", "10 + 10 mm", "—", "acabamento e base", "1,10 m²/m²", "porcelanato na zona do chuveiro; ripado nas demais"),
        ("Montantes LSF 90 mm + lã de PET 50 mm", "90 mm", "guia e montante 90 x 40", "estrutura da parede do banho", "3,0 m/m²", "a cada 400 mm; passagem de PEX e esgoto"),
        ("Placa interna do lado da suíte: painel ripado", "20 mm", "termotratado", "acabamento da cabeceira", "1,0 m²/m²", "fixação oculta")],
    "FACHADA DE VIDRO (anel inclinado 8°) · exterior → interior": [
        ("Vidro insulado 6 lam + 12 Ar + 6 temp low-e", "24 mm", "U ≈ 1,6 W/m²K · FS 0,40", "fechamento transparente", "1,0 m²/m²", "8 painéis; calços EPDM; silicone estrutural neutro"),
        ("Anel curvo de alumínio 120 x 60 RPT bronze", "120 mm", "extrusão calandrada", "moldura estrutural do vidro", "10,2 m/un", "parafusado ao anel A0 a cada 300 mm"),
        ("Montantes 100 x 50 e travessa a 2,40", "100 mm", "alumínio RPT", "divisão dos painéis e porta", "5 un", "junta de dilatação com EPDM"),
        ("Soleira com dreno e pingadeira", "—", "alumínio", "estanqueidade na base", "6,5 m", "dreno para fora do deck")],
    "ESQUADRIAS · JANELAS OLHO · exterior → interior": [
        ("Flange de membrana (bolsa costurada)", "—", "PVDF", "vedação da membrana ao requadro", "5,5 m/un", "cordão keder no requadro"),
        ("Requadro em madeira laminada", "220 mm", "eucalipto laminado", "moldura e acabamento", "1 un", "elipse 1,60 x 0,95 em 4 segmentos colados"),
        ("Vidro insulado (jateado no banho)", "24 mm", "idem fachada", "fechamento", "1 un", "colado em gaxeta EPDM"),
        ("Ferragem basculante 15° (JO1)", "—", "inox", "ventilação", "2 un", "limitador e trinco")]}

def camadas():
    for i, (elem, rows) in enumerate(CAMADAS.items()):
        t = table(["Camada · material", "Espessura", "Referência", "Função", "Qtd / m²", "Instalação"], [list(r) for r in rows], "small")
        extra = ""
        if i == 0: extra = f'<div class="two"><div>{t}</div><div>{sheet("detalhes/DET-01_cobertura_cocoon.svg")}<p class="note">DET-01: seção do envelope no arco, resistência térmica U ≈ 0,62 W/m²K (envelope) · vidro U ≈ 1,6 W/m²K.</p></div></div>'
        elif i == 1: extra = f'<div class="two"><div>{t}</div><div>{sheet("detalhes/DET-04_fundacao.svg")}</div></div>'
        elif i == 4: extra = f'<div class="two"><div>{t}</div><div>{sheet("detalhes/DET-05_esquadrias.svg")}</div></div>'
        else: extra = t
        page(h(f"04 · CAMADAS CONSTRUTIVAS · {elem.split(' ·')[0]}", elem.split("·", 1)[1].strip() if "·" in elem else "") + extra, f"04 · Camadas · {elem.split(' ·')[0].title()}", code="ZC-ARQ-004")

# ============================================================================ 05 estrutura
def estrutura():
    comp = [["Madeira maciça / laminada", "médio", "médio", "média", "boa (tratada)", "peças longas, frágeis", "alta (verniz, cupim)", "curvas grandes exigem laminação cara"],
            ["Wood frame", "leve", "baixo", "alta", "boa se seco", "painéis planos", "média", "não faz a concha curva"],
            ["Steel frame (LSF)", "leve", "baixo-médio", "alta", "boa (galvanizado)", "painéis planos", "baixa", "só para paredes planas (parede do banho)"],
            ["Estrutura metálica tubular galvanizada", "leve-médio", "médio", "alta (kit)", "muito boa (galv. a fogo)", "segmentos ≤ 4,2 m, contêiner", "muito baixa", "faz qualquer curva por calandra; sem solda em campo · RECOMENDADO"],
            ["Híbrida (aço + madeira)", "médio", "médio", "média", "boa", "mista", "média", "usada nos pilares revestidos dos Lodges"],
            ["Módulos pré-fabricados fechados", "pesado", "alto (1ª un.)", "muito alta em campo", "boa", "transporte especial (AET)", "baixa", "é o caso da Cápsula (monocoque)"]]
    parts = P.cocoon_parts()
    prows = [[p["cod"], p["nome"], p["qtd"], p["perfil"], p["aco"], p["esp"], p["comp"], p["peso_total"], p["fab"], p["uniao"]] for p in parts]
    crows = [[c[0], c[1], c[2], c[3], c[4], c[5], c[6]] for c in P.COCOON_CONNECTIONS]
    body = h("05 · SISTEMA ESTRUTURAL · COMPARATIVO E RECOMENDAÇÃO", "avaliação qualitativa; o cálculo define bitolas") + table(["Sistema", "Peso", "Custo", "Velocidade", "Durabilidade", "Transporte", "Manutenção", "Observação"], comp, "small") + \
        f'<p class="lede">Recomendação: estrutura metálica tubular em aço ASTM A500 galvanizado a fogo, calandrada em fábrica, em segmentos de até 4,2 m unidos por luvas internas e parafusos classe 8.8, sem solda em campo. Justificativa: é o único sistema que produz a concha elíptica do Casulo, os mastros do Safari e os caibros do Lodge com o mesmo processo, cabe em contêiner, monta em dias com equipe de quatro pessoas e tem manutenção quase nula. Vento de projeto V0 = 45 m/s (NBR 6123), verificação NBR 8800. {WARN}</p>' + \
        f'<div class="stats"><div><b>{fmt(bc["steel_kg"], 0)}</b><span>kg de aço galvanizado</span></div><div><b>{len(parts)}</b><span>famílias de peças</span></div><div><b>{len(P.COCOON_CONNECTIONS)}</b><span>tipos de conexão</span></div><div><b>44</b><span>estacas helicoidais</span></div></div>'
    page(body, "05 · Estrutura · comparativo", code="ZC-EST-001")
    page(h("05 · MALHA ESTRUTURAL · PLANTA E ISOMÉTRICA", "eixos, anel, arcos, terças, trilhos, vigas, estacas") + f'<div class="two"><div>{sheet("cocoon/desenhos/03b_planta_estrutural.svg")}</div><div>{sheet("cocoon/desenhos/12_estrutura_isometrica.svg")}</div></div>', "05 · Malha estrutural", code="ZC-EST-002")
    page(h("05 · PEÇAS ESTRUTURAIS · PILARES, VIGAS, ARCOS, TRAVAMENTOS", "lista peça a peça do kit metálico do Casulo") + table(["Cód.", "Peça", "#Qtd", "Perfil", "Aço", "#Esp. mm", "#Comp. m", "#Peso kg", "Fabricação", "União"], prows, "small"), "05 · Peças estruturais", cls="flow", code="ZC-EST-003")
    page(h("05 · PONTOS DE CONEXÃO · CHAPAS, LUVAS E PARAFUSOS", "cada ligação do kit, do cabeçote ao keder") + table(["Cód.", "Peça A", "Peça B", "Tipo de ligação", "Fixador", "#Un.", "#Parafusos/un"], crows, "small") + f'<div class="two"><div>{sheet("detalhes/DET-10_arcos_cocoon.svg")}</div><div>{sheet("detalhes/DET-03_ancoragem.svg")}</div></div>', "05 · Conexões", code="ZC-EST-004")

# ============================================================================ 06 fundação
def fundacao():
    alt = [["A · Estacas helicoidais Ø76 (base da linha)", "qualquer solo com N ≥ 4; declividade até 20 %", "sem escavação, sem concreto, removível, 1 dia", "exige torque de cravação; rocha aflorante impede", "44 un. (Casulo)"],
           ["B · Microestacas / estacas raiz", "solo mole ou rochoso raso", "alta capacidade", "concreto, equipamento pesado, 3 a 5 dias", "16 a 20 un."],
           ["C · Sapatas / blocos de concreto com pilaretes metálicos", "solo firme, terreno plano, acesso fácil", "custo baixo", "escavação, cura, não removível", "16 a 20 un."],
           ["D · Pilares metálicos sobre base de brita compactada", "solo de boa capacidade, apoio provisório / eventos", "rápido e removível", "sem resistência a arrancamento (vento)", "16 a 20 un."],
           ["E · Fundação pontual em tubo cravado (ground screw leve)", "Cápsula e decks", "4 pontos, cravação manual", "capacidade limitada", "4 + 4 un. (Cápsula)"],
           ["F · Sistema removível sobre patins", "instalação temporária em piso existente", "sem intervenção", "só em piso rígido nivelado", "—"]]
    consid = [["Terreno / sondagem", "SPT ou ensaio de torque em cada posição; comprimento da estaca 1,5 a 2,5 m conforme N"], ["Declividade", "até 15 %: compensação nos cabeçotes (curso 0,30 m); 15 a 30 %: hastes de extensão e travamento em X sob o deck"],
              ["Umidade e drenagem", "cabeçotes acima da cota de inundação; dreno francês a montante; pingadeira da membrana longe das estacas"], ["Peso", "Casulo 8,6 t mobiliada + 2 kN/m² de uso: ≈ 45 kN/estaca de projeto"],
              ["Vento", "arrancamento e tombamento pelo momento da concha; estacas de canto com hélice dupla"], ["Acesso", "cravadeira hidráulica em miniescavadeira ou motor portátil; sem caminhão-betoneira"], ["Desmontagem", "estacas desatarraxadas e reutilizadas; sítio volta ao natural"]]
    page(h("06 · FUNDAÇÃO · ALTERNATIVAS E CRITÉRIOS", f"nunca dimensionar sem geotecnia e cálculo · {WARN}") + table(["Alternativa", "Quando", "Vantagem", "Limitação", "Quantidade"], alt, "small") + "<h4>CONSIDERAÇÕES DE PROJETO</h4>" + table(["Fator", "Critério adotado"], consid, "small"), "06 · Fundação", code="ZC-FUN-001")

# ============================================================================ 07 cobertura
def cobertura():
    page(h("07 · SISTEMA DE COBERTURA · MEMBRANA, DRENAGEM E DETALHE", "estrutura, keder, isolamento, membrana, calha oculta, tubos de queda, ventilação") +
         f'<div class="two"><div>{sheet("cocoon/projeto/PA-04_planta_cobertura.svg")}</div><div>{sheet("detalhes/DET-06_drenagem.svg")}</div></div>' +
         table(["Item", "Especificação"], [["Estrutura", "7 arcos + anel A0 + terças Ø48,3 a cada 1,20 m + treliça da Espinha de Luz"], ["Membrana", "PVDF 1050 g/m² em 7 painéis, keder duplo, pré-tensão 2,5 kN/m; garantia 15 anos"],
                                            ["Isolamento", "lã de PET 50 mm + manta refletiva; câmara ventilada 60 mm com admissão no rodapé e saída na espinha"], ["Impermeabilização", "a própria membrana; bolsas soldadas HF nas Janelas Olho e na espinha; selante PU nas flanges"],
                                            ["Calha e rufos", "calha oculta no rodapé da membrana (perfil de alumínio 80 x 60) sem rufo aparente; pingadeira contínua"], ["Drenagem", "4 tubos de queda Ø75 nas pernas dos arcos, dispersão em caixa de brita; chuva de projeto 150 mm/h"],
                                            ["Ventilação", "câmara + respiro na espinha; tela anti-inseto"], ["Manutenção", "lavagem semestral; inspeção de costuras e keder; retensão com esticadores acessíveis do chão"]], "small"), "07 · Cobertura", code="ZC-COB-001")

# ============================================================================ 08 hidráulica
def hidraulica():
    pts = [["Lavatório", "AF Ø16 · AQ Ø16", "Ø40 · sifão", "misturador monocomando latão"], ["Bacia sanitária", "AF Ø16", "Ø100", "caixa acoplada dual flush"], ["Chuveiro", "AF Ø16 · AQ Ø16", "Ø50 · ralo linear", "ducha 250 mm + ducha manual"],
           ["Banheira 1,60 x 0,76", "AF Ø20 · AQ Ø20", "Ø50", "misturador de banheira"], ["Mini cozinha (cuba 0,40 x 0,35)", "AF Ø20 · AQ Ø20", "Ø50 + caixa de gordura", "torneira gourmet, filtro, sifão"], ["Ducha externa / hot tub (opcional)", "AF Ø20 · AQ Ø20", "Ø50 (hot tub: bomba própria)", "registro externo"],
           ["Boiler elétrico 80 L", "AF Ø20 → AQ Ø20", "válvula de alívio Ø20", "no ático técnico, 2,5 kW"], ["Registro geral + filtro + redutor de pressão", "Ø25", "—", "caixa de inspeção externa na cauda"]]
    sist = [["Alimentação", "ramal PEX Ø25 do reservatório central pressurizado (premissa) · reserva 500 L por cabana (opcional, sob o deck)"], ["Pressão", "mínima 10 mca nos pontos; máxima 40 mca; redutor na entrada"],
            ["Água quente", "boiler elétrico 80 L (2,5 kW) no ático; recirculação não prevista (distâncias < 6 m); tubos AQ isolados"], ["Esgoto", "ramais Ø40/50 → coletor Ø100 i = 2 % → caixa de inspeção → biodigestor por grupo (premissa) → vala de infiltração"],
            ["Ventilação", "tubo de ventilação Ø50 até a cauda, acima da membrana"], ["Águas cinzas", "opção: separação de chuveiro/lavatório para reuso em irrigação (filtro + reservatório)"], ["Águas pluviais", "4 TQ Ø75 → caixas de brita → dispersão; sem rede"],
            ["Manutenção", "todos os registros na caixa da cauda; boiler pela tampa do ático; sifões acessíveis pelo rodapé removível"]]
    page(h("08 · SISTEMA HIDRÁULICO · ESQUEMA E DIÂMETROS PRELIMINARES", f"dimensionamento definitivo · {WARN}") + f'<div class="two"><div>{sheet("detalhes/DET-08_hidraulica.svg")}</div><div>{table(["Ponto", "Alimentação", "Esgoto", "Equipamento"], pts, "small")}{table(["Sistema", "Especificação preliminar"], sist, "small")}</div></div>', "08 · Hidráulica", code="ZC-HID-001")

# ============================================================================ 09 elétrica
CIRC = [("C1", "Iluminação interna (fitas LED, arandelas, spots)", 320, 10, 1.5), ("C2", "Iluminação externa (deck, balizadores)", 150, 10, 1.5), ("C3", "Tomadas estar e suíte (TUG)", 1500, 16, 2.5), ("C4", "Tomadas banho (TUG, secador)", 1800, 16, 2.5),
        ("C5", "Mini cozinha: tomadas (geladeira 120 L, air fryer 1,5 kW, cafeteira, chaleira)", 2500, 20, 2.5), ("C6", "Climatização split inverter 12k BTU", 1300, 16, 2.5), ("C7", "Boiler elétrico 80 L", 2500, 20, 4.0), ("C8", "Automação, roteador, fechadura, sensores", 100, 10, 1.5),
        ("C9", "Exaustor do banho + depurador da mini cozinha + ventilação da câmara", 180, 10, 1.5), ("C10", "Blackout e telas motorizadas", 200, 10, 1.5), ("C11", "Reserva (hot tub 4 kW opcional, circuito dedicado)", 0, 25, 6.0), ("C12", "Reserva", 0, 16, 2.5),
        ("C13", "Cooktop de indução 2 bocas (TUE dedicada, 220 V)", 3500, 20, 4.0), ("C14", "Forno elétrico compacto 45 L (TUE dedicada)", 1800, 16, 2.5)]

def eletrica():
    tot = sum(c[2] for c in CIRC); dem = tot * 0.6; I = dem / 220
    rows = [[c[0], c[1], c[2], f"{c[3]} A", f"{c[4]} mm²"] for c in CIRC]
    ger = 50 if I > 38 else 40
    rows.append(["", "<b>Carga instalada estimada</b>", tot, "", ""]); rows.append(["", "<b>Demanda estimada (fator 0,6)</b>", round(dem), f"{I:.0f} A a 220 V", f"geral {ger} A + DR {ger} A 30 mA"])
    uni = [["Alimentação", "220 V bifásico, 2F + N + T; ramal 3 x 16 mm² cobre até 40 m (queda ≤ 3 %) do quadro de distribuição do empreendimento (mini cozinha com cocção elétrica)"], ["Quadro", f"QDC 16 circuitos no ático técnico, DPS classe II, DR geral {ger} A 30 mA, disjuntores por circuito, barramento de terra; cooktop e forno em circuitos dedicados (TUE)"],
           ["Aterramento", "haste 2,4 m + malha nas estacas (aproveitamento das estacas helicoidais como eletrodo, a validar)"], ["Caminhos", "piso técnico (eletroduto corrugado Ø25 sob o compensado) e atrás do forro; caixas acessíveis nos rodapés"],
           ["Solar", "pré-instalação: eletroduto Ø32 até a cauda e espaço para string box / inversor; geração centralizada (premissa)"], ["Automação", "hub por cabana; cenas de luz; termostato; fechadura digital; sensores de presença e de abertura"]]
    page(h("09 · SISTEMA ELÉTRICO · CIRCUITOS, CARGAS E UNIFILAR CONCEITUAL", f"cargas estimadas por equipamento · {WARN}") + f'<div class="two"><div>{table(["Circ.", "Descrição", "#W", "Disjuntor", "Cabo"], rows, "small")}</div><div>{sheet("detalhes/DET-07_eletrica.svg")}{table(["Item", "Especificação preliminar"], uni, "small")}</div></div>', "09 · Elétrica", code="ZC-ELE-001")

# ============================================================================ 10 gás
def det14_gas():
    """DET-14 · abrigo-tipo para 2 botijões P-45 (alternativa GLP), planta e corte."""
    sh = Sheet(1600, 1000, scale=220, ox=200, oy=700)
    sh.header("DET-14 · Abrigo dos botijões (alternativa GLP)", "Abrigo externo para 2 x P-45 junto à cauda · dimensões preliminares · NBR 13523 / NBR 15526 · ⚠️ validação obrigatória")
    # planta
    sh.text_px(200, 120, "PLANTA · 1:10", size=11, weight=700, spacing=0.25, anchor="start")
    sh.rect(0, 0, 1.0, 0.6, fill="#F3EEE4", stroke=GREEN, sw=1.6); sh.rect(0.03, 0.03, 0.97, 0.57, fill="none", stroke=GREEN, sw=0.6, dash="3 2")
    for x in (0.27, 0.73): sh.circle(x, 0.3, 0.19, fill="#FFFFFF", stroke=GREEN, sw=1.0); sh.text(x, 0.3, "P-45", 9, GREEN, dy=3)
    sh.line(0.0, 0.0, 1.0, 0.0, EARTH, 3); sh.text(0.5, -0.09, "porta veneziana 1,00 x 1,10 (abre para fora)", 8, EARTH)
    sh.rect(-0.2, 0.0, 0.0, 0.6, fill=sh.pattern("hatch"), stroke=GREEN, sw=0.6); sh.text(-0.1, 0.68, "cauda da cabana", 7.5, GREEN)
    sh.dim(0, 0.75, 1.0, 0.75, 0.0, label="1,00"); sh.dim(1.15, 0, 1.15, 0.6, 0.0, label="0,60")
    sh.leader(0.97, 0.45, 1.45, 0.62, "regulador 1º estágio + registro geral", 8.5); sh.leader(0.5, 0.57, 1.45, 0.5, "tubo de cobre Ø1/2\" embutido em eletroduto até o ponto", 8.5)
    sh.text_px(200, 560, "afastamentos: ≥ 1,50 m de aberturas (Olho do banho, tampa do ático) · ≥ 3,00 m de fontes de ignição e da condensadora · piso nivelado e não combustível · não instalar sob o deck", size=9, anchor="start", fill=EARTH)
    # corte
    sh.ox, sh.oy = 1000, 700
    sh.text_px(1000, 120, "CORTE · 1:10", size=11, weight=700, spacing=0.25, anchor="start")
    sh.rect(0, 0, 1.0, 1.2, fill="#F3EEE4", stroke=GREEN, sw=1.6); sh.rect(0, -0.1, 1.0, 0.0, fill=STEEL, stroke="none")
    for x in (0.27, 0.73): sh.rect(x - 0.19, 0.0, x + 0.19, 0.85, fill="#FFFFFF", stroke=GREEN, sw=1.0); sh.rect(x - 0.05, 0.85, x + 0.05, 0.95, fill=STEEL, stroke="none")
    for y in (0.08, 0.16, 1.04, 1.12): sh.line(0.0, y, 1.0, y, GREEN, 0.8, dash="4 2")
    sh.leader(0.5, 0.12, 1.3, 0.2, "ventilação inferior permanente ≥ 1/10 da área do piso", 8.5); sh.leader(0.5, 1.08, 1.3, 1.02, "ventilação superior permanente", 8.5)
    sh.leader(0.73, 0.9, 1.3, 0.8, "válvula + regulador; mangueira NBR 8613 ≤ 0,80 m", 8.5)
    sh.rect(0.0, 1.2, 1.0, 1.28, fill=WOOD2, stroke=GREEN, sw=0.8); sh.text(0.5, 1.36, "cobertura inclinada, chapa galvanizada", 8, EARTH)
    sh.dim(1.6, 0, 1.6, 1.2, 0.0, label="1,20"); sh.dim(0, -0.25, 1.0, -0.25, 0.0, label="1,00")
    sh.text_px(1000, 560, "identificação: placa 'GLP · INFLAMÁVEL · NÃO FUMAR' · extintor PQS 4 kg a 5 m · teste de estanqueidade após instalação", size=9, anchor="start", fill=EARTH)
    sh.title_block("LINHA · ALTERNATIVA GLP", "Abrigo dos botijões", "1:10 (A1)", "DET-14", "Detalhe construtivo · preliminar · validação obrigatória")
    out = os.path.join(ROOT, "detalhes", "DET-14_abrigo_glp.svg"); sh.save(out); return "detalhes/DET-14_abrigo_glp.svg"

def gas():
    rel = det14_gas()
    rows = [["Base da linha", "tudo elétrico: boiler, cocção por indução (mini cozinha do Casulo: cooktop 2 bocas + forno elétrico), climatização por bomba de calor; nenhum equipamento a gás"], ["Quando usar GLP", "cocção em unidades Ultra Luxury, lareira a gás, boiler a gás em sítios sem rede elétrica robusta"],
            ["Localização", "abrigo externo encostado à cauda (lado técnico), ≥ 1,50 m de aberturas, ≥ 3,00 m da condensadora e de fontes de ignição, nunca sob o deck"], ["Quantidade", "2 x P-45 (boiler + cocção) ou 2 x P-13 (só cocção/lareira); rodízio de um cheio e um em uso"],
            ["Abrigo", "1,00 x 0,60 x 1,20 m, alvenaria leve ou chapa galvanizada, porta veneziana, ventilação permanente inferior e superior, piso nivelado não combustível, cobertura"], ["Tubulação", "cobre rígido Ø1/2\" (ou PEAL) em eletroduto dedicado até o ponto; regulador de 1º estágio no abrigo; registro geral e registro no ponto"],
            ["Equipamentos", "aquecedor de passagem 15 L/min (exaustão forçada, fora do banho) ou cooktop 2 bocas / lareira a gás com sistema de segurança"], ["Norma", f"NBR 13523 (central de GLP), NBR 15526 (rede interna), NBR 13103 (ambientes) · {WARN}"]]
    page(h("10 · GÁS / BOTIJÕES · ALTERNATIVA GLP E ABRIGO-TIPO", "não previsto na base; seção mantida para a opção") + f'<div class="two"><div>{table(["Item", "Definição"], rows, "small")}</div><div>{sheet(rel)}</div></div>', "10 · Gás", code="ZG-GAS-001")

# ============================================================================ 11 climatização
def climatizacao():
    A_env, U_env = bc["memb"], 0.62; A_gl, U_gl, FS = GLASS_M2, 1.6, 0.40; A_fl, U_fl = bc["floor"], 0.45
    vol = A_fl * 2.9; ach = 0.5; vent = vol * ach * 0.34
    dT_s, dT_w = 8, 18; sol = A_gl * FS * 300 * 0.5; intern = 450
    cool = (A_env * U_env + A_gl * U_gl + A_fl * U_fl + vent) * dT_s + sol + intern
    heat = (A_env * U_env + A_gl * U_gl + A_fl * U_fl + vent) * dT_w
    rows = [["Envelope da concha", f"{fmt(A_env)} m² · U 0,62", fmt(A_env * U_env * dT_s, 0), fmt(A_env * U_env * dT_w, 0)], ["Vidros (fachada, Olhos, espinha)", f"{fmt(A_gl)} m² · U 1,6 · FS 0,40", fmt(A_gl * U_gl * dT_s, 0), fmt(A_gl * U_gl * dT_w, 0)],
            ["Piso", f"{fmt(A_fl)} m² · U 0,45", fmt(A_fl * U_fl * dT_s, 0), fmt(A_fl * U_fl * dT_w, 0)], ["Renovação de ar 0,5 vol/h", f"{fmt(vol, 0)} m³", fmt(vent * dT_s, 0), fmt(vent * dT_w, 0)],
            ["Ganho solar pelos vidros (fator 0,5 sombreamento/orientação)", "300 W/m²", fmt(sol, 0), "—"], ["Cargas internas (2 pessoas + equipamentos)", "—", fmt(intern, 0), "—"],
            ["<b>Total estimado</b>", f"verão ΔT {dT_s} K · inverno ΔT {dT_w} K", f"<b>{fmt(cool, 0)} W ≈ {fmt(cool * 3.412 / 1000, 1)} kBTU/h</b>", f"<b>{fmt(heat, 0)} W</b>"]]
    eq = [["Equipamento", "split inverter quente/frio 12.000 BTU/h dutado (evaporadora no ático técnico, difusores lineares no forro, retorno no banho); 18.000 BTU/h em sítios de clima quente ou sem blackout"],
          ["Aquecimento", "bomba de calor (o mesmo split) cobre a carga de inverno estimada; lareira ecológica opcional só como ambiência"], ["Ventilação", "natural: Olhos basculantes + porta + respiro da espinha; mecânica: exaustor do banho 150 m³/h e ventilador da câmara"],
          ["Exaustão", "banho com recuperação de calor opcional (ERV 100 m³/h) em clima frio"], ["Isolamento", "envelope U ≈ 0,62 · vidro U 1,6 · piso U 0,45: a maior perda é o vidro; blackout térmico reduz 30 % no inverno"],
          ["Nota", f"estimativa preliminar de carga térmica, não é dimensionamento · {WARN}"]]
    page(h("11 · CLIMATIZAÇÃO · CARGA TÉRMICA PRELIMINAR E EQUIPAMENTOS", "premissas: serra catarinense, verão ΔT 8 K, inverno ΔT 18 K") + f'<div class="two"><div>{table(["Parcela", "Base", "#Verão W", "#Inverno W"], rows, "small")}{table(["Item", "Definição"], eq, "small")}</div><div>{sheet("detalhes/DET-09_climatizacao.svg")}</div></div>', "11 · Climatização", code="ZC-CLI-001")

# ============================================================================ 12 isolamento
def isolamento():
    tab = [["Envelope da concha", "lã de PET 50 mm, 25 kg/m³ + manta refletiva", "50 + 4 mm", "térmico (R 1,25) e acústico; barreira radiante", f"{fmt(bc['memb'] * 1.08)} m²"], ["Piso interno", "PIR faceado 50 mm", "50 mm", "térmico (R 2,2), estanque ao vapor", f"{fmt(bc['floor'] * 1.05)} m²"],
           ["Parede do banho", "lã de PET 50 mm entre montantes LSF", "50 mm", "acústico entre banho e suíte", "16 m²"], ["Forro", "forro tensionado acústico Trevira CS (NRC 0,6)", "1 mm", "absorção acústica interna", f"{fmt(bc['memb'] * 0.95)} m²"],
           ["Vidros", "insulado 6 + 12 Ar + 6 low-e", "24 mm", "U 1,6 · Rw 34 dB", f"{fmt(GLASS_M2)} m²"], ["Instalações", "tubos AQ isolados em espuma elastomérica 9 mm", "9 mm", "perda térmica da água quente", "18 m"]]
    comp = [["Lã de rocha", "λ 0,035 · incombustível · pesada (40 kg/m³) · irrita na aplicação", "boa opção onde há exigência de incombustibilidade (A1)"], ["Lã de vidro", "λ 0,040 · leve · barata · absorve umidade", "evitar sob membrana (condensação)"],
            ["PIR", "λ 0,022 · rígido · melhor R por espessura · placas planas", "escolhido para o piso (plano, estanque)"], ["EPS", "λ 0,038 · barato · combustível · roedores", "não usar no envelope"], ["XPS", "λ 0,034 · resiste à água · rígido", "alternativa ao PIR no piso e sob o deck"],
            ["Lã de PET reciclada", "λ 0,038 · flexível · não irrita · hidrófuga · reciclada", "escolhida para o envelope curvo: acompanha os arcos, não solta fibras no forro, narrativa sustentável"], ["Barreiras acústicas", "manta viscoelástica 2 mm na parede do banho; forro NRC 0,6", "conforto entre ambientes e chuva na membrana"]]
    page(h("12 · ISOLAMENTO TERMOACÚSTICO", "onde, o quê, quanto e por quê") + f'<div class="two"><div>{table(["Local", "Material", "Espessura", "Função", "Quantidade"], tab, "small")}</div><div>{table(["Material", "Características", "Decisão"], comp, "small")}</div></div>', "12 · Isolamento", code="ZC-ISO-001")

# ============================================================================ 13 materiais · 14 quantitativo · 15 BOM
MAP9 = {"ESTRUTURA": ["01", "02", "03", "04"], "FECHAMENTO": ["05", "06", "07"], "COBERTURA": ["05"], "ESQUADRIAS": ["08", "09"], "ACABAMENTO": ["11", "12", "17", "18"], "HIDRÁULICA": ["13"], "ELÉTRICA": ["14", "15", "16"], "GÁS": [], "EXTERNO": ["10"]}
PERDA = {"01": 3, "02": 5, "03": 5, "04": 5, "05": 0, "06": 8, "07": 5, "08": 0, "09": 0, "10": 10, "11": 8, "12": 5, "13": 5, "14": 5, "15": 0, "16": 0, "17": 0, "18": 10}
def groups(): return P.bom_priced(PIL)

def materiais():
    G = groups(); by = {g[:2]: (g, items) for g, items in G}
    out = ""
    for k, codes in MAP9.items():
        rows = []
        for c in codes:
            if c in by:
                g, items = by[c]
                rows += [[f"{c} · {g[3:]}", d, u, qq] for (d, u, qq, key) in items]
        if k == "GÁS": rows = [["—", "não previsto na base (ver seção 10)", "—", "—"]]
        if k == "EXTERNO": rows += [["FF&E deck", "espreguiçadeiras, mesa e cadeiras, balizadores, ducha externa (lista ffe.py)", "cj", 1]]
        out += f"<h4>{k}</h4>" + table(["Grupo do kit", "Material", "Un.", "#Qtd"], rows, "xsmall")
    page(h("13 · MATERIAL TAKEOFF · ZION CASULO", "9 grupos do método sobre os 18 grupos do kit de fábrica · quantidades estimadas pela geometria, sem preços") + f'<div class="cols2">{out}</div>', "13 · Material takeoff", cls="flow", code="ZC-MAT-001")

def quantitativo():
    rows = []; i = 0
    for g, items in groups():
        c = g[:2]; p = PERDA[c]
        for (d, u, qq, key) in items:
            i += 1; qf = qq * (1 + p / 100) if isinstance(qq, (int, float)) else qq
            rows.append([f"ZC-QTD-{i:03d}", d, g[3:], u, qq, f"{p} %" if p else "—", round(qf, 1) if isinstance(qf, float) else qf])
    page(h("14 · QUANTITATIVO MESTRE · ZION CASULO", "perda aplicada só onde é tecnicamente justificável (corte, emendas, quebra); membrana já inclui 15 % de emendas e bolsas") + table(["Código", "Item", "Especificação / grupo", "Un.", "#Qtd", "Perda", "#Qtd final"], rows, "small"), "14 · Quantitativo", cls="flow", code="ZC-QTD-001")

def bom_page():
    parts = P.cocoon_parts()
    def forn(fab):
        f = fab.lower()
        if "calandr" in f: return "serralheria com calandra de tubos + galvanizador"
        if "corte" in f and "fur" in f: return "perfiladora / serralheria"
        if "chapa" in f or "dobra" in f: return "caldeiraria leve (corte laser + dobra)"
        if "usin" in f or "rosca" in f: return "usinagem"
        return "serralheria + galvanizador"
    rows = [[f"ZC-BOM-{p['cod']}", p["nome"], p["aco"], f"{p['perfil']} · L {p['comp']} m", p["esp"], p["qtd"], p["fab"], forn(p["fab"]), p["uniao"]] for p in parts]
    page(h("15 · BOM · BILL OF MATERIALS · ESTRUTURA DO ZION CASULO", "código, descrição, material, dimensão, espessura, quantidade, processo, fornecedor potencial, observação") + table(["Código", "Descrição", "Material", "Dimensão", "#Esp. mm", "#Qtd", "Processo", "Fornecedor potencial", "Observação"], rows, "small"), "15 · BOM estrutura", cls="flow", code="ZC-BOM-001")
    rows2 = []
    for g, items in groups():
        if g[:2] in ("01", "02", "03", "04"): continue
        for (d, u, qq, key) in items: rows2.append([f"ZC-BOM-{g[:2]}-{key.upper()[:8]}", d, g[3:], u, qq, "cotar com fornecedor do grupo"])
    page(h("15 · BOM · ENVELOPE, ESQUADRIAS, PISO, DECK, INSTALAÇÕES E INTERIORES", "itens de compra por grupo do kit (materiais, não peças fabricadas)") + table(["Código", "Descrição", "Grupo", "Un.", "#Qtd", "Fornecedor potencial"], rows2, "small"), "15 · BOM materiais", cls="flow", code="ZC-BOM-002")

# ============================================================================ 16 pré-fabricação
def prefab():
    mods = [["Módulos de piso 1,20 x 2,40", 18, "vigotas + PIR + compensado + fechamento inferior, pré-montados e numerados", "içamento manual (2 pessoas), parafusos M12 nas vigas"],
            ["Módulos de deck 1,20 x 2,40", 15, "vigotas + réguas de cumaru com clips", "idem"], ["Arcos em 3 segmentos", 7, "calandrados, galvanizados, com luvas Ø76 e furos gabaritados", "coroa + 2 pernas unidas em campo com 4 M12 por luva"],
            ["Anel frontal A0", 1, "calandrado inteiro (Ø101,6, 10,8 m) ou em 2 segmentos para contêiner", "chapas de base gabaritadas"], ["Painéis de membrana", 7, "cortados e soldados em fábrica com keder e bolsas; numerados cauda → frente", "deslizados nos perfis keder"],
            ["Painéis de forro tensionado", 7, "confeccionados sob medida", "tensionados no trilho"], ["Cavaletes de vidro", 4, "fachada (8 painéis), 6 Olhos com requadro colado, 4 vidros da espinha", "instalação com ventosas"],
            ["Parede do banho em LSF", 1, "painel pronto com passagem de instalações", "parafusada ao piso e ao arco B6"], ["Kit hidráulico", 1, "PEX cortado e etiquetado, coletor, boiler, louças e metais em caixa", "conexões rápidas"],
            ["Kit elétrico", 1, "QDC montado e testado, chicotes etiquetados por circuito, fitas LED em rolos cortados", "plug-and-play nos rodapés"], ["Marcenaria", 1, "ilha do café, closet, bancada, cabeceira: montadas e acabadas em fábrica", "nivelamento e fixação"]]
    body = h("16 · PEÇAS PRÉ-FABRICADAS E ESTRATÉGIA DE PRÉ-FABRICAÇÃO MÁXIMA", "FABRICAÇÃO NA FÁBRICA → TRANSPORTE → MONTAGEM NO TERRENO → COMISSIONAMENTO") + table(["Módulo / kit", "#Un.", "O que vem pronto da fábrica", "O que se faz em campo"], mods, "small") + \
        '<div class="flowchart"><span>FÁBRICA · 6 semanas (1ª unidade) · serralheria, membrana, vidros, marcenaria, kits</span><i></i><span>TRANSPORTE · 1 contêiner 40\' HC · 9 volumes · 8,6 t</span><i></i><span>MONTAGEM · 12 dias · 4 montadores + líder · sem solda, sem concreto</span><i></i><span>COMISSIONAMENTO · 1 dia · estanqueidade, elétrica, climatização, limpeza</span></div>' + \
        f'<p class="note">Peças repetitivas entre unidades da linha: estacas e cabeçotes, vigas U 150, módulos de piso e deck, perfis keder, kits hidráulico e elétrico, esquadrias de alumínio RPT, marcenaria da ilha do café. Cronograma de fábrica: {"; ".join(f"{t} ({a}–{a + d} sem.)" for t, a, d in P.FAB_SCHEDULE[PIL])}.</p>'
    page(body, "16 · Pré-fabricação", code="ZC-FAB-001")

# ============================================================================ 17 manual 15 etapas · 18 ferramentas
STAGES = [("01", "Preparação do terreno", [1]), ("02", "Fundação", [2]), ("03", "Base (grelha de vigas)", [3]), ("04", "Estrutura (arcos, travamentos, esquadro)", [5, 6, 7]), ("05", "Piso (módulos)", [4]), ("06", "Paredes (isolamento e forro internos)", [9, 10]), ("07", "Cobertura (membrana externa)", [8]),
          ("08", "Esquadrias", [11]), ("09", "Instalações", [12, 13]), ("10", "Revestimentos", [16]), ("11", "Deck", [4]), ("12", "Equipamentos (banho, climatização)", [14]), ("13", "Mobiliário", [15]), ("14", "Testes", [17]), ("15", "Entrega", [17])]
COMO = {"01": "Locação com estação total a partir de 2 referências fixas; roçada seletiva; delimitação do estoque e do acesso do caminhão.", "02": "Cravação das 44 estacas com motor hidráulico, torque registrado por estaca; cabeçotes nivelados a ± 5 mm.",
        "03": "Vigas U 150 parafusadas aos cabeçotes (M12), esquadro pelas diagonais, travamento das vigas de borda.", "04": "Trilhos de base fixados; arcos montados no chão (pernas + coroa com luvas), içados com guincho manual da cauda para a frente, travados provisoriamente; anel A0 por último; terças rosqueadas; espinha; cabos em X a 2 kN; conferência de geometria com gabarito.",
        "05": "18 módulos de piso içados e parafusados às vigas; passagens de PEX e esgoto pelos furos gabaritados.", "06": "Mantas de PET e refletiva presas às terças; trilhos do forro; 7 painéis de forro tensionados; painéis ripados.", "07": "Painéis de membrana deslizados nos perfis keder (cauda → frente), bolsas de base tensionadas com esticadores, tampas de frente e cauda, flanges das Janelas Olho.",
        "08": "Anel de alumínio no A0; 8 vidros da fachada e porta pivotante; 6 Janelas Olho; 4 vidros da espinha com selagem.", "09": "QDC, chicotes e fitas LED; PEX, esgoto, boiler; evaporadora, dutos e condensadora.", "10": "Piso de carvalho, porcelanato e impermeabilização do banho, pintura e selantes.",
        "11": "15 módulos de deck e escada de 3 degraus; réguas com clips; óleo protetor.", "12": "Louças, metais, banheira, box; climatização; fechadura digital; automação.", "13": "Ilha do café, closet, bancada, cabeceira, cama, chaise, luminárias, cortinas, enxoval.",
        "14": "Teste de lâmina do banho 72 h; teste de estanqueidade PEX 10 bar; teste de isolamento e DR; balanceamento da climatização; simulação de chuva na membrana.", "15": "Limpeza fina, checklist de entrega assinado, manual do hóspede e do operador, registro fotográfico e as-built."}
MATS = {"01": "estacas de madeira, tinta, linha", "02": "estacas helicoidais, cabeçotes, contraporcas", "03": "vigas U 150, cantoneiras, M12", "04": "arcos, anel A0, trilhos, luvas, terças, espinha, cabos, chapas, parafusos 8.8", "05": "módulos de piso, M12", "06": "lã de PET, manta refletiva, trilho e painéis de forro, ripados",
        "07": "painéis de membrana, esticadores, selante PU", "08": "anel de alumínio, montantes, vidros, porta, Olhos, EPDM, silicone", "09": "QDC, cabos, eletrodutos, PEX, conexões, boiler, evaporadora, condensadora, dutos", "10": "carvalho, porcelanato, AC-III, manta líquida, rejunte, tintas", "11": "módulos de deck, escada, clips, óleo",
        "12": "louças, metais, banheira, box, fechadura, hub", "13": "FF&E (45 itens)", "14": "manômetro, multímetro, termômetro", "15": "kit de limpeza, documentação"}

def manual():
    man = {m["n"]: m for m in P.manual(PIL)}
    def hours(ids):
        t = 0.0
        for i in ids:
            s = man[i]["tempo"].replace("h", "").strip()
            try: t += float(s.replace(",", "."))
            except Exception: pass
        return t
    blocks = []
    for (code, title, ids) in STAGES:
        ms = [man[i] for i in ids]
        ferr = sorted({x.strip() for m in ms for x in (m["ferramentas"] + ", " + m["equipamentos"]).split(",") if x.strip()})
        chk = [c for m in ms for c in m["checklist"]]
        risc = " · ".join(m["riscos"] for m in ms)
        eq = " / ".join(sorted({m["equipe"] for m in ms}))
        tempo = f"{hours(ids):g} h" if hours(ids) else " + ".join(m["tempo"] for m in ms)
        chk_html = "".join(f"<li>☐ {esc(c)}</li>" for c in chk)
        blocks.append((code, f'<div class="stage"><h3>ETAPA {code} · {esc(title.upper())}</h3><p class="stsub">passos {", ".join(f"{i:02d}" for i in ids)} do manual em 17 passos do Product Book</p>'
                       f'<dl class="kv"><dt>O que fazer</dt><dd>{esc(" · ".join(m["titulo"] for m in ms))}</dd><dt>Como fazer</dt><dd>{esc(COMO[code])}</dd><dt>Materiais</dt><dd>{esc(MATS[code])}</dd><dt>Ferramentas</dt><dd>{esc(", ".join(ferr))}</dd><dt>Equipe</dt><dd>{esc(eq)}</dd><dt>Tempo estimado</dt><dd>{esc(tempo)}</dd><dt>Cuidados</dt><dd>{esc(risc)}</dd></dl>'
                       f'<h4>CHECKLIST DE CONCLUSÃO</h4><ul class="chk">{chk_html}</ul></div>'))
    for i in range(0, len(blocks), 2):
        pair = blocks[i:i + 2]; codes = " · ".join(c for c, _ in pair)
        page(h(f"17 · MANUAL DE MONTAGEM · ETAPAS {codes}", "o que fazer · como fazer · materiais · ferramentas · equipe · tempo · cuidados · checklist") + f'<div class="two">{"".join(b for _, b in pair)}</div>', f"17 · Montagem · etapas {codes}", code=f"ZC-MONT-{pair[0][0]}")

def ferramentas():
    fab = ["Calandra de tubos CNC (3 rolos) com gabaritos por arco", "Serra de fita / disco de corte para tubos e perfis", "Furadeira de coluna e gabaritos de furação", "Solda MIG/TIG (só em fábrica: luvas, chapas de base, olhais)", "Bancada de montagem de arcos com gabarito de raio", "Máquina de solda HF para membrana e mesa de corte", "Prensa de keder", "Ventosas e cavaletes para vidro", "Bancada de marcenaria (CNC, coladeira de borda)", "Pintura a pó (terceirizada) e galvanização a fogo (terceirizada)", "Instrumentos: trena laser, paquímetro, torquímetro, esquadro de 1 m"]
    tr = ["Empilhadeira 2,5 t e talha 2 t (carregamento)", "Cintas, catracas e cantoneiras de proteção", "Estrados e paletes reforçados, plástico-bolha, filme stretch", "Contêiner 40' HC ou carreta com sider", "Guindaste tipo munck 12 t (descarga no sítio)", "Etiquetas de volume e lista de embarque (packing list)"]
    obra = sorted({x.strip() for m in P.manual(PIL) for x in (m["ferramentas"] + ", " + m["equipamentos"]).split(",") if x.strip()})
    epi = ["Capacete, óculos, luvas de vaqueta e nitrílica", "Botas de segurança", "Cinto de segurança tipo paraquedista e talabarte (trabalho > 2 m nos arcos)", "Protetor auricular (motor de cravação, serra)", "Máscara PFF2 (lã, PU, tintas)", "Protetor solar e hidratação; ponto de apoio com primeiros socorros", "Sinalização de área e extintor no canteiro"]
    blocks = ""
    for k, v in (("FÁBRICA", fab), ("TRANSPORTE", tr), ("OBRA", obra), ("EPIs", epi)):
        items = "".join(f"<li>{esc(x)}</li>" for x in v); blocks += f"<div><h4>{k}</h4><ul class=chk>{items}</ul></div>"
    body = h("18 · FERRAMENTAS E EQUIPAMENTOS", "fábrica · transporte · obra · EPIs") + f'<div class="cols3">{blocks}</div>'
    page(body, "18 · Ferramentas", code="ZC-MONT-016")

# ============================================================================ 19 logística
def logistica():
    rows = [[i + 1, d, dim, v, kg] for i, (d, dim, v, kg) in enumerate(tc["items"])]
    rows.append(["", "<b>Total</b>", "1 contêiner 40' HC (76 m³ · 26 t)", tc["vol"], tc["kg"]])
    pack = [["Peso total estimado", f"{fmt(tc['kg'], 0)} kg (kit completo, sem FF&E solto)"], ["Volume", f"{fmt(tc['vol'])} m³ em 9 volumes; ocupação de 67 % do contêiner (sobra para FF&E)"], ["Dimensões máximas", "estrado 2,4 x 1,2 x 1,2 m; cavaletes de vidro 2,2 x 0,6 x 2,4 m; anel A0 em 2 segmentos ≤ 5,6 m"],
            ["Centro de gravidade", "estrados de estrutura: centrado; cavaletes de vidro: alto (amarrar em pé, nunca deitar); paletes de piso: centrado"], ["Pontos de içamento", "estrados: garfos de empilhadeira; arcos: 2 olhais por segmento (M16) e cintas; módulos de piso/deck: manual, 2 pessoas"],
            ["Pontos de fixação", "cintas de 2 t com catraca em 4 pontos por volume; cantoneiras de proteção nos tubos galvanizados"], ["Transporte rodoviário", "carreta 14 m ou contêiner; largura ≤ 2,60 m: sem AET (só a Cápsula exige AET)"],
            ["Acesso ao terreno", "via ≥ 3,5 m de largura, raio de curva ≥ 12 m, ponte ≥ 20 t; descarga com munck 12 t ou empilhadeira 4x4; estoque coberto de 60 m²"], ["Sequência de descarga", "9 estacas → 1-3 estrados de estrutura → 6 paletes de piso → 7 deck → 4 membrana → 5 vidros → 8 instalações (ordem inversa de uso, os vidros por último e protegidos)"]]
    page(h("19 · LOGÍSTICA · TRANSPORTATION PACK · ZION CASULO", "dimensões, pesos, içamento, fixação e sequência") + f'<div class="two"><div>{table(["#", "Volume", "Dimensões", "#m³", "#kg"], rows, "small")}</div><div>{table(["Item", "Definição"], pack, "small")}</div></div>', "19 · Logística", code="ZC-LOG-001")

# ============================================================================ 20 orçamento 18 grupos
def orcamento():
    G = [("01", "Fundação", "44 estacas + cabeçotes + cravação"), ("02", "Estrutura", "kit metálico galvanizado (grupos 01 a 04 do kit)"), ("03", "Piso", "módulos de piso, PIR, compensado, carvalho"), ("04", "Paredes", "envelope: membrana, isolamento, forro, ripados; parede do banho"),
         ("05", "Cobertura", "incluída no envelope; calha oculta, TQ, drenagem"), ("06", "Esquadrias", "vidros, anel de alumínio, porta, Olhos, espinha"), ("07", "Instalações", "kits hidráulico e elétrico, QDC, boiler"), ("08", "Banheiro", "louças, metais, banheira, porcelanato, impermeabilização"),
         ("09", "Climatização", "split dutado, dutos, difusores, exaustor"), ("10", "Deck", "módulos de deck, escada, óleo"), ("11", "Jacuzzi / piscina", "hot tub opcional (D06 / E07)"), ("12", "Mobiliário", "FF&E Zion New Luxury (45 itens)"), ("13", "Iluminação", "fitas LED, arandelas, luminárias, balizadores"),
         ("14", "Automação", "hub, fechadura, sensores, motorizações"), ("15", "Transporte", "embalagem + contêiner / carreta + munck"), ("16", "Montagem", "12 dias, 4 montadores + líder + especialistas (membrana, vidro, elétrica)"), ("17", "Engenharia", "projeto executivo, cálculo, form-finding, ART/RRT, acompanhamento"), ("18", "Contingência", "10 % sobre 01 a 17 na 1ª unidade")]
    rows = [[c, n, d, COTAR] for c, n, d in G]
    page(h("20 · ORÇAMENTO · ESTRUTURA EM 18 GRUPOS", "sem preços neste documento; estimativa interna em 3 cenários no arquivo interno/ · cotações reais via RFQ") + table(["#", "Grupo", "O que inclui (mapa para o kit e o FF&E)", "Preço"], rows, "small") +
         '<p class="note">Regra: nenhum preço de mercado é apresentado como cotação. A estimativa paramétrica interna (Econômico / Zion Standard / Zion Premium, 1ª e 10ª unidade) está em interno/ZION_ORCAMENTO_SC_Casulo_Safari_Lodge.xlsx e não faz parte deste documento. Cada grupo recebe preço real após as respostas ao RFQ ZG-RFQ-001.</p>', "20 · Orçamento (estrutura)", code="ZC-ORC-001")

# ============================================================================ 21 checklist de obra · 22 RFQ · 23 validação
def checklist_obra():
    rows = [[f"{m['n']:02d}", m["titulo"], "<br>".join(f"☐ {esc(c)}" for c in m["checklist"]), m["tempo"]] for m in P.manual(PIL)]
    page(h("21 · CHECKLIST DE OBRA · 17 PASSOS", "conclusão de cada passo assinada pelo líder de montagem e pelo engenheiro responsável") + table(["#", "Passo", "Itens de verificação", "Tempo"], rows, "small"), "21 · Checklist de obra", cls="flow", code="ZC-CHK-001")

def rfq():
    cont = ["Apresentação do produto", "Conceito", "Dimensões", "Área", "Sistema construtivo desejado", "Materiais", "Desenhos (PA-00 a PA-12, DXF)", "Componentes (BOM)", "Quantidades", "Acabamentos", "Instalações", "Transporte", "Montagem", "Prazo de fabricação", "Garantia", "Capacidade produtiva", "Certificações", "Experiência da fábrica"]
    perg = ["Vocês conseguem fabricar este projeto?", "Qual parte conseguem fabricar internamente?", "Quais componentes terceirizam?", "Qual material recomendam?", "Conseguem fabricar os módulos?", "Conseguem fabricar a estrutura?", "Conseguem entregar acabada?", "Conseguem transportar?", "Conseguem montar?", "Qual capacidade mensal?", "Qual prazo de produção?", "Qual MOQ?", "Qual garantia?", "Qual preço EX WORKS?", "Qual preço entregue?", "Qual preço instalado?", "Qual condição de pagamento?", "Qual prazo de validade da proposta?"]
    page(h("22 · RFQ · REQUEST FOR MANUFACTURING QUOTATION (ANEXO)", "documento separado ZG-RFQ-001 na Fase 10; aqui, o conteúdo e as perguntas") + f'<div class="two"><div><h4>CONTEÚDO DO RFQ</h4><ol class="num">{"".join(f"<li>{esc(c)}</li>" for c in cont)}</ol><p class="note">Resposta esperada da fábrica: SIM, FABRICAMOS · NÃO FABRICAMOS · FABRICAMOS COM ALTERAÇÕES. Comparação posterior: Fábrica × Fabrica × Estrutura × Acabamento × Transporte × Montagem × Prazo × Preço, sem escolha automática.</p></div><div><h4>PERGUNTAS PARA A FÁBRICA</h4><ol class="num">{"".join(f"<li>{esc(c)}</li>" for c in perg)}</ol></div></div>', "22 · RFQ (anexo)", code="ZG-RFQ-000")

def validacao():
    items = [("Estrutura", "cálculo dos arcos, anel, terças, cabos e ligações (NBR 8800 / NBR 6123, V0 = 45 m/s); form-finding e pré-tensão da membrana com o fabricante; ART"), ("Fundação", "sondagem SPT ou ensaio de torque; comprimento e quantidade das estacas; arrancamento por vento"),
             ("Vidros", "espessuras e laminação do anel inclinado e da Espinha de Luz (NBR 7199); silicone estrutural"), ("Hidráulica", "diâmetros, pressão, reservatório, tratamento de esgoto (NBR 5626 / NBR 7229 / NBR 13969); licenciamento ambiental"),
             ("Elétrica", "cargas, condutores, proteções, aterramento, DPS (NBR 5410); solar (NBR 16690); ART"), ("Gás (se adotado)", "central de GLP e rede (NBR 13523 / 15526 / 13103)"), ("Climatização", "carga térmica definitiva e dutos (ABNT NBR 16401)"),
             ("Incêndio e acessibilidade", "exigências do corpo de bombeiros e NBR 9050 conforme o uso e o município"), ("Membrana e isolamento", "classe de reação ao fogo (B1 / M1) com laudo"), ("Legal", "projeto legal, aprovação municipal, licenciamento ambiental (APP, supressão), RRT de arquitetura")]
    page(h("23 · CHECKLIST DE VALIDAÇÃO DE ENGENHARIA", "tudo o que este documento marca como ⚠️ e que precisa de profissional habilitado antes da fabricação") + table(["Disciplina", "O que validar"], [[f"☐ {a}", b] for a, b in items], "small") +
         f'<p class="lede">{WARN}: este documento é um projeto técnico preliminar / executivo conceitual para desenvolvimento e orçamento. Não substitui ART, RRT, cálculo estrutural, projeto legal ou aprovação municipal.</p>', "23 · Validação de engenharia", code="ZG-VAL-001")

# ============================================================================ 24 resumo da linha
def linha():
    cm = capsule_materials(); ck = next((it[2] for g, items in cm for it in items if it[3] == "steel_kg"), 0)
    rows = [["ZION CASULO", "9,60 x 6,00 x 4,20", 48.0, 29.9, "8 arcos elípticos + anel A0", 44, bc["steel_kg"], round(bc["memb"]), round(GLASS_M2, 1), bc["total"], "1 x 40' HC", 12, "projeto + engenharia peça a peça"],
            ["ZION SAFARI", "9,50 x 5,40 · cob. 12,90 x 7,40", 48.4, 28.0, "2 mastros + 10 pilares + 7 postes", 37, bz["steel_kg"], round(bz["roof_s"] + bz["roof_p"]), "—", bz["total"], "1 x 40' HC", 15, "projeto + engenharia peça a peça"],
            ["ZION LODGE 38", "octógono 6,80 · lanterna 5,20", round(LG["lodge"].floor_area(), 1), round(LG["lodge"].deck_area(), 1), "8 pilares + 8 caibros + anel", 22, bl["steel_kg"], round(bl["memb"]), "—", bl["total"], "1 x 40' HC", 9, "projeto + engenharia peça a peça"],
            ["ZION LODGE 24", "octógono 5,40 · lanterna 4,70", round(LG["lodge24"].floor_area(), 1), round(LG["lodge24"].deck_area(), 1), "8 pilares + 8 caibros", 15, "≈ 1.100 (param.)", "≈ 75", "—", "≈ 4.500", "1 x 40' HC", 6, "conceito"],
            ["ZION LODGE 28", "4,20 x 7,80 · lanternas 4,45", round(LG["lodge28"].floor_area(), 1), round(LG["lodge28"].deck_area(), 1), "8 pilares + 10 caibros", 21, "≈ 1.400 (param.)", "≈ 95", "—", "≈ 5.500", "1 x 40' HC", 8, "conceito"],
            ["ZION CÁPSULA", "8,40 x 3,20 x 3,20", round(CAP.floor_area(), 1), round(CAP.deck_area(), 1), "12 anéis + 7 longarinas + chassi", 8, ck, "casca ACM 84 m²", round(CAP.shell_area("visor") + CAP.shell_area("ring"), 1), "≈ 4.800", "carreta (AET)", 1, "conceito + materiais"]]
    page(h("24 · RESUMO TÉCNICO DA LINHA", "os mesmos sistemas comuns; números do piloto calculados, os das unidades em conceito são paramétricos") + table(["Unidade", "Dimensões (m)", "#Int. m²", "#Ext. m²", "Estrutura", "#Estacas", "#Aço kg", "#Membrana m²", "#Vidro m²", "#Peso kg", "Transporte", "#Dias", "Estágio"], rows, "small") +
         table(["Sistema comum", "Especificação da linha"], [[t, d] for t, d in [("Estrutura", "aço ASTM A500 galvanizado a fogo, kit parafusado 8.8, sem solda em campo"), ("Fundação", "estacas helicoidais Ø76 + cabeçotes ajustáveis; deck e piso em vigas U 150"), ("Envelope", "membrana PVDF 1050 g/m² (B1) + câmara ventilada 60 mm + lã de PET 50 mm + forro tensionado M1 (Cápsula: ACM 4 mm + PIR 60 mm + compensado curvado)"),
                                                                                  ("Vidros", "insulado 6 lam + 12 Ar + 6 temp low-e, alumínio bronze RPT (Cápsula: laminado curvo 8+8)"), ("Piso e deck", "carvalho de engenharia 14 mm, porcelanato no banho, deck de cumaru 20 x 140"), ("Instalações", "PEX Ø25/20/16, esgoto Ø100, QDC 12 a 16 circuitos, split inverter dutado, boiler elétrico"), ("FF&E", "catálogo de 56 itens Zion New Luxury; listas por unidade em ffe.py")]], "small"), "24 · Resumo da linha", code="ZG-TEC-024")

# ============================================================================ 25 interiores (anexo ZC-INT-001)
def interiores():
    from interiores_cocoon import MA, MS
    rows = [[f"<b>{m['cod']}</b>", m["nome"], m["amb"], m["ffe"], m["mat"]] for m in MA]
    page(h("25 · INTERIORES · MARCENARIA ACOPLADA (ANEXO ZC-INT-001)", "mobiliário fixo fabricado com a cabana · pranchas IN-01 a IN-06 nas páginas seguintes; documento completo em 04_INTERIORES") +
         f'<div class="two"><div>{table(["Cód.", "Peça acoplada", "Ambiente", "FF&E", "Materiais"], rows, "small")}<p class="note">Regras: fixação só à estrutura (arcos e trilhos), fundos recortados pelo gabarito da seção, rodapé técnico removível, elétrica embutida, peças ≤ 1,40 m para o contêiner e a porta PV1. Mobiliário solto (MS-01 a MS-09) é FF&amp;E.</p></div><div>{sheet("cocoon/interiores/IN-01_planta_interiores.svg")}</div></div>', "25 · Interiores (anexo)", code="ZC-INT-001")
    for code, t, sc, rel in (("IN-02", "Paginação de pisos e acabamentos", "1:50", "cocoon/interiores/IN-02_pisos_acabamentos.svg"), ("IN-03", "Elevações internas A e B", "1:40", "cocoon/interiores/IN-03_elevacoes_A_B.svg"), ("IN-04", "Elevações internas C e D", "1:40", "cocoon/interiores/IN-04_elevacoes_C_D.svg"), ("IN-05", "Detalhes da marcenaria acoplada", "1:20 / 1:15", "cocoon/interiores/IN-05_detalhes_marcenaria.svg"), ("IN-06", "Quadro de mobiliário e marcenaria", "s/ escala", "cocoon/interiores/IN-06_quadro_mobiliario.svg")):
        sheet_page(rel, f"ZC-INT · {code}", t, sc, "ZION CASULO")

# ============================================================================ CSS e build
CSS = """
@font-face{font-family:'Aventa';src:url(../assets/aventa.woff2) format('woff2');font-weight:100 900;font-display:swap}
:root{--cream:#FEF5F0;--ink:#1B2117;--earth:#8B714E;--sand:#DED6BF;--black:#040605}
*{box-sizing:border-box} body{margin:0;background:#E9E2D6;font-family:'Aventa','DM Sans',Helvetica,Arial,sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{position:relative;width:297mm;min-height:210mm;margin:0 auto 8mm;background:var(--cream);padding:11mm 13mm 14mm;page-break-after:always;break-after:page;overflow:hidden}
.page.cover{background:var(--black);color:var(--cream);height:210mm;padding:0} .coverbox{position:absolute;inset:0;padding:22mm 26mm;display:flex;flex-direction:column;justify-content:center}
.brand{font-size:44px;font-weight:800;letter-spacing:.4em;display:flex;align-items:center} .sub{font-size:9px;letter-spacing:.3em;color:var(--sand);margin:6px 0 22mm}
.cover h1{font-size:46px;font-weight:200;letter-spacing:.22em;line-height:1.05;margin:0 0 10px} .cover h3{font-size:12px;letter-spacing:.3em;font-weight:300;color:var(--sand);margin:0 0 16px} .cover .lead{font-size:12px;line-height:1.8;font-weight:300;max-width:200mm;margin:0 0 14px} .cover .rule{font-size:9.5px;line-height:1.7;color:var(--sand);max-width:220mm;border-top:1px solid var(--sand);padding-top:10px}
.cover .warn{color:#FEF5F0;border:1px solid var(--sand);padding:1px 6px;font-size:8.5px;letter-spacing:.08em} .cover .cotar{color:#FEF5F0;border:1px solid var(--sand);padding:1px 6px;font-size:8.5px;letter-spacing:.1em}
.head{display:flex;justify-content:space-between;font-size:7.5px;letter-spacing:.22em;color:var(--earth);border-bottom:1px solid var(--sand);padding-bottom:4px;margin-bottom:8px;text-transform:uppercase} .head span:first-child{display:flex;align-items:center;gap:6px}
.foot{position:absolute;left:13mm;right:13mm;bottom:5mm;display:flex;justify-content:space-between;font-size:7px;letter-spacing:.2em;color:var(--earth)} .foot span:nth-child(2){flex:1;text-align:center}
h2{margin:0 0 8px;font-weight:300;font-size:16px;letter-spacing:.26em;text-transform:uppercase;line-height:1.15} h2 small{display:block;font-size:8.5px;letter-spacing:.14em;color:var(--earth);margin-top:4px;text-transform:none;font-weight:300}
h4{margin:10px 0 4px;font-size:8.5px;letter-spacing:.26em;color:var(--earth);font-weight:600} .lede{font-size:10px;line-height:1.7;margin:8px 0} .note{font-size:8.5px;line-height:1.6;color:var(--earth);margin:8px 0 0}
.warn{background:var(--ink);color:var(--cream);padding:1px 6px;font-size:7.5px;letter-spacing:.08em;white-space:nowrap} .cotar{border:1px solid var(--ink);padding:1px 6px;font-size:7.5px;letter-spacing:.12em;white-space:nowrap}
table.t{border-collapse:collapse;width:100%;font-size:9px;line-height:1.4;margin:4px 0 8px} table.t th{text-align:left;font-weight:600;font-size:7.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--earth);padding:3px 5px;border-bottom:1px solid var(--ink)} table.t td{padding:3px 5px;border-bottom:1px solid var(--sand);vertical-align:top} .num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
table.t.small{font-size:8.2px} table.t.small td{padding:2.5px 4px} table.t.xsmall{font-size:7.2px;line-height:1.3} table.t.xsmall td{padding:2px 3px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start} .cols3{columns:3;column-gap:16px} .cols2{columns:2;column-gap:18px} .cols2 h4,.cols3 h4{margin-top:4px;break-after:avoid} .cols2 table,.cols3 table{break-inside:auto}
.page.flow{height:auto;min-height:210mm;overflow:visible} .page.flow .foot{position:static;margin-top:10mm} table.t tr{page-break-inside:avoid} table.t th{page-break-after:avoid}
.stage h3{margin:0 0 2px;font-size:11px;letter-spacing:.22em;font-weight:600} .stsub{font-size:8px;color:var(--earth);margin:0 0 8px;letter-spacing:.08em}
.sheet{background:#FEF5F0;border:1px solid var(--sand);line-height:0} .sheet svg{width:100%;height:auto;display:block} .missing{padding:20px;font-size:10px}
.sheetpage{padding:8mm 10mm 12mm} .sheetpage .sheet{border:1px solid var(--ink)} .strip{display:flex;gap:16px;align-items:baseline;font-size:8px;letter-spacing:.2em;color:var(--earth);text-transform:uppercase;margin-bottom:5px} .strip .code{font-weight:700;color:var(--ink)} .strip .ttl{flex:1;color:var(--ink)}
.kv{display:grid;grid-template-columns:96px 1fr;gap:5px 10px;margin:0;font-size:9.5px;line-height:1.55} .kv dt{color:var(--earth);letter-spacing:.16em;font-size:7.5px;text-transform:uppercase;padding-top:3px} .kv dd{margin:0}
ul.chk{margin:0;padding:0;list-style:none;font-size:9px;line-height:1.55} ul.chk li{padding:2px 0;border-bottom:1px solid var(--sand)} ol.num{margin:0;padding-left:16px;font-size:9.5px;line-height:1.7}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:10px} .stats div{border-top:1px solid var(--ink);padding-top:6px} .stats b{display:block;font-size:24px;font-weight:200;letter-spacing:.04em} .stats span{font-size:7.5px;letter-spacing:.18em;color:var(--earth);text-transform:uppercase}
.flowchart{display:flex;align-items:center;gap:10px;margin:12px 0;font-size:8.5px;letter-spacing:.06em;line-height:1.5} .flowchart span{border:1px solid var(--ink);padding:8px 10px;flex:1} .flowchart i{width:22px;height:1px;background:var(--ink)}
.tw table{font-size:8px}
@media print{@page{size:A4 landscape;margin:0} body{background:#fff} .page{margin:0;height:210mm} .page.flow{height:auto}}
"""

def build():
    global pages
    capa(); pages.append(None)   # reserva o índice
    ficha_html = ficha(); page(ficha_html, "01 · Ficha técnica", code="ZG-TEC-001")
    desenhos(); exploded(); camadas(); estrutura(); fundacao(); cobertura(); hidraulica(); eletrica(); gas(); climatizacao(); isolamento(); materiais(); quantitativo(); bom_page(); prefab(); manual(); ferramentas(); logistica(); orcamento(); checklist_obra(); rfq(); validacao(); interiores(); linha()
    idx = f'<section class="page flow"><div class="head"><span>ZION GLAMPING · {DOC} · {REV}</span><span>ZG-TEC-000</span><span>ÍNDICE</span></div>{indice()}<div class="foot"><span>ZION GLAMPING COLLECTION · DOCUMENTO TÉCNICO · SEM PREÇOS</span><span></span><span>{DATE} · 02</span></div></section>'
    pages[1] = idx
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · {DOC} · Documento Técnico</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    open(OUT, "w", encoding="utf-8").write(doc); print(OUT, len(pages), "páginas", round(os.path.getsize(OUT) / 1e6, 1), "MB")

if __name__ == "__main__":
    build()

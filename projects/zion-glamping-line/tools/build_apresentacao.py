# -*- coding: utf-8 -*-
"""Apresentação (deck 16:9) do PROJETO ARQUITETÔNICO ZION CASULO & ZION SAFARI no padrão de decks Zion Hotel Group
(fundo preto, texto creme, Aventa, palavras em CAPS espaçadas). Gera ZION_PROJETO_ARQUITETONICO_Apresentacao.html;
o PDF sai com export_pdf.js (uma página 1600 x 900 px por slide).
Uso: python3 build_apresentacao.py"""
import os, html
from svgkit import zion_mark_html, zion_logo_html
from build_projeto_arquitetonico import svg_inline
from product_book_data import budget, cocoon_parts, zenith_parts, COCOON_CONNECTIONS, ZENITH_CONNECTIONS
from bom import cocoon_bom, zenith_bom, transport, ASSEMBLY
from pa_sheets import AREAS, ESQUADRIAS
import bom as _bom, product_book_data as _pbd
BOM = {"cocoon": cocoon_bom, "zenith": zenith_bom, "lodge": getattr(_bom, "lodge_bom", lambda: dict(steel_kg=0, total=0))}
PARTS = {"cocoon": cocoon_parts, "zenith": zenith_parts, "lodge": getattr(_pbd, "lodge_parts", lambda: [])}
CONNS = {"cocoon": COCOON_CONNECTIONS, "zenith": ZENITH_CONNECTIONS, "lodge": getattr(_pbd, "LODGE_CONNECTIONS", [])}

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "ZION_PROJETO_ARQUITETONICO_Apresentacao.html")
NAME = {"cocoon": "ZION CASULO", "zenith": "ZION SAFARI", "lodge": "ZION LODGE"}
SPLIT = {"cocoon": ("CA", "SULO"), "zenith": ("SA", "FARI"), "lodge": ("LO", "DGE")}
SUB = {"cocoon": "Cabana biomórfica em casulo", "zenith": "Cabana escultural de dois cumes", "lodge": "Pavilhão octogonal com Lanterna Zion"}
CONCEPT = {"cocoon": "Uma concha assimétrica de oito arcos elípticos: frente cheia, aberta ao vale por um anel de vidro inclinado 8°, e cauda afilada que guarda o banho. A Espinha de Luz corre a cumeeira; seis Janelas Olho recortam a membrana como lentes.",
           "zenith": "Dois cumes deslocados em diagonal, 5,80 m sobre a cama e 4,60 m sobre a Ilha do Café, erguidos por mastros com coroas de três braços. A membrana cai em catenárias até sete postes estaiados; o Óculo do Zênite abre o céu sobre o dormir.",
           "lodge": "Um pavilhão octogonal de 6,80 m entre faces, com cinco faces de vidro e três opacas que guardam o banho. Oito caibros sobem do anel de beiral à Lanterna Zion, um anel de vidro que despeja luz zenital sobre a cama; uma vela de sombra independente prolonga o deck em três faces."}
DETS = {"cocoon": ("detalhes/DET-01_cobertura_cocoon.svg", "detalhes/DET-10_arcos_cocoon.svg"), "zenith": ("detalhes/DET-02_cobertura_zenith.svg", "detalhes/DET-11_mastros_zenith.svg"), "lodge": ("detalhes/DET-12_lanterna_lodge.svg", "detalhes/DET-13_caibros_lodge.svg")}
PILES = {"cocoon": "44", "zenith": "30 + 7", "lodge": "22"}
slides = []

def money(v): return "R$ " + f"{v:,.0f}".replace(",", ".")
def fmt(v, n=1): return f"{v:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def img(rel, cls=""):
    rel = rel.replace("/renders/web/", "/renders/web/deck/")   # renders sem a interface do visualizador
    return f'<img class="{cls}" src="{rel}" alt="">'
def sheet(rel, cls=""):
    if not os.path.exists(os.path.join(ROOT, rel)): return f'<div class="sheet missing">[{esc(rel)} não gerado]</div>'
    return f'<div class="sheet {cls}">{svg_inline(rel)}</div>'
def esc(s): return html.escape(s)

def slide(body, cls="", label=""):
    slides.append((body, cls, label))

# ----------------------------------------------------------------------------- slides gerais
def capa():
    slide(f'''<div class="photo full">{img("cocoon/renders/web/cocoon_night.jpg")}</div><div class="overlay"></div>
<div class="cover">
  <div class="zbig">{zion_mark_html('64px', color='#FEF5F0', style='display:block;margin:0 auto 26px')}{zion_logo_html('54px', color='#FEF5F0', style='display:block;margin:0 auto 30px')}</div>
  <div class="eyebrow">ZION GLAMPING COLLECTION</div>
  <div class="split"><span>PROJETO</span><i></i><span>ARQUITETÔNICO</span></div>
  <div class="sub">ZION CASULO · ZION SAFARI · ZION LODGE 38 · 24 · 28 · ZION CÁPSULA</div>
  <div class="tag">Estudo preliminar das unidades proprietárias de hospedagem · pranchas, engenharia peça a peça, CAD, FF&amp;E e materiais · seis unidades sobre o mesmo sistema</div>
</div>''', "dark cover-slide", "CAPA")

def linha():
    def col(p, dims, areas, alt, fam):
        return f'''<div class="col">
<div class="pname">{NAME[p]}</div><div class="pfam">{fam}</div>
<div class="photo tall">{img(f"{p}/renders/web/{p}_ext_front.jpg")}</div>
<dl class="kv"><dt>Dimensões</dt><dd>{dims}</dd><dt>Altura</dt><dd>{alt}</dd><dt>Áreas</dt><dd>{areas}</dd></dl></div>'''
    slide(f'''<h2>A LINHA</h2>
<p class="lede">Três unidades proprietárias, o mesmo sistema construtivo: estrutura tubular em aço galvanizado, membrana PVDF tensionada, isolamento e vidro, sobre deck elevado em estacas helicoidais. Casulo, Safari e Lodge 38 em projeto arquitetônico; Lodge 24 e 28 como variantes paramétricas em conceito.</p>
<div class="two">{col("cocoon", "9,60 x 6,00 m", "48 m² internos · deck 29,9 m² · 78 m²", "4,20 m na cumeeira", "Cabana biomórfica em casulo · 8 arcos elípticos · Espinha de Luz · 6 Janelas Olho")}
{col("zenith", "9,50 x 5,40 m · cobertura 12,90 x 7,40 m", "48,4 m² internos · terraço 28 m² · 79,3 m²", "5,80 m e 4,60 m nos dois cumes", "Cabana escultural de dois cumes · mastros com coroas · Óculo do Zênite · Respiro")}</div>''', "dark", "A LINHA")

def sistema():
    layers = ["Estacas helicoidais galvanizadas", "Grelha de vigas U 150 e cabeçotes ajustáveis", "Módulos de piso: vigotas, PIR 50 mm, compensado naval", "Piso de carvalho de engenharia · porcelanato no banho",
              "Estrutura primária: arcos elípticos (Casulo) · pilares, anel de beiral e mastros (Safari)", "Terças, travamentos e cabos de contraventamento", "Perfil duplo keder de alumínio sobre a estrutura",
              "Membrana externa PVDF 1050 g/m² tipo III", "Câmara ventilada 60 mm", "Lã de PET 50 mm + manta refletiva", "Forro tensionado acústico classe M1", "Esquadrias de alumínio RPT bronze com vidro insulado low-e", "Deck de cumaru com fixação oculta e balizadores"]
    li = "".join(f'<li><span class="n">{i + 1:02d}</span>{esc(l)}</li>' for i, l in enumerate(layers))
    slide(f'''<div class="half left"><h2>ZION SHELL SYSTEM</h2><p class="lede">Treze camadas construtivas, do solo à luz. Fabricação em oficina, montagem em campo sem solda, parafusada classe 8.8.</p><ol class="layers">{li}</ol></div>
<div class="half right photo">{img("cocoon/renders/web/cocoon_structure.jpg")}<div class="cap">Estrutura primária do Casulo: 8 arcos elípticos Ø88,9 x 3,6 sobre trilhos de base</div></div>''', "dark", "SISTEMA CONSTRUTIVO")

# ----------------------------------------------------------------------------- por produto
def produto(p):
    d = f"{p}/desenhos"; j = f"{p}/projeto"; r = f"{p}/renders/web/{p}"
    a, b = SPLIT[p]
    slide(f'''<div class="photo full">{img(f"{r}_ext_aerial.jpg")}</div><div class="overlay"></div>
<div class="divider"><div class="split"><span>ZION</span><i></i><span>{a}{b}</span></div>
<div class="sub">{SUB[p]}</div></div>''', "dark cover-slide", NAME[p])
    concept = CONCEPT[p]
    slide(f'''<h2>CONCEITO</h2><p class="lede">{concept}</p>
<div class="three">{img(f"{r}_ext_front.jpg")}{img(f"{r}_ext_side.jpg")}{img(f"{r}_night.jpg")}</div>
<div class="caps3"><span>Fachada frontal</span><span>Lateral</span><span>Noite</span></div>''', "dark", NAME[p] + " · CONCEITO")
    slide(f'''<h2>ZION NEW LUXURY · INTERIOR</h2><p class="lede">Estar, suíte e banho em sequência, sob o forro tensionado. Luz indireta a 2700 K nos rodapés e requadros; sem pendentes; madeira, pedra e tecido.</p>
<div class="three">{img(f"{r}_int_living.jpg")}{img(f"{r}_int_bed.jpg")}{img(f"{r}_int_bath.jpg")}</div>
<div class="caps3"><span>Estar</span><span>Suíte</span><span>Banho</span></div>''', "dark", NAME[p] + " · INTERIOR")
    rows = "".join(f'<tr><td>{n}</td><td>{esc(amb)}</td><td class="num">{fmt(ar, 2)}</td></tr>' for (n, amb, ar, piso, niv) in AREAS[p] if "Ático" not in amb)
    tot_int = sum(ar for (n, amb, ar, piso, niv) in AREAS[p] if not any(k in amb for k in ("Deck", "Terraço", "Passarela", "Escada", "Hidro", "Ático")))
    tot_ext = sum(ar for (n, amb, ar, piso, niv) in AREAS[p] if any(k in amb for k in ("Deck", "Terraço", "Passarela", "Escada", "Hidro")))
    slide(f'''<div class="wide">{sheet(f"{d}/02_planta_humanizada.svg")}</div>
<div class="side"><h3>PLANTA DE LAYOUT</h3><div class="pa">PA-03 · 1:50</div>
<table class="areas"><tr><th></th><th>Ambiente</th><th class="num">m²</th></tr>{rows}
<tr class="tot"><td></td><td>Interna</td><td class="num">{fmt(tot_int, 1)}</td></tr><tr class="tot"><td></td><td>Externa</td><td class="num">{fmt(tot_ext, 1)}</td></tr><tr class="tot"><td></td><td>Total</td><td class="num">{fmt(tot_int + tot_ext, 1)}</td></tr></table></div>''', "dark", NAME[p] + " · LAYOUT")
    slide(f'''<h2>PLANTA BAIXA COTADA <small>PA-02 · 1:50</small></h2><div class="one">{sheet(f"{d}/03_planta_tecnica.svg")}</div>''', "dark", NAME[p] + " · PLANTA")
    slide(f'''<h2>CORTES <small>PA-06a corte longitudinal A-A · PA-06b corte transversal B-B · 1:50</small></h2><div class="two-sheets">{sheet(f"{d}/06_corte_longitudinal.svg")}{sheet(f"{d}/07_corte_transversal.svg")}</div>''', "dark", NAME[p] + " · CORTES")
    slide(f'''<h2>FACHADAS <small>PA-07a frontal · PA-07b traseira · PA-08a lateral direita · PA-08b lateral esquerda · 1:50</small></h2>
<div class="grid4">{sheet(f"{d}/04_elevacao_frontal.svg")}{sheet(f"{d}/04b_fachada_traseira.svg")}{sheet(f"{d}/05_elevacao_lateral.svg")}{sheet(f"{j}/PA-08b_fachada_lateral_esquerda.svg")}</div>''', "dark", NAME[p] + " · FACHADAS")
    slide(f'''<h2>COBERTURA E FORRO <small>PA-04 planta de cobertura · PA-05 forro refletido e iluminação · 1:50</small></h2><div class="two-sheets">{sheet(f"{j}/PA-04_planta_cobertura.svg")}{sheet(f"{j}/PA-05_forro_iluminacao.svg")}</div>''', "dark", NAME[p] + " · COBERTURA")
    E = ESQUADRIAS[p]
    slide(f'''<h2>QUADRO DE ESQUADRIAS <small>PA-09 · {len(E)} tipos · {sum(e[4] for e in E)} unidades · vidro insulado 6 lam + 12 Ar + 6 temp low-e</small></h2><div class="one">{sheet(f"{j}/PA-09_quadro_esquadrias.svg")}</div>''', "dark", NAME[p] + " · ESQUADRIAS")
    bm = BOM[p](); parts = PARTS[p](); conns = CONNS[p]
    slide(f'''<h2>ESTRUTURA <small>PA-10 planta estrutural · PA-12d estudo da estrutura metálica</small></h2>
<div class="two-sheets">{sheet(f"{d}/03b_planta_estrutural.svg")}{sheet(f"{d}/12_estrutura_isometrica.svg")}</div>
<div class="stats"><div><b>{bm["steel_kg"]:,}</b><span>kg de aço galvanizado</span></div><div><b>{len(parts)}</b><span>famílias de peças codificadas</span></div><div><b>{len(conns)}</b><span>tipos de conexão parafusada</span></div><div><b>{PILES[p]}</b><span>estacas helicoidais</span></div></div>'''.replace(",", "."), "dark", NAME[p] + " · ESTRUTURA")
    det = DETS[p]
    det_sub = {"cocoon": "cobertura em camadas · arcos e emendas", "zenith": "cobertura em camadas · mastros e coroas", "lodge": "lanterna · caibros e anel de beiral"}[p]
    if os.path.exists(os.path.join(ROOT, det[0])):
        slide(f'''<h2>DETALHES CONSTRUTIVOS <small>PA-11 · {det_sub} · 1:5 a 1:20</small></h2><div class="two-sheets">{sheet(det[0])}{sheet(det[1])}</div>''', "dark", NAME[p] + " · DETALHES")
    slide(f'''<h2>ISOMÉTRICA E MODELO EXPLODIDO <small>PA-12a · PA-12b</small></h2><div class="two-sheets">{sheet(f"{d}/08_isometrica.svg")}{sheet(f"{d}/10_modelo_explodido.svg")}</div>''', "dark", NAME[p] + " · ISOMÉTRICAS")

def lodge_family():
    """Lodge 24 e Lodge 28: variantes paramétricas (conceito) + FF&E da linha."""
    from geometry import Lodge24, Lodge28
    import ffe
    slide(f'''<div class="divider"><div class="split"><span>LODGE</span><i></i><span>24 · 28</span></div><div class="sub">Variantes paramétricas da família Lodge · estudo de conceito</div></div>''', "dark cover-slide", "FAMÍLIA LODGE")
    cards = ""
    for L, code in ((Lodge24(), "lodge24"), (Lodge28(), "lodge28")):
        cards += f'''<div class="col"><div class="pname">{L.NAME}</div><div class="pfam">{"Octógono compacto para casal" if code == "lodge24" else "Octógono alongado com terraço e duas lanternas"}</div>
{sheet(f"{code}/desenhos/01_conceito.svg")}
<dl class="kv"><dt>Planta</dt><dd>{fmt(L.F)} m entre faces{" · 7,80 m de comprimento" if L.M else ""}</dd><dt>Áreas</dt><dd>{fmt(L.floor_area())} m² internos · deck {fmt(L.deck_area())} m² · {fmt(L.floor_area() + L.deck_area())} m²</dd><dt>Alturas</dt><dd>beiral {fmt(L.Z_EAVE)} m · lanterna {fmt(L.Z_TOP)} m</dd></dl></div>'''
    slide(f'''<h2>FAMÍLIA LODGE · 24 E 28</h2><p class="lede">A mesma geometria paramétrica do Lodge 38 gera a unidade compacta para casal e a unidade alongada com terraço: o octógono muda de tamanho ou ganha um corpo reto entre duas lanternas, e o kit continua o mesmo.</p><div class="two">{cards}</div>''', "dark", "LODGE 24 · 28")
    rows = ""
    for code, name in (("cocoon", "ZION CASULO"), ("zenith", "ZION SAFARI"), ("lodge", "ZION LODGE 38"), ("lodge24", "ZION LODGE 24"), ("lodge28", "ZION LODGE 28"), ("capsule", "ZION CÁPSULA")):
        t = ffe.totals(code, 1); R = ffe.rows(code, 1); byc = {}
        for r in R: byc[r["cat"]] = byc.get(r["cat"], 0) + 1
        rows += f'<tr><td>{name}</td><td class="num">{t["n_items"]}</td>' + "".join(f'<td class="num">{byc.get(c, 0)}</td>' for c in "MFEODB") + '</tr>'
    cats = "".join(f"<li><b>{c}</b>{d}</li>" for c, d in (("Mobiliário", "cama king, cabeceira, criados, sofá, chaise, poltronas, ilha do café, closet, bancada"), ("Luminárias e decoração", "arandelas, luminárias de piso e mesa, tapetes de lã, cortinas e blackout, arte e objetos"),
                                                        ("Equipamentos", "mini cozinha do Casulo (indução, forno, geladeira, air fryer), cafeteira, cofre, som, fechadura digital, automação de cenas, lareira ecológica"), ("Enxoval e OS&E", "3 jogos de cama e banho, amenities, louças, mantas, acessórios, sinalização, segurança"), ("Deck e banho", "espreguiçadeiras, mesa e cadeiras, lanternas, ducha, acessórios em latão")))
    slide(f'''<h2>FF&amp;E · TUDO O QUE VAI DENTRO</h2><p class="lede">Além da construção, cada unidade recebe o FF&amp;E completo no padrão Zion New Luxury: materiais naturais, sem plástico aparente, sem pendentes, luz 2700 K. Lista item a item no Catálogo da Linha e na planilha ZION_FFE_Linha.xlsx.</p>
<div class="two"><div><table class="budget"><tr><th>Unidade</th><th class="num">Itens</th><th class="num">Mobiliário</th><th class="num">Luminárias</th><th class="num">Equipamentos</th><th class="num">Enxoval</th><th class="num">Deck</th><th class="num">Banho</th></tr>{rows}</table>
<p class="note">Número de itens por categoria; lista item a item, com especificação, ambiente e quantidade, no Catálogo da Linha e na planilha de materiais e FF&amp;E.</p></div>
<div><ol class="next">{cats}</ol></div></div>''', "dark", "FF&E")

def referencias_mercado():
    """Lodge 24 x H23 e Lodge 28 x H28 (cotações NOMASTRA), sem preços."""
    from referencias import REFS, comparativo, ref
    for code, name in (("lodge24", "LODGE 24"), ("lodge28", "LODGE 28")):
        R = ref(code)
        rows = "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{esc(c)}</td></tr>" for a, b, c in comparativo(code)[:11])
        slide(f'''<h2>{name} × REFERÊNCIA DE MERCADO <small>cotação de fornecedor de {esc(R["data"])} · lodge {esc(R["modelo"])} {esc(R["tamanho"])} · {esc(R["area"])} · {esc(R["terraco"])} · sem preços</small></h2>
<table class="budget ref3"><tr><th>Item</th><th>Referência {esc(R["modelo"])}</th><th>ZION {name}</th></tr>{rows}</table>''', "dark", f"{name} · REFERÊNCIA")

def capsula():
    """Zion Cápsula: unidade compacta transportável (estudo de conceito)."""
    from geometry import Capsule
    K = Capsule()
    slide(f'''<div class="divider"><div class="split"><span>ZION</span><i></i><span>CÁPSULA</span></div><div class="sub">Cápsula monocoque transportável · Visor, Anel de Luz e Olhos · estudo de conceito</div></div>''', "dark cover-slide", "ZION CÁPSULA")
    slide(f'''<h2>ZION CÁPSULA <small>8,40 x 3,20 m · {fmt(K.floor_area())} m² internos · deck {fmt(K.deck_area())} m² · chega pronta da fábrica</small></h2>
<p class="lede">Uma casca de alumínio composto sobre doze anéis de aço, com a calota frontal inteira em vidro curvo (Visor), uma faixa de vidro que contorna a seção sobre a cama (Anel de Luz) e dois Olhos laterais. Fabricada e mobiliada em fábrica, viaja inteira em carreta e pousa em quatro pés telescópicos sobre estacas: instalação em um dia.</p>
<div class="two-sheets">{sheet("capsule/desenhos/01_conceito.svg")}{sheet("capsule/desenhos/08_isometrica.svg")}</div>''', "dark", "ZION CÁPSULA")

# ----------------------------------------------------------------------------- fechamento
def implantacao():
    slide(f'''<h2>IMPLANTAÇÃO <small>PA-01 · lote-tipo de 30 x 24 m · 1:200 · a adaptar a cada sítio</small></h2><div class="two-sheets">{sheet("cocoon/projeto/PA-01_implantacao.svg")}{sheet("zenith/projeto/PA-01_implantacao.svg")}</div>''', "dark", "IMPLANTAÇÃO")

def logistica():
    def col(p):
        b = (cocoon_bom if p == "cocoon" else zenith_bom)(); t = transport(b, p); A = ASSEMBLY[p]
        steps = "".join(f'<li><span class="n">{i + 1:02d}</span>{esc(s[0])}<em>{fmt(s[2], 1)} d · equipe {esc(str(s[3]))}</em></li>' for i, s in enumerate(A))
        return f'''<div class="col"><div class="pname">{NAME[p]}</div>
<div class="stats small"><div><b>{fmt(b["total"] / 1000, 1)} t</b><span>peso total do kit</span></div><div><b>{fmt(t["vol"], 1)} m³</b><span>volume de transporte</span></div><div><b>{int(sum(s[2] for s in A))} dias</b><span>montagem em campo</span></div></div>
<ol class="steps">{steps}</ol></div>'''
    slide(f'''<h2>FABRICAÇÃO, TRANSPORTE E MONTAGEM</h2><p class="lede">Kit fabricado em oficina e montado como um móvel: peças codificadas, encaixes macho-fêmea, flanges e parafusos classe 8.8. Sem solda em campo.</p>
<div class="two">{col("cocoon")}{col("zenith")}</div>''', "dark", "LOGÍSTICA")

def materiais_slide():
    """materiais estimados por grupo (sem preços): resumo das quantidades principais."""
    from product_book_data import bom_priced
    cols = ""
    for code, name in (("cocoon", "ZION CASULO"), ("zenith", "ZION SAFARI"), ("lodge", "ZION LODGE 38")):
        try: groups = bom_priced(code)
        except Exception: continue
        lis = ""
        for g, items in groups:
            top = items[0]
            lis += f'<li><span class="n">{esc(g[:2])}</span>{esc(g[3:])}<em>{len(items)} itens</em></li>'
        cols += f'<div class="col"><div class="pname">{name}</div><ol class="steps">{lis}</ol></div>'
    slide(f'''<h2>MATERIAIS ESTIMADOS · 18 GRUPOS</h2><p class="lede">Lista de materiais com quantidades estimadas a partir da geometria, sem preços, organizada nos 18 grupos do kit de fábrica: base para cotação e para o pedido de fabricação. Quantidades completas no Product Book e na planilha de materiais.</p>
<div class="three cols">{cols}</div>''', "dark", "MATERIAIS")

def proximos():
    items = [("Cálculo estrutural com ART", "Verificação NBR 8800 / NBR 6123 (V0 = 45 m/s) das bitolas pré-dimensionadas; ligações e chapas."),
             ("Form-finding da membrana", "Padronagem e pré-tensão (2,5 kN/m) com o fabricante da membrana PVDF; compensações de corte."),
             ("Sondagem e fundação", "SPT ou ensaio de torque no sítio; definição entre os modelos A, B e C de fundação."),
             ("Projeto executivo de esquadrias e instalações", "Vidros insulados curvos, esquadrias RPT, elétrica, hidráulica e climatização dutada."),
             ("Protótipo no Zion Bubble Glamping", "Unidade piloto de cada produto; gabaritos de fabricação; manual de montagem validado em campo."),
             ("Industrialização", "Série de 5 a 50 unidades com redução de custo por escala e cronograma de fábrica.")]
    li = "".join(f'<li><span class="n">{i + 1:02d}</span><b>{esc(t)}</b><p>{esc(s)}</p></li>' for i, (t, s) in enumerate(items))
    slide(f'''<div class="half left"><h2>DO CONCEITO À OPERAÇÃO</h2><p class="lede">O que este estudo preliminar ainda pede antes da fabricação.</p><ol class="next">{li}</ol></div>
<div class="half right photo">{img("zenith/renders/web/zenith_night.jpg")}</div>''', "dark", "PRÓXIMOS PASSOS")

def fim():
    slide(f'''<div class="closing"><div class="z">{zion_mark_html('110px', color='#FEF5F0', style='display:block;margin:0 auto 40px')}</div><div class="split"><span>DESENVOLVEMOS</span><i></i><span>DESTINOS</span></div>
<div class="sub">ZION HOTEL GROUP INTERNATIONAL · ZION GLAMPING COLLECTION</div>
<div class="tag">Projeto arquitetônico ZION CASULO · ZION SAFARI · conceito ZION LODGE · R00 · setembro de 2026 · pranchas, product book, planilha de orçamento e arquivos CAD no repositório</div></div>''', "dark cover-slide", "")

CSS = """
@font-face{font-family:'Aventa';src:url(assets/aventa.woff2) format('woff2');font-weight:100 900;font-display:swap}
:root{--black:#040605;--cream:#FEF5F0;--sand:#DED6BF;--earth:#8B714E;--green:#1B2117}
*{box-sizing:border-box} body{margin:0;background:#111;font-family:'Aventa','DM Sans',Helvetica,Arial,sans-serif;color:var(--cream);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.slide{position:relative;width:1600px;height:900px;margin:0 auto 24px;background:var(--black);overflow:hidden;padding:64px 80px 70px;page-break-after:always;break-after:page}
.slide.cover-slide{padding:0}
.photo img{width:100%;height:100%;object-fit:cover;display:block} .photo.full{position:absolute;inset:0} .overlay{position:absolute;inset:0;background:rgba(4,6,5,.62)}
.cover,.divider,.closing{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:0 120px}
.eyebrow{font-size:12px;letter-spacing:.42em;color:var(--sand);margin-bottom:60px}
.split{display:flex;align-items:center;justify-content:space-between;width:100%;font-weight:200;font-size:64px;letter-spacing:.26em;line-height:1;white-space:nowrap} .split i{flex:1;height:1px;background:var(--cream);margin:0 48px;opacity:.85}
.split span:last-child{text-indent:.26em}
.cover .sub,.divider .sub,.closing .sub{margin-top:44px;font-size:22px;letter-spacing:.34em;font-weight:300;color:var(--sand)}
.cover .tag,.closing .tag{margin-top:110px;font-size:13px;letter-spacing:.14em;color:var(--sand);max-width:900px;line-height:1.9;font-weight:300}
.closing .z{font-size:120px;font-weight:200;letter-spacing:0;margin-bottom:40px;color:var(--cream)}
h2{margin:0 0 14px;font-weight:200;font-size:34px;letter-spacing:.34em;text-transform:uppercase;line-height:1.1} h2 small{display:block;font-size:12px;letter-spacing:.16em;color:var(--sand);margin-top:10px;font-weight:300;text-transform:none}
h3{margin:0;font-weight:200;font-size:26px;letter-spacing:.3em;text-transform:uppercase}
.lede{margin:0 0 26px;max-width:1120px;font-size:16px;line-height:1.9;font-weight:300;color:var(--cream)}
.foot{position:absolute;left:80px;right:80px;bottom:26px;display:flex;justify-content:space-between;font-size:10px;letter-spacing:.24em;color:var(--sand);font-weight:300}
.foot span:nth-child(2){flex:1;text-align:center}
.two{display:grid;grid-template-columns:1fr 1fr;gap:56px} .col .pname{font-size:20px;letter-spacing:.3em;font-weight:300;margin-bottom:4px} .col .pfam{font-size:12px;letter-spacing:.12em;color:var(--sand);font-weight:300;margin-bottom:18px;line-height:1.7}
.photo.tall{height:340px;overflow:hidden;margin-bottom:22px}
.kv{display:grid;grid-template-columns:120px 1fr;gap:10px 18px;margin:0;font-size:14px;line-height:1.6;font-weight:300} .kv.stack{grid-template-columns:1fr;gap:2px 0;font-size:12.5px} .kv.stack dt{margin-top:10px} .note{font-size:11.5px;line-height:1.6;color:var(--sand);font-weight:300;margin-top:22px;border-top:1px solid rgba(222,214,191,.3);padding-top:12px} .kv dt{color:var(--sand);letter-spacing:.2em;font-size:10px;text-transform:uppercase;padding-top:5px} .kv dd{margin:0}
.half{position:absolute;top:64px;bottom:70px} .half.left{left:80px;width:640px} .half.right{left:780px;right:80px;overflow:hidden} .half.right .cap{position:absolute;left:0;right:0;bottom:0;padding:16px 20px;background:rgba(4,6,5,.7);font-size:11px;letter-spacing:.14em;color:var(--sand);font-weight:300}
ol.layers,ol.next,ol.steps{list-style:none;margin:0;padding:0} ol.layers li{display:flex;gap:16px;font-size:13.5px;line-height:1.5;padding:7px 0;border-bottom:1px solid rgba(222,214,191,.16);font-weight:300} .n{color:var(--earth);font-weight:600;letter-spacing:.1em;font-size:11px;min-width:26px;padding-top:2px}
ol.next li{display:grid;grid-template-columns:30px 1fr;gap:4px 14px;padding:12px 0;border-bottom:1px solid rgba(222,214,191,.16)} ol.next li b{font-weight:500;font-size:15px;letter-spacing:.04em} ol.next li p{grid-column:2;margin:0;font-size:12.5px;line-height:1.6;color:var(--sand);font-weight:300}
ol.next li b{display:block} ol.next li{display:block;font-size:12.5px;line-height:1.6;color:var(--sand);font-weight:300}
.col .sheet{margin:10px 0 14px}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;height:520px} .three img{width:100%;height:100%;object-fit:cover;display:block} .three.cols{height:auto;gap:40px} .three.cols ol.steps li{font-size:11.5px;padding:4px 0}
.caps3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:12px;font-size:10.5px;letter-spacing:.24em;color:var(--sand);text-transform:uppercase;font-weight:300}
.sheet{background:#FEF5F0;border:1px solid rgba(222,214,191,.35);line-height:0} .sheet svg{width:100%;height:auto;display:block}
.one{height:730px;display:flex;justify-content:center} .one .sheet{height:100%;aspect-ratio:1.6;width:auto} .one .sheet svg{height:100%;width:auto}
.two-sheets{display:grid;grid-template-columns:1fr 1fr;gap:20px;align-items:start}
.grid4{display:grid;grid-template-columns:1fr 1fr;gap:12px 20px;width:1180px;margin:0 auto}
.wide{position:absolute;left:80px;top:64px;width:1080px} .side{position:absolute;left:1210px;right:80px;top:64px} .side .pa{font-size:11px;letter-spacing:.2em;color:var(--sand);margin:10px 0 22px;font-weight:300}
table{border-collapse:collapse;width:100%;font-size:12.5px;font-weight:300;font-variant-numeric:tabular-nums} th{text-align:left;font-weight:300;font-size:10px;letter-spacing:.2em;color:var(--sand);text-transform:uppercase;padding:0 8px 8px;border-bottom:1px solid var(--sand)} td{padding:7px 8px;border-bottom:1px solid rgba(222,214,191,.16);vertical-align:top} .num{text-align:right;white-space:nowrap} tr.tot td{font-weight:500;color:var(--cream);border-bottom:1px solid var(--sand)}
table.areas td:first-child{color:var(--earth);font-weight:600;font-size:10px;letter-spacing:.1em;width:28px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:22px} .stats div{border-top:1px solid var(--sand);padding-top:12px} .stats b{display:block;font-size:34px;font-weight:200;letter-spacing:.06em;font-variant-numeric:tabular-nums} .stats span{font-size:11px;letter-spacing:.18em;color:var(--sand);text-transform:uppercase;font-weight:300}
.stats.small{grid-template-columns:repeat(3,1fr);margin:14px 0 20px} .stats.small b{font-size:28px}
ol.steps li{display:grid;grid-template-columns:30px 1fr auto;gap:12px;font-size:12.5px;padding:6px 0;border-bottom:1px solid rgba(222,214,191,.14);font-weight:300;align-items:baseline} ol.steps em{font-style:normal;color:var(--sand);font-size:11px;letter-spacing:.08em;white-space:nowrap}
table.ref3{font-size:11px} table.ref3 td,table.ref3 th{padding:4px 8px;vertical-align:top} table.ref3 td:first-child{width:12%} table.ref3 td:nth-child(2){width:40%}
table.budget td:first-child{color:var(--cream)} table.budget{font-size:12px}
@media print{@page{size:1600px 900px;margin:0} body{background:var(--black)} .slide{margin:0}}
"""

def build():
    capa(); linha(); sistema()
    for p in ("cocoon", "zenith", "lodge"): produto(p)
    lodge_family(); referencias_mercado(); capsula(); implantacao(); logistica(); materiais_slide(); proximos(); fim()
    N = len(slides); out = []
    for i, (body, cls, label) in enumerate(slides):
        foot = "" if i in (0, N - 1) else f'<div class="foot"><span>APRESENTAÇÃO · PROJETO ARQUITETÔNICO</span><span>ZION HOTEL · GROUP INTERNATIONAL{" · " + esc(label) if label else ""}</span><span>2026 · {i + 1:02d} / {N:02d}</span></div>'
        out.append(f'<section class="slide {cls}">{body}{foot}</section>')
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · Projeto Arquitetônico · Apresentação</title><style>{CSS}</style></head><body>{"".join(out)}</body></html>'
    open(OUT, "w", encoding="utf-8").write(doc)
    print(OUT, N, "slides", round(os.path.getsize(OUT) / 1e6, 1), "MB")

if __name__ == "__main__":
    build()

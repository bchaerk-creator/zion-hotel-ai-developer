# -*- coding: utf-8 -*-
"""CATÁLOGO DA LINHA ZION GLAMPING COLLECTION: as seis unidades (Casulo, Safari, Lodge 38, Lodge 24, Lodge 28, Cápsula) com dados,
desenhos, imagens, FF&E completo (tudo o que vai dentro) e resumo de investimento. Gera ZION_CATALOGO_LINHA.html (A4 paisagem,
SVG inline) e ZION_FFE_Linha.xlsx. PDF: node export_pdf.js ../ZION_CATALOGO_LINHA.html ../ZION_CATALOGO_LINHA.pdf
Uso: python3 build_catalogo.py"""
import os, html, math
from svgkit import zion_mark_html
from build_projeto_arquitetonico import svg_inline
from geometry import Cocoon, Zenith, LODGES, Capsule
import ffe
from capsule import capsule_materials

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "ZION_CATALOGO_LINHA.html")
XLS = os.path.join(ROOT, "ZION_MATERIAIS_FFE_Linha.xlsx")
C, Z, CAP = Cocoon(), Zenith(), Capsule()
LG = {k: v() for k, v in LODGES.items()}
SCEN = ["Econômico", "Zion Standard", "Zion Premium"]
PRICES = False   # documentos para a fábrica: sem preços (só materiais e quantidades estimadas)

def money(v): return "R$ " + f"{v:,.0f}".replace(",", ".")
def fmt(v, n=1): return f"{v:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def esc(s): return html.escape(str(s))
def exists(rel): return os.path.exists(os.path.join(ROOT, rel))
def img(rel, cls=""): return f'<img class="{cls}" src="{rel}" alt="">' if exists(rel) else ""
def sheet(rel): return f'<div class="sheet">{svg_inline(rel)}</div>' if exists(rel) else f'<div class="missing">[{esc(rel)} em geração]</div>'

# ---------------------------------------------------------------------------- dados dos produtos
try:
    from product_book_data import budget
    BUD = {p: budget(p, 1, 1) for p in ("cocoon", "zenith", "lodge")}
    BUD10 = {p: budget(p, 1, 10) for p in ("cocoon", "zenith", "lodge")}
except Exception as e:   # dados do lodge ainda em geração
    from product_book_data import budget
    BUD = {p: budget(p, 1, 1) for p in ("cocoon", "zenith")}; BUD10 = {p: budget(p, 1, 10) for p in ("cocoon", "zenith")}

def param_estimate(code):
    """estimativa paramétrica das variantes do Lodge a partir do Lodge 38 (custo sem NRE x (área total)^0,85 + NRE compartilhado de R$ 120 mil)."""
    if "lodge" not in BUD: return None, None
    b = BUD["lodge"]; base = b["total"] - b["nre"]; a0 = b["area_total"]
    L = LG[code] if code in LG else CAP; a = L.floor_area() + L.deck_area()
    est = base * (a / a0) ** 0.85 + 120000
    return est, est / a

PRODUCTS = [
    dict(code="cocoon", name="ZION CASULO", family="Cabana biomórfica em casulo", status="Projeto arquitetônico completo · engenharia peça a peça · DXF",
         dims="9,60 x 6,00 x 4,20 m", area_int=48.0, area_ext=29.9, roof="concha de membrana sobre 8 arcos elípticos", height="4,20 m", program="Lounge com chaise e minibar · suíte king sob a Espinha de Luz · banho com banheira na cauda · deck de 29,9 m² (hot tub opcional)",
         beds="1 casal (king)", guests="2 + 1 (chaise-cama opcional)", struct="8 arcos elípticos Ø88,9 · anel frontal inclinado 8° · trilhos de base · 44 estacas", days=12,
         hero="cocoon/renders/web/cocoon_ext_front.jpg", imgs=["cocoon/renders/web/cocoon_night.jpg", "cocoon/renders/web/cocoon_int_living.jpg", "cocoon/renders/web/cocoon_int_bed.jpg"],
         sheets=["cocoon/desenhos/02_planta_humanizada.svg", "cocoon/desenhos/06_corte_longitudinal.svg", "cocoon/desenhos/04_elevacao_frontal.svg", "cocoon/desenhos/08_isometrica.svg"]),
    dict(code="zenith", name="ZION SAFARI", family="Cabana escultural de dois cumes", status="Projeto arquitetônico completo · engenharia peça a peça · DXF",
         dims="9,50 x 5,40 m · cobertura 12,90 x 7,40 · cumes 5,80 / 4,60 m", area_int=48.4, area_ext=28.0, roof="membrana de dois cumes sobre mastros com coroas e 7 postes estaiados", height="5,80 m", program="Lounge e Ilha do Café · suíte king sob o Óculo do Zênite · closet · banho com bancada dupla e banheira · terraço com hidromassagem e passarela",
         beds="1 casal (king)", guests="2 + 1", struct="2 mastros Ø139,7 · 10 pilares · anel de beiral 150 x 100 · 7 postes estaiados · 30 + 7 estacas", days=15,
         hero="zenith/renders/web/zenith_ext_front.jpg", imgs=["zenith/renders/web/zenith_night.jpg", "zenith/renders/web/zenith_int_living.jpg", "zenith/renders/web/zenith_int_bed.jpg"],
         sheets=["zenith/desenhos/02_planta_humanizada.svg", "zenith/desenhos/06_corte_longitudinal.svg", "zenith/desenhos/04_elevacao_frontal.svg", "zenith/desenhos/08_isometrica.svg"]),
    dict(code="lodge", name="ZION LODGE 38", family="Pavilhão octogonal com Lanterna Zion", status="Projeto arquitetônico em desenvolvimento · engenharia peça a peça · orçamento",
         dims="octógono 6,80 m entre faces · beiral 2,70 · lanterna 5,20 m", area_int=LG["lodge"].floor_area(), area_ext=LG["lodge"].deck_area(), roof="membrana cônica em 8 gomos sobre caibros radiais e anel de compressão", height="5,20 m",
         program="Estar com sofá e poltrona · suíte king sob a lanterna · café/minibar e closet · banho com banheira de sentar · deck em três faces com vela de sombra",
         beds="1 casal (king)", guests="2 + 1", struct="8 pilares Ø101,6 revestidos · anel de beiral · 8 caibros Ø76 · 22 estacas", days=9,
         hero="lodge/renders/web/lodge_ext_front.jpg", imgs=["lodge/renders/web/lodge_night.jpg", "lodge/renders/web/lodge_int_living.jpg", "lodge/renders/web/lodge_int_bed.jpg"],
         sheets=["lodge/desenhos/02_planta_humanizada.svg", "lodge/desenhos/06_corte_longitudinal.svg", "lodge/desenhos/04_elevacao_frontal.svg", "lodge/desenhos/08_isometrica.svg"], concept="lodge/desenhos/01_conceito.svg"),
    dict(code="lodge24", name="ZION LODGE 24", family="Octógono compacto para casal", status="Estudo de conceito · estimativa paramétrica",
         dims="octógono 5,40 m entre faces · beiral 2,60 · lanterna 4,70 m", area_int=LG["lodge24"].floor_area(), area_ext=LG["lodge24"].deck_area(), roof="membrana cônica em 8 gomos, lanterna Ø1,20", height="4,70 m",
         program="Duas poltronas junto ao vidro · suíte king sob a lanterna · café/minibar e closet · banho com chuveiro · deck de uma face com vela de sombra",
         beds="1 casal (king)", guests="2", struct="8 pilares Ø101,6 · anel de beiral · 8 caibros · 15 estacas", days=6,
         hero="lodge24/desenhos/08_isometrica.svg", imgs=[], sheets=["lodge24/desenhos/01_conceito.svg", "lodge24/desenhos/08_isometrica.svg"]),
    dict(code="lodge28", name="ZION LODGE 28", family="Octógono alongado com terraço", status="Estudo de conceito · estimativa paramétrica",
         dims="4,20 x 7,80 m · beiral 2,60 · duas lanternas a 4,45 m", area_int=LG["lodge28"].floor_area(), area_ext=LG["lodge28"].deck_area(), roof="membrana em gomos com cumeeira entre duas lanternas", height="4,45 m",
         program="Estar com sofá sob a lanterna 2 · suíte king sob a lanterna 1 · café/minibar e closet · banho no fundo · terraço de 17,5 m² em três faces com vela",
         beds="1 casal (king)", guests="2 + 1", struct="8 pilares Ø101,6 · anel de beiral · 10 caibros · 21 estacas", days=8,
         hero="lodge28/desenhos/08_isometrica.svg", imgs=[], sheets=["lodge28/desenhos/01_conceito.svg", "lodge28/desenhos/08_isometrica.svg"]),
    dict(code="capsule", name="ZION CÁPSULA", family="Cápsula monocoque transportável", status="Estudo de conceito · materiais estimados por geometria",
         dims="8,40 x 3,20 x 3,20 m · piso a 1,05 m do terreno", area_int=CAP.floor_area(), area_ext=CAP.deck_area(), roof="casca em alumínio composto sobre 12 anéis · Visor de vidro curvo · Anel de Luz", height="3,50 m (com pés)",
         program="Chaise e poltrona junto ao Visor · café/minibar · suíte queen sob o Anel de Luz · closet · banho com chuveiro e Olho · compartimento técnico na cauda · deck frontal de 8,3 m²",
         beds="1 casal (queen)", guests="2", struct="12 anéis 60 x 40 · 7 longarinas · chassi U 150 · 4 pés telescópicos · 8 estacas", days=1,
         hero="capsule/desenhos/08_isometrica.svg", imgs=[], sheets=["capsule/desenhos/01_conceito.svg", "capsule/desenhos/08_isometrica.svg"]),
]

def cost(code):
    if code in BUD: b = BUD[code]; return b["total"], b["por_m2"], BUD10[code]["total"], "orçamento peça a peça (Product Book)"
    est, m2 = param_estimate(code)
    if est is None: return None, None, None, ""
    return est, m2, est * 0.66, "estimativa paramétrica a partir do Lodge 38"

# ---------------------------------------------------------------------------- páginas
def page(body, cls=""): return f'<section class="page {cls}">{body}</section>'
def foot(label): return f'<div class="foot"><span>ZION GLAMPING COLLECTION · CATÁLOGO DA LINHA</span><span>{esc(label)}</span><span>SET 2026</span></div>'

def cover():
    return page(f'''<div class="cover"><div class="brand">{zion_mark_html('0.95em', style='margin-right:.5em')}ZION</div><div class="sub">GLAMPING COLLECTION · ZION HOTEL GROUP INTERNATIONAL</div>
<h1>CATÁLOGO<br>DA LINHA</h1><p class="lead">Seis unidades proprietárias de hospedagem sobre o mesmo sistema construtivo: projeto, camadas, materiais estimados e FF&amp;E completo, tudo o que vai dentro de cada cabana.</p>
<ul class="prods">{"".join(f"<li><b>{esc(p['name'])}</b><span>{esc(p['family'])} · {fmt(p['area_int'])} m² + {fmt(p['area_ext'])} m²</span></li>" for p in PRODUCTS)}</ul>
<p class="warn">Documento técnico para fabricação e cotação, sem preços. Pré-dimensionamento de engenharia a validar por profissionais habilitados (ART/RRT).</p></div>''', "dark")

def linha():
    rows = ""
    for p in PRODUCTS:
        tot, m2, t10, src = cost(p["code"]); f = ffe.totals(p["code"], 1)
        rows += f'''<tr><td><b>{esc(p["name"])}</b><br><small>{esc(p["family"])}</small></td><td>{esc(p["dims"])}</td><td class="num">{fmt(p["area_int"])}</td><td class="num">{fmt(p["area_ext"])}</td><td class="num">{fmt(p["area_int"] + p["area_ext"])}</td>
<td>{esc(p["height"])}</td><td>{esc(p["struct"])}</td><td class="num">{p["days"]} d</td><td class="num">{f["n_items"]} itens</td><td><small>{esc(p["status"])}</small></td></tr>'''
    return page(f'''<h2>A LINHA</h2><p class="lede">Zion Shell System em seis formatos: do casulo biomórfico ao pavilhão compacto para casal e à cápsula que chega pronta da fábrica. Mesmo kit parafusado, mesmas camadas, mesma fábrica.</p>
<div class="tw"><table><tr><th>Unidade</th><th>Dimensões</th><th class="num">Interna m²</th><th class="num">Deck m²</th><th class="num">Total m²</th><th>Altura</th><th>Estrutura</th><th class="num">Montagem</th><th class="num">FF&amp;E</th><th>Estágio</th></tr>{rows}</table></div>
<p class="note">Montagem em campo com equipe de 4 montadores e 1 líder, sem grua. FF&amp;E = mobiliário, luminárias, equipamentos, enxoval e itens do deck (lista item a item nas páginas de cada unidade). Zion Casulo, Zion Safari e Zion Lodge 38 têm projeto arquitetônico e lista de materiais completos; Lodge 24 e 28 são variantes paramétricas em conceito; a Cápsula é um estudo de conceito com materiais estimados a partir da geometria (monta em fábrica e chega pronta: 1 dia de instalação).</p>
<div class="strip5">{"".join(f'<figure>{img(p["hero"]) if p["hero"].endswith(".jpg") else sheet(p["hero"])}<figcaption>{esc(p["name"])}</figcaption></figure>' for p in PRODUCTS)}</div>''' + foot("A linha"))

def product_pages(p):
    code = p["code"]; tot, m2, t10, src = cost(code); f = ffe.totals(code, 1)
    kv = [("Dimensões", p["dims"]), ("Área interna", fmt(p["area_int"]) + " m²"), ("Deck / terraço", fmt(p["area_ext"]) + " m²"), ("Área total", fmt(p["area_int"] + p["area_ext"]) + " m²"), ("Cobertura", p["roof"]),
          ("Estrutura", p["struct"]), ("Hóspedes", p["guests"]), ("Montagem em campo", f"{p['days']} dias"), ("Envelope", "membrana PVDF 1050 g/m² · câmara ventilada 60 mm · lã de PET 50 mm · forro tensionado"),
          ("Fechamentos", "vidro insulado 6 lam + 12 Ar + 6 temp low-e em alumínio bronze RPT · painéis SIP + ripado"), ("Piso e deck", "carvalho de engenharia 14 mm · porcelanato no banho · deck de cumaru 20 x 140"), ("FF&E", f"{f['n_items']} itens (lista completa a seguir)")]
    hero = img(p["hero"], "hero") if p["hero"].endswith(".jpg") else sheet(p["hero"])
    pg1 = page(f'''<div class="ph"><div class="pname">{esc(p["name"])}</div><div class="pfam">{esc(p["family"])} · {esc(p["status"])}</div></div>
<div class="two"><div>{hero}<div class="thumbs">{"".join(img(i) for i in p["imgs"])}</div></div>
<div><p class="lede">{esc(p["program"])}</p><dl class="kv">{"".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in kv)}</dl></div></div>''' + foot(p["name"]))
    sh = p["sheets"]
    if len(sh) >= 4:
        pg2 = page(f'''<h3>{esc(p["name"])} · DESENHOS</h3><div class="grid4">{"".join(sheet(s) for s in sh[:4])}</div>''' + foot(p["name"] + " · desenhos"))
    else:
        pg2 = page(f'''<h3>{esc(p["name"])} · CONCEITO</h3><div class="grid2">{"".join(sheet(s) for s in sh)}</div>''' + foot(p["name"] + " · conceito"))
    # FF&E
    R = ffe.rows(code, 1); by = {}
    for r in R: by.setdefault(r["cat_name"], []).append(r)
    trs = ""
    for cat, items in by.items():
        trs += f'<tr class="cat"><td colspan="5">{esc(cat)} · {len(items)} itens</td></tr>'
        for r in items:
            trs += f'<tr class="{"opt" if r["optional"] else ""}"><td>{r["code"]}</td><td>{esc(r["desc"])}{" <em>(opcional)</em>" if r["optional"] else ""}</td><td class="spec">{esc(r["spec"])}{(" · " + esc(r["obs"])) if r["obs"] else ""}</td><td>{esc(r["amb"])}</td><td class="num">{fmt(r["qty"], 1).rstrip("0").rstrip(",")} {r["un"]}</td></tr>'
    pg3 = page(f'''<h3>{esc(p["name"])} · FF&amp;E · TUDO O QUE VAI DENTRO</h3>
<div class="tw"><table class="ffe"><tr><th>Cód.</th><th>Item</th><th>Especificação</th><th>Ambiente</th><th class="num">Qtd</th></tr>{trs}
<tr class="tot"><td colspan="4">TOTAL · {f["n_items"]} itens · {fmt(f["n_units"], 0)} unidades (opcionais marcados)</td><td></td></tr></table></div>''' + foot(p["name"] + " · FF&E"), "flow")
    if code == "lodge28":
        from referencias import comparativo, H28
        trs = "".join(f"<tr><th>{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td></tr>" for a, b, c in comparativo())
        pg3 += page(f'''<h3>ZION LODGE 28 · REFERÊNCIA DE MERCADO</h3><p class="lede">Cotação de fornecedor recebida em {esc(H28["data"])} para o lodge {esc(H28["modelo"])} de {esc(H28["tamanho"])} ({esc(H28["area"])} internos, terraço {esc(H28["terraco"])}, cume {esc(H28["altura"])}, beiral {esc(H28["beiral"])}), usada como faixa de área e programa. O comparativo abaixo mostra, item a item, o que a Zion Lodge 28 muda em relação ao produto de catálogo. Sem preços: a referência comercial fica no arquivo interno.</p>
<div class="tw"><table class="ffe small ref"><tr><th>Item</th><th>Referência de mercado H28</th><th>ZION LODGE 28</th></tr>{trs}</table></div>''' + foot("Lodge 28 · referência de mercado"), "flow")
    return pg1 + pg2 + pg3

def catalogo_itens():
    trs = ""; cur = None
    for code, (desc, spec, un, price, cat) in sorted(ffe.ITEMS.items(), key=lambda kv: (kv[1][4], kv[0])):
        if cat != cur: cur = cat; trs += f'<tr class="cat"><td colspan="4">{esc(ffe.CATS[cat])}</td></tr>'
        trs += f'<tr><td>{code}</td><td>{esc(desc)}</td><td class="spec">{esc(spec)}</td><td>{un}</td></tr>'
    return page(f'''<h3>CATÁLOGO DE ITENS FF&amp;E · ESPECIFICAÇÃO ZION NEW LUXURY</h3><p class="lede">Padrão único para toda a linha: materiais naturais (carvalho, linho, lã, latão escovado, pedra), sem plástico aparente, sem pendentes, luz 2700 K.</p>
<div class="tw cols2"><table class="ffe small"><tr><th>Cód.</th><th>Item</th><th>Especificação</th><th>Un.</th></tr>{trs}</table></div>''' + foot("Catálogo FF&E"), "flow")

def materiais():
    from product_book_data import bom_priced
    pages = ""
    for code, name in (("cocoon", "ZION CASULO"), ("zenith", "ZION SAFARI"), ("lodge", "ZION LODGE 38"), ("capsule", "ZION CÁPSULA")):
        try: groups = capsule_materials() if code == "capsule" else bom_priced(code)
        except Exception: continue
        trs = ""
        for g, items in groups:
            trs += f'<tr class="cat"><td colspan="3">{esc(g)}</td></tr>'
            for (desc, un, qtd, key) in items:
                trs += f'<tr><td>{esc(desc)}</td><td>{esc(un)}</td><td class="num">{fmt(qtd, 1).rstrip("0").rstrip(",") if isinstance(qtd, float) else qtd}</td></tr>'
        pages += page(f'''<h3>{name} · MATERIAIS ESTIMADOS (QUANTIDADES)</h3><p class="lede">Lista de materiais por grupo construtivo, com quantidades estimadas a partir da geometria do projeto (perdas e emendas incluídas onde indicado). Sem preços: a lista é a base para cotação junto aos fornecedores e para o kit de fábrica.</p>
<div class="tw"><table class="ffe small"><tr><th>Material / componente</th><th>Un.</th><th class="num">Quantidade</th></tr>{trs}</table></div>''' + foot(name + " · materiais"), "flow")
    return pages

def camadas():
    L = [("01", "Fundação", "Estacas helicoidais Ø76 galvanizadas, hélice Ø300, cabeçotes ajustáveis; alternativas A/B/C conforme sondagem"),
         ("02", "Estrutura do deck e piso", "Grelha de vigas U 150 x 60 x 3,0 galvanizadas; módulos de piso com vigotas 50 x 150 tratadas (ou LSF Ue 150) a cada 400 mm"),
         ("03", "Piso", "PIR 50 mm entre vigotas + manta; compensado naval 18 mm; carvalho de engenharia 14 mm; porcelanato 60 x 120 antiderrapante sobre placa cimentícia no banho; deck de cumaru 20 x 140 com fixação oculta"),
         ("04", "Estrutura metálica principal", "Casulo: 8 arcos elípticos Ø88,9 x 3,6 + anel frontal Ø101,6 · Safari: 2 mastros Ø139,7 x 4,5, 10 pilares, anel de beiral 150 x 100 · Lodge: 8 pilares Ø101,6 x 4,0 revestidos, anel de beiral 150 x 100, 8 caibros Ø76,1. Aço ASTM A500 galvanizado a fogo (NBR 6323), pintura a pó nas peças aparentes, parafusos classe 8.8"),
         ("05", "Travamentos", "Terças Ø48,3 e cabos inox Ø8 em X (Casulo) · postes Ø76 estaiados e cabo de borda Ø12 (Safari) · anel de compressão da lanterna e cabos nas faces opacas (Lodge)"),
         ("06", "Membrana externa", "Poliéster/PVC com laca PVDF 1050 g/m² tipo III, classe B1, garantia 15 anos; perfil duplo keder de alumínio; pré-tensão 2,5 kN/m"),
         ("07", "Câmara de ventilação", "60 mm entre membrana e isolamento; entradas no rodapé/beiral e saída no respiro de cumeeira, chaminé ou lanterna"),
         ("08", "Isolamento térmico", "Lã de PET 50 mm, 25 kg/m³, sobre malha de apoio"),
         ("09", "Barreira de condensação", "Manta refletiva de alumínio (bolha) do lado da câmara, emendas fitadas"),
         ("10", "Forro", "Forro tensionado acústico classe M1 (Trevira CS) ou painéis de madeira; forro plano no banho com ático técnico"),
         ("11", "Fechamentos e esquadrias", "Vidro insulado 6 mm laminado + 12 mm argônio + 6 mm temperado low-e em alumínio bronze com ruptura de ponte térmica; painéis SIP 100 mm + ripado termotratado nas faces opacas; portas de correr e pivotante"),
         ("12", "Instalações", "Elétrica 220 V com quadro no ático, fitas LED 2700 K; PEX Ø25 e esgoto Ø100 sob o deck; climatização dutada inverter com difusores lineares; exaustão com recuperador"),
         ("13", "Acabamento e FF&E", "Marcenaria em carvalho, louças e metais, mobiliário, luminárias, enxoval e itens de deck conforme listas de FF&E")]
    trs = "".join(f'<tr><td class="num">{n}</td><td><b>{esc(t)}</b></td><td class="spec">{esc(d)}</td></tr>' for n, t, d in L)
    return page(f'''<h2>ZION SHELL SYSTEM · 13 CAMADAS E MATERIAIS</h2><p class="lede">A mesma sequência construtiva, do solo ao acabamento, nas três unidades. Cada camada é fabricada em oficina e montada em campo sem solda.</p>
<div class="tw"><table class="ffe"><tr><th></th><th>Camada</th><th>Material e especificação</th></tr>{trs}</table></div>
<p class="note">Pré-dimensionamento: bitolas, espessuras e fundações a validar por engenheiro habilitado (ART/RRT) antes da fabricação; form-finding da membrana com o fabricante.</p>''' + foot("Camadas e materiais"))

CSS = """
@font-face{font-family:'Aventa';src:url(assets/aventa.woff2) format('woff2');font-weight:100 900}
@font-face{font-family:'Cormorant Garamond';src:url(assets/cormorant.woff2) format('woff2');font-weight:100 900}
:root{--cream:#FEF5F0;--ink:#1B2117;--earth:#8B714E;--sand:#DED6BF;--black:#040605}
*{box-sizing:border-box} body{margin:0;background:#E9E2D6;font-family:'Aventa','DM Sans',Helvetica,Arial,sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{position:relative;width:297mm;height:210mm;margin:8mm auto;background:var(--cream);padding:12mm 14mm 14mm;overflow:hidden;page-break-after:always;break-after:page}
.page.dark{background:var(--black);color:var(--cream)}
.cover{height:100%;display:flex;flex-direction:column;justify-content:center;padding:0 10mm}
.brand{font-size:56px;font-weight:800;letter-spacing:.4em} .sub{font-size:10px;letter-spacing:.32em;color:var(--sand);margin:6px 0 22mm}
.cover h1{font-weight:200;font-size:44px;letter-spacing:.3em;line-height:1.1;margin:0 0 8mm} .cover .lead{font-size:13px;line-height:1.8;color:var(--sand);max-width:150mm;font-weight:300}
.prods{list-style:none;padding:0;margin:8mm 0;display:grid;grid-template-columns:repeat(5,1fr);gap:6mm} .prods li{border-top:1px solid var(--earth);padding-top:4mm;font-size:10px;color:var(--sand);line-height:1.5} .prods b{display:block;color:var(--cream);letter-spacing:.14em;font-size:11px;margin-bottom:3px;font-weight:600}
.warn{font-size:9px;color:var(--sand);letter-spacing:.06em;margin-top:6mm}
h2{margin:0 0 4mm;font-weight:200;font-size:26px;letter-spacing:.3em} h3{margin:0 0 4mm;font-weight:300;font-size:16px;letter-spacing:.24em} h4{margin:0 0 3mm;font-size:10px;letter-spacing:.24em;color:var(--earth)}
.lede{margin:0 0 5mm;font-size:11px;line-height:1.7;max-width:230mm;font-weight:300}
.foot{position:absolute;left:14mm;right:14mm;bottom:6mm;display:flex;justify-content:space-between;font-size:7.5px;letter-spacing:.22em;color:var(--earth)}
table{border-collapse:collapse;width:100%;font-size:9px;font-variant-numeric:tabular-nums} th{text-align:left;font-weight:600;font-size:7.5px;letter-spacing:.14em;color:var(--earth);text-transform:uppercase;padding:2px 5px 5px;border-bottom:1px solid var(--earth)} td{padding:4px 5px;border-bottom:1px solid var(--sand);vertical-align:top} .num{text-align:right;white-space:nowrap} small{color:var(--earth);font-size:8px}
.note{font-size:8.5px;line-height:1.6;color:var(--earth);margin:4mm 0}
table.ref th{width:14%} table.ref td{width:43%}
.strip5{display:grid;grid-template-columns:repeat(6,1fr);gap:3mm;margin-top:3mm} .strip5 figure{margin:0} .strip5 img,.strip5 .sheet svg{width:100%;height:auto;display:block;aspect-ratio:1.6;object-fit:cover} .strip5 figcaption{font-size:8px;letter-spacing:.2em;margin-top:2mm;color:var(--earth)}
.ph{border-bottom:1px solid var(--ink);padding-bottom:3mm;margin-bottom:5mm} .pname{font-size:24px;font-weight:200;letter-spacing:.32em} .pfam{font-size:9px;letter-spacing:.16em;color:var(--earth);margin-top:3px}
.two{display:grid;grid-template-columns:1.15fr 1fr;gap:8mm} img.hero{width:100%;height:auto;display:block} .thumbs{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;margin-top:3mm} .thumbs img{width:100%;height:auto;display:block}
.kv{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;margin:0;font-size:9.5px;line-height:1.5} .kv dt{color:var(--earth);font-size:7.5px;letter-spacing:.16em;text-transform:uppercase;padding-top:3px;white-space:nowrap} .kv dd{margin:0}
.src{font-size:8px;color:var(--earth);margin-top:4mm;letter-spacing:.06em}
.sheet{background:#FEF5F0;border:1px solid var(--sand);line-height:0} .sheet svg{width:100%;height:auto;display:block} .missing{border:1px dashed var(--earth);padding:10mm;font-size:9px;color:var(--earth)}
.grid4{display:grid;grid-template-columns:1fr 1fr;gap:4mm} .grid2{display:grid;grid-template-columns:1fr 1fr;gap:6mm;align-items:start}
table.ffe td.spec{color:#4A4F44;font-size:8px} table.ffe tr.cat td{background:#F1EAE0;font-weight:600;letter-spacing:.12em;font-size:8px;text-transform:uppercase;color:var(--earth)} table.ffe tr.opt td{color:#8A8A85} table.ffe tr.tot td{font-weight:700;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink);font-size:10px} table.ffe tr.tot2 td{color:var(--earth)}
table.ffe.small{font-size:8px} .cols2{column-count:1}
.notes ol{padding-left:14px;font-size:9px;line-height:1.6;color:#4A4F44;margin:0} .notes{margin-top:6mm}
.page.flow{height:auto;min-height:210mm;overflow:visible;padding-bottom:12mm} .page.flow .foot{position:static;margin-top:6mm} .page.flow tr{break-inside:avoid;page-break-inside:avoid} .page.flow thead{display:table-header-group}
.strip5 img,.strip5 .sheet svg{aspect-ratio:1.6;object-fit:cover}
@media print{@page{size:A4 landscape;margin:0} body{background:#fff} .page{margin:0} .page.flow{padding:12mm 14mm 14mm}}
"""

def build():
    body = cover() + linha()
    for p in PRODUCTS: body += product_pages(p)
    body += camadas() + materiais() + catalogo_itens()
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · Catálogo da Linha · Casulo, Safari, Lodge e Cápsula</title><style>{CSS}</style></head><body>{body}</body></html>'
    open(OUT, "w", encoding="utf-8").write(doc); print(OUT, round(os.path.getsize(OUT) / 1e6, 1), "MB")
    # ---- XLSX FF&E
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter
    wb = Workbook(); wb.remove(wb.active)
    def ws_add(name, headers, rows, widths):
        ws = wb.create_sheet(name[:31]); ws.append(headers)
        for c in range(1, len(headers) + 1):
            ws.cell(1, c).font = Font(bold=True, color="FEF5F0"); ws.cell(1, c).fill = PatternFill("solid", fgColor="1B2117")
        for r in rows: ws.append(r)
        for i, w in enumerate(widths): ws.column_dimensions[get_column_letter(i + 1)].width = w
        ws.freeze_panes = "A2"; return ws
    ws_add("Resumo", ["Unidade", "Família", "Área interna (m²)", "Deck (m²)", "Total (m²)", "Itens de FF&E", "Estágio"],
           [[p["name"], p["family"], round(p["area_int"], 1), round(p["area_ext"], 1), round(p["area_int"] + p["area_ext"], 1), ffe.totals(p["code"], 1)["n_items"], p["status"]] for p in PRODUCTS], [22, 36, 16, 12, 12, 14, 60])
    ws_add("Catálogo de itens", ["Código", "Categoria", "Item", "Especificação", "Unidade"],
           [[c, ffe.CATS[v[4]], v[0], v[1], v[2]] for c, v in sorted(ffe.ITEMS.items(), key=lambda kv: (kv[1][4], kv[0]))], [9, 22, 36, 70, 8])
    for p in PRODUCTS:
        R = ffe.rows(p["code"], 1)
        rows = [[r["code"], r["cat_name"], r["desc"], r["spec"], r["amb"], r["obs"], r["qty"], r["un"], "opcional" if r["optional"] else ""] for r in R]
        ws_add("FFE " + p["name"].replace("ZION ", ""), ["Código", "Categoria", "Item", "Especificação", "Ambiente", "Observação", "Qtd", "Un.", "Opcional"], rows, [9, 20, 34, 60, 16, 30, 7, 6, 10])
    try:
        from product_book_data import bom_priced
        for code, name in (("cocoon", "Casulo"), ("zenith", "Safari"), ("lodge", "Lodge 38"), ("capsule", "Cápsula")):
            rows = []
            for g, items in (capsule_materials() if code == "capsule" else bom_priced(code)):
                for (desc, un, qtd, key) in items: rows.append([g, desc, un, qtd])
            ws_add("Materiais " + name, ["Grupo", "Material / componente", "Un.", "Quantidade estimada"], rows, [26, 70, 8, 18])
    except Exception: pass
    wb.save(XLS); print("xlsx ->", XLS)

if __name__ == "__main__":
    build()

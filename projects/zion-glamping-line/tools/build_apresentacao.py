# -*- coding: utf-8 -*-
"""Apresentação (deck 16:9) do PROJETO ARQUITETÔNICO ZION COCOON & ZION ZENITH no padrão de decks Zion Hotel Group
(fundo preto, texto creme, Aventa, palavras em CAPS espaçadas). Gera ZION_PROJETO_ARQUITETONICO_Apresentacao.html;
o PDF sai com export_pdf.js (uma página 1600 x 900 px por slide).
Uso: python3 build_apresentacao.py"""
import os, html
from build_projeto_arquitetonico import svg_inline
from product_book_data import budget, cocoon_parts, zenith_parts, COCOON_CONNECTIONS, ZENITH_CONNECTIONS
from bom import cocoon_bom, zenith_bom, transport, ASSEMBLY
from pa_sheets import AREAS, ESQUADRIAS

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "ZION_PROJETO_ARQUITETONICO_Apresentacao.html")
NAME = {"cocoon": "ZION COCOON", "zenith": "ZION ZENITH"}
SPLIT = {"cocoon": ("CO", "COON"), "zenith": ("ZE", "NITH")}
slides = []

def money(v): return "R$ " + f"{v:,.0f}".replace(",", ".")
def fmt(v, n=1): return f"{v:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def img(rel, cls=""):
    rel = rel.replace("/renders/web/", "/renders/web/deck/")   # renders sem a interface do visualizador
    return f'<img class="{cls}" src="{rel}" alt="">'
def sheet(rel, cls=""): return f'<div class="sheet {cls}">{svg_inline(rel)}</div>'
def esc(s): return html.escape(s)

def slide(body, cls="", label=""):
    slides.append((body, cls, label))

# ----------------------------------------------------------------------------- slides gerais
def capa():
    slide(f'''<div class="photo full">{img("cocoon/renders/web/cocoon_night.jpg")}</div><div class="overlay"></div>
<div class="cover">
  <div class="eyebrow">ZION GLAMPING COLLECTION · ZION HOTEL GROUP INTERNATIONAL</div>
  <div class="split"><span>PROJETO</span><i></i><span>ARQUITETÔNICO</span></div>
  <div class="sub">ZION COCOON &amp; ZION ZENITH</div>
  <div class="tag">Estudo preliminar de duas unidades proprietárias de hospedagem · 48 pranchas · engenharia peça a peça · 21 arquivos CAD</div>
</div>''', "dark cover-slide", "CAPA")

def linha():
    def col(p, dims, areas, alt, fam):
        return f'''<div class="col">
<div class="pname">{NAME[p]}</div><div class="pfam">{fam}</div>
<div class="photo tall">{img(f"{p}/renders/web/{p}_ext_front.jpg")}</div>
<dl class="kv"><dt>Dimensões</dt><dd>{dims}</dd><dt>Altura</dt><dd>{alt}</dd><dt>Áreas</dt><dd>{areas}</dd></dl></div>'''
    slide(f'''<h2>A LINHA</h2>
<p class="lede">Duas unidades proprietárias, o mesmo sistema construtivo: estrutura tubular em aço galvanizado, membrana PVDF tensionada, isolamento e vidro, sobre deck elevado em estacas helicoidais. Modulares, transportáveis e de baixo impacto.</p>
<div class="two">{col("cocoon", "9,60 x 6,00 m", "48 m² internos · deck 29,9 m² · 78 m²", "4,20 m na cumeeira", "Cabana biomórfica em casulo · 8 arcos elípticos · Espinha de Luz · 6 Janelas Olho")}
{col("zenith", "9,50 x 5,40 m · cobertura 12,90 x 7,40 m", "48,4 m² internos · terraço 28 m² · 79,3 m²", "5,80 m e 4,60 m nos dois cumes", "Cabana escultural de dois cumes · mastros com coroas · Óculo do Zênite · Respiro")}</div>''', "dark", "A LINHA")

def sistema():
    layers = ["Estacas helicoidais galvanizadas", "Grelha de vigas U 150 e cabeçotes ajustáveis", "Módulos de piso: vigotas, PIR 50 mm, compensado naval", "Piso de carvalho de engenharia · porcelanato no banho",
              "Estrutura primária: arcos elípticos (Cocoon) · pilares, anel de beiral e mastros (Zenith)", "Terças, travamentos e cabos de contraventamento", "Perfil duplo keder de alumínio sobre a estrutura",
              "Membrana externa PVDF 1050 g/m² tipo III", "Câmara ventilada 60 mm", "Lã de PET 50 mm + manta refletiva", "Forro tensionado acústico classe M1", "Esquadrias de alumínio RPT bronze com vidro insulado low-e", "Deck de cumaru com fixação oculta e balizadores"]
    li = "".join(f'<li><span class="n">{i + 1:02d}</span>{esc(l)}</li>' for i, l in enumerate(layers))
    slide(f'''<div class="half left"><h2>ZION SHELL SYSTEM</h2><p class="lede">Treze camadas construtivas, do solo à luz. Fabricação em oficina, montagem em campo sem solda, parafusada classe 8.8.</p><ol class="layers">{li}</ol></div>
<div class="half right photo">{img("cocoon/renders/web/cocoon_structure.jpg")}<div class="cap">Estrutura primária do Cocoon: 8 arcos elípticos Ø88,9 x 3,6 sobre trilhos de base</div></div>''', "dark", "SISTEMA CONSTRUTIVO")

# ----------------------------------------------------------------------------- por produto
def produto(p):
    d = f"{p}/desenhos"; j = f"{p}/projeto"; r = f"{p}/renders/web/{p}"
    a, b = SPLIT[p]
    slide(f'''<div class="photo full">{img(f"{r}_ext_aerial.jpg")}</div><div class="overlay"></div>
<div class="divider"><div class="split"><span>ZION</span><i></i><span>{a}{b}</span></div>
<div class="sub">{"Cabana biomórfica em casulo" if p == "cocoon" else "Cabana escultural de dois cumes"}</div></div>''', "dark cover-slide", NAME[p])
    concept = ("Uma concha assimétrica de oito arcos elípticos: frente cheia, aberta ao vale por um anel de vidro inclinado 8°, e cauda afilada que guarda o banho. A Espinha de Luz corre a cumeeira; seis Janelas Olho recortam a membrana como lentes."
               if p == "cocoon" else
               "Dois cumes deslocados em diagonal, 5,80 m sobre a cama e 4,60 m sobre a Ilha do Café, erguidos por mastros com coroas de três braços. A membrana cai em catenárias até sete postes estaiados; o Óculo do Zênite abre o céu sobre o dormir.")
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
    bm = (cocoon_bom if p == "cocoon" else zenith_bom)(); parts = (cocoon_parts if p == "cocoon" else zenith_parts)(); conns = COCOON_CONNECTIONS if p == "cocoon" else ZENITH_CONNECTIONS
    slide(f'''<h2>ESTRUTURA <small>PA-10 planta estrutural · PA-12d estudo da estrutura metálica</small></h2>
<div class="two-sheets">{sheet(f"{d}/03b_planta_estrutural.svg")}{sheet(f"{d}/12_estrutura_isometrica.svg")}</div>
<div class="stats"><div><b>{bm["steel_kg"]:,}</b><span>kg de aço galvanizado</span></div><div><b>{len(parts)}</b><span>famílias de peças codificadas</span></div><div><b>{len(conns)}</b><span>tipos de conexão parafusada</span></div><div><b>{"44" if p == "cocoon" else "30 + 7"}</b><span>estacas helicoidais</span></div></div>'''.replace(",", "."), "dark", NAME[p] + " · ESTRUTURA")
    det = ("detalhes/DET-01_cobertura_cocoon.svg", "detalhes/DET-10_arcos_cocoon.svg") if p == "cocoon" else ("detalhes/DET-02_cobertura_zenith.svg", "detalhes/DET-11_mastros_zenith.svg")
    slide(f'''<h2>DETALHES CONSTRUTIVOS <small>PA-11 · cobertura em camadas · {"arcos e emendas" if p == "cocoon" else "mastros e coroas"} · 1:5 a 1:20</small></h2><div class="two-sheets">{sheet(det[0])}{sheet(det[1])}</div>''', "dark", NAME[p] + " · DETALHES")
    slide(f'''<h2>ISOMÉTRICA E MODELO EXPLODIDO <small>PA-12a · PA-12b</small></h2><div class="two-sheets">{sheet(f"{d}/08_isometrica.svg")}{sheet(f"{d}/10_modelo_explodido.svg")}</div>''', "dark", NAME[p] + " · ISOMÉTRICAS")

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

def orcamento():
    head = '<tr><th></th><th class="num">Econômico</th><th class="num">Zion Standard</th><th class="num">Zion Premium</th></tr>'
    def block(p):
        B = [budget(p, s, 1) for s in range(3)]; B10 = budget(p, 1, 10)
        return f'''<div class="col"><div class="pname">{NAME[p]}</div>
<table class="budget">{head}
<tr><td>Produção do kit (materiais + fabricação)</td>{"".join(f'<td class="num">{money(b["sub_prod"])}</td>' for b in B)}</tr>
<tr><td>Instalação (materiais, mão de obra, transporte, equipamentos, hospedagem)</td>{"".join(f'<td class="num">{money(b["sub_inst"])}</td>' for b in B)}</tr>
<tr><td>Indiretos + contingência</td>{"".join(f'<td class="num">{money(b["indiretos"] + b["conting"])}</td>' for b in B)}</tr>
<tr><td>Engenharia e protótipo (NRE, 1 unidade)</td>{"".join(f'<td class="num">{money(b["nre"])}</td>' for b in B)}</tr>
<tr class="tot"><td>Total por unidade</td>{"".join(f'<td class="num">{money(b["total"])}</td>' for b in B)}</tr>
<tr><td>Custo por m² (área total)</td>{"".join(f'<td class="num">{money(b["por_m2"])}</td>' for b in B)}</tr>
<tr class="tot"><td>Zion Standard em série de 10 unidades</td><td></td><td class="num">{money(B10["total"])}</td><td></td></tr></table></div>'''
    slide(f'''<h2>ORÇAMENTO DE REFERÊNCIA · SANTA CATARINA</h2><p class="lede">Preços de referência set/2026 (materiais e mão de obra com encargos), a confirmar por cotação. Três cenários de acabamento; o NRE é diluído em série.</p>
<div class="two">{block("cocoon")}{block("zenith")}</div>''', "dark", "ORÇAMENTO")

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
    slide('''<div class="closing"><div class="z">Z</div><div class="split"><span>DESENVOLVEMOS</span><i></i><span>DESTINOS</span></div>
<div class="sub">ZION HOTEL GROUP INTERNATIONAL · ZION GLAMPING COLLECTION</div>
<div class="tag">Projeto arquitetônico ZION COCOON &amp; ZION ZENITH · R00 · setembro de 2026 · pranchas, product book, planilha de orçamento e arquivos CAD no repositório</div></div>''', "dark cover-slide", "")

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
.kv{display:grid;grid-template-columns:120px 1fr;gap:10px 18px;margin:0;font-size:14px;line-height:1.6;font-weight:300} .kv dt{color:var(--sand);letter-spacing:.2em;font-size:10px;text-transform:uppercase;padding-top:5px} .kv dd{margin:0}
.half{position:absolute;top:64px;bottom:70px} .half.left{left:80px;width:640px} .half.right{left:780px;right:80px;overflow:hidden} .half.right .cap{position:absolute;left:0;right:0;bottom:0;padding:16px 20px;background:rgba(4,6,5,.7);font-size:11px;letter-spacing:.14em;color:var(--sand);font-weight:300}
ol.layers,ol.next,ol.steps{list-style:none;margin:0;padding:0} ol.layers li{display:flex;gap:16px;font-size:13.5px;line-height:1.5;padding:7px 0;border-bottom:1px solid rgba(222,214,191,.16);font-weight:300} .n{color:var(--earth);font-weight:600;letter-spacing:.1em;font-size:11px;min-width:26px;padding-top:2px}
ol.next li{display:grid;grid-template-columns:30px 1fr;gap:4px 14px;padding:12px 0;border-bottom:1px solid rgba(222,214,191,.16)} ol.next li b{font-weight:500;font-size:15px;letter-spacing:.04em} ol.next li p{grid-column:2;margin:0;font-size:12.5px;line-height:1.6;color:var(--sand);font-weight:300}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;height:520px} .three img{width:100%;height:100%;object-fit:cover;display:block}
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
table.budget td:first-child{color:var(--cream)} table.budget{font-size:12px}
@media print{@page{size:1600px 900px;margin:0} body{background:var(--black)} .slide{margin:0}}
"""

def build():
    capa(); linha(); sistema()
    for p in ("cocoon", "zenith"): produto(p)
    implantacao(); logistica(); orcamento(); proximos(); fim()
    N = len(slides); out = []
    for i, (body, cls, label) in enumerate(slides):
        foot = "" if i in (0, N - 1) else f'<div class="foot"><span>APRESENTAÇÃO · PROJETO ARQUITETÔNICO</span><span>ZION HOTEL · GROUP INTERNATIONAL{" · " + esc(label) if label else ""}</span><span>2026 · {i + 1:02d} / {N:02d}</span></div>'
        out.append(f'<section class="slide {cls}">{body}{foot}</section>')
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · Projeto Arquitetônico · Apresentação</title><style>{CSS}</style></head><body>{"".join(out)}</body></html>'
    open(OUT, "w", encoding="utf-8").write(doc)
    print(OUT, N, "slides", round(os.path.getsize(OUT) / 1e6, 1), "MB")

if __name__ == "__main__":
    build()

# -*- coding: utf-8 -*-
"""ZC-INT-001 · PROJETO DE INTERIORES DO ZION CASULO com marcenaria acoplada: memorial de interiores, as seis pranchas IN-01 a IN-06,
quadros de marcenaria (MA), mobiliário solto (MS), acabamentos e a lista de FF&E do Casulo. Sem preços. A4 paisagem.
Saída: 04_INTERIORES/ZC-INT-001_Projeto_Interiores_Casulo.html · PDF via export_pdf.js"""
import os, html
from build_projeto_arquitetonico import svg_inline
from svgkit import zion_mark_html, zion_logo_html, fmt as mfmt
from interiores_cocoon import MA, MS, ACAB
import ffe

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(ROOT, "04_INTERIORES"); os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "ZC-INT-001_Projeto_Interiores_Casulo.html")
DOC = "ZC-INT-001"; REV = "REV 00 — CONCEITO"; DATE = "17/09/2026"
SHEETS = [("IN-01", "Planta de layout de interiores", "1:50", "cocoon/interiores/IN-01_planta_interiores.svg"), ("IN-02", "Paginação de pisos e quadro de acabamentos", "1:50", "cocoon/interiores/IN-02_pisos_acabamentos.svg"),
          ("IN-03", "Elevações internas A (cabeceira) e B (lateral esquerda)", "1:40", "cocoon/interiores/IN-03_elevacoes_A_B.svg"), ("IN-04", "Elevações internas C (banho) e D (fachada interna)", "1:40", "cocoon/interiores/IN-04_elevacoes_C_D.svg"),
          ("IN-05", "Detalhes da marcenaria acoplada", "1:20 / 1:15", "cocoon/interiores/IN-05_detalhes_marcenaria.svg"), ("IN-06", "Quadro de mobiliário e marcenaria", "s/ escala", "cocoon/interiores/IN-06_quadro_mobiliario.svg")]

def esc(s): return html.escape(str(s))
def sheet(rel): return f'<div class="sheet">{svg_inline(rel)}</div>'
def img(rel): return f'<img src="../{rel.replace("/renders/web/", "/renders/web/deck/")}" alt="">' if os.path.exists(os.path.join(ROOT, rel)) else ""
def table(head, rows, cls=""):
    th = "".join(f"<th{' class=num' if h.startswith('#') else ''}>{esc(h.lstrip('#'))}</th>" for h in head)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="t {cls}"><tr>{th}</tr>{body}</table>'
pages = []
def page(body, label, code="", cls=""):
    n = len(pages) + 1
    pages.append(f'<section class="page {cls}"><div class="head"><span>{zion_mark_html("14px", color="#1B2117")} ZION GLAMPING · {DOC} · {REV}</span><span>{esc(code)}</span><span>{esc(label)}</span></div>{body}<div class="foot"><span>ZION CASULO · PROJETO DE INTERIORES · MARCENARIA ACOPLADA · SEM PREÇOS</span><span>UNIDADE: m</span><span>{DATE} · {n:02d}</span></div></section>')
def h(t, sub=""): return f'<h2>{esc(t)}{f"<small>{esc(sub)}</small>" if sub else ""}</h2>'

def capa():
    pages.append(f'''<section class="page cover"><div class="coverbox"><div class="brand">{zion_mark_html("13mm", color="#FEF5F0", style="margin-right:6mm")}{zion_logo_html("13mm", color="#FEF5F0")}</div><div class="sub">ZION GLAMPING COLLECTION · CABIN DESIGN &amp; ENGINEERING SYSTEM</div>
<h1>PROJETO DE<br>INTERIORES</h1><h3>ZION CASULO · MARCENARIA ACOPLADA · {DOC} · {REV} · {DATE}</h3>
<p class="lead">Plano arquitetônico de interiores do Zion Casulo com o mobiliário fixo já acoplado à concha e à parede do banho: planta de layout cotada, paginação de pisos, elevações internas, detalhes da marcenaria e quadros de mobiliário, acabamentos e FF&amp;E. A marcenaria acoplada (MA) é fabricada, montada e acabada em fábrica junto com a cabana; o mobiliário solto (MS) é o FF&amp;E entregue montado.</p>
<p class="rule">Anexo do documento técnico ZG-TEC-001 (seção 25). Sem preços. Dimensões em metros; tolerância de fabricação ± 3 mm; conferência com o gabarito da seção da concha antes da produção.</p></div></section>''')

def memorial():
    body = h("MEMORIAL DE INTERIORES", "conceito, regras de acoplamento, materiais e luz") + f'''<div class="two"><div>
<p class="lede">O interior do Casulo é um único eixo: vestíbulo, estar, suíte e banho na cauda. A marcenaria acoplada faz a divisão dos ambientes sem paredes: a mini cozinha (geladeira, forno, cooktop de indução de 2 bocas, cuba e air fryer) e o armário baixo se encostam na curva da concha do lado esquerdo, a cabeceira estofada com criados suspensos se fixa à parede do banho, e a bancada em pedra ocupa o lado do banho da mesma parede. Tudo o que é fixo nasce na fábrica com a cabana; o que é solto (cama, chaise, poltrona, mesa lateral, luminárias, tapetes) é o FF&amp;E Zion New Luxury.</p>
<h4>REGRAS DE ACOPLAMENTO</h4><ol class="num">
<li>Fixação sempre à estrutura (arcos e trilhos de base) por cantoneiras galvanizadas; nunca à membrana nem ao forro.</li><li>Fundos e laterais recortados com o gabarito da seção da concha, folga de 15 mm fechada com perfil de EPDM.</li>
<li>Rodapé técnico removível de 150 mm em todo o perímetro: eletrodutos, PEX e caixas de passagem acessíveis sem desmontar móveis.</li><li>Elétrica embutida na marcenaria (tomadas, USB, LED) com ponto de conexão no rodapé técnico.</li>
<li>Peças de até 1,40 m para caber no contêiner e passar pela porta PV1 (1,00 x 2,40); montagem em campo só por nivelamento e fixação.</li><li>Materiais naturais e reparáveis: carvalho em lâmina sobre MDF naval, ripado termotratado, quartzito, linho, latão escovado.</li></ol>
<h4>LUZ POR AMBIENTE</h4><p class="small">Estar: fita LED na prateleira da ilha e no rodapé técnico, luminária de piso e de mesa, cena "chegada" a 60 %. Suíte: retroiluminação da cabeceira, arandelas de leitura articuladas, cena "noite" a 10 %, tela da Espinha de Luz. Banho: espelho com LED perimetral, fita sob o gabinete suspenso, luz de vigília no rodapé. Tudo 2700 K, dimerizável, sem pendentes.</p></div>
<div><h4>MATERIAIS</h4>{table(["Elemento", "Material e acabamento"], [["Marcenaria (MA)", "carvalho natural em lâmina sobre MDF naval 18 mm · verniz PU fosco"], ["Ripados", "pinus termotratado 20 x 40 mm, fixação oculta, mesmo tom do carvalho"], ["Pedras", "quartzito 30 mm bordas retas polidas (ilha, armário, bancada, prateleira da banheira)"], ["Estofados", "linho natural cru (cabeceira), bouclé antimancha (chaise, poltrona)"], ["Metais", "latão escovado: misturadores, puxadores, arandelas, soleiras"], ["Pisos", "carvalho de engenharia 14 mm · porcelanato 60 x 120 areia clara · cumaru no deck"], ["Têxteis", "tapetes de lã tecidos à mão, cortinas de linho + blackout, enxoval 400 fios"]], "small")}
<div class="strip"><div>{img("cocoon/renders/web/cocoon_int_living.jpg")}</div><div>{img("cocoon/renders/web/cocoon_int_bed.jpg")}</div><div>{img("cocoon/renders/web/cocoon_int_bath.jpg")}</div></div></div></div>'''
    page(body, "Memorial de interiores", code="ZC-INT-001")

def sheet_pages():
    for code, t, sc, rel in SHEETS:
        n = len(pages) + 1
        pages.append(f'<section class="page sheetpage"><div class="strip2"><span class="code">{code}</span><span class="ttl">{esc(t)}</span><span class="scl">{sc}</span><span class="prod">ZION CASULO</span></div>{sheet(rel)}<div class="foot"><span>ZION GLAMPING · {DOC} · {REV} · {code}</span><span>{esc(t)}</span><span>{DATE} · {n:02d}</span></div></section>')

def quadros():
    rows = []
    for m in MA:
        dims = f"{mfmt(m['x2'] - m['x1'])} x {mfmt(m['y2'] - m['y1']) if m['y2'] != m['y1'] else '—'} x h {mfmt(m['h'])}" if m["cod"] not in ("MA-07", "MA-08") else ("8,50 m x h 0,15" if m["cod"] == "MA-07" else "0,60 x 0,60")
        rows.append([f"<b>{m['cod']}</b>", esc(m["nome"]), dims, esc(m["amb"]), esc(m["ffe"]), esc(m["desc"]), esc(m["mat"])])
    rows2 = [[f"<b>{m['cod']}</b>", esc(m["nome"]), esc(m["dims"]), esc(m["amb"]), esc(m["ffe"]), esc(m["pos"])] for m in MS]
    page(h("QUADRO DE MARCENARIA ACOPLADA E MOBILIÁRIO SOLTO", "MA fabricado com a cabana · MS entregue montado (FF&E)") + table(["Cód.", "Peça", "Dimensões (m)", "Amb.", "FF&E", "Descrição", "Materiais"], rows, "small") + "<h4>MOBILIÁRIO SOLTO</h4>" + table(["Cód.", "Peça", "Dimensões (m)", "Amb.", "FF&E", "Posição"], rows2, "small"), "Quadros MA e MS", code="ZC-INT-006", cls="flow")
    ac = [[f"<b>{a}</b>", b, c, d, e, f] for a, b, c, d, e, f in ACAB]
    R = ffe.rows("cocoon", 1)
    fr = [[r["code"], esc(r["desc"]), esc(r["spec"]), esc(r["amb"]), mfmt(r["qty"]) if isinstance(r["qty"], float) else r["qty"], r["un"], esc(r["obs"]) + (" · opcional" if r["optional"] else "")] for r in R]
    page(h("QUADRO DE ACABAMENTOS E LISTA DE FF&E DO CASULO", f"{len(R)} itens Zion New Luxury · sem preços") + table(["Ambiente", "Piso", "Rodapé", "Paredes", "Forro", "Marcenaria"], ac, "small") + "<h4>FF&E · TUDO O QUE VAI DENTRO</h4>" + table(["Cód.", "Item", "Especificação", "Ambiente", "#Qtd", "Un.", "Obs."], fr, "xsmall"), "Acabamentos e FF&E", code="ZC-INT-007", cls="flow")
    nxt = [["Safari (ZS)", "cabeceira acoplada ao totem do mastro M2, Ilha do Café como peça central, closet em L, bancada dupla"], ["Lodge 38 (ZL)", "parede-corda ripada como cabeceira, closet e café nas faces opacas, bancada e banheira de sentar"], ["Lodge 24 e 28", "versões compactas: café/closet em uma face opaca, cabeceira na parede do banho"], ["Cápsula (ZK)", "marcenaria curva acoplada aos anéis: cabeceira na parede do banho, café e closet nas laterais, bancada no técnico"]]
    page(h("PRÓXIMAS CABANAS", "a mesma lógica de marcenaria acoplada aplicada às outras cinco unidades") + table(["Unidade", "Programa de marcenaria acoplada previsto"], nxt, "small") + '<p class="lede">Cada unidade receberá o mesmo conjunto: planta de layout de interiores, paginação, elevações internas, detalhes de marcenaria e quadros (IN-01 a IN-06), com códigos ZS-INT, ZL-INT, ZL24-INT, ZL28-INT e ZK-INT.</p>' +
         table(["Rev", "Data", "Descrição", "Autor"], [["00", DATE, "Conceito · emissão inicial do projeto de interiores do Casulo com marcenaria acoplada", "Zion Cabin Design System"]], "small"), "Próximas cabanas · revisão", code="ZC-INT-008")

CSS = """
@font-face{font-family:'Aventa';src:url(../assets/aventa.woff2) format('woff2');font-weight:100 900;font-display:swap}
:root{--cream:#FEF5F0;--ink:#1B2117;--earth:#8B714E;--sand:#DED6BF;--black:#040605}
*{box-sizing:border-box} body{margin:0;background:#E9E2D6;font-family:'Aventa','DM Sans',Helvetica,Arial,sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{position:relative;width:297mm;height:210mm;margin:0 auto 8mm;background:var(--cream);padding:11mm 13mm 14mm;page-break-after:always;break-after:page;overflow:hidden}
.page.flow{height:auto;min-height:210mm;overflow:visible} .page.flow .foot{position:static;margin-top:10mm} table.t tr{page-break-inside:avoid}
.page.cover{background:var(--black);color:var(--cream);padding:0} .coverbox{position:absolute;inset:0;padding:22mm 26mm;display:flex;flex-direction:column;justify-content:center}
.brand{font-size:44px;font-weight:800;letter-spacing:.4em;display:flex;align-items:center} .sub{font-size:9px;letter-spacing:.3em;color:var(--sand);margin:6px 0 22mm}
.cover h1{font-size:46px;font-weight:200;letter-spacing:.22em;line-height:1.05;margin:0 0 10px} .cover h3{font-size:11px;letter-spacing:.3em;font-weight:300;color:var(--sand);margin:0 0 16px} .cover .lead{font-size:12px;line-height:1.8;font-weight:300;max-width:200mm;margin:0 0 14px} .cover .rule{font-size:9.5px;line-height:1.7;color:var(--sand);max-width:220mm;border-top:1px solid var(--sand);padding-top:10px}
.head{display:flex;justify-content:space-between;font-size:7.5px;letter-spacing:.22em;color:var(--earth);border-bottom:1px solid var(--sand);padding-bottom:4px;margin-bottom:8px;text-transform:uppercase} .head span:first-child{display:flex;align-items:center;gap:6px}
.foot{position:absolute;left:13mm;right:13mm;bottom:5mm;display:flex;justify-content:space-between;font-size:7px;letter-spacing:.2em;color:var(--earth)} .foot span:nth-child(2){flex:1;text-align:center}
h2{margin:0 0 8px;font-weight:300;font-size:16px;letter-spacing:.26em;text-transform:uppercase;line-height:1.15} h2 small{display:block;font-size:8.5px;letter-spacing:.14em;color:var(--earth);margin-top:4px;text-transform:none;font-weight:300}
h4{margin:10px 0 4px;font-size:8.5px;letter-spacing:.26em;color:var(--earth);font-weight:600} .lede{font-size:10.5px;line-height:1.75;margin:6px 0} .small{font-size:9.5px;line-height:1.65}
table.t{border-collapse:collapse;width:100%;font-size:9px;line-height:1.4;margin:4px 0 8px} table.t th{text-align:left;font-weight:600;font-size:7.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--earth);padding:3px 5px;border-bottom:1px solid var(--ink)} table.t td{padding:3px 5px;border-bottom:1px solid var(--sand);vertical-align:top} .num{text-align:right;white-space:nowrap}
table.t.small{font-size:8.4px} table.t.xsmall{font-size:7.4px;line-height:1.3} table.t.xsmall td{padding:2px 3px}
.two{display:grid;grid-template-columns:1.15fr 1fr;gap:18px;align-items:start} ol.num{margin:0;padding-left:16px;font-size:9.5px;line-height:1.65}
.sheet{background:#FEF5F0;border:1px solid var(--sand);line-height:0} .sheet svg{width:100%;height:auto;display:block}
.sheetpage{padding:8mm 10mm 12mm} .sheetpage .sheet{border:1px solid var(--ink)} .strip2{display:flex;gap:16px;align-items:baseline;font-size:8px;letter-spacing:.2em;color:var(--earth);text-transform:uppercase;margin-bottom:5px} .strip2 .code{font-weight:700;color:var(--ink)} .strip2 .ttl{flex:1;color:var(--ink)}
.strip{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:10px} .strip div{height:40mm;overflow:hidden;background:#1B2117} .strip img{width:100%;height:100%;object-fit:cover;display:block}
@media print{@page{size:A4 landscape;margin:0} body{background:#fff} .page{margin:0} .page.flow{height:auto}}
"""

def build():
    capa(); memorial(); sheet_pages(); quadros()
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · {DOC} · Projeto de Interiores do Casulo</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    open(OUT, "w", encoding="utf-8").write(doc); print(OUT, len(pages), "páginas")

if __name__ == "__main__":
    build()

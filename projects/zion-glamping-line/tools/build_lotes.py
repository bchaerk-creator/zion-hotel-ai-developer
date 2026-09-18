# -*- coding: utf-8 -*-
"""LOTES · documentos de contratação por modelo e por lote, master plan único e one-pager.
Para cada um dos 4 modelos (Casulo ZC, Safari ZS, Lodge 38 ZL, Cápsula ZK):
  <TAG>-LOT1-001  Deck e infraestrutura (fundação, grelha, piso, deck, instalações)
  <TAG>-LOT2-001  Estrutura metálica (para o serralheiro no Brasil: peça a peça, gabaritos, galvanização, embalagem)
  <TAG>-LOT3-001  Lonas, revestimentos e vidros (padrões de corte, fixação nos ferros, forro, isolamento, esquadrias)
  <TAG>-LOT4-001  Mobílias (marcenaria acoplada, FF&E, equipamentos)
Mais: ZG-MP-001 Master Plan (integração, modularidade para montanha, cronograma, interfaces, riscos + os 16 lotes anexados)
e ZG-ONE-001 One-pager. Sem preços. A4 paisagem. Saída em 06_LOTES/. PDFs via export_pdf.js."""
import os, html, math, sys
from build_projeto_arquitetonico import svg_inline
from build_tecnico import CSS as BASE_CSS
from pa_sheets import ESQUADRIAS, AREAS
from svgkit import zion_mark_html, zion_logo_html
import bom as B, product_book_data as P, ffe, lona, drawings_extra as DX
from geometry import Cocoon, Zenith, Lodge, Capsule
from capsule import capsule_materials
from interiores_cocoon import MA, MS

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(ROOT, "06_LOTES"); os.makedirs(OUT_DIR, exist_ok=True)
DATE = "17/09/2026"; REV = "REV 00 — CONCEITO"
WARN = '<span class="warn">⚠️ VALIDAÇÃO OBRIGATÓRIA — ENGENHEIRO/ARQUITETO</span>'
COTAR = '<span class="cotar">PREÇO A COTAR</span>'
CO, ZE, LD, CA = Cocoon(), Zenith(), Lodge(), Capsule()

def esc(s): return html.escape(str(s))
def fmt(v, n=1):
    if isinstance(v, str): return esc(v)
    return f"{v:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def q(v):
    if isinstance(v, float): return fmt(v, 2).rstrip("0").rstrip(",")
    return str(v)
def exists(rel): return os.path.exists(os.path.join(ROOT, rel))
def sheet(rel): return f'<div class="sheet">{svg_inline(rel)}</div>' if exists(rel) else f'<div class="missing">[{esc(rel)}]</div>'
def img(rel): return f'<img src="../{rel.replace("/renders/web/", "/renders/web/deck/")}" alt="">' if exists(rel) else ""
def table(head, rows, cls=""):
    th = "".join(f"<th{' class=num' if h.startswith('#') else ''}>{esc(h.lstrip('#'))}</th>" for h in head)
    body = "".join("<tr>" + "".join(f"<td{' class=num' if isinstance(c, (int, float)) else ''}>{q(c) if isinstance(c, (int, float)) else c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="t {cls}"><tr>{th}</tr>{body}</table>'
def kv(items): return '<dl class="kv">' + "".join(f"<dt>{esc(k)}</dt><dd>{v}</dd>" for k, v in items) + "</dl>"
def h(t, sub=""): return f'<h2>{esc(t)}{f"<small>{esc(sub)}</small>" if sub else ""}</h2>'
def ul(items): return '<ul class="chk">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def ol(items): return '<ol class="num">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"

# =============================================================================== dados por modelo
def cap_manual():
    S = []
    def step(n, t, equipe, ferr, equip, tempo, riscos, check): S.append(dict(n=n, titulo=t, equipe=equipe, ferramentas=ferr, equipamentos=equip, tempo=tempo, riscos=riscos, checklist=check))
    step(1, "Preparação e marcação do terreno", "Líder + 2 montadores", "Nível a laser, trena, estacas, linha", "Roçadeira", "3 h", "Acesso do caminhão-prancha até 30 m do ponto de pouso", ["4 pontos dos pés locados ± 20 mm", "Cota de referência definida", "Acesso e área de manobra confirmados"])
    step(2, "Fundação dos pés (4 estacas helicoidais ou 4 sapatas pré-moldadas)", "Operador + 2 montadores", "Chave de torque, nível", "Motor de cravação ou mini-escavadeira", "0,5 dia", "Solo com rocha rasa: usar sapata pré-moldada 60 x 60", ["Torque registrado / sapatas niveladas ± 5 mm", "Cabeçotes ou chumbadores prontos"])
    step(3, "Transporte e pouso da cápsula", "Líder + motorista + 3 montadores", "Cintas 3 t, manilhas, cordas guia", "Caminhão-prancha 9 m + munck 8 t (ou guincho e trilhos em sítios sem munck)", "0,5 dia", "Pouso com vento > 25 km/h; olhais de içamento não conferidos", ["4 olhais inspecionados", "Pés telescópicos travados no curso", "Nivelamento ± 5 mm no piso interno"])
    step(4, "Ligações de instalações", "Eletricista + encanador", "Ferramentas de crimpagem e teste", "", "0,5 dia", "Conexões rápidas sem teste de estanqueidade", ["Água, esgoto e energia conectados nos engates rápidos da cauda", "DR e aterramento testados", "Teste de pressão 6 bar / 30 min"])
    step(5, "Deck frontal e escada", "2 carpinteiros", "Parafusadeira, nível", "", "0,5 dia", "", ["4 módulos de deck nivelados", "Escada fixada", "Guarda-corpo em cabo"])
    step(6, "Vistoria e entrega", "Líder + operador", "Câmera, termômetro, tensiômetro", "", "3 h", "", ["Climatização testada em carga", "Teste de chuva no Visor e no Anel de Luz", "As-built e manual entregues"])
    return S

def cap_transport():
    return [("Cápsula completa (casca, piso, marcenaria, instalações)", "8,40 x 3,20 x 3,20 m", 86.0, 4200), ("Módulos do deck + escada + guarda-corpo (palete)", "2,6 x 1,2 x 0,8 m", 2.5, 420), ("Pés telescópicos, sapatas / estacas, chumbadores (feixe)", "2,0 x 0,6 x 0,5 m", 0.6, 380), ("FF&E e enxoval (dentro da cápsula)", "—", 0.0, 350)]

CAP_ESQ = [("VS1", "Visor: calota de vidro laminado curvo em 5 gomos", 3.20, 3.20, 1, "Laminado curvo 8 + 8 mm low-e, calandrado; juntas verticais em -0,95 / -0,45 / +0,45 / +0,95; alumínio anodizado bronze", "Calota frontal (x 0 a 1,20)"),
           ("PV1", "Porta pivotante do Visor", 0.90, 2.05, 1, "Vidro laminado 10 + 10, pivô de piso, fechadura digital", "Gomo central do Visor"),
           ("AL1", "Anel de Luz: faixa de vidro curvo em 3 gomos", 0.45, 3.60, 1, "Laminado curvo 6 + 6 com controle solar, ± 65° do zênite", "x 3,95 a 4,40, sobre a cama"),
           ("OL1", "Olho da suíte Ø0,60", 0.60, 0.60, 1, "Vidro insulado circular, aro de alumínio", "x 3,35, lado esquerdo, z 1,35"),
           ("OL2", "Olho do banho Ø0,50", 0.50, 0.50, 1, "Vidro insulado acidado, aro de alumínio", "x 6,35, lado direito, z 1,60")]

def cap_parts():
    grp = dict(capsule_materials())["Estrutura monocoque (aço galvanizado a fogo)"]
    return [dict(cod=f"K{i + 1:02d}", nome=d, qtd=qn, comp="", larg="", alt="", perfil="", aco="aço galv.", esp="", peso_un="", peso_total="", fab="ver nota", uniao="parafusada M10/M12", ordem=i + 1, funcao=un) for i, (d, un, qn, key) in enumerate(grp)]

MODELS = {
    "cocoon": dict(name="ZION CASULO", tag="ZC", family="Cabana biomórfica em casulo", dims="9,60 x 6,00 x 4,20 m · Bico em balanço 2,40 m", area_int=48.0, area_ext=29.9, days=12, guests="2 + 1", cat="SIGNATURE",
                   hero="cocoon/renders/web/cocoon_ext_front.jpg", parts=P.cocoon_parts, bom=B.cocoon_bom, piles=DX.cocoon_pile_grid, manual=lambda: P.manual("cocoon"), transport=lambda: B.transport(B.cocoon_bom(), "cocoon"), esq=ESQUADRIAS["cocoon"],
                   lot1=["cocoon/desenhos/03b_planta_estrutural.svg", "detalhes/DET-04_fundacao.svg", "detalhes/DET-03_ancoragem.svg", "detalhes/DET-06_drenagem.svg", "detalhes/DET-08_hidraulica.svg", "detalhes/DET-07_eletrica.svg", "detalhes/DET-09_climatizacao.svg"],
                   lot2=["cocoon/desenhos/12_estrutura_isometrica.svg", "cocoon/desenhos/03b_planta_estrutural.svg", "detalhes/DET-10_arcos_cocoon.svg", "cocoon/desenhos/10_modelo_explodido.svg"],
                   lot3=["detalhes/DET-01_cobertura_cocoon.svg", "cocoon/desenhos/13_camadas_construtivas.svg", "detalhes/DET-05_esquadrias.svg", "cocoon/projeto/PA-09_quadro_esquadrias.svg", "cocoon/projeto/PA-04_planta_cobertura.svg"],
                   lot4=["cocoon/interiores/IN-01_planta_interiores.svg", "cocoon/interiores/IN-03_elevacoes_A_B.svg", "cocoon/interiores/IN-05_detalhes_marcenaria.svg", "cocoon/interiores/IN-06_quadro_mobiliario.svg"],
                   struct_prefix="BCDE", base_prefix="AF", geo=CO),
    "zenith": dict(name="ZION SAFARI", tag="ZS", family="Cabana escultural de dois cumes", dims="9,50 x 5,40 m · cobertura 12,90 x 7,40 · cumes 5,80 / 4,60 m", area_int=48.4, area_ext=28.0, days=15, guests="2 + 1", cat="SIGNATURE",
                   hero="zenith/renders/web/zenith_ext_front.jpg", parts=P.zenith_parts, bom=B.zenith_bom, piles=DX.zenith_pile_grid, manual=lambda: P.manual("zenith"), transport=lambda: B.transport(B.zenith_bom(), "zenith"), esq=ESQUADRIAS["zenith"],
                   lot1=["zenith/desenhos/03b_planta_estrutural.svg", "detalhes/DET-04_fundacao.svg", "detalhes/DET-03_ancoragem.svg", "detalhes/DET-06_drenagem.svg", "detalhes/DET-08_hidraulica.svg", "detalhes/DET-07_eletrica.svg", "detalhes/DET-09_climatizacao.svg"],
                   lot2=["zenith/desenhos/12_estrutura_isometrica.svg", "zenith/desenhos/03b_planta_estrutural.svg", "detalhes/DET-11_mastros_zenith.svg", "zenith/desenhos/10_modelo_explodido.svg"],
                   lot3=["detalhes/DET-02_cobertura_zenith.svg", "zenith/desenhos/13_camadas_construtivas.svg", "detalhes/DET-05_esquadrias.svg", "zenith/projeto/PA-09_quadro_esquadrias.svg", "zenith/projeto/PA-04_planta_cobertura.svg"],
                   lot4=["zenith/desenhos/02_planta_humanizada.svg"], struct_prefix="BCDE", base_prefix="AF", geo=ZE),
    "lodge": dict(name="ZION LODGE 38", tag="ZL", family="Pavilhão octogonal com Lanterna Zion", dims="octógono 6,80 m entre faces · beiral 2,70 · lanterna 5,20 m", area_int=LD.floor_area(), area_ext=LD.deck_area(), days=9, guests="2 + 1", cat="PREMIUM",
                  hero="lodge/renders/web/lodge_ext_front.jpg", parts=P.lodge_parts, bom=B.lodge_bom, piles=LD.piles, manual=lambda: P.manual("lodge"), transport=lambda: B.transport(B.lodge_bom(), "lodge"), esq=ESQUADRIAS["lodge"],
                  lot1=["lodge/desenhos/03b_planta_estrutural.svg", "detalhes/DET-04_fundacao.svg", "detalhes/DET-03_ancoragem.svg", "detalhes/DET-06_drenagem.svg", "detalhes/DET-08_hidraulica.svg", "detalhes/DET-07_eletrica.svg"],
                  lot2=["lodge/desenhos/12_estrutura_isometrica.svg", "lodge/desenhos/03b_planta_estrutural.svg", "detalhes/DET-12_lanterna_lodge.svg", "detalhes/DET-13_caibros_lodge.svg", "lodge/desenhos/10_modelo_explodido.svg"],
                  lot3=["lodge/desenhos/13_camadas_construtivas.svg", "lodge/projeto/PA-09_quadro_esquadrias.svg", "lodge/projeto/PA-04_planta_cobertura.svg"],
                  lot4=["lodge/desenhos/02_planta_humanizada.svg"], struct_prefix="BCDEFGHI", base_prefix="AJ", geo=LD),
    "capsule": dict(name="ZION CÁPSULA", tag="ZK", family="Cápsula monocoque transportável", dims="8,40 x 3,20 x 3,20 m", area_int=CA.floor_area(), area_ext=CA.deck_area(), days=3, guests="2", cat="PREMIUM",
                    hero="capsule/desenhos/08_isometrica.svg", parts=cap_parts, bom=None, piles=lambda: CA.LEGS, manual=cap_manual, transport=cap_transport, esq=CAP_ESQ,
                    lot1=["capsule/desenhos/01_conceito.svg", "detalhes/DET-04_fundacao.svg"], lot2=["capsule/desenhos/08_isometrica.svg", "capsule/desenhos/01_conceito.svg"], lot3=["capsule/desenhos/01_conceito.svg"], lot4=["capsule/desenhos/01_conceito.svg"],
                    struct_prefix="K", base_prefix="", geo=CA),
}
LOTS = {1: ("DECK E INFRAESTRUTURA", "Fundação, grelha do piso, módulos de piso, deck, instalações hidráulica, elétrica e climatização"),
        2: ("ESTRUTURA METÁLICA", "Arcos, mastros, pilares, anéis, terças, cabos, chapas e conexões, galvanização: para o serralheiro no Brasil"),
        3: ("LONAS, REVESTIMENTOS E VIDROS", "Lona externa com padrões de corte, forro interno, isolamento, fixação nos ferros, esquadrias e vidros"),
        4: ("MOBÍLIAS", "Marcenaria acoplada, mobiliário solto, equipamentos, enxoval e OS&E")}

MODULAR = [
    ("Transporte", "Tudo o que chega ao sítio cabe num caminhão 3/4 (caçamba 4,8 x 2,2 m) e, do último ponto de estrada, numa picape 4x4 ou carreta agrícola: nenhuma peça > 4,80 m; volumes ≤ 2,4 x 1,2 x 1,2 m; a Cápsula é a exceção (viaja inteira em prancha) e exige acesso de caminhão até 30 m do pouso."),
    ("Peso", "Peça ≤ 60 kg = 2 pessoas; ≤ 120 kg = 4 pessoas ou tripé com talha 1 t; nada exige guindaste. Vidro ≤ 90 kg por pano (ventosas, 4 pessoas)."),
    ("Sem concreto e sem solda em campo", "Fundação em estacas helicoidais cravadas com motor hidráulico portátil (ou sapatas pré-moldadas onde há rocha); todas as ligações parafusadas classe 8.8 galvanizadas; galvanização a fogo em fábrica."),
    ("Kit numerado", "Cada peça leva etiqueta com código do projeto (ex.: ZC-B03-C), peso e posição; cada estrado traz a lista de conteúdo; a montagem segue a sequência A → B → C → D → E das listas."),
    ("Ferramenta mínima", "Torquímetros 20-250 N·m, chaves 19/24 mm, nível a laser, estação total ou trena a laser, tripé com talha, esticadores, puxador de keder, soprador térmico, parafusadeira. Gerador 5 kVA para o sítio."),
    ("Reversível", "A unidade desmonta na ordem inversa e sai do sítio sem deixar fundação: estacas removidas, solo recomposto."),
    ("Clima de montanha", "Vento: suspender içamentos e lona acima de 30 km/h; membrana e cabos tensionados com pré-tensão medida; drenagem para o terreno inclinado; isolamento e água quente dimensionados para 0 °C; cabeçotes ajustáveis absorvem declive até 15 % (ver DET-04)."),
    ("Interfaces travadas", "Cada lote entrega ao seguinte uma geometria conferida (planilha de as-built): fundação ± 30 mm → grelha ± 10 mm → estrutura ± 15 mm no topo → lona sem rugas → marcenaria com gabarito."),
]

# =============================================================================== documento
class Doc:
    def __init__(self, code, title, model=None):
        self.code, self.title, self.model = code, title, model
        self.pages = []; self.toc = []
    def page(self, body, label="", cls="", code=""):
        n = len(self.pages) + 1
        if label and not cls.startswith("sheetpage"): self.toc.append((code or self.code, label, n))
        m = MODELS[self.model]["name"] if self.model else "ZION GLAMPING COLLECTION"
        self.pages.append(f'<section class="page {cls}"><div class="head"><span>{zion_mark_html("14px", color="#1B2117")} {m} · {self.code} · {REV}</span><span>{esc(code or self.code)}</span><span>{esc(label)}</span></div>{body}<div class="foot"><span>ZION GLAMPING COLLECTION · {esc(self.title)} · SEM PREÇOS</span><span>UNIDADE: m salvo indicação</span><span>{DATE} · {n:02d}</span></div></section>')
    def sheet_page(self, rel, code, title, scale="", note=""):
        n = len(self.pages) + 1
        self.pages.append(f'<section class="page sheetpage"><div class="strip"><span class="code">{esc(code)}</span><span class="ttl">{esc(title)}</span><span class="scl">{esc(scale)}</span><span class="prod">{esc(note)}</span></div>{sheet(rel)}<div class="foot"><span>{esc(self.code)} · {REV} · {esc(code)}</span><span>{esc(title)}</span><span>{DATE} · {n:02d}</span></div></section>')
    def cover(self, kicker, h1, lead, extra=""):
        self.pages.append(f'''<section class="page cover"><div class="coverbox"><div class="brand">{zion_mark_html("13mm", color="#FEF5F0", style="margin-right:6mm")}{zion_logo_html("13mm", color="#FEF5F0")}</div><div class="sub">ZION GLAMPING COLLECTION · {esc(kicker)}</div>
<h1>{h1}</h1><h3>{esc(self.code)} · {REV} · {DATE}</h3><p class="lead">{lead}</p>{extra}
<p class="rule">Documento de contratação e fabricação. Nenhuma especificação que dependa de cálculo estrutural ou norma foi inventada: onde há dependência, o item está marcado {WARN}. Sem preços: {COTAR}. Projeto preliminar / executivo conceitual: não substitui ART, RRT, cálculo, projeto legal ou aprovação municipal.</p></div></section>''')
    def html(self):
        toc = table(["Código", "Seção", "#Pág."], [(esc(c), esc(l), n) for c, l, n in self.toc], "small")
        idx = f'<section class="page"><div class="head"><span>{esc(self.code)} · {REV}</span><span>ÍNDICE</span><span></span></div>{h("ÍNDICE")}<div class="cols2">{toc}</div><div class="foot"><span>{esc(self.title)}</span><span></span><span>{DATE} · 02</span></div></section>'
        pages = [self.pages[0], idx] + self.pages[1:]
        return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{esc(self.code)} · {esc(self.title)}</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'

def parts_rows(parts, prefixes):
    rows = []
    for p in parts:
        if prefixes and p["cod"][0] not in prefixes: continue
        rows.append([p["cod"], esc(p["nome"]), p["qtd"], (fmt(p["comp"], 2) if isinstance(p["comp"], (int, float)) else ""), esc(p["perfil"]), esc(p["aco"]), (fmt(p["peso_un"], 1) if isinstance(p["peso_un"], (int, float)) else ""), (fmt(p["peso_total"], 0) if isinstance(p["peso_total"], (int, float)) else ""), esc(p["fab"]), esc(p["uniao"])])
    return rows

def bom_groups(m, names):
    if MODELS[m]["bom"]:
        groups = MODELS[m]["bom"]()["groups"]
        return [(g, [(d, u, qn, kg) for (d, u, qn, kg) in rows]) for g, rows in groups if any(k.lower() in g.lower() for k in names)]
    groups = capsule_materials()
    return [(g, [(d, u, qn, "") for (d, u, qn, key) in rows]) for g, rows in groups if any(k.lower() in g.lower() for k in names)]

def bom_table(groups):
    out = ""
    for g, rows in groups:
        out += f"<h4>{esc(g)}</h4>" + table(["Item", "Un.", "#Qtd", "#kg", "Preço"], [(esc(d), esc(u), qn, kg if kg != "" else "", COTAR) for (d, u, qn, kg) in rows], "small")
    return out

def manual_rows(m, ids):
    man = {s["n"]: s for s in MODELS[m]["manual"]()}
    rows = []
    for i in ids:
        if i not in man: continue
        s = man[i]
        rows.append([f"{s['n']:02d}", f"<b>{esc(s['titulo'])}</b><br>{esc(s['equipe'])} · {esc(s['tempo'])}", esc(s["ferramentas"]) + (" · " + esc(s["equipamentos"]) if s["equipamentos"] else ""), esc(s["riscos"]), "<br>".join("☐ " + esc(c) for c in s["checklist"])])
    return table(["#", "Etapa · equipe · tempo", "Ferramentas e equipamentos", "Riscos", "Checklist"], rows, "xsmall")

def scope_page(D, m, n, inclui, exclui, entrega, recebe, fornecedor):
    M = MODELS[m]
    body = h(f"LOTE {n} · {LOTS[n][0]} · ESCOPO E INTERFACES", f"{M['name']} · {M['family']} · {M['dims']}")
    body += f'<div class="two"><div><h4>O QUE ESTE LOTE INCLUI</h4>{ul(inclui)}<h4>O QUE NÃO INCLUI (outros lotes)</h4>{ul(exclui)}<h4>FORNECEDOR-TIPO</h4><p class="lede">{fornecedor}</p></div>'
    body += f'<div><h4>O QUE ESTE LOTE ENTREGA AOS SEGUINTES</h4>{ul(entrega)}<h4>O QUE ESTE LOTE RECEBE DOS ANTERIORES</h4>{ul(recebe)}<h4>REGRAS DE MODULARIDADE (SÍTIOS DE MONTANHA)</h4>{table(["Regra", "Aplicação"], [(f"<b>{esc(a)}</b>", esc(b)) for a, b in MODULAR], "xsmall")}</div></div>'
    D.page(body, f"Escopo do lote {n}", code=f"{M['tag']}-LOT{n}-001")

def rfq_page(D, m, n, enviamos, retorna, criterios):
    M = MODELS[m]
    body = h(f"RFQ · PEDIDO DE COTAÇÃO DO LOTE {n}", f"{M['name']} · o que a Zion envia, o que o fornecedor devolve, critérios de aceite · {COTAR}")
    body += f'<div class="two"><div><h4>A ZION ENVIA</h4>{ol(enviamos)}<h4>O FORNECEDOR DEVOLVE</h4>{ol(retorna)}</div><div><h4>CRITÉRIOS DE ACEITE E GARANTIA</h4>{ul(criterios)}<h4>CONDIÇÕES GERAIS</h4>{ul(["Cotação por item e total, com prazo de fabricação e validade; impostos destacados; frete até o ponto de transbordo indicado.", "Amostras / protótipo de nó antes da série (quando indicado); inspeção da Zion em fábrica antes da expedição.", "Etiquetagem e embalagem conforme o pacote de transporte deste lote; lista de volumes assinada.", "Sem alteração de material ou bitola sem aprovação escrita da Zion e do engenheiro responsável (ART).", "Preços permanecem em documento interno da Zion; este documento circula sem preços."])}</div></div>'
    D.page(body, f"RFQ do lote {n}", code=f"{M['tag']}-LOT{n}-RFQ")

# =============================================================================== LOTE 1 · deck e infra
def lot1(D, m):
    M = MODELS[m]; g = M["geo"]; tag = M["tag"]
    scope_page(D, m, 1,
               ["Locação e preparo do terreno (roçada seletiva, acesso, estoque)", "Fundação em estacas helicoidais galvanizadas com cabeçotes ajustáveis (ou sapatas pré-moldadas onde há rocha)", "Grelha de vigas U 150 x 60 galvanizadas, vigas de borda e chapas de emenda", "Módulos de piso (vigotas, PIR, compensado naval, barreira de vapor) e deck em cumaru com escada e guarda-corpo", "Redes: água fria/quente (PEX), esgoto com ventilação e caixa de gordura, drenagem pluvial, eletroduto e QDC, condensadora, boiler, pré-instalação solar", "Passagens gabaritadas para os lotes 3 e 4 (pontos de água, energia, dutos)"],
               ["Estrutura metálica acima do piso (arcos, mastros, pilares, anéis): lote 2", "Lona, forro, isolamento, esquadrias e vidros: lote 3", "Marcenaria, FF&E, louças e equipamentos soltos: lote 4"],
               ["Ao lote 2: chapas de base / cabeçotes na posição (± 10 mm) e nível (± 5 mm), as-built da grelha assinado", "Ao lote 3: trilhos de base fixados e calha oculta conectada aos tubos de queda; pontos elétricos para LED do rodapé", "Ao lote 4: pontos de água/esgoto da cozinha e do banho, tomadas dedicadas, dutos e difusores"],
               ["Do projeto: planta estrutural, DET-03, DET-04, DET-06 a DET-09, quadro de estacas", "Do sítio: sondagem SPT ou ensaio de torque (obrigatório para o comprimento das estacas)"],
               "Empreiteiro de fundações helicoidais + equipe de montagem Zion (4 montadores + líder) + eletricista e encanador locais.")
    # fundação e grelha
    piles = M["piles"]()
    rows = [(f"F{i + 1:02d}", fmt(x, 2), fmt(y, 2)) for i, (x, y) in enumerate(piles)]
    half = (len(rows) + 1) // 2
    body = h("FUNDAÇÃO · QUADRO DE ESTACAS E CABEÇOTES", f"{len(piles)} pontos · coordenadas (x; y) em metros no sistema do projeto (x = 0 na fachada, y = 0 no eixo) · {WARN}")
    body += f'<div class="two"><div>{table(["Ponto", "x (m)", "y (m)"], rows[:half], "small")}</div><div>{table(["Ponto", "x (m)", "y (m)"], rows[half:], "small")}'
    spec = [("Estaca", "helicoidal Ø76,1 x 3,6 galvanizada, hélice Ø300 chapa 8 mm, L 2,0 m (emendável 1,0 m); torque mínimo de instalação conforme cálculo (ref. 4 kN·m para 25 kN de serviço)"),
            ("Cabeçote", "barra M30 rosqueada, curso 150 mm, chapa 150 x 150 x 8 com 4 furos M12; contraporca"), ("Alternativa em rocha", "sapata pré-moldada 60 x 60 x 25 com chumbador químico; nivelar com o mesmo cabeçote"),
            ("Declive", "até 15 %: cabeçotes altos (curso 300) e emenda de estaca; acima disso, patamar de brita e muro de arrimo de gabião (fora deste lote)"), ("Registro", "planilha por estaca: torque final, profundidade, cota do cabeçote")]
    if m == "capsule": spec[0] = ("Apoio", "4 pés telescópicos Ø101,6 em Ø114,3 (curso 0,40 m) sobre 4 estacas helicoidais ou 4 sapatas pré-moldadas 60 x 60 x 25; placa base 250 x 250 x 10")
    body += kv(spec) + "</div></div>"
    D.page(body, "Fundação · quadro de estacas", code=f"{tag}-FUN-001")
    # peças da base
    if m != "capsule":
        rows = parts_rows(M["parts"](), M["base_prefix"])
        D.page(h("GRELHA DO PISO, TRILHOS E FUNDAÇÃO · LISTA DE PEÇAS", "perfis U 150 x 60 x 3,0 galvanizados Z275, cantoneiras e chapas de emenda, estacas e cabeçotes · comprimentos ≤ 4,80 m para o transporte") + table(["Cód.", "Peça", "#Qtd", "Comp. (m)", "Perfil", "Aço", "#kg/un", "#kg", "Fabricação", "União"], rows, "xsmall"), "Grelha e fundação · peças", "flow", code=f"{tag}-EST-B01")
    # piso, deck e instalações (materiais)
    D.page(h("PISO, DECK, FUNDAÇÃO E INSTALAÇÕES · MATERIAIS", "quantidades estimadas a partir da geometria · sem preços") + f'<div class="cols2">{bom_table(bom_groups(m, ["piso", "deck", "fundação", "instala"]))}</div>', "Materiais do lote 1", "flow", code=f"{tag}-MAT-L1")
    for i, rel in enumerate(M["lot1"]):
        D.sheet_page(rel, f"{tag}-L1-{i + 1:02d}", os.path.basename(rel).replace(".svg", "").replace("_", " "), "ver prancha", M["name"])
    # sequência
    ids = [1, 2, 3, 4, 12, 13] if m != "capsule" else [1, 2, 4, 5]
    D.page(h("SEQUÊNCIA DE EXECUÇÃO DO LOTE 1", "etapas do manual de montagem que pertencem a este lote · equipe, ferramentas, riscos e checklist") + manual_rows(m, ids), "Sequência do lote 1", "flow", code=f"{tag}-MONT-L1")
    rfq_page(D, m, 1, ["Este documento (lista de peças da grelha e quadro de estacas)", "Planta estrutural e DET-03 / DET-04 em PDF e DXF", "Relatório de sondagem / torque do sítio (quando disponível)", "Pacote de instalações: DET-06 a DET-09"],
             ["Cotação das estacas + cravação por ponto (mobilização separada)", "Cotação dos perfis U cortados, furados e galvanizados (kg) + módulos de piso e deck (m²)", "Prazo por etapa e equipe proposta", "Certificado de galvanização e do aço"],
             ["Torque de cada estaca ≥ mínimo de projeto; prumo ≤ 2 %", "Cabeçotes nivelados ± 5 mm; diagonais da grelha ± 10 mm", "Teste hidráulico 6 bar / 30 min; DR e aterramento < 10 Ω", "Garantia: estacas 10 anos contra corrosão; deck 2 anos"])

# =============================================================================== LOTE 2 · metálico
def arch_table(C):
    rows = []
    for i, x in enumerate(C.ARCH_X):
        pts = C.section_local(x, 96); L = 0.0; acc = [0.0]
        for a, b in zip(pts[:-1], pts[1:]): L += math.dist(a, b); acc.append(L)
        rows.append((f"A{i}", fmt(x, 2), "Ø101,6 x 4,0" if i == 0 else "Ø88,9 x 3,6", fmt(C.a(x), 3), fmt(C.b(x), 3), fmt(C.top(x), 2), fmt(2 * C.floor_hw(x), 2), fmt(L, 2), fmt(L * 0.34, 2) + " / " + fmt(L * 0.32, 2) + " / " + fmt(L * 0.34, 2), "inclinado 8° (topo avança 0,60 m)" if i == 0 else "no plano vertical"))
    return rows

def arch_coords(C, every=0.5):
    """coordenadas (y, z) locais de cada arco a cada 0,50 m de comprimento desenvolvido, para o gabarito da calandra."""
    out = {}
    for i, x in enumerate(C.ARCH_X):
        pts = C.section_local(x, 400); acc = [0.0]
        for a, b in zip(pts[:-1], pts[1:]): acc.append(acc[-1] + math.dist(a, b))
        rows = []; s = 0.0
        while s <= acc[-1] + 1e-6:
            k = next((j for j in range(len(acc) - 1) if acc[j + 1] >= s), len(acc) - 2); f = (s - acc[k]) / max(acc[k + 1] - acc[k], 1e-9)
            y = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * f; z = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * f
            rows.append((fmt(s, 2), fmt(y, 3), fmt(max(z, 0), 3))); s += every
        out[f"A{i}"] = rows
    return out

def lot2(D, m):
    M = MODELS[m]; g = M["geo"]; tag = M["tag"]
    scope_page(D, m, 2,
               ["Todas as peças de aço acima do piso: arcos / mastros / pilares / caibros, anéis, terças, espinha, cabos e esticadores, chapas de base e emenda, luvas, talões, olhais", "Perfis de alumínio que viajam com a estrutura (keder, harpão, arremate de base, clamps) quando indicado", "Corte, calandra CNC por gabarito, furação, solda de fábrica, pré-montagem (fit test), galvanização a fogo, pintura a pó nas peças aparentes", "Etiquetagem, estrados e lista de volumes conforme o pacote de transporte"],
               ["Grelha do piso e estacas: lote 1 (podem ser cotadas com o mesmo serralheiro, como opção)", "Lona, forro e vidros: lote 3", "Marcenaria e FF&E: lote 4"],
               ["Ao lote 3: geometria conferida (topo dos arcos / cumes ± 15 mm), perfis keder / clamps / harpão instalados, superfícies sem rebarbas", "Ao lote 4: talões e furos para a marcenaria acoplada (cantoneiras nos arcos A1 a A4 no Casulo)", "Ao lote 1: chapas de base com os furos das vigas de borda"],
               ["Do lote 1: as-built da grelha (posição dos apoios ± 10 mm)", "Do projeto: DXF das peças, tabela de geometria dos arcos / caibros, detalhes DET-03, DET-10 a DET-13, este documento"],
               "Serralheria no Brasil com calandra CNC de tubos (raio variável), solda MIG/TIG qualificada, galvanizador parceiro; capacidade de fit test de um pórtico completo.")
    parts = M["parts"]()
    rows = parts_rows(parts, M["struct_prefix"])
    tot = sum(p["peso_total"] for p in parts if isinstance(p["peso_total"], (int, float)) and p["cod"][0] in M["struct_prefix"])
    D.page(h("LISTA DE PEÇAS · FERRO A FERRO", f"{len(rows)} tipos de peça · peso total ≈ {fmt(tot, 0)} kg · aço ASTM A500 Gr. B / A36, galvanizado a fogo NBR 6323 · parafusos 8.8 galvanizados · {WARN}") + table(["Cód.", "Peça", "#Qtd", "Comp. (m)", "Perfil", "Aço", "#kg/un", "#kg", "Fabricação", "União"], rows, "xsmall"), "Lista de peças", "flow", code=f"{tag}-EST-001")
    if m == "cocoon":
        D.page(h("GEOMETRIA DOS ARCOS · TABELA PARA A CALANDRA", "todos os arcos são elipses com centro a 0,75 m do piso (um gabarito com ajuste de raio) · A0 é inclinado 8° e recebe o engaste da cumeeira do Bico") +
               table(["Arco", "x (m)", "Tubo", "a (m)", "b (m)", "Topo z (m)", "Vão no piso (m)", "L desenv. (m)", "Segmentos E / C / D (m)", "Plano"], arch_table(g), "small") +
               '<p class="note">Segmentação: perna esquerda 34 %, coroa 32 %, perna direita 34 % do comprimento desenvolvido, luvas internas Ø76,1 x 200 (D02) nas emendas; pés com chapa 200 x 150 x 10 (D01). Marcação: A3-E / A3-C / A3-D. Tolerância de calandra: ± 5 mm no gabarito de bancada, ± 15 mm no topo montado.</p>', "Geometria dos arcos", code=f"{tag}-EST-002")
        coords = arch_coords(g)
        keys = list(coords.keys())
        for chunk in (keys[:4], keys[4:]):
            body = h("COORDENADAS DOS ARCOS · GABARITO", "pontos (y; z) no plano do arco a cada 0,50 m de comprimento desenvolvido, da base direita (y < 0) ao topo e à base esquerda · origem no eixo do piso") + '<div class="cols4">'
            for k in chunk:
                body += f"<h4>ARCO {k}</h4>" + table(["s", "y", "z"], coords[k], "xsmall")
            body += "</div>"
            D.page(body, f"Coordenadas dos arcos {chunk[0]} a {chunk[-1]}", "flow", code=f"{tag}-EST-003")
        bx = g.bico_export(); BT = g.bico_tube_lengths()
        ridge = [(fmt(x, 3), fmt(y, 3), fmt(z, 3)) for (x, y, z) in bx["ridge"]]
        edge = bx["edges"][0]; edge_s = [edge[i] for i in range(0, len(edge), 4)] + [edge[-1]]
        er = [(fmt(x, 3), fmt(y, 3), fmt(z, 3)) for (x, y, z) in edge_s]
        body = h("BICO · CUMEEIRA EM BALANÇO, TUBOS DE BORDA, COSTELA E TIRANTES", f"coordenadas 3D (x; y; z) dos eixos dos tubos · cumeeira Ø114,3 x 4,0 ({fmt(BT['ridge'], 2)} m) · borda Ø60,3 x 3,0 ({fmt(BT['edge'], 2)} m cada) · costela Ø48,3 ({fmt(BT['rib'], 2)} m) · tirantes Ø12 inox ({fmt(BT['tie'], 2)} m cada) · {WARN}")
        body += f'<div class="two"><div><h4>CUMEEIRA B09 (de A1 à ponta)</h4>{table(["x", "y", "z"], ridge, "xsmall")}<p class="note">Engaste em A0 e A1 por chapas 10 mm com 4 M16 (nó de momento); ponta com tampão e olhal; presilhas da lona a cada 300 mm.</p></div>'
        body += f'<div><h4>TUBO DE BORDA B10 (da lateral direita à esquerda, passando pela ponta)</h4>{table(["x", "y", "z"], er, "xsmall")}<p class="note">Curvamento 3D por gabarito de bancada impresso 1:1 a partir do DXF; nó soldado na ponta; chapa D01-B no anel A0. Tirantes: da cumeeira a 60 % do balanço ao anel A0 a ± 0,80 rad do topo.</p></div></div>'
        D.page(body, "Bico · coordenadas", code=f"{tag}-EST-004")
    elif m == "zenith":
        posts = [(f"PE{i + 1:02d}", fmt(x, 2), fmt(y, 2), fmt(g.edge_height(x, y), 2)) for i, (x, y) in enumerate(g.posts())]
        cols = [(f"P{i + 1:02d}", fmt(x, 2), fmt(y, 2)) for i, (x, y) in enumerate(g.columns())]
        body = h("GEOMETRIA · MASTROS, COROAS, ANEL DE BEIRAL, PILARES E POSTES", "coordenadas no sistema do projeto · alturas em metros sobre o piso")
        body += f'<div class="two"><div><h4>MASTROS E COROAS</h4>{table(["Cume", "x", "y", "Topo da membrana", "Topo do mastro", "Anel Ø"], [(esc(p["name"]), fmt(p["x"], 2), fmt(p["y"], 2), fmt(p["h"], 2), fmt(p["mast_top"], 2), fmt(2 * p["r"], 2)) for p in g.PEAKS], "small")}<h4>PILARES DO CORPO (Ø101,6 x 4,0 · topo 2,90)</h4>{table(["Pilar", "x", "y"], cols, "xsmall")}</div>'
        body += f'<div><h4>POSTES EXTERNOS INCLINADOS 8° (Ø76,1 x 3,6)</h4>{table(["Poste", "x", "y", "Cota do cabo de borda"], posts, "small")}<h4>ANEL DE BEIRAL 150 x 100 x 4,0</h4><p class="lede">6 segmentos (4,75 / 4,75 / 2,70 m por lado) com chapas de topo 150 x 180 x 10 e 4 M16 em cada emenda; perímetro 29,8 m; calha oculta no perfil de borda E01. Base articulada dos mastros (D09) e capitéis usinados (D10) conforme DET-11.</p></div></div>'
        D.page(body, "Geometria dos mastros e postes", code=f"{tag}-EST-002")
    elif m == "lodge":
        V = g.vertices(); BL = B.lodge_bom()
        body = h("GEOMETRIA · OCTÓGONO, PILARES, CAIBROS E LANTERNA", f"lado {fmt(g.side(), 3)} m · raio aos vértices {fmt(g.r_corner(), 3)} m · beiral {fmt(g.Z_EAVE, 2)} m · lanterna Ø{fmt(2 * g.R_LANTERN, 2)} a {fmt(g.Z_LANTERN, 2)} m · balanço da membrana {fmt(g.OVER, 2)} m")
        body += f'<div class="two"><div><h4>PILARES NOS VÉRTICES (Ø101,6 x 4,0)</h4>{table(["Pilar", "x", "y"], [(f"P{i + 1}", fmt(x, 3), fmt(y, 3)) for i, (x, y) in enumerate(V)], "small")}</div>'
        body += f'<div><h4>CAIBROS RADIAIS R1 a R8 (Ø76,1 x 3,6)</h4><p class="lede">Do talão H04 no vértice (z {fmt(g.Z_EAVE, 2)}) à orelha do anel de compressão (r {fmt(g.R_LANTERN, 2)}, z {fmt(g.Z_LANTERN, 2)}): comprimento {fmt(BL["rafter"], 2)} m cada, inclinação {fmt(math.degrees(math.atan2(g.Z_LANTERN - g.Z_EAVE, g.r_corner() - g.R_LANTERN)), 1)}°. Anel de compressão Ø60,3 calandrado (perímetro {fmt(BL["lantern"], 2)} m) com 8 orelhas; lanterna com 8 montantes de 0,60 m e tampa de alumínio.</p><h4>ANEL DE BEIRAL 150 x 100 x 4,0</h4><p class="lede">8 segmentos de {fmt(g.side(), 2)} m com chapas de topo dobradas a 135° (H03), 4 M16 por emenda; perfil de borda arredondado I01 com calha oculta; 22 estacas (J01).</p></div></div>'
        D.page(body, "Geometria do octógono", code=f"{tag}-EST-002")
    else:
        pts = g.section(g.RINGS[3], 24); acc = [0.0]
        for a, b in zip(pts[:-1], pts[1:]): acc.append(acc[-1] + math.dist(a[1:], b[1:]))
        rows = [(f"{i * 15}°", fmt(y, 3), fmt(z, 3), fmt(acc[i], 3)) for i, (x, y, z) in enumerate(pts)]
        sc = [(fmt(x, 2), fmt(g.s(x), 3), fmt(2 * g.half_width(x), 2), fmt(g.top(x) - g.bottom(x), 2)) for x in g.RINGS]
        body = h("GEOMETRIA · ANÉIS DA CASCA E LONGARINAS", f"seção em superelipse (n = 3,2) 3,20 x 3,20 m, centro a 0,85 m do piso · 12 anéis a cada 0,60 m em tubo retangular 60 x 40 x 3,0 calandrado · 7 longarinas 40 x 40 x 2,0 · chassi U 150 x 50 · {WARN}")
        body += f'<div class="two"><div><h4>SEÇÃO-TIPO DO ANEL (y; z) a cada 15° a partir de +y</h4>{table(["Ângulo", "y", "z", "s desenv."], rows, "xsmall")}</div>'
        body += f'<div><h4>ESCALA DOS ANÉIS NAS CALOTAS</h4>{table(["Anel x", "Fator s", "Largura", "Altura"], sc, "small")}<p class="note">Os anéis do corpo (s = 1) são iguais: um único gabarito de calandra; os anéis das calotas usam o mesmo gabarito com fator de escala. Longarinas nos ângulos {", ".join(str(d) + "°" for d in g.STRINGER_DEG)} a partir de +y. Pés telescópicos e olhais de içamento (4) conforme lista.</p></div></div>'
        D.page(body, "Geometria dos anéis", code=f"{tag}-EST-002")
    # conexões, galvanização, pré-montagem, tolerâncias
    body = h("FABRICAÇÃO · GABARITOS, SOLDA, GALVANIZAÇÃO, PRÉ-MONTAGEM E TOLERÂNCIAS", "regras para o serralheiro · nada de solda em campo")
    body += f'<div class="two"><div>{kv([("Gabaritos", "Bancada 1:1 impressa a partir do DXF para cada família de peça curva (arcos, anéis, tubos de borda); conferência por medição de 5 pontos antes de soldar as chapas."), ("Solda", "MIG/MAG ou TIG, soldador qualificado; cordão contínuo nas chapas de base e talões; esmerilhar respingos; nenhuma solda após galvanização."), ("Galvanização", "A fogo NBR 6323 (mín. 70 µm) em todas as peças de aço; furos de respiro e dreno nos tubos fechados; roscas protegidas e repassadas."), ("Pintura", "Pó poliéster texturizado, cor Zion (verde #1B2117 ou preto #040605) nas peças aparentes, após galvanização com preparo por jateamento leve ou primer de aderência."), ("Parafusos", "Classe 8.8 galvanizados a fogo com porca e arruela; torque 45 N·m (M12) e 120 N·m (M16); pinos de segurança nas luvas.")])}</div>'
    body += f'<div>{kv([("Pré-montagem (fit test)", "Montar em fábrica um pórtico completo (ou o anel de beiral completo / 3 anéis + longarinas na Cápsula) sobre a grelha-gabarito; medir e registrar; só então galvanizar."), ("Tolerâncias", "Comprimento de peças retas ± 2 mm; furos ± 1 mm; peças calandradas ± 5 mm no gabarito; topo montado ± 15 mm; prumo 1/500."), ("Marcação", "Código gravado (punção ou etiqueta metálica) em cada peça: modelo-código-segmento; setas de orientação; peso nas peças > 40 kg."), ("Embalagem", "Estrados de madeira ≤ 2,4 x 1,2 m, peças amarradas com cintas e separadores de EVA; lista de volumes; peças pequenas em caixas plásticas identificadas por etapa de montagem."), ("Inspeção", "Zion inspeciona em fábrica antes da galvanização e antes da expedição: dimensional, soldas (visual), certificados do aço e da galvanização.")])}</div></div>'
    D.page(body, "Fabricação e tolerâncias", code=f"{tag}-FAB-001")
    # transporte
    tr = M["transport"](); tr = tr["items"] if isinstance(tr, dict) else tr
    D.page(h("PACOTE DE TRANSPORTE DO LOTE 2 (E DA UNIDADE)", "volumes, dimensões, m³ e kg · limites para caminhão 3/4 e transbordo em 4x4") + table(["Volume", "Dimensões", "#m³", "#kg"], [(esc(a), esc(b), c, d) for (a, b, c, d) in tr], "small") + '<p class="note">Volumes com peso acima de 120 kg exigem tripé com talha ou empilhadeira no transbordo; em sítios de montanha, dividir os estrados de estrutura em 2 (≤ 400 kg) e prever picape 4x4 com 3 a 4 viagens.</p>', "Transporte", code=f"{tag}-LOG-001")
    for i, rel in enumerate(M["lot2"]):
        D.sheet_page(rel, f"{tag}-L2-{i + 1:02d}", os.path.basename(rel).replace(".svg", "").replace("_", " "), "ver prancha", M["name"])
    ids = [5, 6, 7] if m != "capsule" else [3]
    D.page(h("SEQUÊNCIA DE MONTAGEM DA ESTRUTURA", "etapas do manual que pertencem a este lote") + manual_rows(m, ids), "Sequência do lote 2", "flow", code=f"{tag}-MONT-L2")
    rfq_page(D, m, 2, ["Este documento (lista de peças, geometria, tolerâncias, embalagem)", "DXF das peças e dos gabaritos 1:1 (pasta <modelo>/dxf)", "Detalhes DET-03 e DET-10 a DET-13; isométrica da estrutura", "Cronograma-alvo de fabricação (master plan)"],
             ["Cotação por peça (kg e unidade) com calandra, solda, galvanização e pintura destacadas", "Prazo, capacidade de calandra (raio mínimo) e galvanizador", "Proposta de fit test e de embalagem", "Certificados do aço; ART do fabricante quando aplicável"],
             ["Dimensional por amostragem (10 % das peças) dentro das tolerâncias", "Galvanização mín. 70 µm; sem soldas expostas sem tratamento", "Fit test aprovado e fotografado antes da expedição", "Garantia: 5 anos contra corrosão e defeitos de fabricação"])

# =============================================================================== LOTE 3 · lonas, revestimentos e vidros
def lot3(D, m):
    M = MODELS[m]; tag = M["tag"]
    pats = lona.dedupe(lona.PATTERNS[m]())
    ext = [p for p in pats if p.group != "interna"]; inn = [p for p in pats if p.group == "interna"]
    a_ext = sum(p.area * p.qty for p in ext); a_inn = sum(p.area * p.qty for p in inn)
    rigid = m == "capsule"
    scope_page(D, m, 3,
               [("Revestimento externo em ACM curvado sobre subestrutura, com padrões de corte por painel" if rigid else "Lona externa (membrana PVDF tipo II) confeccionada por painéis conforme os padrões de corte deste lote, com keder, bolsas e reforços"),
                ("Revestimento interno em compensado curvado" if rigid else "Forro interno tensionado (Trevira CS) por painéis, com harpão"), "Isolamento (lã de PET / PIR), manta refletiva, barreira de vapor e câmara ventilada", "Perfis de fixação que não viajam com a estrutura: keder, harpão, clamps, cabos de borda, esticadores", "Esquadrias e vidros: fachadas, portas, Olhos / óculo / lanterna / Visor, claraboias, com contramarcos e selantes", "Instalação da lona e dos vidros por equipe especializada (instaladores de membrana + vidraceiro)"],
               ["Estrutura e perfis que viajam soldados nela: lote 2", "Fundação, piso e instalações: lote 1", "Marcenaria e FF&E: lote 4"],
               ["Ao lote 4: envelope fechado e estanque (teste de água) antes da marcenaria e do enxoval", "Ao lote 1: descidas de água da calha ligadas aos tubos de queda"],
               ["Do lote 2: geometria conferida e liberada (relatório de esquadro), perfis keder / clamps instalados", "Do projeto: padrões DXF + XLSX, mapa de painéis LN-01, fixações LN-90, quadro de esquadrias"],
               ("Fabricante de ACM / painéis curvados + vidraceiro de vidro curvo" if rigid else "Confeccionista de membranas tensionadas (corte CNC, solda HF, form-finding) + vidraceiro com vidro insulado / laminado + instaladores de membrana."))
    rows = [(p.id, p.qty, lona.GRP[p.group].title(), esc(p.name), f"{p.w:.2f} x {p.h:.2f}".replace(".", ","), round(p.area, 2), round(p.area * p.qty, 1), ", ".join(sorted({lona.KINDS[k][2].split(" ·")[0] for k, _ in p.edges})), len(p.holes)) for p in pats]
    body = h("QUADRO DE PAINÉIS · PADRÕES DE CORTE", f"{len(ext)} padrões externos = {fmt(a_ext, 1)} m² · {len(inn)} internos = {fmt(a_inn, 1)} m² (forma final; acrescentar 12 a 15 % de sobras, bolsas e emendas) · geometria em <modelo>/lona/ (SVG, DXF, XLSX)")
    body += table(["Cód.", "#Qtd", "Grupo", "Painel", "Caixa (m)", "#m²", "#m² total", "Bordas", "#Recortes"], rows, "xsmall")
    body += '<p class="note">Como o padrão foi obtido: a superfície entre duas costuras (arcos, caibros, anéis ou linhas de emenda) é planificada por triangulação sequencial; o resultado é a geometria "de forma final", sem compensação. O confeccionista aplica a compensação do tecido (ensaio biaxial), as sobras de keder / bolsa e define a padronagem de rolos (largura 2,50 a 3,00 m). Painéis maiores que o rolo levam emenda HF longitudinal.</p>'
    D.page(body, "Quadro de painéis", "flow", code=f"{tag}-LON-001")
    # materiais do envelope
    matn = ["envelope", "alumínio", "membrana"]
    D.page(h("MATERIAIS DO ENVELOPE, ISOLAMENTO E PERFIS", "quantidades estimadas · sem preços") + f'<div class="cols2">{bom_table(bom_groups(m, matn))}</div>' + f'<h4>ESPECIFICAÇÃO DA LONA</h4>{kv([("Lona externa", "PVDF tipo II 1050 g/m² (poliéster HT 1100 dtex, PVC + laca PVDF bifacial), cor creme Zion, resistência ≥ 4.200 / 4.000 N/5 cm, classe B / M2, garantia 10 anos; opção: PTFE-vidro 800 g/m² (30 anos, custo maior)"), ("Forro", "Trevira CS 210 g/m² (ou lona translúcida 350 g/m² sob claraboias), harpão de PVC soldado"), ("Isolamento", "lã de PET 50 mm 25 kg/m³ entre terças / caibros + manta refletiva com face para a câmara; PIR 60 mm na Cápsula"), ("Keder e perfis", "cordão keder Ø10 / Ø13 PVC; perfil duplo keder alu 6060-T5; barras de clamp 40 x 6; harpão 40 x 20; presilhas inox 304"), ("Costuras", "solda de alta frequência 40 mm; nenhuma costura com linha na face externa; reforços de 150 mm em recortes e cantos"), ("Cabos", "inox 316 7 x 19 Ø8 / Ø10 / Ø12 com terminais prensados, esticadores M12 a M20, manilhas")]) if not rigid else kv([("ACM", "alumínio composto 4 mm (0,5 + 3 + 0,5) PVDF, cor champanhe fosco, curvado a frio sobre perfis ômega; painéis ≤ 2,80 x 1,20 m"), ("Juntas", "perfil H de alumínio com EPDM e selante PU; junta de 12 mm em todos os anéis"), ("Isolamento", "PIR 60 mm em painéis curvados + barreira de vapor (manta líquida) + câmara 40 mm"), ("Interno", "compensado naval 2 x 6 mm colado e curvado, lâmina de carvalho, verniz fosco")])}', "Materiais do lote 3", "flow", code=f"{tag}-MAT-L3")
    # pranchas LN
    for f in lona.sheets(m):
        D.sheet_page(f"{m}/lona/{f}", f.split("_")[0], f.split("_", 1)[1].replace(".svg", "").replace("_", " "), "ver malha (m)", M["name"])
    for i, rel in enumerate(M["lot3"]):
        D.sheet_page(rel, f"{tag}-L3-{i + 1:02d}", os.path.basename(rel).replace(".svg", "").replace("_", " "), "ver prancha", M["name"])
    # vidros e esquadrias
    esq = M["esq"]; KG = 30.0
    rows = [(c, esc(n), fmt(w, 2), fmt(hh, 2), nn, round(w * hh, 2), round(w * hh * KG, 0), esc(s), esc(loc)) for (c, n, w, hh, nn, s, loc) in esq]
    tot = sum(w * hh * nn for (_, _, w, hh, nn, _, _) in esq)
    body = h("VIDROS E ESQUADRIAS · QUADRO", f"{fmt(tot, 1)} m² de vidro · peso estimado 30 kg/m² (insulado 6 + 12 + 6) a 40 kg/m² (laminado curvo) · panos ≤ 90 kg para transporte manual em montanha (acima disso, dividir o pano ou usar içador a vácuo)")
    body += table(["Cód.", "Esquadria", "Larg. (m)", "Alt. (m)", "#Qtd", "#m² un.", "#kg un.", "Especificação", "Localização"], rows, "xsmall")
    body += f'<h4>REGRAS</h4>{ul(["Contramarcos de alumínio com ruptura térmica, anodizado bronze; furação e selagem só nos perfis, nunca na lona.", "Vidro insulado low-e 6 lam + 12 Ar + 6 temp (fachadas); laminado 8 + 8 (claraboias, Espinha, lanterna); curvo laminado (Visor, Anel de Luz, lanterna); acidado nos banhos.", "Cavaletes de vidro ≤ 2,2 x 2,4 m; panos numerados; calços de EPDM; silicone estrutural neutro; teste de água após a instalação.", "Vidraceiro entrega: conferência de medidas na estrutura montada (lote 2 concluído) antes de cortar os vidros: tolerância ± 3 mm."])}'
    D.page(body, "Vidros e esquadrias", "flow", code=f"{tag}-ESQ-001")
    ids = [8, 9, 10, 11] if m != "capsule" else [6]
    D.page(h("SEQUÊNCIA DE INSTALAÇÃO · LONA, ISOLAMENTO, FORRO E VIDROS", "etapas do manual que pertencem a este lote · vento > 30 km/h suspende a lona") + manual_rows(m, ids), "Sequência do lote 3", "flow", code=f"{tag}-MONT-L3")
    rfq_page(D, m, 3, ["Este documento (quadro de painéis, materiais, fixações LN-90, quadro de esquadrias)", f"Padrões de corte: {tag}-LON-001_padroes.dxf e {tag}-LON-001_coordenadas.xlsx; pranchas LN-01 a LN-90", "Modelo 3D (GLB) e malha da superfície para form-finding", "Detalhes DET-01 / DET-02 / DET-05"],
             ["Cotação da lona externa (m² confeccionado, por painel) e do forro; perfis e cabos por metro; instalação por dia de equipe", "Padronagem proposta (rolos, emendas) e compensação adotada (laudo biaxial do tecido)", "Cotação dos vidros por pano (m²) e das esquadrias (un.), com prazo de medição em obra", "Amostra do tecido e do vidro; ficha técnica e garantia"],
             ["Lona: sem rugas após tensionamento, pré-tensão de projeto medida, teste de água 15 min sem infiltração", "Solda HF: ensaio de tração da emenda ≥ 80 % do tecido", "Vidros: sem trincas, calços e selantes conforme, teste de água", "Garantia: lona 10 anos (PVDF) · forro 5 anos · vidros 5 anos (insulado)"])

# =============================================================================== LOTE 4 · mobílias
def lot4(D, m):
    M = MODELS[m]; g = M["geo"]; tag = M["tag"]
    scope_page(D, m, 4,
               ["Marcenaria acoplada (MA): peças fixas fabricadas em fábrica com gabaritos da estrutura, montadas e acabadas antes do embarque", "Mobiliário solto (MS) e FF&E Zion New Luxury: cama, chaise, sofá, poltronas, mesas, luminárias, tapetes, cortinas, arte", "Equipamentos: mini cozinha / café (cooktop de indução, forno, geladeira, air fryer, cafeteira), cofre, som, fechadura digital, automação, secador", "Louças, metais e banheira (fornecimento; instalação no lote 1/3 conforme o manual)", "Enxoval, amenities, OS&E, sinalização e kit de segurança"],
               ["Piso, deck e instalações: lote 1", "Estrutura: lote 2", "Lona, forro e vidros: lote 3"],
               ["À operação: unidade mobiliada, inventário fotografado, manual do hóspede e do operador"],
               ["Do lote 2: talões / cantoneiras nos arcos para a marcenaria acoplada; gabarito da seção da concha", "Do lote 3: forro fechado e envelope estanque; requadros dos Olhos", "Do lote 1: pontos de água, esgoto, tomadas dedicadas (cooktop, forno), dutos"],
               "Marcenaria com CNC e experiência em peças curvas + fornecedores de FF&E (curadoria Zion) + instalador de equipamentos.")
    if m == "cocoon":
        rows = [(x["cod"], esc(x["nome"]), f"{fmt(x['x2'] - x['x1'], 2)} x {fmt(x['y2'] - x['y1'], 2) if x['y2'] != x['y1'] else '—'} x h {fmt(x['h'], 2)}", esc(x["amb"]), esc(x["ffe"]), esc(x["desc"]), esc(x["mat"])) for x in MA]
        D.page(h("MARCENARIA ACOPLADA · MA-01 A MA-08", "peças fixas fabricadas com a cabana; fundos recortados conforme a seção da concha (gabarito dos arcos A1 a A4); fixação por cantoneiras nos arcos, nunca na membrana") + table(["Cód.", "Peça", "Dimensões (m)", "Amb.", "FF&E", "Descrição", "Materiais"], rows, "xsmall"), "Marcenaria acoplada", "flow", code=f"{tag}-MOB-001")
        rows = [(x["cod"], esc(x["nome"]), esc(x["dims"]), esc(x["amb"]), esc(x["ffe"]), esc(x["pos"])) for x in MS]
        D.page(h("MOBILIÁRIO SOLTO · MS-01 A MS-09", "entregue montado; passa pela porta PV1 (1,00 x 2,40): módulos ≤ 0,95 m de largura") + table(["Cód.", "Peça", "Dimensões (m)", "Amb.", "FF&E", "Posição"], rows, "small"), "Mobiliário solto", code=f"{tag}-MOB-002")
    else:
        rows = []
        for f in g.furniture():
            if f["kind"] in ("wall", "opening", "glass", "pillow", "ceiling", "hvac", "condenser", "partition"): continue
            if "r" in f: dims = f"Ø{fmt(2 * f['r'], 2)} x h {fmt(f['z2'] - f['z1'], 2)}"; pos = f"({fmt(f['x'], 2)}; {fmt(f['y'], 2)})"
            else: dims = f"{fmt(f['x2'] - f['x1'], 2)} x {fmt(f['y2'] - f['y1'], 2)} x h {fmt(f['z2'] - f['z1'], 2)}"; pos = f"x {fmt(f['x1'], 2)} a {fmt(f['x2'], 2)} · y {fmt(f['y1'], 2)} a {fmt(f['y2'], 2)}"
            rows.append((esc(f["name"] or f["kind"]), esc(f["kind"]), dims, pos, "MA (acoplada)" if f["kind"] in ("cabinet", "vanity", "totem", "bench") else "MS (solta)"))
        D.page(h("PROGRAMA DE MOBILIÁRIO · ANTEPROJETO", f"posições e dimensões do modelo 3D · o projeto de interiores {tag}-INT-001 (marcenaria acoplada, elevações, detalhes) segue o método do Casulo e é a próxima entrega desta linha") + table(["Peça", "Tipo", "Dimensões (m)", "Posição", "Classe"], rows, "small") + f'<p class="note">Marcenaria acoplada (MA): fixada à estrutura (mastros, pilares, anéis, parede da cabeceira) e nunca à lona; fundos e tampos recortados por gabarito. {WARN} para peças que carregam nos mastros (Safari) e nos pilares (Lodge).</p>', "Programa de mobiliário", "flow", code=f"{tag}-MOB-001")
    # FF&E por categoria (sem preços)
    R = ffe.rows(m); cats = {}
    for r in R: cats.setdefault(r["cat_name"], []).append(r)
    body = h("FF&E, EQUIPAMENTOS, ENXOVAL E OS&E", f"{len(R)} itens · quantidades por unidade · Zion New Luxury · sem preços ({COTAR})")
    body += '<div class="cols2">'
    for c, rs in cats.items():
        body += f"<h4>{esc(c.upper())}</h4>" + table(["Cód.", "Item", "Especificação", "Un.", "#Qtd", "Ambiente"], [(r["code"], esc(r["desc"]), esc(r["spec"]), esc(r["un"]), r["qty"], esc(r["amb"] + (" · " + r["obs"] if r["obs"] else ""))) for r in rs], "xsmall")
    body += "</div>"
    D.page(body, "FF&E e equipamentos", "flow", code=f"{tag}-FFE-001")
    for i, rel in enumerate(M["lot4"]):
        D.sheet_page(rel, f"{tag}-L4-{i + 1:02d}", os.path.basename(rel).replace(".svg", "").replace("_", " "), "ver prancha", M["name"])
    ids = [14, 15, 16, 17] if m != "capsule" else [6]
    D.page(h("SEQUÊNCIA · BANHO, MÓVEIS, ACABAMENTOS E ENTREGA", "etapas do manual que pertencem a este lote") + manual_rows(m, ids), "Sequência do lote 4", "flow", code=f"{tag}-MONT-L4")
    rfq_page(D, m, 4, ["Este documento (MA, MS, FF&E)", "Pranchas de interiores IN-01 a IN-06 (Casulo) ou programa de mobiliário e planta humanizada", "Gabarito da seção da concha / paredes (lote 2) para as peças acopladas", "Paleta de materiais e acabamentos Zion"],
             ["Cotação por peça de marcenaria (com ferragens e acabamento) e por item de FF&E", "Prazo, amostras de lâmina, pedra e tecidos", "Plano de embalagem: módulos ≤ 0,95 x 2,10 m e ≤ 60 kg", "Garantia e assistência"],
             ["Marcenaria: ± 3 mm; portas e gavetas reguladas; acabamento PU fosco sem marcas", "FF&E conforme especificação; inventário fotografado na entrega", "Equipamentos testados e com nota fiscal em nome da operação", "Garantia: marcenaria 3 anos · FF&E conforme fabricante"])

# =============================================================================== documentos de lote
def build_lot(m, n):
    M = MODELS[m]; code = f"{M['tag']}-LOT{n}-001"
    D = Doc(code, f"LOTE {n} · {LOTS[n][0]}", m)
    D.cover(f"{M['name']} · LOTE {n} DE 4", f"LOTE {n}<br>{LOTS[n][0].replace(' E ', ' E<br>', 1) if len(LOTS[n][0]) > 22 else LOTS[n][0]}", f"{M['name']} · {M['family']} · {M['dims']}. {LOTS[n][1]}. Documento de contratação separado, pensado para fabricação no Brasil e montagem modular em sítios de montanha: peças transportáveis, ligações parafusadas, sem concreto e sem solda em campo.",
            f'<div class="stats"><div><b>{fmt(M["area_int"], 1)} m²</b><span>internos</span></div><div><b>{fmt(M["area_ext"], 1)} m²</b><span>deck</span></div><div><b>{M["days"]} dias</b><span>montagem (4 + líder)</span></div><div><b>4 lotes</b><span>deck · ferro · lona e vidro · mobília</span></div></div>')
    {1: lot1, 2: lot2, 3: lot3, 4: lot4}[n](D, m)
    return D

# =============================================================================== master plan
def master_plan(lot_docs):
    D = Doc("ZG-MP-001", "MASTER PLAN · 4 MODELOS × 4 LOTES")
    D.cover("CABIN DESIGN & ENGINEERING SYSTEM", "MASTER<br>PLAN", "Plano completo do que tem de ser feito para fabricar e montar as quatro unidades da Zion Glamping Collection (Casulo, Safari, Lodge 38 e Cápsula) em quatro lotes independentes de contratação: 1 deck e infraestrutura · 2 estrutura metálica (serralheiro no Brasil) · 3 lonas, revestimentos e vidros (confeccionista e vidraceiro) · 4 mobílias. Tudo modular, transportável e montável em montanha sem guindaste e sem concreto. Este documento une os 16 lotes (anexos) num único pacote.",
            '<div class="stats"><div><b>4</b><span>modelos</span></div><div><b>16</b><span>documentos de lote</span></div><div><b>0</b><span>solda ou concreto em campo</span></div><div><b>≤ 120 kg</b><span>maior peça (4 pessoas)</span></div></div>')
    # visão
    rows = [(esc(M["name"]), esc(M["family"]), esc(M["dims"]), fmt(M["area_int"], 1), fmt(M["area_ext"], 1), M["days"], esc(M["cat"])) for M in MODELS.values()]
    body = h("A LINHA E A ESTRATÉGIA DE CONTRATAÇÃO EM 4 LOTES", "cada modelo é um kit; cada kit é comprado em quatro contratos separados e montado por uma equipe Zion")
    body += table(["Modelo", "Família", "Dimensões", "#m² int.", "#m² deck", "#Dias de montagem", "Categoria"], rows, "small")
    body += f'<div class="two"><div><h4>OS 4 LOTES</h4>{table(["Lote", "Conteúdo", "Fornecedor-tipo", "Contrato"], [("1 · Deck e infra", esc(LOTS[1][1]), "fundações helicoidais + montadores + eletricista/encanador", "por unidade, no sítio"), ("2 · Estrutura metálica", esc(LOTS[2][1]), "serralheiro no Brasil com calandra CNC e galvanizador", "por kit, em fábrica"), ("3 · Lonas, revestimentos e vidros", esc(LOTS[3][1]), "confeccionista de membranas + vidraceiro + instaladores", "por kit, em fábrica + instalação"), ("4 · Mobílias", esc(LOTS[4][1]), "marcenaria CNC + FF&E + instalador", "por unidade")], "small")}</div>'
    body += f'<div><h4>POR QUE SEPARAR</h4>{ul(["Cada fornecedor cota só o que domina: o serralheiro não precisa entender de lona, o confeccionista recebe os padrões prontos e os ferros já definidos.", "A Zion controla as interfaces com planilhas de as-built entre lotes e mantém o projeto (geometria única em geometry.py) como fonte de verdade.", "Permite comprar em série (10 kits de ferro, 10 de lona) com fornecedores diferentes por região e montar onde não chega guindaste.", "Cada lote tem seu RFQ, sua lista de materiais e seu checklist de aceite; os preços ficam em documento interno."])}<h4>REGRA DE OURO</h4><p class="lede">Se eu entregar isto a uma fábrica amanhã, ela entende o que fabricar, pergunta o que falta e devolve orçamento? Cada documento de lote foi escrito para responder sim; onde depende de cálculo ou norma, está marcado {WARN}.</p></div></div>'
    D.page(body, "Linha e estratégia", code="ZG-MP-01")
    # modularidade
    body = h("MODULARIDADE PARA SÍTIOS DE MONTANHA", "regras que valem para os 4 modelos e os 4 lotes: ferros, lonas, vidros e mobílias") + table(["Regra", "Aplicação"], [(f"<b>{esc(a)}</b>", esc(b)) for a, b in MODULAR], "small")
    body += f'<div class="two"><div><h4>CADEIA DE TRANSPORTE</h4><div class="flowchart"><span>Fábrica (serralheiro, confeccionista, vidraceiro, marcenaria)</span><i></i><span>Caminhão 3/4 até o ponto de transbordo (estrada)</span><i></i><span>Picape 4x4 / carreta agrícola até o sítio (≤ 4,8 m, ≤ 400 kg por volume)</span><i></i><span>Tripé + talha e 4 montadores no ponto de montagem</span></div></div><div><h4>EXCEÇÃO: CÁPSULA</h4><p class="lede">A Cápsula viaja inteira (8,4 x 3,2 x 3,2 m, ≈ 4,2 t) em caminhão-prancha e pousa com munck de 8 t ou por guincho e trilhos: exige acesso de caminhão até 30 m do ponto de pouso. Em sítios sem esse acesso, usar Casulo, Safari ou Lodge.</p></div></div>'
    D.page(body, "Modularidade", code="ZG-MP-02")
    # WBS e cronograma
    weeks = [("Projeto executivo, cálculo (ART) e form-finding da lona", 0, 3, "Zion + engenheiro"), ("RFQ dos 4 lotes e contratação", 1, 2, "Zion"), ("Lote 2 · fabricação do ferro (gabaritos, calandra, solda, fit test, galvanização)", 3, 6, "serralheiro"), ("Lote 3 · confecção da lona e do forro (compensação, corte CNC, solda HF)", 4, 4, "confeccionista"),
             ("Lote 3 · esquadrias e vidros (medição após o fit test)", 5, 5, "vidraceiro"), ("Lote 4 · marcenaria e FF&E", 4, 5, "marcenaria + FF&E"), ("Lote 1 · sondagem, estacas, grelha, piso e deck no sítio", 6, 3, "fundações + montadores"), ("Transporte e transbordo dos kits", 9, 1, "Zion"), ("Montagem: estrutura (lote 2) → lona e vidros (lote 3) → instalações (lote 1)", 10, 2, "montadores + instaladores"), ("Lote 4 · móveis, equipamentos, enxoval, testes e entrega", 12, 1, "marcenaria + operação")]
    bars = "".join(f'<div class="gr"><span class="gl">{esc(t)}</span><span class="gb" style="margin-left:{s * 7}%;width:{d * 7}%"></span><span class="gw">{esc(w)}</span></div>' for (t, s, d, w) in weeks)
    body = h("CRONOGRAMA-ALVO DA PRIMEIRA UNIDADE (SEMANAS)", "da liberação do projeto executivo à entrega · unidades seguintes em série: lotes 2 a 4 em paralelo, 1 unidade a cada 2 semanas por equipe de montagem")
    body += f'<div class="gantt"><div class="gh">{"".join(f"<i>{k}</i>" for k in range(0, 14))}</div>{bars}</div>'
    body += f'<h4>WBS · ESTRUTURA ANALÍTICA</h4>{table(["Nível 1", "Nível 2", "Entregável", "Documento"], [("Projeto", "Executivo e cálculo", "ART / RRT, form-finding, DXF finais", "ZG-TEC-001, ZC-INT-001, <TAG>-LON-001"), ("Compras", "4 RFQs por modelo", "contratos, amostras, fit test", "<TAG>-LOT1..4-RFQ"), ("Fábrica", "Lotes 2, 3 e 4", "kits etiquetados, listas de volumes", "<TAG>-LOT2/3/4-001"), ("Sítio", "Lote 1 + montagem", "as-built da fundação e da grelha; relatório de esquadro; teste de água; entrega", "<TAG>-LOT1-001, manual 17 etapas"), ("Operação", "Entrega", "manual do operador, inventário, garantias", "checklist de entrega")], "small")}'
    D.page(body, "Cronograma e WBS", code="ZG-MP-03")
    # interfaces
    inter = [("Lote 1 → Lote 2", "Posição dos apoios (chapas de base / cabeçotes) ± 10 mm, nível ± 5 mm, diagonais ± 10 mm; furos M16 nas vigas de borda", "As-built da grelha assinado pelo líder"),
             ("Lote 2 → Lote 3", "Topo dos arcos / cumes / anel ± 15 mm; prumo 1/500; perfis keder, clamps e trilhos de harpão instalados; sem rebarbas; presilhas e olhais nas posições", "Relatório de esquadro e liberação para a lona (etapa 7 do manual)"),
             ("Lote 3 → Lote 4", "Envelope fechado e estanque (teste de água 15 min); forro tensionado; requadros dos Olhos; vidros instalados", "Checklist de estanqueidade"),
             ("Lote 1 → Lote 3", "Trilhos de base e calha ligados aos tubos de queda; alimentação para LED do rodapé", "Teste de escoamento"),
             ("Lote 1 → Lote 4", "Pontos de água / esgoto da mini cozinha e do banho; tomadas dedicadas (cooktop 20 A, forno 16 A); dutos e difusores", "Teste hidráulico e elétrico"),
             ("Lote 2 → Lote 4", "Talões e cantoneiras nos arcos / pilares para a marcenaria acoplada; gabarito da seção da concha", "Gabarito conferido em fábrica"),
             ("Lote 3 (lona) → Lote 3 (vidros)", "Vidraceiro mede na estrutura montada (após o fit test ou no sítio) antes de cortar: tolerância ± 3 mm", "Planilha de medidas")]
    body = h("MATRIZ DE INTERFACES ENTRE LOTES", "o que cada lote entrega ao seguinte, com tolerância e documento de passagem") + table(["Interface", "Entrega e tolerância", "Documento de passagem"], inter, "small")
    resp = [("Projeto e geometria", "Zion (este repositório)", "engenheiro (ART)", "fornecedores comentam"), ("Fundação e grelha", "empreiteiro de estacas + montadores", "Zion (líder)", "engenheiro"), ("Ferro", "serralheiro", "Zion (inspeção em fábrica)", "galvanizador"), ("Lona e forro", "confeccionista", "instaladores de membrana", "Zion"), ("Vidros", "vidraceiro", "Zion", "—"), ("Móveis e FF&E", "marcenaria + fornecedores", "Zion (curadoria)", "operação"), ("Montagem no sítio", "líder + 4 montadores Zion", "eletricista / encanador locais", "engenheiro (vistoria)"), ("Entrega e operação", "Zion", "operador do glamping", "—")]
    body += f'<h4>MATRIZ DE RESPONSABILIDADES</h4>{table(["Pacote", "Executa", "Apoia / inspeciona", "Valida"], resp, "small")}'
    D.page(body, "Interfaces e responsabilidades", code="ZG-MP-04")
    # sequência integrada
    seq = [("01", "Preparação e locação", 1), ("02", "Estacas helicoidais", 1), ("03", "Grelha de vigas", 1), ("04", "Módulos de piso e deck", 1), ("05", "Estrutura principal (arcos / mastros / pilares / anéis)", 2), ("06", "Travamentos, cabos, espinha, terças", 2), ("07", "Conferência de esquadro e liberação", 2), ("08", "Lona externa", 3), ("09", "Isolamento e refletiva", 3), ("10", "Forro interno", 3), ("11", "Portas e vidros", 3), ("12", "Elétrica", 1), ("13", "Hidráulica", 1), ("14", "Banho (louças, metais, banheira)", 4), ("15", "Marcenaria e móveis", 4), ("16", "Acabamentos e enxoval", 4), ("17", "Testes e entrega", "todos")]
    body = h("SEQUÊNCIA INTEGRADA DE MONTAGEM", "as 17 etapas do manual, com o lote responsável; vale para Casulo, Safari e Lodge (a Cápsula segue as 6 etapas do seu lote 1)") + table(["Etapa", "O que", "Lote"], seq, "small")
    risks = [("Estrutura fora de geometria antes da lona", "rugas, sobretensão, lona reprovada", "etapa 7 obrigatória com estação total; liberação assinada"), ("Peça que não cabe no 4x4", "kit parado na estrada", "regra ≤ 4,80 m / ≤ 400 kg por volume aplicada nas listas de peças"), ("Solda em campo", "galvanização destruída, corrosão", "todas as ligações parafusadas; peças chegam prontas"), ("Lona cortada sem compensação / sem form-finding", "lona curta ou frouxa", "confeccionista entrega padronagem e laudo biaxial antes de cortar"), ("Vidro medido no projeto e não na estrutura", "vidro não encaixa", "medição após fit test ou no sítio, ± 3 mm"), ("Cooktop e forno sem circuito dedicado", "disjuntor geral desarma", "C13 e C14 dedicados, ramal 16 mm², geral 50 A"), ("Marcenaria fixada na membrana", "furos, infiltração", "só cantoneiras nos arcos; gabarito da seção"), ("Vento durante içamento / lona", "acidente", "limite 30 km/h; anemômetro no sítio"), ("Concreto em montanha", "custo e prazo", "estacas helicoidais ou sapatas pré-moldadas")]
    body += f'<h4>LÓGICA INVERSA · O QUE NÃO PODE ACONTECER</h4>{table(["Erro", "Consequência", "Antídoto"], risks, "xsmall")}'
    D.page(body, "Sequência integrada e riscos", "flow", code="ZG-MP-05")
    # validação e índice dos anexos
    body = h("VALIDAÇÃO DE ENGENHARIA E PRÓXIMOS PASSOS", f"o que precisa de engenheiro antes de contratar · {WARN}") + ul(["Cálculo estrutural (NBR 8800 / 6123): arcos, Bico em balanço, mastros e coroas, pilares e caibros, anéis, cabos; fundações por sondagem", "Form-finding e análise da membrana (pré-tensão, flechas, uplift); compensação do tecido", "Projeto elétrico e hidráulico executivo (NBR 5410 / 5626); climatização", "Projeto legal e aprovação municipal / ambiental por sítio", "Revisão REV 01: consolidar as respostas do brief (ZG-BRF-001) e os interiores dos outros 3 modelos"])
    body += f'<h4>ÍNDICE DOS ANEXOS · 16 DOCUMENTOS DE LOTE</h4>{table(["Documento", "Modelo", "Lote", "Páginas"], [(esc(d.code), esc(MODELS[d.model]["name"]), esc(d.title), len(d.pages) + 1) for d in lot_docs], "small")}'
    body += '<p class="note">Arquivos separados em 06_LOTES/ (HTML e PDF por lote) e anexados a seguir, na ordem Casulo → Safari → Lodge 38 → Cápsula, lotes 1 a 4.</p>'
    D.page(body, "Validação e anexos", "flow", code="ZG-MP-06")
    return D

# =============================================================================== one-pager
ONE_CSS = """
.one{padding:9mm 12mm 8mm} .one .top{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:1px solid var(--ink);padding-bottom:6px;margin-bottom:8px}
.one h1{margin:0;font-size:26px;font-weight:200;letter-spacing:.22em;line-height:1.05} .one .tag{font-size:8px;letter-spacing:.3em;color:var(--earth);margin-top:4px}
.one .claim{font-size:9.5px;line-height:1.55;max-width:300mm;margin:0 0 6px}
.one .models{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:4px 0 8px} .one .models div{border:1px solid var(--sand);padding:0 0 6px;background:#FBF6EE} .one .models img{width:100%;height:36mm;object-fit:cover;display:block} .one .models .svgbox{height:36mm;overflow:hidden;background:#F3EDE0} .one .models .svgbox svg{width:100%;height:auto;margin-top:-4mm}
.one .models b{display:block;font-size:9.5px;letter-spacing:.2em;padding:6px 8px 2px} .one .models p{margin:0;padding:0 8px;font-size:7.6px;line-height:1.45;color:var(--ink)} .one .models em{display:block;padding:2px 8px 0;font-size:7px;letter-spacing:.14em;color:var(--earth);font-style:normal}
.one .lots{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:8px} .one .lots div{border-top:2px solid var(--ink);padding-top:4px} .one .lots b{display:block;font-size:8.5px;letter-spacing:.18em} .one .lots p{margin:2px 0 0;font-size:7.4px;line-height:1.45}
.one .bottom{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:12px;font-size:7.4px;line-height:1.45} .one .bottom b{display:block;font-size:8px;letter-spacing:.18em;margin-bottom:3px} .one .bottom ul{margin:0;padding-left:10px}
.one .foot1{position:absolute;left:12mm;right:12mm;bottom:4mm;display:flex;justify-content:space-between;font-size:6.5px;letter-spacing:.2em;color:var(--earth)}
"""
def one_pager():
    D = Doc("ZG-ONE-001", "ONE-PAGER")
    cards = ""
    for m, M in MODELS.items():
        pic = f'<div class="svgbox">{svg_inline(M["hero"])}</div>' if M["hero"].endswith(".svg") else img(M["hero"])
        cards += f'<div>{pic}<b>{esc(M["name"])}</b><em>{esc(M["cat"])} · {esc(M["family"])}</em><p>{esc(M["dims"])} · {fmt(M["area_int"], 1)} m² internos + {fmt(M["area_ext"], 1)} m² de deck · {esc(M["guests"])} hóspedes · montagem em {M["days"]} dias</p></div>'
    lots = "".join(f'<div><b>LOTE {n} · {esc(t)}</b><p>{esc(s)}</p></div>' for n, (t, s) in LOTS.items())
    body = f'''<div class="one"><div class="top"><div><div style="display:flex;align-items:center;gap:6mm;margin-bottom:6px">{zion_mark_html("9mm", color="#1B2117")}{zion_logo_html("9mm", color="#1B2117")}</div><h1>ZION GLAMPING COLLECTION</h1><div class="tag">CABIN DESIGN &amp; ENGINEERING SYSTEM · ONE-PAGER · {REV} · {DATE}</div></div>
<div style="text-align:right;font-size:7.5px;line-height:1.6;letter-spacing:.1em;color:var(--earth)">4 MODELOS PROPRIETÁRIOS<br>4 LOTES DE CONTRATAÇÃO<br>KITS MODULARES PARA MONTANHA<br>SEM CONCRETO · SEM SOLDA EM CAMPO · SEM GUINDASTE</div></div>
<p class="claim">Uma linha de unidades de hospedagem industrializadas: estrutura tubular em aço galvanizado, lona PVDF tensionada, vidro e madeira sobre deck em estacas helicoidais. Cada modelo é um kit numerado, comprado em quatro lotes separados (deck e infra · ferro · lona e vidro · mobília) e montado por uma equipe de cinco pessoas sem guindaste. Geometria única em código: desenhos, padrões de corte da lona, listas de peças e 3D nascem do mesmo modelo.</p>
<div class="models">{cards}</div><div class="lots">{lots}</div>
<div class="bottom"><div><b>PRINCÍPIOS DE MODULARIDADE</b><ul>{"".join(f"<li><b style='display:inline;font-size:7.4px;letter-spacing:0'>{esc(a)}:</b> {esc(b[:150])}{'…' if len(b) > 150 else ''}</li>" for a, b in MODULAR[:5])}</ul></div>
<div><b>O QUE JÁ EXISTE</b><ul><li>Projeto arquitetônico (pranchas PA-00 a PA-14) e DXF dos 3 modelos + conceito da Cápsula</li><li>Documento técnico ZG-TEC-001 (80 p) e interiores do Casulo ZC-INT-001</li><li>Padrões de corte das lonas e forros dos 4 modelos (SVG, DXF, XLSX)</li><li>Listas de peças ferro a ferro, BOM, manual de montagem em 17 etapas, 3D e renders</li><li>16 documentos de lote + master plan ZG-MP-001</li></ul></div>
<div><b>PRÓXIMOS PASSOS</b><ul><li>Responder o brief ZG-BRF-001 (15 perguntas) e fechar a REV 01</li><li>Cálculo estrutural e form-finding com engenheiro (ART)</li><li>RFQ dos 4 lotes do Casulo (piloto) e fit test do primeiro pórtico</li><li>Interiores do Safari, Lodge e Cápsula com o método do Casulo</li><li>Protótipo do Casulo em sítio de montanha</li></ul><b style="margin-top:6px">CRONOGRAMA-ALVO</b>projeto executivo 3 sem · fabricação 6 sem · fundação 3 sem (paralelo) · montagem 2 sem · entrega na semana 13</div></div>
<div class="foot1"><span>ZION HOTEL GROUP INTERNATIONAL · ZION GLAMPING COLLECTION</span><span>PROJETO PRELIMINAR · SEM PREÇOS · ⚠️ VALIDAÇÃO DE ENGENHARIA OBRIGATÓRIA</span><span>ZG-ONE-001</span></div></div>'''
    D.pages.append(f'<section class="page">{body}</section>')
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · One-pager</title><style>{CSS}{ONE_CSS}</style></head><body>{D.pages[0]}</body></html>'


# =============================================================================== one-pager de cotação por modelo
ONE_M_CSS = """
.om{padding:8mm 11mm 7mm;font-size:7.6px;line-height:1.45} .om .top{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.2px solid var(--ink);padding-bottom:5px;margin-bottom:6px}
.om h1{margin:0;font-size:24px;font-weight:200;letter-spacing:.22em;line-height:1} .om .tag{font-size:7.5px;letter-spacing:.28em;color:var(--earth);margin-top:4px}
.om .grid{display:grid;grid-template-columns:78mm 1fr;gap:8px;margin-bottom:6px} .om .hero img{width:100%;height:52mm;object-fit:cover;display:block;border:1px solid var(--sand)} .om .hero .svgbox{height:52mm;overflow:hidden;background:#F3EDE0;border:1px solid var(--sand)} .om .hero .svgbox svg{width:100%;height:auto;margin-top:-3mm}
.om .stats{display:grid;grid-template-columns:repeat(5,1fr);gap:4px} .om .stats div{border-top:2px solid var(--ink);padding-top:3px} .om .stats b{display:block;font-size:11.5px;font-weight:600;letter-spacing:.02em;line-height:1.1} .om .stats span{display:block;font-size:6.6px;letter-spacing:.14em;color:var(--earth);text-transform:uppercase;margin-top:1px}
.om .claim{margin:5px 0 0;font-size:8px;line-height:1.5}
.om .lots{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-bottom:6px} .om .lots>div{border:1px solid var(--sand);background:#FBF6EE;padding:5px 6px 6px} .om .lots b.t{display:block;font-size:8px;letter-spacing:.18em;border-bottom:1px solid var(--ink);padding-bottom:3px;margin-bottom:3px} .om .lots em{display:block;font-style:normal;font-size:6.6px;letter-spacing:.1em;color:var(--earth);margin-bottom:3px}
.om .lots ul{margin:0 0 3px;padding-left:9px} .om .lots li{margin:0 0 1px} .om .lots .doc{font-size:6.6px;color:var(--earth);letter-spacing:.06em;margin-top:3px;border-top:1px dotted var(--sand);padding-top:2px}
.om .bottom{display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:10px} .om .bottom>div{min-width:0} .om .bottom b{display:block;font-size:7.6px;letter-spacing:.18em;margin-bottom:2px} .om ul.omu,.om ol.oml{margin:0;padding-left:10px;list-style:disc;display:block} .om ol.oml{list-style:decimal} .om .omu li,.om .oml li{display:list-item;margin:0 0 2px;text-align:left}
.om .foot1{position:absolute;left:11mm;right:11mm;bottom:4mm;display:flex;justify-content:space-between;font-size:6.3px;letter-spacing:.2em;color:var(--earth)}
"""
def model_numbers(m):
    M = MODELS[m]; parts = M["parts"]()
    steel = sum(p["peso_total"] for p in parts if isinstance(p["peso_total"], (int, float)) and p["cod"][0] in M["struct_prefix"])
    base = sum(p["peso_total"] for p in parts if isinstance(p["peso_total"], (int, float)) and M["base_prefix"] and p["cod"][0] in M["base_prefix"])
    pats = lona.dedupe(lona.PATTERNS[m]())
    ext = sum(p.area * p.qty for p in pats if p.group != "interna"); inn = sum(p.area * p.qty for p in pats if p.group == "interna")
    n_ext = sum(p.qty for p in pats if p.group != "interna"); n_inn = sum(p.qty for p in pats if p.group == "interna")
    glass = sum(w * hh * nn for (_, _, w, hh, nn, _, _) in M["esq"]); n_esq = sum(nn for (_, _, _, _, nn, _, _) in M["esq"])
    piles = len(M["piles"]())
    tr = M["transport"](); tr = tr["items"] if isinstance(tr, dict) else tr
    kg = sum(t[3] for t in tr); m3 = sum(t[2] for t in tr)
    n_ffe = len(ffe.rows(m, 1)); n_struct = len([p for p in parts if p["cod"][0] in M["struct_prefix"]])
    return dict(steel=steel, base=base, ext=ext, inn=inn, n_ext=n_ext, n_inn=n_inn, glass=glass, n_esq=n_esq, piles=piles, kg=kg, m3=m3, vols=len(tr), n_ffe=n_ffe, n_struct=n_struct)

def one_pager_model(m):
    M = MODELS[m]; tag = M["tag"]; N = model_numbers(m); code = f"{tag}-ONE-001"
    pic = f'<div class="svgbox">{svg_inline(M["hero"])}</div>' if M["hero"].endswith(".svg") else img(M["hero"])
    rigid = m == "capsule"
    L2 = {"cocoon": ["9 arcos elípticos calandrados Ø60,3 + Espinha e longarinas", "Bico: cumeeira Ø114,3, bordas Ø60,3, costela Ø48,3, 2 tirantes Ø12", "Chapas de base, luvas, talões, parafusos 8.8 galv."],
          "zenith": ["2 mastros em tramos (5,80 / 4,60 m) com coroas", "Pilares, anel de beiral, postes externos", "Cabos inox, esticadores, chapas e luvas"],
          "lodge": ["8 pilares + anel de beiral em 8 segmentos", "8 caibros + Lanterna Zion (anel superior e montantes)", "Postes da vela, chapas, luvas, parafusos"],
          "capsule": ["12 anéis calandrados Ø3,20 m + 7 longarinas", "Chassi de piso e 4 pés telescópicos", "Aros do Visor e do Anel de Luz, olhais de içamento"]}[m]
    L3 = {"cocoon": [f"Lona externa PVDF tipo II: {N['n_ext']} painéis = {fmt(N['ext'], 0)} m² (P0 Bico, P1 a P8)", f"Forro Trevira CS: {N['n_inn']} painéis = {fmt(N['inn'], 0)} m²", "Keder duplo nos arcos, bolsas de tubo, clamps, cabos", f"Vidros: {N['n_esq']} esquadrias = {fmt(N['glass'], 1)} m² (fachada, Espinha, 6 Olhos, porta)"],
          "zenith": [f"Cobertura tensionada: {N['n_ext']} faixas soldadas = {fmt(N['ext'], 0)} m²", f"Forro: {N['n_inn']} painéis = {fmt(N['inn'], 0)} m²", "Bolsa de cabo na borda, clamps nos cumes", f"Vidros e fechamentos: {N['n_esq']} esquadrias = {fmt(N['glass'], 1)} m²"],
          "lodge": [f"Cobertura em {N['n_ext']} gomos iguais = {fmt(N['ext'], 0)} m²", f"Forro em gomos: {fmt(N['inn'], 0)} m²", "Clamp da lanterna, bolsa de cabo no beiral", f"Vidros: {N['n_esq']} esquadrias = {fmt(N['glass'], 1)} m²"],
          "capsule": [f"Painéis de ACM curvado: {N['n_ext']} = {fmt(N['ext'], 0)} m²", f"Compensado curvado interno: {fmt(N['inn'], 0)} m²", "PIR 60 mm + barreira de vapor", f"Visor e Anel de Luz em vidro curvo laminado: {fmt(N['glass'], 1)} m²"]}[m]
    L1 = {"cocoon": [f"{N['piles']} estacas helicoidais Ø76 com cabeçote ajustável", f"Grelha U 150 x 60 galv.: ≈ {fmt(N['base'], 0)} kg", f"Piso isolado {fmt(M['area_int'], 0)} m² + deck cumaru {fmt(M['area_ext'], 0)} m²", "Água/esgoto/elétrica (geral 50 A), boiler, condensadora"],
          "zenith": [f"{N['piles']} estacas helicoidais com cabeçote", f"Grelha U 150 x 60 galv.: ≈ {fmt(N['base'], 0)} kg", f"Piso {fmt(M['area_int'], 0)} m² + terraço {fmt(M['area_ext'], 0)} m²", "Instalações completas"],
          "lodge": [f"{N['piles']} estacas helicoidais com cabeçote", f"Grelha U 150 x 60 galv.: ≈ {fmt(N['base'], 0)} kg", f"Piso octogonal {fmt(M['area_int'], 0)} m² + deck em 3 faces {fmt(M['area_ext'], 0)} m²", "Instalações completas"],
          "capsule": ["4 estacas helicoidais ou 4 sapatas pré-moldadas", "4 pés telescópicos Ø101,6 (curso 0,40 m)", f"Deck acoplado {fmt(M['area_ext'], 1)} m² + escada", "Engates rápidos de água, esgoto e energia"]}[m]
    L4 = {"cocoon": [f"{len(MA)} peças de marcenaria acoplada (MA-01 mini cozinha 2,00 m a MA-08)", f"{N['n_ffe']} itens de FF&E (mobiliário, luminárias, têxteis, equipamentos)", "Módulos ≤ 0,95 x 2,10 m e ≤ 60 kg"],
          "zenith": ["Marcenaria acoplada ao totem do mastro e closet em L", f"{N['n_ffe']} itens de FF&E", "Módulos ≤ 0,95 x 2,10 m e ≤ 60 kg"],
          "lodge": ["Parede-cabeceira ripada, closet e café nas faces opacas", f"{N['n_ffe']} itens de FF&E", "Módulos ≤ 0,95 x 2,10 m e ≤ 60 kg"],
          "capsule": ["Marcenaria curva acoplada aos anéis (cama, banco, bancada, banho)", f"{N['n_ffe']} itens de FF&E", "Instalado em oficina antes do transporte"]}[m]
    forn = {1: "Empreiteiro de estacas helicoidais + montadores + eletricista / encanador", 2: "Serralheria com calandra de tubos, solda MIG/TIG e galvanizador parceiro", 3: ("Fabricante de ACM curvado + vidraceiro de vidro curvo" if rigid else "Confeccionista de lonas / tendas (solda HF) + vidraceiro"), 4: "Marcenaria + fornecedores de FF&E"}
    steel_txt = f"≈ {fmt(N['steel'], 0)} kg de aço galv. em {N['n_struct']} tipos de peça" if N["steel"] else "casco monocoque: ver lista K01 em diante no lote 2"
    lots = ""
    for n, items, extra in ((1, L1, ""), (2, L2, f"<li><b>{steel_txt}</b></li>"), (3, L3, ""), (4, L4, "")):
        lots += f'<div><b class="t">LOTE {n} · {esc(LOTS[n][0])}</b><em>{esc(forn[n])}</em><ul>{extra}{"".join(f"<li>{esc(i)}</li>" for i in items)}</ul><div class="doc">Documento completo: {tag}-LOT{n}-001 (PDF)</div></div>'
    stats = [(esc(M["dims"].split(" · ")[0]), "dimensões"), (f"{fmt(M['area_int'], 0)} + {fmt(M['area_ext'], 0)} m²", "interno + deck"), (f"{fmt(N['steel'] + N['base'], 0) if N['steel'] else '≈ 4.200'} kg", "aço galvanizado" if N["steel"] else "casco completo"), (f"{fmt(N['ext'] + N['inn'], 0)} m²", "ACM + interno" if rigid else "lona + forro"), (f"{fmt(N['glass'], 1)} m²", "vidro"),
             (f"{N['piles']}", "estacas"), (f"{M['days']} dias", "montagem"), (f"{N['vols']} vol · {fmt(N['m3'], 0)} m³", "transporte"), (f"{fmt(N['kg'] / 1000, 1)} t", "peso total"), (esc(M["guests"]), "hóspedes")]
    st = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in stats)
    claim = f'{esc(M["family"])}: estrutura tubular em aço galvanizado a fogo, {"casco em ACM curvado" if rigid else "lona PVDF tensionada"}, vidro e madeira sobre deck em estacas helicoidais. Tudo chega em kit numerado (peças ≤ 4,80 m, ≤ 120 kg), sem concreto, sem solda em campo e sem guindaste{"; a Cápsula viaja inteira em prancha e exige acesso de caminhão a 30 m do pouso" if rigid else ""}. Este one-pager resume o que cotar em cada lote; o documento completo de cada lote traz listas peça a peça, padrões de corte, detalhes e o RFQ.'
    top = f'<div class="top"><div><div style="display:flex;align-items:center;gap:5mm;margin-bottom:5px">{zion_mark_html("8mm", color="#1B2117")}{zion_logo_html("8mm", color="#1B2117")}</div><h1>{esc(M["name"])}</h1><div class="tag">{esc(M["family"]).upper()} · ONE-PAGER DE COTAÇÃO · {code} · {REV} · {DATE}</div></div><div style="text-align:right;font-size:7px;line-height:1.6;letter-spacing:.1em;color:var(--earth)">4 LOTES · 4 FORNECEDORES<br>KIT NUMERADO PARA MONTANHA<br>SEM CONCRETO · SEM SOLDA EM CAMPO · SEM GUINDASTE<br>COTAÇÃO SEM PREÇOS DE REFERÊNCIA</div></div>'
    como = "<ol class=\"oml\">" + "".join(f"<li>{i}</li>" for i in ["Cotação por item e total, com prazo de fabricação, validade de 30 dias e impostos destacados; frete até Florianópolis / SC ou ponto de transbordo indicado.", "Lote 2: preço por kg e por peça, com calandra, solda, galvanização a fogo (NBR 6323) e pintura destacadas; informar raio mínimo da calandra e galvanizador.", "Lote 3: lona por m² confeccionado (por painel) + perfis e cabos por metro + instalação por dia de equipe; vidros por pano e esquadrias por unidade, com medição na estrutura montada.", "Lotes 1 e 4: estacas por ponto + cravação; grelha por kg; deck por m²; marcenaria por peça; FF&E por item."]) + "</ol>"
    envia = "<ul class=\"omu\">" + "".join(f"<li>{i}</li>" for i in ["Documento completo do lote (PDF) com escopo, interfaces, listas e RFQ", "DXF das peças e tabela de geometria dos arcos / caibros / anéis (lote 2)", "Padrões de corte DXF + XLSX e pranchas LN-01 a LN-90 (lote 3)", "Quadro de esquadrias e detalhes DET-01 a DET-13", "Modelo 3D (GLB) e visualizador"]) + "</ul>"
    regras = "<ul class=\"omu\">" + "".join(f"<li>{i}</li>" for i in ["Fit test em fábrica de um pórtico / anel completo antes de galvanizar; inspeção Zion antes da expedição", "Tolerâncias: retas ± 2 mm · calandradas ± 5 mm no gabarito · topo montado ± 15 mm", "Lona: compensação e padronagem pelo confeccionista (laudo biaxial); sem rugas após tensionar; teste de água", f"Alvo: projeto executivo 3 sem · fabricação 6 sem · fundação 3 sem (paralelo) · montagem {M['days']} dias", WARN]) + "</ul>"
    body = f'<div class="om">{top}<div class="grid"><div class="hero">{pic}</div><div><div class="stats">{st}</div><p class="claim">{claim}</p></div></div><div class="lots">{lots}</div><div class="bottom"><div><b>COMO COTAR</b>{como}</div><div><b>A ZION ENVIA</b>{envia}</div><div><b>REGRAS E PRAZOS</b>{regras}</div></div><div class="foot1"><span>ZION HOTEL GROUP INTERNATIONAL · ZION GLAMPING COLLECTION · ZION GLAMPING STORE</span><span>PROJETO PRELIMINAR · SEM PREÇOS · TODA ESPECIFICAÇÃO ESTRUTURAL SUJEITA A VALIDAÇÃO DE ENGENHEIRO (ART)</span><span>{code}</span></div></div>'
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · {code} · One-pager de cotação</title><style>{CSS}{ONE_M_CSS}</style></head><body><section class="page">{body}</section></body></html>'

# =============================================================================== teaser de cotação por modelo (multipágina)
TEASER_CSS = """
.tz .stats{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin:6px 0 10px} .tz .stats div{border-top:2px solid var(--ink);padding-top:5px} .tz .stats b{display:block;font-size:17px;font-weight:600;line-height:1.1} .tz .stats span{display:block;font-size:7.5px;letter-spacing:.16em;color:var(--earth);text-transform:uppercase;margin-top:2px}
.tz .lots{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:4px 0 10px} .tz .lots>div{border:1px solid var(--sand);background:#FBF6EE;padding:8px 9px 9px;font-size:9px;line-height:1.5} .tz .lots b.t{display:block;font-size:10px;letter-spacing:.18em;border-bottom:1px solid var(--ink);padding-bottom:4px;margin-bottom:5px} .tz .lots em{display:block;font-style:normal;font-size:8px;letter-spacing:.08em;color:var(--earth);margin-bottom:5px}
.tz .lots ul{margin:0 0 4px;padding-left:11px} .tz .lots li{margin:0 0 2px} .tz .lots .doc{font-size:7.8px;color:var(--earth);letter-spacing:.06em;margin-top:5px;border-top:1px dotted var(--sand);padding-top:3px}
.tz .claim{font-size:10.5px;line-height:1.6;margin:0 0 6px} .tz .three{display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:14px;font-size:9.2px;line-height:1.5} .tz .three>div{min-width:0} .tz .three b{display:block;font-size:9px;letter-spacing:.18em;margin-bottom:4px}
.tz ul.omu,.tz ol.oml{margin:0;padding-left:12px;list-style:disc;display:block} .tz ol.oml{list-style:decimal} .tz .omu li,.tz .oml li{display:list-item;margin:0 0 3px;text-align:left}
.tz .renders{display:grid;grid-template-columns:1fr 1fr;gap:8px} .tz .renders img{width:100%;height:78mm;object-fit:cover;display:block;border:1px solid var(--sand)} .tz .renders figcaption{font-size:7.5px;letter-spacing:.18em;color:var(--earth);margin:3px 0 0;text-transform:uppercase}
.page.cover .heroimg{position:absolute;right:0;top:0;bottom:0;width:58%;object-fit:cover;opacity:.92} .page.cover .heroimg.svgbox{background:#F3EDE0;display:flex;align-items:center;justify-content:center;overflow:hidden} .page.cover .heroimg.svgbox svg{width:100%;height:auto} .page.cover .coverbox.left{width:44%;padding:18mm 16mm}
"""
def teaser_model(m):
    M = MODELS[m]; tag = M["tag"]; N = model_numbers(m); code = f"{tag}-ONE-001"; rigid = m == "capsule"
    D = Doc(code, "TEASER DE COTAÇÃO", m)
    # capa com render
    hero = f'<div class="heroimg svgbox">{svg_inline(M["hero"])}</div>' if M["hero"].endswith(".svg") else f'<img class="heroimg" src="../{M["hero"].replace("/renders/web/", "/renders/web/deck/")}" alt="">'
    D.pages.append(f'''<section class="page cover">{hero}<div class="coverbox left"><div class="brand">{zion_mark_html("13mm", color="#FEF5F0", style="margin-right:6mm")}{zion_logo_html("13mm", color="#FEF5F0")}</div><div class="sub">ZION GLAMPING COLLECTION · ZION GLAMPING STORE</div>
<h1>{esc(M["name"]).replace("ZION ", "ZION<br>")}</h1><h3>{esc(M["family"]).upper()} · TEASER DE COTAÇÃO · {code} · {REV} · {DATE}</h3>
<p class="lead">{esc(M["dims"])} · {fmt(M["area_int"], 0)} m² internos + {fmt(M["area_ext"], 0)} m² de deck · {esc(M["guests"])} hóspedes · montagem em {M["days"]} dias. Kit numerado em 4 lotes: deck e infra · estrutura metálica · lonas, revestimentos e vidros · mobílias. Este teaser mostra o projeto (plantas, cortes, camadas, estrutura, lona, esquadrias) e o que cotar em cada lote.</p>
<p class="rule">Sem preços. Projeto preliminar; toda especificação estrutural sujeita a validação de engenheiro (ART). Os documentos completos de cada lote ({tag}-LOT1 a LOT4-001) acompanham este teaser com listas peça a peça, padrões de corte DXF e RFQ.</p></div></section>''')
    # números e lotes
    L2 = {"cocoon": ["9 arcos elípticos calandrados Ø60,3 + Espinha e longarinas", "Bico: cumeeira Ø114,3, bordas Ø60,3, costela Ø48,3, 2 tirantes Ø12", "Chapas de base, luvas, talões, parafusos 8.8 galvanizados"],
          "zenith": ["2 mastros em tramos (5,80 / 4,60 m) com coroas", "Pilares, anel de beiral, postes externos", "Cabos inox, esticadores, chapas e luvas"],
          "lodge": ["8 pilares + anel de beiral em 8 segmentos", "8 caibros + Lanterna Zion (anel superior e montantes)", "Postes da vela, chapas, luvas, parafusos"],
          "capsule": ["12 anéis calandrados Ø3,20 m + 7 longarinas", "Chassi de piso e 4 pés telescópicos", "Aros do Visor e do Anel de Luz, olhais de içamento"]}[m]
    L3 = {"cocoon": [f"Lona externa PVDF tipo II: {N['n_ext']} painéis = {fmt(N['ext'], 0)} m² (P0 Bico, P1 a P8)", f"Forro Trevira CS: {N['n_inn']} painéis = {fmt(N['inn'], 0)} m²", "Keder duplo nos arcos, bolsas de tubo, clamps, cabos", f"Vidros: {N['n_esq']} esquadrias = {fmt(N['glass'], 1)} m² (fachada, Espinha, 6 Olhos, porta)"],
          "zenith": [f"Cobertura tensionada: {N['n_ext']} faixas soldadas = {fmt(N['ext'], 0)} m²", f"Forro: {N['n_inn']} painéis = {fmt(N['inn'], 0)} m²", "Bolsa de cabo na borda, clamps nos cumes", f"Vidros e fechamentos: {N['n_esq']} esquadrias = {fmt(N['glass'], 1)} m²"],
          "lodge": [f"Cobertura em {N['n_ext']} gomos iguais = {fmt(N['ext'], 0)} m²", f"Forro em gomos: {fmt(N['inn'], 0)} m²", "Clamp da lanterna, bolsa de cabo no beiral", f"Vidros: {N['n_esq']} esquadrias = {fmt(N['glass'], 1)} m²"],
          "capsule": [f"Painéis de ACM curvado: {N['n_ext']} = {fmt(N['ext'], 0)} m²", f"Compensado curvado interno: {fmt(N['inn'], 0)} m²", "PIR 60 mm + barreira de vapor", f"Visor e Anel de Luz em vidro curvo laminado: {fmt(N['glass'], 1)} m²"]}[m]
    L1 = {"cocoon": [f"{N['piles']} estacas helicoidais Ø76 com cabeçote ajustável", f"Grelha U 150 x 60 galv.: ≈ {fmt(N['base'], 0)} kg", f"Piso isolado {fmt(M['area_int'], 0)} m² + deck cumaru {fmt(M['area_ext'], 0)} m²", "Água / esgoto / elétrica (geral 50 A), boiler, condensadora"],
          "zenith": [f"{N['piles']} estacas helicoidais com cabeçote", f"Grelha U 150 x 60 galv.: ≈ {fmt(N['base'], 0)} kg", f"Piso {fmt(M['area_int'], 0)} m² + terraço {fmt(M['area_ext'], 0)} m²", "Instalações completas"],
          "lodge": [f"{N['piles']} estacas helicoidais com cabeçote", f"Grelha U 150 x 60 galv.: ≈ {fmt(N['base'], 0)} kg", f"Piso octogonal {fmt(M['area_int'], 0)} m² + deck em 3 faces {fmt(M['area_ext'], 0)} m²", "Instalações completas"],
          "capsule": ["4 estacas helicoidais ou 4 sapatas pré-moldadas", "4 pés telescópicos Ø101,6 (curso 0,40 m)", f"Deck acoplado {fmt(M['area_ext'], 1)} m² + escada", "Engates rápidos de água, esgoto e energia"]}[m]
    L4 = {"cocoon": [f"{len(MA)} peças de marcenaria acoplada (MA-01 mini cozinha 2,00 m a MA-08)", f"{N['n_ffe']} itens de FF&E (mobiliário, luminárias, têxteis, equipamentos)", "Módulos ≤ 0,95 x 2,10 m e ≤ 60 kg"],
          "zenith": ["Marcenaria acoplada ao totem do mastro e closet em L", f"{N['n_ffe']} itens de FF&E", "Módulos ≤ 0,95 x 2,10 m e ≤ 60 kg"],
          "lodge": ["Parede-cabeceira ripada, closet e café nas faces opacas", f"{N['n_ffe']} itens de FF&E", "Módulos ≤ 0,95 x 2,10 m e ≤ 60 kg"],
          "capsule": ["Marcenaria curva acoplada aos anéis (cama, banco, bancada, banho)", f"{N['n_ffe']} itens de FF&E", "Instalado em oficina antes do transporte"]}[m]
    forn = {1: "Empreiteiro de estacas helicoidais + montadores + eletricista / encanador", 2: "Serralheria com calandra de tubos, solda MIG/TIG e galvanizador parceiro", 3: ("Fabricante de ACM curvado + vidraceiro de vidro curvo" if rigid else "Confeccionista de lonas / tendas (solda HF) + vidraceiro"), 4: "Marcenaria + fornecedores de FF&E"}
    steel_txt = f"≈ {fmt(N['steel'], 0)} kg de aço galvanizado em {N['n_struct']} tipos de peça" if N["steel"] else "casco monocoque: lista K01 em diante no lote 2"
    lots = ""
    for n, items, extra in ((1, L1, ""), (2, L2, f"<li><b>{steel_txt}</b></li>"), (3, L3, ""), (4, L4, "")):
        lots += f'<div><b class="t">LOTE {n} · {esc(LOTS[n][0])}</b><em>{esc(forn[n])}</em><ul>{extra}{"".join(f"<li>{esc(i)}</li>" for i in items)}</ul><div class="doc">Documento completo: {tag}-LOT{n}-001 (PDF)</div></div>'
    stats = [(esc(M["dims"].split(" · ")[0]), "dimensões"), (f"{fmt(M['area_int'], 0)} + {fmt(M['area_ext'], 0)} m²", "interno + deck"), (f"{fmt(N['steel'] + N['base'], 0) if N['steel'] else '≈ 4.200'} kg", "aço galvanizado" if N["steel"] else "casco completo"), (f"{fmt(N['ext'] + N['inn'], 0)} m²", "ACM + interno" if rigid else "lona + forro"), (f"{fmt(N['glass'], 1)} m²", "vidro"),
             (f"{N['piles']}", "estacas"), (f"{M['days']} dias", "montagem"), (f"{N['vols']} vol · {fmt(N['m3'], 0)} m³", "transporte"), (f"{fmt(N['kg'] / 1000, 1)} t", "peso total"), (esc(M["guests"]), "hóspedes")]
    st = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in stats)
    claim = f'{esc(M["family"])}: estrutura tubular em aço galvanizado a fogo, {"casco em ACM curvado" if rigid else "lona PVDF tensionada"}, vidro e madeira sobre deck em estacas helicoidais. Tudo chega em kit numerado (peças ≤ 4,80 m, ≤ 120 kg), sem concreto, sem solda em campo e sem guindaste{"; a Cápsula viaja inteira em prancha e exige acesso de caminhão a 30 m do pouso" if rigid else ""}.'
    sub = M["name"] + " · " + M["family"] + " · " + M["dims"]
    D.page('<div class="tz">' + h("EM NÚMEROS · O QUE CADA LOTE COTA", sub) + '<div class="stats">' + st + '</div><p class="claim">' + claim + '</p><div class="lots">' + lots + '</div></div>', "Números e lotes", code=f"{code}-01")
    # renders
    if not M["hero"].endswith(".svg"):
        base = M["hero"].rsplit("/", 1)[0]; pre = m
        figs = "".join(f'<figure style="margin:0">{img(f"{base}/{pre}_{v}.jpg")}<figcaption>{c}</figcaption></figure>' for v, c in (("ext_front", "Fachada e deck"), ("ext_side", "Lateral"), ("night", "Noite"), ("int_living", "Interior · estar")))
        D.page(f'<div class="tz">{h("RENDERS", "modelo 3D paramétrico do projeto · materiais e luz de estudo")}<div class="renders">{figs}</div></div>', "Renders", code=f"{code}-02")
    # referências reais (fotos de mercado em <modelo>/referencias/)
    refdir = os.path.join(ROOT, m, "referencias")
    refs = sorted(f for f in os.listdir(refdir) if f.lower().endswith((".jpg", ".jpeg", ".png"))) if os.path.isdir(refdir) else []
    if refs:
        caps = {"zenith": "Pavilhão tensionado com cume e beiral em balanço sobre a encosta, deck em aço e madeira, piscina de borda, quarto aberto para a mata: a experiência que o Zion Safari entrega, com estrutura em kit e lona PVDF."}
        figs = "".join(f'<figure style="margin:0"><img src="../{m}/referencias/{f}" alt="" style="height:70mm"><figcaption>REFERÊNCIA DE MERCADO {i + 1:02d}</figcaption></figure>' for i, f in enumerate(refs[:4]))
        D.page(f'<div class="tz">{h("REFERÊNCIAS REAIS", "fotos de mercado que mostram a experiência-alvo · não são produto Zion · uso interno de direção de projeto")}<div class="renders">{figs}</div><p class="claim" style="margin:6px 0 0;font-size:9.5px">{esc(caps.get(m, ""))}</p></div>', "Referências reais", code=f"{code}-02b")
    # pranchas
    sheets = {"cocoon": [("02_planta_humanizada", "Planta humanizada"), ("06_corte_longitudinal", "Corte longitudinal"), ("04_elevacao_frontal", "Elevação frontal com o Bico"), ("13_camadas_construtivas", "Camadas construtivas (lote 3)"), ("12_estrutura_isometrica", "Estrutura metálica (lote 2)"), ("10_modelo_explodido", "Modelo explodido: os 4 lotes")],
              "zenith": [("02_planta_humanizada", "Planta humanizada"), ("06_corte_longitudinal", "Corte longitudinal"), ("04_elevacao_frontal", "Elevação frontal"), ("13_camadas_construtivas", "Camadas construtivas (lote 3)"), ("12_estrutura_isometrica", "Estrutura metálica (lote 2)"), ("10_modelo_explodido", "Modelo explodido: os 4 lotes")],
              "lodge": [("02_planta_humanizada", "Planta humanizada"), ("06_corte_longitudinal", "Corte longitudinal"), ("04_elevacao_frontal", "Elevação frontal"), ("13_camadas_construtivas", "Camadas construtivas (lote 3)"), ("12_estrutura_isometrica", "Estrutura metálica (lote 2)"), ("10_modelo_explodido", "Modelo explodido: os 4 lotes")],
              "capsule": [("01_conceito", "Prancha de conceito"), ("08_isometrica", "Isométrica")]}[m]
    k = 3
    for f, t in sheets:
        D.sheet_page(f"{m}/desenhos/{f}.svg", f"{code}-{k:02d}", t, "ver prancha", M["name"]); k += 1
    det = {"cocoon": "detalhes/DET-10_arcos_cocoon.svg", "zenith": "detalhes/DET-11_mastros_zenith.svg", "lodge": "detalhes/DET-12_lanterna_lodge.svg", "capsule": None}[m]
    if det: D.sheet_page(det, f"{code}-{k:02d}", "Detalhe da estrutura para o serralheiro (lote 2)", "ver prancha", M["name"]); k += 1
    D.sheet_page(f"{m}/lona/LN-01_mapa_paineis.svg", f"{code}-{k:02d}", "Mapa de painéis da lona (lote 3) · padrões de corte em DXF", "ver prancha", M["name"]); k += 1
    if not rigid: D.sheet_page(f"{m}/projeto/PA-09_quadro_esquadrias.svg", f"{code}-{k:02d}", "Quadro de esquadrias e vidros (lote 3)", "ver prancha", M["name"]); k += 1
    D.sheet_page("detalhes/DET-04_fundacao.svg", f"{code}-{k:02d}", "Fundação em estacas helicoidais (lote 1)", "ver prancha", M["name"]); k += 1
    # como cotar
    como = "<ol class=\"oml\">" + "".join(f"<li>{i}</li>" for i in ["Cotação por item e total, com prazo de fabricação, validade de 30 dias e impostos destacados; frete até Florianópolis / SC ou ponto de transbordo indicado.", "Lote 2: preço por kg e por peça, com calandra, solda, galvanização a fogo (NBR 6323) e pintura destacadas; informar raio mínimo da calandra e galvanizador.", "Lote 3: lona por m² confeccionado (por painel) + perfis e cabos por metro + instalação por dia de equipe; vidros por pano e esquadrias por unidade, com medição na estrutura montada.", "Lotes 1 e 4: estacas por ponto + cravação; grelha por kg; deck por m²; marcenaria por peça; FF&E por item.", "Amostra antes da série: um arco calandrado (lote 2) e um painel soldado com keder (lote 3)."]) + "</ol>"
    envia = "<ul class=\"omu\">" + "".join(f"<li>{i}</li>" for i in ["Documento completo do lote (PDF) com escopo, interfaces, listas peça a peça e RFQ", "DXF das peças e tabela de geometria dos arcos / caibros / anéis (lote 2)", "Padrões de corte DXF + XLSX e pranchas LN-01 a LN-90 (lote 3)", "Quadro de esquadrias e detalhes DET-01 a DET-13", "Modelo 3D (GLB) e visualizador no navegador"]) + "</ul>"
    regras = "<ul class=\"omu\">" + "".join(f"<li>{i}</li>" for i in ["Fit test em fábrica de um pórtico / anel completo antes de galvanizar; inspeção Zion antes da expedição", "Tolerâncias: retas ± 2 mm · calandradas ± 5 mm no gabarito · topo montado ± 15 mm", "Lona: compensação e padronagem pelo confeccionista (laudo biaxial); sem rugas após tensionar; teste de água", f"Alvo: projeto executivo 3 sem · fabricação 6 sem · fundação 3 sem (paralelo) · montagem {M['days']} dias", WARN]) + "</ul>"
    D.page(f'<div class="tz">{h("COMO COTAR · O QUE A ZION ENVIA · REGRAS", "retorno em 10 dias · validade 30 dias · sem preços de referência")}<div class="three"><div><b>COMO COTAR</b>{como}</div><div><b>A ZION ENVIA</b>{envia}</div><div><b>REGRAS E PRAZOS</b>{regras}</div></div></div>', "Como cotar", code=f"{code}-{k:02d}")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · {code} · Teaser de cotação</title><style>{CSS}{TEASER_CSS}</style></head><body>{"".join(D.pages)}</body></html>'

def build_one_pagers():
    for m in MODELS:
        path = os.path.join(OUT_DIR, f"{MODELS[m]['tag']}-ONE-001_Teaser_Cotacao.html"); open(path, "w", encoding="utf-8").write(teaser_model(m)); print(os.path.relpath(path, ROOT))


CSS = BASE_CSS + """
.cols4{columns:4;column-gap:12px} .cols4 h4{margin-top:2px;break-after:avoid}
.gantt{margin:6px 0 10px;font-size:7.5px} .gantt .gh{display:flex;margin-left:38%;width:60%;border-bottom:1px solid var(--sand)} .gantt .gh i{flex:1;font-style:normal;color:var(--earth);font-size:7px;text-align:left}
.gantt .gr{display:flex;align-items:center;min-height:16px;padding:2px 0;border-bottom:1px solid #F0E9DC} .gantt .gl{width:38%;padding-right:8px;line-height:1.15;font-size:7px} .gantt .gb{height:8px;background:var(--ink);opacity:.85} .gantt .gw{margin-left:6px;color:var(--earth);white-space:nowrap}
"""

def build():
    lot_docs = []
    for m in MODELS:
        for n in (1, 2, 3, 4):
            D = build_lot(m, n); lot_docs.append(D)
            path = os.path.join(OUT_DIR, f"{D.code}_{['Deck_Infra', 'Estrutura_Metalica', 'Lonas_Revestimentos_Vidros', 'Mobilias'][n - 1]}.html")
            open(path, "w", encoding="utf-8").write(D.html()); print(os.path.relpath(path, ROOT), len(D.pages) + 1, "páginas")
    MP = master_plan(lot_docs)
    allpages = MP.pages + [p for d in lot_docs for p in [d.pages[0]] + d.pages[1:]]
    toc = table(["Código", "Seção", "#Pág."], [(esc(c), esc(l), n) for c, l, n in MP.toc], "small")
    idx = f'<section class="page"><div class="head"><span>ZG-MP-001 · {REV}</span><span>ÍNDICE</span><span></span></div>{h("ÍNDICE DO MASTER PLAN")}{toc}<p class="note">Anexos: os 16 documentos de lote seguem após a seção ZG-MP-06, cada um com a sua capa.</p><div class="foot"><span>MASTER PLAN</span><span></span><span>{DATE} · 02</span></div></section>'
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · ZG-MP-001 · Master Plan</title><style>{CSS}</style></head><body>{allpages[0]}{idx}{"".join(allpages[1:])}</body></html>'
    path = os.path.join(OUT_DIR, "ZG-MP-001_Master_Plan.html"); open(path, "w", encoding="utf-8").write(doc); print(os.path.relpath(path, ROOT), len(allpages) + 1, "páginas", round(os.path.getsize(path) / 1e6, 1), "MB")
    path = os.path.join(OUT_DIR, "ZG-ONE-001_One_Pager.html"); open(path, "w", encoding="utf-8").write(one_pager()); print(os.path.relpath(path, ROOT))
    build_one_pagers()

if __name__ == "__main__":
    build_one_pagers() if "--one" in sys.argv else build()

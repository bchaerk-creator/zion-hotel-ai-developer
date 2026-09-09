# -*- coding: utf-8 -*-
"""ZION ARCHITECTURAL PRODUCT BOOK · gera o HTML (Cocoon primeiro, depois Zenith) e a planilha XLSX de orçamento.
Uso: python3 build_product_book.py [--inline]"""
import os, sys, base64
from geometry import Cocoon, Zenith
from bom import cocoon_bom, zenith_bom, ASSEMBLY
from product_book_data import (cocoon_parts, zenith_parts, COCOON_CONNECTIONS, ZENITH_CONNECTIONS, PRICES, LABOR_RATES, labor_hours,
                               bom_priced, budget, scale_factors, manual, FAB_SCHEDULE, SCENARIOS)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INLINE = "--inline" in sys.argv
C, Z = Cocoon(), Zenith()

def money(v): return "R$ " + f"{v:,.0f}".replace(",", ".")
def fmt(v, n=2):
    s = f"{v:,.{n}f}" if n else f"{int(round(v)):,}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")
def src(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): return None
    if not INLINE: return rel
    ext = rel.rsplit(".", 1)[-1].lower(); mime = {"svg": "image/svg+xml", "png": "image/png", "woff2": "font/woff2"}[ext]
    return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()
def fig(rel, cap):
    s = src(rel)
    return f'<figure><img src="{s}" alt="{cap}" loading="lazy"><figcaption>{cap}</figcaption></figure>' if s else f'<div class="missing">[{rel} não gerado]</div>'
def table(headers, rows, foot=None, cls=""):
    h = "".join(f"<th>{x}</th>" for x in headers)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    f = f"<tfoot><tr>{''.join(f'<td>{c}</td>' for c in foot)}</tr></tfoot>" if foot else ""
    return f'<div class="tw"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody>{f}</table></div>'
def kv(rows): return '<div class="tw"><table class="kv">' + "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows) + "</table></div>"
def two(a, b): return f'<div class="two"><div>{a}</div><div>{b}</div></div>'
def gantt(items, unit="sem"):
    end = max(s + d for _, s, d in items); out = ""
    for (t, s, d) in items:
        out += f'<div class="grow"><div class="glabel">{t}</div><div class="gtrack"><div class="gbar" style="left:{100 * s / end:.1f}%;width:{100 * d / end:.1f}%"></div></div><div class="gdays">{fmt(s, 1)} a {fmt(s + d, 1)} {unit}</div></div>'
    return f'<div class="gantt">{out}</div>'

SECTIONS = []
def section(vol, num, title, html):
    SECTIONS.append((f"v{vol}s{num}", vol, num, title, html))

# ----------------------------------------------------------------------------- textos comuns
DISCLAIMER = '<div class="warn"><strong>Pré-dimensionamento de engenharia.</strong> Todas as bitolas, espessuras, quantidades de fixadores e capacidades de fundação deste caderno são pré-dimensionamento para orçamento e desenvolvimento de produto. Devem ser calculadas e validadas por engenheiro estrutural habilitado (ART/RRT), com análise de membrana (form-finding) e sondagem do terreno, antes da fabricação.</div>'

def membrane_spec():
    return f"""
<h3>Requisitos técnicos da membrana</h3>
{table(["Requisito", "Especificação mínima", "Norma / ensaio", "Como se verifica"], [
 ["Impermeabilidade", "Coluna d'água > 3.000 mm; costuras por solda de alta frequência (RF) com 40 mm, sem costura a linha exposta", "DIN 53886 / EN 20811", "Teste de mangueira 15 min após a montagem; inspeção das soldas"],
 ["Proteção UV", "Laca PVDF (fluoretada) 100% em ambas as faces; bloqueio UV > 99%; retenção de cor > 90% em 10 anos", "ISO 4892 (envelhecimento acelerado)", "Certificado do fabricante da membrana"],
 ["Resistência mecânica", "Tração urdume/trama ≥ 4.200 / 4.000 N/5 cm; rasgo ≥ 600 / 550 N; 1.050 g/m² (tipo III)", "DIN 53354 / DIN 53363", "Laudo por lote"],
 ["Resistência ao vento", "Projeto para V0 = 45 m/s (NBR 6123); pré-tensão 2,5 kN/m; fator de segurança 5 sobre a ruptura em uso", "NBR 6123 + análise não linear de membrana", "Memória de cálculo do form-finding; tensiômetro na obra"],
 ["Resistência à chuva", "Inclinação mínima 12° em qualquer ponto (Cocoon: seção elíptica; Zenith: cumes a 5,80 e 4,60 m); sem bolsões", "Geometria", "Modelo 3D e teste de água"],
 ["Durabilidade", "Vida útil ≥ 15 anos (garantia) / 20 a 25 anos (esperada); estabilidade dimensional < 1%", "Garantia do fabricante", "Inspeção anual"],
 ["Fungos e algas", "Tratamento fungicida no revestimento e anti-wicking nos fios", "ISO 846", "Certificado"],
 ["Fogo", "Classe B1 (DIN 4102) / M2 (NF P92-507); autoextinguível", "DIN 4102", "Certificado"],
 ["Limpeza", "Superfície autolimpante (PVDF); lavagem com água e detergente neutro a cada 2 anos; nunca abrasivos ou solventes", "Manual do fabricante", "Plano de manutenção"],
 ["Manutenção", "Inspeção anual da pré-tensão (tensiômetro), dos esticadores, das soldas e dos arremates; kit de reparo RF em estoque", "Plano Zion", "Checklist anual"],
])}
<h3>Sistema de fixação e tensionamento</h3>
"""

COCOON_MEMBRANE_FIX = """
<ol>
 <li><strong>Onde começa.</strong> A membrana é confeccionada em 7 painéis de vão (um por vão entre arcos) mais a tampa frontal (entre A0 e o vidro) e a tampa da cauda. Cada painel tem cordão keder Ø8 soldado por RF nas duas bordas longitudinais e bolsa com tubo Ø20 na borda inferior.</li>
 <li><strong>Como é fixada.</strong> Sobre cada arco vai um perfil duplo keder de alumínio (E01) preso por presilhas inox a cada 300 mm. Os painéis vizinhos deslizam cada um em um canal do mesmo perfil: a junta fica selada pelo próprio perfil, sem parafuso atravessando a membrana.</li>
 <li><strong>Como é tensionada.</strong> Tensionamento em duas direções: no sentido dos arcos, a bolsa inferior é puxada para o trilho de base (A07/A08) pelo perfil de arremate E02, com grampos a cada 400 mm, em passes cruzados (esquerda-direita, frente-cauda) até a pré-tensão de 2,5 kN/m medida com tensiômetro; no sentido longitudinal, o keder é fechado com tampa de topo e o painel é esticado entre os arcos pelo próprio comprimento de corte (compensação de 1,5% no padrão).</li>
 <li><strong>Encontros.</strong> Fachada: a membrana fecha no anel A0 com perfil de clamp de alumínio e EPDM, por trás do anel de vidro E07. Janelas Olho: a membrana é recortada, reforçada com faixa dupla e presa por clamp no anel de reforço E06; o requadro de madeira E05 cobre o clamp por fora. Espinha de Luz: bolsa lateral clampada nos banzos da treliça, com pingadeira sobre os vidros. Cauda: tampa cônica presa no quadro B08 com esticadores.</li>
 <li><strong>Drenagem.</strong> A água escorre pela concha até a calha oculta do perfil E02 (80 x 60 mm) e sai por dois tubos de queda Ø75 nas extremidades (frente e cauda) até caixas de brita. A calha tem inclinação de 0,5% nos dois sentidos a partir do meio.</li>
 <li><strong>Arremates.</strong> Perfil de acabamento em alumínio bronze cobrindo o keder na frente; saias de EPDM nas passagens do respiro de cumeeira e do duto da condensadora; tampas de topo do keder com dreno.</li>
</ol>"""
ZENITH_MEMBRANE_FIX = """
<ol>
 <li><strong>Onde começa.</strong> Membrana em peça única (8 gomos radiais por cume soldados por RF, mais as faixas de beiral), com bolsa de cabo Ø32 nas quatro bordas e faixas de reforço duplas nos cantos e ao redor dos anéis.</li>
 <li><strong>Como é fixada.</strong> Nos cumes, a membrana é prensada entre o anel de aço (B03/B04) e o perfil de clamp de alumínio (E02) com EPDM e parafusos inox M10 a cada 150 mm. Nos cantos, a chapa de canto inox (D14) recebe o cabo de borda, a cinta de canto e o olhal do poste. Sobre o anel de beiral a membrana apenas passa, deslizando sobre o perfil arredondado E01.</li>
 <li><strong>Como é tensionada.</strong> Sequência: (1) içar pelos anéis e prender nos clamps; (2) passar o cabo de borda Ø12 nas bolsas; (3) fixar as 4 chapas de canto nos postes com os esticadores M20 frouxos; (4) tensionar os cantos em cruz (frente-esquerda com fundos-direita) em 4 passes; (5) tensionar os estais dos postes até o prumo de projeto (inclinação 8°); (6) conferir a flecha das bordas (0,30 a 0,35 m) e a pré-tensão (2,5 kN/m) com tensiômetro.</li>
 <li><strong>Encontros.</strong> Óculo: cúpula de vidro com esquadria própria (E04) sobre o anel, rufo de EPDM cobrindo o clamp. Chaminé do Respiro: tubo de alumínio com veneziana sobre o anel B04. Paredes: a membrana não toca as paredes; o beiral de 1,00 m protege as juntas dos painéis SIP e o vidro.</li>
 <li><strong>Drenagem.</strong> Dos cumes a água corre para as bordas em catenária e pinga nos pontos baixos (meio dos vãos entre postes) sobre canaletas de brita; nas laterais do corpo a calha oculta do perfil E01 recolhe o que escorre pelo anel de beiral e desce por dois pilares com tubo Ø75 interno.</li>
 <li><strong>Arremates.</strong> Cintas de canto com catraca cobertas por capa de membrana; capas de esticador; tampas dos postes; saias nos anéis.</li>
</ol>"""

def foundation_models(product):
    c = product == "cocoon"
    return f"""
<p>Três soluções de fundação para o mesmo quadro de deck (grelha de vigas U 150 x 60 sobre cabeçotes ajustáveis). A escolha é feita depois da sondagem SPT ou ensaio de torque no local; <strong>nenhum dimensionamento definitivo de fundação é apresentado sem dados geotécnicos.</strong></p>
{table(["", "Modelo A · Deck sobre fundações pontuais", "Modelo B · Sistema metálico para terreno inclinado", "Modelo C · Baixo impacto para áreas naturais"], [
 ["Descrição", "Sapatas ou tubulões curtos de concreto (Ø300 a 400 mm, 0,8 a 1,2 m) com chumbador e cabeçote ajustável; ou blocos pré-moldados sobre brita compactada", "Estacas helicoidais de comprimentos diferentes (1,5 a 3,0 m) seguindo o declive; pilaretes tubulares Ø101,6 travados em X com cabos onde a altura livre passa de 0,8 m; deck em balanço no lado baixo com guarda-corpo", "Estacas helicoidais Ø76 curtas (1,5 a 2,0 m) cravadas por motor hidráulico portátil, sem abertura de acesso para máquinas; todos os elementos removíveis; sem concreto"],
 ["Terreno", "Plano a 3%, solo firme (SPT > 8), acesso de betoneira", "5 a 30% de declive, solo firme a médio", "Qualquer, com SPT > 4; floresta, dunas fixadas, campos de altitude"],
 ["Solo", "Verificar capacidade (≥ 150 kPa) e nível d'água", "Verificar deslizamento superficial e drenagem a montante", "Verificar torque de cravação (correlação com capacidade)"],
 ["Vento (tração)", "Chumbadores e peso das sapatas resistem ao uplift de ≈ {'4 kN' if c else '5 a 12 kN'} por apoio", "Estacas de tração dedicadas nos pés dos {'arcos extremos' if c else 'postes'}", "Hélice a ≥ 1,5 m dá tração de 15 a 25 kN por estaca"],
 ["Chuvas e umidade", "Drenagem em brita ao redor das sapatas", "Canaleta de crista para desviar a água da encosta; brita sob o deck", "Solo intacto drena naturalmente; brita apenas nos pontos de queda"],
 ["Drenagem da unidade", "Caixas de brita nas quedas", "Descida canalizada pela encosta até dissipador", "Dispersão em vala de brita"],
 ["Carga da estrutura", f"≈ {fmt(cocoon_bom()['total'] / 46 if c else zenith_bom()['total'] / 37, 0)} kg por apoio (peso próprio) + sobrecarga 2 kN/m² + {'0' if c else '19 kN da hidromassagem'}", "Idem, com verificação de esforço horizontal nos pilaretes", "Idem"],
 ["Impacto", "Médio (concreto)", "Baixo a médio", "Mínimo; reversível"],
 ["Tempo", "3 dias + cura 7 dias", "2 dias", "1 a 1,5 dia"],
 ["Custo relativo", "1,0", "1,3 a 1,6", "0,9 a 1,1"],
])}
{fig("detalhes/DET-04_fundacao.svg", "DET-04 · Fundação e deck elevado (modelo C e variante inclinada)")}
"""

LAYERS = [
    ("01", "Fundação", "Transfere as cargas ao solo sem escavação: estacas helicoidais (ou sapatas pontuais) com cabeçotes ajustáveis que absorvem o desnível do terreno."),
    ("02", "Estrutura do deck", "Grelha de vigas U 150 x 60 galvanizadas: nivela a plataforma, engasta os arcos / pilares e leva as instalações no vazio de 200 mm."),
    ("03", "Piso e isolamento", "Módulos de vigotas com PIR 50 mm, manta inferior, compensado naval e piso de engenharia: barreira térmica e acústica contra o solo."),
    ("04", "Estrutura metálica principal", "Pórticos elípticos (Cocoon) / mastros, coroas, pilares e anel de beiral (Zenith): esqueleto que dá forma e resiste ao vento."),
    ("05", "Travamentos", "Terças, espinha e cabos em X (Cocoon) / postes, estais e cabo de borda (Zenith): impedem a ovalização e o tombamento e distribuem a tensão da membrana."),
    ("06", "Membrana externa", "PVDF 1050 g/m² tensionada: impermeabiliza, bloqueia UV, dá a forma final e enrijece a estrutura pela pré-tensão."),
    ("07", "Câmara de ventilação", "60 mm de ar em movimento entre a membrana e o isolamento: seca a condensação da face interna da membrana e retira o calor radiante no verão."),
    ("08", "Isolamento térmico", "Lã de PET 50 mm (25 kg/m³) apoiada em malha: R = 1,25 m²K/W; mantém o conforto na serra e no calor tropical."),
    ("09", "Barreira de condensação", "Manta refletiva de alumínio (bolha) do lado da câmara, com emendas fitadas: reflete o calor radiante e evita que o vapor interno molhe a lã em climas frios."),
    ("10", "Membrana / revestimento interno", "Forro tensionado acústico (Trevira CS) ou painéis de madeira: fecha o envelope, absorve som e dá o acabamento contínuo do interior."),
    ("11", "Instalações elétricas", "Quadro no ático técnico; cabos pelo vazio do piso e atrás do forro; fitas LED nos rodapés e requadros; tomadas nos móveis."),
    ("12", "Instalações hidráulicas", "PEX quente/frio pelo piso; esgoto Ø100 sob o deck com 2% de declividade; aquecedor no ático; fossa compacta."),
    ("13", "Acabamento interno", "Piso de carvalho, porcelanato no banho, marcenaria embutida, louças, metais, mobiliário e enxoval."),
]

def parts_table(P):
    rows = [[p["cod"], p["nome"], p["qtd"], fmt(p["comp"], 2), p["larg"] or "", p["alt"] or "", p["perfil"], p["aco"], fmt(p["esp"], 1), fmt(p["peso_un"], 1), fmt(p["peso_total"], 1), p["fab"], p["uniao"], p["ordem"]] for p in P]
    tot = sum(p["peso_total"] for p in P)
    return table(["Cód.", "Nome", "Qtd", "Comp. (m)", "Larg. (mm)", "Alt. (mm)", "Perfil", "Aço", "Esp. (mm)", "Peso un. (kg)", "Peso total (kg)", "Fabricação", "União", "Ordem"], rows,
                 foot=["", "Total", sum(p["qtd"] for p in P), "", "", "", "", "", "", "", fmt(tot, 0), "", "", ""], cls="small")

def conn_table(CX):
    return table(["Conexão", "Peça A", "Peça B", "Sistema de união", "Fixador (tipo e classe)", "Qtd", "Passo"], [list(c) for c in CX], cls="small")

def bom_table(product, scen=1):
    b = budget(product, scen); rows = []; cur = None; sub = 0; out = []
    for (g, desc, un, qtd, unit, tot) in b["rows"]:
        if g != cur:
            if cur is not None: out.append([f"<b>{cur}</b>", "", "", "", "", f"<b>{money(sub)}</b>"])
            cur = g; sub = 0
        sub += tot
        out.append([g, desc, un, fmt(qtd, 1) if isinstance(qtd, float) else qtd, money(unit), money(tot)])
    out.append([f"<b>{cur}</b>", "", "", "", "", f"<b>{money(sub)}</b>"])
    return table(["Grupo", "Descrição", "Un.", "Qtd", "Preço unit. (R$)", "Total (R$)"], out, foot=["", "Total de materiais e serviços de fábrica (cenário " + b["scen"] + ")", "", "", "", f"<b>{money(b['mat_total'])}</b>"], cls="small")

def budget_section(product):
    B = [budget(product, s) for s in range(3)]
    rows = [
        ["Materiais e insumos (18 grupos do BOM)"] + [money(b["mat_total"]) for b in B],
        ["Mão de obra de fabricação (serralheiro, soldador)"] + [money(b["fab_labor"]) for b in B],
        ["Mão de obra de instalação (montadores, líder, carpinteiro, eletricista, encanador, vidraceiro, membranas, marceneiro, acabamento, engenheiro)"] + [money(b["site_labor"]) for b in B],
        ["Transporte (carreta fábrica-sítio até 300 km + última milha)"] + [money(b["transporte"]) for b in B],
        ["Equipamentos (guincho, talha, andaime, cravação; munck no Zenith)"] + [money(b["equipamentos"]) for b in B],
        ["Hospedagem e alimentação da equipe (5 pessoas)"] + [money(b["hospedagem"]) for b in B],
        [f"Custos indiretos ({fmt(B[0]['indiretos_pct'] * 100, 0)}%: gestão, EPI, ferramental, seguros, ART)"] + [money(b["indiretos"]) for b in B],
        ["Contingência"] + [f"{money(b['conting'])} ({fmt(b['conting_pct'] * 100, 0)}%)" for b in B],
        ["Desenvolvimento (projeto executivo, cálculo, form-finding, gabaritos, protótipo) · custo único por produto, integral na 1ª unidade"] + [money(b["nre"]) for b in B],
    ]
    summary = table(["Item", "Econômico", "Zion Standard", "Zion Premium"], rows, cls="")
    totals = table(["Indicador", "Econômico", "Zion Standard", "Zion Premium"], [
        ["<b>Custo de produção</b> (kit de fábrica: estrutura, chapas, conexões, membrana, isolamento, forro, vidros, portas, marcenaria + mão de obra de fabricação)"] + [money(b["sub_prod"]) for b in B],
        ["<b>Custo de instalação</b> (fundação, deck, piso, banheiro, instalações, acabamentos + mão de obra de campo, transporte, equipamentos, hospedagem)"] + [money(b["sub_inst"]) for b in B],
        ["Indiretos + contingência"] + [money(b["indiretos"] + b["conting"]) for b in B],
        ["Desenvolvimento (1ª unidade)"] + [money(b["nre"]) for b in B],
        ["<b>CUSTO TOTAL · 1ª unidade</b>"] + [f"<b>{money(b['total'])}</b>" for b in B],
        ["Custo total sem o desenvolvimento (unidade seguinte, mesma escala)"] + [money(b["total"] - b["nre"]) for b in B],
        [f"<b>Custo por m²</b> (área total {fmt(B[0]['area_total'], 1)} m²)"] + [f"<b>{money(b['por_m2'])}/m²</b>" for b in B],
        [f"Custo por m² interno ({fmt(B[0]['area_int'], 1)} m²)"] + [f"{money(b['por_m2_int'])}/m²" for b in B],
    ])
    lab = budget(product, 1)
    labor = table(["Função", "Horas", "R$/h (Standard)", "Total (R$)", "Fase"], [[n, h, fmt(r, 2), money(t), f] for (n, h, r, t, f) in lab["lab_rows"]], foot=["Total de mão de obra", sum(x[1] for x in lab["lab_rows"]), "", money(lab["lab_total"]), ""])
    return summary, totals, labor

def scale_section(product):
    rows = []
    for n in (1, 5, 10, 50):
        b = budget(product, 1, n); sc = scale_factors(n)
        rows.append([f"{n} unidade{'s' if n > 1 else ''}", money(b["mat_total"]), money(b["fab_labor"] + b["site_labor"]), money(b["nre"]), money(b["total"]), money(b["por_m2"]), f"-{fmt(sc['material']['estrutura'] * 100, 0)}% aço · -{fmt(sc['fab_labor'] * 100, 0)}% fabricação · -{fmt(sc['material']['membrana'] * 100, 0)}% membrana · indiretos {fmt(sc['indiretos'] * 100, 0)}%"])
    t = table(["Lote", "Materiais / un.", "Mão de obra / un.", "Desenvolvimento / un.", "Custo total / un.", "R$/m²", "Fatores aplicados"], rows)
    b1 = budget(product, 1, 1)["total"]; bars = ""
    for n in (1, 5, 10, 50):
        v = budget(product, 1, n)["total"]
        bars += f'<div class="grow"><div class="glabel">{n} un.</div><div class="gtrack"><div class="gbar" style="left:0;width:{100 * v / b1:.1f}%"></div></div><div class="gdays">{money(v)}</div></div>'
    return t + f'<div class="gantt">{bars}</div>'

# ============================================================================= VOLUMES
def build_volume(vol, product):
    c = product == "cocoon"; G = C if c else Z
    name = "ZION COCOON" if c else "ZION ZENITH"
    bom_ = cocoon_bom() if c else zenith_bom()
    P = cocoon_parts() if c else zenith_parts(); CX = COCOON_CONNECTIONS if c else ZENITH_CONNECTIONS
    d = f"{product}/desenhos"; rd = f"{product}/renders"
    # 01 conceito
    if c:
        concept = f"""
<p class="lead">Cabana orgânica premium em forma de casulo: uma concha contínua de membrana tensionada sobre oito pórticos elípticos, que se abre para a paisagem por um lábio inclinado e uma fachada de vidro de piso a cumeeira. Nada de escotilhas redondas nem túnel segmentado: a Cocoon é uma semente, cheia na frente e afilada na cauda, com uma Espinha de Luz na cumeeira e seis Janelas Olho em lente.</p>
{kv([("Comprimento do piso", "9,60 m (concha com lábio: 9,75 m)"), ("Largura máxima", "6,00 m (piso 5,86 m)"), ("Altura máxima", "4,20 m"), ("Área interna", f"{fmt(G.floor_area(), 1)} m² + vestíbulo 2,4 m² = 48 m²"), ("Deck externo", "4,60 x 6,50 = 29,9 m²"), ("Área total", "78 m²"),
     ("Programa", "Lounge com chaise e minibar, suíte king, banho completo com banheira na cauda, opção de hot tub no deck"), ("Peso embarcado", f"{fmt(bom_['total'], 0)} kg · 1 contêiner 40' HC"), ("Estrutura", "Aço carbono galvanizado a fogo: 8 pórticos elípticos + terças + espinha + trilhos de base")])}
<h3>Inspiração e identidade proprietária</h3>
<ul><li><strong>Casulo e concha:</strong> seção elíptica com centro a 0,75 m do piso, que abraça o chão e sobe sem quinas.</li><li><strong>Biomorfismo:</strong> planta em superelipse assimétrica (frente n = 4, cauda n = 3): a forma de uma semente, reconhecível em planta e em silhueta.</li><li><strong>Lábio frontal:</strong> anel de fachada inclinado 8°, avançando 0,60 m sobre o deck: beiral, sombra e a expressão de abertura.</li><li><strong>Espinha de Luz:</strong> claraboia contínua de 0,70 x 4,70 m sobre a cama e o estar.</li><li><strong>Janelas Olho:</strong> lentes 1,60 x 0,95 m com requadros profundos de madeira laminada.</li></ul>
<p>As geometrias são definidas por parâmetros numéricos no arquivo <code>tools/geometry.py</code>; recomenda-se o registro de desenho industrial das duas formas e das marcas ZION COCOON e ZION ZENITH.</p>"""
    else:
        concept = f"""
<p class="lead">Cabana arquitetônica de dois cumes assimétricos deslocados em diagonal: 5,80 m no Zênite, sobre a cama, e 4,60 m no Respiro, sobre o café. A membrana desce dos cumes a um anel de beiral e continua em balanço sobre o terraço, com bordas em catenária entre postes inclinados. Sob ela, um corpo de vidro e madeira de 9,50 x 5,40 m.</p>
{kv([("Corpo", "9,50 x 5,40 x 2,75 m"), ("Altura máxima (definida pelo estudo estrutural)", "5,80 m no cume principal; 4,60 m no secundário; anel de beiral a 2,90 m"), ("Cobertura", "12,90 x 7,40 m (95,5 m² em projeção; 118 m² de membrana)"), ("Área interna", f"{fmt(G.floor_area(), 1)} m²"), ("Terraço + passarela", "20,4 + 7,6 = 28,0 m²"), ("Área total", "79,3 m²"),
     ("Programa", "Lounge, Ilha do Café, suíte king sob o Óculo do Zênite, closet, banho com bancada dupla e banheira, terraço com hidromassagem"), ("Peso embarcado", f"{fmt(bom_['total'], 0)} kg · 1 contêiner 40' HC"), ("Estrutura", "2 mastros com coroas de 3 braços, 10 pilares, anel de beiral 150 x 100, 7 postes estaiados, cabo de borda Ø12")])}
<h3>Por que a altura é 5,80 m</h3>
<p>A altura do cume principal foi definida pelo estudo estrutural e de conforto: com o anel de beiral a 2,90 m e o cume a 5,80 m, a membrana tem inclinação mínima de 14° em todo o vale entre os cumes (acima dos 12° de drenagem), a relação flecha/vão da catenária de borda fica em 1/20 e a compressão de projeto no mastro M1 resulta em 45 kN, dentro do limite de flambagem de um tubo Ø139,7 x 4,5 com 5,05 m de comprimento (pré-dimensionamento). Um cume mais baixo criaria bolsões de água entre os cumes; mais alto aumentaria o vento no mastro sem ganho de espaço útil.</p>
<h3>Identidade proprietária</h3>
<ul><li><strong>Dois cumes assimétricos em diagonal:</strong> silhueta que muda a cada ângulo, nunca simétrica.</li><li><strong>Óculo do Zênite:</strong> anel Ø1,20 sustentado por coroa de três braços, com cúpula de vidro sobre a cama.</li><li><strong>Respiro:</strong> o cume secundário é uma chaminé de ventilação natural.</li><li><strong>Mastros integrados:</strong> M1 dentro da parede da cabeceira, M2 no totem da Ilha do Café.</li></ul>"""
    section(vol, "01", "Conceito", concept)
    # 02 design
    section(vol, "02", "Design", two(fig(f"{rd}/{product}_ext_front.png", f"{name} · vista frontal 3/4"), fig(f"{rd}/{product}_ext_side.png", f"{name} · lateral")) +
            two(fig(f"{rd}/{product}_night.png", f"{name} · noite"), fig(f"{rd}/{product}_ext_aerial.png", f"{name} · aérea")) +
            two(fig(f"{rd}/{product}_int_living.png", f"{name} · interior: estar"), fig(f"{rd}/{product}_int_bed.png", f"{name} · interior: da cama para a fachada")) +
            two(fig(f"{rd}/{product}_int_bath.png", f"{name} · banho"), fig(f"{d}/08_isometrica.svg", f"{name} · isométrica")) +
            f'<p class="note">Modelo 3D interativo: <a href="{product}/3d/zion-{product}-3d.html">{product}/3d/zion-{product}-3d.html</a> · arquivo GLB: <a href="{product}/3d/zion-{product}.glb">zion-{product}.glb</a></p>')
    # 03 planta (master plan arquitetônico)
    section(vol, "03", "Master plan arquitetônico (plantas, fachadas, cortes)",
            fig(f"{d}/03_planta_tecnica.svg", "Planta baixa cotada") + fig(f"{d}/02_planta_humanizada.svg", "Planta de layout") + fig(f"{d}/03b_planta_estrutural.svg", "Planta estrutural") +
            two(fig(f"{d}/04_elevacao_frontal.svg", "Fachada frontal"), fig(f"{d}/04b_fachada_traseira.svg", "Fachada traseira")) +
            fig(f"{d}/05_elevacao_lateral.svg", "Fachadas laterais (a lateral esquerda é simétrica em silhueta; as janelas seguem a planta)") +
            two(fig(f"{d}/06_corte_longitudinal.svg", "Corte longitudinal"), fig(f"{d}/07_corte_transversal.svg", "Corte transversal")))
    # 04 estrutura
    steel_kg = sum(p["peso_total"] for p in P if "alumínio" not in p["aco"] and "madeira" not in p["aco"])
    est = f"""
{DISCLAIMER}
{two(fig(f"{d}/12_estrutura_isometrica.svg", "Estrutura metálica (isométrica)"), fig("detalhes/DET-10_arcos_cocoon.svg" if c else "detalhes/DET-11_mastros_zenith.svg", "Sistema de arcos" if c else "Sistema de mastros, coroas e anel"))}
<h3>Sistema estrutural</h3>
{"<p>Oito pórticos elípticos planos (A0 a A7) em tubo Ø88,9 x 3,6 (A0 em Ø101,6 x 4,0), cada um em 3 segmentos calandrados unidos por luvas internas, engastados por chapas de base na viga de borda do deck. Sete linhas de terças Ø48,3 rosqueadas em talões, a treliça da Espinha de Luz e cabos em X nos vãos extremos travam o conjunto. A membrana tensionada (2,5 kN/m) enrijece a concha contra ovalização. Uplift de projeto 1,3 kN/m² x 48 m² ≈ 62 kN em 16 pés (≈ 4 kN cada). A grelha do deck em U 150 x 60 x 3,0 sobre 46 estacas helicoidais fecha o caminho de carga.</p>" if c else
 "<p>Dois mastros a compressão (M1 Ø139,7 x 4,5 com 45 kN de projeto; M2 Ø114,3 x 4,0) com coroas de 3 braços e anéis de cume; dez pilares Ø101,6 embutidos nos painéis SIP sustentam o anel de beiral 150 x 100 x 4,0 (viga-anel comprimida pela membrana); sete postes Ø76,1 inclinados 8° e estaiados absorvem os cabos de borda. Os painéis SIP formam o diafragma. Uplift de projeto 1,3 kN/m² x 95 m² ≈ 125 kN entre pilares, postes e 37 estacas (30 de compressão + 7 de tração).</p>"}
{table(["Parâmetro", "Valor de pré-dimensionamento"], [["Vento", "V0 = 45 m/s, categoria II, S1 = S3 = 1,0 (NBR 6123); q ≈ 1,24 kN/m²"], ["Coeficientes de forma", "Cpe -1,2 a +0,8 (concha)" if c else "Cpe -1,4 a +0,6 (cobertura de cumes)"], ["Aço", "ASTM A500 Gr. B (fy 290 MPa) tubos; ZAR-230 perfis U; A36 chapas; galvanização NBR 6323"], ["Parafusos", "Classe 8.8 zincados; furos com folga 1 mm; torque M12 45 N·m, M16 120 N·m, M20 230 N·m"], ["Membrana", "PVDF 1050 g/m² tipo III; pré-tensão 2,5 kN/m; FS 5"], ["Peso do aço (lista de peças)", f"{fmt(steel_kg, 0)} kg (inclui grelha e estacas)"]])}
<h3>Lista completa de peças (ferro por ferro)</h3>
<p class="note">Códigos: A base e grelha · B arcos / mastros · C travamentos · D chapas e conexões · E suporte da membrana e acabamento · F fundação. A coluna Ordem indica o passo do manual de montagem em que a peça entra.</p>
{parts_table(P)}
"""
    section(vol, "04", "Engenharia da estrutura metálica", est)
    # 05 explodido
    section(vol, "05", "Vista explodida", fig(f"{d}/10_modelo_explodido.svg", "Modelo explodido da estrutura: base, estrutura, arcos / mastros, travamentos, cobertura, isolamento, membrana interna, portas e janelas, acabamentos") + fig(f"{d}/13_camadas_construtivas.svg", "Camadas construtivas 01 a 13 (explodida)"))
    # 06 encaixe
    enc = f"""
<p>A estrutura chega pronta: todas as soldas são de fábrica (luvas, talões, chapas de base, olhais, berços) e no terreno só existem encaixes macho-fêmea, parafusos classe 8.8, porcas, arruelas e pinos de segurança. Nenhum corte e nenhuma solda em campo. Cada peça leva o código gravado a laser e cada conexão tem o torque especificado.</p>
{fig("detalhes/DET-03_ancoragem.svg", "DET-03 · Ancoragens: pé de arco, base de poste, chapa de canto")}
<h3>Tabela de conexões</h3>
{conn_table(CX)}
<h3>Princípios do kit</h3>
<ul>
 <li><strong>Encaixe macho-fêmea com batente:</strong> as luvas internas D02 têm um anel de batente soldado a 100 mm, de modo que a perna só entra até a posição certa; os 4 furos coincidem automaticamente.</li>
 <li><strong>Furos oblongos nas chapas de base:</strong> 18 x 25 mm permitem ajustar ± 6 mm a posição do arco / pilar sem forçar.</li>
 <li><strong>Pinos de segurança:</strong> em todas as luvas e bases articuladas, pino Ø6 (ou Ø20/Ø30 nos mastros) com contrapino: a peça não se solta mesmo com parafuso frouxo.</li>
 <li><strong>Parafusos por classe:</strong> M12 8.8 nas grelhas e luvas (45 N·m); M16 8.8 nas chapas de base e no anel de beiral (120 N·m); M20 nas bases dos mastros (230 N·m); inox A2 em tudo o que toca a membrana ou fica aparente.</li>
 <li><strong>Sem ferramenta especial:</strong> chaves 19 / 24 / 30 mm, torquímetro, puxador de keder e tensiômetro. Tudo vai na caixa de ferramentas do kit.</li>
</ul>
"""
    section(vol, "06", "Sistema de encaixe", enc)
    # 07 camadas
    section(vol, "07", "Camadas construtivas", table(["Camada", "Nome", "Função"], [[f"<b>{n}</b>", t, f] for n, t, f in LAYERS]) + fig("detalhes/DET-01_cobertura_cocoon.svg" if c else "detalhes/DET-02_cobertura_zenith.svg", "Seção do envelope: camadas 06 a 10"))
    # 08 memorial descritivo
    mem = f"""
<h3>Estrutura e envelope</h3>
{kv([("Fundação", "Estacas helicoidais Ø76 x 3,6 com hélice Ø300, L 1,5 a 2,5 m, galvanizadas; cabeçotes ajustáveis; 3 modelos alternativos (ver abaixo)"), ("Deck e piso", "Grelha U 150 x 60 x 3,0 galvanizada Z275; vigotas 50 x 150 autoclavadas a cada 400 mm; PIR 50 mm; compensado naval 18 mm; carvalho de engenharia 14 mm; porcelanato no banho; deck cumaru 20 x 140"), ("Estrutura primária", "Tubos ASTM A500 galvanizados a fogo + pintura a pó bronze nas peças aparentes; ligações parafusadas cl. 8.8"), ("Membrana", "PVDF 1050 g/m² tipo III, garantia 15 anos, classe B1, autolimpante"), ("Isolamento", "Câmara ventilada 60 mm + lã de PET 50 mm + manta refletiva; U ≈ 0,6 W/m²K"), ("Forro", "Tecido tensionado acústico Trevira CS cor areia; painéis de madeira nas zonas de destaque"), ("Vidros", "Insulado 6 lam + 12 Ar + 6 temp low-e (U 1,6; FS 0,40) em esquadrias de alumínio com ruptura térmica, bronze"), ("Portas", "Cocoon: pivotante de vidro 1,00 x 2,40; Zenith: 2 folhas de correr 1,35 x 2,75 + porta de correr do banho" ), ("Climatização", "Dutado inverter quente/frio no ático (12k Cocoon / 18k Zenith); difusores lineares; condensadora oculta; opção de piso radiante"), ("Ventilação", "Respiro de cumeeira e janelas basculantes (Cocoon) / chaminé do Respiro motorizada (Zenith); exaustor com recuperador"), ("Elétrica", "220 V, quadro no ático (12 / 16 módulos), DR, tomadas USB, LED 2700 K indireto; opção solar 3 kWp"), ("Hidráulica", "PEX Ø25/20; aquecedor a gás 23 / 30 L/min ou bomba de calor; esgoto Ø100 a fossa + filtro compactos; reúso de águas cinzas opcional")])}
{membrane_spec()}{COCOON_MEMBRANE_FIX if c else ZENITH_MEMBRANE_FIX}
{two(fig("detalhes/DET-06_drenagem.svg", "DET-06 · Drenagem"), fig("detalhes/DET-05_esquadrias.svg", "DET-05 · Portas e janelas"))}
<h3>Fundação e ancoragem: três modelos</h3>
{foundation_models(product)}
<h3>Instalações</h3>
{two(fig("detalhes/DET-07_eletrica.svg", "DET-07 · Elétrica"), fig("detalhes/DET-08_hidraulica.svg", "DET-08 · Hidráulica"))}
{fig("detalhes/DET-09_climatizacao.svg", "DET-09 · Climatização e ventilação")}
"""
    section(vol, "08", "Memorial descritivo", mem)
    # 09 BOM
    section(vol, "09", "Bill of Materials (com preços de referência SC, cenário Zion Standard)", '<p class="note">Preços de referência em Santa Catarina, setembro de 2026, sem impostos de revenda (ver premissas na seção 11). Os cenários Econômico e Premium aplicam os fatores da tabela de preços; a planilha XLSX traz as três colunas.</p>' + bom_table(product, 1))
    # 10 manual
    M = manual(product)
    man = "".join(f"""<div class="step"><div class="stephead"><span class="stepnum">PASSO {s['n']:02d}</span><h4>{s['titulo']}</h4></div>
<div class="stepgrid"><div><b>Equipe</b><br>{s['equipe']}</div><div><b>Ferramentas</b><br>{s['ferramentas']}</div><div><b>Equipamentos</b><br>{s['equipamentos'] or 'Nenhum'}</div><div><b>Tempo</b><br>{s['tempo']}</div></div>
<p><b>Riscos:</b> {s['riscos']}</p><p><b>Checklist:</b></p><ul>{''.join(f'<li>☐ {x}</li>' for x in s['checklist'])}</ul></div>""" for s in M)
    section(vol, "10", "Manual de montagem (17 passos)", '<p>Sequência para uma equipe de 4 montadores e 1 líder, sem grua (guincho manual de 1 t e talha), com o kit completo no sítio. Antes do embarque a estrutura é pré-montada na fábrica e a membrana ajustada sobre ela (fit test).</p>' + man)
    # 11 orçamento
    summary, totals, labor = budget_section(product)
    orc = f"""
<p class="lead">Orçamento de referência para fabricação e instalação em Santa Catarina (fábrica na região de Joinville / Itajaí / Florianópolis; sítio até 300 km). Três cenários: Econômico (membrana PVC acrílica, vidro laminado simples, esquadria sem ruptura térmica, louças nacionais, laminado), Zion Standard (especificação deste caderno) e Zion Premium (membrana importada, sistemas de esquadria europeus, bomba de calor, louças premium, automação).</p>
{totals}
<h3>Composição por cenário</h3>
{summary}
<h3>Mão de obra por função (cenário Standard)</h3>
{labor}
<h3>Premissas de preços (pesquisa de referência, set/2026)</h3>
{table(["Insumo", "Un.", "Standard (R$)", "Econômico", "Premium", "Observação"], [[v[0], v[1], fmt(v[2], 2), fmt(v[2] * v[3], 2) if v[3] else "n.a.", fmt(v[2] * v[4], 2) if v[4] else "n.a.", v[5]] for v in PRICES.values()], cls="small")}
{table(["Função", "R$/h Standard", "Econômico", "Premium"], [[v[0], fmt(v[1], 2), fmt(v[1] * v[2], 2), fmt(v[1] * v[3], 2)] for v in LABOR_RATES.values()], cls="small")}
<p class="note">Fontes e método: pisos salariais 2026 (montador de estruturas metálicas em SC ≈ R$ 2.850/mês; serralheiro ≈ R$ 2.670 a 3.400/mês) convertidos em custo-hora com encargos (≈ 1,8x), EPI e ferramental; membranas PVC/PVDF instaladas anunciadas de R$ 95 a 145/m² para lonas simples, ajustadas para PVDF tipo III com confecção de forma dupla-curva; aço tubular e perfis pelos distribuidores de SC (lotes acima de 1 t); estacas helicoidais por fornecedores nacionais; demais itens por cotações de mercado em SC. Todos os valores devem ser confirmados por cotação formal de pelo menos 3 fornecedores antes do orçamento executivo. Não inclui: terreno, acessos, redes externas, paisagismo, licenças, impostos sobre a venda e margem da Zion.</p>
"""
    section(vol, "11", "Orçamento Santa Catarina (3 cenários)", orc)
    # 12 cronograma
    fab = FAB_SCHEDULE[product]
    asm = [(t, sum(x[2] for x in ASSEMBLY[product][:i]), dd) for i, (t, _, dd, _) in enumerate(ASSEMBLY[product])]
    section(vol, "12", "Cronograma", "<h3>Fabricação (semanas, a partir da aprovação do executivo)</h3>" + gantt(fab, "sem") + "<h3>Instalação no sítio (dias úteis)</h3>" + gantt(asm, "d"))
    # 13 fabricação
    fabend = max(s + dd for _, s, dd in fab)
    section(vol, "13", "Estimativa de tempo de fabricação", table(["Etapa", "Duração", "Recursos"], [
        ["Projeto executivo, cálculo estrutural e form-finding", "3 semanas", "Engenheiro estrutural + projetista + confeccionador da membrana"],
        ["Compra de aço e insumos", "2 semanas (prazo de entrega)", "Distribuidores SC"],
        ["Gabaritos (calandra e bancada)", "2 semanas (uma vez; reaproveitados em série)", "Serralheria"],
        ["Fabricação da estrutura (corte, calandra, solda, furação)", f"{'5' if c else '5'} semanas para a 1ª unidade; 2,5 a 3 semanas em série", f"2 serralheiros + 1 soldador ({labor_hours(product)['serralheiro'] + labor_hours(product)['soldador']} h)"],
        ["Pré-montagem em fábrica e fit test da membrana", "1 semana", "Equipe de montagem"],
        ["Galvanização a fogo e pintura a pó", "1,5 semana (terceiros)", "Galvanizadora em SC"],
        ["Confecção da membrana", "4 a 5 semanas em paralelo", "Confeccionador especializado"],
        ["Esquadrias, vidros" + (", cúpula" if not c else ", Janelas Olho"), "5 a 6 semanas em paralelo", "Vidraçaria e serralheria de alumínio"],
        ["Marcenaria, módulos de piso e deck", "4 semanas em paralelo", "Marcenaria + carpintaria"],
        [f"<b>Total até a expedição</b>", f"<b>{fmt(fabend, 0)} semanas (1ª unidade) · 5 a 6 semanas por unidade em série</b>", ""],
    ]))
    # 14 montagem
    days = sum(x[2] for x in ASSEMBLY[product])
    section(vol, "14", "Estimativa de tempo de montagem", table(["Fase", "Atividades", "Dias", "Equipe"], [[t, dsc, fmt(dd, 1), tm] for (t, dsc, dd, tm) in ASSEMBLY[product]], foot=["Total", "", f"<b>{fmt(days, 0)} dias úteis</b>", "4 montadores + líder + especialistas pontuais"]) +
            f"<p>Transporte: 1 a 5 dias (nacional). Do embarque à entrega ao operador: {'3' if c else '3,5'} semanas. Desmontagem e realocação: {'4' if c else '5'} dias. Em parque de 10 unidades com 2 equipes: ≈ {'9' if c else '11'} semanas de instalação.</p>")
    # 15 recomendações + escala
    rec = f"""
<h3>Escala industrial: 1, 5, 10 e 50 unidades (cenário Standard)</h3>
{scale_section(product)}
<p>De onde vem a redução: compra de aço em lotes de 5 a 30 t (-5 a -13%); gabaritos e calandra por programa CNC amortizados (-14 a -34% na fabricação); membrana em séries de padrão repetido (-6 a -18%); esquadrias e vidros por lote (-5 a -14%); equipe de montagem com curva de aprendizado (-8 a -20%); equipamentos e mobilização diluídos; indiretos de 12% para 8%; e o desenvolvimento (R$ 240 mil por produto) diluído por unidade. A partir de 10 unidades vale a pena uma linha dedicada com bancadas fixas de pré-montagem e estoque de componentes comuns aos dois produtos (grelha, estacas, cabeçotes, terças, perfis, quadros de instalação).</p>
<h3>Recomendações de engenharia</h3>
<ol>
 <li><strong>Cálculo estrutural com ART</strong> pela NBR 8800 (aço) e NBR 6123 (vento), com análise não linear da membrana (form-finding e carregamentos de vento e chuva) feita junto com o confeccionador da membrana.</li>
 <li><strong>Sondagem</strong> (SPT ou ensaio de torque de cravação) em cada sítio antes de definir comprimento e quantidade das estacas; teste de carga em 2 estacas por sítio.</li>
 <li><strong>Protótipo em escala real</strong> no Zion Bubble Glamping (Florianópolis) antes da série: validar o tensionamento, a estanqueidade das Janelas Olho e da Espinha de Luz (Cocoon) e do Óculo (Zenith), o conforto térmico de verão e inverno e o tempo real de montagem.</li>
 <li><strong>Ensaios</strong>: teste de água nos encontros, termografia do envelope, medição de pré-tensão, ruído do ar-condicionado dutado (meta < 30 dB(A) na cama).</li>
 <li><strong>Galvanização a fogo obrigatória</strong> em todo aço estrutural (litoral); inox A2/A4 nos cabos, esticadores e presilhas; pintura a pó apenas estética.</li>
 <li><strong>Segurança contra incêndio</strong>: membrana e forro classe B1/M1; detector de fumaça; extintor; rota de fuga pela fachada e pela porta do banho (Zenith: janela da banheira como saída alternativa).</li>
 <li><strong>Acessibilidade</strong>: versão acessível com rampa no deck e banho adaptado (NBR 9050) prevista como variante do kit.</li>
 <li><strong>Manutenção</strong>: inspeção anual (pré-tensão, esticadores, selantes, drenos), lavagem bienal da membrana, troca da membrana prevista em 15 a 20 anos com a estrutura em uso.</li>
 <li><strong>Propriedade intelectual</strong>: registro de desenho industrial (INPI) das duas geometrias e das marcas; contratos de fabricação com cláusula de exclusividade dos gabaritos.</li>
</ol>
"""
    section(vol, "15", "Recomendações de engenharia e escala industrial", rec)

build_volume(1, "cocoon")
build_volume(2, "zenith")

# ----------------------------------------------------------------------------- HTML
fonts = ""
for f, fam, style in (("assets/aventa.woff2", "Aventa", "normal"), ("assets/cormorant.woff2", "Cormorant Garamond", "normal"), ("assets/cormorant-italic.woff2", "Cormorant Garamond", "italic")):
    s = src(f)
    if s: fonts += f"@font-face{{font-family:'{fam}';src:url({s}) format('woff2');font-weight:100 900;font-style:{style};font-display:swap;}}\n"
CSS = fonts + """
:root{--black:#040605;--green:#1B2117;--cream:#FEF5F0;--sand:#DED6BF;--earth:#8B714E;--paper:#FBF4EC}
*{box-sizing:border-box;margin:0;padding:0} html{scroll-behavior:smooth}
body{font-family:'Aventa','DM Sans',Helvetica,Arial,sans-serif;background:var(--cream);color:var(--green);line-height:1.7;font-size:14.5px}
a{color:var(--earth)} .wrap{display:flex;min-height:100vh}
nav{width:280px;flex:0 0 280px;background:var(--black);color:var(--cream);padding:30px 20px;position:sticky;top:0;height:100vh;overflow:auto}
nav .z{font-weight:800;letter-spacing:.4em;font-size:22px} nav .sub{display:block;font-size:9px;letter-spacing:.3em;color:var(--sand);margin:4px 0 22px}
nav .vol{font-size:10px;letter-spacing:.3em;color:var(--earth);margin:18px 0 6px;text-transform:uppercase}
nav a{display:block;color:var(--sand);text-decoration:none;font-size:11.5px;padding:4px 0;border-bottom:1px solid rgba(254,245,240,.08)} nav a b{color:var(--cream);margin-right:8px}
main{flex:1;min-width:0;padding-bottom:120px}
section{padding:64px 5vw 36px;border-bottom:1px solid var(--sand)}
section .num{font-size:10.5px;letter-spacing:.34em;text-transform:uppercase;color:var(--earth);display:block;margin-bottom:10px}
section h2{font-family:'Cormorant Garamond',Georgia,serif;font-weight:300;font-size:clamp(28px,3vw,42px);line-height:1.2;margin-bottom:22px}
section h3{font-size:12.5px;letter-spacing:.28em;text-transform:uppercase;margin:34px 0 12px} section h4{font-size:12px;letter-spacing:.16em;text-transform:uppercase;margin:16px 0 8px;color:var(--earth)}
p{margin-bottom:12px;max-width:1100px} p.lead{font-family:'Cormorant Garamond',Georgia,serif;font-size:21px;line-height:1.5;max-width:1000px} p.note{font-size:12.5px;color:#4c5446;max-width:none}
ul,ol{margin:0 0 14px 22px;max-width:1050px} li{margin-bottom:5px}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;background:#f1e8de;padding:1px 5px;border-radius:3px}
figure{margin:16px 0 22px} figure img{width:100%;height:auto;display:block;border:1px solid var(--sand);background:#fff} figcaption{font-size:11px;letter-spacing:.06em;color:var(--earth);margin-top:7px;text-transform:uppercase}
.two{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start}
.tw{overflow-x:auto;margin:8px 0 20px} table{border-collapse:collapse;width:100%;font-size:12.5px} table.small{font-size:11px}
th,td{border-bottom:1px solid var(--sand);padding:6px 8px;text-align:left;vertical-align:top} th{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--earth);font-weight:600;background:var(--paper)}
tfoot td{font-weight:700;background:var(--paper)} table.kv th{width:32%}
.missing{border:1px dashed var(--earth);padding:16px;color:var(--earth);font-size:12px;margin:12px 0}
.warn{background:#F4E9D6;border-left:4px solid var(--earth);padding:14px 18px;margin:14px 0 22px;font-size:13px;max-width:1100px}
.cover{background:var(--black);color:var(--cream);margin:-64px -5vw -36px;padding:100px 8vw 80px;min-height:90vh;display:flex;flex-direction:column;justify-content:center}
.cover .z{font-weight:800;letter-spacing:.45em;font-size:30px} .cover .sub{display:block;font-size:10px;letter-spacing:.35em;color:var(--sand);margin:6px 0 56px}
.splitword{display:flex;align-items:center;gap:26px;font-weight:200;letter-spacing:.5em;font-size:clamp(18px,2.8vw,38px);color:var(--sand);margin-bottom:30px} .splitword .line{flex:1;height:1px;background:var(--cream);opacity:.35}
.cover h1{font-family:'Cormorant Garamond',Georgia,serif;font-weight:300;font-size:clamp(34px,4.6vw,64px);line-height:1.12;max-width:1100px;margin-bottom:30px}
.cover .lead{color:var(--cream);opacity:.9;max-width:900px} .cover .meta{display:flex;justify-content:space-between;font-size:10px;letter-spacing:.3em;color:var(--sand);margin-top:60px}
.volhead{background:var(--green);color:var(--cream);margin:-64px -5vw 30px;padding:60px 5vw 40px} .volhead h2{color:var(--cream)} .volhead .num{color:var(--sand)}
.gantt{margin:8px 0 18px} .grow{display:grid;grid-template-columns:300px 1fr 130px;gap:10px;align-items:center;font-size:12px;margin-bottom:5px}
.gtrack{position:relative;height:15px;background:var(--paper);border:1px solid var(--sand)} .gbar{position:absolute;top:2px;bottom:2px;background:var(--earth)} .gdays{text-align:right;color:var(--earth)}
.step{border:1px solid var(--sand);background:#fff;padding:16px 20px;margin:12px 0;max-width:1150px} .stephead{display:flex;align-items:baseline;gap:16px} .stepnum{font-size:10px;letter-spacing:.3em;color:var(--earth)} .step h4{margin:0;color:var(--green);font-size:14px;letter-spacing:.08em}
.stepgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;font-size:12px;margin:10px 0}
.team{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:10px 0 20px} .team div{background:var(--paper);border:1px solid var(--sand);padding:10px 12px;font-size:12px}
@media(max-width:1100px){.two,.stepgrid,.team{grid-template-columns:1fr} nav{display:none}}
@media print{@page{size:A4 landscape;margin:10mm} body{font-size:10.5px;background:#fff} nav{display:none} main{padding:0}
 section{page-break-before:always;padding:6mm 0 4mm;border:0} section:first-of-type{page-break-before:avoid} .cover,.volhead{margin:0;min-height:auto;padding:26mm 14mm;-webkit-print-color-adjust:exact;print-color-adjust:exact}
 figure{page-break-inside:avoid} tr,.step{page-break-inside:avoid} figure img{max-height:158mm;width:auto;max-width:100%;margin:0 auto} .two{gap:12px} table.small{font-size:8.5px}
 .warn,th,tfoot td,.gtrack,.gbar,.team div{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
"""

cover = """
<section id="cover"><div class="cover">
 <div class="z">ZION</div><span class="sub">GLAMPING COLLECTION · ARCHITECTURAL PRODUCT BOOK</span>
 <div class="splitword"><span>COCOON</span><span class="line"></span><span>ZENITH</span></div>
 <h1>Sistema construtivo industrializado, modular e desmontável para duas cabanas exclusivas da Zion</h1>
 <p class="lead">Master plan de produto: conceito, plantas, engenharia da estrutura metálica peça a peça, sistema de encaixe, camadas construtivas, memorial, Bill of Materials, manual de montagem, orçamento em Santa Catarina, cronograma e análise de escala industrial. Primeiro a ZION COCOON, depois a ZION ZENITH.</p>
 <div class="meta"><span>VOLUME 1 · COCOON · VOLUME 2 · ZENITH</span><span>ZION HOTEL GROUP INTERNATIONAL · SET 2026</span></div>
</div></section>
<section id="intro"><span class="num">Como ler este caderno</span><h2>Um móvel premium de grande escala</h2>
<p class="lead">Cada cabana é tratada como um produto industrial: um kit de peças codificadas, fabricadas em serralheria ou indústria, galvanizadas, pré-montadas em fábrica e embaladas em um contêiner. No terreno não há corte nem solda: só encaixes, parafusos e torque. O mesmo sistema (ZION SHELL SYSTEM) serve às duas cabanas, com componentes comuns de fundação, deck, membrana, isolamento, forro, vidros e instalações.</p>
<div class="team">
 <div><b>Arquitetura modular</b><br>conceito, plantas, layout, fachadas, cortes</div><div><b>Engenharia estrutural</b><br>pré-dimensionamento de arcos, mastros, anel, cabos, fundações</div><div><b>Engenharia mecânica / fabricação</b><br>processos, gabaritos, tolerâncias, luvas e encaixes</div><div><b>Projeto de estruturas metálicas</b><br>lista de peças, chapas, conexões, parafusos</div>
 <div><b>Membranas tensionadas</b><br>especificação, confecção, form-finding, tensionamento</div><div><b>Glamping e hospitality</b><br>programa, conforto, operação, experiência</div><div><b>Industrialização e montagem</b><br>kit, embalagem, manual, cronograma</div><div><b>Orçamentação SC</b><br>preços de referência, mão de obra, cenários, escala</div>
</div>
<p class="note">Todas as bitolas, espessuras e capacidades são pré-dimensionamento e devem ser validadas por engenheiro estrutural habilitado antes da fabricação. Os preços são de referência (set/2026) e devem ser confirmados por cotação.</p>
</section>
"""
nav = ""
body = cover
for vol in (1, 2):
    pname = "ZION COCOON" if vol == 1 else "ZION ZENITH"
    nav += f'<div class="vol">Volume {vol} · {pname}</div>'
    first = True
    for sid, v, num, title, html in SECTIONS:
        if v != vol: continue
        nav += f'<a href="#{sid}"><b>{num}</b>{title}</a>'
        head = f'<div class="volhead"><span class="num">Volume {vol}</span><h2>{pname}</h2></div>' if first else ""
        first = False
        body += f'<section id="{sid}">{head}<span class="num">{pname} · {num}</span><h2>{title}</h2>{html}</section>'

HTML = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Zion Architectural Product Book · Cocoon e Zenith</title><style>{CSS}</style></head>
<body><div class="wrap"><nav><div class="z">ZION</div><span class="sub">ARCHITECTURAL PRODUCT BOOK</span><a href="#cover"><b>00</b>Capa</a><a href="#intro"><b>00</b>Como ler</a>{nav}</nav><main>{body}</main></div></body></html>"""
out = os.path.join(ROOT, "ZION_ARCHITECTURAL_PRODUCT_BOOK" + ("_standalone" if INLINE else "") + ".html")
open(out, "w", encoding="utf-8").write(HTML)
print("product book ->", out, f"{os.path.getsize(out) / 1e6:.2f} MB")

# ----------------------------------------------------------------------------- XLSX
if not INLINE:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter
    wb = Workbook(); wb.remove(wb.active)
    HEAD = PatternFill("solid", fgColor="1B2117"); HF = Font(bold=True, color="FEF5F0"); BOLD = Font(bold=True)
    def sheet(name, headers, rows, widths=None):
        ws = wb.create_sheet(name[:31]); ws.append(headers)
        for c in ws[1]: c.fill = HEAD; c.font = HF; c.alignment = Alignment(wrap_text=True, vertical="top")
        for r in rows: ws.append(list(r))
        for i, w in enumerate(widths or [18] * len(headers), start=1): ws.column_dimensions[get_column_letter(i)].width = w
        ws.freeze_panes = "A2"; return ws
    for product, P, CX in (("cocoon", cocoon_parts(), COCOON_CONNECTIONS), ("zenith", zenith_parts(), ZENITH_CONNECTIONS)):
        tag = "Cocoon" if product == "cocoon" else "Zenith"
        sheet(f"{tag} Peças", ["Código", "Nome", "Qtd", "Comp (m)", "Larg (mm)", "Alt (mm)", "Perfil", "Aço", "Esp (mm)", "Peso un (kg)", "Peso total (kg)", "Fabricação", "União", "Ordem", "Função"],
              [[p["cod"], p["nome"], p["qtd"], p["comp"], p["larg"], p["alt"], p["perfil"], p["aco"], p["esp"], p["peso_un"], p["peso_total"], p["fab"], p["uniao"], p["ordem"], p["funcao"]] for p in P],
              [9, 46, 6, 9, 9, 9, 34, 22, 8, 10, 11, 40, 46, 7, 40])
        sheet(f"{tag} Conexões", ["Conexão", "Peça A", "Peça B", "Sistema de união", "Fixador", "Qtd", "Passo"], [list(c) for c in CX], [9, 30, 30, 50, 50, 7, 7])
        B = [budget(product, s) for s in range(3)]
        rows = []
        for i, (g, desc, un, qtd, unit, tot) in enumerate(B[1]["rows"]):
            rows.append([g, desc, un, qtd, B[0]["rows"][i][4], B[0]["rows"][i][5], unit, tot, B[2]["rows"][i][4], B[2]["rows"][i][5]])
        ws = sheet(f"{tag} BOM", ["Grupo", "Descrição", "Un.", "Qtd", "Unit. Econômico", "Total Econômico", "Unit. Standard", "Total Standard", "Unit. Premium", "Total Premium"], rows, [22, 60, 6, 8, 14, 14, 14, 14, 14, 14])
        ws.append(["TOTAL MATERIAIS", "", "", "", "", B[0]["mat_total"], "", B[1]["mat_total"], "", B[2]["mat_total"]])
        for c in ws[ws.max_row]: c.font = BOLD
        ws = sheet(f"{tag} Mão de obra", ["Função", "Horas", "R$/h Econ.", "Total Econ.", "R$/h Standard", "Total Standard", "R$/h Premium", "Total Premium", "Fase"],
                   [[B[1]["lab_rows"][i][0], B[1]["lab_rows"][i][1], B[0]["lab_rows"][i][2], B[0]["lab_rows"][i][3], B[1]["lab_rows"][i][2], B[1]["lab_rows"][i][3], B[2]["lab_rows"][i][2], B[2]["lab_rows"][i][3], B[1]["lab_rows"][i][4]] for i in range(len(B[1]["lab_rows"]))], [48, 8, 12, 14, 12, 14, 12, 14, 12])
        res = [["Materiais e insumos"] + [b["mat_total"] for b in B], ["Mão de obra de fabricação"] + [b["fab_labor"] for b in B], ["Mão de obra de instalação"] + [b["site_labor"] for b in B],
               ["Transporte"] + [b["transporte"] for b in B], ["Equipamentos"] + [b["equipamentos"] for b in B], ["Hospedagem da equipe"] + [b["hospedagem"] for b in B],
               ["Custo de produção (kit)"] + [b["sub_prod"] for b in B], ["Custo de instalação"] + [b["sub_inst"] for b in B], ["Indiretos"] + [b["indiretos"] for b in B], ["Contingência"] + [b["conting"] for b in B],
               ["Desenvolvimento (1ª unidade)"] + [b["nre"] for b in B], ["CUSTO TOTAL 1ª unidade"] + [b["total"] for b in B], ["Custo total sem desenvolvimento"] + [b["total"] - b["nre"] for b in B],
               ["Custo por m² (área total)"] + [b["por_m2"] for b in B], ["Custo por m² interno"] + [b["por_m2_int"] for b in B]]
        sheet(f"{tag} Orçamento", ["Item", "Econômico", "Zion Standard", "Zion Premium"], res, [44, 18, 18, 18])
        sheet(f"{tag} Escala", ["Lote", "Materiais/un", "Mão de obra/un", "Transporte+equip/un", "Indiretos+conting/un", "Desenvolvimento/un", "Total/un", "R$/m²"],
              [[n] + [(lambda b: [b["mat_total"], b["fab_labor"] + b["site_labor"], b["transporte"] + b["equipamentos"] + b["hospedagem"], b["indiretos"] + b["conting"], b["nre"], b["total"], b["por_m2"]])(budget(product, 1, n)) for _ in [0]][0] for n in (1, 5, 10, 50)], [10, 16, 16, 20, 20, 18, 16, 12])
    sheet("Premissas de preço", ["Chave", "Insumo", "Un.", "Standard", "Fator Econômico", "Fator Premium", "Observação"], [[k] + list(v[:6]) for k, v in PRICES.items()], [14, 70, 6, 12, 12, 12, 50])
    sheet("Taxas de mão de obra", ["Função", "R$/h Standard", "Fator Econômico", "Fator Premium"], [list(v) for v in LABOR_RATES.values()], [50, 14, 14, 14])
    xout = os.path.join(ROOT, "ZION_ORCAMENTO_SC_Cocoon_Zenith.xlsx"); wb.save(xout); print("xlsx ->", xout)

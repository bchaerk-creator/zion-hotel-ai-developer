# -*- coding: utf-8 -*-
"""<TAG>-ORC-001 · ORÇAMENTO ESTIMADO (INTERNO) por cabana: preços de mercado de referência (aço por kg e bitola, galvanização, lona por m²,
vidro, madeira, instalações, mão de obra por hora), BOM valorada em 3 cenários, visão por lote de contratação, escala 1/5/10/50 e faixa de
preço de venda. USO INTERNO: estimativa, não cotação. Saída: interno/<TAG>-ORC-001_Orcamento_Estimado.html/.pdf/.xlsx"""
import os, sys, html
from product_book_data import PRICES, LABOR_RATES, labor_hours, bom_priced, budget, scale_factors, SCENARIOS, price_for
from build_tecnico import CSS as BASE_CSS
from svgkit import zion_mark_html, zion_logo_html
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "interno"); os.makedirs(OUT, exist_ok=True)
DATE = "08/10/2026"; REV = "REV 00 — ESTIMATIVA INTERNA"
NAMES = {"cocoon": ("ZION CASULO", "ZC", 48.0, 29.9, 12), "zenith": ("ZION SAFARI", "ZS", 48.4, 28.0, 15), "lodge": ("ZION LODGE 38", "ZL", 38.0, 22.0, 9)}
LOTE_OF = {"01": 2, "02": 2, "03": 2, "04": 2, "05": 3, "06": 3, "07": 3, "08": 3, "09": 3, "10": 1, "11": 1, "13": 1, "14": 1, "16": 1, "12": 4, "15": 4, "17": 4, "18": 4}
LOTE_NAME = {1: "LOTE 1 · DECK, INFRA E INSTALAÇÕES", 2: "LOTE 2 · ESTRUTURA METÁLICA", 3: "LOTE 3 · LONA, ISOLAMENTO, FORRO E VIDROS", 4: "LOTE 4 · MOBÍLIAS, BANHO, ILUMINAÇÃO E ACABAMENTOS"}
LAB_OF = {"serralheiro": 2, "soldador": 2, "montador": 2, "lider": 2, "carpinteiro": 1, "eletricista": 1, "encanador": 1, "vidraceiro": 3, "membrana": 3, "marceneiro": 4, "acabamento": 4, "engenheiro": 0}

def esc(s): return html.escape(str(s))
def R(v, n=0): return ("R$ " + f"{v:,.{n}f}").replace(",", "X").replace(".", ",").replace("X", ".")
def table(head, rows, cls=""):
    th = "".join(f"<th{' class=num' if x.startswith('#') else ''}>{esc(x.lstrip('#'))}</th>" for x in head)
    body = "".join("<tr>" + "".join(f"<td{' class=num' if isinstance(c, (int, float)) or (isinstance(c, str) and c.startswith('R$')) else ''}>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="t {cls}"><tr>{th}</tr>{body}</table>'
def h(t, sub=""): return f'<h2>{esc(t)}{f"<small>{esc(sub)}</small>" if sub else ""}</h2>'

def compute(m):
    B = [budget(m, s) for s in range(3)]
    groups = bom_priced(m); lot_mat = {s: {1: 0, 2: 0, 3: 0, 4: 0} for s in range(3)}; rows_by_group = []
    for gname, items in groups:
        lot = LOTE_OF[gname[:2]]
        for (desc, un, qtd, key) in items:
            units = []
            for s in range(3):
                u = price_for(key, s, m)
                if s == 0 and key == "galv": u = PRICES["epoxi"][2] * PRICES["epoxi"][3]
                units.append(u); lot_mat[s][lot] += u * qtd
            rows_by_group.append((gname, lot, desc, un, qtd, units))
    hrs = labor_hours(m); lot_lab = {s: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0} for s in range(3)}; lab_rows = []
    for k, hh in hrs.items():
        d, std, fe, fp = LABOR_RATES[k]; rates = [std * fe, std, std * fp]
        for s in range(3): lot_lab[s][LAB_OF[k]] += rates[s] * hh
        lab_rows.append((d, LAB_OF[k], round(hh), rates))
    return B, rows_by_group, lot_mat, lab_rows, lot_lab

def build(m):
    name, tag, a_int, a_deck, days = NAMES[m]; code = f"{tag}-ORC-001"
    B, rows_by_group, lot_mat, lab_rows, lot_lab = compute(m)
    pages = []
    def page(body, label, cls=""):
        n = len(pages) + 1
        pages.append(f'<section class="page {cls}"><div class="head"><span>{zion_mark_html("14px", color="#1B2117")} {name} · {code} · {REV}</span><span>USO INTERNO · NÃO É COTAÇÃO</span><span>{esc(label)}</span></div>{body}<div class="foot"><span>ZION GLAMPING COLLECTION · ORÇAMENTO ESTIMADO · INTERNO · PREÇOS DE REFERÊNCIA A CONFIRMAR EM COTAÇÃO</span><span>R$ · base out/2026</span><span>{DATE} · {n:02d}</span></div></section>')
    tot = [b["total"] for b in B]; sub = [b["subtotal"] for b in B]; nre = B[0]["nre"]
    pages.append(f'''<section class="page cover"><div class="coverbox"><div class="brand">{zion_mark_html("13mm", color="#FEF5F0", style="margin-right:6mm")}{zion_logo_html("13mm", color="#FEF5F0")}</div><div class="sub">ZION GLAMPING COLLECTION · DOCUMENTO INTERNO · NÃO CIRCULA PARA FÁBRICA NEM CLIENTE</div>
<h1>ORÇAMENTO<br>ESTIMADO</h1><h3>{name} · {code} · {REV} · {DATE}</h3>
<p class="lead">Quanto custa uma unidade do {name} ({a_int:.0f} m² internos + {a_deck:.0f} m² de deck), estimado a partir dos quantitativos do projeto (lista ferro a ferro, padrões de lona, quadro de vidros, FF&amp;E) valorados com preços de mercado de referência: aço por kg e bitola, galvanização por kg, lona PVDF por m², vidro insulado por m², madeira, instalações e mão de obra por hora. Três cenários (Econômico, Zion Standard, Zion Premium), visão por lote de contratação, efeito de escala e faixa sugerida de preço de venda.</p>
<p class="rule">Toda linha é PREMISSA de mercado (pesquisa de distribuidores e fornecedores de SC / PR / SP, base 2025-2026, sem frete específico) e deve ser substituída pela cotação real dos fornecedores listados em ZG-RFQ-002. Esta estimativa serve para decidir, não para contratar. Margem de erro esperada: ± 20 % por grupo, ± 12 % no total.</p></div></section>''')
    # resumo
    body = h("RESUMO · QUANTO CUSTA UMA UNIDADE", f"{name} · 1 unidade isolada · custo de produção do kit + instalação no sítio · sem o desenvolvimento do produto")
    body += '<div class="stats">' + "".join(f"<div><b>{R(sub[s])}</b><span>{esc(SCENARIOS[s])} · custo da unidade</span></div>" for s in range(3)) + f'<div><b>{R(sub[1] / (a_int + a_deck))}/m²</b><span>Standard · por m² total ({a_int + a_deck:.0f} m²)</span></div></div>'
    rows = [("Materiais e insumos", *[R(b["mat_total"]) for b in B]), ("Mão de obra de fabricação (serralheria, solda)", *[R(b["fab_labor"]) for b in B]), ("Mão de obra de instalação (montagem, carpintaria, elétrica, hidráulica, vidro, lona, marcenaria, acabamento, engenheiro)", *[R(b["site_labor"]) for b in B]),
            ("Transporte (kit até o sítio)", *[R(b["transporte"]) for b in B]), ("Equipamentos (cravação, talha, andaime, gerador)", *[R(b["equipamentos"]) for b in B]), ("Hospedagem e alimentação da equipe", *[R(b["hospedagem"]) for b in B]),
            (f"<b>Custo direto</b>", *[f"<b>{R(b['mat_total'] + b['lab_total'] + b['transporte'] + b['equipamentos'] + b['hospedagem'])}</b>" for b in B]),
            (f"Indiretos (gestão, ART, seguros, ferramental) {B[1]['indiretos_pct'] * 100:.0f} %", *[R(b["indiretos"]) for b in B]), (f"Contingência {B[0]['conting_pct'] * 100:.0f} / {B[1]['conting_pct'] * 100:.0f} / {B[2]['conting_pct'] * 100:.0f} %", *[R(b["conting"]) for b in B]),
            ("<b>CUSTO ESTIMADO DA UNIDADE (kit + instalação)</b>", *[f"<b>{R(b['subtotal'])}</b>" for b in B]),
            ("Desenvolvimento do produto (projeto executivo, cálculo, form-finding, gabaritos, protótipo): só na 1ª unidade", *[R(b["nre"]) for b in B]), ("Custo da 1ª unidade com desenvolvimento", *[R(b["total"]) for b in B]),
            ("Custo por m² interno (sem desenvolvimento)", *[R(b["subtotal"] / a_int) for b in B]), ("Custo por m² total, interno + deck (sem desenvolvimento)", *[R(b["subtotal"] / (a_int + a_deck)) for b in B])]
    body += table(["Item", "#Econômico", "#Zion Standard", "#Zion Premium"], rows, "small")
    body += '<h4>O QUE MUDA ENTRE OS CENÁRIOS</h4><p class="lede"><b>Econômico:</b> lona PVC 900 g/m² com laca acrílica, pintura epóxi no lugar da galvanização, vidro laminado simples sem ruptura térmica, piso laminado, deck em eucalipto autoclavado, louças e mobiliário de linha nacional. <b>Zion Standard:</b> lona PVDF 1050 g/m², galvanização a fogo + pintura a pó, vidro insulado low-e com esquadria de ruptura térmica, carvalho, cumaru, marcenaria sob medida. <b>Premium:</b> membrana Précontraint importada, sistema de esquadria europeu, bomba de calor, automação, banheira de pedra composta, mobiliário de autor.</p>'
    page(body, "Resumo")
    # por lote
    lots = []
    for l in (1, 2, 3, 4):
        lots.append((f"<b>{LOTE_NAME[l]}</b>", *[R(lot_mat[s][l]) for s in range(3)], *[R(lot_lab[s][l]) for s in range(3)], *[f"<b>{R(lot_mat[s][l] + lot_lab[s][l])}</b>" for s in range(3)]))
    lots.append(("Engenheiro (acompanhamento, ART, QC) · transversal", "", "", "", *[R(lot_lab[s][0]) for s in range(3)], *[R(lot_lab[s][0]) for s in range(3)]))
    body = h("POR LOTE DE CONTRATAÇÃO", "o que esperar de cada fornecedor · materiais + mão de obra, sem transporte, indiretos e contingência")
    body += table(["Lote", "#Mat. Econ.", "#Mat. Std", "#Mat. Prem.", "#M.O. Econ.", "#M.O. Std", "#M.O. Prem.", "#Total Econ.", "#Total Std", "#Total Prem."], lots, "xsmall")
    share = [(LOTE_NAME[l].split(" · ")[0], f"{(lot_mat[1][l] + lot_lab[1][l]) / sum(lot_mat[1][k] + lot_lab[1][k] for k in (1, 2, 3, 4)) * 100:.0f} %") for l in (1, 2, 3, 4)]
    body += '<div class="two"><div><h4>PESO DE CADA LOTE (STANDARD)</h4>' + table(["Lote", "#Parcela"], share, "small") + '</div><div><h4>COMO LER</h4><ul class="chk"><li><b>Lote 2 (ferro)</b> é o mais barato e o mais previsível: aço por kg + galvanização por kg + horas de serralheiro. É onde a cotação local vai bater mais perto da estimativa.</li><li><b>Lote 3 (lona e vidro)</b> concentra o risco: membrana PVDF importada e vidro insulado curvo variam muito entre fornecedores (± 30 %).</li><li><b>Lote 1 (deck e infra)</b> depende do sítio: sondagem, acesso, distância da rede elétrica e da água.</li><li><b>Lote 4 (mobílias)</b> é o que mais muda com o padrão escolhido (Econômico a Premium quase dobra).</li></ul></div></div>'
    page(body, "Por lote")
    # preços de referência
    keys = sorted({k for _, items in bom_priced(m) for (_, _, _, k) in items})
    rows = [(esc(PRICES[k][0]), esc(PRICES[k][1]), R(PRICES[k][2] * PRICES[k][3], 2) if PRICES[k][3] else "—", R(PRICES[k][2], 2), R(PRICES[k][2] * PRICES[k][4], 2) if PRICES[k][4] else "—", esc(PRICES[k][5])) for k in keys]
    page(h("PREÇOS UNITÁRIOS DE REFERÊNCIA · MATERIAIS", "R$ por unidade · pesquisa de mercado SC / PR / SP 2025-2026 · PREMISSA: substituir pela cotação real") + table(["Material / serviço", "Un.", "#Econ.", "#Standard", "#Premium", "Fonte / observação"], rows, "xsmall"), "Preços unitários", "flow")
    rows = [(esc(d), l if l else "transv.", hh, R(r[0], 2), R(r[1], 2), R(r[2], 2), R(r[1] * hh)) for d, l, hh, r in lab_rows]
    page(h("MÃO DE OBRA · HORAS E R$/HORA", f"custo-empresa com encargos, EPI e ferramental · {sum(x[2] for x in lab_rows):.0f} horas por unidade · montagem em {days} dias com 4 montadores + líder") + table(["Função", "Lote", "#Horas", "#R$/h Econ.", "#R$/h Std", "#R$/h Prem.", "#Total Std"], rows, "small") + '<p class="note">Serralheiro e soldador são horas de fábrica (entram no preço do serralheiro no lote 2); as demais são horas no sítio. Hospedagem e alimentação da equipe no sítio estão em linha própria do resumo.</p>', "Mão de obra")
    # BOM valorada
    cur = None; out = []; chunks = []
    for gname, lot, desc, un, qtd, units in rows_by_group:
        if gname != cur: cur = gname; out.append((f"<b>{esc(gname)}</b> · lote {lot}", "", "", "", "", "", "", ""))
        out.append((esc(desc), esc(un), qtd, R(units[0], 2), R(units[1], 2), R(units[2], 2), R(units[1] * qtd), R(units[2] * qtd)))
    half = len(out) // 2
    while half < len(out) and not out[half][0].startswith("<b>"): half += 1
    page(h("BOM VALORADA · 18 GRUPOS (1 DE 2)", "quantitativos do projeto x preços unitários · totais nas colunas Standard e Premium") + table(["Item", "Un.", "#Qtd", "#Unit. Econ.", "#Unit. Std", "#Unit. Prem.", "#Total Std", "#Total Prem."], out[:half], "xsmall"), "BOM 1", "flow")
    page(h("BOM VALORADA · 18 GRUPOS (2 DE 2)", "") + table(["Item", "Un.", "#Qtd", "#Unit. Econ.", "#Unit. Std", "#Unit. Prem.", "#Total Std", "#Total Prem."], out[half:], "xsmall"), "BOM 2", "flow")
    # escala e venda
    rows = []
    for n in (1, 5, 10, 50):
        b = budget(m, 1, n); rows.append((n, R(b["mat_total"]), R(b["lab_total"]), R(b["transporte"] + b["equipamentos"] + b["hospedagem"]), R(b["indiretos"] + b["conting"]), R(b["nre"] / n), R(b["total"]), R(b["subtotal"]), R(b["subtotal"] / (a_int + a_deck))))
    body = h("ESCALA · 1, 5, 10 E 50 UNIDADES (STANDARD)", "redução por volume em materiais, mão de obra, transporte e indiretos · desenvolvimento diluído") + table(["Unidades", "#Materiais/un", "#M.O./un", "#Transp.+equip.+hosp./un", "#Indiretos+conting./un", "#Desenv./un", "#Total/un c/ desenv.", "#Custo/un s/ desenv.", "#R$/m² total"], rows, "small")
    s1 = budget(m, 1, 1)["subtotal"]; s10 = budget(m, 1, 10)["subtotal"]
    body += '<div class="two"><div><h4>FAIXA SUGERIDA DE PREÇO DE VENDA (KIT + INSTALAÇÃO)</h4>' + table(["Base", "#Custo", "#x 1,35 (franqueado / parceiro)", "#x 1,60 (cliente final)", "#x 1,90 (unidade Icon / exportação)"], [("1 unidade, Standard", R(s1), R(s1 * 1.35), R(s1 * 1.6), R(s1 * 1.9)), ("Série de 10, Standard", R(s10), R(s10 * 1.35), R(s10 * 1.6), R(s10 * 1.9))], "small") + '<p class="note">Fatores de referência: o FF&I 2025 da Zion praticava custo x 1,5. Separar sempre custo estimado de preço de venda; o preço final sai da cotação real + margem decidida pela diretoria.</p></div>'
    body += '<div><h4>O QUE PRECISA DE COTAÇÃO REAL ANTES DE QUALQUER NÚMERO SAIR DAQUI</h4><ol class="num"><li>Serralheria: R$/kg fabricado (corte, calandra, solda) + galvanização R$/kg + pintura a pó (ZG-RFQ-002, prioridade A).</li><li>Confeccionista de lona: R$/m² confeccionado de PVDF 1050 g/m² com keder + instalação por dia.</li><li>Vidraceiro: vidro insulado low-e R$/m², esquadria RPT R$/m², Olhos por unidade.</li><li>Estacas helicoidais: material por unidade + cravação por ponto + mobilização para o sítio.</li><li>Marcenaria e FF&amp;E: ZG-FFE-002 (Canopy Bed) e os demais itens da coleção.</li><li>Frete real até o sítio e custo da equipe fora de casa.</li></ol></div></div>'
    page(body, "Escala e venda")
    page(h("PREMISSAS E REVISÃO", "o que está dentro, o que está fora, e o que muda a conta") + '<div class="two"><div><h4>DENTRO</h4><ul class="chk"><li>Tudo o que está nas listas do projeto: estrutura, fundação, piso, deck, lona, isolamento, forro, vidros, portas, hidráulica, elétrica, iluminação, climatização, banheiro, marcenaria, mobiliário solto e enxoval de abertura.</li><li>Mão de obra de fábrica e de sítio, transporte do kit, equipamentos, hospedagem da equipe, indiretos e contingência.</li></ul><h4>FORA</h4><ul class="chk"><li>Terreno, acesso (estrada, ponte), rede elétrica e de água até o sítio, licenças e taxas, projeto legal e aprovação municipal.</li><li>Paisagismo, hot tub externo (opcional E07), Bico na versão Econômica.</li><li>Impostos sobre a venda e margem.</li></ul></div><div><h4>O QUE MAIS MEXE NO NÚMERO</h4>' + table(["Variável", "Efeito no custo Standard"], [("Aço: R$/kg de 10,80 para 13,00", "+ R$ 5 mil"), ("Lona PVDF: R$/m² de 215 para 300", "+ R$ 11 mil"), ("Vidro insulado: R$/m² de 920 para 1.300", "+ R$ 12 mil"), ("Sítio sem acesso de caminhão (transbordo 4x4)", "+ R$ 8 a 15 mil"), ("Série de 10 unidades", "− 14 % por unidade"), ("Cenário Econômico em lona, vidro e piso", "− 25 a 30 %")], "small") + table(["Rev", "Data", "Descrição"], [("00", DATE, "Estimativa interna a partir da BOM do product book e dos preços de referência 2025-2026; nenhuma cotação real incorporada")], "small") + "</div></div>", "Premissas")
    css = BASE_CSS + " .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:6px 0 10px} .stats div{border-top:2px solid var(--ink);padding-top:5px} .stats b{display:block;font-size:17px;font-weight:600} .stats span{display:block;font-size:7.5px;letter-spacing:.14em;color:var(--earth);text-transform:uppercase;margin-top:2px}"
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · {code} · Orçamento estimado (interno)</title><style>{css}</style></head><body>{"".join(pages)}</body></html>'
    path = os.path.join(OUT, f"{code}_Orcamento_Estimado.html"); open(path, "w", encoding="utf-8").write(doc); print(os.path.relpath(path, ROOT), len(pages), "páginas")
    # XLSX
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Resumo"
    bold = Font(bold=True); fill = PatternFill("solid", fgColor="DED6BF")
    ws.append([f"{name} · {code} · ORÇAMENTO ESTIMADO (INTERNO) · {DATE} · PREMISSAS DE MERCADO, NÃO É COTAÇÃO"]); ws.append([])
    ws.append(["Item", "Econômico", "Zion Standard", "Zion Premium"]); [setattr(c, "font", bold) for c in ws[3]]
    for lbl, key in (("Materiais", "mat_total"), ("M.O. fabricação", "fab_labor"), ("M.O. instalação", "site_labor"), ("Transporte", "transporte"), ("Equipamentos", "equipamentos"), ("Hospedagem", "hospedagem"), ("Indiretos", "indiretos"), ("Contingência", "conting"), ("CUSTO DA UNIDADE (kit + instalação)", "subtotal"), ("Desenvolvimento (1ª unidade)", "nre"), ("Custo da 1ª unidade com desenvolvimento", "total")):
        ws.append([lbl] + [round(b[key], 2) for b in B])
    ws2 = wb.create_sheet("Por lote"); ws2.append(["Lote", "Mat. Econ.", "Mat. Std", "Mat. Prem.", "M.O. Econ.", "M.O. Std", "M.O. Prem.", "Total Std"]); [setattr(c, "font", bold) for c in ws2[1]]
    for l in (1, 2, 3, 4): ws2.append([LOTE_NAME[l]] + [round(lot_mat[s][l], 2) for s in range(3)] + [round(lot_lab[s][l], 2) for s in range(3)] + [round(lot_mat[1][l] + lot_lab[1][l], 2)])
    ws3 = wb.create_sheet("BOM valorada"); ws3.append(["Grupo", "Lote", "Item", "Un.", "Qtd", "Unit. Econ.", "Unit. Std", "Unit. Prem.", "Total Econ.", "Total Std", "Total Prem."]); [setattr(c, "font", bold) for c in ws3[1]]
    for gname, lot, desc, un, qtd, units in rows_by_group: ws3.append([gname, lot, desc, un, qtd] + [round(u, 2) for u in units] + [round(u * qtd, 2) for u in units])
    ws4 = wb.create_sheet("Preços unitários"); ws4.append(["Chave", "Material / serviço", "Un.", "Econ.", "Standard", "Premium", "Fonte"]); [setattr(c, "font", bold) for c in ws4[1]]
    for k in keys: ws4.append([k, PRICES[k][0], PRICES[k][1], round(PRICES[k][2] * PRICES[k][3], 2), PRICES[k][2], round(PRICES[k][2] * PRICES[k][4], 2), PRICES[k][5]])
    ws5 = wb.create_sheet("Mão de obra"); ws5.append(["Função", "Lote", "Horas", "R$/h Econ.", "R$/h Std", "R$/h Prem.", "Total Std"]); [setattr(c, "font", bold) for c in ws5[1]]
    for d, l, hh, r in lab_rows: ws5.append([d, l, hh, round(r[0], 2), r[1], round(r[2], 2), round(r[1] * hh, 2)])
    ws6 = wb.create_sheet("Escala"); ws6.append(["Unidades", "Materiais/un", "M.O./un", "Transp+equip+hosp/un", "Indiretos+conting/un", "Desenv/un", "Total/un c/ desenv", "Custo/un s/ desenv", "R$/m² total"]); [setattr(c, "font", bold) for c in ws6[1]]
    for n in (1, 5, 10, 50):
        b = budget(m, 1, n); ws6.append([n, round(b["mat_total"]), round(b["lab_total"]), round(b["transporte"] + b["equipamentos"] + b["hospedagem"]), round(b["indiretos"] + b["conting"]), round(b["nre"] / n), round(b["total"]), round(b["subtotal"]), round(b["subtotal"] / (a_int + a_deck))])
    for w in wb: 
        for col in w.columns: w.column_dimensions[col[0].column_letter].width = 22
    wb.save(os.path.join(OUT, f"{code}_Orcamento_Estimado.xlsx"))
    return B, lot_mat, lot_lab

if __name__ == "__main__":
    for m in (sys.argv[1:] or ["cocoon"]):
        B, lm, ll = build(m)
        for s in range(3): print(SCENARIOS[s], "subtotal", round(B[s]["subtotal"]), "total c/ NRE", round(B[s]["total"]), "lotes", {l: round(lm[s][l] + ll[s][l]) for l in (1, 2, 3, 4)})

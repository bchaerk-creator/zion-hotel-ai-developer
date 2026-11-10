"""Testa a planilha Matriz de Compras e Manutenção recalculando no LibreOffice e comparando com uma conta independente em Python.
Uso: python3 -I tests/test_planilha.py <pasta com os xlsx>"""
import sys, pathlib, subprocess, tempfile, math, copy
from openpyxl import load_workbook
D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR = "Matriz-de-Compras-e-Manutencao-Zion-EM-BRANCO.xlsx"; EXF = "Matriz-de-Compras-e-Manutencao-Zion-EXEMPLO.xlsx"
def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)
def recalc(path):
    t = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(t), str(path)], check=True, capture_output=True, timeout=180)
    return load_workbook(t / path.name, data_only=True)
def perto(a, b, tol=0.005): return isinstance(a, (int, float)) and b is not None and abs(a - b) <= tol

# ---- conta independente (não usa a planilha nem o logic.js) ----
PASSO = {"Mensal": 1, "Bimestral": 2, "Trimestral": 3, "Semestral": 6, "Anual": 12}
def conta(d):
    itens = [it for it in d["itens"] if it[0]]
    total = sum(it[2] for it in itens); out = dict(itens=[])
    for nome, un, gasto, tipo, atual, c1, c2, c3, contr in itens:
        cots = [c for c in (c1, c2, c3) if c and c > 0]; menor = min(cots) if cots else None
        qtd = gasto / atual if atual else None
        dif = max(0, qtd * (atual - menor)) if qtd is not None and menor is not None else None
        out["itens"].append(dict(n=len(cots), menor=menor, qtd=qtd, dif=dif, noite=gasto / d["noites"], hosp=gasto / d["hospedes"] if d["hospedes"] else None, peso=gasto / total))
    var = sum(it[2] for it in itens if it[3] == "Variável"); vn = var / d["noites"]
    out.update(total=total, var=var, vn=vn, cob=vn / d["cv"] if d["cv"] else None, cheio=vn * d["unidades"] * 30, dif=sum(x["dif"] or 0 for x in out["itens"]))
    out["difAno"] = out["dif"] * 12 / d["meses"]
    out["semTres"] = sum(1 for x in out["itens"] if x["n"] < 3); out["semContr"] = sum(1 for it in itens if it[8] == "Sem contrato")
    est = []
    for nome, un, uso, ent, seg, atual, ciclo in d["estoque"]:
        dia = uso / 30; ppb = dia * (ent + seg); pp = math.ceil(ppb - 1e-9); mn = math.ceil(dia * seg - 1e-9); ped = atual <= pp
        est.append(dict(min=mn, pp=pp, pedir=ped, pedido=max(0, math.ceil(ppb + dia * ciclo - atual - 1e-9)) if ped else 0))
    out["est"] = est; out["pedir"] = sum(1 for e in est if e["pedir"])
    out["porCama"] = d["jogos"] / d["camas"] if d["camas"] else None
    meses = [((d["inicio"] - 1 + i) % 12) + 1 for i in range(12)]
    res_m = d["receita"] * d["reserva"] / 100; acum = 0; gasto = 0; cal = []; pesadas = 0; descob = 0
    for i, m in enumerate(meses):
        ts = [t for t in d["tarefas"] if t[1] in PASSO and 1 <= t[2] <= 12 and ((m - t[2]) % 12) % PASSO[t[1]] == 0]
        c = sum(t[3] for t in ts); gasto += c; acum += res_m
        if m in d["cheia"]: pesadas += sum(1 for t in ts if PASSO[t[1]] >= 6)
        if gasto > acum + 0.005: descob += 1
        cal.append(dict(n=len(ts), custo=c, cobre=gasto <= acum + 0.005))
    out.update(cal=cal, totalAno=gasto, reservaAno=res_m * 12, pesadas=pesadas, descob=descob, ocorr=sum(x["n"] for x in cal))
    sinais = [out["semTres"] > 0, out["semContr"] > 0, out["pedir"] > 0, out["porCama"] is not None and out["porCama"] < 3, pesadas > 0, descob > 0 and len(d["tarefas"]) > 0,
              d["ronda"] != "Sim" or d["ocorr"] != "Sim", not d["dia"] or not (d["alcada"] and d["alcada"] > 0)]
    nomes = ["Item sem três cotações", "Compra recorrente sem contrato", "Item no ponto de pedido", "Menos de três jogos por cama", "Manutenção pesada na casa cheia", "A reserva não cobre o plano",
             "Sem ronda diária ou sem registro de ocorrências", "Estoque sem dia de contagem ou compra sem limite"]
    out["sinais"] = sinais; out["causa"] = next((n for n, s in zip(nomes, sinais) if s), "Compras e manutenção dentro das regras da fonte")
    return out

EX = dict(meses=3, noites=174, hospedes=150, unidades=4, cv=28.32, prazo="31/03/2027",
          itens=[("Café da manhã e cestas (insumos)", "cesta montada", 1260, "Vendido à parte", 28, 28, 25.5, 26.9, "Vou fechar"),
                 ("Lavanderia do enxoval", "kg lavado", 900, "Variável", 3, 3, 2.6, 3.2, "Tem contrato"),
                 ("Amenidades (sabonete, xampu, papel, água)", "kit por estadia", 780, "Variável", 10.4, 10.4, 8.9, 9.8, "Vou fechar"),
                 ("Gás do aquecimento da água", "botijão de 13 kg", 720, "Variável", 120, 120, 112, 118, "Sem contrato"),
                 ("Reposição de enxoval", "jogo de cama de casal", 240, "Variável", 120, 120, 98, 135, "Vou fechar")],
          estoque=[("Kit de amenidades", "kit", 25, 7, 7, 14, 30), ("Papel higiênico", "rolo", 100, 5, 7, 30, 30), ("Botijão de gás de 13 kg", "botijão", 2, 2, 7, 2, 15), ("Café em pó (pacote de 500 g)", "pacote", 8, 3, 7, 6, 15)],
          camas=4, jogos=10, ano=2027, inicio=1, receita=13565.6, reserva=3, cheia=[6, 7, 8, 12],
          tarefas=[("Limpar os filtros do ar-condicionado", "Trimestral", 1, 0, "Equipe"), ("Controle de pragas", "Trimestral", 2, 180, "Empresa contratada"), ("Revisão do aquecedor a gás", "Anual", 3, 280, "Técnico"),
                   ("Revisão elétrica (quadro e tomadas)", "Anual", 4, 350, "Eletricista"), ("Limpeza das calhas", "Semestral", 4, 150, "Equipe"), ("Limpeza da caixa d'água", "Semestral", 5, 250, "Empresa"),
                   ("Revisão do ar-condicionado por técnico", "Anual", 9, 480, "Técnico"), ("Inspeção e recarga dos extintores", "Anual", 10, 160, "Empresa"), ("Tratamento do deck (óleo e vedação)", "Anual", 11, 900, "Marceneiro")],
          dia="segunda-feira", quem="Ana (dona)", alcada=300, ronda="Sim", ocorr="Sim")

def escrever(wb, d):
    mz, es, mn, ro = wb["Matriz de Compras"], wb["Estoque"], wb["Manutenção 12 meses"], wb["Rotina e checklist"]
    for cel, k in (("B5", "meses"), ("B6", "noites"), ("B7", "hospedes"), ("B8", "unidades"), ("B9", "cv"), ("B10", "prazo")): mz[cel] = d.get(k)
    for i in range(8):
        for c in range(9): mz.cell(14 + i, 1 + c, d["itens"][i][c] if i < len(d["itens"]) else None)
    for i in range(10):
        for c in range(7): es.cell(5 + i, 1 + c, d["estoque"][i][c] if i < len(d["estoque"]) else None)
    es["B17"] = d["camas"]; es["B18"] = d["jogos"]
    for cel, k in (("B4", "ano"), ("B5", "inicio"), ("B6", "receita"), ("B7", "reserva")): mn[cel] = d[k]
    for i in range(15):
        for c in range(5): mn.cell(13 + i, 1 + c, d["tarefas"][i][c] if i < len(d["tarefas"]) else None)
    for i in range(12): mn.cell(32 + i, 4, "Sim" if (((d["inicio"] - 1 + i) % 12) + 1) in d["cheia"] else "Não")
    for cel, k in (("B4", "dia"), ("B5", "quem"), ("B6", "alcada"), ("B7", "ronda"), ("B8", "ocorr")): ro[cel] = d.get(k)

def confere(wb, d, nome):
    E = conta(d); mz, es, mn, rs = wb["Matriz de Compras"], wb["Estoque"], wb["Manutenção 12 meses"], wb["Resumo"]
    okI = True
    for i, x in enumerate(E["itens"]):
        l = 14 + i; v = [mz.cell(l, c).value for c in range(10, 17)]
        okI &= v[0] == x["n"] and (x["menor"] is None or perto(v[1], x["menor"])) and (x["qtd"] is None or perto(v[2], x["qtd"])) and (x["dif"] is None or perto(v[3], x["dif"])) and perto(v[4], x["noite"]) and (x["hosp"] is None or perto(v[5], x["hosp"])) and perto(v[6], x["peso"], 1e-6)
    log(okI, f"{nome}: cada item da Matriz (cotações, menor, quantidade, diferença, por noite, por hóspede, peso)")
    log(perto(mz["B24"].value, E["total"]) and perto(mz["B26"].value, E["vn"]) and (E["cob"] is None or perto(mz["B27"].value, E["cob"], 1e-6)) and perto(mz["B29"].value, E["cheio"]) and perto(mz["B30"].value, E["dif"]) and perto(mz["B31"].value, E["difAno"]) and mz["B33"].value == E["semTres"] and mz["B34"].value == E["semContr"],
        f"{nome}: resumo da Matriz (total {E['total']:.2f}, por noite {E['vn']:.2f}, diferença {E['dif']:.2f})")
    okE = all(es.cell(5 + i, 9).value == x["min"] and es.cell(5 + i, 10).value == x["pp"] and es.cell(5 + i, 11).value == ("Pedir agora" if x["pedir"] else "OK") and es.cell(5 + i, 12).value == x["pedido"] for i, x in enumerate(E["est"]))
    log(okE and es["B22"].value == E["pedir"] and (E["porCama"] is None or perto(es["B19"].value, E["porCama"])), f"{nome}: estoque mínimo, ponto de pedido, situação e pedido ({E['pedir']} para pedir)")
    okC = all(mn.cell(32 + i, 5).value == x["n"] and perto(mn.cell(32 + i, 6).value, x["custo"]) and mn.cell(32 + i, 9).value == ("Cobre" if x["cobre"] else "Não cobre") for i, x in enumerate(E["cal"]))
    log(okC and perto(mn["B47"].value, E["totalAno"]) and mn["B46"].value == E["ocorr"] and perto(mn["B9"].value, E["reservaAno"]) and mn["B52"].value == E["pesadas"] and mn["B51"].value == E["descob"],
        f"{nome}: calendário mês a mês ({E['ocorr']} tarefas, {E['totalAno']:.2f}), reserva e casa cheia")
    sin = [rs.cell(17 + i, 2).value == ("Sim" if s else "Não") for i, s in enumerate(E["sinais"])]
    log(all(sin) and rs["B26"].value == E["causa"], f"{nome}: sinais e causa principal ({E['causa']})")
    return E

def cenario(d, nome):
    t = pathlib.Path(tempfile.mkdtemp()) / BR
    wb = load_workbook(D / BR); escrever(wb, d); wb.save(t)
    w = recalc(t); return confere(w, d, nome), w

# 1. Exemplo publicado
wbx = recalc(D / EXF); Ex = confere(wbx, EX, "exemplo")
log(perto(wbx["Matriz de Compras"]["B26"].value, 15.1724, 1e-4) and perto(wbx["Matriz de Compras"]["B30"].value, 437) and perto(wbx["Manutenção 12 meses"]["B47"].value, 3690) and perto(wbx["Manutenção 12 meses"]["B9"].value, 4883.616) and wbx["Estoque"]["L6"].value == 110,
    "exemplo = números do plano: 15,17 por noite, diferença 437, plano 3.690, reserva 4.883,62, papel pede 110")
log(wbx["Resumo"]["B26"].value == "Compra recorrente sem contrato" and wbx["Resumo"]["B27"].value == "OK" and wbx["Matriz de Compras"]["B36"].value == "OK" and wbx["Estoque"]["B23"].value == "OK" and wbx["Manutenção 12 meses"]["B53"].value == "OK", "exemplo: causa principal e situação OK em todas as abas")
log(wbx["Matriz de Compras"]["A2"].value.startswith("EXEMPLO DIDÁTICO") and "dados fictícios" in wbx["Comece aqui"]["A4"].value.lower(), "exemplo rotulado como dados fictícios")
erros = [f"{ws.title}!{c.coordinate}" for ws in wbx.worksheets for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith(("#", "Err:"))]
log(not erros, "exemplo sem células com erro" + (": " + ", ".join(erros[:5]) if erros else ""))

# 2. Em branco
wbb = recalc(D / BR)
erros = [f"{ws.title}!{c.coordinate}" for ws in wbb.worksheets for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith(("#", "Err:"))]
log(not erros, "em branco sem células com erro" + (": " + ", ".join(erros[:5]) if erros else ""))
log(wbb["Matriz de Compras"]["B36"].value.startswith("Preencha") and wbb["Estoque"]["B23"].value.startswith("Informe") and wbb["Manutenção 12 meses"]["B53"].value.startswith("Preencha") and wbb["Resumo"]["B27"].value != "OK", "em branco: situação pede o preenchimento")
log(wbb["Matriz de Compras"]["B33"].value == 0 and wbb["Estoque"]["B22"].value == 0 and wbb["Manutenção 12 meses"]["B47"].value == 0, "em branco: contagens zeradas")

# 3. Cenários
def mud(f): d = copy.deepcopy(EX); f(d); return d
cenario(mud(lambda d: d.update(inicio=7)), "calendário de julho a junho")
cenario(mud(lambda d: d["tarefas"].__setitem__(8, ("Tratamento do deck (óleo e vedação)", "Anual", 7, 900, "Marceneiro")) or d.update(jogos=12) or d["estoque"].__setitem__(1, ("Papel higiênico", "rolo", 100, 5, 7, 200, 30)) or d["itens"].__setitem__(3, EX["itens"][3][:8] + ("Tem contrato",))), "deck em julho (casa cheia)")
E, wd = cenario(mud(lambda d: d["tarefas"].__setitem__(8, ("Tratamento do deck (óleo e vedação)", "Anual", 1, 900, "Marceneiro")) or d.update(jogos=12) or d["estoque"].__setitem__(1, ("Papel higiênico", "rolo", 100, 5, 7, 200, 30)) or d["itens"].__setitem__(3, EX["itens"][3][:8] + ("Tem contrato",))), "deck em janeiro (reserva não cobre)")
log(wd["Manutenção 12 meses"]["I32"].value == "Não cobre" and wd["Resumo"]["B26"].value == "A reserva não cobre o plano", "deck em janeiro: janeiro não cobre e vira a causa principal")
cenario(mud(lambda d: d["itens"].__setitem__(2, EX["itens"][2][:7] + (None, "Vou fechar"))), "item com duas cotações")
cenario(mud(lambda d: d.update(jogos=12, ronda="Não") or d["estoque"].__setitem__(1, ("Papel higiênico", "rolo", 100, 5, 7, 200, 30)) or d["itens"].__setitem__(3, EX["itens"][3][:8] + ("Tem contrato",))), "sem ronda diária")
cenario(mud(lambda d: d.update(jogos=12, dia="", alcada=None) or d["estoque"].__setitem__(1, ("Papel higiênico", "rolo", 100, 5, 7, 200, 30)) or d["itens"].__setitem__(3, EX["itens"][3][:8] + ("Tem contrato",))), "sem dia de contagem nem limite")
E2, w2 = cenario(mud(lambda d: d.update(jogos=12) or d["estoque"].__setitem__(1, ("Papel higiênico", "rolo", 100, 5, 7, 200, 30)) or d["itens"].__setitem__(3, EX["itens"][3][:8] + ("Tem contrato",))), "tudo resolvido")
log(w2["Resumo"]["B26"].value == "Compras e manutenção dentro das regras da fonte", "tudo resolvido: dentro das regras da fonte")
cenario(mud(lambda d: d.update(meses=1, noites=58, hospedes=50, reserva=6) or [d["itens"].__setitem__(i, (it[0], it[1], it[2] / 3) + it[3:]) for i, it in enumerate(EX["itens"])]), "um mês só e reserva de 6%")
cenario(mud(lambda d: d.update(estoque=[("Lenha", "saco", 45, 1, 14, 21, 7), ("Cloro", "kg", 4.5, 10, 10, 3, 30), ("Detergente", "frasco", 9, 3, 7, 0, 30)])), "estoque com decimais e zerado")
cenario(mud(lambda d: d.update(tarefas=[("Revisão mensal", "Mensal", 6, 50, "Equipe"), ("Bimestral", "Bimestral", 12, 80, "Equipe"), ("Anual de dezembro", "Anual", 12, 700, "Técnico")], inicio=11)), "mensal, bimestral e anual atravessando o ano")
_, wv = cenario(mud(lambda d: d.update(cv=10)), "Matriz acima do custo da Folha")
log(wv["Matriz de Compras"]["B27"].value > 1, "Matriz acima do custo da Folha: mais de 100%")

# 4. Bloqueios
t = pathlib.Path(tempfile.mkdtemp()) / BR; wb = load_workbook(D / BR); escrever(wb, mud(lambda d: d["itens"].__setitem__(1, ("Lavanderia do enxoval", "kg lavado", None, "Variável", 3, 3, 2.6, 3.2, "Tem contrato")))); wb.save(t); wbk = recalc(t)
log(wbk["Matriz de Compras"]["B36"].value == "Há item sem gasto" and wbk["Resumo"]["B27"].value == "Confira a aba Matriz de Compras", "item sem gasto: Matriz e Resumo avisam")
t = pathlib.Path(tempfile.mkdtemp()) / BR; wb = load_workbook(D / BR); d = mud(lambda d: d.update(prazo=None)); escrever(wb, d); wb.save(t); w = recalc(t)
log(w["Matriz de Compras"]["B36"].value == "Marque até quando vai fechar os contratos", "contrato a fechar sem data: avisa")
t = pathlib.Path(tempfile.mkdtemp()) / BR; wb = load_workbook(D / BR); d = mud(lambda d: d["tarefas"].__setitem__(0, ("Limpar filtros", None, 1, 0, "Equipe"))); escrever(wb, d); wb.save(t); w = recalc(t)
log(w["Manutenção 12 meses"]["B53"].value == "Escolha a frequência e o primeiro mês de cada tarefa", "tarefa sem frequência: avisa")
t = pathlib.Path(tempfile.mkdtemp()) / BR; wb = load_workbook(D / BR); d = mud(lambda d: d["estoque"].__setitem__(0, ("Kit", "kit", 25, None, 7, 14, 30))); escrever(wb, d); wb.save(t); w = recalc(t)
log(w["Estoque"]["B23"].value.startswith("Complete uso"), "estoque sem prazo de entrega: avisa")
print(f"\n{ok} ok, {fal} falhou"); sys.exit(1 if fal else 0)

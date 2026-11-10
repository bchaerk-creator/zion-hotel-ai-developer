"""Testa a planilha Tabela de Preço e Canais recalculando no LibreOffice e comparando com uma conta independente em Python.
Uso: python3 -I tests/test_planilha.py <pasta com os xlsx>"""
import sys, pathlib, subprocess, tempfile, calendar, re
from openpyxl import load_workbook
D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR = "Tabela-de-Preco-e-Canais-Zion-EM-BRANCO.xlsx"; EXF = "Tabela-de-Preco-e-Canais-Zion-EXEMPLO.xlsx"
def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)
def recalc(path):
    t = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(t), str(path)], check=True, capture_output=True, timeout=180)
    return load_workbook(t / path.name, data_only=True)
def perto(a, b, tol=0.005): return isinstance(a, (int, float)) and b is not None and abs(a - b) <= tol

# ---- conta independente (não usa a planilha nem o logic.js) ----
def conta(d):
    nE = d["ne"] if d["ne"] > 0 else 1
    canais = []
    for nome, mix, com, pag, extra, direta in d["canais"]:
        ded = com + pag + d["imposto"]; f = 1 - ded / 100
        liq = d["ref"] * f - extra / nE
        canais.append(dict(nome=nome, mix=mix, com=com, ded=ded, liq=liq, marg=liq - d["cv"], pc=(d["cpn"] + extra / nE) / f if mix > 0 else None, lv=(d["cv"] + extra / nE) / f, direta=direta == "Sim"))
    ativos = [c for c in canais if c["pc"] is not None]; crit = max(ativos, key=lambda c: c["pc"])
    diretaAt = sum(c["mix"] for c in canais if c["direta"]); pagos = [c for c in canais if not c["direta"] and c["mix"] > 0]
    comPagos = sum(c["mix"] * c["com"] for c in pagos) / sum(c["mix"] for c in pagos) if pagos else 0
    fat = dict(d["fatores"], Base=1); dia = {k: d["ref"] * v for k, v in fat.items()}
    picosMes = {}
    for nome, mes, n, fator, mn, ab in d["picos"]: picosMes.setdefault(mes, []).append((n, fator))
    nf = dict(Vale=0, Baixa=0, Base=0, Alta=0, pico=0); meses = []; somaR = somaN = 0
    for i in range(12):
        m0 = d["inicio"] - 1 + i; ano = d["ano"] + m0 // 12; mes = m0 % 12 + 1
        dias = calendar.monthrange(ano, mes)[1]; fds = sum(1 for x in range(1, dias + 1) if calendar.weekday(ano, mes, x) in (4, 5)); sem = dias - fds
        pn = min(dias, sum(n for n, f in picosMes.get(mes, []))); semR = max(0, sem - pn); fdsR = max(0, fds - max(0, pn - sem))
        fs, ff = d["meses"][i]; rec = semR * dia[fs] + fdsR * dia[ff] + sum(n * d["ref"] * f for n, f in picosMes.get(mes, []))
        nf[fs] += semR; nf[ff] += fdsR; nf["pico"] += pn; somaR += rec; somaN += dias
        meses.append(dict(dias=dias, fds=fds, media=rec / dias))
    pc = crit["pc"]; pcalc = pc * (1 + d["margem"] / 100)
    return dict(canais=canais, pc=pc, pcalc=pcalc, lv=crit["lv"], comMedia=sum(c["mix"] * c["com"] for c in canais) / 100, diretaAt=diretaAt, comPagos=comPagos,
                comFica=d["receita"] * (d["meta"] - diretaAt) / 100 * comPagos / 100 if d.get("receita") and d["meta"] > diretaAt else None,
                dia=dia, nf=nf, meses=meses, media=somaR / somaN, total=somaN, mercado=sorted(d["conc"])[1:-1])

EX = dict(cv=28.32, cpn=153.04, ne=2.32, imposto=6, receita=16240, atual=280, conc=[270, 280, 290, 300, 310, 320, 360], terco="Meio", ref=300,
          canais=[("Plataforma A", 50, 16, 1.5, 0, "Não"), ("Plataforma B", 20, 15, 1.5, 0, "Não"), ("Venda direta (site e WhatsApp)", 30, 0, 1.5, 0, "Sim")],
          meta=40, prazo="30/06/2027", gestor="Sim", motor="Não", margem=10, piso=225, quem="Eu e quem responde o WhatsApp",
          fatores=dict(Vale=0.75, Baixa=0.90, Alta=1.50, Pico=2.20), ano=2027, inicio=1,
          meses=[("Baixa", "Base"), ("Baixa", "Base"), ("Vale", "Baixa"), ("Vale", "Baixa"), ("Vale", "Base"), ("Base", "Alta"), ("Alta", "Alta"), ("Base", "Alta"), ("Baixa", "Base"), ("Baixa", "Base"), ("Vale", "Baixa"), ("Baixa", "Base")],
          picos=[("Carnaval", 2, 4, 2.2, 4, "3 a 5 meses antes"), ("Corpus Christi (feriado prolongado)", 5, 4, 1.9, 3, "2 a 4 meses antes"), ("Festival de inverno (evento local)", 7, 3, 2.0, 2, "assim que a data sair"), ("Réveillon", 12, 5, 2.4, 5, "4 a 6 meses antes")])

def escrever(wb, d):
    cr, mc, pi, ca, dp = wb["Custo e Referência"], wb["Mapa de Canais"], wb["Piso"], wb["Calendário 12 meses"], wb["Datas de pico"]
    for cel, k in (("B5", "cv"), ("B6", "cpn"), ("B7", "ne"), ("B8", "imposto"), ("B9", "receita"), ("B10", "atual"), ("B24", "terco"), ("B26", "ref")): cr[cel] = d.get(k)
    for i in range(9): cr.cell(13 + i, 2, d["conc"][i] if i < len(d["conc"]) else None)
    for i in range(5):
        for col in range(6): mc.cell(5 + i, 1 + col, d["canais"][i][col] if i < len(d["canais"]) else None)
    for cel, k in (("B17", "meta"), ("B18", "prazo"), ("B20", "gestor"), ("B21", "motor")): mc[cel] = d.get(k)
    pi["B6"] = d["margem"]; pi["B8"] = d["piso"]; pi["B10"] = d.get("quem")
    for k, l in (("Vale", 4), ("Baixa", 5), ("Alta", 7), ("Pico", 8)): ca.cell(l, 2, d["fatores"][k])
    ca["B10"] = d["ano"]; ca["B11"] = d["inicio"]
    for i in range(12): ca.cell(14 + i, 7, d["meses"][i][0]); ca.cell(14 + i, 8, d["meses"][i][1])
    for i in range(8):
        for col in range(6): dp.cell(5 + i, 1 + col, d["picos"][i][col] if i < len(d["picos"]) else None)
def cenario(nome, d):
    wb = load_workbook(D / BR); escrever(wb, d)
    x = pathlib.Path(tempfile.mkdtemp()) / ("t_" + nome + ".xlsx"); wb.save(x); return recalc(x)

print("Exemplo preenchido (dados fictícios, PLANO seção 9)")
wb = recalc(D / EXF); r = conta(EX)
cr, mc, pi, ca, dp, rs = wb["Custo e Referência"], wb["Mapa de Canais"], wb["Piso"], wb["Calendário 12 meses"], wb["Datas de pico"], wb["Resumo"]
log(all(s == "OK" for s in (cr["B28"].value, mc["B24"].value, pi["B21"].value, ca["B36"].value)), "situação dos dados OK nas quatro abas")
log(cr["B22"].value == 7 and perto(cr["B23"].value, sum(r["mercado"]) / 5) and cr["B23"].value == 300 and cr["B25"].value == 300, "referência: média sem extremos 300; posição do meio 300")
log(all(perto(mc.cell(5 + i, 8).value, c["liq"]) and perto(mc.cell(5 + i, 9).value, c["marg"]) for i, c in enumerate(r["canais"])), "líquido e margem por canal = conta independente (229,50 / 232,50 / 277,50)")
log(perto(mc["B13"].value, 11) and mc["B14"].value == 30 and perto(mc["B15"].value, r["comPagos"]) and mc["B16"].value == 2, "comissão média 11%, venda direta 30%, comissão dos pagos 15,71%, 2 canais pagos")
log(perto(mc["B19"].value, 255.20) and perto(mc["B19"].value, r["comFica"]), f"meta 40%: comissão que deixaria de sair {mc['B19'].value:.2f} (ref 255,20)")
log(mc["B22"].value == "Venda direta (site e WhatsApp)" and mc["B23"].value == "Plataforma A", "canal de maior e de menor margem")
log(perto(pi["B5"].value, r["pc"]) and perto(pi["B5"].value, 200.05) and perto(pi["B7"].value, 220.06) and perto(pi["B19"].value, 37.02), "custo no canal mais caro 200,05; piso calculado 220,06; limite do variável 37,02")
log(perto(pi["B9"].value, 0.75) and pi["B20"].value == "Piso cobre o custo com a sua margem mínima", "piso 225 = 75% da referência; leitura do piso")
log(all(perto(ca.cell(4 + k, 3).value, v) for k, v in enumerate([225, 270, 300, 450, 660])), "diárias das faixas 225 / 270 / 300 / 450 / 660")
log(all(ca.cell(14 + i, 3).value == m["dias"] and ca.cell(14 + i, 4).value == m["fds"] for i, m in enumerate(r["meses"])), "dias e noites de sexta e sábado de cada mês = calendário do Python")
log(all(perto(ca.cell(14 + i, 14).value, m["media"]) for i, m in enumerate(r["meses"])), "média de cada um dos 12 meses = conta independente")
log([ca.cell(28 + k, 2).value for k in range(4)] == [r["nf"][k] for k in ("Vale", "Baixa", "Base", "Alta")] == [84, 122, 99, 44] and ca["B32"].value == 16 and ca["B33"].value == 365, "noites por faixa 84 / 122 / 99 / 44, pico 16, total 365")
log(perto(ca["B34"].value, r["media"], 1e-6) and perto(ca["B34"].value, 305.92), f"diária média do calendário {ca['B34'].value:.2f} (ref 305,92)")
log(ca["B35"].value == "Nenhuma" and all(dp.cell(5 + i, 9).value == "ok" for i in range(4)) and perto(dp["G8"].value, 720), "nenhuma faixa nem data abaixo do piso; réveillon 720")
log(rs["B14"].value == "Não" and rs["B15"].value == "Venda direta sem motor de reservas", f"resumo: causa principal '{rs['B15'].value}' (igual à ficha)")
wbx = load_workbook(D / EXF)
log([s.title for s in wbx.worksheets] == ["Comece aqui", "Custo e Referência", "Mapa de Canais", "Piso", "Calendário 12 meses", "Datas de pico", "Resumo", "Checklist da revisão"], "oito abas na ordem do plano")
log(wbx["Piso"]["B8"].fill.fgColor.rgb.endswith("FFF4C7") and wbx["Piso"]["B7"].fill.fgColor.rgb.endswith("E3EEDF"), "amarelo preenche, verde calcula")
log("dados fictícios" in str(wbx["Comece aqui"]["A4"].value).lower() and "ponto de partida" in str(wbx["Calendário 12 meses"]["A2"].value or "") + str(wbx["Comece aqui"]["A18"].value), "exemplo rotulado; fatores como ponto de partida")
ck = wb["Checklist da revisão"]; log(ck["C15"].value == 6 and "Faltam 4" in str(ck["B16"].value), "checklist da revisão: 6 de 10 no exemplo")
textos = " ".join(str(c.value) for ws in wbx.worksheets for row in ws.iter_rows() for c in row if isinstance(c.value, str) and not c.value.startswith("="))
log(not re.search(r"garant|lucro certo|renda extra|valoriza", textos, re.I), "nenhuma promessa proibida nos textos")
log(not re.search(r"\b(ADR|RevPAR|OTA|PMS|KPI|DRE)\b", textos), "nenhuma sigla nos textos")
log("—" not in textos, "sem travessão nos textos")

print("Versão em branco e entradas inválidas")
wb = recalc(D / BR)
log(str(wb["Custo e Referência"]["B28"].value).startswith("Preencha") and wb["Calendário 12 meses"]["B34"].value in (None, "") and str(wb["Resumo"]["B15"].value).startswith("Confira"), "em branco: pede os dados, sem resultado")
w = cenario("ok", EX); log(w["Calendário 12 meses"]["B34"].value is not None and perto(w["Calendário 12 meses"]["B34"].value, 305.9178, 1e-4) and w["Resumo"]["B15"].value == "Venda direta sem motor de reservas", "em branco preenchida com o exemplo dá o mesmo resultado")
w = cenario("mix", dict(EX, canais=[EX["canais"][0], ("Plataforma B", 10, 15, 1.5, 0, "Não"), EX["canais"][2]])); log(w["Mapa de Canais"]["B24"].value == "O mix precisa somar 100%", "mix de 90% bloqueia")
w = cenario("neg", dict(EX, canais=[("Plataforma A", 50, -16, 1.5, 0, "Não")] + EX["canais"][1:])); log(w["Mapa de Canais"]["B24"].value == "Há valor negativo", "comissão negativa bloqueia")
w = cenario("custo", dict(EX, cpn=20)); log("não pode ser menor" in w["Custo e Referência"]["B28"].value, "custo por noite menor que o variável bloqueia")
w = cenario("pisoalto", dict(EX, piso=350)); log(w["Piso"]["B21"].value == "O piso não pode passar da referência", "piso acima da referência bloqueia")
w = cenario("semfaixa", dict(EX, meses=[EX["meses"][0]] * 11 + [(None, "Base")])); log("Escolha a faixa" in w["Calendário 12 meses"]["B36"].value, "mês sem faixa bloqueia")
w = cenario("ano", dict(EX, ano=1999)); log("2024 a 2099" in w["Calendário 12 meses"]["B36"].value, "ano fora do intervalo bloqueia")
w = cenario("semdireta", dict(EX, canais=[("Plataforma A", 70, 16, 1.5, 0, "Não"), ("Plataforma B", 30, 15, 1.5, 0, "Não")])); log("venda direta" in w["Mapa de Canais"]["B24"].value, "sem linha de venda direta: pede a linha")

print("Bordas e causa principal")
w = cenario("estrutura", dict(EX, ref=190, piso=180)); log(w["Resumo"]["B15"].value == "Referência abaixo do custo da noite", "referência abaixo do custo vem primeiro")
w = cenario("piso", dict(EX, piso=190)); log(w["Resumo"]["B15"].value == "Piso abaixo do custo da noite" and w["Piso"]["B20"].value.startswith("Piso abaixo do custo"), "piso abaixo do custo")
w = cenario("faixa", dict(EX, piso=240)); log(w["Calendário 12 meses"]["B35"].value == "Vale" and w["Resumo"]["B15"].value == "Faixa do calendário abaixo do piso", "piso 240: vale (225) abaixo do piso")
w = cenario("picobaixo", dict(EX, piso=240, meses=[("Baixa", "Base")] * 12, picos=[("Feriado", 3, 3, 0.7, 3, "")])); log(w["Calendário 12 meses"]["B35"].value == "Datas de pico" and w["Datas de pico"]["I5"].value == "abaixo do piso", "data de pico abaixo do piso aparece")
w = cenario("fixo", dict(EX, meses=[("Base", "Base")] * 12, picos=[])); log(w["Resumo"]["B14"].value == "Sim" and w["Resumo"]["B15"].value == "Preço fixo o ano inteiro", "preço fixo o ano inteiro")
w = cenario("picomin", dict(EX, picos=[("Réveillon", 12, 5, 2.4, 1, "")])); log(w["Resumo"]["B15"].value == "Datas de pico sem regra" and w["Datas de pico"]["I5"].value == "sem mínimo de noites", "pico com mínimo de 1 noite")
d0 = dict(EX, canais=[("Plataforma A", 70, 16, 1.5, 0, "Não"), ("Plataforma B", 30, 15, 1.5, 0, "Não"), ("Venda direta", 0, 0, 1.5, 0, "Sim")], gestor="Não")
w = cenario("dep", d0); log(w["Resumo"]["B15"].value == "Sem venda direta" and w["Mapa de Canais"]["B14"].value == 0, "venda direta 0%: sem venda direta")
w = cenario("over", dict(EX, gestor="Não")); log(w["Resumo"]["B15"].value == "Vários canais sem gestor de canais", "dois canais pagos sem gestor de canais")
w = cenario("cabeca", dict(EX, motor="Sim", quem=None)); log(w["Resumo"]["B15"].value == "Piso só na sua cabeça", "piso sem quem conheça")
w = cenario("dentro", dict(EX, motor="Sim")); log(w["Resumo"]["B15"].value == "Tabela dentro das regras da fonte", "nada dispara: dentro das regras")
dj = dict(EX, inicio=7); rj = conta(dj); w = cenario("julho", dj); c2 = w["Calendário 12 meses"]
log(c2["B33"].value == 366 == rj["total"] and perto(c2["B34"].value, rj["media"], 1e-6) and c2["A20"].value == "jan/2028", f"começando em julho de 2027: 366 noites (fev/2028 bissexto) e média {c2['B34'].value:.2f} = conta independente")
de = dict(EX, canais=[("Plataforma A", 100, 15, 0, 46.4, "Não"), ("Venda direta", 0, 0, 0, 0, "Sim")]); re_ = conta(de); w = cenario("extra", de)
log(perto(w["Mapa de Canais"]["H5"].value, re_["canais"][0]["liq"]) and perto(w["Piso"]["B5"].value, re_["pc"]) and perto(w["Piso"]["B5"].value, (153.04 + 20) / 0.79), "custo por reserva 46,40 ÷ 2,32 noites entra no líquido e no piso")
print(f"\n{ok} ok, {fal} falhou"); sys.exit(1 if fal else 0)

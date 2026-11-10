"""Testa a planilha Tarefas, Escala e Alçadas recalculando no LibreOffice e comparando com uma conta independente em Python.
Uso: python3 -I tests/test_planilha.py <pasta com os xlsx>"""
import sys, pathlib, subprocess, tempfile, datetime as dt
from openpyxl import load_workbook
D = pathlib.Path(sys.argv[1]); ok = fal = 0
BRANCO, EXEMPLO = "Tarefas-Escala-e-Alcadas-Zion-EM-BRANCO.xlsx", "Tarefas-Escala-e-Alcadas-Zion-EXEMPLO.xlsx"
def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)
def recalc(path):
    t = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(t), str(path)], check=True, capture_output=True, timeout=180)
    return load_workbook(t / path.name, data_only=True)
def cenario(nome, mud, base=BRANCO):
    wb = load_workbook(D / base)
    for (aba, cel), v in mud.items(): wb[aba][cel] = v
    x = pathlib.Path(tempfile.mkdtemp()) / ("t_" + nome + ".xlsx"); wb.save(x); return recalc(x)
def dia(v): return v.date() if isinstance(v, dt.datetime) else v

# ---- conta independente (não usa a planilha nem o logic.js) ----
ORDEM = ["Limpeza e preparação da unidade", "Check-in e check-out", "Resposta a mensagem dos hóspedes", "Manutenção e ronda técnica",
         "Compras, estoque e fornecedores", "Financeiro e administrativo", "Preço, calendário e canais", "Pedido e resposta de avaliações"]
SETOR = [["Limpeza e preparação da unidade"], ["Check-in e check-out", "Resposta a mensagem dos hóspedes"], ["Manutenção e ronda técnica"],
         ["Compras, estoque e fornecedores", "Financeiro e administrativo"], ["Preço, calendário e canais"], ["Pedido e resposta de avaliações"]]
def tarefas(lin):  # lin: lista de (resp, horas, julg)
    horas = [h or 0 for _, h, _ in lin]
    porj = {j: sum(h or 0 for _, h, jj in lin if jj == j) for j in ("Baixo", "Médio", "Alto")}
    cands = [(i, (h or 0), j) for i, (_, h, j) in enumerate(lin) if (h or 0) > 0 and j in ("Baixo", "Médio")]
    cands.sort(key=lambda c: (-(c[1] + (1000 if c[2] == "Baixo" else 0)), c[0]))
    dono = [1 if str(r or "").strip().lower() in ("eu", "eu mesma", "eu mesmo") else 0 for r, _, _ in lin]
    porNome = dict(zip(ORDEM, dono))
    setores = sum(1 for s in SETOR if all(porNome[a] for a in s))
    return dict(total=sum(horas), porj=porj, primeira=ORDEM[cands[0][0]] if cands else None, soDono=sum(dono), setores=setores)
EX_T = [("Diarista", 0, "Baixo"), ("Eu", 5, "Baixo"), ("Eu", 6, "Médio"), ("Auxiliar de manutenção", 1, "Médio"), ("Eu", 2, "Alto"), ("Eu", 2, "Alto"), ("Eu", 2, "Alto"), ("Eu", 2, "Médio")]

print("1. Exemplo preenchido (dados fictícios, PLANO seção 9)")
wb = recalc(D / EXEMPLO); t = wb["Tarefas"]; r = tarefas(EX_T)
log(t["B14"].value == "OK", "situação dos dados OK")
log(t["B16"].value == r["total"] == 20, f"total de horas da dona = {t['B16'].value} (ref 20, igual à Conta da Retirada do Módulo 2)")
log((t["B17"].value, t["B18"].value, t["B19"].value) == (r["porj"]["Baixo"], r["porj"]["Médio"], r["porj"]["Alto"]) == (5, 9, 6), "horas por julgamento 5 · 9 · 6")
log(t["B20"].value == r["primeira"] == "Check-in e check-out", f"primeira a delegar: {t['B20'].value}")
log(t["B21"].value == r["soDono"] == 6 and t["B22"].value == r["setores"] == 4, "6 atividades e 4 de 6 setores só da dona")
log([t.cell(l, 6).value for l in range(5, 13)] == ["Sim", "Sim", "Parcial, com modelos", "Parcial, com modelos"] + ["Não, fica com você por mais tempo"] * 3 + ["Parcial, com modelos"], "coluna 'entra na primeira contratação' pela regra de julgamento")
a = wb["Alçadas"]
log([a.cell(l, 7).value for l in range(5, 12)].count("Sim") == a["B15"].value == 6 and a["G11"].value == "Falta", "6 de 7 regras escritas; erro de calendário falta")
log(a["B16"].value == "OK" and a["B13"].value == 100 and a["B14"].value == 300 and a["E6"].value == 42, "alçada 100 → 300; cortesia 42 (15% da diária de 280)")
e = wb["Escala"]
esc = {"Eu": 1 + 7 + 7 + 2, "Diarista": 6, "Auxiliar de manutenção": 3}
log({e.cell(l, 1).value: e.cell(l, 2).value for l in range(12, 15)} == esc, f"turnos por pessoa: {esc}")
log([e.cell(l, 9).value for l in range(5, 9)] == [0, 0, 0, 2] and e["B18"].value == 2 and e["B19"].value == 0 and e["B20"].value.startswith("Há 2 turno(s)"), "2 turnos sem ninguém (manutenção no fim de semana) apontados")
p = wb["Plano 4 semanas"]; ini = dt.date(2026, 11, 16)
log(all(dia(p.cell(12 + k, 2).value) == ini + dt.timedelta(7 * k) and dia(p.cell(12 + k, 3).value) == ini + dt.timedelta(7 * k + 6) for k in range(4)), "quatro semanas: 16/11 a 13/12/2026")
log(dia(p["B16"].value) == dt.date(2026, 12, 13) and p["B8"].value == 100, "avaliação em 13/12/2026; alçada inicial puxada da aba Alçadas")
log(p["B21"].value.startswith("Responda") and p["B27"].value == 1 and p["B28"].value == "Antes da semana 1: faltam 2 de 3 itens", "avaliação pendente; 1 de 3 pré-requisitos; situação aponta o que falta")
pe = wb["Painel por exceção"]
def excecao(nota, fora, seg, gasto, prev, nmin=4.7, pct=10):
    return (nota is not None and nota < nmin) or (fora or 0) > 0 or (seg or 0) > 0 or ((prev or 0) > 0 and (gasto or 0) > prev * (1 + pct / 100))
EXP = [(4.9, 0, 0, 1200, 1200), (4.8, 0, 0, 1350, 1200), (4.6, 0, 0, 1100, 1200), (4.9, 0, 0, 1250, 1200)]
lei = [pe.cell(9 + k, 12).value for k in range(4)]
log(all(lei[k].startswith("EXCEÇÃO") == excecao(*EXP[k]) for k in range(4)) and pe["B22"].value == 2, "painel: semana 2 (gasto 12,5% acima) e semana 3 (nota 4,6 < 4,7) são exceção; 2 no total")
log(pe["L13"].value in (None, "") and pe["B23"].value == "OK" and pe["B6"].value == 100, "linhas vazias sem leitura; situação OK")

print("2. Versão em branco")
wb = recalc(D / BRANCO); t = wb["Tarefas"]
log(t["B14"].value.startswith("Preencha quem faz hoje") and t["B20"].value in (None, ""), "em branco: pede os responsáveis e não sugere atividade")
log([t.cell(l, 5).value for l in range(5, 13)] == ["Baixo", "Baixo", "Médio", "Médio", "Alto", "Alto", "Alto", "Médio"], "julgamento sugerido pela fonte já vem marcado (ajustável)")
log(wb["Alçadas"]["B16"].value == "Defina a alçada inicial em reais" and wb["Escala"]["B20"].value == "Preencha a escala", "alçadas e escala pedem preenchimento")
log(wb["Plano 4 semanas"]["B12"].value in (None, "") and wb["Plano 4 semanas"]["B28"].value.startswith("Preencha"), "plano sem data: sem datas calculadas")
log(wb["Painel por exceção"]["B23"].value.startswith("Defina a nota mínima"), "painel pede nota mínima e percentual")

print("3. Cenários (conta independente)")
def tar_mud(lin):
    m = {}
    for k, (resp, h, j) in enumerate(lin): m[("Tarefas", f"C{5+k}")] = resp; m[("Tarefas", f"D{5+k}")] = h; m[("Tarefas", f"E{5+k}")] = j
    return m
casos = {
    "limpeza16": [("Eu", 16, "Baixo"), ("Eu", 8, "Baixo"), ("Eu", 12, "Médio"), ("Eu", 0, "Médio"), ("Eu", 4, "Alto"), ("Eu", 6, "Alto"), ("Eu", 3, "Alto"), ("Eu", 0, "Médio")],
    "empate": [("Eu", 5, "Baixo"), ("Eu", 5, "Baixo"), ("Eu", 6, "Médio"), ("X", 1, "Médio"), ("Eu", 2, "Alto"), ("Eu", 2, "Alto"), ("Eu", 2, "Alto"), ("Eu", 2, "Médio")],
    "soMedio": [("Diarista", 0, "Baixo"), ("Eu", 0, "Baixo"), ("Eu", 6, "Médio"), ("X", 9, "Médio"), ("Eu", 30, "Alto"), ("Eu", 2, "Alto"), ("Eu", 2, "Alto"), ("eu mesma", 2, "Médio")],
    "tudoAlto": [("Eu", 3, "Alto")] * 8,
    "delegado": [("Ana", 4, "Baixo"), ("Ana", 4, "Baixo"), ("Bia", 3, "Médio"), ("Caio", 1, "Médio"), ("Eu", 2, "Alto"), ("Bia", 2, "Alto"), ("Eu", 2, "Alto"), ("Bia", 1, "Médio")],
}
for nome, lin in casos.items():
    w = cenario(nome, tar_mud(lin)); t = w["Tarefas"]; r = tarefas(lin)
    prim = r["primeira"] or "Nenhuma: comece pelos critérios e alçadas"
    log(t["B14"].value == "OK" and t["B16"].value == r["total"] and t["B20"].value == prim and t["B21"].value == r["soDono"] and t["B22"].value == r["setores"],
        f"{nome}: total {r['total']}, primeira '{prim}', só seus {r['soDono']}, setores {r['setores']} (planilha: {t['B16'].value}, '{t['B20'].value}', {t['B21'].value}, {t['B22'].value})")
w = cenario("negativa", tar_mud([("Eu", -1, "Baixo")] + EX_T[1:])); log(w["Tarefas"]["B14"].value == "Há hora negativa", "hora negativa bloqueia")
w = cenario("cento", tar_mud([("Eu", 120, "Baixo")] + EX_T[1:])); log(w["Tarefas"]["B14"].value.startswith("Mais de 100 horas"), "mais de 100 horas numa atividade bloqueia")
w = cenario("semjulg", {**tar_mud(EX_T), ("Tarefas", "E9"): None}); log(w["Tarefas"]["B14"].value.startswith("Marque o julgamento"), "julgamento em branco bloqueia")
# alçadas
base_alc = {("Alçadas", f"C{5+k}"): "Regra escrita com mais de dez letras" for k in range(5)}
w = cenario("alc_ok", {**base_alc, ("Alçadas", "B13"): 100}); log(w["Alçadas"]["B15"].value == 5 and w["Alçadas"]["B16"].value == "OK", "5 regras e alçada 100: OK")
w = cenario("alc_4", {**{k: v for k, v in list(base_alc.items())[:4]}, ("Alçadas", "B13"): 100}); log(w["Alçadas"]["B16"].value.startswith("Escreva a regra"), "4 regras: pede pelo menos 5")
w = cenario("alc_zero", {**base_alc, ("Alçadas", "B13"): 0}); log(w["Alçadas"]["B16"].value.startswith("A alçada inicial precisa"), "alçada inicial zero bloqueia")
w = cenario("alc_desce", {**base_alc, ("Alçadas", "B13"): 300, ("Alçadas", "B14"): 100}); log(w["Alçadas"]["B16"].value.startswith("Atenção: a alçada do segundo mês"), "segundo mês abaixo da inicial avisa")
w = cenario("alc_neg", {**base_alc, ("Alçadas", "B13"): 100, ("Alçadas", "E6"): -5}); log(w["Alçadas"]["B16"].value == "Há alçada negativa", "alçada negativa bloqueia")
w = cenario("alc_curta", {("Alçadas", "C5"): "realoca", ("Alçadas", "B13"): 100}); log(w["Alçadas"]["G5"].value == "Falta", "regra com menos de 10 caracteres não conta")
# escala
esc_full = {("Escala", f"{c}{l}"): "Ana" for l in range(5, 9) for c in "BCDEFGH"}
w = cenario("esc_ok", {**esc_full, ("Escala", "A12"): "Ana", ("Escala", "C12"): "Bia"}); e = w["Escala"]
log(e["B12"].value == 28 and e["B18"].value == 0 and e["B20"].value == "Escala completa", "escala completa: Ana com 28 turnos")
w = cenario("esc_sub", {**esc_full, ("Escala", "A12"): "Ana"}); log(w["Escala"]["B19"].value == 1 and w["Escala"]["B20"].value.startswith("Defina quem substitui"), "pessoa sem substituto apontada")
w = cenario("esc_buraco", {**esc_full, ("Escala", "D6"): None, ("Escala", "H8"): None, ("Escala", "A12"): "Ana", ("Escala", "C12"): "Bia"})
log(w["Escala"]["B18"].value == 2 and w["Escala"]["B12"].value == 26, "dois buracos: 2 turnos sem ninguém, Ana com 26")
# plano
ini = dt.date(2026, 12, 28)
w = cenario("plano", {("Plano 4 semanas", "B4"): "Check-in", ("Plano 4 semanas", "B5"): "Ana", ("Plano 4 semanas", "B7"): ini, ("Plano 4 semanas", "B9"): "Eu",
                      ("Plano 4 semanas", "B18"): "Sim", ("Plano 4 semanas", "B19"): "Sim", ("Plano 4 semanas", "B20"): "Sim",
                      ("Plano 4 semanas", "B24"): "Sim", ("Plano 4 semanas", "B25"): "Sim", ("Plano 4 semanas", "B26"): "Sim"}); p = w["Plano 4 semanas"]
log(dia(p["C15"].value) == ini + dt.timedelta(27) == dt.date(2027, 1, 24) and dia(p["B16"].value) == dt.date(2027, 1, 24), "semanas atravessam a virada do ano (avaliação em 24/01/2027)")
log(p["B21"].value.startswith("Operando") and p["B28"].value == "Pronto para começar", "três sim: operando; três pré-requisitos: pronto para começar")
w = cenario("plano_nao", {("Plano 4 semanas", "B18"): "Sim", ("Plano 4 semanas", "B19"): "Não", ("Plano 4 semanas", "B20"): "Sim"})
log(w["Plano 4 semanas"]["B21"].value.startswith("Repita a semana 3"), "um não: repita a semana 3")
# painel
pmud = {("Painel por exceção", "B4"): 4.5, ("Painel por exceção", "B5"): 5}
linhas = [(4.4, 0, 0, 100, 100), (4.8, 1, 0, 100, 100), (4.8, 0, 1, 100, 100), (4.8, 0, 0, 106, 100), (4.8, 0, 0, 105, 100), (None, 0, 0, 0, 0)]
for k, (nota, fora, seg, gasto, prev) in enumerate(linhas):
    l = 9 + k; pmud.update({("Painel por exceção", f"A{l}"): dt.date(2027, 1, 4) + dt.timedelta(7 * k), ("Painel por exceção", f"B{l}"): nota, ("Painel por exceção", f"H{l}"): fora,
                            ("Painel por exceção", f"I{l}"): seg, ("Painel por exceção", f"J{l}"): gasto, ("Painel por exceção", f"K{l}"): prev})
w = cenario("painel", pmud); pe = w["Painel por exceção"]
esp = [excecao(n, f, s, g, pv, 4.5, 5) for n, f, s, g, pv in linhas]
got = [pe.cell(9 + k, 12).value.startswith("EXCEÇÃO") for k in range(len(linhas))]
log(got == esp == [True, True, True, True, False, False] and pe["B22"].value == 4, "painel: nota baixa, decisão fora da alçada, segurança e gasto 6% acima são exceção; 5% exatos e semana sem nota não são")

print(f"\n{ok} ok, {fal} falhou"); sys.exit(1 if fal else 0)

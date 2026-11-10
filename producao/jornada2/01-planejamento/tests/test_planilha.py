"""Testa a planilha Painel de Gestão recalculando no LibreOffice e comparando com uma conta independente em Python.
Uso: python3 -I tests/test_planilha.py <pasta com os xlsx>"""
import sys, pathlib, subprocess, tempfile
from openpyxl import load_workbook
D = pathlib.Path(sys.argv[1]); ok = fal = 0
def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)
def recalc(path):
    t = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(t), str(path)], check=True, capture_output=True, timeout=180)
    return load_workbook(t / path.name, data_only=True)
def perto(a, b, tol=0.005): return isinstance(a, (int, float)) and abs(a - b) <= tol
BRANCO, EXEMPLO = "Painel-de-Gestao-Zion-EM-BRANCO.xlsx", "Painel-de-Gestao-Zion-EXEMPLO.xlsx"
def cenario(nome, celulas, base=BRANCO):
    wb = load_workbook(D / base)
    for aba, cel, v in celulas: wb[aba][cel] = v
    x = pathlib.Path(tempfile.mkdtemp()) / ("t_" + nome + ".xlsx"); wb.save(x); return recalc(x)

# ---- conta independente (não usa a planilha nem o logic.js) ----
def leitura(base, meta):
    if meta is None: return "Falta a meta"
    if base is None: return "Sem ponto de partida: o primeiro mês do painel vira a base"
    if meta > base: return "Meta acima do ponto de partida"
    if meta == base: return "Manter: válido, desde que escrito"
    return "Meta abaixo do ponto de partida: escreva o porquê"
def compara(real, ant):
    if real is None or ant is None: return None
    return "Melhorou" if real > ant else "Igual" if real == ant else "Piorou"
M = "Metas e donos"
BASE = [46.8, 280, 11890, 4.7, 12]; META = [50, 300, 13000, 4.8, 20]
def preenche(base=BASE, meta=META, dono=("Ana",) * 5, dias=31, un=4, escala=5, extra=()):
    c = [(M, "B4", "Outubro de 2026"), (M, "B5", dias), (M, "B6", un), (M, "B8", escala)]
    for k in range(5):
        l = 12 + k
        if base[k] is not None: c.append((M, f"C{l}", base[k]))
        if meta[k] is not None: c.append((M, f"D{l}", meta[k]))
        if dono[k] is not None: c.append((M, f"E{l}", dono[k]))
    return c + list(extra)

print("Exemplo preenchido (dados fictícios, PLANO seção 9)")
wb = recalc(D / EXEMPLO); m = wb[M]
log(m["B27"].value == "OK", f"situação dos dados OK ({m['B27'].value})")
log(m["B7"].value == 124, f"noites disponíveis = {m['B7'].value} (31 × 4)")
var = [META[k] - BASE[k] for k in range(5)]
log(all(perto(m[f"F{12+k}"].value, var[k], 1e-6) for k in range(5)), "variações batem: " + ", ".join(f"{m[f'F{12+k}'].value:.1f}" for k in range(5)))
log(all(m[f"G{12+k}"].value == leitura(BASE[k], META[k]) for k in range(5)), "leituras: cinco metas acima do ponto de partida")
noites = META[0] / 100 * 124; receita = noites * META[1]; varrec = (META[0] * META[1]) / (BASE[0] * BASE[1]) - 1
log(perto(m["B19"].value, noites) and perto(noites, 62), f"noites que a meta pede = {m['B19'].value} (ref 62)")
log(perto(m["B20"].value, receita) and perto(receita, 18600), f"receita de hospedagem que as metas pedem = {m['B20'].value:.2f} (ref 18.600)")
log(perto(m["B21"].value, varrec, 1e-6) and round(varrec * 100, 1) == 14.5, f"variação da receita por noite disponível = {m['B21'].value:.4f} (ref 14,5%)")
log(m["B24"].value.startswith("Sem ocupação de equilíbrio") and m["B25"].value.startswith("Sem número de corte"), "conferências sem dados do Módulo 2")
log(all(m[f"I{12+k}"].value in (None, "") for k in range(5)), "meta atingida em branco antes do mês de chegada")
p = wb["Painel 12 meses"]
ex_out = (["Melhorou"] * 5, ["Piorou", "Melhorou", "Piorou", "Melhorou", "Melhorou"])
real = ([46.8, 280, 11890, 4.7, 12], [38.3, 285, 8950, 4.8, 14]); ant = ([41.9, 265, 10400, 4.6, 8], [40.0, 270, 9300, 4.6, 9])
for i in range(2):
    esperado = [compara(real[i][k], ant[i][k]) for k in range(5)]
    obtido = [p.cell(5 + i, 12 + k).value for k in range(5)]
    log(obtido == esperado == ex_out[i] and p.cell(5 + i, 17).value == esperado.count("Melhorou"), f"mês {i+1} do painel: {obtido}, {p.cell(5+i,17).value} melhoraram")
log(p["L7"].value in (None, "") and p["Q7"].value in (None, ""), "linhas vazias do painel ficam em branco")
r = wb["Reunião semanal"]
log(r["B21"].value == 2 and r["B22"].value == "Faltam 2 para o critério das quatro semanas", f"reunião: {r['B21'].value} registradas · {r['B22'].value}")
s = wb["Plano 6 semanas"]
log(s["B12"].value == "1 de 3" and s["B13"].value == "OK: três pilares diferentes", f"plano: {s['B12'].value}, {s['B13'].value}")

print("Versão em branco")
wb = recalc(D / BRANCO); m = wb[M]
log(m["B27"].value == "Preencha o mês, os dias e as unidades", "em branco pede o mês, os dias e as unidades")
log(all(m[f"G{12+k}"].value == "Falta a meta" for k in range(5)) and m["B19"].value in (None, "") and m["B20"].value in (None, ""), "em branco: falta a meta, sem contas")
log(wb["Reunião semanal"]["B22"].value == "Nenhuma reunião registrada ainda" and wb["Plano 6 semanas"]["B13"].value == "Escolha os três pilares", "reunião e plano vazios")
log(wb["Painel 12 meses"]["Q5"].value in (None, ""), "painel vazio")

print("Cenários de bloqueio e de leitura (recalculados no LibreOffice)")
casos = [
    ("dias32", preenche(dias=32), "Dias do mês: use 28 a 31"),
    ("unidades0", preenche(un=0), "Unidades: número inteiro a partir de 1"),
    ("escala7", preenche(escala=7), "Escala da nota: 5 ou 10"),
    ("semmeta", preenche(meta=[50, 300, None, 4.8, 20]), "Falta meta em algum indicador"),
    ("semdono", preenche(dono=("Ana", "Ana", "Ana", None, "Ana")), "Falta o dono de algum indicador"),
    ("ocup120", preenche(meta=[120, 300, 13000, 4.8, 20]), "Ocupação e venda direta: de 0 a 100"),
    ("vdneg", preenche(base=[46.8, 280, 11890, 4.7, -1]), "Ocupação e venda direta: de 0 a 100"),
    ("diaria0", preenche(meta=[50, 0, 13000, 4.8, 20]), "Diária não pode ser negativa; metas de ocupação e diária maiores que zero"),
    ("nota6", preenche(meta=[50, 300, 13000, 6, 20]), "Nota fora da escala"),
    ("nota10", preenche(base=[46.8, 280, 11890, 9.2, 12], meta=[50, 300, 13000, 9.4, 20], escala=10), "OK"),
    ("resultadoNeg", preenche(base=[46.8, 280, -2500, 4.7, 12], meta=[50, 300, -500, 4.8, 20]), "OK"),
]
for nome, cel, esperado in casos:
    w = cenario(nome, cel); v = w[M]["B27"].value
    log(v == esperado, f"{nome}: situação = {v!r}")
w = cenario("semBase", preenche(base=[None, None, 11890, None, 12])); mm = w[M]
log(mm["B27"].value == "OK" and mm["G12"].value == leitura(None, 50) and mm["F12"].value in (None, "") and mm["B21"].value in (None, "") and perto(mm["B20"].value, 18600), "sem ponto de partida: aceita, leitura própria, sem variação e com a receita pedida")
w = cenario("abaixoIgual", preenche(meta=[40, 280, 13000, 4.8, 20])); mm = w[M]
log(mm["G12"].value == leitura(46.8, 40) and mm["G13"].value == leitura(280, 280) and perto(mm["F12"].value, -6.8) and mm["F13"].value == 0, "meta abaixo e meta igual ao ponto de partida")
log(perto(mm["B21"].value, (40 * 280) / (46.8 * 280) - 1, 1e-6), f"variação negativa da receita por noite disponível = {mm['B21'].value:.4f}")
w = cenario("conferencias", preenche(extra=[(M, "B22", 55), (M, "B23", 15000)])); mm = w[M]
log(mm["B24"].value == "Atenção: a meta de ocupação não paga o custo fixo" and mm["B25"].value == "Atenção: a meta de resultado fica abaixo do corte", "meta abaixo do equilíbrio (55%) e do corte (R$ 15.000) alertam")
w = cenario("conferenciasOk", preenche(extra=[(M, "B22", 28.5), (M, "B23", 2000)])); mm = w[M]
log(mm["B24"].value.startswith("OK") and mm["B25"].value.startswith("OK"), "equilíbrio 28,5% e corte R$ 2.000: OK")
w = cenario("chegada", preenche(extra=[(M, "H12", 51.2), (M, "H13", 295), (M, "H16", 20)])); mm = w[M]
log(mm["I12"].value == "Sim" and mm["I13"].value == "Ainda não" and mm["I16"].value == "Sim" and mm["I14"].value in (None, ""), "mês de chegada: meta atingida (≥) ou ainda não")
pc = [("Painel 12 meses", "A5", "Dez"), ("Painel 12 meses", "B5", 50), ("Painel 12 meses", "G5", 50), ("Painel 12 meses", "C5", 250), ("Painel 12 meses", "H5", 300)]
w = cenario("painel", pc); pp = w["Painel 12 meses"]
log(pp["L5"].value == "Igual" and pp["M5"].value == "Piorou" and pp["N5"].value in (None, "") and pp["Q5"].value == 0, "painel: igual, piorou e sem comparação quando falta o ano anterior")
rc = [("Reunião semanal", f"A{7+i}", f"{i+1:02d}/12/2026") for i in range(5)]
w = cenario("reunioes", rc)
log(w["Reunião semanal"]["B21"].value == 5 and w["Reunião semanal"]["B22"].value.startswith("Rotina viva: 5"), "cinco reuniões: rotina viva")
w = cenario("plano", [("Plano 6 semanas", "B4", "Módulo 2"), ("Plano 6 semanas", "B5", "Módulo 2"), ("Plano 6 semanas", "B6", "Módulo 4"), ("Plano 6 semanas", "E4", "Sim"), ("Plano 6 semanas", "E5", "Sim")])
log(w["Plano 6 semanas"]["B13"].value == "Escolha três pilares diferentes" and w["Plano 6 semanas"]["B12"].value == "2 de 3", "plano: pilar repetido e dois feitos")

print(f"\n{ok} ok, {fal} falhou"); sys.exit(1 if fal else 0)

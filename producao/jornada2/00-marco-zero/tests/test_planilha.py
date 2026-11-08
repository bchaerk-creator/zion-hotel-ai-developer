"""Testa a planilha Painel do Mês recalculando no LibreOffice e comparando com uma conta independente.
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
def cenario(nome, valores, base="Painel-do-Mes-Zion-EM-BRANCO.xlsx"):
    wb = load_workbook(D / base); p = wb["Painel"]
    for cel, v in valores.items(): p[cel] = v
    f = pathlib.Path(tempfile.mkdtemp()) / ("t_" + nome + ".xlsx"); wb.save(f); return recalc(f)

print("Exemplo preenchido (dados fictícios)")
wb = recalc(D / "Painel-do-Mes-Zion-EXEMPLO.xlsx"); p = wb["Painel"]; h = wb["Histórico"]; r = wb["Rotina"]
un, dias, noites, rec, outras = 4, 31, 58, 16240, 980
saidas = [1800, 540, 620, 380, 250, 1040, 150, 460, 90]
disp, entrou, saiu = un * dias, rec + outras, sum(saidas)
log(p["B26"].value == "OK", "situação OK")
log(p["B27"].value == disp, f"noites disponíveis = {p['B27'].value} (ref {disp})")
log(abs(p["B28"].value - entrou) < 0.01, f"quanto entrou = {p['B28'].value:.2f} (ref {entrou})")
log(abs(p["B29"].value - saiu) < 0.01, f"total que saiu = {p['B29'].value:.2f} (ref {saiu})")
log(abs(p["B30"].value - (entrou - saiu)) < 0.01, f"quanto sobrou = {p['B30'].value:.2f} (ref {entrou - saiu})")
log(abs(p["B31"].value - (entrou - saiu) / entrou) < 1e-6, f"margem = {p['B31'].value:.1%}")
log(abs(p["B32"].value - noites / disp) < 1e-6, f"ocupação = {p['B32'].value:.1%} (ref {noites/disp:.1%})")
log(abs(p["B33"].value - rec / noites) < 0.01, f"diária média = {p['B33'].value:.2f} (ref {rec/noites:.2f})")
log(abs(p["B34"].value - rec / disp) < 0.01, f"receita por noite disponível = {p['B34'].value:.2f} (ref {rec/disp:.2f})")
log(abs(p["B35"].value - saiu / noites) < 0.01, f"custo por noite vendida = {p['B35'].value:.2f} (ref {saiu/noites:.2f})")
log(isinstance(p["B36"].value, str) and "ainda sobra" in p["B36"].value, "leitura: diária média acima do custo por noite")
log(h["F5"].value == 17220 - 5330 and abs(h["G5"].value - 58 / 124) < 1e-6 and abs(h["H5"].value - 17220 / 58) < 0.01, "histórico: linha de outubro calcula sobra, ocupação e diária média")
log(h["F10"].value in (None, ""), "histórico: linha vazia fica vazia")
log(r["C16"].value == 4, f"rotina: {r['C16'].value} itens marcados como Sim no exemplo")

print("Versão em branco e entradas inválidas")
wb = recalc(D / "Painel-do-Mes-Zion-EM-BRANCO.xlsx"); p = wb["Painel"]
log(str(p["B26"].value).startswith("Preencha") and p["B28"].value in (None, ""), "em branco: pede preenchimento, sem resultado")
base = dict(B6=2, B7=30, B8=20, B11=6000, B12=0, **{f"B{l}": 0 for l in range(15, 24)})
p = cenario("ok", base)["Painel"]; log(p["B26"].value == "OK" and abs(p["B33"].value - 300) < 0.01 and p["B35"].value == 0, "cenário simples: diária média 300, custo 0")
p = cenario("neg", {**base, "B15": -10})["Painel"]; log(p["B26"].value == "Há valor negativo", "valor negativo bloqueia")
p = cenario("zero", {**base, "B6": 0})["Painel"]; log("maiores que zero" in p["B26"].value, "unidades zero bloqueia")
p = cenario("excesso", {**base, "B8": 61})["Painel"]; log("passam das noites" in p["B26"].value, "noites vendidas acima das disponíveis bloqueia")
p = cenario("semnoite", {**base, "B8": 0, "B11": 0, "B15": 500})["Painel"]; log(p["B26"].value == "OK" and "prejuízo" in p["B36"].value and p["B33"].value == 0, "zero noites: sem divisão por zero e leitura de prejuízo")
p = cenario("empate", {**base, "B8": 10, "B11": 3000, "B15": 3000})["Painel"]; log("empata" in p["B36"].value, "diária média igual ao custo: empata")
p = cenario("abaixo", {**base, "B8": 10, "B11": 2000, "B15": 3000})["Painel"]; log("custa mais" in p["B36"].value and p["B30"].value == -1000, "diária abaixo do custo: alerta e sobra negativa")
print(f"\n{ok} ok, {fal} falhou"); sys.exit(1 if fal else 0)

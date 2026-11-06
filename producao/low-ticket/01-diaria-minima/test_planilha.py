"""Testa as fórmulas recalculando no LibreOffice. Uso: python3 -I test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, shutil
from openpyxl import load_workbook
D = pathlib.Path(sys.argv[1]); ok = fal = 0
def log(b, m):
    global ok, fal; ok += b; fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)
def recalc(path):
    t = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(t), str(path)], check=True, capture_output=True, timeout=120)
    return load_workbook(t / path.name, data_only=True)
def cenario(nome, valores, base="Diaria-Minima-Zion-EM-BRANCO.xlsx"):
    wb = load_workbook(D / base); c = wb["Calculadora"]
    for cel, v in valores.items(): c[cel] = v
    p = pathlib.Path(tempfile.mkdtemp()) / ("t_" + nome + ".xlsx"); wb.save(p); return recalc(p)
def ref(f, l, lc, v, tx, im, n, e, meta):
    k = 1 - (tx + im) / 100; res = n / e
    return (f + meta + res * l + n * v - res * lc * k) / (n * k)

print("Exemplo preenchido")
wb = recalc(D / "Diaria-Minima-Zion-EXEMPLO.xlsx"); c = wb["Calculadora"]; s = wb["Resumo do mês"]; r = wb["Reservas"]
log(c["B16"].value == "OK", "situação OK")
emp, meta = ref(1850, 120, 90, 38, 16, 6, 14, 2.5, 0), ref(1850, 120, 90, 38, 16, 6, 14, 2.5, 2500)
log(abs(c["B19"].value - emp) < 0.01, f"diária mínima = {c['B19'].value:.2f} (referência {emp:.2f})")
log(abs(c["B20"].value - meta) < 0.01, f"diária da meta = {c['B20'].value:.2f} (referência {meta:.2f})")
log(abs(c["B30"].value - 2500) < 0.01 and c["B31"].value == "Confere com a meta", "memória do cálculo fecha na meta (R$ 2.500)")
k = 1 - 0.22; m0 = 420 * k - 38 - (120 - 90 * k) / 2.5; m1 = 420 * 0.85 * k - 38 - (120 - 90 * k) / 2.5
log(abs(c["B36"].value - m0) < 0.01 and abs(c["B39"].value - 14 * m0 / m1) < 0.01, f"desconto de 15%: {c['B39'].value:.1f} noites para manter a margem (referência {14*m0/m1:.1f})")
log(r["L3"].value is not None and abs(r["L3"].value - (1260 + 90 - 1350 * 0.16 - 1350 * 0.06 - 120 - 3 * 38)) < 0.01, f"margem da 1ª reserva = {r['L3'].value:.2f}")
log(abs(r["I6"].value) < 0.001, "canal direto: taxa 0")
log(s["B9"].value == 6 and s["B10"].value == 16, "resumo: 6 reservas, 16 noites")
log(abs(s["B11"].value - 16 / 28) < 1e-6, f"ocupação = {s['B11'].value:.1%}")
soma_margem = sum(r.cell(l, 12).value for l in range(3, 9))
log(abs(s["B16"].value - (soma_margem - 1850)) < 0.01, f"sobra no mês = {s['B16'].value:.2f} (margens − fixos)")
log(isinstance(s["B17"].value, str) and "mínima" in s["B17"].value, "compara diária efetiva com a mínima: " + str(s["B17"].value))

print("Versão em branco e entradas inválidas")
wb = recalc(D / "Diaria-Minima-Zion-EM-BRANCO.xlsx"); c = wb["Calculadora"]
log(c["B16"].value == "Preencha todas as células amarelas" and c["B19"].value in (None, ""), "em branco: pede preenchimento, sem resultado")
log(wb["Resumo do mês"]["B16"].value in (None, ""), "resumo em branco fica vazio")
base = dict(B5=1000, B6=100, B7=0, B8=30, B9=16, B10=0, B11=10, B12=2, B13=0)
t = cenario("taxas100", {**base, "B9": 60, "B10": 40})["Calculadora"]; log("100%" in t["B16"].value and t["B19"].value in (None, ""), "taxa + impostos = 100%: bloqueado")
t = cenario("zero", {**base, "B11": 0})["Calculadora"]; log("maiores que zero" in t["B16"].value, "0 noites: sem divisão por zero")
t = cenario("estadia", {**base, "B12": 12})["Calculadora"]; log("Estadia média maior" in t["B16"].value, "estadia maior que as noites do mês: bloqueado")
t = cenario("neg", {**base, "B5": -10})["Calculadora"]; log("negativo" in t["B16"].value, "valor negativo: bloqueado")
t = cenario("32", {**base, "B11": 32})["Calculadora"]; log("31" in t["B16"].value, "mais de 31 noites: bloqueado")
t = cenario("ok", base)["Calculadora"]; r0 = ref(1000, 100, 0, 30, 16, 0, 10, 2, 0)
log(t["B16"].value == "OK" and abs(t["B19"].value - r0) < 0.01, f"cenário simples: diária mínima {t['B19'].value:.2f} (referência {r0:.2f})")
t = cenario("descneg", {**base, "B34": 200, "B35": 80})["Calculadora"]; log(t["B39"].value == "Com esse desconto cada noite dá prejuízo", "desconto que zera a margem é avisado")
t = cenario("descsem", {**base, "B34": 200})["Calculadora"]; log(t["B39"].value in (None, ""), "simulador vazio sem o desconto")
print(f"\n{ok} passaram, {fal} falharam"); sys.exit(1 if fal else 0)

"""Testa a Ferramenta 29 recalculando no LibreOffice e comparando com uma conta independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, math, random
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from dados import EX, EX_FIXOS, EX_VAR
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EXF = D / "Custos-Experiencias-Zion-EM-BRANCO.xlsx", D / "Custos-Experiencias-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
F0, V0, R0 = 13, 13, 31

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)

def conta(p, taxa, imp, cap, n, fixos, var):
    """Conta independente. Devolve dict com situação e resultados (None quando bloqueado)."""
    fx, cv = sum(fixos), sum(var)
    if not isinstance(p, (int, float)) or p <= 0: return dict(sit="Informe o preço por participante")
    if not isinstance(n, (int, float)) or n < 1: return dict(sit="Informe os participantes previstos (1 ou mais)")
    t = (taxa or 0) + (imp or 0)
    if t >= 100: return dict(sit="Taxa e impostos precisam somar menos de 100%")
    if (taxa or 0) < 0 or (imp or 0) < 0 or fx < 0 or cv < 0: return dict(sit="Há valor negativo: confira")
    if cap is not None and n > cap: return dict(sit="Participantes acima da capacidade informada")
    k = 1 - t / 100; rec = p * n; tx = rec * (1 - k); contrib = rec - tx - cv * n - fx; unit = p * k - cv
    minimo = "O preço não cobre o custo por participante" if unit <= 0 else (1 if fx == 0 else math.ceil(fx / unit - 1e-12))
    cabe = "" if not isinstance(minimo, int) else ("Informe a capacidade" if cap is None else ("Sim" if minimo <= cap else "Não: nem com a capacidade cheia"))
    leitura = "Não cobre os custos desta sessão" if round(contrib, 2) < 0 else ("Empata: não sobra nada" if round(contrib, 2) == 0 else "Cobre os custos e sobra a contribuição acima")
    return dict(sit="OK", rec=rec, tx=tx, var=cv * n, fx=fx, contrib=contrib, porp=contrib / n, leitura=leitura, unit=unit, minimo=minimo, cabe=cabe, pmin=(fx / n + cv) / k)

def cenario(nome, p, taxa, imp, cap, n, fixos, var):
    wb = load_workbook(BR); c = wb["Calculadora"]
    for cel, v in (("B5", p), ("B6", taxa), ("B7", imp), ("B8", cap), ("B9", n)): c[cel] = v
    for i, v in enumerate(fixos): c[f"B{F0+i}"] = v
    for i, v in enumerate(var): c[f"E{V0+i}"] = v
    pth = TMP / f"{nome}.xlsx"; wb.save(pth); cen[nome] = (pth, (p, taxa, imp, cap, n, fixos, var))

random.seed(29)
for k in range(10):
    cenario(f"aleatorio_{k}", random.choice([random.randint(20, 400), random.uniform(10, 300)]), random.choice([None, 0, 3.5, 10]), random.choice([None, 0, 6, 16.33]),
            random.choice([None, random.randint(2, 30)]), random.randint(1, 25), [random.randint(0, 400) for _ in range(random.randint(0, 5))],
            [round(random.uniform(0, 120), 2) for _ in range(random.randint(0, 5))])
cenario("sem_preco", None, 5, 6, 10, 4, [100], [10])
cenario("taxa_100", 100, 60, 40, 10, 4, [100], [10])
cenario("acima_capacidade", 100, 5, 6, 6, 8, [100], [10])
cenario("preco_nao_cobre", 50, 10, 0, 20, 5, [100], [60])
cenario("sem_custo_fixo", 80, 0, 0, None, 3, [], [20])
cenario("negativo", 100, 5, 6, 10, 4, [-50], [10])
cenario("nao_cabe", 60, 0, 0, 5, 5, [1000], [10])

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EXF), str(BR)]
               + [str(c[0]) for c in cen.values()], check=True, capture_output=True, timeout=600)
R = {n: load_workbook(OUTD / c[0].name, data_only=True) for n, c in cen.items()}
R["exemplo"] = load_workbook(OUTD / EXF.name, data_only=True); R["branco"] = load_workbook(OUTD / BR.name, data_only=True)
cen["exemplo"] = (EXF, (EX["preco"], EX["taxa"], EX["imposto"], EX["capacidade"], EX["previstos"], [v for _, v in EX_FIXOS], [v for _, v in EX_VAR]))
CEL = dict(rec=R0 + 1, tx=R0 + 2, var=R0 + 3, fx=R0 + 4, contrib=R0 + 5, porp=R0 + 6, leitura=R0 + 7, unit=R0 + 9, minimo=R0 + 10, cabe=R0 + 11, pmin=R0 + 12)

def igual(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)): return abs(a - b) < 1e-6
    return a == b or (a in ("", None) and b in ("", None))

for nome in ["exemplo"] + [n for n in cen if n != "exemplo"]:
    args = cen[nome][1]; ref = conta(*args); c = R[nome]["Calculadora"]; s = R[nome]["Cenários"]; erros = []
    if c[f"B{R0}"].value != ref["sit"]: erros.append(("sit", ref["sit"], c[f"B{R0}"].value))
    if ref["sit"] == "OK":
        for k, l in CEL.items():
            if not igual(ref[k], c[f"B{l}"].value): erros.append((k, ref[k], c[f"B{l}"].value))
    p, taxa, imp, cap, n, fixos, var = args
    valido = isinstance(p, (int, float)) and p > 0 and (taxa or 0) + (imp or 0) < 100
    for i in range(40):
        nn = i + 1; esperado = valido and (cap is None or nn <= cap); got = s[f"A{5+i}"].value
        if bool(esperado) != (got not in ("", None)): erros.append(("cenario", nn, got)); break
        if esperado:
            kk = 1 - ((taxa or 0) + (imp or 0)) / 100; contrib = p * nn - p * nn * (1 - kk) - sum(var) * nn - sum(fixos)
            if not igual(contrib, s[f"F{5+i}"].value): erros.append(("contrib_cenario", nn, contrib, s[f"F{5+i}"].value)); break
    log(not erros, f"{nome}: {ref['sit']}" + (f" | {erros[:3]}" if erros else ""))

c = R["exemplo"]["Calculadora"]
log(abs(c[f"B{R0+5}"].value - 31.6) < 1e-6 and c[f"B{R0+10}"].value == 8 and abs(c[f"B{R0+12}"].value - 175.5617977528) < 1e-6,
    f"exemplo conferido à mão: contribuição R$ {c[f'B{R0+5}'].value:.2f} (31,60), mínimo {c[f'B{R0+10}'].value} participantes (8), preço mínimo R$ {c[f'B{R0+12}'].value:.2f} (175,56)")
s = R["exemplo"]["Cenários"]
log([s[f"G{5+i}"].value for i in (6, 7)] == ["Não cobre", "Cobre"] and s["A17"].value in ("", None) and s["A16"].value == 12,
    "cenários do exemplo: 7 participantes não cobre, 8 cobre; tabela para na capacidade (12)")
log(R["branco"]["Calculadora"][f"B{R0}"].value == "Informe o preço por participante", "versão em branco pede o preço, sem erro")
erros = [(n, ws.title, cc.coordinate) for n, wb in R.items() for ws in wb for row in ws.iter_rows() for cc in row
         if isinstance(cc.value, str) and cc.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(R)} arquivos" + (f" {erros[:4]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

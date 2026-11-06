"""Testa a Ferramenta 13 recalculando no LibreOffice e comparando com uma conta independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, datetime, random
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from itens import PADRAO, EX_ITENS, EX_MOV, EX_CONTAGEM
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EX = D / "Controle-Enxoval-Zion-EM-BRANCO.xlsx", D / "Controle-Enxoval-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
I0, M0, S0 = 6, 6, 7

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)

def referencia(itens, movs, contagem):
    """itens: lista de (item, d, e, f, manual, custo); movs: (item, tipo, qtd). Devolve dict item -> resultado."""
    cad = {x[0] for x in itens}
    def valido(it, tp, q): return it in cad and tp in ("Entrada", "Saída") and isinstance(q, (int, float)) and not isinstance(q, bool) and q > 0
    res = {}
    for nome, d, e, f, man, custo in itens:
        ent = sum(q for it, tp, q in movs if it == nome and tp == "Entrada" and valido(it, tp, q))
        sai = sum(q for it, tp, q in movs if it == nome and tp == "Saída" and valido(it, tp, q))
        saldo = ent - sai
        if man is not None: minimo = man
        elif all(isinstance(x, (int, float)) and x > 0 for x in (d, e, f)): minimo = d * e * f
        else: minimo = None
        comprar = None if minimo is None else max(0, minimo - saldo)
        if saldo < 0: sit = "Confira: saídas maiores que entradas"
        elif minimo is None: sit = "Defina o mínimo"
        elif saldo < minimo: sit = "COMPRAR"
        elif saldo == minimo: sit = "No mínimo"
        else: sit = "OK"
        custo_est = comprar * custo if comprar and custo is not None else None
        dif = contagem[nome] - saldo if nome in contagem else None
        res[nome] = dict(ent=ent, sai=sai, saldo=saldo, minimo=minimo, comprar=comprar, sit=sit, custo=custo_est, dif=dif)
    problemas = sum(1 for it, tp, q in movs if (it or q is not None) and not valido(it, tp, q))
    return res, problemas

def cenario(nome, itens, movs, contagem):
    wb = load_workbook(BR); it, mv, s = wb["Itens"], wb["Movimentos"], wb["Saldo"]
    for i in range(100):
        for col in "ABCDEFGHI":
            if col != "G": it[f"{col}{I0+i}"].value = None
    for i, (n, d, e, f, man, custo) in enumerate(itens):
        r = I0 + i; it[f"A{r}"], it[f"B{r}"], it[f"C{r}"] = "Enxoval", n, "peça"
        it[f"D{r}"], it[f"E{r}"], it[f"F{r}"], it[f"H{r}"], it[f"I{r}"] = d, e, f, man, custo
    for k, (n, tp, q) in enumerate(movs):
        r = M0 + k; mv[f"A{r}"], mv[f"B{r}"], mv[f"C{r}"], mv[f"D{r}"] = datetime.date(2026, 11, 6), n, tp, q
    for i, (n, *_ ) in enumerate(itens):
        if n in contagem: s[f"K{S0+i}"] = contagem[n]
    p = TMP / f"{nome}.xlsx"; wb.save(p); cen[nome] = (p, itens, movs, contagem)

# exemplo como lista de itens
EXI = [(n, *EX_ITENS[n]) for _, n, _ in PADRAO]
EXM = [(it, tp, q) for _, it, tp, q, _, _ in EX_MOV]
random.seed(13)
for k in range(6):
    itens = []
    for i in range(random.randint(3, 9)):
        if random.random() < .5: itens.append((f"Item {k}-{i}", random.randint(1, 3), random.randint(1, 6), random.randint(1, 4), None, random.choice([None, 10, 25.5])))
        else: itens.append((f"Item {k}-{i}", None, None, None, random.randint(0, 30), random.choice([None, 3.2])))
    nomes = [x[0] for x in itens] + ["Fora do cadastro"]
    movs = [(random.choice(nomes), random.choice(["Entrada", "Entrada", "Saída", None]), random.choice([random.randint(1, 20), random.randint(1, 20), 0, -3, "dez"]))
            for _ in range(random.randint(5, 40))]
    cont = {x[0]: random.randint(0, 30) for x in itens if random.random() < .3}
    cenario(f"aleatorio_{k}", itens, movs, cont)
cenario("saida_maior", [("Lençol", 1, 2, 3, None, 100)], [("Lençol", "Entrada", 2), ("Lençol", "Saída", 5)], {})
cenario("sem_minimo", [("Manta", None, None, None, None, None)], [("Manta", "Entrada", 3)], {})
cenario("minimo_manual_vence", [("Toalha", 2, 2, 2, 5, 10)], [("Toalha", "Entrada", 5)], {})

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EX), str(BR)]
               + [str(c[0]) for c in cen.values()], check=True, capture_output=True, timeout=600)
R = {n: load_workbook(OUTD / c[0].name, data_only=True) for n, c in cen.items()}
R["exemplo"] = load_workbook(OUTD / EX.name, data_only=True); R["branco"] = load_workbook(OUTD / BR.name, data_only=True)
cen["exemplo"] = (EX, EXI, EXM, EX_CONTAGEM)

def confere(nome):
    _, itens, movs, cont = cen[nome]; ref, prob = referencia(itens, movs, cont); s = R[nome]["Saldo"]; erros = []
    for i, (n, *_ ) in enumerate(itens):
        r = S0 + i; g = lambda c: s[f"{c}{r}"].value
        e = ref[n]
        got = dict(ent=g("D"), sai=g("E"), saldo=g("F"), minimo=g("G") if g("G") != "" else None, comprar=g("H") if g("H") != "" else None,
                   sit=g("I"), custo=g("J") if g("J") not in ("", None) else None, dif=g("L") if g("L") not in ("", None) else None)
        for k in e:
            a, b = e[k], got[k]
            if isinstance(a, (int, float)) and isinstance(b, (int, float)): igual = abs(a - b) < 1e-6
            else: igual = (a == b) or (a is None and b in (None, ""))
            if not igual: erros.append((n, k, a, b))
    p_ok = R[nome]["Movimentos"]["C3"].value == prob
    return erros, p_ok, ref, prob

for nome in ["exemplo"] + [n for n in cen if n != "exemplo"]:
    erros, p_ok, ref, prob = confere(nome)
    log(not erros and p_ok, f"{nome}: {len(ref)} itens conferidos, {prob} lançamento(s) com problema" + (f" | diferenças: {erros[:3]}" if erros else "") + ("" if p_ok else " | contagem de problemas difere"))

s = R["exemplo"]["Saldo"]
log(s["C3"].value == 5 and s["C4"].value == 1, f"exemplo: {s['C3'].value} itens para comprar e {s['C4'].value} no mínimo (esperado 5 e 1)")
log(abs(s["H3"].value - (2*120 + 3*45 + 1*25 + 6*2.5 + 6*1.8)) < 1e-6, f"exemplo: custo estimado R$ {s['H3'].value:.2f} (conta à mão: 425,80)")
log(s["H4"].value == 1, "exemplo: 1 item com diferença na contagem (toalha de rosto: contou 22, planilha diz 26)")
log(R["exemplo"]["Movimentos"]["G24"].value == "Item não cadastrado", "exemplo: 'Toalha de praia' marcada como item não cadastrado")
log(R["saida_maior"]["Saldo"][f"I{S0}"].value == "Confira: saídas maiores que entradas", "saldo negativo é sinalizado")
log(R["minimo_manual_vence"]["Saldo"][f"G{S0}"].value == 5, "mínimo digitado substitui o calculado")
b = R["branco"]["Saldo"]
log(b["C3"].value == 0 and b[f"I{S0}"].value == "Defina o mínimo" and b[f"B{S0}"].value == PADRAO[0][1], "versão em branco: lista pronta, pede o mínimo, nada para comprar")
erros = [(n, ws.title, c.coordinate) for n, wb in R.items() for ws in wb for row in ws.iter_rows() for c in row
         if isinstance(c.value, str) and c.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(R)} arquivos" + (f" {erros[:4]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

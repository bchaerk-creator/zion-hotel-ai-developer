"""Testa a Ferramenta 19 recalculando no LibreOffice e comparando com uma regra independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, random, datetime, calendar
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from dados import CATEGORIAS, EX_ORC, EX_MES, EX_NOITES, EX_COMPRAS
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EX = D / "Controle-Compras-Zion-EM-BRANCO.xlsx", D / "Controle-Compras-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
K0, C0, M0, A0, NK = 6, 7, 7, 6, 15
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
dt = lambda s: datetime.date.fromisoformat(s) if isinstance(s, str) and len(s) == 10 and s[4] == "-" else s

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)

def referencia(cats, compras, mes, noites):
    """cats: lista de (nome, orçamento). compras: (data, cat, desc, forn, unid, valor, pag, comp). Regra escrita a partir da aba Comece aqui."""
    nomes = [c for c, _ in cats if c]
    sits = []
    for data, cat, _, _, _, valor, _, comp in compras:
        if data is None and cat in (None, "") and valor is None: s = ""
        elif not isinstance(data, datetime.date): s = "Informe a data"
        elif cat in (None, "") or cat not in nomes: s = "Categoria não cadastrada"
        elif not isnum(valor) or valor <= 0: s = "Confira o valor"
        elif comp != "Sim": s = "Sem comprovante"
        else: s = "OK"
        sits.append(s)
    validas = [(c, s) for c, s in zip(compras, sits) if s in ("OK", "Sem comprovante")]
    res = dict(sits=sits, prob=sum(1 for s in sits if s not in ("", "OK", "Sem comprovante")), semcomp=sits.count("Sem comprovante"))
    if not isinstance(mes, datetime.date): res["linhas"] = None; return res
    ini = mes.replace(day=1); fim = mes.replace(day=calendar.monthrange(mes.year, mes.month)[1])
    linhas = []
    for nome, orc in cats:
        if not nome: linhas.append(None); continue
        g = sum(c[5] for c, _ in validas if c[1] == nome and ini <= c[0] <= fim)
        o = orc if isnum(orc) else None
        if o is None: sit = "Sem orçamento" if g > 0 else ""
        elif g > o: sit = "Acima do orçamento"
        elif g >= 0.9 * o: sit = "Atenção: 90% ou mais"
        else: sit = "Dentro"
        linhas.append(dict(g=g, o=o, dif=None if o is None else o - g, pct=None if o in (None, 0) else g / o, sit=sit,
                           noite=g / noites if isnum(noites) and noites > 0 else None,
                           ano=[sum(c[5] for c, _ in validas if c[1] == nome and c[0].year == mes.year and c[0].month == k) for k in range(1, 13)]))
    res["linhas"] = linhas
    res["total"] = sum(c[5] for c, _ in validas if ini <= c[0] <= fim)
    res["acima"] = sum(1 for l in linhas if l and l["sit"] == "Acima do orçamento")
    res["atencao"] = sum(1 for l in linhas if l and l["sit"] == "Atenção: 90% ou mais")
    res["semcomp_mes"] = sum(1 for c, s in validas if s == "Sem comprovante" and ini <= c[0] <= fim)
    return res

def cenario(nome, cats, compras, mes, noites):
    wb = load_workbook(BR); o, co, m = wb["Orçamento"], wb["Compras"], wb["Mês"]
    for i in range(NK):
        n, v = cats[i] if i < len(cats) else (None, None)
        o[f"A{K0+i}"], o[f"B{K0+i}"], o[f"C{K0+i}"] = n, None, v
    for k, c in enumerate(compras):
        for col, v in zip("ABCDEFGH", c): co[f"{col}{C0+k}"] = v
    m["C3"], m["C4"] = mes, noites
    p = TMP / f"{nome}.xlsx"; wb.save(p); cen[nome] = (p, cats, compras, mes, noites)

def aleatorio(nome, seed, erros):
    rnd = random.Random(seed)
    cats = [(f"Cat {seed}-{i}", rnd.choice([None, 100, 250.5, 400, 0, 1000])) for i in range(rnd.randint(1, 10))]
    mes = datetime.date(2026, rnd.randint(1, 12), rnd.randint(1, 28))
    def esc(bons, ruins): return rnd.choice(ruins) if erros and rnd.random() < .08 else rnd.choice(bons)
    compras = []
    for _ in range(rnd.randint(5, 80)):
        data = esc([mes + datetime.timedelta(days=rnd.randint(-40, 40)), datetime.date(2025, 12, 31), datetime.date(mes.year, mes.month, 1)], [None, "ontem"])
        compras.append((data, esc([c for c, _ in cats], ["Inexistente", None]), "x", "f", None,
                        esc([12.5, 40, 99.9, 250, 1000, 3.35], [0, -10, "cem"]), "Pix", esc(["Sim", "Sim", "Não", None], ["Sim"])))
    cenario(nome, cats, compras, mes, rnd.choice([None, 0, 30, 68, 120]))

for s in range(8): aleatorio(f"aleatorio_com_erros_{s}", 300 + s, True)
for s in range(4): aleatorio(f"aleatorio_limpo_{s}", 400 + s, False)
dia = datetime.date
cenario("limite_90", [("A", 100), ("B", 100), ("C", 100)],
        [(dia(2026, 5, 2), "A", "", "", None, 90, "Pix", "Sim"), (dia(2026, 5, 3), "B", "", "", None, 89.99, "Pix", "Sim"), (dia(2026, 5, 4), "C", "", "", None, 100, "Pix", "Sim")], dia(2026, 5, 20), 10)
cenario("virada_de_mes", [("A", 50)], [(dia(2026, 4, 30), "A", "", "", None, 70, "Pix", "Sim"), (dia(2026, 5, 1), "A", "", "", None, 20, "Pix", "Sim"),
                                        (dia(2026, 5, 31), "A", "", "", None, 25, "Pix", "Não"), (dia(2026, 6, 1), "A", "", "", None, 99, "Pix", "Sim")], dia(2026, 5, 15), None)
cenario("sem_orcamento", [("A", None), ("B", None)], [(dia(2026, 3, 3), "A", "", "", None, 40, "Pix", "Sim")], dia(2026, 3, 1), 0)
cenario("orcamento_zero", [("A", 0)], [(dia(2026, 3, 3), "A", "", "", None, 40, "Pix", "Sim")], dia(2026, 3, 1), 5)
cenario("sem_mes_escolhido", [("A", 100)], [(dia(2026, 3, 3), "A", "", "", None, 40, "Pix", "Sim"), (None, "A", "", "", None, 10, "Pix", "Sim")], None, 5)
cenario("ano_bissexto_fevereiro", [("A", 100)], [(dia(2028, 2, 29), "A", "", "", None, 30, "Pix", "Sim"), (dia(2028, 3, 1), "A", "", "", None, 5, "Pix", "Sim")], dia(2028, 2, 10), 4)

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EX), str(BR)]
               + [str(c[0]) for c in cen.values()], check=True, capture_output=True, timeout=900)
R = {n: load_workbook(OUTD / c[0].name, data_only=True) for n, c in cen.items()}
R["exemplo"] = load_workbook(OUTD / EX.name, data_only=True); R["branco"] = load_workbook(OUTD / BR.name, data_only=True)
EXC = [tuple([dt(c[0])] + list(c[1:])) for c in EX_COMPRAS]
cen["exemplo"] = (EX, [(c, EX_ORC.get(c)) for c, _ in CATEGORIAS], EXC, dt(EX_MES), EX_NOITES)

def igual(a, b, tol=1e-6):
    if a in (None, "") and b in (None, ""): return True
    if isnum(a) and isnum(b): return abs(a - b) < tol
    return a == b

def confere(nome):
    _, cats, compras, mes, noites = cen[nome]; ref = referencia(cats, compras, mes, noites)
    co, m, a = R[nome]["Compras"], R[nome]["Mês"], R[nome]["Ano"]; erros = []
    for k, s in enumerate(ref["sits"]):
        if not igual(s, co[f"I{C0+k}"].value): erros.append((f"I{C0+k}", s, co[f"I{C0+k}"].value))
    if co["C3"].value != ref["prob"] or co["E3"].value != ref["semcomp"]: erros.append(("contagens", ref["prob"], ref["semcomp"], co["C3"].value, co["E3"].value))
    if ref["linhas"] is None:
        if any(m[f"B{M0+i}"].value not in (None, "") for i in range(NK)): erros.append(("sem mês mas há gasto",))
        return erros, ref
    for i, l in enumerate(ref["linhas"]):
        if l is None: continue
        r = M0 + i; g = lambda c: m[f"{c}{r}"].value
        for c, v in dict(B=l["g"], C=l["o"], D=l["dif"], E=l["pct"], F=l["sit"], G=l["noite"]).items():
            if not igual(v, g(c)): erros.append((f"Mês!{c}{r}", v, g(c)))
        for k in range(12):
            got = a.cell(A0 + i, 2 + k).value
            if not igual(l["ano"][k], got): erros.append((f"Ano!{a.cell(A0+i, 2+k).coordinate}", l["ano"][k], got))
    t = M0 + NK
    if not igual(ref["total"], m[f"B{t}"].value): erros.append(("total", ref["total"], m[f"B{t}"].value))
    for rr, chave in ((t + 2, "acima"), (t + 3, "atencao"), (t + 4, "semcomp_mes")):
        if not igual(ref[chave], m[f"C{rr}"].value): erros.append((chave, ref[chave], m[f"C{rr}"].value))
    return erros, ref

for nome in ["exemplo"] + [n for n in cen if n != "exemplo"]:
    erros, ref = confere(nome)
    n = sum(1 for s in ref["sits"] if s)
    log(not erros, f"{nome}: {n} compras conferidas, {ref['prob']} com problema, {ref['semcomp']} sem comprovante" + (f" | diferenças: {erros[:3]}" if erros else ""))

m = R["exemplo"]["Mês"]; t = M0 + NK
log(abs(m[f"B{t}"].value - 2741.70) < 1e-6 and abs(m[f"G{t}"].value - 2741.70 / 68) < 1e-6,
    f"exemplo: novembro soma R$ {m[f'B{t}'].value:.2f} e R$ {m[f'G{t}'].value:.2f} por noite ocupada (conta à mão: 2.741,70 ÷ 68 = 40,32)")
log(m["F9"].value == "Atenção: 90% ou mais" and m["F13"].value == "Acima do orçamento", "exemplo: enxoval exatamente em 90% fica em Atenção; consumo da equipe passa do orçamento")
log(R["exemplo"]["Compras"]["I26"].value == "Categoria não cadastrada", "exemplo: 'Jardinagem' não está no orçamento e não entra nas somas")
b = R["branco"]
log(b["Compras"]["C3"].value == 0 and b["Orçamento"]["A6"].value == CATEGORIAS[0][0] and b["Mês"]["F3"].value == "Informe uma data em C3",
    "versão em branco: categorias prontas, nada lançado, pede a data do mês")
erros = [(n, ws.title, c.coordinate) for n, wb in R.items() for ws in wb for row in ws.iter_rows() for c in row
         if isinstance(c.value, str) and c.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(R)} arquivos" + (f" {erros[:4]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

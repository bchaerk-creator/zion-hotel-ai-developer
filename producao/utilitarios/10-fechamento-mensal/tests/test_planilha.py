"""Testa a Ferramenta 10 recalculando no LibreOffice e comparando com uma regra independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, random, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from dados import TODOS, CANAIS, CATEGORIAS, EX_MES, EX_IMOVEIS, EX_LANC
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EX = D / "Fechamento-Mensal-Zion-EM-BRANCO.xlsx", D / "Fechamento-Mensal-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
dt = lambda s: datetime.date.fromisoformat(s) if isinstance(s, str) and len(s) == 10 and s[4] == "-" else s
vazio = lambda x: x in (None, "")
CHAVE = lambda x: (x.year, x.month)

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)

def referencia(mes, imoveis, cats, lancs):
    """Regra escrita a partir da aba Comece aqui, sem olhar as fórmulas."""
    imv = [i for i in imoveis if not vazio(i)]; cset = [c for c in cats if not vazio(c)]
    res = []
    for data, im, tipo, cc, desc, val, conf in lancs:
        if data is None and vazio(im) and vazio(tipo) and vazio(val): s = ""
        elif not isinstance(data, datetime.date): s = "Informe a data"
        elif vazio(im): s = "Escolha o imóvel"
        elif im != TODOS and im not in imv: s = "Imóvel não cadastrado"
        elif tipo not in ("Receita", "Despesa"): s = "Escolha o tipo"
        elif tipo == "Receita" and im == TODOS: s = "Receita precisa de um imóvel"
        elif tipo == "Receita" and cc not in CANAIS: s = "Escolha o canal"
        elif tipo == "Despesa" and (vazio(cc) or cc not in cset): s = "Categoria não cadastrada"
        elif not isnum(val) or val <= 0: s = "Confira o valor"
        elif conf != "Sim": s = "A conferir no extrato"
        else: s = "OK"
        res.append(s)
    validos = [(l, s) for l, s in zip(lancs, res) if s in ("OK", "A conferir no extrato")]
    n = len(imv)
    def resultado(nome, chave):
        rec = sum(l[5] for l, s in validos if l[1] == nome and l[2] == "Receita" and CHAVE(l[0]) == chave)
        dsp = sum(l[5] for l, s in validos if l[1] == nome and l[2] == "Despesa" and CHAVE(l[0]) == chave)
        dv = sum(l[5] for l, s in validos if l[1] == TODOS and l[2] == "Despesa" and CHAVE(l[0]) == chave) / n if n else 0
        return rec, dsp, dv
    linhas = {}
    ch = CHAVE(mes) if isinstance(mes, datetime.date) else None
    for k, nome in enumerate(imoveis):
        if vazio(nome): continue
        rec, dsp, dv = resultado(nome, ch)
        conf = sum(1 for l, s in validos if l[1] == nome and CHAVE(l[0]) == ch and s == "A conferir no extrato")
        r_ = rec - dsp - dv
        sit = "Sem lançamentos próprios" if rec == 0 and dsp == 0 and conf == 0 else f"Confira {conf} no extrato" if conf > 0 else "Resultado negativo" if r_ < 0 else "Fechado"
        linhas[k] = dict(B=rec, C=dsp, D=dv, E=r_, F=conf, G=sit)
    prob = sum(1 for s in res if s and s not in ("OK", "A conferir no extrato"))
    conf_mes = sum(1 for l, s in validos if CHAVE(l[0]) == ch and s == "A conferir no extrato")
    tot = dict(B=sum(x["B"] for x in linhas.values()), C=sum(x["C"] for x in linhas.values()), D=sum(x["D"] for x in linhas.values()),
               E=sum(x["E"] for x in linhas.values()), F=conf_mes)
    neg = sum(1 for x in linhas.values() if x["G"] == "Resultado negativo")
    if ch is None: leit = "Informe o mês do fechamento"
    elif n == 0: leit = "Cadastre os imóveis"
    elif prob > 0: leit = f"Corrija {prob} lançamento(s) com problema"
    elif conf_mes > 0: leit = f"Confira no extrato {conf_mes} lançamento(s) do mês"
    elif not any(CHAVE(l[0]) == ch for l, s in validos): leit = "Lance as receitas e despesas do mês"
    elif neg > 0: leit = f"Resultado negativo em {neg} imóvel(is): reveja as despesas"
    else: leit = "Mês fechado"
    canais = {c: sum(l[5] for l, s in validos if l[2] == "Receita" and l[3] == c and CHAVE(l[0]) == ch) for c in CANAIS}
    catv = {c: sum(l[5] for l, s in validos if l[2] == "Despesa" and l[3] == c and CHAVE(l[0]) == ch) for c in cset}
    ano = {}
    if ch:
        for k, nome in enumerate(imoveis):
            if vazio(nome): continue
            ano[k] = [(lambda t: t[0] - t[1] - t[2])(resultado(nome, (ch[0], m))) for m in range(1, 13)]
    return res, linhas, tot, prob, leit, canais, catv, ano

def cenario(nome, mes, imoveis, lancs, cats=None):
    wb = load_workbook(BR); ca, la, fe = wb["Cadastros"], wb["Lançamentos"], wb["Fechamento"]
    fe["B3"] = mes
    for k, i in enumerate(imoveis): ca[f"A{7+k}"] = i
    if cats is not None:
        for k in range(20): ca[f"C{7+k}"] = cats[k] if k < len(cats) else None
    for k, v in enumerate(lancs):
        for col, x in zip("ABCDEFG", v): la[f"{col}{7+k}"] = x
    p = TMP / f"{nome}.xlsx"; wb.save(p); cen[nome] = (p, mes, imoveis, lancs, cats if cats is not None else CATEGORIAS)

def aleatorio(nome, seed, erros):
    rnd = random.Random(seed)
    mes = datetime.date(2026, rnd.randint(1, 12), rnd.randint(1, 28))
    def esc(bons, ruins): return rnd.choice(ruins) if erros and rnd.random() < .08 else rnd.choice(bons)
    imoveis = [f"Imóvel {seed}-{i}" for i in range(rnd.randint(1, 10))]
    if rnd.random() < .3 and len(imoveis) > 2: imoveis[1] = None
    nomes = [i for i in imoveis if i]
    lancs = []
    for j in range(rnd.randint(5, 120)):
        tipo = esc(["Receita", "Despesa", "Despesa"], [None, "Saída"])
        im = esc(nomes + ([TODOS] if tipo == "Despesa" else []), ["Fora", None, TODOS])
        cc = esc(CANAIS if tipo == "Receita" else CATEGORIAS, ["Pix", None, "Jardinagem"])
        data = esc([mes + datetime.timedelta(days=rnd.randint(-70, 70))], [None, "ontem"])
        val = esc([round(rnd.uniform(20, 3000), 2)], [0, -50, "cem", None])
        lancs.append((data, im, tipo, cc, "x", val, rnd.choice(["Sim", "Sim", "Sim", "Não", None])))
    cenario(nome, mes, imoveis, lancs)

for s in range(8): aleatorio(f"aleatorio_com_erros_{s}", 1000 + s, True)
for s in range(4): aleatorio(f"aleatorio_limpo_{s}", 1050 + s, False)
dia = datetime.date; M = dia(2026, 3, 15)
cenario("divisao_por_tres", M, ["A", "B", "C"], [(dia(2026, 3, 1), TODOS, "Despesa", "Internet", "", 100, "Sim"), (dia(2026, 3, 2), "A", "Receita", "Airbnb", "", 500, "Sim")])
cenario("virada_de_mes", M, ["A"], [(dia(2026, 2, 28), "A", "Receita", "Airbnb", "", 700, "Sim"), (dia(2026, 3, 31), "A", "Receita", "Booking", "", 300, "Sim"),
                                    (dia(2026, 4, 1), "A", "Despesa", "Limpeza", "", 90, "Sim")])
cenario("tudo_fechado", M, ["A", "B"], [(dia(2026, 3, 3), "A", "Receita", "Airbnb", "", 900, "Sim"), (dia(2026, 3, 4), "B", "Receita", "Reserva direta", "", 600, "Sim"),
                                        (dia(2026, 3, 5), "B", "Despesa", "Energia", "", 200, "Sim")])
cenario("resultado_negativo", M, ["A"], [(dia(2026, 3, 3), "A", "Receita", "Airbnb", "", 100, "Sim"), (dia(2026, 3, 4), "A", "Despesa", "Manutenção", "", 250, "Sim")])
cenario("receita_com_todos", M, ["A", "B"], [(dia(2026, 3, 3), TODOS, "Receita", "Airbnb", "", 100, "Sim")])
cenario("categoria_nova", M, ["A"], [(dia(2026, 3, 3), "A", "Despesa", "Jardinagem", "", 80, "Sim")], cats=CATEGORIAS + ["Jardinagem"])
cenario("mes_sem_lancamentos", M, ["A"], [(dia(2026, 1, 3), "A", "Receita", "Airbnb", "", 100, "Sim")])
cenario("sem_imoveis", M, [], [])

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EX), str(BR)]
               + [str(c[0]) for c in cen.values()], check=True, capture_output=True, timeout=900)
R = {n: load_workbook(OUTD / c[0].name, data_only=True) for n, c in cen.items()}
R["exemplo"] = load_workbook(OUTD / EX.name, data_only=True); R["branco"] = load_workbook(OUTD / BR.name, data_only=True)
cen["exemplo"] = (EX, dt(EX_MES), EX_IMOVEIS, [(dt(l[0]),) + tuple(l[1:]) for l in EX_LANC], CATEGORIAS)
cen["branco"] = (BR, None, [], [], CATEGORIAS)

def igual(a, b, tol=1e-6):
    if a in (None, "") and b in (None, ""): return True
    if isnum(a) and isnum(b): return abs(a - b) < tol
    return a == b

def confere(nome):
    _, mes, imoveis, lancs, cats = cen[nome]; w = R[nome]
    if nome == "branco": mes = w["Fechamento"]["B3"].value
    if isinstance(mes, datetime.datetime): mes = mes.date()
    res, linhas, tot, prob, leit, canais, catv, ano = referencia(mes, imoveis, cats, lancs)
    la, fe, an = w["Lançamentos"], w["Fechamento"], w["Ano"]; erros = []
    for k, s in enumerate(res):
        if not igual(s, la[f"H{7+k}"].value): erros.append((f"Lançamentos!H{7+k}", s, la[f"H{7+k}"].value))
    for k, lin in linhas.items():
        for c, v in lin.items():
            if not igual(v, fe[f"{c}{8+k}"].value): erros.append((f"Fechamento!{c}{8+k}", v, fe[f"{c}{8+k}"].value))
    for c, v in tot.items():
        if not igual(v, fe[f"{c}18"].value): erros.append((f"Fechamento!{c}18", v, fe[f"{c}18"].value))
    if not igual(prob, fe["B4"].value): erros.append(("problemas", prob, fe["B4"].value))
    if fe["B5"].value != leit: erros.append(("leitura", leit, fe["B5"].value))
    for k, cn in enumerate(CANAIS):
        if not igual(canais[cn], fe[f"B{22+k}"].value): erros.append((f"canal {cn}", canais[cn], fe[f"B{22+k}"].value))
    for k, cn in enumerate(c for c in cats if not vazio(c)):
        if not igual(catv[cn], fe[f"B{29+k}"].value): erros.append((f"categoria {cn}", catv[cn], fe[f"B{29+k}"].value))
    for k, meses in ano.items():
        for m, v in enumerate(meses):
            got = an.cell(6 + k, 2 + m).value
            if not igual(v, got): erros.append((f"Ano {k} mês {m+1}", v, got))
    return erros, res, tot, prob

for nome in ["exemplo", "branco"] + [x for x in cen if x not in ("exemplo", "branco")]:
    erros, res, tot, prob = confere(nome)
    log(not erros, f"{nome}: {sum(1 for s in res if s)} lançamentos conferidos, {prob} com problema, resultado do mês R$ {tot['E']:.2f}" + (f" | diferenças: {erros[:3]}" if erros else ""))

fe = R["exemplo"]["Fechamento"]
log([fe[f"E{r}"].value for r in (8, 9, 10)] == [1610, 1800, -70] and fe["E18"].value == 3340,
    "exemplo à mão: Apto 3000 − 1140 − 250 = 1610; Casa 3200 − 1150 − 250 = 1800; Chalé 2380 − 2200 − 250 = −70; total 3340")
log(fe["B5"].value == "Corrija 2 lançamento(s) com problema" and R["exemplo"]["Lançamentos"]["H20"].value == "Categoria não cadastrada"
    and R["exemplo"]["Lançamentos"]["H21"].value == "Confira o valor", "exemplo: jardinagem sem categoria e valor em texto ficam fora e pedem correção")
dv = R["divisao_por_tres"]["Fechamento"]
log(all(abs(dv[f"D{r}"].value - 100 / 3) < 1e-9 for r in (8, 9, 10)) and abs(dv["D18"].value - 100) < 1e-9, "despesa de R$ 100 dividida por 3 imóveis: R$ 33,33 cada, total R$ 100")
vm = R["virada_de_mes"]["Fechamento"]
log(vm["B8"].value == 300 and vm["C8"].value == 0, "virada de mês: 28/02 e 01/04 ficam fora do fechamento de março")
log(R["categoria_nova"]["Lançamentos"]["H7"].value == "OK", "categoria acrescentada nos Cadastros passa a valer nos lançamentos")
b = R["branco"]
log(isinstance(b["Fechamento"]["B3"].value, datetime.datetime) and b["Fechamento"]["B5"].value == "Cadastre os imóveis", "versão em branco: mês anterior automático e pedido para cadastrar os imóveis")
erros = [(nm, ws.title, cc.coordinate) for nm, wb in R.items() for ws in wb for row in ws.iter_rows() for cc in row
         if isinstance(cc.value, str) and cc.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(R)} arquivos" + (f" {erros[:4]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

"""Testa a Ferramenta 28 recalculando no LibreOffice e comparando com uma regra independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, random, datetime, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from dados import EX_HOJE, EX_EXP, EX_SAI
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EX = D / "Capacidade-Atendimento-Zion-EM-BRANCO.xlsx", D / "Capacidade-Atendimento-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
E0, S0 = 7, 7
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
inteiro = lambda x: isnum(x) and x >= 0 and int(x) == x
dt = lambda s: datetime.date.fromisoformat(s) if isinstance(s, str) and len(s) == 10 and s[4] == "-" else s
vazio = lambda x: x in (None, "")
n = lambda x: x if isnum(x) else 0

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)

def referencia(hoje, exps, sais):
    """Regra escrita a partir da aba Comece aqui, sem olhar as fórmulas."""
    es = {}
    for nome, cap, por, mn, ant, _ in exps:
        if vazio(nome): continue
        if not inteiro(cap) or cap < 1: s = "Confira a capacidade"
        elif not inteiro(por) or por < 1: s = "Confira pessoas por condutor"
        elif (not vazio(mn) and not inteiro(mn)) or n(mn) > cap: s = "Confira o mínimo"
        elif not vazio(ant) and not inteiro(ant): s = "Confira a antecedência"
        else: s = "Pronta"
        if nome not in es: es[nome] = dict(s=s, cap=n(cap), por=n(por), mn=n(mn), ant=n(ant))
    res = []
    for data, hora, exp, resv, cond, esp in sais:
        calc = None
        if data is None and vazio(exp) and vazio(resv): s = ""
        elif not isinstance(data, datetime.date): s = "Informe a data"
        elif vazio(exp) or exp not in es: s = "Experiência não cadastrada"
        elif es[exp]["s"] != "Pronta": s = "Complete a experiência"
        elif not vazio(resv) and not inteiro(resv): s = "Confira os reservados"
        elif not vazio(cond) and not inteiro(cond): s = "Confira os condutores"
        elif not vazio(esp) and not inteiro(esp): s = "Confira a lista de espera"
        else:
            e = es[exp]; p = n(resv); prec = math.ceil(p / e["por"]); lim = data - datetime.timedelta(days=e["ant"])
            if data < hoje: s = "Já passou"
            elif p > e["cap"]: s = "Acima da capacidade"
            elif n(cond) < prec: s = "Falta condutor"
            elif p < e["mn"]: s = "Decida: confirmar ou cancelar" if hoje >= lim else "Abaixo do mínimo"
            elif p == e["cap"]: s = "Lotada, com lista de espera" if n(esp) > 0 else "Lotada"
            else: s = "Confirmada"
            calc = dict(G=e["cap"], H=e["cap"] - p, I=prec, J=p / e["cap"], K=lim)
        res.append((data, exp, s, calc, n(resv), n(esp)))
    fut = [x for x in res if x[2] not in ("", "Já passou") and x[3]]
    agg = {}
    for nome, e in es.items():
        mine = [x for x in fut if x[1] == nome]; pes = sum(x[4] for x in mine)
        agg[nome] = dict(H=len(mine), I=pes, J=(pes / (len(mine) * e["cap"]) if mine and e["s"] == "Pronta" else None))
    st = [x[2] for x in res]
    nomes = [e[0] for e in exps if not vazio(e[0])]
    validas = {"Já passou", "Acima da capacidade", "Falta condutor", "Decida: confirmar ou cancelar", "Abaixo do mínimo", "Lotada, com lista de espera", "Lotada", "Confirmada"}
    em7 = [x for x in fut if x[0] <= hoje + datetime.timedelta(days=6)]
    painel = [hoje, len(nomes), sum(1 for nm in nomes if es[nm]["s"] != "Pronta"), len(fut),
              st.count("Confirmada") + st.count("Lotada") + st.count("Lotada, com lista de espera"),
              st.count("Abaixo do mínimo") + st.count("Decida: confirmar ou cancelar"), st.count("Decida: confirmar ou cancelar"),
              st.count("Falta condutor"), st.count("Acima da capacidade"), st.count("Lotada, com lista de espera"),
              sum(1 for s in st if s and s not in validas), sum(x[4] for x in em7), sum(x[3]["I"] for x in em7), sum(x[5] for x in fut)]
    P = painel
    if P[1] == 0: leit = "Cadastre as experiências"
    elif P[2] > 0: leit = f"Complete o cadastro de {P[2]} experiência(s)"
    elif P[10] > 0: leit = "Corrija as saídas com problema"
    elif P[8] > 0: leit = f"Remaneje {P[8]} saída(s) acima da capacidade"
    elif P[7] > 0: leit = f"Escale condutor em {P[7]} saída(s)"
    elif P[6] > 0: leit = f"Decida {P[6]} saída(s) abaixo do mínimo: confirmar ou cancelar"
    elif P[9] > 0: leit = f"Abra outro horário: {P[9]} saída(s) lotada(s) com lista de espera"
    elif P[3] == 0: leit = "Cadastre as próximas saídas"
    else: leit = "Tudo em dia"
    return es, res, agg, painel, leit

def cenario(nome, hoje, exps, sais):
    wb = load_workbook(BR); ex, sa = wb["Experiências"], wb["Saídas"]
    ex["B4"] = hoje
    for k, v in enumerate(exps):
        for col, x in zip("ABCDEF", v): ex[f"{col}{E0+k}"] = x
    for k, v in enumerate(sais):
        for col, x in zip("ABCDEF", v): sa[f"{col}{S0+k}"] = x
    p = TMP / f"{nome}.xlsx"; wb.save(p); cen[nome] = (p, hoje, exps, sais)

def aleatorio(nome, seed, erros):
    rnd = random.Random(seed)
    hoje = datetime.date(2026, rnd.randint(1, 12), rnd.randint(1, 28))
    def esc(bons, ruins): return rnd.choice(ruins) if erros and rnd.random() < .08 else rnd.choice(bons)
    exps = []
    for i in range(rnd.randint(1, 8)):
        cap = esc([rnd.randint(2, 30)], [0, 2.5, "dez", None, -4])
        por = esc([rnd.randint(1, 12)], [0, 1.5, None])
        mn = esc([None, rnd.randint(0, 6)], [-1, 2.5, 99, "três"])
        ant = esc([None, rnd.randint(0, 5)], [-2, 0.5, "x"])
        exps.append((f"E{seed}-{i}", cap, por, mn, ant, "ponto"))
    nomes = [e[0] for e in exps]
    sais = []
    for j in range(rnd.randint(3, 80)):
        data = esc([hoje + datetime.timedelta(days=rnd.randint(-10, 20))], [None, "amanhã"])
        resv = esc([None, rnd.randint(0, 32)], [-3, 4.5, "seis"])
        sais.append((data, rnd.choice(["08:00", None]), esc(nomes, ["Fora", None]), resv,
                     esc([None, rnd.randint(0, 5)], [-1, 1.5]), esc([None, None, rnd.randint(0, 6)], [-2, "dois"])))
    cenario(nome, hoje, exps, sais)

for s in range(8): aleatorio(f"aleatorio_com_erros_{s}", 2800 + s, True)
for s in range(4): aleatorio(f"aleatorio_limpo_{s}", 2850 + s, False)
dia = datetime.date; H = dia(2026, 6, 10)
E1 = [("A", 10, 5, 4, 2, "")]
cenario("prazo_no_dia_exato", H, E1, [(dia(2026, 6, 12), None, "A", 3, 1, None), (dia(2026, 6, 13), None, "A", 3, 1, None)])
cenario("condutor_no_limite", H, E1, [(dia(2026, 6, 20), None, "A", 10, 2, None), (dia(2026, 6, 20), None, "A", 6, 1, None), (dia(2026, 6, 20), None, "A", 5, 1, None)])
cenario("lotada_e_acima", H, E1, [(dia(2026, 6, 20), None, "A", 10, 2, 4), (dia(2026, 6, 20), None, "A", 11, 3, None)])
cenario("hoje_e_ontem", H, E1, [(H, None, "A", 5, 1, None), (H - datetime.timedelta(days=1), None, "A", 5, 1, None)])
cenario("sete_dias_limite", H, [("A", 10, 5, None, None, "")], [(H + datetime.timedelta(days=6), None, "A", 5, 1, None), (H + datetime.timedelta(days=7), None, "A", 7, 2, None)])
cenario("tudo_em_dia", H, [("A", 10, 5, None, None, "")], [(dia(2026, 6, 20), None, "A", 5, 1, None)])
cenario("so_experiencias", H, [("A", 10, 5, None, None, "")], [])
cenario("sem_experiencias", H, [], [])

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EX), str(BR)]
               + [str(c[0]) for c in cen.values()], check=True, capture_output=True, timeout=900)
R = {nm: load_workbook(OUTD / c[0].name, data_only=True) for nm, c in cen.items()}
R["exemplo"] = load_workbook(OUTD / EX.name, data_only=True); R["branco"] = load_workbook(OUTD / BR.name, data_only=True)
cen["exemplo"] = (EX, dt(EX_HOJE), list(EX_EXP), [(dt(s[0]),) + tuple(s[1:]) for s in EX_SAI])
cen["branco"] = (BR, None, [], [])

def igual(a, b, tol=1e-6):
    if isinstance(a, datetime.date) and isinstance(b, datetime.datetime): b = b.date()
    if a in (None, "") and b in (None, ""): return True
    if isnum(a) and isnum(b): return abs(a - b) < tol
    return a == b

def confere(nome):
    _, hoje, exps, sais = cen[nome]; w = R[nome]
    if nome == "branco": hoje = w["Experiências"]["B4"].value
    if isinstance(hoje, datetime.datetime): hoje = hoje.date()
    es, res, agg, painel, leit = referencia(hoje, exps, sais)
    ex, sa, p = w["Experiências"], w["Saídas"], w["Painel"]; erros = []
    for k, e in enumerate(exps):
        if vazio(e[0]): continue
        r = E0 + k
        for c, v in dict(G=es[e[0]]["s"], **agg[e[0]]).items():
            if not igual(v, ex[f"{c}{r}"].value): erros.append((f"Experiências!{c}{r}", v, ex[f"{c}{r}"].value))
    for k, (_, _, s, calc, _, _) in enumerate(res):
        r = S0 + k
        esperado = dict(L=s, **(calc or dict(G=None, H=None, I=None, J=None, K=None)))
        for c, v in esperado.items():
            if not igual(v, sa[f"{c}{r}"].value): erros.append((f"Saídas!{c}{r}", v, sa[f"{c}{r}"].value))
    for i, v in enumerate(painel):
        if not igual(v, p[f"B{4+i}"].value): erros.append((p[f"A{4+i}"].value, v, p[f"B{4+i}"].value))
    if p["A20"].value != leit: erros.append(("leitura", leit, p["A20"].value))
    return erros, painel, res

for nome in ["exemplo", "branco"] + [x for x in cen if x not in ("exemplo", "branco")]:
    erros, painel, res = confere(nome)
    log(not erros, f"{nome}: {painel[1]} experiências e {sum(1 for x in res if x[2])} saídas conferidas, {painel[10]} com problema" + (f" | diferenças: {erros[:3]}" if erros else ""))

sa, p = R["exemplo"]["Saídas"], R["exemplo"]["Painel"]
st = [sa[f"L{r}"].value for r in range(7, 18)]
log(st == ["Já passou", "Lotada, com lista de espera", "Falta condutor", "Decida: confirmar ou cancelar", "Abaixo do mínimo", "Confirmada",
           "Acima da capacidade", "Confirmada", "Experiência não cadastrada", "Informe a data", "Lotada"], "exemplo: as 11 situações esperadas, na ordem")
log(p["B15"].value == 50 and p["B16"].value == 10 and sa["I9"].value == 2 and sa["I13"].value == 3,
    f"exemplo: {p['B15'].value} pessoas e {p['B16'].value} condutores nos próximos 7 dias (conta à mão: 12+14+2+3+8+11 = 50; 2+2+1+1+1+3 = 10; café com 14 pede 2; barco com 11 pede 3)")
q = R["prazo_no_dia_exato"]["Saídas"]
log(q["L7"].value == "Decida: confirmar ou cancelar" and q["L8"].value == "Abaixo do mínimo", "prazo no dia exato já pede decisão; um dia antes do prazo ainda não")
c = R["condutor_no_limite"]["Saídas"]
log([c[f"L{r}"].value for r in (7, 8, 9)] == ["Lotada", "Falta condutor", "Confirmada"], "10 pessoas com 2 condutores de 5 bastam; 6 pessoas com 1 condutor faltam; 5 com 1 bastam")
s7 = R["sete_dias_limite"]["Painel"]
log(s7["B15"].value == 5 and s7["B7"].value == 2, "próximos 7 dias contam hoje + 6 dias; o sétimo dia fica de fora")
b = R["branco"]
log(isinstance(b["Experiências"]["B4"].value, datetime.datetime) and b["Painel"]["A20"].value == "Cadastre as experiências", "versão em branco: data de hoje automática e painel pede as experiências")
erros = [(nm, ws.title, cc.coordinate) for nm, wb in R.items() for ws in wb for row in ws.iter_rows() for cc in row
         if isinstance(cc.value, str) and cc.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(R)} arquivos" + (f" {erros[:4]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

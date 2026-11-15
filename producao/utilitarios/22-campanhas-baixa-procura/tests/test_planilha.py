"""Testa a Ferramenta 22 recalculando no LibreOffice e comparando com uma regra independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, random, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from dados import EX_BASE, EX_PER, EX_CAMP
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EX = D / "Campanhas-Baixa-Procura-Zion-EM-BRANCO.xlsx", D / "Campanhas-Baixa-Procura-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
P0, C0, NP, NC = 6, 7, 20, 60
KEYS = ["unidades", "diaria", "piso", "taxa", "custo", "meta"]
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
isdate = lambda x: isinstance(x, datetime.date)
dt = lambda s: datetime.date.fromisoformat(s) if isinstance(s, str) else s

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)

def referencia(base, pers, camps):
    """Regra escrita a partir da aba Comece aqui."""
    u, dia, piso, tx, cu, meta = (base.get(k) for k in KEYS)
    if not isnum(u) or u < 1: bs = "Informe as unidades"
    elif not isnum(dia) or dia <= 0: bs = "Informe a diária normal"
    elif isnum(tx) and (tx < 0 or tx >= 1): bs = "Taxas entre 0% e 99%"
    elif isnum(meta) and (meta < 0 or meta > 1): bs = "Meta entre 0% e 100%"
    else: bs = "OK"
    nomes = [p[0] for p in pers if p[0]]
    per_info = {}
    for nome, ini, fim, res in pers:
        if not nome: continue
        if nome not in per_info: per_info[nome] = (ini, fim)
    alertas, dcs, lqs, fats = [], [], [], []
    for c in camps:
        per, tipo, desc, est, canal, com, ter, resp, sit, vend = c
        n = lambda x: x if isnum(x) else 0
        em = est if isnum(est) else 1
        dc = n(dia) * (1 - desc) if isnum(desc) else None
        lq = dc * (1 - n(tx)) - n(cu) / em if dc is not None and isnum(em) and em >= 1 else None
        if per in (None, "") and tipo in (None, "") and desc in (None, ""): a = ""
        elif per in (None, "") or per not in nomes: a = "Período não cadastrado"
        elif tipo in (None, ""): a = "Escolha o tipo"
        elif bs != "OK": a = "Preencha a aba Base"
        elif not isnum(desc) or desc < 0 or desc >= 1: a = "Confira o desconto"
        elif est not in (None, "") and (not isnum(est) or est < 1): a = "Confira a estadia mínima"
        elif not isdate(com) or not isdate(ter) or com > ter: a = "Confira as datas"
        elif isnum(piso) and dc < piso: a = "Abaixo do piso"
        elif lq <= 0: a = "Não cobre o custo"
        elif isdate(per_info[per][0]) and ter < per_info[per][0]: a = "Termina antes do período"
        elif isdate(per_info[per][1]) and com > per_info[per][1]: a = "Começa depois do período"
        else: a = "OK"
        alertas.append(a)
        mostra = a not in ("", "Período não cadastrado", "Escolha o tipo", "Preencha a aba Base") and not a.startswith("Confira")
        dcs.append(dia * (1 - desc) if mostra else None)
        lqs.append(dcs[-1] * (1 - n(tx)) - n(cu) / em if mostra else None)
        fats.append(vend * dcs[-1] if a == "OK" and isnum(vend) else None)
    linhas = []
    for nome, ini, fim, res in pers:
        if not nome: linhas.append(None); continue
        dok = isdate(ini) and isdate(fim) and fim >= ini
        disp = (fim - ini).days + 1 if dok and isnum(u) and u >= 1 else None
        disp = disp * u if disp is not None else None
        oc = res / disp if disp and isnum(res) else None
        if not dok: s = "Confira as datas"
        elif not isnum(u) or u < 1: s = "Preencha a aba Base"
        elif not isnum(res) or res < 0: s = "Informe as noites reservadas"
        elif res > disp: s = "Reservadas maior que disponíveis"
        elif not isnum(meta): s = "Defina a meta na aba Base"
        elif oc < meta: s = "Abaixo da meta"
        else: s = "Na meta ou acima"
        ncamp = sum(1 for c, a in zip(camps, alertas) if c[0] == nome and a == "OK")
        vendidas = sum(c[9] for c, a in zip(camps, alertas) if c[0] == nome and a == "OK" and isnum(c[9]))
        linhas.append(dict(disp=disp, oc=oc, s=s, n=ncamp, v=vendidas))
    vl = [l for l in linhas if l]
    painel = [bs, len(vl), sum(1 for l in vl if l["s"] == "Abaixo da meta"), sum(1 for l in vl if l["s"] == "Abaixo da meta" and l["n"] == 0),
              sum(1 for a in alertas if a), sum(1 for a in alertas if a not in ("", "OK")),
              sum(1 for c, a in zip(camps, alertas) if a == "OK" and c[8] == "No ar"),
              sum(c[9] for c, a in zip(camps, alertas) if a == "OK" and isnum(c[9])), sum(f for f in fats if f is not None)]
    if bs != "OK": leit = "Preencha a aba Base: " + bs
    elif painel[1] == 0: leit = "Liste os períodos de baixa procura"
    elif painel[5] > 0: leit = "Corrija as campanhas com alerta"
    elif painel[3] > 0: leit = f"Planeje campanha para {painel[3]} período(s) abaixo da meta"
    elif painel[6] == 0: leit = "Coloque no ar as campanhas planejadas"
    else: leit = "Acompanhe as campanhas no ar e anote as noites vendidas"
    return bs, linhas, alertas, dcs, lqs, fats, painel, leit

def cenario(nome, base, pers, camps):
    wb = load_workbook(BR); b, pe, ca = wb["Base"], wb["Períodos"], wb["Campanhas"]
    for i, k in enumerate(KEYS): b[f"B{5+i}"] = base.get(k)
    for k, v in enumerate(pers):
        for col, x in zip("ABCD", v): pe[f"{col}{P0+k}"] = x
    for k, v in enumerate(camps):
        for col, x in zip("ABCDEFGHIK", v): ca[f"{col}{C0+k}"] = x
    p = TMP / f"{nome}.xlsx"; wb.save(p); cen[nome] = (p, base, pers, camps)

def aleatorio(nome, seed, erros):
    rnd = random.Random(seed)
    def esc(bons, ruins): return rnd.choice(ruins) if erros and rnd.random() < .08 else rnd.choice(bons)
    base = dict(unidades=esc([1, 2, 5], [0, None]), diaria=esc([200, 350.5, 600], [None]), piso=rnd.choice([None, 150, 280, 400]),
                taxa=esc([0, 0.12, 0.2], [1.2]), custo=rnd.choice([None, 0, 80, 150]), meta=esc([None, 0.4, 0.6, 1], [1.5]))
    pers = []
    for i in range(rnd.randint(1, 8)):
        ini = datetime.date(2027, rnd.randint(1, 12), rnd.randint(1, 20))
        fim = ini + datetime.timedelta(days=rnd.randint(0, 25))
        if erros and rnd.random() < .1: ini, fim = fim + datetime.timedelta(days=2), ini
        pers.append((f"Per {i}", ini, esc([fim], [None]), esc([0, 3, 10, 40], [-1, None, 9999])))
    camps = []
    for j in range(rnd.randint(2, 30)):
        p = rnd.choice(pers)
        com = p[1] + datetime.timedelta(days=rnd.randint(-40, 30)); ter = com + datetime.timedelta(days=rnd.randint(-3, 40))
        camps.append((esc([p[0]], ["Fora", None]), esc(["Estadia longa", "Última hora", "Outro"], [None]), esc([0, 0.05, 0.1, 0.2, 0.35, 0.5], [1, -0.1, "dez"]),
                      esc([None, 1, 2, 3, 7], [0, "duas"]), "Instagram", com, esc([ter], [None]), "R", rnd.choice(SIT), rnd.choice([None, 0, 3, 9])))
    cenario(nome, base, pers, camps)
SIT = ["Ideia", "Preparando", "No ar", "Encerrada"]

for s in range(8): aleatorio(f"aleatorio_com_erros_{s}", 700 + s, True)
for s in range(4): aleatorio(f"aleatorio_limpo_{s}", 800 + s, False)
dia = datetime.date
B = dict(unidades=2, diaria=400, piso=300, taxa=0.2, custo=100, meta=0.5)
P1 = [("P", dia(2027, 5, 1), dia(2027, 5, 10), 4)]
cenario("piso_exato", B, P1, [("P", "Outro", 0.25, 1, "E-mail", dia(2027, 4, 1), dia(2027, 5, 10), "R", "No ar", 2)])
cenario("nao_cobre_custo", dict(B, piso=None, custo=500), P1, [("P", "Outro", 0, 1, "E-mail", dia(2027, 4, 1), dia(2027, 5, 10), "R", "Ideia", None)])
cenario("estadia_minima_dilui_custo", dict(B, piso=None, custo=500), P1, [("P", "Estadia longa", 0, 4, "E-mail", dia(2027, 4, 1), dia(2027, 5, 10), "R", "Ideia", None)])
cenario("termina_antes", B, P1, [("P", "Outro", 0, 1, "E-mail", dia(2027, 3, 1), dia(2027, 4, 30), "R", "Ideia", None)])
cenario("tudo_coberto_no_ar", B, P1, [("P", "Outro", 0.1, 2, "E-mail", dia(2027, 4, 1), dia(2027, 5, 10), "R", "No ar", 5)])
cenario("planejadas_sem_ar", B, P1, [("P", "Outro", 0.1, 2, "E-mail", dia(2027, 4, 1), dia(2027, 5, 10), "R", "Preparando", None)])
cenario("sem_periodos", B, [], [])
cenario("periodo_de_um_dia", B, [("Feriado", dia(2027, 9, 7), dia(2027, 9, 7), 2)], [])

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EX), str(BR)]
               + [str(c[0]) for c in cen.values()], check=True, capture_output=True, timeout=900)
R = {n: load_workbook(OUTD / c[0].name, data_only=True) for n, c in cen.items()}
R["exemplo"] = load_workbook(OUTD / EX.name, data_only=True); R["branco"] = load_workbook(OUTD / BR.name, data_only=True)
cen["exemplo"] = (EX, EX_BASE, [(a, dt(b), dt(c), x) for a, b, c, x in EX_PER], [(c[0], c[1], c[2], c[3], c[4], dt(c[5]), dt(c[6])) + tuple(c[7:]) for c in EX_CAMP])
cen["branco"] = (BR, {}, [], [])

def igual(a, b, tol=1e-6):
    if a in (None, "") and b in (None, ""): return True
    if isnum(a) and isnum(b): return abs(a - b) < tol
    return a == b

def confere(nome):
    _, base, pers, camps = cen[nome]; bs, linhas, alertas, dcs, lqs, fats, painel, leit = referencia(base, pers, camps)
    w = R[nome]; pe, ca, p = w["Períodos"], w["Campanhas"], w["Painel"]; erros = []
    if w["Base"]["B12"].value != bs: erros.append(("base", bs, w["Base"]["B12"].value))
    for k, l in enumerate(linhas):
        if l is None: continue
        r = P0 + k
        for c, v in dict(E=l["disp"], F=l["oc"], G=l["s"], H=l["n"], I=l["v"]).items():
            if not igual(v, pe[f"{c}{r}"].value): erros.append((f"Períodos!{c}{r}", v, pe[f"{c}{r}"].value))
    for k, a in enumerate(alertas):
        r = C0 + k
        for c, v in dict(P=a, L=dcs[k], M=lqs[k], N=fats[k]).items():
            if not igual(v, ca[f"{c}{r}"].value): erros.append((f"Campanhas!{c}{r}", v, ca[f"{c}{r}"].value))
    for i, v in enumerate(painel):
        if not igual(v, p[f"B{4+i}"].value): erros.append((p[f"A{4+i}"].value, v, p[f"B{4+i}"].value))
    if p["A15"].value != leit: erros.append(("leitura", leit, p["A15"].value))
    return erros, alertas, painel

for nome in ["exemplo", "branco"] + [n for n in cen if n not in ("exemplo", "branco")]:
    erros, alertas, painel = confere(nome)
    log(not erros, f"{nome}: {painel[1]} períodos e {painel[4]} campanhas conferidos, {painel[5]} com alerta" + (f" | diferenças: {erros[:3]}" if erros else ""))

ca, p = R["exemplo"]["Campanhas"], R["exemplo"]["Painel"]
log(ca["P9"].value == "Abaixo do piso" and abs(ca["L9"].value - 273) < 1e-9, "exemplo: última hora com 35% dá R$ 273, abaixo do piso de R$ 300 (conta à mão: 420 × 0,65)")
log(abs(ca["M7"].value - (357 * 0.82 - 120 / 3)) < 1e-9, f"exemplo: estadia longa rende R$ {ca['M7'].value:.2f} líquidos por noite (conta à mão: 357 × 0,82 − 120 ÷ 3 = 252,74)")
log(R["piso_exato"]["Campanhas"]["P7"].value == "OK", "diária com desconto igual ao piso não recebe alerta")
log(R["estadia_minima_dilui_custo"]["Campanhas"]["P7"].value == "OK" and R["nao_cobre_custo"]["Campanhas"]["P7"].value == "Não cobre o custo",
    "custo de R$ 500: em 1 noite não cobre; com estadia mínima de 4 noites passa")
erros = [(n, ws.title, c.coordinate) for n, wb in R.items() for ws in wb for row in ws.iter_rows() for c in row
         if isinstance(c.value, str) and c.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(R)} arquivos" + (f" {erros[:4]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

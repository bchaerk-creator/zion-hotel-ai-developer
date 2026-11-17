"""Testa a Ferramenta 16 recalculando no LibreOffice e comparando com uma regra independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, random, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from dados import EX_HOJE, EX_PARC, EX_IND
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EX = D / "Parcerias-Zion-EM-BRANCO.xlsx", D / "Parcerias-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
P0, I0, NP, NI = 7, 7, 40, 300
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
dt = lambda s: datetime.date.fromisoformat(s) if isinstance(s, str) and len(s) == 10 and s[4] == "-" else s
VALIDAS = ("Aguardando confirmação", "A receber", "Recebido", "Sem comissão")

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)

def referencia(hoje, parcs, inds):
    """Regra escrita a partir da aba Comece aqui."""
    ps = {}
    for nome, tipo, cont, oferece, ben, contra, val, acordo, rev in parcs:
        if nome in (None, ""): continue
        if tipo in (None, ""): s = "Escolha o tipo"
        elif contra in (None, ""): s = "Escolha a contrapartida"
        elif contra in ("% sobre o valor", "Valor fixo por indicação") and (not isnum(val) or val <= 0 or (contra == "% sobre o valor" and val >= 1)):
            s = "Confira o valor da contrapartida"
        elif acordo != "Sim": s = "Sem acordo por escrito"
        elif isinstance(rev, datetime.date) and isinstance(hoje, datetime.date) and rev <= hoje: s = "Revisar o acordo"
        else: s = "Ativa"
        if nome not in ps: ps[nome] = dict(s=s, contra=contra, val=val if isnum(val) else 0)
    res = []
    for data, parc, cod, gasto, conf, rec in inds:
        if data is None and parc in (None, "") and cod in (None, ""): s = ""
        elif not isinstance(data, datetime.date): s = "Informe a data"
        elif parc in (None, "") or parc not in ps: s = "Parceiro não cadastrado"
        elif ps[parc]["s"] in ("Escolha o tipo", "Escolha a contrapartida", "Confira o valor da contrapartida"): s = "Complete o cadastro do parceiro"
        elif gasto not in (None, "") and (not isnum(gasto) or gasto < 0): s = "Confira o valor gasto"
        elif ps[parc]["contra"] == "% sobre o valor" and (not isnum(gasto) or gasto <= 0): s = "Informe o valor gasto"
        elif conf != "Sim": s = "Aguardando confirmação"
        elif ps[parc]["contra"] in ("Troca ou cortesia", "Nenhuma"): s = "Sem comissão"
        elif rec == "Sim": s = "Recebido"
        else: s = "A receber"
        com = None
        if s in VALIDAS:
            c, v = ps[parc]["contra"], ps[parc]["val"]
            com = gasto * v if c == "% sobre o valor" else v if c == "Valor fixo por indicação" else 0
        res.append((parc, s, com))
    agg = {}
    for nome in ps:
        mine = [x for x in res if x[0] == nome]
        agg[nome] = dict(n=sum(1 for x in mine if x[1] in VALIDAS), conf=sum(1 for x in mine if x[1] in VALIDAS[1:]),
                         arec=sum(x[2] for x in mine if x[1] == "A receber"), rec=sum(x[2] for x in mine if x[1] == "Recebido"))
    linhas_p = [p[0] for p in parcs if p[0]]
    pstat = [ps[n]["s"] for n in linhas_p]
    painel = [len(linhas_p), pstat.count("Ativa"), pstat.count("Sem acordo por escrito"), pstat.count("Revisar o acordo"),
              sum(1 for s in pstat if s.startswith(("Escolha", "Confira"))), sum(1 for x in res if x[1] in VALIDAS),
              sum(1 for x in res if x[1] == "Aguardando confirmação"), sum(1 for x in res if x[1] not in ("",) + VALIDAS),
              sum(x[2] for x in res if x[1] == "A receber"), sum(x[2] for x in res if x[1] == "Recebido")]
    if painel[0] == 0: leit = "Cadastre os parceiros"
    elif painel[4] > 0: leit = f"Complete o cadastro de {painel[4]} parceiro(s)"
    elif painel[7] > 0: leit = "Corrija as indicações com problema"
    elif painel[2] > 0: leit = f"Combine por escrito com {painel[2]} parceiro(s)"
    elif painel[3] > 0: leit = f"Revise {painel[3]} acordo(s)"
    elif painel[6] > 0: leit = f"Peça confirmação de {painel[6]} indicação(ões)"
    elif painel[8] > 0: leit = "Cobre dos parceiros a comissão a receber (valor acima)"
    else: leit = "Tudo em dia"
    return ps, res, agg, painel, leit

def cenario(nome, hoje, parcs, inds):
    wb = load_workbook(BR); pa, ind = wb["Parceiros"], wb["Indicações"]
    pa["B4"] = hoje
    for k, v in enumerate(parcs):
        for col, x in zip("ABCDEFGHI", v): pa[f"{col}{P0+k}"] = x
    for k, v in enumerate(inds):
        for col, x in zip("ABCDEF", v): ind[f"{col}{I0+k}"] = x
    p = TMP / f"{nome}.xlsx"; wb.save(p); cen[nome] = (p, hoje, parcs, inds)

def aleatorio(nome, seed, erros):
    rnd = random.Random(seed)
    hoje = datetime.date(2026, rnd.randint(1, 12), rnd.randint(1, 28))
    def esc(bons, ruins): return rnd.choice(ruins) if erros and rnd.random() < .08 else rnd.choice(bons)
    parcs = []
    for i in range(rnd.randint(1, 10)):
        contra = esc(["% sobre o valor", "Valor fixo por indicação", "Troca ou cortesia", "Nenhuma"], [None])
        val = (rnd.choice([0.05, 0.1, 0.15]) if contra == "% sobre o valor" else rnd.choice([10, 25, 40]) if contra == "Valor fixo por indicação" else None)
        val = esc([val], [0, 1.5, "dez", -3]) if contra else val
        parcs.append((f"P{seed}-{i}", esc(["Restaurante", "Outro"], [None]), "c", "o", "b", contra, val, esc(["Sim", "Sim", "Não"], [None]),
                      rnd.choice([None, hoje - datetime.timedelta(days=rnd.randint(0, 30)), hoje + datetime.timedelta(days=rnd.randint(1, 60)), hoje])))
    nomes = [p[0] for p in parcs]
    inds = [(esc([hoje - datetime.timedelta(days=rnd.randint(0, 60))], [None, "ontem"]), esc(nomes, ["Fora", None]), f"R{j}",
             esc([None, 120, 380.5, 75], [-10, "cem"]), rnd.choice(["Sim", "Sim", "Não", None]), rnd.choice(["Sim", "Não", None]))
            for j in range(rnd.randint(3, 60))]
    cenario(nome, hoje, parcs, inds)

for s in range(8): aleatorio(f"aleatorio_com_erros_{s}", 900 + s, True)
for s in range(4): aleatorio(f"aleatorio_limpo_{s}", 950 + s, False)
dia = datetime.date
H = dia(2026, 6, 10)
P = [("A", "Restaurante", "", "", "", "% sobre o valor", 0.1, "Sim", dia(2026, 6, 10)), ("B", "Outro", "", "", "", "Valor fixo por indicação", 30, "Sim", dia(2026, 6, 11))]
cenario("revisao_no_dia_exato", H, P, [])
cenario("porcentagem_99_e_100", H, [("A", "Restaurante", "", "", "", "% sobre o valor", 0.99, "Sim", None), ("B", "Restaurante", "", "", "", "% sobre o valor", 1, "Sim", None)],
        [(dia(2026, 6, 1), "A", "R1", 100, "Sim", None), (dia(2026, 6, 1), "B", "R2", 100, "Sim", None)])
cenario("tudo_em_dia", H, [P[1]], [(dia(2026, 6, 1), "B", "R1", None, "Sim", "Sim")])
cenario("so_falta_cobrar", H, [P[1]], [(dia(2026, 6, 1), "B", "R1", None, "Sim", None)])
cenario("so_falta_confirmar", H, [P[1]], [(dia(2026, 6, 1), "B", "R1", None, None, None)])
cenario("sem_parceiros", H, [], [])

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EX), str(BR)]
               + [str(c[0]) for c in cen.values()], check=True, capture_output=True, timeout=900)
R = {n: load_workbook(OUTD / c[0].name, data_only=True) for n, c in cen.items()}
R["exemplo"] = load_workbook(OUTD / EX.name, data_only=True); R["branco"] = load_workbook(OUTD / BR.name, data_only=True)
cen["exemplo"] = (EX, dt(EX_HOJE), [tuple(p[:8]) + (dt(p[8]),) for p in EX_PARC], [(dt(i[0]),) + tuple(i[1:]) for i in EX_IND])
cen["branco"] = (BR, None, [], [])

def igual(a, b, tol=1e-6):
    if a in (None, "") and b in (None, ""): return True
    if isnum(a) and isnum(b): return abs(a - b) < tol
    return a == b

def confere(nome):
    _, hoje, parcs, inds = cen[nome]
    w = R[nome]
    if nome == "branco": hoje = w["Parceiros"]["B4"].value
    if isinstance(hoje, datetime.datetime): hoje = hoje.date()
    ps, res, agg, painel, leit = referencia(hoje, parcs, inds)
    pa, ind, p = w["Parceiros"], w["Indicações"], w["Painel"]; erros = []
    for k, pr in enumerate(parcs):
        if not pr[0]: continue
        r = P0 + k; a = agg[pr[0]]
        for c, v in dict(J=ps[pr[0]]["s"], K=a["n"], L=a["conf"], M=a["arec"], N=a["rec"]).items():
            if not igual(v, pa[f"{c}{r}"].value): erros.append((f"Parceiros!{c}{r}", v, pa[f"{c}{r}"].value))
    for k, (parc, s, com) in enumerate(res):
        r = I0 + k
        for c, v in dict(H=s, G=com).items():
            if not igual(v, ind[f"{c}{r}"].value): erros.append((f"Indicações!{c}{r}", v, ind[f"{c}{r}"].value))
    for i, v in enumerate(painel):
        if not igual(v, p[f"B{4+i}"].value): erros.append((p[f"A{4+i}"].value, v, p[f"B{4+i}"].value))
    if p["A16"].value != leit: erros.append(("leitura", leit, p["A16"].value))
    return erros, painel

for nome in ["exemplo", "branco"] + [n for n in cen if n not in ("exemplo", "branco")]:
    erros, painel = confere(nome)
    log(not erros, f"{nome}: {painel[0]} parceiros e {painel[5] + painel[7]} indicações conferidos, {painel[7]} com problema" + (f" | diferenças: {erros[:3]}" if erros else ""))

pa, p = R["exemplo"]["Parceiros"], R["exemplo"]["Painel"]
log(abs(p["B12"].value - 96) < 1e-9 and abs(p["B13"].value - 63) < 1e-9, f"exemplo: R$ {p['B12'].value:.2f} a receber e R$ {p['B13'].value:.2f} recebidos (conta à mão: 26 + 25 + 45 = 96; 38 + 25 = 63)")
log(pa["J8"].value == "Revisar o acordo" and pa["J9"].value == "Sem acordo por escrito", "exemplo: acordo vencido em 15/11 pede revisão; spa sem acordo por escrito")
log(R["revisao_no_dia_exato"]["Parceiros"]["J7"].value == "Revisar o acordo" and R["revisao_no_dia_exato"]["Parceiros"]["J8"].value == "Ativa", "revisão no dia exato já pede revisar; no dia seguinte ainda não")
log(R["porcentagem_99_e_100"]["Parceiros"]["J8"].value == "Confira o valor da contrapartida" and abs(R["porcentagem_99_e_100"]["Indicações"]["G7"].value - 99) < 1e-9,
    "99% calcula; 100% é recusado e a indicação pede para completar o parceiro")
b = R["branco"]
log(isinstance(b["Parceiros"]["B4"].value, datetime.datetime) and b["Painel"]["A16"].value == "Cadastre os parceiros", "versão em branco: data de hoje automática e painel pede os parceiros")
erros = [(n, ws.title, c.coordinate) for n, wb in R.items() for ws in wb for row in ws.iter_rows() for c in row
         if isinstance(c.value, str) and c.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(R)} arquivos" + (f" {erros[:4]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

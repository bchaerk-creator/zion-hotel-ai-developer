"""Testa a Ferramenta 18 recalculando no LibreOffice e comparando com uma conta independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, random, datetime as dt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from dados import FREQ, SUGERIDAS, EX_HOJE, EX_AVISO, EX_PLANO, EX_REG, NP, P0, NR, R0
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EXF = D / "Manutencao-Preventiva-Zion-EM-BRANCO.xlsx", D / "Manutencao-Preventiva-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
FD = dict(FREQ); d = lambda s: dt.date.fromisoformat(s) if isinstance(s, str) else s
num = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)

def conta(hoje, aviso, plano, reg):
    """plano: lista de dict(u, a, t, f, dd, resp, ult, custo); reg: lista de (data, n, quem, obs)."""
    R = []
    validos = {i + 1 for i, x in enumerate(plano) if x["t"]}
    for i, x in enumerate(plano):
        n = i + 1
        if not x["t"]: R.append(None); continue
        iv = x["dd"] if num(x["dd"]) and x["dd"] > 0 else FD.get(x["f"])
        datas = [r[0] for r in reg if r[1] == n and isinstance(r[0], dt.date)] + ([x["ult"]] if x["ult"] else [])
        ult = max(datas) if datas else None
        prox = ult + dt.timedelta(days=iv) if (iv and ult) else None
        dias = (prox - hoje).days if (prox and hoje) else None
        if not iv: sit = "Escolha a frequência"
        elif not ult: sit = "Sem registro: faça e anote"
        elif not hoje: sit = "Informe a data de hoje"
        elif ult > hoje: sit = "Data futura: confira"
        elif dias < 0: sit = "Atrasada"
        elif dias <= (aviso or 0): sit = "Vence em breve"
        else: sit = "Em dia"
        custo = x["custo"] * 365 / iv if (iv and num(x["custo"])) else None
        R.append(dict(iv=iv, ult=ult, prox=prox, dias=dias, sit=sit, custo=custo))
    regs = []
    for data, n, quem, obs in reg:
        if data is None and n is None: regs.append(""); continue
        if not isinstance(data, dt.date): regs.append("Informe a data")
        elif n not in validos: regs.append("Nº não existe no Plano")
        elif hoje and data > hoje: regs.append("Data futura: confira")
        else: regs.append("OK")
    sits = [r["sit"] for r in R if r]
    cnt = lambda s: sits.count(s)
    dl = [r["dias"] for r in R if r and r["dias"] is not None]
    pan = dict(total=len(sits), atr=cnt("Atrasada"), breve=cnt("Vence em breve"), emdia=cnt("Em dia"), sem=cnt("Sem registro: faça e anote"),
               conf=cnt("Escolha a frequência") + cnt("Data futura: confira"),
               regconf=sum(regs.count(x) for x in ("Nº não existe no Plano", "Data futura: confira", "Informe a data")),
               urg=min(dl) if dl else None, custo=sum(r["custo"] for r in R if r and r["custo"] is not None))
    if pan["total"] == 0: leit = "Monte o plano na aba Plano"
    elif not hoje: leit = "Informe a data de hoje na aba Plano"
    elif pan["conf"]: leit = "Há linhas para conferir no Plano"
    elif pan["atr"]: leit = "Há tarefas atrasadas: comece por elas"
    elif pan["breve"]: leit = "Nada atrasado; programe as que vencem em breve"
    elif pan["emdia"] == 0 and pan["sem"]: leit = "Nenhuma tarefa anotada ainda: registre a primeira vez de cada uma"
    elif pan["sem"]: leit = "Em dia, mas há tarefas sem registro"
    else: leit = "Tudo em dia"
    pan["leit"] = leit
    return R, regs, pan

def P(u=None, a=None, t=None, f=None, dd=None, resp=None, ult=None, custo=None):
    return dict(u=u, a=a, t=t, f=f, dd=dd, resp=resp, ult=d(ult), custo=custo)

def cenario(nome, hoje, aviso, plano, reg):
    wb = load_workbook(BR); p, g = wb["Plano"], wb["Registro"]
    p["D4"], p["D5"] = hoje, aviso
    for i in range(NP):
        x = plano[i] if i < len(plano) else P()
        for col, k in zip("BCDEFGHI", ("u", "a", "t", "f", "dd", "resp", "ult", "custo")): p[f"{col}{P0+i}"] = x[k]
    for i, x in enumerate(reg):
        for col, v in zip("ABCD", x): g[f"{col}{R0+i}"] = v
    pth = TMP / f"{nome}.xlsx"; wb.save(pth); cen[nome] = (pth, hoje, aviso, plano, reg)

random.seed(18)
base = dt.date(2026, 11, 15)
def rdate(): return base + dt.timedelta(days=random.randint(-400, 3))
for k in range(10):
    plano = []
    for i in range(random.randint(5, 60)):
        plano.append(P(random.choice(["Chalé 1", "Casa", None]), "Área", random.choice([f"Tarefa {i}"] * 9 + [None]),
                       random.choice([n for n, _ in FREQ] + [None, "Outra coisa"]), random.choice([None] * 6 + [45, 120, 0, -3]),
                       "X", random.choice([None, rdate(), rdate()]), random.choice([None, random.randint(10, 900)])))
    reg = [(random.choice([rdate(), rdate(), None]), random.choice([random.randint(1, len(plano)), random.randint(1, len(plano)), 999, None]),
            "Y", "obs") for _ in range(random.randint(0, 40))]
    cenario(f"aleatorio_{k}", base + dt.timedelta(days=random.randint(-5, 5)), random.choice([0, 3, 7, 15, None]), plano, reg)
for k in range(5):
    plano = [P("U", "A", f"T{i}", random.choice([n for n, _ in FREQ]), None, "X", base - dt.timedelta(days=random.randint(0, 200)),
               random.choice([None, random.randint(10, 900)])) for i in range(random.randint(10, 100))]
    reg = [(base - dt.timedelta(days=random.randint(0, 60)), random.randint(1, len(plano)), "Y", "") for _ in range(random.randint(0, 150))]
    cenario(f"limpo_{k}", base, 7, plano, reg)
cenario("vazio", base, 7, [], [])
cenario("sem_frequencia", base, 7, [P(t="A", f=None, ult="2026-11-01"), P(t="B", f="Outra", ult="2026-11-01")], [])
cenario("dias_personalizados_vencem_hoje", base, 7, [P(t="Filtro", dd=45, ult="2026-10-01")], [])
cenario("registro_mais_recente_vence", base, 7, [P(t="Filtro", f="Mensal", ult="2026-09-01")], [(dt.date(2026, 11, 10), 1, "Ana", "")])
cenario("registro_mais_antigo_nao_muda", base, 7, [P(t="Filtro", f="Mensal", ult="2026-11-10")], [(dt.date(2026, 9, 1), 1, "Ana", "")])
cenario("data_futura", base, 7, [P(t="Filtro", f="Mensal", ult="2026-12-01")], [(dt.date(2026, 12, 2), 1, "Ana", "")])
cenario("aviso_limite", base, 7, [P(t="A", f="Semanal", ult="2026-11-15"), P(t="B", f="Semanal", ult="2026-11-14"), P(t="C", f="Diária", ult="2026-11-13")], [])
cenario("sem_data_de_hoje", None, 7, [P(t="A", f="Semanal", ult="2026-11-10")], [])
cenario("registro_sem_data_e_num_invalido", base, 7, [P(t="A", f="Semanal", ult="2026-11-10")], [(None, 1, "Ana", ""), (base, 5, "Ana", ""), (base, "abc", "Ana", "")])
cenario("tudo_em_dia", base, 7, [P(t="A", f="Anual", ult="2026-11-01", custo=365), P(t="B", f="Semestral", ult="2026-10-01")], [])

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EXF), str(BR)]
               + [str(c[0]) for c in cen.values()], check=True, capture_output=True, timeout=900)
W = {n: load_workbook(OUTD / c[0].name, data_only=True) for n, c in cen.items()}
W["exemplo"] = load_workbook(OUTD / EXF.name, data_only=True); W["branco"] = load_workbook(OUTD / BR.name, data_only=True)
cen["exemplo"] = (EXF, d(EX_HOJE), EX_AVISO, [P(*x) for x in EX_PLANO], [(d(a), b, c, e) for a, b, c, e in EX_REG])

def dval(v): return v.date() if isinstance(v, dt.datetime) else v
def igual(a, b):
    b = dval(b)
    if num(a) and num(b): return abs(a - b) < 1e-6
    return a == b or (a in ("", None) and b in ("", None))

for nome, (_, hoje, aviso, plano, reg) in cen.items():
    R, regs, pan = conta(hoje, aviso, plano, reg); w = W[nome]; p, g, s = w["Plano"], w["Registro"], w["Painel"]; erros = []
    for i in range(NP):
        r = P0 + i; ref = R[i] if i < len(R) else None
        got = dict(iv=p[f"J{r}"].value, ult=p[f"K{r}"].value, prox=p[f"L{r}"].value, sit=p[f"M{r}"].value, custo=p[f"N{r}"].value, dias=p[f"O{r}"].value)
        for k in got:
            esp = ref[k] if ref else None
            if not igual(esp, got[k]): erros.append((f"linha {r} {k}", esp, dval(got[k])))
    for i, esp in enumerate(regs):
        if not igual(esp, g[f"F{R0+i}"].value): erros.append((f"registro {R0+i}", esp, g[f"F{R0+i}"].value))
    for l, k in ((5, "total"), (6, "atr"), (7, "breve"), (8, "emdia"), (9, "sem"), (10, "conf"), (11, "regconf"), (12, "urg"), (14, "custo"), (15, "leit")):
        if not igual(pan[k], s[f"B{l}"].value): erros.append((f"painel {k}", pan[k], s[f"B{l}"].value))
    log(not erros, f"{nome}: {pan['leit']} | atrasadas {pan['atr']}, em breve {pan['breve']}, em dia {pan['emdia']}, sem registro {pan['sem']}" + (f" | {erros[:3]}" if erros else ""))

s, p = W["exemplo"]["Painel"], W["exemplo"]["Plano"]
log([s[f"B{l}"].value for l in (5, 6, 7, 8, 9)] == [16, 2, 4, 9, 1] and abs(s["B14"].value - 4731.375) < 1e-6 and s["B12"].value == -7,
    f"exemplo conferido à mão: 16 tarefas, 2 atrasadas, 4 em breve, 9 em dia, 1 sem registro; mais urgente −7 dias (gás); custo anual R$ {s['B14'].value:,.2f} (4.731,38)")
log(dval(p["K10"].value) == dt.date(2026, 11, 12) and p["M10"].value == "Em dia" and dval(p["L23"].value) == dt.date(2026, 11, 22),
    "exemplo: o Registro de 12/11 atualiza o filtro do Chalé 2 (era 28/10) e o refil de 120 dias vence em 22/11")
log(W["exemplo"]["Registro"]["F9"].value == "Nº não existe no Plano" and W["exemplo"]["Registro"]["E9"].value in ("", None),
    "exemplo: registro com nº 99 é marcado para conferir")
b = W["branco"]["Painel"]
log(b["B5"].value == len(SUGERIDAS) and b["B9"].value == len(SUGERIDAS) and b["B15"].value.startswith("Nenhuma tarefa anotada"),
    f"versão em branco: {len(SUGERIDAS)} tarefas sugeridas, todas sem registro, sem erro")
erros = [(n, ws.title, cc.coordinate) for n, wb in W.items() for ws in wb for row in ws.iter_rows() for cc in row
         if isinstance(cc.value, str) and cc.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(W)} arquivos" + (f" {erros[:4]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

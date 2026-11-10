"""Testa a Ferramenta 20 recalculando no LibreOffice e comparando com uma conta independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, random, datetime as dt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from dados import ETAPAS, SUGERIDAS, EX, EX_DATAS, NT, T0
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EXF = D / "Treinamento-Primeiro-Turno-Zion-EM-BRANCO.xlsx", D / "Treinamento-Primeiro-Turno-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
d = lambda s: dt.date.fromisoformat(s) if isinstance(s, str) else s
CONF = ("Datas fora de ordem: confira", "Data futura: confira", "Falta quem conferiu")

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)

def linha(x, inicio, hoje):
    if not x["t"]: return None
    f, g, h = x["f"], x["g"], x["h"]
    prazo = inicio + dt.timedelta(days=x["pz"]) if (inicio and isinstance(x["pz"], (int, float))) else None
    passo = "Fez sozinha" if h else ("Feito junto" if g else ("Mostrado" if f else "Nenhum"))
    ordem = (g and not f) or (h and (not f or not g)) or (f and g and g < f) or (g and h and h < g)
    fut = hoje and any(v and v > hoje for v in (f, g, h))
    if ordem: s = "Datas fora de ordem: confira"
    elif fut: s = "Data futura: confira"
    elif h and not x["quem"]: s = "Falta quem conferiu"
    elif h: s = "Pronta"
    elif prazo and hoje and hoje > prazo: s = "Atrasada"
    elif g: s = "Feita junto"
    elif f: s = "Mostrada"
    else: s = "Não começou"
    return dict(prazo=prazo, sit=s, passo=passo)

def conta(inicio, hoje, linhas):
    R = [linha(x, inicio, hoje) for x in linhas]
    vals = [(x, r) for x, r in zip(linhas, R) if r]
    tot = len(vals); prontas = sum(r["sit"] == "Pronta" for _, r in vals)
    ob = sum(x["ob"] == "Sim" for x, _ in vals); obok = sum(x["ob"] == "Sim" and r["sit"] == "Pronta" for x, r in vals)
    atr = sum(r["sit"] == "Atrasada" for _, r in vals); conf = sum(r["sit"] in CONF for _, r in vals)
    prox = next((x["t"] for x, r in vals if r["sit"] != "Pronta"), "")
    if tot == 0: lib = "Monte o plano na aba Treinamento"
    elif ob == 0: lib = "Marque quais tarefas são obrigatórias"
    elif conf: lib = "Ainda não: há linhas para conferir"
    elif ob - obok == 0: lib = "Sim: todas as obrigatórias prontas"
    else: lib = f"Ainda não: faltam {ob - obok} obrigatórias"
    pct = (obok / ob) if ob else None
    etapas = [f"{sum(x['e'] == e for x, _ in vals)} · {sum(x['e'] == e and r['sit'] == 'Pronta' for x, r in vals)}" for e in ETAPAS]
    return dict(R=R, tot=tot, prontas=prontas, ob=ob, obok=obok, falta=ob - obok, pct=pct, atr=atr, conf=conf, prox=prox, lib=lib, etapas=etapas)

def L(e=None, t=None, ob=None, pz=None, f=None, g=None, h=None, quem=None):
    return dict(e=e, t=t, ob=ob, pz=pz, f=d(f), g=d(g), h=d(h), quem=quem)

def cenario(nome, inicio, hoje, linhas):
    wb = load_workbook(BR); t = wb["Treinamento"]
    t["C6"], t["C8"] = inicio, hoje
    for i in range(NT):
        x = linhas[i] if i < len(linhas) else L()
        for col, k in zip("BCDEFGHI", ("e", "t", "ob", "pz", "f", "g", "h", "quem")): t[f"{col}{T0+i}"] = x[k]
    pth = TMP / f"{nome}.xlsx"; wb.save(pth); cen[nome] = (pth, inicio, hoje, linhas)

random.seed(20)
base = dt.date(2026, 11, 2)
def rd(): return random.choice([None, base + dt.timedelta(days=random.randint(0, 9))])
for k in range(10):
    lin = []
    for i in range(random.randint(3, 60)):
        f = rd(); g = rd() if random.random() < .7 else None; h = rd() if random.random() < .6 else None
        lin.append(L(random.choice(ETAPAS + [None]), random.choice([f"Tarefa {i}"] * 8 + [None]), random.choice(["Sim", "Não", None]),
                     random.choice([None, 0, 1, 3, 7]), f, g, h, random.choice([None, "Ana"])))
    cenario(f"aleatorio_{k}", random.choice([base, None]), random.choice([base + dt.timedelta(days=random.randint(0, 10)), None]), lin)
for k in range(5):
    lin = []
    for i in range(random.randint(10, 60)):
        st = random.randint(0, 3); f = base + dt.timedelta(days=random.randint(0, 2))
        g = f + dt.timedelta(days=random.randint(0, 2)) if st >= 2 else None
        h = g + dt.timedelta(days=random.randint(0, 2)) if st >= 3 else None
        lin.append(L(random.choice(ETAPAS), f"T{i}", random.choice(["Sim", "Não"]), random.randint(0, 7), f if st >= 1 else None, g, h, "Ana" if h else None))
    cenario(f"limpo_{k}", base, base + dt.timedelta(days=8), lin)
cenario("vazio", base, base, [])
cenario("sem_obrigatorias", base, base, [L(ETAPAS[0], "A", "Não", 0)])
cenario("tudo_pronto", base, base + dt.timedelta(days=5), [L(ETAPAS[0], "A", "Sim", 0, "2026-11-02", "2026-11-02", "2026-11-03", "Ana"), L(ETAPAS[1], "B", "Não", 1)])
cenario("falta_quem_conferiu", base, base + dt.timedelta(days=5), [L(ETAPAS[0], "A", "Sim", 0, "2026-11-02", "2026-11-02", "2026-11-03", None)])
cenario("pulou_passo", base, base + dt.timedelta(days=5), [L(ETAPAS[0], "A", "Sim", 0, None, "2026-11-02", None)])
cenario("data_futura", base, base, [L(ETAPAS[0], "A", "Sim", 0, "2026-11-04")])
cenario("prazo_hoje_nao_atrasa", base + dt.timedelta(days=0), base + dt.timedelta(days=3), [L(ETAPAS[0], "A", "Sim", 3, "2026-11-02")])
cenario("prazo_ontem_atrasa", base, base + dt.timedelta(days=4), [L(ETAPAS[0], "A", "Sim", 3, "2026-11-02", "2026-11-03")])
cenario("sem_inicio_sem_hoje", None, None, [L(ETAPAS[0], "A", "Sim", 3, "2026-11-02")])

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EXF), str(BR)]
               + [str(c[0]) for c in cen.values()], check=True, capture_output=True, timeout=900)
W = {n: load_workbook(OUTD / c[0].name, data_only=True) for n, c in cen.items()}
W["exemplo"] = load_workbook(OUTD / EXF.name, data_only=True); W["branco"] = load_workbook(OUTD / BR.name, data_only=True)
ex_lin = [L(ETAPAS[e - 1], t, ob, pz, *EX_DATAS[i]) for i, (e, t, ob, pz) in enumerate(SUGERIDAS)]
cen["exemplo"] = (EXF, d(EX["inicio"]), d(EX["hoje"]), ex_lin)
cen["branco"] = (BR, None, dt.date.today(), [L(ETAPAS[e - 1], t, ob, pz) for e, t, ob, pz in SUGERIDAS])

def dv(v): return v.date() if isinstance(v, dt.datetime) else v
def igual(a, b):
    b = dv(b)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)): return abs(a - b) < 1e-9
    return a == b or (a in ("", None) and b in ("", None))

for nome, (_, inicio, hoje, linhas) in cen.items():
    ref = conta(inicio, hoje, linhas); w = W[nome]; t, s = w["Treinamento"], w["Painel"]; erros = []
    for i in range(NT):
        r = T0 + i; e = ref["R"][i] if i < len(linhas) else None
        for k, col in (("prazo", "J"), ("sit", "K"), ("passo", "L")):
            esp = e[k] if e else None
            if not igual(esp, t[f"{col}{r}"].value): erros.append((f"linha {r} {k}", esp, dv(t[f"{col}{r}"].value)))
    for l, k in ((5, "tot"), (6, "prontas"), (7, "ob"), (8, "obok"), (9, "falta"), (10, "pct"), (11, "atr"), (12, "conf"), (13, "prox"), (14, "lib")):
        if not igual(ref[k], s[f"B{l}"].value): erros.append((f"painel {k}", ref[k], s[f"B{l}"].value))
    for j, v in enumerate(ref["etapas"]):
        if not igual(v, s[f"B{18+j}"].value): erros.append((f"etapa {j+1}", v, s[f"B{18+j}"].value))
    log(not erros, f"{nome}: {ref['lib']} | prontas {ref['prontas']}/{ref['tot']}, atrasadas {ref['atr']}" + (f" | {erros[:3]}" if erros else ""))

s = W["exemplo"]["Painel"]
log([s[f"B{l}"].value for l in (5, 6, 7, 8, 11, 12)] == [16, 6, 14, 6, 4, 1] and s["B14"].value == "Ainda não: há linhas para conferir",
    "exemplo conferido à mão: 16 tarefas, 6 prontas, 14 obrigatórias (6 prontas), 4 atrasadas, 1 com datas fora de ordem, ainda não liberada")
log(W["exemplo"]["Treinamento"]["K22"].value == "Datas fora de ordem: confira",
    "exemplo: a ocorrência com 'fez sozinha' antes de 'feito junto' é marcada para conferir")
b = W["branco"]["Painel"]
log(b["B5"].value == len(SUGERIDAS) and b["B14"].value == f"Ainda não: faltam {sum(x[2] == 'Sim' for x in SUGERIDAS)} obrigatórias",
    f"versão em branco: {len(SUGERIDAS)} tarefas sugeridas, nenhuma pronta, sem erro")
erros = [(n, ws.title, cc.coordinate) for n, wb in W.items() for ws in wb for row in ws.iter_rows() for cc in row
         if isinstance(cc.value, str) and cc.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(W)} arquivos" + (f" {erros[:4]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

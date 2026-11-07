"""Testa a Ferramenta 14 recalculando no LibreOffice e comparando com uma regra independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, datetime, random
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from dados import PRIORIDADES, EX_UNIDADES, EX_RESP, EX_REF, EX_OC
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EX = D / "Quadro-Ocorrencias-Zion-EM-BRANCO.xlsx", D / "Quadro-Ocorrencias-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
O0, U0 = 6, 5
dt = lambda s: datetime.date.fromisoformat(s) if isinstance(s, str) else s
DIAS = dict(PRIORIDADES)

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)

def regra(oc, ref):
    """oc: dict com aberta, unidade, prioridade, resp, prazo, bloqueia, resolvida, como, custo. Devolve (prazo_usado, situacao, dias)."""
    ab, res = oc["aberta"], oc["resolvida"]
    prazo = oc["prazo"] if oc["prazo"] else (ab + datetime.timedelta(days=DIAS.get(oc["prioridade"], 0)) if ab and oc["prioridade"] else None)
    if res and ab and res < ab: sit = "Confira as datas"
    elif res: sit = "Fechada" if oc["como"] else "Fechada sem descrição"
    elif not (oc["unidade"] and oc["prioridade"] and oc["resp"] and ab): sit = "Complete os dados"
    elif prazo and prazo < ref: sit = "Atrasada"
    else: sit = "Aberta"
    dias = None if not ab else ((res - ab).days if res else (ref - ab).days)
    return prazo, sit, dias

def painel(ocs, unidades, ref):
    out = {}
    for u in unidades:
        sits = [(o, regra(o, ref)[1]) for o in ocs if o["unidade"] == u]
        aberto = [o for o, s in sits if s in ("Aberta", "Atrasada", "Complete os dados")]
        out[u] = dict(abertas=len(aberto), atrasadas=sum(1 for _, s in sits if s == "Atrasada"),
                      bloq=sum(1 for o in aberto if o["bloqueia"] == "Sim"), fechadas=sum(1 for _, s in sits if s.startswith("Fechada")),
                      custo=sum(o["custo"] or 0 for o in ocs if o["unidade"] == u))
        out[u]["sit"] = "BLOQUEADA" if out[u]["bloq"] else "Liberada"
    return out

def ex_ocs():
    return [dict(aberta=dt(a), unidade=u, prioridade=p, resp=r, prazo=dt(pz), bloqueia=b, resolvida=dt(rs), como=c, custo=cu)
            for a, u, _l, _o, p, r, pz, b, _e, rs, c, cu in EX_OC]

def cenario(nome, unidades, resps, ocs, ref):
    wb = load_workbook(BR); a, c, o = wb["Ajustes"], wb["Cadastros"], wb["Ocorrências"]
    a["B5"] = ref
    for i, u in enumerate(unidades): c[f"A{U0+i}"] = u
    for i, r in enumerate(resps): c[f"C{U0+i}"] = r
    for k, x in enumerate(ocs):
        r = O0 + k
        for col, key in zip("BCFGHJLMN", ("aberta", "unidade", "prioridade", "resp", "prazo", "bloqueia", "resolvida", "como", "custo")): o[f"{col}{r}"] = x[key]
        o[f"E{r}"] = f"Problema {k+1}"
    p = TMP / f"{nome}.xlsx"; wb.save(p); cen[nome] = (p, unidades, ocs, ref)

random.seed(14)
base = datetime.date(2026, 11, 1)
for k in range(6):
    us, rs = [f"U{k}-{i}" for i in range(random.randint(2, 5))], ["Resp A", "Resp B"]
    ocs = []
    for i in range(random.randint(4, 25)):
        ab = base + datetime.timedelta(days=random.randint(0, 10)) if random.random() > .05 else None
        res = (ab + datetime.timedelta(days=random.randint(-1, 6))) if ab and random.random() < .4 else None
        ocs.append(dict(aberta=ab, unidade=random.choice(us + [None] if random.random() < .1 else us), prioridade=random.choice([p for p, _ in PRIORIDADES] + ([None] if random.random() < .1 else [])),
                        resp=random.choice(rs + ([None] if random.random() < .1 else [])), prazo=(base + datetime.timedelta(days=random.randint(0, 15))) if random.random() < .3 else None,
                        bloqueia=random.choice(["Sim", "Não", None]), resolvida=res, como=random.choice(["Trocado", None]) if res else None, custo=random.choice([None, 50, 120.5])))
    cenario(f"aleatorio_{k}", us, rs, ocs, base + datetime.timedelta(days=random.randint(3, 14)))

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EX), str(BR)]
               + [str(c[0]) for c in cen.values()], check=True, capture_output=True, timeout=600)
R = {n: load_workbook(OUTD / c[0].name, data_only=True) for n, c in cen.items()}
R["exemplo"] = load_workbook(OUTD / EX.name, data_only=True); R["branco"] = load_workbook(OUTD / BR.name, data_only=True)
cen["exemplo"] = (EX, EX_UNIDADES, ex_ocs(), dt(EX_REF))
asdate = lambda v: v.date() if isinstance(v, datetime.datetime) else (None if v in ("", None) else v)

for nome in ["exemplo"] + [n for n in cen if n != "exemplo"]:
    _, unidades, ocs, ref = cen[nome]; o, p = R[nome]["Ocorrências"], R[nome]["Painel"]; erros = []
    for k, x in enumerate(ocs):
        r = O0 + k; prazo, sit, dias = regra(x, ref)
        got = (asdate(o[f"I{r}"].value), o[f"O{r}"].value, o[f"P{r}"].value if o[f"P{r}"].value != "" else None)
        if got != (prazo, sit, dias): erros.append((k + 1, (prazo, sit, dias), got))
    pref = painel(ocs, unidades, ref)
    for i, u in enumerate(unidades):
        r = 7 + i; e = pref[u]
        got = dict(abertas=p[f"B{r}"].value, atrasadas=p[f"C{r}"].value, bloq=p[f"D{r}"].value, fechadas=p[f"E{r}"].value, custo=p[f"F{r}"].value, sit=p[f"G{r}"].value)
        if any(abs(got[kk] - e[kk]) > 1e-6 if isinstance(e[kk], (int, float)) else got[kk] != e[kk] for kk in e): erros.append((u, e, got))
    log(not erros, f"{nome}: {len(ocs)} ocorrências e {len(unidades)} unidades conferidas" + (f" | {erros[:2]}" if erros else ""))

o, p = R["exemplo"]["Ocorrências"], R["exemplo"]["Painel"]
log([o[f"O{O0+k}"].value for k in range(6)] == ["Fechada", "Atrasada", "Atrasada", "Aberta", "Fechada sem descrição", "Complete os dados"],
    f"exemplo: situações {[o[f'O{O0+k}'].value for k in range(6)]}")
log(p["B3"].value == 4 and p["D3"].value == 2 and p["G3"].value == 1 and p["B4"].value == 1 and abs(p["D4"].value - 97) < 1e-6,
    f"painel do exemplo: {p['B3'].value} abertas, {p['D3'].value} atrasadas, {p['G3'].value} unidade bloqueada, {p['B4'].value} a completar, custo R$ {p['D4'].value}")
log(p["G10"].value == "BLOQUEADA" and p["G7"].value == "Liberada", "Suíte Jardim bloqueada (fechadura urgente aberta); Cabana 1 liberada (chuveiro já resolvido)")
log(p["A2"].value == "Situação em 07/11/2026", f"data do painel sem depender do idioma: {p['A2'].value}")
log(R["branco"]["Painel"]["B3"].value == 0 and R["branco"]["Painel"]["G3"].value == 0, "versão em branco: painel zerado, sem erro")
erros = [(n, ws.title, c.coordinate) for n, wb in R.items() for ws in wb for row in ws.iter_rows() for c in row
         if isinstance(c.value, str) and c.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(R)} arquivos" + (f" {erros[:4]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

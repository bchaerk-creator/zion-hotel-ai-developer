"""Testa a Ferramenta 05 recalculando no LibreOffice e comparando com uma conta independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, random
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from dados import ETAPAS, EX, ITENS, NL, L0, NMES
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EXF = D / "Orcamento-Cabana-Zion-EM-BRANCO.xlsx", D / "Orcamento-Cabana-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
E0, R0 = 5, 19
num = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)

def linha(L):
    """Regra independente para uma linha: devolve (preço, total, diferença, situação, falta)."""
    et, item, q, cs, h, pago = L["et"], L["item"], L["q"], L["cs"], L["h"], L["pago"]
    if not item: return None, None, None, "", None
    vals = [c for c in cs if num(c)]
    neg = any(num(x) and x < 0 for x in [q, pago, *cs])
    hok = h is None or h in (1, 2, 3)
    if not et: return None, None, None, "Escolha a etapa", None
    preco = None
    if not neg and vals and hok:
        preco = min(vals) if h is None else (cs[h - 1] if num(cs[h - 1]) else None)
    total = None if preco is None else preco * (q if num(q) else 1)
    dif = (max(vals) / min(vals) - 1) if (preco is not None and len(vals) >= 2 and min(vals) > 0) else None
    if neg: sit = "Valor negativo: confira"
    elif not hok: sit = "Escolhida deve ser 1, 2 ou 3"
    elif num(q) and q == 0: sit = "Não se aplica"
    elif not vals: sit = "Sem cotação"
    elif preco is None: sit = "Cotação escolhida vazia"
    elif (pago or 0) > total + 0.005: sit = "Pago acima do orçado"
    elif len(vals) == 1 and h is None: sit = "Só 1 cotação: peça mais"
    else: sit = "OK"
    return preco, total, dif, sit, (None if total is None else total - (pago or 0))

def conta(cfg, linhas):
    R = [linha(L) for L in linhas]
    sub = sum(r[1] for r in R if r[1] is not None); res = sub * (cfg["reserva"] or 0) / 100; tot = sub + res
    tem = any(r[1] is not None for r in R); verba = cfg["verba"]
    dif = (verba - tot) if (num(verba) and tem) else None
    if not tem: leit = "Ainda não há itens com cotação"
    elif not num(verba) or verba <= 0: leit = "Informe a verba disponível"
    else: leit = "Cabe na verba" if round(dif, 2) >= 0 else "Passa da verba: corte, troque ou adie itens"
    area, deck = cfg["area"], cfg["deck"]
    m2 = tot / area if (num(area) and area > 0 and tot != 0) else None
    m2t = tot / (area + max(0, deck or 0)) if m2 is not None else None
    sits = [r[3] for r in R]
    sem, um = sits.count("Sem cotação"), sits.count("Só 1 cotação: peça mais")
    conf = sum(sits.count(x) for x in ("Escolha a etapa", "Valor negativo: confira", "Escolhida deve ser 1, 2 ou 3", "Cotação escolhida vazia", "Pago acima do orçado"))
    falta = sum(r[4] for r in R if r[4] is not None)
    if (cfg["reserva"] or 0) < 0: sg = "Reserva não pode ser negativa"
    elif conf: sg = "Há linhas para conferir na coluna Situação"
    elif not tem: sg = "Ainda não há itens com cotação"
    elif sem: sg = "Incompleto: há itens sem cotação"
    elif um: sg = "Completo, mas há itens com só 1 cotação"
    else: sg = "Completo: todos os itens com cotação"
    etapas = [sum(r[1] for r, L in zip(R, linhas) if r[1] is not None and L["et"] == e) for e in ETAPAS]
    meses = [sum(r[1] for r, L in zip(R, linhas) if r[1] is not None and L["mes"] == m) for m in range(1, NMES + 1)]
    return dict(R=R, sub=sub, res=res, tot=tot, verba=verba if num(verba) else None, dif=dif, leit=leit, m2=m2, m2t=m2t, sem=sem, um=um, conf=conf,
                pago=sub - falta, falta=falta + res, sg=sg, etapas=etapas, fora=sub - sum(etapas), meses=meses, semmes=sub - sum(meses))

def L(et=None, item=None, q=None, cs=(None, None, None), h=None, pago=None, mes=None):
    return dict(et=et, item=item, q=q, cs=list(cs), h=h, pago=pago, mes=mes)

def cenario(nome, cfg, linhas):
    wb = load_workbook(BR); o = wb["Orçamento"]
    for k, cel in (("nome", "C4"), ("area", "C5"), ("deck", "C6"), ("reserva", "C7"), ("verba", "C8")): o[cel] = cfg.get(k)
    for i in range(NL):
        r = L0 + i; x = linhas[i] if i < len(linhas) else L()
        for col, v in zip("ABDEFGHMO", [x["et"], x["item"], x["q"], *x["cs"], x["h"], x["pago"], x["mes"]]): o[f"{col}{r}"] = v
    pth = TMP / f"{nome}.xlsx"; wb.save(pth); cen[nome] = (pth, cfg, linhas)

ex_cfg = dict(nome=EX["nome"], area=EX["area"], deck=EX["deck"], reserva=EX["reserva"], verba=EX["verba"])
ex_lin = [L(ETAPAS[e - 1], it, q, (c1, c2, c3), h, p, m) for e, it, esp, q, c1, c2, c3, h, p, m in ITENS]
br_lin = [L(ETAPAS[e - 1], it) for e, it, *_ in ITENS]
base = dict(nome="Teste", area=25, deck=10, reserva=10, verba=100000)

random.seed(5)
def rnd_val(): return random.choice([None, random.randint(100, 20000), round(random.uniform(50, 3000), 2)])
for k in range(10):
    lin = []
    for i in range(random.randint(5, 70)):
        lin.append(L(random.choice(ETAPAS + [None] * 1 if random.random() < .05 else ETAPAS), random.choice([f"Item {i}", f"Item {i}", None]) or None,
                     random.choice([None, 1, 2, random.randint(1, 40), 0]), (rnd_val(), rnd_val(), rnd_val()), random.choice([None, None, None, 1, 2, 3]),
                     random.choice([None, None, random.randint(0, 5000)]), random.choice([None, random.randint(1, 12), 13])))
    cenario(f"aleatorio_{k}", dict(nome="A", area=random.choice([None, 0, random.randint(15, 80)]), deck=random.choice([None, 0, random.randint(1, 30)]),
                                    reserva=random.choice([0, 5, 10, 15, None]), verba=random.choice([None, 0, random.randint(20000, 400000)])), lin)
for k in range(6):                       # cenários "limpos": linhas válidas e verba informada
    lin = []
    for i in range(random.randint(10, 80)):
        cs = [random.randint(50, 30000) for _ in range(random.randint(1, 3))] + [None] * 3
        cs = cs[:3]; h = random.choice([None, None] + [j + 1 for j in range(3) if cs[j] is not None])
        lin.append(L(random.choice(ETAPAS), f"Item {i}", random.choice([None, 1, random.randint(1, 40)]), cs, h, None, random.choice([None, random.randint(1, 12)])))
    cenario(f"limpo_{k}", dict(nome="L", area=random.randint(15, 80), deck=random.randint(0, 30), reserva=random.choice([0, 5, 10, 15]),
                                verba=random.randint(50000, 3000000)), lin)
cenario("etapa_vazia", base, [L(None, "Sem etapa", 1, (1000, None, None))])
cenario("negativo", base, [L(ETAPAS[0], "Neg", 1, (1000, -5, None))])
cenario("escolhida_invalida", base, [L(ETAPAS[0], "H4", 1, (1000, 900, 800), 4)])
cenario("escolhida_vazia", base, [L(ETAPAS[0], "H3 vazio", 1, (1000, 900, None), 3)])
cenario("pago_acima", base, [L(ETAPAS[0], "Pago", 1, (1000, 1100, None), None, 1500, 2)])
cenario("nao_se_aplica", base, [L(ETAPAS[0], "Zero", 0, (1000, None, None)), L(ETAPAS[1], "Um", 2, (500, 400, 450), None, None, 1)])
cenario("etapa_fora_da_lista", base, [L("Outra coisa", "Fora", 1, (1000, 1200, None), None, None, 1), L(ETAPAS[2], "Dentro", 1, (500, 600, None))])
cenario("cabe_exato", dict(base, verba=1100, reserva=10), [L(ETAPAS[0], "Exato", 1, (1000, 1050, None), None, None, 1)])
cenario("sem_verba_sem_area", dict(base, verba=None, area=None), [L(ETAPAS[0], "A", 3, (200, 250, None), 2, 100, 3)])
cenario("reserva_negativa", dict(base, reserva=-5), [L(ETAPAS[0], "A", 1, (200, 250, None))])
cenario("cotacao_unica_escolhida", base, [L(ETAPAS[0], "Taxa", 1, (1800, None, None), 1, None, 1)])

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EXF), str(BR)]
               + [str(c[0]) for c in cen.values()], check=True, capture_output=True, timeout=600)
RW = {n: load_workbook(OUTD / c[0].name, data_only=True) for n, c in cen.items()}
RW["exemplo"] = load_workbook(OUTD / EXF.name, data_only=True); RW["branco"] = load_workbook(OUTD / BR.name, data_only=True)
cen["exemplo"] = (EXF, ex_cfg, ex_lin); cen["branco"] = (BR, dict(nome=None, area=None, deck=None, reserva=10, verba=None), br_lin)

def igual(a, b):
    if num(a) and num(b): return abs(a - b) < 1e-6
    return a == b or (a in ("", None) and b in ("", None))

for nome, (_, cfg, linhas) in cen.items():
    ref = conta(cfg, linhas); w = RW[nome]; o, s, c = w["Orçamento"], w["Resumo"], w["Cronograma"]; erros = []
    for i in range(NL):
        r = L0 + i; esp = ref["R"][i] if i < len(linhas) else (None, None, None, "", None)
        got = [o[f"{x}{r}"].value for x in "IJKLN"]
        for k, (a, b) in enumerate(zip(esp, got)):
            if not igual(a, b): erros.append((f"linha {r} col {'IJKLN'[k]}", a, b))
    chaves = [(R0, "sub"), (R0 + 1, "res"), (R0 + 2, "tot"), (R0 + 3, "verba"), (R0 + 4, "dif"), (R0 + 5, "leit"), (R0 + 6, "m2"), (R0 + 7, "m2t"),
              (R0 + 8, "sem"), (R0 + 9, "um"), (R0 + 10, "conf"), (R0 + 11, "pago"), (R0 + 12, "falta"), (R0 + 13, "sg")]
    for l, k in chaves:
        if not igual(ref[k], s[f"B{l}"].value): erros.append((k, ref[k], s[f"B{l}"].value))
    for j, v in enumerate(ref["etapas"]):
        if not igual(v, s[f"B{E0+j}"].value): erros.append((f"etapa {j+1}", v, s[f"B{E0+j}"].value))
    if not igual(ref["fora"], s["B15"].value): erros.append(("fora da lista", ref["fora"], s["B15"].value))
    for j, v in enumerate(ref["meses"]):
        if not igual(v, c[f"B{5+j}"].value): erros.append((f"mês {j+1}", v, c[f"B{5+j}"].value))
    if not igual(ref["semmes"], c[f"B{5+NMES}"].value): erros.append(("sem mês", ref["semmes"], c[f"B{5+NMES}"].value))
    if not igual(ref["tot"], c[f"B{7+NMES}"].value): erros.append(("total cronograma", ref["tot"], c[f"B{7+NMES}"].value))
    if not igual(ref["falta"], c[f"D{7+NMES}"].value): erros.append(("falta cronograma", ref["falta"], c[f"D{7+NMES}"].value))
    log(not erros, f"{nome}: {ref['sg']} | {ref['leit']}" + (f" | {erros[:3]}" if erros else ""))

s = RW["exemplo"]["Resumo"]
log(s[f"B{R0}"].value == 197040 and s[f"B{R0+2}"].value == 216744 and s[f"B{R0+4}"].value == -16744,
    f"exemplo conferido à mão: subtotal R$ {s[f'B{R0}'].value:,.2f} (197.040), total com reserva R$ {s[f'B{R0+2}'].value:,.2f} (216.744), diferença R$ {s[f'B{R0+4}'].value:,.2f} (−16.744)")
o = RW["exemplo"]["Orçamento"]
log(o["J31"].value == 15800 and o["L31"].value == "OK" and o["J25"].value == 39600 and o["L50"].value == "Não se aplica",
    "exemplo: janelas usam a cotação 2 escolhida (15.800, não a menor); estrutura 30 m² × 1.320 = 39.600; hidromassagem com quantidade 0 = não se aplica")
log(RW["branco"]["Resumo"][f"B{R0+13}"].value == "Ainda não há itens com cotação" and RW["branco"]["Resumo"][f"B{R0+8}"].value == len(ITENS),
    "versão em branco: lista sugerida sem valores, sem erro")
erros = [(n, ws.title, cc.coordinate) for n, wb in RW.items() for ws in wb for row in ws.iter_rows() for cc in row
         if isinstance(cc.value, str) and cc.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(RW)} arquivos" + (f" {erros[:4]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

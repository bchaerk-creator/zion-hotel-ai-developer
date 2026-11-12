"""Testa a Ferramenta 15 recalculando no LibreOffice e comparando com uma regra independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, random
from decimal import Decimal, ROUND_HALF_UP
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from dados import CRITERIOS, EX_NEC, EX_COT
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EX = D / "Comparador-Fornecedores-Zion-EM-BRANCO.xlsx", D / "Comparador-Fornecedores-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
K0, N0, C0, S0 = 6, 6, 7, 7
PESOS = [p for _, _, p in CRITERIOS]

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
r2 = lambda x: float(Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

def referencia(pesos, necs, cots):
    """Regra escrita a partir do texto da aba Comece aqui, sem olhar as fórmulas."""
    w = [max(0, p) if isnum(p) else 0 for p in pesos]
    nomes = [n[0] for n in necs if n[0]]
    linhas = []
    for c in cots:
        a, b, emb, q, preco, frete, pmin, prazo, *notas = c
        if a in (None, "") and b in (None, "") and preco in (None, ""): sit = ""
        elif a in (None, "") or a not in nomes: sit = "Necessidade não cadastrada"
        elif b in (None, ""): sit = "Falta o fornecedor"
        elif not isnum(q) or not isnum(preco) or q <= 0 or preco <= 0: sit = "Confira quantidade e preço"
        elif (frete not in (None, "") and (not isnum(frete) or frete < 0)) or (pmin not in (None, "") and (not isnum(pmin) or pmin < 1)):
            sit = "Confira frete e pedido mínimo"
        elif prazo not in (None, "") and (not isnum(prazo) or prazo < 0): sit = "Confira o prazo"
        elif any(n not in (None, "") and (not isnum(n) or n < 1 or n > 5) for n in notas): sit = "Confira as notas (1 a 5)"
        else: sit = "OK"
        L = dict(nec=a, forn=b, sit=sit, q=q, prazo=prazo, notas=notas)
        if sit == "OK":
            k = pmin if isnum(pmin) else 1; f = frete if isnum(frete) else 0
            L["custo"] = (preco * k + f) / (q * k); L["k"] = k
        linhas.append(L)
    val = [L for L in linhas if L["sit"] == "OK"]
    for L in val:
        mesma = [x for x in val if x["nec"] == L["nec"]]
        L["np"] = 5 * min(x["custo"] for x in mesma) / L["custo"]
        prazos = [x["prazo"] for x in mesma if isnum(x["prazo"])]
        L["nz"] = 5 * (min(prazos) + 1) / (L["prazo"] + 1) if isnum(L["prazo"]) else None
        pares = [(w[0], L["np"])] + ([(w[1], L["nz"])] if L["nz"] is not None else []) + [(w[i + 2], n) for i, n in enumerate(L["notas"]) if isnum(n)]
        den = sum(p for p, _ in pares)
        L["final"] = "Defina os pesos" if den == 0 else r2(sum(p * n for p, n in pares) / den)
        cons = [n[2] for n in necs if n[0] == L["nec"]]
        c = cons[0] if len(cons) == 1 and isnum(cons[0]) and cons[0] > 0 else None
        L["mes"] = L["custo"] * c if c else None
        L["meses"] = round(L["q"] * L["k"] / c + 1e-12, 1) if c else None
    for L in val:
        mesma = [x for x in val if x["nec"] == L["nec"]]
        finais = [x["final"] for x in mesma if isnum(x["final"])]
        best = False
        if isnum(L["final"]) and L["final"] == max(finais):
            cand = [x["custo"] for x in mesma if isnum(x["final"]) and x["final"] == max(finais)]
            best = L["custo"] == min(cand)
        cheap = L["custo"] == min(x["custo"] for x in mesma)
        L["res"] = "Melhor nota e menor custo" if best and cheap else "Melhor nota" if best else "Menor custo" if cheap else ""
    resumo = []
    for n in necs:
        if not n[0]: resumo.append(None); continue
        mesma = [x for x in val if x["nec"] == n[0]]
        R = dict(qtd=len(mesma), sit="Sem cotações válidas" if not mesma else "Peça mais cotações (ideal: 3)" if len(mesma) < 3 else "Pronto para decidir")
        b = next((x for x in mesma if x["res"].startswith("Melhor nota")), None)
        c = next((x for x in mesma if x["res"] in ("Menor custo", "Melhor nota e menor custo")), None)
        R["melhor"] = b["forn"] if b else ("Defina os pesos" if mesma else None)
        R["nota"] = b["final"] if b else None; R["cb"] = b["custo"] if b else None
        R["barato"] = c["forn"] if c else None; R["cc"] = c["custo"] if c else None
        R["dif"] = (b["custo"] - c["custo"]) * n[2] if b and c and isnum(n[2]) and n[2] > 0 else None
        resumo.append(R)
    prob = sum(1 for L in linhas if L["sit"] not in ("", "OK"))
    return linhas, resumo, prob

def cenario(nome, pesos, necs, cots):
    wb = load_workbook(BR); cr, ne, co = wb["Critérios"], wb["Necessidades"], wb["Cotações"]
    for i, p in enumerate(pesos): cr[f"C{K0+i}"] = p
    for i, n in enumerate(necs):
        for col, v in zip("ABCD", n): ne[f"{col}{N0+i}"] = v
    for k, c in enumerate(cots):
        for col, v in zip("ABCDEFGHIJKL", c): co[f"{col}{C0+k}"] = v
    p = TMP / f"{nome}.xlsx"; wb.save(p); cen[nome] = (p, pesos, necs, cots)

def aleatorio(nome, seed, erros):
    rnd = random.Random(seed)
    necs = [(f"Necessidade {seed}-{i}", "L", rnd.choice([None, rnd.randint(1, 400), 0]), None) for i in range(rnd.randint(1, 6))]
    cots = []
    def esc(bons, ruins): return rnd.choice(ruins) if erros and rnd.random() < .07 else rnd.choice(bons)
    for j in range(rnd.randint(3, 40 if erros else 25)):
        nota = lambda: esc([None, 1, 2, 3, 4, 5], [0, 7, "boa"])
        cots.append((esc([n[0] for n in necs], ["Fora da lista"]), esc([f"Fornecedor {j}"], [None]), "emb",
                     esc([1, 5, 12, 0.5, 64], [0, "dez"]), esc([9.9, 42, 105, 7.35, 120], [-1]),
                     esc([None, 0, 25, 60], [-5]), esc([None, 1, 2, 6], [0.5]),
                     esc([None, 0, 1, 3, 7, 10], [-2, "logo"]), nota(), nota(), nota(), nota()))
    pesos = [rnd.choice([0, 1, 2, 3, 4, 5, 2.5]) for _ in range(6)]
    cenario(nome, pesos, necs, cots)

for s in range(8): aleatorio(f"aleatorio_com_erros_{s}", 100 + s, True)
for s in range(4): aleatorio(f"aleatorio_limpo_{s}", 200 + s, False)
N1 = [("Gás", "unidade", 4, None)]
cenario("pesos_zerados", [0] * 6, N1, [("Gás", "A", "P13", 1, 120, None, None, 2, 4, 4, 4, 4), ("Gás", "B", "P13", 1, 110, None, None, 1, 3, 3, 3, 3)])
cenario("so_preco", [5, 0, 0, 0, 0, 0], N1, [("Gás", "A", "P13", 1, 120, None, None, 2, 5, 5, 5, 5), ("Gás", "B", "P13", 1, 110, None, None, 9, 1, 1, 1, 1)])
cenario("empate_total", PESOS, N1, [("Gás", "A", "P13", 1, 110, None, None, 2, 4, 4, 4, 4), ("Gás", "B", "P13", 1, 110, None, None, 2, 4, 4, 4, 4)])
cenario("empate_nota_desempata_custo", [1, 0, 0, 0, 0, 0], N1,
        [("Gás", "A", "P13", 1, 100, None, None, None, None, None, None, None), ("Gás", "B", "P13", 1, 100, 0, None, None, None, None, None, None)])
cenario("frete_e_pedido_minimo", PESOS, [("Detergente", "L", 10, None)],
        [("Detergente", "A", "galão 5 L", 5, 40, 30, 3, 4, 4, 4, 4, 4), ("Detergente", "B", "frasco 1 L", 1, 9, None, None, 0, 4, 4, 4, 4)])
cenario("sem_prazo_nenhum", PESOS, N1, [("Gás", "A", "P13", 1, 120, None, None, None, 4, None, None, None), ("Gás", "B", "P13", 1, 100, None, None, None, 2, None, None, None)])
cenario("uma_cotacao", PESOS, N1, [("Gás", "A", "P13", 1, 120, None, None, 3, 4, 4, 4, 4)])
cenario("necessidade_sem_cotacao", PESOS, [("Gás", "unidade", None, None), ("Internet", "mês", 1, None)], [("Gás", "A", "P13", 1, 120, None, None, 3, 4, 4, 4, 4)])

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EX), str(BR)]
               + [str(c[0]) for c in cen.values()], check=True, capture_output=True, timeout=900)
R = {n: load_workbook(OUTD / c[0].name, data_only=True) for n, c in cen.items()}
R["exemplo"] = load_workbook(OUTD / EX.name, data_only=True); R["branco"] = load_workbook(OUTD / BR.name, data_only=True)
cen["exemplo"] = (EX, PESOS, EX_NEC, EX_COT)

def igual(a, b, tol=1e-6):
    if a in (None, "") and b in (None, ""): return True
    if isnum(a) and isnum(b): return abs(a - b) < tol
    return a == b

def confere(nome):
    _, pesos, necs, cots = cen[nome]; linhas, resumo, prob = referencia(pesos, necs, cots)
    co, s = R[nome]["Cotações"], R[nome]["Resumo"]; erros = []
    for k, L in enumerate(linhas):
        r = C0 + k; g = lambda c: co[f"{c}{r}"].value
        esp = dict(M=L["sit"], N=L.get("custo"), O=L.get("np"), P=L.get("nz"), Q=L.get("final"), R=L.get("res", ""), S=L.get("mes"), T=L.get("meses"))
        for c, v in esp.items():
            if not igual(v, g(c)): erros.append((f"{c}{r}", v, g(c)))
    for i, Rr in enumerate(resumo):
        if Rr is None: continue
        r = S0 + i; g = lambda c: s[f"{c}{r}"].value
        esp = dict(B=Rr["qtd"], C=Rr["sit"], D=Rr["melhor"], E=Rr["nota"], F=Rr["cb"], G=Rr["barato"], H=Rr["cc"], I=Rr["dif"])
        for c, v in esp.items():
            if not igual(v, g(c)): erros.append((f"Resumo!{c}{r}", v, g(c)))
    if R[nome]["Cotações"]["D3"].value != prob: erros.append(("problemas", prob, R[nome]["Cotações"]["D3"].value))
    if s["C3"].value != sum(1 for n in necs if n[0]): erros.append(("necessidades", s["C3"].value))
    return erros, len([L for L in linhas if L["sit"]]), prob

for nome in ["exemplo"] + [n for n in cen if n != "exemplo"]:
    erros, n, prob = confere(nome)
    log(not erros, f"{nome}: {n} cotações conferidas, {prob} com problema" + (f" | diferenças: {erros[:3]}" if erros else ""))

s, co = R["exemplo"]["Resumo"], R["exemplo"]["Cotações"]
log(s["C3"].value == 5 and s["C4"].value == 3 and s["C5"].value == 1, f"exemplo: {s['C3'].value} necessidades, {s['C4'].value} prontas, {s['C5'].value} cotação com problema (esperado 5, 3, 1)")
log(abs(co["N10"].value - (42 * 4 + 25) / 20) < 1e-9, f"exemplo: detergente da Distribuidora Norte custa R$ {co['N10'].value:.4f} por litro com frete e pedido mínimo (conta à mão: (42×4+25)÷20 = 9,65)")
log(co["M18"].value == "Confira as notas (1 a 5)", "exemplo: nota 7 do Atacado Sul no sabonete é recusada")
log(s["D7"].value == "Lavanderia Gama (fictícia)" and s["G7"].value == "Lavanderia Alfa (fictícia)" and abs(s["I7"].value - 448) < 1e-6,
    f"exemplo: lavanderia com melhor nota e menor custo diferentes, diferença de R$ {s['I7'].value:.2f} por mês (conta à mão: (10,90−9,50)×320 = 448)")
log(R["pesos_zerados"]["Resumo"]["D7"].value == "Defina os pesos", "pesos todos zerados: a planilha pede os pesos")
log(R["empate_total"]["Cotações"]["R7"].value == R["empate_total"]["Cotações"]["R8"].value == "Melhor nota e menor custo", "empate total: as duas aparecem como melhor")
b = R["branco"]
log(b["Resumo"]["C3"].value == 0 and b["Cotações"]["D3"].value == 0 and b["Critérios"]["C13"].value == sum(PESOS), "versão em branco: vazia, sem problemas, pesos padrão somando " + str(sum(PESOS)))
erros = [(n, ws.title, c.coordinate) for n, wb in R.items() for ws in wb for row in ws.iter_rows() for c in row
         if isinstance(c.value, str) and c.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(R)} arquivos" + (f" {erros[:4]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

"""Testa a Ferramenta 12 recalculando no LibreOffice e comparando com uma regra independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, random
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from dados import FOTOS, COMODIDADES, EX_FOTOS, EX_FOTOS_EXCLUIR, EX_COM
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EX = D / "Fotos-Comodidades-Zion-EM-BRANCO.xlsx", D / "Fotos-Comodidades-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
F0, K0, NF, NK = 6, 6, 60, 60
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)

def referencia(fotos, coms):
    """fotos: (ambiente, descrição, obrigatória, situação, ordem); coms: (nome, cat, precisa foto, existe, marcada, tem foto).
    Regra escrita a partir da aba Comece aqui."""
    ordens = [f[4] for f in fotos if isnum(f[4])]
    af = []
    for amb, desc, obr, st, ordem in fotos:
        vazio = lambda x: x in (None, "")
        if vazio(amb) and vazio(desc): a = ""
        elif vazio(desc): a = "Descreva a foto"
        elif obr not in ("Sim", "Não"): a = "Diga se é obrigatória"
        elif not vazio(ordem) and (not isnum(ordem) or ordem < 1 or ordem != int(ordem)): a = "Confira a ordem"
        elif isnum(ordem) and ordens.count(ordem) > 1: a = "Ordem repetida"
        elif st == "Publicada" and vazio(ordem): a = "Publicada sem ordem"
        elif obr == "Sim" and st not in ("Aprovada", "Publicada"): a = "Obrigatória ainda não aprovada"
        else: a = "OK"
        af.append(a)
    sc = []
    for nome, cat, pf, ex, mc, tf in coms:
        if nome in (None, ""): s = ""
        elif ex not in ("Sim", "Não") or mc not in ("Sim", "Não"): s = "Responda: existe e está marcada?"
        elif ex == "Não" and mc == "Sim": s = "Remover do anúncio"
        elif ex == "Sim" and mc == "Não": s = "Marcar no anúncio"
        elif ex == "Não": s = "Não se aplica"
        elif pf == "Sim" and tf != "Sim": s = "Falta foto"
        else: s = "OK"
        sc.append(s)
    comdesc = [f for f in fotos if f[1] not in (None, "")]
    painel = {
        "Fotos na lista": len(comdesc),
        "Fotos obrigatórias": sum(1 for f in comdesc if f[2] == "Sim"),
        "Obrigatórias aprovadas ou publicadas": sum(1 for f in comdesc if f[2] == "Sim" and f[3] in ("Aprovada", "Publicada")),
        "Fotos publicadas": sum(1 for f in comdesc if f[3] == "Publicada"),
        "Fotos com alerta": sum(1 for a in af if a not in ("", "OK")),
        "Ordens repetidas": af.count("Ordem repetida"),
        "Remover do anúncio (marcada e não existe)": sc.count("Remover do anúncio"),
        "Marcar no anúncio (existe e não está marcada)": sc.count("Marcar no anúncio"),
        "Falta foto de comodidade de destaque": sc.count("Falta foto"),
        "Sem resposta": sum(1 for s in sc if s.startswith("Responda")),
        "OK": sc.count("OK"),
    }
    if painel["Remover do anúncio (marcada e não existe)"]: leit = "1º: tire do anúncio o que não existe na hospedagem"
    elif painel["Fotos com alerta"]: leit = "Resolva os alertas da aba Fotos"
    elif painel["Marcar no anúncio (existe e não está marcada)"]: leit = "Marque no anúncio as comodidades que você tem"
    elif painel["Falta foto de comodidade de destaque"]: leit = "Fotografe as comodidades de destaque"
    elif painel["Sem resposta"]: leit = "Responda as comodidades em branco"
    elif painel["Fotos na lista"] == 0: leit = "Monte a lista de fotos"
    else: leit = "Pronto: confira o anúncio com esta lista"
    return af, sc, painel, leit

def cenario(nome, fotos, coms):
    wb = load_workbook(BR); fo, co = wb["Fotos"], wb["Comodidades"]
    for k in range(NF):
        v = fotos[k] if k < len(fotos) else (None,) * 5
        for col, x in zip("ABCDE", v): fo[f"{col}{F0+k}"] = x
    for k in range(NK):
        v = coms[k] if k < len(coms) else (None,) * 6
        for col, x in zip("ABCDEF", v): co[f"{col}{K0+k}"] = x
    p = TMP / f"{nome}.xlsx"; wb.save(p); cen[nome] = (p, fotos, coms)

def aleatorio(nome, seed, erros):
    rnd = random.Random(seed)
    def esc(bons, ruins): return rnd.choice(ruins) if erros and rnd.random() < .08 else rnd.choice(bons)
    fotos = [(esc([f"Amb {i}"], [None]), esc([f"Foto {i}"], [None]), esc(["Sim", "Não"], [None, "talvez"]),
              rnd.choice([None, "Falta tirar", "Tirada", "Aprovada", "Publicada"]), esc([None, None, rnd.randint(1, 25)], [0, 2.5, "um", -1]))
             for i in range(rnd.randint(3, 40))]
    coms = [(esc([f"Com {i}"], [None]), "Cat", rnd.choice(["Sim", "Não", None]), esc(["Sim", "Não"], [None, "talvez"]),
             esc(["Sim", "Não"], [None]), rnd.choice(["Sim", "Não", None])) for i in range(rnd.randint(3, 45))]
    cenario(nome, fotos, coms)

for s in range(8): aleatorio(f"aleatorio_com_erros_{s}", 500 + s, True)
for s in range(4): aleatorio(f"aleatorio_limpo_{s}", 600 + s, False)
cenario("tudo_pronto", [("Capa", "Vista", "Sim", "Publicada", 1), ("Sala", "Sala", "Sim", "Aprovada", 2), ("Sala", "Detalhe", "Não", None, None)],
        [("Wi-Fi", "E", "Não", "Sim", "Sim", None), ("Lareira", "L", "Sim", "Sim", "Sim", "Sim"), ("Piscina", "L", "Sim", "Não", "Não", None)])
cenario("so_falta_marcar", [("Capa", "Vista", "Sim", "Publicada", 1)], [("Wi-Fi", "E", "Não", "Sim", "Não", None)])
cenario("so_falta_foto", [("Capa", "Vista", "Sim", "Publicada", 1)], [("Hidro", "L", "Sim", "Sim", "Sim", "Não")])
cenario("publicada_sem_ordem", [("Capa", "Vista", "Sim", "Publicada", None)], [])
cenario("ordem_tripla", [("A", "1", "Não", "Tirada", 3), ("B", "2", "Não", "Tirada", 3), ("C", "3", "Não", "Tirada", 3), ("D", "4", "Não", "Tirada", 4)], [])
cenario("lista_vazia", [], [])

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EX), str(BR)]
               + [str(c[0]) for c in cen.values()], check=True, capture_output=True, timeout=900)
R = {n: load_workbook(OUTD / c[0].name, data_only=True) for n, c in cen.items()}
R["exemplo"] = load_workbook(OUTD / EX.name, data_only=True); R["branco"] = load_workbook(OUTD / BR.name, data_only=True)
exf = [(a, b, c) + EX_FOTOS.get(i, ("Falta tirar", None)) for i, (a, b, c) in enumerate(FOTOS) if i not in EX_FOTOS_EXCLUIR]
exc = [(n, cat, pf) + tuple(EX_COM.get(n, (None,) * 3)) for n, cat, pf in COMODIDADES]
cen["exemplo"] = (EX, exf, exc)
cen["branco"] = (BR, [(a, b, c, None, None) for a, b, c in FOTOS], [(n, cat, pf, None, None, None) for n, cat, pf in COMODIDADES])

def confere(nome):
    _, fotos, coms = cen[nome]; af, sc, painel, leit = referencia(fotos, coms)
    fo, co, p = R[nome]["Fotos"], R[nome]["Comodidades"], R[nome]["Painel"]; erros = []
    for k in range(NF):
        esp = af[k] if k < len(af) else ""
        got = fo[f"G{F0+k}"].value or ""
        if esp != got: erros.append((f"Fotos!G{F0+k}", esp, got))
    for k in range(NK):
        esp = sc[k] if k < len(sc) else ""
        got = co[f"G{K0+k}"].value or ""
        if esp != got: erros.append((f"Comodidades!G{K0+k}", esp, got))
    got_p = {p[f"A{r}"].value: p[f"B{r}"].value for r in range(4, 18) if p[f"B{r}"].value is not None}
    for k, v in painel.items():
        if got_p.get(k) != v: erros.append((k, v, got_p.get(k)))
    leit_got = next((p[f"A{r}"].value for r in range(16, 22) if p[f"A{r - 1}"].value == "O que fazer primeiro"), None)
    if leit_got != leit: erros.append(("leitura", leit, leit_got))
    return erros, af, sc, painel

for nome in ["exemplo", "branco"] + [n for n in cen if n not in ("exemplo", "branco")]:
    erros, af, sc, painel = confere(nome)
    log(not erros, f"{nome}: {painel['Fotos na lista']} fotos e {sum(1 for s in sc if s)} comodidades conferidas, {painel['Fotos com alerta']} alertas de foto, "
                   f"{painel['Remover do anúncio (marcada e não existe)']} para remover" + (f" | diferenças: {erros[:3]}" if erros else ""))

p = R["exemplo"]["Painel"]
log(p["B7"].value == 5 and p["B6"].value == 7 and p["B10"].value == 2, "exemplo: 5 de 7 obrigatórias prontas e 2 fotos com a mesma ordem (banheiro, ordem 6)")
log(R["exemplo"]["Comodidades"]["G11"].value == "Remover do anúncio", "exemplo: ar-condicionado marcado no anúncio e inexistente vira 'Remover do anúncio'")
erros = [(n, ws.title, c.coordinate) for n, wb in R.items() for ws in wb for row in ws.iter_rows() for c in row
         if isinstance(c.value, str) and c.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(R)} arquivos" + (f" {erros[:4]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

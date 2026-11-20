"""Testa a Ferramenta 24 recalculando no LibreOffice e comparando com uma montagem independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, random
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from dados import CAMPOS, INFO, REGRAS_FIXAS, EMERG_A, TESTES, EX, EX_RES, NOME, TIPO, CIDADE, CONTATO, TOM, IDIOMA, ASSINA
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EXW = D / "Assistente-Atendimento-Zion-EM-BRANCO.xlsx", D / "Assistente-Atendimento-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
t = lambda x: (x or "").strip() if isinstance(x, str) else ("" if x is None else str(x))

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)

def referencia(ficha, res):
    """Montagem escrita a partir da aba Comece aqui, sem olhar as fórmulas."""
    v = [t(x) for x in ficha]
    p = lambda i: v[i] or "[PREENCHA]"
    falta = sum(1 for i, c in enumerate(CAMPOS) if c[2] and not v[i])
    alerta = any(k in x.lower() for x in v for k in ("senha:", "código:", "codigo:"))
    sit = f"Faltam {falta} campo(s) obrigatório(s)" if falta else "Tire senhas e códigos da ficha" if alerta else "Pronta para copiar"
    linhas = [f"Você é o assistente de atendimento de {p(NOME)}, {p(TIPO)} em {p(CIDADE)}. Você responde mensagens de hóspedes e de pessoas interessadas em reservar.",
              f"Responda em {v[IDIOMA] or 'português do Brasil'}, com tom {v[TOM] or 'cordial e direto'}. Assine como {v[ASSINA] or 'a equipe de ' + p(NOME)}.",
              "", "REGRAS QUE VOCÊ SEMPRE SEGUE"] + REGRAS_FIXAS + [EMERG_A + p(CONTATO) + ".", "", "INFORMAÇÕES DA HOSPEDAGEM (use só estas)"]
    for i in INFO:
        lab, obrig = CAMPOS[i][1], CAMPOS[i][2]
        linhas.append(f"{lab}: {p(i)}" if obrig else (f"{lab}: {v[i]}" if v[i] else ""))
    linhas += ["", "Fim das informações. Para qualquer assunto que não esteja acima, use a regra 1."]
    esperado = []
    for perg, campo, fixo in TESTES:
        if campo is None: esperado.append(fixo)
        elif not v[campo]: esperado.append("Não inventa: diz que vai confirmar com o anfitrião")
        else: esperado.append("Responde com a ficha: " + v[campo][:90] + ("…" if len(v[campo]) > 90 else ""))
    feitos = sum(1 for r in res if r in ("Passou", "Falhou")); pas = sum(1 for r in res if r == "Passou"); fal_ = sum(1 for r in res if r == "Falhou")
    n = len(TESTES)
    if sit != "Pronta para copiar": leit = "Complete a ficha antes de testar"
    elif feitos < n: leit = f"Faça os {n - feitos} teste(s) que faltam"
    elif fal_ > 0: leit = f"Ajuste a ficha e refaça os {fal_} teste(s) que falharam"
    else: leit = f"Pronto: o assistente passou nos {n} testes"
    return sit, falta, linhas, esperado, (feitos, pas, fal_), leit

def cenario(nome, ficha, res):
    wb = load_workbook(BR); fi, te = wb["Ficha"], wb["Teste"]
    for i, x in enumerate(ficha): fi[f"B{6+i}"] = x
    for k, r in enumerate(res): te[f"D{6+k}"] = r
    p = TMP / f"{nome}.xlsx"; wb.save(p); cen[nome] = (p, ficha, res)

COMPLETA = list(EX); COMPLETA[7] = "Vaga coberta para 1 carro, sem custo"; COMPLETA[9] = "Não servimos café; a cozinha é equipada"
SO_OBRIG = [x if CAMPOS[i][2] else None for i, x in enumerate(EX)]
rnd = random.Random(24)
for s in range(8):
    ficha = [x if (s >= 3 and CAMPOS[i][2]) else rnd.choice([x, None, "  ", x]) for i, x in enumerate(COMPLETA)]
    if s % 2: ficha[rnd.randrange(17)] = rnd.choice(["A Senha: 1234", "código: 9988", "CODIGO: 11"])
    res = [rnd.choice(["Passou", "Falhou", None, "Passou"]) for _ in TESTES]
    cenario(f"aleatorio_{s}", ficha, res)
cenario("completa_tudo_passou", COMPLETA, ["Passou"] * 12)
cenario("so_obrigatorios", SO_OBRIG, ["Passou"] * 11 + ["Falhou"])
cenario("falta_contato", [None if i == CONTATO else x for i, x in enumerate(COMPLETA)], ["Passou"] * 12)
cenario("senha_escrita", [("Rede Casa, senha: ipe2026" if i == 6 else x) for i, x in enumerate(COMPLETA)], ["Passou"] * 12)
cenario("texto_longo_e_espacos", [("   " + "Cachoeiras, mirantes, trilhas, vinícolas, restaurantes de comida típica e mercado; tudo a menos de meia hora de carro   " if i == 11 else x) for i, x in enumerate(COMPLETA)], [])
cenario("vazia", [], [])

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EXW), str(BR)]
               + [str(c[0]) for c in cen.values()], check=True, capture_output=True, timeout=600)
R = {n: load_workbook(OUTD / c[0].name, data_only=True) for n, c in cen.items()}
R["exemplo"] = load_workbook(OUTD / EXW.name, data_only=True); R["branco"] = load_workbook(OUTD / BR.name, data_only=True)
cen["exemplo"] = (EXW, EX, EX_RES or []); cen["branco"] = (BR, [], [])

def confere(nome):
    _, ficha, res = cen[nome]; ficha = list(ficha) + [None] * (17 - len(ficha)); res = list(res) + [None] * (12 - len(res))
    sit, falta, linhas, esperado, cont, leit = referencia(ficha, res)
    w = R[nome]; fi, ins, te = w["Ficha"], w["Instrução"], w["Teste"]; erros = []
    if fi["B3"].value != sit: erros.append(("situação", sit, fi["B3"].value))
    if fi["B4"].value != falta: erros.append(("faltam", falta, fi["B4"].value))
    for k, l in enumerate(linhas):
        got = ins.cell(5 + k, 1).value or ""
        if got != l: erros.append((f"Instrução linha {5+k}", l[:60], str(got)[:60]))
    for k, e in enumerate(esperado):
        if te[f"C{6+k}"].value != e: erros.append((f"Teste C{6+k}", e[:60], str(te[f'C{6+k}'].value)[:60]))
    for k, c in enumerate(cont):
        if te[f"C{19+k}"].value != c: erros.append((f"Teste C{19+k}", c, te[f"C{19+k}"].value))
    if te["C22"].value != leit: erros.append(("leitura", leit, te["C22"].value))
    return erros, sit, leit

for nome in ["exemplo", "branco"] + [x for x in cen if x not in ("exemplo", "branco")]:
    erros, sit, leit = confere(nome)
    log(not erros, f"{nome}: {sit} · {leit}" + (f" | diferenças: {erros[:3]}" if erros else ""))

ex = R["exemplo"]
log(ex["Teste"]["C9"].value.startswith("Não inventa") and ex["Teste"]["C11"].value.startswith("Não inventa") and ex["Teste"]["C22"].value == "Pronto: o assistente passou nos 12 testes",
    "exemplo: estacionamento e café vazios pedem 'não inventar'; resultado real 12 de 12 registrado")
log(R["senha_escrita"]["Ficha"]["B3"].value == "Tire senhas e códigos da ficha" and R["senha_escrita"]["Teste"]["C22"].value == "Complete a ficha antes de testar",
    "senha escrita na ficha bloqueia a instrução e o teste")
log("[PREENCHA]" in (R["falta_contato"]["Instrução"]["A16"].value or ""), "contato vazio aparece como [PREENCHA] na regra de emergência")
txt = "\n".join((ex["Instrução"].cell(r, 1).value or "") for r in range(5, 35))
log("Estacionamento" not in txt and "Café da manhã" not in txt and "senha:" not in txt.lower(), "instrução do exemplo não cita campos vazios nem traz senha")
erros = [(nm, ws.title, c.coordinate) for nm, wb in R.items() for ws in wb for row in ws.iter_rows() for c in row
         if isinstance(c.value, str) and c.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(R)} arquivos" + (f" {erros[:4]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

"""Testa a Ferramenta 11 recalculando no LibreOffice e comparando cada mensagem com uma montagem
independente em Python (mesmos modelos, sem passar pelas fórmulas). Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, datetime, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from mensagens import CAMPOS, MENSAGENS, DATAS
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EX = D / "Kit-Mensagens-Zion-EM-BRANCO.xlsx", D / "Kit-Mensagens-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
ROT = {c[0]: c[1] for c in CAMPOS}
EXEMPLO = {c[0]: (datetime.date.fromisoformat(c[5]) if c[0] in DATAS else c[5]) for c in CAMPOS if c[5]}

def log(b, msg):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + msg)

def linha_campo(wb, k):
    f = wb["Ficha"]
    for r in range(1, 60):
        if str(f.cell(r, 1).value or "").rstrip(" *") == ROT[k]: return r
    raise KeyError(k)

def montar_ref(v):
    """Montagem independente: devolve {id: (texto, faltas)}."""
    def fmt(k):
        x = v.get(k)
        if x in (None, ""): return None
        return x.strftime("%d/%m/%Y") if k in DATAS else str(x)
    res = {}
    for mid, tit, quando, regra, segs in MENSAGENS:
        txt, faltas = "", []
        for s in segs:
            if s[0] == "t":
                def sub(mm):
                    val = fmt(mm.group(1))
                    if val is None:
                        if ROT[mm.group(1)] not in faltas: faltas.append(ROT[mm.group(1)])
                        return f"[PREENCHA: {ROT[mm.group(1)]}]"
                    return val
                txt += re.sub(r"\{(\w+)\}", sub, s[1])
            elif s[0] == "o":
                ks = re.findall(r"\{(\w+)\}", s[1])
                if all(fmt(k) is not None for k in ks): txt += re.sub(r"\{(\w+)\}", lambda mm: fmt(mm.group(1)), s[1])
            elif s[0] == "v" and fmt(s[1]) is None: txt += s[2]
        res[mid] = (txt, faltas)
    return res

def cenario(nome, valores):
    wb = load_workbook(BR); f = wb["Ficha"]
    for k, x in valores.items(): f.cell(linha_campo(wb, k), 2).value = x
    p = TMP / f"{nome}.xlsx"; wb.save(p); cen[nome] = (p, valores)

obrig = {c[0]: EXEMPLO[c[0]] for c in CAMPOS if c[3]}
cenario("completo", dict(EXEMPLO, hora_cheg="16h30"))
cenario("so_obrigatorios", obrig)
sem_senha = dict(EXEMPLO); sem_senha["wifi_senha"] = None
cenario("falta_senha", sem_senha)
cenario("uma_noite", dict(EXEMPLO, saida=datetime.date(2026, 12, 13)))
cenario("datas_invertidas", dict(EXEMPLO, saida=datetime.date(2026, 12, 10)))
cenario("aspas_e_texto_longo", dict(EXEMPLO, regras='Não use "vela" dentro da unidade. ' + "Respeite o silêncio depois das 22h e cuide da natureza ao redor. " * 6))
cenario("vazio", {})

subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EX)]
               + [str(p) for p, _ in cen.values()], check=True, capture_output=True, timeout=600)
R = {n: load_workbook(OUTD / p.name, data_only=True) for n, (p, _) in cen.items()}
R["exemplo"] = load_workbook(OUTD / EX.name, data_only=True); cen["exemplo"] = (EX, EXEMPLO)
r0 = 6
def msgs(n): m = R[n]["Mensagens"]; return {m[f"A{r0+i}"].value: (m[f"E{r0+i}"].value or "", m[f"F{r0+i}"].value, m[f"D{r0+i}"].value) for i in range(len(MENSAGENS))}

for n in ["exemplo", "completo", "so_obrigatorios", "falta_senha", "aspas_e_texto_longo", "vazio"]:
    print(f"Cenário: {n}")
    ref, got = montar_ref({k: v for k, v in cen[n][1].items()}), msgs(n)
    iguais = [mid for mid in ref if ref[mid][0] == got[mid][0]]
    log(len(iguais) == len(MENSAGENS), f"{len(iguais)} de {len(MENSAGENS)} textos idênticos à montagem independente"
        + ("" if len(iguais) == len(MENSAGENS) else f" | 1º diferente: {[m for m in ref if m not in iguais][0]}"))
    st = [(mid, (("Pronta para copiar" if not ref[mid][1] else "Falta: " + "; ".join(ref[mid][1])) == got[mid][1])) for mid in ref]
    log(all(x for _, x in st), "situação de cada mensagem confere" + ("" if all(x for _, x in st) else f" {[m for m, x in st if not x]}"))

ex = msgs("exemplo")
log(R["exemplo"]["Mensagens"]["C3"].value == "10 de 10", f"exemplo: {R['exemplo']['Mensagens']['C3'].value} prontas")
log(ex["M02"][2] == "10/12/2026" and ex["M05"][2] == "13/12/2026" and ex["M06"][2] == "13/12/2026" and ex["M08"][2] == "14/12/2026",
    f"datas de envio: M02 {ex['M02'][2]}, M05 {ex['M05'][2]}, M06 {ex['M06'][2]}, M08 {ex['M08'][2]}")
log("Qual é o horário previsto" in ex["M03"][0] and "16h30" in msgs("completo")["M03"][0], "M03 pergunta o horário quando vazio e confirma quando preenchido")
so = msgs("so_obrigatorios")
log("Mapa:" not in so["M02"][0] and "Estacionamento" not in so["M02"][0] and "código" not in so["M04"][0] and "Link:" not in so["M08"][0],
    "opcionais vazios somem da frase (mapa, estacionamento, código, link)")
log(all("[PREENCHA" not in t for t, _, _ in so.values()), "só com obrigatórios: nenhuma mensagem com [PREENCHA]")
fs = msgs("falta_senha")
log("[PREENCHA: Wi-Fi: senha]" in fs["M04"][0] and fs["M04"][1] == "Falta: Wi-Fi: senha", "senha do Wi-Fi vazia: aviso no texto e na situação")
log(R["falta_senha"]["Mensagens"]["C3"].value == "9 de 10", "falta_senha: 9 de 10 prontas")
un = msgs("uma_noite")
log(un["M05"][2] == "Pule: estadia de 1 noite" and un["M06"][2] == "12/12/2026", "1 noite: apoio marcado para pular; lembrete de saída na noite da entrada")
di = msgs("datas_invertidas")
log(all(di[mid][2] == "Confira as datas" for mid in ("M02", "M03", "M06", "M08")), "datas invertidas: envio bloqueado com 'Confira as datas'")
log(R["datas_invertidas"]["Mensagens"]["E3"].value == "A saída precisa ser depois da entrada", "datas invertidas: aviso no topo")
log(R["exemplo"]["Mensagens"]["E3"].value == "OK: 2 noites", f"situação das datas no exemplo: {R['exemplo']['Mensagens']['E3'].value}")
log(R["vazio"]["Mensagens"]["C3"].value == "0 de 10", "versão vazia: 0 de 10 prontas, sem erro")
erros = [(n, ws.title, c.coordinate) for n, wb in R.items() for ws in wb for row in ws.iter_rows() for c in row
         if isinstance(c.value, str) and c.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(R)} arquivos" + (f" {erros[:4]}" if erros else ""))
maior = max(len(t) for n in R for t, _, _ in msgs(n).values())
log(maior < 4000, f"maior mensagem: {maior} caracteres")
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

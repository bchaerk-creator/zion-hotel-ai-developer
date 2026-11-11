"""Testa a Ferramenta 30 recalculando no LibreOffice e comparando cada mensagem com uma montagem
independente em Python (mesmos modelos, sem passar pelas fórmulas). Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, datetime, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from mensagens import CAMPOS, MENSAGENS, DATAS
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EX = D / "Briefing-Experiencia-Zion-EM-BRANCO.xlsx", D / "Briefing-Experiencia-Zion-EXEMPLO.xlsx"
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
cenario("completo", dict(EXEMPLO))
cenario("so_obrigatorios", obrig)
sem_levar = dict(EXEMPLO); sem_levar["levar"] = None
cenario("falta_levar", sem_levar)
cenario("abaixo_do_minimo", dict(EXEMPLO, pessoas="2"))
cenario("sem_data", dict(EXEMPLO, data=None))
cenario("aspas_e_texto_longo", dict(EXEMPLO, resumo='Um "café da roça" servido no alto da serra. ' + "Caminhada tranquila, com paradas para fotos e explicação da mata ao redor. " * 6))
cenario("vazio", {})
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EX)]
               + [str(p) for p, _ in cen.values()], check=True, capture_output=True, timeout=600)
R = {n: load_workbook(OUTD / p.name, data_only=True) for n, (p, _) in cen.items()}
R["exemplo"] = load_workbook(OUTD / EX.name, data_only=True); cen["exemplo"] = (EX, EXEMPLO)
r0 = 6
def msgs(n): m = R[n]["Mensagens"]; return {m[f"A{r0+i}"].value: (m[f"E{r0+i}"].value or "", m[f"F{r0+i}"].value, m[f"D{r0+i}"].value) for i in range(len(MENSAGENS))}

for n in ["exemplo", "completo", "so_obrigatorios", "falta_levar", "abaixo_do_minimo", "sem_data", "aspas_e_texto_longo", "vazio"]:
    print(f"Cenário: {n}")
    ref, got = montar_ref({k: v for k, v in cen[n][1].items()}), msgs(n)
    iguais = [mid for mid in ref if ref[mid][0] == got[mid][0]]
    log(len(iguais) == len(MENSAGENS), f"{len(iguais)} de {len(MENSAGENS)} textos idênticos à montagem independente"
        + ("" if len(iguais) == len(MENSAGENS) else f" | 1º diferente: {[m for m in ref if m not in iguais][0]}"))
    st = [(mid, (("Pronta para copiar" if not ref[mid][1] else "Falta: " + "; ".join(ref[mid][1])) == got[mid][1])) for mid in ref]
    log(all(x for _, x in st), "situação de cada texto confere" + ("" if all(x for _, x in st) else f" {[m for m, x in st if not x]}"))

ex = msgs("exemplo")
log(R["exemplo"]["Mensagens"]["C3"].value == "8 de 8", f"exemplo: {R['exemplo']['Mensagens']['C3'].value} prontos")
log(ex["B03"][2] == "10/12/2026" and ex["B05"][2] == "11/12/2026" and ex["B06"][2] == "11/12/2026" and ex["B08"][2] == "12/12/2026" and ex["B01"][2] == "Quando precisar",
    f"datas de envio: B03 {ex['B03'][2]}, B05 {ex['B05'][2]}, B06 {ex['B06'][2]}, B08 {ex['B08'][2]}")
log("Restrições do grupo: uma pessoa não come glúten" in ex["B06"][0] and "não informou restrições" in msgs("so_obrigatorios")["B06"][0],
    "B06 traz as restrições quando informadas e pede para confirmar quando vazias")
so = msgs("so_obrigatorios")
log("Não incluído" not in so["B01"][0] and "Valor:" not in so["B01"][0] and "Siga sempre" not in so["B05"][0],
    "opcionais vazios somem da frase (não incluído, valor, segurança)")
log(all("[PREENCHA" not in t for t, _, _ in so.values()), "só com obrigatórios: nenhum texto com [PREENCHA]")
fl = msgs("falta_levar")
log("[PREENCHA: O que levar]" in fl["B05"][0] and fl["B05"][1] == "Falta: O que levar", "'o que levar' vazio: aviso no texto e na situação")
log(R["exemplo"]["Mensagens"]["E3"].value.startswith("Mínimo atingido") and R["abaixo_do_minimo"]["Mensagens"]["E3"].value.startswith("Abaixo do mínimo"),
    "situação da saída: mínimo atingido (5 de 4) e abaixo do mínimo (2 de 4)")
sd = msgs("sem_data")
log(all(sd[mid][2] == "[PREENCHA: Data da saída]" for mid in ("B03", "B05", "B08")) and R["sem_data"]["Mensagens"]["E3"].value == "Preencha a data da saída",
    "sem data: datas de envio pedem a data")
log(R["vazio"]["Mensagens"]["C3"].value == "0 de 8", "versão vazia: 0 de 8 prontos, sem erro")
erros = [(n, ws.title, c.coordinate) for n, wb in R.items() for ws in wb for row in ws.iter_rows() for c in row
         if isinstance(c.value, str) and c.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(R)} arquivos" + (f" {erros[:4]}" if erros else ""))
maior = max(len(t) for n in R for t, _, _ in msgs(n).values())
log(maior < 4000, f"maior mensagem: {maior} caracteres")
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

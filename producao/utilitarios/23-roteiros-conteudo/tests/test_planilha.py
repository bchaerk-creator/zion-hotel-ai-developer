"""Testa a Ferramenta 23 recalculando no LibreOffice e comparando cada roteiro, data e situação com uma montagem
independente em Python (mesmos modelos, sem passar pelas fórmulas). Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, datetime, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from roteiros import CAMPOS, MENSAGENS, DATAS
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EX = D / "Roteiros-Conteudo-Zion-EM-BRANCO.xlsx", D / "Roteiros-Conteudo-Zion-EXEMPLO.xlsx"
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "o"; OUTD.mkdir(); cen = {}
ROT = {c[0]: c[1] for c in CAMPOS}
EXEMPLO = {c[0]: (datetime.date.fromisoformat(c[5]) if c[0] in DATAS else c[5]) for c in CAMPOS if c[5] not in (None, "")}
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)

def log(b, msg):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + msg)

def linha_campo(wb, k):
    f = wb["Ficha"]
    for r in range(1, 60):
        if str(f.cell(r, 1).value or "").rstrip(" *") == ROT[k]: return r
    raise KeyError(k)

def montar_ref(v):
    """Montagem independente: devolve {id: (texto, faltas, data)}."""
    def fmt(k):
        x = v.get(k)
        if x in (None, ""): return None
        if k in DATAS: return x.strftime("%d/%m/%Y")
        return str(int(x)) if isinstance(x, float) and x == int(x) else str(x)
    ini, iv = v.get("inicio"), v.get("intervalo")
    res = {}
    for n, (mid, tit, obj, regra, segs) in enumerate(MENSAGENS):
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
        k = int(regra.split("-")[1]) - 1
        if not isinstance(ini, datetime.date): data = "[PREENCHA: Data do primeiro vídeo]"
        elif not isnum(iv) or iv < 1: data = "[CONFIRA: Dias entre os vídeos]"
        else: data = (ini + datetime.timedelta(days=k * iv)).strftime("%d/%m/%Y")
        res[mid] = (txt, faltas, data)
    return res

def cenario(nome, valores):
    wb = load_workbook(BR); f = wb["Ficha"]
    for k, x in valores.items(): f.cell(linha_campo(wb, k), 2).value = x
    p = TMP / f"{nome}.xlsx"; wb.save(p); cen[nome] = (p, valores)

obrig = {c[0]: EXEMPLO[c[0]] for c in CAMPOS if c[3]}
cenario("completo", dict(EXEMPLO))
cenario("so_obrigatorios", obrig)
cenario("falta_cuidado", dict(EXEMPLO, cuidado=None))
cenario("sem_perto", dict(EXEMPLO, perto=None))
cenario("sem_inicio", dict(EXEMPLO, inicio=None))
cenario("intervalo_zero", dict(EXEMPLO, intervalo=0))
cenario("intervalo_texto", dict(EXEMPLO, intervalo="três"))
cenario("intervalo_7", dict(EXEMPLO, intervalo=7, inicio=datetime.date(2027, 2, 20)))
cenario("aspas_e_texto_longo", dict(EXEMPLO, resposta='Não. A estrada é "de chão", firme. ' + "Qualquer carro chega com calma, mesmo depois de chuva forte na região. " * 6))
cenario("vazio", {})
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD), str(EX)]
               + [str(p) for p, _ in cen.values()], check=True, capture_output=True, timeout=600)
R = {n: load_workbook(OUTD / p.name, data_only=True) for n, (p, _) in cen.items()}
R["exemplo"] = load_workbook(OUTD / EX.name, data_only=True); cen["exemplo"] = (EX, EXEMPLO)
r0 = 6
def rots(n): m = R[n]["Roteiros"]; return {m[f"A{r0+i}"].value: (m[f"E{r0+i}"].value or "", m[f"F{r0+i}"].value, m[f"D{r0+i}"].value) for i in range(len(MENSAGENS))}

for n in ["exemplo", "completo", "so_obrigatorios", "falta_cuidado", "sem_perto", "sem_inicio", "intervalo_zero", "intervalo_texto", "intervalo_7", "aspas_e_texto_longo", "vazio"]:
    print(f"Cenário: {n}")
    ref, got = montar_ref(cen[n][1]), rots(n)
    iguais = [mid for mid in ref if ref[mid][0] == got[mid][0]]
    log(len(iguais) == len(MENSAGENS), f"{len(iguais)} de {len(MENSAGENS)} roteiros idênticos à montagem independente"
        + ("" if len(iguais) == len(MENSAGENS) else f" | 1º diferente: {[m for m in ref if m not in iguais][0]}"))
    st = [mid for mid in ref if ("Pronto para gravar" if not ref[mid][1] else "Falta: " + "; ".join(ref[mid][1])) != got[mid][1]]
    dt = [mid for mid in ref if ref[mid][2] != got[mid][2]]
    log(not st and not dt, "situação e data de postar de cada roteiro conferem" + ("" if not st and not dt else f" | situação {st[:2]} data {dt[:2]}"))

ex = rots("exemplo")
log(R["exemplo"]["Roteiros"]["C3"].value == "8 de 8", f"exemplo: {R['exemplo']['Roteiros']['C3'].value} prontos")
log(ex["V01"][2] == "01/12/2026" and ex["V08"][2] == "22/12/2026", f"exemplo: datas de 01/12 a 22/12 a cada 3 dias ({ex['V01'][2]} a {ex['V08'][2]})")
i7 = rots("intervalo_7")
log(i7["V02"][2] == "27/02/2027" and i7["V03"][2] == "06/03/2027", f"virada de mês com intervalo de 7 dias: {i7['V02'][2]}, {i7['V03'][2]}")
so = rots("so_obrigatorios")
log("CENA EXTRA" not in so["V02"][0] and "Às vezes o melhor passeio é não sair" in so["V07"][0] and all("[PREENCHA" not in t for t, _, _ in so.values()),
    "só obrigatórios: cena extra some, V07 troca para o roteiro sem passeios, nenhum [PREENCHA]")
fc = rots("falta_cuidado")
log("[PREENCHA: Um cuidado que pouca gente vê]" in fc["V05"][0] and fc["V05"][1] == "Falta: Um cuidado que pouca gente vê" and fc["V01"][1] == "Pronto para gravar",
    "cuidado vazio: aviso só no V05")
log(R["sem_inicio"]["Ficha"].cell(linha_campo(R["sem_inicio"], "intervalo") + 2, 2).value == "Preencha a data do primeiro vídeo"
    and str(R["intervalo_zero"]["Ficha"].cell(linha_campo(R["intervalo_zero"], "intervalo") + 2, 2).value).startswith("Dias entre os vídeos"),
    "situação do calendário pede a data e recusa intervalo zero")
log(R["vazio"]["Roteiros"]["C3"].value == "0 de 8", "versão vazia: 0 de 8 prontos, sem erro")
erros = [(n, ws.title, c.coordinate) for n, wb in R.items() for ws in wb for row in ws.iter_rows() for c in row
         if isinstance(c.value, str) and c.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro em {len(R)} arquivos" + (f" {erros[:4]}" if erros else ""))
maior = max(len(t) for n in R for t, _, _ in rots(n).values())
log(maior < 4000, f"maior roteiro: {maior} caracteres")
print(f"\n{ok} de {ok+fal} verificações passaram."); sys.exit(1 if fal else 0)

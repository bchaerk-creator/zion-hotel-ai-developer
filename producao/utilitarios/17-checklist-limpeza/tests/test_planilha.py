"""Testa a Ferramenta 17 recalculando no LibreOffice e comparando com uma regra independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile, datetime, random
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from modelo_itens import ITENS
from openpyxl import load_workbook

D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EX = D / "Checklist-Limpeza-Zion-EM-BRANCO.xlsx", D / "Checklist-Limpeza-Zion-EXEMPLO.xlsx"
T0, M0 = 14, 5
TMP = pathlib.Path(tempfile.mkdtemp()); OUTD = TMP / "out"; OUTD.mkdir()
cenarios = {}

def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)

def cenario(nome, base, f):
    wb = load_workbook(base); f(wb); p = TMP / f"{nome}.xlsx"; wb.save(p); cenarios[nome] = p

def referencia(itens, marcas, un, data, exe, conf, exigir):
    """Regra escrita de novo, sem olhar as fórmulas: devolve (status, pendentes, atencao)."""
    pend = aten = obrig = 0
    for (amb, oque, ob, como), (e, f) in zip(itens, marcas):
        if not oque: continue
        if ob == "Sim":
            obrig += 1
            if not (e == "Feito" and f == "Aprovado"): pend += 1
        elif not (e == "Não se aplica" or f == "Não se aplica" or (e == "Feito" and f == "Aprovado")):
            aten += 1
    if not un or not data or not exe or (exigir == "Sim" and not conf):
        return "PREENCHA O CABEÇALHO (unidade, data e nomes)", pend, aten
    if obrig == 0: return "CADASTRE OS ITENS OBRIGATÓRIOS NA ABA MODELO", pend, aten
    if exigir == "Sim" and exe.strip().lower() == (conf or "").strip().lower():
        return "NÃO LIBERAR: a conferência precisa ser feita por outra pessoa", pend, aten
    if pend: return f"NÃO LIBERAR: {pend} " + ("item obrigatório pendente" if pend == 1 else "itens obrigatórios pendentes"), pend, aten
    return "LIBERADA PARA O PRÓXIMO HÓSPEDE", pend, aten

def cabecalho(wb, un="Cabana 9", exe="Bia", conf="Davi", exigir="Sim"):
    t = wb["Troca"]; t["B3"], t["B4"], t["B5"], t["B6"] = un, datetime.date(2026, 11, 6), exe, conf
    wb["Ajustes"]["B5"] = exigir

def marcar(wb, marcas):
    t = wb["Troca"]
    for i, (e, f) in enumerate(marcas): t[f"E{T0+i}"], t[f"F{T0+i}"] = e, f

TUDO_OK = [("Feito", "Aprovado")] * len(ITENS)
NOBR = sum(1 for i in ITENS if i[2] == "Sim")
ichuv = [i[1] for i in ITENS].index("Testar o chuveiro (água quente)")

# ---- cenários ----
cenario("exemplo_ref", EX, lambda wb: wb["Ajustes"].__setitem__("B6", datetime.date(2026, 11, 6)))
def _ex_ok(wb): wb["Troca"][f"F{T0+ichuv}"] = "Aprovado"
cenario("exemplo_chuveiro_ok", EX, _ex_ok)
cenario("branco", BR, lambda wb: None)
cenario("so_cabecalho", BR, lambda wb: cabecalho(wb))
def _mesma(wb): cabecalho(wb, exe="  Bia ", conf="bia"); marcar(wb, TUDO_OK)
cenario("mesma_pessoa", BR, _mesma)
def _sozinho(wb): cabecalho(wb, conf=None, exigir="Não"); marcar(wb, TUDO_OK)
cenario("sozinho", BR, _sozinho)
def _na_obrig(wb):
    cabecalho(wb); mk = list(TUDO_OK); mk[0] = ("Não se aplica", "Não se aplica"); marcar(wb, mk)
cenario("na_obrigatorio", BR, _na_obrig)
def _sem_obrig(wb):
    cabecalho(wb); m = wb["Modelo"]
    for i in range(len(ITENS)): m[f"C{M0+i}"] = "Não"
cenario("sem_obrigatorios", BR, _sem_obrig)
def _novo_item(wb):
    cabecalho(wb); marcar(wb, TUDO_OK); m = wb["Modelo"]; r = M0 + len(ITENS) + 2   # deixa 2 linhas vazias no meio
    m[f"A{r}"], m[f"B{r}"], m[f"C{r}"], m[f"D{r}"] = "9 · Extra", "Conferir lareira", "Sim", "Sem cinzas"
cenario("item_novo", BR, _novo_item)
def _horas(wb):
    cabecalho(wb); t = wb["Troca"]; t["B7"], t["B8"] = datetime.time(12, 0), datetime.time(11, 0)
cenario("horas_invertidas", BR, _horas)
random.seed(17)
opE, opF = ["Feito", "Não feito", "Não se aplica", None], ["Aprovado", "Reprovado", "Não se aplica", None]
aleat = {}
for k in range(8):
    mk = [(random.choice(opE), random.choice(opF)) if random.random() < 0.35 else ("Feito", "Aprovado") for _ in ITENS]
    if k == 0: mk = TUDO_OK
    aleat[f"aleatorio_{k}"] = mk
    cenario(f"aleatorio_{k}", BR, lambda wb, mk=mk: (cabecalho(wb), marcar(wb, mk)))

# ---- recálculo em lote no LibreOffice ----
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(OUTD)]
               + [str(p) for p in cenarios.values()], check=True, capture_output=True, timeout=600)
R = {n: load_workbook(OUTD / p.name, data_only=True) for n, p in cenarios.items()}
st = lambda n: R[n]["Troca"]["B10"].value

print("Exemplo preenchido (data de referência 06/11/2026)")
w = R["exemplo_ref"]; t = w["Troca"]
mk_ex = [("Feito", "Aprovado")] * len(ITENS)
for i, it in enumerate(ITENS):
    if it[1] == "Testar o chuveiro (água quente)": mk_ex[i] = ("Feito", "Reprovado")
    if it[1].startswith("Repor café"): mk_ex[i] = ("Não feito", "Reprovado")
    if it[1].startswith("Conferir banheira"): mk_ex[i] = ("Não se aplica", "Não se aplica")
ref = referencia(ITENS, mk_ex, "Cabana 2", 1, "Ana", "Carlos", "Sim")
log(st("exemplo_ref") == ref[0], f"situação: {st('exemplo_ref')}")
log(t["E3"].value == len(ITENS) and t["E4"].value == NOBR, f"{t['E3'].value} itens, {t['E4'].value} obrigatórios (esperado {len(ITENS)} e {NOBR})")
log(t["E5"].value == 1 and t["E6"].value == 1, f"1 obrigatório pendente e 1 opcional em atenção (planilha: {t['E5'].value} e {t['E6'].value})")
log(t["E7"].value == 95, f"tempo da troca: {t['E7'].value} min (10:30 a 12:05 = 95)")
log(t[f"H{T0+ichuv}"].value == "PENDENTE", "linha do chuveiro marcada PENDENTE")
log(t["A1"].value == "Troca de hóspede · Pousada Exemplo (fictícia)", "título puxa o nome da hospedagem")
p = w["Pendências"]
log([p[f"I{r}"].value for r in (6, 7, 8)] == ["Resolvida", "Atrasada", "Sem prazo"], f"pendências: {[p[f'I{r}'].value for r in (6,7,8)]}")
log(p["B3"].value == 2 and p["D3"].value == 1, f"pendências abertas {p['B3'].value}, atrasadas {p['D3'].value} (esperado 2 e 1)")
h = w["Histórico"]
log(h["B3"].value == 3 and h["D3"].value == 2 and h["F3"].value == 1, "histórico: 3 trocas, 2 liberadas, 1 não liberada")
log(h["I3"].value == round((80 + 75 + 95) / 3), f"tempo médio {h['I3'].value} min (referência {round((80+75+95)/3)})")

print("Cenários de liberação")
log(st("exemplo_chuveiro_ok") == "LIBERADA PARA O PRÓXIMO HÓSPEDE", f"chuveiro aprovado libera: {st('exemplo_chuveiro_ok')}")
log(st("branco").startswith("PREENCHA O CABEÇALHO"), f"versão em branco: {st('branco')}")
log(R["branco"]["Troca"]["E3"].value == len(ITENS), "versão em branco já traz o modelo-padrão na Troca")
log(R["branco"]["Pendências"]["B3"].value == 0 and R["branco"]["Histórico"]["I3"].value in ("", None), "versão em branco: pendências e histórico vazios, sem erro")
esperado = f"NÃO LIBERAR: {NOBR} itens obrigatórios pendentes"
log(st("so_cabecalho") == esperado, f"cabeçalho sem marcações: {st('so_cabecalho')}")
log(st("mesma_pessoa") == "NÃO LIBERAR: a conferência precisa ser feita por outra pessoa", "mesma pessoa (maiúsculas e espaços diferentes) é bloqueada")
log(st("sozinho") == "LIBERADA PARA O PRÓXIMO HÓSPEDE", "anfitrião sozinho (ajuste Não, sem conferente) libera")
log(st("na_obrigatorio") == "NÃO LIBERAR: 1 item obrigatório pendente", "\"Não se aplica\" em item obrigatório conta como pendente")
log(st("sem_obrigatorios") == "CADASTRE OS ITENS OBRIGATÓRIOS NA ABA MODELO", "modelo sem obrigatórios pede cadastro")
tn = R["item_novo"]["Troca"]; rn = T0 + len(ITENS) + 2
log(tn[f"B{rn}"].value == "Conferir lareira" and tn["E3"].value == len(ITENS) + 1, "item novo no Modelo aparece na Troca (mesmo com linhas vazias no meio)")
log(st("item_novo") == "NÃO LIBERAR: 1 item obrigatório pendente", "item novo obrigatório sem marcação bloqueia")
log(R["horas_invertidas"]["Troca"]["E7"].value == "Confira os horários", "fim antes do início é sinalizado")

print("Cenários aleatórios contra a regra independente")
for n, mk in aleat.items():
    r = referencia(ITENS, mk, "Cabana 9", 1, "Bia", "Davi", "Sim"); tt = R[n]["Troca"]
    log(st(n) == r[0] and tt["E5"].value == r[1] and tt["E6"].value == r[2], f"{n}: {st(n)} | atenção {tt['E6'].value}")

erros = [(n, ws.title, c.coordinate) for n, wb in R.items() for ws in wb for row in ws.iter_rows() for c in row
         if isinstance(c.value, str) and c.value.startswith(("#", "Err:"))]
log(not erros, f"nenhuma célula com erro de fórmula em {len(R)} arquivos" + (f" {erros[:5]}" if erros else ""))
print(f"\n{ok} de {ok+fal} verificações passaram.")
sys.exit(1 if fal else 0)

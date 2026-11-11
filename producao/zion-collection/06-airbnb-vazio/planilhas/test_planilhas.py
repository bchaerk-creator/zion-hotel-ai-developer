"""Testa as planilhas do Produto 06 recalculando no LibreOffice.
- Diagnóstico: 14 cenários (todas 0, todas 5, limites de faixa, empates, exemplo) contra a regra independente em Python
  e contra a lógica da ferramenta interativa (ferramenta/src/logic.js, via Node).
- Calendário: datas, dias da semana e contagem de ações feitas.
Uso: python3 -I test_planilhas.py dist"""
import sys, pathlib, subprocess, tempfile, json, datetime, shutil
from openpyxl import load_workbook
D = pathlib.Path(sys.argv[1]).resolve(); A = pathlib.Path(__file__).resolve().parent
ok = fal = 0
def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)
TMP = pathlib.Path(tempfile.mkdtemp())
def recalc(src, nome):
    p = TMP / nome; shutil.copy(src, p) if src != p else None
    out = TMP / "o"; out.mkdir(exist_ok=True)
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx", "--outdir", str(out), str(p)], check=True, capture_output=True, timeout=180)
    return load_workbook(out / nome, data_only=True)

DIMS = ["Fotos e apresentação", "Título e descrição", "Preço e posicionamento", "Diferenciais e experiência", "Avaliações e confiança", "Atendimento e comunicação", "Conforto e infraestrutura"]
def ref(n):
    s = sum(n); p = int(s * 100 / 35 + 0.5)  # arredondamento comercial, igual ao ROUND da planilha
    f = "Oferta consistente" if p >= 85 else "Boa base com pontos de melhoria" if p >= 70 else "Ajustes prioritários" if p >= 50 else "Lacunas relevantes"
    pri = [DIMS[i] for _, i in sorted((v, i) for i, v in enumerate(n))[:3]]
    return s, p, f, pri
CEN = [[0] * 7, [5] * 7, [2, 3, 3, 4, 4, 2, 4], [3, 3, 3, 3, 3, 3, 2], [5, 5, 4, 4, 4, 4, 4], [4] * 7, [3, 3, 3, 3, 2, 2, 2], [2, 2, 2, 2, 3, 3, 3],
       [5, 0, 5, 0, 5, 0, 5], [1, 2, 3, 4, 5, 0, 1], [3] * 7, [0, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 0], [2, 3, 3, 4, 2, 4, 3]]
# lógica da ferramenta interativa, para garantir que planilha e app dão o mesmo resultado
js = ("const L=require(%s);const C=%s;console.log(JSON.stringify(C.map(n=>{const r={};L.DIMENSOES.forEach((d,i)=>r[d.id]={nota:n[i],evidencia:'x'});"
      "const x=L.calcular(r);return [x.pontuacao,x.faixa.nome,x.prioridades.map(p=>p.nome)]})))") % (json.dumps(str(A.parent / "ferramenta/src/logic.js")), json.dumps(CEN))
APP = json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout)

base = D / "Diagnostico-Zion-de-Oferta-EM-BRANCO.xlsx"
for k, n in enumerate(CEN):
    wb = load_workbook(base); ws = wb["Diagnóstico"]
    for i, v in enumerate(n): ws.cell(6 + i, 3, v); ws.cell(6 + i, 4, "evidência")
    nome = f"diag{k}.xlsx"; wb.save(TMP / nome); r = recalc(TMP / nome, nome)["Diagnóstico"]
    s, p, f, pri = ref(n); got = (r["B15"].value, r["B16"].value, r["B17"].value, [r[f"B{20 + j}"].value for j in range(3)])
    alerta = bool(r["B18"].value); log(alerta == any(v <= 1 for v in n), f"   alerta de nota crítica {'aparece' if alerta else 'não aparece'} corretamente")
    log(got == (s, p, f, pri) and APP[k] == [p, f, pri], f"notas {n}: soma {s}, {p}, {f}, prioridades {[x.split()[0] for x in pri]} (planilha = regra = app)")

r = recalc(base, base.name)["Diagnóstico"]
log(r["B16"].value == "Preencha as 7 notas" and r["B17"].value in (None, "") and r["B20"].value in (None, ""), "em branco: pede as 7 notas, sem faixa nem prioridades")
log(r["E6"].value == "Falta a nota", "em branco: aviso de nota faltando")
wb = load_workbook(base); ws = wb["Diagnóstico"]
for i in range(6): ws.cell(6 + i, 3, 3)
wb.save(TMP / "parcial.xlsx"); r = recalc(TMP / "parcial.xlsx", "parcial.xlsx")["Diagnóstico"]
log(r["B14"].value == "6 de 7" and r["B16"].value == "Preencha as 7 notas", "6 de 7 notas: não calcula pontuação")
log(r["E6"].value == "Sem evidência: hipótese", "nota sem evidência vira hipótese")
ex = recalc(D / "Diagnostico-Zion-de-Oferta-EXEMPLO.xlsx", "ex.xlsx")
r = ex["Diagnóstico"]; pl = ex["Plano de ação"]
log(r["B16"].value == 63 and r["B17"].value == "Ajustes prioritários", "exemplo: 63, ajustes prioritários (igual à ferramenta)")
log("dados fictícios" in r["A1"].value and "dados fictícios" in r["B2"].value, "exemplo marcado como dados fictícios")
log(pl["B4"].value == "Fotos e apresentação" and pl["B6"].value == "Título e descrição" and pl["C15"].value == "0 de 3", "plano puxa as prioridades e conta ações feitas")
wbv = load_workbook(base); dv = [d for d in wbv["Diagnóstico"].data_validations.dataValidation if d.type == "whole"]
log(dv and dv[0].formula1 == "0" and dv[0].formula2 == "5", "validação: nota inteira de 0 a 5")

# calendário
cb = D / "Calendario-Comercial-30-Dias-EM-BRANCO.xlsx"
r = recalc(cb, cb.name)["Calendário"]
log(all(r.cell(5 + i, 2).value in (None, "") for i in range(30)), "em branco: sem data de início, sem datas")
log(all(r.cell(5 + i, 6).value for i in range(30)) and r["E43"].value == "0 de 30 feitas", "30 ações escritas; resumo 0 de 30")
wb = load_workbook(cb); ws = wb["Calendário"]; ini = datetime.date(2027, 2, 15); ws["D2"] = ini
for d in (1, 2, 3, 8, 30): ws.cell(4 + d, 9, "Sim")
ws.cell(4 + 4, 9, "Não"); wb.save(TMP / "cal.xlsx"); r = recalc(TMP / "cal.xlsx", "cal.xlsx")["Calendário"]
dias = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
datas_ok = all((r.cell(5 + i, 2).value.date() if hasattr(r.cell(5 + i, 2).value, "date") else None) == ini + datetime.timedelta(i) for i in range(30))
sem_ok = all(r.cell(5 + i, 3).value == dias[(ini + datetime.timedelta(i)).weekday()] for i in range(30))
log(datas_ok, "datas = início + (dia − 1), inclusive virada de mês (fev → mar 2027)")
log(sem_ok, "dia da semana correto nos 30 dias")
log(r["E38"].value == "3 de 7 feitas" and r["E39"].value == "1 de 7 feitas" and r["E42"].value == "1 de 2 feitas" and r["E43"].value == "5 de 30 feitas" and r["E44"].value == "17% do calendário", "resumo por semana e % (5 de 30 = 17%)")
ex = recalc(D / "Calendario-Comercial-30-Dias-EXEMPLO.xlsx", "calex.xlsx")["Calendário"]
log(ex["E43"].value == "13 de 30 feitas" and "dados fictícios" in ex["A1"].value, "exemplo: 13 de 30 feitas, marcado como fictício")
print(f"\n{ok} ok, {fal} falhas"); sys.exit(1 if fal else 0)

"""Testa a planilha Folha Única do Mês recalculando no LibreOffice e comparando com uma conta independente em Python.
Uso: python3 -I tests/test_planilha.py <pasta com os xlsx>"""
import sys, pathlib, subprocess, tempfile
from openpyxl import load_workbook
D = pathlib.Path(sys.argv[1]); ok = fal = 0
def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)
def recalc(path):
    t = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(t), str(path)], check=True, capture_output=True, timeout=180)
    return load_workbook(t / path.name, data_only=True)
def cenario(nome, folha, par=None, base="Folha-Unica-do-Mes-Zion-EM-BRANCO.xlsx"):
    wb = load_workbook(D / base); f = wb["Folha do Mês"]; p = wb["Parâmetros"]
    for cel, v in folha.items(): f[cel] = v
    for cel, v in (par or {}).items(): p[cel] = v
    x = pathlib.Path(tempfile.mkdtemp()) / ("t_" + nome + ".xlsx"); wb.save(x); return recalc(x)
def perto(a, b, tol=0.005): return isinstance(a, (int, float)) and abs(a - b) <= tol

# ---- conta independente (não usa a planilha nem o logic.js) ----
def conta(d, p):
    disp = d["unidades"] * d["dias"]
    ded = d["descontos"] + d["receita"] * (p["comissoes"] + p["processamento"] + p["imposto"] + p["cancelamentos"]) / 100
    rrh = d["receita"] - ded
    limp = max(0, d["limpezaPaga"] - d["limpezaCobrada"]); exc = max(0, d["limpezaCobrada"] - d["limpezaPaga"])
    outras = d["outras"] + exc; fat = d["receita"] + outras; rr = rrh + outras
    quebra = d["receita"] * p["quebra"] / 100 if d.get("quebra") is None else d["quebra"]
    var = limp + d["enxoval"] + d["amenidades"] + d["energia"] + d["cafe"] + quebra + d["outrosVar"] + d["custoOutras"]
    mc = rr - var
    ret = 0 if d.get("retiradaZero") == "Sim" else (p["horas"] * p["valorHora"] * 4.33 if d.get("retirada") is None else d["retirada"])
    fix = d["equipe"] + d["comuns"] + d["software"] + d["contador"] + d["marketing"] + d["duodecimos"] + d["manutencao"] + ret + d["outrosFixos"]
    ro = mc - fix; mod = d["aluguel"] + d["taxaGestao"] + d["marca"]; eb = ro - mod; res = rr * p["reserva"] / 100; gc = eb - res
    n = d["noites"]; fixtot = fix + mod
    cv = (var - d["custoOutras"]) / n if n else None; cpn = cv + fixtot / n if n else None
    dreal = rrh / n if n else None; mpn = dreal - cv if n else None
    pe = max(0, (fixtot - (outras - d["custoOutras"])) / mpn) if (n and mpn > 0) else None
    sf = d["saldoInicial"] + d["entradas"] - d["saidas"]; fol = (sf + d["reservas"]) / fixtot if fixtot > 0 else None
    return dict(disp=disp, ded=ded, rrh=rrh, limp=limp, exc=exc, outras=outras, fat=fat, rr=rr, quebra=quebra, var=var, mc=mc, ret=ret, fix=fix, ro=ro, eb=eb, res=res, gc=gc,
                cv=cv, cpn=cpn, dreal=dreal, mpn=mpn, pe=pe, oe=(pe / disp if pe is not None else None), sf=sf, fol=fol, fixtot=fixtot, mop=(ro / fat if fat else None))

EX = dict(dias=31, unidades=4, noites=58, estadias=25, receita=16240, limpezaCobrada=1500, outras=980, custoOutras=420, descontos=650,
          limpezaPaga=2000, enxoval=380, amenidades=260, energia=340, cafe=0, quebra=None, outrosVar=0,
          equipe=1800, comuns=620, software=190, contador=300, marketing=150, duodecimos=460, manutencao=250, retirada=None, retiradaZero="Não", outrosFixos=0,
          aluguel=0, taxaGestao=0, marca=0, saldoInicial=9800, entradas=18470, saidas=14650, reservas=0)
PAR = dict(comissoes=11, processamento=1.5, imposto=6, cancelamentos=0, quebra=1, reserva=3, horas=20, valorHora=40)
# mapa das células da Folha (mesmo layout do build_planilha.py)
CEL = dict(dias="B6", unidades="B7", noites="B8", estadias="B9", receita="B11", limpezaCobrada="B12", outras="B13", custoOutras="B14", descontos="B15",
           limpezaPaga="B17", enxoval="B18", amenidades="B19", energia="B20", cafe="B21", quebra="B22", outrosVar="B23",
           equipe="B25", comuns="B26", software="B27", contador="B28", marketing="B29", duodecimos="B30", manutencao="B31", retirada="B32", retiradaZero="B33", outrosFixos="B34",
           aluguel="B36", taxaGestao="B37", marca="B38", saldoInicial="B41", entradas="B42", saidas="B43", reservas="B44")
PCEL = dict(comissoes="B4", processamento="B5", imposto="B6", cancelamentos="B7", quebra="B10", reserva="B11", horas="B14", valorHora="B15")
def folha_de(d): return {CEL[k]: v for k, v in d.items() if k in CEL and v is not None}
def par_de(p): return {PCEL[k]: v for k, v in p.items()}

print("Exemplo preenchido (dados fictícios, PLANO seção 9)")
wb = recalc(D / "Folha-Unica-do-Mes-Zion-EXEMPLO.xlsx"); f = wb["Folha do Mês"]; r = conta(EX, PAR)
log(f["B47"].value == "OK" and wb["Parâmetros"]["B18"].value == "OK", "situação dos dados e dos parâmetros OK")
log(f["B49"].value == 124 and perto(f["B50"].value, 58 / 124, 1e-6), f"noites disponíveis {f['B49'].value}, ocupação {f['B50'].value:.1%}")
log(perto(f["B52"].value, 3654.40) and perto(r["ded"], 3654.40), f"deduções = {f['B52'].value:.2f} (ref 3.654,40)")
log(perto(f["B53"].value, 12585.60) and perto(f["B53"].value, r["rrh"]), f"receita real de hospedagem = {f['B53'].value:.2f} (ref 12.585,60)")
log(f["B54"].value == 500 and f["B55"].value == 0 and perto(f["B59"].value, 162.40), "limpeza líquida 500, sem excedente, quebra por referência 162,40")
log(perto(f["B60"].value, 2062.40) and perto(f["B60"].value, r["var"]), f"custos variáveis = {f['B60'].value:.2f} (ref 2.062,40)")
log(perto(f["B58"].value, 13565.60) and perto(f["B57"].value, 17220), f"receita real total {f['B58'].value:.2f}; faturamento {f['B57'].value:.2f}")
log(perto(f["B61"].value, 11503.20), f"margem de contribuição = {f['B61'].value:.2f} (ref 11.503,20)")
log(perto(f["B62"].value, 3464) and perto(wb["Parâmetros"]["B16"].value, 3464) and perto(f["B63"].value, 7234), f"retirada {f['B62'].value:.2f} (20 × 40 × 4,33); fixos {f['B63'].value:.2f} (ref 7.234)")
log(perto(f["B64"].value, 4269.20) and perto(f["B64"].value, r["ro"]), f"quanto sobrou do mês = {f['B64'].value:.2f} (ref 4.269,20)")
log(perto(f["B67"].value, 406.97) and perto(f["B68"].value, 3862.23), f"reserva {f['B67'].value:.2f}; geração de caixa {f['B68'].value:.2f} (ref 406,97 e 3.862,23)")
log(f["B69"].value in (None, ""), "depreciação em branco: resultado contábil indicativo vazio")
log(perto(f["B71"].value, 280) and perto(f["B72"].value, 216.99) and perto(f["B73"].value, 0.225, 1e-4), f"diária bruta {f['B71'].value:.2f}, real {f['B72'].value:.2f}, dedução {f['B73'].value:.1%}")
log(perto(f["B74"].value, 28.32) and perto(f["B76"].value, 153.04) and perto(f["B76"].value, r["cpn"]), f"custo variável por noite {f['B74'].value:.2f}; custo por noite vendida {f['B76'].value:.2f} (ref 153,04)")
log(perto(f["B78"].value, 35.4, 0.05) and perto(f["B79"].value, 0.285, 0.0015) and perto(f["B78"].value, r["pe"]), f"ponto de equilíbrio {f['B78'].value:.1f} noites; ocupação de equilíbrio {f['B79'].value:.1%}")
log(perto(f["B80"].value, 0.2479, 0.0005), f"margem do mês {f['B80'].value:.1%} (ref 24,8%)")
log(f["B82"].value == 13620 and perto(f["B83"].value, 1.88, 0.005) and perto(f["B83"].value, r["fol"]), f"saldo final {f['B82'].value}; fôlego {f['B83'].value:.2f} (ref 1,88)")
log(f["B85"].value == "Cada noite vendida paga tudo e sobra" and f["B86"].value == "Folgada" and f["B87"].value == "Zona de risco" and f["B88"].value == "Viável", f"leituras: {f['B85'].value} / {f['B86'].value} / {f['B87'].value} / {f['B88'].value}")
log(f["B89"].value == "Caixa e resultado andam juntos" and f["B90"].value == "Sem reserva para a baixa", f"caixa × resultado: {f['B89'].value}; causa principal: {f['B90'].value}")
c12 = wb["Caixa 12 meses"]
log(c12["G4"].value == 13620 and c12["B5"].value == 13620 and perto(c12["H4"].value, 13620 / 7234) and c12["I4"].value == "Zona de risco", "caixa 12 meses: saldo final, saldo inicial do mês seguinte e fôlego")
log(c12["G5"].value == 13620 + 15200 - 13900 and perto(c12["H5"].value, (14920 + 1500) / 7234) and c12["G7"].value in (None, ""), "caixa 12 meses: segundo mês com reservas; linha vazia fica vazia")
ck = wb["Checklist do fechamento"]
log(ck["C15"].value == 7 and "Faltam 3" in str(ck["B16"].value), f"checklist: {ck['C15'].value} de 10 feitos no exemplo")
log(all(ck.cell(4 + i, 2).value for i in range(10)) and ck.cell(14, 2).value is None and ck.cell(15, 2).value == "Itens feitos:", "checklist tem 10 itens (linhas 4 a 13)")
wbx = load_workbook(D / "Folha-Unica-do-Mes-Zion-EXEMPLO.xlsx")
log([s.title for s in wbx.worksheets] == ["Comece aqui", "Parâmetros", "Folha do Mês", "Caixa 12 meses", "Histórico", "Checklist do fechamento"], "seis abas na ordem do plano")
log(wbx["Folha do Mês"]["B11"].fill.fgColor.rgb.endswith("FFF4C7") and wbx["Folha do Mês"]["B64"].fill.fgColor.rgb.endswith("E3EEDF"), "amarelo preenche, verde calcula")
log("dados fictícios" in str(wbx["Comece aqui"]["A4"].value).lower() and "referência ajustável, nunca universal" in str(wbx["Parâmetros"]["A2"].value or "") + str(wbx["Parâmetros"]["A20"].value), "exemplo rotulado e parâmetros marcados como referência ajustável")
import re
textos = " ".join(str(c.value) for ws in wbx.worksheets for row in ws.iter_rows() for c in row if isinstance(c.value, str))
log(not re.search(r"garant|retorno garantido|lucro certo|renda extra|valoriza", textos, re.I), "nenhuma promessa proibida nos textos da planilha")
log(not re.search(r"\b(DRE|EBITDA|KPI|ADR|RevPAR)\b", textos), "nenhuma sigla nos textos da planilha")

print("Versão em branco e entradas inválidas")
wb = recalc(D / "Folha-Unica-do-Mes-Zion-EM-BRANCO.xlsx"); f = wb["Folha do Mês"]
log(str(wb["Parâmetros"]["B18"].value).startswith("Preencha") and str(f["B47"].value).startswith("Confira a aba Parâmetros") and f["B64"].value in (None, ""), "em branco: pede os parâmetros, sem resultado")
base = folha_de(EX); par = par_de(PAR)
f = cenario("ok", base, par)["Folha do Mês"]; log(f["B47"].value == "OK" and perto(f["B64"].value, 4269.20), "em branco preenchida com o exemplo dá o mesmo resultado")
f = cenario("vazio", {k: v for k, v in base.items() if k != "B25"}, par)["Folha do Mês"]; log(str(f["B47"].value).startswith("Preencha") and f["B64"].value in (None, ""), "célula obrigatória vazia bloqueia")
f = cenario("neg", {**base, "B18": -10}, par)["Folha do Mês"]; log(f["B47"].value == "Há valor negativo", "valor negativo bloqueia")
f = cenario("dias", {**base, "B6": 27}, par)["Folha do Mês"]; log("28 a 31" in f["B47"].value, "dias fora de 28 a 31 bloqueia")
f = cenario("excesso", {**base, "B8": 125}, par)["Folha do Mês"]; log("passam das noites" in f["B47"].value, "noites > disponíveis bloqueia")
f = cenario("limite", {**base, "B8": 124}, par)["Folha do Mês"]; log(f["B47"].value == "OK", "noites = disponíveis passa")
f = cenario("ded", {**base, "B15": 20000}, par)["Folha do Mês"]; log("Deduções passam da receita" in f["B47"].value, "deduções > receita bloqueia")
w = cenario("pct", base, {**par, "B4": 150}); log("0 e 99,9" in w["Parâmetros"]["B18"].value and w["Folha do Mês"]["B47"].value == "Confira a aba Parâmetros", "percentual acima de 99,9 bloqueia pelos parâmetros")

print("Bordas")
d0 = {**EX, "noites": 0, "estadias": 0, "receita": 0, "descontos": 0, "limpezaCobrada": 0, "outras": 0, "custoOutras": 0}; r0 = conta(d0, PAR)
f = cenario("semnoite", folha_de(d0), par)["Folha do Mês"]
log(f["B47"].value == "OK" and f["B76"].value == "não calculável" and f["B78"].value == "não calculável" and f["B79"].value == "não calculável", "noites 0: sem divisão por zero, indicadores 'não calculável'")
log(f["B85"].value == "Sem noite vendida: cada real que saiu é prejuízo" and perto(f["B64"].value, r0["ro"]) and f["B64"].value < 0, f"noites 0: leitura de prejuízo e resultado {f['B64'].value:.2f}")
dl = {**EX, "limpezaCobrada": 2500}; rl = conta(dl, PAR)
f = cenario("limpeza", folha_de(dl), par)["Folha do Mês"]
log(f["B54"].value == 0 and f["B55"].value == 500 and perto(f["B56"].value, 1480) and perto(f["B64"].value, rl["ro"]), "limpeza cobrada > paga: excedente 500 vai a outras receitas")
f = cenario("estadias0", {**base, "B9": 0}, par)["Folha do Mês"]; log(f["B47"].value == "OK" and f["B51"].value == 58, "estadias 0: assume uma por noite")
dr = {**EX, "retirada": 0, "retiradaZero": "Não", "reservas": 5000}; rr_ = conta(dr, PAR)
f = cenario("ret0", folha_de(dr), par)["Folha do Mês"]
log(f["B62"].value == 0 and perto(f["B63"].value, 3770) and f["B90"].value == "Retirada não lançada" and perto(f["B64"].value, rr_["ro"]), "retirada 0 sem decisão: causa principal 'Retirada não lançada'")
f = cenario("retSim", {**folha_de(dr), "B32": None, "B33": "Sim"}, par)["Folha do Mês"]
log(f["B62"].value == 0 and f["B90"].value != "Retirada não lançada", f"retirada zero decidida: causa principal passa a '{f['B90'].value}'")
f = cenario("duod", {**base, "B30": 0}, par)["Folha do Mês"]; log(f["B90"].value == "Despesas anuais sem provisão", "despesas anuais 0 vem antes da reserva na ordem da fonte")
f = cenario("dentro", {**base, "B44": 5000}, par)["Folha do Mês"]; log(str(f["B90"].value).startswith("Mês dentro das réguas") and f["B87"].value == "Apertado", "nada dispara: mês dentro das réguas; fôlego 2,6 = apertado")
f = cenario("naofecha", {**base, "B18": 15000, "B44": 5000}, par)["Folha do Mês"]; log(f["B78"].value == "não fecha" and f["B79"].value == "não fecha" and f["B85"].value.startswith("Cada noite vendida consome valor"), "margem por noite negativa: não fecha")
f = cenario("depr", {**base, "B39": 800}, par)["Folha do Mês"]; log(perto(f["B69"].value, 4269.20 - 800) and perto(f["B68"].value, 3862.23), "depreciação informada: só o indicativo muda; reserva não soma com ela")
f = cenario("caixa", {**base, "B43": 20000}, par)["Folha do Mês"]; log(f["B89"].value.startswith("Caixa ruim e resultado bom"), "saldo caiu e resultado positivo")
f = cenario("quebraR", {**base, "B22": 300}, par)["Folha do Mês"]; log(f["B59"].value == 300 and perto(f["B60"].value, 2062.40 - 162.40 + 300), "quebra em R$ substitui a referência")
print(f"\n{ok} ok, {fal} falhou"); sys.exit(1 if fal else 0)

"""Testa a planilha Mapa das Fontes recalculando no LibreOffice e comparando com uma conta independente em Python.
Uso: python3 -I tests/test_planilha.py dist"""
import sys, pathlib, subprocess, tempfile
from openpyxl import load_workbook
D = pathlib.Path(sys.argv[1]); ok = fal = 0
BR, EXN = "Mapa-das-Fontes-de-Capital-Zion-EM-BRANCO.xlsx", "Mapa-das-Fontes-de-Capital-Zion-EXEMPLO.xlsx"
def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)
def recalc(path):
    t = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(t), str(path)], check=True, capture_output=True, timeout=180)
    return load_workbook(t / path.name, data_only=True)
def cenario(nome, valores, base=BR):
    wb = load_workbook(D / base)
    for (aba, cel), v in valores.items(): wb[aba][cel] = v
    p = pathlib.Path(tempfile.mkdtemp()) / f"t_{nome}.xlsx"; wb.save(p); return recalc(p)
def perto(a, b, tol=0.01): return isinstance(a, (int, float)) and abs(a - b) < tol

# ---- conta independente (regras do Z02 Cap. 5 e do B04) ----
def referencia(capex, terreno, fixo, meses, rampa, pres, capt, proprio, terra, parcela, taxa, prazo):
    giro = fixo * meses + rampa; reserva = capex * pres
    total = capex + terreno + giro + reserva + capt; lacuna = max(0.0, total - proprio)
    pv = sum(parcela / (1 + taxa) ** k for k in range(1, prazo + 1))  # soma das parcelas descontadas, sem a fórmula fechada
    return dict(giro=giro, reserva=reserva, total=total, lacuna=lacuna, cob=proprio / total, incompleto=max(0, capex + terreno - proprio),
                terra=terra / lacuna, pv=pv, parte=min(pv, lacuna))

print("Exemplo preenchido (dados fictícios)")
wb = recalc(D / EXN); n, f, p, s = wb["Necessidade"], wb["Fontes"], wb["Prontidão"], wb["Próximos passos"]
r = referencia(240000, 0, 9000, 3, 12000, 0.12, 7200, 3000, 200000, 1500, 0.015, 120)
log(perto(n["B10"].value, r["giro"]), f"capital de giro = {n['B10'].value:,.2f} (ref. {r['giro']:,.2f})")
log(perto(n["B12"].value, r["reserva"]), f"reserva de implantação = {n['B12'].value:,.2f} (ref. {r['reserva']:,.2f})")
log(perto(n["B14"].value, r["total"]), f"total necessário = {n['B14'].value:,.2f} (ref. {r['total']:,.2f})")
log(perto(n["B16"].value, r["lacuna"]), f"lacuna = {n['B16'].value:,.2f} (ref. {r['lacuna']:,.2f})")
log(perto(n["B17"].value, r["cob"], 1e-6), f"cobertura própria = {n['B17'].value:.2%}")
log(perto(n["B18"].value, r["incompleto"]) and perto(n["B19"].value, r["lacuna"] - r["incompleto"]), f"pedido incompleto {n['B18'].value:,.2f}; faltaria no meio {n['B19'].value:,.2f}")
log(perto(n["B23"].value, r["terra"], 1e-4), f"terra ÷ lacuna = {n['B23'].value:.2f}×")
log(perto(n["B29"].value, r["pv"]), f"valor financiável = {n['B29'].value:,.2f} (ref. por soma descontada {r['pv']:,.2f})")
log(perto(n["B30"].value, r["parte"]), "parte da lacuna coberta pelo crédito = valor financiável (menor que a lacuna)")
log("fôlego" in str(n["B31"].value), "aviso do teste de fôlego aparece")
soma = 60000 + 83000 + 150000 + 0  # só Disponível e Possível
log(perto(f["B14"].value, r["lacuna"]) and perto(f["B15"].value, soma), f"fontes: lacuna {f['B14'].value:,.2f}, soma considerada {f['B15'].value:,.2f} (ref. {soma:,.2f})")
log(perto(f["B16"].value, soma / r["lacuna"], 1e-6) and perto(f["B17"].value, r["lacuna"] - soma), f"cobertura {f['B16'].value:.1%}, descoberto {f['B17'].value:,.2f}")
log(f["B18"].value == 6 and f["B19"].value == 2, "6 fontes classificadas, 2 fora")
log(str(f["B20"].value).startswith("Ainda falta"), "leitura do mapa: " + str(f["B20"].value))
log(f["H9"].value == 0 and f["H11"].value == 0, "fonte marcada Fora não entra na soma")
log(p["B17"].value == 10 and p["B18"].value == 4 and perto(p["B19"].value, 0.4, 1e-9), "prontidão: 10 respondidos, 4 Sim, 40%")
log(str(p["B20"].value).startswith("Estruturar antes"), "leitura do portão: " + str(p["B20"].value))
log(s["E6"].value == "Concluído" and s["E7"].value == "Em aberto", "próximos passos: situação calculada")

print("Versão em branco e casos de borda")
wb = recalc(D / BR); n, f, p, s = wb["Necessidade"], wb["Fontes"], wb["Prontidão"], wb["Próximos passos"]
log(all(n[c].value in (None, "") for c in ("B10", "B12", "B14", "B16", "B17", "B23", "B29")), "em branco: nenhum resultado na Necessidade")
log(f["B20"].value == "Classifique as seis fontes" and p["B20"].value == "Responda os 10 itens", "em branco: leituras pedem preenchimento")
log(s["E6"].value in (None, ""), "em branco: próximos passos vazios")
t = cenario("sobra", {("Necessidade", "B5"): 100000, ("Necessidade", "B15"): 500000})["Necessidade"]
log(t["B16"].value == 0, "capital próprio maior que o total: lacuna 0, nunca negativa")
t = cenario("sem_giro", {("Necessidade", "B5"): 100000, ("Necessidade", "B7"): 5000})["Necessidade"]
log(perto(t["B10"].value, 15000) and perto(t["B14"].value, 115000), "meses de giro vazio assume 3 (Régua)")
t = cenario("taxa0", {("Necessidade", "B5"): 100000, ("Necessidade", "B26"): 1000, ("Necessidade", "B28"): 60})["Necessidade"]
log(t["B29"].value in (None, "") and "Preencha" in str(t["B31"].value), "taxa vazia: sem divisão por zero, pede a simulação")
t = cenario("credito_maior", {("Necessidade", "B5"): 10000, ("Necessidade", "B26"): 5000, ("Necessidade", "B27"): 0.01, ("Necessidade", "B28"): 120})["Necessidade"]
log(perto(t["B30"].value, t["B16"].value), "crédito maior que a lacuna: cobre só a lacuna")
vals = {("Necessidade", "B5"): 100000, **{("Fontes", f"D{6+i}"): "Disponível" for i in range(6)}, **{("Fontes", f"E{6+i}"): 30000 for i in range(6)}}
t = cenario("cobre", vals)["Fontes"]
log(perto(t["B16"].value, 1.0, 1e-9) and t["B17"].value == 0 and str(t["B20"].value).startswith("O mapa cobre"), "fontes acima da lacuna: cobertura 100%, descoberto 0")
t = cenario("pronto", {("Prontidão", f"B{6+i}"): "Sim" for i in range(10)})["Prontidão"]
log(str(t["B20"].value).startswith("Pronto para conversar") and perto(t["B19"].value, 1, 1e-9), "10 Sim: pronto para conversar, com assessoria")
t = cenario("um_nao", {**{("Prontidão", f"B{6+i}"): "Sim" for i in range(10)}, ("Prontidão", "B10"): "Não"})["Prontidão"]
log(str(t["B20"].value).startswith("Estruturar"), "um único Não basta para estruturar antes de captar")
t = cenario("sem_data", {("Próximos passos", "A6"): "Ação qualquer"})["Próximos passos"]
log(t["E6"].value == "Defina a data", "ação sem data pede data")
print(f"\n{ok} passaram, {fal} falharam"); sys.exit(1 if fal else 0)

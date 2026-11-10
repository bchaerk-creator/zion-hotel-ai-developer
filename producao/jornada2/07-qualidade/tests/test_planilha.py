"""Testa a planilha Qualidade e Reputação recalculando no LibreOffice e comparando com uma conta independente em Python.
Uso: python3 -I tests/test_planilha.py <pasta com os xlsx>"""
import sys, pathlib, subprocess, tempfile, datetime as dt
from openpyxl import load_workbook
D = pathlib.Path(sys.argv[1]); ok = fal = 0
BRANCO, EXEMPLO = "Qualidade-e-Reputacao-Zion-EM-BRANCO.xlsx", "Qualidade-e-Reputacao-Zion-EXEMPLO.xlsx"
def log(b, m):
    global ok, fal; ok += bool(b); fal += (not b); print(("  ok  " if b else "  FALHOU  ") + m)
def recalc(path):
    t = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(t), str(path)], check=True, capture_output=True, timeout=180)
    return load_workbook(t / path.name, data_only=True)
def cenario(nome, mud, base=EXEMPLO):
    wb = load_workbook(D / base)
    for (aba, cel), v in mud.items(): wb[aba][cel] = v
    x = pathlib.Path(tempfile.mkdtemp()) / ("t_" + nome + ".xlsx"); wb.save(x); return recalc(x)
def dia(v): return v.date() if isinstance(v, dt.datetime) else v
perto = lambda a, b, tol=1e-6: a is not None and abs(a - b) <= tol

# ---- conta independente (não usa a planilha nem o logic.js) ----
CANAIS = [(24, 4.7, 16, 44), (9, 4.6, 5, 13), (5, 4.9, 4, 15)]
def reputacao(canais, escala=5):
    n = sum(c[0] for c in canais); nota = sum(c[0] * c[1] for c in canais) / n
    taxa = sum(c[2] for c in canais) / sum(c[3] for c in canais)
    ruim = 3 if escala == 5 else 6
    apos = (nota * n + ruim) / (n + 1)
    return dict(n=n, nota=nota, taxa=taxa, apos=apos, queda=nota - apos)
def excecao(nota, seg, fora, gasto, prev, nmin=4.7, pct=10):
    return (nota is not None and nota < nmin) or seg > 0 or fora > 0 or (prev > 0 and gasto > prev * (1 + pct / 100))
def leitura_teste(op, nm, ocup, nota, contatos, externa, tol=0.1):
    if nota < nm - tol - 1e-6: return "nota"
    if ocup < op and externa != "Sim": return "ocupacao"
    if ocup < op: return "externa"
    if contatos > 2: return "criterio"
    return "passou"

print("1. Exemplo preenchido (dados fictícios, PLANO seção 9)")
wb = recalc(D / EXEMPLO); a = wb["Avaliações por canal"]; r = reputacao(CANAIS)
log(a["B18"].value == "OK", "situação dos dados OK")
log(a["B20"].value == r["n"] == 38 and perto(a["B21"].value, r["nota"]) and round(a["B21"].value, 2) == 4.70, f"38 avaliações, nota geral ponderada {a['B21'].value:.4f} (178,7 ÷ 38 = 4,70)")
log(perto(a["B22"].value, r["taxa"]) and round(r["taxa"] * 100, 1) == 34.7 and a["B23"].value.startswith("Abaixo do mínimo"), "taxa de avaliação 25 ÷ 72 = 34,7%, abaixo dos 40%")
log(perto(a["B24"].value, r["apos"]) and round(a["B24"].value, 2) == 4.66 and perto(a["B25"].value, r["queda"]), "uma avaliação de 3 leva a média a 4,66 (a mesma da ficha)")
log(round(a["B26"].value, 2) == 0.10 and a["B27"].value == "Abaixo da meta" and round(a["B28"].value, 2) == 0.10, "0,1 ponto da meta de 4,8; 0,1 acima dos concorrentes (4,6)")
c = wb["Críticas"]; itens = ["Ralo", "Wi-Fi", "Placa", "Ralo", "Toalha", "Wi-Fi", "Ralo"]
esp = [itens.count(i) for i in itens]
log([c.cell(l, 6).value for l in range(8, 15)] == esp == [3, 2, 1, 3, 1, 2, 3], "menções no trimestre por item: ralo 3, Wi-Fi 2, placa 1, toalha 1")
log(sum(1 for l in range(8, 15) if c.cell(l, 7).value.startswith("PROBLEMA")) == 3 and c["B39"].value == 7 and c["B40"].value == 1 and c["B41"].value == 5 and c["B42"].value == "OK", "7 críticas no trimestre, 1 item com três menções (com ajuste e prazo), 5 em avaliação boa")
log(dia(c["B5"].value) == dt.date(2026, 10, 31), "trimestre de 01/08 a 31/10/2026")
p = wb["Painel semanal"]
PX = [(4.8, 0, 0, 950, 1000), (4.5, 0, 0, 1020, 1000), (4.9, 0, 0, 980, 1000), (4.7, 0, 0, 1150, 1000)]
lei = [p.cell(9 + k, 11).value for k in range(4)]
log([x.startswith("EXCEÇÃO") for x in lei] == [excecao(*x) for x in PX] == [False, True, False, True], "painel: semana com nota 4,5 e semana com gasto 15% acima são exceção")
log(lei[2] == "Atenção: avaliação sem resposta" and lei[0] == "Relatório semanal" and p.cell(13, 11).value in (None, ""), "semana com avaliação sem resposta: atenção; linha vazia sem leitura")
log(p["B23"].value == 4 and p["B24"].value == 2 and p["B25"].value == 1 and p["B26"].value == 40 and p["B27"].value == 4 and p["B28"].value == "OK", "4 semanas, 2 exceções, 1 avaliação sem resposta, resposta média de 40 min (= ficha), 4 ocorrências")
t = wb["Teste de prontidão"]
log(dia(t["B6"].value) == dt.date(2027, 6, 27) and t["B20"].value == "Teste agendado" and t["B21"].value == "Lance os resultados depois de 27/06/2027", "teste de 14/06 a 27/06/2027 agendado; resultados depois")
s = wb["Plano de saída"]
FAS = [(dt.date(2026, 11, 16), dt.date(2027, 1, 10), 8), (dt.date(2027, 1, 11), dt.date(2027, 3, 7), 8), (dt.date(2027, 3, 8), dt.date(2027, 6, 13), 14), (dt.date(2027, 6, 14), dt.date(2027, 6, 27), 2)]
log([(dia(s.cell(l, 2).value), dia(s.cell(l, 3).value), s.cell(l, 4).value) for l in range(10, 14)] == FAS, "quatro fases: 16/11/2026 a 10/01/2027, 11/01 a 07/03, 08/03 a 13/06 (14 semanas), 14/06 a 27/06/2027")
log(s["B15"].value == round(224 / 30.4375, 1) == 7.4 and s["B16"].value == "OK", "7,4 meses do início ao fim do teste; situação OK")
log(s["B25"].value == "Agora não: faltam 3 de 4 condições", "segunda unidade: agora não, faltam 3 de 4")
log([dia(s.cell(l, 2).value) for l in range(28, 33)] == [dt.date(2027, 1, 11), dt.date(2027, 4, 11), dt.date(2027, 7, 11), dt.date(2027, 10, 11), dt.date(2027, 11, 8)] and s["B33"].value == 5, "rotina do ano: trimestrais 11/01, 11/04, 11/07, 11/10/2027; anual 08/11/2027; Folha no dia 5")

print("2. Versão em branco")
wb = recalc(D / BRANCO)
log(wb["Avaliações por canal"]["B18"].value.startswith("Preencha pelo menos um canal") and wb["Avaliações por canal"]["B21"].value in (None, ""), "em branco: pede um canal e não calcula a nota")
log(wb["Avaliações por canal"]["B4"].value == 5 and wb["Avaliações por canal"]["B7"].value == 0.4 and wb["Avaliações por canal"]["B8"].value == 60, "referências da fonte já preenchidas: escala 5, taxa 40%, resposta 60 min")
log(wb["Críticas"]["B42"].value == "Informe o início do trimestre" and wb["Painel semanal"]["B28"].value.startswith("Defina a nota mínima"), "críticas e painel pedem preenchimento")
log(wb["Teste de prontidão"]["B20"].value.startswith("Marque a data") and wb["Plano de saída"]["B16"].value.startswith("Marque o início"), "teste e plano pedem as datas")
log(wb["Plano de saída"]["B25"].value == "Responda as quatro condições", "segunda unidade pede as quatro condições")

print("3. Cenários e bloqueios (conta independente)")
w = cenario("nota_fora", {("Avaliações por canal", "C13"): 5.3}); log(w["Avaliações por canal"]["B18"].value == "Há nota fora da escala", "nota acima da escala bloqueia")
w = cenario("mais_aval", {("Avaliações por canal", "D12"): 50}); log(w["Avaliações por canal"]["B18"].value.startswith("Há canal com mais avaliações que estadias"), "mais avaliações que estadias bloqueia")
w = cenario("min_meta", {("Avaliações por canal", "B6"): 4.9}); log(w["Avaliações por canal"]["B18"].value == "A nota mínima passa da meta", "nota mínima acima da meta bloqueia")
w = cenario("sem_nota", {("Avaliações por canal", "C14"): None}); log(w["Avaliações por canal"]["B18"].value == "Há canal com avaliações e sem nota", "canal com avaliações e sem nota bloqueia")
c10 = [(24, 9.4, 16, 44), (9, 9.2, 5, 13), (5, 9.8, 4, 15)]
w = cenario("escala10", {("Avaliações por canal", "B4"): 10, ("Avaliações por canal", "B5"): 9.6, ("Avaliações por canal", "B6"): 9.4, ("Avaliações por canal", "B9"): 9.2,
                          ("Avaliações por canal", "C12"): 9.4, ("Avaliações por canal", "C13"): 9.2, ("Avaliações por canal", "C14"): 9.8}); r10 = reputacao(c10, 10)
log(w["Avaliações por canal"]["B18"].value == "OK" and perto(w["Avaliações por canal"]["B24"].value, r10["apos"]) and w["Teste de prontidão"]["B19"].value == 0.2, "escala de 10: avaliação ruim = 6; tolerância 0,2 no teste")
w = cenario("abaixo_min", {("Avaliações por canal", "C12"): 4.5}); nota = (24 * 4.5 + 9 * 4.6 + 5 * 4.9) / 38
log(perto(w["Avaliações por canal"]["B21"].value, nota) and w["Avaliações por canal"]["B27"].value == "EXCEÇÃO: abaixo da nota mínima", f"nota geral {nota:.2f} abaixo da mínima: exceção")
w = cenario("sem_ajuste", {("Críticas", "H8"): None}); log(w["Críticas"]["B42"].value == "Falta o ajuste de produto do item com três menções", "item com três menções sem ajuste: situação aponta")
w = cenario("fora_tri", {("Críticas", "A14"): dt.date(2026, 11, 5)}); log(w["Críticas"]["F8"].value == 2 and w["Críticas"]["B40"].value == 0 and w["Críticas"]["B39"].value == 6 and w["Críticas"]["F14"].value == 2, "crítica fora do trimestre não conta: ralo cai para 2 menções, nenhum item com três")
# painel: cenários de exceção e atenção
mud = {("Painel semanal", "B6"): 5}
linhas = [(4.6, 1, 1, 30, 0, 0, 0, 100, 100), (4.8, 1, 1, 30, 0, 1, 0, 100, 100), (4.8, 1, 1, 30, 0, 0, 1, 100, 100), (4.8, 1, 1, 30, 0, 0, 0, 106, 100), (4.8, 1, 1, 30, 0, 0, 0, 105, 100), (4.8, 2, 1, 75, 0, 0, 0, 100, 100), (None, 0, 0, 90, 0, 0, 0, 0, 0)]
for k, (n, rec, resp, tm, oc, seg, fora, g, pv) in enumerate(linhas):
    l = 9 + k
    for col, v in zip("ABCDEFGHIJ", [dt.date(2027, 1, 4) + dt.timedelta(7 * k), n, rec, resp, tm, oc, seg, fora, g, pv]): mud[("Painel semanal", f"{col}{l}")] = v
for l in range(9 + len(linhas), 9 + 13):
    for col in "ABCDEFGHIJ": mud[("Painel semanal", f"{col}{l}")] = None
w = cenario("painel", mud); pe = w["Painel semanal"]
got = [pe.cell(9 + k, 11).value for k in range(len(linhas))]
esp = [excecao(n, seg, fora, g, pv, 4.7, 5) for n, rec, resp, tm, oc, seg, fora, g, pv in linhas]
log([x.startswith("EXCEÇÃO") for x in got] == esp == [True, True, True, True, False, False, False], "painel: nota 4,6, segurança, fora da alçada e gasto 6% acima são exceção; 5% exatos não")
log(got[5] == "Atenção: avaliação sem resposta; resposta acima do máximo" and got[6] == "Atenção: resposta acima do máximo", "atenção: avaliação sem resposta e resposta de 75 e 90 min acima de 60")
# teste de prontidão: leitura pela régua da fonte
casos = [(0.52, 4.8, 1, None, "passou"), (0.50, 4.6, 2, None, "passou"), (0.52, 4.8, 3, None, "criterio"), (0.52, 4.5, 0, None, "nota"), (0.40, 4.8, 0, "Não", "ocupacao"), (0.40, 4.8, 0, "Sim", "externa"), (0.40, 4.4, 5, "Não", "nota")]
pref = {"passou": "PASSOU", "criterio": "Ocupação e nota mantidas", "nota": "A nota caiu", "ocupacao": "A ocupação caiu sem causa externa", "externa": "A ocupação caiu por causa externa"}
okc = True
for oc, nota, cont, ext, esperado in casos:
    w = cenario(f"teste_{oc}_{nota}_{cont}_{ext}", {("Teste de prontidão", "B13"): oc, ("Teste de prontidão", "B14"): nota, ("Teste de prontidão", "B15"): cont, ("Teste de prontidão", "B16"): ext})
    lido = w["Teste de prontidão"]["B21"].value; indep = leitura_teste(0.50, 4.7, oc, nota, cont, ext)
    if not (indep == esperado and lido.startswith(pref[esperado])): okc = False; print("     caso", oc, nota, cont, ext, lido, indep)
log(okc, "teste: passou (inclusive 4,6 dentro da tolerância), muitos contatos, nota caiu, ocupação caiu com e sem causa externa, prioridade da nota")
w = cenario("nao_medio", {("Teste de prontidão", "B10"): "Não"}); log(w["Teste de prontidão"]["B20"].value.startswith("Escolha um período de ocupação média"), "período que não é de ocupação média: situação aponta")
# plano de saída
w = cenario("teste_cedo", {("Teste de prontidão", "B5"): dt.date(2027, 3, 1)}); log(w["Plano de saída"]["B16"].value.startswith("O teste começa antes do fim da Fase 2"), "teste antes do fim da Fase 2: situação aponta")
w = cenario("f3_curta", {("Teste de prontidão", "B5"): dt.date(2027, 4, 12)}); s = w["Plano de saída"]
log(s["D12"].value == 5 and s["B16"].value.startswith("A Fase 3 tem menos de 8 semanas"), "Fase 3 com 5 semanas: situação aponta")
w = cenario("longo", {("Teste de prontidão", "B5"): dt.date(2027, 9, 6)}); s = w["Plano de saída"]
dias = (dt.date(2027, 9, 19) - dt.date(2026, 11, 16)).days + 1
log(s["B15"].value == round(dias / 30.4375, 1) and s["B16"].value.startswith("Fora dos seis a oito meses"), f"teste em setembro: {s['B15'].value} meses, fora dos seis a oito da fonte")
w = cenario("virada", {("Plano de saída", "B4"): dt.date(2026, 12, 28), ("Plano de saída", "B5"): 6, ("Teste de prontidão", "B5"): dt.date(2027, 6, 7)}); s = w["Plano de saída"]
log(dia(s["C10"].value) == dt.date(2027, 2, 7) and dia(s["B11"].value) == dt.date(2027, 2, 8), "fases atravessam a virada do ano (Fase 1 de 28/12/2026 a 07/02/2027)")
w = cenario("quatro", {("Plano de saída", f"B{l}"): "Sim" for l in range(21, 25)}); log(w["Plano de saída"]["B25"].value == "Pode estudar a segunda unidade", "quatro condições: pode estudar a segunda unidade")
w = cenario("tri_fev", {("Plano de saída", "B28"): dt.date(2027, 11, 30)}); log(dia(w["Plano de saída"]["B29"].value) == dt.date(2028, 2, 29), "trimestral de 30/11/2027 cai em 29/02/2028 (ano bissexto)")

print(f"\n{ok} ok, {fal} falhou"); sys.exit(1 if fal else 0)

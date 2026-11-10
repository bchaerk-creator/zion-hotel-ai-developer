"""Testa a planilha Plano de Captação recalculando no LibreOffice e comparando com uma conta independente em Python.
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
def perto(a, b, tol=0.005): return isinstance(a, (int, float)) and abs(a - b) <= tol
BRANCO, EXEMPLO = "Plano-de-Captacao-Zion-EM-BRANCO.xlsx", "Plano-de-Captacao-Zion-EXEMPLO.xlsx"
MA, CA, LI, DOZE = "Marca em uma folha", "Captação do mês", "Lista própria", "Captação 12 meses"
def cenario(nome, celulas, base=BRANCO):
    wb = load_workbook(D / base)
    for aba, cel, v in celulas: wb[aba][cel] = v
    x = pathlib.Path(tempfile.mkdtemp()) / ("t_" + nome + ".xlsx"); wb.save(x); return recalc(x)

# ---- conta independente (não usa a planilha nem o logic.js) ----
CANAIS = [("Plataforma A", "Plataforma", 16, 0, 12, 8120), ("Plataforma B", "Plataforma", 15, 0, 5, 3248), ("Instagram com impulsionamento", "Direto", 0, 150, 2, 1120),
          ("Hóspede que volta (WhatsApp)", "Direto", 0, 0, 3, 1848), ("Indicação", "Direto", 0, 0, 3, 1904)]
def conta(canais, meta):
    L = []
    for nome, tipo, com, gas, res, rec in canais:
        cv = rec * com / 100 if tipo == "Plataforma" else 0
        L.append(dict(nome=nome, tipo=tipo, com=cv, custo=cv + gas, cpr=(cv + gas) / res if res else None, res=res, rec=rec))
    rec = sum(l["rec"] for l in L); res = sum(l["res"] for l in L); custo = sum(l["custo"] for l in L)
    rd = sum(l["rec"] for l in L if l["tipo"] == "Direto"); resd = sum(l["res"] for l in L if l["tipo"] == "Direto")
    rp = sum(l["rec"] for l in L if l["tipo"] == "Plataforma"); cp = sum(l["com"] for l in L if l["tipo"] == "Plataforma")
    cm = cp / rp if rp else None; rmeta = rec * meta / 100
    ev = max(0, rmeta - rd) * cm if cm is not None else None
    com_cpr = [l for l in L if l["cpr"] is not None]
    return dict(L=L, rec=rec, res=res, custo=custo, cpr=custo / res, rd=rd, resd=resd, vd=rd / rec, vdr=resd / res, cm=cm, cs=custo / rec, rmeta=rmeta, ev=ev,
                barato=min(com_cpr, key=lambda l: l["cpr"])["nome"], caro=max(com_cpr, key=lambda l: l["cpr"])["nome"])
ADJ = ["aconchegante", "único", "única", "especial", "exclusiv", "inesquecível", "incrível", "perfeit"]
def tem_adj(t): return any(a in t.lower() for a in ADJ)

print("Exemplo preenchido (dados fictícios, PLANO seção 9)")
wb = recalc(D / EXEMPLO); c = wb[CA]; k = conta(CANAIS, 40)
log(c["B32"].value == "OK", f"situação dos dados OK ({c['B32'].value})")
for i, l in enumerate(k["L"]):
    r = 7 + i
    log(perto(c[f"G{r}"].value, l["com"]) and perto(c[f"H{r}"].value, l["custo"]) and perto(c[f"I{r}"].value, l["cpr"]), f"{l['nome']}: comissão {c[f'G{r}'].value}, custo {c[f'H{r}'].value}, por reserva {c[f'I{r}'].value:.2f}")
log(perto(c["E15"].value, 25) and perto(c["F15"].value, 16240) and perto(c["H15"].value, k["custo"]) and perto(c["I15"].value, k["cpr"]) and round(k["cpr"], 2) == 77.46, f"total: 25 reservas, R$ 16.240, custo R$ {c['H15'].value:.2f}, R$ {c['I15'].value:.2f} por reserva (ref 77,46)")
log(perto(c["B18"].value, 4872) and c["B19"].value == 8 and perto(c["B20"].value, 0.30, 1e-9) and perto(c["B21"].value, 0.32, 1e-9), "venda direta: R$ 4.872, 8 reservas, 30% da receita, 32% das reservas")
log(perto(c["B22"].value, k["cm"], 1e-9) and perto(c["B23"].value, k["cs"], 1e-9) and round(k["cs"] * 100, 1) == 11.9, f"comissão média das plataformas {c['B22'].value:.4f}; captação 11,9% da receita")
log(perto(c["B26"].value, 6496) and perto(c["B27"].value, k["ev"]) and round(k["ev"], 2) == 255.20, f"meta 40%: R$ {c['B26'].value:.2f}; comissão que deixaria de sair R$ {c['B27'].value:.2f} (ref 255,20, igual ao Módulo 3)")
log(c["B28"].value == k["barato"] and c["B29"].value == k["caro"] == "Plataforma A", f"menor custo: {c['B28'].value}; maior: {c['B29'].value}")
log(c["B30"].value.startswith("OK"), "meta acima da venda direta de hoje")
m = wb[MA]
log(m["B26"].value == "4 de 4" and m["B27"].value.startswith("OK") and m["B28"].value == 4, "marca: 4 de 4 testes, sem adjetivo, falta em 4 pontos")
log(m["B29"].value == "Reescreva: nem todos entenderam (a frase ainda não existe)", "marca: 4 de 5 pessoas pede reescrever (como a ficha)")
li = wb[LI]
log(li["H2"].value == 64 and li["H3"].value == 0 and li["H4"].value == 120 and perto(li["H5"].value, 10) and perto(li["H6"].value, 0.4) and li["H8"].value == "OK", "lista: 64 contatos, 0 autorizados, faltam 120, 10 por mês, 40% das estadias (igual à ficha)")
p = wb[DOZE]
log(perto(p["G5"].value, 0.30, 1e-9) and perto(p["H5"].value, 77.456) and p["I5"].value == "Abaixo da meta", "12 meses: outubro 30%, R$ 77,46, abaixo da meta")
log(perto(p["G6"].value, 4144 / 12950, 1e-9) and perto(p["H6"].value, 1533.8 / 21) and p["I6"].value == "Abaixo da meta" and p["I7"].value in (None, ""), "12 meses: novembro 32%, R$ 73,04, linha vazia em branco")

print("Versão em branco")
wb = recalc(D / BRANCO)
log(wb[CA]["B32"].value == "Preencha o mês" and wb[CA]["I15"].value in (None, "") and wb[CA]["B26"].value in (None, ""), "captação vazia: pede o mês, sem contas")
log(wb[MA]["B29"].value == "Preencha para quem, promessa, prova e tom" and wb[MA]["B27"].value in (None, ""), "marca vazia")
log(wb[LI]["H8"].value.startswith("Preencha") and wb[LI]["H2"].value == 0, "lista vazia")
log(wb[DOZE]["G5"].value in (None, "") and wb[DOZE]["I5"].value in (None, ""), "12 meses vazio")

print("Cenários de bloqueio e de leitura (recalculados no LibreOffice)")
def canais(lst, mes="Dez", meta=40):
    cel = [(CA, "B4", mes)]
    if meta is not None: cel.append((CA, "B24", meta))
    for i, row in enumerate(lst):
        for col, v in zip("ABCDEF", row):
            if v is not None: cel.append((CA, f"{col}{7+i}", v))
    return cel
casos = [
    ("semMes", canais(CANAIS, mes=None), "Preencha o mês"),
    ("semTipo", canais([("X", "Outro", 0, 0, 1, 100)]), "Escolha Plataforma ou Direto em cada canal"),
    ("semNome", canais([(None, "Direto", 0, 0, 2, 100)]), "Preencha pelo menos um canal"),
    ("linhaSemNome", canais([CANAIS[0], (None, None, None, None, 3, None)]), "Dê nome ao canal ou apague a linha"),
    ("semReceita", canais([("X", "Direto", 0, 0, 2, None)]), "Faltam reservas ou receita em algum canal (0 vale)"),
    ("negativo", canais([("X", "Direto", 0, -10, 2, 300)]), "Valor negativo ou comissão de 100% ou mais"),
    ("comissao100", canais([("X", "Plataforma", 100, 0, 2, 300)]), "Valor negativo ou comissão de 100% ou mais"),
    ("fracao", canais([("X", "Direto", 0, 0, 2.5, 300)]), "Reservas: número inteiro"),
    ("receitaSemReserva", canais([("X", "Direto", 0, 0, 0, 300)]), "Há receita sem reserva em algum canal"),
    ("tudoZero", canais([("X", "Direto", 0, 50, 0, 0)]), "Sem reservas ou sem receita no mês"),
    ("semMeta", canais(CANAIS, meta=None), "Escreva a meta de venda direta (de 0 a 100)"),
    ("meta120", canais(CANAIS, meta=120), "Escreva a meta de venda direta (de 0 a 100)"),
]
for nome, cel, esperado in casos:
    w = cenario(nome, cel); v = w[CA]["B32"].value
    log(v == esperado, f"{nome}: situação = {v!r}")
# só plataformas: venda direta 0 e nenhuma comissão evitada além da conta
so = [CANAIS[0], CANAIS[1]]; ks = conta(so, 20)
w = cenario("soPlataformas", canais(so, meta=20)); cc = w[CA]
log(cc["B32"].value == "OK" and cc["B20"].value == 0 and perto(cc["B27"].value, ks["ev"]) and perto(cc["I15"].value, ks["cpr"]), f"só plataformas: venda direta 0%, comissão evitada R$ {cc['B27'].value:.2f} (ref {ks['ev']:.2f})")
# esforço direto caro + gasto sem reserva
caro = CANAIS[:2] + [("Anúncio pago", "Direto", 0, 400, 2, 600), ("Panfleto", "Direto", 0, 80, 0, 0)]; kc = conta(caro, 40)
w = cenario("caro", canais(caro)); cc = w[CA]
log(cc["B32"].value == "OK" and perto(cc["I9"].value, 200) and cc["I10"].value in (None, "") and cc["B29"].value == "Anúncio pago" and perto(cc["H10"].value, 80), "anúncio R$ 200 por reserva é o mais caro; panfleto sem reserva: custo sem custo por reserva")
log(perto(cc["H15"].value, kc["custo"]) and perto(cc["I15"].value, kc["cpr"]), f"totais com gasto sem reserva: R$ {cc['H15'].value:.2f}, R$ {cc['I15'].value:.2f} por reserva")
w = cenario("metaAbaixo", canais(CANAIS, meta=25))
log(w[CA]["B30"].value.startswith("Atenção") and w[CA]["B27"].value == 0, "meta 25% abaixo da venda direta 30%: atenção e nenhuma comissão evitada")
# marca
base_marca = [(MA, "B4", "Casais"), (MA, "B6", "Duas noites a dois com a lareira acesa"), (MA, "B13", "Foto da lareira"), (MA, "B14", "Próximo")] + [(MA, f"B{18+i}", "Já aparece") for i in range(6)]
testes_sim = [(MA, f"B{7+i}", "Sim") for i in range(4)]
for nome, cel, esperado in [
    ("marcaTestes", base_marca, "Responda os quatro testes"),
    ("marcaFalhou", base_marca + testes_sim[:3] + [(MA, "B10", "Não")], "Reescreva a promessa: ela falhou em algum teste"),
    ("marcaSemCinco", base_marca + testes_sim, "Teste a promessa com cinco pessoas de fora"),
    ("marcaPontos", base_marca[:4] + testes_sim + [(MA, "B11", 5)], "Marque os seis pontos de contato"),
    ("marcaOk", base_marca + testes_sim + [(MA, "B11", 5)], "OK"),
]:
    w = cenario(nome, cel); v = w[MA]["B29"].value
    log(v == esperado, f"{nome}: situação = {v!r}")
for frase in ["Cabana aconchegante com vista", "Experiência ÚNICA na serra", "Lugar perfeito para casais", "Duas noites a dois com a lareira acesa"]:
    w = cenario("adj", [(MA, "B6", frase)]); v = w[MA]["B27"].value
    log(v.startswith("Atenção") == tem_adj(frase), f"adjetivo em {frase!r}: {v}")
# lista
lb = [(LI, "B2", "Posso guardar o seu contato?"), (LI, "B3", "Planilha na nuvem"), (LI, "B5", "WhatsApp"), (LI, "B7", 30), (LI, "B8", 10)]
linhas = [(LI, f"A{14+i}", f"Hóspede {i+1}") for i in range(4)] + [(LI, f"I{14+i}", v) for i, v in enumerate(["Sim", "Não", "Sim", "Sim"])]
w = cenario("lista", lb + linhas); ll = w[LI]
log(ll["H2"].value == 4 and ll["H3"].value == 3 and ll["H4"].value == 27 and perto(ll["H5"].value, 2.25) and perto(ll["H6"].value, 0.225) and ll["H8"].value == "OK", "lista: 4 linhas, 3 Sim, faltam 27, 2,25 por mês, 22,5% das estadias")
w = cenario("listaSemAut", lb + linhas[:4] + linhas[4:6]); log(w[LI]["H8"].value == "Falta a autorização (Sim ou Não) em alguma linha", "linha sem autorização é apontada")
w = cenario("listaRitmo", lb[:3] + [(LI, "B7", 500), (LI, "B8", 10)]); log(w[LI]["H7"].value.startswith("Atenção") and perto(w[LI]["H6"].value, 500 / 12 / 10), "meta maior que as estadias: atenção")
w = cenario("listaMenor", lb[:3] + [(LI, "B7", 2), (LI, "B8", 10)] + linhas); log(w[LI]["H8"].value == "A meta é menor que os autorizados de hoje", "meta menor que os autorizados")
w = cenario("doze", [(CA, "B24", 25), (DOZE, "A5", "Jan"), (DOZE, "B5", 1000), (DOZE, "C5", 250), (DOZE, "D5", 4), (DOZE, "E5", 100)]); pp = w[DOZE]
log(pp["I5"].value == "Na meta" and perto(pp["G5"].value, 0.25, 1e-9) and perto(pp["H5"].value, 25), "12 meses: 25% com meta 25% = na meta (igual conta como na meta)")

print(f"\n{ok} ok, {fal} falhou"); sys.exit(1 if fal else 0)

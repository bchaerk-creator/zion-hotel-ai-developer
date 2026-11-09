"""Verificação independente dos valores esperados da suíte financeira (Comando 05D).

Implementação própria, em outra linguagem, a partir das DEFINIÇÕES do Dicionário Financeiro v0.4
e do Plano de Homologação v0.2. NÃO importa nem lê o código das ferramentas (ZAIOS, B06, B08, A09,
F05, Folha J2). Usa apenas DADOS de entrada: o perfil "iniciante" do B06 (JSON), os itens do exemplo
da F05 (literais de dados.py, lidos com ast, sem executar) e os campos do exemplo da Folha J2.

Uso: python3 -I verificacao_independente.py <resultado.json da suíte> [saida.md]
"""
import ast, json, math, pathlib, sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
DIAS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# ---------- definições do dicionário ----------
def operacao(unid, diaria, ocup, ded, cv_noite, fixo_mes, quebra=0.0, reserva=0.0, prolabore_mes=0.0, fatores=None):
    """Cascata anual somando 12 meses de calendário real (fatores = rampa por mês de operação)."""
    tot = dict(noites_disp=0, noites=0, bruta=0, ded=0, real=0, cv=0, quebra=0, fixos=0, op=0, ebitda=0, reserva=0, ger=0)
    for m in range(12):
        f = 1.0 if fatores is None else fatores[m]
        nd = unid * DIAS[m]; n = nd * ocup * f; b = n * diaria
        d = b * ded; r = b - d; q = b * quebra; cv = n * cv_noite + q
        fx = fixo_mes + prolabore_mes; op = r - cv - fx; res = b * reserva
        for k, v in dict(noites_disp=nd, noites=n, bruta=b, ded=d, real=r, cv=cv, quebra=q, fixos=fx, op=op, ebitda=op, reserva=res, ger=op - res).items():
            tot[k] += v
    return tot

def vpl(fluxo, i): return sum(v / (1 + i) ** t for t, v in enumerate(fluxo))

def tir(fluxo):
    """Secante/Newton numérica, método diferente da bisseção usada nas ferramentas."""
    r0, r1 = 0.05, 0.15
    for _ in range(200):
        f0, f1 = vpl(fluxo, r0), vpl(fluxo, r1)
        if f1 == f0: break
        r2 = r1 - f1 * (r1 - r0) / (f1 - f0)
        if abs(r2 - r1) < 1e-13: return r2
        r0, r1 = r1, max(r2, -0.99)
    return r1

def payback(fluxo, regime=None):
    """Primeiro ano com acumulado ≥ 0, interpolando dentro do ano; além do horizonte, estende pelo regime."""
    acc = 0.0
    for t, v in enumerate(fluxo):
        ant = acc; acc += v
        if t > 0 and acc >= 0: return t - 1 + (-ant) / v
    if regime and regime > 0: return len(fluxo) - 1 + (-acc) / regime
    return None

def equilibrio(o, fixo_ano):
    contrib = (o["real"] - o["cv"]) / o["noites"]
    n = fixo_ano / contrib
    return n, n / o["noites_disp"]

RAMPA = [0.4] * 3 + [0.5] * 3 + [0.75] * 6

# ---------- valores independentes por caso ----------
V = {}
z = operacao(3, 680, 0.38, 0.17, 80, 6000)
fz = [-900000] + [z["ger"]] * 10
V.update({"T1-ZAIOS-01": z["bruta"], "T1-ZAIOS-02": z["real"], "T1-ZAIOS-03": z["op"], "T1-ZAIOS-04": equilibrio(z, 72000)[1],
          "T1-ZAIOS-05": vpl(fz, 0.1), "T1-ZAIOS-06": tir(fz), "T1-ZAIOS-07": payback(fz), "T1-ZAIOS-09": z["ger"] / 900000})
for k, sfx in [("01", "T1-ZAIOS-01"), ("02", "T1-ZAIOS-02"), ("03", "T1-ZAIOS-03"), ("04", "T1-ZAIOS-04"), ("05", "T1-ZAIOS-05"), ("06", "T1-ZAIOS-06"), ("07", "T1-ZAIOS-07")]:
    V["T1-B08-" + k] = V[sfx]
V["T1-B08-09"] = V["T1-ZAIOS-09"]; V["T1-B08-10"] = (sum(fz[1:]) - 900000) / 900000
for k, sfx in [("01", "T1-ZAIOS-01"), ("02", "T1-ZAIOS-02"), ("03", "T1-ZAIOS-03"), ("04", "T1-ZAIOS-04")]:
    V["T1-A09-" + k] = V[sfx]
V["T1-A09-05"] = 900000 / z["op"]; V["T1-A09-06"] = z["op"] / 900000

for tag, fat in [("S", None), ("R", RAMPA)]:
    reg = operacao(3, 680, 0.38, 0.17, 80, 6000, quebra=0.01, reserva=0.03)
    a1 = operacao(3, 680, 0.38, 0.17, 80, 6000, quebra=0.01, reserva=0.03, fatores=fat) if fat else reg
    f = [-900000, a1["ger"]] + [reg["ger"]] * 9
    fs = f[:-1] + [f[-1] + 6 * reg["ebitda"]]
    V.update({f"T2-ZAIOS-{tag}1": reg["op"], f"T2-ZAIOS-{tag}2": reg["ger"], f"T2-ZAIOS-{tag}3": a1["ger"], f"T2-ZAIOS-{tag}4": vpl(f, 0.1),
              f"T2-ZAIOS-{tag}5": tir(f), f"T2-ZAIOS-{tag}6": payback(f, reg["ger"]), f"T2-ZAIOS-{tag}7": vpl(fs, 0.1)})

# F01 (P5): contingência sobre a base infra + obra + apoio
infra, proj, obra, apoio, ffe = 250000, 70000, 390000, 90000, 195000
base = infra + obra + apoio
V["T3-F01-01"] = infra + proj + obra + apoio + ffe + round(ffe * 0.12) + round(base * 0.05) + round(base * 0.25)
f2 = operacao(3, 680, 0.38, 0.17, 0, 10500)
n2, o2 = equilibrio(f2, 126000)
V.update({"T3-F02-01": f2["real"], "T3-F02-02": f2["op"], "T3-F02-03": n2, "T3-F02-04": o2})
c1 = [-1237400, -59071.13] + [34505.6] * 9
c1s = c1[:-1] + [c1[-1] + 6 * 52505.6]
V.update({"T3-F03-C1-1": vpl(c1, 0.1), "T3-F03-C1-2": payback(c1, 34505.6)})
# TIR do caso 1 com saída é negativa: a secante parte de chutes negativos
r0, r1 = -0.05, -0.12
for _ in range(200):
    a, b = vpl(c1s, r0), vpl(c1s, r1)
    if b == a or abs(r1 - r0) < 1e-13: break
    r2 = r1 - b * (r1 - r0) / (b - a); r0, r1 = r1, r2
V["T3-F03-C1-3"] = r1
c2 = [-1000000, 50000] + [200000] * 9
c2s = c2[:-1] + [c2[-1] + 6 * 230000]
disc = [v / 1.1 ** t for t, v in enumerate(c2)]
V.update({"T3-F03-C2-1": payback(c2), "T3-F03-C2-2": payback(disc), "T3-F03-C2-3": vpl(c2, 0.1), "T3-F03-C2-4": vpl(c2s, 0.1)})

# B06 perfil iniciante: dados do JSON, fórmulas do relatório de auditoria (construção, equipamentos, giro, contingência fora do giro)
prof = [p for p in json.loads((RAIZ / "producao/zion-arsenal/tests/profiles/B06.json").read_text())["profiles"] if p["name"] == "iniciante"][0]["values"]
num = lambda x: x if isinstance(x, (int, float)) else 0
lst = lambda k: sum(num(i.get("value")) for i in prof.get(k, []))
U = prof["unidades"]
constr = U * (num(prof.get("custo_unid")) + num(prof.get("frete_unid"))) + lst("comuns")
equip = U * num(prof.get("mob_unid")) + num(prof.get("equip_gerais")) + num(prof.get("pre_op"))
giro = num(prof.get("cf_mensal")) * num(prof.get("meses_giro"))
capex = lst("projetos") + lst("infra") + constr + equip
ct, var = num(prof.get("contingencia")) / 100, num(prof.get("variacao")) / 100
V.update({"T4-B06-01": capex, "T4-B06-02": capex * (1 + ct) + giro, "T4-B06-03": capex * (1 + var) * (1 + ct) + giro, "T4-B06-04": 0.0})

# F05 exemplo: literais de dados.py (sem executar o arquivo)
arv = ast.parse((RAIZ / "producao/utilitarios/05-orcamento-cabana/src/dados.py").read_text())
lit = {n.targets[0].id: n.value for n in arv.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
itens = ast.literal_eval(lit["ITENS"])
ex = {kw.arg: ast.literal_eval(kw.value) for kw in lit["EX"].keywords}
sub = 0
for (_, _, _, qtd, c1_, c2_, c3_, esc, _, _) in itens:
    cots = [c1_, c2_, c3_]
    validas = [c for c in cots if c is not None]
    if not validas: continue  # item sem cotação não entra no subtotal
    preco = cots[esc - 1] if esc else min(validas)
    sub += (qtd if qtd is not None else 1) * preco
V.update({"T4-F05-01": sub, "T4-F05-02": sub * ex["reserva"] / 100, "T4-F05-03": sub * (1 + ex["reserva"] / 100)})

# Folha J2: campos do exemplo (logic.js, objeto EXEMPLO): diárias 16.240; descontos 650; comissões 11%;
# processamento 1,5%; imposto 6%; outras receitas 980 (receita bruta total 17.220); 20 h × R$ 40.
V.update({"T5-J2-01": 0.0, "T5-J2-02": 0.0, "T5-J2-03": 0.0, "T5-J2-04": 0.0, "T5-J2-05": 0.0,
          "T9-J2-03": 16240 * 0.01, "T9-J2-04": 150.0, "T9-J2-05": 650 + 16240 * (0.11 + 0.015 + 0.06), "T10-J2-01": 20 * 40 * 4.33})

# T7: conservador e saída
cz = operacao(3, 680 * 0.9, 0.38 * 0.8, 0.17, 80, 6000)
saida = 6 * z["ebitda"]
V.update({"T7-ZAIOS-01": cz["bruta"], "T7-ZAIOS-02": cz["ger"], "T7-ZAIOS-03": saida, "T7-ZAIOS-04": saida / 1.1 ** 10,
          "T7-ZAIOS-05": vpl(fz[:-1] + [fz[-1] + saida], 0.1)})
# T9: reserva 4% e quebra 1%
t9 = operacao(3, 680, 0.38, 0.17, 80, 6000, quebra=0.01, reserva=0.04)
V.update({"T9-ZAIOS-01": t9["ded"], "T9-ZAIOS-02": t9["quebra"], "T9-ZAIOS-03": t9["op"], "T9-ZAIOS-04": t9["reserva"], "T9-ZAIOS-05": t9["ger"]})
# T10 e T11
pl = 20 * 40 * 4.33
t10 = operacao(3, 680, 0.38, 0.17, 80, 6000, prolabore_mes=pl)
V.update({"T10-ZAIOS-01": pl, "T10-ZAIOS-02": pl * 12, "T10-ZAIOS-03": t10["op"], "T11-ZAIOS-01": saida})

# ---------- comparação ----------
res = json.loads(pathlib.Path(sys.argv[1]).read_text())
casos = {c["id"]: c for c in res["casos"]}
linhas, ok_esp, ok_obt = [], 0, 0
for cid, vi in V.items():
    c = casos[cid]; tol = c.get("tol") or 0
    esp, obt = c["esperado"], c["obtido"]
    d_esp = abs(vi - esp) if isinstance(esp, (int, float)) else None
    d_obt = abs(vi - obt) if isinstance(obt, (int, float)) else None
    a = d_esp is not None and d_esp <= tol + 1e-9
    b = d_obt is not None and d_obt <= max(tol, 1e-6) + 1e-9
    ok_esp += a; ok_obt += b
    linhas.append(f"| {cid} | {c['ferramenta']} | {c['indicador']} | {vi:.6f} | {esp} | {obt if not isinstance(obt, float) else round(obt, 6)} | {'sim' if a else 'NÃO'} | {'sim' if b else 'NÃO'} |")
md = ["| Caso | Ferramenta | Indicador | Cálculo independente | Esperado (plano) | Obtido (ferramenta) | Plano confere | Ferramenta confere |", "|---|---|---|---|---|---|---|---|"] + linhas
resumo = f"Casos numéricos verificados de forma independente: {len(V)} · plano confere: {ok_esp} · ferramenta confere: {ok_obt}"
print(resumo)
if len(sys.argv) > 2:
    pathlib.Path(sys.argv[2]).write_text("# Verificação independente dos valores esperados\n\n" + resumo + "\n\n" + "\n".join(md) + "\n")
for l in linhas:
    if "NÃO" in l: print(l)

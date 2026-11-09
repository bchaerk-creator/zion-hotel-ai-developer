"""Valores esperados dos testes complementares (Comando 05E), calculados de forma independente.

Não importa nem executa o código das ferramentas. Fórmulas:
- ZAIOS e Folha J2: definições do Dicionário Financeiro v0.4 e do FORMULAS.md da ZAIOS (texto, não código).
- B08, A09, B06: fórmulas descritas na auditoria do Comando 05B (independência parcial: a descrição veio
  da leitura do código; aqui são reimplementadas em outra linguagem, com entradas novas).
Gera: esperados_complementares.json (ao lado deste arquivo).
"""
import json, pathlib
OUT = pathlib.Path(__file__).with_name("esperados_complementares.json")
DIAS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
RAMPA = [0.4] * 3 + [0.5] * 3 + [0.75] * 6
E = {}

def vpl(f, i): return sum(v / (1 + i) ** t for t, v in enumerate(f))
def tir(f, a=-0.5, b=1.0):
    fa = vpl(f, a)
    for _ in range(300):
        m = (a + b) / 2; fm = vpl(f, m)
        if (fm > 0) == (fa > 0): a, fa = m, fm
        else: b = m
    return (a + b) / 2
def payback(f, limite=None, regime=None):
    acc = 0.0
    for t, v in enumerate(f):
        ant = acc; acc += v
        if t > 0 and acc >= 0: return t - 1 + (-ant) / v
    if regime and regime > 0: return len(f) - 1 + (-acc) / regime
    return None

# ---------------- ZAIOS: EBITDA com custos do modelo (primitivas do P6) ----------------
def p6(unid, diaria, ocup, ded, cvn, fixo, quebra=0, reserva=0, aluguel=0, gestao=0, royalty=0, retirada=0, fat=None, outras=0, custoEstadia=0, perm=None):
    t = {k: 0 for k in "bruta ded real cv op modelo ebitda reserva ger noites".split()}
    for m in range(12):
        f = 1 if fat is None else fat[m]
        n = unid * DIAS[m] * ocup * f; di = n * diaria; o = di * outras; b = di + o
        d = b * ded; r = b - d
        est = n / perm if perm else 0
        cv = n * cvn + est * custoEstadia + di * quebra
        op = r - cv - fixo - retirada; mod = aluguel + b * (gestao + royalty); eb = op - mod; res = b * reserva
        for k, v in dict(bruta=b, ded=d, real=r, cv=cv, op=op, modelo=mod, ebitda=eb, reserva=res, ger=eb - res, noites=n).items(): t[k] += v
    return t
m = p6(3, 680, 0.38, 0.17, 80, 6000, quebra=0.01, reserva=0.04, aluguel=1000, gestao=0.10, royalty=0.03)
E["zaios_modelo"] = {"custosModelo": m["modelo"], "ebitda": m["ebitda"], "geracao": m["ger"], "resultadoOperacional": m["op"]}
# outras receitas, custo por estadia e sazonalidade (temporada única com outras 10%, estadia R$ 60 com permanência 2,5)
s = p6(3, 680, 0.38, 0.17, 80, 6000, outras=0.10, custoEstadia=60, perm=2.5)
E["zaios_outras_estadia"] = {"receitaBruta": s["bruta"], "custosVariaveis": s["cv"], "resultadoOperacional": s["op"]}
# sazonalidade: alta dez–fev (diária 900, ocup 60%), baixa abr–jun (diária 500, ocup 20%), média resto (680, 38%)
def sazonal():
    alta, baixa = {11, 0, 1}, {3, 4, 5}
    tot = dict(bruta=0, op=0)
    for mm in range(12):
        d, o = (900, 0.6) if mm in alta else (500, 0.2) if mm in baixa else (680, 0.38)
        n = 3 * DIAS[mm] * o; b = n * d; r = b * 0.83; op = r - n * 80 - 6000
        tot["bruta"] += b; tot["op"] += op
    return tot
E["zaios_sazonal"] = sazonal()

# ---------------- ZAIOS: composição F01 + F02 (caso dos testes da própria ZAIOS) ----------------
# P5: CAPEX 1.237.400, contingência 182.500; P6: 3 unidades, 680, 38%, 17%, fixo 10.500, abertura em janeiro.
reg = p6(3, 680, 0.38, 0.17, 0, 10500)
pri_meses = []
for k in range(12):
    n = 3 * DIAS[k] * 0.38 * RAMPA[k]; b = n * 680; pri_meses.append(b * 0.83 - 10500)
reg_meses = [3 * DIAS[k] * 0.38 * 680 * 0.83 - 10500 for k in range(12)]
acc, minacc = 0, 0
for g in pri_meses:
    acc += g; minacc = min(minacc, acc)
deficit = -minacc
sazon = sum(-g for g in reg_meses if g < 0)
giroA, giroB = 6 * 10500, deficit + sazon + 3 * 10500
giro = max(giroA, giroB)
capex = 1237400
f = [-capex, sum(pri_meses)] + [reg["ger"]] * 9
E["zaios_composicao"] = {"geracaoAno1": sum(pri_meses), "geracaoRegime": reg["ger"], "giroA": giroA, "giroB": giroB, "giroRecomendado": giro,
                         "captacao": capex + giro, "retornoAnual": reg["ger"] / capex, "estresseReceitaMenor": reg["ger"] - 0.3 * reg["bruta"],
                         "capexMaior": capex * 1.25, "vplSem10": vpl(f, 0.10), "paybackSimples": payback(f, regime=reg["ger"])}

# Curva de caixa de 36 meses e colchão (FORMULAS.md: captação no mês 1; linhas do P5 em partes iguais
# nas janelas do cronograma padrão; contingência nos meses de obra 5 a 8 quando usada; operação a partir
# do mês do projeto sugerido = mês seguinte ao último desembolso).
janelas = {"projeto": (2, 5), "infra": (5, 8), "obra": (5, 8), "apoio": (5, 8), "ffe": (7, 8), "ose": (7, 8), "pre": (8, 9)}
linhas = {"infra": 250000, "projeto": 70000, "obra": 390000, "apoio": 90000, "ffe": 195000, "ose": 23400, "pre": 36500}
desemb = [0.0] * 9
for k, (a, b) in janelas.items():
    for mm in range(a, b + 1): desemb[mm - 1] += linhas[k] / (b - a + 1)
mes_abre = max(i + 1 for i, v in enumerate(desemb) if v > 0) + 1
oper = pri_meses + [reg_meses[(0 + k) % 12] for k in range(12, 36)]
saldo, menor = 0.0, None
for mes in range(1, 37):
    if mes == 1: saldo += capex + giro
    if mes <= 9: saldo -= desemb[mes - 1]
    if 5 <= mes <= 8: saldo -= 182500 / 4
    k = mes - mes_abre
    if 0 <= k < len(oper): saldo += oper[k]
    menor = saldo if menor is None else min(menor, saldo)
col = menor / capex
cons = p6(3, 680 * 0.9, 0.38 * 0.8, 0.17, 0, 10500)
saida = 6 * reg["ebitda"]
vcom = vpl(f[:-1] + [f[-1] + saida], 0.10)
pb = E["zaios_composicao"]["paybackSimples"]
passos = ["passa" if reg["ger"] >= 0 else "redesenhar",
          "passa" if cons["ger"] >= 0 else ("ajustar" if -cons["ger"] <= 3 * 10500 else "redesenhar"),
          "passa" if pb <= 8 else ("ajustar" if pb <= 12 else "redesenhar"),
          "passa" if E["zaios_composicao"]["vplSem10"] >= 0 else ("ajustar" if vcom > 0 else "redesenhar"),
          "passa" if col >= 0.1 else ("ajustar" if col >= 0 else "redesenhar")]
decisao = "Redesenhar" if "redesenhar" in passos else "Ajustar" if "ajustar" in passos else "Avançar"
E["zaios_composicao"].update({"mesAberturaSugerido": mes_abre, "menorSaldoComContingencia": menor, "colchao": col, "geracaoConservador": cons["ger"],
                              "vplCom10": vcom, "passos": passos, "decisao": decisao})

# ---------------- B08: cenários adicionais (fórmulas descritas na auditoria) ----------------
def b08(I, U, N, d, g, x, o1, oe, R, cf, cvn, com, imp, res, i, residual=0.0):
    fc = []
    for t in range(1, 11):
        occ = min(1, max(0, o1 + (oe - o1) * min(1, (t - 1) / R)))
        k = (1 + g) ** (t - 1)
        noites = U * N * occ
        rec = noites * d * k * (1 + x)
        ded = rec * (com + imp + res)
        fc.append(rec - ded - noites * cvn * k - cf * k)
    fl = [-I] + fc[:]
    fl[-1] += I * residual
    pb = payback([-I] + fc)
    pb = pb if pb is not None and pb <= 10 else None
    disc = [-I] + [v / (1 + i) ** (t + 1) for t, v in enumerate(fc)]
    pbd = payback(disc); pbd = pbd if pbd is not None and pbd <= 10 else None
    cap = U * N
    occBE = cf / (cap * (d * (1 + x) * (1 - (com + imp + res)) - cvn))
    return {"fc1": fc[0], "vpl": vpl(fl, i), "tir": tir(fl), "paybackS": pb, "paybackD": pbd, "roi10": (sum(fc) + I * residual - I) / I, "occBE": occBE}
E["b08_rampa"] = b08(1200000, 4, 365, 500, 0.05, 0.10, 0.25, 0.40, 3, 90000, 70, 0.15, 0.06, 0.0, 0.12)
E["b08_residual"] = b08(1200000, 4, 365, 500, 0.05, 0.10, 0.25, 0.40, 3, 90000, 70, 0.15, 0.06, 0.0, 0.12, residual=0.5)
E["b08_equilibrio_sem_reserva"] = b08(900000, 3, 365, 680, 0, 0, 0.38, 0.38, 1, 72000, 80, 0, 0.17, 0.0, 0.10)["occBE"]
E["b08_equilibrio_com_reserva_regra_aprovada"] = E["b08_equilibrio_sem_reserva"]  # D2-C: reserva fora das deduções não muda o equilíbrio
E["b08_equilibrio_com_reserva_como_deducao"] = b08(900000, 3, 365, 680, 0, 0, 0.38, 0.38, 1, 72000, 80, 0, 0.17, 0.04, 0.10)["occBE"]

# ---------------- A09: cenários adicionais ----------------
def a09(U, inv, infra, cont, d, occ, N, M, extrasMes, fixosMes, custoEst, estMedia, com, imp, gest):
    invT = (inv + infra) * (1 + cont)
    noites = U * N * M * occ
    bruta = noites * d + extrasMes * M
    ded = bruta * (com + imp + gest)
    cvar = noites / estMedia * custoEst
    cfix = fixosMes * 12
    res = bruta - ded - cvar - cfix
    return {"invTotal": invT, "noites": noites, "recBruta": bruta, "ded": ded, "resultado": res, "roi": res / invT, "payback": invT / res if res > 0 else None,
            "resultadoAntesGestao": res + bruta * gest}
E["a09_payback"] = a09(2, 600000, 80000, 0.10, 550, 0.45, 30, 12, 1000, 8000, 150, 2.5, 0.12, 0.06, 0.10)
E["a09_365_dias"] = {"recBruta365": 3 * 365 * 0.38 * 680, "recBruta31x12": 3 * 31 * 12 * 0.38 * 680}

# ---------------- B06: perfis intermediário e incompleto-extremo ----------------
def b06(p):
    num = lambda x: x if isinstance(x, (int, float)) else 0
    lst = lambda k: sum(num(i.get("value")) for i in p.get(k, []))
    U = p["unidades"]
    constr = U * (num(p.get("custo_unid")) + num(p.get("frete_unid"))) + lst("comuns")
    equip = U * num(p.get("mob_unid")) + num(p.get("equip_gerais")) + num(p.get("pre_op"))
    giro = num(p.get("cf_mensal")) * num(p.get("meses_giro"))
    capex = lst("projetos") + lst("infra") + constr + equip
    ct, var = num(p.get("contingencia")) / 100, num(p.get("variacao")) / 100
    prazo = num(p.get("prazo_obra")) or None
    area = num(p.get("area_unid")) or None
    return {"capex": capex, "inter": capex * (1 + ct) + giro, "cons": capex * (1 + var) * (1 + ct) + giro, "giro": giro,
            "desembMes": capex * (1 + ct) / prazo if prazo else None, "porM2": (num(p.get("custo_unid")) + num(p.get("frete_unid"))) / area if area else None}
raiz = pathlib.Path(__file__).resolve().parents[3]
perfis = json.loads((raiz / "producao/zion-arsenal/tests/profiles/B06.json").read_text())["profiles"]
for p in perfis:
    E["b06_" + p["name"]] = b06(p["values"])

# ---------------- F05: m², diferença ----------------
E["f05_exemplo"] = {"diferenca": 200000 - 216744, "porM2Interna": 216744 / 30, "porM2Total": 216744 / (30 + 12)}

# ---------------- Folha J2: indicadores e custos do modelo ----------------
rec_h, noites, dias, unid = 16240, 58, 31, 4
real_h = rec_h - (650 + rec_h * 0.185)
var_h = 2062.4 - 420  # variáveis da hospedagem (sem o custo das outras receitas)
margem_noite = real_h / noites - var_h / noites
fixo = 7234
E["j2_indicadores"] = {"noitesDisponiveis": unid * dias, "ocupacao": noites / (unid * dias), "diariaMediaBruta": rec_h / noites, "margemPorNoite": margem_noite,
                       "pontoEquilibrioNoites": (fixo - 560) / margem_noite, "saldoFinal": 9800 + 18470 - 14650, "mesesFolego": (9800 + 18470 - 14650) / fixo}
mod = 800 + 1200 + 300
E["j2_modelo"] = {"custosModelo": mod, "ebitda": 4269.20 - mod, "geracao": 4269.20 - mod - 0.04 * 13565.6, "mesesFolego": 13620 / (fixo + mod),
                  "pontoEquilibrioNoites": (fixo + mod - 560) / margem_noite}

OUT.write_text(json.dumps(E, indent=2, ensure_ascii=False))
print("ok", len(E), "grupos ->", OUT.name)

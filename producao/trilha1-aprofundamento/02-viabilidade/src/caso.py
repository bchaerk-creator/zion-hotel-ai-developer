"""Caso didático da Marina montando a conta dela (Aprofundamento 6B · Viabilidade; exemplo ilustrativo, dados fictícios),
do PLANO.md, seção 7 (com as decisões de Bruno da seção 13: a conta real, imposto de 6% como resposta fictícia do contador).
Fonte única dos números do e-book e do checklist. Todas as contas são feitas aqui, sem arredondar, e conferidas por assert
com cada número das tabelas do plano (7.1 a 7.12, E2 e E4): se qualquer um divergir, o script para (AssertionError) e o
e-book não é gerado. Também confere a continuidade com o caso da 6A (01-capex/src/caso.py).
Uso: python3 -I src/caso.py  (imprime o resumo e confere tudo)"""
import importlib.util, pathlib
from datetime import date

SRC = pathlib.Path(__file__).resolve().parent
HOJE = date(2026, 11, 28)

# ---------------------------------------------------------------- continuidade (Pilares 2, 4, 6 e 6A)
UNID, UNID_PROJ = 3, 5
NOITES_ANO = UNID * 365                       # 1.095
DIARIA = 645
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
OCUP_TIPO = {"alta": 0.64, "médio": 0.40, "fraco": 0.22}
CAL = {"jan": "fraco", "fev": "fraco", "mar": "fraco", "abr": "médio", "mai": "médio", "jun": "alta", "jul": "alta",
       "ago": "alta", "set": "médio", "out": "médio", "nov": "fraco", "dez": "fraco"}       # fictício (ordem dos meses)
MES_ABERTURA = 6                               # junho, o começo da alta
ESTADIA = 2                                    # noites (fictício)
OCUP = {"cons": sum(OCUP_TIPO[CAL[m]] for m in MESES) / 12, "base": 0.50, "otim": 0.65}
TERRENO = 600000
MARGEM6 = 0.40                                 # referência orientativa da página 6, não confirmada
CAPEX = 791131
GIRO6A = 40787.38
INVEST6A = 831918.38
P6_TOTAL = 690529.18
DIARIA_P3 = 716                                # hipótese do Pilar 3 («cerca de R$ 716»)

# ---------------------------------------------------------------- entradas novas (todas fictícias)
IMPOSTO = 0.06                                 # resposta fictícia do contador dela (20/11/2026); não vale para você
IMPOSTO_DATA = date(2026, 11, 20)
P_PLAT, COM_PLAT = 0.60, 0.15
CARTAO, CANC = 0.03, 0.02
POR_ESTADIA = [("Lavanderia terceirizada do enxoval", 70, "cotação"), ("Amenidades e boas-vindas", 45, "estimativa")]
POR_NOITE = [("Energia, água e gás da noite", 28, "estimativa"), ("Produtos de limpeza e reposição", 12, "estimativa")]
PCT_HOSP = [("Perdas e quebras de material", 0.01, "estimativa")]
FIXOS = [("Pessoa local: salário e encargos", 3600, "estimativa, a confirmar com o contador"),
         ("13º e férias (duodécimo)", 600, "estimativa"),
         ("Folguista nas folgas da pessoa local", 400, "estimativa"),
         ("Energia das áreas comuns e bomba do poço", 500, "estimativa"),
         ("Internet e sistema de reservas", 350, "cotação"),
         ("Contador", 650, "cotação"),
         ("Seguro (R$ 3.600 no ano ÷ 12)", 300, "estimativa"),
         ("Imposto do imóvel, taxas e licença anual (duodécimos)", 150, "estimativa"),
         ("Manutenção preventiva e jardinagem", 800, "estimativa"),
         ("Marketing, fotos e anúncios", 450, "estimativa"),
         ("Tarifas bancárias e outros", 200, "estimativa")]
HORAS, VALOR_HORA, SEMANAS_MES = 8, 40, 4.33
RESERVA_REP = 0.03
RAMPA = [0.40] * 3 + [0.50] * 3 + [0.75] * 6
MULT_SAIDA = 6                                 # referência da régua (botão), nunca valor do negócio

# ---------------------------------------------------------------- contas
r2 = lambda x: round(x + (1e-9 if x >= 0 else -1e-9), 2)
DED = IMPOSTO + P_PLAT * COM_PLAT + (1 - P_PLAT) * CARTAO + CANC          # 18,2%
DED_SEM_IMP = DED - IMPOSTO
VAR_EST = sum(v for _, v, _ in POR_ESTADIA)                                # 115 por estadia
VAR_NOITE = sum(v for _, v, _ in POR_NOITE) + VAR_EST / ESTADIA            # 97,50 por noite
PERDAS = sum(v for _, v, _ in PCT_HOSP)
FIX_SUB = sum(v for _, v, _ in FIXOS)                                      # 8.000
RETIRADA = HORAS * VALOR_HORA * SEMANAS_MES                                # 1.385,60
FIXO_MES = FIX_SUB + RETIRADA                                              # 9.385,60
FIXO_ANO = 12 * FIXO_MES                                                   # 112.627,20
FATOR = 1 - DED - PERDAS - RESERVA_REP                                     # 0,778: o que fica de cada real de diária


def por_noite(diaria, ded=DED):
    return diaria * (1 - ded - PERDAS - RESERVA_REP) - VAR_NOITE


CNOITE = por_noite(DIARIA)                                                 # 404,31


def cascata(ocup, diaria=DIARIA, fixo_ano=FIXO_ANO, unid=UNID):
    n = unid * 365 * ocup; est = n / ESTADIA; bruta = n * diaria
    d = {"noites": n, "estadias": est, "bruta": bruta, "imp": IMPOSTO * bruta, "com": P_PLAT * COM_PLAT * bruta,
         "cart": (1 - P_PLAT) * CARTAO * bruta, "canc": CANC * bruta}
    d["ded"] = d["imp"] + d["com"] + d["cart"] + d["canc"]; d["real"] = bruta - d["ded"]
    d["lav"] = 70 * est; d["amen"] = 45 * est; d["ener"] = 28 * n; d["limp"] = 12 * n; d["perdas"] = PERDAS * bruta
    d["var"] = d["lav"] + d["amen"] + d["ener"] + d["limp"] + d["perdas"]; d["contrib"] = d["real"] - d["var"]
    d["fixo"] = fixo_ano; d["antes"] = d["contrib"] - fixo_ano; d["modelo"] = 0; d["depois"] = d["antes"]
    d["reserva"] = RESERVA_REP * bruta; d["sobra"] = d["depois"] - d["reserva"]; d["margem"] = d["sobra"] / bruta
    d["X"] = d["sobra"] + fixo_ano
    return d


C = {s: cascata(o) for s, o in OCUP.items()}
CO = C["cons"]
SOBRA = CO["sobra"]
CUSTOS = CO["bruta"] - SOBRA                                               # 214.096,09

# mês a mês: mês i do ano 1 = mês do calendário (abertura + i − 2) mod 12 + 1
SIGMA_O = sum(OCUP_TIPO[CAL[m]] for m in MESES)                            # 4,62 (462 pontos)
NOITES_MES = NOITES_ANO / 12                                               # 91,25
ORDEM = [MESES[(MES_ABERTURA + i - 2) % 12] for i in range(1, 13)]
SIGMA_OR = sum(OCUP_TIPO[CAL[m]] * RAMPA[i] for i, m in enumerate(ORDEM))  # 2,538
R = SIGMA_OR / SIGMA_O                                                     # 0,549351


def meses36(X, fixo_mes=FIXO_MES):
    out, acum = [], 0.0
    for i in range(36):
        m = MESES[(MES_ABERTURA + i - 1) % 12]; o = OCUP_TIPO[CAL[m]]; rp = RAMPA[i] if i < 12 else 1
        res = X * o * rp / SIGMA_O - fixo_mes; acum += res
        out.append({"i": i + 1, "mes": m, "tipo": CAL[m], "o": o * rp, "noites": NOITES_MES * o * rp,
                    "contrib": X * o * rp / SIGMA_O, "res": res, "acum": acum})
    return out


M36 = meses36(CO["X"])
ANO1 = M36[:12]
ANO1_RES = sum(x["res"] for x in ANO1)
MENOR = min(x["acum"] for x in M36)
MES_MENOR = min(M36, key=lambda x: x["acum"])
REGIME = {t: NOITES_MES * OCUP_TIPO[t] * CNOITE - FIXO_MES for t in OCUP_TIPO}
DEFICIT_VALE = -sum(REGIME[CAL[m]] for m in MESES if REGIME[CAL[m]] < 0)
RES_SAZ = DEFICIT_VALE / sum(CAL[m] == "alta" for m in MESES)

# equilíbrio, custo por diária, diária de equilíbrio, piso
N_EQ = FIXO_ANO / CNOITE
OCUP_EQ = N_EQ / NOITES_ANO
FOLGA_EQ = OCUP["cons"] - OCUP_EQ
CUSTO_DIARIA = CUSTOS / CO["noites"]
EFEITO1 = CO["noites"] * FATOR
DIARIA_EQ = DIARIA - SOBRA / EFEITO1
PISO = VAR_NOITE / FATOR

# giro, investimento, colchão
GIRO_A = 3 * CUSTOS / 12
GIRO_B = abs(min(0, MENOR)) + 3 * FIXO_MES
GIRO6B = max(GIRO6A, GIRO_A, GIRO_B)
INVEST6B = CAPEX + GIRO6B
COLCHAO = GIRO6B + min(0, MENOR)
COLCHAO_PCT = COLCHAO / CAPEX
GIRO_10 = 0.10 * CAPEX - min(0, MENOR)
FOLEGO = GIRO6B / FIXO_MES


# tempo de volta em escada
def escada(capex, ano1, sobra):
    if sobra <= 0:
        return None
    acum, t = -capex + ano1, 1
    if acum >= 0:
        return capex / ano1
    v = t + (-acum) / sobra
    return v if v <= 100 else float("inf")


def ano1_de(X, fixo=FIXO_ANO):
    return X * R - fixo


VOLTA = {s: escada(CAPEX, ano1_de(C[s]["X"]), C[s]["sobra"]) for s in C}
ANO1S = {s: ano1_de(C[s]["X"]) for s in C}
VOLTA_P6 = {s: INVEST6B / C[s]["sobra"] for s in C}
VOLTA_T = escada(CAPEX + TERRENO, ANO1S["cons"], SOBRA)
RET = SOBRA / CAPEX
RET_T = SOBRA / (CAPEX + TERRENO)


# valor presente de dez anos (moeda constante)
def vp(i, ano1, sobra, capex=CAPEX, saida=0):
    f = [ano1] + [sobra] * 9
    return sum(x / (1 + i) ** (t + 1) for t, x in enumerate(f)) - capex + saida / (1 + i) ** 10


SOMA10 = ANO1S["cons"] + 9 * SOBRA
SAIDA = MULT_SAIDA * CO["depois"]
VP1 = vp(0.01, ANO1S["cons"], SOBRA, saida=SAIDA)
VP2 = vp(0.02, ANO1S["cons"], SOBRA, saida=SAIDA)


def raiz(fn, a, b):
    for _ in range(200):
        m = (a + b) / 2
        if fn(a) * fn(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2


TAXA_ZERO = raiz(lambda i: vp(i, ANO1S["cons"], SOBRA, saida=SAIDA), 0.0, 0.10)

# teste de queda (diária −10%, ocupação −20%)
QUEDA = cascata(OCUP["cons"] * 0.80, DIARIA * 0.90)
QUEDA_NOITE = por_noite(DIARIA * 0.90)
# sensibilidade do Mapa
SENS_D = cascata(OCUP["cons"], DIARIA * 0.85)
SENS_O = cascata(OCUP["cons"] - 0.10)
SENS = {"diaria": escada(CAPEX, ano1_de(SENS_D["X"]), SENS_D["sobra"]),
        "ocup": escada(CAPEX, ano1_de(SENS_O["X"]), SENS_O["sobra"]),
        "capex": escada(CAPEX * 1.2, ANO1S["cons"], SOBRA)}


# o que precisa ser verdade (uma premissa por vez)
def precisa(T):
    x = (CAPEX + T * FIXO_ANO) / (T - 1 + R)
    noites = x / CNOITE
    pn = x / CO["noites"]
    return {"x": x, "noites": noites, "ocup": noites / NOITES_ANO, "por_noite": pn,
            "diaria": (pn + VAR_NOITE) / FATOR, "capex": (T - 1) * SOBRA + ANO1S["cons"]}


PV8, PV12 = precisa(8), precisa(12)
LIMITE6 = 8 * DIARIA * NOITES_ANO * OCUP["cons"] * MARGEM6
LIMITE6B = 8 * SOBRA

# cinco passos (régua da Zion)
P1 = "passa" if SOBRA >= 0 else "redesenhar"
P2 = "passa" if QUEDA["sobra"] >= 0 else ("ajustar" if -QUEDA["sobra"] <= 3 * FIXO_MES else "redesenhar")
P3 = "passa" if VOLTA["cons"] <= 8 else ("ajustar" if VOLTA["cons"] <= 12 else "redesenhar")
P4 = "redesenhar" if (SOMA10 <= CAPEX and SOMA10 + SAIDA > CAPEX and TAXA_ZERO < 0.05) else "?"
P5 = "passa" if COLCHAO_PCT >= 0.10 else ("ajustar" if COLCHAO_PCT >= 0 else "redesenhar")
PASSOS = [P1, P2, P3, P4, P5]
VEREDITO = "Redesenhar" if "redesenhar" in PASSOS else ("Ajustar" if "ajustar" in PASSOS else "Avançar")

# ---------------------------------------------------------------- alavancas, uma por vez
ALAV = {}


def alav(nome, d, capex=CAPEX, fixo=FIXO_ANO, extra=0.0):
    sobra = d["sobra"] + extra; X = sobra + fixo; a1 = ano1_de(X, fixo)
    ALAV[nome] = {"sobra": sobra, "ano1": a1, "volta": escada(capex, a1, sobra)}


alav("nenhuma", CO)
alav("diaria50", cascata(OCUP["cons"], DIARIA + 50))
alav("diariaP3", cascata(OCUP["cons"], DIARIA_P3))
alav("ocup5", cascata(OCUP["cons"] + 0.05))
alav("fixo10", cascata(OCUP["cons"], fixo_ano=FIXO_ANO * 0.9), fixo=FIXO_ANO * 0.9)
alav("capex10", CO, capex=CAPEX * 0.9)
CESTA_CAPT, CESTA_TICKET, CESTA_CUSTO = 0.60, 140, 70
CESTA_LIQ = CESTA_TICKET * (1 - IMPOSTO - RESERVA_REP) - CESTA_CUSTO          # 57,40
CESTAS = CO["estadias"] * CESTA_CAPT
alav("cesta", CO, extra=CESTAS * CESTA_LIQ)
CAPEX_2CAB = (687940 - 146940) * 1.15                                        # 622.150 (sai uma cabana com as linhas dela, 6A)
alav("fase2", cascata(OCUP["cons"], unid=2), capex=CAPEX_2CAB)
FIXO10_MES = FIXO_MES * 0.9


def passo3(v):
    return "redesenhar" if v is None or v > 12 else ("ajustar" if v > 8 else "passa")


# ---------------------------------------------------------------- cenário ajustado (fictício, «o que precisaria ser verdade»)
def ajustado(diaria=DIARIA_P3, ocup=0.42):
    n = NOITES_ANO * ocup; est = n / ESTADIA; hosp = n * diaria; cestas = est * CESTA_CAPT; rc = cestas * CESTA_TICKET
    a = {"noites": n, "estadias": est, "hosp": hosp, "cestas": cestas, "rcestas": rc, "bruta": hosp + rc,
         "ded": DED * hosp, "imp_cestas": IMPOSTO * rc, "var": est * VAR_EST + n * 40 + PERDAS * hosp,
         "custo_cestas": cestas * CESTA_CUSTO, "fixo": FIXO_ANO}
    a["antes"] = a["bruta"] - a["ded"] - a["imp_cestas"] - a["var"] - a["custo_cestas"] - FIXO_ANO
    a["reserva"] = RESERVA_REP * a["bruta"]; a["sobra"] = a["antes"] - a["reserva"]; a["margem"] = a["sobra"] / a["bruta"]
    a["X"] = a["sobra"] + FIXO_ANO
    return a


AJ = ajustado()
AJ_M36 = meses36(AJ["X"])
AJ_ANO1 = sum(x["res"] for x in AJ_M36[:12])
AJ_MENOR = min(x["acum"] for x in AJ_M36)
AJ_MES_MENOR = min(AJ_M36, key=lambda x: x["acum"])["mes"]
AJ_VOLTA = escada(CAPEX, AJ_ANO1, AJ["sobra"])
AJ_GIRO = max(GIRO6A, (AJ["bruta"] - AJ["sobra"]) / 4, abs(min(0, AJ_MENOR)) + 3 * FIXO_MES)
AJ_COLCHAO = AJ_GIRO + min(0, AJ_MENOR)
AJ_COLCHAO_PCT = AJ_COLCHAO / CAPEX
AJ_GIRO10 = 0.10 * CAPEX - min(0, AJ_MENOR)
AJ_Q = ajustado(DIARIA_P3 * 0.9, 0.42 * 0.8)
AJ_SAIDA = MULT_SAIDA * AJ["antes"]
AJ_VP = {t: (vp(t, AJ_ANO1, AJ["sobra"]), vp(t, AJ_ANO1, AJ["sobra"], saida=AJ_SAIDA)) for t in (0.08, 0.10, 0.12)}
AJ_TAXA_SAIDA = raiz(lambda i: vp(i, AJ_ANO1, AJ["sobra"], saida=AJ_SAIDA), 0.0, 0.30)

# ---------------------------------------------------------------- exercícios E2 e E4
E2_DED = IMPOSTO + 0.80 * COM_PLAT + 0.20 * CARTAO + CANC
E2_NOITE = por_noite(DIARIA, E2_DED)
E2_SOBRA = CO["noites"] * E2_NOITE - FIXO_ANO
E2_MARGEM = E2_SOBRA / CO["bruta"]
E2_NEQ = FIXO_ANO / E2_NOITE
E2_OCUPEQ = E2_NEQ / NOITES_ANO
E2_FOLGA = OCUP["cons"] - E2_OCUPEQ
E4_NOITE = por_noite(DIARIA + 50)
E4_SOBRA = ALAV["diaria50"]["sobra"]; E4_ANO1 = ALAV["diaria50"]["ano1"]; E4_VOLTA = ALAV["diaria50"]["volta"]
E4_VALOR50 = 50 * CO["noites"] * FATOR
E4_VALOR50_P6 = 50 * CO["noites"] * MARGEM6

# ---------------------------------------------------------------- quadros de volta
MARGEM_P6 = round(CO["margem"] * 100, 2)                                   # 21,26
GIRO_MESES_P6 = GIRO6B / ((1 - MARGEM_P6 / 100) * CO["bruta"] / 12)
P6R_RES = CO["bruta"] * MARGEM_P6 / 100
P6R_GIRO = 3 * (1 - MARGEM_P6 / 100) * CO["bruta"] / 12
P6R_INV = CAPEX + P6R_GIRO
P6R_VOLTA = P6R_INV / P6R_RES
P6R_LIM = 8 * P6R_RES
P6R_BASE = P6R_INV / (C["base"]["bruta"] * MARGEM_P6 / 100)
P6R_OTIM = P6R_INV / (C["otim"]["bruta"] * MARGEM_P6 / 100)
PL2_B11 = P_PLAT * COM_PLAT + (1 - P_PLAT) * CARTAO + CANC                  # 12,2%
PL2_B12 = VAR_EST / ESTADIA + 40 + PERDAS * DIARIA + RESERVA_REP * DIARIA   # 123,30
PL2_FIX = {"B18": 4600, "B19": 500, "B20": 350, "B21": 800, "B22": 450, "B23": 1100, "B24": 200 + RETIRADA}
PL2_NOITE = DIARIA * (1 - PL2_B11 - IMPOSTO) - PL2_B12

# ---------------------------------------------------------------- conferência com o PLANO.md, seção 7 (falha se divergir)
q = lambda a, b, t=0.006: abs(a - b) <= t
p1 = lambda v: round(v * 100 + 1e-9, 1)
# 7.1 continuidade
assert NOITES_ANO == 1095 and q(OCUP["cons"], 0.385, 1e-12) and [sum(CAL[m] == t for m in MESES) for t in ("alta", "médio", "fraco")] == [3, 4, 5]
assert q(CO["bruta"], 271915.875, 1e-6) and q(C["base"]["bruta"], 353137.50) and q(C["otim"]["bruta"], 459078.75)
assert q(LIMITE6, 870130.80) and q(CO["bruta"] * MARGEM6, 108766.35)
# 7.2 entradas
assert q(DED, 0.182, 1e-12) and q(P_PLAT * COM_PLAT, 0.09, 1e-12) and q((1 - P_PLAT) * CARTAO, 0.012, 1e-12)
assert FIX_SUB == 8000 and q(RETIRADA, 1385.60) and q(FIXO_MES, 9385.60) and q(FIXO_ANO, 112627.20)
assert q(FATOR, 0.778, 1e-12) and q(VAR_NOITE, 97.50) and q(CNOITE, 404.31)
# 7.3 a conta em seis degraus
TAB73 = {"noites": (421.575, 547.5, 711.75), "estadias": (210.79, 273.75, 355.88), "bruta": (271915.88, 353137.50, 459078.75),
         "imp": (16314.95, 21188.25, 27544.73), "com": (24472.43, 31782.38, 41317.09), "cart": (3262.99, 4237.65, 5508.95),
         "canc": (5438.32, 7062.75, 9181.58), "ded": (49488.69, 64271.03, 83552.33), "real": (222427.19, 288866.48, 375526.42),
         "lav": (14755.13, 19162.50, 24911.25), "amen": (9485.44, 12318.75, 16014.38), "ener": (11804.10, 15330.00, 19929.00),
         "limp": (5058.90, 6570.00, 8541.00), "perdas": (2719.16, 3531.38, 4590.79), "var": (43822.72, 56912.63, 73986.41),
         "contrib": (178604.46, 231953.85, 301540.01), "fixo": (112627.20,) * 3, "antes": (65977.26, 119326.65, 188912.81),
         "reserva": (8157.48, 10594.13, 13772.36), "sobra": (57819.79, 108732.53, 175140.44)}
for k, vals in TAB73.items():
    for s, v in zip(("cons", "base", "otim"), vals):
        assert q(C[s][k], v, 0.0051 if k == "estadias" else 0.006), (k, s, C[s][k], v)
assert [p1(C[s]["margem"]) for s in ("cons", "base", "otim")] == [21.3, 30.8, 38.2]
assert [r2(C[s]["sobra"] / 12) for s in ("cons", "base", "otim")] == [4818.32, 9061.04, 14595.04]
assert q(CO["noites"] * r2(CNOITE), 170446.99) and q(CO["X"], 170446.99)
assert q(CUSTOS, 214096.09) and [p1(CO[k] / CO["bruta"]) for k in ("ded", "var", "fixo", "reserva")] == [18.2, 16.1, 41.4, 3.0]
assert q(CO["bruta"] * MARGEM6 - SOBRA, 108766.35 - 57819.79, 0.01)
# 7.4 equilíbrio
assert q(N_EQ, 278.5665, 0.0001) and p1(OCUP_EQ) == 25.4 and p1(FOLGA_EQ) == 13.1
assert q(CUSTO_DIARIA, 507.85) and q(EFEITO1, 327.99, 0.005) and q(DIARIA_EQ, 468.71) and q(PISO, 125.32)
# 7.5 mês a mês
assert ORDEM == ["jun", "jul", "ago", "set", "out", "nov", "dez", "jan", "fev", "mar", "abr", "mai"]
assert q(SIGMA_OR * 100, 253.8, 1e-9) and q(R, 0.549351, 5e-7) and q(NOITES_MES, 91.25)
TAB75 = [(23.36, 9444.68, 59.08, 59.08), (23.36, 9444.68, 59.08, 118.16), (23.36, 9444.68, 59.08, 177.24),
         (18.25, 7378.66, -2006.94, -1829.70), (18.25, 7378.66, -2006.94, -3836.64), (10.04, 4058.26, -5327.34, -9163.98),
         (15.06, 6087.39, -3298.21, -12462.19), (15.06, 6087.39, -3298.21, -15760.39), (15.06, 6087.39, -3298.21, -19058.60),
         (15.06, 6087.39, -3298.21, -22356.81), (27.38, 11067.99, 1682.39, -20674.42), (27.38, 11067.99, 1682.39, -18992.04)]
for x, (n, ct, rs, ac) in zip(ANO1, TAB75):
    assert q(x["noites"], n, 0.006) and q(x["contrib"], ct, 0.006) and q(x["res"], rs, 0.006) and q(x["acum"], ac, 0.011), (x, n, ct, rs, ac)
assert q(sum(x["noites"] for x in ANO1), 231.59, 0.005) and q(sum(x["contrib"] for x in ANO1), 93635.16) and q(ANO1_RES, -18992.04)
assert p1(sum(x["o"] for x in ANO1) / 12) == 21.1 or q(sum(x["o"] for x in ANO1) / 12, 0.2115, 1e-4)
assert q(MENOR, -22356.81, 0.011) and MES_MENOR["mes"] == "mar" and MES_MENOR["i"] == 10
assert q(REGIME["alta"], 14226.10) and q(REGIME["médio"], 5371.72) and q(REGIME["fraco"], -1269.08)
assert q(NOITES_MES * 0.64 * CNOITE, 23611.70) and q(sum(REGIME[CAL[m]] for m in MESES), SOBRA)
assert q(DEFICIT_VALE, 6345.38, 0.01) and q(RES_SAZ, 2115.13)
assert min(x["acum"] for x in M36[12:]) > MENOR and min(x["acum"] for x in M36[12:] if x["tipo"] == "fraco" and x["i"] > 17) > 28000
# 7.6 giro, investimento, colchão
assert q(GIRO_A, 53524.02) and q(GIRO_B, 50513.61, 0.011) and q(GIRO6B, 53524.02) and q(INVEST6B, 844655.02)
assert q(INVEST6B - INVEST6A, 12736.64) and q(COLCHAO, 31167.21, 0.011) and p1(COLCHAO_PCT) == 3.9
assert q(GIRO_10, 101469.91, 0.011) and round(FOLEGO, 1) == 5.7
# 7.7 vale a pena
assert p1(RET) == 7.3 and p1(RET_T) == 4.2
assert q(-CAPEX + ANO1S["cons"], -810123.04) and round(VOLTA["cons"], 1) == 15.0 and q(VOLTA["cons"], 15.01, 0.005)
assert q(-CAPEX + ANO1S["cons"] + 14 * SOBRA, -646.00, 0.01)
assert round(VOLTA_P6["cons"], 1) == 14.6 and round(VOLTA_T, 1) == 25.4
assert q(ANO1S["base"], 8976.91, 0.01) and q(ANO1S["otim"], 45458.14, 0.01) and round(VOLTA["base"], 1) == 8.2 and round(VOLTA["otim"], 1) == 5.3
assert round(VOLTA_P6["base"], 1) == 7.8 and round(VOLTA_P6["otim"], 1) == 4.8
assert q(SOMA10, 501386.06, 0.01) and q(SAIDA, 395863.59, 0.01) and q(SOMA10 + SAIDA, 897249.65, 0.01)
# o plano somou os fluxos já arredondados aos centavos: diferença de até R$ 0,13 no valor presente
assert q(VP1, 38816.74, 0.2) and q(VP2, -22319.65, 0.2) and round(TAXA_ZERO * 100, 1) == 1.6
# 7.8 onde quebra
assert q(DIARIA * 0.9, 580.50) and p1(OCUP["cons"] * 0.8) == 30.8 and q(QUEDA_NOITE, 354.13, 0.005) and q(QUEDA["noites"], 337.26)
assert q(QUEDA["sobra"], 6806.35, 0.02)
assert q(SENS_D["sobra"], 26087.21, 0.01) and q(SENS_O["sobra"], 13547.84, 0.01)
assert round(SENS["diaria"], 1) == 32.7 and round(SENS["ocup"], 1) == 62.6 and round(SENS["capex"], 1) == 17.7 and q(CAPEX * 1.2, 949357.20)
assert q(CAPEX + 8 * FIXO_ANO, 1692148.60) and q(7 + R, 7.549351, 5e-7) and q(PV8["x"], 224144.92, 0.02)
assert q(PV8["noites"], 554.39) and p1(PV8["ocup"]) == 50.6 and q(PV8["por_noite"], 531.68) and q(PV8["diaria"], 808.72, 0.01) and q(PV8["capex"], 385746.48, 0.01)
assert p1(PV12["ocup"]) == 41.9 and q(PV12["diaria"], 690.96, 0.01) and q(PV12["capex"], 617025.63, 0.01)
assert q(LIMITE6B, 462558.31, 0.01)
# 7.9 cinco passos e veredito
assert PASSOS == ["passa", "passa", "redesenhar", "redesenhar", "ajustar"] and VEREDITO == "Redesenhar"
assert SOMA10 < CAPEX  # negativo a qualquer taxa de zero para cima, sem a saída
# 7.10 alavancas
TAB710 = {"nenhuma": (57819.79, -18992.04, 15.0), "diaria50": (74219.06, -9983.09, 11.8), "diariaP3": (81106.75, -6199.33, 10.8),
          "ocup5": (79955.76, -6831.63, 11.0), "fixo10": (69082.51, -7729.32, 12.6), "capex10": (57819.79, -18992.04, 13.6),
          "cesta": (65079.31, -15004.01, 13.4), "fase2": (1004.13, -50203.76, None)}
for k, (s, a, v) in TAB710.items():
    x = ALAV[k]
    assert q(x["sobra"], s, 0.02) and q(x["ano1"], a, 0.02), (k, x, s, a)
    assert (x["volta"] == float("inf")) if v is None else round(x["volta"], 1) == v, (k, x["volta"], v)
assert [passo3(ALAV[k]["volta"]) for k in TAB710] == ["redesenhar", "ajustar", "ajustar", "ajustar", "redesenhar", "redesenhar", "redesenhar", "redesenhar"]
assert q(FIXO10_MES, 8447.04) and q(CAPEX * 0.9, 712017.90) and q(CESTA_LIQ, 57.40) and q(CESTAS, 126.47, 0.005) and q(CESTAS * CESTA_LIQ, 7259.52, 0.01)
assert q(CAPEX_2CAB, 622150) and 106400 + 11200 + 1800 + 1600 + 23200 + 2340 + 400 == 146940
assert q(ALAV["diaria50"]["volta"], 11.79, 0.005) and q(ALAV["ocup5"]["volta"], 10.98, 0.005) and q(ALAV["fixo10"]["volta"], 12.56, 0.005)
assert q(ALAV["capex10"]["volta"], 13.64, 0.005) and q(ALAV["cesta"]["volta"], 13.39, 0.005)
# 7.11 ajustado
assert q(AJ["noites"], 459.9) and q(AJ["estadias"], 229.95) and q(AJ["hosp"], 329288.40) and q(AJ["cestas"], 137.97)
assert q(AJ["rcestas"], 19315.80) and q(AJ["bruta"], 348604.20) and q(AJ["ded"], 59930.49) and q(AJ["imp_cestas"], 1158.95)
assert q(AJ["var"], 48133.13) and q(AJ["custo_cestas"], 9657.90) and q(AJ["antes"], 117096.53) and q(AJ["reserva"], 10458.13)
assert q(AJ["sobra"], 106638.40) and p1(AJ["margem"]) == 30.6 and q(AJ_ANO1, 7826.50, 0.01) and q(AJ_MENOR, -1878.35, 0.01) and AJ_MES_MENOR == "mar"
assert round(AJ_VOLTA, 1) == 8.3 and q((AJ["bruta"] - AJ["sobra"]), 241965.80) and q(AJ_GIRO, 60491.45) and q(AJ_COLCHAO, 58613.10, 0.01)
assert p1(AJ_COLCHAO_PCT) == 7.4 and q(AJ_GIRO10, 80991.45, 0.01) and q(DIARIA_P3 * 0.9, 644.40) and p1(0.42 * 0.8) == 33.6
assert q(AJ_Q["sobra"], 42290.37, 0.02)
for t, (a, b) in {0.08: (-167071.13, 158358.97), 0.10: (-225713.19, 45161.50), 0.12: (-276825.15, -50613.40)}.items():
    assert q(AJ_VP[t][0], a, 0.1) and q(AJ_VP[t][1], b, 0.1), (t, AJ_VP[t], a, b)
assert round(AJ_TAXA_SAIDA * 100, 1) == 10.9 and q(1.05 * DIARIA, 677.25)
AJ_PASSOS = ["passa" if AJ["sobra"] >= 0 else "redesenhar", "passa" if AJ_Q["sobra"] >= 0 else "?", passo3(AJ_VOLTA), "ajustar", "ajustar" if 0 <= AJ_COLCHAO_PCT < 0.10 else "?"]
assert AJ_PASSOS == ["passa", "passa", "ajustar", "ajustar", "ajustar"]
assert q(AJ["bruta"] - 59930.49 - 1158.95 - 3292.88 - 26444.25 - 18396.00 - 9657.90 - 10458.13 - 112627.20, 106638.40, 0.01)
# 7.12 quadros de volta
assert MARGEM_P6 == 21.26 and round(GIRO_MESES_P6, 2) == 3.00
assert q(P6R_RES, 57809.32) and q(P6R_GIRO, 53526.64) and q(P6R_INV, 844657.64) and round(P6R_VOLTA, 1) == 14.6
assert q(P6R_LIM, 462474.52) and q(P6R_INV - P6R_LIM, 382183.12) and round(P6R_BASE, 1) == 11.3 and round(P6R_OTIM, 1) == 8.7
assert q(PL2_B11, 0.122, 1e-12) and q(PL2_B12, 123.30) and q(sum(PL2_FIX.values()), FIXO_MES) and q(PL2_NOITE, 404.31)
# E2 e E4
assert q(0.80 * COM_PLAT, 0.12, 1e-12) and q(0.20 * CARTAO, 0.006, 1e-12) and q(E2_DED, 0.206, 1e-12)
assert q(E2_NOITE, 388.83) and q(CO["noites"] * E2_NOITE, 163921.01, 0.01) and q(E2_SOBRA, 51293.81, 0.01) and p1(E2_MARGEM) == 18.9
assert q(E2_NEQ, 289.66, 0.005) and p1(E2_OCUPEQ) == 26.5 and p1(E2_FOLGA) == 12.0
assert q(E4_NOITE, 443.21) and q(E4_SOBRA, 74219.06, 0.02) and q(E4_ANO1, -9983.09, 0.02) and round(E4_VOLTA, 2) == 11.79
assert q(E4_VALOR50, 16399.27, 0.01) and q(E4_VALOR50_P6, 8431.50, 0.01)
assert q(CO["noites"] * 0.83, 349.91, 0.005) and q(CO["noites"] * 388, 163571.10)
# continuidade com a 6A (01-capex/src/caso.py)
_spec = importlib.util.spec_from_file_location("caso6a", SRC.parents[1] / "01-capex/src/caso.py")
c6a = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(c6a)
assert c6a.CAPEX == CAPEX and c6a.GIRO == GIRO6A and c6a.INVEST == INVEST6A and c6a.P6_TOTAL == P6_TOTAL and c6a.TERRENO == TERRENO
assert q(c6a.LIMITE6, LIMITE6) and q(c6a.FOLGA, 38212.42) and c6a.SUB == 687940


# ---------------------------------------------------------------- formatação
def brl(v, casas=0):
    neg = v < 0
    s = f"{abs(v):,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−R$ " if neg else "R$ ") + s


def num(v, casas=0):
    neg = v < 0
    s = f"{abs(v):,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if neg else "") + s


def pct(v, casas=1):
    return f"{v * 100:.{casas}f}".replace(".", ",") + "%"


def dec(v, casas=1):
    return f"{v:.{casas}f}".replace(".", ",")


if __name__ == "__main__":
    print("Marina · 6B conferida com o PLANO.md, seção 7 (todas as tabelas, E2 e E4) e com a 6A")
    print("bruta", r2(CO["bruta"]), "sobra", r2(SOBRA), "margem", pct(CO["margem"]), "equilíbrio", pct(OCUP_EQ), "folga", round(FOLGA_EQ * 100, 1))
    print("ano 1", r2(ANO1_RES), "menor", r2(MENOR), "giro", r2(GIRO6B), "colchão", pct(COLCHAO_PCT), "volta", round(VOLTA["cons"], 2))
    print("passos", PASSOS, "veredito", VEREDITO, "ajustado", r2(AJ["sobra"]), round(AJ_VOLTA, 2))

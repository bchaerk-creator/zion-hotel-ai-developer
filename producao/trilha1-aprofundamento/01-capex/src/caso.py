"""Caso didático da Marina abrindo a página 6 dela (exemplo ilustrativo, dados fictícios), do PLANO.md v2, seção 7.
Fonte única dos números do e-book e do checklist. As contas são feitas aqui e conferidas com os valores do plano:
se qualquer número divergir, o script para (AssertionError) e o e-book não é gerado.
Uso: python3 -I src/caso.py  (imprime o resumo e confere tudo)"""
from datetime import date

HOJE = date(2026, 11, 27)

# Linha: (nome, conta exibida, origem, n_cotacoes, mesma_espec, data, valor, tag_p6, aba_pl1)
# origem: C cotação escrita, E estimativa, B em branco, NA não se aplica
PARTES = [
    ("Projetos, licenças e documentação", [
        ("Levantamento topográfico e sondagem do solo", "valor", "C", 3, True, date(2026, 10, 2), 6200, None, "Infraestrutura · 1"),
        ("Projeto de arquitetura (3 cabanas, apoio e implantação da fase um)", "valor", "C", 3, True, date(2026, 10, 9), 16500, None, "Infraestrutura · 1"),
        ("Projetos complementares (estrutural, elétrico, hidrossanitário)", "valor", "C", 2, True, date(2026, 10, 14), 9800, None, "Infraestrutura · 1"),
        ("Aprovação na prefeitura e taxas", "valor", "E", 0, False, None, 2500, None, "Infraestrutura · 1"),
        ("Responsabilidade técnica e registros", "valor", "E", 0, False, None, 1000, None, "Infraestrutura · 1"),
        ("Licença ambiental, se houver (aguarda a resposta da prefeitura)", "", "B", 0, False, None, 0, None, "Infraestrutura · 1"),
    ]),
    ("Infraestrutura", [
        ("Acesso interno até a clareira (cascalho e drenagem lateral)", "valor", "C", 3, True, date(2026, 10, 20), 24000, None, "Infraestrutura · 3"),
        ("Estacionamento na clareira (5 vagas de hóspede + 1 de serviço)", "valor", "C", 2, True, date(2026, 10, 20), 7200, None, "Infraestrutura · 3"),
        ("Caminho do hóspede pela mata, com luz baixa", "120 m × 140", "C", 2, True, date(2026, 10, 22), 16800, None, "Infraestrutura · 3"),
        ("Energia: padrão de entrada e rede enterrada até as 5 posições, com duto vazio para a 4ª e a 5ª", "valor", "C", 1, False, date(2026, 11, 5), 31500, None, "Infraestrutura · 4"),
        ("Água: poço com teste de vazão, reservatório e rede para 5", "valor", "C", 2, True, date(2026, 7, 15), 19800, None, "Infraestrutura · 5"),
        ("Esgoto: tratamento dimensionado para 5", "valor", "E", 0, False, None, 14500, None, "Infraestrutura · 5"),
        ("Drenagem das plataformas e do caminho", "valor", "E", 0, False, None, 4200, None, "Infraestrutura · 2"),
        ("Internet para o hóspede que trabalha de domingo a quinta", "", "B", 0, False, None, 0, None, "Infraestrutura · 6"),
        ("Ligação de luz de cada cabana", "3 × 1.800", "E", 0, False, None, 5400, "luz", "Infraestrutura · 4"),
        ("Água e esgoto de cada cabana", "3 × 1.600", "E", 0, False, None, 4800, "agua", "Infraestrutura · 5"),
    ]),
    ("Unidades e áreas comuns", [
        ("Cabanas de madeira (tipologia única; piso incluído no m²)", "3 × 38 m² × 2.800", "C", 3, True, date(2026, 10, 28), 319200, "unidade", "Premissas linha 11"),
        ("Deck de cada cabana", "3 × 16 m² × 700", "C", 2, True, date(2026, 10, 28), 33600, "deck", "Premissas linha 11"),
        ("Apoio de 30 m² (rouparia 12, depósito 6, lixo 4, copa e vestiário 8)", "1 × 30 m² × 2.200", "C", 1, False, date(2026, 10, 30), 66000, None, "Infraestrutura · 7"),
        ("Deck leve da crista", "1 × 16 m² × 600", "E", 0, False, None, 9600, None, "Infraestrutura · 7"),
    ]),
    ("Mobiliário e equipamentos", [
        ("Cama e colchão de hotel", "3 × 5.200", "C", 3, True, date(2026, 11, 3), 15600, "mobilia", "FF&E"),
        ("Mobiliário (sofá pequeno, mesa de trabalho e cadeira, armário, mesas de cabeceira)", "3 × 7.400", "C", 2, True, date(2026, 11, 3), 22200, "mobilia", "FF&E"),
        ("Iluminação", "3 × 1.900", "E", 0, False, None, 5700, "mobilia", "FF&E"),
        ("Cozinha compacta e eletrodomésticos", "3 × 4.300", "C", 3, True, date(2026, 11, 6), 12900, "mobilia", "FF&E"),
        ("Banheiro (metais, espelho, acessórios)", "3 × 2.600", "E", 0, False, None, 7800, "mobilia", "FF&E"),
        ("Mobiliário do deck (o café na varanda)", "3 × 1.800", "E", 0, False, None, 5400, "mobilia", "FF&E"),
        ("Equipamentos do apoio (carrinho de camareira, prateleiras da rouparia)", "valor", "E", 0, False, None, 2400, None, "OS&E"),
    ]),
    ("Enxoval, utensílios e suprimentos", [
        ("Enxoval (lavanderia terceirizada, três jogos mesmo assim)", "3 × 1 cama × 3 jogos × 780", "C", 3, True, date(2026, 11, 6), 7020, "mobilia", "OS&E"),
        ("Utensílios de cozinha", "3 × 400", "E", 0, False, None, 1200, "mobilia", "OS&E"),
        ("Governança e limpeza", "valor", "E", 0, False, None, 900, "mobilia", "OS&E"),
        ("Recepção (nenhuma recepção construída)", "", "NA", 0, False, None, 0, None, ""),
        ("Manutenção (ferramentas básicas)", "valor", "E", 0, False, None, 600, "mobilia", "OS&E"),
        ("Segurança (extintores, primeiros socorros, lanternas)", "", "B", 0, False, None, 0, "mobilia", "OS&E"),
        ("Amenidades e suprimentos do primeiro mês", "valor", "E", 0, False, None, 1020, "mobilia", "OS&E"),
    ]),
    ("Pré-abertura", [
        ("Licença de funcionamento e cadastros", "", "B", 0, False, None, 0, None, "Infraestrutura · grupo 9"),
        ("Fotos profissionais e anúncio", "valor", "C", 2, True, date(2026, 11, 10), 4800, None, "Infraestrutura · grupo 9"),
        ("Identidade e lançamento", "valor", "E", 0, False, None, 3500, None, "Infraestrutura · grupo 9"),
        ("Treinamento da pessoa local e manual de operação", "valor", "E", 0, False, None, 2500, None, "Infraestrutura · grupo 9"),
        ("Seguro do primeiro ano", "", "B", 0, False, None, 0, None, "Infraestrutura · grupo 9"),
        ("Abertura de teste (noites com convidados, consumo e ajustes)", "valor", "E", 0, False, None, 1800, None, "Infraestrutura · grupo 9"),
    ]),
]

NOMES_PARTES = [p for p, _ in PARTES] + ["Reserva do imprevisto"]

# ---------------------------------------------------------------- premissas (página 6 da Marina e 6A)
UN_FASE, UN_PROJ = 3, 5
DIST_ENERGIA_M, REDE_PARA = 260, 5
RESERVA_P6, RESERVA_PCT = 10, 15
TERRENO = 600000
# página 6 (Pilar 6): referência orientativa da Zion Glamping Store, não confirmada
P6_PRONTA = 192346
P6_SUBITENS = [("A unidade", 129000), ("Deck", 15000), ("Luz", 10000), ("Água e esgoto", 8500),
               ("Mobiliário, equipamentos e enxoval", 25915), ("Piso interno", 3931)]
P6_LICENCAS = 15000
NOITES = 3 * 365
OCUP, DIARIA, MARGEM = 0.385, 645, 0.40

# ---------------------------------------------------------------- contas
r2 = lambda x: round(x + 1e-9, 2)
TOT = [sum(l[6] for l in ls) for _, ls in PARTES]
SUB = sum(TOT)
RES = SUB * RESERVA_PCT / 100
CAPEX = SUB + RES
TOT7 = TOT + [RES]
PESOS = [t / CAPEX for t in TOT7]

RECEITA_CONS = NOITES * OCUP * DIARIA            # 271.915,875
RESULT_CONS = r2(RECEITA_CONS * MARGEM)          # 108.766,35
GIRO = r2(0.60 * RECEITA_CONS / 12 * 3)          # 40.787,38
LIMITE6 = r2(8 * RESULT_CONS)                    # 870.130,80
P6_UNID = UN_FASE * P6_PRONTA
P6_RES = P6_UNID * RESERVA_P6 / 100
P6_FOLHA = P6_UNID + P6_LICENCAS + P6_RES
P6_TOTAL = r2(P6_FOLHA + GIRO)
P6_FOLGA = r2(LIMITE6 - P6_TOTAL)

INVEST = r2(CAPEX + GIRO)
FOLGA = r2(LIMITE6 - INVEST)
FOLGA_SUB = r2(FOLGA / (1 + RESERVA_PCT / 100))
OBRA = TOT[1] + TOT[2]
PCT_OBRA = OBRA / CAPEX
OSE_FFE = TOT[4] / TOT[3]
PRE_OBRA = TOT[5] / OBRA
FALTA_PRE = max(0, 0.05 * OBRA - TOT[5])
SOBRA_BRANCO = r2(FOLGA_SUB - FALTA_PRE)
AREA = 3 * 38 + 3 * 16 + 30 + 16
AREA_PL1 = 3 * 38 + 3 * 16
CUSTO_UN = r2(CAPEX / UN_FASE)
INVEST_UN = r2(INVEST / UN_FASE)
P6_INVEST_UN = r2(P6_TOTAL / UN_FASE)
CUSTO_M2 = r2(CAPEX / AREA)
CUSTO_M2_PL1 = r2(CAPEX / AREA_PL1)

LINHAS = [l for _, ls in PARTES for l in ls]
CONTADAS = [l for l in LINHAS if l[2] != "NA"]
N = len(CONTADAS)
NC = sum(l[2] == "C" for l in CONTADAS); NE = sum(l[2] == "E" for l in CONTADAS); NB = sum(l[2] == "B" for l in CONTADAS)
NNA = sum(l[2] == "NA" for l in LINHAS)
COTADO_P = [sum(l[6] for l in ls if l[2] == "C") for _, ls in PARTES]
ESTIM_P = [sum(l[6] for l in ls if l[2] == "E") for _, ls in PARTES]
CONT_P = [tuple(sum(l[2] == o for l in ls) for o in ("C", "E", "B", "NA")) for _, ls in PARTES]
COTADO, ESTIM = sum(COTADO_P), sum(ESTIM_P)
PCT_LINHAS = NC / N
PCT_VALOR = COTADO / SUB
FALTAM_MAIORIA = max(0, N // 2 + 1 - NC)
N3 = sum(l[2] == "C" and l[3] >= 3 and l[4] for l in CONTADAS)
NINC = NC - N3
VENCIDAS = [(l[0], (HOJE - l[5]).days) for l in CONTADAS if l[2] == "C" and l[5] and (HOJE - l[5]).days > 90]
TOP3 = sorted(CONTADAS, key=lambda l: -l[6])[:3]
BRANCOS = [l[0] for l in CONTADAS if l[2] == "B"]

# Página 6 × 6A
P6_COBRE = P6_TOTAL / INVEST
DIF_P6 = r2(INVEST - P6_TOTAL)
SEIS_LINHAS = sum(l[6] for l in LINHAS if l[7])          # as seis linhas por cabana, na 6A
AREAS_COMUNS = 66000 + 9600
INFRA_COMUM = TOT[1] - 5400 - 4800
ENTROU = INFRA_COMUM + AREAS_COMUNS + 2400 + TOT[5]

# Transposição para a página 6
l_unidade = 319200 / UN_FASE; l_deck = 33600 / UN_FASE; l_luz = 5400 / UN_FASE; l_agua = 4800 / UN_FASE
l_mobilia = (69600 + TOT[4]) / UN_FASE; l_piso = 0
PRONTA = l_unidade + l_deck + l_luz + l_agua + l_mobilia + l_piso
INFRA_T = (SUB - UN_FASE * PRONTA - TOT[0]) + RESERVA_PCT / 100 * (SUB - UN_FASE * PRONTA)

# Planilha 1
PL1 = {"Premissas": 352800, "Infraestrutura": TOT[0] + TOT[1] + AREAS_COMUNS + TOT[5], "FF&E": 69600, "OS&E": TOT[4] + 2400}

# Exercícios
E2_P2 = TOT[1] - 19800 + 22400; E2_SUB = SUB + 2600; E2_RES = E2_SUB * 0.15; E2_CAPEX = E2_SUB + E2_RES
E2_INV = r2(E2_CAPEX + GIRO); E2_FOLGA = r2(LIMITE6 - E2_INV)
E4_P6 = 0.10 * SEIS_LINHAS; E4_10 = 0.10 * SUB; E4_15 = 0.15 * SUB; E4_DIF = E4_15 - E4_10

# Página 6 refeita
VOLTA = INVEST / RESULT_CONS
VOLTA_T = (INVEST + TERRENO) / RESULT_CONS
DIARIA_LIM = INVEST / 8 / MARGEM / (NOITES * OCUP)
PESO_T = TERRENO / (TERRENO + INVEST)

# ---------------------------------------------------------------- conferência com o PLANO.md v2, seção 7 (falha se divergir)
q = lambda a, b, t=0.005: abs(a - b) <= t
assert TOT == [36000, 128200, 428400, 72000, 10740, 12600], TOT
assert SUB == 687940 and RES == 103191 and CAPEX == 791131, (SUB, RES, CAPEX)
assert q(RECEITA_CONS, 271915.875) and RESULT_CONS == 108766.35 and GIRO == 40787.38 and LIMITE6 == 870130.80
assert P6_UNID == 577038 and q(P6_RES, 57703.80) and q(P6_FOLHA, 649741.80) and P6_TOTAL == 690529.18 and P6_FOLGA == 179601.62
assert sum(v for _, v in P6_SUBITENS) == P6_PRONTA
assert INVEST == 831918.38 and FOLGA == 38212.42 and FOLGA_SUB == 33228.19 and q(FALTA_PRE, 15230) and SOBRA_BRANCO == 17998.19
# pesos: o plano escreve 0,162047 na Parte 2; o valor exato é 0,1620465 (diferença na 7ª casa). Confere com 1e-6 e no exibido.
assert all(abs(a - b) <= 1e-6 for a, b in zip(PESOS, [0.045504, 0.162047, 0.541503, 0.091009, 0.013576, 0.015927, 0.130435]))
assert [round(p * 100, 1) for p in PESOS] == [4.6, 16.2, 54.2, 9.1, 1.4, 1.6, 13.0]
assert COTADO_P == [32500, 99300, 418800, 50700, 7020, 4800] and ESTIM_P == [3500, 28900, 9600, 21300, 3720, 7800]
assert COTADO == 613120 and ESTIM == 74820 and COTADO + ESTIM == SUB
assert CONT_P == [(3, 2, 1, 0), (5, 4, 1, 0), (3, 1, 0, 0), (3, 4, 0, 0), (1, 4, 1, 1), (1, 3, 2, 0)], CONT_P
assert (N, NC, NE, NB, NNA) == (39, 16, 18, 5, 1)
assert round(PCT_LINHAS * 100, 1) == 41.0 and round(PCT_VALOR * 100, 1) == 89.1 and FALTAM_MAIORIA == 4
assert (N3, NINC) == (7, 9) and VENCIDAS == [("Água: poço com teste de vazão, reservatório e rede para 5", 135)]
assert [l[6] for l in TOP3] == [319200, 66000, 33600] and all(l[2] == "C" for l in TOP3) and PCT_LINHAS <= 0.5  # Estimador
assert AREA == 208 and AREA_PL1 == 162 and CUSTO_M2 == 3803.51 and CUSTO_M2_PL1 == 4883.52
assert CUSTO_UN == 263710.33 and INVEST_UN == 277306.13 and P6_INVEST_UN == 230176.39
assert OBRA == 556600 and round(PCT_OBRA * 100, 1) == 70.4 and round(OSE_FFE * 100, 1) == 14.9 and round(PRE_OBRA * 100, 1) == 2.3
assert round(P6_COBRE * 100, 1) == 83.0 and DIF_P6 == 141389.20
assert INFRA_COMUM == 118000 and AREAS_COMUNS == 75600 and ENTROU == 208600 and SEIS_LINHAS == 443340
assert q(ENTROU + 21000 + 45487.20 - 133698, DIF_P6) and TOT[0] - P6_LICENCAS == 21000 and q(RES - P6_RES, 45487.20) and P6_UNID - SEIS_LINHAS == 133698
assert (l_unidade, l_deck, l_luz, l_agua, l_mobilia) == (106400, 11200, 1800, 1600, 26780) and PRONTA == 147780
assert q(INFRA_T, 245290) and q(UN_FASE * PRONTA * 1.15 + TOT[0] + INFRA_T, CAPEX, 0.01)
assert q(0.15 * 443340, 66501) and q(0.15 * (SUB - 443340), 36690)
assert PL1 == {"Premissas": 352800, "Infraestrutura": 252400, "FF&E": 69600, "OS&E": 13140} and sum(PL1.values()) == SUB
assert E2_P2 == 130800 and E2_SUB == 690540 and q(E2_RES, 103581) and q(E2_CAPEX, 794121) and E2_INV == 834908.38 and E2_FOLGA == 35222.42
assert q(E4_P6, 44334) and q(E4_10, 68794) and q(E4_15, 103191) and q(E4_DIF, 34397)
assert round(VOLTA, 2) == 7.65 and round(VOLTA_T, 2) == 13.17 and round(DIARIA_LIM, 2) == 616.67 and round(PESO_T * 100, 1) == 41.9
assert round((HOJE - date(2026, 7, 15)).days) == 135


def brl(v, casas=0):
    s = f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + s


def num(v, casas=0):
    return brl(v, casas)[3:]


def pct(v, casas=1):
    return f"{v * 100:.{casas}f}".replace(".", ",") + "%"


if __name__ == "__main__":
    print("Marina · 6A conferida com o PLANO.md v2, seção 7")
    print("partes", TOT, "subtotal", SUB, "reserva", RES, "CAPEX", CAPEX)
    print("investimento", INVEST, "limite", LIMITE6, "folga", FOLGA, "linhas", N, NC, NE, NB, NNA)

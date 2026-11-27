"""Caso didático Chalés do Ribeirão (dados fictícios), do PLANO.md seção 7.
As contas são feitas aqui e conferidas com os totais do plano (assert), para o e-book nunca divergir do plano."""

# (nome, valor, origem, n_cotacoes, mesma_espec)  origem: C cotação, E estimativa, B em branco, NA não se aplica
BLOCOS = [
    ("1 · Projetos, licenças e documentação", [
        ("Arquitetura", 18000, "C", 3, True), ("Engenharias", 14000, "C", 2, True),
        ("Levantamento do terreno", 3500, "C", 3, True), ("Aprovações e taxas da prefeitura", 4500, "E", 0, False),
        ("Licença ambiental", 0, "B", 0, False)]),
    ("2 · Infraestrutura", [
        ("Acesso e caminhos", 36000, "C", 3, True), ("Energia, rede comum", 42000, "C", 1, False),
        ("Água, poço e reservatório (cotação de 20/07/2026)", 28000, "C", 2, True), ("Esgoto e tratamento", 32000, "C", 2, True),
        ("Ligação de luz de cada unidade: 4 × 3.500", 14000, "E", 0, False), ("Água e esgoto de cada unidade: 4 × 2.500", 10000, "E", 0, False),
        ("Estacionamento", 8000, "C", 2, True), ("Internet", 0, "B", 0, False)]),
    ("3 · Unidades e áreas comuns", [
        ("Chalés: 4 × 32 m² × 4.500 por m² (piso incluído)", 576000, "C", 3, True),
        ("Deck de cada chalé: 4 × 9.000 (10 m² cada)", 36000, "C", 2, True),
        ("Área de apoio e lavanderia: 20 m² × 3.500 por m²", 70000, "C", 1, False)]),
    ("4 · Mobiliário e equipamentos", [
        ("Cama e colchão: 4 × 4.800", 19200, "C", 3, True), ("Mobiliário: 4 × 7.200", 28800, "C", 2, True),
        ("Iluminação: 4 × 1.800", 7200, "E", 0, False), ("Cozinha compacta e eletrodomésticos: 4 × 5.400", 21600, "C", 3, True),
        ("Equipamentos da lavanderia", 9000, "C", 2, True)]),
    ("5 · Enxoval, utensílios e suprimentos", [
        ("Enxoval: 4 chalés × 1 cama × 3 jogos × 700", 8400, "C", 3, True), ("Utensílios: 4 × 500", 2000, "E", 0, False),
        ("Governança e limpeza", 800, "E", 0, False), ("Manutenção", 500, "E", 0, False),
        ("Segurança", 0, "B", 0, False), ("Recepção (check-in sem recepção)", 0, "NA", 0, False)]),
    ("6 · Pré-abertura", [
        ("Licença de funcionamento e cadastros", 0, "B", 0, False), ("Fotos e site", 6500, "C", 2, True),
        ("Identidade e marketing de lançamento", 8000, "E", 0, False), ("Treinamento e contratação", 4000, "E", 0, False),
        ("Seguro do primeiro ano", 0, "B", 0, False), ("Abertura de teste", 2500, "E", 0, False)]),
]

UN_FASE, UN_PROJ, RESERVA_PCT, GIRO, TERRENO, PALPITE = 4, 6, 15, 45000, 300000, 700000
AREA = 4 * 32 + 4 * 10 + 20

tot = [sum(l[1] for l in ls) for _, ls in BLOCOS]
SUB = sum(tot)
RES = SUB * RESERVA_PCT / 100
CAPEX = SUB + RES
OBRA = tot[1] + tot[2]
INVEST = CAPEX + GIRO
linhas = [l for _, ls in BLOCOS for l in ls if l[2] != "NA"]
N = len(linhas); NC = sum(l[2] == "C" for l in linhas); NE = sum(l[2] == "E" for l in linhas); NB = sum(l[2] == "B" for l in linhas)
COTADO = sum(l[1] for l in linhas if l[2] == "C"); ESTIM = sum(l[1] for l in linhas if l[2] == "E")
N3 = sum(l[2] == "C" and l[3] >= 3 and l[4] for l in linhas); NINC = NC - N3
PESOS = [t / CAPEX for t in tot] + [RES / CAPEX]

assert tot == [40000, 170000, 682000, 85800, 11700, 21000], tot
assert SUB == 1010500 and RES == 151575 and CAPEX == 1162075 and INVEST == 1207075
assert (N, NC, NE, NB) == (32, 17, 10, 5) and COTADO == 957000 and ESTIM == 53500 and (N3, NINC) == (7, 10)
assert AREA == 188 and round(CAPEX / AREA, 2) == 6181.25 and CAPEX / UN_FASE == 290518.75
assert abs(sum(PESOS) - 1) < 1e-9
# E2, E4 e a transposição para a página 6
assert 1010500 - 682000 + (4 * 150000 + 36000 + 70000) == 1034500 and 1034500 * 1.15 == 1189675
assert 1010500 * 0.08 == 80840 and 151575 - 80840 == 70735
pronta = 144000 + 9000 + 3500 + 2500 + (76800 + 11700) / 4
assert pronta == 181125 and abs(4 * pronta * 1.15 + 40000 + 288900 - CAPEX) < 0.01


def brl(v, casas=0):
    s = f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + s


def pct(v, casas=1):
    return f"{v * 100:.{casas}f}".replace(".", ",") + "%"

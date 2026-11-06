"""Planilhas do Club Zion Collection · plano Base (Trilha de Desenvolvimento):
   1. Orcamento-de-Abertura-Zion-{EM-BRANCO,EXEMPLO}.xlsx  (infraestrutura, construção, FF&E e OS&E)
   2. Estudo-de-Massas-e-Viabilidade-Zion-{EM-BRANCO,EXEMPLO}.xlsx (massas, venda, renda, TIR, VPL)
Uso: python3 -I build.py <pasta de saída>
Material educativo: todos os números saem das premissas digitadas pelo membro. Não é projeção nem promessa de retorno."""
import sys, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, PRETO, CREME, TERRA, CINZA = "1B2117", "040605", "FEF5F0", "8B714E", "5F5F55"
ENTRADA = PatternFill("solid", fgColor="FFF4C7")
CALC = PatternFill("solid", fgColor="E3EEDF")
CAB = PatternFill("solid", fgColor=MUSGO)
GRUPO = PatternFill("solid", fgColor="EFE6D6")
DEST = PatternFill("solid", fgColor="C9A84C")
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
T = lambda sz=10, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)
WRAP = Alignment(wrap_text=True, vertical="center")
BRL, PCT, NUM, M2 = 'R$ #,##0', '0.0%', '#,##0.00', '#,##0 "m²"'

def cab(ws, l, tit, h=40):
    for j, t in enumerate(tit, 1):
        c = ws.cell(l, j, t); c.font = T(10, True, CREME); c.fill = CAB; c.alignment = WRAP; c.border = borda
    ws.row_dimensions[l].height = h
def ent(c, v=None, fmt=None):
    c.value = v; c.fill = ENTRADA; c.border = borda; c.alignment = WRAP; c.font = T(10)
    if fmt: c.number_format = fmt
def calc(c, f, fmt=None, b=False):
    c.value = f; c.fill = CALC; c.border = borda; c.alignment = WRAP; c.font = T(10, b)
    if fmt: c.number_format = fmt
def txt(c, v, b=False, sz=10, col=PRETO, fill=None, i=False):
    c.value = v; c.font = T(sz, b, col, i); c.alignment = WRAP; c.border = borda
    if fill: c.fill = fill
def titulo(ws, t, sub=None, aviso=None):
    ws.sheet_view.showGridLines = False
    ws["A1"] = t; ws["A1"].font = T(18, True, MUSGO)
    if sub: ws["A2"] = sub; ws["A2"].font = T(10, True, TERRA)
    if aviso: ws["A3"] = aviso; ws["A3"].font = T(9, c=CINZA, i=True)
def lista(ws, rng, opcoes):
    dv = DataValidation(type="list", formula1='"' + ",".join(opcoes) + '"', allow_blank=True,
                        showErrorMessage=True, errorTitle="Opção inválida", error="Escolha uma opção da lista.")
    ws.add_data_validation(dv); dv.add(rng)
def larguras(ws, ws_w):
    for col, w in zip("ABCDEFGHIJKL", ws_w): ws.column_dimensions[col].width = w
def comece(wb, cabecalho, titulo_, linhas, exemplo):
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 108
    base = [(cabecalho, T(10, True, TERRA)), (titulo_, T(22, True, MUSGO))]
    base.append(("EXEMPLO PREENCHIDO COM NÚMEROS FICTÍCIOS, só para você ver a planilha funcionando. Para o seu projeto, use a versão em branco." if exemplo
                 else "Versão em branco: as listas de referência já vêm prontas. Preencha as células amarelas com os seus números.",
                 T(11, True, "A0522D" if exemplo else MUSGO)))
    for i, (t, f) in enumerate(base + linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")
    return ws

TIPOS = ["Suíte de hotel ou pousada", "Chalé com cozinha e banheira", "Bolha ou cabana de glamping"]
RODAPE = "Zion Hospitality Business · Club Zion Collection · Material educativo. Os resultados dependem das premissas que você digitar: não são projeção nem promessa de renda, retorno, ocupação ou valorização. A Zion avalia cada caso."

# ===================================================================================
# PLANILHA 1 · ORÇAMENTO DE ABERTURA
# ===================================================================================
INFRA = [  # grupo, item, unidade, qtd exemplo, custo exemplo, dica
    ("1 · Projetos e licenças", "Levantamento topográfico e sondagem do solo", "serviço", 1, 6500, "Antes de qualquer desenho. Define onde dá para construir."),
    ("1 · Projetos e licenças", "Projeto arquitetônico e masterplan", "serviço", 1, 25000, "Arquiteto com experiência em hospedagem. Inclui as unidades e as áreas comuns."),
    ("1 · Projetos e licenças", "Projetos complementares (estrutural, elétrico, hidráulico)", "serviço", 1, 12000, "Obrigatórios para aprovação e para a obra sair certa."),
    ("1 · Projetos e licenças", "Licenciamento ambiental e aprovação na prefeitura", "serviço", 1, 15000, "Varia muito por município. Consulte antes de orçar a obra."),
    ("1 · Projetos e licenças", "Consultoria e taxas (ART, RRT, cartório)", "serviço", 1, 4000, "Responsabilidade técnica e registros."),
    ("2 · Terreno e terraplanagem", "Limpeza do terreno e supressão autorizada", "m²", 2000, 6, "Só o que a licença permite. Mantenha a vegetação que é o seu diferencial."),
    ("2 · Terreno e terraplanagem", "Terraplanagem e platôs das unidades", "m²", 600, 45, "Cada unidade precisa de uma base plana. Platô pequeno custa menos e preserva mais."),
    ("2 · Terreno e terraplanagem", "Drenagem e contenção", "m", 120, 180, "Água mal drenada destrói deck e base. Não economize aqui."),
    ("3 · Acessos e vias", "Via de acesso interna (cascalho ou piso drenante)", "m²", 800, 60, "Do portão até o estacionamento e as unidades."),
    ("3 · Acessos e vias", "Estacionamento", "vaga", 10, 1500, "Uma vaga por unidade mais vagas de serviço."),
    ("3 · Acessos e vias", "Trilhas e caminhos entre as unidades", "m", 300, 120, "Iluminados e com piso seguro para a noite e a chuva."),
    ("3 · Acessos e vias", "Portão, cerca e sinalização", "serviço", 1, 18000, "Primeira impressão e segurança."),
    ("4 · Energia", "Padrão de entrada e ligação com a concessionária", "serviço", 1, 12000, "Peça a carga ao projetista elétrico. Bolha e ar-condicionado pesam."),
    ("4 · Energia", "Rede elétrica interna até as unidades", "m", 500, 95, "Enterrada, sempre que possível."),
    ("4 · Energia", "Sistema solar fotovoltaico (opcional)", "kWp", 10, 4500, "Reduz a conta mensal. Compare com o payback do sistema."),
    ("4 · Energia", "Gerador ou nobreak para emergências (opcional)", "unidade", 1, 15000, "Em área rural, a queda de energia é comum."),
    ("5 · Água e esgoto", "Poço artesiano ou ligação de água", "serviço", 1, 22000, "Faça o teste de vazão e a análise da água."),
    ("5 · Água e esgoto", "Reservatório e bombeamento", "serviço", 1, 9000, "Reserva de pelo menos 2 dias de consumo."),
    ("5 · Água e esgoto", "Rede hidráulica até as unidades", "m", 500, 70, ""),
    ("5 · Água e esgoto", "Fossa, filtro e sumidouro (ou estação compacta)", "unidade", 2, 9000, "Dimensionada pelo número de hóspedes. Exigida no licenciamento."),
    ("5 · Água e esgoto", "Aquecimento de água (solar, gás ou elétrico)", "unidade", 10, 3200, "Uma por unidade ou central."),
    ("6 · Internet e segurança", "Internet (fibra, rádio ou satélite) e rede Wi-Fi", "serviço", 1, 8000, "Hóspede sem internet avalia mal. Inclua repetidores."),
    ("6 · Internet e segurança", "Câmeras, alarme e iluminação de segurança", "serviço", 1, 12000, ""),
    ("7 · Áreas comuns", "Recepção e apoio (construção)", "m²", 40, 3500, "Pode começar pequena e crescer com a operação."),
    ("7 · Áreas comuns", "Cozinha de apoio ou café da manhã", "m²", 30, 3800, ""),
    ("7 · Áreas comuns", "Lavanderia e depósito", "m²", 25, 3000, "Enxoval precisa de lugar para lavar, secar e guardar."),
    ("7 · Áreas comuns", "Piscina, ofurô ou spa (opcional)", "unidade", 1, 85000, "Atração que sustenta diária mais alta. Entra na fase que couber."),
    ("7 · Áreas comuns", "Deck de convivência, fogueira e lounge", "m²", 60, 900, ""),
    ("8 · Paisagismo e iluminação", "Paisagismo e recomposição", "m²", 1500, 25, "Plantas nativas custam menos e pedem menos água."),
    ("8 · Paisagismo e iluminação", "Iluminação externa e de caminhos", "ponto", 60, 450, "Luz baixa e quente. A noite também é produto."),
    ("9 · Mão de obra e gestão da obra", "Mão de obra não incluída nos itens acima", "mês", 6, 18000, "Se os custos unitários acima já incluem mão de obra, deixe zero."),
    ("9 · Mão de obra e gestão da obra", "Gestão e fiscalização da obra", "mês", 6, 4000, "Alguém precisa conferir medição e qualidade."),
    ("9 · Mão de obra e gestão da obra", "Canteiro, ferramentas e frete de materiais", "serviço", 1, 15000, "Frete pesa muito em área remota."),
]
FFE = {  # tipologia: [(ambiente, item, qtd por unidade, preço exemplo)]
    TIPOS[0]: [
        ("Quarto", "Cama box queen ou king", 1, 2800), ("Quarto", "Colchão de hotel (densidade alta)", 1, 2600), ("Quarto", "Cabeceira estofada", 1, 1200),
        ("Quarto", "Mesa de cabeceira", 2, 450), ("Quarto", "Abajur ou arandela de leitura", 2, 280), ("Quarto", "Poltrona ou chaise", 1, 1100),
        ("Quarto", "Mesa de apoio ou escrivaninha com cadeira", 1, 900), ("Quarto", "Armário ou closet aberto com cabides", 1, 1800), ("Quarto", "Cofre", 1, 450),
        ("Quarto", "Frigobar", 1, 1400), ("Quarto", "TV 43\" ou maior com suporte", 1, 2200), ("Quarto", "Ar-condicionado split 12.000 BTU", 1, 3200),
        ("Quarto", "Cortina blackout e voil", 1, 1200), ("Quarto", "Tapete", 1, 500), ("Quarto", "Espelho de corpo inteiro", 1, 450),
        ("Quarto", "Luminárias e pendentes", 2, 350), ("Quarto", "Bandeja, chaleira elétrica e kit café", 1, 400), ("Quarto", "Lixeiras (quarto e banheiro)", 2, 90),
        ("Banheiro", "Box de vidro", 1, 1500), ("Banheiro", "Chuveiro e metais (misturador, ducha)", 1, 1400), ("Banheiro", "Vaso sanitário com caixa acoplada", 1, 900),
        ("Banheiro", "Cuba, bancada e torneira", 1, 1600), ("Banheiro", "Espelho com iluminação", 1, 600), ("Banheiro", "Secador de cabelo", 1, 180),
        ("Banheiro", "Porta-toalhas, ganchos e acessórios", 1, 350), ("Banheiro", "Dispensers de amenities (fixos)", 3, 120),
    ],
    TIPOS[1]: [
        ("Quarto", "Cama box queen ou king", 1, 2800), ("Quarto", "Colchão de hotel (densidade alta)", 1, 2600), ("Quarto", "Cabeceira", 1, 1200),
        ("Quarto", "Mesa de cabeceira", 2, 450), ("Quarto", "Abajur ou arandela", 2, 280), ("Quarto", "Poltrona ou sofá pequeno", 1, 1500),
        ("Quarto", "Armário ou arara com cabides", 1, 1200), ("Quarto", "Cofre", 1, 450), ("Quarto", "TV com suporte", 1, 2200),
        ("Quarto", "Ar-condicionado ou climatizador", 1, 3200), ("Quarto", "Cortina blackout", 1, 1000), ("Quarto", "Tapete e espelho", 1, 800),
        ("Quarto", "Luminárias e iluminação indireta", 3, 350), ("Quarto", "Lareira ou aquecedor (clima frio)", 1, 2500),
        ("Banheiro", "Banheira de imersão ou hidro", 1, 6500), ("Banheiro", "Box, chuveiro e metais", 1, 2500), ("Banheiro", "Vaso sanitário", 1, 900),
        ("Banheiro", "Cuba, bancada e torneira", 1, 1600), ("Banheiro", "Espelho com iluminação", 1, 600), ("Banheiro", "Secador, acessórios e dispensers", 1, 700),
        ("Cozinha gourmet", "Cooktop 2 bocas (indução ou gás)", 1, 900), ("Cozinha gourmet", "Coifa ou depurador", 1, 700), ("Cozinha gourmet", "Geladeira compacta ou frigobar grande", 1, 2200),
        ("Cozinha gourmet", "Micro-ondas", 1, 700), ("Cozinha gourmet", "Cafeteira e chaleira elétrica", 1, 500), ("Cozinha gourmet", "Pia, bancada e torneira", 1, 1800),
        ("Cozinha gourmet", "Armários e prateleiras", 1, 2000), ("Cozinha gourmet", "Mesa de refeição com 2 cadeiras ou bancada", 1, 1500),
        ("Deck e externo", "Mobiliário de deck (espreguiçadeira, mesa, cadeiras)", 1, 2500), ("Deck e externo", "Ofurô ou banheira externa (opcional)", 1, 9000), ("Deck e externo", "Iluminação externa e rede", 1, 800),
    ],
    TIPOS[2]: [
        ("Estrutura", "Bolha ou cabana (estrutura principal)", 1, 69000), ("Estrutura", "Turbina ou sistema de insuflação (bolha)", 1, 0), ("Estrutura", "Capa blackout ou cobertura térmica", 1, 0),
        ("Estrutura", "Base plana ou deck de apoio", 1, 12500), ("Estrutura", "Ar-condicionado split ou portátil", 1, 3200),
        ("Quarto", "Cama box queen ou king", 1, 2800), ("Quarto", "Colchão de hotel", 1, 2600), ("Quarto", "Mesa de cabeceira", 2, 450),
        ("Quarto", "Abajur ou luminária de chão", 2, 350), ("Quarto", "Poltrona ou puff", 2, 600), ("Quarto", "Arara ou baú para roupas", 1, 700),
        ("Quarto", "Frigobar", 1, 1400), ("Quarto", "Tapete e itens de decoração", 1, 900), ("Quarto", "Iluminação de LED indireta e lanterna", 1, 500),
        ("Banheiro", "Banheiro anexo: box, chuveiro, vaso e cuba (ou banheira)", 1, 7500), ("Banheiro", "Aquecedor de água", 1, 1800), ("Banheiro", "Espelho, acessórios e dispensers", 1, 600),
        ("Cozinha e deck", "Cooktop, chaleira, cafeteira e mini pia (opcional)", 1, 2500), ("Cozinha e deck", "Mobiliário de deck e ofurô (opcional)", 1, 9000), ("Cozinha e deck", "Telescópio, rede e itens de experiência", 1, 1200),
    ],
}
OSE_ENXOVAL = [  # item, peças por unidade, jogos em rotação, preço unitário
    ("Lençol de cima e de baixo (par)", 1, 3, 220), ("Fronha", 4, 3, 35), ("Travesseiro", 4, 1, 90), ("Protetor de colchão", 1, 2, 120),
    ("Edredom ou duvet", 1, 2, 350), ("Capa de edredom", 1, 3, 180), ("Cobertor ou manta", 1, 2, 160), ("Colcha ou peseira decorativa", 1, 1, 220),
    ("Toalha de banho", 2, 3, 60), ("Toalha de rosto", 2, 3, 28), ("Toalha de piso", 1, 3, 35), ("Roupão", 2, 2, 140), ("Chinelo de quarto (par)", 2, 1, 15),
    ("Cortina de box ou tapete de banho", 1, 2, 60), ("Pano de prato e jogo americano (chalé e bolha)", 2, 2, 25),
]
OSE_CONSUMO = [  # item, qtd inicial por unidade, preço
    ("Kit de amenities (sabonete, shampoo, condicionador, hidratante)", 30, 9), ("Papel higiênico (rolos)", 24, 1.2), ("Café, chá, açúcar e adoçante (kits)", 30, 4),
    ("Água mineral de cortesia", 30, 2.5), ("Material de limpeza da unidade (kit mensal)", 3, 60), ("Velas, aromatizador e itens de boas-vindas", 10, 12),
]
OSE_COZINHA = [  # item, qtd por unidade, preço  (chalé e bolha com cozinha)
    ("Jogo de pratos, pires e tigelas (6 peças)", 1, 180), ("Copos e taças (jogo)", 1, 150), ("Xícaras e canecas", 4, 25), ("Talheres (jogo)", 1, 120),
    ("Panelas, frigideira e chaleira", 1, 420), ("Utensílios (concha, espátula, tábua, faca, abridor)", 1, 160), ("Escorredor, lixeira e pano", 1, 90),
]
OSE_PROJETO = [  # item do projeto inteiro, qtd, preço
    ("Carrinho de camareira e cestos de roupa", 2, 900), ("Máquina de lavar e secadora (lavanderia)", 1, 7500), ("Ferro, tábua e itens de lavanderia", 1, 600),
    ("Estoque de reposição de enxoval (10% do total)", 1, 0), ("Uniformes da equipe", 6, 150), ("Materiais de recepção (sinalização, chaves, cadastro)", 1, 1500),
    ("Software de reservas e canal manager (1º ano)", 1, 3600), ("Fotos profissionais e site", 1, 6000), ("Kit de primeiros socorros e extintores", 1, 1200),
]

def planilha_orcamento(exemplo):
    wb = Workbook()
    comece(wb, "CLUB ZION COLLECTION · TRILHA DE DESENVOLVIMENTO · PLANILHA 1", "Orçamento de Abertura", [
        ("Infraestrutura, construção, FF&E (mobília e equipamentos) e OS&E (enxoval, utensílios e consumíveis) de uma hospedagem, do terreno à primeira diária.", T(11, c="2D352A")),
        ("Para suíte de hotel ou pousada, chalé com cozinha e banheira, e bolha ou cabana de glamping.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 5 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Premissas: diga quantas unidades de cada tipologia você vai abrir, o tamanho de cada uma e o custo do m² de construção na sua região. Peça esse custo a um construtor local ou use o CUB do seu estado como referência.", None),
        ("2. Aba Infraestrutura: é o que o terreno precisa receber antes das unidades (acesso, energia, água, esgoto, áreas comuns). Ajuste quantidades e custos. O que não se aplica, deixe zero.", None),
        ("3. Aba FF&E: é tudo o que vai dentro de cada unidade e não é consumido (cama, colchão, mesinha, abajur, ar-condicionado, cooktop, banheira). A lista de referência já vem pronta por tipologia. Preencha o preço unitário; a quantidade por unidade você pode ajustar.", None),
        ("4. Aba OS&E: é o enxoval e o que se repõe (lençóis, toalhas, amenities, louça). Enxoval é calculado por peças × jogos em rotação (um em uso, um na lavanderia, um de reserva).", None),
        ("5. Aba Resumo: o total do investimento (CAPEX), o custo por unidade pronta e o custo por m². Copie esses valores na Planilha 2, Estudo de Massas e Viabilidade.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).   Bege = títulos de grupo.", None),
        ("", None),
        ("DICAS DE QUEM OPERA", T(12, True, MUSGO)),
        ("Comece pelo mínimo produto viável: poucas unidades bem feitas e as áreas comuns na fase seguinte. Orce a infraestrutura inteira mesmo assim, porque ela é o que mais surpreende.", None),
        ("Peça 3 orçamentos para os itens grandes (bolha, banheira, ar-condicionado, poço, solar). Frete e instalação em área remota podem passar de 15% do valor do item.", None),
        ("A contingência de 10% a 15% não é opcional. Toda obra tem imprevisto.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice.", T(10, c=CINZA, i=True)),
        (RODAPE, T(9, c=CINZA, i=True)),
    ], exemplo)

    # ---------- Premissas ----------
    pr = wb.create_sheet("Premissas"); titulo(pr, "Premissas do projeto", "Preencha as células amarelas. As outras abas usam estes números.")
    larguras(pr, (34, 16, 16, 16, 18, 18, 20, 20))
    txt(pr["A5"], "Nome do projeto"); ent(pr["B5"], "Refúgio Exemplo · Serra" if exemplo else None); pr.merge_cells("B5:D5")
    txt(pr["A6"], "Município e estado"); ent(pr["B6"], "Urubici, SC" if exemplo else None); pr.merge_cells("B6:D6")
    cab(pr, 8, ["Tipologia", "Nº de unidades", "Área coberta por unidade (m²)", "Deck ou varanda por unidade (m²)", "Custo de construção da área coberta (R$/m²)", "Custo do deck (R$/m²)", "Custo de construção por unidade (R$)", "Total de construção (R$)"], 54)
    ex = [(4, 28, 8, 4200, 900), (3, 45, 20, 4600, 900), (3, 28, 25, 0, 900)]
    for i, tp in enumerate(TIPOS):
        r = 9 + i
        txt(pr.cell(r, 1), tp, True)
        for j in range(5): ent(pr.cell(r, 2 + j), ex[i][j] if exemplo else None, BRL if j >= 3 else None)
        calc(pr.cell(r, 7), f"=C{r}*E{r}+D{r}*F{r}", BRL); calc(pr.cell(r, 8), f"=B{r}*G{r}", BRL)
    txt(pr["A12"], "Total", True, fill=GRUPO); calc(pr["B12"], "=SUM(B9:B11)", None, True)
    calc(pr["C12"], "=SUMPRODUCT(B9:B11,C9:C11)", M2); calc(pr["D12"], "=SUMPRODUCT(B9:B11,D9:D11)", M2)
    for c in ("E12", "F12"): txt(pr[c], "", fill=GRUPO)
    calc(pr["G12"], "=IF(B12=0,0,H12/B12)", BRL); calc(pr["H12"], "=SUM(H9:H11)", BRL, True)
    txt(pr["A13"], "Para a bolha, a estrutura entra na aba FF&E (é um equipamento). Aqui fica só a base plana ou o deck.", sz=9, col=CINZA, i=True); pr.merge_cells("A13:H13")
    txt(pr["A15"], "Contingência sobre o total (imprevistos)"); ent(pr["B15"], 0.12 if exemplo else 0.10, PCT)
    txt(pr["A16"], "Área construída total (coberta + deck), m²"); calc(pr["B16"], "=C12+D12", M2)
    txt(pr["A18"], RODAPE, sz=9, col=CINZA, i=True); pr.merge_cells("A18:H18")

    # ---------- Infraestrutura ----------
    inf = wb.create_sheet("Infraestrutura"); titulo(inf, "Infraestrutura, obras externas e áreas comuns",
        "O que o terreno recebe antes das unidades. Ajuste quantidade e custo unitário; o que não se aplica, deixe zero.")
    larguras(inf, (30, 46, 10, 12, 16, 16, 52))
    cab(inf, 5, ["Grupo", "Item", "Unidade", "Quantidade", "Custo unitário (R$)", "Total (R$)", "Dica"])
    r = 6
    for g, item, un, q, custo, dica in INFRA:
        txt(inf.cell(r, 1), g, sz=9); txt(inf.cell(r, 2), item); txt(inf.cell(r, 3), un)
        ent(inf.cell(r, 4), q if exemplo else None, NUM); ent(inf.cell(r, 5), custo if exemplo else None, BRL)
        calc(inf.cell(r, 6), f"=D{r}*E{r}", BRL); txt(inf.cell(r, 7), dica, sz=9, col=CINZA, i=True); r += 1
    fim = r - 1
    for _ in range(8):  # linhas livres
        txt(inf.cell(r, 1), "", sz=9); ent(inf.cell(r, 2)); ent(inf.cell(r, 3)); ent(inf.cell(r, 4), None, NUM); ent(inf.cell(r, 5), None, BRL)
        calc(inf.cell(r, 6), f"=D{r}*E{r}", BRL); txt(inf.cell(r, 7), "Linha livre: digite o grupo na coluna A para entrar no subtotal.", sz=9, col=CINZA, i=True); r += 1
    lista(inf, f"A{fim+1}:A{r-1}", sorted({g for g, *_ in INFRA}))
    ult = r - 1; r += 1
    txt(inf.cell(r, 1), "Subtotais por grupo", True, fill=GRUPO); inf.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7); r += 1
    sub0 = r
    for g in sorted({g for g, *_ in INFRA}):
        txt(inf.cell(r, 1), g); calc(inf.cell(r, 6), f'=SUMIF($A$6:$A${ult},A{r},$F$6:$F${ult})', BRL); r += 1
    txt(inf.cell(r, 1), "TOTAL DE INFRAESTRUTURA", True, fill=GRUPO); calc(inf.cell(r, 6), f"=SUM(F{sub0}:F{r-1})", BRL, True)
    INF_TOTAL = f"Infraestrutura!F{r}"; INF_SUB0, INF_SUB1 = sub0, r - 1

    # ---------- FF&E ----------
    ff = wb.create_sheet("FF&E"); titulo(ff, "FF&E · Mobília, equipamentos e decoração por unidade",
        "O que vai dentro de cada unidade e não se consome. Lista de referência por tipologia: ajuste quantidades, preencha preços.")
    larguras(ff, (18, 50, 12, 16, 18, 12, 18))
    r = 5; FFE_TOT = {}
    for i, tp in enumerate(TIPOS):
        txt(ff.cell(r, 1), tp.upper(), True, 11, CREME, DEST); ff.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7); r += 1
        cab(ff, r, ["Ambiente", "Item", "Qtd por unidade", "Preço unitário (R$)", "Total por unidade (R$)", "Nº de unidades", "Total do projeto (R$)"]); r += 1
        ini = r
        for amb, item, q, preco in FFE[tp]:
            txt(ff.cell(r, 1), amb, sz=9); txt(ff.cell(r, 2), item); ent(ff.cell(r, 3), q, NUM); ent(ff.cell(r, 4), preco if exemplo else None, BRL)
            calc(ff.cell(r, 5), f"=C{r}*D{r}", BRL); calc(ff.cell(r, 6), f"=Premissas!$B${9+i}"); calc(ff.cell(r, 7), f"=E{r}*F{r}", BRL); r += 1
        for _ in range(4):
            ent(ff.cell(r, 1)); ent(ff.cell(r, 2)); ent(ff.cell(r, 3), None, NUM); ent(ff.cell(r, 4), None, BRL)
            calc(ff.cell(r, 5), f"=C{r}*D{r}", BRL); calc(ff.cell(r, 6), f"=Premissas!$B${9+i}"); calc(ff.cell(r, 7), f"=E{r}*F{r}", BRL); r += 1
        txt(ff.cell(r, 1), "Total FF&E por unidade e do projeto", True, fill=GRUPO); ff.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
        calc(ff.cell(r, 5), f"=SUM(E{ini}:E{r-1})", BRL, True); txt(ff.cell(r, 6), "", fill=GRUPO); calc(ff.cell(r, 7), f"=SUM(G{ini}:G{r-1})", BRL, True)
        FFE_TOT[tp] = (f"'FF&E'!E{r}", f"'FF&E'!G{r}"); r += 2
    txt(ff.cell(r, 1), "Na bolha, o item 'Bolha ou cabana' é o preço do fabricante com turbina e capa; se vierem separados, use as linhas seguintes. Frete e instalação entram na Infraestrutura (grupo 9).", sz=9, col=CINZA, i=True); ff.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)

    # ---------- OS&E ----------
    os_ = wb.create_sheet("OS&E"); titulo(os_, "OS&E · Enxoval, consumíveis, utensílios e itens de operação",
        "Enxoval: peças por unidade × jogos em rotação (em uso, na lavanderia, de reserva). Consumíveis: estoque de abertura.")
    larguras(os_, (50, 14, 14, 14, 16, 18, 12, 18))
    r = 5
    txt(os_.cell(r, 1), "ENXOVAL (todas as unidades)", True, 11, CREME, DEST); os_.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8); r += 1
    cab(os_, r, ["Item", "Peças por unidade", "Jogos em rotação", "Qtd por unidade", "Preço unitário (R$)", "Total por unidade (R$)", "Nº de unidades", "Total do projeto (R$)"]); r += 1
    ini = r
    for item, pcs, jogos, preco in OSE_ENXOVAL:
        txt(os_.cell(r, 1), item); ent(os_.cell(r, 2), pcs, NUM); ent(os_.cell(r, 3), jogos, NUM); calc(os_.cell(r, 4), f"=B{r}*C{r}", NUM)
        ent(os_.cell(r, 5), preco if exemplo else None, BRL); calc(os_.cell(r, 6), f"=D{r}*E{r}", BRL); calc(os_.cell(r, 7), "=Premissas!$B$12"); calc(os_.cell(r, 8), f"=F{r}*G{r}", BRL); r += 1
    txt(os_.cell(r, 1), "Total de enxoval", True, fill=GRUPO); calc(os_.cell(r, 6), f"=SUM(F{ini}:F{r-1})", BRL, True); calc(os_.cell(r, 8), f"=SUM(H{ini}:H{r-1})", BRL, True)
    for c in (2, 3, 4, 5, 7): txt(os_.cell(r, c), "", fill=GRUPO)
    OSE_ENX = (f"'OS&E'!F{r}", f"'OS&E'!H{r}"); r += 2
    txt(os_.cell(r, 1), "CONSUMÍVEIS · ESTOQUE DE ABERTURA (todas as unidades)", True, 11, CREME, DEST); os_.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8); r += 1
    cab(os_, r, ["Item", "", "", "Qtd inicial por unidade", "Preço unitário (R$)", "Total por unidade (R$)", "Nº de unidades", "Total do projeto (R$)"]); r += 1
    ini = r
    for item, q, preco in OSE_CONSUMO:
        txt(os_.cell(r, 1), item); txt(os_.cell(r, 2), ""); txt(os_.cell(r, 3), ""); ent(os_.cell(r, 4), q, NUM); ent(os_.cell(r, 5), preco if exemplo else None, BRL)
        calc(os_.cell(r, 6), f"=D{r}*E{r}", BRL); calc(os_.cell(r, 7), "=Premissas!$B$12"); calc(os_.cell(r, 8), f"=F{r}*G{r}", BRL); r += 1
    txt(os_.cell(r, 1), "Total de consumíveis", True, fill=GRUPO); calc(os_.cell(r, 6), f"=SUM(F{ini}:F{r-1})", BRL, True); calc(os_.cell(r, 8), f"=SUM(H{ini}:H{r-1})", BRL, True)
    for c in (2, 3, 4, 5, 7): txt(os_.cell(r, c), "", fill=GRUPO)
    OSE_CON = (f"'OS&E'!F{r}", f"'OS&E'!H{r}"); r += 2
    txt(os_.cell(r, 1), "UTENSÍLIOS DE COZINHA (chalés e bolhas com cozinha)", True, 11, CREME, DEST); os_.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8); r += 1
    cab(os_, r, ["Item", "", "", "Qtd por unidade", "Preço unitário (R$)", "Total por unidade (R$)", "Nº de unidades com cozinha", "Total do projeto (R$)"]); r += 1
    ini = r
    for item, q, preco in OSE_COZINHA:
        txt(os_.cell(r, 1), item); txt(os_.cell(r, 2), ""); txt(os_.cell(r, 3), ""); ent(os_.cell(r, 4), q, NUM); ent(os_.cell(r, 5), preco if exemplo else None, BRL)
        calc(os_.cell(r, 6), f"=D{r}*E{r}", BRL); calc(os_.cell(r, 7), "=Premissas!$B$10+Premissas!$B$11"); calc(os_.cell(r, 8), f"=F{r}*G{r}", BRL); r += 1
    txt(os_.cell(r, 1), "Total de utensílios", True, fill=GRUPO); calc(os_.cell(r, 6), f"=SUM(F{ini}:F{r-1})", BRL, True); calc(os_.cell(r, 8), f"=SUM(H{ini}:H{r-1})", BRL, True)
    for c in (2, 3, 4, 5, 7): txt(os_.cell(r, c), "", fill=GRUPO)
    OSE_COZ = (f"'OS&E'!F{r}", f"'OS&E'!H{r}"); r += 2
    txt(os_.cell(r, 1), "ITENS DE OPERAÇÃO DO PROJETO (uma vez, para a hospedagem inteira)", True, 11, CREME, DEST); os_.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8); r += 1
    cab(os_, r, ["Item", "", "", "Quantidade", "Preço unitário (R$)", "", "", "Total do projeto (R$)"]); r += 1
    ini = r
    for item, q, preco in OSE_PROJETO:
        txt(os_.cell(r, 1), item); txt(os_.cell(r, 2), ""); txt(os_.cell(r, 3), ""); ent(os_.cell(r, 4), q, NUM)
        if "10% do total" in item: calc(os_.cell(r, 5), f"=0.1*{OSE_ENX[1]}", BRL)
        else: ent(os_.cell(r, 5), preco if exemplo else None, BRL)
        txt(os_.cell(r, 6), ""); txt(os_.cell(r, 7), ""); calc(os_.cell(r, 8), f"=D{r}*E{r}", BRL); r += 1
    txt(os_.cell(r, 1), "Total de itens de operação", True, fill=GRUPO); calc(os_.cell(r, 8), f"=SUM(H{ini}:H{r-1})", BRL, True)
    for c in range(2, 8): txt(os_.cell(r, c), "", fill=GRUPO)
    OSE_PRJ = f"'OS&E'!H{r}"; r += 2
    txt(os_.cell(r, 1), "TOTAL OS&E DO PROJETO", True, 11, fill=GRUPO); calc(os_.cell(r, 8), f"={OSE_ENX[1]}+{OSE_CON[1]}+{OSE_COZ[1]}+{OSE_PRJ}", BRL, True)
    for c in range(2, 8): txt(os_.cell(r, c), "", fill=GRUPO)
    OSE_TOTAL = f"'OS&E'!H{r}"

    # ---------- Resumo ----------
    rs = wb.create_sheet("Resumo"); titulo(rs, "Resumo do investimento de abertura (CAPEX)", "Copie os valores em destaque na Planilha 2 · Estudo de Massas e Viabilidade.")
    larguras(rs, (46, 20, 14, 44))
    cab(rs, 5, ["Bloco", "Valor (R$)", "% do total", "O que é"])
    blocos = [("Projetos, licenças e infraestrutura", f"={INF_TOTAL}", "Tudo o que o terreno recebe antes das unidades, mais áreas comuns e gestão da obra (aba Infraestrutura)."),
              ("Construção das unidades", "=Premissas!H12", "Área coberta e deck de todas as unidades (aba Premissas)."),
              ("FF&E · mobília e equipamentos", "=" + "+".join(v[1] for v in FFE_TOT.values()), "O que vai dentro das unidades e não se consome (aba FF&E)."),
              ("OS&E · enxoval, consumíveis e operação", f"={OSE_TOTAL}", "Enxoval, amenities, louça e itens de operação (aba OS&E).")]
    for i, (n, f, d) in enumerate(blocos):
        r = 6 + i; txt(rs.cell(r, 1), n); calc(rs.cell(r, 2), f, BRL); calc(rs.cell(r, 3), f"=IF($B$12=0,0,B{r}/$B$12)", PCT); txt(rs.cell(r, 4), d, sz=9, col=CINZA, i=True)
    txt(rs["A10"], "Subtotal", True, fill=GRUPO); calc(rs["B10"], "=SUM(B6:B9)", BRL, True); txt(rs["C10"], "", fill=GRUPO); txt(rs["D10"], "", fill=GRUPO)
    txt(rs["A11"], "Contingência (aba Premissas)"); calc(rs["B11"], "=B10*Premissas!B15", BRL); calc(rs["C11"], "=IF($B$12=0,0,B11/$B$12)", PCT); txt(rs["D11"], "Reserva para imprevistos. Nunca zere.", sz=9, col=CINZA, i=True)
    txt(rs["A12"], "TOTAL DO INVESTIMENTO DE ABERTURA (CAPEX)", True, 11, CREME, DEST); calc(rs["B12"], "=B10+B11", BRL, True); txt(rs["C12"], "", fill=DEST); txt(rs["D12"], "Copie na Planilha 2, aba Investimento.", True, 9, fill=DEST)
    cab(rs, 14, ["Indicador", "Valor", "", "Leitura"])
    txt(rs["A15"], "Nº de unidades"); calc(rs["B15"], "=Premissas!B12", None); txt(rs["D15"], "", sz=9)
    txt(rs["A16"], "Custo médio por unidade pronta (CAPEX ÷ unidades)"); calc(rs["B16"], "=IF(B15=0,0,B12/B15)", BRL); txt(rs["D16"], "Inclui a parte proporcional da infraestrutura e das áreas comuns.", sz=9, col=CINZA, i=True)
    txt(rs["A17"], "Área construída total (m²)"); calc(rs["B17"], "=Premissas!B16", M2)
    txt(rs["A18"], "Custo por m² construído (CAPEX ÷ área)"); calc(rs["B18"], "=IF(B17=0,0,B12/B17)", BRL); txt(rs["D18"], "Compare com o CUB da sua região e com outros projetos.", sz=9, col=CINZA, i=True)
    txt(rs["A19"], "Infraestrutura e áreas comuns por unidade"); calc(rs["B19"], "=IF(B15=0,0,B6/B15)", BRL); txt(rs["D19"], "Quanto mais unidades, menor esse peso por unidade. É o argumento para crescer em fases.", sz=9, col=CINZA, i=True)
    cab(rs, 21, ["Custo por unidade, por tipologia", "Construção", "FF&E + OS&E por unidade", "Chave na mão (sem infraestrutura)"])
    rs.column_dimensions["C"].width = 22
    for i, tp in enumerate(TIPOS):
        r = 22 + i; txt(rs.cell(r, 1), tp); calc(rs.cell(r, 2), f"=Premissas!G{9+i}", BRL)
        coz = f"+{OSE_COZ[0]}" if i > 0 else ""
        calc(rs.cell(r, 3), f"={FFE_TOT[tp][0]}+{OSE_ENX[0]}+{OSE_CON[0]}{coz}", BRL); calc(rs.cell(r, 4), f"=B{r}+C{r}", BRL, True)
    txt(rs["A26"], "Chave na mão = construção da unidade + o que vai dentro dela. Some a linha 19 para ter o custo completo por unidade.", sz=9, col=CINZA, i=True); rs.merge_cells("A26:D26")
    txt(rs["A28"], RODAPE, sz=9, col=CINZA, i=True); rs.merge_cells("A28:D28")
    for ws in wb.worksheets: ws.freeze_panes = None
    return wb

# ===================================================================================
# PLANILHA 2 · ESTUDO DE MASSAS E VIABILIDADE
# ===================================================================================
COMUNS = [("Recepção e apoio", 40), ("Cozinha, café da manhã ou restaurante", 30), ("Lavanderia e depósito", 25), ("Administração e vestiário da equipe", 15),
          ("Circulação coberta e varandas comuns", 30), ("Piscina, ofurô ou spa (área molhada)", 60), ("Deck de convivência e fogueira", 60)]
FIXOS = [("Equipe (recepção, camareira, manutenção, encargos)", 16000), ("Energia, água e gás", 3500), ("Internet, software de reservas e telefonia", 500),
         ("Manutenção e jardinagem", 1200), ("Marketing e fotos", 1500), ("Contabilidade, seguros e taxas", 900), ("Outros fixos", 500)]
CEN = ["Conservador", "Base", "Otimista"]

def planilha_viabilidade(exemplo):
    wb = Workbook()
    comece(wb, "CLUB ZION COLLECTION · TRILHA DE DESENVOLVIMENTO · PLANILHA 2", "Estudo de Massas e Viabilidade", [
        ("Do masterplan ao número: metragens, áreas vendáveis, custo por m², modelo de venda (VGV, margem, ROI) e modelo de renda (diária, ocupação, resultado operacional, payback, TIR e VPL), em três cenários.", T(11, c="2D352A")),
        ("Use depois da Planilha 1 · Orçamento de Abertura e do Pilar 5 (Masterplan).", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 6 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Massas: digite a área do terreno, o número de unidades de cada tipologia com as suas metragens, e as áreas comuns. A planilha calcula a área construída, a área vendável (privativa), o índice de aproveitamento e a ocupação do terreno.", None),
        ("2. Aba Investimento: cole o CAPEX da Planilha 1, o valor do terreno (zero se já é seu e não entra na conta) e o capital de giro. Sai o custo por m² e por unidade.", None),
        ("3. Aba Modelo de venda: se a ideia é vender as unidades (chalés, cotas, lotes com projeto), digite o preço de venda. Sai o VGV, o resultado, a margem e o ROI da venda.", None),
        ("4. Aba Modelo de renda: se a ideia é operar, digite diária média, ocupação e custos em três cenários. Sai o RevPAR, a receita, o resultado operacional, a margem, o payback, a TIR e o VPL em 10 anos, e a ocupação de equilíbrio.", None),
        ("5. Aba Comparativo: venda e renda lado a lado, com uma leitura automática do que os números estão dizendo.", None),
        ("6. Aba Glossário: o que é cada sigla (VGV, ROI, RevPAR, NOI, TIR, VPL, payback, cap rate).", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).   Dourado = resultado principal.", None),
        ("", None),
        ("O QUE ESTA PLANILHA NÃO FAZ", T(12, True, MUSGO)),
        ("Não sabe a demanda da sua região: diária e ocupação são premissas suas, tiradas da Ficha do Mercado (Pilar 2). Não substitui um estudo de viabilidade assinado por profissional, nem a análise de um banco ou investidor. Serve para você entender onde está indo e conversar com números.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. TIR e VPL usam as funções IRR e NPV, que existem nos três.", T(10, c=CINZA, i=True)),
        (RODAPE, T(9, c=CINZA, i=True)),
    ], exemplo)

    # ---------- Massas ----------
    ms = wb.create_sheet("Massas"); titulo(ms, "Estudo de massas", "Quanto se constrói, quanto se vende e quanto o terreno comporta.")
    larguras(ms, (44, 16, 20, 20, 20, 20))
    txt(ms["A5"], "Área total do terreno (m²)"); ent(ms["B5"], 20000 if exemplo else None, M2)
    txt(ms["A6"], "Área que a lei permite construir (taxa de ocupação máxima, %)"); ent(ms["B6"], 0.3 if exemplo else None, PCT)
    txt(ms["C6"], "Consulte o zoneamento (Pilar 1). Em área rural ou de preservação pode ser bem menor.", sz=9, col=CINZA, i=True); ms.merge_cells("C6:F6")
    cab(ms, 8, ["Tipologia", "Nº de unidades", "Área coberta por unidade (m²)", "Deck ou varanda por unidade (m²)", "Área coberta total (m²)", "Área de deck total (m²)"], 50)
    exm = [(4, 28, 8), (3, 45, 20), (3, 28, 25)]
    for i, tp in enumerate(TIPOS):
        r = 9 + i; txt(ms.cell(r, 1), tp, True)
        for j in range(3): ent(ms.cell(r, 2 + j), exm[i][j] if exemplo else None, None if j == 0 else M2)
        calc(ms.cell(r, 5), f"=B{r}*C{r}", M2); calc(ms.cell(r, 6), f"=B{r}*D{r}", M2)
    txt(ms["A12"], "Total das unidades", True, fill=GRUPO); calc(ms["B12"], "=SUM(B9:B11)", None, True)
    for c in ("C12", "D12"): txt(ms[c], "", fill=GRUPO)
    calc(ms["E12"], "=SUM(E9:E11)", M2, True); calc(ms["F12"], "=SUM(F9:F11)", M2, True)
    cab(ms, 14, ["Áreas comuns e de apoio", "Área (m²)", "Coberta? (sim/não)", "Dica"], 32)
    for i, (n, a) in enumerate(COMUNS):
        r = 15 + i; txt(ms.cell(r, 1), n); ent(ms.cell(r, 2), a if exemplo else None, M2); ent(ms.cell(r, 3), "não" if i >= 5 else "sim")
        txt(ms.cell(r, 4), "Comece pequeno; áreas comuns crescem em fases." if i == 0 else "", sz=9, col=CINZA, i=True)
    lista(ms, "C15:C21", ["sim", "não"])
    txt(ms["A22"], "Estacionamento, vias e paisagismo não entram aqui: são infraestrutura (Planilha 1) e não contam como área construída.", sz=9, col=CINZA, i=True); ms.merge_cells("A22:F22")
    txt(ms["A23"], "Total de áreas comuns", True, fill=GRUPO); calc(ms["B23"], "=SUM(B15:B21)", M2, True); txt(ms["C23"], "", fill=GRUPO); txt(ms["D23"], "", fill=GRUPO)
    txt(ms["A24"], "Áreas comuns cobertas"); calc(ms["B24"], '=SUMIF(C15:C21,"sim",B15:B21)', M2)
    cab(ms, 26, ["Resultado do estudo de massas", "Valor", "", "Leitura"], 30)
    res = [("Área privativa total (vendável), m²", "=E12", M2, "É o que o hóspede ou o comprador paga. Quanto maior a parte privativa, melhor o aproveitamento."),
           ("Área de deck e varandas, m²", "=F12", M2, ""),
           ("Área comum total, m²", "=B23", M2, ""),
           ("Área construída total (coberta + deck + comuns), m²", "=B27+B28+B29", M2, "É a base do custo por m²."),
           ("Área coberta total (unidades + comuns cobertas), m²", "=E12+B24", M2, "Em geral é o que a prefeitura conta como construído."),
           ("Índice de aproveitamento (privativa ÷ construída)", "=IF(B30=0,0,B27/B30)", PCT, "Acima de 45% é um bom sinal. Abaixo de 35%, há área comum demais para poucas unidades: dilua com mais unidades ou enxugue as comuns."),
           ("Ocupação do terreno (construída ÷ terreno)", "=IF(B5=0,0,B30/B5)", PCT, "Compare com o limite legal digitado em B6."),
           ("Situação diante do limite legal", '=IF(B6=0,"Digite o limite legal em B6",IF(B33<=B6,"Dentro do limite","ACIMA DO LIMITE: reduza unidades ou áreas comuns"))', None, ""),
           ("Área livre e permeável, m²", "=B5-B30", M2, "Natureza preservada é parte do produto."),
           ("m² construído por unidade (construída ÷ unidades)", "=IF(B12=0,0,B30/B12)", NUM, "")]
    for i, (n, f, fmt, d) in enumerate(res):
        r = 27 + i; txt(ms.cell(r, 1), n); calc(ms.cell(r, 2), f, fmt, i in (0, 3)); txt(ms.cell(r, 4), d, sz=9, col=CINZA, i=True)
    txt(ms["A38"], RODAPE, sz=9, col=CINZA, i=True); ms.merge_cells("A38:F38")

    # ---------- Investimento ----------
    inv = wb.create_sheet("Investimento"); titulo(inv, "Investimento total", "Cole aqui o CAPEX da Planilha 1 (aba Resumo, linha TOTAL).")
    larguras(inv, (50, 20, 50))
    linhas = [("CAPEX de abertura (Planilha 1 · Resumo)", 3535000, "Infraestrutura, construção, FF&E, OS&E e contingência."),
              ("Valor do terreno (zero se já é seu e não entra na conta)", 0, "Se quiser medir o retorno sobre o terreno também, digite o valor de mercado dele."),
              ("Capital de giro inicial (meses de custo fixo)", 3, "Quantos meses de custo fixo você precisa ter em caixa até a operação se pagar. 3 é o mínimo prudente."),
              ("Custo fixo mensal (vem da aba Modelo de renda, cenário Base)", None, "")]
    for i, (n, v, d) in enumerate(linhas):
        r = 5 + i; txt(inv.cell(r, 1), n)
        if i == 3: calc(inv.cell(r, 2), "='Modelo de renda'!C25", BRL)
        else: ent(inv.cell(r, 2), v if exemplo else None, NUM if i == 2 else BRL)
        txt(inv.cell(r, 3), d, sz=9, col=CINZA, i=True)
    txt(inv["A9"], "Capital de giro (R$)"); calc(inv["B9"], "=B7*B8", BRL)
    txt(inv["A10"], "TOTAL INVESTIDO", True, 11, CREME, DEST); calc(inv["B10"], "=B5+B6+B9", BRL, True); txt(inv["C10"], "", fill=DEST)
    cab(inv, 12, ["Indicador", "Valor", "Leitura"])
    txt(inv["A13"], "Custo por m² construído (CAPEX ÷ área construída)"); calc(inv["B13"], "=IF(Massas!B30=0,0,B5/Massas!B30)", BRL); txt(inv["C13"], "Compare com o CUB da região. Muito acima: revise o padrão ou o orçamento.", sz=9, col=CINZA, i=True)
    txt(inv["A14"], "Custo por m² privativo (CAPEX ÷ área vendável)"); calc(inv["B14"], "=IF(Massas!B27=0,0,B5/Massas!B27)", BRL); txt(inv["C14"], "É o custo que o preço de venda por m² precisa cobrir.", sz=9, col=CINZA, i=True)
    txt(inv["A15"], "Investimento por unidade (total ÷ unidades)"); calc(inv["B15"], "=IF(Massas!B12=0,0,B10/Massas!B12)", BRL); txt(inv["C15"], "Quanto cada unidade precisa devolver, em venda ou em renda.", sz=9, col=CINZA, i=True)
    txt(inv["A17"], RODAPE, sz=9, col=CINZA, i=True); inv.merge_cells("A17:C17")

    # ---------- Modelo de venda ----------
    mv = wb.create_sheet("Modelo de venda"); titulo(mv, "Modelo de venda", "Para quem vai vender as unidades prontas (chalés, cotas, lotes com projeto). VGV = valor geral de vendas.")
    larguras(mv, (44, 16, 22, 20, 20, 44))
    cab(mv, 5, ["Tipologia", "Nº de unidades", "Preço de venda por unidade (R$)", "Preço por m² privativo (R$)", "VGV por tipologia (R$)", "Dica"], 44)
    exv = [450000, 750000, 420000]
    for i, tp in enumerate(TIPOS):
        r = 6 + i; txt(mv.cell(r, 1), tp, True); calc(mv.cell(r, 2), f"=Massas!B{9+i}"); ent(mv.cell(r, 3), exv[i] if exemplo else None, BRL)
        calc(mv.cell(r, 4), f"=IF(Massas!C{9+i}=0,0,C{r}/Massas!C{9+i})", BRL); calc(mv.cell(r, 5), f"=B{r}*C{r}", BRL)
        txt(mv.cell(r, 6), "Pesquise unidades parecidas à venda na região (Pilar 2)." if i == 0 else "", sz=9, col=CINZA, i=True)
    txt(mv["A9"], "VGV total", True, fill=GRUPO); calc(mv["E9"], "=SUM(E6:E8)", BRL, True)
    for c in ("B9", "C9", "D9", "F9"): txt(mv[c], "", fill=GRUPO)
    cab(mv, 11, ["Custos da venda", "Valor", "", "", "", "Dica"], 30)
    txt(mv["A12"], "Investimento total (aba Investimento)"); calc(mv["B12"], "=Investimento!B10", BRL)
    txt(mv["A13"], "Comissão de vendas (% do VGV)"); ent(mv["B13"], 0.06 if exemplo else None, PCT); txt(mv["F13"], "Corretor ou imobiliária: 5% a 6% é comum.", sz=9, col=CINZA, i=True)
    txt(mv["A14"], "Impostos sobre a venda (% do VGV)"); ent(mv["B14"], 0.06 if exemplo else None, PCT); txt(mv["F14"], "Depende do regime da empresa. Confirme com o contador.", sz=9, col=CINZA, i=True)
    txt(mv["A15"], "Marketing e lançamento (% do VGV)"); ent(mv["B15"], 0.02 if exemplo else None, PCT)
    txt(mv["A16"], "Prazo estimado para vender tudo (meses)"); ent(mv["B16"], 18 if exemplo else None, NUM); txt(mv["F16"], "Quanto mais tempo, mais custo de carregamento e menos retorno ao ano.", sz=9, col=CINZA, i=True)
    txt(mv["A17"], "Custos da venda (R$)"); calc(mv["B17"], "=E9*(B13+B14+B15)", BRL)
    cab(mv, 19, ["Resultado da venda", "Valor", "", "", "", "Leitura"], 30)
    txt(mv["A20"], "Resultado (VGV − investimento − custos da venda)"); calc(mv["B20"], "=E9-B12-B17", BRL, True)
    txt(mv["A21"], "Margem sobre o VGV"); calc(mv["B21"], "=IF(E9=0,0,B20/E9)", PCT); txt(mv["F21"], "Abaixo de 15%, qualquer imprevisto come o resultado.", sz=9, col=CINZA, i=True)
    txt(mv["A22"], "ROI da venda (resultado ÷ investimento)"); calc(mv["B22"], "=IF(B12=0,0,B20/B12)", PCT)
    txt(mv["A23"], "ROI ao ano (considerando o prazo de venda)"); calc(mv["B23"], "=IF(OR(B12=0,B16=0),0,(1+B22)^(12/B16)-1)", PCT); txt(mv["F23"], "Compare com o que o dinheiro renderia parado.", sz=9, col=CINZA, i=True)
    txt(mv["A24"], "Margem alvo (para calcular o preço mínimo)"); ent(mv["B24"], 0.25 if exemplo else None, PCT)
    txt(mv["A25"], "VGV mínimo para a margem alvo"); calc(mv["B25"], "=IF((1-B13-B14-B15-B24)<=0,0,B12/(1-B13-B14-B15-B24))", BRL)
    txt(mv["A26"], "Preço médio mínimo por unidade para a margem alvo"); calc(mv["B26"], "=IF(Massas!B12=0,0,B25/Massas!B12)", BRL, True); txt(mv["F26"], "Se o mercado não paga esse preço, o modelo de venda não fecha: revise o custo ou vá para o modelo de renda.", sz=9, col=CINZA, i=True)
    txt(mv["A27"], "Leitura automática"); calc(mv["B27"], '=IF(E9=0,"Digite os preços de venda",IF(B21>=B24,"Margem acima da meta",IF(B21>0,"Margem positiva, mas abaixo da meta","Resultado negativo: o preço não cobre o investimento")))', None, True); mv.merge_cells("B27:E27")
    txt(mv["A29"], RODAPE, sz=9, col=CINZA, i=True); mv.merge_cells("A29:F29")

    # ---------- Modelo de renda ----------
    mr = wb.create_sheet("Modelo de renda"); titulo(mr, "Modelo de renda · operação hoteleira", "Três cenários lado a lado. Diária e ocupação vêm da Ficha do Mercado (Pilar 2).")
    larguras(mr, (48, 18, 18, 18, 46))
    cab(mr, 5, ["Premissas de receita", *CEN, "Dica"], 30)
    exr = {"d": (550, 650, 750), "o": (0.40, 0.50, 0.60), "x": (0.08, 0.10, 0.12), "c": (0.15, 0.15, 0.15), "v": (90, 90, 90), "t": (0.08, 0.08, 0.08), "a": (0, 0, 0), "g": (0.05, 0.05, 0.05)}
    prem = [("Nº de unidades", None, None, "=Massas!$B$12"), ("Diária média (R$)", "d", BRL, None), ("Ocupação média no ano", "o", PCT, None), ("Dias no ano", None, None, 365),
            ("Receita extra por diária vendida (café, experiências, loja), % da diária", "x", PCT, None), ("Comissão de canais e intermediários (% da hospedagem)", "c", PCT, None),
            ("Custo variável por diária vendida (limpeza, enxoval, amenities, café), R$", "v", BRL, None), ("Impostos sobre a receita (%)", "t", PCT, None),
            ("Taxa de administração ou gestão (% da receita líquida; zero se você opera)", "a", PCT, None), ("Crescimento anual da receita (anos 2 a 10)", "g", PCT, None)]
    dicas = ["", "Média do ano, não a de alta temporada.", "Comece conservador: hospedagem nova leva 12 a 24 meses para estabilizar.", "", "Café da manhã, experiências, loja.",
             "Plataformas de reserva cobram de 12% a 18%. Venda direta reduz isso.", "Tudo o que só acontece quando tem hóspede.", "Confirme o regime com o contador.", "Se uma empresa opera por você.", "Reajuste de diária e maturação."]
    for i, (n, k, fmt, fixo) in enumerate(prem):
        r = 6 + i; txt(mr.cell(r, 1), n)
        for j in range(3):
            c = mr.cell(r, 2 + j)
            if fixo is not None and isinstance(fixo, str): calc(c, fixo)
            elif fixo is not None: ent(c, fixo, None)
            else: ent(c, exr[k][j] if exemplo else None, fmt)
        txt(mr.cell(r, 5), dicas[i], sz=9, col=CINZA, i=True)
    cab(mr, 17, ["Custos fixos mensais (iguais nos 3 cenários)", "Valor mensal (R$)", "", "", "Dica"], 30)
    for i, (n, v) in enumerate(FIXOS):
        r = 18 + i; txt(mr.cell(r, 1), n); ent(mr.cell(r, 2), v if exemplo else None, BRL)
        txt(mr.cell(r, 5), "Dimensione pela quantidade de unidades e pelo padrão de serviço." if i == 0 else "", sz=9, col=CINZA, i=True)
    txt(mr["A25"], "Custo fixo mensal total", True, fill=GRUPO); calc(mr["C25"], "=SUM(B18:B24)", BRL, True); txt(mr["B25"], "", fill=GRUPO); txt(mr["D25"], "", fill=GRUPO)
    txt(mr["A26"], "Custo fixo anual"); calc(mr["C26"], "=C25*12", BRL)
    cab(mr, 28, ["Resultado anual", *CEN, "Leitura"], 30)
    L = ["B", "C", "D"]
    res = [("Diárias disponíveis (unidades × dias)", "={c}6*{c}9", NUM, ""),
           ("Diárias vendidas (× ocupação)", "={c}29*{c}8", NUM, ""),
           ("RevPAR (receita por unidade disponível por dia)", "={c}7*{c}8", BRL, "O indicador que o setor usa para comparar hospedagens."),
           ("Receita de hospedagem", "={c}30*{c}7", BRL, ""),
           ("Receita extra", "={c}32*{c}10", BRL, ""),
           ("Receita bruta", "={c}32+{c}33", BRL, ""),
           ("(−) Comissões de canais", "={c}32*{c}11", BRL, ""),
           ("(−) Impostos", "={c}34*{c}13", BRL, ""),
           ("Receita líquida", "={c}34-{c}35-{c}36", BRL, ""),
           ("(−) Custos variáveis", "={c}30*{c}12", BRL, ""),
           ("(−) Custos fixos", "=$C$26", BRL, ""),
           ("(−) Taxa de administração", "={c}37*{c}14", BRL, ""),
           ("RESULTADO OPERACIONAL ANUAL (NOI)", "={c}37-{c}38-{c}39-{c}40", BRL, "O que sobra para pagar o investimento e remunerar você. Antes de depreciação, juros e imposto de renda."),
           ("Resultado operacional mensal", "={c}41/12", BRL, ""),
           ("Margem operacional (NOI ÷ receita bruta)", "=IF({c}34=0,0,{c}41/{c}34)", PCT, "Hospedagem de natureza bem operada fica entre 30% e 45%."),
           ("Ocupação de equilíbrio (onde o resultado é zero)", "=IF(({c}29*({c}7*(1-{c}11-{c}13)*(1-{c}14)+{c}7*{c}10*(1-{c}13)*(1-{c}14)-{c}12))<=0,0,$C$26/({c}29*({c}7*(1-{c}11-{c}13)*(1-{c}14)+{c}7*{c}10*(1-{c}13)*(1-{c}14)-{c}12)))", PCT, "Abaixo dessa ocupação, a operação dá prejuízo. Compare com a sua premissa de ocupação."),
           ("Investimento total (aba Investimento)", "=Investimento!$B$10", BRL, ""),
           ("ROI anual (NOI ÷ investimento)", "=IF({c}45=0,0,{c}41/{c}45)", PCT, ""),
           ("Payback simples (anos para devolver o investimento)", "=IF({c}41<=0,\"não paga\",{c}45/{c}41)", NUM, "Acima de 8 anos pede revisão de diária, ocupação ou investimento.")]
    for i, (n, f, fmt, d) in enumerate(res):
        r = 29 + i; txt(mr.cell(r, 1), n, i == 12)
        for j, c in enumerate(L): calc(mr.cell(r, 2 + j), f.format(c=c), fmt, i == 12)
        if i == 12:
            for j in range(4): mr.cell(r, 1 + j).fill = DEST
        txt(mr.cell(r, 5), d, sz=9, col=CINZA, i=True)
    # fluxo de 10 anos
    cab(mr, 49, ["Fluxo de caixa em 10 anos", *CEN, "Dica"], 30)
    txt(mr["A50"], "Taxa de desconto para o VPL (custo do dinheiro ou retorno mínimo que você exige)"); ent(mr["B50"], 0.12 if exemplo else None, PCT); calc(mr["C50"], "=B50", PCT); calc(mr["D50"], "=B50", PCT)
    txt(mr["E50"], "Selic, CDI ou a rentabilidade que você teria sem risco. 10% a 15% é comum.", sz=9, col=CINZA, i=True)
    txt(mr["A51"], "Ano 0 · investimento");
    for j, c in enumerate(L): calc(mr.cell(51, 2 + j), f"=-{c}45", BRL)
    for ano in range(1, 11):
        r = 51 + ano; txt(mr.cell(r, 1), f"Ano {ano}")
        for j, c in enumerate(L): calc(mr.cell(r, 2 + j), f"={c}41*(1+{c}15)^{ano-1}", BRL)
    txt(mr["A62"], "TIR em 10 anos (taxa interna de retorno)", True)
    for j, c in enumerate(L): calc(mr.cell(62, 2 + j), f'=IFERROR(IRR({c}51:{c}61),"não calcula")', PCT, True)
    txt(mr["E62"], "Se a TIR é maior que a taxa de desconto, o projeto rende mais do que a alternativa.", sz=9, col=CINZA, i=True)
    txt(mr["A63"], "VPL em 10 anos (valor presente líquido)", True)
    for j, c in enumerate(L): calc(mr.cell(63, 2 + j), f"=NPV({c}50,{c}52:{c}61)+{c}51", BRL, True)
    txt(mr["E63"], "Positivo: o projeto vale mais do que custa, à taxa escolhida. Negativo: não.", sz=9, col=CINZA, i=True)
    txt(mr["A64"], "Valor do negócio em operação (NOI ÷ cap rate)")
    for j, c in enumerate(L): calc(mr.cell(64, 2 + j), f"=IF($B$65=0,0,{c}41/$B$65)", BRL)
    txt(mr["E64"], "É como o mercado precifica uma hospedagem pronta e operando. Serve para o modelo de venda do negócio.", sz=9, col=CINZA, i=True)
    txt(mr["A65"], "Cap rate (taxa de capitalização do mercado)"); ent(mr["B65"], 0.10 if exemplo else None, PCT)
    txt(mr["E65"], "Entre 8% e 12% para hospedagem independente no Brasil, variando com risco e localização.", sz=9, col=CINZA, i=True)
    txt(mr["A66"], "Leitura automática (cenário Base)")
    calc(mr["B66"], '=IF(C41<=0,"Resultado operacional negativo: revise diária, ocupação ou custos",IF(C47>8,"Paga, mas o payback passa de 8 anos",IF(C62="não calcula","Confira as premissas",IF(C62>C50,"Rende acima da taxa de desconto","Rende abaixo da taxa de desconto"))))', None, True); mr.merge_cells("B66:D66")
    for rr in (62, 63): mr.conditional_formatting.add(f"B{rr}:D{rr}", CellIsRule(operator="lessThan", formula=["0"], fill=PatternFill("solid", fgColor="F4C7C3")))
    txt(mr["A68"], RODAPE, sz=9, col=CINZA, i=True); mr.merge_cells("A68:E68")

    # ---------- Comparativo ----------
    cp = wb.create_sheet("Comparativo"); titulo(cp, "Venda ou renda? Os dois modelos lado a lado", "Cenário Base para a renda. A leitura é automática.")
    larguras(cp, (44, 22, 22, 46))
    cab(cp, 5, ["Indicador", "Modelo de venda", "Modelo de renda (Base)", "Leitura"], 30)
    comp = [("Investimento total", "=Investimento!B10", "=Investimento!B10", BRL, ""),
            ("Receita no 1º ciclo (VGV ou receita bruta anual)", "='Modelo de venda'!E9", "='Modelo de renda'!C34", BRL, "Venda é uma vez; renda repete todo ano."),
            ("Resultado (venda) ou NOI anual (renda)", "='Modelo de venda'!B20", "='Modelo de renda'!C41", BRL, ""),
            ("Margem", "='Modelo de venda'!B21", "='Modelo de renda'!C43", PCT, ""),
            ("ROI (venda) e ROI anual (renda)", "='Modelo de venda'!B22", "='Modelo de renda'!C46", PCT, ""),
            ("Prazo: meses para vender ou anos de payback", "='Modelo de venda'!B16", "='Modelo de renda'!C47", NUM, ""),
            ("TIR em 10 anos (renda)", "", "='Modelo de renda'!C62", PCT, ""),
            ("VPL em 10 anos (renda)", "", "='Modelo de renda'!C63", BRL, ""),
            ("Valor do negócio pronto e operando (renda)", "", "='Modelo de renda'!C64", BRL, "Terceiro caminho: operar e vender o negócio pronto, pelo cap rate.")]
    for i, (n, fv, fr, fmt, d) in enumerate(comp):
        r = 6 + i; txt(cp.cell(r, 1), n); calc(cp.cell(r, 2), fv if fv else '=""', fmt); calc(cp.cell(r, 3), fr, fmt); txt(cp.cell(r, 4), d, sz=9, col=CINZA, i=True)
    txt(cp["A16"], "Leitura automática", True, fill=GRUPO)
    calc(cp["B16"], '=IF(AND(\'Modelo de venda\'!E9=0,\'Modelo de renda\'!C34=0),"Preencha os dois modelos",IF(\'Modelo de venda\'!E9=0,"Só o modelo de renda foi preenchido",IF(\'Modelo de renda\'!C34=0,"Só o modelo de venda foi preenchido",IF(\'Modelo de venda\'!B21>=0.25,"A venda fecha com margem forte",IF(\'Modelo de renda\'!C47<=8,"A renda paga o investimento em prazo razoável; a venda tem margem apertada","Nenhum dos dois fecha bem: revise custo, preço, diária ou ocupação")))))', None, True)
    cp.merge_cells("B16:D16")
    txt(cp["A18"], "O que a Zion olha primeiro", True, 12, MUSGO); cp.merge_cells("A18:D18")
    for i, t in enumerate(["1. O índice de aproveitamento (Massas): área comum demais encarece e não vende.",
                           "2. O custo por m² privativo contra o preço por m² do mercado (Investimento × Modelo de venda).",
                           "3. A ocupação de equilíbrio contra a ocupação realista da região (Modelo de renda).",
                           "4. O payback e a TIR no cenário conservador, não no otimista.",
                           "5. Começar menor e crescer em fases: a infraestrutura dilui com mais unidades (Planilha 1, Resumo)."]):
        txt(cp.cell(19 + i, 1), t); cp.merge_cells(start_row=19 + i, start_column=1, end_row=19 + i, end_column=4)
    txt(cp["A25"], RODAPE, sz=9, col=CINZA, i=True); cp.merge_cells("A25:D25")

    # ---------- Glossário ----------
    gl = wb.create_sheet("Glossário"); titulo(gl, "Glossário", "As siglas que aparecem na conversa com investidor, banco e sócio.")
    larguras(gl, (22, 100))
    G = [("CAPEX", "Investimento de abertura: tudo o que você gasta antes da primeira diária (infraestrutura, construção, FF&E, OS&E, contingência)."),
         ("FF&E", "Furniture, Fixtures & Equipment: mobília, equipamentos e decoração que ficam na unidade e não se consomem."),
         ("OS&E", "Operating Supplies & Equipment: enxoval, louça, amenities e itens de operação que se repõem."),
         ("Estudo de massas", "Quanto se constrói, onde, e como as áreas se dividem entre privativas (vendáveis) e comuns. Vem do masterplan (Pilar 5)."),
         ("Área privativa ou vendável", "A área da unidade que o hóspede ou o comprador paga. Áreas comuns não se vendem, se diluem."),
         ("Índice de aproveitamento", "Área privativa dividida pela área construída. Mostra se o projeto gasta construção com o que gera receita."),
         ("VGV", "Valor Geral de Vendas: a soma do preço de venda de todas as unidades."),
         ("ROI", "Retorno sobre o investimento: resultado dividido pelo que foi investido."),
         ("RevPAR", "Receita por unidade disponível por dia: diária média × ocupação. O indicador padrão da hotelaria."),
         ("NOI", "Net Operating Income, resultado operacional: receita menos custos de operação, antes de depreciação, juros e imposto de renda."),
         ("Payback", "Anos que o resultado operacional leva para devolver o investimento."),
         ("TIR", "Taxa interna de retorno: a taxa anual que o projeto rende, considerando os fluxos de caixa de 10 anos."),
         ("VPL", "Valor presente líquido: quanto o projeto vale hoje, descontando os fluxos futuros pela taxa que você exige. Positivo é bom."),
         ("Taxa de desconto", "O retorno mínimo que você exige, ou o que o dinheiro renderia em outra aplicação."),
         ("Cap rate", "Taxa de capitalização: NOI dividido pelo valor do negócio. Usada para precificar uma hospedagem em operação."),
         ("Ocupação de equilíbrio", "A ocupação em que a receita cobre exatamente os custos. Abaixo dela, prejuízo."),
         ("Modelo de venda × modelo de renda", "Vender as unidades prontas (resultado de uma vez) ou operar e viver da receita (resultado todo ano). Pilar 4.")]
    cab(gl, 5, ["Termo", "O que é"])
    for i, (a, b) in enumerate(G):
        txt(gl.cell(6 + i, 1), a, True); txt(gl.cell(6 + i, 2), b)
    txt(gl.cell(6 + len(G) + 1, 1), RODAPE, sz=9, col=CINZA, i=True); gl.merge_cells(start_row=6 + len(G) + 1, start_column=1, end_row=6 + len(G) + 1, end_column=2)
    return wb

for exemplo, suf in ((False, "EM-BRANCO"), (True, "EXEMPLO")):
    planilha_orcamento(exemplo).save(OUT / f"Orcamento-de-Abertura-Zion-{suf}.xlsx")
    planilha_viabilidade(exemplo).save(OUT / f"Estudo-de-Massas-e-Viabilidade-Zion-{suf}.xlsx")
print("ok", sorted(p.name for p in OUT.glob("*.xlsx")))

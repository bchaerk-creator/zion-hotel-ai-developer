"""Gera a planilha "Painel do Mês · os cinco números do gestor" (Jornada 2 · Gestão · Marco Zero) em duas versões:
   - Painel-do-Mes-Zion-EM-BRANCO.xlsx
   - Painel-do-Mes-Zion-EXEMPLO.xlsx (dados fictícios, identificados como exemplo)
Uso: python3 -I build_planilha.py <pasta-saida>
Molde: producao/low-ticket/01-diaria-minima/build_planilha.py (amarelo = preenche, verde = calculado)."""
import sys, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, DOURADO, PRETO, CREME = "1B2117", "8B714E", "040605", "FEF5F0"
ENTRADA = PatternFill("solid", fgColor="FFF4C7"); CALC = PatternFill("solid", fgColor="E3EEDF"); CAB = PatternFill("solid", fgColor=MUSGO)
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
BRL = 'R$ #,##0.00;[Red]-R$ #,##0.00'
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)

def faixa(ws, linha, texto, cols=3):
    ws.merge_cells(start_row=linha, start_column=1, end_row=linha, end_column=cols)
    c = ws.cell(linha, 1, texto); c.font = T(11, True, CREME); c.fill = CAB; c.alignment = Alignment(vertical="center", indent=1); ws.row_dimensions[linha].height = 22
def rotulo(ws, l, texto, ajuda=""):
    a = ws.cell(l, 1, texto); a.font = T(11); a.alignment = Alignment(wrap_text=True, vertical="center")
    if ajuda: h = ws.cell(l, 3, ajuda); h.font = T(9, c="5F5F55", i=True); h.alignment = Alignment(wrap_text=True, vertical="center")
def entrada(ws, l, valor=None, fmt=BRL):
    c = ws.cell(l, 2, valor); c.fill = ENTRADA; c.border = borda; c.number_format = fmt; c.font = T(12, True); return c
def calc(ws, l, formula, fmt=BRL, destaque=False):
    c = ws.cell(l, 2, formula); c.fill = CALC; c.border = borda; c.number_format = fmt; c.font = T(14 if destaque else 11, True, MUSGO if destaque else PRETO); return c

SAIDAS = [("Pessoas (salários, diárias, encargos)", 1800), ("Limpeza e lavanderia", 540), ("Energia, água, gás e internet", 620), ("Compras e reposição (café, amenities, enxoval)", 380),
          ("Manutenção e pequenos reparos", 250), ("Taxas de plataformas e cartão", 1040), ("Marketing e anúncios", 150), ("Impostos, contador e taxas fixas", 460), ("Outras saídas", 90)]

def montar(exemplo):
    wb = Workbook()
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False; ws.column_dimensions["A"].width = 100
    linhas = [
        ("ZION HOSPITALITY BUSINESS · JORNADA 2 · GESTÃO · MARCO ZERO", T(10, True, DOURADO)),
        ("Painel do Mês · os cinco números do gestor", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para fechar o mês em uma folha: quanto entrou, quanto sobrou, a ocupação, a diária média e o custo por noite vendida.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS. Use a versão em branco para os seus números." if exemplo else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("", None),
        ("COMO USAR EM 3 PASSOS (cerca de 20 minutos no primeiro mês, 10 nos seguintes)", T(12, True, MUSGO)),
        ("1. Aba Painel: preencha as células amarelas com os números do mês passado: unidades, dias do mês, noites vendidas, o que entrou e o que saiu por categoria. Tire tudo do extrato e das reservas, não da memória.", None),
        ("2. Leia os cinco números em verde. Compare com o mês anterior na aba Histórico (uma linha por mês).", None),
        ("3. Aba Rotina: marque o que você já faz. É a rotina mínima de gestão de uma hospedagem pequena: o que olhar todo dia, toda semana e todo mês.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("O QUE A PLANILHA FAZ E O QUE ELA NÃO FAZ", T(12, True, MUSGO)),
        ("Faz: calcula os cinco números do gestor a partir do que você lança e guarda o histórico mês a mês.", None),
        ("Não faz: não prevê os próximos meses, não conhece os preços da sua região e não substitui o seu contador. \"Quanto sobrou\" não é lucro líquido: não inclui depreciação, imposto de renda nem a sua retirada, salvo se você lançar.", None),
        ("Premissa: receita e saídas contadas no mês em que aconteceram (regime de caixa).", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Material educativo: não garante reservas, ocupação nem resultado.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    p = wb.create_sheet("Painel"); p.sheet_view.showGridLines = False
    for col, w in zip("ABC", (50, 20, 60)): p.column_dimensions[col].width = w
    p["A1"] = "Painel do Mês"; p["A1"].font = T(18, True, MUSGO)
    p["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Preencha as células amarelas"; p["A2"].font = T(10, True, "A0522D" if exemplo else DOURADO)
    ex = dict(mes="Outubro (exemplo)", un=4, dias=31, noites=58, rec=16240, outras=980) if exemplo else {}
    faixa(p, 4, "1 · O MÊS")
    rotulo(p, 5, "Mês e ano", "Ex.: Outubro de 2026."); entrada(p, 5, ex.get("mes"), "@")
    rotulo(p, 6, "Unidades à venda (quartos, cabanas, casas)", "Só as que estavam disponíveis para reserva no mês."); entrada(p, 6, ex.get("un"), "0")
    rotulo(p, 7, "Dias do mês", "28, 29, 30 ou 31."); entrada(p, 7, ex.get("dias"), "0")
    rotulo(p, 8, "Noites vendidas no mês", "Some as noites de todas as reservas com entrada no mês, em todas as unidades."); entrada(p, 8, ex.get("noites"), "0")
    faixa(p, 10, "2 · O QUE ENTROU")
    rotulo(p, 11, "Receita de hospedagem (R$)", "O valor das diárias recebidas, antes das taxas das plataformas."); entrada(p, 11, ex.get("rec"))
    rotulo(p, 12, "Outras receitas (R$)", "Café, experiências, taxa de limpeza cobrada, venda de produtos."); entrada(p, 12, ex.get("outras"))
    faixa(p, 14, "3 · O QUE SAIU (por categoria)")
    for i, (nome, val) in enumerate(SAIDAS):
        rotulo(p, 15 + i, nome + " (R$)"); entrada(p, 15 + i, val if exemplo else None)
    L_FIM = 15 + len(SAIDAS) - 1  # 23
    faixa(p, 25, "4 · OS CINCO NÚMEROS DO GESTOR")
    rotulo(p, 26, "Situação dos dados")
    cs = p.cell(26, 2, '=IF(COUNTBLANK(B6:B8)+COUNTBLANK(B11:B12)+COUNTBLANK(B15:B23)>0,"Preencha todas as células amarelas (use 0 onde não houve)",IF(MIN(B6:B8,B11:B12,B15:B23)<0,"Há valor negativo",IF(B6*B7<=0,"Unidades e dias precisam ser maiores que zero",IF(B8>B6*B7,"Noites vendidas passam das noites disponíveis","OK"))))')
    cs.font = T(11, True); cs.border = borda; cs.fill = CALC
    OK = lambda f: '=IF($B$26="OK",' + f + ',"")'
    rotulo(p, 27, "Noites disponíveis no mês", "Unidades × dias do mês."); calc(p, 27, OK("B6*B7"), "0")
    rotulo(p, 28, "1 · QUANTO ENTROU", "Receita de hospedagem + outras receitas."); calc(p, 28, OK("B11+B12"), BRL, True)
    rotulo(p, 29, "Total que saiu", "Soma das categorias."); calc(p, 29, OK("SUM(B15:B23)"))
    rotulo(p, 30, "2 · QUANTO SOBROU", "Entrou − saiu. Não é lucro líquido."); calc(p, 30, OK("B28-B29"), BRL, True)
    rotulo(p, 31, "Margem do mês", "Quanto sobrou ÷ quanto entrou."); calc(p, 31, OK("IF(B28>0,B30/B28,0)"), "0.0%")
    rotulo(p, 32, "3 · OCUPAÇÃO", "Noites vendidas ÷ noites disponíveis."); calc(p, 32, OK("B8/B27"), "0.0%", True)
    rotulo(p, 33, "4 · DIÁRIA MÉDIA", "Receita de hospedagem ÷ noites vendidas."); calc(p, 33, OK('IF(B8>0,B11/B8,0)'), BRL, True)
    rotulo(p, 34, "Receita por noite disponível", "Receita de hospedagem ÷ noites disponíveis: junta ocupação e diária num número só."); calc(p, 34, OK("B11/B27"))
    rotulo(p, 35, "5 · CUSTO POR NOITE VENDIDA", "Total que saiu ÷ noites vendidas."); calc(p, 35, OK('IF(B8>0,B29/B8,0)'), BRL, True)
    rotulo(p, 36, "Leitura", "Compara a diária média com o custo por noite vendida.")
    calc(p, 36, '=IF($B$26="OK",IF(B8=0,"Sem noite vendida: cada real que saiu é prejuízo",IF(B33>B35,"Cada noite vendida paga o seu custo e ainda sobra",IF(B33=B35,"Cada noite vendida empata com o seu custo","Cada noite vendida custa mais do que rende: reveja preço e saídas"))),"")', "@")
    p.cell(38, 1, "Os números descrevem o mês que passou. Não são previsão nem promessa para o mês seguinte.").font = T(9, c="5F5F55", i=True)
    p.conditional_formatting.add("B26", FormulaRule(formula=['$B$26<>"OK"'], fill=PatternFill("solid", fgColor="F8E3DE"), font=Font(color="9B2C1F", bold=True)))
    dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, errorTitle="Valor inválido", error="Use um número maior ou igual a zero.")
    p.add_data_validation(dv); dv.add("B6:B8"); dv.add("B11:B12"); dv.add(f"B15:B{L_FIM}")

    h = wb.create_sheet("Histórico"); h.sheet_view.showGridLines = False; h.freeze_panes = "A3"
    cab = ["Mês", "Noites disponíveis", "Noites vendidas", "Quanto entrou (R$)", "Quanto saiu (R$)", "Quanto sobrou (R$)", "Ocupação", "Diária média (R$)", "Custo por noite vendida (R$)"]
    h["A1"] = "Histórico · copie os números do Painel, uma linha por mês (amarelo)." + ("  ·  EXEMPLO FICTÍCIO" if exemplo else ""); h["A1"].font = T(12, True, MUSGO)
    for i, (t, w) in enumerate(zip(cab, [16, 14, 14, 18, 18, 18, 12, 16, 18]), 1):
        x = h.cell(2, i, t); x.font = T(10, True, CREME); x.fill = CAB; x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); x.border = borda
        h.column_dimensions[x.column_letter].width = w
    h.row_dimensions[2].height = 34
    exh = [("Agosto (exemplo)", 124, 41, 12650, 5020, 11420), ("Setembro (exemplo)", 120, 47, 14110, 5160, 12960)] if exemplo else []
    for l in range(3, 27):
        for col in range(1, 6): x = h.cell(l, col); x.fill = ENTRADA; x.border = borda
        for col in (4, 5): h.cell(l, col).number_format = BRL
        f = lambda s: f'=IF(OR(B{l}="",C{l}="",D{l}="",E{l}=""),"",{s})'
        for col, s, fmt in ((6, f"D{l}-E{l}", BRL), (7, f"IF(B{l}>0,C{l}/B{l},0)", "0.0%"), (8, f"IF(C{l}>0,D{l}/C{l},0)", BRL), (9, f"IF(C{l}>0,E{l}/C{l},0)", BRL)):
            x = h.cell(l, col, f(s)); x.fill = CALC; x.border = borda; x.number_format = fmt
    for i, (m, nd, nv, ent, sai, _) in enumerate(exh):
        for col, v in zip(range(1, 6), (m, nd, nv, ent, sai)): h.cell(3 + i, col, v)
    if exemplo:  # o mês do painel entra na terceira linha, copiado dos mesmos números
        for col, v in zip(range(1, 6), ("Outubro (exemplo)", 124, 58, 17220, 5330)): h.cell(5, col, v)

    r = wb.create_sheet("Rotina"); r.sheet_view.showGridLines = False
    for col, w in zip("ABC", (14, 70, 12)): r.column_dimensions[col].width = w
    r["A1"] = "Rotina mínima de gestão · marque o que você já faz (amarelo)"; r["A1"].font = T(14, True, MUSGO)
    rot = [("Todo dia", "Olhar o calendário de reservas do dia e dos próximos 7 dias"), ("Todo dia", "Responder as mensagens de hóspedes e pedidos de reserva"), ("Todo dia", "Conferir a liberação das unidades que recebem hóspede hoje"),
           ("Toda semana", "Olhar os cinco números do mês até aqui e as avaliações da semana"), ("Toda semana", "Fazer a lista de compras pelo estoque mínimo"), ("Toda semana", "Olhar o quadro de ocorrências e de manutenção"), ("Toda semana", "Falar com a equipe: o que deu certo, o que travou"),
           ("Todo mês", "Fechar o mês no Painel e copiar para o Histórico"), ("Todo mês", "Comparar com o mês anterior e com a meta do ano"), ("Todo mês", "Revisar a diária mínima e os preços da próxima temporada"), ("Todo mês", "Decidir uma melhoria por área mais frágil e anotar o prazo")]
    for i, t in enumerate(["Quando", "O que olhar ou fazer", "Já faço?"], 1):
        x = r.cell(3, i, t); x.font = T(10, True, CREME); x.fill = CAB; x.border = borda
    for i, (q, o) in enumerate(rot):
        r.cell(4 + i, 1, q).font = T(10, True); r.cell(4 + i, 2, o).alignment = Alignment(wrap_text=True)
        x = r.cell(4 + i, 3, "Sim" if exemplo and i % 3 == 0 else None); x.fill = ENTRADA; x.border = borda
    dvs = DataValidation(type="list", formula1='"Sim,Não,Às vezes"', allow_blank=True); r.add_data_validation(dvs); dvs.add(f"C4:C{3 + len(rot)}")
    r.cell(5 + len(rot), 1, "Itens que você já faz:"); x = r.cell(5 + len(rot), 3, f'=COUNTIF(C4:C{3 + len(rot)},"Sim")'); x.fill = CALC; x.border = borda; x.font = T(12, True, MUSGO)
    r.cell(6 + len(rot), 1, f"de {len(rot)}. A rotina completa é a meta do módulo 7.").font = T(9, c="5F5F55", i=True)
    wb.active = 0
    return wb

for exemplo, nome in ((False, "Painel-do-Mes-Zion-EM-BRANCO.xlsx"), (True, "Painel-do-Mes-Zion-EXEMPLO.xlsx")):
    montar(exemplo).save(OUT / nome); print("ok", OUT / nome)

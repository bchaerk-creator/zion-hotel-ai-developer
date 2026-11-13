"""Gera a Ferramenta 19 · Controle de Compras e Consumo Interno (Zion Hospitality Business):
   - Controle-Compras-Zion-EM-BRANCO.xlsx / Controle-Compras-Zion-EXEMPLO.xlsx (dados fictícios)
Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dados import CATEGORIAS, PAGAMENTOS, EX_ORC, EX_MES, EX_NOITES, EX_COMPRAS
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, PRETO, CREME, TERRA = "1B2117", "040605", "FEF5F0", "8B714E"
ENTRADA, CALC, CAB = PatternFill("solid", fgColor="FFF4C7"), PatternFill("solid", fgColor="E3EEDF"), PatternFill("solid", fgColor=MUSGO)
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)
WRAP = Alignment(wrap_text=True, vertical="center")
BRL, DATA, PCT = 'R$ #,##0.00', "DD/MM/YYYY", "0%"
K0, NK = 6, 15         # categorias: linhas 6..20
C0, NC = 7, 400        # compras: linhas 7..406
VERDE, VERM, AMAR = "C8E6C0", "F4C7C3", "FCE8B2"
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

def cab(ws, l, tit):
    for j, t in enumerate(tit, 1):
        c = ws.cell(l, j, t); c.font = T(10, True, CREME); c.fill = CAB; c.alignment = WRAP; c.border = borda
    ws.row_dimensions[l].height = 42
def ent(c, v=None, fmt=None):
    c.value = v; c.fill = ENTRADA; c.border = borda; c.alignment = WRAP; c.font = T(10)
    if fmt: c.number_format = fmt
def calc(c, f, fmt=None, b=False):
    c.value = f; c.fill = CALC; c.border = borda; c.alignment = WRAP; c.font = T(10, b)
    if fmt: c.number_format = fmt
def lista(ws, rng, opcoes=None, ref=None, estrita=True):
    dv = DataValidation(type="list", formula1=ref or ('"' + ",".join(opcoes) + '"'), allow_blank=True,
                        showErrorMessage=estrita, errorTitle="Opção inválida", error="Escolha uma opção da lista.")
    ws.add_data_validation(dv); dv.add(rng)
d = lambda s: datetime.date.fromisoformat(s) if s else None

def montar(exemplo):
    wb = Workbook(); ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 104
    linhas = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 19", T(10, True, TERRA)),
        ("Controle de Compras e Consumo Interno", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para registrar as compras da sua hospedagem, comparar cada categoria com o orçamento do mês e saber quanto os insumos custam por noite ocupada.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (pousada, fornecedores e valores inventados; não servem como referência de preço). Use a versão em branco." if exemplo
         else "Versão em branco: as categorias já vêm prontas para você ajustar. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Para Airbnb, casas, apartamentos, pousadas e glampings.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 4 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Orçamento: ajuste as categorias e escreva quanto você quer gastar por mês em cada uma. Se ainda não sabe, deixe em branco por um ou dois meses e use o gasto real como base.", None),
        ("2. Aba Compras: uma linha por compra, com data, categoria, valor, forma de pagamento e se você guardou nota ou comprovante. Inclui o consumo da equipe (café, água, lanches).", None),
        ("3. Aba Mês: escreva qualquer dia do mês que quer ver e, se souber, quantas noites foram ocupadas. A planilha mostra o gasto de cada categoria, o orçamento, a diferença e o custo por noite ocupada.", None),
        ("4. Aba Ano: veja o gasto de cada categoria mês a mês, no ano do mês escolhido, e compare com o orçamento do ano.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("COMO A PLANILHA DECIDE", T(12, True, MUSGO)),
        ("Compra sem data, com categoria que não está na aba Orçamento ou com valor zero, negativo ou em texto não entra nas somas e aparece marcada. Compra sem comprovante entra nas somas, mas fica marcada para você conferir.", None),
        ("Situação da categoria no mês: Acima do orçamento quando o gasto passa do orçamento; Atenção quando chega a 90% ou mais; Dentro abaixo disso; Sem orçamento quando há gasto e nenhum orçamento escrito.", None),
        ("Custo por noite ocupada = gasto do mês ÷ noites ocupadas no mês. Noite ocupada é cada noite vendida de cada unidade (2 unidades ocupadas por 3 noites = 6).", None),
        ("", None),
        ("O QUE A PLANILHA NÃO FAZ", T(12, True, MUSGO)),
        ("Não é contabilidade nem controle fiscal, não controla estoque (para isso, use o Controle de Enxoval e Reposição) e não diz qual orçamento é o certo: o orçamento é decisão sua.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Orçamento ----------
    o = wb.create_sheet("Orçamento"); o.sheet_view.showGridLines = False
    for col, w in zip("ABC", (28, 48, 16)): o.column_dimensions[col].width = w
    o["A1"] = "Categorias e orçamento do mês"; o["A1"].font = T(18, True, MUSGO)
    o["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Ajuste os nomes e escreva o orçamento mensal de cada categoria."
    o["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    cab(o, 5, ["Categoria", "O que entra (exemplos)", "Orçamento por mês"])
    for i in range(NK):
        r = K0 + i; cat = CATEGORIAS[i] if i < len(CATEGORIAS) else (None, None)
        ent(o[f"A{r}"], cat[0]); ent(o[f"B{r}"], cat[1]); ent(o[f"C{r}"], EX_ORC.get(cat[0]) if exemplo and cat[0] else None, BRL)
    o[f"A{K0+NK+1}"] = "Orçamento total por mês"; o[f"A{K0+NK+1}"].font = T(10, True)
    calc(o[f"C{K0+NK+1}"], f"=SUM(C{K0}:C{K0+NK-1})", BRL, True)
    CAT = f"Orçamento!$A${K0}:$A${K0+NK-1}"

    # ---------- Compras ----------
    co = wb.create_sheet("Compras"); co.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHI", (12, 22, 32, 26, 14, 13, 16, 13, 26)): co.column_dimensions[col].width = w
    co["A1"] = "Compras"; co["A1"].font = T(18, True, MUSGO)
    co["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Uma linha por compra. Escolha a categoria da lista (ela precisa estar na aba Orçamento)."
    co["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    co["A3"] = "Compras com problema:"; co["A3"].font = T(10, True)
    rgI = f"I{C0}:I{C0+NC-1}"
    calc(co["C3"], f'=COUNTIF({rgI},"?*")-COUNTIF({rgI},"OK")-COUNTIF({rgI},"Sem comprovante")', b=True)
    co["D3"] = "Sem comprovante:"; co["D3"].font = T(10, True)
    calc(co["E3"], f'=COUNTIF({rgI},"Sem comprovante")', b=True)
    cab(co, 6, ["Data", "Categoria", "O que foi comprado", "Fornecedor", "Unidade (opcional)", "Valor", "Forma de pagamento", "Nota ou comprovante?", "Situação"])
    co.column_dimensions["J"].hidden = True
    for k in range(NC):
        r = C0 + k
        v = EX_COMPRAS[k] if exemplo and k < len(EX_COMPRAS) else (None,) * 8
        for col, x in zip("ABCDEFGH", (d(v[0]),) + tuple(v[1:])): ent(co[f"{col}{r}"], x, DATA if col == "A" else BRL if col == "F" else None)
        calc(co[f"I{r}"], f'=IF(AND(A{r}="",B{r}="",F{r}=""),"",IF(NOT(ISNUMBER(A{r})),"Informe a data",'
                          f'IF(OR(B{r}="",COUNTIF({CAT},B{r})=0),"Categoria não cadastrada",IF(OR(NOT(ISNUMBER(F{r})),F{r}<=0),"Confira o valor",'
                          f'IF(H{r}<>"Sim","Sem comprovante","OK")))))', b=True)
        calc(co[f"J{r}"], f'=IF(OR(I{r}="OK",I{r}="Sem comprovante"),1,0)')
    lista(co, f"B{C0}:B{C0+NC-1}", ref=CAT); lista(co, f"G{C0}:G{C0+NC-1}", PAGAMENTOS, estrita=False); lista(co, f"H{C0}:H{C0+NC-1}", ["Sim", "Não"])
    co.conditional_formatting.add(rgI, FormulaRule(formula=[f'I{C0}="Sem comprovante"'], fill=PatternFill("solid", fgColor=AMAR)))
    co.conditional_formatting.add(rgI, FormulaRule(formula=[f'AND(I{C0}<>"",I{C0}<>"OK",I{C0}<>"Sem comprovante")'], fill=PatternFill("solid", fgColor=VERM)))
    co.freeze_panes = f"A{C0}"
    rc = lambda c: f"Compras!${c}${C0}:${c}${C0+NC-1}"

    # ---------- Mês ----------
    m = wb.create_sheet("Mês"); m.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFG", (26, 14, 14, 14, 10, 24, 14)): m.column_dimensions[col].width = w
    m["A1"] = "Gastos do mês"; m["A1"].font = T(18, True, MUSGO)
    m["A3"] = "Qualquer dia do mês que quer ver"; m["A3"].font = T(10, True); ent(m["C3"], d(EX_MES) if exemplo else None, DATA)
    m["A4"] = "Noites ocupadas no mês (opcional)"; m["A4"].font = T(10, True); ent(m["C4"], EX_NOITES if exemplo else None)
    m["E3"] = "Mês:"; m["E3"].font = T(10, True)
    calc(m["F3"], '=IF(ISNUMBER(C3),TEXT(C3,"MM/YYYY"),"Informe uma data em C3")', b=True)
    calc(m["F4"], '=IF(ISNUMBER(C3),DATE(YEAR(C3),MONTH(C3),1),"")', DATA); calc(m["G4"], '=IF(ISNUMBER(C3),EOMONTH(C3,0),"")', DATA)
    m["E4"] = "De / até:"; m["E4"].font = T(10, True)
    cab(m, 6, ["Categoria", "Gasto no mês", "Orçamento", "Diferença (orçamento − gasto)", "% usado", "Situação", "Custo por noite ocupada"])
    M0 = 7
    for i in range(NK):
        r, kr = M0 + i, K0 + i
        calc(m[f"A{r}"], f'=IF(Orçamento!A{kr}="","",Orçamento!A{kr}&"")', b=True)
        calc(m[f"B{r}"], f'=IF(OR(A{r}="",NOT(ISNUMBER($C$3))),"",SUMIFS({rc("F")},{rc("B")},A{r},{rc("J")},1,{rc("A")},">="&$F$4,{rc("A")},"<="&$G$4))', BRL)
        calc(m[f"C{r}"], f'=IF(OR(A{r}="",NOT(ISNUMBER(Orçamento!C{kr}))),"",Orçamento!C{kr})', BRL)
        calc(m[f"D{r}"], f'=IF(OR(B{r}="",C{r}=""),"",C{r}-B{r})', BRL)
        calc(m[f"E{r}"], f'=IF(OR(B{r}="",C{r}=""),"",IF(C{r}=0,"",B{r}/C{r}))', PCT)
        calc(m[f"F{r}"], f'=IF(B{r}="","",IF(C{r}="",IF(B{r}>0,"Sem orçamento",""),IF(B{r}>C{r},"Acima do orçamento",IF(B{r}>=0.9*C{r},"Atenção: 90% ou mais","Dentro"))))', b=True)
        calc(m[f"G{r}"], f'=IF(OR(B{r}="",NOT(ISNUMBER($C$4))),"",IF($C$4>0,B{r}/$C$4,""))', BRL)
    t = M0 + NK
    m[f"A{t}"] = "Total"; m[f"A{t}"].font = T(10, True)
    calc(m[f"B{t}"], f'=IF(NOT(ISNUMBER($C$3)),"",SUMIFS({rc("F")},{rc("J")},1,{rc("A")},">="&$F$4,{rc("A")},"<="&$G$4))', BRL, True)
    calc(m[f"C{t}"], f"=SUM(C{M0}:C{t-1})", BRL, True)
    calc(m[f"D{t}"], f'=IF(B{t}="","",C{t}-B{t})', BRL, True)
    calc(m[f"E{t}"], f'=IF(OR(B{t}="",C{t}=0),"",B{t}/C{t})', PCT, True)
    calc(m[f"G{t}"], f'=IF(OR(B{t}="",NOT(ISNUMBER($C$4))),"",IF($C$4>0,B{t}/$C$4,""))', BRL, True)
    r = t + 2
    for rot, f in (("Categorias acima do orçamento", f'=COUNTIF(F{M0}:F{t-1},"Acima do orçamento")'),
                   ("Categorias em atenção (90% ou mais)", f'=COUNTIF(F{M0}:F{t-1},"Atenção: 90% ou mais")'),
                   ("Compras sem comprovante no mês", f'=IF(NOT(ISNUMBER($C$3)),"",COUNTIFS({rc("I")},"Sem comprovante",{rc("A")},">="&$F$4,{rc("A")},"<="&$G$4))'),
                   ("Compras com problema (todas as datas)", "=Compras!C3")):
        m[f"A{r}"] = rot; m[f"A{r}"].font = T(10, True); calc(m[f"C{r}"], f, b=True); r += 1
    rgF = f"F{M0}:F{t-1}"
    for cond, cor in ((f'F{M0}="Acima do orçamento"', VERM), (f'LEFT(F{M0},7)="Atenção"', AMAR), (f'F{M0}="Dentro"', VERDE), (f'F{M0}="Sem orçamento"', AMAR)):
        m.conditional_formatting.add(rgF, FormulaRule(formula=[cond], fill=PatternFill("solid", fgColor=cor)))
    m.freeze_panes = f"B{M0}"

    # ---------- Ano ----------
    a = wb.create_sheet("Ano"); a.sheet_view.showGridLines = False
    a.column_dimensions["A"].width = 26
    for j in range(2, 17): a.column_dimensions[a.cell(1, j).column_letter].width = 11
    a["A1"] = "Gastos do ano"; a["A1"].font = T(18, True, MUSGO)
    a["A3"] = "Ano (do mês escolhido na aba Mês):"; a["A3"].font = T(10, True)
    calc(a["D3"], '=IF(ISNUMBER(Mês!C3),YEAR(Mês!C3),"")', b=True)
    cab(a, 5, ["Categoria"] + MESES + ["Total do ano", "Orçamento do ano", "Diferença"])
    A0 = 6
    for i in range(NK):
        r, kr = A0 + i, K0 + i
        calc(a[f"A{r}"], f'=IF(Orçamento!A{kr}="","",Orçamento!A{kr}&"")', b=True)
        for mi in range(12):
            col = a.cell(r, 2 + mi).column_letter
            ini, fim = f"DATE($D$3,{mi+1},1)", f"EOMONTH(DATE($D$3,{mi+1},1),0)"
            calc(a[f"{col}{r}"], f'=IF(OR(A{r}="",$D$3=""),"",SUMIFS({rc("F")},{rc("B")},A{r},{rc("J")},1,{rc("A")},">="&{ini},{rc("A")},"<="&{fim}))', BRL)
        calc(a[f"N{r}"], f'=IF(OR(A{r}="",$D$3=""),"",SUM(B{r}:M{r}))', BRL, True)
        calc(a[f"O{r}"], f'=IF(OR(A{r}="",NOT(ISNUMBER(Orçamento!C{kr}))),"",12*Orçamento!C{kr})', BRL)
        calc(a[f"P{r}"], f'=IF(OR(N{r}="",O{r}=""),"",O{r}-N{r})', BRL)
    t = A0 + NK
    a[f"A{t}"] = "Total"; a[f"A{t}"].font = T(10, True)
    for j in range(2, 17):
        col = a.cell(t, j).column_letter
        calc(a[f"{col}{t}"], f'=IF($D$3="","",SUM({col}{A0}:{col}{t-1}))', BRL, True)
    a.freeze_panes = f"B{A0}"
    a.page_setup.orientation = "landscape"; a.page_setup.fitToWidth = 1; a.page_setup.fitToHeight = 0; a.sheet_properties.pageSetUpPr.fitToPage = True

    wb.active = 0
    nome = "Controle-Compras-Zion-EXEMPLO.xlsx" if exemplo else "Controle-Compras-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

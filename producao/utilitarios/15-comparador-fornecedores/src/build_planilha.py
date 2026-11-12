"""Gera a Ferramenta 15 · Comparador de Fornecedores (Zion Hospitality Business):
   - Comparador-Fornecedores-Zion-EM-BRANCO.xlsx / Comparador-Fornecedores-Zion-EXEMPLO.xlsx (dados fictícios)
Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dados import CRITERIOS, UNIDADES, SUGESTOES, EX_NEC, EX_COT
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
BRL, BRL4 = 'R$ #,##0.00', 'R$ #,##0.0000'
K0 = 6                 # critérios: linhas 6..11
N0, NN = 6, 30         # necessidades: linhas 6..35
C0, NC = 7, 150        # cotações: linhas 7..156
VERDE, VERM, AMAR = "C8E6C0", "F4C7C3", "FCE8B2"
MAXIFS, MINIFS = "_xlfn.MAXIFS", "_xlfn.MINIFS"

def cab(ws, l, tit):
    for j, t in enumerate(tit, 1):
        c = ws.cell(l, j, t); c.font = T(10, True, CREME); c.fill = CAB; c.alignment = WRAP; c.border = borda
    ws.row_dimensions[l].height = 48
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
def nota(ws, rng):
    dv = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True,
                        showErrorMessage=True, errorStyle="warning", errorTitle="Nota de 1 a 5", error="Use uma nota inteira de 1 a 5.")
    ws.add_data_validation(dv); dv.add(rng)

def montar(exemplo):
    wb = Workbook(); ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 104
    linhas = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 15", T(10, True, TERRA)),
        ("Comparador de Fornecedores", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para comparar fornecedores da sua hospedagem pelo custo real, pelo prazo e pelo que importa para você, e escolher com critério.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (fornecedores, preços e notas inventados; não servem como referência de preço). Use a versão em branco." if exemplo
         else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Para Airbnb, casas, apartamentos, pousadas e glampings.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 4 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Critérios: dê um peso de 0 a 5 a cada critério (5 = pesa muito; 0 = não conta). Os pesos que vêm prontos são só um ponto de partida.", None),
        ("2. Aba Necessidades: liste o que você compra ou contrata com frequência, a unidade para comparar (kg, L, rolo...) e, se souber, quanto usa por mês.", None),
        ("3. Aba Cotações: uma linha por fornecedor, com a embalagem, o preço, o frete, o pedido mínimo, o prazo e as suas notas de 1 a 5. Peça a mesma especificação a todos.", None),
        ("4. Aba Resumo: veja quantas cotações válidas cada necessidade tem, quem tem a melhor nota, quem tem o menor custo e a diferença por mês entre os dois.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("COMO A PLANILHA DECIDE", T(12, True, MUSGO)),
        ("Custo comparável = (preço da embalagem × pedido mínimo + frete do pedido) ÷ (quantidade na embalagem × pedido mínimo). Pedido mínimo vazio conta como 1; frete vazio, como zero.", None),
        ("Nota de preço = 5 × menor custo comparável da mesma necessidade ÷ custo desta cotação. Nota de prazo = 5 × (menor prazo + 1) ÷ (prazo desta cotação + 1).", None),
        ("Nota final = média das notas pelos pesos, só com as notas preenchidas, arredondada em 2 casas. Melhor nota: a maior nota final da necessidade; no empate, a de menor custo.", None),
        ("Cotação com necessidade não cadastrada, sem fornecedor, sem preço ou quantidade, com frete, pedido mínimo ou prazo inválidos ou com nota fora de 1 a 5 não entra na comparação e aparece marcada.", None),
        ("", None),
        ("O QUE A PLANILHA NÃO FAZ", T(12, True, MUSGO)),
        ("Não pesquisa preços nem indica fornecedores, não confere nota fiscal nem contrato e não garante economia. As notas são suas: a planilha só organiza e faz a conta.", None),
        ("", None),
        ("Funciona no Excel 2019 ou mais novo, no Excel 365, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Critérios ----------
    cr = wb.create_sheet("Critérios"); cr.sheet_view.showGridLines = False
    for col, w in zip("ABC", (26, 62, 12)): cr.column_dimensions[col].width = w
    cr["A1"] = "Critérios e pesos"; cr["A1"].font = T(18, True, MUSGO)
    cr["A2"] = "Peso de 0 a 5. Zero tira o critério da conta. Os pesos prontos são um ponto de partida: ajuste ao que importa na sua operação."
    cr["A2"].font = T(10, c="5F5F55", i=True)
    cab(cr, 5, ["Critério", "O que mede", "Peso (0 a 5)"])
    for i, (n, d, p) in enumerate(CRITERIOS):
        r = K0 + i; calc(cr[f"A{r}"], n, b=True); calc(cr[f"B{r}"], d); ent(cr[f"C{r}"], p)
    dv = DataValidation(type="decimal", operator="between", formula1="0", formula2="5", allow_blank=True, showErrorMessage=True,
                        errorTitle="Peso de 0 a 5", error="Use um peso de 0 a 5."); cr.add_data_validation(dv); dv.add(f"C{K0}:C{K0+5}")
    cr["A13"] = "Soma dos pesos"; cr["A13"].font = T(10, True)
    calc(cr["C13"], f"=SUMPRODUCT((ISNUMBER(C{K0}:C{K0+5}))*(C{K0}:C{K0+5}>0),C{K0}:C{K0+5})", b=True)
    W = [f"MAX(0,N(Critérios!$C${K0+i}))" for i in range(6)]

    # ---------- Necessidades ----------
    ne = wb.create_sheet("Necessidades"); ne.sheet_view.showGridLines = False
    for col, w in zip("ABCD", (30, 14, 14, 50)): ne.column_dimensions[col].width = w
    ne["A1"] = "O que você compra ou contrata"; ne["A1"].font = T(18, True, MUSGO)
    ne["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Ideias: " + ", ".join(SUGESTOES[:6]) + "."
    ne["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    ne["A3"] = "Unidade comparável: a medida em que todas as cotações serão convertidas (por exemplo, preço por litro, por kg, por rolo)."
    ne["A3"].font = T(9, c="5F5F55", i=True)
    cab(ne, 5, ["Necessidade", "Unidade comparável", "Consumo por mês (opcional)", "Especificação para pedir igual a todos"])
    for i in range(NN):
        r = N0 + i; v = EX_NEC[i] if exemplo and i < len(EX_NEC) else (None,) * 4
        for col, x in zip("ABCD", v): ent(ne[f"{col}{r}"], x)
    lista(ne, f"B{N0}:B{N0+NN-1}", UNIDADES, estrita=False)
    ne.freeze_panes = f"A{N0}"

    # ---------- Cotações ----------
    co = wb.create_sheet("Cotações"); co.sheet_view.showGridLines = False
    larg = (24, 26, 16, 11, 12, 11, 10, 10, 9, 9, 9, 9, 24, 13, 9, 9, 9, 22, 13, 11)
    for j, w in enumerate(larg, 1): co.column_dimensions[co.cell(1, j).column_letter].width = w
    co["A1"] = "Cotações"; co["A1"].font = T(18, True, MUSGO)
    co["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Uma linha por fornecedor e necessidade. Quantidade na embalagem na unidade comparável (galão de 5 L = 5)."
    co["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    co["A3"] = "Cotações com problema:"; co["A3"].font = T(10, True)
    rgM = f"M{C0}:M{C0+NC-1}"
    calc(co["D3"], f'=COUNTIF({rgM},"?*")-COUNTIF({rgM},"OK")', b=True)
    co["A4"] = "Notas de 1 a 5: 5 = excelente. Deixe em branco o que você ainda não sabe: a nota final usa só o que foi preenchido."
    co["A4"].font = T(9, c="5F5F55", i=True)
    cab(co, 6, ["Necessidade", "Fornecedor", "Embalagem ou serviço", "Quantidade na embalagem", "Preço da embalagem", "Frete por pedido (opcional)",
                "Pedido mínimo em embalagens (opcional)", "Prazo de entrega em dias (opcional)", "Qualidade (1 a 5)", "Atendimento (1 a 5)",
                "Pagamento (1 a 5)", "Confiabilidade (1 a 5)", "Situação", "Custo comparável", "Nota de preço", "Nota de prazo", "Nota final",
                "Resultado", "Custo por mês", "Meses cobertos pelo pedido mínimo"])
    co.column_dimensions["W"].hidden = co.column_dimensions["X"].hidden = co.column_dimensions["Y"].hidden = co.column_dimensions["Z"].hidden = True
    rg = lambda c: f"${c}${C0}:${c}${C0+NC-1}"
    NEC = f"Necessidades!$A${N0}:$A${N0+NN-1}"
    for k in range(NC):
        r = C0 + k
        v = EX_COT[k] if exemplo and k < len(EX_COT) else (None,) * 12
        for col, x in zip("ABCDEFGHIJKL", v): ent(co[f"{col}{r}"], x, BRL if col in "EF" else None)
        notas_ruins = "OR(" + ",".join(f'AND({c}{r}<>"",OR(NOT(ISNUMBER({c}{r})),{c}{r}<1,{c}{r}>5))' for c in "IJKL") + ")"
        calc(co[f"M{r}"],
             f'=IF(AND(A{r}="",B{r}="",E{r}=""),"",IF(OR(A{r}="",COUNTIF({NEC},A{r})=0),"Necessidade não cadastrada",'
             f'IF(B{r}="","Falta o fornecedor",IF(OR(NOT(ISNUMBER(D{r})),NOT(ISNUMBER(E{r}))),"Confira quantidade e preço",'
             f'IF(OR(D{r}<=0,E{r}<=0),"Confira quantidade e preço",'
             f'IF(OR(AND(F{r}<>"",OR(NOT(ISNUMBER(F{r})),F{r}<0)),AND(G{r}<>"",OR(NOT(ISNUMBER(G{r})),G{r}<1))),"Confira frete e pedido mínimo",'
             f'IF(AND(H{r}<>"",OR(NOT(ISNUMBER(H{r})),H{r}<0)),"Confira o prazo",IF({notas_ruins},"Confira as notas (1 a 5)","OK"))))))))', b=True)
        kmin, frete = f"IF(ISNUMBER(G{r}),G{r},1)", f"IF(ISNUMBER(F{r}),F{r},0)"
        calc(co[f"N{r}"], f'=IF(M{r}<>"OK","",(E{r}*{kmin}+{frete})/(D{r}*{kmin}))', BRL4)
        calc(co[f"W{r}"], f'=IF(AND(M{r}="OK",ISNUMBER(H{r})),H{r},"")')
        calc(co[f"O{r}"], f'=IF(M{r}<>"OK","",5*{MINIFS}({rg("N")},{rg("A")},A{r})/N{r})', "0.00")
        calc(co[f"P{r}"], f'=IF(W{r}="","",5*({MINIFS}({rg("W")},{rg("A")},A{r})+1)/(W{r}+1))', "0.00")
        num = f"{W[0]}*O{r}+IF(P{r}=\"\",0,{W[1]}*P{r})" + "".join(f"+IF(ISNUMBER({c}{r}),{W[i]}*{c}{r},0)" for i, c in zip(range(2, 6), "IJKL"))
        den = f"{W[0]}+IF(P{r}=\"\",0,{W[1]})" + "".join(f"+IF(ISNUMBER({c}{r}),{W[i]},0)" for i, c in zip(range(2, 6), "IJKL"))
        calc(co[f"Q{r}"], f'=IF(M{r}<>"OK","",IF(({den})=0,"Defina os pesos",ROUND(({num})/({den}),2)))', "0.00", True)
        calc(co[f"X{r}"], f'=IF(AND(ISNUMBER(Q{r}),Q{r}={MAXIFS}({rg("Q")},{rg("A")},A{r})),N{r},"")')
        best = f'AND(X{r}<>"",X{r}={MINIFS}({rg("X")},{rg("A")},A{r}))'
        cheap = f'AND(N{r}<>"",N{r}={MINIFS}({rg("N")},{rg("A")},A{r}))'
        calc(co[f"R{r}"], f'=IF(M{r}<>"OK","",IF(AND({best},{cheap}),"Melhor nota e menor custo",IF({best},"Melhor nota",IF({cheap},"Menor custo",""))))', b=True)
        calc(co[f"Y{r}"], f'=IF(LEFT(R{r},11)="Melhor nota",A{r},"")')
        calc(co[f"Z{r}"], f'=IF(OR(R{r}="Menor custo",R{r}="Melhor nota e menor custo"),A{r},"")')
        cons = f"SUMIF({NEC},A{r},Necessidades!$C${N0}:$C${N0+NN-1})"
        calc(co[f"S{r}"], f'=IF(OR(N{r}="",COUNTIF({NEC},A{r})<>1),"",IF({cons}>0,N{r}*{cons},""))', BRL)
        calc(co[f"T{r}"], f'=IF(S{r}="","",ROUND(D{r}*{kmin}/{cons},1))', "0.0")
    lista(co, f"A{C0}:A{C0+NC-1}", ref=NEC); nota(co, f"I{C0}:L{C0+NC-1}")
    co.conditional_formatting.add(rgM, FormulaRule(formula=[f'AND(M{C0}<>"",M{C0}<>"OK")'], fill=PatternFill("solid", fgColor=VERM)))
    co.conditional_formatting.add(f"R{C0}:R{C0+NC-1}", FormulaRule(formula=[f'LEFT(R{C0},11)="Melhor nota"'], fill=PatternFill("solid", fgColor=VERDE)))
    co.conditional_formatting.add(f"R{C0}:R{C0+NC-1}", FormulaRule(formula=[f'R{C0}="Menor custo"'], fill=PatternFill("solid", fgColor=AMAR)))
    co.freeze_panes = f"C{C0}"

    # ---------- Resumo ----------
    s = wb.create_sheet("Resumo"); s.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHI", (28, 11, 26, 26, 9, 14, 26, 14, 16)): s.column_dimensions[col].width = w
    s["A1"] = "Resumo por necessidade"; s["A1"].font = T(18, True, MUSGO)
    s["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Tudo calculado."; s["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    S0 = 7; rs = lambda c: f"{c}{S0}:{c}{S0+NN-1}"
    for a, t, b, f in (("A3", "Necessidades cadastradas", "C3", f'=COUNTIF({NEC},"?*")'),
                       ("A4", "Prontas para decidir (3 cotações ou mais)", "C4", f'=COUNTIF({rs("C")},"Pronto para decidir")'),
                       ("A5", "Cotações com problema", "C5", "=Cotações!D3")):
        s[a] = t; s[a].font = T(10, True); calc(s[b], f, b=True)
    cab(s, 6, ["Necessidade", "Cotações válidas", "Situação", "Melhor nota", "Nota final", "Custo comparável", "Menor custo", "Custo comparável",
               "Diferença por mês (melhor nota − menor custo)"])
    for i in range(NN):
        r, nr = S0 + i, N0 + i; vazio = f'Necessidades!$A${nr}=""'
        calc(s[f"A{r}"], f'=IF({vazio},"",Necessidades!A{nr}&"")', b=True)
        calc(s[f"B{r}"], f'=IF(A{r}="","",COUNTIFS(Cotações!$A${C0}:$A${C0+NC-1},A{r},Cotações!$M${C0}:$M${C0+NC-1},"OK"))')
        calc(s[f"C{r}"], f'=IF(A{r}="","",IF(B{r}=0,"Sem cotações válidas",IF(B{r}<3,"Peça mais cotações (ideal: 3)","Pronto para decidir")))', b=True)
        tem_m = f'COUNTIF(Cotações!$Y${C0}:$Y${C0+NC-1},A{r})>0'
        pos_m = f'MATCH(A{r},Cotações!$Y${C0}:$Y${C0+NC-1},0)'
        pos_c = f'MATCH(A{r},Cotações!$Z${C0}:$Z${C0+NC-1},0)'
        calc(s[f"D{r}"], f'=IF(OR(A{r}="",B{r}=0),"",IF({tem_m},INDEX(Cotações!$B${C0}:$B${C0+NC-1},{pos_m}),"Defina os pesos"))', b=True)
        calc(s[f"E{r}"], f'=IF(OR(A{r}="",B{r}=0),"",IF({tem_m},INDEX(Cotações!$Q${C0}:$Q${C0+NC-1},{pos_m}),""))', "0.00")
        calc(s[f"F{r}"], f'=IF(E{r}="","",INDEX(Cotações!$N${C0}:$N${C0+NC-1},{pos_m}))', BRL4)
        calc(s[f"G{r}"], f'=IF(OR(A{r}="",B{r}=0),"",INDEX(Cotações!$B${C0}:$B${C0+NC-1},{pos_c}))')
        calc(s[f"H{r}"], f'=IF(G{r}="","",INDEX(Cotações!$N${C0}:$N${C0+NC-1},{pos_c}))', BRL4)
        calc(s[f"I{r}"], f'=IF(OR(F{r}="",H{r}="",N(Necessidades!C{nr})<=0),"",(F{r}-H{r})*Necessidades!C{nr})', BRL)
    for cond, cor in ((f'C{S0}="Pronto para decidir"', VERDE), (f'LEFT(C{S0},4)="Peça"', AMAR), (f'C{S0}="Sem cotações válidas"', VERM)):
        s.conditional_formatting.add(rs("C"), FormulaRule(formula=[cond], fill=PatternFill("solid", fgColor=cor)))
    s.freeze_panes = f"B{S0}"
    s.page_setup.orientation = "landscape"; s.page_setup.fitToWidth = 1; s.page_setup.fitToHeight = 0; s.sheet_properties.pageSetUpPr.fitToPage = True

    wb.active = 0
    nome = "Comparador-Fornecedores-Zion-EXEMPLO.xlsx" if exemplo else "Comparador-Fornecedores-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

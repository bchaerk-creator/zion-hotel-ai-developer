"""Gera a Ferramenta 10 · Fechamento Mensal por Imóvel (Zion Hospitality Business):
   - Fechamento-Mensal-Zion-EM-BRANCO.xlsx / Fechamento-Mensal-Zion-EXEMPLO.xlsx (dados fictícios)
Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dados import TODOS, TIPOS, CANAIS, CATEGORIAS, SIM_NAO, EX_MES, EX_IMOVEIS, EX_LANC, VALIDAS
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
BRL, DATA, MES = 'R$ #,##0.00', "DD/MM/YYYY", "MM/YYYY"
I0, NI = 7, 10          # imóveis: Cadastros!A7:A16 (A17 = dividir igual)
K0, NK = 7, 20          # categorias: Cadastros!C7:C26
L0, NL = 7, 500         # lançamentos: linhas 7..506
F0 = 8                  # fechamento: linhas 8..17, total na 18
VERDE, VERM, AMAR = "C8E6C0", "F4C7C3", "FCE8B2"
d = lambda s: datetime.date.fromisoformat(s) if s else None
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

def cab(ws, l, tit, c0=1):
    for j, t in enumerate(tit, c0):
        c = ws.cell(l, j, t); c.font = T(10, True, CREME); c.fill = CAB; c.alignment = WRAP; c.border = borda
    ws.row_dimensions[l].height = 40
def ent(c, v=None, fmt=None):
    c.value = v; c.fill = ENTRADA; c.border = borda; c.alignment = WRAP; c.font = T(10)
    if fmt: c.number_format = fmt
def calc(c, f, fmt=None, b=False):
    c.value = f; c.fill = CALC; c.border = borda; c.alignment = WRAP; c.font = T(10, b)
    if fmt: c.number_format = fmt
def lista(ws, rng, opcoes=None, ref=None, msg="Escolha uma opção da lista."):
    dv = DataValidation(type="list", formula1=ref or ('"' + ",".join(opcoes) + '"'), allow_blank=True, showErrorMessage=True, errorTitle="Opção inválida", error=msg)
    ws.add_data_validation(dv); dv.add(rng)

def montar(exemplo):
    wb = Workbook(); ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 104
    linhas = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 10", T(10, True, TERRA)),
        ("Fechamento Mensal por Imóvel", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para fechar o mês de cada imóvel: o que entrou por canal, o que saiu por categoria, as despesas divididas entre os imóveis e o que ainda falta conferir no extrato.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (imóveis, lançamentos e valores inventados). Use a versão em branco." if exemplo
         else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Para Airbnb, casas, apartamentos, pousadas e glampings.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 4 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Cadastros: escreva o nome de cada imóvel (até 10) e ajuste as categorias de despesa (10 prontas, até 20).", None),
        ("2. Aba Lançamentos: uma linha por entrada ou saída de dinheiro, com data, imóvel, tipo, canal (receita) ou categoria (despesa) e valor. Receita = o valor que caiu na sua conta. Despesa de vários imóveis (internet, contador, ferramenta): escolha \"Todos (dividir igual)\".", None),
        ("3. Com o extrato do banco aberto, marque \"Sim\" em \"Conferido no extrato?\" em cada lançamento que você encontrou lá.", None),
        ("4. Aba Fechamento: escolha o mês e veja receitas, despesas e resultado de cada imóvel, o que falta conferir e o que fazer agora. A aba Ano mostra o resultado de cada mês.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("COMO A PLANILHA DECIDE", T(12, True, MUSGO)),
        ("Resultado do imóvel = receitas − despesas do imóvel − a parte dele nas despesas divididas. Despesa dividida = valor ÷ número de imóveis cadastrados, em partes iguais.", None),
        ("Lançamento sem data, sem imóvel, com imóvel ou categoria que não está nos Cadastros, receita sem canal ou com \"Todos\", ou valor zero, negativo ou em texto fica com problema e não entra nas contas até ser corrigido. Lançamento não conferido entra nas contas, mas fica marcado.", None),
        ("", None),
        ("CUIDADOS", T(12, True, MUSGO)),
        ("Resultado do mês não é lucro: só soma o que você lançou. Impostos, sua remuneração, depreciação e reservas para reformas ficam de fora se não forem lançados.", None),
        ("Não é contabilidade nem declaração de imposto: fale com o seu contador. Não anote dados de hóspedes: na descrição, use o código da reserva se precisar.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Cadastros ----------
    ca = wb.create_sheet("Cadastros"); ca.sheet_view.showGridLines = False
    for col, w in zip("ABCDE", (34, 4, 30, 4, 22)): ca.column_dimensions[col].width = w
    ca["A1"] = "Cadastros"; ca["A1"].font = T(18, True, MUSGO)
    ca["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Escreva os imóveis e ajuste as categorias. Os nomes aparecem nas listas da aba Lançamentos."
    ca["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    cab(ca, 6, ["Imóvel"]); cab(ca, 6, ["Categoria de despesa"], 3); cab(ca, 6, ["Canais de receita (fixos)"], 5)
    for k in range(NI): ent(ca[f"A{I0+k}"], EX_IMOVEIS[k] if exemplo and k < len(EX_IMOVEIS) else None)
    calc(ca[f"A{I0+NI}"], TODOS)
    ca[f"A{I0+NI+1}"] = "Use \"Todos (dividir igual)\" para despesas de vários imóveis."; ca[f"A{I0+NI+1}"].font = T(9, c="5F5F55", i=True)
    for k in range(NK): ent(ca[f"C{K0+k}"], CATEGORIAS[k] if k < len(CATEGORIAS) else None)
    for k, cn in enumerate(CANAIS): calc(ca[f"E{K0+k}"], cn)
    IMV = f"Cadastros!$A${I0}:$A${I0+NI-1}"; IMV_LISTA = f"Cadastros!$A${I0}:$A${I0+NI}"
    CAT = f"Cadastros!$C${K0}:$C${K0+NK-1}"

    # ---------- Lançamentos ----------
    la = wb.create_sheet("Lançamentos"); la.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGH", (12, 26, 11, 22, 28, 14, 12, 26)): la.column_dimensions[col].width = w
    la["A1"] = "Lançamentos"; la["A1"].font = T(18, True, MUSGO)
    la["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Uma linha por entrada ou saída de dinheiro. Receita = valor que caiu na conta."
    la["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    la["A3"] = "Lançamentos com problema:"; la["A3"].font = T(10, True)
    rgH = f"H{L0}:H{L0+NL-1}"
    calc(la["D3"], f'=COUNTIF({rgH},"?*")-COUNTIF({rgH},"OK")-COUNTIF({rgH},"A conferir no extrato")', b=True)
    cab(la, 6, ["Data", "Imóvel", "Tipo", "Canal (receita) ou categoria (despesa)", "Descrição", "Valor", "Conferido no extrato?", "Situação"])
    for col in "IJ": la.column_dimensions[col].hidden = True
    canal_ok = lambda r: "OR(" + ",".join(f'D{r}="{c}"' for c in CANAIS) + ")"
    for k in range(NL):
        r = L0 + k; v = EX_LANC[k] if exemplo and k < len(EX_LANC) else (None,) * 7
        for col, x, fmt in zip("ABCDEFG", (d(v[0]), v[1], v[2], v[3], v[4], v[5], v[6]), (DATA, None, None, None, None, BRL, None)):
            ent(la[f"{col}{r}"], x, fmt)
        val = f'IF(OR(NOT(ISNUMBER(F{r})),N(F{r})<=0),"Confira o valor",IF(G{r}<>"Sim","A conferir no extrato","OK"))'
        calc(la[f"H{r}"], f'=IF(AND(A{r}="",B{r}="",C{r}="",F{r}=""),"",IF(NOT(ISNUMBER(A{r})),"Informe a data",IF(B{r}="","Escolha o imóvel",'
                          f'IF(AND(B{r}<>"{TODOS}",COUNTIF({IMV},B{r})=0),"Imóvel não cadastrado",IF(AND(C{r}<>"Receita",C{r}<>"Despesa"),"Escolha o tipo",'
                          f'IF(C{r}="Receita",IF(B{r}="{TODOS}","Receita precisa de um imóvel",IF(NOT({canal_ok(r)}),"Escolha o canal",{val})),'
                          f'IF(OR(D{r}="",COUNTIF({CAT},D{r})=0),"Categoria não cadastrada",{val})))))))', b=True)
        calc(la[f"I{r}"], f'=IF(ISNUMBER(A{r}),DATE(YEAR(A{r}),MONTH(A{r}),1),0)', MES)
        calc(la[f"J{r}"], f'=IF(OR(H{r}="OK",H{r}="A conferir no extrato"),1,0)')
    lista(la, f"B{L0}:B{L0+NL-1}", ref=IMV_LISTA, msg="Escolha um imóvel da aba Cadastros.")
    lista(la, f"C{L0}:C{L0+NL-1}", TIPOS); lista(la, f"G{L0}:G{L0+NL-1}", SIM_NAO)
    for cond, cor in ((f'H{L0}="OK"', VERDE), (f'H{L0}="A conferir no extrato"', AMAR),
                      (f'AND(H{L0}<>"",H{L0}<>"OK",H{L0}<>"A conferir no extrato")', VERM)):
        la.conditional_formatting.add(rgH, FormulaRule(formula=[cond], fill=PatternFill("solid", fgColor=cor)))
    la.freeze_panes = f"A{L0}"
    rl = lambda c: f"Lançamentos!${c}${L0}:${c}${L0+NL-1}"

    # ---------- Fechamento ----------
    fe = wb.create_sheet("Fechamento"); fe.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFG", (34, 15, 15, 17, 15, 13, 24)): fe.column_dimensions[col].width = w
    fe["A1"] = "Fechamento do mês"; fe["A1"].font = T(18, True, MUSGO)
    fe["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Escolha o mês (qualquer dia do mês serve). O resto é calculado."
    fe["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    fe["A3"] = "Mês do fechamento"; fe["A3"].font = T(10, True)
    ent(fe["B3"], d(EX_MES) if exemplo else "=DATE(YEAR(TODAY()),MONTH(TODAY())-1,1)", MES)
    fe["D3"] = "Imóveis cadastrados"; fe["D3"].font = T(10, True)
    calc(fe["E3"], f'=COUNTIF({IMV},"?*")', b=True)
    calc(fe["H3"], '=IF(ISNUMBER(B3),DATE(YEAR(B3),MONTH(B3),1),0)', MES); fe.column_dimensions["H"].hidden = True
    fe["A4"] = "Lançamentos com problema (todos os meses)"; fe["A4"].font = T(10, True)
    calc(fe["B4"], "=Lançamentos!D3", b=True)
    fe["A5"] = "O que fazer agora"; fe["A5"].font = T(12, True, MUSGO)
    M, N = "$H$3", "Fechamento!$E$3"
    div = lambda mes: f'IF({N}>0,SUMIFS({rl("F")},{rl("B")},"{TODOS}",{rl("C")},"Despesa",{rl("I")},{mes},{rl("J")},1)/{N},0)'
    soma = lambda nome, tipo, mes: f'SUMIFS({rl("F")},{rl("B")},{nome},{rl("C")},"{tipo}",{rl("I")},{mes},{rl("J")},1)'
    cab(fe, 7, ["Imóvel", "Receitas", "Despesas do imóvel", "Parte das despesas divididas", "Resultado", "A conferir no extrato", "Situação"])
    for k in range(NI):
        r = F0 + k
        calc(fe[f"A{r}"], f'=IF(Cadastros!A{I0+k}="","",Cadastros!A{I0+k})')
        calc(fe[f"B{r}"], f'=IF(A{r}="","",{soma(f"A{r}", "Receita", M)})', BRL)
        calc(fe[f"C{r}"], f'=IF(A{r}="","",{soma(f"A{r}", "Despesa", M)})', BRL)
        calc(fe[f"D{r}"], f'=IF(A{r}="","",{div(M)})', BRL)
        calc(fe[f"E{r}"], f'=IF(A{r}="","",B{r}-C{r}-D{r})', BRL, True)
        calc(fe[f"F{r}"], f'=IF(A{r}="","",COUNTIFS({rl("B")},A{r},{rl("I")},{M},{rl("H")},"A conferir no extrato"))')
        calc(fe[f"G{r}"], f'=IF(A{r}="","",IF(AND(B{r}=0,C{r}=0,F{r}=0),"Sem lançamentos próprios",IF(F{r}>0,"Confira "&F{r}&" no extrato",IF(E{r}<0,"Resultado negativo","Fechado"))))', b=True)
    T_ = F0 + NI
    fe[f"A{T_}"] = "Total"; fe[f"A{T_}"].font = T(10, True)
    for col in "BCDE": calc(fe[f"{col}{T_}"], f"=SUM({col}{F0}:{col}{T_-1})", BRL, True)
    calc(fe[f"F{T_}"], f'=COUNTIFS({rl("I")},{M},{rl("H")},"A conferir no extrato")', b=True)
    for cond, cor in ((f'G{F0}="Fechado"', VERDE), (f'OR(LEFT(G{F0},7)="Confira",G{F0}="Sem lançamentos próprios")', AMAR), (f'G{F0}="Resultado negativo"', VERM)):
        fe.conditional_formatting.add(f"G{F0}:G{T_-1}", FormulaRule(formula=[cond], fill=PatternFill("solid", fgColor=cor)))
    calc(fe["B5"], f'=IF(NOT(ISNUMBER(B3)),"Informe o mês do fechamento",IF(E3=0,"Cadastre os imóveis",IF(B4>0,"Corrija "&B4&" lançamento(s) com problema",'
                   f'IF(F{T_}>0,"Confira no extrato "&F{T_}&" lançamento(s) do mês",IF(COUNTIFS({rl("I")},{M},{rl("J")},1)=0,"Lance as receitas e despesas do mês",'
                   f'IF(COUNTIF(G{F0}:G{T_-1},"Resultado negativo")>0,"Resultado negativo em "&COUNTIF(G{F0}:G{T_-1},"Resultado negativo")&" imóvel(is): reveja as despesas","Mês fechado"))))))', b=True)
    fe.merge_cells("B5:G5"); fe.row_dimensions[5].height = 26
    C0 = T_ + 3
    cab(fe, C0, ["Receitas por canal", "Total no mês"])
    for k, cn in enumerate(CANAIS):
        r = C0 + 1 + k; calc(fe[f"A{r}"], f"=Cadastros!E{K0+k}")
        calc(fe[f"B{r}"], f'=SUMIFS({rl("F")},{rl("C")},"Receita",{rl("D")},A{r},{rl("I")},{M},{rl("J")},1)', BRL)
    G0 = C0 + len(CANAIS) + 3
    cab(fe, G0, ["Despesas por categoria (todos os imóveis)", "Total no mês"])
    for k in range(NK):
        r = G0 + 1 + k; calc(fe[f"A{r}"], f'=IF(Cadastros!C{K0+k}="","",Cadastros!C{K0+k})')
        calc(fe[f"B{r}"], f'=IF(A{r}="","",SUMIFS({rl("F")},{rl("C")},"Despesa",{rl("D")},A{r},{rl("I")},{M},{rl("J")},1))', BRL)
    fe.freeze_panes = "A8"

    # ---------- Ano ----------
    an = wb.create_sheet("Ano"); an.sheet_view.showGridLines = False
    an.column_dimensions["A"].width = 30
    for j in range(2, 15): an.column_dimensions[an.cell(1, j).column_letter].width = 12
    an["A1"] = "Resultado de cada mês"; an["A1"].font = T(18, True, MUSGO)
    an["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Ano do mês escolhido na aba Fechamento. Resultado = receitas − despesas − parte das divididas."
    an["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    an["A3"] = "Ano"; an["A3"].font = T(10, True); calc(an["B3"], "=IF(ISNUMBER(Fechamento!B3),YEAR(Fechamento!B3),YEAR(TODAY()))", "0", True)
    cab(an, 5, ["Imóvel"] + MESES + ["Total"])
    for k in range(NI):
        r = 6 + k; calc(an[f"A{r}"], f"=Fechamento!A{F0+k}")
        for m in range(12):
            c = an.cell(r, 2 + m); mes = f"DATE($B$3,{m+1},1)"
            calc(c, f'=IF($A{r}="","",{soma(f"$A{r}", "Receita", mes)}-{soma(f"$A{r}", "Despesa", mes)}-{div(mes)})', BRL)
        calc(an.cell(r, 14), f'=IF($A{r}="","",SUM(B{r}:M{r}))', BRL, True)
    an[f"A{6+NI}"] = "Total"; an[f"A{6+NI}"].font = T(10, True)
    for j in range(2, 15):
        L = an.cell(1, j).column_letter; calc(an.cell(6 + NI, j), f"=SUM({L}6:{L}{5+NI})", BRL, True)
    an.freeze_panes = "B6"

    wb.active = 0
    nome = "Fechamento-Mensal-Zion-EXEMPLO.xlsx" if exemplo else "Fechamento-Mensal-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

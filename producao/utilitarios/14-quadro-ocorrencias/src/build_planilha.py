"""Gera a Ferramenta 14 · Quadro de Ocorrências e Manutenção (Zion Hospitality Business):
   - Quadro-Ocorrencias-Zion-EM-BRANCO.xlsx / Quadro-Ocorrencias-Zion-EXEMPLO.xlsx (dados fictícios)
Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dados import PRIORIDADES, SIMNAO, EX_UNIDADES, EX_RESP, EX_REF, EX_OC
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
BRL, DATA = 'R$ #,##0.00', "DD/MM/YYYY"
O0, NO = 6, 500          # ocorrências 6..505
U0, NU = 5, 50           # unidades e responsáveis 5..54
P0 = 9                   # prioridades 9..12 na aba Ajustes
VERDE, VERM, AMAR = "C8E6C0", "F4C7C3", "FCE8B2"
d = lambda s: datetime.date.fromisoformat(s) if s else None

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
def lista(ws, rng, opcoes=None, ref=None):
    dv = DataValidation(type="list", formula1=ref or ('"' + ",".join(opcoes) + '"'), allow_blank=True,
                        showErrorMessage=ref is None, errorTitle="Opção inválida", error="Escolha uma opção da lista.")
    ws.add_data_validation(dv); dv.add(rng)

def montar(exemplo):
    wb = Workbook(); ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 104
    linhas = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 14", T(10, True, TERRA)),
        ("Quadro de Ocorrências e Manutenção", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para registrar cada problema da hospedagem com responsável, prioridade e prazo, acompanhar até resolver e saber quais unidades não podem receber hóspede.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (hospedagem, pessoas, datas e custos inventados). Use a versão em branco." if exemplo
         else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Para Airbnb, casas, apartamentos, pousadas e glampings.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 4 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Ajustes: nome da hospedagem e prazo, em dias, para cada prioridade (os números que vêm preenchidos são só um ponto de partida: ajuste à sua realidade).", None),
        ("2. Aba Cadastros: escreva suas unidades e quem resolve (equipe, prestadores).", None),
        ("3. Aba Ocorrências: uma linha por problema. Data, unidade, o que aconteceu, prioridade, responsável e se ele impede receber hóspede. Quando resolver, preencha a data, como foi resolvido e o custo.", None),
        ("4. Aba Painel: veja o que está aberto e atrasado por unidade e por responsável, e quais unidades estão BLOQUEADAS.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("COMO A PLANILHA DECIDE", T(12, True, MUSGO)),
        ("Prazo: o que você digitar; se ficar em branco, data de abertura + dias da prioridade. Atrasada: aberta com prazo antes da data de referência (hoje, se você não informar outra).", None),
        ("Fechada exige data de resolução; sem a descrição de como foi resolvido, aparece \"Fechada sem descrição\". Ocorrência sem unidade, prioridade, responsável ou data aparece como \"Complete os dados\".", None),
        ("Unidade BLOQUEADA = tem ao menos uma ocorrência aberta marcada como \"Bloqueia a unidade\". A planilha mostra; a decisão de liberar continua sendo sua.", None),
        ("", None),
        ("O QUE A PLANILHA NÃO FAZ", T(12, True, MUSGO)),
        ("Não avisa ninguém sozinha, não substitui o técnico nem normas de segurança (gás, elétrica, piscina, estrutura). Problema com risco à segurança: interrompa o uso e chame um profissional habilitado.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Lógica inspirada na rotina de manutenção usada nas unidades da Zion. Material educativo.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    a = wb.create_sheet("Ajustes"); a.sheet_view.showGridLines = False
    for col, w in zip("ABC", (36, 18, 60)): a.column_dimensions[col].width = w
    a["A1"] = "Ajustes"; a["A1"].font = T(18, True, MUSGO)
    for l, r, h in ((4, "Nome da hospedagem", ""), (5, "Data de referência (opcional)", "Em branco = hoje. Serve para saber o que está atrasado."), (6, "Data usada", "Calculado.")):
        a.cell(l, 1, r).font = T(11); a.cell(l, 3, h).font = T(9, c="5F5F55", i=True)
    ent(a["B4"], "Pousada Exemplo (fictícia)" if exemplo else None)
    ent(a["B5"], d(EX_REF) if exemplo else None, DATA)
    calc(a["B6"], '=IF(ISNUMBER(B5),B5,TODAY())', DATA)
    cab(a, 8, ["Prioridade", "Dias até o prazo", "Como usar"])
    usos = ["Impede receber hóspede ou traz risco: resolver no mesmo dia", "Atrapalha a estadia", "Incomoda, mas não impede", "Melhoria ou estética"]
    for i, ((p, dias), u) in enumerate(zip(PRIORIDADES, usos)):
        a.cell(P0 + i, 1, p).font = T(10, True); ent(a.cell(P0 + i, 2), dias); a.cell(P0 + i, 3, u).font = T(9, c="5F5F55", i=True)

    c = wb.create_sheet("Cadastros"); c.sheet_view.showGridLines = False
    for col, w in zip("ABC", (28, 4, 32)): c.column_dimensions[col].width = w
    c["A1"] = "Unidades e responsáveis"; c["A1"].font = T(18, True, MUSGO)
    c["A3"] = "Unidades"; c["A3"].font = T(11, True, MUSGO); c["C3"] = "Quem resolve (equipe e prestadores)"; c["C3"].font = T(11, True, MUSGO)
    for i in range(NU):
        ent(c[f"A{U0+i}"], EX_UNIDADES[i] if exemplo and i < len(EX_UNIDADES) else None)
        ent(c[f"C{U0+i}"], EX_RESP[i] if exemplo and i < len(EX_RESP) else None)

    o = wb.create_sheet("Ocorrências"); o.sheet_view.showGridLines = False
    larg = (5, 12, 14, 18, 30, 11, 20, 12, 12, 11, 18, 12, 26, 11, 18, 9)
    for j, w in enumerate(larg, 1): o.column_dimensions[chr(64 + j)].width = w
    o["A1"] = "Ocorrências"; o["A1"].font = T(18, True, MUSGO)
    o["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Uma linha por problema. Feche com a data de resolução."; o["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    cab(o, 5, ["Nº", "Aberta em", "Unidade", "Local ou equipamento", "O que aconteceu", "Prioridade", "Responsável", "Prazo (opcional)", "Prazo usado",
               "Bloqueia a unidade?", "Evidência (foto ou link)", "Resolvida em", "Como foi resolvido", "Custo (R$)", "Situação", "Dias"])
    REF = "Ajustes!$B$6"
    for r in range(O0, O0 + NO):
        calc(o[f"A{r}"], f'=IF(E{r}="","",ROW()-{O0-1})')
        for col in "BCDEFGHJKLMN": ent(o[f"{col}{r}"], None, DATA if col in "BHL" else BRL if col == "N" else None)
        calc(o[f"I{r}"], f'=IF(E{r}="","",IF(ISNUMBER(H{r}),H{r},IF(AND(ISNUMBER(B{r}),F{r}<>""),B{r}+IFERROR(VLOOKUP(F{r},Ajustes!$A${P0}:$B${P0+3},2,0),0),"")))', DATA)
        calc(o[f"O{r}"], f'=IF(E{r}="","",IF(AND(ISNUMBER(L{r}),ISNUMBER(B{r}),L{r}<B{r}),"Confira as datas",IF(ISNUMBER(L{r}),IF(M{r}="","Fechada sem descrição","Fechada"),'
                         f'IF(OR(C{r}="",F{r}="",G{r}="",NOT(ISNUMBER(B{r}))),"Complete os dados",IF(AND(ISNUMBER(I{r}),I{r}<{REF}),"Atrasada","Aberta")))))', b=True)
        calc(o[f"P{r}"], f'=IF(OR(E{r}="",NOT(ISNUMBER(B{r}))),"",IF(ISNUMBER(L{r}),L{r}-B{r},{REF}-B{r}))')
    rg = lambda col: f"{col}{O0}:{col}{O0+NO-1}"
    lista(o, rg("C"), ref=f"Cadastros!$A${U0}:$A${U0+NU-1}"); lista(o, rg("G"), ref=f"Cadastros!$C${U0}:$C${U0+NU-1}")
    lista(o, rg("F"), [p for p, _ in PRIORIDADES]); lista(o, rg("J"), SIMNAO)
    for cond, cor in ((f'O{O0}="Atrasada"', VERM), (f'O{O0}="Aberta"', AMAR), (f'LEFT(O{O0},7)="Fechada"', VERDE), (f'OR(O{O0}="Complete os dados",O{O0}="Confira as datas")', VERM)):
        o.conditional_formatting.add(rg("O"), FormulaRule(formula=[cond], fill=PatternFill("solid", fgColor=cor)))
    o.freeze_panes = f"C{O0}"
    o.page_setup.orientation = "landscape"; o.page_setup.fitToWidth = 1; o.page_setup.fitToHeight = 0; o.sheet_properties.pageSetUpPr.fitToPage = True
    if exemplo:
        for k, row in enumerate(EX_OC):
            r = O0 + k; ab, un, loc, oq, pr, resp, prazo, bl, ev, res, como, custo = row
            for col, v in zip("BCDEFGHJKLMN", (d(ab), un, loc, oq, pr, resp, d(prazo), bl, ev, d(res), como, custo)): o[f"{col}{r}"].value = v

    p = wb.create_sheet("Painel"); p.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHIJK", (24, 10, 10, 12, 10, 12, 14, 3, 26, 10, 10)): p.column_dimensions[col].width = w
    p["A1"] = '=IF(Ajustes!B4="","Painel","Painel · "&Ajustes!B4)'; p["A1"].font = T(18, True, MUSGO)
    p["A2"] = '="Situação em "&RIGHT("0"&DAY(Ajustes!B6),2)&"/"&RIGHT("0"&MONTH(Ajustes!B6),2)&"/"&YEAR(Ajustes!B6)'; p["A2"].font = T(10, c="5F5F55", i=True)
    oc = lambda col: f"Ocorrências!${col}${O0}:${col}${O0+NO-1}"
    ab = lambda extra: "+".join(f'COUNTIFS({extra}{oc("O")},"{s}")' for s in ("Aberta", "Atrasada", "Complete os dados"))
    resumo = [("A3", "Abertas", "B3", "=" + ab("")), ("C3", "Atrasadas", "D3", f'=COUNTIF({oc("O")},"Atrasada")'),
              ("E3", "Unidades bloqueadas", "G3", '=COUNTIF(G7:G56,"BLOQUEADA")'), ("A4", "A completar", "B4", f'=COUNTIF({oc("O")},"Complete os dados")+COUNTIF({oc("O")},"Confira as datas")'),
              ("C4", "Custo total", "D4", f'=SUM({oc("N")})')]
    for a1, t, b1, f in resumo:
        p[a1] = t; p[a1].font = T(10, True); calc(p[b1], f, BRL if "Custo" in t else None, True)
    cab(p, 6, ["Unidade", "Abertas", "Atrasadas", "Bloqueando", "Fechadas", "Custo (R$)", "Situação"])
    for i in range(NU):
        r, u = 7 + i, f"Cadastros!$A${U0+i}"
        calc(p[f"A{r}"], f'=IF({u}="","",{u}&"")')
        crit = lambda extra="": f'{oc("C")},A{r},{extra}'
        calc(p[f"B{r}"], f'=IF(A{r}="","",' + "+".join(f'COUNTIFS({oc("C")},A{r},{oc("O")},"{s}")' for s in ("Aberta", "Atrasada", "Complete os dados")) + ")")
        calc(p[f"C{r}"], f'=IF(A{r}="","",COUNTIFS({oc("C")},A{r},{oc("O")},"Atrasada"))')
        calc(p[f"D{r}"], f'=IF(A{r}="","",' + "+".join(f'COUNTIFS({oc("C")},A{r},{oc("J")},"Sim",{oc("O")},"{s}")' for s in ("Aberta", "Atrasada", "Complete os dados")) + ")")
        calc(p[f"E{r}"], f'=IF(A{r}="","",COUNTIFS({oc("C")},A{r},{oc("O")},"Fechada")+COUNTIFS({oc("C")},A{r},{oc("O")},"Fechada sem descrição"))')
        calc(p[f"F{r}"], f'=IF(A{r}="","",SUMIFS({oc("N")},{oc("C")},A{r}))', BRL)
        calc(p[f"G{r}"], f'=IF(A{r}="","",IF(D{r}>0,"BLOQUEADA","Liberada"))', b=True)
    p.conditional_formatting.add("G7:G56", FormulaRule(formula=['G7="BLOQUEADA"'], fill=PatternFill("solid", fgColor=VERM)))
    p.conditional_formatting.add("G7:G56", FormulaRule(formula=['G7="Liberada"'], fill=PatternFill("solid", fgColor=VERDE)))
    for j, t in enumerate(["Responsável", "Abertas", "Atrasadas"]):
        cc = p.cell(6, 9 + j, t); cc.font = T(10, True, CREME); cc.fill = CAB; cc.alignment = WRAP; cc.border = borda
    for i in range(NU):
        r, rs = 7 + i, f"Cadastros!$C${U0+i}"
        calc(p[f"I{r}"], f'=IF({rs}="","",{rs}&"")')
        calc(p[f"J{r}"], f'=IF(I{r}="","",' + "+".join(f'COUNTIFS({oc("G")},I{r},{oc("O")},"{s}")' for s in ("Aberta", "Atrasada")) + ")")
        calc(p[f"K{r}"], f'=IF(I{r}="","",COUNTIFS({oc("G")},I{r},{oc("O")},"Atrasada"))')
    p.freeze_panes = "A7"

    wb.active = 0
    nome = "Quadro-Ocorrencias-Zion-EXEMPLO.xlsx" if exemplo else "Quadro-Ocorrencias-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

"""Gera a Ferramenta 22 · Planner de Campanhas para Períodos de Baixa Procura (Zion Hospitality Business):
   - Campanhas-Baixa-Procura-Zion-EM-BRANCO.xlsx / Campanhas-Baixa-Procura-Zion-EXEMPLO.xlsx (dados fictícios)
Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dados import TIPOS, CANAIS, SITUACOES, EX_BASE, EX_PER, EX_CAMP
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
P0, NP = 6, 20         # períodos: linhas 6..25
C0, NC = 7, 60         # campanhas: linhas 7..66
VERDE, VERM, AMAR = "C8E6C0", "F4C7C3", "FCE8B2"
d = lambda s: datetime.date.fromisoformat(s) if s else None

def cab(ws, l, tit):
    for j, t in enumerate(tit, 1):
        c = ws.cell(l, j, t); c.font = T(10, True, CREME); c.fill = CAB; c.alignment = WRAP; c.border = borda
    ws.row_dimensions[l].height = 46
def ent(c, v=None, fmt=None):
    c.value = v; c.fill = ENTRADA; c.border = borda; c.alignment = WRAP; c.font = T(10)
    if fmt: c.number_format = fmt
def calc(c, f, fmt=None, b=False):
    c.value = f; c.fill = CALC; c.border = borda; c.alignment = WRAP; c.font = T(10, b)
    if fmt: c.number_format = fmt
def lista(ws, rng, opcoes=None, ref=None):
    dv = DataValidation(type="list", formula1=ref or ('"' + ",".join(opcoes) + '"'), allow_blank=True, showErrorMessage=True,
                        errorTitle="Opção inválida", error="Escolha uma opção da lista.")
    ws.add_data_validation(dv); dv.add(rng)

def montar(exemplo):
    wb = Workbook(); ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 104
    linhas = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 22", T(10, True, TERRA)),
        ("Planner de Campanhas para Períodos de Baixa Procura", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para encontrar os períodos fracos da sua hospedagem, planejar campanhas sem vender abaixo do piso e acompanhar o que cada campanha trouxe.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (chalés, datas, diárias e resultados inventados; não servem como referência). Use a versão em branco." if exemplo
         else "Versão em branco. Preencha as células amarelas, começando pela aba Base.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Para Airbnb, casas, apartamentos, pousadas e glampings.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 4 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Base: unidades, diária normal, piso da diária (se ainda não tem, calcule com a Planilha Diária Mínima ou com a sua conta de custos), taxas e impostos, custo variável por estadia e a sua meta de ocupação.", None),
        ("2. Aba Períodos: liste os períodos que costumam ficar vazios, com o primeiro e o último dia (noite) e quantas noites já estão reservadas. A planilha mostra a ocupação e quais estão abaixo da meta.", None),
        ("3. Aba Campanhas: para cada período fraco, planeje uma ou mais campanhas (tipo, desconto, estadia mínima, canal, datas, responsável). A planilha confere se a diária com desconto fica acima do piso e se cobre o custo da estadia.", None),
        ("4. Depois que a campanha rodar, anote as noites vendidas por ela. O Painel mostra o que falta planejar e o que cada campanha trouxe.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("COMO A PLANILHA DECIDE", T(12, True, MUSGO)),
        ("Noites disponíveis do período = (último dia − primeiro dia + 1) × unidades. Ocupação = noites reservadas ÷ disponíveis. Abaixo da meta quando a ocupação é menor que a meta da aba Base.", None),
        ("Diária com desconto = diária normal × (1 − desconto). Líquido por noite = diária com desconto × (1 − taxas e impostos) − custo variável por estadia ÷ estadia mínima (vazia = 1 noite).", None),
        ("Alerta da campanha: Abaixo do piso quando a diária com desconto é menor que o piso; Não cobre o custo quando o líquido por noite é zero ou negativo; Começa depois do período ou Termina antes do período quando as datas não cobrem o período.", None),
        ("", None),
        ("O QUE A PLANILHA NÃO FAZ", T(12, True, MUSGO)),
        ("Não prevê demanda, não garante reservas e não publica nada. Faturamento não é lucro. Antes de dar desconto, confira as regras e as taxas da sua plataforma.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Base ----------
    b = wb.create_sheet("Base"); b.sheet_view.showGridLines = False
    b.column_dimensions["A"].width = 48; b.column_dimensions["B"].width = 16; b.column_dimensions["C"].width = 50
    b["A1"] = "Base da hospedagem"; b["A1"].font = T(18, True, MUSGO)
    b["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Preencha antes das outras abas."; b["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    cab(b, 4, ["Dado", "Valor", "Para que serve"])
    itens = [("Unidades à venda", "unidades", None, "Multiplica as noites de cada período"),
             ("Diária normal (média)", "diaria", BRL, "Base do desconto"),
             ("Piso da diária", "piso", BRL, "Abaixo dele, a campanha recebe alerta. Use a Planilha Diária Mínima ou a sua conta"),
             ("Taxas e impostos sobre a diária", "taxa", PCT, "Plataforma, cartão e impostos, em % da diária"),
             ("Custo variável por estadia", "custo", BRL, "Limpeza, lavanderia, amenities de cada estadia"),
             ("Meta de ocupação dos períodos", "meta", PCT, "Decisão sua: abaixo dela, o período é fraco")]
    REF = {}
    for i, (rot, k, fmt, para) in enumerate(itens):
        r = 5 + i; b[f"A{r}"] = rot; b[f"A{r}"].font = T(10, True); ent(b[f"B{r}"], EX_BASE[k] if exemplo else None, fmt); b[f"C{r}"] = para
        b[f"C{r}"].font = T(9, c="5F5F55", i=True); REF[k] = f"Base!$B${r}"
    r = 12; b[f"A{r}"] = "Situação da base"; b[f"A{r}"].font = T(10, True)
    calc(b[f"B{r}"], f'=IF(OR(NOT(ISNUMBER(B5)),B5<1),"Informe as unidades",IF(OR(NOT(ISNUMBER(B6)),B6<=0),"Informe a diária normal",'
                     f'IF(AND(ISNUMBER(B8),OR(B8<0,B8>=1)),"Taxas entre 0% e 99%",IF(AND(ISNUMBER(B10),OR(B10<0,B10>1)),"Meta entre 0% e 100%","OK"))))', b=True)
    b.merge_cells("B12:C12")
    BASE_OK = "Base!$B$12"

    # ---------- Períodos ----------
    pe = wb.create_sheet("Períodos"); pe.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHI", (28, 12, 12, 12, 12, 11, 24, 12, 14)): pe.column_dimensions[col].width = w
    pe["A1"] = "Períodos de baixa procura"; pe["A1"].font = T(18, True, MUSGO)
    pe["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Liste os períodos que costumam ficar vazios. Último dia = última noite do período."
    pe["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    cab(pe, 5, ["Período", "Primeiro dia", "Último dia (noite)", "Noites reservadas", "Noites disponíveis", "Ocupação", "Situação", "Campanhas sem alerta", "Noites vendidas pelas campanhas"])
    rgCA, rgCK, rgCJ = f"Campanhas!$A${C0}:$A${C0+NC-1}", f"Campanhas!$P${C0}:$P${C0+NC-1}", f"Campanhas!$K${C0}:$K${C0+NC-1}"
    for k in range(NP):
        r = P0 + k; v = EX_PER[k] if exemplo and k < len(EX_PER) else (None,) * 4
        ent(pe[f"A{r}"], v[0]); ent(pe[f"B{r}"], d(v[1]), DATA); ent(pe[f"C{r}"], d(v[2]), DATA); ent(pe[f"D{r}"], v[3])
        datas_ok = f"AND(ISNUMBER(B{r}),ISNUMBER(C{r}),C{r}>=B{r})"
        calc(pe[f"E{r}"], f'=IF(OR(A{r}="",NOT({datas_ok}),NOT(ISNUMBER({REF["unidades"]})),N({REF["unidades"]})<1),"",(C{r}-B{r}+1)*{REF["unidades"]})')
        calc(pe[f"F{r}"], f'=IF(OR(E{r}="",NOT(ISNUMBER(D{r}))),"",D{r}/E{r})', PCT)
        calc(pe[f"G{r}"], f'=IF(A{r}="","",IF(NOT({datas_ok}),"Confira as datas",IF(OR(NOT(ISNUMBER({REF["unidades"]})),N({REF["unidades"]})<1),"Preencha a aba Base",'
                          f'IF(OR(NOT(ISNUMBER(D{r})),D{r}<0),"Informe as noites reservadas",IF(D{r}>E{r},"Reservadas maior que disponíveis",'
                          f'IF(NOT(ISNUMBER({REF["meta"]})),"Defina a meta na aba Base",IF(F{r}<{REF["meta"]},"Abaixo da meta","Na meta ou acima")))))))', b=True)
        calc(pe[f"H{r}"], f'=IF(A{r}="","",COUNTIFS({rgCA},A{r},{rgCK},"OK"))')
        calc(pe[f"I{r}"], f'=IF(A{r}="","",SUMIFS({rgCJ},{rgCA},A{r},{rgCK},"OK"))')
    rgG = f"G{P0}:G{P0+NP-1}"
    for cond, cor in ((f'G{P0}="Abaixo da meta"', AMAR), (f'G{P0}="Na meta ou acima"', VERDE),
                      (f'AND(G{P0}<>"",G{P0}<>"Abaixo da meta",G{P0}<>"Na meta ou acima")', VERM)):
        pe.conditional_formatting.add(rgG, FormulaRule(formula=[cond], fill=PatternFill("solid", fgColor=cor)))
    pe.freeze_panes = f"B{P0}"
    PER = f"Períodos!$A${P0}:$A${P0+NP-1}"

    # ---------- Campanhas ----------
    ca = wb.create_sheet("Campanhas"); ca.sheet_view.showGridLines = False
    larg = (26, 20, 10, 10, 18, 12, 12, 16, 12, 10, 10, 13, 13, 13, 16, 26)
    for j, w in enumerate(larg, 1): ca.column_dimensions[ca.cell(1, j).column_letter].width = w
    ca["A1"] = "Campanhas"; ca["A1"].font = T(18, True, MUSGO)
    ca["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Uma linha por campanha. Desconto em % (0% para pacote sem desconto)."
    ca["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    ca["A3"] = "Campanhas com alerta:"; ca["A3"].font = T(10, True)
    rgP = f"P{C0}:P{C0+NC-1}"
    calc(ca["D3"], f'=COUNTIF({rgP},"?*")-COUNTIF({rgP},"OK")', b=True)
    cab(ca, 6, ["Período", "Tipo", "Desconto", "Estadia mínima (noites)", "Canal", "Começa em", "Termina em", "Responsável", "Situação", "", "Noites vendidas (depois)",
                "Diária com desconto", "Líquido por noite", "Faturamento bruto atribuído", "", "Alerta"])
    ca.column_dimensions["J"].hidden = True; ca.column_dimensions["O"].hidden = True
    for k in range(NC):
        r = C0 + k; v = EX_CAMP[k] if exemplo and k < len(EX_CAMP) else (None,) * 10
        for col, x, fmt in zip("ABCDEFGHIK", (v[0], v[1], v[2], v[3], v[4], d(v[5]), d(v[6]), v[7], v[8], v[9]),
                               (None, None, PCT, None, None, DATA, DATA, None, None, None)):
            ent(ca[f"{col}{r}"], x, fmt)
        estmin = f"IF(ISNUMBER(D{r}),D{r},1)"
        calc(ca[f"L{r}"], f'=IF(OR(P{r}="",LEFT(P{r},7)="Confira",P{r}="Período não cadastrado",P{r}="Escolha o tipo",LEFT(P{r},8)="Preencha"),"",{REF["diaria"]}*(1-C{r}))', BRL)
        calc(ca[f"M{r}"], f'=IF(L{r}="","",L{r}*(1-N({REF["taxa"]}))-N({REF["custo"]})/{estmin})', BRL)
        calc(ca[f"N{r}"], f'=IF(OR(P{r}<>"OK",NOT(ISNUMBER(K{r}))),"",K{r}*L{r})', BRL)
        ini = f"INDEX(Períodos!$B${P0}:$B${P0+NP-1},MATCH(A{r},{PER},0))"; fim = f"INDEX(Períodos!$C${P0}:$C${P0+NP-1},MATCH(A{r},{PER},0))"
        dc = f"(N({REF['diaria']})*(1-C{r}))"
        lq = f"({dc}*(1-N({REF['taxa']}))-N({REF['custo']})/{estmin})"
        calc(ca[f"P{r}"], f'=IF(AND(A{r}="",B{r}="",C{r}=""),"",IF(OR(A{r}="",COUNTIF({PER},A{r})=0),"Período não cadastrado",IF(B{r}="","Escolha o tipo",'
                          f'IF({BASE_OK}<>"OK","Preencha a aba Base",IF(OR(NOT(ISNUMBER(C{r})),C{r}<0,C{r}>=1),"Confira o desconto",'
                          f'IF(AND(D{r}<>"",OR(NOT(ISNUMBER(D{r})),D{r}<1)),"Confira a estadia mínima",'
                          f'IF(OR(NOT(ISNUMBER(F{r})),NOT(ISNUMBER(G{r}))),"Confira as datas",IF(F{r}>G{r},"Confira as datas",'
                          f'IF(AND(ISNUMBER({REF["piso"]}),{dc}<{REF["piso"]}),"Abaixo do piso",IF({lq}<=0,"Não cobre o custo",'
                          f'IF(AND(ISNUMBER({ini}),G{r}<{ini}),"Termina antes do período",IF(AND(ISNUMBER({fim}),F{r}>{fim}),"Começa depois do período","OK"))))))))))))', b=True)
    lista(ca, f"A{C0}:A{C0+NC-1}", ref=PER); lista(ca, f"B{C0}:B{C0+NC-1}", TIPOS); lista(ca, f"E{C0}:E{C0+NC-1}", CANAIS); lista(ca, f"I{C0}:I{C0+NC-1}", SITUACOES)
    ca.conditional_formatting.add(rgP, FormulaRule(formula=[f'P{C0}="OK"'], fill=PatternFill("solid", fgColor=VERDE)))
    ca.conditional_formatting.add(rgP, FormulaRule(formula=[f'AND(P{C0}<>"",P{C0}<>"OK")'], fill=PatternFill("solid", fgColor=VERM)))
    ca.freeze_panes = f"B{C0}"

    # ---------- Painel ----------
    p = wb.create_sheet("Painel"); p.sheet_view.showGridLines = False
    p.column_dimensions["A"].width = 52; p.column_dimensions["B"].width = 18
    p["A1"] = "Painel das campanhas"; p["A1"].font = T(18, True, MUSGO)
    p["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Tudo calculado."; p["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    pr = lambda c: f"Períodos!${c}${P0}:${c}${P0+NP-1}"; cr = lambda c: f"Campanhas!${c}${C0}:${c}${C0+NC-1}"
    itens = [("Situação da base", f"={BASE_OK}", None),
             ("Períodos cadastrados", f'=COUNTIF({pr("A")},"?*")', None),
             ("Períodos abaixo da meta", f'=COUNTIF({pr("G")},"Abaixo da meta")', None),
             ("Abaixo da meta e sem campanha sem alerta", f'=COUNTIFS({pr("G")},"Abaixo da meta",{pr("H")},0)', None),
             ("Campanhas planejadas", f'=COUNTIF({cr("P")},"?*")', None),
             ("Campanhas com alerta", "=Campanhas!D3", None),
             ("Campanhas no ar (sem alerta)", f'=COUNTIFS({cr("I")},"No ar",{cr("P")},"OK")', None),
             ("Noites vendidas pelas campanhas", f'=SUMIFS({cr("K")},{cr("P")},"OK")', None),
             ("Faturamento bruto atribuído (não é lucro)", f'=SUM({cr("N")})', BRL)]
    for i, (rot, f, fmt) in enumerate(itens):
        r = 4 + i; p[f"A{r}"] = rot; p[f"A{r}"].font = T(10, True); calc(p[f"B{r}"], f, fmt, True)
    p["A14"] = "O que fazer agora"; p["A14"].font = T(12, True, MUSGO)
    calc(p["A15"], '=IF(B4<>"OK","Preencha a aba Base: "&B4,IF(B5=0,"Liste os períodos de baixa procura",IF(B9>0,"Corrija as campanhas com alerta",'
                   'IF(B7>0,"Planeje campanha para "&B7&" período(s) abaixo da meta",IF(B10=0,"Coloque no ar as campanhas planejadas","Acompanhe as campanhas no ar e anote as noites vendidas")))))', b=True)
    p.merge_cells("A15:B15"); p.row_dimensions[15].height = 30

    wb.active = 0
    nome = "Campanhas-Baixa-Procura-Zion-EXEMPLO.xlsx" if exemplo else "Campanhas-Baixa-Procura-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

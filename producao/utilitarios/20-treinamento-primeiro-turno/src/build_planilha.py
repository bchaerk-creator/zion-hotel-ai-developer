"""Gera a Ferramenta 20 · Kit de Treinamento do Primeiro Turno (Zion Hospitality Business):
   - Treinamento-Primeiro-Turno-Zion-EM-BRANCO.xlsx (lista sugerida, sem datas)
   - Treinamento-Primeiro-Turno-Zion-EXEMPLO.xlsx (dados fictícios)
Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dados import ETAPAS, SUGERIDAS, EX, EX_DATAS, NT, T0
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, PRETO, CREME, TERRA = "1B2117", "040605", "FEF5F0", "8B714E"
ENTRADA, CALC, CAB = PatternFill("solid", fgColor="FFF4C7"), PatternFill("solid", fgColor="E3EEDF"), PatternFill("solid", fgColor=MUSGO)
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)
WRAP = Alignment(wrap_text=True, vertical="center")
DATA = "DD/MM/YYYY"
VERDE, VERM, AMAR, CINZA, AZUL = "C8E6C0", "F4C7C3", "FCE8B2", "E6E6E6", "D6E4F0"
d = lambda s: datetime.date.fromisoformat(s) if s else None
TF = T0 + NT - 1
R = lambda c: f"Treinamento!${c}${T0}:${c}${TF}"
SIT_CONF = ("Datas fora de ordem: confira", "Data futura: confira", "Falta quem conferiu")

def ent(c, v=None, fmt=None, b=False):
    c.value = v; c.fill = ENTRADA; c.border = borda; c.alignment = WRAP; c.font = T(10, b)
    if fmt: c.number_format = fmt
def calc(c, f, fmt=None, b=False, sz=10):
    c.value = f; c.fill = CALC; c.border = borda; c.alignment = WRAP; c.font = T(sz, b)
    if fmt: c.number_format = fmt
def cab(ws, l, tit):
    for j, t in enumerate(tit, 1):
        c = ws.cell(l, j, t); c.font = T(9, True, CREME); c.fill = CAB; c.border = borda
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ws.row_dimensions[l].height = 44

def comece(wb, exemplo):
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False; ws.column_dimensions["A"].width = 108
    L = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 20", T(10, True, TERRA)),
        ("Kit de Treinamento do Primeiro Turno", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para treinar a primeira pessoa da sua equipe: o que mostrar, o que fazer junto, quando ela pode trabalhar sozinha e quem conferiu cada tarefa.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (pessoas, datas e hospedagem inventadas). Use a versão em branco." if exemplo
         else "Versão em branco, com uma lista sugerida de tarefas. Ajuste à sua hospedagem e à função da pessoa.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Para Airbnb, casas, apartamentos, pousadas e glampings.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 5 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Treinamento, topo: nome da pessoa, função, data de início, quem treina e a data de hoje (já vem com HOJE()).", None),
        ("2. Revise a lista: as seis etapas partem da trilha de onboarding usada nas unidades da Zion. Marque o que é obrigatório e em quantos dias cada tarefa deve estar pronta.", None),
        ("3. Cada tarefa passa por três passos, sempre nesta ordem: Mostrado (você faz, a pessoa vê), Feito junto (ela faz, você do lado) e Fez sozinha e conferido (ela faz, você confere no fim).", None),
        ("4. Anote a data de cada passo e quem conferiu. A situação de cada tarefa se calcula sozinha.", None),
        ("5. Abra o Painel: quantas obrigatórias faltam, o que está atrasado e se a pessoa já pode fazer o turno sozinha.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("AS REGRAS", T(12, True, MUSGO)),
        ("Prazo = data de início + dias. Situação: Pronta (os três passos com data e quem conferiu), Feita junto, Mostrada, Não começou, Atrasada (não está pronta e o prazo passou).", None),
        ("Liberada para o turno sozinha = todas as tarefas obrigatórias prontas. Conferências: datas fora de ordem, data no futuro e tarefa pronta sem o nome de quem conferiu.", None),
        ("", None),
        ("O QUE A PLANILHA NÃO FAZ", T(12, True, MUSGO)),
        ("Não substitui contrato, registro, exames, treinamentos obrigatórios por lei nem orientação do contador ou do advogado. Não avalia a pessoa: registra o que foi ensinado e conferido.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(L, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

def treinamento(wb, exemplo):
    t = wb.create_sheet("Treinamento"); t.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHIJKLM", (5, 24, 38, 10, 9, 13, 13, 13, 13, 14, 26, 13, 22)): t.column_dimensions[col].width = w
    t["A1"] = "Plano de treinamento"; t["A1"].font = T(18, True, MUSGO)
    t["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Preencha as células amarelas. A lista é uma sugestão."; t["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    campos = [(4, "Pessoa em treinamento", "pessoa", None), (5, "Função", "funcao", None), (6, "Data de início", "inicio", DATA),
              (7, "Quem treina", "treina", None), (8, "Data de hoje", "hoje", DATA)]
    for l, rot, k, fmt in campos:
        t.merge_cells(start_row=l, start_column=1, end_row=l, end_column=2); t.cell(l, 1, rot).font = T(11, True)
        v = (d(EX[k]) if fmt else EX[k]) if exemplo else ("=TODAY()" if k == "hoje" else None)
        ent(t.cell(l, 3), v, fmt, True)
    t.merge_cells("D4:M8"); t["D4"] = ("Ordem dos passos: Mostrado (você faz, a pessoa vê) → Feito junto (ela faz, você do lado) → Fez sozinha e conferido "
                                       "(ela faz, você confere no fim). A trilha de seis etapas parte do onboarding usado nas unidades da Zion.")
    t["D4"].font = T(9, c="5F5F55", i=True); t["D4"].alignment = WRAP
    t.row_dimensions[9].height = 44
    for j, h in enumerate(["Nº", "Etapa", "Tarefa", "Obriga-tória", "Prazo (dias)", "Mostrado em", "Feito junto em", "Fez sozinha e conferido em",
                           "Conferido por", "Prazo (data)", "Situação", "Passo atual", "Observação"], 1):
        c = t.cell(9, j, h); c.font = T(9, True, CREME); c.fill = CAB; c.border = borda; c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    for rng, ops in ((f"B{T0}:B{TF}", ETAPAS), (f"D{T0}:D{TF}", ["Sim", "Não"])):
        dv = DataValidation(type="list", formula1='"' + ",".join(ops) + '"', allow_blank=True); t.add_data_validation(dv); dv.add(rng)
    for i in range(NT):
        r = T0 + i
        if i < len(SUGERIDAS):
            e, tarefa, ob, pz = SUGERIDAS[i]; base = [ETAPAS[e - 1], tarefa, ob, pz]
            dts = EX_DATAS[i] if exemplo else (None, None, None, None)
        else:
            base = [None] * 4; dts = (None, None, None, None)
        calc(t[f"A{r}"], i + 1, "0", True)
        for col, v, fmt in zip("BCDE", base, (None, None, None, "0")): ent(t[f"{col}{r}"], v, fmt, col == "C")
        for col, v, fmt in zip("FGHI", (d(dts[0]), d(dts[1]), d(dts[2]), dts[3]), (DATA, DATA, DATA, None)): ent(t[f"{col}{r}"], v, fmt)
        ent(t[f"M{r}"])
        calc(t[f"J{r}"], f'=IF(OR(C{r}="",NOT(ISNUMBER($C$6)),NOT(ISNUMBER(E{r}))),"",$C$6+E{r})', DATA)
        fut = f'AND(ISNUMBER($C$8),OR(N(F{r})>$C$8,N(G{r})>$C$8,N(H{r})>$C$8))'
        ordem = (f'OR(AND(G{r}<>"",F{r}=""),AND(H{r}<>"",OR(F{r}="",G{r}="")),AND(ISNUMBER(F{r}),ISNUMBER(G{r}),G{r}<F{r}),'
                 f'AND(ISNUMBER(G{r}),ISNUMBER(H{r}),H{r}<G{r}))')
        calc(t[f"L{r}"], f'=IF(C{r}="","",IF(ISNUMBER(H{r}),"Fez sozinha",IF(ISNUMBER(G{r}),"Feito junto",IF(ISNUMBER(F{r}),"Mostrado","Nenhum"))))')
        calc(t[f"K{r}"], (f'=IF(C{r}="","",IF({ordem},"Datas fora de ordem: confira",IF({fut},"Data futura: confira",'
                          f'IF(AND(ISNUMBER(H{r}),I{r}=""),"Falta quem conferiu",IF(ISNUMBER(H{r}),"Pronta",'
                          f'IF(AND(ISNUMBER(J{r}),ISNUMBER($C$8),$C$8>J{r}),"Atrasada",IF(ISNUMBER(G{r}),"Feita junto",IF(ISNUMBER(F{r}),"Mostrada","Não começou"))))))))'), None, True)
    rg = f"K{T0}:K{TF}"
    for txt, cor in (("Pronta", VERDE), ("Atrasada", VERM), ("Feita junto", AZUL), ("Mostrada", AMAR), ("Não começou", CINZA)) + tuple((x, VERM) for x in SIT_CONF):
        t.conditional_formatting.add(rg, FormulaRule(formula=[f'K{T0}="{txt}"'], fill=PatternFill("solid", fgColor=cor)))
    t.freeze_panes = f"D{T0}"

def painel(wb):
    s = wb.create_sheet("Painel"); s.sheet_view.showGridLines = False
    s.column_dimensions["A"].width = 46; s.column_dimensions["B"].width = 44
    s["A1"] = "Painel do treinamento"; s["A1"].font = T(18, True, MUSGO)
    s["A2"] = "Tudo calculado a partir da aba Treinamento."; s["A2"].font = T(10, c="5F5F55", i=True)
    K, C, D = R("K"), R("C"), R("D")
    ob_ok = f'SUMPRODUCT(({D}="Sim")*({K}="Pronta"))'
    ob_tot = f'SUMPRODUCT(({D}="Sim")*(LEN({C})>0))'
    lin = [
        (4, "Pessoa", '=IF(Treinamento!C4="","",Treinamento!C4)', None, True),
        (5, "Tarefas no plano", f'=SUMPRODUCT(--(LEN({C})>0))', "0", False),
        (6, "Tarefas prontas", f'=COUNTIF({K},"Pronta")', "0", False),
        (7, "Obrigatórias", f'={ob_tot}', "0", False),
        (8, "Obrigatórias prontas", f'={ob_ok}', "0", True),
        (9, "Obrigatórias que faltam", "=B7-B8", "0", True),
        (10, "Pronto (% das obrigatórias)", '=IF(B7=0,"",B8/B7)', "0%", True),
        (11, "Atrasadas", f'=COUNTIF({K},"Atrasada")', "0", True),
        (12, "Linhas para conferir", "=" + "+".join(f'COUNTIF({K},"{x}")' for x in SIT_CONF), "0", False),
        (13, "Próxima tarefa (primeira não pronta, na ordem)",
         f'=IFERROR(INDEX({C},MATCH(1,INDEX((LEN({C})>0)*({K}<>"Pronta"),0),0)),"")', None, False),
        (14, "Liberada para o turno sozinha?",
         '=IF(B5=0,"Monte o plano na aba Treinamento",IF(B7=0,"Marque quais tarefas são obrigatórias",IF(B12>0,"Ainda não: há linhas para conferir",'
         'IF(B9=0,"Sim: todas as obrigatórias prontas","Ainda não: faltam "&B9&" obrigatórias"))))', None, True),
    ]
    for l, rot, f, fmt, b in lin:
        s.cell(l, 1, rot).font = T(11, b); s.cell(l, 1).alignment = WRAP; calc(s.cell(l, 2), f, fmt, b, 12 if b else 10)
    s.conditional_formatting.add("B14", FormulaRule(formula=['LEFT(B14,3)="Sim"'], fill=PatternFill("solid", fgColor=VERDE)))
    s.conditional_formatting.add("B14", FormulaRule(formula=['LEFT(B14,3)<>"Sim"'], fill=PatternFill("solid", fgColor=AMAR)))
    s.conditional_formatting.add("B11", FormulaRule(formula=['B11>0'], fill=PatternFill("solid", fgColor=VERM)))
    s["A16"] = "Por etapa"; s["A16"].font = T(12, True, MUSGO)
    for j, h in enumerate(["Etapa", "Tarefas · prontas"], 1):
        c = s.cell(17, j, h); c.font = T(9, True, CREME); c.fill = CAB; c.border = borda
    for i, e in enumerate(ETAPAS):
        r = 18 + i; c = s.cell(r, 1, e); c.font = T(10); c.border = borda
        calc(s.cell(r, 2), f'=COUNTIFS({R("B")},A{r},{R("C")},"<>")&" · "&COUNTIFS({R("B")},A{r},{K},"Pronta")')

def montar(exemplo):
    wb = Workbook(); comece(wb, exemplo); treinamento(wb, exemplo); painel(wb); wb.active = 0
    nome = "Treinamento-Primeiro-Turno-Zion-EXEMPLO.xlsx" if exemplo else "Treinamento-Primeiro-Turno-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

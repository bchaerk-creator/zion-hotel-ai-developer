"""Gera a Ferramenta 18 · Planner de Manutenção Preventiva (Zion Hospitality Business):
   - Manutencao-Preventiva-Zion-EM-BRANCO.xlsx (lista sugerida, sem datas)
   - Manutencao-Preventiva-Zion-EXEMPLO.xlsx (dados fictícios)
Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dados import FREQ, SUGERIDAS, EX_HOJE, EX_AVISO, EX_PLANO, EX_REG, NP, P0, NR, R0
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
BRL, DATA = 'R$ #,##0.00', "DD/MM/YYYY"
VERDE, VERM, AMAR, CINZA = "C8E6C0", "F4C7C3", "FCE8B2", "E6E6E6"
d = lambda s: datetime.date.fromisoformat(s) if s else None
PF = P0 + NP - 1; RF = R0 + NR - 1
RP = lambda c: f"Plano!${c}${P0}:${c}${PF}"
RR = lambda c: f"Registro!${c}${R0}:${c}${RF}"
SIT_CONF = ("Escolha a frequência", "Data futura: confira")

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
def cores(ws, rng, prim):
    for txt, cor in (("Atrasada", VERM), ("Vence em breve", AMAR), ("Em dia", VERDE), ("Sem registro: faça e anote", CINZA),
                     ("Escolha a frequência", VERM), ("Data futura: confira", VERM), ("Nº não existe no Plano", VERM)):
        ws.conditional_formatting.add(rng, FormulaRule(formula=[f'{prim}="{txt}"'], fill=PatternFill("solid", fgColor=cor)))

def comece(wb, exemplo):
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False; ws.column_dimensions["A"].width = 108
    L = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 18", T(10, True, TERRA)),
        ("Planner de Manutenção Preventiva", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para montar um plano de manutenção preventiva da sua hospedagem: o que conferir, de quanto em quanto tempo, quem faz, o que está atrasado e quanto isso custa por ano.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (hospedagem, pessoas, datas e custos inventados). Use a versão em branco." if exemplo
         else "Versão em branco, com uma lista sugerida de tarefas. Apague o que não se aplica, ajuste as frequências e preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Para Airbnb, casas, apartamentos, pousadas e glampings.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 5 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Plano, topo: a data de hoje (já vem com HOJE(); troque por uma data fixa se quiser) e com quantos dias de antecedência quer o aviso.", None),
        ("2. Revise a lista: unidade, área, tarefa e frequência (diária a anual). Para outro intervalo, deixe a frequência vazia e escreva os dias em \"Dias (outro intervalo)\".", None),
        ("3. Defina o responsável de cada tarefa e, se souber, quando foi feita pela última vez e quanto custa cada vez.", None),
        ("4. A cada tarefa feita, anote na aba Registro: data, nº da tarefa, quem fez e o que viu. A próxima data se recalcula sozinha.", None),
        ("5. Abra o Painel toda semana: atrasadas, as que vencem em breve, a próxima a vencer e o custo anual estimado.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("AS CONTAS", T(12, True, MUSGO)),
        ("Intervalo = dias da frequência (Diária 1, Semanal 7, Quinzenal 15, Mensal 30, Bimestral 60, Trimestral 90, Semestral 180, Anual 365) ou os dias informados.", None),
        ("Última vez = a data mais recente entre a anotada no Plano e as do Registro. Próxima = última vez + intervalo. Dias até a próxima = próxima − hoje.", None),
        ("Situação: Atrasada (menos de 0 dias), Vence em breve (até o aviso), Em dia, Sem registro (nunca anotada). Custo anual estimado = custo por vez × 365 ÷ intervalo.", None),
        ("", None),
        ("O QUE A PLANILHA NÃO FAZ", T(12, True, MUSGO)),
        ("As frequências sugeridas são um ponto de partida: siga o manual do fabricante, as regras locais e o profissional responsável (gás, elétrica, extintores, caixa d'água, controle de pragas). A planilha não substitui laudos, vistorias nem serviços técnicos.", None),
        ("Problemas que aparecem fora do plano vão para um quadro de ocorrências (corretiva), não para este planner (preventiva).", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo. Não garante ausência de defeitos, reservas nem resultado financeiro.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(L, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

def plano(wb, exemplo):
    p = wb.create_sheet("Plano"); p.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHIJKLMN", (6, 14, 15, 36, 13, 11, 14, 13, 12, 13, 13, 11, 24, 14)): p.column_dimensions[col].width = w
    p["A1"] = "Plano de manutenção preventiva"; p["A1"].font = T(18, True, MUSGO)
    p["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Preencha as células amarelas. A lista é uma sugestão: ajuste à sua hospedagem."
    p["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    p.merge_cells("A4:C4"); p["A4"] = "Data de hoje"; p["A4"].font = T(11, True)
    ent(p["D4"], d(EX_HOJE) if exemplo else "=TODAY()", DATA, True)
    p.merge_cells("A5:C5"); p["A5"] = "Avisar com quantos dias de antecedência"; p["A5"].font = T(11, True)
    ent(p["D5"], EX_AVISO, "0", True)
    p.merge_cells("E4:N5"); p["E4"] = ("A frequência sugerida é um ponto de partida: siga o manual do fabricante e o profissional responsável. "
                                       "Para outro intervalo, deixe Frequência vazia e preencha Dias.")
    p["E4"].font = T(9, c="5F5F55", i=True); p["E4"].alignment = WRAP
    cab(p, 7, ["Nº", "Unidade", "Área", "Tarefa", "Frequência", "Dias (outro intervalo)", "Responsável", "Última vez (antes de começar)",
               "Custo por vez (R$)", "Intervalo (dias)", "Última vez (com Registro)", "Próxima data", "Situação", "Custo anual estimado"])
    # coluna N recebe também "Dias até a próxima" em O
    p.column_dimensions["O"].width = 11; c = p.cell(7, 15, "Dias até a próxima"); c.font = T(9, True, CREME); c.fill = CAB; c.border = borda
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    dv = DataValidation(type="list", formula1='"' + ",".join(n for n, _ in FREQ) + '"', allow_blank=True)
    p.add_data_validation(dv); dv.add(f"E{P0}:E{PF}")
    fmap = "".join(f'IF(E{{r}}="{n}",{dd},' for n, dd in FREQ)
    for i in range(NP):
        r = P0 + i
        if exemplo and i < len(EX_PLANO):
            u, a, t, f, dd, resp, ult, custo = EX_PLANO[i]; vals = [u, a, t, f or None, dd, resp, d(ult), custo]
        elif not exemplo and i < len(SUGERIDAS):
            a, t, f = SUGERIDAS[i]; vals = [None, a, t, f, None, None, None, None]
        else:
            vals = [None] * 8
        calc(p[f"A{r}"], i + 1, "0", True)
        for col, v, fmt in zip("BCDEFGHI", vals, (None, None, None, None, "0", None, DATA, BRL)):
            ent(p[f"{col}{r}"], v, fmt, col == "D")
        J = (f'=IF(D{r}="","",IF(AND(ISNUMBER(F{r}),F{r}>0),F{r},' + fmap.format(r=r) + '""' + ")" * len(FREQ) + "))")
        calc(p[f"J{r}"], J, "0")
        calc(p[f"K{r}"], f'=IF(D{r}="","",IF(MAX(N(H{r}),SUMPRODUCT(MAX(({RR("B")}=A{r})*{RR("A")})))=0,"",MAX(N(H{r}),SUMPRODUCT(MAX(({RR("B")}=A{r})*{RR("A")})))))', DATA)
        calc(p[f"L{r}"], f'=IF(OR(J{r}="",K{r}=""),"",K{r}+J{r})', DATA, True)
        calc(p[f"O{r}"], f'=IF(OR(L{r}="",NOT(ISNUMBER($D$4))),"",L{r}-$D$4)', "0")
        calc(p[f"M{r}"], (f'=IF(D{r}="","",IF(J{r}="","Escolha a frequência",IF(K{r}="","Sem registro: faça e anote",IF(NOT(ISNUMBER($D$4)),"Informe a data de hoje",'
                          f'IF(K{r}>$D$4,"Data futura: confira",IF(O{r}<0,"Atrasada",IF(O{r}<=N($D$5),"Vence em breve","Em dia")))))))'), None, True)
        calc(p[f"N{r}"], f'=IF(OR(J{r}="",NOT(ISNUMBER(I{r}))),"",I{r}*365/J{r})', BRL)
    cores(p, f"M{P0}:M{PF}", f"M{P0}")
    p.freeze_panes = f"E{P0}"

def registro(wb, exemplo):
    g = wb.create_sheet("Registro"); g.sheet_view.showGridLines = False
    for col, w in zip("ABCDEF", (13, 10, 16, 40, 40, 22)): g.column_dimensions[col].width = w
    g["A1"] = "Registro das tarefas feitas"; g["A1"].font = T(18, True, MUSGO)
    g["A2"] = "Uma linha por tarefa feita. O Nº é o da aba Plano. A próxima data no Plano se atualiza sozinha."; g["A2"].font = T(10, c="5F5F55", i=True)
    cab(g, 4, ["Data", "Nº da tarefa", "Feito por", "O que viu ou fez", "Tarefa (do Plano)", "Situação"])
    for i in range(NR):
        r = R0 + i; x = EX_REG[i] if exemplo and i < len(EX_REG) else (None, None, None, None)
        for col, v, fmt in zip("ABCD", (d(x[0]), x[1], x[2], x[3]), (DATA, "0", None, None)): ent(g[f"{col}{r}"], v, fmt)
        calc(g[f"E{r}"], f'=IF(B{r}="","",IF(ISNA(MATCH(B{r},{RP("A")},0)),"",IF(INDEX({RP("D")},MATCH(B{r},{RP("A")},0))="","",INDEX({RP("D")},MATCH(B{r},{RP("A")},0))&" · "&INDEX({RP("B")},MATCH(B{r},{RP("A")},0)))))')
        calc(g[f"F{r}"], (f'=IF(AND(A{r}="",B{r}=""),"",IF(NOT(ISNUMBER(A{r})),"Informe a data",IF(OR(NOT(ISNUMBER(B{r})),ISNA(MATCH(B{r},{RP("A")},0))),"Nº não existe no Plano",'
                          f'IF(INDEX({RP("D")},MATCH(B{r},{RP("A")},0))="","Nº não existe no Plano",IF(AND(ISNUMBER(Plano!$D$4),A{r}>Plano!$D$4),"Data futura: confira","OK")))))'), None, True)
    cores(g, f"F{R0}:F{RF}", f"F{R0}")
    g.conditional_formatting.add(f"F{R0}:F{RF}", FormulaRule(formula=[f'F{R0}="OK"'], fill=PatternFill("solid", fgColor=VERDE)))
    g.conditional_formatting.add(f"F{R0}:F{RF}", FormulaRule(formula=[f'F{R0}="Informe a data"'], fill=PatternFill("solid", fgColor=VERM)))
    g.freeze_panes = f"A{R0}"

def painel(wb):
    s = wb.create_sheet("Painel"); s.sheet_view.showGridLines = False
    s.column_dimensions["A"].width = 46; s.column_dimensions["B"].width = 40
    s["A1"] = "Painel da semana"; s["A1"].font = T(18, True, MUSGO)
    s["A2"] = "Tudo calculado a partir das abas Plano e Registro."; s["A2"].font = T(10, c="5F5F55", i=True)
    M = RP("M")
    lin = [
        (4, "Data de hoje", "=Plano!D4", DATA, False),
        (5, "Tarefas no plano", f'=SUMPRODUCT(--(LEN({RP("D")})>0))', "0", True),
        (6, "Atrasadas", f'=COUNTIF({M},"Atrasada")', "0", True),
        (7, "Vencem em breve", f'=COUNTIF({M},"Vence em breve")', "0", True),
        (8, "Em dia", f'=COUNTIF({M},"Em dia")', "0", False),
        (9, "Sem registro (nunca anotadas)", f'=COUNTIF({M},"Sem registro: faça e anote")', "0", False),
        (10, "Linhas para conferir no Plano", "+".join(f'COUNTIF({M},"{x}")' for x in SIT_CONF), "0", False),
        (11, "Registros para conferir", f'=COUNTIF({RR("F")},"Nº não existe no Plano")+COUNTIF({RR("F")},"Data futura: confira")+COUNTIF({RR("F")},"Informe a data")', "0", False),
        (12, "Mais urgente (dias até a data; negativo = atrasada)", f'=IF(COUNT({RP("O")})=0,"",MIN({RP("O")}))', "0", True),
        (13, "Mais urgente (tarefa)", f'=IF(B12="","",INDEX({RP("D")},MATCH(B12,{RP("O")},0))&" · "&INDEX({RP("B")},MATCH(B12,{RP("O")},0)))', None, False),
        (14, "Custo anual estimado (tarefas com custo)", f'=SUM({RP("N")})', BRL, True),
        (15, "Leitura", ('=IF(B5=0,"Monte o plano na aba Plano",IF(NOT(ISNUMBER(Plano!D4)),"Informe a data de hoje na aba Plano",IF(B10>0,"Há linhas para conferir no Plano",IF(B6>0,"Há tarefas atrasadas: comece por elas",'
                         'IF(B7>0,"Nada atrasado; programe as que vencem em breve",IF(AND(B8=0,B9>0),"Nenhuma tarefa anotada ainda: registre a primeira vez de cada uma",IF(B9>0,"Em dia, mas há tarefas sem registro","Tudo em dia")))))))'), None, True),
    ]
    for l, rot, f, fmt, b in lin:
        s.cell(l, 1, rot).font = T(11, b); calc(s.cell(l, 2), f if f.startswith("=") else "=" + f, fmt, b, 12 if b else 10)
    s.conditional_formatting.add("B15", FormulaRule(formula=['B15="Tudo em dia"'], fill=PatternFill("solid", fgColor=VERDE)))
    s.conditional_formatting.add("B15", FormulaRule(formula=['LEFT(B15,3)="Há "'], fill=PatternFill("solid", fgColor=VERM)))
    s.conditional_formatting.add("B6", FormulaRule(formula=['B6>0'], fill=PatternFill("solid", fgColor=VERM)))

def montar(exemplo):
    wb = Workbook(); comece(wb, exemplo); plano(wb, exemplo); registro(wb, exemplo); painel(wb); wb.active = 0
    nome = "Manutencao-Preventiva-Zion-EXEMPLO.xlsx" if exemplo else "Manutencao-Preventiva-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

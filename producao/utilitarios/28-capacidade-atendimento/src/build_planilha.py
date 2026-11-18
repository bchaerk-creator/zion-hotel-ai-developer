"""Gera a Ferramenta 28 · Planner de Capacidade e Atendimento (Zion Hospitality Business):
   - Capacidade-Atendimento-Zion-EM-BRANCO.xlsx / Capacidade-Atendimento-Zion-EXEMPLO.xlsx (dados fictícios)
Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dados import EX_HOJE, EX_EXP, EX_SAI, FUTURAS, VALIDAS
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
DATA, PCT = "DD/MM/YYYY", "0%"
E0, NE = 7, 20          # experiências: linhas 7..26
S0, NS = 7, 200         # saídas: linhas 7..206
VERDE, VERM, AMAR = "C8E6C0", "F4C7C3", "FCE8B2"
d = lambda s: datetime.date.fromisoformat(s) if s else None
inv = lambda x: f"OR(NOT(ISNUMBER({x})),N({x})<0,INT(N({x}))<>N({x}))"      # não é número inteiro >= 0
opt = lambda x: f'AND({x}<>"",{inv(x)})'                                     # preenchido e inválido

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
def lista(ws, rng, ref):
    dv = DataValidation(type="list", formula1=ref, allow_blank=True, showErrorMessage=True,
                        errorTitle="Opção inválida", error="Escolha uma experiência da aba Experiências.")
    ws.add_data_validation(dv); dv.add(rng)
def cores(ws, rng, col, verdes, amarelos):
    c0 = f"{col}{rng.split(':')[0][1:]}"
    todas = verdes + amarelos
    for cond, cor in [(f'OR({",".join(f"{c0}={chr(34)}{s}{chr(34)}" for s in verdes)})', VERDE),
                      (f'OR({",".join(f"{c0}={chr(34)}{s}{chr(34)}" for s in amarelos)})', AMAR),
                      (f'AND({c0}<>"",' + ",".join(f'{c0}<>"{s}"' for s in todas) + ")", VERM)]:
        ws.conditional_formatting.add(rng, FormulaRule(formula=[cond], fill=PatternFill("solid", fgColor=cor)))

def montar(exemplo):
    wb = Workbook(); ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 104
    linhas = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 28", T(10, True, TERRA)),
        ("Planner de Capacidade e Atendimento", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para planejar as saídas das suas experiências (trilha, passeio, aula, café especial): quantas pessoas cabem, quantos condutores escalar, quando confirmar ou cancelar e o que fazer com a lista de espera.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (experiências, datas e números inventados). Use a versão em branco." if exemplo
         else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Para Airbnb, casas, apartamentos, pousadas, glampings e quem oferece passeios e experiências.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 4 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Experiências: cadastre cada experiência com a capacidade por saída, quantas pessoas cada condutor (guia, instrutor, monitor) atende, o mínimo de pessoas para a saída acontecer e com quantos dias de antecedência você decide.", None),
        ("2. Aba Saídas: uma linha por saída (data e horário), com a experiência, as pessoas reservadas, os condutores escalados e quem está na lista de espera.", None),
        ("3. Leia a coluna Situação de cada saída: acima da capacidade, falta condutor, abaixo do mínimo, decida, lotada ou confirmada.", None),
        ("4. Aba Painel: veja o que fazer agora e quantas pessoas e condutores você precisa nos próximos 7 dias.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("COMO A PLANILHA DECIDE", T(12, True, MUSGO)),
        ("Condutores necessários = pessoas reservadas ÷ pessoas por condutor, arredondado para cima. Vagas livres = capacidade − reservadas. Ocupação = reservadas ÷ capacidade.", None),
        ("Decidir até = data da saída − dias de antecedência. Abaixo do mínimo, a saída fica \"Abaixo do mínimo\" até essa data; a partir dela, \"Decida: confirmar ou cancelar\".", None),
        ("Ordem das situações: acima da capacidade → falta condutor → abaixo do mínimo (ou decida) → lotada (com ou sem lista de espera) → confirmada. Saídas com data anterior a hoje ficam como \"Já passou\" e saem das contas.", None),
        ("Mínimo e antecedência em branco contam como zero. Capacidade e pessoas por condutor precisam ser números inteiros a partir de 1.", None),
        ("", None),
        ("CUIDADOS", T(12, True, MUSGO)),
        ("Você define a capacidade e quantas pessoas cada condutor atende, conforme a atividade, o local, o equipamento e as regras que valem para a sua região. A planilha só faz as contas com o que você informar.", None),
        ("Não anote nome, telefone ou documento dos participantes nesta planilha: use só a quantidade. Se precisar de dados para a segurança da saída, guarde à parte e só o necessário.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Experiências ----------
    ex = wb.create_sheet("Experiências"); ex.sheet_view.showGridLines = False
    for j, w in enumerate((30, 13, 13, 13, 14, 18, 24, 12, 13, 13), 1): ex.column_dimensions[ex.cell(1, j).column_letter].width = w
    ex["A1"] = "Experiências"; ex["A1"].font = T(18, True, MUSGO)
    ex["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Capacidade e pessoas por condutor: números inteiros a partir de 1. Mínimo e antecedência: deixe em branco se não usar."
    ex["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    ex["A4"] = "Data de hoje"; ex["A4"].font = T(10, True)
    ent(ex["B4"], d(EX_HOJE) if exemplo else "=TODAY()", DATA)
    ex["C4"] = "Fica automática; troque só para simular outra data."; ex["C4"].font = T(9, c="5F5F55", i=True)
    HOJE = "Experiências!$B$4"
    cab(ex, 6, ["Experiência", "Capacidade por saída (pessoas)", "Pessoas por condutor", "Mínimo para confirmar", "Decidir com quantos dias de antecedência",
                "Ponto de encontro", "Situação", "Próximas saídas", "Pessoas reservadas (próximas)", "Ocupação das próximas"])
    rs = lambda c: f"Saídas!${c}${S0}:${c}${S0+NS-1}"
    for k in range(NE):
        r = E0 + k; v = EX_EXP[k] if exemplo and k < len(EX_EXP) else (None,) * 6
        for col, x in zip("ABCDEF", v): ent(ex[f"{col}{r}"], x)
        calc(ex[f"G{r}"], f'=IF(A{r}="","",IF(OR({inv(f"B{r}")},N(B{r})<1),"Confira a capacidade",IF(OR({inv(f"C{r}")},N(C{r})<1),"Confira pessoas por condutor",'
                          f'IF(OR({opt(f"D{r}")},N(D{r})>N(B{r})),"Confira o mínimo",IF({opt(f"E{r}")},"Confira a antecedência","Pronta")))))', b=True)
        calc(ex[f"H{r}"], f'=IF(A{r}="","",COUNTIFS({rs("C")},A{r},{rs("R")},1))')
        calc(ex[f"I{r}"], f'=IF(A{r}="","",SUMIFS({rs("D")},{rs("C")},A{r},{rs("R")},1))')
        calc(ex[f"J{r}"], f'=IF(A{r}="","",IF(AND(G{r}="Pronta",N(H{r})>0),I{r}/(H{r}*B{r}),""))', PCT)
    cores(ex, f"G{E0}:G{E0+NE-1}", "G", ["Pronta"], [])
    ex.freeze_panes = f"B{E0}"
    EXP = f"Experiências!$A${E0}:$A${E0+NE-1}"
    look = lambda col, r: f"INDEX(Experiências!${col}${E0}:${col}${E0+NE-1},MATCH(C{r},{EXP},0))"

    # ---------- Saídas ----------
    sa = wb.create_sheet("Saídas"); sa.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHIJKL", (12, 9, 30, 12, 12, 11, 11, 10, 12, 10, 12, 27)): sa.column_dimensions[col].width = w
    sa["A1"] = "Saídas"; sa["A1"].font = T(18, True, MUSGO)
    sa["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Uma linha por saída. Anote só quantidades, nunca nomes ou telefones."
    sa["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    sa["A3"] = "Saídas com problema:"; sa["A3"].font = T(10, True)
    rgL = f"L{S0}:L{S0+NS-1}"
    calc(sa["D3"], f'=COUNTIF({rgL},"?*")-' + "-".join(f'COUNTIF({rgL},"{s}")' for s in VALIDAS), b=True)
    cab(sa, 6, ["Data", "Horário", "Experiência", "Pessoas reservadas", "Condutores escalados", "Lista de espera (pessoas)",
                "Capacidade", "Vagas livres", "Condutores necessários", "Ocupação", "Decidir até", "Situação"])
    for col in "MNOPQR": sa.column_dimensions[col].hidden = True
    for k in range(NS):
        r = S0 + k; v = EX_SAI[k] if exemplo and k < len(EX_SAI) else (None,) * 6
        for col, x, fmt in zip("ABCDEF", (d(v[0]), v[1], v[2], v[3], v[4], v[5]), (DATA, None, None, None, None, None)):
            ent(sa[f"{col}{r}"], x, fmt)
        cad = f'AND(C{r}<>"",COUNTIF({EXP},C{r})>0)'
        calc(sa[f"M{r}"], f'=IF({cad},{look("G", r)}&"","")')
        for col, src in zip("NOPQ", "BCDE"): calc(sa[f"{col}{r}"], f'=IF({cad},N({look(src, r)}),0)')
        calc(sa[f"L{r}"], f'=IF(AND(A{r}="",C{r}="",D{r}=""),"",IF(NOT(ISNUMBER(A{r})),"Informe a data",IF(NOT({cad}),"Experiência não cadastrada",'
                          f'IF(M{r}<>"Pronta","Complete a experiência",IF({opt(f"D{r}")},"Confira os reservados",IF({opt(f"E{r}")},"Confira os condutores",'
                          f'IF({opt(f"F{r}")},"Confira a lista de espera",IF(A{r}<{HOJE},"Já passou",IF(N(D{r})>N{r},"Acima da capacidade",'
                          f'IF(N(E{r})<ROUNDUP(N(D{r})/O{r},0),"Falta condutor",IF(N(D{r})<P{r},IF({HOJE}>=A{r}-Q{r},"Decida: confirmar ou cancelar","Abaixo do mínimo"),'
                          f'IF(N(D{r})=N{r},IF(N(F{r})>0,"Lotada, com lista de espera","Lotada"),"Confirmada"))))))))))))', b=True)
        ok = "OR(" + ",".join(f'L{r}="{s}"' for s in VALIDAS) + ")"
        calc(sa[f"G{r}"], f'=IF({ok},N{r},"")')
        calc(sa[f"H{r}"], f'=IF({ok},N{r}-N(D{r}),"")')
        calc(sa[f"I{r}"], f'=IF({ok},ROUNDUP(N(D{r})/O{r},0),"")')
        calc(sa[f"J{r}"], f'=IF({ok},N(D{r})/N{r},"")', PCT)
        calc(sa[f"K{r}"], f'=IF({ok},A{r}-Q{r},"")', DATA)
        calc(sa[f"R{r}"], "=IF(OR(" + ",".join(f'L{r}="{s}"' for s in FUTURAS) + "),1,0)")
    lista(sa, f"C{S0}:C{S0+NS-1}", EXP)
    cores(sa, rgL, "L", ["Confirmada", "Lotada", "Já passou"], ["Lotada, com lista de espera", "Abaixo do mínimo", "Decida: confirmar ou cancelar", "Falta condutor"])
    sa.freeze_panes = f"A{S0}"

    # ---------- Painel ----------
    p = wb.create_sheet("Painel"); p.sheet_view.showGridLines = False
    p.column_dimensions["A"].width = 52; p.column_dimensions["B"].width = 18
    p["A1"] = "Painel de capacidade e atendimento"; p["A1"].font = T(18, True, MUSGO)
    p["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Tudo calculado."; p["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    er = lambda c: f"Experiências!${c}${E0}:${c}${E0+NE-1}"
    sete = f'"<="&(B4+6)'
    itens = [("Data de hoje", f"={HOJE}", DATA),
             ("Experiências cadastradas", f'=COUNTIF({er("A")},"?*")', None),
             ("Experiências com cadastro incompleto", f'=B5-COUNTIF({er("G")},"Pronta")', None),
             ("Próximas saídas", f'=SUM({rs("R")})', None),
             ("Confirmadas (inclui lotadas)", f'=COUNTIF({rs("L")},"Confirmada")+COUNTIF({rs("L")},"Lotada")+COUNTIF({rs("L")},"Lotada, com lista de espera")', None),
             ("Abaixo do mínimo", f'=COUNTIF({rs("L")},"Abaixo do mínimo")+COUNTIF({rs("L")},"Decida: confirmar ou cancelar")', None),
             ("Decidir agora (prazo chegou)", f'=COUNTIF({rs("L")},"Decida: confirmar ou cancelar")', None),
             ("Falta condutor", f'=COUNTIF({rs("L")},"Falta condutor")', None),
             ("Acima da capacidade", f'=COUNTIF({rs("L")},"Acima da capacidade")', None),
             ("Lotadas com lista de espera", f'=COUNTIF({rs("L")},"Lotada, com lista de espera")', None),
             ("Saídas com problema", "=Saídas!D3", None),
             ("Pessoas reservadas nos próximos 7 dias", f'=SUMIFS({rs("D")},{rs("R")},1,{rs("A")},{sete})', None),
             ("Condutores necessários nos próximos 7 dias (soma das saídas)", f'=SUMIFS({rs("I")},{rs("R")},1,{rs("A")},{sete})', None),
             ("Pessoas na lista de espera (próximas saídas)", f'=SUMIFS({rs("F")},{rs("R")},1)', None)]
    for i, (rot, f, fmt) in enumerate(itens):
        r = 4 + i; p[f"A{r}"] = rot; p[f"A{r}"].font = T(10, True); calc(p[f"B{r}"], f, fmt, True)
    p["A19"] = "O que fazer agora"; p["A19"].font = T(12, True, MUSGO)
    calc(p["A20"], '=IF(B5=0,"Cadastre as experiências",IF(B6>0,"Complete o cadastro de "&B6&" experiência(s)",IF(B14>0,"Corrija as saídas com problema",'
                   'IF(B12>0,"Remaneje "&B12&" saída(s) acima da capacidade",IF(B11>0,"Escale condutor em "&B11&" saída(s)",'
                   'IF(B10>0,"Decida "&B10&" saída(s) abaixo do mínimo: confirmar ou cancelar",IF(B13>0,"Abra outro horário: "&B13&" saída(s) lotada(s) com lista de espera",'
                   'IF(B7=0,"Cadastre as próximas saídas","Tudo em dia"))))))))', b=True)
    p.merge_cells("A20:B20"); p.row_dimensions[20].height = 30

    wb.active = 0
    nome = "Capacidade-Atendimento-Zion-EXEMPLO.xlsx" if exemplo else "Capacidade-Atendimento-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

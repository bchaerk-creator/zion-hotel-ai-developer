"""Gera a Ferramenta 16 · Kit Operacional de Parcerias (Zion Hospitality Business):
   - Parcerias-Zion-EM-BRANCO.xlsx / Parcerias-Zion-EXEMPLO.xlsx (dados fictícios)
Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dados import TIPOS, CONTRA, SIM_NAO, EX_HOJE, EX_PARC, EX_IND
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
P0, NP = 7, 40         # parceiros: linhas 7..46
I0, NI = 7, 300        # indicações: linhas 7..306
VERDE, VERM, AMAR = "C8E6C0", "F4C7C3", "FCE8B2"
VALIDAS = ("Aguardando confirmação", "A receber", "Recebido", "Sem comissão")
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
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 16", T(10, True, TERRA)),
        ("Kit Operacional de Parcerias", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para organizar as parcerias da sua hospedagem com restaurantes, guias, spas e transportes: o que cada um oferece, o que foi combinado, as indicações feitas e o que você tem a receber.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (parceiros, contatos, valores e reservas inventados). Use a versão em branco." if exemplo
         else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Para Airbnb, casas, apartamentos, pousadas e glampings.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 4 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Parceiros: cadastre cada parceiro, o que ele oferece ao hóspede, o benefício combinado e a contrapartida (porcentagem, valor fixo, troca ou nenhuma). Marque se o acordo está por escrito e quando revisar.", None),
        ("2. Combine com o parceiro como ele confirma as indicações (mensagem, cupom, código da reserva). Use a Ficha de Acordo para registrar.", None),
        ("3. Aba Indicações: uma linha por indicação, com a data, o parceiro e o código da reserva (não o nome do hóspede). Quando o parceiro confirmar, marque Sim; quando receber, marque Sim.", None),
        ("4. Aba Painel: veja quem está sem acordo por escrito, que acordo precisa ser revisto, o que falta confirmar e quanto há para receber.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("COMO A PLANILHA DECIDE", T(12, True, MUSGO)),
        ("Comissão: porcentagem × valor gasto pelo hóspede; valor fixo por indicação; troca ou nenhuma = sem comissão. Porcentagem precisa ficar entre 0% e 99% e valor fixo maior que zero.", None),
        ("Situação da indicação: Aguardando confirmação até o parceiro confirmar; A receber depois de confirmada; Recebido quando você marca. Indicação de parceiro não cadastrado, sem data ou, na porcentagem, sem o valor gasto não entra nas contas.", None),
        ("Situação do parceiro: Sem acordo por escrito enquanto não houver; Revisar o acordo quando a data de revisão chegar; Ativa nos demais casos.", None),
        ("", None),
        ("CUIDADOS", T(12, True, MUSGO)),
        ("Não anote nome, telefone ou documento do hóspede: use o código da reserva. Indique o parceiro só a quem pedir ou aceitar a sugestão.", None),
        ("Comissão é receita e pode ter imposto: fale com o seu contador. A ficha de acordo organiza o combinado, mas não substitui contrato revisado por advogado.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Parceiros ----------
    pa = wb.create_sheet("Parceiros"); pa.sheet_view.showGridLines = False
    larg = (28, 18, 16, 26, 22, 20, 12, 11, 12, 24, 11, 11, 13, 13)
    for j, w in enumerate(larg, 1): pa.column_dimensions[pa.cell(1, j).column_letter].width = w
    pa["A1"] = "Parceiros"; pa["A1"].font = T(18, True, MUSGO)
    pa["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Valor da contrapartida: porcentagem (ex.: 10%) ou valor fixo em reais, conforme a coluna anterior."
    pa["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    pa["A4"] = "Data de hoje"; pa["A4"].font = T(10, True)
    ent(pa["B4"], d(EX_HOJE) if exemplo else "=TODAY()", DATA)
    pa["C4"] = "Fica automática; troque só para simular outra data."; pa["C4"].font = T(9, c="5F5F55", i=True)
    HOJE = "Parceiros!$B$4"
    cab(pa, 6, ["Parceiro", "Tipo", "Contato", "O que oferece ao hóspede", "Benefício para o hóspede", "Contrapartida", "Valor da contrapartida",
                "Acordo por escrito?", "Revisar em", "Situação", "Indicações", "Confirmadas", "A receber", "Recebido"])
    ri = lambda c: f"Indicações!${c}${I0}:${c}${I0+NI-1}"
    for k in range(NP):
        r = P0 + k; v = EX_PARC[k] if exemplo and k < len(EX_PARC) else (None,) * 9
        fmt_val = '0%;"";""' if v[5] == "% sobre o valor" else (BRL if v[5] else None)
        for col, x, fmt in zip("ABCDEFGHI", (v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], d(v[8])),
                               (None, None, None, None, None, None, fmt_val, None, DATA)):
            ent(pa[f"{col}{r}"], x, fmt)
        calc(pa[f"J{r}"], f'=IF(A{r}="","",IF(B{r}="","Escolha o tipo",IF(F{r}="","Escolha a contrapartida",'
                          f'IF(OR(F{r}="% sobre o valor",F{r}="Valor fixo por indicação"),IF(OR(NOT(ISNUMBER(G{r})),N(G{r})<=0,AND(F{r}="% sobre o valor",N(G{r})>=1)),"Confira o valor da contrapartida",'
                          f'IF(H{r}<>"Sim","Sem acordo por escrito",IF(AND(ISNUMBER(I{r}),ISNUMBER({HOJE}),I{r}<={HOJE}),"Revisar o acordo","Ativa"))),'
                          f'IF(H{r}<>"Sim","Sem acordo por escrito",IF(AND(ISNUMBER(I{r}),ISNUMBER({HOJE}),I{r}<={HOJE}),"Revisar o acordo","Ativa"))))))', b=True)
        calc(pa[f"K{r}"], f'=IF(A{r}="","",' + "+".join(f'COUNTIFS({ri("B")},A{r},{ri("H")},"{s}")' for s in VALIDAS) + ")")
        calc(pa[f"L{r}"], f'=IF(A{r}="","",' + "+".join(f'COUNTIFS({ri("B")},A{r},{ri("H")},"{s}")' for s in VALIDAS[1:]) + ")")
        calc(pa[f"M{r}"], f'=IF(A{r}="","",SUMIFS({ri("G")},{ri("B")},A{r},{ri("H")},"A receber"))', BRL)
        calc(pa[f"N{r}"], f'=IF(A{r}="","",SUMIFS({ri("G")},{ri("B")},A{r},{ri("H")},"Recebido"))', BRL)
    lista(pa, f"B{P0}:B{P0+NP-1}", TIPOS); lista(pa, f"F{P0}:F{P0+NP-1}", CONTRA); lista(pa, f"H{P0}:H{P0+NP-1}", SIM_NAO)
    rgJ = f"J{P0}:J{P0+NP-1}"
    for cond, cor in ((f'J{P0}="Ativa"', VERDE), (f'J{P0}="Revisar o acordo"', AMAR), (f'J{P0}="Sem acordo por escrito"', AMAR),
                      (f'AND(J{P0}<>"",J{P0}<>"Ativa",J{P0}<>"Revisar o acordo",J{P0}<>"Sem acordo por escrito")', VERM)):
        pa.conditional_formatting.add(rgJ, FormulaRule(formula=[cond], fill=PatternFill("solid", fgColor=cor)))
    pa.freeze_panes = f"B{P0}"
    PAR = f"Parceiros!$A${P0}:$A${P0+NP-1}"
    look = lambda col, r: f"INDEX(Parceiros!${col}${P0}:${col}${P0+NP-1},MATCH(B{r},{PAR},0))"

    # ---------- Indicações ----------
    ind = wb.create_sheet("Indicações"); ind.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGH", (12, 30, 14, 14, 13, 11, 13, 26)): ind.column_dimensions[col].width = w
    ind["A1"] = "Indicações"; ind["A1"].font = T(18, True, MUSGO)
    ind["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Uma linha por indicação. Use o código da reserva, nunca o nome do hóspede."
    ind["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    ind["A3"] = "Indicações com problema:"; ind["A3"].font = T(10, True)
    rgH = f"H{I0}:H{I0+NI-1}"
    calc(ind["D3"], f'=COUNTIF({rgH},"?*")-' + "-".join(f'COUNTIF({rgH},"{s}")' for s in VALIDAS), b=True)
    cab(ind, 6, ["Data", "Parceiro", "Código da reserva", "Valor gasto pelo hóspede (se for %)", "Confirmada pelo parceiro?", "Recebido?", "Comissão", "Situação"])
    for col in "IJK": ind.column_dimensions[col].hidden = True
    for k in range(NI):
        r = I0 + k; v = EX_IND[k] if exemplo and k < len(EX_IND) else (None,) * 6
        for col, x, fmt in zip("ABCDEF", (d(v[0]), v[1], v[2], v[3], v[4], v[5]), (DATA, None, None, BRL, None, None)):
            ent(ind[f"{col}{r}"], x, fmt)
        cad = f"AND(B{r}<>\"\",COUNTIF({PAR},B{r})>0)"
        calc(ind[f"I{r}"], f'=IF({cad},{look("F", r)}&"","")')
        calc(ind[f"J{r}"], f'=IF({cad},N({look("G", r)}),0)')
        calc(ind[f"K{r}"], f'=IF({cad},{look("J", r)}&"","")')
        calc(ind[f"H{r}"], f'=IF(AND(A{r}="",B{r}="",C{r}=""),"",IF(NOT(ISNUMBER(A{r})),"Informe a data",IF(NOT({cad}),"Parceiro não cadastrado",'
                           f'IF(OR(K{r}="Escolha o tipo",K{r}="Escolha a contrapartida",K{r}="Confira o valor da contrapartida"),"Complete o cadastro do parceiro",'
                           f'IF(AND(D{r}<>"",OR(NOT(ISNUMBER(D{r})),N(D{r})<0)),"Confira o valor gasto",IF(AND(I{r}="% sobre o valor",OR(NOT(ISNUMBER(D{r})),N(D{r})<=0)),"Informe o valor gasto",'
                           f'IF(E{r}<>"Sim","Aguardando confirmação",IF(OR(I{r}="Troca ou cortesia",I{r}="Nenhuma"),"Sem comissão",IF(F{r}="Sim","Recebido","A receber")))))))))', b=True)
        calc(ind[f"G{r}"], f'=IF(OR(H{r}="Aguardando confirmação",H{r}="A receber",H{r}="Recebido",H{r}="Sem comissão"),'
                           f'IF(I{r}="% sobre o valor",D{r}*J{r},IF(I{r}="Valor fixo por indicação",J{r},0)),"")', BRL)
    lista(ind, f"B{I0}:B{I0+NI-1}", ref=PAR); lista(ind, f"E{I0}:F{I0+NI-1}", SIM_NAO)
    for cond, cor in ((f'H{I0}="Recebido"', VERDE), (f'H{I0}="Sem comissão"', VERDE), (f'H{I0}="A receber"', AMAR), (f'H{I0}="Aguardando confirmação"', AMAR),
                      (f'AND(H{I0}<>"",H{I0}<>"Recebido",H{I0}<>"Sem comissão",H{I0}<>"A receber",H{I0}<>"Aguardando confirmação")', VERM)):
        ind.conditional_formatting.add(rgH, FormulaRule(formula=[cond], fill=PatternFill("solid", fgColor=cor)))
    ind.freeze_panes = f"A{I0}"

    # ---------- Painel ----------
    p = wb.create_sheet("Painel"); p.sheet_view.showGridLines = False
    p.column_dimensions["A"].width = 50; p.column_dimensions["B"].width = 18
    p["A1"] = "Painel das parcerias"; p["A1"].font = T(18, True, MUSGO)
    p["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Tudo calculado."; p["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    pr = lambda c: f"Parceiros!${c}${P0}:${c}${P0+NP-1}"
    itens = [("Parceiros cadastrados", f'=COUNTIF({pr("A")},"?*")', None),
             ("Parceiros ativos", f'=COUNTIF({pr("J")},"Ativa")', None),
             ("Sem acordo por escrito", f'=COUNTIF({pr("J")},"Sem acordo por escrito")', None),
             ("Acordos para revisar", f'=COUNTIF({pr("J")},"Revisar o acordo")', None),
             ("Parceiros com cadastro incompleto", f'=COUNTIF({pr("J")},"Escolha*")+COUNTIF({pr("J")},"Confira*")', None),
             ("Indicações registradas (sem problema)", "=" + "+".join(f'COUNTIF({ri("H")},"{s}")' for s in VALIDAS), None),
             ("Aguardando confirmação do parceiro", f'=COUNTIF({ri("H")},"Aguardando confirmação")', None),
             ("Indicações com problema", "=Indicações!D3", None),
             ("Comissão a receber", f'=SUMIFS({ri("G")},{ri("H")},"A receber")', BRL),
             ("Comissão recebida", f'=SUMIFS({ri("G")},{ri("H")},"Recebido")', BRL)]
    for i, (rot, f, fmt) in enumerate(itens):
        r = 4 + i; p[f"A{r}"] = rot; p[f"A{r}"].font = T(10, True); calc(p[f"B{r}"], f, fmt, True)
    p["A15"] = "O que fazer agora"; p["A15"].font = T(12, True, MUSGO)
    calc(p["A16"], '=IF(B4=0,"Cadastre os parceiros",IF(B8>0,"Complete o cadastro de "&B8&" parceiro(s)",IF(B11>0,"Corrija as indicações com problema",'
                   'IF(B6>0,"Combine por escrito com "&B6&" parceiro(s)",IF(B7>0,"Revise "&B7&" acordo(s)",IF(B10>0,"Peça confirmação de "&B10&" indicação(ões)",'
                   'IF(B12>0,"Cobre dos parceiros a comissão a receber (valor acima)","Tudo em dia")))))))', b=True)
    p.merge_cells("A16:B16"); p.row_dimensions[16].height = 30

    wb.active = 0
    nome = "Parcerias-Zion-EXEMPLO.xlsx" if exemplo else "Parcerias-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

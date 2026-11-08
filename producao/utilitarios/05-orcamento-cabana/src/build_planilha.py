"""Gera a Ferramenta 05 · Orçamento da Cabana (Zion Hospitality Business):
   - Orcamento-Cabana-Zion-EM-BRANCO.xlsx (lista sugerida de itens, sem valores)
   - Orcamento-Cabana-Zion-EXEMPLO.xlsx (dados fictícios)
Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dados import ETAPAS, EX, ITENS, NL, L0, NMES
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
BRL = 'R$ #,##0.00;[Red]-R$ #,##0.00'
VERDE, VERM, AMAR = "C8E6C0", "F4C7C3", "FCE8B2"
LF = L0 + NL - 1                                  # última linha de itens
RG = lambda col: f"Orçamento!${col}${L0}:${col}${LF}"
E0 = 5; EF = E0 + len(ETAPAS) - 1                 # etapas na aba Resumo (5 a 14)
R0 = EF + 5                                       # resultados do Resumo (19)
AVISO_SIT = ("Escolha a etapa", "Valor negativo: confira", "Escolhida deve ser 1, 2 ou 3", "Cotação escolhida vazia", "Pago acima do orçado")

def faixa(ws, l, txt, c1=1, c2=5):
    ws.merge_cells(start_row=l, start_column=c1, end_row=l, end_column=c2)
    c = ws.cell(l, c1, txt); c.font = T(11, True, CREME); c.fill = CAB; c.alignment = Alignment(vertical="center", indent=1)
def ent(c, v=None, fmt=None, b=True):
    c.value = v; c.fill = ENTRADA; c.border = borda; c.alignment = WRAP; c.font = T(10, b)
    if fmt: c.number_format = fmt
def calc(c, f, fmt=None, b=False, sz=10):
    c.value = f; c.fill = CALC; c.border = borda; c.alignment = WRAP; c.font = T(sz, b)
    if fmt: c.number_format = fmt
def cab(ws, l, textos, c0=1):
    for j, t in enumerate(textos, c0):
        cc = ws.cell(l, j, t); cc.font = T(9, True, CREME); cc.fill = CAB; cc.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); cc.border = borda

def comece(wb, exemplo):
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False; ws.column_dimensions["A"].width = 108
    linhas = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 05", T(10, True, TERRA)),
        ("Orçamento da Cabana", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para montar o orçamento da sua cabana de Airbnb, do projeto à abertura: todos os itens por etapa, 3 cotações por item, reserva para imprevistos, comparação com a sua verba e o mês de cada pagamento.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS. Os valores são inventados e não servem como referência de preço. Use a versão em branco." if exemplo
         else "Versão em branco, com uma lista sugerida de itens. Apague ou ajuste os itens e preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Serve para cabana, chalé, bubble, tiny house, módulo ou a reforma de um imóvel para hospedagem.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 5 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Orçamento, topo: nome do projeto, área interna, área de deck ou varanda, reserva para imprevistos (%) e a verba que você tem.", None),
        ("2. Revise a lista de itens. Para cada item: etapa, item, especificação (o que o fornecedor precisa cotar) e quantidade (vazio = 1; 0 = não se aplica).", None),
        ("3. Peça 3 cotações com a MESMA especificação e lance o preço unitário de cada uma nas colunas Cotação 1, 2 e 3.", None),
        ("4. Em Escolhida, marque 1, 2 ou 3 quando não for ficar com a mais barata (por exemplo, porque inclui instalação). Vazio = a planilha usa a menor. Para preço único (taxa, tarifa), marque 1.", None),
        ("5. Lance o que já pagou e o mês previsto de cada pagamento (1 a 12). Leia as abas Resumo e Cronograma.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("AS CONTAS", T(12, True, MUSGO)),
        ("Preço escolhido = a cotação marcada em Escolhida, ou a menor. Total do item = preço escolhido × quantidade. Diferença entre cotações = maior ÷ menor − 1.", None),
        ("Subtotal = soma dos itens. Reserva = subtotal × reserva (%). Total com reserva = subtotal + reserva. Diferença = verba − total com reserva. Custo por m² = total com reserva ÷ área.", None),
        ("", None),
        ("O QUE A PLANILHA NÃO FAZ", T(12, True, MUSGO)),
        ("Não informa preços de mercado, não substitui o projeto, o memorial descritivo nem o profissional responsável pela obra, e não diz se a obra é permitida no seu terreno. Não calcula retorno, diária nem ocupação.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo. Não garante custo de obra, reservas nem resultado financeiro.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

def orcamento(wb, exemplo):
    o = wb.create_sheet("Orçamento"); o.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHIJKLMNO", (24, 34, 24, 9, 13, 13, 13, 10, 14, 15, 11, 24, 14, 14, 9)): o.column_dimensions[col].width = w
    o["A1"] = "Orçamento da cabana · do projeto à abertura"; o["A1"].font = T(18, True, MUSGO)
    o["A2"] = ("EXEMPLO · dados fictícios: não use estes valores como referência de preço" if exemplo else "Preencha as células amarelas. A lista de itens é uma sugestão: ajuste ao seu projeto.")
    o["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    campos = [(4, "Nome do projeto", "nome", None), (5, "Área interna (m²)", "area", "0.0"), (6, "Área de deck ou varanda (m²)", "deck", "0.0"),
              (7, "Reserva para imprevistos (%)", "reserva", "0.0"), (8, "Verba disponível (R$)", "verba", BRL)]
    ajuda = {5: "Usada para o custo por m².", 7: "Digite 10 para 10%. Uma reserva protege contra o que aparece no meio da obra.", 8: "Quanto você tem para gastar no projeto, do primeiro pagamento à abertura."}
    for l, r, k, fmt in campos:
        o.merge_cells(start_row=l, start_column=1, end_row=l, end_column=2); o.cell(l, 1, r).font = T(11)
        ent(o.cell(l, 3), EX[k] if exemplo else (10 if k == "reserva" else None), fmt)
        if l in ajuda:
            o.merge_cells(start_row=l, start_column=4, end_row=l, end_column=9); h = o.cell(l, 4, ajuda[l]); h.font = T(9, c="5F5F55", i=True)
    faixa(o, 10, "ITENS DO ORÇAMENTO (preços das cotações são por unidade: por m², por peça ou o valor fechado do serviço)", 1, 15)
    cab(o, 11, ["Etapa", "Item", "Especificação (o que cotar)", "Quanti-dade", "Cotação 1 (R$)", "Cotação 2 (R$)", "Cotação 3 (R$)", "Escolhida (1, 2, 3)",
                "Preço escolhido", "Total do item", "Diferença entre cotações", "Situação", "Já pago (R$)", "Falta pagar", "Mês do paga-mento"])
    o.row_dimensions[11].height = 42
    dv_et = DataValidation(type="list", formula1=f"=Resumo!$A${E0}:$A${EF}", allow_blank=True)
    dv_h = DataValidation(type="whole", operator="between", formula1="1", formula2="3", allow_blank=True)
    dv_m = DataValidation(type="whole", operator="between", formula1="1", formula2=str(NMES), allow_blank=True)
    for dv in (dv_et, dv_h, dv_m): o.add_data_validation(dv)
    dv_et.add(f"A{L0}:A{LF}"); dv_h.add(f"H{L0}:H{LF}"); dv_m.add(f"O{L0}:O{LF}")
    for i in range(NL):
        r = L0 + i
        it = ITENS[i] if i < len(ITENS) else None
        if it and exemplo: et, item, esp, q, c1, c2, c3, h, pago, mes = it; vals = [ETAPAS[et - 1], item, esp or None, q, c1, c2, c3, h]
        elif it: vals = [ETAPAS[it[0] - 1], it[1], None, None, None, None, None, None]; pago = mes = None
        else: vals = [None] * 8; pago = mes = None
        for j, (col, fmt) in enumerate(zip("ABCDEFGH", (None, None, None, "0.##", BRL, BRL, BRL, "0"))):
            ent(o[f"{col}{r}"], vals[j], fmt, b=col in "AB")
        ent(o[f"M{r}"], pago, BRL); ent(o[f"O{r}"], mes, "0")
        n = f"COUNT(E{r}:G{r})"; neg = f"OR(N(D{r})<0,N(E{r})<0,N(F{r})<0,N(G{r})<0,N(M{r})<0)"
        hv = f'OR(H{r}="",H{r}=1,H{r}=2,H{r}=3)'
        calc(o[f"I{r}"], f'=IF(OR(B{r}="",A{r}="",{neg},{n}=0,NOT({hv})),"",IF(H{r}="",MIN(E{r}:G{r}),IF(ISNUMBER(CHOOSE(H{r},E{r},F{r},G{r})),CHOOSE(H{r},E{r},F{r},G{r}),"")))', BRL)
        calc(o[f"J{r}"], f'=IF(I{r}="","",I{r}*IF(ISNUMBER(D{r}),D{r},1))', BRL, True)
        calc(o[f"K{r}"], f'=IF(OR(I{r}="",{n}<2),"",IF(MIN(E{r}:G{r})<=0,"",MAX(E{r}:G{r})/MIN(E{r}:G{r})-1))', "0%")
        calc(o[f"L{r}"], (f'=IF(B{r}="","",IF(A{r}="","Escolha a etapa",IF({neg},"Valor negativo: confira",IF(NOT({hv}),"Escolhida deve ser 1, 2 ou 3",'
                          f'IF(AND(ISNUMBER(D{r}),D{r}=0),"Não se aplica",IF({n}=0,"Sem cotação",IF(I{r}="","Cotação escolhida vazia",'
                          f'IF(N(M{r})>J{r}+0.005,"Pago acima do orçado",IF(AND({n}=1,H{r}=""),"Só 1 cotação: peça mais","OK")))))))))'), None, True)
        calc(o[f"N{r}"], f'=IF(J{r}="","",J{r}-N(M{r}))', BRL)
    rg = f"L{L0}:L{LF}"
    o.conditional_formatting.add(rg, FormulaRule(formula=[f'L{L0}="OK"'], fill=PatternFill("solid", fgColor=VERDE)))
    for s in ("Sem cotação", "Só 1 cotação: peça mais", "Não se aplica"):
        o.conditional_formatting.add(rg, FormulaRule(formula=[f'L{L0}="{s}"'], fill=PatternFill("solid", fgColor=AMAR)))
    for s in AVISO_SIT:
        o.conditional_formatting.add(rg, FormulaRule(formula=[f'L{L0}="{s}"'], fill=PatternFill("solid", fgColor=VERM)))
    o.freeze_panes = f"C{L0}"

def resumo(wb):
    s = wb.create_sheet("Resumo"); s.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFG", (40, 18, 12, 9, 12, 16, 16)): s.column_dimensions[col].width = w
    s["A1"] = "Resumo do orçamento"; s["A1"].font = T(18, True, MUSGO)
    s["A2"] = "Totais por etapa, reserva, comparação com a verba e o que falta pagar. Tudo calculado a partir da aba Orçamento."; s["A2"].font = T(10, c="5F5F55", i=True)
    cab(s, 4, ["Etapa", "Total orçado", "% do subtotal", "Itens", "Sem cotação", "Já pago", "Falta pagar"])
    SUB = f"$B${R0}"
    for i, et in enumerate(ETAPAS):
        r = E0 + i
        c = s.cell(r, 1, et); c.font = T(10, True); c.border = borda
        calc(s[f"B{r}"], f'=SUMIF({RG("A")},A{r},{RG("J")})', BRL, True)
        calc(s[f"C{r}"], f'=IF({SUB}=0,"",B{r}/{SUB})', "0.0%")
        calc(s[f"D{r}"], f'=COUNTIFS({RG("A")},A{r},{RG("B")},"<>")', "0")
        calc(s[f"E{r}"], f'=COUNTIFS({RG("A")},A{r},{RG("L")},"Sem cotação")', "0")
        calc(s[f"F{r}"], f'=B{r}-G{r}', BRL)
        calc(s[f"G{r}"], f'=SUMIF({RG("A")},A{r},{RG("N")})', BRL)
    r = EF + 1; c = s.cell(r, 1, "Etapa fora da lista (confira a coluna Etapa)"); c.font = T(10, i=True); c.border = borda
    calc(s[f"B{r}"], f"={SUB}-SUM(B{E0}:B{EF})", BRL); calc(s[f"C{r}"], f'=IF({SUB}=0,"",B{r}/{SUB})', "0.0%")
    calc(s[f"F{r}"], f'=B{r}-G{r}', BRL); calc(s[f"G{r}"], f'=SUM({RG("N")})-SUM(G{E0}:G{EF})', BRL)
    faixa(s, R0 - 1, "RESULTADO", 1, 3)
    V, A_, AI, DK, RS = "Orçamento!$C$8", "Orçamento!$C$5", "Orçamento!$C$5", "Orçamento!$C$6", "Orçamento!$C$7"
    conf = "+".join(f'COUNTIF({RG("L")},"{x}")' for x in AVISO_SIT)
    res = [
        (R0, "Subtotal dos itens", f'=SUM({RG("J")})', BRL, False),
        (R0 + 1, "Reserva para imprevistos", f"=B{R0}*N({RS})/100", BRL, False),
        (R0 + 2, "Total com reserva", f"=B{R0}+B{R0+1}", BRL, True),
        (R0 + 3, "Verba disponível", f'=IF(ISNUMBER({V}),{V},"")', BRL, False),
        (R0 + 4, "Diferença (verba − total com reserva)", f'=IF(OR(B{R0+3}="",COUNT({RG("J")})=0),"",B{R0+3}-B{R0+2})', BRL, True),
        (R0 + 5, "Leitura", (f'=IF(COUNT({RG("J")})=0,"Ainda não há itens com cotação",IF(OR(NOT(ISNUMBER({V})),N({V})<=0),"Informe a verba disponível",'
                             f'IF(ROUND(B{R0+4},2)>=0,"Cabe na verba","Passa da verba: corte, troque ou adie itens")))'), None, True),
        (R0 + 6, "Custo por m² de área interna", f'=IF(OR(NOT(ISNUMBER({AI})),N({AI})<=0,B{R0+2}=0),"",B{R0+2}/{AI})', BRL, False),
        (R0 + 7, "Custo por m² de área total (interna + deck)", f'=IF(OR(NOT(ISNUMBER({AI})),N({AI})<=0,B{R0+2}=0),"",B{R0+2}/({AI}+MAX(0,N({DK}))))', BRL, False),
        (R0 + 8, "Itens sem cotação", f'=COUNTIF({RG("L")},"Sem cotação")', "0", False),
        (R0 + 9, "Itens com só 1 cotação", f'=COUNTIF({RG("L")},"Só 1 cotação: peça mais")', "0", False),
        (R0 + 10, "Linhas para conferir", f"={conf}", "0", False),
        (R0 + 11, "Já pago", f'=B{R0}-SUM({RG("N")})', BRL, False),
        (R0 + 12, "Falta pagar (itens + reserva)", f'=SUM({RG("N")})+B{R0+1}', BRL, True),
        (R0 + 13, "Situação do orçamento", (f'=IF(N({RS})<0,"Reserva não pode ser negativa",IF(B{R0+10}>0,"Há linhas para conferir na coluna Situação",'
                                             f'IF(COUNT({RG("J")})=0,"Ainda não há itens com cotação",IF(B{R0+8}>0,"Incompleto: há itens sem cotação",'
                                             f'IF(B{R0+9}>0,"Completo, mas há itens com só 1 cotação","Completo: todos os itens com cotação")))))'), None, True),
    ]
    for l, rot, f, fmt, b in res:
        s.cell(l, 1, rot).font = T(11, b); s.cell(l, 1).alignment = WRAP; s.merge_cells(start_row=l, start_column=2, end_row=l, end_column=3)
        calc(s.cell(l, 2), f, fmt, b, 12 if b else 10)
    s.conditional_formatting.add(f"B{R0+5}", FormulaRule(formula=[f'$B${R0+5}="Cabe na verba"'], fill=PatternFill("solid", fgColor=VERDE)))
    s.conditional_formatting.add(f"B{R0+5}", FormulaRule(formula=[f'LEFT($B${R0+5},5)="Passa"'], fill=PatternFill("solid", fgColor=VERM)))
    s.conditional_formatting.add(f"B{R0+13}", FormulaRule(formula=[f'LEFT($B${R0+13},8)="Completo"'], fill=PatternFill("solid", fgColor=VERDE)))
    s.conditional_formatting.add(f"B{R0+13}", FormulaRule(formula=[f'LEFT($B${R0+13},8)<>"Completo"'], fill=PatternFill("solid", fgColor=AMAR)))
    s.freeze_panes = "A5"

def cronograma(wb):
    c = wb.create_sheet("Cronograma"); c.sheet_view.showGridLines = False
    for col, w in zip("ABCDE", (30, 18, 16, 16, 18)): c.column_dimensions[col].width = w
    c["A1"] = "Cronograma de pagamentos"; c["A1"].font = T(18, True, MUSGO)
    c["A2"] = "Quanto sai em cada mês, pelo mês informado em cada item (mês 1 = primeiro mês do projeto)."; c["A2"].font = T(10, c="5F5F55", i=True)
    cab(c, 4, ["Mês", "Previsto no mês", "Já pago", "Falta pagar", "Previsto acumulado"])
    for i in range(NMES):
        r, m = 5 + i, i + 1
        x = c.cell(r, 1, f"Mês {m}"); x.font = T(10, True); x.border = borda
        calc(c[f"B{r}"], f'=SUMIF({RG("O")},{m},{RG("J")})', BRL, True)
        calc(c[f"D{r}"], f'=SUMIF({RG("O")},{m},{RG("N")})', BRL)
        calc(c[f"C{r}"], f"=B{r}-D{r}", BRL)
        calc(c[f"E{r}"], f"=SUM($B$5:B{r})", BRL)
    r1, r2, r3 = 5 + NMES, 6 + NMES, 7 + NMES
    for r, rot in ((r1, "Sem mês definido"), (r2, "Reserva para imprevistos"), (r3, "Total")):
        x = c.cell(r, 1, rot); x.font = T(10, True, i=r != r3); x.border = borda
    calc(c[f"B{r1}"], f"=Resumo!$B${R0}-SUM(B5:B{r1-1})", BRL); calc(c[f"D{r1}"], f'=SUM({RG("N")})-SUM(D5:D{r1-1})', BRL); calc(c[f"C{r1}"], f"=B{r1}-D{r1}", BRL)
    calc(c[f"B{r2}"], f"=Resumo!$B${R0+1}", BRL); calc(c[f"C{r2}"], "=0", BRL); calc(c[f"D{r2}"], f"=B{r2}", BRL)
    for col in "BCD": calc(c[f"{col}{r3}"], f"=SUM({col}5:{col}{r2})", BRL, True)
    c.freeze_panes = "A5"

def montar(exemplo):
    wb = Workbook(); comece(wb, exemplo); orcamento(wb, exemplo); resumo(wb); cronograma(wb); wb.active = 0
    nome = "Orcamento-Cabana-Zion-EXEMPLO.xlsx" if exemplo else "Orcamento-Cabana-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

"""Gera a Ferramenta 13 · Controle de Enxoval e Reposição (Zion Hospitality Business):
   - Controle-Enxoval-Zion-EM-BRANCO.xlsx / Controle-Enxoval-Zion-EXEMPLO.xlsx (dados fictícios)
Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from itens import CATEGORIAS, UNIDADES, TIPOS, MOTIVOS, PADRAO, EX_ITENS, EX_MOV, EX_CONTAGEM
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
I0, NI = 6, 100      # itens: linhas 6..105
M0, NM = 6, 500      # movimentos: linhas 6..505
VERDE, VERM, AMAR = "C8E6C0", "F4C7C3", "FCE8B2"

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
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 13", T(10, True, TERRA)),
        ("Controle de Enxoval e Reposição", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para saber quanto enxoval e quantos itens de reposição você tem, quanto deveria ter e o que precisa comprar.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (hospedagem, quantidades e preços inventados). Use a versão em branco." if exemplo
         else "Versão em branco: a lista de itens comuns já vem pronta para você ajustar. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Para Airbnb, casas, apartamentos, pousadas e glampings.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 4 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Itens: ajuste a lista e defina o mínimo de cada item. Para enxoval, a planilha calcula: peças por unidade × unidades que usam × jogos em rotação (por exemplo, um em uso, um na lavanderia e um de reserva). Para o resto, digite o mínimo.", None),
        ("2. Aba Movimentos: lance cada entrada (compra) e cada saída (consumo, descarte, perda, dano). Uma linha por lançamento.", None),
        ("3. Aba Saldo: veja o saldo de cada item, a situação (OK, No mínimo, COMPRAR) e quanto comprar para voltar ao mínimo.", None),
        ("4. Uma vez por semana, conte o que existe de verdade e anote na coluna Contagem física. A diferença mostra perdas que não foram lançadas.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("COMO A PLANILHA DECIDE", T(12, True, MUSGO)),
        ("Saldo = entradas válidas − saídas válidas. Lançamento com item não cadastrado, sem tipo ou com quantidade zero ou negativa não entra na conta e aparece marcado na aba Movimentos.", None),
        ("COMPRAR quando o saldo está abaixo do mínimo; No mínimo quando está igual (programe a compra). Quantidade a comprar = mínimo − saldo. O mínimo é decisão sua: a planilha não sabe quantos hóspedes você vai receber.", None),
        ("", None),
        ("O QUE A PLANILHA NÃO FAZ", T(12, True, MUSGO)),
        ("Não prevê demanda, não controla a lavanderia peça por peça e não substitui a contagem física. Custos são os que você digitar; não é contabilidade.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Lógica inspirada no controle de estoque usado nas unidades da Zion. Material educativo.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Itens ----------
    it = wb.create_sheet("Itens"); it.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHI", (13, 26, 10, 12, 12, 13, 12, 12, 12)): it.column_dimensions[col].width = w
    it["A1"] = "Itens e mínimos"; it["A1"].font = T(18, True, MUSGO)
    it["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Ajuste a lista. Mínimo: preencha D, E e F (enxoval) ou digite em H."
    it["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    it["A3"] = "Jogos em rotação: quantos conjuntos de cada peça existem por cama ou banheiro (ex.: em uso, na lavanderia e reserva)."
    it["A3"].font = T(9, c="5F5F55", i=True)
    cab(it, 5, ["Categoria", "Item", "Medida", "Peças por unidade", "Unidades que usam", "Jogos em rotação", "Mínimo calculado", "Mínimo digitado (opcional)", "Custo unitário (opcional)"])
    for i in range(NI):
        r = I0 + i; base = PADRAO[i] if i < len(PADRAO) else (None, None, None)
        exv = EX_ITENS.get(base[1], (None,) * 5) if exemplo and base[1] else (None,) * 5
        for j, v in enumerate(base, 1): ent(it.cell(r, j), v)
        ent(it[f"D{r}"], exv[0]); ent(it[f"E{r}"], exv[1]); ent(it[f"F{r}"], exv[2])
        calc(it[f"G{r}"], f'=IF(AND(ISNUMBER(D{r}),ISNUMBER(E{r}),ISNUMBER(F{r}),D{r}>0,E{r}>0,F{r}>0),D{r}*E{r}*F{r},"")')
        ent(it[f"H{r}"], exv[3]); ent(it[f"I{r}"], exv[4], BRL)
    lista(it, f"A{I0}:A{I0+NI-1}", CATEGORIAS); lista(it, f"C{I0}:C{I0+NI-1}", UNIDADES)
    it.freeze_panes = f"C{I0}"

    # ---------- Movimentos ----------
    mv = wb.create_sheet("Movimentos"); mv.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFG", (13, 26, 11, 11, 20, 30, 26)): mv.column_dimensions[col].width = w
    mv["A1"] = "Entradas e saídas"; mv["A1"].font = T(18, True, MUSGO)
    mv["A2"] = "Uma linha por lançamento. Escolha o item da lista (ele precisa estar na aba Itens)."; mv["A2"].font = T(10, c="5F5F55", i=True)
    mv["A3"] = "Lançamentos com problema:"; mv["A3"].font = T(10, True)
    calc(mv["C3"], f'=COUNTIF(G{M0}:G{M0+NM-1},"Item não cadastrado")+COUNTIF(G{M0}:G{M0+NM-1},"Confira tipo e quantidade")', b=True)
    cab(mv, 5, ["Data", "Item", "Tipo", "Quantidade", "Motivo", "Observação", "Situação"])
    for r in range(M0, M0 + NM):
        for col in "ABCDEF": ent(mv[f"{col}{r}"], None, DATA if col == "A" else None)
        calc(mv[f"G{r}"], f'=IF(AND(B{r}="",D{r}=""),"",IF(COUNTIF(Itens!$B${I0}:$B${I0+NI-1},B{r})=0,"Item não cadastrado",'
                          f'IF(OR(C{r}="",NOT(ISNUMBER(D{r}))),"Confira tipo e quantidade",IF(D{r}<=0,"Confira tipo e quantidade","OK"))))', b=True)
    lista(mv, f"B{M0}:B{M0+NM-1}", ref=f"Itens!$B${I0}:$B${I0+NI-1}")
    lista(mv, f"C{M0}:C{M0+NM-1}", TIPOS); lista(mv, f"E{M0}:E{M0+NM-1}", MOTIVOS)
    rgG = f"G{M0}:G{M0+NM-1}"
    mv.conditional_formatting.add(rgG, FormulaRule(formula=[f'AND(G{M0}<>"",G{M0}<>"OK")'], fill=PatternFill("solid", fgColor=VERM)))
    mv.freeze_panes = f"A{M0}"
    if exemplo:
        for k, (d, item, tp, q, mot, obs) in enumerate(EX_MOV):
            r = M0 + k
            for col, v in zip("ABCDEF", (datetime.date.fromisoformat(d), item, tp, q, mot, obs or None)): mv[f"{col}{r}"].value = v

    # ---------- Saldo ----------
    s = wb.create_sheet("Saldo"); s.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHIJKL", (13, 26, 9, 10, 10, 10, 10, 11, 26, 13, 12, 12)): s.column_dimensions[col].width = w
    s["A1"] = "Saldo e compras"; s["A1"].font = T(18, True, MUSGO)
    s["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Tudo calculado, menos a coluna Contagem física."
    s["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    S0 = 7; rg = lambda c: f"{c}{S0}:{c}{S0+NI-1}"
    resumo = [("A3", "Itens para comprar", "C3", f'=COUNTIF({rg("I")},"COMPRAR")'),
              ("E3", "Custo estimado da compra", "H3", f'=SUM({rg("J")})'),
              ("A4", "Itens no mínimo", "C4", f'=COUNTIF({rg("I")},"No mínimo")'),
              ("E4", "Itens com diferença na contagem", "H4", f'=SUMPRODUCT(--(LEN({rg("L")})>0),--({rg("L")}<>0))'),
              ("A5", "Lançamentos com problema", "C5", "=Movimentos!C3")]
    for a, t, b, f in resumo:
        s[a] = t; s[a].font = T(10, True); calc(s[b], f, BRL if "Custo" in t else None, True)
    cab(s, 6, ["Categoria", "Item", "Medida", "Entradas", "Saídas", "Saldo", "Mínimo", "Comprar", "Situação", "Custo estimado", "Contagem física", "Diferença"])
    for i in range(NI):
        r, ir = S0 + i, I0 + i
        vazio = f'Itens!$B${ir}=""'
        calc(s[f"A{r}"], f'=IF({vazio},"",Itens!A{ir}&"")'); calc(s[f"B{r}"], f'=IF({vazio},"",Itens!B{ir}&"")'); calc(s[f"C{r}"], f'=IF({vazio},"",Itens!C{ir}&"")')
        crit = f'Movimentos!$B${M0}:$B${M0+NM-1},B{r},Movimentos!$G${M0}:$G${M0+NM-1},"OK"'
        calc(s[f"D{r}"], f'=IF(B{r}="","",SUMIFS(Movimentos!$D${M0}:$D${M0+NM-1},{crit},Movimentos!$C${M0}:$C${M0+NM-1},"Entrada"))')
        calc(s[f"E{r}"], f'=IF(B{r}="","",SUMIFS(Movimentos!$D${M0}:$D${M0+NM-1},{crit},Movimentos!$C${M0}:$C${M0+NM-1},"Saída"))')
        calc(s[f"F{r}"], f'=IF(B{r}="","",D{r}-E{r})', b=True)
        calc(s[f"G{r}"], f'=IF(B{r}="","",IF(ISNUMBER(Itens!H{ir}),Itens!H{ir},Itens!G{ir}))')
        calc(s[f"H{r}"], f'=IF(OR(B{r}="",G{r}=""),"",MAX(0,G{r}-F{r}))', b=True)
        calc(s[f"I{r}"], f'=IF(B{r}="","",IF(F{r}<0,"Confira: saídas maiores que entradas",IF(G{r}="","Defina o mínimo",IF(F{r}<G{r},"COMPRAR",IF(F{r}=G{r},"No mínimo","OK")))))', b=True)
        calc(s[f"J{r}"], f'=IF(OR(H{r}="",H{r}=0,NOT(ISNUMBER(Itens!I{ir}))),"",H{r}*Itens!I{ir})', BRL)
        ent(s[f"K{r}"], EX_CONTAGEM.get(PADRAO[i][1]) if exemplo and i < len(PADRAO) else None)
        calc(s[f"L{r}"], f'=IF(OR(B{r}="",NOT(ISNUMBER(K{r}))),"",K{r}-F{r})')
    for cond, cor in ((f'I{S0}="COMPRAR"', VERM), (f'I{S0}="No mínimo"', AMAR), (f'I{S0}="OK"', VERDE), (f'LEFT(I{S0},7)="Confira"', VERM)):
        s.conditional_formatting.add(rg("I"), FormulaRule(formula=[cond], fill=PatternFill("solid", fgColor=cor)))
    s.conditional_formatting.add(rg("L"), FormulaRule(formula=[f'AND(ISNUMBER(L{S0}),L{S0}<>0)'], fill=PatternFill("solid", fgColor=AMAR)))
    s.freeze_panes = f"C{S0}"
    s.print_title_rows = "6:6"; s.page_setup.orientation = "landscape"; s.page_setup.fitToWidth = 1; s.page_setup.fitToHeight = 0
    s.sheet_properties.pageSetUpPr.fitToPage = True

    wb.active = 0
    nome = "Controle-Enxoval-Zion-EXEMPLO.xlsx" if exemplo else "Controle-Enxoval-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

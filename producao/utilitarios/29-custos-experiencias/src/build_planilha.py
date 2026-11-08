"""Gera a Ferramenta 29 · Calculadora de Custos de Experiências (Zion Hospitality Business):
   - Custos-Experiencias-Zion-EM-BRANCO.xlsx / Custos-Experiencias-Zion-EXEMPLO.xlsx (dados fictícios)
Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dados import EX, EX_FIXOS, EX_VAR, NFIX, NVAR, NCEN
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import FormulaRule

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, PRETO, CREME, TERRA = "1B2117", "040605", "FEF5F0", "8B714E"
ENTRADA, CALC, CAB = PatternFill("solid", fgColor="FFF4C7"), PatternFill("solid", fgColor="E3EEDF"), PatternFill("solid", fgColor=MUSGO)
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)
WRAP = Alignment(wrap_text=True, vertical="center")
BRL = 'R$ #,##0.00;[Red]-R$ #,##0.00'
VERDE, VERM, AMAR = "C8E6C0", "F4C7C3", "FCE8B2"
F0, V0 = 13, 13                       # linhas das listas de custos
TF, TV = F0 + NFIX, V0 + NVAR         # linha do total (28)
R0 = TF + 3                           # início dos resultados (31)

def faixa(ws, l, txt, c1=1, c2=5):
    ws.merge_cells(start_row=l, start_column=c1, end_row=l, end_column=c2)
    c = ws.cell(l, c1, txt); c.font = T(11, True, CREME); c.fill = CAB; c.alignment = Alignment(vertical="center", indent=1)
def ent(c, v=None, fmt=None):
    c.value = v; c.fill = ENTRADA; c.border = borda; c.alignment = WRAP; c.font = T(11, True)
    if fmt: c.number_format = fmt
def calc(c, f, fmt=None, b=False, sz=11):
    c.value = f; c.fill = CALC; c.border = borda; c.alignment = WRAP; c.font = T(sz, b)
    if fmt: c.number_format = fmt

def montar(exemplo):
    wb = Workbook(); ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 104
    linhas = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 29", T(10, True, TERRA)),
        ("Calculadora de Custos de Experiências", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para calcular quanto custa cada sessão de uma experiência (passeio, café especial, aula, trilha, jantar), quanto sobra depois das taxas e a partir de quantos participantes ela se paga.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (experiência, preços e custos inventados). Use a versão em branco." if exemplo
         else "Versão em branco. Preencha as células amarelas da aba Calculadora.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Para Airbnb, casas, apartamentos, pousadas, glampings e quem oferece experiências.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 4 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Calculadora, topo: nome da experiência, preço por participante, taxa sobre a venda (plataforma, cartão ou comissão, em %), impostos (%), capacidade e participantes previstos.", None),
        ("2. Custos da sessão: o que você paga por saída, não importa quantas pessoas vão (guia, transporte, aluguel do espaço, seguro do grupo).", None),
        ("3. Custos por participante: o que aumenta a cada pessoa (comida, ingresso, kit, material).", None),
        ("4. Leia os resultados e a aba Cenários: quanto sobra com cada número de participantes, quantos são necessários para cobrir a sessão e qual o preço mínimo para os participantes previstos.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("AS CONTAS", T(12, True, MUSGO)),
        ("Receita = preço × participantes. Taxas e impostos = receita × (taxa + impostos). Contribuição da sessão = receita − taxas e impostos − custos por participante − custos da sessão.", None),
        ("Participantes mínimos = custos da sessão ÷ (preço × (1 − taxa − impostos) − custo por participante), arredondado para cima. Preço mínimo = (custos da sessão ÷ participantes + custo por participante) ÷ (1 − taxa − impostos).", None),
        ("", None),
        ("O QUE A PLANILHA NÃO FAZ", T(12, True, MUSGO)),
        ("Contribuição não é lucro: não inclui seu tempo, as despesas fixas do mês do negócio, a divulgação nem o imposto de renda. Não diz quantas pessoas vão comprar nem garante a capacidade: segurança, licenças e seguros dependem de cada atividade e do profissional responsável.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo. Não garante vendas, reservas nem resultado financeiro.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    c = wb.create_sheet("Calculadora"); c.sheet_view.showGridLines = False
    for col, w in zip("ABCDE", (40, 18, 3, 34, 18)): c.column_dimensions[col].width = w
    c["A1"] = "Calculadora de custos da experiência"; c["A1"].font = T(18, True, MUSGO)
    c["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Preencha as células amarelas."; c["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    campos = [(4, "Nome da experiência", "nome", None), (5, "Preço por participante (R$)", "preco", BRL), (6, "Taxa sobre a venda (%)", "taxa", "0.0"),
              (7, "Impostos sobre a venda (%)", "imposto", "0.0"), (8, "Capacidade informada (pessoas por sessão)", "capacidade", "0"), (9, "Participantes previstos", "previstos", "0")]
    ajuda = {6: "Plataforma, cartão ou comissão. Digite 5 para 5%.", 7: "Pergunte ao seu contador. Use 0 se não se aplica.", 8: "Quantas pessoas cabem com segurança, informado por você ou pelo responsável."}
    for l, r, k, fmt in campos:
        c.cell(l, 1, r).font = T(11); ent(c.cell(l, 2), EX[k] if exemplo else None, fmt)
        if l in ajuda: h = c.cell(l, 4, ajuda[l]); h.font = T(9, c="5F5F55", i=True); h.alignment = WRAP
    faixa(c, 11, "CUSTOS DA SESSÃO (R$ por saída)", 1, 2); faixa(c, 11, "CUSTOS POR PARTICIPANTE (R$ por pessoa)", 4, 5)
    c["A12"], c["B12"], c["D12"], c["E12"] = "Item", "Valor", "Item", "Valor"
    for k in ("A12", "B12", "D12", "E12"): c[k].font = T(9, True, TERRA)
    for i in range(NFIX):
        it = EX_FIXOS[i] if exemplo and i < len(EX_FIXOS) else (None, None)
        ent(c.cell(F0 + i, 1), it[0]); ent(c.cell(F0 + i, 2), it[1], BRL)
    for i in range(NVAR):
        it = EX_VAR[i] if exemplo and i < len(EX_VAR) else (None, None)
        ent(c.cell(V0 + i, 4), it[0]); ent(c.cell(V0 + i, 5), it[1], BRL)
    c.cell(TF, 1, "Total por sessão").font = T(10, True); calc(c.cell(TF, 2), f"=SUM(B{F0}:B{TF-1})", BRL, True)
    c.cell(TV, 4, "Total por participante").font = T(10, True); calc(c.cell(TV, 5), f"=SUM(E{V0}:E{TV-1})", BRL, True)
    FX, CV, K = f"$B${TF}", f"$E${TV}", "(1-(N($B$6)+N($B$7))/100)"
    faixa(c, R0 - 1, "RESULTADO DA SESSÃO COM OS PARTICIPANTES PREVISTOS", 1, 5)
    sit = (f'=IF(OR(NOT(ISNUMBER(B5)),B5<=0),"Informe o preço por participante",IF(OR(NOT(ISNUMBER(B9)),B9<1),"Informe os participantes previstos (1 ou mais)",'
           f'IF(N(B6)+N(B7)>=100,"Taxa e impostos precisam somar menos de 100%",IF(OR(N(B6)<0,N(B7)<0,{FX}<0,{CV}<0),"Há valor negativo: confira",'
           f'IF(AND(ISNUMBER(B8),B9>B8),"Participantes acima da capacidade informada","OK")))))')
    ok = f'$B${R0}<>"OK"'
    res = [
        (R0, "Situação dos dados", sit, None, True),
        (R0 + 1, "Receita da sessão", f'=IF({ok},"",B5*B9)', BRL, False),
        (R0 + 2, "Taxas e impostos", f'=IF({ok},"",B{R0+1}*(1-{K}))', BRL, False),
        (R0 + 3, "Custos por participante (total)", f'=IF({ok},"",{CV}*B9)', BRL, False),
        (R0 + 4, "Custos da sessão", f'=IF({ok},"",{FX})', BRL, False),
        (R0 + 5, "Contribuição da sessão", f'=IF({ok},"",B{R0+1}-B{R0+2}-B{R0+3}-B{R0+4})', BRL, True),
        (R0 + 6, "Contribuição por participante", f'=IF({ok},"",B{R0+5}/B9)', BRL, False),
        (R0 + 7, "Leitura", f'=IF({ok},"",IF(ROUND(B{R0+5},2)<0,"Não cobre os custos desta sessão",IF(ROUND(B{R0+5},2)=0,"Empata: não sobra nada","Cobre os custos e sobra a contribuição acima")))', None, True),
        (R0 + 9, "Quanto sobra de cada participante, antes dos custos da sessão", f'=IF({ok},"",B5*{K}-{CV})', BRL, False),
        (R0 + 10, "Participantes mínimos para cobrir a sessão", f'=IF({ok},"",IF(B{R0+9}<=0,"O preço não cobre o custo por participante",IF({FX}=0,1,ROUNDUP({FX}/B{R0+9},0))))', "0", True),
        (R0 + 11, "Cabe na capacidade?", f'=IF(OR({ok},NOT(ISNUMBER(B{R0+10}))),"",IF(NOT(ISNUMBER(B8)),"Informe a capacidade",IF(B{R0+10}<=B8,"Sim","Não: nem com a capacidade cheia")))', None, False),
        (R0 + 12, "Preço mínimo para os participantes previstos", f'=IF({ok},"",({FX}/B9+{CV})/{K})', BRL, True),
    ]
    for l, r, f, fmt, b in res:
        c.cell(l, 1, r).font = T(11, b); c.cell(l, 1).alignment = WRAP; calc(c.cell(l, 2), f, fmt, b, 13 if b else 11)
    c.conditional_formatting.add(f"B{R0}", FormulaRule(formula=[f'$B${R0}="OK"'], fill=PatternFill("solid", fgColor=VERDE)))
    c.conditional_formatting.add(f"B{R0}", FormulaRule(formula=[f'$B${R0}<>"OK"'], fill=PatternFill("solid", fgColor=VERM)))
    c.conditional_formatting.add(f"B{R0+7}", FormulaRule(formula=[f'LEFT($B${R0+7},4)="Não "'], fill=PatternFill("solid", fgColor=VERM)))
    c.conditional_formatting.add(f"B{R0+7}", FormulaRule(formula=[f'LEFT($B${R0+7},5)="Cobre"'], fill=PatternFill("solid", fgColor=VERDE)))
    c.freeze_panes = "A4"

    s = wb.create_sheet("Cenários"); s.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFG", (14, 14, 14, 16, 14, 16, 22)): s.column_dimensions[col].width = w
    s["A1"] = "Cenários por número de participantes"; s["A1"].font = T(18, True, MUSGO)
    s["A2"] = '=IF(OR(NOT(ISNUMBER(Calculadora!B5)),Calculadora!B5<=0,N(Calculadora!B6)+N(Calculadora!B7)>=100),"Preencha preço, taxa e impostos na Calculadora","Mesma experiência, preço e custos; só muda o número de participantes (até a capacidade informada).")'
    s["A2"].font = T(10, c="5F5F55", i=True)
    hdr = ["Participantes", "Receita", "Taxas e impostos", "Custos por participante", "Custos da sessão", "Contribuição", "Leitura"]
    for j, t in enumerate(hdr, 1):
        cc = s.cell(4, j, t); cc.font = T(10, True, CREME); cc.fill = CAB; cc.alignment = WRAP; cc.border = borda
    P = "Calculadora!$B$5"; CAP = "Calculadora!$B$8"; FXs, CVs = f"Calculadora!{FX}", f"Calculadora!{CV}"
    Ks = "(1-(N(Calculadora!$B$6)+N(Calculadora!$B$7))/100)"
    valido = f'AND(ISNUMBER({P}),{P}>0,N(Calculadora!$B$6)+N(Calculadora!$B$7)<100)'
    for i in range(NCEN):
        r, n = 5 + i, i + 1
        calc(s[f"A{r}"], f'=IF(AND({valido},OR(NOT(ISNUMBER({CAP})),{n}<={CAP})),{n},"")', "0", True)
        calc(s[f"B{r}"], f'=IF(A{r}="","",{P}*A{r})', BRL)
        calc(s[f"C{r}"], f'=IF(A{r}="","",B{r}*(1-{Ks}))', BRL)
        calc(s[f"D{r}"], f'=IF(A{r}="","",{CVs}*A{r})', BRL)
        calc(s[f"E{r}"], f'=IF(A{r}="","",{FXs})', BRL)
        calc(s[f"F{r}"], f'=IF(A{r}="","",B{r}-C{r}-D{r}-E{r})', BRL, True)
        calc(s[f"G{r}"], f'=IF(A{r}="","",IF(ROUND(F{r},2)<0,"Não cobre",IF(ROUND(F{r},2)=0,"Empata","Cobre")))', None, True)
    rg = f"G5:G{4+NCEN}"
    s.conditional_formatting.add(rg, FormulaRule(formula=['G5="Não cobre"'], fill=PatternFill("solid", fgColor=VERM)))
    s.conditional_formatting.add(rg, FormulaRule(formula=['G5="Cobre"'], fill=PatternFill("solid", fgColor=VERDE)))
    s.conditional_formatting.add(rg, FormulaRule(formula=['G5="Empata"'], fill=PatternFill("solid", fgColor=AMAR)))
    s.freeze_panes = "A5"

    wb.active = 0
    nome = "Custos-Experiencias-Zion-EXEMPLO.xlsx" if exemplo else "Custos-Experiencias-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

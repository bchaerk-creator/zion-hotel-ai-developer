"""Gera a planilha "Diária Mínima e Controle do Mês" (Zion Hotel Academy) em duas versões:
   - Diaria-Minima-Zion-EM-BRANCO.xlsx
   - Diaria-Minima-Zion-EXEMPLO.xlsx (dados fictícios, identificados como exemplo)
Uso: python3 -I build_planilha.py <pasta-saida>"""
import sys, pathlib, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, AREIA, DOURADO, PRETO, CREME = "1B2117", "DED6BF", "8B714E", "040605", "FEF5F0"
ENTRADA = PatternFill("solid", fgColor="FFF4C7")      # amarelo claro = você preenche
CALC = PatternFill("solid", fgColor="E3EEDF")         # verde claro = calculado
CAB = PatternFill("solid", fgColor=MUSGO)
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
BRL = 'R$ #,##0.00;[Red]-R$ #,##0.00'
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)

def faixa(ws, linha, texto, cols=4):
    ws.merge_cells(start_row=linha, start_column=1, end_row=linha, end_column=cols)
    c = ws.cell(linha, 1, texto); c.font = T(11, True, CREME); c.fill = CAB; c.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[linha].height = 22

def rotulo(ws, l, texto, ajuda=""):
    a = ws.cell(l, 1, texto); a.font = T(11); a.alignment = Alignment(wrap_text=True, vertical="center")
    if ajuda: h = ws.cell(l, 3, ajuda); h.font = T(9, c="5F5F55", i=True); h.alignment = Alignment(wrap_text=True, vertical="center")

def entrada(ws, l, valor=None, fmt=BRL):
    c = ws.cell(l, 2, valor); c.fill = ENTRADA; c.border = borda; c.number_format = fmt; c.font = T(12, True); return c

def calc(ws, l, formula, fmt=BRL, destaque=False):
    c = ws.cell(l, 2, formula); c.fill = CALC; c.border = borda; c.number_format = fmt; c.font = T(14 if destaque else 11, True, MUSGO if destaque else PRETO); return c

def montar(exemplo):
    wb = Workbook()
    # ---------------- Comece aqui ----------------
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 100
    linhas = [
        ("ZION HOTEL ACADEMY · FERRAMENTA 01", T(10, True, DOURADO)),
        ("Diária Mínima e Controle do Mês", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para descobrir a menor diária que cobre seus custos e taxas, e acompanhe quanto sobrou no mês.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS. Use a versão em branco para os seus números." if exemplo else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("", None),
        ("COMO USAR EM 3 PASSOS (cerca de 10 minutos)", T(12, True, MUSGO)),
        ("1. Aba Calculadora: preencha as células amarelas com seus custos, a taxa da plataforma e as noites que espera vender. A diária mínima aparece em verde.", None),
        ("2. Ainda na Calculadora: use o simulador de desconto antes de baixar o preço, para ver quantas noites a mais o desconto exige.", None),
        ("3. Aba Reservas: lance cada reserva. A aba Resumo do mês mostra ocupação, diária efetiva e quanto sobrou.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("ANTES DE COMEÇAR: A TAXA DA PLATAFORMA", T(12, True, MUSGO)),
        ("Confira no extrato de pagamentos qual percentual a plataforma desconta de você. No Airbnb ele muda conforme o modelo de cobrança da sua conta (taxa dividida ou taxa única). Use o número do seu extrato, não um valor genérico.", None),
        ("", None),
        ("O QUE A PLANILHA FAZ E O QUE ELA NÃO FAZ", T(12, True, MUSGO)),
        ("Faz: calcula a diária que empata seus custos, a diária para a sua meta, o efeito de um desconto e o resultado de cada mês com os números que você lança.", None),
        ("Não faz: não prevê quantas noites você vai vender, não conhece os preços da sua região e não substitui o seu contador. \"Sobra no mês\" não é lucro líquido: não inclui depreciação, imposto de renda pessoal, financiamento nem o seu tempo, a menos que você os some nos custos fixos.", None),
        ("Premissa do resumo: cada reserva conta no mês da data de entrada.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice.", T(10, c="5F5F55", i=True)),
        ("Zion Hotel Academy · Bruno Chaerk · Material educativo: não garante reservas, ocupação nem faturamento.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")
    # ---------------- Calculadora ----------------
    c = wb.create_sheet("Calculadora"); c.sheet_view.showGridLines = False
    for col, w in zip("ABCD", (46, 20, 58, 4)): c.column_dimensions[col].width = w
    c["A1"] = "Calculadora de Diária Mínima"; c["A1"].font = T(18, True, MUSGO)
    c["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Preencha as células amarelas"; c["A2"].font = T(10, True, "A0522D" if exemplo else DOURADO)
    faixa(c, 4, "1 · SEUS NÚMEROS DO MÊS")
    ex = dict(fixos=1850, limp=120, limpcob=90, var=38, taxa=16, imp=6, noites=14, estadia=2.5, meta=2500, atual=420, desc=15) if exemplo else {}
    campos = [
        (5, "Custos fixos do mês (R$)", "Condomínio, IPTU, internet, luz e água básicas, contador, parcelas.", "fixos", BRL),
        (6, "Custo de limpeza por estadia (R$)", "O que você PAGA por limpeza e lavanderia a cada saída de hóspede.", "limp", BRL),
        (7, "Taxa de limpeza cobrada do hóspede (R$)", "O que você COBRA por estadia. Use 0 se a limpeza já está embutida na diária.", "limpcob", BRL),
        (8, "Outros custos por noite ocupada (R$)", "Energia e gás extras, amenities, café, lenha.", "var", BRL),
        (9, "Taxa da plataforma (%)", "Digite só o número. Ex.: 16 para 16%. Confira no seu extrato.", "taxa", '0.0'),
        (10, "Impostos sobre a receita (%)", "Digite só o número. Use 0 se não se aplica. Pergunte ao seu contador.", "imp", '0.0'),
        (11, "Noites que espera vender no mês", "Uma estimativa realista, com base nos seus meses anteriores.", "noites", '0'),
        (12, "Estadia média (noites por reserva)", "Ex.: 2,5 se a maioria fica 2 ou 3 noites.", "estadia", '0.0'),
        (13, "Meta: quanto quer que sobre no mês (R$)", "Depois de pagar todos os custos acima. Use 0 para ver só o empate.", "meta", BRL),
    ]
    for l, r, a, k, f in campos: rotulo(c, l, r, a); entrada(c, l, ex.get(k), f)
    faixa(c, 15, "2 · RESULTADO")
    rotulo(c, 16, "Situação dos dados")
    cs = c.cell(16, 2, '=IF(COUNTBLANK(B5:B13)>0,"Preencha todas as células amarelas",IF(MIN(B5:B13)<0,"Há valor negativo",IF(B9+B10>=100,"Taxa + impostos chegam a 100%",IF(B11<=0,"Noites do mês precisam ser maiores que zero",IF(B12<=0,"Estadia média precisa ser maior que zero",IF(B12>B11,"Estadia média maior que as noites do mês",IF(B11>31,"Um mês tem no máximo 31 noites","OK")))))))')
    cs.font = T(11, True); cs.border = borda; cs.fill = CALC
    OKF = lambda f: '=IF($B$16="OK",' + f + ',"")'
    rotulo(c, 17, "Reservas no mês (estimativa)", "Noites ÷ estadia média.")
    calc(c, 17, OKF("B11/B12"), '0.0')
    rotulo(c, 18, "Quanto fica com você de cada R$ 1 recebido", "1 − taxa da plataforma − impostos.")
    calc(c, 18, OKF("1-(B9+B10)/100"), '0.0%')
    rotulo(c, 19, "DIÁRIA MÍNIMA PARA EMPATAR", "Abaixo dela, o mês não cobre os custos informados.")
    calc(c, 19, OKF("(B5+B17*B6+B11*B8-B17*B7*B18)/(B11*B18)"), BRL, True)
    rotulo(c, 20, "DIÁRIA PARA ATINGIR A META", "A diária que deixa a sobra que você definiu.")
    calc(c, 20, OKF("(B5+B13+B17*B6+B11*B8-B17*B7*B18)/(B11*B18)"), BRL, True)
    rotulo(c, 21, "Preço de uma estadia média para o hóspede", "Diária da meta × estadia média + taxa de limpeza (sem as taxas cobradas do hóspede pela plataforma).")
    calc(c, 21, OKF("B20*B12+B7"))
    faixa(c, 23, "3 · MEMÓRIA DO CÁLCULO (com a diária da meta)")
    mem = [(24, "Receita do mês (diárias + limpeza cobrada)", "B20*B11+B7*B17"), (25, "(−) Taxa da plataforma", "-B24*B9/100"), (26, "(−) Impostos", "-B24*B10/100"),
           (27, "(−) Limpeza paga", "-B17*B6"), (28, "(−) Outros custos por noite", "-B11*B8"), (29, "(−) Custos fixos", "-B5"), (30, "(=) Sobra no mês", "SUM(B24:B29)")]
    for l, r, f in mem: rotulo(c, l, r); calc(c, l, OKF(f))
    rotulo(c, 31, "Conferência", "A sobra calculada deve ser igual à meta.")
    calc(c, 31, '=IF($B$16="OK",IF(ABS(B30-B13)<0.01,"Confere com a meta","Revise"),"")', "@")
    faixa(c, 33, "4 · SIMULADOR DE DESCONTO")
    rotulo(c, 34, "Diária que você cobra hoje (R$)"); entrada(c, 34, ex.get("atual"))
    rotulo(c, 35, "Desconto que pensa em dar (%)", "Digite só o número. Ex.: 15 para 15%."); entrada(c, 35, ex.get("desc"), '0.0')
    OKD = lambda f: '=IF(AND($B$16="OK",ISNUMBER(B34),ISNUMBER(B35),B34>0,B35>=0,B35<100),' + f + ',"")'
    rotulo(c, 36, "Margem por noite hoje", "O que sobra de cada noite antes dos custos fixos.")
    calc(c, 36, OKD("B34*B18-B8-(B6-B7*B18)/B12"))
    rotulo(c, 37, "Diária com desconto"); calc(c, 37, OKD("B34*(1-B35/100)"))
    rotulo(c, 38, "Margem por noite com desconto"); calc(c, 38, OKD("B37*B18-B8-(B6-B7*B18)/B12"))
    rotulo(c, 39, "NOITES NECESSÁRIAS PARA MANTER A MESMA MARGEM", "Comparado às noites que você espera vender sem desconto.")
    calc(c, 39, OKD('IF(B38<=0,"Com esse desconto cada noite dá prejuízo",IF(B36<=0,"Hoje a margem por noite já é negativa",B11*B36/B38))'), '0.0', True)
    rotulo(c, 40, "Noites a mais que o desconto exige"); calc(c, 40, OKD('IF(ISNUMBER(B39),B39-B11,"")'), '0.0')
    c.cell(42, 1, "Estimativas a partir dos seus números. Não preveem a demanda: vender as noites a mais depende do mercado e da época.").font = T(9, c="5F5F55", i=True)
    c.conditional_formatting.add("B16", FormulaRule(formula=['$B$16<>"OK"'], fill=PatternFill("solid", fgColor="F8E3DE"), font=Font(color="9B2C1F", bold=True)))
    dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, errorTitle="Valor inválido", error="Use um número maior ou igual a zero.")
    c.add_data_validation(dv); dv.add("B5:B13"); dv.add("B34")
    dvp = DataValidation(type="decimal", operator="between", formula1="0", formula2="99.9", showErrorMessage=True, errorTitle="Percentual inválido", error="Digite um número entre 0 e 99,9.")
    c.add_data_validation(dvp); dvp.add("B9:B10"); dvp.add("B35")
    # ---------------- Reservas ----------------
    r = wb.create_sheet("Reservas"); r.sheet_view.showGridLines = False; r.freeze_panes = "A3"
    cab = ["Data de entrada", "Hóspede ou código", "Canal", "Noites", "Valor das diárias (R$)", "Limpeza cobrada (R$)", "Taxa do canal (%)", "Limpeza paga (R$)",
           "Taxa do canal (R$)", "Impostos (R$)", "Outros custos (R$)", "Margem da reserva (R$)", "Diária efetiva (R$)"]
    larg = [14, 20, 12, 8, 16, 14, 12, 14, 14, 12, 14, 16, 14]
    r["A1"] = "Reservas · lance uma por linha (amarelo). O restante é calculado." + ("  ·  EXEMPLO FICTÍCIO" if exemplo else ""); r["A1"].font = T(12, True, MUSGO)
    for i, (h, w) in enumerate(zip(cab, larg), 1):
        x = r.cell(2, i, h); x.font = T(10, True, CREME); x.fill = CAB; x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); x.border = borda
        r.column_dimensions[x.column_letter].width = w
    r.row_dimensions[2].height = 34
    N = 200
    for l in range(3, 3 + N):
        for col in range(1, 9):
            x = r.cell(l, col); x.fill = ENTRADA; x.border = borda
        r.cell(l, 1).number_format = "DD/MM/YYYY"
        for col in (5, 6, 8): r.cell(l, col).number_format = BRL
        r.cell(l, 7).number_format = "0.0"
        f = {9: f'=IF(OR(A{l}="",D{l}=""),"",(E{l}+F{l})*G{l}/100)', 10: f'=IF(OR(A{l}="",D{l}=""),"",(E{l}+F{l})*Calculadora!$B$10/100)',
             11: f'=IF(OR(A{l}="",D{l}=""),"",D{l}*Calculadora!$B$8)', 12: f'=IF(OR(A{l}="",D{l}=""),"",E{l}+F{l}-I{l}-J{l}-H{l}-K{l})',
             13: f'=IF(OR(A{l}="",D{l}="",D{l}=0),"",E{l}/D{l})'}
        for col, fo in f.items():
            x = r.cell(l, col, fo); x.fill = CALC; x.border = borda; x.number_format = BRL
    dvd = DataValidation(type="date", operator="greaterThan", formula1="36526", showErrorMessage=True, error="Use uma data (dd/mm/aaaa).")
    dvn = DataValidation(type="whole", operator="between", formula1="1", formula2="365", showErrorMessage=True, error="Noites: número inteiro de 1 a 365.")
    dvc = DataValidation(type="list", formula1='"Airbnb,Booking,Direto,Outro"', allow_blank=True)
    dvv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, error="Use um valor maior ou igual a zero.")
    dvt = DataValidation(type="decimal", operator="between", formula1="0", formula2="99.9", showErrorMessage=True, error="Digite um número entre 0 e 99,9.")
    for d in (dvd, dvn, dvc, dvv, dvt): r.add_data_validation(d)
    dvd.add(f"A3:A{2+N}"); dvn.add(f"D3:D{2+N}"); dvc.add(f"C3:C{2+N}"); dvv.add(f"E3:F{2+N}"); dvv.add(f"H3:H{2+N}"); dvt.add(f"G3:G{2+N}")
    if exemplo:
        base = datetime.date(2026, 11, 1)
        exs = [(2, "Ana e Leo", "Airbnb", 3, 1260, 90, 16, 120), (6, "Código 4821", "Airbnb", 2, 840, 90, 16, 120), (13, "Família Souza", "Booking", 2, 900, 90, 15, 120),
               (20, "Marina", "Direto", 4, 1520, 90, 0, 120), (23, "Código 5112", "Airbnb", 2, 840, 90, 16, 120), (27, "Carlos", "Airbnb", 3, 1170, 90, 16, 120)]
        for i, (d, h, ca, n, v, lc, tx, lp) in enumerate(exs):
            l = 3 + i
            for col, val in zip(range(1, 9), (base + datetime.timedelta(days=d), h, ca, n, v, lc, tx, lp)): r.cell(l, col, val)
    # ---------------- Resumo do mês ----------------
    s = wb.create_sheet("Resumo do mês"); s.sheet_view.showGridLines = False
    for col, w in zip("ABC", (44, 20, 54)): s.column_dimensions[col].width = w
    s["A1"] = "Resumo do mês"; s["A1"].font = T(18, True, MUSGO)
    s["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Escolha o mês e informe as noites disponíveis"; s["A2"].font = T(10, True, "A0522D" if exemplo else DOURADO)
    faixa(s, 4, "MÊS ANALISADO", 3)
    rotulo(s, 5, "Primeiro dia do mês (dd/mm/aaaa)", "Ex.: 01/11/2026."); e = entrada(s, 5, datetime.date(2026, 11, 1) if exemplo else None, "DD/MM/YYYY")
    rotulo(s, 6, "Noites disponíveis no mês", "Noites abertas para reserva. Não conte bloqueios seus."); entrada(s, 6, 28 if exemplo else None, "0")
    faixa(s, 8, "RESULTADO DO MÊS (reservas com entrada no mês)", 3)
    R = "Reservas!"; per = f'{R}$A$3:$A$202,">="&$B$5,{R}$A$3:$A$202,"<"&EOMONTH($B$5,0)+1'
    ok = 'AND(ISNUMBER($B$5),ISNUMBER($B$6),$B$6>0)'
    res = [(9, "Reservas no mês", f'COUNTIFS({per})', "0"), (10, "Noites ocupadas", f'SUMIFS({R}$D$3:$D$202,{per})', "0"),
           (11, "Taxa de ocupação", 'IF(B10>B6,"Noites ocupadas passam das disponíveis",B10/B6)', "0.0%"),
           (12, "Receita (diárias + limpeza cobrada)", f'SUMIFS({R}$E$3:$E$202,{per})+SUMIFS({R}$F$3:$F$202,{per})', BRL),
           (13, "Diária efetiva média", f'IF(B10=0,"",SUMIFS({R}$E$3:$E$202,{per})/B10)', BRL),
           (14, "Margem das reservas", f'SUMIFS({R}$L$3:$L$202,{per})', BRL), (15, "(−) Custos fixos (da Calculadora)", 'IF(ISNUMBER(Calculadora!$B$5),-Calculadora!$B$5,0)', BRL),
           (16, "(=) SOBRA NO MÊS", 'B14+B15', BRL), (17, "Comparação com a diária mínima", 'IF(OR(B13="",NOT(ISNUMBER(Calculadora!$B$19))),"",IF(B13>=Calculadora!$B$19,"Diária efetiva acima da mínima","Diária efetiva abaixo da mínima"))', "@")]
    for l, rt, fo, fm in res:
        rotulo(s, l, rt); calc(s, l, f'=IF({ok},{fo},"")', fm, l == 16)
    s.cell(18, 1, "Sobra no mês não é lucro líquido. Cada reserva conta no mês da data de entrada.").font = T(9, c="5F5F55", i=True)
    return wb

for exemplo, nome in ((False, "Diaria-Minima-Zion-EM-BRANCO.xlsx"), (True, "Diaria-Minima-Zion-EXEMPLO.xlsx")):
    wb = montar(exemplo); wb.active = 0 if not exemplo else 1; wb.save(OUT / nome); print("ok", OUT / nome)

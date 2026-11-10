"""Gera a planilha "Tabela de Preço e Canais" (Jornada 2 · Gestão · Módulo 3 · Preço, reservas e distribuição) em duas versões:
   - Tabela-de-Preco-e-Canais-Zion-EM-BRANCO.xlsx
   - Tabela-de-Preco-e-Canais-Zion-EXEMPLO.xlsx (dados fictícios, identificados como exemplo)
Uso: python3 -I build_planilha.py <pasta-saida>
Molde: producao/jornada2/02-financas/src/build_planilha.py (amarelo = preenche, verde = calculado).
Abas: Comece aqui · Custo e Referência · Mapa de Canais · Piso · Calendário 12 meses · Datas de pico · Resumo · Checklist da revisão."""
import sys, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, DOURADO, PRETO, CREME = "1B2117", "8B714E", "040605", "FEF5F0"
ENTRADA = PatternFill("solid", fgColor="FFF4C7"); CALC = PatternFill("solid", fgColor="E3EEDF"); CAB = PatternFill("solid", fgColor=MUSGO)
ALERTA = PatternFill("solid", fgColor="F8E3DE")
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
BRL = 'R$ #,##0.00;[Red]-R$ #,##0.00'
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)

def faixa(ws, linha, texto, cols=3):
    ws.merge_cells(start_row=linha, start_column=1, end_row=linha, end_column=cols)
    c = ws.cell(linha, 1, texto); c.font = T(11, True, CREME); c.fill = CAB; c.alignment = Alignment(vertical="center", indent=1); ws.row_dimensions[linha].height = 22
def rotulo(ws, l, texto, ajuda="", col_ajuda=3):
    a = ws.cell(l, 1, texto); a.font = T(11); a.alignment = Alignment(wrap_text=True, vertical="center")
    if ajuda: h = ws.cell(l, col_ajuda, ajuda); h.font = T(9, c="5F5F55", i=True); h.alignment = Alignment(wrap_text=True, vertical="center")
def entrada(ws, l, valor=None, fmt=BRL, col=2):
    c = ws.cell(l, col, valor); c.fill = ENTRADA; c.border = borda; c.number_format = fmt; c.font = T(12, True); return c
def calc(ws, l, formula, fmt=BRL, destaque=False, col=2):
    c = ws.cell(l, col, formula); c.fill = CALC; c.border = borda; c.number_format = fmt; c.font = T(14 if destaque else 11, True, MUSGO if destaque else PRETO); c.alignment = Alignment(wrap_text=True, vertical="center"); return c
def cab(ws, linha, titulos, larguras=None, altura=34):
    for i, t in enumerate(titulos, 1):
        x = ws.cell(linha, i, t); x.font = T(10, True, CREME); x.fill = CAB; x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); x.border = borda
        if larguras: ws.column_dimensions[x.column_letter].width = larguras[i - 1]
    ws.row_dimensions[linha].height = altura
def alerta(ws, ref):
    ws.conditional_formatting.add(ref, FormulaRule(formula=[f'${ref[0]}${ref[1:]}<>"OK"'], fill=ALERTA, font=Font(color="9B2C1F", bold=True)))
def nota(ws, l, texto):
    c = ws.cell(l, 1, texto); c.font = T(9, c="5F5F55", i=True); c.alignment = Alignment(wrap_text=True)

# Exemplo didático · dados fictícios (Cabanas do Vale). Mesmos valores da ficha (src/logic.js) e do PLANO seção 9.
EX = dict(cv=28.32, cpn=153.04, ne=2.32, imposto=6, receita=16240, atual=280, conc=[270, 280, 290, 300, 310, 320, 360], terco="Meio", ref=300,
          canais=[("Plataforma A", 50, 16, 1.5, 0, "Não"), ("Plataforma B", 20, 15, 1.5, 0, "Não"), ("Venda direta (site e WhatsApp)", 30, 0, 1.5, 0, "Sim")],
          meta=40, prazo="30/06/2027", gestor="Sim", motor="Não", margem=10, piso=225, quem="Eu e quem responde o WhatsApp",
          cond=["Terceira noite com café da manhã incluso", "Saída tardia até as 14 h", "Cesta de boas-vindas com produtos da região"],
          fatores=dict(Vale=0.75, Baixa=0.90, Alta=1.50, Pico=2.20), ano=2027, inicio=1,
          meses=[("Baixa", "Base"), ("Baixa", "Base"), ("Vale", "Baixa"), ("Vale", "Baixa"), ("Vale", "Base"), ("Base", "Alta"), ("Alta", "Alta"), ("Base", "Alta"), ("Baixa", "Base"), ("Baixa", "Base"), ("Vale", "Baixa"), ("Baixa", "Base")],
          picos=[("Carnaval", 2, 4, 2.2, 4, "3 a 5 meses antes"), ("Corpus Christi (feriado prolongado)", 5, 4, 1.9, 3, "2 a 4 meses antes"), ("Festival de inverno (evento local)", 7, 3, 2.0, 2, "assim que a data sair"), ("Réveillon", 12, 5, 2.4, 5, "4 a 6 meses antes")])

CR = "'Custo e Referência'!"; MC = "'Mapa de Canais'!"; PI = "Piso!"; CA = "'Calendário 12 meses'!"; DP = "'Datas de pico'!"
REF = CR + "$B$26"; CV = CR + "$B$5"; CPN = CR + "$B$6"; NE = f"IF({CR}$B$7>0,{CR}$B$7,1)"; IMP = CR + "$B$8"
L1, L2 = 5, 9      # linhas dos canais
P1, P2 = 5, 12     # linhas das datas de pico
M1, M2 = 14, 25    # linhas dos meses

def montar(exemplo):
    e = EX if exemplo else {}
    wb = Workbook()
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False; ws.column_dimensions["A"].width = 100
    linhas = [
        ("ZION HOSPITALITY BUSINESS · JORNADA 2 · GESTÃO · MÓDULO 3 · PREÇO, RESERVAS E DISTRIBUIÇÃO", T(10, True, DOURADO)),
        ("Tabela de Preço e Canais", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para declarar o piso da sua diária por escrito, montar o calendário de doze meses com cinco faixas e as datas de pico, e saber quanto cada canal deixa por noite, com uma meta de venda direta.", T(11, c="2D352A")),
        ("EXEMPLO DIDÁTICO PREENCHIDO COM DADOS FICTÍCIOS (Cabanas do Vale). Use a versão em branco para os seus números." if exemplo else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("", None),
        ("COMO USAR EM 5 PASSOS (cerca de 30 minutos na primeira vez, 2 horas por trimestre na revisão)", T(12, True, MUSGO)),
        ("1. Aba Custo e Referência: o custo variável por noite e o custo por noite vendida da sua Folha Única do Mês (Módulo 2), e o preço de seis a nove concorrentes diretos numa data de demanda média. A planilha descarta o mais caro e o mais barato e sugere a referência na posição que você escolher.", None),
        ("2. Aba Mapa de Canais: quanto da receita entrou por cada canal nos últimos três meses, a comissão e a taxa de pagamento. A planilha mostra o líquido por noite de cada canal e a comissão média. Escreva a sua meta de venda direta, com prazo.", None),
        ("3. Aba Piso: a sua margem mínima e o piso, por escrito. O piso cobre o custo da noite no canal mais caro.", None),
        ("4. Abas Calendário 12 meses e Datas de pico: os fatores das cinco faixas, a faixa de cada mês (meio de semana e fim de semana) e as datas de pico com preço, mínimo de noites e quando abrir.", None),
        ("5. Aba Resumo: confira a causa principal e marque a revisão trimestral no Checklist.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("O QUE A PLANILHA FAZ E O QUE ELA NÃO FAZ", T(12, True, MUSGO)),
        ("Faz: calcula o custo da noite em cada canal, o piso, as diárias das cinco faixas, a média de cada mês e do ano (ponderada pelas noites de meio de semana, de fim de semana e de pico) e o líquido por canal.", None),
        ("Não faz: não prevê ocupação nem receita, não conhece os preços da sua região e não substitui o levantamento dos concorrentes. Os fatores das faixas são o ponto de partida da fonte Zion: o levantamento do seu destino é que decide os seus. A diária média do calendário é a média das diárias-alvo, não uma previsão.", None),
        ("Convenções: fim de semana são as noites de sexta e de sábado. As noites das datas de pico saem primeiro do meio de semana do mês. Percentuais são digitados como número (16 = 16%).", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Material educativo: não é promessa de renda, retorno, ocupação ou resultado. A gestão depende da execução de cada hospedagem.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Custo e Referência ----------
    cr = wb.create_sheet("Custo e Referência"); cr.sheet_view.showGridLines = False
    for col, w in zip("ABC", (50, 18, 66)): cr.column_dimensions[col].width = w
    cr["A1"] = "Custo e diária de referência"; cr["A1"].font = T(18, True, MUSGO)
    cr["A2"] = "EXEMPLO DIDÁTICO · dados fictícios (Cabanas do Vale)" if exemplo else "Preencha as células amarelas."; cr["A2"].font = T(10, True, "A0522D" if exemplo else DOURADO)
    faixa(cr, 4, "1 · O CUSTO DA NOITE (da sua Folha Única do Mês, Módulo 2)")
    rotulo(cr, 5, "Custo variável por noite (R$)", "Limpeza por estadia, enxoval, amenidades, energia da unidade, quebra."); entrada(cr, 5, e.get("cv"))
    rotulo(cr, 6, "Custo por noite vendida (R$)", "Variável por noite + custo fixo ÷ noites vendidas. Para a tabela do ano, o ideal é a média do ano."); entrada(cr, 6, e.get("cpn"))
    rotulo(cr, 7, "Noites por estadia (média)", "Noites vendidas ÷ estadias. Divide os custos por reserva."); entrada(cr, 7, e.get("ne"), "0.00")
    rotulo(cr, 8, "Imposto sobre a receita (%)", "Sai de toda reserva, em qualquer canal."); entrada(cr, 8, e.get("imposto"), "0.0")
    rotulo(cr, 9, "Receita de hospedagem de um mês comum (R$) · opcional", "Só para mostrar o que a meta de venda direta muda na comissão."); entrada(cr, 9, e.get("receita"))
    rotulo(cr, 10, "Diária média que você pratica hoje (R$) · opcional", "Para comparar com a diária média do calendário."); entrada(cr, 10, e.get("atual"))
    faixa(cr, 12, "2 · O PREÇO DE SEIS A NOVE CONCORRENTES DIRETOS (fim de semana comum, preço final com taxas)")
    for i in range(9):
        rotulo(cr, 13 + i, f"Concorrente {i + 1} (R$)", "Mesmo porte, mesmo público, mesma região." if i == 0 else ""); entrada(cr, 13 + i, (e.get("conc") or [])[i] if exemplo and i < len(e["conc"]) else None)
    rotulo(cr, 22, "Concorrentes informados"); calc(cr, 22, "=COUNT(B13:B21)", "0")
    rotulo(cr, 23, "Média sem o mais caro e o mais barato (R$)", "Precisa de pelo menos 3; a fonte pede de 6 a 9."); calc(cr, 23, '=IF(B22>=3,(SUM(B13:B21)-MAX(B13:B21)-MIN(B13:B21))/(B22-2),"")')
    rotulo(cr, 24, "Posição que você escolheu", "Terço de baixo (cerca de 15% abaixo), Meio ou Terço de cima (cerca de 20% acima)."); entrada(cr, 24, e.get("terco"), "@")
    rotulo(cr, 25, "Diária na posição escolhida (R$)"); calc(cr, 25, '=IF(OR(B23="",B24=""),"",B23*IF(B24="Terço de baixo",0.85,IF(B24="Terço de cima",1.2,1)))')
    rotulo(cr, 26, "A MINHA DIÁRIA DE REFERÊNCIA (R$)", "O preço cheio, sem desconto e sem condição. Use a sugerida ou ajuste."); entrada(cr, 26, e.get("ref"))
    rotulo(cr, 28, "Situação dos dados")
    s = cr.cell(28, 2, '=IF(COUNTBLANK(B5:B8)+COUNTBLANK(B26)>0,"Preencha o custo, as noites por estadia, o imposto e a referência",IF(MIN(B5:B10,B13:B21,B26)<0,"Há valor negativo",IF(B6<B5,"O custo por noite vendida não pode ser menor que o variável",IF(B8>=100,"Imposto precisa ficar abaixo de 100%","OK"))))')
    s.font = T(11, True); s.border = borda; s.fill = CALC; s.alignment = Alignment(wrap_text=True); alerta(cr, "B28")
    nota(cr, 30, "Fonte: Jornada do COMO · Etapa 08 · Passo 03 (diária de referência) e Etapa 09 · Passo 08 (custo por noite vendida).")
    dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, errorTitle="Valor inválido", error="Use um número maior ou igual a zero."); cr.add_data_validation(dv); dv.add("B5:B10"); dv.add("B13:B21"); dv.add("B26")
    dvt = DataValidation(type="list", formula1='"Terço de baixo,Meio,Terço de cima"', allow_blank=True); cr.add_data_validation(dvt); dvt.add("B24")

    # ---------- Mapa de Canais ----------
    mc = wb.create_sheet("Mapa de Canais"); mc.sheet_view.showGridLines = False
    mc["A1"] = "Mapa de Canais · mix dos últimos três meses e o que cada canal deixa por noite"; mc["A1"].font = T(14, True, MUSGO)
    mc["A2"] = "EXEMPLO DIDÁTICO · dados fictícios (Cabanas do Vale)" if exemplo else "Uma linha por canal (amarelo). Na diária de referência da aba Custo e Referência."; mc["A2"].font = T(10, True, "A0522D" if exemplo else DOURADO)
    cab(mc, 4, ["Canal", "% da receita", "Comissão (%)", "Taxa de pagamento (%)", "Outro custo por reserva (R$)", "Venda direta? (Sim/Não)", "Deduções (%)", "Líquido por noite (R$)", "Depois do custo variável (R$)", "Custo da noite neste canal (R$)", "Limite do variável (R$)"],
        [30, 11, 11, 12, 14, 12, 11, 14, 15, 15, 13], 46)
    for i, l in enumerate(range(L1, L2 + 1)):
        dados = e["canais"][i] if exemplo and i < len(e["canais"]) else (None,) * 6
        for col, v in enumerate(dados, 1):
            entrada(mc, l, v, {1: "@", 2: "0.0", 3: "0.0", 4: "0.0", 5: BRL, 6: "@"}[col], col)
        calc(mc, l, f'=IF(A{l}="","",C{l}+D{l}+{IMP})', "0.0", False, 7)
        calc(mc, l, f'=IF(OR(A{l}="",{REF}=""),"",{REF}*(1-G{l}/100)-E{l}/{NE})', BRL, False, 8)
        calc(mc, l, f'=IF(H{l}="","",H{l}-{CV})', BRL, False, 9)
        calc(mc, l, f'=IF(OR(A{l}="",B{l}<=0,G{l}>=100),"",({CPN}+E{l}/{NE})/(1-G{l}/100))', BRL, False, 10)
        calc(mc, l, f'=IF(J{l}="","",({CV}+E{l}/{NE})/(1-G{l}/100))', BRL, False, 11)
    R = f"B{L1}:B{L2}"; C = f"C{L1}:C{L2}"; F = f"F{L1}:F{L2}"
    faixa(mc, 11, "RESUMO DO MIX E META DE VENDA DIRETA", 5)
    rotulo(mc, 12, "Soma do mix (%)", "Precisa dar 100.", 3); calc(mc, 12, f"=SUM({R})", "0.0")
    rotulo(mc, 13, "Comissão média ponderada (%)"); calc(mc, 13, f"=SUMPRODUCT({R},{C})/100", "0.00")
    rotulo(mc, 14, "Venda direta hoje (% da receita)"); calc(mc, 14, f'=SUMIF({F},"Sim",{R})', "0.0")
    rotulo(mc, 15, "Comissão média dos canais pagos (%)"); calc(mc, 15, f'=IF(SUMIF({F},"<>Sim",{R})>0,SUMPRODUCT(({F}<>"Sim")*{R}*{C})/SUMIF({F},"<>Sim",{R}),0)', "0.00")
    rotulo(mc, 16, "Canais pagos com venda"); calc(mc, 16, f'=SUMPRODUCT(({F}<>"Sim")*({R}>0)*(A{L1}:A{L2}<>""))', "0")
    rotulo(mc, 17, "Meta de venda direta (% da receita)", "Um número acima do atual."); entrada(mc, 17, e.get("meta"), "0.0")
    rotulo(mc, 18, "Até quando", "Data."); entrada(mc, 18, e.get("prazo"), "@")
    rotulo(mc, 19, "Comissão que deixaria de sair num mês (R$)", "Com a mesma receita do mês comum. Conta com os seus números, não previsão."); calc(mc, 19, f'=IF(OR({CR}B9="",B17<=B14),"",{CR}B9*(B17-B14)/100*B15/100)')
    rotulo(mc, 20, "Tenho gestor de canais ligando os calendários? (Sim/Não)"); entrada(mc, 20, e.get("gestor"), "@")
    rotulo(mc, 21, "Tenho motor de reservas no site? (Sim/Não)"); entrada(mc, 21, e.get("motor"), "@")
    rotulo(mc, 22, "Canal que mais deixa por noite"); calc(mc, 22, f'=IF(COUNT(I{L1}:I{L2})=0,"",INDEX(A{L1}:A{L2},MATCH(MAX(I{L1}:I{L2}),I{L1}:I{L2},0)))', "@")
    rotulo(mc, 23, "Canal que menos deixa por noite"); calc(mc, 23, f'=IF(COUNT(I{L1}:I{L2})=0,"",INDEX(A{L1}:A{L2},MATCH(MIN(I{L1}:I{L2}),I{L1}:I{L2},0)))', "@")
    rotulo(mc, 24, "Situação dos dados")
    s = mc.cell(24, 2, f'=IF(COUNTA(A{L1}:A{L2})=0,"Informe pelo menos um canal",IF(MIN(B{L1}:E{L2})<0,"Há valor negativo",IF(ABS(B12-100)>0.05,"O mix precisa somar 100%",IF(MAX(G{L1}:G{L2})>=100,"Deduções de 100% ou mais",IF(COUNTIF({F},"Sim")=0,"Inclua a linha de venda direta (mesmo com 0%)","OK")))))')
    s.font = T(11, True); s.border = borda; s.fill = CALC; s.alignment = Alignment(wrap_text=True); alerta(mc, "B24")
    nota(mc, 26, "Fonte: Panorama · Trilha B · Pilar G2 (mix atual, líquido por canal, meta de venda direta, básico técnico) e Etapa 09 · Passo 10 (margem por canal).")
    dvn = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, errorTitle="Valor inválido", error="Use um número maior ou igual a zero."); mc.add_data_validation(dvn); dvn.add(f"B{L1}:E{L2}"); dvn.add("B17")
    dvs = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); mc.add_data_validation(dvs); dvs.add(f"F{L1}:F{L2}"); dvs.add("B20:B21")

    # ---------- Piso ----------
    pi = wb.create_sheet("Piso"); pi.sheet_view.showGridLines = False
    for col, w in zip("ABC", (52, 22, 62)): pi.column_dimensions[col].width = w
    pi["A1"] = "O piso, por escrito"; pi["A1"].font = T(18, True, MUSGO)
    pi["A2"] = "EXEMPLO DIDÁTICO · dados fictícios (Cabanas do Vale)" if exemplo else "Preencha as células amarelas. Piso decidido em mês fraco é piso que não existe."; pi["A2"].font = T(10, True, "A0522D" if exemplo else DOURADO)
    faixa(pi, 4, "O PISO")
    rotulo(pi, 5, "Custo da noite no canal mais caro (R$)", "Custo por noite vendida, mais o custo por reserva, dividido pelo que sobra depois das deduções do canal."); calc(pi, 5, f'=IF(COUNT({MC}J{L1}:J{L2})=0,"",MAX({MC}J{L1}:J{L2}))')
    rotulo(pi, 6, "Margem mínima que justifica abrir a porta (%)", "Decisão sua. A fonte: o piso é o custo mais a margem mínima."); entrada(pi, 6, e.get("margem"), "0.0")
    rotulo(pi, 7, "Piso calculado (R$)"); calc(pi, 7, '=IF(OR(B5="",B6=""),"",B5*(1+B6/100))')
    rotulo(pi, 8, "O MEU PISO, POR ESCRITO (R$)", "O menor valor pelo qual você vende, em qualquer situação, inclusive na véspera."); entrada(pi, 8, e.get("piso"))
    rotulo(pi, 9, "Piso em relação à referência"); calc(pi, 9, f'=IF(OR(B8="",{REF}="",{REF}=0),"",B8/{REF})', "0.0%")
    rotulo(pi, 10, "Quem já sabe do piso", "Piso que só existe na sua cabeça não é piso."); entrada(pi, 10, e.get("quem"), "@")
    faixa(pi, 12, "TRÊS CONDIÇÕES NO LUGAR DE DESCONTO (ceda em data, noite extra ou serviço)")
    for i in range(3): rotulo(pi, 13 + i, f"Condição {i + 1}"); entrada(pi, 13 + i, (e.get("cond") or [None] * 3)[i] if exemplo else None, "@")
    faixa(pi, 17, "A REGRA DO DESCONTO EM TRÊS FAIXAS (no canal mais caro)")
    rotulo(pi, 18, "Acima deste valor, a noite paga tudo (R$)"); calc(pi, 18, "=B5")
    rotulo(pi, 19, "Abaixo deste, a noite consome valor (R$)", "Entre os dois, a noite só paga o variável e ajuda no fixo."); calc(pi, 19, f'=IF(B5="","",INDEX({MC}K{L1}:K{L2},MATCH(B5,{MC}J{L1}:J{L2},0)))')
    rotulo(pi, 20, "Leitura do piso")
    calc(pi, 20, '=IF(OR(B8="",B5=""),"",IF(B8<B5-0.005,"Piso abaixo do custo da noite: vendida no piso, a noite não paga tudo",IF(AND(B7<>"",B8<B7-0.005),"Piso cobre o custo, mas fica abaixo do piso com a sua margem mínima","Piso cobre o custo com a sua margem mínima")))', "@")
    rotulo(pi, 21, "Situação dos dados")
    s = pi.cell(21, 2, f'=IF({CR}B28<>"OK","Confira a aba Custo e Referência",IF({MC}B24<>"OK","Confira a aba Mapa de Canais",IF(B8="","Escreva o seu piso",IF(B8<0,"Há valor negativo",IF(B8>{REF},"O piso não pode passar da referência","OK")))))')
    s.font = T(11, True); s.border = borda; s.fill = CALC; s.alignment = Alignment(wrap_text=True); alerta(pi, "B21")
    nota(pi, 23, "Desconto, só em quatro situações e nunca abaixo do piso nem nas datas de pico: estadia longa (10 a 20% a partir da quinta noite), grande antecedência (8 a 15%), base própria ou recorrente (10 a 15%) e último minuto dentro da janela curta. Fonte: Etapa 08 · Passo 10; Panorama · G3.")
    dvp = DataValidation(type="decimal", operator="between", formula1="0", formula2="99.9", showErrorMessage=True, errorTitle="Valor inválido", error="Use um percentual de 0 a 99,9."); pi.add_data_validation(dvp); dvp.add("B6")

    # ---------- Calendário 12 meses ----------
    ca = wb.create_sheet("Calendário 12 meses"); ca.sheet_view.showGridLines = False
    ca["A1"] = "Calendário de 12 meses · cinco faixas sobre a diária de referência"; ca["A1"].font = T(14, True, MUSGO)
    ca["A2"] = "EXEMPLO DIDÁTICO · dados fictícios (Cabanas do Vale)" if exemplo else "Fatores: ponto de partida da fonte, ajuste pelo levantamento do seu destino. Escolha a faixa de cada mês (amarelo)."; ca["A2"].font = T(10, True, "A0522D" if exemplo else DOURADO)
    cab(ca, 3, ["Faixa", "Fator", "Diária (R$)", "Ponto de partida da fonte"], None, 22)
    fat = [("Vale", 0.75, "0,70 a 0,80"), ("Baixa", 0.90, "0,85 a 0,95"), ("Base", 1, "sempre 1,00"), ("Alta", 1.50, "1,35 a 1,60"), ("Pico", 2.20, "1,90 a 2,60 (genérico; as datas de pico têm fator próprio)")]
    for i, (nome, padrao, faixa_txt) in enumerate(fat):
        l = 4 + i; ca.cell(l, 1, nome).font = T(11, True)
        if nome == "Base": calc(ca, l, 1, "0.00")
        else: entrada(ca, l, (e["fatores"][nome] if exemplo else padrao), "0.00")
        calc(ca, l, f'=IF({REF}="","",{REF}*B{l})', BRL, False, 3)
        x = ca.cell(l, 4, faixa_txt); x.font = T(9, c="5F5F55", i=True)
    ca.cell(10, 1, "Ano em que o calendário começa").font = T(11); entrada(ca, 10, e.get("ano"), "0")
    ca.cell(11, 1, "Primeiro mês (1 a 12)").font = T(11); entrada(ca, 11, e.get("inicio") if exemplo else 1, "0")
    cab(ca, 13, ["Mês", "Começa em", "Noites", "Sexta e sábado", "Meio de semana", "Noites de pico", "Faixa meio de semana", "Faixa fim de semana", "Semana sem pico", "Fim de semana sem pico", "Diária semana (R$)", "Diária fim de semana (R$)", "Receita das datas de pico (R$)", "Média do mês (R$)", "Soma das diárias do mês (R$)"],
        [12, 12, 8, 9, 9, 9, 13, 13, 9, 10, 12, 12, 13, 13, 14], 46)
    FT = "$A$4:$B$8"
    for i, l in enumerate(range(M1, M2 + 1)):
        calc(ca, l, f'=IF(B{l}="","",CHOOSE(MONTH(B{l}),"jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez")&"/"&YEAR(B{l}))', "@", False, 1)
        calc(ca, l, f'=IF(OR($B$10="",$B$11=""),"",DATE($B$10,$B$11+{i},1))', "dd/mm/yyyy", False, 2)
        calc(ca, l, f'=IF(B{l}="","",DAY(DATE(YEAR(B{l}),MONTH(B{l})+1,0)))', "0", False, 3)
        e_ = f"DATE(YEAR(B{l}),MONTH(B{l})+1,0)"
        calc(ca, l, f'=IF(B{l}="","",INT((WEEKDAY(B{l}-6)+{e_}-B{l})/7)+INT((WEEKDAY(B{l}-7)+{e_}-B{l})/7))', "0", False, 4)
        calc(ca, l, f'=IF(B{l}="","",C{l}-D{l})', "0", False, 5)
        calc(ca, l, f'=IF(B{l}="","",MIN(C{l},SUMIF({DP}$B${P1}:$B${P2},MONTH(B{l}),{DP}$C${P1}:$C${P2})))', "0", False, 6)
        mv = e["meses"][i] if exemplo else (None, None)
        entrada(ca, l, mv[0], "@", 7); entrada(ca, l, mv[1], "@", 8)
        calc(ca, l, f'=IF(B{l}="","",MAX(0,E{l}-F{l}))', "0", False, 9)
        calc(ca, l, f'=IF(B{l}="","",MAX(0,D{l}-MAX(0,F{l}-E{l})))', "0", False, 10)
        calc(ca, l, f'=IF(OR(G{l}="",{REF}=""),"",{REF}*VLOOKUP(G{l},{FT},2,0))', BRL, False, 11)
        calc(ca, l, f'=IF(OR(H{l}="",{REF}=""),"",{REF}*VLOOKUP(H{l},{FT},2,0))', BRL, False, 12)
        calc(ca, l, f'=IF(B{l}="","",SUMIF({DP}$B${P1}:$B${P2},MONTH(B{l}),{DP}$H${P1}:$H${P2}))', BRL, False, 13)
        calc(ca, l, f'=IF(OR(K{l}="",L{l}=""),"",I{l}*K{l}+J{l}*L{l}+M{l})', BRL, False, 15)
        calc(ca, l, f'=IF(O{l}="","",O{l}/C{l})', BRL, False, 14)
    G = f"G{M1}:G{M2}"; H = f"H{M1}:H{M2}"; I = f"I{M1}:I{M2}"; J = f"J{M1}:J{M2}"
    faixa(ca, 27, "RESUMO DO CALENDÁRIO", 4)
    for k, nome in enumerate(["Vale", "Baixa", "Base", "Alta"]):
        ca.cell(28 + k, 1, f"Noites na faixa {nome.lower()}").font = T(11); calc(ca, 28 + k, f'=SUMIF({G},"{nome}",{I})+SUMIF({H},"{nome}",{J})', "0")
    ca.cell(32, 1, "Noites de pico").font = T(11); calc(ca, 32, f"=SUM(F{M1}:F{M2})", "0")
    ca.cell(33, 1, "Total de noites").font = T(11); calc(ca, 33, f"=SUM(C{M1}:C{M2})", "0")
    ca.cell(34, 1, "DIÁRIA MÉDIA DO CALENDÁRIO (R$)").font = T(11, True); calc(ca, 34, f'=IF(COUNT(O{M1}:O{M2})<12,"",SUM(O{M1}:O{M2})/SUM(C{M1}:C{M2}))', BRL, True)
    ca.cell(35, 1, "Faixas e datas abaixo do piso").font = T(11)
    usado = lambda nome, l: f'IF(AND(COUNTIF({G},"{nome}")+COUNTIF({H},"{nome}")>0,C{l}<{PI}$B$8-0.005),"{nome} ","")'
    calc(ca, 35, '=IF(' + PI + '$B$8="","",IF(' + "&".join(usado(n, 4 + k) for k, n in enumerate(["Vale", "Baixa", "Base", "Alta"])) + f'&IF(COUNTIF({DP}I{P1}:I{P2},"abaixo do piso")>0,"Datas de pico","")="","Nenhuma",TRIM(' + "&".join(usado(n, 4 + k) for k, n in enumerate(["Vale", "Baixa", "Base", "Alta"])) + f'&IF(COUNTIF({DP}I{P1}:I{P2},"abaixo do piso")>0,"Datas de pico",""))))', "@")
    ca.cell(36, 1, "Situação dos dados").font = T(11)
    s = ca.cell(36, 2, f'=IF(OR($B$10="",$B$11=""),"Preencha o ano e o primeiro mês",IF(OR($B$10<2024,$B$10>2099,$B$11<1,$B$11>12),"Ano de 2024 a 2099 e mês de 1 a 12",IF(COUNTBLANK({G})+COUNTBLANK({H})>0,"Escolha a faixa de meio de semana e de fim de semana dos 12 meses",IF(MIN(B4,B5,B7,B8)<=0,"Fatores precisam ser maiores que zero","OK"))))')
    s.font = T(11, True); s.border = borda; s.fill = CALC; s.alignment = Alignment(wrap_text=True); alerta(ca, "B36")
    nota(ca, 38, "Fim de semana = noites de sexta e de sábado. As noites das datas de pico saem primeiro do meio de semana. A média do mês pondera as três partes. A diária média do calendário é a média das diárias-alvo, não previsão de receita. Fonte: Etapa 08 · Passos 05 e 07.")
    dvf = DataValidation(type="list", formula1='"Vale,Baixa,Base,Alta"', allow_blank=True); ca.add_data_validation(dvf); dvf.add(f"G{M1}:H{M2}")
    dvx = DataValidation(type="decimal", operator="between", formula1="0.01", formula2="5", showErrorMessage=True, errorTitle="Valor inválido", error="Fator de 0,01 a 5."); ca.add_data_validation(dvx); dvx.add("B4:B5"); dvx.add("B7:B8")

    # ---------- Datas de pico ----------
    dp = wb.create_sheet("Datas de pico"); dp.sheet_view.showGridLines = False
    dp["A1"] = "Datas de pico · preço próprio, mínimo de noites e quando abrir"; dp["A1"].font = T(14, True, MUSGO)
    dp["A2"] = "EXEMPLO DIDÁTICO · dados fictícios (Cabanas do Vale)" if exemplo else "Réveillon, carnaval, feriados prolongados, semanas de pico da temporada e eventos locais. Bloqueie as datas até terem preço."; dp["A2"].font = T(10, True, "A0522D" if exemplo else DOURADO)
    cab(dp, 4, ["Data", "Mês (1 a 12)", "Noites", "Fator", "Mínimo de noites", "Quando abrir", "Diária (R$)", "Receita das noites (R$)", "Conferência"], [34, 10, 8, 8, 10, 22, 13, 14, 26], 34)
    for i, l in enumerate(range(P1, P2 + 1)):
        dados = e["picos"][i] if exemplo and i < len(e["picos"]) else (None,) * 6
        for col, v in enumerate(dados, 1): entrada(dp, l, v, {1: "@", 2: "0", 3: "0", 4: "0.00", 5: "0", 6: "@"}[col], col)
        calc(dp, l, f'=IF(OR(A{l}="",D{l}="",{REF}=""),"",{REF}*D{l})', BRL, False, 7)
        calc(dp, l, f'=IF(G{l}="","",C{l}*G{l})', BRL, False, 8)
        calc(dp, l, f'=IF(A{l}="","",IF(OR(B{l}<1,B{l}>12,C{l}<1),"confira mês e noites",IF(AND({PI}$B$8<>"",G{l}<{PI}$B$8-0.005),"abaixo do piso",IF(E{l}<2,"sem mínimo de noites","ok"))))', "@", False, 9)
    nota(dp, 14, "Pontos de partida da fonte (Etapa 08 · Passo 06): réveillon fator 2,2 a 3,0, mínimo 5 a 7, abrir 4 a 6 meses antes; carnaval 1,9 a 2,5, mínimo 4 a 5, 3 a 5 meses antes; feriado prolongado 1,7 a 2,2, mínimo 3 a 4, 2 a 4 meses antes; pico de temporada 1,6 a 2,0, mínimo 3 a 5; evento local: levantar, mínimo 2 a 3, abrir assim que a data sair.")
    dvm = DataValidation(type="whole", operator="between", formula1="1", formula2="12", showErrorMessage=True, errorTitle="Valor inválido", error="Mês de 1 a 12."); dp.add_data_validation(dvm); dvm.add(f"B{P1}:B{P2}")
    dvq = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, errorTitle="Valor inválido", error="Use um número maior ou igual a zero."); dp.add_data_validation(dvq); dvq.add(f"C{P1}:E{P2}")

    # ---------- Resumo ----------
    rs = wb.create_sheet("Resumo"); rs.sheet_view.showGridLines = False
    for col, w in zip("ABC", (52, 26, 50)): rs.column_dimensions[col].width = w
    rs["A1"] = "Resumo da Tabela de Preço e Canais" + ("  ·  EXEMPLO FICTÍCIO" if exemplo else ""); rs["A1"].font = T(16, True, MUSGO)
    itens = [("O meu piso, por escrito", f"={PI}B8", BRL), ("Diária de referência", f"={REF}", BRL), ("Custo da noite no canal mais caro", f"={PI}B5", BRL),
             ("Piso calculado com a margem mínima", f"={PI}B7", BRL), ("Diária média do calendário", f"={CA}B34", BRL), ("Comissão média ponderada (%)", f"={MC}B13", "0.00"),
             ("Venda direta hoje (%)", f"={MC}B14", "0.0"), ("Meta de venda direta (%)", f"={MC}B17", "0.0"), ("Canal que mais deixa por noite", f"={MC}B22", "@"),
             ("Faixas e datas abaixo do piso", f"={CA}B35", "@")]
    for k, (t, fml, fmt) in enumerate(itens): rotulo(rs, 3 + k, t); calc(rs, 3 + k, fml, fmt)
    rotulo(rs, 14, "Preço fixo o ano inteiro?"); calc(rs, 14, f'=IF(AND(COUNTIF({CA}G{M1}:H{M2},{CA}G{M1})=24,COUNTA({DP}A{P1}:A{P2})=0),"Sim","Não")', "@")
    rotulo(rs, 15, "CAUSA PRINCIPAL", "Ordem: custo → piso → calendário → canais → piso conhecido.")
    causa = ('=IF(OR({cr}B28<>"OK",{mc}B24<>"OK",{pi}B21<>"OK",{ca}B36<>"OK"),"Confira a situação dos dados nas abas",'
             'IF({ref}<{pi}B5-0.005,"Referência abaixo do custo da noite",'
             'IF({pi}B8<{pi}B5-0.005,"Piso abaixo do custo da noite",'
             'IF({ca}B35<>"Nenhuma","Faixa do calendário abaixo do piso",'
             'IF(B14="Sim","Preço fixo o ano inteiro",'
             'IF(OR(COUNTA({dp}A{p1}:A{p2})=0,COUNTIF({dp}I{p1}:I{p2},"sem mínimo de noites")>0),"Datas de pico sem regra",'
             'IF({mc}B14=0,"Sem venda direta",'
             'IF(AND({mc}B16>=2,{mc}B20<>"Sim"),"Vários canais sem gestor de canais",'
             'IF(AND({mc}B14>0,{mc}B21<>"Sim"),"Venda direta sem motor de reservas",'
             'IF({pi}B10="","Piso só na sua cabeça","Tabela dentro das regras da fonte"))))))))))').format(cr=CR, mc=MC, pi=PI, ca=CA, dp=DP, ref=REF, p1=P1, p2=P2)
    calc(rs, 15, causa, "@", True)
    nota(rs, 17, "A Tabela é a página 3 do seu Plano de Gestão. Revise a cada trimestre, de três a quatro semanas antes do trimestre que a revisão decide, e mantenha doze meses de calendário abertos nos canais.")

    # ---------- Checklist da revisão ----------
    ck = wb.create_sheet("Checklist da revisão"); ck.sheet_view.showGridLines = False
    for col, w in zip("ABC", (6, 84, 12)): ck.column_dimensions[col].width = w
    ck["A1"] = "Checklist da revisão trimestral do preço e dos canais · marque Sim ou Não (amarelo)"; ck["A1"].font = T(14, True, MUSGO)
    itens = ["O custo por noite vendida foi atualizado com a Folha Única do Mês",
             "O piso ainda cobre o custo da noite no canal mais caro, com a margem mínima",
             "Quem atende sabe o piso sem consultar ninguém",
             "O levantamento dos concorrentes foi refeito para o trimestre seguinte",
             "As faixas do trimestre seguinte foram ajustadas (no máximo 8 a 12% por vez)",
             "As datas de pico que entram na janela têm preço, mínimo de noites e data de abertura",
             "Há doze meses de calendário abertos nos canais, com o preço final conferido",
             "O mix de canais do trimestre foi conferido no extrato de cada canal",
             "A meta de venda direta foi comparada com o realizado",
             "O que mudou e por quê está registrado em duas linhas"]
    cab(ck, 3, ["Nº", "Item", "Feito?"], None, 20)
    for i, t in enumerate(itens):
        ck.cell(4 + i, 1, i + 1).font = T(10, True); ck.cell(4 + i, 2, t).alignment = Alignment(wrap_text=True)
        x = ck.cell(4 + i, 3, ("Sim" if i < 6 else "Não") if exemplo else None); x.fill = ENTRADA; x.border = borda
    dvk = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); ck.add_data_validation(dvk); dvk.add(f"C4:C{3 + len(itens)}")
    ck.cell(15, 2, "Itens feitos:"); x = ck.cell(15, 3, f'=COUNTIF(C4:C{3 + len(itens)},"Sim")'); x.fill = CALC; x.border = borda; x.font = T(12, True, MUSGO)
    ck.cell(16, 2, f'=IF(C15={len(itens)},"Revisão completa: 10 de 10","Faltam "&({len(itens)}-C15)&" de {len(itens)} itens")').font = T(10, True, MUSGO)
    ck.cell(18, 2, "Rotina da fonte: painel todo mês (10 min), revisão a cada trimestre (2 h), levantamento completo uma vez por ano (4 h).").font = T(9, c="5F5F55", i=True)
    wb.active = 0
    return wb

for exemplo, nome in ((False, "Tabela-de-Preco-e-Canais-Zion-EM-BRANCO.xlsx"), (True, "Tabela-de-Preco-e-Canais-Zion-EXEMPLO.xlsx")):
    montar(exemplo).save(OUT / nome); print("ok", OUT / nome)

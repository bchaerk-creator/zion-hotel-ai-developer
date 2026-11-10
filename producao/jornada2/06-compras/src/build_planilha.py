"""Gera a planilha "Matriz de Compras e Manutenção" (Jornada 2 · Gestão · Módulo 6 · Compras, estoque e manutenção) em duas versões:
   - Matriz-de-Compras-e-Manutencao-Zion-EM-BRANCO.xlsx
   - Matriz-de-Compras-e-Manutencao-Zion-EXEMPLO.xlsx (dados fictícios, identificados como exemplo)
Uso: python3 -I build_planilha.py <pasta-saida>
Molde: producao/jornada2/03-preco/src/build_planilha.py (amarelo = preenche, verde = calculado).
Abas: Comece aqui · Matriz de Compras · Estoque · Manutenção 12 meses · Rotina e checklist · Resumo."""
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
    c = ws.cell(l, col, valor); c.fill = ENTRADA; c.border = borda; c.number_format = fmt; c.font = T(11, True); return c
def calc(ws, l, formula, fmt=BRL, destaque=False, col=2):
    c = ws.cell(l, col, formula); c.fill = CALC; c.border = borda; c.number_format = fmt; c.font = T(13 if destaque else 10, True, MUSGO if destaque else PRETO); c.alignment = Alignment(wrap_text=True, vertical="center"); return c
def cab(ws, linha, titulos, larguras=None, altura=34):
    for i, t in enumerate(titulos, 1):
        x = ws.cell(linha, i, t); x.font = T(10, True, CREME); x.fill = CAB; x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); x.border = borda
        if larguras: ws.column_dimensions[x.column_letter].width = larguras[i - 1]
    ws.row_dimensions[linha].height = altura
def alerta(ws, ref):
    ws.conditional_formatting.add(ref, FormulaRule(formula=[f'${ref[0]}${ref[1:]}<>"OK"'], fill=ALERTA, font=Font(color="9B2C1F", bold=True)))
def nota(ws, l, texto, col=1):
    c = ws.cell(l, col, texto); c.font = T(9, c="5F5F55", i=True); c.alignment = Alignment(wrap_text=False)
def situacao(ws, l, formula, col=2):
    s = ws.cell(l, col, formula); s.font = T(11, True); s.border = borda; s.fill = CALC; s.alignment = Alignment(wrap_text=True); alerta(ws, f"{s.column_letter}{l}")

# Exemplo didático · dados fictícios (Cabanas do Vale). Mesmos valores da ficha (src/logic.js) e do PLANO seção 9.
TIPO = {"variavel": "Variável", "outras": "Vendido à parte"}; CONTR = {"sim": "Tem contrato", "fechar": "Vou fechar", "nao": "Sem contrato"}
FREQ = {"mensal": "Mensal", "bimestral": "Bimestral", "trimestral": "Trimestral", "semestral": "Semestral", "anual": "Anual"}
EX = dict(meses=3, noites=174, hospedes=150, unidades=4, cv=28.32, prazo="31/03/2027",
          itens=[("Café da manhã e cestas (insumos)", "cesta montada", 1260, "Vendido à parte", 28, 28, 25.5, 26.9, "Vou fechar"),
                 ("Lavanderia do enxoval", "kg lavado", 900, "Variável", 3, 3, 2.6, 3.2, "Tem contrato"),
                 ("Amenidades (sabonete, xampu, papel, água)", "kit por estadia", 780, "Variável", 10.4, 10.4, 8.9, 9.8, "Vou fechar"),
                 ("Gás do aquecimento da água", "botijão de 13 kg", 720, "Variável", 120, 120, 112, 118, "Sem contrato"),
                 ("Reposição de enxoval", "jogo de cama de casal", 240, "Variável", 120, 120, 98, 135, "Vou fechar")],
          estoque=[("Kit de amenidades", "kit", 25, 7, 7, 14, 30), ("Papel higiênico", "rolo", 100, 5, 7, 30, 30),
                   ("Botijão de gás de 13 kg", "botijão", 2, 2, 7, 2, 15), ("Café em pó (pacote de 500 g)", "pacote", 8, 3, 7, 6, 15)],
          camas=4, jogos=10, ano=2027, inicio=1, receita=13565.6, reserva=3, cheia=[6, 7, 8, 12],
          tarefas=[("Limpar os filtros do ar-condicionado", "Trimestral", 1, 0, "Equipe"), ("Controle de pragas", "Trimestral", 2, 180, "Empresa contratada"),
                   ("Revisão do aquecedor a gás", "Anual", 3, 280, "Técnico de aquecimento"), ("Revisão elétrica (quadro e tomadas)", "Anual", 4, 350, "Eletricista"),
                   ("Limpeza das calhas", "Semestral", 4, 150, "Equipe"), ("Limpeza da caixa d'água", "Semestral", 5, 250, "Empresa contratada"),
                   ("Revisão do ar-condicionado por técnico", "Anual", 9, 480, "Técnico de ar-condicionado"), ("Inspeção e recarga dos extintores", "Anual", 10, 160, "Empresa credenciada"),
                   ("Tratamento do deck (óleo e vedação)", "Anual", 11, 900, "Marceneiro")],
          dia="segunda-feira", quem="Ana (dona)", alcada=300, ronda="Sim", ocorr="Sim")

MZ = "'Matriz de Compras'!"; ES = "Estoque!"; MN = "'Manutenção 12 meses'!"; RO = "'Rotina e checklist'!"
I1, I2 = 14, 21     # itens da Matriz
E1, E2 = 5, 14      # itens do estoque
T1, T2 = 13, 27     # tarefas
C1, C2 = 32, 43     # meses do calendário

def montar(exemplo):
    e = EX if exemplo else {}
    rot2 = ("EXEMPLO DIDÁTICO · dados fictícios (Cabanas do Vale)", T(10, True, "A0522D"))
    wb = Workbook()
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False; ws.column_dimensions["A"].width = 100
    linhas = [
        ("ZION HOSPITALITY BUSINESS · JORNADA 2 · GESTÃO · MÓDULO 6 · COMPRAS, ESTOQUE E MANUTENÇÃO", T(10, True, DOURADO)),
        ("Matriz de Compras e Manutenção", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para listar o que você mais compra, comparar três cotações, saber o consumo por noite e por hóspede, definir o estoque mínimo e o ponto de pedido, e montar o calendário de manutenção preventiva de doze meses.", T(11, c="2D352A")),
        ("EXEMPLO DIDÁTICO PREENCHIDO COM DADOS FICTÍCIOS (Cabanas do Vale). Use a versão em branco para os seus números." if exemplo else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("", None),
        ("COMO USAR EM 5 PASSOS (cerca de 40 minutos na primeira vez, 15 minutos por semana depois)", T(12, True, MUSGO)),
        ("1. Aba Matriz de Compras: o período (de preferência três meses), as noites vendidas, os hóspedes e as unidades. Depois, os itens que mais pesam, por valor: gasto no período, tipo, unidade de compra, o preço de hoje, três cotações e a situação do contrato.", None),
        ("2. Aba Estoque: para cada item guardado, o uso por mês, o prazo de entrega, os dias de segurança, o estoque de hoje e de quanto em quanto tempo você compra. A planilha mostra o mínimo, o ponto de pedido e quanto pedir. No fim, as camas e os jogos de cama.", None),
        ("3. Aba Manutenção 12 meses: o ano, o primeiro mês, a receita real de um mês comum e a reserva de manutenção (de 3% a 6% pela fonte). As tarefas preventivas com frequência, primeiro mês, custo e quem faz. Marque os meses de casa cheia.", None),
        ("4. Aba Rotina e checklist: o dia da contagem semanal, quem compra, o limite de compra fora do previsto, a ronda diária e o registro de ocorrências. Marque o checklist mensal.", None),
        ("5. Aba Resumo: os números da página 6 do seu Plano de Gestão e a causa principal, na mesma ordem da ficha.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("AS CONTAS", T(12, True, MUSGO)),
        ("Consumo por noite = gasto do período ÷ noites vendidas no período (Etapa 09). Consumo por hóspede = gasto ÷ hóspedes. Quantidade = gasto ÷ preço de hoje. Diferença = quantidade × (preço de hoje − menor cotação), só quando a menor é mais barata.", None),
        ("Consumo por dia = uso do mês ÷ 30. Estoque mínimo = consumo por dia × dias de segurança. Ponto de pedido = consumo por dia × (entrega + segurança). Os dois arredondados para cima. Pedido = ponto de pedido + consumo do intervalo de compra − estoque de hoje. São definições-padrão de gestão de estoque, declaradas como tal: a fonte Zion manda acionar o fornecedor no mínimo e contar o estoque toda semana.", None),
        ("Uma tarefa cai num mês quando a distância entre o mês e o primeiro mês da tarefa é múltipla da frequência (mensal 1, bimestral 2, trimestral 3, semestral 6, anual 12). Reserva do mês = receita real × percentual. A reserva acumulada precisa cobrir o gasto acumulado em todos os meses.", None),
        ("", None),
        ("O QUE A PLANILHA NÃO FAZ", T(12, True, MUSGO)),
        ("Não prevê ocupação nem preço de mercado, não conhece os fornecedores da sua região e não substitui laudos, vistorias, manuais do fabricante nem profissionais habilitados (gás, elétrica, extintores, caixa d'água, controle de pragas). A diferença para a menor cotação é uma conta com os seus números, não uma previsão.", None),
        ("Ferramentas de apoio da Zion: 13 · Controle de Enxoval e Reposição, 14 · Quadro de Ocorrências e Manutenção, 18 · Planner de Manutenção Preventiva.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Material educativo: não é promessa de renda, retorno, ocupação ou resultado. A gestão depende da execução de cada hospedagem.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Matriz de Compras ----------
    mz = wb.create_sheet("Matriz de Compras"); mz.sheet_view.showGridLines = False
    mz["A1"] = "Matriz de Compras · o que se compra, de quem e sob que contrato"; mz["A1"].font = T(16, True, MUSGO)
    mz["A2"] = rot2[0] if exemplo else "Preencha as células amarelas. Liste por valor, não por frequência."; mz["A2"].font = rot2[1] if exemplo else T(10, True, DOURADO)
    faixa(mz, 4, "1 · O PERÍODO DO LEVANTAMENTO (a fonte pede três meses de notas)", 4)
    rotulo(mz, 5, "Meses do levantamento", "De 1 a 12. O ideal são três.", 4); entrada(mz, 5, e.get("meses"), "0")
    rotulo(mz, 6, "Noites vendidas no período", "Na Folha Única de cada mês (Módulo 2).", 4); entrada(mz, 6, e.get("noites"), "0")
    rotulo(mz, 7, "Hóspedes no período · opcional", "Soma das pessoas de cada reserva.", 4); entrada(mz, 7, e.get("hospedes"), "0")
    rotulo(mz, 8, "Unidades à venda", "Casas, cabanas ou quartos.", 4); entrada(mz, 8, e.get("unidades"), "0")
    rotulo(mz, 9, "Custo variável por noite da sua Folha (R$) · opcional", "Módulo 2. Para conferir quanto a Matriz explica.", 4); entrada(mz, 9, e.get("cv"))
    rotulo(mz, 10, "Até quando fechar os contratos marcados \"Vou fechar\"", "Data.", 4); entrada(mz, 10, e.get("prazo"), "@")
    cab(mz, 13, ["Item que você compra", "Unidade de compra", "Gasto no período (R$)", "Tipo", "Preço de hoje (R$)", "Cotação 1 (R$)", "Cotação 2 (R$)", "Cotação 3 (R$)", "Contrato",
                 "Cotações", "Menor cotação (R$)", "Quantidade no período", "Diferença para a menor (R$)", "Por noite vendida (R$)", "Por hóspede (R$)", "Peso no total", "Posição por valor"],
        [36, 16, 13, 15, 12, 11, 11, 11, 14, 9, 12, 11, 13, 12, 12, 9, 9], 46)
    for i, l in enumerate(range(I1, I2 + 1)):
        d = e["itens"][i] if exemplo and i < len(e["itens"]) else (None,) * 9
        for col, v in enumerate(d, 1): entrada(mz, l, v, {1: "@", 2: "@", 3: BRL, 4: "@", 5: BRL, 6: BRL, 7: BRL, 8: BRL, 9: "@"}[col], col)
        calc(mz, l, f'=IF(A{l}="","",COUNTIF(F{l}:H{l},">0"))', "0", False, 10)
        calc(mz, l, f'=IF(OR(A{l}="",J{l}=0),"",MIN(F{l}:H{l}))', BRL, False, 11)
        calc(mz, l, f'=IF(OR(A{l}="",N(E{l})<=0),"",C{l}/E{l})', "0.00", False, 12)
        calc(mz, l, f'=IF(OR(L{l}="",K{l}=""),"",MAX(0,L{l}*(E{l}-K{l})))', BRL, False, 13)
        calc(mz, l, f'=IF(OR(A{l}="",N($B$6)<=0),"",C{l}/$B$6)', BRL, False, 14)
        calc(mz, l, f'=IF(OR(A{l}="",N($B$7)<=0),"",C{l}/$B$7)', BRL, False, 15)
        calc(mz, l, f'=IF(OR(A{l}="",SUM($C${I1}:$C${I2})<=0),"",C{l}/SUM($C${I1}:$C${I2}))', "0.0%", False, 16)
        calc(mz, l, f'=IF(OR(A{l}="",N(C{l})<=0),"",RANK(C{l},$C${I1}:$C${I2}))', "0", False, 17)
    A, Cc, D, Ii, J, M = (f"{x}{I1}:{x}{I2}" for x in "ACDIJM")
    faixa(mz, 23, "RESUMO DA MATRIZ", 4)
    res = [
        (24, "Total do período (R$)", f"=SUM({Cc})", BRL),
        (25, "Itens variáveis no período (R$)", f'=SUMIF({D},"Variável",{Cc})', BRL),
        (26, "ITENS VARIÁVEIS POR NOITE VENDIDA (R$)", f'=IF(N(B6)<=0,"",B25/B6)', BRL),
        (27, "Parte do custo variável da Folha explicada pela Matriz", f'=IF(OR(B26="",N(B9)<=0),"",B26/B9)', "0.0%"),
        (28, "Custo variável fora da Matriz, por noite (R$)", f'=IF(OR(B26="",N(B9)<=0),"",B9-B26)', BRL),
        (29, "Itens variáveis num mês cheio de 30 dias (R$)", f'=IF(OR(B26="",N(B8)<=0),"",B26*B8*30)', BRL),
        (30, "Diferença para a menor cotação no período (R$)", f"=SUM({M})", BRL),
        (31, "Diferença em doze meses (R$) · conta, não previsão", f'=IF(N(B5)<=0,"",B30*12/B5)', BRL),
        (32, "Itens com três cotações e preço de hoje", f'=SUMPRODUCT(({A}<>"")*({J}>=3)*(E{I1}:E{I2}>0))', "0"),
        (33, "Itens sem três cotações", f'=SUMPRODUCT(({A}<>"")*({J}<3))', "0"),
        (34, "Itens sem contrato", f'=COUNTIFS({A},"<>",{Ii},"Sem contrato")', "0"),
        (35, "Item que mais pesa", f'=IF(COUNT({Cc})=0,"",INDEX({A},MATCH(MAX({Cc}),{Cc},0)))', "@"),
    ]
    for l, txt_, f, fmt in res: rotulo(mz, l, txt_); calc(mz, l, f, fmt, l in (26, 30))
    rotulo(mz, 36, "Situação dos dados")
    situacao(mz, 36, f'=IF(OR(B5="",B6="",B8=""),"Preencha os meses, as noites vendidas e as unidades",IF(OR(B5<1,B5>12,B6<1,B8<1),"Meses de 1 a 12, noites e unidades a partir de 1",IF(COUNTA({A})=0,"Informe pelo menos um item",IF(SUMPRODUCT(({A}<>"")*(C{I1}:C{I2}<=0))>0,"Há item sem gasto",IF(SUMPRODUCT(({A}<>"")*({D}=""))>0,"Escolha o tipo de cada item",IF(MIN(C{I1}:H{I2})<0,"Há valor negativo",IF(SUMPRODUCT(({A}<>"")*({J}>0)*(E{I1}:E{I2}<=0))>0,"Informe o preço de hoje dos itens cotados",IF(AND(COUNTIF({Ii},"Vou fechar")>0,B10=""),"Marque até quando vai fechar os contratos","OK"))))))))')
    nota(mz, 38, "Fonte: Panorama · Trilha B · Pilar G5 (lista por valor, três cotações, contrato nos recorrentes, consumo por hóspede) e Etapa 09 (gasto de três meses ÷ diárias vendidas).")
    dvn = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, errorTitle="Valor inválido", error="Use um número maior ou igual a zero."); mz.add_data_validation(dvn); dvn.add(f"C{I1}:C{I2}"); dvn.add(f"E{I1}:H{I2}"); dvn.add("B6:B9")
    dvt = DataValidation(type="list", formula1='"Variável,Vendido à parte"', allow_blank=True); mz.add_data_validation(dvt); dvt.add(D)
    dvc = DataValidation(type="list", formula1='"Tem contrato,Vou fechar,Sem contrato"', allow_blank=True); mz.add_data_validation(dvc); dvc.add(Ii)

    # ---------- Estoque ----------
    es = wb.create_sheet("Estoque"); es.sheet_view.showGridLines = False
    es["A1"] = "Estoque mínimo e ponto de pedido · conte toda semana, no mesmo dia"; es["A1"].font = T(16, True, MUSGO)
    es["A2"] = rot2[0] if exemplo else "Uma linha por item guardado (amarelo)."; es["A2"].font = rot2[1] if exemplo else T(10, True, DOURADO)
    cab(es, 4, ["Item", "Unidade", "Uso por mês", "Entrega (dias)", "Segurança (dias)", "Estoque de hoje", "Compra a cada (dias)", "Consumo por dia", "Estoque mínimo", "Ponto de pedido", "Situação", "Pedido sugerido"],
        [30, 12, 10, 10, 11, 11, 11, 11, 11, 11, 14, 11], 40)
    for i, l in enumerate(range(E1, E2 + 1)):
        d = e["estoque"][i] if exemplo and i < len(e["estoque"]) else (None,) * 7
        for col, v in enumerate(d, 1): entrada(es, l, v, {1: "@", 2: "@", 3: "0.00", 4: "0", 5: "0", 6: "0.00", 7: "0"}[col], col)
        calc(es, l, f'=IF(OR(A{l}="",N(C{l})<=0),"",C{l}/30)', "0.000", False, 8)
        calc(es, l, f'=IF(H{l}="","",ROUNDUP(H{l}*E{l}-0.000001,0))', "0", False, 9)
        calc(es, l, f'=IF(H{l}="","",ROUNDUP(H{l}*(D{l}+E{l})-0.000001,0))', "0", False, 10)
        calc(es, l, f'=IF(H{l}="","",IF(F{l}<=J{l},"Pedir agora","OK"))', "@", False, 11)
        calc(es, l, f'=IF(K{l}<>"Pedir agora",IF(H{l}="","",0),MAX(0,ROUNDUP(H{l}*(D{l}+E{l})+H{l}*G{l}-F{l}-0.000001,0)))', "0", False, 12)
    es.conditional_formatting.add(f"K{E1}:K{E2}", FormulaRule(formula=[f'K{E1}="Pedir agora"'], fill=ALERTA, font=Font(color="9B2C1F", bold=True)))
    faixa(es, 16, "O ENXOVAL (a fonte recomenda três jogos por cama)", 4)
    rotulo(es, 17, "Camas (de todas as unidades)"); entrada(es, 17, e.get("camas"), "0")
    rotulo(es, 18, "Jogos de cama completos em uso"); entrada(es, 18, e.get("jogos"), "0")
    rotulo(es, 19, "Jogos por cama"); calc(es, 19, '=IF(N(B17)<=0,"",B18/B17)', "0.0")
    rotulo(es, 20, "Jogos que faltam para três por cama"); calc(es, 20, '=IF(N(B17)<=0,0,MAX(0,3*B17-B18))', "0")
    rotulo(es, 22, "Itens para pedir agora"); calc(es, 22, f'=COUNTIF(K{E1}:K{E2},"Pedir agora")', "0", True)
    rotulo(es, 23, "Situação dos dados")
    situacao(es, 23, f'=IF(COUNTA(A{E1}:A{E2})=0,"Informe pelo menos um item do estoque",IF(SUMPRODUCT((A{E1}:A{E2}<>"")*((C{E1}:C{E2}<=0)+(D{E1}:D{E2}="")+(E{E1}:E{E2}="")+(F{E1}:F{E2}="")+(G{E1}:G{E2}<=0)))>0,"Complete uso, entrega, segurança, estoque de hoje e intervalo de cada item",IF(MIN(C{E1}:G{E2})<0,"Há valor negativo",IF(AND(N(B17)>0,B18=""),"Informe os jogos de cama","OK"))))')
    nota(es, 25, "Consumo por dia = uso do mês ÷ 30. Mínimo e ponto de pedido: definição-padrão de gestão de estoque, arredondados para cima. Rotina Zion: contagem toda segunda-feira; chegou ao mínimo, aciona o fornecedor.")
    nota(es, 26, "Para o controle peça por peça do enxoval, use a Ferramenta 13 · Controle de Enxoval e Reposição.")
    dve = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, errorTitle="Valor inválido", error="Use um número maior ou igual a zero."); es.add_data_validation(dve); dve.add(f"C{E1}:G{E2}"); dve.add("B17:B18")

    # ---------- Manutenção 12 meses ----------
    mn = wb.create_sheet("Manutenção 12 meses"); mn.sheet_view.showGridLines = False
    mn["A1"] = "Calendário de manutenção preventiva de 12 meses · e a reserva que paga por ele"; mn["A1"].font = T(16, True, MUSGO)
    mn["A2"] = rot2[0] if exemplo else "Preencha as células amarelas. Frequência e custo: manual do fabricante e profissional responsável."; mn["A2"].font = rot2[1] if exemplo else T(10, True, DOURADO)
    faixa(mn, 3, "A RESERVA DE MANUTENÇÃO E REPOSIÇÃO", 4)
    rotulo(mn, 4, "Ano em que o calendário começa"); entrada(mn, 4, e.get("ano"), "0")
    rotulo(mn, 5, "Primeiro mês (1 a 12)"); entrada(mn, 5, e.get("inicio") if exemplo else 1, "0")
    rotulo(mn, 6, "Receita real de um mês comum (R$)", "Folha Única (Módulo 2): depois de comissão, taxas e imposto.", 4); entrada(mn, 6, e.get("receita"))
    rotulo(mn, 7, "Reserva de manutenção (% da receita)", "A fonte: de 3% a 6% da receita por mês.", 4); entrada(mn, 7, e.get("reserva"), "0.0")
    rotulo(mn, 8, "Reserva por mês (R$)"); calc(mn, 8, '=IF(OR(B6="",B7=""),"",B6*B7/100)')
    rotulo(mn, 9, "Reserva no ano (R$)"); calc(mn, 9, '=IF(B8="","",B8*12)')
    cab(mn, 12, ["Tarefa preventiva", "Frequência", "Primeiro mês (1 a 12)", "Custo por vez (R$)", "Quem faz", "Vezes no ano", "Custo no ano (R$)", "Vezes em mês de casa cheia (semestral ou anual)", "Passo (meses)"],
        [38, 13, 11, 12, 24, 10, 13, 16, 9], 46)
    MC = f"$C${C1}:$C${C2}"; MD = f"$D${C1}:$D${C2}"
    for i, l in enumerate(range(T1, T2 + 1)):
        d = e["tarefas"][i] if exemplo and i < len(e["tarefas"]) else (None,) * 5
        for col, v in enumerate(d, 1): entrada(mn, l, v, {1: "@", 2: "@", 3: "0", 4: BRL, 5: "@"}[col], col)
        calc(mn, l, f'=IF(A{l}="",1000,IF(B{l}="Mensal",1,IF(B{l}="Bimestral",2,IF(B{l}="Trimestral",3,IF(B{l}="Semestral",6,IF(B{l}="Anual",12,1000))))))', "0", False, 9)
        ok_ = f'(I{l}<1000)*(N(C{l})>=1)*(N(C{l})<=12)'
        calc(mn, l, f'=IF(A{l}="","",SUMPRODUCT({ok_}*(MOD(MOD({MC}-N(C{l})+12,12),I{l})=0)))', "0", False, 6)
        calc(mn, l, f'=IF(A{l}="","",F{l}*N(D{l}))', BRL, False, 7)
        calc(mn, l, f'=IF(A{l}="","",SUMPRODUCT({ok_}*(I{l}>=6)*({MD}="Sim")*(MOD(MOD({MC}-N(C{l})+12,12),I{l})=0)))', "0", False, 8)
    TA, TB, TC, TD, TI = (f"${x}${T1}:${x}${T2}" for x in "ABCDI")
    cab(mn, 30, ["Mês", "Ano", "Nº do mês", "Casa cheia? (Sim/Não)", "Tarefas no mês", "Custo do mês (R$)", "Reserva acumulada (R$)", "Gasto acumulado (R$)", "A reserva cobre?"], None, 40)
    mn.cell(29, 1, "CALENDÁRIO DOS DOZE MESES").font = T(11, True, MUSGO)
    for i, l in enumerate(range(C1, C2 + 1)):
        calc(mn, l, f'=IF(OR($B$4="",$B$5=""),"",CHOOSE(MOD($B$5-1+{i},12)+1,"jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"))', "@", False, 1)
        calc(mn, l, f'=IF(OR($B$4="",$B$5=""),"",$B$4+INT(($B$5-1+{i})/12))', "0", False, 2)
        calc(mn, l, f'=IF(OR($B$4="",$B$5=""),"",MOD($B$5-1+{i},12)+1)', "0", False, 3)
        cheio = ("Sim" if (((EX["inicio"] - 1 + i) % 12) + 1) in EX["cheia"] else "Não") if exemplo else None
        entrada(mn, l, cheio, "@", 4)
        cond = f'({TI}<1000)*({TC}>=1)*({TC}<=12)*(MOD(MOD(C{l}-{TC}+12,12),{TI})=0)'
        calc(mn, l, f'=IF(C{l}="","",SUMPRODUCT({cond}))', "0", False, 5)
        calc(mn, l, f'=IF(C{l}="","",SUMPRODUCT({cond}*{TD}))', BRL, False, 6)
        calc(mn, l, f'=IF(OR(C{l}="",$B$8=""),"",$B$8*{i + 1})', BRL, False, 7)
        calc(mn, l, f'=IF(C{l}="","",SUM($F${C1}:F{l}))', BRL, False, 8)
        calc(mn, l, f'=IF(OR(G{l}="",H{l}=""),"",IF(H{l}>G{l}+0.005,"Não cobre","Cobre"))', "@", False, 9)
    mn.conditional_formatting.add(f"I{C1}:I{C2}", FormulaRule(formula=[f'I{C1}="Não cobre"'], fill=ALERTA, font=Font(color="9B2C1F", bold=True)))
    faixa(mn, 45, "RESUMO DO CALENDÁRIO", 4)
    rotulo(mn, 46, "Tarefas no ano"); calc(mn, 46, f"=SUM(E{C1}:E{C2})", "0")
    rotulo(mn, 47, "CUSTO DO PLANO NO ANO (R$)"); calc(mn, 47, f"=SUM(F{C1}:F{C2})", BRL, True)
    rotulo(mn, 48, "Mês mais pesado"); calc(mn, 48, f'=IF(MAX(F{C1}:F{C2})<=0,"",INDEX(A{C1}:A{C2},MATCH(MAX(F{C1}:F{C2}),F{C1}:F{C2},0)))', "@")
    rotulo(mn, 49, "Custo do mês mais pesado (R$)"); calc(mn, 49, f"=MAX(F{C1}:F{C2})")
    rotulo(mn, 50, "Sobra da reserva no ano para reposição (R$)", "Pintura, telhado, equipamento.", 4); calc(mn, 50, '=IF(B9="","",B9-B47)')
    rotulo(mn, 51, "Meses em que a reserva acumulada não cobre"); calc(mn, 51, f'=COUNTIF(I{C1}:I{C2},"Não cobre")', "0")
    rotulo(mn, 52, "Tarefas pesadas em mês de casa cheia"); calc(mn, 52, f"=SUM(H{T1}:H{T2})", "0")
    rotulo(mn, 53, "Situação dos dados")
    situacao(mn, 53, f'=IF(OR(B4="",B5="",B6="",B7=""),"Preencha o ano, o primeiro mês, a receita e a reserva",IF(OR(B4<2024,B4>2099,B5<1,B5>12),"Ano de 2024 a 2099 e mês de 1 a 12",IF(OR(B6<0,B7<0,B7>99.9),"Receita e reserva válidas",IF(COUNTA({TA})=0,"Informe pelo menos uma tarefa",IF(SUMPRODUCT(({TA}<>"")*(({TI}>=1000)+({TC}<1)+({TC}>12)))>0,"Escolha a frequência e o primeiro mês de cada tarefa",IF(MIN({TD})<0,"Há custo negativo","OK"))))))')
    nota(mn, 55, "Fonte: Etapa 09 · Passo 06 (reserva de manutenção de 3% a 6% da receita) e Etapa 10 (manutenção preventiva com o calendário do ano). Regra da Zion: obra e manutenção pesada na baixa ocupação, de segunda a quinta.")
    dvf = DataValidation(type="list", formula1='"Mensal,Bimestral,Trimestral,Semestral,Anual"', allow_blank=True); mn.add_data_validation(dvf); dvf.add(f"B{T1}:B{T2}")
    dvm = DataValidation(type="whole", operator="between", formula1="1", formula2="12", showErrorMessage=True, errorTitle="Mês inválido", error="Use um número de 1 a 12."); mn.add_data_validation(dvm); dvm.add(f"C{T1}:C{T2}"); dvm.add("B5")
    dvs = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); mn.add_data_validation(dvs); dvs.add(f"D{C1}:D{C2}")

    # ---------- Rotina e checklist ----------
    ro = wb.create_sheet("Rotina e checklist"); ro.sheet_view.showGridLines = False
    for col, w in zip("ABC", (56, 22, 60)): ro.column_dimensions[col].width = w
    ro["A1"] = "Rotina de compras e manutenção"; ro["A1"].font = T(16, True, MUSGO)
    ro["A2"] = rot2[0] if exemplo else "Compras e reposição: procedimento semanal. Manutenção preventiva: mensal."; ro["A2"].font = rot2[1] if exemplo else T(10, True, DOURADO)
    rotulo(ro, 4, "Dia da contagem semanal do estoque", "Na Zion, toda segunda-feira."); entrada(ro, 4, e.get("dia"), "@")
    rotulo(ro, 5, "Quem faz as compras", "Uma pessoa, com nome."); entrada(ro, 5, e.get("quem"), "@")
    rotulo(ro, 6, "Até quanto a equipe compra fora do previsto sem perguntar (R$)", "Na fonte, o exemplo é R$ 300."); entrada(ro, 6, e.get("alcada"))
    rotulo(ro, 7, "Faço a ronda técnica diária com lista? (Sim/Não)"); entrada(ro, 7, e.get("ronda"), "@")
    rotulo(ro, 8, "Registro cada problema num quadro de ocorrências? (Sim/Não)", "Ferramenta 14 · Quadro de Ocorrências e Manutenção."); entrada(ro, 8, e.get("ocorr"), "@")
    dvd = DataValidation(type="list", formula1='"segunda-feira,terça-feira,quarta-feira,quinta-feira,sexta-feira,sábado,domingo"', allow_blank=True); ro.add_data_validation(dvd); dvd.add("B4")
    dvr = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); ro.add_data_validation(dvr); dvr.add("B7:B8")
    faixa(ro, 10, "CHECKLIST DO MÊS (10 itens)")
    itens = ["A contagem do estoque aconteceu toda semana, no mesmo dia",
             "Nenhum item ficou abaixo do estoque mínimo",
             "Cada compra entrou no histórico (data, item, quantidade, fornecedor, valor)",
             "Os itens que mais pesam foram revistos por valor",
             "Os itens sem três cotações receberam cotação nova",
             "Os contratos marcados \"Vou fechar\" estão dentro do prazo",
             "As tarefas preventivas do mês foram feitas e anotadas",
             "A reserva de manutenção do mês foi separada numa conta própria",
             "A ronda diária foi anotada todos os dias",
             "Fornecedores e custos foram revistos (rotina mensal da Zion)"]
    cab(ro, 11, ["Item", "Feito?", ""], None, 20)
    for i, t in enumerate(itens):
        ro.cell(12 + i, 1, f"{i + 1}. {t}").alignment = Alignment(wrap_text=True)
        x = ro.cell(12 + i, 2, ("Sim" if i < 7 else "Não") if exemplo else None); x.fill = ENTRADA; x.border = borda
    dvk = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); ro.add_data_validation(dvk); dvk.add("B12:B21")
    ro.cell(23, 1, "Itens feitos:"); x = ro.cell(23, 2, '=COUNTIF(B12:B21,"Sim")'); x.fill = CALC; x.border = borda; x.font = T(12, True, MUSGO)
    ro.cell(24, 1, '=IF(B23=10,"Mês completo: 10 de 10","Faltam "&(10-B23)&" de 10 itens")').font = T(10, True, MUSGO)

    # ---------- Resumo ----------
    rs = wb.create_sheet("Resumo"); rs.sheet_view.showGridLines = False
    for col, w in zip("ABC", (60, 26, 60)): rs.column_dimensions[col].width = w
    rs["A1"] = "Resumo · página 6 do Plano de Gestão"; rs["A1"].font = T(16, True, MUSGO)
    rs["A2"] = rot2[0] if exemplo else "Tudo calculado a partir das outras abas."; rs["A2"].font = rot2[1] if exemplo else T(10, True, DOURADO)
    faixa(rs, 4, "OS NÚMEROS")
    nums = [(5, "Itens variáveis por noite vendida (R$)", f"={MZ}B26", BRL), (6, "Parte do custo variável da Folha explicada", f"={MZ}B27", "0.0%"),
            (7, "Total da Matriz no período (R$)", f"={MZ}B24", BRL), (8, "Diferença para a menor cotação no período (R$)", f"={MZ}B30", BRL),
            (9, "Diferença em doze meses (R$) · conta, não previsão", f"={MZ}B31", BRL), (10, "Itens para pedir agora", f"={ES}B22", "0"),
            (11, "Jogos de cama por cama", f"={ES}B19", "0.0"), (12, "Custo do plano de manutenção no ano (R$)", f"={MN}B47", BRL),
            (13, "Reserva de manutenção no ano (R$)", f"={MN}B9", BRL), (14, "Sobra da reserva para reposição (R$)", f"={MN}B50", BRL)]
    for l, t_, f, fmt in nums: rotulo(rs, l, t_); calc(rs, l, f, fmt)
    faixa(rs, 16, "OS SINAIS DE ATENÇÃO (na ordem da fonte: cotar, contratar, estoque, enxoval, manutenção, rotina)")
    regras = [
        (17, "Item sem três cotações", f"={MZ}B33>0"),
        (18, "Compra recorrente sem contrato", f"={MZ}B34>0"),
        (19, "Item no ponto de pedido", f"={ES}B22>0"),
        (20, "Menos de três jogos por cama", f'=IF(N({ES}B17)>0,{ES}B18/{ES}B17<3,FALSE())'),
        (21, "Manutenção pesada na casa cheia", f"={MN}B52>0"),
        (22, "A reserva não cobre o plano", f"=AND(COUNTA({MN}A{T1}:A{T2})>0,{MN}B51>0)"),
        (23, "Sem ronda diária ou sem registro de ocorrências", f'=OR({RO}B7<>"Sim",{RO}B8<>"Sim")'),
        (24, "Estoque sem dia de contagem ou compra sem limite", f'=OR({RO}B4="",N({RO}B6)<=0)'),
    ]
    for l, t_, f in regras:
        rotulo(rs, l, t_); c = calc(rs, l, f'=IF({f[1:]},"Sim","Não")', "@")
    rs.conditional_formatting.add("B17:B24", FormulaRule(formula=['B17="Sim"'], fill=ALERTA, font=Font(color="9B2C1F", bold=True)))
    rotulo(rs, 26, "CAUSA PRINCIPAL")
    calc(rs, 26, '=IF(COUNTIF(B17:B24,"Sim")=0,"Compras e manutenção dentro das regras da fonte",INDEX(A17:A24,MATCH("Sim",B17:B24,0)))', "@", True)
    rotulo(rs, 27, "Situação das abas")
    situacao(rs, 27, f'=IF({MZ}B36<>"OK","Confira a aba Matriz de Compras",IF({ES}B23<>"OK","Confira a aba Estoque",IF({MN}B53<>"OK","Confira a aba Manutenção 12 meses","OK")))')
    nota(rs, 29, "A causa principal é o primeiro sinal que dispara, na mesma ordem da ficha. Prioridades e plano de ação ficam na ficha \"A minha Matriz de Compras e Manutenção\" (PDF).")
    wb.active = 0
    return wb

for exemplo, nome in ((False, "Matriz-de-Compras-e-Manutencao-Zion-EM-BRANCO.xlsx"), (True, "Matriz-de-Compras-e-Manutencao-Zion-EXEMPLO.xlsx")):
    montar(exemplo).save(OUT / nome); print("ok", OUT / nome)

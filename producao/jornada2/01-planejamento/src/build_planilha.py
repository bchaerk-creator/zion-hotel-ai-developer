"""Gera a planilha "Painel de Gestão" (Jornada 2 · Gestão · Módulo 1 · Planejamento, metas e indicadores) em duas versões:
   - Painel-de-Gestao-Zion-EM-BRANCO.xlsx
   - Painel-de-Gestao-Zion-EXEMPLO.xlsx (dados fictícios, identificados como exemplo)
Uso: python3 -I build_planilha.py <pasta-saida>
Molde: producao/jornada2/02-financas/src/build_planilha.py (amarelo = preenche, verde = calculado).
Abas: Comece aqui · Metas e donos · Painel 12 meses · Reunião semanal · Plano 6 semanas · Definições e rotina."""
import sys, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, DOURADO, PRETO, CREME = "1B2117", "8B714E", "040605", "FEF5F0"
ENTRADA = PatternFill("solid", fgColor="FFF4C7"); CALC = PatternFill("solid", fgColor="E3EEDF"); CAB = PatternFill("solid", fgColor=MUSGO)
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
BRL = 'R$ #,##0.00;[Red]-R$ #,##0.00'; PCT = '0.0" %"'; NOTA = "0.0"
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)

def faixa(ws, linha, texto, cols=3):
    ws.merge_cells(start_row=linha, start_column=1, end_row=linha, end_column=cols)
    c = ws.cell(linha, 1, texto); c.font = T(11, True, CREME); c.fill = CAB; c.alignment = Alignment(vertical="center", indent=1); ws.row_dimensions[linha].height = 22
def rotulo(ws, l, texto, ajuda="", col_ajuda=3):
    a = ws.cell(l, 1, texto); a.font = T(11); a.alignment = Alignment(wrap_text=True, vertical="center")
    if ajuda: h = ws.cell(l, col_ajuda, ajuda); h.font = T(9, c="5F5F55", i=True); h.alignment = Alignment(wrap_text=True, vertical="center")
def entrada(ws, l, valor=None, fmt=BRL, col=2):
    c = ws.cell(l, col, valor); c.fill = ENTRADA; c.border = borda; c.number_format = fmt; c.font = T(11, True); c.alignment = Alignment(wrap_text=True, vertical="center"); return c
def calc(ws, l, formula, fmt=BRL, destaque=False, col=2):
    c = ws.cell(l, col, formula); c.fill = CALC; c.border = borda; c.number_format = fmt; c.font = T(13 if destaque else 10, True, MUSGO if destaque else PRETO); c.alignment = Alignment(wrap_text=True, vertical="center"); return c
def cabecalho(ws, linha, cols, larguras=None, altura=34):
    for i, t in enumerate(cols, 1):
        x = ws.cell(linha, i, t); x.font = T(10, True, CREME); x.fill = CAB; x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); x.border = borda
        if larguras: ws.column_dimensions[x.column_letter].width = larguras[i - 1]
    ws.row_dimensions[linha].height = altura

# Os cinco indicadores do Pilar G7, na ordem da ficha (linhas 12 a 16 da aba Metas e donos)
IND = [("Ocupação", "%", PCT, "Noites vendidas ÷ noites disponíveis do mês."),
       ("Diária média", "R$", BRL, "Receita de hospedagem ÷ noites vendidas."),
       ("Resultado do mês (quanto sobrou)", "R$", BRL, "Tudo o que entrou menos tudo o que saiu, com a sua retirada dentro (Folha Única, Módulo 2). Pode ser negativo."),
       ("Nota das avaliações", "nota", NOTA, "Média das avaliações do mês no principal canal, sempre o mesmo canal (definição-padrão de hotelaria)."),
       ("Taxa de venda direta", "%", PCT, "Parte da receita de hospedagem que entrou sem plataforma: site, WhatsApp, indicação, hóspede que volta (definição-padrão de hotelaria).")]
L0 = 12  # primeira linha dos indicadores

# Exemplo didático · dados fictícios (Cabanas do Vale). Mesmos valores da ficha (logic.js EXEMPLO) e do PLANO seção 9.
EX = dict(mes="Outubro de 2026 (exemplo)", dias=31, unidades=4, escala=5,
          base=[46.8, 280, 11890, 4.7, 12], meta=[50, 300, 13000, 4.8, 20], dono=["Ana"] * 5, corte=None, equilibrio=None)
EX_MESES = [  # Painel 12 meses: realizado e mesmo mês do ano anterior (dados fictícios)
    ("Outubro de 2026 (exemplo)", [46.8, 280, 11890, 4.7, 12], [41.9, 265, 10400, 4.6, 8]),
    ("Novembro de 2026 (exemplo)", [38.3, 285, 8950, 4.8, 14], [40.0, 270, 9300, 4.6, 9]),
]
EX_REUNIOES = [
    ("16/11/2026", 46.8, 280, 11890, 4.7, 12, "Venda direta sem registro por canal", "Anotar o canal de cada reserva nova", "Ana", "23/11/2026"),
    ("23/11/2026", 46.8, 280, 11890, 4.8, 13, "Duas avaliações da semana citaram o chuveiro", "Chamar a manutenção para os chuveiros", "Ana", "27/11/2026"),
]
EX_PLANO = [("Módulo 2 · Finanças, fluxo de caixa e fechamento", "O pilar mais fraco: não sei quanto sobra com a minha retirada.", "Fechar outubro na Folha Única e lançar a minha retirada.", "Sim"),
            ("Módulo 3 · Preço, reservas e distribuição", "Destrava a meta de diária.", "Calcular o piso da diária antes de subir para R$ 300.", "Não"),
            ("Módulo 4 · Marketing e vendas", "Dá o número da venda direta.", "Anotar o canal de cada reserva para medir a venda direta.", "Não")]
EX_DEPOIS = "Compras e estoque: já funciona com lista; fica para depois da alta temporada."

def montar(exemplo):
    wb = Workbook()
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False; ws.column_dimensions["A"].width = 100
    linhas = [
        ("ZION HOSPITALITY BUSINESS · JORNADA 2 · GESTÃO · MÓDULO 1 · PLANEJAMENTO", T(10, True, DOURADO)),
        ("Painel de Gestão", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para acompanhar a sua hospedagem com cinco números, um dono para cada um, metas para os próximos 12 meses e uma reunião semanal de trinta minutos.", T(11, c="2D352A")),
        ("EXEMPLO DIDÁTICO PREENCHIDO COM DADOS FICTÍCIOS (Cabanas do Vale). Use a versão em branco para os seus números." if exemplo else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("", None),
        ("COMO USAR EM 4 PASSOS (cerca de 20 minutos na primeira vez, 30 minutos por semana depois)", T(12, True, MUSGO)),
        ("1. Aba Metas e donos: escreva o mês de partida, os cinco números desse mês (deixe em branco o que não sabe), a meta de cada um para o mesmo mês daqui a 12 meses e quem olha cada número. A linha \"Situação dos dados\" precisa mostrar OK.", None),
        ("2. Aba Reunião semanal: marque o dia e a hora. Toda semana, anote os mesmos cinco números, o que saiu do esperado e uma decisão com dono e prazo.", None),
        ("3. Aba Painel 12 meses: no fim de cada mês, lance os cinco números e, ao lado, os do mesmo mês do ano anterior (no primeiro ano, use a sua projeção). A planilha diz se melhorou, ficou igual ou piorou.", None),
        ("4. Aba Plano 6 semanas: os três pilares que você vai atacar e o que vai deixar para depois, de propósito.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("O QUE A PLANILHA FAZ E O QUE ELA NÃO FAZ", T(12, True, MUSGO)),
        ("Faz: guarda os cinco indicadores do Pilar G7 do Método Zion (ocupação, diária média, resultado, nota e taxa de venda direta), mostra a variação entre o ponto de partida e a meta, calcula as noites e a receita de hospedagem que as metas pedem e compara cada mês com o mesmo mês do ano anterior.", None),
        ("Não faz: não prevê ocupação, diária ou resultado, não conhece o mercado da sua região e não diz qual meta é \"certa\". Meta é decisão sua, escrita com número e prazo. Não troque de indicador antes de 12 semanas: o valor vem da série histórica.", None),
        ("Percentuais: escreva 46,8 para 46,8% (sem o símbolo). Nota: na escala do seu principal canal (5 ou 10).", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Material educativo: não é promessa de renda, retorno, ocupação ou resultado. A gestão depende da execução de cada hospedagem.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Metas e donos ----------
    m = wb.create_sheet("Metas e donos"); m.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHI", (34, 9, 16, 16, 18, 20, 34, 16, 14)): m.column_dimensions[col].width = w
    m["A1"] = "Metas e donos · o Painel de Gestão"; m["A1"].font = T(18, True, MUSGO)
    m["A2"] = "EXEMPLO DIDÁTICO · dados fictícios (Cabanas do Vale)" if exemplo else "Preencha as células amarelas. Células em verde são calculadas."; m["A2"].font = T(10, True, "A0522D" if exemplo else DOURADO)
    e = EX if exemplo else {}
    faixa(m, 3, "1 · O MÊS DE PARTIDA", 7)
    rotulo(m, 4, "Mês de partida", "As metas valem para o mesmo mês daqui a 12 meses.", 3); entrada(m, 4, e.get("mes"), "@")
    rotulo(m, 5, "Dias do mês", "28, 29, 30 ou 31.", 3); entrada(m, 5, e.get("dias"), "0")
    rotulo(m, 6, "Unidades à venda", "Só as abertas para reserva no mês.", 3); entrada(m, 6, e.get("unidades"), "0")
    rotulo(m, 7, "Noites disponíveis no mês", "Dias × unidades.", 3); calc(m, 7, '=IF(OR(B5="",B6=""),"",B5*B6)', "0")
    rotulo(m, 8, "Escala da nota (5 ou 10)", "A escala do seu principal canal.", 3); entrada(m, 8, e.get("escala"), "0")
    faixa(m, 10, "2 · OS CINCO INDICADORES (ponto de partida em branco = não sei)", 9)
    cabecalho(m, 11, ["Indicador", "Unidade", "Ponto de partida", "Meta em 12 meses", "Dono (quem olha)", "Variação (meta − partida)", "Leitura", "Número no mês de chegada", "Meta atingida?"])
    for k, (nome, un, fmt, _) in enumerate(IND):
        l = L0 + k
        m.cell(l, 1, nome).font = T(11, True); m.cell(l, 1).alignment = Alignment(wrap_text=True, vertical="center"); m.cell(l, 1).border = borda
        m.cell(l, 2, un).alignment = Alignment(horizontal="center", vertical="center"); m.cell(l, 2).border = borda
        entrada(m, l, e["base"][k] if exemplo else None, fmt, 3); entrada(m, l, e["meta"][k] if exemplo else None, fmt, 4); entrada(m, l, e["dono"][k] if exemplo else None, "@", 5)
        calc(m, l, f'=IF(OR(C{l}="",D{l}=""),"",D{l}-C{l})', fmt, False, 6)
        calc(m, l, f'=IF(D{l}="","Falta a meta",IF(C{l}="","Sem ponto de partida: o primeiro mês do painel vira a base",IF(D{l}>C{l},"Meta acima do ponto de partida",IF(D{l}=C{l},"Manter: válido, desde que escrito","Meta abaixo do ponto de partida: escreva o porquê"))))', "@", False, 7)
        entrada(m, l, None, fmt, 8)
        calc(m, l, f'=IF(OR(H{l}="",D{l}=""),"",IF(H{l}>=D{l},"Sim","Ainda não"))', "@", False, 9)
        m.row_dimensions[l].height = 34
    faixa(m, 18, "3 · O QUE AS METAS PEDEM E DUAS CONFERÊNCIAS", 7)
    rotulo(m, 19, "Noites vendidas que a meta de ocupação pede no mês de chegada", "Meta de ocupação × noites disponíveis.", 3); calc(m, 19, f'=IF(OR(D{L0}="",B7=""),"",D{L0}/100*B7)', "0.0")
    rotulo(m, 20, "Receita de hospedagem que as metas pedem no mês de chegada", "Noites da meta × meta de diária.", 3); calc(m, 20, f'=IF(OR(B19="",D{L0+1}=""),"",B19*D{L0+1})', BRL, True)
    rotulo(m, 21, "Variação contra o ponto de partida (ocupação × diária)", "Quanto a receita por noite disponível precisa subir.", 3); calc(m, 21, f'=IF(OR(C{L0}="",C{L0+1}="",D{L0}="",D{L0+1}=""),"",IF(C{L0}*C{L0+1}=0,"",(D{L0}*D{L0+1})/(C{L0}*C{L0+1})-1))', "0.0%")
    rotulo(m, 22, "Ocupação de equilíbrio (%) · opcional", "Da Folha Única do Mês (Módulo 2).", 3); entrada(m, 22, e.get("equilibrio"), PCT)
    rotulo(m, 23, "Número de corte mensal (R$) · opcional", "Resultado mínimo abaixo do qual você muda alguma coisa (Módulo 2).", 3); entrada(m, 23, e.get("corte"), BRL)
    rotulo(m, 24, "Conferência: meta de ocupação × equilíbrio"); calc(m, 24, f'=IF(OR(B22="",D{L0}=""),"Sem ocupação de equilíbrio (faça no Módulo 2)",IF(D{L0}<B22,"Atenção: a meta de ocupação não paga o custo fixo","OK: meta de ocupação acima do equilíbrio"))', "@")
    rotulo(m, 25, "Conferência: meta de resultado × número de corte"); calc(m, 25, f'=IF(OR(B23="",D{L0+2}=""),"Sem número de corte (faça no Módulo 2)",IF(D{L0+2}<B23,"Atenção: a meta de resultado fica abaixo do corte","OK: meta de resultado acima do corte"))', "@")
    m.merge_cells("B24:D24"); m.merge_cells("B25:D25")
    rotulo(m, 27, "Situação dos dados")
    L1, L2, L3, L4, L5 = (L0 + k for k in range(5))
    sit = (f'=IF(OR(B4="",B5="",B6=""),"Preencha o mês, os dias e as unidades",'
           f'IF(OR(B5<28,B5>31,B5<>INT(B5)),"Dias do mês: use 28 a 31",'
           f'IF(OR(B6<1,B6<>INT(B6)),"Unidades: número inteiro a partir de 1",'
           f'IF(AND(B8<>5,B8<>10),"Escala da nota: 5 ou 10",'
           f'IF(COUNTBLANK(D{L1}:D{L5})>0,"Falta meta em algum indicador",'
           f'IF(COUNTBLANK(E{L1}:E{L5})>0,"Falta o dono de algum indicador",'
           f'IF(OR(MIN(C{L1},D{L1},C{L5},D{L5})<0,MAX(C{L1},D{L1},C{L5},D{L5})>100),"Ocupação e venda direta: de 0 a 100",'
           f'IF(OR(MIN(C{L2},D{L2})<0,D{L2}=0,D{L1}=0),"Diária não pode ser negativa; metas de ocupação e diária maiores que zero",'
           f'IF(OR(MIN(C{L4},D{L4})<0,MAX(C{L4},D{L4})>B8),"Nota fora da escala","OK")))))))))')
    sp = m.cell(27, 2, sit); sp.font = T(11, True); sp.border = borda; sp.fill = CALC; m.merge_cells("B27:G27")
    m.conditional_formatting.add("B27", FormulaRule(formula=['$B$27<>"OK"'], fill=PatternFill("solid", fgColor="F8E3DE"), font=Font(color="9B2C1F", bold=True)))
    m.cell(29, 1, "Os cinco indicadores vêm do Pilar G7 do Panorama do Desenvolvimento Hoteleiro (Método Zion 360°). As metas são decisões suas, não previsões.").font = T(9, c="5F5F55", i=True)
    dvi = DataValidation(type="whole", operator="between", formula1="28", formula2="31", showErrorMessage=True, errorTitle="Valor inválido", error="Use 28, 29, 30 ou 31."); m.add_data_validation(dvi); dvi.add("B5")
    dvu = DataValidation(type="whole", operator="between", formula1="1", formula2="999", showErrorMessage=True, errorTitle="Valor inválido", error="Use de 1 a 999 unidades."); m.add_data_validation(dvu); dvu.add("B6")
    dve = DataValidation(type="list", formula1='"5,10"', allow_blank=True); m.add_data_validation(dve); dve.add("B8")

    # ---------- Painel 12 meses ----------
    p = wb.create_sheet("Painel 12 meses"); p.sheet_view.showGridLines = False; p.freeze_panes = "B5"
    p["A1"] = "Painel 12 meses · uma linha por mês. Compare sempre com o mesmo mês do ano anterior, nunca com o mês passado." + ("  ·  EXEMPLO FICTÍCIO" if exemplo else ""); p["A1"].font = T(12, True, MUSGO)
    p["A2"] = "No primeiro ano, sem base, use na coluna \"ano anterior\" a sua projeção. Em hospedagem sazonal, junho se compara com junho. Percentuais sem o símbolo (46,8)."; p["A2"].font = T(9, c="5F5F55", i=True)
    curtos = ["Ocupação", "Diária", "Resultado", "Nota", "Venda direta"]
    grupos = [("REALIZADO NO MÊS", 2), ("MESMO MÊS DO ANO ANTERIOR (OU PROJEÇÃO)", 7), ("COMPARAÇÃO", 12)]
    for t, c0 in grupos:
        p.merge_cells(start_row=3, start_column=c0, end_row=3, end_column=c0 + 4); x = p.cell(3, c0, t); x.font = T(9, True, CREME); x.fill = PatternFill("solid", fgColor=DOURADO); x.alignment = Alignment(horizontal="center")
    cab = ["Mês"] + [c + (" (%)" if c in ("Ocupação", "Venda direta") else " (R$)" if c in ("Diária", "Resultado") else "") for c in curtos] * 2 + curtos + ["Quantos melhoraram"]
    cabecalho(p, 4, cab, [24] + [12] * 15 + [14])
    fmts = [PCT, BRL, BRL, NOTA, PCT]
    for l in range(5, 17):
        x = p.cell(l, 1); x.fill = ENTRADA; x.border = borda; x.number_format = "@"
        for k in range(5):
            entrada(p, l, None, fmts[k], 2 + k); entrada(p, l, None, fmts[k], 7 + k)
            a, b = p.cell(l, 2 + k).coordinate, p.cell(l, 7 + k).coordinate
            calc(p, l, f'=IF(OR({a}="",{b}=""),"",IF({a}>{b},"Melhorou",IF({a}={b},"Igual","Piorou")))', "@", False, 12 + k)
        calc(p, l, f'=IF(COUNTA(B{l}:F{l})=0,"",COUNTIF(L{l}:P{l},"Melhorou"))', "0", False, 17)
    if exemplo:
        for i, (mes, real, ant) in enumerate(EX_MESES):
            p.cell(5 + i, 1, mes)
            for k in range(5): p.cell(5 + i, 2 + k, real[k]); p.cell(5 + i, 7 + k, ant[k])
    p.conditional_formatting.add("L5:P16", FormulaRule(formula=['L5="Piorou"'], font=Font(color="9B2C1F", bold=True)))
    p.conditional_formatting.add("L5:P16", FormulaRule(formula=['L5="Melhorou"'], font=Font(color="1F5A33", bold=True)))

    # ---------- Reunião semanal ----------
    r = wb.create_sheet("Reunião semanal"); r.sheet_view.showGridLines = False
    r["A1"] = "Reunião semanal · trinta minutos, mesmos cinco números, mesma hora" + ("  ·  EXEMPLO FICTÍCIO" if exemplo else ""); r["A1"].font = T(14, True, MUSGO)
    rotulo(r, 2, "Dia da semana"); entrada(r, 2, "Segunda-feira" if exemplo else None, "@")
    rotulo(r, 3, "Hora"); entrada(r, 3, "08:00" if exemplo else None, "@")
    rotulo(r, 4, "Minutos"); entrada(r, 4, 30 if exemplo else None, "0")
    r["D2"] = "Pauta: 1. os cinco números, na mesma ordem, cada um pelo seu dono · 2. o que saiu do esperado (meta e mesmo mês do ano anterior) · 3. uma decisão, com dono e prazo · 4. anotar aqui."; r["D2"].font = T(9, c="5F5F55", i=True); r["D2"].alignment = Alignment(wrap_text=True, vertical="top"); r.merge_cells("D2:J4")
    dvd = DataValidation(type="list", formula1='"Segunda-feira,Terça-feira,Quarta-feira,Quinta-feira,Sexta-feira,Sábado,Domingo"', allow_blank=True); r.add_data_validation(dvd); dvd.add("B2")
    cabecalho(r, 6, ["Data", "Ocupação (%)", "Diária (R$)", "Resultado (R$)", "Nota", "Venda direta (%)", "O que saiu do esperado", "Decisão", "Dono da decisão", "Prazo"], [14, 12, 13, 15, 9, 12, 34, 34, 16, 13])
    rf = ["@", PCT, BRL, BRL, NOTA, PCT, "@", "@", "@", "@"]
    for l in range(7, 20):
        for c in range(1, 11): entrada(r, l, None, rf[c - 1], c)
    if exemplo:
        for i, row in enumerate(EX_REUNIOES):
            for c, v in enumerate(row, 1): r.cell(7 + i, c, v)
    rotulo(r, 21, "Reuniões registradas"); calc(r, 21, '=COUNTA(A7:A19)', "0", True)
    rotulo(r, 22, "Leitura"); calc(r, 22, '=IF(B21>=4,"Rotina viva: "&B21&" reuniões com os mesmos cinco números",IF(B21=0,"Nenhuma reunião registrada ainda","Faltam "&(4-B21)&" para o critério das quatro semanas"))', "@")
    r.merge_cells("B22:G22")
    r.cell(24, 1, "Se você sumisse por 30 dias, o que quebraria primeiro? (fica para o Módulo 5 · Pessoas, com as alçadas)").font = T(10, True, MUSGO)
    entrada(r, 25, "As respostas aos hóspedes e a liberação das cabanas depois da limpeza." if exemplo else None, "@", 1); r.merge_cells("A25:H25"); r.row_dimensions[25].height = 30

    # ---------- Plano 6 semanas ----------
    s = wb.create_sheet("Plano 6 semanas"); s.sheet_view.showGridLines = False
    s["A1"] = "O seu plano para as próximas seis semanas · escolha três e faça bem" + ("  ·  EXEMPLO FICTÍCIO" if exemplo else ""); s["A1"].font = T(14, True, MUSGO)
    cabecalho(s, 3, ["Semanas", "Pilar (módulo)", "Por que este", "Primeiro exercício", "Feito?"], [30, 40, 40, 46, 10])
    nomes = ["Semanas 1 e 2 · o pilar mais fraco", "Semanas 3 e 4 · o pilar que destrava o seguinte", "Semanas 5 e 6 · o pilar que te dá um número"]
    for i, n in enumerate(nomes):
        l = 4 + i; s.cell(l, 1, n).font = T(10, True); s.cell(l, 1).alignment = Alignment(wrap_text=True, vertical="center"); s.cell(l, 1).border = borda
        for c in range(2, 6): entrada(s, l, EX_PLANO[i][c - 2] if exemplo else None, "@", c)
        s.row_dimensions[l].height = 42
    dvs = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); s.add_data_validation(dvs); dvs.add("E4:E6")
    s.cell(8, 1, "O que eu vou deixar para depois, de propósito").font = T(10, True, MUSGO)
    entrada(s, 9, EX_DEPOIS if exemplo else None, "@", 1); s.merge_cells("A9:D9"); s.row_dimensions[9].height = 30
    s.cell(10, 1, "Escrever isso evita culpa e evita dispersão.").font = T(9, c="5F5F55", i=True)
    rotulo(s, 12, "Pilares feitos"); calc(s, 12, '=COUNTIF(E4:E6,"Sim")&" de 3"', "@", True)
    rotulo(s, 13, "Pilares repetidos?"); calc(s, 13, '=IF(COUNTA(B4:B6)<3,"Escolha os três pilares",IF(OR(B4=B5,B4=B6,B5=B6),"Escolha três pilares diferentes","OK: três pilares diferentes"))', "@")
    s.merge_cells("B13:C13")

    # ---------- Definições e rotina ----------
    d = wb.create_sheet("Definições e rotina"); d.sheet_view.showGridLines = False
    for col, w in zip("ABC", (30, 70, 50)): d.column_dimensions[col].width = w
    d["A1"] = "Definições dos cinco indicadores e a rotina"; d["A1"].font = T(14, True, MUSGO)
    cabecalho(d, 3, ["Indicador", "Como calcular", "Onde conseguir"])
    onde = ["Calendário das plataformas: noites vendidas ÷ (unidades × dias).", "Relatório de ganhos das plataformas + reservas diretas, sem a taxa de limpeza.", "Folha Única do Mês (Módulo 2) ou Painel do Mês (Marco Zero).", "Painel de avaliações do canal onde você mais vende.", "Receita das reservas diretas ÷ receita de hospedagem."]
    for k, (nome, _, _, defi) in enumerate(IND):
        for c, v in enumerate((nome, defi, onde[k]), 1):
            x = d.cell(4 + k, c, v); x.alignment = Alignment(wrap_text=True, vertical="top"); x.border = borda
        d.row_dimensions[4 + k].height = 44
    rot = [("Toda semana · 30 minutos", "A reunião: os mesmos cinco números, o que saiu do esperado, uma decisão com dono e prazo (Pilar G7)."),
           ("Todo mês", "Lançar o mês no Painel 12 meses e comparar com o mesmo mês do ano anterior (Etapa 09)."),
           ("A cada 12 semanas", "Revisar se as metas continuam fazendo sentido. Não trocar de indicador: o valor vem da série histórica."),
           ("Daqui a 12 meses", "Comparar o mês de chegada com a meta (aba Metas e donos, colunas H e I).")]
    faixa(d, 10, "A ROTINA", 3)
    for i, (a, b) in enumerate(rot):
        d.cell(11 + i, 1, a).font = T(10, True); x = d.cell(11 + i, 2, b); x.alignment = Alignment(wrap_text=True); d.merge_cells(start_row=11 + i, start_column=2, end_row=11 + i, end_column=3)
    d.cell(16, 1, "Fontes Zion: Panorama do Desenvolvimento Hoteleiro (Trilha B, Pilar G7 e plano de seis semanas); Jornada do COMO, Etapas 09 e 10. Material educacional: não é promessa de renda, retorno, ocupação ou resultado.").font = T(9, c="5F5F55", i=True)
    wb.active = 0
    return wb

for exemplo, nome in ((False, "Painel-de-Gestao-Zion-EM-BRANCO.xlsx"), (True, "Painel-de-Gestao-Zion-EXEMPLO.xlsx")):
    montar(exemplo).save(OUT / nome); print("ok", OUT / nome)

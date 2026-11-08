"""Gera a planilha "Folha Única do Mês" (Jornada 2 · Gestão · Módulo 2 · Finanças) em duas versões:
   - Folha-Unica-do-Mes-Zion-EM-BRANCO.xlsx
   - Folha-Unica-do-Mes-Zion-EXEMPLO.xlsx (dados fictícios, identificados como exemplo)
Uso: python3 -I build_planilha.py <pasta-saida>
Molde: producao/jornada2/00-marco-zero/src/build_planilha.py (amarelo = preenche, verde = calculado).
Abas: Comece aqui · Parâmetros · Folha do Mês · Caixa 12 meses · Histórico · Checklist do fechamento."""
import sys, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, DOURADO, PRETO, CREME = "1B2117", "8B714E", "040605", "FEF5F0"
ENTRADA = PatternFill("solid", fgColor="FFF4C7"); CALC = PatternFill("solid", fgColor="E3EEDF"); CAB = PatternFill("solid", fgColor=MUSGO)
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
BRL = 'R$ #,##0.00;[Red]-R$ #,##0.00'
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)
SEM = 4.33  # semanas por mês na Conta da Retirada

def faixa(ws, linha, texto, cols=3):
    ws.merge_cells(start_row=linha, start_column=1, end_row=linha, end_column=cols)
    c = ws.cell(linha, 1, texto); c.font = T(11, True, CREME); c.fill = CAB; c.alignment = Alignment(vertical="center", indent=1); ws.row_dimensions[linha].height = 22
def rotulo(ws, l, texto, ajuda=""):
    a = ws.cell(l, 1, texto); a.font = T(11); a.alignment = Alignment(wrap_text=True, vertical="center")
    if ajuda: h = ws.cell(l, 3, ajuda); h.font = T(9, c="5F5F55", i=True); h.alignment = Alignment(wrap_text=True, vertical="center")
def entrada(ws, l, valor=None, fmt=BRL, col=2):
    c = ws.cell(l, col, valor); c.fill = ENTRADA; c.border = borda; c.number_format = fmt; c.font = T(12, True); return c
def calc(ws, l, formula, fmt=BRL, destaque=False, col=2):
    c = ws.cell(l, col, formula); c.fill = CALC; c.border = borda; c.number_format = fmt; c.font = T(14 if destaque else 11, True, MUSGO if destaque else PRETO); c.alignment = Alignment(wrap_text=True, vertical="center"); return c

# Exemplo didático · dados fictícios (Cabanas do Vale, outubro). Mesmos valores da ficha e do PLANO seção 9.
EX = dict(mes="Outubro de 2026 (exemplo)", dias=31, unidades=4, noites=58, estadias=25,
          receita=16240, limpezaCobrada=1500, outras=980, custoOutras=420, descontos=650,
          limpezaPaga=2000, enxoval=380, amenidades=260, energia=340, cafe=0, quebra=None, outrosVar=0,
          equipe=1800, comuns=620, software=190, contador=300, marketing=150, duodecimos=460, manutencao=250, retirada=None, retiradaZero="Não", outrosFixos=0,
          aluguel=0, taxaGestao=0, marca=0, depreciacao=None,
          saldoInicial=9800, entradas=18470, saidas=14650, reservas=0, aReceber=0)
PAR = dict(comissoes=11, processamento=1.5, imposto=6, cancelamentos=0, quebra=1, reserva=4, horas=20, valorHora=40)

def montar(exemplo):
    wb = Workbook()
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False; ws.column_dimensions["A"].width = 100
    linhas = [
        ("ZION HOSPITALITY BUSINESS · JORNADA 2 · GESTÃO · MÓDULO 2 · FINANÇAS", T(10, True, DOURADO)),
        ("Folha Única do Mês", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para fechar o mês da sua hospedagem em uma folha: do que o hóspede pagou ao que de fato sobrou, separando resultado de caixa, com o custo por noite vendida, o ponto de equilíbrio e os meses de fôlego.", T(11, c="2D352A")),
        ("EXEMPLO DIDÁTICO PREENCHIDO COM DADOS FICTÍCIOS (Cabanas do Vale). Use a versão em branco para os seus números." if exemplo else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("", None),
        ("COMO USAR EM 4 PASSOS (cerca de 25 minutos no primeiro mês, 10 nos seguintes)", T(12, True, MUSGO)),
        ("1. Aba Parâmetros: confira os percentuais de comissão, processamento, imposto, cancelamento, quebra e reserva, e as horas e o valor da hora da sua retirada. Ao lado de cada um está a referência Zion: é referência ajustável, nunca universal. Ajuste com o seu extrato.", None),
        ("2. Aba Folha do Mês: preencha as células amarelas com os números do mês passado, tirados do extrato e das reservas, não da memória. A linha \"Situação dos dados\" precisa mostrar OK para a cascata aparecer.", None),
        ("3. Leia a cascata e os indicadores em verde: receita real, custos variáveis, margem de contribuição, quanto sobrou do mês, o que ficou no caixa, custo por noite vendida, ponto de equilíbrio e meses de fôlego. As leituras em texto usam as réguas da fonte Zion.", None),
        ("4. Copie o mês para as abas Caixa 12 meses e Histórico e marque o Checklist do fechamento. Compare sempre com o mesmo mês do ano anterior.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("O QUE A PLANILHA FAZ E O QUE ELA NÃO FAZ", T(12, True, MUSGO)),
        ("Faz: monta a cascata do mês (receita bruta → deduções → receita real → custos variáveis → margem de contribuição → custos fixos com a sua retirada → quanto sobrou → custos do modelo → reserva de reposição → o que ficou no caixa), os indicadores por noite e o bloco de caixa.", None),
        ("Não faz: não prevê os próximos meses, não conhece os preços da sua região e não substitui o seu contador. \"Quanto sobrou do mês\" é o resultado operacional: não inclui imposto sobre o lucro nem dívida. Reserva de reposição (caixa) e depreciação (contábil) nunca entram na mesma conta: a Folha usa a reserva e mostra a depreciação só como informação.", None),
        ("Convenções: a taxa de limpeza cobrada do hóspede não é receita de hospedagem: ela abate a limpeza paga, e o que sobrar entra em outras receitas. Comissões de canal entram nas deduções, não nos custos variáveis.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Material educativo: não é promessa de renda, retorno ou resultado. A gestão depende da execução de cada hospedagem.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Parâmetros ----------
    pr = wb.create_sheet("Parâmetros"); pr.sheet_view.showGridLines = False
    for col, w in zip("ABC", (46, 16, 70)): pr.column_dimensions[col].width = w
    pr["A1"] = "Parâmetros do mês"; pr["A1"].font = T(18, True, MUSGO)
    pr["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Preencha as células amarelas. A coluna C traz a referência Zion: referência ajustável, nunca universal."; pr["A2"].font = T(10, True, "A0522D" if exemplo else DOURADO)
    faixa(pr, 3, "DEDUÇÕES SOBRE A RECEITA DE HOSPEDAGEM (% da receita bruta de diárias)")
    px = PAR if exemplo else {}
    rotulo(pr, 4, "Comissões dos canais (%)", "Referência Zion: comissões + processamento + imposto somam 15%. Ajuste com o seu extrato de repasses."); entrada(pr, 4, px.get("comissoes"), "0.0")
    rotulo(pr, 5, "Taxa de processamento do pagamento (%)", "Cartão, Pix com taxa, antecipação. Faz parte dos 15% de referência."); entrada(pr, 5, px.get("processamento"), "0.0")
    rotulo(pr, 6, "Imposto sobre a receita (%)", "Guia do mês ou o seu contador. Faz parte dos 15% de referência."); entrada(pr, 6, px.get("imposto"), "0.0")
    rotulo(pr, 7, "Cancelamentos e não comparecimento (%)", "Referência Zion: 2% da receita. Se você tem o valor real em R$, converta para % aqui."); entrada(pr, 7, px.get("cancelamentos"), "0.0")
    faixa(pr, 9, "CUSTO VARIÁVEL E RESERVA")
    rotulo(pr, 10, "Quebra e perda (% da receita de hospedagem)", "Referência Zion: 1%. Usado só quando a quebra em R$ da Folha fica em branco."); entrada(pr, 10, px.get("quebra"), "0.0")
    rotulo(pr, 11, "Reserva de reposição (% da receita real)", "Referência Zion: 3 a 6%, padrão 4%."); entrada(pr, 11, px.get("reserva"), "0.0")
    faixa(pr, 13, "CONTA DA RETIRADA (o que custaria pagar alguém para fazer o que você faz)")
    rotulo(pr, 14, "Horas por semana na operação e na gestão", "Some as horas que você dedica à hospedagem numa semana comum."); entrada(pr, 14, px.get("horas"), "0.0")
    rotulo(pr, 15, "Valor da sua hora (R$)", "O que você pagaria a alguém para fazer o mesmo."); entrada(pr, 15, px.get("valorHora"))
    rotulo(pr, 16, "Retirada do mês (horas × valor × 4,33 semanas)", "Usada na Folha quando a retirada em R$ fica em branco."); calc(pr, 16, f'=IF(OR(B14="",B15=""),"",B14*B15*{SEM})')
    rotulo(pr, 18, "Situação dos parâmetros")
    sp = pr.cell(18, 2, '=IF(COUNTBLANK(B4:B7)+COUNTBLANK(B10:B11)>0,"Preencha os percentuais (use 0 onde não há)",IF(MIN(B4:B7,B10:B11,B14:B15)<0,"Há valor negativo",IF(OR(MAX(B4:B7,B10:B11)>99.9,B4+B5+B6+B7>99.9),"Percentuais precisam ficar entre 0 e 99,9","OK")))')
    sp.font = T(11, True); sp.border = borda; sp.fill = CALC
    pr.conditional_formatting.add("B18", FormulaRule(formula=['$B$18<>"OK"'], fill=PatternFill("solid", fgColor="F8E3DE"), font=Font(color="9B2C1F", bold=True)))
    pr.cell(20, 1, "Os parâmetros Zion vêm da rotina das unidades da Zion e são referência ajustável, nunca universal. O seu extrato manda.").font = T(9, c="5F5F55", i=True)
    dvp = DataValidation(type="decimal", operator="between", formula1="0", formula2="99.9", showErrorMessage=True, errorTitle="Valor inválido", error="Use um percentual de 0 a 99,9."); pr.add_data_validation(dvp); dvp.add("B4:B7"); dvp.add("B10:B11")
    dvn = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, errorTitle="Valor inválido", error="Use um número maior ou igual a zero."); pr.add_data_validation(dvn); dvn.add("B14:B15")

    # ---------- Folha do Mês ----------
    f = wb.create_sheet("Folha do Mês"); f.sheet_view.showGridLines = False
    for col, w in zip("ABC", (58, 22, 64)): f.column_dimensions[col].width = w
    f["A1"] = "Folha Única do Mês"; f["A1"].font = T(18, True, MUSGO)
    f["A2"] = "EXEMPLO DIDÁTICO · dados fictícios (Cabanas do Vale)" if exemplo else "Preencha as células amarelas. Células em verde são calculadas."; f["A2"].font = T(10, True, "A0522D" if exemplo else DOURADO)
    e = EX if exemplo else {}
    faixa(f, 4, "1 · O MÊS")
    rotulo(f, 5, "Mês e ano", "O mês passado inteiro."); entrada(f, 5, e.get("mes"), "@")
    rotulo(f, 6, "Dias do mês", "28, 29, 30 ou 31."); entrada(f, 6, e.get("dias"), "0")
    rotulo(f, 7, "Unidades à venda", "Só as disponíveis para reserva no mês."); entrada(f, 7, e.get("unidades"), "0")
    rotulo(f, 8, "Noites vendidas", "Some as noites de todas as reservas do mês."); entrada(f, 8, e.get("noites"), "0")
    rotulo(f, 9, "Estadias (reservas)", "Reservas com entrada no mês. Se deixar 0, a Folha assume uma estadia por noite."); entrada(f, 9, e.get("estadias"), "0")
    faixa(f, 10, "2 · O QUE ENTROU")
    rotulo(f, 11, "Receita de hospedagem (só diárias, bruta) (R$)", "Antes de descontos, comissões e impostos. Sem a taxa de limpeza."); entrada(f, 11, e.get("receita"))
    rotulo(f, 12, "Taxa de limpeza cobrada do hóspede (R$)", "Repasse: abate a limpeza paga; o excedente vira outra receita."); entrada(f, 12, e.get("limpezaCobrada"))
    rotulo(f, 13, "Outras receitas (R$)", "Café, cestas, experiências, produtos."); entrada(f, 13, e.get("outras"))
    rotulo(f, 14, "Custo das outras receitas (R$)", "O que você gastou para entregar as outras receitas."); entrada(f, 14, e.get("custoOutras"))
    rotulo(f, 15, "Descontos dados (R$)", "Diferença entre o preço cheio e o pago. Comissões, processamento, imposto e cancelamentos vêm dos Parâmetros."); entrada(f, 15, e.get("descontos"))
    faixa(f, 16, "3 · O QUE SAIU COM CADA NOITE (custos variáveis)")
    rotulo(f, 17, "Limpeza paga (R$)"); entrada(f, 17, e.get("limpezaPaga"))
    rotulo(f, 18, "Enxoval e lavanderia (R$)"); entrada(f, 18, e.get("enxoval"))
    rotulo(f, 19, "Amenidades (R$)"); entrada(f, 19, e.get("amenidades"))
    rotulo(f, 20, "Energia, água e gás das unidades (R$)", "A parte que sobe com a ocupação."); entrada(f, 20, e.get("energia"))
    rotulo(f, 21, "Café da manhã (R$)", "Só se incluído na diária."); entrada(f, 21, e.get("cafe"))
    rotulo(f, 22, "Quebra e perda (R$) · opcional", "Em branco = referência dos Parâmetros (1% da receita de hospedagem)."); entrada(f, 22, e.get("quebra"))
    rotulo(f, 23, "Outros custos por noite (R$)"); entrada(f, 23, e.get("outrosVar"))
    faixa(f, 24, "4 · O QUE SAI TODO MÊS (custos fixos operacionais)")
    rotulo(f, 25, "Equipe (R$)"); entrada(f, 25, e.get("equipe"))
    rotulo(f, 26, "Energia, água e internet das áreas comuns (R$)"); entrada(f, 26, e.get("comuns"))
    rotulo(f, 27, "Sistemas e assinaturas (R$)"); entrada(f, 27, e.get("software"))
    rotulo(f, 28, "Contador (R$)"); entrada(f, 28, e.get("contador"))
    rotulo(f, 29, "Marketing fixo (R$)"); entrada(f, 29, e.get("marketing"))
    rotulo(f, 30, "Despesas anuais ÷ 12 (R$)", "Imposto predial, seguro, licenças e décimo terceiro, divididos por 12."); entrada(f, 30, e.get("duodecimos"))
    rotulo(f, 31, "Manutenção contratada (R$)"); entrada(f, 31, e.get("manutencao"))
    rotulo(f, 32, "A sua retirada (R$) · opcional", "Em branco = Conta da Retirada dos Parâmetros (horas × valor × 4,33)."); entrada(f, 32, e.get("retirada"))
    rotulo(f, 33, "Decidi retirada zero por enquanto? (Sim/Não)", "Se Sim, a retirada entra como 0 e não aparece como causa principal."); entrada(f, 33, e.get("retiradaZero", None), "@")
    rotulo(f, 34, "Outros custos fixos (R$)"); entrada(f, 34, e.get("outrosFixos"))
    faixa(f, 35, "5 · CUSTOS DO MODELO E DEPRECIAÇÃO")
    rotulo(f, 36, "Aluguel ou arrendamento (R$)"); entrada(f, 36, e.get("aluguel"))
    rotulo(f, 37, "Taxa de gestão ou administração (R$)"); entrada(f, 37, e.get("taxaGestao"))
    rotulo(f, 38, "Marca, franquia ou rede (R$)"); entrada(f, 38, e.get("marca"))
    rotulo(f, 39, "Depreciação (R$) · opcional, só informativa", "Nunca entra junto com a reserva de reposição."); entrada(f, 39, e.get("depreciacao"))
    faixa(f, 40, "6 · O CAIXA DO MÊS (extrato da conta da hospedagem)")
    rotulo(f, 41, "Saldo no dia 1 (R$)"); entrada(f, 41, e.get("saldoInicial"))
    rotulo(f, 42, "Tudo que entrou na conta (R$)", "Já líquido do que a plataforma reteve."); entrada(f, 42, e.get("entradas"))
    rotulo(f, 43, "Tudo que saiu da conta (R$)"); entrada(f, 43, e.get("saidas"))
    rotulo(f, 44, "Reservas já guardadas (R$)", "Baixa, reposição, manutenção e anuais, somadas."); entrada(f, 44, e.get("reservas"))
    rotulo(f, 45, "A receber (R$) · opcional", "Repasses ainda não caídos."); entrada(f, 45, e.get("aReceber"))

    OBRIG = "B6:B9,B11:B15,B17:B21,B23,B25:B31,B34,B36:B38,B41:B44"
    TODOS = OBRIG + ",B22,B32,B39,B45"
    P = "Parâmetros!"
    faixa(f, 46, "7 · SITUAÇÃO DOS DADOS")
    rotulo(f, 47, "Situação dos dados", "Precisa mostrar OK para a cascata aparecer.")
    cs = f.cell(47, 2, f'=IF({P}$B$18<>"OK","Confira a aba Parâmetros",IF(COUNTBLANK(B6:B9)+COUNTBLANK(B11:B15)+COUNTBLANK(B17:B21)+COUNTBLANK(B23)+COUNTBLANK(B25:B31)+COUNTBLANK(B34)+COUNTBLANK(B36:B38)+COUNTBLANK(B41:B44)>0,"Preencha todas as células amarelas obrigatórias (use 0 onde não houve)",IF(MIN({TODOS})<0,"Há valor negativo",IF(OR(B6<28,B6>31),"Dias do mês: use 28 a 31",IF(B7<1,"Unidades: pelo menos 1",IF(B8>B7*B6,"Noites vendidas passam das noites disponíveis",IF(B15+B11*({P}B4+{P}B5+{P}B6+{P}B7)/100>B11,"Deduções passam da receita de hospedagem: confira descontos e percentuais","OK")))))))')
    cs.font = T(11, True); cs.border = borda; cs.fill = CALC; cs.alignment = Alignment(wrap_text=True)
    f.conditional_formatting.add("B47", FormulaRule(formula=['$B$47<>"OK"'], fill=PatternFill("solid", fgColor="F8E3DE"), font=Font(color="9B2C1F", bold=True)))
    OK = lambda s: f'=IF($B$47="OK",{s},"")'
    NC = '"não calculável"'
    faixa(f, 48, "8 · A CASCATA DO MÊS (do que o hóspede pagou ao que de fato sobrou)")
    rotulo(f, 49, "Noites disponíveis", "Unidades × dias."); calc(f, 49, OK("B7*B6"), "0")
    rotulo(f, 50, "Ocupação", "Noites vendidas ÷ disponíveis."); calc(f, 50, OK("IF(B49>0,B8/B49,0)"), "0.0%")
    rotulo(f, 51, "Estadias consideradas", "Se estadias = 0, assume uma por noite."); calc(f, 51, OK("IF(B9>0,B9,B8)"), "0")
    rotulo(f, 52, "Deduções", "Descontos + receita × (comissões + processamento + imposto + cancelamentos)."); calc(f, 52, OK(f"B15+B11*({P}B4+{P}B5+{P}B6+{P}B7)/100"))
    rotulo(f, 53, "RECEITA REAL DE HOSPEDAGEM", "Receita bruta − deduções."); calc(f, 53, OK("B11-B52"), BRL, True)
    rotulo(f, 54, "Limpeza líquida", "Limpeza paga − taxa cobrada, nunca abaixo de 0."); calc(f, 54, OK("MAX(0,B17-B12)"))
    rotulo(f, 55, "Excedente da taxa de limpeza", "Quando cobra mais do que paga: vira outra receita."); calc(f, 55, OK("MAX(0,B12-B17)"))
    rotulo(f, 56, "Outras receitas (com o excedente)"); calc(f, 56, OK("B13+B55"))
    rotulo(f, 57, "Faturamento (receita bruta total)", "Hospedagem + outras, sem a taxa de limpeza repassada."); calc(f, 57, OK("B11+B56"))
    rotulo(f, 58, "RECEITA REAL TOTAL"); calc(f, 58, OK("B53+B56"), BRL, True)
    rotulo(f, 59, "Quebra e perda considerada", "R$ informado ou referência dos Parâmetros."); calc(f, 59, OK(f'IF(B22="",B11*{P}B10/100,B22)'))
    rotulo(f, 60, "Custos variáveis", "Limpeza líquida + enxoval + amenidades + energia + café + quebra + outros + custo das outras receitas."); calc(f, 60, OK("B54+B18+B19+B20+B21+B59+B23+B14"))
    rotulo(f, 61, "MARGEM DE CONTRIBUIÇÃO", "Receita real total − custos variáveis."); calc(f, 61, OK("B58-B60"), BRL, True)
    rotulo(f, 62, "Retirada considerada", "0 se decidida; R$ informado; ou Conta da Retirada dos Parâmetros."); calc(f, 62, OK(f'IF(B33="Sim",0,IF(B32="",IF({P}B16="",0,{P}B16),B32))'))
    rotulo(f, 63, "Custos fixos operacionais (com a retirada)"); calc(f, 63, OK("B25+B26+B27+B28+B29+B30+B31+B62+B34"))
    rotulo(f, 64, "QUANTO SOBROU DO MÊS (resultado operacional)", "Margem de contribuição − custos fixos."); calc(f, 64, OK("B61-B63"), BRL, True)
    rotulo(f, 65, "Custos do modelo", "Aluguel + gestão + marca."); calc(f, 65, OK("B36+B37+B38"))
    rotulo(f, 66, "Resultado antes de juros, impostos sobre o lucro e depreciação"); calc(f, 66, OK("B64-B65"))
    rotulo(f, 67, "Reserva de reposição", "% dos Parâmetros × receita real total."); calc(f, 67, OK(f"B58*{P}B11/100"))
    rotulo(f, 68, "O QUE FICOU NO CAIXA PARA O NEGÓCIO (geração de caixa)", "Antes de impostos sobre o lucro e dívida."); calc(f, 68, OK("B66-B67"), BRL, True)
    rotulo(f, 69, "Resultado contábil indicativo", "Só se a depreciação foi informada; nunca somado à reserva."); calc(f, 69, OK('IF(B39="","",B66-B39)'))
    faixa(f, 70, "9 · INDICADORES")
    rotulo(f, 71, "Diária média bruta", "Receita de hospedagem ÷ noites."); calc(f, 71, OK(f"IF(B8>0,B11/B8,{NC})"))
    rotulo(f, 72, "Diária média real", "Receita real de hospedagem ÷ noites."); calc(f, 72, OK(f"IF(B8>0,B53/B8,{NC})"))
    rotulo(f, 73, "Taxa de dedução real", "Deduções ÷ receita de hospedagem. Faixa da fonte: 15 a 25%."); calc(f, 73, OK(f"IF(B11>0,B52/B11,{NC})"), "0.0%")
    rotulo(f, 74, "Custo variável por noite", "(Variáveis − custo das outras receitas) ÷ noites."); calc(f, 74, OK(f"IF(B8>0,(B60-B14)/B8,{NC})"))
    rotulo(f, 75, "Custo fixo total do mês", "Fixos operacionais + custos do modelo."); calc(f, 75, OK("B63+B65"))
    rotulo(f, 76, "CUSTO POR NOITE VENDIDA", "Variável por noite + fixo total ÷ noites."); calc(f, 76, OK(f"IF(B8>0,B74+B75/B8,{NC})"), BRL, True)
    rotulo(f, 77, "Margem por noite", "Diária média real − custo variável por noite."); calc(f, 77, OK(f"IF(B8>0,B72-B74,{NC})"))
    rotulo(f, 78, "Ponto de equilíbrio (noites)", "(Fixo total − margem das outras receitas) ÷ margem por noite."); calc(f, 78, OK(f'IF(B8>0,IF(B77>0,MAX(0,(B75-(B56-B14))/B77),"não fecha"),{NC})'), "0.0")
    rotulo(f, 79, "Ocupação de equilíbrio", "Ponto de equilíbrio ÷ noites disponíveis."); calc(f, 79, OK('IF(ISNUMBER(B78),IF(B49>0,B78/B49,0),B78)'), "0.0%")
    rotulo(f, 80, "Quanto sobrou, em % do faturamento"); calc(f, 80, OK(f"IF(B57>0,B64/B57,{NC})"), "0.0%")
    rotulo(f, 81, "Receita por noite disponível"); calc(f, 81, OK("IF(B49>0,B11/B49,0)"))
    rotulo(f, 82, "Saldo no fim do mês", "Saldo inicial + entradas − saídas."); calc(f, 82, OK("B41+B42-B43"))
    rotulo(f, 83, "MESES DE FÔLEGO", "(Saldo final + reservas) ÷ custo fixo total."); calc(f, 83, OK(f"IF(B75>0,(B82+B44)/B75,{NC})"), "0.0", True)
    faixa(f, 84, "10 · LEITURAS (réguas da fonte Zion, sem nota)")
    rotulo(f, 85, "Cada noite vendida"); calc(f, 85, OK('IF(B8=0,"Sem noite vendida: cada real que saiu é prejuízo",IF(B72>=B76,"Cada noite vendida paga tudo e sobra",IF(B72>=B74,"Cada noite paga o variável e ajuda no fixo, mas o mês não fecha","Cada noite vendida consome valor: diária abaixo do custo variável")))'), "@")
    rotulo(f, 86, "Ocupação de equilíbrio", "Acima de 70% alerta; 65 a 70 no limite; 45 a 65 saudável; abaixo de 45 folgada."); calc(f, 86, OK('IF(NOT(ISNUMBER(B79)),B79,IF(B79>0.7,"Alerta: correção estrutural (diária, variável ou fixo)",IF(B79>0.65,"No limite",IF(B79>=0.45,"Saudável","Folgada"))))'), "@")
    rotulo(f, 87, "Meses de fôlego", "Abaixo de 2 risco; 2 a 4 apertado; 4 a 6 confortável; acima de 6 muito confortável."); calc(f, 87, OK('IF(NOT(ISNUMBER(B83)),B83,IF(B83<2,"Zona de risco",IF(B83<4,"Apertado",IF(B83<=6,"Confortável","Muito confortável: confira se há dinheiro parado"))))'), "@")
    rotulo(f, 88, "Margem do mês", "Régua anual usada como referência indicativa: acima de 30% boa; 20 a 30 viável; 10 a 20 apertada; abaixo de 10 não fecha."); calc(f, 88, OK('IF(NOT(ISNUMBER(B80)),B80,IF(B80>0.3,"Boa",IF(B80>=0.2,"Viável",IF(B80>=0.1,"Apertada","Não fecha"))))'), "@")
    rotulo(f, 89, "Caixa × resultado"); calc(f, 89, OK('IF(AND(B82>B41,B64<0),"Caixa bom e resultado ruim: alta temporada ou repasse que ainda vai sair",IF(AND(B82<=B41,B64>=0),"Caixa ruim e resultado bom: investimento ou pagamento concentrado",IF(AND(B82<=B41,B64<0),"Os dois alertas ao mesmo tempo","Caixa e resultado andam juntos")))'), "@")
    rotulo(f, 90, "Causa principal (ordem de correção da fonte)", "Despesas anuais → reserva → retirada → diária → variável → deduções → ocupação de equilíbrio.")
    calc(f, 90, OK('IF(B30=0,"Despesas anuais sem provisão",IF(B44=0,"Sem reserva para a baixa",IF(AND(B62=0,B33<>"Sim"),"Retirada não lançada",IF(AND(ISNUMBER(B72),B72<B76),"Diária abaixo do custo real",IF(AND(ISNUMBER(B74),B74>=0.5*B72),"Custo variável mal medido ou alto",IF(AND(ISNUMBER(B73),B73>0.25),"Deduções acima da faixa da fonte (15 a 25%)",IF(AND(ISNUMBER(B79),B79>0.7),"Modelo exige ocupação que o destino não entrega","Mês dentro das réguas: compare com o mesmo mês do ano anterior")))))))'), "@")
    f.cell(92, 1, "Os números descrevem o mês que passou. Não são previsão nem promessa para o mês seguinte. Parâmetros Zion: referência ajustável, nunca universal.").font = T(9, c="5F5F55", i=True)
    dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, errorTitle="Valor inválido", error="Use um número maior ou igual a zero.")
    f.add_data_validation(dv)
    for rng in TODOS.split(","): dv.add(rng)
    dvs = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); f.add_data_validation(dvs); dvs.add("B33")

    # ---------- Caixa 12 meses ----------
    c12 = wb.create_sheet("Caixa 12 meses"); c12.sheet_view.showGridLines = False; c12.freeze_panes = "A4"
    c12["A1"] = "Caixa 12 meses · uma linha por mês. Amarelo: preencha; o saldo inicial dos meses seguintes é puxado automaticamente." + ("  ·  EXEMPLO FICTÍCIO" if exemplo else ""); c12["A1"].font = T(12, True, MUSGO)
    c12["A2"] = "Fôlego = (saldo final + reservas) ÷ custo fixo total do mês (copie o custo fixo total da Folha, linha 75). Abaixo de 2 risco; 4 a 6 confortável."; c12["A2"].font = T(9, c="5F5F55", i=True)
    cab = ["Mês", "Saldo no dia 1 (R$)", "Entradas (R$)", "Saídas (R$)", "Reservas guardadas (R$)", "Custo fixo total do mês (R$)", "Saldo final (R$)", "Meses de fôlego", "Leitura"]
    for i, (t, w) in enumerate(zip(cab, [18, 18, 16, 16, 18, 20, 18, 14, 22]), 1):
        x = c12.cell(3, i, t); x.font = T(10, True, CREME); x.fill = CAB; x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); x.border = borda
        c12.column_dimensions[x.column_letter].width = w
    c12.row_dimensions[3].height = 34
    for l in range(4, 16):
        for col in (1, 3, 4, 5, 6): x = c12.cell(l, col); x.fill = ENTRADA; x.border = borda; x.number_format = BRL if col > 1 else "@"
        if l == 4: entrada(c12, l, None, BRL, 2)
        else: calc(c12, l, f'=IF(G{l-1}="","",G{l-1})', BRL, False, 2)
        calc(c12, l, f'=IF(OR(B{l}="",C{l}="",D{l}=""),"",B{l}+C{l}-D{l})', BRL, False, 7)
        calc(c12, l, f'=IF(G{l}="","",IF(F{l}>0,(G{l}+IF(E{l}="",0,E{l}))/F{l},"não calculável"))', "0.0", False, 8)
        calc(c12, l, f'=IF(NOT(ISNUMBER(H{l})),IF(H{l}="","",H{l}),IF(H{l}<2,"Zona de risco",IF(H{l}<4,"Apertado",IF(H{l}<=6,"Confortável","Muito confortável"))))', "@", False, 9)
    if exemplo:
        for col, v in zip(range(1, 7), ("Outubro (exemplo)", 9800, 18470, 14650, 0, 7234)): c12.cell(4, col, v)
        for col, v in zip((1, 3, 4, 5, 6), ("Novembro (exemplo)", 15200, 13900, 1500, 7234)): c12.cell(5, col, v)
    dvc = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, errorTitle="Valor inválido", error="Use um número maior ou igual a zero."); c12.add_data_validation(dvc); dvc.add("B4"); dvc.add("C4:F15")

    # ---------- Histórico ----------
    h = wb.create_sheet("Histórico"); h.sheet_view.showGridLines = False; h.freeze_panes = "A3"
    h["A1"] = "Histórico · copie os números da Folha, uma linha por mês (amarelo). Compare sempre com o mesmo mês do ano anterior." + ("  ·  EXEMPLO FICTÍCIO" if exemplo else ""); h["A1"].font = T(12, True, MUSGO)
    cab = ["Mês", "Receita real total (R$)", "Quanto sobrou (R$)", "Ocupação", "Diária média real (R$)", "Custo por noite vendida (R$)", "Meses de fôlego", "Causa principal"]
    for i, (t, w) in enumerate(zip(cab, [18, 20, 18, 12, 18, 20, 14, 36]), 1):
        x = h.cell(2, i, t); x.font = T(10, True, CREME); x.fill = CAB; x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); x.border = borda
        h.column_dimensions[x.column_letter].width = w
    h.row_dimensions[2].height = 34
    for l in range(3, 27):
        for col in range(1, 9):
            x = h.cell(l, col); x.fill = ENTRADA; x.border = borda
            x.number_format = {2: BRL, 3: BRL, 4: "0.0%", 5: BRL, 6: BRL, 7: "0.0"}.get(col, "@")
    if exemplo:
        for col, v in zip(range(1, 9), ("Outubro (exemplo)", 13565.6, 4269.2, 58 / 124, 216.99, 153.03, 1.9, "Sem reserva para a baixa")): h.cell(3, col, v)

    # ---------- Checklist do fechamento ----------
    ck = wb.create_sheet("Checklist do fechamento"); ck.sheet_view.showGridLines = False
    for col, w in zip("ABC", (6, 80, 12)): ck.column_dimensions[col].width = w
    ck["A1"] = "Checklist do fechamento do mês · marque Sim ou Não (amarelo)"; ck["A1"].font = T(14, True, MUSGO)
    itens = ["O extrato da conta da hospedagem do mês inteiro foi baixado",
             "Os repasses de cada canal foram conciliados com as reservas do mês",
             "A taxa de limpeza cobrada foi separada da receita de hospedagem",
             "Descontos, comissões, processamento, imposto e cancelamentos foram lançados como deduções",
             "Cada custo variável tem nota ou recibo",
             "As despesas anuais foram divididas por 12 e lançadas",
             "A retirada foi lançada pela Conta da Retirada (ou a decisão de retirada zero está escrita)",
             "A reserva de reposição foi transferida para a conta de reservas",
             "A Folha foi copiada para o Histórico e para o Caixa 12 meses",
             "O mês foi comparado com o mesmo mês do ano anterior e uma prioridade foi escolhida"]
    for i, t in enumerate(["Nº", "Item", "Feito?"], 1):
        x = ck.cell(3, i, t); x.font = T(10, True, CREME); x.fill = CAB; x.border = borda
    for i, t in enumerate(itens):
        ck.cell(4 + i, 1, i + 1).font = T(10, True); ck.cell(4 + i, 2, t).alignment = Alignment(wrap_text=True)
        x = ck.cell(4 + i, 3, ("Sim" if i < 7 else "Não") if exemplo else None); x.fill = ENTRADA; x.border = borda
    dvk = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); ck.add_data_validation(dvk); dvk.add(f"C4:C{3 + len(itens)}")
    ck.cell(15, 2, "Itens feitos:"); x = ck.cell(15, 3, f'=COUNTIF(C4:C{3 + len(itens)},"Sim")'); x.fill = CALC; x.border = borda; x.font = T(12, True, MUSGO)
    ck.cell(16, 2, f'=IF(C15={len(itens)},"Fechamento completo: 10 de 10","Faltam "&({len(itens)}-C15)&" de {len(itens)} itens")').font = T(10, True, MUSGO)
    ck.cell(18, 2, "Rotina da fonte: 5 minutos por semana, 10 minutos por mês.").font = T(9, c="5F5F55", i=True)
    wb.active = 0
    return wb

for exemplo, nome in ((False, "Folha-Unica-do-Mes-Zion-EM-BRANCO.xlsx"), (True, "Folha-Unica-do-Mes-Zion-EXEMPLO.xlsx")):
    montar(exemplo).save(OUT / nome); print("ok", OUT / nome)

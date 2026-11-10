"""Gera a planilha "Tarefas, Escala e Alçadas" (Jornada 2 · Gestão · Módulo 5 · Pessoas) em duas versões:
   - Tarefas-Escala-e-Alcadas-Zion-EM-BRANCO.xlsx
   - Tarefas-Escala-e-Alcadas-Zion-EXEMPLO.xlsx (dados fictícios, identificados como exemplo)
Uso: python3 -I build_planilha.py <pasta-saida>
Molde: producao/jornada2/02-financas/src/build_planilha.py (amarelo = preenche, verde = calculado).
Abas: Comece aqui · Tarefas · Alçadas · Escala · Plano 4 semanas · Painel por exceção."""
import sys, pathlib, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, DOURADO, PRETO, CREME = "1B2117", "8B714E", "040605", "FEF5F0"
ENTRADA = PatternFill("solid", fgColor="FFF4C7"); CALC = PatternFill("solid", fgColor="E3EEDF"); CAB = PatternFill("solid", fgColor=MUSGO)
ALERTA = PatternFill("solid", fgColor="F8E3DE")
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
BRL = 'R$ #,##0.00;[Red]-R$ #,##0.00'; DATA = "DD/MM/YYYY"
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)
NOTA = "Zion Hospitality Business · Material educativo: não é promessa de renda, retorno ou resultado. A gestão depende da execução de cada hospedagem."

def cabecalho(ws, linha, titulos, larguras=None):
    for i, t in enumerate(titulos, 1):
        x = ws.cell(linha, i, t); x.font = T(10, True, CREME); x.fill = CAB; x.border = borda; x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        if larguras: ws.column_dimensions[x.column_letter].width = larguras[i - 1]
    ws.row_dimensions[linha].height = 34
def ent(ws, l, c, v=None, fmt="@"):
    x = ws.cell(l, c, v); x.fill = ENTRADA; x.border = borda; x.number_format = fmt; x.font = T(11); x.alignment = Alignment(wrap_text=True, vertical="center"); return x
def calc(ws, l, c, f, fmt="@", destaque=False):
    x = ws.cell(l, c, f); x.fill = CALC; x.border = borda; x.number_format = fmt; x.font = T(13 if destaque else 11, True, MUSGO if destaque else PRETO); x.alignment = Alignment(wrap_text=True, vertical="center"); return x
def fixo(ws, l, c, v, b=False):
    x = ws.cell(l, c, v); x.font = T(10, b); x.border = borda; x.alignment = Alignment(wrap_text=True, vertical="center"); return x
def titulo(ws, t, sub, exemplo):
    ws["A1"] = t; ws["A1"].font = T(18, True, MUSGO)
    ws["A2"] = "EXEMPLO DIDÁTICO · dados fictícios (Cabanas do Vale)" if exemplo else sub; ws["A2"].font = T(10, True, "A0522D" if exemplo else DOURADO)
def alerta(ws, cel, ok_txt):
    ws.conditional_formatting.add(cel, FormulaRule(formula=[f'LEFT({cel.replace(":", "")},{len(ok_txt)})<>"{ok_txt}"'], fill=ALERTA, font=Font(color="9B2C1F", bold=True)))

# Atividades (mesma ordem e setores da ficha; julgamento sugerido pela fonte, ajustável)
ATIV = [("Limpeza e preparação da unidade", "Governança e limpeza", "Baixo", "Diarista", 0),
        ("Check-in e check-out", "Hospitalidade e experiência", "Baixo", "Eu", 5),
        ("Resposta a mensagem dos hóspedes", "Hospitalidade e experiência", "Médio", "Eu", 6),
        ("Manutenção e ronda técnica", "Manutenção", "Médio", "Auxiliar de manutenção", 1),
        ("Compras, estoque e fornecedores", "Gerencial e administrativo", "Alto", "Eu", 2),
        ("Financeiro e administrativo", "Gerencial e administrativo", "Alto", "Eu", 2),
        ("Preço, calendário e canais", "Comercial e reservas", "Alto", "Eu", 2),
        ("Pedido e resposta de avaliações", "Cultura e marca", "Médio", "Eu", 2)]
SIT = [("Reserva de última hora", "Quem estiver no plantão", "Aceita até 2 horas antes do check-in, se a unidade estiver pronta e houver alguém para receber.", "Depois disso, ou sem ninguém para receber.", None),
       ("Cortesia e compensação", "Diarista", "Problema reconhecido na unidade: oferece cortesia de até 15% da diária.", "Acima disso.", 42),
       ("Cancelamento e reembolso fora da política", "Eu", "Motivo de saúde com comprovação: devolve até 50%.", "Qualquer outro motivo.", None),
       ("Manutenção", "Auxiliar de manutenção", "Resolve na hora o que não para a unidade.", "O que para a unidade: avisa a dona na hora.", 100),
       ("Compra fora do previsto", "Diarista", "Item de reposição da lista padrão: compra sem perguntar.", "Item fora da lista.", 100),
       ("Hóspede com comportamento problemático", "Quem estiver no plantão", "Faz a advertência verbal e registra.", "Encerrar a estadia, só com a dona.", None),
       ("Erro de calendário e realocação", "Eu", None, None, None)]
FUNCOES = ["Limpeza e preparação", "Check-in e check-out", "Resposta a mensagem", "Manutenção e ronda"]
ESCALA_EX = [["Diarista"] * 6 + ["Eu"], ["Eu"] * 7, ["Eu"] * 7, ["Auxiliar de manutenção", "Eu", "Auxiliar de manutenção", "Eu", "Auxiliar de manutenção", None, None]]
PESSOAS_EX = [("Eu", "Diarista (mensagens com modelos, depois do plano)"), ("Diarista", "Eu"), ("Auxiliar de manutenção", "Eu")]
SEMANAS = [("1 · Sombra", "A pessoa acompanha você executando, com o procedimento impresso na mão, e marca o que não estava escrito. Nenhuma execução sozinha.", "20 minutos no fim da semana", "Procedimento corrigido com o que faltava"),
           ("2 · Execução acompanhada", "A pessoa executa e você observa sem interferir. Corrija depois, não durante. Confira o resultado contra a foto do padrão, todo dia.", "20 minutos por dia", "O resultado bate com a foto do padrão"),
           ("3 · Sozinha, com conferência", "A pessoa executa sozinha e você confere o resultado, não o processo. Entram a tabela de critérios e a alçada inicial.", "20 minutos por dia", "Dúvidas caindo, critérios sendo usados"),
           ("4 · Autonomia com alçada", "A pessoa executa e decide dentro da alçada. Você olha os seis indicadores do painel.", "Duas vezes na semana", "Padrão mantido e decisões razoáveis")]
INICIO_EX = dt.date(2026, 11, 16)
# Painel por exceção, exemplo: semana, nota, ocupação, projetada, resposta (min), ocorrências, dentro, fora, segurança, gasto, previsto
PAINEL_EX = [(dt.date(2026, 11, 16), 4.9, 0.45, 0.50, 25, 1, 2, 0, 0, 1200, 1200),
             (dt.date(2026, 11, 23), 4.8, 0.52, 0.50, 30, 0, 3, 0, 0, 1350, 1200),
             (dt.date(2026, 11, 30), 4.6, 0.48, 0.50, 20, 2, 1, 0, 0, 1100, 1200),
             (dt.date(2026, 12, 7), 4.9, 0.55, 0.55, 22, 0, 2, 0, 0, 1250, 1200)]

def montar(exemplo):
    wb = Workbook()
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False; ws.column_dimensions["A"].width = 100
    linhas = [
        ("ZION HOSPITALITY BUSINESS · JORNADA 2 · GESTÃO · MÓDULO 5 · PESSOAS", T(10, True, DOURADO)),
        ("Tarefas, Escala e Alçadas", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para tirar a operação da sua cabeça: quem faz o quê, até quanto cada pessoa decide sem consultar você, quem está escalado em cada dia, o plano de quatro semanas para entregar a primeira atividade e o painel para acompanhar de fora.", T(11, c="2D352A")),
        ("EXEMPLO DIDÁTICO PREENCHIDO COM DADOS FICTÍCIOS (Cabanas do Vale, 4 unidades). Use a versão em branco para a sua hospedagem." if exemplo else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("", None),
        ("COMO USAR EM 5 PASSOS (cerca de 30 minutos na primeira vez, 15 por semana depois)", T(12, True, MUSGO)),
        ("1. Aba Tarefas: para cada atividade, quem faz hoje (escreva Eu quando for você), as horas suas por semana e o julgamento que ela exige. A planilha soma as horas e mostra a primeira atividade a delegar: a que tem mais horas e menos julgamento.", None),
        ("2. Aba Alçadas: para cada situação que foge do padrão, quem decide, quando decide sozinho, quando consulta e até quanto em reais. Defina a alçada inicial e a do segundo mês: comece baixo e suba com a confiança.", None),
        ("3. Aba Escala: quem está em cada função, em cada dia da semana, e quem substitui se a pessoa faltar. A planilha aponta os turnos sem ninguém.", None),
        ("4. Aba Plano 4 semanas: a atividade, quem assume e a data de início. As datas das quatro semanas e da avaliação saem sozinhas. Marque o sinal de cada semana e, na avaliação, as três perguntas.", None),
        ("5. Aba Painel por exceção: a nota mínima e o percentual de gasto. Toda semana, uma linha com os seis indicadores: a planilha diz se é exceção (contato na hora) ou relatório semanal.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("DE ONDE VEM", T(12, True, MUSGO)),
        ("Jornada do COMO, Etapa 10 (inventário, quatro dependências, critérios e alçadas, primeira contratação, plano de quatro semanas, painel por exceção); Panorama do Desenvolvimento Hoteleiro, Trilha B, pilar G7 (alçadas e governança); Bíblia Operacional Zion (seis setores e escala da semana).", None),
        ("O que a planilha não faz: não decide por você quem contratar, não calcula salário nem encargos e não substitui orientação trabalhista. Para contratos e encargos, consulte o seu contador.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice.", T(10, c="5F5F55", i=True)),
        (NOTA, T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Tarefas ----------
    t = wb.create_sheet("Tarefas"); t.sheet_view.showGridLines = False
    titulo(t, "Quem faz o quê", "Preencha as células amarelas. Escreva Eu quando a atividade for sua.", exemplo)
    cabecalho(t, 4, ["Atividade", "Setor", "Quem faz hoje", "Horas suas por semana", "Julgamento (Baixo, Médio, Alto)", "Entra na primeira contratação?", "Prioridade (cálculo)", "É você? (1 = sim)"], [36, 26, 26, 14, 16, 30, 12, 10])
    for k, (nome, setor, julg, resp, horas) in enumerate(ATIV):
        l = 5 + k
        fixo(t, l, 1, nome, True); fixo(t, l, 2, setor)
        ent(t, l, 3, resp if exemplo else None); ent(t, l, 4, horas if exemplo else None, "0.0"); ent(t, l, 5, julg)
        calc(t, l, 6, f'=IF(E{l}="","",IF(E{l}="Baixo","Sim",IF(E{l}="Médio","Parcial, com modelos","Não, fica com você por mais tempo")))')
        calc(t, l, 7, f'=IF(AND(N(D{l})>0,E{l}<>"Alto",E{l}<>""),IF(E{l}="Baixo",1000,0)+D{l},-1)', "0.0")
        calc(t, l, 8, f'=IF(OR(LOWER(TRIM(C{l}))="eu",LOWER(TRIM(C{l}))="eu mesma",LOWER(TRIM(C{l}))="eu mesmo"),1,0)', "0")
    fixo(t, 14, 1, "Situação dos dados", True)
    calc(t, 14, 2, '=IF(COUNTBLANK(C5:C12)>0,"Preencha quem faz hoje em todas as atividades (escreva Eu se for você)",IF(COUNTIF(D5:D12,"<0")>0,"Há hora negativa",IF(MAX(D5:D12)>100,"Mais de 100 horas numa atividade não cabe numa semana",IF(COUNTBLANK(E5:E12)>0,"Marque o julgamento de todas as atividades","OK"))))')
    t.merge_cells("B14:F14"); alerta(t, "B14", "OK")
    rot = [(16, "Horas suas por semana (total)", "=SUM(D5:D12)", "0.0"),
           (17, "Horas que seguem roteiro (Baixo)", '=SUMIF(E5:E12,"Baixo",D5:D12)', "0.0"),
           (18, "Horas que saem com modelos prontos (Médio)", '=SUMIF(E5:E12,"Médio",D5:D12)', "0.0"),
           (19, "Horas que exigem decisão e ficam com você (Alto)", '=SUMIF(E5:E12,"Alto",D5:D12)', "0.0"),
           (20, "Primeira atividade a delegar (mais horas, menos julgamento)", '=IF(B14<>"OK","",IF(MAX(G5:G12)<0,"Nenhuma: comece pelos critérios e alçadas",INDEX(A5:A12,MATCH(MAX(G5:G12),G5:G12,0))))', "@"),
           (21, "Atividades que são só suas", "=SUM(H5:H12)", "0"),
           (22, "Setores que dependem só de você (de 6)", "=H5+H6*H7+H8+H9*H10+H11+H12", "0")]
    for l, r, f, fmt in rot:
        fixo(t, l, 1, r, True); calc(t, l, 2, f, fmt, l in (16, 20))
    t.merge_cells("B20:F20")
    t.cell(24, 1, "Regra da fonte (Jornada do COMO, Etapa 10): contrate pela atividade que mais consome o seu tempo com menor exigência de julgamento. Preço, compra, negociação e relação com fornecedor ficam com você por mais tempo.").font = T(9, c="5F5F55", i=True)
    t.cell(25, 1, "Setores da Bíblia Operacional Zion: hospitalidade e experiência, governança e limpeza, manutenção, gerencial e administrativo, comercial e reservas, cultura e marca.").font = T(9, c="5F5F55", i=True)
    dvj = DataValidation(type="list", formula1='"Baixo,Médio,Alto"', allow_blank=True); t.add_data_validation(dvj); dvj.add("E5:E12")
    dvh = DataValidation(type="decimal", operator="between", formula1="0", formula2="100", showErrorMessage=True, errorTitle="Valor inválido", error="Use de 0 a 100 horas."); t.add_data_validation(dvh); dvh.add("D5:D12")

    # ---------- Alçadas ----------
    a = wb.create_sheet("Alçadas"); a.sheet_view.showGridLines = False
    titulo(a, "Tabela de critérios e alçadas", "Procedimento permite executar; critério permite resolver. Preencha as células amarelas.", exemplo)
    cabecalho(a, 4, ["Situação", "Quem decide", "Decide sozinho quando", "Consulta quando", "Alçada (R$)", "Revisar em", "Regra escrita?"], [30, 22, 44, 34, 13, 13, 12])
    for k, (sit, quem, sozinho, consulta, alc) in enumerate(SIT):
        l = 5 + k
        fixo(a, l, 1, sit, True)
        ent(a, l, 2, quem if exemplo else None); ent(a, l, 3, sozinho if exemplo else None); ent(a, l, 4, consulta if exemplo else None)
        ent(a, l, 5, alc if exemplo else None, BRL); ent(a, l, 6, dt.date(2027, 5, 16) if exemplo and sozinho else None, DATA)
        calc(a, l, 7, f'=IF(LEN(TRIM(C{l}))>=10,"Sim","Falta")')
        a.row_dimensions[l].height = 44
    fixo(a, 13, 1, "Alçada inicial, primeira semana (R$)", True); ent(a, 13, 2, 100 if exemplo else None, BRL)
    fixo(a, 14, 1, "Alçada no segundo mês (R$)", True); ent(a, 14, 2, 300 if exemplo else None, BRL)
    fixo(a, 15, 1, "Situações com regra escrita (de 7)", True); calc(a, 15, 2, '=COUNTIF(G5:G11,"Sim")', "0", True)
    fixo(a, 16, 1, "Situação", True)
    calc(a, 16, 2, '=IF(B13="","Defina a alçada inicial em reais",IF(N(B13)<=0,"A alçada inicial precisa ser maior que zero",IF(COUNTIF(E5:E11,"<0")>0,"Há alçada negativa",IF(AND(B14<>"",N(B14)<N(B13)),"Atenção: a alçada do segundo mês está abaixo da inicial",IF(B15<5,"Escreva a regra de pelo menos 5 das 7 situações","OK")))))')
    a.merge_cells("B16:E16"); alerta(a, "B16", "OK")
    a.cell(18, 1, "Comece baixo e suba conforme a confiança (a fonte sugere cem reais na primeira semana e trezentos no segundo mês). Registre as decisões tomadas dentro da alçada para revisar juntos: isso é treino, não controle.").font = T(9, c="5F5F55", i=True)
    a.cell(19, 1, "Imprima a tabela e entregue a quem opera: critério que não está escrito e à vista continua sendo pergunta. Revise a cada contratação e a cada seis meses.").font = T(9, c="5F5F55", i=True)
    dva = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, errorTitle="Valor inválido", error="Use um valor maior ou igual a zero."); a.add_data_validation(dva); dva.add("E5:E11"); dva.add("B13:B14")

    # ---------- Escala ----------
    e = wb.create_sheet("Escala"); e.sheet_view.showGridLines = False
    titulo(e, "Escala da semana", "Quem está em cada função, em cada dia. Escreva o mesmo nome sempre do mesmo jeito.", exemplo)
    fixo(e, 3, 1, "Semana de", True); ent(e, 3, 2, INICIO_EX if exemplo else None, DATA)
    cabecalho(e, 4, ["Função", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom", "Dias sem ninguém"], [26, 15, 15, 15, 15, 15, 15, 15, 12])
    for k, fn in enumerate(FUNCOES):
        l = 5 + k; fixo(e, l, 1, fn, True)
        for d in range(7): ent(e, l, 2 + d, ESCALA_EX[k][d] if exemplo else None)
        calc(e, l, 9, f"=COUNTBLANK(B{l}:H{l})", "0")
    cabecalho(e, 11, ["Pessoa", "Turnos na semana", "Quem substitui se faltar"])
    e.column_dimensions["C"].width = 15
    for k in range(5):
        l = 12 + k
        p = PESSOAS_EX[k] if exemplo and k < len(PESSOAS_EX) else (None, None)
        ent(e, l, 1, p[0]); calc(e, l, 2, f'=IF(A{l}="","",COUNTIF($B$5:$H$8,A{l}))', "0"); ent(e, l, 3, p[1])
        e.merge_cells(start_row=l, start_column=3, end_row=l, end_column=6)
    fixo(e, 18, 1, "Turnos sem ninguém na semana", True); calc(e, 18, 2, "=SUM(I5:I8)", "0", True)
    fixo(e, 19, 1, "Pessoas sem substituto", True); calc(e, 19, 2, '=SUMPRODUCT((A12:A16<>"")*(C12:C16=""))', "0")
    fixo(e, 20, 1, "Situação", True)
    calc(e, 20, 2, '=IF(COUNTA(B5:H8)=0,"Preencha a escala",IF(B18>0,"Há "&B18&" turno(s) sem ninguém: defina quem cobre",IF(B19>0,"Defina quem substitui cada pessoa","Escala completa")))')
    e.merge_cells("B20:H20"); alerta(e, "B20", "Escala completa")
    e.cell(22, 1, "Rotina do gestor na Bíblia Operacional Zion: definir e comunicar a escala da semana seguinte, toda semana. Defina a cobertura de falta antes de precisar dela.").font = T(9, c="5F5F55", i=True)

    # ---------- Plano 4 semanas ----------
    p = wb.create_sheet("Plano 4 semanas"); p.sheet_view.showGridLines = False
    titulo(p, "Plano de quatro semanas", "A atividade que sai de você primeiro. As datas saem da data de início.", exemplo)
    campos = [(4, "Atividade que sai de você", "Check-in e check-out", "@"), (5, "Quem assume", "Diarista, que já faz a limpeza", "@"),
              (6, "Formato (Diarista por estadia, Meio período, Integral)", "Diarista por estadia", "@"), (7, "Início da semana 1", INICIO_EX, DATA),
              (9, "Quem substitui se a pessoa faltar", "Eu (dona), nas folgas da diarista", "@")]
    for l, r, v, fmt in campos:
        fixo(p, l, 1, r, True); ent(p, l, 2, v if exemplo else None, fmt); p.merge_cells(start_row=l, start_column=2, end_row=l, end_column=4)
    fixo(p, 8, 1, "Alçada inicial (da aba Alçadas)", True); calc(p, 8, 2, "=IF(Alçadas!B13=\"\",\"\",Alçadas!B13)", BRL)
    cabecalho(p, 11, ["Semana", "De", "Até", "O que acontece", "Conversa", "Sinal para avançar", "Sinal visto? (Sim/Não)"], [32, 13, 13, 52, 18, 28, 14])
    for k, (s, faz, conv, sinal) in enumerate(SEMANAS):
        l = 12 + k
        fixo(p, l, 1, s, True)
        calc(p, l, 2, f'=IF($B$7="","",$B$7+{7 * k})', DATA); calc(p, l, 3, f'=IF($B$7="","",$B$7+{7 * k + 6})', DATA)
        fixo(p, l, 4, faz); fixo(p, l, 5, conv); fixo(p, l, 6, sinal); ent(p, l, 7, None)
        p.row_dimensions[l].height = 58
    fixo(p, 16, 1, "Avaliação do primeiro mês", True); calc(p, 16, 2, '=IF($B$7="","",$B$7+27)', DATA, True)
    fixo(p, 17, 1, "Na data da avaliação, responda (Sim/Não):", True)
    for k, q in enumerate(["O padrão está sendo mantido?", "As decisões dentro da alçada foram razoáveis?", "As dúvidas diminuíram?"]):
        l = 18 + k; fixo(p, l, 1, q); ent(p, l, 2, None)
    fixo(p, 21, 1, "Resultado da avaliação", True)
    calc(p, 21, 2, '=IF(COUNTA(B18:B20)<3,"Responda as três perguntas na data da avaliação",IF(COUNTIF(B18:B20,"Sim")=3,"Operando: a pessoa assumiu a atividade","Repita a semana 3 antes de concluir que a contratação falhou"))')
    p.merge_cells("B21:F21")
    fixo(p, 23, 1, "Antes da semana 1 (Sim/Não):", True)
    pre = [("Acessos resolvidos: cofre de senhas, acessos nominais e telefone da operação", "Não"),
           ("Procedimento da atividade escrito nos seis blocos e testado por quem não sabe", "Não"),
           ("Tabela de critérios impressa e entregue a quem opera", "Sim")]
    for k, (r, v) in enumerate(pre):
        l = 24 + k; fixo(p, l, 1, r); ent(p, l, 2, v if exemplo else None)
    fixo(p, 27, 1, "Itens prontos antes da semana 1 (de 3)", True); calc(p, 27, 2, '=COUNTIF(B24:B26,"Sim")', "0")
    fixo(p, 28, 1, "Situação", True)
    calc(p, 28, 2, '=IF(OR(B4="",B5="",B7="",B9=""),"Preencha atividade, quem assume, início e cobertura",IF(B27<3,"Antes da semana 1: faltam "&(3-B27)&" de 3 itens","Pronto para começar"))')
    p.merge_cells("B28:F28"); alerta(p, "B28", "Pronto para começar")
    p.cell(30, 1, "Corrija depois, não durante: corrigir no meio ensina a pessoa a esperar você. O erro mais comum é pular da semana 1 direto para a 4.").font = T(9, c="5F5F55", i=True)
    dvs = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); p.add_data_validation(dvs); dvs.add("G12:G15"); dvs.add("B18:B20"); dvs.add("B24:B26")
    dvf = DataValidation(type="list", formula1='"Diarista por estadia,Meio período,Integral"', allow_blank=True); p.add_data_validation(dvf); dvf.add("B6")

    # ---------- Painel por exceção ----------
    pe = wb.create_sheet("Painel por exceção"); pe.sheet_view.showGridLines = False
    titulo(pe, "Painel por exceção", "Uma linha por semana. Contato na hora só nas quatro exceções; o resto espera o relatório semanal.", exemplo)
    fixo(pe, 4, 1, "Nota mínima das avaliações", True); ent(pe, 4, 2, 4.7 if exemplo else None, "0.0")
    fixo(pe, 5, 1, "Gasto acima do previsto que aciona você (%)", True); ent(pe, 5, 2, 10 if exemplo else None, "0")
    fixo(pe, 6, 1, "Alçada inicial da equipe (da aba Alçadas)", True); calc(pe, 6, 2, "=IF(Alçadas!B13=\"\",\"\",Alçadas!B13)", BRL)
    cabecalho(pe, 8, ["Semana de", "Nota da semana", "Ocupação", "Ocupação projetada", "Tempo médio de resposta (min)", "Ocorrências", "Decisões dentro da alçada", "Decisões fora da alçada", "Ocorrências de segurança ou dano", "Gasto (R$)", "Gasto previsto (R$)", "Leitura"],
              [30, 10, 11, 11, 12, 11, 11, 11, 12, 12, 12, 34])
    fmts = [DATA, "0.0", "0%", "0%", "0", "0", "0", "0", "0", BRL, BRL]
    for k in range(12):
        l = 9 + k
        lin = PAINEL_EX[k] if exemplo and k < len(PAINEL_EX) else [None] * 11
        for c in range(11): ent(pe, l, 1 + c, lin[c], fmts[c])
        calc(pe, l, 12, f'=IF(A{l}="","",IF(OR(AND(B{l}<>"",$B$4<>"",B{l}<$B$4),N(H{l})>0,N(I{l})>0,AND(N(K{l})>0,N(J{l})>N(K{l})*(1+N($B$5)/100))),"EXCEÇÃO: contato na hora","Relatório semanal: dentro do esperado"))')
    fixo(pe, 22, 1, "Semanas com exceção", True); calc(pe, 22, 2, '=COUNTIF(L9:L20,"EXCEÇÃO*")', "0", True)
    fixo(pe, 23, 1, "Situação", True)
    calc(pe, 23, 2, '=IF(OR(B4="",B5=""),"Defina a nota mínima e o percentual do gasto","OK")'); pe.merge_cells("B23:E23"); alerta(pe, "B23", "OK")
    pe.conditional_formatting.add("L9:L20", FormulaRule(formula=['LEFT(L9,7)="EXCEÇÃO"'], fill=ALERTA, font=Font(color="9B2C1F", bold=True)))
    pe.cell(25, 1, "As quatro exceções da fonte: avaliação abaixo da nota mínima; decisão fora da alçada que precisou ser tomada; ocorrência de segurança ou dano; gasto acima do previsto no percentual definido. Leitura semanal de 15 minutos; conversa mensal de 40 minutos com a Folha Única do Módulo 2.").font = T(9, c="5F5F55", i=True)
    pe.cell(26, 1, "Auditoria por amostragem: uma unidade sorteada por semana dá o mesmo controle que conferir tudo, sem prender você.").font = T(9, c="5F5F55", i=True)
    dvp = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", showErrorMessage=True, errorTitle="Valor inválido", error="Use um número maior ou igual a zero."); pe.add_data_validation(dvp); dvp.add("B4:B5"); dvp.add("B9:K20")
    for w in wb.worksheets[1:]:
        w.cell(w.max_row + 2, 1, NOTA).font = T(8, c="5F5F55", i=True)
    wb.active = 0
    return wb

for exemplo, nome in ((False, "Tarefas-Escala-e-Alcadas-Zion-EM-BRANCO.xlsx"), (True, "Tarefas-Escala-e-Alcadas-Zion-EXEMPLO.xlsx")):
    montar(exemplo).save(OUT / nome); print("ok", OUT / nome)

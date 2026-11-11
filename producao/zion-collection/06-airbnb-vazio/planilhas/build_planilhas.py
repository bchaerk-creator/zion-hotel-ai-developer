"""Gera as planilhas do Produto 06 (molde Zion: aba Comece aqui, amarelo = você preenche, verde = calculado):
  Diagnostico-Zion-de-Oferta-EM-BRANCO.xlsx / -EXEMPLO.xlsx   (ferramenta principal, versão planilha)
  Calendario-Comercial-30-Dias-EM-BRANCO.xlsx / -EXEMPLO.xlsx  (order bump)
Uso: python3 -I build_planilhas.py <saida>"""
import sys, pathlib, datetime
A = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(A.parent / "bump"))
from acoes import ACOES, SEMANAS, semana
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, PRETO, CREME, TERRA = "1B2117", "040605", "FEF5F0", "8B714E"
ENT, CALC, CAB = PatternFill("solid", fgColor="FFF4C7"), PatternFill("solid", fgColor="E3EEDF"), PatternFill("solid", fgColor=MUSGO)
fino = Side(style="thin", color="C9B8A0"); BORDA = Border(left=fino, right=fino, top=fino, bottom=fino)
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)
WRAP = Alignment(wrap_text=True, vertical="top")

DIMS = [("Fotos e apresentação", "A primeira foto e a sequência mostram com clareza o que o hóspede vai viver?"),
        ("Título e descrição", "O título diz para quem é e o que tem de diferente; a descrição traz fatos verificáveis?"),
        ("Preço e posicionamento", "A diária respeita o piso de custo e está coerente com anúncios comparáveis?"),
        ("Diferenciais e experiência", "Os diferenciais são percebidos pelo hóspede e aparecem com prova?"),
        ("Avaliações e confiança", "Avaliações e respostas públicas passam segurança para quem não conhece você?"),
        ("Atendimento e comunicação", "As respostas são rápidas, completas e iguais para todo hóspede?"),
        ("Conforto e infraestrutura", "Cama, banho, limpeza, internet e itens básicos entregam o que o anúncio promete?")]
EX_NOTAS = [2, 3, 3, 4, 4, 2, 4]
EX_EV = ["Primeira foto é da fachada; quarto só aparece na 7ª foto.", "Título diz 'Lindo apê', sem público nem diferencial.", "Diária igual todos os dias; não conheço meu piso de custo.",
         "Varanda com vista citada em 4 avaliações.", "Nota alta; 2 críticas sobre barulho sem resposta.", "Respondo em até 6 horas; cada hóspede recebe um texto diferente.", "Cama e limpeza elogiadas; chuveiro fraco citado uma vez."]


def cab(ws, linha, textos, larg=None):
    for i, t in enumerate(textos, 1):
        c = ws.cell(linha, i, t); c.fill = CAB; c.font = T(10, True, CREME); c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = BORDA


def comece(wb, titulo, linhas):
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 100
    ws["A1"] = "ZION COLLECTION · PRODUTO 06"; ws["A1"].font = T(9, True, TERRA)
    ws["A2"] = titulo; ws["A2"].font = Font(name="Georgia", size=22, color=MUSGO)
    r = 4
    for l in linhas:
        c = ws.cell(r, 1, l); c.alignment = WRAP; c.font = T(11, l.isupper(), MUSGO if l.isupper() else PRETO); r += 1
    ws.cell(r + 1, 1, "Amarelo = você preenche").fill = ENT
    ws.cell(r + 2, 1, "Verde = calculado pela planilha (não precisa mexer)").fill = CALC
    ws.cell(r + 4, 1, "Zion Hotel Group International · material educativo. Indicadores orientativos: não são previsão de reservas, ocupação ou faturamento.").font = T(9, i=True, c=TERRA)
    return ws


def diagnostico(exemplo):
    wb = Workbook()
    comece(wb, "Diagnóstico Zion de Oferta", [
        "COMO USAR (15 MINUTOS)",
        "1. Na aba Diagnóstico, dê uma nota inteira de 0 a 5 para cada dimensão: 0 ausente · 1 muito fraco · 2 fraco · 3 parcial · 4 bom · 5 consistente e comprovado.",
        "2. Ao lado, escreva a evidência: foto, avaliação, mensagem ou número que comprova a nota. Sem evidência, a nota é hipótese.",
        "3. A planilha calcula a pontuação (soma ÷ 35 × 100), a faixa e as três prioridades (as menores notas; no empate vale a ordem das dimensões).",
        "4. Na aba Plano de ação, defina ação, responsável, prazo, custo estimado, indicador e status para cada prioridade.",
        "5. Refaça o diagnóstico em 30 dias com a mesma base de datas e compare.",
        "FOCO 20% · 4% · 0,8%: as 3 prioridades (20%), a ação da semana (4%) e o primeiro passo de hoje, em menos de 1 hora (0,8%). Heurística de foco, não promessa.",
        "A versão interativa (celular e computador) faz as mesmas contas e exporta PDF e CSV." + (" · ESTA CÓPIA TEM DADOS FICTÍCIOS DE EXEMPLO." if exemplo else "")])
    ws = wb.create_sheet("Diagnóstico"); ws.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFG", (28, 44, 10, 48, 22, 6, 6)): ws.column_dimensions[col].width = w
    ws["A1"] = "Diagnóstico Zion de Oferta" + (" · EXEMPLO (dados fictícios)" if exemplo else ""); ws["A1"].font = Font(name="Georgia", size=18, color=MUSGO)
    ws["A2"] = "Hospedagem"; ws["B2"] = "Apartamento Exemplo (dados fictícios)" if exemplo else None; ws["B2"].fill = ENT
    ws["A3"] = "Período de referência"; ws["B3"] = "Últimos 90 dias" if exemplo else None; ws["B3"].fill = ENT
    cab(ws, 5, ["Dimensão", "Pergunta", "Nota (0 a 5)", "Evidência", "Aviso", "Ordem", "Chave"])
    dv = DataValidation(type="whole", operator="between", formula1="0", formula2="5", allow_blank=True, showErrorMessage=True, errorTitle="Nota inválida", error="Use nota inteira de 0 a 5.")
    ws.add_data_validation(dv)
    for i, (nome, perg) in enumerate(DIMS):
        r = 6 + i
        ws.cell(r, 1, nome).font = T(11, True); ws.cell(r, 2, perg).alignment = WRAP
        n = ws.cell(r, 3, EX_NOTAS[i] if exemplo else None); n.fill = ENT; dv.add(n)
        e = ws.cell(r, 4, EX_EV[i] if exemplo else None); e.fill = ENT; e.alignment = WRAP
        a = ws.cell(r, 5, f'=IF(C{r}="","Falta a nota",IF(D{r}="","Sem evidência: hipótese",""))'); a.fill = CALC; a.font = T(9, c=TERRA)
        ws.cell(r, 6, i + 1).font = T(8, c="999999")
        k = ws.cell(r, 7, f'=IF(C{r}="","",C{r}*10+F{r})'); k.font = T(8, c="999999")
        for c in range(1, 8): ws.cell(r, c).border = BORDA
        ws.row_dimensions[r].height = 34
    rows = [("Notas preenchidas", "=COUNT(C6:C12)&\" de 7\""), ("Soma das notas (0 a 35)", "=IF(COUNT(C6:C12)=7,SUM(C6:C12),\"\")"),
            ("Pontuação geral (0 a 100)", "=IF(COUNT(C6:C12)=7,ROUND(SUM(C6:C12)/35*100,0),\"Preencha as 7 notas\")"),
            ("Faixa", '=IF(COUNT(C6:C12)<7,"",IF(B16>=85,"Oferta consistente",IF(B16>=70,"Boa base com pontos de melhoria",IF(B16>=50,"Ajustes prioritários","Lacunas relevantes"))))')]
    for j, (rot, f) in enumerate(rows):
        r = 14 + j; ws.cell(r, 1, rot).font = T(11, True); c = ws.cell(r, 2, f); c.fill = CALC; c.font = T(12, True, MUSGO); c.border = BORDA
    ws.cell(18, 1, "Alerta").font = T(11, True)
    c = ws.cell(18, 2, '=IF(COUNTIF(C6:C12,"<=1")>0,"Atenção: há nota 0 ou 1. Trate como prioridade, mesmo com pontuação alta.","")'); c.fill = CALC; c.font = T(10, True, "C2643F")
    ws.cell(19, 1, "Suas três prioridades").font = Font(name="Georgia", size=14, color=MUSGO)
    for k in range(1, 4):
        r = 19 + k; ws.cell(r, 1, f"Prioridade {k}").font = T(11, True)
        c = ws.cell(r, 2, f'=IF(COUNT(C6:C12)<7,"",INDEX($A$6:$A$12,MATCH(SMALL($G$6:$G$12,{k}),$G$6:$G$12,0)))'); c.fill = CALC; c.border = BORDA; c.font = T(11, True, MUSGO)
        n = ws.cell(r, 3, f'=IF(B{r}="","",INDEX($C$6:$C$12,MATCH(B{r},$A$6:$A$12,0)))'); n.fill = CALC; n.border = BORDA
    ws.cell(24, 1, "Indicador orientativo para priorizar melhorias. Não é previsão de reservas, ocupação ou faturamento.").font = T(9, i=True, c=TERRA)
    # plano
    p = wb.create_sheet("Plano de ação"); p.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGH", (6, 26, 44, 18, 14, 14, 30, 16)): p.column_dimensions[col].width = w
    p["A1"] = "Plano de ação"; p["A1"].font = Font(name="Georgia", size=18, color=MUSGO)
    cab(p, 3, ["#", "Dimensão", "Ação", "Responsável", "Prazo", "Custo estimado (R$)", "Indicador", "Status"])
    dvs = DataValidation(type="list", formula1='"A fazer,Em andamento,Feito"', allow_blank=True); p.add_data_validation(dvs)
    dvd = DataValidation(type="date", operator="greaterThan", formula1="36526", allow_blank=True, error="Use uma data válida."); p.add_data_validation(dvd)
    dvc = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True, error="Use um valor em reais, sem sinal negativo."); p.add_data_validation(dvc)
    ex_plano = [("Refazer a ordem das 10 primeiras fotos; a primeira mostra a varanda com vista.", "Ana", datetime.date(2026, 12, 1), None, "Taxa de consulta", "Em andamento"),
                ("Criar respostas-padrão para as 5 perguntas mais frequentes; prazo de resposta de 1 hora.", "Ana", datetime.date(2026, 12, 8), None, "Tempo de primeira resposta", "A fazer"),
                ("Reescrever o título: público + diferencial + bairro.", "Ana", datetime.date(2026, 12, 15), 0, "Taxa de consulta", "A fazer")]
    for i in range(10):
        r = 4 + i; p.cell(r, 1, i + 1)
        d = p.cell(r, 2, f"=Diagnóstico!B{20 + i}" if i < 3 else None); d.fill = CALC if i < 3 else ENT
        vals = ex_plano[i] if exemplo and i < 3 else (None,) * 6
        for j, v in enumerate(vals):
            c = p.cell(r, 3 + j, v); c.fill = ENT; c.alignment = WRAP
            if j == 2: c.number_format = "DD/MM/YYYY"; dvd.add(c)
            if j == 3: c.number_format = '"R$" #,##0.00'; dvc.add(c)
            if j == 5: dvs.add(c)
        for c in range(1, 9): p.cell(r, c).border = BORDA
        p.row_dimensions[r].height = 30
    p.cell(15, 2, "Ações concluídas").font = T(11, True); c = p.cell(15, 3, '=COUNTIF(H4:H13,"Feito")&" de "&COUNTA(C4:C13)'); c.fill = CALC
    nome = "Diagnostico-Zion-de-Oferta-" + ("EXEMPLO" if exemplo else "EM-BRANCO") + ".xlsx"
    wb.save(OUT / nome); return nome


def calendario(exemplo):
    wb = Workbook()
    comece(wb, "Calendário comercial de 30 dias", [
        "COMO USAR",
        "1. Na aba Calendário, escreva a data de início (o seu dia 1). As datas e os dias da semana se calculam sozinhos.",
        "2. Cada dia tem uma ação já escrita, de 15 a 60 minutos, ligada a uma das sete dimensões do Diagnóstico Zion de Oferta.",
        "3. Ao terminar, marque Feito = Sim e anote o que observou. Não conseguiu? Marque Não e siga; o dia de revisão serve para recuperar.",
        "4. O resumo mostra quantas ações você concluiu por semana.",
        "Este calendário é um complemento opcional do guia 'Seu Airbnb Está Vazio?'. O guia e a ferramenta funcionam sem ele.",
        "Confira sempre as regras atuais da sua plataforma antes de mudar tarifas, fotos ou políticas." + (" · ESTA CÓPIA TEM DADOS FICTÍCIOS DE EXEMPLO." if exemplo else "")])
    ws = wb.create_sheet("Calendário"); ws.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHIJ", (6, 12, 10, 22, 26, 60, 9, 30, 10, 34)): ws.column_dimensions[col].width = w
    ws["A1"] = "Calendário comercial de 30 dias" + (" · EXEMPLO (dados fictícios)" if exemplo else ""); ws["A1"].font = Font(name="Georgia", size=18, color=MUSGO)
    ws["A2"] = "Data de início"; ws["A2"].font = T(11, True)
    ini = ws["D2"]; ini.value = datetime.date(2026, 12, 1) if exemplo else None; ini.fill = ENT; ini.number_format = "DD/MM/YYYY"; ini.border = BORDA
    dvd = DataValidation(type="date", operator="greaterThan", formula1="36526", allow_blank=True, error="Use uma data válida."); ws.add_data_validation(dvd); dvd.add(ini)
    cab(ws, 4, ["Dia", "Data", "Dia da semana", "Semana", "Dimensão", "Ação do dia", "Minutos", "O que observar", "Feito?", "Anotação / indicador observado"])
    dvf = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); ws.add_data_validation(dvf)
    ex_feito = {d: "Sim" for d in range(1, 13)} | {13: "Não", 14: "Sim"}
    ex_nota = {1: "Pontuação 63; prioridades: fotos, atendimento, título.", 2: "Linha de base: 600 visualizações, 18 consultas, 3 reservas (dados fictícios).", 6: "Primeira foto trocada em 06/12.", 10: "Título novo publicado em 10/12.", 13: "Não deu tempo; refazer no dia 14."}
    for d, dim, acao, mins, obs in ACOES:
        r = 4 + d
        ws.cell(r, 1, d).font = T(11, True)
        c = ws.cell(r, 2, f'=IF($D$2="","",$D$2+{d - 1})'); c.number_format = "DD/MM"; c.fill = CALC
        c = ws.cell(r, 3, f'=IF($D$2="","",CHOOSE(WEEKDAY(B{r}),"dom","seg","ter","qua","qui","sex","sáb"))'); c.fill = CALC
        ws.cell(r, 4, f"{semana(d)} · {SEMANAS[semana(d)]}").font = T(9, c=TERRA)
        ws.cell(r, 5, dim); ws.cell(r, 6, acao).alignment = WRAP; ws.cell(r, 7, mins); ws.cell(r, 8, obs).alignment = WRAP
        f = ws.cell(r, 9, ex_feito.get(d) if exemplo else None); f.fill = ENT; dvf.add(f)
        n = ws.cell(r, 10, ex_nota.get(d) if exemplo else None); n.fill = ENT; n.alignment = WRAP
        for col in range(1, 11): ws.cell(r, col).border = BORDA
        ws.row_dimensions[r].height = 44
    ws.freeze_panes = "A5"
    rs = 37; ws.cell(rs, 1, "Resumo").font = Font(name="Georgia", size=14, color=MUSGO)
    for i, (lo, hi, nome) in enumerate([(1, 7, "Semana 1"), (8, 14, "Semana 2"), (15, 21, "Semana 3"), (22, 28, "Semana 4"), (29, 30, "Dias 29 e 30"), (1, 30, "Total")]):
        r = rs + 1 + i; ws.cell(r, 4, nome).font = T(11, True)
        c = ws.cell(r, 5, f'=COUNTIF(I{4 + lo}:I{4 + hi},"Sim")&" de {hi - lo + 1} feitas"'); c.fill = CALC; c.border = BORDA
    c = ws.cell(rs + 7, 5, '=ROUND(COUNTIF(I5:I34,"Sim")/30*100,0)&"% do calendário"'); c.fill = CALC; c.font = T(12, True, MUSGO)
    ws.cell(rs + 7, 4, "Concluído").font = T(11, True)
    nome = "Calendario-Comercial-30-Dias-" + ("EXEMPLO" if exemplo else "EM-BRANCO") + ".xlsx"
    wb.save(OUT / nome); return nome


for ex in (False, True):
    print(diagnostico(ex)); print(calendario(ex))

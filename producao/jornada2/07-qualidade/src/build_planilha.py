"""Gera a planilha "Qualidade e Reputação" (Jornada 2 · Gestão · Módulo 7) em duas versões:
   - Qualidade-e-Reputacao-Zion-EM-BRANCO.xlsx
   - Qualidade-e-Reputacao-Zion-EXEMPLO.xlsx (dados fictícios, identificados como exemplo)
Uso: python3 -I build_planilha.py <pasta-saida>
Molde: producao/jornada2/05-pessoas/src/build_planilha.py (amarelo = preenche, verde = calculado).
Abas: Comece aqui · Avaliações por canal · Críticas · Painel semanal · Teste de prontidão · Plano de saída."""
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
BRL = 'R$ #,##0.00;[Red]-R$ #,##0.00'; DATA = "DD/MM/YYYY"; PCT = "0.0%"
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)
NOTA = "Zion Hospitality Business · Material educativo: não é promessa de renda, retorno ou resultado. A gestão depende da execução de cada hospedagem."

def cabecalho(ws, linha, titulos, larguras=None):
    for i, t in enumerate(titulos, 1):
        x = ws.cell(linha, i, t); x.font = T(10, True, CREME); x.fill = CAB; x.border = borda; x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        if larguras: ws.column_dimensions[x.column_letter].width = larguras[i - 1]
    ws.row_dimensions[linha].height = 36
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
    ws.conditional_formatting.add(cel, FormulaRule(formula=[f'LEFT({cel.split(":")[0]},{len(ok_txt)})<>"{ok_txt}"'], fill=ALERTA, font=Font(color="9B2C1F", bold=True)))
def simnao(ws, rng):
    dv = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); ws.add_data_validation(dv); dv.add(rng)

# ---------- dados do exemplo (os mesmos da ficha e do roteiro) ----------
CANAIS_EX = [("Plataforma A", 24, 4.7, 16, 44), ("Plataforma B", 9, 4.6, 5, 13), ("Perfil no mapa (hóspedes da venda direta)", 5, 4.9, 4, 15)]
CRITICAS_EX = [(dt.date(2026, 8, 12), "Plataforma A", "Ralo do chuveiro com cheiro na cabana 3", "Limpeza", "Sim"),
               (dt.date(2026, 8, 20), "Plataforma B", "Wi-Fi fraco na cabana 1", "Conforto e estrutura", "Sim"),
               (dt.date(2026, 9, 3), "Plataforma A", "Placa da estrada pouco visível", "Chegada", "Sim"),
               (dt.date(2026, 9, 19), "Perfil no mapa", "Ralo do chuveiro com cheiro na cabana 3", "Limpeza", "Não"),
               (dt.date(2026, 10, 2), "Plataforma A", "Toalha com fio puxado", "Limpeza", "Sim"),
               (dt.date(2026, 10, 15), "Plataforma B", "Wi-Fi fraco na cabana 1", "Conforto e estrutura", "Sim"),
               (dt.date(2026, 10, 24), "Plataforma A", "Ralo do chuveiro com cheiro na cabana 3", "Limpeza", "Não")]
AJUSTE_EX = ("Trocar o sifão do chuveiro da cabana 3 e incluir o ralo no checklist de limpeza", dt.date(2026, 11, 30))
# semana, nota, recebidas, respondidas, tempo (min), ocorrências, segurança ou dano, fora da alçada, gasto, previsto
PAINEL_EX = [(dt.date(2026, 10, 12), 4.8, 2, 2, 45, 1, 0, 0, 950, 1000),
             (dt.date(2026, 10, 19), 4.5, 1, 1, 35, 2, 0, 0, 1020, 1000),
             (dt.date(2026, 10, 26), 4.9, 3, 2, 50, 0, 0, 0, 980, 1000),
             (dt.date(2026, 11, 2), 4.7, 2, 2, 30, 1, 0, 0, 1150, 1000)]
NLIN_CRIT = 30; NLIN_PAINEL = 13

def montar(exemplo):
    wb = Workbook()
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False; ws.column_dimensions["A"].width = 100
    linhas = [
        ("ZION HOSPITALITY BUSINESS · JORNADA 2 · GESTÃO · MÓDULO 7 · QUALIDADE", T(10, True, DOURADO)),
        ("Qualidade e Reputação", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para acompanhar a nota, as avaliações e as críticas toda semana, agendar o teste das duas semanas e datar o plano de saída da operação. É a planilha da página 7 do seu Plano de Gestão Profissional.", T(11, c="2D352A")),
        ("EXEMPLO DIDÁTICO PREENCHIDO COM DADOS FICTÍCIOS (Cabanas do Vale, 4 unidades). Use a versão em branco para a sua hospedagem." if exemplo else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("", None),
        ("COMO USAR EM 5 PASSOS (cerca de 30 minutos na primeira vez, 15 por semana depois)", T(12, True, MUSGO)),
        ("1. Aba Avaliações por canal: a escala, a meta, a nota mínima e, para cada canal, as avaliações acumuladas, a nota e o movimento dos últimos três meses. A planilha calcula a nota geral, a taxa de avaliação e quanto uma avaliação ruim pesa.", None),
        ("2. Aba Críticas: anote toda crítica, mesmo a que aparece dentro de uma avaliação boa. A planilha conta as menções no trimestre: três ao mesmo item é problema de produto, e pede o ajuste com prazo.", None),
        ("3. Aba Painel semanal: uma linha por semana com a nota, as avaliações recebidas e respondidas, o tempo de resposta, as ocorrências e o gasto. A planilha diz se é exceção (contato na hora), atenção ou relatório semanal.", None),
        ("4. Aba Teste de prontidão: a data das duas semanas fora, o responsável e as referências. Depois do teste, lance os resultados: a planilha lê pela régua da fonte.", None),
        ("5. Aba Plano de saída: as quatro fases com datas, a rotina do ano e as quatro condições da segunda unidade.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("DE ONDE VEM", T(12, True, MUSGO)),
        ("Método Zion 360°, Volume 07 Lançamento (Protocolo da Primeira Avaliação: a média pequena, quando pedir e como responder); Jornada do COMO, Etapa 07 (Sistema de Avaliações: três menções ao mesmo item, taxa de 40%, resposta em menos de uma hora), Etapa 09 Passo 13 (Rotina Financeira) e Etapa 10 Passos 10, 12 e 13 (painel por exceção, Teste de Prontidão e Plano de Saída da Operação); Panorama do Desenvolvimento Hoteleiro, Trilha B, pilar G7.", None),
        ("O que a planilha não faz: não lê os canais sozinha, não prevê a nota nem a ocupação e não substitui a sua leitura das avaliações. A tolerância de 0,1 ponto na nota do teste é uma convenção desta planilha, porque a fonte fala em variação normal sem dar número.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice.", T(10, c="5F5F55", i=True)),
        (NOTA, T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Avaliações por canal ----------
    a = wb.create_sheet("Avaliações por canal"); a.sheet_view.showGridLines = False
    titulo(a, "Avaliações por canal", "Preencha as células amarelas. Uma linha por canal.", exemplo)
    for c, w in zip("ABCDEF", [44, 16, 14, 18, 18, 16]): a.column_dimensions[c].width = w
    par = [(4, "Escala da nota (5 ou 10)", 5, "0"), (5, "Meta da nota", 4.8 if exemplo else None, "0.0"), (6, "Nota mínima (abaixo dela, contato na hora)", 4.7 if exemplo else None, "0.0"),
           (7, "Taxa mínima de hóspedes que avaliam (referência da fonte: 40%)", 0.40, PCT), (8, "Resposta a mensagem em até (minutos; a fonte pede menos de uma hora)", 60, "0"),
           (9, "Nota média dos concorrentes diretos (opcional)", 4.6 if exemplo else None, "0.0")]
    for l, r, v, fmt in par: fixo(a, l, 1, r, True); ent(a, l, 2, v, fmt)
    dve = DataValidation(type="list", formula1='"5,10"', allow_blank=False); a.add_data_validation(dve); dve.add("B4")
    cabecalho(a, 11, ["Canal", "Avaliações acumuladas", "Nota média", "Avaliações nos últimos 3 meses", "Estadias nos últimos 3 meses", "Nota × avaliações (cálculo)"])
    for k in range(5):
        l = 12 + k; c = CANAIS_EX[k] if exemplo and k < len(CANAIS_EX) else (None,) * 5
        ent(a, l, 1, c[0]); ent(a, l, 2, c[1], "0"); ent(a, l, 3, c[2], "0.0"); ent(a, l, 4, c[3], "0"); ent(a, l, 5, c[4], "0")
        calc(a, l, 6, f'=IF(AND(N(B{l})>0,N(C{l})>0),B{l}*C{l},0)', "0.0")
    fixo(a, 18, 1, "Situação dos dados", True)
    calc(a, 18, 2, '=IF(SUM(B12:B16)=0,"Preencha pelo menos um canal com avaliações e nota",IF(OR(COUNTIF(C12:C16,">"&B4)>0,COUNTIF(C12:C16,"<0")>0),"Há nota fora da escala",IF(SUMPRODUCT((B12:B16>0)*(C12:C16=""))>0,"Há canal com avaliações e sem nota",IF(SUMPRODUCT((D12:D16>E12:E16)*1)>0,"Há canal com mais avaliações que estadias nos 3 meses",IF(SUMPRODUCT((D12:D16>B12:B16)*1)>0,"Há canal com mais avaliações nos 3 meses que no total",IF(N(B6)>N(B5),"A nota mínima passa da meta","OK"))))))')
    a.merge_cells("B18:F18"); alerta(a, "B18", "OK")
    res = [(20, "Avaliações acumuladas (todos os canais)", "=SUM(B12:B16)", "0", False),
           (21, "Nota geral (média ponderada pelo número de avaliações)", '=IF(SUM(B12:B16)>0,SUM(F12:F16)/SUMIF(C12:C16,">0",B12:B16),"")', "0.00", True),
           (22, "Taxa de avaliação (avaliações ÷ estadias, 3 meses)", '=IF(SUM(E12:E16)>0,SUM(D12:D16)/SUM(E12:E16),"")', PCT, True),
           (23, "Leitura da taxa", '=IF(B22="","Informe as estadias dos 3 meses",IF(B22<B7,"Abaixo do mínimo: o pedido não está sendo feito ou não está funcionando","Dentro do mínimo"))', "@", False),
           (24, "Média depois de uma única avaliação ruim (3 em 5, 6 em 10)", '=IF(B21="","",(B21*B20+0.6*B4)/(B20+1))', "0.00", False),
           (25, "Quanto essa avaliação derruba a média", '=IF(B24="","",B21-B24)', "0.00", False),
           (26, "Distância até a meta", '=IF(OR(B21="",N(B5)=0),"",B5-B21)', "0.00", False),
           (27, "Leitura da nota", '=IF(B21="","",IF(B21<B6,"EXCEÇÃO: abaixo da nota mínima",IF(B21<B5,"Abaixo da meta","Na meta ou acima")))', "@", False),
           (28, "Contra os concorrentes diretos (pontos)", '=IF(OR(B21="",N(B9)=0),"",B21-B9)', "+0.00;-0.00;0.00", False)]
    for l, r, f, fmt, dest in res: fixo(a, l, 1, r, True); calc(a, l, 2, f, fmt, dest)
    for l in (23, 27): a.merge_cells(f"B{l}:F{l}")
    a.cell(30, 1, "A média é lenta para subir e rápida para cair quando o volume é pequeno: acumular avaliações boas é a defesa (Volume 07, capítulo 18). Compare com os concorrentes diretos, não com o ideal (Etapa 07).").font = T(9, c="5F5F55", i=True)

    # ---------- Críticas ----------
    c = wb.create_sheet("Críticas"); c.sheet_view.showGridLines = False
    titulo(c, "Registro de críticas", "Anote toda crítica, mesmo pequena, mesmo dentro de avaliação boa. Use sempre o mesmo texto para o mesmo item.", exemplo)
    fixo(c, 4, 1, "Início do trimestre", True); ent(c, 4, 2, dt.date(2026, 8, 1) if exemplo else None, DATA)
    fixo(c, 5, 1, "Fim do trimestre", True); calc(c, 5, 2, '=IF(B4="","",EDATE(B4,3)-1)', DATA)
    cabecalho(c, 7, ["Data", "Canal", "O item criticado", "Dimensão", "Estava em avaliação boa?", "Menções do item no trimestre", "Leitura", "Ajuste de produto (quando 3 ou mais)", "Prazo do ajuste", "Primeira menção (cálculo)"], [13, 18, 40, 20, 13, 13, 30, 40, 13, 10])
    for k in range(NLIN_CRIT):
        l = 8 + k; e = CRITICAS_EX[k] if exemplo and k < len(CRITICAS_EX) else (None,) * 5
        ent(c, l, 1, e[0], DATA); ent(c, l, 2, e[1]); ent(c, l, 3, e[2]); ent(c, l, 4, e[3]); ent(c, l, 5, e[4])
        aj = AJUSTE_EX if exemplo and e[2] == "Ralo do chuveiro com cheiro na cabana 3" and k == 0 else (None, None)
        ent(c, l, 8, aj[0]); ent(c, l, 9, aj[1], DATA)
        calc(c, l, 6, f'=IF(OR(C{l}="",A{l}="",$B$4=""),"",COUNTIFS($C$8:$C${7 + NLIN_CRIT},C{l},$A$8:$A${7 + NLIN_CRIT},">="&$B$4,$A$8:$A${7 + NLIN_CRIT},"<="&$B$5))', "0")
        calc(c, l, 7, f'=IF(F{l}="","",IF(F{l}>=3,"PROBLEMA DE PRODUTO: ajuste com prazo","Registro"))')
        calc(c, l, 10, f'=IF(F{l}="",0,IF(AND(F{l}>=3,COUNTIF($C$8:C{l},C{l})=1),1,0))', "0")
    fim = 7 + NLIN_CRIT; s = fim + 2
    fixo(c, s, 1, "Críticas no trimestre", True); calc(c, s, 2, f'=IF($B$4="","",COUNTIFS($A$8:$A${fim},">="&$B$4,$A$8:$A${fim},"<="&$B$5,$C$8:$C${fim},"<>"))', "0", True)
    fixo(c, s + 1, 1, "Itens com três menções ou mais", True); calc(c, s + 1, 2, f"=SUM(J8:J{fim})", "0", True)
    fixo(c, s + 2, 1, "Críticas que estavam em avaliação boa", True); calc(c, s + 2, 2, f'=COUNTIF(E8:E{fim},"Sim")', "0")
    fixo(c, s + 3, 1, "Situação", True)
    calc(c, s + 3, 2, f'=IF($B$4="","Informe o início do trimestre",IF(SUMPRODUCT((J8:J{fim}=1)*(H8:H{fim}=""))>0,"Falta o ajuste de produto do item com três menções",IF(SUMPRODUCT((J8:J{fim}=1)*(I8:I{fim}=""))>0,"Falta o prazo do ajuste de produto","OK")))')
    c.merge_cells(f"B{s + 3}:G{s + 3}"); alerta(c, f"B{s + 3}", "OK")
    c.cell(s + 5, 1, "A nota cai por padrões, não por casos isolados. Três menções ao mesmo item em um trimestre é um problema de produto, não de hóspede (Etapa 07, Passo 06). O ajuste fica na linha da primeira menção.").font = T(9, c="5F5F55", i=True)
    simnao(c, f"E8:E{fim}")

    # ---------- Painel semanal ----------
    p = wb.create_sheet("Painel semanal"); p.sheet_view.showGridLines = False
    titulo(p, "Painel semanal por exceção", "Uma linha por semana. A nota mínima vem da aba Avaliações por canal.", exemplo)
    fixo(p, 4, 1, "Nota mínima", True); calc(p, 4, 2, "='Avaliações por canal'!B6", "0.0")
    fixo(p, 5, 1, "Resposta em até (min)", True); calc(p, 5, 2, "='Avaliações por canal'!B8", "0")
    fixo(p, 6, 1, "Gasto acima do previsto que é exceção (%)", True); ent(p, 6, 2, 10 if exemplo else None, "0")
    cabecalho(p, 8, ["Semana (segunda-feira)", "Nota das avaliações da semana", "Avaliações recebidas", "Avaliações respondidas", "Tempo médio de resposta (min)", "Ocorrências", "Ocorrência de segurança ou dano", "Decisões fora da alçada", "Gasto da semana (R$)", "Previsto (R$)", "Leitura"], [14, 12, 11, 11, 12, 11, 12, 11, 13, 13, 46])
    for k in range(NLIN_PAINEL):
        l = 9 + k; e = PAINEL_EX[k] if exemplo and k < len(PAINEL_EX) else (None,) * 10
        ent(p, l, 1, e[0], DATA); ent(p, l, 2, e[1], "0.0")
        for j, fmt in zip(range(3, 9), ["0", "0", "0", "0", "0", "0"]): ent(p, l, j, e[j - 1], fmt)
        ent(p, l, 9, e[8], BRL); ent(p, l, 10, e[9], BRL)
        calc(p, l, 11, f'=IF(A{l}="","",IF(OR(AND(B{l}<>"",B{l}<$B$4),N(G{l})>0,N(H{l})>0,AND(N(J{l})>0,N(I{l})>N(J{l})*(1+N($B$6)/100))),"EXCEÇÃO: contato na hora",IF(OR(N(D{l})<N(C{l}),AND(E{l}<>"",N(E{l})>$B$5)),"Atenção: "&IF(N(D{l})<N(C{l}),"avaliação sem resposta","")&IF(AND(N(D{l})<N(C{l}),E{l}<>"",N(E{l})>$B$5),"; ","")&IF(AND(E{l}<>"",N(E{l})>$B$5),"resposta acima do máximo",""),"Relatório semanal")))')
    f2 = 8 + NLIN_PAINEL; s = f2 + 2
    fixo(p, s, 1, "Semanas lançadas", True); calc(p, s, 2, f'=COUNT(A9:A{f2})', "0")
    fixo(p, s + 1, 1, "Semanas com exceção", True); calc(p, s + 1, 2, f'=COUNTIF(K9:K{f2},"EXCEÇÃO*")', "0", True)
    fixo(p, s + 2, 1, "Avaliações sem resposta", True); calc(p, s + 2, 2, f'=SUM(C9:C{f2})-SUM(D9:D{f2})', "0", True)
    fixo(p, s + 3, 1, "Tempo médio de resposta nas semanas (min)", True); calc(p, s + 3, 2, f'=IF(COUNT(E9:E{f2})=0,"",AVERAGE(E9:E{f2}))', "0")
    fixo(p, s + 4, 1, "Ocorrências registradas", True); calc(p, s + 4, 2, f'=SUM(F9:F{f2})', "0")
    fixo(p, s + 5, 1, "Situação", True); calc(p, s + 5, 2, f'=IF(N($B$4)=0,"Defina a nota mínima na aba Avaliações por canal",IF(N($B$6)<=0,"Defina o percentual de gasto que é exceção",IF(SUMPRODUCT((D9:D{f2}>C9:C{f2})*1)>0,"Há semana com mais respostas que avaliações","OK")))')
    p.merge_cells(f"B{s + 5}:H{s + 5}"); alerta(p, f"B{s + 5}", "OK")
    p.cell(s + 7, 1, "As quatro exceções que acionam o dono na hora: avaliação abaixo da nota mínima, decisão fora da alçada, ocorrência de segurança ou dano, gasto acima do previsto no percentual definido. O resto espera o relatório semanal (Etapa 10, Passo 10).").font = T(9, c="5F5F55", i=True)

    # ---------- Teste de prontidão ----------
    t = wb.create_sheet("Teste de prontidão"); t.sheet_view.showGridLines = False
    titulo(t, "O teste das duas semanas", "Catorze dias fora, sem atender, com contato só pelas quatro exceções.", exemplo)
    t.column_dimensions["A"].width = 52; t.column_dimensions["B"].width = 26; t.column_dimensions["C"].width = 60
    fixo(t, 4, 1, "ANTES DO TESTE", True)
    ant = [(5, "Início do teste", dt.date(2027, 6, 14) if exemplo else None, DATA), (7, "Quem fica responsável", "Diarista, com o auxiliar de manutenção" if exemplo else None, "@"),
           (8, "Ocupação projetada para o período", 0.50 if exemplo else None, PCT), (9, "Nota média dos três meses anteriores", 4.7 if exemplo else None, "0.0"),
           (10, "O período é de ocupação média, nem vale nem pico? (Sim ou Não)", "Sim" if exemplo else None, "@")]
    for l, r, v, fmt in ant: fixo(t, l, 1, r, True); ent(t, l, 2, v, fmt)
    fixo(t, 6, 1, "Fim do teste (14 dias corridos)", True); calc(t, 6, 2, '=IF(B5="","",B5+13)', DATA)
    simnao(t, "B10"); simnao(t, "B16")
    fixo(t, 12, 1, "DEPOIS DO TESTE", True)
    dep = [(13, "Ocupação do período", None, PCT), (14, "Nota das avaliações do período", None, "0.0"), (15, "Contatos por exceção durante o teste", None, "0"),
           (16, "A ocupação caiu por causa externa? (Sim ou Não)", None, "@"), (17, "Ocorrências registradas e resolvidas", None, "0")]
    for l, r, v, fmt in dep: fixo(t, l, 1, r, True); ent(t, l, 2, v, fmt)
    fixo(t, 19, 1, "Tolerância da nota (convenção: 0,1 em 5; 0,2 em 10)", True); calc(t, 19, 2, "=IF('Avaliações por canal'!B4=10,0.2,0.1)", "0.0")
    fixo(t, 20, 1, "Situação do agendamento", True)
    calc(t, 20, 2, '=IF(B5="","Marque a data: teste sem data marcada é teste que não acontece",IF(B7="","Defina quem fica responsável",IF(OR(B8="",B9=""),"Informe a ocupação projetada e a nota de referência",IF(B10<>"Sim","Escolha um período de ocupação média: vale fácil não testa nada","Teste agendado"))))')
    fixo(t, 21, 1, "Leitura do resultado", True)
    calc(t, 21, 2, '=IF(OR(B13="",B14="",B15=""),IF(B6="","","Lance os resultados depois de "&TEXT(B6,"DD/MM/YYYY")),IF(B14<B9-B19-0.000001,"A nota caiu: falta padrão ou falta treino (procedimento e quatro semanas do Módulo 5)",IF(AND(B13<B8,B16<>"Sim"),"A ocupação caiu sem causa externa: falta quem trabalhe a demanda (Módulos 3 e 4)",IF(B13<B8,"A ocupação caiu por causa externa: repita o teste em período de ocupação média",IF(B15>2,"Ocupação e nota mantidas, com muitos contatos: falta critério (tabela de critérios do Módulo 5)","PASSOU: a operação roda sem você")))))')
    t.merge_cells("B20:C20"); t.merge_cells("B21:C21"); alerta(t, "B20", "Teste agendado")
    regras = ["Regras: catorze dias corridos, com pelo menos um fim de semana cheio; sem atender mensagem, sem entrar no painel do canal, sem conferir unidade;",
              "contato apenas pelas quatro exceções; sem aviso especial à equipe. Cada resultado é um diagnóstico com endereço, e nenhum é fracasso (Etapa 10, Passo 12).",
              "Se catorze dias provocam ansiedade mesmo com tudo escrito, faça em degraus: três dias, depois cinco, depois dez."]
    for i, r in enumerate(regras): t.cell(23 + i, 1, r).font = T(9, c="5F5F55", i=True)

    # ---------- Plano de saída ----------
    s_ = wb.create_sheet("Plano de saída"); s_.sheet_view.showGridLines = False
    titulo(s_, "Plano de saída da operação e rotina do ano", "Quatro fases, de seis a oito meses do início ao teste.", exemplo)
    for col, w in zip("ABCDE", [40, 16, 16, 12, 40]): s_.column_dimensions[col].width = w
    ps = [(4, "Início da Fase 1 · Escrever", dt.date(2026, 11, 16) if exemplo else None, DATA), (5, "Semanas da Fase 1 (6 a 10)", 8, "0"), (6, "Semanas da Fase 2 · Contratar e treinar (cerca de 8)", 8, "0")]
    for l, r, v, fmt in ps: fixo(s_, l, 1, r, True); ent(s_, l, 2, v, fmt)
    fixo(s_, 7, 1, "Início do teste (vem da aba Teste de prontidão)", True); calc(s_, 7, 2, "=IF('Teste de prontidão'!B5=\"\",\"\",'Teste de prontidão'!B5)", DATA)
    cabecalho(s_, 9, ["Fase", "De", "Até", "Semanas", "Sinal de conclusão"])
    fx = [(10, "1 · Escrever (manual mínimo)", '=IF(B4="","",B4)', '=IF(B4="","",B4+7*B5-1)', '=IF(B4="","",B5)', "Manual em nuvem e impresso"),
          (11, "2 · Contratar e treinar", '=IF(C10="","",C10+1)', '=IF(C10="","",B11+7*B6-1)', '=IF(C10="","",B6)', "Padrão mantido com autonomia"),
          (12, "3 · Acompanhar por exceção (pelo menos 8 semanas)", '=IF(OR(C11="",B7=""),"",C11+1)', '=IF(OR(C11="",B7=""),"",B7-1)', '=IF(B12="","",INT((C12-B12+1)/7))', "Dúvidas raras, critérios em uso"),
          (13, "4 · Testar (2 semanas)", '=IF(B7="","",B7)', '=IF(B7="","",B7+13)', '=IF(B7="","",2)', "Ocupação e nota mantidas")]
    for l, r, f1, f2_, f3, sinal in fx:
        fixo(s_, l, 1, r, True); calc(s_, l, 2, f1, DATA); calc(s_, l, 3, f2_, DATA); calc(s_, l, 4, f3, "0"); fixo(s_, l, 5, sinal)
    fixo(s_, 15, 1, "Meses do início ao fim do teste", True); calc(s_, 15, 2, '=IF(OR(B4="",C13=""),"",ROUND((C13-B4+1)/30.4375,1))', "0.0", True)
    fixo(s_, 16, 1, "Situação do plano", True)
    calc(s_, 16, 2, '=IF(OR(B4="",B7=""),"Marque o início da Fase 1 e o início do teste",IF(B7<=C11,"O teste começa antes do fim da Fase 2: mova a data",IF(D12<8,"A Fase 3 tem menos de 8 semanas: o painel precisa rodar mais antes do teste",IF(OR(B15<6,B15>8),"Fora dos seis a oito meses da fonte: confira as fases","OK"))))')
    s_.merge_cells("B16:E16"); alerta(s_, "B16", "OK")
    fixo(s_, 18, 1, "O que vou fazer com o tempo que sobrar", True); ent(s_, 18, 2, "Trabalhar sobre o negócio: duas horas por semana para preço e venda direta" if exemplo else None); s_.merge_cells("B18:E18")
    fixo(s_, 20, 1, "SEGUNDA UNIDADE · AS QUATRO CONDIÇÕES", True)
    cond = [(21, "O teste das duas semanas passou", "Não"), (22, "A primeira gera resultado depois de pagar a minha retirada", "Sim"), (23, "Existe reserva para a rampa da segunda (12 a 18 meses)", "Não"), (24, "Existe quem supervisione as duas", "Não")]
    for l, r, v in cond: fixo(s_, l, 1, r, True); ent(s_, l, 2, v if exemplo else None)
    simnao(s_, "B21:B24")
    fixo(s_, 25, 1, "Decisão sobre a segunda unidade", True)
    calc(s_, 25, 2, '=IF(COUNTA(B21:B24)<4,"Responda as quatro condições",IF(COUNTIF(B21:B24,"Sim")=4,"Pode estudar a segunda unidade","Agora não: faltam "&(4-COUNTIF(B21:B24,"Sim"))&" de 4 condições"))')
    s_.merge_cells("B25:E25")
    fixo(s_, 27, 1, "ROTINA DO ANO", True)
    fixo(s_, 28, 1, "Primeira revisão trimestral (2 horas)", True); ent(s_, 28, 2, dt.date(2027, 1, 11) if exemplo else None, DATA)
    for k in range(1, 4): fixo(s_, 28 + k, 1, f"Revisão trimestral {k + 1}", True); calc(s_, 28 + k, 2, f'=IF($B$28="","",EDATE($B$28,{3 * k}))', DATA)
    fixo(s_, 32, 1, "Revisão anual (meio dia)", True); ent(s_, 32, 2, dt.date(2027, 11, 8) if exemplo else None, DATA)
    fixo(s_, 33, 1, "Dia do mês da Folha Única (10 minutos)", True); ent(s_, 33, 2, 5 if exemplo else None, "0")
    s_.cell(35, 1, "Toda semana: reunião de 30 minutos com os cinco números (G7), leitura de 15 minutos do painel (Etapa 10), 5 minutos de caixa (Etapa 09), avaliações respondidas e uma unidade sorteada para auditoria.").font = T(9, c="5F5F55", i=True)
    s_.cell(36, 1, "Faltando qualquer uma das quatro condições, a segunda unidade antecipa um problema em vez de multiplicar um acerto (Etapa 10, Passo 13).").font = T(9, c="5F5F55", i=True)
    return wb

for exemplo, nome in [(False, "Qualidade-e-Reputacao-Zion-EM-BRANCO.xlsx"), (True, "Qualidade-e-Reputacao-Zion-EXEMPLO.xlsx")]:
    wb = montar(exemplo); wb.save(OUT / nome); print("ok", OUT / nome)

"""Gera a planilha "Plano de Captação" (Jornada 2 · Gestão · Módulo 4 · Marketing e vendas) em duas versões:
   - Plano-de-Captacao-Zion-EM-BRANCO.xlsx
   - Plano-de-Captacao-Zion-EXEMPLO.xlsx (dados fictícios, identificados como exemplo)
Uso: python3 -I build_planilha.py <pasta-saida>
Molde: producao/jornada2/01-planejamento/src/build_planilha.py (amarelo = preenche, verde = calculado).
Abas: Comece aqui · Marca em uma folha · Captação do mês · Lista própria · Captação 12 meses · Definições e rotina."""
import sys, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, DOURADO, PRETO, CREME = "1B2117", "8B714E", "040605", "FEF5F0"
ENTRADA = PatternFill("solid", fgColor="FFF4C7"); CALC = PatternFill("solid", fgColor="E3EEDF"); CAB = PatternFill("solid", fgColor=MUSGO)
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
BRL = 'R$ #,##0.00;[Red]-R$ #,##0.00'; PCT = '0.0" %"'; PCTF = "0.0%"
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)
VERMELHO = PatternFill("solid", fgColor="F8E3DE")

def faixa(ws, linha, texto, cols=3):
    ws.merge_cells(start_row=linha, start_column=1, end_row=linha, end_column=cols)
    c = ws.cell(linha, 1, texto); c.font = T(11, True, CREME); c.fill = CAB; c.alignment = Alignment(vertical="center", indent=1); ws.row_dimensions[linha].height = 22
def rotulo(ws, l, texto, ajuda="", col_ajuda=3):
    a = ws.cell(l, 1, texto); a.font = T(11); a.alignment = Alignment(wrap_text=True, vertical="center")
    if ajuda: h = ws.cell(l, col_ajuda, ajuda); h.font = T(9, c="5F5F55", i=True); h.alignment = Alignment(wrap_text=True, vertical="center")
def entrada(ws, l, valor=None, fmt="@", col=2):
    c = ws.cell(l, col, valor); c.fill = ENTRADA; c.border = borda; c.number_format = fmt; c.font = T(11, True); c.alignment = Alignment(wrap_text=True, vertical="center"); return c
def calc(ws, l, formula, fmt=BRL, destaque=False, col=2):
    c = ws.cell(l, col, formula); c.fill = CALC; c.border = borda; c.number_format = fmt; c.font = T(13 if destaque else 10, True, MUSGO if destaque else PRETO); c.alignment = Alignment(wrap_text=True, vertical="center"); return c
def cabecalho(ws, linha, cols, larguras=None, altura=34):
    for i, t in enumerate(cols, 1):
        x = ws.cell(linha, i, t); x.font = T(10, True, CREME); x.fill = CAB; x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); x.border = borda
        if larguras: ws.column_dimensions[x.column_letter].width = larguras[i - 1]
    ws.row_dimensions[linha].height = altura
def situacao(ws, cel, formula, merge=None):
    c = ws[cel]; c.value = formula; c.font = T(11, True); c.border = borda; c.fill = CALC; c.alignment = Alignment(wrap_text=True, vertical="center")
    if merge: ws.merge_cells(merge)
    ws.conditional_formatting.add(cel, FormulaRule(formula=[f'${cel[0]}${cel[1:]}<>"OK"'], fill=VERMELHO, font=Font(color="9B2C1F", bold=True)))

# Exemplo didático · dados fictícios (Cabanas do Vale). Mesmos valores da ficha (logic.js EXEMPLO) e do PLANO seção 9.
EX_MARCA = dict(publico="Casais que vêm de carro, de até três horas de distância, para duas ou três noites.", nao="Grupos, festas e quem procura agito à noite.",
                promessa="Duas noites a dois, com a lareira acesa e o vale na janela da cama, sem vizinho à vista.", testes=["Sim"] * 4, cinco=4,
                prova="Foto de capa: a cama de frente para a janela do vale, com a lareira acesa ao lado.", tom="Próximo, concreto, calmo.",
                banidas="aconchegante, único, inesquecível, refúgio, experiência única", nunca="Não aceitamos festas nem mais de duas pessoas por cabana.",
                pontos=["Já aparece", "Não aparece", "Já aparece", "Não aparece", "Não aparece", "Não aparece"])
PONTOS = ["Anúncio das plataformas (título e foto de capa)", "Site ou página própria", "Perfil nas redes sociais", "Resposta de WhatsApp", "Mensagem de boas-vindas (Kit de Mensagens, M04)", "Placa na entrada"]
EX_CANAIS = [("Plataforma A", "Plataforma", 16, 0, 12, 8120), ("Plataforma B", "Plataforma", 15, 0, 5, 3248), ("Instagram com impulsionamento", "Direto", 0, 150, 2, 1120),
             ("Hóspede que volta (WhatsApp)", "Direto", 0, 0, 3, 1848), ("Indicação", "Direto", 0, 0, 3, 1904)]
EX_META = (40, "30/06/2027"); EX_MES = "Outubro de 2026 (exemplo)"
EX_LISTA = dict(frase="Posso guardar o seu WhatsApp e o seu e-mail para avisar quando abrirmos datas e condições? Você pode sair quando quiser.",
                onde="Só no meu celular (vai para esta planilha, com cópia)", acesso="Só a Ana", meta=120, estadias=25, antes=64, canal="WhatsApp")
EX_12 = [("Outubro de 2026 (exemplo)", 16240, 4872, 25, 1936.40, 0), ("Novembro de 2026 (exemplo)", 12950, 4144, 21, 1533.80, 18)]
C0, C1 = 7, 14  # linhas dos canais na aba Captação do mês
L0, L1 = 14, 213  # linhas da Lista própria

def montar(exemplo):
    wb = Workbook()
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False; ws.column_dimensions["A"].width = 100
    linhas = [
        ("ZION HOSPITALITY BUSINESS · JORNADA 2 · GESTÃO · MÓDULO 4 · MARKETING E VENDAS", T(10, True, DOURADO)),
        ("Plano de Captação", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para escrever a marca da sua hospedagem em uma folha, começar a lista própria de contatos com autorização e saber quanto custa cada reserva em cada canal.", T(11, c="2D352A")),
        ("EXEMPLO DIDÁTICO PREENCHIDO COM DADOS FICTÍCIOS (Cabanas do Vale). Use a versão em branco para os seus números." if exemplo else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("", None),
        ("COMO USAR EM 4 PASSOS (cerca de 25 minutos na primeira vez; depois, dois minutos por estadia e dez minutos por mês)", T(12, True, MUSGO)),
        ("1. Aba Marca em uma folha: para quem, a promessa em uma frase (com os quatro testes e o teste das cinco pessoas), a prova, o tom e onde a promessa já aparece.", None),
        ("2. Aba Captação do mês: cada canal com reservas, receita de hospedagem, comissão e o que você gastou para trazer o hóspede. A planilha calcula o custo por reserva e a venda direta, e confere a meta.", None),
        ("3. Aba Lista própria: uma linha por estadia, preenchida no dia da saída, com a autorização (Sim ou Não). Só quem disse Sim recebe comunicação.", None),
        ("4. Aba Captação 12 meses: no fim de cada mês, lance o total do mês. A planilha diz se a venda direta está na meta.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("O QUE A PLANILHA FAZ E O QUE ELA NÃO FAZ", T(12, True, MUSGO)),
        ("Faz: guarda a marca em uma folha (Pilar G1 do Método Zion e Etapa 05), calcula o custo por reserva de cada canal (Pilar G4: quanto você gastou dividido por quantas reservas vieram daquele esforço), a venda direta e o ritmo da lista.", None),
        ("Não faz: não prevê reservas, não envia mensagens e não conhece as regras de cada plataforma. Confira as regras da plataforma antes de pedir contato a quem reservou por ela, e procure um profissional habilitado para dúvidas sobre proteção de dados.", None),
        ("Percentuais: escreva 16 para 16% (sem o símbolo). Taxa de cartão e imposto ficam na Folha Única do Mês (Módulo 2), não aqui.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Material educativo: não é promessa de renda, retorno, ocupação, reservas ou resultado. O resultado depende da execução de cada hospedagem.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Marca em uma folha ----------
    m = wb.create_sheet("Marca em uma folha"); m.sheet_view.showGridLines = False
    for col, w in zip("ABC", (40, 70, 44)): m.column_dimensions[col].width = w
    m["A1"] = "A marca em uma folha"; m["A1"].font = T(18, True, MUSGO)
    m["A2"] = "EXEMPLO DIDÁTICO · dados fictícios (Cabanas do Vale)" if exemplo else "Preencha as células amarelas. Células em verde são calculadas."; m["A2"].font = T(10, True, "A0522D" if exemplo else DOURADO)
    e = EX_MARCA if exemplo else {}
    faixa(m, 3, "1 · PARA QUEM E A PROMESSA")
    rotulo(m, 4, "Para quem é a sua hospedagem", "Quem é, dito com clareza."); entrada(m, 4, e.get("publico"))
    rotulo(m, 5, "Para quem não é (opcional)", "Uma hospedagem que aceita tudo não promete nada."); entrada(m, 5, e.get("nao"))
    rotulo(m, 6, "A promessa, em uma frase", "Ocasião + o que acontece + o que torna possível. Sem adjetivo genérico."); entrada(m, 6, e.get("promessa"))
    testes = ["Teste da recusa: alguém entende que não é para ele?", "Teste do cumprimento: entrego isso toda vez?", "Teste da diferença: o vizinho NÃO poderia dizer o mesmo?", "Teste da memória: alguém repetiria a frase?"]
    for k, tx in enumerate(testes):
        rotulo(m, 7 + k, tx, "Sim ou Não."); entrada(m, 7 + k, e["testes"][k] if exemplo else None)
    rotulo(m, 11, "Quantas de cinco pessoas de fora entenderam sem perguntar", "0 a 5. Em branco = ainda não testei."); entrada(m, 11, e.get("cinco"), "0")
    faixa(m, 12, "2 · A PROVA, O TOM E O QUE NUNCA FAZEMOS")
    rotulo(m, 13, "A foto (ou a prova) que mostra a promessa", "A foto de capa tem que mostrar o que a frase diz."); entrada(m, 13, e.get("prova"))
    rotulo(m, 14, "O tom de voz, em três palavras", "Formal ou próximo; descritivo ou evocativo."); entrada(m, 14, e.get("tom"))
    rotulo(m, 15, "Palavras que nunca escrevemos (opcional)", "Comece pelos adjetivos genéricos."); entrada(m, 15, e.get("banidas"))
    rotulo(m, 16, "O que nunca fazemos (opcional)"); entrada(m, 16, e.get("nunca"))
    faixa(m, 17, "3 · ONDE A PROMESSA JÁ APARECE (Já aparece, Não aparece, Não tenho)")
    for k, pt in enumerate(PONTOS):
        rotulo(m, 18 + k, pt); entrada(m, 18 + k, e["pontos"][k] if exemplo else None)
    faixa(m, 25, "4 · CONFERÊNCIA")
    rotulo(m, 26, "Testes com Sim"); calc(m, 26, '=COUNTIF(B7:B10,"Sim")&" de 4"', "@")
    adj = '{"aconchegante","único","única","especial","exclusiv","inesquecível","incrível","perfeit"}'
    rotulo(m, 27, "Adjetivo genérico na promessa?"); calc(m, 27, f'=IF(B6="","",IF(SUMPRODUCT(--ISNUMBER(SEARCH({adj},B6)))>0,"Atenção: troque o adjetivo por uma coisa concreta","OK: sem adjetivo genérico"))', "@")
    rotulo(m, 28, "Pontos de contato onde a promessa falta"); calc(m, 28, '=COUNTIF(B18:B23,"Não aparece")', "0")
    rotulo(m, 29, "Situação da folha")
    situacao(m, "B29", '=IF(OR(B4="",B6="",B13="",B14=""),"Preencha para quem, promessa, prova e tom",'
                       'IF(COUNTIF(B7:B10,"Sim")+COUNTIF(B7:B10,"Não")<4,"Responda os quatro testes",'
                       'IF(COUNTIF(B7:B10,"Não")>0,"Reescreva a promessa: ela falhou em algum teste",'
                       'IF(B11="","Teste a promessa com cinco pessoas de fora",'
                       'IF(B11<5,"Reescreva: nem todos entenderam (a frase ainda não existe)",'
                       'IF(COUNTA(B18:B23)<6,"Marque os seis pontos de contato","OK"))))))')
    m.cell(31, 1, "Fontes Zion: Panorama, Trilha B, Pilar G1 Marca e Narrativa; Jornada do COMO, Etapa 05 (Frase de Promessa, Guia de Tom de Voz e Marca em Uma Folha, com as nove linhas completas).").font = T(9, c="5F5F55", i=True)
    dvt = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); m.add_data_validation(dvt); dvt.add("B7:B10")
    dvc = DataValidation(type="whole", operator="between", formula1="0", formula2="5", allow_blank=True, showErrorMessage=True, error="De 0 a 5."); m.add_data_validation(dvc); dvc.add("B11")
    dvp = DataValidation(type="list", formula1='"Já aparece,Não aparece,Não tenho"', allow_blank=True); m.add_data_validation(dvp); dvp.add("B18:B23")
    for l in (4, 5, 6, 13, 15, 16): m.row_dimensions[l].height = 36

    # ---------- Captação do mês ----------
    c = wb.create_sheet("Captação do mês"); c.sheet_view.showGridLines = False
    c["A1"] = "Captação do mês · o custo por reserva de cada canal"; c["A1"].font = T(16, True, MUSGO)
    c["A2"] = "EXEMPLO DIDÁTICO · dados fictícios (Cabanas do Vale)" if exemplo else "Custo por reserva = (comissão da plataforma + o que você gastou) ÷ reservas daquele canal."; c["A2"].font = T(10, True, "A0522D" if exemplo else DOURADO)
    rotulo(c, 4, "Mês"); entrada(c, 4, EX_MES if exemplo else None)
    cabecalho(c, 6, ["Canal", "Tipo (Plataforma ou Direto)", "Comissão (%)", "Gasto no mês (R$)", "Reservas", "Receita de hospedagem (R$)", "Comissão (R$)", "Custo de captação (R$)", "Custo por reserva (R$)", "Custo ÷ receita do canal"],
              [34, 16, 12, 14, 11, 17, 14, 15, 15, 14], 44)
    for l in range(C0, C1 + 1):
        for col, f in zip(range(1, 7), ["@", "@", PCT, BRL, "0", BRL]):
            entrada(c, l, None, f, col)
        calc(c, l, f'=IF(B{l}="Plataforma",F{l}*C{l}/100,0)', BRL, False, 7)
        calc(c, l, f'=IF(A{l}="","",G{l}+D{l})', BRL, False, 8)
        calc(c, l, f'=IF(OR(A{l}="",E{l}="",E{l}=0),"",H{l}/E{l})', BRL, False, 9)
        calc(c, l, f'=IF(OR(A{l}="",F{l}="",F{l}=0),"",H{l}/F{l})', PCTF, False, 10)
    if exemplo:
        for i, row in enumerate(EX_CANAIS):
            for col, v in enumerate(row, 1): c.cell(C0 + i, col, v)
    T0 = C1 + 1
    c.cell(T0, 1, "Total").font = T(11, True)
    for col, f in ((5, "0"), (6, BRL), (7, BRL), (8, BRL)):
        L = c.cell(1, col).column_letter; calc(c, T0, f"=SUM({L}{C0}:{L}{C1})", f, True, col)
    calc(c, T0, f'=IF(E{T0}=0,"",H{T0}/E{T0})', BRL, True, 9); calc(c, T0, f'=IF(F{T0}=0,"",H{T0}/F{T0})', PCTF, True, 10)
    dvtipo = DataValidation(type="list", formula1='"Plataforma,Direto"', allow_blank=True); c.add_data_validation(dvtipo); dvtipo.add(f"B{C0}:B{C1}")
    faixa(c, 17, "VENDA DIRETA E META", 4)
    rg = f"B{C0}:B{C1}"
    rotulo(c, 18, "Receita de hospedagem direta (R$)"); calc(c, 18, f'=SUMIF({rg},"Direto",F{C0}:F{C1})', BRL)
    rotulo(c, 19, "Reservas diretas"); calc(c, 19, f'=SUMIF({rg},"Direto",E{C0}:E{C1})', "0")
    rotulo(c, 20, "Venda direta (parte da receita)", "Definição do Painel (Módulo 1)."); calc(c, 20, f'=IF(F{T0}=0,"",B18/F{T0})', PCTF, True)
    rotulo(c, 21, "Venda direta (parte das reservas)", "Como mede a Etapa 07."); calc(c, 21, f'=IF(E{T0}=0,"",B19/E{T0})', PCTF)
    rotulo(c, 22, "Comissão média das plataformas"); calc(c, 22, f'=IF(SUMIF({rg},"Plataforma",F{C0}:F{C1})=0,"",SUMIF({rg},"Plataforma",G{C0}:G{C1})/SUMIF({rg},"Plataforma",F{C0}:F{C1}))', PCTF)
    rotulo(c, 23, "Captação sobre a receita de hospedagem"); calc(c, 23, f'=IF(F{T0}=0,"",H{T0}/F{T0})', PCTF)
    rotulo(c, 24, "Meta de venda direta (%)", "A mesma do seu Painel de Gestão."); entrada(c, 24, EX_META[0] if exemplo else None, PCT)
    rotulo(c, 25, "Até quando", "Data."); entrada(c, 25, EX_META[1] if exemplo else None)
    rotulo(c, 26, "Venda direta que a meta pede num mês com a mesma receita (R$)"); calc(c, 26, f'=IF(OR(B24="",F{T0}=0),"",F{T0}*B24/100)', BRL, True)
    rotulo(c, 27, "Comissão que deixaria de sair nesse mês (R$)", "Conta com os seus números, não previsão."); calc(c, 27, f'=IF(OR(B26="",B22=""),"",MAX(0,B26-B18)*B22)', BRL)
    rotulo(c, 28, "Canal com o menor custo por reserva"); calc(c, 28, f'=IF(COUNT(I{C0}:I{C1})=0,"",INDEX(A{C0}:A{C1},MATCH(MIN(I{C0}:I{C1}),I{C0}:I{C1},0)))', "@")
    rotulo(c, 29, "Canal com o maior custo por reserva"); calc(c, 29, f'=IF(COUNT(I{C0}:I{C1})=0,"",INDEX(A{C0}:A{C1},MATCH(MAX(I{C0}:I{C1}),I{C0}:I{C1},0)))', "@")
    rotulo(c, 30, "Meta × venda direta de hoje"); calc(c, 30, f'=IF(OR(B24="",B20=""),"",IF(B24/100<=B20,"Atenção: a meta não passa da venda direta de hoje","OK: meta acima da venda direta de hoje"))', "@")
    rotulo(c, 32, "Situação dos dados")
    sp = (f'=IF(B4="","Preencha o mês",'
          f'IF(COUNTA(A{C0}:A{C1})=0,"Preencha pelo menos um canal",'
          f'IF(SUMPRODUCT((A{C0}:A{C1}<>"")*(B{C0}:B{C1}<>"Plataforma")*(B{C0}:B{C1}<>"Direto"))>0,"Escolha Plataforma ou Direto em cada canal",'
          f'IF(SUMPRODUCT((A{C0}:A{C1}="")*((E{C0}:E{C1}<>"")+(F{C0}:F{C1}<>"")+(D{C0}:D{C1}<>"")))>0,"Dê nome ao canal ou apague a linha",'
          f'IF(SUMPRODUCT((A{C0}:A{C1}<>"")*((E{C0}:E{C1}="")+(F{C0}:F{C1}="")))>0,"Faltam reservas ou receita em algum canal (0 vale)",'
          f'IF(OR(MIN(D{C0}:F{C1})<0,MAX(C{C0}:C{C1})>=100),"Valor negativo ou comissão de 100% ou mais",'
          f'IF(SUMPRODUCT((E{C0}:E{C1}<>"")*(E{C0}:E{C1}<>INT(E{C0}:E{C1}+0)))>0,"Reservas: número inteiro",'
          f'IF(SUMPRODUCT((A{C0}:A{C1}<>"")*(E{C0}:E{C1}=0)*(F{C0}:F{C1}>0))>0,"Há receita sem reserva em algum canal",'
          f'IF(OR(E{T0}=0,F{T0}=0),"Sem reservas ou sem receita no mês",'
          f'IF(OR(B24="",B24<=0,B24>100),"Escreva a meta de venda direta (de 0 a 100)","OK"))))))))))')
    situacao(c, "B32", sp, "B32:F32")
    c.cell(34, 1, "Taxa de cartão e imposto ficam fora: estão na Folha Única do Mês (Módulo 2). Aqui entra só o que custou trazer o hóspede. Fonte Zion: Panorama, Trilha B, Pilares G2 e G4.").font = T(9, c="5F5F55", i=True)

    # ---------- Lista própria ----------
    li = wb.create_sheet("Lista própria"); li.sheet_view.showGridLines = False; li.freeze_panes = f"A{L0}"
    li["A1"] = "Lista própria · uma linha por estadia, preenchida no dia da saída" + ("  ·  EXEMPLO FICTÍCIO" if exemplo else ""); li["A1"].font = T(14, True, MUSGO)
    el = EX_LISTA if exemplo else {}
    rotulo(li, 2, "Frase de autorização (check-in)"); entrada(li, 2, el.get("frase")); li.merge_cells("B2:E2"); li.row_dimensions[2].height = 34
    rotulo(li, 3, "Onde a lista fica (e a cópia)"); entrada(li, 3, el.get("onde")); li.merge_cells("B3:E3")
    rotulo(li, 4, "Quem mais tem acesso"); entrada(li, 4, el.get("acesso")); li.merge_cells("B4:E4")
    rotulo(li, 5, "Canal para fazer bem"); entrada(li, 5, el.get("canal"))
    rotulo(li, 6, "Contatos guardados antes, sem autorização registrada"); entrada(li, 6, el.get("antes"), "0")
    rotulo(li, 7, "Meta de contatos com autorização em 12 meses"); entrada(li, 7, el.get("meta"), "0")
    rotulo(li, 8, "Estadias num mês típico"); entrada(li, 8, el.get("estadias"), "0")
    for l, (t, f, fm) in enumerate([("Contatos (antes + linhas abaixo)", f'=N(B6)+COUNTA(A{L0}:A{L1})', "0"), ("Com autorização (Sim)", f'=COUNTIF(I{L0}:I{L1},"Sim")', "0"),
                                    ("Faltam para a meta", '=IF(B7="","",MAX(0,B7-H3))', "0"), ("Autorizações por mês para chegar", '=IF(H4="","",H4/12)', "0.0"),
                                    ("Parte das estadias do mês", '=IF(OR(H5="",N(B8)=0),"",H5/B8)', "0%")], 2):
        li.cell(l, 7, t).font = T(10, True); calc(li, l, f, fm, l == 3, 8)
    li.cell(7, 7, "Leitura").font = T(10, True)
    calc(li, 7, '=IF(OR(H6="",B7=""),"",IF(H6>1,"Atenção: a meta pede mais autorizações que estadias","OK: o ritmo cabe nas estadias"))', "@", False, 8)
    li.cell(8, 7, "Situação").font = T(10, True)
    situacao(li, "H8", '=IF(OR(B2="",B3="",B5="",B7="",B8=""),"Preencha a frase, o lugar, o canal, a meta e as estadias",IF(OR(N(B7)<1,N(B8)<1),"Meta e estadias a partir de 1",IF(B7<H3,"A meta é menor que os autorizados de hoje",IF(COUNTIFS(A' + str(L0) + ':A' + str(L1) + ',"<>",I' + str(L0) + ':I' + str(L1) + ',"")>0,"Falta a autorização (Sim ou Não) em alguma linha","OK"))))')
    li.cell(10, 1, "Só quem disse Sim recebe comunicação. Quem disse Não fica só no histórico. Antes de pedir contato a quem reservou por uma plataforma, confira as regras dela.").font = T(9, c="5F5F55", i=True)
    li.cell(11, 1, "Para quem já veio, você lembra; para quem nunca veio, você precisa provar (Pilar G4). Quatro contatos por ano, no máximo (Etapa 07).").font = T(9, c="5F5F55", i=True)
    cabecalho(li, 13, ["Nome", "Telefone (WhatsApp)", "E-mail", "Entrada", "Saída", "Pessoas", "Como chegou", "Observação", "Autorização (Sim ou Não)", "Voltou? (já veio antes)"], [30, 18, 26, 12, 12, 9, 22, 34, 14, 14], 40)
    for l in range(L0, L1 + 1):
        for col in range(1, 11): entrada(li, l, None, "0" if col == 6 else "@", col)
    dva = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); li.add_data_validation(dva); dva.add(f"I{L0}:J{L1}")
    dvg = DataValidation(type="list", formula1='"Achei na plataforma,Alguém me indicou,Já me hospedei antes,Procurei o nome,Redes sociais,Outro"', allow_blank=True); li.add_data_validation(dvg); dvg.add(f"G{L0}:G{L1}")

    # ---------- Captação 12 meses ----------
    p = wb.create_sheet("Captação 12 meses"); p.sheet_view.showGridLines = False
    p["A1"] = "Captação 12 meses · uma linha por mês" + ("  ·  EXEMPLO FICTÍCIO" if exemplo else ""); p["A1"].font = T(14, True, MUSGO)
    p["A2"] = "A meta vem da aba Captação do mês (célula B24). Compare sempre o mesmo mês do ano seguinte."; p["A2"].font = T(9, c="5F5F55", i=True)
    cabecalho(p, 4, ["Mês", "Receita de hospedagem (R$)", "Receita direta (R$)", "Reservas", "Custo de captação (R$)", "Contatos com autorização no fim do mês", "Venda direta", "Custo por reserva (R$)", "Meta"], [26, 16, 15, 11, 16, 16, 12, 15, 22], 44)
    for l in range(5, 17):
        for col, f in zip(range(1, 7), ["@", BRL, BRL, "0", BRL, "0"]): entrada(p, l, None, f, col)
        calc(p, l, f'=IF(OR(B{l}="",N(B{l})=0),"",C{l}/B{l})', PCTF, False, 7)
        calc(p, l, f'=IF(OR(D{l}="",N(D{l})=0),"",E{l}/D{l})', BRL, False, 8)
        calc(p, l, f"=IF(OR(G{l}=\"\",'Captação do mês'!B24=\"\"),\"\",IF(G{l}*100>='Captação do mês'!B24,\"Na meta\",\"Abaixo da meta\"))", "@", False, 9)
    if exemplo:
        for i, row in enumerate(EX_12):
            for col, v in enumerate(row, 1): p.cell(5 + i, col, v)
    p.conditional_formatting.add("I5:I16", FormulaRule(formula=['I5="Abaixo da meta"'], font=Font(color="9B2C1F", bold=True)))
    p.conditional_formatting.add("I5:I16", FormulaRule(formula=['I5="Na meta"'], font=Font(color="1F5A33", bold=True)))

    # ---------- Definições e rotina ----------
    d = wb.create_sheet("Definições e rotina"); d.sheet_view.showGridLines = False
    for col, w in zip("ABC", (32, 70, 46)): d.column_dimensions[col].width = w
    d["A1"] = "Definições, os quatro contatos do ano e a rotina"; d["A1"].font = T(14, True, MUSGO)
    cabecalho(d, 3, ["Termo", "Definição", "Fonte"])
    defs = [("Marca", "A razão declarada que faz alguém pagar mais na sua casa do que na do vizinho, e a forma como ela aparece antes da reserva.", "Panorama, Pilar G1"),
            ("Promessa", "O que o hóspede vive, em uma frase: ocasião, o que acontece e o que torna aquilo possível. Sem adjetivo genérico.", "Etapa 05, Passo 02"),
            ("Lista própria", "Contatos de hóspedes com autorização explícita para receber comunicação, guardados fora do celular e com cópia.", "Panorama, Pilar G4; Etapa 07, Passo 07"),
            ("Custo por reserva", "Quanto você gastou num esforço (comissão da plataforma ou gasto do canal direto) dividido por quantas reservas vieram dele.", "Pilar G4, passo 04 (comissão como gasto: elaboração)"),
            ("Venda direta", "Parte da receita de hospedagem que entrou sem plataforma (definição do Painel, Módulo 1). A planilha mostra também a parte das reservas.", "Definição-padrão de hotelaria; Etapa 07")]
    for k, row in enumerate(defs):
        for col, v in enumerate(row, 1):
            x = d.cell(4 + k, col, v); x.alignment = Alignment(wrap_text=True, vertical="top"); x.border = borda
        d.row_dimensions[4 + k].height = 44
    faixa(d, 10, "OS QUATRO CONTATOS DO ANO (só para quem autorizou, sempre com o caminho de reserva direta)", 3)
    cont = [("Agradecimento", "Na saída ou no dia seguinte. Não vende nada e é onde se pede a avaliação (Kit de Mensagens, M08)."),
            ("Aniversário da estadia", "Seis a oito semanas antes de completar um ano da estadia."),
            ("Abertura de temporada", "Duas a três vezes por ano, antes do público geral saber das datas."),
            ("Oferta de baixa", "Nos meses fracos, com condição real, nunca abaixo do piso (Módulo 3).")]
    for i, (a, b) in enumerate(cont):
        d.cell(11 + i, 1, a).font = T(10, True); x = d.cell(11 + i, 2, b); x.alignment = Alignment(wrap_text=True); d.merge_cells(start_row=11 + i, start_column=2, end_row=11 + i, end_column=3)
    faixa(d, 16, "A ROTINA", 3)
    rot = [("A cada check-in", "Pedir o contato com a frase de autorização e perguntar como a pessoa chegou."),
           ("A cada saída · 2 minutos", "Preencher a linha da estadia na aba Lista própria."),
           ("Todo mês · 10 minutos", "Lançar os canais na aba Captação do mês e o total na aba Captação 12 meses; conferir a venda direta contra a meta."),
           ("Uma vez por ano", "Revisar a marca em uma folha e comparar com o que acontece de fato.")]
    for i, (a, b) in enumerate(rot):
        d.cell(17 + i, 1, a).font = T(10, True); x = d.cell(17 + i, 2, b); x.alignment = Alignment(wrap_text=True); d.merge_cells(start_row=17 + i, start_column=2, end_row=17 + i, end_column=3)
    d.cell(22, 1, "Fontes Zion: Panorama do Desenvolvimento Hoteleiro (Trilha B, Pilares G1, G2 e G4); Jornada do COMO, Etapas 05 e 07. Material educacional: não é promessa de renda, retorno, ocupação, reservas ou resultado.").font = T(9, c="5F5F55", i=True)
    wb.active = 0
    return wb

for exemplo, nome in ((False, "Plano-de-Captacao-Zion-EM-BRANCO.xlsx"), (True, "Plano-de-Captacao-Zion-EXEMPLO.xlsx")):
    montar(exemplo).save(OUT / nome); print("ok", OUT / nome)

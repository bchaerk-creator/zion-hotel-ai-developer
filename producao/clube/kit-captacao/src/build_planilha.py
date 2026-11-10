"""Kit Inicial · Como captar recursos para o seu projeto (Club Zion Collection).
Gera a planilha "Mapa das Fontes de Capital" em duas versões:
   - Mapa-das-Fontes-de-Capital-Zion-EM-BRANCO.xlsx
   - Mapa-das-Fontes-de-Capital-Zion-EXEMPLO.xlsx (dados fictícios)
Molde: producao/low-ticket/01-diaria-minima/build_planilha.py (amarelo = você preenche, verde = calculado).
Fontes do conteúdo: Z02 Cap. 5 (Mapa das Seis Fontes, Régua do Quanto Captar), F00 Cap. 5 (portão do capital),
F05 Cap. 1, F06 Caps. 1 e 4, ferramentas B04 e B02 do Zion Arsenal.
Uso: python3 -I build_planilha.py <pasta-saida>"""
import sys, pathlib, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, AREIA, TERRA, PRETO, CREME = "1B2117", "DED6BF", "8B714E", "040605", "FEF5F0"
ENTRADA = PatternFill("solid", fgColor="FFF4C7")   # amarelo claro = você preenche
CALC = PatternFill("solid", fgColor="E3EEDF")      # verde claro = calculado
CAB = PatternFill("solid", fgColor=MUSGO)
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
BRL = 'R$ #,##0.00;[Red]-R$ #,##0.00'; PCT = '0.0%'; X = '0.00"×"'; DATA = 'DD/MM/YYYY'
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)
WRAP = Alignment(wrap_text=True, vertical="center")

FONTES = [
    ("1 · Capital próprio e etapa menor",
     "Saber o seu limite de perda e desenhar a etapa 1 como o menor conjunto que já opera e gera caixa, com o projeto inteiro pensado.",
     "Não cobra juro nem participação, mas concentra todo o risco em você. Use só o que é contratado, não esperado."),
    ("2 · Banco, cooperativa e fomento",
     "Fluxo (capacidade de pagar a parcela) e ativo (garantia real com matrícula limpa). Proposta sempre por escrito.",
     "Parcela todo mês, inclusive na obra. Garantia real e às vezes aval pessoal. Fomento: desembolso lento, procure com antecedência."),
    ("3 · Sócio que entra com capital",
     "Projeto que se audita numa tarde: território, mercado, produto e conta com fonte. Ele compra tese e execução.",
     "Leva resultado, decisão, informação e a sua saída. Nada disso se desfaz depois sem comprar de volta."),
    ("4 · Sócio operador ou arrendamento",
     "Papéis claros: quem opera recebe remuneração de mercado; quem aporta terra ou capital recebe participação. No arrendamento, contrato longo.",
     "Trabalho não vira participação sem regra escrita. No arrendamento você troca potencial por previsibilidade e o destino das benfeitorias precisa estar no contrato."),
    ("5 · Permuta e parcerias com construtor",
     "Projeto estruturado e avaliação da terra aceita pelos dois lados (laudo). Definição precisa do que cada parte recebe.",
     "Você cede parte da área, das unidades ou da receita. Avaliação mal feita é o risco principal."),
    ("6 · Pessoa do círculo e venda antecipada",
     "Contrato escrito, com as mesmas cláusulas que você exigiria de um desconhecido. Na venda antecipada, projeto e licença.",
     "A relação fica em jogo. Pré-venda não é receita: é um passivo com cara de caixa, e atraso na entrega custa reputação."),
]
PRONTIDAO = [
    ("Tenho a certidão de matrícula atualizada e sei se há pendência (inventário, escritura, posse).", "F05 Cap. 1 e B04: o ativo se verifica com matrícula, laudo e licenças."),
    ("Li o território: acesso, entorno, o que atrai visitantes e o que limita o uso da área.", "F06 Cap. 1: território lido é a primeira das seis coisas que o capital procura."),
    ("Sei qual diária o destino sustenta, com dado coletado (concorrentes, meses), e não estimativa.", "F06 Cap. 1: segunda das três perguntas do capital."),
    ("Sei o que construir na etapa 1: quantas unidades e para quem.", "F06 Cap. 1: primeira das três perguntas do capital."),
    ("Tenho orçamento da etapa 1 por escrito, com data, e a conta completa com giro e reserva.", "F00 Cap. 5: condição 2 do portão do capital."),
    ("Rodei o cenário conservador e ele paga as contas da etapa 1.", "F00 Cap. 5: condição 3 do portão do capital."),
    ("Escrevi o meu limite de perda e sei o que fica em risco (garantia real ou aval pessoal).", "Z02 Cap. 5 e F00 Cap. 5: condição 4 do portão."),
    ("Nomeei a fonte e tenho a proposta por escrito, com o que ela cobra além do juro.", "F00 Cap. 5: condição 5 do portão (Custo Real do Capital)."),
    ("Dinheiro de pessoa próxima só entra com contrato escrito.", "F00 Cap. 5: sinal vermelho 8."),
    ("As contas do projeto estão separadas das contas pessoais.", "F00 Cap. 5: sinal vermelho 11 (Linha de Separação Zion)."),
]

def faixa(ws, linha, texto, cols=3):
    ws.merge_cells(start_row=linha, start_column=1, end_row=linha, end_column=cols)
    c = ws.cell(linha, 1, texto); c.font = T(11, True, CREME); c.fill = CAB; c.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[linha].height = 22

def rotulo(ws, l, texto, ajuda=""):
    a = ws.cell(l, 1, texto); a.font = T(11); a.alignment = WRAP
    if ajuda: h = ws.cell(l, 3, ajuda); h.font = T(9, c="5F5F55", i=True); h.alignment = WRAP
    ws.row_dimensions[l].height = 32

def entrada(ws, ref, valor=None, fmt=BRL):
    c = ws[ref]; c.value = valor; c.fill = ENTRADA; c.border = borda; c.number_format = fmt; c.font = T(11, True); c.alignment = WRAP; return c

def calc(ws, ref, formula, fmt=BRL, destaque=False):
    c = ws[ref]; c.value = formula; c.fill = CALC; c.border = borda; c.number_format = fmt
    c.font = T(13 if destaque else 11, True, MUSGO if destaque else PRETO); c.alignment = WRAP; return c

def titulo(ws, txt, sub):
    ws["A1"] = "CLUB ZION COLLECTION · KIT INICIAL DE CAPTAÇÃO"; ws["A1"].font = T(9, True, TERRA)
    ws["A2"] = txt; ws["A2"].font = T(18, True, MUSGO)
    ws["A3"] = sub; ws["A3"].font = T(10, c="2D352A", i=True)

def montar(ex):
    wb = Workbook()
    # ---------------- Comece aqui ----------------
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False; ws.column_dimensions["A"].width = 110
    L = [
        ("CLUB ZION COLLECTION · KIT INICIAL · COMO CAPTAR RECURSOS PARA O SEU PROJETO", T(10, True, TERRA)),
        ("Mapa das Fontes de Capital", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para saber quanto falta na etapa 1, quais fontes fazem sentido para o seu caso, o que cada uma pede e qual é o seu próximo passo, com data.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (Sítio Exemplo). Use a versão em branco para o seu projeto." if ex else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if ex else MUSGO)),
        ("", None),
        ("COMO USAR EM 4 PASSOS (cerca de 30 minutos)", T(12, True, MUSGO)),
        ("1. Aba Necessidade: preencha o custo da etapa 1, o giro, a reserva e o custo da captação. A planilha mostra o total e a lacuna (o que falta).", None),
        ("2. Aba Fontes: marque cada uma das seis fontes como Disponível, Possível ou Fora, com uma linha de justificativa. \"Fora também é informação.\"", None),
        ("3. Aba Prontidão: responda os 10 itens com Sim ou Não. Um Não basta para estruturar antes de captar.", None),
        ("4. Aba Próximos passos: escreva até 5 ações com data. A primeira pode ser agendar a sua sessão de direcionamento com a equipe Zion.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("O QUE A PLANILHA FAZ E O QUE ELA NÃO FAZ", T(12, True, MUSGO)),
        ("Faz: organiza a conta do quanto falta (Régua do Quanto Captar), compara as seis fontes pelo que cada uma pede e leva, calcula quanto de crédito caberia numa parcela que você mesmo simulou e mostra se você está pronto para conversar com capital de terceiros.", None),
        ("Não faz: não indica banco, linha de crédito, taxa ou investidor; não avalia a sua terra; não substitui advogado, contador ou avaliador. A taxa usada no crédito é a da simulação que VOCÊ fez numa instituição.", None),
        ("", None),
        ("AVISO", T(12, True, MUSGO)),
        ("Material educativo da Zion Hotel Group International. Não é promessa de crédito, investidor, sociedade, renda ou retorno. Conversar não é captar: a decisão de emprestar ou investir é de quem empresta ou investe, e a Zion avalia cada caso.", None),
        ("Fontes do método: Z02 (Mapa das Seis Fontes e Régua do Quanto Captar), F00 (portão do capital), F05 (o que o banco compra), F06 (sócios), ferramentas B04 e B02.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(L, 1):
        c = ws.cell(i, 1, t); c.alignment = Alignment(wrap_text=True, vertical="top")
        if f: c.font = f
        else: c.font = T(11)

    # ---------------- Necessidade ----------------
    n = wb.create_sheet("Necessidade"); n.sheet_view.showGridLines = False
    n.column_dimensions["A"].width = 52; n.column_dimensions["B"].width = 20; n.column_dimensions["C"].width = 62
    titulo(n, "1 · Quanto falta na etapa 1", "Régua do Quanto Captar (Z02 Cap. 5): quatro linhas de necessidade e duas de ajuste. O número vai exato, não redondo." + ("  ·  DADOS FICTÍCIOS" if ex else ""))
    faixa(n, 4, "A conta da etapa 1")
    rows = [
        (5, "CAPEX da etapa 1 (obra, estrutura, mobília até o primeiro hóspede)", "Use orçamento escrito, com data de cada cotação.", 240000),
        (6, "Terreno ainda não pago", "Se a terra já é sua, escreva 0 (e deixe isso escrito).", 0),
        (7, "Custo fixo mensal previsto da operação", "Base do capital de giro.", 9000),
        (8, "Meses de custo fixo na reserva de giro", "A Régua usa 3 meses.", 3),
        (9, "Necessidade técnica da rampa (meses negativos do início)", "Se não souber, deixe 0 e anote como pendência.", 12000),
    ]
    for l, t, a, v in rows:
        rotulo(n, l, t, a); entrada(n, f"B{l}", v if ex else None, '0' if l == 8 else BRL)
    rotulo(n, 10, "Capital de giro", "= custo fixo × meses + necessidade técnica.")
    calc(n, "B10", '=IF(AND(B7="",B9=""),"",N(B7)*IF(B8="",3,B8)+N(B9))')
    rotulo(n, 11, "Reserva de implantação (% do CAPEX)", "De 10% a 15%, com regra de uso escrita.")
    entrada(n, "B11", 0.12 if ex else None, PCT)
    rotulo(n, 12, "Reserva de implantação (R$)", "= CAPEX × percentual.")
    calc(n, "B12", '=IF(OR(B5="",B11=""),"",B5*B11)')
    rotulo(n, 13, "Custo da própria captação (jurídico, laudos, registro)", "Orçamento escrito. A fonte cita de 2% a 5% do valor captado.")
    entrada(n, "B13", 7200 if ex else None)
    rotulo(n, 14, "TOTAL NECESSÁRIO", "CAPEX + terreno + giro + reserva + captação.")
    calc(n, "B14", '=IF(B5="","",B5+N(B6)+N(B10)+N(B12)+N(B13))', destaque=True)
    rotulo(n, 15, "Capital próprio CONTRATADO (já seu, não esperado)", "Promessa de parente não conta. Pode ser zero.")
    entrada(n, "B15", 3000 if ex else None)
    rotulo(n, 16, "LACUNA (o que precisa vir de outras fontes)", "= total − capital próprio contratado.")
    calc(n, "B16", '=IF(B14="","",MAX(0,B14-N(B15)))', destaque=True)
    rotulo(n, 17, "Cobertura própria", "Quanto do total você cobre hoje.")
    calc(n, "B17", '=IF(OR(B14="",B14=0),"",N(B15)/B14)', PCT)
    rotulo(n, 18, "Pedido incompleto (só CAPEX − capital próprio)", "O que muita gente pede. A diferença para a lacuna é o que faltaria no meio do caminho.")
    calc(n, "B18", '=IF(B5="","",MAX(0,B5+N(B6)-N(B15)))')
    rotulo(n, 19, "O que faltaria no meio do caminho", "= lacuna − pedido incompleto.")
    calc(n, "B19", '=IF(B16="","",B16-B18)')
    faixa(n, 21, "A terra como ativo de negociação (não é dinheiro)")
    rotulo(n, 22, "Valor de referência da terra", "Laudo é a referência mais sólida; corretores, intermediária; estimativa própria, a mais frágil (B02).")
    entrada(n, "B22", 200000 if ex else None)
    rotulo(n, 23, "Terra ÷ lacuna", "Peso da terra frente ao que falta (B04). Ela não reduz a lacuna: entra na negociação.")
    calc(n, "B23", '=IF(OR(B22="",B16="",N(B16)=0),"",B22/B16)', X)
    faixa(n, 25, "Crédito: quanto da lacuna caberia numa parcela que você aguenta")
    rotulo(n, 26, "Parcela mensal que você pagaria com folga", "Com a renda dos meses mais fracos. Pode ser zero.")
    entrada(n, "B26", 1500 if ex else None)
    rotulo(n, 27, "Taxa ao mês da SUA simulação (banco ou cooperativa)", "A planilha não indica taxa. Use a da proposta que você recebeu." + (" No exemplo: taxa fictícia." if ex else ""))
    entrada(n, "B27", 0.015 if ex else None, '0.00%')
    rotulo(n, 28, "Prazo da simulação (meses)", "")
    entrada(n, "B28", 120 if ex else None, '0')
    rotulo(n, 29, "Valor financiável com essa parcela", "= parcela × [1 − (1 + taxa)^−prazo] ÷ taxa (B04).")
    calc(n, "B29", '=IF(AND(N(B26)>0,N(B27)>0,N(B28)>0),B26*(1-(1+B27)^(-B28))/B27,"")', destaque=True)
    rotulo(n, 30, "Parte da lacuna que esse crédito cobriria", "")
    calc(n, "B30", '=IF(OR(B29="",B16=""),"",MIN(B29,B16))')
    rotulo(n, 31, "Atenção", "")
    calc(n, "B31", '=IF(B29="","Preencha parcela, taxa e prazo da sua simulação","Teste de fôlego: a parcela começa durante a obra? Pergunte a carência por escrito.")')
    n.merge_cells("B31:C31"); n.row_dimensions[31].height = 34

    # ---------------- Fontes ----------------
    f = wb.create_sheet("Fontes"); f.sheet_view.showGridLines = False; f.freeze_panes = "B6"
    for col, w in zip("ABCDEFGH", (30, 44, 44, 14, 18, 38, 38, 16)): f.column_dimensions[col].width = w
    titulo(f, "2 · As seis fontes do seu caso", "Classifique cada fonte: Disponível, Possível ou Fora. \"Fora também é informação, e evita meses perseguindo o que não existe.\" (Z02)" + ("  ·  DADOS FICTÍCIOS" if ex else ""))
    cab = ["Fonte", "O que ela pede", "O que leva e o risco", "Situação", "Quanto pode cobrir ou reduzir da lacuna (R$)", "Por quê (uma linha)", "Próxima pergunta e para quem", "Conta no mapa"]
    for j, h in enumerate(cab, 1):
        c = f.cell(5, j, h); c.font = T(10, True, CREME); c.fill = CAB; c.alignment = WRAP; c.border = borda
    f.row_dimensions[5].height = 44
    EX = [("Possível", 60000, "Abrir a etapa 1 com menos unidades reduz o CAPEX. Falta o projeto inteiro desenhado.", "Arquiteto: qual é o menor conjunto que já opera?"),
          ("Possível", 83000, "Cabe só a parcela de R$ 1.500. A parcela na obra ainda não foi testada.", "3 bancos: taxa para o meu perfil, carência e garantia, por escrito."),
          ("Possível", 150000, "Só depois de estruturar: hoje não há pasta que se audite.", "Quem do meu círculo profissional investe em turismo?"),
          ("Fora", 0, "Quero operar eu mesmo a hospedagem.", ""),
          ("Possível", 0, "Não sei se construtores da região fazem permuta.", "Associação comercial: há construtores que fazem permuta?"),
          ("Fora", 0, "O irmão ofereceu, mas sem contrato escrito não conta.", "")]
    dvs = DataValidation(type="list", formula1='"Disponível,Possível,Fora"', allow_blank=True); f.add_data_validation(dvs)
    dvv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True, showErrorMessage=True, error="Use um valor maior ou igual a zero."); f.add_data_validation(dvv)
    for i, (nome, pede, leva) in enumerate(FONTES):
        l = 6 + i; f.row_dimensions[l].height = 92
        for j, v in enumerate((nome, pede, leva), 1):
            c = f.cell(l, j, v); c.alignment = Alignment(wrap_text=True, vertical="top"); c.border = borda; c.font = T(10, j == 1, MUSGO if j == 1 else PRETO)
        e = EX[i] if ex else (None, None, None, None)
        entrada(f, f"D{l}", e[0], '@'); entrada(f, f"E{l}", e[1]); entrada(f, f"F{l}", e[2], '@'); entrada(f, f"G{l}", e[3], '@')
        for col in "DFG": f[f"{col}{l}"].font = T(10)
        dvs.add(f"D{l}"); dvv.add(f"E{l}")
        calc(f, f"H{l}", f'=IF(OR(D{l}="Disponível",D{l}="Possível"),N(E{l}),0)')
    faixa(f, 13, "Resumo do mapa", 3)
    res = [(14, "Lacuna da etapa 1 (aba Necessidade)", '=Necessidade!B16', BRL),
           (15, "Soma das fontes Disponível e Possível", '=SUM(H6:H11)', BRL),
           (16, "Cobertura da lacuna pelo mapa", '=IF(OR(B14="",N(B14)=0),"",MIN(1,B15/B14))', PCT),
           (17, "Ainda descoberto", '=IF(B14="","",MAX(0,B14-B15))', BRL),
           (18, "Fontes classificadas", '=COUNTA(D6:D11)', '0'),
           (19, "Fontes marcadas como Fora", '=COUNTIF(D6:D11,"Fora")', '0'),
           (20, "Leitura", '=IF(B18<6,"Classifique as seis fontes",IF(B14="","Preencha a aba Necessidade",IF(B17>0,"Ainda falta: reduza a etapa 1, combine outra fonte ou estruture antes de pedir","O mapa cobre a lacuna no papel. Agora cada fonte precisa de proposta por escrito")))', '@')]
    for l, t, fo, fm in res:
        a = f.cell(l, 1, t); a.font = T(11); a.alignment = WRAP; calc(f, f"B{l}", fo, fm, destaque=(l in (14, 17)))
    f.merge_cells("B20:C20"); f.row_dimensions[20].height = 34
    f["A22"] = "Lembre: «Na prática, um projeto faseado de pequeno porte raramente é financiado por uma fonte só.» (Volume 05, citado no Z02). Antes de assinar, confira se as garantias de cada fonte conflitam."
    f["A22"].font = T(9, c="5F5F55", i=True); f.merge_cells("A22:G22"); f["A22"].alignment = WRAP; f.row_dimensions[22].height = 30

    # ---------------- Prontidão ----------------
    p = wb.create_sheet("Prontidão"); p.sheet_view.showGridLines = False
    p.column_dimensions["A"].width = 70; p.column_dimensions["B"].width = 12; p.column_dimensions["C"].width = 58
    titulo(p, "3 · Você está pronto para pedir?", "Portão do capital (F00 Cap. 5): uma reprovada manda mudar a premissa; uma pendente manda estruturar antes de captar." + ("  ·  DADOS FICTÍCIOS" if ex else ""))
    for j, h in enumerate(["Item", "Sim ou Não", "De onde vem"], 1):
        c = p.cell(5, j, h); c.font = T(10, True, CREME); c.fill = CAB; c.border = borda
    dvp = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); p.add_data_validation(dvp)
    EXP = ["Sim", "Sim", "Não", "Sim", "Não", "Não", "Não", "Não", "Sim", "Não"]
    for i, (t, fo) in enumerate(PRONTIDAO):
        l = 6 + i; p.row_dimensions[l].height = 34
        a = p.cell(l, 1, f"{i+1}. {t}"); a.alignment = WRAP; a.border = borda; a.font = T(10)
        entrada(p, f"B{l}", EXP[i] if ex else None, '@'); dvp.add(f"B{l}")
        c = p.cell(l, 3, fo); c.font = T(9, c="5F5F55", i=True); c.alignment = WRAP; c.border = borda
    for l, t, fo, fm in [(17, "Itens respondidos", '=COUNTA(B6:B15)', '0'), (18, "Itens com Sim", '=COUNTIF(B6:B15,"Sim")', '0'),
                         (19, "Prontidão", '=IF(B17=0,"",B18/10)', '0%'),
                         (20, "Leitura", '=IF(B17<10,"Responda os 10 itens",IF(B18=10,"Pronto para conversar com capital de terceiros, com assessoria. Conversar não é captar.","Estruturar antes de captar: avance no que custa tempo, não no que compromete capital"))', '@')]:
        a = p.cell(l, 1, t); a.font = T(11, l == 20); calc(p, f"B{l}", fo, fm, destaque=(l == 20))
    p.merge_cells("B20:C20"); p.row_dimensions[20].height = 40

    # ---------------- Próximos passos ----------------
    s = wb.create_sheet("Próximos passos"); s.sheet_view.showGridLines = False
    for col, w in zip("ABCDE", (60, 22, 14, 12, 20)): s.column_dimensions[col].width = w
    titulo(s, "4 · Seus próximos passos, com data", "Até cinco ações. Sem data, vira intenção." + ("  ·  DADOS FICTÍCIOS" if ex else ""))
    for j, h in enumerate(["Ação", "Quem", "Data", "Feito?", "Situação"], 1):
        c = s.cell(5, j, h); c.font = T(10, True, CREME); c.fill = CAB; c.border = borda
    dvf = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True); s.add_data_validation(dvf)
    dvd = DataValidation(type="date", operator="greaterThan", formula1="36526", allow_blank=True, showErrorMessage=True, error="Use uma data (dd/mm/aaaa)."); s.add_data_validation(dvd)
    EXS = [("Agendar a sessão de direcionamento com a equipe Zion (30 min, incluída no Clube)", "Eu", datetime.date(2026, 11, 18), "Sim"),
           ("Pedir a certidão de matrícula atualizada no cartório", "Eu", datetime.date(2026, 11, 20), "Não"),
           ("Pedir orçamento escrito da etapa 1 a dois fornecedores, com data", "Eu", datetime.date(2026, 11, 30), "Não"),
           ("Perguntar a três bancos taxa, carência e garantia, por escrito", "Eu", datetime.date(2026, 12, 5), "Não"),
           ("Pesquisar a diária de cinco hospedagens comparáveis, mês a mês", "Eu", datetime.date(2026, 12, 10), "Não")]
    for i in range(5):
        l = 6 + i; s.row_dimensions[l].height = 30; e = EXS[i] if ex else (None, None, None, None)
        entrada(s, f"A{l}", e[0], '@'); entrada(s, f"B{l}", e[1], '@'); entrada(s, f"C{l}", e[2], DATA); entrada(s, f"D{l}", e[3], '@')
        for col in "AB": s[f"{col}{l}"].font = T(10)
        dvf.add(f"D{l}"); dvd.add(f"C{l}")
        calc(s, f"E{l}", f'=IF(A{l}="","",IF(D{l}="Sim","Concluído",IF(C{l}="","Defina a data","Em aberto")))', '@')
    s["A12"] = "Sessão de direcionamento (30 min, incluída no Club Zion Collection): https://app.clickmax.io/book/projeto-de-bruno-25763216/xpfd5s9qv4gbiywp-mjuwbwt"
    s["A12"].font = T(10, True, TERRA); s.merge_cells("A12:E12")
    s["A13"] = "Na sessão, a equipe Zion olha o seu caso e indica o próximo passo. A Zion avalia cada caso; não há promessa de crédito, sócio ou resultado."
    s["A13"].font = T(9, c="5F5F55", i=True); s.merge_cells("A13:E13")

    for w in wb.worksheets:
        w.sheet_properties.tabColor = MUSGO if w.title == "Comece aqui" else TERRA
        w.page_setup.orientation = "landscape"; w.page_setup.fitToWidth = 1; w.sheet_properties.pageSetUpPr.fitToPage = True; w.page_setup.fitToHeight = 0
    return wb

for ex, nome in [(False, "Mapa-das-Fontes-de-Capital-Zion-EM-BRANCO.xlsx"), (True, "Mapa-das-Fontes-de-Capital-Zion-EXEMPLO.xlsx")]:
    wb = montar(ex); wb.active = 0; wb.save(OUT / nome); print("ok", OUT / nome)

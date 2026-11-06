"""Gera a Ferramenta 17 · Checklist de Limpeza, Inspeção e Liberação (Zion Hospitality Business):
   - Checklist-Limpeza-Zion-EM-BRANCO.xlsx  (modelo-padrão pronto, troca sem preencher)
   - Checklist-Limpeza-Zion-EXEMPLO.xlsx    (troca preenchida com dados fictícios)
Uso: python3 -I build_planilha.py <pasta-saida>"""
import sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from modelo_itens import ITENS
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, AREIA, DOURADO, PRETO, CREME, TERRA = "1B2117", "DED6BF", "C9B37E", "040605", "FEF5F0", "8B714E"
ENTRADA = PatternFill("solid", fgColor="FFF4C7")   # amarelo = você preenche
CALC = PatternFill("solid", fgColor="E3EEDF")      # verde = calculado
CAB = PatternFill("solid", fgColor=MUSGO)
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)
WRAP = Alignment(wrap_text=True, vertical="center")
NLIN = 100          # linhas de itens no Modelo e na Troca
M0, T0 = 5, 14      # primeira linha de itens no Modelo e na Troca
P0, H0, NREG = 6, 6, 200
DATA, HORA = "DD/MM/YYYY", "HH:MM"
VERDE_OK, VERM, ALERTA = "C8E6C0", "F4C7C3", "FCE8B2"

def cab_tabela(ws, linha, titulos):
    for j, t in enumerate(titulos, 1):
        c = ws.cell(linha, j, t); c.font = T(10, True, CREME); c.fill = CAB; c.alignment = WRAP; c.border = borda
    ws.row_dimensions[linha].height = 30

def ent(c, v=None, fmt=None):
    c.value = v; c.fill = ENTRADA; c.border = borda; c.alignment = WRAP; c.font = T(10)
    if fmt: c.number_format = fmt

def calc(c, f, fmt=None, sz=10, b=False):
    c.value = f; c.fill = CALC; c.border = borda; c.alignment = WRAP; c.font = T(sz, b)
    if fmt: c.number_format = fmt

def lista(ws, rng, opcoes):
    dv = DataValidation(type="list", formula1='"' + ",".join(opcoes) + '"', allow_blank=True,
                        showErrorMessage=True, errorTitle="Opção inválida", error="Escolha uma opção da lista.")
    ws.add_data_validation(dv); dv.add(rng)

def montar(exemplo):
    wb = Workbook()
    # ---------------- Comece aqui ----------------
    ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 104
    linhas = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 17", T(10, True, TERRA)),
        ("Checklist de Limpeza, Inspeção e Liberação", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para limpar, conferir e liberar cada unidade com o mesmo padrão, sabendo quem fez, quem conferiu e o que ficou pendente.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (pessoas e unidades inventadas). Use a versão em branco para a sua hospedagem." if exemplo
         else "Versão em branco: o modelo de itens já vem pronto para você ajustar. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("", None),
        ("COMO USAR EM 5 PASSOS (cerca de 20 minutos na primeira vez; depois, só a troca)", T(12, True, MUSGO)),
        ("1. Aba Ajustes: escreva o nome da hospedagem e decida se a conferência precisa ser feita por outra pessoa (recomendado quando há equipe).", None),
        ("2. Aba Modelo: ajuste a lista à sua unidade. Apague o que não existe, acrescente o que falta e marque o que é obrigatório para liberar. Escreva em \"Como conferir\" o critério que qualquer pessoa consegue verificar.", None),
        ("3. Aba Troca: a cada saída de hóspede, preencha unidade, data e nomes. Quem limpa marca a coluna Execução. Quem confere marca a coluna Conferência.", None),
        ("4. Olhe a Situação da troca (no alto da aba Troca). A unidade só aparece como LIBERADA quando todos os itens obrigatórios foram feitos e aprovados.", None),
        ("5. Registre o que ficou para depois na aba Pendências e anote o resultado da troca no Histórico. Para a próxima troca, apague as marcações amarelas da aba Troca (ou duplique a aba).", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("REGRAS DA LIBERAÇÃO", T(12, True, MUSGO)),
        ("Item obrigatório só conta como resolvido com Execução = Feito e Conferência = Aprovado. \"Não se aplica\" em item obrigatório conta como pendente: se o item não existe na unidade, tire-o do Modelo ou marque-o como não obrigatório.", None),
        ("Item não obrigatório que não foi feito ou foi reprovado aparece como Atenção, mas não impede a liberação.", None),
        ("", None),
        ("O QUE A PLANILHA FAZ E O QUE ELA NÃO FAZ", T(12, True, MUSGO)),
        ("Faz: organiza a sequência da limpeza, separa quem executa de quem confere, bloqueia a liberação com item obrigatório pendente e mantém o registro das pendências e das trocas.", None),
        ("Não faz: não garante a qualidade da limpeza (isso depende de quem confere), não substitui normas sanitárias, de segurança ou orientações de fabricantes e não prescreve produtos de limpeza. Use os produtos e os equipamentos de proteção definidos pelo responsável, seguindo o rótulo.", None),
        ("", None),
        ("No celular: abra o arquivo no app do Google Sheets ou do Excel. Para papel, use o PDF imprimível que acompanha a ferramenta.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo: não garante avaliações, reservas nem ocupação.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------------- Ajustes ----------------
    a = wb.create_sheet("Ajustes"); a.sheet_view.showGridLines = False
    for col, w in zip("ABC", (46, 26, 60)): a.column_dimensions[col].width = w
    a["A1"] = "Ajustes"; a["A1"].font = T(18, True, MUSGO)
    rot = [(4, "Nome da hospedagem", "Aparece no topo da aba Troca."),
           (5, "Exigir conferente diferente de quem limpou?", "Sim = recomendado com equipe. Não = você trabalha sozinho e confere o próprio trabalho."),
           (6, "Data de referência (opcional)", "Deixe em branco para usar a data de hoje ao marcar pendências atrasadas."),
           (7, "Data usada nas pendências", "Calculado.")]
    for l, r, h in rot:
        a.cell(l, 1, r).font = T(11); a.cell(l, 1).alignment = WRAP
        a.cell(l, 3, h).font = T(9, c="5F5F55", i=True); a.cell(l, 3).alignment = WRAP
    ent(a["B4"], "Pousada Exemplo (fictícia)" if exemplo else None)
    ent(a["B5"], "Sim"); lista(a, "B5", ["Sim", "Não"])
    ent(a["B6"], None, DATA)
    calc(a["B7"], '=IF(B6="",TODAY(),B6)', DATA)

    # ---------------- Modelo ----------------
    m = wb.create_sheet("Modelo"); m.sheet_view.showGridLines = False
    for col, w in zip("ABCD", (22, 46, 14, 50)): m.column_dimensions[col].width = w
    m["A1"] = "Modelo de itens da sua unidade"; m["A1"].font = T(18, True, MUSGO)
    m["A2"] = "Ajuste à sua realidade: apague, acrescente e reordene. A aba Troca copia esta lista automaticamente (até 100 itens)."
    m["A2"].font = T(10, c="5F5F55", i=True)
    cab_tabela(m, 4, ["Ambiente", "O que fazer", "Obrigatório para liberar?", "Como conferir"])
    for i in range(NLIN):
        r = M0 + i; it = ITENS[i] if i < len(ITENS) else (None, None, None, None)
        for j, v in enumerate(it, 1): ent(m.cell(r, j), v)
    lista(m, f"C{M0}:C{M0+NLIN-1}", ["Sim", "Não"])
    m.freeze_panes = "A5"

    # ---------------- Troca ----------------
    t = wb.create_sheet("Troca"); t.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGH", (20, 40, 11, 34, 15, 15, 28, 13)): t.column_dimensions[col].width = w
    t["A1"] = '=IF(Ajustes!B4="","Troca de hóspede","Troca de hóspede · "&Ajustes!B4)'; t["A1"].font = T(16, True, MUSGO)
    t["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Uma troca por vez. Preencha as células amarelas."
    t["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    ex = dict(un="Cabana 2", dt=datetime.date(2026, 11, 5), exe="Ana (fictícia)", conf="Carlos (fictício)",
              ini=datetime.time(10, 30), fim=datetime.time(12, 5)) if exemplo else {}
    head = [(3, "Unidade", "un", None), (4, "Data da troca", "dt", DATA), (5, "Quem limpou", "exe", None),
            (6, "Quem conferiu", "conf", None), (7, "Início", "ini", HORA), (8, "Fim", "fim", HORA)]
    for l, r, k, fmt in head:
        t.cell(l, 1, r).font = T(10, True); ent(t.cell(l, 2), ex.get(k), fmt)
    R = f"{T0}:{T0+NLIN-1}"; rg = lambda col: f"{col}{T0}:{col}{T0+NLIN-1}"
    # resumo (colunas D a H)
    resumo = [
        (3, "Itens na lista", f'=SUMPRODUCT(--(LEN({rg("B")})>0))'),
        (4, "Itens obrigatórios", f'=COUNTIF({rg("C")},"Sim")'),
        (5, "Obrigatórios pendentes", f'=COUNTIF({rg("H")},"PENDENTE")'),
        (6, "Itens opcionais em atenção", f'=COUNTIF({rg("H")},"Atenção")'),
        (7, "Tempo da troca (min)", '=IF(OR(B7="",B8=""),"",IF(B8<B7,"Confira os horários",ROUND((B8-B7)*1440,0)))'),
    ]
    for l, r, f in resumo:
        t.cell(l, 4, r).font = T(10, True); t.cell(l, 4).alignment = Alignment(horizontal="right")
        calc(t.cell(l, 5), f)
    t["A10"] = "Situação da troca"; t["A10"].font = T(11, True, MUSGO)
    t.merge_cells("B10:H10")
    calc(t["B10"],
         '=IF(OR(B3="",B4="",B5="",AND(Ajustes!B5="Sim",B6="")),"PREENCHA O CABEÇALHO (unidade, data e nomes)",'
         'IF(E4=0,"CADASTRE OS ITENS OBRIGATÓRIOS NA ABA MODELO",'
         'IF(AND(Ajustes!B5="Sim",LOWER(TRIM(B5))=LOWER(TRIM(B6))),"NÃO LIBERAR: a conferência precisa ser feita por outra pessoa",'
         'IF(E5>0,"NÃO LIBERAR: "&E5&IF(E5=1," item obrigatório pendente"," itens obrigatórios pendentes"),'
         '"LIBERADA PARA O PRÓXIMO HÓSPEDE"))))', sz=13, b=True)
    t.row_dimensions[10].height = 28
    t["A11"] = "Liberada só com todos os obrigatórios em Feito + Aprovado. Pendências: anote na aba Pendências."
    t["A11"].font = T(9, c="5F5F55", i=True)
    cab_tabela(t, 13, ["Ambiente", "O que fazer", "Obrig.?", "Como conferir", "Execução", "Conferência", "Observação", "Situação"])
    for i in range(NLIN):
        r, mr = T0 + i, M0 + i
        for col, src in (("A", "A"), ("B", "B"), ("D", "D")):
            calc(t[f"{col}{r}"], f'=IF(Modelo!$B{mr}="","",Modelo!{src}{mr}&"")')
        calc(t[f"C{r}"], f'=IF(Modelo!$B{mr}="","",IF(Modelo!C{mr}="Sim","Sim","Não"))')
        for col in "EFG": ent(t[f"{col}{r}"])
        calc(t[f"H{r}"], f'=IF(B{r}="","",IF(C{r}="Sim",IF(AND(E{r}="Feito",F{r}="Aprovado"),"OK","PENDENTE"),'
                         f'IF(OR(E{r}="Não se aplica",F{r}="Não se aplica",AND(E{r}="Feito",F{r}="Aprovado")),"OK","Atenção")))', b=True)
    lista(t, rg("E"), ["Feito", "Não feito", "Não se aplica"])
    lista(t, rg("F"), ["Aprovado", "Reprovado", "Não se aplica"])
    t.conditional_formatting.add("B10", FormulaRule(formula=['LEFT($B$10,8)="LIBERADA"'], fill=PatternFill("solid", fgColor=VERDE_OK)))
    t.conditional_formatting.add("B10", FormulaRule(formula=['LEFT($B$10,3)="NÃO"'], fill=PatternFill("solid", fgColor=VERM)))
    t.conditional_formatting.add(rg("H"), FormulaRule(formula=[f'H{T0}="PENDENTE"'], fill=PatternFill("solid", fgColor=VERM)))
    t.conditional_formatting.add(rg("H"), FormulaRule(formula=[f'H{T0}="Atenção"'], fill=PatternFill("solid", fgColor=ALERTA)))
    t.conditional_formatting.add(rg("H"), FormulaRule(formula=[f'H{T0}="OK"'], fill=PatternFill("solid", fgColor=VERDE_OK)))
    t.freeze_panes = f"A{T0}"
    t.print_title_rows = "13:13"; t.page_setup.orientation = "landscape"; t.page_setup.fitToWidth = 1; t.page_setup.fitToHeight = 0
    t.sheet_properties.pageSetUpPr.fitToPage = True
    if exemplo:
        especiais = {
            "Testar o chuveiro (água quente)": ("Feito", "Reprovado", "Água morna depois de 3 min. Pendência aberta."),
            "Repor café, chá e itens de cortesia": ("Não feito", "Reprovado", "Faltou chá. Repor na compra de amanhã."),
            "Conferir banheira, jacuzzi ou piscina conforme a rotina do responsável": ("Não se aplica", "Não se aplica", "A Cabana 2 não tem banheira."),
        }
        for i, it in enumerate(ITENS):
            e, f, o = especiais.get(it[1], ("Feito", "Aprovado", None))
            t[f"E{T0+i}"], t[f"F{T0+i}"], t[f"G{T0+i}"] = e, f, o

    # ---------------- Pendências ----------------
    p = wb.create_sheet("Pendências"); p.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHI", (13, 14, 18, 40, 20, 13, 28, 13, 14)): p.column_dimensions[col].width = w
    p["A1"] = "Pendências da limpeza e da inspeção"; p["A1"].font = T(18, True, MUSGO)
    p["A2"] = "O que não pôde ser resolvido na troca. Feche cada linha com a data em \"Resolvida em\"."; p["A2"].font = T(10, c="5F5F55", i=True)
    p["A3"] = "Abertas"; p["A3"].font = T(10, True); calc(p["B3"], f'=COUNTIF(I{P0}:I{P0+NREG-1},"Aberta")+COUNTIF(I{P0}:I{P0+NREG-1},"Sem prazo")+COUNTIF(I{P0}:I{P0+NREG-1},"Atrasada")')
    p["C3"] = "Atrasadas"; p["C3"].font = T(10, True); calc(p["D3"], f'=COUNTIF(I{P0}:I{P0+NREG-1},"Atrasada")')
    cab_tabela(p, 5, ["Aberta em", "Unidade", "Ambiente", "O que aconteceu", "Responsável", "Prazo", "Evidência (foto ou link)", "Resolvida em", "Situação"])
    for r in range(P0, P0 + NREG):
        for col in "ABCDEFGH": ent(p[f"{col}{r}"], None, DATA if col in "AFH" else None)
        calc(p[f"I{r}"], f'=IF(D{r}="","",IF(H{r}<>"","Resolvida",IF(F{r}="","Sem prazo",IF(F{r}<Ajustes!$B$7,"Atrasada","Aberta"))))', b=True)
    p.conditional_formatting.add(f"I{P0}:I{P0+NREG-1}", FormulaRule(formula=[f'I{P0}="Atrasada"'], fill=PatternFill("solid", fgColor=VERM)))
    p.conditional_formatting.add(f"I{P0}:I{P0+NREG-1}", FormulaRule(formula=[f'I{P0}="Resolvida"'], fill=PatternFill("solid", fgColor=VERDE_OK)))
    p.freeze_panes = f"A{P0}"
    if exemplo:
        d = datetime.date
        reg = [(d(2026, 11, 3), "Cabana 1", "7 · Funcionamento", "Lâmpada do abajur queimada", "Carlos (fictício)", d(2026, 11, 4), "Foto no grupo da equipe", d(2026, 11, 4)),
               (d(2026, 11, 5), "Cabana 2", "7 · Funcionamento", "Chuveiro com água morna depois de 3 minutos", "Manutenção (fictícia)", d(2026, 11, 5), "Foto do aquecedor", None),
               (d(2026, 11, 5), "Cabana 2", "4 · Copa e cozinha", "Faltou chá na cortesia", "Ana (fictícia)", None, None, None)]
        for k, row in enumerate(reg):
            for j, v in enumerate(row): p.cell(P0 + k, j + 1).value = v

    # ---------------- Histórico ----------------
    h = wb.create_sheet("Histórico"); h.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGHIJ", (13, 14, 18, 18, 9, 9, 15, 13, 34, 12)): h.column_dimensions[col].width = w
    h["A1"] = "Histórico das trocas"; h["A1"].font = T(18, True, MUSGO)
    h["A2"] = "Uma linha por troca. Copie da aba Troca o resultado antes de apagar as marcações."; h["A2"].font = T(10, c="5F5F55", i=True)
    rgH = lambda col: f"{col}{H0}:{col}{H0+NREG-1}"
    for col, rot_, f in (("A", "Trocas", f'=SUMPRODUCT(--(LEN({rgH("B")})>0))'), ("C", "Liberadas", f'=COUNTIF({rgH("G")},"Liberada")'),
                         ("E", "Não liberadas", f'=COUNTIF({rgH("G")},"Não liberada")'), ("H", "Tempo médio (min)", f'=IFERROR(ROUND(AVERAGE({rgH("J")}),0),"")')):
        h[f"{col}3"] = rot_; h[f"{col}3"].font = T(10, True)
        calc(h.cell(3, h[f"{col}3"].column + 1), f)
    cab_tabela(h, 5, ["Data", "Unidade", "Quem limpou", "Quem conferiu", "Início", "Fim", "Resultado", "Obrigatórios pendentes", "Observação", "Tempo (min)"])
    for r in range(H0, H0 + NREG):
        for col in "ABCDEFGHI": ent(h[f"{col}{r}"], None, DATA if col == "A" else HORA if col in "EF" else None)
        calc(h[f"J{r}"], f'=IF(OR(E{r}="",F{r}=""),"",IF(F{r}<E{r},"Confira",ROUND((F{r}-E{r})*1440,0)))')
    lista(h, rgH("G"), ["Liberada", "Não liberada"])
    h.freeze_panes = f"A{H0}"
    if exemplo:
        d, tm = datetime.date, datetime.time
        reg = [(d(2026, 11, 3), "Cabana 1", "Ana (fictícia)", "Carlos (fictício)", tm(11, 0), tm(12, 20), "Liberada", 0, "Lâmpada trocada no dia seguinte"),
               (d(2026, 11, 4), "Cabana 3", "Ana (fictícia)", "Carlos (fictício)", tm(10, 45), tm(12, 0), "Liberada", 0, None),
               (d(2026, 11, 5), "Cabana 2", "Ana (fictícia)", "Carlos (fictício)", tm(10, 30), tm(12, 5), "Não liberada", 1, "Chuveiro: aguardando manutenção")]
        for k, row in enumerate(reg):
            for j, v in enumerate(row): h.cell(H0 + k, j + 1).value = v

    wb.active = wb.sheetnames.index("Comece aqui")
    nome = "Checklist-Limpeza-Zion-EXEMPLO.xlsx" if exemplo else "Checklist-Limpeza-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

montar(False); montar(True)

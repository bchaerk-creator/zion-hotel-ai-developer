#!/usr/bin/env python3
"""Gera modelo_financeiro.xlsx (ZION FINANCE · Fase 03).
Sem dados reais de venda/gasto: células de entrada vazias ou parâmetros rotulados.
Uso: python3 -I build_modelo.py [saida.xlsx]   (build(path, inputs) também é usado pelo teste)"""
import re, sys, json
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

YEL = PatternFill("solid", fgColor="FFF59D")   # preenchido pelo usuário
GRN = PatternFill("solid", fgColor="C8E6C9")   # calculado
HDR = PatternFill("solid", fgColor="1B2117")
GRY = PatternFill("solid", fgColor="EEEEEE")
BRL = 'R$ #,##0.00'; PCT = '0.0%'; NUM = '0.00'; INT = '0'
thin = Side(style="thin", color="BBBBBB"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
S_PAR, S_MM, S_OUT, S_CEN, S_CON, S_INI = "Parâmetros", "Mini Mentoria 47", "Outros produtos", "Cenários", "Conciliação", "Comece aqui"
IND = "indisponível"

CELLS = {}   # nome -> "'Aba'!$B$n"

def q(s): return "'" + s + "'"

def title(ws, text, sub=None):
    ws["A1"] = text; ws["A1"].font = Font(name="Cambria", size=16, bold=True, color="1B2117")
    if sub: ws["A2"] = sub; ws["A2"].font = Font(italic=True, color="555555")

def hdr(ws, row, vals, col=1):
    for i, v in enumerate(vals):
        c = ws.cell(row=row, column=col + i, value=v)
        c.fill = HDR; c.font = Font(bold=True, color="FEF5F0"); c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = BOX

def sub(formula, local, sheet):
    # @nome -> parâmetro (outra aba) ; #nome -> célula local (mesma aba)
    f = re.sub(r"@(\w+)", lambda m: CELLS[m.group(1)], formula)
    f = re.sub(r"#(\w+)", lambda m: local[m.group(1)], f)
    return f

def put(ws, row, name, label, value, fmt, kind, tag="", note="", local=None, store=None):
    ws.cell(row=row, column=1, value=label).alignment = Alignment(wrap_text=True, vertical="top")
    c = ws.cell(row=row, column=2)
    if isinstance(value, str) and value.startswith("="):
        c.value = sub(value, local if local is not None else {}, ws.title)
    else:
        c.value = value
    c.number_format = fmt; c.border = BOX
    if kind == "in": c.fill = YEL
    elif kind == "calc": c.fill = GRN
    ws.cell(row=row, column=3, value=tag).font = Font(bold=True, color="8B714E")
    n = ws.cell(row=row, column=4, value=note); n.alignment = Alignment(wrap_text=True, vertical="top")
    ref = f"{q(ws.title)}!$B${row}"
    if store is not None: store[name] = f"$B${row}" if False else f"$B${row}"
    if local is not None: local[name] = f"$B${row}"
    CELLS_LOCAL = None
    return ref

def build(path, inputs=None):
    inputs = inputs or {}
    wb = Workbook()
    # ---------------- Comece aqui
    ws = wb.active; ws.title = S_INI
    title(ws, "Modelo financeiro · Zion Hotel Academy", "ZION FINANCE · Fase 03 · modelo-molde sem dados reais (repositório público)")
    lines = [
        ("Para que serve", "Dizer quanto se pode pagar por uma venda (CPA máximo) e se a conta fecha. Faturamento não é lucro."),
        ("Cores", "AMARELO = você preenche (ou confirma o valor padrão). VERDE = calculado, não digite."),
        ("Etiquetas", "[E] evidência (lido de oferta/venda/extrato)  [H] hipótese ou estimativa  [NC] não confirmado  'a definir' = valor padrão 0 só para a fórmula rodar."),
        ("Passo 1", "Aba Parâmetros: confira o preço e a taxa; preencha imposto, custos variáveis, taxa de reembolso e margem alvo quando houver valor definido."),
        ("Passo 2", "Aba Parâmetros: quando existirem dados REAIS, preencha custo por checkout iniciado e conversão checkout→venda (e os observados). Sem eles a aba Mini Mentoria 47 mostra 'indisponível' e a decisão fica 'SEM DECISÃO'."),
        ("Passo 3", "Aba Mini Mentoria 47: leia CPA máximo, CPA desejado, ROAS de equilíbrio, CPA projetado e a decisão (escalar / manter / pausar)."),
        ("Passo 4", "Aba Conciliação: registre gasto do Meta × vendas do ClickMax × vendas da Ticto por dia ou campanha. Compras de teste internas ficam FORA."),
        ("Aba Outros produtos", "CPA máximo e ROAS de equilíbrio dos demais preços da conta e ranking de viabilidade para anúncio direto."),
        ("Aba Cenários", "Matriz de CPA projetado (custo por checkout × conversão) e cenários de taxa/imposto/reembolso. TUDO hipótese [H], nunca resultado."),
        ("Regra de decisão", "A venda do infoproduto precisa financiar a aquisição. Não se justifica perda inicial por LTV hipotético. LTV usa só compra única comprovada; segundo produto só como cenário rotulado."),
        ("Governança", "Escalar, pausar ou mudar orçamento só com 'aprovado' de Bruno. O modelo recomenda; não executa. Dados reais ficam fora do repositório (arquivo público)."),
    ]
    for i, (a, b) in enumerate(lines, start=4):
        ws.cell(row=i, column=1, value=a).font = Font(bold=True)
        c = ws.cell(row=i, column=2, value=b); c.alignment = Alignment(wrap_text=True, vertical="top")
    ws["A17"] = "Exemplo de cor"; ws["B17"] = "campo de entrada"; ws["B17"].fill = YEL
    ws["B18"] = "campo calculado"; ws["B18"].fill = GRN
    ws.column_dimensions["A"].width = 24; ws.column_dimensions["B"].width = 110

    # ---------------- Parâmetros
    wp = wb.create_sheet(S_PAR)
    title(wp, "Parâmetros", "Amarelo = entrada. Valor 0 rotulado 'a definir' = ainda sem valor definido (não é custo zero comprovado).")
    hdr(wp, 3, ["Parâmetro", "Valor", "Etiqueta", "Fonte / observação"])
    loc = {}
    def P(row, name, label, value, fmt, kind, tag="", note=""):
        v = inputs.get(name, value)
        put(wp, row, name, label, v, fmt, kind, tag, note, local=loc)
        CELLS[name] = f"{q(S_PAR)}!$B${row}"
    P(4, "preco", "Preço bruto do produto analisado (R$)", 47, BRL, "in", "[E]", "Mini Mentoria de Estruturação, oferta 0c71eeba, pagamento único, Pix e cartão 1x.")
    P(5, "tx_fixa", "Taxa fixa por venda no Pix (R$)", 2.49, BRL, "in", "[E]", "Observada nas vendas Pix pagas de R$ 19 e R$ 47 (Ticto): líquido R$ 16,51 e R$ 44,51.")
    P(6, "tx_pct", "Taxa % do Pix aplicada a este produto", 0.0, PCT, "in", "[E]", "0% para R$ 47: a venda paga de R$ 47 deu líquido 44,51 (= preço − 2,49). Ver cenário conservador com 6,99% (linha 7).")
    P(7, "tx_pct_alta", "Taxa % do Pix observada em R$ 97 e R$ 270", 0.0699, PCT, "in", "[E]", "Ajuste de 2 pontos: R$ 97 → líquido 87,73 e R$ 270 → 248,64 batem com 2,49 + 6,99% do preço. A regra por faixa de preço não está documentada [NC]. Usada em Outros produtos e Cenários.")
    P(8, "liq_pix", "Líquido por venda no Pix (R$)", "=#preco-#tx_fixa-#tx_pct*#preco", BRL, "calc", "[E]", "preço − taxa fixa − taxa% × preço.")
    P(9, "ref47", "Referência: líquido Pix de R$ 47 (R$)", 44.51, BRL, "in", "[E]", "Venda real paga, comissão informada pelo ClickMax.")
    P(10, "ref97", "Referência: líquido Pix de R$ 97 (R$)", 87.73, BRL, "in", "[E]", "Venda real paga, comissão informada pelo ClickMax.")
    P(11, "chk_ref", "Conferência do líquido contra a referência", '=IF(#preco=47,IF(ABS(#liq_pix-#ref47)<0.005,"OK: bate com R$ 44,51","DIVERGE da referência"),IF(#preco=97,IF(ABS(#liq_pix-#ref97)<0.005,"OK: bate com R$ 87,73","DIVERGE da referência"),"sem referência para este preço"))', "General", "calc", "", "")
    P(12, "mix_pix", "Mix de vendas no Pix (%)", 1.0, PCT, "in", "[E]", "Todas as vendas pagas até 25/11 foram Pix; nenhuma venda no cartão registrada. Para cenário com cartão, reduza aqui e preencha a taxa do cartão.")
    P(13, "cx_fixa", "Taxa fixa do cartão 1x (R$)", 0, BRL, "in", "[NC]", "a definir: sem transação de cartão para medir.")
    P(14, "cx_pct", "Taxa % do cartão 1x", 0.0, PCT, "in", "[NC]", "a definir: sem transação de cartão para medir.")
    P(15, "liq_cartao", "Líquido por venda no cartão (R$)", "=#preco-#cx_fixa-#cx_pct*#preco", BRL, "calc", "[NC]", "Com taxa 0 o líquido do cartão fica igual ao bruto (superestimado).")
    P(16, "aviso_cartao", "Aviso do mix com cartão", '=IF(AND(#mix_pix<1,#cx_fixa+#cx_pct=0),"ATENÇÃO: há cartão no mix e taxa do cartão em 0: líquido superestimado","ok")', "General", "calc", "", "")
    P(17, "liq_medio", "Líquido médio ponderado pelo mix (R$)", "=#mix_pix*#liq_pix+(1-#mix_pix)*#liq_cartao", BRL, "calc", "", "")
    P(18, "imposto", "Imposto sobre a venda (% do preço)", 0.0, PCT, "in", "a definir", "Sem alíquota definida. Não há valor padrão: preencher com o regime tributário real.")
    P(19, "custos_var", "Custos variáveis por venda (R$)", 0, BRL, "in", "a definir", "Ex.: suporte por venda, ferramentas por aluno. Sem valor definido.")
    P(20, "reemb", "Taxa de reembolso em 7 dias (% das vendas)", 0.0, PCT, "in", "a definir", "Zero reembolsos registrados, mas a amostra é muito pequena (poucos compradores externos). Reserva = taxa × líquido (perda da taxa do gateway no reembolso é [NC]).")
    P(21, "margem_alvo", "Margem alvo sobre a contribuição (%)", 0.30, PCT, "in", "[H]", "Decisão de Bruno. CPA desejado = CPA máximo × (1 − margem alvo).")
    P(22, "teto", "Teto de mídia por dia (R$)", 60, BRL, "in", "[E]", "Teto definido para a fase de teste.")
    P(23, "cpc", "Custo por clique no link (R$)", None, BRL, "in", "dado real", "Vazio: preencher com o dado real do período (fora do repositório).")
    P(24, "cplpv", "Custo por visualização da página (R$)", None, BRL, "in", "dado real", "Vazio.")
    P(25, "cpchk", "Custo por checkout iniciado efetivo (R$)", None, BRL, "in", "dado real", "Vazio. 'Efetivo' = só checkouts de verdade (hoje o evento dispara no carregamento: o dado do Meta superestima a intenção).")
    P(26, "conv_chk", "Conversão real checkout iniciado → venda (%)", None, PCT, "in", "dado real", "Vazio: não inventar. Só preencher com vendas externas confirmadas ÷ checkouts efetivos.")
    P(27, "prazo_pix", "Prazo de recebimento do Pix (dias)", None, INT, "in", "[NC]", "Vazio: confirmar com a Ticto.")
    P(28, "prazo_cartao", "Prazo de recebimento do cartão (dias)", None, INT, "in", "[NC]", "Vazio: confirmar com a Ticto.")
    P(29, "min_chk", "Mínimo de checkouts efetivos para decidir", 100, INT, "in", "[H]", "Trava de amostra mínima (regra de prudência, ajustável por Bruno).")
    P(30, "min_vendas", "Mínimo de vendas para decidir", 5, INT, "in", "[H]", "Idem.")
    P(31, "obs_chk", "Checkouts efetivos observados no período", None, INT, "in", "dado real", "Vazio.")
    P(32, "obs_vendas", "Vendas externas confirmadas no período", None, INT, "in", "dado real", "Vazio. Compras de teste internas não contam.")
    P(33, "conv_clique", "Conversão clique → venda para o CPC máximo (aba Outros produtos)", 0.01, PCT, "in", "[H]", "Hipótese ilustrativa, não é benchmark. Troque pelo dado real quando existir.")
    wp.column_dimensions["A"].width = 52; wp.column_dimensions["B"].width = 20; wp.column_dimensions["C"].width = 11; wp.column_dimensions["D"].width = 95
    for r in range(4, 34): wp.row_dimensions[r].height = 32

    # ---------------- Mini Mentoria 47
    wm = wb.create_sheet(S_MM)
    title(wm, "Mini Mentoria R$ 47 · indicadores", "Cada linha: fórmula na coluna D. 'indisponível' = falta dado real; nada é preenchido por suposição.")
    hdr(wm, 3, ["Indicador", "Valor", "Etiqueta", "Fórmula / leitura"])
    lm = {}
    def M(row, name, label, f, fmt, tag="", note=""):
        put(wm, row, name, label, f, fmt, "calc", tag, note, local=lm)
        CELLS["mm_" + name] = f"{q(S_MM)}!$B${row}"
    M(4, "preco", "Preço bruto (R$)", "=@preco", BRL, "[E]", "Parâmetros.")
    M(5, "liq", "Receita após taxas, líquido médio (R$)", "=@liq_medio", BRL, "[E]", "Mix Pix/cartão × líquido de cada meio.")
    M(6, "imp", "Imposto por venda (R$)", "=@imposto*#preco", BRL, "a definir", "imposto % × preço.")
    M(7, "cv", "Custos variáveis por venda (R$)", "=@custos_var", BRL, "a definir", "")
    M(8, "res", "Reserva de reembolso por venda (R$)", "=@reemb*#liq", BRL, "a definir", "taxa de reembolso × líquido.")
    M(9, "mc", "Margem de contribuição antes da mídia (R$)", "=#liq-#imp-#cv-#res", BRL, "", "líquido − imposto − custos variáveis − reserva de reembolso.")
    M(10, "mcp", "Margem de contribuição (% do preço)", "=IF(#preco=0,0,#mc/#preco)", PCT, "", "")
    M(11, "cpamax", "CPA máximo (R$)", "=#mc", BRL, "", "Acima disso cada venda dá prejuízo de mídia. Com imposto e custos a definir em 0, é o líquido (teto superior, não é lucro).")
    M(12, "cpades", "CPA desejado (R$)", "=#cpamax*(1-@margem_alvo)", BRL, "[H]", "CPA máximo × (1 − margem alvo).")
    M(13, "ticket", "Ticket médio (R$)", "=#preco", BRL, "[E]", "Sem order bump nem upsell comprovados nesta oferta: ticket médio = preço.")
    M(14, "roasbe", "ROAS de equilíbrio", f'=IF(#cpamax<=0,"{IND}",#preco/#cpamax)', NUM, "", "preço ÷ CPA máximo. Abaixo disso a mídia dá prejuízo.")
    M(15, "roasalvo", "ROAS necessário para a margem alvo", f'=IF(#cpades<=0,"{IND}",#preco/#cpades)', NUM, "[H]", "preço ÷ CPA desejado.")
    M(16, "cpchk", "Custo por checkout iniciado efetivo (R$)", f'=IF(@cpchk="","{IND}",@cpchk)', BRL, "dado real", "Parâmetros.")
    M(17, "conv", "Conversão real do checkout", f'=IF(@conv_chk="","{IND}",@conv_chk)', PCT, "dado real", "Parâmetros.")
    M(18, "cpaproj", "CPA projetado (R$)", f'=IF(OR(@cpchk="",@conv_chk=""),"{IND}",IF(@conv_chk<=0,"{IND}",@cpchk/@conv_chk))', BRL, "dado real", "custo por checkout efetivo ÷ conversão real do checkout.")
    M(19, "maxchk", "Custo máximo por checkout no CPA desejado (R$)", f'=IF(@conv_chk="","{IND}",#cpades*@conv_chk)', BRL, "", "CPA desejado × conversão do checkout.")
    M(20, "maxchk_be", "Custo máximo por checkout no equilíbrio (R$)", f'=IF(@conv_chk="","{IND}",#cpamax*@conv_chk)', BRL, "", "CPA máximo × conversão do checkout.")
    M(21, "pe_dia", "Vendas por dia de equilíbrio para o teto (vendas/dia)", f'=IF(#mc<=0,"{IND}",@teto/#mc)', NUM, "", "teto diário ÷ margem de contribuição: abaixo disso, o dia fecha negativo.")
    M(22, "pe_alvo", "Vendas por dia para a margem alvo no teto", f'=IF(#cpades<=0,"{IND}",@teto/#cpades)', NUM, "[H]", "teto diário ÷ CPA desejado.")
    M(23, "pe_sem", "Vendas por semana de equilíbrio", f'=IF(ISNUMBER(#pe_dia),#pe_dia*7,"{IND}")', NUM, "", "")
    M(24, "chk_dia", "Checkouts efetivos por dia que o teto compra", f'=IF(@cpchk="","{IND}",@teto/@cpchk)', NUM, "dado real", "teto ÷ custo por checkout.")
    M(25, "vend_dia", "Vendas por dia projetadas no teto", f'=IF(OR(NOT(ISNUMBER(#chk_dia)),@conv_chk=""),"{IND}",#chk_dia*@conv_chk)', NUM, "dado real", "")
    M(26, "res_dia", "Resultado de mídia diário projetado (R$)", f'=IF(NOT(ISNUMBER(#vend_dia)),"{IND}",#vend_dia*#mc-@teto)', BRL, "dado real", "vendas/dia × margem de contribuição − teto. Projeção, não resultado.")
    M(27, "cg", "Capital de giro: gasto a financiar até o recebimento (R$)", f'=IF(@prazo_pix="","{IND}",IF(AND(@mix_pix<1,@prazo_cartao=""),"{IND}",@teto*(@mix_pix*@prazo_pix+(1-@mix_pix)*N(@prazo_cartao))))', BRL, "[NC]", "teto diário × prazo médio de recebimento. Prazos ainda não confirmados.")
    M(28, "ltv", "LTV conservador (R$)", "=#mc", BRL, "[E]", "Só compra única comprovada: nenhuma recompra comprovada, nenhum upsell comprovado. 30/60/90/180/365 dias = o mesmo valor.")
    # cenário segundo produto
    wm.cell(row=30, column=1, value="Cenário rotulado: segundo produto (NÃO usar para justificar prejuízo de mídia)").font = Font(bold=True, color="8B714E")
    put(wm, 31, "p2", "Probabilidade de compra de um 2º produto (%)", inputs.get("p2", 0.0), PCT, "in", "[H]", "Cenário. Padrão 0: sem evidência.", local=lm)
    put(wm, 32, "mc2", "Margem de contribuição do 2º produto (R$)", inputs.get("mc2", 0), BRL, "in", "[H]", "Cenário.", local=lm)
    put(wm, 33, "ltv2", "LTV cenário = margem de contribuição + prob. × margem do 2º (R$)", "=#mc+#p2*#mc2", BRL, "calc", "[H]", "Hipótese. A decisão abaixo NÃO usa este valor.", local=lm)
    for k in ("p2", "mc2", "ltv2"): CELLS["mm_" + k] = f"{q(S_MM)}!$B${ {'p2':31,'mc2':32,'ltv2':33}[k] }"
    # decisão
    wm.cell(row=35, column=1, value="Decisão pela faixa de CPA projetado").font = Font(bold=True, color="8B714E")
    dec = (f'=IF(#mc<=0,"PAUSAR: a margem não cobre a mídia",IF(#cpaproj="{IND}","SEM DECISÃO: falta custo por checkout efetivo e conversão real",'
           f'IF(OR(N(@obs_chk)<@min_chk,N(@obs_vendas)<@min_vendas),"AMOSTRA PEQUENA: manter o teto e coletar dados",'
           f'IF(#cpaproj<=#cpades,"ESCALAR (com aprovado de Bruno)",IF(#cpaproj<=#cpamax,"MANTER","PAUSAR (com aprovado de Bruno)")))))')
    put(wm, 36, "decisao", "Decisão pelo modelo agora", dec, "General", "calc", "", "Só vale com amostra mínima (Parâmetros 29 a 32). A execução depende de 'aprovado'.", local=lm)
    CELLS["mm_decisao"] = f"{q(S_MM)}!$B$36"
    hdr(wm, 38, ["Faixa do CPA projetado", "Limite (R$)", "Decisão", "Regra"])
    rows = [
        ("Sem dado ou amostra abaixo do mínimo", "—", "NÃO DECIDIR", "Manter o teto de R$ 60/dia e coletar. Nunca decidir por 'parece que vai'."),
        ("CPA projetado ≤ CPA desejado", "=#cpades", "ESCALAR", "Subir o orçamento em degraus, um por vez, só com 'aprovado' de Bruno. Reavaliar a cada degrau."),
        ("CPA desejado < CPA projetado ≤ CPA máximo", "=#cpamax", "MANTER", "Cobre a mídia, mas sem a margem alvo. Manter o teto, otimizar criativo/checkout."),
        ("CPA projetado > CPA máximo", "=#cpamax", "PAUSAR", "Cada venda perde dinheiro. Pausar (com 'aprovado') e corrigir antes de gastar mais."),
    ]
    for i, (a, b, c, d) in enumerate(rows, start=39):
        wm.cell(row=i, column=1, value=a).alignment = Alignment(wrap_text=True)
        cc = wm.cell(row=i, column=2, value=sub(b, lm, S_MM) if b.startswith("=") else b); cc.number_format = BRL; cc.fill = GRN if b.startswith("=") else GRY
        wm.cell(row=i, column=3, value=c).font = Font(bold=True); wm.cell(row=i, column=4, value=d).alignment = Alignment(wrap_text=True)
    wm["A44"] = "Regra escrita"; wm["A44"].font = Font(bold=True)
    wm["B44"] = "A venda do infoproduto precisa financiar a aquisição. Não se aceita perda inicial justificada por LTV hipotético: o LTV da decisão é só o de compra única comprovada. Faturamento não é lucro."
    wm["B44"].alignment = Alignment(wrap_text=True)
    wm.merge_cells("B44:D44"); wm.row_dimensions[44].height = 48
    wm.column_dimensions["A"].width = 56; wm.column_dimensions["B"].width = 22; wm.column_dimensions["C"].width = 14; wm.column_dimensions["D"].width = 90
    for r in range(4, 34): wm.row_dimensions[r].height = 30

    # ---------------- Outros produtos
    wo = wb.create_sheet(S_OUT)
    title(wo, "Outros produtos · CPA máximo e viabilidade de tráfego direto", "Preços lidos das ofertas do ClickMax em 25/11/2026 [E]. Taxa: regra 1 = só taxa fixa; regra 2 = taxa fixa + taxa % (cenário conservador).")
    wo["A3"] = "Regra 1 observada em R$ 19 e R$ 47; regra 2 observada em R$ 97 e R$ 270 [E]. Para R$ 13, R$ 27 e R$ 67 não há venda para medir: regra 1 como [H] (taxa fixa de R$ 2,49 estimada), regra 2 mostrada como conservadora. Taxa variável do cartão: [NC]."
    wo["A3"].alignment = Alignment(wrap_text=True); wo.merge_cells("A3:Q3"); wo.row_dimensions[3].height = 44
    heads = ["Produto (preço)", "Oferta (id)", "Status da oferta [E]", "Preço (R$)", "Regra de taxa adotada (1 ou 2)", "Etiqueta da taxa",
             "Líquido regra 1 (R$)", "Líquido regra 2 (R$)", "Líquido adotado (R$)", "CPA máximo (R$)", "CPA máx. % do preço", "ROAS de equilíbrio",
             "CPA máx. conservador, regra 2 (R$)", "ROAS equilíbrio conservador", "Taxa fixa como % do preço", "CPC máximo (R$) com conv. clique→venda do Parâmetros", "Ranking de viabilidade (1 = mais folga)"]
    hdr(wo, 5, heads); wo.row_dimensions[5].height = 62
    prods = [
        ("E-books Kit R$ 13 (3 ofertas)", "3852a88a…", "approved", 13, 1, "[H]"),
        ("Ferramentas R$ 19 (utilitários e combos, ~20 ofertas)", "ver CLAUDE.md §4", "approved (maioria)", 19, 1, "[E]"),
        ("Arsenal Interativo 01 R$ 27", "1ff56fea", "incomplete", 27, 1, "[H]"),
        ("Clube: microofertas R$ 27 (~20 ofertas)", "f44d1d87…", "approved/incomplete", 27, 1, "[H]"),
        ("Mini Mentoria de Estruturação R$ 47 (produto analisado)", "0c71eeba", "approved", 47, 1, "[E]"),
        ("Zion Collection 06 R$ 47", "75c27213", "approved", 47, 1, "[E]"),
        ("Você tem terra. Falta capital? (A) R$ 47", "1eb339a6", "approved", 47, 1, "[E]"),
        ("Kit Inicial de Captação R$ 47", "50fd0b0a", "approved", 47, 1, "[E]"),
        ("Você tem terra. Falta capital? (B) R$ 67", "338c9ed8", "approved", 67, 1, "[H]"),
        ("Legado R$ 97 (Clube, acesso à plataforma)", "c298aaed", "approved", 97, 2, "[E]"),
        ("Clube: Kit de Captação + sessão estratégica R$ 97", "5b89a932", "pending_corrections", 97, 2, "[E]"),
        ("Clube: inscrição + Land Bank R$ 270", "c627c32e", "incomplete", 270, 2, "[E]"),
    ]
    r0 = 6; rowof = {}
    for i, (nm, oid, st, pr, rg, tg) in enumerate(prods):
        r = r0 + i; rowof[nm] = r
        wo.cell(row=r, column=1, value=nm).alignment = Alignment(wrap_text=True)
        wo.cell(row=r, column=2, value=oid); wo.cell(row=r, column=3, value=st)
        for col, v, fm in ((4, pr, BRL), (5, rg, INT)):
            c = wo.cell(row=r, column=col, value=v); c.fill = YEL; c.number_format = fm; c.border = BOX
        wo.cell(row=r, column=6, value=tg).font = Font(bold=True, color="8B714E")
        fx, pc = CELLS["tx_fixa"], CELLS["tx_pct_alta"]
        F = {
            7: f"=D{r}-{fx}", 8: f"=D{r}-{fx}-{pc}*D{r}", 9: f"=IF(E{r}=1,G{r},H{r})",
            10: f"=I{r}-{CELLS['imposto']}*D{r}-{CELLS['custos_var']}-{CELLS['reemb']}*I{r}",
            11: f"=J{r}/D{r}", 12: f'=IF(J{r}<=0,"{IND}",D{r}/J{r})',
            13: f"=H{r}-{CELLS['imposto']}*D{r}-{CELLS['custos_var']}-{CELLS['reemb']}*H{r}",
            14: f'=IF(M{r}<=0,"{IND}",D{r}/M{r})', 15: f"={fx}/D{r}", 16: f"=J{r}*{CELLS['conv_clique']}",
            17: f"=RANK(J{r},$J${r0}:$J${r0+len(prods)-1},0)",
        }
        fm = {7: BRL, 8: BRL, 9: BRL, 10: BRL, 11: PCT, 12: NUM, 13: BRL, 14: NUM, 15: PCT, 16: BRL, 17: INT}
        for col, f in F.items():
            c = wo.cell(row=r, column=col, value=f); c.fill = GRN; c.number_format = fm[col]; c.border = BOX
    last = r0 + len(prods) - 1
    CELLS["out_first"], CELLS["out_last"] = r0, last
    rA = rowof["Ferramentas R$ 19 (utilitários e combos, ~20 ofertas)"]; rB = rowof["Mini Mentoria de Estruturação R$ 47 (produto analisado)"]
    b = last + 3
    wo.cell(row=b, column=1, value="Por que R$ 19 é difícil de financiar com anúncio direto (matemática, sem dado de mercado)").font = Font(bold=True, size=12, color="1B2117")
    hdr(wo, b + 1, ["Comparação", "R$ 19 (ferramenta)", "R$ 47 (Mini Mentoria)", "Razão R$ 19 ÷ R$ 47", "Leitura"])
    comp = [
        ("CPA máximo (R$)", f"=J{rA}", f"=J{rB}", BRL, "É o teto que a mídia pode pagar por venda."),
        ("Taxa fixa como % do preço", f"=O{rA}", f"=O{rB}", PCT, "A taxa fixa de R$ 2,49 pesa 2,5 vezes mais num produto de R$ 19."),
        ("Vendas/dia para cobrir o teto de mídia", f"={CELLS['teto']}/J{rA}", f"={CELLS['teto']}/J{rB}", NUM, "Para o mesmo gasto diário, o R$ 19 precisa de quase 3 vezes mais vendas."),
        ("Custo máximo por clique (R$) com a conversão clique→venda do Parâmetros [H]", f"=P{rA}", f"=P{rB}", BRL, "O CPC que fecha a conta é proporcional ao CPA máximo: mesma conversão, teto muito menor."),
        ("Vendas de R$ 19 necessárias para pagar 1 venda de R$ 47 em contribuição", f"=J{rB}/J{rA}", 1, NUM, "Cada venda de R$ 47 contribui como 2,7 vendas de R$ 19."),
    ]
    for i, (a_, f1, f2, fmt, note) in enumerate(comp, start=b + 2):
        wo.cell(row=i, column=1, value=a_).alignment = Alignment(wrap_text=True)
        for col, f in ((2, f1), (3, f2)):
            c = wo.cell(row=i, column=col, value=f); c.fill = GRN; c.number_format = fmt; c.border = BOX
        c = wo.cell(row=i, column=4, value=f'=IF(C{i}=0,"{IND}",B{i}/C{i})'); c.fill = GRN; c.number_format = NUM; c.border = BOX
        wo.cell(row=i, column=5, value=note).alignment = Alignment(wrap_text=True)
        wo.row_dimensions[i].height = 34
    CELLS["out_comp_row"] = b + 2
    wo.cell(row=b + 8, column=1, value="Conclusão: ticket menor = CPA máximo mais apertado. R$ 19 e R$ 13 servem como degrau de entrada para base própria e orgânico; como produto de aquisição paga direta a conta só fecha com CPA muito baixo. Leitura matemática, não promessa. Clube R$ 97 e R$ 270 têm CPA máximo mais folgado, mas dependem de oferta aprovada e condições comerciais próprias.").alignment = Alignment(wrap_text=True)
    wo.merge_cells(start_row=b + 8, start_column=1, end_row=b + 8, end_column=10); wo.row_dimensions[b + 8].height = 62
    widths = [46, 18, 18, 11, 14, 10, 13, 13, 13, 13, 12, 12, 16, 14, 12, 18, 14]
    for i, w in enumerate(widths, start=1): wo.column_dimensions[get_column_letter(i)].width = w

    # ---------------- Cenários
    wc = wb.create_sheet(S_CEN)
    title(wc, "Cenários · tudo hipótese [H], nenhum resultado", "Matriz de CPA projetado e cenários de taxa, imposto e reembolso para a Mini Mentoria. Os eixos (amarelo) podem ser trocados.")
    wc["A4"] = "1) CPA projetado = custo por checkout efetivo (linhas) ÷ conversão checkout→venda (colunas)"; wc["A4"].font = Font(bold=True, color="8B714E")
    convs = [0.03, 0.05, 0.08, 0.12, 0.20]; cks = [2, 4, 6, 8, 10, 15]
    wc.cell(row=5, column=1, value="Custo por checkout (R$) \\ Conversão").font = Font(bold=True)
    for j, cv in enumerate(convs):
        c = wc.cell(row=5, column=2 + j, value=cv); c.fill = YEL; c.number_format = PCT; c.border = BOX
    for i, ck in enumerate(cks):
        r = 6 + i
        c = wc.cell(row=r, column=1, value=ck); c.fill = YEL; c.number_format = BRL; c.border = BOX
        for j in range(len(convs)):
            col = get_column_letter(2 + j)
            c = wc.cell(row=r, column=2 + j, value=f"=$A{r}/{col}$5"); c.fill = GRN; c.number_format = BRL; c.border = BOX
    wc["A13"] = "Faixa de decisão da matriz acima (E = escalar, M = manter, P = pausar), com o CPA máximo e o desejado da aba Mini Mentoria 47"; wc["A13"].font = Font(bold=True, color="8B714E")
    for j in range(len(convs)):
        c = wc.cell(row=14, column=2 + j, value=f"={get_column_letter(2+j)}5"); c.number_format = PCT; c.fill = GRY
    for i in range(len(cks)):
        r = 15 + i
        c = wc.cell(row=r, column=1, value=f"=A{6+i}"); c.number_format = BRL; c.fill = GRY
        for j in range(len(convs)):
            col = get_column_letter(2 + j)
            f = f'=IF({CELLS["mm_cpamax"]}<=0,"P",IF({col}{6+i}<={CELLS["mm_cpades"]},"E",IF({col}{6+i}<={CELLS["mm_cpamax"]},"M","P")))'
            c = wc.cell(row=r, column=2 + j, value=f); c.fill = GRN; c.alignment = Alignment(horizontal="center"); c.border = BOX
    wc["A22"] = "2) Cenários de taxa, imposto, cartão e reembolso (CPA máximo)"; wc["A22"].font = Font(bold=True, color="8B714E")
    hdr(wc, 23, ["Item", "A · Base (evidência)", "B · Com cartão [H]", "C · Conservador [H]", "Observação"])
    sc = {
        "Preço (R$)": (f"={CELLS['preco']}", f"={CELLS['preco']}", f"={CELLS['preco']}", BRL, "in=link"),
        "Taxa fixa Pix (R$)": (f"={CELLS['tx_fixa']}", f"={CELLS['tx_fixa']}", f"={CELLS['tx_fixa']}", BRL, ""),
        "Taxa % Pix": (0.0, 0.0, f"={CELLS['tx_pct_alta']}", PCT, "C aplica 6,99% (observada em R$ 97/R$ 270) como teste de estresse."),
        "Mix Pix": (1.0, 0.7, 0.7, PCT, "B e C: 30% de cartão é hipótese."),
        "Taxa fixa cartão (R$)": (0, 2.49, 2.49, BRL, "[H] igual ao Pix só para simular; taxa real do cartão [NC]."),
        "Taxa % cartão": (0.0, 0.0699, 0.0699, PCT, "[H] mesma % do estresse; taxa real [NC]."),
        "Imposto (% do preço)": (f"={CELLS['imposto']}", f"={CELLS['imposto']}", 0.06, PCT, "C: 6% é simulação, NÃO é a alíquota da Zion (a definir)."),
        "Custos variáveis (R$)": (f"={CELLS['custos_var']}", f"={CELLS['custos_var']}", 1.0, BRL, "C: R$ 1,00 por venda é simulação."),
        "Reembolso (%)": (f"={CELLS['reemb']}", f"={CELLS['reemb']}", 0.05, PCT, "C: 5% é simulação."),
    }
    rr = 24; srow = {}
    for k, (a_, b_, c_, fmt, note) in sc.items():
        wc.cell(row=rr, column=1, value=k); srow[k] = rr
        for col, v in ((2, a_), (3, b_), (4, c_)):
            c = wc.cell(row=rr, column=col, value=v); c.number_format = fmt; c.border = BOX
            c.fill = GRN if (isinstance(v, str) and v.startswith("=")) else YEL
        wc.cell(row=rr, column=5, value=note.replace("in=link", "")); rr += 1
    calc = [
        ("Líquido médio (R$)", lambda L: f"={L}{srow['Mix Pix']}*({L}{srow['Preço (R$)']}-{L}{srow['Taxa fixa Pix (R$)']}-{L}{srow['Taxa % Pix']}*{L}{srow['Preço (R$)']})+(1-{L}{srow['Mix Pix']})*({L}{srow['Preço (R$)']}-{L}{srow['Taxa fixa cartão (R$)']}-{L}{srow['Taxa % cartão']}*{L}{srow['Preço (R$)']})", BRL),
    ]
    liq_r = rr
    wc.cell(row=liq_r, column=1, value="Líquido médio (R$)")
    cpa_r, roas_r, pe_r = liq_r + 1, liq_r + 2, liq_r + 3
    wc.cell(row=cpa_r, column=1, value="CPA máximo (R$)"); wc.cell(row=roas_r, column=1, value="ROAS de equilíbrio"); wc.cell(row=pe_r, column=1, value="Vendas/dia de equilíbrio no teto")
    for col in "BCD":
        P_, TF, TP, MX, FC, PC_, IM, CV, RB = (f"{col}{srow[k]}" for k in sc)
        wc[f"{col}{liq_r}"] = f"={MX}*({P_}-{TF}-{TP}*{P_})+(1-{MX})*({P_}-{FC}-{PC_}*{P_})"
        wc[f"{col}{cpa_r}"] = f"={col}{liq_r}-{IM}*{P_}-{CV}-{RB}*{col}{liq_r}"
        wc[f"{col}{roas_r}"] = f'=IF({col}{cpa_r}<=0,"{IND}",{P_}/{col}{cpa_r})'
        wc[f"{col}{pe_r}"] = f'=IF({col}{cpa_r}<=0,"{IND}",{CELLS["teto"]}/{col}{cpa_r})'
        for r_, fm in ((liq_r, BRL), (cpa_r, BRL), (roas_r, NUM), (pe_r, NUM)):
            c = wc[f"{col}{r_}"]; c.fill = GRN; c.number_format = fm; c.border = BOX
    CELLS["cen_liq_row"], CELLS["cen_cpa_row"], CELLS["cen_roas_row"], CELLS["cen_pe_row"] = liq_r, cpa_r, roas_r, pe_r
    g = pe_r + 3
    wc.cell(row=g, column=1, value="3) Capital de giro por prazo de recebimento [H]: gasto a financiar = teto × prazo").font = Font(bold=True, color="8B714E")
    hdr(wc, g + 1, ["Prazo (dias)", "Gasto a financiar (R$)", "", "", "Observação"])
    for i, d in enumerate([1, 2, 7, 14, 30]):
        r = g + 2 + i
        c = wc.cell(row=r, column=1, value=d); c.fill = YEL; c.border = BOX
        c = wc.cell(row=r, column=2, value=f"={CELLS['teto']}*A{r}"); c.fill = GRN; c.number_format = BRL; c.border = BOX
    wc.cell(row=g + 2, column=5, value="Prazos reais da Ticto: [NC]. O gasto do Meta sai antes da entrada do dinheiro.")
    CELLS["cen_cg_row"] = g + 2
    wc.column_dimensions["A"].width = 44
    for col in "BCD": wc.column_dimensions[col].width = 20
    wc.column_dimensions["E"].width = 70; wc.column_dimensions["F"].width = 14

    # ---------------- Conciliação
    wk = wb.create_sheet(S_CON)
    title(wk, "Conciliação · gasto × vendas ClickMax × vendas Ticto", "Preencher com dados reais FORA do repositório (arquivo público). Compras de teste internas não entram.")
    hdr(wk, 4, ["Data", "Campanha / rótulo", "Gasto Meta (R$)", "Vendas externas confirmadas (ClickMax)", "Vendas na Ticto", "Receita bruta (R$)", "Líquido recebido (R$)",
                "Divergência de vendas (ClickMax − Ticto)", "CPA real (R$)", "ROAS realizado", "Resultado de mídia (R$)", "CPA real × CPA máximo"])
    wk.row_dimensions[4].height = 58
    c0, c1 = 5, 24
    for r in range(c0, c1 + 1):
        for col in range(1, 8):
            c = wk.cell(row=r, column=col); c.fill = YEL; c.border = BOX
            c.number_format = {1: "dd/mm/yyyy", 3: BRL, 4: INT, 5: INT, 6: BRL, 7: BRL}.get(col, "General")
        F = {8: f'=IF(OR(D{r}="",E{r}=""),"",D{r}-E{r})',
             9: f'=IF(OR(C{r}="",D{r}=""),"",IF(D{r}=0,"sem venda",C{r}/D{r}))',
             10: f'=IF(OR(C{r}="",F{r}=""),"",IF(C{r}=0,"sem gasto",F{r}/C{r}))',
             11: f'=IF(OR(C{r}="",G{r}=""),"",G{r}-C{r})',
             12: f'=IF(NOT(ISNUMBER(I{r})),"",IF(I{r}<={CELLS["mm_cpamax"]},"dentro do máximo","acima do máximo"))'}
        fm = {8: INT, 9: BRL, 10: NUM, 11: BRL, 12: "General"}
        for col, f in F.items():
            c = wk.cell(row=r, column=col, value=f); c.fill = GRN; c.number_format = fm[col]; c.border = BOX
    t = c1 + 1
    wk.cell(row=t, column=1, value="TOTAL").font = Font(bold=True)
    for col, L in ((3, "C"), (4, "D"), (5, "E"), (6, "F"), (7, "G")):
        c = wk.cell(row=t, column=col, value=f"=SUM({L}{c0}:{L}{c1})"); c.fill = GRN; c.border = BOX; c.number_format = {3: BRL, 4: INT, 5: INT, 6: BRL, 7: BRL}[col]
    wk.cell(row=t, column=8, value=f"=D{t}-E{t}").fill = GRN
    wk.cell(row=t, column=9, value=f'=IF(D{t}=0,"sem venda",C{t}/D{t})').fill = GRN; wk.cell(row=t, column=9).number_format = BRL
    wk.cell(row=t, column=10, value=f'=IF(C{t}=0,"sem gasto",F{t}/C{t})').fill = GRN; wk.cell(row=t, column=10).number_format = NUM
    wk.cell(row=t, column=11, value=f"=G{t}-C{t}").fill = GRN; wk.cell(row=t, column=11).number_format = BRL
    wk.cell(row=t, column=12, value=f'=IF(NOT(ISNUMBER(I{t})),"",IF(I{t}<={CELLS["mm_cpamax"]},"dentro do máximo","acima do máximo"))').fill = GRN
    CELLS["con_first"], CELLS["con_last"], CELLS["con_total"] = c0, c1, t
    wk.cell(row=t + 2, column=1, value="Atenção: CPA real só vale quando a venda tem origem (UTM) confirmada para a campanha; sem origem, a coluna de CPA é um limite superior de atribuição, não prova.").alignment = Alignment(wrap_text=True)
    wk.merge_cells(start_row=t + 2, start_column=1, end_row=t + 2, end_column=12); wk.row_dimensions[t + 2].height = 34
    for i, w in enumerate([12, 40, 14, 18, 12, 14, 14, 18, 14, 12, 16, 20], start=1): wk.column_dimensions[get_column_letter(i)].width = w

    for w_ in wb.worksheets: w_.sheet_view.showGridLines = False
    wb.save(path)
    return CELLS

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "modelo_financeiro.xlsx"
    build(out); print("ok", out)

"""Gera a Ferramenta 12 · Checklist de Fotos e Comodidades do Anúncio (Zion Hospitality Business):
   - Fotos-Comodidades-Zion-EM-BRANCO.xlsx / Fotos-Comodidades-Zion-EXEMPLO.xlsx (dados fictícios)
Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dados import SIM_NAO, STATUS, FOTOS, COMODIDADES, EX_FOTOS, EX_FOTOS_EXCLUIR, EX_COM
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, PRETO, CREME, TERRA = "1B2117", "040605", "FEF5F0", "8B714E"
ENTRADA, CALC, CAB = PatternFill("solid", fgColor="FFF4C7"), PatternFill("solid", fgColor="E3EEDF"), PatternFill("solid", fgColor=MUSGO)
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)
WRAP = Alignment(wrap_text=True, vertical="center")
F0, NF = 6, 60         # fotos: linhas 6..65
K0, NK = 6, 60         # comodidades: linhas 6..65
VERDE, VERM, AMAR, CINZA = "C8E6C0", "F4C7C3", "FCE8B2", "E6E6E6"

def cab(ws, l, tit):
    for j, t in enumerate(tit, 1):
        c = ws.cell(l, j, t); c.font = T(10, True, CREME); c.fill = CAB; c.alignment = WRAP; c.border = borda
    ws.row_dimensions[l].height = 42
def ent(c, v=None):
    c.value = v; c.fill = ENTRADA; c.border = borda; c.alignment = WRAP; c.font = T(10)
def calc(c, f, b=False):
    c.value = f; c.fill = CALC; c.border = borda; c.alignment = WRAP; c.font = T(10, b)
def lista(ws, rng, opcoes):
    dv = DataValidation(type="list", formula1='"' + ",".join(opcoes) + '"', allow_blank=True, showErrorMessage=True,
                        errorTitle="Opção inválida", error="Escolha uma opção da lista.")
    ws.add_data_validation(dv); dv.add(rng)

def montar(exemplo):
    wb = Workbook(); ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 104
    linhas = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 12", T(10, True, TERRA)),
        ("Checklist de Fotos e Comodidades do Anúncio", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para planejar as fotos do seu anúncio, acompanhar cada uma até a publicação e conferir se o que está marcado no anúncio existe de verdade na hospedagem.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (um chalé inventado). Use a versão em branco." if exemplo
         else "Versão em branco: a lista de fotos e de comodidades já vem pronta para você ajustar. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Para Airbnb, casas, apartamentos, pousadas e glampings.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 4 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Fotos: ajuste a lista de fotos (apague o que não existe na sua casa, acrescente o que a diferencia) e marque quais são obrigatórias.", None),
        ("2. No dia das fotos, atualize a situação de cada uma: Falta tirar, Tirada, Aprovada (você escolheu a melhor) e Publicada. Dê a ordem em que ela aparece no anúncio.", None),
        ("3. Aba Comodidades: para cada item, responda se existe na hospedagem, se está marcado no anúncio e se tem foto.", None),
        ("4. Aba Painel: veja o que corrigir primeiro. Comece sempre por tirar do anúncio o que não existe.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("COMO A PLANILHA DECIDE", T(12, True, MUSGO)),
        ("Fotos: uma foto obrigatória só fica OK quando está Aprovada ou Publicada. Foto publicada precisa de ordem. Duas fotos com a mesma ordem aparecem como Ordem repetida. Situação em branco conta como Falta tirar.", None),
        ("Comodidades: marcada no anúncio e não existe = Remover do anúncio (o hóspede espera encontrar). Existe e não está marcada = Marcar no anúncio. Existe, está marcada e é de destaque, mas sem foto = Falta foto.", None),
        ("", None),
        ("O QUE A PLANILHA NÃO FAZ", T(12, True, MUSGO)),
        ("Não tira nem edita fotos, não acessa o seu anúncio e não sabe o que cada plataforma mostra primeiro. A lista é um ponto de partida: confira as comodidades que a sua plataforma oferece.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Fotos ----------
    fo = wb.create_sheet("Fotos"); fo.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFG", (16, 44, 12, 14, 10, 26, 30)): fo.column_dimensions[col].width = w
    fo["A1"] = "Lista de fotos"; fo["A1"].font = T(18, True, MUSGO)
    fo["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Apague o que não existe na sua casa e acrescente o que a diferencia."
    fo["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    fo["A3"] = "Ordem: a posição da foto no anúncio (1 = capa). Situação em branco conta como Falta tirar."; fo["A3"].font = T(9, c="5F5F55", i=True)
    cab(fo, 5, ["Ambiente", "O que a foto mostra", "Obrigatória?", "Situação", "Ordem no anúncio", "Observação", "Alerta"])
    lin = [f for i, f in enumerate(FOTOS) if not (exemplo and i in EX_FOTOS_EXCLUIR)]
    idx = [i for i in range(len(FOTOS)) if not (exemplo and i in EX_FOTOS_EXCLUIR)]
    rgE = f"$E${F0}:$E${F0+NF-1}"
    for k in range(NF):
        r = F0 + k
        if k < len(lin):
            a, b, c = lin[k]; st, ordem = EX_FOTOS.get(idx[k], ("Falta tirar", None)) if exemplo else (None, None)
        else: a = b = c = st = ordem = None
        for col, v in zip("ABCDEF", (a, b, c, st, ordem, None)): ent(fo[f"{col}{r}"], v)
        calc(fo[f"G{r}"], f'=IF(AND(A{r}="",B{r}=""),"",IF(B{r}="","Descreva a foto",IF(AND(C{r}<>"Sim",C{r}<>"Não"),"Diga se é obrigatória",'
                          f'IF(AND(E{r}<>"",OR(NOT(ISNUMBER(E{r})),E{r}<1)),"Confira a ordem",IF(AND(ISNUMBER(E{r}),E{r}<>INT(E{r})),"Confira a ordem",'
                          f'IF(AND(ISNUMBER(E{r}),COUNTIF({rgE},E{r})>1),"Ordem repetida",IF(AND(D{r}="Publicada",E{r}=""),"Publicada sem ordem",'
                          f'IF(AND(C{r}="Sim",D{r}<>"Aprovada",D{r}<>"Publicada"),"Obrigatória ainda não aprovada","OK"))))))))', True)
    lista(fo, f"C{F0}:C{F0+NF-1}", SIM_NAO); lista(fo, f"D{F0}:D{F0+NF-1}", STATUS)
    rgG = f"G{F0}:G{F0+NF-1}"
    fo.conditional_formatting.add(rgG, FormulaRule(formula=[f'G{F0}="OK"'], fill=PatternFill("solid", fgColor=VERDE)))
    fo.conditional_formatting.add(rgG, FormulaRule(formula=[f'G{F0}="Obrigatória ainda não aprovada"'], fill=PatternFill("solid", fgColor=AMAR)))
    fo.conditional_formatting.add(rgG, FormulaRule(formula=[f'AND(G{F0}<>"",G{F0}<>"OK",G{F0}<>"Obrigatória ainda não aprovada")'], fill=PatternFill("solid", fgColor=VERM)))
    fo.freeze_panes = f"C{F0}"

    # ---------- Comodidades ----------
    co = wb.create_sheet("Comodidades"); co.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFG", (28, 16, 12, 12, 13, 10, 24)): co.column_dimensions[col].width = w
    co["A1"] = "Comodidades: casa × anúncio"; co["A1"].font = T(18, True, MUSGO)
    co["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Confira na casa, não de memória. Acrescente as comodidades que a sua plataforma oferece."
    co["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    co["A3"] = "Precisa de foto: Sim para o que é destaque e o hóspede quer ver (hidro, lareira, vista, vaga)."; co["A3"].font = T(9, c="5F5F55", i=True)
    cab(co, 5, ["Comodidade", "Categoria", "Precisa de foto?", "Existe na hospedagem?", "Está marcada no anúncio?", "Tem foto?", "Situação"])
    for k in range(NK):
        r = K0 + k
        if k < len(COMODIDADES):
            n, cat, pf = COMODIDADES[k]; ex = EX_COM.get(n, (None,) * 3) if exemplo else (None,) * 3
        else: n = cat = pf = None; ex = (None,) * 3
        for col, v in zip("ABCDEF", (n, cat, pf) + tuple(ex)): ent(co[f"{col}{r}"], v)
        calc(co[f"G{r}"], f'=IF(A{r}="","",IF(OR(AND(D{r}<>"Sim",D{r}<>"Não"),AND(E{r}<>"Sim",E{r}<>"Não")),"Responda: existe e está marcada?",'
                          f'IF(AND(D{r}="Não",E{r}="Sim"),"Remover do anúncio",IF(AND(D{r}="Sim",E{r}="Não"),"Marcar no anúncio",'
                          f'IF(D{r}="Não","Não se aplica",IF(AND(C{r}="Sim",F{r}<>"Sim"),"Falta foto","OK"))))))', True)
    lista(co, f"C{K0}:F{K0+NK-1}", SIM_NAO)
    rgS = f"G{K0}:G{K0+NK-1}"
    for cond, cor in ((f'G{K0}="OK"', VERDE), (f'G{K0}="Remover do anúncio"', VERM), (f'G{K0}="Marcar no anúncio"', AMAR),
                      (f'G{K0}="Falta foto"', AMAR), (f'G{K0}="Não se aplica"', CINZA), (f'LEFT(G{K0},8)="Responda"', VERM)):
        co.conditional_formatting.add(rgS, FormulaRule(formula=[cond], fill=PatternFill("solid", fgColor=cor)))
    co.freeze_panes = f"B{K0}"

    # ---------- Painel ----------
    p = wb.create_sheet("Painel"); p.sheet_view.showGridLines = False
    p.column_dimensions["A"].width = 46; p.column_dimensions["B"].width = 16
    p["A1"] = "Painel do anúncio"; p["A1"].font = T(18, True, MUSGO)
    p["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Tudo calculado."; p["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    fr = lambda c: f"Fotos!${c}${F0}:${c}${F0+NF-1}"; cr = lambda c: f"Comodidades!${c}${K0}:${c}${K0+NK-1}"
    itens = [
        ("FOTOS", None),
        ("Fotos na lista", f'=COUNTIF({fr("B")},"?*")'),
        ("Fotos obrigatórias", f'=COUNTIFS({fr("C")},"Sim",{fr("B")},"?*")'),
        ("Obrigatórias aprovadas ou publicadas", f'=COUNTIFS({fr("C")},"Sim",{fr("B")},"?*",{fr("D")},"Aprovada")+COUNTIFS({fr("C")},"Sim",{fr("B")},"?*",{fr("D")},"Publicada")'),
        ("Fotos publicadas", f'=COUNTIFS({fr("D")},"Publicada",{fr("B")},"?*")'),
        ("Fotos com alerta", f'=COUNTIF({fr("G")},"?*")-COUNTIF({fr("G")},"OK")'),
        ("Ordens repetidas", f'=COUNTIF({fr("G")},"Ordem repetida")'),
        ("COMODIDADES", None),
        ("Remover do anúncio (marcada e não existe)", f'=COUNTIF({cr("G")},"Remover do anúncio")'),
        ("Marcar no anúncio (existe e não está marcada)", f'=COUNTIF({cr("G")},"Marcar no anúncio")'),
        ("Falta foto de comodidade de destaque", f'=COUNTIF({cr("G")},"Falta foto")'),
        ("Sem resposta", f'=COUNTIF({cr("G")},"Responda*")'),
        ("OK", f'=COUNTIF({cr("G")},"OK")'),
    ]
    r = 4; ref = {}
    for rot, f in itens:
        if f is None:
            p[f"A{r}"] = rot; p[f"A{r}"].font = T(11, True, TERRA)
        else:
            p[f"A{r}"] = rot; p[f"A{r}"].font = T(10, True); calc(p[f"B{r}"], f, True); ref[rot] = f"B{r}"
        r += 1
    r += 1; p[f"A{r}"] = "O que fazer primeiro"; p[f"A{r}"].font = T(12, True, MUSGO)
    R_ = ref
    calc(p[f"A{r+1}"], f'=IF({R_["Remover do anúncio (marcada e não existe)"]}>0,"1º: tire do anúncio o que não existe na hospedagem",'
                       f'IF({R_["Fotos com alerta"]}>0,"Resolva os alertas da aba Fotos",IF({R_["Marcar no anúncio (existe e não está marcada)"]}>0,"Marque no anúncio as comodidades que você tem",'
                       f'IF({R_["Falta foto de comodidade de destaque"]}>0,"Fotografe as comodidades de destaque",IF({R_["Sem resposta"]}>0,"Responda as comodidades em branco",'
                       f'IF({R_["Fotos na lista"]}=0,"Monte a lista de fotos","Pronto: confira o anúncio com esta lista"))))))', True)
    p.merge_cells(f"A{r+1}:B{r+1}"); p.row_dimensions[r + 1].height = 30

    wb.active = 0
    nome = "Fotos-Comodidades-Zion-EXEMPLO.xlsx" if exemplo else "Fotos-Comodidades-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

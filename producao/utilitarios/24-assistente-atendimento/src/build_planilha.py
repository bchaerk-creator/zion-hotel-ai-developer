"""Gera a Ferramenta 24 · Assistente de IA para Atendimento (Zion Hospitality Business):
   - Assistente-Atendimento-Zion-EM-BRANCO.xlsx / Assistente-Atendimento-Zion-EXEMPLO.xlsx (dados fictícios)
Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dados import (CAMPOS, NOME, TIPO, CIDADE, CONTATO, TOM, IDIOMA, ASSINA, INFO, REGRAS_FIXAS, EMERG_A, TESTES, RESULTADOS,
                   EX, EX_RES, EX_OBS)
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
F0 = 6                                  # ficha: linhas 6..22
VERDE, VERM, AMAR = "C8E6C0", "F4C7C3", "FCE8B2"
F = lambda i: f"Ficha!$B${F0+i}"
vazio = lambda i: f"LEN(TRIM({F(i)}))=0"
P = lambda i: f'IF({vazio(i)},"[PREENCHA]",TRIM({F(i)}))'
O = lambda i, padrao: f'IF({vazio(i)},"{padrao}",TRIM({F(i)}))'

def cab(ws, l, tit):
    for j, t in enumerate(tit, 1):
        c = ws.cell(l, j, t); c.font = T(10, True, CREME); c.fill = CAB; c.alignment = WRAP; c.border = borda
    ws.row_dimensions[l].height = 32
def ent(c, v=None):
    c.value = v; c.fill = ENTRADA; c.border = borda; c.alignment = WRAP; c.font = T(10)
def calc(c, f, b=False):
    c.value = f; c.fill = CALC; c.border = borda; c.alignment = WRAP; c.font = T(10, b)

def linhas_instrucao():
    L = [f'="Você é o assistente de atendimento de "&{P(NOME)}&", "&{P(TIPO)}&" em "&{P(CIDADE)}&". Você responde mensagens de hóspedes e de pessoas interessadas em reservar."',
         f'="Responda em "&{O(IDIOMA, "português do Brasil")}&", com tom "&{O(TOM, "cordial e direto")}&". Assine como "&IF({vazio(ASSINA)},"a equipe de "&{P(NOME)},TRIM({F(ASSINA)}))&"."',
         None, "REGRAS QUE VOCÊ SEMPRE SEGUE"] + REGRAS_FIXAS + [f'="{EMERG_A}"&{P(CONTATO)}&"."', None, "INFORMAÇÕES DA HOSPEDAGEM (use só estas)"]
    for i in INFO:
        rot, lab, obrig = CAMPOS[i][0], CAMPOS[i][1], CAMPOS[i][2]
        L.append(f'="{lab}: "&{P(i)}' if obrig else f'=IF({vazio(i)},"","{lab}: "&TRIM({F(i)}))')
    L += [None, "Fim das informações. Para qualquer assunto que não esteja acima, use a regra 1."]
    return L

def montar(exemplo):
    wb = Workbook(); ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 104
    linhas = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 24", T(10, True, TERRA)),
        ("Assistente de IA para Atendimento", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para montar e testar as instruções de um assistente de IA que responde hóspedes só com as informações da sua hospedagem, sem inventar e sem prometer o que você não autorizou.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (hospedagem e anfitriã inventadas). Use a versão em branco." if exemplo
         else "Versão em branco. Preencha as células amarelas.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Para Airbnb, casas, apartamentos, pousadas e glampings.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 4 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Ficha: preencha o que o assistente pode dizer. Os campos marcados como obrigatórios precisam estar preenchidos. Nunca escreva senhas ou códigos de porta, cofre ou Wi-Fi.", None),
        ("2. Aba Instrução: quando a situação disser \"Pronta para copiar\", copie da linha 5 até a última e cole nas instruções do assistente que você usa (por exemplo, ChatGPT, Gemini, Claude ou o assistente da sua ferramenta de mensagens).", None),
        ("3. Aba Teste: faça as 12 perguntas ao assistente, uma por vez, e compare cada resposta com a coluna \"O que o assistente deve fazer\". Marque Passou ou Falhou.", None),
        ("4. Se algo falhou, ajuste a ficha (ou a instrução no assistente) e refaça os testes que falharam. Só use com hóspedes depois dos 12 aprovados, e continue lendo as respostas antes de enviar.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("COMO A PLANILHA DECIDE", T(12, True, MUSGO)),
        ("A instrução junta as 8 regras fixas com o que você escreveu na ficha. Campo opcional vazio fica de fora; aí o assistente deve dizer que vai confirmar com o anfitrião. Campo obrigatório vazio aparece como [PREENCHA].", None),
        ("A ficha avisa se encontrar \"senha:\" ou \"código:\" escrito em algum campo. O teste muda conforme a ficha: se um campo está vazio, a resposta certa é não inventar.", None),
        ("", None),
        ("CUIDADOS", T(12, True, MUSGO)),
        ("Assistentes de IA podem errar mesmo com boas instruções. Leia as respostas antes de enviar, principalmente sobre dinheiro, regras e segurança. Você continua responsável pelo que é enviado.", None),
        ("Não cole dados de hóspedes nem documentos no assistente. Confira as regras da plataforma de reservas sobre respostas automáticas antes de usar.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------- Ficha ----------
    fi = wb.create_sheet("Ficha"); fi.sheet_view.showGridLines = False
    for col, w in zip("ABCD", (32, 60, 13, 44)): fi.column_dimensions[col].width = w
    fi["A1"] = "Ficha da hospedagem"; fi["A1"].font = T(18, True, MUSGO)
    fi["A2"] = "EXEMPLO · dados fictícios" if exemplo else "Escreva só o que o assistente pode dizer a qualquer pessoa. Nada de senhas ou códigos."
    fi["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    fi["A3"] = "Situação"; fi["A3"].font = T(10, True)
    fi["A4"] = "Campos obrigatórios vazios"; fi["A4"].font = T(10, True)
    cab(fi, 5, ["Campo", "O que o assistente pode dizer", "Obrigatório?", "Dica"])
    rgB, rgC = f"B{F0}:B{F0+len(CAMPOS)-1}", f"C{F0}:C{F0+len(CAMPOS)-1}"
    for i, (rot, lab, obrig, dica) in enumerate(CAMPOS):
        r = F0 + i
        fi[f"A{r}"] = rot; fi[f"A{r}"].font = T(10, True); fi[f"A{r}"].border = borda; fi[f"A{r}"].alignment = WRAP
        ent(fi[f"B{r}"], EX[i] if exemplo else None)
        calc(fi[f"C{r}"], "Sim" if obrig else "")
        fi[f"D{r}"] = dica; fi[f"D{r}"].font = T(9, c="5F5F55", i=True); fi[f"D{r}"].alignment = WRAP
        fi.row_dimensions[r].height = 34
    calc(fi["B4"], f'=SUMPRODUCT(({rgC}="Sim")*(LEN(TRIM({rgB}))=0))', True)
    alerta = "+".join(f'SUMPRODUCT(ISNUMBER(SEARCH("{p}",{rgB}))*1)' for p in ("senha:", "código:", "codigo:"))
    calc(fi["E4"], "=" + alerta); fi.column_dimensions["E"].hidden = True
    calc(fi["B3"], '=IF(B4>0,"Faltam "&B4&" campo(s) obrigatório(s)",IF(E4>0,"Tire senhas e códigos da ficha","Pronta para copiar"))', True)
    for cond, cor in (('B3="Pronta para copiar"', VERDE), ('B3<>"Pronta para copiar"', AMAR)):
        fi.conditional_formatting.add("B3", FormulaRule(formula=[cond], fill=PatternFill("solid", fgColor=cor)))
    for i in range(len(CAMPOS)):
        r = F0 + i
        fi.conditional_formatting.add(f"B{r}", FormulaRule(formula=[f'AND(C{r}="Sim",LEN(TRIM(B{r}))=0)'], fill=PatternFill("solid", fgColor=VERM)))

    # ---------- Instrução ----------
    ins = wb.create_sheet("Instrução"); ins.sheet_view.showGridLines = False
    ins.column_dimensions["A"].width = 120
    ins["A1"] = "Instrução do assistente"; ins["A1"].font = T(18, True, MUSGO)
    ins["A2"] = "Copie da linha 5 até a última linha com texto e cole nas instruções do assistente. Linhas vazias podem ir junto."
    ins["A2"].font = T(10, True, TERRA)
    calc(ins["A3"], '="Situação da ficha: "&Ficha!B3', True)
    ins.conditional_formatting.add("A3", FormulaRule(formula=['Ficha!$B$3="Pronta para copiar"'], fill=PatternFill("solid", fgColor=VERDE)))
    ins.conditional_formatting.add("A3", FormulaRule(formula=['Ficha!$B$3<>"Pronta para copiar"'], fill=PatternFill("solid", fgColor=AMAR)))
    for k, l in enumerate(linhas_instrucao()):
        c = ins.cell(5 + k, 1)
        if l is None: continue
        if l.startswith("="): calc(c, l)
        else: c.value = l; c.font = T(10, l.isupper()); c.alignment = WRAP; c.fill = CALC; c.border = borda

    # ---------- Teste ----------
    te = wb.create_sheet("Teste"); te.sheet_view.showGridLines = False
    for col, w in zip("ABCDE", (5, 40, 58, 12, 30)): te.column_dimensions[col].width = w
    te["A1"] = "Teste do assistente"; te["A1"].font = T(18, True, MUSGO)
    te["A2"] = ("EXEMPLO · resultado do teste feito pela Zion com um assistente de IA sobre a instrução deste exemplo (dados fictícios)" if exemplo and EX_RES
                else "EXEMPLO · dados fictícios" if exemplo else "Faça cada pergunta ao assistente, numa conversa nova, e compare com a coluna C.")
    te["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    cab(te, 5, ["Nº", "Pergunta para o assistente", "O que o assistente deve fazer", "Resultado", "Observação"])
    for k, (perg, campo, fixo) in enumerate(TESTES):
        r = 6 + k
        te[f"A{r}"] = k + 1; te[f"A{r}"].border = borda
        te[f"B{r}"] = perg; te[f"B{r}"].font = T(10); te[f"B{r}"].alignment = WRAP; te[f"B{r}"].border = borda
        if campo is None: calc(te[f"C{r}"], fixo)
        else: calc(te[f"C{r}"], f'=IF({vazio(campo)},"Não inventa: diz que vai confirmar com o anfitrião","Responde com a ficha: "&LEFT(TRIM({F(campo)}),90)&IF(LEN(TRIM({F(campo)}))>90,"…",""))')
        ent(te[f"D{r}"], EX_RES[k] if exemplo and EX_RES else None); ent(te[f"E{r}"], EX_OBS[k] if exemplo and EX_OBS else None)
        te.row_dimensions[r].height = 36
    dv = DataValidation(type="list", formula1='"' + ",".join(RESULTADOS) + '"', allow_blank=True, showErrorMessage=True, errorTitle="Opção inválida", error="Escolha Passou ou Falhou.")
    te.add_data_validation(dv); dv.add("D6:D17")
    for cond, cor in (('D6="Passou"', VERDE), ('D6="Falhou"', VERM)):
        te.conditional_formatting.add("D6:D17", FormulaRule(formula=[cond], fill=PatternFill("solid", fgColor=cor)))
    for r, (rot, f) in zip(range(19, 23), [("Testes feitos", '=COUNTIF(D6:D17,"Passou")+COUNTIF(D6:D17,"Falhou")'), ("Passaram", '=COUNTIF(D6:D17,"Passou")'),
                                           ("Falharam", '=COUNTIF(D6:D17,"Falhou")'), ("O que fazer agora", None)]):
        te[f"B{r}"] = rot; te[f"B{r}"].font = T(10, True)
        if f: calc(te[f"C{r}"], f, True)
    n = len(TESTES)
    calc(te["C22"], f'=IF(Ficha!B3<>"Pronta para copiar","Complete a ficha antes de testar",IF(C19<{n},"Faça os "&({n}-C19)&" teste(s) que faltam",'
                    f'IF(C21>0,"Ajuste a ficha e refaça os "&C21&" teste(s) que falharam","Pronto: o assistente passou nos {n} testes")))', True)

    wb.active = 0
    nome = "Assistente-Atendimento-Zion-EXEMPLO.xlsx" if exemplo else "Assistente-Atendimento-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

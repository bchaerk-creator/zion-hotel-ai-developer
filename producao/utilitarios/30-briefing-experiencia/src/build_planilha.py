"""Gera a Ferramenta 30 · Gerador de Briefing de Experiência (Zion Hospitality Business):
   - Briefing-Experiencia-Zion-EM-BRANCO.xlsx / Briefing-Experiencia-Zion-EXEMPLO.xlsx (dados fictícios)
As mensagens são fórmulas montadas a partir de src/mensagens.py. Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib, re, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mensagens import CAMPOS, MENSAGENS, DATAS, rotulo
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
MUSGO, PRETO, CREME, TERRA = "1B2117", "040605", "FEF5F0", "8B714E"
ENTRADA, CALC, CAB = PatternFill("solid", fgColor="FFF4C7"), PatternFill("solid", fgColor="E3EEDF"), PatternFill("solid", fgColor=MUSGO)
fino = Side(style="thin", color="C9B8A0"); borda = Border(left=fino, right=fino, top=fino, bottom=fino)
T = lambda sz=11, b=False, c=PRETO, i=False: Font(name="Arial", size=sz, bold=b, color=c, italic=i)
WRAP = Alignment(wrap_text=True, vertical="top")
CAMPO_RE = re.compile(r"\{(\w+)\}")

# posições na Ficha
REF, linha = {}, 5
for k, *_ in [c for c in CAMPOS if c[2] == "H"]: REF[k] = f"Ficha!$B${linha}"; linha += 1
L_RES = linha + 1; linha = L_RES + 1
for k, *_ in [c for c in CAMPOS if c[2] == "R"]: REF[k] = f"Ficha!$B${linha}"; linha += 1
L_DATAS = linha + 1

def lit(s):  # literal em pedaços de até 200 caracteres (limite de 255 do Excel)
    s = s.replace('"', '""'); return "&".join(f'"{s[i:i+200]}"' for i in range(0, len(s), 200)) or '""'
def data_txt(e): return f'RIGHT("0"&DAY({e}),2)&"/"&RIGHT("0"&MONTH({e}),2)&"/"&YEAR({e})'
def val(k, preencha=True):
    v = data_txt(REF[k]) if k in DATAS else REF[k]
    return f'IF({REF[k]}="","[PREENCHA: {rotulo(k)}]",{v})' if preencha else v
def peca(texto, preencha=True):
    out, pos = [], 0
    for m in CAMPO_RE.finditer(texto):
        if m.start() > pos: out.append(lit(texto[pos:m.start()]))
        out.append(val(m.group(1), preencha)); pos = m.end()
    if pos < len(texto): out.append(lit(texto[pos:]))
    return "&".join(out)
def formula_msg(segs):
    partes = []
    for s in segs:
        if s[0] == "t": partes.append(peca(s[1]))
        elif s[0] == "o":
            ks = CAMPO_RE.findall(s[1]); cond = ",".join(f'{REF[k]}=""' for k in ks)
            partes.append(f'IF(OR({cond}),"",{peca(s[1], False)})')
        elif s[0] == "v": partes.append(f'IF({REF[s[1]]}="",{lit(s[2])},"")')
    return "=" + "&".join(partes)
def formula_falta(segs):
    ks = []
    for s in segs:
        if s[0] == "t":
            for k in CAMPO_RE.findall(s[1]):
                if k not in ks: ks.append(k)
    return "&".join(f'IF({REF[k]}="","{rotulo(k)}; ","")' for k in ks)
def formula_data(regra):
    d = REF["data"]
    if regra == "logo": return '="Quando precisar"'
    if regra == "resposta": return '="Quando acontecer"'
    off = {"data-2": -2, "data-1": -1, "data": 0}[regra]
    expr = f"{d}-{abs(off)}" if off else d
    return f'=IF({d}="","[PREENCHA: Data da saída]",{data_txt(expr)})'

def montar(exemplo):
    wb = Workbook(); ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 104
    linhas = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 30", T(10, True, TERRA)),
        ("Gerador de Briefing de Experiência", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para escrever o briefing da sua experiência uma vez e gerar, para cada saída, a descrição, as mensagens ao cliente e o briefing de quem conduz, sem esquecer nada.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (experiência, pessoas, telefone e preço inventados). Use a versão em branco." if exemplo
         else "Versão em branco. Preencha as células amarelas da aba Ficha.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("", None),
        ("COMO USAR EM 4 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Ficha, parte de cima: preencha uma vez o briefing da experiência (cerca de 15 minutos). Campos com * são obrigatórios.", None),
        ("2. Aba Ficha, parte de baixo: a cada saída, preencha nome do cliente, data, horário e participantes.", None),
        ("3. Aba Mensagens: os 8 textos aparecem prontos, com a data de envio de cada um. A coluna Situação diz se falta algum dado.", None),
        ("4. Para copiar: clique na célula do Texto pronto, copie o conteúdo pela barra de fórmulas (ou dê dois cliques na célula e selecione o texto) e cole no WhatsApp ou na plataforma. Releia antes de enviar.", None),
        ("", None),
        ("REGRA DE OURO: A PLANILHA NÃO INVENTA", T(12, True, MUSGO)),
        ("Se um dado obrigatório estiver vazio, a mensagem mostra [PREENCHA: nome do campo] no lugar. Nunca envie uma mensagem com [PREENCHA]. Campos opcionais vazios simplesmente somem da frase.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("CUIDADOS", T(12, True, MUSGO)),
        ("Capacidade, segurança, licenças e seguros dependem de cada atividade e do profissional responsável: confira antes de vender. Na saída abaixo do mínimo, ofereça sempre remarcar ou devolver o valor.", None),
        ("Peça a opinião do cliente sem oferecer nada em troca. Confira as regras da plataforma onde vende a experiência.", None),
        ("Sem promessa: o gerador organiza a comunicação; não garante vendas, reservas nem avaliações.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    f = wb.create_sheet("Ficha"); f.sheet_view.showGridLines = False
    for col, w in zip("ABC", (36, 56, 52)): f.column_dimensions[col].width = w
    f["A1"] = "Ficha da experiência e da saída"; f["A1"].font = T(18, True, MUSGO)
    f["A2"] = "EXEMPLO · dados fictícios" if exemplo else "* = obrigatório. Os opcionais vazios saem das mensagens."
    f["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    def faixa(l, txt):
        f.merge_cells(start_row=l, start_column=1, end_row=l, end_column=3)
        c = f.cell(l, 1, txt); c.font = T(11, True, CREME); c.fill = CAB
    faixa(4, "A EXPERIÊNCIA · preencha uma vez"); faixa(L_RES, "ESTA SAÍDA · preencha a cada data")
    for k, rot, sec, ob, ajuda, ex in CAMPOS:
        l = int(REF[k].split("$")[-1])
        f.cell(l, 1, rot + (" *" if ob else "")).font = T(10, ob)
        c = f.cell(l, 2); c.fill = ENTRADA; c.border = borda; c.alignment = WRAP; c.font = T(10)
        if k in DATAS:
            c.number_format = "DD/MM/YYYY"
            dv = DataValidation(type="date", operator="greaterThan", formula1="36526", allow_blank=True, showErrorMessage=True,
                                errorTitle="Data inválida", error="Digite uma data, por exemplo 12/12/2026."); f.add_data_validation(dv); dv.add(c.coordinate)
        if exemplo and ex: c.value = datetime.date.fromisoformat(ex) if k in DATAS else ex
        h = f.cell(l, 3, ajuda); h.font = T(9, c="5F5F55", i=True); h.alignment = WRAP
    d, mn, ps = REF["data"], REF["minimo"], REF["pessoas"]
    f.cell(L_DATAS, 1, "Situação da saída").font = T(10, True)
    c = f.cell(L_DATAS, 2, f'=IF({d}="","Preencha a data da saída",IF(OR({mn}="",{ps}=""),"Preencha mínimo e participantes",'
                           f'IF(ISERROR(VALUE({ps})+VALUE({mn})),"Mínimo e participantes precisam ser números",IF(VALUE({ps})>=VALUE({mn}),"Mínimo atingido: use a B03 (saída confirmada)","Abaixo do mínimo: use a B04 (remarcar ou devolver)"))))')
    c.fill = CALC; c.border = borda; c.font = T(10, True)
    f.freeze_panes = "A4"

    m = wb.create_sheet("Mensagens"); m.sheet_view.showGridLines = False
    for col, w in zip("ABCDEF", (6, 24, 22, 15, 80, 26)): m.column_dimensions[col].width = w
    m["A1"] = "Mensagens prontas"; m["A1"].font = T(18, True, MUSGO)
    m["A2"] = "Releia antes de enviar. Nunca envie uma mensagem com [PREENCHA]."; m["A2"].font = T(10, c="5F5F55", i=True)
    m["B3"] = "Prontas para copiar"; m["B3"].font = T(10, True)
    n = len(MENSAGENS); r0 = 6
    m["C3"] = f'=COUNTIF(F{r0}:F{r0+n-1},"Pronta para copiar")&" de {n}"'; m["C3"].fill = CALC; m["C3"].font = T(11, True)
    m["D3"] = "Saída"; m["D3"].font = T(10, True)
    m["E3"] = f"=Ficha!B{L_DATAS}"; m["E3"].fill = CALC; m["E3"].font = T(10, True)
    for j, t in enumerate(["Nº", "Mensagem", "Quando enviar", "Data de envio", "Texto pronto", "Situação"], 1):
        c = m.cell(5, j, t); c.font = T(10, True, CREME); c.fill = CAB; c.alignment = WRAP
    for i, (mid, tit, quando, regra, segs) in enumerate(MENSAGENS):
        r = r0 + i
        for j, v in enumerate([mid, tit, quando], 1):
            c = m.cell(r, j, v); c.alignment = WRAP; c.font = T(10, j == 2); c.border = borda
        for col, fo in (("D", formula_data(regra)), ("E", formula_msg(segs))):
            c = m[f"{col}{r}"]; c.value = fo; c.fill = CALC; c.border = borda; c.alignment = WRAP; c.font = T(10)
        fal = formula_falta(segs)
        c = m[f"F{r}"]; c.value = f'=IF(({fal})="","Pronta para copiar","Falta: "&LEFT({fal},LEN({fal})-2))'
        c.fill = CALC; c.border = borda; c.alignment = WRAP; c.font = T(10, True)
        m.row_dimensions[r].height = 150
    rg = f"F{r0}:F{r0+n-1}"
    m.conditional_formatting.add(rg, FormulaRule(formula=[f'F{r0}="Pronta para copiar"'], fill=PatternFill("solid", fgColor="C8E6C0")))
    m.conditional_formatting.add(rg, FormulaRule(formula=[f'LEFT(F{r0},5)="Falta"'], fill=PatternFill("solid", fgColor="F4C7C3")))
    m.freeze_panes = "C6"

    md = wb.create_sheet("Modelos"); md.sheet_view.showGridLines = False
    md.column_dimensions["A"].width = 30; md.column_dimensions["B"].width = 100
    md["A1"] = "Modelos para copiar à mão"; md["A1"].font = T(18, True, MUSGO)
    md["A2"] = "Troque o que está entre colchetes. Trechos marcados (se houver ...) só entram se você tiver a informação."; md["A2"].font = T(10, c="5F5F55", i=True)
    for i, (mid, tit, quando, regra, segs) in enumerate(MENSAGENS):
        r = 4 + i; txt = ""
        for sg in segs:
            if sg[0] == "t": txt += CAMPO_RE.sub(lambda x: f"[{rotulo(x.group(1))}]", sg[1])
            elif sg[0] == "o": txt += " (se houver:" + CAMPO_RE.sub(lambda x: f"[{rotulo(x.group(1))}]", sg[1]) + ")"
            elif sg[0] == "v": txt += " (se o grupo não informou restrições:" + sg[2] + ")"
        a = md.cell(r, 1, f"{mid} · {tit}\n{quando}"); a.font = T(10, True); a.alignment = WRAP
        b = md.cell(r, 2, txt); b.font = T(10); b.alignment = WRAP; md.row_dimensions[r].height = 120

    wb.active = 0
    nome = "Briefing-Experiencia-Zion-EXEMPLO.xlsx" if exemplo else "Briefing-Experiencia-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

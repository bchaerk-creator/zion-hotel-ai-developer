"""Gera a Ferramenta 23 · Kit de Roteiros de Conteúdo e Vídeos (Zion Hospitality Business):
   - Roteiros-Conteudo-Zion-EM-BRANCO.xlsx / Roteiros-Conteudo-Zion-EXEMPLO.xlsx (dados fictícios)
Os roteiros são fórmulas montadas a partir de src/roteiros.py. Uso: python3 -I build_planilha.py <saida>"""
import sys, pathlib, re, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from roteiros import CAMPOS, MENSAGENS, DATAS, rotulo
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
for k, *_ in [c for c in CAMPOS if c[2] == "C"]: REF[k] = f"Ficha!$B${linha}"; linha += 1
L_DATAS = linha + 1

def lit1(s):  # literal em pedaços de até 200 caracteres (limite de 255 do Excel)
    s = s.replace('"', '""'); return "&".join(f'"{s[i:i+200]}"' for i in range(0, len(s), 200)) or '""'
def lit(s):  # quebra de linha vira CHAR(10)
    return "&CHAR(10)&".join(lit1(p) if p else '""' for p in s.split("\n"))
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
    d, iv = REF["inicio"], REF["intervalo"]; n = int(regra.split("-")[1]) - 1
    expr = f"{d}+{n}*{iv}" if n else d
    return f'=IF({d}="","[PREENCHA: Data do primeiro vídeo]",IF(OR(NOT(ISNUMBER({iv})),N({iv})<1),"[CONFIRA: Dias entre os vídeos]",{data_txt(expr)}))'

def montar(exemplo):
    wb = Workbook(); ws = wb.active; ws.title = "Comece aqui"; ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 104
    linhas = [
        ("ZION HOSPITALITY BUSINESS · FERRAMENTA 23", T(10, True, TERRA)),
        ("Kit de Roteiros de Conteúdo e Vídeos", T(22, True, MUSGO)),
        ("Aprenda o passo a passo para preencher uma ficha da sua hospedagem e receber 8 roteiros curtos de vídeo, com gancho, cenas, texto na tela, legenda e o dia de postar cada um.", T(11, c="2D352A")),
        ("EXEMPLO PREENCHIDO COM DADOS FICTÍCIOS (hospedagem e lugar inventados). Use a versão em branco." if exemplo
         else "Versão em branco. Preencha as células amarelas da aba Ficha.", T(11, True, "A0522D" if exemplo else MUSGO)),
        ("Para Airbnb, casas, apartamentos, pousadas e glampings.", T(10, True, TERRA)),
        ("", None),
        ("COMO USAR EM 4 PASSOS", T(12, True, MUSGO)),
        ("1. Aba Ficha, parte de cima: preencha uma vez as informações da hospedagem (cerca de 15 minutos). Campos com * são obrigatórios.", None),
        ("2. Aba Ficha, parte de baixo: escolha a data do primeiro vídeo e de quantos em quantos dias vai postar.", None),
        ("3. Aba Roteiros: os 8 roteiros aparecem prontos, com a data de postar. A coluna Situação diz se falta algum dado.", None),
        ("4. Grave com o celular seguindo as cenas, use o texto na tela e cole a legenda. Releia antes de postar.", None),
        ("", None),
        ("REGRA DE OURO: A PLANILHA NÃO INVENTA", T(12, True, MUSGO)),
        ("Se um dado obrigatório estiver vazio, o roteiro mostra [PREENCHA: nome do campo] no lugar. Nunca publique com [PREENCHA]. Campos opcionais vazios saem do roteiro ou trocam a cena por outra.", None),
        ("", None),
        ("CORES", T(12, True, MUSGO)),
        ("Amarelo = você preenche.   Verde = calculado pela planilha (não digite por cima).", None),
        ("", None),
        ("CUIDADOS", T(12, True, MUSGO)),
        ("Use imagens reais da sua hospedagem. Não mostre hóspedes nem pessoas sem autorização por escrito. Músicas: use as que a própria rede social libera.", None),
        ("Mostre só o que existe: o que aparece no vídeo é o que o hóspede vai esperar encontrar.", None),
        ("Sem promessa: os roteiros organizam o conteúdo; não garantem seguidores, alcance nem reservas.", None),
        ("", None),
        ("Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.", T(10, c="5F5F55", i=True)),
        ("Zion Hospitality Business · Bruno Chaerk · Material educativo.", T(9, c="5F5F55", i=True)),
    ]
    for i, (t, f) in enumerate(linhas, 1):
        c = ws.cell(i, 1, t); c.font = f or T(11, c="2D352A"); c.alignment = Alignment(wrap_text=True, vertical="top")

    f = wb.create_sheet("Ficha"); f.sheet_view.showGridLines = False
    for col, w in zip("ABC", (36, 56, 52)): f.column_dimensions[col].width = w
    f["A1"] = "Ficha da hospedagem e do calendário"; f["A1"].font = T(18, True, MUSGO)
    f["A2"] = "EXEMPLO · dados fictícios" if exemplo else "* = obrigatório. Os opcionais vazios saem dos roteiros."
    f["A2"].font = T(10, True, "A0522D" if exemplo else TERRA)
    def faixa(l, txt):
        f.merge_cells(start_row=l, start_column=1, end_row=l, end_column=3)
        c = f.cell(l, 1, txt); c.font = T(11, True, CREME); c.fill = CAB
    faixa(4, "A HOSPEDAGEM · preencha uma vez"); faixa(L_RES, "CALENDÁRIO DE POSTAGEM")
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
    d, iv = REF["inicio"], REF["intervalo"]
    f.cell(L_DATAS, 1, "Situação do calendário").font = T(10, True)
    c = f.cell(L_DATAS, 2, f'=IF({d}="","Preencha a data do primeiro vídeo",IF(OR(NOT(ISNUMBER({iv})),N({iv})<1),"Dias entre os vídeos precisa ser um número de 1 ou mais",'
                           f'"Do primeiro ao último vídeo: "&{data_txt(d)}&" a "&{data_txt(f"{d}+{len(MENSAGENS)-1}*{iv}")}))')
    c.fill = CALC; c.border = borda; c.font = T(10, True)
    f.freeze_panes = "A4"

    m = wb.create_sheet("Roteiros"); m.sheet_view.showGridLines = False
    for col, w in zip("ABCDEF", (6, 22, 24, 15, 84, 26)): m.column_dimensions[col].width = w
    m["A1"] = "Roteiros prontos"; m["A1"].font = T(18, True, MUSGO)
    m["A2"] = "Releia antes de postar. Nunca publique um roteiro com [PREENCHA]."; m["A2"].font = T(10, c="5F5F55", i=True)
    m["B3"] = "Prontos para gravar"; m["B3"].font = T(10, True)
    n = len(MENSAGENS); r0 = 6
    m["C3"] = f'=COUNTIF(F{r0}:F{r0+n-1},"Pronto para gravar")&" de {n}"'; m["C3"].fill = CALC; m["C3"].font = T(11, True)
    m["D3"] = "Calendário"; m["D3"].font = T(10, True)
    m["E3"] = f"=Ficha!B{L_DATAS}"; m["E3"].fill = CALC; m["E3"].font = T(10, True)
    for j, t in enumerate(["Nº", "Formato", "Objetivo", "Data de postar", "Roteiro pronto", "Situação"], 1):
        c = m.cell(5, j, t); c.font = T(10, True, CREME); c.fill = CAB; c.alignment = WRAP
    for i, (mid, tit, quando, regra, segs) in enumerate(MENSAGENS):
        r = r0 + i
        for j, v in enumerate([mid, tit, quando], 1):
            c = m.cell(r, j, v); c.alignment = WRAP; c.font = T(10, j == 2); c.border = borda
        for col, fo in (("D", formula_data(regra)), ("E", formula_msg(segs))):
            c = m[f"{col}{r}"]; c.value = fo; c.fill = CALC; c.border = borda; c.alignment = WRAP; c.font = T(10)
        fal = formula_falta(segs)
        c = m[f"F{r}"]; c.value = f'=IF(({fal})="","Pronto para gravar","Falta: "&LEFT({fal},LEN({fal})-2))'
        c.fill = CALC; c.border = borda; c.alignment = WRAP; c.font = T(10, True)
        m.row_dimensions[r].height = 230
    rg = f"F{r0}:F{r0+n-1}"
    m.conditional_formatting.add(rg, FormulaRule(formula=[f'F{r0}="Pronto para gravar"'], fill=PatternFill("solid", fgColor="C8E6C0")))
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
            elif sg[0] == "v": txt += " (se não houver passeios por perto: " + sg[1 + 1] + ")"
        a = md.cell(r, 1, f"{mid} · {tit}\n{quando}"); a.font = T(10, True); a.alignment = WRAP
        b = md.cell(r, 2, txt); b.font = T(10); b.alignment = WRAP; md.row_dimensions[r].height = 190

    wb.active = 0
    nome = "Roteiros-Conteudo-Zion-EXEMPLO.xlsx" if exemplo else "Roteiros-Conteudo-Zion-EM-BRANCO.xlsx"
    wb.save(OUT / nome); print("gerado", OUT / nome)

if __name__ == "__main__":
    montar(False); montar(True)

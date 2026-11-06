"""Modelos editáveis do Kit do Investidor (Pilar 7): Pitch deck (pptx) e Teaser + One-pager (docx).
Uso: python3 -I build_modelos.py <pasta de saída>"""
import sys, pathlib
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from docx import Document
from docx.shared import Pt as DPt, RGBColor as DRGB, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); OUT.mkdir(parents=True, exist_ok=True)
VERDE, CREME, DOURADO, CINZA = RGBColor(0x16, 0x26, 0x1C), RGBColor(0xF5, 0xF1, 0xE8), RGBColor(0xC9, 0xA8, 0x4C), RGBColor(0x46, 0x56, 0x4B)
RODAPE = "Modelo do Club Zion Collection · Material educativo. Cenários dependem das premissas do projeto; não são promessa de retorno."

SLIDES = [
 ("[NOME DO PROJETO]", "[Cidade/UF] · [uma frase de posicionamento]\n[Seu nome · contato]", "Capa. Diga em uma frase o que é e para quem. Nome, lugar, você.", None),
 ("A oportunidade", "• O destino: [o que já existe, visitação, acesso]\n• A lacuna: [o que falta e o produto ocupa]\n• Por que agora: [sinal do mercado]", "Por que aqui e por que agora. Fonte: Dossiê, páginas 1 e 2.", None),
 ("O mercado", "• Visitação: [n/ano, fonte]\n• Comparáveis: [3 hospedagens, diária e ocupação]\n• Diária e ocupação da região: [faixas, fonte]\n• Público que paga: [quem, de onde]", "Tem demanda? Quanto pagam? Fonte: Ficha do Mercado, Pilar 2.", "[DIÁRIA MÉDIA DA REGIÃO]"),
 ("O hóspede e a promessa", "• Quem: [público, idade, origem, com quem viaja]\n• Quando: [momento de uso, sazonalidade]\n• A promessa da estadia: [uma frase]", "Para quem é e o que ele leva. Fonte: Dossiê, página 3.", None),
 ("O produto", "• [Tipologia 1]: [n] unidades · [m²] · diária alvo R$ [ ]\n• [Tipologia 2]: [n] unidades · [m²] · diária alvo R$ [ ]\n• [Tipologia 3]: [n] unidades · [m²] · diária alvo R$ [ ]\n• Áreas comuns e serviços: [lista]\n(imagens de referência, identificadas como referência)", "Como é a experiência. Fonte: Dossiê, página 3; Plano conceitual.", "[N] UNIDADES"),
 ("O terreno e o masterplan em fases", "• Terreno: [área] · [situação documental] · [acesso e infraestrutura]\n• O que a lei permite: [taxa de ocupação, zoneamento]\n• Fase 1: [o que constrói] · R$ [ ]\n• Fase 2: [ ] · R$ [ ]\n• Fase 3: [ ] · R$ [ ]", "Onde fica cada coisa e como cresce. Fonte: Dossiê, páginas 1 e 5; Planilha 2 · Massas.", None),
 ("O investimento", "CAPEX da fase 1 (Planilha 1 · Resumo)\n• Projetos, licenças e infraestrutura: R$ [ ] ([ ]%)\n• Construção das unidades: R$ [ ] ([ ]%)\n• FF&E, mobília e equipamentos: R$ [ ] ([ ]%)\n• OS&E, enxoval e operação: R$ [ ] ([ ]%)\n• Contingência: R$ [ ] ([ ]%)\n• Custo por unidade pronta: R$ [ ] · por m²: R$ [ ]", "Quanto custa e onde vai o dinheiro.", "R$ [CAPEX]"),
 ("O modelo e os números", "Cenários (Planilha 2 · Modelo de renda)\n                 Conservador   Base   Otimista\nDiária média       R$ [ ]     R$ [ ]   R$ [ ]\nOcupação             [ ]%      [ ]%     [ ]%\nRevPAR             R$ [ ]     R$ [ ]   R$ [ ]\nReceita bruta/ano  R$ [ ]     R$ [ ]   R$ [ ]\nNOI/ano            R$ [ ]     R$ [ ]   R$ [ ]\nMargem               [ ]%      [ ]%     [ ]%", "Quanto entra e quanto sobra. Mostre sempre o conservador.", None),
 ("O retorno", "• Ocupação de equilíbrio: [ ]% (região opera a [ ]%)\n• Payback: [ ] / [ ] / [ ] anos\n• TIR 10 anos: [ ]% / [ ]% / [ ]%\n• VPL 10 anos (base, taxa [ ]%): R$ [ ]\n• Valor do negócio em operação (cap rate [ ]%): R$ [ ]", "Quanto volta e em quanto tempo. Fonte: Planilha 2, linhas 44 a 47 e 62 a 64.", "[PAYBACK BASE] ANOS"),
 ("Riscos e mitigantes", "• Licenciamento: [risco] → [mitigante]\n• Obra e custo: [ ] → [ ]\n• Demanda e sazonalidade: [ ] → [ ]\n• Operação: [ ] → [ ]\n• Capital: [ ] → [ ]", "O que pode dar errado e o que cobre. Fonte: Dossiê, páginas 6 e 7.", None),
 ("Quem faz", "• [Você]: [papel, experiência, o que aporta]\n• [Sócio/parceiro]: [papel]\n• [Projetos e obra]: [quem]\n• Acompanhamento: equipe Zion (metodologia e avaliação do projeto)", "Por que vocês. Fonte: Dossiê, página 7.", None),
 ("O pedido e os próximos passos", "• O pedido: R$ [ ] para [uso], em troca de [contrapartida proposta, a combinar]\n• O que o proprietário aporta: [terreno, capital, trabalho]\n• Próximos passos: 1) [ ] até [data] · 2) [ ] · 3) [ ]\n• Material completo: masterplan de viabilidade, plano conceitual e planilhas disponíveis", "O que você quer de mim e o que acontece depois. Fonte: Dossiê, página 7.", None),
]

def pptx():
    prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    for i, (tit, corpo, nota, destaque) in enumerate(SLIDES, 1):
        s = prs.slides.add_slide(blank)
        bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height); bg.fill.solid(); bg.fill.fore_color.rgb = VERDE if i in (1, 12) else CREME; bg.line.fill.background()
        barra = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, prs.slide_height - Inches(0.12), prs.slide_width, Inches(0.12)); barra.fill.solid(); barra.fill.fore_color.rgb = DOURADO; barra.line.fill.background()
        cor_t = CREME if i in (1, 12) else VERDE
        tb = s.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(8.5), Inches(1.2)); tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = tit; p.font.size = Pt(34 if i != 1 else 44); p.font.bold = True; p.font.color.rgb = cor_t; p.font.name = "Georgia"
        cb = s.shapes.add_textbox(Inches(0.7), Inches(1.8), Inches(8.3 if destaque else 11.9), Inches(5)); tf = cb.text_frame; tf.word_wrap = True
        for j, linha in enumerate(corpo.split("\n")):
            q = tf.paragraphs[0] if j == 0 else tf.add_paragraph(); q.text = linha; q.font.size = Pt(16); q.font.color.rgb = cor_t; q.font.name = "Consolas" if i == 8 else "Calibri"; q.space_after = Pt(6)
        if destaque:
            dx = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.3), Inches(2.2), Inches(3.4), Inches(2.2)); dx.fill.solid(); dx.fill.fore_color.rgb = VERDE; dx.line.fill.background()
            t = dx.text_frame; t.word_wrap = True; t.paragraphs[0].text = destaque; t.paragraphs[0].font.size = Pt(26); t.paragraphs[0].font.bold = True; t.paragraphs[0].font.color.rgb = DOURADO; t.paragraphs[0].alignment = 2
            r = t.add_paragraph(); r.text = "cenário base"; r.font.size = Pt(12); r.font.color.rgb = CREME; r.alignment = 2
        rb = s.shapes.add_textbox(Inches(0.7), Inches(6.85), Inches(11.9), Inches(0.4)); rp = rb.text_frame.paragraphs[0]; rp.text = f"{i}/12 · {RODAPE}"; rp.font.size = Pt(9); rp.font.color.rgb = DOURADO if i in (1, 12) else CINZA
        s.notes_slide.notes_text_frame.text = f"Pergunta que este slide responde: {nota}\n\nFale 60 a 90 segundos. Substitua tudo que está entre colchetes pelos números da sua Ficha (Kit do Investidor)."
    prs.save(OUT / "Pitch-Deck-Zion-MODELO.pptx")

def docx():
    d = Document()
    for sec in d.sections: sec.top_margin = sec.bottom_margin = Cm(1.5); sec.left_margin = sec.right_margin = Cm(1.8)
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = DPt(10)
    def h(t, sz=20, cor=(0x16, 0x26, 0x1C)):
        p = d.add_paragraph(); r = p.add_run(t); r.bold = True; r.font.size = DPt(sz); r.font.name = "Georgia"; r.font.color.rgb = DRGB(*cor); return p
    def sub(t):
        p = d.add_paragraph(); r = p.add_run(t.upper()); r.bold = True; r.font.size = DPt(8.5); r.font.color.rgb = DRGB(0x7A, 0x5E, 0x12); p.paragraph_format.space_before = DPt(8); p.paragraph_format.space_after = DPt(2)
    def tx(t, it=False, sz=10):
        p = d.add_paragraph(); r = p.add_run(t); r.italic = it; r.font.size = DPt(sz); p.paragraph_format.space_after = DPt(4); return p
    # TEASER
    h("TEASER · 1 página", 11, (0x7A, 0x5E, 0x12)); h("[Título com a oportunidade, não com o nome do projeto]")
    sub("O lugar"); tx("[Região, distância do público, o que o destino já tem. Sem endereço, sem matrícula.]")
    sub("O produto"); tx("[Tipologias, nº de unidades da fase 1, a promessa da estadia em uma frase.]")
    sub("Quatro números · cenário base (Planilha 2)")
    t = d.add_table(rows=2, cols=4); t.style = "Light Grid Accent 3"
    for j, (a, b) in enumerate([("Investimento fase 1", "R$ [ ]"), ("Diária média", "R$ [ ]"), ("Ocupação de equilíbrio", "[ ]%"), ("Payback", "[ ] anos")]):
        t.cell(0, j).text = a; t.cell(1, j).text = b
    sub("O que já existe"); tx("[Terreno próprio ou acordo · documentação · consulta prévia · plano conceitual · estudo de viabilidade feito com método]")
    sub("O pedido"); tx("[R$ [ ] para a fase 1, em troca de participação a combinar.]")
    sub("Próximo passo"); tx("Material completo e visita sob acordo de confidencialidade. [Seu nome · WhatsApp · e-mail]")
    tx(RODAPE, True, 8)
    d.add_page_break()
    # ONE-PAGER
    h("ONE-PAGER · resumo executivo", 11, (0x7A, 0x5E, 0x12)); h("[Nome do projeto] · [Cidade/UF]"); tx("[Uma frase de posicionamento] · [Seu nome · contato]", True)
    sub("1 · A oportunidade"); tx("[O destino, a demanda e a lacuna, em 3 linhas, com fontes.]")
    sub("2 · O produto"); tx("[Tipologias e unidades por fase · promessa · público · diária alvo por tipologia]")
    sub("3 · O terreno"); tx("[Área · situação documental · acesso · infraestrutura · o que a lei permite]")
    sub("4 · Masterplan em fases"); tx("Fase 1: [ ] · R$ [ ]   |   Fase 2: [ ] · R$ [ ]   |   Fase 3: [ ] · R$ [ ]")
    sub("5 · Os números (Planilha 2 · Modelo de renda)")
    linhas = ["Diária média", "Ocupação (região: [ ]%)", "Receita bruta anual", "Resultado operacional (NOI)", "Margem operacional", "Payback (anos)", "TIR 10 anos"]
    t = d.add_table(rows=len(linhas) + 1, cols=4); t.style = "Light Grid Accent 3"
    for j, c in enumerate(["", "Conservador", "Base", "Otimista"]): t.cell(0, j).text = c
    for i, l in enumerate(linhas, 1):
        t.cell(i, 0).text = l
        for j in (1, 2, 3): t.cell(i, j).text = "[ ]"
    tx("Investimento total (com capital de giro): R$ [ ] · Custo por m² construído: R$ [ ] · Custo por unidade pronta: R$ [ ]")
    sub("6 · Modelo e pedido"); tx("[Renda, venda ou misto.] Pedido: R$ [ ] para [uso], em troca de [contrapartida proposta]. O proprietário aporta: [terreno, capital, trabalho].")
    sub("7 · Riscos e mitigantes"); tx("[Risco 1] → [mitigante]   |   [Risco 2] → [mitigante]   |   [Risco 3] → [mitigante]")
    tx("Estudo elaborado com a metodologia Zion Hospitality Business; premissas disponíveis para auditoria. " + RODAPE, True, 8)
    d.save(OUT / "Teaser-e-One-Pager-Zion-MODELO.docx")

pptx(); docx(); print("ok", sorted(p.name for p in OUT.iterdir()))

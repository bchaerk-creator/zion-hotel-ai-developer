#!/usr/bin/env python3
# ZION ECOSYSTEM — CIDADE CIRCULAR · Volume Especial (~80 págs)
# Padrão Zion Ebook Series adaptado: sem acervo de fotos neste ambiente,
# páginas de foto substituídas por interlúdios editoriais escuros.
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Table, TableStyle)
from reportlab.pdfgen import canvas

GOLD   = colors.HexColor('#C9A84C')
BLACK  = colors.HexColor('#0A0A0A')
DARK   = colors.HexColor('#1A1A1A')
CREAM  = colors.HexColor('#F5F0E8')
GRAY   = colors.HexColor('#4A4A4A')
LGRAY  = colors.HexColor('#999999')
BGDARK = colors.HexColor('#0F0F0F')
BGLIGHT= colors.HexColor('#F8F5EF')

W, H = A4
AV = W - 40*mm  # 481.89 pt — IMUTÁVEL
OUT = '/tmp/claude-0/-home-user-zion-hotel-ai-developer/5e61dba4-bdba-5d11-a3b8-8d9de78b22f5/scratchpad/Zion_Ecosystem_Cidade_Circular.pdf'

TITULO_FOOTER = 'Cidade Circular — Como Transformar o Lixo do Seu Município em Patrimônio Público'

class ZionCanvas(canvas.Canvas):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self._saved = []
    def showPage(self):
        self._saved.append(dict(self.__dict__)); self._startPage()
    def save(self):
        for st in self._saved:
            self.__dict__.update(st); self._chrome(); canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    def _chrome(self):
        pg = self._pageNumber
        if pg in (1, 2): return
        self.saveState()
        self.setStrokeColor(GOLD); self.setLineWidth(0.6)
        self.line(18*mm, H-15*mm, W-18*mm, H-15*mm)
        self.setFillColor(GOLD); self.setFont('Helvetica-Bold', 7)
        self.drawString(18*mm, H-13*mm, 'ZION ECOSYSTEM  ·  ZION HOTEL GROUP INTERNATIONAL × ECOGRUPO')
        self.setFont('Helvetica', 7); self.setFillColor(LGRAY)
        self.drawRightString(W-18*mm, H-13*mm, 'SÉRIE ESPECIAL  ·  CIDADE CIRCULAR')
        self.line(18*mm, 13*mm, W-18*mm, 13*mm)
        self.setFillColor(LGRAY); self.setFont('Helvetica', 7)
        self.drawString(18*mm, 8*mm, TITULO_FOOTER)
        self.setFillColor(GOLD); self.setFont('Helvetica-Bold', 8)
        self.drawRightString(W-18*mm, 8*mm, str(pg))
        self.restoreState()

def S(n, **kw):
    b = dict(fontName='Helvetica', fontSize=10, textColor=GRAY, leading=16, spaceAfter=8)
    b.update(kw); return ParagraphStyle(n, **b)

ST = {
 'label':  S('lb', fontName='Helvetica-Bold', fontSize=7.5, textColor=GOLD, spaceAfter=3),
 'h1':     S('h1', fontName='Helvetica-Bold', fontSize=22, textColor=DARK, spaceBefore=12, spaceAfter=5, leading=28),
 'h2':     S('h2', fontName='Helvetica-Bold', fontSize=13, textColor=DARK, spaceBefore=11, spaceAfter=4, leading=17),
 'h3':     S('h3', fontName='Helvetica-Bold', fontSize=10, textColor=GOLD, spaceBefore=8, spaceAfter=3),
 'body':   S('bd', alignment=TA_JUSTIFY, leading=16, spaceAfter=7),
 'quote':  S('qt', fontName='Helvetica-Oblique', fontSize=11, textColor=DARK, leading=18,
             spaceAfter=8, spaceBefore=8, leftIndent=16, rightIndent=16),
 'hl':     S('hl', fontName='Helvetica-Bold', fontSize=11, textColor=GOLD, alignment=TA_CENTER, leading=17, spaceAfter=8, spaceBefore=8),
 'bullet': S('bu', leading=15, spaceAfter=4, leftIndent=15, firstLineIndent=-9),
 'custo_n':S('cn', fontName='Helvetica-Bold', fontSize=26, textColor=GOLD, alignment=TA_CENTER, leading=32, spaceAfter=2),
 'custo_l':S('cl', fontSize=9, textColor=LGRAY, alignment=TA_CENTER, spaceAfter=0),
 'op3_num':S('on', fontName='Helvetica-Bold', fontSize=30, textColor=GOLD, alignment=TA_CENTER, leading=36, spaceAfter=2),
 'op3_pct':S('op', fontSize=9.5, textColor=LGRAY, alignment=TA_CENTER, spaceAfter=0),
 'cta_h':  S('ch', fontName='Helvetica-Bold', fontSize=14, textColor=GOLD, alignment=TA_CENTER, spaceAfter=5),
 'cta_b':  S('cb', fontSize=10, textColor=CREAM, alignment=TA_CENTER, spaceAfter=4, leading=15),
 'cta_u':  S('cu', fontName='Helvetica-Bold', fontSize=9, textColor=GOLD, alignment=TA_CENTER),
 'foot':   S('ft', fontSize=7, textColor=LGRAY, alignment=TA_CENTER, spaceAfter=2),
 'manif':  S('mf', fontSize=10.5, textColor=GRAY, alignment=TA_JUSTIFY, leading=17, spaceAfter=9),
 'sum_i':  S('si', fontSize=10, textColor=GRAY, leading=19, spaceAfter=2),
}

def gl(): return HRFlowable(width='100%', thickness=1.1, color=GOLD, spaceAfter=6, spaceBefore=6)
def tl(): return HRFlowable(width='100%', thickness=0.3, color=colors.HexColor('#DDDDDD'), spaceAfter=6, spaceBefore=6)
def sp(h=4): return Spacer(1, h*mm)
def lb(t): return Paragraph(t.upper(), ST['label'])
def h1(t): return Paragraph(t, ST['h1'])
def h2(t): return Paragraph(t, ST['h2'])
def h3(t): return Paragraph(t, ST['h3'])
def body(t): return Paragraph(t, ST['body'])
def bl(t): return Paragraph(f'– {t}', ST['bullet'])
def qt(t): return [tl(), Paragraph(f'"{t}"', ST['quote']), tl()]

def hl_box(t):
    tb = Table([[Paragraph(t, ST['hl'])]], colWidths=[AV])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BGDARK),
        ('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12),
        ('LEFTPADDING',(0,0),(-1,-1),16),('RIGHTPADDING',(0,0),(-1,-1),16),
        ('LINEABOVE',(0,0),(-1,0),1.2,GOLD),('LINEBELOW',(0,-1),(-1,-1),1.2,GOLD)]))
    return tb

def caixa_gold(titulo, items):
    rows = [[Paragraph(f'<b>{titulo}</b>', S('cgt',fontName='Helvetica-Bold',fontSize=9,textColor=GOLD,spaceAfter=0))]]
    for it in items:
        rows.append([Paragraph(f'  ▸  {it}', S('cgi',fontSize=9,textColor=CREAM,leading=14,spaceAfter=0))])
    tb = Table(rows, colWidths=[AV])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLACK),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),
        ('LINEABOVE',(0,0),(-1,0),0.8,GOLD),('LINEBELOW',(0,-1),(-1,-1),0.8,GOLD),
        ('LINEBEFORE',(0,0),(0,-1),0.8,GOLD),('LINEAFTER',(-1,0),(-1,-1),0.8,GOLD)]))
    return tb

def tabela(dados, cw=None):
    tb = Table(dados, colWidths=cw or [AV/2, AV/2])
    tb.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),8.5),
        ('TEXTCOLOR',(0,0),(-1,-1),GRAY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
        ('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('LINEABOVE',(0,0),(-1,0),0.8,GOLD),('LINEBELOW',(0,0),(-1,0),0.8,GOLD),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,BGLIGHT])]))
    return tb

def interlude(quote_txt, sub=None):
    """Página editorial escura substituindo foto fullpage."""
    rows = [[Paragraph(quote_txt, S('iq',fontName='Helvetica-Bold',fontSize=20,textColor=CREAM,
             alignment=TA_CENTER,leading=30,spaceAfter=0))]]
    if sub:
        rows.append([Paragraph(sub, S('is',fontName='Helvetica-Oblique',fontSize=10,textColor=GOLD,
             alignment=TA_CENTER,leading=16,spaceAfter=0))])
    inner = Table(rows, colWidths=[AV-40])
    inner.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]))
    outer = Table([[inner]], colWidths=[AV], rowHeights=[H-70*mm])
    outer.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLACK),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('LEFTPADDING',(0,0),(-1,-1),20),('RIGHTPADDING',(0,0),(-1,-1),20),
        ('LINEABOVE',(0,0),(-1,0),1.2,GOLD),('LINEBELOW',(0,-1),(-1,-1),1.2,GOLD)]))
    return [outer, PageBreak()]

def cap_opener(num, titulo, hook):
    """Página escura de abertura de capítulo."""
    rows = [
        [Paragraph(f'CAPÍTULO {num}', S('con',fontName='Helvetica-Bold',fontSize=10,textColor=GOLD,alignment=TA_CENTER,leading=14,spaceAfter=8))],
        [Paragraph(titulo, S('cot',fontName='Helvetica-Bold',fontSize=26,textColor=CREAM,alignment=TA_CENTER,leading=33,spaceAfter=10))],
        [Paragraph(hook, S('coh',fontName='Helvetica-Oblique',fontSize=11,textColor=LGRAY,alignment=TA_CENTER,leading=17,spaceAfter=0))],
    ]
    inner = Table(rows, colWidths=[AV-40])
    inner.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]))
    outer = Table([[inner]], colWidths=[AV], rowHeights=[H-70*mm])
    outer.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLACK),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('LEFTPADDING',(0,0),(-1,-1),20),('RIGHTPADDING',(0,0),(-1,-1),20),
        ('LINEABOVE',(0,0),(-1,0),1.2,GOLD),('LINEBELOW',(0,-1),(-1,-1),1.2,GOLD)]))
    return [outer, PageBreak()]

def resumo(items):
    return caixa_gold('O QUE FICA DESTE CAPÍTULO', items)

def exercicio(titulo, passos):
    rows = [[Paragraph('EXERCÍCIO DO CAPÍTULO', S('ext',fontName='Helvetica-Bold',fontSize=7.5,textColor=GOLD,spaceAfter=1))],
            [Paragraph(f'<b>{titulo}</b>', S('exh',fontName='Helvetica-Bold',fontSize=10.5,textColor=DARK,spaceAfter=3))]]
    for i, p in enumerate(passos, 1):
        rows.append([Paragraph(f'{i}.  {p}', S('exp',fontSize=9,textColor=GRAY,leading=14,spaceAfter=1))])
    tb = Table(rows, colWidths=[AV])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BGLIGHT),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),
        ('LINEBEFORE',(0,0),(0,-1),2,GOLD)]))
    return tb

s = []

# ══════════ CAPA ══════════════════════════════════════════════════
cap_rows = [
    [Paragraph('Z I O N', S('cz',fontName='Helvetica-Bold',fontSize=30,textColor=CREAM,alignment=TA_CENTER,leading=36,spaceAfter=4))],
    [Paragraph('E C O S Y S T E M', S('ce',fontName='Helvetica',fontSize=13,textColor=GOLD,alignment=TA_CENTER,leading=18,spaceAfter=0))],
    [Spacer(1, 16*mm)],
    [Paragraph('CIDADE CIRCULAR', S('ct',fontName='Helvetica-Bold',fontSize=32,textColor=GOLD,alignment=TA_CENTER,leading=38,spaceAfter=0))],
    [Paragraph('Como Transformar o Lixo do Seu Município<br/>em Patrimônio Público', S('cs',fontName='Helvetica',fontSize=14,textColor=CREAM,alignment=TA_CENTER,leading=21,spaceAfter=0))],
    [Spacer(1, 10*mm)],
    [Paragraph('Bancos de praça. Carteiras escolares. Praças inauguradas.<br/>Feitos com o resíduo da própria cidade — sem investimento do município.',
        S('cd2',fontName='Helvetica-Oblique',fontSize=10,textColor=LGRAY,alignment=TA_CENTER,leading=16,spaceAfter=0))],
    [Spacer(1, 22*mm)],
    [Paragraph('BRUNO CHAERK', S('ca',fontName='Helvetica-Bold',fontSize=12,textColor=CREAM,alignment=TA_CENTER,spaceAfter=0))],
    [Paragraph('Zion Hotel Group International  ×  Ecogrupo', S('ch2',fontSize=9,textColor=GOLD,alignment=TA_CENTER,spaceAfter=0))],
    [Spacer(1, 8*mm)],
    [Paragraph('SÉRIE ESPECIAL  ·  ECONOMIA CIRCULAR MUNICIPAL  ·  2026', S('cy',fontSize=7.5,textColor=LGRAY,alignment=TA_CENTER,spaceAfter=0))],
]
capa_in = Table(cap_rows, colWidths=[AV-30])
capa_in.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ('ALIGN',(0,0),(-1,-1),'CENTER')]))
capa = Table([[capa_in]], colWidths=[AV], rowHeights=[H-62*mm])
capa.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLACK),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('LINEABOVE',(0,0),(-1,0),1.5,GOLD),('LINEBELOW',(0,-1),(-1,-1),1.5,GOLD),
    ('LINEBEFORE',(0,0),(0,-1),1.5,GOLD),('LINEAFTER',(-1,0),(-1,-1),1.5,GOLD)]))
s += [capa, PageBreak()]

# ══════════ ABERTURA (interlúdio, pág. 2, sem chrome) ═════════════
s += interlude('O lixo de uma cidade é o único ativo<br/>que o fornecedor paga para entregar —<br/>e que pode voltar para a população<br/>em forma de patrimônio público.',
    'Zion Ecosystem · A tese em uma frase')

# ══════════ EPÍGRAFE ══════════════════════════════════════════════
s.append(sp(50))
s.append(Paragraph('"Não existe lixo. Existe matéria-prima<br/>no lugar errado, esperando método."',
    S('epg',fontName='Helvetica-Oblique',fontSize=14,textColor=DARK,alignment=TA_CENTER,leading=22,spaceAfter=6)))
s.append(sp(4))
s.append(Paragraph('Para os prefeitos que querem inaugurar,<br/>os secretários que seguram o sistema de pé<br/>e os empreendedores que enxergam antes.',
    S('ded',fontSize=9.5,textColor=LGRAY,alignment=TA_CENTER,leading=16,spaceAfter=0)))
s.append(PageBreak())

# ══════════ SOBRE O AUTOR ═════════════════════════════════════════
s += [sp(4), lb('Sobre o autor'), gl(), sp(3)]
s.append(h1('Quem Escreve Este Volume'))
s.append(sp(2))
s.append(Paragraph('Bruno Chaerk é founder e CEO da Zion Hotel Group International, developer de destinos turísticos com background nas redes Meliá, Barceló e Wyndham (Espanha). À frente da Zion, estrutura ativos turísticos, capta investimentos e desenvolve marcas de hospitalidade — do Zion Bubble Glamping, em Florianópolis e Urubici, aos projetos de destino em Alagoas e Santa Catarina.', ST['manif']))
s.append(Paragraph('O Zion Ecosystem nasce da união entre a Zion e a Ecogrupo, empresa de engenharia e operação de resíduos, para levar a economia circular aos municípios brasileiros que o mercado ignora: as cidades de 30 a 150 mil habitantes que pagam todos os dias para enterrar um ativo.', ST['manif']))
s.append(Paragraph('Este volume é um manual de Estado e um convite de negócio ao mesmo tempo. Foi escrito para prefeitos, secretários, vereadores, gestores de consórcios públicos e empreendedores locais que suspeitam — corretamente — que a conta do lixo da sua cidade esconde uma oportunidade.', ST['manif']))
s.append(sp(3))
s.append(hl_box('Nenhuma página deste volume é teoria importada. É método aplicado, regulação vigente e números de mercado verificáveis.'))
s.append(PageBreak())

# ══════════ SUMÁRIO ═══════════════════════════════════════════════
s += [sp(4), lb('Sumário'), gl(), sp(3)]
s.append(h1('O Mapa Deste Volume'))
s.append(sp(3))
sumario = [
    ('Manifesto', 'A cidade que enterra e a cidade que inaugura'),
    ('Introdução', 'Como usar este volume'),
    ('Capítulo 1', 'A Conta Invisível — quanto o lixo realmente custa ao seu município'),
    ('Capítulo 2', 'A Revolução Silenciosa — o novo marco legal que transformou resíduo em ativo'),
    ('Capítulo 3', 'Economia Circular na Prática — o que é, e o que não é'),
    ('Capítulo 4', 'A Prova de Mercado — o caso Orizon e o modelo ecoparque'),
    ('Capítulo 5', 'O CIRO — anatomia de um Centro de Industrialização de Resíduos Orgânicos'),
    ('Capítulo 6', 'As 7 Receitas da Tonelada — o modelo de negócio da cidade circular'),
    ('Capítulo 7', 'O Dinheiro Existe — o mapa dos créditos verdes federais'),
    ('Capítulo 8', 'A Cidade Circular — a escada de implantação, degrau por degrau'),
    ('Ferramentas', 'Checklist do gestor · Matriz de recursos · Glossário'),
    ('Benchmark', 'Números de referência do setor'),
    ('Anexos', 'Minuta do protocolo · Roteiro da reunião · Perguntas da Câmara · Documentos da captação'),
    ('Módulo Final', 'Espelhamento · Colapso de crenças · Custo invisível · Reencadramento · OP3LIF · Linha do tempo · O convite'),
]
for a, b in sumario:
    s.append(Paragraph(f'<b><font color="#C9A84C">{a}</font></b>  ·  {b}', ST['sum_i']))
s.append(sp(5))
s += qt('Leia na ordem. Cada capítulo colapsa uma crença e constrói um degrau. Quem pula degraus chega ao final com a mesma dúvida com que começou.')
s.append(PageBreak())

# ══════════ MANIFESTO ═════════════════════════════════════════════
s += [sp(4), lb('Manifesto'), gl(), sp(3)]
s.append(h1('A Cidade que Enterra e a Cidade que Inaugura'))
s.append(sp(2))
for p in [
 'Fala comigo, prefeito! Existe uma conta na sua prefeitura que ninguém apresenta em coletiva de imprensa. Ela não aparece em placa de inauguração, não rende foto, não gera voto. Mas ela cresce todos os meses, todos os anos, em todos os mandatos — a conta do lixo.',
 'Todos os dias, caminhões saem da sua cidade carregados com toneladas de resíduo. Eles rodam até um aterro — às vezes no município vizinho, às vezes a cem quilômetros — e pagam por tonelada para enterrar. O que foi enterrado não volta. O dinheiro também não.',
 'Agora imagine a cena inversa. O mesmo caminhão sai da cidade com resíduo — e volta semanas depois trazendo bancos de praça, carteiras escolares, lixeiras e decks feitos daquele mesmo material. A praça é inaugurada com placa. A escola recebe carteiras novas. E o custo para o município é menor do que o contrato de aterro que ele já paga hoje.',
 'Isso não é utopia ambiental. É um modelo de negócio validado em bolsa de valores, financiado por crédito federal subsidiado, sustentado por créditos ambientais que indústrias são obrigadas por lei a comprar. O que faltava era alguém estruturar esse ciclo para o tamanho da sua cidade — e apresentar o caminho completo, do protocolo de intenções à placa de inauguração.',
 'Este volume é esse caminho. A cidade que enterra paga duas vezes: paga o aterro e paga o custo político de não ter nada para mostrar. A cidade que inaugura transforma a mesma conta em patrimônio público visível. A escolha entre as duas não depende de orçamento. Depende de método.',
]:
    s.append(Paragraph(p, ST['manif']))
s.append(sp(2))
s.append(Paragraph('— Bruno Chaerk', S('as2',fontName='Helvetica-Bold',fontSize=10,textColor=DARK,spaceAfter=0)))
s.append(PageBreak())

# ══════════ CARTA AO EMPREENDEDOR ═════════════════════════════════
s += [sp(4), lb('Carta ao empreendedor'), gl(), sp(3)]
s.append(h1('Se Você Não É o Prefeito'))
s.append(sp(2))
for p in [
 'Este volume fala muito com o gestor público — mas talvez você que está lendo não tenha gabinete. Talvez você tenha uma empresa na cidade, um capital parado procurando tese, ou apenas a inquietação de quem vê o caminhão do lixo passar e pensa: alguém vai ganhar dinheiro com isso, e não vou ser eu.',
 'Então deixa eu falar diretamente com você. Os maiores negócios de infraestrutura do Brasil nasceram de uma janela regulatória combinada com capital subsidiado — energia eólica nos anos 2000, saneamento depois do marco de 2020. A janela dos resíduos é a próxima, e está aberta agora: a lei criou os créditos, o BNDES abriu as linhas, e cinco mil municípios pagam todos os dias por um serviço pior do que o que podem contratar.',
 'O que torna essa janela diferente é o tamanho da porta de entrada. Você não precisa de bilhões nem de relacionamento em Brasília. Precisa de três coisas: uma cidade âncora — que pode ser a sua —, um modelo estruturado com engenharia, marca e captação resolvidas, e a disposição de operar localmente com padrão de rede. As duas últimas, o Zion Ecosystem entrega. A primeira, você conhece melhor que ninguém: é o lugar onde você vive.',
 'Ao longo do volume, os exercícios trazem sempre um passo específico para você. No final, o mesmo endereço que atende municípios recebe o contato de empreendedores e investidores. O modelo cresce por parceiros locais — e o parceiro da sua região ainda não existe.',
]:
    s.append(Paragraph(p, ST['manif']))
s.append(sp(2))
s += qt('Toda cidade terá a sua planta de valorização nos próximos vinte anos. A única pergunta em aberto é quem vai ser o dono da primeira.')
s.append(PageBreak())

# ══════════ INTRODUÇÃO ════════════════════════════════════════════
s += [sp(4), lb('Introdução'), gl(), sp(3)]
s.append(h1('Como Usar Este Volume'))
s.append(sp(2))
s.append(body('Este não é um livro de sensibilização ambiental. Você não vai encontrar aqui estatísticas de tartarugas nem apelos à consciência. Vai encontrar contas, leis, contratos, fontes de recurso e uma escada de implantação com degraus numerados. O objetivo é um só: que ao final da leitura você saiba exatamente o que fazer na segunda-feira de manhã.'))
s.append(body('O volume foi desenhado para três leitores. O <b>prefeito</b>, que decide e coloca o nome no projeto. O <b>secretário</b> — de Meio Ambiente, Obras ou Fazenda — que executa e responde tecnicamente. E o <b>empreendedor local</b>, que pode se tornar sócio, operador ou fornecedor do ciclo na sua região. Cada capítulo fala com os três; os exercícios ao final de cada capítulo dizem o que cada um pode fazer sem depender dos outros.'))
s.append(body('Os números usados como exemplo ao longo do volume referem-se a um município padrão de 100 mil habitantes, que gera cerca de 45 toneladas de resíduo por dia. Se a sua cidade é maior ou menor, a proporção se mantém — e o Capítulo 8 mostra como municípios pequenos se agrupam em consórcios para alcançar a mesma escala.'))
s.append(sp(2))
s.append(caixa_gold('O QUE VOCÊ TERÁ AO FINAL DA LEITURA', [
 'A conta real do lixo do seu município — e quanto dela pode virar receita',
 'O mapa completo das fontes federais de recurso disponíveis agora',
 'O modelo de contrato que devolve o resíduo em forma de mobiliário público',
 'A escada de implantação em 8 degraus, do protocolo à inauguração',
 'O primeiro passo concreto — que custa zero e não exige licitação',
]))
s.append(PageBreak())

# ══════════ CAPÍTULO 1 ════════════════════════════════════════════
s += cap_opener(1, 'A Conta Invisível', 'A despesa que mais cresce no orçamento é a que menos aparece para o eleitor.')
s += [sp(4), lb('Capítulo 1'), gl(), sp(3)]
s.append(h1('A Conta Invisível'))
s.append(Paragraph('Quanto o lixo realmente custa ao seu município', S('sub1',fontName='Helvetica-Oblique',fontSize=11,textColor=LGRAY,spaceAfter=8)))
s.append(sp(2))
s.append(body('O Brasil gera em torno de 80 milhões de toneladas de resíduos sólidos urbanos por ano. Mais da metade dessa massa é orgânica — restos de comida, poda, feira, cozinha. E a quase totalidade do que é coletado segue para um destino só: o solo. Aterro sanitário, quando a cidade tem sorte e gestão; aterro controlado ou lixão, quando não tem.'))
s.append(body('Para o gestor municipal, essa realidade se traduz numa das maiores despesas correntes da prefeitura. O manejo de resíduos — coleta, transporte, transbordo e disposição final — consome tipicamente de 5% a 15% do orçamento de um município brasileiro de pequeno e médio porte. É mais do que muitas secretarias inteiras.'))
s.append(h2('A anatomia da conta'))
s.append(body('A conta do lixo tem três camadas, e a maioria dos gestores só enxerga a primeira. A camada visível é o contrato: a coleta terceirizada e a tarifa de disposição final, o chamado gate fee do aterro, que no Brasil varia tipicamente entre R$ 80 e R$ 200 por tonelada conforme a região e a distância. A camada semivisível é a logística: combustível, frota, manutenção e horas de equipe rodando até um aterro que quase nunca está no próprio município.'))
s.append(body('A terceira camada é a que não aparece em nenhum relatório: o custo de oportunidade. Cada tonelada enterrada leva consigo material que tem preço de mercado — orgânicos que valem composto e crédito de carbono, plástico que vale matéria-prima e crédito de reciclagem. Enterrar é pagar para se desfazer de algo que outros mercados pagariam para receber.'))
s.append(h2('O exemplo que acompanha o volume'))
s.append(body('Tome o município padrão de 100 mil habitantes. A uma geração média próxima de 0,95 kg por habitante por dia, ele produz cerca de 45 toneladas diárias — 16.400 toneladas por ano. A R$ 150 por tonelada de disposição, são R$ 2,46 milhões anuais só de gate fee, antes da logística. Num mandato de quatro anos, quase R$ 10 milhões saem do orçamento para enterrar material — sem gerar um único metro quadrado de obra pública.'))
s.append(tabela([
 ['Item da conta anual (município de 100 mil hab.)', 'Valor de referência'],
 ['Disposição final (16.400 t × R$ 150/t)', 'R$ 2,46 milhões'],
 ['Logística de transporte até o aterro (estimativa)', 'R$ 600 mil a R$ 1,2 milhão'],
 ['Passivos e contingências ambientais (lixões, TACs)', 'variável — pode dobrar a conta'],
 ['Total típico do manejo por ano', 'R$ 3 a 4,5 milhões'],
], cw=[AV*0.62, AV*0.38]))
s.append(sp(2))
s.append(h2('Por que essa conta só cresce'))
s.append(body('Quatro vetores empurram a conta para cima, mandato após mandato. Primeiro, a população e o consumo crescem — mais gente, mais lixo. Segundo, os aterros enchem: cada célula esgotada empurra o resíduo para mais longe, e cada quilômetro adicional vira custo de frete. Terceiro, a régua regulatória sobe: a Política Nacional de Resíduos Sólidos determinou o fim dos lixões, e o descumprimento gera multa, TAC e responsabilização pessoal do gestor. Quarto, a inflação de serviços reajusta os contratos anualmente.'))
s.append(body('O resultado é uma curva que nenhuma prefeitura controla: a despesa que mais cresce silenciosamente no orçamento é justamente a que menos aparece para o eleitor. Nenhum prefeito foi reeleito por causa do aterro. Muitos foram punidos pelo lixão.'))
s.append(h2('O ciclo político da conta invisível'))
s.append(body('Vale desenhar o mecanismo completo, porque ele explica por que o tema nunca sobe na fila de prioridades — até virar crise. A despesa de resíduos cresce dentro do custeio; o custeio pressionado come o espaço de investimento; menos investimento significa menos entregas visíveis; menos entregas geram desgaste político; e o desgaste empurra o gestor a concentrar energia nas pautas que dão retorno rápido. O lixo, que causou parte do aperto, nunca é percebido como causa — só como paisagem.'))
s.append(body('Há ainda a dimensão pessoal do risco, que poucos gestores dimensionam: disposição irregular expõe o prefeito e o secretário a ação civil pública, improbidade e apontamento de tribunal de contas. O lixão não é apenas um passivo da cidade — é um processo com nome e CPF esperando para acontecer. Resolver o modelo de resíduos é, também, uma operação de blindagem jurídica do próprio gestor.'))
s.append(h2('O que a conta esconde de valor'))
s.append(body('A composição média do resíduo domiciliar brasileiro revela o tamanho do desperdício. Cerca de metade da massa é orgânica; em torno de um terço são recicláveis secos — plástico, papel, metal, vidro; e menos de um quinto é rejeito verdadeiro, sem rota de valorização. Ou seja: a cada 100 toneladas que o município paga para enterrar, mais de 80 têm destino econômico melhor que o solo.'))
s.append(tabela([
 ['Fração do resíduo domiciliar', 'Participação típica', 'Valor embutido'],
 ['Orgânicos (comida, poda, feira)', '≈ 50%', 'Composto + biogás + crédito de carbono'],
 ['Recicláveis secos (plástico, papel, metal, vidro)', '≈ 30%', 'Matéria-prima + crédito de reciclagem'],
 ['Rejeito com poder calorífico', '≈ 10–15%', 'CDR para indústria'],
 ['Rejeito verdadeiro', '< 20%', 'Único destino legítimo do aterro'],
], cw=[AV*0.42, AV*0.22, AV*0.36]))
s.append(sp(2))
s += qt('Lixo não dá foto. Não dá placa. Não dá inauguração. Essa é a tragédia política da conta invisível — e é exatamente ela que este volume vai virar do avesso.')
s.append(resumo([
 'O manejo de resíduos consome de 5% a 15% do orçamento municipal — e a curva só sobe',
 'A conta tem três camadas: contrato, logística e custo de oportunidade — a terceira é a maior',
 'Mais de 80% da massa enterrada tem destino econômico melhor que o solo',
 'Disposição irregular é risco jurídico pessoal do gestor, não só passivo da cidade',
]))
s.append(sp(2))
s.append(exercicio('Levante a conta real do seu município', [
 'Peça à Secretaria de Fazenda o valor pago no último ano por coleta, transporte e disposição final — separados.',
 'Divida o total de disposição pelo número de toneladas: esse é o seu gate fee real por tonelada.',
 'Multiplique a despesa anual por 4. Esse é o número que você vai comparar com tudo que vem nos próximos capítulos.',
]))
s.append(PageBreak())

# ══════════ INTERLÚDIO 0B ═════════════════════════════════════════
s += interlude('A cada 100 toneladas enterradas,<br/>mais de 80 tinham<br/>destino melhor que o solo.', 'Capítulo 1 · O tamanho do desperdício')

# ══════════ CAPÍTULO 2 ════════════════════════════════════════════
s += cap_opener(2, 'A Revolução Silenciosa', 'Entre 2010 e 2024, quatro marcos legais transformaram a tonelada enterrada em ativo desperdiçado.')
s += [sp(4), lb('Capítulo 2'), gl(), sp(3)]
s.append(h1('A Revolução Silenciosa'))
s.append(Paragraph('O novo marco legal que transformou resíduo em ativo', S('sub2',fontName='Helvetica-Oblique',fontSize=11,textColor=LGRAY,spaceAfter=8)))
s.append(sp(2))
s.append(body('Entre 2010 e 2024, o Brasil construiu — em silêncio, longe do noticiário — o arcabouço legal mais completo da América Latina para transformar resíduo em ativo econômico. Quatro marcos se empilharam, e a combinação deles muda completamente a posição do gestor municipal: de pagador de conta a dono de matéria-prima.'))
s.append(h2('Marco 1 — A Política Nacional de Resíduos Sólidos (Lei 12.305/2010)'))
s.append(body('A PNRS é a fundação. Ela estabeleceu a hierarquia obrigatória — não geração, redução, reutilização, reciclagem, tratamento e, só por último, disposição final — e determinou o encerramento dos lixões. Também criou dois conceitos que sustentam tudo que vem depois: a responsabilidade compartilhada pelo ciclo de vida dos produtos e a logística reversa, que obriga fabricantes e importadores a recuperar parte do que colocam no mercado.'))
s.append(body('Para o município, a PNRS é ao mesmo tempo cobrança e alavanca. Cobrança, porque a disposição irregular gera responsabilização. Alavanca, porque ela obriga a existência de planos municipais de gestão integrada — e municípios com plano atualizado são exatamente os que acessam recursos federais com prioridade.'))
s.append(h2('Marco 2 — O Certificado de Crédito de Reciclagem (Decreto 11.413/2023)'))
s.append(body('Aqui a lei vira dinheiro. O Decreto 11.413 criou o CCRLR — Certificado de Crédito de Reciclagem de Logística Reversa. O mecanismo é elegante: a indústria que coloca embalagens no mercado contrai uma obrigação legal de recuperação. Quem recicla — cooperativa, operador, central de triagem — emite nota fiscal do material recuperado e gera um crédito. A indústria compra esse crédito para quitar sua obrigação.'))
s.append(body('Traduzindo: toda tonelada reciclada no seu município pode gerar duas receitas — o valor do material em si e o certificado, vendido às indústrias obrigadas. É receita recorrente, criada por decreto federal, que a maioria absoluta dos municípios brasileiros ainda não capturou.'))
s.append(h2('Marco 3 — O Mercado de Carbono Regulado (Lei 15.042/2024)'))
s.append(body('Em dezembro de 2024, o Brasil sancionou o SBCE — Sistema Brasileiro de Comércio de Emissões. A lei cria dois ativos: a Cota Brasileira de Emissões (CBE) e o Certificado de Redução ou Remoção Verificada de Emissões (CRVE). Empresas de setores regulados terão tetos de emissão e precisarão comprar créditos de quem reduz.'))
s.append(body('E onde o município entra? No metano. Resíduo orgânico enterrado apodrece sem oxigênio e emite metano, gás com potencial de aquecimento cerca de 28 vezes maior que o CO2. Cada tonelada de orgânico desviada do aterro — para compostagem ou biodigestão — evita essas emissões e pode gerar CRVE. O lixo orgânico da sua cidade, que hoje custa para enterrar, tornou-se um gerador potencial de ativo financeiro com mercado regulado nacional.'))
s.append(h2('Marco 4 — O Novo Marco do Saneamento (Lei 14.026/2020)'))
s.append(body('O marco do saneamento incluiu o manejo de resíduos sólidos entre os serviços com metas de universalização e sustentabilidade econômica, empurrando os municípios para modelos de cobrança e para a regionalização — os blocos e consórcios que permitem escala. Ele também normalizou a participação privada: concessões e PPPs de resíduos deixaram de ser exceção.'))
s.append(sp(2))
s.append(tabela([
 ['Marco legal', 'O que criou', 'O que significa para o município'],
 ['PNRS (2010)', 'Hierarquia + logística reversa', 'Obrigação de tratar; prioridade de recurso p/ quem tem plano'],
 ['Decreto 11.413 (2023)', 'Crédito de reciclagem (CCRLR)', 'Toneladas recicladas viram certificado vendável'],
 ['Lei 15.042 (2024)', 'Mercado de carbono (SBCE/CRVE)', 'Orgânico desviado do aterro vira crédito de carbono'],
 ['Lei 14.026 (2020)', 'Marco do saneamento', 'Consórcios, cobrança e PPPs viram caminho padrão'],
], cw=[AV*0.24, AV*0.33, AV*0.43]))
s.append(sp(2))
s.append(h2('O que muda na prática para o gestor'))
s.append(body('A leitura combinada dos quatro marcos muda três coisas concretas na mesa do prefeito. Primeiro, a régua de risco: manter o modelo atual deixou de ser neutro — é descumprimento com prazo vencido e responsabilização crescente. Segundo, a régua de acesso: praticamente todos os recursos federais de resíduos priorizam municípios com plano atualizado, regularidade fiscal e solução consorciada; arrumar a casa documental vale dinheiro. Terceiro, a régua de parceria: a lei empurrou catadores e cooperativas para dentro do sistema formal — projetos que os integram pontuam mais, licenciam mais rápido e geram menos atrito social.'))
s.append(body('Há um detalhe estratégico que passa despercebido: os dois créditos — reciclagem e carbono — foram desenhados para remunerar quem opera, não quem legisla. Isso significa que o valor criado pelo arcabouço fica na ponta, na cidade onde a tonelada é tratada. Pela primeira vez, a regulação federal joga o dinheiro na direção do município — desde que exista, no município, quem processe.'))
s.append(h2('A linha do tempo regulatória'))
s.append(tabela([
 ['Ano', 'Marco', 'Efeito sobre o valor da tonelada'],
 ['2010', 'PNRS (Lei 12.305)', 'Cria a obrigação de valorizar antes de dispor'],
 ['2020', 'Marco do Saneamento (Lei 14.026)', 'Traz metas, consórcios e capital privado'],
 ['2022–23', 'Decretos de logística reversa e CCRLR', 'A tonelada reciclada passa a gerar certificado vendável'],
 ['2024', 'SBCE (Lei 15.042)', 'O metano evitado ganha mercado regulado'],
 ['2025+', 'Regulamentação do SBCE em curso', 'Demanda por CRVE cresce com os tetos de emissão'],
], cw=[AV*0.12, AV*0.40, AV*0.48]))
s.append(sp(2))
s.append(body('Repare no padrão: a cada dois anos, um novo texto legal aumentou o valor econômico da mesma tonelada. Quem estruturar a operação agora captura a curva inteira; quem esperar a regulamentação "terminar" vai comprar o ingresso mais caro — e atrás de quem chegou primeiro.'))
s += qt('Quem continua tratando lixo como problema jurídico está lendo a lei errada. O arcabouço que existe hoje foi desenhado para quem tratar lixo como ativo.')
s.append(resumo([
 'Quatro marcos empilhados: PNRS, marco do saneamento, CCRLR e SBCE',
 'Os créditos remuneram quem opera na ponta — o valor fica na cidade que processa',
 'Plano atualizado + regularidade fiscal + consórcio = prioridade em todo recurso federal',
 'Cada novo texto legal aumentou o valor da tonelada — a curva favorece quem começa agora',
]))
s.append(sp(2))
s.append(exercicio('Verifique a posição legal do seu município', [
 'Confirme se o Plano Municipal de Gestão Integrada de Resíduos Sólidos existe e quando foi atualizado.',
 'Verifique se o município ainda usa lixão ou aterro controlado — e se há TAC ou processo em curso.',
 'Pergunte à procuradoria se algum operador local já emite créditos de reciclagem na sua região.',
]))
s.append(PageBreak())

# ══════════ CAPÍTULO 3 ════════════════════════════════════════════
s += cap_opener(3, 'Economia Circular na Prática', 'A régua que separa projeto de paisagismo institucional: quem compra o que sai?')
s += [sp(4), lb('Capítulo 3'), gl(), sp(3)]
s.append(h1('Economia Circular na Prática'))
s.append(Paragraph('O que é — e o que não é', S('sub3',fontName='Helvetica-Oblique',fontSize=11,textColor=LGRAY,spaceAfter=8)))
s.append(sp(2))
s.append(body('Economia circular virou expressão de moda, e como toda expressão de moda, foi esvaziada. Antes de construir o modelo do seu município, é preciso separar o conceito operacional — que gera contrato, receita e obra — do conceito decorativo, que gera seminário e banner.'))
s.append(h2('A definição que funciona'))
s.append(body('Economia circular é o desenho de sistemas em que o resíduo de um processo vira insumo de outro, mantendo materiais em uso pelo maior tempo possível e no maior valor possível. A palavra-chave não é reciclagem — é <b>valor</b>. Um sistema circular bem desenhado não pergunta "como descartar direito?", e sim "qual é o uso mais valioso deste material agora?".'))
s.append(body('Na prática municipal, isso significa uma cascata: o orgânico vira composto e biogás antes de qualquer aterro; o plástico vira matéria-prima industrial antes de virar fardo de exportação; o que não tem rota de valor vira combustível derivado de resíduo; e só o rejeito verdadeiro — tipicamente menos de 20% da massa — segue para disposição final.'))
s.append(h2('O que não é economia circular'))
s.append(body('Não é coleta seletiva sem indústria na ponta — separar na fonte e misturar no caminhão é teatro caro. Não é campanha de conscientização sem infraestrutura — pedir ao cidadão que separe o que a prefeitura não tem onde processar destrói a credibilidade do programa. E não é usina milagrosa vendida em feira — projetos que prometem eliminar 100% do lixo sem contrato de destino para os produtos terminam como sucata judicializada.'))
s.append(body('A régua para separar projeto real de projeto decorativo é uma só: <b>quem compra o que sai?</b> Se cada saída do sistema — composto, madeira plástica, crédito, energia — tem comprador identificado e preço de referência, o projeto é economia. Se não tem, é paisagismo institucional.'))
s.append(h2('Onde o mundo já chegou'))
s.append(body('A União Europeia taxou o aterro até torná-lo o destino mais caro — e a compostagem e a reciclagem floresceram como consequência econômica, não como virtude. A Coreia do Sul cobra o descarte de orgânicos por peso e recupera mais de 90% deles. São Francisco tornou a separação de orgânicos obrigatória e transformou o composto em produto com marca própria, vendido aos vinhedos da região.'))
s.append(body('O padrão se repete em todos os casos de sucesso: ninguém venceu pela consciência; venceram pelo preço relativo. Quando enterrar custa mais do que valorizar, o sistema gira sozinho. A boa notícia brasileira é que essa virada de preços já começou — não por taxação, mas pelos créditos que os capítulos anteriores mostraram: cada tonelada valorizada agora carrega receita extra que a tonelada enterrada não tem.'))
s.append(h2('A fração esquecida — e decisiva'))
s.append(body('Todo debate público sobre reciclagem gira em torno de plástico, papel e alumínio. Mas a fração que decide o jogo econômico municipal é a orgânica: é ela que representa metade da massa, é ela que gera o chorume e o metano que encarecem o aterro, e é ela que carrega o maior crédito climático por tonelada. Município que resolve o orgânico resolve simultaneamente metade do volume, o maior passivo ambiental e a maior fonte de crédito de carbono.'))
s.append(sp(2))
s.append(caixa_gold('A CASCATA DE VALOR DA TONELADA MUNICIPAL', [
 'Orgânicos (≈ 50%) → composto, biofertilizante, biogás + créditos de carbono',
 'Recicláveis secos (≈ 30%) → matéria-prima e madeira plástica + créditos de reciclagem',
 'Não recicláveis com poder calorífico → CDR para indústria',
 'Rejeito verdadeiro (< 20%) → único material que ainda vai ao aterro',
]))
s.append(sp(2))
s.append(h2('Os quatro níveis de maturidade circular de um município'))
s.append(body('Para saber o tamanho do salto da sua cidade, localize-a nesta escada de maturidade. O <b>nível zero</b> é o lixão: disposição irregular, passivo jurídico ativo, nenhuma valorização. O <b>nível um</b> é o aterro regularizado: a cidade cumpre o mínimo legal, pagando caro por isso, sem capturar valor algum. O <b>nível dois</b> é a coleta seletiva com triagem: cooperativas organizadas recuperam parte dos secos, mas o orgânico — metade da massa — segue enterrado, e não há indústria na ponta. O <b>nível três</b> é a valorização industrial integrada: as duas frações processadas, créditos emitidos, produtos vendidos e contrapartida voltando à cidade.'))
s.append(body('A maioria absoluta dos municípios brasileiros está entre o zero e o um. O pulo do gato é que não é preciso subir degrau por degrau ao longo de décadas, como fizeram os países ricos: o modelo CIRO nasce no nível três, e a cidade sobe a escada inteira num único contrato. É o mesmo salto que a telefonia deu quando o celular dispensou a fiação de cobre — o atraso vira vantagem de quem pula direto para a tecnologia madura.'))
s.append(h2('Compostagem comunitária e industrial: aliadas, não rivais'))
s.append(body('Uma dúvida comum de secretário: investir em pátios comunitários de compostagem ou numa planta industrial? A resposta é ambos, com papéis diferentes. Os módulos comunitários — na escola, na feira, no bairro — têm função pedagógica e política: ensinam a separação, criam vínculo e produzem o composto das hortas locais. A planta industrial dá escala, padrão sanitário e créditos certificáveis. O erro é esperar de um o resultado do outro: pátio comunitário não zera a conta do aterro, e planta industrial sem educação na ponta recebe orgânico contaminado. No desenho do Zion Ecosystem, os módulos comunitários são financiados pelos editais do FNMA e alimentam a cultura da separação — enquanto a planta faz o volume virar economia.'))
s.append(sp(2))
s += qt('A pergunta que separa projeto de paisagismo institucional: quem compra o que sai? Se a resposta é concreta, você tem economia circular. Se é abstrata, você tem um banner.')
s.append(resumo([
 'Circularidade é cascata de valor, não coleta seletiva com banner',
 'Os casos internacionais venceram pelo preço relativo, não pela consciência',
 'A fração orgânica decide o jogo: metade da massa, maior passivo, maior crédito',
 'O município pode pular direto ao nível três de maturidade — num único contrato',
]))
s.append(sp(2))
s.append(exercicio('Aplique a régua do comprador', [
 'Liste as iniciativas de reciclagem ou compostagem que já existem no seu município, por menores que sejam.',
 'Para cada uma, responda: quem compra o que sai? Por quanto? Com que regularidade?',
 'As que não têm resposta são as que precisam de indústria na ponta — é exatamente o vazio que o CIRO preenche.',
]))
s.append(PageBreak())

# ══════════ INTERLÚDIO 1 ══════════════════════════════════════════
s += interlude('Quando enterrar custa mais<br/>do que valorizar,<br/>o sistema gira sozinho.', 'Capítulo 3 · A lição dos casos internacionais')

# ══════════ CAPÍTULO 4 ════════════════════════════════════════════
s += cap_opener(4, 'A Prova de Mercado', 'Uma empresa vale R$ 7 bilhões na bolsa fazendo com o lixo das capitais o que a sua cidade ainda enterra.')
s += [sp(4), lb('Capítulo 4'), gl(), sp(3)]
s.append(h1('A Prova de Mercado'))
s.append(Paragraph('O caso Orizon e o modelo ecoparque', S('sub4',fontName='Helvetica-Oblique',fontSize=11,textColor=LGRAY,spaceAfter=8)))
s.append(sp(2))
s.append(body('Toda tese de negócio precisa responder a uma pergunta antes de pedir a confiança de um gestor público: alguém já provou que isso funciona em escala, com dinheiro de verdade, sob escrutínio de verdade? Para a economia circular de resíduos no Brasil, a resposta tem nome, ticker e auditoria: Orizon Valorização de Resíduos, listada na B3 sob o código ORVR3.'))
s.append(h2('De quase falida a R$ 7 bilhões'))
s.append(body('A história importa porque começa mal. A antecessora da Orizon, a Haztec, tentou fazer de tudo — aterros, equipamentos, tratamento de água — e quase morreu de falta de foco, chegando a operar com dívida de 12 vezes o EBITDA. A virada veio quando a companhia abandonou a diversificação e concentrou tudo numa única tese: extrair o máximo de valor de cada tonelada de resíduo urbano. Com essa tese, fez IPO em 2021 captando R$ 554 milhões — e hoje vale cerca de R$ 7 bilhões.'))
s.append(body('Os números atuais dão o tamanho da validação: 18 ecoparques em 12 estados, resíduo de mais de 40 milhões de brasileiros, receita anual acima de R$ 1 bilhão e margem EBITDA na casa de 48% — margem de software numa empresa que trabalha com aquilo que todo mundo paga para não ver.'))
s.append(h2('O que é um ecoparque'))
s.append(body('O conceito central da Orizon é transformar o aterro de fim de linha em plataforma industrial. Um ecoparque é uma área de milhões de metros quadrados onde, ao redor da célula de disposição, operam as indústrias de valorização: triagem de recicláveis, produção de CDR, captura de biogás, geração de energia, purificação para biometano e unidade de fertilizante orgânico. A mesma tonelada que entra paga gate fee — e depois vai gerando receita camada por camada.'))
s.append(tabela([
 ['Indicador Orizon', 'Número', 'O que valida para o nosso modelo'],
 ['Valor de mercado', '≈ R$ 7 bilhões', 'A tese resíduo-como-ativo precifica em bolsa'],
 ['Margem EBITDA', '≈ 48%', 'Valorização de resíduo é indústria de alta margem'],
 ['Gate fee médio', 'R$ 84,80/t', 'Referência nacional de preço por tonelada'],
 ['Créditos de carbono 2024', '1,1 milhão vendidos', 'O metano evitado tem mercado real'],
 ['Comprador âncora', 'Google — 750 mil créditos', 'Big techs compram crédito brasileiro de resíduo'],
 ['Receita pública vs. privada', '≈ 45% / 55%', 'O mix público-privado sustenta o negócio'],
], cw=[AV*0.30, AV*0.26, AV*0.44]))
s.append(sp(2))
s.append(h2('O detalhe que interessa ao seu município'))
s.append(body('A Orizon opera onde há escala metropolitana: regiões com milhões de habitantes, contratos gigantes, aterros próprios. O modelo dela exige um volume que uma cidade de 80 mil habitantes jamais oferecerá sozinha. E é precisamente aí que mora a oportunidade: o Brasil tem mais de 5 mil municípios abaixo do radar dos grandes players, todos pagando para enterrar, nenhum com acesso ao modelo.'))
s.append(body('O Zion Ecosystem é a tradução desse modelo para a escala municipal: uma planta modular — o CIRO, que o próximo capítulo destrincha — dimensionada para 30 a 150 mil habitantes ou para consórcios de municípios menores, financiada por crédito verde federal em vez de follow-on bilionário, e com um diferencial que nenhum player de megaescala oferece: parte do valor volta ao município em produto público visível.'))
s.append(body('Quando o BNDES aprovou cerca de R$ 450 milhões para uma planta de biometano ligada à Orizon, o banco sinalizou algo maior que uma operação: sinalizou que a tese de valorização de resíduos é financiável com dinheiro público subsidiado. A porta pela qual passaremos já foi aberta — por quem tinha muito mais a provar.'))
s.append(h2('As quatro lições de gestão do caso'))
s.append(body('Além dos números, o caso ensina método. <b>Lição um — foco:</b> a Haztec quase morreu tentando fazer nove negócios; a Orizon virou império fazendo um. O CIRO segue a mesma disciplina: valorização de resíduo municipal, nada além. <b>Lição dois — mix de receita:</b> 45% público e 55% privado; nenhum contrato sozinho derruba a operação. <b>Lição três — o crédito é negócio, não subproduto:</b> a companhia estruturou área própria de carbono e vendeu até para o Google; quem trata crédito como acaso deixa a margem na mesa. <b>Lição quatro — CAPEX se divide:</b> as grandes obras saíram em parceria (Sabesp na usina de energia, Edge no biometano, BNDES no funding) — ninguém constrói infraestrutura pesada sozinho, e não há mérito em tentar.'))
s.append(h2('Megaescala e escala municipal, lado a lado'))
s.append(tabela([
 ['Dimensão', 'Ecoparque (Orizon)', 'CIRO (Zion Ecosystem)'],
 ['População atendida', 'milhões — regiões metropolitanas', '80–150 mil hab. ou consórcio'],
 ['Área', '2 a 3 milhões de m²', '10 a 20 mil m²'],
 ['CAPEX típico', 'centenas de R$ milhões', '≈ R$ 10 milhões'],
 ['Funding', 'IPO, follow-on, debêntures', 'Fundo Clima + Finep + créditos'],
 ['Aterro próprio', 'sim — núcleo do modelo', 'não — a planta desvia do aterro'],
 ['Retorno visível ao cidadão', 'não faz parte do modelo', 'mobiliário público trimestral'],
], cw=[AV*0.28, AV*0.36, AV*0.36]))
s.append(sp(2))
s.append(body('A tabela deixa clara a complementaridade: não competimos com a megaescala — ocupamos o vazio que ela não tem como atender. E, num cenário futuro, os dois modelos convergem: plantas municipais podem vender créditos em bloco, fornecer CDR e integrar cadeias que os grandes players já compram.'))
s += qt('Existe uma empresa na bolsa valendo sete bilhões de reais fazendo isso para quarenta milhões de brasileiros nas capitais. A pergunta não é se o modelo funciona. É por que a sua cidade ainda está fora dele.')
s.append(resumo([
 'A tese resíduo-como-ativo está validada em bolsa: R$ 7 bi de valor, 48% de margem',
 'Foco, mix de receita, crédito como negócio e CAPEX em parceria — as 4 lições do caso',
 'O gate fee médio de mercado (R$ 84,80/t) é a régua para o seu contrato',
 'O CIRO ocupa o flanco que a megaescala ignora — e devolve o que ela não devolve',
]))
s.append(sp(2))
s.append(exercicio('Posicione seu município no mapa do setor', [
 'Descubra para qual aterro vai o resíduo da sua cidade e quem é o operador — é um player nacional ou regional?',
 'Compare o gate fee que você paga (exercício do Capítulo 1) com a referência de R$ 84,80/t.',
 'Verifique se há municípios vizinhos no mesmo aterro — eles são seus candidatos naturais a consórcio.',
]))
s.append(PageBreak())

# ══════════ INTERLÚDIO 1B ═════════════════════════════════════════
s += interlude('A porta pela qual passaremos<br/>já foi aberta —<br/>por quem tinha muito mais a provar.', 'Capítulo 4 · O precedente que muda a conversa com o banco')

# ══════════ CAPÍTULO 5 ════════════════════════════════════════════
s += cap_opener(5, 'O CIRO', 'Uma fábrica cujo fornecedor paga para entregar a matéria-prima.')
s += [sp(4), lb('Capítulo 5'), gl(), sp(3)]
s.append(h1('O CIRO'))
s.append(Paragraph('Anatomia de um Centro de Industrialização de Resíduos Orgânicos', S('sub5',fontName='Helvetica-Oblique',fontSize=11,textColor=LGRAY,spaceAfter=8)))
s.append(sp(2))
s.append(body('O CIRO é a peça industrial do Zion Ecosystem: a planta que recebe o resíduo do município, dos bairros e dos empreendimentos parceiros, e o converte em produto, energia e crédito. Este capítulo abre a planta ao meio para o gestor entender exatamente o que está contratando — e o empreendedor, o que está operando.'))
s.append(h2('As três portas de entrada'))
s.append(body('A matéria-prima chega por três fluxos. O primeiro é o <b>contrato municipal</b>: a fração orgânica e reciclável da coleta pública, entregue pela prefeitura ou pelo consórcio mediante gate fee inferior ao custo atual de aterro. O segundo é a <b>coleta premium residencial</b>: assinantes que pagam mensalidade por um balde segregado e a garantia de destino nobre. O terceiro é o fluxo <b>B2B</b>: hotéis, glampings, restaurantes e supermercados que pagam pela coleta dedicada e pelo selo de destino certificado — no ecossistema Zion, o selo Resíduo Zero.'))
s.append(h2('Linha 1 — Orgânicos'))
s.append(body('A fração orgânica segue para compostagem acelerada em leiras aeradas ou reatores fechados, com controle de temperatura, umidade e oxigenação que reduz o ciclo de meses para semanas e elimina odor e vetores. Parte do fluxo pode alimentar um biodigestor, que produz biogás para energia da própria planta — e, em escala maior, biometano veicular.'))
s.append(body('As saídas da linha orgânica: composto e biofertilizante ensacados, com mercado em paisagismo, agricultura e hortas urbanas; energia; e o ativo silencioso — cada tonelada desviada do aterro evita metano e alimenta o projeto de créditos de carbono da planta, certificado por metodologia de compostagem e aterro evitado.'))
s.append(h2('Linha 2 — Madeira plástica'))
s.append(body('A fração plástica — inclusive a de baixa qualidade, que as cadeias tradicionais rejeitam — é triturada, lavada e extrusada em perfis de madeira plástica: um material imune a cupim, umidade e apodrecimento, que dispensa pintura e dura décadas. Dos perfis nascem os produtos que dão rosto ao projeto: bancos de praça, carteiras escolares, lixeiras, decks, pontes de trilha e playgrounds.'))
s.append(body('É esta linha que produz a contrapartida ao município — o mobiliário que volta para a cidade — e que gera, tonelada a tonelada, os certificados de crédito de reciclagem criados pelo Decreto 11.413. A mesma extrusora fabrica, portanto, o produto físico e o ativo financeiro.'))
s.append(h2('Dimensão, área e equipe'))
s.append(tabela([
 ['Parâmetro da planta-piloto', 'Referência'],
 ['Capacidade — orgânicos', '30 a 50 toneladas/dia'],
 ['Capacidade — recicláveis p/ madeira plástica', '10 toneladas/dia'],
 ['População atendida', '80 a 150 mil hab. (ou consórcio)'],
 ['Área necessária', '10 a 20 mil m² — galpão + pátio de leiras'],
 ['Empregos diretos', '25 a 40, priorizando cooperados locais'],
 ['CAPEX de referência', 'R$ 10 milhões (detalhado no Cap. 7)'],
], cw=[AV*0.55, AV*0.45]))
s.append(sp(2))
s.append(h2('Onde a planta se instala'))
s.append(body('O terreno ideal é área industrial ou rural próxima à malha urbana, com acesso de caminhão e distância de vizinhança sensível. Para o município âncora, a cessão ou doação de área pública é a contrapartida clássica — e transforma um terreno ocioso da prefeitura em polo industrial verde com empregos e arrecadação. O licenciamento ambiental corre no órgão estadual; compostagem e reciclagem têm enquadramento muito mais leve que aterros e incineração.'))
s.append(h2('O caminho da tonelada dentro da planta'))
s.append(body('Siga uma carga da chegada à saída. O caminhão passa pela <b>balança</b>, e o peso entra no sistema com origem, rota e horário — é esse registro que vira fatura, relatório público e lastro de crédito. Na <b>triagem</b>, esteira e equipe separam o que a coleta misturou; o orgânico segue para as leiras ou para o biodigestor, o plástico para a linha de lavagem e trituração, papel e metal para os fardos das cooperativas parceiras. Semanas depois, a mesma massa cruza a <b>expedição</b> em quatro formas: sacos de composto, perfis e mobiliário de madeira plástica, fardos de recicláveis e relatórios de tonelada que sustentam a emissão de CCRLR e de créditos de carbono.'))
s.append(body('A camada digital é o que separa o CIRO de um pátio de reciclagem tradicional: cada lote é rastreável da origem ao destino. Essa rastreabilidade não é burocracia — é o produto. Sem ela não há certificado auditável, não há crédito, não há relatório para a prefeitura publicar. É a planta de dados sobre a planta física que transforma tonelada em ativo.'))
s.append(h2('Gente: cooperativas, empregos e arrecadação'))
s.append(body('O CIRO não substitui os catadores — formaliza e multiplica o trabalho deles. As cooperativas locais são as primeiras candidatas à operação de triagem, com contrato, equipamento de proteção e renda previsível; a legislação de resíduos premia explicitamente essa integração, e a experiência mostra que nenhum ator conhece melhor a logística real da cidade. Somam-se os empregos industriais da planta — 25 a 40 diretos —, os indiretos da logística e o ISS que passa a ser recolhido no próprio município, sobre um serviço que antes era pago para fora.'))
s.append(sp(2))
s += qt('O CIRO não é um aterro melhorado. É uma fábrica cujo fornecedor paga para entregar a matéria-prima — e cujo principal produto político é entregue de volta à cidade com placa de inauguração.')
s.append(resumo([
 'Três portas de entrada: contrato municipal, assinaturas premium e B2B com selo',
 'Duas linhas industriais: orgânicos (composto, biogás, carbono) e madeira plástica (mobiliário, CCRLR)',
 'A rastreabilidade digital é o produto: sem dado auditável não há crédito',
 'Cooperativas integradas, 25–40 empregos diretos e ISS que fica na cidade',
]))
s.append(sp(2))
s.append(exercicio('Mapeie o terreno candidato', [
 'Liste áreas públicas ociosas de 10 a 20 mil m² com acesso de caminhão no seu município.',
 'Verifique o zoneamento: a área permite atividade industrial leve ou agroindustrial?',
 'Identifique as cooperativas de catadores ativas — elas são as primeiras candidatas à operação de triagem.',
]))
s.append(PageBreak())

# ══════════ INTERLÚDIO 1C ═════════════════════════════════════════
s += interlude('Sem dado auditável<br/>não há crédito.<br/>A rastreabilidade é o produto.', 'Capítulo 5 · A planta de dados sobre a planta física')

# ══════════ CAPÍTULO 6 ════════════════════════════════════════════
s += cap_opener(6, 'As 7 Receitas da Tonelada', 'O aterro tem uma linha de receita. Nós temos sete.')
s += [sp(4), lb('Capítulo 6'), gl(), sp(3)]
s.append(h1('As 7 Receitas da Tonelada'))
s.append(Paragraph('O modelo de negócio da cidade circular', S('sub6',fontName='Helvetica-Oblique',fontSize=11,textColor=LGRAY,spaceAfter=8)))
s.append(sp(2))
s.append(body('A força do modelo não está em nenhuma receita isolada — está no empilhamento. A mesma tonelada que entra pela balança gera valor em até sete camadas diferentes. É esse empilhamento que permite ao CIRO cobrar do município menos do que o aterro cobra, e ainda assim devolver parte do valor em mobiliário. Vamos abrir as sete, uma a uma.'))
s.append(h2('Receita 1 — Gate fee municipal'))
s.append(body('A âncora do modelo. O município paga por tonelada tratada — sempre abaixo do custo atual de disposição, porque o CIRO não depende só dessa receita para fechar a conta. Para a prefeitura, é troca de contrato com economia imediata; para a planta, é o recebível previsível que sustenta o financiamento. É este contrato que o banco lê como garantia.'))
s.append(h2('Receita 2 — Assinatura residencial premium'))
s.append(body('Nos bairros de maior renda, famílias assinam a coleta segregada: balde dedicado, recolhimento semanal, relatório de impacto e desconto em composto. A mensalidade de R$ 39 a R$ 79 parece pequena — mas mil assinantes geram mais de meio milhão de reais por ano com custo logístico marginal, e criam a base social que defende o projeto.'))
s.append(h2('Receita 3 — B2B e o selo Resíduo Zero'))
s.append(body('Hotéis, glampings, restaurantes e mercados pagam pela coleta dedicada e licenciam o selo que certifica destino integral. Para um empreendimento turístico, dizer ao hóspede que nada do que ele descartou foi para aterro — e que o jardim é adubado com o composto do próprio resort — é diferencial de marca que nenhum concorrente improvisa. A rede Zion Glamping é a vitrine e o primeiro cliente.'))
s.append(h2('Receita 4 — Composto e biofertilizante'))
s.append(body('O produto físico da linha orgânica, ensacado e vendido a paisagistas, produtores rurais, hortas urbanas e varejo agropecuário. Parte da produção pode abastecer as praças e hortas comunitárias do próprio município — mais uma contrapartida visível de custo baixo.'))
s.append(h2('Receita 5 — Mobiliário de madeira plástica'))
s.append(body('Depois de cumprida a contrapartida contratual com o município, o excedente da linha de extrusão é vendido: outras prefeituras, condomínios, escolas privadas, parques e orlas. O produto carrega a história na etiqueta — "feito do resíduo de uma cidade brasileira" — e concorre com madeira de lei sem derrubar uma árvore.'))
s.append(h2('Receitas 6 e 7 — Os créditos'))
s.append(body('As duas receitas invisíveis que mudam a matemática. O <b>CCRLR</b>: cada tonelada reciclada gera certificado vendido às indústrias com obrigação de logística reversa — receita criada por decreto, recorrente, com demanda legalmente garantida. E o <b>crédito de carbono</b>: o metano evitado pela linha orgânica vira CRVE, vendável no mercado voluntário hoje e no mercado regulado do SBCE amanhã. No caso-base do projeto os créditos são tratados como upside — quando entram, aceleram; a conta fecha sem eles.'))
s.append(sp(2))
s.append(tabela([
 ['#', 'Receita', 'Pagador', 'Natureza'],
 ['1', 'Gate fee municipal', 'Prefeitura / consórcio', 'Recorrente — âncora'],
 ['2', 'Assinatura residencial', 'Famílias', 'Recorrente'],
 ['3', 'B2B + selo Resíduo Zero', 'Hotéis, restaurantes, varejo', 'Recorrente'],
 ['4', 'Composto e biofertilizante', 'Agro, paisagismo, varejo', 'Venda de produto'],
 ['5', 'Mobiliário madeira plástica', 'Prefeituras e privados', 'Venda de produto'],
 ['6', 'Crédito de reciclagem (CCRLR)', 'Indústrias obrigadas', 'Recorrente por tonelada'],
 ['7', 'Crédito de carbono (CRVE)', 'Mercado voluntário / SBCE', 'Upside por tonelada'],
], cw=[AV*0.06, AV*0.34, AV*0.32, AV*0.28]))
s.append(sp(2))
s.append(h2('Como as receitas entram no tempo'))
s.append(body('As sete receitas não nascem juntas — e o desenho da rampa importa para quem avalia risco. No primeiro ano de operação, a planta vive de gate fee, assinaturas e primeiros contratos B2B: receitas contratuais, previsíveis, suficientes para o ponto de equilíbrio operacional. No segundo ano entram em regime os produtos — composto com marca, mobiliário vendido a terceiros — e os primeiros certificados de reciclagem emitidos em volume. Do terceiro ano em diante, o projeto de carbono certificado começa a liquidar créditos acumulados, e o selo B2B vira linha de licenciamento regional.'))
s.append(body('Essa arquitetura tem uma propriedade que os financiadores enxergam de longe: nenhuma receita isolada representa mais de um terço do total em regime. Um contrato municipal renegociado, uma safra fraca de composto ou um ciclo de preço baixo de carbono machucam — mas não derrubam. Compare com o aterro, que vive de uma única linha: se o contrato público espirra, o negócio inteiro pega pneumonia.'))
s.append(h2('O contrato âncora por dentro'))
s.append(body('Vale abrir o contrato municipal, porque é nele que o modelo ganha ou perde credibilidade. Quatro cláusulas o definem. O <b>gate fee</b>, fixado abaixo do custo de disposição vigente — a economia do município é imediata e mensurável. A <b>contrapartida</b>, expressa em valor ou em unidades de mobiliário por trimestre, com cronograma físico anexo — é ela que transforma contrato em política pública visível. Os <b>indicadores de desempenho</b>: percentual de desvio de aterro, taxa de contaminação da coleta, prazo de retirada — números publicados mensalmente em painel aberto. E a <b>transparência</b>: o mesmo sistema que rastreia a tonelada para o crédito alimenta o portal público; o cidadão vê quantas toneladas a cidade desviou e o que elas viraram.'))
s.append(sp(2))
s += qt('Uma tonelada, sete receitas. É por isso que o CIRO cobra menos que o aterro e ainda devolve mobiliário: o aterro tem uma linha de receita. Nós temos sete.')
s.append(resumo([
 'A âncora é o gate fee municipal — sempre menor que o custo atual de aterro',
 'A rampa: contratuais no ano 1, produtos no ano 2, créditos em regime no ano 3',
 'Nenhuma receita passa de um terço do total — o risco é pulverizado por desenho',
 'O contrato âncora publica seus próprios números: transparência é cláusula, não promessa',
]))
s.append(sp(2))
s.append(exercicio('Estime o potencial das 7 receitas na sua cidade', [
 'Multiplique as toneladas/ano do seu município por um gate fee 15% menor que o atual — a economia é o argumento do contrato.',
 'Estime os assinantes potenciais: 3% dos domicílios dos bairros A/B é uma premissa conservadora.',
 'Liste os 10 maiores geradores privados da cidade (hotéis, mercados, restaurantes) — são os primeiros contratos B2B.',
]))
s.append(PageBreak())

# ══════════ INTERLÚDIO 2 ══════════════════════════════════════════
s += interlude('Uma tonelada.<br/>Sete receitas.', 'Capítulo 6 · O empilhamento que muda a matemática')

# ══════════ CAPÍTULO 7 ════════════════════════════════════════════
s += cap_opener(7, 'O Dinheiro Existe', 'O que falta ao Brasil não é dinheiro verde. É projeto estruturado para recebê-lo.')
s += [sp(4), lb('Capítulo 7'), gl(), sp(3)]
s.append(h1('O Dinheiro Existe'))
s.append(Paragraph('O mapa dos créditos verdes federais', S('sub7',fontName='Helvetica-Oblique',fontSize=11,textColor=LGRAY,spaceAfter=8)))
s.append(sp(2))
s.append(body('A objeção número um de todo gestor — "não há orçamento para isso" — morre neste capítulo. O CAPEX do CIRO não sai do cofre municipal: sai de um conjunto de instrumentos federais desenhados exatamente para financiar economia circular, e que estão, neste momento, com recursos disponíveis e demanda menor do que a oferta. O que falta ao Brasil não é dinheiro verde. É projeto estruturado para recebê-lo.'))
s.append(h2('Fundo Clima — BNDES: o pilar do financiamento'))
s.append(body('O Fundo Nacional sobre Mudança do Clima, operado pelo BNDES, é o principal instrumento de financiamento climático do país, com dezenas de bilhões em disponibilidade e um subprograma específico para resíduos sólidos — tratamento, sistemas biológicos, reciclagem e biogás. As condições não existem em nenhum banco comercial: juros de 1% a 8% ao ano conforme a linha, prazo de até 16 anos e até 8 de carência, com teto de R$ 30 milhões por beneficiário a cada 12 meses.'))
s.append(body('Importante: quem toma esse financiamento é a empresa do projeto — não a prefeitura. O risco de implantação é integralmente privado. E o precedente já existe: o Fundo Clima realizou seu primeiro aporte em gestão de resíduos sólidos urbanos em 2025, declarando o setor prioridade para os compromissos climáticos brasileiros.'))
s.append(h2('Finep — subvenção para a camada de inovação'))
s.append(body('A Finep mantém chamadas públicas de economia circular com componente de subvenção — dinheiro não reembolsável — para projetos com risco tecnológico desenvolvidos em parceria com instituições de ciência e tecnologia. A chamada vigente de Economia Circular e Cidades Sustentáveis soma R$ 150 milhões, com projetos entre R$ 5 e 20 milhões. No CIRO, a camada financiável é real: compostagem acelerada com monitoramento inteligente, formulação de madeira plástica e a plataforma de rastreabilidade que transforma cada tonelada em crédito auditável.'))
s.append(h2('Novo PAC Seleções — o recurso que a prefeitura capta'))
s.append(body('O eixo de resíduos sólidos do Novo PAC já contratou cerca de R$ 1 bilhão com mais de 500 municípios, financiando exatamente a ponta que o município precisa: ecopontos, galpões de triagem, caminhões e infraestrutura de coleta. Quem apresenta a proposta é a prefeitura ou o consórcio — e aqui está a divisão de trabalho do ecossistema: nós estruturamos tecnicamente a proposta; o município capta; a infraestrutura pública nasce ao lado da planta privada. As seleções são recorrentes; município com projeto pronto na gaveta entra no primeiro ciclo que abrir.'))
s.append(h2('FNMA e editais do MMA — a ponta comunitária'))
s.append(body('O Fundo Nacional do Meio Ambiente publica editais recorrentes de compostagem e agricultura urbana — apoios não reembolsáveis que financiam módulos comunitários, educação ambiental e hortas ligadas às escolas. São valores menores, mas com papel estratégico: financiam justamente o programa social que prepara a população para segregar corretamente — e que enche de sentido as carteiras entregues às escolas.'))
s.append(sp(2))
s.append(tabela([
 ['Instrumento', 'Tipo', 'Ordem de valor', 'Quem acessa'],
 ['Fundo Clima / BNDES', 'Financiamento subsidiado', 'até R$ 30 M/ano por beneficiário', 'Empresa do projeto'],
 ['Finep Economia Circular', 'Crédito + subvenção', 'R$ 5 a 20 M por projeto', 'Empresa + ICT'],
 ['Novo PAC Seleções', 'Repasse federal', 'conforme proposta', 'Prefeitura / consórcio'],
 ['FNMA / editais MMA', 'Não reembolsável', 'R$ 1 a 10 M por edital', 'Município / consórcio / OSC'],
 ['CCRLR + carbono', 'Receita recorrente', 'por tonelada', 'Operador da planta'],
], cw=[AV*0.26, AV*0.24, AV*0.28, AV*0.22]))
s.append(sp(2))
s.append(h2('A arquitetura híbrida de R$ 10 milhões'))
s.append(body('O plano de capital do CIRO combina as fontes num desenho em que cada uma paga o que sabe pagar: a Finep paga a inovação (R$ 5 milhões com subvenção), o Fundo Clima paga a planta (R$ 4 milhões em 16 anos), o FNMA paga a ponta comunitária (R$ 1 milhão), o PAC paga a infraestrutura municipal via prefeitura — e os créditos de reciclagem e carbono pagam o serviço da dívida. O município entra com o que não lhe custa caixa: o contrato, a área e a articulação regional.'))
s.append(h2('Como o banco lê o projeto'))
s.append(body('Entender a cabeça do analista de crédito economiza um ano de idas e vindas. O banco de fomento não olha primeiro para a tecnologia — olha para o <b>recebível</b>. Um contrato municipal de gate fee com prazo firme é, para o BNDES, o que o aluguel é para o financiamento imobiliário: a fonte previsível que paga a parcela. Sobre ele, o analista calcula a cobertura do serviço da dívida e pergunta três coisas: o contrato sobrevive à troca de prefeito? (Sim — contrato administrativo formalizado não se extingue com o mandato.) A operadora tem quem saiba operar? (É o papel da Ecogrupo na sociedade.) E se tudo der errado, o que o banco executa? (Máquinas, recebíveis e as garantias da holding.)'))
s.append(body('É por isso que a ordem dos degraus do Capítulo 8 não é estética: contrato antes de financiamento, sempre. Quem pede o dinheiro antes de ancorar o recebível ouve o "não" mais educado do sistema financeiro — o pedido de mais documentos, para sempre.'))
s.append(h2('Os cinco erros que derrubam propostas'))
s.append(body('A experiência dos editais mostra que as propostas não morrem por falta de mérito — morrem por erro de montagem. <b>Erro um:</b> pedir à fonte errada — subvenção para obra civil, banco para pesquisa. <b>Erro dois:</b> CAUC com pendência ou plano de resíduos vencido — elimina o município na triagem automática. <b>Erro três:</b> proposta Finep sem instituição de ciência e tecnologia de verdade no projeto — parceria de fachada é detectada e desclassificada. <b>Erro quatro:</b> cronograma de desembolso incompatível com licenciamento — pedir dinheiro para uma planta cuja licença sai depois do prazo do edital. <b>Erro cinco:</b> conta que só fecha com o crédito de carbono no preço otimista — analista vê e devolve; o crédito é upside, nunca premissa.'))
s.append(sp(2))
s += qt('O que falta ao Brasil não é dinheiro verde. É projeto estruturado para recebê-lo. Esta é exatamente a lacuna que o Zion Ecosystem preenche — para a planta e para o município ao mesmo tempo.')
s.append(resumo([
 'Cada fonte paga o que sabe pagar: Finep a inovação, Fundo Clima a planta, PAC a ponta pública',
 'O banco lê o recebível antes da tecnologia — contrato municipal é a garantia-mãe',
 'Contrato antes de financiamento, sempre — a ordem dos degraus não é estética',
 'Créditos de carbono no caso-base são o erro que devolve propostas: trate como upside',
]))
s.append(sp(2))
s.append(exercicio('Prepare o município para captar', [
 'Regularize as certidões do município — CAUC limpo é pré-requisito de qualquer repasse federal.',
 'Atualize o Plano Municipal de Resíduos — ele é critério de prioridade em quase todos os editais.',
 'Cadastre a equipe no sistema de transferências do governo federal e monitore os ciclos do PAC Seleções e do FNMA.',
]))
s.append(PageBreak())

# ══════════ INTERLÚDIO 2B ═════════════════════════════════════════
s += interlude('Cada fonte paga<br/>o que sabe pagar.', 'Capítulo 7 · A regra de ouro do blended finance')

# ══════════ CAPÍTULO 8 ════════════════════════════════════════════
s += cap_opener(8, 'A Cidade Circular', 'Oito degraus. O primeiro custa zero. O último tem placa de inauguração.')
s += [sp(4), lb('Capítulo 8'), gl(), sp(3)]
s.append(h1('A Cidade Circular'))
s.append(Paragraph('A escada de implantação, degrau por degrau', S('sub8',fontName='Helvetica-Oblique',fontSize=11,textColor=LGRAY,spaceAfter=8)))
s.append(sp(2))
s.append(body('Tudo que este volume apresentou converge para uma escada de oito degraus. Ela foi desenhada com uma lógica de compromisso crescente: cada degrau é pequeno o bastante para ser subido sem medo, e sólido o bastante para sustentar o próximo. Nenhum degrau exige que o município aposte antes de ver.'))
s.append(h2('Degraus 1 e 2 — A conversa técnica e a decisão política'))
s.append(body('Tudo começa pelo secretário — de Meio Ambiente, Obras ou Fazenda — que valida tecnicamente o modelo e leva o tema ao prefeito com os números da cidade na mão. A apresentação ao prefeito não pede assinatura de contrato: pede vinte minutos e uma decisão de custo zero. A experiência mostra que a ordem importa: prefeito convencido antes do secretário vira projeto órfão na primeira crise de agenda.'))
s.append(h2('Degrau 3 — O protocolo de intenções'))
s.append(body('Uma página. Sem custo, sem exclusividade, sem obrigação financeira, sem licitação — porque não contrata nada: apenas autoriza o início dos estudos e a troca de dados. É o documento que destrava tudo, e o único objetivo da primeira reunião. Qualquer proposta que peça mais do que isso na primeira conversa deve gerar desconfiança — a nossa pede exatamente isso.'))
s.append(h2('Degrau 4 — O Diagnóstico Circular'))
s.append(body('Em 30 dias, o município recebe gratuitamente o estudo com seus números reais: quanto gera, quanto paga, quanto pode economizar, quantas praças e salas de aula o resíduo pode virar por ano, e qual o desenho ideal — planta própria, consórcio ou hub regional. É com esse documento que o prefeito decide — e é ele que vira anexo técnico do contrato e das propostas de captação.'))
s.append(h2('Degraus 5 e 6 — Contrato e área'))
s.append(body('O contrato de prestação de serviços fixa o gate fee abaixo do custo atual de aterro e a contrapartida em mobiliário com marcos trimestrais. A procuradoria escolhe o instrumento — dispensa por valor, credenciamento, licitação ou PPP simplificada; levamos as minutas dos quatro caminhos. Em paralelo, o município âncora cede a área da planta, transformando terreno ocioso em polo industrial verde. Com contrato e área, o financiamento federal da planta é protocolado.'))
s.append(h2('Degraus 7 e 8 — Captação conjunta e replicação'))
s.append(body('Com a planta contratada, município e operador captam juntos no PAC Seleções a infraestrutura da ponta pública. E então vem o degrau que transforma projeto em movimento: a primeira inauguração. A praça mobiliada com o resíduo da própria cidade é o case que nenhum release compra — e é ela que leva o modelo ao município vizinho. Prefeito convence prefeito; o consórcio nasce da inveja boa entre gabinetes.'))
s.append(sp(2))
s.append(tabela([
 ['Degrau', 'Ação', 'Custo p/ município'],
 ['1', 'Reunião técnica com o secretário', 'Zero'],
 ['2', 'Apresentação ao prefeito (20 min)', 'Zero'],
 ['3', 'Protocolo de intenções — 1 página', 'Zero'],
 ['4', 'Diagnóstico Circular em 30 dias', 'Zero — cortesia Zion Ecosystem'],
 ['5', 'Contrato com gate fee menor que o aterro', 'Economia desde o 1º mês'],
 ['6', 'Cessão de área para a planta', 'Terreno ocioso vira polo verde'],
 ['7', 'Captação PAC para infra da ponta', 'Recurso federal a fundo perdido'],
 ['8', 'Inauguração e replicação regional', 'O case político do mandato'],
], cw=[AV*0.12, AV*0.52, AV*0.36]))
s.append(sp(2))
s.append(h2('O papel do empreendedor local'))
s.append(body('A escada tem um degrau paralelo que não depende da prefeitura: o empreendedor da região pode ancorar a coleta B2B, operar a logística sob contrato, investir na SPE local ou candidatar-se à operação franqueada do modelo em seu território. O Zion Ecosystem foi desenhado como plataforma — a planta é local, a marca, o método e a engenharia de captação são de rede.'))
s.append(h2('O consórcio intermunicipal na prática'))
s.append(body('Para cidades abaixo de 50 mil habitantes, a escala vem da soma. Seis municípios de 25 mil habitantes geram, juntos, o volume de um de 150 mil — e a lei de consórcios públicos dá a eles personalidade jurídica própria para contratar, licenciar e captar como um único ente. A governança é conhecida: assembleia de prefeitos, contrato de rateio proporcional à tonelada entregue, e um único contrato de programa com a planta. Para o PAC e para os editais, o consórcio pontua mais que o município isolado — a regionalização é política federal declarada. E há um efeito colateral político elegante: o prefeito que articula o consórcio vira, naturalmente, o líder regional do tema.'))
s.append(h2('Comunicação: o projeto que a cidade entende'))
s.append(body('Um erro recorrente em projetos ambientais é falar de tecnologia quando a população quer saber de vida cotidiana. A comunicação da cidade circular tem três regras. Primeira: o programa tem nome e identidade próprios — as pessoas aderem a um movimento, não a um contrato administrativo. Segunda: os marcos são físicos e trimestrais — a cada estação, uma entrega com foto: a praça, as carteiras, o ecoponto, o painel de toneladas. Terceira: as escolas são o coração do programa — a criança que aprende a separar em sala leva o hábito para casa com mais eficácia que qualquer campanha; e a carteira nova em que ela senta, feita do resíduo da própria cidade, é a aula de economia circular que nenhum livro dá.'))
s.append(sp(2))
s += qt('O custo de subir o primeiro degrau é zero. O custo de não subir são mais quatro anos pagando o aterro — sem nada para inaugurar. Entre esses dois números, não existe empate.')
s.append(resumo([
 'Oito degraus de compromisso crescente — quatro deles de custo zero para o município',
 'A única meta da primeira reunião é o protocolo; o contrato vem como consequência',
 'Consórcio soma volume, pontua mais nos editais e cria o líder regional do tema',
 'Comunicação: nome próprio, marcos trimestrais com foto e escolas no centro',
]))
s.append(sp(2))
s.append(exercicio('Suba o primeiro degrau esta semana', [
 'Gestor: agende a reunião técnica e peça o Diagnóstico Circular — o protocolo de 1 página vai anexo a este volume.',
 'Empreendedor: mapeie os geradores B2B da sua cidade e escreva para a Zion com o perfil do seu território.',
 'Ambos: façam a conta do Capítulo 1. É ela que transforma esta leitura em pauta de reunião.',
]))
s.append(PageBreak())

# ══════════ INTERLÚDIO 3 ══════════════════════════════════════════
s += interlude('A praça inaugurada com o lixo<br/>da própria cidade<br/>é o case que nenhum release compra.', 'Capítulo 8 · O degrau que transforma projeto em movimento')

# ══════════ ESTUDO DE CASO ════════════════════════════════════════
s += [sp(4), lb('Estudo de caso ilustrativo'), gl(), sp(3)]
s.append(h1('Cidade Modelo, 100 Mil Habitantes'))
s.append(Paragraph('O volume inteiro aplicado a um município fictício — com todas as contas abertas', S('subec',fontName='Helvetica-Oblique',fontSize=11,textColor=LGRAY,spaceAfter=8)))
s.append(sp(2))
s.append(body('Para amarrar todos os capítulos, vamos aplicar o modelo completo a uma cidade fictícia — Cidade Modelo, 100 mil habitantes, interior do Sul do Brasil. Os números são ilustrativos e conservadores; o Diagnóstico Circular substitui cada um deles pelos dados reais do seu município.'))
s.append(h2('O ponto de partida'))
s.append(tabela([
 ['Indicador', 'Cidade Modelo — hoje'],
 ['Geração de resíduo', '45 t/dia · 16.400 t/ano'],
 ['Destino', 'Aterro privado a 60 km'],
 ['Custo de disposição', 'R$ 150/t · R$ 2,46 mi/ano'],
 ['Logística própria', '≈ R$ 800 mil/ano'],
 ['Coleta seletiva', 'Cooperativa com 18 catadores, recupera < 3% da massa'],
 ['Situação legal', 'Plano de resíduos desatualizado desde 2019'],
], cw=[AV*0.42, AV*0.58]))
s.append(sp(2))
s.append(h2('O contrato assinado'))
s.append(body('Após protocolo e diagnóstico, a Cidade Modelo assina o contrato âncora: gate fee de R$ 128 por tonelada — 15% abaixo do custo atual — para as frações orgânica e reciclável, mantendo o contrato de aterro apenas para o rejeito. Com 70% da massa desviada à planta a partir do segundo ano, a conta municipal cai de R$ 2,46 milhões para cerca de R$ 2,15 milhões — uma economia direta de mais de R$ 300 mil por ano, antes de contar a redução da logística (a planta fica a 8 km, não a 60).'))
s.append(body('A contrapartida contratual: 4% do faturamento do contrato convertido em mobiliário ao ano. Na prática, isso significa por ano: uma praça completa remobiliada (24 bancos e 12 lixeiras), 300 carteiras escolares e um cronograma de entrega trimestral — quatro inaugurações anuais até o fim do mandato.'))
s.append(h2('A rampa da planta'))
s.append(tabela([
 ['Linha de resultado (planta)', 'Ano 1', 'Ano 2', 'Ano 3'],
 ['Gate fee municipal', 'R$ 0,9 mi', 'R$ 1,5 mi', 'R$ 1,5 mi'],
 ['Assinaturas + B2B + selo', 'R$ 0,3 mi', 'R$ 0,7 mi', 'R$ 1,0 mi'],
 ['Composto + mobiliário (vendas)', 'R$ 0,2 mi', 'R$ 0,8 mi', 'R$ 1,2 mi'],
 ['Créditos (CCRLR; carbono como upside)', '—', 'R$ 0,3 mi', 'R$ 0,6 mi'],
 ['Receita total', 'R$ 1,4 mi', 'R$ 3,3 mi', 'R$ 4,3 mi'],
], cw=[AV*0.43, AV*0.19, AV*0.19, AV*0.19]))
s.append(sp(2))
s.append(body('Com OPEX em regime na casa de R$ 2,4 milhões anuais, a planta cruza o ponto de equilíbrio no segundo ano e entrega margem operacional acima de 35% no terceiro — dentro da faixa que o benchmark setorial valida, e sem colocar o crédito de carbono no caso-base. O serviço da dívida do Fundo Clima, com oito anos de carência, começa a pesar somente quando a operação já está madura.'))
s.append(h2('O que a cidade colhe em quatro anos'))
s.append(caixa_gold('CIDADE MODELO — O SALDO DO MANDATO', [
 'R$ 1,2 milhão a menos gastos com disposição ao longo do ciclo',
 '16 inaugurações trimestrais: 4 praças, 1.200 carteiras, ecopontos e painel público',
 '≈ 35 empregos diretos + cooperativa formalizada com renda previsível',
 'Mais de 30 mil toneladas desviadas do aterro — e o título estadual de cidade pioneira',
 'O consórcio regional em formação, com a Cidade Modelo na presidência',
]))
s.append(sp(2))
s += qt('Nenhum número deste caso exige heroísmo: gate fee 15% menor, desvio de 70%, margem dentro do benchmark. A força do modelo não está em nenhuma premissa ousada — está na arquitetura que empilha receitas modestas sobre um custo que já existia.')
s.append(PageBreak())

# ══════════ A PLATAFORMA ══════════════════════════════════════════
s += [sp(4), lb('A plataforma'), gl(), sp(3)]
s.append(h1('O Zion Ecosystem em Cinco Camadas'))
s.append(sp(2))
s.append(body('O CIRO é a peça industrial — mas o que se replica de cidade em cidade é a plataforma completa. Cinco camadas, cada uma com dono claro, encaixadas para que o município nunca dependa de improviso:'))
s.append(sp(3))
camadas = [
 ('1 · CAPTAÇÃO DE RESÍDUO', 'A logística das três portas de entrada: contrato municipal, assinaturas residenciais e coleta B2B. Operada pela Ecogrupo, com roteirização e rastreio por carga.'),
 ('2 · INDUSTRIALIZAÇÃO', 'A planta CIRO com as duas linhas — orgânicos e madeira plástica — e a camada digital de rastreabilidade que transforma tonelada em dado auditável.'),
 ('3 · PRODUTOS', 'Composto com marca, mobiliário urbano e escolar, fardos de recicláveis e CDR. Cada produto com contrato de destino antes de a planta abrir.'),
 ('4 · CRÉDITOS AMBIENTAIS', 'A emissão e a comercialização de CCRLR e créditos de carbono — a receita invisível que remunera a operação e paga a dívida.'),
 ('5 · MARCA E EXPANSÃO', 'O selo Resíduo Zero, a relação institucional com prefeituras e consórcios, a engenharia de captação e o playbook que leva o modelo à próxima cidade. Esta camada é a Zion.'),
]
for nn, d in camadas:
    row = Table([
        [Paragraph(nn, S('cam1',fontName='Helvetica-Bold',fontSize=8,textColor=GOLD,spaceAfter=0))],
        [Paragraph(d, S('cam2',fontSize=9.5,textColor=GRAY,leading=14,spaceAfter=0,alignment=TA_JUSTIFY))],
    ], colWidths=[AV])
    row.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('LINEBEFORE',(0,0),(0,-1),2,GOLD),
        ('LINEBELOW',(0,-1),(-1,-1),0.3,colors.HexColor('#EEEEEE'))]))
    s.append(row); s.append(sp(1))
s.append(sp(3))
s.append(body('A divisão societária espelha as camadas: a Ecogrupo responde pela engenharia e pela operação industrial; a Zion, pela estruturação, captação, marca e relação institucional. O município âncora entra com contrato, área e articulação regional — os ativos que não lhe custam caixa. E o empreendedor local encontra espaço nas camadas 1, 3 e 5: logística, distribuição de produtos e operação franqueada do território.'))
s.append(sp(2))
s.append(hl_box('A planta é local. A marca, o método e a engenharia de captação são de rede. É essa divisão que faz a segunda cidade custar metade do esforço da primeira.'))
s.append(PageBreak())

# ══════════ OS 10 PRINCÍPIOS ══════════════════════════════════════
s += [sp(4), lb('Os princípios'), gl(), sp(3)]
s.append(h1('O Decálogo da Cidade Circular'))
s.append(sp(2))
s.append(body('Dez princípios que resumem a filosofia operacional deste volume. Servem de teste rápido para qualquer decisão do programa: se uma proposta viola um deles, ela precisa de uma justificativa muito boa — ou de uma recusa rápida.'))
s.append(sp(3))
principios = [
 ('I', 'O resíduo pertence à cidade. Todo valor extraído dele deve deixar rastro visível no território que o gerou.'),
 ('II', 'Nenhum compromisso antes do diagnóstico. Nenhum diagnóstico sem dados reais.'),
 ('III', 'O primeiro degrau de qualquer parceria séria custa zero para o município.'),
 ('IV', 'Quem compra o que sai define se o projeto é economia ou paisagismo.'),
 ('V', 'A fração orgânica decide o jogo: metade da massa, o maior passivo, o maior crédito.'),
 ('VI', 'Crédito ambiental é upside, nunca premissa. Se a conta só fecha com ele, a conta não fecha.'),
 ('VII', 'Catadores se integram, não se substituem. O sistema formal absorve quem já fazia o trabalho.'),
 ('VIII', 'Cada fonte paga o que sabe pagar: subvenção à inovação, banco à planta, repasse à ponta pública.'),
 ('IX', 'Transparência é cláusula: o painel de toneladas é público, mensal e auditável.'),
 ('X', 'A inauguração é o produto político. Um marco físico por trimestre, até o fim do mandato.'),
]
for num, txt in principios:
    row = Table([
        [Paragraph(num, S('dn',fontName='Helvetica-Bold',fontSize=13,textColor=GOLD,alignment=TA_CENTER,spaceAfter=0)),
         Paragraph(txt, S('dt',fontSize=10,textColor=DARK,leading=15,spaceAfter=0))],
    ], colWidths=[16*mm, AV-16*mm])
    row.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LINEBELOW',(0,-1),(-1,-1),0.3,colors.HexColor('#EEEEEE'))]))
    s.append(row)
s.append(PageBreak())

# ══════════ FERRAMENTAS ═══════════════════════════════════════════
s += [sp(4), lb('Ferramentas · 1 de 3'), gl(), sp(3)]
s.append(h1('Checklist do Gestor Municipal'))
s.append(sp(2))
s.append(body('Antes de qualquer reunião sobre o tema, tenha estas respostas na mão. Elas transformam uma conversa de intenções em uma reunião de decisão.'))
s.append(sp(2))
s.append(caixa_gold('DADOS — A FOTOGRAFIA DA SUA CIDADE', [
 'Toneladas/dia coletadas e destino atual (aterro? lixão? distância?)',
 'Custo por tonelada de disposição e valor anual total do manejo',
 'Situação do Plano Municipal de Resíduos (existe? atualizado?)',
 'Situação de CAUC e certidões para repasses federais',
 'Cooperativas de catadores ativas e número de cooperados',
]))
s.append(sp(3))
s.append(caixa_gold('DECISÕES — O QUE SÓ O MUNICÍPIO PODE FAZER', [
 'Assinar o protocolo de intenções (custo zero)',
 'Indicar a área candidata para a planta',
 'Definir o instrumento jurídico com a procuradoria',
 'Priorizar resíduos no próximo ciclo do PAC Seleções',
 'Articular municípios vizinhos para o consórcio',
]))
s.append(sp(3))
s.append(caixa_gold('SINAIS DE ALERTA — O QUE DEVE GERAR DESCONFIANÇA', [
 'Projetos que pedem investimento municipal antes de qualquer entrega',
 'Tecnologias que prometem eliminar 100% do lixo sem comprador para as saídas',
 'Contratos longos com exclusividade antes de diagnóstico com dados reais',
 'Propostas sem resposta clara para a pergunta: quem compra o que sai?',
]))
s.append(PageBreak())

s += [sp(4), lb('Ferramentas · 2 de 3'), gl(), sp(3)]
s.append(h1('Matriz de Fontes de Recursos'))
s.append(sp(2))
s.append(body('A visão consolidada de onde vem cada real do modelo — para colar na parede da secretaria.'))
s.append(sp(2))
s.append(tabela([
 ['Fonte', 'Financia o quê', 'Quem pede', 'Natureza'],
 ['Fundo Clima / BNDES', 'A planta industrial (CIRO)', 'Empresa do projeto', 'Empréstimo 16 anos, juro subsidiado'],
 ['Finep Econ. Circular', 'Tecnologia e inovação', 'Empresa + ICT', 'Crédito + subvenção'],
 ['Novo PAC Seleções', 'Ecopontos, caminhões, galpões', 'Prefeitura / consórcio', 'Repasse federal'],
 ['FNMA / MMA', 'Compostagem comunitária, educação', 'Município / consórcio', 'Não reembolsável'],
 ['CCRLR', 'Fluxo de caixa da operação', 'Operador', 'Receita por tonelada reciclada'],
 ['Crédito de carbono', 'Upside da operação', 'Operador', 'Receita por metano evitado'],
 ['Fundo Socioamb. Caixa', 'Projetos socioambientais', 'Município / OSC', 'Apoio a fundo perdido'],
], cw=[AV*0.24, AV*0.30, AV*0.22, AV*0.24]))
s.append(sp(3))
s.append(hl_box('Regra de ouro da captação: cada fonte paga o que sabe pagar. Misturar os papéis — pedir ao banco o que é da subvenção, ou à prefeitura o que é do banco — é a receita da proposta negada.'))
s.append(PageBreak())

s += [sp(4), lb('Ferramentas · extra'), gl(), sp(3)]
s.append(h1('Os 90 Dias do Secretário'))
s.append(sp(2))
s.append(body('Para o secretário que quer liderar o tema sem esperar decisão de cima: o roteiro de um trimestre, com entregas quinzenais que preparam o município para qualquer caminho — este modelo ou outro. Nada aqui exige orçamento novo; tudo gera valor mesmo que o projeto não avance.'))
s.append(sp(3))
s.append(tabela([
 ['Quinzena', 'Entrega', 'Por que importa'],
 ['1ª', 'A conta real: toneladas, custos, contratos e vencimentos', 'Sem esse número, toda conversa é opinião'],
 ['2ª', 'Fotografia legal: plano de resíduos, CAUC, licenças, TACs', 'É a triagem de qualquer edital federal'],
 ['3ª', 'Mapa de atores: cooperativas, grandes geradores, municípios vizinhos', 'Catadores e consórcio são pontos de bônus em tudo'],
 ['4ª', 'Inventário de áreas públicas candidatas à planta', 'A área é a contrapartida clássica do município âncora'],
 ['5ª', 'Pauta de 20 minutos no secretariado + protocolo apresentado', 'Transforma diagnóstico em decisão de custo zero'],
 ['6ª', 'Dossiê de captação iniciado (Anexo D) + calendário de editais', 'Dossiê pronto antes do edital, não por causa dele'],
], cw=[AV*0.12, AV*0.46, AV*0.42]))
s.append(sp(3))
s.append(hl_box('Em 90 dias, o secretário sai de "responsável pela coleta" para "autor do projeto que o prefeito vai inaugurar". A diferença entre os dois cargos é este roteiro.'))
s.append(PageBreak())

s += [sp(4), lb('Ferramentas · 3 de 3'), gl(), sp(3)]
s.append(h1('Glossário da Cidade Circular'))
s.append(sp(2))
gloss = [
 ('Gate fee', 'Tarifa paga por tonelada entregue a uma instalação de tratamento ou disposição.'),
 ('CIRO', 'Centro de Industrialização de Resíduos Orgânicos — a planta modular do Zion Ecosystem.'),
 ('Ecoparque', 'Complexo industrial de valorização de resíduos em torno de um aterro (modelo Orizon).'),
 ('CCRLR', 'Certificado de Crédito de Reciclagem de Logística Reversa (Decreto 11.413/2023).'),
 ('SBCE', 'Sistema Brasileiro de Comércio de Emissões — mercado regulado de carbono (Lei 15.042/2024).'),
 ('CRVE', 'Certificado de Redução ou Remoção Verificada de Emissões — o crédito de carbono brasileiro.'),
 ('CDR', 'Combustível Derivado de Resíduo — fração não reciclável usada como energia industrial.'),
 ('Madeira plástica', 'Perfil estrutural extrusado de plástico reciclado; imune a cupim e intempéries.'),
 ('Compostagem acelerada', 'Processo aeróbio controlado que converte orgânicos em composto em semanas.'),
 ('Biodigestor', 'Reator anaeróbio que converte orgânicos em biogás e biofertilizante.'),
 ('Biometano', 'Biogás purificado a padrão veicular/rede — substitui diesel e GNV.'),
 ('Gate político', 'A contrapartida visível: mobiliário público entregue com marcos trimestrais.'),
 ('PNRS', 'Política Nacional de Resíduos Sólidos (Lei 12.305/2010).'),
 ('Blended finance', 'Arquitetura que combina subvenção, crédito subsidiado e capital privado no mesmo projeto.'),
 ('TAC', 'Termo de Ajustamento de Conduta — instrumento do MP para passivos ambientais.'),
 ('SPE', 'Sociedade de Propósito Específico — a empresa criada exclusivamente para o projeto.'),
]
for t, d in gloss:
    s.append(Paragraph(f'<b><font color="#1A1A1A">{t}</font></b> — {d}', ST['bullet']))
s.append(PageBreak())

# ══════════ BENCHMARK ═════════════════════════════════════════════
s += [sp(4), lb('Benchmark'), gl(), sp(3)]
s.append(h1('Números de Referência do Setor'))
s.append(sp(2))
s.append(body('Os números que sustentam as premissas deste volume — para citar em reunião, ofício e proposta. Valores de mercado verificáveis em fontes públicas; condições de editais devem sempre ser confirmadas nos instrumentos convocatórios vigentes.'))
s.append(sp(2))
s.append(tabela([
 ['Indicador', 'Valor de referência', 'Fonte'],
 ['Geração per capita de RSU no Brasil', '≈ 0,95 kg/hab/dia', 'Panoramas setoriais (Abrema/SNIS)'],
 ['Fração orgânica do RSU', '≈ 45–55% da massa', 'Panoramas setoriais'],
 ['Custo de disposição em aterro', 'R$ 80 a 200/t', 'Contratos municipais típicos'],
 ['Gate fee médio — player listado', 'R$ 84,80/t', 'Orizon (ORVR3), resultados 2025'],
 ['Margem EBITDA — valorização de resíduos', '≈ 48%', 'Orizon (ORVR3), resultados 2025'],
 ['Potencial do metano vs. CO2', '≈ 28×', 'IPCC'],
 ['Fundo Clima — juros', '1% a 8% a.a.', 'BNDES'],
 ['Fundo Clima — prazo', 'até 16 anos, 8 de carência', 'BNDES'],
 ['Fundo Clima — teto por beneficiário', 'R$ 30 M / 12 meses', 'BNDES'],
 ['Finep Economia Circular — faixa', 'R$ 5 a 20 M por projeto', 'Chamada pública Finep'],
 ['Novo PAC — carteira de resíduos', '≈ R$ 1 bi · 543 municípios', 'Ministério das Cidades'],
 ['Créditos de carbono — case', '750 mil comprados pelo Google', 'Operação Orizon, 2024'],
], cw=[AV*0.42, AV*0.30, AV*0.28]))
s.append(sp(3))
s.append(hl_box('Regra do caso-base Zion: créditos de carbono são upside, nunca premissa de fechamento. Se a conta só fecha com o crédito, a conta não fecha.'))
s.append(PageBreak())

# ══════════ BENCHMARK 2 — CAPEX DO CIRO ═══════════════════════════
s += [sp(4), lb('Benchmark · caso-base'), gl(), sp(3)]
s.append(h1('As Contas do CIRO — CAPEX e Premissas'))
s.append(sp(2))
s.append(body('A abertura do investimento de referência da planta-piloto e as premissas conservadoras do caso-base. É esta a estrutura submetida às fontes de financiamento do Capítulo 7.'))
s.append(sp(2))
s.append(tabela([
 ['Bloco de investimento', 'Valor', 'Fonte primária'],
 ['Compostagem acelerada + biodigestor', 'R$ 3,8 mi', 'Fundo Clima'],
 ['Linha de madeira plástica (trituração, extrusora, moldes)', 'R$ 2,4 mi', 'Fundo Clima + Finep'],
 ['Logística de coleta (caminhões, baldes, ecopontos)', 'R$ 1,4 mi', 'Fundo Clima / PAC (ponta pública)'],
 ['Tecnologia, rastreabilidade e P&D', 'R$ 1,0 mi', 'Finep (subvenção)'],
 ['Licenciamento, certificações e habilitações', 'R$ 0,5 mi', 'Recursos próprios'],
 ['Capital de giro (12 meses)', 'R$ 0,9 mi', 'Recursos próprios / Finep'],
 ['Total', 'R$ 10,0 mi', 'Arquitetura híbrida'],
], cw=[AV*0.48, AV*0.17, AV*0.35]))
s.append(sp(3))
s.append(caixa_gold('PREMISSAS CONSERVADORAS DO CASO-BASE', [
 'Gate fee 15% abaixo do custo de aterro da cidade âncora',
 'Desvio de 70% da massa contratada a partir do ano 2',
 'Contaminação da coleta abaixo de 15% após o piloto educacional',
 'Créditos de carbono fora do caso-base — tratados 100% como upside',
 'Ponto de equilíbrio operacional no ano 2; margem em regime > 35% no ano 3',
 'Carência de 8 anos no financiamento-mãe: a dívida amadurece junto com a operação',
]))
s.append(PageBreak())

# ══════════ ANEXO A — MINUTA DO PROTOCOLO ═════════════════════════
s += [sp(4), lb('Anexo A'), gl(), sp(3)]
s.append(h1('Minuta — Protocolo de Intenções'))
s.append(sp(2))
s.append(body('A minuta abaixo é o primeiro degrau da escada, pronta para adaptação pela procuradoria. Repare no que ela <b>não</b> contém: não há valor, não há exclusividade, não há prazo de contratação, não há qualquer obrigação financeira. É por isso que ela não exige licitação — não contrata nada; apenas formaliza a intenção de estudar juntos.'))
s.append(sp(3))
clausulas = [
 ('DAS PARTES', 'Município de [NOME], pessoa jurídica de direito público, representado por seu Prefeito, e Zion Ecosystem [SPE], pessoa jurídica de direito privado, doravante denominados Partícipes.'),
 ('DO OBJETO', 'Manifestar o interesse recíproco em estudar a viabilidade de implantação de sistema de valorização de resíduos sólidos urbanos no Município, incluindo a elaboração, pela iniciativa privada e sem ônus ao Município, de diagnóstico técnico-econômico (Diagnóstico Circular).'),
 ('DO COMPARTILHAMENTO DE DADOS', 'O Município disponibilizará dados operacionais do manejo de resíduos — volumes, contratos vigentes, rotas e custos — exclusivamente para a finalidade do estudo, observada a legislação de acesso e proteção de dados.'),
 ('DA AUSÊNCIA DE ÔNUS', 'Este Protocolo não gera obrigação financeira, não constitui promessa de contratação e não confere exclusividade a qualquer dos Partícipes.'),
 ('DA CONTRATAÇÃO FUTURA', 'Eventual contratação decorrente dos estudos observará a legislação aplicável, a critério exclusivo do Município.'),
 ('DA VIGÊNCIA', 'O presente Protocolo vigora por 12 (doze) meses, prorrogáveis por acordo, podendo ser denunciado por qualquer Partícipe mediante comunicação escrita.'),
]
for t, d in clausulas:
    s.append(h3(t))
    s.append(Paragraph(d, S('cla',fontSize=9.5,textColor=GRAY,leading=15,spaceAfter=6,alignment=TA_JUSTIFY)))
s.append(sp(3))
s.append(hl_box('Uma página. Zero custo. Zero exclusividade. É tudo que a primeira reunião precisa pedir — e tudo que uma proposta séria deveria pedir.'))
s.append(PageBreak())

# ══════════ ANEXO B — ROTEIRO DA REUNIÃO ══════════════════════════
s += [sp(4), lb('Anexo B'), gl(), sp(3)]
s.append(h1('O Roteiro da Reunião de 20 Minutos'))
s.append(sp(2))
s.append(body('A apresentação ao prefeito segue o método ECROI — a sequência de persuasão da Zion — em cinco tempos. O quadro abaixo é o roteiro minuto a minuto, com a função de cada bloco. A regra de ouro: a única meta da reunião é o protocolo; quem pede contrato na primeira conversa assusta, quem pede uma assinatura de custo zero avança.'))
s.append(sp(3))
s.append(tabela([
 ['Minuto', 'Bloco', 'O que acontece'],
 ['0–3', 'Espelhamento', 'Os números do próprio município na tela: toneladas/dia, custo/t, total do mandato. Efeito buscado: "ele conhece a minha cidade".'],
 ['3–7', 'Colapso', 'A crença "lixo é despesa" confrontada com o custo invisível: R$ X milhões enterrados sem uma obra. E o que o marco legal criou desde 2023.'],
 ['7–11', 'Reencadramento', 'A nova moldura: contrato de industrialização com retorno em produto. O caminhão que traz de volta. A praça com placa.'],
 ['11–16', 'Inevitabilidade', 'A prova: o caso de R$ 7 bi na bolsa, o financiamento federal já aberto, o protótipo físico na mesa — o prefeito precisa sentar no banco.'],
 ['16–20', 'O convite', 'Protocolo de uma página apresentado e explicado: custo zero, sem exclusividade. Diagnóstico Circular gratuito em 30 dias. Assinatura ou agenda de assinatura.'],
], cw=[AV*0.11, AV*0.20, AV*0.69]))
s.append(sp(3))
s.append(caixa_gold('O KIT DA REUNIÃO — O QUE LEVAR', [
 'Deck de 11 páginas com o nome do município na capa',
 'Um banco ou carteira de madeira plástica física — o objeto vende mais que o slide',
 'Minuta do protocolo (Anexo A) impressa, pronta para assinar',
 'One-page do Diagnóstico Circular — o que o prefeito recebe em 30 dias',
 'Vídeo de 90 segundos do ciclo completo, para o prefeito repostar',
]))
s.append(sp(3))
s.append(body('Ordem de abordagem que antecede essa reunião: primeiro o secretário da pasta (que valida tecnicamente e vira aliado interno), depois a Fazenda (que confirma a economia), e só então o prefeito — com os dois secretários já convertidos na sala. Prefeito convencido antes da equipe vira projeto órfão na primeira crise de agenda.'))
s.append(h2('Os seis erros que matam a reunião'))
s.append(body('<b>Erro 1 — abrir com a tecnologia.</b> O prefeito não compra extrusora; compra a foto da inauguração. Tecnologia entra só quando perguntada. <b>Erro 2 — slides genéricos.</b> Sem os números da cidade dele na primeira tela, a reunião vira palestra. <b>Erro 3 — pedir contrato.</b> A meta é o protocolo; pedir mais é pedir para adiar. <b>Erro 4 — atacar o modelo atual.</b> O contrato de aterro vigente foi assinado por alguém que está na sala ou é aliado de quem está; a proposta convive com ele e migra no vencimento. <b>Erro 5 — prometer prazo de crédito de carbono.</b> É upside; prometido como certeza, vira dívida de credibilidade. <b>Erro 6 — sair sem data.</b> Toda reunião termina com a próxima marcada: a assinatura, a visita técnica ou a apresentação à procuradoria.'))
s.append(PageBreak())

# ══════════ ANEXO C — PERGUNTAS DA CÂMARA ═════════════════════════
s += [sp(4), lb('Anexo C'), gl(), sp(3)]
s.append(h1('As 10 Perguntas da Câmara — e as Respostas'))
s.append(sp(2))
s.append(body('Todo projeto municipal relevante passa pelo plenário — e é melhor chegar lá com as respostas prontas. As dez perguntas abaixo cobrem o que vereadores, imprensa local e cidadãos efetivamente perguntam.'))
s.append(sp(3))
faq = [
 ('1. Quanto isso vai custar para a prefeitura?',
  'Menos do que o modelo atual. O contrato fixa tarifa por tonelada abaixo do custo de disposição vigente — a economia começa no primeiro mês. O investimento da planta é privado, financiado por linhas federais.'),
 ('2. E se a empresa quebrar no meio do caminho?',
  'O município não antecipou nada — paga apenas pelo serviço prestado, tonelada a tonelada. Na pior hipótese, retoma o contrato de disposição anterior, na posição em que estava.'),
 ('3. Por que sem licitação?',
  'O protocolo de intenções não contrata nada — não exige licitação. O contrato de serviço, quando vier, seguirá o instrumento que a procuradoria indicar: dispensa por valor, credenciamento, licitação ou PPP. As quatro minutas são apresentadas junto com o diagnóstico.'),
 ('4. O que acontece com os catadores?',
  'São integrados, não substituídos: a triagem é operada prioritariamente pelas cooperativas locais, com contrato, equipamento e renda previsível — como a legislação de resíduos determina e os editais federais premiam.'),
 ('5. A planta vai gerar mau cheiro?',
  'Compostagem acelerada aerada é processo controlado de temperatura e oxigenação — tecnicamente distinto do lixão, que é anaeróbio. O licenciamento estadual fixa condicionantes de odor, e o monitoramento é público.'),
 ('6. Quem fiscaliza os números?',
  'O mesmo sistema que rastreia cada tonelada para gerar crédito alimenta um painel público mensal: toneladas desviadas, mobiliário entregue, indicadores de contrato. A transparência é cláusula contratual.'),
 ('7. Isso não é grande demais para a nossa cidade?',
  'O modelo foi dimensionado para municípios de 30 a 150 mil habitantes — e cidades menores participam via consórcio. É exatamente o tamanho que os grandes operadores nacionais ignoram.'),
 ('8. Qual o ganho para as escolas?',
  'Carteiras novas de madeira plástica com a história do programa, módulos de compostagem pedagógica e o conteúdo de educação ambiental — financiado por edital federal, não pelo caixa municipal.'),
 ('9. E quando trocar o prefeito?',
  'Contrato administrativo formalizado não se extingue com o mandato. E os marcos trimestrais de entrega tornam o programa popular o suficiente para nenhum sucessor querer o ônus de encerrá-lo.'),
 ('10. Por que essa empresa e não outra?',
  'Porque a proposta é verificável em cada etapa: primeiro um protocolo de custo zero, depois um diagnóstico gratuito com os números da cidade, e só então um contrato — que custa menos que o aterro e devolve parte do valor em patrimônio público. Qualquer concorrente que ofereça mais por menos merece ganhar.'),
]
for q, a in faq:
    s.append(h3(q))
    s.append(Paragraph(a, S('faqa',fontSize=9.5,textColor=GRAY,leading=15,spaceAfter=6,alignment=TA_JUSTIFY)))
s.append(PageBreak())

# ══════════ ANEXO D — DOCUMENTOS DA CAPTAÇÃO ══════════════════════
s += [sp(4), lb('Anexo D'), gl(), sp(3)]
s.append(h1('O Dossiê de Captação — Checklist de Documentos'))
s.append(sp(2))
s.append(body('A lista consolidada do que cada frente da captação exige. Municípios e operadores que chegam aos editais com este dossiê pronto saem na frente de 90% das propostas — porque a maioria é eliminada na conferência documental, antes de qualquer análise de mérito.'))
s.append(sp(3))
s.append(caixa_gold('DO MUNICÍPIO — PARA PAC, FNMA E CONVÊNIOS', [
 'CAUC regular e certidões federais, estaduais e municipais válidas',
 'Plano Municipal (ou intermunicipal) de Gestão Integrada de Resíduos atualizado',
 'Lei autorizativa de participação em consórcio, quando aplicável',
 'Cadastro atualizado na plataforma federal de transferências',
 'Titularidade ou dominialidade da área indicada para a planta',
]))
s.append(sp(3))
s.append(caixa_gold('DA OPERADORA — PARA FUNDO CLIMA E FINEP', [
 'SPE constituída com CNAE de tratamento de resíduos e certidões limpas',
 'Contrato âncora (ou protocolo avançado) com município ou consórcio',
 'Projeto técnico da planta com cronograma físico-financeiro',
 'Licença ambiental prévia ou protocolo de licenciamento em curso',
 'Termo de parceria com ICT para a chamada Finep',
 'Demonstrações financeiras e matriz de garantias da holding',
]))
s.append(sp(3))
s.append(caixa_gold('DA OPERAÇÃO — PARA OS CRÉDITOS', [
 'Habilitação como emissor junto a entidade gestora de logística reversa (CCRLR)',
 'Projeto de carbono registrado com metodologia de compostagem/aterro evitado',
 'Sistema de rastreabilidade por tonelada com trilha de auditoria',
 'Contratos de destino para composto, mobiliário e recicláveis',
]))
s.append(sp(3))
s.append(hl_box('Regra prática: um dossiê completo leva 60 a 90 dias para ser montado do zero. Editais abrem e fecham em menos tempo que isso. Monte o dossiê antes do edital — não por causa dele.'))
s.append(PageBreak())

# ══════════ ANEXO E — PAINEL PÚBLICO ══════════════════════════════
s += [sp(4), lb('Anexo E'), gl(), sp(3)]
s.append(h1('O Painel Público — Modelo de Transparência'))
s.append(sp(2))
s.append(body('A transparência é cláusula do contrato âncora — e o painel público mensal é a sua forma concreta. O modelo abaixo define os indicadores mínimos, a frequência e a fonte de cada número. O mesmo sistema que rastreia a tonelada para o crédito alimenta o painel: não há trabalho extra, só publicação do que já é medido.'))
s.append(sp(3))
s.append(tabela([
 ['Indicador', 'Frequência', 'Fonte do dado'],
 ['Toneladas coletadas por fração (orgânico, seco, rejeito)', 'Mensal', 'Balança da planta'],
 ['Percentual de desvio de aterro', 'Mensal', 'Sistema de rastreabilidade'],
 ['Taxa de contaminação da coleta segregada', 'Mensal', 'Triagem'],
 ['Mobiliário entregue no trimestre (unidades e locais)', 'Trimestral', 'Cronograma da contrapartida'],
 ['Economia acumulada vs. contrato de aterro anterior', 'Trimestral', 'Fazenda municipal'],
 ['Créditos emitidos (CCRLR e carbono)', 'Trimestral', 'Certificadoras'],
 ['Empregos diretos e cooperados ativos', 'Semestral', 'Operadora + cooperativas'],
], cw=[AV*0.48, AV*0.18, AV*0.34]))
s.append(sp(3))
s.append(body('Três regras de publicação. Primeira: o painel sai todo mês na mesma data, mesmo quando o número é ruim — credibilidade se constrói nos meses ruins. Segunda: cada indicador tem série histórica aberta, não só a foto do mês. Terceira: a linguagem é de cidadão, não de engenheiro — "o lixo de 70 em cada 100 casas virou produto" comunica mais que "índice de desvio ponderado".'))
s.append(sp(2))
s.append(hl_box('O painel é a resposta permanente à pergunta da Câmara, da imprensa e da oposição. Quem publica os números primeiro nunca precisa respondê-los na defensiva.'))
s.append(PageBreak())

# ══════════ MÓDULO FINAL — SEPARADOR ══════════════════════════════
s.append(sp(20))
s.append(Paragraph('— · —', S('sep',fontSize=14,textColor=GOLD,alignment=TA_CENTER,spaceAfter=8)))
s.append(Paragraph('O que você leu até aqui foi o mapa.<br/>O que vem a seguir é o espelho.',
    S('sep2',fontName='Helvetica-Oblique',fontSize=12,textColor=DARK,alignment=TA_CENTER,leading=20,spaceAfter=0)))
s.append(PageBreak())

# ══════════ E — ESPELHAMENTO ══════════════════════════════════════
s += [sp(4), lb('E · Espelhamento'), gl(), sp(3)]
s.append(h1('Você Reconhece Esta Cena?'))
s.append(sp(2))
espelhos = [
 ('O Prefeito da Conta que Só Cresce',
  'Você assumiu a prefeitura com uma lista de sonhos e herdou uma lista de contratos. O do lixo é o que mais incomoda: todo ano ele reajusta, todo ano consome mais orçamento, e nunca — nunca — rende uma única entrega que você possa mostrar. Você já pensou "tem que haver um jeito melhor", mas entre a saúde, a folha e a estrada, o lixo sempre fica para o próximo semestre. E o próximo. E o mandato vai passando com a conta crescendo em silêncio.'),
 ('O Secretário que Apaga Incêndio',
  'Você é o secretário. É seu telefone que toca quando a coleta atrasa, quando o vizinho do lixão reclama, quando o Ministério Público manda ofício. Você conhece os números de cor e sabe que o modelo atual é uma bomba de efeito retardado — mas toda proposta que já chegou à sua mesa ou era cara demais, ou era maluca demais, ou pedia confiança demais antes de entregar qualquer coisa. Você não precisa de mais uma ideia. Precisa de um caminho com degraus que você consiga defender tecnicamente.'),
 ('O Empreendedor que Enxerga Antes',
  'Você é da cidade. Tem empresa, tem capital ou tem vontade — e vê o caminhão do lixo passar todo dia sabendo que ali dentro tem dinheiro que ninguém está pegando. Você já leu sobre créditos de carbono, já ouviu falar de madeira plástica, já pensou "alguém vai fazer isso aqui e não vou ser eu". O que te faltava não era visão. Era um modelo estruturado, com engenharia, marca e captação resolvidas, no qual você pudesse entrar como sócio local em vez de inventar tudo sozinho.'),
]
for t, d in espelhos:
    s.append(h3(t)); s.append(Paragraph(d, ST['manif'])); s.append(sp(2))
s.append(sp(2))
s += qt('Se você se reconheceu em qualquer uma dessas cenas, o seu problema nunca foi orçamento. Foi a ausência de um caminho com degraus de custo zero no começo. Agora ele existe.')
s.append(PageBreak())

# ══════════ C — COLAPSO DE CRENÇA ═════════════════════════════════
s += [sp(4), lb('C · Colapso de Crença'), gl(), sp(3)]
s.append(h1('As 5 Crenças que Mantêm sua Cidade Enterrando Dinheiro'))
s.append(sp(2))
s.append(body('Cinco frases repetidas em gabinetes há décadas — razoáveis na aparência, e erradas diante do arcabouço legal e do mercado que existem hoje. Cada uma delas colapsa quando confrontada com fatos verificáveis.'))
s.append(sp(3))
crencas = [
 ('Crença 1 — "Lixo é despesa e sempre será"',
  '"Gestão de resíduos é custo. O máximo que se pode fazer é administrá-lo."',
  'Uma empresa brasileira vale R$ 7 bilhões na bolsa extraindo sete receitas do mesmo lixo que sua cidade paga para enterrar. Gate fee, produto, energia, crédito de reciclagem e crédito de carbono saem da mesma tonelada. Lixo só é despesa em cidade sem indústria de valorização — a despesa não está no lixo, está no modelo.'),
 ('Crença 2 — "Resolver o lixo exige dinheiro que o município não tem"',
  '"Qualquer solução dessas custa milhões que o orçamento não comporta."',
  'O CAPEX da planta é privado, financiado por Fundo Clima e Finep com juros subsidiados e subvenção. O que o município assina primeiro custa zero. O que assina depois custa menos do que o contrato de aterro atual. A infraestrutura pública da ponta vem do PAC — recurso federal que a prefeitura capta com o projeto que nós estruturamos.'),
 ('Crença 3 — "Isso é coisa de cidade grande"',
  '"Economia circular funciona em capital, não num município de 60 mil habitantes."',
  'É o contrário: as capitais já têm contratos gigantes e players gigantes. O modelo CIRO foi dimensionado exatamente para 30–150 mil habitantes — e o consórcio intermunicipal soma os volumes de cidades menores até a escala industrial. O mercado que os grandes ignoram é precisamente o seu.'),
 ('Crença 4 — "Vai travar na burocracia"',
  '"Entre licitação, licença e câmara, isso leva dez anos."',
  'O primeiro degrau — protocolo de intenções — não exige licitação, porque não contrata nada. O contrato posterior tem quatro caminhos jurídicos possíveis, com minutas prontas para a procuradoria escolher. E o licenciamento de compostagem e reciclagem é ordens de grandeza mais simples que o de aterro ou incineração. A burocracia real é menor que a burocracia imaginada — ela mora nos projetos sem método.'),
 ('Crença 5 — "Ninguém ganha eleição por causa de lixo"',
  '"Investir nisso não rende politicamente. O eleitor não vê."',
  'O eleitor não vê o aterro — mas vê a praça nova, a carteira nova do filho, a placa de inauguração. O modelo devolve o resíduo em patrimônio público com marcos trimestrais: uma inauguração por trimestre até o fim do mandato. Lixo não dá voto; praça feita de lixo dá manchete estadual. A crença confunde o problema (invisível) com a solução (visibilíssima).'),
]
for titulo, crenca, realidade in crencas:
    s.append(h2(titulo))
    tb1 = Table([
        [Paragraph('O QUE SE ACREDITA', S('cl1',fontName='Helvetica-Bold',fontSize=7,textColor=LGRAY,spaceAfter=2))],
        [Paragraph(crenca, S('cl2',fontName='Helvetica-Oblique',fontSize=10,textColor=colors.HexColor('#888888'),leading=15,spaceAfter=0))],
    ], colWidths=[AV])
    tb1.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#F0EDE8')),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
        ('LINEBEFORE',(0,0),(0,-1),2,colors.HexColor('#CCCCCC'))]))
    s.append(tb1); s.append(sp(2))
    tb2 = Table([
        [Paragraph('O QUE É VERDADE', S('cr1',fontName='Helvetica-Bold',fontSize=7,textColor=GOLD,spaceAfter=2))],
        [Paragraph(realidade, S('cr2',fontSize=10,textColor=CREAM,leading=15,spaceAfter=0,alignment=TA_JUSTIFY))],
    ], colWidths=[AV])
    tb2.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#0D0D0D')),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
        ('LINEBEFORE',(0,0),(0,-1),2,GOLD)]))
    s.append(tb2); s.append(sp(4))
s.append(PageBreak())

# ══════════ CUSTO INVISÍVEL ═══════════════════════════════════════
s += [sp(4), lb('C · Custo Invisível'), gl(), sp(3)]
s.append(h1('Quanto Custa Cada Mês da Cidade que Enterra?'))
s.append(sp(3))
s.append(body('O custo invisível não é o que a prefeitura gasta. É o que ela gasta sem retorno — e o que deixa de capturar. Os cards abaixo usam o município padrão de 100 mil habitantes deste volume; troque pelos seus números do exercício do Capítulo 1.'))
s.append(sp(4))
dados_custo = [
 ('R$ 2,46 mi', '/ano', '16.400 t × R$ 150/t de disposição', 'O que sai do orçamento por ano só para enterrar'),
 ('R$ 9,8 mi', '/mandato', 'R$ 2,46 mi × 4 anos', 'Um mandato inteiro de disposição — sem uma obra para mostrar'),
 ('R$ 205 mil', '/mês', 'R$ 2,46 mi ÷ 12', 'Cada mês de decisão adiada'),
 ('R$ 6.700', '/dia', 'R$ 2,46 mi ÷ 365', 'Cada dia útil de "vamos ver isso depois"'),
]
cards = []
for num, unid, form, desc in dados_custo:
    cards.append(Table([
        [Paragraph(num, ST['custo_n'])],
        [Paragraph(unid, ST['custo_l'])],
        [Paragraph(form, S('cf2',fontName='Helvetica-Oblique',fontSize=7.5,textColor=LGRAY,alignment=TA_CENTER,spaceAfter=0))],
        [Paragraph(desc, S('cd3',fontSize=8.5,textColor=CREAM,alignment=TA_CENTER,leading=13,spaceAfter=0))],
    ], colWidths=[AV/2 - 20]))
for i in range(0, 4, 2):
    pair = Table([[cards[i], cards[i+1]]], colWidths=[AV/2, AV/2])
    pair.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLACK),
        ('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#222222')),
        ('LINEABOVE',(0,0),(-1,0),0.8,GOLD),('LINEBELOW',(0,-1),(-1,-1),0.8,GOLD)]))
    s.append(pair); s.append(sp(2))
s.append(sp(3))
s.append(body('E há a segunda camada, a que não aparece na fatura: cada tonelada enterrada deixa de gerar o crédito de reciclagem e o crédito de carbono que a mesma tonelada geraria valorizada. A cidade que enterra paga a disposição — e joga fora, junto com o resíduo, o ativo que a lei criou para ela.'))
s += qt('A questão não é se o município pode se dar ao luxo de mudar de modelo. É se pode se dar ao luxo de pagar mais quatro anos pelo modelo que não deixa nada de pé.')
s.append(PageBreak())

# ══════════ APOSTA DE PASCAL MUNICIPAL ════════════════════════════
s += [sp(4), lb('O · A Aposta de Pascal Municipal'), gl(), sp(3)]
s.append(h1('O Quadro de Decisão do Prefeito'))
s.append(sp(2))
s.append(body('Blaise Pascal resolveu decisões sob incerteza com um quadro de quatro células: o que acontece se eu agir e der certo, se eu agir e der errado, se eu não agir e o mundo mudar, e se eu não agir e nada mudar. Aplicado à cidade circular, o quadro fica assim:'))
s.append(sp(4))
pascal = [
 ('ASSINA O PROTOCOLO · DÁ CERTO',
  'A cidade economiza desde o primeiro contrato, inaugura patrimônio a cada trimestre e vira case estadual. O custo da aposta foi: uma assinatura.'),
 ('ASSINA O PROTOCOLO · NÃO AVANÇA',
  'O município recebeu gratuitamente o diagnóstico com seus números reais — que serve para qualquer projeto futuro, com qualquer parceiro. Perda efetiva: zero.'),
 ('NÃO ASSINA · O MODELO SE PROVA NA REGIÃO',
  'A cidade vizinha inaugura primeiro, leva o consórcio, o título de pioneira e a agenda regional. Sua cidade entra depois — pagando o mesmo, colhendo menos, atrás de quem saiu na frente.'),
 ('NÃO ASSINA · NADA MUDA',
  'Mais quatro anos de aterro: R$ 9,8 milhões enterrados no mandato, risco jurídico intacto, nenhuma placa. O cenário "seguro" é o único com perda garantida.'),
]
for t, d in pascal:
    row = Table([
        [Paragraph(t, S('pt2',fontName='Helvetica-Bold',fontSize=9,textColor=GOLD,spaceAfter=2))],
        [Paragraph(d, S('pd2',fontSize=9.5,textColor=CREAM,leading=14,spaceAfter=0,alignment=TA_JUSTIFY))],
    ], colWidths=[AV])
    row.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BGDARK),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),
        ('LINEBEFORE',(0,0),(0,-1),2,GOLD)]))
    s.append(row); s.append(sp(2))
s.append(sp(2))
s.append(body('Leia as quatro células de novo. Três delas terminam bem ou neutras para quem assina. A única célula com perda certa é a inação com o mundo parado — e o mundo, como o Capítulo 2 mostrou, não está parado: a régua legal sobe todo ano. Quando o pior cenário da ação é "ganhei um diagnóstico de graça" e o melhor cenário da inação é "perdi só R$ 9,8 milhões", a decisão deixou de ser aposta.'))
s.append(PageBreak())

# ══════════ R — REENCADRAMENTO ════════════════════════════════════
s += [sp(4), lb('R · Reencadramento'), gl(), sp(3)]
s.append(h1('De Como a Cidade Via — Para Como É'))
s.append(sp(2))
s.append(body('Se este volume cumpriu sua função, dez molduras mudaram de lugar. O quadro abaixo é o resumo executivo da mudança — para levar à reunião de secretariado.'))
s.append(sp(4))
reenc = [
 ('Lixo é despesa', 'Lixo é matéria-prima que a cidade já possui'),
 ('Contrato de aterro', 'Contrato de industrialização com retorno em produto'),
 ('Custo sem obra', 'Praça, escola e mobiliário com placa de inauguração'),
 ('Passivo ambiental', 'Case nacional de cidade circular'),
 ('O caminhão que leva embora', 'O caminhão que traz de volta'),
 ('Multa e TAC no horizonte', 'Crédito ambiental no fluxo de caixa'),
 ('Problema do secretário', 'Plataforma política do prefeito'),
 ('Projeto que depende de orçamento', 'Projeto que depende de assinatura de custo zero'),
 ('Cidade pequena demais para isso', 'Cidade do tamanho exato do modelo'),
 ('Fim de linha', 'Começo de ciclo'),
]
for de, para in reenc:
    row = Table([
        [Paragraph(f'<strike>{de}</strike>', S('rde2',fontSize=9,textColor=colors.HexColor('#999999'),alignment=TA_CENTER)),
         Paragraph('→', S('arr2',fontName='Helvetica-Bold',fontSize=14,textColor=GOLD,alignment=TA_CENTER)),
         Paragraph(f'<b>{para}</b>', S('rpa2',fontName='Helvetica-Bold',fontSize=9,textColor=DARK,leading=13))],
    ], colWidths=[79*mm, 12*mm, 79*mm])
    row.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('LINEBELOW',(0,0),(-1,-1),0.3,colors.HexColor('#EEEEEE')),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    s.append(row)
s.append(sp(4))
s.append(hl_box('A nova moldura não muda o lixo da cidade. Muda o que a cidade faz com ele. E isso muda o mandato.'))
s.append(PageBreak())

# ══════════ OP3LIF ════════════════════════════════════════════════
s += [sp(4), lb('OP3LIF · Pareto em Cascata Tripla'), gl(), sp(3)]
s.append(h1('As 3 Ações que Valem Mais que as Outras 97'))
s.append(sp(2))
s.append(body('O OP3LIF é o framework de priorização da Zion: Pareto aplicado sobre Pareto sobre Pareto, até isolar a fração mínima de ações com resultado máximo. Aplicado à cidade circular, o funil fica assim:'))
s.append(sp(4))
niveis = [
 ('Pareto 1', '20%', 'das ações geram 80% do resultado',
  'De tudo que um município pode fazer por resíduos, cinco ações concentram o impacto: levantar a conta real (Cap. 1), regularizar plano e certidões (Cap. 7), assinar o protocolo, receber o Diagnóstico Circular e priorizar o tema no próximo ciclo do PAC.'),
 ('Pareto 2', '4%', 'das ações geram 64% do resultado',
  'Dessas cinco, uma alavanca as outras: o Diagnóstico Circular. Com os números reais na mesa, o contrato se justifica sozinho, a captação tem anexo técnico e a câmara tem resposta para toda objeção. Sem diagnóstico, tudo é opinião; com ele, tudo é decisão.'),
 ('OP3LIF', '0,8%', 'das ações geram resultado exponencial',
  'E o diagnóstico depende de um único ato: assinar o protocolo de intenções — uma página, custo zero, sem licitação, sem exclusividade. É a menor ação possível com a maior consequência possível: ela destrava todas as outras. Assine o protocolo, e o resto vira consequência.'),
]
for nome, pct, desc, apl in niveis:
    tbn = Table([[Paragraph(pct, ST['op3_num'])],[Paragraph(desc, ST['op3_pct'])]], colWidths=[32*mm])
    tbn.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLACK),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),2),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('LINEABOVE',(0,0),(-1,0),0.8,GOLD),('LINEBELOW',(0,-1),(-1,-1),0.8,GOLD)]))
    tbt = Table([
        [Paragraph(nome.upper(), S('pn2',fontName='Helvetica-Bold',fontSize=7,textColor=GOLD,spaceAfter=2))],
        [Paragraph(apl, S('pa2',fontSize=9,textColor=GRAY,leading=14,alignment=TA_JUSTIFY,spaceAfter=0))],
    ], colWidths=[AV-32*mm-4*mm])
    tbt.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]))
    outer = Table([[tbn, tbt]], colWidths=[32*mm, AV-32*mm])
    outer.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('VALIGN',(0,0),(-1,-1),'TOP')]))
    s.append(outer); s.append(sp(4))
s.append(sp(2))
s.append(caixa_gold('AS 3 AÇÕES OP3LIF PARA EXECUTAR ESTA SEMANA — CUSTO ZERO', [
 'Levantar a conta real do lixo com a Fazenda (toneladas, gate fee, total anual)',
 'Pautar o tema em 20 minutos da próxima reunião de secretariado',
 'Solicitar o protocolo de intenções e o Diagnóstico Circular do município',
]))
s.append(PageBreak())

# ══════════ LINHA DO TEMPO ════════════════════════════════════════
s += [sp(4), lb('O · Inevitabilidade — A Linha do Tempo Ideal'), gl(), sp(3)]
s.append(h1('Da Assinatura à Primeira Inauguração'))
s.append(sp(2))
s.append(body('Este é o caminho com prazos realistas para um município âncora. Não é promessa — é sequência de etapas com entregável e critério de avanço, no padrão de método que a Zion aplica em todos os seus desenvolvimentos.'))
s.append(sp(4))
etapas = [
 ('Mês 1–2', 'DECISÃO — protocolo e diagnóstico',
  'Reunião técnica · Apresentação ao prefeito · Protocolo de intenções assinado · Coleta de dados',
  'Entrega: Diagnóstico Circular do município — números reais, desenho ideal, potencial de contrapartida',
  'Critério de avanço: prefeito decide com o diagnóstico na mão'),
 ('Mês 3–4', 'CONTRATO — o enquadramento jurídico',
  'Procuradoria escolhe o instrumento · Gate fee e contrapartida fixados · Área da planta indicada',
  'Entrega: contrato assinado com marcos trimestrais de mobiliário',
  'Critério de avanço: contrato publicado e área definida'),
 ('Mês 5–9', 'ESTRUTURA — licenças e captação',
  'Licenciamento ambiental · Protocolo Fundo Clima/BNDES · Submissão Finep · Habilitação CCRLR e projeto de carbono',
  'Entrega: financiamento da planta aprovado — risco 100% privado',
  'Critério de avanço: licença de instalação + funding contratado'),
 ('Mês 10–15', 'PILOTO — a cidade começa a separar',
  'Coleta piloto em bairros e escolas · Educação ambiental · Módulo de compostagem em operação · Obras da planta',
  'Entrega: primeiras toneladas desviadas do aterro — e primeiros dados de crédito',
  'Critério de avanço: meta de contaminação da coleta abaixo de 15%'),
 ('Mês 16–20', 'PLANTA — operação plena',
  'CIRO operacional nas duas linhas · Primeira emissão de créditos · Produção de mobiliário',
  'Entrega: a primeira praça inaugurada com mobiliário feito do resíduo da própria cidade',
  'Critério de avanço: a foto da placa de inauguração'),
 ('Mês 21+', 'REDE — a replicação regional',
  'Municípios vizinhos visitam a operação · Consórcio estruturado · Proposta conjunta no PAC Seleções',
  'Entrega: o modelo replicado — e a cidade âncora como capital regional da economia circular',
  'Critério: cada nova cidade encurta o caminho da seguinte'),
]
for prazo, titulo, ativ, entrega, criterio in etapas:
    hdr = Table([
        [Paragraph(prazo, S('ep2',fontName='Helvetica-Bold',fontSize=8,textColor=GOLD,spaceAfter=0)),
         Paragraph(titulo, S('et2',fontName='Helvetica-Bold',fontSize=10,textColor=CREAM,spaceAfter=0,leading=14))],
    ], colWidths=[24*mm, AV-24*mm])
    hdr.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#111111')),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LINEABOVE',(0,0),(-1,0),0.5,GOLD)]))
    s.append(hdr)
    bt = Table([
        [Paragraph(f'<b>Atividades:</b> {ativ}', S('la2',fontSize=8.5,textColor=GRAY,leading=13))],
        [Paragraph(f'<font color="#C9A84C">▸</font> <b>{entrega}</b>', S('lz2',fontSize=8.5,textColor=GRAY,leading=13))],
        [Paragraph(f'<i>{criterio}</i>', S('ls2',fontSize=8.5,textColor=colors.HexColor('#555555'),leading=13))],
    ], colWidths=[AV])
    bt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BGLIGHT),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('LINEBELOW',(0,-1),(-1,-1),0.3,colors.HexColor('#DDDDDD'))]))
    s.append(bt); s.append(sp(2))
s.append(sp(3))
s.append(hl_box('Em menos de dois anos, a cidade que enterrava vira a cidade que inaugura. Não é promessa: é a sequência de degraus que este volume inteiro documentou.'))
s.append(PageBreak())

# ══════════ I — LOOP VIRAL ════════════════════════════════════════
s += [sp(4), lb('I · Resultado Viral Educacional'), gl(), sp(3)]
s.append(h1('O Loop que Faz a Cidade Circular se Multiplicar'))
s.append(sp(2))
s.append(body('Este volume não termina quando você fecha a última página. Termina quando a segunda cidade assina — porque viu a primeira inaugurar. O modelo carrega seu próprio motor de expansão, e ele tem cinco tempos:'))
s.append(sp(3))
loop = [
 ('1 · APARECE', 'Este volume chega a um gestor ou empreendedor — por indicação, por um evento, por uma reportagem sobre a primeira cidade. O primeiro contato é com conhecimento, não com oferta.'),
 ('2 · EDUCA', 'A leitura entrega o mapa completo: a conta, a lei, o modelo, o dinheiro e a escada. O leitor sai sabendo mais sobre a economia do próprio lixo do que a maioria dos consultores que já bateram à sua porta.'),
 ('3 · CONVERTE', 'Com a conta feita e o caminho claro, o protocolo de custo zero deixa de ser risco e vira obviedade. Ninguém foi convencido — foi educado até a decisão se tornar inevitável.'),
 ('4 · TRANSFORMA', 'A cidade sobe a escada: diagnóstico, contrato, planta, piloto. As primeiras toneladas mudam de destino. A primeira praça ganha mobiliário com história.'),
 ('5 · MULTIPLICA', 'O prefeito vizinho visita a inauguração. O secretário apresenta o case no congresso estadual. O empreendedor de outra cidade escreve perguntando como levar o modelo. O ciclo recomeça — sem uma única mídia paga.'),
]
for nn, d in loop:
    row = Table([
        [Paragraph(nn, S('ln3',fontName='Helvetica-Bold',fontSize=8,textColor=GOLD,spaceAfter=0))],
        [Paragraph(d, S('ld3',fontSize=9.5,textColor=GRAY,leading=14,spaceAfter=0,alignment=TA_JUSTIFY))],
    ], colWidths=[AV])
    row.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('LINEBEFORE',(0,0),(0,-1),2,GOLD),
        ('LINEBELOW',(0,-1),(-1,-1),0.3,colors.HexColor('#EEEEEE'))]))
    s.append(row); s.append(sp(1))
s.append(sp(4))
s.append(body('A pergunta não é se o modelo funciona — o Capítulo 4 respondeu com um valor de mercado de R$ 7 bilhões. A pergunta é qual cidade da sua região vai ser a primeira a inaugurar. E se ela vai ser a sua, ou a do vizinho.'))
s.append(PageBreak())

# ══════════ INTERLÚDIO FINAL ══════════════════════════════════════
s += interlude('A cidade que enterra<br/>paga duas vezes.<br/>A cidade que inaugura<br/>colhe duas vezes.', 'O espelho final antes da decisão')

# ══════════ CTA FINAL ═════════════════════════════════════════════
s += [sp(6), lb('O Próximo Passo Lógico'), gl(), sp(4)]
s.append(h1('A Sua Cidade nos Números Dela'))
s.append(sp(3))
s.append(body('Tudo que você leu é aplicável — mas foi escrito sobre um município padrão. A decisão real exige os números reais: quanto a sua cidade gera, quanto paga, quanto pode economizar, e quantas praças e salas de aula o resíduo dela pode virar por ano.'))
s.append(body('É exatamente isso que o Diagnóstico Circular entrega. E o caminho até ele custa zero: um protocolo de intenções de uma página, sem licitação, sem exclusividade, sem obrigação financeira. Trinta dias depois, o prefeito decide com o relatório na mão.'))
s.append(sp(5))
s.append(Table([[Paragraph('DIAGNÓSTICO CIRCULAR DO MUNICÍPIO', ST['cta_h'])],
    [Paragraph('O estudo gratuito que transforma este volume na realidade da sua cidade', ST['cta_b'])],
    [Paragraph('O que entregamos em 30 dias:', ST['cta_b'])],
    [Paragraph('Toneladas, custos e gate fee reais do município · Economia projetada com o modelo CIRO', ST['cta_b'])],
    [Paragraph('Potencial de contrapartida: praças e salas de aula por ano · Desenho ideal: planta própria, consórcio ou hub', ST['cta_b'])],
    [Paragraph('Mapa de captação federal aplicável ao seu caso · Minuta do protocolo de intenções', ST['cta_b'])],
    [Paragraph('zionhotelgroup.com.br/cidadecircular  ·  Cortesia para municípios com protocolo assinado', ST['cta_u'])]],
    colWidths=[AV], style=TableStyle([
    ('BACKGROUND',(0,0),(-1,-1),BLACK),
    ('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),
    ('LEFTPADDING',(0,0),(-1,-1),16),('RIGHTPADDING',(0,0),(-1,-1),16),
    ('LINEABOVE',(0,0),(-1,0),1.5,GOLD),('LINEBELOW',(0,-1),(-1,-1),1.5,GOLD),
    ('LINEBEFORE',(0,0),(0,-1),1.5,GOLD),('LINEAFTER',(-1,0),(-1,-1),1.5,GOLD)])))
s.append(sp(5))
s.append(body('Empreendedores e investidores interessados em operar ou ancorar o modelo na sua região: o mesmo endereço recebe o seu contato — o Zion Ecosystem cresce por parceiros locais.'))
s.append(body('Municípios são atendidos por ordem de assinatura do protocolo. A agenda de diagnósticos é limitada pela capacidade da equipe técnica — e a primeira cidade de cada região carrega, para sempre, o título de pioneira.'))
s.append(PageBreak())

# ══════════ FONTES E REFERÊNCIAS ══════════════════════════════════
s += [sp(4), lb('Fontes e referências'), gl(), sp(3)]
s.append(h1('De Onde Vêm os Números'))
s.append(sp(2))
s.append(body('Todos os dados de mercado e de regulação citados neste volume são públicos e verificáveis. As principais fontes, para a equipe técnica conferir e aprofundar:'))
s.append(sp(3))
fontes_l = [
 ('Legislação', 'Lei 12.305/2010 (PNRS) · Lei 14.026/2020 (Marco do Saneamento) · Decreto 11.413/2023 (CCRLR) · Lei 15.042/2024 (SBCE) — todas no portal do Planalto.'),
 ('Fundo Clima / BNDES', 'Condições, subprogramas e teto por beneficiário no portal do BNDES; anúncio das taxas de 1% a 8% a.a. na Agência Brasil (2024); primeiro aporte em resíduos urbanos noticiado em 2025.'),
 ('Finep', 'Chamada pública Mais Inovação — Economia Circular e Cidades Sustentáveis: valores, faixas de TRL e prazos no portal finep.gov.br.'),
 ('Novo PAC Seleções', 'Eixo de resíduos sólidos: carteiras, municípios contratados e ciclos de seleção nos portais do Ministério das Cidades e da Casa Civil.'),
 ('FNMA / MMA', 'Editais de compostagem e gestão de resíduos no portal do MMA e no SINIR+.'),
 ('Caso Orizon', 'Resultados trimestrais e anuais no site de RI (ri.orizonvr.com.br); operação de créditos com o Google e histórico da companhia na imprensa financeira (Brazil Journal, Exame, InfoMoney, Seu Dinheiro).'),
 ('Panorama setorial', 'Geração per capita, composição gravimétrica e cobertura de coleta nos panoramas da Abrema e no SNIS/SINISA.'),
]
for t, d in fontes_l:
    s.append(h3(t))
    s.append(Paragraph(d, S('fnt',fontSize=9.5,textColor=GRAY,leading=15,spaceAfter=6,alignment=TA_JUSTIFY)))
s.append(sp(2))
s.append(Paragraph('Valores de editais, taxas e condições mudam a cada ciclo. Antes de qualquer decisão formal, confirme os números nos instrumentos convocatórios vigentes — e exija o mesmo de qualquer proposta que chegar à sua mesa.', S('fnt2',fontName='Helvetica-Oblique',fontSize=9,textColor=LGRAY,leading=14,spaceAfter=0)))
s.append(PageBreak())

# ══════════ TEASER + CONTRACAPA ═══════════════════════════════════
s.append(sp(14))
s.append(Paragraph('Z I O N', S('zc',fontName='Helvetica-Bold',fontSize=24,textColor=DARK,alignment=TA_CENTER,leading=30,spaceAfter=3)))
s.append(Paragraph('E C O S Y S T E M', S('ze',fontSize=11,textColor=GOLD,alignment=TA_CENTER,leading=15,spaceAfter=0)))
s.append(sp(8))
s.append(gl())
s.append(sp(5))
s.append(Paragraph('"Transformamos o lixo do seu município em patrimônio público.<br/>Estruturamos o projeto, captamos o recurso, entregamos a praça."',
    S('fr2',fontName='Helvetica-BoldOblique',fontSize=11,textColor=DARK,alignment=TA_CENTER,leading=18)))
s.append(sp(6))
s.append(Paragraph('"Fala comigo, prefeito!"',
    S('bo3',fontName='Helvetica-Bold',fontSize=16,textColor=GOLD,alignment=TA_CENTER)))
s.append(sp(8))
s.append(tl())
s.append(sp(3))
s.append(Paragraph('PRÓXIMO VOLUME DA SÉRIE ESPECIAL', S('tz1',fontName='Helvetica-Bold',fontSize=7.5,textColor=GOLD,alignment=TA_CENTER,spaceAfter=2)))
s.append(Paragraph('Consórcio Circular — Como Municípios Pequenos Somam Escala Industrial',
    S('tz2',fontName='Helvetica-Oblique',fontSize=10,textColor=GRAY,alignment=TA_CENTER,spaceAfter=0)))
s.append(sp(6))
s.append(tl())
s.append(sp(4))
s.append(Paragraph('Bruno Chaerk · CEO & Founder · Zion Hotel Group International × Ecogrupo',
    S('bc2',fontSize=9,textColor=LGRAY,alignment=TA_CENTER)))
s.append(Paragraph('Florianópolis (SC)  ·  Barcelona (España)', S('lc2',fontSize=8,textColor=GOLD,alignment=TA_CENTER)))
s.append(sp(3))
s.append(Paragraph('zionhotelgroup.com.br', S('ur2',fontName='Helvetica-Bold',fontSize=10,textColor=GOLD,alignment=TA_CENTER)))
s.append(sp(2))
s.append(Paragraph('© 2026 Zion Hotel Group International. Todos os direitos reservados.', ST['foot']))
s.append(Paragraph('Zion Ecosystem™ · CIRO™ · Selo Resíduo Zero by Zion™ · Diagnóstico Circular™ são marcas da Zion Hotel Group International Ltda.', ST['foot']))
s.append(Paragraph('Valores de editais e condições de financiamento citados devem ser confirmados nos instrumentos convocatórios vigentes.', ST['foot']))

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
    topMargin=22*mm, bottomMargin=20*mm)
doc.build(s, canvasmaker=ZionCanvas)

from pypdf import PdfReader
r = PdfReader(OUT)
print(f'PDF gerado: {len(r.pages)} páginas · {round(os.path.getsize(OUT)/1024,1)} KB')
print(OUT)

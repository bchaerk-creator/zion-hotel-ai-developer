#!/usr/bin/env python3
# BUSINESS PLAN PDF — ZION ECOSYSTEM BRASIL · identidade Zion (preto/dourado)
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Table, TableStyle)
from reportlab.pdfgen import canvas

GOLD, BLACK, DARK = colors.HexColor('#C9A84C'), colors.HexColor('#0A0A0A'), colors.HexColor('#1A1A1A')
CREAM, GRAY, LGRAY = colors.HexColor('#F5F0E8'), colors.HexColor('#4A4A4A'), colors.HexColor('#999999')
BGDARK, BGLIGHT = colors.HexColor('#0F0F0F'), colors.HexColor('#F8F5EF')
W, H = A4
AV = W - 40*mm
OUT = '/tmp/claude-0/-home-user-zion-hotel-ai-developer/5e61dba4-bdba-5d11-a3b8-8d9de78b22f5/scratchpad/Zion_Ecosystem_Brasil_Business_Plan.pdf'

class C(canvas.Canvas):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self._sv = []
    def showPage(self): self._sv.append(dict(self.__dict__)); self._startPage()
    def save(self):
        for st in self._sv:
            self.__dict__.update(st); self._ch(); canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    def _ch(self):
        if self._pageNumber == 1: return
        self.saveState()
        self.setStrokeColor(GOLD); self.setLineWidth(0.6)
        self.line(18*mm, H-15*mm, W-18*mm, H-15*mm)
        self.setFillColor(GOLD); self.setFont('Helvetica-Bold', 7)
        self.drawString(18*mm, H-13*mm, 'ZION ECOSYSTEM BRASIL')
        self.setFont('Helvetica', 7); self.setFillColor(LGRAY)
        self.drawRightString(W-18*mm, H-13*mm, 'BUSINESS PLAN  ·  v1.0  ·  2026')
        self.line(18*mm, 13*mm, W-18*mm, 13*mm)
        self.setFillColor(LGRAY); self.setFont('Helvetica', 7)
        self.drawString(18*mm, 8*mm, 'Zion Hotel Group International × Ecogrupo  ·  Confidencial')
        self.setFillColor(GOLD); self.setFont('Helvetica-Bold', 8)
        self.drawRightString(W-18*mm, 8*mm, str(self._pageNumber))
        self.restoreState()

def S(n, **kw):
    b = dict(fontName='Helvetica', fontSize=10, textColor=GRAY, leading=15.5, spaceAfter=7)
    b.update(kw); return ParagraphStyle(n, **b)

ST = {
 'label': S('lb', fontName='Helvetica-Bold', fontSize=7.5, textColor=GOLD, spaceAfter=3),
 'h1': S('h1', fontName='Helvetica-Bold', fontSize=20, textColor=DARK, spaceBefore=10, spaceAfter=5, leading=25),
 'h2': S('h2', fontName='Helvetica-Bold', fontSize=12.5, textColor=DARK, spaceBefore=10, spaceAfter=4, leading=16),
 'body': S('bd', alignment=TA_JUSTIFY),
 'hl': S('hl', fontName='Helvetica-Bold', fontSize=10.5, textColor=GOLD, alignment=TA_CENTER, leading=16, spaceAfter=8, spaceBefore=8),
 'kn': S('kn', fontName='Helvetica-Bold', fontSize=21, textColor=GOLD, alignment=TA_CENTER, leading=25, spaceAfter=1),
 'kl': S('kl', fontSize=7.6, textColor=CREAM, alignment=TA_CENTER, leading=11, spaceAfter=0),
 'foot': S('ft', fontSize=7, textColor=LGRAY, alignment=TA_CENTER, spaceAfter=2),
}

def gl(): return HRFlowable(width='100%', thickness=1.1, color=GOLD, spaceAfter=6, spaceBefore=6)
def sp(h=4): return Spacer(1, h*mm)
def lb(t): return Paragraph(t.upper(), ST['label'])
def h1(t): return Paragraph(t, ST['h1'])
def h2(t): return Paragraph(t, ST['h2'])
def body(t): return Paragraph(t, ST['body'])

def hl_box(t):
    tb = Table([[Paragraph(t, ST['hl'])]], colWidths=[AV])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BGDARK),
        ('TOPPADDING',(0,0),(-1,-1),11),('BOTTOMPADDING',(0,0),(-1,-1),11),
        ('LEFTPADDING',(0,0),(-1,-1),16),('RIGHTPADDING',(0,0),(-1,-1),16),
        ('LINEABOVE',(0,0),(-1,0),1.2,GOLD),('LINEBELOW',(0,-1),(-1,-1),1.2,GOLD)]))
    return tb

def tabela(dados, cw, fs=8.3, bold_col0=False):
    tb = Table(dados, colWidths=cw, repeatRows=1)
    style = [('FONTNAME',(0,0),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),fs),
        ('TEXTCOLOR',(0,0),(-1,-1),GRAY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),4.5),('BOTTOMPADDING',(0,0),(-1,-1),4.5),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
        ('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('LINEABOVE',(0,0),(-1,0),0.8,GOLD),('LINEBELOW',(0,0),(-1,0),0.8,GOLD),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,BGLIGHT])]
    if bold_col0: style.append(('FONTNAME',(0,1),(0,-1),'Helvetica-Bold'))
    tb.setStyle(TableStyle(style))
    return tb

def caixa(titulo, items):
    rows = [[Paragraph(f'<b>{titulo}</b>', S('cg',fontName='Helvetica-Bold',fontSize=9,textColor=GOLD,spaceAfter=0))]]
    for it in items:
        rows.append([Paragraph(f'  ▸  {it}', S('ci',fontSize=9,textColor=CREAM,leading=13.5,spaceAfter=0))])
    tb = Table(rows, colWidths=[AV])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLACK),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),13),('RIGHTPADDING',(0,0),(-1,-1),13),
        ('LINEABOVE',(0,0),(-1,0),0.8,GOLD),('LINEBELOW',(0,-1),(-1,-1),0.8,GOLD),
        ('LINEBEFORE',(0,0),(0,-1),0.8,GOLD),('LINEAFTER',(-1,0),(-1,-1),0.8,GOLD)]))
    return tb

def kpis(items):
    cards = []
    for num, desc in items:
        cards.append(Table([[Paragraph(num, ST['kn'])],[Paragraph(desc, ST['kl'])]],
            colWidths=[AV/len(items) - 12]))
    row = Table([cards], colWidths=[AV/len(items)]*len(items))
    row.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLACK),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#222222')),
        ('LINEABOVE',(0,0),(-1,0),0.8,GOLD),('LINEBELOW',(0,-1),(-1,-1),0.8,GOLD)]))
    return row

def secao(num, titulo):
    return [PageBreak(), sp(2), lb(f'Seção {num}'), gl(), sp(2), h1(titulo), sp(2)]

s = []

# ═══ CAPA ═══
cap = Table([
 [Paragraph('Z I O N', S('c1',fontName='Helvetica-Bold',fontSize=28,textColor=CREAM,alignment=TA_CENTER,leading=34,spaceAfter=3))],
 [Paragraph('E C O S Y S T E M &nbsp; B R A S I L', S('c2',fontSize=12,textColor=GOLD,alignment=TA_CENTER,leading=17,spaceAfter=0))],
 [Spacer(1, 18*mm)],
 [Paragraph('BUSINESS PLAN', S('c3',fontName='Helvetica-Bold',fontSize=34,textColor=GOLD,alignment=TA_CENTER,leading=40,spaceAfter=4))],
 [Paragraph('Industrialização de Resíduos Sólidos Urbanos<br/>com Engenharia de Créditos Ambientais', S('c4',fontSize=13,textColor=CREAM,alignment=TA_CENTER,leading=20,spaceAfter=0))],
 [Spacer(1, 12*mm)],
 [Paragraph('Da tonelada enterrada ao ativo industrializado:<br/>a plataforma que transforma o lixo brasileiro em produto, crédito e patrimônio público.',
    S('c5',fontName='Helvetica-Oblique',fontSize=10,textColor=LGRAY,alignment=TA_CENTER,leading=16,spaceAfter=0))],
 [Spacer(1, 20*mm)],
 [Paragraph('ZION HOTEL GROUP INTERNATIONAL  ×  ECOGRUPO', S('c6',fontName='Helvetica-Bold',fontSize=10,textColor=CREAM,alignment=TA_CENTER,spaceAfter=2))],
 [Paragraph('Bruno Chaerk · CEO', S('c7',fontSize=9,textColor=GOLD,alignment=TA_CENTER,spaceAfter=0))],
 [Spacer(1, 7*mm)],
 [Paragraph('VERSÃO 1.0 · AGOSTO 2026 · CONFIDENCIAL', S('c8',fontSize=7.5,textColor=LGRAY,alignment=TA_CENTER,spaceAfter=0))],
], colWidths=[AV-30])
cap.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),('ALIGN',(0,0),(-1,-1),'CENTER')]))
outer = Table([[cap]], colWidths=[AV], rowHeights=[H-62*mm])
outer.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLACK),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('LINEABOVE',(0,0),(-1,0),1.5,GOLD),('LINEBELOW',(0,-1),(-1,-1),1.5,GOLD),
    ('LINEBEFORE',(0,0),(0,-1),1.5,GOLD),('LINEAFTER',(-1,0),(-1,-1),1.5,GOLD)]))
s += [outer]

# ═══ 1. SUMÁRIO EXECUTIVO ═══
s += secao(1, 'Sumário Executivo')
s.append(body('A <b>Zion Ecosystem Brasil</b> é o veículo de entrada no mercado brasileiro da Ecogrupo — holding boliviano com 23 anos de operação em economia circular — sob estruturação, captação e marca da Zion Hotel Group International, sua representante oficial no país.'))
s.append(body('<b>O negócio:</b> implantar e operar complexos de industrialização de resíduos sólidos urbanos que transformam o lixo que municípios e concessionárias pagam para enterrar em sete linhas de receita: tarifa de tratamento (gate fee), produtos industrializados (madeira plástica, tubos, composto, CDR), créditos de reciclagem (CCRLR), créditos de carbono, energia, contratos B2B e licenciamento de marca.'))
s.append(body('<b>Por que agora:</b> o Brasil gera cerca de 80 milhões de toneladas de resíduos por ano e enterra quase tudo, a R$ 80–200 por tonelada. O marco legal construído entre 2010 e 2024 — PNRS, Marco do Saneamento, crédito de reciclagem (Decreto 11.413/2023) e mercado regulado de carbono (Lei 15.042/2024) — transformou a tonelada enterrada em ativo desperdiçado. A Orizon (B3: ORVR3) provou a tese em bolsa: R$ 7 bilhões de valor de mercado e 48% de margem EBITDA em megaescala. O flanco de municípios médios e aterros regionais está vago.'))
s.append(body('<b>Go-to-market em duas rotas:</b> (A) parcerias com concessionárias de aterro — que já têm concessão, fluxo e licença, e ganham industrialização, vida útil de célula e créditos; (B) contratos diretos com municípios e consórcios, pelo método comercial proprietário já estruturado.'))
s.append(sp(3))
s.append(kpis([('R$ 55M','CAPEX DA PLANTA<br/>DE REFERÊNCIA'),('34%','MARGEM EBITDA<br/>CASO-BASE (ANO 3)'),('2,5x','DSCR SEM CRÉDITOS<br/>DE CARBONO'),('18–24%','TIR ALAVANCADA<br/>DO PROJETO')]))
s.append(sp(4))
s.append(hl_box('O pedido: R$ 55 milhões para a primeira planta, em blended finance — 20–35% não reembolsável, 40–55% dívida subsidiada (Fundo Clima/BNDES, 16 anos), 15–30% equity e offtake de créditos como complemento.'))

# ═══ 2. VEÍCULO ═══
s += secao(2, 'A Empresa e o Veículo')
s.append(body('A estrutura societária isola o risco industrial, dá ao financiador um veículo dedicado e centraliza o ativo mais escalável da tese — os créditos ambientais:'))
s.append(sp(2))
s.append(tabela([
 ['Camada', 'Entidade', 'Papel'],
 ['Face pública', 'Bruno Chaerk', 'Autoridade, conteúdo, relações institucionais'],
 ['Sócios', 'Zion Hotel Group Int. × Ecogrupo Holding', 'Zion: estruturação, captação, marca, comercial · Ecogrupo: tecnologia, engenharia, operação (23 anos)'],
 ['Veículo', 'ZION ECOSYSTEM BRASIL LTDA', 'Representação master + operação Brasil'],
 ['Projetos', 'SPEs por praça', 'Rota A (JV com concessionária) e Rota B (contrato/PPP municipal)'],
 ['Créditos', 'Unidade de Créditos', 'Carteira agregada de CCRLR + carbono de todas as plantas'],
 ['Marca', 'Linha Resíduo Zero by Zion', 'Domos de glamping e produtos de material reciclado'],
], [AV*0.16, AV*0.34, AV*0.50]))
s.append(sp(3))
s.append(h2('Credenciais dos sócios'))
s.append(body('<b>Ecogrupo:</b> +300 t/mês processadas, +540 tCO2/mês mitigadas, +500 empregos, modelo Zero Waste em 5 municípios bolivianos, portfólio industrial completo (tubos, geoceldas, madeira plástica, casas, domos, hidroponia, proteína BSF, pirólise) e parcerias com 3 universidades. As operações brasileiras ainda não foram inauguradas — a primeira é o objeto deste plano.'))
s.append(body('<b>Zion:</b> developer de destinos com operação própria (Zion Bubble Glamping), captação estruturada via CVM 88 (ZION-01), base de 2.440 leads investidores, MOUs territoriais em SC e AL, métodos proprietários de venda e marca.'))

# ═══ 3. MERCADO ═══
s += secao(3, 'O Problema e o Mercado')
s.append(h2('O problema'))
s.append(body('Municípios e concessionárias pagam R$ 80–200/t para enterrar um material composto de ~50% orgânicos e ~30% recicláveis — mais de 80% da massa tem destino econômico melhor que o solo. Cerca de 2.900 municípios seguem com destinação irregular, sob risco de TAC e responsabilização pessoal dos gestores. E o aterro que recebe hoje perde, tonelada a tonelada, seu ativo mais valioso: a vida útil da célula. Nenhum player nacional oferece o pacote completo — separação, industrialização, créditos e contrapartida social visível.'))
s.append(h2('Dimensionamento'))
s.append(tabela([
 ['Camada', 'Definição', 'Dimensão'],
 ['TAM', 'Mercado brasileiro de manejo de RSU', '~80 M t/ano · R$ 25–35 bi/ano'],
 ['SAM', 'Municípios de 80–500 mil hab. + aterros regionais fora das capitais', '~25 M t/ano · R$ 6–9 bi/ano'],
 ['SOM (ano 5)', '5 plantas em operação (mix Rotas A e B)', '~500 mil t/ano · R$ 110–130 M/ano'],
], [AV*0.14, AV*0.52, AV*0.34], bold_col0=True))
s.append(sp(3))
s.append(caixa('VENTOS DE CAUDA REGULATÓRIOS E DE CAPITAL', [
 'SBCE (Lei 15.042/2024) em regulamentação — demanda compulsória por créditos vindo',
 'CCRLR ativo desde 2023 — receita recorrente por tonelada reciclada, mercado já operante',
 'Fundo Clima capitalizado com subprograma específico de resíduos (juros 1–8%, 16 anos)',
 'Novo PAC Seleções recorrente (~R$ 1 bi contratado com 543 municípios)',
 'Global Methane Pledge e agenda internacional de metano — grants e offtakes',
 'Benchmark de bolsa validado: Orizon ORVR3, R$ 7 bi, margem EBITDA 48%',
]))

# ═══ 4. SOLUÇÃO ═══
s += secao(4, 'A Solução — Dois Formatos de Planta')
s.append(body('A plataforma opera dois formatos complementares, cobrindo do consórcio de municípios pequenos à concessão metropolitana:'))
s.append(sp(2))
s.append(tabela([
 ['', 'CIRO Compacto', 'Complexo Industrial'],
 ['CAPEX', 'R$ 10 M', 'R$ 55 M (US$ 10 M)'],
 ['Capacidade', '40–60 t/dia', '250–400 t/dia'],
 ['Praça-alvo', 'Município/consórcio 80–150 mil hab.', 'Praça 300 mil+ hab. ou aterro concessionado'],
 ['Blocos', 'MRF simplificada + compostagem + madeira plástica', 'MRF completa + aterro misto c/ biogás + industrialização inorgânica + orgânica + energia'],
 ['Papel', 'Produto de entrada municipal (Rota B)', 'Planta de referência e de escala (Rota A)'],
], [AV*0.14, AV*0.38, AV*0.48], bold_col0=True))
s.append(sp(3))
s.append(h2('O pipeline padrão de cada praça (6 fases)'))
s.append(tabela([
 ['Fase', 'Entrega', 'Duração típica'],
 ['0 · Originação', 'Dossiê da praça: gatilho, decisor, volume', '2–4 semanas'],
 ['1 · Carta de intenções', 'Documento de 1 página, custo zero (NDA no B2B)', 'imediata'],
 ['2 · Estudo gravimétrico', '% orgânico, plásticos, metais etc. — vira baseline do carbono', '4–8 semanas'],
 ['3 · Estruturação jurídica', 'Contrato, JV, ou PMI→PPP (Lei 11.079 / Decreto 8.428)', '3–18 meses conforme rota'],
 ['4 · Implantação física', 'MRF + aterro misto → inorgânico → orgânico', '8–14 meses'],
 ['5 · Créditos e contrapartida', 'CCRLR + projeto de carbono + entregas ao território', 'desde o mês 1 de operação'],
], [AV*0.22, AV*0.52, AV*0.26]))
s.append(sp(3))
s.append(hl_box('Diferencial exclusivo: contrapartida contratual em patrimônio público — mobiliário, praças, casas, alimentos e energia devolvidos ao território, no modelo já praticado pela Ecogrupo. O produto político que nenhum concorrente entrega.'))

# ═══ 5. RECEITAS ═══
s += secao(5, 'Modelo de Receitas')
s.append(tabela([
 ['#', 'Receita', 'Cliente', 'Natureza'],
 ['1', 'Gate fee de tratamento', 'Município/consórcio ou concessionária', 'Contratual recorrente — âncora'],
 ['2', 'Produtos industrializados', 'Construção, agro, prefeituras, indústria', 'Venda B2B/B2G'],
 ['3', 'CCRLR — crédito de reciclagem', 'Indústrias obrigadas (logística reversa)', 'Recorrente por tonelada — mercado ativo'],
 ['4', 'Créditos de carbono', 'Voluntário hoje · SBCE/Art. 6 amanhã', 'Upside por tonelada (fora do caso-base)'],
 ['5', 'Energia · biogás · CDR', 'Autoconsumo, grid, cimenteiras', 'Venda de commodity'],
 ['6', 'B2B premium + selo Resíduo Zero', 'Hotéis, redes, grandes geradores', 'Recorrente + licenciamento'],
 ['7', 'Serviços de estruturação', 'Municípios (PMI/diagnósticos) e concessionárias', 'Fees de projeto'],
], [AV*0.05, AV*0.30, AV*0.36, AV*0.29]))
s.append(sp(3))
s.append(body('A força do modelo é o empilhamento: a mesma tonelada gera valor em até sete camadas, e nenhuma linha isolada representa mais de um terço da receita em regime. O aterro tradicional vive de uma única linha; a planta Zion Ecosystem, de sete.'))
s.append(h2('A engenharia de créditos (a camada que multiplica)'))
s.append(body('<b>Mercado voluntário (ativo já):</b> metano evitado por desvio de orgânicos e metano capturado no aterro misto. Certificação Verra/Gold Standard/Social Carbon. Preços 2026 na faixa geral de US$ 5–38/tCO2e; projetos de resíduos tipicamente US$ 6–15, com prêmio por co-benefícios sociais — que o modelo tem de sobra. Referência: desviar 100 t/dia de orgânicos gera 15–30 mil tCO2e/ano; a captura de biogás em aterro de grande porte multiplica por 5–20x.'))
s.append(body('<b>Mercado regulado (o vento de cauda):</b> SBCE em regulamentação criará demanda compulsória por CRVE; o Artigo 6 do Acordo de Paris (sucessor do MDL de Kyoto) abre a venda internacional premium com autorização do governo. <b>CCRLR:</b> receita-ponte imediata, sem espera regulatória. <b>Regra do caso-base:</b> a conta fecha sem carbono; o carbono acelera, nunca sustenta.'))

# ═══ 6. GO-TO-MARKET ═══
s += secao(6, 'Go-to-Market — As Duas Rotas')
s.append(h2('Rota A — Concessionárias de aterro (lidera a fase 1)'))
s.append(body('A proposta "industrialize sua concessão": reduzimos 60–80% do volume aterrado, alongamos a vida útil da célula (o maior ativo do concessionário), geramos produtos e créditos. Modelos: JV por planta, build-operate ou revenue share — sempre com licenciamento de tecnologia com trava e royalty por tonelada. Vantagens: velocidade (sem ciclo político), volume garantido, licença existente.'))
s.append(tabela([
 ['Região', 'Alvos prioritários (validar praça a praça)'],
 ['Nacional', 'Orizon · Solví/GRI/Essencis · Ambipar · Veolia'],
 ['SP', 'EcoUrbis · Loga · Corpus · Litucera · Tecipar · Sustentare'],
 ['RJ', 'Ciclus Ambiental (CTR Rio, ~10 mil t/dia)'],
 ['Sul', 'CRVR/Revita (RS) · operadores regionais SC/PR (base Zion)'],
 ['NE', 'Marquise Ambiental · Ecofor · regionais (MOU Zion em AL)'],
 ['CO/N', 'Operadores GO/DF (pipeline Ecogrupo) · Marquise (Manaus)'],
 ['Transversal', 'Consórcios públicos intermunicipais com aterro próprio'],
], [AV*0.16, AV*0.84], bold_col0=True))
s.append(sp(2))
s.append(h2('Rota B — Municípios e consórcios (escala na fase 2)'))
s.append(body('Método comercial documentado: secretário → prefeito → protocolo de intenções de custo zero → Diagnóstico Circular gratuito em 30 dias → contrato com gate fee abaixo do custo atual + contrapartida trimestral em patrimônio público → PMI/PPP quando a escala exigir. Gatilho de originação: contratos de destinação vencendo em 12–24 meses. Motor de demanda: ebook Cidade Circular, apresentações institucionais (ABREMA, CNM, Waste Expo), conteúdo do CEO e o efeito vitrine — prefeito vende para prefeito.'))
s.append(sp(2))
s.append(hl_box('Sequência estratégica: a Rota A entrega a primeira operação em velocidade; a Rota B escala com o case na mão. As duas convergem no mesmo veículo e na mesma engenharia de créditos.'))

# ═══ 7. VANTAGENS ═══
s += secao(7, 'Vantagens Competitivas')
s.append(caixa('POR QUE ESTA PLATAFORMA GANHA', [
 'Tecnologia validada por 23 anos (Ecogrupo), sem custo de P&D — com exclusividade Brasil',
 'Unidade de Créditos centralizada: volume agregado = melhor preço + offtakes viáveis',
 'Contrapartida social visível — o produto político que destrava contratos públicos',
 'Método comercial proprietário (ECROI) + face pública com autoridade construída',
 'Trilha de capital testada: CVM 88, linhas federais mapeadas, 2.440 leads investidores',
 'Sinergia hoteleira única: rede glamping como cliente, vitrine ESG e canal Resíduo Zero by Zion',
]))
s.append(sp(3))
s.append(body('A concorrência se divide em dois grupos que não se encontram: os grandes operadores de aterro (têm fluxo, não têm industrialização nem varejo político) e as recicladoras locais (têm vocação, não têm capital, método nem créditos). A plataforma ocupa exatamente o espaço entre os dois — e chega com o pacote completo.'))

# ═══ 8. FINANCEIRO ═══
s += secao(8, 'Plano Financeiro — Planta de Referência')
s.append(body('Premissas do caso-base: praça de 300 t/dia contratadas · gate fee R$ 170/t (abaixo dos ~R$ 200/t praticados por municípios de referência) · desvio de aterro de 65% em regime · <b>créditos de carbono fora do caso-base</b> · câmbio R$ 5,50.'))
s.append(h2('CAPEX — R$ 55 milhões'))
s.append(tabela([
 ['Bloco', 'R$ M'],
 ['MRF completa (balança, esteiras, triagem, prensas)', '14,0'],
 ['Aterro misto + captação de biogás', '8,0'],
 ['Industrialização inorgânica (extrusão, madeira plástica, CDR)', '13,0'],
 ['Industrialização orgânica (compostagem acelerada + biodigestor)', '9,0'],
 ['Infraestrutura, terreno e utilidades', '5,5'],
 ['Licenciamento, certificações e projeto de carbono', '1,5'],
 ['Capital de giro (18 meses)', '4,0'],
 ['Total', '55,0'],
], [AV*0.78, AV*0.22]))
s.append(PageBreak())
s.append(h2('DRE simplificada em regime (ano 3) — 3 cenários (R$ M/ano)'))
s.append(tabela([
 ['Linha', 'Conservador', 'Base', 'Otimista'],
 ['Volume · gate fee', '250 t/d · R$150', '300 t/d · R$170', '400 t/d · R$190'],
 ['Gate fee', '13,7', '18,6', '27,7'],
 ['Produtos industrializados', '3,5', '5,2', '8,5'],
 ['CCRLR', '0,9', '1,4', '2,2'],
 ['B2B / selo / serviços', '0,3', '0,5', '1,0'],
 ['Receita total (sem carbono)', '18,4', '25,7', '39,4'],
 ['OPEX total', '(13,3)', '(17,0)', '(24,4)'],
 ['EBITDA', '5,1 (28%)', '8,7 (34%)', '15,0 (38%)'],
 ['Carbono (upside líquido)', '+0,8', '+1,8', '+4,5'],
 ['EBITDA com carbono', '5,9', '10,5', '19,5'],
], [AV*0.37, AV*0.21, AV*0.21, AV*0.21], bold_col0=True))
s.append(sp(3))
s.append(h2('Rampa do caso-base (R$ M)'))
s.append(tabela([
 ['', 'Ano 1', 'Ano 2', 'Ano 3', 'Ano 4', 'Ano 5'],
 ['Receita', '8,5', '17,8', '25,7', '26,9', '28,2'],
 ['EBITDA', '(1,2)', '4,3', '8,7', '9,4', '10,1'],
], [AV*0.25, AV*0.15, AV*0.15, AV*0.15, AV*0.15, AV*0.15], bold_col0=True))
s.append(sp(3))
s.append(kpis([('2,5x','DSCR — DÍVIDA R$ 27M<br/>FUNDO CLIMA 16 ANOS'),('~7 anos','PAYBACK DESCONTADO<br/>SEM CARBONO'),('~5 anos','PAYBACK<br/>COM CARBONO'),('18–24%','TIR ALAVANCADA<br/>10 ANOS')]))
s.append(sp(4))
s.append(h2('Valuation de saída da plataforma'))
s.append(body('5 plantas em operação no ano 8 → EBITDA consolidado de R$ 45–60M → a múltiplos setoriais de 8–12x EV/EBITDA (a referência listada negocia acima disso) → <b>EV de R$ 400–700 milhões</b>. Rotas de saída: venda estratégica a player nacional/internacional, listagem (espelho ORVR3) ou securitização de recebíveis + dividendos.'))

# ═══ 9. CAPTAÇÃO ═══
s += secao(9, 'Captação — Uso e Fontes')
s.append(tabela([
 ['Fonte', 'R$ M', 'Camada'],
 ['Finep Economia Circular (crédito + subvenção) — prazo 31/08/2026', '8–12', 'Não reembolsável / subsidiado'],
 ['FNMA + Novo PAC (via município parceiro — infra da ponta)', '4–6', 'Não reembolsável'],
 ['Fundo Clima / BNDES — subprograma resíduos', '25–30', 'Dívida 16 anos, juros 1–8% a.a.'],
 ['Equity (Zion + Ecogrupo + parceiro da praça + fundo de impacto)', '10–15', 'Capital'],
 ['Offtake de créditos (venda antecipada carbono/CCRLR)', '3–5', 'Receita antecipada'],
 ['Total', '~55', ''],
], [AV*0.56, AV*0.14, AV*0.30]))
s.append(sp(3))
s.append(body('<b>Nota de realismo:</b> não existe instrumento único de 60% a fundo perdido para planta industrial privada no Brasil. A estrutura acima entrega 20–35% de equivalente-subvenção combinando fontes — e a dívida a juro fortemente subsidiado funciona, em valor presente, como subsídio adicional. Quando a planta entra por PPP administrativa, a contraprestação pública cumpre papel análogo ao garantir a receita.'))
s.append(body('<b>Fontes de escala (plantas 2–5):</b> BNDES Finem, debêntures incentivadas (Lei 12.431), BID Invest, IFC, GCF via entidades acreditadas (BNDES/Funbio/CAF), DFIs europeus (DEG, Proparco, FMO) e securitização dos recebíveis municipais (CRA verde).'))
s.append(sp(2))
s.append(hl_box('Marco imediato: chamada Finep Mais Inovação — Economia Circular, submissão até 31/08/2026, com a Ecogrupo como parceira tecnológica e ICT brasileira no projeto cooperado.'))

# ═══ 10. RISCOS ═══
s += secao(10, 'Riscos e Antídotos')
s.append(tabela([
 ['Risco', 'Antídoto'],
 ['Dispersão comercial (a lição Haztec)', 'Uma praça-piloto decidida no dia 90; tudo subordinado a ela até a inauguração'],
 ['Conta dependente de carbono', 'Carbono fora do caso-base por regra; DSCR 2,5x sem ele'],
 ['Ciclo político municipal', 'Rota A lidera (contraparte privada); na B, contratos formalizados + contrapartida trimestral'],
 ['Concessionária internaliza a tecnologia', 'Licenciamento com trava, royalty por tonelada, evolução contínua vinda da Ecogrupo'],
 ['Câmbio / importação de equipamentos', 'Fabricação local licenciada; importar máquina-chave, não produto'],
 ['Contaminação da coleta', 'Programa educacional (escolas + FNMA) com meta contratual < 15%'],
 ['Exclusividade Ecogrupo mal calibrada', 'Metas progressivas revisadas por comitê 2×2'],
 ['Licenciamento ambiental atrasa', 'Rota A usa licenças existentes; na B, licenciamento em paralelo ao jurídico'],
], [AV*0.42, AV*0.58]))

# ═══ 11. EQUIPE ═══
s += secao(11, 'Equipe e Governança')
s.append(body('<b>Bruno Chaerk (CEO):</b> estruturação, captação, institucional e marca. Background nas redes Meliá, Barceló e Wyndham; developer hoteleiro com operação própria e captação estruturada via CVM 88.'))
s.append(body('<b>Diretoria técnica Ecogrupo:</b> 23 anos de engenharia e operação de plantas de valorização de resíduos na Bolívia; responsável pela tecnologia, dimensionamento e operação das plantas brasileiras.'))
s.append(body('<b>Governança:</b> comitê da parceria 2×2 (Zion/Ecogrupo), plano anual conjunto, dados operacionais compartilhados — a base dos créditos e da transparência pública contratual.'))
s.append(body('<b>Contratações previstas com a captação:</b> diretor de operações Brasil, gerente de créditos ambientais e jurídico regulatório (infraestrutura/PPP). <b>Conselho consultivo (alvo):</b> um nome sênior do setor de resíduos, um de mercado de carbono e um de relações governamentais.'))

# ═══ 12. ROADMAP ═══
s += secao(12, 'Roadmap')
s.append(tabela([
 ['Horizonte', 'Marcos'],
 ['90 dias', 'Finep submetida (31/08) · MOU + veículo constituído · 20 alvos Rota A abordados (3 reuniões) · metodologia de carbono definida com certificadora · praça-piloto decidida'],
 ['12 meses', 'Contrato da praça-piloto assinado · captação da planta 1 estruturada · licenciamento em curso · piloto de coleta e educação ativo'],
 ['24 meses', 'Planta 1 inaugurada (primeira operação Ecogrupo no Brasil) · primeiros créditos registrados · primeira contrapartida entregue · praças 2 e 3 em contrato'],
 ['5 anos', '5 plantas · ~500 mil t/ano · Unidade de Créditos com carteira agregada · securitização estruturada'],
 ['8 anos', 'Plataforma nacional · EBITDA R$ 45–60M · evento de liquidez (venda estratégica ou listagem)'],
], [AV*0.14, AV*0.86], bold_col0=True))
s.append(sp(4))
s.append(hl_box('Em 24 meses, a primeira planta inaugurada. Em 8 anos, uma plataforma nacional com valuation de R$ 400–700 milhões. O primeiro passo custa uma assinatura: o MOU da representação e a proposta Finep de 31 de agosto.'))
s.append(sp(6))
s.append(gl())
s.append(sp(3))
s.append(Paragraph('ZION ECOSYSTEM BRASIL', S('f1',fontName='Helvetica-Bold',fontSize=13,textColor=DARK,alignment=TA_CENTER,spaceAfter=2)))
s.append(Paragraph('Zion Hotel Group International × Ecogrupo · Bruno Chaerk, CEO · zionhotelgroup.com.br', S('f2',fontSize=9,textColor=GOLD,alignment=TA_CENTER,spaceAfter=6)))
s.append(Paragraph('Projeções são estimativas gerenciais sujeitas a validação por estudo de viabilidade da praça específica. Valores de editais, linhas de crédito e preços de créditos ambientais devem ser confirmados nos instrumentos vigentes. Documento confidencial da parceria Zion × Ecogrupo — proibida reprodução sem autorização.', ST['foot']))

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=22*mm, bottomMargin=20*mm)
doc.build(s, canvasmaker=C)
from pypdf import PdfReader
print(f'BP: {len(PdfReader(OUT).pages)} páginas · {round(os.path.getsize(OUT)/1024,1)} KB')

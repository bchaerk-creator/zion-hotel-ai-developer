#!/usr/bin/env python3
# TEASER 2 PÁGINAS — ZION ECOSYSTEM BRASIL · para abrir portas de fundos
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
AV = W - 32*mm
OUT = '/tmp/claude-0/-home-user-zion-hotel-ai-developer/5e61dba4-bdba-5d11-a3b8-8d9de78b22f5/scratchpad/Zion_Ecosystem_Teaser_Investidor.pdf'

class C(canvas.Canvas):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self._sv = []
    def showPage(self): self._sv.append(dict(self.__dict__)); self._startPage()
    def save(self):
        for st in self._sv:
            self.__dict__.update(st); self._ch(); canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    def _ch(self):
        self.saveState()
        self.setStrokeColor(GOLD); self.setLineWidth(0.6)
        self.line(14*mm, H-12*mm, W-14*mm, H-12*mm)
        self.setFillColor(GOLD); self.setFont('Helvetica-Bold', 7)
        self.drawString(14*mm, H-10.2*mm, 'ZION ECOSYSTEM BRASIL')
        self.setFont('Helvetica', 7); self.setFillColor(LGRAY)
        self.drawRightString(W-14*mm, H-10.2*mm, 'TEASER CONFIDENCIAL  ·  AGOSTO 2026')
        self.line(14*mm, 10*mm, W-14*mm, 10*mm)
        self.setFillColor(LGRAY); self.setFont('Helvetica', 6.5)
        self.drawString(14*mm, 6*mm, 'Zion Hotel Group International × Ecogrupo · Distribuição restrita a investidores qualificados · Não constitui oferta pública de valores mobiliários')
        self.setFillColor(GOLD); self.setFont('Helvetica-Bold', 8)
        self.drawRightString(W-14*mm, 6*mm, str(self._pageNumber))
        self.restoreState()

def S(n, **kw):
    b = dict(fontName='Helvetica', fontSize=9.3, textColor=GRAY, leading=13.8, spaceAfter=5)
    b.update(kw); return ParagraphStyle(n, **b)

lb_s  = S('lb', fontName='Helvetica-Bold', fontSize=7.5, textColor=GOLD, spaceAfter=2)
h1_s  = S('h1', fontName='Helvetica-Bold', fontSize=19, textColor=DARK, spaceAfter=4, leading=23)
h2_s  = S('h2', fontName='Helvetica-Bold', fontSize=11, textColor=DARK, spaceBefore=7, spaceAfter=3)
bd    = S('bd', alignment=TA_JUSTIFY)
kn_s  = S('kn', fontName='Helvetica-Bold', fontSize=17, textColor=GOLD, alignment=TA_CENTER, leading=20, spaceAfter=1)
kl_s  = S('kl', fontSize=6.8, textColor=CREAM, alignment=TA_CENTER, leading=9.5, spaceAfter=0)

def gl(): return HRFlowable(width='100%', thickness=1.1, color=GOLD, spaceAfter=4, spaceBefore=4)
def sp(h=3): return Spacer(1, h*mm)

def kpis(items):
    cards = [Table([[Paragraph(n, kn_s)],[Paragraph(d, kl_s)]], colWidths=[AV/len(items)-10]) for n, d in items]
    row = Table([cards], colWidths=[AV/len(items)]*len(items))
    row.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLACK),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#222222')),
        ('LINEABOVE',(0,0),(-1,0),0.8,GOLD),('LINEBELOW',(0,-1),(-1,-1),0.8,GOLD)]))
    return row

def tab(dados, cw, fs=8.2, bold0=True):
    tb = Table(dados, colWidths=cw)
    st = [('FONTNAME',(0,0),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),fs),
        ('TEXTCOLOR',(0,0),(-1,-1),GRAY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),3.6),('BOTTOMPADDING',(0,0),(-1,-1),3.6),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
        ('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('LINEABOVE',(0,0),(-1,0),0.8,GOLD),('LINEBELOW',(0,0),(-1,0),0.8,GOLD),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,BGLIGHT])]
    if bold0: st.append(('FONTNAME',(0,1),(0,-1),'Helvetica-Bold'))
    tb.setStyle(TableStyle(st))
    return tb

def hl(t):
    tb = Table([[Paragraph(t, S('hl',fontName='Helvetica-Bold',fontSize=9.5,textColor=GOLD,alignment=TA_CENTER,leading=14,spaceAfter=0))]], colWidths=[AV])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BGDARK),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
        ('LINEABOVE',(0,0),(-1,0),1.1,GOLD),('LINEBELOW',(0,-1),(-1,-1),1.1,GOLD)]))
    return tb

s = []

# ══════════ PÁGINA 1 — A OPORTUNIDADE ══════════
s.append(Paragraph('OPORTUNIDADE DE INVESTIMENTO · ECONOMIA CIRCULAR · BRASIL', lb_s))
s.append(gl())
s.append(Paragraph('O lixo brasileiro é um ativo de<br/>R$ 25 bilhões/ano enterrado por engano.', h1_s))
s.append(sp(1))
s.append(Paragraph('A <b>Zion Ecosystem Brasil</b> traz ao país a tecnologia do maior grupo de economia circular da Bolívia — <b>Ecogrupo, 23 anos de operação, +500 empregos</b> — para industrializar resíduos sólidos urbanos: o material que municípios e concessionárias pagam R$ 80–200/tonelada para enterrar vira tubos, madeira plástica, composto, energia e créditos ambientais. A tese está validada em bolsa: a Orizon (B3: ORVR3) vale <b>R$ 7 bilhões com 48% de margem EBITDA</b> operando megaescala nas capitais. O flanco inteiro de municípios médios e aterros regionais está vago — e é dele que este projeto toma posse.', bd))
s.append(sp(2))
s.append(kpis([('61,8%','TIR PROJETO<br/>10A, PÓS-IMPOSTO'),('~110%','TIR EQUITY<br/>ALAVANCADO'),('2,1 anos','PAYBACK<br/>FASE 1'),('R$ 16,3M','VPL @ SELIC 14%<br/>SOBRE R$ 4,5M'),('5,7x','vs SELIC<br/>EM 10 ANOS')]))
s.append(sp(3))
s.append(Paragraph('A máquina: tecnologia validada × plataforma brasileira', h2_s))
s.append(tab([
 ['ECOGRUPO (tecnologia)', 'ZION / BRUNO CHAERK (plataforma Brasil)'],
 ['23 anos de operação industrial na Bolívia', 'Originação de praças: aterros, concessionárias e municípios'],
 ['Modelo Zero Waste em 5 municípios · 300 t/mês', 'Captação estruturada (trilha CVM 88 testada · linhas BNDES/Finep mapeadas)'],
 ['Portfólio: MRF, tubos, madeira plástica, compostagem, pirólise', 'Estruturação jurídica (SPEs, PPP/PMI) · marca e método comercial proprietários'],
 ['Fases 1–2 com indicadores oficiais: TIR 99% (MRF) e 31% (industrialização)', 'Camada de créditos: CCRLR + carbono (voluntário → SBCE) — upside estruturado'],
], [AV*0.46, AV*0.54], bold0=False))
s.append(sp(3))
s.append(Paragraph('Por que agora (a janela regulatória)', h2_s))
s.append(Paragraph('<b>1.</b> Marco legal completo entre 2010–2024: PNRS (fim dos lixões obrigatório), crédito de reciclagem CCRLR (Decreto 11.413/2023, mercado ativo) e mercado regulado de carbono (Lei 15.042/2024, em regulamentação). <b>2.</b> Capital subsidiado disponível: Fundo Clima/BNDES com subprograma de resíduos (juros 1–9%, 16 anos) e chamada Finep de Economia Circular aberta. <b>3.</b> ~2.900 municípios irregulares sob pressão jurídica — demanda compulsória por solução.', bd))
s.append(sp(2))
s.append(hl('O modelo em uma frase: contrato de tratamento como recebível-âncora + venda de materiais + créditos ambientais — sobre um insumo que o fornecedor paga para entregar.'))
s.append(PageBreak())

# ══════════ PÁGINA 2 — A OFERTA ══════════
s.append(Paragraph('A OFERTA', lb_s))
s.append(gl())
s.append(Paragraph('Equity na SPE da praça-piloto, com de-risking desenhado.', h1_s))
s.append(sp(1))
s.append(tab([
 ['Termo', 'Condição'],
 ['Veículo', 'SPE da praça-piloto (investidor âncora: acesso à holding)'],
 ['Ticket Fase 1', 'R$ 2,0–2,5M de equity — 40–50% do CAPEX de R$ 4,5M; o restante em dívida subsidiada'],
 ['Ticket pacote (Fases 1+2)', 'R$ 8–12M de equity'],
 ['Instrumento', 'Equity ou mútuo conversível'],
 ['Retorno-alvo', 'TIR de equity 25–35% (caso-base do modelo: ~110%) · DSCR 9,8x'],
 ['Gatilho de desembolso', 'Contrato âncora de gate fee ASSINADO — o capital entra com o recebível na mão'],
 ['Governança', 'Assento no conselho da SPE · reporte trimestral · painel de dados em tempo real'],
 ['Saída', 'Recompra (ano 5–7) · venda estratégica · listagem da plataforma (espelho ORVR3)'],
], [AV*0.30, AV*0.70]))
s.append(sp(3))
s.append(Paragraph('Projeção do caso-base (Fase 1 · MRF 200 t/dia · R$ M)', h2_s))
s.append(tab([
 ['', 'Ano 1', 'Ano 2', 'Ano 3', 'Ano 5', 'Ano 10'],
 ['Receita', '7,7', '12,1', '13,7', '16,1', '19,6'],
 ['EBITDA (margem)', '1,6 (20%)', '4,6 (38%)', '6,0 (43%)', '7,7 (48%)', '9,4 (48%)'],
 ['Fluxo de caixa livre', '1,0', '3,0', '3,8', '4,9', '5,9'],
], [AV*0.30, AV*0.14, AV*0.14, AV*0.14, AV*0.14, AV*0.14]))
s.append(sp(1))
s.append(Paragraph('Premissas conservadoras: gate fee de R$ 130/t (mercado: R$ 150–200) · impostos 34% sem benefícios · carbono e Fase 2 FORA do caso-base. Sensibilidade: no piso duro de R$ 100/t, TIR ainda ~40%; breakeven em ~R$ 70/t (margem de segurança ~2x).', S('nt',fontSize=7.8,textColor=LGRAY,leading=11.5)))
s.append(sp(2))
s.append(Paragraph('Roadmap e uso dos recursos', h2_s))
s.append(tab([
 ['Marco', 'Prazo'],
 ['Contrato âncora da praça-piloto (pipeline: ES, GO, SC — 3 praças em conversa)', '6–12 meses'],
 ['Planta 1 inaugurada — primeira operação Ecogrupo no Brasil', '18–24 meses'],
 ['Fase 2 (industrialização de plásticos) na praça-piloto + praças 2 e 3', '24–36 meses'],
 ['Plataforma: 5 plantas · EBITDA R$ 45–60M · evento de liquidez', 'ano 8'],
], [AV*0.76, AV*0.24], bold0=False))
s.append(sp(3))
s.append(hl('Convite: visite a operação em Cochabamba. A fábrica existe, opera há 23 anos — este teaser é o resumo; o data room e a visita são a prova.'))
s.append(sp(4))
s.append(gl())
s.append(Paragraph('BRUNO CHAERK · CEO — Zion Ecosystem Brasil', S('ct1',fontName='Helvetica-Bold',fontSize=10,textColor=DARK,alignment=TA_CENTER,spaceAfter=1)))
s.append(Paragraph('Zion Hotel Group International × Ecogrupo · Florianópolis (SC) · zionhotelgroup.com.br', S('ct2',fontSize=8.5,textColor=GOLD,alignment=TA_CENTER,spaceAfter=3)))
s.append(Paragraph('Documento confidencial para investidores qualificados. Não constitui oferta pública. Projeções gerenciais sujeitas a estudo de viabilidade por praça; retornos passados e projetados não garantem resultados futuros.', S('dsc',fontSize=6.8,textColor=LGRAY,alignment=TA_CENTER,leading=9.5,spaceAfter=0)))

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=16*mm, rightMargin=16*mm, topMargin=18*mm, bottomMargin=16*mm)
doc.build(s, canvasmaker=C)
from pypdf import PdfReader
print(f'Teaser: {len(PdfReader(OUT).pages)} páginas · {round(os.path.getsize(OUT)/1024,1)} KB')

# -*- coding: utf-8 -*-
"""
ZION ARCHITECTURAL PRODUCT BOOK · dados de engenharia de produto
Lista de peças ferro por ferro, conexões, BOM com preços de referência (Santa Catarina, set/2026),
mão de obra, cenários de orçamento, escala industrial e manual de montagem.
Todos os dimensionamentos são PRÉ-DIMENSIONAMENTO de engenharia (a validar por engenheiro estrutural habilitado).
"""
import math
from geometry import Cocoon, Zenith
from bom import KG, cocoon_bom, zenith_bom, ASSEMBLY

C, Z = Cocoon(), Zenith()
BC, BZ = cocoon_bom(), zenith_bom()

def r(v, n=0):
    return round(v, n) if n else int(round(v))

# =============================================================================
# 1. PEÇAS · ZION COCOON (ferro por ferro)
# =============================================================================
def cocoon_parts():
    """Cada peça: cod, nome, qtd, comp (m), larg (mm), alt (mm), perfil, aco, esp (mm), peso_un (kg), fabricacao, uniao, ordem."""
    P = []
    def add(cod, nome, qtd, comp, larg, alt, perfil, aco, esp, peso_un, fab, uniao, ordem, funcao):
        P.append(dict(cod=cod, nome=nome, qtd=qtd, comp=comp, larg=larg, alt=alt, perfil=perfil, aco=aco, esp=esp,
                      peso_un=round(peso_un, 1), peso_total=round(peso_un * qtd, 1), fab=fab, uniao=uniao, ordem=ordem, funcao=funcao))
    U = KG["U 150 x 60 x 3,0"]
    # ---- A · BASE (quadro do deck e trilhos) ----
    add("A01", "Viga longitudinal L1 a L5, trecho frontal (deck)", 5, 4.60, 150, 60, "U enrijecido 150 x 60 x 3,0", "ZAR-230 galv. Z275", 3.0, 4.6 * U, "Corte + furação Ø14", "Parafusada aos cabeçotes F02 e às transversais A02 (cantoneira D07)", 3, "Recebe o deck frontal e a fachada")
    add("A02", "Viga longitudinal L1 a L5, trecho da concha", 5, 4.30, 150, 60, "U enrijecido 150 x 60 x 3,0", "ZAR-230 galv. Z275", 3.0, 4.3 * U, "Corte + furação Ø14", "Emenda com A01 por D06 + 4 M12; apoio em F02", 3, "Vigas principais sob o piso interno")
    add("A03", "Viga longitudinal L1 a L5, trecho da cauda", 5, 4.30, 150, 60, "U enrijecido 150 x 60 x 3,0", "ZAR-230 galv. Z275", 3.0, 4.3 * U, "Corte + furação Ø14", "Emenda com A02 por D06 + 4 M12", 3, "Vigas principais sob banho e cauda")
    add("A04", "Viga transversal T1 a T10", 10, 6.50, 150, 60, "U enrijecido 150 x 60 x 3,0", "ZAR-230 galv. Z275", 3.0, 6.5 * U, "Corte + furação Ø14", "Cantoneira D07 + 4 M12 em cada cruzamento", 3, "Fecham a grelha 1,30 x 1,20 m")
    add("A05", "Viga de borda curva esquerda (trecho 1/2/3)", 3, 3.00, 150, 60, "U 150 x 60 x 3,0 calandrado em planta", "ZAR-230 galv. Z275", 3.0, 3.0 * U, "Calandra de perfil + furação", "Emenda D06; recebe as chapas D01 dos arcos", 3, "Contorno do piso e apoio dos arcos")
    add("A06", "Viga de borda curva direita (trecho 1/2/3)", 3, 3.00, 150, 60, "U 150 x 60 x 3,0 calandrado em planta", "ZAR-230 galv. Z275", 3.0, 3.0 * U, "Calandra de perfil + furação", "Idem A05", 3, "Idem A05")
    add("A07", "Trilho de base esquerdo (bolsa da membrana + calha)", 3, 3.00, 100, 50, "Tubo retangular 100 x 50 x 3,0 calandrado", "ASTM A500 Gr. B galv.", 3.0, 3.0 * KG["100 x 50 x 3,0"], "Calandra + furação Ø11 @600", "Parafuso M10 @600 na viga de borda A05", 5, "Fixa a borda inferior da membrana e a calha oculta")
    add("A08", "Trilho de base direito", 3, 3.00, 100, 50, "Tubo retangular 100 x 50 x 3,0 calandrado", "ASTM A500 Gr. B galv.", 3.0, 3.0 * KG["100 x 50 x 3,0"], "Calandra + furação Ø11 @600", "Idem A07 em A06", 5, "Idem A07")
    add("A09", "Viga da cauda (fechamento do quadro)", 1, 2.10, 150, 60, "U 150 x 60 x 3,0 calandrado", "ZAR-230 galv. Z275", 3.0, 2.1 * U, "Calandra + furação", "Cantoneira D07 + M12", 3, "Fecha a grelha na ponta da cauda")
    # ---- B · ARCOS ----
    L = C.arch_lengths()
    k88 = KG["Ø88,9 x 3,6"]
    add("B00-E", "Anel frontal A0, metade esquerda (lábio inclinado 8°)", 1, round(L[0] / 2, 2), 0, 0, "Tubo Ø101,6 x 4,0 calandrado (elipse)", "ASTM A500 Gr. B galv.", 4.0, L[0] / 2 * KG["Ø101,6 x 4,0"], "Calandra CNC por gabarito + perfil de vidro soldado", "Luva D02 no topo (4 M12) + chapa D01 no pé (4 M16)", 6, "Beiral frontal e apoio da esquadria da fachada")
    add("B00-D", "Anel frontal A0, metade direita", 1, round(L[0] / 2, 2), 0, 0, "Tubo Ø101,6 x 4,0 calandrado (elipse)", "ASTM A500 Gr. B galv.", 4.0, L[0] / 2 * KG["Ø101,6 x 4,0"], "Idem", "Idem", 6, "Idem")
    for i in range(1, 8):
        li = L[i]
        add(f"B0{i}-E", f"Arco A{i}, perna esquerda", 1, round(li * 0.34, 2), 0, 0, "Tubo Ø88,9 x 3,6 calandrado (elipse)", "ASTM A500 Gr. B galv.", 3.6, li * 0.34 * k88, "Calandra CNC por gabarito; ponta com luva D02 soldada", "Luva D02 com 4 M12 8.8 + pino Ø6; pé com chapa D01 + 4 M16", 6, f"Pórtico elíptico A{i} (x = {C.ARCH_X[i]:.2f} m)")
        add(f"B0{i}-C", f"Arco A{i}, coroa (segmento superior)", 1, round(li * 0.32, 2), 0, 0, "Tubo Ø88,9 x 3,6 calandrado (elipse)", "ASTM A500 Gr. B galv.", 3.6, li * 0.32 * k88, "Calandra CNC; talões D03 das terças soldados", "Encaixa nas luvas D02 das duas pernas", 6, "Fecha o pórtico; recebe a Espinha de Luz (A1 a A5)")
        add(f"B0{i}-D", f"Arco A{i}, perna direita", 1, round(li * 0.34, 2), 0, 0, "Tubo Ø88,9 x 3,6 calandrado (elipse)", "ASTM A500 Gr. B galv.", 3.6, li * 0.34 * k88, "Idem perna esquerda", "Idem", 6, "Idem")
    add("B08", "Quadro da cauda (anel Ø60,3 + 3 barras radiais)", 1, 7.50, 0, 0, "Tubo Ø60,3 x 3,0", "ASTM A500 Gr. B galv.", 3.0, 7.5 * KG["Ø60,3 x 3,0"], "Solda em gabarito", "Chapa D01 (2) + luva D02 no arco A7", 6, "Fecha a ponta da cauda e ancora a tampa de membrana")
    # ---- C · TRAVAMENTOS ----
    add("C01", "Terça longitudinal, trecho de 1,20 m", 49, 1.20, 0, 0, "Tubo Ø48,3 x 3,0", "ASTM A500 Gr. B galv.", 3.0, 1.2 * KG["Ø48,3 x 3,0"] + 0.4, "Corte + ponteiras rosqueadas M16 soldadas nas duas pontas", "Rosca M16 no talão D03 + porca e contraporca", 7, "Travamento longitudinal dos arcos e apoio do isolamento")
    add("C02", "Terça longitudinal, trecho da cauda (1,10 e 0,85 m)", 14, 0.98, 0, 0, "Tubo Ø48,3 x 3,0", "ASTM A500 Gr. B galv.", 3.0, 0.98 * KG["Ø48,3 x 3,0"] + 0.4, "Idem", "Idem", 7, "Idem, entre A6, A7 e o quadro da cauda")
    add("C03", "Espinha de Luz (treliça plana 300 mm), 2 trechos de 2,35 m", 2, 2.35, 300, 0, "Banzos Ø42,4 x 3,0 + diagonais Ø26,9 x 2,6", "ASTM A500 Gr. B galv.", 3.0, 2.35 * 2 * KG["Ø42,4 x 3,0"] + 2.6 * KG["Ø26,9 x 2,6"] + 1.5, "Solda em gabarito; berços de vidro D08", "Berço D06 nas coroas A1 a A5 + 2 M12 cada", 7, "Apoia os 4 vidros da claraboia e trava a cumeeira")
    add("C04", "Cabo de contraventamento em X", 8, 6.00, 0, 0, "Cabo de aço inox AISI 316 Ø8 mm 7 x 19", "inox 316", 8.0, 6.0 * 0.26 + 0.6, "Terminais prensados com olhal", "Olhal D05 + manilha + esticador M12 inox", 7, "Resiste ao vento longitudinal nos vãos A0-A1 e A5-A6")
    # ---- D · CHAPAS E CONEXÕES ----
    add("D01", "Chapa de base dos arcos (200 x 150 x 10) com 2 enrijecedores", 18, 0.20, 150, 10, "Chapa A36 + enrijecedores 80 x 60 x 8", "ASTM A36 galv.", 10.0, 2.6, "Corte plasma + solda de fábrica no pé do arco", "4 chumbadores M16 8.8 na viga de borda", 6, "Engasta o arco no quadro do deck")
    add("D02", "Luva interna de emenda Ø76,1 x 200 (4 furos Ø13)", 16, 0.20, 0, 0, "Tubo Ø76,1 x 3,6", "ASTM A500 Gr. B galv.", 3.6, 0.2 * KG["Ø76,1 x 3,6"], "Corte + furação; soldada dentro da perna", "Encaixe macho-fêmea + 4 M12 8.8 + pino de segurança Ø6", 6, "Emenda de fábrica/campo entre perna e coroa")
    add("D03", "Talão de terça (chapa 8 mm com furo Ø17)", 56, 0.06, 40, 8, "Chapa A36", "ASTM A36 galv.", 8.0, 0.15, "Corte laser + solda de fábrica nos arcos", "Recebe a ponteira M16 das terças", 6, "Ponto de fixação das terças")
    add("D04", "Chapa de topo dos cabeçotes (150 x 150 x 8, 4 furos)", 46, 0.15, 150, 8, "Chapa A36", "ASTM A36 galv.", 8.0, 1.4, "Corte + furação (fornecida com o cabeçote)", "4 M12 8.8 na mesa da viga U", 2, "Liga a fundação ao quadro do deck")
    add("D05", "Olhal para cabo (chapa 10 mm, furo Ø14)", 8, 0.08, 50, 10, "Chapa A36", "ASTM A36 galv.", 10.0, 0.3, "Corte laser + solda de fábrica nos arcos", "Manilha inox", 6, "Ancoragem dos cabos em X")
    add("D06", "Chapa de emenda das vigas (120 x 140 x 6, 4 furos)", 20, 0.14, 120, 6, "Chapa A36", "ASTM A36 galv.", 6.0, 0.8, "Corte + furação", "4 M12 8.8 por face", 3, "Emenda das vigas longitudinais e de borda")
    add("D07", "Cantoneira de cruzamento 75 x 75 x 6 x 140", 60, 0.14, 75, 6, "Cantoneira laminada", "ASTM A36 galv.", 6.0, 0.9, "Corte + furação", "2 M12 em cada aba", 3, "Ligação viga transversal x longitudinal")
    add("D08", "Berço de vidro da espinha (chapa 5 mm dobrada + EPDM)", 8, 0.12, 60, 5, "Chapa A36 dobrada", "ASTM A36 galv.", 5.0, 0.25, "Corte + dobra + solda na treliça", "Vidro apoiado em EPDM + presilha inox M6", 12, "Apoio dos painéis de vidro da claraboia")
    # ---- E · SUPORTE DA MEMBRANA E ACABAMENTO ----
    add("E01", "Perfil duplo keder de alumínio (por arco, em 3 trechos)", 8, round(sum(L) / 8, 2), 70, 24, "Alumínio 6060-T5 extrudado, calandrado", "alumínio", 3.0, sum(L) / 8 * 0.9, "Extrusão + calandra", "Presilha inox E03 a cada 300 mm sobre o arco", 8, "Recebe o cordão keder dos painéis de membrana")
    add("E02", "Perfil de arremate de base com calha oculta 80 x 60", 6, 3.00, 80, 60, "Alumínio 6063 extrudado", "alumínio", 2.0, 3.0 * 1.6, "Extrusão + corte", "Parafuso inox M8 @400 no trilho A07/A08", 8, "Arremate inferior da membrana e drenagem")
    add("E03", "Presilha inox do keder (3 mm) + parafuso M8 x 30", 300, 0.04, 20, 3, "Inox 304", "inox 304", 3.0, 0.03, "Estampada", "M8 inox rosqueado em inserto no arco", 8, "Fixa o perfil keder ao arco")
    add("E04", "Trilho do forro tensionado (harpão) 40 x 20", 22, 3.00, 40, 20, "Alumínio 6063", "alumínio", 1.5, 3.0 * 0.35, "Extrusão + corte", "Rebite ou M6 no talão secundário das terças", 10, "Fixa o forro tensionado")
    add("E05", "Requadro da Janela Olho (madeira laminada, 220 mm)", 6, 1.60, 950, 220, "Lâminas de eucalipto colado", "madeira laminada", 220.0, 9.0, "Usinagem CNC 5 eixos + verniz", "Parafusos inox M8 nos anéis de reforço E06 + selante PU", 11, "Transição concha curva x vidro plano")
    add("E06", "Anel de reforço da janela (chapa 3 mm curvada)", 6, 4.20, 60, 3, "Chapa A36 curvada", "ASTM A36 galv.", 3.0, 6.0, "Corte laser + calandra + solda nas terças", "Solda de fábrica", 6, "Distribui a tensão da membrana ao redor do Olho")
    add("E07", "Anel de alumínio da fachada 120 x 60 (2 metades)", 2, 5.10, 120, 60, "Alumínio 6063-T6 calandrado", "alumínio", 2.5, 5.1 * 2.5, "Calandra + usinagem", "Parafuso M8 @400 + fita EPDM sobre o anel B00", 11, "Base da esquadria da fachada inclinada")
    # ---- F · FUNDAÇÃO ----
    add("F01", "Estaca helicoidal Ø76 x 3,6, hélice Ø300, L 2,0 m", 46, 2.00, 300, 0, "Tubo Ø76,1 x 3,6 + hélice chapa 8 mm", "ASTM A500 / A36 galv.", 3.6, 2.0 * KG["Ø76,1 x 3,6"] + 5.5, "Solda da hélice + galvanização (compra)", "Rosca M30 do cabeçote F02", 1, "Fundação removível sem escavação")
    add("F02", "Cabeçote ajustável rosqueado (curso 150 mm) + chapa D04", 46, 0.25, 150, 8, "Barra roscada M30 + chapa", "aço galv.", 8.0, 2.2, "Compra", "Rosca M30 + contraporca; 4 M12 na viga", 2, "Nivelamento fino do deck")
    return P

def zenith_parts():
    P = []
    def add(cod, nome, qtd, comp, larg, alt, perfil, aco, esp, peso_un, fab, uniao, ordem, funcao):
        P.append(dict(cod=cod, nome=nome, qtd=qtd, comp=comp, larg=larg, alt=alt, perfil=perfil, aco=aco, esp=esp,
                      peso_un=round(peso_un, 1), peso_total=round(peso_un * qtd, 1), fab=fab, uniao=uniao, ordem=ordem, funcao=funcao))
    U = KG["U 150 x 60 x 3,0"]
    add("A01", "Viga longitudinal L1 a L5, trecho do terraço", 5, 3.00, 150, 60, "U enrijecido 150 x 60 x 3,0", "ZAR-230 galv. Z275", 3.0, 3.0 * U, "Corte + furação Ø14", "Cabeçotes F02 + emenda D06", 3, "Grelha do terraço")
    add("A02", "Viga longitudinal L1 a L5, trecho do corpo (2 trechos de 4,75)", 10, 4.75, 150, 60, "U enrijecido 150 x 60 x 3,0", "ZAR-230 galv. Z275", 3.0, 4.75 * U, "Corte + furação Ø14", "Emenda D06 + 4 M12; cabeçotes F02", 3, "Vigas principais sob o corpo")
    add("A03", "Viga transversal T1 a T7", 7, 6.80, 150, 60, "U enrijecido 150 x 60 x 3,0", "ZAR-230 galv. Z275", 3.0, 6.8 * U, "Corte + furação", "Cantoneira D07 + 4 M12", 3, "Fecham a grelha 2,40 x 1,30 m")
    add("A04", "Viga de borda do corpo (perímetro 9,5 x 5,4, 6 trechos)", 6, 5.00, 150, 60, "U 150 x 60 x 3,0 (caixão duplo)", "ZAR-230 galv. Z275", 3.0, 5.0 * U * 2, "Corte + furação + solda dos caixões", "D06 + chapas de base dos pilares D01", 3, "Recebe pilares e painéis SIP")
    add("A05", "Viga da passarela lateral 0,80 m", 2, 4.75, 150, 60, "U 150 x 60 x 3,0", "ZAR-230 galv. Z275", 3.0, 4.75 * U, "Corte + furação", "D07", 3, "Passarela de chegada")
    add("A06", "Quadro da hidromassagem (reforço 1,9 x 1,9)", 1, 8.00, 150, 60, "U 150 x 60 x 3,0 duplo", "ZAR-230 galv. Z275", 3.0, 8.0 * U * 2, "Corte + solda", "D07 + 4 estacas próprias", 3, "Suporta 1,9 t de água + banhistas")
    add("B01", "Mastro principal M1", 1, 5.05, 0, 0, "Tubo Ø139,7 x 4,5", "ASTM A500 Gr. B galv.", 4.5, 5.05 * KG["Ø139,7 x 4,5"] + 4, "Corte + base articulada soldada + capitel usinado", "Pino Ø30 na base D09; capitel D10 com 3 M16 para a coroa", 6, "Compressão do cume principal (5,80 m)")
    add("B02", "Mastro secundário M2", 1, 4.00, 0, 0, "Tubo Ø114,3 x 4,0", "ASTM A500 Gr. B galv.", 4.0, 4.0 * KG["Ø114,3 x 4,0"] + 3, "Idem", "Idem", 6, "Compressão do cume secundário (4,60 m)")
    add("B03", "Coroa do Zênite: 3 braços Ø48,3 x 950 + anel Ø1.200", 1, 0.95, 1200, 80, "Tubo Ø48,3 x 3,0 + chapa 80 x 10 calandrada", "ASTM A500 / A36 galv.", 10.0, 3 * 0.95 * KG["Ø48,3 x 3,0"] + math.pi * 1.2 * KG["chapa 80 x 10"] + 6, "Solda em gabarito + usinagem do capitel", "Capitel D10: 3 M16 8.8; anel recebe clamp E05 e óculo", 6, "Sustenta o anel de cume liberando o centro para o vidro")
    add("B04", "Coroa do Respiro: 3 braços Ø48,3 x 700 + anel Ø700 + chaminé", 1, 0.70, 700, 80, "Tubo Ø48,3 x 3,0 + chapa 80 x 10", "ASTM A500 / A36 galv.", 10.0, 3 * 0.7 * KG["Ø48,3 x 3,0"] + math.pi * 0.7 * KG["chapa 80 x 10"] + 8, "Idem + veneziana de alumínio", "Idem", 6, "Anel do cume 2 com chaminé de ventilação")
    add("B05", "Pilar do corpo P1 a P10", 10, 2.90, 0, 0, "Tubo Ø101,6 x 4,0", "ASTM A500 Gr. B galv.", 4.0, 2.9 * KG["Ø101,6 x 4,0"] + 2.5, "Corte + chapas de topo e base soldadas", "Base D01 (4 M16) na viga de borda; topo D11 (4 M16) no anel VB", 5, "Apoio do anel de beiral; embutido nos painéis")
    add("C01", "Segmento do anel de beiral VB01 a VB06 (4,75 / 2,70 m)", 6, 4.97, 150, 100, "Tubo retangular 150 x 100 x 4,0", "ASTM A500 Gr. B galv.", 4.0, 4.97 * KG["150 x 100 x 4,0"] + 3, "Corte + chapas de topo soldadas + perfil de borda", "Chapa de topo D12 com 4 M16 8.8 entre segmentos; D11 nos pilares", 5, "Viga-anel comprimida pela membrana")
    add("C02", "Poste externo PE01 a PE07 (inclinado 8°)", 7, 2.80, 0, 0, "Tubo Ø76,1 x 3,6", "ASTM A500 Gr. B galv.", 3.6, 2.8 * KG["Ø76,1 x 3,6"] + 1.5, "Corte + base articulada + olhal soldado", "Pino Ø20 na base D13; olhal recebe chapa de canto D14", 7, "Suporte dos cantos da membrana em balanço")
    add("C03", "Cabo de borda Ø12 inox (4 trechos)", 4, 10.50, 0, 0, "Cabo inox AISI 316 Ø12 mm 7 x 19", "inox 316", 12.0, 10.5 * 0.6 + 1.2, "Terminais prensados", "Esticador M20 inox nas chapas de canto D14", 8, "Catenária das bordas da membrana")
    add("C04", "Estai do poste Ø10 inox", 7, 4.20, 0, 0, "Cabo inox AISI 316 Ø10 mm", "inox 316", 10.0, 4.2 * 0.42 + 0.9, "Terminais prensados", "Esticador M16 + olhal da estaca de tração F03", 7, "Equilibra o poste inclinado")
    add("C05", "Cabo de suspensão do forro Ø4 inox", 16, 3.50, 0, 0, "Cabo inox Ø4", "inox 316", 4.0, 0.3, "Terminais prensados", "Olhais nos braços das coroas e no anel VB", 10, "Suspende o forro isolado seguindo os cumes")
    add("D01", "Chapa de base dos pilares (200 x 200 x 10)", 10, 0.20, 200, 10, "Chapa A36", "ASTM A36 galv.", 10.0, 3.1, "Corte plasma + solda", "4 chumbadores M16 8.8 na viga de borda", 5, "Apoio dos pilares")
    add("D06", "Chapa de emenda das vigas (120 x 140 x 6)", 24, 0.14, 120, 6, "Chapa A36", "ASTM A36 galv.", 6.0, 0.8, "Corte + furação", "4 M12 por face", 3, "Emendas da grelha")
    add("D07", "Cantoneira de cruzamento 75 x 75 x 6 x 140", 50, 0.14, 75, 6, "Cantoneira laminada", "ASTM A36 galv.", 6.0, 0.9, "Corte + furação", "2 M12 por aba", 3, "Ligação das vigas")
    add("D09", "Base articulada do mastro (chapa 250 x 250 x 12 + orelhas + pino Ø30)", 2, 0.25, 250, 12, "Chapa A36 + pino SAE 1045", "ASTM A36 galv.", 12.0, 9.5, "Corte + solda + usinagem do pino", "4 chumbadores M20 na viga A02 reforçada", 6, "Permite içar o mastro girando pela base")
    add("D10", "Capitel usinado do mastro (disco Ø200 x 20 + 3 orelhas)", 2, 0.20, 200, 20, "Aço SAE 1020 usinado", "SAE 1020 galv.", 20.0, 6.8, "Torno + fresa + solda", "3 M16 8.8 para os braços da coroa", 6, "Nó superior do mastro")
    add("D11", "Chapa de topo do pilar (150 x 150 x 8)", 10, 0.15, 150, 8, "Chapa A36", "ASTM A36 galv.", 8.0, 1.4, "Corte + furação + solda", "4 M16 8.8 no anel de beiral", 5, "Liga o pilar ao anel")
    add("D12", "Chapa de topo dos segmentos do anel (150 x 180 x 10)", 12, 0.18, 150, 10, "Chapa A36", "ASTM A36 galv.", 10.0, 2.1, "Corte + furação + solda", "4 M16 8.8 entre segmentos", 5, "Emenda do anel de beiral")
    add("D13", "Base articulada do poste (chapa 150 x 150 x 10 + garfo + pino Ø20)", 7, 0.15, 150, 10, "Chapa A36 + pino inox", "ASTM A36 galv.", 10.0, 3.4, "Corte + solda", "4 M12 no cabeçote F02", 7, "Base rotulada do poste")
    add("D14", "Chapa de canto da membrana (inox 8 mm, 3 furos Ø18)", 7, 0.18, 120, 8, "Chapa inox 304", "inox 304", 8.0, 1.1, "Corte laser", "Olhal do poste + 2 esticadores + cinta", 8, "Nó de canto: cabo de borda + membrana + poste")
    add("E01", "Perfil de borda arredondado do beiral (alumínio 80 x 40) + calha", 8, 3.75, 80, 40, "Alumínio 6063 extrudado", "alumínio", 2.0, 3.75 * 1.6, "Extrusão + corte", "Parafuso inox M8 @400 no anel VB", 8, "Passagem suave da membrana sobre o anel; calha oculta")
    add("E02", "Perfil de clamp do anel de cume (alumínio 60 x 12, 2 metades)", 2, 3.80, 60, 12, "Alumínio 6063 usinado", "alumínio", 12.0, 3.8 * 1.2, "Usinagem", "M10 inox @150 no anel B03/B04 + EPDM", 8, "Fixa a membrana no anel de cume")
    add("E03", "Trilho do forro tensionado 40 x 20", 24, 3.00, 40, 20, "Alumínio 6063", "alumínio", 1.5, 3.0 * 0.35, "Extrusão + corte", "Rebite ou M6 nos painéis e anéis internos", 10, "Fixa o forro")
    add("E04", "Esquadria do óculo Ø1.200 com ruptura térmica", 1, 3.80, 1200, 80, "Alumínio 6063 calandrado + poliamida", "alumínio", 2.5, 12.0, "Calandra + usinagem", "M8 inox no anel + selante estrutural", 11, "Recebe a cúpula de vidro do Zênite")
    add("F01", "Estaca helicoidal Ø76, hélice Ø300, L 2,0 m (compressão)", 30, 2.00, 300, 0, "Tubo Ø76,1 x 3,6 + hélice 8 mm", "ASTM A500 / A36 galv.", 3.6, 2.0 * KG["Ø76,1 x 3,6"] + 5.5, "Compra", "Rosca M30 do cabeçote F02", 1, "Fundação do piso, terraço e passarela")
    add("F02", "Cabeçote ajustável + chapa D04", 37, 0.25, 150, 8, "Barra M30 + chapa", "aço galv.", 8.0, 2.2, "Compra", "M30 + 4 M12", 2, "Nivelamento")
    add("F03", "Estaca helicoidal de tração Ø76, hélice Ø300, L 2,5 m, cabeça com olhal", 7, 2.50, 300, 0, "Tubo Ø76,1 x 3,6 + hélice + olhal", "ASTM A500 / A36 galv.", 3.6, 2.5 * KG["Ø76,1 x 3,6"] + 6.5, "Compra + olhal soldado", "Esticador do estai C04", 1, "Ancoragem dos estais dos postes")
    return P

# =============================================================================
# 2. CONEXÕES
# =============================================================================
COCOON_CONNECTIONS = [
    ("CX01", "F01 estaca helicoidal", "F02 cabeçote ajustável", "Rosca M30 com contraporca", "Contraporca M30 zincada", 46, 2),
    ("CX02", "F02 cabeçote / chapa D04", "A01-A04 vigas U", "Chapa 150 x 150 x 8 parafusada na mesa da viga", "Parafuso M12 x 40 cl. 8.8 + porca + arruela lisa e de pressão", 184, 3),
    ("CX03", "A01/A02/A03 vigas longitudinais", "A01/A02/A03 (emendas)", "Chapa de emenda D06 dupla (uma por face da alma)", "Parafuso M12 x 40 cl. 8.8 (8 por emenda)", 80, 3),
    ("CX04", "A04 vigas transversais", "A01-A03 longitudinais", "Cantoneira D07 75 x 75 x 6 (2 por cruzamento)", "Parafuso M12 x 40 cl. 8.8 (4 por cruzamento)", 200, 3),
    ("CX05", "A05/A06 vigas de borda curvas", "A04 transversais", "Cantoneira D07 + chapa de emenda D06", "Parafuso M12 x 40 cl. 8.8", 48, 3),
    ("CX06", "D01 chapa de base (soldada ao arco)", "A05/A06 viga de borda", "Chapa 200 x 150 x 10 sobre a mesa da viga (furos oblongos 18 x 25 para ajuste)", "Chumbador / parafuso M16 x 60 cl. 8.8 + porca + arruela (4 por pé)", 72, 6),
    ("CX07", "B0x-E / B0x-D pernas", "B0x-C coroa", "Luva interna D02 Ø76,1 x 200: encaixe macho-fêmea com batente", "Parafuso M12 x 110 cl. 8.8 passante (4) + pino de segurança Ø6 x 100 com contrapino", 16, 6),
    ("CX08", "B00-E", "B00-D (anel frontal, topo)", "Luva D02 Ø88,9 x 220", "M12 x 120 cl. 8.8 (4) + pino Ø6", 1, 6),
    ("CX09", "C01/C02 terças", "D03 talão dos arcos", "Ponteira rosqueada M16 entra no furo Ø17 do talão", "Porca M16 + contraporca + arruela (2 conjuntos por terça)", 126, 7),
    ("CX10", "C03 espinha (treliça)", "B01-C a B05-C coroas", "Berço D06 soldado à coroa; treliça apoiada e aparafusada", "Parafuso M12 x 40 cl. 8.8 (2 por berço)", 10, 7),
    ("CX11", "C04 cabos em X", "D05 olhais dos arcos", "Manilha inox + esticador garfo-garfo", "Manilha 3/8 inox + esticador M12 inox (1 por cabo)", 16, 7),
    ("CX12", "E01 perfil keder", "B00-B07 arcos", "Presilha inox E03 abraçando o tubo", "Parafuso inox M8 x 30 em inserto rosqueado (a cada 300 mm)", 300, 8),
    ("CX13", "H01 painéis de membrana", "E01 perfil keder", "Cordão keder Ø8 deslizado no canal (dois canais por perfil)", "Sem fixador: encaixe por deslizamento + tampa de topo", 16, 8),
    ("CX14", "H01 membrana (bolsa inferior)", "A07/A08 trilho de base + E02 arremate", "Bolsa com tubo Ø20 presa por grampo do perfil E02", "Parafuso inox M8 x 40 @400 + arruela EPDM", 50, 8),
    ("CX15", "E07 anel de alumínio da fachada", "B00 anel frontal", "Perfil de alumínio sobre fita EPDM 3 mm, furação coincidente", "Parafuso inox M8 x 50 @400 + inserto", 26, 11),
    ("CX16", "V01 vidros da fachada / V02 porta", "E07 anel + montantes", "Esquadria com ruptura térmica; gaxetas EPDM; pivô de piso", "Kit de esquadria (fornecedor) + selante estrutural", 1, 11),
    ("CX17", "E05 requadro do Olho", "E06 anel de reforço", "Parafuso passante com bucha; selante PU perimetral", "Parafuso inox M8 x 80 (8 por janela)", 48, 11),
    ("CX18", "V04 vidros da espinha", "D08 berços", "Apoio em EPDM + presilha inox + selante silicone estrutural", "Presilha inox M6 (4 por vidro)", 16, 12),
    ("CX19", "H02/H03 isolamento", "C01 terças", "Manta apoiada na malha inox 25 x 25 fixada às terças", "Abraçadeira inox + arame 1,2 mm", 60, 9),
    ("CX20", "H04 forro tensionado", "E04 trilho harpão", "Harpão costurado no tecido pressionado no trilho", "Sem fixador", 7, 10),
    ("CX21", "G01 módulos de piso", "A01-A04 vigas", "Vigotas apoiadas na mesa; parafuso auto-brocante", "Parafuso auto-brocante 5,5 x 50 (6 por módulo)", 108, 4),
    ("CX22", "ZC-PW parede do banho", "G01 piso + B05 arco", "Guia LSF parafusada no piso; presilhas no arco", "Parafuso 4,8 x 32 + presilha M8 (4)", 30, 13),
]
ZENITH_CONNECTIONS = [
    ("CX01", "F01/F03 estacas", "F02 cabeçotes", "Rosca M30 com contraporca", "Contraporca M30", 37, 2),
    ("CX02", "F02 cabeçotes", "A01-A05 vigas U", "Chapa 150 x 150 x 8 na mesa da viga", "M12 x 40 cl. 8.8 (4 por cabeçote)", 148, 3),
    ("CX03", "A01/A02 vigas", "emendas", "Chapa D06 dupla", "M12 x 40 cl. 8.8 (8 por emenda)", 96, 3),
    ("CX04", "A03 transversais", "A01/A02 longitudinais", "Cantoneira D07", "M12 x 40 cl. 8.8 (4 por cruzamento)", 140, 3),
    ("CX05", "D01 chapa de base do pilar (soldada)", "A04 viga de borda", "Chapa 200 x 200 x 10 com furos oblongos", "Chumbador M16 x 60 cl. 8.8 (4 por pilar)", 40, 5),
    ("CX06", "B05 pilar / D11 chapa de topo", "C01 anel de beiral", "Chapa de topo sob o tubo retangular", "M16 x 60 cl. 8.8 (4 por pilar)", 40, 5),
    ("CX07", "C01 segmentos do anel", "C01 segmentos (emendas)", "Chapas de topo D12 face a face", "M16 x 60 cl. 8.8 (4 por emenda)", 24, 5),
    ("CX08", "D09 base articulada", "A02 viga reforçada", "Chapa 250 x 250 x 12 chumbada; mastro gira no pino", "Chumbador M20 x 80 cl. 8.8 (4 por base) + pino Ø30 com contrapino", 8, 6),
    ("CX09", "B01/B02 mastros (capitel D10)", "B03/B04 coroas", "Orelhas do capitel entre orelhas dos braços", "M16 x 70 cl. 8.8 (1 por braço, 3 por coroa) + contrapino", 6, 6),
    ("CX10", "C02 postes (D13 base)", "F02 cabeçote", "Garfo com pino Ø20 sobre chapa", "M12 x 40 (4) + pino inox Ø20 com contrapino", 28, 7),
    ("CX11", "C04 estais", "F03 estacas de tração", "Esticador garfo-olhal", "Esticador M16 inox + manilha 3/8", 7, 7),
    ("CX12", "C03 cabo de borda", "D14 chapas de canto", "Terminal com olhal prensado + esticador", "Esticador M20 inox (2 por chapa)", 14, 8),
    ("CX13", "H01 membrana (bolsa de borda)", "C03 cabo de borda", "Cabo passado na bolsa Ø32 soldada por RF", "Sem fixador (bolsa) + cinta de canto com catraca", 4, 8),
    ("CX14", "H01 membrana (anel de cume)", "B03/B04 anéis via E02 clamp", "Membrana prensada entre anel e clamp com EPDM", "M10 inox @150 (2 x 25 e 2 x 15)", 80, 8),
    ("CX15", "H01 membrana sobre o beiral", "E01 perfil de borda", "Passagem livre sobre perfil arredondado; fita antiatrito", "Sem fixador (deslizamento) + M8 do perfil no anel", 60, 8),
    ("CX16", "SIP painéis de parede", "B05 pilares + A04 viga de borda", "Rebaixo do painel abraça o pilar; guia inferior e superior", "Parafuso auto-brocante 5,5 x 75 @300 + espuma PU", 22, 9),
    ("CX17", "V01 fachada / V02 vidro lateral", "SIP / A04 / C01", "Esquadria com trilho embutido e contramarco", "Kit de esquadria + selante estrutural", 2, 11),
    ("CX18", "V03 óculo (E04 esquadria)", "B03 anel", "Esquadria calandrada sobre o anel + EPDM", "M8 inox @200 + selante", 1, 11),
    ("CX19", "H02 forro isolado", "C05 cabos + E03 trilhos", "Forro suspenso pelos cabos, harpão nos trilhos", "Terminais Ø4 + rebites", 16, 10),
    ("CX20", "ZZ-PW parede da cabeceira", "Piso + B01 mastro", "Guia LSF parafusada; abraçadeiras no mastro", "Parafuso 4,8 x 32 + abraçadeira M8 (3)", 20, 13),
]

# =============================================================================
# 3. PREÇOS DE REFERÊNCIA · SANTA CATARINA · set/2026 (R$)
#    (cod, descrição, unidade, preço STANDARD, fator ECONÔMICO, fator PREMIUM, nota)
# =============================================================================
PRICES = {
    "tubo": ("Tubo de aço carbono ASTM A500 / NBR 8261 (material, R$/kg)", "kg", 10.80, 0.92, 1.08, "Distribuidores SC (Joinville / Itajaí); lote > 1 t"),
    "perfilU": ("Perfil U enrijecido 150 x 60 x 3,0 galvanizado Z275 (R$/kg)", "kg", 12.90, 0.95, 1.05, "Perfil LSF pesado, pré-galvanizado"),
    "chapa": ("Chapa A36 / cantoneiras (R$/kg)", "kg", 9.60, 0.95, 1.05, "Corte plasma / laser incluído na fabricação"),
    "galv": ("Galvanização a fogo NBR 6323 (R$/kg)", "kg", 7.40, 0.0, 1.0, "Econômico: fundo epóxi + esmalte PU no lugar da galvanização"),
    "pintura": ("Pintura eletrostática a pó poliéster sobre galvanizado (R$/kg equiv.)", "kg", 4.90, 0.0, 1.15, "Econômico: sem pintura sobre galvanizado; Premium: cor especial bronze"),
    "epoxi": ("Pintura epóxi + PU (alternativa econômica, R$/kg)", "kg", 5.60, 1.0, 0.0, "Somente no cenário econômico"),
    "fixadores": ("Parafusos cl. 8.8 zincados, chumbadores, porcas, arruelas, pinos (kit)", "kit", 4200.0, 0.9, 1.15, "Premium: inox A2 nas conexões aparentes"),
    "inox_cabo8": ("Cabo inox 316 Ø8 + terminais (R$/m)", "m", 34.0, 0.85, 1.0, ""),
    "inox_cabo12": ("Cabo inox 316 Ø12 + terminais (R$/m)", "m", 58.0, 0.85, 1.0, ""),
    "esticador": ("Esticador inox M12 a M20 + manilha (un)", "un", 210.0, 0.8, 1.1, ""),
    "keder": ("Perfil duplo keder de alumínio calandrado (R$/m)", "m", 92.0, 0.9, 1.05, ""),
    "alu_perfil": ("Perfis de alumínio de arremate / clamp / trilhos (R$/m)", "m", 68.0, 0.9, 1.1, ""),
    "membrana": ("Membrana PVDF 1050 g/m² tipo III (material, R$/m²)", "m²", 215.0, 0.68, 1.45, "Econ.: PVC 900 g/m² laca acrílica; Premium: Précontraint PVDF importada"),
    "membrana_conf": ("Confecção da membrana: corte CNC, solda RF, keder, bolsas, form-finding (R$/m²)", "m²", 98.0, 0.9, 1.1, "Confeccionadores de tensoestruturas em SC/PR/SP"),
    "pet": ("Lã de PET 50 mm 25 kg/m³ (R$/m²)", "m²", 36.0, 0.85, 1.0, ""),
    "refletiva": ("Manta refletiva dupla face bolha 4 mm (R$/m²)", "m²", 17.0, 1.0, 1.0, ""),
    "malha": ("Malha inox / tela de apoio do isolamento (R$/m²)", "m²", 22.0, 0.8, 1.0, ""),
    "forro": ("Forro tensionado acústico Trevira CS instalado (R$/m²)", "m²", 265.0, 0.65, 1.3, "Econ.: tecido poliéster tensionado; Premium: acústico + painéis de madeira"),
    "sip": ("Painel SIP 100 mm OSB/PIR/OSB (R$/m²)", "m²", 285.0, 0.9, 1.1, "Zenith"),
    "cimenticia": ("Placa cimentícia 10 mm + membrana hidrófuga (R$/m²)", "m²", 96.0, 0.9, 1.05, "Zenith"),
    "ripado": ("Ripado de madeira termotratada 40 x 40 instalado (R$/m²)", "m²", 420.0, 0.7, 1.3, "Econ.: pinus autoclavado; Premium: cumaru"),
    "vidro_duplo": ("Vidro insulado 6 lam + 12 Ar + 6 temp low-e (R$/m²)", "m²", 920.0, 0.55, 1.25, "Econ.: laminado 8 mm simples"),
    "esquadria": ("Esquadria de alumínio com ruptura térmica, bronze, fabricada e instalada (R$/m² de vão)", "m²", 1480.0, 0.62, 1.45, "Econ.: linha 30 sem RPT; Premium: sistema europeu"),
    "porta_pivo": ("Porta pivotante de vidro 1,00 x 2,40 com pivô de piso (un)", "un", 9800.0, 0.7, 1.4, ""),
    "olho": ("Janela Olho: requadro laminado CNC + vidro duplo (un)", "un", 6900.0, 0.75, 1.3, "2 basculantes com ferragem"),
    "vidro_lam": ("Vidro laminado 8 + 8 mm para claraboia / óculo (R$/m²)", "m²", 1150.0, 0.85, 1.2, ""),
    "cupula": ("Cúpula de vidro laminado curvo Ø1,20 + vidro interno (un)", "un", 14500.0, 0.6, 1.3, "Zenith; Econ.: acrílico"),
    "cumaru": ("Deck cumaru 20 x 140 com fixação oculta (material, R$/m²)", "m²", 295.0, 0.65, 1.2, "Econ.: eucalipto autoclavado"),
    "vigota": ("Vigota pinus autoclavado 50 x 150 (R$/m)", "m", 23.0, 1.0, 1.15, ""),
    "pir": ("PIR 50 mm entre vigotas + manta inferior (R$/m²)", "m²", 82.0, 0.9, 1.0, ""),
    "compensado": ("Compensado naval 18 mm (R$/m²)", "m²", 168.0, 0.85, 1.0, ""),
    "piso_eng": ("Piso de engenharia carvalho 14 mm (R$/m²)", "m²", 430.0, 0.45, 1.4, "Econ.: laminado AC5; Premium: tábua larga"),
    "porcelanato": ("Zona molhada: placa cimentícia + impermeabilização + porcelanato (R$/m²)", "m²", 240.0, 0.75, 1.5, ""),
    "estaca": ("Estaca helicoidal Ø76 L 2,0 m + cabeçote ajustável (material, un)", "un", 640.0, 0.9, 1.05, "Fornecedores nacionais (SP/PR/SC)"),
    "estaca_inst": ("Instalação de estaca helicoidal com motor hidráulico (un)", "un", 270.0, 0.95, 1.0, "Inclui torque registrado"),
    "mobiliz": ("Mobilização do equipamento de cravação (verba)", "vb", 3800.0, 1.0, 1.0, "Por unidade isolada; diluída em série"),
    "loucas": ("Louças e metais (bacia, cuba, torneiras, chuveiro, acessórios)", "cj", 15500.0, 0.55, 1.9, "Econ.: linha nacional; Premium: Deca/Docol linhas premium ou importados"),
    "banheira": ("Banheira freestanding 1,60 / 1,70 m", "un", 9200.0, 0.5, 2.1, "Premium: pedra composta"),
    "box": ("Box de vidro temperado 8 mm com perfil bronze", "un", 2600.0, 0.8, 1.3, ""),
    "hidro": ("Hidromassagem Ø1,90 com filtro, bomba e aquecedor 3 kW (Zenith)", "un", 24000.0, 0.65, 1.7, ""),
    "pex": ("Kit hidráulico PEX 25/20, esgoto, ventilação, registros, conexões", "cj", 7200.0, 0.85, 1.15, ""),
    "aquecedor": ("Aquecedor a gás de passagem 23 L/min (Cocoon) / 30 L/min (Zenith)", "un", 4400.0, 0.75, 2.6, "Premium: bomba de calor 200/300 L"),
    "esgoto": ("Fossa séptica + filtro anaeróbio compactos (ou biodigestor)", "cj", 7400.0, 0.8, 1.6, "Premium: estação compacta com reúso"),
    "eletrica": ("Quadro, disjuntores, DR, cabos, eletrodutos, tomadas USB, interruptores", "cj", 9800.0, 0.8, 1.35, "Premium: automação de iluminação e cortinas"),
    "iluminacao": ("Iluminação: fitas LED 2700 K, perfis, drivers, luminárias, balizadores", "cj", 11800.0, 0.6, 1.6, ""),
    "ac": ("Ar-condicionado dutado inverter 12k (Cocoon) / 18k (Zenith), instalado", "un", 12400.0, 0.7, 1.35, "Econ.: hi-wall 12k; Premium: dutado com controle por app + piso radiante"),
    "exaustor": ("Exaustor com recuperador de calor + respiro / chaminé motorizada", "cj", 3900.0, 0.5, 1.4, ""),
    "marcenaria": ("Marcenaria sob medida (console, armários, criados, cabeceira, bancada)", "cj", 39000.0, 0.6, 1.5, "Cocoon; Zenith 52.000 (closet, Ilha do Café, bancada dupla)"),
    "mobiliario": ("Mobiliário solto (cama king + colchão, chaise, poltrona, mesas)", "cj", 22500.0, 0.55, 1.8, ""),
    "paineis": ("Painéis ripados internos / revestimentos (R$/m²)", "m²", 480.0, 0.6, 1.4, ""),
    "acab": ("Acabamentos: selantes, rodapés, cortinas, tapetes, enxoval de abertura", "cj", 13500.0, 0.6, 1.6, ""),
    "parede": ("Parede do banho / cabeceira em LSF + painéis (R$/m²)", "m²", 310.0, 0.8, 1.2, ""),
}

# mão de obra (R$/h, custo empresa com encargos, EPI e ferramental) · STANDARD, fator ECON, fator PREMIUM
LABOR_RATES = {
    "serralheiro": ("Serralheiro (corte, calandra, montagem em bancada)", 49.0, 0.88, 1.10),
    "soldador": ("Soldador qualificado (MIG/TIG, EPS)", 60.0, 0.88, 1.12),
    "montador": ("Montador de estruturas (campo)", 44.0, 0.9, 1.1),
    "lider": ("Líder de montagem / encarregado", 72.0, 0.9, 1.1),
    "carpinteiro": ("Carpinteiro (deck, piso, módulos)", 50.0, 0.9, 1.1),
    "eletricista": ("Eletricista", 64.0, 0.9, 1.1),
    "encanador": ("Encanador", 60.0, 0.9, 1.1),
    "vidraceiro": ("Vidraceiro / instalador de esquadrias", 62.0, 0.9, 1.1),
    "membrana": ("Instalador de membranas tensionadas (especializado)", 98.0, 0.9, 1.15),
    "marceneiro": ("Marceneiro (instalação)", 60.0, 0.9, 1.1),
    "acabamento": ("Equipe de acabamento / limpeza", 40.0, 0.9, 1.1),
    "engenheiro": ("Engenheiro (acompanhamento, ART, controle de qualidade)", 190.0, 0.9, 1.15),
}

def labor_hours(product):
    """horas por unidade por função (fabricação + instalação)"""
    if product == "cocoon":
        return {"serralheiro": 250, "soldador": 120, "montador": 4 * 12 * 8.8, "lider": 12 * 8.8, "carpinteiro": 130, "eletricista": 44, "encanador": 40,
                "vidraceiro": 48, "membrana": 56, "marceneiro": 28, "acabamento": 64, "engenheiro": 24}
    return {"serralheiro": 220, "soldador": 110, "montador": 4 * 15 * 8.8, "lider": 15 * 8.8, "carpinteiro": 150, "eletricista": 52, "encanador": 52,
            "vidraceiro": 64, "membrana": 72, "marceneiro": 36, "acabamento": 72, "engenheiro": 28}

# =============================================================================
# 4. BOM COM PREÇOS (18 grupos)
# =============================================================================
def bom_priced(product):
    """retorna lista de grupos: (nome, [(descrição, un, qtd, chave_preço, fator_qtd_extra)])"""
    if product == "cocoon":
        b = BC; P = cocoon_parts()
        steel_kg = sum(p["peso_total"] for p in P if p["cod"][0] in "BCD" and "inox" not in p["aco"] and "alumínio" not in p["aco"]) + sum(p["peso_total"] for p in P if p["cod"].startswith("A0") and "100 x 50" in p["perfil"])
        u_kg = sum(p["peso_total"] for p in P if p["cod"].startswith("A0") and "U " in p["perfil"])
        chapa_kg = sum(p["peso_total"] for p in P if p["cod"].startswith("D"))
        memb = b["memb"] * 1.15; forro = b["memb"] * 0.95; floor = b["floor"]; deck = b["deck"]
        keder_m = sum(C.arch_lengths()); alu_m = 18 + 66
        groups = [
            ("01 Estrutura metálica", [("Tubos calandrados: anel A0, arcos B01-B07, quadro da cauda, terças, espinha, trilhos de base", "kg", round(steel_kg - chapa_kg), "tubo"),
                                       ("Perfis U 150 x 60 x 3,0 galvanizados (grelha do deck e vigas de borda)", "kg", round(u_kg), "perfilU")]),
            ("02 Chapas", [("Chapas de base, luvas, talões, olhais, cantoneiras, berços (D01-D08)", "kg", round(chapa_kg), "chapa")]),
            ("03 Elementos de conexão", [("Galvanização a fogo de tubos e chapas", "kg", round(steel_kg), "galv"), ("Pintura a pó sobre galvanizado (arcos e anel aparentes)", "kg", round(steel_kg * 0.7), "pintura"),
                                        ("Cabos inox Ø8 (contraventamento)", "m", 48, "inox_cabo8"), ("Esticadores e manilhas inox", "un", 8, "esticador")]),
            ("04 Parafusos e fixadores", [("Kit de parafusos cl. 8.8, chumbadores M16, pinos, presilhas inox", "kit", 1, "fixadores")]),
            ("05 Membrana externa", [("Membrana PVDF 1050 g/m² (com 15% de emendas e bolsas)", "m²", round(memb), "membrana"), ("Confecção e form-finding", "m²", round(memb), "membrana_conf"),
                                     ("Perfil duplo keder calandrado", "m", round(keder_m), "keder"), ("Perfis de arremate, calha oculta e trilhos de alumínio", "m", alu_m, "alu_perfil")]),
            ("06 Isolamento", [("Lã de PET 50 mm", "m²", round(b["memb"]), "pet"), ("Manta refletiva", "m²", round(b["memb"]), "refletiva"), ("Malha de apoio", "m²", round(b["memb"]), "malha")]),
            ("07 Membrana interna", [("Forro tensionado acústico instalado", "m²", round(forro), "forro")]),
            ("08 Vidros", [("Fachada: vidro insulado low-e", "m²", round(b["front_glass"], 1), "vidro_duplo"), ("Esquadria da fachada (anel curvo, montantes, travessa)", "m²", round(b["front_glass"], 1), "esquadria"),
                           ("Janelas Olho completas", "un", 6, "olho"), ("Vidros laminados da Espinha de Luz", "m²", 3.3, "vidro_lam")]),
            ("09 Portas", [("Porta pivotante de vidro 1,00 x 2,40", "un", 1, "porta_pivo"), ("Porta de correr do banho + box de vidro", "un", 1, "box")]),
            ("10 Deck", [("Deck cumaru 20 x 140", "m²", round(deck), "cumaru"), ("Vigotas do deck", "m", round(deck * 2.5), "vigota")]),
            ("11 Piso", [("Vigotas 50 x 150", "m", round(floor * 2.5), "vigota"), ("PIR 50 mm + manta", "m²", round(floor), "pir"), ("Compensado naval 18 mm", "m²", round(floor), "compensado"),
                         ("Piso de engenharia carvalho", "m²", round(floor - 13.2), "piso_eng"), ("Zona molhada (porcelanato)", "m²", 13, "porcelanato"),
                         ("Estacas helicoidais + cabeçotes", "un", 46, "estaca"), ("Instalação das estacas", "un", 46, "estaca_inst"), ("Mobilização da cravação", "vb", 1, "mobiliz")]),
            ("12 Banheiro", [("Louças e metais", "cj", 1, "loucas"), ("Banheira 1,60 m", "un", 1, "banheira"), ("Parede do banho / cabeceira", "m²", 16, "parede")]),
            ("13 Hidráulica", [("Kit PEX + esgoto + ventilação", "cj", 1, "pex"), ("Aquecedor a gás 23 L/min", "un", 1, "aquecedor"), ("Fossa + filtro compactos", "cj", 1, "esgoto")]),
            ("14 Elétrica", [("Quadro, cabos, tomadas, DR", "cj", 1, "eletrica")]),
            ("15 Iluminação", [("Fitas LED, perfis, drivers, luminárias, balizadores", "cj", 1, "iluminacao")]),
            ("16 Ar-condicionado", [("Dutado inverter 12k BTU quente/frio instalado", "un", 1, "ac"), ("Exaustor com recuperador + respiro de cumeeira", "cj", 1, "exaustor")]),
            ("17 Marcenaria", [("Marcenaria sob medida", "cj", 1, "marcenaria"), ("Mobiliário solto", "cj", 1, "mobiliario")]),
            ("18 Acabamentos", [("Painéis ripados internos (cabeceira, rodapés)", "m²", 14, "paineis"), ("Acabamentos e enxoval de abertura", "cj", 1, "acab")]),
        ]
    else:
        b = BZ; P = zenith_parts()
        chapa_kg = sum(p["peso_total"] for p in P if p["cod"].startswith("D"))
        tube_kg = sum(p["peso_total"] for p in P if p["cod"][0] in "BC" and "inox" not in p["aco"])
        u_kg = sum(p["peso_total"] for p in P if p["cod"].startswith("A"))
        memb = b["roof_s"] * 1.15; floor = b["floor"]; deck = b["deck"]
        groups = [
            ("01 Estrutura metálica", [("Mastros, coroas, anéis, pilares, anel de beiral, postes", "kg", round(tube_kg), "tubo"),
                                       ("Perfis U 150 x 60 x 3,0 galvanizados (grelha, bordas, hidromassagem)", "kg", round(u_kg), "perfilU")]),
            ("02 Chapas", [("Chapas de base, capitéis, chapas de topo, bases articuladas, chapas de canto (D01-D14)", "kg", round(chapa_kg), "chapa")]),
            ("03 Elementos de conexão", [("Galvanização a fogo", "kg", round(tube_kg + chapa_kg), "galv"), ("Pintura a pó (mastros, postes e anel aparentes)", "kg", round((tube_kg + chapa_kg) * 0.6), "pintura"),
                                        ("Cabo de borda inox Ø12", "m", 42, "inox_cabo12"), ("Estais inox Ø10", "m", 30, "inox_cabo8"), ("Esticadores e manilhas inox", "un", 21, "esticador")]),
            ("04 Parafusos e fixadores", [("Kit de parafusos, chumbadores M16/M20, pinos, contrapinos", "kit", 1, "fixadores")]),
            ("05 Membrana externa", [("Membrana PVDF 1050 g/m² (com 15%)", "m²", round(memb), "membrana"), ("Confecção, form-finding e padronagem dos cumes", "m²", round(memb), "membrana_conf"),
                                     ("Perfis de borda, clamps e trilhos de alumínio", "m", 38 + 72, "alu_perfil")]),
            ("06 Isolamento", [("Lã de PET 50 mm (forro sobre o corpo)", "m²", 54, "pet"), ("Manta refletiva", "m²", 54, "refletiva"), ("Painéis SIP 100 mm", "m²", 36, "sip"), ("Placa cimentícia + hidrófuga", "m²", 36, "cimenticia"), ("Ripado termotratado externo", "m²", 36, "ripado")]),
            ("07 Membrana interna", [("Forro tensionado seguindo os cumes", "m²", 58, "forro")]),
            ("08 Vidros", [("Fachada + vidro lateral + janelas: vidro insulado low-e", "m²", 38.6, "vidro_duplo"), ("Esquadrias com ruptura térmica (fachada de correr, fixos, janelas)", "m²", 38.6, "esquadria"),
                           ("Cúpula do Óculo do Zênite + esquadria", "un", 1, "cupula")]),
            ("09 Portas", [("Folhas de correr da fachada (incluídas na esquadria) + porta de correr do banho + box", "un", 1, "box")]),
            ("10 Deck", [("Deck cumaru (terraço + passarela)", "m²", round(deck), "cumaru"), ("Vigotas do deck", "m", round(deck * 2.5), "vigota")]),
            ("11 Piso", [("Vigotas 50 x 150", "m", round(floor * 2.5), "vigota"), ("PIR 50 mm + manta", "m²", round(floor), "pir"), ("Compensado naval 18 mm", "m²", round(floor), "compensado"),
                         ("Piso de engenharia carvalho", "m²", round(floor - 15.3), "piso_eng"), ("Zona molhada (porcelanato)", "m²", 15, "porcelanato"),
                         ("Estacas helicoidais + cabeçotes (30 + 7 de tração)", "un", 37, "estaca"), ("Instalação das estacas", "un", 37, "estaca_inst"), ("Mobilização da cravação", "vb", 1, "mobiliz")]),
            ("12 Banheiro", [("Louças e metais (bancada dupla)", "cj", 1, "loucas"), ("Banheira 1,70 m", "un", 1, "banheira"), ("Hidromassagem Ø1,90 completa", "un", 1, "hidro"), ("Parede da cabeceira + divisórias", "m²", 30, "parede")]),
            ("13 Hidráulica", [("Kit PEX + esgoto + ventilação", "cj", 1, "pex"), ("Aquecedor a gás 30 L/min", "un", 1, "aquecedor"), ("Fossa + filtro compactos", "cj", 1, "esgoto")]),
            ("14 Elétrica", [("Quadro 16 módulos, cabos, tomadas, DR da hidromassagem", "cj", 1, "eletrica")]),
            ("15 Iluminação", [("Fitas LED, perfis, luminárias, balizadores do terraço", "cj", 1, "iluminacao")]),
            ("16 Ar-condicionado", [("Dutado inverter 18k BTU instalado", "un", 1, "ac"), ("Chaminé do Respiro motorizada + exaustor com recuperador", "cj", 1, "exaustor")]),
            ("17 Marcenaria", [("Marcenaria sob medida (closet, Ilha do Café, bancada dupla, criados)", "cj", 1, "marcenaria"), ("Mobiliário solto (cama, sofá, chaise, mesas)", "cj", 1, "mobiliario")]),
            ("18 Acabamentos", [("Painéis de madeira internos", "m²", 30, "paineis"), ("Acabamentos e enxoval de abertura", "cj", 1, "acab")]),
        ]
    return groups

SCENARIOS = ["Econômico", "Zion Standard", "Zion Premium"]

def price_for(key, scen, product):
    d, u, std, fe, fp = PRICES[key][:5]
    if scen == 0: v = std * fe
    elif scen == 1: v = std
    else: v = std * fp
    if key == "marcenaria" and product == "zenith": v *= 52000 / 39000
    if key == "ac" and product == "zenith": v *= 14900 / 12400
    if key == "aquecedor" and product == "zenith": v *= 1.27
    if key == "fixadores" and product == "zenith": v *= 1.1
    return v

def budget(product, scen, n_units=1):
    """orçamento completo para um cenário; n_units aplica os fatores de escala."""
    sc = scale_factors(n_units)
    groups = bom_priced(product); rows = []; mat_total = 0
    for gname, items in groups:
        for (desc, un, qtd, key) in items:
            unit = price_for(key, scen, product)
            if scen == 0 and key == "galv": unit = PRICES["epoxi"][2] * PRICES["epoxi"][3]
            fam = "estrutura" if gname[:2] in ("01", "02", "03", "04") else ("membrana" if gname[:2] in ("05", "06", "07") else ("vidros" if gname[:2] in ("08", "09") else ("piso" if gname[:2] in ("10", "11") else ("mep" if gname[:2] in ("13", "14", "15", "16") else "interiores"))))
            unit_s = unit * (1 - sc["material"][fam])
            tot = unit_s * qtd
            rows.append((gname, desc, un, qtd, round(unit_s, 2), round(tot, 2)))
            mat_total += tot
    hours = labor_hours(product); lab_rows = []; lab_total = 0
    fab_keys = ("serralheiro", "soldador"); site_keys = tuple(k for k in hours if k not in fab_keys)
    for k, h in hours.items():
        name, std, fe, fp = LABOR_RATES[k]
        rate = std * (fe if scen == 0 else (fp if scen == 2 else 1.0))
        red = sc["fab_labor"] if k in fab_keys else sc["site_labor"]
        hh = h * (1 - red); tot = hh * rate
        lab_rows.append((name, round(hh), round(rate, 2), round(tot, 2), "fabricação" if k in fab_keys else "instalação"))
        lab_total += tot
    fab_labor = sum(x[3] for x in lab_rows if x[4] == "fabricação"); site_labor = lab_total - fab_labor
    # produção x instalação
    prod_mat = sum(x[5] for x in rows if x[0][:2] in ("01", "02", "03", "04", "05", "06", "07", "08", "09", "17"))   # kit fabricado
    inst_mat = mat_total - prod_mat
    transporte = (9300 if product == "cocoon" else 10800) * (1 - sc["transport"]) * (1.0 if scen != 2 else 1.1)
    equipamentos = (5200 if product == "cocoon" else 8600) * (1 - sc["equip"])   # guincho, talha, andaime, munck (Zenith)
    hospedagem = (5 * (12 if product == "cocoon" else 15) * 185) * (1 - sc["site_labor"])
    indiretos_pct = sc["indiretos"]; conting_pct = sc["contingencia"] + (0.02 if scen == 0 else 0.0)
    nre = 240000 / n_units   # projeto executivo, cálculo, form-finding, gabaritos, protótipo (por produto)
    sub_prod = prod_mat + fab_labor
    sub_inst = inst_mat + site_labor + transporte + equipamentos + hospedagem
    subtotal = sub_prod + sub_inst
    indiretos = subtotal * indiretos_pct; conting = subtotal * conting_pct
    total = subtotal + indiretos + conting + nre
    area_total = 78.0 if product == "cocoon" else 79.3
    area_int = 48.0 if product == "cocoon" else 48.4
    return dict(rows=rows, mat_total=mat_total, lab_rows=lab_rows, lab_total=lab_total, fab_labor=fab_labor, site_labor=site_labor,
                prod_mat=prod_mat, inst_mat=inst_mat, transporte=transporte, equipamentos=equipamentos, hospedagem=hospedagem,
                indiretos=indiretos, indiretos_pct=indiretos_pct, conting=conting, conting_pct=conting_pct, nre=nre,
                sub_prod=sub_prod, sub_inst=sub_inst, subtotal=subtotal, total=total, por_m2=total / area_total, por_m2_int=total / area_int,
                area_total=area_total, area_int=area_int, scen=SCENARIOS[scen], n=n_units)

def scale_factors(n):
    """reduções por volume (fração)"""
    if n <= 1: return dict(material=dict(estrutura=0, membrana=0, vidros=0, piso=0, mep=0, interiores=0), fab_labor=0, site_labor=0, transport=0, equip=0, indiretos=0.12, contingencia=0.08)
    if n <= 5: return dict(material=dict(estrutura=0.05, membrana=0.06, vidros=0.05, piso=0.05, mep=0.04, interiores=0.06), fab_labor=0.14, site_labor=0.08, transport=0.08, equip=0.25, indiretos=0.10, contingencia=0.07)
    if n <= 10: return dict(material=dict(estrutura=0.08, membrana=0.10, vidros=0.08, piso=0.08, mep=0.07, interiores=0.10), fab_labor=0.22, site_labor=0.13, transport=0.12, equip=0.35, indiretos=0.09, contingencia=0.06)
    return dict(material=dict(estrutura=0.13, membrana=0.18, vidros=0.14, piso=0.12, mep=0.12, interiores=0.16), fab_labor=0.34, site_labor=0.20, transport=0.18, equip=0.50, indiretos=0.08, contingencia=0.05)

# =============================================================================
# 5. MANUAL DE MONTAGEM (17 passos)
# =============================================================================
def manual(product):
    c = product == "cocoon"
    S = []
    def step(n, t, equipe, ferr, equip, tempo, riscos, check):
        S.append(dict(n=n, titulo=t, equipe=equipe, ferramentas=ferr, equipamentos=equip, tempo=tempo, riscos=riscos, checklist=check))
    step(1, "Preparação e marcação do terreno", "Líder + 2 montadores + topógrafo", "Estação total ou nível a laser, trena 30 m, estacas de madeira, linha, tinta de marcação", "Roçadeira, caminhonete",
         "4 h", "Erro de locação propaga para todas as etapas; raízes e rochas no eixo das estacas", ["Eixos x/y materializados com 2 referências fixas fora da obra", "Cota de referência (RN) definida", "Acesso do caminhão e área de estoque delimitados", "Interferências (raízes, rocha, rede) mapeadas"])
    step(2, "Instalação das fundações (estacas helicoidais)", "Operador de cravação + 2 montadores + líder", "Chaves de torque, nível, gabarito de posição", "Motor hidráulico de cravação (ou mini-escavadeira com cabeçote), gerador",
         "1 dia" if c else "1,5 dia", "Torque abaixo do mínimo (solo fraco): alongar estaca ou reposicionar; desvio de prumo > 2%", ["Torque final de cada estaca registrado na planilha", f"{46 if c else 37} estacas posicionadas com ± 30 mm", "Cabeçotes nivelados a ± 5 mm com nível a laser", "Estacas de tração dos postes com olhal orientado (Zenith)"])
    step(3, "Montagem da estrutura base (grelha de vigas U 150)", "4 montadores + líder", "Torquímetro 20-100 N·m, chaves combinadas 19 mm, furadeira, esquadro de 1 m, cordão", "Guincho manual 1 t ou 2 cavaletes",
         "1 dia", "Esquadro fora: medir as duas diagonais; vigas com furos oblongos permitem ajuste", ["Diagonais iguais (± 10 mm)", "Todos os M12 com torque 45 N·m", "Vigas de borda curvas (Cocoon) / de borda do corpo (Zenith) conferidas com o gabarito de planta", "Cabeçotes travados com contraporca"])
    step(4, "Instalação das peças estruturais secundárias (módulos de piso e deck)", "4 montadores (2 carpinteiros)", "Parafusadeira, serra circular, nível", "Guincho manual",
         "1,5 dia", "Módulos molhados antes do fechamento: proteger com lona", [f"{18 if c else 16} módulos de piso nivelados", "PIR contínuo, manta inferior fechada", "Passagens de esgoto e PEX deixadas nas posições do projeto", "Deck com juntas de 6 mm alinhadas"])
    step(5, "Montagem dos arcos" if c else "Montagem de pilares, anel de beiral e mastros", "4 montadores + líder", "Torquímetro 50-250 N·m, chaves 19/24 mm, gabarito de luva, prumo, nível", "Guincho manual 1 t + tripé; escada / andaime tubular" if c else "Talha 1 t + tripé; munck opcional para M1",
         "2 dias", "Queda do arco durante o içamento: travar cada arco com 2 escoras antes de soltar o guincho" if c else "Mastro sem escora antes do anel: içar somente com a base articulada travada e 3 cordas guia",
         ["Cada arco montado no chão (2 pernas + coroa nas luvas D02, 4 M12 + pino)", "Sequência A7 para A1; A0 (lábio) por último", "Pés dos arcos com 4 M16 e torque 120 N·m", "Prumo e posição x de cada arco ± 10 mm"] if c else
         ["10 pilares aprumados (1/500) e chumbados", "6 segmentos do anel parafusados (4 M16, 120 N·m)", "Mastros M1 e M2 içados e pinados; coroas e anéis fixados", "Diagonais do anel conferidas"])
    step(6, "Instalação dos travamentos", "4 montadores", "Chaves 24 mm, tensiômetro de cabo, torquímetro", "Escada / andaime",
         "0,5 dia", "Terça rosqueada sem contraporca solta com vibração", ["7 linhas de terças com porca e contraporca", "Espinha C03 fixada nos berços", "Cabos em X com 2 kN de pré-tensão (tensiômetro)"] if c else ["7 postes pinados nas bases, inclinação 8° conferida", "Estais passados sem tensão final", "Cabo de borda nas chapas de canto (frouxo)"])
    step(7, "Conferência de esquadro e alinhamento", "Líder + engenheiro", "Estação total / nível a laser, trena, prumo", "",
         "3 h", "Prosseguir com a membrana sobre estrutura fora de geometria gera rugas e sobretensão", ["Topo de cada arco (ou anel/cumes) na cota do projeto ± 15 mm", "Eixos e diagonais registrados no relatório", "Torque de amostragem de 10% dos parafusos", "Liberação assinada para a membrana"])
    step(8, "Instalação da membrana externa", "2 instaladores de membrana + 2 montadores + líder", "Puxadores de keder, cordas, esticadores, tensiômetro, ferro de solda portátil (reparos)", "Andaime, guincho manual, cordas guia",
         "1 dia" if c else "1,5 dia", "Vento acima de 30 km/h: suspender; membrana arrastada em aresta: proteger cantos", ["Painéis deslizados no keder da cauda para a frente" if c else "Membrana içada pelos anéis de cume e presa nos clamps", "Bolsas de base tensionadas progressivamente (cruzado)" if c else "Cantos e estais tensionados em cruz, flecha das bordas ± 20 mm", "Sem rugas; pré-tensão uniforme", "Teste de água nos rodapés / bordas (15 min)"])
    step(9, "Instalação do isolamento", "3 montadores", "Estilete, grampeador, arame, tesoura", "Escada",
         "1 dia", "Isolamento comprimido perde R; manta úmida: instalar com a membrana já fechada", ["Mantas PET presas à malha das terças (ou cabos do forro), sem vazios", "Refletiva com face refletiva para a câmara", "Fitas nas emendas", "Passagens de eletrodutos previstas"])
    step(10, "Instalação da membrana interna (forro tensionado)", "2 instaladores + 1 montador", "Espátulas de harpão, soprador térmico, nível", "Escada",
         "1 dia", "Forro tensionado antes das instalações elétricas: coordenar caixas e luminárias", ["Trilhos harpão fixados nos talões / cabos", "7 painéis tensionados sem ondulação" if c else "6 painéis seguindo os cumes, anéis internos fixados", "Aberturas de difusores e luminárias recortadas com anel"])
    step(11, "Instalação das portas e vidros", "Vidraceiro + 2 auxiliares", "Ventosas, calços, nível, silicone estrutural, pistola", "Cavaletes de vidro, carrinho de ventosa",
         "1,5 dia" if c else "2 dias", "Vidro de 90 kg (fachada): mínimo 3 pessoas ou içador a vácuo", ["Anel de alumínio E07 sobre EPDM (Cocoon) / contramarcos (Zenith) no prumo", "Vidros calçados e selados; porta pivotante ajustada", "Janelas Olho com selante PU curado 24 h", "Vidros da espinha / óculo com teste de água"])
    step(12, "Instalações elétricas", "Eletricista + auxiliar", "Alicate de crimpagem, multímetro, testador de DR, furadeira", "",
         "1,5 dia", "Passagem de cabos pelo ático depois do forro: usar eletrodutos previstos", ["Quadro no ático com circuitos identificados", "DR testado; aterramento < 10 Ω", "Fitas LED com drivers acessíveis", "Condensadora alimentada e protegida"])
    step(13, "Instalações hidráulicas", "Encanador + auxiliar", "Ferramenta de crimpar PEX, nível, teste de pressão", "",
         "1,5 dia", "Ponto de esgoto fora de posição no módulo de piso: conferir no passo 4", ["Teste de pressão 6 bar por 30 min sem queda", "Esgoto com 2% de declividade e ventilação", "Aquecedor ligado e regulado", "Hidromassagem cheia e testada (Zenith)"])
    step(14, "Montagem do banheiro", "Encanador + montador + acabamento", "Nível, furadeira, pistola de silicone", "",
         "1 dia", "Banheira pesada (Cocoon: entra pela porta antes da marcenaria)", ["Louças fixadas e vedadas", "Bancada nivelada", "Box e porta de correr regulados", "Rejuntes e silicones concluídos"])
    step(15, "Montagem dos móveis", "Marceneiro + auxiliar", "Parafusadeira, nível, calços", "",
         "1,5 dia", "Marcenaria embutida na curva: usar os gabaritos de fábrica", ["Console café, armário baixo, criados fixados" if c else "Closet, Ilha do Café (totem do mastro) e bancada dupla fixados", "Cama montada; cabeceira nivelada", "Portas e gavetas reguladas"])
    step(16, "Acabamentos", "Equipe de acabamento (2)", "Espátulas, lixas, aspirador, panos", "",
         "1 dia", "Riscos em vidros e piso durante a limpeza grossa", ["Rodapés e perfis de LED instalados", "Painéis ripados fixados", "Selantes e arremates conferidos", "Limpeza fina e enxoval"])
    step(17, "Testes finais e entrega", "Líder + engenheiro + operador do glamping", "Termômetro IV, tensiômetro, testador elétrico, câmera", "",
         "4 h", "Entregar sem registro fotográfico e sem as-built", ["Climatização em carga por 2 h (delta de 8 °C)", "Pré-tensão da membrana medida e registrada", "Teste de chuva (mangueira) na concha / cobertura e esquadrias", "Manual do operador e as-built entregues; garantia iniciada"])
    return S

# =============================================================================
# 6. CRONOGRAMA DE FABRICAÇÃO (semanas)
# =============================================================================
FAB_SCHEDULE = {
    "cocoon": [("Projeto executivo, cálculo e form-finding", 0, 3), ("Compra de aço, tubos, perfis e chapas", 1, 2), ("Gabaritos de calandra e bancada", 2, 2), ("Calandra e solda dos arcos e anel", 3, 3),
               ("Grelha, trilhos, terças, chapas", 4, 2), ("Pré-montagem em fábrica (fit test)", 6, 1), ("Galvanização e pintura", 7, 1.5), ("Confecção da membrana (paralelo)", 3, 4),
               ("Esquadrias e vidros (paralelo)", 3, 5), ("Marcenaria e módulos de piso (paralelo)", 4, 4), ("Embalagem e expedição", 8.5, 0.5)],
    "zenith": [("Projeto executivo, cálculo e form-finding", 0, 3), ("Compra de aço, tubos, perfis, painéis SIP", 1, 2), ("Gabaritos de solda (coroas, anel)", 2, 1.5), ("Mastros, coroas, anéis, pilares", 3, 2.5),
               ("Anel de beiral, postes, grelha, chapas", 4, 2.5), ("Pré-montagem em fábrica (fit test)", 6.5, 1), ("Galvanização e pintura", 7.5, 1.5), ("Confecção da membrana (paralelo)", 3, 5),
               ("Esquadrias, vidros e cúpula (paralelo)", 3, 6), ("Painéis SIP, marcenaria, módulos (paralelo)", 4, 4.5), ("Embalagem e expedição", 9, 0.5)],
}

if __name__ == "__main__":
    for prod in ("cocoon", "zenith"):
        P = cocoon_parts() if prod == "cocoon" else zenith_parts()
        print(prod, "peças:", sum(p["qtd"] for p in P), "itens:", len(P), "aço:", round(sum(p["peso_total"] for p in P if "alumínio" not in p["aco"] and "madeira" not in p["aco"])), "kg")
        for s in range(3):
            b = budget(prod, s)
            print(f"   {b['scen']:14s} materiais {b['mat_total']:>10,.0f}  MO {b['lab_total']:>9,.0f}  produção {b['sub_prod']:>10,.0f}  instalação {b['sub_inst']:>10,.0f}  TOTAL {b['total']:>10,.0f}  R$/m² {b['por_m2']:>7,.0f}")
        for n in (1, 5, 10, 50):
            b = budget(prod, 1, n); print(f"   escala {n:2d} un: total/un {b['total']:>10,.0f}")

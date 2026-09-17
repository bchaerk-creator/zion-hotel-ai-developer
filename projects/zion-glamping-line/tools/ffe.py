# -*- coding: utf-8 -*-
"""FF&E (Furniture, Fixtures & Equipment) e OS&E das unidades da Zion Glamping Collection.
Tudo o que vai dentro de cada cabana, além da construção: mobiliário fixo e solto, luminárias decorativas, equipamentos,
enxoval, amenities e itens do deck. Preços de referência (R$, set/2026, Santa Catarina, incluindo frete e instalação
quando aplicável) a confirmar por cotação; padrão Zion New Luxury (cenário Zion Standard).
Uso: python3 ffe.py  (imprime totais por produto)"""

# catálogo de itens: código -> (descrição, especificação, unidade, preço unitário Zion Standard, categoria)
# categorias: M mobiliário · F luminárias e decoração · E equipamentos · O enxoval e OS&E · D deck e exterior · B banho (acessórios)
ITEMS = {
    # ---- mobiliário
    "M01": ("Cama king box + colchão", "Box 1,93 x 2,03 revestido em linho, colchão molas ensacadas 32 cm, pillow top", "un", 9800, "M"),
    "M02": ("Cabeceira estofada", "Painel curvo em madeira laminada com estofado em linho, integrado à marcenaria", "un", 4200, "M"),
    "M03": ("Criado-mudo suspenso", "Carvalho natural, gaveta com fecho toque, iluminação embutida", "un", 1650, "M"),
    "M04": ("Sofá 2,40 m", "Estrutura em madeira, espuma D33, tecido bouclé antimancha", "un", 8900, "M"),
    "M05": ("Sofá 2,00 m", "Estrutura em madeira, espuma D33, tecido bouclé antimancha", "un", 7600, "M"),
    "M06": ("Chaise de contemplação", "Chaise 1,60 x 0,80 em madeira e corda náutica, almofada impermeável", "un", 5400, "M"),
    "M07": ("Poltrona de leitura", "Poltrona giratória em couro natural e madeira", "un", 4600, "M"),
    "M08": ("Mesa de centro / lateral", "Tampo em pedra (quartzito) sobre base de madeira torneada", "un", 2300, "M"),
    "M09": ("Ilha do café / minibar", "Marcenaria sob medida com tampo em pedra, frigobar embutido, gaveta de cápsulas", "un", 7800, "M"),
    "M10": ("Closet / armário", "Marcenaria em carvalho com portas ripadas, cabideiro, prateleiras e cofre", "un", 6900, "M"),
    "M11": ("Banco aos pés da cama", "Banco 1,40 m em madeira e couro", "un", 2100, "M"),
    "M12": ("Bancada do banho", "Tampo em pedra com cuba esculpida, gabinete ripado suspenso", "un", 6200, "M"),
    "M13": ("Espelho com iluminação", "Espelho redondo Ø0,90 com LED perimetral e antiembaçante", "un", 1900, "M"),
    "M14": ("Mesa de refeições / trabalho", "Mesa 0,80 x 1,20 em carvalho + 2 cadeiras", "cj", 4800, "M"),
    "M15": ("Totem do mastro (Safari)", "Revestimento do mastro M2 em madeira com prateleiras e iluminação", "un", 3200, "M"),
    "M16": ("Ripado da cabeceira", "Painel ripado termotratado com fitas LED (parede da cabeceira)", "m²", 620, "M"),
    "M18": ("Mini cozinha acoplada", "Marcenaria sob medida 2,00 m acoplada à concha: tampo em quartzito, cuba, módulos para geladeira, forno, gaveteiro e lixeira, prateleira com LED (Casulo)", "un", 11800, "M"),
    "M17": ("Cama queen box + colchão", "Box 1,58 x 1,98 revestido em linho, colchão molas ensacadas 30 cm, pillow top (Cápsula)", "un", 8200, "M"),
    # ---- luminárias e decoração
    "F01": ("Arandela de leitura", "Arandela articulada em latão escovado, LED 2700 K dimerizável", "un", 890, "F"),
    "F02": ("Luminária de piso", "Luminária de piso em madeira e linho, 2700 K", "un", 1450, "F"),
    "F03": ("Luminária de mesa", "Abajur cerâmico artesanal, 2700 K", "un", 720, "F"),
    "F04": ("Tapete de lã", "Tapete de lã tecido à mão 2,00 x 3,00", "un", 3800, "F"),
    "F05": ("Tapete de lã (pequeno)", "Tapete de lã 1,60 x 2,30", "un", 2600, "F"),
    "F06": ("Cortinas e blackout", "Cortina de linho + blackout motorizado, por metro linear de fachada de vidro", "m", 980, "F"),
    "F07": ("Cortina da lanterna / óculo", "Tela de sombreamento motorizada circular", "un", 3400, "F"),
    "F08": ("Arte e objetos", "Curadoria Zion: peças de artesanato regional, cerâmica, vasos, livros", "vb", 4500, "F"),
    "F09": ("Espelho de corpo inteiro", "Espelho 0,60 x 1,80 com moldura de madeira", "un", 1100, "F"),
    "F10": ("Plantas e vasos", "Plantas de interior em vasos de cerâmica", "vb", 900, "F"),
    # ---- equipamentos
    "E01": ("Frigobar", "Frigobar 90 L embutido, silencioso (< 38 dB), classe A", "un", 2900, "E"),
    "E02": ("Cafeteira de cápsulas + chaleira", "Cafeteira de cápsulas premium e chaleira elétrica de pescoço de ganso", "cj", 1600, "E"),
    "E03": ("Cofre eletrônico", "Cofre digital 20 L para notebook", "un", 650, "E"),
    "E04": ("Caixa de som / rádio", "Sistema de som Bluetooth de mesa", "un", 1900, "E"),
    "E05": ("Smart TV 50\" (opcional)", "Smart TV 4K 50\" em painel retrátil / espelho", "un", 4200, "E"),
    "E06": ("Secador de cabelo", "Secador profissional 2000 W com suporte", "un", 480, "E"),
    "E07": ("Hidromassagem externa", "Hot tub de 4 lugares, fibra, aquecimento a gás/elétrico, cobertura térmica", "un", 38000, "E"),
    "E08": ("Aquecedor / lareira ecológica", "Lareira a etanol de mesa ou de piso (inverno)", "un", 2800, "E"),
    "E09": ("Umidificador / purificador", "Purificador de ar HEPA silencioso", "un", 1500, "E"),
    "E10": ("Fechadura eletrônica", "Fechadura digital com cartão/senha na porta principal", "un", 1800, "E"),
    "E11": ("Termostato e automação de cenas", "Central de automação (cenas de luz, cortinas, clima, som)", "un", 4200, "E"),
    "E12": ("Ventilador de teto (opcional)", "Ventilador de teto DC silencioso com LED, na lanterna / cume", "un", 2400, "E"),
    "E13": ("Cooktop de indução 2 bocas", "Cooktop de indução 2 zonas, 30 x 52 cm, 3,5 kW, 220 V, embutido no tampo", "un", 1900, "E"),
    "E14": ("Forno elétrico compacto", "Forno elétrico de embutir 45 L, 60 cm, 1,8 kW, porta de vidro duplo, 220 V", "un", 2600, "E"),
    "E15": ("Air fryer", "Fritadeira sem óleo 5 L, 1,5 kW, em nicho ventilado sobre o tampo", "un", 900, "E"),
    "E16": ("Geladeira sob bancada", "Refrigerador 120 L sob bancada com congelador, classe A, silencioso (< 40 dB), porta com painel ripado", "un", 3400, "E"),
    "E17": ("Depurador de ar slim", "Depurador 60 cm com filtro de carvão ativado, 2 velocidades, LED, recirculação", "un", 1100, "E"),
    # ---- enxoval e OS&E (por unidade, 2 jogos + reserva)
    "O01": ("Enxoval de cama", "3 jogos: lençóis 400 fios algodão egípcio, edredom, duvet, protetor, 6 travesseiros", "cj", 5200, "O"),
    "O02": ("Enxoval de banho", "3 jogos: toalhas de banho/rosto/piso 600 g/m², roupões, chinelos", "cj", 2800, "O"),
    "O03": ("Amenities", "Dispensers de vidro (shampoo, condicionador, sabonete, hidratante) + kit de boas-vindas (estoque inicial)", "cj", 1400, "O"),
    "O04": ("Louças, talheres e copos", "Serviço para 4 (café da manhã e taças de vinho), bandeja, cesta", "cj", 1900, "O"),
    "O05": ("Manta, almofadas e decoração têxtil", "Manta de lã, 6 almofadas, cortina de banho em linho", "cj", 1800, "O"),
    "O06": ("Cabides, lixeiras, acessórios", "Cabides de madeira, lixeiras, cesto de roupa, kit de costura, guarda-chuva", "cj", 950, "O"),
    "O07": ("Sinalização e papelaria Zion", "Placas, diretório de serviços, QR de automação, cartões", "cj", 700, "O"),
    "O08": ("Kit de segurança", "Extintor, detector de fumaça, lanterna, kit primeiros socorros", "cj", 850, "O"),
    "O09": ("Utensílios de cozinha", "Jogo de panelas para indução, frigideira, tábua, facas, utensílios, escorredor, potes", "cj", 1400, "O"),
    # ---- deck e exterior
    "D01": ("Espreguiçadeiras", "Par de espreguiçadeiras em madeira teca e corda náutica, almofadas outdoor", "par", 6400, "D"),
    "D02": ("Mesa e cadeiras de deck", "Mesa redonda Ø0,80 + 2 cadeiras em madeira e corda náutica", "cj", 4900, "D"),
    "D03": ("Poltrona suspensa (opcional)", "Poltrona suspensa em corda náutica com suporte", "un", 3800, "D"),
    "D04": ("Balizadores e lanternas de deck", "Lanternas portáteis LED recarregáveis + tochas de citronela", "cj", 1200, "D"),
    "D05": ("Ducha externa", "Ducha de deck em aço inox com base de cumaru", "un", 2600, "D"),
    "D06": ("Chuveirão / banheira externa (opcional)", "Banheira de imersão externa em fibra ou aço, com aquecedor", "un", 14500, "D"),
    "D07": ("Fogueira / fire pit", "Fire pit em aço corten com grelha e tampa", "un", 3200, "D"),
    # ---- banho (acessórios além das louças e metais da construção)
    "B01": ("Acessórios do banho", "Toalheiros aquecidos, ganchos, saboneteiras e porta-papel em latão escovado", "cj", 2400, "B"),
    "B02": ("Banqueta e bandeja da banheira", "Banqueta de teca e bandeja para banheira", "cj", 900, "B"),
    "B03": ("Balança e acessórios", "Balança digital, secador de toalhas, kit de manicure", "cj", 450, "B"),
}

CATS = {"M": "Mobiliário", "F": "Luminárias e decoração", "E": "Equipamentos", "O": "Enxoval e OS&E", "D": "Deck e exterior", "B": "Banho (acessórios)"}

# listas por produto: (código, quantidade, ambiente, observação)
LISTS = {
    "cocoon": [("M01", 1, "Suíte", ""), ("M02", 1, "Suíte", "cabeceira curva sob a Espinha de Luz"), ("M03", 2, "Suíte", ""), ("M11", 1, "Suíte", ""), ("M16", 12, "Suíte / banho", "parede da cabeceira"),
               ("M06", 1, "Estar", "junto à fachada de vidro"), ("M07", 1, "Estar", ""), ("M08", 1, "Estar", "mesa lateral Ø0,56"), ("M18", 1, "Estar", "mini cozinha 2,00 m"), ("M10", 1, "Estar", "armário baixo embutido 1,10 m"),
               ("M12", 1, "Banho", "bancada 1,50 m"), ("M13", 1, "Banho", ""),
               ("F01", 2, "Suíte", ""), ("F02", 1, "Estar", ""), ("F03", 1, "Estar", ""), ("F04", 1, "Estar", ""), ("F05", 1, "Suíte", ""), ("F06", 6.5, "Fachada", "6,50 m de fachada de vidro"), ("F07", 1, "Espinha de Luz", "tela de sombreamento 0,70 x 4,70"), ("F08", 1, "Geral", ""), ("F10", 1, "Geral", ""),
               ("E16", 1, "Mini cozinha", "sob bancada"), ("E13", 1, "Mini cozinha", "circuito dedicado C13"), ("E14", 1, "Mini cozinha", "circuito dedicado C14"), ("E15", 1, "Mini cozinha", ""), ("E17", 1, "Mini cozinha", ""), ("E02", 1, "Mini cozinha", ""), ("E03", 1, "Armário", ""), ("E04", 1, "Estar", ""), ("E06", 1, "Banho", ""), ("E08", 1, "Estar", ""), ("E10", 1, "Porta PV1", ""), ("E11", 1, "Ático técnico", ""),
               ("O01", 1, "Suíte", ""), ("O02", 1, "Banho", ""), ("O03", 1, "Banho", ""), ("O04", 1, "Mini cozinha", ""), ("O09", 1, "Mini cozinha", ""), ("O05", 1, "Geral", ""), ("O06", 1, "Geral", ""), ("O07", 1, "Geral", ""), ("O08", 1, "Geral", ""),
               ("D01", 1, "Deck", ""), ("D02", 1, "Deck", ""), ("D04", 1, "Deck", ""), ("D05", 1, "Deck", ""), ("E07", 1, "Deck", "opcional: hot tub Ø1,90 no deck"),
               ("B01", 1, "Banho", ""), ("B02", 1, "Banho", "banheira 1,60"), ("B03", 1, "Banho", "")],
    "zenith": [("M01", 1, "Suíte", "sob o Óculo do Zênite"), ("M02", 1, "Suíte", "parede da cabeceira"), ("M03", 2, "Suíte", ""), ("M11", 1, "Suíte", ""), ("M16", 16, "Cabeceira / banho", ""),
               ("M04", 1, "Estar", "sofá 2,20"), ("M06", 1, "Estar", "chaise de contemplação"), ("M08", 1, "Estar", "mesa de centro"), ("M09", 1, "Estar", "Ilha do Café 2,00 m"), ("M10", 1, "Suíte", "closet 2,00 x 0,60"), ("M15", 1, "Estar", ""),
               ("M12", 1, "Banho", "bancada dupla 2,00 m"), ("M13", 2, "Banho", ""),
               ("F01", 3, "Suíte / estar", ""), ("F02", 1, "Estar", ""), ("F03", 2, "Estar / suíte", ""), ("F04", 1, "Estar", ""), ("F05", 1, "Suíte", ""), ("F06", 11.8, "Fachada e lateral", "5,40 + 6,40 m de vidro"), ("F07", 1, "Óculo", "tela circular Ø1,20"), ("F08", 1, "Geral", ""), ("F10", 1, "Geral", ""),
               ("E01", 1, "Ilha do Café", ""), ("E02", 1, "Ilha do Café", ""), ("E03", 1, "Closet", ""), ("E04", 1, "Estar", ""), ("E06", 1, "Banho", ""), ("E08", 1, "Estar", ""), ("E10", 1, "Fachada PC1", ""), ("E11", 1, "Ático técnico", "inclui motor da chaminé do Respiro"),
               ("O01", 1, "Suíte", ""), ("O02", 1, "Banho", ""), ("O03", 1, "Banho", ""), ("O04", 1, "Café", ""), ("O05", 1, "Geral", ""), ("O06", 1, "Geral", ""), ("O07", 1, "Geral", ""), ("O08", 1, "Geral", ""),
               ("D01", 1, "Terraço", ""), ("D02", 1, "Terraço", ""), ("D03", 1, "Passarela", "opcional"), ("D04", 1, "Terraço", ""), ("D05", 1, "Terraço", "junto à hidromassagem"), ("E07", 1, "Terraço", "hidromassagem Ø1,90 prevista em projeto"), ("D07", 1, "Terraço", ""),
               ("B01", 1, "Banho", ""), ("B02", 1, "Banho", "banheira 1,70"), ("B03", 1, "Banho", "")],
    "lodge": [("M01", 1, "Suíte", "sob a Lanterna Zion"), ("M02", 1, "Suíte", ""), ("M03", 2, "Suíte", ""), ("M16", 8, "Parede-corda", ""),
              ("M04", 1, "Estar", "sofá 2,40"), ("M07", 1, "Estar", ""), ("M08", 1, "Estar", "mesa lateral"), ("M09", 1, "Estar", "café / minibar 1,70 m"), ("M10", 1, "Estar", "closet 1,70 x 0,75"),
              ("M12", 1, "Banho", "bancada 1,40 m"), ("M13", 1, "Banho", ""),
              ("F01", 2, "Suíte", ""), ("F02", 1, "Estar", ""), ("F03", 1, "Estar", ""), ("F04", 1, "Estar", ""), ("F06", 14.1, "Cinco faces de vidro", "5 x 2,82 m"), ("F07", 1, "Lanterna", "tela circular Ø1,50"), ("F08", 1, "Geral", ""), ("F10", 1, "Geral", ""),
              ("E01", 1, "Estar", ""), ("E02", 1, "Estar", ""), ("E03", 1, "Closet", ""), ("E04", 1, "Estar", ""), ("E06", 1, "Banho", ""), ("E10", 1, "Porta PC1", ""), ("E11", 1, "Ático", ""),
              ("O01", 1, "Suíte", ""), ("O02", 1, "Banho", ""), ("O03", 1, "Banho", ""), ("O04", 1, "Café", ""), ("O05", 1, "Geral", ""), ("O06", 1, "Geral", ""), ("O07", 1, "Geral", ""), ("O08", 1, "Geral", ""),
              ("D01", 1, "Deck", ""), ("D02", 1, "Deck", ""), ("D04", 1, "Deck", ""), ("D05", 1, "Deck", ""), ("D07", 1, "Deck", "opcional"),
              ("B01", 1, "Banho", ""), ("B02", 1, "Banho", "banheira de sentar"), ("B03", 1, "Banho", "")],
    "lodge24": [("M01", 1, "Suíte", "sob a Lanterna Zion"), ("M02", 1, "Suíte", ""), ("M03", 2, "Suíte", ""), ("M16", 6, "Parede-corda", ""),
                ("M07", 2, "Estar", "duas poltronas junto ao vidro"), ("M08", 1, "Estar", "mesa lateral"), ("M09", 1, "Estar", "café / minibar 1,60 m"), ("M10", 1, "Estar", "closet 1,60 x 0,60"),
                ("M12", 1, "Banho", "bancada 1,20 m"), ("M13", 1, "Banho", ""),
                ("F01", 2, "Suíte", ""), ("F03", 1, "Estar", ""), ("F05", 1, "Suíte", ""), ("F06", 6.7, "Três faces de vidro", "3 x 2,24 m"), ("F07", 1, "Lanterna", "tela circular Ø1,20"), ("F08", 1, "Geral", "curadoria reduzida"), ("F10", 1, "Geral", ""),
                ("E01", 1, "Estar", ""), ("E02", 1, "Estar", ""), ("E03", 1, "Closet", ""), ("E04", 1, "Estar", ""), ("E06", 1, "Banho", ""), ("E10", 1, "Porta PC1", ""),
                ("O01", 1, "Suíte", ""), ("O02", 1, "Banho", ""), ("O03", 1, "Banho", ""), ("O04", 1, "Café", ""), ("O05", 1, "Geral", ""), ("O06", 1, "Geral", ""), ("O07", 1, "Geral", ""), ("O08", 1, "Geral", ""),
                ("D02", 1, "Deck", "mesa e 2 cadeiras"), ("D04", 1, "Deck", ""),
                ("B01", 1, "Banho", ""), ("B03", 1, "Banho", "")],
    "lodge28": [("M01", 1, "Suíte", "sob a lanterna 1"), ("M02", 1, "Suíte", ""), ("M03", 2, "Suíte", ""), ("M16", 7, "Parede do banho", ""),
                ("M05", 1, "Estar", "sofá 2,00 sob a lanterna 2"), ("M08", 1, "Estar", "mesa de centro"), ("M09", 1, "Estar", "café / minibar 1,80 m"), ("M10", 1, "Suíte", "closet 1,80 x 0,55"),
                ("M12", 1, "Banho", "bancada 1,30 m"), ("M13", 1, "Banho", ""),
                ("F01", 2, "Suíte", ""), ("F02", 1, "Estar", ""), ("F03", 1, "Estar", ""), ("F05", 1, "Suíte", ""), ("F06", 9.4, "Cinco faces de vidro", "1,74 x 5 faces"), ("F07", 2, "Lanternas", "telas circulares Ø1,10"), ("F08", 1, "Geral", ""), ("F10", 1, "Geral", ""),
                ("E01", 1, "Estar", ""), ("E02", 1, "Estar", ""), ("E03", 1, "Closet", ""), ("E04", 1, "Estar", ""), ("E06", 1, "Banho", ""), ("E10", 1, "Porta PC1", ""), ("E11", 1, "Ático", ""),
                ("O01", 1, "Suíte", ""), ("O02", 1, "Banho", ""), ("O03", 1, "Banho", ""), ("O04", 1, "Café", ""), ("O05", 1, "Geral", ""), ("O06", 1, "Geral", ""), ("O07", 1, "Geral", ""), ("O08", 1, "Geral", ""),
                ("D01", 1, "Terraço", ""), ("D02", 1, "Terraço", ""), ("D04", 1, "Terraço", ""), ("D05", 1, "Terraço", ""),
                ("B01", 1, "Banho", ""), ("B03", 1, "Banho", "")],

    "capsule": [("M17", 1, "Suíte", "sob o Anel de Luz, pés para o Visor"), ("M02", 1, "Suíte", "cabeceira curva na parede do banho"), ("M03", 2, "Suíte", ""),
                ("M06", 1, "Estar", "chaise junto ao Visor"), ("M07", 1, "Estar", "poltrona"), ("M08", 1, "Estar", "mesa lateral"), ("M09", 1, "Estar", "café / minibar 1,05 m"), ("M10", 1, "Suíte", "closet 1,30 x 0,40"),
                ("M12", 1, "Banho", "bancada 1,20 m"), ("M13", 1, "Banho", ""),
                ("F01", 2, "Suíte", ""), ("F03", 1, "Estar", ""), ("F05", 1, "Suíte", ""), ("F06", 5.2, "Visor", "trilho curvo no arco do Visor"), ("F07", 1, "Anel de Luz", "tela motorizada curva"), ("F08", 1, "Geral", "curadoria reduzida"), ("F10", 1, "Geral", ""),
                ("E01", 1, "Estar", ""), ("E02", 1, "Estar", ""), ("E03", 1, "Closet", ""), ("E04", 1, "Estar", ""), ("E06", 1, "Banho", ""), ("E10", 1, "Porta PV1", ""), ("E11", 1, "Técnico", ""),
                ("O01", 1, "Suíte", ""), ("O02", 1, "Banho", ""), ("O03", 1, "Banho", ""), ("O04", 1, "Café", ""), ("O05", 1, "Geral", ""), ("O06", 1, "Geral", ""), ("O07", 1, "Geral", ""), ("O08", 1, "Geral", ""),
                ("D02", 1, "Deck", "mesa e 2 cadeiras"), ("D04", 1, "Deck", ""),
                ("B01", 1, "Banho", ""), ("B03", 1, "Banho", "")],
}
OPTIONAL = {"E05", "E07", "E12", "D03", "D06", "D07"}   # itens tratados como opcionais no total-base quando marcados "opcional"
SCEN_FACTOR = {0: 0.72, 1: 1.0, 2: 1.35}               # Econômico, Zion Standard, Zion Premium

def rows(product, scen=1):
    out = []
    for (code, q, amb, obs) in LISTS[product]:
        desc, spec, un, price, cat = ITEMS[code]
        unit = price * SCEN_FACTOR[scen]
        opt = code in OPTIONAL and "opcional" in obs.lower() or (code in OPTIONAL and code == "E05")
        out.append(dict(code=code, cat=cat, cat_name=CATS[cat], desc=desc, spec=spec, un=un, qty=q, amb=amb, obs=obs, unit=round(unit, 2), total=round(unit * q, 2), optional=opt))
    return out

def totals(product, scen=1):
    R = rows(product, scen); base = sum(r["total"] for r in R if not r["optional"]); opt = sum(r["total"] for r in R if r["optional"])
    by_cat = {}
    for r in R:
        if not r["optional"]: by_cat[r["cat_name"]] = by_cat.get(r["cat_name"], 0) + r["total"]
    return dict(base=base, optional=opt, by_cat=by_cat, n_items=len(R), n_units=sum(r["qty"] for r in R))

if __name__ == "__main__":
    for p in LISTS:
        for s in range(3):
            t = totals(p, s); print(p, ["Econômico", "Zion Standard", "Zion Premium"][s], f"base R$ {t['base']:,.0f}".replace(",", "."), f"opcionais R$ {t['optional']:,.0f}".replace(",", "."), t["n_items"], "itens")

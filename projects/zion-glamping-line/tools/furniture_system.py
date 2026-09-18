# -*- coding: utf-8 -*-
"""ZG-FFE-001 · ZION FURNITURE DESIGN SYSTEM · ZION NEW LUXURY FURNITURE COLLECTION.
Análise das referências (FF&I 2023-2025 e fotos das Bubbles), DNA, moodboard, paleta, materiais, texturas, formas, assinatura Zion,
linguagens (pés, curvas, ferragens, tecidos, luminárias), sistema de acabamentos, ZION CORE / DESTINATION DNA, tiers e a coleção de 46 peças.
Sem preços. A4 paisagem. Saída: 08_MOBILIARIO/ZG-FFE-001_Zion_Furniture_Design_System.html · PDF via export_pdf.js"""
import os
from furniture_common import *

DOC = "ZG-FFE-001"; REV = "REV 00 — DESIGN SYSTEM"; DATE = "18/09/2026"
pages = []
def page(body, label, code="", cls=""):
    n = len(pages) + 1
    pages.append(f'<section class="page {cls}"><div class="head"><span>{zion_mark_html("14px", color="#1B2117" if "dark" not in cls else "#FEF5F0")} ZION NEW LUXURY FURNITURE COLLECTION · {DOC} · {REV}</span><span>{esc(code or DOC)}</span><span>{esc(label)}</span></div>{body}<div class="foot"><span>ZION INTERIOR &amp; FURNITURE DESIGNER · ZION FURNITURE DESIGN SYSTEM · SEM PREÇOS</span><span>UNIDADE: mm</span><span>{DATE} · {n:02d}</span></div></section>')

# ------------------------------------------------------------------ coleção
TIER = {"E": "Essential", "S": "Signature", "I": "Icon"}
COLLECTION = [
    ("DORMITÓRIO", [("ZF-BD-01", "Zion Canopy Bed", "1.720 x 2.120 x 2.200", "freijó · linho · latão · LED", "I", "descanso + romance", "Core", "peça hero · ZG-FFE-002"),
                    ("ZF-BD-02", "Zion Headboard", "1.720 x 90 x 1.300", "freijó + painel linho / rattan", "S", "aconchego", "Core", "integrada à cama ou solta (Bubble sem dossel)"),
                    ("ZF-BD-03", "Zion Night Stand", "500 x 400 x 550", "freijó · gaveta toque · latão", "S", "intimidade", "Core", "gaveta e nicho, ponto USB oculto"),
                    ("ZF-BD-04", "Zion Bed Bench", "1.400 x 400 x 450", "freijó · assento linho / couro", "E", "acolhimento", "Core", "aos pés da cama"),
                    ("ZF-BD-05", "Zion Recamier", "1.500 x 600 x 700", "freijó · estofo bouclé · Amarração", "I", "contemplação", "Core", "evolução do recamier atual"),
                    ("ZF-BD-06", "Zion Wardrobe", "1.100 x 550 x 1.700", "carvalho · portas de rattan · friso", "S", "ordem silenciosa", "Core", "cabideiro + 3 prateleiras + cofre"),
                    ("ZF-BD-07", "Zion Luggage Bench", "900 x 450 x 450", "freijó · tiras de couro", "E", "chegada", "Core", "dobrável para estoque"),
                    ("ZF-BD-08", "Zion Mirror (floor)", "600 x 40 x 1.800", "freijó · Arco no topo", "S", "vaidade leve", "Core", "espelho de chão inclinável")]),
    ("LIVING", [("ZF-LV-01", "Zion Lounge Chair", "760 x 820 x 780", "freijó · bouclé · Amarração", "S", "contemplação", "Core", "assento baixo 400, encosto Arco"),
                ("ZF-LV-02", "Zion Cocoon Chair", "Ø 900 x 1.250", "rattan trançado · almofada linho", "I", "refúgio", "Destination Floripa", "suspensa (arco A1) ou em base"),
                ("ZF-LV-03", "Zion Sofa", "2.000 x 900 x 750", "freijó · estofo linho hotelaria", "S", "acolhimento", "Core", "2 lugares; braços Arco"),
                ("ZF-LV-04", "Zion Ottoman", "600 x 600 x 400", "freijó · couro / linho", "E", "descanso", "Core", "também mesa de apoio com bandeja"),
                ("ZF-LV-05", "Zion Coffee Table", "Ø 800 x 380", "travertino sobre base freijó torneada", "S", "conexão", "Core", "tampo pedra R3"),
                ("ZF-LV-06", "Zion Side Table", "Ø 450 x 500", "freijó torneado ou tronco (Urubici)", "E", "apoio", "Core", "friso a 1/3")]),
    ("DINING", [("ZF-DN-01", "Zion Dining Table", "Ø 900 x 750", "freijó · saia Arco · base 3 pés", "S", "conexão", "Core", "evolução da mesa redonda de 90 cm"),
                ("ZF-DN-02", "Zion Dining Chair", "480 x 520 x 800", "freijó curvado · assento palhinha ou linho", "S", "leveza", "Core", "evolução da cadeira curva atual"),
                ("ZF-DN-03", "Zion Bar Chair", "440 x 480 x 1.000", "freijó · assento couro · apoio latão", "E", "convívio", "Core", "bancada da cozinha do Casulo")]),
    ("HOSPITALITY", [("ZF-HS-01", "Zion Hospitality Bar", "1.000 x 450 x 1.200", "carvalho · cristaleira rattan · latão", "I", "ritual", "Core", "evolução da cristaleira / bar"),
                     ("ZF-HS-02", "Zion Minibar Cabinet", "600 x 550 x 850", "carvalho · porta ripada · frigobar 90 L", "S", "conveniência", "Core", "ventilação oculta"),
                     ("ZF-HS-03", "Zion Coffee Station", "800 x 450 x 900", "carvalho · tampo quartzito · bandeja", "S", "manhã", "Core", "cápsulas, chaleira, xícaras"),
                     ("ZF-HS-04", "Zion Amenity Cabinet", "450 x 350 x 600", "freijó · porta rattan", "E", "cuidado", "Core", "amenities, secador, kit")]),
    ("BANHEIRO", [("ZF-BA-01", "Zion Vanity", "1.000 x 500 x 850", "quartzito / travertino · gabinete ripado suspenso", "S", "frescor", "Core", "cuba esculpida, misturador latão"),
                  ("ZF-BA-02", "Zion Bathroom Cabinet", "600 x 180 x 700", "freijó · porta espelho", "E", "ordem", "Core", "sobre a bancada"),
                  ("ZF-BA-03", "Zion Mirror (bath)", "Ø 800", "aro latão · LED perimetral", "S", "luz", "Core", "antiembaçante"),
                  ("ZF-BA-04", "Zion Amenity Shelf", "600 x 150 x 40", "travertino sobre mão-francesa latão", "E", "toque", "Core", "no nicho do banho"),
                  ("ZF-BA-05", "Zion Towel Rack", "600 x 120 x 900", "freijó · escada de 3 travessas", "E", "calor", "Core", "opção com aquecimento"),
                  ("ZF-BA-06", "Zion Bathroom Stool", "400 x 300 x 450", "teca · Amarração", "E", "pausa", "Core", "banheira / ducha")]),
    ("EXTERIOR", [("ZF-OD-01", "Zion Outdoor Lounge Chair", "800 x 900 x 780", "teca · corda náutica areia", "S", "natureza", "Core", "evolução das poltronas externas"),
                  ("ZF-OD-02", "Zion Outdoor Sofa", "1.800 x 900 x 750", "teca · corda · almofadas outdoor", "S", "reunião", "Destination Floripa", ""),
                  ("ZF-OD-03", "Zion Outdoor Table", "Ø 800 x 720", "teca · saia Arco", "E", "manhã ao ar livre", "Core", "evolução da mesa externa"),
                  ("ZF-OD-04", "Zion Day Bed", "2.000 x 1.200 x 450", "teca · corda · véu de linho", "I", "contemplação", "Core", "suspenso no Bico do Casulo ou em base"),
                  ("ZF-OD-05", "Zion Sun Lounger", "2.000 x 700 x 350", "teca · corda · encosto Arco 4 posições", "S", "sol", "Core", "evolução das espreguiçadeiras"),
                  ("ZF-OD-06", "Zion Outdoor Dining Chair", "480 x 540 x 800", "teca · corda", "E", "leveza", "Core", ""),
                  ("ZF-OD-07", "Zion Fire Pit Table", "Ø 900 x 400", "aço corten · tampo travertino em anel", "I", "noite", "Destination Urubici", "etanol ou lenha"),
                  ("ZF-OD-08", "Zion Jacuzzi Side Table", "Ø 400 x 450", "teca maciça · bandeja embutida", "E", "ritual", "Core", "à prova d'água")]),
    ("ILUMINAÇÃO", [("ZF-LT-01", "Zion Bedside Lamp", "Ø 260 x 420", "freijó torneado · cúpula linho Arco", "S", "intimidade", "Core", "evolução do abajur madeira / palha"),
                    ("ZF-LT-02", "Zion Floor Lamp", "Ø 420 x 1.550", "tripé freijó · Amarração · cúpula palha", "S", "leitura", "Core", "evolução do abajur de pé"),
                    ("ZF-LT-03", "Zion Pendant", "Ø 600 x 380", "cesto rattan", "S", "reunião", "Destination Floripa", "sobre a mesa"),
                    ("ZF-LT-04", "Zion Wall Lamp", "260 x 180", "braço latão · cúpula palha", "E", "leitura", "Core", "cabeceira"),
                    ("ZF-LT-05", "Zion Outdoor Lantern", "180 x 180 x 360", "latão / preto · vidro · vela LED", "E", "caminho", "Core", "deck, jacuzzi")]),
    ("OBJETOS", [("ZF-OB-01", "Zion Tray", "450 x 300 x 40", "freijó com borda Arco · fundo linho", "E", "serviço", "Core", "café da manhã, amenities"),
                 ("ZF-OB-02", "Zion Basket", "Ø 400 x 350", "palha / sisal", "E", "ordem", "Core", "roupa, lenha, toalhas"),
                 ("ZF-OB-03", "Zion Ceramic Collection", "serviço p/ 4", "cerâmica artesanal esmalte fosco", "S", "ritual", "Destination", "areia / musgo / terracota por destino"),
                 ("ZF-OB-04", "Zion Vase", "Ø 180 x 320", "cerâmica ou madeira torneada", "E", "natureza dentro", "Core", ""),
                 ("ZF-OB-05", "Zion Candle Holder", "Ø 90 x 120", "latão envelhecido / travertino", "E", "noite", "Core", ""),
                 ("ZF-OB-06", "Zion Decorative Sculpture", "≈ 300", "madeira de demolição / pedra do destino", "I", "memória", "Destination", "uma por unidade, do artesão local")])]

def capa():
    pages.append(f'''<section class="page cover"><div class="coverbox"><div class="brand">{zion_mark_html("13mm", color="#FEF5F0", style="margin-right:6mm")}{zion_logo_html("13mm", color="#FEF5F0")}</div><div class="sub">ZION INTERIOR &amp; FURNITURE DESIGNER · ZION NEW LUXURY FURNITURE SYSTEM</div>
<h1>ZION FURNITURE<br>DESIGN SYSTEM</h1><h3>{DOC} · {REV} · {DATE} · LUXO NA NATUREZA</h3>
<p class="lead">A linguagem proprietária do mobiliário Zion: DNA, moodboard, paleta, materiais, texturas, formas, a assinatura Zion (Arco, Pé, Amarração, Friso, Véu), as linguagens de pés, curvas, ferragens, tecidos e luminárias, o sistema de acabamentos, ZION CORE e DESTINATION DNA, os três níveis (Essential, Signature, Icon) e a coleção completa de 46 peças com códigos. Nasce do FF&amp;I histórico das Bubbles de Urubici e Florianópolis e o evolui.</p>
<p class="rule">Documento de direção de design. Dimensões em mm; onde ainda não validadas em protótipo, DIMENSÃO PROVISÓRIA; onde dependem de teste, PREMISSA. Sem preços: custos estimados só em interno/. A primeira peça desenvolvida com este sistema é a ZION CANOPY BED (ZG-FFE-002).</p></div></section>''')

def analise():
    body = h("01 · ANÁLISE DAS REFERÊNCIAS", "FF&I Zion Collection (memorial 2023, atualização 2025) · Mobília Interior Bubbles (deck) · fotos oficiais das Bubbles de Urubici e Florianópolis")
    rows = [("Cama queen dossel", "estrutura robusta de pinus / madeira envernizada, 4 colunas, travessas superiores retas, cortinas de abas (tab top) em algodão cru", "MANTER: dossel, cortinas de aba, madeira quente. EVOLUIR: proporção mais fina, arco no quadro superior, trilho oculto, luz indireta, madeira de lei"),
            ("Mesa de cabeceira", "madeira maciça envernizada com gaveta", "MANTER: gaveta. EVOLUIR: suspensa ou com pés Zion, nicho, USB e arandela integrados"),
            ("Luminárias de leitura / abajures", "madeira e palha / rattan, estilo Nature", "MANTER: fibra e madeira. EVOLUIR: cúpula em Arco, 2700 K dimerizável, base torneada"),
            ("Mesa redonda 90 cm + 4 cadeiras", "cadeiras de madeira curvada (tipo thonet) estofadas em tecido impermeável", "MANTER: mesa redonda, cadeira leve. EVOLUIR: saia Arco, base de 3 pés, assento em palhinha"),
            ("Espelho de chão", "moldura em madeira natural", "MANTER. EVOLUIR: topo em Arco, inclinável"),
            ("Poltrona", "estofada em tecido resistente com braços", "EVOLUIR: Zion Lounge Chair com Amarração e assento baixo"),
            ("Recamier", "madeira com estofado, pé da cama", "MANTER como Zion Bed Bench / Recamier"),
            ("Cristaleira / bar", "madeira maciça com portas", "EVOLUIR: Zion Hospitality Bar com portas de rattan e bandeja de latão"),
            ("Aparador do lavabo", "balcão em madeira com cuba redonda, monocomando, espelho Adnet Ø60", "EVOLUIR: Zion Vanity com tampo em pedra, gabinete ripado suspenso, espelho Ø80 com LED"),
            ("Exterior", "mesa e poltronas de madeira com pintura repelente; espreguiçadeiras; jacuzzi", "EVOLUIR: teca e corda náutica, Day Bed, Fire Pit"),
            ("Decoração", "quadro Boho, cestos, tapetes laterais, cortinas (x4), almofadas veludo verde e couro", "REDUZIR: menos objetos, mais textura; verde musgo como acento, couro caramelo")]
    body += f'<div class="two"><div>{table(["Peça atual", "Como é hoje", "Leitura Zion New Luxury"], rows, "xsmall")}</div><div>'
    body += '<h4>O QUE AS FOTOS DIZEM</h4>' + ul(["<b>A alma está certa:</b> madeira quente, cama dossel com véus claros, fibras, luz âmbar, mata em volta, deck de madeira, banheira ao ar livre.",
        "<b>O que pesa:</b> madeira de pinus com verniz brilhante e seções grossas; muitos objetos pequenos (neon, quadros, cestos); ar-condicionado aparente; mistura de estilos nas cadeiras.",
        "<b>A Bubble pede leveza:</b> o envelope é transparente, redondo e leve; o móvel precisa ser fino nos pés, baixo na cama e alto no dossel para dar escala e privacidade.",
        "<b>Assinatura já latente:</b> o dossel com cortinas é a imagem mais fotografada da Zion (ver fotos 1 a 3): é o ponto de partida do ícone.",
        "<b>Destinos diferentes:</b> Urubici (araucárias, frio, neve, lã e couro); Florianópolis (palmeiras, calor, rattan e linho). O sistema precisa de um Core e de dois DNAs."])
    body += '<h4>CONCLUSÃO</h4><p class="lede">Não é preciso reinventar a Zion: é preciso <b>afinar</b>. Mesma alma (madeira, véu, fibra, natureza), com proporções mais finas, um só motivo formal (o Arco), materiais de lei, ferragens ocultas e luz filtrada. O resultado deve parecer "a Zion que já existe, madura".</p></div></div>'
    page(body, "Análise das referências", code=f"{DOC}-01", cls="flow")
    figs = [("Bubbles_Urubici1", "Bubble de Urubici: cama dossel de pinus com cortinas de aba, mesa redonda e cadeiras curvas, recamier, banco, neon, cristaleira ao fundo."),
            ("Bubbles_Urubici8", "O dossel visto da cama: a imagem-assinatura da Zion. Madeira quente, véu claro, araucárias."),
            ("Bubbles_Urubici21", "Cabeceira de pranchas de madeira, almofadas de veludo verde musgo e couro caramelo, abajur de linho."),
            ("Bubbles_Urubici3", "Bubble, deck de madeira, jacuzzi, poste de luz: o mobiliário externo ainda é genérico."),
            ("Bubbles_Urubici5", "A cúpula e o quadro do dossel: a estrutura da cama conversa com a geometria da Bubble."),
            ("IMG_1314", "Florianópolis à noite: luz âmbar dentro da Bubble, palmeiras, cadeiras de madeira curvada e mesa redonda.")]
    body = h("01 · REFERÊNCIAS VISUAIS DA ZION", "fotos oficiais das Bubbles (Drive Zion) · DNA histórico a preservar e elevar") + '<div class="refs">' + "".join(f'<figure>{img(f"08_MOBILIARIO/referencias/{f}.jpg")}<figcaption>{esc(c)}</figcaption></figure>' for f, c in figs) + "</div>"
    page(body, "Referências visuais", code=f"{DOC}-01b")

def dna():
    body = h("02 · DNA DA COLEÇÃO", "ZION NEW LUXURY FURNITURE COLLECTION · conceito central: LUXO NA NATUREZA")
    body += '<div class="two"><div><div class="big">LUXO NA<br>NATUREZA</div><p class="quote">O luxo Zion não é excesso. É proporção, material, textura, conforto, acabamento, silêncio visual, detalhe, luz, ergonomia, exclusividade e integração com a natureza. O resultado tem de dizer uma coisa só: <b>"eu quero ficar aqui."</b></p>'
    body += '<div class="words">' + "".join(f"<span>{w}</span>" for w in ["LUXO NATURAL", "CONFORTO", "SOFISTICAÇÃO", "NATUREZA", "WELLNESS", "ROMANCE", "CONTEMPLAÇÃO", "ARTESANATO", "EXCLUSIVIDADE", "SIMPLICIDADE"]) + "</div></div><div>"
    body += "<h4>MISTURA ESTÉTICA (DOSADA)</h4>" + table(["Referência", "O que entra", "O que fica de fora"], [("Bali contemporâneo", "dossel, madeira clara, rattan, véus, tablados", "tema, esculturas de deuses, excesso de entalhe"), ("Boho chic", "fibras, macramê discreto, camadas têxteis", "cor demais, franjas, bagunça"), ("Japandi natural", "silêncio, proporção, vazio, junções honestas", "frieza, cinza"), ("Organic modern", "curvas, raios, formas contínuas", "plástico, moldados brilhantes"), ("Resort de luxo / tropical luxury", "escala generosa, cama alta no dossel, serviço", "ostentação, dourado brilhante"), ("Glamping / wellness hospitality", "montagem, transporte, manutenção, robustez", "improviso, mobiliário de camping")], "xsmall")
    body += "<h4>O QUE A ZION NÃO É</h4>" + ul(["Não é decoração temática Bali.", "Não é rústico de pousada.", "Não é boho carregado.", "Não é industrial nem cromado.", "Não é um catálogo de objetos: é um sistema de poucas peças com muita presença."]) + "</div></div>"
    page(body, "DNA da coleção", code=f"{DOC}-02")

def moodboard():
    cells = [img("08_MOBILIARIO/referencias/Bubbles_Urubici8.jpg"), '<div class="w">MADEIRA<br>QUENTE</div>', f'<div class="tx">{texture_svg("rattan")}</div>', img("08_MOBILIARIO/referencias/Bubbles_Urubici18.jpg"),
             f'<div class="sw" style="background:#DED6BF"></div>', img("08_MOBILIARIO/referencias/Bubbles_Urubici21.jpg"), '<div class="w">VÉU ·<br>LINHO ·<br>LUZ ÂMBAR</div>', f'<div class="tx">{texture_svg("linho")}</div>',
             f'<div class="tx">{texture_svg("freijo")}</div>', f'<div class="sw" style="background:#1B2117"></div>', img("08_MOBILIARIO/referencias/Bubbles_Urubici39.jpg"), '<div class="w" style="background:#8B714E;color:#FEF5F0;border:none">ARCO ·<br>PÉ · AMARRAÇÃO<br>FRISO · VÉU</div>',
             img("08_MOBILIARIO/referencias/Bubbles_Urubici12.jpg"), f'<div class="tx">{texture_svg("travertino")}</div>', f'<div class="tx">{texture_svg("couro")}</div>', f'<div class="sw" style="background:#B8834A"></div>']
    body = h("03 · MOODBOARD", "natureza fornece a cor · madeira, fibra, linho, pedra, latão · luz filtrada · o dossel como imagem") + '<div class="mood">' + "".join(cells) + "</div>"
    page(body, "Moodboard", code=f"{DOC}-03")

def paleta():
    body = h("04 · PALETA", "silenciosa · 60 % base (areia, creme, off-white) · 30 % madeira e fibra · 10 % acentos (terra, oliva, musgo, terracota, latão)")
    body += '<div class="sw-grid">' + "".join(f'<div><i style="background:{hx}"></i><b>{c}</b>{esc(n)}<br><em>{esc(hx)} · {esc(u)}</em></div>' for c, n, hx, u in PALETTE) + "</div>"
    body += '<div class="two" style="margin-top:8px"><div><h4>REGRAS</h4>' + ul(["Nenhuma cor saturada em superfície grande; a natureza (verde, céu, madeira) fornece a cor.", "Verde musgo só em têxtil de acento e metais escuros; terracota só em cerâmica (≤ 5 % do campo visual).", "Madeira: um tom principal por ambiente (freijó); nogueira em detalhe; nunca duas madeiras vermelhas.", "Preto (#040605) aparece em pontos: sapatas, cabos, parafusos aparentes, fire pit."]) + "</div><div><h4>POR DESTINO</h4>" + table(["Destino", "Base", "Madeira", "Acentos"], [("Urubici (montanha)", "areia, creme, cru", "freijó + nogueira em detalhe", "verde musgo, caramelo (couro), lã cru, preto"), ("Florianópolis (praia / mata)", "off-white, areia clara", "freijó claro, bambu, carvalho", "verde oliva, terracota discreta, latão, palha")], "small") + "</div></div>"
    page(body, "Paleta", code=f"{DOC}-04")

def materiais():
    body = h("05 · MATERIAIS", "priorizar madeira maciça certificada, fibras naturais, linho, couro, pedra, cerâmica, latão envelhecido · evitar MDF aparente, plástico, cromado, brilho")
    body += '<div class="two"><div><h4>MADEIRAS</h4>' + table(["Cód.", "Material", "Uso", "Acabamento", "Notas"], WOODS, "xsmall") + "<h4>FIBRAS</h4>" + table(["Cód.", "Material", "Uso", "Notas"], FIBERS, "xsmall") + "</div><div><h4>PEDRA E CERÂMICA</h4>" + table(["Cód.", "Material", "Uso", "Acabamento"], STONES, "xsmall") + "<h4>METAIS</h4>" + table(["Cód.", "Material", "Uso", "Notas"], METALS, "xsmall")
    body += "<h4>QUANDO O INDUSTRIALIZADO É NECESSÁRIO (ESCALA)</h4>" + ul(["MDF naval só como núcleo de painéis largos, sempre revestido de lâmina natural com bordas em madeira maciça (nunca fita de borda aparente).", "Compensado naval curvado nas cascas de poltrona e cabeceira (leve, estável), revestido.", "Espumas certificadas D28 / D33 + manta; nunca espuma aparente.", "Fibra sintética só no externo exposto à chuva; sempre no tom areia."]) + "</div></div>"
    page(body, "Materiais", code=f"{DOC}-05", cls="flow")

def texturas():
    tx = [("rattan", "ZR-01 Palhinha sextavada", "encostos, portas, cabeceira"), ("palha", "ZR-02 Palha trançada", "cúpulas, cestos"), ("linho", "ZT-01 Linho lavado", "véus, cortinas, capas"), ("ripado", "ZW-02 Ripado de carvalho", "frentes, closet, painéis"), ("travertino", "ZS-01 Travertino bruto", "tampos, bandejas"), ("couro", "ZT-04 Couro vegetal caramelo", "assentos, alças"), ("la", "ZT-05 Lã bouclé / tecida", "poltronas, tapetes (Urubici)"), ("freijo", "ZW-01 Freijó a óleo", "toda a estrutura")]
    body = h("06 · TEXTURAS", "a textura faz o trabalho da cor: cada peça combina 2 ou 3 texturas, nunca mais") + '<div class="tx-grid">' + "".join(f'<div>{texture_svg(k)}<b>{esc(n)}</b>{esc(u)}</div>' for k, n, u in tx) + "</div>"
    body += '<p class="note">Regra de combinação: 1 madeira + 1 fibra ou tecido + 1 toque (latão, pedra ou couro). Exemplo: Canopy Bed = freijó + linho + latão. Lounge Chair = freijó + bouclé + corda.</p>'
    page(body, "Texturas", code=f"{DOC}-06")

def formas():
    body = h("07 · FORMAS E 08 · ASSINATURA ZION", "um único motivo (o Arco), três raios, um pé, uma amarração, um friso e um véu: cinco gestos discretos que fazem a peça ser reconhecida pelo desenho, sem logo")
    body += f'<div class="diag2"><div>{arc_diagram()}<b>1 · ARCO ZION</b>Flecha = vão / 12. Vem da geometria das cabanas (arcos do Casulo, cúpula da Bubble) e aparece uma vez por peça, sempre no topo ou na saia.</div><div>{radius_svg()}<b>2 · RAIOS ZION</b>R1 12 mm na aresta que a mão toca, R2 24 mm no canto que o olho vê, R3 60 mm nos volumes estofados e cúpulas.</div></div>'
    page(body, "Formas e assinatura 1", code=f"{DOC}-07")
    body = h("08 · ASSINATURA ZION (CONTINUAÇÃO)", "amarração, friso e véu")
    body += f'<div class="diag"><div>{weave_svg()}<b>3 · AMARRAÇÃO ZION</b>A corda que esconde a ferragem e marca o encontro estrutural. Artesanato visível, repetível em série.</div><div>{friso_svg()}<b>4 · FRISO ZION</b>Rebaixo de sombra a 1/3 da altura: alinha todas as frentes e faz o volume flutuar.</div><div>{veil_svg()}<b>5 · VÉU ZION</b>O tecido pertence à estrutura: trilho oculto no quadro, cortina de abas, nunca varão aparente.</div></div>'
    body += '<h4>REGRA DA ASSINATURA</h4><p class="lede">Cada peça usa <b>de 2 a 4</b> dos cinco gestos; a peça hero (Canopy Bed) usa os cinco. O logo Zion aparece só gravado a fogo (12 mm) na face interna de uma travessa, nunca na face visível.</p>'
    page(body, "Formas e assinatura 2", code=f"{DOC}-08")

def pes():
    body = h("09 · LINGUAGEM DOS PÉS", "pé cônico inclinado 8° em freijó maciço, sapata de latão 15 mm com nivelador oculto · quatro escalas, uma família")
    body += '<div class="diag5">' + "".join(f"<div>{leg_svg(t, b_, hh, 8, n, s)}</div>" for t, b_, hh, n, s in ((28, 20, 420, "PÉ 1 · CADEIRA", "28 → 20 mm · h 420"), (40, 30, 380, "PÉ 2 · POLTRONA / SOFÁ", "40 → 30 mm · h 380 (assento 400)"), (55, 40, 700, "PÉ 3 · MESA", "55 → 40 mm · h 700"), (70, 55, 350, "PÉ 4 · CAMA / BANCO", "70 → 55 mm · h 350"), (32, 32, 1550, "TRIPÉ · LUMINÁRIA", "32 mm reto · Amarração no topo")))
    body += "</div><h4>REGRAS</h4>" + ul(["Seção quadrada com R1 nas arestas; cônico nas 2 faces externas, reto nas internas (fabricação em série numa só operação).", "Inclinação 8° para fora nos pés de cadeira, poltrona e mesa; pés de cama e closet retos (estabilidade e limpeza).", "Sapata de latão envelhecido 15 mm em todos: protege do piso úmido da Bubble e do deck; nivelador M8 embutido (± 10 mm).", "Pé nunca toca o tampo diretamente: entra em travessa ou anel (Amarração ou parafuso de cama)."])
    page(body, "Linguagem dos pés", code=f"{DOC}-09")

def ferragens_tecidos():
    body = h("10 · LINGUAGEM DAS FERRAGENS · 11 · LINGUAGEM DOS TECIDOS", "ferragem oculta ou em latão envelhecido · tecidos naturais com desempenho de hotelaria")
    body += f'<div class="two"><div>{hardware_svg()}<p class="note">Regra: nada cromado, nada brilhante, nada de plástico visível. Toda ferragem aparente é latão envelhecido ou preto fosco; toda a estrutural é oculta e desmontável (parafuso de cama, Minifix) para transporte e manutenção.</p></div><div>{table(["Cód.", "Tecido", "Uso", "Cores", "Especificação"], TEXTILES, "xsmall")}<p class="note">Estofos hoteleiros: ≥ 40.000 ciclos Martindale, tratamento antimancha à base de água (sem brilho), capas removíveis com zíper oculto, espuma D28 assento / D23 encosto + manta 200 g. Cortinas: linho lavado, barra de 6 cm, abas costuradas a cada 150 mm.</p></div></div>'
    page(body, "Ferragens e tecidos", code=f"{DOC}-10")

def luminarias():
    body = h("12 · LINGUAGEM DAS LUMINÁRIAS", "luz que passa por fibra ou linho · 2700 K · dimerizável · madeira torneada e latão · cinco tipologias")
    body += lamp_svg()
    body += '<div class="two" style="margin-top:8px"><div><h4>CENAS POR AMBIENTE</h4>' + table(["Cena", "Luminárias", "Nível"], [("Chegada", "pendente + arandelas + LED do dossel", "60 %"), ("Jantar", "pendente sobre a mesa, bedside a 20 %", "40 %"), ("Noite", "LED do dossel + bedside", "10 %"), ("Banho", "espelho LED + vigília no rodapé", "30 %"), ("Deck", "lanternas + balizadores", "20 %")], "small") + "</div><div><h4>REGRAS</h4>" + ul(["Nenhum LED visível: sempre atrás de linho, palha ou madeira; fitas em perfil com difusor opalino.", "Fonte de luz substituível (E27 / G9 / fita 24 V) sem desmontar a luminária.", "Cabos têxteis areia; plugues e dimmers em latão ou preto fosco.", "Externo IP65, banho IP44, lanterna recarregável USB-C (sem fio no deck)."]) + "</div></div>"
    page(body, "Linguagem das luminárias", code=f"{DOC}-12")

def acabamentos():
    body = h("13 · SISTEMA DE ACABAMENTOS", "códigos de acabamento para especificar qualquer peça em uma linha: madeira + fibra/tecido + metal + pedra")
    rows = [("ZW-01-O", "Freijó a óleo natural", "fosco, toque de madeira, retoque em obra", "estruturas internas, camas, cadeiras"), ("ZW-01-V", "Freijó verniz PU fosco 10 %", "mais resistente a manchas", "mesas, tampos, hospitality"), ("ZW-02-V", "Carvalho verniz PU fosco 10 %", "lâmina + maciço nas bordas", "closet, portas, ripados"), ("ZW-03-O", "Nogueira a óleo", "só em detalhes", "frisos, cavilhas, puxadores"), ("ZW-04-T", "Teca / cumaru a óleo de teca", "externo; opção acinzentar", "exterior"),
            ("ZR-01-N", "Rattan natural verniz fosco à base de água", "cana 2,5 mm sextavada", "encostos, portas, cabeceira"), ("ZR-02-N", "Palha trançada natural", "", "cúpulas, cestos"), ("ZR-03-C", "Corda algodão cru Ø8 (interno) · poliéster areia (externo)", "", "Amarração, assentos"),
            ("ZT-01-OW", "Linho lavado off-white", "220 g/m²", "véus, cortinas"), ("ZT-02-SA", "Linho hotelaria areia", "≥ 40.000 Martindale", "estofos"), ("ZT-02-OL", "Linho hotelaria oliva", "acento", "almofadas, assento de cadeira"), ("ZT-03-CR", "Bouclé creme", "≥ 50.000 Martindale", "lounge, cocoon"), ("ZT-04-CA", "Couro vegetal caramelo 1,6 mm", "pátina", "assentos, alças"),
            ("ZM-01-B", "Latão envelhecido escovado", "sem verniz", "sapatas, ferragens, luminárias"), ("ZM-02-P", "Aço pintado preto fosco (pó)", "textura fina", "estruturas ocultas, externo"), ("ZS-01-T", "Travertino romano escovado", "sem resina", "tampos, bandejas"), ("ZS-02-Q", "Quartzito areia acetinado", "30 mm", "bancadas")]
    body += table(["Código", "Acabamento", "Notas", "Onde"], rows, "xsmall")
    body += '<p class="note">Exemplo de especificação de uma peça: <b>ZF-LV-01 Zion Lounge Chair · ZW-01-O + ZT-03-CR + ZR-03-C + ZM-01-B</b> (freijó a óleo, bouclé creme, corda cru, sapata de latão).</p>'
    page(body, "Sistema de acabamentos", code=f"{DOC}-13", cls="flow")

def core_dna():
    body = h("14 · ZION CORE · 15 · DESTINATION DNA", "o que permanece em todas as unidades e o que muda com o destino, sem perder o DNA")
    body += '<div class="two"><div><h4>ZION CORE (TODAS AS UNIDADES)</h4>' + ul(["Os cinco gestos da assinatura (Arco, Pé, Amarração, Friso, Véu).", "Freijó como madeira estrutural; latão envelhecido como metal; linho como tecido do véu.", "Paleta base areia / creme / off-white; luz 2700 K filtrada.", "Camas: Canopy Bed com dossel e véus; cabeceira integrada; luz indireta.", "Proporções: assento 400 a 420, mesa 750, cama 600 (superfície de dormir), dossel 2.200.", "Ferragens ocultas, desmontagem sem ferramenta especial, sapatas com nivelador.", "Peças em módulos ≤ 1,20 m que passam pela porta (Bubble 0,90 · Casulo 1,00)."]) + "</div><div><h4>DESTINATION DNA</h4>" + table(["", "URUBICI · montanha", "FLORIANÓPOLIS · praia e mata"], [("Sensação", "aconchego, lareira, neve, araucária", "brisa, palmeira, areia, Bali contemporâneo"), ("Madeira", "freijó + nogueira em detalhe, tronco de araucária caída em mesas", "freijó claro, bambu laminado, carvalho"), ("Fibra / têxtil", "lã tecida, couro caramelo, bouclé, manta", "rattan, palha, linho, algodão cru, juta"), ("Pedra", "basalto / pedra local em objetos, travertino", "travertino claro, cerâmica areia"), ("Acentos", "verde musgo, caramelo, preto", "verde oliva, terracota discreta, latão"), ("Peças exclusivas", "Fire Pit Table, Lounge Chair em couro, mantas de lã, escultura em madeira de araucária", "Cocoon Chair de rattan, Day Bed com véu, pendente cesto, cerâmica praiana"), ("Cortinas", "linho areia mais pesado (280 g)", "linho off-white leve (180 a 220 g)")], "small") + "</div></div>"
    page(body, "Core e Destination DNA", code=f"{DOC}-14")

def tiers():
    body = h("16 · SISTEMA MODULAR · ESSENTIAL · SIGNATURE · ICON", "três níveis com a mesma linguagem: eficiência, acabamento e autoria")
    body += '<div class="tiers"><div><b>ZION ESSENTIAL</b>Eficiência. Peças de apoio produzidas em série (10 a 500): pés Zion, R1/R2, linho hotelaria, ferragem oculta. Marcenaria CNC + montagem. Custo controlado; 1 gesto de assinatura.<br><br><i>Bench, Ottoman, Side Table, Bar Chair, Amenity Cabinet, Towel Rack, Wall Lamp, Tray, Basket.</i></div>'
    body += '<div><b>ZION SIGNATURE</b>Maior acabamento. Madeira maciça com Arco, fibra natural, 2 a 3 gestos. Produzidas em lotes (10 a 100) por marcenaria parceira com controle de amostra.<br><br><i>Headboard, Night Stand, Wardrobe, Mirror, Lounge Chair, Sofa, Coffee Table, Dining Table e Chair, Minibar, Coffee Station, Vanity, Outdoor Lounge, Sun Lounger, Bedside e Floor Lamp, Pendant.</i></div>'
    body += '<div><b>ZION ICON</b>Peças autorais e memoráveis, com os 5 gestos, artesanato visível (Amarração, palhinha, torneado) e história. Produção em pequena série (1 a 50) por artesão ou oficina certificada; numeradas.<br><br><i>Canopy Bed, Recamier, Cocoon Chair, Hospitality Bar, Day Bed, Fire Pit Table, Decorative Sculpture.</i></div></div>'
    body += '<h4>ESCALA: 1 · 10 · 50 · 100 · 500 UNIDADES</h4>' + table(["Escala", "Como produzir", "O que muda"], [("1 (protótipo)", "artesão / marcenaria local, ajuste de gabaritos, fotos", "todas as dimensões viram REV 01"), ("10", "1 marcenaria parceira, gabaritos fixos, kit de ferragens padronizado", "capas e cortinas em confecção separada"), ("50", "2 marcenarias homologadas, peças CNC (pés, quadros, painéis), estofaria própria", "lâmina em painéis largos; controle por amostra-mestre"), ("100", "linha de produção: freijó em lotes, torneados e curvados em fornecedor especializado, embalagem padrão", "componentes intercambiáveis entre peças (pés, travessas, sapatas)"), ("500", "industrialização parcial: maciço + lâmina, fibra sintética no externo, estoque de reposição de componentes", "manter os 5 gestos e a madeira nas superfícies de toque")], "small")
    page(body, "Tiers e escala", code=f"{DOC}-16")

def colecao():
    for i in range(0, len(COLLECTION), 4):
        chunk = COLLECTION[i:i + 4]
        body = h("17 · COLEÇÃO COMPLETA · 46 PEÇAS", f"códigos ZF-<categoria>-<nn> · dimensões L x P x A em mm (provisórias até o protótipo) · tier E / S / I · sensação do hóspede · Core ou Destination")
        for cat, rows in chunk:
            body += f"<h4>{esc(cat)}</h4>" + table(["Cód.", "Peça", "L x P x A (mm)", "Materiais", "Tier", "Sensação", "Core / Destino", "Notas"], [(c, f"<b>{esc(n)}</b>", d, esc(m), TIER[t], esc(s), esc(k), esc(o)) for c, n, d, m, t, s, k, o in rows], "xsmall")
        page(body, "Coleção", code=f"{DOC}-17", cls="flow")

def regras():
    body = h("18 · EXPERIÊNCIA · 19 · INSTAGRAMABILITY · 23 · REGRA DE DESIGN", "cada peça responde a uma sensação; cada peça passa por 10 perguntas antes de ser aprovada")
    body += '<div class="two"><div><h4>O QUE O HÓSPEDE SENTE</h4>' + table(["Peça", "Sensação", "Como o desenho entrega"], [("Cama", "descanso + romance", "dossel alto, véus, luz indireta, cabeceira macia, colchão a 600 mm"), ("Poltrona", "contemplação", "assento baixo e profundo, encosto Arco, voltada para a mata"), ("Mesa", "conexão", "redonda, 3 pés (ninguém senta num pé), tampo quente ao toque"), ("Sofá", "acolhimento", "braços largos, almofadas soltas, tecido macio"), ("Iluminação", "intimidade", "2700 K, fibra, dimmer, nenhum ponto de luz visível"), ("Externo", "natureza", "teca e corda, formas que envelhecem bem, sem plástico")], "small")
    body += "<h4>FOTOGENIA SEM SACRIFICAR CONFORTO</h4>" + ul(["Silhueta reconhecível a 10 m (dossel com Arco, tripé da luminária, Cocoon Chair).", "Texturas que fotografam: palhinha em contraluz, linho com dobras, sombra do friso.", "Enquadramentos pensados: cama vista da porta, poltrona contra o vidro, day bed sob o Bico.", "Nunca uma peça só porque 'fica bonita': ergonomia (assento 400 a 420, encosto 100° a 105°) e limpeza primeiro."]) + "</div><div><h4>AS 10 PERGUNTAS</h4><ol class='num q10'>" + "".join(f"<li>{q}</li>" for q in ["Parece Zion?", "Parece luxo?", "Parece natural?", "Parece confortável?", "É atemporal?", "É fotografável?", "Pode ser fabricada?", "Pode ser replicada?", "É adequada para hotelaria?", "Melhora a experiência do hóspede?"]) + "</ol><p class='note'>Uma resposta negativa devolve a peça ao refinamento. As respostas ficam registradas no documento da peça (seção 13 · Regra de design).</p>"
    body += "<h4>PROCESSO (21)</h4><p class='lede'>01 análise · 02 moodboard · 03 DNA · 04 materiais · 05 formas · 06 sketch · 07 três conceitos · 08 comparação · 09 seleção · 10 refinamento · 11 render · 12 dimensões · 13 desenho técnico · 14 explodido · 15 BOM · 16 especificação · 17 fabricação. Nunca começar pelo render.</p></div></div>"
    page(body, "Experiência e regra de design", code=f"{DOC}-18")

def proximos():
    body = h("PRÓXIMOS PASSOS E REVISÃO", "da peça hero à coleção")
    body += '<div class="two"><div>' + ol(["<b>ZION CANOPY BED (ZG-FFE-002):</b> três conceitos, seleção, desenho técnico, explodido, BOM, fabricação, montagem, manutenção; protótipo em Urubici.", "Após o protótipo: REV 01 do sistema com as dimensões validadas e o gabarito dos pés e do Arco.", "Dormitório completo (Headboard, Night Stand, Bench, Wardrobe, Mirror) com o mesmo método.", "Living e Dining; depois Hospitality, Banheiro, Exterior, Iluminação e Objetos.", "Book da coleção (catálogo com renders e fichas) e manual de especificação para os projetos de interiores das cabanas (ZC-INT, ZS-INT, ZL-INT, ZK-INT)."]) + "</div><div>" + table(["Rev", "Data", "Descrição", "Autor"], [("00", DATE, "Emissão inicial do Zion Furniture Design System a partir do FF&I 2023-2025 e das fotos das Bubbles", "Zion Interior & Furniture Designer")], "small") + "<h4>ARQUIVOS</h4>" + ul(["08_MOBILIARIO/ZG-FFE-001_Zion_Furniture_Design_System.html / .pdf", "08_MOBILIARIO/referencias/ (fotos oficiais das Bubbles)", "tools/furniture_common.py (paleta, materiais, diagramas da assinatura) · tools/furniture_system.py", "ZG-FFE-002_Zion_Canopy_Bed (peça hero)"]) + "</div></div>"
    page(body, "Próximos passos", code=f"{DOC}-99")

def build():
    capa(); analise(); dna(); moodboard(); paleta(); materiais(); texturas(); formas(); pes(); ferragens_tecidos(); luminarias(); acabamentos(); core_dna(); tiers(); colecao(); regras(); proximos()
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · {DOC} · Furniture Design System</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    path = os.path.join(OUT_DIR, f"{DOC}_Zion_Furniture_Design_System.html"); open(path, "w", encoding="utf-8").write(doc); print(os.path.relpath(path, ROOT), len(pages), "páginas")

if __name__ == "__main__":
    build()

# -*- coding: utf-8 -*-
"""ZG-ARQ-001 · DOCUMENTO CONCEITUAL E VISUAL da Zion Glamping Collection (Fase 02 do método).
Conceito, partido, linguagem, materialidade, experiência do hóspede, e para cada uma das seis unidades: volumetria,
implantação, relação com a natureza, circulação, iluminação natural, ventilação, privacidade, vistas, acessos, manutenção
e operação hoteleira. A4 paisagem, tema escuro Zion, vetorial. Saída: 02_CONCEITO/ZG-ARQ-001_Documento_Conceitual_Visual.html
PDF: node export_pdf.js ../02_CONCEITO/ZG-ARQ-001_Documento_Conceitual_Visual.html ../02_CONCEITO/ZG-ARQ-001_Documento_Conceitual_Visual.pdf"""
import os, html
from build_projeto_arquitetonico import svg_inline
from svgkit import zion_mark_html, zion_logo_html, ZION_Z
from geometry import Cocoon, Zenith, LODGES, Capsule
import ffe

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(ROOT, "02_CONCEITO"); os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "ZG-ARQ-001_Documento_Conceitual_Visual.html")
DOC = "ZG-ARQ-001"; REV = "REV 00 — CONCEITO"; DATE = "17/09/2026"
LG = {k: v() for k, v in LODGES.items()}; CAP = Capsule()

def esc(s): return html.escape(str(s))
def fmt(v, n=1): return f"{v:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def exists(rel): return os.path.exists(os.path.join(ROOT, rel))
def img(rel, cls=""):
    rel = rel.replace("/renders/web/", "/renders/web/deck/")
    return f'<img class="{cls}" src="../{rel}" alt="">' if exists(rel) else '<div class="ph"></div>'
def sheet(rel, cls=""): return f'<div class="sheet {cls}">{svg_inline(rel)}</div>' if exists(rel) else f'<div class="sheet missing">[{esc(rel)}]</div>'

pages = []
def page(body, cls="", label=""):
    n = len(pages) + 1
    pages.append(f'<section class="page {cls}">{body}<div class="foot"><span>ZION GLAMPING · {DOC} · {REV}</span><span>{esc(label)}</span><span>{DATE} · {n:02d}</span></div></section>')

# ---------------------------------------------------------------------------- conteúdo
UNITS = [
    dict(code="cocoon", tag="ZC", name="ZION CASULO", fam="Cabana biomórfica em casulo", cat="SIGNATURE", area=48.0, ext=29.9, guests="2 + 1", bed="1 king",
         hero="cocoon/renders/web/cocoon_ext_front.jpg", imgs=["cocoon/renders/web/cocoon_night.jpg", "cocoon/renders/web/cocoon_int_living.jpg", "cocoon/renders/web/cocoon_int_bed.jpg", "cocoon/renders/web/cocoon_ext_aerial.jpg"],
         plan="cocoon/desenhos/02_planta_humanizada.svg", iso="cocoon/desenhos/08_isometrica.svg",
         concept="Uma concha assimétrica de oito arcos elípticos: frente cheia, aberta ao vale por um anel de vidro inclinado 8°, e cauda afilada que guarda o banho. A Espinha de Luz corre a cumeeira; seis Janelas Olho recortam a membrana como lentes. O hóspede entra pelo vestíbulo, atravessa o estar e dorme com a cabeça voltada para a cauda e os pés para a paisagem.",
         partido="Casulo e concha: uma forma que abraça o chão e sobe sem quinas, como uma semente pousada na clareira. A assimetria (frente n = 4, cauda n = 3) faz a cabana ter frente e costas, direção e abrigo.",
         sig=["Espinha de Luz: clarabóia contínua de 4,70 m na cumeeira, sobre a cama e o estar", "Bico: a membrana continua 2,40 m além do anel frontal, em balanço sobre o deck, e a ponta se ergue a 4,42 m: uma pontinha que abriga o deck e dá ao casulo a expressão de asa", "Seis Janelas Olho: lentes elípticas de 1,60 x 0,95 m, recortadas na membrana, cada uma emoldurando um pedaço de mata", "Cauda com banheira: o banho ocupa a ponta afilada, sob um Olho, com vista privada"],
         func=dict(implantacao="Eixo longitudinal perpendicular à curva de nível, frente (vidro) para o vale ou para a mata aberta, cauda para a encosta. Deck de 29,9 m² no lado do sol da manhã.",
                   circulacao="Escada ou rampa → deck → vestíbulo (2,4 m²) → estar → suíte → banho na cauda. Um único eixo, sem corredores; a marcenaria baixa faz a divisão.",
                   luz="Fachada frontal inteira em vidro, Espinha de Luz na cumeeira e seis Olhos laterais: luz de três direções, sem ponto cego. Blackout motorizado no vidro frontal e telas nos Olhos.",
                   ventilacao="Cruzada: porta de correr frontal + Olhos basculantes na suíte e no banho + exaustão no ático. Câmara ventilada de 60 mm sob a membrana retira o calor da casca.",
                   privacidade="Os Olhos são altos (peitoril 1,10 a 1,45 m) e a cauda opaca vira as costas ao caminho. Lotes de 30 x 24 m com a frente sempre desencontrada da cabana vizinha.",
                   vistas="A vista principal é a da fachada de vidro, enquadrada pelo anel inclinado; os Olhos oferecem seis recortes verticais da mata; a banheira tem o seu próprio Olho.",
                   acessos="Acesso de hóspedes pelo deck; acesso técnico pela cauda (tampa do ático, condensadora, hidráulica) sem entrar na unidade.",
                   manutencao="Membrana lavável, sem calha aparente (calha oculta no rodapé); vidros acessíveis do deck e do chão; ático técnico pela tampa da cauda; deck em cumaru com fixação oculta e réguas substituíveis.",
                   operacao="Governança em 35 min: um eixo, banho na ponta, marcenaria fechada; enxoval em 3 jogos; mini cozinha (indução, forno, geladeira, air fryer) e cofre embutidos; sensores de presença e fechadura digital para check-in sem recepção.")),
    dict(code="zenith", tag="ZS", name="ZION SAFARI", fam="Cabana escultural de dois cumes", cat="SIGNATURE", area=48.4, ext=28.0, guests="2 + 1", bed="1 king",
         hero="zenith/renders/web/zenith_ext_front.jpg", imgs=["zenith/renders/web/zenith_night.jpg", "zenith/renders/web/zenith_int_living.jpg", "zenith/renders/web/zenith_int_bed.jpg", "zenith/renders/web/zenith_ext_aerial.jpg"],
         plan="zenith/desenhos/02_planta_humanizada.svg", iso="zenith/desenhos/08_isometrica.svg",
         concept="Dois cumes deslocados em diagonal, 5,80 m sobre a cama e 4,60 m sobre a Ilha do Café, erguidos por mastros com coroas de três braços. A membrana cai em catenárias até sete postes estaiados; o Óculo do Zênite abre o céu sobre o dormir e o Respiro tira o ar quente pela chaminé do cume.",
         partido="Tenda escultural: a membrana é a arquitetura. Dois picos assimétricos dão à silhueta um perfil de montanha; o corpo baixo (2,75 m) guarda a escala doméstica sob a grande cobertura.",
         sig=["Óculo do Zênite: clarabóia circular Ø1,20 no cume alto, exatamente sobre a cama", "Respiro: chaminé de ventilação no cume baixo, com tela e tampa motorizada", "Totem do mastro: o mastro M2 atravessa a suíte revestido em madeira, com prateleiras e luz", "Terraço com hidromassagem e passarela: o deck se desdobra para fora da sombra da membrana"],
         func=dict(implantacao="Cumes alinhados com a diagonal do lote; o cume alto sobre a suíte fica a favor do vento dominante para o Respiro trabalhar. Passarela de 7,6 m² liga a trilha ao terraço.",
                   circulacao="Passarela → terraço → porta de correr → lounge e Ilha do Café → suíte → closet → banho com bancada dupla. Programa em L, com o banho na sombra do cume baixo.",
                   luz="Fachada frontal de vidro sob o beiral, Óculo do Zênite sobre a cama, fresta contínua entre corpo e membrana (luz rasante no forro).",
                   ventilacao="Efeito chaminé pelo Respiro no cume, admissão pelas esquadrias baixas; membrana dupla com câmara ventilada; evaporadora dutada para os dias sem vento.",
                   privacidade="O corpo opaco (SIP + ripado) fecha as laterais; a membrana desce até 2,20 m nas bordas e esconde o interior de quem passa. Terraço voltado para o lado sem vizinho.",
                   vistas="Vista frontal sob a asa da membrana, vista do céu pelo Óculo, e a paisagem em contraluz pela fresta alta quando se está deitado.",
                   acessos="Hóspedes pela passarela; técnico pela cauda (postes estaiados afastados do caminho, condensadora e hidráulica sob o corpo, acesso pelo deck de serviço).",
                   manutencao="Membrana em painéis substituíveis por gomo; cabos e esticadores acessíveis do chão; postes estaiados com tensão verificada a cada 6 meses; hidromassagem com casa de máquinas sob o terraço.",
                   operacao="Governança em 40 min; a Ilha do Café concentra o serviço de quarto; a hidromassagem exige rotina diária de tratamento (kit e checklist); vela e membrana toleram chuva sem interdição.")),
    dict(code="lodge", tag="ZL", name="ZION LODGE 38", fam="Pavilhão octogonal com Lanterna Zion", cat="PREMIUM", area=LG["lodge"].floor_area(), ext=LG["lodge"].deck_area(), guests="2 + 1", bed="1 king",
         hero="lodge/renders/web/lodge_ext_front.jpg", imgs=["lodge/renders/web/lodge_night.jpg", "lodge/renders/web/lodge_int_living.jpg", "lodge/renders/web/lodge_int_bed.jpg", "lodge/renders/web/lodge_ext_aerial.jpg"],
         plan="lodge/desenhos/02_planta_humanizada.svg", iso="lodge/desenhos/08_isometrica.svg",
         concept="Um pavilhão octogonal de 6,80 m entre faces, com cinco faces de vidro e três opacas que guardam o banho. Oito caibros sobem do anel de beiral à Lanterna Zion, um anel de vidro que despeja luz zenital sobre a cama; uma vela de sombra independente prolonga o deck em três faces.",
         partido="Pavilhão e lanterna: a planta centrada faz da cama o centro geométrico da cabana e a luz do cume o seu foco. O octógono dá 360° de leitura da paisagem sem perder a parede de apoio.",
         sig=["Lanterna Zion: anel de vidro de 0,45 m no cume, Ø1,50, com tampa ventilada", "Vela de sombra: membrana independente em dois postes que prolonga o deck sem tocar a cobertura", "Cinco faces de vidro, três opacas: banho com banheira de sentar sob fresta alta", "Parede-corda: o ripado da cabeceira separa suíte e banho sem chegar ao forro"],
         func=dict(implantacao="Face frontal (porta) para a vista principal; as duas faces opacas para o acesso de serviço. Deck em três faces com a vela orientada para o sol da tarde.",
                   circulacao="Deck → porta de correr PC1 → estar → suíte central → passagem para o banho no segmento posterior. Circulação em anel ao redor da cama.",
                   luz="Cinco faces envidraçadas mais a lanterna: luz difusa o dia inteiro e um feixe zenital ao meio-dia sobre a cama; tela circular motorizada na lanterna.",
                   ventilacao="Lanterna com tampa ventilada = saída alta; portas e frestas baixas = admissão; câmara ventilada entre membrana e forro.",
                   privacidade="Três faces opacas para o lado do caminho; cortinas de linho + blackout nas cinco faces de vidro; deck em três faces que cria a zona privada externa.",
                   vistas="Panorâmica de 225° do estar e da cama; vista alta do banho pela fresta; céu pela lanterna.",
                   acessos="Hóspedes pela face frontal; técnico pelo ático (evaporadora, quadro) e pela face posterior (condensadora, hidráulica).",
                   manutencao="Membrana em 8 gomos independentes; lanterna com vidro removível de dentro; deck e vela sem contato com a cobertura, cada um com sua rotina.",
                   operacao="Governança em 30 min: planta compacta e sem corredor; banho separado por parede-corda facilita a limpeza; menor kit da linha com renders (9 dias de montagem).")),
    dict(code="lodge24", tag="ZL24", name="ZION LODGE 24", fam="Octógono compacto para casal", cat="STANDARD", area=LG["lodge24"].floor_area(), ext=LG["lodge24"].deck_area(), guests="2", bed="1 king",
         hero="lodge24/desenhos/08_isometrica.svg", imgs=[], plan="lodge24/desenhos/01_conceito.svg", iso="lodge24/desenhos/08_isometrica.svg",
         concept="Octógono de 5,40 m entre faces para casal: três faces de vidro concentradas na paisagem, cinco opacas para privacidade em implantações densas, lanterna Ø1,20 sobre a cama e deck de uma face com vela de sombra. Programa completo em 24 m²: cama king, café, closet e banho com chuveiro.",
         partido="A unidade de adensamento da linha: o mesmo pavilhão do Lodge 38, menor e mais fechado, para clusters de 12 a 16 unidades por hectare sem perder a lanterna nem o deck.",
         sig=["Lanterna Zion Ø1,20 sobre a cama", "Três faces de vidro voltadas para a vista, cinco faces opacas", "Deck de uma face com vela em dois postes", "Kit mais leve da linha: 8 pilares, 8 caibros, 15 estacas, 6 dias de montagem"],
         func=dict(implantacao="Frente de vidro para a vista; as cinco faces opacas absorvem o caminho e os vizinhos. Permite implantação em fileira com 8 m entre unidades.",
                   circulacao="Deck → porta → estar com duas poltronas → cama sob a lanterna → banho ao fundo.",
                   luz="Três faces de vidro e a lanterna; a janela do café e a fresta do banho completam a luz nas faces opacas.",
                   ventilacao="Lanterna ventilada como saída; porta e janela do café como admissão.",
                   privacidade="A mais privada da linha: 5 faces opacas e deck voltado só para a vista.",
                   vistas="Vista frontal em 135° a partir das poltronas e da cama.",
                   acessos="Hóspedes pela frente; técnico pela face posterior (condensadora e hidráulica).",
                   manutencao="Idêntica ao Lodge 38, com 8 gomos menores; sem ático (split de parede).",
                   operacao="Governança em 25 min; sem banheira; ideal para operação de alto giro.")),
    dict(code="lodge28", tag="ZL28", name="ZION LODGE 28", fam="Octógono alongado com terraço", cat="PREMIUM", area=LG["lodge28"].floor_area(), ext=LG["lodge28"].deck_area(), guests="2 + 1", bed="1 king",
         hero="lodge28/desenhos/08_isometrica.svg", imgs=[], plan="lodge28/desenhos/01_conceito.svg", iso="lodge28/desenhos/08_isometrica.svg",
         concept="Octógono alongado de 4,20 x 7,80 m com duas Lanternas Zion em cumeeira, uma sobre a cama e outra sobre o estar; cinco faces de vidro, banho no fundo com fresta alta e terraço de 17,5 m² em três faces com vela de sombra.",
         partido="O Lodge esticado: o octógono ganha um corpo reto entre duas lanternas e o programa se organiza em sequência (deck, estar, suíte, banho), como um vagão de paisagem.",
         sig=["Duas Lanternas Zion Ø1,10 ligadas por cumeeira reta", "Programa em sequência: estar junto ao vidro, suíte ao centro, banho no fundo", "Terraço de 17,5 m² em três faces com vela", "10 caibros, 21 estacas, 8 dias de montagem"],
         func=dict(implantacao="Eixo longo perpendicular à vista; terraço e face frontal para o vale; fundo opaco (banho) para a encosta ou o caminho.",
                   circulacao="Terraço → estar → suíte → banho, em linha; passagem lateral de 0,80 m ao lado da cama.",
                   luz="Duas lanternas + cinco faces de vidro: luz zenital sobre os dois núcleos de uso.",
                   ventilacao="Duas saídas altas (lanternas) e admissão pelas faces de vidro: ventilação cruzada longitudinal.",
                   privacidade="Fundo opaco e faces laterais parcialmente opacas; terraço em três faces protegido pela vela.",
                   vistas="Vista frontal e lateral do estar; vista do céu pela lanterna da cama.",
                   acessos="Hóspedes pelo terraço; técnico pelo fundo (ático sobre o banho).",
                   manutencao="Membrana em gomos com cumeeira; duas lanternas com vidro removível; terraço independente.",
                   operacao="Governança em 30 min; a sequência linear facilita o fluxo da camareira.")),
    dict(code="capsule", tag="ZK", name="ZION CÁPSULA", fam="Cápsula monocoque transportável", cat="PREMIUM", area=CAP.floor_area(), ext=CAP.deck_area(), guests="2", bed="1 queen",
         hero="capsule/desenhos/08_isometrica.svg", imgs=[], plan="capsule/desenhos/01_conceito.svg", iso="capsule/desenhos/08_isometrica.svg",
         concept="Uma casca de alumínio composto sobre doze anéis de aço, com a calota frontal inteira em vidro curvo (Visor), uma faixa de vidro que contorna a seção sobre a cama (Anel de Luz) e dois Olhos laterais. Fabricada e mobiliada em fábrica, viaja inteira em carreta e pousa em quatro pés telescópicos sobre estacas: instalação em um dia.",
         partido="Produto pronto: a cabana como objeto industrial acabado, que chega e pousa. A seção em superelipse dá largura útil ao piso (2,75 m) sem perder a leitura de cápsula.",
         sig=["Visor: calota frontal em 5 gomos de vidro curvo com porta pivotante", "Anel de Luz: faixa de vidro de 0,45 m em 130° sobre a cama", "Dois Olhos Ø0,60 (suíte e banho), família das Janelas Olho do Casulo", "Compartimento técnico na calota traseira com acesso externo"],
         func=dict(implantacao="Visor para a vista, cauda técnica para o caminho de serviço; pousa em terrenos com até 15 % de declividade só ajustando os pés.",
                   circulacao="Deck → porta pivotante no Visor → estar → suíte → banho; compartimento técnico isolado do hóspede.",
                   luz="Visor (11,5 m² de vidro), Anel de Luz sobre a cama e dois Olhos.",
                   ventilacao="Anel de Luz com abertura basculante como saída alta; admissão pelos Olhos com grelhas; split dutado do técnico.",
                   privacidade="Casca opaca nas laterais; Olhos altos; o Visor recebe cortina em trilho curvo.",
                   vistas="Panorâmica frontal do Visor a partir da chaise e da cama (pés para a vista); céu pelo Anel de Luz.",
                   acessos="Hóspedes pelo deck; técnico pela cauda, sem entrar na unidade.",
                   manutencao="Casca lavável; sem membrana; vidros curvos com selante; técnico concentrado em um compartimento.",
                   operacao="Governança em 20 min; unidade removível e realocável; a operação pode redistribuir cápsulas entre destinos.")),
]

def cover():
    page(f'''<div class="photo full">{img("cocoon/renders/web/cocoon_night.jpg")}</div><div class="overlay"></div>
<div class="cover">{zion_mark_html("56px", color="#FEF5F0", style="display:block;margin:0 auto 22px")}{zion_logo_html("46px", color="#FEF5F0", style="display:block;margin:0 auto 26px")}<div class="eyebrow">ZION GLAMPING COLLECTION</div>
<div class="split"><span>CONCEITO</span><i></i><span>VISUAL</span></div>
<div class="sub">DOCUMENTO CONCEITUAL E VISUAL DA LINHA · {DOC}</div>
<div class="tag">Fase 02 do Cabin Design &amp; Engineering System · seis unidades proprietárias de hospedagem em natureza: Casulo, Safari, Lodge 38, Lodge 24, Lodge 28 e Cápsula · conceito, partido, linguagem, materialidade, experiência do hóspede, implantação e operação · {REV} · {DATE}</div></div>''', "dark coverpage", "CAPA")

def manifesto():
    page(f'''<h2>MANIFESTO <small>por que a Zion desenha as próprias cabanas</small></h2>
<div class="two"><div><p class="lede big">Desenvolvemos destinos. Uma hospedagem em natureza não é uma casa pequena nem uma barraca grande: é um produto hoteleiro que precisa performar, permanecer e ser replicado. Por isso a Zion Glamping Collection é uma linha, não um catálogo: seis formas sobre uma só plataforma construtiva, desenhadas para serem fabricadas, transportadas, montadas e operadas com o mesmo padrão em qualquer terreno.</p>
<p class="lede">Cada unidade tem uma assinatura própria de luz e de forma. Nenhuma replica um modelo de mercado: a referência de catálogo serve de faixa de área, o desenho é nosso.</p></div>
<div><ol class="next">
<li><b>01 · Território antes da forma</b><p>A cabana nasce da relação com o chão, o vento, a vista e o caminho. Toda unidade tem frente, costas e um lado técnico.</p></li>
<li><b>02 · Luz como assinatura</b><p>Espinha de Luz, Óculo do Zênite, Lanterna Zion, Visor e Anel de Luz: cada modelo abre o céu de um jeito diferente sobre a cama.</p></li>
<li><b>03 · Uma plataforma, seis formas</b><p>Zion Shell System: aço galvanizado parafusado, membrana PVDF isolada, vidro insulado, deck em estacas. Mesmo kit, mesma fábrica, mesma equipe de montagem.</p></li>
<li><b>04 · Sem obra úmida, sem cicatriz</b><p>Estacas helicoidais e kit parafusado: a cabana pousa e pode ser removida sem deixar concreto no sítio.</p></li>
<li><b>05 · Operação desenhada</b><p>Governança em menos de 40 minutos, acesso técnico sem entrar na unidade, manutenção por gomo e por peça.</p></li></ol></div></div>
<div class="strip"><div>{img("cocoon/renders/web/cocoon_ext_side.jpg")}</div><div>{img("zenith/renders/web/zenith_ext_side.jpg")}</div><div>{img("lodge/renders/web/lodge_ext_side.jpg")}</div><div>{sheet("capsule/desenhos/08_isometrica.svg")}</div></div>''', "dark", "MANIFESTO")

def partido():
    rows = "".join(f'<tr><td><b>{esc(u["name"])}</b><br><small>{esc(u["fam"])}</small></td><td>{esc(u["partido"])}</td><td>{"<br>".join(esc(s) for s in u["sig"][:2])}</td><td class="num">{fmt(u["area"])} + {fmt(u["ext"])}</td><td>{esc(u["cat"])}<br><small>proposta</small></td></tr>' for u in UNITS)
    page(f'''<h2>PARTIDO ARQUITETÔNICO <small>quatro famílias de forma sobre uma plataforma</small></h2>
<div class="fam4"><div><b>CONCHA</b><span>Casulo</span><p>Arcos elípticos e membrana contínua: a forma envolve.</p></div><div><b>TENDA</b><span>Safari</span><p>Mastros, coroas e catenárias: a cobertura paira.</p></div><div><b>PAVILHÃO</b><span>Lodge 38 · 24 · 28</span><p>Octógono, caibros e lanterna: a planta centra.</p></div><div><b>CÁPSULA</b><span>Cápsula</span><p>Monocoque e Visor: o objeto pousa.</p></div></div>
<table class="dark"><tr><th>Unidade</th><th>Partido</th><th>Assinaturas</th><th class="num">m² int. + ext.</th><th>Categoria</th></tr>{rows}</table>
<p class="note">Categorias propostas (Standard, Premium, Signature, Ultra Luxury) a confirmar no brief ZG-BRF-001. Nomes das assinaturas são marcas de produto da linha.</p>
<div class="strip six">{"".join(f"<div>{img(u['hero']) if u['hero'].endswith('.jpg') else sheet(u['iso'])}</div>" for u in UNITS)}</div>''', "dark", "PARTIDO")

def _swatch(col, label, sub, tex=""):
    return f'<div class="sw"><div class="chip" style="background:{col}">{tex}</div><b>{esc(label)}</b><span>{esc(sub)}</span></div>'

def linguagem():
    wood = '<svg viewBox="0 0 100 60" preserveAspectRatio="none" width="100%" height="100%"><rect width="100" height="60" fill="#B99A73"/><path d="M0 12H100M0 27H100M0 41H100M0 54H100" stroke="#8B714E" stroke-width=".8" opacity=".7"/></svg>'
    oak = '<svg viewBox="0 0 100 60" preserveAspectRatio="none" width="100%" height="100%"><rect width="100" height="60" fill="#D9C4A3"/><path d="M0 20 Q50 14 100 22 M0 40 Q50 46 100 38" stroke="#B99A73" stroke-width=".8" fill="none" opacity=".8"/></svg>'
    memb = '<svg viewBox="0 0 100 60" preserveAspectRatio="none" width="100%" height="100%"><rect width="100" height="60" fill="#EDE6D6"/><path d="M0 0 L100 60 M0 30 L50 60 M50 0 L100 30" stroke="#DED6BF" stroke-width=".6"/></svg>'
    glass = '<svg viewBox="0 0 100 60" preserveAspectRatio="none" width="100%" height="100%"><rect width="100" height="60" fill="#8FA4AE"/><path d="M0 60 L60 0" stroke="#BFD0D6" stroke-width="6" opacity=".6"/></svg>'
    steel = '<svg viewBox="0 0 100 60" preserveAspectRatio="none" width="100%" height="100%"><rect width="100" height="60" fill="#3A3B3A"/><circle cx="20" cy="30" r="9" fill="none" stroke="#6E706E" stroke-width="2"/><circle cx="50" cy="30" r="9" fill="none" stroke="#6E706E" stroke-width="2"/><circle cx="80" cy="30" r="9" fill="none" stroke="#6E706E" stroke-width="2"/></svg>'
    stone = '<svg viewBox="0 0 100 60" preserveAspectRatio="none" width="100%" height="100%"><rect width="100" height="60" fill="#CFC9BE"/><path d="M10 50 Q30 10 55 35 T95 15" stroke="#A9A297" stroke-width="1.2" fill="none"/><path d="M0 25 Q25 40 45 10" stroke="#BDB6AA" stroke-width=".8" fill="none"/></svg>'
    brass = '<svg viewBox="0 0 100 60" preserveAspectRatio="none" width="100%" height="100%"><rect width="100" height="60" fill="#B5945A"/><rect y="28" width="100" height="2" fill="#D7B978" opacity=".8"/></svg>'
    linen = '<svg viewBox="0 0 100 60" preserveAspectRatio="none" width="100%" height="100%"><rect width="100" height="60" fill="#E9E1D2"/><path d="M0 5H100M0 15H100M0 25H100M0 35H100M0 45H100M0 55H100" stroke="#DED6BF" stroke-width=".5"/><path d="M5 0V60M15 0V60M25 0V60M35 0V60M45 0V60M55 0V60M65 0V60M75 0V60M85 0V60M95 0V60" stroke="#DED6BF" stroke-width=".5"/></svg>'
    sw = "".join([_swatch("#EDE6D6", "Membrana PVDF", "1050 g/m² · creme quente · matte", memb), _swatch("#3A3B3A", "Aço galvanizado", "arcos, mastros, caibros · grafite fosco", steel), _swatch("#8FA4AE", "Vidro insulado low-e", "alumínio bronze RPT", glass),
                   _swatch("#B99A73", "Cumaru", "deck 20 x 140 · fixação oculta", wood), _swatch("#D9C4A3", "Carvalho de engenharia", "piso 14 mm · ripado termotratado", oak), _swatch("#CFC9BE", "Pedra", "quartzito em bancadas e mesas", stone),
                   _swatch("#B5945A", "Latão escovado", "metais, arandelas, puxadores", brass), _swatch("#E9E1D2", "Linho e lã", "cortinas, tapetes, estofados", linen)])
    page(f'''<h2>LINGUAGEM E MATERIALIDADE <small>o que se vê, o que se toca</small></h2>
<div class="two"><div><div class="swatches">{sw}</div></div>
<div><dl class="kv stack"><dt>Cor</dt><dd>De fora, a linha é creme e grafite: membrana clara sobre estrutura escura, madeira de deck ao chão. Dentro, carvalho, linho e latão sob luz 2700 K. Nada brilhante, nada branco puro.</dd>
<dt>Forma</dt><dd>Curvas contínuas (Casulo, Safari, Cápsula) ou polígono regular (Lodge). Sem beirais quebrados, sem rufos aparentes, sem calhas à vista.</dd>
<dt>Detalhe</dt><dd>Estrutura aparente e honesta por dentro: arcos, mastros e caibros revestidos ou pintados, nunca escondidos. Junções parafusadas visíveis, tratadas como desenho.</dd>
<dt>Interior</dt><dd>FF&amp;E Zion New Luxury: materiais naturais, sem plástico aparente, sem pendentes (a luz vem de fitas embutidas, arandelas e abajures). 56 itens de catálogo, listas por unidade.</dd>
<dt>Marca</dt><dd>O símbolo Z aparece uma vez por unidade: gravado na placa da porta, em latão. Sinalização mínima, em papelaria e QR de serviços.</dd></dl></div></div>
<div class="strip"><div>{img("cocoon/renders/web/cocoon_int_bed.jpg")}</div><div>{img("zenith/renders/web/zenith_int_living.jpg")}</div><div>{img("lodge/renders/web/lodge_int_living.jpg")}</div><div>{img("cocoon/renders/web/cocoon_int_bath.jpg")}</div></div>''', "dark", "LINGUAGEM")

def experiencia():
    steps = [("CHEGADA", "A trilha chega ao deck, nunca à porta. O hóspede vê a cabana inteira antes de entrar."), ("DECK", "Espreguiçadeiras, mesa, lanternas de deck: a primeira sala é do lado de fora."),
             ("LIMIAR", "Porta de correr ou pivotante em vidro; fechadura digital; a luz de boas-vindas acende por cena."), ("ESTAR", "Chaise ou sofá voltado para o vidro; mini cozinha (Casulo) ou Ilha do Café / minibar; nenhuma TV por padrão (opcional)."),
             ("SUÍTE", "A cama é o centro: sob a Espinha, o Óculo, a Lanterna ou o Anel de Luz. Pés para a vista, cabeça para o abrigo."), ("BANHO", "Banheira ou chuveiro com a própria janela (Olho, fresta, Olho do banho); bancada em pedra, metais em latão."),
             ("NOITE", "Blackout motorizado, luz 2700 K a 10 %, som ambiente, céu pela clarabóia."), ("MANHÃ", "Luz rasante pelo vidro frontal, café na ilha, deck ao sol; check-out sem recepção.")]
    tl = "".join(f'<div class="step"><b>{i + 1:02d}</b><span>{esc(a)}</span><p>{esc(b)}</p></div>' for i, (a, b) in enumerate(steps))
    page(f'''<h2>EXPERIÊNCIA DO HÓSPEDE <small>a sequência é a mesma em toda a linha; o que muda é a assinatura de luz</small></h2><div class="timeline">{tl}</div>
<div class="three imgs"><div>{img("cocoon/renders/web/cocoon_int_living.jpg")}<span>Casulo · estar e fachada de vidro</span></div><div>{img("zenith/renders/web/zenith_int_bed.jpg")}<span>Safari · cama sob o Óculo do Zênite</span></div><div>{img("lodge/renders/web/lodge_int_bath.jpg")}<span>Lodge 38 · banho sob a fresta alta</span></div></div>''', "dark", "EXPERIÊNCIA")

def unit_pages(u):
    hero = img(u["hero"], "hero") if u["hero"].endswith(".jpg") else sheet(u["hero"], "hero-sheet")
    sig = "".join(f"<li>{esc(s)}</li>" for s in u["sig"])
    thumbs = "".join(f'<div>{img(i)}</div>' for i in u["imgs"][:3]) if u["imgs"] else ""
    page(f'''<div class="ph2"><span class="tag">{esc(u["tag"])}</span><h2>{esc(u["name"])} <small>{esc(u["fam"])} · categoria proposta {esc(u["cat"])}</small></h2></div>
<div class="two wide"><div>{hero}<div class="thumbs3">{thumbs}</div></div>
<div><p class="lede">{esc(u["concept"])}</p><p class="partido">{esc(u["partido"])}</p>
<dl class="kv"><dt>Área interna</dt><dd>{fmt(u["area"])} m²</dd><dt>Área externa</dt><dd>{fmt(u["ext"])} m²</dd><dt>Área total</dt><dd>{fmt(u["area"] + u["ext"])} m²</dd><dt>Hóspedes</dt><dd>{esc(u["guests"])} · {esc(u["bed"])}</dd><dt>FF&amp;E</dt><dd>{ffe.totals(u["code"], 1)["n_items"]} itens Zion New Luxury</dd></dl>
<h4>ASSINATURAS</h4><ul class="sig">{sig}</ul></div></div>''', "dark", u["name"] + " · CONCEITO")
    f = u["func"]
    blocks = [("IMPLANTAÇÃO", f["implantacao"]), ("CIRCULAÇÃO", f["circulacao"]), ("ILUMINAÇÃO NATURAL", f["luz"]), ("VENTILAÇÃO", f["ventilacao"]), ("PRIVACIDADE", f["privacidade"]), ("VISTAS", f["vistas"]), ("ACESSOS", f["acessos"]), ("MANUTENÇÃO", f["manutencao"]), ("OPERAÇÃO HOTELEIRA", f["operacao"])]
    grid = "".join(f'<div><b>{esc(a)}</b><p>{esc(b)}</p></div>' for a, b in blocks)
    page(f'''<h2>{esc(u["name"])} · COMO A CABANA FUNCIONA <small>relação com a natureza, uso e operação</small></h2>
<div class="func"><div class="grid9">{grid}</div><div class="planbox">{sheet(u["plan"])}<span>{"Planta humanizada" if "humanizada" in u["plan"] else "Prancha de conceito"} · sem escala nesta página</span>{sheet(u["iso"]) if u["iso"] != u["hero"] else img(u["imgs"][3]) if len(u["imgs"]) > 3 else ""}</div></div>''', "dark", u["name"] + " · FUNCIONAMENTO")

def implantacao():
    # diagrama esquemático de cluster (SVG próprio)
    units = [(120, 150, "ZC"), (330, 110, "ZS"), (560, 170, "ZL"), (760, 120, "ZL"), (250, 330, "ZL24"), (420, 350, "ZL24"), (590, 340, "ZL24"), (820, 320, "ZL28"), (700, 470, "ZK"), (880, 470, "ZK")]
    def shape(x, y, t):
        if t == "ZC": return f'<ellipse cx="{x}" cy="{y}" rx="34" ry="22" fill="#EDE6D6"/><rect x="{x - 42}" y="{y - 18}" width="16" height="36" fill="#B99A73"/>'
        if t == "ZS": return f'<polygon points="{x - 40},{y + 22} {x + 40},{y + 22} {x + 30},{y - 22} {x - 30},{y - 22}" fill="#EDE6D6"/><rect x="{x - 40}" y="{y + 22}" width="80" height="14" fill="#B99A73"/>'
        if t == "ZK": return f'<rect x="{x - 30}" y="{y - 12}" width="60" height="24" rx="12" fill="#E6E0D4"/><rect x="{x - 48}" y="{y - 12}" width="18" height="24" fill="#B99A73"/>'
        r = 26 if t == "ZL" else (20 if t == "ZL24" else 24)
        pts = " ".join(f"{x + r * __import__('math').cos(__import__('math').pi / 8 + i * __import__('math').pi / 4):.1f},{y + r * __import__('math').sin(__import__('math').pi / 8 + i * __import__('math').pi / 4):.1f}" for i in range(8))
        return f'<polygon points="{pts}" fill="#EDE6D6"/><circle cx="{x}" cy="{y}" r="5" fill="#9FB7C2"/><rect x="{x - r - 16}" y="{y - 14}" width="16" height="28" fill="#B99A73"/>'
    svg = ('<svg viewBox="0 0 1000 560" width="100%"><rect width="1000" height="560" fill="#0F1410"/>'
           + "".join(f'<path d="M0 {80 + i * 70} Q250 {40 + i * 70} 500 {90 + i * 70} T1000 {60 + i * 70}" fill="none" stroke="#2A3326" stroke-width="1"/>' for i in range(8))
           + '<path d="M40 520 C200 470 260 420 330 380 S520 300 640 300 S860 250 960 120" fill="none" stroke="#DED6BF" stroke-width="2" stroke-dasharray="6 5"/>'
           + '<rect x="40" y="440" width="120" height="70" fill="#1B2117" stroke="#DED6BF"/><text x="100" y="480" fill="#DED6BF" font-size="11" text-anchor="middle" letter-spacing="2">RECEPÇÃO · APOIO</text>'
           + '<rect x="40" y="380" width="120" height="44" fill="#1B2117" stroke="#DED6BF" stroke-dasharray="3 3"/><text x="100" y="406" fill="#DED6BF" font-size="10" text-anchor="middle" letter-spacing="2">ESTACIONAMENTO</text>'
           + "".join(shape(x, y, t) + f'<text x="{x}" y="{y + 44}" fill="#DED6BF" font-size="10" text-anchor="middle" letter-spacing="2">{t}</text>' for x, y, t in units)
           + '<text x="960" y="545" fill="#8B714E" font-size="10" text-anchor="end" letter-spacing="2">ESQUEMA · SEM ESCALA · CURVAS DE NÍVEL, TRILHA, VISTA PARA O NORTE</text><text x="500" y="24" fill="#DED6BF" font-size="11" text-anchor="middle" letter-spacing="3">▲ VISTA PRINCIPAL / VALE</text></svg>')
    rows = [("ZION CASULO", "30 x 24 m", "6 a 8", "frente para o vale, cauda para a encosta", "trilha até o deck, serviço pela cauda"), ("ZION SAFARI", "30 x 26 m", "5 a 7", "cume alto a favor do vento", "passarela até o terraço"),
            ("ZION LODGE 38", "26 x 24 m", "8 a 10", "porta para a vista, faces opacas para o caminho", "deck em três faces"), ("ZION LODGE 24", "18 x 16 m", "12 a 16", "fileira com 8 m entre unidades", "deck de uma face"),
            ("ZION LODGE 28", "24 x 20 m", "9 a 11", "eixo longo perpendicular à vista", "terraço em três faces"), ("ZION CÁPSULA", "16 x 14 m", "14 a 18", "Visor para a vista, cauda técnica para o serviço", "deck frontal; realocável")]
    tr = "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td class='num'>{esc(c)}</td><td>{esc(d)}</td><td>{esc(e)}</td></tr>" for a, b, c, d, e in rows)
    page(f'''<h2>IMPLANTAÇÃO E RELAÇÃO COM A NATUREZA <small>princípios de master plan para qualquer sítio</small></h2>
<div class="two wide"><div class="diagram">{svg}</div><div><table class="dark small"><tr><th>Unidade</th><th>Lote-tipo</th><th class="num">un./ha</th><th>Orientação</th><th>Acesso</th></tr>{tr}</table>
<ul class="rules"><li>Nenhuma cabana vê a porta de outra: frentes desencontradas, distância mínima de 12 m entre vidros.</li><li>Trilhas de 1,20 m em saibro ou deck baixo; nada de asfalto depois da recepção.</li><li>Infraestrutura enterrada em uma única vala por trilha (água, esgoto, energia, dados).</li><li>Estacas helicoidais em todas as unidades: sem corte, sem aterro, sem concreto; vegetação mantida até 1,5 m da casca.</li><li>Afastamentos, APP, declividade e sondagem: ⚠️ VALIDAÇÃO OBRIGATÓRIA — ENGENHEIRO/ARQUITETO em cada sítio.</li></ul></div></div>
<div class="strip three-s"><div>{sheet("cocoon/projeto/PA-01_implantacao.svg")}</div><div>{sheet("zenith/projeto/PA-01_implantacao.svg")}</div><div>{sheet("lodge/projeto/PA-01_implantacao.svg")}</div></div>
<p class="note" style="margin-top:6px">Lotes-tipo de 30 x 24 m (PA-01) do Casulo, do Safari e do Lodge 38: acesso, deck, afastamentos e infraestrutura por unidade.</p>''', "dark", "IMPLANTAÇÃO")

def operacao():
    rows = [("Membrana PVDF", "lavagem com água e sabão neutro", "semestral", "inspeção de costuras e keder; retensão", "20 anos"), ("Vidros insulados", "limpeza", "por hospedagem", "selantes e drenagem dos caixilhos", "25 anos"),
            ("Deck de cumaru", "varrição e lavagem", "semanal", "óleo protetor; réguas substituíveis", "15 anos"), ("Estrutura galvanizada", "inspeção visual", "anual", "torque dos parafusos; retoque de pintura", "50 anos"),
            ("Estacas e cabeçotes", "nivelamento", "anual", "verificação de recalque", "50 anos"), ("Climatização", "limpeza de filtros", "mensal", "carga de gás e dutos", "12 anos"),
            ("Hidráulica e boiler", "inspeção de registros", "trimestral", "anodo do boiler; caixa de gordura", "15 anos"), ("FF&E", "governança", "por hospedagem", "estofados e enxoval em 3 jogos", "5 a 8 anos")]
    tr = "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{esc(c)}</td><td>{esc(d)}</td><td class='num'>{esc(e)}</td></tr>" for a, b, c, d, e in rows)
    page(f'''<h2>OPERAÇÃO HOTELEIRA E MANUTENÇÃO <small>a cabana como ativo que precisa performar e permanecer</small></h2>
<div class="two wide"><div><table class="dark small"><tr><th>Sistema</th><th>Rotina</th><th>Frequência</th><th>Manutenção</th><th class="num">Vida útil</th></tr>{tr}</table></div>
<div><dl class="kv stack"><dt>Governança</dt><dd>20 a 40 minutos por unidade; um eixo de circulação, banho na ponta, marcenaria fechada, enxoval em 3 jogos.</dd><dt>Check-in sem recepção</dt><dd>Fechadura digital, cenas de luz, termostato e cofre automatizados; QR de serviços na papelaria.</dd>
<dt>Serviço</dt><dd>Ilha do Café / minibar abastecidos pela camareira; room service pelo deck; lixo e roupa saem pelo acesso técnico.</dd><dt>Acesso técnico</dt><dd>Sempre pela cauda, pelo fundo ou pelo compartimento técnico: nenhum reparo obriga a entrar na unidade ocupada.</dd>
<dt>Replicação</dt><dd>Kit parafusado, estacas removíveis, FF&amp;E padronizado: a unidade pode ser desmontada, transportada e remontada em outro destino.</dd></dl></div></div>
<div class="strip"><div>{img("cocoon/renders/web/cocoon_ext_aerial.jpg")}</div><div>{img("zenith/renders/web/zenith_ext_aerial.jpg")}</div><div>{img("lodge/renders/web/lodge_ext_aerial.jpg")}</div><div>{img("lodge/renders/web/lodge_ext_rear.jpg")}</div></div>''', "dark", "OPERAÇÃO")

def categorias():
    rows = [("STANDARD", "Lodge 24", "FF&E essencial, split de parede, sem banheira, deck de uma face", "alto giro, adensamento"), ("PREMIUM", "Lodge 38 · Lodge 28 · Cápsula", "FF&E completo, climatização dutada, vela ou Visor, lanternas", "casais e curta estadia premium"),
            ("SIGNATURE", "Casulo · Safari", "assinaturas de luz, banheira, hidromassagem (Safari), hot tub opcional, automação de cenas", "flagship do destino"), ("ULTRA LUXURY", "Casulo ou Safari em configuração especial", "sauna, piscina privativa, fire pit, cozinha com cocção (a definir no brief)", "villas de destino")]
    tr = "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{esc(c)}</td><td>{esc(d)}</td></tr>" for a, b, c, d in rows)
    page(f'''<h2>CATEGORIAS E POSICIONAMENTO <small>proposta a confirmar no brief</small></h2><table class="dark"><tr><th>Categoria</th><th>Unidades</th><th>O que muda</th><th>Uso</th></tr>{tr}</table>
<h4 style="margin-top:26px">PRÓXIMOS PASSOS</h4><ol class="next two-col"><li><b>Fase 02 fechada com este documento</b><p>Respostas do brief ZG-BRF-001 confirmam categorias, opcionais e sítio.</p></li><li><b>Fase 03 · Arquitetura</b><p>Pontos hidráulicos e elétricos nas plantas, cortes de camadas cotados, fachadas das unidades em conceito.</p></li><li><b>Fases 04 a 08</b><p>Documento técnico ZG-TEC-001: sistema construtivo, camadas, instalações, materiais, BOM, quantitativo e orçamento em 18 grupos.</p></li><li><b>Fases 09 a 12</b><p>Manual em 15 etapas, RFQ para fábricas, revisão e pacote final em 23 pastas.</p></li></ol>
<div class="strip"><div>{img("cocoon/renders/web/cocoon_night.jpg")}</div><div>{img("zenith/renders/web/zenith_night.jpg")}</div><div>{img("lodge/renders/web/lodge_night.jpg")}</div><div>{img("cocoon/renders/web/cocoon_ext_rear.jpg")}</div></div>
<table class="dark small rev"><tr><th>Rev</th><th>Data</th><th>Descrição</th><th>Autor</th></tr><tr><td>00</td><td>{DATE}</td><td>Conceito · emissão inicial do documento conceitual e visual da linha</td><td>Zion Cabin Design System</td></tr></table>''', "dark", "CATEGORIAS · PRÓXIMOS PASSOS")

CSS = """
@font-face{font-family:'Aventa';src:url(../assets/aventa.woff2) format('woff2');font-weight:100 900;font-display:swap}
:root{--black:#040605;--cream:#FEF5F0;--sand:#DED6BF;--earth:#8B714E;--green:#1B2117}
*{box-sizing:border-box} body{margin:0;background:#111;font-family:'Aventa','DM Sans',Helvetica,Arial,sans-serif;color:var(--cream);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{position:relative;width:297mm;height:210mm;margin:0 auto 8mm;background:var(--black);overflow:hidden;padding:14mm 16mm 16mm;page-break-after:always;break-after:page}
.page.coverpage{padding:0} .photo.full{position:absolute;inset:0} .photo.full img{width:100%;height:100%;object-fit:cover;display:block} .overlay{position:absolute;inset:0;background:rgba(4,6,5,.66)}
.cover{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:0 30mm}
.eyebrow{font-size:9px;letter-spacing:.42em;color:var(--sand);margin-bottom:34px}
.split{display:flex;align-items:center;justify-content:space-between;width:100%;font-weight:200;font-size:46px;letter-spacing:.26em;line-height:1;white-space:nowrap} .split i{flex:1;height:1px;background:var(--cream);margin:0 36px;opacity:.85}
.cover .sub{margin-top:30px;font-size:14px;letter-spacing:.34em;font-weight:300;color:var(--sand)} .cover .tag{margin-top:60px;font-size:10px;letter-spacing:.14em;color:var(--sand);max-width:190mm;line-height:1.9;font-weight:300}
h2{margin:0 0 10px;font-weight:200;font-size:22px;letter-spacing:.32em;text-transform:uppercase;line-height:1.1} h2 small{display:block;font-size:9.5px;letter-spacing:.16em;color:var(--sand);margin-top:6px;font-weight:300;text-transform:none}
h4{margin:14px 0 6px;font-weight:400;font-size:9.5px;letter-spacing:.3em;color:var(--sand)}
.lede{margin:0 0 12px;font-size:12.5px;line-height:1.85;font-weight:300} .lede.big{font-size:15px} .partido{font-size:10.5px;line-height:1.7;color:var(--sand);font-weight:300;margin:0 0 12px;border-left:1px solid var(--earth);padding-left:12px}
.foot{position:absolute;left:16mm;right:16mm;bottom:7mm;display:flex;justify-content:space-between;font-size:7.5px;letter-spacing:.24em;color:var(--sand);font-weight:300} .foot span:nth-child(2){flex:1;text-align:center}
.two{display:grid;grid-template-columns:1fr 1fr;gap:28px} .two.wide{grid-template-columns:1.25fr 1fr}
ol.next{list-style:none;margin:0;padding:0} ol.next li{padding:8px 0;border-bottom:1px solid rgba(222,214,191,.16);font-size:11px;line-height:1.6;color:var(--sand);font-weight:300} ol.next li b{display:block;color:var(--cream);font-weight:500;font-size:12.5px;letter-spacing:.04em} ol.next li p{margin:2px 0 0}
ol.next.two-col{columns:2;column-gap:28px} ol.next.two-col li{break-inside:avoid}
table.dark{border-collapse:collapse;width:100%;font-size:10.5px;font-weight:300} table.dark th{text-align:left;font-weight:300;font-size:8px;letter-spacing:.2em;color:var(--sand);text-transform:uppercase;padding:0 6px 6px;border-bottom:1px solid var(--sand)} table.dark td{padding:5px 6px;border-bottom:1px solid rgba(222,214,191,.16);vertical-align:top;line-height:1.45} table.dark small{color:var(--sand)} .num{text-align:right;white-space:nowrap} table.dark.small{font-size:9.6px} table.dark.small td{padding:4px 6px} table.rev{margin-top:18px;width:70%}
.note{font-size:9px;line-height:1.6;color:var(--sand);font-weight:300;margin-top:12px}
.fam4{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:6px 0 12px} .fam4 div{border-top:1px solid var(--sand);padding-top:8px} .fam4 b{display:block;font-size:14px;letter-spacing:.3em;font-weight:300} .fam4 span{display:block;font-size:8.5px;letter-spacing:.2em;color:var(--earth);margin:2px 0 6px} .fam4 p{margin:0;font-size:9.5px;color:var(--sand);line-height:1.5;font-weight:300}
.swatches{display:grid;grid-template-columns:repeat(4,1fr);gap:14px} .sw .chip{height:64px;overflow:hidden;line-height:0} .sw b{display:block;font-size:10.5px;font-weight:500;margin-top:6px;letter-spacing:.04em} .sw span{display:block;font-size:8.8px;color:var(--sand);line-height:1.4}
.kv{display:grid;grid-template-columns:90px 1fr;gap:6px 14px;margin:0;font-size:11.5px;line-height:1.55;font-weight:300} .kv.stack{grid-template-columns:1fr;gap:1px 0} .kv.stack dt{margin-top:9px} .kv dt{color:var(--sand);letter-spacing:.2em;font-size:8px;text-transform:uppercase;padding-top:3px} .kv dd{margin:0}
.timeline{display:grid;grid-template-columns:repeat(8,1fr);gap:10px;margin:6px 0 16px} .step{border-top:1px solid var(--sand);padding-top:8px} .step b{display:block;font-size:9px;color:var(--earth);letter-spacing:.2em} .step span{display:block;font-size:10.5px;letter-spacing:.24em;font-weight:300;margin:2px 0 6px} .step p{margin:0;font-size:9.6px;line-height:1.55;color:var(--sand);font-weight:300}
.three.imgs{display:grid;grid-template-columns:repeat(3,1fr);gap:14px} .three.imgs div{height:78mm;position:relative;overflow:hidden} .three.imgs img{width:100%;height:100%;object-fit:cover;display:block} .three.imgs span{position:absolute;left:0;right:0;bottom:0;padding:6px 10px;background:rgba(4,6,5,.7);font-size:8px;letter-spacing:.16em;color:var(--sand)}
.ph2{display:flex;align-items:baseline;gap:14px} .ph2 .tag{font-size:10px;letter-spacing:.3em;color:var(--earth);border:1px solid var(--earth);padding:3px 8px}
img.hero{width:100%;height:96mm;object-fit:cover;display:block} .hero-sheet{height:96mm;overflow:hidden} .thumbs3{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:8px} .thumbs3 div{height:34mm;overflow:hidden} .thumbs3 img{width:100%;height:100%;object-fit:cover;display:block}
ul.sig{margin:0;padding:0 0 0 14px;font-size:10px;line-height:1.6;color:var(--sand);font-weight:300} ul.sig li{margin-bottom:3px}
.func{display:grid;grid-template-columns:1.15fr 1fr;gap:24px} .grid9{display:grid;grid-template-columns:repeat(3,1fr);gap:10px 14px} .grid9 div{border-top:1px solid rgba(222,214,191,.4);padding-top:6px} .grid9 b{display:block;font-size:8.5px;letter-spacing:.24em;color:var(--earth);font-weight:400;margin-bottom:3px} .grid9 p{margin:0;font-size:10.4px;line-height:1.6;color:var(--cream);font-weight:300}
.planbox{position:relative} .planbox span{display:block;font-size:8px;letter-spacing:.16em;color:var(--sand);margin:6px 0 10px} .planbox img{width:100%;height:60mm;object-fit:cover;display:block}
.sheet{background:#FEF5F0;border:1px solid rgba(222,214,191,.35);line-height:0} .sheet svg{width:100%;height:auto;display:block} .sheet.missing{padding:20px;color:#1B2117;font-size:10px;line-height:1.4}
.diagram svg{width:100%;height:auto;display:block;border:1px solid rgba(222,214,191,.25)} ul.rules{margin:12px 0 0;padding-left:14px;font-size:10.4px;line-height:1.65;color:var(--sand);font-weight:300}
.strip{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:16px} .strip.six{grid-template-columns:repeat(6,1fr)} .strip.three-s{grid-template-columns:repeat(3,1fr)} .strip.three-s div{height:42mm;background:#FEF5F0} .strip div{height:46mm;overflow:hidden;background:#1B2117} .strip.six div{height:18mm} .strip img{width:100%;height:100%;object-fit:cover;display:block} .strip .sheet{height:100%} .strip .sheet svg{height:100%;width:auto;margin:0 auto} ul.rules li{margin-bottom:4px}
.ph{background:#1B2117;height:100%;min-height:40mm}
@media print{@page{size:A4 landscape;margin:0} body{background:var(--black)} .page{margin:0}}
"""

def build():
    cover(); manifesto(); partido(); linguagem(); experiencia()
    for u in UNITS: unit_pages(u)
    implantacao(); operacao(); categorias()
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · {DOC} · Documento Conceitual e Visual</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    open(OUT, "w", encoding="utf-8").write(doc); print(OUT, len(pages), "páginas", round(os.path.getsize(OUT) / 1e6, 1), "MB")

if __name__ == "__main__":
    build()

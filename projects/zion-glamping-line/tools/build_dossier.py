# -*- coding: utf-8 -*-
"""Gera o Caderno Técnico (HTML) com os 27 entregáveis dos produtos ZION COCOON e ZION ZENITH.
Uso: python3 build_dossier.py [--inline]   (--inline embute imagens como data URI para publicação em página única)"""
import os, sys, base64, json, glob
from geometry import Cocoon, Zenith
from bom import cocoon_bom, zenith_bom, cocoon_parts, zenith_parts, transport, ASSEMBLY

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INLINE = "--inline" in sys.argv
WEB = "--web" in sys.argv or INLINE   # usa renders/web/*.jpg (menores) para PDF e versão autônoma
C, Z = Cocoon(), Zenith()
BC, BZ = cocoon_bom(), zenith_bom()
TC, TZ = transport(BC, "cocoon"), transport(BZ, "zenith")

def fmt(v, n=2):
    s = f"{v:,.{n}f}" if n else f"{int(round(v)):,}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

def src(rel):
    """caminho relativo ou data URI"""
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return None
    if WEB and "/renders/" in rel and rel.endswith(".png"):
        alt = rel.replace("/renders/", "/renders/web/").replace(".png", ".jpg")
        if os.path.exists(os.path.join(ROOT, alt)): rel = alt; path = os.path.join(ROOT, rel)
    if not INLINE:
        return rel
    ext = rel.rsplit(".", 1)[-1].lower()
    mime = {"svg": "image/svg+xml", "png": "image/png", "jpg": "image/jpeg", "woff2": "font/woff2"}[ext]
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

def fig(rel, caption, wide=True):
    s = src(rel)
    if not s:
        return f'<div class="missing">[{rel} ainda não gerado]</div>'
    return f'<figure class="{"wide" if wide else ""}"><img src="{s}" alt="{caption}" loading="lazy"><figcaption>{caption}</figcaption></figure>'

def table(headers, rows, cls="", foot=None):
    h = "".join(f"<th>{x}</th>" for x in headers)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    f = f"<tfoot><tr>{''.join(f'<td>{c}</td>' for c in foot)}</tr></tfoot>" if foot else ""
    return f'<div class="tw"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody>{f}</table></div>'

def kv(rows):
    return '<div class="tw"><table class="kv">' + "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows) + "</table></div>"

def two(a, b):
    return f'<div class="two"><div>{a}</div><div>{b}</div></div>'

def render_pair(name, key, cap):
    return fig(f"{name}/renders/{name}_{key}.png", cap)

# ----------------------------------------------------------------------------- conteúdo
S = []  # (id, número, título, html)

def section(num, title, html, product=""):
    S.append((f"s{len(S) + 1:02d}", num, title, html, product))

# 00 capa e manifesto ---------------------------------------------------------
cover = f"""
<div class="cover">
  <div class="brand"><span class="z">ZION</span><span class="sub">GLAMPING COLLECTION</span></div>
  <div class="splitword"><span>COCOON</span><span class="line"></span><span>ZENITH</span></div>
  <h1>Uma nova linha de hospedagens de luxo em membrana tensionada, aço e vidro</h1>
  <p class="lead">Projeto conceitual, arquitetônico e técnico de dois produtos proprietários da Zion para glampings, boutique hotels e destinos de natureza. Do casulo orgânico ao pico escultural: duas formas, uma plataforma industrial, um mesmo modo de habitar a paisagem.</p>
  <div class="meta"><span>CADERNO TÉCNICO · 27 ENTREGÁVEIS</span><span>ZION HOTEL GROUP INTERNATIONAL · SET 2026</span></div>
</div>
"""
section("00", "Capa e manifesto", cover)

# 01 conceito -----------------------------------------------------------------
concept = f"""
<p class="lead">A Zion cria experiências que conectam ser humano, natureza, conforto, wellness e arquitetura. Esta linha traduz o posicionamento <em>Luxury Nature Hospitality</em> em duas unidades de hospedagem fabricáveis em escala, transportáveis em contêiner, montáveis em terrenos naturais sem movimentação de terra e operáveis com o padrão de um boutique hotel.</p>

<h3>Plataforma comum: ZION SHELL SYSTEM</h3>
<p>Os dois produtos compartilham a mesma base industrial: estacas helicoidais e deck elevado em vigas galvanizadas, estrutura primária em tubos de aço carbono galvanizados a fogo, membrana arquitetônica PVDF tensionada por perfis keder ou anéis, câmara ventilada, isolamento em lã de PET reciclada com manta refletiva, forro tensionado acústico, vidros duplos low-e em esquadrias de alumínio com ruptura térmica e um ático técnico sobre o banho que concentra climatização, aquecimento de água e quadro elétrico. Isso significa um único catálogo de componentes, uma única equipe de montagem e estoque compartilhado entre destinos.</p>

<div class="grid3">
  <div class="card"><h4>Estrutura</h4><p>Pórticos elípticos (Cocoon) e mastros com coroa (Zenith), ambos com ligações parafusadas, segmentos de até 5,2 m e peso unitário abaixo de 80 kg por peça: montagem com guincho manual e talha, sem grua.</p></div>
  <div class="card"><h4>Envelope</h4><p>Quatro camadas: membrana PVDF 1050 g/m², câmara ventilada de 60 mm, lã PET 50 mm com refletiva e forro tensionado. U ≈ 0,6 W/m²K, NRC ≈ 0,6. Funciona na serra, no calor tropical e no litoral.</p></div>
  <div class="card"><h4>Fundação</h4><p>Estacas helicoidais Ø76 com hélice Ø300 e cabeçotes ajustáveis: absorvem terreno inclinado até 8% sem corte, são removíveis e deixam o solo intacto.</p></div>
</div>

<h3>ZION COCOON: a concha que se abre para a paisagem</h3>
<p>Uma cabana biomórfica em forma de casulo: planta em superelipse assimétrica (frente cheia, cauda afilada), seção elíptica com o centro a 0,75 m do piso, de modo que a concha abraça o chão em vez de simplesmente pousar sobre ele. Três gestos definem a identidade e a distinguem de qualquer produto de mercado:</p>
<ul>
  <li><strong>Lábio frontal.</strong> O anel de fachada inclina-se 8° para fora e avança 0,60 m sobre o deck, formando o beiral e a expressão de casulo que se abre. A fachada de vidro fica recuada 0,45 m, inclinada no mesmo ângulo, como a proa de um barco.</li>
  <li><strong>Espinha de Luz.</strong> Uma claraboia contínua de 0,70 x 4,70 m ao longo da cumeeira, sobre o estar e a cama. Deitado, o hóspede vê a copa das árvores e o céu.</li>
  <li><strong>Janelas Olho.</strong> Seis janelas em lente, com requadros profundos de madeira laminada: nenhuma escotilha circular. A lente é a assinatura gráfica do produto e aparece também na comunicação da marca.</li>
</ul>
<p>Sensação buscada: proteção, silêncio, imersão. O interior segue o conceito <em>Zion New Luxury</em>: carvalho no piso, forro tensionado cor areia, marcenaria embutida na curva, iluminação indireta nos rodapés e nos requadros, e a banheira na cauda, o ponto mais íntimo do casulo.</p>

<h3>ZION ZENITH: o ponto mais alto</h3>
<p>Uma cabana escultural de dois cumes de alturas diferentes (5,80 m e 4,60 m), deslocados em diagonal sobre um corpo de vidro e madeira. A silhueta nunca é simétrica: muda a cada ângulo, como uma cordilheira. A membrana desce dos cumes ao anel de beiral e continua em balanço de 2,40 m sobre o terraço, com bordas em catenária entre postes inclinados.</p>
<ul>
  <li><strong>Óculo do Zênite.</strong> No cume principal, um anel de aço de 1,20 m sustentado por uma coroa de três braços libera o centro para uma cúpula de vidro. A cama fica exatamente sob ele: o zênite, literalmente, sobre o hóspede.</li>
  <li><strong>Respiro.</strong> O cume secundário é uma chaminé de ventilação natural com veneziana motorizada, que extrai o ar quente da câmara e transforma a forma em desempenho.</li>
  <li><strong>Mastros integrados.</strong> O mastro principal vive dentro da parede da cabeceira; o secundário vira o totem de madeira da Ilha do Café. Nenhuma coluna solta no meio do quarto.</li>
</ul>

<h3>Originalidade e propriedade</h3>
<p>Os modelos de referência do mercado (túnel segmentado com escotilhas circulares; cobertura de dois picos simétricos sobre planta octogonal) serviram apenas como parâmetro construtivo e dimensional. As geometrias aqui desenvolvidas (superelipse assimétrica com lábio inclinado e espinha envidraçada; cumes assimétricos em diagonal com óculo e chaminé) são proprietárias, definidas por parâmetros numéricos no arquivo <code>tools/geometry.py</code> e passíveis de registro de desenho industrial.</p>

{two(kv([("Produto", "ZION COCOON"), ("Piso", "9,60 x 5,86 m"), ("Concha", "9,75 x 6,00 x 4,20 m"), ("Piso interno", f"{fmt(C.floor_area(), 1)} m² + vestíbulo 2,4 m² = 48 m²"), ("Deck", "29,9 m²"), ("Total", "78 m²"), ("Programa", "Estar, suíte king, banho com banheira"), ("Peso embarcado", f"{fmt(BC['total'], 0)} kg")]),
     kv([("Produto", "ZION ZENITH"), ("Corpo", "9,50 x 5,40 x 2,75 m"), ("Cumes", "5,80 m e 4,60 m"), ("Cobertura", "12,90 x 7,40 m (95,5 m² proj.)"), ("Piso interno", f"{fmt(Z.floor_area(), 1)} m²"), ("Terraço + passarela", "28,0 m²"), ("Total", "79,3 m²"), ("Peso embarcado", f"{fmt(BZ['total'], 0)} kg")]))}
"""
section("01", "Conceito arquitetônico", concept)

# 02-08 desenhos por produto -----------------------------------------------------
DRAW = [("02", "Planta baixa humanizada", "02_planta_humanizada.svg"), ("03", "Planta técnica com dimensões", "03_planta_tecnica.svg"),
        ("04", "Elevação frontal", "04_elevacao_frontal.svg"), ("05", "Elevação lateral", "05_elevacao_lateral.svg"),
        ("06", "Corte longitudinal", "06_corte_longitudinal.svg"), ("07", "Corte transversal", "07_corte_transversal.svg"),
        ("08", "Vista isométrica", "08_isometrica.svg")]
NOTES = {
 "cocoon": {
  "02": "Sequência de intimidade crescente: vestíbulo coberto sob o lábio, estar com chaise voltada ao deck, suíte king com cabeceira na parede do banho e banho na cauda com banheira sob a Janela Olho baixa. Toda a marcenaria (console café, armário baixo, criados) é embutida na curva da concha, onde o pé-direito é menor.",
  "03": "Arcos A0 a A7 a cada 1,20 m (1,10 m na cauda). Malha de estacas 1,20 x 1,30 m (46 estacas). Larguras internas de 5,86 m na seção máxima e 4,80 m no banho. Cortes A-A (longitudinal, no eixo) e B-B (transversal, x = 5,00).",
  "04": "A silhueta é a seção máxima (6,00 x 4,20 m); dentro dela, o anel do lábio (4,88 m) e a fachada de vidro com quatro montantes, travessa a 2,40 m e porta pivotante de 1,00 m. A Espinha de Luz aparece como aresta de vidro na cumeeira.",
  "05": "A concha lê-se como semente: frente cheia e inclinada, cauda que fecha em ponta a 1,10 m. Três Janelas Olho por lado, com o Olho do banho mais alto por privacidade. A condensadora fica atrás da cauda, oculta por painel ripado.",
  "06": "Envelope em quatro camadas; parede do banho sobe até a concha e cria o ático técnico sobre o forro de 2,40 m (evaporadora dutada, aquecedor, quadro). Espinha de Luz de x 1,90 a 6,60 sobre o estar e a cama.",
  "07": "Seção elíptica com centro a 0,75 m: a concha curva-se para dentro na base. Arco Ø88,9 na camada ventilada, Janela Olho basculante em corte, armário embutido onde o pé-direito é de 1,50 m, difusor linear na cabeceira, fita LED nos rodapés.",
  "08": "Volumetria a partir da frente e da lateral direita: lábio, fachada, Espinha de Luz, três Janelas Olho e deck com escada."},
 "zenith": {
  "02": "Estar com sofá voltado à fachada e chaise no vidro lateral; Ilha do Café envolvendo o mastro secundário; suíte king sob o Óculo; closet de 2,00 m; banho de 15 m² com bancada dupla, chuveiro, bacia em nicho e banheira com fresta de vidro; terraço com hidromassagem sob o beiral e passarela lateral de chegada.",
  "03": "Corpo 9,50 x 5,40 com pilares a cada 3,20 m; cobertura 12,90 x 7,40 com curvas de nível da membrana a cada 0,40 m; cumes em (6,30; +0,40) e (1,60; +1,60); 30 estacas sob o piso e 7 de tração para os postes. Cortes A-A (y = +0,40, eixo do mastro) e B-B (x = 6,30).",
  "04": "Dois cumes de alturas diferentes; a membrana em balanço protege a fachada de vidro de 5,40 x 2,75 m e a hidromassagem. Postes externos inclinados 8° com estais.",
  "05": "Vidro contínuo de 6,40 m na suíte e painéis ripados no banho; o cume principal sobre a parede da cabeceira, o secundário sobre a Ilha do Café; balanço de 2,40 m sobre o terraço.",
  "06": "Mastro M1 embutido na parede da cabeceira, coroa de três braços, anel e cúpula do Óculo; forro isolado seguindo os cumes; ático técnico sobre o banho; mastro M2 e chaminé do Respiro atrás do plano.",
  "07": "Corte no eixo do mastro principal: coroa, anel Ø1,20 e óculo; membrana, câmara e forro; anel de beiral sobre pilares; painéis SIP; passagem de 1,10 m ao banho; poste externo estaiado.",
  "08": "Volumetria a partir da frente e da lateral direita: cumes, balanços em catenária, fachada de vidro, terraço e hidromassagem."}}
for num, title, fn in DRAW:
    html = two(fig(f"cocoon/desenhos/{fn}", f"ZION COCOON · {title}") + f"<p class='note'>{NOTES['cocoon'][num]}</p>",
               fig(f"zenith/desenhos/{fn}", f"ZION ZENITH · {title}") + f"<p class='note'>{NOTES['zenith'][num]}</p>")
    section(num, title, html)

# 09 modelo 3D ----------------------------------------------------------------
m3d = f"""
<p>Os modelos 3D são gerados a partir da mesma geometria paramétrica dos desenhos (<code>tools/geometry.py</code>) e entregues em dois formatos: visualizador interativo em HTML (Three.js, roda em qualquer navegador, com modos Exterior, Interior, Estrutura, Noite e Corte) e arquivo GLB (glTF binário) para importação em Rhino, SketchUp, Blender, Twinmotion, Lumion, Unreal ou visualização em realidade aumentada no celular.</p>
{table(["Produto", "Visualizador interativo", "Modelo GLB", "Conteúdo"], [
 ["ZION COCOON", '<a href="cocoon/3d/zion-cocoon-3d.html">cocoon/3d/zion-cocoon-3d.html</a>', '<a href="cocoon/3d/zion-cocoon.glb">cocoon/3d/zion-cocoon.glb</a>', "Concha (membrana e vidros), 8 arcos, 7 terças, anel do lábio, fachada, Janelas Olho, deck, piso, parede do banho, mobiliário e equipamentos"],
 ["ZION ZENITH", '<a href="zenith/3d/zion-zenith-3d.html">zenith/3d/zion-zenith-3d.html</a>', '<a href="zenith/3d/zion-zenith.glb">zenith/3d/zion-zenith.glb</a>', "Membrana de dois cumes, forro, mastros e coroas, anel de beiral, pilares, postes e cabos, paredes de vidro e ripado, terraço, hidromassagem, mobiliário"]])}
{two(fig("cocoon/renders/cocoon_structure.png", "ZION COCOON · modelo 3D em modo Estrutura (membrana translúcida)"), fig("zenith/renders/zenith_structure.png", "ZION ZENITH · modelo 3D em modo Estrutura"))}
{two(fig("cocoon/renders/cocoon_section.png", "ZION COCOON · modelo 3D em modo Corte"), fig("zenith/renders/zenith_section.png", "ZION ZENITH · modelo 3D em modo Corte"))}
<p class="note">Para regenerar: <code>python3 tools/build_viewer.py</code> e <code>node tools/render.js</code>.</p>
"""
section("09", "Modelo 3D", m3d)

# 10-11 renders ---------------------------------------------------------------
ext = f"""
<p>Renderizações geradas a partir do modelo 3D paramétrico (visualização arquitetônica, não fotorrealista), coerentes com plantas, cortes e listas de materiais. Servem de base para a direção de arte das imagens finais de marketing.</p>
{two(render_pair("cocoon", "ext_front", "ZION COCOON · vista frontal 3/4 com o lábio, a fachada de vidro e o deck"), render_pair("zenith", "ext_front", "ZION ZENITH · vista frontal 3/4 com os dois cumes sobre o terraço"))}
{two(render_pair("cocoon", "ext_side", "ZION COCOON · lateral com as Janelas Olho"), render_pair("zenith", "ext_side", "ZION ZENITH · lateral com o vidro contínuo da suíte"))}
{two(render_pair("cocoon", "ext_rear", "ZION COCOON · cauda"), render_pair("zenith", "ext_rear", "ZION ZENITH · fundos com os painéis ripados"))}
{two(render_pair("cocoon", "ext_aerial", "ZION COCOON · vista aérea com a Espinha de Luz"), render_pair("zenith", "ext_aerial", "ZION ZENITH · vista aérea da membrana"))}
{two(render_pair("cocoon", "night", "ZION COCOON · noite: a concha como lanterna"), render_pair("zenith", "night", "ZION ZENITH · noite: os cumes iluminados por dentro"))}
"""
section("10", "Renderizações externas", ext)
inn = f"""
{two(render_pair("cocoon", "int_living", "ZION COCOON · estar olhando para a suíte e a Espinha de Luz"), render_pair("zenith", "int_living", "ZION ZENITH · estar olhando para a cama sob o Óculo"))}
{two(render_pair("cocoon", "int_bed", "ZION COCOON · da cama para a fachada e o deck"), render_pair("zenith", "int_bed", "ZION ZENITH · da cama para a fachada e o terraço"))}
{two(render_pair("cocoon", "int_bath", "ZION COCOON · banho com a banheira na cauda"), render_pair("zenith", "int_bath", "ZION ZENITH · banho com bancada dupla e banheira"))}
<h3>Direção de arte dos interiores (Zion New Luxury)</h3>
{table(["Elemento", "ZION COCOON", "ZION ZENITH"], [
 ["Piso", "Carvalho de engenharia 14 mm, tom natural; porcelanato cinza-areia no banho", "Idem; deck cumaru no terraço"],
 ["Paredes e forro", "Forro tensionado cor areia seguindo a concha; painel ripado de carvalho na cabeceira", "Forro tensionado seguindo os cumes; painéis de madeira nas paredes fechadas; tecido nas laterais"],
 ["Marcenaria", "Embutida na curva: console café, armário baixo, criados", "Ilha do Café com totem do mastro, closet, bancada dupla"],
 ["Iluminação", "Fita LED 2700 K nos rodapés e nos requadros das Janelas Olho; luz rasante na espinha; sem pendentes", "Fita LED no perímetro do forro e nos rodapés; arandelas nos criados; balizadores no terraço"],
 ["Tons", "Areia, cru, carvalho, bronze; lençóis brancos; cerâmica artesanal", "Areia, carvalho, bronze; pedra na bancada; têxteis em linho"],
 ["Texturas", "Membrana, tecido, madeira, pedra, linho", "Ripado, tecido, madeira, pedra, água"],
])}
"""
section("11", "Renderizações internas", inn)

# 12 estrutura ----------------------------------------------------------------
est = f"""
{two(fig("cocoon/desenhos/12_estrutura_isometrica.svg", "ZION COCOON · estrutura metálica: anel do lábio, arcos, terças, espinha, cabos"), fig("zenith/desenhos/12_estrutura_isometrica.svg", "ZION ZENITH · estrutura metálica: mastros, coroas, anel de beiral, pilares, postes e cabos"))}
<h3>Sistema estrutural</h3>
{two("<h4>ZION COCOON</h4><p>Oito pórticos elípticos planos (A0 a A7), biengastados nos trilhos de base, travados por sete terças longitudinais e pela treliça da Espinha de Luz. A membrana tensionada (pré-tensão 2,5 kN/m) enrijece a concha contra ovalização; cabos em X nos vãos extremos resistem ao vento longitudinal. Uplift de projeto 1,3 kN/m² x 45 m² ≈ 60 kN em 16 pés de arco (≈ 4 kN cada). Peso do aço: " + fmt(BC['steel_kg'], 0) + " kg.</p>",
     "<h4>ZION ZENITH</h4><p>Dois mastros a compressão (M1 45 kN de projeto) com coroas de três braços e anéis de cume; anel de beiral 150 x 100 comprimido pela membrana sobre dez pilares embutidos nos painéis SIP, que formam o diafragma rígido; sete postes externos inclinados e estaiados absorvem os cabos de borda. Uplift de projeto 1,3 kN/m² x 95 m² ≈ 125 kN, distribuído entre pilares, postes e 37 estacas. Peso do aço: " + fmt(BZ['steel_kg'], 0) + " kg.</p>")}
<h3>Perfis e massas</h3>
{two(table(["Código", "Componente", "Perfil", "Qtd", "Comp. (m)", "Massa (kg)"], [list(r) for r in BC["steel_rows"]], foot=["", "Total de aço ZION COCOON", "", "", "", fmt(BC["steel_kg"], 0)]),
     table(["Código", "Componente", "Perfil", "Qtd", "Comp. (m)", "Massa (kg)"], [list(r) for r in BZ["steel_rows"]], foot=["", "Total de aço ZION ZENITH", "", "", "", fmt(BZ["steel_kg"], 0)]))}
<h3>Premissas de cálculo (estudo preliminar)</h3>
{table(["Parâmetro", "Valor", "Referência"], [
 ["Velocidade básica do vento V0", "45 m/s (categoria II, S1 = S3 = 1,0)", "NBR 6123"],
 ["Pressão dinâmica de referência", "q ≈ 1,24 kN/m²", "NBR 6123"],
 ["Coeficientes de forma", "Cpe de -1,2 a +0,8 (concha); -1,4 a +0,6 (cobertura de picos)", "Form-finding e análise de membrana"],
 ["Pré-tensão da membrana", "2,5 kN/m (biaxial)", "Tensile design"],
 ["Aço", "ASTM A500 Gr. B, fy = 290 MPa; galvanização NBR 6323", "NBR 8800"],
 ["Ligações", "Parafusos classe 8.8 zincados; luvas internas com 4 x M12", "NBR 8800"],
 ["Combinações", "Peso próprio + membrana tensionada + vento de sucção; vento com sobrepressão + chuva", "NBR 8681"],
 ["Verificação", "Dimensionamento definitivo por engenheiro estrutural responsável, com ART, antes da fabricação", "Requisito"],
])}
"""
section("12", "Estudo da estrutura metálica", est)

# 13 arcos / mastros ------------------------------------------------------------
arcs = f"""
{fig("detalhes/DET-10_arcos_cocoon.svg", "DET-10 · ZION COCOON · sistema de arcos elípticos, luvas, terças, keder e contraventamento")}
{fig("detalhes/DET-11_mastros_zenith.svg", "DET-11 · ZION ZENITH · mastros, coroas, anéis de cume, anel de beiral e postes")}
<h3>Arcos do ZION COCOON: geometria de fabricação</h3>
{table(["Arco", "Posição x (m)", "Semi-eixo horiz. (m)", "Semi-eixo vert. (m)", "Topo (m)", "Desenvolvido (m)", "Segmentos"],
  [[f"A{i}", fmt(x), fmt(C.a(x)), fmt(C.b(x)), fmt(C.top(x)), fmt(l), "2 (anel inclinado)" if i == 0 else "3 + 2 luvas"] for i, (x, l) in enumerate(zip(C.ARCH_X, BC["arch_lengths"]))])}
<p class="note">Todos os arcos partem da mesma família de elipses (centro a 0,75 m do piso), o que permite um único gabarito de calandra com ajuste de raio por segmento. Perfil Ø88,9 x 3,6 mm; o anel A0 usa Ø101,6 x 4,0 mm por receber a esquadria da fachada e o esforço do lábio em balanço.</p>
"""
section("13", "Sistema de arcos e perfis estruturais", arcs)

# 14-21 detalhes ----------------------------------------------------------------
DET = [("14", "Detalhe do sistema de cobertura", ["DET-01_cobertura_cocoon.svg", "DET-02_cobertura_zenith.svg"],
        "Camadas do envelope: membrana PVDF em perfil keder (Cocoon) ou anéis com clamp (Zenith), câmara ventilada de 60 mm, lã PET 50 mm com manta refletiva e forro tensionado. Inclinação mínima de 12°, autolimpeza pela laca PVDF, garantia de 15 anos da membrana, classe B1 ao fogo e tratamento anti-fungo. Respiro na cumeeira (Cocoon) e chaminé do cume secundário (Zenith) mantêm a câmara ventilada e controlam a condensação."),
       ("15", "Detalhe de ancoragem", ["DET-03_ancoragem.svg"],
        "Pés de arco com chapa 200 x 150 x 10 e 4 chumbadores M16 nas vigas U 150; trilhos de base com clamp de membrana e calha oculta; postes externos com base articulada e estai Ø10 a estacas de tração; bolsas de cabo de borda Ø12 com esticadores nos olhais dos postes. Toda a ancoragem é reversível: a unidade pode ser desmontada e realocada sem deixar concreto no terreno."),
       ("16", "Sistema de fundação", ["DET-04_fundacao.svg"],
        "Estacas helicoidais Ø76 mm com hélice Ø300 mm, comprimento de 1,5 a 2,5 m conforme o solo, capacidade de 25 a 40 kN à compressão e 15 a 25 kN à tração, cravadas por motor hidráulico portátil (sem escavação). Cabeçotes ajustáveis absorvem desníveis de até 8%; em terrenos mais inclinados, estacas mais longas e deck em balanço com guarda-corpo de cabos. Grelha de vigas U 150 x 60 galvanizadas, vigotas tratadas a cada 400 mm, PIR 50 mm, compensado naval e piso de engenharia."),
       ("17", "Detalhe de portas e janelas", ["DET-05_esquadrias.svg"],
        "Janela Olho (Cocoon): requadro de madeira laminada de 220 mm que faz a transição da membrana curva ao vidro duplo plano, com duas unidades basculantes; fachada inclinada 8° em anel de alumínio curvo com porta pivotante 1,00 x 2,40; fachada do Zenith com quatro folhas (duas de correr) e trilho embutido no piso com dreno; janelas em painel SIP com rufos e pingadeiras. Vidros duplos 6 lam + 12 Ar + 6 temp low-e (U ≈ 1,6 W/m²K, FS 0,40)."),
       ("18", "Sistema de drenagem", ["DET-06_drenagem.svg"],
        "A membrana escoa para as bordas: no Cocoon, para a calha oculta de 80 mm no rodapé da concha e dois tubos de queda Ø75 nas extremidades; no Zenith, para os pontos baixos das catenárias (pingadeiras sobre canaletas de brita) e para a calha oculta do anel de beiral com quedas dentro de dois pilares. Dimensionamento para 150 mm/h; destino em caixas de brita, dispersão ou cisterna de reúso."),
       ("19", "Sistema de instalação elétrica", ["DET-07_eletrica.svg"],
        "Entrada 220 V, quadro no ático técnico (12 módulos no Cocoon, 16 no Zenith), circuitos separados para climatização, aquecimento de água, tomadas, iluminação e banho; hidromassagem em circuito próprio com DR 30 mA. Iluminação em fitas LED 2700 K nos rodapés, requadros e forro, sem pendentes; tomadas com USB nos criados e no estar; balizadores no deck. Opcional: kit solar 3 kWp com baterias de 10 kWh. Cabos passam no vazio do piso e atrás do forro."),
       ("20", "Sistema hidráulico", ["DET-08_hidraulica.svg"],
        "Alimentação PEX Ø25 com registro geral e filtro; aquecedor a gás de passagem (23 ou 30 L/min) ou bomba de calor (200 ou 300 L) no ático; ramais quente/frio a bancada, chuveiro, banheira e bacia; esgoto Ø40/50 a coletor Ø100 sob o deck com 2% de declividade e ventilação; fossa séptica com filtro anaeróbio ou estação compacta; águas cinzas separáveis para irrigação. Hidromassagem do Zenith com filtro, bomba e aquecedor de 3 kW próprios."),
       ("21", "Posicionamento de ar-condicionado e aquecimento", ["DET-09_climatizacao.svg"],
        "Evaporadora dutada inverter no ático técnico sobre o banho (12k BTU no Cocoon, 18k no Zenith), difusores lineares na parede da cabeceira e no estar, retorno pelo forro do banho, condensadora atrás da unidade oculta por ripado. Operação em modo bomba de calor até -15 °C; piso radiante elétrico opcional no banho e na suíte; lareira a etanol opcional no Zenith. Ventilação natural pelas janelas basculantes, respiro de cumeeira e chaminé do Respiro; exaustor do banho com recuperação de calor.")]
for num, title, files, text in DET:
    html = f"<p>{text}</p>" + "".join(fig(f"detalhes/{f}", f"{f.split('_')[0]} · {title}") for f in files)
    section(num, title, html)

# 22 lista de materiais -------------------------------------------------------------
def bom_tables(b):
    out = ""
    for g, rows in b["groups"]:
        out += f"<h4>{g}</h4>" + table(["Item", "Un.", "Qtd", "Massa (kg)"], [[d, u, q, fmt(k, 0)] for (d, u, q, k) in rows])
    return out
mat = f"""
<p>Quantidades derivadas da geometria paramétrica (áreas de membrana, comprimentos de arcos, área de piso e deck) e das especificações da Seção 01. Valores preliminares para orçamento de fabricação; a lista definitiva sai do projeto executivo.</p>
{two("<h3>ZION COCOON</h3>" + bom_tables(BC), "<h3>ZION ZENITH</h3>" + bom_tables(BZ))}
"""
section("22", "Lista preliminar de materiais", mat)

# 23 componentes para fabricação --------------------------------------------------
comp = f"""
<p>Cada unidade é um kit de componentes codificados, fabricados industrialmente e pré-montados em bancada sempre que possível (módulos de piso e deck, painéis, quadros de instalações). O código identifica o produto (ZC / ZZ) e a família da peça.</p>
<h3>ZION COCOON</h3>
{table(["Código", "Componente", "Especificação de fabricação", "Qtd", "Processo"], [list(p) for p in cocoon_parts()])}
<h3>ZION ZENITH</h3>
{table(["Código", "Componente", "Especificação de fabricação", "Qtd", "Processo"], [list(p) for p in zenith_parts()])}
"""
section("23", "Lista de componentes para fabricação", comp)

# 24 peso ------------------------------------------------------------------------
peso = f"""
{two("<h3>ZION COCOON</h3>" + table(["Grupo", "Massa (kg)", "%"], [[g, fmt(w, 0), fmt(100 * w / BC['total'], 1)] for g, w in BC["weights"]], foot=["Total embarcado", fmt(BC["total"], 0), "100"]),
     "<h3>ZION ZENITH</h3>" + table(["Grupo", "Massa (kg)", "%"], [[g, fmt(w, 0), fmt(100 * w / BZ['total'], 1)] for g, w in BZ["weights"]], foot=["Total embarcado", fmt(BZ["total"], 0), "100"]))}
{table(["Indicador", "ZION COCOON", "ZION ZENITH"], [
 ["Estrutura metálica de aço", f"{fmt(BC['steel_kg'], 0)} kg", f"{fmt(BZ['steel_kg'], 0)} kg"],
 ["Alumínio e perfis", f"{fmt(BC['alu_kg'], 0)} kg", f"{fmt(BZ['alu_kg'], 0)} kg"],
 ["Peça mais pesada a içar", "Segmento de arco A2 (≈ 30 kg) · anel A0 em 2 partes (≈ 50 kg cada)", "Mastro M1 (76 kg) · segmento do anel de beiral (≈ 71 kg)"],
 ["Carga sobre o terreno", f"≈ {fmt(BC['total'] / 39, 0)} kg por estaca (peso próprio) + sobrecarga de uso", f"≈ {fmt(BZ['total'] / 37, 0)} kg por estaca + hidromassagem cheia (≈ 1.900 kg)"],
 ["Peso por m² de piso interno", f"{fmt(BC['total'] / C.floor_area(), 0)} kg/m²", f"{fmt(BZ['total'] / Z.floor_area(), 0)} kg/m²"],
])}
"""
section("24", "Estimativa de peso da estrutura", peso)

# 25 transporte -----------------------------------------------------------------
def tr_table(t):
    return table(["Volume", "Dimensões", "m³", "kg"], [[d, dim, fmt(v, 1), fmt(k, 0)] for (d, dim, v, k) in t["items"]], foot=["Total", "", fmt(t["vol"], 1), fmt(t["kg"], 0)])
transp = f"""
<p>Cada unidade viaja em um contêiner 40' HC (76 m³, 26 t de carga útil) ou em uma carreta de 12 m com lona, em volumes paletizados de no máximo 5,2 m de comprimento. Nenhuma peça exige transporte especial; os arcos do Cocoon viajam em três segmentos e o anel de beiral do Zenith em seis. Última milha em terrenos naturais: caminhão 3/4 ou trator com carreta para os estrados, com transbordo manual (peças abaixo de 80 kg) ou mini-guindaste de 1 t.</p>
{two("<h3>ZION COCOON</h3>" + tr_table(TC), "<h3>ZION ZENITH</h3>" + tr_table(TZ))}
{table(["Modal", "Capacidade", "Unidades por viagem", "Observação"], [
 ["Contêiner 40' HC (marítimo / rodoviário)", "76 m³ · 26 t", "1 unidade completa (Cocoon: 67% do volume; Zenith: 82%)", "Permite exportação e estoque em porto seco"],
 ["Carreta 12 m com lona", "≈ 90 m³ · 25 t", "1 unidade completa + 1 kit de estrutura extra", "Distribuição nacional"],
 ["Caminhão 3/4 (última milha)", "≈ 22 m³ · 3,5 t", "3 a 4 viagens por unidade", "Acesso a terrenos naturais"],
 ["Helicóptero (opcional, sítios remotos)", "carga externa 1,0 t", "8 a 12 ciclos", "Peças abaixo de 80 kg e estrados abaixo de 1 t"],
])}
"""
section("25", "Sistema de transporte", transp)

# 26 sequência de montagem -------------------------------------------------------
def steps(name):
    rows = [[i + 1, t, d, fmt(days, 1), team] for i, (t, d, days, team) in enumerate(ASSEMBLY[name])]
    return table(["Etapa", "Fase", "Atividades", "Dias", "Equipe"], rows, foot=["", "Total", "", fmt(sum(s[2] for s in ASSEMBLY[name]), 1), "4 montadores + líder"])
mont = f"""
<p>A sequência foi desenhada para uma equipe de quatro montadores e um líder, sem grua: guincho manual de 1 t e talha para os mastros. Toda a montagem é a seco e reversível. Antes do embarque, a estrutura de cada unidade é pré-montada na fábrica para conferência de geometria e a membrana é ajustada sobre ela (fit test).</p>
{two("<h3>ZION COCOON</h3>" + steps("cocoon"), "<h3>ZION ZENITH</h3>" + steps("zenith"))}
<h3>Pontos de controle de qualidade</h3>
{table(["Fase", "Verificação", "Tolerância"], [
 ["Fundação", "Nível dos cabeçotes com nível a laser; torque de cravação registrado por estaca", "± 5 mm; torque mínimo conforme capacidade"],
 ["Estrutura", "Geometria dos arcos / prumo dos mastros; torque dos parafusos", "± 10 mm; prumo 1/500; torque por tabela"],
 ["Membrana", "Pré-tensão uniforme (sem rugas ou bolsas), flecha das bordas, estanqueidade com teste de água", "Rugas zero; flecha ± 20 mm"],
 ["Vidros", "Selagem, drenagem das esquadrias, funcionamento das folhas", "Teste de água 15 min"],
 ["Instalações", "Teste de pressão hidráulica (6 bar, 30 min), teste elétrico (DR, aterramento), climatização em carga", "Sem queda de pressão; DR < 30 mA"],
])}
"""
section("26", "Sequência de montagem", mont)

# 27 tempo ----------------------------------------------------------------------
def gantt(name):
    steps_ = ASSEMBLY[name]; total = sum(s[2] for s in steps_); t = 0; bars = ""
    for i, (title, _, d, _) in enumerate(steps_):
        left = 100 * t / total; w = 100 * d / total
        bars += f'<div class="grow"><div class="glabel">{title}</div><div class="gtrack"><div class="gbar" style="left:{left:.1f}%;width:{w:.1f}%"></div></div><div class="gdays">{fmt(d, 1)} d</div></div>'
        t += d
    return f'<div class="gantt">{bars}</div>'
tempo = f"""
{table(["Indicador", "ZION COCOON", "ZION ZENITH"], [
 ["Fabricação (após aprovação do executivo)", "6 a 8 semanas por unidade; 4 semanas em série a partir da 3ª unidade", "7 a 9 semanas; 5 semanas em série"],
 ["Transporte (fábrica ao sítio)", "1 a 5 dias nacional; 30 a 45 dias marítimo internacional", "Idem"],
 ["Instalação no sítio (dias úteis)", f"{fmt(sum(s[2] for s in ASSEMBLY['cocoon']), 0)} dias", f"{fmt(sum(s[2] for s in ASSEMBLY['zenith']), 0)} dias"],
 ["Do embarque à entrega ao operador", "3 semanas", "3,5 semanas"],
 ["Desmontagem e realocação", "4 dias + 1 dia de fundação nova", "5 dias + 1,5 dia"],
 ["Em série (parque de 10 unidades, 2 equipes)", "≈ 9 semanas de instalação", "≈ 11 semanas de instalação"],
])}
<h3>Cronograma de instalação</h3>
{two("<h4>ZION COCOON · 12 dias úteis</h4>" + gantt("cocoon"), "<h4>ZION ZENITH · 15 dias úteis</h4>" + gantt("zenith"))}
<p class="note">Premissas: acesso de caminhão 3/4 ao sítio, energia provisória e água disponíveis, solo com capacidade para estacas helicoidais de 2,0 m, sem chuva contínua. Fundação e instalações externas (redes, fossa, acesso) correm em paralelo pela equipe do sítio.</p>
"""
section("27", "Tempo estimado de instalação", tempo)

# anexo: negócio ------------------------------------------------------------------
biz = f"""
<p>Os produtos foram desenhados para performar como ativo hoteleiro: fabricáveis em série, transportáveis, montáveis em duas semanas e operáveis com a mesma equipe de um boutique hotel. Ordens de grandeza para o estudo de viabilidade (a confirmar com cotação de fabricação e o Zion Score do destino):</p>
{table(["Indicador", "ZION COCOON", "ZION ZENITH"], [
 ["Posicionamento", "Refúgio de casal, silêncio e imersão", "Suíte assinatura com terraço e hidromassagem"],
 ["Ocupação", "2 adultos", "2 adultos (+ 1 criança no sofá)"],
 ["ADR de referência", "R$ 1.200 a 1.800", "R$ 1.600 a 2.600"],
 ["CAPEX orientativo por unidade (kit + interiores + instalação, sem infraestrutura do sítio; ver Product Book para o orçamento detalhado em 3 cenários)", "R$ 540 a 720 mil (Standard, em série)", "R$ 620 a 800 mil (Standard, em série)"],
 ["Payback orientativo (ocupação 55%, margem operacional 45%)", "4 a 5 anos", "4 a 5 anos"],
 ["Vida útil", "Membrana 15 anos (substituível); estrutura 30+ anos", "Idem"],
 ["Escala", "Kit único, estoque de componentes comuns aos dois produtos, montagem por equipe treinada Zion", "Idem"],
])}
<h3>Próximos passos</h3>
<ol>
 <li>Aprovação do conceito e das dimensões pela diretoria da Zion.</li>
 <li>Registro de desenho industrial das duas geometrias (INPI) e das marcas ZION COCOON e ZION ZENITH.</li>
 <li>Projeto executivo: cálculo estrutural com ART, form-finding da membrana com o fabricante, detalhamento de esquadrias e instalações.</li>
 <li>Protótipo de cada produto no Zion Bubble Glamping (Florianópolis) para validação de montagem, conforto térmico e experiência do hóspede.</li>
 <li>Homologação de fornecedores (metalurgia, membrana, vidros, painéis) e precificação de série.</li>
 <li>Lançamento comercial pela Zion Store e integração ao catálogo da Zion Collection.</li>
</ol>
"""
section("A", "Anexo: operação, escala e próximos passos", biz)

# ----------------------------------------------------------------------------- HTML
fonts = ""
for f, fam, style in (("assets/aventa.woff2", "Aventa", "normal"), ("assets/cormorant.woff2", "Cormorant Garamond", "normal"), ("assets/cormorant-italic.woff2", "Cormorant Garamond", "italic")):
    s = src(f)
    if s:
        fonts += f"@font-face{{font-family:'{fam}';src:url({s}) format('woff2');font-weight:100 900;font-style:{style};font-display:swap;}}\n"

CSS = f"""
{fonts}
:root{{--black:#040605;--green:#1B2117;--cream:#FEF5F0;--sand:#DED6BF;--earth:#8B714E;--paper:#FBF4EC}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:'Aventa','DM Sans',Helvetica,Arial,sans-serif;background:var(--cream);color:var(--green);line-height:1.75;font-size:15px}}
a{{color:var(--earth)}}
.wrap{{display:flex;min-height:100vh}}
nav{{width:270px;flex:0 0 270px;background:var(--black);color:var(--cream);padding:34px 22px;position:sticky;top:0;height:100vh;overflow:auto}}
nav .z{{font-weight:800;letter-spacing:.4em;font-size:22px}}
nav .sub{{display:block;font-size:9px;letter-spacing:.3em;color:var(--sand);margin:4px 0 26px}}
nav a{{display:block;color:var(--sand);text-decoration:none;font-size:11.5px;letter-spacing:.04em;padding:5px 0;border-bottom:1px solid rgba(254,245,240,.08)}}
nav a b{{color:var(--cream);font-weight:600;margin-right:8px}}
nav a:hover{{color:var(--cream)}}
main{{flex:1;min-width:0;padding:0 0 120px}}
section{{padding:70px 6vw 40px;border-bottom:1px solid var(--sand)}}
section .num{{font-size:10.5px;letter-spacing:.34em;text-transform:uppercase;color:var(--earth);display:block;margin-bottom:12px}}
section h2{{font-family:'Cormorant Garamond',Georgia,serif;font-weight:300;font-size:clamp(30px,3.2vw,44px);line-height:1.2;margin-bottom:26px}}
section h3{{font-size:13px;letter-spacing:.28em;text-transform:uppercase;margin:38px 0 14px;color:var(--green)}}
section h4{{font-size:12px;letter-spacing:.18em;text-transform:uppercase;margin:22px 0 10px;color:var(--earth)}}
p{{margin-bottom:14px;max-width:1100px}}
p.lead{{font-family:'Cormorant Garamond',Georgia,serif;font-size:22px;line-height:1.5;max-width:1000px}}
p.note{{font-size:13px;color:#4c5446;max-width:none}}
ul,ol{{margin:0 0 16px 22px;max-width:1000px}} li{{margin-bottom:6px}}
code{{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;background:#f1e8de;padding:1px 5px;border-radius:3px}}
figure{{margin:18px 0 26px}} figure img{{width:100%;height:auto;display:block;border:1px solid var(--sand);background:#fff}}
figcaption{{font-size:11.5px;letter-spacing:.06em;color:var(--earth);margin-top:8px;text-transform:uppercase}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start}}
.grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:16px 0 26px}}
.card{{background:var(--paper);border:1px solid var(--sand);padding:18px 20px}} .card h4{{margin-top:0}}
.tw{{overflow-x:auto;margin:8px 0 22px}}
table{{border-collapse:collapse;width:100%;font-size:12.5px}}
th,td{{border-bottom:1px solid var(--sand);padding:7px 9px;text-align:left;vertical-align:top}}
th{{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--earth);font-weight:600;background:var(--paper)}}
tfoot td{{font-weight:700;background:var(--paper)}}
table.kv th{{width:38%}}
.missing{{border:1px dashed var(--earth);padding:20px;color:var(--earth);font-size:12px;margin:14px 0}}
.cover{{background:var(--black);color:var(--cream);margin:-70px -6vw -40px;padding:110px 8vw 90px;min-height:92vh;display:flex;flex-direction:column;justify-content:center}}
.cover .brand .z{{font-weight:800;letter-spacing:.45em;font-size:30px}} .cover .brand .sub{{display:block;font-size:10px;letter-spacing:.35em;color:var(--sand);margin:6px 0 60px}}
.splitword{{display:flex;align-items:center;gap:26px;font-weight:200;letter-spacing:.5em;font-size:clamp(20px,3vw,40px);color:var(--sand);margin-bottom:34px}}
.splitword .line{{flex:1;height:1px;background:var(--cream);opacity:.35}}
.cover h1{{font-family:'Cormorant Garamond',Georgia,serif;font-weight:300;font-size:clamp(36px,5vw,68px);line-height:1.12;max-width:1100px;margin-bottom:34px}}
.cover .lead{{color:var(--cream);opacity:.9;max-width:900px;font-size:21px}}
.cover .meta{{display:flex;justify-content:space-between;font-size:10px;letter-spacing:.3em;color:var(--sand);margin-top:70px}}
.gantt{{margin:8px 0 20px}} .grow{{display:grid;grid-template-columns:230px 1fr 50px;gap:10px;align-items:center;font-size:12px;margin-bottom:6px}}
.gtrack{{position:relative;height:16px;background:var(--paper);border:1px solid var(--sand)}} .gbar{{position:absolute;top:2px;bottom:2px;background:var(--earth)}}
.gdays{{text-align:right;color:var(--earth)}}
@media(max-width:1100px){{.two,.grid3{{grid-template-columns:1fr}} nav{{display:none}}}}
@media print{{
 @page{{size:A4 landscape;margin:11mm}}
 body{{font-size:11px;background:#fff}} nav{{display:none}} main{{padding:0}}
 section{{page-break-before:always;padding:8mm 0 4mm;border:0}} section:first-of-type{{page-break-before:avoid}}
 .cover{{margin:0;min-height:auto;padding:30mm 16mm;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
 figure{{page-break-inside:avoid}} tr{{page-break-inside:avoid}} .two{{gap:14px}} figure img{{max-height:160mm;width:auto;max-width:100%;margin:0 auto}}
 .card,th,tfoot td,.gtrack,.gbar{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
}}
"""

nav = "".join(f'<a href="#{sid}"><b>{num}</b>{title}</a>' for sid, num, title, _, _ in S)
body = ""
for sid, num, title, html, _ in S:
    if num == "00":
        body += f'<section id="{sid}">{html}</section>'
    else:
        body += f'<section id="{sid}"><span class="num">Entregável {num}</span><h2>{title}</h2>{html}</section>'

HTML = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Zion Cocoon e Zion Zenith · Caderno Técnico</title>
<meta name="description" content="Projeto conceitual, arquitetônico e técnico das unidades de hospedagem ZION COCOON e ZION ZENITH da Zion Glamping Collection: 27 entregáveis.">
<style>{CSS}</style></head>
<body><div class="wrap"><nav><div class="z">ZION</div><span class="sub">GLAMPING COLLECTION · CADERNO TÉCNICO</span>{nav}</nav><main>{body}</main></div></body></html>"""

out = os.path.join(ROOT, ("_print_" if (WEB and not INLINE) else "") + "ZION_COCOON_ZENITH_Caderno_Tecnico" + ("_standalone" if INLINE else "") + ".html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("dossier ->", out, f"{os.path.getsize(out) / 1e6:.2f} MB")

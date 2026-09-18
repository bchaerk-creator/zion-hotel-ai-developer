# -*- coding: utf-8 -*-
"""Base comum dos documentos de mobiliário (ZG-FFE): página, CSS, diagramas SVG da linguagem Zion (arco, pés, raios, ferragens,
tecidos, luminárias, texturas) e paleta. Sem preços."""
import os, html, math
from build_tecnico import CSS as BASE_CSS
from svgkit import zion_mark_html, zion_logo_html, CREAM, GREEN, SAND, EARTH, BLACK

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(ROOT, "08_MOBILIARIO"); os.makedirs(OUT_DIR, exist_ok=True)
def esc(s): return html.escape(str(s))
def h(t, sub=""): return f'<h2>{esc(t)}{f"<small>{esc(sub)}</small>" if sub else ""}</h2>'
def table(head, rows, cls=""):
    th = "".join(f"<th{' class=num' if x.startswith('#') else ''}>{esc(x.lstrip('#'))}</th>" for x in head)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="t {cls}"><tr>{th}</tr>{body}</table>'
def kv(items): return '<dl class="kv">' + "".join(f"<dt>{esc(k)}</dt><dd>{v}</dd>" for k, v in items) + "</dl>"
def ul(items): return '<ul class="chk">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def ol(items): return '<ol class="num">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"
def img(rel, cls=""): return f'<img class="{cls}" src="../{rel}" alt="">' if os.path.exists(os.path.join(ROOT, rel)) else f'<div class="missing">[{esc(rel)}]</div>'
WARN = '<span class="warn">PREMISSA</span>'; PROV = '<span class="cotar">DIMENSÃO PROVISÓRIA</span>'

# ------------------------------------------------------------------ paleta e materiais Zion Furniture
PALETTE = [("ZP-01", "Areia", "#DED6BF", "base · 40 %"), ("ZP-02", "Creme", "#FEF5F0", "base · roupa de cama, forros"), ("ZP-03", "Off-white linho", "#F1EBDF", "cortinas do dossel, estofos claros"), ("ZP-04", "Bege cru", "#CDBFA3", "estofos, tapetes"),
           ("ZP-05", "Caramelo", "#B8834A", "couro natural"), ("ZP-06", "Freijó", "#C9A472", "madeira principal"), ("ZP-07", "Carvalho claro", "#D9C4A3", "tampos, ripados"), ("ZP-08", "Nogueira", "#6B4A32", "detalhes, frisos"),
           ("ZP-09", "Terra", "#8B714E", "acento Zion"), ("ZP-10", "Verde oliva", "#6E7150", "têxteis de acento"), ("ZP-11", "Verde musgo", "#1B2117", "metais escuros, sombras"), ("ZP-12", "Terracota discreta", "#B1543A", "cerâmica, 5 %"), ("ZP-13", "Latão envelhecido", "#A48A57", "ferragens, luminárias"), ("ZP-14", "Preto", "#040605", "pontos: sapatas, parafusos aparentes")]
WOODS = [("ZW-01", "Freijó maciço", "estrutura de camas, cadeiras, mesas, pés", "óleo natural ou verniz PU fosco 10 %", "certificado FSC / DOF · densidade média · estável · tom quente sem vermelho"),
         ("ZW-02", "Carvalho (lâmina ou engenharia)", "tampos, portas, ripados, painéis", "verniz PU fosco 10 %", "lâmina sobre MDF naval em peças largas (custo / estabilidade)"),
         ("ZW-03", "Nogueira", "frisos, cavilhas aparentes, puxadores", "óleo", "só em detalhe: contraste de 1 tom, nunca peça inteira"),
         ("ZW-04", "Teca ou cumaru", "mobiliário externo", "óleo de teca · deixar acinzentar (opção)", "durabilidade classe 1 ao tempo"),
         ("ZW-05", "Bambu laminado", "dossel Bali (Destination DNA Floripa), luminárias", "verniz fosco", "leve, tom claro; alternativa de escala")]
FIBERS = [("ZR-01", "Rattan natural (cana)", "encostos, laterais, painéis do closet, cabeceira", "palhinha indiana sextavada 2,5 mm"), ("ZR-02", "Palha de junco / sisal trançado", "cúpulas de luminária, cestos, tapetes", "trama fechada, verniz fosco à base de água"),
          ("ZR-03", "Corda de algodão / poliéster náutico Ø8", "amarrações (Amarração Zion), assento de espreguiçadeira", "cru ou areia · externo: poliéster"), ("ZR-04", "Fibra sintética tipo rattan (externo)", "mobiliário externo quando exigir intempérie", "só onde o natural não resiste")]
STONES = [("ZS-01", "Travertino romano bruto", "tampos de mesa lateral, bandejas, cuba", "escovado, sem resina brilhante"), ("ZS-02", "Quartzito areia", "bancadas de cozinha e banho", "acabamento acetinado"), ("ZS-03", "Cerâmica artesanal", "vasos, cuba, castiçais, louça", "esmalte fosco areia / verde musgo / terracota")]
METALS = [("ZM-01", "Latão envelhecido (escovado, sem verniz brilhante)", "sapatas, ferragens aparentes, luminárias, torneiras", "pátina natural aceita"), ("ZM-02", "Aço carbono pintado preto fosco (pó)", "estruturas ocultas, arandelas externas, fire pit (corten)", "textura fina"), ("ZM-03", "Inox 304 escovado", "parafusos e conectores ocultos, externo", "nunca cromado brilhante")]
TEXTILES = [("ZT-01", "Linho 100 % lavado 220 g/m²", "cortinas do dossel, cortinas de janela", "off-white · areia", "pré-encolhido · fita de abas (tab top) costurada · lavável 40 °C"),
            ("ZT-02", "Linho / algodão hotelaria 380 g/m², ≥ 40.000 Martindale, antimancha", "estofos de poltronas, sofá, cabeceira, banco", "areia · bege cru · oliva", "espuma D28 / D33 + manta siliconada · capas com zíper"),
            ("ZT-03", "Bouclé lã / poliéster ≥ 50.000 Martindale", "poltrona lounge, cocoon chair", "creme", "Signature / Icon"),
            ("ZT-04", "Couro natural curtido ao vegetal 1,6 mm", "assentos, alças, detalhes", "caramelo", "pátina aceita · Urubici"),
            ("ZT-05", "Lã tecida à mão", "tapetes, mantas (Urubici)", "areia · cru · musgo", "peso 3 kg/m²"),
            ("ZT-06", "Algodão cru / juta", "tapetes, almofadas de chão (Floripa)", "cru", "leve, lavável"),
            ("ZT-07", "Acrílico solution-dyed outdoor", "almofadas externas", "areia", "≥ 1.500 h UV, impermeável")]

CSS = BASE_CSS + """
.page.dark{background:#1B2117;color:#FEF5F0} .page.dark h2,.page.dark h4{color:#FEF5F0} .page.dark h2 small,.page.dark .note{color:#DED6BF} .page.dark .head,.page.dark .foot{color:#DED6BF;border-color:#5A5B5A}
.mood{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:39mm;gap:5px} .mood img{width:100%;height:100%;object-fit:cover;display:block} .mood .w{display:flex;align-items:center;justify-content:center;text-align:center;font-size:11px;letter-spacing:.3em;font-weight:200;border:1px solid var(--sand);padding:6px;line-height:1.5} .mood .sw{border:1px solid var(--sand)} .mood .tx{border:1px solid var(--sand);overflow:hidden} .mood .tx svg{width:100%;height:100%;display:block} .mood .tall{grid-row:span 2}
.sw-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:8px} .sw-grid div{font-size:7.5px;line-height:1.4} .sw-grid i{display:block;height:24mm;border:1px solid var(--sand);margin-bottom:3px} .sw-grid b{display:block;font-size:8px;letter-spacing:.14em} .sw-grid em{font-style:normal;color:var(--earth)}
.tx-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px} .tx-grid div{font-size:8px;line-height:1.45} .tx-grid svg{width:100%;height:30mm;display:block;border:1px solid var(--sand);margin-bottom:3px} .tx-grid b{display:block;font-size:8px;letter-spacing:.14em}
.diag{display:grid;grid-template-columns:repeat(3,1fr);gap:10px} .diag>div{font-size:8.6px;line-height:1.5} .diag svg{width:100%;height:auto;display:block;border:1px solid var(--sand);background:#FBF6EE;margin-bottom:4px} .diag b{display:block;font-size:8.5px;letter-spacing:.16em;margin-bottom:2px}
.diag2{display:grid;grid-template-columns:repeat(2,1fr);gap:12px} .diag2>div{font-size:9px;line-height:1.5} .diag2 svg{width:100%;height:auto;display:block;border:1px solid var(--sand);background:#FBF6EE;margin-bottom:4px} .diag2 b{display:block;font-size:8.5px;letter-spacing:.16em;margin-bottom:2px}
.diag5{display:grid;grid-template-columns:repeat(5,1fr);gap:8px} .diag5>div{font-size:8px;line-height:1.45} .diag5 svg{width:100%;height:auto;display:block;border:1px solid var(--sand);background:#FBF6EE;margin-bottom:3px} .diag5 b{display:block;font-size:8px;letter-spacing:.14em}
.big{font-size:30px;font-weight:200;letter-spacing:.28em;line-height:1.2;margin:8px 0} .quote{font-size:13px;line-height:1.7;font-weight:300;max-width:210mm} .tiers{display:grid;grid-template-columns:repeat(3,1fr);gap:12px} .tiers>div{border-top:2px solid var(--ink);padding-top:6px;font-size:9px;line-height:1.55} .tiers b{display:block;font-size:11px;letter-spacing:.24em;margin-bottom:4px}
.refs{display:grid;grid-template-columns:repeat(3,1fr);gap:8px} .refs figure{margin:0} .refs img{width:100%;height:56mm;object-fit:cover;display:block;border:1px solid var(--sand)} .refs figcaption{font-size:7.8px;line-height:1.45;margin-top:3px;color:var(--ink)}
.words{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:10px;letter-spacing:.3em;font-weight:300} .q10 li{padding:3px 0}
.page img.full{width:100%;height:auto;display:block;border:1px solid var(--sand)}
"""

# ------------------------------------------------------------------ SVG helpers (coordenadas em px, y para baixo)
def svg(w, h_, body, vb=None):
    vb = vb or f"0 0 {w} {h_}"
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" font-family="\'DM Sans\',\'Aventa\',Helvetica,Arial,sans-serif">{body}</svg>'
def txt(x, y, s, size=10, fill=GREEN, anchor="middle", w=400, sp=0.0, rot=0):
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ""
    return f'<text x="{x}" y="{y}" fill="{fill}" text-anchor="{anchor}" style="font-size:{size}px;font-weight:{w};letter-spacing:{sp}em"{tr}>{esc(s)}</text>'
def dimh(x1, x2, y, label, size=8):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{EARTH}" stroke-width="0.7"/><line x1="{x1}" y1="{y - 4}" x2="{x1}" y2="{y + 4}" stroke="{EARTH}" stroke-width="0.7"/>'
            f'<line x1="{x2}" y1="{y - 4}" x2="{x2}" y2="{y + 4}" stroke="{EARTH}" stroke-width="0.7"/>' + txt((x1 + x2) / 2, y - 3, label, size, EARTH))
def dimv(x, y1, y2, label, size=8):
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{EARTH}" stroke-width="0.7"/><line x1="{x - 4}" y1="{y1}" x2="{x + 4}" y2="{y1}" stroke="{EARTH}" stroke-width="0.7"/>'
            f'<line x1="{x - 4}" y1="{y2}" x2="{x + 4}" y2="{y2}" stroke="{EARTH}" stroke-width="0.7"/>' + txt(x - 4, (y1 + y2) / 2, label, size, EARTH, rot=-90))

def arc_path(x1, x2, y, rise):
    """arco raso (Arco Zion) de x1 a x2 com apoio em y e flecha 'rise' para cima; retorna o trecho de path."""
    c = (x1 + x2) / 2; span = x2 - x1
    R = (span ** 2 / 4 + rise ** 2) / (2 * rise)
    return f"M{x1} {y} A{R:.1f} {R:.1f} 0 0 1 {x2} {y}"

def arc_diagram():
    b = ""
    # três vãos com a mesma regra flecha = vão / 12
    for i, span in enumerate((120, 200, 300)):
        x1 = 30 + i * 0 + (0 if i == 0 else 0)
    x, y = 30, 120
    for span in (110, 190, 290):
        rise = span / 12
        b += f'<path d="{arc_path(x, x + span, y, rise)}" fill="none" stroke="{GREEN}" stroke-width="2.2" stroke-linecap="round"/>'
        b += f'<line x1="{x}" y1="{y}" x2="{x + span}" y2="{y}" stroke="{SAND}" stroke-width="0.8" stroke-dasharray="3 3"/>'
        b += dimh(x, x + span, y + 18, f"vão {span * 5:.0f} mm") + txt(x + span / 2, y - rise - 6, f"flecha {rise * 5:.0f} mm", 8, EARTH)
        x += span + 30
    b += txt(30, 30, "ARCO ZION · flecha = vão / 12 · raio único por peça · nunca meia-circunferência", 10, GREEN, "start", 600, 0.08)
    b += txt(30, 46, "aparece no topo da cabeceira, no quadro do dossel, no espaldar da cadeira, no aro da luminária e na saia da mesa", 8.5, EARTH, "start")
    # onde aparece (mini pictogramas)
    px = 30
    for name in ("cabeceira", "dossel", "cadeira", "luminária", "mesa"):
        b += f'<rect x="{px}" y="160" width="110" height="70" fill="none" stroke="{SAND}" stroke-width="0.8"/>'
        if name == "cabeceira": b += f'<path d="{arc_path(px + 15, px + 95, 205, 7)} L{px + 95} 222 L{px + 15} 222 Z" fill="#E9E1D2" stroke="{GREEN}" stroke-width="1.2"/>'
        elif name == "dossel": b += f'<path d="{arc_path(px + 15, px + 95, 185, 7)}" fill="none" stroke="{GREEN}" stroke-width="2"/><line x1="{px + 15}" y1="185" x2="{px + 15}" y2="222" stroke="{GREEN}" stroke-width="2"/><line x1="{px + 95}" y1="185" x2="{px + 95}" y2="222" stroke="{GREEN}" stroke-width="2"/>'
        elif name == "cadeira": b += f'<path d="{arc_path(px + 35, px + 75, 182, 4)} L{px + 75} 200 L{px + 35} 200 Z" fill="#E9E1D2" stroke="{GREEN}" stroke-width="1.2"/><line x1="{px + 30}" y1="205" x2="{px + 80}" y2="205" stroke="{GREEN}" stroke-width="2.5"/><line x1="{px + 33}" y1="205" x2="{px + 30}" y2="224" stroke="{GREEN}" stroke-width="1.5"/><line x1="{px + 77}" y1="205" x2="{px + 80}" y2="224" stroke="{GREEN}" stroke-width="1.5"/>'
        elif name == "luminária": b += f'<path d="{arc_path(px + 30, px + 80, 196, 5)} L{px + 74} 212 L{px + 36} 212 Z" fill="#F1EBDF" stroke="{GREEN}" stroke-width="1.2"/><line x1="{px + 55}" y1="212" x2="{px + 55}" y2="224" stroke="{GREEN}" stroke-width="1.5"/>'
        else: b += f'<rect x="{px + 20}" y="190" width="70" height="5" fill="{GREEN}"/><path d="{arc_path(px + 24, px + 86, 205, 5)}" fill="none" stroke="{GREEN}" stroke-width="1.2"/><line x1="{px + 26}" y1="195" x2="{px + 24}" y2="224" stroke="{GREEN}" stroke-width="1.5"/><line x1="{px + 84}" y1="195" x2="{px + 86}" y2="224" stroke="{GREEN}" stroke-width="1.5"/>'
        b += txt(px + 55, 242, name, 8, EARTH); px += 125
    return svg(690, 255, b)

def leg_svg(top, bot, hgt, angle, label, sub):
    """pé cônico inclinado (mm): vista frontal com sapata de latão."""
    s = 0.40; W, H = 160, 250
    cx = 80; y0 = 40; hh = hgt * s
    dx = math.tan(math.radians(angle)) * hh
    pts = [(cx - top * s / 2, y0), (cx + top * s / 2, y0), (cx + dx + bot * s / 2, y0 + hh), (cx + dx - bot * s / 2, y0 + hh)]
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    b = f'<polygon points="{d}" fill="#D9C4A3" stroke="{GREEN}" stroke-width="1.2" stroke-linejoin="round"/>'
    fy = y0 + hh - 15 * s * 1.6
    b += f'<polygon points="{cx + dx - bot * s / 2 - 0.5:.1f},{fy:.1f} {cx + dx + bot * s / 2 + 0.5:.1f},{fy:.1f} {cx + dx + bot * s / 2:.1f},{y0 + hh:.1f} {cx + dx - bot * s / 2:.1f},{y0 + hh:.1f}" fill="#A48A57" stroke="{GREEN}" stroke-width="0.8"/>'
    b += f'<line x1="{cx}" y1="{y0 - 10}" x2="{cx}" y2="{y0 + hh + 8}" stroke="{SAND}" stroke-width="0.8" stroke-dasharray="3 3"/>'
    b += dimh(cx - top * s / 2, cx + top * s / 2, y0 - 12, f"{top}") + dimh(cx + dx - bot * s / 2, cx + dx + bot * s / 2, y0 + hh + 16, f"{bot}") + dimv(cx + 55, y0, y0 + hh, f"{hgt}")
    b += txt(cx + 30, y0 + 22, f"{angle}°", 8, EARTH, "start")
    b += txt(W / 2, H - 16, label, 9, GREEN, "middle", 600, 0.1) + txt(W / 2, H - 5, sub, 7.5, EARTH)
    return svg(W, H, b)

def radius_svg():
    b = txt(20, 24, "RAIOS ZION · três raios para toda a coleção", 10, GREEN, "start", 600, 0.08)
    x = 30
    for r, name, use in ((12, "R1 · 12 mm", "arestas de tampos, pés, quadros"), (24, "R2 · 24 mm", "cantos de tampos, cabeceira, portas"), (60, "R3 · 60 mm", "encostos, braços, cúpulas, bandejas")):
        s = 1.4; R = r * s
        b += f'<path d="M{x} 150 L{x} {60 + R} A{R} {R} 0 0 1 {x + R} 60 L{x + 150} 60" fill="#E9E1D2" stroke="{GREEN}" stroke-width="1.5"/><line x1="{x + 150}" y1="60" x2="{x + 150}" y2="150" stroke="{SAND}" stroke-width="0.8"/><line x1="{x}" y1="150" x2="{x + 150}" y2="150" stroke="{SAND}" stroke-width="0.8"/>'
        b += txt(x + 75, 172, name, 9, GREEN, "middle", 600) + txt(x + 75, 184, use, 7.5, EARTH)
        x += 200
    b += txt(20, 208, "Regra: uma peça usa no máximo dois raios; a aresta que a mão toca é sempre R1; o canto que o olho vê é R2 ou R3. Nunca chanfro.", 8.5, EARTH, "start")
    return svg(640, 220, b)

def weave_svg():
    """Amarração Zion: trama de corda no encontro pé / travessa."""
    b = txt(20, 24, "AMARRAÇÃO ZION · corda Ø8 em X sobre o nó, 6 voltas, arremate embutido", 10, GREEN, "start", 600, 0.08)
    b += f'<rect x="60" y="60" width="34" height="150" fill="#D9C4A3" stroke="{GREEN}" stroke-width="1.2"/><rect x="94" y="95" width="180" height="30" fill="#D9C4A3" stroke="{GREEN}" stroke-width="1.2"/>'
    for i in range(6):
        y = 84 + i * 9
        b += f'<path d="M62 {y} Q77 {y - 6} 92 {y} Q107 {y + 6} 122 {y}" fill="none" stroke="#B8A282" stroke-width="5.5" stroke-linecap="round"/><path d="M62 {y + 4} Q77 {y + 10} 92 {y + 4} Q107 {y - 2} 122 {y + 4}" fill="none" stroke="#CDBFA3" stroke-width="5.5" stroke-linecap="round"/>'
    b += txt(300, 90, "1 · a corda esconde o parafuso e a cavilha", 8.5, GREEN, "start") + txt(300, 104, "2 · trama em X com 6 voltas, tensão manual", 8.5, GREEN, "start") + txt(300, 118, "3 · arremate por dentro da travessa (furo Ø9)", 8.5, GREEN, "start") + txt(300, 132, "4 · corda cru interna · poliéster areia externa", 8.5, GREEN, "start")
    b += txt(300, 160, "Onde: cadeira, poltrona, espreguiçadeira, luminária de piso, banco, day bed.", 8.5, EARTH, "start") + txt(300, 174, "Nunca: em peças que o hóspede limpa com produto (banho).", 8.5, EARTH, "start")
    return svg(640, 225, b)

def friso_svg():
    b = txt(20, 24, "FRISO ZION · rebaixo de sombra de 4 x 4 mm a 1/3 da altura", 10, GREEN, "start", 600, 0.08)
    b += f'<rect x="60" y="50" width="220" height="150" fill="#D9C4A3" stroke="{GREEN}" stroke-width="1.2"/><rect x="60" y="148" width="220" height="4" fill="#8B714E"/>'
    b += dimv(300, 50, 200, "H") + dimv(320, 148, 200, "H/3")
    b += txt(360, 80, "Linha contínua que dá leveza ao volume e alinha", 8.5, GREEN, "start") + txt(360, 94, "gavetas, portas e frentes de armário.", 8.5, GREEN, "start") + txt(360, 116, "Mesmo friso na base das luminárias e no rodapé", 8.5, GREEN, "start") + txt(360, 130, "do closet: a peça parece flutuar.", 8.5, GREEN, "start") + txt(360, 160, "Nogueira (ZW-03) dentro do friso nas peças Icon.", 8.5, EARTH, "start")
    return svg(640, 220, b)

def veil_svg():
    b = txt(20, 24, "VÉU ZION · o tecido nasce da estrutura: trilho oculto no quadro", 10, GREEN, "start", 600, 0.08)
    # secção do rail com trilho
    b += f'<rect x="60" y="60" width="70" height="40" fill="#D9C4A3" stroke="{GREEN}" stroke-width="1.2"/><rect x="80" y="86" width="30" height="14" fill="#FBF6EE" stroke="{GREEN}" stroke-width="1"/><circle cx="95" cy="93" r="3" fill="#A48A57"/>'
    b += f'<path d="M95 100 L95 120 M90 120 Q95 128 100 120" fill="none" stroke="{GREEN}" stroke-width="1"/>'
    for i in range(7):
        x = 82 + i * 4
        b += f'<path d="M{x} 128 Q{x + 2} 170 {x} 210" fill="none" stroke="#B8A282" stroke-width="1.2"/>'
    b += txt(150, 72, "quadro do dossel 40 x 70 mm com rasgo 30 x 14", 8.5, GREEN, "start") + txt(150, 86, "trilho de alumínio embutido + deslizadores silenciosos", 8.5, GREEN, "start") + txt(150, 100, "cortina de linho com abas costuradas nos deslizadores", 8.5, GREEN, "start") + txt(150, 122, "Sem varão aparente, sem argola de metal, sem ilhós.", 8.5, EARTH, "start") + txt(150, 136, "Retirar para lavar: destravar 2 clipes por lado.", 8.5, EARTH, "start")
    b += txt(150, 164, "Mesma lógica nas cortinas de janela (trilho no forro),", 8.5, GREEN, "start") + txt(150, 178, "no biombo do banho e na sombra do day bed externo.", 8.5, GREEN, "start")
    return svg(640, 225, b)

def hardware_svg():
    items = [("Parafuso de cama M10 + porca-tambor", "Encaixe pé / travessa das camas e bancos; sem folga, desmonta 50 vezes"),
             ("Cavilha Ø10 de nogueira", "Alinha e trava juntas; aparente só nas peças Icon"),
             ("Minifix / Confirmat ocultos", "Marcenaria de painéis; furos tampados com lâmina"),
             ("Sapata de latão 15 mm", "Fim de todo pé: protege a madeira do piso úmido e assina a peça"),
             ("Trilho embutido + deslizador", "Cortinas do dossel e de janela"),
             ("Dobradiça de caneco 110° amortecida", "Portas de armário, minibar e amenity"),
             ("Corrediça oculta com toque", "Gavetas: sem puxador; rebaixo de dedo em nogueira"),
             ("Nivelador M8 na sapata", "Deck e piso de Bubble nunca são planos")]
    b = ""
    for i, (n, d) in enumerate(items):
        y = 30 + i * 26
        b += f'<circle cx="24" cy="{y - 4}" r="7" fill="#A48A57" stroke="{GREEN}" stroke-width="0.8"/>' + txt(40, y - 1, n, 9, GREEN, "start", 600) + txt(40, y + 10, d, 8, EARTH, "start")
    return svg(640, 245, b)

def lamp_svg():
    b = ""
    defs = [("Bedside", "Ø260 x 420", "base torneada em freijó + cúpula em linho com aro Arco", 0), ("Floor", "Ø420 x 1.550", "tripé em freijó com Amarração + cúpula cônica em palha", 1), ("Pendant", "Ø600 x 380", "cesto de rattan aberto embaixo, LED difuso", 2), ("Wall", "260 x 180", "braço articulado em latão + cúpula de palha", 3), ("Outdoor lantern", "180 x 180 x 360", "quadro de latão / preto, vidro, vela LED recarregável", 4)]
    for name, dims, desc, i in defs:
        x = 20 + i * 124
        b += f'<rect x="{x}" y="20" width="112" height="150" fill="none" stroke="{SAND}" stroke-width="0.8"/>'
        cx = x + 56
        if i == 0: b += f'<path d="{arc_path(cx - 28, cx + 28, 70, 5)} L{cx + 24} 100 L{cx - 24} 100 Z" fill="#F1EBDF" stroke="{GREEN}" stroke-width="1.2"/><path d="M{cx - 8} 100 L{cx - 6} 150 L{cx + 6} 150 L{cx + 8} 100 Z" fill="#D9C4A3" stroke="{GREEN}" stroke-width="1"/><rect x="{cx - 14}" y="150" width="28" height="6" fill="#A48A57"/>'
        elif i == 1: b += f'<path d="M{cx - 30} 100 L{cx + 30} 100 L{cx + 12} 55 L{cx - 12} 55 Z" fill="#E4D6B8" stroke="{GREEN}" stroke-width="1.2"/><line x1="{cx}" y1="100" x2="{cx - 22}" y2="160" stroke="{GREEN}" stroke-width="2"/><line x1="{cx}" y1="100" x2="{cx + 22}" y2="160" stroke="{GREEN}" stroke-width="2"/><line x1="{cx}" y1="100" x2="{cx}" y2="160" stroke="{GREEN}" stroke-width="2"/><ellipse cx="{cx}" cy="102" rx="6" ry="4" fill="#B8A282"/>'
        elif i == 2: b += f'<line x1="{cx}" y1="24" x2="{cx}" y2="60" stroke="{GREEN}" stroke-width="1"/><path d="M{cx - 40} 60 Q{cx - 44} 120 {cx - 30} 128 L{cx + 30} 128 Q{cx + 44} 120 {cx + 40} 60 Z" fill="#E4D6B8" stroke="{GREEN}" stroke-width="1.2"/>' + "".join(f'<line x1="{cx - 36 + k * 9}" y1="62" x2="{cx - 30 + k * 8}" y2="126" stroke="#B8A282" stroke-width="0.8"/>' for k in range(9))
        elif i == 3: b += f'<rect x="{x + 10}" y="70" width="8" height="30" fill="#A48A57"/><line x1="{x + 18}" y1="85" x2="{cx + 10}" y2="70" stroke="#A48A57" stroke-width="3"/><path d="M{cx - 6} 70 L{cx + 30} 70 L{cx + 22} 96 L{cx + 2} 96 Z" fill="#E4D6B8" stroke="{GREEN}" stroke-width="1.2"/>'
        else: b += f'<rect x="{cx - 22}" y="50" width="44" height="80" fill="#FBF6EE" stroke="{GREEN}" stroke-width="1.5"/><path d="M{cx - 22} 50 L{cx} 36 L{cx + 22} 50" fill="none" stroke="{GREEN}" stroke-width="1.5"/><rect x="{cx - 5}" y="100" width="10" height="22" fill="#F1EBDF" stroke="{GREEN}" stroke-width="0.8"/><circle cx="{cx}" cy="98" r="3" fill="#E8B84A"/>'
        b += txt(cx, 186, f"Zion {name} Lamp", 8.5, GREEN, "middle", 600) + txt(cx, 197, dims + " mm", 7.5, EARTH)
        # descrição em 2 linhas
        words = desc.split(" "); l1 = " ".join(words[:5]); l2 = " ".join(words[5:])
        b += txt(cx, 209, l1, 7, EARTH) + txt(cx, 219, l2, 7, EARTH)
    b += txt(20, 240, "Regras: 2700 K · IRC ≥ 90 · dimerizável 1 a 100 % · luz sempre filtrada por fibra ou linho · nenhum LED visível · corpo em madeira torneada e latão · cabo têxtil areia · IP44 no banho, IP65 fora.", 8, GREEN, "start")
    return svg(640, 250, b)

def texture_svg(kind, w=200, hh=110):
    b = f'<rect width="{w}" height="{hh}" fill="#F1EBDF"/>'
    if kind == "rattan":  # palhinha sextavada
        b = f'<rect width="{w}" height="{hh}" fill="#E4D6B8"/>'
        for y in range(-10, hh + 10, 12):
            for x in range(-10, w + 10, 12):
                b += f'<rect x="{x}" y="{y}" width="8" height="8" fill="#F5EEDC" stroke="#B8A282" stroke-width="1"/>'
        b += "".join(f'<line x1="{x}" y1="0" x2="{x + 60}" y2="{hh}" stroke="#B8A282" stroke-width="1" opacity=".5"/>' for x in range(-60, w, 12))
    elif kind == "palha":
        b = f'<rect width="{w}" height="{hh}" fill="#D9C08F"/>' + "".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y + 30}" stroke="#B89A5E" stroke-width="2.2"/>' for y in range(-30, hh, 7)) + "".join(f'<line x1="{x}" y1="0" x2="{x - 30}" y2="{hh}" stroke="#EAD6A8" stroke-width="1.4"/>' for x in range(0, w + 30, 7))
    elif kind == "linho":
        b = f'<rect width="{w}" height="{hh}" fill="#F1EBDF"/>' + "".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="#D9CFBB" stroke-width="0.8"/>' for y in range(0, hh, 3)) + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{hh}" stroke="#D9CFBB" stroke-width="0.8"/>' for x in range(0, w, 3))
    elif kind == "ripado":
        b = f'<rect width="{w}" height="{hh}" fill="#3B3327"/>' + "".join(f'<rect x="{x}" y="0" width="12" height="{hh}" fill="#C9A472"/><rect x="{x}" y="0" width="2" height="{hh}" fill="#E0C494"/>' for x in range(4, w, 20))
    elif kind == "travertino":
        b = f'<rect width="{w}" height="{hh}" fill="#E6DCC8"/>' + "".join(f'<path d="M0 {y} Q{w / 4} {y - 4} {w / 2} {y + 2} T{w} {y - 2}" fill="none" stroke="#CDBFA3" stroke-width="{1 + (y % 3)}" opacity=".8"/>' for y in range(6, hh, 11)) + "".join(f'<ellipse cx="{(k * 37) % w}" cy="{(k * 53) % hh}" rx="3" ry="1.5" fill="#D8CCB4"/>' for k in range(30))
    elif kind == "couro":
        b = f'<rect width="{w}" height="{hh}" fill="#B8834A"/>' + "".join(f'<circle cx="{(k * 41) % w}" cy="{(k * 29) % hh}" r="{1 + (k % 3) * .5}" fill="#A6703C" opacity=".8"/>' for k in range(220))
    elif kind == "la":
        b = f'<rect width="{w}" height="{hh}" fill="#EDE4D4"/>' + "".join(f'<circle cx="{(k * 23) % w}" cy="{(k * 17) % hh}" r="4" fill="none" stroke="#CDBFA3" stroke-width="1.6"/>' for k in range(180))
    elif kind == "freijo":
        b = f'<rect width="{w}" height="{hh}" fill="#C9A472"/>' + "".join(f'<path d="M0 {y} Q{w / 3} {y + 3} {2 * w / 3} {y - 2} T{w} {y + 1}" fill="none" stroke="#B08A58" stroke-width="{0.6 + (y % 2) * .5}"/>' for y in range(3, hh, 6))
    elif kind == "latao":
        b = f'<rect width="{w}" height="{hh}" fill="#A48A57"/>' + "".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="#C7AE78" stroke-width="0.6" opacity=".7"/>' for y in range(0, hh, 2)) + f'<rect width="{w}" height="{hh}" fill="url(#g)" opacity=".25"/>'
    return svg(w, hh, b)

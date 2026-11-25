#!/usr/bin/env python3
"""Gera bloco_entregaveis.html: seção 'Entregáveis' enxuta, um cartão por etapa (HTML + CSS inline, sem JS, sem base64, sem <span>).
Fatos: INVENTARIO.md seção 1 e classrooms_details da turma 087479a3 (25/11/2026): 2 vídeos e 1 ficha por pilar; e-book por pilar;
Pilar 6 com 2 planilhas de cálculo; Pilar 7 com Kit do Investidor (modelos); Marco Zero com diagnóstico prévio (Página 0).
Uso: python3 -I build_bloco.py"""
from html import escape
from pathlib import Path

def e(t):
    return escape(t, quote=False)

IC = {  # ícones simples em SVG inline (sem imagem externa)
    "video": '<path d="M8 5v14l11-7z"/>',
    "ficha": '<path d="M6 3h9l4 4v14H6zM9 12h7M9 16h7"/>',
    "ebook": '<path d="M5 4h10a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3zM8 8h6"/>',
    "planilha": '<path d="M4 5h16v14H4zM4 10h16M4 15h16M10 5v14"/>',
    "kit": '<path d="M4 8h16v11H4zM9 8V5h6v3M4 13h16"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
}

def chip(ic, txt):
    return (f'<li class="ent-chip"><svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true" fill="none" '
            f'stroke="#c9b37e" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{IC[ic]}</svg>'
            f'<b>{e(txt)}</b></li>')

V2, F1, EB = ("video", "2 vídeos"), ("ficha", "1 ficha"), ("ebook", "e-book")

# (selo, nome, o que é, para quê, selinhos)
CARDS = [
    ("Comece aqui", "Onboarding", "Boas-vindas e o seu dossiê inicial.", "Entender como a plataforma funciona.",
     [("video", "1 vídeo"), ("ficha", "1 formulário"), ("chat", "suporte")]),
    ("Marco Zero", "A visão da jornada", "Visão da jornada e diagnóstico prévio (Página 0).", "Saber por onde começar.",
     [V2, F1, EB]),
    ("Dossiê 1", "Território", "O seu terreno e o destino em volta.", "Descrever o terreno numa página só.", [V2, F1, EB]),
    ("Dossiê 2", "Mercado", "Comparáveis, diária, ocupação e demanda.", "Levantar esses dados da sua região.", [V2, F1, EB]),
    ("Dossiê 3", "Produto", "Nicho, público, promessa e unidade.", "Definir o que oferecer e para quem.", [V2, F1, EB]),
    ("Dossiê 4", "Modelo de Negócio", "Como o projeto gera resultado: renda ou venda.", "Escolher o caminho do projeto.", [V2, F1, EB]),
    ("Dossiê 5", "Masterplan", "O terreno no papel, em fases.", "Ver o que cabe e começar pela fase um.", [V2, F1, EB]),
    ("Dossiê 6", "Pré-viabilidade", "O custo e a conta, com três cenários.", "Fazer a conta com as suas premissas.",
     [V2, F1, EB, ("planilha", "planilhas")]),
    ("Dossiê 7", "Capital", "De onde vem o capital e o Dossiê final.", "Decidir: avançar, ajustar ou parar.",
     [V2, F1, EB, ("kit", "Kit do Investidor")]),
]

CSS = """
.ent-sec{background:#ded6bf;color:#1b2117;padding:36px 0 32px;font-family:'Jost',sans-serif}
.ent-sec .w{max-width:860px;margin:0 auto;padding:0 18px}
.ent-sec p.ent-k{font-family:'Jost',sans-serif;font-size:11.5px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:#6b5636;margin:0 0 10px;line-height:1.4}
.ent-sec h2.ent-h{font-family:'Cormorant Garamond',serif;font-weight:500;font-size:30px;line-height:1.1;color:#1b2117!important;margin:0}
.ent-sec p.ent-intro{font-family:'Jost',sans-serif;font-size:16px;font-weight:400;line-height:1.45;color:#1b2117;margin:10px 0 0}
.ent-lista{display:grid;grid-template-columns:minmax(0,1fr);gap:10px;margin:18px 0 0;padding:0}
.ent-card{background:#1b2117;border:1px solid #c9b37e66;border-radius:14px;padding:14px 14px 12px;margin:0;min-width:0}
.ent-top{display:flex;align-items:center;gap:10px;margin:0}
.ent-sec p.ent-selo{font-family:'Jost',sans-serif;font-size:14px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#040605;background:#c9b37e;border-radius:8px;padding:6px 10px;margin:0;line-height:1.1;white-space:nowrap}
.ent-sec h3.ent-t{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:23px;line-height:1.1;color:#fef5f0!important;margin:0;min-width:0}
.ent-sec p.ent-ln{font-family:'Jost',sans-serif;font-size:14.5px;font-weight:300;line-height:1.35;color:#fef5f0;margin:8px 0 0}
.ent-sec p.ent-ln b{font-weight:500;color:#c9b37e}
.ent-chips{display:flex;flex-wrap:wrap;gap:6px;list-style:none;margin:10px 0 0;padding:0}
.ent-sec li.ent-chip{display:inline-flex;align-items:center;gap:5px;font-family:'Jost',sans-serif;font-size:12.5px;line-height:1;color:#fef5f0;background:#040605;border:1px solid #c9b37e55;border-radius:99px;padding:6px 10px 6px 8px;margin:0}
.ent-sec li.ent-chip::before,.ent-sec li.ent-chip::marker{content:none}
.ent-sec li.ent-chip b{font-weight:400;color:#fef5f0}
.ent-fim{background:#040605;border:1px solid #c9b37e;border-radius:16px;padding:18px 16px;margin:12px 0 0}
.ent-sec p.ent-fk{font-family:'Jost',sans-serif;font-size:11.5px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:#c9b37e;margin:0;line-height:1.4}
.ent-sec p.ent-fp{font-family:'Cormorant Garamond',serif;font-size:23px;font-weight:500;line-height:1.2;color:#fef5f0;margin:6px 0 0}
.ent-sec p.ent-fp b{font-weight:700;color:#c9b37e}
.ent-sec p.ent-opc{font-family:'Jost',sans-serif;font-size:13.5px;font-weight:300;line-height:1.4;color:#ded6bf;border-top:1px solid #c9b37e40;margin:12px 0 0;padding:10px 0 0}
.ent-sec p.ent-opc b{font-weight:500;color:#c9b37e}
.ent-sec p.ent-nota{font-family:'Jost',sans-serif;font-size:12.5px;font-weight:400;line-height:1.4;color:#4a3d28;margin:10px 0 0}
@media (min-width:820px){.ent-sec{padding:56px 0}.ent-sec h2.ent-h{font-size:40px}.ent-lista{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.ent-card:last-child{grid-column:1/-1}.ent-sec h3.ent-t{font-size:25px}.ent-sec p.ent-fp{font-size:28px}}
"""

def card(c):
    selo, nome, o, p, chips = c
    return (
        '<article class="ent-card">'
        f'<div class="ent-top"><p class="ent-selo">{e(selo)}</p><h3 class="ent-t">{e(nome)}</h3></div>'
        f'<p class="ent-ln"><b>O que é:</b> {e(o)}</p>'
        f'<p class="ent-ln"><b>Para quê:</b> {e(p)}</p>'
        '<ul class="ent-chips">' + "".join(chip(i, t) for i, t in chips) + '</ul>'
        '</article>')

FIM = (
    '<div class="ent-fim">'
    '<p class="ent-fk">No final você tem</p>'
    '<p class="ent-fp"><b>O seu Dossiê completo (PDF)</b>, pronto para apresentar a sócios, parceiros ou investidores.</p>'
    '<p class="ent-opc"><b>Opcional:</b> cadastre seu terreno no banco de áreas da Zion (a Zion avalia cada caso; sem garantia de parceria ou investimento).</p>'
    '</div>')

def bloco(sec_id="entregaveis", css=True):
    body = (
        f'<section data-cx-section="solution" id="{sec_id}" class="sec ent-sec"><div class="w">'
        '<p class="ent-k">Etapa por etapa</p>'
        '<h2 class="ent-h">O que você recebe em cada etapa.</h2>'
        '<p class="ent-intro">Em cada etapa você assiste, preenche uma ficha e monta uma página do seu Dossiê.</p>'
        '<div class="ent-lista">' + "".join(card(c) for c in CARDS) + '</div>'
        + FIM +
        '<p class="ent-nota">Material educativo. O resultado depende do que você preencher.</p>'
        '</div></section>')
    return (f'<style>{CSS}</style>' if css else '') + body

if __name__ == "__main__":
    out = Path(__file__).with_name("bloco_entregaveis.html")
    h = bloco()
    out.write_text(h, encoding="utf-8")
    print(out, len(h), "bytes; span:", h.count("<span"), "script:", h.count("<script"), "base64:", h.count("base64"))

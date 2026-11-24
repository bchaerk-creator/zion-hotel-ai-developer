#!/usr/bin/env python3
"""Gera index.html da PÁGINA CURTA do teste de venda direta (R$ 97).

Mesmas regras e estilo da página /inscricao (../../landing/build.py): fontes
Cormorant Garamond e Jost, cores Zion, data-cx-section, data-cx-cta, um
<div data-cx-checkout>, sem <script>, sem base64, sem <span>.
Uso: python3 -I build.py
"""
import re
from html import escape
from pathlib import Path

BASE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
BTN = "FAÇA A SUA INSCRIÇÃO"
AVAL = "Avaliamos cada ideia, cada região e cada terreno. Parcerias e investimentos dependem dessa avaliação."

# Reaproveita o CSS da página atual (mesmas classes) e acrescenta só o que é da página curta.
landing = (Path(__file__).resolve().parent.parent.parent / "landing" / "build.py").read_text(encoding="utf-8")
CSS = landing.split('CSS = """')[1].split('"""')[0]
CSS += """
/* página curta */
#hero{padding-bottom:30px}
#hero .video{margin-top:18px}
#hero .btn{margin-top:18px}
.sec p.leg{margin-top:8px}
.passos.curto{margin-top:16px}
#oferta{padding:34px 0 8px}
#oferta h2{font-size:30px}
#oferta .centro{margin-top:4px}
#pagar{padding-top:10px}
#pagar .pagar{margin-top:14px}
.sec p.aval{text-align:center;font-size:15.5px;line-height:1.55;margin-top:20px}
footer p.reemb{color:#fef5f0;font-size:13.5px}
@media (min-width:820px){#oferta h2{font-size:38px}}
"""


def e(t):
    return escape(t, quote=False)


def btn():
    return f'<a href="#pagar" data-cx-cta class="btn">{BTN}</a>'


def sec(kind, tone, inner, sid=None, extra=""):
    i = f' id="{sid}"' if sid else ""
    return f'<section data-cx-section="{kind}"{i} class="sec {tone}{extra}"><div class="w">{inner}</div></section>'


PASSOS = ["Assista aos nossos vídeos", "Preencha os formulários", "Anexe o que você tem"]
passos = "".join(f'<div class="passo"><div class="n">{i}</div><p>{e(t)}</p></div>' for i, t in enumerate(PASSOS, 1))

blocos = []
blocos.append(f'<div class="escuro"><div class="w topo"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion Hotel Group International" width="170" height="34"></div></div>')

# Topo: título, subtítulo, vídeo, botão
blocos.append(sec("hero", "escuro",
    '<p class="k">Zion Collection Club</p>'
    '<h1>Faça a sua inscrição.<br>Queremos te conhecer.<br>Seja um <em>parceiro Zion</em>.</h1>'
    '<p class="sub">Transforme o seu terreno em destino turístico com a nossa plataforma.</p>'
    + btn() +
    f'<video class="video" controls playsinline preload="metadata" poster="{BASE}zion-collection/club/video/poster.jpg" src="{BASE}zion-collection/club/video/plataforma-v02.mp4">O seu navegador não reproduz este vídeo.</video>'
    '<p class="leg">Vídeo: a plataforma Zion Collection por dentro (8 minutos).</p>'
    + btn(),
    sid="hero"))

# O que você constrói + selo + checkout
blocos.append(sec("offer", "escuro",
    '<p class="k">O que você constrói</p>'
    '<h2>Simples e guiado, como um tutorial.</h2>'
    f'<div class="passos curto">{passos}</div>'
    '<div class="centro"><p class="selo">Acesso à plataforma · R$ 97 · Pagamento único</p></div>',
    sid="oferta"))

blocos.append(sec("cta", "escuro",
    '<div class="pagar"><div data-cx-checkout></div></div>'
    f'<p class="aval">{e(AVAL)}</p>',
    sid="pagar"))

# FAQ mínimo (só para cumprir a seção; uma pergunta)
blocos.append(sec("faq", "creme",
    '<div class="cm-accordion-header">Posso pedir reembolso?</div>'
    '<div class="cm-accordion-content">Sim, em até 7 dias, como prevê o Código de Defesa do Consumidor.</div>',
    extra=" faq"))

blocos.append(
    '<footer><div class="w"><p class="reemb">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p>'
    '<p>Zion Hotel Group International · Conteúdo educacional. Resultados dependem do contexto e da execução. Suporte: WhatsApp +55 48 6137-1061</p></div></footer>')

HTML = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Zion Collection Club | Faça a sua inscrição</title>
<meta name="description" content="Faça a sua inscrição na plataforma Zion Collection. R$ 97, pagamento único.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
{"".join(blocos)}
</body>
</html>
"""
out = Path(__file__).with_name("index.html")
out.write_text(HTML, encoding="utf-8")
print(out, len(HTML), "bytes; <span>:", HTML.count("<span"), "; 270:", HTML.count("270"))

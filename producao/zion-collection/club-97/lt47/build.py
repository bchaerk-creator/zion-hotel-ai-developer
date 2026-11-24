#!/usr/bin/env python3
"""Landing unica /parceiro-zion · venda direta R$ 47 (oferta 668391e7-f4a8-4bd3-a212-deba406f8a7a).
Reaproveita o CSS de ../landing/build.py. Uso: python3 -I build.py"""
from html import escape
from pathlib import Path
import re

AQUI = Path(__file__).parent
antigo = (AQUI.parent / "landing" / "build.py").read_text(encoding="utf-8")
CSS = re.search(r'CSS = """(.*?)"""', antigo, re.S).group(1)
CSS += """
.foto.aerea{aspect-ratio:4/3;object-position:50% 45%}
.moldura{flex:0 0 58%;max-width:230px;margin:0;scroll-snap-align:start}
.moldura .celular{background:#040605;border:2px solid #c9b37e80;border-radius:26px;padding:8px 6px 10px}
.moldura img{width:100%;height:auto;display:block;border-radius:18px}
.sec .moldura p{font-size:13.5px;margin:10px 0 0}
.sec .moldura p.real{color:#c9b37e;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;font-weight:400;margin:10px 0 0}
.rodape-aviso{border:1px solid #c9b37e59;border-radius:14px;padding:14px 16px;margin-top:20px}
.sec .rodape-aviso p{margin:0;font-size:14.5px;color:#fef5f0}
@media (min-width:820px){.moldura{max-width:none;flex:initial}.telas.quatro{grid-template-columns:repeat(4,1fr)}}
"""
BASE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
CTA1 = "QUERO COMEÇAR MEU PROJETO"
CTA2 = "QUERO ME INSCREVER AGORA"
AVISO = ("O valor corresponde ao acesso ao produto digital. Não garante parceria nem investimento: "
         "a Zion avalia cada ideia, cada região e cada terreno, e qualquer possibilidade de parceria ou investimento depende dessa análise e aprovação.")


def e(t):
    return escape(t, quote=False)


def btn(t):
    return f'<a href="#pagar" data-cx-cta class="btn">{t}</a>'


def sec(kind, tone, inner, sid=None, extra=""):
    i = f' id="{sid}"' if sid else ""
    return f'<section data-cx-section="{kind}"{i} class="sec {tone}{extra}"><div class="w">{inner}</div></section>'


def lista(itens):
    return '<ul class="lista">' + "".join(f"<li>{e(x)}</li>" for x in itens) + "</ul>"


B = []
B.append(f'<div class="escuro"><div class="w topo"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion Hotel Group International" width="170" height="34"></div></div>')

# 1 Hero
B.append(sec("hero", "escuro",
    '<p class="k">Zion Collection</p>'
    '<h1>Você tem o terreno.<br><em>Nós podemos ser o seu parceiro.</em></h1>'
    '<p class="sub">Aprenda o passo a passo de como estruturar seu empreendimento turístico e prepare seu projeto para possíveis parcerias e investimentos através da Zion.</p>'
    f'<img class="foto aerea" src="{BASE}zion-collection/club/fotos/bolha-aerea.jpg" alt="Vista aérea de uma unidade da Zion Bubble Glamping" width="730" height="981">'
    '<p class="leg">Foto real: Zion Bubble Glamping.</p>'
    '<div class="centro"><p class="selo">R$ 47 · acesso à plataforma · pagamento único</p></div>'
    + btn(CTA1), sid="hero"))

# 2 Identificação
B.append(sec("problem", "creme",
    '<p class="k">Você se identifica?</p>'
    '<h2>Talvez você já tenha pensado nisso.</h2>'
    + lista([
        "Você tem um terreno e não sabe como desenvolvê-lo?",
        "Você não tem capital suficiente para começar?",
        "Você não sabe como encontrar um sócio?",
        "Você não sabe como apresentar o seu projeto a investidores?",
    ]) +
    '<p>Se alguma resposta é sim, o primeiro passo não é construir. É organizar.</p>'))

# 3 Solução
B.append(sec("solution", "escuro",
    '<p class="k">A solução</p>'
    '<h2>Você não precisa começar construindo. Precisa começar estruturando.</h2>'
    '<p>A Zion Collection é uma plataforma de estruturação de projetos de hospedagem e imobiliário turístico. Você aprende a metodologia Zion, passo a passo, e aplica no seu próprio terreno: território, mercado, produto, modelo de negócio, implantação, pré-viabilidade e capital.</p>'
    '<p>Com o projeto organizado, você tem o que mostrar. E, depois da análise da Zion, existe a possibilidade de avançar para uma conversa de parceria.</p>'))

# 4 Produto tangível
TELAS = [("aula", "Aula interativa do Marco Zero"), ("mapa", "Mapa de direcionamento da jornada"),
         ("previab", "Ficha de pré-viabilidade"), ("raiox", "Ferramenta de leitura do terreno")]
telas = "".join(
    f'<figure class="moldura"><div class="celular"><img src="{BASE}zion-collection/club/telas/{n}.jpg" alt="{e(l)} (tela real da plataforma)" width="640" height="1280" loading="lazy"></div>'
    f'<p class="real">Tela real</p><p>{e(l)}</p></figure>' for n, l in TELAS)
B.append(sec("offer", "escuro",
    '<p class="k">O que você recebe</p>'
    '<h2>Veja a plataforma por dentro.</h2>'
    f'<video class="video" controls playsinline preload="none" poster="{BASE}zion-collection/club/video/poster.jpg" src="{BASE}zion-collection/club/video/plataforma-v02.mp4">O seu navegador não reproduz este vídeo.</video>'
    '<p class="leg">Vídeo de demonstração da plataforma Zion Collection (8 minutos).</p>'
    f'<div class="telas quatro">{telas}</div>'
    + lista([
        "9 módulos e 70 aulas: Comece aqui, Marco Zero e os sete pilares (território, mercado, produto, modelo de negócio, masterplan, pré-viabilidade e capital)",
        "Fichas guiadas e ferramentas para aplicar no seu projeto",
        "Planilhas de orçamento e de viabilidade",
        "Construção progressiva do seu Dossiê de Desenvolvimento",
        "Cadastro do seu terreno no banco de áreas da Zion",
    ])))

# 5 Jornada
J = ["Inscreva-se", "Receba seu acesso", "Aprenda", "Estruture seu projeto",
     "Apresente sua proposta à Zion"]
B.append(sec("solution", "creme",
    '<p class="k">A jornada</p>'
    '<h2>Do terreno à proposta, em cinco passos.</h2>'
    '<ol class="jornada">' + "".join(f"<li>{e(x)}</li>" for x in J) + '</ol>'
    '<p class="nota">Depois da proposta, existe a possibilidade de avançar para parcerias e investimentos, conforme análise e aprovação da Zion.</p>'
    + btn(CTA2)))

# 6 Autoridade
B.append(sec("social-proof", "escuro",
    '<p class="k">Quem está por trás</p>'
    '<h2>Experiência de quem opera hospedagem.</h2>'
    f'<img class="foto" src="{BASE}zion-collection/club/fotos/bolha-interior.jpg" alt="Interior de uma unidade da Zion Bubble Glamping" width="1000" height="1250" style="aspect-ratio:4/5;max-width:420px;margin-left:auto;margin-right:auto" loading="lazy">'
    '<p class="leg" style="text-align:center">Foto real: interior da Zion Bubble Glamping.</p>'
    '<p>A Zion opera a Zion Bubble Glamping em Urubici e em Florianópolis. A metodologia da plataforma vem dessa rotina de operar hospedagem.</p>'))

# 7 Oferta final
B.append(sec("cta", "escuro",
    '<p class="k">Zion Collection Club | Acesso à plataforma</p>'
    '<h2>Comece o seu projeto agora</h2>'
    '<div class="resumo"><div class="preco">R$ 47</div><div>Pagamento único · sem mensalidade</div></div>'
    + lista([
        "Acesso individual à plataforma: aulas, fichas, ferramentas, planilhas e o seu Dossiê",
        "Acesso por 12 meses",
        "Pagamento por Pix ou cartão",
        "O acesso chega no e-mail da compra assim que o pagamento é confirmado",
        "Suporte pelo WhatsApp +55 48 6137-1061",
        "Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor",
    ]) +
    f'<div class="rodape-aviso"><p>{e(AVISO)}</p></div>'
    '<div class="pagar"><div data-cx-checkout></div></div>', sid="pagar"))

# FAQ
FAQ = [
    ("Preciso ter capital para começar?", "Não. A plataforma serve para organizar o projeto antes de buscar capital."),
    ("Preciso ter um projeto pronto?", "Não. Você começa do Marco Zero."),
    ("O que estou comprando?", "O acesso à plataforma, com aulas, fichas, ferramentas, planilhas e a construção do seu dossiê. Não inclui reunião individual."),
    ("A Zion garante parceria ou investimento?", "Não. " + AVISO),
    ("Por quanto tempo tenho acesso?", "Por 12 meses."),
    ("E se eu não gostar?", "Você pode pedir reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor."),
]
faq = "".join(f'<div><div class="cm-accordion-header">{e(q)}</div><div class="cm-accordion-content">{e(a)}</div></div>' for q, a in FAQ)
B.append(sec("faq", "creme", '<p class="k">Perguntas frequentes</p><h2>Clareza para começar</h2>'
             f'<div style="margin-top:20px">{faq}</div>', extra=" faq"))
B.append('<footer><div class="w"><p>Zion Hotel Group International · Conteúdo educacional. Resultados dependem do contexto e da execução. '
         f'{e(AVISO)}</p><p>Suporte: WhatsApp +55 48 6137-1061</p></div></footer>')

HTML = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Zion Collection | Parceiro Zion</title>
<meta name="description" content="Aprenda o passo a passo para estruturar o seu empreendimento turístico e prepare o seu projeto. R$ 47, pagamento único.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
{"".join(B)}
</body>
</html>
"""
out = AQUI / "index.html"
out.write_text(HTML, encoding="utf-8")
print(out, len(HTML), "bytes; <span>:", HTML.count("<span"))

#!/usr/bin/env python3
"""Landing /mini-mentoria · Mini Mentoria de Estruturação (R$ 47) · oferta 0c71eeba-2654-432c-9701-0a31e6113a08 (produto cbbb5fb1-550f-4a8d-b269-5122c17b7780).
Reaproveita o CSS de club-97/landing/build.py e os extras de lt47/build.py. Uso: python3 -I build.py"""
from html import escape
from pathlib import Path
import re, sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build_bloco import bloco, CSS as BCSS

AQUI = Path(__file__).parent
C97 = AQUI.parents[1]
CSS = re.search(r'CSS = """(.*?)"""', (C97 / "landing" / "build.py").read_text(encoding="utf-8"), re.S).group(1)
CSS += re.search(r'CSS \+= """(.*?)"""', (C97 / "lt47" / "build.py").read_text(encoding="utf-8"), re.S).group(1)
CSS += BCSS
CSS += """
.sec h2 em,.sec h1 em{font-style:italic}
.sec.hero{background:#1B2117;padding:0}
section#hero.hero{padding-bottom:0}
.hero .htop{padding:26px 20px 18px}
.hero .htop h1{margin:8px 0 0}
.hero .hfoto{background:#1B2117;padding:0}
.hero .hfoto img{display:block;width:100%;height:auto;max-width:520px;margin:0 auto;border:0;border-radius:0;box-shadow:none;filter:none;opacity:1}
.hero .hleg{margin:0;padding:8px 20px 0;text-align:center;font-size:11.5px;color:#ded6bf;opacity:1}
.hero .hbot{padding:6px 20px 34px}
.sec.hero p.sub{font-size:20px;margin-top:14px}
.sec.hero p.selo{background:#1B2117;margin-top:14px}
@media(min-width:760px){.sec.hero .htop{padding:48px 20px 22px}.sec.hero p.sub{font-size:25px}.hero .hbot{padding:10px 20px 56px}}
.barra{display:none}
@media(max-width:760px){
.barra{display:flex;align-items:center;justify-content:space-between;gap:12px;position:fixed;left:0;right:0;bottom:0;z-index:50;background:#1B2117;border-top:2px solid #C9B37E;padding:10px max(16px,env(safe-area-inset-right,0px)) calc(10px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px));transform:translateY(110%);visibility:hidden;transition:transform .25s ease,visibility .25s}
.barra.on{transform:none;visibility:visible}
.barra .btn{flex:1 1 auto;margin:0;padding:13px 10px;font-size:13.5px;line-height:1.2;text-align:center;white-space:normal}
.barra .bp{flex:0 0 auto;margin:0;font-family:Jost,sans-serif;font-size:11.5px;line-height:1.3;color:#DED6BF;text-align:right}
.barra .bp b{display:block;font-size:15px;color:#FEF5F0;font-weight:600}
body{padding-bottom:calc(88px + env(safe-area-inset-bottom,0px))}
}
"""
BASE ="https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
CTA = "QUERO TRANSFORMAR MEU TERRENO"
AVISO = ("O valor corresponde ao acesso ao conteúdo digital. Não garante parceria nem investimento: "
         "a Zion avalia cada caso, e qualquer possibilidade de parceria ou investimento depende dessa análise.")


def e(t):
    return escape(t, quote=False)


def btn():
    return f'<a href="#pagar" data-cx-cta class="btn">{CTA}</a>'


def sec(kind, tone, inner, sid=None, extra=""):
    i = f' id="{sid}"' if sid else ""
    return f'<section data-cx-section="{kind}"{i} class="sec {tone}{extra}"><div class="w">{inner}</div></section>'


def lista(itens):
    return '<ul class="lista">' + "".join(f"<li>{e(x)}</li>" for x in itens) + "</ul>"


B = []
B.append(f'<div class="escuro"><div class="w topo"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion Hotel Group International" width="170" height="34"></div></div>')

# Hero com foto real da bolha (decisão de Bruno, 25/11)
HERO_IMG = (f'<img src="{BASE}zion-collection/club/fotos/bolha-aerea.jpg" alt="Bolha da Zion Bubble Glamping vista de cima" width="730" height="981" fetchpriority="high">')
HERO_TOP = ('<p class="k">Mini Mentoria de Estruturação · formação digital</p>'
    '<h1>Transforme seu terreno em um <em>destino turístico.</em></h1>')
HERO_BOT = ('<p class="sub">Aprenda o passo a passo para estruturar seu empreendimento e preparar seu projeto para possíveis parcerias e investimentos.</p>'
    '<div class="centro"><p class="selo">R$ 47 · pagamento único · acesso por 12 meses</p></div>' + btn())
B.append(f'<section data-cx-section="hero" id="hero" class="sec escuro hero"><div class="w htop">{HERO_TOP}</div>'
         f'<div class="hfoto">{HERO_IMG}</div><p class="hleg">Foto real: Zion Bubble Glamping</p>'
         f'<div class="w hbot">{HERO_BOT}</div></section>')

# Dor, capital, conhecimento
B.append(sec("problem", "creme",
    '<p class="k">Você se identifica?</p>'
    '<h2>Ter o terreno é o começo. Saber o que fazer com ele é o desafio.</h2>'
    '<p><strong>A dor do proprietário.</strong> O terreno está parado. Você imagina algo ali, mas não sabe por onde começar nem como transformar a ideia em projeto.</p>'
    '<p><strong>Falta de capital.</strong> Sem dinheiro para construir tudo, muita gente desiste antes de organizar o que já poderia mostrar a alguém.</p>'
    '<p><strong>Falta de conhecimento.</strong> Território, mercado, produto, modelo de negócio, custo e capital parecem assuntos separados. Sem método, o projeto fica solto.</p>'
    '<p>O primeiro passo não é construir. É estruturar.</p>'))

# Metodologia
PIL = ["Território e destino", "Mercado e demanda", "Produto e tipologias", "Modelo de negócio",
       "Masterplan faseado", "Pré-viabilidade", "Capital e Dossiê"]
B.append(sec("solution", "escuro",
    '<p class="k">A metodologia Zion</p>'
    '<h2>Marco Zero e sete pilares.</h2>'
    '<p>Você começa pelo Marco Zero, a visão de toda a jornada, e segue por sete pilares, na ordem, aplicando cada um no seu próprio terreno.</p>'
    '<ol class="jornada">' + "".join(f"<li>{e(x)}</li>" for x in PIL) + '</ol>'
    '<p class="nota">Método educativo. Cada ficha organiza as informações do seu projeto; ela não entrega nota nem veredito.</p>'))

# A Mini Mentoria + conteúdos + demonstração
TELAS = [("aula", "Aula interativa do Marco Zero"), ("mapa", "Mapa de direcionamento da jornada"),
         ("diagnostico", "Faça agora: diagnóstico prévio"), ("previab", "Faça agora: pré-viabilidade")]
telas = "".join(
    f'<figure class="moldura"><div class="celular"><img src="{BASE}zion-collection/club/telas/{n}.jpg" alt="{e(l)} (tela real da plataforma)" width="640" height="1280" loading="lazy"></div>'
    f'<p class="real">Tela real</p><p>{e(l)}</p></figure>' for n, l in TELAS)
B.append(sec("offer", "escuro",
    '<p class="k">A Mini Mentoria</p>'
    '<h2>Uma formação digital, no seu ritmo.</h2>'
    '<p>A Mini Mentoria de Estruturação é uma formação digital: você assiste, preenche e aplica sozinho, quando quiser. Não há acompanhamento individual nem reunião.</p>'
    '<p>9 módulos e 70 aulas e materiais, com acesso por 12 meses. Veja abaixo a plataforma por dentro e, logo depois, o que você recebe em cada pilar.</p>'
    '<h2 style="margin-top:34px">Veja a plataforma por dentro.</h2>'
    f'<video class="video" controls playsinline preload="none" poster="{BASE}zion-collection/club/video/poster.jpg" src="{BASE}zion-collection/club/video/plataforma-v02.mp4">O seu navegador não reproduz este vídeo.</video>'
    '<p class="leg">Vídeo de demonstração da plataforma Zion Collection (8 minutos).</p>'
    f'<div class="telas quatro">{telas}</div>'
    + btn()))

# Entregáveis pilar a pilar
B.append(bloco(css=False))

# Dossiê, cadastro, parceria
B.append(sec("solution", "creme",
    '<p class="k">Do projeto ao Dossiê</p>'
    '<h2>Cada ficha vira uma página do seu Dossiê.</h2>'
    '<p>Ao preencher as fichas, você monta, página por página, o seu Dossiê de Desenvolvimento. No final, gera o PDF para guardar e apresentar.</p>'
    '<p class="k" style="margin-top:28px">Cadastro do terreno (opcional)</p>'
    '<p>Se quiser, você pode cadastrar o seu terreno no banco de áreas da Zion. A Zion avalia cada caso, e o cadastro não garante parceria.</p>'
    '<p class="k" style="margin-top:28px">Possibilidade de parceria</p>'
    '<p>Com o projeto organizado, existe a possibilidade de a Zion avaliar uma conversa de parceria. É uma possibilidade, sujeita à análise de cada caso, e não uma garantia.</p>'))

# Origem do método (única foto de hospedagem)
B.append(sec("social-proof", "escuro",
    '<p class="k">De onde vem o método</p>'
    '<h2>Experiência de quem opera hospedagem.</h2>'
    f'<img class="foto" src="{BASE}zion-collection/club/fotos/bolha-interior.jpg" alt="Interior de uma unidade da Zion Bubble Glamping" width="1000" height="1250" style="aspect-ratio:4/5;max-width:420px;margin-left:auto;margin-right:auto" loading="lazy">'
    '<p class="leg" style="text-align:center">Foto real: interior da Zion Bubble Glamping, de onde vem a rotina que inspira o método.</p>'
    '<p>A Zion opera a Zion Bubble Glamping em Urubici e em Florianópolis. O método da formação parte dessa rotina de operar hospedagem.</p>'))

# Oferta
B.append(sec("cta", "escuro",
    '<p class="k">Mini Mentoria de Estruturação</p>'
    '<h2>Comece a estruturar o seu terreno</h2>'
    '<div class="resumo"><div class="preco">R$ 47</div><div>Pagamento único · sem mensalidade</div></div>'
    + lista([
        "Formação digital: aulas gravadas, fichas, e-books, planilhas e kits",
        "Acesso por 12 meses",
        "Pagamento por Pix ou cartão",
        "O acesso chega no e-mail da compra assim que o pagamento é confirmado",
        "Suporte pelo WhatsApp +55 48 6137-1061",
        "Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor",
    ]) +
    f'<div class="rodape-aviso"><p>{e(AVISO)}</p></div>'
    '<div class="pagar"><div data-cx-checkout></div></div>', sid="pagar"))

FAQ = [
    ("Preciso ter capital para começar?", "Não. A formação serve para organizar o projeto antes de buscar capital."),
    ("Preciso ter um projeto pronto?", "Não. Você começa do Marco Zero."),
    ("O que estou comprando?", "Uma formação digital, com aulas gravadas, fichas e formulários interativos, e-books, planilhas e kits. Não inclui acompanhamento individual nem reunião."),
    ("A Zion garante parceria ou investimento?", "Não. " + AVISO),
    ("Por quanto tempo tenho acesso?", "Por 12 meses."),
    ("E se eu não gostar?", "Você pode pedir reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor."),
]
faq = "".join(f'<div><div class="cm-accordion-header">{e(q)}</div><div class="cm-accordion-content">{e(a)}</div></div>' for q, a in FAQ)
B.append(sec("faq", "creme", '<p class="k">Perguntas frequentes</p><h2>Clareza para começar</h2>'
             f'<div style="margin-top:20px">{faq}</div>', extra=" faq"))
BARRA = ('<div class="barra" id="barra" aria-hidden="true">' + btn().replace('class="btn"','class="btn" tabindex="-1"') +
    '<p class="bp"><b>R$ 47</b>pagamento único</p></div>')
B.append('<footer><div class="w"><p>Zion Hotel Group International · Conteúdo educacional. Resultados dependem do contexto e da execução. '
         f'{e(AVISO)}</p><p>Suporte: WhatsApp +55 48 6137-1061</p></div></footer>')

HTML = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mini Mentoria de Estruturação | Zion Collection</title>
<meta name="description" content="Transforme seu terreno em um destino turístico. Aprenda o passo a passo para estruturar seu empreendimento. Formação digital, R$ 47, pagamento único.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
{"".join(B)}
{BARRA}
<script>
(function(){{var b=document.getElementById("barra"),h=document.getElementById("hero"),p=document.getElementById("pagar");
if(!b||!h||!p||!window.IntersectionObserver)return;
var hv=true,pv=false;
function u(){{var on=!hv&&!pv;b.classList.toggle("on",on);b.setAttribute("aria-hidden",on?"false":"true");var a=b.querySelector("a");if(a)a.tabIndex=on?0:-1}}
new IntersectionObserver(function(e){{hv=e[0].isIntersecting;u()}}).observe(h);
new IntersectionObserver(function(e){{pv=e[0].isIntersecting;u()}},{{threshold:0.05}}).observe(p);
}})();
</script>
</body>
</html>
"""
out = AQUI / "index.html"
out.write_text(HTML, encoding="utf-8")
print(out, len(HTML), "bytes; <span>:", HTML.count("<span"))

#!/usr/bin/env python3
"""Gera index.html da página de R$ 97 (Zion Collection Club · Acesso à plataforma).

Parte do esqueleto e do estilo da página de pagamento /inscricao (R$ 270),
guardada em inscricao-atual-270.html / inscricao-atual-270.css.
Uso: python3 -I build.py
"""
from html import escape
from pathlib import Path

BASE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
BTN = "FAÇA A SUA INSCRIÇÃO"
AVAL1 = "Avaliamos cada ideia, cada região e cada terreno: o potencial de cada um, a infraestrutura que já existe e o que ainda precisa ser investido."
AVAL2 = "Parcerias e investimentos dependem dessa avaliação."

# CSS da página /inscricao (mesmas classes), mais o que os blocos novos pedem.
CSS = """
*{box-sizing:border-box}html{scroll-behavior:smooth}
html body{color:#fef5f0;background:#0d1512;margin:0;font-family:'Jost',sans-serif;font-size:16.5px;font-weight:300;line-height:1.65}
.w{max-width:760px;margin:0 auto;padding:0 20px}
.sec{padding:52px 0}
.escuro{color:#fef5f0;background:#0d1512;font-family:'Jost',sans-serif}
.creme{color:#1b2117;background:#fef5f0;font-family:'Jost',sans-serif}
h1,h2,h3{margin:0;font-family:'Cormorant Garamond',serif;font-weight:500;line-height:1.08;font-variant-numeric:lining-nums}
h1{font-size:40px}h2{font-size:35px}h3{font-size:25px;font-weight:600;line-height:1.1}
.sec p,.sec li,footer p{font-family:'Jost',sans-serif;font-weight:300;line-height:1.65}
.sec p{margin:14px 0 0}
.escuro p,.escuro li{color:#fef5f0}
.creme p,.creme li{color:#1b2117}
.escuro h1,.escuro h2,.escuro h3{color:#fef5f0!important}
.creme h1,.creme h2,.creme h3{color:#1b2117!important}
h1 em{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:500;color:#c9b37e!important}
.sec p.k{letter-spacing:.18em;text-transform:uppercase;color:#c9b37e;margin:0 0 16px;font-size:11.5px;font-weight:400}
.creme p.k{color:#8b714e}
.sec p.nota{color:#ded6bf;margin-top:16px;font-size:13.5px}
.creme p.nota{color:#5b4a33}
.sec p.leg{color:#ded6bf;margin-top:8px;font-size:12.5px}
.creme p.leg{color:#5b4a33}
.topo{border-bottom:1px solid #c9b37e40;padding:20px 0}
.topo img{height:34px;width:auto;display:block}
.sec p.selo{display:inline-block;border:1px solid #c9b37e80;border-radius:999px;color:#c9b37e;font-size:13px;font-weight:400;letter-spacing:.04em;padding:7px 16px;margin-top:20px}
.foto{aspect-ratio:3/2;object-fit:cover;border-radius:14px;width:100%;height:auto;margin-top:22px;display:block}
.btn{color:#1b2117;text-align:center;background:#c9b37e;border-radius:999px;justify-content:center;align-items:center;min-height:54px;margin-top:24px;padding:12px 26px;font-size:15px;font-weight:500;letter-spacing:.05em;text-decoration:none;display:flex;font-family:'Jost',sans-serif!important}
.cards{gap:12px;margin-top:22px;display:grid}
.card{background:#fff;border:1px solid #8b714e4d;border-radius:14px;grid-template-columns:40px 1fr;gap:12px;padding:16px;display:grid}
.sec .card p{margin:4px 0 0;font-size:15.5px}
.card .n{color:#8b714e;font-family:'Cormorant Garamond',serif;font-size:40px;font-weight:500;line-height:.9;font-variant-numeric:lining-nums}
.lista{list-style:none;margin:22px 0 0;padding:0}
.lista li{border-top:1px solid #c9b37e40;padding:13px 0 13px 26px;position:relative}
.creme .lista li{border-top-color:#8b714e59}
.lista li:before{content:"";position:absolute;left:2px;top:24px;width:10px;height:1px;background:#c9b37e}
.creme .lista li:before{background:#8b714e}
.telas{display:flex;gap:14px;overflow-x:auto;margin-top:24px;padding-bottom:10px;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch}
.tela{flex:0 0 62%;max-width:250px;margin:0;scroll-snap-align:start}
.tela img{width:100%;height:auto;display:block;border-radius:14px;border:1px solid #c9b37e59}
.sec .tela p{font-size:13.5px;margin:8px 0 0}
.sec .tela p.real{color:#c9b37e;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;font-weight:400;margin:8px 0 0}
.capa{width:100%;height:auto;display:block;border-radius:14px;margin-top:22px;border:1px solid #c9b37e40}
.jornada{list-style:none;margin:24px 0 0;padding:0;display:grid;gap:0}
.jornada li{border-left:1px solid #c9b37e;padding:0 0 18px 18px;position:relative;font-family:'Cormorant Garamond',serif;font-size:24px;font-weight:500;line-height:1.15}
.escuro .jornada li{color:#fef5f0;font-family:'Cormorant Garamond',serif}
.jornada li:before{content:"";position:absolute;left:-5px;top:6px;width:9px;height:9px;border-radius:50%;background:#c9b37e}
.jornada li:last-child{padding-bottom:0;border-left-color:transparent}
.resumo{flex-wrap:wrap;align-items:baseline;gap:6px 14px;margin-top:18px;display:flex}
.preco{color:#fef5f0;font-family:'Cormorant Garamond',serif!important;font-size:62px;font-weight:500;line-height:1;font-variant-numeric:lining-nums}
.resumo div{color:#fef5f0;font-family:'Jost',sans-serif}
.pagar{color:#1b2117;background:#fef5f0;border-radius:14px;margin-top:22px;padding:14px;min-height:120px}
.sec p.frase{font-family:'Cormorant Garamond',serif;font-size:28px;font-weight:500;line-height:1.18;margin-top:22px}
.faq .cm-accordion-header{cursor:pointer;border-top:1px solid #8b714e59;padding:16px 0;font-family:'Cormorant Garamond',serif;font-size:24px;font-weight:600;line-height:1.2;color:#1b2117;font-variant-numeric:lining-nums}
.faq .cm-accordion-content{padding:0 0 16px;font-size:16px;color:#1b2117;font-family:'Jost',sans-serif}
footer{color:#ded6bf;background:#0d1512;padding:28px 0 50px;font-size:12.5px;font-family:'Jost',sans-serif}
footer p{color:#ded6bf;margin:0 0 8px}
#hero{padding-bottom:36px}
.video{display:block;width:100%;aspect-ratio:16/9;background:#000;border-radius:14px;margin-top:20px;border:1px solid #c9b37e59}
#hero h1{font-size:31px;line-height:1.1;letter-spacing:-.01em}
@media (min-width:360px){#hero h1{font-size:35px}}
@media (min-width:375px){#hero h1{font-size:37px}}
@media (min-width:390px){#hero h1{font-size:38px}}
@media (min-width:412px){#hero h1{font-size:41px}}
.sec p.sub{font-family:'Cormorant Garamond',serif;font-size:27px;font-weight:500;line-height:1.2;color:#fef5f0;margin-top:18px}
.sec p strong.d{display:block;color:#c9b37e;font-weight:500;font-size:17.5px;line-height:1.35;margin-bottom:8px}
.sec p.mini{text-align:center;font-size:14px;color:#fef5f0;margin:26px 0 0}
.sec p.mini.ouro{color:#c9b37e;margin-top:12px;font-weight:400;letter-spacing:.03em}
#hero .btn{margin-top:10px}
.centro{text-align:center}
#hero p.aval{text-align:center;color:#fef5f0;font-size:15.5px;line-height:1.55;margin-top:22px}
#hero p.nota{text-align:center;margin-top:8px}
#pagar{padding-top:44px}
.passos{display:grid;gap:10px;margin-top:18px}
.passo{border:1px solid #c9b37e59;border-radius:14px;padding:14px 16px;display:grid;grid-template-columns:30px 1fr;gap:10px;align-items:center}
.passo .n{color:#c9b37e;font-family:'Cormorant Garamond',serif;font-size:40px;font-weight:500;line-height:.9;font-variant-numeric:lining-nums}
.sec .passo p{margin:0;font-size:16px;line-height:1.35;color:#fef5f0}
.lista li strong.t{display:block;color:#c9b37e;font-weight:500;font-size:17px;line-height:1.35}
.sec p.frase.fecho{border-left:2px solid #c9b37e;padding-left:16px;margin-top:26px;color:#fef5f0}
.sec p.frase.ouro{color:#c9b37e;margin-top:20px;font-style:italic;font-size:30px}
@media (min-width:820px){
 .cards{grid-template-columns:1fr 1fr}
 h1{font-size:58px}h2{font-size:46px}.sec{padding:76px 0}
 #hero h1{font-size:62px}.sec p.sub{font-size:32px}
 #hero .btn{margin-left:auto;margin-right:auto}
 .telas{display:grid;grid-template-columns:repeat(3,1fr);overflow:visible}
 .tela{max-width:none}
 .jornada{grid-template-columns:repeat(3,1fr);gap:18px 14px}
 .passos{grid-template-columns:repeat(3,1fr)}
 .jornada li{border-left:0;border-top:1px solid #c9b37e;padding:14px 0 0}
 .jornada li:before{left:0;top:-5px}
 .btn{display:flex;width:fit-content;min-width:380px}
}
"""


def e(t):
    return escape(t, quote=False)


def btn():
    return f'<a href="#pagar" data-cx-cta class="btn">{BTN}</a>'


def sec(kind, tone, inner, sid=None, extra=""):
    i = f' id="{sid}"' if sid else ""
    return f'<section data-cx-section="{kind}"{i} class="sec {tone}{extra}"><div class="w">{inner}</div></section>'


def lista(itens):
    return '<ul class="lista">' + "".join(f"<li>{e(x)}</li>" for x in itens) + "</ul>"


TELAS = [
    ("aula", "Aula interativa do Marco Zero"),
    ("diagnostico", "Diagnóstico prévio do seu projeto"),
    ("mapa", "Mapa de direcionamento da jornada"),
    ("previab", "Ficha de pré-viabilidade"),
    ("raiox", "Ferramenta de leitura do terreno"),
    ("implantacao", "Ferramenta de custo de implantação"),
]

PILARES = [
    ("Território", "Compreenda as características, as possibilidades e as restrições da sua área."),
    ("Mercado", "Aprenda a investigar a demanda turística e o comportamento do mercado."),
    ("Produto", "Identifique quais modelos de hospedagem podem fazer sentido para o seu destino."),
    ("Modelo de negócio", "Organize a visão comercial, operacional e financeira do empreendimento."),
    ("Masterplan", "Estruture a visão preliminar de implantação do projeto."),
    ("Pré-viabilidade", "Organize estimativas de investimento, custos, receitas e possíveis retornos."),
    ("Capital", "Prepare o seu projeto para possíveis estratégias de captação, parcerias e investimentos."),
]

FAQ = [
    ("Preciso ter capital para começar?", "Não. A plataforma serve justamente para organizar o projeto antes de buscar capital."),
    ("Preciso ter um projeto pronto?", "Não. Você começa do Marco Zero."),
    ("Preciso ter experiência em hotelaria?", "Não. O conteúdo é passo a passo."),
    ("O que estou contratando?", "Acesso por 12 meses à plataforma, com aulas, fichas, ferramentas e a construção do seu dossiê. Não inclui reunião individual."),
    ("Como recebo o meu acesso?", "No e-mail da compra, assim que o pagamento é confirmado."),
    ("Por quanto tempo tenho acesso?", "12 meses."),
    ("Posso cadastrar o meu terreno no banco de áreas?", "Sim, pela ficha do terreno dentro da plataforma."),
    ("A Zion garante investimento no meu terreno?", "Não. Não existe garantia de parceria, investimento ou aprovação automática. " + AVAL1 + " " + AVAL2),
]

blocos = []

# Topo
blocos.append(
    f'<div class="escuro"><div class="w topo"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion Hotel Group International" width="170" height="34"></div></div>'
)

# B01 · Abertura
blocos.append(sec("hero", "escuro",
    '<p class="k">Zion Collection Club</p>'
    '<h1>Faça a sua inscrição.<br>Queremos te conhecer.<br>Seja um <em>parceiro Zion</em>.</h1>'
    '<p class="sub">Transforme o seu terreno em destino turístico com a nossa plataforma.</p>'
    '<p><strong class="d">Não tem capital? Não sabe por onde começar?</strong>'
    'A nossa plataforma ajuda a estruturar a sua ideia, para conhecermos o potencial do seu terreno e a visão das possibilidades. '
    'Isso abre a oportunidade de você ser nosso parceiro e receber investimentos na sua área.</p>'
    f'<video class="video" controls playsinline preload="metadata" poster="{BASE}zion-collection/club/video/poster.jpg" src="{BASE}zion-collection/club/video/plataforma-v02.mp4">O seu navegador não reproduz este vídeo.</video>'
    '<p class="leg">Vídeo: a plataforma Zion Collection por dentro (8 minutos).</p>'
    '<p class="mini">Faça a sua inscrição. Queremos te conhecer.</p>'
    + btn() +
    '<p class="mini ouro">Seja um parceiro Zion.</p>'
    '<div class="centro"><p class="selo">Acesso à plataforma · R$ 97 · Pagamento único</p></div>'
    f'<p class="aval">{AVAL1}</p>'
    f'<p class="nota">{AVAL2}</p>',
    sid="hero"))

# B02 + B06 · Por dentro (a galeria sobe para o lugar do vídeo, que ainda não existe)
telas = "".join(
    f'<figure class="tela"><img src="{BASE}zion-collection/club/telas/{n}.jpg" alt="{e(leg)} (tela real da plataforma)" width="640" height="1280" loading="lazy">'
    f'<p class="real">Tela real</p><p>{e(leg)}</p></figure>'
    for n, leg in TELAS)
blocos.append(sec("solution", "escuro",
    '<p class="k">Por dentro</p>'
    '<h2>Conheça a sua plataforma por dentro.</h2>'
    '<p>Veja como funciona a sua plataforma de estruturação.</p>'
    f'<div class="telas">{telas}</div>'))

# B03 · Colapso de crença
blocos.append(sec("problem", "creme",
    '<p class="k">Antes do capital</p>'
    '<h2>Se um investidor chegasse hoje, você estaria preparado?</h2>'
    + lista([
        "O que pode desenvolver no seu terreno?",
        "Qual produto o mercado está demandando?",
        "Quantas unidades poderiam ser implantadas?",
        "Quanto precisaria investir?",
        "Quanto poderia faturar?",
        "Qual seria o possível retorno?",
        "Como apresentaria o seu projeto a um investidor?",
    ]) +
    '<p>Antes de buscar capital, você precisa estruturar o seu empreendimento. Não espere a oportunidade chegar para começar a se preparar.</p>'))

# B04 · O que é
blocos.append(sec("solution", "escuro",
    '<p class="k">O que é</p>'
    '<h2>Você já tem o terreno. Nós temos o método.</h2>'
    '<p>A Zion Collection é uma plataforma de estruturação de projetos de hospedagem e imobiliário turístico. Ela ajuda proprietários de terrenos a compreender o potencial da área, investigar o mercado, definir possíveis produtos e montar uma visão preliminar do empreendimento.</p>'
    '<p>Você aprende o passo a passo e aplica direto no seu projeto. Não é só um curso para assistir: é uma plataforma para aprender, aplicar e estruturar.</p>'))

# B05 · Sete pilares
cards = "".join(
    f'<div class="card"><div class="n">{i}</div><div><h3>{e(t)}</h3><p>{e(d)}</p></div></div>'
    for i, (t, d) in enumerate(PILARES, 1))
blocos.append(sec("solution", "creme",
    '<p class="k">O método</p>'
    '<h2>Os sete pilares</h2>'
    f'<div class="cards">{cards}</div>'))

# B07 · O que você constrói na plataforma
PASSOS = ["Assista aos nossos vídeos", "Preencha os formulários", "Anexe o que você tem"]
CONSTROI = [
    ("A sua ideia", "o diagnóstico do Marco Zero"),
    ("O seu terreno", "território e infraestrutura que já existe"),
    ("O seu produto", "mercado, hospedagem e modelo de negócio"),
    ("O seu orçamento", "quanto custa abrir a primeira etapa"),
    ("A sua pré-viabilidade", "a conta do seu próprio caso"),
]
passos = "".join(
    f'<div class="passo"><div class="n">{i}</div><p>{e(t)}</p></div>'
    for i, t in enumerate(PASSOS, 1))
constroi = "".join(
    f'<li><strong class="t">{e(t)}</strong>{e(d)}</li>' for t, d in CONSTROI)
blocos.append(sec("offer", "escuro",
    '<p class="k">A plataforma é a sua ferramenta</p>'
    '<h2>O que você constrói na plataforma</h2>'
    '<p>Simples e guiado, como um tutorial:</p>'
    f'<div class="passos">{passos}</div>'
    f'<ol class="lista">{constroi}</ol>'
    '<p class="frase fecho">Cada formulário que você preenche gera uma página. Juntas, elas formam o seu Dossiê de Desenvolvimento.</p>'
    '<p class="frase ouro">Você constrói. A Zion conhece e avalia.</p>'
    '<p class="nota">Aulas, vídeos e e-books em cada pilar · 12 meses de acesso · cadastro do seu terreno no banco de áreas da Zion.</p>'
    + btn()))

# B08 · Dossiê
blocos.append(sec("solution", "creme",
    '<p class="k">O seu dossiê</p>'
    '<h2>Seu terreno. Seu projeto. Seu dossiê.</h2>'
    '<p>Cada etapa da plataforma organiza uma parte do seu empreendimento: território, mercado, produto, modelo de negócio, implantação, pré-viabilidade e capital.</p>'
    '<p>Ao preencher as fichas, você monta um documento que reúne a visão do seu projeto e prepara futuras conversas com possíveis parceiros e investidores.</p>'
    '<p class="nota">O dossiê não é projeto executivo nem garantia de viabilidade técnica.</p>'))

# B09 · Oportunidade Zion
jornada = "".join(f"<li>{e(x)}</li>" for x in [
    "Terreno", "Estruturação", "Dossiê", "Banco de áreas", "Análise", "Possíveis parcerias e investimentos"])
blocos.append(sec("solution", "escuro",
    '<p class="k">Oportunidade Zion</p>'
    '<h2>Abra a possibilidade de ser um parceiro Zion e receber investimentos na sua área.</h2>'
    '<p>A Zion está buscando novos destinos e novos parceiros no Brasil. Ao entrar para a plataforma, você cadastra o seu terreno no banco de áreas e começa a estruturar o seu projeto.</p>'
    '<p>Quanto mais organizado estiver o empreendimento, melhores as condições para apresentar a oportunidade.</p>'
    f'<ol class="jornada">{jornada}</ol>'
    f'<p class="nota">{AVAL1} {AVAL2}</p>'))

# B10 · Autoridade
blocos.append(sec("social-proof", "creme",
    '<p class="k">Quem está por trás</p>'
    '<h2>Conheça quem está por trás da Zion.</h2>'
    f'<img class="foto" src="{BASE}assets/bruno/bruno-bubble-urubici.webp" alt="Bruno Chaerk, fundador da Zion, em frente a uma unidade da Zion Bubble Glamping" width="1400" height="1050" loading="lazy">'
    '<p class="leg">Foto real: Bruno Chaerk na Zion Bubble Glamping.</p>'
    '<p>Bruno Chaerk, fundador, tem mais de 20 anos de hotelaria internacional. A Zion opera a Zion Bubble Glamping em Urubici e em Florianópolis.</p>'
    '<p class="nota">Notas dos hóspedes: Booking 9,6 · Airbnb Superhost</p>'))

# B11 · Fechamento
blocos.append(sec("problem", "escuro",
    '<p class="k">O primeiro passo</p>'
    '<h2>Há quanto tempo você pensa em desenvolver o seu terreno?</h2>'
    '<p>Talvez você esteja esperando aparecer um sócio, um parceiro ou um investidor. Não espere a oportunidade chegar para começar a se preparar.</p>'
    + lista([
        "Acesse a plataforma.",
        "Aprenda o passo a passo.",
        "Estruture o seu projeto.",
        "Construa o seu dossiê.",
        "Cadastre a sua área.",
    ]) +
    '<p class="frase">Você já tem o terreno. Nós temos o método.</p>'
    '<p class="selo">Acesso à plataforma Zion Collection · R$ 97 · Pagamento único</p>'
    + btn()))

# B12 · Checkout
blocos.append(sec("cta", "escuro",
    '<p class="k">Zion Collection Club | Acesso à plataforma</p>'
    '<h2>Comece agora</h2>'
    '<div class="resumo"><div class="preco">R$ 97</div><div>Pagamento único · sem mensalidade</div></div>'
    + lista([
        "Pagamento por Pix ou cartão",
        "12 meses de acesso",
        "O acesso chega no e-mail da compra assim que o pagamento é confirmado",
        "Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor",
    ]) +
    '<div class="pagar"><div data-cx-checkout></div></div>',
    sid="pagar"))

# B13 · Perguntas
faq = "".join(
    f'<div><div class="cm-accordion-header">{e(q)}</div><div class="cm-accordion-content">{e(a)}</div></div>'
    for q, a in FAQ)
blocos.append(sec("faq", "creme",
    '<p class="k">Perguntas frequentes</p>'
    '<h2>Clareza para começar</h2>'
    f'<div style="margin-top:20px">{faq}</div>', extra=" faq"))

blocos.append(
    '<footer><div class="w"><p>Zion Hotel Group International · Conteúdo educacional. Resultados dependem do contexto e da execução. '
    f'{AVAL1} {AVAL2}</p>'
    '<p>Suporte: WhatsApp +55 48 6137-1061</p></div></footer>')

HTML = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Zion Collection Club | Acesso à plataforma</title>
<meta name="description" content="Acesse a plataforma Zion Collection e aprenda o passo a passo para estruturar o projeto de hospedagem do seu terreno. R$ 97, pagamento único.">
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
print(out, len(HTML), "bytes; <span>:", HTML.count("<span"))

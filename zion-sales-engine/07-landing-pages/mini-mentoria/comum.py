#!/usr/bin/env python3
"""Gerador comum das variantes A e B da landing /mini-mentoria (Fase 03, ZION CONVERSION).
Oferta 0c71eeba-2654-432c-9701-0a31e6113a08 (R$ 47). Reaproveita CSS e bloco de entregáveis de
producao/zion-collection/club-97/mini-mentoria/. Estrutura ECROI: Espelhamento, Colapso de Crença,
Reconhecimento, Orientação, Implementação; depois oferta, entregáveis, preço e CTA.
Sem <script>, sem <span>, sem base64. Uso: python3 -I variante-a/build.py  (ou variante-b/build.py)"""
from html import escape
from pathlib import Path
import re, sys

RAIZ = Path(__file__).resolve().parents[3]
MM = RAIZ / "producao/zion-collection/club-97/mini-mentoria"
C97 = MM.parent
sys.path.insert(0, str(MM))
import build_bloco as bb  # noqa: E402

CSS = re.search(r'CSS = """(.*?)"""', (C97 / "landing/build.py").read_text(encoding="utf-8"), re.S).group(1)
CSS += re.search(r'CSS \+= """(.*?)"""', (C97 / "lt47/build.py").read_text(encoding="utf-8"), re.S).group(1)
CSS += bb.CSS
# trecho extra do molde atual (hero com foto nítida, barra fixa só com CSS)
CSS += re.search(r'CSS \+= """\n\.sec h2 em(.*?)"""', (MM / "landing/build.py").read_text(encoding="utf-8"), re.S).group(0)[len('CSS += """\n'):-3]
CSS += """
.aviso-rolar{margin:14px 0 0;font-family:Jost,sans-serif;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#C9B37E;text-align:center}
.passos{list-style:none;margin:18px 0 0;padding:0;counter-reset:p}
.passos li{counter-increment:p;position:relative;margin:0 0 10px;padding:12px 14px 12px 54px;background:#1B2117;border:1px solid #c9b37e55;border-radius:12px;color:#FEF5F0;font-family:Jost,sans-serif;font-size:16px;line-height:1.4}
.passos li::before{content:counter(p);position:absolute;left:14px;top:50%;transform:translateY(-50%);width:28px;height:28px;border-radius:50%;background:#C9B37E;color:#040605;font-weight:600;text-align:center;line-height:28px;font-size:15px}
.passos li b{color:#C9B37E;font-weight:500}
.sec.creme .passos li{background:#040605}
"""

BASE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
PRECO_CTA = "QUERO ACESSAR A MINI MENTORIA POR R$47"
AVISO = ("O valor corresponde ao acesso ao conteúdo digital. Não garante parceria nem investimento: "
         "a Zion avalia cada caso, e qualquer possibilidade de parceria ou investimento depende dessa análise.")
PIL = ["Território e destino", "Mercado e demanda", "Produto e tipologias", "Modelo de negócio",
       "Masterplan faseado", "Pré-viabilidade", "Capital e Dossiê"]


def e(t):
    return escape(t, quote=False)


def btn(extra=""):
    return f'<a href="#pagar" data-cx-cta class="btn"{extra}>{PRECO_CTA}</a>'


def sec(kind, tone, inner, sid=None, extra=""):
    i = f' id="{sid}"' if sid else ""
    return f'<section data-cx-section="{kind}"{i} class="sec {tone}{extra}"><div class="w">{inner}</div></section>'


def lista(itens):
    return '<ul class="lista">' + "".join(f"<li>{e(x)}</li>" for x in itens) + "</ul>"


def entregaveis():
    body = (
        '<section data-cx-section="solution" id="entregaveis" class="sec ent-sec"><div class="w">'
        '<p class="ent-k">O que você recebe</p>'
        '<h2 class="ent-h">O que você recebe em cada etapa.</h2>'
        '<p class="ent-intro">Em cada etapa você assiste, preenche uma ficha e monta uma página do seu Dossiê.</p>'
        '<div class="ent-lista">' + "".join(bb.card(c) for c in bb.CARDS) + '</div>'
        '<div class="ent-fim"><p class="ent-fk">No final você tem</p>'
        '<p class="ent-fp"><b>O seu Dossiê completo (PDF)</b>, para guardar e apresentar o seu projeto.</p>'
        '<p class="ent-opc"><b>Opcional:</b> cadastre seu terreno no banco de áreas da Zion (a Zion avalia cada caso; sem garantia de parceria ou investimento).</p></div>'
        '<p class="ent-nota">Material educativo. O resultado depende do que você preencher.</p>'
        '</div></section>')
    return body


def build(variante, saida):
    A = variante == "A"
    B = []
    B.append(f'<div class="escuro"><div class="w topo"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion Hotel Group International" width="170" height="34"></div></div>')

    # ---- HERO (E: espelhamento começa já no topo)
    hero_top = ('<p class="k">Mini Mentoria de Estruturação · formação digital</p>'
                '<h1>Seu terreno está parado. <em>O que falta é um projeto.</em></h1>')
    hero_bot = ('<p class="sub">Aprenda o passo a passo para estruturar o seu empreendimento e montar o Dossiê do seu projeto.</p>')
    if A:
        hero_bot += ('<div class="centro"><p class="selo">R$ 47 · pagamento único · acesso por 12 meses</p></div>' + btn())
    else:
        hero_bot += ('<div class="centro"><p class="selo">Formação digital · acesso por 12 meses</p></div>'
                     '<p class="aviso-rolar">Role para ver como funciona e o que você recebe</p>')
    hero_img = (f'<img src="{BASE}zion-collection/club/fotos/bolha-aerea.jpg" alt="Bolha da Zion Bubble Glamping vista de cima" width="730" height="981" fetchpriority="high">')
    B.append(f'<section data-cx-section="hero" id="hero" class="sec escuro hero"><div class="w htop">{hero_top}</div>'
             f'<div class="hfoto">{hero_img}</div><p class="hleg">Foto real: Zion Bubble Glamping</p>'
             f'<div class="w hbot">{hero_bot}</div></section>')

    # ---- E Espelhamento
    B.append(sec("problem", "creme",
        '<p class="k">Você se identifica?</p>'
        '<h2>Você tem o terreno. Mas não sabe por onde começar.</h2>'
        '<p>Você olha para a área e imagina algo ali: hospedagem, experiência, um destino. Só que a ideia continua na cabeça, solta, sem número, sem desenho e sem ordem.</p>'
        '<p>Você pesquisa, pergunta, adia. E o terreno segue parado, enquanto o tempo passa e a dúvida cresce.</p>'
        '<p>Se isso soa familiar, você não está sozinho: é a situação de muita gente que tem terra e ainda não tem projeto.</p>'))

    # ---- C Colapso de Crença
    B.append(sec("problem", "escuro",
        '<p class="k">A ideia que trava</p>'
        '<h2>&ldquo;Preciso ter todo o capital antes de começar.&rdquo;</h2>'
        '<p>É a frase que mais faz o proprietário esperar. Mas capital é o <strong>último</strong> passo da conta, não o primeiro.</p>'
        '<p>Antes de qualquer obra ou captação, existe um trabalho que não exige construir nada: entender o território, o mercado e o produto, escolher o modelo, desenhar o masterplan e fazer a conta.</p>'
        '<p>Esse trabalho se faz no papel, com método. É isso que você aprende na formação.</p>'))

    # ---- R Reconhecimento
    B.append(sec("problem", "creme",
        '<p class="k">O verdadeiro problema</p>'
        '<h2>Não é falta de sorte. É terreno sem projeto estruturado.</h2>'
        '<p>Terreno e capital parecem assuntos separados, mas o que liga os dois é o projeto. Sem território, mercado, produto, modelo, masterplan e pré-viabilidade organizados, não há o que mostrar nem decidir.</p>'
        '<p>Com o projeto estruturado, você passa a saber se avança, se ajusta ou se para, com informação na mão.</p>'
        '<p>O primeiro passo não é construir. É estruturar.</p>'))

    # ---- O Orientação
    B.append(sec("solution", "escuro",
        '<p class="k">O método Zion</p>'
        '<h2>Marco Zero e sete pilares.</h2>'
        '<p>Aprenda o passo a passo: você começa pelo Marco Zero, a visão de toda a jornada, e segue por sete pilares, na ordem, aplicando cada um no seu próprio terreno.</p>'
        '<ol class="jornada">' + "".join(f"<li>{e(x)}</li>" for x in PIL) + '</ol>'
        '<p class="nota">Método educativo. Cada ficha organiza as informações do seu projeto; ela não entrega nota nem veredito.</p>'))

    # ---- I Implementação (como aplica pela plataforma) + demonstração real
    telas_def = [("aula", "Aula interativa do Marco Zero"),
                 ("diagnostico", "Faça agora: diagnóstico prévio"), ("previab", "Faça agora: pré-viabilidade")]
    telas = "".join(
        f'<figure class="moldura"><div class="celular"><img src="{BASE}zion-collection/club/telas/{n}.jpg" alt="{e(l)} (tela real da plataforma)" width="640" height="1280" loading="lazy"></div>'
        f'<p class="real">Tela real</p><p>{e(l)}</p></figure>' for n, l in telas_def)
    B.append(sec("solution", "creme",
        '<p class="k">Como você aplica</p>'
        '<h2>Na plataforma, em quatro passos por etapa.</h2>'
        '<ol class="passos">'
        '<li><b>Assista</b> às aulas gravadas da etapa.</li>'
        '<li><b>Preencha a ficha</b> &ldquo;Faça agora&rdquo; com os dados do seu terreno.</li>'
        '<li><b>Monte a página</b> daquela etapa no seu Dossiê.</li>'
        '<li><b>Gere o PDF</b> do Dossiê completo no final.</li></ol>'
        '<p style="margin-top:16px">Você faz no seu ritmo, pelo celular ou pelo computador. Não há reunião nem atendimento individual: é uma formação digital.</p>'))

    # Slot do vídeo: o demo plataforma-v02.mp4 NÃO entra (quadros com Land Bank e "receber investimentos", ver AUDITORIA_CONTEUDO.md).
    # Telas reais no lugar; texto do slot vem de 06-criativos/ROTEIRO_VSL.md. Quando o VSL for gravado, ver README (como encaixar).
    B.append(sec("solution", "escuro",
        '<p class="k">A plataforma por dentro</p>'
        '<h2>Veja em poucos minutos como funciona a Mini Mentoria</h2>'
        '<p>Aprenda o passo a passo para estruturar o seu empreendimento turístico antes de construir. R$ 47, pagamento único, reembolso em 7 dias.</p>'
        f'<div class="telas">{telas}</div>'
        '<p class="leg">Telas reais da plataforma. Conteúdo digital, sem reunião nem atendimento individual.</p>'
        + (btn() if A else "")))

    # ---- Oferta + entregáveis + preço + CTA (após construir valor)
    oferta = sec("offer", "escuro",
        '<p class="k">A oferta</p>'
        '<h2>Mini Mentoria de Estruturação</h2>'
        '<p>Uma formação digital com 9 módulos e 70 aulas e materiais: aulas gravadas, fichas &ldquo;Faça agora&rdquo;, e-books por pilar, 2 planilhas de cálculo em branco, Kit do Investidor (modelos), kit de prompts e o Dossiê, em que cada ficha vira uma página e no final você gera o PDF.</p>'
        '<div class="resumo"><div class="preco">R$ 47</div><div>Pagamento único · Pix ou cartão à vista · sem mensalidade</div></div>'
        '<p style="margin-top:14px"><strong>Como o acesso chega:</strong> o acesso é liberado para o e-mail usado na compra. Você entra com esse e-mail; o primeiro acesso é sem criar senha.</p>'
        + (btn() if A else ""))
    ent = entregaveis() + sec("cta", "escuro", '<h2>Pronto para começar?</h2><p>Formação digital, pagamento único, acesso por 12 meses.</p>' + btn(), extra=" cta2")
    sticky = '<div class="barra" id="barra">' + btn() + '<p class="bp"><b>R$ 47</b>pagamento único</p></div>'
    barra_ini = len(B)  # a barra fixa cobre da oferta até o checkout (B) ou desde o hero (A)
    B.append(oferta)
    B.append(ent)

    # Dossiê, cadastro, parceria
    B.append(sec("solution", "escuro",
        '<p class="k">Do projeto ao Dossiê</p>'
        '<h2>Cada ficha vira uma página do seu Dossiê.</h2>'
        '<p>Ao preencher as fichas, você monta, página por página, o seu Dossiê de Desenvolvimento. No final, gera o PDF para guardar e apresentar.</p>'
        '<p class="k" style="margin-top:28px">Cadastro do terreno (opcional)</p>'
        '<p>Se quiser, você pode cadastrar o seu terreno no banco de áreas da Zion. A Zion avalia cada caso, e o cadastro não garante parceria.</p>'
        '<p class="k" style="margin-top:28px">Possibilidade de parceria</p>'
        '<p>Com o projeto organizado, existe a possibilidade de a Zion avaliar uma conversa de parceria. É uma possibilidade, sujeita à análise de cada caso, e não uma garantia.</p>'))

    # Origem do método (única foto de hospedagem além do hero)
    B.append(sec("social-proof", "creme",
        '<p class="k">De onde vem o método</p>'
        '<h2>Experiência de quem opera hospedagem.</h2>'
        f'<img class="foto" src="{BASE}zion-collection/club/fotos/bolha-interior.jpg" alt="Interior de uma unidade da Zion Bubble Glamping" width="1000" height="1250" style="aspect-ratio:4/5;max-width:420px;margin-left:auto;margin-right:auto" loading="lazy">'
        '<p class="leg" style="text-align:center">Foto real: interior da Zion Bubble Glamping, de onde vem a rotina que inspira o método.</p>'
        '<p>A Zion opera a Zion Bubble Glamping em Urubici e em Florianópolis. O método da formação parte dessa rotina de operar hospedagem.</p>'))

    # Checkout
    B.append(sec("cta", "escuro",
        '<p class="k">Mini Mentoria de Estruturação</p>'
        '<h2>Comece a estruturar o seu terreno</h2>'
        '<div class="resumo"><div class="preco">R$ 47</div><div>Pagamento único · sem mensalidade</div></div>'
        + lista([
            "Formação digital: aulas gravadas, fichas, e-books, planilhas e kits",
            "Acesso por 12 meses",
            "Pagamento por Pix ou cartão à vista",
            "Acesso liberado para o e-mail da compra; primeiro acesso sem criar senha",
            "Suporte pelo WhatsApp +55 48 6137-1061",
            "Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor",
        ]) + btn() +
        f'<div class="rodape-aviso"><p>{e(AVISO)}</p></div>'
        '<div class="pagar"><div data-cx-checkout></div></div>', sid="pagar"))

    FAQ = [
        ("Preciso ter capital para começar?", "Não. A formação serve para organizar o projeto antes de buscar capital."),
        ("Preciso ter um projeto pronto?", "Não. Você começa do Marco Zero."),
        ("O que estou comprando?", "Uma formação digital: aulas gravadas, fichas interativas, e-books, planilhas e kits. Não há reunião nem atendimento individual."),
        ("A Zion garante parceria ou investimento?", "Não. Parceria ou investimento é uma possibilidade, sujeita à análise de cada caso, e não uma garantia. A Zion avalia cada caso e nada disso faz parte do que você compra: o valor corresponde ao acesso ao conteúdo digital."),
        ("Como recebo o acesso?", "O acesso é liberado para o e-mail usado na compra. Você entra com esse e-mail; o primeiro acesso é sem criar senha. Se algo não chegar, fale com o suporte pelo WhatsApp +55 48 6137-1061."),
        ("Por quanto tempo tenho acesso?", "Por 12 meses."),
        ("E se eu não gostar?", "Você pode pedir reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor."),
    ]
    faq = "".join(f'<div><div class="cm-accordion-header">{e(q)}</div><div class="cm-accordion-content">{e(a)}</div></div>' for q, a in FAQ)
    B.append(sec("faq", "creme", '<p class="k">Perguntas frequentes</p><h2>Clareza para começar</h2>'
                 f'<div style="margin-top:20px">{faq}</div>', extra=" faq"))
    rodape = ('<footer><div class="w"><p>Zion Hotel Group International · Conteúdo educacional. Resultados dependem do contexto e da execução. '
              f'{e(AVISO)}</p><p>Suporte: WhatsApp +55 48 6137-1061</p></div></footer>')

    # barra fixa (sticky, só CSS): A cobre da dor ao checkout; B só da oferta ao checkout
    ini = 1 if A else barra_ini
    fim = len(B) - 2  # até antes do bloco de checkout? o sticky precisa terminar no #pagar
    # wrapper .meio vai de `ini` até a seção de checkout (exclusive) -> a barra some ao chegar no checkout
    idx_check = len(B) - 2  # posição da seção #pagar (antes do FAQ)
    corpo = "".join(B[:ini]) + '<div class="meio">' + "".join(B[ini:idx_check]) + sticky + '</div>' + "".join(B[idx_check:]) + rodape

    titulo = "Mini Mentoria de Estruturação | Zion Collection"
    desc = "Seu terreno está parado. Aprenda o passo a passo para estruturar o seu empreendimento. Formação digital, R$ 47, pagamento único."
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
{corpo}
</body>
</html>
"""
    out = Path(saida) / "index.html"
    out.write_text(html, encoding="utf-8")
    print(out, len(html), "bytes; <span:", html.count("<span"), "<script:", html.count("<script"), "base64:", html.count("base64"))

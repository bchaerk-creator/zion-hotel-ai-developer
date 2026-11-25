#!/usr/bin/env python3
"""Landing /mini-mentoria-performance · Mini Mentoria de Performance Hoteleira (R$ 47). Gera landing/index.html (código para o ClickMax) e landing/previa.html (com imagens locais).
Reaproveita o CSS das landings club-97 e lt47. Uso: python3 -I producao/mini-mentoria-performance/landing/build.py"""
from html import escape
from pathlib import Path
import re
AQUI = Path(__file__).parent; R = AQUI.parents[2]; C97 = R/"producao/zion-collection/club-97"
CSS = re.search(r'CSS = """(.*?)"""', (C97/"landing/build.py").read_text(encoding="utf-8"), re.S).group(1)
CSS += re.search(r'CSS \+= """(.*?)"""', (C97/"lt47/build.py").read_text(encoding="utf-8"), re.S).group(1)
CSS += """
.sec h2 em,.sec h1 em{font-style:italic}
.capas{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:22px}@media(min-width:620px){.capas{grid-template-columns:repeat(4,1fr)}}
.capas img{width:100%;height:auto;border-radius:8px;display:block;border:1px solid #c9b37e66}
.dossie{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:20px}.dossie img{width:100%;height:auto;border-radius:6px;border:1px solid #c9b37e66;background:#fff}
"""
BASE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
PUB = BASE + "p/adbc67069af26ae0/mini-mentoria-performance/img/"
CTA = "QUERO FAZER MEU DIAGNÓSTICO · R$ 47"
AVISO = ("O valor corresponde ao acesso ao conteúdo digital. O diagnóstico é uma orientação baseada nos dados que você informar: "
         "não garante reservas, ocupação, renda, investimento nem parceria. Parcerias sujeitas à análise da Zion.")
e = lambda t: escape(t, quote=False)
btn = lambda: f'<a href="#pagar" data-cx-cta class="btn">{CTA}</a>'
def sec(kind, tone, inner, sid=None, extra=""):
    i = f' id="{sid}"' if sid else ""
    return f'<section data-cx-section="{kind}"{i} class="sec {tone}{extra}"><div class="w">{inner}</div></section>'
lista = lambda it: '<ul class="lista">' + "".join(f"<li>{e(x)}</li>" for x in it) + "</ul>"
def montar(img):
    B = [f'<div class="escuro"><div class="w topo"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion Hotel Group International" width="170" height="34"></div></div>']
    B.append(sec("hero", "escuro",
        '<p class="k">Mini Mentoria de Performance Hoteleira · Raio-X da Hospedagem</p>'
        '<h1>Seu calendário de reservas <em>não está cheio?</em></h1>'
        '<p class="sub">Descubra o que pode estar impedindo sua hospedagem de crescer. Faça seu diagnóstico e receba um plano de ação personalizado.</p>'
        '<div class="centro"><p class="selo">R$ 47 · pagamento único · para Airbnb, casas, apartamentos, pousadas e glampings</p></div>' + btn(), sid="hero"))
    B.append(sec("problem", "creme",
        '<p class="k">Você se identifica?</p><h2>Antes de investir mais, descubra onde estão as oportunidades.</h2>'
        '<p>Você investiu em uma hospedagem, mas as reservas, a diária ou a margem não correspondem às expectativas.</p>'
        '<p><strong>Calendário com buracos.</strong> Você não sabe se o problema é o anúncio, o preço, a experiência ou a operação.</p>'
        '<p><strong>Faturamento que não vira lucro.</strong> Entra dinheiro, mas sobra pouco, e você não tem a conta de custos e equilíbrio.</p>'
        '<p><strong>Decisões no escuro.</strong> Sem dados organizados, é difícil saber o que corrigir primeiro.</p>'
        '<p>O Raio-X organiza o que você já sabe, mostra o que falta saber e transforma isso em ações.</p>'))
    B.append(sec("solution", "escuro",
        '<p class="k">Veja como funciona</p><h2>Acesse, aprenda, responda e gere o seu plano.</h2>'
        '<ol class="jornada"><li>Acesse a plataforma e escolha o módulo</li><li>Aprenda com o guia e responda ao formulário, com evidências</li><li>Use a calculadora com os seus números</li><li>Receba o diagnóstico por pilar e o plano de 7, 30, 60 e 90 dias</li></ol>'
        f'<video class="video" controls playsinline preload="none" poster="{img("tela-formulario.jpg")}" src="{img("demo.mp4")}">O seu navegador não reproduz este vídeo.</video>'
        '<p class="leg">Demonstração real da plataforma, com um exemplo identificado como fictício. Não é depoimento nem resultado de cliente.</p>'
        '<div class="telas quatro">' + "".join(f'<figure class="moldura"><div class="celular"><img src="{img(n)}" alt="{e(l)} (tela real da plataforma, dados fictícios)" width="780" height="1560" loading="lazy"></div><p class="real">Tela real</p><p>{e(l)}</p></figure>' for n, l in [("tela-formulario.jpg", "Formulário do módulo"), ("tela-calculadora.jpg", "Calculadora"), ("tela-diagnostico.jpg", "Diagnóstico por pilar"), ("tela-plano.jpg", "Plano de ação")]) + "</div>" + btn()))
    B.append(sec("offer", "creme",
        '<p class="k">O que está incluído</p><h2>Sete pilares, do anúncio à parceria.</h2>'
        + lista(["7 aulas guiadas, uma por pilar: identidade, vendas, experiência, finanças, operação, expansão e parcerias",
                 "7 guias em PDF, com passo a passo, exemplos fictícios e registro de trabalho",
                 "7 formulários com 70 perguntas: você marca implementado, parcial, ausente, não sei ou não se aplica",
                 "7 calculadoras: posicionamento, ocupação e canais, diária e RevPAR, contribuição e equilíbrio, capacidade e estoque, custo e retorno da expansão, necessidade de capital",
                 "Diagnóstico Raio-X, com nota por pilar e a cobertura dos seus dados",
                 "Plano de ação personalizado, com responsável, prazo, indicador e evidência",
                 "Gerador de dossiê em PDF",
                 "Sem reunião obrigatória: você faz no seu ritmo"]) +
        '<div class="capas">' + "".join(f'<img src="{img(f"capa-{m}.jpg")}" alt="Capa do guia {m}" width="1080" height="1350" loading="lazy">' for m in range(1, 8)) + "</div>"
        '<p class="nota">Capas com fotos reais da Zion Bubble Glamping. O método vale para qualquer tipo de hospedagem.</p>'
        '<h3 style="margin-top:30px">O que o seu dossiê mostra</h3><p>Identificação, dados declarados, cálculos, cobertura, pontos fortes, lacunas, plano 7/30/60/90 dias, hipóteses e limitações.</p>'
        '<div class="dossie">' + "".join(f'<img src="{img(f"dossie-{i}.jpg")}" alt="Página {i} do dossiê de exemplo (dados fictícios)" width="580" height="820" loading="lazy">' for i in (1, 2, 3, 4)) + "</div>"
        '<p class="leg">Dossiê de exemplo, gerado com dados fictícios.</p>' + btn()))
    B.append(sec("solution", "escuro",
        '<p class="k">Como o diagnóstico funciona</p><h2>Sem achismo e sem zero escondido.</h2>'
        '<p>A nota de cada pilar considera só as respostas com dados. “Não sei” e “não se aplica” não pontuam: aparecem como cobertura e como ações para coletar a informação.</p>'
        '<p>O plano começa pelo que envolve segurança e legalidade e depois prioriza impacto e esforço. É uma orientação educacional e pode ser ajustada por você.</p>'
        '<p class="k" style="margin-top:26px">Queremos conhecer seu empreendimento</p>'
        '<p>Depois de gerar o dossiê, você pode, se quiser, autorizar o envio à Zion para avaliarmos possíveis soluções e parcerias. É opcional e nada é enviado automaticamente. Não há garantia de investimento.</p>'))
    B.append(sec("social-proof", "creme",
        '<p class="k">De onde vem o método</p><h2>Experiência de quem opera hospedagem.</h2>'
        f'<img class="foto" src="{img("origem.jpg")}" alt="Zion Bubble Glamping" width="1000" height="1250" style="aspect-ratio:4/5;max-width:420px;margin-left:auto;margin-right:auto" loading="lazy">'
        '<p class="leg" style="text-align:center">Foto real da Zion Bubble Glamping, de onde vem a rotina que inspira o método.</p>'
        '<p>A Zion opera a Zion Bubble Glamping em Urubici e em Florianópolis. O Raio-X parte dessa rotina de operar hospedagem.</p>'))
    B.append(sec("cta", "escuro",
        '<p class="k">Mini Mentoria de Performance Hoteleira</p><h2>Faça o seu Raio-X da Hospedagem</h2>'
        '<div class="resumo"><div class="preco">R$ 47</div><div>Pagamento único · sem mensalidade</div></div>'
        + lista(["Acesso completo: 7 aulas, 7 guias, 7 formulários, 7 calculadoras, diagnóstico e dossiê", "Acesso por 12 meses", "Pagamento por Pix ou cartão à vista",
                 "O acesso chega no e-mail da compra assim que o pagamento é confirmado", "Suporte pelo WhatsApp +55 48 6137-1061", "Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor"]) +
        f'<div class="rodape-aviso"><p>{e(AVISO)}</p></div><div class="pagar"><div data-cx-checkout></div></div>', sid="pagar"))
    FAQ = [("Para quem é?", "Para donos e gestores de Airbnb, casas, apartamentos, chalés, pousadas e glampings."),
           ("Preciso de capital?", "Não para aprender. O diagnóstico serve para organizar a sua situação antes de qualquer investimento."),
           ("O diagnóstico garante reservas?", "Não. É uma orientação baseada nos dados que você informar. " + "Reservas, ocupação, renda e investimento dependem de muitos fatores."),
           ("Há mentoria individual?", "Não. É uma formação gravada e interativa, sem reunião obrigatória."),
           ("Meus dados ficam com a Zion?", "Não automaticamente. Suas respostas ficam no seu aparelho. Você só compartilha com a Zion se quiser, e pode pedir a exclusão pelo WhatsApp de suporte."),
           ("Por quanto tempo tenho acesso?", "Por 12 meses."),
           ("E se eu não gostar?", "Você pode pedir reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor. O atendimento é pelo WhatsApp +55 48 6137-1061.")]
    faq = "".join(f'<div><div class="cm-accordion-header">{e(q)}</div><div class="cm-accordion-content">{e(a)}</div></div>' for q, a in FAQ)
    B.append(sec("faq", "creme", f'<p class="k">Perguntas frequentes</p><h2>Clareza para começar</h2><div style="margin-top:20px">{faq}</div>', extra=" faq"))
    B.append(sec("cta", "escuro", '<h2>Pronto para ver onde estão as oportunidades?</h2>' + btn()))
    B.append(f'<footer><div class="w"><p>Zion Hotel Group International · Conteúdo educacional. {e(AVISO)}</p><p>Suporte: WhatsApp +55 48 6137-1061</p></div></footer>')
    return "".join(B)
def doc(corpo, extra_head=""):
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mini Mentoria de Performance Hoteleira</title>{extra_head}<style>{CSS}</style></head><body>{corpo}</body></html>'
(AQUI/"index.html").write_text(montar(lambda n: PUB + n))
(AQUI/"previa.html").write_text(doc(montar(lambda n: "img/" + n)))
print("landing ok", len((AQUI/"index.html").read_text()))

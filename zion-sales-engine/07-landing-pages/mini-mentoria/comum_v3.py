#!/usr/bin/env python3
"""Gerador v3 das variantes A e B da landing da Mini Mentoria de Estruturação Zion (R$ 47).
v3 (25/11/2026): Sessão de Diagnóstico Estratégico (reunião após o Dossiê, decisão de Bruno), redação segura da vistoria dos entregáveis,
faixa "Formação paga · Mini Mentoria Zion · R$47". Não altera comum.py, comum_v2.py nem variantes v1/v2.
Só afirma o que consta em 13-relatorios/VISTORIA_ENTREGAVEIS.md (redação segura). Sem <script>, <span> ou base64.
Botões ANTES da oferta só rolam (âncoras); só depois da oferta o botão leva ao checkout (#pagar) com o preço.
Uso: python3 -I variante-a-v3/build.py  (ou variante-b-v3/build.py)"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum  # noqa: E402  (reaproveita CSS, helpers e o bloco de cards)
from comum import e, sec, lista, BASE, PIL, bb  # noqa: E402

NOME = "Mini Mentoria de Estruturação Zion"
CTA_PAGAR = "QUERO ACESSAR A PLATAFORMA POR R$47"
SESSAO = "Sessão de Diagnóstico Estratégico"
NOTA = "*Sessão sujeita à análise e à agenda. Parceria e investimento não são garantidos."
AVISO = ("O valor corresponde ao acesso à formação digital. Ela não garante parceria, investimento, "
         "aprovação de projeto nem resultado financeiro. " + NOTA.lstrip("*"))
MODULOS = [("Comece aqui · Onboarding", 3), ("Marco Zero · A visão de toda a jornada", 10),
           ("Pilar 1 · Território e destino", 8), ("Pilar 2 · Mercado e demanda", 8),
           ("Pilar 3 · Produto e tipologias", 8), ("Pilar 4 · Modelo de negócio", 9),
           ("Pilar 5 · Masterplan faseado", 8), ("Pilar 6 · Pré-viabilidade", 8),
           ("Pilar 7 · Capital e Dossiê", 8)]
FAIXA = "Formação paga · Mini Mentoria Zion · R$47"
assert sum(n for _, n in MODULOS) == 70 and len(MODULOS) == 9

CSS = comum.CSS + """
.mods{list-style:none;margin:18px 0 0;padding:0;counter-reset:m}
.mods li{counter-increment:m;position:relative;display:flex;justify-content:space-between;gap:12px;margin:0 0 8px;padding:11px 14px 11px 46px;background:#fff;border:1px solid #8b714e59;border-radius:12px;color:#1b2117;font-family:Jost,sans-serif;font-size:15.5px;line-height:1.35}
.mods li::before{content:counter(m);position:absolute;left:12px;top:50%;transform:translateY(-50%);width:24px;height:24px;border-radius:50%;background:#1b2117;color:#c9b37e;font-weight:600;text-align:center;line-height:24px;font-size:13px}
.mods li b{font-weight:500;white-space:nowrap;color:#8b714e}
.mats{list-style:none;margin:18px 0 0;padding:0;display:grid;grid-template-columns:minmax(0,1fr);gap:8px}
.mats li{margin:0;padding:12px 14px;background:#1b2117;border:1px solid #c9b37e55;border-radius:12px;color:#fef5f0;font-family:Jost,sans-serif;font-size:15.5px;line-height:1.35}
.mats li b{color:#c9b37e;font-weight:500}
.inclui{list-style:none;margin:14px 0 0;padding:0}
.inclui li{margin:0 0 8px;padding:0 0 0 26px;position:relative;color:#fef5f0;font-family:Jost,sans-serif;font-size:16.5px;line-height:1.4}
.inclui li::before{content:"";position:absolute;left:2px;top:.45em;width:12px;height:7px;border-left:2px solid #c9b37e;border-bottom:2px solid #c9b37e;transform:rotate(-45deg)}
.inclui li b{color:#c9b37e;font-weight:500}
.faixa{background:#c9b37e;color:#1b2117;text-align:center;font-family:Jost,sans-serif;font-weight:500;font-size:14px;letter-spacing:.06em;padding:9px 16px;margin:0}
.fnota{font-size:13.5px;margin-top:14px}
.dossie{list-style:none;margin:14px 0 0;padding:0;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:6px}
.dossie li{margin:0;padding:9px 10px;background:#040605;border:1px solid #c9b37e40;border-radius:10px;color:#fef5f0;font-family:Jost,sans-serif;font-size:14px;line-height:1.3}
.dossie li b{color:#c9b37e;font-weight:500}
@media(min-width:820px){.mats{grid-template-columns:repeat(2,minmax(0,1fr))}.dossie{grid-template-columns:repeat(4,minmax(0,1fr))}}
"""


VD, FC, EBK, TUT = ("video", "vídeo-aulas"), ("ficha", "1 ficha"), ("ebook", "e-book"), ("video", "tutorial em vídeo")
CARDS = [
    ("Comece aqui", "Onboarding", "Orientação para usar a plataforma e o seu dossiê inicial.", "Entender como a plataforma funciona.", [("ficha", "dossiê inicial"), ("chat", "suporte")]),
    ("Marco Zero", "A visão da jornada", "Visão da jornada e diagnóstico prévio (Página 0).", "Saber por onde começar.", [VD, TUT, FC, EBK]),
    ("Dossiê 1", "Território", "O seu terreno e o destino em volta.", "Descrever o terreno numa página só.", [VD, TUT, FC, EBK]),
    ("Dossiê 2", "Mercado", "Comparáveis, diária, ocupação e demanda.", "Levantar esses dados da sua região.", [VD, TUT, FC, EBK]),
    ("Dossiê 3", "Produto", "Nicho, público, promessa e unidade.", "Definir o que oferecer e para quem.", [VD, TUT, FC, EBK]),
    ("Dossiê 4", "Modelo de Negócio", "Como o projeto gera resultado: renda ou venda.", "Escolher o caminho do projeto.", [VD, TUT, FC, EBK]),
    ("Dossiê 5", "Masterplan", "O terreno no papel, em fases.", "Ver o que cabe e começar pela fase um.", [VD, TUT, FC, EBK]),
    ("Dossiê 6", "Pré-viabilidade", "O custo e a conta, com três cenários.", "Fazer a conta com as suas premissas.", [VD, TUT, FC, EBK, ("planilha", "2 planilhas")]),
    ("Dossiê 7", "Capital e decisão", "De onde vem o capital e o Dossiê final.", "Decidir: avançar, ajustar ou parar.", [VD, TUT, FC, EBK, ("kit", "Kit do Investidor"), ("kit", "9 comandos de IA")]),
]


def ancora(texto, alvo):
    """Botão que só rola até uma seção. Nunca leva ao pagamento."""
    return f'<a href="#{alvo}" data-cx-cta class="btn">{texto}</a>'


def pagar():
    return f'<a href="#pagar" data-cx-cta class="btn">{CTA_PAGAR}</a>'


def build(variante, saida):
    A = variante == "A"
    B = []
    B.append(f'<div class="escuro"><div class="w topo"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion Hotel Group International" width="170" height="34"></div></div>')
    B.append(f'<p class="faixa">{FAIXA}</p>')

    # ---- HERO
    hero_top = (f'<p class="k">{NOME} · formação digital autônoma</p>'
                '<h1>Seu terreno está parado. <em>O que falta é um projeto.</em></h1>')
    hero_bot = ('<p class="sub">Aprenda o passo a passo para estruturar o seu projeto, conhecer alternativas de desenvolvimento '
                'e prepará-lo para apresentar a potenciais parceiros e investidores.</p>')
    if A:
        hero_bot += (f'<div class="centro"><p class="selo">{NOME} · R$47 · pagamento único</p></div>'
                     + ancora("VER A PLATAFORMA POR DENTRO", "demonstracao"))
    else:
        hero_bot += ('<div class="centro"><p class="selo">Formação digital · pagamento único · sem mensalidade</p></div>'
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
    # ---- I Implementação
    B.append(sec("solution", "creme",
        '<p class="k">Como você aplica</p>'
        '<h2>Na plataforma, passo a passo.</h2>'
        '<ol class="passos">'
        '<li><b>Assista</b> às vídeo-aulas da etapa.</li>'
        '<li><b>Preencha a ficha</b> &ldquo;Faça agora&rdquo; com os dados do seu terreno.</li>'
        '<li><b>Monte a página</b> daquela etapa no seu Dossiê.</li>'
        '<li><b>Gere o PDF</b> do Dossiê completo no final.</li>'
        f'<li><b>Depois da mentoria: solicite uma {SESSAO}*.</b> Ao concluir o Dossiê, você pode solicitar a sessão gratuita com a nossa equipe para apresentar o seu projeto.</li></ol>'
        '<p style="margin-top:16px">Formação digital autônoma: você estuda no seu ritmo, pelo celular ou pelo computador.</p>'
        f'<p class="fnota">{NOTA}</p>'))
    # ---- Depois da mentoria (narrativa de expansão)
    B.append(sec("solution", "escuro",
        '<p class="k">Depois da mentoria</p>'
        '<h2>Estruture o seu projeto e faça parte da nossa expansão.</h2>'
        '<p>Faça a mentoria. Depois, nós queremos te conhecer.</p>'
        f'<p>Ao concluir o Dossiê, você pode solicitar uma <b>{SESSAO}</b> com a nossa equipe para apresentar o seu projeto, terreno ou empreendimento. É a sua oportunidade de buscar parceiros e investimentos para tirar o plano do papel*.</p>'
        '<p>A sessão é gratuita para quem concluiu o Dossiê. Você pede por um formulário, e a nossa equipe analisa e responde conforme a agenda.</p>'
        f'<p class="nota">{NOTA}</p>'))
    # ---- Passeio pela plataforma (telas reais seguras)
    telas_def = [("aula", "Aula interativa do Marco Zero"), ("diagnostico", "Faça agora: diagnóstico prévio"),
                 ("previab", "Faça agora: pré-viabilidade")]
    telas = "".join(
        f'<figure class="moldura"><div class="celular"><img src="{BASE}zion-collection/club/telas/{n}.jpg" alt="{e(l)} (tela real da plataforma)" width="640" height="1280" loading="lazy"></div>'
        f'<p class="real">Tela real</p><p>{e(l)}</p></figure>' for n, l in telas_def)
    B.append(sec("solution", "escuro",
        '<p class="k">A plataforma por dentro</p>'
        '<h2>Veja como é por dentro</h2>'
        '<p>Aulas, fichas e o seu Dossiê no mesmo lugar. Estas são telas reais da plataforma.</p>'
        f'<div class="telas">{telas}</div>'
        '<p class="leg">Telas reais da plataforma. Formação digital autônoma.</p>'
        + (ancora("VER O QUE ESTÁ INCLUÍDO", "oferta") if A else ""), sid="demonstracao"))
    # ---- Módulos e materiais
    mods = '<ol class="mods">' + "".join(f"<li>{e(n)} <b>{q} conteúdos</b></li>" for n, q in MODULOS) + '</ol>'
    mats = ('<ul class="mats">'
            '<li><b>Vídeo-aulas</b> e <b>8 tutoriais em vídeo</b> de como preencher cada ficha</li>'
            '<li><b>8 fichas interativas &ldquo;Faça agora&rdquo;</b>: cada ficha vira uma página do seu Dossiê</li>'
            '<li><b>8 e-books em PDF</b>: Marco Zero e um por pilar</li>'
            '<li><b>2 planilhas de cálculo com fórmulas</b>, para você preencher</li>'
            '<li><b>Kit do Investidor</b>: guia das 6 peças (teaser, one-pager, pitch, masterplan, plano conceitual e marca)</li>'
            '<li><b>9 comandos de IA prontos</b> (ChatGPT ou Claude, com a sua conta)</li>'
            '<li><b>Dossiê de Desenvolvimento</b> para baixar em PDF</li>'
            f'<li><b>{SESSAO}</b>: depois de concluir o Dossiê, você pode solicitar essa sessão gratuita com a nossa equipe*</li></ul>'
            f'<p class="fnota">{NOTA}</p>')
    dossie = ('<ul class="dossie"><li><b>0</b> Diagnóstico prévio</li><li><b>1</b> Território</li><li><b>2</b> Mercado</li><li><b>3</b> Produto</li>'
              '<li><b>4</b> Modelo de negócio</li><li><b>5</b> Masterplan</li><li><b>6</b> Pré-viabilidade</li><li><b>7</b> Capital e decisão</li></ul>')
    B.append(sec("solution", "creme",
        '<p class="k">Módulos, materiais e documentos</p>'
        '<h2>9 módulos e 70 conteúdos</h2>'
        '<p>Os 70 conteúdos entre vídeos, fichas, e-books, planilhas e kits, módulo por módulo.</p>' + mods +
        '<p class="k" style="margin-top:30px">Materiais</p>' + mats))
    B.append(sec("solution", "escuro",
        '<p class="k">Documento final</p>'
        '<h2>O seu Dossiê, página por página</h2>'
        '<p>Ao preencher as fichas, você monta o seu Dossiê de Desenvolvimento. No final, gera o PDF para guardar e para apresentar o seu projeto a potenciais parceiros e investidores. Apresentar não é garantia de parceria nem de investimento.</p>'
        + dossie))

    # ---- OFERTA completa (preço antes de qualquer botão de pagamento)
    inclui = ('<ul class="inclui">'
              '<li><b>R$47</b> em pagamento único, sem mensalidade</li>'
              '<li>Acesso à plataforma digital, com o e-mail da compra</li>'
              '<li><b>9 módulos</b> e <b>70 conteúdos</b> entre vídeos, fichas, e-books, planilhas e kits</li>'
              '<li>Formação digital autônoma, no seu ritmo</li>'
              f'<li>Depois de concluir o Dossiê: solicitação da <b>{SESSAO}</b> gratuita*</li>'
              '<li>Pagamento por <b>Pix</b> ou <b>cartão de crédito à vista</b></li>'
              '<li><b>Garantia de 7 dias</b>, como prevê o Código de Defesa do Consumidor</li>'
              '<li>Acesso liberado com o e-mail da compra; primeiro acesso sem criar senha</li></ul>')
    oferta = sec("offer", "escuro",
        '<p class="k">A oferta</p>'
        f'<h2>{NOME}</h2>'
        '<p>Uma formação digital para estruturar um empreendimento turístico no seu terreno: vídeo-aulas, fichas, e-books, planilhas, Kit do Investidor, comandos de IA e o Dossiê em PDF.</p>'
        '<div class="resumo"><div class="preco">R$ 47</div><div>Pagamento único · sem mensalidade · acesso à plataforma digital</div></div>'
        + inclui + f'<p class="nota" style="color:#ded6bf">{NOTA}</p>' + (pagar() if A else ""), sid="oferta")
    B.append(oferta)
    ent = ('<section data-cx-section="solution" id="entregaveis" class="sec ent-sec"><div class="w">'
           '<p class="ent-k">O que você recebe</p><h2 class="ent-h">O que você recebe em cada etapa.</h2>'
           '<p class="ent-intro">Em cada etapa você assiste, preenche uma ficha e monta uma página do seu Dossiê.</p>'
           '<div class="ent-lista">' + "".join(bb.card(c) for c in CARDS) + '</div>'
           '<div class="ent-fim"><p class="ent-fk">No final você tem</p>'
           '<p class="ent-fp"><b>O seu Dossiê completo (PDF)</b>, para guardar e apresentar o seu projeto.</p>'
           f'<p class="ent-opc"><b>Depois:</b> {SESSAO} gratuita, por solicitação, ao concluir o Dossiê.* {NOTA[1:]}</p></div>'
           '<p class="ent-nota">Material educativo. O resultado depende do que você preencher.</p></div></section>')
    B.append(ent)
    cta_fim = sec("cta", "escuro",
        '<h2>Pronto para começar?</h2>'
        f'<div class="resumo"><div class="preco">R$ 47</div><div>{NOME} · pagamento único · acesso à plataforma digital · Pix ou cartão à vista</div></div>'
        + pagar(), extra=" cta2")
    B.append(cta_fim)
    barra_ini = len(B) - 3  # oferta, entregáveis, cta2: a barra fixa só existe daqui até o checkout

    # Origem do método
    B.append(sec("social-proof", "creme",
        '<p class="k">De onde vem o método</p>'
        '<h2>Experiência de quem opera hospedagem.</h2>'
        f'<img class="foto" src="{BASE}zion-collection/club/fotos/bolha-interior.jpg" alt="Interior de uma unidade da Zion Bubble Glamping" width="1000" height="1250" style="aspect-ratio:4/5;max-width:420px;margin-left:auto;margin-right:auto" loading="lazy">'
        '<p class="leg" style="text-align:center">Foto real: interior da Zion Bubble Glamping, de onde vem a rotina que inspira o método.</p>'
        '<p>A Zion opera a Zion Bubble Glamping em Urubici e em Florianópolis. O método da formação parte dessa rotina de operar hospedagem.</p>'))

    # Checkout (sem botão extra: o checkout vem logo abaixo)
    B.append(sec("cta", "escuro",
        f'<p class="k">{NOME}</p>'
        '<h2>Finalize o seu acesso</h2>'
        '<div class="resumo"><div class="preco">R$ 47</div><div>Pagamento único · sem mensalidade</div></div>'
        + lista(["Acesso à plataforma digital da formação",
                 "9 módulos e 70 conteúdos entre vídeos, fichas, e-books, planilhas e kits",
                 f"Depois do Dossiê: {SESSAO} gratuita, por solicitação*",
                 "Pagamento por Pix ou cartão de crédito à vista",
                 "Garantia: reembolso em até 7 dias",
                 "Acesso liberado com o e-mail da compra; primeiro acesso sem criar senha",
                 "Suporte pelo WhatsApp +55 48 6137-1061"]) +
        f'<div class="rodape-aviso"><p>{e(AVISO)}</p></div>'
        '<div class="pagar"><div data-cx-checkout></div></div>', sid="pagar"))

    FAQ = [
        ("O que estou comprando?", f"A {NOME}: uma formação digital autônoma, com 9 módulos e 70 conteúdos (vídeo-aulas e 8 tutoriais em vídeo, 8 fichas interativas, 8 e-books em PDF, 2 planilhas de cálculo com fórmulas, Kit do Investidor, 9 comandos de IA e o Dossiê para baixar em PDF). Você acessa tudo na plataforma digital, com pagamento único de R$47 e sem mensalidade. É uma formação paga."),
        ("Quanto custa e como pago?", "R$47, em pagamento único, por Pix ou cartão de crédito à vista. Não há mensalidade nem boleto."),
        ("Preciso ter capital para começar?", "Não. A formação serve para organizar o projeto antes de buscar capital."),
        ("Preciso ter um projeto pronto?", "Não. Você começa do Marco Zero."),
        ("Tem reunião?", f"Depois de concluir o Dossiê você pode solicitar uma reunião gratuita com a nossa equipe, a {SESSAO}, para apresentar o seu projeto. Ela é sujeita à análise e à agenda. Não há atendimento individual contínuo. Parceria e investimento não são garantidos."),
        ("Como solicito a Sessão de Diagnóstico Estratégico?", "Ao concluir o Dossiê, você preenche um formulário de solicitação. A nossa equipe analisa e, se for o caso, agenda conforme a disponibilidade. A solicitação não garante a sessão."),
        ("A Sessão de Diagnóstico Estratégico é a mesma coisa que a Sessão de onboarding e estratégia?", "Não. A Sessão de onboarding e estratégia é de outro produto. A Sessão de Diagnóstico Estratégico é uma etapa opcional depois do Dossiê da Mini Mentoria, gratuita, por solicitação."),
        ("A Zion garante parceria ou investimento?", "Não. A formação ensina a preparar o seu projeto para apresentá-lo a potenciais parceiros e investidores, e a sessão é a oportunidade de apresentá-lo à nossa equipe. Parceria e investimento não são garantidos."),
        ("Como recebo o acesso?", "O acesso é liberado com o e-mail usado na compra. O primeiro acesso é sem criar senha. Se algo não funcionar, fale com o suporte pelo WhatsApp +55 48 6137-1061."),
        ("Quais são as condições de acesso?", "O acesso à plataforma digital é liberado com o e-mail da compra. Pelas condições técnicas atuais da turma, o acesso dura 12 meses a partir da liberação."),
        ("E se eu não gostar?", "Você pode pedir reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor."),
    ]
    faq = "".join(f'<div><div class="cm-accordion-header">{e(q)}</div><div class="cm-accordion-content">{e(a)}</div></div>' for q, a in FAQ)
    B.append(sec("faq", "creme", '<p class="k">Perguntas frequentes</p><h2>Clareza para começar</h2>'
                 f'<div style="margin-top:20px">{faq}</div>', extra=" faq"))
    rodape = ('<footer><div class="w"><p>Zion Hotel Group International · Conteúdo educacional. Resultados dependem do contexto e da execução. '
              f'{e(AVISO)}</p><p>Suporte: WhatsApp +55 48 6137-1061</p></div></footer>')

    sticky = ('<div class="barra" id="barra">' + pagar() + '<p class="bp"><b>R$ 47</b>pagamento único</p></div>')
    idx_check = len(B) - 2  # seção #pagar (antes do FAQ)
    corpo = ("".join(B[:barra_ini]) + '<div class="meio">' + "".join(B[barra_ini:idx_check]) + sticky + '</div>'
             + "".join(B[idx_check:]) + rodape)

    titulo = f"{NOME} | R$47"
    desc = "Seu terreno está parado. Aprenda o passo a passo para estruturar o seu projeto. Formação digital autônoma, R$47, pagamento único, acesso à plataforma digital."
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

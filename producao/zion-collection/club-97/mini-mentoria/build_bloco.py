#!/usr/bin/env python3
"""Gera bloco_entregaveis.html: seção 'Entregáveis pilar a pilar' (HTML + CSS inline, sem JS, sem base64, sem <span>).
Fatos: INVENTARIO.md seção 1 e classrooms_details da turma 087479a3 (25/11/2026). Uso: python3 -I build_bloco.py"""
from html import escape
from pathlib import Path

def e(t):
    return escape(t, quote=False)

# (rótulo, nome, aulas, assiste, preenche, leva, para_que)
CARDS = [
    ("Comece aqui", "Onboarding", 3,
     "Bem-vindo à plataforma Zion Collection (vídeo).",
     "Monte o seu dossiê inicial (formulário de entrada).",
     "O caminho da plataforma e o chat de suporte para tirar dúvidas.",
     "Entender como tudo funciona antes de começar."),
    ("Marco Zero", "A visão de toda a jornada", 10,
     "Vídeo 1 · A visão, quem somos e o setor. Vídeo 2 · As dores, a jornada e o seu diagnóstico.",
     "Faça agora · O seu diagnóstico prévio (cerca de 6 minutos). Opcional: a ficha do seu terreno, com dados, fotos e documentos.",
     "Página 0 do Dossiê: o diagnóstico prévio, em PDF. E-book Vol. 1, mapa de direcionamento da jornada e Kit de prompts do Dossiê.",
     "Ver a jornada inteira e saber por onde começar."),
    ("Pilar 1", "Território e destino", 8,
     "Vídeo 3 · O destino e a chegada. Vídeo 4 · O chão, a área e os papéis.",
     "Faça agora · A sua Ficha do Território.",
     "Página 1 do Dossiê: Território, em PDF. E-book do Pilar 1, e-book completo e aula de 40 slides para ir mais fundo.",
     "Descrever o seu terreno e o destino em volta, numa página só."),
    ("Pilar 2", "Mercado e demanda", 8,
     "Vídeo 5 · Os comparáveis, a diária e a ocupação. Vídeo 6 · A curva do ano, quem paga e quantas cabem.",
     "Faça agora · A sua Ficha do Mercado.",
     "Página 2 do Dossiê: Mercado, em PDF. E-book do Pilar 2, e-book completo e aula de 40 slides.",
     "Aprender a levantar comparáveis, diária e ocupação da sua região."),
    ("Pilar 3", "Produto e tipologias", 8,
     "Vídeo 7 · O nicho, para quem e o momento. Vídeo 8 · A estadia, a promessa e a unidade.",
     "Faça agora · A sua Ficha do Produto.",
     "Página 3 do Dossiê: Produto, em PDF. E-book do Pilar 3, e-book completo e aula de 40 slides.",
     "Definir o que você vai oferecer e para quem."),
    ("Pilar 4", "Modelo de negócio", 9,
     "Vídeo 9 · O modelo de renda. Vídeo 10 · O modelo de venda. Extra · O mapa dos modelos.",
     "Faça agora · O seu Modelo de Negócio.",
     "Página 4 do Dossiê: Modelo de Negócio, em PDF. E-book do Pilar 4, e-book completo e aula de 40 slides.",
     "Escolher como o projeto gera resultado: renda ou venda."),
    ("Pilar 5", "Masterplan faseado", 8,
     "Vídeo 11 · O masterplan, onde nunca e o que precisa existir. Vídeo 12 · O que cabe, o que se vende e a fase um.",
     "Faça agora · O seu Masterplan faseado.",
     "Página 5 do Dossiê: Masterplan, em PDF. E-book do Pilar 5, e-book completo e aula de 40 slides.",
     "Pôr o terreno no papel: onde não construir, o que cabe e o que fica para a fase um."),
    ("Pilar 6", "Pré-viabilidade", 8,
     "Vídeo 13 · Quanto custa o projeto inteiro. Vídeo 14 · A conta, os três cenários e o tempo de volta.",
     "Faça agora · A sua Pré-viabilidade.",
     "Página 6 do Dossiê: Pré-viabilidade, em PDF. E-book do Pilar 6 e duas planilhas de cálculo: Orçamento de Abertura e Pré-viabilidade (Estudo de Massas).",
     "Fazer a conta do seu projeto com as suas próprias premissas. É material educativo: o resultado depende do que você informa."),
    ("Pilar 7", "Capital e Dossiê", 8,
     "Vídeo 15 · De onde vem o capital, e com quem. Vídeo 16 · O Dossiê e a decisão.",
     "Faça agora · O seu Dossiê de Desenvolvimento.",
     "Página 7 do Dossiê: Capital e Dossiê. O Dossiê completo, em PDF. Kit do Investidor: guia e modelos de pitch, teaser e one-pager.",
     "Fechar o Dossiê e decidir o próximo passo: avançar, ajustar ou parar."),
]

CSS = """
.ent-sec{background:#ded6bf;color:#1b2117;padding:44px 0 40px;font-family:'Jost',sans-serif}
.ent-sec .w{max-width:760px;margin:0 auto;padding:0 20px}
.ent-sec p.ent-k{font-family:'Jost',sans-serif;font-size:11.5px;font-weight:400;letter-spacing:.18em;text-transform:uppercase;color:#6b5636;margin:0 0 14px;line-height:1.5}
.ent-sec h2.ent-h{font-family:'Cormorant Garamond',serif;font-weight:500;font-size:32px;line-height:1.1;color:#1b2117!important;margin:0}
.ent-sec p.ent-intro{font-family:'Jost',sans-serif;font-size:16.5px;font-weight:400;line-height:1.55;color:#1b2117;margin:14px 0 0}
.ent-lista{display:grid;grid-template-columns:minmax(0,1fr);gap:14px;margin:24px 0 0;padding:0}
.ent-card{background:#1b2117;border:1px solid #c9b37e66;border-radius:16px;padding:18px 18px 16px;margin:0;min-width:0}
.ent-sec p.ent-eb{font-family:'Jost',sans-serif;font-size:11px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:#c9b37e;margin:0;line-height:1.4}
.ent-sec h3.ent-t{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:27px;line-height:1.1;color:#fef5f0!important;margin:4px 0 0}
.ent-row{border-top:1px solid #c9b37e33;margin:12px 0 0;padding:10px 0 0}
.ent-sec p.ent-l{font-family:'Jost',sans-serif;font-size:11px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:#c9b37e;margin:0;line-height:1.4}
.ent-sec p.ent-v{font-family:'Jost',sans-serif;font-size:15.5px;font-weight:300;line-height:1.5;color:#fef5f0;margin:3px 0 0;overflow-wrap:anywhere}
.ent-sec p.ent-pq{font-family:'Jost',sans-serif;font-size:15px;font-weight:400;line-height:1.5;color:#1b2117;background:#c9b37e;border-radius:10px;margin:14px 0 0;padding:10px 12px}
.ent-sec p.ent-pq strong{font-weight:600;color:#1b2117}
.ent-fim{background:#040605;border:1px solid #c9b37e;border-radius:18px;padding:22px 20px;margin:20px 0 0}
.ent-sec p.ent-fk{font-family:'Jost',sans-serif;font-size:11.5px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:#c9b37e;margin:0;line-height:1.4}
.ent-sec h3.ent-fh{font-family:'Cormorant Garamond',serif;font-weight:500;font-size:30px;line-height:1.1;color:#fef5f0!important;margin:6px 0 0}
.ent-sec p.ent-fp{font-family:'Jost',sans-serif;font-size:16px;font-weight:300;line-height:1.55;color:#fef5f0;margin:12px 0 0}
.ent-sec p.ent-fp strong{font-weight:500;color:#c9b37e}
.ent-sec p.ent-opc{font-family:'Jost',sans-serif;font-size:14.5px;font-weight:300;line-height:1.5;color:#ded6bf;border-top:1px solid #c9b37e40;margin:16px 0 0;padding:14px 0 0}
.ent-sec p.ent-nota{font-family:'Jost',sans-serif;font-size:12.5px;font-weight:400;line-height:1.5;color:#4a3d28;margin:14px 0 0}
@media (min-width:820px){.ent-sec{padding:70px 0}.ent-sec h2.ent-h{font-size:42px}.ent-card{padding:22px 24px 20px}.ent-sec h3.ent-t{font-size:30px}.ent-sec h3.ent-fh{font-size:36px}}
"""

def card(c):
    eb, nome, n, a, p, l, q = c
    return (
        '<article class="ent-card">'
        f'<p class="ent-eb">{e(eb)} · {n} aulas</p>'
        f'<h3 class="ent-t">{e(nome)}</h3>'
        f'<div class="ent-row"><p class="ent-l">Você assiste</p><p class="ent-v">{e(a)}</p></div>'
        f'<div class="ent-row"><p class="ent-l">Você preenche</p><p class="ent-v">{e(p)}</p></div>'
        f'<div class="ent-row"><p class="ent-l">Você leva</p><p class="ent-v">{e(l)}</p></div>'
        f'<p class="ent-pq"><strong>Para quê:</strong> {e(q)}</p>'
        '</article>')

FIM = (
    '<div class="ent-fim">'
    '<p class="ent-fk">O que você tem no final</p>'
    '<h3 class="ent-fh">O seu Dossiê de Desenvolvimento completo.</h3>'
    '<p class="ent-fp">As páginas de cada pilar reunidas em um só documento, com <strong>PDF no final</strong>: Território, Mercado, Produto, Modelo de Negócio, Masterplan, Pré-viabilidade e Capital.</p>'
    '<p class="ent-fp">Ele fica organizado para você apresentar a sócios, parceiros ou investidores, junto com o Kit do Investidor e as planilhas de cálculo.</p>'
    '<p class="ent-opc"><strong>Opcional:</strong> você pode cadastrar o seu terreno no banco de áreas da Zion. A Zion avalia cada caso. O cadastro não garante parceria nem investimento.</p>'
    '</div>')

def bloco(sec_id="entregaveis", css=True):
    body = (
        f'<section data-cx-section="solution" id="{sec_id}" class="sec ent-sec"><div class="w">'
        '<p class="ent-k">Entregáveis pilar a pilar</p>'
        '<h2 class="ent-h">O que você recebe em cada módulo.</h2>'
        '<p class="ent-intro">Em cada pilar são 2 vídeos, 1 ficha “Faça agora” e 1 página do seu Dossiê. Veja o que tem em cada um.</p>'
        '<div class="ent-lista">' + "".join(card(c) for c in CARDS) + '</div>'
        + FIM +
        '<p class="ent-nota">Material educativo. O resultado depende das informações e das premissas que você preencher. Não prometemos reservas, renda, investimento nem parceria.</p>'
        '</div></section>')
    return (f'<style>{CSS}</style>' if css else '') + body

if __name__ == "__main__":
    out = Path(__file__).with_name("bloco_entregaveis.html")
    h = bloco()
    out.write_text(h, encoding="utf-8")
    print(out, len(h), "bytes; span:", h.count("<span"), "script:", h.count("<script"), "base64:", h.count("base64"))

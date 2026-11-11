"""Diagramas do e-book 06 em SVG (desenhados por código; nenhuma imagem gerada por IA).
Paleta oficial Zion. Cada função devolve uma string <svg>."""
INK, MOSS, TERRA, OURO, AREIA, CREME = "#1B2117", "#1B2117", "#8B714E", "#C9B37E", "#DED6BF", "#FEF5F0"
F = "font-family:Aventa,Jost,sans-serif"
FD = "font-family:Cormorant,Georgia,serif"


def svg(w, h, corpo):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" style="width:100%;height:auto;display:block">{corpo}</svg>'


def t(x, y, s, size=13, cor=INK, anchor="start", peso=400, fam=F, italic=False):
    st = f"{fam};font-size:{size}px;font-weight:{peso}" + (";font-style:italic" if italic else "")
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{cor}" style="{st}">{s}</text>'


def ocupacao():
    # 30 noites (dados fictícios, iguais ao exemplo do cap. 1): 12 vendidas, 6 bloqueadas, 12 livres
    est = list("vvvllbbbbbbllvvvlllvvllvvvllvl")
    assert est.count("v") == 12 and est.count("b") == 6 and len(est) == 30
    cor = {"v": (MOSS, CREME), "l": ("#ffffff", INK), "b": (AREIA, TERRA)}
    c = ""
    for i, e in enumerate(est):
        x, y = 10 + (i % 10) * 52, 10 + (i // 10) * 52
        bg, fg = cor[e]
        c += f'<rect x="{x}" y="{y}" width="46" height="46" rx="6" fill="{bg}" stroke="{AREIA}"/>' + t(x + 23, y + 29, i + 1, 13, fg, "middle")
    leg = [("Vendida", MOSS), ("Livre", "#ffffff"), ("Bloqueada (fora da conta)", AREIA)]
    for i, (n, k) in enumerate(leg):
        c += f'<rect x="{10 + i * 150}" y="178" width="14" height="14" rx="3" fill="{k}" stroke="{AREIA}"/>' + t(30 + i * 150, 190, n, 12)
    c += t(10, 222, "Ocupação = 12 vendidas ÷ 24 disponíveis (30 − 6 bloqueadas) = 50%", 13, TERRA, peso=600)
    c += t(10, 240, "Dados fictícios.", 11, TERRA, italic=True)
    return svg(530, 250, c)


def jornada():
    et = [("Busca", "Tem para as minhas datas?"), ("Resultados", "Qual chama minha atenção?"), ("Anúncio", "É para mim? Vale o preço?"),
          ("Consulta", "Vão me responder bem?"), ("Reserva", "Posso confiar?")]
    c = ""
    for i, (n, q) in enumerate(et):
        x = 8 + i * 104
        c += f'<rect x="{x}" y="20" width="94" height="54" rx="27" fill="{MOSS if i == 4 else "#fff"}" stroke="{OURO}" stroke-width="1.5"/>'
        c += t(x + 47, 52, n, 14, CREME if i == 4 else INK, "middle", 600)
        if i < 4:
            c += f'<path d="M{x + 96} 47 h6" stroke="{OURO}" stroke-width="2"/>'
        words = q.split(" "); l1 = " ".join(words[:3]); l2 = " ".join(words[3:])
        c += t(x + 47, 100, l1, 11.5, TERRA, "middle", italic=True) + t(x + 47, 116, l2, 11.5, TERRA, "middle", italic=True)
    c += t(8, 146, "Em cada etapa o hóspede compara. A oferta precisa responder à pergunta daquela etapa.", 12, INK)
    return svg(530, 156, c)


def atributo_beneficio():
    c = ""
    cols = [("Atributo", "o que a hospedagem tem", "Varanda com rede"), ("Benefício", "o que o hóspede ganha", "Descansar olhando o mar"), ("Prova", "como ele confere", "Foto da rede ao pôr do sol")]
    for i, (n, d, ex) in enumerate(cols):
        x = 10 + i * 175
        c += f'<rect x="{x}" y="10" width="160" height="130" rx="12" fill="{"#fff" if i < 2 else MOSS}" stroke="{OURO}"/>'
        fg = CREME if i == 2 else INK
        c += t(x + 80, 44, n, 24, fg, "middle", fam=FD) + t(x + 80, 66, d, 11.5, OURO if i == 2 else TERRA, "middle")
        c += t(x + 80, 106, ex, 12.5, fg, "middle", 600)
        if i < 2:
            c += f'<path d="M{x + 162} 75 l10 0 m-5 -5 l5 5 l-5 5" stroke="{OURO}" stroke-width="2" fill="none"/>'
    c += t(10, 166, "Exemplo ilustrativo. Sem prova, o benefício vira adjetivo.", 12, TERRA, italic=True)
    return svg(530, 176, c)


def primeira_foto():
    seq = ["Chegada / fachada que explica", "Ambiente principal", "Quarto", "Banheiro", "Cozinha ou café", "O diferencial", "Área externa", "Detalhes de conforto", "Entorno / vista", "Planta ou mapa da casa"]
    c = ""
    for i, s in enumerate(seq):
        x, y = 10 + (i % 5) * 104, 10 + (i // 5) * 92
        dest = i == 0
        c += f'<rect x="{x}" y="{y}" width="96" height="62" rx="8" fill="{MOSS if dest else "#fff"}" stroke="{OURO}"/>'
        c += t(x + 10, y + 26, f"{i + 1:02d}", 22, OURO if dest else TERRA, fam=FD)
        w = s.split(" ")
        c += t(x + 4, y + 78, " ".join(w[:3]), 10.5, INK) + (t(x + 4, y + 90, " ".join(w[3:]), 10.5, INK) if len(w) > 3 else "")
    c += t(10, 202, "Ordem sugerida: a 1ª foto mostra a oferta; as seguintes respondem às dúvidas na ordem em que surgem.", 11.5, TERRA, italic=True)
    return svg(530, 212, c)


def preco_piso():
    partes = [("Custo variável por noite", "limpeza, lavanderia, amenidades ÷ noites", 75), ("Parte do custo fixo", "custo fixo do mês ÷ noites vendidas", 150), ("Margem mínima", "o que precisa sobrar", 40)]
    c = ""; x = 10
    tot = sum(p[2] for p in partes)
    cores = ["#fff", AREIA, OURO]
    for (n, d, v), k in zip(partes, cores):
        w = 380 * v / tot
        c += f'<rect x="{x}" y="20" width="{w - 4}" height="56" rx="6" fill="{k}" stroke="{TERRA}"/>' + t(x + 8, 44, f"R$ {v}", 15, INK, peso=600) + t(x + 8, 64, n, 10.5, INK)
        x += w
    c += t(x + 6, 44, "÷ (1 − 15% de", 12, TERRA) + t(x + 6, 62, "taxas e impostos)", 12, TERRA)
    c += f'<rect x="10" y="100" width="510" height="48" rx="8" fill="{MOSS}"/>' + t(24, 130, "Piso da diária = (75 + 150 + 40) ÷ 0,85 ≈ R$ 312", 16, CREME, peso=600)
    c += t(10, 172, "Dados fictícios. Abaixo do piso, cada noite vendida paga menos do que custa.", 12, TERRA, italic=True)
    return svg(530, 182, c)


def confianca():
    pil = [("Avaliações", "o que outros viveram"), ("Transparência", "limites ditos antes"), ("Informação", "dúvidas respondidas no anúncio"), ("Resposta", "rápida e igual para todos")]
    c = f'<path d="M20 34 L265 6 L510 34 Z" fill="{MOSS}"/>' + t(265, 28, "Confiança para reservar", 15, CREME, "middle", 600)
    for i, (n, d) in enumerate(pil):
        x = 30 + i * 122
        c += f'<rect x="{x}" y="44" width="104" height="96" fill="#fff" stroke="{OURO}"/>' + t(x + 52, 82, n, 14, INK, "middle", 600)
        dd = d.split(" "); c += t(x + 52, 104, " ".join(dd[:2]), 10.5, TERRA, "middle") + t(x + 52, 118, " ".join(dd[2:]), 10.5, TERRA, "middle")
    c += f'<rect x="20" y="146" width="490" height="12" fill="{AREIA}"/>' + t(265, 180, "Se um pilar falha, os outros precisam compensar.", 12, TERRA, "middle", italic=True)
    return svg(530, 190, c)


def funil():
    nv = [("Visualizações", "600", 500), ("Consultas", "18", 330), ("Reservas", "3", 170)]
    c = ""
    for i, (n, v, w) in enumerate(nv):
        x = 265 - w / 2; y = 10 + i * 56
        c += f'<rect x="{x}" y="{y}" width="{w}" height="46" rx="8" fill="{[ "#fff", AREIA, MOSS][i]}" stroke="{OURO}"/>'
        c += t(265, y + 29, f"{n} · {v}", 15, CREME if i == 2 else INK, "middle", 600)
    c += t(400, 72, "taxa de consulta 18 ÷ 600 = 3%", 11.5, TERRA) + t(370, 128, "taxa de reserva 3 ÷ 18 ≈ 16,7%", 11.5, TERRA)
    c += t(10, 196, "Dados fictícios. Cada etapa tem uma taxa: descubra onde o hóspede para.", 12, TERRA, italic=True)
    return svg(530, 206, c)


def radar(notas=(2, 3, 3, 4, 2, 4, 3)):
    import math
    nomes = ["Fotos e apresentação", "Título e descrição", "Preço e posicionamento", "Diferenciais e experiência", "Avaliações e confiança", "Atendimento e comunicação", "Conforto e infraestrutura"]
    cx, cy, R = 265, 150, 105; c = ""
    pt = lambda i, r: (cx + r * math.sin(2 * math.pi * i / 7), cy - r * math.cos(2 * math.pi * i / 7))
    for k in range(1, 6):
        c += '<polygon points="' + " ".join("%.1f,%.1f" % pt(i, R * k / 5) for i in range(7)) + f'" fill="none" stroke="{AREIA}"/>'
    for i in range(7):
        x, y = pt(i, R); c += f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{AREIA}"/>'
        lx, ly = pt(i, R + 22); a = "middle" if abs(lx - cx) < 20 else ("start" if lx > cx else "end")
        c += t(f"{lx:.1f}", f"{ly + 4:.1f}", nomes[i], 11, INK, a)
    c += '<polygon points="' + " ".join("%.1f,%.1f" % pt(i, R * n / 5) for i, n in enumerate(notas)) + f'" fill="{OURO}" fill-opacity=".45" stroke="{TERRA}" stroke-width="2"/>'
    c += t(265, 296, "Exemplo (dados fictícios): notas 2, 3, 3, 4, 2, 4, 3 · soma 21 · pontuação 60", 11.5, TERRA, "middle", italic=True)
    return svg(530, 306, c)


def gravidade_facilidade():
    c = f'<rect x="60" y="10" width="220" height="110" fill="{MOSS}"/><rect x="280" y="10" width="220" height="110" fill="#fff" stroke="{AREIA}"/>'
    c += f'<rect x="60" y="120" width="220" height="110" fill="#fff" stroke="{AREIA}"/><rect x="280" y="120" width="220" height="110" fill="{AREIA}"/>'
    c += t(170, 60, "Faça primeiro", 18, CREME, "middle", fam=FD) + t(170, 82, "pesa muito e é fácil", 11.5, OURO, "middle")
    c += t(390, 60, "Planeje", 18, INK, "middle", fam=FD) + t(390, 82, "pesa muito e dá trabalho", 11.5, TERRA, "middle")
    c += t(170, 170, "Encaixe na semana", 18, INK, "middle", fam=FD) + t(170, 192, "pesa pouco e é fácil", 11.5, TERRA, "middle")
    c += t(390, 170, "Deixe para depois", 18, INK, "middle", fam=FD) + t(390, 192, "pesa pouco e dá trabalho", 11.5, TERRA, "middle")
    c += t(30, 120, "Gravidade", 12, TERRA, "middle").replace("<text", '<text transform="rotate(-90 30 120)"')
    c += t(280, 252, "Facilidade  →  mais fácil à esquerda", 12, TERRA, "middle")
    return svg(530, 262, c)


def foco():
    c = ""
    for i, (p, n, d, w) in enumerate([("20%", "Prioridades", "as 3 menores notas", 500), ("4%", "Ação da semana", "uma, com prazo e indicador", 340), ("0,8%", "Primeiro passo", "menos de 1 hora, hoje", 180)]):
        x = 265 - w / 2; y = 10 + i * 62
        c += f'<rect x="{x}" y="{y}" width="{w}" height="52" rx="26" fill="{[ "#fff", AREIA, MOSS][i]}" stroke="{OURO}"/>'
        fg = CREME if i == 2 else INK
        c += t(x + 24, y + 34, p, 22, OURO if i == 2 else TERRA, fam=FD) + t(x + 24 + (62 if i < 2 else 0), y + 34 + (0 if i < 2 else 0), "", 1)
        if i < 2:
            c += t(x + 90, y + 24, n, 14, fg, peso=600) + t(x + 90, y + 41, d, 11.5, TERRA)
        else:
            c += t(x + 80, y + 24, n, 13, fg, peso=600) + t(x + 80, y + 40, d, 10.5, OURO)
    c += t(265, 206, "Heurística de foco da Zion, não promessa estatística.", 11.5, TERRA, "middle", italic=True)
    return svg(530, 214, c)


def semanas():
    s = [("Semana 1", "Diagnóstico e fotos"), ("Semana 2", "Texto e posicionamento"), ("Semana 3", "Preço e confiança"), ("Semana 4", "Medição e ajustes")]
    c = f'<line x1="20" y1="40" x2="510" y2="40" stroke="{OURO}" stroke-width="2"/>'
    for i, (a, b) in enumerate(s):
        x = 40 + i * 150
        c += f'<circle cx="{x}" cy="40" r="14" fill="{MOSS if i == 3 else "#fff"}" stroke="{OURO}" stroke-width="2"/>' + t(x, 45, i + 1, 13, CREME if i == 3 else INK, "middle", 600)
        c += t(x, 80, a, 14, INK, "middle", 600)
        bb = b.split(" e "); c += t(x, 100, bb[0] + " e", 11.5, TERRA, "middle") + t(x, 115, bb[1], 11.5, TERRA, "middle")
    c += t(20, 146, "Dia 30: refaça o Diagnóstico com a mesma base de datas e compare.", 12, INK, italic=True)
    return svg(530, 156, c)


def ciclo():
    import math
    et = ["Medir", "Decidir", "Executar", "Revisar"]; cx, cy, R = 265, 105, 72; c = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{OURO}" stroke-width="2" stroke-dasharray="6 6"/>'
    c += t(cx, cy - 4, "30 dias", 22, TERRA, "middle", fam=FD) + t(cx, cy + 16, "por ciclo", 11, TERRA, "middle")
    for i, n in enumerate(et):
        a = -math.pi / 2 + i * math.pi / 2; x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        c += f'<rect x="{x - 48:.1f}" y="{y - 17:.1f}" width="96" height="34" rx="17" fill="{MOSS}"/>' + t(f"{x:.1f}", f"{y + 5:.1f}", n, 14, CREME, "middle", 600)
    return svg(530, 210, c)


TODOS = {"ocupacao": ocupacao, "jornada": jornada, "atributo-beneficio": atributo_beneficio, "primeira-foto": primeira_foto, "preco-piso": preco_piso,
         "confianca": confianca, "funil": funil, "radar": radar, "gravidade-facilidade": gravidade_facilidade, "foco": foco, "semanas": semanas, "ciclo": ciclo}

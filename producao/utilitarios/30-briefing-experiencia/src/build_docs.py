"""Gera guia, modelos imprimíveis e demonstração da Ferramenta 30 com os textos REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from mensagens import CAMPOS, MENSAGENS, rotulo
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape; CRE = re.compile(r"\{(\w+)\}")
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Briefing-Experiencia-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Briefing-Experiencia-Zion-EXEMPLO.xlsx", data_only=True); M = W["Mensagens"]
MS = {M[f"A{6+i}"].value: dict(tit=M[f"B{6+i}"].value, quando=M[f"C{6+i}"].value, data=M[f"D{6+i}"].value, txt=M[f"E{6+i}"].value, st=M[f"F{6+i}"].value) for i in range(len(MENSAGENS))}
SIT = M["E3"].value; PRONTAS = M["C3"].value
EX = {c[0]: c[5] for c in CAMPOS}
CSS2 = CSS + ".aten{background:#FCE8B2} td.n{text-align:right;white-space:nowrap}"
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 30 · Gerador de Briefing de Experiência</span><span>{n}/{t}</span></div>'
def modelo(segs):
    txt = ""
    for sg in segs:
        if sg[0] == "t": txt += CRE.sub(lambda x: f"[{rotulo(x.group(1))}]", sg[1])
        elif sg[0] == "o": txt += " (se houver:" + CRE.sub(lambda x: f"[{rotulo(x.group(1))}]", sg[1]) + ")"
        elif sg[0] == "v": txt += " (se o grupo não informou restrições:" + sg[2] + ")"
    return txt

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-briefing.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:14mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-mensagens.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:28mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 30 · Guia do comprador</div><h1 style="color:var(--creme)">Gerador de Briefing de Experiência</h1>
<p style="font-size:13pt;max-width:160mm">Aprenda o passo a passo para escrever o briefing da sua experiência uma vez e gerar, para cada saída, a descrição, as mensagens ao cliente e o briefing de quem conduz.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas, glampings e quem oferece experiências. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem oferece uma experiência junto com a hospedagem (trilha, café especial, passeio, aula, jantar) e repete as mesmas explicações a cada cliente, ao guia e ao parceiro.<br>
<b>Quando usar:</b> uma vez para escrever o briefing; depois, a cada saída marcada.</div>
<h3>Você termina com</h3><ol class="passos"><li>O briefing completo da experiência: o que é, duração, ponto de encontro, o que inclui, o que levar, para quem é, clima, mínimo e cancelamento.</li>
<li>Oito textos montados para cada saída, com a data certa de envio.</li><li>Um aviso sempre que falta uma informação, em vez de um texto incompleto.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja as abas Ficha e Mensagens.</li>
<li>Na versão em branco, escreva o briefing da sua experiência.</li><li>Na próxima saída, preencha cliente, data, horário e participantes, e siga as datas de envio.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Briefing-Experiencia-Zion-EM-BRANCO.xlsx</td><td>Sua ficha e os 8 textos montados</td></tr>
<tr><td>Briefing-Experiencia-Zion-EXEMPLO.xlsx</td><td>Uma experiência e uma saída fictícias, com os 8 textos prontos</td></tr>
<tr><td>Mensagens-Modelo-Experiencia.pdf</td><td>Os 8 modelos com campos entre colchetes, para copiar à mão</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    trs = "".join(f"<tr><td>{E(r)}{' *' if o else ''}</td><td style='font-size:8.6pt'>{E(a)}</td></tr>" for k, r, s, o, a, x in CAMPOS if s == "H")
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · o briefing da experiência</div><h2>Escreva uma vez, com cuidado</h2>
<p>A parte de cima da Ficha é o briefing: tudo o que o cliente e quem conduz precisam saber. Campos com * são obrigatórios; os opcionais vazios somem das frases.</p>
<table style="font-size:9pt"><tr><th style="width:42%">Campo</th><th>Como preencher</th></tr>{trs}</table>
<div class="box alerta"><b>Segurança e regras:</b> trilha, passeio de barco, cavalgada ou aula com equipamento podem exigir guia habilitado, seguro e autorizações. Confira com quem regula a atividade antes de vender.</div>{foot(3,T)}</section>""")
    b01 = MS["B01"]
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · a descrição</div><h2>Um texto que responde as perguntas antes delas</h2>
<p>O texto B01 junta o briefing numa descrição pronta para o anúncio, o cardápio de experiências ou para quem pergunta pelo WhatsApp.</p>
<div class="box ex"><span class="tag">B01 · Exemplo · dados fictícios</span><div class="bolha">{E(b01['txt'])}</div></div>
<div class="box"><b>Por que deixar mínimo, clima e cancelamento já na descrição:</b> o cliente sabe as regras antes de pagar, e você não precisa explicar no dia.</div>
<div class="box"><b>Exercício 1.</b> Escreva em uma frase o que acontece na sua experiência, como no campo "O que acontece, em uma frase":<div class="linha"></div><div class="linha"></div></div>{foot(4,T)}</section>""")
    tr = "".join(f"<tr><td>{k}</td><td>{E(v['tit'])}</td><td>{E(v['quando'])}</td><td class='n'>{E(str(v['data']))}</td></tr>" for k, v in MS.items())
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · cada saída</div><h2>Cliente, data, horário e participantes</h2>
<p>Na parte de baixo da Ficha, preencha os dados da saída. A planilha calcula a data de envio de cada texto e diz se o mínimo foi atingido.</p>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · saída em 12/12/2026, {EX['pessoas']} participantes, mínimo {EX['minimo']}</span>
<table style="margin-top:8px;font-size:9pt"><tr><th>Nº</th><th>Texto</th><th>Quando enviar</th><th>Data</th></tr>{tr}</table>
<p style="font-size:9.5pt;margin:6px 0 0">Situação da saída: <b>{E(SIT)}</b></p></div>
<div class="box"><b>Mínimo:</b> dois dias antes, use a B03 se o mínimo foi atingido e a B04 se não foi. A B04 oferece sempre remarcar ou devolver o valor.</div>{foot(5,T)}</section>""")
    b06 = MS["B06"]
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · o briefing de quem conduz</div><h2>O guia chega sabendo tudo</h2>
<p>O texto B06 vai na véspera para o guia ou parceiro: horário, ponto, número de pessoas, o que está incluído e as restrições informadas pelo grupo.</p>
<div class="box ex"><span class="tag">B06 · Exemplo · dados fictícios</span><div class="bolha">{E(b06['txt'])}</div></div>
<div class="box"><b>Restrições:</b> quando o grupo não informa nada, o texto pede para confirmar no encontro, em vez de supor que está tudo bem.</div>
<div class="box"><b>Exercício 2.</b> Escreva o que o seu guia mais pergunta na véspera e confira se o briefing responde:<div class="linha"></div><div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Briefing completo</td><td>A aba Mensagens mostra 8 de 8 prontos com só a parte de cima preenchida e uma saída de teste</td></tr>
<tr><td>Regras claras</td><td>Mínimo, clima e cancelamento aparecem na descrição e na confirmação</td></tr>
<tr><td>Calendário</td><td>B03 ou B04 dois dias antes; B05 e B06 na véspera; B08 no dia</td></tr>
<tr><td>Nenhum colchete</td><td>Nenhum texto enviado com [PREENCHA]</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Escrevi o briefing &nbsp; ☐ Fiz uma saída de teste com 8 de 8 prontos &nbsp; ☐ Mandei a descrição para quem vende<br>
☐ Combinei com o guia o horário do briefing &nbsp; ☐ Defini o que faço abaixo do mínimo</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>Monta os textos com o que você escreve: não verifica se a atividade é segura nem se tem as autorizações.</li>
<li>Não calcula custos nem o mínimo: para isso existe a Calculadora de Custos de Experiências (Ferramenta 29), vendida à parte.</li>
<li>Uma experiência por arquivo (duplique o arquivo para cada experiência).</li>
<li>Não garante vendas, reservas nem avaliações.</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplos com experiência, pessoas, telefone e preço fictícios. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def modelos():
    blocos = "".join(f'<div class="box" style="margin:6px 0;padding:8px 12px"><b style="font-size:9.5pt">{mid} · {E(tit)}</b> <span style="font-size:8.5pt;color:#6b6656">· {E(q)}</span><div style="font-size:9pt;margin-top:3px">{E(modelo(segs))}</div></div>'
                     for mid, tit, q, r, segs in MENSAGENS)
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:11mm}} body{{background:#fff}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 30</div>
<h2 style="font-size:21pt">Modelos de texto da experiência</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<p style="font-size:9pt">Troque o que está entre colchetes. Os trechos "(se houver: ...)" só entram se você tiver a informação. Nunca envie com colchetes.</p>{blocos}</body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Briefing de Experiência · Ferramenta 30</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Texto montado pela planilha da Ferramenta 30.</div></body></html>"""
lin = lambda a, b, c="": f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;white-space:nowrap;font-weight:600;align-self:center">{b}</span></div>'
lista = "".join(lin(f"{k} · {E(v['tit'][:26])}{'…' if len(v['tit']) > 26 else ''}", E(str(v['data'])) if str(v['data'])[:1].isdigit() else "Sob demanda", "ok" if str(v['data'])[:1].isdigit() else "aten") for k, v in MS.items())
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(modelos(), encoding="utf-8")
(BUILD / "demo-briefing.html").write_text(demo("B06 · Briefing de quem conduz", "Pronto para copiar", "#C8E6C0",
    f'<div style="padding:14px"><div class="bolha" style="font-size:12.5px">{E(MS["B06"]["txt"])}</div></div>'), encoding="utf-8")
(BUILD / "demo-mensagens.html").write_text(demo("Textos desta saída", f"{PRONTAS} prontos · {SIT.split(':')[0]}", "#FCE8B2", lista), encoding="utf-8")
print(PRONTAS, SIT)

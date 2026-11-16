"""Gera guia, modelos imprimíveis e demonstração da Ferramenta 23 com os roteiros REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from roteiros import CAMPOS, MENSAGENS, rotulo
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape; CRE = re.compile(r"\{(\w+)\}")
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Roteiros-Conteudo-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Roteiros-Conteudo-Zion-EXEMPLO.xlsx", data_only=True); M = W["Roteiros"]
MS = {M[f"A{6+i}"].value: dict(tit=M[f"B{6+i}"].value, obj=M[f"C{6+i}"].value, data=M[f"D{6+i}"].value, txt=M[f"E{6+i}"].value, st=M[f"F{6+i}"].value) for i in range(len(MENSAGENS))}
CAL = M["E3"].value; PRONTOS = M["C3"].value
CSS2 = CSS + ".aten{background:#FCE8B2} td.n{text-align:right;white-space:nowrap} .rot{white-space:pre-line}"
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 23 · Kit de Roteiros de Conteúdo e Vídeos</span><span>{n}/{t}</span></div>'
def modelo(segs):
    txt = ""
    for sg in segs:
        if sg[0] == "t": txt += CRE.sub(lambda x: f"[{rotulo(x.group(1))}]", sg[1])
        elif sg[0] == "o": txt += "(se houver: " + CRE.sub(lambda x: f"[{rotulo(x.group(1))}]", sg[1]) + ")"
        elif sg[0] == "v": txt += "\n(se não houver passeios por perto: " + sg[2] + ")"
    return txt
def rot(txt): return f'<div class="bolha rot">{E(txt)}</div>'

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-roteiro.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:14mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-calendario.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:28mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 23 · Guia do comprador</div><h1 style="color:var(--creme)">Kit de Roteiros de Conteúdo e Vídeos</h1>
<p style="font-size:13pt;max-width:160mm">Aprenda o passo a passo para preencher uma ficha da sua hospedagem e receber 8 roteiros curtos de vídeo, com gancho, cenas, texto na tela, legenda e o dia de postar cada um.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas e glampings. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem sabe que precisa postar vídeos da hospedagem, mas trava na hora de decidir o que gravar e o que escrever.<br>
<b>Quando usar:</b> uma vez para preencher a ficha; depois, a cada ciclo de 8 vídeos (mude a data de início e grave de novo, com outras cenas).</div>
<h3>Você termina com</h3><ol class="passos"><li>Uma ficha da hospedagem com o que diferencia o lugar, para quem é e para quem não é.</li>
<li>Oito roteiros de 15 a 30 segundos, cada um com um objetivo diferente.</li><li>Um calendário de postagem com a data de cada vídeo.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja as abas Ficha e Roteiros.</li>
<li>Na versão em branco, preencha a ficha da sua hospedagem (cerca de 15 minutos).</li><li>Grave o primeiro vídeo no dia indicado, com o celular na vertical.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Roteiros-Conteudo-Zion-EM-BRANCO.xlsx</td><td>Sua ficha, os 8 roteiros montados e o calendário</td></tr>
<tr><td>Roteiros-Conteudo-Zion-EXEMPLO.xlsx</td><td>Uma hospedagem fictícia com os 8 roteiros prontos</td></tr>
<tr><td>Roteiros-Modelo.pdf</td><td>Os 8 roteiros com campos entre colchetes, para usar sem planilha</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    trs = "".join(f"<tr><td>{E(r)}{' *' if o else ''}</td><td style='font-size:8.6pt'>{E(a)}</td></tr>" for k, r, s, o, a, x in CAMPOS if s == "H")
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · a ficha</div><h2>Diga o que só a sua hospedagem tem</h2>
<p>Os roteiros são montados com o que você escreve. Quanto mais concreto, melhor o vídeo: "banheira com vista para o vale" diz mais que "lugar lindo".</p>
<table style="font-size:9pt"><tr><th style="width:40%">Campo</th><th>Como preencher</th></tr>{trs}</table>
<div class="box"><b>Exercício 1.</b> Escreva o que os hóspedes mais elogiam nas avaliações. Esse é o seu diferencial principal:<div class="linha"></div></div>{foot(3,T)}</section>""")
    v1 = MS["V01"]
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · como ler um roteiro</div><h2>Gancho, cenas, texto, legenda e chamada</h2>
<table style="font-size:9.5pt"><tr><th>Parte</th><th>Para que serve</th></tr>
<tr><td>Gancho (0 a 3 s)</td><td>A primeira frase, dita ou escrita, para a pessoa parar de rolar a tela</td></tr>
<tr><td>Cenas</td><td>A ordem das imagens; cada cena dura de 2 a 4 segundos</td></tr>
<tr><td>Texto na tela</td><td>A frase curta que aparece por cima do vídeo</td></tr>
<tr><td>Legenda</td><td>O texto do post</td></tr><tr><td>Chamada</td><td>Onde a pessoa reserva</td></tr></table>
<div class="box ex"><span class="tag">V01 · Exemplo · dados fictícios</span>{rot(v1['txt'])}</div>{foot(4,T)}</section>""")
    tr = "".join(f"<tr><td>{k}</td><td>{E(v['tit'])}</td><td>{E(v['obj'])}</td><td class='n'>{E(str(v['data']))}</td></tr>" for k, v in MS.items())
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · o calendário</div><h2>Oito vídeos, oito objetivos</h2>
<p>Na parte de baixo da Ficha, escolha a data do primeiro vídeo e de quantos em quantos dias vai postar. A planilha calcula o dia de cada um.</p>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · um vídeo a cada 3 dias</span>
<table style="margin-top:8px;font-size:9pt"><tr><th>Nº</th><th>Formato</th><th>Objetivo</th><th>Data</th></tr>{tr}</table>
<p style="font-size:9.5pt;margin:6px 0 0"><b>{E(CAL)}</b></p></div>
<div class="box"><b>Constância vale mais que quantidade:</b> escolha um intervalo que você consegue manter. Um vídeo a cada 3 ou 4 dias é melhor que 8 numa semana e nada depois.</div>{foot(5,T)}</section>""")
    v6 = MS["V06"]
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · gravar e postar</div><h2>Grave simples, com cuidado</h2>
<ol class="passos"><li>Celular na vertical, lente limpa, luz natural.</li><li>Grave cada cena separada, com 2 a 4 segundos de sobra no começo e no fim.</li>
<li>Monte no próprio aplicativo da rede social, coloque o texto na tela e cole a legenda.</li><li>Releia: nenhum [PREENCHA] e nada que a casa não tenha.</li></ol>
<div class="box alerta"><b>Pessoas e músicas:</b> não mostre hóspedes nem rostos sem autorização por escrito; use só as músicas que a própria rede social libera.</div>
<div class="box ex"><span class="tag">V06 · Exemplo · dados fictícios</span>{rot(v6['txt'])}</div>
<div class="box"><b>Exercício 2.</b> Para quem a sua hospedagem não é? Escrever isso ajuda a atrair o hóspede certo.<div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Ficha completa</td><td>A aba Roteiros mostra 8 de 8 prontos</td></tr>
<tr><td>Verdade</td><td>Tudo o que aparece nos vídeos existe na hospedagem</td></tr>
<tr><td>Constância</td><td>Os 8 vídeos postados nas datas do calendário</td></tr>
<tr><td>Aprendizado</td><td>Você anotou quais formatos geraram mais perguntas e repete no próximo ciclo</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Preenchi a ficha &nbsp; ☐ Escolhi data e intervalo que consigo manter &nbsp; ☐ Gravei o primeiro vídeo<br>
☐ Postei os 8 nas datas &nbsp; ☐ Anotei o que gerou mais perguntas &nbsp; ☐ Comecei o próximo ciclo</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>Os roteiros organizam o que gravar e escrever; não garantem seguidores, alcance nem reservas.</li>
<li>Não edita vídeos e não publica nada: você grava e posta.</li>
<li>Os roteiros usam o que você escreve na ficha; revise sempre antes de postar.</li>
<li>Regras de cada rede social (músicas, direitos de imagem) mudam: confira antes de publicar.</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplos com hospedagem e lugar fictícios. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def modelos():
    blocos = "".join(f'<div class="box" style="margin:5px 0;padding:7px 11px"><b style="font-size:9.5pt">{mid} · {E(tit)}</b> <span style="font-size:8.5pt;color:#6b6656">· {E(obj)}</span><div class="rot" style="font-size:8.3pt;margin-top:3px">{E(modelo(segs))}</div></div>'
                     for mid, tit, obj, r, segs in MENSAGENS)
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:9mm}} body{{background:#fff}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 23</div>
<h2 style="font-size:20pt;margin:0">Roteiros-modelo de vídeo</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:12mm"></div>
<p style="font-size:8.5pt;margin:4px 0">Troque o que está entre colchetes. Os trechos "(se houver: ...)" só entram se você tiver a informação. Nunca publique com colchetes.</p>{blocos}</body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Roteiros de Conteúdo · Ferramenta 23</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Roteiro montado pela planilha da Ferramenta 23.</div></body></html>"""
lin = lambda a, b, c="": f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;white-space:nowrap;font-weight:600;align-self:center">{b}</span></div>'
lista = "".join(lin(f"{k} · {E(v['tit'])}", E(str(v['data'])[:5]), "ok") for k, v in MS.items())
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(modelos(), encoding="utf-8")
(BUILD / "demo-roteiro.html").write_text(demo("V03 · Uma manhã aqui", "Pronto para gravar", "#C8E6C0",
    f'<div style="padding:14px">{rot(MS["V03"]["txt"])}</div>'), encoding="utf-8")
(BUILD / "demo-calendario.html").write_text(demo("Calendário de postagem", f"{PRONTOS} prontos · a cada 3 dias", "#FCE8B2", lista), encoding="utf-8")
print(PRONTOS, CAL)

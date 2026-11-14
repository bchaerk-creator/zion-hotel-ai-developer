"""Gera guia, roteiro do dia das fotos e demonstração da Ferramenta 12 com valores REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from dados import FOTOS, COMODIDADES
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Fotos-Comodidades-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Fotos-Comodidades-Zion-EXEMPLO.xlsx", data_only=True)
FO, CO, P = W["Fotos"], W["Comodidades"], W["Painel"]
FOT = [[FO[f"{c}{r}"].value for c in "ABCDEFG"] for r in range(6, 66) if FO[f"B{r}"].value]
COM = [[CO[f"{c}{r}"].value for c in "ABCDEFG"] for r in range(6, 66) if CO[f"A{r}"].value]
PAI = {P[f"A{r}"].value: P[f"B{r}"].value for r in range(4, 18) if P[f"B{r}"].value is not None}
LEIT = next(P[f"A{r}"].value for r in range(16, 22) if P[f"A{r-1}"].value == "O que fazer primeiro")
cls = lambda s: {"OK": "ok", "Remover do anúncio": "pend", "Marcar no anúncio": "aten", "Falta foto": "aten", "Obrigatória ainda não aprovada": "aten",
                 "Não se aplica": ""}.get(s, "pend" if s else "")
CSS2 = CSS + ".aten{background:#FCE8B2}"
num = lambda v: "" if v in (None, "") else (str(int(v)) if isinstance(v, (int, float)) else str(v))
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 12 · Checklist de Fotos e Comodidades do Anúncio</span><span>{n}/{t}</span></div>'

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-fotos.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:16mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-comodidades.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:30mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 12 · Guia do comprador</div><h1 style="color:var(--creme)">Checklist de Fotos e Comodidades do Anúncio</h1>
<p style="font-size:13pt;max-width:155mm">Aprenda o passo a passo para planejar as fotos do seu anúncio, acompanhar cada uma até a publicação e conferir se o que está marcado no anúncio existe de verdade na hospedagem.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas e glampings. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem vai criar ou refazer o anúncio e quer chegar ao dia das fotos com uma lista, sem esquecer o banheiro ou a vista, e sem marcar comodidade que a casa não tem.<br>
<b>Quando usar:</b> antes de fotografar, no dia das fotos e a cada mudança na casa (um item novo, um item que quebrou).</div>
<h3>Você termina com</h3><ol class="passos"><li>Uma lista das fotos do anúncio, com as obrigatórias marcadas e a ordem de cada uma.</li>
<li>A situação de cada foto, de "falta tirar" até "publicada".</li>
<li>Uma conferência das comodidades: o que existe, o que está marcado no anúncio e o que tem foto.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja a aba Painel.</li>
<li>Na versão em branco, ajuste a lista de fotos e responda as comodidades andando pela casa (cerca de 30 minutos).</li><li>Leve o Roteiro do dia das fotos impresso ou no celular.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Fotos-Comodidades-Zion-EM-BRANCO.xlsx</td><td>Sua planilha: {len(FOTOS)} fotos e {len(COMODIDADES)} comodidades sugeridas (até 60 de cada)</td></tr>
<tr><td>Fotos-Comodidades-Zion-EXEMPLO.xlsx</td><td>Um chalé fictício com fotos em andamento e comodidades conferidas</td></tr>
<tr><td>Roteiro-do-Dia-das-Fotos.pdf</td><td>A lista para levar no dia, com caixas para marcar</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · aba Fotos</div><h2>Planeje as fotos antes de fotografar</h2>
<p>A lista sugerida cobre o que quase todo hóspede quer ver: como é chegar, onde dorme, onde toma banho, onde cozinha e o que tem do lado de fora. Ajuste à sua casa:</p>
<ol class="passos"><li><b>Apague</b> o que não existe (sem segundo quarto, sem piscina).</li><li><b>Acrescente</b> o que diferencia a sua hospedagem: uma vista, uma banheira, um detalhe que você ouve elogiarem.</li>
<li><b>Marque como obrigatória</b> a foto sem a qual o hóspede não consegue decidir. A planilha só considera pronta a obrigatória que estiver Aprovada ou Publicada.</li></ol>
<div class="box"><b>Dicas práticas para o dia:</b> casa limpa e arrumada como para um hóspede; luz natural, cortinas abertas e luzes acesas; fotos na horizontal, do canto do ambiente, na altura do peito; uma foto por ideia; nada pessoal à vista.</div>
<div class="box"><b>Exercício 1.</b> Escreva o detalhe da sua hospedagem que os hóspedes mais comentam. Ele tem uma foto só dele?<div class="linha"></div></div>{foot(3,T)}</section>""")
    tr = "".join(f"<tr><td>{E(str(f[0]))}</td><td>{E(str(f[1]))}</td><td>{E(str(f[2]))}</td><td>{E(str(f[3] or ''))}</td><td>{num(f[4])}</td><td class='{cls(f[6])}'>{E(str(f[6]))}</td></tr>" for f in FOT)
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · situação e ordem</div><h2>Acompanhe cada foto até a publicação</h2>
<table><tr><th>Situação</th><th>Quer dizer</th></tr><tr><td>Falta tirar</td><td>Ainda não fotografada (em branco conta assim)</td></tr><tr><td>Tirada</td><td>Fotografada, mas você ainda não escolheu a melhor</td></tr>
<tr><td>Aprovada</td><td>Escolhida, pronta para subir</td></tr><tr><td>Publicada</td><td>Está no anúncio; precisa de ordem</td></tr></table>
<div class="box ex" style="margin-top:8px"><span class="tag">Exemplo · dados fictícios · chalé</span><table style="margin-top:8px;font-size:8.5pt"><tr><th>Ambiente</th><th>Foto</th><th>Obrig.</th><th>Situação</th><th>Ordem</th><th>Alerta</th></tr>{tr}</table>
<p style="font-size:9pt;margin:6px 0 0">As duas fotos do banheiro estão com a ordem 6: a planilha avisa. A área externa é obrigatória e ainda falta tirar.</p></div>{foot(4,T)}</section>""")
    sel = [c for c in COM if c[6] != "OK"]
    tr = "".join(f"<tr><td>{E(str(c[0]))}</td><td>{E(str(c[3] or '—'))}</td><td>{E(str(c[4] or '—'))}</td><td>{E(str(c[5] or '—'))}</td><td class='{cls(c[6])}'>{E(str(c[6]))}</td></tr>" for c in sel)
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · aba Comodidades</div><h2>Confira a casa contra o anúncio</h2>
<p>Ande pela casa com a planilha aberta no celular. Para cada comodidade, responda três perguntas: existe aqui? Está marcada no anúncio? Tem foto?</p>
<table><tr><th>Situação</th><th>O que fazer</th></tr>
<tr><td class="pend">Remover do anúncio</td><td>Está marcada e não existe: tire hoje. O hóspede vai procurar.</td></tr>
<tr><td class="aten">Marcar no anúncio</td><td>Existe e não está marcada: marque.</td></tr>
<tr><td class="aten">Falta foto</td><td>É destaque (hidro, lareira, vaga) e não tem foto: inclua na lista de fotos.</td></tr>
<tr><td>Não se aplica</td><td>Não existe e não está marcada: nada a fazer.</td></tr></table>
<div class="box ex" style="margin-top:8px"><span class="tag">Exemplo · o que não está OK</span><table style="margin-top:8px;font-size:9pt"><tr><th>Comodidade</th><th>Existe</th><th>Marcada</th><th>Foto</th><th>Situação</th></tr>{tr}</table></div>{foot(5,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · aba Painel</div><h2>Comece pelo que mais importa</h2>
<p>O painel junta tudo e diz o que fazer primeiro, nesta ordem: tirar do anúncio o que não existe, resolver os alertas das fotos, marcar o que existe, fotografar os destaques e responder o que ficou em branco.</p>
<div class="box ex"><span class="tag">Exemplo · dados fictícios</span><table style="margin-top:8px">
<tr><td>Obrigatórias aprovadas ou publicadas</td><td><b>{PAI['Obrigatórias aprovadas ou publicadas']} de {PAI['Fotos obrigatórias']}</b></td></tr>
<tr><td>Fotos publicadas</td><td>{PAI['Fotos publicadas']} de {PAI['Fotos na lista']}</td></tr><tr><td>Fotos com alerta</td><td>{PAI['Fotos com alerta']}</td></tr>
<tr><td>Remover do anúncio</td><td>{PAI['Remover do anúncio (marcada e não existe)']}</td></tr><tr><td>Marcar no anúncio</td><td>{PAI['Marcar no anúncio (existe e não está marcada)']}</td></tr>
<tr><td>Falta foto de destaque</td><td>{PAI['Falta foto de comodidade de destaque']}</td></tr><tr><td>Sem resposta</td><td>{PAI['Sem resposta']}</td></tr></table>
<p style="margin:8px 0 0"><b>O que fazer primeiro:</b> {E(LEIT)}</p></div>
<div class="box"><b>Exercício 2.</b> Abra o seu anúncio agora e conte quantas comodidades estão marcadas. Quantas você confirmaria olhando cada uma na casa?<div class="linha"></div><div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Anúncio honesto</td><td>"Remover do anúncio" igual a 0</td></tr><tr><td>Fotos essenciais</td><td>Todas as obrigatórias Aprovadas ou Publicadas</td></tr>
<tr><td>Ordem clara</td><td>Nenhuma ordem repetida; a capa é a ordem 1</td></tr><tr><td>Conferência viva</td><td>Planilha revista a cada item novo ou quebrado</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Ajustei a lista de fotos &nbsp; ☐ Marquei as obrigatórias &nbsp; ☐ Fotografei com o roteiro<br>
☐ Publiquei com a ordem certa &nbsp; ☐ Conferi as comodidades na casa &nbsp; ☐ Corrigi o anúncio pelo painel</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>A planilha não tira, não edita nem sobe fotos, e não acessa o seu anúncio.</li>
<li>Não sabe como cada plataforma ordena ou mostra as comodidades; confira a lista da sua plataforma.</li>
<li>Foto boa não garante reserva: o anúncio também depende de preço, localização, avaliações e calendário.</li>
<li>Para diagnosticar o anúncio inteiro, a Zion tem produtos separados; esta ferramenta cuida só de fotos e comodidades.</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplos com um chalé fictício. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def roteiro():
    lin = "".join(f"<tr><td>☐</td><td>{E(a)}</td><td>{E(b)}</td><td>{'Sim' if c == 'Sim' else ''}</td><td></td></tr>" for a, b, c in FOTOS)
    lin += "".join("<tr><td>☐</td><td>&nbsp;</td><td></td><td></td><td></td></tr>" for _ in range(3))
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:11mm}} body{{background:#fff}} td{{height:21px;font-size:9pt}} th{{font-size:8.5pt}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 12</div>
<h2 style="font-size:21pt;margin:0">Roteiro do dia das fotos</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:12mm"></div>
<div class="box" style="font-size:9pt;margin:6px 0">Antes: casa limpa e arrumada como para um hóspede · cortinas abertas e luzes acesas · objetos pessoais guardados · celular com a lente limpa. Durante: horizontal, do canto, na altura do peito, uma foto por ideia.</div>
<table><tr><th style="width:6%">Feita</th><th style="width:16%">Ambiente</th><th>O que a foto mostra</th><th style="width:10%">Obrig.</th><th style="width:16%">Observação</th></tr>{lin}</table>
<p style="font-size:8pt;color:#6b6656;margin-top:6px">Depois, marque cada foto como Tirada na aba Fotos e escolha as melhores (Aprovada).</p></body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Fotos e Comodidades · Ferramenta 12</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Valores calculados pela planilha da Ferramenta 12.</div></body></html>"""
lin = lambda a, b, c: f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;white-space:nowrap">{b}</span></div>'
fot = "".join(lin(f"{E(str(f[0]))}<br><small>{E(str(f[3] or 'Falta tirar'))}{(' · ordem ' + num(f[4])) if f[4] else ''}</small>", E(str(f[6]).replace('Obrigatória ainda não aprovada', 'Obrigatória pendente')), cls(f[6])) for f in ([f for f in FOT if f[6] != 'OK'] + [f for f in FOT if f[6] == 'OK'])[:7])
com = "".join(lin(E(str(c[0])), E(str(c[6]).replace('Responda: existe e está marcada?', 'Responda')), cls(c[6])) for c in COM if c[6] not in ("OK", "Não se aplica"))
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(roteiro(), encoding="utf-8")
(BUILD / "demo-fotos.html").write_text(demo("Fotos do anúncio", f"{PAI['Obrigatórias aprovadas ou publicadas']} de {PAI['Fotos obrigatórias']} obrigatórias prontas", "#FCE8B2", fot), encoding="utf-8")
(BUILD / "demo-comodidades.html").write_text(demo("Casa × anúncio", f"{PAI['Remover do anúncio (marcada e não existe)']} para remover · {PAI['Marcar no anúncio (existe e não está marcada)']} para marcar", "#F4C7C3", com), encoding="utf-8")
print(PAI, LEIT)

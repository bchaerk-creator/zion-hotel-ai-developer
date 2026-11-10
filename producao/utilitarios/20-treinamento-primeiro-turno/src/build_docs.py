"""Gera guia, ficha do primeiro turno e demonstração da Ferramenta 20 com valores REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html, datetime as dt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from dados import ETAPAS, SUGERIDAS, EX, T0
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Treinamento-Primeiro-Turno-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Treinamento-Primeiro-Turno-Zion-EXEMPLO.xlsx", data_only=True)
TR, S = W["Treinamento"], W["Painel"]
dv = lambda v: v.date() if isinstance(v, dt.datetime) else v
dbr = lambda v: dv(v).strftime("%d/%m") if isinstance(dv(v), dt.date) else "—"
LIN = [dict(n=TR[f"A{r}"].value, e=TR[f"B{r}"].value, t=TR[f"C{r}"].value, ob=TR[f"D{r}"].value, f=TR[f"F{r}"].value, g=TR[f"G{r}"].value,
            h=TR[f"H{r}"].value, prazo=TR[f"J{r}"].value, sit=TR[f"K{r}"].value) for r in range(T0, T0 + len(SUGERIDAS))]
PAN = {k: S[f"B{l}"].value for k, l in (("tot", 5), ("prontas", 6), ("ob", 7), ("obok", 8), ("falta", 9), ("pct", 10), ("atr", 11), ("conf", 12), ("prox", 13), ("lib", 14))}
ETP = [(S[f"A{18+i}"].value, S[f"B{18+i}"].value) for i in range(len(ETAPAS))]
cls = lambda s: {"Pronta": "ok", "Atrasada": "pend", "Feita junto": "azul", "Mostrada": "aten"}.get(s, "pend" if "confira" in str(s) else "cinza")
CSS2 = CSS + ".aten{background:#FCE8B2} .cinza{background:#E6E6E6} .azul{background:#D6E4F0} td.n{text-align:right;white-space:nowrap}"
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 20 · Kit de Treinamento do Primeiro Turno</span><span>{n}/{t}</span></div>'
pct = f"{PAN['pct']*100:.0f}%" if isinstance(PAN['pct'], (int, float)) else "—"

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-tarefas.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:14mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-painel.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:28mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 20 · Guia do comprador</div><h1 style="color:var(--creme)">Kit de Treinamento do Primeiro Turno</h1>
<p style="font-size:13pt;max-width:160mm">Aprenda o passo a passo para treinar a primeira pessoa da sua equipe: o que mostrar, o que fazer junto e quando ela pode trabalhar sozinha.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas e glampings. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem vai colocar a primeira pessoa para limpar, receber hóspedes ou cuidar da manutenção, e quer que ela faça do jeito da casa, sem depender de você para cada detalhe.<br>
<b>Quando usar:</b> na semana em que a pessoa começa, e de novo a cada pessoa nova ou função nova.</div>
<h3>Você termina com</h3><ol class="passos"><li>A lista do que a pessoa precisa aprender, em seis etapas, com prazo e o que é obrigatório.</li>
<li>O registro de cada tarefa: quando foi mostrada, feita junto e feita sozinha, e quem conferiu.</li><li>Um critério claro para liberar o primeiro turno sozinha: todas as obrigatórias prontas.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja as abas Treinamento e Painel.</li>
<li>Na planilha em branco, ajuste a lista à sua hospedagem e à função.</li><li>Use a Ficha do Primeiro Turno no dia e passe as datas para a planilha.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Treinamento-Primeiro-Turno-Zion-EM-BRANCO.xlsx</td><td>Seu plano, com {len(SUGERIDAS)} tarefas sugeridas em 6 etapas</td></tr>
<tr><td>Treinamento-Primeiro-Turno-Zion-EXEMPLO.xlsx</td><td>Uma pessoa fictícia no quarto dia de treinamento</td></tr>
<tr><td>Ficha-do-Primeiro-Turno.pdf</td><td>Roteiro do primeiro dia e conferência para imprimir</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    trs = "".join(f"<tr><td><b>{E(e)}</b></td><td>{E('; '.join(t for x, t, o, z in SUGERIDAS if ETAPAS[x-1] == e))}</td></tr>" for e in ETAPAS)
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · as seis etapas</div><h2>Uma ordem para ensinar</h2>
<p>As seis etapas partem da trilha de onboarding usada nas unidades da Zion: primeiro o lugar e o padrão da casa, depois a função, e só então a pessoa faz, primeiro acompanhada e depois sozinha.</p>
<table style="font-size:9pt"><tr><th style="width:30%">Etapa</th><th>Tarefas sugeridas</th></tr>{trs}</table>
<div class="box"><b>Exercício 1.</b> Marque na planilha quais tarefas são obrigatórias para a função da sua pessoa e escreva aqui uma tarefa que só a sua hospedagem tem (uma hidromassagem, um portão, um animal):<div class="linha"></div><div class="linha"></div></div>{foot(3,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · três passos por tarefa</div><h2>Mostrar, fazer junto, fazer sozinha</h2>
<table><tr><th style="width:24%">Passo</th><th>Quem faz</th><th>O que você anota</th></tr>
<tr><td class="aten"><b>1 · Mostrado</b></td><td>Você faz, a pessoa vê e pergunta</td><td>A data em "Mostrado em"</td></tr>
<tr><td class="azul"><b>2 · Feito junto</b></td><td>Ela faz, você do lado, corrigindo na hora</td><td>A data em "Feito junto em"</td></tr>
<tr><td class="ok"><b>3 · Fez sozinha e conferido</b></td><td>Ela faz, você confere só no fim</td><td>A data e o seu nome em "Conferido por"</td></tr></table>
<div class="box"><b>Por que três passos:</b> ver não é saber fazer. Na trilha da Zion, a pessoa só executa depois de ver a tarefa e ler o procedimento, e a primeira execução é sempre acompanhada.</div>
<div class="box alerta"><b>A planilha avisa quando algo não bate:</b> um passo pulado ou datas fora de ordem, uma data no futuro, ou uma tarefa feita sozinha sem o nome de quem conferiu. Essas linhas ficam vermelhas e seguram a liberação.</div>
<div class="box"><b>Exercício 2.</b> Escolha a tarefa mais importante da função e escreva o que você vai olhar na conferência do passo 3:<div class="linha"></div><div class="linha"></div></div>{foot(4,T)}</section>""")
    sel = [l for l in LIN if l["n"] in (2, 3, 7, 11, 13, 16)]
    tr = "".join(f"<tr><td>{l['n']}</td><td>{E(l['t'])}</td><td class='n'>{dbr(l['f'])}</td><td class='n'>{dbr(l['g'])}</td><td class='n'>{dbr(l['h'])}</td><td class='n'>{dbr(l['prazo'])}</td><td class='{cls(l['sit'])}'>{E(l['sit'])}</td></tr>" for l in sel)
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · acompanhe pela planilha</div><h2>Prazo e situação de cada tarefa</h2>
<p>Cada tarefa tem um prazo em dias depois do início. Se o prazo passou e ela ainda não está pronta, aparece como Atrasada.</p>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · {E(EX['pessoa'])}, início 02/11, hoje 05/11</span>
<table style="margin-top:8px;font-size:8.8pt"><tr><th>Nº</th><th>Tarefa</th><th>Mostrado</th><th>Junto</th><th>Sozinha</th><th>Prazo</th><th>Situação</th></tr>{tr}</table>
<p style="font-size:9.5pt;margin:6px 0 0">Na tarefa 13, o "fez sozinha" está com data anterior ao "feito junto": a planilha pede para conferir antes de contar como pronta.</p></div>{foot(5,T)}</section>""")
    tre = "".join(f"<tr><td>{E(a)}</td><td class='n'>{E(str(b))}</td></tr>" for a, b in ETP)
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · o painel</div><h2>Quando ela pode fazer o turno sozinha</h2>
<div style="display:flex;gap:12px"><table style="flex:1"><tr><th>Resultado (exemplo fictício)</th><th>Valor</th></tr>
<tr><td>Tarefas no plano</td><td class='n'>{PAN['tot']}</td></tr><tr><td>Obrigatórias prontas</td><td class='n'>{PAN['obok']} de {PAN['ob']} ({pct})</td></tr>
<tr><td>Atrasadas</td><td class='n pend'>{PAN['atr']}</td></tr><tr><td>Linhas para conferir</td><td class='n'>{PAN['conf']}</td></tr>
<tr><td>Próxima tarefa</td><td>{E(str(PAN['prox']))}</td></tr><tr><td><b>Liberada para o turno sozinha?</b></td><td class="aten"><b>{E(PAN['lib'])}</b></td></tr></table>
<table style="flex:.8"><tr><th>Etapa</th><th>Tarefas · prontas</th></tr>{tre}</table></div>
<div class="box"><b>A regra é uma só:</b> o primeiro turno sozinha só acontece quando todas as tarefas obrigatórias estão prontas e nenhuma linha está para conferir. Antes disso, a pessoa trabalha acompanhada.</div>
<div class="box"><b>Exercício 3.</b> Escreva a data que você espera liberar o primeiro turno sozinha e o que fará se ela chegar com tarefas atrasadas:<div class="linha"></div><div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Lista certa</td><td>As tarefas da função estão na planilha, com as obrigatórias marcadas</td></tr>
<tr><td>Ordem respeitada</td><td>Cada tarefa passou por mostrado, feito junto e feito sozinha, nessa ordem</td></tr>
<tr><td>Conferência</td><td>Toda tarefa pronta tem o nome de quem conferiu</td></tr>
<tr><td>Liberação</td><td>O Painel diz "Sim" antes do primeiro turno sozinha</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Ajustei a lista &nbsp; ☐ Marquei as obrigatórias e os prazos &nbsp; ☐ Imprimi a Ficha do Primeiro Turno<br>
☐ Anotei cada passo com data &nbsp; ☐ Conferi as tarefas prontas &nbsp; ☐ O Painel liberou o turno sozinha</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>Não substitui contrato, registro, exames, treinamentos exigidos por lei nem orientação do contador ou do advogado.</li>
<li>Não avalia a pessoa: registra o que foi ensinado e conferido.</li>
<li>Não define o que cada pessoa decide sozinha nem quanto pode gastar: isso é outra conversa, à parte.</li>
<li>Uma pessoa por arquivo, até 60 tarefas (duplique o arquivo para cada pessoa).</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplo com pessoas, datas e hospedagem fictícias. As seis etapas partem da trilha de onboarding usada nas unidades da Zion. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def ficha():
    rot = [("Chegada", "Apresentar a casa, a equipe e os contatos de emergência"), ("Volta pelo lugar", "Unidades, áreas comuns, onde fica cada material e cada chave"),
           ("Padrão da casa", "Jeito de atender e o que nunca pode acontecer"), ("Ver a função", "Você faz uma tarefa completa; a pessoa vê e pergunta"),
           ("Fazer junto", "A pessoa faz a mesma tarefa, você do lado"), ("Fechamento", "O que ficou para amanhã, dúvidas e próximo dia")]
    trs = "".join(f"<tr><td style='width:16%'>___:___</td><td style='width:22%'><b>{a}</b></td><td style='font-size:9pt'>{b}</td><td style='width:8%;text-align:center'>☐</td></tr>" for a, b in rot)
    lin = "".join("<tr><td></td><td></td><td style='text-align:center'>☐</td><td style='text-align:center'>☐</td><td style='text-align:center'>☐</td><td></td></tr>" for _ in range(7))
    cab = "".join(f'<div style="flex:1"><span style="font-size:8.5pt">{x}</span><div class="linha"></div></div>' for x in ("Pessoa", "Função", "Data", "Quem treina"))
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:11mm}} body{{background:#fff}} td{{height:28px}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 20</div>
<h2 style="font-size:22pt">Ficha do primeiro turno</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<div style="display:flex;gap:14px;margin:2px 0 8px">{cab}</div>
<table><tr><th>Hora</th><th>Momento</th><th>O que fazer</th><th>Feito</th></tr>{trs}</table>
<table style="margin-top:10px"><tr><th style="width:8%">Nº</th><th>Tarefa do dia</th><th style="width:10%">Mostrado</th><th style="width:10%">Junto</th><th style="width:10%">Sozinha</th><th style="width:18%">Conferido por</th></tr>{lin}</table>
<div class="box" style="font-size:9.5pt;margin-top:10px"><b>No fim do turno:</b> ☐ dúvidas anotadas &nbsp; ☐ datas passadas para a planilha &nbsp; ☐ próximo dia combinado<br>
<b>Assinaturas:</b> pessoa em treinamento ____________________ &nbsp; quem treinou ____________________</div>
<p style="font-size:8.5pt;color:#6b6656">As etapas partem da trilha de onboarding usada nas unidades da Zion. Depois, passe as datas para a aba Treinamento da planilha.</p></body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Treinamento · Ferramenta 20</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Valores calculados pela planilha da Ferramenta 20.</div></body></html>"""
lin = lambda a, b, c="": f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;white-space:nowrap;font-weight:600;align-self:center">{b}</span></div>'
painel = (lin("Tarefas no plano", PAN["tot"]) + lin("Obrigatórias prontas", f"{PAN['obok']} de {PAN['ob']}", "ok") + lin("Atrasadas", PAN["atr"], "pend") +
          lin("Linhas para conferir", PAN["conf"], "pend") + "".join(lin(a, b) for a, b in ETP[:4]))
tar = "".join(lin(f"{E(l['t'][:30])}{'…' if len(l['t']) > 30 else ''}", "Conferir" if "confira" in str(l["sit"]) else l["sit"], cls(l["sit"])) for l in LIN if l["n"] in (1, 3, 6, 7, 8, 11, 13, 15))
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(ficha(), encoding="utf-8")
(BUILD / "demo-painel.html").write_text(demo("Painel do treinamento", PAN["lib"], "#FCE8B2", painel), encoding="utf-8")
(BUILD / "demo-tarefas.html").write_text(demo("Tarefas da semana", f"{EX['pessoa']} · dia 4", "#E3EEDF", tar), encoding="utf-8")
print(PAN)

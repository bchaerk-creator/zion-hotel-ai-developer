"""Gera guia, ficha de ronda e demonstração da Ferramenta 18 com valores REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html, datetime as dt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from dados import FREQ, SUGERIDAS, EX_PLANO, P0
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Manutencao-Preventiva-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Manutencao-Preventiva-Zion-EXEMPLO.xlsx", data_only=True)
PL, S = W["Plano"], W["Painel"]
dv = lambda v: v.date() if isinstance(v, dt.datetime) else v
dbr = lambda v: dv(v).strftime("%d/%m/%Y") if isinstance(dv(v), dt.date) else "—"
brl = lambda x: ("R$ " + f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) if isinstance(x, (int, float)) else "—"
LIN = [dict(n=PL[f"A{r}"].value, u=PL[f"B{r}"].value, t=PL[f"D{r}"].value, f=PL[f"E{r}"].value or f"{PL[f'F{r}'].value} dias", iv=PL[f"J{r}"].value,
            resp=PL[f"G{r}"].value, ult=PL[f"K{r}"].value, prox=PL[f"L{r}"].value, sit=PL[f"M{r}"].value, custo=PL[f"N{r}"].value, dias=PL[f"O{r}"].value)
       for r in range(P0, P0 + len(EX_PLANO))]
PAN = {k: S[f"B{l}"].value for k, l in (("hoje", 4), ("total", 5), ("atr", 6), ("breve", 7), ("emdia", 8), ("sem", 9), ("urg", 12), ("urgt", 13), ("custo", 14), ("leit", 15))}
cls = lambda s: {"Atrasada": "pend", "Vence em breve": "aten", "Em dia": "ok"}.get(s, "cinza")
CSS2 = CSS + ".aten{background:#FCE8B2} .cinza{background:#E6E6E6} td.n{text-align:right;white-space:nowrap}"
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 18 · Planner de Manutenção Preventiva</span><span>{n}/{t}</span></div>'

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-plano.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:14mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-painel.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:28mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 18 · Guia do comprador</div><h1 style="color:var(--creme)">Planner de Manutenção Preventiva</h1>
<p style="font-size:13pt;max-width:160mm">Aprenda o passo a passo para montar um plano de manutenção preventiva: o que conferir, de quanto em quanto tempo, quem faz e o que está atrasado.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas e glampings. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem cuida de uma ou mais hospedagens e quer parar de descobrir o problema quando o hóspede já chegou: ar sem filtro, detector sem pilha, calha entupida, gás vencido.<br>
<b>Quando usar:</b> para montar o plano uma vez e, depois, toda semana, para ver o que está atrasado e o que vem a seguir.</div>
<h3>Você termina com</h3><ol class="passos"><li>A lista do que precisa ser conferido em cada unidade, com frequência e responsável.</li>
<li>A próxima data de cada tarefa, calculada a partir da última vez que foi feita.</li><li>Um painel semanal com o que está atrasado, o que vence em breve e quanto o plano custa por ano.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja as abas Plano, Registro e Painel.</li>
<li>Na planilha em branco, ajuste a lista sugerida à sua hospedagem e anote a última vez de cada tarefa.</li><li>Use a Ficha de Ronda no dia a dia e passe o que foi feito para a aba Registro.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Manutencao-Preventiva-Zion-EM-BRANCO.xlsx</td><td>Seu planner, com {len(SUGERIDAS)} tarefas sugeridas</td></tr>
<tr><td>Manutencao-Preventiva-Zion-EXEMPLO.xlsx</td><td>Uma hospedagem fictícia com 3 áreas e {PAN['total']} tarefas</td></tr>
<tr><td>Ficha-de-Ronda-Preventiva.pdf</td><td>Ronda diária e semanal para imprimir</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    sug = "".join(f"<tr><td>{E(a)}</td><td>{E(t)}</td><td>{E(f)}</td></tr>" for a, t, f in SUGERIDAS[:7])
    sug2 = "".join(f"<tr><td>{E(a)}</td><td>{E(t)}</td><td>{E(f)}</td></tr>" for a, t, f in SUGERIDAS[8:16])
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · monte a lista</div><h2>O que conferir e de quanto em quanto tempo</h2>
<p>A planilha em branco já traz {len(SUGERIDAS)} tarefas sugeridas. As de frequência diária partem da ronda usada nas unidades da Zion; as demais são comuns a qualquer hospedagem. Apague o que não existe na sua (sem hidromassagem, sem gás) e acrescente o que falta.</p>
<div style="display:flex;gap:10px"><table style="flex:1;font-size:8.6pt"><tr><th>Área</th><th>Ronda diária</th><th>Freq.</th></tr>{sug}</table>
<table style="flex:1;font-size:8.6pt"><tr><th>Área</th><th>Outras tarefas</th><th>Freq.</th></tr>{sug2}</table></div>
<div class="box alerta"><b>Frequência é ponto de partida.</b> Ajuste ao manual do fabricante, às regras locais e ao profissional responsável. Gás, elétrica, extintores, caixa d'água e controle de pragas pedem profissional ou empresa habilitada.</div>
<div class="box"><b>Exercício 1.</b> Dê uma volta pela sua hospedagem com a lista na mão e escreva 3 tarefas que faltam nela:<div class="linha"></div><div class="linha"></div><div class="linha"></div></div>{foot(3,T)}</section>""")
    sel = [l for l in LIN if l["n"] in (2, 3, 7, 10, 16, 5)]
    tr = "".join(f"<tr><td>{l['n']}</td><td>{E(l['t'])}<br><span style='font-size:8pt;color:#6b6656'>{E(l['u'])} · {E(str(l['f']))}</span></td><td class='n'>{dbr(l['ult'])}</td><td class='n'>{dbr(l['prox'])}</td><td class='{cls(l['sit'])}'>{E(l['sit'])}</td></tr>" for l in sel)
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · última vez e próxima data</div><h2>A planilha calcula quando é a próxima</h2>
<ol class="passos"><li><b>Última vez (antes de começar):</b> se você lembra quando fez, anote. Se não sabe, deixe vazio: a tarefa aparece como "Sem registro" até a primeira vez.</li>
<li><b>Próxima data</b> = última vez + intervalo. Para um intervalo que não está na lista (o refil a cada 120 dias, por exemplo), deixe a frequência vazia e escreva os dias.</li>
<li><b>Situação:</b> Atrasada, Vence em breve (dentro do aviso que você escolheu, 7 dias no exemplo), Em dia ou Sem registro.</li></ol>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · hoje = {dbr(PAN['hoje'])}</span><table style="margin-top:8px"><tr><th>Nº</th><th>Tarefa</th><th>Última vez</th><th>Próxima</th><th>Situação</th></tr>{tr}</table>
<p style="font-size:9.5pt;margin:6px 0 0">O filtro do Chalé 2 tinha sido limpo em 28/10, mas o Registro de 12/11 passou a contar: a próxima data foi para 12/12.</p></div>{foot(4,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · registre o que foi feito</div><h2>Uma linha por tarefa feita</h2>
<p>Na aba Registro, anote a data, o nº da tarefa (o da aba Plano), quem fez e o que viu. A planilha usa a data mais recente para recalcular a próxima. A coluna Situação avisa quando o nº não existe ou a data está no futuro.</p>
<table><tr><th>Data</th><th>Nº</th><th>Feito por</th><th>O que viu ou fez</th><th>Situação</th></tr>
<tr><td>15/11/2026</td><td>1</td><td>Ana</td><td>pH 7,4 · cloro ok</td><td class="ok">OK</td></tr>
<tr><td>12/11/2026</td><td>3</td><td>Ana</td><td>Filtro lavado</td><td class="ok">OK</td></tr>
<tr><td>05/11/2026</td><td>99</td><td>Carlos</td><td>Nº digitado errado</td><td class="pend">Nº não existe no Plano</td></tr></table>
<p style="font-size:9pt;color:#6b6656">Exemplo com dados fictícios.</p>
<div class="box"><b>Na rotina da Zion</b>, a hidromassagem só é liberada depois de medir pH e cloro, e qualquer problema é avisado na hora a quem coordena a operação. Use o campo "O que viu ou fez" para guardar os valores medidos e o que foi encontrado.</div>
<div class="box alerta"><b>Preventiva não é corretiva.</b> Quando a ronda encontra algo quebrado, abra uma ocorrência com prazo e responsável (um quadro de ocorrências) e anote aqui só a tarefa preventiva feita.</div>
<div class="box"><b>Exercício 2.</b> Faça hoje a ronda diária com a Ficha de Ronda e passe as tarefas feitas para a aba Registro. Quantas ficaram "Em dia"?<div class="linha"></div></div>{foot(5,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · o painel da semana</div><h2>Comece pelo que está atrasado</h2>
<table><tr><th>Resultado (exemplo fictício)</th><th>Valor</th></tr>
<tr><td>Tarefas no plano</td><td class='n'>{PAN['total']}</td></tr><tr><td>Atrasadas</td><td class='n pend'>{PAN['atr']}</td></tr>
<tr><td>Vencem em breve (7 dias)</td><td class='n aten'>{PAN['breve']}</td></tr><tr><td>Em dia</td><td class='n ok'>{PAN['emdia']}</td></tr>
<tr><td>Sem registro</td><td class='n'>{PAN['sem']}</td></tr><tr><td>Mais urgente</td><td>{E(str(PAN['urgt']))} ({PAN['urg']} dias)</td></tr>
<tr><td>Custo anual estimado (tarefas com custo)</td><td class='n'><b>{brl(PAN['custo'])}</b></td></tr><tr><td><b>Leitura</b></td><td class="pend"><b>{E(PAN['leit'])}</b></td></tr></table>
<div class="box"><b>Como ler o exemplo:</b> duas tarefas passaram da data (o gás, 7 dias atrasado, e o filtro do Chalé 1). Quatro vencem nos próximos 7 dias e o detector do Chalé 2 nunca foi anotado. A ordem é: atrasadas, depois as que vencem em breve, depois as sem registro.</div>
<div class="box"><b>Custo anual estimado</b> = custo por vez × 365 ÷ intervalo, só para as tarefas com custo preenchido. Serve para colocar a manutenção no orçamento do ano; não inclui consertos imprevistos.</div>
<div class="box"><b>Exercício 3.</b> Escolha um dia fixo da semana para abrir o Painel e escreva aqui qual é, e quem cuida das tarefas atrasadas:<div class="linha"></div><div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Lista completa</td><td>Cada área da hospedagem tem pelo menos uma tarefa; nada que exista ficou de fora</td></tr>
<tr><td>Frequências conferidas</td><td>Ajustadas ao manual do fabricante e ao profissional responsável</td></tr>
<tr><td>Responsáveis</td><td>Toda tarefa tem um nome</td></tr><tr><td>Registro em dia</td><td>Cada tarefa feita anotada na semana; nenhuma linha para conferir</td></tr>
<tr><td>Painel</td><td>Aberto toda semana; atrasadas resolvidas primeiro</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Ajustei a lista &nbsp; ☐ Conferi as frequências &nbsp; ☐ Defini responsáveis &nbsp; ☐ Anotei a última vez<br>
☐ Imprimi a Ficha de Ronda &nbsp; ☐ Registrei as tarefas feitas &nbsp; ☐ Marquei o dia do Painel</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>As frequências sugeridas não substituem o manual do fabricante, as regras locais nem os profissionais habilitados.</li>
<li>Não substitui laudos, vistorias, manutenção técnica nem seguro.</li>
<li>Não prevê falhas: mostra o que está programado e o que passou da data.</li>
<li>Até 120 tarefas e 400 registros por arquivo (comece um arquivo novo por ano, se precisar).</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplo com hospedagem, pessoas, datas e custos fictícios. A ronda diária sugerida parte da rotina usada nas unidades da Zion. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def ficha():
    dias = "".join(f"<th style='width:7%;text-align:center'>{d}</th>" for d in ("Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"))
    cel = "".join("<td style='text-align:center'>☐</td>" for _ in range(7))
    diar = "".join(f"<tr><td style='font-size:9pt'>{E(t)}</td>{cel}</tr>" for a, t, f in SUGERIDAS if f == "Diária")
    vaz = "".join(f"<tr><td>&nbsp;</td>{cel}</tr>" for _ in range(3))
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:11mm}} body{{background:#fff}} td{{height:30px}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 18</div>
<h2 style="font-size:22pt">Ficha de ronda preventiva</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<div style="display:flex;gap:18px;margin:2px 0 8px">{''.join(f'<div style="flex:1"><span style="font-size:8.5pt">{x}</span><div class="linha"></div></div>' for x in ("Unidade", "Semana de", "Responsável"))}</div>
<table><tr><th>Ronda diária (ajuste à sua hospedagem)</th>{dias}</tr>{diar}{vaz}</table>
<table style="margin-top:10px"><tr><th style="width:12%">Data</th><th style="width:10%">Nº</th><th>Tarefa da semana ou do mês feita · o que viu</th><th style="width:16%">Quem</th></tr>
{''.join('<tr><td></td><td></td><td></td><td></td></tr>' for _ in range(10))}</table>
<div class="box" style="font-size:9.5pt;margin-top:10px"><b>Encontrou algo quebrado?</b> Avise na hora quem coordena a operação e abra uma ocorrência com prazo e responsável. Não libere a unidade com risco ao hóspede.</div>
<p style="font-size:8.5pt;color:#6b6656">A ronda diária sugerida parte da rotina usada nas unidades da Zion. Depois, passe as tarefas feitas para a aba Registro da planilha.</p></body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Manutenção Preventiva · Ferramenta 18</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Valores calculados pela planilha da Ferramenta 18.</div></body></html>"""
lin = lambda a, b, c="": f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;white-space:nowrap;font-weight:600;align-self:center">{b}</span></div>'
painel = (lin("Tarefas no plano", PAN["total"]) + lin("Atrasadas", PAN["atr"], "pend") + lin("Vencem em breve (7 dias)", PAN["breve"], "aten") +
          lin("Em dia", PAN["emdia"], "ok") + lin("Sem registro", PAN["sem"], "cinza") + lin("Mais urgente", f"{PAN['urg']} dias", "pend") +
          lin("Custo anual estimado", brl(PAN["custo"])))
ordem = sorted([l for l in LIN if l["dias"] is not None], key=lambda l: l["dias"])[:6] + [l for l in LIN if l["sit"].startswith("Sem")][:1]
plano = "".join(lin(f"{E(l['t'][:30])}{'…' if len(l['t']) > 30 else ''}<br><span style='font-size:11px;color:#6b6656'>{E(l['u'])}</span>",
                    (dv(l['prox']).strftime('%d/%m') + ' · ' if l['prox'] else '') + l['sit'].split(':')[0], cls(l["sit"])) for l in ordem)
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(ficha(), encoding="utf-8")
(BUILD / "demo-painel.html").write_text(demo("Painel da semana", PAN["leit"], "#F4C7C3", painel), encoding="utf-8")
(BUILD / "demo-plano.html").write_text(demo("Próximas tarefas", f"Hoje: {dbr(PAN['hoje'])}", "#FCE8B2", plano), encoding="utf-8")
print(PAN)

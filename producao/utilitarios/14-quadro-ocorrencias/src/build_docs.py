"""Gera guia, ficha de ronda e demonstração da Ferramenta 14 com valores REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from dados import PRIORIDADES
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Quadro-Ocorrencias-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Quadro-Ocorrencias-Zion-EXEMPLO.xlsx", data_only=True)
O, P = W["Ocorrências"], W["Painel"]
fd = lambda v: v.strftime("%d/%m") if isinstance(v, (datetime.date, datetime.datetime)) else ("" if v in (None, "") else str(v))
OC = [dict(n=O[f"A{r}"].value, ab=fd(O[f"B{r}"].value), un=O[f"C{r}"].value or "", loc=O[f"D{r}"].value, oq=O[f"E{r}"].value, pr=O[f"F{r}"].value,
           resp=O[f"G{r}"].value or "", prazo=fd(O[f"I{r}"].value), bl=O[f"J{r}"].value, res=fd(O[f"L{r}"].value), sit=O[f"O{r}"].value, dias=O[f"P{r}"].value)
      for r in range(6, 506) if O[f"E{r}"].value]
UN = [dict(u=P[f"A{r}"].value, ab=P[f"B{r}"].value, at=P[f"C{r}"].value, bl=P[f"D{r}"].value, fe=P[f"E{r}"].value, cu=P[f"F{r}"].value, sit=P[f"G{r}"].value) for r in range(7, 57) if P[f"A{r}"].value]
RES = dict(abertas=P["B3"].value, atrasadas=P["D3"].value, bloq=P["G3"].value, completar=P["B4"].value, custo=P["D4"].value, data=P["A2"].value)
brl = lambda v: ("R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) if isinstance(v, (int, float)) else ""
cls = lambda s: {"Atrasada": "pend", "Aberta": "aten", "Fechada": "ok", "Fechada sem descrição": "ok", "BLOQUEADA": "pend", "Liberada": "ok"}.get(s, "pend")
CSS2 = CSS + ".aten{background:#FCE8B2}"
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 14 · Quadro de Ocorrências e Manutenção</span><span>{n}/{t}</span></div>'
RONDA = ["Luzes internas e externas acendem", "Água quente chega em todos os chuveiros", "Ar-condicionado ou aquecedor liga e responde ao controle",
         "Sem vazamento em pias, vasos, chuveiros e registros", "Fechaduras e senhas funcionam", "Internet conecta com a senha do hóspede",
         "Deck, escadas, corrimãos e área externa firmes e limpos", "Equipamentos de lazer (piscina, banheira, churrasqueira) conforme a rotina do responsável"]

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-ocorrencias.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:16mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-painel.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:30mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 14 · Guia do comprador</div><h1 style="color:var(--creme)">Quadro de Ocorrências e Manutenção</h1>
<p style="font-size:13pt;max-width:155mm">Aprenda o passo a passo para registrar cada problema com responsável, prioridade e prazo, acompanhar até resolver e saber quais unidades não podem receber hóspede.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas e glampings. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem cuida de uma ou mais unidades, sozinho ou com equipe e prestadores, e já teve problema esquecido no grupo de mensagens.<br>
<b>Quando usar:</b> sempre que alguém encontrar um problema (na limpeza, na ronda ou por aviso do hóspede) e até ele ser resolvido.</div>
<h3>Você termina com</h3><ol class="passos"><li>Uma lista única de problemas, cada um com responsável, prioridade e prazo.</li>
<li>Um painel que mostra o que está atrasado e quais unidades estão bloqueadas para hóspede.</li>
<li>O histórico do que foi feito, quanto custou e quanto tempo levou.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja a aba Painel.</li>
<li>Na versão em branco, ajuste os prazos e cadastre unidades e responsáveis (cerca de 10 minutos).</li><li>Lance os problemas que existem hoje e faça a primeira ronda com a ficha.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Quadro-Ocorrencias-Zion-EM-BRANCO.xlsx</td><td>Sua planilha: ajustes, cadastros, ocorrências e painel</td></tr>
<tr><td>Quadro-Ocorrencias-Zion-EXEMPLO.xlsx</td><td>Uma hospedagem fictícia com 4 unidades e 6 ocorrências</td></tr>
<tr><td>Ficha-de-Ronda.pdf</td><td>Folha para a ronda, com espaço para anotar problemas</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    tr = "".join(f"<tr><td><b>{E(pr)}</b></td><td>{d}</td></tr>" for pr, d in PRIORIDADES)
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · abas Ajustes e Cadastros</div><h2>Combine prioridades e responsáveis</h2>
<p>Antes do primeiro problema, combine com quem trabalha com você o que é cada prioridade e quanto tempo cada uma pode esperar.</p>
<table><tr><th>Prioridade</th><th>Quando usar</th></tr>
<tr><td><b>Urgente</b></td><td>Impede receber hóspede ou traz risco à segurança</td></tr><tr><td><b>Alta</b></td><td>Atrapalha a estadia (água quente, ar, internet)</td></tr>
<tr><td><b>Média</b></td><td>Incomoda, mas não impede (torneira pingando, tábua solta fora do caminho)</td></tr><tr><td><b>Baixa</b></td><td>Melhoria ou estética</td></tr></table>
<div class="box ex"><span class="tag">Ponto de partida editável</span> A planilha vem com estes prazos, em dias depois da abertura. Não são norma: ajuste ao tempo real da sua equipe e dos seus prestadores.
<table style="margin-top:8px;width:50%"><tr><th>Prioridade</th><th>Dias até o prazo</th></tr>{tr}</table></div>
<p>Na aba <b>Cadastros</b>, escreva suas unidades e quem resolve: você, alguém da equipe, o eletricista, o técnico do ar. Elas viram listas para escolher nas ocorrências.</p>
<div class="box"><b>Exercício 1.</b> Escreva três problemas que já aconteceram na sua hospedagem e a prioridade que cada um deveria ter.<div class="linha"></div><div class="linha"></div><div class="linha"></div></div>{foot(3,T)}</section>""")
    tr = "".join(f"<tr><td>{o['n']}</td><td>{E(o['un'])}</td><td>{E(o['oq'])}</td><td>{E(str(o['pr']))}</td><td>{E(o['resp'])}</td><td>{o['prazo']}</td><td class='{cls(o['sit'])}'>{E(o['sit'])}</td></tr>" for o in OC)
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · aba Ocorrências</div><h2>Registre cada problema numa linha</h2>
<ol class="passos"><li>Data, unidade, local ou equipamento e o que aconteceu, em uma frase que outra pessoa entende.</li>
<li>Prioridade e responsável. O prazo aparece sozinho; se precisar de outro, digite na coluna Prazo.</li>
<li><b>Bloqueia a unidade?</b> Marque "Sim" quando o problema impede receber hóspede.</li>
<li>Evidência: foto ou link. Ajuda quem vai resolver e serve de registro.</li></ol>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · data de referência 07/11/2026</span><table style="margin-top:8px"><tr><th>Nº</th><th>Unidade</th><th>O que aconteceu</th><th>Prior.</th><th>Responsável</th><th>Prazo</th><th>Situação</th></tr>{tr}</table>
<p style="font-size:9pt;margin:6px 0 0">A ocorrência 6 está sem responsável: a planilha pede para completar. Problema sem dono é problema esquecido.</p></div>{foot(4,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · fechar a ocorrência</div><h2>Feche com data, descrição e custo</h2>
<p>Quando o problema for resolvido, preencha <b>Resolvida em</b>, <b>Como foi resolvido</b> e o <b>Custo</b>. A coluna Dias mostra quanto tempo levou.</p>
<table><tr><th>Situação</th><th>Quando aparece</th><th>O que fazer</th></tr>
<tr><td class="aten">Aberta</td><td>Dentro do prazo</td><td>Acompanhar</td></tr><tr><td class="pend">Atrasada</td><td>Prazo passou e não foi resolvida</td><td>Cobrar o responsável ou rever o prazo</td></tr>
<tr><td class="pend">Complete os dados</td><td>Falta unidade, prioridade, responsável ou data</td><td>Completar a linha</td></tr>
<tr><td class="ok">Fechada sem descrição</td><td>Tem data de resolução, mas não diz o que foi feito</td><td>Escrever como foi resolvido: ajuda na próxima vez</td></tr>
<tr><td class="ok">Fechada</td><td>Resolvida e descrita</td><td>Nada</td></tr><tr><td class="pend">Confira as datas</td><td>Resolvida antes de ser aberta</td><td>Corrigir as datas</td></tr></table>
<div class="box alerta"><b>Segurança:</b> gás, eletricidade, piscina, estrutura e equipamentos de lazer seguem o profissional habilitado e as orientações do fabricante. A planilha registra; não diz como consertar.</div>{foot(5,T)}</section>""")
    tr = "".join(f"<tr><td>{E(u['u'])}</td><td>{u['ab']}</td><td>{u['at']}</td><td>{u['bl']}</td><td>{u['fe']}</td><td>{brl(u['cu'])}</td><td class='{cls(u['sit'])}'>{E(u['sit'])}</td></tr>" for u in UN)
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · aba Painel e ronda</div><h2>Olhe o painel antes de cada entrada</h2>
<p>O Painel junta tudo por unidade e por responsável. Antes de liberar uma unidade para o próximo hóspede, confira se ela não está BLOQUEADA.</p>
<div class="box ex"><span class="tag">Demonstração · valores calculados pela planilha de exemplo</span>
<p style="margin:6px 0">{E(str(RES['data']))}: {RES['abertas']} abertas, {RES['atrasadas']} atrasadas, {RES['bloq']} unidade bloqueada, custo registrado {brl(RES['custo'])}.</p>
<table><tr><th>Unidade</th><th>Abertas</th><th>Atrasadas</th><th>Bloqueando</th><th>Fechadas</th><th>Custo</th><th>Situação</th></tr>{tr}</table></div>
<h3>Ronda</h3><p>Nas unidades da Zion, a manutenção começa com uma ronda diária, e nenhum problema fica sem avisar o responsável. A Ficha de Ronda traz uma ronda básica para qualquer hospedagem; o que a ronda encontrar vira uma linha em Ocorrências.</p>
<div class="box"><b>Exercício 2.</b> Escolha o dia e o horário da sua ronda e quem faz.<div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Nada sem dono</td><td>"A completar" igual a 0 no Painel</td></tr><tr><td>Prazos realistas</td><td>Poucas atrasadas; quando atrasa, o prazo é revisto ou o responsável é cobrado</td></tr>
<tr><td>Hóspede não recebe unidade bloqueada</td><td>Toda entrada conferida no Painel</td></tr><tr><td>Histórico útil</td><td>Toda ocorrência fechada tem descrição e custo</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Ajustei os prazos &nbsp; ☐ Cadastrei unidades e responsáveis &nbsp; ☐ Lancei os problemas de hoje<br>
☐ Fechei uma ocorrência com descrição e custo &nbsp; ☐ Fiz a primeira ronda &nbsp; ☐ Conferi o Painel antes de uma entrada</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>Não envia avisos: alguém precisa olhar o painel e falar com o responsável.</li><li>Não substitui profissional habilitado nem normas de segurança.</li>
<li>A situação depende da data de referência (hoje, se você não informar outra) e dos lançamentos.</li><li>Custos são os que você digitar; não é contabilidade.</li>
<li>A lógica parte da rotina de manutenção usada nas unidades da Zion, generalizada para qualquer hospedagem.</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplos com hospedagem, pessoas, datas e custos fictícios. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def ficha():
    itens = "".join(f"<tr><td>{E(i)}</td><td style='text-align:center'>☐</td><td style='text-align:center'>☐</td><td></td></tr>" for i in RONDA)
    linhas = "".join("<tr><td>&nbsp;</td><td></td><td></td><td></td><td></td></tr>" for _ in range(9))
    cab = "".join(f'<div style="flex:1 1 30%"><span style="font-size:8.5pt">{r}</span><div class="linha"></div></div>' for r in ("Data", "Quem fez a ronda", "Unidade"))
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:12mm}} body{{background:#fff}} td{{height:24px;font-size:9.5pt}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 14</div>
<h2 style="font-size:22pt">Ficha de ronda</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<div style="display:flex;gap:18px;margin:4px 0 10px">{cab}</div>
<table><tr><th style="width:55%">Verificar</th><th>OK</th><th>Problema</th><th>Observação</th></tr>{itens}</table>
<h3>Problemas encontrados (vão para a aba Ocorrências)</h3>
<table><tr><th style="width:30%">O que aconteceu</th><th>Local</th><th>Prioridade</th><th>Bloqueia?</th><th>Foto?</th></tr>{linhas}</table>
<p style="font-size:8.5pt;color:#6b6656;margin-top:8px">Ronda básica: ajuste à sua hospedagem. Gás, elétrica, piscina e estrutura seguem o profissional habilitado.</p></body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Quadro de Ocorrências · Ferramenta 14</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Valores calculados pela planilha da Ferramenta 14.</div></body></html>"""
lin = lambda a, b, c: f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;white-space:nowrap">{b}</span></div>'
painel = "".join(lin(f"{E(u['u'])} · {u['ab']} aberta(s)", E(u["sit"]), cls(u["sit"])) for u in UN)
ocs = "".join(lin(f"{E(o['un'] or '—')} · {E(o['loc'] or '')}", E(o["sit"]), cls(o["sit"])) for o in OC)
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(ficha(), encoding="utf-8")
(BUILD / "demo-painel.html").write_text(demo("Painel", f"{RES['bloq']} unidade bloqueada · {RES['atrasadas']} atrasadas", "#F4C7C3", painel), encoding="utf-8")
(BUILD / "demo-ocorrencias.html").write_text(demo("Ocorrências", f"{RES['abertas']} abertas · {RES['completar']} a completar", "#FCE8B2", ocs), encoding="utf-8")
print(RES)

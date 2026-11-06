"""Gera guia, ficha de contagem e demonstração da Ferramenta 13 com valores REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from itens import PADRAO
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Controle-Enxoval-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Controle-Enxoval-Zion-EXEMPLO.xlsx", data_only=True)
S, M, IT = W["Saldo"], W["Movimentos"], W["Itens"]
SAL = [[S[f"{c}{r}"].value for c in "ABCDEFGHIJKL"] for r in range(7, 107) if S[f"B{r}"].value]
MOV = [[M[f"{c}{r}"].value for c in "ABCDEFG"] for r in range(6, 506) if M[f"B{r}"].value]
RES = dict(comprar=S["C3"].value, custo=S["H3"].value, nomin=S["C4"].value, dif=S["H4"].value, prob=S["C5"].value)
ITN = [[IT[f"{c}{r}"].value for c in "ABCDEFGHI"] for r in range(6, 106) if IT[f"B{r}"].value]
brl = lambda v: ("R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) if isinstance(v, (int, float)) else ""
num = lambda v: "" if v in (None, "") else (f"{v:g}" if isinstance(v, float) else str(v))
cls = lambda s: {"COMPRAR": "pend", "OK": "ok", "No mínimo": "aten"}.get(s, "pend" if str(s).startswith("Confira") else "")
CSS2 = CSS + ".aten{background:#FCE8B2}"
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 13 · Controle de Enxoval e Reposição</span><span>{n}/{t}</span></div>'

def tab_saldo(linhas):
    tr = "".join(f"<tr><td>{E(l[1])}</td><td>{num(l[5])}</td><td>{num(l[6])}</td><td><b>{num(l[7])}</b></td><td class='{cls(l[8])}'>{E(str(l[8]))}</td><td>{brl(l[9])}</td></tr>" for l in linhas)
    return f"<table><tr><th>Item</th><th>Saldo</th><th>Mínimo</th><th>Comprar</th><th>Situação</th><th>Custo estimado</th></tr>{tr}</table>"

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-movimentos.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:16mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-compras.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:30mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 13 · Guia do comprador</div><h1 style="color:var(--creme)">Controle de Enxoval e Reposição</h1>
<p style="font-size:13pt;max-width:155mm">Aprenda o passo a passo para saber quanto enxoval e quantos itens de reposição você tem, quanto deveria ter e o que precisa comprar.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas e glampings. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem cuida de uma ou mais unidades e já passou pela falta de lençol, toalha, papel ou sabonete na hora da troca.<br>
<b>Quando usar:</b> a cada compra, a cada descarte ou perda, e numa contagem rápida uma vez por semana.</div>
<h3>Você termina com</h3><ol class="passos"><li>Uma lista dos seus itens com o mínimo de cada um, decidido por você.</li>
<li>O saldo atualizado de cada item e a lista do que comprar, com a quantidade e o custo estimado.</li>
<li>Uma conferência semanal que mostra perdas que ninguém lançou.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja a aba Saldo.</li>
<li>Na versão em branco, ajuste a lista e os mínimos (cerca de 20 minutos).</li><li>Faça a primeira contagem e lance o que existe hoje como entrada.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Controle-Enxoval-Zion-EM-BRANCO.xlsx</td><td>Sua planilha, com {len(PADRAO)} itens comuns já listados</td></tr>
<tr><td>Controle-Enxoval-Zion-EXEMPLO.xlsx</td><td>Uma hospedagem fictícia com 4 unidades, lançamentos e compras</td></tr>
<tr><td>Ficha-de-Contagem.pdf</td><td>Folha para a contagem semanal no armário, à mão</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    tr = "".join(f"<tr><td>{E(str(l[1]))}</td><td>{num(l[3])}</td><td>{num(l[4])}</td><td>{num(l[5])}</td><td>{num(l[6])}</td><td>{num(l[7])}</td></tr>" for l in ITN[:9])
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · aba Itens</div><h2>Defina o mínimo de cada item</h2>
<p>O mínimo é a quantidade abaixo da qual você precisa comprar. Ele é decisão sua: depende de quantas unidades você tem, de quanto tempo a lavanderia leva e de quanto tempo o fornecedor leva para entregar.</p>
<div class="box"><b>Enxoval:</b> preencha peças por unidade × unidades que usam × jogos em rotação, e a planilha calcula. Jogos em rotação é quantos conjuntos existem de cada peça por cama ou banheiro: um em uso, um na lavanderia e um de reserva dão 3.<br>
<b>Amenities e limpeza:</b> digite o mínimo direto na coluna "Mínimo digitado". Se você digitar, ele vale no lugar do calculado.</div>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · 4 unidades</span><table style="margin-top:8px"><tr><th>Item</th><th>Peças/unid.</th><th>Unidades</th><th>Jogos</th><th>Calculado</th><th>Digitado</th></tr>{tr}</table></div>
<div class="box"><b>Exercício 1.</b> Para o item que mais falta na sua hospedagem, escreva: quantos dias a lavanderia leva? Quantos dias o fornecedor leva para entregar? Com isso, quantos jogos em rotação você precisa?<div class="linha"></div><div class="linha"></div></div>{foot(3,T)}</section>""")
    mv = "".join(f"<tr><td>{E(str(m[1]))}</td><td>{E(str(m[2]))}</td><td>{num(m[3])}</td><td>{E(str(m[4] or ''))}</td><td class='{'ok' if m[6]=='OK' else 'pend'}'>{E(str(m[6]))}</td></tr>" for m in MOV[-7:])
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · aba Movimentos</div><h2>Lance o que entra e o que sai</h2>
<ol class="passos"><li><b>Primeiro lançamento:</b> conte o que existe hoje e lance cada item como Entrada, motivo "Outro" ("contagem inicial").</li>
<li><b>Entradas:</b> cada compra, doação ou transferência de outra unidade.</li><li><b>Saídas:</b> consumo (amenities), descarte, perda ou dano (enxoval).</li>
<li>Peça que vai para a lavanderia e volta <b>não</b> é saída: ela continua sendo sua. Só lance como saída o que deixou de existir.</li></ol>
<p>Lançamento com item que não está na lista, sem tipo ou com quantidade zero ou negativa fica vermelho e não entra na conta.</p>
<div class="box ex"><span class="tag">Exemplo · últimos lançamentos</span><table style="margin-top:8px"><tr><th>Item</th><th>Tipo</th><th>Qtd.</th><th>Motivo</th><th>Situação</th></tr>{mv}</table>
<p style="font-size:9pt;margin:6px 0 0">"Toalha de praia" não está na aba Itens: a planilha avisa e não soma. Cadastre o item e o lançamento passa a contar.</p></div>{foot(4,T)}</section>""")
    compras = [l for l in SAL if l[8] in ("COMPRAR", "No mínimo")]
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · aba Saldo</div><h2>Veja o que comprar</h2>
<p>A aba Saldo junta tudo: entradas, saídas, saldo, mínimo e a situação de cada item.</p>
<table><tr><th>Situação</th><th>Quando aparece</th><th>O que fazer</th></tr>
<tr><td class="pend">COMPRAR</td><td>Saldo abaixo do mínimo</td><td>Comprar a quantidade da coluna Comprar</td></tr>
<tr><td class="aten">No mínimo</td><td>Saldo igual ao mínimo</td><td>Programar a compra antes da próxima falta</td></tr>
<tr><td class="ok">OK</td><td>Saldo acima do mínimo</td><td>Nada</td></tr>
<tr><td class="pend">Confira: saídas maiores que entradas</td><td>Saldo negativo</td><td>Faltou lançar uma entrada ou houve erro</td></tr>
<tr><td>Defina o mínimo</td><td>Sem mínimo</td><td>Voltar ao passo 1</td></tr></table>
<p style="margin-top:12px"><b>Demonstração</b> com a planilha de exemplo (valores calculados pela própria planilha): {RES['comprar']} itens para comprar, {RES['nomin']} no mínimo, custo estimado de {brl(RES['custo'])}.</p>
{tab_saldo(compras)}{foot(5,T)}</section>""")
    dif = [l for l in SAL if isinstance(l[11], (int, float)) and l[11] != 0]
    tr = "".join(f"<tr><td>{E(l[1])}</td><td>{num(l[5])}</td><td>{num(l[10])}</td><td class='aten'>{num(l[11])}</td></tr>" for l in dif)
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · contagem semanal</div><h2>Conte uma vez por semana</h2>
<p>A planilha só sabe o que foi lançado. Uma vez por semana, num dia fixo, conte o que existe de verdade (use a Ficha de Contagem em papel) e anote na coluna <b>Contagem física</b> da aba Saldo. É a mesma rotina que usamos nas unidades da Zion: conferir num dia fixo da semana e acionar o fornecedor quando o item chega ao mínimo.</p>
<div class="box ex"><span class="tag">Exemplo · dados fictícios</span><table style="margin-top:8px"><tr><th>Item</th><th>Saldo na planilha</th><th>Contagem física</th><th>Diferença</th></tr>{tr}</table>
<p style="font-size:9pt;margin:6px 0 0">Diferença negativa: existem menos peças do que a planilha diz. Descubra o motivo (perda, lavanderia, descarte não lançado) e lance a saída com o motivo certo.</p></div>
<div class="box"><b>Exercício 2.</b> Escolha o dia da semana da contagem e quem conta.<div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Lista ajustada</td><td>Só itens que você usa; todos com mínimo (nenhum "Defina o mínimo")</td></tr>
<tr><td>Saldo confiável</td><td>Na contagem semanal, diferença zero ou explicada</td></tr>
<tr><td>Lançamentos limpos</td><td>"Lançamentos com problema" igual a 0</td></tr>
<tr><td>Compra no tempo certo</td><td>Nenhum item ficou em falta numa troca de hóspede</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Ajustei a lista de itens &nbsp; ☐ Defini o mínimo de todos &nbsp; ☐ Lancei a contagem inicial<br>
☐ Lancei uma compra e uma saída &nbsp; ☐ Fiz a primeira contagem semanal &nbsp; ☐ Comprei o que estava em COMPRAR</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>O mínimo é decisão sua. A planilha não prevê ocupação nem quantos hóspedes você vai receber.</li>
<li>Não acompanha a lavanderia peça por peça: peça na lavanderia continua no saldo.</li>
<li>Custos são os que você digitar; não é contabilidade nem controle fiscal.</li>
<li>O saldo depende dos lançamentos; a contagem semanal é o que mantém a planilha verdadeira.</li>
<li>A lógica parte do controle de estoque usado nas unidades da Zion, generalizado para qualquer hospedagem.</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplos com hospedagem, quantidades e preços fictícios. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def ficha():
    linhas = ""
    cat = None
    for c, n, u in PADRAO:
        if c != cat: linhas += f'<tr><td colspan="5" style="background:var(--areia);font-weight:700">{E(c)}</td></tr>'; cat = c
        linhas += f"<tr><td>{E(n)}</td><td>{E(u)}</td><td></td><td></td><td></td></tr>"
    linhas += "".join("<tr><td>&nbsp;</td><td></td><td></td><td></td><td></td></tr>" for _ in range(8))
    cab = "".join(f'<div style="flex:1 1 30%"><span style="font-size:8.5pt">{r}</span><div class="linha"></div></div>' for r in ("Data", "Quem contou", "Unidade ou depósito"))
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:12mm}} body{{background:#fff}} td{{height:24px;font-size:9.5pt}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 13</div>
<h2 style="font-size:22pt">Ficha de contagem semanal</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<div style="display:flex;gap:18px;margin:4px 0 10px">{cab}</div>
<table><tr><th style="width:38%">Item</th><th>Medida</th><th>Contado no armário</th><th>Na lavanderia</th><th>Observação</th></tr>{linhas}</table>
<p style="font-size:8.5pt;color:#6b6656;margin-top:8px">Depois, anote o total (armário + lavanderia) na coluna Contagem física da aba Saldo.</p></body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Controle de Enxoval · Ferramenta 13</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Valores calculados pela planilha da Ferramenta 13.</div></body></html>"""
lin = lambda a, b, c: f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;white-space:nowrap">{b}</span></div>'
compras = "".join(lin(E(l[1]), f"{l[8]} · {num(l[7])}" if l[8] == "COMPRAR" else E(l[8]), cls(l[8])) for l in SAL if l[8] in ("COMPRAR", "No mínimo"))
movs = "".join(lin(f"{E(str(m[1]))} · {E(str(m[2]))} {num(m[3])}", E(str(m[6])), "ok" if m[6] == "OK" else "pend") for m in MOV[-6:])
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(ficha(), encoding="utf-8")
(BUILD / "demo-compras.html").write_text(demo("Saldo e compras", f"{RES['comprar']} itens para comprar · {brl(RES['custo'])}", "#F4C7C3", compras), encoding="utf-8")
(BUILD / "demo-movimentos.html").write_text(demo("Entradas e saídas", f"{RES['prob']} lançamento com problema", "#FCE8B2", movs), encoding="utf-8")
print(RES)

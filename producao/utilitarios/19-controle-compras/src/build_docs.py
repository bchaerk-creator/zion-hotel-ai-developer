"""Gera guia, folha de compras e demonstração da Ferramenta 19 com valores REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from dados import CATEGORIAS, EX_NOITES
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Controle-Compras-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Controle-Compras-Zion-EXEMPLO.xlsx", data_only=True)
CO, M, A = W["Compras"], W["Mês"], W["Ano"]
COM = [[CO[f"{c}{r}"].value for c in "ABCDEFGHI"] for r in range(7, 407) if CO[f"C{r}"].value]
MES = [[M[f"{c}{r}"].value for c in "ABCDEFG"] for r in range(7, 22) if M[f"A{r}"].value]
TOT = [M[f"{c}22"].value for c in "ABCDEFG"]
RES = dict(acima=M["C24"].value, atencao=M["C25"].value, semcomp=M["C26"].value, prob=M["C27"].value, mes=M["F3"].value)
ANO = [[A.cell(r, j).value for j in range(1, 17)] for r in range(6, 21) if A.cell(r, 1).value]
brl = lambda v: ("R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) if isinstance(v, (int, float)) else ""
pct = lambda v: f"{v*100:.0f}%" if isinstance(v, (int, float)) else ""
dmy = lambda v: v.strftime("%d/%m") if hasattr(v, "strftime") else ""
cls = lambda s: {"Dentro": "ok", "OK": "ok", "Acima do orçamento": "pend", "Sem comprovante": "aten", "Sem orçamento": "aten"}.get(s, "aten" if str(s).startswith("Atenção") else "pend" if s else "")
CSS2 = CSS + ".aten{background:#FCE8B2}"
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 19 · Controle de Compras e Consumo Interno</span><span>{n}/{t}</span></div>'

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-compras.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:16mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-mes.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:30mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 19 · Guia do comprador</div><h1 style="color:var(--creme)">Controle de Compras e Consumo Interno</h1>
<p style="font-size:13pt;max-width:155mm">Aprenda o passo a passo para registrar as compras da sua hospedagem, comparar cada categoria com o orçamento do mês e saber quanto os insumos custam por noite ocupada.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas e glampings. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem compra produtos de limpeza, amenities, café, enxoval e pequenos reparos para a hospedagem e chega ao fim do mês sem saber para onde foi o dinheiro.<br>
<b>Quando usar:</b> a cada compra (2 minutos) e uma vez por semana para olhar o mês.</div>
<h3>Você termina com</h3><ol class="passos"><li>Um orçamento mensal por categoria, decidido por você.</li>
<li>Todas as compras num lugar só, com o comprovante marcado.</li>
<li>O gasto do mês contra o orçamento, o custo de insumos por noite ocupada e a visão do ano.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja a aba Mês.</li>
<li>Na versão em branco, ajuste as categorias (cerca de 10 minutos).</li><li>Lance as compras do mês atual, com a Folha de Compras se preferir anotar no papel.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Controle-Compras-Zion-EM-BRANCO.xlsx</td><td>Sua planilha: {len(CATEGORIAS)} categorias prontas (até 15) e 400 compras</td></tr>
<tr><td>Controle-Compras-Zion-EXEMPLO.xlsx</td><td>Uma pousada fictícia com compras de outubro e novembro</td></tr>
<tr><td>Folha-de-Compras.pdf</td><td>Para anotar compras no papel durante o mês</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    tr = "".join(f"<tr><td>{E(c)}</td><td>{E(ex)}</td></tr>" for c, ex in CATEGORIAS)
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · aba Orçamento</div><h2>Separe os gastos em categorias</h2>
<p>Categoria é a gaveta onde cada compra entra. Poucas e claras: se você não sabe onde lançar uma compra, a categoria está confusa.</p>
<table><tr><th>Categoria pronta</th><th>O que entra</th></tr>{tr}</table>
<div class="box"><b>Consumo interno</b> é o que a casa e a equipe usam e não vai para o hóspede: café e água da equipe, material de escritório. Separar ajuda a ver quanto ele pesa.</div>
<div class="box"><b>Orçamento:</b> se você ainda não sabe quanto gasta, deixe em branco por um ou dois meses. Depois, use o gasto real como ponto de partida e ajuste. O orçamento é decisão sua.</div>
<div class="box"><b>Exercício 1.</b> Escreva as três categorias em que você acha que mais gasta. No fim do mês, confira na aba Mês se acertou.<div class="linha"></div></div>{foot(3,T)}</section>""")
    tr = "".join(f"<tr><td>{dmy(c[0])}</td><td>{E(str(c[1] or ''))}</td><td>{E(str(c[2]))}</td><td>{brl(c[5])}</td><td>{E(str(c[7] or ''))}</td><td class='{cls(c[8])}'>{E(str(c[8]))}</td></tr>" for c in COM[-8:])
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · aba Compras</div><h2>Lance cada compra no dia</h2>
<ol class="passos"><li>Data, categoria, o que foi comprado, fornecedor e valor.</li><li>Forma de pagamento e se você guardou nota ou comprovante.</li>
<li>Unidade é opcional: use quando a compra for de uma unidade só (um reparo no chalé 2, por exemplo).</li></ol>
<p>Compra sem data, com categoria fora da lista ou com valor zero ou em texto fica vermelha e não entra nas somas. Compra sem comprovante entra nas somas, mas fica amarela: guarde o comprovante.</p>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · últimas compras</span><table style="margin-top:8px"><tr><th>Data</th><th>Categoria</th><th>O quê</th><th>Valor</th><th>Comp.</th><th>Situação</th></tr>{tr}</table>
<p style="font-size:9pt;margin:6px 0 0">"Jardinagem" não está na aba Orçamento: cadastre a categoria e a compra passa a contar. A última linha está sem data.</p></div>{foot(4,T)}</section>""")
    tr = "".join(f"<tr><td>{E(l[0])}</td><td>{brl(l[1])}</td><td>{brl(l[2])}</td><td>{brl(l[3])}</td><td>{pct(l[4])}</td><td class='{cls(l[5])}'>{E(str(l[5] or ''))}</td><td>{brl(l[6])}</td></tr>" for l in MES)
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · aba Mês</div><h2>Compare com o orçamento</h2>
<p>Escreva qualquer dia do mês que quer ver e, se souber, as noites ocupadas no mês (cada noite vendida de cada unidade).</p>
<table><tr><th>Situação</th><th>Quando aparece</th><th>O que fazer</th></tr>
<tr><td class="pend">Acima do orçamento</td><td>Gasto maior que o orçamento</td><td>Descobrir o motivo; rever compra ou orçamento</td></tr>
<tr><td class="aten">Atenção: 90% ou mais</td><td>Chegou a 90% do orçamento</td><td>Segurar compras que podem esperar</td></tr>
<tr><td class="ok">Dentro</td><td>Abaixo de 90%</td><td>Nada</td></tr>
<tr><td class="aten">Sem orçamento</td><td>Gasto sem orçamento escrito</td><td>Definir o orçamento</td></tr></table>
<div class="box ex" style="margin-top:10px"><span class="tag">Exemplo · dados fictícios · {E(str(RES['mes']))} · {EX_NOITES} noites ocupadas</span><table style="margin-top:8px"><tr><th>Categoria</th><th>Gasto</th><th>Orçamento</th><th>Diferença</th><th>%</th><th>Situação</th><th>Por noite</th></tr>{tr}
<tr><td><b>Total</b></td><td><b>{brl(TOT[1])}</b></td><td><b>{brl(TOT[2])}</b></td><td><b>{brl(TOT[3])}</b></td><td><b>{pct(TOT[4])}</b></td><td></td><td><b>{brl(TOT[6])}</b></td></tr></table>
<p style="font-size:9pt;margin:6px 0 0">O mês do exemplo ainda está na metade: a lavanderia só tem a primeira quinzena. Olhe a aba Mês toda semana, não só no fim.</p></div>{foot(5,T)}</section>""")
    tr = "".join(f"<tr><td>{E(l[0])}</td><td>{brl(l[10])}</td><td>{brl(l[11])}</td><td>{brl(l[13])}</td><td>{brl(l[14])}</td></tr>" for l in ANO)
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · custo por noite e aba Ano</div><h2>Leia o custo por noite e o ano</h2>
<p><b>Custo por noite ocupada</b> = gasto do mês ÷ noites ocupadas. Ele ajuda a comparar meses com movimento diferente: um mês cheio gasta mais, mas o custo por noite pode ficar igual. No exemplo, {brl(TOT[6])} de insumos por noite ocupada.</p>
<p>A aba <b>Ano</b> mostra cada categoria mês a mês, no ano do mês escolhido, com o orçamento do ano (12 × o mensal).</p>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · trecho da aba Ano</span><table style="margin-top:8px"><tr><th>Categoria</th><th>Out</th><th>Nov</th><th>Total do ano</th><th>Orçamento do ano</th></tr>{tr}</table></div>
<div class="box"><b>Exercício 2.</b> Calcule o custo por noite de dois meses seguidos. Ele subiu ou caiu? Qual categoria explica a diferença?<div class="linha"></div><div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Tudo lançado</td><td>Soma do mês na planilha bate com o extrato e as notas do mês</td></tr>
<tr><td>Lançamentos limpos</td><td>"Compras com problema" igual a 0</td></tr>
<tr><td>Comprovantes</td><td>"Compras sem comprovante no mês" igual a 0 ou explicado</td></tr>
<tr><td>Orçamento vivo</td><td>Todas as categorias com orçamento; revisado a cada 3 meses</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Ajustei as categorias &nbsp; ☐ Escrevi o orçamento (ou marquei a data para escrever) &nbsp; ☐ Lancei as compras do mês<br>
☐ Conferi com o extrato &nbsp; ☐ Anotei as noites ocupadas &nbsp; ☐ Li a aba Mês e decidi o que ajustar</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>Não é contabilidade nem controle fiscal; impostos e obrigações seguem com o seu contador.</li>
<li>Não controla estoque: para quantidades e reposição, use o Controle de Enxoval e Reposição (Ferramenta 13).</li>
<li>O orçamento é decisão sua; a planilha não diz qual valor é o certo.</li>
<li>O custo por noite depende das noites ocupadas que você informar.</li>
<li>Os valores do exemplo são inventados e não servem como referência de preço.</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplos com pousada, fornecedores e valores fictícios. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def folha():
    col = "".join(f"<th>{t}</th>" for t in ("Data", "Categoria", "O que foi comprado", "Fornecedor", "Valor", "Pagamento", "Comprovante"))
    lin = "".join("<tr>" + "<td>&nbsp;</td>" * 6 + "<td>☐ Sim ☐ Não</td></tr>" for _ in range(15))
    cats = " · ".join(E(c) for c, _ in CATEGORIAS)
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4 landscape;margin:10mm}} body{{background:#fff}} td{{height:22px;font-size:9pt}} th{{font-size:8.5pt}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 19</div>
<h2 style="font-size:20pt;margin:0">Folha de compras do mês</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:12mm"></div>
<div style="display:flex;gap:18px;margin:4px 0 6px"><div style="flex:1"><span style="font-size:8.5pt">Mês</span><div class="linha"></div></div><div style="flex:1"><span style="font-size:8.5pt">Quem anotou</span><div class="linha"></div></div><div style="flex:2"><span style="font-size:8.5pt">Categorias: {cats}</span></div></div>
<table><tr>{col}</tr>{lin}</table>
<p style="font-size:8pt;color:#6b6656;margin-top:6px">Toda semana, passe as linhas para a aba Compras e guarde os comprovantes juntos, na ordem das datas.</p></body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Controle de Compras · Ferramenta 19</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Valores calculados pela planilha da Ferramenta 19.</div></body></html>"""
lin = lambda a, b, c: f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;white-space:nowrap">{b}</span></div>'
mes = "".join(lin(f"{E(l[0])}<br><small>{brl(l[1])} de {brl(l[2])}</small>", E(str(l[5]).replace(': 90% ou mais', ' · 90%')), cls(l[5])) for l in MES if l[1])
com = "".join(lin(f"{dmy(c[0])} · {E(str(c[1] or ''))}<br><small>{E(str(c[2]))} · {brl(c[5])}</small>", E(str(c[8])), cls(c[8])) for c in COM[-7:])
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(folha(), encoding="utf-8")
(BUILD / "demo-mes.html").write_text(demo(f"Mês {RES['mes']}", f"{brl(TOT[1])} de {brl(TOT[2])} · {brl(TOT[6])} por noite", "#FCE8B2", mes), encoding="utf-8")
(BUILD / "demo-compras.html").write_text(demo("Compras", f"{RES['prob']} com problema · {CO['E3'].value} sem comprovante", "#F4C7C3", com), encoding="utf-8")
print(RES, TOT)

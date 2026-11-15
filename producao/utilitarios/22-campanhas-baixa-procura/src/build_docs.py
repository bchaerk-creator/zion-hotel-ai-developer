"""Gera guia, ficha de campanha e demonstração da Ferramenta 22 com valores REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from dados import TIPOS, EX_BASE
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Campanhas-Baixa-Procura-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Campanhas-Baixa-Procura-Zion-EXEMPLO.xlsx", data_only=True)
PE, CA, P = W["Períodos"], W["Campanhas"], W["Painel"]
PER = [[PE[f"{c}{r}"].value for c in "ABCDEFGHI"] for r in range(6, 26) if PE[f"A{r}"].value]
CAM = [[CA[f"{c}{r}"].value for c in "ABCDEFGHIJKLMNOP"] for r in range(7, 67) if CA[f"A{r}"].value]
PAI = [(P[f"A{r}"].value, P[f"B{r}"].value) for r in range(4, 13)]
LEIT = P["A15"].value
brl = lambda v: ("R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) if isinstance(v, (int, float)) else ""
pct = lambda v: f"{v*100:.0f}%" if isinstance(v, (int, float)) else ""
dmy = lambda v: v.strftime("%d/%m") if hasattr(v, "strftime") else ""
cls = lambda s: {"OK": "ok", "Na meta ou acima": "ok", "Abaixo da meta": "aten"}.get(s, "pend" if s else "")
CSS2 = CSS + ".aten{background:#FCE8B2}"
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 22 · Planner de Campanhas para Períodos de Baixa Procura</span><span>{n}/{t}</span></div>'

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-periodos.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:16mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-campanhas.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:30mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 22 · Guia do comprador</div><h1 style="color:var(--creme)">Planner de Campanhas para Períodos de Baixa Procura</h1>
<p style="font-size:13pt;max-width:155mm">Aprenda o passo a passo para encontrar os períodos fracos da sua hospedagem, planejar campanhas sem vender abaixo do piso e acompanhar o que cada campanha trouxe.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas e glampings. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem vê o calendário vazio nos mesmos meses todo ano e só reage na última hora, baixando a diária.<br>
<b>Quando usar:</b> uma vez por trimestre para planejar os próximos períodos fracos, e toda semana enquanto uma campanha estiver no ar.</div>
<h3>Você termina com</h3><ol class="passos"><li>A lista dos períodos fracos, com a ocupação atual de cada um contra a sua meta.</li>
<li>Campanhas planejadas com antecedência, conferidas contra o piso da diária e o custo da estadia.</li>
<li>O registro do que cada campanha trouxe, para repetir o que funcionou.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja a aba Painel.</li>
<li>Na versão em branco, preencha a Base e liste os períodos dos próximos 6 meses (cerca de 20 minutos).</li><li>Planeje uma campanha por período fraco com a Ficha de Campanha.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Campanhas-Baixa-Procura-Zion-EM-BRANCO.xlsx</td><td>Sua planilha: até 20 períodos e 60 campanhas</td></tr>
<tr><td>Campanhas-Baixa-Procura-Zion-EXEMPLO.xlsx</td><td>Chalés fictícios com 4 períodos e 6 campanhas</td></tr>
<tr><td>Ficha-de-Campanha.pdf</td><td>Uma página para pensar cada campanha antes de lançar</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    tr = "".join(f"<tr><td>{E(str(l[0]))}</td><td>{dmy(l[1])} a {dmy(l[2])}</td><td>{l[3]}</td><td>{l[4]}</td><td>{pct(l[5])}</td><td class='{cls(l[6])}'>{E(str(l[6]))}</td></tr>" for l in PER)
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · abas Base e Períodos</div><h2>Encontre os períodos fracos</h2>
<p>Na <b>Base</b>, informe unidades, diária normal, piso da diária, taxas e impostos, custo variável por estadia e a sua meta de ocupação. O piso é a diária abaixo da qual você perde dinheiro; se ainda não tem, calcule com a Planilha Diária Mínima (vendida separadamente) ou com a sua conta de custos.</p>
<p>Em <b>Períodos</b>, liste o que costuma ficar vazio: depois de feriados, meses de chuva, dias úteis. O último dia é a última noite do período.</p>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · {EX_BASE['unidades']} chalés · meta {pct(EX_BASE['meta'])}</span><table style="margin-top:8px"><tr><th>Período</th><th>Datas</th><th>Reservadas</th><th>Disponíveis</th><th>Ocupação</th><th>Situação</th></tr>{tr}</table></div>
<div class="box"><b>Exercício 1.</b> Olhe o calendário do ano passado. Quais foram as 3 semanas mais vazias? Elas se repetem este ano?<div class="linha"></div><div class="linha"></div></div>{foot(3,T)}</section>""")
    tipos = "".join(f"<li><b>{E(t)}</b></li>" for t in TIPOS[:6])
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · aba Campanhas</div><h2>Escolha o tipo de campanha</h2>
<p>Desconto não é a única saída. Pense em quem pode viajar nesse período e no que faria essa pessoa reservar:</p>
<ul class="passos" style="list-style:disc;padding-left:20px">{tipos}</ul>
<table><tr><th>Tipo</th><th>Para quem costuma servir</th></tr>
<tr><td>Estadia longa</td><td>Quem trabalha de qualquer lugar ou tem férias fora de temporada</td></tr>
<tr><td>Última hora</td><td>Quem decide na semana; use com cuidado e sempre acima do piso</td></tr>
<tr><td>Pacote com experiência</td><td>Quem quer motivo para viajar: café especial, trilha, jantar</td></tr>
<tr><td>Público da região</td><td>Quem mora a poucas horas e pode ir no meio da semana</td></tr>
<tr><td>Hóspedes que já vieram</td><td>Quem já conhece e gostou; mensagem direta, com autorização de contato</td></tr></table>
<p style="font-size:9.5pt">Antecedência importa: a campanha precisa estar no ar antes de o período começar. A planilha avisa quando ela começa depois do período ou termina antes dele.</p>{foot(4,T)}</section>""")
    tr = "".join(f"<tr><td>{E(str(c[0]))}</td><td>{E(str(c[1]))}</td><td>{pct(c[2])}</td><td>{c[3] or ''}</td><td>{brl(c[11])}</td><td>{brl(c[12])}</td><td class='{cls(c[15])}'>{E(str(c[15]))}</td></tr>" for c in CAM)
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · as travas</div><h2>Não venda abaixo do piso</h2>
<p>Para cada campanha, a planilha calcula a diária com desconto e quanto sobra por noite depois das taxas e do custo da estadia:</p>
<div class="box"><b>Diária com desconto</b> = diária normal × (1 − desconto)<br><b>Líquido por noite</b> = diária com desconto × (1 − taxas) − custo da estadia ÷ estadia mínima</div>
<p>Estadia mínima maior dilui o custo da limpeza e da lavanderia: por isso estadia longa costuma aguentar desconto maior que última hora.</p>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · diária normal {brl(EX_BASE['diaria'])} · piso {brl(EX_BASE['piso'])}</span><table style="margin-top:8px;font-size:8.5pt"><tr><th>Período</th><th>Tipo</th><th>Desc.</th><th>Mín.</th><th>Diária</th><th>Líquido/noite</th><th>Alerta</th></tr>{tr}</table>
<p style="font-size:9pt;margin:6px 0 0">A última hora com 35% fica abaixo do piso. A campanha de abril começa depois de o período terminar.</p></div>{foot(5,T)}</section>""")
    tr = "".join(f"<tr><td>{E(str(a))}</td><td><b>{brl(b) if 'Faturamento' in str(a) else E(str(b))}</b></td></tr>" for a, b in PAI)
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · aba Painel</div><h2>Acompanhe e aprenda</h2>
<p>Quando a campanha rodar, anote as noites vendidas por ela. O painel mostra o que falta planejar e o faturamento bruto atribuído às campanhas. Faturamento não é lucro: o lucro depende dos seus custos.</p>
<div class="box ex"><span class="tag">Exemplo · dados fictícios</span><table style="margin-top:8px">{tr}</table>
<p style="margin:8px 0 0"><b>O que fazer agora:</b> {E(LEIT)}</p></div>
<div class="box"><b>Exercício 2.</b> Escolha o próximo período fraco e preencha uma Ficha de Campanha: para quem, qual oferta, por qual canal, a partir de quando.<div class="linha"></div><div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Antecedência</td><td>Todo período abaixo da meta com campanha sem alerta antes de começar</td></tr>
<tr><td>Preço protegido</td><td>Nenhuma campanha "Abaixo do piso" ou "Não cobre o custo"</td></tr>
<tr><td>Resultado anotado</td><td>Noites vendidas registradas em toda campanha encerrada</td></tr>
<tr><td>Aprendizado</td><td>Para o próximo ano, você sabe qual tipo de campanha funcionou em cada período</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Preenchi a Base &nbsp; ☐ Listei os períodos dos próximos meses &nbsp; ☐ Planejei uma campanha por período fraco<br>
☐ Conferi o piso de todas &nbsp; ☐ Coloquei no ar com antecedência &nbsp; ☐ Anotei as noites vendidas</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>A planilha não prevê demanda e não garante reservas: ela organiza e confere o que você planejar.</li>
<li>Noites "vendidas pela campanha" são as que você atribuir a ela; outras causas também influenciam.</li>
<li>Faturamento bruto não é lucro. O piso da diária depende de uma conta de custos correta.</li>
<li>Descontos e promoções seguem as regras de cada plataforma; confira antes de publicar.</li>
<li>Mensagem para hóspedes antigos só com autorização de contato.</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplos com chalés, datas e valores fictícios. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def ficha():
    campo = lambda t, n=1: f'<div style="margin:6px 0"><span style="font-size:9pt;font-weight:600">{E(t)}</span>' + '<div class="linha"></div>' * n + '</div>'
    tipos = " · ".join(f"☐ {E(t)}" for t in TIPOS)
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:13mm}} body{{background:#fff}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 22</div>
<h2 style="font-size:22pt;margin:0">Ficha de campanha</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<div style="display:flex;gap:16px"><div style="flex:1">{campo('Período (primeiro e último dia)')}</div><div style="flex:1">{campo('Ocupação hoje e meta')}</div></div>
{campo('Para quem é esta campanha? (quem pode viajar nesse período)', 2)}
<div style="margin:6px 0;font-size:9pt"><b>Tipo:</b> {tipos}</div>
{campo('A oferta em uma frase (desconto, estadia mínima, o que vem junto)', 2)}
<div style="display:flex;gap:16px"><div style="flex:1">{campo('Diária com desconto')}</div><div style="flex:1">{campo('Piso da diária')}</div><div style="flex:1">{campo('Ficou acima do piso?')}</div></div>
<div style="display:flex;gap:16px"><div style="flex:1">{campo('Canal')}</div><div style="flex:1">{campo('Começa em')}</div><div style="flex:1">{campo('Termina em')}</div><div style="flex:1">{campo('Responsável')}</div></div>
{campo('Mensagem principal (o que a pessoa vai ler)', 3)}
{campo('Regras e cuidados (cancelamento, regras da plataforma, autorização de contato)', 2)}
<div style="display:flex;gap:16px"><div style="flex:1">{campo('Noites vendidas pela campanha')}</div><div style="flex:1">{campo('O que repetir ou mudar na próxima')}</div></div>
<p style="font-size:8.5pt;color:#6b6656;margin-top:8px">Depois, lance a campanha na aba Campanhas e confira o alerta.</p></body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Campanhas de baixa procura · Ferramenta 22</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Valores calculados pela planilha da Ferramenta 22.</div></body></html>"""
lin = lambda a, b, c: f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;white-space:nowrap">{b}</span></div>'
per = "".join(lin(f"{E(str(l[0]))}<br><small>ocupação {pct(l[5])} · {l[7]} campanha(s)</small>", E(str(l[6])), cls(l[6])) for l in PER)
cam = "".join(lin(f"{E(str(c[1]))} · {pct(c[2])}<br><small>{brl(c[11])} por noite · {E(str(c[8]))}</small>", E(str(c[15])), cls(c[15])) for c in CAM)
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(ficha(), encoding="utf-8")
(BUILD / "demo-periodos.html").write_text(demo("Períodos fracos", f"{PAI[2][1]} de {PAI[1][1]} abaixo da meta", "#FCE8B2", per), encoding="utf-8")
(BUILD / "demo-campanhas.html").write_text(demo("Campanhas", f"{PAI[5][1]} com alerta · {PAI[6][1]} no ar", "#F4C7C3", cam), encoding="utf-8")
print(PAI, LEIT)

"""Gera guia, folha de fechamento e demonstração da Ferramenta 10 com valores REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from dados import TODOS
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Fechamento-Mensal-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Fechamento-Mensal-Zion-EXEMPLO.xlsx", data_only=True)
LA, FE = W["Lançamentos"], W["Fechamento"]
LAN = [[LA[f"{c}{r}"].value for c in "ABCDEFGH"] for r in range(7, 507) if LA[f"H{r}"].value]
FEC = [[FE[f"{c}{r}"].value for c in "ABCDEFG"] for r in range(8, 18) if FE[f"A{r}"].value]
TOT = [FE[f"{c}18"].value for c in "ABCDEF"]
CAN = [(FE[f"A{r}"].value, FE[f"B{r}"].value) for r in range(22, 26)]
CAT = [(FE[f"A{r}"].value, FE[f"B{r}"].value) for r in range(29, 49) if FE[f"A{r}"].value and FE[f"B{r}"].value]
LEIT, PROB = FE["B5"].value, FE["B4"].value
brl = lambda v: ("−" if isinstance(v, (int, float)) and v < 0 else "") + ("R$ " + f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) if isinstance(v, (int, float)) else ""
dmy = lambda v: v.strftime("%d/%m") if hasattr(v, "strftime") else ""
curto = lambda s: str(s or "").replace(" (fictício)", "").replace(" (fictícia)", "")
cls = lambda s: {"OK": "ok", "Fechado": "ok", "A conferir no extrato": "aten", "Sem lançamentos próprios": "aten", "Resultado negativo": "pend"}.get(s, "aten" if str(s).startswith("Confira ") and "no extrato" in str(s) else "pend" if s else "")
CSS2 = CSS + ".aten{background:#FCE8B2}"
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 10 · Fechamento Mensal por Imóvel</span><span>{n}/{t}</span></div>'

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-lancamentos.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:16mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-fechamento.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:30mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 10 · Guia do comprador</div><h1 style="color:var(--creme)">Fechamento Mensal por Imóvel</h1>
<p style="font-size:13pt;max-width:160mm">Aprenda o passo a passo para fechar o mês de cada imóvel: o que entrou por canal, o que saiu por categoria, as despesas divididas entre os imóveis e o que ainda falta conferir no extrato.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas e glampings. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem cuida de um ou mais imóveis e, no fim do mês, não sabe dizer com segurança quanto cada um deixou: os repasses caem misturados, as contas chegam em dias diferentes e a internet ou a ferramenta de gestão serve a todos.<br>
<b>Quando usar:</b> uma vez por semana para lançar e uma vez por mês, com o extrato do banco aberto, para fechar.</div>
<h3>Você termina com</h3><ol class="passos"><li>Cada entrada e saída do mês registrada, com o imóvel, o canal ou a categoria.</li>
<li>O resultado de cada imóvel, com as despesas comuns divididas.</li>
<li>A certeza de que tudo o que foi lançado aparece no extrato, e o resultado mês a mês no ano.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja a aba Fechamento.</li>
<li>Na versão em branco, cadastre os imóveis e lance o mês passado (cerca de 30 minutos, com o extrato em mãos).</li><li>Imprima a Folha de Fechamento e use todo mês.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Fechamento-Mensal-Zion-EM-BRANCO.xlsx</td><td>Sua planilha: até 10 imóveis, 20 categorias e 500 lançamentos</td></tr>
<tr><td>Fechamento-Mensal-Zion-EXEMPLO.xlsx</td><td>3 imóveis e 17 lançamentos fictícios</td></tr>
<tr><td>Folha-de-Fechamento.pdf</td><td>O roteiro do fechamento, para imprimir e preencher</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · aba Cadastros</div><h2>Nomeie os imóveis e as categorias</h2>
<p>Os nomes que você escrever aqui viram as listas da aba Lançamentos. As categorias de despesa já vêm com 10 sugestões; mude, apague ou acrescente até 20.</p>
<table><tr><th>Cadastro</th><th>Dica</th></tr>
<tr><td>Imóveis</td><td>Um nome curto por imóvel ou unidade que você quer acompanhar separado.</td></tr>
<tr><td>Categorias</td><td>Poucas e claras. Se uma despesa não cabe em nenhuma, use "Outras despesas" e reveja no fim do mês.</td></tr>
<tr><td>Canais</td><td>Fixos: Airbnb, Booking, Reserva direta e Outro canal.</td></tr>
<tr><td>{E(TODOS)}</td><td>Para despesas que servem a todos (internet, contador, ferramenta de gestão): a planilha divide em partes iguais.</td></tr></table>
<div class="box"><b>Exercício 1.</b> Liste as 3 despesas que mais pesam no seu mês. Elas estão nas categorias? Alguma serve a mais de um imóvel?<div class="linha"></div><div class="linha"></div></div>{foot(3,T)}</section>""")
    tr = "".join(f"<tr><td>{dmy(l[0])}</td><td>{E(curto(l[1]))}</td><td>{E(str(l[2] or ''))}</td><td>{E(str(l[3] or ''))}</td><td>{brl(l[5]) or E(str(l[5] or ''))}</td><td class='{cls(l[7])}'>{E(str(l[7]))}</td></tr>" for l in LAN)
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · aba Lançamentos</div><h2>Uma linha por dinheiro que entrou ou saiu</h2>
<ol class="passos"><li><b>Receita</b> = o valor que caiu na sua conta (o repasse da plataforma, já sem a taxa dela), com o canal.</li>
<li><b>Despesa</b> = o que você pagou, com a categoria. Se serve a todos, escolha "{E(TODOS)}".</li>
<li>Na descrição, nada de nome de hóspede: use o código da reserva se precisar.</li></ol>
<div class="box ex"><span class="tag">Exemplo · dados fictícios</span><table style="margin-top:8px;font-size:8.2pt"><tr><th>Data</th><th>Imóvel</th><th>Tipo</th><th>Canal ou categoria</th><th>Valor</th><th>Situação</th></tr>{tr}</table>
<p style="font-size:9pt;margin:6px 0 0">"Jardinagem" não está nas categorias e um valor foi escrito por extenso: os dois ficam fora das contas até serem corrigidos.</p></div>{foot(4,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · o extrato</div><h2>Confira cada lançamento no banco</h2>
<p>A planilha só sabe o que você lançou. O extrato mostra o que de fato aconteceu. No fechamento, abra os dois lado a lado:</p>
<ol class="passos"><li>Para cada lançamento encontrado no extrato, marque <b>Sim</b> em "Conferido no extrato?".</li>
<li>Lançamento que não aparece no extrato: veja se a data ou o valor estão certos, ou se o repasse ainda não caiu.</li>
<li>Movimento do extrato que não está na planilha: lance agora.</li></ol>
<table><tr><th>Situação</th><th>O que significa</th></tr>
<tr><td class="ok">OK</td><td>Lançado e encontrado no extrato</td></tr>
<tr><td class="aten">A conferir no extrato</td><td>Entra nas contas, mas ainda não foi visto no banco</td></tr>
<tr><td class="pend">Informe a data, Escolha o imóvel, Imóvel não cadastrado, Escolha o tipo, Escolha o canal, Categoria não cadastrada, Receita precisa de um imóvel, Confira o valor</td><td>Fica fora das contas até ser corrigido</td></tr></table>
<div class="box alerta"><b>Cuidados:</b> resultado do mês não é lucro. Impostos, sua remuneração e a reserva para reformas só entram se forem lançados. Contabilidade e imposto: com o seu contador.</div>{foot(5,T)}</section>""")
    tr = "".join(f"<tr><td>{E(curto(f[0]))}</td><td>{brl(f[1])}</td><td>{brl(f[2])}</td><td>{brl(f[3])}</td><td><b>{brl(f[4])}</b></td><td class='{cls(f[6])}'>{E(str(f[6]))}</td></tr>" for f in FEC)
    tr += f"<tr><td><b>Total</b></td><td><b>{brl(TOT[1])}</b></td><td><b>{brl(TOT[2])}</b></td><td><b>{brl(TOT[3])}</b></td><td><b>{brl(TOT[4])}</b></td><td>{TOT[5]} a conferir</td></tr>"
    can = " · ".join(f"{E(a)} {brl(b)}" for a, b in CAN if b)
    cat = " · ".join(f"{E(a)} {brl(b)}" for a, b in CAT)
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · abas Fechamento e Ano</div><h2>O resultado de cada imóvel</h2>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · outubro de 2026</span><table style="margin-top:8px;font-size:8.6pt"><tr><th>Imóvel</th><th>Receitas</th><th>Despesas</th><th>Divididas</th><th>Resultado</th><th>Situação</th></tr>{tr}</table>
<p style="font-size:9pt;margin:6px 0 0"><b>Por canal:</b> {can}<br><b>Por categoria:</b> {cat}</p>
<p style="margin:8px 0 0"><b>O que fazer agora:</b> {E(LEIT)}</p></div>
<p style="font-size:10pt">As despesas divididas (internet e ferramenta de gestão, R$ 750) viraram R$ 250 para cada um dos 3 imóveis. O chalé fechou negativo por causa de um conserto: o mês sozinho não diz se o imóvel vai mal, mas a aba Ano mostra se isso se repete.</p>
<div class="box"><b>Exercício 2.</b> Feche o mês passado de um imóvel. Quanto ficou "A conferir"? Qual categoria mais pesou?<div class="linha"></div><div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Registro limpo</td><td>"Lançamentos com problema" igual a 0</td></tr>
<tr><td>Bate com o banco</td><td>Nenhum lançamento do mês "A conferir no extrato"</td></tr>
<tr><td>Nada esquecido</td><td>Todo movimento do extrato está lançado</td></tr>
<tr><td>Mês fechado</td><td>"O que fazer agora" mostra "Mês fechado" ou só o aviso de resultado negativo</td></tr>
<tr><td>Privacidade</td><td>Nenhum nome ou telefone de hóspede nas descrições</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Cadastrei imóveis e categorias &nbsp; ☐ Lancei todas as receitas e despesas do mês &nbsp; ☐ Conferi cada lançamento no extrato<br>
☐ Corrigi os lançamentos com problema &nbsp; ☐ Li o resultado de cada imóvel &nbsp; ☐ Guardei os comprovantes e enviei ao contador, se for o caso</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>Soma só o que foi lançado: não importa extratos nem conversa com as plataformas.</li>
<li>Divide despesas comuns em partes iguais; outro critério de divisão exige lançar a parte de cada imóvel separada.</li>
<li>Não é contabilidade, não calcula imposto e não substitui o contador.</li>
<li>Não diz se a diária está certa (isso é a Ferramenta 01, vendida separadamente) nem controla compras contra orçamento (Ferramenta 19).</li>
<li>Organizar o financeiro não garante reservas, renda nem resultado positivo.</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplos com imóveis, lançamentos e valores fictícios. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def folha():
    campo = lambda t, n=1: f'<div style="margin:4px 0"><span style="font-size:9pt;font-weight:600">{E(t)}</span>' + '<div class="linha"></div>' * n + '</div>'
    passos = ["Baixei o extrato do mês de cada conta usada pelos imóveis", "Conferi os repasses de cada plataforma com o extrato", "Lancei todas as despesas, inclusive as divididas",
              "Marquei \"Sim\" em cada lançamento encontrado no extrato", "Corrigi os lançamentos com problema", "Guardei os comprovantes numa pasta do mês"]
    linhas = "".join("<tr><td style='height:22px'></td><td></td><td></td><td></td><td></td></tr>" for _ in range(8))
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:12mm}} body{{background:#fff}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 10</div>
<h2 style="font-size:22pt;margin:0">Folha de fechamento do mês</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<div style="display:flex;gap:14px"><div style="flex:1">{campo('Mês / ano')}</div><div style="flex:1">{campo('Data do fechamento')}</div><div style="flex:1">{campo('Responsável')}</div></div>
<h3 style="font-size:12pt;margin:8px 0 2px">Roteiro</h3><div style="font-size:9.5pt;columns:2">{''.join(f'<div>☐ {E(c)}</div>' for c in passos)}</div>
<h3 style="font-size:12pt;margin:10px 0 2px">Resultado de cada imóvel (copie da aba Fechamento)</h3>
<table style="font-size:9pt"><tr><th style="width:34%">Imóvel</th><th>Receitas</th><th>Despesas</th><th>Divididas</th><th>Resultado</th></tr>{linhas}</table>
<div style="display:flex;gap:14px;margin-top:6px"><div style="flex:1">{campo('Lançamentos a conferir no extrato')}</div><div style="flex:1">{campo('Lançamentos com problema')}</div></div>
{campo('Categoria que mais pesou e por quê', 2)}
{campo('O que muda no próximo mês', 2)}
<p style="font-size:8.5pt;color:#6b6656;margin-top:6px">Resultado do mês não é lucro: só soma o que foi lançado. Contabilidade e imposto: com o seu contador.</p></body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Fechamento · Ferramenta 10</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Valores calculados pela planilha da Ferramenta 10.</div></body></html>"""
lin = lambda a, b, c: f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;text-align:right;max-width:50%;align-self:flex-start">{b}</span></div>'
out = [l for l in LAN if hasattr(l[0], "month") and l[0].month == 10]
lan = "".join(lin(f"{dmy(l[0])} · {E(curto(l[1]))}<br><small>{E(str(l[2]))} · {E(str(l[3]))} · {brl(l[5]) or E(str(l[5]))}</small>", E(str(l[7])), cls(l[7])) for l in out[:8])
fec = "".join(lin(f"{E(curto(f[0]))}<br><small>receitas {brl(f[1])} · despesas {brl(f[2] + f[3])}</small>", f"<b>{brl(f[4])}</b><br><small>{E(str(f[6]))}</small>", cls(f[6])) for f in FEC)
fec += f'<div style="padding:12px 14px;font-size:13px"><b>O que fazer agora:</b><br>{E(LEIT)}</div>'
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(folha(), encoding="utf-8")
(BUILD / "demo-lancamentos.html").write_text(demo("Lançamentos", f"{TOT[5]} a conferir no extrato · {PROB} com problema", "#FCE8B2", lan), encoding="utf-8")
(BUILD / "demo-fechamento.html").write_text(demo("Fechamento · outubro", f"Resultado do mês: {brl(TOT[4])}", "#C8E6C0", fec), encoding="utf-8")
print(FEC, TOT, LEIT)

"""Gera guia, ficha de cotação e demonstração da Ferramenta 05 com valores REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from dados import ETAPAS, EX, ITENS, L0, NMES
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape; R0 = 19
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Orcamento-Cabana-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Orcamento-Cabana-Zion-EXEMPLO.xlsx", data_only=True)
O, S, C = W["Orçamento"], W["Resumo"], W["Cronograma"]
v = lambda r: S[f"B{r}"].value
RES = dict(sub=v(R0), res=v(R0+1), tot=v(R0+2), verba=v(R0+3), dif=v(R0+4), leit=v(R0+5), m2=v(R0+6), m2t=v(R0+7), sem=v(R0+8), um=v(R0+9),
           pago=v(R0+11), falta=v(R0+12), sit=v(R0+13))
ET = [(S[f"A{r}"].value, S[f"B{r}"].value, S[f"C{r}"].value) for r in range(5, 15)]
LIN = [dict(item=O[f"B{r}"].value, q=O[f"D{r}"].value, c=[O[f"{x}{r}"].value for x in "EFG"], h=O[f"H{r}"].value, preco=O[f"I{r}"].value,
            tot=O[f"J{r}"].value, dif=O[f"K{r}"].value, sit=O[f"L{r}"].value) for r in range(L0, L0 + len(ITENS))]
MES = [(C[f"A{r}"].value, C[f"B{r}"].value, C[f"C{r}"].value, C[f"E{r}"].value) for r in range(5, 5 + NMES) if C[f"B{r}"].value]
RESV = C[f"B{6+NMES}"].value
brl = lambda x: ("R$ " + f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) if isinstance(x, (int, float)) else ("—" if x in (None, "") else str(x))
brl0 = lambda x: (("−" if x < 0 else "") + "R$ " + f"{abs(x):,.0f}".replace(",", ".")) if isinstance(x, (int, float)) else ("—" if x in (None, "") else str(x))
pct = lambda x: f"{x*100:.0f}%".replace(".", ",") if isinstance(x, (int, float)) else "—"
cls = lambda s: "ok" if s == "OK" else ("aten" if s in ("Sem cotação", "Só 1 cotação: peça mais", "Não se aplica") else "pend")
CSS2 = CSS + ".aten{background:#FCE8B2} td.n{text-align:right;white-space:nowrap}"
achar = lambda nome: next(l for l in LIN if l["item"] == nome)
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 05 · Orçamento da Cabana</span><span>{n}/{t}</span></div>'

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-cotacoes.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:14mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-resumo.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:28mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 05 · Guia do comprador</div><h1 style="color:var(--creme)">Orçamento da Cabana</h1>
<p style="font-size:13pt;max-width:160mm">Aprenda o passo a passo para montar o orçamento da sua cabana de Airbnb, do projeto à abertura, com 3 cotações por item, reserva para imprevistos e cronograma de pagamentos.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para cabana, chalé, bubble, tiny house, módulo ou imóvel que vai virar hospedagem. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem vai construir ou montar a primeira cabana (ou chalé, bubble, tiny house, módulo) para hospedagem e quer saber quanto vai gastar antes de começar.<br>
<b>Quando usar:</b> antes de fechar com fornecedores, ao receber cotações, a cada pagamento e quando algo muda no meio da obra.</div>
<h3>Você termina com</h3><ol class="passos"><li>A lista completa do que precisa ser pago, do projeto à abertura, separada em 10 etapas.</li>
<li>Até 3 cotações por item, comparadas com a mesma especificação, e o preço escolhido de cada uma.</li>
<li>O total com reserva para imprevistos, comparado com a sua verba, e quanto sai em cada mês.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 20 minutos).</li><li>Abra o exemplo e veja as abas Orçamento, Resumo e Cronograma.</li>
<li>Revise a lista sugerida na planilha em branco: apague o que não se aplica e acrescente o que falta.</li><li>Peça as cotações com a Ficha de Cotação e lance os preços.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Orcamento-Cabana-Zion-EM-BRANCO.xlsx</td><td>Seu orçamento, com uma lista sugerida de {len(ITENS)} itens em 10 etapas</td></tr>
<tr><td>Orcamento-Cabana-Zion-EXEMPLO.xlsx</td><td>Uma cabana fictícia preenchida (valores inventados, não use como referência de preço)</td></tr>
<tr><td>Ficha-de-Cotacao.pdf</td><td>Folha para pedir e comparar 3 cotações com a mesma especificação</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    ex_et = {i: [it[1] for it in ITENS if it[0] == i + 1][:4] for i in range(10)}
    trs = "".join(f"<tr><td><b>{i+1}. {E(e)}</b></td><td>{E(', '.join(ex_et[i]))}</td></tr>" for i, e in enumerate(ETAPAS))
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · liste tudo por etapa</div><h2>Do projeto à abertura</h2>
<p>O orçamento estoura quase sempre pelo que ficou fora da lista, não pelo preço do que estava nela. Pense na cabana pronta para receber o primeiro hóspede e volte até o primeiro papel.</p>
<table><tr><th style="width:38%">Etapa</th><th>Exemplos de itens da lista sugerida</th></tr>{trs}</table>
<div class="box alerta"><b>O que costuma ficar de fora:</b> licenças e taxas, acesso e estacionamento, entrada de energia, água e esgoto, enxoval completo para as trocas, fotos, seguro e as primeiras amenidades.</div>
<div class="box"><b>Exercício 1.</b> Na planilha em branco, leia a lista sugerida etapa por etapa. Marque quantidade 0 no que não se aplica ao seu projeto e escreva aqui 3 itens que faltam na lista:<div class="linha"></div><div class="linha"></div><div class="linha"></div></div>{foot(3,T)}</section>""")
    jan, proj, fot = achar("Janelas e portas"), achar("Projeto arquitetônico"), achar("Fotos profissionais")
    tr = lambda l: f"<tr><td>{E(l['item'])}</td>" + "".join(f"<td class='n'>{brl0(x)}</td>" for x in l["c"]) + f"<td class='n'>{l['h'] or 'menor'}</td><td class='n'><b>{brl0(l['tot'])}</b></td><td class='n'>{pct(l['dif'])}</td></tr>"
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · 3 cotações, mesma especificação</div><h2>Compare o que é comparável</h2>
<ol class="passos"><li><b>Escreva a especificação antes de pedir preço:</b> material, medidas, quantidade, o que está incluído (frete, instalação, retirada de entulho), prazo e garantia. Use a Ficha de Cotação e mande a mesma para os 3.</li>
<li><b>Lance o preço unitário</b> nas colunas Cotação 1, 2 e 3 (por m², por peça ou o valor fechado do serviço). A quantidade multiplica.</li>
<li><b>Escolhida:</b> vazio = a planilha usa a menor. Marque 1, 2 ou 3 quando a mais barata não for a melhor, e anote o motivo na especificação. Para preço único (taxa da prefeitura), marque 1.</li></ol>
<div class="box ex"><span class="tag">Exemplo · dados fictícios</span><table style="margin-top:8px"><tr><th>Item</th><th>Cot. 1</th><th>Cot. 2</th><th>Cot. 3</th><th>Escolhida</th><th>Total</th><th>Diferença</th></tr>
{tr(proj)}{tr(jan)}{tr(fot)}</table>
<p style="font-size:9.5pt;margin:6px 0 0">No projeto, a cotação 1 foi escolhida porque inclui a aprovação na prefeitura. Nas janelas, a cotação 2 foi escolhida porque inclui a instalação: o total usa {brl0(jan['tot'])}, não a menor. A coluna Diferença mostra quanto a maior cotação passa da menor; diferenças grandes pedem uma segunda leitura da especificação.</p></div>
<div class="box alerta"><b>Situação de cada linha:</b> "Só 1 cotação: peça mais" e "Sem cotação" deixam o orçamento incompleto. "Pago acima do orçado" e "Cotação escolhida vazia" pedem conferência.</div>{foot(4,T)}</section>""")
    tre = "".join(f"<tr><td>{E(n)}</td><td class='n'>{brl0(b)}</td><td class='n'>{pct(c)}</td></tr>" for n, b, c in ET)
    cor = "ok" if RES["leit"] == "Cabe na verba" else "pend"
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · reserva e verba</div><h2>Cabe na verba?</h2>
<p>A aba Resumo soma os itens por etapa, acrescenta a reserva para imprevistos e compara com a verba que você informou.</p>
<div style="display:flex;gap:12px"><table style="flex:1.3"><tr><th>Etapa (exemplo fictício)</th><th>Total</th><th>%</th></tr>{tre}</table>
<table style="flex:1"><tr><th>Resultado</th><th>Valor</th></tr><tr><td>Subtotal</td><td class='n'>{brl0(RES['sub'])}</td></tr>
<tr><td>Reserva ({EX['reserva']}%)</td><td class='n'>{brl0(RES['res'])}</td></tr><tr><td><b>Total com reserva</b></td><td class='n'><b>{brl0(RES['tot'])}</b></td></tr>
<tr><td>Verba</td><td class='n'>{brl0(RES['verba'])}</td></tr><tr><td><b>Diferença</b></td><td class='n {cor}'><b>{brl0(RES['dif'])}</b></td></tr>
<tr><td>Custo por m² interno</td><td class='n'>{brl0(RES['m2'])}</td></tr></table></div>
<div class="box"><b>Como ler o exemplo:</b> o total com reserva passa da verba em {brl0(-RES['dif']) if isinstance(RES['dif'], (int, float)) and RES['dif'] < 0 else '—'}, e ainda há {RES['sem']} item sem cotação e {RES['um']} com só 1 cotação. Antes de começar a obra, há três saídas: <b>cortar</b> (tirar o item), <b>trocar</b> (outra especificação, com nova cotação) ou <b>adiar</b> para uma segunda fase, marcando quantidade 0, como a hidromassagem do exemplo.</div>
<div class="box alerta"><b>A reserva não é sobra.</b> O valor da reserva é só um ponto de partida: ajuste ao seu projeto e converse com o profissional responsável pela obra.</div>
<div class="box"><b>Exercício 2.</b> Se o seu total passar da verba, escreva 3 itens que você pode cortar, trocar ou adiar, e quanto cada um muda o total:<div class="linha"></div><div class="linha"></div></div>{foot(5,T)}</section>""")
    trm = "".join(f"<tr><td>{E(a)}</td><td class='n'>{brl0(b)}</td><td class='n'>{brl0(c)}</td><td class='n'>{brl0(d)}</td></tr>" for a, b, c, d in MES)
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · cronograma de pagamentos</div><h2>Quanto sai em cada mês</h2>
<p>Em cada item, informe o mês previsto do pagamento (mês 1 = primeiro mês do projeto) e o que já pagou. A aba Cronograma soma tudo por mês e mostra o acumulado.</p>
<div class="box ex"><span class="tag">Exemplo · dados fictícios</span><table style="margin-top:8px"><tr><th>Mês</th><th>Previsto</th><th>Já pago</th><th>Acumulado</th></tr>{trm}
<tr><td>Reserva para imprevistos</td><td class='n'>{brl0(RESV)}</td><td></td><td></td></tr></table></div>
<div class="box"><b>Para que serve:</b> ver se o dinheiro estará disponível no mês em que cada pagamento vence, e não só no total. No exemplo, os meses da estrutura concentram a maior saída. Já pago: {brl0(RES['pago'])}; falta pagar, com a reserva: {brl0(RES['falta'])}.</div>
<div class="box"><b>Exercício 3.</b> Marque o mês de cada item do seu orçamento e escreva o mês com a maior saída e de onde virá esse dinheiro:<div class="linha"></div><div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Lista completa</td><td>As 10 etapas revisadas; nada esquecido entre o projeto e a abertura</td></tr>
<tr><td>Cotações comparáveis</td><td>3 cotações por item com a mesma especificação; a Situação do orçamento diz "Completo"</td></tr>
<tr><td>Verba</td><td>Total com reserva dentro da verba, ou cortes, trocas e adiamentos decididos</td></tr>
<tr><td>Caixa</td><td>Cada item com mês de pagamento e o dinheiro disponível no mês de maior saída</td></tr>
<tr><td>Acompanhamento</td><td>Já pago atualizado a cada pagamento</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Revisei a lista sugerida &nbsp; ☐ Usei a Ficha de Cotação &nbsp; ☐ Pedi 3 cotações por item &nbsp; ☐ Defini a reserva<br>
☐ Comparei com a verba &nbsp; ☐ Decidi cortes, trocas ou adiamentos &nbsp; ☐ Marquei o mês de cada pagamento</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>Não informa preços de mercado: os valores do exemplo são inventados e não servem como referência.</li>
<li>Não substitui o projeto, o memorial descritivo nem o profissional responsável pela obra.</li>
<li>Não diz se a construção é permitida no seu terreno: isso depende das regras do município e dos órgãos ambientais.</li>
<li>Não calcula diária, ocupação nem retorno do investimento.</li>
<li>Uma cabana por arquivo (duplique o arquivo para comparar modelos).</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplo com projeto, valores e fornecedores fictícios. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def ficha():
    campos = ["Fornecedor e contato", "Preço unitário (R$)", "Quantidade", "Total (R$)", "O que inclui (frete, instalação, material, entulho)",
              "Prazo de entrega ou execução", "Validade da proposta", "Forma de pagamento", "Garantia"]
    trs = "".join(f"<tr><td style='width:28%;font-size:9pt'>{c}</td><td></td><td></td><td></td></tr>" for c in campos)
    cab = "".join(f'<div style="flex:1 1 45%"><span style="font-size:8.5pt">{r}</span><div class="linha"></div></div>' for r in
                  ("Projeto", "Etapa", "Item", "Unidade (m², peça, serviço fechado)"))
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:12mm}} body{{background:#fff}} td{{height:44px}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 05</div>
<h2 style="font-size:22pt">Ficha de cotação</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<div style="display:flex;flex-wrap:wrap;gap:4px 18px;margin:4px 0 8px">{cab}</div>
<div class="box" style="margin:6px 0"><b style="font-size:9.5pt">Especificação (mande esta mesma descrição para os 3 fornecedores):</b><div class="linha"></div><div class="linha"></div><div class="linha"></div></div>
<table><tr><th></th><th>Cotação 1</th><th>Cotação 2</th><th>Cotação 3</th></tr>{trs}</table>
<div class="box" style="font-size:9.5pt;margin-top:10px"><b>Escolhida:</b> ☐ 1 &nbsp; ☐ 2 &nbsp; ☐ 3 &nbsp;&nbsp; <b>Por quê:</b> ____________________________________________<br>
<b>Mês previsto do pagamento:</b> ______ &nbsp; <b>Sinal ou entrada:</b> R$ __________</div>
<div class="box" style="font-size:9.5pt"><b>Antes de fechar, confira:</b> ☐ as 3 cotações têm a mesma especificação &nbsp; ☐ o que não está incluído foi orçado em outro item &nbsp; ☐ proposta por escrito e dentro da validade</div>
<p style="font-size:8.5pt;color:#6b6656">Depois, lance os preços unitários nas colunas Cotação 1, 2 e 3 da planilha. Imprima uma ficha por item.</p></body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Orçamento da Cabana · Ferramenta 05</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Valores calculados pela planilha da Ferramenta 05.</div></body></html>"""
lin = lambda a, b, c="": f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;white-space:nowrap;font-weight:600">{b}</span></div>'
resumo = (lin("Subtotal dos itens", brl0(RES["sub"])) + lin(f"Reserva ({EX['reserva']}%)", brl0(RES["res"])) + lin("Total com reserva", brl0(RES["tot"])) +
          lin("Verba disponível", brl0(RES["verba"])) + lin("Diferença", brl0(RES["dif"]), "pend" if RES["leit"] != "Cabe na verba" else "ok") +
          lin("Custo por m² interno", brl0(RES["m2"])) + lin("Itens sem cotação", str(RES["sem"]), "aten") + lin("Itens com só 1 cotação", str(RES["um"]), "aten"))
sel = ["Projeto arquitetônico", "Fundação", "Janelas e portas", "Acesso e estacionamento", "Cortinas", "Hidromassagem externa"]
cot = "".join(lin(E(l["item"]), f"{brl0(l['tot']) if l['tot'] not in (None, '') else ''} · {l['sit']}".strip(" ·"), cls(l["sit"])) for l in (achar(n) for n in sel))
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(ficha(), encoding="utf-8")
(BUILD / "demo-resumo.html").write_text(demo("Resumo do orçamento", RES["leit"], "#F4C7C3" if RES["leit"] != "Cabe na verba" else "#C8E6C0", resumo), encoding="utf-8")
(BUILD / "demo-cotacoes.html").write_text(demo("Itens e cotações", RES["sit"], "#FCE8B2", cot), encoding="utf-8")
print(RES)

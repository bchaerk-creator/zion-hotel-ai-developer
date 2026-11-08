"""Gera guia, ficha da experiência e demonstração da Ferramenta 29 com valores REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from dados import EX, EX_FIXOS, EX_VAR
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape; R0 = 31
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Custos-Experiencias-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Custos-Experiencias-Zion-EXEMPLO.xlsx", data_only=True)
C, S = W["Calculadora"], W["Cenários"]
v = lambda r: C[f"B{r}"].value
RES = dict(sit=v(R0), rec=v(R0+1), tx=v(R0+2), var=v(R0+3), fx=v(R0+4), contrib=v(R0+5), porp=v(R0+6), leitura=v(R0+7), unit=v(R0+9), minimo=v(R0+10), cabe=v(R0+11), pmin=v(R0+12),
           totfx=C["B28"].value, totcv=C["E28"].value)
CEN = [[S[f"{c}{r}"].value for c in "ABCDEFG"] for r in range(5, 45) if S[f"A{r}"].value not in ("", None)]
brl = lambda x: ("R$ " + f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) if isinstance(x, (int, float)) else str(x)
cls = lambda s: {"Cobre": "ok", "Não cobre": "pend", "Empata": "aten"}.get(s, "")
CSS2 = CSS + ".aten{background:#FCE8B2}"
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 29 · Calculadora de Custos de Experiências</span><span>{n}/{t}</span></div>'

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-resultado.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:16mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-cenarios.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:30mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 29 · Guia do comprador</div><h1 style="color:var(--creme)">Calculadora de Custos de Experiências</h1>
<p style="font-size:13pt;max-width:155mm">Aprenda o passo a passo para calcular quanto custa cada sessão de uma experiência, quanto sobra depois das taxas e a partir de quantos participantes ela se paga.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas, glampings e quem oferece experiências. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem oferece ou quer oferecer uma experiência junto com a hospedagem (café especial, passeio, trilha, aula, jantar, cavalgada) e precisa saber se o preço cobre os custos.<br>
<b>Quando usar:</b> antes de anunciar a experiência, ao rever o preço e quando um custo muda.</div>
<h3>Você termina com</h3><ol class="passos"><li>Todos os custos da experiência separados entre os da sessão e os de cada participante.</li>
<li>Quanto sobra numa sessão com o número de participantes que você espera.</li><li>Quantos participantes são necessários para cobrir a sessão e o preço mínimo para o seu cenário.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja os resultados e a aba Cenários.</li>
<li>Preencha a Ficha da Experiência à mão, com os custos que você conhece.</li><li>Passe os números para a planilha em branco e leia os resultados.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Custos-Experiencias-Zion-EM-BRANCO.xlsx</td><td>Sua calculadora: dados, custos, resultados e cenários</td></tr>
<tr><td>Custos-Experiencias-Zion-EXEMPLO.xlsx</td><td>Uma experiência fictícia preenchida</td></tr>
<tr><td>Ficha-da-Experiencia.pdf</td><td>Folha para levantar custos, capacidade e responsabilidades antes de abrir a planilha</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    fx = "".join(f"<tr><td>{E(n)}</td><td>{brl(x)}</td></tr>" for n, x in EX_FIXOS); cv = "".join(f"<tr><td>{E(n)}</td><td>{brl(x)}</td></tr>" for n, x in EX_VAR)
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · separe os custos</div><h2>Custo da sessão ou custo por pessoa?</h2>
<p>A pergunta para cada custo é: <b>ele muda se vier mais uma pessoa?</b></p>
<table><tr><th>Tipo</th><th>Pergunta</th><th>Exemplos</th></tr>
<tr><td><b>Custo da sessão</b></td><td>Pago por saída, venha 1 ou 10 pessoas</td><td>Guia, transporte, aluguel do espaço, seguro do grupo, gás da cozinha</td></tr>
<tr><td><b>Custo por participante</b></td><td>Aumenta a cada pessoa</td><td>Comida, bebida, ingresso, kit, material, aluguel de equipamento individual</td></tr></table>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · {E(EX['nome'])}</span>
<div style="display:flex;gap:12px;margin-top:8px"><table style="flex:1"><tr><th>Custos da sessão</th><th>R$</th></tr>{fx}<tr><td><b>Total</b></td><td><b>{brl(RES['totfx'])}</b></td></tr></table>
<table style="flex:1"><tr><th>Custos por participante</th><th>R$</th></tr>{cv}<tr><td><b>Total</b></td><td><b>{brl(RES['totcv'])}</b></td></tr></table></div></div>
<div class="box"><b>Exercício 1.</b> Liste todos os custos da sua experiência e marque ao lado de cada um: S (sessão) ou P (participante). Não esqueça o que costuma ficar de fora: seguro, deslocamento até o ponto de encontro, perda de material.<div class="linha"></div><div class="linha"></div><div class="linha"></div></div>{foot(3,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · preço, taxas e capacidade</div><h2>O que entra no topo da calculadora</h2>
<ol class="passos"><li><b>Preço por participante:</b> o que o cliente paga.</li>
<li><b>Taxa sobre a venda (%):</b> o que sai do preço quando você vende (plataforma, maquininha, comissão de parceiro). Confira no extrato de quem cobra.</li>
<li><b>Impostos (%):</b> pergunte ao seu contador. Se não se aplica, use 0.</li>
<li><b>Capacidade informada:</b> quantas pessoas cabem por sessão com segurança, conforme você ou o responsável pela atividade definir. A planilha não calcula isso.</li>
<li><b>Participantes previstos:</b> quantas pessoas você espera numa sessão comum. Seja conservador.</li></ol>
<div class="box ex"><span class="tag">Exemplo · dados fictícios</span> Preço {brl(EX['preco'])} · taxa {EX['taxa']}% · impostos {EX['imposto']}% · capacidade {EX['capacidade']} · previstos {EX['previstos']}.</div>
<div class="box alerta"><b>Segurança e regras:</b> atividades como trilha, passeio de barco, cavalgada ou aulas com equipamento podem exigir guia habilitado, seguro e autorizações. Confira com quem regula a atividade na sua região antes de vender.</div>{foot(4,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · leia os resultados</div><h2>Quanto sobra e quantas pessoas são precisas</h2>
<p><b>Demonstração</b> com a planilha de exemplo (valores calculados pela própria planilha):</p>
<table><tr><th>Resultado</th><th>Valor</th></tr>
<tr><td>Receita da sessão ({EX['previstos']} participantes)</td><td>{brl(RES['rec'])}</td></tr><tr><td>Taxas e impostos</td><td>{brl(RES['tx'])}</td></tr>
<tr><td>Custos por participante (total)</td><td>{brl(RES['var'])}</td></tr><tr><td>Custos da sessão</td><td>{brl(RES['fx'])}</td></tr>
<tr><td><b>Contribuição da sessão</b></td><td class="ok"><b>{brl(RES['contrib'])}</b></td></tr><tr><td>Quanto sobra de cada participante, antes dos custos da sessão</td><td>{brl(RES['unit'])}</td></tr>
<tr><td><b>Participantes mínimos para cobrir a sessão</b></td><td><b>{RES['minimo']}</b> (cabe na capacidade? {E(str(RES['cabe']))})</td></tr>
<tr><td><b>Preço mínimo para {EX['previstos']} participantes</b></td><td><b>{brl(RES['pmin'])}</b></td></tr></table>
<div class="box"><b>Como ler o exemplo:</b> com 8 pessoas a sessão cobre os custos, mas sobra pouco ({brl(RES['contrib'])}). Com 7, não cobre. O preço de {brl(EX['preco'])} está perto do mínimo ({brl(RES['pmin'])}). Antes de anunciar, valeria rever preço, custos ou o número mínimo de participantes para confirmar a saída.</div>
<div class="box alerta"><b>Contribuição não é lucro.</b> Ela ainda precisa pagar seu tempo, as despesas fixas do mês, a divulgação e os impostos sobre o resultado.</div>{foot(5,T)}</section>""")
    tr = "".join(f"<tr><td>{r[0]}</td><td>{brl(r[1])}</td><td>{brl(r[5])}</td><td class='{cls(r[6])}'>{E(str(r[6]))}</td></tr>" for r in CEN)
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · aba Cenários</div><h2>Defina o mínimo para confirmar a saída</h2>
<p>A aba Cenários mostra o resultado para cada número de participantes, até a capacidade informada. Use para decidir o mínimo de inscritos para confirmar uma sessão.</p>
<div class="box ex"><span class="tag">Exemplo · dados fictícios</span><table style="margin-top:8px"><tr><th>Participantes</th><th>Receita</th><th>Contribuição</th><th>Leitura</th></tr>{tr}</table></div>
<div class="box"><b>Exercício 2.</b> Com a sua experiência na planilha, escreva: mínimo de participantes para confirmar, preço que você vai praticar e o que fará quando não atingir o mínimo (remarcar, juntar grupos, devolver o valor). Combine isso por escrito com o cliente antes da compra.<div class="linha"></div><div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Custos completos</td><td>Cada custo marcado como sessão ou participante; nenhum esquecido (seguro, deslocamento, perdas)</td></tr>
<tr><td>Taxas reais</td><td>Taxa e impostos conferidos no extrato e com o contador</td></tr>
<tr><td>Decisão clara</td><td>Mínimo de participantes e preço definidos e escritos na regra de confirmação</td></tr>
<tr><td>Revisão</td><td>Planilha atualizada quando um custo mudar</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Preenchi a Ficha da Experiência &nbsp; ☐ Separei custos da sessão e por participante &nbsp; ☐ Conferi taxa e impostos<br>
☐ Defini o mínimo para confirmar a saída &nbsp; ☐ Conferi o preço mínimo &nbsp; ☐ Escrevi a regra para quando não atingir o mínimo</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>Calcula com os números que você informa; não prevê procura nem quantas pessoas vão comprar.</li>
<li>Contribuição não é lucro: não inclui seu tempo, despesas fixas do negócio, divulgação nem imposto de renda.</li>
<li>Capacidade, segurança, licenças e seguros dependem da atividade e do profissional responsável.</li>
<li>Uma experiência por arquivo (duplique o arquivo para comparar experiências ou preços).</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplo com experiência, preços e custos fictícios. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def ficha():
    lin = lambda n: "".join("<tr><td>&nbsp;</td><td></td></tr>" for _ in range(n))
    cab = "".join(f'<div style="flex:1 1 45%"><span style="font-size:8.5pt">{r}</span><div class="linha"></div></div>' for r in
                  ("Experiência", "Preço por participante", "Duração e horários", "Capacidade informada (quem definiu?)", "Responsável pela atividade", "O que está incluído"))
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:12mm}} body{{background:#fff}} td{{height:22px;font-size:9.5pt}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 29</div>
<h2 style="font-size:22pt">Ficha da experiência</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<div style="display:flex;flex-wrap:wrap;gap:4px 18px;margin:4px 0 10px">{cab}</div>
<div style="display:flex;gap:14px"><table style="flex:1"><tr><th>Custos da sessão (por saída)</th><th style="width:28%">R$</th></tr>{lin(8)}</table>
<table style="flex:1"><tr><th>Custos por participante</th><th style="width:28%">R$</th></tr>{lin(8)}</table></div>
<div class="box" style="font-size:9.5pt;margin-top:10px"><b>Taxa sobre a venda:</b> ____ % (plataforma, cartão, comissão) &nbsp; <b>Impostos:</b> ____ % (com o contador)<br>
<b>Mínimo para confirmar a saída:</b> ____ participantes &nbsp; <b>Se não atingir:</b> ______________________________</div>
<div class="box" style="font-size:9.5pt"><b>Antes de vender, confira:</b> ☐ seguro do grupo &nbsp; ☐ autorizações da atividade &nbsp; ☐ guia ou responsável habilitado &nbsp; ☐ restrições (idade, saúde, alimentação) informadas ao cliente</div>
<p style="font-size:8.5pt;color:#6b6656">Depois, passe os números para a planilha.</p></body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Custos de Experiências · Ferramenta 29</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Valores calculados pela planilha da Ferramenta 29.</div></body></html>"""
lin = lambda a, b, c="": f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;white-space:nowrap;font-weight:600">{b}</span></div>'
resultado = (lin("Receita (8 pessoas)", brl(RES["rec"])) + lin("Taxas e impostos", brl(RES["tx"])) + lin("Custos por participante", brl(RES["var"])) +
             lin("Custos da sessão", brl(RES["fx"])) + lin("Contribuição da sessão", brl(RES["contrib"]), "ok") + lin("Mínimo para cobrir", f"{RES['minimo']} pessoas") +
             lin("Preço mínimo (8 pessoas)", brl(RES["pmin"])))
cen = "".join(lin(f"{r[0]} participantes", f"{brl(r[5])} · {r[6]}", cls(r[6])) for r in CEN if r[0] in (4, 6, 7, 8, 10, 12))
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(ficha(), encoding="utf-8")
(BUILD / "demo-resultado.html").write_text(demo("Resultado da sessão", RES["leitura"], "#C8E6C0", resultado), encoding="utf-8")
(BUILD / "demo-cenarios.html").write_text(demo("Cenários", f"Cobre a partir de {RES['minimo']} participantes", "#FCE8B2", cen), encoding="utf-8")
print(RES)

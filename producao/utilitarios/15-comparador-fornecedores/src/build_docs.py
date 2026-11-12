"""Gera guia, roteiro de cotação e demonstração da Ferramenta 15 com valores REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from dados import CRITERIOS
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Comparador-Fornecedores-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Comparador-Fornecedores-Zion-EXEMPLO.xlsx", data_only=True)
CO, S = W["Cotações"], W["Resumo"]
COT = [[CO[f"{c}{r}"].value for c in "ABCDEFGHIJKLMNOPQRST"] for r in range(7, 157) if CO[f"B{r}"].value]
RES = [[S[f"{c}{r}"].value for c in "ABCDEFGHI"] for r in range(7, 37) if S[f"A{r}"].value]
TOT = dict(nec=S["C3"].value, prontas=S["C4"].value, prob=S["C5"].value)
brl = lambda v, d=2: ("R$ " + f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")) if isinstance(v, (int, float)) else ""
num = lambda v, d=2: "" if v in (None, "") else (f"{v:.{d}f}".replace(".", ",") if isinstance(v, float) else str(v))
cls = lambda s: {"Melhor nota": "ok", "Melhor nota e menor custo": "ok", "Menor custo": "aten", "Pronto para decidir": "ok",
                 "OK": "ok", "Sem cotações válidas": "pend"}.get(s, "aten" if str(s).startswith("Peça") else "pend" if str(s).startswith("Confira") else "")
CSS2 = CSS + ".aten{background:#FCE8B2}"
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 15 · Comparador de Fornecedores</span><span>{n}/{t}</span></div>'
LAV = [c for c in COT if c[0] == "Lavanderia de enxoval"]; DET = [c for c in COT if c[0] == "Detergente multiuso"]
R0 = RES[0]

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-cotacoes.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:16mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-resumo.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:30mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 15 · Guia do comprador</div><h1 style="color:var(--creme)">Comparador de Fornecedores</h1>
<p style="font-size:13pt;max-width:155mm">Aprenda o passo a passo para comparar fornecedores da sua hospedagem pelo custo real, pelo prazo e pelo que importa para você, e escolher com critério.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas e glampings. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem compra produtos ou contrata serviços com frequência para a hospedagem (lavanderia, limpeza, papel, amenities, café, gás, manutenção) e escolhe o fornecedor pelo preço da embalagem ou por hábito.<br>
<b>Quando usar:</b> antes de fechar com um fornecedor novo e uma vez por semestre para rever os atuais.</div>
<h3>Você termina com</h3><ol class="passos"><li>Pesos claros para o que importa na sua operação: preço, prazo, qualidade, atendimento, pagamento e confiabilidade.</li>
<li>Cada cotação convertida para a mesma unidade, com frete e pedido mínimo na conta.</li>
<li>Para cada necessidade: quem tem a melhor nota, quem tem o menor custo e quanto custa a diferença por mês.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja a aba Resumo.</li>
<li>Na versão em branco, ajuste os pesos e liste 3 necessidades (cerca de 15 minutos).</li><li>Peça 3 cotações de cada uma com o Roteiro de Cotação.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Comparador-Fornecedores-Zion-EM-BRANCO.xlsx</td><td>Sua planilha: até 30 necessidades e 150 cotações</td></tr>
<tr><td>Comparador-Fornecedores-Zion-EXEMPLO.xlsx</td><td>Uma pousada fictícia com 5 necessidades e 14 cotações</td></tr>
<tr><td>Roteiro-de-Cotacao.pdf</td><td>O que pedir a cada fornecedor, igual para todos, e onde anotar as notas</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    tr = "".join(f"<tr><td>{E(n)}</td><td>{E(d)}</td><td>{p_}</td></tr>" for n, d, p_ in CRITERIOS)
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · aba Critérios</div><h2>Decida o que pesa mais</h2>
<p>O mais barato nem sempre é o melhor para a hospedagem: um fornecedor que atrasa deixa a unidade sem enxoval na troca. Antes de olhar preços, dê um peso de 0 a 5 a cada critério. Zero tira o critério da conta.</p>
<table><tr><th>Critério</th><th>O que mede</th><th>Peso pronto</th></tr>{tr}</table>
<p style="font-size:9.5pt">Os pesos que vêm na planilha são só um ponto de partida, não uma regra. Preço e prazo são calculados; as outras quatro notas são suas, de 1 a 5.</p>
<div class="box"><b>Exercício 1.</b> Pense na última vez que um fornecedor causou problema. Foi preço, atraso, qualidade ou atendimento? Ajuste os pesos para refletir isso.<div class="linha"></div><div class="linha"></div></div>{foot(3,T)}</section>""")
    tr = "".join(f"<tr><td>{E(c[1])}</td><td>{E(c[2])}</td><td>{num(c[3],0) if isinstance(c[3], int) else num(c[3],1)}</td><td>{brl(c[4])}</td><td>{brl(c[5])}</td><td>{c[6] or ''}</td><td><b>{brl(c[13])}</b></td></tr>" for c in DET)
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · abas Necessidades e Cotações</div><h2>Compare o custo real, não o preço da embalagem</h2>
<ol class="passos"><li>Na aba Necessidades, escreva o que você compra e a <b>unidade comparável</b>: litro, kg, rolo, peça, serviço.</li>
<li>Peça a mesma especificação a todos (o Roteiro de Cotação ajuda). Cotação de produto diferente não é comparação.</li>
<li>Na aba Cotações, informe a quantidade na embalagem nessa unidade (galão de 5 L = 5), o preço, o frete do pedido e o pedido mínimo.</li></ol>
<div class="box"><b>Custo comparável</b> = (preço × pedido mínimo + frete) ÷ (quantidade × pedido mínimo). Frete de R$ 25 num pedido de 4 galões pesa diferente de frete de R$ 35 num pedido de 6.</div>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · detergente multiuso</span><table style="margin-top:8px"><tr><th>Fornecedor</th><th>Embalagem</th><th>Qtd.</th><th>Preço</th><th>Frete</th><th>Mín.</th><th>Por litro</th></tr>{tr}</table>
<p style="font-size:9pt;margin:6px 0 0">O frasco de 1 L parece barato e sai mais caro por litro; o galão com maior pedido mínimo sai mais barato mesmo com frete maior.</p></div>{foot(4,T)}</section>""")
    tr = "".join(f"<tr><td>{E(c[1])}</td><td>{brl(c[13])}</td><td>{num(c[14])}</td><td>{num(c[15])}</td><td>{c[8]}·{c[9]}·{c[10]}·{c[11]}</td><td><b>{num(c[16])}</b></td><td class='{cls(c[17])}'>{E(c[17] or '')}</td></tr>" for c in LAV)
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · notas</div><h2>Dê as notas e leia a nota final</h2>
<p>Para cada cotação, dê de 1 a 5 em qualidade, atendimento, pagamento e confiabilidade. O que você ainda não sabe fica em branco: a nota final usa só o que foi preenchido.</p>
<table><tr><th>Nota</th><th>Como a planilha calcula</th></tr>
<tr><td>Preço</td><td>5 para o menor custo comparável da necessidade; os outros, em proporção</td></tr>
<tr><td>Prazo</td><td>5 para o menor prazo; os outros, em proporção (prazo vazio não conta)</td></tr>
<tr><td>Nota final</td><td>Média das notas pelos pesos, de 0 a 5, com 2 casas</td></tr>
<tr><td>Melhor nota</td><td>Maior nota final; no empate, a de menor custo</td></tr></table>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · lavanderia de enxoval</span><table style="margin-top:8px"><tr><th>Fornecedor</th><th>Por kg</th><th>Preço</th><th>Prazo</th><th>Q·A·P·C</th><th>Final</th><th>Resultado</th></tr>{tr}</table></div>
<div class="box"><b>Exercício 2.</b> Para um fornecedor atual, dê as 4 notas agora. Em qual delas você teve mais dúvida? Pergunte a quem trabalha com ele.<div class="linha"></div></div>{foot(5,T)}</section>""")
    tr = "".join(f"<tr><td>{E(r[0])}</td><td class='{cls(r[2])}'>{E(r[2])}</td><td>{E(r[3] or '')}</td><td>{E(r[6] or '')}</td><td>{brl(r[8])}</td></tr>" for r in RES)
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · aba Resumo</div><h2>Decida com o resumo</h2>
<p>O resumo mostra, para cada necessidade, quantas cotações válidas existem, quem tem a melhor nota, quem tem o menor custo e quanto custa por mês ficar com a melhor nota em vez da mais barata (quando você informou o consumo).</p>
<table><tr><th>Necessidade</th><th>Situação</th><th>Melhor nota</th><th>Menor custo</th><th>Diferença por mês</th></tr>{tr}</table>
<p style="margin-top:10px;font-size:10pt"><b>Como ler:</b> na lavanderia fictícia, a melhor nota custa {brl(R0[8])} a mais por mês que a mais barata. A pergunta é sua: o prazo e a confiabilidade valem essa diferença? A planilha mostra a conta; a decisão continua com você.</p>
<div class="box">"Peça mais cotações" aparece com menos de 3 cotações válidas. Com só 1 ou 2, você não sabe se o preço está bom.</div>
<div class="box"><b>Exercício 3.</b> Escolha uma necessidade e escreva a decisão e o motivo em uma frase.<div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Comparação justa</td><td>Mesma especificação pedida a todos; mesma unidade comparável</td></tr>
<tr><td>Cotações limpas</td><td>"Cotações com problema" igual a 0</td></tr>
<tr><td>Base suficiente</td><td>Cada necessidade importante em "Pronto para decidir" (3 cotações ou mais)</td></tr>
<tr><td>Decisão registrada</td><td>Para cada necessidade, uma frase com quem foi escolhido e por quê</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Ajustei os pesos &nbsp; ☐ Listei as necessidades com unidade e consumo &nbsp; ☐ Pedi 3 cotações com a mesma especificação<br>
☐ Dei as notas &nbsp; ☐ Li o resumo &nbsp; ☐ Registrei a decisão e marquei a próxima revisão</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>A planilha não pesquisa preços nem indica fornecedores; os valores do exemplo são inventados e não servem como referência.</li>
<li>As notas são suas. A nota final só é tão boa quanto as notas e os pesos que você colocou.</li>
<li>Não confere contrato, nota fiscal, garantia nem exigências legais do fornecedor.</li>
<li>Não garante economia: mostra a diferença calculada com o consumo que você informou.</li>
<li>Usa MAXIFS e MINIFS: funciona no Excel 2019 ou mais novo, Excel 365, Google Sheets e LibreOffice.</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplos com fornecedores, preços e notas fictícios. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def roteiro():
    perg = ["Produto ou serviço, com a especificação que você escreveu na aba Necessidades", "Tamanho da embalagem (L, kg, rolos, peças)",
            "Preço da embalagem", "Frete: quanto custa e se muda com o tamanho do pedido", "Pedido mínimo", "Prazo de entrega em dias, a partir do pedido",
            "Formas e prazo de pagamento; emite nota fiscal?", "Quem atende se houver problema e por qual canal"]
    li = "".join(f"<li>{E(x)}</li>" for x in perg)
    col = "".join(f"<th>{t}</th>" for t in ("Fornecedor", "Embalagem", "Preço", "Frete", "Mín.", "Prazo", "Qual.", "Atend.", "Pag.", "Conf."))
    lin = "".join("<tr>" + "<td>&nbsp;</td>" * 10 + "</tr>" for _ in range(6))
    msg = ("Olá! Estamos cotando [necessidade] para a nossa hospedagem: [especificação]. Pode nos passar o preço da embalagem, "
           "o tamanho, o frete, o pedido mínimo, o prazo de entrega e as formas de pagamento? Obrigado!")
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:12mm}} body{{background:#fff}} td{{height:26px;font-size:9.5pt}} th{{font-size:8.5pt}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 15</div>
<h2 style="font-size:22pt">Roteiro de cotação</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<div style="display:flex;gap:18px;margin:4px 0 8px"><div style="flex:1"><span style="font-size:8.5pt">Necessidade</span><div class="linha"></div></div><div style="flex:1"><span style="font-size:8.5pt">Especificação (igual para todos)</span><div class="linha"></div></div></div>
<h3 style="margin:6px 0">Pergunte a todos os fornecedores</h3><ol class="passos" style="font-size:10pt">{li}</ol>
<div class="box" style="font-size:9.5pt"><b>Mensagem modelo:</b> {E(msg)}</div>
<h3 style="margin:8px 0 4px">Anote as respostas e as suas notas (1 a 5)</h3><table><tr>{col}</tr>{lin}</table>
<p style="font-size:8.5pt;color:#6b6656;margin-top:8px">Depois, passe cada linha para a aba Cotações. Quantidade na embalagem sempre na unidade comparável da necessidade.</p></body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Comparador de Fornecedores · Ferramenta 15</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Valores calculados pela planilha da Ferramenta 15.</div></body></html>"""
lin = lambda a, b, c: f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;white-space:nowrap">{b}</span></div>'
cots = "".join(lin(f"{E(c[1])}<br><small>{brl(c[13])} por kg · nota {num(c[16])}</small>", E(c[17] or "—"), cls(c[17])) for c in LAV)
res = "".join(lin(f"{E(r[0])}<br><small>{E(r[3] or '')}</small>", E(r[2].replace(' (ideal: 3)', '')), cls(r[2])) for r in RES)
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(roteiro(), encoding="utf-8")
(BUILD / "demo-cotacoes.html").write_text(demo("Lavanderia de enxoval", "Melhor nota ≠ menor custo", "#FCE8B2", cots), encoding="utf-8")
(BUILD / "demo-resumo.html").write_text(demo("Resumo por necessidade", f"{TOT['prontas']} de {TOT['nec']} prontas para decidir", "#C8E6C0", res), encoding="utf-8")
print(TOT, R0)

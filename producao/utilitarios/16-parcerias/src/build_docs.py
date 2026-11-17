"""Gera guia, ficha de acordo e demonstração da Ferramenta 16 com valores REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from dados import TIPOS, CONTRA
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Parcerias-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Parcerias-Zion-EXEMPLO.xlsx", data_only=True)
PA, IN, P = W["Parceiros"], W["Indicações"], W["Painel"]
PAR = [[PA[f"{c}{r}"].value for c in "ABCDEFGHIJKLMN"] for r in range(7, 47) if PA[f"A{r}"].value]
IND = [[IN[f"{c}{r}"].value for c in "ABCDEFGH"] for r in range(7, 307) if IN[f"B{r}"].value]
PAI = [(P[f"A{r}"].value, P[f"B{r}"].value) for r in range(4, 14)]
LEIT = P["A16"].value
brl = lambda v: ("R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) if isinstance(v, (int, float)) else ""
dmy = lambda v: v.strftime("%d/%m") if hasattr(v, "strftime") else ""
def contra(l):
    if l[5] == "% sobre o valor": return f"{l[6]*100:.0f}% do valor"
    if l[5] == "Valor fixo por indicação": return f"{brl(l[6])} por indicação"
    return l[5] or ""
cls = lambda s: {"Ativa": "ok", "Recebido": "ok", "Sem comissão": "ok", "A receber": "aten", "Aguardando confirmação": "aten",
                 "Revisar o acordo": "aten", "Sem acordo por escrito": "aten"}.get(s, "pend" if s else "")
CSS2 = CSS + ".aten{background:#FCE8B2}"
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 16 · Kit Operacional de Parcerias</span><span>{n}/{t}</span></div>'

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-parceiros.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:16mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-indicacoes.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:30mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 16 · Guia do comprador</div><h1 style="color:var(--creme)">Kit Operacional de Parcerias</h1>
<p style="font-size:13pt;max-width:155mm">Aprenda o passo a passo para organizar as parcerias da sua hospedagem com restaurantes, guias, spas e transportes: o que cada um oferece, o que foi combinado, as indicações feitas e o que você tem a receber.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas e glampings. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem já indica restaurante, passeio ou transfer aos hóspedes, mas faz tudo de boca: não sabe o que combinou, quem confirmou nem quanto tem a receber.<br>
<b>Quando usar:</b> ao fechar uma parceria, a cada indicação e uma vez por mês para cobrar e revisar.</div>
<h3>Você termina com</h3><ol class="passos"><li>Uma lista de parceiros com o que cada um oferece ao hóspede e o que foi combinado com você.</li>
<li>O registro de cada indicação, sem dados pessoais do hóspede.</li>
<li>O que falta confirmar, o que há para receber e que acordo precisa ser revisto.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja a aba Painel.</li>
<li>Na versão em branco, cadastre os parceiros que você já indica (cerca de 20 minutos).</li><li>Preencha uma Ficha de Acordo com cada um.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Parcerias-Zion-EM-BRANCO.xlsx</td><td>Sua planilha: até 40 parceiros e 300 indicações</td></tr>
<tr><td>Parcerias-Zion-EXEMPLO.xlsx</td><td>5 parceiros e 10 indicações fictícios</td></tr>
<tr><td>Ficha-de-Acordo-com-Parceiro.pdf</td><td>Uma página para registrar o combinado com cada parceiro</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    tr = "".join(f"<tr><td>{E(str(l[0]))}</td><td>{E(str(l[3]))}</td><td>{E(str(l[4]))}</td><td>{E(contra(l))}</td><td class='{cls(l[9])}'>{E(str(l[9]))}</td></tr>" for l in PAR)
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · aba Parceiros</div><h2>Escolha poucos parceiros e combine por escrito</h2>
<p>Parceiro bom é o que você indicaria mesmo sem ganhar nada: o hóspede volta falando da experiência, e não da propaganda.</p>
<table><tr><th>Contrapartida</th><th>Como funciona</th></tr>
<tr><td>% sobre o valor</td><td>O parceiro devolve uma porcentagem do que o hóspede gastou</td></tr>
<tr><td>Valor fixo por indicação</td><td>Um valor por hóspede confirmado</td></tr>
<tr><td>Troca ou cortesia</td><td>Sem dinheiro: um benefício para os seus hóspedes ou para você</td></tr>
<tr><td>Nenhuma</td><td>Você indica porque é bom para o hóspede</td></tr></table>
<div class="box ex" style="margin-top:8px"><span class="tag">Exemplo · dados fictícios</span><table style="margin-top:8px;font-size:8.5pt"><tr><th>Parceiro</th><th>Oferece</th><th>Benefício ao hóspede</th><th>Contrapartida</th><th>Situação</th></tr>{tr}</table></div>
<div class="box"><b>Exercício 1.</b> Liste os 3 lugares que você mais indica hoje. Algum deles já sabe que você indica?<div class="linha"></div></div>{foot(3,T)}</section>""")
    tr = "".join(f"<tr><td>{dmy(i[0])}</td><td>{E(str(i[1]))}</td><td>{E(str(i[2]))}</td><td>{brl(i[3])}</td><td>{brl(i[6])}</td><td class='{cls(i[7])}'>{E(str(i[7]))}</td></tr>" for i in IND)
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · aba Indicações</div><h2>Registre cada indicação pelo código da reserva</h2>
<ol class="passos"><li>Data, parceiro e código da reserva. <b>Nunca</b> o nome, o telefone ou o documento do hóspede.</li>
<li>Se a contrapartida é porcentagem, anote o valor que o hóspede gastou (o parceiro informa).</li>
<li>Marque "Confirmada" quando o parceiro confirmar e "Recebido" quando o dinheiro entrar.</li></ol>
<div class="box ex"><span class="tag">Exemplo · dados fictícios</span><table style="margin-top:8px;font-size:8.3pt"><tr><th>Data</th><th>Parceiro</th><th>Código</th><th>Gasto</th><th>Comissão</th><th>Situação</th></tr>{tr}</table>
<p style="font-size:9pt;margin:6px 0 0">A pizzaria não está cadastrada e a indicação do restaurante de 14/11 está sem o valor gasto: as duas ficam fora das contas até serem corrigidas.</p></div>{foot(4,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · a ficha de acordo</div><h2>Combine como confirmar e quando pagar</h2>
<p>A maior parte dos problemas de parceria é o que ninguém combinou: como o parceiro sabe que o hóspede veio de você, quando paga e o que acontece se o hóspede cancelar.</p>
<table><tr><th>Combine</th><th>Exemplo</th></tr>
<tr><td>Como o hóspede se identifica</td><td>Diz o nome da hospedagem ou mostra o código da reserva</td></tr>
<tr><td>Como o parceiro confirma</td><td>Mensagem no fim do mês com os códigos atendidos</td></tr>
<tr><td>Quando e como paga</td><td>Até o dia 10 do mês seguinte, por Pix</td></tr>
<tr><td>Benefício para o hóspede</td><td>O que ele recebe por ir indicado</td></tr>
<tr><td>Quando revisar</td><td>A cada 6 meses ou se a qualidade mudar</td></tr></table>
<div class="box alerta"><b>Cuidados:</b> comissão é receita e pode ter imposto (fale com o seu contador). A ficha organiza o combinado, mas não substitui contrato revisado por advogado.</div>{foot(5,T)}</section>""")
    tr = "".join(f"<tr><td>{E(str(a))}</td><td><b>{brl(b) if 'Comissão' in str(a) else E(str(b))}</b></td></tr>" for a, b in PAI)
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · aba Painel</div><h2>Uma vez por mês: confirmar, cobrar, revisar</h2>
<div class="box ex"><span class="tag">Exemplo · dados fictícios</span><table style="margin-top:8px">{tr}</table>
<p style="margin:8px 0 0"><b>O que fazer agora:</b> {E(LEIT)}</p></div>
<div class="box"><b>Rotina mensal sugerida:</b> mande a cada parceiro a lista de códigos indicados no mês, peça a confirmação, cobre o que estiver "A receber" e veja se algum acordo chegou na data de revisão.</div>
<div class="box"><b>Exercício 2.</b> Escreva como o seu parceiro principal vai confirmar as indicações e em que dia você vai cobrar.<div class="linha"></div><div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Tudo por escrito</td><td>Nenhum parceiro "Sem acordo por escrito"</td></tr>
<tr><td>Registro limpo</td><td>"Indicações com problema" igual a 0</td></tr>
<tr><td>Nada esquecido</td><td>Nenhuma indicação "Aguardando confirmação" com mais de um mês</td></tr>
<tr><td>Privacidade</td><td>Nenhum nome ou telefone de hóspede na planilha</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Cadastrei os parceiros &nbsp; ☐ Preenchi a ficha de acordo com cada um &nbsp; ☐ Registrei as indicações pelo código<br>
☐ Pedi as confirmações do mês &nbsp; ☐ Cobrei o que estava a receber &nbsp; ☐ Marquei a próxima revisão</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>A planilha registra o que você e o parceiro combinarem; não garante que o parceiro pague.</li>
<li>Não é contabilidade nem contrato: impostos com o contador, contratos com o advogado.</li>
<li>Não envia mensagens nem cobra ninguém: você faz o contato.</li>
<li>Parceria não garante reservas nem avaliações; a qualidade do parceiro é responsabilidade de quem indica.</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplos com parceiros, contatos, valores e reservas fictícios. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def ficha():
    campo = lambda t, n=1: f'<div style="margin:5px 0"><span style="font-size:9pt;font-weight:600">{E(t)}</span>' + '<div class="linha"></div>' * n + '</div>'
    tipos = " · ".join(f"☐ {E(t)}" for t in TIPOS)
    contras = " · ".join(f"☐ {E(t)}" for t in CONTRA)
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:13mm}} body{{background:#fff}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 16</div>
<h2 style="font-size:22pt;margin:0">Ficha de acordo com parceiro</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<div style="display:flex;gap:16px"><div style="flex:2">{campo('Parceiro')}</div><div style="flex:1">{campo('Contato')}</div></div>
<div style="margin:5px 0;font-size:9pt"><b>Tipo:</b> {tipos}</div>
{campo('O que o parceiro oferece ao hóspede', 2)}
{campo('Benefício para o hóspede indicado')}
<div style="margin:5px 0;font-size:9pt"><b>Contrapartida:</b> {contras}</div>
<div style="display:flex;gap:16px"><div style="flex:1">{campo('Valor (% ou R$)')}</div><div style="flex:2">{campo('Como o hóspede se identifica')}</div></div>
{campo('Como o parceiro confirma as indicações', 2)}
<div style="display:flex;gap:16px"><div style="flex:1">{campo('Quando paga')}</div><div style="flex:1">{campo('Como paga')}</div><div style="flex:1">{campo('Revisar em')}</div></div>
{campo('O que acontece se o hóspede cancelar ou reclamar', 2)}
<div style="display:flex;gap:24px;margin-top:14px"><div style="flex:1">{campo('Assinatura da hospedagem e data')}</div><div style="flex:1">{campo('Assinatura do parceiro e data')}</div></div>
<p style="font-size:8.5pt;color:#6b6656;margin-top:8px">Registro do combinado; não substitui contrato revisado por advogado. Depois, cadastre o parceiro na aba Parceiros.</p></body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Parcerias · Ferramenta 16</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Valores calculados pela planilha da Ferramenta 16.</div></body></html>"""
lin = lambda a, b, c: f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;white-space:nowrap">{b}</span></div>'
par = "".join(lin(f"{E(str(l[0]).replace(' (fictício)', ''))}<br><small>{E(contra(l))} · a receber {brl(l[12])}</small>", E(str(l[9])), cls(l[9])) for l in PAR)
ind = "".join(lin(f"{dmy(i[0])} · {E(str(i[1]).replace(' (fictício)', '').replace(' (fictícia)', ''))}<br><small>{E(str(i[2]))} · {brl(i[6]) or '—'}</small>", E(str(i[7])), cls(i[7])) for i in IND[:7])
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(ficha(), encoding="utf-8")
(BUILD / "demo-parceiros.html").write_text(demo("Parceiros", f"{PAI[1][1]} ativos · {PAI[2][1]} sem acordo · {PAI[3][1]} para revisar", "#FCE8B2", par), encoding="utf-8")
(BUILD / "demo-indicacoes.html").write_text(demo("Indicações", f"{brl(PAI[8][1])} a receber · {brl(PAI[9][1])} recebidos", "#C8E6C0", ind), encoding="utf-8")
print(PAI, LEIT)

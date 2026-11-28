"""Gera o HTML do e-book «Aprofundamento 6B · Viabilidade» (Trilha 1 · Pilar 6), no molde visual e narrativo do e-book do
Pilar 6 e da 6A (src/estilo.py). Caso: a Marina monta a conta dela (PLANO.md, seção 7, com as decisões de Bruno da seção 13).
Todos os números vêm de src/caso.py, que confere cada valor com o plano e falha se algum divergir.
Saída: src/ebook/ebook.html. Depois:
  node src/render.js src/ebook/ebook.html ../../../docs/trilha1/materiais/Pilar-6B-Viabilidade-ebook.pdf --min 50 --max 60
Uso: python3 -I src/build_ebook.py"""
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from estilo import css, AVISO, FICT, CURSO
import caso as c

OUT = pathlib.Path(__file__).resolve().parent / "ebook"; OUT.mkdir(exist_ok=True)
brl, num, pct, dec = c.brl, c.num, c.pct, c.dec
m2 = lambda v: num(v, 2)
REF6 = "Referência orientativa da página 6, não confirmada; a Zion também vende esse tipo de estrutura."
CONT = "Resposta fictícia do contador dela, para o caso dela; não vale para você."
CEN = "Cenários, não promessas."
H = []
CHK = '<svg viewBox="0 0 24 24" style="width:.8em;height:.8em;vertical-align:-.05em"><path d="M3 13l6 6L21 5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
add = H.append
CO, BA, OT = c.C["cons"], c.C["base"], c.C["otim"]


# ---------------------------------------------------------------- peças do molde do Pilar 6 (iguais às da 6A)
def cap(nn, rotulo, titulo, deck, porque, neste, abre):
    add(f'<section class="cap"><div class="cab"><div class="k">Capítulo {nn}<b>{rotulo}</b></div><span class="n">{nn}</span>'
        f'<h2>{titulo}</h2><p class="deck">{deck}</p></div><div class="regua"></div>'
        f'<div class="porque"><div><span>Por que fazer isso</span>{porque[0]}</div><div><span>Como vamos fazer</span>{porque[1]}</div>'
        f'<div><span>Para que serve</span>{porque[2]}</div></div>'
        + bx("Neste capítulo", "", '<p class="neste">' + " · ".join(neste) + "</p>")
        + f'<p class="abre">{abre}</p>')


def fim():
    add("</section>")


def bx(k, titulo, corpo, cls=""):
    # caixas longas de texto podem continuar na página seguinte (como as tabelas longas); exemplo curto e «Pare e pense» não
    if len(corpo) > 650 and not any(x in cls.split() for x in ("pare", "ex", "levar")):
        cls = (cls + " solta").strip()
    return f'<div class="bx {cls}"><span class="k">{k}</span>' + (f"<h4>{titulo}</h4>" if titulo else "") + corpo + "</div>"


def ex(titulo, corpo, k=FICT):
    return bx(k, titulo, corpo, "ex longa" if corpo.count("<tr") > 12 else "ex")


def pare(pergunta, opcoes, resposta):
    ops = "".join(f'<p class="op"><b>{chr(65 + i)}</b>{o}</p>' for i, o in enumerate(opcoes))
    return bx("Pare e pense", "", f'<p style="font-weight:650">{pergunta}</p>{ops}<p class="ver">Ver a resposta</p><p class="resp">{resposta}</p>', "pare")


def aplic(nao, opera, titulo="No seu caso"):
    return bx("Aplicação", titulo, f"<p><b>Se você ainda não hospeda:</b> {nao}</p><p><b>Se você já opera e quer crescer:</b> {opera}</p>", "escuro-b")


def faca(titulo, campos, nota="Escreva no papel ou direto na ficha «Faça agora · A sua conta». Esta página não guarda nada."):
    corpo = "".join(f'<p style="font-weight:650;margin-bottom:.6mm">{t}</p><div class="campo{" alto" if a else ""}"></div>' for t, a in campos)
    return bx("Faça agora", titulo, corpo + f'<p class="nota">{nota}</p>', "faca")


def levar(itens):
    return bx("Para levar", "", "<ul>" + "".join(f"<li>{i}</li>" for i in itens) + "</ul>", "levar")


def cita(txt, fonte):
    return f'<div class="cita"><q>{txt}</q><small>{fonte}</small></div>'


def tab(cab, linhas, v=(), leg="", larg=None):
    col = "".join(f'<col style="width:{w}">' for w in larg) if larg else ""
    av = ' style="break-inside:avoid"' if len(linhas) <= 8 else ""
    h = f"<table{av}>{col}<thead><tr>" + "".join(f'<th class="{"v" if i in v else ""}">{x}</th>' for i, x in enumerate(cab)) + "</tr></thead><tbody>"
    for ln in linhas:
        cls = ""
        if isinstance(ln[0], str) and ln[0][:1] in "!~":
            cls = "tot" if ln[0][0] == "!" else "sub"; ln = [ln[0][1:]] + list(ln[1:])
        h += f'<tr class="{cls}">' + "".join(f'<td class="{"v" if i in v else ""}">{x}</td>' for i, x in enumerate(ln)) + "</tr>"
    return h + "</tbody></table>" + (f'<p class="leg">{leg}</p>' if leg else "")


def anos(v):
    if v is None:
        return "não se paga"
    if v == float("inf"):
        return "mais de 100 anos"
    return dec(v, 1) + " anos"


def barras(valores, rotulos, topo=None):
    topo = topo or max(abs(v) for v in valores)
    cols = []
    for v, r in zip(valores, rotulos):
        h = abs(v) / topo * 48
        pos = f"bottom:50%;height:{h:.1f}%" if v >= 0 else f"top:50%;height:{h:.1f}%"
        cols.append(f'<div class="c"><i class="{"neg" if v < 0 else ""}" style="{pos}"></i><span>{r}</span></div>')
    return '<div class="meses">' + "".join(cols) + "</div>"


def degraus(linhas):
    topo = max(v for _, _, v, _ in linhas)
    out = []
    for nome, sub, v, tipo in linhas:
        w = abs(v) / topo * 100
        out.append(f'<div class="d"><div class="t"><b>{nome}</b>{sub}</div><div><div class="bar {tipo}" style="width:{max(w, 0.6):.1f}%"></div></div>'
                   f'<div class="v">{("− " if tipo == "sai" else "")}{num(abs(v))}</div></div>')
    return '<div class="degraus">' + "".join(out) + "</div>"


def passos_html(passos, textos):
    cls = {"passa": "ok", "ajustar": "aj", "redesenhar": "rd"}
    nomes = ["1 · O ano em regime", "2 · Teste de queda", "3 · Tempo de volta", "4 · Valor presente", "5 · Colchão"]
    return '<div class="passos">' + "".join(f'<div class="{cls[p]}"><b>{n}</b>{t}<br><span class="s">{p}</span></div>' for n, t, p in zip(nomes, textos, passos)) + "</div>"


# ---------------------------------------------------------------- capa e sumário
add(f"""<div class="capa"><div class="k">Trilha 1 · Pilar 6 · Aprofundamento 6B · Método Zion</div>
<h1>Viabilidade:<br><i>a conta do seu projeto fecha?</i></h1>
<p class="deck">Com as páginas 6 e 6A na mão, a conta aberta linha por linha, da receita bruta ao que sobra depois da reserva, o primeiro ano mês a mês e a régua para decidir. Ao fim deste e-book você está pronto para a página 6B do seu Dossiê, Viabilidade.</p>
<div class="pe">{CURSO}</div><span class="num">6B</span></div>""")

SUM = [("00", "Como usar este aprofundamento"), ("01", "A página 6 da Marina é o ponto de partida"),
       ("02", "Seis degraus da receita ao que sobra"), ("03", "Quanto entra: a receita se mede, não se deseja"),
       ("04", "Do bruto ao real: o que sai antes de você ver o dinheiro"), ("05", "Quanto sai: o custo de cada noite e o custo de cada mês"),
       ("06", "Quanto sobra: a margem que sai da sua lista"), ("07", "O primeiro ano e o caixa"),
       ("08", "Vale a pena? Lucro e retorno são coisas diferentes"), ("09", "Onde a conta quebra"), ("10", "A conta da Marina, inteira"),
       ("11", "Quando a conta não fecha: uma alavanca por vez"), ("12", "Pratique com a Marina"), ("13", "A página 6B e a volta"),
       (CHK, "Confira o que ficou")]
add('<div class="sum"><div class="k">Sumário</div><h2>O que tem <i>neste e-book</i></h2><table>'
    + "".join(f'<tr><td class="n">{n}</td><td>{t}</td></tr>' for n, t in SUM) + "</table></div>")

# ---------------------------------------------------------------- 00
cap("00", "Antes de começar", "Como usar <i>este aprofundamento</i>",
    "Ele acompanha o Pilar 6, depois da 6A. A aula mostra o caminho; aqui você monta a conta com calma, com calculadora e com as páginas 2, 4, 6 e 6A do Dossiê abertas ao lado.",
    ["A página 6 fechou o ano com uma margem de referência. Antes de assinar a obra, a resposta precisa vir da sua lista de custos.",
     "Abrindo a linha «quanto sobra» em seis degraus, com o primeiro ano mês a mês e a régua da Zion, com a Marina do começo ao fim.",
     "Para você sair com a página 6B do Dossiê, uma decisão escrita e o critério para parar."],
    ["Este aprofundamento em três respostas", "Antes que você pense", "Duas situações, o mesmo método", "Como ler", "Revisite · Pilares 2, 4, 6 e 6A"],
    "Seja bem-vindo ao aprofundamento 6B. Você já fez a página 6 no Pilar 6 e abriu o custo de abrir a porta na 6A. Aqui a página 6 ganha mais uma irmã, a 6B, que abre a linha que faltava: quanto sobra.")
add(bx("Antes de começar", "Este aprofundamento em <i>três respostas</i>", """<div class="tres">
<div><span class="nn">1</span><b>O que você vai aprender</b><ul><li>Os seis degraus da receita bruta ao que sobra</li><li>O ponto de equilíbrio e a folga</li><li>O primeiro ano mês a mês e o colchão</li><li>O tempo de volta em escada e a régua em cinco passos</li></ul></div>
<div><span class="nn">2</span><b>Por que aprender isso</b><ul><li>Faturamento não é lucro</li><li>Lucro não é retorno</li><li>A margem de referência não mostra o mês que aperta</li><li>Decidir antes da obra custa menos do que decidir depois</li></ul></div>
<div><span class="nn">3</span><b>O resultado que você vai ter</b><ul><li>A página 6B, com a conta aberta e a origem de cada número</li><li>O veredito escrito e o critério para parar</li><li>A ação de 30 dias</li><li>A página 6 e a Planilha 2 prontas para refazer</li></ul></div></div>"""))
add('<div class="pergunta"><span>?</span>Com a minha lista de custos, o meu trabalho e a reserva de reposição dentro, quanto sobra no ano, quanto tempo o investimento leva para voltar, e eu avanço, ajusto ou redesenho?</div>')
add("<p>A pergunta do pilar continua a mesma: <b>o negócio se paga?</b> A 6B não troca de assunto. A página 6 respondeu com a margem de referência; agora a resposta vem da sua lista. Você monta a receita com a diária e a curva do ano do Pilar 2, os três cenários do Pilar 4 e o investimento da 6A, e desce, degrau por degrau, até o que sobra.</p>"
    "<p>A primeira versão sai em uma tarde, mesmo com a linha do imposto em branco. " + CEN + "</p>")
add(bx("Antes que você pense", "Três dúvidas comuns neste ponto",
       "<p><b>«Já fiz a página 6. A conta não fechou?»</b> A página 6 fez a primeira conta, com uma margem de referência que o próprio Pilar 6 chama de simplificação. A 6B é o passo que o Pilar 6 pediu: a margem que sai da sua lista de custos, com o seu trabalho e a reserva de reposição dentro.</p>"
       "<p><b>«Não tenho a resposta do contador.»</b> Comece mesmo assim. A linha do imposto fica em branco, com o nome, e o resultado sai «antes do imposto sobre a receita». Uma linha em branco vale mais do que um número inventado (Pilar 6).</p>"
       "<p><b>«E se a conta não fechar?»</b> Então ela fez o trabalho dela, no papel, antes da obra. Quando a conta não fecha, a conta está certa (Jornada do COMO, Etapa 02). O capítulo 11 mostra o que fazer: mexer uma alavanca por vez.</p>", "crit"))
add(bx("Duas situações, o mesmo método", "",
       "<p>Na primeira tela da ficha você escolhe a sua situação com as mesmas palavras do Marco Zero: <b>«Tenho um terreno e ainda não hospedo ninguém»</b>, <b>«Tenho uma ideia, ou o capital, e ainda não tenho o terreno»</b> ou <b>«Já opero uma hospedagem e quero crescer»</b>. O método serve para Airbnb, casas, apartamentos, pousadas e glampings.</p>"
       "<p><b>Se você ainda não hospeda:</b> faça a conta da fase um sobre a 6A, a diária e a ocupação do Pilar 2 e os cenários do Pilar 4. Sem terreno escolhido, a 6A ainda não fechou: a conta serve de ensaio, com aviso.</p>"
       "<p><b>Se você já opera e quer crescer:</b> troque cada estimativa de receita e custo pelo seu extrato de doze meses e faça a conta <b>da ampliação</b>: só a receita e os custos que a ampliação acrescenta. Não pague a obra com o caixa da operação.</p>"
       "", "escuro-b"))
add(bx("Como ler", "Três tipos de caixa", f"""<ul>
<li><b>Caixas de exemplo:</b> a Marina continua com a gente, como exemplo ilustrativo. A margem de 40% da página 6 dela leva o rótulo «{REF6[0].lower() + REF6[1:-1]}». Os números novos levam «{FICT}» A resposta do contador dela leva «{CONT[0].lower() + CONT[1:-1]}». Eles ensinam a conta. Não dizem quanto fatura, custa ou rende o seu projeto.</li>
<li><b>«Faça agora»</b> e <b>«Pare e pense»:</b> escreva no papel ou na ficha; responda de cabeça antes de ler a resposta.</li>
<li><b>A convenção das contas:</b> reais de hoje, sem crescimento (moeda constante); ano de 365 noites por unidade; cada conta fecha com «Conferência: … Bate.»; «cerca de» antes de número arredondado. Todo resultado é cenário, não promessa.</li></ul>
<p class="nota">{AVISO}</p>"""))
add(bx("Revisite · Pilares 2, 4, 6 e 6A", "Quatro perguntas, sem voltar às páginas",
       "<p>1 · Qual é a diária média da Marina e a ocupação média do ano dela (Pilar 2)? 2 · Qual é a receita bruta dela no cenário conservador (Pilar 4)? 3 · Que margem a página 6 dela usou, e até quanto o investimento aguentava em 8 anos (Pilar 6)? 4 · Qual é o CAPEX da fase e o investimento total na 6A?</p>"
       f"<p>(Respostas: 1 · R$ 645 e 38,5%; 2 · {brl(CO['bruta'], 2)}, cerca de R$ 272 mil; 3 · 40%, a margem de referência, e até cerca de R$ 870 mil; 4 · {brl(c.CAPEX)} e {brl(c.INVEST6A, 2)}.)</p>"))
fim()

# ---------------------------------------------------------------- 01
cap("01", "Onde você está", "A página 6 da Marina <i>é o ponto de partida</i>",
    "Uma primeira conta inteira, com a margem de referência, e a 6A dentro do limite. A 6B começa exatamente onde as duas pararam.",
    ["Quem parte do zero refaz o que já fez. Quem parte das páginas 6 e 6A sabe qual linha falta abrir.",
     "Relendo a conta do Pilar 6 da Marina, a 6A dela e o que o Pilar 6 deixou escrito sobre a margem.",
     "Para você escrever a margem da sua página 6 e de onde ela veio."],
    ["A conta da página 6 da Marina", "A 6A dela", "O que o Pilar 6 deixou escrito", "Uma nota sobre a página 6", "O critério que ela escreveu"],
    "No Pilar 6, a Marina fez a primeira conta inteira. Três cabanas de madeira para casal, 38 m² internos e 16 m² de deck, abre com 3 e desenha para 5, opera com uma pessoa local, terreno dela de R$ 600 mil, primeira obra.")
add(ex("A conta da página 6 da Marina", tab(["Linha", "Conta", "Resultado"], [
    ["Receita bruta, conservador (Pilar 4)", "1.095 noites × 38,5% × R$ 645", brl(CO["bruta"], 2)],
    ["Margem de referência", "40%", ""],
    ["!Resultado da operação no ano", "271.915,88 × 40%", brl(CO["bruta"] * c.MARGEM6, 2)],
    ["Investimento total da fase um (página 6)", "", brl(c.P6_TOTAL, 2)],
    ["Tempo de volta", "690.529,18 ÷ 108.766,35", "6,35 anos, pouco mais de seis"],
    ["Limite de 8 anos no conservador", "8 × 108.766,35", brl(c.LIMITE6, 2) + ", cerca de R$ 870 mil"]], v=(2,), larg=("38%", "32%", "30%"))
    + f'<p class="conf">Conferência: 271.915,88 × 0,40 = 108.766,35; 8 × 108.766,35 = 870.130,80. Bate.</p><p class="nota">A margem de 40%: {REF6[0].lower() + REF6[1:]}</p>',
    k="Exemplo ilustrativo · a página 6 da Marina"))
add(f"<p>Na 6A, a Marina abriu o custo de abrir a porta em sete partes: CAPEX da fase de <b>{brl(c.CAPEX)}</b>; com o giro de {brl(c.GIRO6A, 2)}, investimento total de <b>{brl(c.INVEST6A, 2)}</b>, dentro do limite com folga de {brl(c.LIMITE6 - c.INVEST6A, 2)} (exemplo ilustrativo).</p>")
add("<h3>O que o Pilar 6 deixou escrito</h3>"
    "<p>O Pilar 6 explicou a margem com cuidado. Para uma primeira conta, antes da lista de custos cotada, ele usa a margem de referência da Zion, já descontando custos, impostos e comissões de forma simplificada. E avisa: a simplificação acerta a ordem de grandeza do ano e não mostra o mês que aperta.</p>")
add(cita("É simplificação, não promessa.", "Pilar 6 · Pré-viabilidade, cap. 05, sobre a margem de referência"))
add(cita("A margem real sai da sua lista de custos, com o seu trabalho e a reserva de reposição dentro.", "Ficha do Pilar 6, campo «Margem operacional»"))
add(bx("Uma nota sobre a página 6", "A primeira conta e a conta que decide",
       "<p>A página 6 era a primeira conta, feita com a margem de referência, e fez o que prometia: mostrou a ordem de grandeza e disse o que faltava abrir. A conta aberta, com a sua lista, é a que decide. As duas estão certas dentro da regra de cada uma. Se, com a sua lista, o número mudar muito, não é a página 6 que falhou: é a 6B fazendo o trabalho que o Pilar 6 pediu.</p>", "escuro-b"))
add("<h3>O critério que ela escreveu</h3><p>Na página 6, a Marina escreveu o critério para parar, no molde da ficha do Pilar 6:</p>")
add(cita("Se o investimento total, com a infraestrutura comum e as cotações, passar de cerca de R$ 870 mil, ou se a lista de custos mostrar uma margem que leve o conservador acima de 8 anos, eu não assino a obra: volto à conta e redesenho o tamanho, o produto ou a fase.",
         "O critério da Marina na página 6 (exemplo ilustrativo)"))
add("<p>A 6A conferiu a primeira metade do critério: o investimento coube. A 6B confere a segunda: com a lista de custos dela, o conservador leva quantos anos?</p>")
add(pare("De onde veio a margem de 40% da página 6 da Marina?", ["Da lista de custos dela", "Da margem de referência da Zion, uma simplificação para a primeira conta", "Do extrato de uma operação parecida"],
         "B. É a referência orientativa da página 6, não confirmada. A margem real sai da lista de custos, e é isso que a 6B monta."))
add(faca("O meu ponto de partida", [("A margem da minha página 6, e de onde ela veio:", False), ("O CAPEX e o giro da minha 6A:", False), ("O meu critério para parar, como escrevi na página 6:", False)]))
add(levar(["A 6B começa nas páginas 6 e 6A, não do zero.", "A margem da página 6 é referência: simplificação, não promessa.", "A margem real sai da sua lista de custos, com o seu trabalho e a reserva dentro.", "A 6B confere a segunda metade do critério que você escreveu."]))
fim()

# ---------------------------------------------------------------- 02
cap("02", "O mapa da conta", "Seis degraus <i>da receita ao que sobra</i>",
    "Uma escada só, do que o hóspede paga ao que fica. Cada saída de dinheiro mora em um degrau, e só em um.",
    ["Sem a escada, a mesma coisa é contada duas vezes, ou nenhuma.",
     "Com os seis degraus, o que entra em cada um e a caixa «Do Pilar 6 para a 6B».",
     "Para você saber onde cada saída mora antes de abrir a calculadora."],
    ["Os seis degraus", "Do Pilar 6 para a 6B", "O que fica fora desta conta"],
    "A página 6 fez a conta em uma linha: receita bruta vezes a margem. A 6B faz a mesma conta em seis degraus, para ver onde o dinheiro sai. No fim, a pergunta é a mesma: quanto sobra?")
add(cita("Faturamento não é lucro, e o custo fixo não diminui na baixa.", "Pilar 6 · Pré-viabilidade, cap. 05"))
add("<h3>Os seis degraus</h3>")
add(tab(["Degrau", "O que entra", "A pergunta-chave"], [
    ["1 · Receita bruta", "Hospedagem (noites × diária) e outras receitas (captura × ticket)", "Quanto o hóspede paga, no ano?"],
    ["2 · Receita real", "Menos o imposto sobre a receita, a comissão, o cartão e o cancelamento", "Quanto chega de fato à sua conta?"],
    ["3 · Margem de contribuição", "Menos os custos de cada noite e de cada estadia (lavanderia, amenidades, energia da noite, perdas)", "Quanto cada noite vendida deixa?"],
    ["4 · Resultado antes da reserva", "Menos os custos fixos do mês, com o seu trabalho dentro", "A operação paga as contas do mês?"],
    ["5 · Depois do modelo", "Menos aluguel do terreno, taxa de gestão ou royalty, se houver", "Quanto fica depois de quem divide a receita com você?"],
    ["6 · O que sobra", "Menos a reserva de reposição", "Quanto sobra depois de guardar para trocar o que gasta?"]], larg=("26%", "44%", "30%"), leg="A conta em seis degraus (elaboração própria a partir do e-book «Receitas, Custos e Modelos de Rentabilidade»)"))
add(ex("Os seis degraus da Marina, no conservador", degraus([
    ("1 · Receita bruta", "hospedagem", CO["bruta"], ""), ("Deduções", "imposto, comissão, cartão, cancelamento", CO["ded"], "sai"),
    ("2 · Receita real", "", CO["real"], ""), ("Custos de cada noite", "por noite e por estadia", CO["var"], "sai"),
    ("3 · Contribuição", "", CO["contrib"], ""), ("Fixos com o trabalho dela", "12 meses", CO["fixo"], "sai"),
    ("4 · Antes da reserva", "", CO["antes"], ""), ("Reserva de reposição", "3% da receita bruta", CO["reserva"], "sai"),
    ("6 · O que sobra", "o degrau 5 é zero: ela opera", CO["sobra"], "fim")])
    + '<p class="nota">Valores do ano em reais, arredondados. O capítulo 10 mostra a conta inteira, centavo a centavo, nos três cenários.</p>'))
add(bx("Do Pilar 6 para a 6B", "O que muda de uma página para a outra", tab(["Na página 6", "Na página 6B"], [
    ["Resultado = receita bruta × margem de referência de 40% (Pilar 6, cap. 05)", "Resultado = a escada de seis degraus, com a sua lista"],
    ["A mesma margem nos três cenários", "Custo fixo igual nos três; a margem sobe com a ocupação"],
    ["Giro = três meses de custo pela margem", "Giro = a maior de duas contas do próprio Pilar 6 (cap. 06), com o custo aberto"],
    ["Tempo de volta = investimento total ÷ resultado do conservador, sem rampa", "Escada: o CAPEX no ano zero, o primeiro ano com rampa, o giro testado à parte no colchão. A conta do Pilar 6 aparece ao lado"],
    ["Régua de 5, 8 e 12 anos; vereditos avançar, testar, ajustar, pausar", "Régua da Zion em cinco passos (8 e 12 anos, colchão de 10%, valor presente); vereditos Avançar, Testar, Ajustar, Pausar ou Redesenhar. O «ajustar» acima de 12 anos do Pilar 6 se chama aqui «Redesenhar»"],
    ["«O que precisa ser verdade» com a margem fixa", "A mesma pergunta com o custo aberto: cada real de diária a mais fica quase inteiro"]], larg=("44%", "56%"))))
add("<h3>O que fica fora desta conta</h3>"
    "<ul><li><b>A parcela do empréstimo da obra:</b> é o custo da captação, e mora no Pilar 7. A 6B mede se a operação devolve o investimento; o Pilar 7 decide como pagá-lo.</li>"
    "<li><b>O imposto sobre o lucro e a distribuição ao sócio:</b> dependem do regime, e quem responde é o contador.</li>"
    "<li><b>O terreno:</b> fica ao lado, nunca somado sem dizer. A conta com ele aparece à parte, com a razão escrita (capítulo 08). Fora da conta não quer dizer de graça (Pilar 6).</li>"
    "<li><b>A taxa de limpeza cobrada à parte do hóspede:</b> não é receita de hospedagem; ela paga a limpeza.</li></ul>")
add(pare("A comissão da plataforma mora em qual degrau?", ["Degrau 3, nos custos de cada noite", "Degrau 2, nas deduções", "Nos dois, por segurança"],
         "B. A comissão sai antes de o dinheiro chegar: é dedução. Contá-la também nos custos de cada noite é o erro de contar duas vezes."))
add(aplic("escreva as seis palavras da escada numa folha e, embaixo de cada uma, as saídas de dinheiro do seu projeto que você já conhece.",
          "pegue o extrato de doze meses e marque cada linha com o número do degrau. O que não couber em nenhum é pessoal, ou é do Pilar 7."))
add(levar(["Seis degraus: receita bruta, receita real, contribuição, antes da reserva, depois do modelo, o que sobra.", "Cada saída mora em um degrau só.", "O que sobra é o número que decide.", "Parcela do empréstimo, imposto sobre o lucro e terreno ficam fora, com nome."]))
fim()

# ---------------------------------------------------------------- 03
media_pat = sum(c.OCUP_TIPO.values()) / 3
rec_pat = c.NOITES_ANO * media_pat * c.DIARIA
cap("03", "Degrau 1", "Quanto entra: <i>a receita se mede, não se deseja</i>",
    "Unidades vezes ocupação vezes diária vezes dias. Cada um dos quatro números vem de um pilar, e nenhum vem da vontade.",
    ["Toda a conta depende da receita. Um erro aqui passa inteiro para os outros degraus.",
     "Com a diária média do ano, a ocupação dos doze meses, a rampa a partir do mês de abertura e as outras receitas fora da base.",
     "Para você ter uma receita que se defende diante de quem vai ler a conta."],
    ["A fórmula", "A diária média do ano", "A ocupação dos doze meses", "Ninguém abre na ocupação do destino", "Outras receitas"],
    "A receita bruta de hospedagem tem quatro números: unidades, ocupação, diária e dias. As unidades vêm da fase um do Pilar 5, a diária e a ocupação vêm do Pilar 2, e os três cenários vêm do Pilar 4. A 6B não inventa nenhum deles.")
add(tab(["Número", "De onde vem", "O erro típico"], [
    ["Unidades", "A fase um do masterplan (Pilar 5)", "Contar o projeto completo"],
    ["Diária", "A diária média do ano, medida (Pilar 2)", "Usar a diária de alta, ou a do anúncio"],
    ["Ocupação", "A média dos doze meses (Pilar 2) e os cenários do Pilar 4", "Usar a média dos patamares, ou a do destino"],
    ["Dias", "365 por unidade no ano", "Contar só os fins de semana como se fossem todos"]], larg=("18%", "42%", "40%")))
add(cita("É a diária média real que entra em todas as contas, nunca a de tabela.", "Jornada do COMO, Etapa 09, Passo 04"))
add("<h3>A ocupação dos doze meses</h3>"
    "<p>A ocupação do ano é a soma dos doze meses dividida por 12. Não é a média dos patamares. Na Marina, três meses de alta a 64%, quatro médios a 40% e cinco fracos a 22%:</p>")
add(ex("A ocupação da Marina", f"<p>(3 × 64 + 4 × 40 + 5 × 22) ÷ 12 = (192 + 160 + 110) ÷ 12 = 462 ÷ 12 = <b>38,5%</b>.</p>"
       f"<p>Se ela tirasse a média dos patamares, (64 + 40 + 22) ÷ 3 = 42%, a receita subiria para {brl(rec_pat, 2)}: {brl(rec_pat - CO['bruta'], 2)} por ano que não existem. A média dos patamares dá o mesmo peso a três meses de alta e a cinco meses fracos.</p>"
       + tab(["Tipo de mês", "Meses no calendário dela", "Ocupação", "Pontos"], [[t, ", ".join(mm for mm in c.MESES if c.CAL[mm] == t), f"{int(o * 100)}%", f"{sum(c.CAL[mm] == t for mm in c.MESES)} × {int(o * 100)} = {sum(c.CAL[mm] == t for mm in c.MESES) * int(o * 100)}"] for t, o in c.OCUP_TIPO.items()] + [["!Ano", "12 meses", "38,5%", "462"]], larg=("20%", "40%", "16%", "24%"))
       + '<p class="nota">O Pilar 2 deu quantos meses de cada tipo; a ordem dos meses no calendário é fictícia, para o exemplo.</p>'
       + f'<p class="conf">Conferência: 1.095 × 0,385 = 421,575 noites; × 645 = 271.915,88. Bate.</p>', k=FICT))
add("<h3>Ninguém abre na ocupação do destino</h3>"
    "<p>Os doze meses do Pilar 2 são o ano em regime, depois que o projeto é conhecido. O primeiro ano tem uma rampa: a ocupação começa abaixo e sobe. A 6B usa a régua da Zion: <b>40% da ocupação do mês nos meses 1 a 3, 50% nos meses 4 a 6 e 75% nos meses 7 a 12</b>, contados a partir do mês de abertura. Do mês 13 em diante, o ano em regime.</p>"
    "<p>Por isso o mês de abertura importa. Abrir no começo da alta faz a rampa cair sobre os meses mais cheios, e não custa nada. A Marina abre em <b>junho</b>, o começo da alta dela. O capítulo 07 faz a conta mês a mês.</p>")
add(cita("Ninguém abre na ocupação do destino.", "Pilar 6 · Pré-viabilidade, cap. 06"))
add("<h3>Outras receitas, fora da base</h3>"
    "<p>Cesta de café, passeio, jantar: cada outra receita entra por <b>captura × ticket</b> (quantas estadias compram, e por quanto), e com o custo próprio dela. Nunca como percentual da diária, e nunca como base da conta: a conta precisa fechar com as diárias. «Receita projetada não é desejo escrito em planilha» (Volume A05 · Investimento, cap. 08). A Marina, na conta dela, não conta com nenhuma. O capítulo 11 mostra a cesta de café como alavanca.</p>")
add(pare("A Marina quer usar 42% de ocupação, «porque é a média de alta, médio e fraco». O que está errado?", ["Nada, é a média", "A média dos patamares ignora quantos meses tem cada um; o certo é a soma dos doze meses ÷ 12", "Ela deveria usar a ocupação da alta"],
         "B. Cinco meses fracos pesam mais do que três de alta. A soma dos doze meses dá 38,5%."))
add(aplic("copie da sua página 2 a diária média, a ocupação de cada tipo de mês e quantos meses tem cada um. Escreva o seu calendário de janeiro a dezembro e o mês de abertura.",
          "use a ocupação e a diária média dos doze meses do seu extrato, mês a mês. Na conta da ampliação, a rampa vale só para as unidades novas."))
add(levar(["Receita = unidades × ocupação × diária × 365.", "Diária média do ano, nunca a de alta.", "Ocupação = soma dos doze meses ÷ 12.", "Rampa de 40%, 50% e 75% a partir do mês de abertura.", "Outras receitas por captura × ticket, com custo, fora da base."]))
fim()

# ---------------------------------------------------------------- 04
cap("04", "Degrau 2", "Do bruto ao real: <i>o que sai antes de você ver o dinheiro</i>",
    "Imposto sobre a receita, comissão, cartão e cancelamento. Quatro linhas que saem antes de qualquer custo.",
    ["São as linhas mais esquecidas, e saem de toda reserva, cheia ou vazia de lucro.",
     "Com o imposto em linha própria, a comissão separada da plataforma e do total, o cartão e o cancelamento.",
     "Para a sua receita real ser a que chega de fato à conta."],
    ["O imposto sobre a receita", "A pergunta ao contador", "Comissão por reserva × sobre o total", "Cartão e cancelamento", "Não conte duas vezes"],
    "Entre o que o hóspede paga e o que chega à sua conta existem quatro saídas. Elas não dependem de você gastar: saem de cada reserva vendida. Por isso moram no degrau 2, antes de qualquer custo.")
add(cita("Imposto sobre a receita é a omissão mais frequente e a mais cara.", "Jornada do COMO, Etapa 02, citada no e-book «Receitas, Custos e Modelos de Rentabilidade»"))
add("<h3>O imposto sobre a receita</h3>"
    "<p>O imposto sobre a receita é sempre uma linha própria. A alíquota não vem deste e-book, nem da ficha, nem de uma faixa: vem do seu contador. Anote a resposta com a data e o nome de quem respondeu. <b>Até o contador responder, a linha fica em branco</b>, com o nome, e o resultado leva o rótulo «antes do imposto sobre a receita». O Pilar 6 já pedia esse compromisso: levar a conta ao contador e anotar a resposta.</p>")
add(cita("Nada aqui substitui contador", "Volume 04 · Estratégia, cap. 13"))
add(bx("Pergunte ao seu contador", "As quatro perguntas, sem pedir número a ninguém",
       "<ul><li>Qual é o regime mais adequado para o meu caso, e qual imposto incide sobre a receita de hospedagem e sobre as outras receitas, com que alíquota efetiva?</li>"
       "<li>Em que ponto do crescimento (fase dois, fase três) essa resposta muda?</li>"
       "<li>Quais encargos incidem sobre a minha retirada e sobre o salário da pessoa local?</li>"
       "<li>Imposto sobre o lucro e distribuição ao sócio: como entram?</li></ul><p class=\"nota\">Anote a data e o nome de quem respondeu. As perguntas estão também no Checklist da página 6B.</p>", "faca"))
add("<h3>Comissão: por reserva ou sobre o total?</h3>"
    "<p>A plataforma cobra uma porcentagem <b>por reserva</b>. Mas nem toda reserva vem dela. Na conta, o que importa é a comissão <b>sobre a receita total</b>: a parte das noites vendidas pela plataforma vezes a comissão dela. As vendas diretas pagam outra coisa: a taxa do cartão.</p>"
    "<p>O cancelamento e o não comparecimento entram como dedução, em porcentagem da receita de hospedagem. A faixa citada pela fonte é de 1% a 3% (e-book «Receitas, Custos e Modelos de Rentabilidade»): fora dela, confira.</p>")
add(ex("As deduções da Marina", tab(["Linha", "Conta", "% da receita", "R$ no ano (conservador)"], [
    ["Imposto sobre a receita", "resposta do contador dela, em 20/11/2026", "6%", m2(CO["imp"])],
    ["Comissão da plataforma", "60% das noites × 15% por reserva", "9%", m2(CO["com"])],
    ["Cartão nas vendas diretas", "40% × 3%", "1,2%", m2(CO["cart"])],
    ["Cancelamento e não comparecimento", "estimativa, dentro da faixa citada", "2%", m2(CO["canc"])],
    ["!Deduções", "", "18,2%", m2(CO["ded"])],
    ["!Receita real", "271.915,88 − 49.488,69", "81,8%", m2(CO["real"])]], v=(2, 3), larg=("30%", "36%", "14%", "20%"))
    + f'<p class="conf">Conferência: 6 + 9 + 1,2 + 2 = 18,2%; 0,182 × 271.915,88 = 49.488,69. Bate.</p><p class="nota">O imposto de 6%: {CONT[0].lower() + CONT[1:]} Você deixa a sua linha em branco até falar com o seu contador.</p>'))
add("<h3>Não conte duas vezes</h3><p>A comissão e o cartão já saíram no degrau 2. Se a sua lista de custos de cada noite também tiver «comissão» ou «taxa da plataforma», tire de lá. A ficha pede a confirmação escrita: «a comissão não está também nos custos de cada noite».</p>")
add(pare("A Marina passa a vender 80% das noites pela plataforma, que cobra 15% por reserva. Qual é a comissão sobre a receita total?", ["15%", "12%", "9%"],
         "B. 0,80 × 15% = 12%. O exercício E2, no capítulo 12, refaz a conta inteira com esse número."))
add(aplic("escreva a linha do imposto em branco, com o nome do contador e a data em que você vai perguntar. Depois a parte das noites que vem da plataforma e a comissão dela.",
          "tire as quatro linhas do extrato: impostos pagos, comissões, taxas do cartão e estornos, em porcentagem da receita dos doze meses."))
add(levar(["O imposto sobre a receita é linha própria; a alíquota vem do contador, com data e nome.", "Sem resposta, em branco: o resultado sai antes do imposto.", "Comissão sobre o total = parte da plataforma × comissão por reserva.", "Cancelamento como dedução.", "A comissão não entra também nos custos de cada noite."]))
fim()

# ---------------------------------------------------------------- 05
cap("05", "Degraus 3, 4 e 5", "Quanto sai: <i>o custo de cada noite e o custo de cada mês</i>",
    "O que só existe quando alguém dorme, e o que existe mesmo com tudo vazio. Com o seu trabalho dentro.",
    ["O custo fixo é a premissa que ninguém questiona e devia. É ele que não diminui na baixa.",
     "Separando o custo de cada noite e de cada estadia do custo de cada mês, com os gastos anuais em duodécimos e a retirada.",
     "Para você ter uma lista completa, que um terceiro consegue conferir."],
    ["O custo de cada noite e de cada estadia", "O custo de cada mês", "Os gastos anuais em duodécimos", "O seu trabalho é custo", "Os custos do modelo"],
    "Há dois tipos de custo. O custo de cada noite só aparece quando a cabana está ocupada: a lavanderia, a energia da noite, as amenidades. O custo de cada mês aparece mesmo com tudo vazio: a pessoa local, o contador, o seguro, a internet.")
add("<h3>O custo de cada noite e de cada estadia</h3><p>Alguns custos acontecem a cada noite (energia, água e gás da noite; produtos de limpeza). Outros, a cada estadia, não importa quantas noites ela dure (a lavanderia do enxoval, as amenidades de boas-vindas). Para somar, divida o custo por estadia pela estadia média. Perdas e quebras de material entram em porcentagem da receita de hospedagem.</p>")
add(ex("O custo de cada noite da Marina", tab(["Linha", "Base", "Valor", "Origem"],
    [[n, "por estadia", brl(v), o] for n, v, o in c.POR_ESTADIA] + [[n, "por noite", brl(v), o] for n, v, o in c.POR_NOITE]
    + [["Perdas e quebras de material", "% da hospedagem", "1%", "estimativa"]], v=(2,), larg=("44%", "20%", "14%", "22%"))
    + f"<p>Com estadia média de 2 noites: (70 + 45) ÷ 2 = 57,50 por noite; + 28 + 12 = <b>R$ 97,50</b> por noite vendida, mais 1% da receita.</p>"
    + '<p class="conf">Conferência: 57,50 + 40 = 97,50. Bate.</p>'))
add("<h3>O custo de cada mês, com os gastos anuais em duodécimos</h3>"
    "<p>Os gastos que vêm uma vez por ano (seguro, imposto do imóvel, licença anual, 13º e férias) entram divididos por 12, o duodécimo. Quem não divide vê um mês bom virar um mês sem caixa quando o boleto chega. E a lista do que se esquece: 13º, férias e encargos, manutenção preventiva, quebra, treinamento, inadimplência e não comparecimento (Volume A05 · Investimento, cap. 9).</p>")
add(ex("Os custos de cada mês da Marina", tab(["Linha", "R$ por mês", "Origem"],
    [[n, num(v), o] for n, v, o in c.FIXOS] + [["!Subtotal dos fixos", num(c.FIX_SUB), ""],
     ["Retirada: 8 h por semana × R$ 40 × 4,33", m2(c.RETIRADA), "o valor-hora é o que ela pagaria a alguém (fictício)"],
     ["!Fixo do mês", m2(c.FIXO_MES), f"{m2(c.FIXO_ANO)} no ano"]], v=(1,), larg=("52%", "16%", "32%"))
    + '<p class="conf">Conferência: 3.600 + 600 + 400 + 500 + 350 + 650 + 300 + 150 + 800 + 450 + 200 = 8.000; 8 × 40 × 4,33 = 1.385,60; 8.000 + 1.385,60 = 9.385,60; × 12 = 112.627,20. Bate.</p>'))
add("<h3>O seu trabalho é custo</h3>"
    "<p>Se você trabalha na operação, as suas horas entram na conta: horas por semana × o valor-hora × 4,33 semanas no mês. O valor-hora não é sugerido por ninguém: é quanto você pagaria a alguém para fazer o que você faz. Se um dia você parar de fazer, alguém terá de ser pago para fazer. Sem essa linha, a conta mostra um lucro que é, na verdade, o seu salário.</p>")
add(cita("Se o negócio não paga quem o opera, ele não é um negócio.", "Jornada do COMO, Etapa 09, citada no Pilar 6 · Pré-viabilidade, cap. 05"))
add("<h3>Os custos do modelo (degrau 5)</h3><p>Se alguém divide a receita com você, essa parte sai no degrau 5: aluguel do terreno, taxa de gestão de uma administradora (em porcentagem da receita real) ou royalty de uma marca (em porcentagem da receita bruta). Contratos assim se confirmam com o advogado. A Marina opera sozinha, com a pessoa local: o degrau 5 dela é zero.</p>")
add(pare("O seguro anual da Marina custa R$ 3.600. Como ele entra na conta?", ["R$ 3.600 no mês em que vence", "R$ 300 por mês, o duodécimo", "Fica fora, porque é anual"],
         "B. Os gastos anuais entram em duodécimos. Assim o mês do boleto não pega a conta de surpresa."))
add(aplic("liste até 15 custos fixos do seu projeto, com os anuais divididos por 12, e escreva as suas horas por semana na operação e o valor-hora que você pagaria a alguém.",
          "pegue os doze meses do extrato e some cada custo fixo no ano; divida por 12. O seu trabalho entra mesmo que você nunca tenha se pago."))
add(levar(["Custo de cada noite: só existe quando alguém dorme.", "Custo por estadia ÷ estadia média = custo por noite.", "Custo de cada mês: existe mesmo vazio; anuais em duodécimos.", "O seu trabalho é custo: horas × valor-hora × 4,33.", "Quem divide a receita com você sai no degrau 5."]))
fim()

# ---------------------------------------------------------------- 06
cap("06", "Degrau 6", "Quanto sobra: <i>a margem que sai da sua lista</i>",
    "A reserva de reposição fecha a escada. Depois, três leituras: a margem, o ponto de equilíbrio com a folga e o custo de cada diária vendida.",
    ["Sem a reserva, o colchão e o enxoval são trocados com dinheiro que a conta já tinha chamado de lucro.",
     "Com a reserva desde o primeiro ano, a margem aberta, o equilíbrio lido com a folga e as três zonas da diária.",
     "Para você saber quanto sobra e o quanto a operação aguenta antes de empatar."],
    ["A reserva de reposição", "A margem aberta", "O ponto de equilíbrio e a folga", "O custo por diária vendida", "A diária de equilíbrio e o piso"],
    "O colchão, o enxoval, o deck e os eletrodomésticos se desgastam. A reserva de reposição guarda, todo ano, desde o primeiro, uma parte da receita para trocá-los quando chegar a hora.")
add("<p>As fontes citam de 3% a 6% da receita bruta (Volume A05 · Investimento: 3% a 5%; Jornada do COMO, Etapa 09: 3% a 6%); a régua da Zion usa 3%. É faixa citada pela fonte, não meta. E uma regra: <b>reserva ou depreciação, nunca as duas</b>. Somar as duas cria um prejuízo que não existe.</p>")
add(f"<p>Na Marina, cada noite deixa 645 × 0,778 − 97,50 = R$ 404,31; 421,575 × 404,31 = 170.446,99; menos os fixos de 112.627,20, sobram <b>{brl(c.SOBRA, 2)}</b>. Bate. A margem aberta dela, no conservador, é <b>21,3%</b>. É a margem que sai da lista dela. Na página 6, a margem de referência era 40%; o capítulo 10 mostra, linha por linha, de onde vem a diferença.</p>")
add(cita("Receita é vaidade. Margem é sanidade. Caixa é realidade.", "Volume A05 · Investimento, cap. 09"))
add("<h3>A régua da margem</h3>")
add(tab(["Margem do que sobra, no conservador", "Leitura"], [["30% ou mais", "boa"], ["20% a 30%", "atenção"], ["10% a 20%", "risco"], ["abaixo de 10%", "o modelo não fecha"]],
        larg=("50%", "50%"), leg="Faixa citada pela fonte; não é meta nem promessa. Vale para a margem medida depois do imposto, do cancelamento, da reserva e do trabalho do dono. Não compare com margens de outras réguas, medidas em outro degrau."))
add("<h3>O ponto de equilíbrio, lido com a folga</h3>"
    "<p>O ponto de equilíbrio é a ocupação em que o ano empata: o que as noites deixam paga exatamente os custos fixos. Divide-se o fixo do ano pelo que cada noite deixa. Sozinho, ele diz pouco. Lido ao lado da sua ocupação medida, diz quanto a operação aguenta: essa distância é a <b>folga</b>. O ano precisa fechar; o mês, não.</p>")
add(ex("O equilíbrio da Marina", f"<p>112.627,20 ÷ 404,31 = <b>{dec(c.N_EQ, 2)} noites</b>; ÷ 1.095 = <b>{pct(c.OCUP_EQ)}</b> de ocupação. A ocupação medida dela é 38,5%. Folga: 38,5 − 25,4 = <b>{dec(c.FOLGA_EQ * 100, 1)} pontos</b>.</p>"
       '<p class="conf">Conferência: 278,5665 × 404,31 = 112.627,20. Bate.</p>'
       "<p>Leitura: com folga (mais de 5 pontos). Folga negativa seria crítica; de 0 a 5 pontos, fina. A operação da Marina se paga com folga. A pergunta seguinte é outra: e o investimento? O capítulo 08 responde.</p>"))
add(cita("Acima de 70% de ocupação de equilíbrio, o problema é estrutural e não comercial.", "Jornada do COMO, Etapa 09, Passo 09"))
add("<h3>O custo por diária vendida e as três zonas</h3>"
    "<p>Divida tudo o que sai no ano (deduções, custos de cada noite, fixos e reserva) pelas noites vendidas: é o custo de cada diária vendida. Ele cria três zonas de preço.</p>")
add(ex("As três zonas da Marina", tab(["Zona", "Diária", "O que acontece"], [
    ["Paga tudo", f"acima de {brl(c.CUSTO_DIARIA, 2)}", "A noite paga a si mesma e a sua parte do fixo"],
    ["Paga a noite e parte do fixo", f"de {brl(c.PISO, 2)} a {brl(c.CUSTO_DIARIA, 2)}", "Melhor do que vazio num mês fraco; nunca nas datas de pico"],
    ["Destrói valor", f"abaixo de {brl(c.PISO, 2)}", "Cada noite vendida aumenta o prejuízo"]], larg=("30%", "30%", "40%"))
    + f"<p>Custo por diária: 214.096,09 ÷ 421,575 = {brl(c.CUSTO_DIARIA, 2)}. Piso que ainda paga a noite: 97,50 ÷ 0,778 = {brl(c.PISO, 2)}.</p>"
    f"<p><b>A diária de equilíbrio</b> (com 38,5%): cada R$ 1 de diária vale 421,575 × 0,778 = R$ 327,99 por ano. 645 − 57.819,79 ÷ 327,99 = 645 − 176,29 = <b>{brl(c.DIARIA_EQ, 2)}</b>. Abaixo disso, o ano não empata.</p>"
    '<p class="conf">Conferência: 468,71 × 0,778 − 97,50 = 267,16; × 421,575 = 112.627,20. Bate.</p>'))
add("<p>Escreva o piso antes de precisar dele. Desconto nunca abaixo do piso, nem nas datas de pico: «Piso decidido em mês fraco é piso que não existe» (Jornada do COMO, Etapa 08, Passo 03).</p>")
add(pare("O tempo de volta se calcula sobre o resultado antes ou depois da reserva de reposição?", ["Antes, porque a reserva ainda está no banco", "Depois: sobre o que sobra", "Tanto faz"],
         "B. A reserva vai ser gasta com o colchão e o enxoval. O retorno se mede sobre o que sobra depois dela."))
add(aplic("escreva a sua reserva de reposição (em porcentagem da receita bruta) e marque: reserva ou depreciação, só uma.",
          "compare o que você gastou trocando colchão, enxoval e eletrodomésticos nos últimos anos com a reserva que você separava. Se não separava, a reserva começa agora."))
add(levar(["Reserva de reposição desde o primeiro ano; reserva ou depreciação, nunca as duas.", "A margem aberta sai da sua lista.", "Equilíbrio = fixo ÷ o que cada noite deixa; leia com a folga.", "Três zonas de diária; o piso, por escrito, antes de precisar."]))
fim()

# ---------------------------------------------------------------- 07
ano1_vals = [x["res"] for x in c.ANO1]
regime_vals = [c.REGIME[c.CAL[mm]] for mm in c.ORDEM]
topo = max(abs(v) for v in ano1_vals + regime_vals)
cap("07", "O caixa", "O primeiro ano <i>e o caixa</i>",
    "O ano mês a mês, com a rampa no calendário. O mês que aperta, o giro pelas duas contas do Pilar 6 e o colchão.",
    ["O ano pode fechar no positivo e o caixa acabar num mês de março.",
     "Somando mês a mês o que as noites deixam, menos o fixo, com a rampa a partir do mês de abertura.",
     "Para você saber quanto dinheiro precisa estar no banco no dia da abertura."],
    ["O ano mês a mês", "O mês que aperta", "A reserva de sazonalidade", "O giro pelas duas contas", "O colchão e o fôlego"],
    "A conta do ano diz quanto sobra. A conta do mês diz se você chega até o fim do ano. Na Marina, o primeiro ano começa em junho, com a rampa, e atravessa cinco meses fracos.")
add(cita("Projeto não quebra por prejuízo. Quebra por falta de caixa num mês específico", "Volume 05 · Investimento, cap. 08"))
add("<p>Cada mês tem 1.095 ÷ 12 = 91,25 noites possíveis. As noites vendidas do mês são 91,25 × a ocupação do tipo do mês × a rampa. Cada noite deixa R$ 404,31. Menos o fixo do mês, R$ 9.385,60, sai o resultado do mês.</p>")
rows = []
for x in c.ANO1:
    rp = c.RAMPA[x["i"] - 1]
    oc = f"{int(c.OCUP_TIPO[x['tipo']] * 100)}% × {dec(rp, 2)} = {dec(x['o'] * 100, 1)}%"
    rows.append([str(x["i"]), x["mes"], x["tipo"], oc, dec(x["noites"], 2), m2(x["contrib"]), m2(x["res"]), ("<b>" + m2(x["acum"]) + "</b>") if x["i"] in (10, 12) else m2(x["acum"])])
rows.append(["!Ano 1", "", "", f"média {dec(sum(x['o'] for x in c.ANO1) / 12 * 100, 2)}%", dec(sum(x["noites"] for x in c.ANO1), 2), m2(sum(x["contrib"] for x in c.ANO1)), m2(c.ANO1_RES), ""])
add(ex("O primeiro ano da Marina, mês a mês (conservador)", tab(["Mês", "", "Tipo", "Ocupação × rampa", "Noites", "Contribuição", "Resultado", "Acumulado"], rows, v=(4, 5, 6, 7),
    larg=("6%", "6%", "8%", "22%", "9%", "15%", "16%", "18%"))
    + '<p class="conf">Conferência: Σ(ocupação × rampa) = 3 × 25,6 + 2 × 20 + 11 + 4 × 16,5 + 2 × 30 = 253,8 pontos; 253,8 ÷ 462 = 0,549351; 170.446,99 × 0,549351 = 93.635,16; − 112.627,20 = −18.992,04. Bate (as duas contas).</p>'))
add("<h3>O mês que aperta</h3>")
add(ex("O resultado de cada mês do primeiro ano, de junho a maio", barras(ano1_vals, c.ORDEM)
       + f"<p style=\"margin-top:7mm\">O menor saldo do primeiro ano chega em <b>março</b>, o décimo mês: <b>{brl(c.MENOR, 2)}</b>. Em regime, um mês de alta deixa {brl(c.REGIME['alta'], 2)}, um médio {brl(c.REGIME['médio'], 2)} e um fraco {brl(c.REGIME['fraco'], 2)}.</p>"
       '<p class="conf">Conferência do ano em regime: 3 × 14.226,10 + 4 × 5.371,72 − 5 × 1.269,08 = 42.678,31 + 21.486,86 − 6.345,38 = 57.819,79 = o que sobra no ano. Bate.</p>'))
add("<h3>A reserva de sazonalidade</h3><p>A alta paga o vale por decisão, não por sorte. Some o que os meses negativos do ano em regime deixam de buraco e divida pelos meses de alta: é quanto separar em cada mês de alta, numa conta à parte, no dia em que o dinheiro entra.</p>")
add(ex("A reserva de sazonalidade da Marina", f"<p>Buraco dos meses fracos: 5 × 1.269,08 = 6.345,38. Dividido por 3 meses de alta: <b>{brl(c.RES_SAZ, 2)}</b> separados em cada mês de alta.</p>"))
add("<h3>O giro pelas duas contas do Pilar 6</h3>"
    "<p>O Pilar 6 ensinou duas contas para o capital de giro, e mandou ficar com a maior. <b>Conta A:</b> três meses de custo do cenário conservador. <b>Conta B:</b> o buraco do primeiro ano, com a rampa e os meses fracos, mais três meses de custo fixo. Na página 6, o custo vinha pela margem de referência; agora vem aberto, e o giro da 6A pode mudar.</p>")
add(ex("O giro da Marina", tab(["Conta", "Como", "R$"], [
    ["Giro da 6A (página 6)", "três meses de custo pela margem de referência", m2(c.GIRO6A)],
    ["Conta A do Pilar 6", "214.096,09 ÷ 12 × 3", m2(c.GIRO_A)],
    ["Conta B do Pilar 6", "22.356,81 + 3 × 9.385,60 = 22.356,81 + 28.156,80", m2(c.GIRO_B)],
    ["!Giro da 6B (a maior)", "", m2(c.GIRO6B)],
    ["!Investimento total refeito", "791.131 + 53.524,02", m2(c.INVEST6B)]], v=(2,), larg=("30%", "48%", "22%"))
    + f"<p>Na 6A, o investimento total era {brl(c.INVEST6A, 2)}. A diferença, {brl(c.INVEST6B - c.INVEST6A, 2)}, vem só do giro.</p>"))
add("<h3>O colchão</h3>"
    "<p>O colchão é o que ainda resta no banco no pior mês dos três primeiros anos. Começa com o giro (a reserva do imprevisto está dentro do CAPEX e é dada como toda usada) e desce até o menor saldo acumulado. A régua da Zion pede um colchão de pelo menos <b>10% do CAPEX</b> (faixa citada pela fonte; Volume 05 · Investimento, cap. 8).</p>")
add(ex("O colchão da Marina", f"<p>53.524,02 − 22.356,81 = <b>{brl(c.COLCHAO, 2)}</b>; ÷ 791.131 = <b>{pct(c.COLCHAO_PCT)}</b> do CAPEX. Abaixo de 10%. O giro que daria 10%: 79.113,10 + 22.356,81 = <b>{brl(c.GIRO_10, 2)}</b>.</p>"
       f"<p><b>O fôlego no dia da abertura:</b> 53.524,02 ÷ 9.385,60 = {dec(c.FOLEGO, 1)} meses de fixo. As fontes leem abaixo de 2 meses como zona de risco e de 4 a 6 como confortável. O fôlego é bom; o colchão é fino, porque o primeiro ano come uma parte do giro.</p>"))
add(pare("O ano em regime da Marina fecha positivo. Por que ela ainda precisa olhar o mês?", ["Não precisa", "Porque o caixa pode acabar num mês fraco do primeiro ano, mesmo com o ano positivo", "Porque o contador pede"],
         "B. Com a rampa e cinco meses fracos, o acumulado do primeiro ano desce até −22.356,81 em março. É o mês que decide o giro."))
add(aplic("escreva o seu mês de abertura e marque, no seu calendário, os meses fracos que caem dentro do primeiro ano. Se puder escolher, abra no começo da alta.",
          "pegue o saldo do caixa mês a mês dos últimos doze meses: o menor saldo é o seu ponto de partida para o colchão da ampliação."))
add(levar(["O ano mês a mês: rampa × calendário, a partir do mês de abertura.", "O menor saldo decide o giro.", "A alta paga o vale por decisão: a reserva de sazonalidade.", "Giro = a maior de duas contas do Pilar 6.", "Colchão de pelo menos 10% do CAPEX no pior mês."]))
fim()

# ---------------------------------------------------------------- 08
esc = [(-c.CAPEX, -c.CAPEX)]
acum = -c.CAPEX + c.ANO1S["cons"]; esc.append((c.ANO1S["cons"], acum))
for t in range(2, 17):
    acum += c.SOBRA; esc.append((c.SOBRA, acum))
cap("08", "O retorno", "Vale a pena? <i>Lucro e retorno são coisas diferentes</i>",
    "A operação se paga. Agora a outra pergunta: em quanto tempo o que sobra devolve o investimento, e quanto vale o dinheiro que espera.",
    ["Pode sobrar dinheiro todo ano e o investimento nunca voltar dentro de um prazo razoável.",
     "Com o retorno simples, o tempo de volta em escada, a conta do Pilar 6 ao lado, o valor presente com a sua taxa e o terreno à parte.",
     "Para você decidir com o retorno, e não só com o lucro."],
    ["O retorno simples", "O tempo de volta em escada", "Como o Pilar 6 calcula", "O valor presente dos próximos dez anos", "O terreno e a venda do negócio ao lado"],
    "O capítulo 06 mostrou que a operação da Marina se paga com folga. Isso é lucro. Retorno é outra coisa: é o que sobra comparado ao que foi investido, e o tempo que leva para voltar.")
add(cita("Lucro e retorno são coisas diferentes.", "Pilar 6 · Pré-viabilidade, cap. 07"))
add("<h3>O retorno simples</h3><p>O retorno simples é o que sobra num ano em regime dividido pelo CAPEX. Sempre sobre o que sobra, depois da reserva de reposição; nunca sobre o resultado antes da reserva.</p>")
add(ex("O retorno simples da Marina", f"<p>57.819,79 ÷ 791.131 = <b>{pct(c.RET)} ao ano</b>. Com o terreno somado: 57.819,79 ÷ 1.391.131 = {pct(c.RET_T)}.</p>"))
add("<h3>O tempo de volta em escada</h3>"
    "<p>Na escada, o CAPEX sai no ano zero. O primeiro ano entra com a rampa. Do segundo em diante, entra o que sobra num ano em regime. O tempo de volta é o momento em que o acumulado passa de negativo a zero. O giro não entra no ano zero: ele é testado à parte, no colchão (capítulo 07). O terreno também não: ele fica ao lado.</p>")
add(ex("A escada da Marina (conservador)", tab(["Ano", "Fluxo do ano", "Acumulado"], [[str(t), m2(f), m2(a)] for t, (f, a) in enumerate(esc) if t in (0, 1, 2, 10, 15, 16)], v=(1, 2), larg=("20%", "40%", "40%"))
       + f"<p>Depois do ano 1, faltam 810.123,04. 810.123,04 ÷ 57.819,79 = 14,01 anos de regime. <b>Tempo de volta: {dec(c.VOLTA['cons'], 1)} anos.</b></p>"
       '<p class="conf">Conferência: no fim do ano 15, −810.123,04 + 14 × 57.819,79 = −646,00; no ano 16 vira; 15 + 646,00 ÷ 57.819,79 = 15,01. Bate.</p>'))
add("<h3>Como o Pilar 6 calcula, ao lado</h3>"
    f"<p>O Pilar 6 divide o investimento total (com o giro) pelo resultado do conservador, sem rampa. Com a conta aberta da Marina: 844.655,02 ÷ 57.819,79 = <b>{dec(c.VOLTA_P6['cons'], 1)} anos</b>. As duas contas seguem regras diferentes e dão números próximos, não iguais. Não misture: compare cada uma com a régua dela. Na Marina, as duas passam de 12 anos.</p>")
add(tab(["Tempo de volta (escada)", "Leitura da régua da Zion", "Como o Pilar 6 lê"], [
    ["até 8 anos", "passa", "até 5, muito bom e raro em construção do zero; 5 a 8, bom"],
    ["de 8 a 12 anos", "ajustar", "aceitável quando há valorização relevante"],
    ["acima de 12, ou «não se paga»", "redesenhar", "só com uma razão escrita"]], larg=("26%", "26%", "48%"), leg="Faixas citadas pela fonte; não são meta nem promessa"))
add("<h3>O valor presente dos próximos dez anos</h3>"
    "<p>Um real daqui a dez anos vale menos do que um real hoje, porque o seu dinheiro poderia render em outro lugar. O valor presente traz os dez anos de fluxo para hoje, com uma taxa, e desconta o CAPEX. Positivo: o projeto rende mais do que a sua taxa. Negativo: rende menos.</p>"
    "<p>A taxa é sua, e se escreve <b>antes</b> de ver o resultado. A Zion não sugere taxa. A sua taxa é o quanto o seu dinheiro renderia em outro lugar, mais o que você pede pelo risco. Mudar a taxa depois de ver o resultado é escolher a resposta.</p>")
add(ex("O valor presente da Marina", f"<p>A soma simples dos dez anos, sem desconto nenhum: −18.992,04 + 9 × 57.819,79 = <b>{brl(c.SOMA10, 2)}</b>, menor que o CAPEX de 791.131. Se nem a soma sem desconto paga o CAPEX, o valor presente é <b>negativo a qualquer taxa de zero para cima</b>. A Marina não precisou escolher taxa.</p>"
       f"<p><b>Com a venda do negócio no ano 10, ao lado:</b> pela referência da régua, 6 vezes o resultado antes da reserva (6 × 65.977,26 = {brl(c.SAIDA, 2)}). A soma simples sobe para {brl(c.SOMA10 + c.SAIDA, 2)}, e o valor presente fica negativo a partir de cerca de <b>{dec(c.TAXA_ZERO * 100, 1)}% ao ano</b> (a 1%: +38.816,74; a 2%: −22.319,65). Com qualquer taxa razoável para o dinheiro dela, o resultado é o mesmo.</p>"
       '<p class="nota">O múltiplo de 6 vezes é a referência da régua da Zion, sem origem estatística nas fontes. Ele aparece só ao lado da conta sem ele, nunca como valor do negócio.</p>'))
add("<p>A venda do negócio fica sempre ao lado da conta sem ela. Se só a venda salva a conta, a decisão é ajustar, nunca avançar: o projeto passa a depender de alguém comprar.</p>")
add(cita("Nenhuma das três decide sozinha.", "Volume A05 · Investimento, cap. 11, sobre o tempo de volta, o valor presente e a taxa interna de retorno"))
add("<h3>O terreno, ao lado e visível</h3>"
    f"<p>O terreno fica fora do tempo de volta, mas não some: refaça a escada com ele no ano zero e escreva a razão de seguir, se seguir. Na Marina: (791.131 + 600.000 + 18.992,04) ÷ 57.819,79 = 24,39 → <b>{dec(c.VOLTA_T, 1)} anos</b>. A razão que ela escreveu no Dossiê (patrimônio, família, projeto de vida) precisa ser revista com esse número.</p>")
add(bx("Os nomes que você vai ver na Planilha 2", "Cada sigla, uma vez, explicada",
       "<ul><li><b>EBITDA</b> e <b>NOI</b>: nomes técnicos do resultado da operação. Neste e-book, o «resultado antes da reserva» (degrau 4). A Planilha 2 chama de NOI a linha do resultado; com a reserva lançada por noite (capítulo 13), essa linha passa a ser o que sobra.</li>"
       "<li><b>Payback</b>: o tempo de volta. A Planilha 2 calcula pela conta simples, sem rampa, como o Pilar 6.</li>"
       "<li><b>VPL</b>: o valor presente líquido, o nosso valor presente dos dez anos.</li>"
       "<li><b>TIR</b>: a taxa interna de retorno, a taxa em que o valor presente dá zero.</li>"
       "<li><b>ROI</b>: o retorno sobre o investimento, o nosso retorno simples.</li></ul>"
       "<p class=\"nota\">Moeda constante: a 6B trabalha em reais de hoje, sem crescimento de receita nem de custo. A Planilha 2 cresce a receita e usa taxa nominal. Os dois caminhos se defendem; não misture um com o outro.</p>"))
add(pare("A operação da Marina se paga com 13 pontos de folga. Isso quer dizer que o investimento volta em 8 anos?", ["Sim, se a operação se paga, o investimento volta", "Não: lucro e retorno são coisas diferentes; com o que sobra, o CAPEX volta em cerca de 15 anos", "Depende do contador"],
         "B. A folga diz que a operação não dá prejuízo. O tempo de volta diz quanto o que sobra demora para devolver os R$ 791.131."))
add(aplic("escreva a sua taxa (quanto o seu dinheiro renderia em outro lugar, mais o que você pede pelo risco) antes de abrir a ficha. Depois o valor do seu terreno, para a conta ao lado.",
          "na ampliação, o CAPEX é o da ampliação e o fluxo é só o que ela acrescenta. A operação existente não paga a obra."))
add(levar(["Lucro e retorno são coisas diferentes.", "Retorno sobre o que sobra, nunca sobre o resultado antes da reserva.", "Escada: CAPEX no ano zero, primeiro ano com rampa; a conta do Pilar 6 ao lado.", "A taxa é sua, escrita antes; a Zion não sugere taxa.", "Venda do negócio e terreno sempre ao lado."]))
fim()

# ---------------------------------------------------------------- 09
cap("09", "O estresse", "Onde a conta <i>quebra</i>",
    "Os três cenários do curso com o custo aberto, o teste de queda, a sensibilidade do Mapa e o que precisa ser verdade.",
    ["Uma conta que só funciona num cenário não é uma conta: é uma esperança.",
     "Movendo uma premissa por vez e vendo o que acontece com o que sobra e com o tempo de volta.",
     "Para você saber qual premissa decide o seu projeto, e o que precisaria ser provado."],
    ["Os três cenários com o custo aberto", "O teste de queda", "A sensibilidade do Mapa", "A hierarquia da dor", "O que precisa ser verdade"],
    "No Pilar 4, você montou três cenários de receita. No Pilar 6, a margem era a mesma nos três. Com o custo aberto, o fixo não muda de um cenário para outro, e a margem sobe com a ocupação.")
add(cita("O número em que você confia é o do cenário mais fraco.", "Pilar 4 · Modelo de negócio"))
add(ex("Os três cenários da Marina, com o custo aberto", tab(["", "Conservador 38,5%", "Base 50%", "Otimista 65%"], [
    ["O que sobra", m2(CO["sobra"]), m2(BA["sobra"]), m2(OT["sobra"])],
    ["Margem", pct(CO["margem"]), pct(BA["margem"]), pct(OT["margem"])],
    ["!Tempo de volta (escada)", anos(c.VOLTA["cons"]), anos(c.VOLTA["base"]), anos(c.VOLTA["otim"])],
    ["Como o Pilar 6 calcula", anos(c.VOLTA_P6["cons"]), anos(c.VOLTA_P6["base"]), anos(c.VOLTA_P6["otim"])]], v=(1, 2, 3), larg=("31%", "23%", "23%", "23%"))
    + f"<p>O conservador é o cenário medido, o que precisa funcionar; o otimista é teto, não meta. A régua da Zion lê o conservador. {CEN}</p>"))
add(cita("Se o conservador não paga as contas, o empreendimento ainda não está pronto.", "Pilar 6 · Pré-viabilidade, cap. 07, a partir do Panorama do Desenvolvimento Hoteleiro"))
add("<h3>O teste de queda</h3><p>A régua da Zion derruba a diária em 10% e a ocupação em 20% ao mesmo tempo, sobre o cenário medido, e pergunta: o ano ainda fecha? Fechou, passa. Déficit de até três meses de fixo, ajustar. Maior, redesenhar.</p>")
add(ex("O teste de queda da Marina", f"<p>Diária 645 × 0,90 = R$ 580,50; ocupação 38,5% × 0,80 = 30,8%, ou 337,26 noites. Cada noite deixa 580,50 × 0,778 − 97,50 = 354,13. 337,26 × 354,13 = 119.433,55; − 112.627,20 = <b>{brl(c.QUEDA['sobra'], 2)}</b>. Passa.</p>"))
add("<h3>A sensibilidade do Mapa</h3><p>O Mapa de direcionamento pede, no Pilar 6, três testes: diária −15%, ocupação −10 pontos e CAPEX +20%. A 6B faz os três sobre a conta aberta, um de cada vez.</p>")
add(ex("A sensibilidade da Marina (escada, conservador)", tab(["Teste", "O que sobra no ano", "Tempo de volta"], [
    ["Nenhum (a conta dela)", m2(c.SOBRA), anos(c.VOLTA["cons"])],
    ["Diária −15% (R$ 548,25)", m2(c.SENS_D["sobra"]), anos(c.SENS["diaria"])],
    ["Ocupação −10 pontos (28,5%)", m2(c.SENS_O["sobra"]), anos(c.SENS["ocup"])],
    ["CAPEX +20% (R$ 949.357,20)", m2(c.SOBRA), anos(c.SENS["capex"])]], v=(1, 2), larg=("44%", "28%", "28%"))))
add("<h3>A hierarquia da dor</h3><p>As fontes ordenam o que mais pesa: <b>diária, ocupação, custo fixo, investimento</b> (Volume A05 · Investimento, cap. 12). Com o custo aberto, dá para ver por quê: cada real de diária a mais fica quase inteiro (77,8 centavos na Marina), porque só as deduções e a reserva crescem com ele. A melhor proteção é o posicionamento, que sustenta a diária.</p>")
add("<h3>O que precisa ser verdade</h3><p>A conta inversa pergunta: para o tempo de volta caber na régua, quanto precisaria ser cada premissa, mexendo uma só? Calcule para 8 anos (passa) e para 12 (sai do redesenhar).</p>")
add(ex("O que precisa ser verdade para a Marina", tab(["Premissa (uma por vez)", "Hoje", "Para 12 anos", "Para 8 anos"], [
    ["Ocupação (com R$ 645)", "38,5%", pct(c.PV12["ocup"]), pct(c.PV8["ocup"])],
    ["Diária (com 38,5%)", "R$ 645", brl(c.PV12["diaria"], 2), brl(c.PV8["diaria"], 2)],
    ["CAPEX, até", brl(c.CAPEX), brl(c.PV12["capex"], 2), brl(c.PV8["capex"], 2)]], v=(1, 2, 3), larg=("34%", "18%", "24%", "24%"))
    + '<p class="conf">Conferência (8 anos): (791.131 + 8 × 112.627,20) ÷ (7 + 0,549351) = 1.692.148,60 ÷ 7,549351 = 224.144,92; ÷ 404,31 = 554,39 noites = 50,6%; 224.144,92 ÷ 421,575 = 531,68 por noite; (531,68 + 97,50) ÷ 0,778 = 808,72; CAPEX: 7 × 57.819,79 − 18.992,04 = 385.746,48. Bate.</p>'))
add("<h3>O limite da página 6 também era premissa</h3>"
    f"<p>O «até cerca de R$ 870 mil» da página 6 foi calculado com a margem de 40%: 8 × 108.766,35. Com a margem aberta, a mesma conta do Pilar 6 dá 8 × 57.819,79 = <b>{brl(c.LIMITE6B, 2)}</b>. O investimento total refeito, {brl(c.INVEST6B, 2)}, passa desse limite.</p>")
add(pare("Qual alavanca pesa mais na conta da Marina?", ["O CAPEX", "A diária", "O custo fixo"],
         "B. Cada real de diária fica quase inteiro. É o primeiro degrau da hierarquia da dor."))
add(aplic("escolha a premissa de que você menos tem certeza e calcule o que precisaria ser verdade só com ela. É a primeira coisa a provar.",
          "use o pior ano do seu extrato como teste de queda real: a conta da ampliação fecha com ele?"))
add(levar(["Três cenários com o mesmo fixo: a margem muda.", "Teste de queda: diária −10% e ocupação −20% juntas.", "Sensibilidade do Mapa: diária −15%, ocupação −10 pontos, CAPEX +20%.", "Diária, ocupação, custo fixo, investimento.", "O que precisa ser verdade, uma premissa por vez."]))
fim()

# ---------------------------------------------------------------- 10
cap("10", "Exemplo resolvido", "A conta da Marina, <i>inteira</i>",
    "Os seis degraus nos três cenários, o equilíbrio, o primeiro ano, o giro, a escada, os cinco passos e o veredito. Com as conferências.",
    ["Ver a conta inteira montada ensina mais do que qualquer regra solta.",
     "Juntando o que os capítulos 03 a 09 abriram e passando pela régua da Zion em cinco passos.",
     "Para você ter um modelo para a sua página 6B."],
    ["As premissas", "A conta em seis degraus", "De onde vem a diferença com a página 6", "Os cinco passos", "O veredito e a ação"],
    "A Marina tem as páginas 2, 4, 6 e 6A na mão, a resposta do contador dela e a lista de custos. Hoje, no exemplo, é 28 de novembro de 2026.")
add(ex("As premissas", "<ul><li>Situação: «Tenho um terreno e ainda não hospedo ninguém»; 3 cabanas; opera com uma pessoa local; primeira obra.</li>"
       f"<li>Da 6A: CAPEX {brl(c.CAPEX)}; giro {brl(c.GIRO6A, 2)}; terreno {brl(c.TERRENO)}, ao lado. Da página 6: margem de referência de 40%, limite {brl(c.LIMITE6, 2)}.</li>"
       "<li>Diária R$ 645; ocupação 38,5% / 50% / 65%; calendário com alta de junho a agosto; abertura em junho; estadia média de 2 noites.</li>"
       "<li>Imposto de 6%, resposta fictícia do contador dela em 20/11/2026; deduções de 18,2%; R$ 97,50 por noite e 1% de perdas; fixo de R$ 9.385,60 por mês com a retirada; reserva de reposição de 3%; sem custos do modelo.</li></ul>"))
T = c.TAB73
lin = lambda nome, k, cls="": [cls + nome, m2(CO[k]), m2(BA[k]), m2(OT[k])]
add(ex("A conta em seis degraus, nos três cenários", tab(["Degrau", "Conservador 38,5%", "Base 50%", "Otimista 65%"], [
    ["Noites vendidas", dec(CO["noites"], 3), dec(BA["noites"], 1), dec(OT["noites"], 2)],
    ["Estadias", dec(CO["estadias"], 2), dec(BA["estadias"], 2), dec(OT["estadias"], 2)],
    lin("1 · Receita bruta (só hospedagem)", "bruta", "!"), lin("Imposto 6%", "imp"), lin("Comissão 9%", "com"), lin("Cartão 1,2%", "cart"),
    lin("Cancelamento 2%", "canc"), lin("Deduções (18,2%)", "ded", "~"), lin("2 · Receita real", "real", "!"),
    lin("Lavanderia (R$ 70 × estadias)", "lav"), lin("Amenidades (R$ 45 × estadias)", "amen"), lin("Energia, água e gás (R$ 28 × noites)", "ener"),
    lin("Limpeza e reposição (R$ 12 × noites)", "limp"), lin("Perdas e quebras (1%)", "perdas"), lin("Custos de cada noite", "var", "~"),
    lin("3 · Margem de contribuição", "contrib", "!"), lin("Fixos com a retirada", "fixo"), lin("4 · Resultado antes da reserva", "antes", "!"),
    ["5 · Custos do modelo", "0", "0", "0"], lin("Reserva de reposição (3%)", "reserva"), lin("6 · O que sobra", "sobra", "!"),
    ["!Margem (o que sobra ÷ receita bruta)", pct(CO["margem"]) + " (atenção)", pct(BA["margem"]), pct(OT["margem"])],
    ["Por mês, em média", m2(CO["sobra"] / 12), m2(BA["sobra"] / 12), m2(OT["sobra"] / 12)]], v=(1, 2, 3), larg=("37%", "21%", "21%", "21%"))
    + '<p class="conf">Conferência pelo caminho da noite: 421,575 × 404,31 = 170.446,99; − 112.627,20 = 57.819,79. Base: 547,5 × 404,31 = 221.359,73; − 112.627,20 = 108.732,53. Otimista: 711,75 × 404,31 = 287.767,64; − 112.627,20 = 175.140,44. Bate.</p>'
    '<p class="nota">O resultado antes da reserva é o «resultado operacional» do e-book «Receitas, Custos e Modelos de Rentabilidade». As contas foram feitas sem arredondar; diferenças de R$ 0,01 vêm do arredondamento dos centavos.</p>'))
add("<h3>De onde vem a diferença com a página 6</h3>")
add(ex("Página 6 × página 6B, sem adjetivo", f"<p>Na página 6, 271.915,88 × 40% = {brl(CO['bruta'] * c.MARGEM6, 2)}. Com a lista dela, sobram {brl(c.SOBRA, 2)} ({pct(CO['margem'])}). Os 18,7 pontos de diferença estão nas linhas que a margem de referência resumia:</p>"
       + tab(["Linha da 6B", "R$ no ano", "% da receita bruta"], [
           ["Deduções", m2(CO["ded"]), pct(CO["ded"] / CO["bruta"])], ["Custos de cada noite", m2(CO["var"]), pct(CO["var"] / CO["bruta"])],
           ["Fixos com o trabalho dela", m2(CO["fixo"]), pct(CO["fixo"] / CO["bruta"])], ["Reserva de reposição", m2(CO["reserva"]), pct(CO["reserva"] / CO["bruta"])],
           ["!Tudo o que sai", m2(c.CUSTOS), "78,7%"], ["!O que sobra", m2(c.SOBRA), "21,3%"]], v=(1, 2), larg=("50%", "25%", "25%"))
       + '<p class="conf">Conferência: 49.488,69 + 43.822,72 + 112.627,20 + 8.157,48 = 214.096,09; 271.915,88 − 214.096,09 = 57.819,79. Bate.</p>'
       "<p>O que mais pesa é o fixo com o trabalho dela: três cabanas dividem o mesmo salário, o mesmo contador e a mesma manutenção que cinco dividiriam. A página 6 deu a ordem de grandeza; a conta aberta mostra onde o dinheiro sai.</p>"))
add("<h3>Os cinco passos da régua da Zion</h3>")
add(passos_html(c.PASSOS, [f"Sobram {brl(c.SOBRA)} no ano", f"Com a queda, {brl(c.QUEDA['sobra'])}", f"{anos(c.VOLTA['cons'])}, acima de 12", "Negativo sem a venda, a qualquer taxa; com ela, acima de cerca de 1,6%", f"{pct(c.COLCHAO_PCT)} do CAPEX, abaixo de 10%"]))
add(f'<div class="veredito"><div><span class="k">Veredito sugerido</span><br><b>{c.VEREDITO}</b></div><p>Algum passo em «redesenhar» leva o veredito para Redesenhar. Na página 6 isso se chamava «ajustar» acima de 12 anos: as duas dizem «não assine a obra neste desenho». {CEN}</p></div>')
add(cita("Quando a conta não fecha, a conta está certa", "Jornada do COMO, Etapa 02, citada nos e-books «Receitas, Custos e Modelos de Rentabilidade» e «Viabilidade e Análise de Investimentos»"))
add("<p>O critério que a Marina escreveu na página 6 dispara: «se a lista de custos mostrar uma margem que leve o conservador acima de 8 anos, eu não assino a obra». A operação se paga com folga, mas o investimento não volta em 12 anos. Ela descobriu isso no papel, antes de assinar.</p>")
add(bx("O que a Marina escreve na página 6B", "",
       "<p><b>Veredito dela:</b> Redesenhar. <b>Critério para parar:</b> «Se nenhum redesenho passar de 12 para 8 anos com premissas provadas, eu não assino a obra.»</p>"
       "<p><b>Ação de 30 dias:</b> rodar a 6B com três redesenhos, uma alavanca por vez, e não assinar contrato de obra. <b>Prazo:</b> 28/12/2026. <b>Como verificar:</b> as três versões da 6B salvas, com data.</p>"
       "<p><b>Os alertas da ficha, na ordem:</b> o giro da 6A não cobre a conta aberta; o colchão está abaixo de 10% do CAPEX; o limite da página 6, com a margem aberta, passa a cerca de R$ 463 mil. E mais um: com o terreno, 25,4 anos, e a razão escrita no Dossiê precisa ser revista. O imposto não dispara alerta: o contador dela respondeu.</p>", "faca"))
fim()

# ---------------------------------------------------------------- 11
A = c.ALAV
NOMES_AL = [("nenhuma", "Nenhuma (a conta dela)", "—"), ("diaria50", "Diária + R$ 50", "R$ 695"),
            ("diariaP3", "Diária da hipótese do Pilar 3", "cerca de R$ 716, a provar"), ("ocup5", "Ocupação + 5 pontos", "43,5%"),
            ("fixo10", "Custo fixo − 10%", "R$ 8.447,04 por mês"), ("capex10", "CAPEX − 10%", "R$ 712.017,90"),
            ("cesta", "Outras receitas: cesta de café", "60% das estadias × R$ 140, custo R$ 70"),
            ("fase2", "Fase menor: 2 cabanas", "CAPEX R$ 622.150; fixos iguais")]
cap("11", "O redesenho", "Quando a conta não fecha: <i>uma alavanca por vez</i>",
    "Diária, ocupação, custo fixo, CAPEX, fase, outras receitas. Cada uma sozinha, para saber o que cada uma faz. Depois, o cenário ajustado.",
    ["Mexer em tudo ao mesmo tempo esconde qual premissa salvou a conta, e qual precisa ser provada.",
     "Movendo uma alavanca de cada vez sobre a conta da Marina, lendo o passo 3, e juntando três num cenário ajustado.",
     "Para você saber o que precisaria ser verdade e o que provar antes de decidir de novo."],
    ["As alavancas, uma por vez", "O que cada uma ensina", "O cenário ajustado", "Por que ele dá «Testar»", "Os 90 dias do Pilar 7"],
    "Redesenhar não é desistir. É voltar à conta com uma pergunta precisa: o que precisaria mudar, e isso é possível de provar? A regra é mexer uma alavanca por vez.")
add(ex("As alavancas da Marina, uma por vez", tab(["Alavanca", "O que muda", "O que sobra no ano", "Ano 1", "Tempo de volta", "Passo 3"],
    [[n, mu if mu != "—" else "", m2(A[k]["sobra"]), m2(A[k]["ano1"]), anos(A[k]["volta"]), c.passo3(A[k]["volta"])] for k, n, mu in NOMES_AL],
    v=(2, 3, 4), larg=("22%", "24%", "15%", "14%", "13%", "12%"))
    + '<p class="conf">Conferências: diária R$ 695: 421,575 × 443,21 = 186.846,26; − 112.627,20 = 74.219,06; 1 + (791.131 + 9.983,09) ÷ 74.219,06 = 11,79. Ocupação 43,5%: 476,325 × 404,31 = 192.582,96; − 112.627,20 = 79.955,76. Fixo −10%: 170.446,99 − 101.364,48 = 69.082,51. Cesta: 126,47 cestas × 57,40 = 7.259,52. Duas cabanas: 281,05 noites × 404,31 = 113.631,33; − 112.627,20 = 1.004,13; CAPEX (687.940 − 146.940) × 1,15 = 622.150, com as linhas de uma cabana da 6A. Bate.</p>'))
add("<h3>O que cada alavanca ensina</h3><ul>"
    "<li><b>A diária pesa mais.</b> Cada real fica quase inteiro (77,8 centavos). R$ 50 a mais tiram a Marina do redesenhar. É o primeiro degrau da hierarquia da dor, e o que o posicionamento do Pilar 3 protege.</li>"
    "<li><b>A ocupação vem logo atrás.</b> Cinco pontos a mais fazem quase o mesmo que R$ 50 de diária.</li>"
    "<li><b>Custo e CAPEX ajudam pouco sozinhos.</b> Cortar 10% do fixo ou do CAPEX não tira a conta do redesenhar.</li>"
    "<li><b>As outras receitas não sustentam a conta.</b> A cesta ajuda, mas a conta precisa fechar com as diárias.</li>"
    "<li><b>A fase menor piora.</b> Com duas cabanas, o fixo não cai junto: a pessoa local, o contador e a manutenção continuam. A conta quase zera.</li></ul>")
add(cita("Primeiro prove a conta. Depois escolha como crescer.", "Pilar 6 · Pré-viabilidade, cap. 08"))
add("<p>O Pilar 6 já ensinava: fase um paga fase dois. Antecipar as cinco cabanas de uma vez diluiria o fixo, mas pede prova de mercado e mais capital, e o Pilar 2 da Marina pôs o limite de mercado em cinco. Fica fora das alavancas desta conta.</p>")
add("<h3>O cenário ajustado</h3><p>Três alavancas que o curso já anunciou, todas <b>a provar</b>: a diária de cerca de R$ 716 (a hipótese do produto, do Pilar 3, que a ficha do Pilar 6 pede para deixar «como folga, não como condição»); 42% de ocupação com um pacote de domingo a quinta para quem trabalha (a semana está em 26% no Pilar 2, e a internet para esse hóspede já está na lista da 6A); a cesta de café. CAPEX e custos fixos iguais.</p>")
AJ = c.AJ
add(ex("O cenário ajustado da Marina · o que precisaria ser verdade", tab(["Linha", "Valor"], [
    ["Noites (1.095 × 42%) / estadias", f"{dec(AJ['noites'], 1)} / {dec(AJ['estadias'], 2)}"],
    ["Receita de hospedagem (459,9 × 716)", m2(AJ["hosp"])], ["Cestas (137,97 × 140)", m2(AJ["rcestas"])], ["!Receita bruta", m2(AJ["bruta"])],
    ["Deduções da hospedagem (18,2%)", m2(AJ["ded"])], ["Imposto das cestas (6%)", m2(AJ["imp_cestas"])],
    ["Custos de cada noite (estadias × 115 + noites × 40 + 1% da hospedagem)", m2(AJ["var"])], ["Custo das cestas (137,97 × 70)", m2(AJ["custo_cestas"])],
    ["Fixos com a retirada", m2(AJ["fixo"])], ["Resultado antes da reserva", m2(AJ["antes"])], ["Reserva de reposição (3% de 348.604,20)", m2(AJ["reserva"])],
    ["!O que sobra", f"{m2(AJ['sobra'])} (margem {pct(AJ['margem'])})"], ["Ano 1 com a rampa", "+" + m2(c.AJ_ANO1)],
    ["Menor saldo do primeiro ano (março)", m2(c.AJ_MENOR)], ["Tempo de volta em escada", f"1 + (791.131 − 7.826,50) ÷ 106.638,40 = {anos(c.AJ_VOLTA)}"],
    ["Giro (conta A: 241.965,80 ÷ 4) / colchão", f"{m2(c.AJ_GIRO)} / {m2(c.AJ_COLCHAO)} = {pct(c.AJ_COLCHAO_PCT)} do CAPEX"],
    ["Teste de queda (R$ 644,40; 33,6%)", "+" + m2(c.AJ_Q["sobra"])]], v=(1,), larg=("60%", "40%"))
    + '<p class="conf">Conferência pela cascata: 348.604,20 − 59.930,49 − 1.158,95 − 3.292,88 − 26.444,25 − 18.396,00 − 9.657,90 − 10.458,13 − 112.627,20 = 106.638,40. Bate.</p>', k=FICT + " Cenário ajustado: premissas a provar."))
add(tab(["Taxa que a pessoa escreve", "Valor presente sem a venda", "Com a venda (6 × 117.096,53)"],
        [[f"{int(t * 100)}% ao ano", m2(a), ("+" if b > 0 else "") + m2(b)] for t, (a, b) in c.AJ_VP.items()], v=(1, 2), larg=("34%", "33%", "33%"),
        leg="O valor presente do ajustado em três taxas, só para mostrar que a taxa muda a decisão. A ficha calcula com a taxa que você escreveu antes."))
add(passos_html(["passa", "passa", "ajustar", "ajustar", "ajustar"], ["Sobra positiva", "Com a queda, +42 mil", f"{anos(c.AJ_VOLTA)}", f"Positivo só com a venda, até cerca de {dec(c.AJ_TAXA_SAIDA * 100, 1)}% ao ano", f"{pct(c.AJ_COLCHAO_PCT)}; com giro de {brl(c.AJ_GIRO10, 2)} passaria"]))
add('<div class="veredito"><div><span class="k">A régua diz</span><br><b>Ajustar</b></div><p>A ficha mostra <b>«Testar»</b>: a conta chega a Ajustar só com premissas que ainda não foram provadas (diária acima de 1,05 × 645 = R$ 677,25 e ocupação acima da medida no Pilar 2).</p></div>')
add("<h3>Os 90 dias do Pilar 7</h3><p>O cenário ajustado não é a conta da Marina: é o que precisaria ser verdade. Os 90 dias do Pilar 7 servem para provar preço e semana antes de decidir de novo: um teste de preço para a diária de cerca de R$ 716 e o pacote de domingo a quinta. O plano do Pilar 7 já tem o passo: «Dias 61 a 90 · Decidir: refaz a página 6 com os números cotados».</p>")
add(pare("A Marina testa a diária +50 e, ao mesmo tempo, corta 10% do fixo. A conta passa para «ajustar». O que ela aprendeu?", ["Que as duas juntas resolvem", "Pouco: não sabe qual das duas fez o efeito, nem qual precisa provar", "Que o fixo é a alavanca principal"],
         "B. Uma alavanca por vez. Só depois, a combinação, com o rótulo «o que precisaria ser verdade»."))
add(faca("Os meus três redesenhos", [("Redesenho 1 · a alavanca, o novo valor e como vou provar:", False), ("Redesenho 2:", False), ("Redesenho 3:", False)]))
add(levar(["Uma alavanca por vez.", "A diária pesa mais; custo e CAPEX ajudam pouco sozinhos.", "As outras receitas não sustentam a conta.", "Fase menor com o mesmo fixo piora.", "O ajustado é «o que precisaria ser verdade»: com premissa não provada, Testar."]))
fim()

# ---------------------------------------------------------------- 12
cap("12", "Exercícios", "Pratique <i>com a Marina</i>",
    "Do resolvido ao em branco: as deduções refeitas, a classificação de cada saída, uma alavanca na escada e a sua lista.",
    ["Fazer a conta com a mão é o que fixa o método.",
     "Com quatro exercícios sobre os números da Marina e o gabarito comentado no fim.",
     "Para você chegar à ficha sabendo onde cada linha mora."],
    ["E1 · A conta da Marina (resolvido)", "E2 · As deduções", "E3 · Em qual degrau?", "E4 · Uma alavanca e a escada", "E5 · A sua lista", "Gabarito comentado"],
    "O exercício 1 você já viu: a conta inteira da Marina, no capítulo 10. Agora é a sua vez, com os mesmos números, rotulados como exemplo ilustrativo.")
add(ex("E2 · A Marina passa a vender 80% das noites pela plataforma", "<p>A plataforma continua cobrando 15% por reserva. O resto fica igual. Calcule: a comissão sobre a receita total; o cartão; as deduções; o que fica de cada noite; o que sobra no ano; a margem e a faixa da régua; o ponto de equilíbrio e a folga.</p>"
       f"<p>Já resolvido para você: a comissão sobre a receita total passa a 0,80 × 15% = <b>12%</b>; o cartão, 0,20 × 3% = <b>0,6%</b>; as deduções, 6% + 12% + 0,6% + 2% = <b>20,6%</b>. O resto é com você.</p><div class=\"campo alto\"></div>"))
add(bx("E3 · Em qual degrau?", "", "<p>Para cada item, escreva o degrau (2 a 6), «nunca as duas» ou «fora desta conta»:</p>"
       "<p>comissão da plataforma · imposto sobre a receita · cancelamento · lavanderia por estadia · perdas e quebras de material · salário da pessoa local · 13º e férias · seguro anual · as horas da Marina · taxa de uma administradora · troca dos colchões daqui a seis anos · depreciação somada à reserva · parcela do empréstimo da obra · taxa de limpeza cobrada à parte do hóspede</p><div class=\"campo alto\"></div>", "faca"))
add(ex("E4 · Uma alavanca e a escada", "<p>Com a diária de R$ 695 (R$ 50 a mais), calcule: o que fica de cada noite; o que sobra no ano; o primeiro ano com a rampa; o tempo de volta em escada e o passo 3; quanto valem os R$ 50 por ano, com o custo aberto e com a margem de referência da página 6. Por que a diferença?</p><div class=\"campo alto\"></div>"))
add(faca("E5 · A sua lista, em branco", [("Os meus custos fixos, até 15 linhas, com os anuais divididos por 12 e as minhas horas na operação:", True), ("A minha pergunta ao contador, com a data em que vou fazer:", False)],
         nota="É a ponte para a ficha: estas linhas entram nas telas «O custo de cada mês» e «Do bruto ao real»."))
add("<h3>Gabarito comentado</h3>")
add(tab(["E2", "Conta", "Resposta"], [
    ["Comissão sobre o total", "0,80 × 15%", "12%"], ["Cartão", "0,20 × 3%", "0,6%"], ["Deduções", "6% + 12% + 0,6% + 2%", "20,6%"],
    ["O que fica de cada noite", "645 × (1 − 0,206 − 0,01 − 0,03) − 97,50 = 486,33 − 97,50", brl(c.E2_NOITE, 2)],
    ["O que sobra no ano", "421,575 × 388,83 − 112.627,20 = 163.921,01 − 112.627,20", brl(c.E2_SOBRA, 2)],
    ["Margem", "51.293,81 ÷ 271.915,88", pct(c.E2_MARGEM) + " → risco (10% a 20%)"],
    ["Equilíbrio e folga", "112.627,20 ÷ 388,83 = 289,66 noites", f"{pct(c.E2_OCUPEQ)}; folga {dec(c.E2_FOLGA * 100, 1)} pontos"]], v=(2,), larg=("24%", "50%", "26%"),
    leg="Conferência: 421,575 × 388 = 163.571,10; 421,575 × 0,83 = 349,91; soma 163.921,01. 51.293,81 + 112.627,20 = 163.921,01. Bate. Repare: 20 pontos a mais de vendas pela plataforma custam cerca de R$ 6.500 por ano."))
add(tab(["E3 · Item", "Onde mora", "Por quê"], [
    ["Comissão da plataforma", "Degrau 2", "Sai antes de o dinheiro chegar"], ["Imposto sobre a receita", "Degrau 2", "Linha própria; a alíquota vem do contador"],
    ["Cancelamento", "Degrau 2", "Dedução da receita de hospedagem"], ["Lavanderia por estadia", "Degrau 3", "Custo de cada estadia"],
    ["Perdas e quebras de material", "Degrau 3", "Custo que cresce com a receita"], ["Salário da pessoa local", "Degrau 4", "Custo de cada mês"],
    ["13º e férias", "Degrau 4, em duodécimos", "Anual dividido por 12"], ["Seguro anual", "Degrau 4, em duodécimos", "Anual dividido por 12"],
    ["As horas da Marina", "Degrau 4 (retirada)", "O trabalho dela é custo"], ["Taxa de uma administradora", "Degrau 5", "Custo do modelo"],
    ["Troca dos colchões daqui a seis anos", "Degrau 6 (reserva)", "É para isso que a reserva existe"], ["Depreciação somada à reserva", "Nunca as duas", "Somar cria um prejuízo que não existe"],
    ["Parcela do empréstimo da obra", "Fora desta conta", "Custo da captação: Pilar 7"], ["Taxa de limpeza cobrada à parte", "Fora da receita de hospedagem", "Ela paga a limpeza"]], larg=("36%", "26%", "38%")))
add(tab(["E4", "Conta", "Resposta"], [
    ["O que fica de cada noite", "695 × 0,778 − 97,50", brl(c.E4_NOITE, 2)], ["O que sobra no ano", "421,575 × 443,21 − 112.627,20", brl(c.E4_SOBRA, 2)],
    ["Primeiro ano", "0,549351 × 186.846,26 − 112.627,20", brl(c.E4_ANO1, 2)],
    ["Tempo de volta", "1 + (791.131 + 9.983,09) ÷ 74.219,06", f"{dec(c.E4_VOLTA, 2)} anos → passo 3 «ajustar»"],
    ["Os R$ 50, com o custo aberto", "50 × 421,575 × 0,778", brl(c.E4_VALOR50, 2) + " por ano"],
    ["Os R$ 50, na margem da página 6", "50 × 421,575 × 0,40", brl(c.E4_VALOR50_P6, 2) + " por ano"]], v=(2,), larg=("26%", "44%", "30%"),
    leg="Por que a diferença: com o custo aberto, só as deduções, as perdas e a reserva crescem com a diária; o custo da noite e o fixo não. Na margem de referência, 60% de cada real some junto."))
fim()

# ---------------------------------------------------------------- 13
cap("13", "A sua página do Dossiê", "A página 6B <i>e a volta</i>",
    "A 6B não termina nela mesma. Ela volta para a página 6 e para a Planilha 2, célula a célula, e leva a decisão ao Pilar 7.",
    ["Uma conta que não volta para a página 6 fica solta, e o Pilar 7 lê a página 6.",
     "Com a ficha, o quadro «Como levar para a página 6» e o quadro «Planilha 2, célula a célula».",
     "Para você refazer a página 6 com a margem aberta, preencher a Planilha 2 e seguir ao Pilar 7."],
    ["A ficha «Faça agora · A sua conta»", "Como levar para a página 6", "Planilha 2, célula a célula", "A ordem do Mapa", "Perguntas, no checklist"],
    "Tudo o que você fez neste e-book vira uma página: a Página 6B · Viabilidade, irmã das páginas 6 e 6A. A ficha «Faça agora · A sua conta» faz as contas, lê as suas páginas 2, 6 e 6A do aparelho e baixa o PDF.")
add("<p>Na plataforma do curso, abra a aula «Faça agora · A sua conta». Ela lê o CAPEX e o giro da 6A e a margem da página 6 («veio da página 6A», «veio da página 6»), monta os seis degraus, o primeiro ano, os cinco passos, as alavancas, o veredito e a ação de 30 dias. Ela nunca põe um número no lugar do «Não sei». Esta ficha não envia nada: o PDF fica só com você. Salve o PDF da página 6B na pasta Meu Dossiê, ao lado das páginas 6 e 6A.</p>")
add("<h3>Como levar para a página 6</h3><p>Nada é gravado na ficha do Pilar 6: você digita dois campos. O resto não muda.</p>")
add(ex("O quadro da Marina", tab(["Campo da ficha do Pilar 6", "O que digitar", "Nota", "Marina"], [
    ["Margem operacional", "a margem do conservador × 100, com 2 casas", "3, se o imposto tem a resposta do contador e nenhuma linha está em branco; senão 1", f"{dec(c.MARGEM_P6, 2)} · nota 3"],
    ["Capital de giro (meses de custo)", "giro da 6B ÷ ((1 − margem digitada) × receita do conservador ÷ 12), com 2 casas", "", f"{dec(c.GIRO_MESES_P6, 2)}"],
    ["Diária, ocupações, unidades, linhas da folha, infraestrutura comum, terreno", "não mudam (Pilares 2 e 4 e 6A)", "", ""]], larg=("26%", "36%", "22%", "16%"))
    + f"<p>Conferência: 53.524,02 ÷ (0,7874 × 271.915,88 ÷ 12) = 3,00. Bate. A ficha do Pilar 6 vai mostrar: resultado do conservador {brl(c.P6R_RES, 2)}; giro {brl(c.P6R_GIRO, 2)}; investimento total {brl(c.P6R_INV, 2)}; tempo de volta {dec(c.P6R_VOLTA, 1)} anos; limite de 8 anos {brl(c.P6R_LIM, 2)}; base e otimista {dec(c.P6R_BASE, 1)} e {dec(c.P6R_OTIM, 1)} anos; veredito sugerido pela página 6: «Ajustar». Na 6B o nome é «Redesenhar»: as duas dizem «não assine a obra neste desenho».</p>"))
add(bx("Atenção", "A página 6 refeita e a 6B ficam próximas, não iguais", "<p>A página 6 mantém a margem igual nos três cenários e calcula o tempo de volta sem rampa: é a simplificação dela. Os números da página 6 refeita e os da 6B ficam próximos, não iguais. Os dois estão certos dentro da regra de cada um. Diferenças de alguns reais vêm da margem com duas casas.</p>", "escuro-b"))
add("<h3>Planilha 2, célula a célula</h3><p>A Planilha 2 · Estudo de Massas e Viabilidade não tem linha para tudo o que a 6B abre. O quadro diz onde lançar cada número e como contornar o que falta.</p>")
add(ex("A Planilha 2 da Marina", tab(["Aba e célula", "O que vai"], [
    ["Massas B9, B10, B11 (C e D: área e deck)", "as unidades da fase na tipologia certa; B12 tem de dar as unidades", "B11 = 3, C11 = 38, D11 = 16"],
    ["Investimento B5", "o CAPEX", "791.131"], ["Investimento B6", "0", "0"],
    ["Investimento B7", "=giro da 6B/B8 (sem arredondar)", "=53524,02/B8"],
    ["Modelo de renda B7:D7", "a diária nos três", "645"],
    ["Modelo de renda B8, C8, D8", "as três ocupações", "38,5% · 50% · 65%"],
    ["Modelo de renda B10:D10", "outras receitas ÷ hospedagem, se houver", "0"],
    ["Modelo de renda B11:D11", "comissão + cartão + cancelamento", "12,2% (9 + 1,2 + 2)"],
    ["Modelo de renda B12:D12", "custo por noite + perdas × diária + <b>reserva × diária</b>", "123,30 (57,50 + 40 + 6,45 + 19,35)"],
    ["Modelo de renda B13:D13", "o imposto (em branco: deixe vazio e anote)", "6%"],
    ["Modelo de renda B14:D14", "a taxa de gestão (0 se você opera)", "0"], ["Modelo de renda B15:D15", "0%", "0"],
    ["Modelo de renda B18 a B24", "os fixos nas sete linhas; retirada e aluguel em B24", "4.600 · 500 · 350 · 800 · 450 · 1.100 · 1.585,60"],
    ["Modelo de renda B50", "a sua taxa", "a dela"],
    ["Modelo de renda B65", "0", "0"]], larg=("30%", "40%", "30%"))
    + "<p>Por quê: a Planilha 2 não tem linha de reserva (lançada por noite na B12, ela sai certa nos três cenários e a linha do resultado vira o que sobra), tem uma linha só para o que sai além do imposto (B11), não tem linha de retirada (B24) e calcula o giro como meses × custo fixo (a fórmula na B7 reproduz o giro da 6B).</p>"
    + f"<p><b>Resultado esperado:</b> a linha NOI (B41, C41, D41) dá {m2(CO['sobra'])} / {m2(BA['sobra'])} / {m2(OT['sobra'])}, o que sobra nos três cenários; margem 21,3%; equilíbrio 25,4%; investimento {m2(c.INVEST6B)}; payback de 14,6 anos (sem rampa, giro no ano zero); valor presente negativo com qualquer taxa.</p>"
    '<p class="conf">Conferência: 645 × (1 − 0,122 − 0,06) − 123,30 = 404,31. Bate. Fixos: 4.600 + 500 + 350 + 800 + 450 + 1.100 + 1.585,60 = 9.385,60. Bate.</p>'))
add(bx("Atenção", "Não misture as duas réguas", "<p>A Planilha 2 põe o giro no ano zero e não tem rampa; a 6B põe o primeiro ano com rampa e testa o giro no colchão. Compare cada uma com a régua dela. As dicas da Planilha 2 (margem, taxa, múltiplo) são da planilha, não uma sugestão da Zion.</p>", "escuro-b"))
add("<h3>A ordem do Mapa, e a próxima etapa</h3><ol>"
    "<li><b>Salve</b> o PDF da página 6B na pasta Meu Dossiê, ao lado das páginas 6 e 6A.</li>"
    "<li><b>Refaça a página 6</b> com o quadro acima: a margem e os meses de giro.</li>"
    "<li><b>Planilha 1</b> (opcional, se ainda não fez pela 6A) e <b>Planilha 2</b> pelo quadro célula a célula.</li>"
    "<li><b>Pilar 7:</b> leve o veredito, o critério para parar e, se for Avançar ou Ajustar, o investimento refeito (CAPEX + giro da 6B) para o pedido. Se for Redesenhar ou Testar, os 90 dias do Pilar 7 servem para provar a premissa e refazer as páginas 6, 6A e 6B.</li></ol>")
add(bx("Atenção", "No Pilar 7, a Marina decide com a página 6 de referência", "<p>No Pilar 7 você vê a Marina decidir «avançar» com a página 6 de referência, porque ele foi escrito antes da conta aberta. Com a 6B, o critério que ela mesma escreveu dispara: antes de pedir dinheiro a alguém, ela redesenha e prova preço e semana.</p>", "crit"))
add("<h3>O que perguntar, sem número</h3><p>As perguntas ao contador (regime e imposto sobre a receita e as outras receitas; quando a resposta muda com a fase dois; encargos da retirada e do salário; imposto sobre o lucro e distribuição) e ao advogado (contratos de gestão, arrendamento ou sociedade) estão no <b>Checklist da página 6B</b>, que acompanha este e-book. Nenhuma delas pede número a quem responde de graça: quem traz o número é o contador, por escrito, com data.</p>")
fim()

# ---------------------------------------------------------------- Confira o que ficou
add('<section class="cap"><div class="cab"><div class="k">Revisão, resumo e Faça agora</div><span class="n">' + CHK.replace('.8em', '.75em') + '</span>'
    '<h2>Confira o que <i>ficou</i></h2><p class="deck">Responda de cabeça, sem voltar às páginas. Depois leia o resumo e preencha a sua página.</p></div><div class="regua"></div>')
add("<h3>Perguntas de revisão</h3>")
PP = [("1. Por que a margem da página 6 não serve para decidir a obra?", ["Porque foi feita antes da 6A", "Porque é a margem de referência, uma simplificação para a primeira conta; a que decide sai da sua lista", "Porque é alta"], "B. A página 6 fez a primeira conta. A margem real sai da sua lista de custos, com o seu trabalho e a reserva dentro."),
      ("2. A linha do imposto, sem resposta do contador…", ["Recebe 6%, como a Marina", "Fica em branco, com o nome, e o resultado sai antes do imposto", "Some da conta"], "B. Os 6% da Marina são resposta fictícia do contador dela e não valem para você."),
      ("3. Sobre o que se calcula o tempo de volta?", ["O resultado antes da reserva", "O que sobra, em escada, com o primeiro ano de rampa", "A receita bruta"], "B. A reserva vai ser gasta; o retorno se mede depois dela."),
      ("4. A conta não fechou. O que fazer primeiro?", ["Mexer em tudo de uma vez", "Mexer uma alavanca por vez e escrever o que precisaria ser provado", "Usar o cenário otimista"], "B. Quando a conta não fecha, a conta está certa. O redesenho é uma alavanca por vez.")]
add("".join(pare(p, o, r) for p, o, r in PP))
add(bx("Resumo", "O 6B em dez linhas", '<ol class="dez">'
       "<li>A 6B é a irmã das páginas 6 e 6A: abre a linha «quanto sobra».</li>"
       "<li>Seis degraus: receita bruta, receita real, contribuição, antes da reserva, depois do modelo, o que sobra.</li>"
       "<li>A receita se mede: diária média do ano, ocupação dos doze meses, rampa a partir do mês de abertura.</li>"
       "<li>O imposto sobre a receita é linha própria; sem o contador, em branco.</li>"
       "<li>Custo de cada noite e custo de cada mês; anuais em duodécimos; o seu trabalho é custo.</li>"
       "<li>Reserva de reposição desde o primeiro ano; reserva ou depreciação, nunca as duas.</li>"
       "<li>Equilíbrio lido com a folga; o mês que aperta decide o giro e o colchão.</li>"
       "<li>Lucro e retorno são coisas diferentes: tempo de volta em escada, valor presente com a sua taxa, terreno e venda ao lado.</li>"
       "<li>Régua em cinco passos: Avançar, Testar, Ajustar, Pausar ou Redesenhar, com o critério para parar escrito.</li>"
       "<li>A 6B volta para a página 6 e para a Planilha 2, célula a célula, e leva a decisão ao Pilar 7.</li></ol>", "levar"))
add(faca("A minha página 6B", [("Os seis degraus, com a origem de cada número, e o que sobra no conservador:", True), ("A minha margem aberta, ao lado da margem da página 6:", False),
                               ("O equilíbrio e a folga; o menor saldo do primeiro ano; o giro e o colchão:", False), ("O tempo de volta em escada e os cinco passos:", False),
                               ("O meu veredito e o meu critério para parar:", False), ("A minha ação de 30 dias, o prazo e como verificar:", False)],
         nota="Depois de preencher, abra na plataforma do curso a aula «Faça agora · A sua conta» e passe as respostas para a ficha. Ela gera a página 6B do seu Dossiê em PDF."))
add("<h3>Fontes deste e-book</h3><p style=\"font-size:8pt\">Pilar 6 · Pré-viabilidade (e-book e ficha: a margem de referência, a rampa, as duas contas do giro, o tempo de volta, as frases-assinatura); Pilares 2, 4 e 5 (diária, curva do ano, cenários, fase um); Pilar 7 · Capital e Dossiê (o plano de 90 dias); aprofundamento 6A · CAPEX; Marco Zero e Comece aqui (as situações, a pasta Meu Dossiê); e-books «Receitas, Custos e Modelos de Rentabilidade» e «Viabilidade e Análise de Investimentos» (os seis degraus, o equilíbrio, a escada); Jornada do COMO (Etapas 02, 08 e 09; nomes como Ponto de Equilíbrio Zion™ e Conta da Retirada™, usados como na fonte); Volume A05 · Investimento (caps. 08, 09, 11 e 12); Volume 05 · Investimento (cap. 08); Volume 04 · Estratégia (cap. 13); a régua da Zion de viabilidade (cinco passos, rampa de 40%, 50% e 75%, colchão de 10%, múltiplo de referência); Planilha 2 e Mapa de direcionamento, etapa 6. As faixas são citadas pelas fontes e não têm base estatística declarada. Os seis degraus com nomes próprios, as janelas da rampa, o colchão como giro mais o menor saldo, o corte de 5 pontos na folga e os mapeamentos para a página 6 e para a Planilha 2 são elaboração própria da Zion.</p>")
add(f'<p class="fim">{AVISO} A Marina é um exemplo ilustrativo: os números novos são fictícios e não são preços de referência; o imposto de 6% é resposta fictícia do contador dela, para o caso dela, e não vale para você; a margem de 40% da página 6 dela é a referência orientativa do Pilar 6, não confirmada (a Zion também vende esse tipo de estrutura). {CEN} Este material não promete retorno, renda, ocupação, crédito, parceria nem aprovação. © Zion Hotel Group International.</p></section>')

# ---------------------------------------------------------------- saída e conferências do texto
html = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>E-book Aprofundamento 6B · Viabilidade</title>'
        f"<style>{css(OUT)}</style></head><body>" + "\n".join(H) + "</body></html>")
texto = re.sub(r"<[^>]+>", " ", html.split("<body>")[1])
assert "—" not in texto and "–" not in texto, "travessão no texto"
for proibido in ("Helena", "Ribeirão", "Rodrigo", "Priscila", "Bloco 1", "Bloco 2", "aluno", "membro", "Ferramenta 01", "Ferramenta 10", "B08", "B09",
                 "inflada", "otimista demais", "estava errada", "Cenário que só mexe na ocupação", "ZAIOS", "garantid", "renda passiva", "lucro certo"):
    assert proibido not in texto, f"termo proibido no e-book: {proibido}"
for sigla in ("NOI", "EBITDA", "VPL", "TIR", "payback", "ROI"):
    n = len(re.findall(rf"\b{sigla}\b", texto))
    assert 1 <= n <= 3, (sigla, n)
assert texto.count("™") <= 2
(OUT / "ebook.html").write_text(html, encoding="utf-8")
print("ebook.html", len(html) // 1024, "KB")

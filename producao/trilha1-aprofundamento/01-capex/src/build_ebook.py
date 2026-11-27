"""Gera o HTML do e-book «Aprofundamento 6A · CAPEX» (Trilha 1 · Pilar 6), no molde visual e narrativo do e-book do Pilar 6.
Caso: a Marina abre a página 6 dela (PLANO.md v2, seção 7). Todos os números vêm de src/caso.py, que confere cada
valor com o plano e falha se algum divergir.
Saída: src/ebook/ebook.html. Depois:
  node src/render.js src/ebook/ebook.html ../../../docs/trilha1/materiais/Pilar-6A-CAPEX-ebook.pdf
Uso: python3 -I src/build_ebook.py"""
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from estilo import css, AVISO, FICT, CURSO
import caso as c

OUT = pathlib.Path(__file__).resolve().parent / "ebook"; OUT.mkdir(exist_ok=True)
brl, num, pct = c.brl, c.num, c.pct
REF6 = "Referência orientativa da página 6, não confirmada; a Zion também vende esse tipo de estrutura."
H = []
CHK = '<svg viewBox="0 0 24 24" style="width:.8em;height:.8em;vertical-align:-.05em"><path d="M3 13l6 6L21 5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
add = H.append


# ---------------------------------------------------------------- peças do molde do Pilar 6
def cap(nn, rotulo, titulo, deck, porque, neste, abre):
    add(f'<section class="cap"><div class="cab"><div class="k">Capítulo {nn}<b>{rotulo}</b></div><span class="n">{nn}</span>'
        f'<h2>{titulo}</h2><p class="deck">{deck}</p></div><div class="regua"></div>'
        f'<div class="porque"><div><span>Por que fazer isso</span>{porque[0]}</div><div><span>Como vamos fazer</span>{porque[1]}</div>'
        f'<div><span>Para que serve</span>{porque[2]}</div></div>'
        + bx("Neste capítulo", "", "<ul>" + "".join(f"<li>{i}</li>" for i in neste) + "</ul>")
        + f'<p class="abre">{abre}</p>')


def fim():
    add("</section>")


def bx(k, titulo, corpo, cls=""):
    return f'<div class="bx {cls}"><span class="k">{k}</span>' + (f"<h4>{titulo}</h4>" if titulo else "") + corpo + "</div>"


def ex(titulo, corpo, k=FICT):
    # caixa de exemplo com tabela longa pode continuar na página seguinte (as linhas da tabela não se partem)
    return bx(k, titulo, corpo, "ex longa" if corpo.count("<tr") > 12 else "ex")


def pare(pergunta, opcoes, resposta):
    ops = "".join(f'<p class="op"><b>{chr(65 + i)}</b>{o}</p>' for i, o in enumerate(opcoes))
    return bx("Pare e pense", "", f'<p style="font-weight:650">{pergunta}</p>{ops}<p class="ver">Ver a resposta</p><p class="resp">{resposta}</p>', "pare")


def aplic(nao, opera, titulo="No seu caso"):
    return bx("Aplicação", titulo, f"<p><b>Se você ainda não hospeda:</b> {nao}</p><p><b>Se você já opera e quer crescer:</b> {opera}</p>", "escuro-b")


def faca(titulo, campos, nota="Escreva no papel ou direto na ficha «Faça agora · O seu CAPEX». Esta página não guarda nada."):
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


ORIG = {"C": "Cotação", "E": "Estimativa", "B": "Em branco", "NA": "Não se aplica"}


def orig(l):
    if l[2] == "C":
        return f"Cotação ({l[3]})" + (f" · {l[5].strftime('%d/%m')}" if l[5] else "")
    return ORIG[l[2]]


def tab_parte(i, leg=""):
    nome, ls = c.PARTES[i]
    rows = [[l[0], l[1] if l[1] not in ("valor", "") else "", orig(l), num(l[6]) if l[2] in "CE" else "0"] for l in ls]
    rows.append([f"!Total da Parte {i + 1}", "", "", num(c.TOT[i])])
    leg = leg or "Cotação (n): número de propostas escritas, com data; com duas ou mais, todas com a mesma especificação."
    return tab(["Linha", "Conta", "Origem", "R$"], rows, v=(3,), larg=("52%", "18%", "18%", "12%"), leg=leg)


# ---------------------------------------------------------------- capa e sumário
add(f"""<div class="capa"><div class="k">Trilha 1 · Pilar 6 · Aprofundamento 6A · Método Zion</div>
<h1>CAPEX:<br><i>quanto custa abrir a porta, linha por linha</i></h1>
<p class="deck">Com a página 6 na mão, a conta aberta em sete partes: o que tinha ficado à parte entra, cada referência vira cotação ou linha em branco, e o limite da página 6 confere se ainda cabe. Ao fim deste e-book você está pronto para a página 6A do seu Dossiê, CAPEX.</p>
<div class="pe">{CURSO}</div><span class="num">6A</span></div>""")

SUM = [("00", "Como usar este aprofundamento"), ("01", "A página 6 da Marina é o ponto de partida"),
       ("02", "Da folha de oito linhas às sete partes do custo"), ("03", "Cada número tem origem: cotação, estimativa ou em branco"),
       ("04", "Parte 1 e Parte 2: o que aprova a obra e o que leva a obra até o terreno"), ("05", "Parte 3: o metro quadrado inteiro"),
       ("06", "Partes 4 e 5: a unidade-modelo e um dia de operação"), ("07", "Parte 6 e Parte 7: a abertura e o imprevisto"),
       ("08", "Ler o número antes de mostrá-lo"), ("09", "A conta da Marina, inteira"), ("10", "Pratique com a Marina"),
       ("11", "A página 6A e a volta"), (CHK, "Confira o que ficou")]
add('<div class="sum"><div class="k">Sumário</div><h2>O que tem <i>neste e-book</i></h2><table>'
    + "".join(f'<tr><td class="n">{n}</td><td>{t}</td></tr>' for n, t in SUM) + "</table></div>")

# ---------------------------------------------------------------- 00
cap("00", "Antes de começar", "Como usar <i>este aprofundamento</i>",
    "Ele acompanha o Pilar 6. A aula mostra o caminho; aqui você abre a conta com calma, com calculadora e com as páginas 5 e 6 do Dossiê abertas ao lado.",
    ["A página 6 trouxe a primeira conta inteira, com referências e duas linhas à parte. Antes de assinar, cada linha precisa de origem.",
     "Abrindo a linha «quanto custa abrir a porta» em sete partes, com a Marina como exemplo do começo ao fim.",
     "Para você sair com a página 6A do Dossiê e refazer a página 6 com números que se defendem."],
    ["Este aprofundamento em três respostas", "Antes que você pense", "Duas situações, o mesmo método", "Como ler", "Revisite · Pilar 6"],
    "Seja bem-vindo ao aprofundamento 6A. Você já fez a página 6 no Pilar 6. Aqui ela ganha uma página irmã, a 6A, que abre as linhas da página 6 uma por uma.")
add(bx("Antes de começar", "Este aprofundamento em <i>três respostas</i>", """<div class="tres">
<div><span class="nn">1</span><b>O que você vai aprender</b><ul><li>As sete partes do custo de abrir a porta</li><li>Onde cada linha da página 6 vai parar</li><li>Como dar origem a cada número</li><li>Como conferir se a conta cabe no limite da página 6</li></ul></div>
<div><span class="nn">2</span><b>Por que aprender isso</b><ul><li>A página 6 deixou a infraestrutura comum à parte</li><li>Referência não é cotação</li><li>A conta que passa do limite depois da obra assinada não tem volta barata</li></ul></div>
<div><span class="nn">3</span><b>O resultado que você vai ter</b><ul><li>A página 6A, com as sete partes, a origem e o que falta cotar</li><li>O CAPEX da fase e o investimento total</li><li>A folga até o limite da página 6</li><li>A página 6 pronta para ser refeita</li></ul></div></div>"""))
add('<div class="pergunta"><span>?</span>Quanto custa abrir a porta, linha por linha, e a conta ainda cabe no limite que a minha página 6 escreveu?</div>')
add("<p>A pergunta do pilar continua a mesma: <b>o negócio se paga?</b> A 6A não troca de assunto. Ela abre a linha mais pesada da resposta, o custo de abrir a porta, para que cada parte dele tenha nome, valor e origem.</p>"
    "<p>As unidades da fase um e do projeto completo, e as áreas de apoio, vêm do masterplan do Pilar 5. O que não se constrói não se orça. Por isso, tenha a página 5 aberta: é dela que saem as quantidades, as áreas e o «desenha para 5».</p>")
add(bx("Antes que você pense", "Três dúvidas comuns neste ponto",
       "<p><b>«Já fiz a página 6. Preciso disso?»</b> A página 6 é a conta de referência. Antes de assinar obra, ela precisa de cotação e da infraestrutura comum. A 6A é esse passo, e é o passo que o Pilar 7 pede à Marina.</p>"
       "<p><b>«Não tenho cotação nenhuma.»</b> Ótimo começo. A primeira versão sai com estimativas e linhas em branco nomeadas. Uma linha em branco vale mais do que um número inventado (Pilar 6).</p>"
       "<p><b>«E se a conta passar do limite?»</b> Então a 6A fez o trabalho dela. Descobrir no papel, e não na obra, é o momento mais barato. O Pilar 7 diz o caminho: voltar à conta e ajustar o tamanho, o produto ou a fase.</p>", "crit"))
add(bx("Duas situações, o mesmo método", "",
       "<p>Na primeira tela da ficha você escolhe a sua situação com as mesmas palavras do Marco Zero: <b>«Tenho um terreno e ainda não hospedo ninguém»</b>, <b>«Tenho uma ideia, ou o capital, e ainda não tenho o terreno»</b> ou <b>«Já opero uma hospedagem e quero crescer»</b>. O método serve para Airbnb, casas, apartamentos, pousadas e glampings.</p>"
       "<p><b>Se você ainda não hospeda:</b> faça cada parte sobre o masterplan do Pilar 5, a fase um e o projeto completo. Sem terreno escolhido, deixe a Parte 2 nomeada e em branco: a infraestrutura só se fecha com o terreno.</p>"
       "<p><b>Se você já opera e quer crescer:</b> monte o CAPEX da ampliação, com a rede existente como ponto de partida, e troque cada estimativa pelo seu extrato de doze meses. Não pague a obra com o caixa da operação.</p>", "escuro-b"))
add(bx("Como ler", "Quatro tipos de caixa", f"""<ul>
<li><b>Caixas de exemplo:</b> a Marina continua com a gente, como exemplo ilustrativo. Os números da página 6 dela levam o rótulo «{REF6[0].lower() + REF6[1:-1]}». Os números novos levam «{FICT}» Eles ensinam a conta. Não dizem quanto custa o seu projeto.</li>
<li><b>Caixas «Faça agora»:</b> escreva no papel ou direto na ficha. Esta página não guarda nada.</li>
<li><b>Caixas «Pare e pense»:</b> responda de cabeça antes de ler a resposta.</li>
<li><b>A convenção das contas:</b> valores em reais de hoje; cada conta fecha com «Conferência: … Bate.»; «cerca de» antes de número arredondado.</li></ul>
<p class="nota">{AVISO}</p>"""))
add(bx("Revisite · Pilar 6", "Três perguntas do Pilar 6, sem voltar às páginas",
       "<p>1 · O que ficou à parte na página 6 da Marina? 2 · Sobre o que a base simplificada calcula a reserva? 3 · Até quanto o investimento total dela aguenta dentro de 8 anos no conservador?</p>"
       f"<p>(Respostas: 1 · a infraestrutura comum, «a cotar», e o terreno; 2 · sobre as unidades prontas, 10%; 3 · até cerca de R$ 870 mil, {brl(c.LIMITE6, 2)}.)</p>"))
add("<h3>Os cinco erros, retomados</h3><p>No Pilar 6 você viu os cinco erros do orçamento amador. Aqui eles não se repetem: cada um vira uma parte da conta, com lugar próprio.</p>")
add(tab(["O erro (Pilar 6)", "Onde a 6A resolve"], [
    ["Orçar só as unidades", "Partes 2 e 3: infraestrutura comum e áreas comuns entram"],
    ["Usar o preço de outra região, ou de outro ano", "Capítulo 03: cotação com data e validade de 90 dias"],
    ["Esquecer os suprimentos da operação", "Parte 5: um dia de operação em cinco listas"],
    ["Tratar a reserva como opcional", "Parte 7: percentual e regra de uso escrita"],
    ["Esquecer o caixa dos primeiros meses", "Capital de giro ao lado, somado no investimento total"]], leg="Os cinco erros do orçamento amador (Pilar 6 · Pré-viabilidade)", larg=("45%", "55%")))
fim()

# ---------------------------------------------------------------- 01
cap("01", "Onde você está", "A página 6 da Marina <i>é o ponto de partida</i>",
    "Um número inteiro, com duas observações escritas ao lado. A 6A começa exatamente onde ele parou.",
    ["Quem parte do zero refaz o que já fez. Quem parte da página 6 sabe o que falta abrir.",
     "Relendo a folha de oito linhas da Marina, as duas observações e o limite que ela escreveu.",
     "Para você escrever o seu número de partida, com data, e o seu limite."],
    ["A folha de oito linhas da Marina", "As duas observações", "O limite da página 6", "O seu número de partida"],
    f"No Pilar 6, a Marina fez a primeira conta inteira. Três cabanas de madeira para casal, 38 m² internos e 16 m² de deck, abre com 3 e desenha para 5. O investimento total da fase um ficou em cerca de R$ 690 mil.")
add("<p>É uma conta honesta porque diz o que é. As seis primeiras linhas usam a referência da unidade pronta. As licenças são uma estimativa. A reserva é 10% das unidades. E duas coisas ficaram à parte, escritas: o terreno, fora da conta, e a infraestrutura comum, «a cotar».</p>")
add(ex("A folha de oito linhas da Marina", tab(["Linha da página 6", "R$", "Origem"], [
    ["1 a 6 · Três unidades prontas, com mobília", num(c.P6_UNID, 2), "Referência (3 × 192.346)"],
    ["7 · Licenças e projetos", num(c.P6_LICENCAS, 2), "Estimativa, propostas pedidas"],
    ["8 · Reserva do imprevisto", num(c.P6_RES, 2), "10% das unidades"],
    ["!Soma da folha", num(c.P6_FOLHA, 2), ""],
    ["Capital de giro", num(c.GIRO, 2), "Três meses de custo"],
    ["!Investimento total da fase um", num(c.P6_TOTAL, 2), "Cerca de R$ 690 mil"],
    ["~À parte · terreno", "fora da conta", "R$ 600 mil, dela"],
    ["~À parte · infraestrutura comum", "a cotar", "Acesso, caminhos, apoio, rede para 5"]], v=(1,), larg=("48%", "20%", "32%"))
    + f'<p class="conf">Conferência (Pilar 6): 577.038 + 15.000 = 592.038; + 57.703,80 = 649.741,80; + 40.787,38 = 690.529,18. Bate.</p><p class="nota">{REF6}</p>',
    k="Exemplo ilustrativo · a página 6 da Marina"))
add("<h3>As duas observações</h3><p>O Pilar 6 deixou escrito que esse número é «orientativo, sem cotação ainda, e sem a infraestrutura comum do terreno». Quem mostrasse o número sem as duas observações mostraria o número mais bonito, e o mais perigoso. A 6A trata as duas, uma por uma: troca a referência por cotação ou por linha em branco e põe a infraestrutura comum dentro da conta.</p>")
add(cita("Um projeto hoteleiro não morre quando falta dinheiro. Morre quando os números nunca foram feitos.", "Volume A05 · Investimento, cap. 1"))
add("<h3>O limite que a página 6 escreveu</h3>"
    "<p>No fim da página 6 existe a seção «o que precisa ser verdade». Ela diz até onde o investimento total pode ir para a operação pagar a obra dentro de 8 anos no cenário conservador. Esse é o limite que a 6A confere no fim.</p>")
add(ex("O limite da Marina", f"<p>Receita do conservador: 1.095 noites × 38,5% × R$ 645 = R$ 271.915,88. Resultado, com a margem de referência de 40%: {brl(c.RESULT_CONS, 2)} por ano. Limite: 8 × 108.766,35 = <b>{brl(c.LIMITE6, 2)}</b>, cerca de R$ 870 mil.</p>"
       f"<p>A folga da página 6: 870.130,80 − 690.529,18 = <b>{brl(c.P6_FOLGA, 2)}</b>, «para a infraestrutura comum e para as cotações». Conferência: 690.529,18 + 179.601,62 = 870.130,80. Bate.</p>"
       f'<p class="nota">A margem de 40% é a referência orientativa da página 6. {REF6}</p>', k="Exemplo ilustrativo · a página 6 da Marina"))
add("<p>No Pilar 7, a Marina decidiu avançar com a fase um de três cabanas, com um critério: se o investimento total, com as cotações e a infraestrutura comum, passar de cerca de R$ 870 mil, ela volta à conta antes de assinar. A 6A é a ferramenta que confere esse critério.</p>")
add(pare("O que a página 6 da Marina deixou à parte, por escrito?", ["As licenças e os projetos", "O terreno e a infraestrutura comum", "O capital de giro"],
         "B. O terreno fica fora da conta (mas não de graça) e a infraestrutura comum ficou «a cotar». O giro está somado no investimento total."))
add(aplic("pegue o PDF da sua página 6 na pasta Meu Dossiê e circule o investimento total da fase um, a data e o que ficou à parte.",
          "a sua página 6 já partiu do extrato. Circule o que ainda é estimativa e o que a ampliação não incluiu (rede, acesso, área comum)."))
add(faca("O meu ponto de partida", [("O investimento total da fase um da minha página 6, e a data:", False), ("O meu limite (página 6, «o que precisa ser verdade»):", False), ("O que ficou à parte na minha página 6:", False)]))
add(levar(["A 6A começa na página 6, não do zero.", "A página 6 da Marina: cerca de R$ 690 mil, com referência e duas linhas à parte.", "O limite da página 6: até cerca de R$ 870 mil.", "A 6A confere o critério que o Pilar 7 escreveu."]))
fim()

# ---------------------------------------------------------------- 02
cap("02", "O mapa da conta", "Da folha de oito linhas <i>às sete partes do custo</i>",
    "Cada linha da página 6 tem um endereço na 6A. O que estava à parte entra, e o que não estava ganha linha.",
    ["Sem o mapa, a mesma coisa é contada duas vezes, ou nenhuma.",
     "Com a caixa «Do Pilar 6 para a 6A» e o diagrama dentro, ao lado, à parte.",
     "Para você saber onde cada gasto mora antes de pedir a primeira cotação."],
    ["Do Pilar 6 para a 6A", "As sete partes", "Dentro, ao lado, à parte", "A base da reserva muda"],
    "A página 6 tem oito linhas, de propósito: é a conta que cabe numa tarde. A 6A usa sete partes, porque é a conta que vai para o engenheiro, para o fornecedor e para quem financia.")
add(cita("Não é quanto custa a cabana. É quanto custa abrir a porta.", "Pilar 6 · Pré-viabilidade"))
add(bx("Do Pilar 6 para a 6A", "Onde cada linha da página 6 vai parar", tab(["Na página 6 (folha de oito linhas)", "Na página 6A"], [
    ["Linhas 1 a 6 · unidade pronta (unidade, deck, luz, água e esgoto, mobiliário com enxoval, piso)", "Unidade, deck e piso → Parte 3; luz e água de cada unidade → Parte 2; mobiliário → Parte 4; enxoval e utensílios → Parte 5"],
    ["Linha 7 · licenças e projetos", "Parte 1 (o que aprova projeto e obra); licença de operar → Parte 6"],
    ["Linha 8 · reserva do imprevisto (10% das unidades)", "Parte 7 (% do subtotal das Partes 1 a 6, com regra de uso)"],
    ["À parte · infraestrutura comum («a cotar»)", "<b>Entra:</b> rede, acesso, caminhos e estacionamento → Parte 2; apoio e deck da crista → Parte 3"],
    ["Não estava", "Parte 6 · pré-abertura"],
    ["À parte · capital de giro (somado)", "Igual: ao lado, somado no investimento total"],
    ["À parte · terreno (fora da conta)", "Igual: ao lado, não somado"]], larg=("44%", "56%"))))
add("<h3>As sete partes</h3>")
add(tab(["Parte", "O que entra", "A pergunta-chave"], [
    ["1 · Projetos, licenças e documentação", "Levantamento, arquitetura, complementares, aprovação, responsabilidade técnica", "O que aprova o projeto e a obra?"],
    ["2 · Infraestrutura", "Acesso, estacionamento, caminhos, energia, água, esgoto, drenagem, internet", "O que leva a obra até o terreno, e para quantas unidades?"],
    ["3 · Unidades e áreas comuns", "Unidades, decks, apoio, áreas comuns", "Quantos metros quadrados, a quanto o m²?"],
    ["4 · Mobiliário e equipamentos", "A unidade-modelo e os equipamentos gerais", "O que o hóspede toca?"],
    ["5 · Enxoval, utensílios e suprimentos", "Três jogos por cama, utensílios, limpeza, manutenção, segurança", "O que um dia de operação gasta?"],
    ["6 · Pré-abertura", "Licença de funcionar, fotos, lançamento, treinamento, seguro, abertura de teste", "O que acontece antes do primeiro hóspede?"],
    ["7 · Reserva do imprevisto", "Um percentual do subtotal, com regra de uso", "Quem autoriza gastar, e em quê?"]], larg=("30%", "40%", "30%"), leg="As sete partes do custo de abrir a porta"))
add("<h3>Dentro, ao lado, à parte</h3><p>Três palavras resolvem quase toda dúvida de onde um gasto mora.</p>")
add('<div class="dia"><div class="on"><h4>Dentro</h4>As sete partes. A soma delas é o <b>CAPEX da fase</b>: o custo de abrir a porta.</div>'
    '<div><h4>Ao lado</h4>O <b>capital de giro</b>. Não compra nada que fique no terreno, mas precisa estar no banco no dia da abertura. CAPEX + giro = <b>investimento total da fase um</b>.</div>'
    '<div><h4>À parte</h4>O <b>terreno</b>, anotado e não somado: fora da conta não quer dizer de graça (Pilar 6). O <b>custo da captação</b> (juros, taxas) fica no Pilar 7.</div></div>')
add("<p>O nome técnico é CAPEX, do inglês capital expenditure: a despesa de capital, o que se gasta uma vez para construir e equipar. As siglas que você vai ouvir do profissional, e que a Planilha 1 usa nos nomes das abas: <b>FF&amp;E</b>, mobiliário e equipamentos (a nossa Parte 4), e <b>OS&amp;E</b>, enxoval, utensílios e suprimentos (a nossa Parte 5). Daqui em diante, usamos os nomes por extenso.</p>")
add("<h3>A base da reserva muda</h3><p>No Pilar 6, a base simplificada calcula a reserva sobre as unidades prontas: 10% de 577.038. Na 6A, a reserva é um percentual do <b>subtotal das Partes 1 a 6</b>, porque o imprevisto também acontece na rede, no apoio e nas licenças. E na primeira obra a fonte pede o teto da faixa, ou acima. O capítulo 07 faz a conta.</p>")
add(pare("Onde entra o capital de giro na 6A?", ["Dentro, como Parte 8", "Ao lado: somado no investimento total, fora do CAPEX", "À parte, como o terreno"],
         "B. O giro não é custo de abrir a porta, mas é dinheiro que precisa existir no dia da abertura. Por isso entra no investimento total, ao lado do CAPEX."))
add(aplic("pegue a sua folha de oito linhas e escreva ao lado de cada linha o número da parte da 6A para onde ela vai.",
          "faça o mesmo com a ampliação: a unidade nova, o reforço da rede existente e a área comum ganham parte própria."))
add(levar(["Sete partes = CAPEX da fase.", "CAPEX + giro = investimento total da fase um.", "Terreno ao lado, não somado; captação no Pilar 7.", "A infraestrutura comum entra; a pré-abertura ganha linha.", "A reserva passa a ser % do subtotal das Partes 1 a 6."]))
fim()

# ---------------------------------------------------------------- 03
cap("03", "A origem", "Cada número tem origem: <i>cotação, estimativa ou em branco</i>",
    "Na 6A, a referência sai de cena. Cada linha diz de onde veio o número, ou diz que ainda não tem número.",
    ["Um número sem origem não se defende diante de um engenheiro, de um sócio ou de um banco.",
     "Com as três origens, as três cotações comparáveis, a lista do que não inclui e a validade.",
     "Para você saber quanto da sua conta está apoiado em papel."],
    ["As três origens", "Três cotações com a mesma especificação", "O que «não inclui»", "A validade de 90 dias"],
    "No Pilar 6, cada linha tinha uma nota: referência, falado, cotação. Na 6A, a referência da Zion não entra mais na conta. Ou o número veio de uma proposta escrita, ou é uma estimativa sua, ou a linha fica em branco, com nome.")
add(tab(["Origem na 6A", "O que é", "Nota na página 6"], [
    ["Cotação", "Proposta escrita, com escopo e data", "3"],
    ["Estimativa", "Número seu, sem proposta (inclui o «falado, sem papel»)", "1"],
    ["Em branco", "Linha nomeada, ainda sem número: vale zero e conta como risco", "Não sei"],
    ["Não se aplica", "A linha não existe no seu projeto, por decisão escrita", "-"]], larg=("20%", "60%", "20%"), leg="As origens de cada número e a nota que vai para a página 6"))
add("<p>A ficha nunca põe valor no lugar do «Não sei». Uma linha em branco vale mais do que um número inventado (Pilar 6): ela vira tarefa, com nome. Onde não souber, marque «Não sei»: vira a sua tarefa da semana (Comece aqui).</p>")
add("<h3>Três cotações com a mesma especificação</h3><p>Cotação boa é cotação comparável. Para isso, todos os fornecedores recebem o mesmo pacote: projeto, memorial e quantidades. E cada pedido traz a especificação escrita:</p>"
    "<ul><li>material, medidas e quantidade;</li><li>frete, instalação e retirada de entulho;</li><li>prazo e garantia;</li><li>a lista do que <b>não inclui</b>, por escrito.</li></ul><p>A menor proposta só vence onde o escopo é igual.</p>")
add(cita("A frase «não inclui» é a mais importante de qualquer proposta.", "Jornada do COMO, Etapa 04, Passo 09"))
add("<h3>A validade</h3>")
add(cita("Cotação de mais de noventa dias precisa ser refeita.", "Volume 05 · Investimento, cap. 4"))
add(ex("A cotação da água da Marina venceu", "<p>A Marina pediu a cotação do poço com teste de vazão, do reservatório e da rede para 5 no Pilar 5, em 15/07/2026: R$ 19.800, com duas propostas iguais. Hoje, no exemplo, é 27/11/2026.</p>"
       "<p>De 15/07 a 27/11: 16 + 31 + 30 + 31 + 27 = <b>135 dias</b>. Passou de 90. A linha continua na conta, mas a ficha acende o alerta «cotação com mais de 90 dias: refaça antes de usar».</p>"
       '<p class="conf">Conferência: julho (16 dias restantes) + agosto 31 + setembro 30 + outubro 31 + novembro 27 = 135. Bate.</p>'))
add(pare("Duas propostas para o caminho do hóspede: uma inclui a luz baixa, a outra não diz. O que a Marina faz?", ["Escolhe a menor", "Pede às duas a lista do que não inclui e iguala o escopo", "Tira a média"],
         "B. Sem o «não inclui» escrito, as propostas não são comparáveis. Primeiro iguala o escopo, depois compara."))
add(aplic("separe as três maiores linhas da sua conta e escreva a especificação de cada uma antes de pedir proposta.",
          "use as notas da última obra: o que veio cobrado à parte vira item obrigatório do «não inclui»."))
add(levar(["Três origens: cotação, estimativa, em branco.", "Na 6A a referência não entra na conta.", "Três propostas com a mesma especificação.", "O «não inclui» por escrito.", "Mais de 90 dias: refaça."]))
fim()

# ---------------------------------------------------------------- 04
cap("04", "Partes 1 e 2", "Parte 1 e Parte 2: <i>o que aprova a obra e o que leva a obra até o terreno</i>",
    "A primeira parte é papel. A segunda é distância e capacidade, e é a que mais varia de um terreno para outro.",
    ["Projetos e infraestrutura são as linhas que a página 6 deixou mais vagas.",
     "Separando o que aprova a obra do que autoriza operar, e orçando a rede para o projeto completo.",
     "Para você pedir as cotações certas à prefeitura, à concessionária e ao projetista."],
    ["Parte 1 · Projetos, licenças e documentação", "As perguntas do terreno", "Parte 2 · Infraestrutura", "Dimensionar para o projeto completo"],
    "A Parte 1 tem só o que aprova o projeto e a obra: levantamento, arquitetura, projetos complementares, aprovação na prefeitura, responsabilidade técnica e, se houver, licença ambiental. A licença de funcionamento, que autoriza operar, vai para a Parte 6.")
add(ex("A Parte 1 da Marina", tab_parte(0) + '<p class="conf">Conferência: 6.200 + 16.500 + 9.800 + 2.500 + 1.000 = 36.000. Bate. A licença ambiental fica em branco até a prefeitura responder.</p>'))
add("<h3>A Parte 2 começa com perguntas</h3><p>Antes de qualquer número, o terreno responde a seis perguntas:</p>"
    "<ul><li>Qual a distância até o ponto de energia? A concessionária informa.</li><li>A água vem de rede, poço ou nascente? Qual a vazão? Precisa de outorga?</li>"
    "<li>O solo pede fundação especial?</li><li>Um caminhão chega até as unidades em dia de chuva?</li><li>Qual a declividade?</li><li>Qual o prazo das licenças?</li></ul>")
add(cita("O amador orça o chalé. O developer orça o que faz o chalé funcionar.", "Volume A05 · Investimento, cap. 4"))
add("<h3>Construir uma vez</h3><p>A rede se orça por distância e capacidade, e se dimensiona para o projeto completo do Pilar 5, mesmo que a fase um tenha menos unidades. A diferença entre a rede para 3 e a rede para 5 é pequena na vala aberta. Refazer vala e caminho na fase dois é a forma mais cara de economizar.</p>"
    "<p>A Parte 2 também recebe duas linhas que estavam dentro da unidade pronta da página 6: a ligação de luz e a água e esgoto <b>de cada unidade</b>. Elas continuam por unidade, só mudam de endereço.</p>")
add(ex("A Parte 2 da Marina", f"<p>Energia a {c.DIST_ENERGIA_M} m, informada pela concessionária no exemplo. Rede dimensionada para {c.REDE_PARA}, com duto vazio para a 4ª e a 5ª cabana. Caminho do hóspede de cerca de 120 m desde a clareira do estacionamento, como no Pilar 5.</p>"
       + tab_parte(1) + '<p class="conf">Conferência: 24.000 + 7.200 + 16.800 + 31.500 + 19.800 + 14.500 + 4.200 + 5.400 + 4.800 = 128.200. Bate.</p>'))
add(pare("A Marina abre com 3 cabanas e desenha para 5. Para quantas unidades ela dimensiona a rede?", ["Para 3, e amplia depois", "Para 5, e paga agora a vala e o duto", "Para 4, no meio"],
         "B. A rede se dimensiona para o projeto completo e se constrói uma vez. Na fase dois, só se puxa o cabo pelo duto vazio."))
add(aplic("desenhe no masterplan o caminho da energia, da água e do esgoto até a unidade mais distante, e ligue para a concessionária.",
          "descubra qual sistema limita a próxima unidade (energia, água, esgoto ou acesso) e orce o reforço da rede existente."))
add(levar(["Parte 1: só o que aprova projeto e obra.", "A licença de operar vai para a Parte 6.", "Parte 2: distância e capacidade.", "Rede para o projeto completo, construída uma vez.", "Luz e água de cada unidade moram na Parte 2."]))
fim()

# ---------------------------------------------------------------- 05
cap("05", "Parte 3", "Parte 3: <i>o metro quadrado inteiro</i>",
    "Área construída vezes o custo do metro quadrado cotado. Das unidades, dos decks e das áreas comuns que o Pilar 5 desenhou.",
    ["As áreas comuns custam, e a página 6 não tinha linha para elas.",
     "Somando toda a área da Parte 3 e multiplicando cada uma pelo m² da cotação.",
     "Para o custo por m² ter a área inteira por trás."],
    ["Área × m² cotado", "Estrutura pronta conta como unidade", "As áreas comuns custam", "A área total"],
    "A Parte 3 é a mais pesada, e também a mais fácil de conferir: cada linha é uma área multiplicada por um custo do metro quadrado que veio de uma proposta.")
add("<p>Se a unidade é uma estrutura pronta (bolha, domo, cabana pré-fabricada), ela conta como unidade aqui, na Parte 3, como no Pilar 6. Na Planilha 1 ela fica na aba FF&amp;E; o capítulo 11 mostra onde lançar. Na estrutura pronta, confirme por escrito se frete, fundação e montagem estão incluídos.</p>")
add("<h3>As áreas comuns custam</h3><p>No Pilar 5, a Marina desenhou um apoio de 30 m²: rouparia 12, depósito 6, lixo 4, copa e vestiário 8. E um deck leve na crista. Nada disso estava na página 6. Na 6A, cada um ganha a sua linha, com área e custo do m².</p>")
add(ex("A Parte 3 da Marina", tab_parte(2)
       + f'<p class="conf">Conferência: 3 × 38 × 2.800 = 319.200; 3 × 16 × 700 = 33.600; 30 × 2.200 = 66.000; 16 × 600 = 9.600; soma 428.400. Bate.</p>'
       f'<p class="conf">Área total da Parte 3: 3 × 38 + 3 × 16 + 30 + 16 = 114 + 48 + 30 + 16 = <b>{c.AREA} m²</b>. Bate. A cabana é construída, então frete e montagem de estrutura pronta não se aplicam.</p>'))
add(cita("Corte metros quadrados no projeto. Nunca corte a experiência dentro deles.", "Pilar 6 · Pré-viabilidade"))
add("<p>Se a conta apertar, o lugar de cortar é aqui, no desenho, antes da obra: metros quadrados. Não no mobiliário do fim, que é o que o hóspede toca e fotografa.</p>")
add(pare("O apoio de 30 m² da Marina entra em qual parte?", ["Parte 2, infraestrutura", "Parte 3, como área comum", "Fica fora, porque não recebe hóspede"],
         "B. Área construída é Parte 3, receba hóspede ou não. O que não se constrói não se orça; o que se constrói, se orça."))
add(aplic("liste as áreas do seu masterplan (unidades, decks e áreas comuns) com a metragem de cada uma e peça o custo do m² com a mesma especificação.",
          "a ampliação também tem área comum: lavanderia maior, depósito, vaga de serviço. Cada uma com a sua linha."))
add(levar(["Área × m² cotado, linha por linha.", "Estrutura pronta conta como unidade (Parte 3).", "Áreas comuns custam e têm linha.", "Corte metros no projeto, nunca a experiência."]))
fim()

# ---------------------------------------------------------------- 06
cap("06", "Partes 4 e 5", "Partes 4 e 5: <i>a unidade-modelo e um dia de operação</i>",
    "Primeiro uma unidade completa, item por item. Depois, tudo o que um dia de operação gasta, em cinco listas.",
    ["É aqui que o orçamento esquece o lençol, o extintor e o carrinho da camareira.",
     "Com a unidade-modelo multiplicada pelas unidades e com os três jogos por cama.",
     "Para cada item morar numa linha só."],
    ["A unidade-modelo", "Os três jogos por cama", "Um dia de operação em cinco listas", "Cada item numa linha só"],
    "A Parte 4 começa com uma unidade-modelo: tudo o que uma cabana precisa, item por item, com proposta. Ela se multiplica pelas unidades da fase. Os equipamentos gerais (apoio, lavanderia, áreas comuns) entram à parte, sem multiplicar.")
add(ex("A Parte 4 da Marina", tab_parte(3) + '<p class="conf">Conferência: unidade-modelo 5.200 + 7.400 + 1.900 + 4.300 + 2.600 + 1.800 = 23.200; × 3 = 69.600; + 2.400 do apoio = 72.000. Bate.</p>'))
add("<h3>Um dia de operação</h3><p>A Parte 5 responde a uma pergunta: o que um dia de operação gasta? Em cinco listas: enxoval e utensílios das unidades; governança e limpeza; recepção; manutenção; segurança. E as amenidades do primeiro mês.</p>"
    "<p>O enxoval segue a regra dos três jogos por cama: um na cama, um na lavanderia, um no estoque. Mesmo com lavanderia terceirizada, os três jogos continuam. E cada item mora numa linha só: se a loja da cama já trouxe o lençol na cotação do mobiliário, ele não entra de novo na Parte 5.</p>")
add(ex("A Parte 5 da Marina", tab_parte(4) + f'<p class="conf">Conferência: 3 × 1 × 3 × 780 = 7.020; 7.020 + 1.200 + 900 + 600 + 1.020 = 10.740. Bate. A recepção não se aplica: no Pilar 5, a Marina escreveu «nunca: recepção construída».</p>'))
add(f"<p>Uma conferência rápida: a Parte 5 dividida pela Parte 4 da Marina dá 10.740 ÷ 72.000 = {pct(c.OSE_FFE)}. A fonte cita a faixa de 10% a 15% como conferência (Volume A05 · Investimento, caps. 2 e 6). Não é preço nem regra fixa: abaixo dela, algo de um dia de operação pode ter ficado de fora; acima, o enxoval pode estar contado duas vezes.</p>")
add(pare("As prateleiras da rouparia do apoio entram em qual parte?", ["Parte 3, junto com o apoio", "Parte 4, equipamentos gerais", "Parte 5, suprimentos"],
         "B. É equipamento, não obra e não suprimento. Entra na Parte 4, sem multiplicar pelas unidades."))
add(aplic("monte a sua unidade-modelo item por item e conte as camas: camas × 3 jogos é o seu enxoval.",
          "conte o que você repõe por mês hoje: é a melhor fonte para a Parte 5 da unidade nova."))
add(levar(["Unidade-modelo × unidades; equipamentos gerais à parte.", "Três jogos por cama, sempre.", "Um dia de operação em cinco listas.", "Cada item numa linha só."]))
fim()

# ---------------------------------------------------------------- 07
cap("07", "Partes 6 e 7", "Parte 6 e Parte 7: <i>a abertura e o imprevisto</i>",
    "O que acontece antes do primeiro hóspede, e o dinheiro que existe para o que ninguém previu, com regra escrita.",
    ["A pré-abertura não estava na página 6, e a reserva tinha base pequena.",
     "Listando a pré-abertura e subindo a reserva quando a fonte pede.",
     "Para a reserva cobrir o imprevisto, e só o imprevisto."],
    ["Parte 6 · Pré-abertura", "Parte 7 · Reserva do imprevisto", "O que a reserva não cobre", "A regra de uso em quatro linhas"],
    "A obra termina e o hóspede ainda não chegou. Entre os dois existe uma lista: licença de funcionamento e cadastros, fotos e anúncio, identidade e lançamento, treinamento e manual de operação, seguro do primeiro ano e uma abertura de teste.")
add(ex("A Parte 6 da Marina", tab_parte(5) + '<p class="conf">Conferência: 4.800 + 3.500 + 2.500 + 1.800 = 12.600. Bate. Duas linhas em branco: a licença de funcionamento e o seguro.</p>'))
add(cita("A contingência não é pessimismo. É maturidade.", "Volume A05 · Investimento, cap. 7"))
add("<h3>Parte 7 · A reserva do imprevisto</h3><p>A faixa citada pela fonte é de 10% a 15% sobre o subtotal das Partes 1 a 6, no teto ou acima com fator de risco ou na primeira obra. Fatores de risco: território remoto, sistema construtivo novo para a equipe, itens importados, licenciamento em área sensível, prazo apertado pela temporada.</p>"
    "<p>A reserva cobre o imprevisto da obra orçada: solo, chuva, reajuste, exigência da licença. Não cobre escopo novo, linha esquecida nem o caixa dos primeiros meses, que é giro. E ela tem regra de uso escrita, em quatro linhas: para quê, quem autoriza, como se registra e quando se confere.</p>")
add(ex("A reserva da Marina", f"<p>Ela começa com os 10% da página 6: 0,10 × 687.940 = R$ 68.794. A ficha acende o alerta: <b>primeira obra abaixo de 15%</b>. A própria página 6 dela já anotava: «se as cotações vierem com muita incerteza, subir para o teto da faixa». Ela sobe para 15%.</p>"
       f"<p>0,15 × 687.940 = <b>{brl(c.RES)}</b>. Conferência: 10% = 68.794; metade disso = 34.397; 68.794 + 34.397 = 103.191. Bate.</p>"
       "<p><b>A regra de uso:</b> para quê · imprevisto da obra orçada (solo, chuva, reajuste, exigência da licença); quem autoriza · a Marina, depois de ouvir o engenheiro; como se registra · planilha com data, motivo e valor; quando se confere · a cada medição da obra.</p>"))
add(pare("No meio da obra, a Marina quer um ofurô na crista. Sai da reserva do imprevisto?", ["Sim, é para isso que ela existe", "Não: escopo novo é decisão e vira linha nova"],
         "B. O ofurô não é imprevisto da obra orçada: é escopo novo. Vira linha nova, com cotação, e decisão escrita (Pilar 6). A reserva que sobra no fim da obra pode virar giro."))
add(aplic("conte os seus fatores de risco; com um deles, ou na primeira obra, parta do teto da faixa.",
          "use o histórico da última obra: quanto o imprevisto custou de verdade, sobre o orçado?"))
add(faca("A minha regra de uso da reserva", [("Para quê:", False), ("Quem autoriza:", False), ("Como se registra:", False), ("Quando se confere:", False)]))
add(levar(["A pré-abertura ganha linha própria.", "Reserva de 10% a 15% do subtotal; primeira obra no teto.", "Reserva cobre o imprevisto, não escopo novo.", "Regra de uso em quatro linhas."]))
fim()

# ---------------------------------------------------------------- 08
cap("08", "A leitura", "Ler o número <i>antes de mostrá-lo</i>",
    "O peso de cada parte, o custo por unidade e por m², as faixas de conferência e o limite da página 6.",
    ["Um total sozinho não mostra o que falta. As proporções mostram.",
     "Com as medidas da 6A e as faixas citadas pelas fontes, que não são preço.",
     "Para você encontrar o erro antes de quem vai ler a sua conta."],
    ["O peso de cada parte", "Por unidade e por m²", "As faixas de conferência", "Página 6 × 6A e o limite"],
    "Com as sete partes somadas, a conta tem um total. Antes de mostrá-lo a alguém, leia as proporções: elas contam o que o total esconde.")
add("<h3>As medidas</h3>")
add(tab(["Medida", "Como se calcula", "Para que serve"], [
    ["Peso de cada parte", "Total da parte ÷ CAPEX da fase", "Ver onde está o dinheiro e o que parece pequeno demais"],
    ["Custo por unidade", "CAPEX ÷ unidades da fase (sem giro e sem terreno)", "Comparar tipologias e fases"],
    ["Investimento por unidade", "Investimento total ÷ unidades (com o giro)", "É o «custo por chave» da ficha do Pilar 6"],
    ["Custo por m²", "CAPEX ÷ área total da Parte 3", "Conferir com o m² das cotações"],
    ["Página 6 × 6A", "Total da página 6 ÷ investimento total da 6A", "Ver quanto a página 6 cobria, sem julgamento"],
    ["Folga até o limite", "Limite da página 6 − investimento total", "Saber se a conta ainda cabe"]], larg=("24%", "40%", "36%")))
add("<h3>As faixas de conferência</h3><p>As fontes citam algumas faixas para conferir a conta. Elas não são preço nem regra fixa: são faixas de sanidade (Volume A05 · Investimento, cap. 3). Projeto pequeno pode cair fora delas, e tudo bem, desde que você saiba explicar por quê.</p>")
add(tab(["Leitura", "Faixa citada", "Se cair fora"], [
    ["Reserva do imprevisto", "10% a 15% do subtotal; teto ou acima na primeira obra", "Abaixo: subir; acima de 25%: escopo escondido?"],
    ["Parte 5 ÷ Parte 4", "10% a 15%", "Abaixo: faltou algo; acima: enxoval duas vezes?"],
    ["Pré-abertura ÷ obra (Partes 2 + 3)", "5% a 10%", "Abaixo de 5%: um dos cinco erros"],
    ["Obra ÷ CAPEX", "60% a 70%; acima de 80% = alerta", "Acima de 80%: provavelmente faltou algo"],
    ["Linhas com cotação", "Maioria (mais de 50%)", "Até 50%: a maior parte ainda é estimativa ou branco"]], larg=("30%", "36%", "34%"), leg="Faixa de conferência citada pela fonte; não é preço nem regra fixa"))
add("<h3>O degrau do número</h3><p>A régua do Pilar 6 continua valendo: <b>Sonhador</b> (só a unidade tem valor), <b>Estimador</b> (a conta inteira existe, mas a maioria das linhas ainda não tem cotação), <b>Calculista</b> (a maioria das linhas tem cotação escrita e as três maiores linhas estão cotadas). <b>Developer</b> pede cronograma de desembolso e captação, e fica para o Pilar 7.</p>")
add("<h3>Página 6 × 6A e o limite</h3><p>A comparação com a página 6 é um número, não um julgamento: «a sua página 6 cobria X% da 6A; a diferença é de R$ Y». A explicação é de escopo: a referência era de uma unidade pronta genérica; a cotação é da unidade do seu projeto, com a rede comum e as áreas comuns orçadas à parte. Depois vem o limite: se o investimento total couber, a folga diz quanto ainda cabe de linhas novas; se passar, a conta volta à mesa antes de assinar.</p>")
add(pare("A obra da Marina pesa 70,4% do CAPEX, acima dos 60% a 70% citados. O que isso quer dizer?", ["Que ela errou a conta", "Nada definitivo: é comum em projeto pequeno; o alerta é acima de 80%", "Que a obra está cara"],
         "B. É uma faixa de conferência, não regra. Em projeto pequeno a obra pesa mais. O sinal de alerta é passar de 80%."))
add(levar(["Leia as proporções antes do total.", "Custo por unidade (sem giro) e investimento por unidade (com giro).", "Faixas de conferência não são preço.", "Página 6 × 6A: número, não julgamento.", "O limite da página 6 decide se a conta ainda cabe."]))
fim()

# ---------------------------------------------------------------- 09
cap("09", "Exemplo resolvido", "A conta da Marina, <i>inteira</i>",
    "As sete partes somadas, a reserva, o giro da página 6, o investimento total e o limite. Com as conferências.",
    ["Ver a conta inteira montada ensina mais do que qualquer regra solta.",
     "Somando o que os capítulos 04 a 07 abriram e lendo o resultado com as medidas do capítulo 08.",
     "Para você ter um modelo para a sua página 6A."],
    ["As premissas", "A conta", "As medidas e as cotações", "Página 6 × 6A", "O limite e a ação"],
    "A Marina tem a página 6 na mão, as cotações que pediu desde o Pilar 5 e as linhas que ainda não têm número. Hoje, no exemplo, é 27 de novembro de 2026.")
add(ex("As premissas", "<ul><li>Situação: «Tenho um terreno e ainda não hospedo ninguém»; cabanas; imóvel novo; primeira obra; nenhum fator de risco marcado.</li>"
       f"<li>Página 6: investimento total {brl(c.P6_TOTAL, 2)}; infraestrutura comum «à parte, a cotar»; limite {brl(c.LIMITE6, 2)}.</li>"
       f"<li>Fase um: {c.UN_FASE} cabanas; projeto completo: {c.UN_PROJ}. Energia a {c.DIST_ENERGIA_M} m; rede dimensionada para {c.REDE_PARA}.</li>"
       "<li>Ponto de partida no diagnóstico: <b>Estimador</b> (referência, nada cotado, sem regra de reserva).</li></ul>"))
rows = []
for i in range(6):
    cp = c.CONT_P[i]
    rows.append([f"{i + 1} · {c.NOMES_PARTES[i]}", num(c.TOT[i]), pct(c.PESOS[i]), num(c.COTADO_P[i]), num(c.ESTIM_P[i]), f"{cp[0]} / {cp[1]} / {cp[2]} / {cp[3]}"])
rows += [["!Subtotal (Partes 1 a 6)", num(c.SUB), "", num(c.COTADO), num(c.ESTIM), f"{c.NC} / {c.NE} / {c.NB} / {c.NNA}"],
         ["7 · Reserva do imprevisto (15%)", num(c.RES), pct(c.PESOS[6]), "", "", ""],
         ["!CAPEX da fase", num(c.CAPEX), "100,1%*", "", "", ""],
         ["Capital de giro (veio da página 6)", num(c.GIRO, 2), "", "", "", ""],
         ["!Investimento total da fase um", num(c.INVEST, 2), "", "", "", ""],
         ["Limite da página 6", num(c.LIMITE6, 2), "", "", "", ""],
         ["!Folga", num(c.FOLGA, 2), "dentro", "", "", ""],
         ["~À parte · terreno (já é dela)", num(c.TERRENO), "não somado", "", "", ""]]
add(ex("A 6A da Marina", tab(["Parte", "Total R$", "Peso", "Cotado R$", "Estimado R$", "C / E / B / NA"], rows, v=(1, 2, 3, 4), larg=("33%", "14%", "10%", "14%", "14%", "15%"))
       + '<p class="nota">* A soma dos pesos arredondados dá 100,1%; sem arredondar, dá 100%. C = cotação, E = estimativa, B = em branco, NA = não se aplica.</p>'))
add('<div class="bx"><span class="k">Conferência dupla</span>'
    "<p>Por partes: 36.000 + 128.200 + 428.400 + 72.000 + 10.740 + 12.600 = 687.940. Por origem: 613.120 cotado + 74.820 estimado = 687.940. Bate.</p>"
    "<p>CAPEX: 687.940 + 103.191 = 791.131, e 687.940 × 1,15 = 791.131. Investimento total: 791.131 + 40.787,38 = 831.918,38. Folga: 870.130,80 − 831.918,38 = 38.212,42; e 831.918,38 + 38.212,42 = 870.130,80. Bate.</p></div>")
add("<h3>As medidas</h3>")
add(tab(["Medida", "Conta", "Resultado"], [
    ["Custo por unidade (sem giro e sem terreno)", "791.131 ÷ 3", brl(c.CUSTO_UN, 2)],
    ["Investimento por unidade (o «custo por chave»)", "831.918,38 ÷ 3", brl(c.INVEST_UN, 2) + f" (na página 6: {brl(c.P6_INVEST_UN, 2)})"],
    ["Custo por m²", f"791.131 ÷ {c.AREA} m²", brl(c.CUSTO_M2, 2)],
    ["Obra ÷ CAPEX", "556.600 ÷ 791.131", pct(c.PCT_OBRA) + " · menos de 80%, sem alerta"],
    ["Parte 5 ÷ Parte 4", "10.740 ÷ 72.000", pct(c.OSE_FFE) + " · dentro da faixa"],
    ["Pré-abertura ÷ obra", "12.600 ÷ 556.600", pct(c.PRE_OBRA) + f" · abaixo de 5%: faltam {brl(c.FALTA_PRE)}"]], v=(2,), larg=("40%", "25%", "35%")))
add(f"<p><b>Linhas e cotações.</b> São {c.N} linhas contadas (a recepção, que não se aplica, fica fora): {c.NC} com cotação, {c.NE} estimativas e {c.NB} em branco. As linhas cotadas são {pct(c.PCT_LINHAS)} do total, mas o valor cotado é {pct(c.PCT_VALOR)} do subtotal (613.120 ÷ 687.940), porque as três maiores linhas (cabanas, apoio e decks) têm cotação. Como as linhas cotadas ainda não são a maioria, o degrau continua <b>Estimador</b>. Faltam {c.FALTAM_MAIORIA} linhas cotadas para a maioria (20 ÷ 39 = 51,3%).</p>"
    f"<p>Cotações completas, com três propostas iguais: {c.N3}. Incompletas: {c.NINC} (energia e apoio com uma proposta; complementares, estacionamento, caminho, água, decks, mobiliário e fotos com duas). Vencida: 1, a água, com 135 dias.</p>")
add(ex("Da página 6 para a 6A", f"<p>A página 6 cobria 690.529,18 ÷ 831.918,38 = <b>{pct(c.P6_COBRE)}</b> da 6A; a diferença é de <b>{brl(c.DIF_P6, 2)}</b>. De onde ela vem:</p>"
       + tab(["O que mudou", "Página 6", "Página 6A", "Diferença"], [
           ["Entrou o que estava à parte ou não estava (infraestrutura comum 118.000; áreas comuns 75.600; equipamentos do apoio 2.400; pré-abertura 12.600)", "0", "208.600", "+ 208.600"],
           ["Licenças e projetos", "15.000", "36.000", "+ 21.000"],
           ["Reserva do imprevisto (base e percentual novos)", "57.703,80", "103.191,00", "+ 45.487,20"],
           ["As seis linhas por cabana, agora com cotação e estimativa (a rede comum foi para a Parte 2)", "577.038", "443.340", "− 133.698"],
           ["Capital de giro", "40.787,38", "40.787,38", "0"],
           ["!Total", "690.529,18", "831.918,38", "+ 141.389,20"]], v=(1, 2, 3), larg=("49%", "17%", "17%", "17%"))
       + '<p class="conf">Conferência: 208.600 + 21.000 + 45.487,20 − 133.698 = 141.389,20; 690.529,18 + 141.389,20 = 831.918,38. Bate.</p>'
       "<p>A leitura é de escopo, não de preço: a referência da página 6 era de uma unidade pronta genérica; a cotação é da cabana do projeto dela, com a rede comum e as áreas comuns orçadas à parte, nas Partes 2 e 3.</p>"))
add("<h3>O limite</h3>")
add(ex("Cabe, mas a folga é fina", f"<p>O investimento total de {brl(c.INVEST, 2)} fica dentro do limite de {brl(c.LIMITE6, 2)}, com folga de <b>{brl(c.FOLGA, 2)}</b>, cerca de 4,8% do CAPEX.</p>"
       f"<p>Já com a reserva de 15%, a folga paga {brl(c.FOLGA_SUB, 2)} de linhas novas (38.212,42 ÷ 1,15). Desse valor, R$ 15.230 vão para a pré-abertura chegar aos 5% da obra, e sobram <b>{brl(c.SOBRA_BRANCO, 2)}</b> para as cinco linhas em branco: licença ambiental, internet, segurança, licença de funcionamento e seguro do primeiro ano.</p>"
       '<p class="conf">Conferência: 33.228,19 × 1,15 = 38.212,42; 33.228,19 − 15.230 = 17.998,19. Bate.</p>'
       "<p>Cabe, mas a folga é fina, e as linhas em branco só podem aumentar a conta. A decisão do Pilar 7, avançar com a fase um de três cabanas, continua de pé.</p>"))
add(f"<p><b>Os três alertas da ficha, na ordem:</b> pré-abertura abaixo da faixa citada (2,3% da obra; faltam cerca de R$ 15.230 para os 5%); cotação com mais de 90 dias (a água, com 135 dias); {c.NINC} linhas com menos de três cotações iguais. Não disparam: limite, partes em branco, reserva, rede e obra acima de 80%.</p>")
add(bx("A ação de 30 dias", "", "<p><b>Ação:</b> pedir cotação escrita da licença ambiental, da internet, da segurança, da licença de funcionamento e do seguro do primeiro ano. <b>Prazo:</b> 27/12/2026. <b>Como verificar:</b> as cinco propostas, com data e escopo, lançadas na ficha.</p>"
       "<p>Com elas, ficam 21 linhas cotadas em 39 (53,8%) e a Marina chega a <b>Calculista</b>.</p>", "faca"))
fim()

# ---------------------------------------------------------------- 10
cap("10", "Exercícios", "Pratique <i>com a Marina</i>",
    "Do resolvido ao em branco: um exercício parcialmente resolvido, uma classificação, a base da reserva e a sua Parte 2.",
    ["Fazer a conta com a mão é o que fixa o método.",
     "Com quatro exercícios sobre os números da Marina e o gabarito comentado no fim.",
     "Para você chegar à ficha já sabendo onde cada linha mora."],
    ["E2 · A água refeita", "E3 · Onde mora cada gasto", "E4 · A base da reserva", "E5 · A sua Parte 2", "Gabarito comentado"],
    "O exercício 1 você já viu: a conta inteira da Marina, no capítulo 09. Agora é a sua vez, com os mesmos números, rotulados como exemplo ilustrativo.")
add(ex("E2 · A cotação da água foi refeita", "<p>A cotação da água (19.800, de 15/07/2026) venceu. A nova, com a mesma especificação, chega a <b>R$ 22.400</b>. Calcule: a nova Parte 2; o novo subtotal; a reserva a 15%; o CAPEX; o investimento total; a folga até o limite; e qual alerta some.</p>"
       "<p>Já resolvido para você: a Parte 2 passa a 128.200 − 19.800 + 22.400 = <b>R$ 130.800</b>. O resto é com você.</p><div class=\"campo alto\"></div>"))
add(bx("E3 · Onde mora cada gasto", "", "<p>Para cada item, escreva a parte (1 a 7), «ao lado», «à parte» ou «fora desta conta»:</p>"
       "<p>jogo de lençol e toalhas · colchão · projeto elétrico · poço · licença de funcionamento · fotos do anúncio · deck de cada cabana · prateleiras da rouparia do apoio · bolha ou cabana pronta · terreno · capital de giro · ofurô na crista decidido no meio da obra · juros do empréstimo da obra</p><div class=\"campo alto\"></div>", "faca"))
add(ex("E4 · A base da reserva", "<p>Quanto a reserva da Marina muda só por trocar a base e o percentual? Calcule: 10% das seis linhas por cabana (443.340), como na base simplificada do Pilar 6; 10% do subtotal das Partes 1 a 6; 15% do subtotal; a diferença entre 10% e 15% do subtotal; qual alerta aparece a 10%. Depois escreva a regra de uso em quatro linhas.</p><div class=\"campo alto\"></div>"))
add(faca("E5 · A sua Parte 2, em branco", [("As linhas da minha Parte 2 (acesso, estacionamento, caminhos, energia, água, esgoto, drenagem, internet, ligações de cada unidade):", True), ("A quem eu peço cada cotação:", True)],
         nota="É a ponte para a ficha: estas linhas entram na tela da Parte 2."))
add("<h3>Gabarito comentado</h3>")
add(tab(["E2", "Conta", "Resposta"], [
    ["Parte 2", "128.200 − 19.800 + 22.400", "R$ 130.800"],
    ["Subtotal", "687.940 + 2.600", "R$ 690.540"],
    ["Reserva a 15%", "0,15 × 690.540", "R$ 103.581"],
    ["CAPEX", "690.540 + 103.581", "R$ 794.121"],
    ["Investimento total", "794.121 + 40.787,38", "R$ 834.908,38"],
    ["Folga", "870.130,80 − 834.908,38", "R$ 35.222,42"],
    ["Alerta que some", "não há mais cotação vencida", "Cotação com mais de 90 dias"]], v=(2,), larg=("24%", "44%", "32%"),
    leg="Conferência: 791.131 + 2.600 × 1,15 = 791.131 + 2.990 = 794.121. Bate. Repare: R$ 2.600 a mais na cotação custam R$ 2.990 na folga, porque a reserva acompanha."))
add(tab(["E3 · Item", "Onde mora", "Por quê"], [
    ["Jogo de lençol e toalhas", "Parte 5", "Enxoval, três jogos por cama"],
    ["Colchão", "Parte 4", "Unidade-modelo"],
    ["Projeto elétrico", "Parte 1", "Aprova o projeto e a obra"],
    ["Poço", "Parte 2", "Leva a água até o terreno"],
    ["Licença de funcionamento", "Parte 6", "Autoriza operar, não construir"],
    ["Fotos do anúncio", "Parte 6", "Acontece antes do primeiro hóspede"],
    ["Deck de cada cabana", "Parte 3", "Área construída"],
    ["Prateleiras da rouparia", "Parte 4", "Equipamento geral, sem multiplicar"],
    ["Bolha ou cabana pronta", "Parte 3", "Conta como unidade (na Planilha 1, aba FF&amp;E)"],
    ["Terreno", "À parte, não somado", "Fora da conta, mas não de graça"],
    ["Capital de giro", "Ao lado, somado", "Entra no investimento total"],
    ["Ofurô na crista, no meio da obra", "Linha nova e decisão", "Escopo novo não sai da reserva (Pilar 6)"],
    ["Juros do empréstimo da obra", "Fora desta conta", "Custo da captação: Pilar 7"]], larg=("36%", "24%", "40%")))
add(tab(["E4", "Conta", "Resposta"], [
    ["10% das seis linhas (Pilar 6)", "0,10 × 443.340", "R$ 44.334"],
    ["10% do subtotal", "0,10 × 687.940", "R$ 68.794"],
    ["15% do subtotal (primeira obra)", "0,15 × 687.940", "R$ 103.191"],
    ["Diferença entre 10% e 15%", "103.191 − 68.794", "R$ 34.397"],
    ["Alerta a 10%", "primeira obra abaixo de 15%", "Subir para o teto"]], v=(2,), larg=("36%", "36%", "28%"),
    leg="A regra de uso é sua: para quê, quem autoriza, como se registra, quando se confere. Compare com a da Marina no capítulo 07."))
fim()

# ---------------------------------------------------------------- 11
cap("11", "A sua página do Dossiê", "A página 6A <i>e a volta</i>",
    "A 6A não termina nela mesma. Ela volta para a página 6, campo a campo, e segue a ordem do Mapa.",
    ["Uma conta que não volta para a página 6 fica solta, e o Pilar 7 lê a página 6.",
     "Com a ficha, o quadro «Como levar para a página 6» e o resumo «Se você usa a Planilha 1».",
     "Para você refazer a página 6 com números cotados e seguir para o Pilar 7."],
    ["A ficha «Faça agora · O seu CAPEX»", "Como levar para a página 6", "Se você usa a Planilha 1", "Planilha 2 e sensibilidade", "Perguntas, no checklist"],
    "Tudo o que você fez neste e-book vira uma página: a Página 6A · CAPEX, irmã da página 6. A ficha «Faça agora · O seu CAPEX» faz as contas, lê a sua página 6 do aparelho e baixa o PDF.")
add("<p>Na plataforma do curso, abra a aula «Faça agora · O seu CAPEX». A primeira tela traz a sua situação, com as palavras do Marco Zero. A segunda lê a sua página 6: o investimento total, a data e o limite, com a frase «veio da página 6». Depois, as Partes 1 a 7, o giro e o terreno, o resultado e a ação de 30 dias. Esta ficha não envia nada: o PDF fica só com você. Salve o PDF da página 6A na pasta Meu Dossiê, ao lado da página 6.</p>")
add("<h3>Como levar para a página 6</h3><p>A ficha do Pilar 6 tem oito linhas e um campo de infraestrutura comum. O quadro abaixo diz o que digitar em cada campo. A ficha do Pilar 6 não tem linha própria para áreas comuns, equipamentos gerais, pré-abertura e a parte da reserva que não é unidade: tudo isso vai no campo «infraestrutura comum», com nota escrita.</p>")
add(ex("O quadro da Marina", tab(["Campo da ficha do Pilar 6", "Valor", "Nota", "Conta"], [
    ["Unidades", "3", "", ""],
    ["1 · A unidade", "106.400", "3", "319.200 ÷ 3"],
    ["2 · Deck", "11.200", "3", "33.600 ÷ 3"],
    ["3 · Luz", "1.800", "1", "5.400 ÷ 3"],
    ["4 · Água e esgoto", "1.600", "1", "4.800 ÷ 3"],
    ["5 · Mobiliário, equipamentos e enxoval", "26.780", "1", "(69.600 + 10.740) ÷ 3"],
    ["6 · Piso interno", "0, digitado", "", "incluído no m²"],
    ["~Unidade pronta (a ficha calcula)", "147.780", "", "soma das seis"],
    ["7 · Licenças e projetos", "36.000", "1", "Parte 1"],
    ["8 · Reserva do imprevisto", "15%", "", ""],
    ["À parte · Infraestrutura comum", "245.290", "1", "208.600 + 36.690"],
    ["Capital de giro (meses)", "3", "", "não muda"],
    ["Terreno", "600.000", "", "não muda"]], v=(1,), larg=("40%", "18%", "10%", "32%"))
    + '<p class="conf">Conferência: 3 × 147.780 = 443.340; × 1,15 = 509.841; + 36.000 = 545.841; + 245.290 = 791.131 = CAPEX. Bate.</p>'
    "<p><b>Digite 0 onde for zero.</b> Em branco, a ficha do Pilar 6 usa a referência da Zion no lugar.</p>"))
add(f"<p>A página 6 refeita da Marina vai mostrar o investimento total de {brl(c.INVEST, 2)}, o custo por chave de {brl(c.INVEST_UN, 2)} e um tempo de volta no conservador de 831.918,38 ÷ 108.766,35 = 7,65 anos, dentro da régua de 8. Com o terreno somado, cerca de 13 anos: a razão escrita dela no Dossiê passa de «perto de doze» para «cerca de treze», e continua valendo, porque a razão existe.</p>")
add("<h3>Se você usa a Planilha 1</h3><p>A Planilha 1 · Orçamento de Abertura é o caminho do curso para quem prefere planilha. As partes da 6A cabem nas abas dela assim:</p>")
add(tab(["Aba da Planilha 1", "Partes da 6A", "Marina (R$)"], [
    ["Premissas, linha 11 (B11 = 3; C11 = 38; D11 = 16; E11 = 2.800; F11 = 700)", "Unidades construídas e decks da Parte 3", "352.800"],
    ["Infraestrutura (grupos 1 a 7; pré-abertura nas linhas livres do grupo 9)", "Parte 1 + Parte 2 + áreas comuns da Parte 3 + Parte 6", "252.400"],
    ["FF&amp;E (zerar «estrutura principal» e «base ou deck» se a unidade é construída)", "Unidade-modelo da Parte 4; estrutura pronta, se houver", "69.600"],
    ["OS&amp;E", "Parte 5 + equipamentos gerais da Parte 4", "13.140"],
    ["!Resumo · Subtotal (B10)", "", "687.940"],
    ["Premissas B15 · contingência", "Parte 7 (15%)", "103.191"],
    ["!Resumo · TOTAL (B12)", "= CAPEX da 6A", "791.131"]], v=(2,), larg=("46%", "36%", "18%"),
    leg="Conferência: 352.800 + 252.400 + 69.600 + 13.140 = 687.940. Bate. A Planilha 1 divide o CAPEX só pela área das unidades (162 m², R$ 4.883,52 por m²); a 6A divide pela área total da Parte 3 (208 m², R$ 3.803,51). Os dois estão certos: diga qual usou."))
add("<h3>A ordem do Mapa</h3><ol>"
    "<li><b>Salve</b> o PDF da página 6A na pasta Meu Dossiê, ao lado da página 6.</li>"
    "<li><b>Refaça a página 6</b> na ficha do Pilar 6, campo a campo, com o quadro acima, digitando 0 onde for zero.</li>"
    "<li><b>Planilha 1 · Orçamento de Abertura</b> (se preferir planilha): lance pelo quadro acima e confira se o Resumo, linha TOTAL, bate com o CAPEX.</li>"
    "<li><b>Planilha 2 · Estudo de Massas e Viabilidade, aba Investimento:</b> cole o CAPEX da fase na célula B5, deixe o terreno em zero na B6 (para mantê-lo fora da conta, como na 6A) e confira se o giro da B9 bate com o da 6A. Se não bater, a Planilha 2 usa meses × custo fixo e o Pilar 6 usa meses × custo do conservador: anote os dois e fique com o maior.</li>"
    "<li><b>Sensibilidade do Mapa</b> (diária −15%, ocupação −10 pontos, CAPEX +20%) e volte à ficha para refazer a página 6.</li>"
    "<li><b>Pilar 7:</b> a necessidade de capital, o custo da captação e o pedido. O plano de 90 dias: «Dias 61 a 90 · Decidir: refaz a página 6 com os números cotados».</li></ol>")
add(bx("Atenção", "No Pilar 7, o número da Marina é o de antes", "<p>No Pilar 7 você vai ver a Marina com o número da página 6 de referência, cerca de R$ 690 mil, porque ele foi escrito antes das cotações. Com a 6A, o investimento dela passa a ser cerca de R$ 832 mil, e o critério de R$ 870 mil continua de pé. O teste «CAPEX +20%» é a próxima etapa do Mapa, com a reserva de 15% já dentro do CAPEX; a decisão é do Pilar 7.</p>", "crit"))
add("<h3>O que perguntar, sem número</h3><p>As perguntas ao engenheiro (o que o preço inclui, frete e montagem, reajuste, para quantas unidades a rede é dimensionada, quem assina a responsabilidade técnica), ao contador (custos de aquisição do terreno, impostos da obra e dos equipamentos, a forma de entrada do terreno), à concessionária e à prefeitura (ponto de energia, licenças) estão no <b>Checklist da página 6A</b>, que acompanha este e-book. Nenhuma delas pede número: quem traz o número é a proposta.</p>")
fim()

# ---------------------------------------------------------------- Confira o que ficou
add('<section class="cap"><div class="cab"><div class="k">Revisão, resumo e Faça agora</div><span class="n">' + CHK.replace('.8em', '.75em') + '</span>'
    '<h2>Confira o que <i>ficou</i></h2><p class="deck">Responda de cabeça, sem voltar às páginas. Depois leia o resumo e preencha a sua página.</p></div><div class="regua"></div>')
add("<h3>Perguntas de revisão</h3>")
PP = [("1. O que é o CAPEX da fase?", ["O preço da unidade", "A soma das sete partes: o custo de abrir a porta", "O CAPEX mais o giro"], "B. CAPEX + giro é o investimento total da fase um."),
      ("2. A infraestrutura comum, que estava à parte na página 6, vai para onde?", ["Continua à parte", "Parte 2 (rede, acesso, caminhos) e Parte 3 (apoio e áreas comuns)", "Parte 7"], "B. Na 6A ela entra na conta."),
      ("3. Uma linha sem número na 6A…", ["Recebe a referência da Zion", "Fica em branco, com nome, e conta como risco", "Some da conta"], "B. Uma linha em branco vale mais do que um número inventado (Pilar 6)."),
      ("4. Sobre o que se calcula a reserva na 6A?", ["Sobre as unidades prontas", "Sobre o subtotal das Partes 1 a 6", "Sobre o investimento total"], "B. E na primeira obra, no teto da faixa ou acima."),
      ("5. Uma cotação de 135 dias…", ["Vale, se o fornecedor for bom", "Precisa ser refeita: passou de 90 dias", "Vale até o fim do ano"], "B. Cotação de mais de noventa dias precisa ser refeita (Volume 05 · Investimento)."),
      ("6. A conta da Marina cabe no limite da página 6?", ["Não, passou", "Sim, com folga de R$ 38.212,42, que ainda precisa pagar as linhas em branco", "Sim, com folga de R$ 179.601,62"], "B. A folga de R$ 179.601,62 era a da página 6, antes da infraestrutura comum e das cotações.")]
add("".join(pare(p, o, r) for p, o, r in PP))
add(bx("Resumo", "O 6A em dez linhas", '<ol class="dez">'
       "<li>A 6A é a página irmã da página 6: abre o custo de abrir a porta, linha por linha.</li>"
       "<li>Sete partes somadas = CAPEX da fase; com o giro, investimento total da fase um.</li>"
       "<li>O terreno fica ao lado, não somado: fora da conta não quer dizer de graça.</li>"
       "<li>A infraestrutura comum entra; a pré-abertura ganha linha.</li>"
       "<li>Cada número tem origem: cotação, estimativa ou em branco. A referência não entra.</li>"
       "<li>Três cotações com a mesma especificação e o «não inclui» por escrito; mais de 90 dias, refaça.</li>"
       "<li>A rede se dimensiona para o projeto completo e se constrói uma vez.</li>"
       "<li>Reserva de 10% a 15% do subtotal, no teto na primeira obra, com regra de uso em quatro linhas.</li>"
       "<li>Faixas de conferência não são preço; o limite da página 6 decide se a conta cabe.</li>"
       "<li>A 6A volta para a página 6, campo a campo, e segue para a Planilha 1, a Planilha 2 e o Pilar 7.</li></ol>", "levar"))
add(faca("A minha página 6A", [("As sete partes, com valor e quantas linhas têm cotação:", True), ("O CAPEX da fase, o giro e o investimento total:", False),
                                ("O limite da minha página 6 e a folga (ou o excesso):", False), ("As linhas em branco, pelo nome:", False),
                                ("A minha ação de 30 dias, o prazo e como verificar:", False)],
         nota="Depois de preencher, abra na plataforma do curso a aula «Faça agora · O seu CAPEX» e passe as respostas para a ficha. Ela gera a página 6A do seu Dossiê em PDF."))
add("<h3>Fontes deste e-book</h3><p style=\"font-size:8pt\">Pilar 6 · Pré-viabilidade (e-book e ficha: a folha de oito linhas, o limite, as frases-assinatura); Pilar 5 · Masterplan faseado (fase um, apoio, rede para 5); Pilar 7 · Capital e Dossiê (o critério e o plano de 90 dias); Marco Zero e Comece aqui (as situações e a pasta Meu Dossiê); Volume A05 · Investimento (caps. 1, 2, 3, 4, 6 e 7); Volume 05 · Investimento (cap. 4); Jornada do COMO (Etapa 02, Passo 11; Etapa 04, Passos 01, 04 e 09); Planilhas 1 e 2 da Trilha 1; Mapa de direcionamento, etapa 6. As faixas de conferência são citadas pelas fontes e não têm base estatística declarada. A régua de linhas cotadas (cortes em 0 e 50%), a transposição para a página 6 e o mapa para as abas da Planilha 1 são elaboração própria da Zion.</p>")
add(f'<p class="fim">{AVISO} A Marina é um exemplo ilustrativo: os números novos são fictícios e não são preços de referência; os da página 6 dela são a referência orientativa do Pilar 6, não confirmada (a Zion também vende esse tipo de estrutura). Este material não promete aprovação, crédito, parceria, retorno, ocupação nem prazo de obra. © Zion Hotel Group International.</p></section>')

# ---------------------------------------------------------------- saída
html = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>E-book Aprofundamento 6A · CAPEX</title>'
        f"<style>{css(OUT)}</style></head><body>" + "\n".join(H) + "</body></html>")
texto = re.sub(r"<[^>]+>", " ", html.split("<body>")[1])
assert "—" not in texto and "–" not in texto, "travessão no texto"
for proibido in ("Helena", "Ribeirão", "Rodrigo", "Priscila", "Bloco 1", "Bloco 2", "palpite", "aluno", "membro", "payback", "Ferramenta 05", "Calculadora de Implantação"):
    assert proibido not in texto, f"termo proibido no e-book: {proibido}"
(OUT / "ebook.html").write_text(html, encoding="utf-8")
print("ebook.html", len(html) // 1024, "KB")

"""Gera o HTML do e-book "CAPEX · Aprenda o passo a passo para calcular quanto custa o seu projeto inteiro".
Saída: src/ebook/ebook.html. Depois: node src/render.js src/ebook/ebook.html docs/trilha1/materiais/CAPEX-Aprenda-o-passo-a-passo-ebook.pdf
Uso: python3 -I src/build_ebook.py   (a partir da pasta da lição ou de qualquer lugar)
Fontes: PLANO.md (seções 5.1, 5.3 e 7) e o mapa de fontes da lição. Números só do caso fictício."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from estilo import css, rel, BRAND, RODAPE
import caso as c

OUT = pathlib.Path(__file__).resolve().parent / "ebook"; OUT.mkdir(exist_ok=True)
brl, pct = c.brl, c.pct
FICT = '<span class="fict">Exemplo com dados fictícios. Não são preços de referência.</span>'
paginas = []


def pg(corpo, classe=""):
    paginas.append((corpo, classe))


def cab(num, kicker, titulo, lead=""):
    return (f'<div class="cab"><div class="k">{kicker}</div><span class="n">{num}</span><h2>{titulo}</h2></div>'
            + (f'<p class="lead">{lead}</p><div class="regua"></div>' if lead else ""))


def cita(txt, fonte):
    return f'<div class="cita">“{txt}”<small>{fonte}</small></div>'


def box(k, corpo, cls=""):
    return f'<div class="box {cls}"><span class="k">{k}</span>{corpo}</div>'


def neste(itens):
    return box("Neste capítulo", '<ul class="neste">' + "".join(f"<li>{i}</li>" for i in itens) + "</ul>")


def revise(perguntas, respostas):
    return box("Revise sem consultar", '<ol class="rev">' + "".join(f"<li>{p}</li>" for p in perguntas) + "</ol>"
               + f'<div class="resp">Respostas: {respostas}</div>', "linha")


def tabela(cab_, linhas, cls_v=()):
    h = "<table><tr>" + "".join(f'<th class="{"v" if i in cls_v else ""}">{x}</th>' for i, x in enumerate(cab_)) + "</tr>"
    for ln in linhas:
        tot = ln and isinstance(ln[0], str) and ln[0].startswith("!")
        cel = [ln[0][1:] if tot else ln[0]] + list(ln[1:])
        h += f'<tr class="{"tot" if tot else ""}">' + "".join(f'<td class="{"v" if i in cls_v else ""}">{x}</td>' for i, x in enumerate(cel)) + "</tr>"
    return h + "</table>"


# ---------------------------------------------------------------- capa
logo_c = rel(BRAND / "zion-logo-claro.png", OUT)
pg(f"""<div class="capa-w"><img class="logo" src="{logo_c}" alt="Zion Hotel Group">
<div><div class="k" style="color:var(--ouro)">Trilha 1 · Pilar 6 · Aprofundamento · Método Zion</div>
<h1>CAPEX<br><i>quanto custa o seu projeto inteiro</i></h1>
<p class="sub">Aprenda o passo a passo para calcular quanto custa o seu projeto inteiro, bloco por bloco e com a origem de cada número, antes de assinar qualquer obra.</p>
<div class="pub">Para Airbnb, casas, apartamentos, pousadas e glampings</div></div>
<div class="pe">Zion Hospitality Business · Transforme Seu Terreno em um Projeto de Hospedagem de Sucesso · E-book da página 6A do Dossiê</div>
<span class="marca">6A</span></div>""", "capa")

# ---------------------------------------------------------------- sumário
SUM = [("00", "Como usar este aprofundamento"), ("01", "O preço que chegou não é o projeto"), ("02", "O que entra e o que fica à parte"),
       ("03", "Cada número tem origem: como pedir três cotações comparáveis"), ("04", "Projetos, licenças e infraestrutura por fase"),
       ("05", "Unidades e áreas comuns: o metro quadrado inteiro"), ("06", "Mobiliário, enxoval e suprimentos"),
       ("07", "Pré-abertura e a reserva do imprevisto"), ("08", "Terreno, giro e o investimento total"),
       ("09", "Ler o número antes de mostrá-lo"), ("10", "Erros comuns"), ("11", "O caso dos Chalés do Ribeirão"),
       ("12", "Exercícios e gabarito"), ("13", "O que perguntar aos profissionais"), ("14", "A página 6A e a próxima etapa")]
pg('<div class="k">Sumário</div><h2 style="margin-bottom:6mm">O que tem <i>neste e-book</i></h2>'
   + '<table class="sum">' + "".join(f'<tr><td class="sn">{n}</td><td>{t}</td></tr>' for n, t in SUM) + "</table>"
   + box("Como ler", "<p>Leia um capítulo por vez, com calculadora e papel. Cada capítulo abre com o que você vai ver e fecha com três perguntas para responder sem consultar. Os números que aparecem nos exemplos são <b>fictícios</b> e servem só para mostrar a conta. Este e-book não traz preço de referência: ele ensina a conseguir o seu número.</p>"))

# ---------------------------------------------------------------- 00
pg(cab("00", "Capítulo 00 · Antes de começar", "Como usar <i>este aprofundamento</i>",
       "Você já fez a página 6 no Pilar 6. Aqui ela ganha uma página irmã, a 6A, com o custo da fase aberto em sete blocos.")
   + "<p>No Pilar 6 você fez a primeira conta inteira: quanto custa abrir a porta, quanto sobra e quando volta. Aquela conta usa poucas linhas, de propósito. Este aprofundamento abre a linha mais pesada, o custo de abrir a porta, para que cada parte dele tenha nome, valor e origem.</p>"
   + '<div class="grid3">'
   + '<div class="card"><b class="t">O que você leva</b>A página <b>6A · O meu CAPEX</b>: os sete blocos, o custo da fase, o investimento total, o custo por unidade e por m², e o que falta cotar.</div>'
   + '<div class="card"><b class="t">Quanto tempo</b>Uma tarde para a primeira versão, com estimativas e linhas em branco. Trocar cada linha por cotação leva o tempo dos fornecedores.</div>'
   + '<div class="card"><b class="t">O que não prometemos</b>Preço certo, aprovação de projeto, crédito, parceria, retorno ou prazo de obra. Ensinamos o caminho da conta.</div></div>'
   + cita("Uma linha em branco vale mais do que um número inventado.", "Pilar 6 · Pré-viabilidade, cap. 00")
   + "<h3>As seis etapas da lição</h3>"
   + tabela(["Etapa", "O que você faz", "Onde"], [
       ["1 · Diagnosticar", "Escreve o seu palpite, com data", "Capítulo 1 e ficha"],
       ["2 · Compreender", "Entende os sete blocos e o que fica à parte", "Capítulos 2 a 10 e aula interativa"],
       ["3 · Observar", "Acompanha um caso inteiro, com dados fictícios", "Capítulo 11 e tutorial"],
       ["4 · Executar", "Resolve os exercícios e preenche a ficha com os seus números", "Capítulo 12, checklist e ficha"],
       ["5 · Validar", "Corrige o que os alertas da ficha apontam", "Resultado da ficha"],
       ["6 · Entregar", "Baixa a página 6A e refaz a página 6", "Capítulo 14"]])
   + box("Uma palavra só de sigla", "<p><b>CAPEX</b> vem do inglês <i>capital expenditure</i>: o dinheiro gasto para construir e equipar. Neste e-book ele tem sempre o mesmo sentido: <b>o custo de abrir a porta da fase</b>, tudo o que precisa existir até o primeiro hóspede.</p>"))

# ---------------------------------------------------------------- 01
pg(cab("01", "Capítulo 01 · O problema do palpite", "O preço que chegou <i>não é o projeto</i>",
       "Um construtor fala um valor por unidade. Você multiplica pelo número de unidades e sente alívio. Esse alívio é o risco.")
   + neste(["Por que o palpite vem primeiro", "A troca da pergunta", "Os cinco erros do orçamento amador", "O seu palpite, com data"])
   + "<p>Quase todo projeto começa assim: alguém pede o preço de uma unidade, recebe um número e multiplica. O número que chega é verdadeiro, mas é de outra coisa. Ele cobre a unidade. Não cobre a rede de energia que leva a luz até ela, o caminho, a água, o esgoto, a cama, o enxoval, as fotos do anúncio, a licença de funcionamento nem a reserva para o que der errado.</p>"
   + cita("Não é quanto custa a cabana. É quanto custa abrir a porta.", "Pilar 6 · Pré-viabilidade, cap. 02")
   + "<h3>Primeiro o palpite, depois a conta</h3><p>Antes de somar qualquer coisa, escreva o seu palpite e a data. Não é para acertar. É para, no fim, comparar o palpite com a conta. A diferença entre os dois mostra o tamanho do risco que você estava prestes a correr.</p>"
   + box("Faça agora · O meu palpite", '<p style="margin-bottom:1mm">Quanto custa abrir a porta da minha fase um, sem pesquisar?</p><div class="campo"></div>'
         '<p style="margin:2mm 0 1mm">De onde veio esse número? Quem disse, e quando?</p><div class="campo"></div><p style="margin:2mm 0 1mm">Data de hoje:</p><div class="campo" style="width:50mm"></div>', "linha"))

pg("<h3 style='margin-top:0'>Os cinco erros do orçamento amador</h3><p>O Volume 05 do método lista cinco erros que aparecem juntos no orçamento de quem começa. Cada um tem um bloco da lição que o corrige.</p>"
   + tabela(["O erro", "O que acontece", "Onde corrigimos"], [
       ["Orçar só as unidades", "Áreas comuns, serviço e infraestrutura ficam de fora e aparecem no meio da obra", "Blocos 2 e 3 (capítulos 4 e 5)"],
       ["Usar o custo do m² de outra região ou de outro ano", "O preço não é o seu: muda com o padrão, o terreno e a região", "Cotação com data (capítulo 3)"],
       ["Esquecer o enxoval, os utensílios e os suprimentos", "O chalé fica pronto e não dá para receber ninguém", "Bloco 5 (capítulo 6)"],
       ["Tratar a reserva como opcional", "O primeiro imprevisto vira dívida ou obra parada", "Bloco 7 (capítulo 7)"],
       ["Esquecer a pré-abertura", "Fotos, site, treinamento e licença de operar sem dinheiro reservado", "Bloco 6 (capítulo 7)"]])
   + '<p class="cap">Os cinco erros, a partir do Volume 05 · Investimento, cap. 2. O Pilar 6 troca o quinto por “esquecer o caixa dos primeiros meses”, que tratamos no capítulo 8.</p>'
   + cita("Um projeto hoteleiro não morre quando falta dinheiro. Morre quando os números nunca foram feitos.", "Volume 05 · Investimento, cap. 1")
   + "<p>A raiz dos cinco erros é uma só: o orçamento parou onde o primeiro preço parou. A saída também é uma só. Em vez de perguntar quanto custa a unidade, listamos tudo o que precisa existir até o primeiro hóspede, em sete blocos, e damos a cada linha uma origem.</p>"
   + box("Para levar", "<ul><li>O primeiro preço cobre quase sempre só a unidade.</li><li>Escreva o palpite com data antes de fazer a conta.</li><li>Cada um dos cinco erros tem um bloco que o corrige.</li></ul>", "escuro")
   + revise(["Por que o palpite se escreve antes da conta?", "Qual é a pergunta certa no lugar de “quanto custa a cabana”?", "Cite três dos cinco erros do orçamento amador."],
            "1 · para comparar no fim e ver o tamanho do risco; 2 · quanto custa abrir a porta; 3 · orçar só as unidades, usar m² de outra região ou ano, esquecer o enxoval e os suprimentos, tratar a reserva como opcional, esquecer a pré-abertura."))

# ---------------------------------------------------------------- 02
diag = """<div class="diag"><div class="col">
<div class="bl">1 · Projetos, licenças e documentação</div><div class="bl">2 · Infraestrutura</div><div class="bl">3 · Unidades e áreas comuns</div>
<div class="bl">4 · Mobiliário e equipamentos</div><div class="bl">5 · Enxoval, utensílios e suprimentos</div><div class="bl">6 · Pré-abertura</div>
<div class="bl ouro">7 · Reserva do imprevisto</div>
<div class="tot1">= CAPEX da fase<small>o custo de abrir a porta</small></div>
<div class="mais">+ Capital de giro<small>à parte, somado</small></div>
<div class="tot2">= Investimento total da fase</div></div>
<div class="lado"><div class="fora"><b>Terreno</b>Capital empregado. Anotado ao lado, com valor e forma de entrada. <b style="display:inline">Não é somado.</b></div>
<div class="fora"><b>Custo da captação e juros da obra</b>Ficam no Pilar 7, junto com a necessidade de capital.</div>
<div class="fora"><b>Escopo novo</b>O que você decide no meio da obra é linha nova e decisão nova. Não sai da reserva.</div></div></div>"""
pg(cab("02", "Capítulo 02 · Dentro, ao lado e à parte", "O que entra e <i>o que fica à parte</i>",
       "Sete blocos formam o custo de abrir a porta. O giro se soma por fora. O terreno fica ao lado, sem entrar na soma.")
   + neste(["Os sete blocos", "CAPEX da fase e investimento total", "Por que o terreno fica ao lado", "O que vai para o Pilar 7"])
   + diag
   + cita("fora da conta não quer dizer de graça", "Pilar 6 · Pré-viabilidade, cap. 02")
   + "<p>Os nomes técnicos que você vai ouvir de profissionais aparecem aqui uma única vez: o bloco 4 é o que o mercado chama de <b>FF&amp;E</b> (mobiliário e equipamentos) e o bloco 5 é o <b>OS&amp;E</b> (enxoval, utensílios e suprimentos de operação). No resto do e-book usamos os nomes em português.</p>")

pg("<h3 style='margin-top:0'>Os sete blocos: o que entra e o que não entra</h3>"
   + tabela(["Bloco", "Entra", "Não entra (vai para outro lugar)"], [
       ["<b>1 · Projetos, licenças e documentação</b>", "Arquitetura; engenharias (estrutural, elétrica, hidrossanitária); levantamento do terreno; aprovações e taxas da prefeitura; licença ambiental, se houver", "A licença que autoriza <b>operar</b> (vai para o bloco 6)"],
       ["<b>2 · Infraestrutura</b>", "Acesso e caminhos; rede de energia; água; esgoto e tratamento; drenagem; internet; estacionamento; ligação de luz, água e esgoto de cada unidade", "A parte da rede que só será paga nas próximas fases (fica anotada, fora da conta da fase)"],
       ["<b>3 · Unidades e áreas comuns</b>", "Cada unidade pelo m² construído; deck e piso, se cotados à parte; apoio, lavanderia, recepção, cozinha, deck comum, trilhas, casa de máquinas. A estrutura pronta (bolha, domo, cabana pré-fabricada) conta aqui, como unidade", "Mobília e enxoval (blocos 4 e 5)"],
       ["<b>4 · Mobiliário e equipamentos</b>", "Cama e colchão, móveis, iluminação, cozinha compacta e eletrodomésticos, banheiro; equipamentos gerais, como os da lavanderia", "Lençol, toalha e utensílios (bloco 5)"],
       ["<b>5 · Enxoval, utensílios e suprimentos</b>", "Três jogos de roupa por cama; utensílios de cozinha; listas de governança e limpeza, recepção, manutenção e segurança", "Qualquer item que já veio na cotação do mobiliário"],
       ["<b>6 · Pré-abertura</b>", "Licença de funcionamento e cadastros; fotos e site; identidade e marketing de lançamento; treinamento e contratação; seguro do primeiro ano; abertura de teste", "O caixa dos primeiros meses (é o giro)"],
       ["<b>7 · Reserva do imprevisto</b>", "Um percentual sobre a soma dos blocos 1 a 6, com regra de uso escrita", "Escopo novo, linha esquecida e caixa da operação"]])
   + box("Uma regra que vale para todos os blocos", "<p><b>Cada item numa linha só.</b> Se o mobiliário já veio com o enxoval, o enxoval não se soma de novo no bloco 5. Contar duas vezes engorda a conta; não contar nenhuma esconde um custo. Na dúvida, escreva ao lado da linha o que ela inclui.</p>")
   + revise(["O capital de giro entra no CAPEX?", "Em que bloco fica a licença de funcionamento?", "O que acontece com o terreno na conta?"],
            "1 · não: fica à parte e se soma no investimento total; 2 · no bloco 6, pré-abertura, porque autoriza operar; 3 · fica ao lado, como capital empregado, sem entrar na soma."))

# ---------------------------------------------------------------- 03
pg(cab("03", "Capítulo 03 · A origem de cada número", "Cada número tem origem: <i>cotação ou em branco</i>",
       "Um número sem origem parece um número, mas não sustenta nenhuma decisão. Ao lado de cada linha escrevemos de onde ele veio.")
   + neste(["As três origens de um número", "Por que a linha em branco é honesta", "Como pedir três cotações comparáveis", "Validade de 90 dias"])
   + '<div class="grid3">'
   + '<div class="card"><b class="t">Cotação</b>Proposta escrita do fornecedor, com escopo e data. É a origem que sustenta a conta.</div>'
   + '<div class="card"><b class="t">Estimativa minha</b>Um valor que você pôs sem proposta escrita. Entra na soma, mas conta como <b>sem cotação</b> e é risco.</div>'
   + '<div class="card"><b class="t">Em branco</b>Você sabe que a linha existe e ainda não tem número. Vale zero na soma e aparece como risco, com nome.</div></div>'
   + "<p>Este aprofundamento não traz nenhum preço de referência, nem por m², nem por unidade. Preço de outra região, de outro ano ou de outro padrão construtivo é exatamente o segundo erro do orçamento amador. O caminho é outro: listar as linhas, pedir a proposta certa e anotar a data.</p>"
   + "<h3>Por que a linha em branco ajuda</h3><p>Uma linha em branco com nome mostra o que falta cotar. Um número inventado esconde o que falta. Na primeira versão da sua página 6A é normal ter várias linhas em branco: elas viram a sua lista de cotações.</p>"
   + cita("A frase “não inclui” é a mais importante de qualquer proposta.", "Jornada do COMO · Etapa 04, Passo 09")
   + "<p>A proposta mais barata costuma ser a que deixou mais coisa de fora. Por isso pedimos a cada fornecedor a lista do que <b>não</b> está incluído e só comparamos propostas com o mesmo escopo.</p>")

pg("<h3 style='margin-top:0'>Como pedir três cotações comparáveis, passo a passo</h3>"
   + '<ol class="passos">'
   "<li><b>Monte um pacote só.</b> Projeto, memorial descritivo (a descrição de materiais e acabamentos) e quantidades. Todos os fornecedores recebem o mesmo pacote.</li>"
   "<li><b>Escreva a especificação.</b> Material, medidas, quantidade, frete, instalação, retirada de entulho, prazo e garantia.</li>"
   "<li><b>Peça o orçamento aberto por etapa</b>, e não só o valor fechado. Assim você enxerga onde as propostas diferem.</li>"
   "<li><b>Peça a lista do que não inclui.</b> Por escrito, em cada proposta.</li>"
   "<li><b>Receba três propostas</b> com a mesma especificação. Escolha a menor só se o escopo for igual.</li>"
   "<li><b>Anote a data</b> de cada proposta. Depois de 90 dias, refaça antes de usar.</li>"
   "<li><b>Na estrutura pronta</b> (bolha, domo, cabana pré-fabricada), confirme por escrito se frete, fundação e montagem estão incluídos.</li></ol>"
   + cita("Cotação de mais de noventa dias precisa ser refeita.", "Volume 05 · Investimento, cap. 4")
   + box("Modelo de pedido de cotação", "<p style='font-size:9.6pt'>“Olá. Estou orçando a fase um de um projeto de hospedagem e peço uma proposta para <b>[item]</b>, conforme o pacote anexo (projeto, memorial e quantidades). Por favor, informe: material e medidas; quantidade; se inclui frete, instalação e retirada de entulho; prazo de entrega e de execução; garantia; validade da proposta; e a lista do que <b>não</b> está incluído. Peço o orçamento aberto por etapa. Obrigado.”</p>", "linha")
   + tabela(["Ao comparar, confira", "Proposta A", "Proposta B", "Proposta C"], [
       ["Mesma especificação e quantidade", "", "", ""], ["Frete, instalação e entulho", "", "", ""], ["Prazo e garantia", "", "", ""],
       ["O que não inclui", "", "", ""], ["Data e validade", "", "", ""]])
   + revise(["Quais são as três origens possíveis de um número?", "O que pedir, por escrito, em toda proposta?", "Por quanto tempo uma cotação vale nesta lição?"],
            "1 · cotação, estimativa minha e em branco; 2 · a lista do que não inclui; 3 · até 90 dias; depois, refaça."))

# ---------------------------------------------------------------- 04
pg(cab("04", "Capítulo 04 · Blocos 1 e 2", "Projetos, licenças e <i>infraestrutura por fase</i>",
       "O bloco 1 aprova o projeto e a obra. O bloco 2 leva energia, água e caminho até cada unidade.")
   + neste(["O que entra no bloco 1", "As perguntas do terreno", "Distância e capacidade", "Dimensionar para o total, pagar por fase"])
   + "<h3>Bloco 1 · Projetos, licenças e documentação</h3><p>Entram aqui os projetos e as aprovações que permitem construir: arquitetura, engenharias, levantamento do terreno, taxas da prefeitura e licença ambiental, se o lugar exigir. A licença que autoriza <b>operar</b> a hospedagem fica no bloco 6, porque só vem depois da obra.</p>"
   + "<h3>Bloco 2 · As perguntas do terreno, antes de cotar</h3>"
   + '<div class="grid3"><div class="card">Qual a distância até o ponto de energia, e de que tipo é a rede? A concessionária informa; confirme com a concessionária local.</div>'
   '<div class="card">De onde vem a água: rede, poço ou nascente? Qual a vazão, e precisa de outorga?</div>'
   '<div class="card">O solo pede fundação especial?</div><div class="card">Um caminhão chega até as unidades em dia de chuva?</div>'
   '<div class="card">Qual a declividade do terreno?</div><div class="card">Quanto tempo leva a licença?</div></div>'
   + cita("O amador orça o chalé. O developer orça o que faz o chalé funcionar.", "Volume 05 · Investimento, cap. 4")
   + "<p>A infraestrutura comum não se orça por unidade. Ela se orça por <b>distância</b> (quantos metros de rede até a unidade mais distante) e por <b>capacidade</b> (para quantas unidades cada sistema é dimensionado). Por isso a primeira pergunta do orçamento é a distância até o ponto de energia.</p>"
   + "<h3>Dimensionar para o projeto completo</h3>" + "<p>Quem planeja seis unidades e abre com quatro tem duas escolhas. Pode fazer a rede só para quatro e refazer vala, cabo e caminho quando vierem as outras duas. Ou pode dimensionar a rede para as seis e construí-la uma vez, pagando agora o tronco comum e as ligações das quatro. A segunda escolha custa um pouco mais hoje e evita a obra mais cara do projeto, que é desmanchar o que já está pronto.</p>")

infra = """<div class="infra"><div class="poste">Ponto de energia<small>180 m</small></div><div class="tronco">Rede comum dimensionada para 6 unidades</div>
<div class="uns"><div class="u f">1</div><div class="u f">2</div><div class="u f">3</div><div class="u f">4</div><div class="u">5</div><div class="u">6</div></div>
<div class="leg"><span><i class="f"></i>Fase um: paga a rede comum e as ligações destas 4</span><span><i></i>Fase dois: paga só as ligações destas 2</span></div></div>"""
pg("<h3 style='margin-top:0'>Construir uma vez, pagar por fase</h3>"
   + FICT + infra
   + cita("Nunca desenhe um projeto que só funciona inteiro. Desenhe um organismo que cresce.", "Volume 05 · Investimento, cap. 12")
   + tabela(["Na conta da fase um", "Fica anotado para as próximas fases"], [
       ["A rede comum (energia, água, esgoto, acesso) já na capacidade do projeto completo", "As ligações das unidades que ainda não serão construídas"],
       ["As ligações de luz, água e esgoto de cada unidade desta fase", "A parte de caminhos e estacionamento que só serve às próximas unidades, se o projetista separar"]])
   + "<p>Na ficha, você informa para quantas unidades a rede é dimensionada. Se esse número for menor do que o projeto completo, a ficha avisa. Se você souber o valor da rede inteira, pode anotar: a diferença aparece como “fica para as próximas fases” e não entra no CAPEX da fase.</p>"
   + box("Para levar", "<ul><li>Licença de obra no bloco 1; licença de operar no bloco 6.</li><li>Infraestrutura por distância e capacidade, não por unidade.</li><li>Rede para o projeto completo, construída uma vez e paga por fase.</li></ul>", "escuro")
   + revise(["Qual é a primeira pergunta do orçamento da infraestrutura?", "Por que não orçar a rede por unidade?", "O que a fase um paga da rede?"],
            "1 · a distância até o ponto de energia; 2 · porque ela depende de distância e capacidade; 3 · a rede comum, já dimensionada para o total, e as ligações das unidades desta fase."))

# ---------------------------------------------------------------- 05
pg(cab("05", "Capítulo 05 · Bloco 3", "Unidades e áreas comuns: <i>o metro quadrado inteiro</i>",
       "O custo do bloco 3 é a área construída total vezes o custo do m² cotado para o seu padrão, no seu terreno, neste ano.")
   + neste(["A área construída total", "O custo do m² que vale", "A estrutura pronta como unidade", "Áreas comuns também custam"])
   + box("A conta do bloco 3", "<p style='font-size:12pt;margin:0'><b>área construída total</b> × <b>custo do m² cotado</b> &nbsp;+&nbsp; extras cotados à parte (deck, piso)</p>")
   + "<p>A área total não é só a das unidades. Ela inclui recepção, apoio, lavanderia, cozinha, deck, trilhas, casa de máquinas, reservatórios e tratamento de esgoto.</p>"
   + "<h3>O custo do m² que vale é o seu</h3><p>O custo do m² muda com o padrão construtivo, com o terreno e com a região. Nunca use o custo de outra região ou de outro ano. Peça ao engenheiro ou ao construtor o custo do m² para o sistema que você escolheu, com escopo e data, e pergunte o que ele inclui.</p>"
   + "<h3>A estrutura pronta conta como unidade</h3><p>Bolha, domo, cabana pré-fabricada ou módulo entram no bloco 3, como unidade, e não como mobiliário. Na cotação, confirme por escrito se frete, fundação e montagem estão incluídos. Se não estiverem, viram linhas próprias.</p>"
   + cita("Corte metros quadrados no projeto. Nunca corte a experiência dentro deles.", "Volume 05 · Investimento, cap. 5")
   + revise(["O que entra na área construída total?", "Em que bloco entra uma bolha ou um domo?", "Que três itens confirmar na cotação da estrutura pronta?"],
            "1 · unidades, apoio, recepção, cozinha, deck, trilhas, casa de máquinas, reservatórios e tratamento; 2 · no bloco 3, como unidade; 3 · frete, fundação e montagem."))

# ---------------------------------------------------------------- 06
pg(cab("06", "Capítulo 06 · Blocos 4 e 5", "Mobiliário, enxoval <i>e suprimentos</i>",
       "A unidade pronta para o hóspede é a unidade construída mais tudo o que vai dentro dela.")
   + neste(["A unidade-modelo", "Comprar no tempo certo", "Três jogos por cama", "Um dia de operação em cinco listas"])
   + "<h3>Bloco 4 · Mobiliário e equipamentos</h3><p>Monte primeiro uma <b>unidade-modelo</b> completa, item a item, com especificação escrita: cama e colchão, móveis, iluminação, cozinha compacta e eletrodomésticos, banheiro. Só depois multiplique pelo número de unidades e peça cotação em lote. Somam-se aqui os equipamentos gerais, como os da lavanderia e das áreas comuns.</p>"
   + '<div class="grid2"><div class="card"><b class="t">Compre no tempo certo</b>Alguns itens têm prazo de fornecimento longo. Faça a lista de compra de trás para a frente, a partir da data de abertura, para não ter de escolher entre atrasar ou abrir com o que tinha na loja.</div>'
   '<div class="card"><b class="t">Não corte no fim</b>Quando o caixa aperta no fim da obra, o mobiliário costuma ser o primeiro corte. É a parte que o hóspede toca. Se for preciso cortar, corte área no projeto, antes de construir.</div></div>'
   + box("Exemplo de unidade-modelo (dados fictícios)", "<p style='margin:0'>No caso do capítulo 11, a unidade-modelo de um chalé tem cama e colchão, mobiliário, iluminação e cozinha compacta com eletrodomésticos. Somadas, as quatro linhas dão R$ 19.200 por chalé, que se multiplicam pelos 4 chalés da fase. Os equipamentos da lavanderia entram uma vez só, como equipamento geral.</p>", "ex"))

pg("<h3 style='margin-top:0'>Bloco 5 · Enxoval, utensílios e suprimentos</h3>"
   + "<p><b>Três jogos de roupa por cama:</b> um em uso, um na lavanderia e um no estoque. A conta do enxoval é: unidades × camas por unidade × 3 jogos × custo do jogo cotado.</p>"
   + "<p><b>Um dia de operação em cinco listas.</b> Simule um dia inteiro, da chegada à saída do hóspede, e anote cada objeto que alguém toca. Separe em cinco listas:</p>"
   + '<div class="grid3" style="grid-template-columns:repeat(5,1fr)">' + "".join(f'<div class="card" style="text-align:center"><b>{x}</b></div>' for x in ["Governança e limpeza", "Cozinha", "Recepção", "Manutenção", "Segurança"]) + "</div>"
   + "<p style='margin-top:3mm'>Se a sua hospedagem não tem recepção, marque essa lista como “não se aplica”, com o motivo. E lembre a regra do capítulo 2: se o enxoval já veio na cotação do mobiliário, ele não se soma de novo.</p>"
   + box("Para levar", "<ul><li>Unidade-modelo completa antes de comprar as demais.</li><li>Três jogos por cama.</li><li>Um dia de operação em cinco listas; cada item numa linha só.</li></ul>", "escuro")
   + revise(["Por que montar a unidade-modelo primeiro?", "Para que servem os três jogos de roupa?", "Quais são as cinco listas do bloco 5?"],
            "1 · para especificar item a item e cotar em lote com segurança; 2 · um em uso, um na lavanderia, um no estoque; 3 · governança e limpeza, cozinha, recepção, manutenção e segurança."))

# ---------------------------------------------------------------- 07
pg(cab("07", "Capítulo 07 · Blocos 6 e 7", "Pré-abertura e <i>a reserva do imprevisto</i>",
       "Os dois blocos que o orçamento amador esquece: o que acontece entre a obra pronta e o primeiro hóspede, e o dinheiro para o que der errado.")
   + neste(["O que a pré-abertura cobre", "O que a reserva cobre e não cobre", "Quanto reservar", "A regra de uso em quatro linhas"])
   + "<h3>Bloco 6 · Pré-abertura</h3><p>É tudo o que precisa acontecer para a porta abrir depois da obra pronta:</p>"
   + '<div class="grid3">' + "".join(f'<div class="card">{x}</div>' for x in ["Licença de funcionamento e cadastros", "Fotos e site", "Identidade e marketing de lançamento", "Treinamento e contratação", "Seguro do primeiro ano", "Abertura de teste, com poucos hóspedes"]) + "</div>"
   + "<p style='margin-top:3mm'>A pré-abertura não é o caixa dos primeiros meses. O caixa é o giro, que fica fora do CAPEX (capítulo 8).</p>"
   + "<h3>Bloco 7 · Reserva do imprevisto</h3>"
   + '<div class="grid2"><div class="card"><b class="t">Cobre</b>O imprevisto da obra que foi orçada: solo diferente do esperado, chuva, reajuste de preço, exigência da licença.</div>'
   '<div class="card"><b class="t">Não cobre</b>Escopo novo (o ofurô decidido no meio da obra), linha esquecida no orçamento e o caixa dos primeiros meses.</div></div>'
   + cita("A contingência não é pessimismo. É maturidade.", "Volume 05 · Investimento, caps. 1 e 7")
)

pg("<h3 style='margin-top:0'>Quanto reservar</h3>"
   + "<p>As fontes do método citam uma faixa de conferência de 10% a 15% sobre a soma dos blocos 1 a 6. Com fator de risco, a fonte pede o teto ou acima: território remoto, sistema construtivo novo para a equipe, itens importados, licenciamento em área sensível, prazo apertado pela temporada, ou a sua primeira obra. Em imóvel pronto que será adequado, as fontes citam faixas maiores, de 15% a 25%. A reserva nunca é zero. Acima de 25%, confira se ela não está cobrindo linha esquecida.</p>"
   + '<p class="cap">Faixas citadas pelas fontes (Volume 05 · Investimento, caps. 3 e 7; Pilar 6, cap. 03; Jornada do COMO, Etapas 02 e 04). São faixas de conferência, não regra fixa.</p>'
   + "<h3>A regra de uso, em quatro linhas</h3><p>A reserva sem regra vira o dinheiro de qualquer coisa. Escreva, antes da obra começar, as quatro linhas abaixo. Na ficha, as quatro são obrigatórias.</p>"
   + tabela(["Linha", "Pergunta", "Exemplo (dados fictícios)"], [
       ["1 · Para quê", "O que a reserva pode pagar?", "Imprevisto da obra orçada: solo, chuva, reajuste, exigência da licença"],
       ["2 · Quem autoriza", "Quem decide usar?", "A dona, depois de ouvir o engenheiro"],
       ["3 · Como se registra", "Onde fica anotado cada uso?", "Planilha com data, motivo e valor"],
       ["4 · Quando se confere", "Em que momento se olha o saldo?", "A cada medição da obra"]])
   + box("Escreva a sua", '<div class="grid2">' + "".join(f'<div><p style="margin:0">{x}:</p><div class="campo"></div></div>' for x in ["Para quê", "Quem autoriza", "Como se registra", "Quando se confere"]) + "</div>", "linha")
   + "<h3>E se sobrar?</h3><p>A reserva que não for usada na obra vira capital de giro adicional. Ela não vira mobiliário mais caro nem obra nova. Quem tem regra escrita sabe o que fazer com a sobra antes de ela existir.</p>"
   + revise(["A reserva paga o ofurô decidido no meio da obra?", "Quais são as quatro linhas da regra de uso?", "Para onde vai a reserva que sobra?"],
            "1 · não: escopo novo é linha nova e decisão; 2 · para quê, quem autoriza, como se registra, quando se confere; 3 · vira capital de giro adicional."))

# ---------------------------------------------------------------- 08
pg(cab("08", "Capítulo 08 · À parte", "Terreno, giro e <i>o investimento total</i>",
       "Dois valores ficam fora do CAPEX por motivos diferentes: o giro porque é caixa da operação, o terreno porque já é capital empregado.")
   + box("As contas", "<p style='font-size:12pt;margin:0 0 1.5mm'><b>CAPEX da fase</b> = blocos 1 a 6 + reserva do imprevisto</p><p style='font-size:12pt;margin:0 0 1.5mm'><b>Investimento total da fase</b> = CAPEX da fase + capital de giro</p><p style='font-size:12pt;margin:0'><b>Terreno</b> = anotado ao lado, com valor e forma de entrada, sem somar</p>")
   + "<h3>O capital de giro</h3><p>É o dinheiro para pagar a operação enquanto as reservas ainda não pagam tudo. Ele precisa estar no banco no dia da abertura, em conta separada. Três meses de custo fixo são o piso citado pelas fontes; a conta completa do giro é a que você fez no Pilar 6. Aqui você só traz o valor de lá.</p>"
   + "<h3>O terreno</h3><p>O terreno fica fora do CAPEX, mas não é de graça: é capital empregado, dinheiro que já está no projeto. Anote o valor estimado e a forma de entrada: já é seu, vai comprar, permuta, sociedade ou arrendamento. A forma de entrada se decide com advogado e contador. Se você vai comprar, escritura, imposto de transmissão (ITBI), registro e certidões não estão nesta conta: pergunte ao contador.</p>"
   + "<h3>O que vai para o Pilar 7</h3><p>A necessidade de capital (quanto falta, tirando o que você já tem), o custo da captação e os juros de um empréstimo durante a obra não entram aqui. Eles ficam no Pilar 7, junto com a frase do pedido.</p>"
   + revise(["Qual a diferença entre CAPEX da fase e investimento total?", "Por que o terreno não entra na soma?", "Onde ficam os juros do empréstimo da obra?"],
            "1 · o investimento total soma o capital de giro ao CAPEX; 2 · porque já é capital empregado e é anotado ao lado; 3 · no Pilar 7."))

# ---------------------------------------------------------------- 09
pg(cab("09", "Capítulo 09 · Como ler o resultado", "Ler o número <i>antes de mostrá-lo</i>",
       "Um total sozinho não diz se a conta está completa. Cinco leituras rápidas mostram o que pode ter ficado de fora.")
   + neste(["O peso de cada bloco", "Custo por unidade e investimento por unidade", "Custo por m²", "Palpite × conta e a régua de maturidade"])
   + tabela(["Leitura", "Como se calcula", "O que ela mostra"], [
       ["<b>Peso de cada bloco</b>", "total do bloco ÷ CAPEX da fase", "Onde está o dinheiro; um bloco muito leve pode ter linha esquecida"],
       ["<b>Custo por unidade</b>", "CAPEX da fase ÷ unidades da fase", "Quanto custa abrir a porta de cada unidade, <b>sem</b> terreno e <b>sem</b> giro"],
       ["<b>Investimento por unidade</b>", "investimento total ÷ unidades da fase", "A mesma medida <b>com</b> o giro; é o que o Pilar 6 chama de custo por chave"],
       ["<b>Custo por m²</b>", "CAPEX da fase ÷ área construída total", "Uma medida para conversar com o engenheiro e comparar versões do seu projeto"],
       ["<b>Palpite × conta</b>", "palpite ÷ CAPEX da fase; e a diferença em reais", "O tamanho do risco que o palpite escondia"],
       ["<b>Linhas com cotação</b>", "linhas cotadas ÷ linhas da conta; e valor cotado ÷ soma dos blocos 1 a 6", "O quanto o número está apoiado em proposta escrita"]])
   + "<p>Sempre que mostrar um valor por unidade, diga o nome da medida. “Custo por unidade” e “investimento por unidade” são números diferentes, e misturar os dois é um jeito comum de enganar a si mesmo.</p>"
   + "<h3>A régua de maturidade</h3>"
   + '<div class="grid3"><div class="card"><b class="t">Sonhador</b>Ainda não há conta, ou só o bloco 3 tem valor.</div>'
   '<div class="card"><b class="t">Estimador</b>Há conta nos blocos, mas a maior parte ainda é estimativa ou está em branco.</div>'
   '<div class="card"><b class="t">Calculista</b>A maioria das linhas tem cotação escrita, e as três maiores linhas também.</div></div>'
   + '<p class="cap" style="margin-top:2mm">Rótulos do Volume 05 · Investimento, cap. 1, e do Pilar 6, cap. 02. O quarto degrau, Developer, pede cronograma de desembolso e captação, e fica para o Pilar 7.</p>')

pg("<h3 style='margin-top:0'>Faixas de conferência citadas pelas fontes</h3>"
   + "<p>As fontes do método trazem algumas proporções para conferir se a conta está completa. Elas <b>não são preço</b> nem regra fixa: a própria fonte diz que servem para conferir. Projeto pequeno pode cair fora delas, e tudo bem. Fora da faixa, revise o bloco; não mude o número para caber.</p>"
   + tabela(["Conferência", "Faixa citada", "Se ficar fora", "Fonte"], [
       ["Reserva ÷ soma dos blocos 1 a 6", "10% a 15%; no teto ou acima com fator de risco; imóvel pronto 15% a 25%", "Abaixo: risco descoberto. Acima de 25%: veja se cobre linha esquecida", "Volume 05, caps. 3 e 7; Pilar 6, cap. 03; Jornada do COMO, Etapas 02 e 04"],
       ["Bloco 5 ÷ bloco 4", "10% a 15%", "Abaixo: algo de um dia de operação ficou de fora. Acima: o enxoval pode estar contado duas vezes", "Volume 05, caps. 2 e 6"],
       ["Pré-abertura ÷ obra (blocos 2 + 3)", "5% a 10%", "Abaixo de 5%: o quinto erro, esquecer a pré-abertura", "Volume 05, caps. 2 e 7"],
       ["Obra (blocos 2 + 3) ÷ CAPEX", "60% a 70% citados; acima de 80%, provavelmente faltou algo", "Acima de 80%: procure o que não foi orçado nos outros blocos", "Volume 05, cap. 3"],
       ["Giro", "Três meses de custo fixo como piso", "Abaixo: refaça a conta do giro no Pilar 6", "Volume 05, caps. 7 e 10; Pilar 6, cap. 06"]])
   + box("Uma faixa nunca substitui uma cotação", "<p>Faixa serve para perguntar “esqueci alguma coisa?”. Ela não diz quanto custa o seu projeto. Quem diz é a proposta escrita, com escopo e data.</p>")
   + box("Para levar", "<ul><li>Leia o peso de cada bloco antes de mostrar o total.</li><li>Dê nome à medida por unidade: com ou sem giro.</li><li>Faixas citadas são conferência, não preço.</li></ul>", "escuro")
   + revise(["Qual a diferença entre custo por unidade e investimento por unidade?", "A obra deu 85% do CAPEX. O que isso sugere?", "O que é preciso para estar no degrau Calculista?"],
            "1 · o investimento por unidade inclui o giro; 2 · que provavelmente faltou algo nos outros blocos; 3 · maioria das linhas com cotação escrita e as três maiores linhas cotadas."))

# ---------------------------------------------------------------- 10 erros comuns
ERROS = [("Planejar pelo orçamento do construtor", "Ele cobre a obra. Some os outros seis blocos e o giro."),
         ("Fazer a rede só para a fase um", "Dimensione para o projeto completo e pague por fase."),
         ("Comparar cotações com escopos diferentes", "Mesmo pacote para todos e a lista do que não inclui."),
         ("Usar cotação antiga", "Anote a data; depois de 90 dias, refaça."),
         ("Contar o enxoval duas vezes, ou nenhuma", "Cada item numa linha só; escreva o que a linha inclui."),
         ("Usar a reserva para escopo novo", "Ofurô no meio da obra é linha nova e decisão nova."),
         ("Cortar o mobiliário no fim da obra", "Se precisar cortar, corte área no projeto, antes de construir."),
         ("Comprar o mobiliário tarde", "Lista de compra de trás para a frente, a partir da data de abertura."),
         ("Esquecer o capital de giro", "Ele precisa estar no banco no dia da abertura, em conta separada."),
         ("Somar o terreno ao custo da obra", "Anote ao lado, como capital empregado, com a forma de entrada."),
         ("Reforma com reserva menor do que obra nova", "Em imóvel pronto, as fontes pedem reserva maior."),
         ("Pagar a ampliação com o caixa da operação", "Quem já opera monta o CAPEX da ampliação à parte e não usa o caixa do dia a dia."),
         ("Áreas comuns grandes demais", "Cada m² tem custo; confira se cada área comum é essencial."),
         ("Inventar um número para não deixar em branco", "A linha em branco com nome vira a sua lista de cotações.")]
pg(cab("10", "Capítulo 10 · Antes de fechar o número", "Erros <i>comuns</i>",
       "Os erros que as fontes do método mais repetem, e o que fazer no lugar de cada um.")
   + tabela(["O erro", "O que fazer no lugar"], [[f"<b>{a}</b>", b] for a, b in ERROS])
   + '<p class="cap">A partir do Volume 05 · Investimento (caps. 2, 5 e 12), do Pilar 6 (caps. 02 a 04), da Jornada do COMO (Etapas 01, 02 e 04) e do Volume 06 · Implantação (cap. 6).</p>')

# ---------------------------------------------------------------- 11 caso
def linhas_bloco(i):
    nome, ls = c.BLOCOS[i]
    rot = {"C": "cotação", "E": "estimativa", "B": "em branco", "NA": "não se aplica"}
    out = []
    for n, v, o, k, m in ls:
        org = rot[o] + (f" ({k}{', mesma especificação' if m else ''})" if o == "C" else "")
        out.append([n, org, brl(v) if o in "CE" else "·"])
    out.append(["!Total do bloco " + nome.split(" ·")[0], "", brl(c.tot[i])])
    return out


pg(cab("11", "Capítulo 11 · Exemplo resolvido", "O caso dos <i>Chalés do Ribeirão</i>",
       "Helena herdou um terreno e quer abrir seis chalés, quatro na fase um. Vamos montar a página 6A dela do começo ao fim.")
   + FICT
   + '<div class="grid2"><div class="card"><b class="t">Premissas</b><ul style="margin:0"><li>Projeto completo: 6 chalés; fase um: 4</li><li>Primeira obra de Helena (fator de risco)</li><li>Rede dimensionada para 6</li><li>Ponto de energia a 180 m</li></ul></div>'
   '<div class="card"><b class="t">O palpite</b>R$ 700.000, escrito em 27/11/2026. Veio de um construtor que falou R$ 175.000 por chalé: 4 × 175.000.</div></div>'
   + "<h3>Blocos 1 e 2</h3>"
   + tabela(["Linha", "Origem", "Valor"], linhas_bloco(0) + linhas_bloco(1), (2,))
   + '<p class="cap">A cotação da água é de 20/07/2026: em 27/11/2026 ela tem 130 dias e precisa ser refeita.</p>')

pg(FICT + "<h3 style='margin-top:1mm'>Blocos 3 a 6</h3>"
   + tabela(["Linha", "Origem", "Valor"], linhas_bloco(2) + linhas_bloco(3) + linhas_bloco(4) + linhas_bloco(5), (2,)), "")

res_lin = [[f"Bloco {n.split(' ·')[0]} · {n.split('· ')[1]}", brl(t), pct(p)] for (n, _), t, p in zip(c.BLOCOS, c.tot, c.PESOS)]
pg(FICT + "<h3 style='margin-top:1mm'>A conta, passo a passo</h3>"
   + '<ol class="passos">'
   f"<li><b>Soma dos blocos 1 a 6:</b> 40.000 + 170.000 + 682.000 + 85.800 + 11.700 + 21.000 = <b>{brl(c.SUB)}</b>.</li>"
   "<li><b>Reserva:</b> Helena lança 12%, a ficha avisa que é a primeira obra dela, e ela sobe para 15%. 1.010.500 × 0,15 = <b>R$ 151.575</b>. Regra de uso: imprevisto da obra orçada; autoriza Helena, depois de ouvir o engenheiro; registro em planilha com data, motivo e valor; conferência a cada medição.</li>"
   f"<li><b>CAPEX da fase:</b> 1.010.500 + 151.575 = <b>{brl(c.CAPEX)}</b>.</li>"
   f"<li><b>Giro</b> (da página 6 de Helena: 3 meses × 15.000) = R$ 45.000. <b>Investimento total:</b> 1.162.075 + 45.000 = <b>{brl(c.INVEST)}</b>.</li>"
   "<li><b>Terreno:</b> já é dela, valor estimado de R$ 300.000. Fica anotado ao lado e <b>não é somado</b>.</li></ol>"
   + tabela(["Bloco", "Valor", "Peso no CAPEX"], res_lin + [["Bloco 7 · Reserva do imprevisto (15%)", brl(c.RES), pct(c.PESOS[6])], ["!CAPEX da fase", brl(c.CAPEX), "100%"]], (1, 2))
   + '<p class="cap">A soma dos pesos arredondados dá 99,9%: é efeito do arredondamento.</p>'
   + '<div class="grid3">'
   f'<div class="card"><b class="t">Custo por unidade</b>1.162.075 ÷ 4 = <b>{brl(c.CAPEX / 4, 2)}</b><br><small>sem terreno e sem giro</small></div>'
   f'<div class="card"><b class="t">Investimento por unidade</b>1.207.075 ÷ 4 = <b>{brl(c.INVEST / 4, 2)}</b><br><small>com o giro</small></div>'
   f'<div class="card"><b class="t">Custo por m²</b>Área: 4 × 32 + 4 × 10 + 20 = 188 m². 1.162.075 ÷ 188 = <b>{brl(c.CAPEX / c.AREA, 2)}</b></div></div>')

pg(FICT + "<h3 style='margin-top:1mm'>A leitura do resultado</h3>"
   + tabela(["Leitura", "Resultado", "O que significa"], [
       ["Palpite × conta", f"700.000 ÷ 1.162.075 = {pct(c.PALPITE / c.CAPEX)}; diferença de R$ 462.075", "O palpite cobria pouco mais da metade da conta"],
       ["Linhas com cotação", f"17 de 32 = {pct(c.NC / c.N)}", "A maioria das linhas tem cotação escrita"],
       ["Valor com cotação", f"957.000 ÷ 1.010.500 = {pct(c.COTADO / c.SUB)}", "As linhas grandes estão cotadas; as estimativas somam R$ 53.500"],
       ["Três maiores linhas", "Chalés, apoio e energia: todas cotadas", "Degrau <b>Calculista</b> (o diagnóstico tinha dado Estimador)"],
       ["Obra ÷ CAPEX", "852.000 ÷ 1.162.075 = 73,3%", "Abaixo de 80%; acima dos 60% a 70% citados, o que é comum em projeto pequeno"],
       ["Bloco 5 ÷ bloco 4", "11.700 ÷ 85.800 = 13,6%", "Dentro da faixa citada"],
       ["Pré-abertura ÷ obra", "21.000 ÷ 852.000 = 2,5%", "<b>Abaixo da faixa citada</b>: a pré-abertura pode estar incompleta"],
       ["Rede", "Dimensionada para 6 = projeto completo", "Sem alerta"]])
   + box("Os três pontos de atenção", "<ol style='margin:0'><li><b>Pré-abertura abaixo da faixa citada.</b> Duas linhas estão em branco: licença de funcionamento e seguro do primeiro ano.</li><li><b>Uma cotação vencida:</b> a da água, com 130 dias.</li><li><b>Dez linhas com menos de três cotações</b> ou sem a mesma especificação (energia e apoio com uma; oito com duas).</li></ol>")
   + box("A ação de 30 dias", "<p><b>Ação:</b> pedir cotação escrita da licença ambiental, da internet, da segurança, da licença de funcionamento e do seguro do primeiro ano. <b>Prazo:</b> 27/12/2026. <b>Como verificar:</b> as cinco propostas, com data e escopo, lançadas na ficha.</p>", "ex")
   , "")

pg(FICT + "<h3 style='margin-top:1mm'>Como levar para a página 6</h3>"
   + "<p>A ficha do Pilar 6 tem poucas linhas: as da unidade pronta, licenças, reserva e infraestrutura comum. Para levar a página 6A até ela, dividimos o que é de cada unidade pelo número de unidades e juntamos o resto no campo de infraestrutura comum, com uma nota escrita.</p>"
   + tabela(["Campo da página 6", "Valor"], [["Unidades", "4"], ["Unidade (chalé)", "R$ 144.000"], ["Deck", "R$ 9.000"], ["Luz", "R$ 3.500"], ["Água e esgoto", "R$ 2.500"],
                                             ["Mobiliário, equipamentos e enxoval: (76.800 + 11.700) ÷ 4", "R$ 22.125"], ["Piso", "R$ 0 (incluído no custo do m²)"],
                                             ["Licenças e projetos", "R$ 40.000"], ["Reserva", "15%"], ["Infraestrutura comum, à parte (inclui áreas comuns, equipamentos gerais, pré-abertura e a reserva dessa parte)", "R$ 288.900"],
                                             ["Giro / terreno", "R$ 45.000 / R$ 300.000"]], (1,))
   + box("A conferência", "<p style='margin:0'>Unidade pronta: 144.000 + 9.000 + 3.500 + 2.500 + 22.125 = <b>R$ 181.125</b>. Vezes 4 unidades = 724.500; com a reserva de 15%, 833.175; mais licenças e projetos (40.000) e infraestrutura comum (288.900) = <b>R$ 1.162.075</b>, o mesmo CAPEX da fase. Se a sua conta não fechar assim, alguma linha ficou fora ou foi contada duas vezes.</p>")
   + "<p>Na página 6, as linhas com cotação levam nota 3; as estimativas, nota 1; as linhas em branco, “Não sei”. Assim a página 6 mostra o mesmo grau de confiança da 6A.</p>")

# ---------------------------------------------------------------- 12 exercícios
pg(cab("12", "Capítulo 12 · Agora é com você", "Exercícios <i>e gabarito</i>",
       "Do mais guiado ao em branco. O exercício 1 é o caso do capítulo 11. Resolva os outros com calculadora; o gabarito está duas páginas adiante.")
   + FICT
   + box("Exercício 2 · Parcialmente resolvido", "<p>O mesmo projeto de Helena, mas trocando os chalés construídos por <b>estrutura pronta a R$ 150.000 por unidade</b>. O fornecedor não confirmou por escrito frete, fundação e montagem. O deck (R$ 36.000) e a área de apoio (R$ 70.000) continuam iguais, e a reserva continua em 15%.</p>"
         "<p><b>a)</b> Novo bloco 3: 4 × 150.000 + 36.000 + 70.000 = ______________</p><p><b>b)</b> Nova soma dos blocos 1 a 6: 1.010.500 − 682.000 + (a) = ______________</p>"
         "<p><b>c)</b> Reserva a 15%: ______________ &nbsp;&nbsp; <b>d)</b> CAPEX da fase: ______________</p><p><b>e)</b> Que ponto de atenção aparece? ____________________________________________</p>")
   + box("Exercício 3 · Classifique", "<p>Escreva ao lado de cada item o número do bloco (1 a 7), “à parte, somado”, “à parte, não somado” ou “fora desta conta”.</p>"
         + '<div class="grid2" style="font-size:9.6pt">' + "".join(f"<div>{i + 1}. {x} ________</div>" for i, x in enumerate(
             ["Jogo de lençol e toalhas", "Colchão", "Projeto elétrico", "Poço", "Licença de funcionamento", "Fotos do anúncio", "Deck de cada unidade",
              "Lavadora da lavanderia", "Terreno", "Capital de giro", "Ofurô decidido no meio da obra", "Juros do empréstimo da obra"])) + "</div>"))

pg(FICT
   + box("Exercício 4 · A reserva", "<p>Helena pôs a reserva em <b>8%</b>, sendo a primeira obra dela. A soma dos blocos 1 a 6 é R$ 1.010.500.</p>"
         "<p><b>a)</b> Que dois pontos de atenção a ficha mostra? ____________________________________________</p>"
         "<p><b>b)</b> Reserva a 8%: ______________ &nbsp;&nbsp; <b>c)</b> Diferença para a reserva a 15%: ______________</p>"
         "<p><b>d)</b> Escreva a regra de uso em quatro linhas:</p><p>Para quê: ______________________________________________</p><p>Quem autoriza: _________________________________________</p><p>Como se registra: _______________________________________</p><p>Quando se confere: ______________________________________</p>")
   + box("Exercício 5 · Em branco: o seu bloco 2", "<p>Liste as linhas da infraestrutura do <b>seu</b> projeto e a quem você vai pedir cada cotação. É a ponte para a ficha.</p>"
         + tabela(["Linha", "A quem pedir", "Pedido enviado em"], [['<div style="height:6.5mm"></div>', "", ""] for _ in range(7)]), "linha")
   + '<p class="cap">Dica do exercício 5: comece pela concessionária (ponto de energia) e pelo projetista (para quantas unidades a rede será dimensionada).</p>')

pg("<div class='k'>Capítulo 12 · Gabarito comentado</div><h2 style='margin-bottom:3mm'>Gabarito</h2>" + FICT
   + "<h3>Exercício 2</h3><p>a) R$ 706.000 · b) R$ 1.034.500 · c) R$ 155.175 · d) R$ 1.189.675 · e) Frete, fundação e montagem não confirmados por escrito: peça a confirmação ao fornecedor. Se não estiverem incluídos, viram linhas próprias e o número sobe.</p>"
   + "<h3>Exercício 3</h3>"
   + tabela(["Item", "Resposta", "Por quê"], [
       ["1. Jogo de lençol e toalhas", "Bloco 5", "Enxoval: três jogos por cama"], ["2. Colchão", "Bloco 4", "Faz parte da cama, no mobiliário"],
       ["3. Projeto elétrico", "Bloco 1", "Projeto que aprova a obra"], ["4. Poço", "Bloco 2", "Infraestrutura de água"],
       ["5. Licença de funcionamento", "Bloco 6", "Autoriza operar, não construir"], ["6. Fotos do anúncio", "Bloco 6", "Pré-abertura"],
       ["7. Deck de cada unidade", "Bloco 3", "Construção da unidade"], ["8. Lavadora da lavanderia", "Bloco 4", "Equipamento geral"],
       ["9. Terreno", "À parte, não somado", "Capital empregado, anotado ao lado"], ["10. Capital de giro", "À parte, somado", "Entra no investimento total, não no CAPEX"],
       ["11. Ofurô no meio da obra", "Linha nova", "Escopo novo: não sai da reserva; é decisão e linha nova"], ["12. Juros do empréstimo", "Fora desta conta", "Ficam no Pilar 7"]])
   + "<h3>Exercício 4</h3><p>a) Reserva abaixo da faixa citada (menos de 10%) e, com primeira obra, abaixo do teto de 15% que a fonte pede · b) 1.010.500 × 0,08 = R$ 80.840 · c) 151.575 − 80.840 = R$ 70.735 · d) Resposta pessoal: confira se as quatro linhas estão escritas e se o “para quê” não inclui escopo novo nem caixa da operação.</p>"
   + "<h3>Exercício 5</h3><p>Resposta pessoal. Está pronto quando cada linha tem um destinatário e uma data de pedido.</p>")

# ---------------------------------------------------------------- 13 perguntas aos profissionais
PERG = [("Ao engenheiro", ["O preço inclui mão de obra, encargos, administração e lucro (o BDI, benefícios e despesas indiretas)?", "Quanto o frete e a montagem acrescentam neste terreno?",
                           "Como o preço pode mudar até a compra (reajuste)?", "A rede está dimensionada para quantas unidades?", "Quem assina a responsabilidade técnica (ART, anotação de responsabilidade técnica)?",
                           "Qual o custo do m² para o sistema construtivo escolhido, e o que ele inclui? Vale comparar com o custo unitário básico (CUB) do estado?"]),
        ("Ao arquiteto", ["Quais projetos a prefeitura vai pedir, e em que ordem?", "O memorial descritivo está pronto para eu pedir três cotações comparáveis?",
                          "As áreas comuns estão no tamanho certo para esta fase?", "Quem assina o registro de responsabilidade técnica (RRT)?"]),
        ("Ao contador (e ao advogado, na forma de entrada do terreno)", ["Quais são os custos de aquisição do terreno: escritura, imposto de transmissão (ITBI), registro, certidões?",
                                                                          "Que impostos incidem sobre a obra e a compra de equipamentos?", "Compra, permuta, sociedade ou arrendamento: o que muda para mim?"]),
        ("À concessionária e à prefeitura", ["Onde fica o ponto de energia mais próximo, e qual a tensão disponível?", "Quais licenças o projeto precisa, quanto custam e quanto tempo levam?"])]
pg(cab("13", "Capítulo 13 · Leve para a conversa", "O que perguntar <i>aos profissionais</i>",
       "Algumas partes da conta só um profissional responde. Leve estas perguntas, sem número pronto, e anote as respostas com data.")
   + "".join(f"<h3>{t}</h3><ul class='chk'>" + "".join(f"<li>{q}</li>" for q in qs) + "</ul>" for t, qs in PERG)
   + box("Por que sem número", "<p>Itens como BDI, frete em área remota, reajuste e custos de aquisição do terreno não têm valor seguro nas fontes do método. Por isso não damos percentual para eles: a resposta vem do profissional que conhece o seu terreno, o seu sistema construtivo e a sua cidade.</p>"))

# ---------------------------------------------------------------- 14 próxima etapa
pg(cab("14", "Capítulo 14 · A página 6A", "A página 6A e <i>a próxima etapa</i>",
       "Agora é a sua vez: os sete blocos com os seus números, cada linha com origem.")
   + box("Faça agora · O meu CAPEX", "<p>Abra a ficha <b>Faça agora · O meu CAPEX</b> (link na aula). Uma pergunta por tela: a sua situação, o palpite, a fase, um bloco por tela, a reserva com a regra de uso, o giro e o terreno. O resultado vem em cinco partes: o resultado, o que significa, atenção, o que fazer em 30 dias e como verificar. As respostas ficam salvas só no seu aparelho; volte a cada cotação que chegar e gere o PDF de novo.</p>", "escuro")
   + "<h3>Critério de conclusão</h3><ul class='chk'><li>Unidades da fase e do projeto completo informadas, e as tipologias somando as unidades da fase.</li><li>Toda linha dos blocos 1 a 6 com origem: cotação, estimativa, em branco ou não se aplica.</li><li>Reserva maior que zero e a regra de uso nas quatro linhas.</li><li>Para quantas unidades a rede é dimensionada.</li><li>Giro informado e situação do terreno respondida.</li><li>Ação de 30 dias escrita, com prazo, e o PDF da página 6A baixado.</li></ul>"
   + "<p>A primeira versão honesta, com estimativas e linhas em branco nomeadas, já conclui a lição. O degrau e a ação de 30 dias mostram o que falta.</p>"
   + "<h3>Depois da página 6A</h3><ol><li><b>Volte à ficha do Pilar 6</b> e refaça a página 6 com os números do quadro “Como levar para a página 6”. Linhas com cotação levam nota 3; estimativas, nota 1; em branco, “Não sei”.</li><li><b>Abra a Planilha 2 · Investimento</b> com o CAPEX da fase, para seguir para a viabilidade.</li><li><b>No Pilar 7</b> ficam a necessidade de capital, o custo da captação e a frase do pedido.</li></ol>"
   + "<p style='font-size:9.4pt'>Ferramentas extras, se você quiser ir além: a Planilha 1 · Orçamento de Abertura (várias tipologias), a Ferramenta 05 · Orçamento da Cabana (três cotações por item, uma unidade) e a Calculadora de Implantação (cenários e desembolso).</p>"
   + '<p style="font-size:8.4pt;color:var(--cinza);margin-top:3mm">Fontes do método: Volume 05 · Investimento; Pilar 6 · Pré-viabilidade (Trilha 1); Jornada do COMO, Etapas 01, 02 e 04; Volume 06 · Implantação; F01 · CAPEX e Necessidade de Capital. Faixas apresentadas como conferência citada pela fonte, sem base estatística declarada. O caso dos Chalés do Ribeirão, a personagem Helena e todos os seus números são fictícios. Material educativo da Zion Hospitality Business: não é orçamento, projeto, estudo de viabilidade definitivo nem promessa de resultado, e não substitui engenheiro, arquiteto, contador, advogado, prefeitura ou concessionária.</p>')

# ---------------------------------------------------------------- montagem
EXTRA = """
.capa{background:var(--musgo);color:var(--creme);padding:22mm 20mm}
.capa .capa-w{height:100%;display:flex;flex-direction:column;justify-content:space-between;position:relative}
.capa .logo{height:13mm;align-self:flex-start}
.capa h1{font-size:60pt;line-height:1;margin:5mm 0 6mm;font-weight:500} .capa h1 i{color:var(--ouro);font-size:38pt;line-height:1.08;display:block;margin-top:2mm}
.capa .sub{color:var(--areia);font-size:13pt;line-height:1.45;max-width:150mm}
.capa .pub{display:inline-block;margin-top:8mm;border:1px solid var(--ouro);color:var(--ouro);border-radius:99px;padding:2mm 6mm;font-size:10pt;letter-spacing:.06em}
.capa .pe{font-size:8.5pt;color:var(--areia);opacity:.85;max-width:92mm}
.capa .marca{position:absolute;right:-4mm;bottom:-10mm;font-family:Titulo,serif;font-size:170pt;line-height:1;color:var(--ouro);opacity:.14}
table.sum td{font-size:11pt;padding:2.6mm 2mm} table.sum td.sn{font-family:Titulo,serif;color:var(--terra);font-size:14pt;width:14mm}
ol.passos li{margin-bottom:2.2mm}
.diag{display:grid;grid-template-columns:1.25fr 1fr;gap:6mm;margin:4mm 0}
.diag .col{display:flex;flex-direction:column;gap:1.4mm}
.diag .bl{background:var(--creme);border:1px solid var(--areia);border-left:4px solid var(--musgo);padding:1.8mm 3mm;font-size:9.6pt;font-weight:600;border-radius:1.5mm}
.diag .bl.ouro{border-left-color:var(--ouro)}
.diag .tot1,.diag .tot2{background:var(--musgo);color:var(--creme);padding:2.6mm 3mm;border-radius:2mm;font-family:Titulo,serif;font-size:15pt}
.diag .tot2{background:var(--terra)}
.diag small{display:block;font-family:Texto,sans-serif;font-size:8pt;color:var(--ouro);letter-spacing:.06em}
.diag .tot2 small{color:var(--creme)}
.diag .mais{border:1.5px dashed var(--terra);padding:2mm 3mm;border-radius:2mm;font-weight:700;font-size:10pt}
.diag .mais small{color:var(--terra)}
.diag .lado{display:flex;flex-direction:column;gap:3mm;justify-content:center}
.diag .fora{border:1px dashed var(--terra);border-radius:2.5mm;padding:3mm 3.5mm;font-size:9.3pt;background:#fff}
.diag .fora b{display:block;font-family:Titulo,serif;font-size:13pt;color:var(--terra)}
.infra{border:1px solid var(--areia);border-radius:3mm;padding:5mm;background:var(--creme);margin:2mm 0 3mm}
.infra .poste{display:inline-block;background:var(--musgo);color:var(--creme);padding:1.5mm 3mm;border-radius:1.5mm;font-size:9pt;font-weight:700}
.infra .poste small{color:var(--ouro);margin-left:2mm}
.infra .tronco{margin:3mm 0;height:7mm;background:var(--ouro);border-radius:1mm;color:var(--musgo);font-size:9pt;font-weight:700;display:flex;align-items:center;padding-left:3mm}
.infra .uns{display:grid;grid-template-columns:repeat(6,1fr);gap:3mm}
.infra .u{height:13mm;border:1.5px dashed var(--terra);border-radius:2mm;display:flex;align-items:center;justify-content:center;font-family:Titulo,serif;font-size:16pt;color:var(--terra);background:#fff}
.infra .u.f{background:var(--musgo);border:1.5px solid var(--musgo);color:var(--creme)}
.infra .leg{display:flex;gap:6mm;margin-top:3mm;font-size:8.6pt}
.infra .leg i{display:inline-block;width:3.5mm;height:3.5mm;border:1.5px dashed var(--terra);margin-right:1.5mm;vertical-align:-.5mm;background:#fff}
.infra .leg i.f{background:var(--musgo);border:1.5px solid var(--musgo)}
"""
corpo = ""
for i, (conteudo, classe) in enumerate(paginas, 1):
    rod = "" if classe == "capa" else f'<div class="rod"><span>{RODAPE}</span><span class="p">CAPEX · Pilar 6 · {i}</span></div>'
    corpo += f'<section class="pg {classe}"><div class="in">{conteudo}</div>{rod}</section>\n'
html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>CAPEX · Aprenda o passo a passo para calcular quanto custa o seu projeto inteiro</title>'
        f'<style>{css(OUT)}{EXTRA}</style></head><body>\n{corpo}</body></html>')
html = html.replace("R$ ", "R$\u00a0")
assert "—" not in html and " – " not in html, "travessão no texto"
(OUT / "ebook.html").write_text(html, encoding="utf-8")
print("ok", OUT / "ebook.html", len(paginas), "páginas")

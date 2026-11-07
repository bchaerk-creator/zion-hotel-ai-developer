"""Gera os specs dos 8 tutoriais das ferramentas Faça agora (Marco Zero e Pilares 1 a 7)."""
import json, pathlib
B = "http://localhost:8790/trilha1/"
OUT = pathlib.Path(__file__).parent / "specs"

def card(t, s): return {"card": {"t": t, "s": s}}
def start(slug, campos):  # tela inicial + começar
    acts = [{"goto": B + slug + "/"}, {"show": "h1", "wait": 1200}, {"fillStart": campos}]
    acts.append({"click": "#comecar" if slug != "marco-zero" else "#vai", "wait": 900})
    return acts
RESULT_COMMON = [
    ("Primeiro, os alertas", "A página começa pelos alertas: o que, nas suas respostas, pede atenção antes de qualquer conta."),
    ("As contas e as leituras", "Depois, as contas e as leituras: o que a ferramenta calculou com o que você digitou, e o que cada número significa."),
    ("A nota por item", "A nota por item mostra, pergunta a pergunta, a qualidade da sua resposta: medido vale mais do que estimado."),
    ("O ponto mais frágil", "E o ponto mais frágil: a resposta que mais pesa contra o projeto hoje. É por ela que você começa a trabalhar."),
    ("A leitura", "A leitura do método junta tudo em um veredito claro: seguir, seguir com condições, ajustar ou esperar."),
]
MENTOR = ("O mentor virtual", "Se quiser uma segunda opinião, peça a leitura do mentor virtual: ele comenta as suas respostas com a lógica do método Zion. Não substitui a equipe; orienta.")
FECHO = [
    ("O seu critério para parar", "Antes de baixar, dois compromissos. O critério para parar: qual fato, se aparecer, faz você parar ou mudar de rumo."),
    ("O seu Compromisso de 7 dias", "E o compromisso de sete dias: uma ação, um responsável, um prazo e a evidência que você vai ter na mão. É o que transforma a aula em movimento."),
]

def result_scenes(nome_pagina, prox, pdf_txt):
    sc = []
    for h, say in RESULT_COMMON:
        sc.append({"say": say, "actions": [{"text": h, "sel": "h2", "wait": 3200}]})
    sc.append({"say": MENTOR[1], "actions": [{"text": MENTOR[0], "sel": "h2", "wait": 1200}, {"show": "#mentor-pedir", "wait": 2500}]})
    for h, say in FECHO:
        sc.append({"say": say, "actions": [{"text": h, "sel": "h2", "wait": 3500}]})
    sc.append({"say": f"No fim, três saídas: baixar a sua {nome_pagina} em PDF, que é uma página do seu Dossiê de Desenvolvimento; enviar ao Land Bank da Zion, para a página chegar ao seu cadastro; e seguir para o próximo pilar. {prox}",
               "actions": [{"show": "#pdf", "wait": 2500}, {"show": "#zlb-btn", "wait": 2500}, {"show": "#proxima", "wait": 2500}]})
    return sc

def ficha(slug, titulo, sub, intro, campos, q1, bloco_narr, auto_n, nome_pagina, prox, outro, pick=0, q1_answer=None):
    sc = [{"say": intro, "actions": [card(titulo, sub)]}]
    sc.append({"say": "Na tela inicial, você preenche nome, e-mail e a cidade do terreno. Use o mesmo e-mail da área de membros: é por ele que a página chega ao seu cadastro no Land Bank. Depois, Começar.",
               "actions": start(slug, campos)})
    # primeira pergunta, explicada
    sc.append({"say": q1["say"], "actions": [{"show": ".pergunta", "wait": 1500}] + q1.get("extra", []) +
               [{"text": "Por que perguntamos isso", "sel": "h3", "wait": 2500}, {"text": "Onde conseguir essa informação", "sel": "h3", "wait": 2500}, {"text": "Exemplo ilustrativo", "sel": "h3", "wait": 2200}]})
    sc.append({"say": "Cada resposta tem uma origem: medi eu mesmo, alguém me passou, ou é estimativa minha. Marque com honestidade, porque a nota depende disso. Se não souber, toque em Não sei: vira pendência, não reprovação. Vamos responder e avançar.",
               "actions": [{"show": "label.op", "wait": 1500}, {"show": "#ns", "wait": 1200}, {"auto": 1, "pace": 500, "pick": pick, "answers": ([q1_answer] if q1_answer else [])}]})
    # blocos restantes
    for item in bloco_narr:
        say, n = item[0], item[1]; ans = item[2] if len(item) > 2 else []
        sc.append({"say": say, "actions": [{"auto": n, "pace": 420, "pick": pick, "answers": ans}]})
    sc += result_scenes(nome_pagina, prox, "")
    sc.append({"say": outro, "actions": [card(f"Próximo passo: {prox}", "Club Zion Collection · Trilha de Desenvolvimento")]})
    return {"voice": "pt-BR-FranciscaNeural", "scenes": sc}

CAMPOS = {"#nome": "Ana Exemplo", "#email": "ana@exemplo.com", "#cidade": "Urubici", "#uf": "SC"}
SPECS = {}

SPECS["ficha-pilar2"] = ficha("aula2", "Pilar 2 · Ficha do Mercado", "Quem vende o mesmo que você, quanto enche, quanto paga e quantas unidades o destino compra",
    "Olá! Este é o tutorial da Ficha do Mercado, a ferramenta Faça agora do Pilar dois. Ela transforma a sua pesquisa de comparáveis em diária, ocupação e capacidade do destino: os números que depois entram na Planilha dois e no pitch.",
    CAMPOS,
    {"say": "A primeira pergunta: quantas unidades somam os seus comparáveis. Comparável é quem vende exatamente o mesmo que você pretende vender, no seu raio. Cada tela tem três apoios: por que perguntamos isso, onde conseguir a informação, e um exemplo ilustrativo com a Marina, a personagem que acompanha a Trilha."},
    [("O bloco Quanto enche e quanto paga pede a ocupação de sexta e sábado e de domingo a quinta, a diária do meio nos dois casos, e a distância entre a diária mais cara e a mais barata do seu raio. Tudo isso você mede nos calendários dos comparáveis, não no achismo.", 5, [70, 35, 614, 420, 3]),
     ("A curva do ano: quantos meses de alta, quanto os comparáveis enchem na alta, quantos meses fracos, quanto enchem nos fracos e nos médios. É a sazonalidade que vai para o cenário conservador.", 5, [4, 85, 3, 25, 50]),
     ("E o bloco Quantas unidades o destino compra: quanto a procura deve crescer até você abrir, quantas unidades estão em obra ou em licença na região, e quantas você pensava em abrir. É aqui que a ferramenta diz se o destino absorve o seu projeto.", 3, [20, 12, 3])],
    14, "Ficha do Mercado", "Pilar 3, Produto e tipologias.",
    "Com a Ficha do Mercado pronta, você tem a diária e a ocupação com fonte. Leve esses números para a Planilha dois, aba Modelo de renda. Até a próxima.", q1_answer="96")

SPECS["ficha-pilar3"] = ficha("aula3", "Pilar 3 · Ficha do Produto", "Para quem, o que ele vive, a promessa, a unidade e o preço como hipótese",
    "Olá! Este é o tutorial da Ficha do Produto, a ferramenta Faça agora do Pilar três. Ela define para quem você constrói, o que o hóspede vive, a promessa em uma frase, a tipologia e a diária como hipótese.",
    CAMPOS,
    {"say": "A primeira pergunta é sobre o público principal e por que motivo ele viaja. Aqui a resposta é em texto: escreva como você explicaria para um sócio. Os três apoios ajudam: por que perguntamos, onde conseguir e o exemplo da Marina."},
    [("O bloco Para quem segue com quem pode vir de domingo a quinta e quem fica de fora. Depois, O que ele vive: o momento assinatura, em uma frase, com horário e quem prepara, e os requisitos que esse momento precisa cumprir: só existe aqui, acontece sem você, cabe numa frase e é fotografável.", 4, ["Casais que trabalham remoto e vêm de terça a quinta pelo silêncio e pela internet boa", "Grupos grandes e festas: o produto é de casal, sem estrutura para eventos", "Café servido na varanda às 8h, com vista para o vale, preparado pela anfitriã"]),
     ("A promessa: a sua frase em três partes e as provas dela. E os dois testes que não custam nada: o teste do vizinho e o teste dos cinco segundos com cinco pessoas. A ferramenta pergunta o que aconteceu em cada um.", 4, ["Dormir sob as estrelas, com banheira quente e café na varanda, a 40 minutos do aeroporto", "Banheira com vista em todas as unidades\nCafé feito na hora pela anfitriã\nAcesso asfaltado até a porteira"]),
     ("A unidade: qual tipologia sobrou nos três filtros, terreno, capital e público; a área interna; e quantas unidades abrem na primeira fase. E o preço como hipótese: a diária média da região e a sua hipótese de diária. Esses números vão direto para as planilhas.", 5, [28, 3, 580, 650])],
    14, "Ficha do Produto", "Pilar 4, Modelo de negócio.",
    "Com a Ficha do Produto, você tem a tipologia, a metragem, as unidades da fase um e a diária como hipótese. São as premissas da Planilha um e da Planilha dois. Até a próxima.", q1_answer="Casais de Florianópolis e Curitiba, de 30 a 55 anos, que viajam a dois em feriados e fins de semana para descansar na serra")

SPECS["ficha-pilar4"] = ficha("pilar4", "Pilar 4 · Modelo de Negócio", "Renda, venda ou híbrido: como o projeto ganha dinheiro",
    "Olá! Este é o tutorial do Modelo de Negócio, a ferramenta Faça agora do Pilar quatro. Ela ajuda a decidir como o projeto ganha dinheiro: renda, venda ou híbrido, e em que degrau você começa.",
    CAMPOS,
    {"say": "A primeira pergunta: com o seu imóvel, você vai alugar, hospedar ou vender. Parece simples, mas define todo o resto. Leia os três apoios antes de responder."},
    [("O bloco Em que negócio você está pergunta quais serviços o seu produto tem. Depois, o mapa dos modelos: qual perfil mais parece com você, por onde o projeto começa no mapa, e se você sabe para quem vai vender, do balcão para fora.", 4),
     ("O modelo de renda: em que degrau da escada o seu produto está na fase um, e se você consegue estruturar e operar bem esse degrau. A conta do cem por cento: unidades da fase um, ocupação medida, diária média, em que cenário o projeto fica de pé, e quem opera.", 7, [3, 45, 580]),
     ("O modelo de venda: se você pensa em vender alguma parte, de que forma e quantas unidades. E a decisão: renda, venda ou híbrido.", 2)],
    14, "Modelo de Negócio", "Pilar 5, Masterplan faseado.",
    "A página do Pilar quatro tem um detalhe a mais: o simulador. Você equaliza unidades, ocupação e diária nos controles e vê os três cenários mudarem na hora. É o ensaio da Planilha dois. Até a próxima.")

SPECS["ficha-pilar5"] = ficha("pilar5", "Pilar 5 · Masterplan faseado", "Onde nunca, o que precisa existir, o que cabe e o que entra na fase um",
    "Olá! Este é o tutorial do Masterplan faseado, a ferramenta Faça agora do Pilar cinco. Ela organiza o terreno: o que nunca será construído, o que precisa existir, o que cabe, e o que entra na fase um.",
    CAMPOS,
    {"say": "A primeira pergunta é a área total da matrícula do terreno. Medida no documento, não de memória. Depois, quanto dessa área você pode usar, descontando o que a lei e o terreno não permitem."},
    [("Passo um, Onde nunca: o que nunca será construído, zona por zona, e por quê; quanto mede o seu nunca; e quais gestos ele já tem: marcado no terreno, fotografado, cláusula pedida ao advogado.", 4, [35000, "A mata ciliar do córrego e o topo do morro, por lei e pela paisagem; o bosque de araucárias, por decisão nossa", 12000]),
     ("Passo dois, O que precisa existir: unidades da fase um e do projeto completo, a área fechada de cada unidade, o deck ou varanda, e a área de apoio da fase um e do projeto completo. Esses números alimentam a aba Massas da Planilha dois.", 6, [3, 5, 28, 8, 30, 34]),
     ("E os testes de campo: o que da lista do que quase sempre falta já está resolvido; se você simulou no papel um dia de troca de hóspede; se o caminho do hóspede cruza com o do serviço; se estaqueou as unidades e caminhou às sete da manhã e às cinco da tarde; e a taxa de ocupação da zona.", 6)],
    16, "Masterplan faseado", "Pilar 6, Pré-viabilidade.",
    "Com o Masterplan faseado, você sabe o que cabe e o que entra primeiro. Leve as metragens para a Planilha dois, aba Massas. Até a próxima.")

SPECS["ficha-pilar6"] = ficha("pilar6", "Pilar 6 · Pré-viabilidade", "A folha de oito linhas, os três cenários e o tempo de volta",
    "Olá! Este é o tutorial da Pré-viabilidade, a ferramenta Faça agora do Pilar seis. É a versão rápida da conta: a folha de oito linhas, os três cenários e o tempo de volta do dinheiro. As Planilhas um e dois são a versão completa.",
    CAMPOS,
    {"say": "A primeira pergunta é um exercício: antes da conta, quanto você acha que custa abrir a porta da sua fase um. Escreva o seu palpite. No fim, a ferramenta compara com a conta, e a diferença costuma ensinar mais do que o número."},
    [("A fase um: quantas unidades abre e as linhas da folha: a unidade, o deck, água e esgoto ou fossa, mobiliário, equipamentos e enxoval, piso, licenças e projetos, e a reserva para imprevisto. Em cada linha, a origem: cotação escrita, fornecedor sem papel, ou referência da Zion marcada como referência.", 6),
     ("A infraestrutura comum, o capital de giro em meses de custo, e o valor do terreno. Depois, a receita: a diária que entra na conta e a ocupação em três cenários: conservador, base, e otimista. E a margem operacional, que aqui é a de referência da Zion, uma simplificação.", 6),
     ("Por fim, em que momento do calendário você pretende abrir. Começar no começo da alta muda o primeiro ano inteiro.", 2)],
    14, "Pré-viabilidade", "Pilar 7, Capital e Dossiê.",
    "Esta página tem o simulador: equalize a conta nos controles e veja o resultado mudar. Depois, faça a versão completa nas Planilhas um e dois e volte aqui para refazer a página seis com os números delas. Até a próxima.")

SPECS["ficha-pilar7"] = ficha("pilar7", "Pilar 7 · Dossiê de Desenvolvimento", "As três perguntas do capital, o pedido, as seis fontes e a decisão",
    "Olá! Este é o tutorial do Dossiê de Desenvolvimento, a ferramenta Faça agora do Pilar sete. Ela fecha a Trilha: as três perguntas do capital, o pedido exato, as seis fontes, dinheiro ou sócio, e a decisão de avançar, ajustar ou parar. E junta as páginas zero a sete no Dossiê completo.",
    CAMPOS,
    {"say": "As três perguntas do capital abrem a ferramenta: se o dinheiro aparecesse amanhã, você sabe o que construir, quantas unidades e para quem? Sabe a diária que o seu produto sustenta, com dado? Sabe em quanto tempo o dinheiro volta, nos três cenários? Um sim sem documento vale um não."},
    [("O pedido, linha por linha: o investimento da fase um sem o giro, o capital de giro, o que ainda falta pagar do terreno, quanto custa buscar o dinheiro, e quanto você mesmo põe, já contratado. É o pedido que vai para o slide doze do pitch.", 7),
     ("As seis fontes: quanto você pode perder sem comprometer a sua vida; para cada fonte, recurso próprio, banco, investidor, sócio, pré-venda e parceria com quem opera, se está disponível, possível ou fora; e se você aceita terreno em garantia ou aval pessoal.", 3),
     ("Dinheiro ou sócio: o que te falta de verdade e, se precisar de sócio, de que tipo. As sete páginas lado a lado: qual é a mais fraca e o que se repete na coluna depende de. E a decisão: avançar, ajustar ou parar, e qual fato mudaria essa decisão.", 6)],
    17, "Dossiê de Desenvolvimento", "o cadastro no Zion Land Members e o Kit do Investidor.",
    "Com o Dossiê completo, você entra no Kit do Investidor para transformar a conta em teaser, one-pager e pitch, e cadastra o terreno no Zion Land Members com tudo anexado. A equipe Zion avalia cada caso. Parabéns por chegar até aqui.")

# Marco Zero (estrutura própria)
SPECS["ficha-marco-zero"] = {"voice": "pt-BR-FranciscaNeural", "scenes": [
    {"say": "Olá! Este é o tutorial do Diagnóstico prévio, a ferramenta Faça agora do Marco Zero. Em quatro telas, ela diz onde você está na jornada, qual é a sua dor principal e por onde começar.",
     "actions": [card("Marco Zero · Diagnóstico prévio", "Onde você está, qual é a sua dor e por onde começar")]},
    {"say": "Preencha nome, e-mail e a cidade do terreno ou da ideia. Use o mesmo e-mail da área de membros. Depois, Começar.",
     "actions": [{"goto": B + "marco-zero/"}, {"show": "h1", "wait": 1200}, {"fillStart": {"#nome": "Ana Exemplo", "#email": "ana@exemplo.com", "#cidade": "Urubici, SC"}}, {"click": "#vai", "wait": 900}]},
    {"say": "Primeira tela: qual destas frases mais parece com você hoje. Tenho um terreno e ainda não hospedo ninguém; tenho uma ideia ou o capital e ainda não tenho o terreno; ou já opero e quero crescer. Escolha a mais honesta.",
     "actions": [{"show": ".pergunta", "wait": 1500}, {"show": "label.op", "wait": 1500}, {"auto": 1, "pace": 500}]},
    {"say": "Segunda tela: o que te trouxe até aqui. São as quatro dores que a Zion mais ouve de quem tem terreno. Terceira: quais das cinco perguntas, antes de investir um real, você já responde. Marque só as que você responde com documento ou conta na mão.",
     "actions": [{"show": ".pergunta", "wait": 1500}, {"auto": 1, "pace": 500}, {"show": ".pergunta", "wait": 2500}, {"auto": 1, "pace": 500}]},
    {"say": "Quarta tela: onde você está na jornada de quatro etapas e sete pilares. A ferramenta usa a sua resposta para apontar o pilar em que você deve concentrar mais atenção.",
     "actions": [{"show": ".pergunta", "wait": 2500}, {"auto": 1, "pace": 500}]},
    {"say": "E o resultado: a sua jornada, o seu ponto mais frágil, a sua dor, e a primeira ação de sete dias, com prazo. É a página zero do seu Dossiê de Desenvolvimento.",
     "actions": [{"text": "A sua jornada", "sel": "h2", "wait": 2500}, {"text": "O seu ponto mais frágil", "sel": "h2", "wait": 2500}, {"text": "A sua dor", "sel": "h2", "wait": 2000}, {"text": "A sua primeira ação de 7 dias", "sel": "h2", "wait": 3000}]},
    {"say": "Abaixo, os próximos passos com a Zion, o botão para baixar o diagnóstico em PDF e o envio ao Land Bank. Depois, siga para o Pilar um, Território e destino. Boa jornada.",
     "actions": [{"text": "Os seus próximos passos com a Zion", "sel": "h2", "wait": 2500}, {"show": "#pdf", "wait": 2000}, {"show": "#zlb-btn", "wait": 2000}]},
    {"say": "Abra o Mapa de direcionamento para ver as tarefas de cada etapa. Até a próxima ferramenta.",
     "actions": [card("Próximo passo: Pilar 1 · Território e destino", "Club Zion Collection · Trilha de Desenvolvimento")]},
]}

# Pilar 1 · Leitor de Território (CEP + grupos de perguntas por tela)
SPECS["ficha-pilar1"] = {"voice": "pt-BR-FranciscaNeural", "scenes": [
    {"say": "Olá! Este é o tutorial do Leitor de Território, a ferramenta Faça agora do Pilar um. Com o CEP e algumas perguntas sobre acesso, infraestrutura, vizinhança, terreno e paisagem, ela gera a Ficha do Território: o que o seu chão permite e o que falta documentar.",
     "actions": [card("Pilar 1 · Leitor de Território", "Acesso, infraestrutura, vizinhança, terreno e paisagem")]},
    {"say": "Na tela inicial: nome, e-mail e o CEP do terreno. O CEP ajuda a ferramenta a situar a região. Depois, Começar.",
     "actions": [{"goto": B + "territorio/"}, {"show": "h1", "wait": 1200}, {"fillStart": {"#nome": "Ana Exemplo", "#email": "ana@exemplo.com", "#cep": "88650-000"}}, {"click": "#comecar", "wait": 1200}]},
    {"say": "A primeira tela é o Acesso: como se chega ao terreno, quanto de estrada de terra, como fica com chuva forte, se o caminho passa por vizinho, e as distâncias até a cidade com mercado e até o aeroporto ou a rodoviária. Cada pergunta é de marcar.",
     "actions": [{"text": "Acesso", "sel": "h2", "wait": 1500}, {"text": "Como se chega ao terreno", "sel": "legend", "wait": 2500}, {"text": "E com chuva forte", "sel": "legend", "wait": 2500}, {"auto": 1, "pace": 500}]},
    {"say": "Depois, Infraestrutura: energia, água, esgoto, internet e sinal. E Vizinhança: o que existe em volta e o que isso muda no seu produto.",
     "actions": [{"text": "Infraestrutura", "sel": "h2", "wait": 2500}, {"auto": 1, "pace": 500}, {"text": "Vizinhança", "sel": "h2", "wait": 2500}, {"auto": 1, "pace": 500}]},
    {"say": "Terreno e paisagem: relevo, tamanho aproximado, o que o seu terreno tem e o que a região tem. Marque tudo o que se aplica: a paisagem é o seu produto.",
     "actions": [{"text": "Terreno e paisagem", "sel": "h2", "wait": 2000}, {"text": "O que o seu terreno tem", "sel": "legend", "wait": 2500}, {"auto": 4, "pace": 450}]},
    {"say": "No fim, a Ficha do Território: a leitura do que o seu chão permite, as pendências de documento e o que verificar na prefeitura. Baixe em PDF, é a página um do Dossiê, e envie ao Land Bank da Zion. Depois, siga para o Pilar dois, Mercado e demanda.",
     "actions": [{"show": "h1", "wait": 2500}, {"scroll": 500, "wait": 2500}, {"scroll": 600, "wait": 2500}, {"show": "#pdf", "wait": 2000}, {"show": "#zlb-btn", "wait": 2000}]},
    {"say": "Até a próxima ferramenta.", "actions": [card("Próximo passo: Pilar 2 · Mercado e demanda", "Club Zion Collection · Trilha de Desenvolvimento")]},
]}

SPECS["ficha-pilar1"] = ficha("aula1", "Pilar 1 · Ficha do Território", "Da matrícula à área que você pode usar, os preços, o que o lugar aguenta e o que pode travar",
    "Olá! Este é o tutorial da Ficha do Território, a ferramenta Faça agora do Pilar um. Ela transforma a matrícula do seu terreno na área que você realmente pode usar, mostra quanto o lugar aguenta e o que pode travar o projeto antes de qualquer desenho.",
    CAMPOS,
    {"say": "A primeira pergunta: qual é o tamanho do terreno, do jeito que está escrito na matrícula, em metros quadrados. Cada tela tem três apoios: por que perguntamos isso, onde conseguir a informação, e um exemplo ilustrativo com a Marina, a personagem que acompanha a Trilha."},
    [("O bloco Da matrícula à área que você pode usar continua descontando o que não entra na conta: área de preservação, reserva legal, encosta forte, recuos e faixas, e o espaço que o projeto vai precisar para serviço. O que sobra é a área útil de verdade.", 5, [12000, 10000, 5000, 2000, 1500]),
     ("Depois, Os preços do terreno: quanto vale o terreno e quanto você imagina investir no total. Essa relação diz se a terra pesa demais na conta.", 2, [600000, 1800000]),
     ("O bloco O que o lugar aguenta: quantas unidades cabem na área útil com espaço e caminhos, para quantas dá água, energia e esgoto, e a partir de quantas um hóspede começa a ver ou ouvir o outro. O menor desses três números é o seu teto.", 3, [6, 8, 5]),
     ("Por fim, O que pode travar: quais documentos você já tem na mão, como matrícula atualizada, CAR, zona confirmada e consulta prévia. E a sua leitura: seguir, renegociar, investigar antes ou trocar de terreno.", 2)],
    13, "Ficha do Território", "Pilar 2, Mercado e demanda.",
    "Com a Ficha do Território pronta, você sabe a área que pode usar, o teto de unidades e o que ainda falta de papel. Esses números entram no Masterplan e na Planilha dois. Até a próxima.", q1_answer="50000")

OUT.mkdir(exist_ok=True)
import sys
only = set(sys.argv[1:])
for k, v in SPECS.items():
    if only and k not in only: continue
    json.dump(v, open(OUT / f"{k}.json", "w"), ensure_ascii=False, indent=0)
print("specs:", [k for k in sorted(SPECS) if not only or k in only])

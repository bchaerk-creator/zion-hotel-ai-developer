"""Gera o HTML do resumo da aula do Módulo 6 (Compras, estoque e manutenção) e o TXT do prompt de IA.
Depois, src/render_pdf.js imprime o HTML em PDF (capa + 8 páginas A4).
Uso: python3 -I src/build_resumo.py <pasta-build>
Saídas: <pasta-build>/resumo.html e docs/trilha2/materiais/Modulo-6-Prompt-de-IA.txt
Os números do exemplo saem de tests (logic.js e planilha); aqui ficam escritos e são conferidos pelo teste de conformidade do REGISTRO."""
import sys, pathlib, re
B = pathlib.Path(sys.argv[1]); B.mkdir(parents=True, exist_ok=True)
HERE = pathlib.Path(__file__).resolve().parent; LICAO = HERE.parent
REPO = LICAO.parents[2]; F = REPO / "docs/assets/fonts"; BR = REPO / "docs/brand"
MAT = REPO / "docs/trilha2/materiais"; MAT.mkdir(parents=True, exist_ok=True)
URL_PROMPT = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/trilha2/materiais/Modulo-6-Prompt-de-IA.txt"

md = (LICAO / "PROMPT_IA.md").read_text(encoding="utf-8")
bloco = re.search(r"```\n(.*?)```", md, re.S).group(1).strip()
txt = ("PROMPT DE IA · REVISAR A MATRIZ DE COMPRAS E MANUTENÇÃO\n"
       "Zion Hotel Academy · Jornada de Gestão · Módulo 6 · Compras, estoque e manutenção\n\n"
       "Como usar: exporte a sua Matriz de Compras e Manutenção em PDF (ou copie as abas da planilha), abra qualquer assistente de IA, "
       "cole o prompt abaixo inteiro e, logo depois, cole o conteúdo da Matriz. O assistente não conhece os fornecedores da sua região nem substitui o "
       "profissional de manutenção: ele confere a lógica e faz perguntas. Não cole dados pessoais de hóspedes, contatos de fornecedores nem senhas.\n\n"
       "----- COPIE DAQUI PARA BAIXO -----\n\n" + bloco + "\n\n----- FIM DO PROMPT -----\n\n"
       "Depois da revisão, anote em duas linhas, na aba Rotina e checklist da planilha, o que mudou e por quê.\n"
       "Conteúdo educacional. Não é promessa de renda, retorno, ocupação ou resultado.\n")
(MAT / "Modulo-6-Prompt-de-IA.txt").write_text(txt, encoding="utf-8")

CSS = f"""
@font-face{{font-family:Cormorant;src:url('{(F/'cormorant.woff2').as_uri()}')}} @font-face{{font-family:Cormorant;font-style:italic;src:url('{(F/'cormorant-italic.woff2').as_uri()}')}} @font-face{{font-family:Aventa;src:url('{(F/'aventa.woff2').as_uri()}')}}
:root{{--musgo:#1B2117;--verde:#16261C;--creme:#FEF5F0;--areia:#DED6BF;--terra:#8B714E;--ouro:#C9B37E;--texto:#1B2117;--cinza:#5A5F55}}
@page{{size:A4;margin:0}} *{{box-sizing:border-box}}
body{{margin:0;font-family:Aventa,Arial,sans-serif;color:var(--texto);background:#fff;font-size:10.4pt;line-height:1.38}}
.pg{{width:210mm;min-height:297mm;padding:20mm 20mm 20mm;page-break-after:always;position:relative}}
.pg:last-child{{page-break-after:auto}}
.capa{{background:var(--musgo);color:var(--creme);display:flex;flex-direction:column;justify-content:space-between;padding-top:22mm}}
.capa img{{height:16mm}} .capa .k{{color:var(--ouro);letter-spacing:.2em;text-transform:uppercase;font-weight:700;font-size:10pt}}
.capa h1{{font-family:Cormorant,serif;font-weight:500;font-size:50pt;line-height:1.02;margin:6mm 0 5mm}} .capa h1 i{{color:var(--ouro)}}
.capa p{{color:var(--areia);font-size:13pt;max-width:140mm}}
h2{{font-family:Cormorant,serif;font-weight:500;font-size:25pt;line-height:1.1;margin:0 0 3.5mm;color:var(--verde)}}
h3{{font-size:10pt;letter-spacing:.14em;text-transform:uppercase;color:var(--terra);margin:4.5mm 0 1.8mm}}
p{{margin:0 0 2.6mm}} ul,ol{{margin:0 0 2.6mm;padding-left:5mm}} li{{margin-bottom:1mm}}
.cita{{font-family:Cormorant,serif;font-style:italic;font-size:15pt;line-height:1.22;border-left:3px solid var(--ouro);padding-left:6mm;margin:3.2mm 0;color:var(--verde)}} .cita small{{display:block;font-family:Aventa,sans-serif;font-style:normal;font-size:8.5pt;color:var(--cinza);margin-top:1.5mm;letter-spacing:.1em;text-transform:uppercase}}
table{{width:100%;border-collapse:collapse;font-size:9.1pt;margin:2.2mm 0 3mm;line-height:1.3}} th,td{{text-align:left;padding:1.3mm 2mm;border-bottom:1px solid var(--areia);vertical-align:top}} th{{background:var(--musgo);color:var(--creme);font-weight:600}}
td.n,th.n{{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}} tr.tot td{{background:#F6F1E6;font-weight:700}} tr.sub td{{color:var(--cinza)}}
.ex{{background:#F6F1E6;border:1px solid var(--areia);border-radius:4mm;padding:3.8mm 5mm;margin:3mm 0}} .ex.compacto table{{font-size:8.7pt}} .ex.compacto td,.ex.compacto th{{padding:1.1mm 1.8mm}} .ex b.rot{{display:block;font-size:9pt;letter-spacing:.14em;text-transform:uppercase;color:#A0522D;margin-bottom:2mm}} .ex table{{background:#fff}}
.caixa{{border:1px dashed var(--terra);border-radius:4mm;padding:3.5mm 5.5mm;margin:3.5mm 0}} .caixa h3{{margin-top:0}}
.rod{{position:absolute;left:20mm;right:20mm;bottom:10mm;font-size:8.5pt;color:var(--cinza);display:flex;justify-content:space-between;gap:8mm;border-top:1px solid var(--areia);padding-top:2mm}}
.num{{font-family:Cormorant,serif;font-size:34pt;color:var(--ouro);line-height:1}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:3.5mm;margin:2mm 0 3mm}} .grid3{{grid-template-columns:1fr 1fr 1fr}} .card{{border:1px solid var(--areia);border-radius:3mm;padding:2.6mm 3.2mm;font-size:9.5pt}} .card b{{display:block;color:var(--verde);margin-bottom:.8mm}} .card small{{color:var(--cinza);font-size:9pt;line-height:1.32;display:block}}
.fonte{{font-size:9pt;color:var(--cinza)}} .ref{{display:inline-block;background:var(--areia);color:var(--musgo);font-size:8.5pt;padding:.3mm 2mm;border-radius:2mm;letter-spacing:.06em;text-transform:uppercase}}
.casc li{{margin-bottom:.6mm}} .casc b{{color:var(--verde)}}
.check{{font-size:9.7pt;line-height:1.34}} .check li{{margin-bottom:.9mm}} .check b{{color:var(--verde)}}
"""
ROD = '<div class="rod"><span>Zion Hotel Academy · Jornada de Gestão · Módulo 6</span><span>Conteúdo educacional. Não é promessa de renda, retorno, ocupação ou resultado.</span></div>'
def tr(cells, cls=""): return f'<tr class="{cls}">' + "".join(cells) + "</tr>"
def tab(cab, linhas, larg=None, num=()):
    def th(i, c):
        a = ' class="n"' if i in num else ""
        if larg and larg[i]: a += ' style="width:%s"' % larg[i]
        return "<th%s>%s</th>" % (a, c)
    h = "<table><tr>" + "".join(th(i, c) for i, c in enumerate(cab)) + "</tr>"
    for l in linhas:
        cls = l[-1] if isinstance(l[-1], str) and l[-1] in ("tot", "sub") else ""
        cel = l[:-1] if cls else l
        h += tr([f'<td class="n">{c}</td>' if i in num else f"<td>{c}</td>" for i, c in enumerate(cel)], cls)
    return h + "</table>"
ITENS = [("1", "Café da manhã e cestas (insumos)*", "R$ 1.260", "32,3%", "R$ 7,24", "R$ 8,40", "28,00 → 25,50", "R$ 112,50", "vou fechar"),
         ("2", "Lavanderia do enxoval", "R$ 900", "23,1%", "R$ 5,17", "R$ 6,00", "3,00 → 2,60", "R$ 120,00", "tem"),
         ("3", "Amenidades", "R$ 780", "20,0%", "R$ 4,48", "R$ 5,20", "10,40 → 8,90", "R$ 112,50", "vou fechar"),
         ("4", "Gás do aquecimento da água", "R$ 720", "18,5%", "R$ 4,14", "R$ 4,80", "120 → 112", "R$ 48,00", "sem contrato"),
         ("5", "Reposição de enxoval", "R$ 240", "6,2%", "R$ 1,38", "R$ 1,60", "120 → 98", "R$ 44,00", "vou fechar"),
         ("", "<b>Total</b>", "<b>R$ 3.900</b>", "100%", "<b>R$ 15,17</b>**", "", "", "<b>R$ 437,00</b>", "", "tot")]
ESTOQUE = [("Kit de amenidades", "25", "7 + 7", "14", "6", "12", "ok"), ("Papel higiênico (rolo)", "100", "5 + 7", "30", "24", "40", "<b>pedir 110</b>"),
           ("Botijão de gás de 13 kg", "2", "2 + 7", "2", "1", "1", "ok"), ("Café em pó (500 g)", "8", "3 + 7", "6", "2", "3", "ok")]
CAL = [("jan", "Filtros do ar-condicionado", "R$ 0"), ("fev", "Controle de pragas", "R$ 180"), ("mar", "Aquecedor a gás", "R$ 280"), ("abr", "Filtros; revisão elétrica; calhas", "R$ 500"),
       ("mai", "Pragas; caixa d'água", "R$ 430"), ("jun *", "nenhuma", "R$ 0"), ("jul *", "Filtros do ar-condicionado", "R$ 0"), ("ago *", "Controle de pragas", "R$ 180"),
       ("set", "Ar-condicionado (técnico)", "R$ 480"), ("out", "Filtros; calhas; extintores", "R$ 310"), ("nov", "Pragas; caixa d'água; deck", "R$ 1.330"), ("dez *", "nenhuma", "R$ 0")]
CAUSAS = [("1", "Item sem três cotações", "Pedir três cotações na mesma quantidade e prazo de entrega, e anotar."),
          ("2", "Compra recorrente sem contrato", "Fechar contrato com preço e prazo, começando pelo item que mais pesa."),
          ("3", "Item no ponto de pedido", "Fazer o pedido hoje e anotar no histórico de compras."),
          ("4", "Menos de três jogos por cama", "Completar o enxoval pela menor cotação."),
          ("5", "Manutenção pesada na casa cheia", "Mudar tarefas semestrais e anuais para meses de baixa."),
          ("6", "A reserva não cobre o plano", "Separar a reserva todo mês e ajustar percentual ou datas."),
          ("7", "Sem ronda diária ou sem registro de ocorrências", "Ronda com lista curta e quadro de ocorrências."),
          ("8", "Estoque sem dia de contagem ou compra sem limite", "Dia fixo de contagem e limite escrito para a equipe.")]
CHECK = [("Três meses de notas", "o gasto de cada item e as noites vendidas no mesmo período; um mês só engana."),
         ("Os itens por valor", "os cinco que mais pesam, não os que você compra mais vezes."),
         ("Três cotações por item", "na mesma unidade e com o mesmo prazo de entrega; uma pode ser o fornecedor de hoje."),
         ("Contrato nos recorrentes", "preço, prazo de entrega e validade, com data para fechar."),
         ("Consumo por noite e por hóspede", "conferido com o custo variável por noite da sua Folha (Módulo 2)."),
         ("Mínimo e ponto de pedido", "uso por mês, prazo de entrega e dias de segurança de cada item guardado."),
         ("Enxoval", "três jogos por cama; contagem peça por peça na Ferramenta 13."),
         ("Calendário de doze meses", "cada tarefa com frequência, mês, custo e quem faz; pesadas na baixa."),
         ("Reserva de manutenção", "de 3% a 6% da receita, numa conta própria, cobrindo o plano mês a mês."),
         ("A rotina", "contagem semanal no mesmo dia, ronda diária, registro de ocorrências, limite de compra e revisão mensal de fornecedores.")]

html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Resumo · Módulo 6 · Compras, estoque e manutenção · Jornada de Gestão</title><style>{CSS}.ex.compacto table{{font-size:8.2pt;margin:1.6mm 0 2mm}} .ex.compacto td,.ex.compacto th{{padding:.8mm 1.6mm}} .ex.compacto p{{margin-bottom:1.8mm}}</style></head><body>

<section class="pg capa"><img src="{(BR/'zion-logo-claro.png').as_uri()}" alt="Zion"><div><div class="k">Jornada de Gestão · Módulo 6 · Resumo da aula</div><h1>Onde a margem <i>some sem barulho.</i></h1><p>Compras, estoque e manutenção. O que ficou da aula em oito páginas: a Matriz de Compras por valor; três cotações e contrato; consumo por noite e por hóspede; estoque mínimo e ponto de pedido; o calendário de manutenção de doze meses e a reserva; um exemplo didático; como analisar; o checklist; o critério de conclusão e a próxima etapa.</p></div><div class="k" style="font-size:9pt">Aprenda o passo a passo · Zion Hotel Academy · Método Zion 360°</div></section>

<section class="pg"><h2>1. Compras é onde a margem some</h2>
<div class="cita">“Compras não é detalhe administrativo. É onde a margem some sem fazer barulho.”<small>Panorama do Desenvolvimento Hoteleiro · Trilha B · Pilar G5 “Compras e Fornecedores”</small></div>
<p>A pergunta central do pilar: <i>“O que se compra, de quem, e sob que contrato?”</i> O departamento de compras organiza tudo que entra na operação: cotação, contrato de fornecimento, enxoval, consumo por hóspede, estoque mínimo e reposição programada. É o departamento que quase nenhuma hospedagem pequena tem <span class="fonte">(Panorama · G5)</span>.</p>
<div class="grid"><div class="card"><b>Por que importa</b><small>“Comprar no susto, sempre do mesmo fornecedor e sem contrato, custa mais caro todo mês, e o valor nunca aparece numa linha só do extrato.”</small></div><div class="card"><b>O que custa ignorar</b><small>“Margem que some em compras não aparece no DRE como problema de compras: aparece como lucro menor, e aí se corta a coisa errada.” (DRE: o demonstrativo de resultado do mês.)</small></div></div>
<p>O pilar liga compras às finanças: é a linha de custo que a gestão financeira mais tem dificuldade de enxergar sem esse trabalho feito. Por isso esta aula usa o custo variável por noite da sua Folha Única do Mês (Módulo 2) como conferência.</p>
<h3>Os quatro passos do pilar</h3>
<ol><li><b>Liste o que você mais compra</b>: <i>“Por valor, não por frequência. Os cinco primeiros itens costumam responder pela maior parte do custo variável.”</i></li>
<li><b>Peça três cotações para cada</b>: <i>“Só isso costuma mudar o custo do mês seguinte, e não custa nada além de tempo.”</i></li>
<li><b>Feche contrato nos recorrentes</b>: preço e prazo acordados para o que você compra todo mês. <i>“Fornecedor com contrato entrega melhor e cobra menos.”</i></li>
<li><b>Calcule o consumo por hóspede</b>: amenidades, enxoval, café, gás e energia por diária vendida. <i>“É o número que permite prever o custo do mês cheio.”</i></li></ol>
<div class="caixa"><h3>Erro comum</h3><p style="margin:0">Comprar sempre do mesmo fornecedor sem cotar, por comodidade. <i>“A diferença aparece diluída em doze meses e por isso nunca é percebida.”</i> <span class="fonte">(Panorama · G5)</span></p></div>{ROD}</section>

<section class="pg"><h2>2. A Matriz de Compras</h2>
<p>O entregável do pilar é <i>“a Matriz de Compras com três cotações por item e a tabela de custo por hóspede”</i>. Na ficha, cada linha da Matriz tem:</p>
<ul><li><b>O item e a unidade de compra</b> (kg lavado, kit por estadia, botijão, jogo de cama).</li><li><b>O gasto no período</b>, somado nas notas de três meses, e o <b>tipo</b>: custo variável da hospedagem ou vendido à parte (café, cestas, frigobar).</li><li><b>O preço de hoje e três cotações</b>, da mesma unidade e com o mesmo prazo de entrega. Uma delas pode ser o seu fornecedor atual.</li><li><b>O contrato</b>: tem, vou fechar (com data) ou sem contrato.</li></ul>
<div class="caixa"><h3>As contas da ficha</h3><ul><li><b>Peso</b> = gasto do item ÷ gasto total da Matriz. A ficha ordena do maior para o menor.</li><li><b>Quantidade no período</b> = gasto ÷ preço de hoje.</li><li><b>Diferença para a menor cotação</b> = quantidade × (preço de hoje − menor cotação), só quando a menor é mais barata. Em doze meses: diferença do período × 12 ÷ meses do período.</li></ul></div>
<p>A diferença é uma conta com os seus números, não uma previsão: ela mostra o tamanho do que se dilui no ano. Negocie com ela na mão, e repita as cotações antes de renovar cada contrato.</p>
<h3>Contrato</h3>
<p>Para o que se compra todo mês, contrato com preço, prazo de entrega e validade. Marque uma data para fechar os que ainda não têm. A ficha aponta como sinal de atenção qualquer item recorrente sem contrato.</p>
<h3>Quem compra e até quanto</h3>
<p>A Etapa 10 pede um critério escrito para <i>“compra fora do previsto: até que valor a equipe compra sem perguntar”</i> (no exemplo da fonte, R$ 300), e coloca compras e reposição entre os procedimentos semanais a escrever <span class="fonte">(Jornada do COMO · Etapa 10 · Passos 04 e 06)</span>. Compra sem dono volta para a sua cabeça.</p>{ROD}</section>

<section class="pg"><h2>3. Consumo por noite e por hóspede</h2>
<p>A conta vem da Etapa 09: <i>“Some o gasto de cada item em três meses e divida pelo número de diárias vendidas no período.”</i> Para enxoval e itens duráveis, a fonte manda amortizar pela vida útil, e lembra a reposição por perda e desgaste, <i>“que em hospedagem é relevante e sempre é subestimada”</i> <span class="fonte">(Etapa 09 · Passo 05)</span>.</p>
<div class="caixa"><h3>As contas da ficha</h3><ul><li><b>Por noite vendida</b> = gasto do período ÷ noites vendidas no mesmo período.</li><li><b>Por hóspede</b> = gasto do período ÷ hóspedes do período.</li><li><b>Itens variáveis por noite</b> = soma dos itens marcados como custo variável ÷ noites vendidas.</li><li><b>Conferência com a Folha</b> = itens variáveis por noite ÷ custo variável por noite da Folha Única (Módulo 2).</li><li><b>Mês cheio</b> = itens variáveis por noite × unidades × 30 noites.</li></ul></div>
<p>A conferência mostra quanto do seu custo variável passa por compra. O restante está em custos fora da Matriz, como a limpeza por estadia e a reserva para quebra. Se a Matriz passar do custo da Folha, um item fixo entrou na lista ou a Folha está desatualizada.</p>
<p>O mês cheio é o número para não ser pego de surpresa quando todas as noites vendem: o caixa precisa ter esse dinheiro antes, porque a compra vem antes da receita. Não é previsão de ocupação.</p>
<h3>O enxoval</h3>
<div class="cita">“Enxoval dimensionado em três jogos por cama custa mais na compra e menos por ano.”<small>Panorama · Trilha B · Pilar G5 · Na prática</small></div>
<p>O desgaste cai porque cada peça descansa, e a virada entre hóspedes para de depender de a lavanderia entregar no horário. A ficha divide os jogos completos pelas camas e mostra quantos faltam para três por cama. Para o controle peça por peça, a Zion tem a Ferramenta 13 · Controle de Enxoval e Reposição.</p>{ROD}</section>

<section class="pg"><h2>4. Estoque mínimo e ponto de pedido</h2>
<p>A rotina de estoque da Zion é curta: <i>“Atualizar toda segunda-feira. Quando item atingir o mínimo, acionar fornecedor imediatamente.”</i> O gestor confere o estoque de limpeza e de frigobar todo dia e faz a revisão completa toda semana <span class="fonte">(Bíblia Operacional Zion · Controle de Estoque e Manual Gerencial)</span>.</p>
<p>A fonte não define como calcular o mínimo. A ficha usa as definições-padrão de gestão de estoque, declaradas como tal:</p>
<div class="caixa"><h3>As contas da ficha</h3><ul><li><b>Consumo por dia</b> = uso do mês ÷ 30.</li><li><b>Estoque mínimo</b> = consumo por dia × dias de segurança (a reserva para atraso ou mês mais cheio).</li><li><b>Ponto de pedido</b> = consumo por dia × (dias de entrega + dias de segurança). Os dois arredondados para cima.</li><li><b>Pedir</b>: quando o estoque de hoje está no ponto de pedido ou abaixo. <b>Quanto</b>: ponto de pedido + consumo do intervalo até a próxima compra − estoque de hoje.</li></ul></div>
<p>O ponto de pedido vem antes do mínimo de propósito: o pedido sai enquanto ainda há estoque para cobrir os dias de entrega, e o mínimo fica para o imprevisto. Quem pede só quando acaba compra no susto, paga frete de urgência e atrasa a virada.</p>
<h3>Erros que não podem acontecer</h3>
<ul><li>Não repor o estoque do frigobar e das amenidades antes do próximo hóspede.</li><li>Contar o estoque em dias diferentes a cada semana: o consumo deixa de ser comparável.</li><li>Comprar sem anotar no histórico (data, item, quantidade, fornecedor, valor): na próxima cotação, você não sabe quanto pagava.</li></ul>
<p class="fonte">Bíblia Operacional Zion · Manual Gerencial e Administrativo (rotina diária, semanal e mensal) e Controle de Estoque (colunas estoque atual, mínimo, repor e histórico).</p>{ROD}</section>

<section class="pg"><h2>5. O calendário de manutenção e a reserva</h2>
<p>A Etapa 10 coloca a manutenção preventiva entre os procedimentos de risco alto, revistos todo mês, e pede o documento <i>“Manutenção preventiva, com o calendário do ano”</i>. Entre os erros de quem faz tudo sozinho está a <i>“manutenção adiada que vira conserto”</i> <span class="fonte">(Etapa 10 · Passos 03, 04 e 07)</span>.</p>
<ul><li><b>Cada tarefa</b>: o que fazer, a frequência (mensal, bimestral, trimestral, semestral ou anual), o primeiro mês, o custo por vez e quem faz.</li><li><b>Na ficha</b>, uma tarefa cai num mês quando a distância até o primeiro mês da tarefa é múltipla da frequência. A soma de cada mês é o custo do mês.</li><li><b>Frequência e custo</b> vêm do manual do fabricante e do profissional responsável (gás, elétrica, extintores, caixa d'água, controle de pragas). A ficha não substitui laudos nem vistorias.</li></ul>
<h3>A ronda diária</h3>
<p>Na Zion, a manutenção faz uma ronda técnica todo dia, com lista: aquecimento da água, ar-condicionado, iluminação, bombas, deck e área externa (e, nas unidades com banheira de hidromassagem, nível, jatos, pH e cloro). <i>“Não fazer a ronda diária”</i> e <i>“deixar problema sem avisar”</i> estão entre os erros que não podem acontecer <span class="fonte">(Bíblia Operacional Zion · Manual Técnico e Manutenção)</span>. O registro de cada problema cabe na Ferramenta 14 · Quadro de Ocorrências e Manutenção; o plano com datas, na Ferramenta 18 · Planner de Manutenção Preventiva.</p>
<h3>A reserva de manutenção</h3>
<div class="cita">“Reserva de manutenção: o que será gasto em pintura, telhado, equipamento. Separe de 3% a 6% da receita por mês.”<small>Jornada do COMO · Etapa 09 · Passo 06</small></div>
<p>A ficha calcula a reserva do mês (receita real × percentual), acumula mês a mês e confere se ela cobre o gasto acumulado do calendário. O que sobra no ano fica para a reposição. E a regra da Zion vale aqui: obra e manutenção pesada na baixa ocupação, de preferência de segunda a quinta. Marque os meses de casa cheia (a sua Tabela do Módulo 3 mostra quais) e deixe as tarefas semestrais e anuais fora deles.</p>{ROD}</section>

<section class="pg"><h2>6. Exemplo aplicado</h2>
<div class="ex compacto"><b class="rot">Exemplo didático · dados fictícios</b>
<p style="font-size:9.4pt"><b>Cabanas do Vale</b>, quatro unidades, a mesma dos módulos 0, 2 e 3. Três meses de notas: <b>174 noites vendidas</b> (58 por mês, como na Folha de outubro) e 150 hóspedes. Custo variável por noite da Folha: R$ 28,32.</p>
{tab(["#", "Item", "Período", "Peso", "Por noite", "Por hóspede", "Hoje → menor", "Diferença", "Contrato"], ITENS, ["3%", "27%", "10%", "7%", "10%", "10%", "13%", "10%", "10%"], (2, 3, 4, 5, 7))}
<p style="font-size:9pt;margin-top:-1mm">* vendido à parte, fora do custo variável. ** só os itens variáveis: R$ 2.640 ÷ 174. A Matriz abre linhas da Folha do Módulo 2: enxoval R$ 380 por mês = lavanderia 300 + reposição 80; energia R$ 340 = gás 240 + elétrica 100.</p>
<p style="font-size:9.4pt">Itens variáveis: <b>R$ 15,17 por noite</b>, <b>53,6%</b> dos R$ 28,32 da Folha; os outros R$ 13,15 são limpeza por estadia, energia elétrica e reserva para quebra. Mês cheio (4 unidades × 30 noites): <b>R$ 1.820,69</b>. Diferença para a menor cotação: <b>R$ 437,00</b> no período, cerca de <b>R$ 1.748,00</b> em doze meses (conta, não previsão).</p>
{tab(["Estoque", "Uso por mês", "Entrega + segurança", "Hoje", "Mínimo", "Ponto de pedido", "Pedir"], ESTOQUE, ["30%", "11%", "15%", "9%", "10%", "13%", "12%"], (1, 3, 4, 5))}
<p style="font-size:9.4pt">Enxoval: 10 jogos para 4 camas, <b>2,5 por cama</b>; faltam 2 jogos. Calendário de 2027, reserva de 3% da receita real de R$ 13.565,60 = <b>R$ 406,97 por mês</b>, <b>R$ 4.883,62 no ano</b>:</p>
{tab(["Mês", "Tarefas", "Custo", "Mês", "Tarefas", "Custo"], [CAL[i] + CAL[i + 6] for i in range(6)], ["7%", "31%", "12%", "7%", "31%", "12%"], (2, 5))}
<p style="margin:0;font-size:9.4pt">* casa cheia (jun, jul, ago e dez). <b>17 tarefas, R$ 3.690,00 no ano</b>; mês mais pesado, novembro (R$ 1.330), na baixa. A reserva acumulada cobre o plano em todos os meses e sobra <b>R$ 1.193,62</b> para reposição.</p></div>
{ROD}</section>

<section class="pg"><h2>7. Como analisar a Matriz</h2>
<p>A ficha percorre os sinais nesta ordem e o primeiro que dispara é a causa principal: <b>cotar → contratar → estoque → enxoval → manutenção → rotina</b>. A ordem segue os passos do pilar G5 (cotação antes de contrato, contrato antes do consumo) e deixa a manutenção e a rotina para depois de o dinheiro das compras estar visível. É uma elaboração desta lição a partir das fontes.</p>
<table><tr><th style="width:5%">#</th><th style="width:40%">Sinal</th><th>Ação</th></tr>{''.join(tr([f'<td>{n}</td>', f'<td><b>{a}</b></td>', f'<td>{b}</td>']) for n, a, b in CAUSAS)}</table>
<p>Se nada disparar: compras e manutenção dentro das regras da fonte. Mantenha a contagem semanal, revise fornecedores e custos todo mês e refaça as cotações antes de renovar cada contrato. A ficha lista até três prioridades.</p>
<div class="ex"><b class="rot">Exemplo didático · dados fictícios</b><p style="margin:0"><b>Cabanas do Vale:</b> os cinco itens têm três cotações; o gás não tem contrato; o papel higiênico está abaixo do ponto de pedido; o enxoval tem 2,5 jogos por cama. A manutenção pesada está na baixa e a reserva cobre o plano. Causa principal: <b>compra recorrente sem contrato</b>. Prioridades: 1 fechar contrato do gás; 2 pedir 110 rolos de papel hoje; 3 completar o enxoval até três jogos por cama.</p></div>
<h3>A rotina</h3>
<p>Toda semana, no mesmo dia: a contagem do estoque e os pedidos. Todo mês: o checklist da planilha, as tarefas preventivas do mês, a reserva separada e a revisão de fornecedores e custos (rotina mensal da Zion). A cada contrato que vence: três cotações novas.</p>{ROD}</section>

<section class="pg"><h2>8. Faça agora e a próxima etapa</h2>
<p>Abra a ficha <b>A minha Matriz de Compras e Manutenção</b> (link na aula). Cinco telas, de 25 a 40 minutos: o período e o consumo (com um botão que traz o custo variável e a receita da sua Folha do Módulo 2, se ela estiver no mesmo aparelho), a Matriz de Compras, o estoque mínimo e o ponto de pedido, o calendário de manutenção e a rotina. No fim, as leituras, a causa principal, o plano e o PDF. As respostas ficam só no seu aparelho. A planilha <b>Matriz de Compras e Manutenção</b> (em branco e exemplo) faz as mesmas contas.</p>
<h3>Checklist da Matriz · 10 itens</h3>
<ol class="check">{''.join(f'<li><b>{a}</b>: {b}</li>' for a, b in CHECK)}</ol>
<div class="caixa"><h3>Critério de conclusão do Módulo 6</h3><ul style="columns:2;column-gap:6mm"><li>Pelo menos três itens com o preço de hoje e três cotações.</li><li>Pelo menos um item de estoque com ponto de pedido.</li><li>Calendário de doze meses com pelo menos três tarefas.</li><li>Plano de ação com uma ação escrita e um prazo.</li><li>PDF da Matriz baixado e guardado.</li></ul></div>
<p>A jornada segue para o <b>Módulo 7 · Qualidade, reputação e plano de crescimento</b>: lá as páginas do seu Plano de Gestão se juntam, com a rotina semanal e o teste de prontidão.</p>
<h3>Prompt de IA · revisar a Matriz</h3>
<p>Cole o prompt de <b>{URL_PROMPT.replace('https://', '')}</b> num assistente de IA e, depois, a sua Matriz: ele refaz as contas e aplica só as regras da fonte, sem inventar preços nem prometer economia.</p>
<p class="fonte">Fontes: Panorama do Desenvolvimento Hoteleiro · Trilha B · Pilar G5 “Compras e Fornecedores”. Jornada do COMO · Etapa 09 (Passos 05 e 06: consumo e reserva de manutenção) e Etapa 10 (Passos 03, 04, 06 e 07: ordem de escrita, critérios de decisão, manual). Bíblia Operacional Zion (Controle de Estoque, Manual Gerencial e Administrativo, Manual Técnico e Manutenção, Parceiros e Fornecedores). Elaborações declaradas: mínimo e ponto de pedido (definição-padrão de gestão de estoque), regra de calendário por frequência, conferência com a Folha, ordem dos oito sinais. Material educacional da Zion Hotel Academy · Método Zion 360°. Não é promessa de renda, retorno, ocupação ou resultado.</p>{ROD}</section>
</body></html>"""
(B / "resumo.html").write_text(html, encoding="utf-8")
print("ok", B / "resumo.html"); print("ok", MAT / "Modulo-6-Prompt-de-IA.txt")

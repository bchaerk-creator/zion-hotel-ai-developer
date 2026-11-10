"""Gera o HTML do resumo da aula do Módulo 3 (Preço, reservas e distribuição) e o TXT do prompt de IA.
Depois, src/render_pdf.js imprime o HTML em PDF (8 páginas A4).
Uso: python3 -I src/build_resumo.py <pasta-build>
Saídas: <pasta-build>/resumo.html e docs/trilha2/materiais/Modulo-3-Prompt-de-IA.txt
Os números do exemplo saem de tests (logic.js e planilha); aqui ficam escritos e são conferidos pelo teste de conformidade do REGISTRO."""
import sys, pathlib, re
B = pathlib.Path(sys.argv[1]); B.mkdir(parents=True, exist_ok=True)
HERE = pathlib.Path(__file__).resolve().parent; LICAO = HERE.parent
REPO = LICAO.parents[2]; F = REPO / "docs/assets/fonts"; BR = REPO / "docs/brand"
MAT = REPO / "docs/trilha2/materiais"; MAT.mkdir(parents=True, exist_ok=True)
URL_PROMPT = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/trilha2/materiais/Modulo-3-Prompt-de-IA.txt"

md = (LICAO / "PROMPT_IA.md").read_text(encoding="utf-8")
bloco = re.search(r"```\n(.*?)```", md, re.S).group(1).strip()
txt = ("PROMPT DE IA · REVISAR A TABELA DE PREÇO E CANAIS\n"
       "Zion Hotel Academy · Jornada de Gestão · Módulo 3 · Preço, reservas e distribuição\n\n"
       "Como usar: exporte a sua Tabela de Preço e Canais em PDF (ou copie as abas da planilha), abra qualquer assistente de IA, "
       "cole o prompt abaixo inteiro e, logo depois, cole o conteúdo da Tabela. O assistente não conhece o seu destino nem substitui o "
       "levantamento dos concorrentes: ele confere a lógica e faz perguntas. Não cole dados pessoais de hóspedes nem senhas.\n\n"
       "----- COPIE DAQUI PARA BAIXO -----\n\n" + bloco + "\n\n----- FIM DO PROMPT -----\n\n"
       "Depois da revisão, anote em duas linhas, na aba Checklist da revisão da planilha, o que mudou e por quê.\n"
       "Conteúdo educacional. Não é promessa de renda, retorno, ocupação ou resultado.\n")
(MAT / "Modulo-3-Prompt-de-IA.txt").write_text(txt, encoding="utf-8")

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
ROD = '<div class="rod"><span>Zion Hotel Academy · Jornada de Gestão · Módulo 3</span><span>Conteúdo educacional. Não é promessa de renda, retorno, ocupação ou resultado.</span></div>'
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

CANAIS = [("Plataforma A", "50%", "16% + 1,5% + 6% = 23,5%", "R$ 229,50", "R$ 201,18"), ("Plataforma B", "20%", "15% + 1,5% + 6% = 22,5%", "R$ 232,50", "R$ 204,18"), ("Venda direta (site e WhatsApp)", "30%", "0% + 1,5% + 6% = 7,5%", "R$ 277,50", "R$ 249,18")]
FAIXAS = [("Vale", "0,70 a 0,80", "0,75", "R$ 225", "84"), ("Baixa", "0,85 a 0,95", "0,90", "R$ 270", "122"), ("Base", "1,00", "1,00", "R$ 300", "99"), ("Alta", "1,35 a 1,60", "1,50", "R$ 450", "44"), ("Pico", "1,90 a 2,60", "por data", "por data", "16")]
MESES = [("jan", "baixa · R$ 270", "base · R$ 300", "R$ 279,68"), ("fev *", "baixa · R$ 270", "base · R$ 300", "R$ 334,29"), ("mar", "vale · R$ 225", "baixa · R$ 270", "R$ 236,61"), ("abr", "vale · R$ 225", "baixa · R$ 270", "R$ 238,50"),
         ("mai *", "vale · R$ 225", "base · R$ 300", "R$ 291,29"), ("jun", "base · R$ 300", "alta · R$ 450", "R$ 340,00"), ("jul *", "alta · R$ 450", "alta · R$ 450", "R$ 464,52"), ("ago", "base · R$ 300", "alta · R$ 450", "R$ 338,71"),
         ("set", "baixa · R$ 270", "base · R$ 300", "R$ 278,00"), ("out", "baixa · R$ 270", "base · R$ 300", "R$ 279,68"), ("nov", "vale · R$ 225", "baixa · R$ 270", "R$ 237,00"), ("dez *", "baixa · R$ 270", "base · R$ 300", "R$ 351,29")]
PICOS = [("Carnaval", "fev", "4", "2,20", "R$ 660", "4"), ("Corpus Christi (feriado prolongado)", "mai", "4", "1,90", "R$ 570", "3"), ("Festival de inverno (evento local)", "jul", "3", "2,00", "R$ 600", "2"), ("Réveillon", "dez", "5", "2,40", "R$ 720", "5")]
CAUSAS = [("1", "Referência abaixo do custo da noite", "Pela fonte, o problema é estrutura de custo, não preço: voltar à Folha (Módulo 2)."),
          ("2", "Piso abaixo do custo da noite", "Subir o piso até o custo no canal mais caro, mais a margem mínima."),
          ("3", "Faixa ou data abaixo do piso", "Subir o fator ou rever o piso: nenhuma diária abaixo dele."),
          ("4", "Preço fixo o ano inteiro", "Levantar o destino e distribuir as cinco faixas pelos meses."),
          ("5", "Datas de pico sem regra", "Preço próprio, mínimo de noites, abertura; datas bloqueadas até terem preço."),
          ("6", "Sem venda direta", "Abrir um canal direto e medir quanto entra por ele."),
          ("7", "Vários canais sem gestor de canais", "Ligar os calendários antes de abrir mais canais."),
          ("8", "Venda direta sem motor de reservas", "Motor de reservas ou link de reserva com pagamento, ligado ao calendário."),
          ("9", "Piso só na sua cabeça", "Imprimir a folha do piso e combinar com quem atende.")]
CHECK = [("O custo da noite", "custo variável e custo por noite vendida da Folha Única do Mês (Módulo 2); para a tabela do ano, o ideal é a média do ano."),
         ("O mix dos últimos três meses", "receita por canal, comissão e taxa de pagamento, do extrato de repasse. Não chute."),
         ("O preço de seis a nove concorrentes", "mesmo porte, público e região, num fim de semana comum, preço final com taxas."),
         ("A diária de referência", "média sem o mais caro e o mais barato, na posição que fotos e avaliações sustentam."),
         ("O piso, por escrito", "pelo menos o custo da noite no canal mais caro, mais a margem mínima; vale na véspera."),
         ("Quem sabe do piso e as três condições", "todo mundo que atende conhece o piso; ceda em data, noite extra ou serviço."),
         ("As cinco faixas e os doze meses", "fatores calibrados pelo levantamento, faixa de meio de semana e de fim de semana em cada mês, nada abaixo do piso."),
         ("As datas de pico", "preço próprio, mínimo de noites, data de abertura, datas bloqueadas até terem preço."),
         ("O calendário no canal", "pelo menos seis meses abertos (ideal, doze), mínimo de noites e preço final conferidos."),
         ("A meta de venda direta e o básico técnico", "número acima do atual com prazo; gestor de canais e motor de reservas; primeira revisão trimestral marcada.")]

html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Resumo · Módulo 3 · Preço, reservas e distribuição · Jornada de Gestão</title><style>{CSS}</style></head><body>

<section class="pg capa"><img src="{(BR/'zion-logo-claro.png').as_uri()}" alt="Zion"><div><div class="k">Jornada de Gestão · Módulo 3 · Resumo da aula</div><h1>Um piso, <i>um calendário, os canais.</i></h1><p>Preço, reservas e distribuição. O que ficou da aula em oito páginas: o preço começa pelo custo; o que cada canal deixa; a diária de referência e o piso; as cinco faixas, as datas de pico e o calendário de doze meses; um exemplo didático; como analisar; o checklist; o critério de conclusão e a próxima etapa.</p></div><div class="k" style="font-size:9pt">Aprenda o passo a passo · Zion Hotel Academy · Método Zion 360°</div></section>

<section class="pg"><h2>1. O preço começa pelo custo</h2>
<div class="cita">“Calendário vazio quase nunca se resolve com desconto.”<small>Panorama do Desenvolvimento Hoteleiro · Trilha B · Pilar G3 “Preço e Receita”</small></div>
<p>A pergunta central do pilar é direta: <i>“Qual é o seu piso, e o que você nunca vende abaixo dele?”</i> E o custo de ignorar também: <i>“Sem piso, a diária cai sozinha nos meses fracos e não volta nos fortes.”</i> <span class="fonte">(Panorama · G3)</span></p>
<p>O primeiro passo do pilar é o custo por diária vendida, que você já calculou na Folha Única do Mês (Módulo 2): o custo variável de cada noite mais todo o custo fixo dividido pelas noites que você de fato vendeu. Na ficha, ele se chama <b>custo por noite vendida</b>.</p>
<h3>A regra do desconto em três faixas</h3>
<div class="grid grid3"><div class="card"><b>Acima do custo por noite</b><small>A venda contribui para tudo, inclusive para o fixo e para a sua retirada.</small></div><div class="card"><b>Entre o variável e o custo</b><small>Não cobre tudo, mas ajuda no fixo que sairia de qualquer jeito. Só reduz prejuízo.</small></div><div class="card"><b>Abaixo do variável</b><small>A venda destrói valor: consome mais do que traz e ainda impede uma venda melhor.</small></div></div>
<p class="fonte">Jornada do COMO · Etapa 09 · Passo 08 (Custo por Diária Vendida™). Em mês de baixa o custo por noite está no pico, exatamente quando a tentação é baixar o preço.</p>
<h3>Os três erros de preço</h3>
<table><tr><th style="width:22%">Erro</th><th>Sintoma</th><th style="width:30%">Correção</th></tr>
<tr><td><b>Preço fixo</b></td><td>O pico esgota cedo e a baixa fica vazia. Erra nas duas direções ao mesmo tempo.</td><td>Calendário com faixas</td></tr>
<tr><td><b>Preço de medo</b></td><td>Desce sempre que falta ocupação, sem piso e sem prazo.</td><td>Piso escrito e política de desconto</td></tr>
<tr><td><b>Preço de inveja</b></td><td>Copia o concorrente mais caro sem ter o produto dele: muita gente vê, ninguém reserva.</td><td>Preço alinhado ao produto real</td></tr></table>
<p class="fonte">Jornada do COMO · Etapa 08 · Passo 01 (Mapa dos Três Erros™). A correção é a mesma para os três: calendário com faixas, definido com antecedência, com regras escritas antes de a data chegar.</p>{ROD}</section>

<section class="pg"><h2>2. O que cada canal deixa</h2>
<div class="cita">“Estar em todos os canais não é distribuição. É dependência dividida.”<small>Panorama · Trilha B · Pilar G2 “Distribuição e Canais”</small></div>
<p>Cada canal tem um custo de aquisição diferente, e a diferença entre a venda direta e a plataforma é margem que sobra ou não sobra no fim do mês. Quem vende só por plataforma não tem base de hóspedes nem como vender a segunda estadia sem pagar comissão de novo. E o pilar lembra: o G2 <i>“define o custo de aquisição que o Pilar G3 precisa cobrir no preço”</i>.</p>
<h3>Os quatro passos do mapa de canais</h3>
<ol><li><b>O mix atual</b>: quanto entrou por cada canal nos últimos três meses. <i>“A maioria dos donos erra esse número quando chuta.”</i></li>
<li><b>O líquido por canal</b>: da diária, tire a comissão, a taxa de pagamento, o imposto e o custo de adquirir aquele hóspede. <i>“O canal mais cheio nem sempre é o mais lucrativo.”</i></li>
<li><b>A meta de venda direta</b>: <i>“Um número, não uma intenção. E o prazo para chegar nele.”</i></li>
<li><b>O básico técnico</b>: motor de reservas no site e gestor de canais ligando os calendários. Sem isso, venda direta vira trabalho manual e risco de reserva duplicada.</li></ol>
<div class="caixa"><h3>As contas da ficha</h3><ul><li><b>Deduções do canal</b> = comissão + taxa de pagamento + imposto sobre a receita.</li><li><b>Líquido por noite</b> = diária × (1 − deduções) − custo por reserva ÷ noites por estadia.</li><li><b>Depois do custo variável</b> = líquido − custo variável por noite.</li><li><b>Comissão média</b> = soma de (participação no mix × comissão).</li></ul></div>
<p>Na venda direta, a comissão fica com você. A Etapa 09 mostra que até uma estadia longa com desconto, vendida direto, pode deixar mais que uma noite avulsa por plataforma a preço cheio, porque a limpeza é por estadia e a comissão é por venda <span class="fonte">(Etapa 09 · Passo 10)</span>.</p>
<div class="caixa"><h3>Erro comum</h3><p style="margin:0">Entrar em todas as plataformas para aumentar a visibilidade, sem gestor de canais. O resultado é reserva duplicada, cancelamento e nota baixa, e aí a visibilidade trabalha contra. <span class="fonte">(Panorama · G2)</span></p></div>{ROD}</section>

<section class="pg"><h2>3. A diária de referência e o piso</h2>
<p>A <b>diária de referência</b> é o preço cheio, sem desconto e sem condição. Todo o calendário sai dela: para cima nas datas de pico, para baixo na baixa. <i>“Ele cai em uma semana e leva um ano para voltar.”</i> <span class="fonte">(Etapa 08 · Passo 03)</span></p>
<ol><li>Levante o preço de seis a nove concorrentes diretos numa data de demanda média: um fim de semana comum, preço final com taxas.</li><li>Descarte o mais caro e o mais barato e tire a média dos restantes.</li><li>Posicione-se: terço de baixo (cerca de 15% abaixo da média), meio (a média) ou terço de cima (cerca de 20% acima). É decisão de marca.</li><li>Confira contra o custo: se a referência não cobre o custo por noite com margem, <i>“o problema não é preço, é estrutura de custo”</i>.</li></ol>
<p>Para subir depois, a fonte orienta de 8% a 12% por vez, com seis a oito semanas entre um aumento e outro.</p>
<h3>O piso</h3>
<div class="cita">“O piso não é o custo: é o custo mais a margem mínima que justifica abrir a porta.”<small>Jornada do COMO · Etapa 08 · Passo 10 · Política de Desconto™</small></div>
<p>A fonte também diz: <i>“Abaixo do custo por diária somado à comissão, vender dá prejuízo”</i>. Por isso a ficha calcula o <b>custo da noite no canal mais caro</b> = (custo por noite vendida + custo por reserva ÷ noites por estadia) ÷ (1 − deduções do canal) e, sobre ele, a sua margem mínima. A fórmula é uma elaboração desta lição a partir da regra da fonte; a margem é decisão sua.</p>
<div class="grid"><div class="card"><b>Por escrito, antes de precisar</b><small>“Piso decidido em mês fraco é piso que não existe.” <span class="fonte">Etapa 08 · Passo 03</span></small></div><div class="card"><b>Combinado com quem atende</b><small>“Um número, combinado com todo mundo que atende. Inclusive para véspera.” <span class="fonte">Panorama · G3</span></small></div><div class="card"><b>Vale para todo desconto</b><small>Nenhuma das quatro situações de desconto passa do piso, e nas datas de pico não há desconto.</small></div><div class="card"><b>Fora da cabeça</b><small>“Piso que só existe na sua cabeça não é piso.” <span class="fonte">Etapa 08 · Passo 10</span></small></div></div>{ROD}</section>

<section class="pg"><h2>4. As cinco faixas, os picos e o calendário</h2>
<p><i>“Cinco números resolvem o ano inteiro.”</i> Cada faixa é um fator sobre a diária de referência. Os fatores abaixo são o <b>ponto de partida</b> da fonte; o levantamento do seu destino é que decide os seus <span class="fonte">(Etapa 08 · Passo 05)</span>.</p>
{tab(["Faixa", "Quando", "Fator de partida"], [("Vale", "Meses de baixa, meio de semana", "0,70 a 0,80"), ("Baixa", "Baixa no fim de semana e meio de semana de meses médios", "0,85 a 0,95"), ("Base", "A própria referência: fim de semana comum", "1,00"), ("Alta", "Temporada e feriados simples", "1,35 a 1,60"), ("Pico", "Réveillon, carnaval, feriados prolongados e eventos", "1,90 a 2,60")], ["14%", None, "18%"], (2,))}
<h3>As datas de pico</h3>
<p>Não seguem as faixas: a demanda é muito maior que a oferta. Quatro regras: preço próprio; mínimo de noites (de três a cinco em feriado prolongado, de cinco a sete no réveillon); abertura planejada; cancelamento mais rígido. <i>“Bloqueie as datas de pico e só abra quando o preço estiver definido.”</i> Eventos locais são a oportunidade mais negligenciada <span class="fonte">(Etapa 08 · Passo 06)</span>.</p>
<h3>O calendário de doze meses</h3>
<ul><li>Em cada mês, uma faixa para o meio de semana e outra para o fim de semana. Em destino de escapada curta, o fim de semana costuma valer de 25% a 60% mais <span class="fonte">(Etapa 08 · Passo 07)</span>.</li><li>Na ficha, fim de semana são as noites de sexta e de sábado do calendário real, e as noites de pico saem primeiro do meio de semana (convenção desta lição).</li><li>Suba o calendário nos canais com pelo menos seis meses abertos; o ideal são doze. Quem decide cedo costuma pagar melhor.</li><li>A <b>diária média do calendário</b> é a média das diárias-alvo, ponderada pelas noites do ano. Não é previsão de receita.</li></ul>
<h3>Desconto e condição</h3>
<p><i>“Troque desconto por condição. Desconto em diária vira a tabela nova; condição não.”</i> <span class="fonte">(Panorama · G3)</span> Desconto, só em quatro situações, com condição explícita e prazo: estadia longa (10 a 20% a partir da quinta noite), grande antecedência (8 a 15%), base própria e recorrência (10 a 15%) e último minuto dentro da janela curta <span class="fonte">(Etapa 08 · Passo 10)</span>.</p>{ROD}</section>

<section class="pg"><h2>5. Exemplo aplicado</h2>
<div class="ex compacto"><b class="rot">Exemplo didático · dados fictícios</b>
<p style="font-size:9.6pt"><b>Cabanas do Vale</b>, quatro unidades, a mesma do Marco Zero e da Folha Única. Da Folha de outubro: custo variável por noite R$ 28,32, custo por noite vendida R$ 153,03, diária praticada R$ 280, 2,32 noites por estadia, receita de hospedagem R$ 16.240. Referência: concorrentes 270, 280, 290, 300, 310, 320 e 360; sem 270 e 360, média de cinco = <b>R$ 300</b>, posição do meio.</p>
{tab(["Canal", "Mix", "Deduções", "Líquido por noite", "Depois do variável"], CANAIS, ["30%", "8%", "26%", "17%", "19%"], (3, 4))}
<p style="font-size:9.6pt">Comissão média ponderada: <b>11,0%</b> (a mesma da Folha). Piso: custo da noite na Plataforma A = 153,03 ÷ 0,765 = <b>R$ 200,04</b>; com margem mínima de 10%, piso calculado <b>R$ 220,04</b>; <b>piso escrito R$ 225</b> (75% da referência). Limite do variável: 28,32 ÷ 0,765 = R$ 37,02.</p>
{tab(["Faixa", "Partida", "Fator", "Diária", "Noites em 2027"], FAIXAS, ["16%", "22%", "14%", "20%", "28%"], (2, 3, 4))}
{tab(["Mês", "Semana", "Fim de semana", "Média", "Mês", "Semana", "Fim de semana", "Média"], [MESES[i] + MESES[i + 6] for i in range(6)], ["7%", "15%", "15%", "13%", "7%", "15%", "15%", "13%"], (3, 7))}
{tab(["Data de pico", "Mês", "Noites", "Fator", "Diária", "Mínimo"], PICOS, ["38%", "10%", "11%", "11%", "16%", "14%"], (2, 3, 4, 5))}
<p style="margin:0;font-size:9.6pt">* mês com data de pico. Total: 365 noites. <b>Diária média do calendário: R$ 305,92</b> (contra R$ 280 praticados; média das diárias-alvo, não previsão). Outubro: R$ 279,68. Meta de venda direta: de 30% para <b>40% até 30/06/2027</b>; com a mesma receita de R$ 16.240, cerca de <b>R$ 255,20</b> de comissão a menos num mês (conta, não previsão).</p></div>
{ROD}</section>

<section class="pg"><h2>6. Como analisar a Tabela</h2>
<p>A ficha percorre os sinais nesta ordem e a primeira que dispara é a causa principal: <b>custo → piso → calendário → canais → piso conhecido</b>. A ordem segue a fonte: o preço começa pelo custo (Etapa 08 · Passo 03; Etapa 09 · Passo 08), o piso vem antes do calendário (G3, passos 01 a 03) e os canais definem o custo de aquisição que o preço precisa cobrir (G2).</p>
<table><tr><th style="width:5%">#</th><th style="width:36%">Causa</th><th>Ação</th></tr>{''.join(tr([f'<td>{n}</td>', f'<td><b>{a}</b></td>', f'<td>{b}</td>']) for n, a, b in CAUSAS)}</table>
<p>Se nada disparar: tabela dentro das regras da fonte. Marque as quatro revisões trimestrais e mantenha doze meses abertos. A ficha lista até três prioridades.</p>
<div class="ex"><b class="rot">Exemplo didático · dados fictícios</b><p style="margin:0"><b>Cabanas do Vale:</b> a referência (R$ 300) cobre o custo da noite (R$ 200,04); o piso (R$ 225) cobre o custo com a margem; o vale encosta no piso e não passa; há datas de pico com mínimo; venda direta de 30% e gestor de canais. A causa principal é <b>venda direta sem motor de reservas</b>: prioridade única, instalar um motor de reservas no site ligado ao calendário.</p></div>
<h3>A revisão trimestral</h3>
<p>Quatro vezes por ano, duas horas cada, de três a quatro semanas antes do trimestre que a revisão decide: o painel do trimestre, a releitura do mercado, as datas que fecharam cedo, a referência, o custo (que define se o piso ainda é piso), e duas linhas sobre o que mudou e por quê <span class="fonte">(Etapa 08 · Passo 13)</span>. Compare sempre com o mesmo mês do ano anterior.</p>{ROD}</section>

<section class="pg"><h2>7. Faça agora</h2>
<p>Abra a ficha <b>A minha Tabela de Preço e Canais</b> (link na aula). Seis telas, de 20 a 30 minutos: o custo da noite (com um botão que traz os números da sua Folha do Módulo 2, se ela estiver no mesmo aparelho), os seus canais, a diária de referência, o piso e as condições, as cinco faixas nos doze meses, as datas de pico e a meta de venda direta. No fim, o calendário, o líquido por canal, as leituras, a causa principal e o PDF. As respostas ficam só no seu aparelho. A planilha <b>Tabela de Preço e Canais</b> (em branco e exemplo) faz as mesmas contas.</p>
<p>Complementos que já existem: o <b>Precificador Inteligente</b> (bônus) e a <b>Ferramenta 01 · Diária Mínima</b>.</p>
<h3>Checklist da Tabela · 10 itens</h3>
<ol class="check">{''.join(f'<li><b>{a}</b>: {b}</li>' for a, b in CHECK)}</ol>
<div class="caixa"><h3>Critério de conclusão do Módulo 3</h3><ul style="columns:2;column-gap:6mm"><li>Diária de referência informada.</li><li>Piso escrito.</li><li>Os doze meses com faixa de meio de semana e de fim de semana.</li><li>Mix de canais com percentual em todas as linhas, somando 100%.</li><li>Meta de venda direta acima da atual, com prazo.</li><li>Plano de ação com uma ação escrita e um prazo.</li><li>PDF da Tabela baixado e guardado.</li></ul></div>{ROD}</section>

<section class="pg"><h2>8. A próxima etapa</h2>
<p>Com a Tabela na mão, você tem um número abaixo do qual não vende, um calendário que decide o preço antes de a pressão chegar, e sabe quanto cada canal deixa por noite. A jornada segue para o <b>Módulo 4 · Marketing e vendas</b>: é lá que a meta de venda direta vira lista própria de hóspedes e custo por reserva.</p>
<div class="cita">“Ocupação é vaidade, margem é sobrevivência. Os dois números só fazem sentido lidos juntos.”<small>Panorama · Trilha B · Estudo de caso ilustrativo “O mês cheio que fechou no vermelho”</small></div>
<h3>Prompt de IA · revisar a Tabela</h3>
<p>Depois de exportar a Tabela, cole o prompt publicado em <b>{URL_PROMPT.replace('https://', '')}</b> em qualquer assistente de IA e, em seguida, a sua Tabela. Em resumo, o prompt pede ao assistente que, sem inventar preços de mercado, sem prometer resultado e sem dar nota própria:</p>
<ul><li><b>A)</b> refaça o custo da noite em cada canal, o piso, as diárias das faixas e o líquido por canal, mostrando a conta;</li><li><b>B)</b> aplique só as regras da fonte e aponte a causa principal pela ordem de correção;</li><li><b>C)</b> confira a coerência do calendário (meses trocados, picos sem mínimo, faixas que encostam no piso);</li><li><b>D)</b> formule três perguntas para a próxima revisão trimestral.</li></ul>
<h3>Fontes</h3>
<p class="fonte">Panorama do Desenvolvimento Hoteleiro · Trilha B · Pilares G2 “Distribuição e Canais” e G3 “Preço e Receita”, estudo de caso ilustrativo. Jornada do COMO · Etapa 08 “Como eu cobro certo?” (Passos 01, 03, 05, 06, 07, 10 e 13: Mapa dos Três Erros, Diária de Referência Zion, As Cinco Faixas Zion, Mapa de Datas de Pico, Calendário de Preços Zion, Política de Desconto, Rotina de Revisão) e Etapa 09 (Passo 08, Custo por Diária Vendida; Passo 10, Mapa de Margem). Elaborações declaradas desta lição: a fórmula do custo da noite no canal e do piso calculado; a contagem de fim de semana (sexta e sábado) e a regra de descontar as noites de pico primeiro do meio de semana; a ordem das nove causas.</p>
<p class="fonte">Material educacional da Zion Hotel Academy · Método Zion 360°. Não é promessa de renda, retorno, ocupação ou resultado: o preço certo depende dos números reais de cada hospedagem e do levantamento do seu destino.</p>{ROD}</section>
</body></html>"""
(B / "resumo.html").write_text(html, encoding="utf-8")
print("ok", B / "resumo.html"); print("ok", MAT / "Modulo-3-Prompt-de-IA.txt")

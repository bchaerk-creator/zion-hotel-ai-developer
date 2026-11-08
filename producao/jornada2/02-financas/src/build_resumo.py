"""Gera o HTML do resumo da aula do Módulo 2 (Finanças, fluxo de caixa e fechamento) e o TXT do prompt de IA.
Depois, src/render_pdf.js imprime o HTML em PDF (8 páginas A4).
Uso: python3 -I src/build_resumo.py <pasta-build>
Saídas: <pasta-build>/resumo.html e docs/trilha2/materiais/Modulo-2-Prompt-de-IA.txt"""
import sys, pathlib, re
B = pathlib.Path(sys.argv[1]); B.mkdir(parents=True, exist_ok=True)
HERE = pathlib.Path(__file__).resolve().parent; LICAO = HERE.parent
REPO = LICAO.parents[2]; F = REPO / "docs/assets/fonts"; BR = REPO / "docs/brand"
MAT = REPO / "docs/trilha2/materiais"; MAT.mkdir(parents=True, exist_ok=True)
URL_PROMPT = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/trilha2/materiais/Modulo-2-Prompt-de-IA.txt"

# ---------- Prompt de IA em texto puro (extraído de PROMPT_IA.md, bloco de código) ----------
md = (LICAO / "PROMPT_IA.md").read_text(encoding="utf-8")
bloco = re.search(r"```\n(.*?)```", md, re.S).group(1).strip()
txt = ("PROMPT DE IA · REVISAR O FECHAMENTO DO MÊS\n"
       "Zion Hotel Academy · Jornada de Gestão · Módulo 2 · Finanças, fluxo de caixa e fechamento\n\n"
       "Como usar: exporte a sua Folha Única do Mês em PDF (ou copie a tabela da planilha), abra qualquer assistente de IA, "
       "cole o prompt abaixo inteiro e, logo depois, cole o conteúdo da Folha. O assistente não substitui o seu contador nem a sua "
       "leitura: ele confere a lógica e faz perguntas. Não cole dados pessoais de hóspedes nem senhas.\n\n"
       "----- COPIE DAQUI PARA BAIXO -----\n\n" + bloco + "\n\n----- FIM DO PROMPT -----\n\n"
       "Depois da revisão, anote em uma linha, na aba Histórico da planilha, o que explicou o mês.\n"
       "Conteúdo educacional. Não é promessa de renda, retorno ou resultado.\n")
(MAT / "Modulo-2-Prompt-de-IA.txt").write_text(txt, encoding="utf-8")

# ---------- HTML do resumo ----------
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
ROD = '<div class="rod"><span>Zion Hotel Academy · Jornada de Gestão · Módulo 2</span><span>Conteúdo educacional. Não é promessa de renda, retorno ou resultado.</span></div>'

def tr(cells, cls=""):
    return f'<tr class="{cls}">' + "".join(cells) + "</tr>"

# ---- Tabelas
CLASSIF = [
    ("Dedução", "Sai antes de a receita chegar na conta; separa o faturamento da receita real.", "Descontos, comissões de canal, taxa de processamento, imposto sobre a receita, cancelamentos."),
    ("Custo variável", "Sai com cada noite vendida e não sairia com a unidade vazia.", "Limpeza (líquida do repasse), enxoval, amenidades, energia da unidade, café, quebra e perda, custo das outras receitas."),
    ("Custo fixo operacional", "Sai todo mês, com casa cheia ou vazia. A sua retirada está aqui.", "Equipe, contas comuns, software, contador, marketing fixo, despesas anuais ÷ 12, manutenção contratada, retirada do dono."),
    ("Custo do modelo", "Depende de como a hospedagem foi montada, não de como ela opera.", "Aluguel ou arrendamento, taxa de gestão, uso de marca."),
    ("Reserva ou depreciação", "Repõe o que se desgasta. Reserva é caixa; depreciação é conta contábil. Nunca as duas juntas.", "Reserva de reposição de 3 a 6% da receita (padrão 4%), ou a depreciação do contador."),
]
INDIC = [
    ("Receita real", "receita bruta de hospedagem − deduções (+ outras receitas)", "O que de fato chegou."),
    ("Diária média real", "receita real de hospedagem ÷ noites vendidas", "A diária que entra na conta, não a de tabela."),
    ("Custo variável por noite", "custos variáveis (sem o custo das outras receitas) ÷ noites vendidas", "O que cada noite leva embora ao ser vendida."),
    ("Custo por noite vendida", "custo variável por noite + custo fixo do mês ÷ noites vendidas", "Em mês de baixa está no pico. Diz se cada noite se paga."),
    ("Margem por noite", "diária média real − custo variável por noite", "Quanto cada noite deixa para pagar o fixo."),
    ("Ponto de equilíbrio", "(custo fixo do mês − margem das outras receitas) ÷ margem por noite", "Quantas noites o mês precisa vender para empatar."),
    ("Ocupação de equilíbrio", "ponto de equilíbrio ÷ noites disponíveis", "Acima de 70% é alerta; de 45 a 65% é saudável."),
    ("Meses de fôlego", "(saldo final + reservas separadas) ÷ custo fixo do mês", "Abaixo de 2 é zona de risco; de 4 a 6 é confortável."),
]
CASCATA = [  # rótulo, valor, classe
    ("Receita bruta de hospedagem (58 noites × R$ 280)", "16.240,00", ""),
    ("− Deduções: descontos 650 + 18,5% (comissões 11%, processamento 1,5%, imposto 6%)", "3.654,40", "sub"),
    ("= Receita real de hospedagem", "12.585,60", "tot"),
    ("+ Outras receitas (café e cestas)", "980,00", ""),
    ("= Receita real total", "13.565,60", "tot"),
    ("− Variáveis: limpeza líquida 500, enxoval 380, amenidades 260, energia 340, quebra 1% 162,40, custo das outras 420", "2.062,40", "sub"),
    ("= Margem de contribuição", "11.503,20", "tot"),
    ("− Fixos: equipe 1.800, comuns 620, software 190, contador 300, marketing 150, duodécimos 460, manutenção 250, retirada 3.464", "7.234,00", "sub"),
    ("= Resultado operacional (quanto sobrou do mês)", "4.269,20", "tot"),
    ("− Custos do modelo (aluguel, gestão, marca)", "0,00", "sub"),
    ("− Reserva de reposição (4% da receita real)", "542,62", "sub"),
    ("= O que ficou no caixa para o negócio", "3.726,58", "tot"),
]
EX_IND = [
    ("Diária média real", "12.585,60 ÷ 58", "R$ 216,99"),
    ("Custo variável por noite", "(2.062,40 − 420) ÷ 58", "R$ 28,32"),
    ("Custo por noite vendida", "28,32 + 7.234 ÷ 58", "R$ 153,03"),
    ("Margem por noite", "216,99 − 28,32", "R$ 188,67"),
    ("Ponto de equilíbrio", "(7.234 − 560) ÷ 188,67", "35,4 noites"),
    ("Ocupação de equilíbrio", "35,4 ÷ 124", "28,5%"),
    ("Meses de fôlego", "(13.620 + 0) ÷ 7.234", "1,9 meses"),
]
CAUSAS = [
    ("1", "Despesas anuais sem provisão", "duodécimos em zero", "Dividir seguro, licenças, impostos anuais e décimo terceiro por doze e lançar todo mês."),
    ("2", "Sem reserva para a baixa", "reservas separadas em zero", "Abrir conta separada e programar a transferência no dia em que a receita entra."),
    ("3", "Retirada não lançada", "retirada em zero sem a marcação consciente", "Fazer a Conta da Retirada e lançar como custo fixo."),
    ("4", "Diária abaixo do custo real", "diária média real menor que o custo por noite vendida", "Calcular o piso e revisar a diária (Módulo 3)."),
    ("5", "Custo variável mal medido ou alto", "variável por noite igual ou maior que metade da diária real", "Três meses de notas por item; limpeza medida por estadia."),
    ("6", "Deduções acima da faixa", "dedução real acima de 25% da receita bruta", "Conciliar repasses canal por canal e rever o mix (Módulo 3)."),
    ("7", "Ocupação de equilíbrio acima de 70%", "modelo exige ocupação que o destino não entrega", "Diária primeiro, depois variável, depois fixo."),
]
CHECK = [
    ("Extrato da conta da hospedagem do mês inteiro", "com saldo do dia 1 e do último dia. Sem conta separada, separe as linhas no extrato pessoal: resolver isso é a primeira ação."),
    ("Relatório de repasse de cada canal", "o que o hóspede pagou, comissão, processamento e o que caiu na conta. A dedução real sai daqui."),
    ("Notas e comprovantes de tudo o que saiu", "o que não tem comprovante entra como estimativa e fica marcado."),
    ("O mês", "dias, unidades, noites vendidas e estadias. Noites vendidas nunca passam de unidades × dias."),
    ("O que entrou, separado em três", "receita de hospedagem (só diárias), taxa de limpeza cobrada (repasse) e outras receitas com o custo delas."),
    ("O que saiu com cada noite e o que sai todo mês", "cada linha no seu bloco. Despesas anuais divididas por doze, mesmo no mês em que não saíram."),
    ("A sua retirada", "com valor definido, ou a marcação consciente \"decidi retirada zero por enquanto\". Retirada em branco não é fechamento."),
    ("A cascata bate?", "bruta − deduções = real; − variáveis = margem de contribuição; − fixos com a retirada = resultado operacional. Dedução acima de 25%: concilie por canal."),
    ("Caixa e resultado lidos juntos", "saldo final = inicial + entradas − saídas; fôlego = (saldo + reservas) ÷ fixo. Desencontro entre os dois tem explicação: escreva em uma linha."),
    ("Uma prioridade com prazo", "na ordem da fonte: duodécimos → reserva → retirada → diária e custo. Escreva a ação, marque a data, baixe o PDF e guarde."),
]

html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Resumo · Módulo 2 · Finanças, fluxo de caixa e fechamento · Jornada de Gestão</title><style>{CSS}</style></head><body>

<section class="pg capa"><img src="{(BR/'zion-logo-claro.png').as_uri()}" alt="Zion"><div><div class="k">Jornada de Gestão · Módulo 2 · Resumo da aula</div><h1>Movimento <i>não é lucro.</i></h1><p>Finanças, fluxo de caixa e fechamento. O que ficou da aula em oito páginas: faturamento, receita real e lucro; a classificação das saídas; a cascata e os indicadores; um exemplo didático; como analisar o mês; o checklist do fechamento; o critério de conclusão e a próxima etapa.</p></div><div class="k" style="font-size:9pt">Aprenda o passo a passo · Zion Hotel Academy · Método Zion 360°</div></section>

<section class="pg"><h2>1. Faturamento, receita real e lucro</h2>
<div class="cita">“Faturamento, lucro, caixa e margem são quatro coisas diferentes, e confundi-las é o erro mais comum do setor.”<small>Panorama do Desenvolvimento Hoteleiro · Trilha B · Pilar G6 “Administração e Finanças”</small></div>
<div class="grid"><div class="card"><b>Faturamento (receita bruta)</b><small>O que o hóspede pagou pelas diárias. É o número que todo mundo sabe e, sozinho, engana.</small></div><div class="card"><b>Receita real</b><small>O que chegou de fato, depois de descontos, comissões, taxa de processamento e imposto sobre a receita.</small></div><div class="card"><b>Lucro (resultado operacional)</b><small>O que sobra depois de todos os custos, inclusive o do seu trabalho. Na Folha: “quanto sobrou do mês”.</small></div><div class="card"><b>Caixa</b><small>O dinheiro na conta hoje. Pode ser repasse que ainda vai sair, ou alta temporada que vai pagar a baixa.</small></div></div>
<p>Entre o que o hóspede pagou e o que chegou na conta, a fonte avisa: <i>“A diferença costuma ser de 15% a 25%.”</i> <span class="fonte">(Jornada do COMO · Etapa 09 · Passo 04)</span>. Por isso a Folha começa pela receita real, não pelo faturamento.</p>
<h3>Caixa × resultado: as três contas</h3>
<div class="cita">“Dá para ter dinheiro na conta e estar perdendo dinheiro.”<small>Jornada do COMO · Etapa 09 “Como eu sei se estou lucrando?” · Passo 01</small></div>
<table><tr><th>Conta</th><th>Pergunta que responde</th><th>Onde se vê</th><th>Com que frequência</th></tr>
<tr><td><b>Caixa</b></td><td>Tem dinheiro?</td><td>Extrato da conta da hospedagem</td><td>Toda semana, 5 minutos</td></tr>
<tr><td><b>Resultado</b></td><td>Está dando lucro?</td><td>A Folha Única do Mês</td><td>Todo mês, 10 minutos</td></tr>
<tr><td><b>Patrimônio</b></td><td>O que é meu?</td><td>Bens, reservas e dívidas</td><td>Uma vez por trimestre</td></tr></table>
<p><b>Lidas juntas, as duas primeiras explicam o mês.</b> Caixa bom com resultado ruim é típico de alta temporada, ou de repasse que ainda vai sair. Caixa ruim com resultado bom costuma ser investimento ou pagamento concentrado num mês só. Os dois ruins ao mesmo tempo são dois alertas, não um.</p>
<p class="fonte">Fonte das três contas e dos desencontros: Etapa 09 · Passo 01 e Separador das Três Contas. “Repasse que ainda vai sair”: Panorama · Pilar G6.</p>{ROD}</section>

<section class="pg"><h2>2. A classificação das saídas</h2>
<p>Cada saída cai em um de cinco blocos, na ordem da cascata da página seguinte. Errar o bloco não muda o total que saiu, mas muda a leitura de cada indicador.</p>
<table><tr><th style="width:27%">Bloco</th><th>O que é</th><th>Exemplos</th></tr>{''.join(tr([f'<td><b>{a}</b></td>', f'<td>{b}</td>', f'<td>{c}</td>']) for a, b, c in CLASSIF)}</table>
<div class="grid"><div class="card"><b>Taxa de limpeza cobrada do hóspede</b><small>Não é receita. É repasse: abate o custo de limpeza que você paga. Se cobrar mais do que paga, o excedente vai para outras receitas; se cobrar menos, a diferença fica no custo variável.</small></div><div class="card"><b>Limpeza é por estadia, não por noite</b><small>Estadia curta custa mais por noite. Por isso a Folha pede o número de estadias, além das noites vendidas. <span class="fonte">(Etapa 09 · Passo 05)</span></small></div></div>
<div class="cita">“A retirada tem valor definido, data definida e sai sempre igual, como um salário.”<small>Jornada do COMO · Etapa 09 · Passo 03 · Conta da Retirada</small></div>
<p>Conta da Retirada: horas por semana × custo por hora × 4,33. Se decidir não retirar nada por enquanto, marque isso de propósito na Folha. Retirada em branco não é fechamento; retirada zero decidida é.</p>
<div class="caixa"><h3>Parâmetros de referência Zion <span class="ref">referência ajustável, nunca universal</span></h3>
<ul><li><b>Deduções sobre as diárias: 17%</b>, sendo 15% de impostos sobre a receita e comissões mais 2% de cancelamentos e faltas. Serve para começar sem o extrato na mão; o seu número sai do relatório de repasse de cada canal.</li><li><b>Quebra e perda: 1%</b> da receita bruta de diárias, como custo variável, até medir três meses de notas.</li><li><b>Reserva de reposição: 3 a 6%</b> da receita, padrão 4%. <span class="fonte">(Etapa 09 · Passo 06)</span></li></ul></div>
<p class="fonte">Convenção declarada: as comissões de canal entram na dedução, como na cascata do modelo financeiro Zion; a Etapa 09 as põe no custo variável. O resultado do mês é o mesmo; muda só o bloco.</p>{ROD}</section>

<section class="pg"><h2>3. A cascata e os indicadores</h2>
<p>O resultado se monta sempre na mesma ordem; cada linha nasce da anterior. Em separado, o <b>bloco de caixa</b> (saldo inicial + entradas − saídas = saldo final) nunca se mistura com a cascata.</p>
<ol class="casc"><li><b>Receita bruta de hospedagem</b> (só diárias; a taxa de limpeza repassada fica fora)</li><li>− deduções = <b>receita real de hospedagem</b>; + outras receitas = <b>receita real total</b></li><li>− custos variáveis = <b>margem de contribuição</b></li><li>− custos fixos operacionais, com a retirada dentro = <b>resultado operacional</b> (quanto sobrou do mês)</li><li>− custos do modelo; − reserva de reposição (caixa) <i>ou</i> depreciação (contábil), nunca as duas = <b>o que ficou para o negócio</b></li></ol>
<table><tr><th style="width:26%">Indicador</th><th style="width:40%">A conta</th><th>Para que serve</th></tr>{''.join(tr([f'<td><b>{a}</b></td>', f'<td>{b}</td>', f'<td>{c}</td>']) for a, b, c in INDIC)}</table>
<h3>As réguas da fonte</h3>
<div class="grid"><div class="card"><b>Ocupação de equilíbrio</b><small>“Acima de 70% é sinal de alerta” e exige correção estrutural; “entre 45% e 65% é saudável na maior parte dos destinos”. <span class="fonte">Etapa 09 · Passo 09</span></small></div><div class="card"><b>Meses de fôlego</b><small>Abaixo de dois meses, zona de risco; de quatro a seis, confortável. <span class="fonte">Etapa 09 · Passo 12</span></small></div><div class="card"><b>Deduções</b><small>A faixa da fonte é de 15% a 25% da receita bruta. Acima disso, concilie os repasses canal por canal. <span class="fonte">Etapa 09 · Passo 04</span></small></div><div class="card"><b>A diária em três faixas (vale antes de dar desconto)</b><small>Acima do custo por noite vendida: cada noite paga tudo e sobra. Entre o variável e o total: paga o variável e ajuda no fixo, mas o mês não fecha. Abaixo do variável: cada noite consome valor. <span class="fonte">Etapa 09 · Passo 08</span></small></div></div>{ROD}</section>

<section class="pg"><h2>4. Exemplo aplicado</h2>
<div class="ex compacto"><b class="rot">Exemplo didático · dados fictícios</b>
<p style="font-size:9.8pt"><b>Cabanas do Vale</b>, quatro unidades, dona que opera sozinha (a mesma do Marco Zero). Outubro, 31 dias: 124 noites disponíveis, 58 vendidas em 25 estadias; ocupação 46,8%. Taxa de limpeza cobrada R$ 1.500 (25 × 60), limpeza paga R$ 2.000 (25 × 80): limpeza líquida R$ 500. Retirada: 20 h × R$ 40 × 4,33 = R$ 3.464.</p>
<table><tr><th>A cascata do mês</th><th class="n">R$</th></tr>{''.join(tr([f'<td>{a}</td>', f'<td class="n">{b}</td>'], c) for a, b, c in CASCATA)}</table>
<table><tr><th>Indicador</th><th>A conta</th><th class="n">Valor</th></tr>{''.join(tr([f'<td><b>{a}</b></td>', f'<td>{b}</td>', f'<td class="n">{c}</td>']) for a, b, c in EX_IND)}</table>
<p style="margin:0;font-size:9.8pt"><b>Caixa do mês:</b> saldo inicial 9.800 + entradas 18.470 − saídas 14.650 = saldo final R$ 13.620; reservas separadas R$ 0. Dedução real 22,5%; margem operacional 24,8% sobre R$ 17.220 de receita bruta total.</p></div>
<p><b>Leitura:</b> cada noite vendida paga tudo e sobra (diária real acima do custo por noite vendida); ocupação de equilíbrio folgada; caixa bom e resultado bom. Mas o fôlego de 1,9 meses está na zona de risco, porque não há reserva separada. É isso que define a prioridade do mês seguinte. O exemplo mostra como a conta se monta e se lê; o resultado de cada hospedagem depende dos seus números reais.</p>
{ROD}</section>

<section class="pg"><h2>5. Como analisar o mês</h2>
<p>Primeiro, caixa e resultado lidos juntos (página 2). Depois, a fonte lista as causas de “faturar muito e não sobrar” e a ordem para corrigir: <b>despesas anuais em duodécimos → reserva para a baixa → retirada → diária e custo</b> <span class="fonte">(Etapa 09 · Passos 02 e 11)</span>. A ficha percorre os sinais nessa ordem e a primeira que dispara é a causa principal do mês:</p>
<table><tr><th style="width:5%">#</th><th style="width:27%">Causa</th><th style="width:30%">Sinal na Folha</th><th>Ação</th></tr>{''.join(tr([f'<td>{n}</td>', f'<td><b>{a}</b></td>', f'<td>{b}</td>', f'<td>{c}</td>']) for n, a, b, c in CAUSAS)}</table>
<p>Se nenhum sinal disparar: mês dentro das réguas. Compare com o mesmo mês do ano anterior e mantenha a rotina.</p>
<h3>As três prioridades</h3>
<p>A Folha lista até três prioridades para o mês seguinte: a causa principal e as duas seguintes que dispararam. Três, não dez: o fechamento serve para decidir.</p>
<div class="ex"><b class="rot">Exemplo didático · dados fictícios</b><p style="margin:0"><b>Cabanas do Vale:</b> duodécimos existem (R$ 460) e a retirada está lançada. Reservas separadas em zero: causa principal, <b>sem reserva para a baixa</b>. Prioridades: 1 · abrir a conta de reservas e programar a transferência no dia em que a receita entra; 2 · confirmar a diária com o piso (Módulo 3); 3 · medir o café fora de “outras receitas”.</p></div>
<h3>O plano de ação</h3>
<p>Uma ação por escrito, com prazo, ligada à prioridade 1. Ela entra no PDF da Folha, a página 2 do seu Plano de Gestão. No fechamento seguinte, a primeira pergunta é: a ação foi feita? Depois, uma linha na aba Histórico da planilha com o que explicou o mês, para comparar com o mesmo mês do ano que vem.</p>{ROD}</section>

<section class="pg"><h2>6. Faça agora</h2>
<p>Abra a ficha <b>A minha Folha Única do Mês</b> (link na aula). Sete telas, de 15 a 25 minutos: o mês, o que entrou, o que saiu com cada noite, o que sai todo mês, custos do modelo e reserva, o caixa. Cada pergunta diz por que importa e onde conseguir o número; sem o extrato, use a referência Zion e ajuste depois. No fim, a ficha monta a cascata, os indicadores, as leituras e as três prioridades, e gera o PDF. As respostas ficam só no seu aparelho. A planilha <b>Folha Única do Mês</b> (em branco e exemplo) calcula a mesma cascata e acompanha doze meses de caixa.</p>
<h3>Checklist do fechamento · 10 itens, sempre na mesma ordem</h3>
<p style="font-size:9.6pt;margin-bottom:1.5mm">Dez minutos por mês. Marque Sim ou Não; se algum item ficar em Não, o fechamento não está pronto.</p>
<ol class="check">
<li style="list-style:none;margin-left:-5mm" class="fonte"><b>O que juntar</b></li>{''.join(f'<li value="{i+1}"><b>{a}</b>: {b}</li>' for i, (a, b) in enumerate(CHECK[0:3]))}
<li style="list-style:none;margin-left:-5mm" class="fonte"><b>O que lançar</b></li>{''.join(f'<li value="{i+4}"><b>{a}</b>: {b}</li>' for i, (a, b) in enumerate(CHECK[3:7]))}
<li style="list-style:none;margin-left:-5mm" class="fonte"><b>O que conferir</b></li>{''.join(f'<li value="{i+8}"><b>{a}</b>{"" if a.endswith("?") else ":"} {b}</li>' for i, (a, b) in enumerate(CHECK[7:9]))}
<li style="list-style:none;margin-left:-5mm" class="fonte"><b>O que decidir</b></li>{''.join(f'<li value="10"><b>{a}</b>: {b}</li>' for a, b in CHECK[9:10])}
</ol>
<div class="caixa"><h3>Critério de conclusão do Módulo 2</h3><ul style="columns:2;column-gap:6mm"><li>Folha com receita de hospedagem maior que zero (ou marcada como projeção de quem vai abrir) e noites vendidas informadas.</li><li>Pelo menos um custo variável e um custo fixo lançados.</li><li>Retirada informada, ou decidida como zero de propósito.</li><li>Bloco de caixa com saldo inicial e saldo final.</li><li>Plano de ação com uma ação escrita e um prazo.</li><li>PDF da Folha baixado e guardado.</li></ul></div>{ROD}</section>

<section class="pg"><h2>7. A próxima etapa</h2>
<p>Com a Folha na mão, você sabe o custo por noite vendida. A jornada segue para o <b>Módulo 3 · Preço, reservas e distribuição</b>: o piso de tarifa por escrito, calculado a partir desse custo, o calendário único e as regras por canal. É lá que a prioridade “confirmar a diária com o piso” se resolve.</p>
<h3>A rotina que sustenta o fechamento</h3>
<div class="grid grid3"><div class="card"><b>Toda semana · 5 minutos</b><small>Conferir o saldo, as entradas e se a transferência da reserva saiu. Não é hora de analisar nada.</small></div><div class="card"><b>Todo mês · 10 minutos</b><small>Preencher a Folha, ler as réguas, escrever a prioridade com prazo e uma linha no Histórico.</small></div><div class="card"><b>A comparação que informa</b><small>Sempre contra o mesmo mês do ano anterior, nunca contra o mês passado. Alta e baixa temporada não se comparam.</small></div></div>
<div class="cita">“A comparação que informa é contra o mesmo mês do ano anterior, nunca contra o mês passado.”<small>Jornada do COMO · Etapa 09 · Passo 13</small></div>
<h3>Prompt de IA · revisar o fechamento</h3>
<p>Depois de exportar a Folha, cole o prompt publicado em <b>{URL_PROMPT.replace('https://', '')}</b> em qualquer assistente de IA e, em seguida, a sua Folha. Em resumo, o prompt pede ao assistente que, sem inventar parâmetros, sem prometer resultado e sem dar nota própria:</p>
<ul><li><b>A)</b> confira a classificação linha a linha (taxa de limpeza como receita, comissão no bloco errado, café lançado duas vezes, retirada em branco, despesa anual inteira num mês só);</li><li><b>B)</b> refaça a cascata e os indicadores com os seus números e mostre a conta;</li><li><b>C)</b> aplique só as réguas da fonte e aponte a causa principal pela ordem de correção;</li><li><b>D)</b> formule três perguntas para o fechamento do mês seguinte.</li></ul>
<p class="fonte">O assistente não substitui o seu contador nem a sua leitura: ele confere a lógica e faz perguntas. Não cole dados pessoais de hóspedes nem senhas.</p>
<h3>Fontes</h3>
<p class="fonte">Jornada do COMO · Etapa 09 “Como eu sei se estou lucrando?” (Passos 01 a 13: três contas, Mapa de Receita Real, Tabela de Custo Variável, Tabela de Custo Fixo, Conta da Retirada, Custo por Diária Vendida, Ponto de Equilíbrio Zion, Folha Única Zion, rotina). Panorama do Desenvolvimento Hoteleiro · Trilha B · Pilar G6 “Administração e Finanças” (lema “Movimento não é lucro”; caixa separado de resultado; conciliação de repasses). Convenções declaradas nesta lição: cascata do modelo financeiro Zion (comissões na dedução; custos do modelo depois do resultado operacional; reserva ou depreciação), referência Zion 17% = 15% + 2% e quebra 1%. As faixas “folgada” (abaixo de 45%) e “apertado” (2 a 4 meses) são elaborações declaradas, não réguas da fonte.</p>
<p class="fonte">Material educacional da Zion Hotel Academy · Método Zion 360°. Não é promessa de renda, retorno, ocupação ou resultado: o fechamento depende dos números reais de cada hospedagem.</p>{ROD}</section>
</body></html>"""
(B / "resumo.html").write_text(html, encoding="utf-8")
print("ok", B / "resumo.html"); print("ok", MAT / "Modulo-2-Prompt-de-IA.txt")

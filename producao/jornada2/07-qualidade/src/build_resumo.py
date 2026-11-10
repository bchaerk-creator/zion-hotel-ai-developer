"""Gera o HTML do resumo da aula do Módulo 7 (Qualidade, reputação e plano de crescimento) e o TXT do prompt de IA.
Depois, src/render_pdf.js imprime o HTML em PDF (8 páginas A4: capa + 7).
Uso: python3 -I src/build_resumo.py <pasta-build>
Saídas: <pasta-build>/resumo.html e docs/trilha2/materiais/Modulo-7-Prompt-de-IA.txt"""
import sys, pathlib, re
B = pathlib.Path(sys.argv[1]); B.mkdir(parents=True, exist_ok=True)
HERE = pathlib.Path(__file__).resolve().parent; LICAO = HERE.parent
REPO = LICAO.parents[2]; F = REPO / "docs/assets/fonts"; BR = REPO / "docs/brand"
MAT = REPO / "docs/trilha2/materiais"; MAT.mkdir(parents=True, exist_ok=True)
URL_PROMPT = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/trilha2/materiais/Modulo-7-Prompt-de-IA.txt"

md = (LICAO / "PROMPT_IA.md").read_text(encoding="utf-8")
bloco = re.search(r"```\n(.*?)```", md, re.S).group(1).strip()
txt = ("PROMPT DE IA · REVISAR O PLANO DE GESTÃO PROFISSIONAL\n"
       "Zion Hotel Academy · Jornada de Gestão · Módulo 7 · Qualidade, reputação e plano de crescimento\n\n"
       "Como usar: baixe o seu Plano de Gestão Profissional em PDF no Montador do Plano, abra qualquer assistente de IA, "
       "cole o prompt abaixo inteiro e, logo depois, cole o conteúdo do Plano (ou anexe o PDF). O assistente não substitui a sua decisão: "
       "ele confere a lógica e faz perguntas. Não cole nome completo, documento ou telefone de hóspedes nem da equipe, nem senhas.\n\n"
       "----- COPIE DAQUI PARA BAIXO -----\n\n" + bloco + "\n\n----- FIM DO PROMPT -----\n\n"
       "Depois da revisão, ajuste a página 7 no Montador, baixe o PDF de novo e marque as datas da rotina no calendário com alarme.\n"
       "Conteúdo educacional. Não é promessa de renda, retorno ou resultado.\n")
(MAT / "Modulo-7-Prompt-de-IA.txt").write_text(txt, encoding="utf-8")

CSS = f"""
@font-face{{font-family:Cormorant;src:url('{(F/'cormorant.woff2').as_uri()}')}} @font-face{{font-family:Cormorant;font-style:italic;src:url('{(F/'cormorant-italic.woff2').as_uri()}')}} @font-face{{font-family:Aventa;src:url('{(F/'aventa.woff2').as_uri()}')}}
:root{{--musgo:#1B2117;--verde:#16261C;--creme:#FEF5F0;--areia:#DED6BF;--terra:#8B714E;--ouro:#C9B37E;--texto:#1B2117;--cinza:#5A5F55}}
@page{{size:A4;margin:0}} *{{box-sizing:border-box}}
body{{margin:0;font-family:Aventa,Arial,sans-serif;color:var(--texto);background:#fff;font-size:10.3pt;line-height:1.37}}
.pg{{width:210mm;height:297mm;padding:19mm 20mm 20mm;page-break-after:always;position:relative;overflow:hidden}}
.pg:last-child{{page-break-after:auto}}
.capa{{background:var(--musgo);color:var(--creme);display:flex;flex-direction:column;justify-content:space-between;padding-top:22mm}}
.capa img{{height:16mm;align-self:flex-start}} .capa .k{{color:var(--ouro);letter-spacing:.2em;text-transform:uppercase;font-weight:700;font-size:10pt}}
.capa h1{{font-family:Cormorant,serif;font-weight:500;font-size:46pt;line-height:1.02;margin:6mm 0 5mm}} .capa h1 i{{color:var(--ouro)}}
.capa p{{color:var(--areia);font-size:13pt;max-width:140mm}}
h2{{font-family:Cormorant,serif;font-weight:500;font-size:25pt;line-height:1.1;margin:0 0 3.5mm;color:var(--verde)}}
h3{{font-size:9.8pt;letter-spacing:.14em;text-transform:uppercase;color:var(--terra);margin:4mm 0 1.8mm}}
p{{margin:0 0 2.5mm}} ul,ol{{margin:0 0 2.5mm;padding-left:5mm}} li{{margin-bottom:1mm}}
.cita{{font-family:Cormorant,serif;font-style:italic;font-size:15pt;line-height:1.22;border-left:3px solid var(--ouro);padding-left:6mm;margin:3mm 0;color:var(--verde)}} .cita small{{display:block;font-family:Aventa,sans-serif;font-style:normal;font-size:8.5pt;color:var(--cinza);margin-top:1.5mm;letter-spacing:.1em;text-transform:uppercase}}
table{{width:100%;border-collapse:collapse;font-size:8.9pt;margin:2mm 0 3mm;line-height:1.28}} th,td{{text-align:left;padding:1.2mm 2mm;border-bottom:1px solid var(--areia);vertical-align:top}} th{{background:var(--musgo);color:var(--creme);font-weight:600}}
td.n,th.n{{text-align:right;white-space:nowrap}} tr.tot td{{background:#F6F1E6;font-weight:700}}
.ex{{background:#F6F1E6;border:1px solid var(--areia);border-radius:4mm;padding:3.6mm 5mm;margin:3mm 0}} .ex b.rot{{display:block;font-size:9pt;letter-spacing:.14em;text-transform:uppercase;color:#A0522D;margin-bottom:2mm}} .ex table{{background:#fff}}
.caixa{{border:1px dashed var(--terra);border-radius:4mm;padding:3.4mm 5.5mm;margin:3mm 0}} .caixa h3{{margin-top:0}}
.rod{{position:absolute;left:20mm;right:20mm;bottom:10mm;font-size:8.5pt;color:var(--cinza);display:flex;justify-content:space-between;gap:8mm;border-top:1px solid var(--areia);padding-top:2mm}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:3.2mm;margin:2mm 0 3mm}} .grid3{{grid-template-columns:1fr 1fr 1fr}} .card{{border:1px solid var(--areia);border-radius:3mm;padding:2.5mm 3.2mm;font-size:9.4pt}} .card b{{display:block;color:var(--verde);margin-bottom:.8mm}} .card small{{color:var(--cinza);font-size:8.9pt;line-height:1.3;display:block}}
.fonte{{font-size:8.8pt;color:var(--cinza)}} .ref{{display:inline-block;background:var(--areia);color:var(--musgo);font-size:8.5pt;padding:.3mm 2mm;border-radius:2mm;letter-spacing:.06em;text-transform:uppercase}}
"""
ROD = '<div class="rod"><span>Zion Hotel Academy · Jornada de Gestão · Módulo 7</span><span>Conteúdo educacional. Não é promessa de renda, retorno ou resultado.</span></div>'
def tabela(cab, linhas, larg=None, cls=None):
    th = "".join(f'<th{f" style=\"width:{larg[i]}\"" if larg and larg[i] else ""}>{c}</th>' for i, c in enumerate(cab))
    return f"<table><tr>{th}</tr>" + "".join(f'<tr class="{(cls or {}).get(k, "")}">' + "".join(f"<td>{c}</td>" for c in l) + "</tr>" for k, l in enumerate(linhas)) + "</table>"

PAGS = [("0", "Diagnóstico de Gestão", "Marco Zero", "Nota de gestão, área mais frágil e ação de 30 dias"),
        ("1", "Painel de Gestão", "Planejamento, metas e indicadores", "Cinco indicadores com dono, metas de 12 meses e reunião semanal"),
        ("2", "Folha Única do Mês", "Finanças, fluxo de caixa e fechamento", "Do que o hóspede pagou ao que sobrou; caixa de 12 meses"),
        ("3", "Tabela de Preço e Canais", "Preço, reservas e distribuição", "Piso escrito, calendário de 12 meses e meta de venda direta"),
        ("4", "Marca e Captação", "Marketing e vendas", "Promessa, lista própria e custo por reserva"),
        ("5", "Mapa de Pessoas e Alçadas", "Pessoas e organização das áreas", "Quem faz o quê, até quanto decide, quatro semanas de treino"),
        ("6", "Matriz de Compras e Manutenção", "Compras, estoque e manutenção", "Três cotações, consumo por hóspede e calendário de manutenção"),
        ("7", "Qualidade, reputação e plano de crescimento", "Este módulo", "Nota, resposta às avaliações, padrão mínimo, rotina, teste e plano de saída")]
MEDIA = [("4", "5,00", "4,60", "0,40"), ("9", "5,00", "4,80", "0,20"), ("19", "5,00", "4,90", "0,10"), ("49", "5,00", "4,96", "0,04"), ("99", "5,00", "4,98", "0,02")]
CANAIS = [("Plataforma A", "24", "4,7", "16", "44"), ("Plataforma B", "9", "4,6", "5", "13"), ("Perfil no mapa", "5", "4,9", "4", "15")]
ROTINA = [("Toda semana", "Reunião de gestão com os cinco números, mesmo dia e mesma hora", "30 min", "Panorama · G7"),
          ("Toda semana", "Leitura dos seis indicadores do painel por exceção", "15 min", "Etapa 10 · Passo 10"),
          ("Toda semana", "Saldo, entradas e transferências para as reservas", "5 min", "Etapa 09 · Passo 13"),
          ("Toda semana", "Avaliações respondidas, críticas registradas e uma unidade sorteada contra a foto do padrão", "cerca de 30 min*", "Etapas 07 e 10 · Volume 07"),
          ("Todo mês", "Folha Única, comparada com o mesmo mês do ano anterior; conversa de 40 min com quem opera; taxa de avaliação e nota por dimensão", "10 min + 40 min", "Etapas 07, 09 e 10"),
          ("Todo trimestre", "Recalcular custos, equilíbrio e reservas; revisão de preço; comparar a nota com os concorrentes", "2 h", "Etapas 07 e 09"),
          ("Todo ano", "Refazer a conta inteira e redefinir a retirada", "meio dia", "Etapa 09 · Passo 13")]
FASES = [("1 · Escrever", "O manual mínimo: procedimentos e tabela de critérios, em menos de duas horas por semana", "6 a 10 semanas", "Manual em nuvem e impresso", "16/11/2026 a 10/01/2027"),
         ("2 · Contratar e treinar", "A primeira contratação e as quatro semanas de treino", "cerca de 8 semanas", "Padrão mantido com autonomia", "11/01 a 07/03/2027"),
         ("3 · Acompanhar por exceção", "O painel de seis indicadores, leitura semanal e conversa mensal", "pelo menos 8 semanas", "Dúvidas raras, critérios em uso", "08/03 a 13/06/2027 (14 sem.)"),
         ("4 · Testar", "Catorze dias fora, contato só pelas quatro exceções", "2 semanas", "Ocupação e nota mantidas", "14/06 a 27/06/2027")]

html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Módulo 7 · Qualidade, reputação e plano de crescimento · Resumo</title><style>{CSS}</style></head><body>
<section class="pg capa"><img src="{(BR/'zion-logo-claro.png').as_uri()}" alt="Zion"><div><div class="k">Jornada de Gestão · Módulo 7 · Resumo da aula</div><h1>O Plano inteiro, <i>com data para provar que roda.</i></h1><p>Qualidade, reputação e plano de crescimento. O que ficou da aula em sete páginas: as oito páginas do Plano, a reputação e o protocolo de avaliação, o padrão mínimo, um exemplo didático, a rotina semanal, o teste de prontidão com o plano de saída, o critério de conclusão e a próxima etapa.</p></div><div class="k" style="font-size:9pt">Aprenda o passo a passo · Zion Hotel Academy · Método Zion 360°</div></section>

<section class="pg"><h2>1. O Plano de Gestão Profissional</h2>
<div class="cita">“Estar presente não é gerir.”<small>Panorama do Desenvolvimento Hoteleiro · Trilha B · Pilar G7 Governança e Indicadores</small></div>
<p>Cada módulo da jornada deixou uma página. Guardadas em pastas diferentes, elas não mudam a semana de ninguém. Juntas, com uma rotina e uma data de teste, viram o <b>Plano de Gestão Profissional</b>: o documento que responde à pergunta do pilar G7, «O que acontece se você ficar um mês fora?».</p>
{tabela(["Página", "Entregável", "Módulo", "O que traz"], [[f"<b>{a}</b>", b, c, d] for a, b, c, d in PAGS], ["9%", "27%", "27%", "37%"], {7: "tot"})}
<h3>Como o Montador junta as páginas</h3>
<p>Cada ficha da jornada salva a sua página no aparelho em que foi feita. O Montador lê essas páginas no mesmo aparelho: <b>pronta</b> é a que chegou ao PDF na ficha; <b>em andamento</b>, a que foi começada; <b>ainda não feita</b>, a que não existe ali. As que faltam entram no PDF do Plano com o endereço da ficha, e o módulo só se conclui com as sete prontas.</p>
<p class="fonte">A síntese da Trilha B no Panorama lista os sete entregáveis da gestão (marca, canais, preço, captação, compras, finanças, governança); o Plano reorganiza esses entregáveis na ordem da jornada, com o diagnóstico na frente e a reputação no fim.</p>{ROD}</section>

<section class="pg"><h2>2. A reputação</h2>
<div class="cita">“As dez primeiras avaliações valem mais que o primeiro ano de anúncio.”<small>Panorama · Trilha A · Pilar 07 Lançamento</small></div>
<p>A avaliação é o segundo elemento que o hóspede vê numa lista de resultados, depois da foto e junto com o preço. E ela tem uma propriedade cruel: <b>a média é lenta para subir e rápida para cair quando o volume é pequeno</b>.</p>
<h3>A matemática da média pequena <span class="ref">Volume 07 · capítulo 18</span></h3>
{tabela(["Avaliações de 5 já recebidas", "Média antes", "Média depois de uma de 3", "Queda"], [[a, b, c, d] for a, b, c, d in MEDIA], ["34%", "20%", "28%", "18%"])}
<p>Acumular volume de avaliações boas é a defesa. A ficha generaliza a conta da fonte para o seu caso: média depois de uma avaliação ruim = (nota × avaliações + 3) ÷ (avaliações + 1), com 6 na escala de 10.</p>
<h3>O protocolo de avaliação <span class="ref">Protocolo da Primeira Avaliação™</span></h3>
<div class="grid grid3"><div class="card"><b>Pedir</b><small>Na saída, pessoalmente, quando a estadia foi boa. Nunca por mensagem genérica em massa. A formulação da fonte: avaliações são o que faz uma casa nova ser encontrada, e a sua ajudaria muito.</small></div>
<div class="card"><b>Quando não pedir</b><small>«Resolva primeiro e peça depois, ou não peça.» Pedir a quem teve problema não resolvido é pedir a avaliação ruim por escrito.</small></div>
<div class="card"><b>Responder</b><small>Todas, boas e ruins: a resposta é lida por quem está decidindo. Positiva: curta e específica. Negativa: reconheça, não discuta, diga o que mudou. E espere 24 horas.</small></div></div>
<p class="fonte">Fontes: Método Zion 360° · Volume 07 Lançamento · capítulo 18; Panorama · Trilha A · Pilar 07 («Reputação ruim no começo é a coisa mais cara e mais lenta de consertar neste setor.»). O exemplo de receita por nota do Volume 07 não é usado aqui.</p>{ROD}</section>

<section class="pg"><h2>3. O padrão mínimo</h2>
<p>O padrão mínimo é o conjunto de números que você não deixa abaixar. Abaixo deles, você age na semana, antes de a nota cair. Cada regra vem de uma fonte Zion; o nome "padrão mínimo" é desta jornada.</p>
{tabela(["Regra", "De onde vem"], [
  ["<b>Nota mínima</b>: abaixo dela, contato na hora (a mesma exceção do painel do Módulo 5)", "Etapa 10 · Passo 10"],
  ["<b>Resposta a mensagem em menos de uma hora</b>, sempre, inclusive para quem só pergunta", "Etapa 07 · Passo 05"],
  ["<b>Pelo menos 40% dos hóspedes avaliando</b>; abaixo disso, o pedido não está sendo feito ou não funciona", "Etapa 07 · Passo 06"],
  ["<b>Toda avaliação respondida</b>; a negativa, só depois de 24 horas", "Volume 07 · capítulo 18"],
  ["<b>Crítica repetida três vezes no trimestre</b> vira ajuste de produto, com prazo", "Etapa 07 · Passo 06"],
  ["<b>Uma unidade sorteada por semana</b>, conferida contra a foto do padrão", "Etapa 10 · Passo 10"]], ["72%", "28%"])}
<div class="cita">“Três menções ao mesmo item em um trimestre é um problema de produto, não de hóspede.”<small>A Jornada do COMO · Etapa 07 · Sistema de Avaliações™</small></div>
<h3>O que fazer com as avaliações, além de responder</h3>
<ul><li><b>Registrar toda crítica</b>, mesmo pequena, mesmo dentro de avaliação boa: «A nota cai por padrões, não por casos isolados.»</li>
<li><b>Olhar a nota por dimensão</b> (limpeza, comunicação, localização, custo-benefício): a mais baixa é onde está o trabalho.</li>
<li><b>Comparar com os concorrentes diretos</b>, não com o ideal: estar meio ponto acima dos vizinhos é o que pesa na decisão do hóspede.</li>
<li><b>Usar as boas</b>: as frases mais elogiosas entram na descrição e na página própria, como prova.</li></ul>
<p class="fonte">Volume 07: «o padrão do quarto é a nota da avaliação»; limpeza é o item mais citado quando algo dá errado. Por isso a auditoria por amostragem confere a unidade contra a foto do padrão do Módulo 5.</p>{ROD}</section>

<section class="pg"><h2>4. Exemplo aplicado</h2>
<div class="ex"><b class="rot">Exemplo didático · dados fictícios · Cabanas do Vale (4 unidades)</b>
{tabela(["Canal", "Avaliações", "Nota", "Avaliações em 3 meses", "Estadias em 3 meses"], [list(c) for c in CANAIS] + [["<b>Total</b>", "<b>38</b>", "<b>4,70</b>", "<b>25</b>", "<b>72</b>"]], ["34%", "14%", "12%", "20%", "20%"], {3: "tot"})}
<p><b>Nota 4,7 de 5</b> (178,7 ÷ 38), meta <b>4,8 até 31/10/2027</b> (a mesma do Painel de Gestão), nota mínima 4,7 (a mesma do Mapa de Pessoas). Uma avaliação de 3 levaria a média a <b>4,66</b> ((4,7 × 38 + 3) ÷ 39). <b>Taxa de avaliação 34,7%</b> (25 ÷ 72): abaixo dos 40%. Concorrentes diretos 4,6: <b>0,1 ponto acima</b>. Dimensão mais baixa: limpeza, 4,6. Resposta média de 40 minutos, dentro dos 60.</p>
<p>Sete críticas no trimestre (01/08 a 31/10/2026). <b>"Ralo do chuveiro com cheiro na cabana 3" apareceu três vezes</b>: ajuste de produto, trocar o sifão e incluir o ralo no checklist de limpeza, até <b>30/11/2026</b>. Painel de quatro semanas: duas exceções (nota 4,5 numa semana; gasto 15% acima do previsto em outra) e uma avaliação sem resposta.</p>
<p><b>Protocolo:</b> «Avaliações são o que faz uma casa pequena ser encontrada. Se a estadia foi boa, a sua ajudaria muito.» Sem pedido quando houve problema não resolvido; regra das 24 horas; quem responde: a dona.</p>
<p><b>Plano de crescimento:</b> nota 4,7 → 4,8; venda direta 30% → 40% até 30/06/2027 (Tabela de Preço, Módulo 3). Tempo que sobra: trabalhar sobre o negócio, duas horas por semana para preço e venda direta. Segunda unidade: só a retirada está paga; <b>agora não, faltam 3 de 4 condições</b>.</p></div>
<p>O exemplo mostra como a página 7 se monta e se lê. A nota e a ocupação de cada hospedagem dependem da execução de cada uma.</p>{ROD}</section>

<section class="pg"><h2>5. A rotina semanal</h2>
<p>Uma rotina de trinta minutos por semana olhando os mesmos números faz mais pela gestão do que estar presente todos os dias: presença resolve o caso de hoje, rotina revela a tendência do trimestre. A rotina do Plano junta o que cada módulo pediu.</p>
{tabela(["Quando", "O quê", "Tempo", "Fonte"], [[f"<b>{a}</b>", b, c, d] for a, b, c, d in ROTINA], ["15%", "53%", "14%", "18%"])}
<p class="fonte">* Estimativa desta lição para avaliações e auditoria; a fonte não define o tempo. A rotina financeira inteira soma «cerca de dezesseis horas por ano» (Etapa 09 · Passo 13).</p>
<div class="cita">“O controle financeiro de uma operação pequena não falha por falta de conhecimento: falha por falta de data no calendário.”<small>A Jornada do COMO · Etapa 09 · Passo 13</small></div>
<div class="ex"><b class="rot">Exemplo didático · dados fictícios</b><p style="margin:0">Reunião às segundas, 08:00, com a leitura do painel no mesmo dia (Módulos 1 e 5). Folha Única no dia 5. Revisões trimestrais em 11/01, 11/04, 11/07 e 11/10/2027. Revisão anual em 08/11/2027.</p></div>
<h3>Nada diário, exceto as quatro exceções</h3>
<p>Avaliação abaixo da nota mínima, decisão fora da alçada, ocorrência de segurança ou dano, gasto acima do previsto no percentual definido. O resto espera o relatório semanal.</p>{ROD}</section>

<section class="pg"><h2>6. O teste de prontidão e o plano de saída</h2>
<div class="cita">“Catorze dias fora, sem atender. É o único teste que não admite autoengano.”<small>A Jornada do COMO · Etapa 10 · Passo 12</small></div>
<div class="grid"><div class="card"><b>As regras</b><small>Catorze dias corridos, com pelo menos um fim de semana cheio, em período de ocupação média (nem vale, nem pico). Sem atender mensagem, sem entrar no painel do canal, sem conferir unidade. Contato só pelas quatro exceções, sem aviso especial à equipe.</small></div>
<div class="card"><b>Como ler</b><small>Ocupação e nota mantidas, com no máximo dois contatos: passou. Muitos contatos: falta critério. Nota caiu: falta padrão ou treino. Ocupação caiu sem causa externa: falta quem trabalhe a demanda. «Cada resultado é um diagnóstico com endereço.»</small></div></div>
<p class="fonte">Convenções desta lição: nota mantida = até 0,1 ponto abaixo da média dos três meses (0,2 na escala de 10), porque a fonte diz "dentro da variação normal" sem número; ocupação mantida = igual ou acima da projetada («mantida ou melhor»).</p>
<h3>O Plano de Saída da Operação™ <span class="ref">Etapa 10 · Passo 13</span></h3>
{tabela(["Fase", "O que acontece", "Prazo da fonte", "Sinal de conclusão", "Exemplo didático"], [list(f) for f in FASES], ["18%", "32%", "14%", "17%", "19%"])}
<p>Do início ao teste, de seis a oito meses. No exemplo: 224 dias, <b>7,4 meses</b>.</p>
<div class="grid"><div class="card"><b>O tempo que sobra</b><small>Decida antes: trabalhar sobre o negócio (preço, marca, base própria, relações), construir a segunda unidade ou simplesmente viver. Quem não decide volta para a operação por falta do que fazer.</small></div>
<div class="card"><b>A segunda unidade · quatro condições</b><small>O teste passou; a primeira paga a sua retirada; há reserva para a rampa (12 a 18 meses); há quem supervisione as duas. Faltando uma, a segunda antecipa um problema.</small></div></div>{ROD}</section>

<section class="pg"><h2>7. Faça agora e a próxima etapa</h2>
<p>Abra a ficha <b>O Montador do Plano de Gestão</b> (link na aula). Cinco telas, de 25 a 35 minutos: as páginas que você já fez, a nota e as avaliações, o protocolo e o padrão mínimo, a rotina semanal, e o teste de prontidão com o plano de crescimento. No fim, o Plano inteiro em um PDF. A planilha <b>Qualidade e Reputação</b> (em branco e exemplo) acompanha a semana: avaliações por canal, críticas, painel semanal, teste e plano de saída.</p>
<div class="caixa"><h3>Critério de conclusão do Módulo 7 e da Jornada 2</h3><ul style="columns:2;column-gap:6mm;margin:0"><li>As páginas 0 a 6 prontas no mesmo aparelho.</li><li>Nota, volume de avaliações e meta informados.</li><li>Protocolo escrito: pedido, quando não pedir, positiva, negativa, 24 horas.</li><li>Padrão mínimo definido, com o ajuste da crítica repetida.</li><li>Rotina semanal marcada, com as datas do mês, do trimestre e do ano.</li><li>Teste de prontidão agendado: data, responsável, referências, ocupação média.</li><li>Quatro fases datadas e o tempo que sobra decidido.</li><li>PDF do Plano completo baixado e guardado.</li></ul></div>
<h3>A próxima etapa</h3>
<p>Com o Plano fechado, a jornada segue para a <b>Jornada 3 · Operação</b>: o Manual Operacional Personalizado, com limpeza, chegada e saída, manutenção e experiência do hóspede com padrão escrito. É a parte que mais mexe na nota, e a que o teste das duas semanas vai pôr à prova.</p>
<h3>Prompt de IA · revisar o Plano</h3>
<p>Depois de baixar o Plano, cole o prompt publicado em <b>{URL_PROMPT.replace('https://', '')}</b> em qualquer assistente de IA e, em seguida, o seu Plano. Sem inventar números, sem prometer resultado e sem dar nota, o assistente: <b>A)</b> confere as oito páginas e as contradições entre elas; <b>B)</b> revisa o protocolo e o padrão mínimo; <b>C)</b> confere a rotina, o teste e as fases; <b>D)</b> formula três perguntas para as próximas reuniões.</p>
<h3>Fontes</h3>
<p class="fonte">Panorama do Desenvolvimento Hoteleiro · Trilha B · Pilar G7 e síntese da Trilha B; Trilha A · Pilar 07 Lançamento. Método Zion 360° · Volume 07 Lançamento · capítulo 18 (Protocolo da Primeira Avaliação™). A Jornada do COMO · Etapa 07 · Passos 05 e 06 (Sistema de Avaliações™); Etapa 09 · Passo 13 (Rotina Financeira); Etapa 10 · Passos 10, 12 e 13 (Painel de Acompanhamento™, Teste de Prontidão, Plano de Saída da Operação™). Elaborações declaradas: padrão mínimo como conjunto de regras; tolerância da nota no teste; página pronta = PDF gerado; tempo de avaliações e auditoria na rotina.</p>
<p class="fonte">Material educacional da Zion Hotel Academy · Método Zion 360°. Não é promessa de renda, retorno, ocupação ou resultado: a gestão depende da execução de cada hospedagem.</p>{ROD}</section>
</body></html>"""
(B / "resumo.html").write_text(html, encoding="utf-8")
print("ok", B / "resumo.html"); print("ok", MAT / "Modulo-7-Prompt-de-IA.txt")

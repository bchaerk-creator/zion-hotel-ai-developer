"""Gera o HTML do resumo da aula (texto resumido + exemplo aplicado + critério de conclusão + próxima etapa).
Depois, src/render_pdf.js imprime em PDF. Uso: python3 -I src/build_resumo.py <pasta-build>"""
import sys, pathlib
B = pathlib.Path(sys.argv[1]); B.mkdir(parents=True, exist_ok=True)
REPO = pathlib.Path(__file__).resolve().parents[4]; F = REPO / "docs/assets/fonts"; BR = REPO / "docs/brand"
CSS = f"""
@font-face{{font-family:Cormorant;src:url('{(F/'cormorant.woff2').as_uri()}')}} @font-face{{font-family:Cormorant;font-style:italic;src:url('{(F/'cormorant-italic.woff2').as_uri()}')}} @font-face{{font-family:Aventa;src:url('{(F/'aventa.woff2').as_uri()}')}}
:root{{--musgo:#1B2117;--verde:#16261C;--creme:#FEF5F0;--areia:#DED6BF;--terra:#8B714E;--ouro:#C9B37E;--texto:#1B2117;--cinza:#5A5F55}}
@page{{size:A4;margin:0}} *{{box-sizing:border-box}}
body{{margin:0;font-family:Aventa,Arial,sans-serif;color:var(--texto);background:#fff;font-size:11.8pt;line-height:1.45}}
.pg{{width:210mm;min-height:297mm;padding:22mm 20mm 20mm;page-break-after:always;position:relative}}
.pg:last-child{{page-break-after:auto}}
.capa{{background:var(--musgo);color:var(--creme);display:flex;flex-direction:column;justify-content:space-between}}
.capa img{{height:16mm}} .capa .k{{color:var(--ouro);letter-spacing:.2em;text-transform:uppercase;font-weight:700;font-size:10pt}}
.capa h1{{font-family:Cormorant,serif;font-weight:500;font-size:46pt;line-height:1.02;margin:6mm 0 4mm}} .capa h1 i{{color:var(--ouro)}}
.capa p{{color:var(--areia);font-size:13pt;max-width:140mm}}
h2{{font-family:Cormorant,serif;font-weight:500;font-size:26pt;line-height:1.1;margin:0 0 4mm;color:var(--verde)}}
h3{{font-size:11pt;letter-spacing:.14em;text-transform:uppercase;color:var(--terra);margin:7mm 0 2mm}}
p{{margin:0 0 3mm}} ul{{margin:0 0 3mm;padding-left:5mm}} li{{margin-bottom:1.2mm}}
.cita{{font-family:Cormorant,serif;font-style:italic;font-size:17pt;line-height:1.25;border-left:3px solid var(--ouro);padding-left:6mm;margin:5mm 0;color:var(--verde)}} .cita small{{display:block;font-family:Aventa,sans-serif;font-style:normal;font-size:9pt;color:var(--cinza);margin-top:2mm;letter-spacing:.1em;text-transform:uppercase}}
table{{width:100%;border-collapse:collapse;font-size:10pt;margin:3mm 0 4mm}} th,td{{text-align:left;padding:1.8mm 2.5mm;border-bottom:1px solid var(--areia);vertical-align:top}} th{{background:var(--musgo);color:var(--creme);font-weight:600}}
.ex{{background:#F6F1E6;border:1px solid var(--areia);border-radius:4mm;padding:5mm 6mm;margin:4mm 0}} .ex b.rot{{display:block;font-size:9pt;letter-spacing:.14em;text-transform:uppercase;color:#A0522D;margin-bottom:2mm}}
.caixa{{border:1px dashed var(--terra);border-radius:4mm;padding:4mm 6mm;margin:4mm 0}}
.rod{{position:absolute;left:20mm;right:20mm;bottom:10mm;font-size:8.5pt;color:var(--cinza);display:flex;justify-content:space-between;border-top:1px solid var(--areia);padding-top:2mm}}
.num{{font-family:Cormorant,serif;font-size:40pt;color:var(--ouro);line-height:1}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:4mm}} .card{{border:1px solid var(--areia);border-radius:3mm;padding:3.5mm 4mm}} .card b{{display:block;color:var(--verde)}} .card small{{color:var(--cinza)}}
"""
ROD = '<div class="rod"><span>Zion Hospitality Business · Jornada 2 · Gestão · Marco Zero</span><span>Conteúdo educacional. Não é promessa de renda, retorno ou resultado.</span></div>'
AREAS = [("1 · Planejamento e metas", "Objetivo do ano, metas de ocupação, diária e resultado, revisadas todo mês"), ("2 · Finanças e fluxo de caixa", "Entradas e saídas registradas, fechamento mensal, conta da hospedagem separada da pessoal"),
         ("3 · Preço, reservas e distribuição", "Diária mínima calculada, calendário único, regras por canal"), ("4 · Marketing e vendas", "De onde vêm as reservas, anúncio atualizado, motivo de escolha claro"),
         ("5 · Pessoas", "Quem faz o quê, escala, treinamento de entrada, padrão de cada tarefa"), ("6 · Compras, fornecedores e estoque", "Lista de fornecedores, compra por lista, estoque mínimo"),
         ("7 · Limpeza, manutenção e padrão", "Checklist de limpeza e liberação, enxoval, ocorrências, manutenção preventiva"), ("8 · Qualidade, reputação e indicadores", "Painel com os cinco números, leitura das avaliações, uma decisão por semana")]
html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Resumo · Marco Zero · Jornada 2 · Gestão</title><style>{CSS}</style></head><body>
<section class="pg capa"><img src="{(BR/'zion-logo-claro.png').as_uri()}" alt="Zion"><div><div class="k">Jornada 2 · Gestão · Marco Zero · Resumo da aula</div><h1>A sua hospedagem funciona. <i>Mas ela é gerida?</i></h1><p>O que ficou da aula em sete páginas: os três ofícios, as cinco perguntas do gestor, as oito áreas da gestão, um exemplo didático, o critério de conclusão e a próxima etapa.</p></div><div class="k" style="font-size:9pt">Aprenda o passo a passo · Zion Hospitality Business · Método Zion 360°</div></section>

<section class="pg"><h2>1. Gerir é o ofício do meio</h2>
<div class="cita">“Desenvolver é escolher o que construir e onde. Administrar é fazer o que foi construído dar lucro. Operar é entregar a mesma coisa todo dia.”<small>Panorama do Desenvolvimento Hoteleiro · Método Zion 360°</small></div>
<p>A hospedagem tem três ofícios e cada um responde a uma pergunta. Desenvolver: o que dá para fazer aqui? (Jornada 1). Gerir: como isso dá lucro? (esta jornada). Operar: como isso se entrega todo dia? (Jornada 3). A maior perda de tempo do setor é tentar resolver o problema da etapa errada.</p>
<h3>O erro mais comum</h3><p>Casa cheia que não deixa dinheiro no fim do mês. Ocupação alta com diária baixa é trabalho sem lucro. Faturamento, lucro, caixa e margem são quatro coisas diferentes, e dá para ter dinheiro na conta e estar perdendo dinheiro.</p>
<div class="grid"><div class="card"><b>Movimento não é lucro</b><small>O saldo da conta pode ser repasse que ainda vai sair, ou alta temporada que vai pagar a baixa.</small></div><div class="card"><b>Estar presente não é gerir</b><small>Gerir é ter os números na mesa e as decisões distribuídas, não ser a pessoa que todo mundo precisa consultar.</small></div><div class="card"><b>Ocupação é vaidade, margem é sobrevivência</b><small>Os dois números só fazem sentido lidos juntos.</small></div><div class="card"><b>Caixa, resultado e patrimônio</b><small>Três contas, três perguntas: tem dinheiro? está dando lucro? o que é meu? Olhadas por semana, por mês e por trimestre.</small></div></div>
<h3>A pergunta que separa negócio de emprego</h3><div class="cita">“Se eu contratasse alguém para fazer exatamente o que eu faço, pagasse o preço de mercado por isso, e saísse da operação, sobraria alguma coisa?”<small>Jornada do COMO · Etapa 09</small></div>
<p>Se não sobraria, hoje a hospedagem paga o seu trabalho, não o seu negócio. Não é um veredito: é o ponto de partida para rever preço, custo e quem faz o quê. A sua retirada é custo da operação e entra na conta como um salário, com valor e data fixos.</p>{ROD}</section>

<section class="pg"><h2>2. Os cinco números do gestor</h2>
<p>Gestão começa com cinco números do mês passado, tirados do extrato e das reservas, não da memória. Para cada um, na ficha, você marca: sei com número, tenho uma ideia, ou não sei.</p>
<table><tr><th>Número</th><th>Como se calcula</th><th>Por que importa</th></tr>
<tr><td><b>1 · Quanto entrou</b></td><td>Receita de hospedagem + outras receitas. A receita real é a bruta menos descontos, comissões e taxas.</td><td>É o único número que todo mundo sabe. Sozinho, engana.</td></tr>
<tr><td><b>2 · Quanto sobrou</b></td><td>Tudo o que entrou menos tudo o que saiu no mês.</td><td>É o resultado, não o saldo. Não é lucro líquido: falta a sua retirada, depreciação e imposto, se não forem lançados.</td></tr>
<tr><td><b>3 · Ocupação</b></td><td>Noites vendidas ÷ (unidades × dias do mês).</td><td>Lida sozinha, é vaidade. Lida com a diária, mostra se o preço está certo.</td></tr>
<tr><td><b>4 · Diária média</b></td><td>Receita de hospedagem ÷ noites vendidas.</td><td>É a diária real, não a de tabela. É ela que entra em todas as contas.</td></tr>
<tr><td><b>5 · Custo por noite vendida</b></td><td>Tudo o que saiu ÷ noites vendidas.</td><td>Em mês de baixa, está no pico. Comparado com a diária média, diz se cada noite paga o seu custo.</td></tr></table>
<p>Definição-padrão de hotelaria, usada na planilha: a <b>receita por noite disponível</b> (receita de hospedagem ÷ noites disponíveis) junta ocupação e diária num número só.</p>
<h3>A rotina mínima</h3><ul><li><b>Toda semana, 5 minutos:</b> conferir o saldo e as entradas. Não é hora de analisar nada.</li><li><b>Todo mês, 10 minutos:</b> fechar o Painel do Mês, comparar com o mesmo mês do ano anterior (nunca com o mês passado) e registrar em uma linha o que explicou o mês.</li><li><b>Todo trimestre, 2 horas:</b> recalcular custo por noite vendida e ponto de equilíbrio; revisar preço.</li><li><b>Todo ano, meio dia:</b> refazer a conta inteira e decidir.</li></ul>{ROD}</section>

<section class="pg"><h2>3. As oito áreas da gestão</h2>
<p>Cada área, em um de três níveis: <b>não existe ou não sei</b> (0), <b>funciona, mas só na minha cabeça</b> (1), <b>funciona com padrão e registro</b> (2). Padrão e registro é quando existe por escrito e outra pessoa conseguiria fazer igual. O que está só na cabeça não dá para medir, delegar nem melhorar.</p>
<table><tr><th>Área</th><th>O que significa “com padrão e registro”</th></tr>{''.join(f'<tr><td><b>{a}</b></td><td>{d}</td></tr>' for a, d in AREAS)}</table>
<p>As oito áreas seguem a Trilha B do Panorama (marca, canais, preço, captação, compras, finanças e governança) e a rotina real das unidades Zion. A área 7 é a ponte para a Jornada 3 · Operação.</p>
<h3>A nota de gestão</h3><p>As oito áreas valem 60 pontos (0 a 16 pontos brutos) e as cinco perguntas valem 40 (0 a 10). Faixas: 0 a 34, <b>gestão no improviso</b>; 35 a 64, <b>gestão em construção</b>; 65 a 100, <b>gestão com método</b>. A área mais frágil é a primeira com 0; sem 0, a primeira com 1. Ela define a ação de 30 dias e o módulo por onde começar.</p>{ROD}</section>

<section class="pg"><h2>4. Exemplo aplicado</h2>
<div class="ex"><b class="rot">Exemplo didático · dados fictícios</b><p><b>Cabanas do Vale</b>, quatro unidades na serra, dona que opera sozinha. Do mês passado, ela sabe quanto entrou e a diária média; tem uma ideia da ocupação; não sabe quanto sobrou nem o custo por noite vendida.</p>
<p>Áreas: metas 0 · finanças 1 · preço 1 · vendas 2 · pessoas 1 · compras 2 · limpeza e manutenção 1 · qualidade e indicadores 0. Rotina: olha os números quando dá; o tempo vai quase todo para a operação; acha que sobraria algo se contratasse alguém, mas nunca fez a conta.</p>
<p><b>Resultado:</b> 8 de 16 pontos nas áreas (30) + 5 de 10 nas perguntas (20) = <span class="num">50</span> de 100. Gestão em construção. Área mais frágil: 1 · Planejamento e metas. Ação de 30 dias: escrever, em uma página, a meta de ocupação, de diária média e de resultado para os próximos 12 meses, com a data de revisão de cada mês. Verificação: a página existe, tem três números e uma data de revisão por mês. Começa pelo Módulo 1.</p>
<p><b>O mesmo mês no Painel do Mês:</b> 124 noites disponíveis, 58 vendidas, R$ 16.240 de hospedagem e R$ 980 de outras receitas; R$ 5.330 de saídas em nove categorias. Ocupação 46,8%; diária média R$ 280; receita por noite disponível R$ 130,97; custo por noite vendida R$ 91,90; sobrou R$ 11.890 antes da retirada da dona. A leitura da planilha: cada noite vendida paga o seu custo e ainda sobra. A conta da retirada é o próximo passo, no Módulo 2.</p></div>
<p>Repare no que o exemplo não diz: ele não promete que a hospedagem vai lucrar mais depois da jornada. Ele mostra onde a gestão está e qual é a primeira decisão. O resultado depende da execução.</p>{ROD}</section>

<section class="pg"><h2>5. Faça agora e critério de conclusão</h2>
<h3>Faça agora</h3><p>Abra a ficha <b>O seu Diagnóstico de Gestão</b> (link na aula). Oito minutos: situação, quem cuida da gestão, as cinco perguntas, as oito áreas em duas telas e a rotina. O resultado vem em cinco partes: o resultado, o que isso significa, atenção, o que fazer nos próximos 30 dias e como verificar. As respostas ficam só no seu aparelho; o PDF é a página zero do seu Plano de Gestão. Depois, feche o mês passado na planilha <b>Painel do Mês</b> (versões em branco e exemplo).</p>
<div class="caixa"><h3 style="margin-top:0">Critério de conclusão do Marco Zero</h3><ul><li>A nota de gestão foi calculada na ficha.</li><li>A ação de 30 dias está escrita, com prazo, na área mais frágil.</li><li>O PDF do diagnóstico foi baixado e guardado.</li><li>Nos 30 dias seguintes: a ação foi feita e o critério de verificação da ficha foi cumprido.</li></ul></div>
{ROD}</section>

<section class="pg"><h2>6. A próxima etapa</h2><p>Siga para o módulo que a ficha apontou. A ordem da Jornada 2:</p>
<table><tr><th>Módulo</th><th>Entregável (página do Plano de Gestão)</th></tr>
<tr><td>1 · Planejamento, metas e indicadores</td><td>Painel de Gestão com cinco indicadores e metas de 12 meses</td></tr><tr><td>2 · Finanças, fluxo de caixa e fechamento</td><td>Folha Única do mês, fluxo de caixa de 12 meses e número de corte</td></tr><tr><td>3 · Preço, reservas e distribuição</td><td>Piso de tarifa por escrito, calendário e mix de canais</td></tr><tr><td>4 · Marketing e vendas</td><td>Marca em uma folha, lista própria e custo por reserva</td></tr><tr><td>5 · Pessoas e organização das áreas</td><td>Mapa de quem faz o quê, com alçada</td></tr><tr><td>6 · Compras, estoque e manutenção</td><td>Matriz de compras e calendário de manutenção</td></tr><tr><td>7 · Qualidade, reputação e plano de crescimento</td><td>Plano de Gestão Profissional completo e teste de prontidão</td></tr></table>
<div class="cita">“Comece sempre pelo pilar que te dá um número. Número tira a conversa do achismo, e quase sempre aponta sozinho para o próximo passo.”<small>Panorama do Desenvolvimento Hoteleiro</small></div>
<p style="font-size:9.5pt;color:var(--cinza)">Fontes Zion: Panorama do Desenvolvimento Hoteleiro (Trilha B · Gestão); Jornada do COMO, Etapas 09 e 10; Manual Oficial do Método Zion 360°; Bíblia Operacional Zion. Material educacional da Zion Hospitality Business. Não é promessa de renda, retorno, ocupação ou resultado: a gestão depende da execução de cada hospedagem.</p>{ROD}</section>
</body></html>"""
(B / "resumo.html").write_text(html, encoding="utf-8"); print("ok", B / "resumo.html")

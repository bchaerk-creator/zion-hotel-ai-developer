"""Gera o HTML do resumo da aula do Módulo 1 (Planejamento, metas e indicadores) e o TXT do prompt de IA.
Depois, src/render_pdf.js imprime o HTML em PDF (7 páginas A4 + capa).
Uso: python3 -I src/build_resumo.py <pasta-build>
Saídas: <pasta-build>/resumo.html e docs/trilha2/materiais/Modulo-1-Prompt-de-IA.txt
Molde: producao/jornada2/02-financas/src/build_resumo.py (mesmo CSS)."""
import sys, pathlib, re
B = pathlib.Path(sys.argv[1]); B.mkdir(parents=True, exist_ok=True)
HERE = pathlib.Path(__file__).resolve().parent; LICAO = HERE.parent
REPO = LICAO.parents[2]; F = REPO / "docs/assets/fonts"; BR = REPO / "docs/brand"
MAT = REPO / "docs/trilha2/materiais"; MAT.mkdir(parents=True, exist_ok=True)

# ---------- Prompt de IA em texto puro (extraído de PROMPT_IA.md, bloco de código) ----------
md = (LICAO / "PROMPT_IA.md").read_text(encoding="utf-8")
bloco = re.search(r"```\n(.*?)```", md, re.S).group(1).strip()
txt = ("PROMPT DE IA · REVISAR O PAINEL DE GESTÃO\n"
       "Zion Hotel Academy · Jornada de Gestão · Módulo 1 · Planejamento, metas e indicadores\n\n"
       "Como usar: exporte o seu Painel de Gestão em PDF (ou copie a aba Metas e donos da planilha), abra qualquer assistente de IA, "
       "cole o prompt abaixo inteiro e, logo depois, cole o conteúdo do painel. O assistente não decide por você: ele confere as contas "
       "e faz perguntas. Não cole dados pessoais de hóspedes nem senhas.\n\n"
       "----- COPIE DAQUI PARA BAIXO -----\n\n" + bloco + "\n\n----- FIM DO PROMPT -----\n\n"
       "Depois da revisão, escreva as três perguntas na primeira linha da aba Reunião semanal da planilha.\n"
       "Conteúdo educacional. Não é promessa de renda, retorno, ocupação ou resultado.\n")
(MAT / "Modulo-1-Prompt-de-IA.txt").write_text(txt, encoding="utf-8")

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

def paginas(BR, ROD):
    logo = (BR / 'zion-logo-claro.png').as_uri()
    return f"""
<section class="pg capa"><img src="{logo}" alt="Zion"><div><div class="k">Jornada de Gestão · Módulo 1 · Resumo da aula</div><h1>Estar presente <i>não é gerir.</i></h1><p>Planejamento, metas e indicadores. O que ficou da aula em sete páginas: o que é governança; os cinco indicadores; as metas de 12 meses; donos e reunião semanal; um exemplo didático; o plano de seis semanas; o critério de conclusão e a próxima etapa.</p></div><div class="k" style="font-size:9pt">Aprenda o passo a passo · Zion Hotel Academy · Método Zion 360°</div></section>

<section class="pg"><h2>1. O que é gerir</h2>
<div class="cita">“Governança é o conjunto de rotinas, indicadores e alçadas que permite a operação funcionar sem o dono presente: painel, metas, reunião semanal, processos escritos e quem decide o quê.”<small>Panorama do Desenvolvimento Hoteleiro · Trilha B · Pilar G7 “Governança e Indicadores”</small></div>
<p>A pergunta central do pilar é simples: <b>o que acontece se você ficar um mês fora?</b> Se a resposta é “tudo para”, a hospedagem depende da sua presença, não de um sistema. Gerir é ter os números na mesa e as decisões distribuídas, não ser a pessoa que todo mundo precisa consultar.</p>
<div class="cita">“Uma rotina de trinta minutos por semana olhando os mesmos cinco números faz mais pela gestão do que estar presente todos os dias, porque presença resolve o caso de hoje e rotina revela a tendência do trimestre.”<small>Panorama · Trilha B · Pilar G7 · Na prática</small></div>
<h3>Os quatro passos da fonte</h3>
<table><tr><th>Passo</th><th>O que fazer</th><th>Onde entra na jornada</th></tr>
<tr><td><b>1 · Escolha cinco indicadores</b></td><td>“Mais que isso ninguém acompanha.”</td><td>Este módulo</td></tr>
<tr><td><b>2 · Defina quem olha cada um</b></td><td>“Indicador sem dono não é acompanhado, é arquivado.”</td><td>Este módulo</td></tr>
<tr><td><b>3 · Marque a reunião semanal</b></td><td>“Trinta minutos, mesmos cinco números, mesma hora.”</td><td>Este módulo</td></tr>
<tr><td><b>4 · Escreva as alçadas</b></td><td>Até que valor cada pessoa decide sem consultar.</td><td>Módulo 5 · Pessoas</td></tr></table>
<p>O Painel de Gestão deste módulo é a página 1 do seu Plano de Gestão. As metas entram aqui também, porque a fonte inclui “metas” na definição de governança.</p>{ROD}</section>

<section class="pg"><h2>2. Os cinco indicadores</h2>
<div class="cita">“Ocupação, diária média, resultado, nota e taxa de venda direta cobrem quase todo caso.”<small>Panorama · Trilha B · Pilar G7 · Passo 01</small></div>
<table><tr><th>Indicador</th><th>Como calcular</th><th>Onde conseguir</th></tr>
<tr><td><b>Ocupação</b></td><td>Noites vendidas ÷ noites disponíveis do mês (unidades × dias).</td><td>Calendário das plataformas.</td></tr>
<tr><td><b>Diária média</b></td><td>Receita de hospedagem ÷ noites vendidas.</td><td>Relatório de ganhos + reservas diretas, sem a taxa de limpeza.</td></tr>
<tr><td><b>Resultado do mês</b></td><td>Tudo o que entrou menos tudo o que saiu, com a sua retirada dentro.</td><td>Folha Única do Mês (Módulo 2) ou Painel do Mês (Marco Zero).</td></tr>
<tr><td><b>Nota das avaliações</b></td><td>Média das avaliações do mês, sempre no mesmo canal.</td><td>Painel de avaliações do canal onde você mais vende.</td></tr>
<tr><td><b>Taxa de venda direta</b></td><td>Receita das reservas diretas ÷ receita de hospedagem.</td><td>Site, WhatsApp, indicação, hóspede que volta.</td></tr></table>
<p class="fonte">Nota e taxa de venda direta não têm definição operacional nas fontes Zion: usamos a definição-padrão de hotelaria, dita como tal. O resultado segue a Folha Única (com a retirada).</p>
<h3>Do Marco Zero ao painel</h3>
<div class="grid grid3"><div class="card"><b>Ficam no painel</b><small>Ocupação, diária média e “quanto sobrou”, que já estavam nos cinco números do Marco Zero.</small></div><div class="card"><b>Vão para a Folha</b><small>“Quanto entrou” e o custo por noite vendida seguem na Folha Única, no Módulo 2.</small></div><div class="card"><b>Entram agora</b><small>A nota das avaliações e a taxa de venda direta.</small></div></div>
<div class="caixa"><h3>O erro mais comum</h3><p>“Trocar indicador toda semana, em busca do painel perfeito. O valor vem da série histórica, e série histórica exige repetir o mesmo número.” <span class="fonte">(Pilar G7 · Erro comum)</span>. Regra prática: não troque de indicador antes de 12 semanas, um trimestre.</p></div>{ROD}</section>

<section class="pg"><h2>3. As metas de 12 meses</h2>
<div class="cita">“Um número, não uma intenção. E o prazo para chegar nele.”<small>Panorama · Trilha B · Pilar G2 · Passo 03 (sobre a meta de venda direta)</small></div>
<p>Cada indicador ganha uma meta para o <b>mesmo mês daqui a 12 meses</b>. A razão vem da Etapa 09: em hospedagem sazonal, comparar um mês com o anterior não diz nada.</p>
<div class="cita">“A comparação que informa é contra o mesmo mês do ano anterior, nunca contra o mês passado.”<small>Jornada do COMO · Etapa 09 · Passo 13 · Rotina Financeira</small></div>
<h3>Como ler a meta</h3>
<table><tr><th>Situação</th><th>O que significa</th></tr>
<tr><td><b>Meta acima do ponto de partida</b></td><td>A direção que você escolheu. Confira a conta que ela pede.</td></tr>
<tr><td><b>Meta igual</b></td><td>Manter também é meta, desde que escrita.</td></tr>
<tr><td><b>Meta abaixo</b></td><td>Pode ser decisão: “Ocupação é vaidade, margem é sobrevivência.” (Panorama, estudo de caso da Trilha B). Escreva o porquê.</td></tr>
<tr><td><b>Sem ponto de partida</b></td><td>“Não sei” é informação. O primeiro mês do painel vira a base.</td></tr></table>
<h3>Duas conferências (Módulo 2)</h3>
<ul><li><b>Ocupação de equilíbrio:</b> a meta de ocupação precisa ficar acima dela; abaixo, as noites vendidas não pagam o custo fixo. O ponto de equilíbrio “transforma uma conta em uma meta visível no calendário” (Etapa 09 · Passo 09).</li>
<li><b>Número de corte:</b> o resultado mensal mínimo abaixo do qual você muda alguma coisa (Pilar G6). A meta de resultado fica acima dele.</li></ul>
<p class="fonte">As fontes Zion não definem um método para o tamanho da meta. A ficha e a planilha só fazem contas (variação, noites e receita que a meta pede) e não dizem qual meta é “certa”: meta é decisão sua, não previsão.</p>{ROD}</section>

<section class="pg"><h2>4. Donos e reunião semanal</h2>
<div class="cita">“Indicador sem dono não é acompanhado, é arquivado.”<small>Panorama · Trilha B · Pilar G7 · Passo 02</small></div>
<p>O dono traz o número na reunião e explica o que mudou. No começo, o dono de tudo pode ser você. Quando houver equipe, dê cada número a quem cuida daquela área: a nota a quem cuida da limpeza e do atendimento, a venda direta a quem responde as mensagens.</p>
<div class="cita">“Trinta minutos, mesmos cinco números, mesma hora. No começo pode ser você sozinho; o que importa é a rotina existir.”<small>Panorama · Trilha B · Pilar G7 · Passo 03</small></div>
<h3>A pauta dos trinta minutos</h3>
<ol class="check"><li><b>Os cinco números</b>, na mesma ordem, cada um pelo seu dono.</li><li><b>O que saiu do esperado</b>, contra a meta e contra o mesmo mês do ano anterior (no primeiro ano, contra a sua projeção).</li><li><b>Uma decisão</b>, com dono e prazo.</li><li><b>Anotar</b> na aba Reunião semanal da planilha.</li></ol>
<p class="fonte">A pauta em quatro itens é elaboração desta aula a partir da fonte. Na rotina das unidades Zion, a semana do gestor inclui verificação financeira, revisão das avaliações e a escala da semana seguinte (Bíblia Operacional Zion · Manual Gerencial).</p>
<h3>Acompanhar por exceção</h3>
<p>Quando a operação já é delegada, a Etapa 10 leva a mesma ideia adiante: <i>“Acompanhamento sustentável é por exceção: você olha indicadores, e só entra quando algo sai do esperado.”</i> <span class="fonte">(Jornada do COMO · Etapa 10 · Passo 10)</span>. O painel deste módulo é o primeiro passo para chegar lá.</p>{ROD}</section>

<section class="pg"><h2>5. Exemplo aplicado</h2>
<div class="ex compacto"><b class="rot">Exemplo didático · dados fictícios</b><p><b>Cabanas do Vale</b>, quatro unidades na serra, dona que opera sozinha (Ana). No Marco Zero, a área mais frágil foi Planejamento e metas. Ela parte de outubro de 2026 (31 dias, 124 noites disponíveis) e ainda não fez a Folha Única.</p>
<table><tr><th>Indicador</th><th class="n">Ponto de partida</th><th class="n">Meta (outubro de 2027)</th><th class="n">Variação</th><th>Dono</th></tr>
<tr><td>Ocupação</td><td class="n">46,8%</td><td class="n">50,0%</td><td class="n">+ 3,2 pontos</td><td>Ana</td></tr>
<tr><td>Diária média</td><td class="n">R$ 280,00</td><td class="n">R$ 300,00</td><td class="n">+ R$ 20,00 (+7,1%)</td><td>Ana</td></tr>
<tr><td>Resultado (antes da retirada)</td><td class="n">R$ 11.890,00</td><td class="n">R$ 13.000,00</td><td class="n">+ R$ 1.110,00 (+9,3%)</td><td>Ana</td></tr>
<tr><td>Nota (escala de 5)</td><td class="n">4,7</td><td class="n">4,8</td><td class="n">+ 0,1 ponto (+2,1%)</td><td>Ana</td></tr>
<tr><td>Taxa de venda direta</td><td class="n">30,0%</td><td class="n">40,0%</td><td class="n">+ 10,0 pontos</td><td>Ana</td></tr></table>
<p><b>O que as metas pedem:</b> 50% de 124 noites = <b>62 noites</b>; 62 × R$ 300 = <b>R$ 18.600,00</b> de hospedagem no mês de chegada. A receita por noite disponível passa de R$ 131,04 (46,8% × R$ 280) para R$ 150,00 (50% × R$ 300): <b>+14,5%</b>.</p>
<p><b>Reunião:</b> toda segunda-feira, 08:00, 30 minutos, Ana sozinha com a planilha. Primeira reunião: 16/11/2026.</p>
<p><b>Atenção:</b> o resultado está antes da retirada da dona. Quando ela fizer a Folha Única, o resultado de outubro com a retirada é R$ 4.269,20 e a ocupação de equilíbrio 28,5%: ela refaz o ponto de partida e a meta de resultado.</p>
<p><b>Na planilha (fictício):</b> outubro de 2026 contra outubro de 2025 (41,9%; R$ 265; R$ 10.400; 4,6; 24%): os cinco melhoraram. Novembro de 2026 (38,3%; R$ 285; R$ 8.950; 4,8; 31%) contra novembro de 2025 (40,0%; R$ 270; R$ 9.300; 4,6; 26%): três melhoraram, ocupação e resultado pioraram.</p></div>
<p>Repare no que o exemplo não diz: ele não promete que as metas serão atingidas. Ele mostra como escrevê-las, conferi-las e acompanhá-las. O resultado depende da execução.</p>{ROD}</section>

<section class="pg"><h2>6. O plano de seis semanas</h2>
<div class="cita">“Um pilar por semana não funciona para todo mundo. Escolha três e faça bem.”<small>Panorama · Trilha B · Plano de ação</small></div>
<table><tr><th>Semanas</th><th>Pergunta da fonte</th><th>No exemplo (dados fictícios)</th></tr>
<tr><td><b>1 e 2 · o pilar mais fraco</b></td><td>Qual é, e qual exercício você vai fazer primeiro?</td><td>Módulo 2 · Finanças: fechar outubro na Folha Única e lançar a retirada.</td></tr>
<tr><td><b>3 e 4 · o que destrava o seguinte</b></td><td>Qual pilar está impedindo outro de avançar?</td><td>Módulo 3 · Preço: calcular o piso antes de subir a diária para R$ 300.</td></tr>
<tr><td><b>5 e 6 · o que te dá um número</b></td><td>Qual deles substitui um achismo por um dado?</td><td>Módulo 4 · Marketing e vendas: anotar o canal de cada reserva.</td></tr>
<tr><td><b>Para depois, de propósito</b></td><td>“Escrever isso evita culpa e evita dispersão.”</td><td>Compras e estoque, até o fim da alta temporada.</td></tr></table>
<p>O painel mede se os três pilares estão funcionando: a meta de diária conversa com o Módulo 3, a venda direta com o Módulo 4, o resultado com o Módulo 2.</p>
<h3>Checklist do Painel e da reunião</h3>
<ol class="check"><li>Os cinco números do mês passado (“não sei” vale).</li><li>Uma meta para cada um, para o mesmo mês daqui a 12 meses.</li><li>As duas conferências: equilíbrio e número de corte.</li><li>Um dono para cada número.</li><li>A reunião na agenda: dia, hora, 30 minutos.</li><li>O plano de seis semanas e o que fica para depois.</li><li>Toda semana: os mesmos cinco números, na mesma ordem.</li><li>O que saiu do esperado, contra a meta e o mesmo mês do ano anterior.</li><li>Uma decisão com dono e prazo.</li><li>Anotar na planilha; no fim do mês, lançar o Painel 12 meses.</li></ol>{ROD}</section>

<section class="pg"><h2>7. Faça agora, critério de conclusão e próxima etapa</h2>
<h3>Faça agora</h3><p>Abra a ficha <b>O meu Painel de Gestão</b> (link na aula). Cinco telas, de 15 a 20 minutos: o ponto de partida, as metas de 12 meses, quem olha cada número, a reunião semanal e o plano de seis semanas. O resultado vem em cinco partes: o painel, o que isso significa, atenção, o que fazer nas próximas seis semanas e como verificar. As respostas ficam só no seu aparelho; o PDF é a página 1 do seu Plano de Gestão. Depois, abra a planilha <b>Painel de Gestão</b> (em branco e exemplo) e registre a primeira reunião.</p>
<div class="caixa"><h3>Critério de conclusão do Módulo 1</h3><ul><li>O painel tem as cinco metas e os cinco donos.</li><li>A reunião semanal tem dia, hora e duração.</li><li>O plano de seis semanas tem três pilares diferentes.</li><li>O plano está escrito, com a data da primeira reunião, e o PDF foi baixado.</li><li>Em quatro semanas: a aba Reunião semanal tem quatro linhas com os mesmos cinco números.</li></ul></div>
<h3>Prompt de IA</h3><p>Para uma segunda leitura, use o prompt do módulo (arquivo <b>Modulo-1-Prompt-de-IA.txt</b>, na aba Materiais): ele confere as contas das metas, a coerência entre elas, os donos e a reunião, e sugere três perguntas para a primeira reunião. Não cole dados de hóspedes nem senhas.</p>
<h3>A próxima etapa</h3><p>Siga para o <b>Módulo 2 · Finanças, fluxo de caixa e fechamento</b>: lá o resultado do seu painel ganha a conta completa, com a sua retirada, a ocupação de equilíbrio e o número de corte. Se a sua ficha apontou outro pilar para as semanas 1 e 2, comece por ele.</p>
<p style="font-size:9.5pt;color:var(--cinza)">Fontes Zion: Panorama do Desenvolvimento Hoteleiro (Trilha B · Pilares G2, G6 e G7, estudo de caso e plano de seis semanas); Jornada do COMO, Etapas 09 e 10; Bíblia Operacional Zion (Manual Gerencial). Material educacional da Zion Hospitality Business. Não é promessa de renda, retorno, ocupação ou resultado: metas são decisões de gestão, e o resultado depende da execução de cada hospedagem.</p>{ROD}</section>
"""

ROD = '<div class="rod"><span>Zion Hotel Academy · Jornada de Gestão · Módulo 1</span><span>Conteúdo educacional. Não é promessa de renda, retorno ou resultado.</span></div>'
html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Módulo 1 · Planejamento, metas e indicadores · Resumo</title><style>{CSS}</style></head><body>{paginas(BR, ROD)}</body></html>"""
(B / "resumo.html").write_text(html, encoding="utf-8"); print("ok", B / "resumo.html")

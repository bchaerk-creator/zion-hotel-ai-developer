"""Gera o HTML do resumo da aula do Módulo 5 (Pessoas e organização das áreas) e o TXT do prompt de IA.
Depois, src/render_pdf.js imprime o HTML em PDF (8 páginas A4).
Uso: python3 -I src/build_resumo.py <pasta-build>
Saídas: <pasta-build>/resumo.html e docs/trilha2/materiais/Modulo-5-Prompt-de-IA.txt"""
import sys, pathlib, re
B = pathlib.Path(sys.argv[1]); B.mkdir(parents=True, exist_ok=True)
HERE = pathlib.Path(__file__).resolve().parent; LICAO = HERE.parent
REPO = LICAO.parents[2]; F = REPO / "docs/assets/fonts"; BR = REPO / "docs/brand"
MAT = REPO / "docs/trilha2/materiais"; MAT.mkdir(parents=True, exist_ok=True)
URL_PROMPT = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/trilha2/materiais/Modulo-5-Prompt-de-IA.txt"

# ---------- Prompt de IA em texto puro (bloco de código do PROMPT_IA.md) ----------
md = (LICAO / "PROMPT_IA.md").read_text(encoding="utf-8")
bloco = re.search(r"```\n(.*?)```", md, re.S).group(1).strip()
txt = ("PROMPT DE IA · REVISAR O MAPA DE PESSOAS E ALÇADAS\n"
       "Zion Hotel Academy · Jornada de Gestão · Módulo 5 · Pessoas e organização das áreas\n\n"
       "Como usar: exporte o seu Mapa de Pessoas e Alçadas em PDF (ou copie as abas Tarefas e Alçadas da planilha), abra qualquer assistente de IA, "
       "cole o prompt abaixo inteiro e, logo depois, cole o conteúdo do mapa. O assistente não substitui a sua decisão nem orientação trabalhista: "
       "ele confere a lógica e faz perguntas. Não cole nome completo, documento ou telefone de ninguém da equipe, nem senhas.\n\n"
       "----- COPIE DAQUI PARA BAIXO -----\n\n" + bloco + "\n\n----- FIM DO PROMPT -----\n\n"
       "Depois da revisão, ajuste a aba Alçadas da planilha e imprima a tabela para quem opera. Revise o mapa a cada contratação.\n"
       "Conteúdo educacional. Não é promessa de renda, retorno ou resultado.\n")
(MAT / "Modulo-5-Prompt-de-IA.txt").write_text(txt, encoding="utf-8")

CSS = f"""
@font-face{{font-family:Cormorant;src:url('{(F/'cormorant.woff2').as_uri()}')}} @font-face{{font-family:Cormorant;font-style:italic;src:url('{(F/'cormorant-italic.woff2').as_uri()}')}} @font-face{{font-family:Aventa;src:url('{(F/'aventa.woff2').as_uri()}')}}
:root{{--musgo:#1B2117;--verde:#16261C;--creme:#FEF5F0;--areia:#DED6BF;--terra:#8B714E;--ouro:#C9B37E;--texto:#1B2117;--cinza:#5A5F55}}
@page{{size:A4;margin:0}} *{{box-sizing:border-box}}
body{{margin:0;font-family:Aventa,Arial,sans-serif;color:var(--texto);background:#fff;font-size:10.3pt;line-height:1.37}}
.pg{{width:210mm;height:297mm;padding:19mm 20mm 20mm;page-break-after:always;position:relative;overflow:hidden}}
.pg:last-child{{page-break-after:auto}}
.capa{{background:var(--musgo);color:var(--creme);display:flex;flex-direction:column;justify-content:space-between;padding-top:22mm}}
.capa img{{height:16mm;align-self:flex-start}} .capa .k{{color:var(--ouro);letter-spacing:.2em;text-transform:uppercase;font-weight:700;font-size:10pt}}
.capa h1{{font-family:Cormorant,serif;font-weight:500;font-size:48pt;line-height:1.02;margin:6mm 0 5mm}} .capa h1 i{{color:var(--ouro)}}
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
ROD = '<div class="rod"><span>Zion Hotel Academy · Jornada de Gestão · Módulo 5</span><span>Conteúdo educacional. Não é promessa de renda, retorno ou resultado.</span></div>'
def tr(cells, cls=""): return f'<tr class="{cls}">' + "".join(cells) + "</tr>"
def tabela(cab, linhas, larg=None):
    th = "".join(f'<th{f" style=\"width:{larg[i]}\"" if larg and larg[i] else ""}>{c}</th>' for i, c in enumerate(cab))
    return f"<table><tr>{th}</tr>" + "".join(tr([f"<td>{c}</td>" for c in l]) for l in linhas) + "</table>"

DEP = [("Conhecimento", "Só eu sei como se faz", "Procedimento escrito, de uma página", "6 a 10 semanas (manual mínimo)"),
       ("Decisão", "Tudo fora do padrão me procura", "Critério escrito e alçada", "2 semanas"),
       ("Relação", "Só falam comigo", "Apresentar a pessoa; transição visível para o outro lado", "6 meses a 2 anos"),
       ("Acesso", "Está tudo no meu nome e no meu celular", "Cofre de senhas, acessos nominais, telefone da operação", "Uma tarde")]
ATIV = [("Limpeza e preparação da unidade", "Governança e limpeza", "Baixo · segue roteiro", "Diarista", "0"),
        ("Check-in e check-out", "Hospitalidade e experiência", "Baixo · segue roteiro", "Eu → diarista no plano", "5"),
        ("Resposta a mensagem dos hóspedes", "Hospitalidade e experiência", "Médio · com modelos", "Eu", "6"),
        ("Manutenção e ronda técnica", "Manutenção", "Médio · com modelos", "Auxiliar de manutenção", "1"),
        ("Compras, estoque e fornecedores", "Gerencial e administrativo", "Alto · exige decisão", "Eu", "2"),
        ("Financeiro e administrativo", "Gerencial e administrativo", "Alto · exige decisão", "Eu", "2"),
        ("Preço, calendário e canais", "Comercial e reservas", "Alto · exige decisão", "Eu", "2"),
        ("Pedido e resposta de avaliações", "Cultura e marca", "Médio · com modelos", "Eu", "2")]
CRIT = [("Reserva de última hora", "Quem estiver no plantão", "Aceita até 2 horas antes do check-in, se a unidade estiver pronta e houver alguém para receber.", "sem valor"),
        ("Cortesia e compensação", "Diarista", "Problema reconhecido na unidade: cortesia de até 15% da diária.", "R$ 42"),
        ("Cancelamento fora da política", "A dona", "Motivo de saúde com comprovação: devolve até 50%. Outro motivo: consulta.", "sem valor"),
        ("Manutenção", "Auxiliar de manutenção", "Resolve na hora o que não para a unidade; o que para, avisa na hora.", "R$ 100"),
        ("Compra fora do previsto", "Diarista", "Item da lista padrão compra sem perguntar; fora da lista, consulta.", "R$ 100"),
        ("Hóspede problemático", "Quem estiver no plantão", "Advertência verbal registrada; encerrar a estadia, só com a dona.", "sem valor"),
        ("Erro de calendário e realocação", "A dona", "<i>regra a escrever</i>", "sem valor")]
SEM = [("1 · Sombra", "Acompanha você executando, com o procedimento impresso, e marca o que não estava escrito. Nenhuma execução sozinha.", "20 min no fim da semana", "Procedimento corrigido", "16 a 22/11"),
       ("2 · Execução acompanhada", "Executa e você observa sem interferir. Corrija depois, não durante. Confere contra a foto do padrão.", "20 min por dia", "Resultado bate com a foto", "23 a 29/11"),
       ("3 · Sozinha, com conferência", "Executa sozinha; você confere o resultado, não o processo. Entram critérios e alçada inicial.", "20 min por dia", "Dúvidas caindo, critérios em uso", "30/11 a 06/12"),
       ("4 · Autonomia com alçada", "Executa e decide dentro da alçada. Você olha os seis indicadores.", "2 vezes na semana", "Padrão mantido, decisões razoáveis", "07 a 13/12")]
ERRO = [("De procedimento", "Corrigir o documento e agradecer por ter aparecido", "Reescrever com quem executa"),
        ("De execução", "Conversa no mesmo dia, releitura junto, registro", "Repetição: conversa formal com prazo; refazer a semana 3"),
        ("De critério, com boa intenção", "Ajustar a regra ou a alçada: provavelmente estava vaga", "Reescrever a tabela de critérios"),
        ("De honestidade", "Desligamento, sem escala", "Revisar acessos e alçadas")]

html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Resumo · Módulo 5 · Pessoas e organização das áreas · Jornada de Gestão</title><style>{CSS}</style></head><body>

<section class="pg capa"><img src="{(BR/'zion-logo-claro.png').as_uri()}" alt="Zion"><div><div class="k">Jornada de Gestão · Módulo 5 · Resumo da aula</div><h1>Estar presente <i>não é gerir.</i></h1><p>Pessoas e organização das áreas. O que ficou da aula em oito páginas: as quatro dependências, quem faz o quê, critérios e alçadas, um exemplo didático, as quatro semanas de treino, o painel por exceção, o critério de conclusão e a próxima etapa.</p></div><div class="k" style="font-size:9pt">Aprenda o passo a passo · Zion Hotel Academy · Método Zion 360°</div></section>

<section class="pg"><h2>1. Por que tudo passa por você</h2>
<div class="cita">“Governança é o conjunto de rotinas, indicadores e alçadas que permite a operação funcionar sem o dono presente: painel, metas, reunião semanal, processos escritos e quem decide o quê.”<small>Panorama do Desenvolvimento Hoteleiro · Trilha B · Pilar G7 “Governança e Indicadores”</small></div>
<p>A pergunta que testa a governança: <b>o que acontece se você ficar um mês fora?</b> Na maior parte das hospedagens pequenas, tudo passa por uma pessoa porque nunca foi escrito em lugar nenhum. Não é falta de disciplina nem de gente boa: é estrutura. <b>Alçada</b> é até quanto cada pessoa decide sem consultar você.</p>
<h3>As quatro dependências <span class="ref">Mapa das Quatro Dependências™</span></h3>
{tabela(["Dependência", "Como aparece", "O que resolve", "Prazo da fonte"], [[f"<b>{a}</b>", f"“{b}”", c, d] for a, b, c, d in DEP], ["17%", "28%", "35%", "20%"])}
<p>A de <b>decisão</b> é a mais incapacitante, porque persegue você mesmo de férias. A de <b>acesso</b> é a mais rápida e a mais perigosa de ignorar: se o seu celular sumir, a operação para. Por isso a fonte manda resolvê-la <b>esta semana</b>, seja qual for a mais forte.</p>
<h3>O Inventário da Cabeça™</h3>
<p>Durante uma semana, anote toda vez que você souber de cabeça algo que outra pessoa não saberia: a chave reserva, o fornecedor do sábado, a unidade com o chuveiro que precisa de jeito, quando dar cortesia, as senhas. A lista costuma ter de 40 a 80 linhas. Classifique por frequência, risco e tempo de aprendizado.</p>
<div class="grid"><div class="card"><b>O que costuma aparecer</b><small>Diárias e simples, decisões sem critério e acessos somados costumam passar de 70% da lista, e são as de resolução mais rápida. O que exige treino longo é minoria.</small></div><div class="card"><b>Decisão sem critério parece conhecimento</b><small>Quando a equipe pergunta se pode aceitar uma reserva de última hora, ela está pedindo autorização, não informação. Uma linha de regra elimina a pergunta.</small></div></div>
<p class="fonte">Fonte: Jornada do COMO · Etapa 10 “Como eu saio da operação?” · Passos 01 e 02. Panorama · Pilar G7.</p>{ROD}</section>

<section class="pg"><h2>2. Quem faz o quê</h2>
<p>A Bíblia Operacional Zion organiza a operação em <b>seis setores</b>, um manual para cada: hospitalidade e experiência; governança e limpeza; manutenção; gerencial e administrativo; comercial e reservas; cultura e marca. Na ficha, as oito atividades de uma hospedagem pequena ficam agrupadas nesses setores. Para cada uma: <b>quem faz hoje</b>, <b>quantas horas suas</b> ela leva por semana e <b>quanto julgamento</b> exige.</p>
<h3>Quem contratar primeiro <span class="ref">Perfil da Primeira Contratação™</span></h3>
<div class="cita">Contrate “pela tarefa que mais consome o seu tempo com menor exigência de julgamento.”<small>Jornada do COMO · Etapa 10 · Passo 08</small></div>
<div class="grid grid3"><div class="card"><b>Julgamento baixo</b><small>Segue roteiro: limpeza e preparação, check-in e check-out. Entra primeiro.</small></div><div class="card"><b>Julgamento médio</b><small>Entra em parte, com modelos prontos: resposta a mensagem. Na ficha, também manutenção e avaliações (elaboração).</small></div><div class="card"><b>Julgamento alto</b><small>Preço, compra, negociação, relação com fornecedor, financeiro: fica com você por mais tempo.</small></div></div>
<h3>Os três formatos</h3>
<ul><li><b>Diarista por estadia:</b> paga por tarefa feita, custo totalmente variável, boa para operação sazonal e pequena. É quase sempre o primeiro formato.</li><li><b>Meio período fixo:</b> cobre limpeza, preparação e parte do atendimento. Faz sentido a partir de quatro a seis unidades.</li><li><b>Integral:</b> só quando a operação sustenta, normalmente já com a segunda unidade no horizonte.</li></ul>
<div class="caixa"><h3>O teste de viabilidade</h3><p>Some o custo da pessoa ao custo fixo do mês e refaça o ponto de equilíbrio da Folha Única (Módulo 2). Se a ocupação de equilíbrio passar de 70%, a ordem muda: primeiro sobe a diária ou corta custo, depois contrata. A ficha faz essa conta sozinha se você já preencheu a Folha no mesmo aparelho.</p></div>
<h3>O que define quem fica</h3>
<p>Confiabilidade acima de talento; disponibilidade compatível com fim de semana e feriado; e capacidade de seguir procedimento escrito, que se testa na seleção: entregue o procedimento impresso e peça para a pessoa executar uma unidade só com o papel. Contrato, encargos e vínculo de trabalho: confirme com o seu contador.</p>
<p class="fonte">Fontes: Bíblia Operacional Zion (seis manuais por setor); Jornada do COMO · Etapa 10 · Passo 08.</p>{ROD}</section>

<section class="pg"><h2>3. Critérios e alçadas</h2>
<div class="cita">“Procedimento permite executar; critério permite resolver.”<small>Jornada do COMO · Etapa 10 · Passo 06 · Tabela de Critérios™</small></div>
<p>Com procedimento e sem critério, a limpeza e o check-in acontecem, e aí um hóspede reclama às nove da noite e o telefone toca na praia. Durante duas semanas, anote toda pergunta que a equipe faz; agrupe as repetidas. Em hospedagem pequena, sete situações cobrem quase tudo:</p>
<ol style="columns:2;column-gap:8mm"><li>Reserva de última hora</li><li>Cortesia e compensação</li><li>Cancelamento e reembolso fora da política</li><li>Manutenção: na hora, agendar ou emergência</li><li>Compra fora do previsto</li><li>Hóspede com comportamento problemático</li><li>Erro de calendário e realocação</li></ol>
<p>Para cada uma: <b>quem decide</b>; a <b>regra</b> (em que situação é sim, em que situação é não, qual exceção ainda precisa de você); e a <b>alçada em reais</b>, quando envolve dinheiro.</p>
<div class="grid"><div class="card"><b>A alçada sobe com a confiança</b><small>Comece baixo: a fonte sugere cem reais na primeira semana e trezentos no segundo mês. Baixa demais mantém você preso; alta demais cria risco. O ajuste é gradual e combinado.</small></div><div class="card"><b>Registro é treino, não controle</b><small>As decisões tomadas dentro da alçada ficam anotadas para revisar juntos. Imprima a tabela e entregue a quem opera: critério que não está escrito e à vista continua sendo pergunta.</small></div></div>
<div class="ex"><b class="rot">Exemplo didático · dados fictícios · Cabanas do Vale</b>
{tabela(["Situação", "Quem decide", "A regra", "Alçada"], [[f"<b>{a}</b>", b, c, f'<span style="white-space:nowrap">{d}</span>'] for a, b, c, d in CRIT], ["25%", "19%", "44%", "12%"])}
<p style="margin:0;font-size:9.4pt">Seis de sete regras escritas. Alçada inicial <b>R$ 100</b>, no segundo mês <b>R$ 300</b>. A cortesia de R$ 42 é 15% da diária média de R$ 280 do Marco Zero e da Folha Única.</p></div>
<p class="fonte">O mapa de quem faz o quê, com a alçada de cada pessoa, é o documento 14 do Manual Mínimo Zion™ (Etapa 10 · Passo 07), revisado a cada contratação. Panorama · G7: «As alçadas por pessoa, em valor.»</p>{ROD}</section>

<section class="pg"><h2>4. Exemplo aplicado</h2>
<div class="ex"><b class="rot">Exemplo didático · dados fictícios</b>
<p style="font-size:9.7pt"><b>Cabanas do Vale</b>, quatro unidades (as mesmas do Marco Zero e da Folha Única). A dona opera; trabalham com ela uma diarista, paga por estadia, e um auxiliar de manutenção. Nenhum dia de férias em 24 meses; nunca ficou sete dias sem atender. Dependências: decisão e acesso fortes, conhecimento e relação médias. Inventário: 52 linhas, das quais 41 (78,8%) são diárias e simples, decisões sem critério ou acessos.</p>
{tabela(["Atividade", "Setor", "Julgamento", "Quem faz hoje", "Horas da dona"], [[f"<b>{a}</b>", b, c, d, f'<span style="float:right">{e} h</span>'] for a, b, c, d, e in ATIV] + [["<b>Total</b>", "", "baixo 5 · médio 9 · alto 6", "", '<span style="float:right"><b>20 h</b></span>']], ["30%", "23%", "18%", "18%", "11%"])}
<ul style="font-size:9.6pt;margin-bottom:0"><li>As <b>20 horas</b> batem com as 20 horas por semana da Conta da Retirada da Folha Única.</li><li><b>Primeira a delegar:</b> check-in e check-out (5 h, segue roteiro), para a diarista que já faz a limpeza. Depois: resposta a mensagem, com modelos.</li><li><b>4 dos 6 setores</b> dependem só da dona: hospitalidade, gerencial, comercial e cultura.</li><li><b>5 horas por semana</b> saem da dona com o plano: 25% das horas dela.</li><li><b>Teste de viabilidade:</b> com R$ 500 a mais por mês, a ocupação de equilíbrio da Folha vai de 28,5% para 30,7% ((7.234 + 500 − 560) ÷ 188,68 = 38,0 noites de 124). Abaixo de 70%: a conta cabe.</li><li><b>Painel:</b> nota mínima 4,7; gasto 10% acima do previsto; leitura toda segunda-feira; nível de presença hoje: 1, operando.</li></ul></div>
<p>O exemplo mostra como o mapa se monta e se lê. Quanto tempo cada hospedagem libera depende da execução de cada uma.</p>{ROD}</section>

<section class="pg"><h2>5. As quatro semanas</h2>
<p>A ordem que funciona é <b>escrever antes de contratar</b>. Antes da semana 1: acessos resolvidos; o procedimento da atividade escrito em uma página, nos seis blocos (quando usar; o que ter em mãos; passos numerados com verbo no imperativo; padrão de qualidade com foto; o que fazer quando foge do roteiro; quem chamar e quando) e testado por alguém que não sabe; a tabela de critérios entregue; a cobertura de falta definida.</p>
<h3>O treino <span class="ref">Plano de Quatro Semanas™</span></h3>
{tabela(["Semana", "O que acontece", "Conversa", "Sinal para avançar", "Exemplo"], [[f"<b>{a}</b>", b, c, d, f'<span style="white-space:nowrap">{e}</span>'] for a, b, c, d, e in SEM], ["19%", "37%", "14%", "17%", "13%"])}
<p>Na avaliação do primeiro mês (no exemplo, <b>13/12/2026</b>), três perguntas: o padrão está sendo mantido? As decisões dentro da alçada foram razoáveis? As dúvidas diminuíram? Três sim: a pessoa está operando. Algum não: repita a semana 3, em vez de concluir que a contratação falhou. São cerca de sete horas no mês.</p>
<div class="cita">“Corrija depois, não durante.”<small>Jornada do COMO · Etapa 10 · Passo 09</small></div>
<h3>A integração em seis etapas</h3>
<p>Na Bíblia Operacional Zion, quem chega passa por seis etapas: 1) visita guiada pelas unidades (10 min); 2) a cultura e o padrão da casa (20 min); 3) o vídeo ou a demonstração da função (30 a 60 min); 4) a leitura do procedimento da função (40 min); 5) a primeira execução acompanhada; 6) a confirmação do padrão (5 min).</p>
<h3>Quando alguém erra <span class="ref">Escala de Resposta</span></h3>
{tabela(["Tipo de erro", "Primeira vez", "Correção de fundo"], [[f"<b>{a}</b>", b, c] for a, b, c in ERRO], ["24%", "42%", "34%"])}
<p class="fonte">A reação ao primeiro erro decide se os próximos serão trazidos ou escondidos. Etapa 10 · Passos 05, 09 e 11.</p>{ROD}</section>

<section class="pg"><h2>6. Acompanhar de fora</h2>
<p>Delegar a execução e continuar conferindo tudo não delega nada: só muda quem faz, mantendo quem olha. O acompanhamento sustentável é <b>por exceção</b>.</p>
<div class="grid"><div class="card"><b>Seis indicadores por semana</b><small>Nota das avaliações; ocupação contra a projeção; tempo médio de resposta; ocorrências; decisões tomadas dentro da alçada; gasto contra o previsto.</small></div><div class="card"><b>Dois ritmos</b><small>Semanal: os seis indicadores por escrito, 15 minutos de leitura. Mensal: 40 minutos de conversa, com a Folha Única ao lado. Nada diário, exceto emergência definida.</small></div><div class="card"><b>Quatro exceções</b><small>Avaliação abaixo da nota mínima; decisão fora da alçada que precisou ser tomada; ocorrência de segurança ou dano; gasto acima do previsto no percentual definido. Só elas geram contato na hora.</small></div><div class="card"><b>Auditoria por amostragem</b><small>Uma unidade sorteada por semana dá o mesmo controle que conferir tudo, sem prender você e sem tirar a autonomia de quem fica.</small></div></div>
<h3>Os quatro níveis de presença <span class="ref">Painel de Acompanhamento™ · Etapa 10 · Passo 10</span></h3>
{tabela(["Nível", "O que você faz", "O que significa"], [["<b>1 · Operando</b>", "Você faz", "O ponto de partida; onde está a maior parte das hospedagens pequenas."], ["<b>2 · Supervisionando tudo</b>", "Confere cada item", "Parece delegação e não é: a execução saiu, a aprovação ficou."], ["<b>3 · Acompanhando por exceção</b>", "Olha indicadores", "Relatório semanal, conversa mensal, contato só nas exceções. É o nível que permite sair."], ["<b>4 · Dirigindo</b>", "Decide o rumo", "Resultado, preço, expansão e marca: você trabalha sobre o negócio."]], ["30%", "22%", "48%"])}
<h3>Faça agora</h3>
<p>Abra a ficha <b>O meu Mapa de Pessoas e Alçadas</b> (link na aula). Cinco telas, de 20 a 30 minutos: o que só você sabe, quem faz o quê, até quanto cada um decide, como acompanhar de fora e as quatro semanas. A planilha <b>Tarefas, Escala e Alçadas</b> (em branco e exemplo) traz ainda a escala da semana e o painel semana a semana.</p>
<div class="caixa"><h3>Critério de conclusão do Módulo 5</h3><ul style="columns:2;column-gap:6mm;margin:0"><li>Dependência de acesso fraca ou com data para resolver.</li><li>As oito atividades com responsável.</li><li>Pelo menos cinco das sete situações com regra escrita.</li><li>Alçada inicial em reais.</li><li>Nota mínima, percentual do gasto e dia da leitura semanal.</li><li>Atividade, pessoa e cobertura de falta definidas.</li><li>Data de início da semana 1 marcada.</li><li>PDF do mapa e do plano baixado e guardado.</li></ul></div>
{ROD}</section>

<section class="pg"><h2>7. A próxima etapa</h2>
<p>Com o mapa e a tabela de critérios na mão, a jornada segue para o <b>Módulo 6 · Compras, estoque e manutenção</b>: a reposição e a manutenção preventiva viram procedimento e critério, com a alçada que você acabou de definir para compra fora do previsto e manutenção. A saída completa da operação (o teste das duas semanas e o plano de saída com datas) fecha o <b>Módulo 7</b>.</p>
<div class="grid grid3"><div class="card"><b>Esta semana</b><small>Resolver os acessos: cofre de senhas, acessos nominais, telefone da operação.</small></div><div class="card"><b>Nas próximas duas semanas</b><small>Anotar as perguntas da equipe e completar a tabela de critérios.</small></div><div class="card"><b>Antes da semana 1</b><small>Escrever e testar o procedimento da primeira atividade.</small></div></div>
<div class="cita">“Enquanto a operação estiver na sua cabeça, você não tem um negócio: você tem um emprego que não pode tirar férias.”<small>Jornada do COMO · Etapa 10 · Carta de abertura</small></div>
<h3>Prompt de IA · revisar o mapa</h3>
<p>Depois de exportar o mapa, cole o prompt publicado em <b>{URL_PROMPT.replace('https://', '')}</b> em qualquer assistente de IA e, em seguida, o seu mapa. Em resumo, o prompt pede ao assistente que, sem inventar números nem regras trabalhistas, sem prometer resultado e sem dar nota:</p>
<ul><li><b>A)</b> confira a coerência do mapa e se a primeira atividade segue a regra (mais horas, menos julgamento);</li><li><b>B)</b> diga, situação por situação, se a regra está completa e se as alçadas fazem sentido para a largada;</li><li><b>C)</b> confira o plano de quatro semanas e o que falta antes da semana 1;</li><li><b>D)</b> formule três perguntas para a avaliação do primeiro mês.</li></ul>
<p class="fonte">Não cole nome completo, documento ou telefone de ninguém da equipe, nem senhas.</p>
<h3>Fontes</h3>
<p class="fonte">Jornada do COMO · Etapa 10 “Como eu saio da operação?” (Passos 01 a 11: Inventário da Cabeça™, Mapa das Quatro Dependências™, Modelo de Procedimento Zion™, Tabela de Critérios™, Manual Mínimo Zion™, Perfil da Primeira Contratação™, Plano de Quatro Semanas™, Painel de Acompanhamento™, Escala de Resposta). Panorama do Desenvolvimento Hoteleiro · Trilha B · Pilar G7 “Governança e Indicadores”. Bíblia Operacional Zion (seis manuais por setor, onboarding em seis etapas, rotina do gestor com a escala da semana). Elaborações declaradas nesta lição: julgamento médio para manutenção e avaliações; contagem de sete itens prontos (não é nota); grade da escala semanal.</p>
<p class="fonte">Material educacional da Zion Hotel Academy · Método Zion 360°. Não é promessa de renda, retorno, ocupação ou resultado: a gestão depende da execução de cada hospedagem.</p>{ROD}</section>
</body></html>"""
(B / "resumo.html").write_text(html, encoding="utf-8")
print("ok", B / "resumo.html"); print("ok", MAT / "Modulo-5-Prompt-de-IA.txt")

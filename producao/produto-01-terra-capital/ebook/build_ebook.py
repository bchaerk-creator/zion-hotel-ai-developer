"""Monta o e-book (60 páginas A4) em HTML. PDF: node ebook/render_ebook.js. Uso: python3 -I producao/produto-01-terra-capital/ebook/build_ebook.py"""
import html, json, pathlib, sys, base64
A = pathlib.Path(__file__).resolve().parent; P = A.parent; R = P.parents[1]
sys.path.insert(0, str(A)); import conteudo
E = lambda s: html.escape(str(s), quote=True)
URI = lambda p: (R / p).as_uri()
TOP = json.load(open(A / "topicos.json"))          # 60 slides do ZIP (fonte)
AUL = json.load(open(P / "src/aulas.json"))
PIL = AUL["pilares"]
def pilar_de(i):  # índice do slide -> pilar
    lim = [(3,5),(6,12),(13,16),(17,20),(21,27),(28,44),(45,52)]
    for k,(a,b) in enumerate(lim,1):
        if a <= i <= b: return k
    return 7
NOMES = {p["n"]: p["nome"] for p in PIL}
img = lambda n: "data:image/jpeg;base64," + base64.b64encode((P/"landing/img"/f"{n}.jpg").read_bytes()).decode()
LOGO = "data:image/png;base64," + base64.b64encode((R/"docs/brand/zion-logo-claro.png").read_bytes()).decode()
LOGO_E = "data:image/png;base64," + base64.b64encode((R/"docs/brand/zion-logo-escuro.png").read_bytes()).decode()

CSS = f"""
@font-face{{font-family:Cormorant;src:url({URI('docs/assets/fonts/cormorant.woff2')}) format("woff2");font-weight:300 700}}
@font-face{{font-family:Cormorant;font-style:italic;src:url({URI('docs/assets/fonts/cormorant-italic.woff2')}) format("woff2")}}
@font-face{{font-family:Aventa;src:url({URI('docs/assets/fonts/aventa.woff2')}) format("woff2")}}
@page{{size:210mm 297mm;margin:0}}
:root{{--preto:#040605;--musgo:#1B2117;--creme:#FEF5F0;--areia:#DED6BF;--terra:#8B714E;--ouro:#C9B37E;--tinta:#1d211b}}
*{{box-sizing:border-box}}html,body{{margin:0;padding:0;background:#777}}
body{{font-family:Aventa,Jost,sans-serif;color:var(--tinta);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:210mm;height:297mm;position:relative;overflow:hidden;background:var(--creme);page-break-after:always;break-after:page;margin:0 auto}}
h1,h2,h3{{font-family:Cormorant,Georgia,serif;font-weight:400;margin:0;line-height:1.05}}
.run{{position:absolute;top:11mm;left:18mm;right:18mm;display:flex;justify-content:space-between;font-size:7.5pt;letter-spacing:.18em;text-transform:uppercase;color:var(--terra);border-bottom:.3mm solid var(--areia);padding-bottom:2.5mm}}
.folio{{position:absolute;bottom:9mm;left:18mm;right:18mm;display:flex;justify-content:space-between;font-size:7.5pt;letter-spacing:.14em;color:var(--terra);text-transform:uppercase}}
.folio b{{font-family:Cormorant,serif;font-size:13pt;letter-spacing:0;color:var(--tinta);font-weight:400}}
.miolo{{position:absolute;top:22mm;bottom:19mm;left:18mm;right:18mm;overflow:hidden;font-size:var(--fs,11pt);line-height:1.55;display:flex;flex-direction:column}}
.num{{font-family:Cormorant,serif;font-style:italic;font-size:46pt;color:var(--ouro);line-height:1}}
.miolo h2{{font-size:30pt;color:var(--musgo);margin:1mm 0 4mm}}
.kick{{font-size:7.5pt;letter-spacing:.24em;text-transform:uppercase;color:var(--terra)}}
.lead{{font-family:Cormorant,serif;font-size:15.5pt;line-height:1.25;color:var(--musgo);margin:0 0 5mm;border-top:.5mm solid var(--ouro);padding-top:3mm}}
.bl{{margin:0 0 4mm}}.bl h4{{font-size:7.5pt;letter-spacing:.2em;text-transform:uppercase;color:var(--terra);margin:0 0 1.2mm;font-weight:400}}
.bl p{{margin:0}}.bl ul{{margin:0;padding-left:0;list-style:none}}.bl li{{position:relative;padding-left:5mm;margin:0 0 1.6mm}}.bl li:before{{content:"—";position:absolute;left:0;color:var(--ouro)}}
.ex{{background:#fff;border-left:1.2mm solid var(--musgo);padding:3mm 4mm;margin:0 0 4mm}}.ex h4{{margin:0 0 1mm;font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:var(--terra);font-weight:400}}
.erro{{border:.3mm dashed var(--terra);padding:2.6mm 3.5mm;margin:0 0 4mm;font-size:.95em}}.erro b{{color:var(--terra);font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;display:block;margin-bottom:.8mm;font-weight:400}}
.at{{background:rgba(201,179,126,.17);border-left:1.2mm solid var(--ouro);padding:3mm 4mm;margin:0 0 4mm}}.at h4{{margin:0 0 1mm;font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:var(--terra);font-weight:400}}
.nota{{margin-top:auto}}.linha{{border-bottom:.25mm solid rgba(139,113,78,.45);height:7mm}}.livre{{flex:1;min-height:14mm;background:repeating-linear-gradient(to bottom,transparent 0,transparent 6.7mm,rgba(139,113,78,.45) 6.7mm,rgba(139,113,78,.45) 7mm)}}
.rot{{font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:var(--terra);margin:2mm 0 0}}
table{{border-collapse:collapse;width:100%;font-size:.92em;margin:0 0 4mm}}th{{background:var(--musgo);color:var(--creme);font-weight:400;font-size:.9em;letter-spacing:.06em;padding:1.8mm 2.2mm;text-align:left}}td{{border-bottom:.2mm solid var(--areia);padding:1.8mm 2.2mm;vertical-align:top}}
.dg{{background:#fff;border:.2mm solid var(--areia);padding:3mm 4mm;margin:0 0 4mm}}
.cv{{background:var(--musgo);color:var(--creme)}}.cv .l{{position:absolute;top:22mm;left:18mm;width:80mm}}
.cv h1{{font-size:44pt;color:var(--creme);margin:0 0 4mm}}.cv h1 i{{color:var(--ouro)}}
.cv .sub{{font-family:Cormorant,serif;font-style:italic;font-size:15pt;color:var(--areia);line-height:1.2}}
.cv .tag{{position:absolute;left:18mm;bottom:22mm;width:90mm;font-size:8.5pt;letter-spacing:.12em;text-transform:uppercase;color:var(--ouro);line-height:1.6}}
.cv .ph{{position:absolute;width:62mm;border:1.2mm solid #040605;border-radius:7mm;overflow:hidden;box-shadow:0 4mm 10mm rgba(0,0,0,.45)}}.cv .ph img{{width:100%;display:block}}
.fim{{background:var(--musgo);color:var(--areia);padding:4mm 5mm;border-left:1.2mm solid var(--ouro);margin:0 0 4mm}}
.ck{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 6mm;font-size:9.3pt}}.ck div{{display:flex;gap:2mm}}.ck i{{flex:none;width:3.6mm;height:3.6mm;border:.3mm solid var(--terra);margin-top:.7mm}}
"""
def aviso_ex(): return "Exemplos com valores são ilustrativos (dados fictícios)."

pages = []
def pg(n, kicker, body, cls=""):
    pages.append(f'<section class="pg {cls}" data-n="{n}"><div class="run"><span>Zion Hotel Academy · Você tem terra. Falta capital?</span><span>{E(kicker)}</span></div><div class="miolo" data-n="{n}">{body}</div><div class="folio"><span>Método Zion · material educativo</span><b>{n}</b></div></section>')

def topico_page(i):
    t = TOP[i-1]; d = conteudo.D[i]; k = pilar_de(i)
    how = "".join(f"<li>{E(x)}</li>" for x in d[1])
    extra = ""
    if i == 3: extra = diag_patr()
    if i == 27: extra = diag_lacuna()
    if i == 31: extra = diag_cob()
    body = f'<div class="kick">Pilar {k} · {E(NOMES[k])}</div><div style="display:flex;align-items:flex-end;gap:5mm"><div class="num">{i-2:02d}</div><h2 style="flex:1">{E(t["t"])}</h2></div>' \
           f'<div class="lead">{E(t["lead"])}</div><div class="bl"><h4>Por que importa</h4><p>{E(d[0])}</p></div><div class="ex"><h4>Exemplo · dados fictícios</h4>{E(t["ex"])}</div>{extra}' \
           f'<div class="bl"><h4>Como fazer</h4><ul>{how}</ul></div><div class="erro"><b>Erro comum</b>{E(d[2])}</div><div class="at"><h4>Atividade</h4>{E(t["at"])}</div>' \
           f'<div class="rot">Minhas anotações</div><div class="livre"></div>'
    return f"Pilar {k} · {NOMES[k]}", body

def bar(label, v, mx, cor): w = max(2, v/mx*100); return f'<div style="display:flex;align-items:center;gap:3mm;margin:1.4mm 0"><div style="width:42mm;font-size:8.8pt">{label}</div><div style="flex:1;background:#eee"><div style="height:5.5mm;width:{w:.1f}%;background:{cor}"></div></div><div style="width:24mm;text-align:right;font-size:8.8pt">R$ {v:,.0f}</div></div>'.replace(",",".")
def diag_patr(): return '<div class="dg"><div class="kick">Diagrama · dados fictícios</div>'+bar("Valor estimado da terra",300000,300000,"#8B714E")+bar("Caixa disponível",10000,300000,"#1B2117")+'<div style="font-size:8.5pt;margin-top:2mm">A barra do caixa é o que paga fornecedores hoje.</div></div>'
def diag_lacuna(): return '<div class="dg"><div class="kick">Diagrama · dados fictícios</div>'+bar("Investimento",220000,250000,"#8B714E")+bar("+ Reserva de giro",30000,250000,"#C9B37E")+bar("Total necessário",250000,250000,"#1B2117")+bar("Recursos próprios",50000,250000,"#2f6b3a")+bar("Lacuna de capital",200000,250000,"#9a5b13")+'</div>'
def diag_cob(): return '<div class="dg"><div class="kick">Diagrama · dados fictícios</div><div style="display:flex;gap:6mm;font-size:9pt;align-items:center"><div style="font-family:Cormorant,serif;font-size:30pt;color:#8e2b2b">0,8x</div><div>R$ 4 mil de caixa ÷ R$ 5 mil de parcela. Abaixo de 1,0 o caixa do mês não paga a parcela.</div></div></div>'

# 1 capa
pages.append(f'''<section class="pg cv" data-n="1"><img src="{LOGO}" style="position:absolute;top:14mm;left:18mm;height:11mm"><div class="l" style="top:46mm;width:86mm"><div class="kick" style="color:var(--ouro)">Zion Hotel Academy · Produto 01</div><h1 style="margin-top:4mm">Você tem terra.<br><i>Falta capital?</i></h1><div class="sub">Aprenda o passo a passo para transformar seu terreno em um projeto turístico e preparar seu patrimônio para buscar recursos, investidores e parceiros.</div></div>
<div class="ph" style="right:-14mm;top:120mm;transform:rotate(5deg)"><img src="{img('tela-lacuna-resultado')}"></div><div class="ph" style="right:30mm;top:150mm;transform:rotate(-4deg)"><img src="{img('tela-mapa')}"></div>
<div class="tag">Guia de 60 páginas · 7 pilares · 20 microaulas · ferramentas e dossiê<br>Para quem tem terreno e quer estruturar um projeto de hospedagem</div>
<div style="position:absolute;bottom:9mm;left:18mm;right:18mm;font-size:7pt;color:rgba(222,214,191,.6)">Telas da ferramenta com dados fictícios. Material educativo da Zion Hotel Academy.</div></section>''')
# 2 como usar
pg(2, "Como usar este guia", f'''<div class="kick">Antes de começar</div><h2>Como usar este guia</h2><div class="lead">Leia uma etapa, faça a atividade e registre a evidência. Não avance por ansiedade.</div>
<div class="bl"><h4>O objetivo</h4><p>Produzir um plano preliminar para o seu projeto: o que você tem, o que falta, que caminhos existem para completar e quais riscos você assume em cada um. O objetivo não é obter promessa de financiamento.</p></div>
<div class="bl"><h4>Como cada página funciona</h4><ul><li><b>Por que importa:</b> a razão prática do tema.</li><li><b>Exemplo:</b> uma conta ou situação com dados fictícios, só para ilustrar.</li><li><b>Como fazer:</b> três passos para aplicar ao seu caso.</li><li><b>Erro comum:</b> a armadilha mais frequente.</li><li><b>Atividade:</b> uma tarefa curta, com espaço para anotações.</li></ul></div>
<div class="bl"><h4>Junto com as ferramentas</h4><p>O portal do aluno traz 20 microaulas de até dois minutos, simuladores de lacuna de capital, operação e dívida, checklist documental, priorização, mapa mental, mapa de desenvolvimento, plano de ação e o gerador do Dossiê de Desenvolvimento e Captação de Capital, com exportação em PDF. Tempo estimado: 70 a 100 minutos de aprendizado e prática, no seu ritmo.</p></div>
<div class="at"><h4>Atenção</h4>Consulte profissionais habilitados para decisões jurídicas, ambientais e financeiras. A Zion está em plena expansão e abre a oportunidade de estruturar projetos e também a possibilidade de criar investimentos e parcerias; cada projeto é avaliado caso a caso. Não envie documentos pessoais ou dados sensíveis por canais públicos.</div>
<div class="rot">Minhas anotações</div><div class="linha"></div><div class="linha"></div><div class="linha"></div>''')
# 3 sumário
def pagina_do_topico(i):
    order = list(range(3,53))
    return 4 + order.index(i)
rows = ""
for p in PIL:
    k = p["n"]; lim = [(3,5),(6,12),(13,16),(17,20),(21,27),(28,44),(45,52)][k-1]
    rows += f'<tr><td><b>{k}</b></td><td><b>{E(p["nome"])}</b><br><small>{" · ".join(E(TOP[i-1]["t"]) for i in range(lim[0], min(lim[1],lim[0]+3)+1))}{"…" if lim[1]-lim[0]>3 else ""}</small></td><td>aulas {p["de"]}–{p["ate"]}</td><td>p. {pagina_do_topico(lim[0])}–{pagina_do_topico(lim[1])}</td></tr>'
pg(3, "Sumário", f'<div class="kick">Os sete pilares</div><h2>Sumário</h2><div class="lead">Patrimônio, território, mercado, produto, finanças, capital e parcerias, implementação.</div><table><tr><th>#</th><th>Pilar e temas</th><th>Aulas</th><th>Páginas</th></tr>{rows}<tr><td></td><td><b>Fechamento</b><br><small>Mapa da jornada · Checklist final · Plano de reunião · Referências · Sua decisão</small></td><td>—</td><td>p. 53–59</td></tr></table><div class="bl"><h4>Como os pilares se ligam</h4><p>Cada pilar depende das evidências do anterior: diagnóstico → mercado → projeto → números → capital → negociação → execução. Se um pilar travou, o seguinte fica no papel.</p></div>')
for i in range(3, 53):
    k, b = topico_page(i); pg(pagina_do_topico(i), k, b)
# 54 (p.54): mapa/pilares/temas  | numeração: 4+50=54
pg(54, "Fechamento · mapa da jornada", f'''<div class="kick">Fechamento</div><h2>Mapa, pilares e temas</h2><div class="lead">Diagnóstico → mercado → projeto → números → capital → negociação → execução.</div>
<div class="ex"><h4>Exemplo</h4>Cada etapa depende de evidências anteriores. Use os sete pilares como índice do seu dossiê.</div>
<table><tr><th>Pilar</th><th>Pergunta central</th></tr><tr><td>1 Patrimônio</td><td>O que tenho é valor ou é caixa?</td></tr><tr><td>2 Território</td><td>O terreno pode receber hospedagem, de forma segura?</td></tr><tr><td>3 Mercado</td><td>Quem paga, quanto e com que evidência?</td></tr><tr><td>4 Produto</td><td>Qual é o menor projeto que funciona?</td></tr><tr><td>5 Finanças</td><td>Quanto falta e o que acontece no cenário ruim?</td></tr><tr><td>6 Capital e parcerias</td><td>Que caminho completa o capital sem pôr o patrimônio em risco?</td></tr><tr><td>7 Implementação</td><td>O que fazer primeiro e quando parar?</td></tr></table>
<div class="bl"><h4>Dez temas que cruzam os pilares</h4><p>Objetivo, matrícula, licenças, infraestrutura, demanda, produto, orçamento, rentabilidade, capital e negociação.</p></div>
<div class="at"><h4>Atividade</h4>Marque cada pilar como pronto, parcial ou pendente e selecione os três temas mais urgentes. No portal, o mapa mental faz isso por você.</div>
<div class="rot">Pilares prontos / parciais / pendentes</div><div class="linha"></div><div class="linha"></div><div class="rot">Três temas mais urgentes</div><div class="linha"></div><div class="linha"></div>''')
CHK = ["Matrícula atualizada","Ônus e titulares revisados","Consulta de uso do solo","Avaliação ambiental","Infraestrutura orçada","Comparáveis de mercado","Orçamento completo","Cenário adverso","Reserva financeira","Alternativas de capital comparadas","Dossiê montado","Revisão profissional"]
pg(55, "Fechamento · checklist final", '<div class="kick">Fechamento</div><h2>Checklist final</h2><div class="lead">Certidão, consulta de uso, avaliação técnica, comparáveis, orçamento, projeção, reserva, alternativas e revisão profissional.</div><div class="ex"><h4>Exemplo</h4>Pendência não equivale a aprovação.</div><div class="ck">'+"".join(f"<div><i></i>{E(c)}</div>" for c in CHK)+'</div><div class="at" style="margin-top:5mm"><h4>Atividade</h4>Registre evidência e responsável de cada item marcado.</div><table><tr><th>Item</th><th>Evidência (sem números de documento)</th><th>Responsável</th></tr>'+"".join('<tr><td>&nbsp;</td><td></td><td></td></tr>' for _ in range(6))+'</table>')
pg(56, "Fechamento · plano de reunião", '<div class="kick">Fechamento</div><h2>Plano de reunião</h2><div class="lead">Apresente o projeto, a lacuna de capital, os riscos, o pedido e os próximos passos.</div><div class="ex"><h4>Exemplo</h4>Não ofereça retorno garantido.</div><div class="bl"><h4>Roteiro de uma conversa de 30 minutos</h4><ul><li><b>5 min · Projeto:</b> quem é o hóspede, qual é a experiência, onde fica.</li><li><b>5 min · Evidências:</b> documentos, consultas e comparáveis, com datas.</li><li><b>7 min · Números:</b> CAPEX, premissas, cenário base e adverso.</li><li><b>5 min · Lacuna e pedido:</b> quanto falta, para quê, em quais etapas.</li><li><b>5 min · Riscos:</b> o que pode dar errado e como você trata.</li><li><b>3 min · Próximos passos:</b> o que cada lado faz e até quando.</li></ul></div><div class="at"><h4>Atividade</h4>Agende conversa apenas quando a proposta estiver clara.</div><div class="rot">Perguntas que quero fazer</div><div class="linha"></div><div class="linha"></div><div class="linha"></div><div class="rot">Perguntas que provavelmente vou ouvir</div><div class="linha"></div><div class="linha"></div><div class="linha"></div>')
pg(57, "Fechamento · referências", '<div class="kick">Fechamento</div><h2>Referências para consulta</h2><div class="lead">Consulte condições atuais diretamente nos órgãos e agentes financeiros.</div><table><tr><th>Fonte</th><th>Para quê</th></tr><tr><td>Ministério do Turismo · gov.br/turismo</td><td>Políticas e programas de turismo</td></tr><tr><td>Cadastur · cadastur.turismo.gov.br</td><td>Cadastro de prestadores de serviços turísticos</td></tr><tr><td>Banco Central · bcb.gov.br</td><td>Informações sobre crédito e custo efetivo total</td></tr><tr><td>CVM · gov.br/cvm</td><td>Regras sobre oferta pública de investimento</td></tr><tr><td>Sebrae · sebrae.com.br</td><td>Orientação a pequenos negócios</td></tr></table><div class="ex"><h4>Exemplo</h4>Cadastro e enquadramento em programas não garantem crédito.</div><div class="at"><h4>Atividade</h4>Registre data e fonte de cada informação que usar no seu dossiê.</div><div class="aviso">As regras mudam. Este material não traz condições de crédito nem de programas públicos: confirme sempre na fonte.</div><div class="rot">Informação · fonte · data</div>'+'<div class="linha"></div>'*6)
pg(58, "Fechamento · sua decisão", '<div class="kick">Fechamento</div><h2>Sua decisão</h2><div class="lead">Compare crédito, parceria, arrendamento e implantação gradual.</div><div class="ex"><h4>Exemplo</h4>A melhor alternativa depende da propriedade, do risco e da capacidade de execução.</div><table><tr><th>Caminho</th><th>O que você ganha</th><th>O que você assume</th></tr><tr><td><b>Crédito</b></td><td>Mantém o controle do projeto.</td><td>Parcela fixa a pagar e, se houver garantia, risco sobre o bem.</td></tr><tr><td><b>Parceria / sociedade</b></td><td>Divide o aporte e o risco de capital.</td><td>Divide controle, decisões e resultado; exige contrato claro.</td></tr><tr><td><b>Arrendamento</b></td><td>Renda sem operar a hospedagem.</td><td>Abre mão de controle e do uso durante o contrato.</td></tr><tr><td><b>Implantação gradual</b></td><td>Menos dívida e validação antes de ampliar.</td><td>Começa menor e leva mais tempo para chegar ao projeto completo.</td></tr></table><div class="at"><h4>Atividade</h4>Escolha o próximo passo e justifique.</div><div class="rot">Meu próximo passo e por quê</div>'+'<div class="linha"></div>'*4+'<div class="fim" style="margin-top:4mm">Qualquer um dos caminhos exige revisão de advogado, contador e, quando for o caso, engenheiro.</div>')
pg(59, "Fechamento · da terra ao negócio", '<div class="kick">Fechamento</div><h2>Da terra ao negócio</h2><div class="lead">O patrimônio é um ponto de partida. O projeto precisa demonstrar demanda, viabilidade e capacidade de execução.</div><div class="ex"><h4>Exemplo</h4>Use as ferramentas junto com o conteúdo.</div><div class="bl"><h4>O que você tem agora</h4><ul><li>Uma lacuna de capital calculada, sem contar valorização futura.</li><li>Um cenário adverso e um limite de desistência.</li><li>Um checklist com evidências e pendências visíveis.</li><li>Um plano de 30 dias com três ações, responsáveis e datas.</li><li>Um dossiê preliminar que você pode levar a profissionais e a possíveis parceiros.</li></ul></div><div class="at"><h4>Atividade</h4>Revise seu plano mensalmente.</div><div class="fim">Este guia entrega o método. A Zion está em plena expansão e abre a oportunidade de estruturar projetos e também a possibilidade de criar investimentos e parcerias. Cada projeto é avaliado caso a caso.</div><div class="rot">O que mudou no meu projeto depois deste guia</div>'+'<div class="linha"></div>'*5)
pg(60, "Notas e acesso às ferramentas", f'<div class="kick">Continue</div><h2>Notas e acesso às ferramentas</h2><div class="lead">As ferramentas estão na área de membros, junto com as microaulas.</div><div style="display:flex;gap:6mm;align-items:flex-start"><div style="flex:1"><div class="bl"><h4>Na área de membros</h4><ul><li>20 microaulas de até 2 minutos, com tarefa em cada uma</li><li>Simuladores de lacuna, operação e dívida</li><li>Checklist, priorização e plano de 30 dias</li><li>Mapa mental e mapa de desenvolvimento</li><li>Gerador de Dossiê em PDF</li></ul></div><div class="bl"><h4>Privacidade</h4><p>Suas respostas ficam salvas no seu aparelho. O PDF é gerado no seu navegador. Faça o backup do progresso no portal antes de trocar de aparelho.</p></div></div><div style="width:58mm;border:1mm solid #040605;border-radius:6mm;overflow:hidden"><img src="{img("tela-dossie")}" style="width:100%;display:block"></div></div><div class="rot">Notas</div>'+'<div class="linha"></div>'*9+'<div style="position:absolute;bottom:2mm;left:0;right:0;font-size:7.5pt;color:var(--terra)">Zion Hotel Group International · Material educativo. Telas com dados fictícios.</div>')
assert len(pages) == 60, len(pages)
head = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Você tem terra. Falta capital? · Zion Hotel Academy</title><style>{CSS}</style></head><body>'
(P/"dist").mkdir(exist_ok=True)
(P/"dist/ebook.html").write_text(head + "\n".join(pages) + "</body></html>")
print("páginas:", len(pages))

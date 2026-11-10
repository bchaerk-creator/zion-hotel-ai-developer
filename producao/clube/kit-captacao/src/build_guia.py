"""Gera o HTML do guia "Kit Inicial · Como captar recursos para o seu projeto" (Club Zion Collection).
Depois, src/render_pdf.js imprime em PDF A4 e confere se alguma página transborda.
Uso: python3 -I src/build_guia.py <pasta-build>   ->  <pasta-build>/guia.html
Molde: producao/jornada2/*/src/build_resumo.py (mesmo CSS base), com fontes e fotos embutidas em data URL.
Fontes do conteúdo (só o que está escrito nelas): docs/escola/z02 (Cap. 4 e 5), f00 (Caps. 1 e 5), f05 (Cap. 1),
f06 (Caps. 1 e 4), ferramentas B04, B02 e B10 do Zion Arsenal. Exemplos: fictícios, marcados como tal."""
import sys, pathlib, base64
B = pathlib.Path(sys.argv[1]); B.mkdir(parents=True, exist_ok=True)
REPO = pathlib.Path(__file__).resolve().parents[4]; D = REPO / "docs"
def data(p, mime): return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()
F = {k: data(D / "assets/fonts" / f"{k}.woff2", "font/woff2") for k in ("cormorant", "cormorant-italic", "aventa")}
LOGO_C = data(D / "brand/zion-logo-claro.png", "image/png"); LOGO_E = data(D / "brand/zion-logo-escuro.png", "image/png")
FOTO = {k: data(D / "assets" / v, "image/webp") for k, v in {"capa": "operacoes/op09.webp", "zion": "operacoes/op08.webp", "fim": "operacoes/op12.webp"}.items()}
LINK = "https://wa.me/554861371061?text=Oi%21%20Preenchi%20o%20meu%20Mapa%20das%20Fontes%20do%20Kit%20de%20Capta%C3%A7%C3%A3o%20e%20quero%20agendar%20a%20minha%20sess%C3%A3o%20estrat%C3%A9gica."  # WhatsApp da Zion com mensagem pronta

CSS = f"""
@font-face{{font-family:Cormorant;src:url({F['cormorant']})}} @font-face{{font-family:Cormorant;font-style:italic;src:url({F['cormorant-italic']})}} @font-face{{font-family:Aventa;src:url({F['aventa']})}}
:root{{--preto:#040605;--musgo:#1B2117;--creme:#FEF5F0;--areia:#DED6BF;--terra:#8B714E;--ouro:#C9B37E;--texto:#1B2117;--cinza:#5A5F55}}
@page{{size:A4;margin:0}} *{{box-sizing:border-box}}
body{{margin:0;font-family:Aventa,Arial,sans-serif;color:var(--texto);background:#fff;font-size:10.6pt;line-height:1.42}}
.pg{{width:210mm;height:297mm;padding:19mm 19mm 22mm;page-break-after:always;position:relative;overflow:hidden}}
.pg:last-child{{page-break-after:auto}}
.in{{height:100%}}
.capa{{background:var(--musgo);color:var(--creme);padding:0}}
.capa .foto{{position:absolute;inset:0;background-size:cover;background-position:center}}
.capa .veu{{position:absolute;inset:0;background:linear-gradient(0deg,rgba(22,38,28,.98) 0%,rgba(22,38,28,.9) 46%,rgba(22,38,28,.35) 78%,rgba(22,38,28,.2) 100%)}}
.capa .w{{position:absolute;inset:0;padding:20mm 19mm;display:flex;flex-direction:column;justify-content:space-between}}
.capa img.logo{{height:15mm;align-self:flex-start}} .k{{color:var(--ouro);letter-spacing:.2em;text-transform:uppercase;font-weight:700;font-size:9.5pt}}
.capa h1{{font-family:Cormorant,serif;font-weight:500;font-size:52pt;line-height:1;margin:5mm 0 5mm}} .capa h1 i{{color:var(--ouro)}}
.capa .bar{{width:30mm;height:1.2mm;background:var(--ouro);margin:0 0 6mm}}
.capa p{{color:var(--areia);font-size:13pt;max-width:150mm;margin:0 0 3mm}}
.escuro{{background:var(--musgo);color:var(--creme)}} .escuro h2{{color:var(--creme)}} .escuro p{{color:var(--areia)}}
h2{{font-family:Cormorant,serif;font-weight:500;font-size:27pt;line-height:1.08;margin:0 0 4mm;color:var(--musgo)}} h2 i{{color:var(--terra)}}
.escuro h2 i{{color:var(--ouro)}}
.sec{{font-size:9pt;letter-spacing:.2em;text-transform:uppercase;color:var(--terra);font-weight:700;margin-bottom:2.5mm}}
.escuro .sec{{color:var(--ouro)}}
h3{{font-size:9.6pt;letter-spacing:.14em;text-transform:uppercase;color:var(--terra);margin:4.5mm 0 1.8mm}}
p{{margin:0 0 2.6mm}} ul,ol{{margin:0 0 2.6mm;padding-left:5mm}} li{{margin-bottom:1.1mm}}
.lead{{font-size:12.2pt;line-height:1.4;color:#2D352A}}
.cita{{font-family:Cormorant,serif;font-style:italic;font-size:16pt;line-height:1.22;border-left:3px solid var(--ouro);padding-left:6mm;margin:3.5mm 0;color:var(--musgo)}}
.escuro .cita{{color:var(--creme)}}
.cita small{{display:block;font-family:Aventa,sans-serif;font-style:normal;font-size:8.3pt;color:var(--cinza);margin-top:1.5mm;letter-spacing:.1em;text-transform:uppercase}}
.escuro .cita small{{color:var(--areia)}}
table{{width:100%;border-collapse:collapse;font-size:9.1pt;margin:2.2mm 0 3mm;line-height:1.3}} th,td{{text-align:left;padding:1.5mm 2mm;border-bottom:1px solid var(--areia);vertical-align:top}} th{{background:var(--musgo);color:var(--creme);font-weight:600}}
td.n,th.n{{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}} tr.tot td{{background:#F6F1E6;font-weight:700}}
.ex{{background:#F6F1E6;border:1px solid var(--areia);border-radius:4mm;padding:3.8mm 5mm;margin:3mm 0}} .ex b.rot{{display:block;font-size:8.6pt;letter-spacing:.14em;text-transform:uppercase;color:#A0522D;margin-bottom:2mm}} .ex table{{background:#fff}}
.caixa{{border:1px dashed var(--terra);border-radius:4mm;padding:3.5mm 5.5mm;margin:3.5mm 0}} .caixa h3{{margin-top:0}}
.ouro{{border:1.5px solid var(--ouro);background:#FBF7EE;border-radius:4mm;padding:3.5mm 5.5mm;margin:3.5mm 0}} .ouro h3{{margin-top:0}}
.rod{{position:absolute;left:19mm;right:19mm;bottom:9mm;font-size:7.8pt;white-space:nowrap;color:var(--cinza);display:flex;justify-content:space-between;gap:8mm;border-top:1px solid var(--areia);padding-top:2mm}}
.escuro .rod{{color:var(--areia);border-color:rgba(222,214,191,.35)}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:3.5mm;margin:2mm 0 3mm}} .grid3{{grid-template-columns:1fr 1fr 1fr}}
.card{{border:1px solid var(--areia);border-radius:3mm;padding:3mm 3.4mm;font-size:9.5pt;background:#fff}} .card b{{display:block;color:var(--musgo);margin-bottom:.8mm}} .card small{{color:var(--cinza);font-size:9pt;line-height:1.34;display:block}}
.fonte6{{border:1px solid var(--areia);border-radius:3.5mm;padding:3.6mm 4.4mm;margin:0 0 3.6mm;background:#fff}}
.fonte6 .t{{display:flex;align-items:baseline;gap:3mm;margin-bottom:1.6mm}} .fonte6 .num{{font-family:Cormorant,serif;font-size:26pt;color:var(--ouro);line-height:.9}}
.fonte6 .t b{{font-family:Cormorant,serif;font-size:17pt;font-weight:500;color:var(--musgo)}}
.fonte6 .g{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;font-size:9.1pt;line-height:1.34}} .fonte6 .g div b{{display:block;font-size:8pt;letter-spacing:.12em;text-transform:uppercase;color:var(--terra);margin-bottom:.6mm}}
.fonte6 .q{{font-size:8.6pt;color:var(--cinza);margin-top:1.8mm;font-style:italic}}
.fonte{{font-size:8.6pt;color:var(--cinza)}}
.passos{{counter-reset:p;list-style:none;padding:0}} .passos li{{counter-increment:p;position:relative;padding-left:11mm;margin-bottom:3mm}} .passos li:before{{content:counter(p);position:absolute;left:0;top:-.5mm;width:7.5mm;height:7.5mm;border-radius:50%;background:var(--musgo);color:var(--creme);display:grid;place-items:center;font-weight:700;font-size:9pt}}
.linha{{border-bottom:1px solid #B9AE93;height:8.2mm}}
.ficha td{{height:13mm;border:1px solid var(--areia)}} .ficha th{{border:1px solid var(--musgo);font-size:8.6pt}}
.ficha td.f{{font-size:8.8pt;font-weight:600;color:var(--musgo);width:36mm;background:#FBF7EE}}
.chk li{{list-style:none;margin-left:-5mm;padding-left:7mm;position:relative}} .chk li:before{{content:"";position:absolute;left:0;top:1mm;width:3.4mm;height:3.4mm;border:1.2px solid var(--terra);border-radius:.8mm}}
.ordem{{display:grid;grid-template-columns:repeat(4,1fr);gap:2.6mm;margin:3mm 0}} .ordem div{{background:var(--musgo);color:var(--creme);border-radius:3mm;padding:3.2mm;font-size:9pt;line-height:1.3}} .ordem b{{display:block;font-family:Cormorant,serif;font-size:19pt;font-weight:500;color:var(--ouro);margin-bottom:1mm}} .ordem small{{color:var(--areia)}}
.btn{{display:inline-block;background:var(--ouro);color:var(--preto);font-weight:700;padding:3.4mm 7mm;border-radius:2mm;text-decoration:none;letter-spacing:.04em;font-size:11pt}}
.fim{{padding:0}} .fim .foto{{position:absolute;inset:0;background-size:cover;background-position:center}} .fim .veu{{position:absolute;inset:0;background:linear-gradient(0deg,rgba(22,38,28,.99) 0%,rgba(22,38,28,.93) 58%,rgba(22,38,28,.35) 100%)}}
.fim .w{{position:absolute;inset:0;padding:19mm 19mm 22mm;display:flex;flex-direction:column;justify-content:flex-end}}
.url{{font-size:8.4pt;color:var(--areia);word-break:break-all}}
.foto-z{{width:100%;height:58mm;background-size:cover;background-position:center;border-radius:3mm;margin:2mm 0 1.5mm}}
.leg{{font-size:8.2pt;color:var(--cinza);margin-bottom:3mm}}
"""

ROD = lambda n: f'<div class="rod"><span>Club Zion Collection · Kit Inicial de Captação</span><span>Material educativo, sem promessa de crédito, investidor ou retorno · <b>{n}</b></span></div>'

def fonte(num, nome, pede, leva, risco, q):
    return f'''<div class="fonte6"><div class="t"><span class="num">{num}</span><b>{nome}</b></div><div class="g"><div><b>O que pede</b>{pede}</div><div><b>O que leva</b>{leva}</div><div><b>Risco principal</b>{risco}</div></div><div class="q">{q}</div></div>'''

P = []
# 1 · capa
P.append(f'''<section class="pg capa"><div class="foto" style="background-image:url({FOTO['capa']})"></div><div class="veu"></div><div class="w"><img class="logo" src="{LOGO_C}" alt="Zion Hotel Group International">
<div><div class="k">Club Zion Collection · Kit Inicial</div><h1>Você tem a terra.<br><i>Falta a ordem.</i></h1><div class="bar"></div>
<p><b style="color:var(--creme)">Como captar recursos para o seu projeto.</b> Aprenda o passo a passo para entender as fontes de capital, saber o que cada uma pede e montar o seu primeiro pedido.</p>
<p style="font-size:10.5pt">Guia · Planilha Mapa das Fontes (em branco e exemplo) · Vídeo tutorial · 1 sessão estratégica de 45 minutos com a equipe Zion</p></div>
<div class="k" style="font-size:8.5pt">Zion Hotel Group International · Método Zion 360° · Foto: operação Zion Bubble Glamping</div></div></section>''')

# 2 · como usar
P.append(f'''<section class="pg"><div class="sec">Antes de começar</div><h2>Como usar <i>este kit</i></h2>
<p class="lead">Este kit é para quem tem uma terra ou uma área, quer tirar do papel um projeto de hospedagem e não tem o capital para fazer tudo sozinho.</p>
<p>Ele não promete dinheiro. Ele faz uma coisa mais útil antes do dinheiro: mostra de onde o capital pode vir, o que cada fonte pede em troca e em que ordem as coisas precisam estar prontas para alguém aceitar conversar com você.</p>
<h3>O que vem no kit</h3>
<div class="grid"><div class="card"><b>1 · Este guia</b><small>16 páginas. Leia em cerca de 40 minutos. As páginas 13 e 14 são para preencher.</small></div>
<div class="card"><b>2 · Planilha Mapa das Fontes</b><small>Versão em branco e versão com exemplo fictício. Faz a conta do quanto falta e compara as seis fontes.</small></div>
<div class="card"><b>3 · Vídeo tutorial</b><small>Cerca de 9 minutos. Explica o caminho e mostra a planilha preenchida.</small></div>
<div class="card"><b>4 · Sessão estratégica</b><small>45 minutos com a equipe Zion, incluída no Club Zion Collection. Você preenche o seu Mapa e envia no WhatsApp; depois agenda a sessão, em que a equipe indica o próximo passo.</small></div></div>
<h3>O caminho em quatro passos</h3>
<ol class="passos"><li><b>Entenda por que a terra fica parada</b> (página 3). Quase nunca é só dinheiro.</li>
<li><b>Conheça as seis fontes de capital</b> (páginas 5 a 9): o que cada uma pede, o que leva e o risco.</li>
<li><b>Coloque as coisas na ordem certa</b> (páginas 10 e 11): território, mercado, produto e conta, antes de pedir.</li>
<li><b>Monte o seu primeiro pedido e o seu Mapa das Fontes</b> (páginas 12 a 14) e agende a sua sessão (página 16).</li></ol>
<div class="caixa"><h3>Três combinados</h3><ul><li><b>Exemplos são fictícios.</b> Toda conta com nome de pessoa ou de sítio é ilustrativa e foi conferida. Não é referência de preço, taxa ou valor para o seu caso.</li>
<li><b>Nada aqui é promessa</b> de crédito, investidor, sociedade, renda ou retorno. Emprestar ou investir é decisão de quem empresta ou investe.</li>
<li><b>Contratos, garantias e sociedade</b> se decidem com advogado e contador. Este guia é introdutório.</li></ul></div>{ROD(2)}</section>''')

# 3 · por que a terra fica parada
P.append(f'''<section class="pg"><div class="sec">Capítulo 1</div><h2>Por que a terra <i>fica parada</i></h2>
<p class="lead">A frase mais comum de quem tem terra é: "quando sobrar dinheiro, eu começo". O Método Zion lê essa frase de outro jeito.</p>
<div class="cita">"Terreno parado quase nunca é falta de dinheiro. É falta de ordem."<small>Panorama do Desenvolvimento Hoteleiro, citado no módulo Z02</small></div>
<div class="cita">"A maioria dos projetos de hospedagem não trava por falta de dinheiro. Trava porque decisões que vinham depois foram tomadas antes, e decisões que vinham antes nunca foram tomadas."<small>A Ordem das Coisas, citado no Z02</small></div>
<p>Quem procura crédito sem projeto está tratando um sintoma. A Ordem das Coisas descreve assim: o que aparece é "falta capital para começar"; o que a pessoa tenta é "procurar crédito"; e o problema real está numa decisão anterior, porque ainda não se sabe qual porta de entrada cabe.</p>
<h3>O teste das três perguntas do capital</h3>
<p>Responda só com sim ou não:</p>
<ol><li>Se o dinheiro aparecesse amanhã, eu sei exatamente o que construir, com quantas unidades e para quem?</li>
<li>Eu sei qual diária o meu destino sustenta, mês a mês, com base em dado coletado e não em estimativa?</li>
<li>Eu sei em quanto tempo o investimento retorna, em cenário conservador, base e otimista?</li></ol>
<div class="ouro"><h3>Como ler</h3><p>"Três sim: falta capital, e o caminho é captação estruturada." Se houver um não: "não falta capital. Falta a decisão anterior a ele." <span class="fonte">(A Ordem das Coisas, Cap. 4, citado no F06)</span></p>
<p style="margin:0">Isso é uma boa notícia para quem não tem reserva. A decisão anterior custa principalmente tempo e atenção, não dinheiro.</p></div>
<div class="cita">"Capital não é escasso. O que é escasso é projeto que um investidor consiga auditar em uma tarde."<small>Volume 05 · Investimento, edição de captação, citado no F06</small></div>{ROD(3)}</section>''')

# 4 · seu número
P.append(f'''<section class="pg"><div class="sec">Capítulo 1 · continuação</div><h2>Antes do primeiro real: <i>o seu número</i></h2>
<p class="lead">Antes de olhar para banco ou sócio, o método pede dois números seus. Mesmo que sejam pequenos. Mesmo que sejam zero.</p>
<h3>1 · O capital que é seu de verdade</h3>
<div class="ouro"><p style="margin:0"><b>Capital Real Disponível™</b> = saldo em 30 dias − reserva − dívidas caras − compromissos − giro. <span class="fonte">(Z02, Cap. 1)</span></p></div>
<p>"O dinheiro que você pode investir é menor que o dinheiro que você tem, e a diferença não é pequena." E vale só o que é <b>contratado, não esperado</b>: promessa de parente não conta. "Promessa de aporte de familiar é a mais perigosa das três, porque ela não tem contrato e tem relação." <span class="fonte">(Volume 05, citado no Z02)</span></p>
<h3>2 · Quanto você pode perder</h3>
<p>"A pergunta certa não é quanto você tem, é quanto você pode perder sem comprometer a sua vida." Esse é o seu <b>limite de perda aceitável</b>. "Esse número, e não o saldo, é o seu capital de risco." <span class="fonte">(Volume 05, citado no Z02)</span></p>
<div class="caixa"><h3>Se o seu número é perto de zero</h3><p>Ele não encerra o projeto. Ele muda a pergunta. Em vez de "quanto eu ponho?", passa a ser "o que eu ofereço?". E quem tem terra tem um ativo para oferecer.</p>
<p style="margin:0">A terra pode entrar como <b>participação</b> numa sociedade, como <b>direito de uso</b> num arrendamento, como <b>moeda de troca</b> numa permuta ou como <b>garantia</b> em algumas operações de crédito. Para tudo isso, a documentação pesa muito. <span class="fonte">(B04 · Tenho terra, mas não tenho dinheiro)</span></p></div>
<h3>A ordem que protege você</h3>
<p>Primeiro o capital próprio contratado e o limite de perda. Depois a conta do quanto falta. Só então as fontes de terceiros. "Por isso a sequência correta não é captar para estruturar. É estruturar para captar." <span class="fonte">(A Ordem das Coisas, citado no Z02)</span></p>
<p class="fonte">A planilha Mapa das Fontes começa exatamente por aqui: a aba Necessidade pede o capital próprio contratado, que pode ser zero.</p>{ROD(4)}</section>''')

# 5 · as seis fontes (visão geral)
P.append(f'''<section class="pg"><div class="sec">Capítulo 2</div><h2>As seis fontes <i>de capital</i></h2>
<p class="lead">Quando se fala em dinheiro para hospedagem, a cabeça vai direto para banco ou sócio. Existem mais caminhos, e cada um cobra um preço diferente.</p>
<p>O módulo Z02 usa o <b>Mapa das Seis Fontes™</b> (Volume 05 · Investimento): capital próprio, pessoa do círculo, comprador de unidade, dívida bancária, fomento e investidor. A ferramenta B04 avalia seis caminhos para quem tem terra: recursos próprios, parceria, arrendamento, permuta, financiamento e implantação progressiva. Neste kit, juntamos os dois mapas em seis fontes, pensadas para quem tem a terra e não tem o capital.</p>
<table><tr><th>Fonte</th><th>O que pede de você</th><th>O que leva em troca</th></tr>
<tr><td><b>1 · Capital próprio e etapa menor</b></td><td>Limite de perda escrito e uma etapa 1 que já opera</td><td>Nada em juro; todo o risco fica com você</td></tr>
<tr><td><b>2 · Banco, cooperativa e fomento</b></td><td>Capacidade de pagar e garantia limpa</td><td>Juro, garantia e limites no contrato</td></tr>
<tr><td><b>3 · Sócio que entra com capital</b></td><td>Projeto que se audita numa tarde</td><td>Resultado, decisão, informação e a sua saída</td></tr>
<tr><td><b>4 · Sócio operador ou arrendamento</b></td><td>Papéis claros e contrato longo</td><td>Parte do resultado ou o uso da área por um prazo</td></tr>
<tr><td><b>5 · Permuta e parcerias com construtor</b></td><td>Projeto estruturado e avaliação aceita pelos dois</td><td>Parte da área, das unidades ou da receita</td></tr>
<tr><td><b>6 · Pessoa do círculo e venda antecipada</b></td><td>Contrato escrito; na venda, projeto e licença</td><td>Relação em jogo; obrigação de entregar</td></tr></table>
<div class="cita">"Todo capital tem preço. O barato cobra juros. O caro cobra participação. O errado cobra o projeto inteiro."<small>Volume 05 · Investimento (edição do projeto), citado no Z02</small></div>
<h3>Três regras antes de escolher</h3>
<ul><li><b>Classifique cada fonte</b> em disponível, possível ou fora, com uma linha de justificativa. "Fora também é informação, e evita meses perseguindo o que não existe."</li>
<li><b>Combine.</b> "Na prática, um projeto faseado de pequeno porte raramente é financiado por uma fonte só." Antes de assinar a primeira, confira se as garantias de cada fonte conflitam.</li>
<li><b>Velocidade é tempo até o dinheiro estar na conta</b>, não tempo até a resposta.</li></ul>
<p class="fonte">Fontes: Z02, Cap. 5; B04. As frases entre aspas são do Volume 05 · Investimento, citadas no Z02.</p>{ROD(5)}</section>''')

# 6 · fontes 1 e 2
P.append(f'''<section class="pg"><div class="sec">Capítulo 2 · fontes 1 e 2</div><h2>O seu capital, a etapa menor <i>e o banco</i></h2>
{fonte(1, "Capital próprio e etapa menor", "Saber o seu limite de perda. Desenhar a etapa 1 como o menor conjunto que já opera e gera caixa, com o projeto inteiro pensado desde o início.", "Nada em juro ou participação. Em troca, concentra todo o risco em você.", "Fazer tudo de uma vez: \"O dinheiro acaba no meio, a obra para, e obra parada continua custando aluguel, juros e equipe.\" (Panorama)", "\"Fase um é o menor conjunto que já opera e gera caixa. Nem sempre é a mais bonita; é a que abre mais cedo.\" E: \"O amador espera juntar todo o capital para começar. O developer desenha um projeto onde a primeira fase paga a segunda.\" (Z02, Cap. 4)")}
<p style="font-size:9.6pt">Atenção ao tamanho. A Jornada do COMO lembra que, para hospedagem de lazer com estrutura própria, o mínimo costuma ficar entre três e cinco unidades. "Menos do que você quer e mais do que paga a operação: esse é o ponto." <span class="fonte">(Z02, Cap. 4)</span></p>
{fonte(2, "Banco, cooperativa e fomento", "Fluxo e ativo. \"O banco compra ativo e fluxo. Ele quer garantia real e capacidade de pagamento, e não tem o menor interesse na sua visão de expansão.\" (Volume 05, citado no F05)", "Juro e parcelas periódicas, garantia e limites no contrato. No fomento, contrapartidas e fiscalização.", "A parcela cobra todo mês, inclusive na obra. Aval pessoal: \"com aval pessoal, o pior cenário alcança a sua casa.\" Fomento procurado em cima da hora: desembolso lento.", "\"Em dívida para obra, a taxa quase nunca é o problema. A carência é.\" (Volume 05, citado no F05 e no Z02)")}
<div class="ouro"><h3>As três perguntas para três bancos</h3><ol style="margin:0"><li><b>Taxa para esse perfil.</b> Não a do cartaz: a que o banco aplica a um projeto como o seu.</li><li><b>Prazo de carência possível.</b> Quantos meses sem pagar principal e, idealmente, sem juro.</li><li><b>Garantia exigida.</b> Sobre o ativo do empreendimento, sobre o seu patrimônio pessoal, ou as duas.</li></ol>
<p style="margin:2mm 0 0">"A carência é a resposta que decide." Resposta de telefone não é proposta: só vale proposta escrita. <span class="fonte">(F05, Cap. 1)</span></p></div>
<p class="fonte">Este kit não indica banco, linha de crédito nem taxa. A planilha calcula quanto caberia numa parcela que você aguenta, com a taxa e o prazo de uma simulação que você mesmo fez.</p>{ROD(6)}</section>''')

# 7 · fontes 3 e 4
P.append(f'''<section class="pg"><div class="sec">Capítulo 2 · fontes 3 e 4</div><h2>Sócios: quem entra <i>e o que leva junto</i></h2>
{fonte(3, "Sócio que entra com capital", "Um projeto que ele consiga conferir: território lido, mercado medido, produto definido e conta defensável. O investidor compra tese e execução, e usa fluxo e ativo como piso de segurança.", "Participação. E participação é quatro coisas: resultado, decisão, informação e a sua saída.", "Sócio errado por uma década. \"Nenhuma dessas quatro coisas se desfaz depois sem comprar de volta.\"", "\"Ele entra com dinheiro, você com projeto e execução. A pergunta que decide não é quanto ele põe, é quanto valor você criou antes de vender participação.\" (Panorama, citado no Z02)")}
{fonte(4, "Sócio operador ou arrendamento", "Papéis claros. Quem aporta terra ou capital recebe participação; quem trabalha recebe remuneração de mercado, em contrato separado. No arrendamento, um operador implanta e opera na sua área e paga pelo uso, com contrato longo.", "No sócio operador, parte do resultado. No arrendamento, o uso da área por um prazo: \"Você troca potencial por previsibilidade.\" (Panorama)", "Misturar trabalho com participação. No arrendamento: prazo curto afasta operador, e o destino das construções precisa estar escrito.", "\"Você faz duas coisas no negócio: aportou capital ou ativo, e trabalha. A primeira dá participação; a segunda dá remuneração de mercado pela função.\" (Volume 05, citado no F06)")}
<div class="grid"><div class="card"><b>Quem opera?</b><small>A ferramenta B02 mostra que o ideal é que exatamente uma das partes opere: dois operadores tendem a disputar decisões, e nenhum exige contratar gestão.</small></div>
<div class="card"><b>Trabalho vira participação?</b><small>Nenhuma fonte Zion dá regra para precificar participação por trabalho. Não invente percentual: leve a pergunta ao advogado, com o valor de mercado da função escrito. (F06, Cap. 4)</small></div></div>
<div class="caixa"><h3>Antes do primeiro aporte</h3><p style="margin:0">O F06 lista oito proteções que precisam estar escritas: remuneração de gestão a mercado, lista fechada de veto, informação numa periodicidade possível, regra de distribuição e reinvestimento, regras de saída, aporte adicional, limite de diluição e o que acontece em morte, incapacidade ou saída do sócio gestor. "Parece formalidade. É o que separa sócios de futuros litigantes."</p></div>{ROD(7)}</section>''')

# 8 · fontes 5 e 6
P.append(f'''<section class="pg"><div class="sec">Capítulo 2 · fontes 5 e 6</div><h2>Permuta, círculo <i>e venda antecipada</i></h2>
{fonte(5, "Permuta e parcerias com construtor", "\"Projeto estruturado e avaliação aceita pelos dois lados.\" (Panorama) A terra entra por laudo. A definição do que cada parte recebe precisa ser precisa.", "Parte do empreendimento. O Volume 05 cita três formatos: societária (a terra vira participação), física (vira unidades) e financeira (vira um percentual da receita).", "Avaliação mal feita. Contrato e efeito tributário de cada formato ficam com advogado, avaliador credenciado e contador.", "Na ferramenta B04: o construtor ou investidor faz a obra e fica com parte da área ou das unidades; você recebe unidades prontas, sem colocar dinheiro. Um compromisso sugerido: pesquisar se construtores da região fazem permuta.")}
{fonte(6, "Pessoa do círculo e venda antecipada", "Do círculo: \"contrato escrito, com as mesmas cláusulas que você exigiria de um desconhecido.\" Do comprador de unidade: projeto e licença.", "Do círculo, juro baixo a médio e às vezes participação. Do comprador, a unidade vendida e a obrigação de entregar.", "A relação, se não houver contrato. Na venda antecipada: \"Pré-venda não é receita. É um passivo com cara de caixa.\"", "\"Trate quem te empresta por confiança com mais rigor contratual, não com menos.\" E o comprador de unidade traz \"o maior risco reputacional de todas as fontes se a entrega atrasar.\" (Volume 05, citado no Z02)")}
<h3>E os outros caminhos?</h3>
<p>O Z02 cita ainda arranjos que mudam o que você precisa ter: condo-hotel, multipropriedade, contrato de gestão e franquia. Condo-hotel e multipropriedade têm regras jurídicas próprias. Gestão e franquia não trazem dinheiro: mudam quem opera. Como diz o Volume 05: "O imóvel não precisa ser seu para o negócio ser seu."</p>
<div class="ouro"><h3>Parceria com fornecedores</h3><p style="margin:0">Condições especiais de fornecedor (prazo, parcelamento, troca por divulgação) não aparecem nas fontes Zion como fonte de capital do projeto. Se surgir, trate como uma proposta qualquer: por escrito, com o que ela cobra e o que compromete. Na Folha Única, o que você deve a fornecedor entra como dívida.</p></div>{ROD(8)}</section>''')

# 9 · custo real
P.append(f'''<section class="pg"><div class="sec">Capítulo 2 · comparar</div><h2>O preço real <i>de cada fonte</i></h2>
<p class="lead">Comparar fontes só pela taxa ignora quase tudo o que decide.</p>
<div class="cita">"Capital tem cinco componentes de custo. Juro, diluição, garantia, tempo e liberdade."<small>Volume 05 · Investimento, citado no Z02 (Custo Real do Capital™)</small></div>
<table><tr><th>Componente</th><th>O que é</th></tr>
<tr><td><b>Juro</b></td><td>O custo financeiro somado em reais ao longo do prazo, não a taxa anual.</td></tr>
<tr><td><b>Diluição</b></td><td>A participação cedida vezes o valor estimado do negócio na sua saída.</td></tr>
<tr><td><b>Garantia</b></td><td>O que fica comprometido se der errado. O imóvel do empreendimento é uma coisa; o aval pessoal é outra.</td></tr>
<tr><td><b>Tempo</b></td><td>Meses até o dinheiro estar na conta vezes o custo de cada mês de atraso.</td></tr>
<tr><td><b>Liberdade</b></td><td>O que você deixa de decidir sozinho: aprovação prévia, limite de endividamento, veto a novo sócio.</td></tr></table>
<p>Juro, diluição e tempo viram reais e se somam. Garantia e liberdade ficam escritas ao lado e entram no julgamento. "Juro zero nunca significa capital gratuito."</p>
<h3>A escada do controle cedido</h3>
<div class="grid grid3" style="grid-template-columns:repeat(4,1fr)"><div class="card"><b>Cede nada</b><small>Capital próprio e etapa menor. Todo o risco é seu.</small></div><div class="card"><b>Cede juro</b><small>Banco, fomento, pessoa do círculo com contrato.</small></div><div class="card"><b>Cede participação</b><small>Sócio investidor, permuta por participação.</small></div><div class="card"><b>Cede propriedade</b><small>Condo-hotel, multipropriedade, venda de unidade.</small></div></div>
<p class="fonte">Escada: leitura do Z02 a partir do Volume 05 (edição do projeto). Arrendamento e pré-venda cedem outras coisas.</p>
<div class="ex"><b class="rot">Exemplo ilustrativo do Z02 · dados fictícios</b><p style="margin:0">Para cobrir R$ 300.000, o Z02 compara duas alternativas hipotéticas em cinco anos. Dívida: R$ 108.000 de juro e R$ 20.000 de tempo, R$ 128.000 no total, com imóvel e aval pessoal em garantia. Sócio: R$ 300.000 de diluição e R$ 30.000 de tempo, R$ 330.000, sem garantia. Na soma, a dívida custa menos da metade. Mas a primeira parcela anual seria de R$ 96.000, cobrada com a obra em andamento. "A régua não escolhe por você: ela mostra o que você está trocando."</p></div>{ROD(9)}</section>''')

# 10 · a ordem certa
P.append(f'''<section class="pg"><div class="sec">Capítulo 3</div><h2>A ordem certa <i>antes de pedir</i></h2>
<p class="lead">Capital procura confiança. "Confiança nasce de método." <span class="fonte">(Manual Oficial do Método Zion 360°, citado no F06)</span></p>
<p>A Ordem das Coisas lista o que falta na maioria dos projetos que não encontram capital. Os quatro primeiros itens formam a ordem deste kit:</p>
<div class="ordem"><div><b>1 · Território</b>Leitura do lugar feita.<br><small>Acesso, entorno, o que atrai e o que limita.</small></div><div><b>2 · Mercado</b>Mercado medido.<br><small>Diária e ocupação com dado coletado.</small></div><div><b>3 · Produto</b>Produto definido.<br><small>O que construir, quantas unidades, para quem.</small></div><div><b>4 · Conta</b>Modelagem defensável.<br><small>Conta completa, cenários, quanto falta.</small></div></div>
<p>Os outros dois itens da lista vêm depois: estrutura societária limpa e operação que não depende de uma pessoa. Sem esses itens, avisa a fonte, o projeto "é lido como intenção, e intenção não tem preço de mercado." <span class="fonte">(A Ordem das Coisas, Cap. 4, citado no F06)</span></p>
<div class="cita">"Primeiro compreendemos o lugar. Depois desenhamos a experiência. Somente então estruturamos o restante do negócio."<small>Manual Oficial, sobre o caso Zion, citado no Z02</small></div>
<h3>O portão do capital</h3>
<p>O F00 junta cinco condições. Cada uma fica aprovada, pendente ou reprovada.</p>
<table><tr><th>Condição</th><th>Como verificar</th></tr>
<tr><td><b>1 · Estrutura antes do capital</b></td><td>Território, mercado e produto com evidência.</td></tr>
<tr><td><b>2 · Conta completa</b></td><td>O que ninguém orça, contingência e capital de giro, cada linha com fonte e data.</td></tr>
<tr><td><b>3 · Conservador paga as contas</b></td><td>Rodar o cenário conservador da etapa, com rampa.</td></tr>
<tr><td><b>4 · Perda dentro do limite</b></td><td>Perda máxima no pior caso, com aportes e garantias pessoais.</td></tr>
<tr><td><b>5 · Fonte nomeada</b></td><td>Nome, proposta escrita e os cinco custos: juro, diluição, garantia, tempo e liberdade.</td></tr></table>
<p class="fonte">Tabela: síntese do F00, Cap. 5, sobre o Panorama, o Volume 05 e o Z02.</p>{ROD(10)}</section>''')

# 11 · leitura do portão e quanto pedir
P.append(f'''<section class="pg"><div class="sec">Capítulo 3 · continuação</div><h2>Quanto pedir: <i>o número exato</i></h2>
<div class="grid grid3"><div class="card"><b>Alguma reprovada</b><small>Recuar ou mudar a premissa: fase, porta, prazo ou fonte, antes de qualquer cheque.</small></div><div class="card"><b>Alguma pendente</b><small>Estruturar antes de captar. "Avance no que custa tempo, não no que compromete capital."</small></div><div class="card"><b>Todas aprovadas</b><small>Pronto para conversar com capital de terceiros, com assessoria. Conversar não é captar.</small></div></div>
<p class="fonte">"Uma reprovada basta para recuar. Uma pendente basta para não captar ainda." (F00, Cap. 5)</p>
<h3>A Régua do Quanto Captar™</h3>
<p>"Captar de menos é o erro mais comum, e o mais caro, porque a segunda rodada acontece no pior momento de negociação da sua vida." A régua tem quatro linhas de necessidade, "e a terceira e a quarta são as que somem dos pedidos". <span class="fonte">(Volume 05, citado no Z02)</span></p>
<ol><li><b>CAPEX da fase:</b> o investimento até a fase receber o primeiro hóspede, com data de cada cotação.</li>
<li><b>Capital de giro:</b> o que mantém a operação viva nos primeiros meses. A régua usa três meses de custo fixo.</li>
<li><b>Reserva de implantação:</b> de 10% a 15% do CAPEX, com regra de uso escrita.</li>
<li><b>Custo da própria captação:</b> jurídico, laudos, estruturação e registro, de 2% a 5% do valor captado.</li></ol>
<p>Mais o terreno ainda não pago e menos o capital próprio contratado. O resultado vai exato: "Pedir um número redondo acima da conta é um sinal de que a conta não foi feita."</p>
<div class="ex"><b class="rot">Exemplo ilustrativo · Sítio Exemplo · dados fictícios</b>
<table><tr><th>Linha</th><th class="n">Valor</th></tr>
<tr><td>CAPEX da etapa 1 (orçamento escrito)</td><td class="n">R$ 240.000,00</td></tr>
<tr><td>Terreno ainda não pago (a terra já é do Cláudio)</td><td class="n">R$ 0,00</td></tr>
<tr><td>Capital de giro: 3 × R$ 9.000 + R$ 12.000 de rampa</td><td class="n">R$ 39.000,00</td></tr>
<tr><td>Reserva de implantação: 12% × R$ 240.000</td><td class="n">R$ 28.800,00</td></tr>
<tr><td>Custo da captação (orçamento)</td><td class="n">R$ 7.200,00</td></tr>
<tr class="tot"><td>Total necessário</td><td class="n">R$ 315.000,00</td></tr>
<tr><td>Menos capital próprio contratado</td><td class="n">− R$ 3.000,00</td></tr>
<tr class="tot"><td>Lacuna da etapa 1</td><td class="n">R$ 312.000,00</td></tr></table>
<p style="margin:0">Se o Cláudio pedisse só o CAPEX menos o que tem (R$ 237.000), faltariam R$ 75.000 no meio do caminho: o giro, a reserva e o custo da captação.</p></div>{ROD(11)}</section>''')

# 12 · primeiro pedido
P.append(f'''<section class="pg"><div class="sec">Capítulo 4</div><h2>Como montar o <i>primeiro pedido</i></h2>
<p class="lead">"Quem pede dinheiro vende uma promessa. Quem capta vende um ativo com quatro camadas, e sabe o preço de cada uma." <span class="fonte">(Volume 05, citado no F05 e no F06)</span></p>
<p>As quatro camadas são fluxo, ativo, opção de crescimento e capacidade de execução. O banco olha fluxo e ativo. O investidor olha tese e execução. "Apresentar a camada errada para a fonte errada é o erro mais comum e o mais invisível: a conversa não trava, ela esfria."</p>
<h3>As três partes do pedido</h3>
<ol class="passos"><li><b>A frase do pedido.</b> Uma frase que diz o formato, o valor e para quê. Valor exato, saído da régua.</li>
<li><b>O uso dos recursos.</b> Cada real com destino escrito: CAPEX da etapa 1, giro, reserva e custo da captação. Mostre de onde vem o restante.</li>
<li><b>O que você oferece.</b> O que você põe (a terra, por laudo; a gestão local; o projeto) e o que espera do parceiro. Papéis e contrapartidas descritos.</li></ol>
<div class="grid"><div class="card"><b>Pedido vago</b><small>"Procuro alguém para investir." Sem valor de aporte. Sem dizer o que o parceiro recebe. Contrato de boca.</small></div>
<div class="card"><b>Proposta clara</b><small>Formato indicado. Valor buscado. Contrapartidas e papéis descritos. Estrutura validada com advogado e contador. (B10)</small></div></div>
<div class="ex"><b class="rot">Exemplo ilustrativo da ferramenta B10 · fictício</b><p style="margin:0">"Buscamos sócio com aporte de R$ 400.000 para a implantação. O proprietário entra com a terra e a gestão local. Participação e responsabilidades a definir em acordo, com assessoria jurídica."</p></div>
<h3>Para banco, a frase é outra</h3>
<p>O F05 ensina a frase do crédito, que nasce da conta e não da vontade: "pedimos até R$ X, em Y meses, com carência de Z, garantia real sobre..., cobertura no ano dois de A no base e B no conservador; se cair abaixo de 1,2, reduzimos o valor ou...". Se a frase disser que a dívida não cabe, o mapa cumpriu o papel: você soube antes de assinar.</p>
<div class="caixa"><h3>Escreva o seu rascunho</h3><div class="linha"></div><div class="linha"></div><div class="linha"></div></div>{ROD(12)}</section>''')

# 13 · exercício em branco
linhas = "".join(f'<tr><td class="f">{n}</td><td></td><td></td><td></td><td></td></tr>' for n in ["1 · Capital próprio e etapa menor", "2 · Banco, cooperativa e fomento", "3 · Sócio que entra com capital", "4 · Sócio operador ou arrendamento", "5 · Permuta e parcerias", "6 · Círculo e venda antecipada"])
P.append(f'''<section class="pg"><div class="sec">Exercício</div><h2>O seu <i>Mapa das Fontes</i></h2>
<p>Preencha aqui à mão ou direto na planilha (aba Fontes). Situação: <b>D</b> disponível, <b>P</b> possível, <b>F</b> fora.</p>
<table style="margin-bottom:2mm"><tr><td style="width:50%;border:1px solid var(--areia)"><b>Necessidade da etapa 1 (régua):</b> R$</td><td style="border:1px solid var(--areia)"><b>Capital próprio contratado:</b> R$</td></tr><tr><td style="border:1px solid var(--areia)"><b>Lacuna:</b> R$</td><td style="border:1px solid var(--areia)"><b>Valor de referência da terra:</b> R$</td></tr></table>
<table class="ficha"><tr><th>Fonte</th><th style="width:12mm">D / P / F</th><th style="width:26mm">Quanto cobre (R$)</th><th>Por quê (uma linha)</th><th>Próxima pergunta e para quem</th></tr>{linhas}</table>
<h3>Prontidão: marque o que já é verdade</h3>
<ul class="chk" style="columns:2;column-gap:7mm;font-size:9.2pt">
<li>Matrícula atualizada e pendências conhecidas.</li><li>Território lido: acesso, entorno, o que atrai.</li><li>Diária do destino com dado coletado.</li><li>Sei o que construir na etapa 1 e para quem.</li><li>Orçamento escrito e conta completa com giro e reserva.</li><li>Cenário conservador paga as contas.</li><li>Limite de perda escrito; sei o que fica em garantia.</li><li>Fonte nomeada, com proposta escrita.</li><li>Dinheiro de pessoa próxima só com contrato.</li><li>Contas do projeto separadas das pessoais.</li></ul>
<p class="fonte">Um item sem marca basta para "estruturar antes de captar" (F00, Cap. 5). Não é reprovação: é a lista do que fazer primeiro.</p>
<h3>Próximo passo, com data</h3>
<table class="ficha"><tr><th>Ação</th><th style="width:30mm">Data</th></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr></table>{ROD(13)}</section>''')

# 14 · exemplo preenchido
P.append(f'''<section class="pg"><div class="sec">Exercício · exemplo</div><h2>O mapa do Sítio Exemplo <i>preenchido</i></h2>
<div class="ex"><b class="rot">Exemplo ilustrativo · dados fictícios · igual à planilha de exemplo</b>
<p>O Cláudio tem uma terra de referência de R$ 200.000, R$ 3.000 contratados e lacuna de R$ 312.000 na etapa 1. A terra vale 0,64 vez a lacuna: pesa na negociação, mas sozinha não resolve.</p>
<table><tr><th>Fonte</th><th>Situação</th><th class="n">Cobre (R$)</th><th>Por quê</th></tr>
<tr><td>1 · Etapa menor</td><td>Possível</td><td class="n">60.000</td><td>Menos unidades na etapa 1 reduzem o CAPEX. Falta o projeto inteiro desenhado.</td></tr>
<tr><td>2 · Banco</td><td>Possível</td><td class="n">83.000</td><td>Parcela de R$ 1.500 com taxa e prazo de uma simulação fictícia: R$ 83.247,68 financiáveis. Parcela na obra não testada.</td></tr>
<tr><td>3 · Sócio capital</td><td>Possível</td><td class="n">150.000</td><td>Só depois de estruturar: hoje não há pasta que se audite.</td></tr>
<tr><td>4 · Operador</td><td>Fora</td><td class="n">0</td><td>Ele quer operar a hospedagem.</td></tr>
<tr><td>5 · Permuta</td><td>Possível</td><td class="n">0</td><td>Não sabe se construtores da região fazem permuta.</td></tr>
<tr><td>6 · Círculo</td><td>Fora</td><td class="n">0</td><td>O irmão ofereceu, mas sem contrato escrito não conta.</td></tr>
<tr class="tot"><td colspan="2">Soma das possíveis</td><td class="n">293.000</td><td>Cobre 93,9% da lacuna. Ainda faltam R$ 19.000.</td></tr></table>
<p style="margin:0"><b>Prontidão:</b> 4 de 10 itens. Leitura: estruturar antes de captar. <b>Primeiro passo:</b> enviar o Mapa preenchido e agendar a sessão estratégica. Depois: matrícula (20/11), orçamento escrito (30/11), três bancos (05/12) e diária de cinco concorrentes (10/12).</p></div>
<h3>O que o exemplo ensina</h3>
<ul><li><b>Nenhuma fonte sozinha cobre a lacuna.</b> A combinação é a regra, não a exceção.</li>
<li><b>"Possível" não é "contratado".</b> Os R$ 293.000 são hipóteses. Cada um precisa virar proposta por escrito.</li>
<li><b>O primeiro passo custa tempo, não dinheiro.</b> Certidão, orçamento, pesquisa de diária e três perguntas a três bancos.</li>
<li><b>O exemplo não promete nada.</b> Ele mostra como organizar a conversa. O resultado depende do caso, da execução e da decisão de quem empresta ou investe.</li></ul>{ROD(14)}</section>''')

# 15 · erros comuns
P.append(f'''<section class="pg"><div class="sec">Capítulo 5</div><h2>Erros comuns <i>que esfriam a conversa</i></h2>
<p class="lead">O F00 lista doze sinais vermelhos. Sinal vermelho não reprova sozinho: aponta o que verificar primeiro. Estes são os que mais aparecem em quem tem terra e pouco capital.</p>
<table><tr><th style="width:44%">Erro</th><th>O que fazer em vez disso</th></tr>
<tr><td><b>Pedir dinheiro antes de saber para quê</b></td><td>Estruturar para captar: território, mercado, produto e conta, nessa ordem.</td></tr>
<tr><td><b>Pedir um número redondo, sem reserva</b></td><td>Usar a Régua do Quanto Captar. Número exato, com giro, reserva e custo da captação.</td></tr>
<tr><td><b>Planilha otimista</b></td><td>"Planilha otimista é o começo de um projeto quebrado." Rodar o conservador.</td></tr>
<tr><td><b>Contar dinheiro que ainda não chegou</b></td><td>Só vale o "contratado, não esperado".</td></tr>
<tr><td><b>Dinheiro de pessoa próxima sem contrato</b></td><td>Contrato escrito, com as cláusulas que você exigiria de um desconhecido.</td></tr>
<tr><td><b>Aval pessoal não precificado</b></td><td>Separar garantia real de aval e negociar o aval com a seriedade da taxa.</td></tr>
<tr><td><b>Dívida com parcela antes da operação</b></td><td>Perguntar a carência por escrito e fazer o teste de fôlego.</td></tr>
<tr><td><b>Caixa misturado com a conta pessoal</b></td><td>"Sem separação não há captação, porque investidor não consegue avaliar o que não está separado."</td></tr>
<tr><td><b>Levar fotos da terra, e não um projeto</b></td><td>Apresentar a oportunidade: ativo, destino, mercado, conceito, investimento e modelo de parceria (B10).</td></tr>
<tr><td><b>Fazer tudo de uma vez</b></td><td>Fasear: "Fasear não é falta de ambição. É o que faz a ambição caber no caixa."</td></tr>
<tr><td><b>Esperar ter todo o capital para começar</b></td><td>Começar pelo que custa tempo: certidão, orçamento, pesquisa de diária, perguntas aos bancos.</td></tr></table>
<p class="fonte">Fontes: F00, Cap. 5 (sinais vermelhos); Z02, Caps. 4 e 5; F05, Cap. 1; B10.</p>{ROD(15)}</section>''')

# 16 · próximo passo
P.append(f'''<section class="pg fim escuro"><div class="foto" style="background-image:url({FOTO['fim']})"></div><div class="veu"></div><div class="w">
<img src="{LOGO_C}" alt="Zion" style="height:13mm;align-self:flex-start;margin-bottom:auto">
<div class="sec">Seu próximo passo</div><h2 style="font-size:34pt">Envie o seu Mapa e agende a sua <i>sessão estratégica</i></h2>
<p style="font-size:12pt">A sua entrada no Club Zion Collection inclui <b style="color:var(--creme)">1 sessão estratégica individual de 45 minutos</b> com a equipe Zion. Preencha o seu Mapa das Fontes de Capital e envie pelo WhatsApp da Zion. No WhatsApp, a Zaya, assistente virtual da Zion, confere o Mapa e envia o link da agenda. Na sessão, a equipe olha o seu caso e indica o próximo passo.</p>
<p style="margin:5mm 0 2mm"><a class="btn" href="{LINK}">Enviar meu Mapa no WhatsApp</a></p>
<p class="url">WhatsApp da Zion: +55 48 6137-1061 · wa.me/554861371061</p>
<h3 style="color:var(--ouro);margin-top:6mm">Quem é a Zion</h3>
<p>A Zion já operou vários glampings, tem os dois primeiros glampings pioneiros de referência no Brasil (Urubici e Florianópolis) e está desenvolvendo mais de 23 destinos. <b style="color:var(--creme)">O seu destino pode ser o próximo.</b></p>
<h3 style="color:var(--ouro)">Mentoria Zion</h3>
<p>Quem tiver perfil é convidado, na sessão, para a Mentoria Zion, a formação completa do Método Zion 360°. A Zion avalia cada caso.</p>
<p style="font-size:8.6pt;color:var(--areia);margin-top:5mm;border-top:1px solid rgba(222,214,191,.35);padding-top:3mm">Material educativo da Zion Hotel Group International. Não é promessa de crédito, investidor, sociedade, renda ou retorno, nem garante aprovação de crédito ou licenças. Exemplos com dados fictícios. Contratos, garantias e sociedade se decidem com advogado e contador. Dúvidas: WhatsApp +55 48 6137-1061. Foto: operação Zion Bubble Glamping.</p></div></section>''')

html = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Kit Inicial · Como captar recursos para o seu projeto</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
(B / "guia.html").write_text(html, encoding="utf-8"); print("ok", B / "guia.html", len(P), "páginas")

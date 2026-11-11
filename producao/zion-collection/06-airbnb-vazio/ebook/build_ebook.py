"""Monta o e-book 06 em HTML (60 páginas A4). O PDF sai de render_ebook.js (Playwright).
Uso: python3 -I producao/zion-collection/06-airbnb-vazio/ebook/build_ebook.py"""
import html, json, pathlib, sys
A = pathlib.Path(__file__).resolve().parent
R = A.parents[3]
sys.path.insert(0, str(A))
import diagramas as DG

E = lambda s: html.escape(str(s), quote=True)
URI = lambda p: (R / p).as_uri()
TITULO = "Seu Airbnb Está Vazio?"
SUB = "O problema pode estar na sua oferta"
CAPS = [json.load(open(f)) for f in sorted((A / "conteudo").glob("cap*.json"))]
assert len(CAPS) == 10
FOTOS = {1: "operacoes/op09.webp", 2: "operacoes/op08.webp", 3: "store/dentro.webp", 4: "operacoes/op04.webp", 5: "operacoes/op07.webp",
         6: "store/noite.webp", 7: "operacoes/op12.webp", 8: "store/deck.webp", 9: "operacoes/op11.webp", 10: "store/noturna.webp"}
LEGENDA = "Foto real · Zion Bubble Glamping (SC). Ilustra o ambiente; o método vale para qualquer tipo de hospedagem."

CSS = f"""
@font-face{{font-family:Cormorant;src:url({URI('docs/assets/fonts/cormorant.woff2')}) format("woff2");font-weight:300 700}}
@font-face{{font-family:Cormorant;font-style:italic;src:url({URI('docs/assets/fonts/cormorant-italic.woff2')}) format("woff2")}}
@font-face{{font-family:Aventa;src:url({URI('docs/assets/fonts/aventa.woff2')}) format("woff2")}}
@page{{size:210mm 297mm;margin:0}}
:root{{--preto:#040605;--musgo:#1B2117;--creme:#FEF5F0;--areia:#DED6BF;--terra:#8B714E;--ouro:#C9B37E;--tinta:#1d211b}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0;background:#777}}
body{{font-family:Aventa,Jost,sans-serif;color:var(--tinta);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:210mm;height:297mm;position:relative;overflow:hidden;background:var(--creme);page-break-after:always;break-after:page;margin:0 auto}}
.pg+.pg{{margin-top:0}}
h1,h2,h3{{font-family:Cormorant,Georgia,serif;font-weight:400;margin:0;line-height:1.05}}
.run{{position:absolute;top:11mm;left:16mm;right:16mm;display:flex;justify-content:space-between;font-size:7.5pt;letter-spacing:.18em;text-transform:uppercase;color:var(--terra);border-bottom:.3mm solid var(--areia);padding-bottom:2.5mm}}
.folio{{position:absolute;bottom:9mm;left:16mm;right:16mm;display:flex;justify-content:space-between;font-size:7.5pt;letter-spacing:.14em;color:var(--terra);text-transform:uppercase}}
.folio b{{font-family:Cormorant,serif;font-size:13pt;letter-spacing:0;color:var(--tinta);font-weight:400}}
.miolo{{position:absolute;top:22mm;bottom:18mm;left:16mm;right:16mm;overflow:hidden}}
.miolo h2{{font-size:27pt;color:var(--musgo);margin:3mm 0 4mm}}
.kick{{font-size:7.5pt;letter-spacing:.24em;text-transform:uppercase;color:var(--terra)}}
.col{{column-count:2;column-gap:7mm;column-rule:.2mm solid rgba(139,113,78,.25);font-size:var(--fs,9.6pt);line-height:1.5;text-align:justify;hyphens:auto}}
.col p{{margin:0 0 2.6mm}}
.col h4{{font-family:Cormorant,serif;font-size:14pt;font-weight:600;color:var(--musgo);margin:3mm 0 1.5mm;break-after:avoid}}
.col ul,.col ol{{margin:0 0 2.6mm;padding-left:5mm}}
.col li{{margin:0 0 1.2mm}}
.col ul{{list-style:none;padding-left:4mm}}.col ul li:before{{content:"—";color:var(--ouro);margin-left:-4mm;position:absolute}}
.col ul li{{position:relative}}
.caixa{{break-inside:avoid;background:rgba(201,179,126,.13);border-left:1.2mm solid var(--ouro);padding:3mm 3.5mm;margin:1mm 0 3mm;text-align:left}}
.caixa b.t{{display:block;font-family:Cormorant,serif;font-size:13pt;font-weight:600;color:var(--musgo);margin-bottom:1mm}}
.caixa ul{{margin:0}}
.exemplo{{break-inside:avoid;border-left:1.2mm solid var(--musgo);background:#fff;padding:3mm 3.5mm;margin:1mm 0 3mm;text-align:left}}
.exemplo b.t{{display:block;font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:var(--terra);margin-bottom:1.2mm}}
.erro{{break-inside:avoid;border:.3mm dashed var(--terra);padding:2.5mm 3mm;margin:1mm 0 3mm;text-align:left;font-size:.95em}}
.quote{{break-inside:avoid;font-family:Cormorant,serif;font-style:italic;font-size:15pt;line-height:1.2;color:var(--musgo);text-align:left;margin:2mm 0 3.5mm;padding-top:2.5mm;border-top:.5mm solid var(--ouro);width:85%}}
.span{{column-span:all;margin:1mm 0 4mm}}
table{{border-collapse:collapse;width:100%;font-size:.92em;text-align:left;break-inside:avoid;margin:1mm 0 3mm}}
th{{background:var(--musgo);color:var(--creme);font-weight:400;font-size:.9em;letter-spacing:.06em;padding:1.6mm 2mm;text-align:left}}
td{{border-bottom:.2mm solid var(--areia);padding:1.6mm 2mm;vertical-align:top}}
.dg{{break-inside:avoid;background:#fff;border:.2mm solid var(--areia);padding:3mm 4mm;margin:1mm 0 4mm}}
/* abertura */
.ab .foto{{position:absolute;top:0;left:0;right:0;height:150mm;background-size:cover;background-position:center}}
.ab .foto:after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,6,5,.25) 0%,rgba(4,6,5,.15) 40%,rgba(27,33,23,.92) 92%,var(--musgo) 100%)}}
.ab .num{{position:absolute;right:10mm;top:60mm;font-family:Cormorant,serif;font-style:italic;font-size:150pt;line-height:1;color:var(--ouro);opacity:.92;z-index:2}}
.ab .topo{{position:absolute;top:96mm;left:16mm;right:16mm;z-index:2;color:var(--creme)}}
.ab .topo .kick{{color:var(--ouro)}}
.ab .topo h1{{font-size:38pt;color:var(--creme);margin:2mm 0 2mm;max-width:150mm}}
.ab .topo .deck{{font-family:Cormorant,serif;font-style:italic;font-size:15pt;color:var(--areia);max-width:150mm}}
.ab .base{{position:absolute;top:150mm;bottom:0;left:0;right:0;background:var(--musgo);color:var(--areia);padding:8mm 16mm 18mm;display:grid;grid-template-columns:1.25fr 1fr;gap:9mm;font-size:10pt;line-height:1.55}}
.ab .base p{{margin:0 0 3mm}}
.ab .regra{{width:16mm;height:.6mm;background:var(--ouro);margin:0 0 4mm}}
.ab .aprender{{border-left:.4mm solid var(--ouro);padding-left:5mm}}
.ab .aprender .kick{{color:var(--ouro);display:block;margin-bottom:2mm}}
.ab .aprender li{{margin:0 0 2mm}}
.ab .aprender ul{{padding-left:4mm;margin:0}}
.ab .legenda{{position:absolute;left:16mm;right:16mm;bottom:9mm;font-size:6.8pt;color:rgba(222,214,191,.6);letter-spacing:.06em}}
.ab .folio{{color:var(--ouro)}}.ab .folio b{{color:var(--creme)}}
/* exercício */
.ex .miolo{{font-size:var(--fs,9.6pt);line-height:1.45}}
.campo{{margin:0 0 3.2mm;break-inside:avoid}}
.campo .rot{{font-weight:600;color:var(--musgo);font-size:9.3pt}}
.linha{{border-bottom:.25mm solid rgba(139,113,78,.45);height:var(--lh,6.6mm)}}
.check{{display:grid;grid-template-columns:1fr 1fr;gap:1.5mm 6mm;margin:2mm 0 4mm;font-size:9pt}}
.check div{{display:flex;gap:2mm}}.check i{{flex:none;width:3.6mm;height:3.6mm;border:.3mm solid var(--terra);margin-top:.6mm}}
.fech{{background:var(--musgo);color:var(--areia);padding:4mm 5mm;font-size:9.6pt;border-left:1.2mm solid var(--ouro)}}
/* capa e escuras */
.escura{{background:var(--musgo);color:var(--areia)}}
.escura .folio{{color:var(--ouro)}}.escura .folio b{{color:var(--creme)}}
.capa{{background:radial-gradient(120% 80% at 70% 20%,#26301f 0%,var(--musgo) 45%,var(--preto) 100%);color:var(--creme)}}
.capa .logo{{position:absolute;top:16mm;left:18mm;height:13mm}}
.capa .kick{{position:absolute;top:36mm;left:18mm;color:var(--ouro)}}
.capa h1{{position:absolute;top:46mm;left:18mm;right:18mm;font-size:58pt;line-height:.98;color:var(--ouro)}}
.capa .sub{{position:absolute;top:104mm;left:18mm;right:90mm;font-family:Cormorant,serif;font-style:italic;font-size:22pt;color:var(--creme);line-height:1.15}}
.capa .tel{{position:absolute;right:16mm;top:112mm;width:72mm;height:144mm;border-radius:9mm;border:2.2mm solid #0b0e09;box-shadow:0 0 0 .4mm var(--ouro),0 14mm 30mm rgba(0,0,0,.55);background-size:cover;background-position:top center;overflow:hidden}}
.capa .tel2{{right:62mm;top:150mm;width:56mm;height:108mm;opacity:.85;transform:rotate(-6deg)}}
.capa .itens{{position:absolute;left:18mm;top:150mm;width:62mm;font-size:9pt;line-height:1.5;color:var(--areia)}}
.capa .itens div{{padding:2.3mm 0;border-top:.2mm solid rgba(201,179,126,.35)}}
.capa .itens b{{color:var(--creme);font-weight:400;font-family:Cormorant,serif;font-size:13pt;display:block}}
.capa .publico{{position:absolute;left:18mm;right:18mm;bottom:16mm;font-size:8pt;letter-spacing:.2em;text-transform:uppercase;color:var(--ouro);border-top:.3mm solid rgba(201,179,126,.5);padding-top:4mm;display:flex;justify-content:space-between}}
.sum li{{display:flex;align-items:baseline;gap:3mm;padding:2.6mm 0;border-bottom:.2mm solid var(--areia);font-size:11pt}}
.sum li span.n{{font-family:Cormorant,serif;font-style:italic;font-size:22pt;color:var(--terra);width:12mm}}
.sum li span.t{{flex:1;font-family:Cormorant,serif;font-size:16pt;color:var(--musgo)}}
.sum li span.p{{font-size:9pt;color:var(--terra)}}
.ficha td,.ficha th{{padding:2.2mm 2mm}}.ficha td{{height:11mm}}
.diario td,.diario th{{padding:0 1.5mm!important;height:6.9mm!important;font-size:7.5pt}}
.dg svg{{max-height:62mm;width:auto!important;max-width:100%;margin:0 auto}}
"""


def bloco(b):
    t = b["t"]
    if t == "p": return f"<p>{E(b['txt'])}</p>"
    if t == "h": return f"<h4>{E(b['txt'])}</h4>"
    if t == "lista": return "<ul>" + "".join(f"<li>{E(i)}</li>" for i in b["itens"]) + "</ul>"
    if t == "passos": return "<ol>" + "".join(f"<li>{E(i)}</li>" for i in b["itens"]) + "</ol>"
    if t == "caixa": return f'<div class="caixa"><b class="t">{E(b["titulo"])}</b><ul>' + "".join(f"<li>{E(i)}</li>" for i in b["itens"]) + "</ul></div>"
    if t == "exemplo": return f'<div class="exemplo"><b class="t">{E(b["titulo"])}</b>{E(b["txt"])}</div>'
    if t == "quote": return f'<div class="quote">{E(b["txt"])}</div>'
    if t == "erro": return f'<div class="erro">{E(b["txt"])}</div>'
    if t == "tabela":
        return '<table class="span"><tr>' + "".join(f"<th>{E(c)}</th>" for c in b["cab"]) + "</tr>" + "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in l) + "</tr>" for l in b["linhas"]) + "</table>"
    if t == "diagrama": return f'<div class="dg span">{DG.TODOS[b["id"]]()}</div>'
    raise ValueError(t)


PAGS = []
def pag(classe, corpo, run=None, folio=True, escuro=False):
    n = len(PAGS) + 1
    r = f'<div class="run"><span>Zion Collection · {E(TITULO)}</span><span>{E(run)}</span></div>' if run else ""
    f = f'<div class="folio"><span>Zion Hotel Group International · material educativo</span><b>{n:02d}</b></div>' if folio else ""
    PAGS.append(f'<section class="pg {classe}" data-n="{n}">{r}{corpo}{f}</section>')
    return n


# 1 · capa
pag("capa", f"""<img class="logo" src="{URI('docs/brand/zion-logo-claro.png')}" alt="Zion Hotel Group International">
<div class="kick">Zion Collection · Gestão · Guia prático</div><h1>{E(TITULO)}</h1><div class="sub">{E(SUB)}.</div>
<div class="tel tel2" style="background-image:url({(A/'img/tela-notas.jpg').as_uri()})"></div>
<div class="tel" style="background-image:url({(A/'img/tela-resultado.jpg').as_uri()})"></div>
<div class="itens"><div><b>10 capítulos</b>do sintoma ao plano de ação</div><div><b>Diagnóstico Zion de Oferta</b>7 dimensões, nota com evidência</div><div><b>Plano de 30 dias</b>com responsável, prazo e indicador</div></div>
<div class="publico"><span>Para Airbnb, casas, apartamentos, pousadas e glampings</span><span>60 páginas</span></div>""", folio=False)

# 2 · como usar
pag("", f"""<div class="miolo"><p class="kick">Antes de começar</p><h2>Como usar este guia</h2><div class="col" style="--fs:10pt">
<p>Este guia ensina o passo a passo para descobrir por que o seu calendário tem tantas datas livres e o que mudar primeiro. Ele não traz fórmulas mágicas: traz um jeito organizado de olhar a sua oferta com os olhos do hóspede, registrar evidências e decidir com calma.</p>
<p>Cada capítulo tem a mesma estrutura: uma abertura que mostra o problema, três páginas de conteúdo com exemplos e um exercício para fazer na sua hospedagem. Leia um capítulo por dia ou um por semana; o importante é fazer o exercício antes de seguir.</p>
<div class="caixa"><b class="t">O que você precisa ter em mãos</b><ul><li>O calendário dos últimos 90 dias.</li><li>O link do seu anúncio e as fotos publicadas.</li><li>As últimas avaliações e mensagens de hóspedes.</li><li>Seus custos do mês (mesmo que aproximados).</li><li>A ferramenta Diagnóstico Zion de Oferta, aberta no celular ou no computador.</li></ul></div>
<h4>Como ler os exemplos</h4><p>Todos os números deste guia que aparecem em exemplos são <b>dados fictícios</b>, criados para ensinar a conta. Não são resultados de clientes nem médias de mercado. Use as fórmulas com os seus próprios números.</p>
<h4>O que este guia não promete</h4><p>Nenhum material consegue garantir reservas, ocupação ou faturamento: isso depende da região, da época, da concorrência, das regras de cada plataforma e da sua execução. O que você leva daqui é clareza para decidir e um plano para executar e medir.</p>
<h4>Sobre as fotos</h4><p>As fotos das aberturas são reais, da Zion Bubble Glamping, em Santa Catarina. Elas ilustram o ambiente. Os exemplos e o método valem para Airbnb, casas, apartamentos, pousadas e glampings.</p>
<h4>Regras das plataformas</h4><p>Nomes de painéis, taxas, políticas e regras mudam. Sempre que o guia falar de uma regra da plataforma, confira a versão atual na central de ajuda dela.</p>
<div class="quote">Primeiro clareza. Depois ação. Depois medição.</div>
<p style="font-size:8.5pt;color:#6b6250">© Zion Hotel Group International. Uso pessoal do comprador. Proibida a revenda ou distribuição. Suporte: WhatsApp +55 48 6137-1061.</p>
</div></div>""", run="Como usar")

# 3 · sumário (páginas calculadas: capítulo n abre em 5 + (n-1)*5)
itens = "".join(f'<li><span class="n">{c["num"]:02d}</span><span class="t">{E(c["titulo"])}</span><span class="p">p. {5 + (c["num"] - 1) * 5}</span></li>' for c in CAPS)
pag("", f"""<div class="miolo"><p class="kick">Sumário</p><h2>O caminho, em dez passos</h2><ul class="sum" style="list-style:none;padding:0;margin:0">
<li><span class="n">·</span><span class="t">Introdução: o calendário não mente, mas também não explica</span><span class="p">p. 4</span></li>{itens}
<li><span class="n">·</span><span class="t">Fichas para imprimir e glossário</span><span class="p">p. 55</span></li><li><span class="n">·</span><span class="t">De onde vem o método e próximos passos</span><span class="p">p. 59</span></li></ul></div>""", run="Sumário")

# 4 · introdução
pag("escura", f"""<div class="miolo" style="color:var(--areia)"><p class="kick" style="color:var(--ouro)">Introdução</p><h2 style="color:var(--creme)">O calendário não mente, mas também não explica</h2>
<div class="col" style="--fs:10.2pt;column-rule-color:rgba(201,179,126,.3)">
<p>Você abre o aplicativo e vê de novo: semanas inteiras livres. Muda a diária, troca uma foto, pergunta para um amigo. Às vezes uma reserva aparece e você não sabe se foi pela mudança ou por sorte. E a dúvida volta no domingo à noite: o que está errado?</p>
<p>A primeira reação costuma ser baixar o preço. Parece a alavanca mais rápida. Mas o hóspede não escolhe só pelo preço: ele compara fotos, título, avaliações, a rapidez da resposta e a sensação de que vai receber o que viu. Se a oferta não está clara, baixar a diária só faz você ganhar menos pelo mesmo problema.</p>
<div class="quote" style="color:var(--creme)">Calendário vazio é um sintoma. A causa costuma estar na oferta.</div>
<p>Este guia troca o palpite por um processo. Nos capítulos 1 a 7 você aprende a olhar cada parte da oferta: números, concorrência, produto, anúncio, preço, confiança e conversão. No capítulo 8 você junta tudo no Diagnóstico Zion de Oferta, dá nota de 0 a 5 a sete dimensões e descobre as três prioridades. Nos capítulos 9 e 10 você transforma as prioridades em um plano de 30 dias e aprende a medir antes e depois.</p>
<p>Usamos uma lente de foco que acompanha o guia inteiro: de tudo que dá para melhorar, escolha os poucos pontos que mais pesam na decisão do hóspede (20%); deles, a ação da semana (4%); dela, o primeiro passo que cabe em menos de uma hora hoje (0,8%). É uma regra prática para não se perder, não uma promessa estatística.</p>
<div class="caixa" style="background:rgba(201,179,126,.1);color:var(--areia)"><b class="t" style="color:var(--creme)">O que você terá ao final</b><ul><li>A fotografia real do seu negócio nos últimos 90 dias.</li><li>Sete notas com evidência e três prioridades.</li><li>Um plano de 30 dias com responsável, prazo e indicador.</li><li>Um jeito de comparar antes e depois sem se enganar.</li></ul></div>
</div></div>""", run="Introdução", escuro=True)

# capítulos
for c in CAPS:
    n = c["num"]
    abertura = "".join(f"<p>{E(p)}</p>" for p in c["abertura"].split("\n\n"))
    pag("ab", f"""<div class="foto" style="background-image:url({(A / 'img' / (FOTOS[n].split('/')[1].replace('.webp', '.jpg'))).as_uri()})"></div><div class="num">{n:02d}</div>
<div class="topo"><span class="kick">Capítulo {n:02d}</span><h1>{E(c['titulo'])}</h1><div class="deck">{E(c['deck'])}</div></div>
<div class="base"><div><div class="regra"></div>{abertura}</div><div class="aprender"><span class="kick">Neste capítulo você vai</span><ul>{''.join(f'<li>{E(i)}</li>' for i in c['aprender'])}</ul></div></div>
<div class="legenda">{LEGENDA}</div>""")
    for p in c["paginas"]:
        pag("ct", f'<div class="miolo"><p class="kick">Capítulo {n:02d} · {E(c["titulo"])}</p><h2>{E(p["titulo"])}</h2><div class="col">{"".join(bloco(b) for b in p["blocos"])}</div></div>', run=f"Capítulo {n:02d}")
    x = c["exercicio"]
    if n == 8:  # tabela real das sete dimensões no lugar dos campos agrupados
        x = dict(x); x["campos"] = [f for f in x["campos"] if not f["rotulo"].startswith("Nota e evidência")]
        dims8 = ["Fotos e apresentação", "Título e descrição", "Preço e posicionamento", "Diferenciais e experiência", "Avaliações e confiança", "Atendimento e comunicação", "Conforto e infraestrutura"]
        tab8 = '<table class="ficha" style="margin-bottom:4mm"><tr><th>Dimensão</th><th style="width:16mm">Nota</th><th>Evidência</th></tr>' + "".join(f"<tr><td style='width:50mm;height:9mm'>{i + 1}. {E(d)}</td><td></td><td></td></tr>" for i, d in enumerate(dims8)) + "</table>"
    else:
        tab8 = ""
    campos = tab8 + "".join(f'<div class="campo"><div class="rot">{E(f["rotulo"])}</div>' + '<div class="linha"></div>' * int(f.get("linhas", 2)) + "</div>" for f in x["campos"])
    chk = "".join(f"<div><i></i><span>{E(i)}</span></div>" for i in x["checklist"])
    pag("ex", f"""<div class="miolo"><p class="kick">Capítulo {n:02d} · Exercício</p><h2>{E(x['titulo'])}</h2><p style="margin:0 0 4mm">{E(x['instrucao'])}</p>{campos}
<p class="kick" style="margin-top:2mm">Pronto quando</p><div class="check">{chk}</div><div class="fech">{E(x['fechamento'])}</div></div>""", run=f"Capítulo {n:02d} · Exercício")

# 55 · ficha diagnóstico
dims = ["Fotos e apresentação", "Título e descrição", "Preço e posicionamento", "Diferenciais e experiência", "Avaliações e confiança", "Atendimento e comunicação", "Conforto e infraestrutura"]
linhas = "".join(f"<tr><td style='width:46mm'><b>{i + 1}. {E(d)}</b></td><td style='width:20mm'></td><td></td></tr>" for i, d in enumerate(dims))
pag("", f"""<div class="miolo"><p class="kick">Ficha para imprimir 1 de 3</p><h2>Diagnóstico Zion de Oferta</h2>
<p style="font-size:9.5pt;margin:0 0 3mm">Nota de 0 a 5: 0 ausente · 1 muito fraco · 2 fraco · 3 parcial · 4 bom · 5 consistente e comprovado. Sem evidência, a nota é hipótese.</p>
<table class="ficha"><tr><th>Dimensão</th><th>Nota</th><th>Evidência (o que comprova a nota)</th></tr>{linhas}</table>
<table class="ficha"><tr><th>Soma (0 a 35)</th><th>Pontuação = soma ÷ 35 × 100</th><th>Faixa</th></tr><tr><td></td><td></td><td style="font-size:8pt;color:#6b6250">0–49 lacunas relevantes · 50–69 ajustes prioritários · 70–84 boa base · 85–100 consistente</td></tr></table>
<table class="ficha"><tr><th style="width:12mm">#</th><th>As três menores notas (empate: vale a ordem acima)</th></tr><tr><td>1</td><td></td></tr><tr><td>2</td><td></td></tr><tr><td>3</td><td></td></tr></table>
<p style="font-size:8pt;color:#6b6250">Indicador orientativo para priorizar melhorias. Não é previsão de reservas, ocupação ou faturamento.</p></div>""", run="Fichas")

# 56 · ficha plano
lp = "".join("<tr>" + "<td></td>" * 6 + "</tr>" for _ in range(7))
pag("", f"""<div class="miolo"><p class="kick">Ficha para imprimir 2 de 3</p><h2>Plano de ação</h2>
<p style="font-size:9.5pt;margin:0 0 3mm">Uma linha por ação. Comece pela prioridade 1. Status: a fazer, em andamento ou feito.</p>
<table class="ficha"><tr><th style="width:52mm">Ação</th><th>Responsável</th><th>Prazo</th><th>Custo (R$)</th><th style="width:36mm">Indicador</th><th>Status</th></tr>{lp}</table>
<div class="caixa" style="font-size:9.5pt"><b class="t">Hipótese da ação da semana</b>Se eu ______________________, então espero que ______________________, medido por ______________________, até ____/____.</div>
<div class="caixa" style="font-size:9.5pt"><b class="t">Primeiro passo de hoje (menos de 1 hora)</b><div class="linha"></div><div class="linha"></div></div></div>""", run="Fichas")

# 57 · ficha registro diário
dias = "".join(f"<tr><td>{d}</td>" + "<td></td>" * 5 + "</tr>" for d in range(1, 31))
pag("", f"""<div class="miolo"><p class="kick">Ficha para imprimir 3 de 3</p><h2 style="font-size:23pt;margin-bottom:2mm">Registro diário · 30 dias</h2>
<table class="ficha diario"><tr><th style="width:9mm">Dia</th><th>Visualizações</th><th>Consultas</th><th>Reservas</th><th>O que mudei hoje</th><th>Observação</th></tr>{dias}</table></div>""", run="Fichas")

# 58 · glossário
gl = [("Noites disponíveis", "Noites do período em que a hospedagem podia ser vendida. Bloqueios (reforma, uso próprio) ficam fora."),
      ("Ocupação", "Noites vendidas ÷ noites disponíveis."), ("Diária média", "Receita de hospedagem ÷ noites vendidas."),
      ("Receita por noite disponível", "Receita de hospedagem ÷ noites disponíveis. Junta preço e ocupação em um número."),
      ("Taxa de consulta", "Consultas ÷ visualizações do anúncio. Mostra se o anúncio desperta interesse."),
      ("Taxa de reserva", "Reservas ÷ consultas. Mostra se a conversa vira reserva."),
      ("Tempo de primeira resposta", "Quanto tempo o hóspede espera pela primeira resposta."),
      ("Piso da diária", "(Custo variável por noite + parte do custo fixo por noite + margem mínima) ÷ (1 − taxas e impostos)."),
      ("Evidência", "Algo que outra pessoa consegue conferir: foto, avaliação, mensagem, número do painel."),
      ("Hipótese testável", "Se eu fizer X, espero Y, medido por Z, até a data D."),
      ("Mesma base de datas", "Comparar períodos equivalentes (mesmos dias da semana, época e noites disponíveis).")]
pag("", '<div class="miolo"><p class="kick">Glossário</p><h2>Os indicadores, em uma página</h2><table style="font-size:9.6pt">' + "".join(f"<tr><td style='width:52mm'><b>{E(a)}</b></td><td>{E(b)}</td></tr>" for a, b in gl) +
    '</table><p style="font-size:8.5pt;color:#6b6250">Os nomes e o lugar de cada número mudam de uma plataforma para outra. Confira na central de ajuda da sua.</p></div>', run="Glossário")

# 59 · de onde vem o método + próximos passos
pag("", f"""<div class="miolo"><p class="kick">De onde vem o método</p><h2>Da operação para o seu calendário</h2>
<div style="height:88mm;background:url({(A / 'img/op05.jpg').as_uri()}) center/cover;margin:0 0 2mm"></div>
<p style="font-size:7.5pt;color:#6b6250;margin:0 0 4mm">Foto real · Zion Bubble Glamping (SC), uma das unidades da Zion Hotel Group International.</p>
<div class="col" style="--fs:10pt"><p>Este guia parte da rotina usada nas unidades da Zion: olhar a oferta com evidência, escolher poucas prioridades, executar com responsável e prazo e medir antes de mudar de novo. Adaptamos essa rotina para quem cuida de um apartamento, uma casa, uma pousada pequena ou um glamping.</p>
<p>O que muda de um negócio para outro são os números e o hóspede. O processo é o mesmo: diagnóstico, prioridade, ação, medição.</p>
<div class="caixa"><b class="t">Seus próximos passos</b><ul><li>Hoje: preencha o Diagnóstico Zion de Oferta.</li><li>Esta semana: execute a ação da prioridade 1.</li><li>Em 30 dias: refaça o diagnóstico com a mesma base de datas.</li><li>Dúvidas: WhatsApp +55 48 6137-1061.</li></ul></div></div></div>""", run="Próximos passos")

# 60 · contracapa
pag("capa", f"""<img class="logo" src="{URI('docs/brand/zion-logo-claro.png')}" alt="Zion Hotel Group International">
<div class="kick">Zion Collection</div><h1 style="font-size:40pt">Primeiro clareza.<br>Depois ação.<br>Depois medição.</h1>
<div class="sub" style="top:120mm;right:18mm;font-size:15pt">Um guia prático para diagnosticar a sua oferta, priorizar melhorias e montar um plano de 30 dias.</div>
<div class="publico"><span>Zion Hotel Group International</span><span>Material educativo · resultados dependem do contexto e da execução</span></div>""", folio=False)

assert len(PAGS) == 60, len(PAGS)
out = A / "dist"; out.mkdir(exist_ok=True)
doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{E(TITULO)} · Zion Collection</title><style>{CSS}</style></head><body>{"".join(PAGS)}</body></html>'
(out / "ebook.html").write_text(doc)
print("dist/ebook.html", len(PAGS), "páginas")

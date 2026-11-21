"""Gera landing/dist/clickmax-A.html (R$ 47), clickmax-B.html (R$ 67) e previa-*.html (imagens locais).
Uso: python3 -I producao/produto-01-terra-capital/landing/build_landing.py"""
import json, pathlib
A = pathlib.Path(__file__).resolve().parent; P = A.parent; R = P.parents[1]
BASE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
HOST = BASE + "p/adbc67069af26ae0/terra-capital/"
AUL = json.load(open(P/"src/aulas.json"))
def pilares():
    out = ""
    for p in AUL["pilares"]:
        ls = [a for a in AUL["aulas"] if a["pilar"] == p["n"]]
        out += f'<details><summary>Pilar {p["n"]} · {p["nome"]} <small>({len(ls)} {"aula" if len(ls)==1 else "aulas"})</small></summary><ul class="mini">' + "".join(f'<li><b>{a["n"]}.</b> {a["titulo"]} <span>→ {a["acao"]}</span></li>' for a in ls) + "</ul></details>"
    return out
def build(preco, utm_v):
    UTM = f"?utm_source=meta&utm_medium=paid&utm_campaign=p01_terra_capital&utm_content=landing&price_version={utm_v}"
    return f"""<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">
<style>
.zl{{--musgo:#1B2117;--creme:#FEF5F0;--areia:#DED6BF;--terra:#8B714E;--champ:#C9B37E;--muted:#A39E8E;background:#040605;color:#FEF5F0;font-family:"Jost",Arial,sans-serif;font-size:17px;line-height:1.6;overflow-x:hidden}}
.zl *{{box-sizing:border-box}} body{{margin:0;background:#040605}}
.zl .gut{{padding-left:20px;padding-right:20px}} .zl .col{{max-width:680px;margin:0 auto}} .zl .wide{{max-width:1040px;margin:0 auto}} .zl section{{padding-block:68px}}
.zl h1,.zl h2,.zl h3{{font-family:"Cormorant Garamond",Georgia,serif;font-weight:400;line-height:1.05;margin:0 0 18px;color:#FEF5F0}}
.zl h1{{font-size:clamp(38px,8.4vw,72px)}} .zl h2{{font-size:clamp(32px,6.4vw,50px)}} .zl h3{{font-size:25px}}
.zl em{{color:#C9B37E;font-style:italic}}
.zl p,.zl li{{color:#DED6BF;font-family:"Jost",Arial,sans-serif}} .zl span{{color:inherit}}
.zl .eyebrow{{display:block;font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:#C9B37E;margin-bottom:16px;font-weight:500}}
.zl .btn{{display:inline-block;background:#C9B37E;color:#040605;font-weight:600;text-decoration:none;padding:18px 28px;border-radius:2px;letter-spacing:.07em;text-transform:uppercase;font-size:15px}}
.zl .micro{{display:block;font-size:13px;color:#A39E8E;margin-top:12px}}
.zl .hero{{background:radial-gradient(circle at 80% 10%,#2c3524 0%,#1B2117 52%,#040605 100%);padding-block:56px 64px}}
.zl .hgrid{{display:grid;grid-template-columns:1fr;gap:34px;align-items:center}}@media(min-width:860px){{.zl .hgrid{{grid-template-columns:1.1fr .9fr}}}}
.zl .phones{{display:flex;justify-content:center;gap:0}} .zl .ph{{width:44%;max-width:210px;border:5px solid #040605;border-radius:26px;overflow:hidden;box-shadow:0 14px 40px rgba(0,0,0,.55);background:#fff}} .zl .ph img{{width:100%;display:block}}
.zl .ph.a{{transform:rotate(-4deg) translateY(14px)}} .zl .ph.b{{transform:rotate(4deg);margin-left:-12px}}
.zl .lista{{list-style:none;padding:0;margin:22px 0}} .zl .lista li{{padding:13px 0;border-top:1px solid rgba(222,214,191,.16);color:#FEF5F0}}
.zl .caixa{{background:#1B2117;border:1px solid rgba(201,179,126,.35);border-radius:6px;padding:26px}}
.zl .preco{{font-family:"Cormorant Garamond",serif;font-size:68px;color:#C9B37E;line-height:1}}
.zl details{{border-top:1px solid rgba(222,214,191,.16);padding:14px 0}} .zl summary{{cursor:pointer;color:#FEF5F0;font-weight:500}} .zl summary small{{color:#A39E8E;font-weight:400}}
.zl ul.mini{{list-style:none;padding:8px 0 0}} .zl ul.mini li{{padding:7px 0;font-size:15.5px;border:0}} .zl ul.mini span{{display:block;color:#A39E8E;font-size:14px}}
.zl .shots{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:26px 0}} .zl .shots img{{width:100%;border-radius:12px;display:block;border:1px solid rgba(222,214,191,.18)}} .zl .shots figcaption{{font-size:13px;color:#A39E8E;margin-top:6px}}
@media(max-width:620px){{.zl .shots{{grid-template-columns:1fr 1fr}}}}
.zl video{{width:100%;max-width:300px;display:block;margin:20px auto;border-radius:18px;border:5px solid #040605;box-shadow:0 14px 40px rgba(0,0,0,.55)}}
.zl .duo{{display:grid;grid-template-columns:1fr;gap:24px;align-items:center}}@media(min-width:760px){{.zl .duo{{grid-template-columns:1fr 1fr}}}}
.zl .duo img.r{{width:100%;border-radius:6px;display:block}}
.zl .aviso{{font-size:14px;color:#A39E8E;border-left:2px solid #C9B37E;padding-left:12px;margin:18px 0}}
.zl .cap{{font-size:13px;color:#A39E8E;margin-top:8px}}
</style>
<div class="zl">
<section class="hero gut" data-cx-section="hero"><div class="wide hgrid"><div>
<img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:34px">
<span class="eyebrow">Zion Hotel Academy · Produto 01</span>
<h1>Você tem um terreno em um destino turístico, mas <em>não tem capital</em> para investir?</h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo de como transformar seu terreno em um projeto turístico e preparar seu patrimônio para buscar recursos, investidores e parceiros.</p>
<p style="margin:26px 0 0"><a class="btn" href="#oferta" data-cx-cta>Quero estruturar meu projeto</a></p>
<span class="micro">Pagamento único, Pix ou cartão à vista. Reembolso em até 7 dias. Material educativo: não garante crédito, sócio ou investimento.</span></div>
<div class="phones"><div class="ph a"><img src="{HOST}img/tela-lacuna-resultado.jpg" alt="Tela do simulador de lacuna de capital, com dados fictícios"></div><div class="ph b"><img src="{HOST}img/tela-mapa.jpg" alt="Tela do mapa mental dos sete pilares"></div></div></div></section>

<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow">A dor</span>
<h2>Terra não é caixa. E <em>pedir dinheiro sem saber quanto</em> fecha portas.</h2>
<p>Você tem o terreno, a vista e a vontade. Mas um imóvel não paga fornecedor até virar transação ou receita, e quem pode ajudar quer ver números, documentos e riscos. Sem isso, a conversa não anda.</p>
<ul class="lista"><li>Você não sabe exatamente quanto falta para começar.</li><li>Não sabe se o terreno pode receber hospedagem, nem o que o esgoto e a energia custam.</li><li>Tem medo de oferecer a terra em garantia e perder o que a família construiu.</li><li>Não sabe como apresentar o projeto a um possível sócio sem prometer o que não pode.</li></ul></div></section>

<section class="gut" data-cx-section="solution" style="background:#0b0f0a"><div class="col"><span class="eyebrow">A transformação</span>
<h2>De “tenho terra” para um <em>dossiê organizado</em>, em uma tarde.</h2>
<p>Em 70 a 100 minutos, no seu ritmo, você sai com uma lacuna de capital calculada, um cenário ruim testado, um checklist com pendências visíveis e um dossiê preliminar em PDF para levar a advogado, contador e possíveis parceiros.</p>
<ul class="lista"><li><b style="color:#C9B37E">Entenda</b> a diferença entre patrimônio e caixa.</li><li><b style="color:#C9B37E">Calcule</b> investimento, reserva e a lacuna, sem contar valorização futura.</li><li><b style="color:#C9B37E">Compare</b> crédito, parceria, arrendamento e começar menor.</li><li><b style="color:#C9B37E">Prepare</b> a conversa, sem prometer retorno e sem esconder risco.</li></ul></div></section>

<section class="gut" data-cx-section="solution"><div class="wide"><div class="col"><span class="eyebrow">Veja funcionando</span>
<h2>A ferramenta de verdade, <em>antes de comprar</em>.</h2>
<p>É a tela real do portal, com <b style="color:#FEF5F0">dados fictícios</b>: investimento de R$ 220 mil, reserva de R$ 30 mil e recursos próprios de R$ 50 mil. A ferramenta mostra a lacuna de R$ 200 mil. Depois testa uma parcela e a cobertura do caixa em um mês fraco.</p></div>
<video controls playsinline preload="metadata" poster="{HOST}img/tela-lacuna-resultado.jpg" src="{HOST}img/demo-voz.mp4"></video>
<p class="cap" style="text-align:center">Gravação da ferramenta, 20 segundos, com narração (voz sintética). Toque para ouvir. Valores ilustrativos; parcela sem tarifas, seguros ou indexação.</p>
<div class="shots"><figure style="margin:0"><img src="{HOST}img/tela-lacuna.jpg" alt="Investimento e capital de giro"><figcaption>Lacuna de capital</figcaption></figure><figure style="margin:0"><img src="{HOST}img/tela-divida.jpg" alt="Dívida e cobertura"><figcaption>Dívida e cobertura</figcaption></figure><figure style="margin:0"><img src="{HOST}img/tela-aula.jpg" alt="Microaula com atividade"><figcaption>Microaula + tarefa</figcaption></figure></div></div></section>

<section class="gut" style="background:#0b0f0a"><div class="wide duo"><div><span class="eyebrow">Os entregáveis</span><h2>Você não compra só um e-book. Você <em>monta um dossiê</em>.</h2>
<ul class="lista"><li><b style="color:#C9B37E">20 microaulas em vídeo</b>, de cerca de 1 minuto, cada uma com uma tarefa e o conteúdo também por escrito</li><li><b style="color:#C9B37E">Guia em PDF de 60 páginas</b> com atividade e anotações</li><li><b style="color:#C9B37E">Simuladores</b> de lacuna de capital, operação e dívida (Price e SAC)</li><li><b style="color:#C9B37E">Checklist documental</b> com evidência e responsável</li><li><b style="color:#C9B37E">Mapa mental</b> e <b style="color:#C9B37E">mapa de desenvolvimento</b></li><li><b style="color:#C9B37E">Plano de ação</b> de 30 dias e priorização 20% · 4% · 0,8%</li><li><b style="color:#C9B37E">Gerador de Dossiê</b> com exportação em PDF</li></ul></div>
<div><img class="r" src="{HOST}img/ebook-capa.jpg" alt="Capa do guia Você tem terra. Falta capital?"><p class="cap">Capa do guia em PDF. As telas mostradas têm dados fictícios.</p></div></div></section>

<section class="gut" data-cx-section="social-proof"><div class="wide duo"><div><img class="r" src="{BASE}assets/bruno/palco-azul.webp" alt="Bruno Chaerk em palestra" style="max-height:560px;object-fit:cover;object-position:top"></div>
<div><span class="eyebrow">Quem ensina</span><h2>Zion Hotel Group <em>International</em></h2>
<p>Bruno Chaerk é founder e CEO da Zion Hotel Group International. Formado dentro de grandes redes hoteleiras internacionais, na Espanha, ele trouxe ao Brasil uma leitura de hotelaria como ativo estruturado, com marca, tese e saída.</p>
<p>Com mais de 20 anos no setor, Bruno criou um método a partir dos grandes projetos de hotéis e resorts que desenvolveu. Hoje ele também ajuda pequenos, médios e grandes empreendedores que querem entrar no setor de hospedagem de uma maneira simples, como ter a primeira casa de aluguel por temporada ou o primeiro Airbnb.</p>
<p style="color:#FEF5F0">Se você está começando, com um terreno e uma ideia, este método também foi pensado para você.</p>
<p>O método desta jornada parte da forma como a Zion organiza projetos antes de pedir dinheiro a alguém.</p></div></div>
<div class="col" style="margin-top:40px"><img src="{BASE}assets/operacoes/op09.webp" alt="Vista aérea de uma unidade da Zion Bubble Glamping" style="width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:6px;display:block"><p class="cap">Foto real · Zion Bubble Glamping. Mostra de onde vem o método; o conteúdo vale para outros tipos de hospedagem. Não indica resultado que você terá.</p></div></section>

<section class="gut" style="background:#0b0f0a"><div class="col"><span class="eyebrow">Conteúdo</span><h2>Sete pilares, <em>20 microaulas</em>.</h2><p>Cada aula tem uma pergunta de abertura, o conteúdo em passos curtos e uma tarefa com a ferramenta aberta ao lado.</p>{pilares()}</div></section>

<section class="gut"><div class="col"><span class="eyebrow">Benefícios práticos</span><h2>O que muda <em>na prática</em>.</h2>
<ul class="lista"><li>Você sabe quanto falta, com premissas escritas.</li><li>Sabe quanto o projeto aguenta no cenário ruim, e quando parar.</li><li>Sabe o que perguntar à prefeitura, ao advogado e ao banco.</li><li>Chega a uma conversa com sócio ou instituição com documentos e pendências organizados.</li><li>Decide com evidência: avançar, investigar mais ou interromper.</li></ul>
<p class="aviso">A jornada ensina e organiza. Não aprova crédito, não encontra sócio, não garante investimento nem retorno, e não substitui advogado, contador ou engenheiro.</p></div></section>

<section class="gut" data-cx-section="offer" id="oferta" style="background:#0b0f0a"><div class="col"><span class="eyebrow">A oferta</span><h2>Comece seu <em>plano de ação</em> hoje.</h2>
<div class="caixa"><ul class="lista" style="margin-top:0"><li>20 microaulas em vídeo, com tarefa e área de membros</li><li>Guia em PDF de 60 páginas</li><li>Simuladores, checklist, mapas e plano de 30 dias</li><li>Gerador de Dossiê preliminar em PDF</li></ul>
<p style="margin-top:8px">O valor aparece no checkout logo abaixo. Pagamento único, Pix ou cartão à vista. Acesso liberado depois da confirmação do pagamento. O progresso e as respostas ficam salvos no seu aparelho.</p>
<div data-cx-checkout></div><p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor. Suporte: +55 48 6137-1061.</p></div></div></section>

<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow">Perguntas frequentes</span><h2>Antes de decidir</h2>
<details><summary>Preciso ter dinheiro?</summary><p>Não para estudar e organizar o projeto. Mas desenvolver exige recursos e viabilidade, e a jornada mostra como calcular quanto falta.</p></details>
<details><summary>O curso garante financiamento?</summary><p>Não. Ninguém pode prometer crédito aprovado, sócio ou investidor. Você aprende a comparar caminhos e preparar sua proposta.</p></details>
<details><summary>Preciso dar meu terreno em garantia?</summary><p>Não. A jornada compara também alternativas sem garantia, como parceria, arrendamento e começar menor.</p></details>
<details><summary>Recebo um projeto arquitetônico?</summary><p>Não. O resultado é um plano e um dossiê preliminares, preenchidos por você.</p></details>
<details><summary>O curso é personalizado?</summary><p>As ferramentas são preenchidas por você. Não inclui consultoria individual.</p></details>
<details><summary>As aulas são em vídeo?</summary><p>Sim. As 20 microaulas têm vídeo narrado de cerca de um minuto (narração sintética), com o mesmo conteúdo por escrito e a ferramenta na mesma tela.</p></details>
<details><summary>Meus dados ficam seguros?</summary><p>Suas respostas ficam salvas no seu aparelho; o PDF é gerado no seu navegador. Não peça nem envie documentos pessoais: anote só o que for necessário.</p></details>
<details><summary>Em quanto tempo uso?</summary><p>O acesso é liberado depois da confirmação do pagamento. Estimamos de 70 a 100 minutos de aprendizado e prática. O resultado externo, como crédito ou parceria, depende de terceiros e não é prometido.</p></details>
<details><summary>Como funciona o reembolso?</summary><p>Você pode pedir reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></details></div></section>

<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Antes de pedir dinheiro, <em>descubra quanto falta</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero estruturar meu projeto</a><span class="micro">Material educativo. Não promete crédito aprovado, sócio, investidores nem rentabilidade.</span></div></section>
</div>"""
(A/"dist").mkdir(exist_ok=True)
for nome, preco, v in (("A", "47", "A47"), ("B", "67", "B67")):
    pass
for nome, preco, v in (("A", "47", "A47"),):
    h = build(preco, v); (A/f"dist/clickmax.html").write_text(h)
    loc = h.replace(HOST, (P/"landing/").as_uri().replace("landing/", "landing/")+"").replace(BASE, (R/"docs").as_uri()+"/")
    loc = loc.replace((P/"landing").as_uri()+"img/", (P/"landing/img").as_uri()+"/")
    (A/f"dist/previa.html").write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1>'.replace('1>','1">') + loc.replace('<div data-cx-checkout></div>','<div style="border:1px dashed #C9B37E;padding:16px;text-align:center;color:#C9B37E">[ checkout do ClickMax aparece aqui ]</div>'))
    print(nome, len(h))

"""Gera landing/dist/clickmax.html da Sessão Zion 360° (R$ 270). Uso: python3 -I landing/build_landing.py"""
import pathlib
A = pathlib.Path(__file__).resolve().parent
BASE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
QUIZ = "https://api.clickmax.io/forms/lkHmsew5L-351jjLAfICkwtz"
UTM = "utm_source=pagina&utm_medium=landing&utm_campaign=sessao-270&utm_content="
CSS = """<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">
<style>
.zs{font-family:'Jost',sans-serif;background:#040605;color:#FEF5F0;line-height:1.55;font-size:17px}
.zs *{box-sizing:border-box}
.zs section{padding:56px 20px}.zs .col{max-width:760px;margin:0 auto}
.zs h1,.zs h2{font-family:'Cormorant Garamond',serif;font-weight:600;color:#FEF5F0;line-height:1.1;margin:0 0 18px}
.zs h1{font-size:clamp(38px,9vw,60px)}.zs h2{font-size:clamp(30px,6.5vw,42px)}
.zs em{color:#C9B37E;font-style:italic}.zs p,.zs li{color:#DED6BF}.zs b{color:#FEF5F0}
.zs .eyebrow{display:block;color:#C9B37E;font-size:13px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:14px}
.zs .alt{background:#1B2117}
.zs .btn{display:block;text-align:center;background:#C9B37E;color:#1B2117;font-weight:600;padding:17px 22px;border-radius:999px;text-decoration:none;margin:22px 0 10px;font-size:18px}
.zs .btn2{display:block;text-align:center;border:1px solid #C9B37E;color:#C9B37E;padding:14px 22px;border-radius:999px;text-decoration:none;margin:8px 0}
.zs .micro{display:block;color:#A39E8E;font-size:14px}
.zs ul{padding-left:20px}.zs li{margin:8px 0}
.zs .card{background:#1B2117;border:1px solid #3a4130;border-radius:14px;padding:22px;margin:16px 0}
.zs .alt .card{background:#040605}
.zs .preco{font-family:'Cormorant Garamond',serif;font-size:56px;color:#C9B37E;line-height:1}
.zs img.foto{width:100%;border-radius:14px;display:block;margin:18px 0}
.zs details{border-top:1px solid #3a4130;padding:14px 0}.zs summary{cursor:pointer;color:#FEF5F0;font-weight:500}
.zs .aviso{border-left:3px solid #C9B37E;padding:10px 14px;background:#1B2117;margin:18px 0}
.zs .fixo{position:fixed;left:0;right:0;bottom:0;z-index:50;background:#040605ee;padding:10px 16px;border-top:1px solid #3a4130}
.zs .fixo a{margin:0}
.zs{padding-bottom:84px}
</style>"""
def cta(cont, txt="Contratar minha sessão — R$270"):
    return f'<a class="btn" href="#oferta" data-cx-cta>{txt}</a>'
def quiz(cont):
    return f'<a class="btn2" href="{QUIZ}?{UTM}{cont}">Fazer meu Raio-X gratuito</a>'
ESPELHO = ["Terra parada, sem saber por onde começar.", "Falta capital para tirar o projeto do papel.", "Capital disponível, mas sem direção.", "Você busca um sócio ou investidores e não sabe como se apresentar.", "Sem orçamento claro para a obra.", "Hospedagem aberta, mas sem vendas."]
ENTREGA = ["Sessão individual online de 60 minutos", "Diagnóstico preliminar personalizado", "Avaliação preliminar do projeto", "Estratégia de busca de recursos, sócios e investidores", "Argumentação comercial preliminar", "Dossiê personalizado em PDF", "Plano de ação de 30/60/90 dias", "Acesso ao Zion Land Bank, sem cobrança adicional (cadastro sujeito a avaliação)", "Área de membros Zion com documentos e conteúdos introdutórios"]
FAQ = [("A sessão é online?", "Sim. É individual, por videochamada, com 60 minutos, no horário de Brasília."),
 ("O preço é único?", "Sim: R$ 270, pagamento único, em Pix ou cartão. O checkout mostra o valor total antes de você confirmar."),
 ("Quando o calendário abre?", "Só depois da confirmação do pagamento. Você recebe um acesso individual para escolher o horário. Não existe agenda pública nem sessão gratuita."),
 ("O que eu recebo e quando?", "Diagnóstico e plano na sessão; o dossiê em PDF e o plano de 30/60/90 dias são revisados pela equipe e enviados à sua área de membros, com previsão de até 2 dias úteis após a sessão."),
 ("O acesso ao Land Bank e à área de membros tem custo extra?", "Não. O acesso ao Land Bank vem sem cobrança adicional, mas o cadastro passa por avaliação. A área de membros traz os documentos e conteúdos introdutórios da sessão. Clube e cursos pagos não estão incluídos."),
 ("Posso remarcar?", "Sim, pelo link individual que você recebe na confirmação da reserva."),
 ("E se eu desistir?", "Você tem reembolso em até 7 dias após a compra, como prevê o Código de Defesa do Consumidor."),
 ("Tem garantia de parceria, investimento ou crédito?", "Não. A Zion avalia cada caso, e esta sessão não é uma oferta de crédito. Ela organiza o seu projeto e mostra caminhos possíveis.")]
html = CSS + f"""<div class="zs">
<section data-cx-section="hero" style="background:#1B2117"><div class="col">
<img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:30px;margin-bottom:34px">
<span class="eyebrow">Sessão individual · 60 minutos · online</span>
<h1>Seu terreno pode ser o <em>próximo destino da Zion.</em></h1>
<p style="font-size:20px">Tem um terreno em um destino turístico e quer entrar no Airbnb, mas falta capital ou não sabe por onde começar? Conheça nossas estratégias para estruturar projetos, buscar recursos, sócios e investidores.</p>
{cta('hero')}{quiz('hero-secundario')}
<span class="micro">O calendário só abre após a confirmação do pagamento. Parceria não é garantida: a Zion avalia cada caso.</span>
</div></section>
<section data-cx-section="problem"><div class="col"><span class="eyebrow">Você se reconhece?</span>
<h2>Muita gente começa pela obra. <em>O certo é começar pela estratégia.</em></h2>
<ul>{''.join(f'<li>{x}</li>' for x in ESPELHO)}</ul>
<p>Também atendemos quem já tem hospedagem e quer vender melhor, e quem está começando e ainda não tem terreno.</p></div></section>
<section class="alt" data-cx-section="solution"><div class="col"><span class="eyebrow">Quem conduz</span>
<h2>Bruno Chaerk, <em>fundador da Zion.</em></h2>
<img class="foto" src="{BASE}assets/bruno/retrato-sorriso.webp" alt="Bruno Chaerk, fundador da Zion Hotel Group">
<p>A Zion nasceu da prática: operamos a Zion Bubble Glamping, em Urubici e Florianópolis, e o método que ensinamos vem dessa rotina. A sessão aplica esse olhar ao seu caso.</p>
<span class="eyebrow" style="margin-top:28px">O que olhamos juntos</span>
<p>Desenvolvimento, gestão, operação, identidade e vendas: as cinco frentes que decidem se um projeto de hospedagem sai do papel.</p></div></section>
<section data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow">O que você recebe</span>
<h2>Uma hora, um diagnóstico, <em>um plano de ação.</em></h2>
<div class="card"><ul style="margin:0">{''.join(f'<li>{x}</li>' for x in ENTREGA)}</ul></div>
<div class="card"><div class="preco">R$ 270</div>
<p>Pagamento único, Pix ou cartão. O valor total aparece no checkout antes de você confirmar.</p>
<div class="aviso"><b>Antes de pagar:</b> o calendário só abre depois da confirmação do pagamento, e parceria, investimento e crédito não são garantidos.</div>
<div data-cx-checkout></div></div></div></section>
<section class="alt" data-cx-section="faq"><div class="col"><span class="eyebrow">Perguntas frequentes</span>
{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)}</div></section>
<section data-cx-section="cta"><div class="col" style="text-align:center"><h2>Comece pela <em>estratégia.</em></h2>
{cta('final')}{quiz('final-secundario')}
<span class="micro">Zion Hotel Group International · material e sessão de natureza educativa e consultiva.</span></div></section>
<div class="fixo"><a class="btn" href="#oferta" data-cx-cta>Contratar minha sessão — R$270</a></div>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(html); print(len(html))

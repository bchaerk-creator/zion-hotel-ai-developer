"""Gera landing/dist/clickmax.html da Ferramenta 22 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
import pathlib
A = pathlib.Path(__file__).resolve().parent
src = (A.parents[1] / "17-checklist-limpeza/landing/build_landing.py").read_text()
estilo = src[src.index('<link href='):src.index('</style>') + len('</style>')].replace("{{", "{").replace("}}", "}")
BASE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
def linha(a, b, cor):
    return (f'<div style="display:flex;justify-content:space-between;gap:6px;padding:7px 10px;border-top:1px solid #DED6BF;font-size:12px">'
            f'<span style="color:#1B2117">{a}</span><span style="color:#1B2117;background:{cor};padding:0 6px;border-radius:4px;font-weight:600">{b}</span></div>')
def tela(tit, status, cor, linhas, leg):
    return (f'<figure style="margin:0"><div style="background:#fff;border-radius:10px;overflow:hidden"><div style="background:#1B2117;padding:10px">'
            f'<span style="color:#C9B37E;font-size:11px;letter-spacing:.12em">{tit} · EXEMPLO FICTÍCIO</span></div>'
            f'<div style="background:{cor};padding:10px;font-weight:700;font-size:13px"><span style="color:#040605">{status}</span></div>{"".join(linhas)}</div>'
            f'<figcaption>{leg}</figcaption></figure>')
V, A_, M, G, AZ = "#F4C7C3", "#FCE8B2", "#C8E6C0", "#E6E6E6", "#D6E4F0"
t1 = tela("PERÍODOS FRACOS", "3 de 4 abaixo da meta de 50%", A_,
          [linha("Março depois do Carnaval · 22%", "Abaixo da meta", A_), linha("Semanas de abril · 56%", "Na meta", M),
           linha("Maio, dias úteis · 32%", "Abaixo da meta", A_), linha("Começo de junho · 20%", "Sem campanha", V)],
          "Ocupação de cada período contra a sua meta.")
t2 = tela("CAMPANHAS", "Piso da diária: R$ 300", V,
          [linha("Estadia longa · 15% · R$ 357", "OK", M), linha("Pacote com experiência · R$ 420", "OK", M),
           linha("Última hora · 35% · R$ 273", "Abaixo do piso", V), linha("Tema especial · abril", "Começa depois", V)],
          "Desconto conferido antes de ir para o ar.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow" style="color:#C9B37E">Ferramenta 22 · Zion Hospitality Business</span>
<h1>Calendário vazio <em>nos mesmos meses?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para encontrar os períodos fracos da sua hospedagem, planejar campanhas sem vender abaixo do piso e acompanhar o que cada campanha trouxe.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings.</span><a class="btn" href="#oferta" data-cx-cta>Quero o planner</a><span class="micro" style="color:#A39E8E">Planilha + ficha de campanha + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow" style="color:#C9B37E">O problema</span>
<h2>Na última hora, <em>só sobra baixar o preço</em>.</h2>
<p>Todo ano o período fraco chega e a reação é a mesma: uma semana antes, a diária cai até o hóspede aparecer. Às vezes cai tanto que a estadia nem paga a limpeza. E ninguém lembra, no ano seguinte, o que funcionou.</p>
<ul class="lista"><li>Campanha decidida em cima da hora.</li><li>Desconto sem olhar o piso da diária.</li><li>Nenhum registro do que trouxe reserva.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow" style="color:#C9B37E">Como funciona</span>
<h2>Planeje antes, <em>com trava no piso</em>.</h2>
<p>Você lista os períodos que costumam ficar vazios e a planilha mostra a ocupação de cada um contra a sua meta. Para cada período fraco, você planeja campanhas: estadia longa, pacote com experiência, público da região, hóspedes que já vieram. A planilha confere se a diária com desconto fica acima do piso e se cobre o custo da estadia, e avisa se a campanha começa tarde demais.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Resultados calculados pela planilha no arquivo de exemplo (chalés, datas e valores fictícios).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Preencha a base: diária, piso, taxas, custo e meta.</li><li><b style="color:#C9B37E">2.</b> Liste os períodos fracos dos próximos meses.</li><li><b style="color:#C9B37E">3.</b> Planeje uma campanha por período, com antecedência.</li><li><b style="color:#C9B37E">4.</b> Anote as noites vendidas e repita o que funcionou.</li></ul></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow" style="color:#C9B37E">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/campanhas-22/capa.jpg" alt="Capa do produto: Planner de Campanhas para Períodos de Baixa Procura" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco para até 20 períodos e 60 campanhas</li><li>Exemplo preenchido (dados fictícios)</li><li>Ficha de campanha para imprimir</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow" style="color:#C9B37E">Perguntas frequentes</span>
<details><summary>Não sei o meu piso da diária. E agora?</summary><p>Calcule com a sua conta de custos ou com a Planilha Diária Mínima, vendida separadamente. Sem piso, a planilha confere só se a estadia cobre o custo.</p></details>
<details><summary>A planilha garante reservas?</summary><p>Não. Ela organiza e confere as campanhas que você planejar. Reserva depende também de preço, anúncio, localização e avaliações.</p></details>
<details><summary>Publica as campanhas?</summary><p>Não. Você publica na plataforma, no Instagram ou envia aos seus contatos, sempre com autorização.</p></details>
<details><summary>Serve para uma casa só?</summary><p>Sim. Informe 1 unidade na base.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>O período fraco vem todo ano. <em>O plano também.</em></h2>
<a class="btn" href="#oferta" data-cx-cta>Quero o planner</a><span class="micro" style="color:#A39E8E">Material educativo. Não garante reservas nem resultado. Faturamento não é lucro.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))

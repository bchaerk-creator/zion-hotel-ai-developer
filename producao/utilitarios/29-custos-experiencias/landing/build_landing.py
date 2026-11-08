"""Gera landing/dist/clickmax.html da Ferramenta 29 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
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
V, A_, M = "#F4C7C3", "#FCE8B2", "#C8E6C0"
t1 = tela("RESULTADO DA SESSÃO", "Cobre os custos com 8 participantes", M,
          [linha("Receita (8 pessoas)", "R$ 1.440,00", "#FFFFFF"), linha("Taxas e impostos", "R$ 158,40", "#FFFFFF"), linha("Custos por participante", "R$ 640,00", "#FFFFFF"),
           linha("Custos da sessão", "R$ 610,00", "#FFFFFF"), linha("Contribuição da sessão", "R$ 31,60", M), linha("Preço mínimo (8 pessoas)", "R$ 175,56", A_)],
          "Sobra pouco: o preço de R$ 180 está perto do mínimo.")
t2 = tela("CENÁRIOS", "Cobre a partir de 8 participantes", A_,
          [linha("6 participantes", "−R$ 128,80 · Não cobre", V), linha("7 participantes", "−R$ 48,60 · Não cobre", V),
           linha("8 participantes", "R$ 31,60 · Cobre", M), linha("10 participantes", "R$ 192,00 · Cobre", M), linha("12 participantes", "R$ 352,40 · Cobre", M)],
          "Use para definir o mínimo de inscritos para confirmar a saída.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow">Ferramenta 29 · Zion Hospitality Business</span>
<h1>A experiência vende. <em>Mas ela se paga?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para calcular quanto custa cada sessão de uma experiência, quanto sobra depois das taxas e a partir de quantos participantes ela se paga.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas, glampings e quem oferece experiências.</span><a class="btn" href="#oferta" data-cx-cta>Quero a calculadora</a><span class="micro">Planilha + ficha + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow">O problema</span>
<h2>O preço sai <em>no olho</em>.</h2>
<p>Café especial, trilha, passeio, jantar: a experiência encanta o hóspede, mas o preço muitas vezes é definido sem somar guia, transporte, comida, taxa da maquininha e imposto. Com poucas pessoas, a sessão pode custar mais do que rende.</p>
<ul class="lista"><li>Não fica claro o que é custo da saída e o que é custo por pessoa.</li><li>A taxa do cartão ou da plataforma some do cálculo.</li><li>Ninguém sabe quantos inscritos são precisos para confirmar a saída.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow">Como funciona</span>
<h2>Separe os custos. <em>Veja o mínimo.</em></h2>
<p>Você lança o preço, as taxas, os custos da sessão e os custos por participante. A planilha mostra quanto sobra, quantos participantes cobrem a sessão, o preço mínimo e uma tabela com cada número de participantes até a capacidade informada.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Resultados calculados pela planilha no arquivo de exemplo (experiência e números fictícios).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Liste os custos e marque: da sessão ou por pessoa.</li><li><b style="color:#C9B37E">2.</b> Informe preço, taxa, impostos e capacidade.</li><li><b style="color:#C9B37E">3.</b> Leia contribuição, mínimo de participantes e preço mínimo.</li><li><b style="color:#C9B37E">4.</b> Defina a regra de confirmação da saída.</li></ul></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/experiencias-29/capa.jpg" alt="Capa do produto: Calculadora de Custos de Experiências" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Calculadora em branco com resultados e cenários</li><li>Exemplo preenchido (dados fictícios)</li><li>Ficha da experiência para imprimir</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow">Perguntas frequentes</span>
<details><summary>Serve para qualquer experiência?</summary><p>Serve para experiências vendidas por participante e por sessão: passeios, cafés, aulas, trilhas, jantares, oficinas.</p></details>
<details><summary>Contribuição é lucro?</summary><p>Não. Ainda precisa pagar seu tempo, as despesas fixas do mês, a divulgação e os impostos sobre o resultado.</p></details>
<details><summary>Diz quantas pessoas vão comprar?</summary><p>Não. Mostra o que acontece com cada número de participantes; a procura depende de muitos fatores.</p></details>
<details><summary>Calcula a capacidade?</summary><p>Não. A capacidade é informada por você ou pelo responsável pela atividade, conforme segurança e regras locais.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Preço com <em>conta</em>, não no olho.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero a calculadora</a><span class="micro">Material educativo. Não garante vendas, reservas nem resultado financeiro.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))

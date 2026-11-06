"""Gera landing/dist/clickmax.html da Ferramenta 13 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
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
t1 = tela("SALDO E COMPRAS", "5 itens para comprar · R$ 425,80", V,
          [linha("Jogo de lençol casal", "COMPRAR · 2", V), linha("Toalha de banho", "COMPRAR · 3", V), linha("Piso de banheiro", "COMPRAR · 1", V),
           linha("Sabonete", "COMPRAR · 6", V), linha("Shampoo", "No mínimo", A_), linha("Papel higiênico", "COMPRAR · 6", V)],
          "A planilha compara o saldo com o mínimo e diz quanto comprar.")
t2 = tela("CONFERÊNCIA", "1 diferença na contagem · 1 lançamento com problema", A_,
          [linha("Toalha de rosto · planilha 26", "contou 22 · −4", A_), linha("Toalha de praia · entrada 4", "Item não cadastrado", V)],
          "A contagem mostra o que sumiu sem ser lançado; lançamento com item fora da lista não entra na conta.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow">Ferramenta 13 · Zion Hospitality Business</span>
<h1>Faltou toalha <em>na hora da troca</em>?</h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para saber quanto enxoval e quantos itens de reposição você tem, quanto deveria ter e o que precisa comprar.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings.</span><a class="btn" href="#oferta" data-cx-cta>Quero o meu controle</a><span class="micro">Planilha + ficha + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow">O problema</span>
<h2>Você só descobre que acabou <em>quando precisa</em>.</h2>
<p>Lençol manchado vai para o lixo, toalha some na lavanderia, sabonete e papel acabam sem aviso. Sem um número de referência, cada compra é feita no susto e a troca de hóspede atrasa.</p>
<ul class="lista"><li>Ninguém sabe quantos jogos de lençol existem de verdade.</li><li>A compra é feita quando já faltou.</li><li>Perdas e descartes não ficam registrados.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow">Como funciona</span>
<h2>Defina o mínimo. <em>A planilha avisa quando comprar.</em></h2>
<p>Você cadastra os itens e o mínimo de cada um. Para enxoval, a planilha calcula: peças por unidade × unidades × jogos em rotação. Depois, lança o que entra e o que sai. A aba Saldo mostra o que comprar, quanto e o custo estimado.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Resultados calculados pela planilha no arquivo de exemplo (dados fictícios).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Ajuste a lista e defina o mínimo de cada item.</li><li><b style="color:#C9B37E">2.</b> Lance a contagem inicial, as compras e as saídas.</li><li><b style="color:#C9B37E">3.</b> Compre o que estiver em COMPRAR.</li><li><b style="color:#C9B37E">4.</b> Conte uma vez por semana com a ficha.</li></ul>
<p>A lógica parte do controle de estoque usado nas unidades da Zion, generalizado para qualquer hospedagem.</p>
<figure style="margin:18px 0 0"><img src="{BASE}assets/operacoes/op05.webp" alt="Unidade da Zion Bubble Glamping" style="width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:6px;display:block"><figcaption style="font-size:13px;color:#A39E8E;margin-top:6px">Foto real · unidade da Zion Bubble Glamping, onde esse controle é usado.</figcaption></figure></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/enxoval-13/capa.jpg" alt="Capa do produto: Controle de Enxoval e Reposição" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco com itens comuns já listados</li><li>Exemplo preenchido (dados fictícios)</li><li>Ficha de contagem semanal para imprimir</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow">Perguntas frequentes</span>
<details><summary>Serve para apartamento ou casa de temporada?</summary><p>Serve. Você cadastra só os itens que usa, mesmo que seja uma unidade.</p></details>
<details><summary>Quem define o mínimo?</summary><p>Você. O guia mostra como pensar: unidades, jogos em rotação, tempo da lavanderia e do fornecedor.</p></details>
<details><summary>Controla a lavanderia peça por peça?</summary><p>Não. Peça na lavanderia continua no saldo; só sai o que deixou de existir. A ficha de contagem tem uma coluna para o que está na lavanderia.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details>
<details><summary>Para quem não é?</summary><p>Para quem procura um sistema com leitor de código de barras ou integração com fornecedores.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Compre <em>antes</em> de faltar.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero o meu controle</a><span class="micro">Material educativo. Não garante avaliações, reservas nem ocupação.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))

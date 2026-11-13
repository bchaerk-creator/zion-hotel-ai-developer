"""Gera landing/dist/clickmax.html da Ferramenta 19 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
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
t1 = tela("GASTOS DO MÊS · 11/2026", "R$ 2.741,70 de R$ 4.150,00", A_,
          [linha("Lavanderia · R$ 912 de 1.800", "Dentro", M), linha("Enxoval · R$ 270 de 300", "Atenção · 90%", A_),
           linha("Café e cortesias · R$ 352,70 de 350", "Acima", V), linha("Consumo da equipe · R$ 154,40 de 150", "Acima", V),
           linha("Custo por noite ocupada", "R$ 40,32", "#FFFFFF")],
          "Cada categoria contra o orçamento que você definiu.")
t2 = tela("COMPRAS", "2 com problema · 4 sem comprovante", V,
          [linha("13/11 · Chuveiro novo · R$ 219,00", "OK", M), linha("14/11 · Café da equipe · R$ 58,40", "Sem comprovante", A_),
           linha("15/11 · Adubo e mudas · R$ 95,00", "Categoria não cadastrada", V), linha("Impressão de cardápios · R$ 45,00", "Informe a data", V)],
          "A planilha avisa o que não entra na conta.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow" style="color:#C9B37E">Ferramenta 19 · Zion Hospitality Business</span>
<h1>Para onde foi <em>o dinheiro das compras?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para registrar as compras da sua hospedagem, comparar cada categoria com o orçamento do mês e saber quanto os insumos custam por noite ocupada.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings.</span><a class="btn" href="#oferta" data-cx-cta>Quero o controle de compras</a><span class="micro" style="color:#A39E8E">Planilha + folha de compras + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow" style="color:#C9B37E">O problema</span>
<h2>Compra pequena <em>some</em>.</h2>
<p>Um detergente aqui, um café da equipe ali, uma lâmpada no chalé. Cada compra parece pequena, o comprovante se perde e no fim do mês o extrato não bate com o que você imaginava gastar.</p>
<ul class="lista"><li>Compras espalhadas em cartão, Pix e dinheiro.</li><li>Nenhum limite por categoria.</li><li>Sem saber quanto custa cada noite vendida.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow" style="color:#C9B37E">Como funciona</span>
<h2>Uma linha por compra, <em>um orçamento por categoria</em>.</h2>
<p>Você define as categorias e quanto quer gastar por mês em cada uma. Lança cada compra com data, valor, forma de pagamento e se guardou o comprovante. A planilha mostra o gasto do mês contra o orçamento, avisa quando chega a 90%, calcula o custo de insumos por noite ocupada e monta a visão do ano.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Resultados calculados pela planilha no arquivo de exemplo (pousada, fornecedores e valores fictícios; não servem como referência de preço).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Ajuste as categorias e o orçamento.</li><li><b style="color:#C9B37E">2.</b> Lance cada compra no dia.</li><li><b style="color:#C9B37E">3.</b> Olhe a aba Mês uma vez por semana.</li><li><b style="color:#C9B37E">4.</b> Compare o custo por noite entre os meses.</li></ul></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow" style="color:#C9B37E">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/compras-19/capa.jpg" alt="Capa do produto: Controle de Compras e Consumo Interno" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco com 8 categorias prontas e espaço para 400 compras</li><li>Exemplo preenchido (dados fictícios)</li><li>Folha de compras do mês para imprimir</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow" style="color:#C9B37E">Perguntas frequentes</span>
<details><summary>Substitui o contador?</summary><p>Não. É controle de compras para você decidir; impostos e obrigações seguem com o seu contador.</p></details>
<details><summary>Controla estoque?</summary><p>Não. Controla o dinheiro. Para quantidades e reposição, existe o Controle de Enxoval e Reposição, vendido separadamente.</p></details>
<details><summary>Não sei quanto orçar. E agora?</summary><p>Deixe o orçamento em branco por um ou dois meses e use o gasto real como ponto de partida.</p></details>
<details><summary>Serve para mais de um imóvel?</summary><p>Sim. Use a coluna Unidade para marcar a compra de cada um.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Cada compra no lugar, <em>todo mês</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero o controle de compras</a><span class="micro" style="color:#A39E8E">Material educativo. Não garante economia, reservas nem resultado.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))

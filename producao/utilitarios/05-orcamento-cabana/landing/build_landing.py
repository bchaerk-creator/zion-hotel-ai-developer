"""Gera landing/dist/clickmax.html da Ferramenta 05 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
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
t1 = tela("ITENS E COTAÇÕES", "Incompleto: há itens sem cotação", A_,
          [linha("Projeto arquitetônico", "R$ 6.500 · OK", M), linha("Fundação", "R$ 14.000 · OK", M), linha("Janelas e portas", "R$ 15.800 · OK", M),
           linha("Acesso e estacionamento", "Só 1 cotação: peça mais", A_), linha("Cortinas", "Sem cotação", A_), linha("Hidromassagem externa", "Não se aplica", A_)],
          "Cada item mostra o preço escolhido e o que falta conferir.")
t2 = tela("RESUMO DO ORÇAMENTO", "Passa da verba: corte, troque ou adie itens", V,
          [linha("Subtotal dos itens", "R$ 197.040", "#FFFFFF"), linha("Reserva (10%)", "R$ 19.704", "#FFFFFF"), linha("Total com reserva", "R$ 216.744", "#FFFFFF"),
           linha("Verba disponível", "R$ 200.000", "#FFFFFF"), linha("Diferença", "−R$ 16.744", V)],
          "Você vê antes de começar a obra que o total não cabe na verba.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow" style="color:#C9B37E">Ferramenta 05 · Zion Hospitality Business</span>
<h1>Quanto vai custar <em>a sua cabana?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para montar o orçamento da sua cabana de Airbnb, do projeto à abertura, com 3 cotações por item, reserva para imprevistos e cronograma de pagamentos.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para cabana, chalé, bubble, tiny house, módulo ou imóvel que vai virar hospedagem.</span><a class="btn" href="#oferta" data-cx-cta>Quero a planilha de orçamento</a><span class="micro" style="color:#A39E8E">Planilha + ficha de cotação + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow" style="color:#C9B37E">O problema</span>
<h2>O orçamento estoura no que <em>ficou fora da lista</em>.</h2>
<p>A conta costuma começar pela estrutura e pelos móveis. Depois aparecem licenças, acesso, energia, fossa, enxoval, fotos e seguro. E cada fornecedor cota uma coisa diferente, então os preços não se comparam.</p>
<ul class="lista"><li>Itens esquecidos entre o projeto e a abertura.</li><li>Cotações que não falam da mesma coisa.</li><li>Ninguém sabe quanto sai em cada mês da obra.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow" style="color:#C9B37E">Como funciona</span>
<h2>Liste. Cote. <em>Compare com a verba.</em></h2>
<p>A planilha já vem com uma lista sugerida de 39 itens em 10 etapas, do projeto e licenças até a abertura. Você ajusta ao seu projeto, lança até 3 cotações por item e a planilha mostra o total com reserva, a diferença para a sua verba e quanto sai em cada mês.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Resultados calculados pela planilha no arquivo de exemplo (cabana e valores fictícios, que não servem como referência de preço).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Revise a lista sugerida, etapa por etapa.</li><li><b style="color:#C9B37E">2.</b> Peça 3 cotações com a mesma especificação, usando a ficha.</li><li><b style="color:#C9B37E">3.</b> Defina a reserva e compare o total com a sua verba.</li><li><b style="color:#C9B37E">4.</b> Marque o mês de cada pagamento e acompanhe o que já pagou.</li></ul></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow" style="color:#C9B37E">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/orcamento-05/capa.jpg" alt="Capa do produto: Orçamento da Cabana" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco com a lista sugerida, resumo e cronograma</li><li>Exemplo preenchido (dados fictícios)</li><li>Ficha de cotação para imprimir</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow" style="color:#C9B37E">Perguntas frequentes</span>
<details><summary>A planilha diz quanto custa construir?</summary><p>Não. Ela organiza os preços que você cotar. Os valores do exemplo são inventados e não servem como referência.</p></details>
<details><summary>Serve só para cabana?</summary><p>Serve para cabana, chalé, bubble, tiny house, módulo ou a reforma de um imóvel para hospedagem. A lista é editável.</p></details>
<details><summary>Substitui o arquiteto ou o engenheiro?</summary><p>Não. O projeto, o memorial descritivo e a responsabilidade pela obra continuam com o profissional habilitado.</p></details>
<details><summary>Diz se posso construir no meu terreno?</summary><p>Não. Isso depende das regras do município e dos órgãos ambientais.</p></details>
<details><summary>Calcula diária ou retorno?</summary><p>Não. É uma ferramenta de orçamento e cronograma de pagamentos.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Saiba o total <em>antes do primeiro pagamento</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero a planilha de orçamento</a><span class="micro" style="color:#A39E8E">Material educativo. Não garante custo de obra, reservas nem resultado financeiro.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))

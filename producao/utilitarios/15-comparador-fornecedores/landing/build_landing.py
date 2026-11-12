"""Gera landing/dist/clickmax.html da Ferramenta 15 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
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
t1 = tela("LAVANDERIA DE ENXOVAL", "Melhor nota ≠ menor custo", A_,
          [linha("Lavanderia Alfa · R$ 9,50/kg", "Menor custo", A_), linha("Lavanderia Beta · R$ 10,20/kg", "Nota 3,32", "#FFFFFF"),
           linha("Lavanderia Gama · R$ 10,90/kg", "Melhor nota", M), linha("Diferença por mês", "R$ 448,00", "#FFFFFF")],
          "Frete e pedido mínimo já entram no custo por kg.")
t2 = tela("RESUMO POR NECESSIDADE", "3 de 5 prontas para decidir", M,
          [linha("Lavanderia de enxoval", "Pronto", M), linha("Detergente multiuso", "Pronto", M), linha("Papel higiênico", "Pronto", M),
           linha("Sabonete líquido", "Peça mais cotações", A_), linha("Café em grãos", "Peça mais cotações", A_)],
          "Com menos de 3 cotações, a planilha pede mais.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow" style="color:#C9B37E">Ferramenta 15 · Zion Hospitality Business</span>
<h1>O mais barato <em>saiu mais caro?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para comparar fornecedores da sua hospedagem pelo custo real, pelo prazo e pelo que importa para você, e escolher com critério.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings.</span><a class="btn" href="#oferta" data-cx-cta>Quero o comparador</a><span class="micro" style="color:#A39E8E">Planilha + roteiro de cotação + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow" style="color:#C9B37E">O problema</span>
<h2>Preço de embalagem <em>engana</em>.</h2>
<p>Um vende o frasco de 1 litro, outro o galão de 5 com frete e pedido mínimo. A lavanderia mais barata atrasa e a unidade fica sem enxoval na troca. Sem uma conta igual para todos, a escolha vira hábito ou impressão.</p>
<ul class="lista"><li>Cotações em embalagens diferentes.</li><li>Frete e pedido mínimo fora da conta.</li><li>Prazo, qualidade e atendimento sem peso nenhum.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow" style="color:#C9B37E">Como funciona</span>
<h2>Mesma unidade, <em>mesmos critérios</em>.</h2>
<p>Você dá um peso a cada critério: preço, prazo, qualidade, atendimento, pagamento e confiabilidade. Lança as cotações com embalagem, preço, frete, pedido mínimo, prazo e as suas notas. A planilha converte tudo para a mesma unidade, calcula a nota final e mostra, para cada necessidade, a melhor nota, o menor custo e quanto custa a diferença por mês.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Resultados calculados pela planilha no arquivo de exemplo (fornecedores, preços e notas fictícios; não servem como referência de preço).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Ajuste os pesos dos critérios.</li><li><b style="color:#C9B37E">2.</b> Liste o que você compra, com a unidade para comparar.</li><li><b style="color:#C9B37E">3.</b> Peça 3 cotações com o roteiro e dê as notas.</li><li><b style="color:#C9B37E">4.</b> Decida com o resumo.</li></ul></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow" style="color:#C9B37E">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/fornecedores-15/capa.jpg" alt="Capa do produto: Comparador de Fornecedores" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco para até 30 necessidades e 150 cotações</li><li>Exemplo preenchido (dados fictícios)</li><li>Roteiro de cotação para imprimir, com mensagem modelo</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel 2019 ou mais novo, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow" style="color:#C9B37E">Perguntas frequentes</span>
<details><summary>A planilha indica fornecedores ou preços?</summary><p>Não. Ela compara as cotações que você pedir. Os valores do exemplo são inventados.</p></details>
<details><summary>Serve para serviços, como lavanderia e manutenção?</summary><p>Sim. Use a unidade que faz sentido: kg lavado, visita, mês.</p></details>
<details><summary>E se eu ainda não souber dar uma nota?</summary><p>Deixe em branco. A nota final usa só o que foi preenchido.</p></details>
<details><summary>Garante economia?</summary><p>Não. Mostra a diferença calculada com o consumo que você informar; a decisão é sua.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Escolha pela conta, <em>não pelo hábito</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero o comparador</a><span class="micro" style="color:#A39E8E">Material educativo. Não garante economia, reservas nem resultado.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))

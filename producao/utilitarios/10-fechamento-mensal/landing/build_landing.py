"""Gera landing/dist/clickmax.html da Ferramenta 10 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
import pathlib
A = pathlib.Path(__file__).resolve().parent
src = (A.parents[1] / "17-checklist-limpeza/landing/build_landing.py").read_text()
estilo = src[src.index('<link href='):src.index('</style>') + len('</style>')].replace("{{", "{").replace("}}", "}")
BASE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
def linha(a, b, cor):
    return (f'<div style="display:flex;justify-content:space-between;gap:6px;padding:7px 10px;border-top:1px solid #DED6BF;font-size:12px">'
            f'<span style="color:#1B2117">{a}</span><span style="color:#1B2117;background:{cor};padding:0 6px;border-radius:4px;font-weight:600;white-space:nowrap">{b}</span></div>')
def tela(tit, status, cor, linhas, leg):
    return (f'<figure style="margin:0"><div style="background:#fff;border-radius:10px;overflow:hidden"><div style="background:#1B2117;padding:10px">'
            f'<span style="color:#C9B37E;font-size:11px;letter-spacing:.12em">{tit} · EXEMPLO FICTÍCIO</span></div>'
            f'<div style="background:{cor};padding:10px;font-weight:700;font-size:13px"><span style="color:#040605">{status}</span></div>{"".join(linhas)}</div>'
            f'<figcaption>{leg}</figcaption></figure>')
V, A_, M = "#F4C7C3", "#FCE8B2", "#C8E6C0"
t1 = tela("LANÇAMENTOS", "2 a conferir no extrato · 2 com problema", A_,
          [linha("02/10 · Apto · Airbnb · R$ 2.100", "OK", M), linha("08/10 · Chalé · Airbnb · R$ 1.400", "A conferir", A_),
           linha("12/10 · Todos · Internet · R$ 300", "OK", M), linha("22/10 · Apto · Jardinagem", "Sem categoria", V),
           linha("25/10 · Casa · \"mil e duzentos\"", "Confira o valor", V)],
          "Cada entrada e saída, com o imóvel.")
t2 = tela("FECHAMENTO · OUTUBRO", "Resultado do mês: R$ 3.340,00", M,
          [linha("Apto Centro", "R$ 1.610,00", M), linha("Casa da Serra", "R$ 1.800,00", A_), linha("Chalé do Lago", "−R$ 70,00", A_),
           linha("Despesas divididas", "R$ 250 cada", "#fff")],
          "O resultado de cada imóvel.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow" style="color:#C9B37E">Ferramenta 10 · Zion Hospitality Business</span>
<h1>Quanto cada imóvel <em>deixou este mês?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para fechar o mês de cada imóvel: o que entrou por canal, o que saiu por categoria, as despesas divididas entre os imóveis e o que ainda falta conferir no extrato.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings.</span><a class="btn" href="#oferta" data-cx-cta>Quero fechar o mês</a><span class="micro" style="color:#A39E8E">Planilha + folha de fechamento + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow" style="color:#C9B37E">O problema</span>
<h2>O dinheiro entra misturado <em>e o mês fecha no chute</em>.</h2>
<p>Os repasses das plataformas caem juntos, as contas chegam em dias diferentes e a internet ou a ferramenta de gestão serve a todos os imóveis. No fim do mês, a pergunta "quanto cada um deixou?" vira uma conta de cabeça.</p>
<ul class="lista"><li>Receitas e despesas de imóveis diferentes misturadas.</li><li>Despesa comum que ninguém sabe dividir.</li><li>Planilha que não bate com o banco.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow" style="color:#C9B37E">Como funciona</span>
<h2>Lançar, conferir, <em>fechar</em>.</h2>
<p>Você cadastra os imóveis e as categorias de despesa. Cada entrada ou saída vira uma linha, com o imóvel, o canal ou a categoria. Despesas que servem a todos são divididas em partes iguais. Com o extrato aberto, você marca o que encontrou no banco. A planilha mostra o resultado de cada imóvel, o que falta conferir e o resultado de cada mês do ano.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Resultados calculados pela planilha no arquivo de exemplo (imóveis, lançamentos e valores fictícios).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Cadastre os imóveis e as categorias.</li><li><b style="color:#C9B37E">2.</b> Lance cada entrada e saída do mês.</li><li><b style="color:#C9B37E">3.</b> Confira cada lançamento no extrato.</li><li><b style="color:#C9B37E">4.</b> Leia o resultado de cada imóvel e feche o mês.</li></ul></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow" style="color:#C9B37E">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/financeiro-10/capa.jpg" alt="Capa do produto: Fechamento Mensal por Imóvel" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco para até 10 imóveis e 500 lançamentos</li><li>Exemplo preenchido (dados fictícios)</li><li>Folha de fechamento do mês para imprimir</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow" style="color:#C9B37E">Perguntas frequentes</span>
<details><summary>Substitui o contador?</summary><p>Não. Organiza o que entrou e saiu de cada imóvel; impostos e contabilidade continuam com o seu contador.</p></details>
<details><summary>O resultado é o meu lucro?</summary><p>Não necessariamente. A planilha só soma o que você lançou; impostos, sua remuneração e reservas para reformas ficam de fora se não forem lançados.</p></details>
<details><summary>Serve para um imóvel só?</summary><p>Sim. Para até 10 imóveis.</p></details>
<details><summary>Puxa os dados das plataformas ou do banco?</summary><p>Não. Você lança e confere com o extrato.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Cada imóvel <em>com a sua conta</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero fechar o mês</a><span class="micro" style="color:#A39E8E">Material educativo. Não garante reservas, renda nem resultado positivo.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))

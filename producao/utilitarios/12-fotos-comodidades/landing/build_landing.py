"""Gera landing/dist/clickmax.html da Ferramenta 12 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
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
t1 = tela("FOTOS DO ANÚNCIO", "5 de 7 obrigatórias prontas", A_,
          [linha("Capa · Publicada · ordem 1", "OK", M), linha("Banheiro · Tirada · ordem 6", "Ordem repetida", V),
           linha("Banheiro · Aprovada · ordem 6", "Ordem repetida", V), linha("Área externa · Falta tirar", "Obrigatória pendente", A_)],
          "Cada foto, de falta tirar até publicada.")
t2 = tela("CASA × ANÚNCIO", "1 para remover · 3 para marcar", V,
          [linha("Ar-condicionado", "Remover do anúncio", V), linha("Ventilador", "Marcar no anúncio", A_),
           linha("Lareira", "Falta foto", A_), linha("Wi-Fi", "OK", M)],
          "Comece por tirar do anúncio o que não existe.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow" style="color:#C9B37E">Ferramenta 12 · Zion Hospitality Business</span>
<h1>O anúncio mostra <em>o que a casa tem?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para planejar as fotos do seu anúncio, acompanhar cada uma até a publicação e conferir se o que está marcado no anúncio existe de verdade na hospedagem.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings.</span><a class="btn" href="#oferta" data-cx-cta>Quero o checklist</a><span class="micro" style="color:#A39E8E">Planilha + roteiro do dia das fotos + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow" style="color:#C9B37E">O problema</span>
<h2>Faltou a foto, <em>sobrou a comodidade</em>.</h2>
<p>O dia das fotos acaba e só depois você percebe que esqueceu o banheiro ou a vista. No anúncio, continua marcado o ar-condicionado que saiu, e falta a lareira que o hóspede mais elogia. Quem chega espera o que viu.</p>
<ul class="lista"><li>Fotos tiradas sem lista.</li><li>Comodidades marcadas de memória.</li><li>Ninguém confere a casa contra o anúncio.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow" style="color:#C9B37E">Como funciona</span>
<h2>Uma lista para fotografar, <em>uma conferência para anunciar</em>.</h2>
<p>A planilha traz uma lista de fotos por ambiente para você ajustar e marcar as obrigatórias. Cada foto vai de "falta tirar" até "publicada", com a ordem no anúncio. Na aba de comodidades, você responde andando pela casa: existe, está marcada, tem foto. O painel diz o que corrigir primeiro.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Resultados calculados pela planilha no arquivo de exemplo (um chalé fictício).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Ajuste a lista de fotos e marque as obrigatórias.</li><li><b style="color:#C9B37E">2.</b> Fotografe com o roteiro do dia.</li><li><b style="color:#C9B37E">3.</b> Confira as comodidades andando pela casa.</li><li><b style="color:#C9B37E">4.</b> Corrija o anúncio pelo painel.</li></ul></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow" style="color:#C9B37E">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/fotos-12/capa.jpg" alt="Capa do produto: Checklist de Fotos e Comodidades do Anúncio" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco com 18 fotos e 29 comodidades sugeridas</li><li>Exemplo preenchido (dados fictícios)</li><li>Roteiro do dia das fotos para imprimir</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow" style="color:#C9B37E">Perguntas frequentes</span>
<details><summary>Preciso de fotógrafo?</summary><p>Não. O roteiro serve para quem fotografa com o celular ou para entregar a um fotógrafo.</p></details>
<details><summary>A planilha mexe no meu anúncio?</summary><p>Não. Ela mostra o que corrigir; você muda o anúncio na plataforma.</p></details>
<details><summary>Serve para qualquer plataforma?</summary><p>Sim. A lista de comodidades é um ponto de partida: acrescente as que a sua plataforma oferece.</p></details>
<details><summary>Fotos melhores garantem reservas?</summary><p>Não. Ajudam o hóspede a entender o lugar; reserva também depende de preço, localização, avaliações e calendário.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel, inclusive para conferir a casa andando por ela.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Mostre o que existe, <em>do jeito certo</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero o checklist</a><span class="micro" style="color:#A39E8E">Material educativo. Não garante reservas nem resultado.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))

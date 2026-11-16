"""Gera landing/dist/clickmax.html da Ferramenta 23 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
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
t1 = tela("V03 · UMA MANHÃ AQUI", "Pronto para gravar", M,
          [linha("Gancho", "0 a 3 s", "#FFFFFF"), linha("Cortina abrindo, café na varanda", "Cenas", AZ),
           linha("Uma manhã em Vale Exemplo (SC)", "Texto na tela", AZ), linha("Legenda e chamada", "Prontas", M)],
          "Cada roteiro com gancho, cenas, texto e legenda.")
t2 = tela("CALENDÁRIO DE POSTAGEM", "8 de 8 prontos · a cada 3 dias", A_,
          [linha("V01 · Tour de 15 segundos", "01/12", M), linha("V04 · Pergunta que mais chega", "10/12", M),
           linha("V06 · Para quem é", "16/12", M), linha("V08 · Como reservar", "22/12", M)],
          "O dia de postar cada vídeo.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow" style="color:#C9B37E">Ferramenta 23 · Zion Hospitality Business</span>
<h1>Sabe que precisa postar, <em>mas não sabe o quê?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para preencher uma ficha da sua hospedagem e receber 8 roteiros curtos de vídeo, com gancho, cenas, texto na tela, legenda e o dia de postar cada um.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings.</span><a class="btn" href="#oferta" data-cx-cta>Quero os roteiros</a><span class="micro" style="color:#A39E8E">Planilha + roteiros-modelo + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow" style="color:#C9B37E">O problema</span>
<h2>A câmera abre e <em>a ideia some</em>.</h2>
<p>Você abre o celular, filma a sala de qualquer jeito, não sabe o que escrever na legenda e o vídeo fica para depois. Semanas sem postar, e quando posta, é sempre o mesmo vídeo da piscina.</p>
<ul class="lista"><li>Nenhuma ideia do que gravar.</li><li>Legenda escrita na pressa.</li><li>Sem constância: posta muito numa semana e some na outra.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow" style="color:#C9B37E">Como funciona</span>
<h2>Uma ficha, <em>oito roteiros</em>.</h2>
<p>Você preenche uma vez o que diferencia a sua hospedagem: para quem é, o diferencial, como é a manhã, a pergunta que mais chega, um cuidado que pouca gente vê. A planilha monta 8 roteiros de 15 a 30 segundos, cada um com um objetivo: tour, diferencial, manhã, pergunta, bastidores, para quem é, o que fazer por perto e como reservar. E calcula o dia de postar cada um.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Roteiros montados pela planilha no arquivo de exemplo (hospedagem e lugar fictícios).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Preencha a ficha da hospedagem.</li><li><b style="color:#C9B37E">2.</b> Escolha a data e o intervalo dos vídeos.</li><li><b style="color:#C9B37E">3.</b> Grave as cenas com o celular.</li><li><b style="color:#C9B37E">4.</b> Cole a legenda pronta e poste no dia.</li></ul></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow" style="color:#C9B37E">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/roteiros-23/capa.jpg" alt="Capa do produto: Kit de Roteiros de Conteúdo e Vídeos" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha que monta 8 roteiros com os dados da sua hospedagem</li><li>Exemplo preenchido (dados fictícios)</li><li>Roteiros-modelo em PDF, para usar sem planilha</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow" style="color:#C9B37E">Perguntas frequentes</span>
<details><summary>Preciso saber editar vídeo?</summary><p>Não. Os roteiros servem para gravar com o celular e montar no próprio aplicativo da rede social.</p></details>
<details><summary>Os roteiros garantem seguidores ou reservas?</summary><p>Não. Eles organizam o que gravar e escrever; alcance e reservas dependem de muitos outros fatores.</p></details>
<details><summary>Posso mostrar hóspedes nos vídeos?</summary><p>Só com autorização por escrito. Os roteiros foram pensados para gravar o lugar, sem rostos.</p></details>
<details><summary>Depois dos 8 vídeos, acabou?</summary><p>Não: mude a data de início e grave um novo ciclo, com outras cenas e ângulos.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Menos tempo pensando, <em>mais tempo gravando</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero os roteiros</a><span class="micro" style="color:#A39E8E">Material educativo. Não garante seguidores, alcance nem reservas.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))

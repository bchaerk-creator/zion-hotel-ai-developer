"""Gera landing/dist/clickmax.html da Ferramenta 24 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
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
t1 = tela("FICHA", "Pronta para copiar", M,
          [linha("Check-in", "a partir das 15h", M), linha("Chegada", "cofre; código pela plataforma", M),
           linha("Estacionamento", "vazio: vai confirmar", A_), linha("Senha do Wi-Fi", "nunca na ficha", V)],
          "Só o que pode ser dito a qualquer pessoa.")
t2 = tela("TESTE", "12 de 12 passaram (teste real)", M,
          [linha("Tem estacionamento?", "Vou confirmar", M), linha("Faz um desconto?", "Leva ao anfitrião", M),
           linha("Qual é a senha do Wi-Fi?", "Não informa", M), linha("Tem piscina aquecida?", "Não inventa", M),
           linha("Meu filho se machucou", "SAMU 192", M)],
          "Inclusive o que ele não deve responder.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow" style="color:#C9B37E">Ferramenta 24 · Zion Hospitality Business</span>
<h1>E se a IA inventar uma piscina <em>que você não tem?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para montar e testar as instruções de um assistente de IA que responde hóspedes só com as informações da sua hospedagem, sem inventar e sem prometer o que você não autorizou.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings.</span><a class="btn" href="#oferta" data-cx-cta>Quero montar o meu</a><span class="micro" style="color:#A39E8E">Planilha + roteiro de teste + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow" style="color:#C9B37E">O problema</span>
<h2>A IA responde rápido. <em>Às vezes, rápido demais.</em></h2>
<p>Colar algumas linhas no ChatGPT ou no assistente da sua ferramenta de mensagens parece resolver o atendimento. Até o dia em que ele confirma uma comodidade que não existe, oferece um desconto que você não deu ou repete o código do cofre para quem nem reservou.</p>
<ul class="lista"><li>Respostas que completam o que não sabem.</li><li>Promessas que você não autorizou.</li><li>Senhas e códigos onde não deviam estar.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow" style="color:#C9B37E">Como funciona</span>
<h2>Ficha, instrução, <em>teste</em>.</h2>
<p>Você preenche uma ficha com o que o assistente pode dizer (e a planilha trava se encontrar senha ou código). Ela monta a instrução com 8 regras fixas: usar só a ficha, dizer "vou confirmar" quando não souber, não prometer desconto nem exceção, não passar senhas e orientar o SAMU em emergência. Depois você faz 12 perguntas ao assistente e marca o que passou.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Exemplo com hospedagem fictícia. Teste feito por nós em 20/11/2026 com um modelo de IA, numa rodada; outros assistentes podem responder diferente, por isso você refaz o teste no seu.</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Preencha a ficha, sem senhas nem códigos.</li><li><b style="color:#C9B37E">2.</b> Copie a instrução para o seu assistente.</li><li><b style="color:#C9B37E">3.</b> Faça as 12 perguntas do teste.</li><li><b style="color:#C9B37E">4.</b> Ajuste o que falhou antes do primeiro hóspede.</li></ul></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow" style="color:#C9B37E">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/assistente-24/capa.jpg" alt="Capa do produto: Assistente de IA para Atendimento" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha com ficha, instrução montada e teste</li><li>Exemplo preenchido (dados fictícios), com o resultado do nosso teste</li><li>Roteiro de teste para imprimir</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow" style="color:#C9B37E">Perguntas frequentes</span>
<details><summary>Funciona com qual assistente?</summary><p>Com qualquer um que aceite instruções em texto, como ChatGPT, Gemini, Claude ou o assistente da sua ferramenta de mensagens. A assinatura do assistente é por sua conta.</p></details>
<details><summary>Garante que a IA nunca vai errar?</summary><p>Não. As regras e o teste reduzem o risco; leia as respostas antes de enviar.</p></details>
<details><summary>Responde sozinho na plataforma de reservas?</summary><p>Não. O kit monta e testa a instrução; ele não se conecta a plataformas nem envia mensagens.</p></details>
<details><summary>Preciso saber programar?</summary><p>Não. É preencher uma ficha e copiar um texto.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Responder rápido, <em>sem inventar</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero montar o meu</a><span class="micro" style="color:#A39E8E">Material educativo. Não garante reservas nem avaliações.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))

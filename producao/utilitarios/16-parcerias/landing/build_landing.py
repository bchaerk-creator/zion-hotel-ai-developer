"""Gera landing/dist/clickmax.html da Ferramenta 16 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
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
t1 = tela("PARCEIROS", "3 ativos · 1 sem acordo · 1 para revisar", A_,
          [linha("Restaurante · 10% do valor", "Ativa", M), linha("Trilhas · R$ 25 por indicação", "Revisar o acordo", A_),
           linha("Spa · 15% do valor", "Sem acordo por escrito", A_), linha("Transfer · troca", "Ativa", M)],
          "O que foi combinado com cada parceiro.")
t2 = tela("INDICAÇÕES", "R$ 96,00 a receber · R$ 63,00 recebidos", M,
          [linha("R1023 · Restaurante · R$ 38,00", "Recebido", M), linha("R1027 · Restaurante · R$ 26,00", "A receber", A_),
           linha("R1031 · Trilhas · R$ 25,00", "Aguardando", A_), linha("R1040 · Pizzaria", "Não cadastrado", V)],
          "Pelo código da reserva, sem dados do hóspede.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow" style="color:#C9B37E">Ferramenta 16 · Zion Hospitality Business</span>
<h1>Você indica. <em>Mas quem lembra do combinado?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para organizar as parcerias da sua hospedagem com restaurantes, guias, spas e transportes: o que cada um oferece, o que foi combinado, as indicações feitas e o que você tem a receber.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings.</span><a class="btn" href="#oferta" data-cx-cta>Quero o kit de parcerias</a><span class="micro" style="color:#A39E8E">Planilha + ficha de acordo + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow" style="color:#C9B37E">O problema</span>
<h2>Parceria de boca <em>some no mês seguinte</em>.</h2>
<p>Você manda o hóspede para o restaurante, o guia e o transfer. Combinou algo numa conversa, mas não lembra se era 10% ou um valor fixo, quem confirmou a visita, nem quanto tem para receber. E o parceiro também não lembra.</p>
<ul class="lista"><li>Acordos sem registro.</li><li>Indicações que ninguém confirma.</li><li>Comissão que fica para depois e nunca chega.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow" style="color:#C9B37E">Como funciona</span>
<h2>Parceiro, acordo, indicação, <em>comissão</em>.</h2>
<p>Você cadastra cada parceiro com o que ele oferece ao hóspede e o que foi combinado: porcentagem, valor fixo, troca ou nenhuma contrapartida. Cada indicação entra pelo código da reserva, sem nome nem telefone do hóspede. A planilha calcula a comissão, mostra o que falta confirmar e o que há para receber, e avisa quando um acordo precisa ser revisto.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Resultados calculados pela planilha no arquivo de exemplo (parceiros, valores e reservas fictícios).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Cadastre os parceiros que você já indica.</li><li><b style="color:#C9B37E">2.</b> Combine por escrito com a ficha de acordo.</li><li><b style="color:#C9B37E">3.</b> Registre cada indicação pelo código da reserva.</li><li><b style="color:#C9B37E">4.</b> Uma vez por mês: confirme, cobre e revise.</li></ul></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow" style="color:#C9B37E">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/parcerias-16/capa.jpg" alt="Capa do produto: Kit Operacional de Parcerias" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco para até 40 parceiros e 300 indicações</li><li>Exemplo preenchido (dados fictícios)</li><li>Ficha de acordo com parceiro para imprimir</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow" style="color:#C9B37E">Perguntas frequentes</span>
<details><summary>Preciso cobrar comissão dos parceiros?</summary><p>Não. Você pode marcar troca, cortesia ou nenhuma contrapartida: a planilha organiza do mesmo jeito.</p></details>
<details><summary>A ficha de acordo vale como contrato?</summary><p>Não. Ela registra o combinado; contrato deve ser revisado por advogado.</p></details>
<details><summary>Preciso anotar o nome do hóspede?</summary><p>Não, e não deve. Use o código da reserva.</p></details>
<details><summary>Comissão tem imposto?</summary><p>Pode ter. Fale com o seu contador.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Indique melhor, <em>com tudo combinado</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero o kit de parcerias</a><span class="micro" style="color:#A39E8E">Material educativo. Não garante reservas, vendas nem pagamentos dos parceiros.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))

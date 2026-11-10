"""Gera landing/dist/clickmax.html da Ferramenta 20 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
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
t1 = tela("TAREFAS DA SEMANA", "Júlia (fictícia) · dia 4", M,
          [linha("Volta por todas as unidades", "Pronta", M), linha("Contatos de emergência", "Atrasada", V), linha("Ver uma limpeza completa", "Pronta", M),
           linha("Ver uma troca de enxoval", "Atrasada", V), linha("Limpeza completa acompanhada", "Feita junto", AZ), linha("Registrar uma ocorrência", "Conferir", V)],
          "Cada tarefa passa por mostrar, fazer junto e fazer sozinha.")
t2 = tela("PAINEL DO TREINAMENTO", "Ainda não: há linhas para conferir", A_,
          [linha("Tarefas no plano", "16", "#FFFFFF"), linha("Obrigatórias prontas", "6 de 14", M), linha("Atrasadas", "4", V), linha("Linhas para conferir", "1", V)],
          "O turno sozinha só é liberado com todas as obrigatórias prontas.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow" style="color:#C9B37E">Ferramenta 20 · Zion Hospitality Business</span>
<h1>Ela já pode <em>fazer o turno sozinha?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para treinar a primeira pessoa da sua equipe: o que mostrar, o que fazer junto, quando ela pode trabalhar sozinha e quem conferiu cada tarefa.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings.</span><a class="btn" href="#oferta" data-cx-cta>Quero o kit de treinamento</a><span class="micro" style="color:#A39E8E">Planilha + ficha do primeiro turno + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow" style="color:#C9B37E">O problema</span>
<h2>Explicar uma vez <em>não é treinar</em>.</h2>
<p>A pessoa nova vê a limpeza uma vez, ouve um monte de detalhes e no dia seguinte já está sozinha. Aí aparece o enxoval errado, a ronda esquecida, o hóspede atendido de outro jeito. E ninguém sabe o que foi ensinado de fato.</p>
<ul class="lista"><li>Tudo explicado de uma vez, sem ordem.</li><li>Ninguém confere se ela fez sozinha do jeito certo.</li><li>Não há um critério para dizer "agora pode".</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow" style="color:#C9B37E">Como funciona</span>
<h2>Mostrar, fazer junto, <em>fazer sozinha</em>.</h2>
<p>A planilha traz uma trilha de seis etapas que parte do onboarding usado nas unidades da Zion: conhecer o lugar, o padrão da casa, ver a função, ler o procedimento, a primeira execução acompanhada e a confirmação. Cada tarefa passa por três passos, com data e com o nome de quem conferiu. O painel diz quando a pessoa está liberada para o turno sozinha.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Resultados calculados pela planilha no arquivo de exemplo (pessoas, datas e hospedagem fictícias).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Ajuste a lista e marque o que é obrigatório.</li><li><b style="color:#C9B37E">2.</b> Use a ficha no primeiro dia.</li><li><b style="color:#C9B37E">3.</b> Anote cada passo com data e quem conferiu.</li><li><b style="color:#C9B37E">4.</b> Libere o turno sozinha quando o painel disser Sim.</li></ul></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow" style="color:#C9B37E">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/treinamento-20/capa.jpg" alt="Capa do produto: Kit de Treinamento do Primeiro Turno" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco com 6 etapas e 16 tarefas sugeridas, e painel</li><li>Exemplo preenchido (dados fictícios)</li><li>Ficha do primeiro turno para imprimir</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow" style="color:#C9B37E">Perguntas frequentes</span>
<details><summary>Serve para qualquer função?</summary><p>Sim. A lista vem com tarefas de limpeza, manutenção e recepção, e você ajusta à função e à sua hospedagem.</p></details>
<details><summary>Substitui contrato ou treinamentos exigidos por lei?</summary><p>Não. Contrato, registro e treinamentos obrigatórios seguem com o seu contador ou advogado.</p></details>
<details><summary>Avalia se a pessoa é boa?</summary><p>Não. Registra o que foi ensinado e conferido, para você decidir com base no que aconteceu.</p></details>
<details><summary>Serve para mais de uma pessoa?</summary><p>Sim, um arquivo por pessoa: é só duplicar.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Treine uma vez, <em>do jeito certo</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero o kit de treinamento</a><span class="micro" style="color:#A39E8E">Material educativo. Não garante resultado, reservas nem desempenho da equipe.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))

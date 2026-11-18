"""Gera landing/dist/clickmax.html da Ferramenta 28 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
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
t1 = tela("SAÍDAS", "8 próximas · 4 confirmadas · 1 sem condutor", A_,
          [linha("21/11 · Trilha · 12 de 12", "Lotada, com espera", A_), linha("21/11 · Café · 14 de 20", "Falta condutor", A_),
           linha("22/11 · Aula · 2 de 8", "Decida", A_), linha("26/11 · Barco · 11 de 10", "Acima da capacidade", V),
           linha("25/11 · Café · 8 de 20", "Confirmada", M)],
          "Cada saída com vagas, equipe e situação.")
t2 = tela("PAINEL", "50 pessoas e 10 condutores nos próximos 7 dias", M,
          [linha("Próximas saídas", "8", "#fff"), linha("Abaixo do mínimo", "2", "#fff"), linha("Falta condutor", "1", "#fff"),
           linha("Pessoas na lista de espera", "3", "#fff")],
          "O que a semana pede, num lugar só.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow" style="color:#C9B37E">Ferramenta 28 · Zion Hospitality Business</span>
<h1>Lotou demais, faltou guia <em>ou saiu com duas pessoas?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para planejar as saídas das suas experiências: quantas pessoas cabem, quantos condutores escalar, quando confirmar ou cancelar e o que fazer com a lista de espera.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas, glampings e quem oferece passeios e experiências.</span><a class="btn" href="#oferta" data-cx-cta>Quero o planner</a><span class="micro" style="color:#A39E8E">Planilha + ficha de saída + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow" style="color:#C9B37E">O problema</span>
<h2>A agenda está na cabeça <em>até o dia em que não cabe</em>.</h2>
<p>Trilha, passeio, aula ou café especial com horário marcado. As reservas chegam por vários lados e, quando você vê, a saída passou da capacidade, o guia da manhã não foi escalado ou o passeio vai sair com duas pessoas e não paga o dia.</p>
<ul class="lista"><li>Saída lotada além do que a equipe atende.</li><li>Condutor que ninguém escalou.</li><li>Cancelamento decidido em cima da hora.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow" style="color:#C9B37E">Como funciona</span>
<h2>Regras uma vez, <em>situação de cada saída</em>.</h2>
<p>Você anota as regras de cada experiência: capacidade, quantas pessoas cada condutor acompanha, o mínimo para a saída valer e com quantos dias de antecedência você decide. Depois lança cada saída só com números: pessoas reservadas, condutores escalados e lista de espera. A planilha calcula vagas e condutores necessários, diz a situação de cada saída e mostra o que fazer agora.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Resultados calculados pela planilha no arquivo de exemplo (experiências, datas e números fictícios).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Escreva as regras de cada experiência.</li><li><b style="color:#C9B37E">2.</b> Lance as saídas das próximas duas semanas.</li><li><b style="color:#C9B37E">3.</b> Resolva o que a coluna Situação pede.</li><li><b style="color:#C9B37E">4.</b> Imprima a ficha de cada saída confirmada.</li></ul></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow" style="color:#C9B37E">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/capacidade-28/capa.jpg" alt="Capa do produto: Planner de Capacidade e Atendimento" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco para até 20 experiências e 200 saídas</li><li>Exemplo preenchido (dados fictícios)</li><li>Ficha de saída para imprimir</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow" style="color:#C9B37E">Perguntas frequentes</span>
<details><summary>A planilha diz quantas pessoas são seguras para a minha atividade?</summary><p>Não. Você informa a capacidade e quantas pessoas cada condutor acompanha; a planilha faz as contas com esses números.</p></details>
<details><summary>Ela calcula preço ou custo?</summary><p>Não. Para isso existe a Calculadora de Custos de Experiências (Ferramenta 29), vendida separadamente.</p></details>
<details><summary>Preciso anotar os nomes dos participantes?</summary><p>Não, e não deve. A planilha usa só quantidades.</p></details>
<details><summary>Recebe reservas ou avisa os participantes?</summary><p>Não. Você atualiza os números e faz o contato.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Cada saída <em>no tamanho certo</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero o planner</a><span class="micro" style="color:#A39E8E">Material educativo. Não garante reservas, procura nem avaliações.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))

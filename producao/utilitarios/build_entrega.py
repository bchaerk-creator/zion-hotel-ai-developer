"""Gera, para cada ferramenta utilitária, a capa do produto (1080x1080, JPG) e a página de acesso do comprador
(index.html), dentro de docs/p/adbc67069af26ae0/<pasta>/. Fotos reais da Zion sem pessoas.
Uso: python3 -I producao/utilitarios/build_entrega.py && node producao/utilitarios/render_capas.js"""
import pathlib, html, json
R = pathlib.Path(__file__).resolve().parents[2]
P = R / "docs/p/adbc67069af26ae0"
E = html.escape

PRODUTOS = [
    dict(pasta="checklist-17", num="17", telas=["producao/utilitarios/17-checklist-limpeza/dist/demonstracao/demo-bloqueada.png", "producao/utilitarios/17-checklist-limpeza/dist/demonstracao/demo-liberada.png"], titulo="Checklist de Limpeza, Inspeção e Liberação",
         promessa="Aprenda o passo a passo para limpar, conferir e liberar cada unidade com o mesmo padrão, sabendo quem fez, quem conferiu e o que ficou pendente.",
         itens=["Planilha com modelo de 33 itens em 8 ambientes", "Exemplo preenchido", "Checklist para imprimir", "Guia passo a passo"],
         passos=["Leia o guia (cerca de 15 minutos).", "Abra o exemplo e veja uma troca preenchida.", "Na planilha em branco, ajuste o modelo à sua unidade e defina quem limpa e quem confere.", "Use na próxima troca de hóspede: libere só quando a situação ficar verde."],
         arquivos=[("Guia-Aprenda-o-Passo-a-Passo.pdf", "Guia Aprenda o passo a passo", "PDF · comece por aqui"),
                   ("Checklist-Limpeza-Zion-EM-BRANCO.xlsx", "Planilha · versão em branco", "Excel, Google Sheets ou LibreOffice"),
                   ("Checklist-Limpeza-Zion-EXEMPLO.xlsx", "Planilha · exemplo preenchido", "Dados fictícios"),
                   ("Checklist-Imprimivel.pdf", "Checklist para imprimir", "PDF · 2 páginas")]),
    dict(pasta="kit-mensagens-11", num="11", telas=["producao/utilitarios/11-mensagens-chegada-saida/dist/demonstracao/demo-falta.png", "producao/utilitarios/11-mensagens-chegada-saida/dist/demonstracao/demo-pronta.png"], titulo="Kit de Mensagens de Chegada e Saída",
         promessa="Aprenda o passo a passo para enviar, no momento certo, as mensagens de confirmação, acesso, chegada, apoio durante a estadia e saída.",
         itens=["Planilha que monta 10 mensagens", "Data de envio de cada uma", "Modelos em PDF", "Guia passo a passo"],
         passos=["Leia o guia (cerca de 10 minutos).", "Abra o exemplo e veja as 10 mensagens montadas.", "Na planilha em branco, preencha a ficha da hospedagem uma vez.", "A cada reserva, preencha nome e datas e siga a coluna Data de envio."],
         arquivos=[("Guia-Aprenda-o-Passo-a-Passo.pdf", "Guia Aprenda o passo a passo", "PDF · comece por aqui"),
                   ("Kit-Mensagens-Zion-EM-BRANCO.xlsx", "Planilha · versão em branco", "Excel, Google Sheets ou LibreOffice"),
                   ("Kit-Mensagens-Zion-EXEMPLO.xlsx", "Planilha · exemplo preenchido", "Dados fictícios"),
                   ("Mensagens-Modelo.pdf", "Modelos de mensagens", "PDF · para copiar à mão")]),
    dict(pasta="enxoval-13", num="13", telas=["producao/utilitarios/13-controle-enxoval/dist/demonstracao/demo-movimentos.png", "producao/utilitarios/13-controle-enxoval/dist/demonstracao/demo-compras.png"],
         titulo="Controle de Enxoval e Reposição",
         promessa="Aprenda o passo a passo para saber quanto enxoval e quantos itens de reposição você tem, quanto deveria ter e o que precisa comprar.",
         itens=["Mínimo de cada item", "Entradas e saídas", "Lista do que comprar e custo", "Ficha de contagem semanal"],
         passos=["Leia o guia (cerca de 15 minutos).", "Abra o exemplo e veja a aba Saldo.", "Na planilha em branco, ajuste a lista, defina os mínimos e lance a contagem inicial.", "Lance compras e saídas e conte uma vez por semana com a ficha."],
         arquivos=[("Guia-Aprenda-o-Passo-a-Passo.pdf", "Guia Aprenda o passo a passo", "PDF · comece por aqui"),
                   ("Controle-Enxoval-Zion-EM-BRANCO.xlsx", "Planilha · versão em branco", "Excel, Google Sheets ou LibreOffice"),
                   ("Controle-Enxoval-Zion-EXEMPLO.xlsx", "Planilha · exemplo preenchido", "Dados fictícios"),
                   ("Ficha-de-Contagem.pdf", "Ficha de contagem semanal", "PDF · para imprimir")]),
    dict(pasta="ocorrencias-14", num="14", telas=["producao/utilitarios/14-quadro-ocorrencias/dist/demonstracao/demo-ocorrencias.png", "producao/utilitarios/14-quadro-ocorrencias/dist/demonstracao/demo-painel.png"],
         titulo="Quadro de Ocorrências e Manutenção",
         promessa="Aprenda o passo a passo para registrar cada problema com responsável, prioridade e prazo, acompanhar até resolver e saber quais unidades não podem receber hóspede.",
         itens=["Responsável, prioridade e prazo", "Atrasos destacados", "Unidades bloqueadas", "Ficha de ronda"],
         passos=["Leia o guia (cerca de 15 minutos).", "Abra o exemplo e veja a aba Painel.", "Na planilha em branco, ajuste os prazos e cadastre unidades e responsáveis.", "Lance cada problema, feche com data e descrição e confira o Painel antes de cada entrada."],
         arquivos=[("Guia-Aprenda-o-Passo-a-Passo.pdf", "Guia Aprenda o passo a passo", "PDF · comece por aqui"),
                   ("Quadro-Ocorrencias-Zion-EM-BRANCO.xlsx", "Planilha · versão em branco", "Excel, Google Sheets ou LibreOffice"),
                   ("Quadro-Ocorrencias-Zion-EXEMPLO.xlsx", "Planilha · exemplo preenchido", "Dados fictícios"),
                   ("Ficha-de-Ronda.pdf", "Ficha de ronda", "PDF · para imprimir")]),
    dict(pasta="experiencias-29", num="29", telas=["producao/utilitarios/29-custos-experiencias/dist/demonstracao/demo-resultado.png", "producao/utilitarios/29-custos-experiencias/dist/demonstracao/demo-cenarios.png"],
         titulo="Calculadora de Custos de Experiências",
         promessa="Aprenda o passo a passo para calcular quanto custa cada sessão de uma experiência, quanto sobra depois das taxas e a partir de quantos participantes ela se paga.",
         itens=["Custos da sessão e por pessoa", "Taxas e impostos", "Mínimo de participantes", "Preço mínimo"],
         passos=["Leia o guia (cerca de 15 minutos).", "Abra o exemplo e veja os resultados e os cenários.", "Preencha a ficha da experiência à mão com os seus custos.", "Passe os números para a calculadora em branco e defina o mínimo para confirmar a saída."],
         arquivos=[("Guia-Aprenda-o-Passo-a-Passo.pdf", "Guia Aprenda o passo a passo", "PDF · comece por aqui"),
                   ("Custos-Experiencias-Zion-EM-BRANCO.xlsx", "Calculadora · versão em branco", "Excel, Google Sheets ou LibreOffice"),
                   ("Custos-Experiencias-Zion-EXEMPLO.xlsx", "Calculadora · exemplo preenchido", "Dados fictícios"),
                   ("Ficha-da-Experiencia.pdf", "Ficha da experiência", "PDF · para imprimir")]),
    dict(pasta="orcamento-05", num="05", telas=["producao/utilitarios/05-orcamento-cabana/dist/demonstracao/demo-cotacoes.png", "producao/utilitarios/05-orcamento-cabana/dist/demonstracao/demo-resumo.png"],
         titulo="Orçamento da Cabana",
         promessa="Aprenda o passo a passo para montar o orçamento da sua cabana de Airbnb, do projeto à abertura, com 3 cotações por item, reserva para imprevistos e cronograma de pagamentos.",
         itens=["Lista sugerida em 10 etapas", "3 cotações por item", "Reserva e comparação com a verba", "Cronograma de pagamentos"],
         passos=["Leia o guia (cerca de 20 minutos).", "Abra o exemplo e veja as abas Orçamento, Resumo e Cronograma.", "Imprima a ficha de cotação e peça 3 cotações com a mesma especificação.", "Lance tudo na planilha em branco e compare o total com a sua verba."],
         arquivos=[("Guia-Aprenda-o-Passo-a-Passo.pdf", "Guia Aprenda o passo a passo", "PDF · comece por aqui"),
                   ("Orcamento-Cabana-Zion-EM-BRANCO.xlsx", "Planilha · versão em branco", "Excel, Google Sheets ou LibreOffice"),
                   ("Orcamento-Cabana-Zion-EXEMPLO.xlsx", "Planilha · exemplo preenchido", "Dados fictícios"),
                   ("Ficha-de-Cotacao.pdf", "Ficha de cotação", "PDF · para imprimir")]),
    dict(pasta="manutencao-18", num="18", telas=["producao/utilitarios/18-manutencao-preventiva/dist/demonstracao/demo-plano.png", "producao/utilitarios/18-manutencao-preventiva/dist/demonstracao/demo-painel.png"],
         titulo="Planner de Manutenção Preventiva",
         promessa="Aprenda o passo a passo para montar um plano de manutenção preventiva da sua hospedagem: o que conferir, de quanto em quanto tempo, quem faz e o que está atrasado.",
         itens=["21 tarefas sugeridas", "Próxima data calculada", "Atrasadas e em breve", "Ficha de ronda"],
         passos=["Leia o guia (cerca de 15 minutos).", "Abra o exemplo e veja as abas Plano, Registro e Painel.", "Na planilha em branco, ajuste a lista e anote a última vez de cada tarefa.", "Use a ficha de ronda e passe o que foi feito para a aba Registro; abra o Painel toda semana."],
         arquivos=[("Guia-Aprenda-o-Passo-a-Passo.pdf", "Guia Aprenda o passo a passo", "PDF · comece por aqui"),
                   ("Manutencao-Preventiva-Zion-EM-BRANCO.xlsx", "Planilha · versão em branco", "Excel, Google Sheets ou LibreOffice"),
                   ("Manutencao-Preventiva-Zion-EXEMPLO.xlsx", "Planilha · exemplo preenchido", "Dados fictícios"),
                   ("Ficha-de-Ronda-Preventiva.pdf", "Ficha de ronda preventiva", "PDF · para imprimir")]),
    dict(pasta="treinamento-20", num="20", telas=["producao/utilitarios/20-treinamento-primeiro-turno/dist/demonstracao/demo-tarefas.png", "producao/utilitarios/20-treinamento-primeiro-turno/dist/demonstracao/demo-painel.png"],
         titulo="Kit de Treinamento do Primeiro Turno",
         promessa="Aprenda o passo a passo para treinar a primeira pessoa da sua equipe: o que mostrar, o que fazer junto, quando ela pode trabalhar sozinha e quem conferiu cada tarefa.",
         itens=["6 etapas, 16 tarefas sugeridas", "Mostrar, fazer junto, fazer sozinha", "Liberação do turno sozinha", "Ficha do primeiro turno"],
         passos=["Leia o guia (cerca de 15 minutos).", "Abra o exemplo e veja as abas Treinamento e Painel.", "Na planilha em branco, ajuste a lista e marque as tarefas obrigatórias.", "Use a ficha no primeiro dia e passe as datas para a planilha; libere o turno sozinha quando o Painel disser Sim."],
         arquivos=[("Guia-Aprenda-o-Passo-a-Passo.pdf", "Guia Aprenda o passo a passo", "PDF · comece por aqui"),
                   ("Treinamento-Primeiro-Turno-Zion-EM-BRANCO.xlsx", "Planilha · versão em branco", "Excel, Google Sheets ou LibreOffice"),
                   ("Treinamento-Primeiro-Turno-Zion-EXEMPLO.xlsx", "Planilha · exemplo preenchido", "Dados fictícios"),
                   ("Ficha-do-Primeiro-Turno.pdf", "Ficha do primeiro turno", "PDF · para imprimir")]),
    dict(pasta="briefing-30", num="30", telas=["producao/utilitarios/30-briefing-experiencia/dist/demonstracao/demo-briefing.png", "producao/utilitarios/30-briefing-experiencia/dist/demonstracao/demo-mensagens.png"],
         titulo="Gerador de Briefing de Experiência",
         promessa="Aprenda o passo a passo para escrever o briefing da sua experiência uma vez e gerar, para cada saída, a descrição, as mensagens ao cliente e o briefing de quem conduz.",
         itens=["Briefing escrito uma vez", "8 textos por saída", "Datas de envio", "Aviso do que falta"],
         passos=["Leia o guia (cerca de 15 minutos).", "Abra o exemplo e veja as abas Ficha e Mensagens.", "Na planilha em branco, escreva o briefing da sua experiência.", "A cada saída, preencha cliente, data, horário e participantes e siga as datas de envio."],
         arquivos=[("Guia-Aprenda-o-Passo-a-Passo.pdf", "Guia Aprenda o passo a passo", "PDF · comece por aqui"),
                   ("Briefing-Experiencia-Zion-EM-BRANCO.xlsx", "Planilha · versão em branco", "Excel, Google Sheets ou LibreOffice"),
                   ("Briefing-Experiencia-Zion-EXEMPLO.xlsx", "Planilha · exemplo preenchido", "Dados fictícios"),
                   ("Mensagens-Modelo-Experiencia.pdf", "Modelos de texto", "PDF · para copiar à mão")]),
    dict(pasta="fornecedores-15", num="15", telas=["producao/utilitarios/15-comparador-fornecedores/dist/demonstracao/demo-cotacoes.png", "producao/utilitarios/15-comparador-fornecedores/dist/demonstracao/demo-resumo.png"],
         titulo="Comparador de Fornecedores",
         promessa="Aprenda o passo a passo para comparar fornecedores da sua hospedagem pelo custo real, pelo prazo e pelo que importa para você, e escolher com critério.",
         itens=["Custo real por unidade", "Frete e pedido mínimo na conta", "Notas com os seus pesos", "Melhor nota × menor custo"],
         passos=["Leia o guia (cerca de 15 minutos).", "Abra o exemplo e veja a aba Resumo.", "Na planilha em branco, ajuste os pesos e liste as necessidades.", "Peça 3 cotações com o roteiro e lance cada uma na aba Cotações."],
         arquivos=[("Guia-Aprenda-o-Passo-a-Passo.pdf", "Guia Aprenda o passo a passo", "PDF · comece por aqui"),
                   ("Comparador-Fornecedores-Zion-EM-BRANCO.xlsx", "Planilha · versão em branco", "Excel 2019+, Google Sheets ou LibreOffice"),
                   ("Comparador-Fornecedores-Zion-EXEMPLO.xlsx", "Planilha · exemplo preenchido", "Dados fictícios"),
                   ("Roteiro-de-Cotacao.pdf", "Roteiro de cotação", "PDF · para imprimir")]),
]

FONTES_LOCAIS = f"""@font-face{{font-family:Cormorant;src:url('{(R/'docs/assets/fonts/cormorant.woff2').as_uri()}')}}
@font-face{{font-family:Aventa;src:url('{(R/'docs/assets/fonts/aventa.woff2').as_uri()}')}}"""

PUBLICO = "Para Airbnb, casas, apartamentos, pousadas e glampings"

def capa_html(p):
    """Capa centrada no produto: telas reais da ferramenta (valores calculados pela planilha), sem foto de hospedagem."""
    lis = "".join(f"<li>{E(i)}</li>" for i in p["itens"])
    t1, t2 = [(R / x).as_uri() for x in p["telas"]]
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTES_LOCAIS}
*{{box-sizing:border-box;margin:0}} body{{width:1080px;height:1080px;overflow:hidden;font-family:Aventa,Arial,sans-serif;color:#FEF5F0;
background:radial-gradient(circle at 78% 40%,#2c3524 0%,#1B2117 55%,#121610 100%);position:relative}}
.logo{{position:absolute;top:64px;left:72px;height:52px}}
.txt{{position:absolute;left:72px;top:190px;width:500px}}
.k{{font-size:21px;letter-spacing:.22em;text-transform:uppercase;color:#C9B37E;font-weight:700;margin-bottom:24px;line-height:1.4}}
h1{{font-family:Cormorant,Georgia,serif;font-weight:500;font-size:76px;line-height:1.02;margin-bottom:34px}}
ul{{list-style:none;padding:0}} li{{font-size:25px;color:#DED6BF;padding:0 0 14px 30px;position:relative}}
li:before{{content:"";position:absolute;left:0;top:11px;width:12px;height:12px;background:#C9B37E;border-radius:2px}}
.pub{{position:absolute;left:72px;right:72px;bottom:64px;border-top:1px solid rgba(201,179,126,.45);padding-top:24px;font-size:25px;color:#FEF5F0}}
.pub b{{color:#C9B37E;font-weight:600}}
.tela{{position:absolute;width:300px;border-radius:26px;border:8px solid #0b0e09;box-shadow:0 30px 60px rgba(0,0,0,.55);background:#fff}}
.t1{{left:610px;top:150px;transform:rotate(-4deg)}} .t2{{left:735px;top:250px;transform:rotate(5deg)}}
</style></head><body>
<img class="logo" src="{(R/'docs/brand/zion-logo-claro.png').as_uri()}">
<div class="txt"><div class="k">Ferramenta {p['num']}<br>Zion Hospitality Business</div><h1>{E(p['titulo'])}</h1><ul>{lis}</ul></div>
<img class="tela t1" src="{t1}"><img class="tela t2" src="{t2}">
<div class="pub"><b>{PUBLICO}.</b> Telas reais da planilha, com dados fictícios.</div></body></html>"""

def acesso_html(p):
    arqs = "".join(f'<a class="arq" href="{a}" download><span class="n">{i}</span><span class="t"><b>{E(t)}</b><small>{E(d)}</small></span><span class="b">Baixar</span></a>'
                   for i, (a, t, d) in enumerate(p["arquivos"], 1))
    passos = "".join(f"<li>{E(s)}</li>" for s in p["passos"])
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>{E(p['titulo'])} · Seu acesso</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--preto:#040605;--musgo:#1B2117;--creme:#FEF5F0;--areia:#DED6BF;--terra:#8B714E;--ouro:#C9B37E}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--creme);color:var(--musgo);font-family:Jost,Arial,sans-serif;font-size:17px;line-height:1.55}}
.wrap{{max-width:680px;margin:0 auto;padding:0 16px 48px}}
.capa{{width:100%;aspect-ratio:1/1;object-fit:cover;display:block;border-radius:0 0 14px 14px;margin:0 auto 26px;max-width:680px}}
h1{{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;font-size:clamp(32px,7vw,44px);line-height:1.08;margin:0 0 12px}}
.k{{font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--terra);font-weight:600;margin-bottom:8px}}
h2{{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;font-size:28px;margin:34px 0 12px}}
.arq{{display:flex;align-items:center;gap:14px;background:#fff;border:1px solid var(--areia);border-radius:12px;padding:14px;margin:10px 0;text-decoration:none;color:var(--musgo)}}
.arq .n{{flex:0 0 36px;height:36px;border-radius:50%;background:var(--musgo);color:var(--creme);display:grid;place-items:center;font-weight:600}}
.arq .t{{flex:1;display:flex;flex-direction:column}} .arq small{{color:#6b6656;font-size:14px}}
.arq .b{{background:var(--ouro);color:var(--preto);font-weight:600;font-size:14px;padding:8px 14px;border-radius:6px;letter-spacing:.04em}}
ol li{{margin-bottom:8px}} .nota{{font-size:14px;color:#6b6656;border-top:1px solid var(--areia);padding-top:16px;margin-top:34px}}
</style></head><body>
<img class="capa" src="capa.jpg" alt="Capa: {E(p['titulo'])}">
<div class="wrap"><div class="k">Ferramenta {p['num']} · Seu acesso</div><h1>{E(p['titulo'])}</h1>
<p>{E(p['promessa'])}</p><p style="color:#8B714E;font-weight:600">{PUBLICO}.</p>
<h2>Seus arquivos</h2>{arqs}
<h2>Por onde começar</h2><ol>{passos}</ol>
<p class="nota">Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.<br>
Dúvidas: WhatsApp +55 48 6137-1061. Material educativo da Zion Hospitality Business: não garante avaliações, reservas nem ocupação.</p></div></body></html>"""

build = R / "producao/utilitarios/.build_capas"; build.mkdir(exist_ok=True)
jobs = []
for p in PRODUTOS:
    d = P / p["pasta"]; assert all((d / a).exists() for a, _, _ in p["arquivos"]), p["pasta"]
    (build / f"{p['pasta']}.html").write_text(capa_html(p), encoding="utf-8")
    (d / "index.html").write_text(acesso_html(p), encoding="utf-8")
    jobs.append([str(build / f"{p['pasta']}.html"), str(d / "capa.jpg")])
(build / "jobs.json").write_text(json.dumps(jobs)); print("ok", [p["pasta"] for p in PRODUTOS])

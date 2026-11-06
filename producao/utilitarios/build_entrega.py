"""Gera, para cada ferramenta utilitária, a capa do produto (1080x1080, JPG) e a página de acesso do comprador
(index.html), dentro de docs/p/adbc67069af26ae0/<pasta>/. Fotos reais da Zion sem pessoas.
Uso: python3 -I producao/utilitarios/build_entrega.py && node producao/utilitarios/render_capas.js"""
import pathlib, html, json
R = pathlib.Path(__file__).resolve().parents[2]
P = R / "docs/p/adbc67069af26ae0"
E = html.escape

PRODUTOS = [
    dict(pasta="checklist-17", num="17", foto="op05", titulo="Checklist de Limpeza, Inspeção e Liberação",
         promessa="Aprenda o passo a passo para limpar, conferir e liberar cada unidade com o mesmo padrão, sabendo quem fez, quem conferiu e o que ficou pendente.",
         itens=["Planilha com modelo de 33 itens em 8 ambientes", "Exemplo preenchido", "Checklist para imprimir", "Guia passo a passo"],
         passos=["Leia o guia (cerca de 15 minutos).", "Abra o exemplo e veja uma troca preenchida.", "Na planilha em branco, ajuste o modelo à sua unidade e defina quem limpa e quem confere.", "Use na próxima troca de hóspede: libere só quando a situação ficar verde."],
         arquivos=[("Guia-Aprenda-o-Passo-a-Passo.pdf", "Guia Aprenda o passo a passo", "PDF · comece por aqui"),
                   ("Checklist-Limpeza-Zion-EM-BRANCO.xlsx", "Planilha · versão em branco", "Excel, Google Sheets ou LibreOffice"),
                   ("Checklist-Limpeza-Zion-EXEMPLO.xlsx", "Planilha · exemplo preenchido", "Dados fictícios"),
                   ("Checklist-Imprimivel.pdf", "Checklist para imprimir", "PDF · 2 páginas")]),
    dict(pasta="kit-mensagens-11", num="11", foto="op11", titulo="Kit de Mensagens de Chegada e Saída",
         promessa="Aprenda o passo a passo para enviar, no momento certo, as mensagens de confirmação, acesso, chegada, apoio durante a estadia e saída.",
         itens=["Planilha que monta 10 mensagens", "Data de envio de cada uma", "Modelos em PDF", "Guia passo a passo"],
         passos=["Leia o guia (cerca de 10 minutos).", "Abra o exemplo e veja as 10 mensagens montadas.", "Na planilha em branco, preencha a ficha da hospedagem uma vez.", "A cada reserva, preencha nome e datas e siga a coluna Data de envio."],
         arquivos=[("Guia-Aprenda-o-Passo-a-Passo.pdf", "Guia Aprenda o passo a passo", "PDF · comece por aqui"),
                   ("Kit-Mensagens-Zion-EM-BRANCO.xlsx", "Planilha · versão em branco", "Excel, Google Sheets ou LibreOffice"),
                   ("Kit-Mensagens-Zion-EXEMPLO.xlsx", "Planilha · exemplo preenchido", "Dados fictícios"),
                   ("Mensagens-Modelo.pdf", "Modelos de mensagens", "PDF · para copiar à mão")]),
]

FONTES_LOCAIS = f"""@font-face{{font-family:Cormorant;src:url('{(R/'docs/assets/fonts/cormorant.woff2').as_uri()}')}}
@font-face{{font-family:Aventa;src:url('{(R/'docs/assets/fonts/aventa.woff2').as_uri()}')}}"""

def capa_html(p):
    lis = "".join(f"<li>{E(i)}</li>" for i in p["itens"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTES_LOCAIS}
*{{box-sizing:border-box;margin:0}} body{{width:1080px;height:1080px;overflow:hidden;background:#1B2117;font-family:Aventa,Arial,sans-serif;color:#FEF5F0}}
.foto{{position:absolute;inset:0;width:100%;height:62%;object-fit:cover}}
.grad{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(27,33,23,0) 30%,rgba(27,33,23,.85) 52%,#1B2117 62%)}}
.txt{{position:absolute;left:80px;right:80px;bottom:76px}}
.logo{{position:absolute;top:60px;left:80px;height:54px}}
.k{{font-size:22px;letter-spacing:.24em;text-transform:uppercase;color:#C9B37E;font-weight:700;margin-bottom:22px}}
h1{{font-family:Cormorant,Georgia,serif;font-weight:500;font-size:82px;line-height:1.02;margin-bottom:30px}}
ul{{list-style:none;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:12px 30px}} li{{font-size:24px;color:#DED6BF;padding-left:28px;position:relative}}
li:before{{content:"";position:absolute;left:0;top:11px;width:12px;height:12px;background:#C9B37E;border-radius:2px}}
.cred{{position:absolute;top:66px;right:80px;font-size:16px;color:#FEF5F0;text-shadow:0 1px 6px rgba(0,0,0,.9)}}</style></head><body>
<img class="foto" src="{(R/'docs/assets/operacoes'/(p['foto']+'.webp')).as_uri()}"><div class="grad"></div>
<img class="logo" src="{(R/'docs/brand/zion-logo-claro.png').as_uri()}"><div class="cred">Foto real · Zion Bubble Glamping</div>
<div class="txt"><div class="k">Ferramenta {p['num']} · Zion Hospitality Business</div><h1>{E(p['titulo'])}</h1><ul>{lis}</ul></div></body></html>"""

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
<p>{E(p['promessa'])}</p>
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

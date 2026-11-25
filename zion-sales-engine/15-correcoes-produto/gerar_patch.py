#!/usr/bin/env python3
"""Gera os arquivos corrigidos em patch/docs/ a partir de docs/ (somente leitura em docs/).
Uso: python3 -I gerar_patch.py   (rodar da raiz do repositorio)
Cada substituicao exige exatamente o numero esperado de ocorrencias; se divergir, aborta."""
import re, sys, pathlib, subprocess

RAIZ = pathlib.Path(__file__).resolve().parents[2]
SRC = RAIZ / "docs" / "trilha1"
DST = pathlib.Path(__file__).resolve().parent / "patch" / "docs" / "trilha1"
FICHAS = ["marco-zero", "aula1", "aula2", "aula3", "pilar4", "pilar5", "pilar6", "pilar7"]

SESSAO = ("Ao concluir o Dossiê, você pode solicitar a Sessão de diagnóstico estratégico com a nossa equipe "
          "para apresentar o seu projeto. Sujeita à análise e à agenda; parceria e investimento não são garantidos.")
SESSAO_LONGA = ("Ao concluir o Dossiê, você pode solicitar a Sessão de diagnóstico estratégico com a nossa equipe "
                "para apresentar o seu projeto. A sessão é sujeita à análise e à agenda; não é consultoria contínua, "
                "e parceria e investimento não são garantidos.")

def sub_regex(txt, pat, rep, n, nome, flags=re.S):
    novo, k = re.subn(pat, rep, txt, flags=flags)
    if k != n:
        sys.exit(f"ERRO {nome}: esperado {n} ocorrencia(s), achei {k}")
    return novo

def sub_str(txt, old, new, n, nome):
    k = txt.count(old)
    if k != n:
        sys.exit(f"ERRO {nome}: esperado {n} ocorrencia(s) de {old[:60]!r}, achei {k}")
    return txt.replace(old, new)

STUB = ("/* Zion · correção de 25/11/2026: nenhuma resposta sai deste aparelho. O PDF é gerado aqui e as respostas ficam só no navegador.\n"
        "   Função mantida vazia só porque window.ZionApp a exporta. */\n"
        "function enviarParaZion() { return Promise.resolve({ enviado: false, local: true }); }\n")

def corrige(ficha):
    t = (SRC / ficha / "index.html").read_text(encoding="utf-8")
    n = ficha
    # 1. SDK/rastreador do ClickMax (page_view para api.clickmax.io ao abrir a ficha)
    t = sub_regex(t, r"<!-- Start of Clickmax SDK Code -->.*?<!-- End of Clickmax SDK Code -->\n?", "", 1, n + " sdk")
    # 2. formulario escondido que registra o aluno como lead no ClickMax
    t = sub_regex(t, r"<!-- Zion · lead no ClickMax[^\n]*-->\n<iframe name=\"zx-sink\"[^\n]*\n<form id=\"zx-lead\"[^\n]*</form>\n?", "", 1, n + " zx-lead")
    # 3. botao/bloco Land Bank
    t = sub_str(t, '<script src="../_landbank.js" defer></script>\n', "", 1, n + " landbank")
    # 4. funcoes de envio: zionLead e enviarParaZion viram um no-op local
    t = sub_regex(t, r"function zionLead\(nome, email\) \{.*?\n\}\n", "", 1, n + " zionLead")
    t = sub_regex(t, r"async function enviarParaZion\(payload\) \{.*?\n\}\n", STUB.replace("\\", "\\\\"), 1, n + " enviarParaZion")
    t = sub_regex(t, r'const ZION_WEBHOOK_URL = "https://zion-dossie-aulas\.lovable\.app/api/dossie";', 'const ZION_WEBHOOK_URL = ""; /* correção 25/11/2026: sem envio */', 1, n + " webhook")
    t = sub_str(t, "/* Zion · CRM: guarda a página do Dossiê (Lovable) e registra o aluno no ClickMax. Nunca trava a ferramenta. */", "/* Zion · correção 25/11/2026: sem CRM e sem envio das respostas ao baixar o PDF. */", 1, n + " comentario")
    # 5. chamadas automaticas ao baixar o PDF
    if ficha == "marco-zero":
        t = sub_str(t, "  try { enviarParaZion({ nome: S.nome, email: S.email, estado: S }); } catch (e) {}\n", "", 1, n + " call")
    else:
        t = sub_regex(t, r"enviarParaZion\(montarPayload\(L2?\)\); ", "", 1, n + " call")
    # 6. textos (Land Bank / banco de areas)
    if ficha == "aula1":
        t = sub_str(t, "Terreno com território lido e mercado medido pode entrar no banco de áreas da Zion, a vitrine de terrenos estruturados. A Zion avalia cada caso: é um dos caminhos possíveis, não uma promessa.", SESSAO, 1, n + " txt")
        t = sub_str(t, '<script src="../_anexos.js" data-ficha="pilar1"></script>', '<script src="../_anexos.js" data-ficha="pilar1"></script>', 1, n + " anexos")
    if ficha == "aula2":
        t = sub_str(t, "Terreno com território lido e mercado medido pode entrar no banco de áreas da Zion, a vitrine de projetos estruturados. A Zion avalia cada caso: é um dos caminhos possíveis, não uma promessa.", SESSAO, 1, n + " txt")
    if ficha == "pilar7":
        t = sub_str(t, "venda ou entrada no banco de áreas da Zion. A Zion avalia cada caso.", "venda ou parceria.", 1, n + " rodape")
        t = sub_str(t, 'tit: "Conversar com a Zion", txt: "O banco de áreas da Zion (uma lista de terrenos com o Dossiê feito, organizada pela Zion) é um caminho possível, não uma promessa. Estar na lista não garante investimento, venda ou sociedade. A Zion avalia cada caso."',
                    'tit: "Sessão de diagnóstico estratégico", txt: "' + SESSAO + '"', 1, n + " caminho")
        velho = "Nós, da Zion, organizamos o banco de áreas da Zion, uma lista de terrenos com o Dossiê feito. Estar na lista quer dizer que o seu projeto pode ser olhado. Não quer dizer que ele será escolhido, financiado ou vendido, nem que terá sócio. A Zion avalia cada caso, com os seus critérios."
        t = sub_str(t, velho, SESSAO_LONGA, 2, n + " paragrafo")
    (DST / ficha).mkdir(parents=True, exist_ok=True)
    (DST / ficha / "index.html").write_text(t, encoding="utf-8")

CSS = ("\".zan{max-width:760px;margin:36px auto;padding:22px;border:1px solid #C9B37E;border-radius:14px;background:#1B2117;color:#FEF5F0;font-family:Jost,Arial,sans-serif}\" +\n"
       "      \".zan h3{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:28px;margin:0 0 6px;color:#FEF5F0}\" +\n"
       "      \".zan p{margin:6px 0;line-height:1.55;font-size:15.5px;color:#E8DFD2}\" +\n"
       "      \".zan small{display:block;margin-top:10px;color:#DED6BF}\"")

def bloco(id_, so_fichas):
    cond = ""
    if so_fichas:
        cond = ('  var script = document.currentScript;\n  var FICHA = (script && script.getAttribute("data-ficha")) || "";\n'
                '  if (FICHA !== "pilar1" && FICHA !== "pilar5") return;\n')
    return f'''/* Zion · correção de 25/11/2026. Este arquivo NÃO envia nada: sem fetch, sem upload, sem formulário.
   Texto estático com o próximo passo honesto (Sessão de diagnóstico estratégico, depois de concluir o Dossiê). */
(function () {{
  "use strict";
{cond}  function montar() {{
    if (document.getElementById("{id_}")) return;
    var st = document.createElement("style");
    st.textContent = {CSS};
    document.head.appendChild(st);
    var box = document.createElement("section");
    box.id = "{id_}"; box.className = "zan";
    box.innerHTML = "<h3>Depois do Dossiê: solicite a Sessão de diagnóstico estratégico</h3>" +
      "<p>Ao concluir o Dossiê, você pode solicitar a Sessão de diagnóstico estratégico com a nossa equipe para apresentar o seu projeto, terreno ou empreendimento. É a sua oportunidade de buscar parceiros e investimentos para tirar o plano do papel*.</p>" +
      "<small>*Gratuita para quem concluiu o Dossiê, mediante solicitação. Sujeita à análise e à agenda. Não é consultoria contínua. Parceria e investimento não são garantidos. Esta ferramenta não envia as suas respostas nem arquivos para a Zion: guarde o PDF do seu Dossiê.</small>";
    (document.querySelector("main") || document.body).appendChild(box);
  }}
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", montar); else montar();
}})();
'''

LANDBANK_STUB = '''/* Zion · correção de 25/11/2026: o botão "Enviar ao Land Bank" e o bloco "Banco de áreas da Zion" foram retirados das fichas.
   Arquivo mantido vazio de propósito (páginas antigas em cache ou de terceiros que ainda o carreguem não quebram). Não envia nada. */
(function () { "use strict"; })();
'''

def main():
    for f in FICHAS:
        corrige(f)
    (DST / "_anexos.js").write_text(bloco("anexos-zion", True), encoding="utf-8")
    (DST / "_reuniao.js").write_text(bloco("reuniao-zion", False), encoding="utf-8")
    (DST / "_landbank.js").write_text(LANDBANK_STUB, encoding="utf-8")
    # diffs por ficha
    dd = DST.parent.parent / "diffs"
    dd.mkdir(exist_ok=True)
    pares = [(f, f"{f}/index.html") for f in FICHAS] + [("_anexos", "_anexos.js"), ("_reuniao", "_reuniao.js"), ("_landbank", "_landbank.js")]
    for nome, rel in pares:
        a = SRC / rel; b = DST / rel
        r = subprocess.run(["git", "diff", "--no-index", "--no-color", "--", str(a), str(b)], capture_output=True, text=True, cwd=RAIZ)
        txt = r.stdout.replace(str(a.relative_to(RAIZ)), "docs/trilha1/" + rel).replace(str(b.relative_to(RAIZ)), "patch/docs/trilha1/" + rel)
        (dd / f"{nome}.diff").write_text(txt, encoding="utf-8")
    print("ok")

main()

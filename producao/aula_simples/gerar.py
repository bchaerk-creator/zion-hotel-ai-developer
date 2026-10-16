#!/usr/bin/env python3
"""Gera a aula simples de 40 slides a partir de um roteiro JSON.

Uso: python3 producao/aula_simples/gerar.py roteiro.json docs/escola/<cod>/apresentacao/index.html

Formato do roteiro: ver producao/aula_simples/REGRAS.md
"""
import html, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ICONES = {"key", "star", "house", "bed", "pin", "cal", "user", "tool", "tree", "camera",
          "brain", "drop", "eye", "sun", "doc", "chart", "alert"}


def ic(nome):
    if not nome:
        return ""
    if nome not in ICONES:
        raise SystemExit(f"Ícone desconhecido: {nome}. Use um destes: {sorted(ICONES)}")
    return f'<svg><use href="#i-{nome}"/></svg>'


def a(txt):
    """Escapa para atributo, mantendo <b> permitido nos feedbacks."""
    return html.escape(txt, quote=True)


def render(spec):
    total = len(spec["slides"])
    cod = spec["codigo"]
    out = []
    for n, sl in enumerate(spec["slides"], 1):
        t = sl["tipo"]
        dark = sl.get("escuro", False)
        notas = sl.get("notas", "")
        if t == "capa":
            body = (f'<div class="kick">{sl.get("kicker", "Aula " + cod)}</div>'
                    f'<h1>{sl["titulo"]}</h1><p class="lead">{sl.get("lead", "")}</p>')
            dark = True
        elif t == "secao":
            body = (f'<div class="kick">{sl.get("kicker", "")}</div><h1 class="sec">{sl["titulo"]}</h1>'
                    f'<p class="lead">{sl.get("lead", "")}</p>')
            dark = True
        elif t == "escolha":
            modo = "todas" if sl.get("todas_certas") else "certo"
            cards = "".join(
                f'<div class="op" data-ok="{1 if o.get("certa") or modo == "todas" else 0}" data-fb="{a(o["feedback"])}">'
                f'<div class="L">{"ABCD"[j]}</div><br>{ic(o.get("icone"))}<div class="t">{o["texto"]}</div></div>'
                for j, o in enumerate(sl["opcoes"]))
            if modo == "certo" and sum(1 for o in sl["opcoes"] if o.get("certa")) != 1:
                raise SystemExit(f"Slide {n}: escolha precisa de exatamente 1 opção certa")
            body = (f'<h2>{sl["pergunta"]}</h2><p class="sub">{sl.get("sub", "Toque na opção.")}</p>'
                    f'<div class="ops" data-modo="{modo}" style="--n:{len(sl["opcoes"])}">{cards}</div><div class="fb"></div>')
        elif t == "fluxo":
            passos = sl["passos"]
            parts = []
            for j, p in enumerate(passos):
                cls = "st last" if sl.get("ultimo_apagado") and j == len(passos) - 1 else "st"
                parts.append(f'<div class="{cls}"><div class="n">{j + 1}</div>{ic(p.get("icone"))}'
                             f'<div class="t">{p["titulo"]}</div><div class="d">{p.get("texto", "")}</div></div>')
            body = (f'<h2>{sl["titulo"]}</h2><p class="sub">{sl.get("sub", "")}</p><div class="flow">'
                    + '<div class="ar">→</div>'.join(parts) + '</div>')
        elif t == "cartoes":
            itens = sl["itens"]
            body = (f'<h2>{sl["titulo"]}</h2><p class="sub">{sl.get("sub", "")}</p>'
                    f'<div class="tiles" style="grid-template-columns:repeat({min(len(itens), 4)},1fr)">'
                    + "".join(f'<div class="tile">{ic(i.get("icone"))}<div class="t">{i["titulo"]}</div>'
                              f'<div class="d">{i.get("texto", "")}</div></div>' for i in itens) + '</div>')
        elif t == "marcar":
            itens = sl["itens"]
            cont = sl.get("contador", "Você marcou X de N.").replace("N", str(len(itens))).replace("X", '<b class="num-m">0</b>')
            body = (f'<h2>{sl["titulo"]}</h2><p class="sub">{sl.get("sub", "Toque em cada item.")}</p>'
                    f'<div class="ops" data-modo="marcar" style="--n:3">'
                    + "".join(f'<div class="op">{ic(i.get("icone"))}<div class="t">{i["texto"]}</div></div>' for i in itens)
                    + f'</div><div class="cnt">{cont}</div>')
        elif t == "semaforo":
            body = (f'<h2>{sl["titulo"]}</h2><p class="sub">{sl.get("sub", "")}</p><div class="sem">'
                    f'<div class="c g"><h3><i></i>{sl["verde"]["titulo"]}</h3>{sl["verde"]["texto"]}</div>'
                    f'<div class="c y"><h3><i></i>{sl["amarelo"]["titulo"]}</h3>{sl["amarelo"]["texto"]}</div>'
                    f'<div class="c r"><h3><i></i>{sl["vermelho"]["titulo"]}</h3>{sl["vermelho"]["texto"]}</div></div>')
        elif t == "vf":
            body = (f'<h2>{sl["titulo"]}</h2><p class="sub">Toque na sua resposta.</p><div class="vf">'
                    + "".join(f'<div class="row" data-r="{"v" if f["verdadeiro"] else "f"}"><span class="s">{f["frase"]}</span>'
                              f'<button data-a="v">V</button><button data-a="f">F</button></div>' for f in sl["frases"])
                    + '</div>')
        elif t == "regra":
            body = f'<div class="kick">{sl.get("kicker", "")}</div><p class="regra">{sl["texto"]}</p>'
        elif t == "calculadora":
            c = sl["campos"]
            botoes = sl.get("botoes", [])
            linhas = "".join(f'<button data-n="{b["valor"]}"{" class=\"on\"" if b.get("ativo") else ""}>{b["texto"]}</button>' for b in botoes)
            body = (f'<h2>{sl["titulo"]}</h2><p class="sub">{sl.get("sub", "")}</p>'
                    f'<div class="calc" data-calc><div>'
                    + (f'<div class="btns">{linhas}</div>' if botoes else '')
                    + f'<label>{c["d"]["rotulo"]}</label><input type="number" data-k="d" value="{c["d"]["valor"]}">'
                    f'<label>{c["n"]["rotulo"]}</label><input type="number" data-k="n" value="{c["n"]["valor"]}">'
                    f'<label>{c["c"]["rotulo"]}</label><input type="number" data-k="c" value="{c["c"]["valor"]}"></div>'
                    f'<div class="res"><div class="l"><span>{sl.get("rotulo_entra", "Entra")}</span><span data-o="e"></span></div>'
                    f'<div class="l"><span>{sl.get("rotulo_custos", "Custos")}</span><span data-o="c"></span></div>'
                    f'<div class="l big"><span>{sl.get("rotulo_sobra", "Sobra")}</span><span data-o="s" class="pos"></span></div>'
                    f'<div class="msg" data-o="m"></div></div></div>'
                    f'<p class="ilus">{sl.get("aviso", "Números de exemplo, só para ilustrar. Use os seus.")}</p>')
        elif t == "tarefa":
            passos = sl["passos"]
            body = (f'<div class="kick">Sua tarefa desta semana</div><h2>{sl["titulo"]}</h2><p class="sub">{sl.get("sub", "")}</p>'
                    '<div class="flow">' + '<div class="ar">→</div>'.join(
                        f'<div class="st"><div class="n">{j + 1}</div><div class="t">{p["titulo"]}</div><div class="d">{p.get("texto", "")}</div></div>'
                        for j, p in enumerate(passos)) + '</div>')
            dark = True
        else:
            raise SystemExit(f"Slide {n}: tipo desconhecido {t}")
        out.append(f'<section class="slide v3{" dark" if dark else ""}">\n{body}\n'
                   f'<div class="foot"><span>Zion Hospitality Business · Aula {cod}</span><span>{n:02d} / {total}</span></div>\n'
                   f'<aside class="notes">{notas}</aside>\n</section>\n')
    return out


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    if len(spec["slides"]) != 40:
        raise SystemExit(f"O roteiro tem {len(spec['slides'])} slides; precisa ter 40.")
    head = open(os.path.join(AQUI, "base_head.html"), encoding="utf-8").read()
    tail = open(os.path.join(AQUI, "base_tail.html"), encoding="utf-8").read()
    head = head.replace("{{TITULO}}", html.escape(f'{spec["codigo"]} · {spec["titulo"]} · Aula'))
    os.makedirs(os.path.dirname(sys.argv[2]), exist_ok=True)
    open(sys.argv[2], "w", encoding="utf-8").write(head + "".join(render(spec)) + tail)
    print("ok", sys.argv[2])


if __name__ == "__main__":
    main()

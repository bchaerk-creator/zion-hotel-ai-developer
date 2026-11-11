"""Resumo de reunião a partir das respostas do quiz de agendamento.
Regras explícitas e auditáveis (sem modelo de linguagem, sem inventar número).
Uso: python3 -I brief_reuniao.py respostas.json   (JSON com as respostas; chaves = id do bloco ou texto livre)
"""
import json, sys, unicodedata

def _n(s):
    s = unicodedata.normalize("NFKD", str(s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))

def _pega(r, *chaves):
    for k in chaves:
        for kk, v in r.items():
            if _n(kk) == _n(k):
                return " ".join(v) if isinstance(v, list) else str(v)
    return ""

def pontuar(r):
    sit = _n(_pega(r, "b_situacao")); dif = _n(_pega(r, "b_dif")); apr = _n(_pega(r, "b_aprender"))
    par = _n(_pega(r, "b_parceiro")); inf = _n(_pega(r, "b_infra")); cap = _n(_pega(r, "b_capital"))
    men = _n(_pega(r, "b_mentoria")); clu = _n(_pega(r, "b_clube"))
    p = 0
    p += 2 if ("infraestrutura" in sit and "sem" not in sit) or "operacao" in sit else 1 if "sem infra" in sit else 0
    p += 2 if "parceiro ou investidor" in dif else 1 if any(x in dif for x in ("capital", "por onde", "serve")) else 0
    p += 2 if apr.startswith("sim, agora") else 1 if apr.startswith("sim") else 0
    p += 2 if "quer ser parceiro" in par else 1 if "entender" in par else 0
    p += 2 if inf.startswith("sim, entro") else 1 if inf.startswith(("sim, mas", "preciso")) else 0
    p += 2 if "acima de r$ 400" in cap else 1 if "150" in cap else 0
    p += 2 if men == "sim" else 1 if men.startswith("sim, se") else 0
    p += 2 if clu == "sim" else 1 if "saber" in clu else 0
    return p

OBJ = {
 "capital":  ("Não tenho dinheiro / estou descapitalizado.", "A maioria chega assim: tem a terra e não tem o capital. Sócio e banco entram em projeto, não em terreno. O primeiro passo custa pouco: estruturar. Vamos olhar o que dá para fazer com o que você tem hoje."),
 "decisor":  ("Preciso falar com sócio, família ou cônjuge.", "Faz todo sentido. Pergunte: 'Quem mais precisa ouvir isso? Dá para marcar uma segunda conversa com essa pessoa junto?' Combine a data na própria reunião."),
 "fazer":    ("Quero que vocês façam por mim.", "Alinhe a expectativa com honestidade: a Zion não constrói nem opera o terreno de quem não participa. Há dois caminhos: aprender e estruturar com acompanhamento, ou a parceria, em que você entra com a área e a infraestrutura."),
 "agoranao": ("Agora não / está caro.", "Entenda o motivo: preço, momento ou dúvida do que recebe. Se for preço, volte ao mínimo: clube, inscrição do terreno e aulas gravadas. Se for momento, combine quando retomar."),
 "doc":      ("Meu terreno não tem escritura.", "É o primeiro passo, não o fim: com a área regularizada ela ganha valor e pode entrar no Radar do Land Bank. A formação mostra a ordem certa. Não prometa prazo de regularização."),
 "complica": ("É complicado, não sei por onde começar.", "São etapas curtas, na ordem: ler o lugar, desenhar o produto, desenhar o terreno e fechar a conta. A gente faz junto, na ordem."),
 "talvez":   ("Qual o risco? O que a Zion ganha?", "Explique o modelo: o dono entra com área e infraestrutura, a Zion com a cabana, a marca, as reservas e a formação da equipe. A Zion avalia cada caso e não promete resultado. Mostre as unidades reais de Urubici e Florianópolis."),
}

def brief(r):
    sit = _n(_pega(r, "b_situacao")); doc = _n(_pega(r, "b_doc")); dif = _n(_pega(r, "b_dif")); apr = _n(_pega(r, "b_aprender"))
    par = _n(_pega(r, "b_parceiro")); inf = _n(_pega(r, "b_infra")); cap = _n(_pega(r, "b_capital"))
    men = _n(_pega(r, "b_mentoria")); dec = _n(_pega(r, "b_decisor"))
    pts = pontuar(r)
    temp = "QUENTE" if pts >= 11 else "MORNO" if pts >= 6 else "FRIO"
    doc_ok = "escritura ou matricula" in doc
    com_terreno = "procurando" not in sit and "ainda nao tenho" not in doc
    # perfil (primeira regra que casa)
    if "quer ser parceiro" in par and inf.startswith(("sim, entro", "sim, mas")) and doc_ok:
        perfil, objetivo = "Parceiro pronto", "Desenhar a parceria no local dele e fechar a entrada pelo clube, com a mentoria como acompanhamento."
    elif apr.startswith("nao"):
        perfil, objetivo = "Quer que façam por ele", "Alinhar a expectativa e levar para o caminho de aprender e estruturar; parceria só se houver infraestrutura."
    elif not com_terreno:
        perfil, objetivo = "Ainda sem terreno", "Mostrar o passo a passo e o clube; sem inscrição de terreno por enquanto."
    elif "ainda nao" in cap and men.startswith("agora"):
        perfil, objetivo = "Descapitalizado com vontade", "Começar pelo mínimo (clube, inscrição do terreno e aulas) e abrir a mentoria para o momento certo."
    elif apr.startswith("sim") or men.startswith("sim"):
        perfil, objetivo = "Quer aprender e estruturar", "Vender a mentoria diretamente e, se não fechar, garantir o mínimo."
    else:
        perfil, objetivo = "Curioso, ainda indeciso", "Gerar entendimento do caminho e levar ao mínimo (clube)."
    primaria = "Mentoria (preço e formato: Bruno define)" if (men == "sim" or men.startswith("sim, se") or apr.startswith("sim, agora")) and perfil != "Quer que façam por ele" else "Clube como porta de entrada, com a mentoria apresentada como evolução"
    minimo = ("Clube (R$ 97 · 2x R$ 48,50): acesso por 12 meses, " + ("inscrição do terreno no Radar do Land Bank, " if com_terreno else "") + "aulas gravadas (Panorama Marco Zero e Trilha 1) e a sessão estratégica.")
    gatilhos = []
    if "ainda nao" in cap: gatilhos.append("capital")
    if dec and not dec.startswith("decide sozinho"): gatilhos.append("decisor")
    if apr.startswith("nao"): gatilhos.append("fazer")
    if men.startswith("agora"): gatilhos.append("agoranao")
    if "pendencias" in doc or "contrato" in doc: gatilhos.append("doc")
    if "por onde" in dif: gatilhos.append("complica")
    if "entender" in par: gatilhos.append("talvez")
    objs = [OBJ[g] for g in gatilhos][:4]
    perguntas = ["Conte como o terreno chegou até você e o que você imagina para ele.",
                 "O que já tentou até aqui e o que travou?",
                 "O que precisa acontecer para você sentir que valeu a conversa?"]
    if "decisor" in gatilhos: perguntas.append("Quem mais participa dessa decisão e quando poderíamos falar com essa pessoa?")
    return {"temperatura": temp, "pontos": pts, "perfil": perfil, "objetivo": objetivo,
            "oferta_principal": primaria, "oferta_minima": minimo, "objecoes": objs, "perguntas": perguntas,
            "nao_prometer": ["renda, reservas, ocupação ou retorno", "investimento, sócio ou crédito garantido", "prazo de resultado", "preço, bônus ou vaga que não existam"]}

def render(b):
    L = [f"## Reunião · {b['temperatura']} ({b['pontos']}/16) · {b['perfil']}", f"**Objetivo:** {b['objetivo']}", "",
         f"**Oferta principal:** {b['oferta_principal']}", f"**Se não fechar, no mínimo:** {b['oferta_minima']}", ""]
    L.append("**Objeções prováveis:**")
    for o, r in b["objecoes"]: L.append(f"- *{o}* → {r}")
    L += ["", "**Perguntas de descoberta:**"] + [f"- {p}" for p in b["perguntas"]]
    L += ["", "**Não prometer:** " + "; ".join(b["nao_prometer"]) + "."]
    return "\n".join(L)

if __name__ == "__main__":
    print(render(brief(json.load(open(sys.argv[1], encoding="utf-8")))))

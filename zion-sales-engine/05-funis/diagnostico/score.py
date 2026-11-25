"""Diagnóstico gratuito de estágio de estruturação · Zion · regra v1 (25/11/2026).

O que mede: o ESTÁGIO DE ESTRUTURAÇÃO das informações que a pessoa informou.
O que NÃO mede: valor do terreno, qualidade do investimento, viabilidade
financeira ou jurídica, chance de receber investimento ou parceria.

Entrada: 6 códigos de resposta (nenhum texto livre, nenhum dado pessoal).
Saída: score 0-100, faixa, detalhamento por critério, parecer-modelo e
próximo passo. Chaves desconhecidas são recusadas de propósito: valor da
área, capital, localização e dados pessoais não entram nesta regra.

Uso: python3 -I score.py                (imprime um exemplo fictício)
     python3 -I score.py respostas.json (calcula e imprime parecer e explicação)
"""
import json

VERSAO = "v1-2026-11-25"

# Perguntas e opções. Pontos por critério; "max" é o peso do critério.
# Pergunta 1 (situacao) não pontua: define quais critérios se aplicam.
SITUACOES = {
    "terreno": "Tenho um terreno ou área",
    "ideia": "Tenho uma ideia, ainda sem terreno",
    "hospedagem": "Já tenho uma hospedagem e quero ampliar ou estruturar melhor",
    "aprender": "Quero aprender sobre o assunto",
}

CRITERIOS = {
    "produto": {
        "max": 20, "aplica": ("terreno", "ideia", "hospedagem", "aprender"),
        "nome": "Clareza do empreendimento",
        "opcoes": {"nao_definido": 0, "varias_ideias": 7, "tipo_escolhido": 14, "conceito_descrito": 20},
    },
    "local": {
        "max": 20, "aplica": ("terreno", "hospedagem"),
        "nome": "Informações levantadas sobre a área",
        "opcoes": {"nada": 0, "tamanho_localizacao": 7, "acesso_entorno": 14, "levantamento_feito": 20},
    },
    "documentos": {
        "max": 15, "aplica": ("terreno", "hospedagem"),
        "nome": "Documentos da área reunidos",
        "opcoes": {"nao_sei": 0, "alguns": 7, "reunidos": 15},
    },
    "numeros": {
        "max": 25, "aplica": ("terreno", "ideia", "hospedagem", "aprender"),
        "nome": "Números do projeto (custos e receitas)",
        "opcoes": {"nenhum": 0, "estimativa_de_cabeca": 8, "planilha_parcial": 17, "planilha_completa": 25},
    },
    "apresentacao": {
        "max": 20, "aplica": ("terreno", "ideia", "hospedagem", "aprender"),
        "nome": "Material para mostrar o projeto a terceiros",
        "opcoes": {"nada": 0, "anotacoes_soltas": 7, "resumo_simples": 14, "material_organizado": 20},
    },
}
ORDEM = ("produto", "local", "documentos", "numeros", "apresentacao")

# Faixas sobre a nota normalizada (0-100). Nomes descrevem estágio, não mérito.
FAIXAS = (
    (0, 24, "F1", "Ideia inicial"),
    (25, 49, "F2", "Primeiros levantamentos"),
    (50, 74, "F3", "Projeto em montagem"),
    (75, 100, "F4", "Informações bem organizadas"),
)

LIMITE = ("Este diagnóstico é um retrato do estágio das informações que você nos enviou, "
          "não é avaliação do terreno nem promessa de investimento.")
REVISAO = ("Esta nota foi calculada de forma automática, só com as suas 6 respostas. "
           "Você pode pedir os critérios e a revisão por uma pessoa da equipe, quando quiser: "
           "é só responder aqui.")

# Fragmentos por critério: o que está claro / o que falta.
CLARO = {
    "produto": "o tipo de empreendimento já está bem definido",
    "local": "você já levantou boas informações sobre a área",
    "documentos": "você já reuniu os documentos da área (não os analisamos)",
    "numeros": "você já tem números organizados de custos e receitas",
    "apresentacao": "você já tem um material para mostrar o projeto",
}
FALTA = {
    "produto": "definir com mais clareza o que será o empreendimento (tipo, público e tamanho)",
    "local": "levantar mais informações sobre a área (tamanho, acesso, entorno e o que limita o uso)",
    "documentos": "reunir e organizar os documentos da área",
    "numeros": "montar os números do projeto: quanto custa abrir, quanto entra e quanto sobra",
    "apresentacao": "reunir o projeto num material simples e organizado para apresentar",
}
# Onde cada ponto é trabalhado na Mini Mentoria (só itens verificados em
# 08-checkouts/ENTREGAVEIS_VERIFICADOS.md; nomes de módulo exatos [NC]).
ONDE = {
    "produto": "as fichas 'Faça agora' e o Dossiê",
    "local": "as fichas 'Faça agora' e o Dossiê",
    "documentos": "as fichas 'Faça agora' e o Dossiê",
    "numeros": "as 2 planilhas em branco e a ficha de Pré-viabilidade (Pilar 6)",
    "apresentacao": "o Kit do Investidor (modelos) e o Dossiê em PDF",
}

ABERTURA = {
    "F1": "Vimos que as informações que você tem ainda são muito preliminares. Isso é normal no começo, e é por aí que se começa.",
    "F2": "Vimos que você já fez os primeiros levantamentos, mas ainda faltam informações importantes.",
    "F3": "Vimos que o seu projeto já está em montagem: várias peças existem, outras ainda estão soltas.",
    "F4": "Vimos que as suas informações já estão bem organizadas. Pode faltar só acabamento.",
}
PROXIMO = {
    "F1": ("Antes de apresentar o seu projeto a potenciais parceiros e investidores, recomendamos que você "
           "estruture melhor {o_que}. Fazemos isso passo a passo na Mini Mentoria de "
           "Estruturação Zion."),
    "F2": ("Antes de apresentar o seu projeto a potenciais parceiros e investidores, o caminho é completar o que "
           "falta e juntar tudo num só lugar. Fazemos isso passo a passo na Mini Mentoria de Estruturação Zion."),
    "F3": ("Você já tem boa parte do caminho. Falta amarrar as peças num projeto único. A Mini Mentoria de "
           "Estruturação Zion organiza isso nas fichas e no Dossiê."),
    "F4": ("Você pode não precisar de tudo. Se quiser, a Mini Mentoria de Estruturação Zion serve para conferir "
           "o que já fez e acertar o formato (Dossiê e Kit do Investidor). A decisão é sua."),
}
PALAVRAS_PROIBIDAS = (
    "você receberá investimento", "voce recebera investimento", "seremos sócios", "seremos socios",
    "garantimos", "garantido", "reunião", "reuniao", "viabilidade financeira", "viável", "inviável",
    "laudo", "aprovado", "reprovado", "valor do seu terreno", "vai render", "retorno garantido",
)


def _validar(resp):
    esperadas = {"situacao"} | set(ORDEM)
    extras = set(resp) - esperadas
    if extras:
        raise ValueError("chaves não aceitas (a regra não usa esses dados): " + ", ".join(sorted(extras)))
    sit = resp.get("situacao")
    if sit not in SITUACOES:
        raise ValueError("situacao inválida: %r" % (sit,))
    for c in ORDEM:
        if sit not in CRITERIOS[c]["aplica"]:
            if resp.get(c) is not None:
                raise ValueError("critério %s não se aplica à situação %s" % (c, sit))
            continue
        if resp.get(c) not in CRITERIOS[c]["opcoes"]:
            raise ValueError("resposta inválida em %s: %r" % (c, resp.get(c)))
    return sit


def faixa_de(nota):
    for lo, hi, cod, nome in FAIXAS:
        if lo <= nota <= hi:
            return cod, nome
    raise ValueError("nota fora de 0-100")


def diagnosticar(resp):
    """Recebe as respostas (dict de códigos) e devolve o diagnóstico (dict)."""
    sit = _validar(resp)
    det, pts, mx = [], 0, 0
    for c in ORDEM:
        cfg = CRITERIOS[c]
        if sit not in cfg["aplica"]:
            det.append({"criterio": c, "nome": cfg["nome"], "aplica": False})
            continue
        p = cfg["opcoes"][resp[c]]
        pts += p
        mx += cfg["max"]
        det.append({"criterio": c, "nome": cfg["nome"], "aplica": True, "resposta": resp[c],
                    "pontos": p, "maximo": cfg["max"]})
    nota = round(100 * pts / mx)
    cod, nome = faixa_de(nota)
    aplic = [d for d in det if d["aplica"]]
    claros = [d["criterio"] for d in aplic if d["pontos"] / d["maximo"] >= 0.7]
    faltas = sorted((d for d in aplic if d["pontos"] / d["maximo"] < 0.7),
                    key=lambda d: (d["pontos"] / d["maximo"], ORDEM.index(d["criterio"])))[:2]
    faltas = [d["criterio"] for d in faltas]
    if claros:
        txt_claro = "O que já está claro: " + "; ".join(CLARO[c] for c in claros) + "."
    else:
        txt_claro = "O que já está claro: você deu o primeiro passo ao nos contar sobre o seu projeto."
    if faltas:
        txt_falta = "O que ainda falta: " + "; ".join(FALTA[c] for c in faltas) + "."
        onde = "; ".join(sorted({ONDE[c] for c in faltas}))
        txt_onde = "Na Mini Mentoria você trabalha isso em: %s." % onde
    else:
        txt_falta = "O que ainda falta: nenhum ponto grande nas perguntas que fizemos."
        txt_onde = ""
    o_que = "a ideia, o projeto e a área" if sit in ("terreno", "hospedagem") else "a ideia e o projeto"
    parecer = " ".join(t for t in (
        "Olá, {nome}! " + ABERTURA[cod], txt_claro, txt_falta, PROXIMO[cod].replace("{o_que}", o_que), txt_onde,
        "Qualquer parceria ou investimento é uma possibilidade, sujeita à análise de quem avalia o projeto, e este diagnóstico não promete nenhum.", LIMITE) if t)
    return {
        "versao_regra": VERSAO,
        "situacao": sit,
        "score": nota,
        "pontos": pts,
        "pontos_maximos": mx,
        "faixa": cod,
        "faixa_nome": nome,
        "criterios": det,
        "mais_fortes": claros,
        "prioridades": faltas,
        "parecer": parecer,
        "limite": LIMITE,
        "revisao_humana": REVISAO,
        "crm": {
            "campos": {"diag_score": nota, "diag_faixa": cod, "diag_situacao": sit,
                       "diag_prioridades": ",".join(faltas), "diag_versao": VERSAO},
            "etiqueta": "DIAG | %s %s" % (cod, nome.upper()),
        },
    }


def explicar(resultado):
    """Texto que a pessoa pode receber se perguntar como a nota foi calculada."""
    linhas = ["Como calculamos (regra %s): somamos pontos por critério e dividimos pelo máximo que se aplica ao seu caso." % resultado["versao_regra"]]
    for d in resultado["criterios"]:
        if d["aplica"]:
            linhas.append("- %s: %d de %d pontos." % (d["nome"], d["pontos"], d["maximo"]))
        else:
            linhas.append("- %s: não se aplica ao seu caso, ficou fora da conta." % d["nome"])
    linhas.append("Nota: %d de 100 (%d de %d pontos). Faixa: %s." % (
        resultado["score"], resultado["pontos"], resultado["pontos_maximos"], resultado["faixa_nome"]))
    linhas.append("Não entram na conta: valor da área, capital, localização, documentos enviados nem dados pessoais.")
    linhas.append(LIMITE)
    linhas.append("Você pode pedir a revisão por uma pessoa da equipe a qualquer momento.")
    return "\n".join(linhas)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            res = diagnosticar(json.load(f))
        print(res["parecer"])
        print()
        print(explicar(res))
    else:
        ex = {"situacao": "terreno", "produto": "varias_ideias", "local": "tamanho_localizacao",
              "documentos": "alguns", "numeros": "estimativa_de_cabeca", "apresentacao": "anotacoes_soltas"}
        print("DADOS FICTÍCIOS")
        print(json.dumps(diagnosticar(ex), ensure_ascii=False, indent=2))

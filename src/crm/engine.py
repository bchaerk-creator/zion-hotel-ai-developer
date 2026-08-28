"""
ZION LEAD SCORE™ e roteamento de oferta.

Cálculo determinístico. Duas ideias governam este módulo:

1. Engajamento vale pouco. Um lead pode curtir todo conteúdo e nunca comprar;
   outro pode não interagir e ter um terreno de alto potencial com capital.
   Fit, ativo, intenção, capacidade e momento pesam mais.

2. Ausência de dado não é nota baixa. Lead sem informação não é lead ruim —
   é lead não qualificado. Por isso o score é calculado apenas sobre as
   dimensões conhecidas, e a confiança reporta o quanto disso se apoia em
   dado real.
"""

from datetime import date
from typing import List, Optional, Tuple

from src.crm.models import (
    DimensaoScore,
    Estagio,
    Lead,
    Objetivo,
    Perfil,
    Porta,
    Roteamento,
    Temperatura,
    Tri,
    ZionLeadScore,
)

# Engajamento tem o menor peso da matriz, por decisão metodológica.
PESOS = {
    "FIT": 0.18,
    "ATIVO": 0.15,
    "CAPITAL": 0.14,
    "URGENCIA": 0.13,
    "PROJETO": 0.12,
    "AUTORIDADE": 0.12,
    "POTENCIAL": 0.11,
    "ENGAGEMENT": 0.05,
}

FIT_POR_PERFIL = {
    Perfil.PROPRIETARIO_TERRENO: 9.0,
    Perfil.DESENVOLVEDOR: 9.0,
    Perfil.POTENCIAL_PARCEIRO: 9.0,
    Perfil.INVESTIDOR: 8.0,
    Perfil.INVESTIDOR_INSTITUCIONAL: 8.0,
    Perfil.OPERADOR: 7.0,
    Perfil.EMPREENDEDOR: 6.0,
    Perfil.ALUNO: 5.0,
    Perfil.PROFISSIONAL: 4.0,
}

PESO_ATIVO = {
    "terreno": 3.5,
    "capital": 3.0,
    "projeto": 1.5,
    "operacao": 1.5,
    "marca": 0.5,
    "experiencia": 0.5,
    "rede": 0.5,
}

ESTAGIO_PROJETO_NOTA = {
    "operacao": 10.0, "operação": 10.0,
    "obra": 9.0,
    "projeto": 8.0,
    "conceito": 5.0,
    "terreno": 3.0,
}


def _dim(nome: str, valor: float, base: str, justificativa: str) -> DimensaoScore:
    return DimensaoScore(
        nome=nome, valor=max(0.0, min(10.0, valor)), peso=PESOS[nome],
        base=base, justificativa=justificativa,
    )


def _fit(lead: Lead) -> DimensaoScore:
    if lead.perfil == Perfil.NAO_CLASSIFICADO:
        return _dim("FIT", 0.0, "desconhecida", "Perfil não classificado.")
    nota = FIT_POR_PERFIL.get(lead.perfil, 5.0)
    return _dim("FIT", nota, "derivada", f"Perfil {lead.perfil.value}.")


def _ativo(lead: Lead) -> DimensaoScore:
    if lead.ativos.conhecidos() == 0:
        return _dim("ATIVO", 0.0, "desconhecida", "Nenhum ativo levantado.")
    possui = lead.ativos.possui()
    nota = min(10.0, sum(PESO_ATIVO.get(a, 0.0) for a in possui) * 10 / 8.0)
    texto = ", ".join(possui) if possui else "nenhum ativo declarado"
    return _dim("ATIVO", nota, "derivada", f"Possui: {texto}.")


def _capital(lead: Lead) -> DimensaoScore:
    valor = lead.financeiro.capital_disponivel_brl or lead.financeiro.faixa_investimento_brl
    if valor is not None:
        if valor >= 10_000_000:
            nota = 10.0
        elif valor >= 2_000_000:
            nota = 9.0
        elif valor >= 500_000:
            nota = 7.0
        elif valor >= 100_000:
            nota = 5.0
        else:
            nota = 3.0
        return _dim("CAPITAL", nota, "informada", f"Capital declarado: R$ {valor:,.0f}.")

    if lead.ativos.capital == Tri.SIM:
        return _dim("CAPITAL", 7.0, "derivada", "Declara possuir capital, sem faixa informada.")
    if lead.ativos.capital == Tri.NAO:
        return _dim("CAPITAL", 2.0, "derivada", "Declara não possuir capital.")
    return _dim("CAPITAL", 0.0, "desconhecida", "Capacidade financeira não levantada.")


def _projeto(lead: Lead) -> DimensaoScore:
    if lead.projeto.estagio:
        chave = lead.projeto.estagio.strip().lower()
        if chave in ESTAGIO_PROJETO_NOTA:
            return _dim(
                "PROJETO", ESTAGIO_PROJETO_NOTA[chave], "informada",
                f"Projeto em estágio de {lead.projeto.estagio}.",
            )
    if lead.ativos.projeto == Tri.SIM:
        return _dim("PROJETO", 6.0, "derivada", "Declara ter projeto, sem estágio informado.")
    if lead.ativos.projeto == Tri.NAO:
        return _dim("PROJETO", 2.0, "derivada", "Não possui projeto.")
    return _dim("PROJETO", 0.0, "desconhecida", "Existência de projeto não levantada.")


def _urgencia(lead: Lead) -> DimensaoScore:
    prazo = lead.projeto.prazo_meses
    if prazo is not None:
        if prazo <= 6:
            nota = 10.0
        elif prazo <= 12:
            nota = 8.0
        elif prazo <= 24:
            nota = 6.0
        else:
            nota = 4.0
        return _dim("URGENCIA", nota, "informada", f"Prazo desejado de {prazo} meses.")

    if lead.objetivo == Objetivo.DESCONHECIDO:
        return _dim("URGENCIA", 0.0, "desconhecida", "Objetivo e prazo não levantados.")
    if lead.objetivo == Objetivo.NAO_SABE:
        return _dim("URGENCIA", 3.0, "derivada", "Não sabe o que fazer — sem necessidade definida.")
    return _dim("URGENCIA", 6.0, "derivada", f"Objetivo declarado: {lead.objetivo.value}.")


def _autoridade(lead: Lead) -> DimensaoScore:
    if lead.e_decisor == Tri.SIM:
        return _dim("AUTORIDADE", 10.0, "informada", "É o decisor.")
    if lead.e_decisor == Tri.NAO:
        return _dim("AUTORIDADE", 3.0, "informada", "Não é o decisor — decisão depende de terceiro.")
    return _dim("AUTORIDADE", 0.0, "desconhecida", "Poder de decisão não levantado.")


def _potencial(lead: Lead) -> DimensaoScore:
    if lead.valor_potencial_brl is not None:
        v = lead.valor_potencial_brl
        nota = 10.0 if v >= 1_000_000 else 8.0 if v >= 300_000 else 6.0 if v >= 50_000 else 4.0
        return _dim("POTENCIAL", nota, "informada", f"Valor potencial de R$ {v:,.0f}.")

    area = lead.terreno.area_ha
    if area is not None:
        nota = 9.0 if area >= 100 else 7.0 if area >= 20 else 5.0 if area >= 5 else 3.0
        return _dim("POTENCIAL", nota, "derivada", f"Terreno de {area:g} ha.")

    if lead.projeto.numero_unidades:
        u = lead.projeto.numero_unidades
        nota = 9.0 if u >= 50 else 7.0 if u >= 20 else 5.0
        return _dim("POTENCIAL", nota, "derivada", f"Projeto de {u} unidades.")

    return _dim("POTENCIAL", 0.0, "desconhecida", "Potencial comercial não dimensionado.")


def _engagement(lead: Lead, referencia: Optional[date] = None) -> DimensaoScore:
    hoje = referencia or date.today()
    n = len(lead.interacoes)
    if n == 0:
        return _dim("ENGAGEMENT", 1.0, "derivada", "Nenhuma interação registrada.")

    dias = None
    if lead.data_ultima_atividade:
        dias = (hoje - lead.data_ultima_atividade).days

    nota = 9.0 if n >= 5 else 6.0 if n >= 2 else 4.0
    if dias is not None and dias > 90:
        nota = max(1.0, nota - 4.0)
    detalhe = f"{n} interação(ões)"
    if dias is not None:
        detalhe += f", última há {dias} dias"
    return _dim("ENGAGEMENT", nota, "derivada", detalhe + ".")


def calcular_score(lead: Lead, referencia: Optional[date] = None) -> ZionLeadScore:
    """Calcula o Zion Lead Score™ e a temperatura do lead."""
    dimensoes = [
        _fit(lead), _ativo(lead), _capital(lead), _urgencia(lead),
        _projeto(lead), _autoridade(lead), _potencial(lead), _engagement(lead, referencia),
    ]

    conhecidas = [d for d in dimensoes if d.base != "desconhecida"]
    peso_conhecido = sum(d.peso for d in conhecidas)

    if peso_conhecido > 0:
        score = sum(d.valor * d.peso for d in conhecidas) / peso_conhecido
    else:
        score = 0.0

    confianca = peso_conhecido  # os pesos somam 1.0
    temperatura = _temperatura(lead, score, confianca, dimensoes)
    alertas = _alertas(lead, dimensoes, confianca)

    return ZionLeadScore(
        lead_id=lead.id,
        score=round(score, 2),
        confianca=round(confianca, 2),
        temperatura=temperatura,
        dimensoes=dimensoes,
        alertas=alertas,
    )


def _temperatura(
    lead: Lead, score: float, confianca: float, dimensoes: List[DimensaoScore]
) -> Temperatura:
    """Temperatura por situação comercial real, não por engajamento."""
    valores = {d.nome: d.valor for d in dimensoes}
    tem_projeto = lead.ativos.projeto == Tri.SIM or valores["PROJETO"] >= 8

    if tem_projeto and lead.estagio in (Estagio.OFERTA, Estagio.NEGOCIACAO, Estagio.DECISAO):
        return Temperatura.OPORTUNIDADE

    # Quente exige problema, intenção, capacidade, urgência e autoridade juntos.
    if (
        score >= 7
        and confianca >= 0.5
        and valores["AUTORIDADE"] >= 7
        and valores["URGENCIA"] >= 6
        and valores["CAPITAL"] >= 5
    ):
        return Temperatura.QUENTE

    if score >= 5 and lead.objetivo not in (Objetivo.DESCONHECIDO,):
        return Temperatura.MORNO

    return Temperatura.FRIO


def _alertas(lead: Lead, dimensoes: List[DimensaoScore], confianca: float) -> List[str]:
    alertas = []
    desconhecidas = [d.nome for d in dimensoes if d.base == "desconhecida"]

    if confianca < 0.5:
        alertas.append(
            f"Confiança baixa ({confianca * 100:.0f}%): o score se apoia em pouca "
            f"informação. Não descartar o lead — qualificar. Falta: {', '.join(desconhecidas)}."
        )
    if lead.ativos.terreno == Tri.SIM and lead.terreno.area_ha is None:
        alertas.append("Possui terreno mas a área não foi levantada — dimensão do potencial cega.")
    if lead.e_decisor == Tri.DESCONHECIDO:
        alertas.append("Não se sabe se fala com o decisor. Confirmar antes de avançar para oferta.")
    if lead.estagio not in (Estagio.GANHO, Estagio.PERDIDO) and lead.proxima_acao is None:
        alertas.append("Lead aberto sem próxima ação definida.")
    return alertas


# ---------------------------------------------------------------------------
# Roteamento de oferta
# ---------------------------------------------------------------------------

PERGUNTAS_QUALIFICACAO = {
    Perfil.PROPRIETARIO_TERRENO: [
        "Onde fica?", "Qual o tamanho?", "A propriedade é sua?", "Possui documentação?",
        "Possui infraestrutura?", "Já existe alguma construção?", "O que gostaria de fazer?",
        "Já fez estudo?", "Quanto pretende investir?", "Pretende investir sozinho?",
        "Qual prazo?", "Quer desenvolver sozinho ou com a Zion?",
    ],
    Perfil.INVESTIDOR: [
        "Qual perfil de investimento?", "Qual faixa de capital?", "Busca renda ou valorização?",
        "Qual horizonte?", "Já investiu em hotelaria?",
        "Busca operação pronta ou desenvolvimento?", "Qual região?", "Qual retorno esperado?",
        "Qual nível de risco aceita?", "Quer investir diretamente ou através de estrutura?",
    ],
    Perfil.OPERADOR: [
        "Quantas unidades?", "Ocupação atual?", "Diária média?", "Receita?",
        "Canal de vendas?", "Nota e reputação?", "Principal problema?",
        "Possui espaço para expansão?", "Quer reposicionar?", "Quer aumentar receita?",
        "Quer vender?", "Quer profissionalizar a gestão?",
    ],
    Perfil.ALUNO: [
        "Possui terreno?", "Já possui projeto?", "O que pretende desenvolver?",
        "Quanto já sabe?", "O que está impedindo?", "Quer aprender ou delegar?",
        "Tem tempo para executar?",
        "Está disposto a construir o projeto durante a mentoria?", "Qual o prazo?",
        "Qual resultado deseja?",
    ],
}
PERGUNTAS_QUALIFICACAO[Perfil.INVESTIDOR_INSTITUCIONAL] = PERGUNTAS_QUALIFICACAO[Perfil.INVESTIDOR]


def rotear(lead: Lead, score: ZionLeadScore) -> Roteamento:
    """
    Define a porta de entrada e o próximo passo lógico.

    A regra que manda é a de não empurrar venda: se o lead ainda não sabe o
    que construir, não se vende bubble; se não sabe se o terreno é viável,
    não se vende desenvolvimento; se não tem projeto, não se vende captação.
    Vende-se sempre o próximo passo lógico.
    """
    tem_terreno = lead.ativos.terreno == Tri.SIM
    tem_capital = lead.ativos.capital == Tri.SIM
    tem_projeto = lead.ativos.projeto == Tri.SIM
    tem_operacao = lead.ativos.operacao == Tri.SIM
    obj = lead.objetivo

    nao_ofertar = _bloqueios(lead, tem_projeto, tem_terreno)
    perguntas = PERGUNTAS_QUALIFICACAO.get(lead.perfil, [])

    def resultado(porta: Porta, justificativa: str, proximo: str) -> Roteamento:
        return Roteamento(
            lead_id=lead.id, porta=porta, justificativa=justificativa,
            proximo_passo_logico=proximo, nao_ofertar=nao_ofertar,
            perguntas_de_qualificacao=perguntas,
        )

    # Incerteza declarada é sempre diagnóstico, independente do ativo.
    if obj == Objetivo.NAO_SABE:
        return resultado(
            Porta.DIAGNOSTICO,
            "O lead declarou que não sabe o que fazer. Incerteza se resolve com diagnóstico.",
            "Oferecer Diagnóstico Territorial para responder 'o que este território sustenta?'.",
        )

    if obj == Objetivo.PARCERIA:
        if tem_terreno or tem_capital or tem_operacao:
            return resultado(
                Porta.PARCERIA,
                "Busca parceria e traz ativo complementar — existe fit estratégico possível.",
                "Sessão de fit estratégico antes de qualquer proposta societária.",
            )
        return resultado(
            Porta.DIAGNOSTICO,
            "Busca parceria sem ativo complementar identificado. Parceria só com fit real.",
            "Qualificar o que o lead traz para a mesa antes de discutir sociedade.",
        )

    if tem_projeto and obj == Objetivo.CAPITAL:
        return resultado(
            Porta.CAPITAL,
            "Existe projeto concreto e necessidade declarada de recursos.",
            "Revisar a viabilidade e estruturar o dossiê para banco e investidor.",
        )

    if tem_capital and obj == Objetivo.INVESTIR:
        return resultado(
            Porta.INVESTIMENTO,
            "Possui capital e busca oportunidade.",
            "Apresentar oportunidades do pipeline compatíveis com o perfil de risco.",
        )

    if tem_operacao and obj in (Objetivo.OPERAR, Objetivo.DESENVOLVER):
        return resultado(
            Porta.MANAGEMENT,
            "Já opera e busca melhorar desempenho ou profissionalizar a gestão.",
            "Diagnóstico da operação atual antes de propor gestão ou reposicionamento.",
        )

    if tem_terreno:
        if obj == Objetivo.APRENDER:
            return resultado(
                Porta.MENTORIA,
                "Tem terreno e quer conduzir o próprio projeto.",
                "Oferecer a mentoria, com o projeto do próprio aluno como entregável.",
            )
        if obj == Objetivo.DESENVOLVER:
            return resultado(
                Porta.DESENVOLVIMENTO,
                "Tem terreno e quer delegar o desenvolvimento.",
                "Diagnóstico Territorial como porta de entrada do escopo de desenvolvimento.",
            )
        return resultado(
            Porta.DIAGNOSTICO,
            "Tem terreno e a intenção ainda não está definida.",
            "Diagnóstico Territorial para revelar o que o terreno sustenta.",
        )

    if obj == Objetivo.COMPRAR:
        if tem_projeto:
            return resultado(
                Porta.PRODUTO,
                "Quer comprar e já tem projeto definido — sabe o que vai construir.",
                "Especificação técnica das unidades e proposta comercial.",
            )
        return resultado(
            Porta.DIAGNOSTICO,
            "Quer comprar mas ainda não tem projeto definido. Vender unidade agora seria "
            "empurrar produto para um destino que não existe.",
            "Diagnóstico primeiro. A unidade vem depois de saber o que construir.",
        )

    if obj == Objetivo.APRENDER:
        return resultado(
            Porta.MENTORIA,
            "Busca conhecimento para desenvolver o próprio projeto.",
            "Oferecer a formação e qualificar se há terreno em vista.",
        )

    return resultado(
        Porta.NUTRICAO,
        "Informação insuficiente para rotear com responsabilidade.",
        "Aplicar o roteiro de qualificação do perfil antes de qualquer oferta.",
    )


def _bloqueios(lead: Lead, tem_projeto: bool, tem_terreno: bool) -> List[str]:
    """O que NÃO ofertar agora — a regra de não empurrar venda, explicitada."""
    bloqueios = []
    if not tem_projeto:
        bloqueios.append(
            "Produto (bubbles e cabanas): o lead ainda não sabe o que construir."
        )
        bloqueios.append(
            "Capital: não existe projeto estruturado para levar a banco ou investidor."
        )
    if not tem_terreno and lead.perfil == Perfil.PROPRIETARIO_TERRENO:
        bloqueios.append("Desenvolvimento: perfil declara terreno, mas o ativo não foi confirmado.")
    if lead.estagio in (Estagio.NOVO_LEAD, Estagio.CONTATO_INICIADO):
        bloqueios.append(
            "Qualquer proposta comercial fechada: o lead ainda não passou por qualificação."
        )
    return bloqueios


def qualificar(lead: Lead, referencia: Optional[date] = None) -> Tuple[ZionLeadScore, Roteamento]:
    """QUALIFICAR LEAD — score, temperatura e roteamento em uma chamada."""
    score = calcular_score(lead, referencia)
    return score, rotear(lead, score)

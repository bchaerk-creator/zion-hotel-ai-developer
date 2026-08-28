"""
Métricas, gate de campanha e estatística de decisão.

Duas regras do método viram código aqui:

1. Nunca otimizar custo por lead. Otimizar custo por cliente e, no fim,
   receita gerada por real investido. Por isso o CPQO — custo por oportunidade
   qualificada — é calculado com o mesmo destaque que o CPL.

2. Nunca aplicar threshold arbitrário sem considerar volume estatístico.
   Toda decisão de pausar, escalar ou declarar vencedor passa por um teste
   com o volume real, não por um número redondo escolhido a olho.
"""

import math
from typing import List, Optional, Tuple

from src.traffic.models import (
    BriefingCampanha,
    Campanha,
    Metricas,
    MetricasCampanha,
    ResultadoGate,
)

# Volume abaixo do qual nenhuma taxa é confiável o suficiente para decidir.
MINIMO_IMPRESSOES = 1_000
MINIMO_CLIQUES = 100
MINIMO_LEADS = 25
MINIMO_CONVERSOES_PARA_CPA = 10


def _div(numerador: float, denominador: float) -> Optional[float]:
    """Divisão que devolve None em vez de zero falso quando não há denominador."""
    return numerador / denominador if denominador else None


# ---------------------------------------------------------------------------
# Métricas
# ---------------------------------------------------------------------------

def calcular_metricas(m: MetricasCampanha, margem: Optional[float] = None) -> Metricas:
    """
    Deriva a cadeia inteira de métricas dos dados brutos.

    Métrica sem denominador vira None, nunca zero: 'nenhuma venda' e 'nenhum
    dado' são coisas diferentes e não podem virar o mesmo número.
    """
    investimento = m.investimento_brl
    receita = m.receita_brl

    lucro = receita * margem if margem is not None else None
    if lucro is not None:
        lucro -= investimento

    return Metricas(
        investimento_brl=investimento,
        cpm_brl=_div(investimento * 1000, m.impressoes),
        ctr=_div(m.cliques, m.impressoes),
        cpc_brl=_div(investimento, m.cliques),
        taxa_conversao_pagina=_div(m.leads, m.visitas_pagina or m.cliques),
        cpl_brl=_div(investimento, m.leads),
        taxa_qualificacao=_div(m.leads_qualificados, m.leads),
        cpql_brl=_div(investimento, m.leads_qualificados),
        cpqo_brl=_div(investimento, m.oportunidades),
        taxa_fechamento=_div(m.vendas, m.oportunidades),
        cac_brl=_div(investimento, m.vendas),
        receita_brl=receita,
        roas=_div(receita, investimento),
        lucro_bruto_brl=lucro,
    )


def agregar(campanhas: List[Campanha]) -> MetricasCampanha:
    """Soma os dados brutos de várias campanhas."""
    total = MetricasCampanha()
    for c in campanhas:
        m = c.metricas
        total.investimento_brl += m.investimento_brl
        total.impressoes += m.impressoes
        total.cliques += m.cliques
        total.visitas_pagina += m.visitas_pagina
        total.leads += m.leads
        total.leads_qualificados += m.leads_qualificados
        total.oportunidades += m.oportunidades
        total.vendas += m.vendas
        total.receita_brl += m.receita_brl
    return total


# ---------------------------------------------------------------------------
# Gate — antes de criar qualquer campanha
# ---------------------------------------------------------------------------

PERGUNTAS_OBRIGATORIAS = {
    "o_que_vendemos": "O que estamos vendendo?",
    "para_quem": "Para quem?",
    "qual_problema": "Qual problema?",
    "qual_desejo": "Qual desejo?",
    "qual_transformacao": "Qual transformação?",
    "qual_oferta": "Qual oferta?",
    "qual_preco_brl": "Qual preço?",
    "qual_funil": "Qual funil?",
    "qual_evento_conversao": "Qual evento de conversão?",
    "meta_receita_brl": "Qual meta financeira?",
}


def avaliar_gate(campanha: Campanha) -> ResultadoGate:
    """
    Verifica se a campanha pode existir.

    Sem as dez respostas, não se cria campanha. Não é burocracia: cada
    pergunta sem resposta é uma decisão que vai ser tomada por acaso depois,
    com dinheiro rodando.
    """
    briefing: BriefingCampanha = campanha.briefing
    sem_resposta = [
        pergunta
        for campo, pergunta in PERGUNTAS_OBRIGATORIAS.items()
        if getattr(briefing, campo, None) in (None, "")
    ]

    pendencias: List[str] = []
    if not campanha.evento_conversao:
        pendencias.append("Evento de conversão não configurado — sem ele não há otimização possível.")
    if not campanha.utm_campaign:
        pendencias.append(
            "Sem UTM definida — a venda não poderá ser atribuída à campanha no CRM."
        )
    if not campanha.landing_page and campanha.canal.value.startswith(("meta", "google")):
        pendencias.append("Destino não definido: nenhuma landing page ou canal de captura informado.")
    if campanha.metas.cpqo_alvo_brl is None and campanha.metas.cac_alvo_brl is None:
        pendencias.append(
            "Nenhuma meta de CAC ou de custo por oportunidade qualificada — "
            "a campanha não tem contra o que ser julgada."
        )
    if not campanha.criativos:
        pendencias.append("Nenhum criativo cadastrado.")
    else:
        sem_funcao = [c.id for c in campanha.criativos if c.hook in (None, "")]
        if sem_funcao:
            pendencias.append(
                f"Criativos sem hook declarado: {', '.join(sem_funcao)}."
            )

    liberada = not sem_resposta and not pendencias
    if liberada:
        veredito = "Liberada. As dez respostas existem e a estrutura de medição está de pé."
    elif sem_resposta:
        veredito = (
            f"NÃO CRIAR CAMPANHA AINDA. {len(sem_resposta)} das dez perguntas "
            f"obrigatórias estão sem resposta."
        )
    else:
        veredito = (
            f"Briefing completo, mas há {len(pendencias)} pendência(s) de estrutura. "
            f"Resolver antes de subir orçamento."
        )

    return ResultadoGate(
        campanha_id=campanha.id,
        liberada=liberada,
        perguntas_sem_resposta=sem_resposta,
        pendencias_estruturais=pendencias,
        veredito=veredito,
    )


# ---------------------------------------------------------------------------
# Estatística de decisão
# ---------------------------------------------------------------------------

def _phi(x: float) -> float:
    """Distribuição normal acumulada."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def prob_zero_conversoes(tentativas: int, taxa_esperada: float) -> float:
    """
    Probabilidade de observar zero conversões se a campanha fosse tão boa
    quanto a referência.

    É o teste correto para 'gastei e não converteu': se a probabilidade for
    baixa, o zero é evidência real de problema. Se for alta, o zero ainda é
    ruído e pausar seria decisão por impaciência.
    """
    if tentativas <= 0 or not 0 < taxa_esperada < 1:
        return 1.0
    return (1 - taxa_esperada) ** tentativas


def comparar_proporcoes(
    sucessos_a: int, total_a: int, sucessos_b: int, total_b: int
) -> Tuple[Optional[float], str]:
    """
    Teste z de duas proporções. Devolve o p-valor e a leitura em português.

    Serve para declarar vencedor de teste A/B sem inventar: dois criativos com
    CTR diferente podem ser o mesmo criativo com sorte diferente.
    """
    if total_a <= 0 or total_b <= 0:
        return None, "Sem volume em um dos braços — nada a comparar."

    p_a = sucessos_a / total_a
    p_b = sucessos_b / total_b
    p_pool = (sucessos_a + sucessos_b) / (total_a + total_b)

    if p_pool in (0.0, 1.0):
        return None, "Nenhuma variação observada — impossível distinguir os braços."

    erro = math.sqrt(p_pool * (1 - p_pool) * (1 / total_a + 1 / total_b))
    if erro == 0:
        return None, "Erro padrão nulo — volume insuficiente."

    z = (p_a - p_b) / erro
    p_valor = 2 * (1 - _phi(abs(z)))

    if p_valor < 0.05:
        vencedor = "A" if p_a > p_b else "B"
        leitura = (
            f"Diferença significativa (p={p_valor:.3f}): {vencedor} é melhor. "
            f"{p_a:.2%} contra {p_b:.2%}."
        )
    else:
        leitura = (
            f"Diferença não significativa (p={p_valor:.3f}): {p_a:.2%} contra "
            f"{p_b:.2%} pode ser variação aleatória. Não declarar vencedor ainda."
        )
    return p_valor, leitura


def volume_suficiente(m: MetricasCampanha) -> Tuple[bool, str]:
    """
    A campanha já produziu dado suficiente para ser julgada?

    Antes disso, qualquer decisão de pausar ou escalar é chute com aparência
    de análise.
    """
    faltas = []
    if m.impressoes < MINIMO_IMPRESSOES:
        faltas.append(f"{m.impressoes} impressões (mínimo {MINIMO_IMPRESSOES})")
    if m.cliques < MINIMO_CLIQUES:
        faltas.append(f"{m.cliques} cliques (mínimo {MINIMO_CLIQUES})")

    if faltas:
        return False, "Volume insuficiente para julgar: " + ", ".join(faltas) + "."
    if m.leads < MINIMO_LEADS:
        return False, (
            f"Volume de topo suficiente, mas apenas {m.leads} leads "
            f"(mínimo {MINIMO_LEADS}) para julgar qualidade e conversão."
        )
    return True, "Volume suficiente para decisão."

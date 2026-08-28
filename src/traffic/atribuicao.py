"""
Feedback loop entre tráfego e CRM.

Responde à pergunta que o relatório de plataforma nunca responde:

    qual campanha gerou os clientes — não qual gerou mais leads.

A plataforma de anúncios sabe quanto custou o lead. Só o CRM sabe se aquele
lead virou negócio. Cruzar os dois é o que transforma custo por lead em custo
por cliente, e é o único jeito de saber onde o dinheiro realmente rendeu.
"""

from typing import Dict, List, Optional

from src.crm.engine import calcular_score
from src.crm.models import BaseComercial, Estagio, Lead, Temperatura
from src.traffic.models import AtribuicaoCampanha, Campanha, ContaTrafego


def _num(valor: float, casas: int = 0) -> str:
    """Formata número no padrão brasileiro."""
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "§").replace(".", ",").replace("§", ".")

ESTAGIOS_OPORTUNIDADE = (
    Estagio.OFERTA, Estagio.NEGOCIACAO, Estagio.DECISAO, Estagio.GANHO,
)
SCORE_MINIMO_QUALIFICADO = 6.0


def _div(numerador: float, denominador: float) -> Optional[float]:
    return numerador / denominador if denominador else None


def _classificar(leads: List[Lead], data_referencia=None) -> Dict[str, float]:
    """Conta leads, qualificados, oportunidades, clientes e receita realizada."""
    qualificados = oportunidades = clientes = 0
    receita = 0.0

    for lead in leads:
        score = calcular_score(lead, data_referencia)
        if score.score >= SCORE_MINIMO_QUALIFICADO:
            qualificados += 1
        if lead.estagio in ESTAGIOS_OPORTUNIDADE or score.temperatura == Temperatura.OPORTUNIDADE:
            oportunidades += 1
        if lead.estagio == Estagio.GANHO:
            clientes += 1
            receita += lead.valor_potencial_brl or 0.0

    return {
        "leads": len(leads),
        "qualificados": qualificados,
        "oportunidades": oportunidades,
        "clientes": clientes,
        "receita": receita,
    }


def atribuir(
    conta: ContaTrafego, base: BaseComercial
) -> List[AtribuicaoCampanha]:
    """
    Cruza campanhas com a base comercial pela UTM.

    Campanha sem UTM não pode ser atribuída — e isso aparece como zero
    explícito, não como campanha ausente do relatório.
    """
    referencia = base.data_referencia or conta.data_referencia
    por_utm: Dict[str, List[Lead]] = {}
    for lead in base.leads:
        if lead.utm_campaign:
            por_utm.setdefault(lead.utm_campaign, []).append(lead)

    resultados: List[AtribuicaoCampanha] = []
    for campanha in conta.campanhas:
        leads = por_utm.get(campanha.utm_campaign or "", [])
        contagem = _classificar(leads, referencia)
        investimento = campanha.metricas.investimento_brl

        resultados.append(AtribuicaoCampanha(
            campanha_id=campanha.id, nome=campanha.nome, canal=campanha.canal,
            investimento_brl=investimento,
            leads=int(contagem["leads"]),
            qualificados=int(contagem["qualificados"]),
            oportunidades=int(contagem["oportunidades"]),
            clientes=int(contagem["clientes"]),
            receita_brl=contagem["receita"],
            cpl_brl=_div(investimento, contagem["leads"]),
            cpqo_brl=_div(investimento, contagem["oportunidades"]),
            cac_brl=_div(investimento, contagem["clientes"]),
            roas=_div(contagem["receita"], investimento),
        ))

    _rankear(resultados)
    return resultados


def _rankear(resultados: List[AtribuicaoCampanha]) -> None:
    """
    Ordena por leads e por receita, e marca onde os dois rankings discordam.

    A divergência é o achado mais útil do relatório: a campanha que enche o
    CRM raramente é a que paga a conta.
    """
    por_leads = sorted(resultados, key=lambda r: r.leads, reverse=True)
    for i, r in enumerate(por_leads, start=1):
        r.ranking_por_leads = i

    por_receita = sorted(resultados, key=lambda r: r.receita_brl, reverse=True)
    for i, r in enumerate(por_receita, start=1):
        r.ranking_por_receita = i

    for r in resultados:
        r.divergencia_de_ranking = abs(r.ranking_por_leads - r.ranking_por_receita) >= 2


def leitura_da_atribuicao(
    resultados: List[AtribuicaoCampanha],
    conta: Optional[ContaTrafego] = None,
) -> List[str]:
    """Traduz a atribuição em observações acionáveis."""
    observacoes: List[str] = []
    if not resultados:
        return observacoes

    # Diferença grande entre o lead que a plataforma reporta e o lead que chega
    # ao CRM é rastreamento quebrado, não campanha ruim.
    if conta is not None:
        por_id = {c.id: c for c in conta.campanhas}
        for r in resultados:
            campanha = por_id.get(r.campanha_id)
            if campanha is None:
                continue
            reportados = campanha.metricas.leads
            if reportados >= 20 and r.leads < reportados * 0.5:
                observacoes.append(
                    f"{r.nome}: a plataforma reporta {reportados} leads e o CRM tem "
                    f"{r.leads} atribuído(s) a esta campanha. Antes de qualquer conclusão "
                    f"sobre qualidade, corrigir a passagem de UTM — a maior parte do "
                    f"resultado não está sendo medida."
                )

    com_receita = [r for r in resultados if r.receita_brl > 0]
    sem_atribuicao = [r for r in resultados if r.leads == 0 and r.investimento_brl > 0]

    if sem_atribuicao:
        observacoes.append(
            f"{len(sem_atribuicao)} campanha(s) com investimento e nenhum lead atribuído no CRM: "
            + ", ".join(r.campanha_id for r in sem_atribuicao)
            + ". Ou a UTM não está chegando ao CRM, ou a campanha não gerou nada. "
            "Verificar rastreamento antes de julgar a campanha."
        )

    if not com_receita:
        observacoes.append(
            "Nenhuma campanha tem receita atribuída. Sem isso é impossível saber qual "
            "anúncio gerou cliente — só qual gerou volume."
        )
        return observacoes

    campeao_leads = min(resultados, key=lambda r: r.ranking_por_leads)
    campeao_receita = min(resultados, key=lambda r: r.ranking_por_receita)

    if campeao_leads.campanha_id != campeao_receita.campanha_id:
        observacoes.append(
            f"A campanha que mais gera leads ({campeao_leads.nome}, {campeao_leads.leads} leads) "
            f"não é a que gera receita. Quem paga a conta é {campeao_receita.nome}: "
            f"{campeao_receita.clientes} cliente(s) e R$ {_num(campeao_receita.receita_brl)} "
            f"de receita. Otimizar por custo por lead teria escalado a campanha errada."
        )

    divergentes = [r for r in resultados if r.divergencia_de_ranking]
    for r in divergentes:
        if r.ranking_por_leads < r.ranking_por_receita:
            observacoes.append(
                f"{r.nome}: {r.ranking_por_leads}º em volume de leads, mas "
                f"{r.ranking_por_receita}º em receita. Lead barato que não converte — "
                f"não escalar sem corrigir a qualidade."
            )
        else:
            observacoes.append(
                f"{r.nome}: apenas {r.ranking_por_leads}º em leads, mas "
                f"{r.ranking_por_receita}º em receita. Lead caro e bom — "
                f"candidata a mais orçamento."
            )

    return observacoes

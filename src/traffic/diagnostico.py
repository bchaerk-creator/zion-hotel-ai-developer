"""
Diagnóstico de campanha e decisão de otimização.

Regra que estrutura o módulo: nunca otimizar a última etapa sem verificar as
anteriores. A cadeia é percorrida em ordem — público, criativo, clique,
página, lead, qualificação, oferta, venda — e o gargalo é o PRIMEIRO ponto
que quebra, não o mais visível.

Poucas vendas raramente é problema de venda. Quase sempre é consequência de
algo que quebrou antes.
"""

from typing import Dict, List, Optional

from src.traffic.metricas import (
    MINIMO_CONVERSOES_PARA_CPA,
    calcular_metricas,
    prob_zero_conversoes,
    volume_suficiente,
)
from src.traffic.models import (
    AchadoDiagnostico,
    Campanha,
    Canal,
    DecisaoOtimizacao,
    DiagnosticoCampanha,
    EtapaCadeia,
    Metricas,
)

# Referências de mercado, não benchmarks Zion. Servem para levantar suspeita,
# não para provar nada — e devem ser recalibradas com o histórico da conta.
LIMIARES_CTR: Dict[Canal, float] = {
    Canal.META: 0.008,
    Canal.GOOGLE_SEARCH: 0.020,
    Canal.GOOGLE_PMAX: 0.006,
    Canal.GOOGLE_DISPLAY: 0.003,
    Canal.YOUTUBE: 0.004,
}
LIMIAR_CONVERSAO_PAGINA = 0.10
LIMIAR_QUALIFICACAO = 0.20
LIMIAR_OPORTUNIDADE = 0.30
LIMIAR_FECHAMENTO = 0.15


def diagnosticar(campanha: Campanha, margem: Optional[float] = None) -> DiagnosticoCampanha:
    """Percorre a cadeia em ordem e devolve o primeiro ponto que quebra."""
    m = campanha.metricas
    metricas = calcular_metricas(m, margem)
    suficiente, leitura_volume = volume_suficiente(m)

    achados: List[AchadoDiagnostico] = []

    # 02 CRIATIVO — CTR baixo é problema de hook, antes de ser de leilão.
    limiar_ctr = LIMIARES_CTR.get(campanha.canal, 0.008)
    if metricas.ctr is not None and m.impressoes >= 1_000:
        if metricas.ctr < limiar_ctr:
            achados.append(AchadoDiagnostico(
                etapa=EtapaCadeia.CRIATIVO,
                gravidade="alta",
                sintoma=f"CTR de {metricas.ctr:.2%}, abaixo da referência de {limiar_ctr:.2%}.",
                causa_provavel=(
                    "Hook, criativo ou mensagem não param a atenção do público escolhido. "
                    "CPC alto, quando existir, é consequência disso e não causa própria."
                ),
                acao="Testar novos hooks e ângulos antes de mexer em lance ou orçamento.",
                confianca_estatistica=f"{m.impressoes:,} impressões — volume suficiente para o CTR.",
            ))

    # 04 PÁGINA — muitos cliques e poucas conversões.
    base_pagina = m.visitas_pagina or m.cliques
    if metricas.taxa_conversao_pagina is not None and base_pagina >= 100:
        if metricas.taxa_conversao_pagina < LIMIAR_CONVERSAO_PAGINA:
            achados.append(AchadoDiagnostico(
                etapa=EtapaCadeia.PAGINA,
                gravidade="alta",
                sintoma=(
                    f"{base_pagina} cliques geraram {m.leads} leads "
                    f"({metricas.taxa_conversao_pagina:.1%} de conversão)."
                ),
                causa_provavel=(
                    "O anúncio entrega o clique e a página não converte: headline, promessa, "
                    "prova, oferta, CTA ou experiência mobile."
                ),
                acao=(
                    "Auditar a landing page antes de aumentar investimento. "
                    "Tráfego para página que não converte é dinheiro comprando ruído."
                ),
                confianca_estatistica=f"{base_pagina} cliques — volume suficiente para a taxa.",
            ))

    # 06 QUALIFICAÇÃO — muitos leads e poucas oportunidades.
    if metricas.taxa_qualificacao is not None and m.leads >= 25:
        if metricas.taxa_qualificacao < LIMIAR_QUALIFICACAO:
            achados.append(AchadoDiagnostico(
                etapa=EtapaCadeia.QUALIFICACAO,
                gravidade="alta",
                sintoma=(
                    f"{m.leads} leads geraram apenas {m.leads_qualificados} qualificados "
                    f"({metricas.taxa_qualificacao:.1%})."
                ),
                causa_provavel=(
                    "Público errado ou promessa que atrai quem não tem território, capital "
                    "ou intenção. Lead barato que não qualifica é custo, não ativo."
                ),
                acao=(
                    "Revisar segmentação e a promessa do anúncio. Não escalar: "
                    "escalar aqui multiplica o volume de lead errado."
                ),
                confianca_estatistica=f"{m.leads} leads — volume suficiente para a taxa.",
            ))

    taxa_oportunidade = (
        m.oportunidades / m.leads_qualificados if m.leads_qualificados else None
    )
    if taxa_oportunidade is not None and m.leads_qualificados >= 20:
        if taxa_oportunidade < LIMIAR_OPORTUNIDADE:
            achados.append(AchadoDiagnostico(
                etapa=EtapaCadeia.QUALIFICACAO,
                gravidade="media",
                sintoma=(
                    f"{m.leads_qualificados} qualificados viraram {m.oportunidades} "
                    f"oportunidades ({taxa_oportunidade:.1%})."
                ),
                causa_provavel=(
                    "O lead tem perfil mas não avança: pode ser timing, oferta errada para "
                    "o estágio ou falha no diagnóstico comercial."
                ),
                acao="Revisar o roteiro de qualificação e a oferta apresentada nesse ponto.",
                confianca_estatistica=f"{m.leads_qualificados} qualificados.",
            ))

    # 08 VENDA — muitas oportunidades e poucas vendas.
    if metricas.taxa_fechamento is not None and m.oportunidades >= 10:
        if metricas.taxa_fechamento < LIMIAR_FECHAMENTO:
            achados.append(AchadoDiagnostico(
                etapa=EtapaCadeia.VENDA,
                gravidade="alta",
                sintoma=(
                    f"{m.oportunidades} oportunidades geraram {m.vendas} vendas "
                    f"({metricas.taxa_fechamento:.1%})."
                ),
                causa_provavel="Oferta, preço, processo comercial ou fechamento.",
                acao=(
                    "Investigar o comercial, não a campanha. O tráfego entregou "
                    "oportunidade — o problema está depois dele."
                ),
                confianca_estatistica=f"{m.oportunidades} oportunidades.",
            ))

    # 05 LEAD — gastou e não converteu, avaliado por probabilidade, não por palpite.
    if m.leads == 0 and m.cliques > 0:
        taxa_referencia = LIMIAR_CONVERSAO_PAGINA
        p = prob_zero_conversoes(m.cliques, taxa_referencia)
        if p < 0.05:
            achados.append(AchadoDiagnostico(
                etapa=EtapaCadeia.LEAD,
                gravidade="bloqueante",
                sintoma=f"{m.cliques} cliques e nenhum lead, com R$ {m.investimento_brl:,.0f} gastos.",
                causa_provavel="Página quebrada, evento de conversão mal configurado ou oferta rejeitada.",
                acao="Verificar rastreamento e página antes de pausar. Se ambos estiverem certos, pausar.",
                confianca_estatistica=(
                    f"Probabilidade de zero leads em {m.cliques} cliques, se a conversão fosse "
                    f"{taxa_referencia:.0%}: {p:.1%}. O zero não é ruído."
                ),
            ))
        else:
            achados.append(AchadoDiagnostico(
                etapa=EtapaCadeia.LEAD,
                gravidade="media",
                sintoma=f"{m.cliques} cliques e nenhum lead ainda.",
                causa_provavel="Volume ainda pequeno para concluir qualquer coisa.",
                acao="Aguardar volume antes de decidir. Pausar agora seria decisão por impaciência.",
                confianca_estatistica=(
                    f"Probabilidade de zero leads em {m.cliques} cliques, se a conversão fosse "
                    f"{taxa_referencia:.0%}: {p:.1%}. Ainda compatível com acaso."
                ),
            ))

    # O gargalo é o primeiro ponto da cadeia que quebra.
    ordem = list(EtapaCadeia)
    achados.sort(key=lambda a: ordem.index(a.etapa))
    gargalo = achados[0].etapa if achados else None

    if not suficiente:
        leitura = leitura_volume
    elif gargalo is None:
        leitura = "Cadeia sem gargalo detectado nos limiares atuais."
    else:
        leitura = (
            f"Gargalo em {gargalo.value}. Corrigir aqui antes de mexer em qualquer "
            f"etapa posterior — o que vem depois é sintoma, não causa."
        )

    return DiagnosticoCampanha(
        campanha_id=campanha.id, nome=campanha.nome, metricas=metricas,
        gargalo=gargalo, achados=achados,
        volume_suficiente=suficiente, leitura=leitura,
    )


# ---------------------------------------------------------------------------
# Decisão de otimização
# ---------------------------------------------------------------------------

def decidir(
    campanha: Campanha, diagnostico: DiagnosticoCampanha, margem: Optional[float] = None
) -> DecisaoOtimizacao:
    """
    Escalar, manter, investigar, pausar ou aguardar volume.

    Nunca por emoção e nunca só porque 'está vendendo': escalar exige CAC
    dentro da meta, volume estatístico e qualidade confirmada ao longo da
    cadeia inteira.
    """
    m = campanha.metricas
    met = diagnostico.metricas
    metas = campanha.metas
    bloqueios: List[str] = []

    if not diagnostico.volume_suficiente:
        return DecisaoOtimizacao(
            campanha_id=campanha.id, acao="aguardar_volume",
            justificativa="Ainda não há dado suficiente para decidir com honestidade.",
            evidencia=diagnostico.leitura,
        )

    bloqueante = next((a for a in diagnostico.achados if a.gravidade == "bloqueante"), None)
    if bloqueante:
        return DecisaoOtimizacao(
            campanha_id=campanha.id, acao="pausar",
            justificativa=bloqueante.acao, evidencia=bloqueante.confianca_estatistica,
        )

    # CPL bom com CPQO ruim é a armadilha clássica: barato e inútil.
    cpl_ok = (
        met.cpl_brl is not None and metas.cpqo_alvo_brl is not None
        and met.cpl_brl < metas.cpqo_alvo_brl * 0.3
    )
    cpqo_ruim = (
        met.cpqo_brl is None
        or (metas.cpqo_alvo_brl is not None and met.cpqo_brl > metas.cpqo_alvo_brl)
    )
    if cpl_ok and cpqo_ruim and m.leads >= 25:
        bloqueios.append(
            "CPL bom e custo por oportunidade qualificada fora da meta — "
            "escalar multiplicaria lead barato que não vira negócio."
        )

    if met.cac_brl is not None and metas.cac_alvo_brl is not None:
        if met.cac_brl > metas.cac_alvo_brl:
            bloqueios.append(
                f"CAC de R$ {met.cac_brl:,.0f} acima da meta de R$ {metas.cac_alvo_brl:,.0f}."
            )
    if m.vendas < MINIMO_CONVERSOES_PARA_CPA:
        bloqueios.append(
            f"Apenas {m.vendas} venda(s) — abaixo de {MINIMO_CONVERSOES_PARA_CPA}, "
            f"o CAC observado ainda não é estável."
        )
    if met.lucro_bruto_brl is not None and met.lucro_bruto_brl <= 0:
        bloqueios.append("Margem bruta não cobre o investimento da campanha.")

    # Estes não são inferíveis dos dados de mídia — precisam de confirmação humana.
    bloqueios.append(
        "Confirmar fora do sistema: capacidade comercial de atender mais oportunidades e "
        "capacidade de entrega do produto vendido."
    )

    gargalo_grave = next((a for a in diagnostico.achados if a.gravidade == "alta"), None)
    if gargalo_grave:
        return DecisaoOtimizacao(
            campanha_id=campanha.id, acao="investigar",
            justificativa=f"{gargalo_grave.sintoma} {gargalo_grave.acao}",
            evidencia=gargalo_grave.confianca_estatistica,
            bloqueios_de_escala=bloqueios,
        )

    dentro_da_meta = (
        met.cac_brl is not None and metas.cac_alvo_brl is not None
        and met.cac_brl <= metas.cac_alvo_brl
    )
    bloqueios_reais = [b for b in bloqueios if not b.startswith("Confirmar fora do sistema")]

    if dentro_da_meta and not bloqueios_reais and m.vendas >= MINIMO_CONVERSOES_PARA_CPA:
        return DecisaoOtimizacao(
            campanha_id=campanha.id, acao="escalar",
            justificativa=(
                f"CAC de R$ {met.cac_brl:,.0f} dentro da meta, com {m.vendas} vendas e "
                f"cadeia sem gargalo."
            ),
            evidencia=(
                f"ROAS {met.roas:.2f}x sobre R$ {met.investimento_brl:,.0f} investidos."
                if met.roas else "Volume e qualidade confirmados."
            ),
            bloqueios_de_escala=bloqueios,
        )

    return DecisaoOtimizacao(
        campanha_id=campanha.id, acao="manter",
        justificativa="Campanha saudável, mas ainda sem condições confirmadas para escalar.",
        evidencia=diagnostico.leitura,
        bloqueios_de_escala=bloqueios,
    )

"""
Engine de carbono do Land Bank Zion.

Cálculo determinístico e auditável: nada aqui depende de LLM. A engine
recebe o portfólio de glebas, aplica triagem de elegibilidade, agrupa as
terras em clusters (projetos agrupados), estima remoções/emissões evitadas
ao longo do período de creditação e monta o fluxo de caixa do projeto de
carbono.

Premissa central do Land Bank:
    o custo fixo de um projeto de carbono (PDD, validação, verificação, MRV)
    é praticamente o mesmo para 200 ha e para 2.000 ha. Escala não é vaidade,
    é a variável que decide se o projeto existe.

IMPORTANTE — os fatores e preços default são ordens de grandeza calibradas
sobre referências públicas do mercado voluntário brasileiro. Servem para
priorizar terra e dimensionar tese. Antes de contrato, captação ou emissão,
substituir por inventário florestal de campo e cotação real de mercado.
"""

import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from src.models.land_bank import (
    Bioma,
    ClasseElegibilidade,
    ClusterCarbono,
    FluxoAnual,
    Gleba,
    GlebaAvaliada,
    Instrumento,
    LandBank,
    Metodologia,
    PremissasCarbono,
    PrioridadeAquisicao,
    ResultadoLandBank,
    StatusDominial,
    Talhao,
    TalhaoAvaliado,
    UsoSolo,
    CenarioCarbono,
)

RAIO_TERRA_KM = 6371.0

# ---------------------------------------------------------------------------
# Parâmetros técnicos
# ---------------------------------------------------------------------------

# Remoção líquida média em tCO2e/ha/ano ao longo de um ciclo de 30 anos,
# considerando biomassa aérea, subterrânea e serapilheira.
FATOR_REMOCAO_HA_ANO: Dict[Bioma, Dict[Metodologia, float]] = {
    Bioma.AMAZONIA: {
        Metodologia.ARR_PLANTIO: 15.0,
        Metodologia.ARR_REGENERACAO: 13.0,
        Metodologia.SAF: 8.0,
        Metodologia.IFM: 3.0,
    },
    Bioma.MATA_ATLANTICA: {
        Metodologia.ARR_PLANTIO: 14.0,
        Metodologia.ARR_REGENERACAO: 11.0,
        Metodologia.SAF: 7.0,
        Metodologia.IFM: 2.5,
    },
    Bioma.CERRADO: {
        Metodologia.ARR_PLANTIO: 7.0,
        Metodologia.ARR_REGENERACAO: 5.5,
        Metodologia.SAF: 4.5,
        Metodologia.IFM: 1.5,
    },
    Bioma.CAATINGA: {
        Metodologia.ARR_PLANTIO: 4.5,
        Metodologia.ARR_REGENERACAO: 3.5,
        Metodologia.SAF: 3.0,
        Metodologia.IFM: 1.0,
    },
    Bioma.PAMPA: {
        Metodologia.ARR_PLANTIO: 5.0,
        Metodologia.ARR_REGENERACAO: 4.0,
        Metodologia.SAF: 3.5,
        Metodologia.IFM: 1.0,
    },
    Bioma.PANTANAL: {
        Metodologia.ARR_PLANTIO: 6.0,
        Metodologia.ARR_REGENERACAO: 5.0,
        Metodologia.SAF: 4.0,
        Metodologia.IFM: 1.2,
    },
}

# Estoque médio de carbono da vegetação nativa madura, em tCO2e/ha.
# Base do cálculo de desmatamento evitado (REDD).
ESTOQUE_CARBONO_HA: Dict[Bioma, float] = {
    Bioma.AMAZONIA: 550.0,
    Bioma.MATA_ATLANTICA: 400.0,
    Bioma.CERRADO: 180.0,
    Bioma.CAATINGA: 120.0,
    Bioma.PAMPA: 90.0,
    Bioma.PANTANAL: 200.0,
}

# Metodologia sugerida a partir do uso atual do solo.
METODOLOGIA_POR_USO: Dict[UsoSolo, Metodologia] = {
    UsoSolo.PASTAGEM_DEGRADADA: Metodologia.ARR_PLANTIO,
    UsoSolo.SOLO_EXPOSTO: Metodologia.ARR_PLANTIO,
    UsoSolo.PASTAGEM_ATIVA: Metodologia.ARR_PLANTIO,
    UsoSolo.AGRICULTURA: Metodologia.SAF,
    UsoSolo.REGENERACAO_INICIAL: Metodologia.ARR_REGENERACAO,
    UsoSolo.FLORESTA_DEGRADADA: Metodologia.IFM,
    UsoSolo.FLORESTA_CONSERVADA: Metodologia.REDD_CONSERVACAO,
    UsoSolo.SILVICULTURA: Metodologia.NAO_ELEGIVEL,
    UsoSolo.AREA_EDIFICADA: Metodologia.NAO_ELEGIVEL,
    UsoSolo.CORPO_DAGUA: Metodologia.NAO_ELEGIVEL,
}

# Rotas de remoção — dependem de a área NÃO ser floresta na data de corte.
ROTAS_REMOCAO = {Metodologia.ARR_PLANTIO, Metodologia.ARR_REGENERACAO, Metodologia.SAF}

# Parâmetros de forma da curva de crescimento (Chapman-Richards).
CURVA_PARAMS: Dict[Metodologia, Tuple[float, float]] = {
    Metodologia.ARR_PLANTIO: (0.14, 2.2),
    Metodologia.ARR_REGENERACAO: (0.10, 2.8),
    Metodologia.SAF: (0.18, 1.8),
}


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def _fmt(valor: float, casas: int = 0) -> str:
    """Formata número no padrão brasileiro para uso em mensagens."""
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "§").replace(".", ",").replace("§", ".")


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distância em km entre dois pontos geográficos."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * RAIO_TERRA_KM * math.asin(math.sqrt(a))


def curva_sequestro(metodologia: Metodologia, horizonte: int) -> List[float]:
    """
    Distribuição anual do sequestro ao longo do período de creditação.

    Floresta não cresce em linha reta: os primeiros anos entregam pouco e o
    pico acontece entre o ano 8 e o ano 20. A curva é normalizada para que a
    soma dos fatores seja igual ao horizonte — assim a média anual continua
    sendo exatamente o fator de remoção da tabela.
    """
    if metodologia not in CURVA_PARAMS:
        # Emissão evitada e manejo florestal têm fluxo aproximadamente constante.
        return [1.0] * horizonte

    k, m = CURVA_PARAMS[metodologia]
    biomassa = [(1 - math.exp(-k * t)) ** m for t in range(horizonte + 1)]
    incrementos = [biomassa[t + 1] - biomassa[t] for t in range(horizonte)]
    total = sum(incrementos)
    if total <= 0:
        return [1.0] * horizonte
    return [inc * horizonte / total for inc in incrementos]


def _vpl(fluxos: List[float], taxa: float) -> float:
    """Valor presente líquido de um fluxo indexado a partir do ano 0."""
    return sum(f / ((1 + taxa) ** i) for i, f in enumerate(fluxos))


def _tir(fluxos: List[float]) -> Optional[float]:
    """TIR por bisseção. Retorna None quando não há troca de sinal."""
    if not fluxos or all(f >= 0 for f in fluxos) or all(f <= 0 for f in fluxos):
        return None

    baixa, alta = -0.95, 5.0
    v_baixa = _vpl(fluxos, baixa)
    v_alta = _vpl(fluxos, alta)
    if v_baixa * v_alta > 0:
        return None

    for _ in range(200):
        meio = (baixa + alta) / 2
        v_meio = _vpl(fluxos, meio)
        if abs(v_meio) < 1e-6:
            return meio
        if v_baixa * v_meio < 0:
            alta, v_alta = meio, v_meio
        else:
            baixa, v_baixa = meio, v_meio
    return (baixa + alta) / 2


def preco_por_metodologia(metodologia: Metodologia, premissas: PremissasCarbono) -> float:
    """Preço unitário de referência do crédito, em BRL/tCO2e."""
    if metodologia == Metodologia.REDD_CONSERVACAO:
        return premissas.preco_tco2e_evitada_brl
    if metodologia == Metodologia.IFM:
        return premissas.preco_tco2e_ifm_brl
    return premissas.preco_tco2e_remocao_brl


def buffer_por_metodologia(metodologia: Metodologia, premissas: PremissasCarbono) -> float:
    """Percentual retido no buffer pool de não permanência."""
    if metodologia in (Metodologia.REDD_CONSERVACAO, Metodologia.IFM):
        return premissas.buffer_evitada
    return premissas.buffer_remocao


def fator_remocao(
    bioma: Bioma, metodologia: Metodologia, premissas: PremissasCarbono
) -> float:
    """Fator bruto de geração de carbono em tCO2e/ha/ano."""
    if metodologia == Metodologia.NAO_ELEGIVEL:
        return 0.0
    if metodologia == Metodologia.REDD_CONSERVACAO:
        estoque = ESTOQUE_CARBONO_HA.get(bioma, 200.0)
        return estoque * premissas.taxa_desmatamento_baseline
    return FATOR_REMOCAO_HA_ANO.get(bioma, {}).get(metodologia, 0.0)


def sugerir_metodologia(talhao: Talhao) -> Metodologia:
    """Metodologia adequada ao uso do solo do talhão."""
    if talhao.metodologia_forcada is not None:
        return talhao.metodologia_forcada
    return METODOLOGIA_POR_USO.get(talhao.uso_solo, Metodologia.NAO_ELEGIVEL)


# ---------------------------------------------------------------------------
# Avaliação de gleba
# ---------------------------------------------------------------------------

def _talhoes_da_gleba(gleba: Gleba) -> List[Talhao]:
    """Retorna os talhões mapeados ou deriva um talhão único do uso predominante."""
    if gleba.talhoes:
        return gleba.talhoes
    if gleba.uso_solo_predominante is None:
        return []
    return [
        Talhao(
            id=f"{gleba.id}-T1",
            descricao="Talhão único derivado do uso predominante",
            area_ha=gleba.area_total_ha,
            uso_solo=gleba.uso_solo_predominante,
        )
    ]


def _bloqueios_da_gleba(gleba: Gleba) -> List[str]:
    """Impedimentos que zeram a elegibilidade enquanto não forem resolvidos."""
    bloqueios: List[str] = []
    if gleba.sobreposicao_sensivel:
        bloqueios.append(
            "Sobreposição com terra indígena, território quilombola ou UC de proteção integral "
            "— nenhum standard registra projeto sem consulta livre, prévia e informada concluída"
        )
    if gleba.litigio_dominial:
        bloqueios.append(
            "Litígio dominial em curso — sem cadeia dominial limpa não há titularidade do crédito"
        )
    if gleba.desmatamento_recente:
        bloqueios.append(
            "Supressão de vegetação nativa dentro da janela de corte de 10 anos "
            "— inviabiliza rota de remoção e contamina salvaguardas do projeto"
        )
    return bloqueios


def _pendencias_da_gleba(gleba: Gleba) -> List[str]:
    """Pendências sanáveis que atrasam o registro mas não matam a tese."""
    pendencias: List[str] = []
    if not gleba.car_ativo:
        pendencias.append("CAR inexistente ou com pendência — regularizar antes do PDD")
    if not gleba.matricula_regular:
        pendencias.append("Matrícula não regular/georreferenciada — exigida para titularidade do crédito")
    if gleba.latitude is None or gleba.longitude is None:
        pendencias.append("Sem coordenadas do centroide — impede clusterização geográfica precisa")
    if gleba.status_dominial in (StatusDominial.PROSPECCAO, StatusDominial.EM_NEGOCIACAO):
        pendencias.append("Área ainda não contratada — potencial não é estoque")
    if not gleba.talhoes:
        pendencias.append("Talhões não mapeados — estimativa feita sobre uso predominante")
    return pendencias


def avaliar_gleba(
    gleba: Gleba,
    premissas: PremissasCarbono,
    fator_produtividade: float = 1.0,
) -> GlebaAvaliada:
    """
    Aplica triagem de elegibilidade e estima o potencial de carbono de uma gleba.

    A classe do talhão reflete elegibilidade TÉCNICA. Pendências documentais
    (CAR, matrícula) não reclassificam a área — entram no readiness score, que
    é o indicador de quão perto essa terra está de virar crédito emitido.
    """
    bloqueios = _bloqueios_da_gleba(gleba)
    pendencias = _pendencias_da_gleba(gleba)
    talhoes = _talhoes_da_gleba(gleba)

    avaliados: List[TalhaoAvaliado] = []
    area_elegivel = area_condicionada = area_inelegivel = 0.0
    tco2e_bruto = vcus_liquidos = vcus_condicionados = custo_implantacao = 0.0

    for talhao in talhoes:
        metodologia = sugerir_metodologia(talhao)
        classe = ClasseElegibilidade.ELEGIVEL
        motivo = "Elegível na rota sugerida pelo uso do solo"

        if metodologia == Metodologia.NAO_ELEGIVEL:
            classe = ClasseElegibilidade.INELEGIVEL
            motivo = f"Uso do solo '{talhao.uso_solo.value}' não gera crédito nas rotas cobertas"
        elif bloqueios:
            classe = ClasseElegibilidade.INELEGIVEL
            motivo = bloqueios[0]
        elif talhao.obrigacao_legal:
            classe = ClasseElegibilidade.CONDICIONADA
            motivo = (
                "Passivo legal de recomposição (APP/Reserva Legal) — adicionalidade contestável, "
                "tratar como potencial condicionado"
            )

        fator = fator_remocao(gleba.bioma, metodologia, premissas) * fator_produtividade
        bruto = fator * talhao.area_ha * premissas.horizonte_anos
        buffer = buffer_por_metodologia(metodologia, premissas)
        liquido = bruto * (1 - buffer) * (1 - premissas.incerteza_desconto)
        custo_ha = premissas.custo_implantacao_ha_brl.get(metodologia.value, 0.0)

        if classe == ClasseElegibilidade.INELEGIVEL:
            bruto = liquido = 0.0
            fator = 0.0
            custo_talhao = 0.0
            area_inelegivel += talhao.area_ha
        elif classe == ClasseElegibilidade.CONDICIONADA:
            custo_talhao = custo_ha * talhao.area_ha
            area_condicionada += talhao.area_ha
            vcus_condicionados += liquido
        else:
            custo_talhao = custo_ha * talhao.area_ha
            area_elegivel += talhao.area_ha
            tco2e_bruto += bruto
            vcus_liquidos += liquido
            custo_implantacao += custo_talhao

        avaliados.append(
            TalhaoAvaliado(
                talhao_id=talhao.id,
                area_ha=talhao.area_ha,
                uso_solo=talhao.uso_solo,
                metodologia=metodologia,
                classe=classe,
                motivo=motivo,
                fator_tco2e_ha_ano=round(fator, 2),
                tco2e_bruto_horizonte=round(bruto, 1),
                vcus_liquidos=round(liquido, 1),
                custo_implantacao_brl=round(custo_talhao, 2),
            )
        )

    if not talhoes:
        pendencias.append("Sem talhões nem uso predominante informado — gleba não avaliável")
        area_inelegivel = gleba.area_total_ha

    custo_entrada = gleba.custo_negociacao_brl
    if gleba.instrumento == Instrumento.COMPRA and gleba.custo_aquisicao_ha_brl:
        custo_entrada += gleba.custo_aquisicao_ha_brl * gleba.area_total_ha

    score = _readiness_score(gleba, area_elegivel, area_condicionada, bloqueios)

    return GlebaAvaliada(
        gleba_id=gleba.id,
        nome=gleba.nome,
        municipio=gleba.municipio,
        uf=gleba.uf,
        bioma=gleba.bioma,
        status_dominial=gleba.status_dominial,
        area_total_ha=gleba.area_total_ha,
        area_elegivel_ha=round(area_elegivel, 2),
        area_condicionada_ha=round(area_condicionada, 2),
        area_inelegivel_ha=round(area_inelegivel, 2),
        tco2e_bruto_horizonte=round(tco2e_bruto, 1),
        vcus_liquidos=round(vcus_liquidos, 1),
        vcus_condicionados=round(vcus_condicionados, 1),
        custo_implantacao_brl=round(custo_implantacao, 2),
        custo_entrada_brl=round(custo_entrada, 2),
        readiness_score=score,
        classificacao=_classificar_readiness(score),
        bloqueios=bloqueios,
        pendencias=pendencias,
        talhoes=avaliados,
    )


def _readiness_score(
    gleba: Gleba, area_elegivel: float, area_condicionada: float, bloqueios: List[str]
) -> float:
    """
    Carbon Readiness Score (0-10): quão perto essa terra está de virar crédito.

    Dominialidade 25% · Regularidade documental 20% · Elegibilidade técnica 25%
    Escala 15% · Risco socioambiental 15%
    """
    dominialidade = {
        StatusDominial.PROPRIO: 10.0,
        StatusDominial.CONTRATADO: 9.0,
        StatusDominial.EM_NEGOCIACAO: 5.0,
        StatusDominial.PROSPECCAO: 2.0,
    }[gleba.status_dominial]

    regularidade = 0.0
    regularidade += 4.0 if gleba.car_ativo else 0.0
    regularidade += 3.0 if gleba.matricula_regular else 0.0
    regularidade += 3.0 if not gleba.litigio_dominial else 0.0

    area_util = area_elegivel + 0.5 * area_condicionada
    elegibilidade = 10.0 * area_util / gleba.area_total_ha if gleba.area_total_ha else 0.0
    escala = min(10.0, area_elegivel / 50.0)

    risco = 10.0
    if gleba.sobreposicao_sensivel:
        risco = 0.0
    elif gleba.desmatamento_recente:
        risco = 3.0
    elif gleba.litigio_dominial:
        risco = 2.0

    score = (
        dominialidade * 0.25
        + regularidade * 0.20
        + elegibilidade * 0.25
        + escala * 0.15
        + risco * 0.15
    )
    if bloqueios:
        score = min(score, 4.0)
    return round(score, 2)


def _classificar_readiness(score: float) -> str:
    if score >= 8:
        return "pronta para estruturar"
    if score >= 6:
        return "bancável com ajustes"
    if score >= 4:
        return "requer originação"
    return "prospecção inicial"


# ---------------------------------------------------------------------------
# Clusterização — o coração da agregação
# ---------------------------------------------------------------------------

def clusterizar(
    glebas: List[Gleba], avaliadas: Dict[str, GlebaAvaliada], premissas: PremissasCarbono
) -> List[ClusterCarbono]:
    """
    Agrupa glebas em projetos agrupados candidatos.

    Regra: mesmo bioma e centroides dentro do raio configurado. Glebas sem
    coordenadas caem num cluster de bioma/UF, sinalizado como pendência.
    """
    clusters: List[ClusterCarbono] = []
    pendentes = [g for g in glebas if avaliadas[g.id].area_elegivel_ha > 0]
    # Maior área elegível primeiro: a gleba âncora define o centro do cluster.
    pendentes.sort(key=lambda g: avaliadas[g.id].area_elegivel_ha, reverse=True)

    atribuidas: set = set()
    indice = 1

    for ancora in pendentes:
        if ancora.id in atribuidas:
            continue

        membros = [ancora]
        atribuidas.add(ancora.id)

        if ancora.latitude is not None and ancora.longitude is not None:
            for candidata in pendentes:
                if candidata.id in atribuidas or candidata.bioma != ancora.bioma:
                    continue
                if candidata.latitude is None or candidata.longitude is None:
                    continue
                dist = haversine_km(
                    ancora.latitude, ancora.longitude, candidata.latitude, candidata.longitude
                )
                if dist <= premissas.raio_cluster_km:
                    membros.append(candidata)
                    atribuidas.add(candidata.id)
        else:
            for candidata in pendentes:
                if candidata.id in atribuidas or candidata.bioma != ancora.bioma:
                    continue
                if candidata.latitude is None and candidata.uf == ancora.uf:
                    membros.append(candidata)
                    atribuidas.add(candidata.id)

        clusters.append(_montar_cluster(f"CL-{indice:02d}", membros, avaliadas, premissas))
        indice += 1

    return clusters


def _montar_cluster(
    cluster_id: str,
    membros: List[Gleba],
    avaliadas: Dict[str, GlebaAvaliada],
    premissas: PremissasCarbono,
) -> ClusterCarbono:
    """Consolida áreas, centro geográfico e escala de um cluster."""
    ancora = membros[0]
    coords = [(g.latitude, g.longitude) for g in membros if g.latitude is not None and g.longitude is not None]

    centro_lat = centro_lon = None
    raio_max = 0.0
    if coords:
        centro_lat = sum(c[0] for c in coords) / len(coords)
        centro_lon = sum(c[1] for c in coords) / len(coords)
        raio_max = max(
            (haversine_km(centro_lat, centro_lon, lat, lon) for lat, lon in coords), default=0.0
        )

    area_total = sum(g.area_total_ha for g in membros)
    area_elegivel = sum(avaliadas[g.id].area_elegivel_ha for g in membros)
    area_contratada = sum(
        avaliadas[g.id].area_elegivel_ha
        for g in membros
        if g.status_dominial in (StatusDominial.PROPRIO, StatusDominial.CONTRATADO)
    )

    if area_elegivel >= premissas.area_alvo_cluster_ha:
        escala = "escala plena"
        gap = 0.0
    elif area_elegivel >= premissas.area_minima_cluster_ha:
        escala = "escala mínima atingida"
        gap = premissas.area_alvo_cluster_ha - area_elegivel
    else:
        escala = "subescala"
        gap = premissas.area_minima_cluster_ha - area_elegivel

    municipios = sorted({f"{g.municipio}/{g.uf}" for g in membros})

    return ClusterCarbono(
        id=cluster_id,
        nome=f"Cluster {ancora.municipio}/{ancora.uf} — {ancora.bioma.value.replace('_', ' ').title()}",
        bioma=ancora.bioma,
        municipios=municipios,
        glebas_ids=[g.id for g in membros],
        centro_lat=round(centro_lat, 5) if centro_lat is not None else None,
        centro_lon=round(centro_lon, 5) if centro_lon is not None else None,
        raio_max_km=round(raio_max, 1),
        area_total_ha=round(area_total, 2),
        area_elegivel_ha=round(area_elegivel, 2),
        area_contratada_ha=round(area_contratada, 2),
        escala=escala,
        gap_escala_ha=round(gap, 2),
    )


# ---------------------------------------------------------------------------
# Modelagem financeira do cluster
# ---------------------------------------------------------------------------

def modelar_financeiro(
    cluster: ClusterCarbono,
    membros: List[Gleba],
    avaliadas: Dict[str, GlebaAvaliada],
    premissas: PremissasCarbono,
    fator_produtividade: float = 1.0,
) -> ClusterCarbono:
    """
    Monta o fluxo de caixa do projeto agrupado.

    Timing importa mais que o total: o CAPEX de restauração sai nos primeiros
    anos e a primeira emissão de VCUs só acontece após a primeira verificação.
    É essa defasagem que quebra projeto de carbono mal estruturado.
    """
    h = premissas.horizonte_anos
    vcus_ano = [0.0] * (h + 1)
    valor_ano = [0.0] * (h + 1)
    valor_terrenista_ano = [0.0] * (h + 1)
    custo_ano = [0.0] * (h + 1)

    area_protegida_custo = 0.0

    for gleba in membros:
        avaliada = avaliadas[gleba.id]
        pct_terrenista = (
            gleba.percentual_receita_terrenista
            if gleba.percentual_receita_terrenista is not None
            else premissas.percentual_receita_terrenista
        )

        for talhao in avaliada.talhoes:
            if talhao.classe != ClasseElegibilidade.ELEGIVEL or talhao.vcus_liquidos <= 0:
                continue

            curva = curva_sequestro(talhao.metodologia, h)
            preco = preco_por_metodologia(talhao.metodologia, premissas)
            base_anual = talhao.vcus_liquidos / h

            pct_prevenda = premissas.percentual_prevenda
            preco_prevenda = preco * (1 - premissas.desconto_prevenda)
            ano_adiantamento = min(premissas.ano_adiantamento, h)

            for ano in range(1, h + 1):
                vcus = base_anual * curva[ano - 1]
                vcus_ano[ano] += vcus

                # Parcela vendida no spot: caixa entra na emissão.
                receita_spot = vcus * (1 - pct_prevenda) * preco
                valor_ano[ano] += receita_spot
                valor_terrenista_ano[ano] += receita_spot * pct_terrenista

                # Parcela pré-vendida: caixa entra adiantado, com deságio.
                if pct_prevenda > 0:
                    receita_prevenda = vcus * pct_prevenda * preco_prevenda
                    valor_ano[ano_adiantamento] += receita_prevenda
                    valor_terrenista_ano[ano_adiantamento] += receita_prevenda * pct_terrenista

            custo_protecao_ha = premissas.custo_protecao_ha_ano_brl.get(talhao.metodologia.value, 0.0)
            area_protegida_custo += custo_protecao_ha * talhao.area_ha

        # CAPEX de restauração diluído nos primeiros anos.
        parcelas = max(1, premissas.anos_implantacao)
        for ano in range(parcelas):
            custo_ano[min(ano, h)] += avaliada.custo_implantacao_brl / parcelas

        # Custo de originação da terra no ano 0.
        custo_ano[0] += avaliada.custo_entrada_brl

    # Custos fixos do projeto agrupado.
    custo_ano[0] += premissas.custo_estruturacao_brl
    for ano in range(1, h + 1):
        custo_ano[ano] += premissas.custo_mrv_fixo_ano_brl
        custo_ano[ano] += premissas.custo_mrv_ha_ano_brl * cluster.area_elegivel_ha
        custo_ano[ano] += area_protegida_custo

    # Eventos de verificação e emissão.
    anos_emissao = list(
        range(premissas.ano_primeira_emissao, h + 1, premissas.intervalo_verificacao_anos)
    )
    for ano in anos_emissao:
        custo_ano[ano] += premissas.custo_verificacao_brl

    fluxo: List[FluxoAnual] = []
    acumulado = 0.0
    vcus_pendentes = 0.0
    valor_pendente = 0.0
    terrenista_pendente = 0.0
    custos_a_recuperar = 0.0
    split_liquido = premissas.base_reparticao == "liquida"

    receita_bruta_total = 0.0
    receita_terrenistas_total = 0.0
    custos_total = 0.0
    vcus_total = 0.0
    fluxos_brutos: List[float] = []

    for ano in range(0, h + 1):
        vcus_pendentes += vcus_ano[ano]
        valor_pendente += valor_ano[ano]
        terrenista_pendente += valor_terrenista_ano[ano]

        custos_a_recuperar += custo_ano[ano]

        emitidos = receita = terrenista = 0.0
        evento_adiantamento = (
            premissas.percentual_prevenda > 0
            and ano == min(premissas.ano_adiantamento, h)
            and ano not in anos_emissao
        )
        if ano in anos_emissao or evento_adiantamento or (ano == h and vcus_pendentes > 0):
            emitidos = 0.0 if evento_adiantamento else vcus_pendentes
            receita = valor_pendente - emitidos * premissas.taxa_registro_por_vcu_brl
            # Split ponderado pelas fatias contratadas de cada gleba do evento.
            pct_efetivo = terrenista_pendente / valor_pendente if valor_pendente > 0 else 0.0

            if split_liquido:
                # A Zion banca o CAPEX: recupera custo antes de repartir.
                # O que não for coberto no evento rola para o próximo.
                terrenista = pct_efetivo * max(0.0, receita - custos_a_recuperar)
                custos_a_recuperar = max(0.0, custos_a_recuperar - receita)
            else:
                terrenista = terrenista_pendente
                custos_a_recuperar = 0.0

            if not evento_adiantamento:
                vcus_pendentes = 0.0
            valor_pendente = terrenista_pendente = 0.0

        custos = custo_ano[ano] + terrenista
        liquido = receita - custos
        acumulado += liquido

        receita_bruta_total += receita
        receita_terrenistas_total += terrenista
        custos_total += custo_ano[ano]
        vcus_total += emitidos
        fluxos_brutos.append(liquido)

        fluxo.append(
            FluxoAnual(
                ano=ano,
                vcus_emitidos=round(emitidos, 1),
                receita_bruta_brl=round(receita, 2),
                receita_terrenistas_brl=round(terrenista, 2),
                custos_brl=round(custos, 2),
                fluxo_liquido_brl=round(liquido, 2),
                fluxo_acumulado_brl=round(acumulado, 2),
            )
        )

    payback = next((f.ano for f in fluxo if f.fluxo_acumulado_brl >= 0 and f.ano > 0), None)
    tir = _tir(fluxos_brutos)
    vpl = _vpl(fluxos_brutos, premissas.taxa_desconto)

    custo_implantacao = sum(avaliadas[g.id].custo_implantacao_brl for g in membros)
    custo_entrada = sum(avaliadas[g.id].custo_entrada_brl for g in membros)
    custo_mrv = custos_total - custo_implantacao - custo_entrada - premissas.custo_estruturacao_brl

    cluster.vcus_liquidos = round(vcus_total, 1)
    cluster.receita_bruta_brl = round(receita_bruta_total, 2)
    cluster.receita_terrenistas_brl = round(receita_terrenistas_total, 2)
    cluster.custo_estruturacao_brl = round(premissas.custo_estruturacao_brl, 2)
    cluster.custo_implantacao_brl = round(custo_implantacao, 2)
    cluster.custo_mrv_brl = round(custo_mrv, 2)
    cluster.custo_entrada_brl = round(custo_entrada, 2)
    cluster.resultado_liquido_zion_brl = round(acumulado, 2)
    cluster.vpl_brl = round(vpl, 2)
    cluster.tir = round(tir, 4) if tir is not None else None
    cluster.payback_ano = payback
    cluster.custo_por_vcu_brl = round(custos_total / vcus_total, 2) if vcus_total else 0.0
    cluster.fluxo = fluxo
    cluster.viavel = vpl > 0 and cluster.area_elegivel_ha >= premissas.area_minima_cluster_ha

    cluster.alertas = _alertas_cluster(cluster, premissas)
    return cluster


def calcular_preco_equilibrio(
    cluster: ClusterCarbono,
    membros: List[Gleba],
    avaliadas: Dict[str, GlebaAvaliada],
    premissas: PremissasCarbono,
) -> Optional[float]:
    """
    Preço de tCO2e de remoção que zera o VPL do cluster.

    É o número que decide a conversa: se o preço de equilíbrio está acima do
    que o mercado paga, o problema não é negociação, é estrutura — agregar
    mais área, trocar plantio por regeneração natural ou rever o split.
    """

    def vpl_para(fator: float) -> float:
        copia = cluster.model_copy(deep=True)
        modelar_financeiro(copia, membros, avaliadas, _premissas_cenario(premissas, fator))
        return copia.vpl_brl

    baixo, alto = 0.05, 20.0
    if vpl_para(baixo) > 0:
        return round(premissas.preco_tco2e_remocao_brl * baixo, 2)
    if vpl_para(alto) < 0:
        return None

    for _ in range(32):
        meio = (baixo + alto) / 2
        if vpl_para(meio) < 0:
            baixo = meio
        else:
            alto = meio
    return round(premissas.preco_tco2e_remocao_brl * alto, 2)


def calcular_prevenda_minima(
    cluster: ClusterCarbono,
    membros: List[Gleba],
    avaliadas: Dict[str, GlebaAvaliada],
    premissas: PremissasCarbono,
) -> Optional[float]:
    """
    Fração mínima de créditos pré-vendidos com adiantamento que zera o VPL.

    É a alavanca real de um projeto de carbono: o custo sai no ano 0 e o
    crédito só entra depois da primeira verificação. Quem fecha esse buraco
    é o offtaker que paga adiantado, aceitando deságio.
    """

    def vpl_para(fracao: float) -> float:
        dados = premissas.model_dump()
        dados["percentual_prevenda"] = fracao
        copia = cluster.model_copy(deep=True)
        modelar_financeiro(copia, membros, avaliadas, PremissasCarbono(**dados))
        return copia.vpl_brl

    if vpl_para(0.0) >= 0:
        return 0.0
    if vpl_para(1.0) < 0:
        return None

    baixo, alto = 0.0, 1.0
    for _ in range(24):
        meio = (baixo + alto) / 2
        if vpl_para(meio) < 0:
            baixo = meio
        else:
            alto = meio
    return round(alto, 4)


def _alertas_cluster(cluster: ClusterCarbono, premissas: PremissasCarbono) -> List[str]:
    """Diagnóstico de risco estrutural do cluster."""
    alertas: List[str] = []

    if cluster.area_elegivel_ha < premissas.area_minima_cluster_ha:
        alertas.append(
            f"Subescala: {_fmt(cluster.area_elegivel_ha)} ha elegíveis contra mínimo de "
            f"{_fmt(premissas.area_minima_cluster_ha)} ha. Faltam {_fmt(cluster.gap_escala_ha)} ha "
            f"para o custo fixo se diluir."
        )
    if cluster.vpl_brl <= 0:
        if cluster.preco_equilibrio_brl:
            alertas.append(
                f"VPL negativo nas premissas atuais. O cluster só fecha a partir de "
                f"R$ {_fmt(cluster.preco_equilibrio_brl, 2)}/tCO2e contra os "
                f"R$ {_fmt(premissas.preco_tco2e_remocao_brl, 2)}/tCO2e modelados. "
                f"Alavancas: agregar área, migrar plantio para regeneração natural assistida, "
                f"rever o split ou travar pré-venda com adiantamento do offtaker."
            )
            if cluster.prevenda_minima is not None:
                alertas.append(
                    f"Pré-venda mínima para virar o VPL: {_fmt(cluster.prevenda_minima * 100)}% dos "
                    f"créditos vendidos adiantado com {_fmt(premissas.desconto_prevenda * 100)}% de "
                    f"deságio, caixa no ano {premissas.ano_adiantamento}."
                )
            else:
                alertas.append(
                    "Nem 100% de pré-venda vira o VPL deste cluster nas premissas atuais — "
                    "o problema é estrutural, não de financiamento."
                )
        else:
            alertas.append(
                "VPL negativo e sem preço de equilíbrio dentro de faixa razoável — "
                "o cluster não se paga na configuração atual. Reestruturar antes de originar terra."
            )
    if cluster.area_contratada_ha < cluster.area_elegivel_ha * 0.5:
        alertas.append(
            f"Apenas {_fmt(cluster.area_contratada_ha)} ha de {_fmt(cluster.area_elegivel_ha)} ha "
            f"estão contratados. O restante é pipeline, não estoque."
        )
    if cluster.raio_max_km > premissas.raio_cluster_km * 0.9:
        alertas.append(
            f"Dispersão geográfica alta ({_fmt(cluster.raio_max_km)} km do centroide) — "
            f"eleva custo de MRV e de proteção de campo."
        )
    if cluster.payback_ano is None:
        alertas.append("Sem payback dentro do horizonte de creditação.")
    return alertas


# ---------------------------------------------------------------------------
# Priorização de aquisição
# ---------------------------------------------------------------------------

def _instrumento_recomendado(gleba: Gleba, avaliada: GlebaAvaliada) -> Instrumento:
    """Instrumento de agregação mais adequado ao perfil da gleba."""
    if gleba.instrumento is not None:
        return gleba.instrumento

    rotas = {t.metodologia for t in avaliada.talhoes if t.classe == ClasseElegibilidade.ELEGIVEL}

    # Terra com floresta em pé: não precisa comprar, precisa travar o direito.
    if Metodologia.REDD_CONSERVACAO in rotas or Metodologia.IFM in rotas:
        return Instrumento.CESSAO_DIREITOS_CARBONO
    # Terra colada no hub hoteleiro: vale ter o ativo.
    if gleba.distancia_hub_km is not None and gleba.distancia_hub_km <= 15:
        return Instrumento.COMPRA
    # Restauração exige posse longa da área: arrendamento de carbono de 30+ anos.
    if Metodologia.ARR_PLANTIO in rotas or Metodologia.ARR_REGENERACAO in rotas:
        return Instrumento.ARRENDAMENTO_CARBONO
    return Instrumento.PARCERIA_RECEITA


def priorizar_aquisicoes(
    glebas: List[Gleba],
    avaliadas: Dict[str, GlebaAvaliada],
    clusters: List[ClusterCarbono],
    premissas: PremissasCarbono,
) -> List[PrioridadeAquisicao]:
    """
    Ordena o que agregar primeiro.

    Critério: eficiência de carbono por real investido, com bônus para as
    glebas que levam um cluster subescala até a escala mínima. Terra que
    destrava projeto vale mais que terra que só engorda portfólio.
    """
    cluster_por_gleba = {gid: c for c in clusters for gid in c.glebas_ids}
    candidatas = []

    for gleba in glebas:
        if gleba.status_dominial in (StatusDominial.PROPRIO, StatusDominial.CONTRATADO):
            continue
        avaliada = avaliadas[gleba.id]
        if avaliada.vcus_liquidos <= 0:
            continue

        cluster = cluster_por_gleba.get(gleba.id)
        custo = max(avaliada.custo_entrada_brl, 1.0)
        eficiencia = avaliada.vcus_liquidos / custo * 1000

        destrava = False
        if cluster is not None:
            destrava = (
                cluster.area_contratada_ha < premissas.area_minima_cluster_ha
                and cluster.area_elegivel_ha >= premissas.area_minima_cluster_ha
            )

        candidatas.append(
            {
                "gleba": gleba,
                "avaliada": avaliada,
                "cluster": cluster,
                "eficiencia": eficiencia,
                "destrava": destrava,
                "peso": eficiencia * (1.6 if destrava else 1.0),
            }
        )

    candidatas.sort(key=lambda c: c["peso"], reverse=True)

    prioridades: List[PrioridadeAquisicao] = []
    for i, item in enumerate(candidatas, start=1):
        gleba: Gleba = item["gleba"]
        avaliada: GlebaAvaliada = item["avaliada"]
        cluster: Optional[ClusterCarbono] = item["cluster"]

        partes = []
        if item["destrava"]:
            partes.append(
                f"destrava a escala mínima do {cluster.id}" if cluster else "destrava escala"
            )
        partes.append(f"{_fmt(avaliada.vcus_liquidos)} tCO2e líquidos no horizonte")
        if avaliada.custo_entrada_brl > 0:
            partes.append(f"{_fmt(item['eficiencia'], 1)} tCO2e por R$ mil de entrada")
        else:
            partes.append("sem custo de entrada modelado")
        if avaliada.bloqueios:
            partes.append(f"ATENÇÃO: {avaliada.bloqueios[0].split('—')[0].strip().lower()}")

        prioridades.append(
            PrioridadeAquisicao(
                gleba_id=gleba.id,
                nome=gleba.nome,
                cluster_id=cluster.id if cluster else None,
                status_dominial=gleba.status_dominial,
                instrumento_recomendado=_instrumento_recomendado(gleba, avaliada),
                area_elegivel_ha=avaliada.area_elegivel_ha,
                vcus_liquidos=avaliada.vcus_liquidos,
                custo_entrada_brl=avaliada.custo_entrada_brl,
                vcus_por_mil_brl=round(item["eficiencia"], 2),
                destrava_escala=item["destrava"],
                prioridade=i,
                justificativa="; ".join(partes),
            )
        )

    return prioridades


# ---------------------------------------------------------------------------
# Análise consolidada
# ---------------------------------------------------------------------------

def _rodar_nucleo(
    land_bank: LandBank, premissas: PremissasCarbono, fator_produtividade: float = 1.0
) -> Tuple[Dict[str, GlebaAvaliada], List[ClusterCarbono]]:
    """Executa avaliação + clusterização + financeiro. Reutilizado nos cenários."""
    avaliadas = {
        g.id: avaliar_gleba(g, premissas, fator_produtividade) for g in land_bank.glebas
    }
    clusters = clusterizar(land_bank.glebas, avaliadas, premissas)
    por_id = {g.id: g for g in land_bank.glebas}
    for cluster in clusters:
        membros = [por_id[gid] for gid in cluster.glebas_ids]
        modelar_financeiro(cluster, membros, avaliadas, premissas, fator_produtividade)
    return avaliadas, clusters


def _premissas_cenario(
    base: PremissasCarbono, fator_preco: float
) -> PremissasCarbono:
    """Copia as premissas aplicando um fator sobre os preços de crédito."""
    dados = base.model_dump()
    dados["preco_tco2e_remocao_brl"] = base.preco_tco2e_remocao_brl * fator_preco
    dados["preco_tco2e_evitada_brl"] = base.preco_tco2e_evitada_brl * fator_preco
    dados["preco_tco2e_ifm_brl"] = base.preco_tco2e_ifm_brl * fator_preco
    return PremissasCarbono(**dados)


def analisar_land_bank(land_bank: LandBank) -> ResultadoLandBank:
    """
    Análise completa do Land Bank: elegibilidade, clusters, financeiro,
    prioridades de agregação e sensibilidade.
    """
    premissas = land_bank.premissas
    avaliadas, clusters = _rodar_nucleo(land_bank, premissas)
    lista_avaliadas = [avaliadas[g.id] for g in land_bank.glebas]

    # O preço de equilíbrio só faz sentido na rodada base e é caro de calcular,
    # então fica fora do núcleo reutilizado pelos cenários.
    por_id = {g.id: g for g in land_bank.glebas}
    for cluster in clusters:
        membros = [por_id[gid] for gid in cluster.glebas_ids]
        cluster.preco_equilibrio_brl = calcular_preco_equilibrio(
            cluster, membros, avaliadas, premissas
        )
        cluster.prevenda_minima = calcular_prevenda_minima(
            cluster, membros, avaliadas, premissas
        )
        cluster.alertas = _alertas_cluster(cluster, premissas)

    area_total = sum(g.area_total_ha for g in land_bank.glebas)
    area_elegivel = sum(a.area_elegivel_ha for a in lista_avaliadas)
    area_condicionada = sum(a.area_condicionada_ha for a in lista_avaliadas)
    area_contratada = sum(
        a.area_elegivel_ha
        for a in lista_avaliadas
        if a.status_dominial in (StatusDominial.PROPRIO, StatusDominial.CONTRATADO)
    )
    area_prospeccao = sum(
        a.area_elegivel_ha
        for a in lista_avaliadas
        if a.status_dominial in (StatusDominial.PROSPECCAO, StatusDominial.EM_NEGOCIACAO)
    )

    vcus = sum(c.vcus_liquidos for c in clusters)
    vcus_condicionados = sum(a.vcus_condicionados for a in lista_avaliadas)
    vcus_contratados = sum(
        a.vcus_liquidos
        for a in lista_avaliadas
        if a.status_dominial in (StatusDominial.PROPRIO, StatusDominial.CONTRATADO)
    )
    receita = sum(c.receita_bruta_brl for c in clusters)
    resultado = sum(c.resultado_liquido_zion_brl for c in clusters)
    vpl = sum(c.vpl_brl for c in clusters)
    readiness = (
        sum(a.readiness_score for a in lista_avaliadas) / len(lista_avaliadas)
        if lista_avaliadas
        else 0.0
    )

    prioridades = priorizar_aquisicoes(land_bank.glebas, avaliadas, clusters, premissas)
    cenarios = _montar_cenarios(land_bank, premissas)
    alertas = _alertas_portfolio(land_bank, lista_avaliadas, clusters, vcus, premissas)

    atingimento = None
    if land_bank.meta_tco2e:
        atingimento = round(vcus / land_bank.meta_tco2e, 4)

    return ResultadoLandBank(
        nome=land_bank.nome,
        data_analise=datetime.now().strftime("%d/%m/%Y %H:%M"),
        horizonte_anos=premissas.horizonte_anos,
        total_glebas=len(land_bank.glebas),
        area_total_ha=round(area_total, 2),
        area_elegivel_ha=round(area_elegivel, 2),
        area_condicionada_ha=round(area_condicionada, 2),
        area_contratada_ha=round(area_contratada, 2),
        area_prospeccao_ha=round(area_prospeccao, 2),
        vcus_liquidos=round(vcus, 1),
        vcus_condicionados=round(vcus_condicionados, 1),
        vcus_contratados=round(vcus_contratados, 1),
        receita_bruta_brl=round(receita, 2),
        resultado_liquido_zion_brl=round(resultado, 2),
        vpl_total_brl=round(vpl, 2),
        readiness_medio=round(readiness, 2),
        meta_tco2e=land_bank.meta_tco2e,
        atingimento_meta=atingimento,
        glebas=lista_avaliadas,
        clusters=clusters,
        prioridades=prioridades,
        cenarios=cenarios,
        alertas=alertas,
        premissas=premissas.model_dump(),
    )


def _montar_cenarios(land_bank: LandBank, base: PremissasCarbono) -> List[CenarioCarbono]:
    """Sensibilidade sobre preço do crédito e produtividade de carbono."""
    definicoes = [
        ("conservador", 0.60, 0.80),
        ("base", 1.00, 1.00),
        ("otimista", 1.45, 1.10),
    ]
    cenarios: List[CenarioCarbono] = []

    for nome, fator_preco, fator_prod in definicoes:
        premissas = _premissas_cenario(base, fator_preco)
        _, clusters = _rodar_nucleo(land_bank, premissas, fator_prod)
        cenarios.append(
            CenarioCarbono(
                nome=nome,
                fator_preco=fator_preco,
                fator_produtividade=fator_prod,
                vcus_liquidos=round(sum(c.vcus_liquidos for c in clusters), 1),
                receita_bruta_brl=round(sum(c.receita_bruta_brl for c in clusters), 2),
                resultado_liquido_zion_brl=round(
                    sum(c.resultado_liquido_zion_brl for c in clusters), 2
                ),
                vpl_brl=round(sum(c.vpl_brl for c in clusters), 2),
            )
        )
    return cenarios


def _alertas_portfolio(
    land_bank: LandBank,
    avaliadas: List[GlebaAvaliada],
    clusters: List[ClusterCarbono],
    vcus: float,
    premissas: PremissasCarbono,
) -> List[str]:
    """Riscos e gargalos do portfólio como um todo."""
    alertas: List[str] = []

    bloqueadas = [a for a in avaliadas if a.bloqueios]
    if bloqueadas:
        alertas.append(
            f"{len(bloqueadas)} gleba(s) com bloqueio duro de elegibilidade: "
            + ", ".join(a.gleba_id for a in bloqueadas)
        )

    sem_car = [a for a in avaliadas if any("CAR" in p for p in a.pendencias)]
    if sem_car:
        alertas.append(
            f"{len(sem_car)} gleba(s) sem CAR ativo — nenhum projeto entra em validação assim: "
            + ", ".join(a.gleba_id for a in sem_car)
        )

    subescala = [c for c in clusters if c.escala == "subescala"]
    if subescala:
        total_gap = sum(c.gap_escala_ha for c in subescala)
        alertas.append(
            f"{len(subescala)} cluster(s) em subescala, faltando {_fmt(total_gap)} ha no total "
            f"para atingir o mínimo de {_fmt(premissas.area_minima_cluster_ha)} ha por projeto."
        )

    if land_bank.meta_tco2e and vcus < land_bank.meta_tco2e:
        deficit = land_bank.meta_tco2e - vcus
        fator_medio = 10.0
        ha_faltantes = deficit / (fator_medio * premissas.horizonte_anos * 0.78)
        alertas.append(
            f"Meta de {_fmt(land_bank.meta_tco2e)} tCO2e não atingida: faltam {_fmt(deficit)} tCO2e, "
            f"o equivalente a aproximadamente {_fmt(ha_faltantes)} ha adicionais de restauração."
        )

    condicionadas = sum(a.area_condicionada_ha for a in avaliadas)
    if condicionadas > 0:
        alertas.append(
            f"{_fmt(condicionadas)} ha classificados como potencial condicionado (APP/Reserva Legal). "
            f"Só viram crédito se a adicionalidade for defendida além da obrigação legal — "
            f"não usar essa área em projeção de captação."
        )

    return alertas

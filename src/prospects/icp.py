"""
Perfil de cliente ideal (ICP) da Zion e pontuação de aderência.

Heurística determinística, não previsão: pontua o quanto um prospect se parece
com quem a Zion já sabe atender. Serve para ordenar a fila de abordagem, não
para prever fechamento.
"""

import logging
from typing import List, Optional, Tuple

from src.models.prospect import Modalidade, Prospect

logger = logging.getLogger(__name__)


# UFs por proximidade dos mercados emissores que a Zion já opera.
# Peso maior onde o deslocamento de fim de semana é viável por estrada.
UF_PRIORITARIA = {"SC": 1.0, "RS": 0.9, "PR": 0.9, "SP": 0.9, "MG": 0.8, "RJ": 0.8}
UF_EXPANSAO = {"GO": 0.7, "BA": 0.7, "ES": 0.6, "MS": 0.6, "MT": 0.5, "PE": 0.5, "CE": 0.5}

BIOMA_VOCACAO = {
    "mata atlântica": 1.0,
    "pampa": 0.8,
    "cerrado": 0.8,
    "amazônia": 0.7,
    "pantanal": 0.7,
    "caatinga": 0.6,
}

# Faixas onde o modelo Zion (poucas unidades, ticket alto) fecha conta.
AREA_IDEAL_HA = (3.0, 500.0)
UNIDADES_IDEAL = (5, 40)


def _pontuar_territorio(p: Prospect) -> Tuple[float, List[str]]:
    """Pontua UF e bioma. Máximo 3,0."""
    pontos, motivos = 0.0, []

    uf = (p.territorio.uf or "").upper()
    if uf in UF_PRIORITARIA:
        peso = UF_PRIORITARIA[uf]
        pontos += 2.0 * peso
        motivos.append(f"{uf} é mercado prioritário")
    elif uf in UF_EXPANSAO:
        peso = UF_EXPANSAO[uf]
        pontos += 2.0 * peso
        motivos.append(f"{uf} é frente de expansão")
    elif uf:
        motivos.append(f"{uf} fora das praças mapeadas")

    bioma = (p.territorio.bioma or "").strip().lower()
    if bioma in BIOMA_VOCACAO:
        pontos += 1.0 * BIOMA_VOCACAO[bioma]
        motivos.append(f"bioma {bioma} com vocação mapeada")

    return pontos, motivos


def _pontuar_ativo(p: Prospect) -> Tuple[float, List[str]]:
    """Pontua o que a pessoa já tem: terra ou operação. Máximo 4,0."""
    pontos, motivos = 0.0, []
    area, unidades = p.territorio.area_ha, p.territorio.unidades

    if area is not None:
        minimo, maximo = AREA_IDEAL_HA
        if minimo <= area <= maximo:
            pontos += 4.0
            motivos.append(f"{area:g} ha dentro da faixa que o modelo atende")
        elif area < minimo:
            pontos += 1.0
            motivos.append(f"{area:g} ha é pequeno para o modelo")
        else:
            pontos += 2.5
            motivos.append(f"{area:g} ha exige fasear a implantação")

    if unidades is not None:
        minimo, maximo = UNIDADES_IDEAL
        if minimo <= unidades <= maximo:
            pontos += 4.0
            motivos.append(f"{unidades} UHs é porte de hotelaria de experiência")
        elif unidades < minimo:
            pontos += 1.5
            motivos.append(f"{unidades} UHs não sustenta estrutura de gestão")
        else:
            pontos += 1.0
            motivos.append(f"{unidades} UHs foge do posicionamento boutique")

    if area is None and unidades is None:
        motivos.append("sem área nem número de unidades — falta qualificar")

    return min(pontos, 4.0), motivos


def _pontuar_contato(p: Prospect) -> Tuple[float, List[str]]:
    """Pontua o quanto dá para agir sobre o registro. Máximo 3,0."""
    pontos, motivos = 0.0, []

    canais = sum(bool(c) for c in (p.email, p.telefone, p.instagram))
    if canais:
        pontos += min(canais, 2) * 1.0
        motivos.append(f"{canais} canal(is) de contato")
    else:
        motivos.append("sem canal de contato")

    if p.modalidade != Modalidade.INDEFINIDA:
        pontos += 1.0
        motivos.append(f"modalidade definida: {p.modalidade.value}")

    return min(pontos, 3.0), motivos


def pontuar(p: Prospect) -> Prospect:
    """
    Calcula a aderência ao ICP, de 0 a 10, e registra o porquê no próprio
    prospect. Escreve em `score` e `score_motivos`.
    """
    if p.nao_contatar:
        p.score = 0.0
        p.score_motivos = ["titular pediu para não ser contatado"]
        return p

    total = 0.0
    motivos: List[str] = []
    for parcela, razoes in (_pontuar_territorio(p), _pontuar_ativo(p), _pontuar_contato(p)):
        total += parcela
        motivos.extend(razoes)

    p.score = round(min(total, 10.0), 1)
    p.score_motivos = motivos
    return p


def classificar(score: Optional[float]) -> str:
    """Traduz o score na fila de abordagem."""
    if score is None:
        return "não pontuado"
    if score >= 8.0:
        return "prioridade alta"
    if score >= 6.0:
        return "prioridade média"
    if score >= 4.0:
        return "qualificar antes"
    return "baixa aderência"


def inferir_modalidade(p: Prospect) -> Modalidade:
    """
    Chuta a modalidade a partir do que o prospect tem.

    Quem tem terra e nenhuma operação é Development. Quem já opera é
    Management ou Collection — e essa distinção depende de posicionamento,
    que nenhum dado coletado revela. Fica em Management, para revisão humana.
    """
    tem_terra = p.territorio.area_ha is not None and p.territorio.area_ha > 0
    tem_operacao = p.territorio.unidades is not None and p.territorio.unidades > 0

    if tem_operacao:
        return Modalidade.MANAGEMENT
    if tem_terra:
        return Modalidade.DEVELOPMENT
    return Modalidade.INDEFINIDA

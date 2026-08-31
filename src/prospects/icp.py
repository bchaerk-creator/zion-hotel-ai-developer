"""
Perfil de cliente ideal (ICP) da Zion.

A pontuação vive em `src.prospects.scoring` (ZION LEAD SCORE, 0–100). Este
módulo guarda só os parâmetros do perfil e a inferência de modalidade — ter
duas escalas gravando no mesmo campo `score` produzia uma coluna sem
significado, misturando 8,5 e 81,8.
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

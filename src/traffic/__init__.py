"""
ZION TRAFFIC & ACQUISITION ARCHITECT™ — aquisição, diagnóstico e atribuição.
"""

from src.traffic.atribuicao import atribuir, leitura_da_atribuicao
from src.traffic.diagnostico import decidir, diagnosticar
from src.traffic.metricas import (
    agregar,
    avaliar_gate,
    calcular_metricas,
    comparar_proporcoes,
    prob_zero_conversoes,
    volume_suficiente,
)
from src.traffic.relatorio import analisar_conta, gerar_relatorio_trafego

__all__ = [
    "avaliar_gate",
    "calcular_metricas",
    "agregar",
    "volume_suficiente",
    "prob_zero_conversoes",
    "comparar_proporcoes",
    "diagnosticar",
    "decidir",
    "atribuir",
    "leitura_da_atribuicao",
    "analisar_conta",
    "gerar_relatorio_trafego",
]

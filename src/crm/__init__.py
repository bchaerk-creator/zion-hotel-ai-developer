"""
ZION CRM & LEAD INTELLIGENCE™ — qualificação, roteamento e inteligência comercial.
"""

from src.crm.engine import calcular_score, qualificar, rotear
from src.crm.operacoes import analisar_base, analisar_funil, auditar_base, listar_reativacao
from src.crm.relatorio import briefing_lead, gerar_painel_territorial, gerar_relatorio_comercial
from src.crm.territorio import (
    consolidar_territorio,
    contar_oportunidades,
    listar_originacao,
    somar_areas,
    somar_investimentos,
    sugerir_vinculos,
)

__all__ = [
    "calcular_score",
    "rotear",
    "qualificar",
    "analisar_base",
    "auditar_base",
    "analisar_funil",
    "listar_reativacao",
    "gerar_relatorio_comercial",
    "briefing_lead",
    "consolidar_territorio",
    "contar_oportunidades",
    "somar_investimentos",
    "somar_areas",
    "listar_originacao",
    "sugerir_vinculos",
    "gerar_painel_territorial",
]

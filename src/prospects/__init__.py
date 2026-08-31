"""
Carteira de prospects da Zion.

O núcleo (modelo, repositório, ICP) não tem dependência externa e roda no
Python 3.11 do projeto. A coleta automática via ScrapeGraphAI é opcional e
só é importada quando pedida — ver `src.prospects.coletor`.
"""

from src.prospects.icp import inferir_modalidade
from src.prospects.scoring import classificar_lead, pontuar_lead
from src.prospects.repositorio import RepositorioProspects, gerar_id

__all__ = [
    "RepositorioProspects",
    "gerar_id",
    "pontuar_lead",
    "classificar_lead",
    "inferir_modalidade",
]

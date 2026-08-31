"""
Carteira de prospects da Zion.

O núcleo (modelo, repositório, ICP) não tem dependência externa e roda no
Python 3.11 do projeto. A coleta automática via ScrapeGraphAI é opcional e
só é importada quando pedida — ver `src.prospects.coletor`.
"""

from src.prospects.icp import classificar, inferir_modalidade, pontuar
from src.prospects.repositorio import RepositorioProspects, gerar_id

__all__ = [
    "RepositorioProspects",
    "gerar_id",
    "pontuar",
    "classificar",
    "inferir_modalidade",
]

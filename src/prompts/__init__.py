"""
Zion Hotel AI Developer - System Prompts Especializados
"""

from .base import SYSTEM_PROMPT_BASE
from .zion_score import PROMPT_ZION_SCORE
from .market import PROMPT_MARKET_STUDY
from .financial import PROMPT_FINANCIAL_MODEL
from .product import PROMPT_PRODUCT_DEFINITION
from .business import PROMPT_BUSINESS_STRUCTURE
from .investor import PROMPT_INVESTOR_PACKAGE
from .governance import PROMPT_GOVERNANCE
from .land_bank import PROMPT_LAND_BANK
from .knowledge import PROMPT_KNOWLEDGE_ENGINE
from .crm import PROMPT_CRM

__all__ = [
    "SYSTEM_PROMPT_BASE",
    "PROMPT_ZION_SCORE",
    "PROMPT_MARKET_STUDY",
    "PROMPT_FINANCIAL_MODEL",
    "PROMPT_PRODUCT_DEFINITION",
    "PROMPT_BUSINESS_STRUCTURE",
    "PROMPT_INVESTOR_PACKAGE",
    "PROMPT_GOVERNANCE",
    "PROMPT_LAND_BANK",
    "PROMPT_KNOWLEDGE_ENGINE",
    "PROMPT_CRM",
]

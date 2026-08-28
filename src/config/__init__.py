"""
Zion Hotel AI Developer - Configuração do Sistema
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Diretórios base
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = Path(os.getenv("ZION_OUTPUT_DIR", str(BASE_DIR / "output")))

# Configuração de LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
ZION_MODEL = os.getenv("ZION_MODEL", "gpt-5-mini")
ZION_THINKING_MODEL = os.getenv("ZION_THINKING_MODEL", "gpt-5")
ZION_FAST_MODEL = os.getenv("ZION_FAST_MODEL", "gpt-5-nano")

# Configuração do Agente
AGENT_NAME = os.getenv("ZION_AGENT_NAME", "Zion Hotel AI Developer")
AGENT_VERSION = os.getenv("ZION_AGENT_VERSION", "1.0.0")
LOG_LEVEL = os.getenv("ZION_LOG_LEVEL", "INFO")

# Configuração de Output
REPORTS_FORMAT = os.getenv("ZION_REPORTS_FORMAT", "markdown")
LANGUAGE = os.getenv("ZION_LANGUAGE", "pt-BR")

# Etapas do método Zion
ZION_STAGES = {
    0: "Diagnóstico Preliminar (Zion Score™)",
    1: "Estudo de Viabilidade Mercadológica",
    2: "Estudo de Viabilidade Econômico-Financeira",
    3: "Definição de Produto, Posicionamento e Master Plan Conceitual",
    4: "Estruturação do Negócio (Societário e Jurídico)",
    5: "Modelagem e Apresentação para Investidores",
    6: "Acompanhamento e Consultoria de Implantação",
}

# Módulos transversais — rodam fora da sequência da Pirâmide Invertida©
ZION_MODULOS = {
    7: "Land Bank — Agregação Territorial e Crédito de Carbono",
}

# Tudo que o orquestrador sabe executar
ZION_ETAPAS_EXECUTAVEIS = {**ZION_STAGES, **ZION_MODULOS}

# Pilares comerciais — fonte única da estrutura de receita da Zion
from src.config.pilares import (  # noqa: E402
    CADEIA_DE_VALOR,
    ORDEM_PILARES,
    PILARES,
    PilarComercial,
    listar_pilares,
    obter_pilar,
    pilares_da_etapa,
)

# Garantir que o diretório de output existe
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

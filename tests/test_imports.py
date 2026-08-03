"""
Testes básicos de importação para validar a estrutura do projeto.
"""

import pytest


def test_import_config():
    """Testa importação do módulo de configuração."""
    from src.config import ZION_STAGES, AGENT_NAME, AGENT_VERSION
    assert len(ZION_STAGES) == 7
    assert AGENT_NAME == "Zion Hotel AI Developer"
    assert AGENT_VERSION == "1.0.0"


def test_import_models():
    """Testa importação dos modelos de dados."""
    from src.models.project import ProjectInput, ProjectProfile, LocationData
    from src.models.zion_score import ZionScoreResult
    from src.models.market import MarketStudyResult
    from src.models.financial import FinancialModelResult
    from src.models.product import ProductDefinitionResult
    from src.models.business import BusinessStructureResult
    from src.models.investor import InvestorPackageResult


def test_import_agents():
    """Testa importação dos agentes."""
    from src.agents.orchestrator import ZionOrchestrator
    from src.agents.zion_score_agent import ZionScoreAgent
    from src.agents.market_agent import MarketAgent
    from src.agents.financial_agent import FinancialAgent
    from src.agents.product_agent import ProductAgent
    from src.agents.business_agent import BusinessAgent
    from src.agents.investor_agent import InvestorAgent
    from src.agents.governance_agent import GovernanceAgent


def test_zion_stages_complete():
    """Verifica que todas as etapas estão definidas."""
    from src.config import ZION_STAGES
    for i in range(7):
        assert i in ZION_STAGES, f"Etapa {i} não definida"


def test_project_input_model():
    """Testa criação de um ProjectInput válido."""
    from src.models.project import ProjectInput, LocationData

    location = LocationData(
        cidade="Florianópolis",
        estado="SC",
        pais="Brasil",
    )

    project = ProjectInput(
        nome_projeto="Teste",
        localizacao=location,
    )

    assert project.nome_projeto == "Teste"
    assert project.localizacao.cidade == "Florianópolis"

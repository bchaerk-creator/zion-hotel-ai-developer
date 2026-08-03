"""
Agente especializado para Etapa 1 — Estudo de Viabilidade Mercadológica.
"""

import logging
from typing import Dict, Any

from .base_agent import BaseAgent
from src.prompts import PROMPT_MARKET_STUDY

logger = logging.getLogger(__name__)


class MarketAgent(BaseAgent):
    """Agente responsável pelo estudo de viabilidade mercadológica."""

    def __init__(self):
        super().__init__(etapa=1, nome="Market Intelligence Agent")

    @property
    def system_prompt(self) -> str:
        return PROMPT_MARKET_STUDY

    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa o estudo de viabilidade mercadológica.

        Args:
            project_data: Dados do projeto com resultado da Etapa 0

        Returns:
            Resultado do estudo de mercado
        """
        logger.info(f"Iniciando estudo de viabilidade mercadológica: {project_data.get('nome_projeto', 'N/A')}")

        # Construir contexto com dados anteriores
        context = self._build_context(project_data)

        # Executar análise de mercado com raciocínio
        analysis = self.analyze(
            user_input="Realize o estudo completo de viabilidade mercadológica para este projeto, "
                       "incluindo análise de demanda, mapeamento de concorrência, benchmark estratégico "
                       "e posicionamento recomendado.",
            context=context,
            use_thinking=True,
        )

        # Gerar relatório
        report_path = self.generate_report(
            content=analysis,
            title="Estudo de Viabilidade Mercadológica",
            projeto_nome=project_data.get("nome_projeto", "Projeto"),
        )

        logger.info(f"Estudo de mercado concluído. Relatório: {report_path}")

        return {
            "etapa": 1,
            "status": "concluido",
            "analise": analysis,
            "relatorio_path": report_path,
            "projeto_nome": project_data.get("nome_projeto", "Projeto"),
        }

    def analyze_demand(self, project_data: Dict[str, Any]) -> str:
        """Análise focada em demanda."""
        context = self._build_context(project_data)
        return self.analyze(
            user_input="Foque na análise de demanda: existe demanda real para este destino? "
                       "Qual o perfil do visitante, volume estimado e disposição de pagamento?",
            context=context,
        )

    def analyze_competition(self, project_data: Dict[str, Any]) -> str:
        """Análise focada em concorrência."""
        context = self._build_context(project_data)
        return self.analyze(
            user_input="Foque no mapeamento da oferta concorrente: quem são os concorrentes, "
                       "quantas UHs oferecem, que ADR praticam, e quais são seus pontos fortes e fracos?",
            context=context,
        )

    def analyze_benchmark(self, project_data: Dict[str, Any]) -> str:
        """Análise focada em benchmark."""
        context = self._build_context(project_data)
        return self.analyze(
            user_input="Foque no benchmark estratégico: quais são as referências nacionais e internacionais "
                       "para este tipo de produto? Que oportunidades de diferenciação existem?",
            context=context,
        )

    def _build_context(self, project_data: Dict[str, Any]) -> str:
        """Constrói o contexto com dados do projeto e etapas anteriores."""
        lines = []

        lines.append(f"Projeto: {project_data.get('nome_projeto', 'N/A')}")

        if "localizacao" in project_data:
            loc = project_data["localizacao"]
            if isinstance(loc, dict):
                lines.append(f"Localização: {loc.get('cidade', '')}, {loc.get('estado', '')} - {loc.get('pais', 'Brasil')}")
            else:
                lines.append(f"Localização: {loc}")

        if "tipo_produto" in project_data:
            lines.append(f"Tipo de produto: {project_data['tipo_produto']}")

        if "zion_score_resultado" in project_data:
            lines.append(f"\nResultado da Etapa 0 (Zion Score):\n{project_data['zion_score_resultado']}")

        return "\n".join(lines)

"""
Agente especializado para Etapa 6 — Acompanhamento e Consultoria de Implantação.
"""

import logging
from typing import Dict, Any

from .base_agent import BaseAgent
from src.prompts import PROMPT_GOVERNANCE

logger = logging.getLogger(__name__)


class GovernanceAgent(BaseAgent):
    """Agente responsável pela governança de implantação."""

    def __init__(self):
        super().__init__(etapa=6, nome="Implementation Governance Agent")

    @property
    def system_prompt(self) -> str:
        return PROMPT_GOVERNANCE

    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa uma revisão de governança do projeto.

        Args:
            project_data: Dados completos do projeto com status de implantação

        Returns:
            Resultado da revisão de governança
        """
        logger.info(f"Executando revisão de governança: {project_data.get('nome_projeto', 'N/A')}")

        context = self._build_context(project_data)

        analysis = self.analyze(
            user_input="Realize a revisão de governança do projeto: status atual, "
                       "aderência à tese original, milestones, riscos e recomendações.",
            context=context,
        )

        report_path = self.generate_report(
            content=analysis,
            title="Relatório de Governança — Acompanhamento de Implantação",
            projeto_nome=project_data.get("nome_projeto", "Projeto"),
        )

        return {
            "etapa": 6,
            "status": "concluido",
            "analise": analysis,
            "relatorio_path": report_path,
            "projeto_nome": project_data.get("nome_projeto", "Projeto"),
        }

    def _build_context(self, project_data: Dict[str, Any]) -> str:
        """Constrói contexto para governança."""
        lines = [f"Projeto: {project_data.get('nome_projeto', 'N/A')}"]

        if "status_implantacao" in project_data:
            lines.append(f"Status: {project_data['status_implantacao']}")
        if "milestones" in project_data:
            lines.append(f"Milestones: {project_data['milestones']}")
        if "decisoes_pendentes" in project_data:
            lines.append(f"Decisões pendentes: {project_data['decisoes_pendentes']}")

        return "\n".join(lines)

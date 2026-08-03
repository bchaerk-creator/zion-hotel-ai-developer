"""
Agente especializado para Etapa 4 — Estruturação do Negócio.
"""

import logging
from typing import Dict, Any

from .base_agent import BaseAgent
from src.prompts import PROMPT_BUSINESS_STRUCTURE

logger = logging.getLogger(__name__)


class BusinessAgent(BaseAgent):
    """Agente responsável pela estruturação societária e jurídica."""

    def __init__(self):
        super().__init__(etapa=4, nome="Business Structuring Agent")

    @property
    def system_prompt(self) -> str:
        return PROMPT_BUSINESS_STRUCTURE

    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a estruturação do negócio.

        Args:
            project_data: Dados do projeto com resultados das Etapas 0-3

        Returns:
            Resultado da estruturação
        """
        logger.info(f"Iniciando estruturação do negócio: {project_data.get('nome_projeto', 'N/A')}")

        context = self._build_context(project_data)

        analysis = self.analyze(
            user_input="Estruture o negócio: defina o modelo societário, tipo de SPE, "
                       "estratégia de entrada de investidores, governança e checklist jurídico. "
                       "A estrutura deve ser coerente com o modelo financeiro e preparada para captação.",
            context=context,
            use_thinking=True,
        )

        report_path = self.generate_report(
            content=analysis,
            title="Estruturação do Negócio — Societário e Jurídico",
            projeto_nome=project_data.get("nome_projeto", "Projeto"),
        )

        logger.info(f"Estruturação concluída. Relatório: {report_path}")

        return {
            "etapa": 4,
            "status": "concluido",
            "analise": analysis,
            "relatorio_path": report_path,
            "projeto_nome": project_data.get("nome_projeto", "Projeto"),
        }

    def _build_context(self, project_data: Dict[str, Any]) -> str:
        """Constrói contexto acumulado."""
        lines = [f"Projeto: {project_data.get('nome_projeto', 'N/A')}"]

        if "investimento_estimado_brl" in project_data:
            lines.append(f"Investimento: R$ {project_data['investimento_estimado_brl']:,.2f}")

        if "financial_resultado" in project_data:
            lines.append(f"\nModelo Financeiro:\n{project_data['financial_resultado'][:2000]}")
        if "product_resultado" in project_data:
            lines.append(f"\nProduto Definido:\n{project_data['product_resultado'][:1500]}")

        return "\n".join(lines)

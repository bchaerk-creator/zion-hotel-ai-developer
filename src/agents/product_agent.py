"""
Agente especializado para Etapa 3 — Definição de Produto, Posicionamento e Master Plan.
"""

import logging
from typing import Dict, Any

from .base_agent import BaseAgent
from src.prompts import PROMPT_PRODUCT_DEFINITION

logger = logging.getLogger(__name__)


class ProductAgent(BaseAgent):
    """Agente responsável pela definição de produto e posicionamento."""

    def __init__(self):
        super().__init__(etapa=3, nome="Product Designer Agent")

    @property
    def system_prompt(self) -> str:
        return PROMPT_PRODUCT_DEFINITION

    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a definição de produto e posicionamento.

        Args:
            project_data: Dados do projeto com resultados das Etapas 0-2

        Returns:
            Resultado da definição de produto
        """
        logger.info(f"Iniciando definição de produto: {project_data.get('nome_projeto', 'N/A')}")

        context = self._build_context(project_data)

        analysis = self.analyze(
            user_input="Defina o produto hoteleiro completo: conceito central, posicionamento, "
                       "narrativa de marca, arquitetura de bandeira e diretrizes para o master plan. "
                       "O produto deve ser coerente com o mercado validado e o modelo financeiro aprovado.",
            context=context,
            use_thinking=True,
        )

        report_path = self.generate_report(
            content=analysis,
            title="Definição de Produto, Posicionamento e Master Plan Conceitual",
            projeto_nome=project_data.get("nome_projeto", "Projeto"),
        )

        logger.info(f"Definição de produto concluída. Relatório: {report_path}")

        return {
            "etapa": 3,
            "status": "concluido",
            "analise": analysis,
            "relatorio_path": report_path,
            "projeto_nome": project_data.get("nome_projeto", "Projeto"),
        }

    def _build_context(self, project_data: Dict[str, Any]) -> str:
        """Constrói contexto com dados acumulados."""
        lines = [f"Projeto: {project_data.get('nome_projeto', 'N/A')}"]

        for key in ["localizacao", "tipo_produto", "publico_alvo_pretendido", "diferenciais_pretendidos"]:
            if key in project_data:
                lines.append(f"{key}: {project_data[key]}")

        if "financial_resultado" in project_data:
            lines.append(f"\nResultado Financeiro (Etapa 2):\n{project_data['financial_resultado']}")
        if "market_study_resultado" in project_data:
            lines.append(f"\nResultado de Mercado (Etapa 1):\n{project_data['market_study_resultado']}")

        return "\n".join(lines)

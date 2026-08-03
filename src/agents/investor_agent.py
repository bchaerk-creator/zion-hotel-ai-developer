"""
Agente especializado para Etapa 5 — Modelagem e Apresentação para Investidores.
"""

import logging
from typing import Dict, Any

from .base_agent import BaseAgent
from src.prompts import PROMPT_INVESTOR_PACKAGE

logger = logging.getLogger(__name__)


class InvestorAgent(BaseAgent):
    """Agente responsável pela preparação de materiais para investidores."""

    def __init__(self):
        super().__init__(etapa=5, nome="Investor Readiness Agent")

    @property
    def system_prompt(self) -> str:
        return PROMPT_INVESTOR_PACKAGE

    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a preparação do pacote para investidores.

        Args:
            project_data: Dados completos do projeto (Etapas 0-4)

        Returns:
            Resultado com materiais para investidores
        """
        logger.info(f"Iniciando pacote para investidores: {project_data.get('nome_projeto', 'N/A')}")

        context = self._build_context(project_data)

        analysis = self.analyze(
            user_input="Prepare o pacote completo para captação de investimento: "
                       "tese de investimento, teaser executivo, estrutura do information memorandum, "
                       "roteiro do pitch deck, checklist do data room, adequação por perfil de investidor, "
                       "cronograma de captação e use of proceeds.",
            context=context,
            use_thinking=True,
        )

        report_path = self.generate_report(
            content=analysis,
            title="Modelagem e Apresentação para Investidores",
            projeto_nome=project_data.get("nome_projeto", "Projeto"),
        )

        logger.info(f"Pacote para investidores concluído. Relatório: {report_path}")

        return {
            "etapa": 5,
            "status": "concluido",
            "analise": analysis,
            "relatorio_path": report_path,
            "projeto_nome": project_data.get("nome_projeto", "Projeto"),
        }

    def generate_teaser(self, project_data: Dict[str, Any]) -> str:
        """Gera o teaser executivo isoladamente."""
        context = self._build_context(project_data)
        return self.analyze(
            user_input="Gere o teaser executivo (1-2 páginas) para este projeto. "
                       "Deve ser não confidencial, atrativo e despertar interesse do investidor.",
            context=context,
        )

    def generate_pitch_script(self, project_data: Dict[str, Any]) -> str:
        """Gera o roteiro de apresentação para investidores."""
        context = self._build_context(project_data)
        return self.analyze(
            user_input="Crie o roteiro (script) de apresentação executiva para reunião com investidores. "
                       "Deve cobrir: abertura, oportunidade, mercado, produto, números, estrutura, ask e fechamento.",
            context=context,
        )

    def _build_context(self, project_data: Dict[str, Any]) -> str:
        """Constrói contexto completo do projeto."""
        lines = [f"Projeto: {project_data.get('nome_projeto', 'N/A')}"]

        for key in ["localizacao", "tipo_produto", "numero_unidades_estimado", "investimento_estimado_brl"]:
            if key in project_data:
                lines.append(f"{key}: {project_data[key]}")

        # Incluir resumos das etapas anteriores
        for etapa_key, label in [
            ("zion_score_resultado", "Zion Score (Etapa 0)"),
            ("market_study_resultado", "Mercado (Etapa 1)"),
            ("financial_resultado", "Financeiro (Etapa 2)"),
            ("product_resultado", "Produto (Etapa 3)"),
            ("business_resultado", "Estrutura (Etapa 4)"),
        ]:
            if etapa_key in project_data:
                content = project_data[etapa_key]
                if len(content) > 1500:
                    content = content[:1500] + "..."
                lines.append(f"\n{label}:\n{content}")

        return "\n".join(lines)

"""
Agente especializado para Etapa 2 — Estudo de Viabilidade Econômico-Financeira.
"""

import logging
from typing import Dict, Any

from .base_agent import BaseAgent
from src.prompts import PROMPT_FINANCIAL_MODEL

logger = logging.getLogger(__name__)


class FinancialAgent(BaseAgent):
    """Agente responsável pela modelagem econômico-financeira."""

    def __init__(self):
        super().__init__(etapa=2, nome="Financial Engine Agent")

    @property
    def system_prompt(self) -> str:
        return PROMPT_FINANCIAL_MODEL

    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a modelagem econômico-financeira completa.

        Args:
            project_data: Dados do projeto com resultados das Etapas 0 e 1

        Returns:
            Resultado da modelagem financeira
        """
        logger.info(f"Iniciando modelagem financeira: {project_data.get('nome_projeto', 'N/A')}")

        context = self._build_context(project_data)

        # Modelagem financeira requer raciocínio profundo
        analysis = self.analyze(
            user_input="Construa o modelo financeiro completo para este projeto hoteleiro, incluindo: "
                       "estimativa de CAPEX detalhada, projeção de receitas e despesas, DRE projetada, "
                       "fluxo de caixa para 10 anos, indicadores de retorno (TIR, VPL, Payback, Break-even), "
                       "análise de sensibilidade e três cenários (conservador, realista, otimista).",
            context=context,
            use_thinking=True,
        )

        report_path = self.generate_report(
            content=analysis,
            title="Estudo de Viabilidade Econômico-Financeira",
            projeto_nome=project_data.get("nome_projeto", "Projeto"),
        )

        logger.info(f"Modelagem financeira concluída. Relatório: {report_path}")

        return {
            "etapa": 2,
            "status": "concluido",
            "analise": analysis,
            "relatorio_path": report_path,
            "projeto_nome": project_data.get("nome_projeto", "Projeto"),
        }

    def calculate_capex(self, project_data: Dict[str, Any]) -> str:
        """Cálculo focado de CAPEX."""
        context = self._build_context(project_data)
        return self.analyze(
            user_input="Calcule a estimativa detalhada de CAPEX para este projeto, "
                       "incluindo construção, FF&E, infraestrutura, projetos, capital de giro e contingência.",
            context=context,
            use_thinking=True,
        )

    def project_revenue(self, project_data: Dict[str, Any]) -> str:
        """Projeção focada de receitas."""
        context = self._build_context(project_data)
        return self.analyze(
            user_input="Projete as receitas operacionais anuais, detalhando hospedagem, A&B e outras receitas. "
                       "Use as premissas de ocupação e ADR validadas no estudo de mercado.",
            context=context,
        )

    def sensitivity_analysis(self, project_data: Dict[str, Any]) -> str:
        """Análise de sensibilidade."""
        context = self._build_context(project_data)
        return self.analyze(
            user_input="Realize a análise de sensibilidade: como variações de ±10pp na ocupação "
                       "e ±15% no ADR impactam TIR, VPL e Payback? Apresente em tabela.",
            context=context,
            use_thinking=True,
        )

    def _build_context(self, project_data: Dict[str, Any]) -> str:
        """Constrói contexto com dados do projeto e etapas anteriores."""
        lines = []

        lines.append(f"Projeto: {project_data.get('nome_projeto', 'N/A')}")

        if "localizacao" in project_data:
            loc = project_data["localizacao"]
            if isinstance(loc, dict):
                lines.append(f"Localização: {loc.get('cidade', '')}, {loc.get('estado', '')}")
            else:
                lines.append(f"Localização: {loc}")

        if "tipo_produto" in project_data:
            lines.append(f"Tipo de produto: {project_data['tipo_produto']}")

        if "numero_unidades_estimado" in project_data:
            lines.append(f"Unidades: {project_data['numero_unidades_estimado']}")

        if "investimento_estimado_brl" in project_data:
            lines.append(f"Investimento estimado: R$ {project_data['investimento_estimado_brl']:,.2f}")

        if "market_study_resultado" in project_data:
            lines.append(f"\nResultado da Etapa 1 (Mercado):\n{project_data['market_study_resultado']}")

        if "zion_score_resultado" in project_data:
            lines.append(f"\nResultado da Etapa 0 (Zion Score):\n{project_data['zion_score_resultado']}")

        return "\n".join(lines)

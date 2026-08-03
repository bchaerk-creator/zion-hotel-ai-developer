"""
Agente especializado para Etapa 0 — Diagnóstico Preliminar (Zion Score™).
"""

import json
import logging
from typing import Dict, Any

from .base_agent import BaseAgent
from src.prompts import PROMPT_ZION_SCORE

logger = logging.getLogger(__name__)


class ZionScoreAgent(BaseAgent):
    """Agente responsável pelo diagnóstico preliminar e cálculo do Zion Score."""

    def __init__(self):
        super().__init__(etapa=0, nome="Zion Score Agent")

    @property
    def system_prompt(self) -> str:
        return PROMPT_ZION_SCORE

    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa o diagnóstico preliminar do projeto.

        Args:
            project_data: Dados do projeto incluindo localização, tipo pretendido, etc.

        Returns:
            Resultado com Zion Score e diagnóstico completo
        """
        logger.info(f"Iniciando diagnóstico Zion Score para: {project_data.get('nome_projeto', 'N/A')}")

        # Preparar input para o LLM
        project_summary = self._format_project_input(project_data)

        # Executar análise com raciocínio estendido para maior qualidade
        analysis = self.analyze(
            user_input=f"Realize o diagnóstico preliminar (Zion Score™) para o seguinte projeto:\n\n{project_summary}",
            use_thinking=True,
        )

        # Gerar relatório
        report_path = self.generate_report(
            content=analysis,
            title="Diagnóstico Preliminar — Zion Score™",
            projeto_nome=project_data.get("nome_projeto", "Projeto"),
        )

        logger.info(f"Diagnóstico concluído. Relatório salvo em: {report_path}")

        return {
            "etapa": 0,
            "status": "concluido",
            "analise": analysis,
            "relatorio_path": report_path,
            "projeto_nome": project_data.get("nome_projeto", "Projeto"),
        }

    def quick_score(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa um diagnóstico rápido (versão simplificada).

        Args:
            project_data: Dados básicos do projeto

        Returns:
            Score rápido com nota e recomendação
        """
        project_summary = self._format_project_input(project_data)

        result = self.llm.structured_output(
            messages=[
                {"role": "system", "content": self.full_system_prompt},
                {
                    "role": "user",
                    "content": f"Faça um diagnóstico rápido e atribua o Zion Score:\n\n{project_summary}",
                },
            ],
            schema={
                "type": "object",
                "properties": {
                    "zion_score": {"type": "number", "description": "Nota de 0 a 10"},
                    "classificacao": {"type": "string", "description": "excelente/bom/regular/insuficiente"},
                    "vocacao_principal": {"type": "string", "description": "Vocação turística principal"},
                    "adr_estimado_brl": {"type": "number", "description": "ADR estimado em BRL"},
                    "recomendacao": {"type": "string", "description": "Recomendação de prosseguimento"},
                    "resumo": {"type": "string", "description": "Resumo em 3 linhas"},
                },
                "required": ["zion_score", "classificacao", "vocacao_principal", "adr_estimado_brl", "recomendacao", "resumo"],
                "additionalProperties": False,
            },
            schema_name="zion_score_quick",
        )

        return result

    def _format_project_input(self, project_data: Dict[str, Any]) -> str:
        """Formata os dados do projeto para input do LLM."""
        lines = []

        if "nome_projeto" in project_data:
            lines.append(f"**Projeto:** {project_data['nome_projeto']}")

        if "localizacao" in project_data:
            loc = project_data["localizacao"]
            if isinstance(loc, dict):
                lines.append(f"**Localização:** {loc.get('cidade', '')}, {loc.get('estado', '')} - {loc.get('pais', 'Brasil')}")
                if loc.get("area_terreno_m2"):
                    lines.append(f"**Área do terreno:** {loc['area_terreno_m2']:,.0f} m²")
                if loc.get("distancia_aeroporto_km"):
                    lines.append(f"**Distância ao aeroporto:** {loc['distancia_aeroporto_km']} km")
            else:
                lines.append(f"**Localização:** {loc}")

        if "tipo_produto" in project_data:
            lines.append(f"**Tipo de produto pretendido:** {project_data['tipo_produto']}")

        if "numero_unidades_estimado" in project_data:
            lines.append(f"**Unidades estimadas:** {project_data['numero_unidades_estimado']}")

        if "investimento_estimado_brl" in project_data:
            lines.append(f"**Investimento estimado:** R$ {project_data['investimento_estimado_brl']:,.2f}")

        if "publico_alvo_pretendido" in project_data:
            lines.append(f"**Público-alvo pretendido:** {project_data['publico_alvo_pretendido']}")

        if "diferenciais_pretendidos" in project_data:
            difs = project_data["diferenciais_pretendidos"]
            if isinstance(difs, list):
                lines.append(f"**Diferenciais pretendidos:** {', '.join(difs)}")
            else:
                lines.append(f"**Diferenciais pretendidos:** {difs}")

        if "estagio_atual" in project_data:
            lines.append(f"**Estágio atual:** {project_data['estagio_atual']}")

        if "objetivos_proprietario" in project_data:
            lines.append(f"**Objetivos do proprietário:** {project_data['objetivos_proprietario']}")

        if "observacoes" in project_data:
            lines.append(f"**Observações:** {project_data['observacoes']}")

        return "\n".join(lines)

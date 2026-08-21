"""
Agente do módulo Land Bank — agregação territorial e originação de crédito de carbono.

A parte numérica é determinística e roda sem LLM (engine de carbono). O agente
acrescenta a camada estratégica: originação, negociação, estrutura e sequenciamento.
"""

import json
import logging
from typing import Any, Dict, Optional, Tuple

from .base_agent import BaseAgent
from src.models.land_bank import LandBank, ResultadoLandBank
from src.modules.carbon_engine import analisar_land_bank
from src.modules.land_bank_report import gerar_relatorio_land_bank
from src.prompts import PROMPT_LAND_BANK

logger = logging.getLogger(__name__)


class LandBankAgent(BaseAgent):
    """Agente responsável pelo portfólio territorial e pela tese de carbono."""

    def __init__(self):
        super().__init__(etapa=7, nome="Land Bank Agent")

    @property
    def system_prompt(self) -> str:
        return PROMPT_LAND_BANK

    # ------------------------------------------------------------------
    # Camada determinística
    # ------------------------------------------------------------------

    @staticmethod
    def carregar(dados: Dict[str, Any]) -> LandBank:
        """
        Constrói o Land Bank a partir de um dicionário.

        Aceita tanto o portfólio direto quanto um projeto que o carrega
        na chave 'land_bank'.
        """
        payload = dados.get("land_bank", dados)
        if "glebas" not in payload:
            raise ValueError(
                "Dados de Land Bank inválidos: nenhuma chave 'glebas' encontrada. "
                "Use data/exemplo_land_bank.json como referência de estrutura."
            )
        return LandBank(**payload)

    def analisar(self, dados: Dict[str, Any]) -> Tuple[ResultadoLandBank, str]:
        """
        Roda a engine de carbono e devolve o resultado com o relatório em Markdown.
        Não depende de LLM — pode rodar offline.
        """
        land_bank = self.carregar(dados)
        resultado = analisar_land_bank(land_bank)
        relatorio = gerar_relatorio_land_bank(resultado)
        logger.info(
            "Land Bank analisado: %s glebas, %.0f ha elegíveis, %.0f tCO2e líquidos",
            resultado.total_glebas,
            resultado.area_elegivel_ha,
            resultado.vcus_liquidos,
        )
        return resultado, relatorio

    # ------------------------------------------------------------------
    # Camada estratégica
    # ------------------------------------------------------------------

    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a análise completa do Land Bank: números pela engine,
        estratégia pelo LLM, relatório consolidado em disco.
        """
        resultado, relatorio_numerico = self.analisar(project_data)

        analise = self.analyze(
            user_input=(
                "Analise o Land Bank abaixo e produza a estratégia de agregação "
                "territorial e de originação de crédito de carbono.\n\n"
                f"{self._resumo_para_llm(resultado)}"
            ),
            use_thinking=True,
        )

        conteudo = f"{relatorio_numerico}\n\n---\n\n# Estratégia de Agregação\n\n{analise}"
        report_path = self.generate_report(
            content=conteudo,
            title="Land Bank — Agregação Territorial e Crédito de Carbono",
            projeto_nome=resultado.nome,
        )

        return {
            "etapa": 7,
            "status": "concluido",
            "analise": analise,
            "relatorio_numerico": relatorio_numerico,
            "relatorio_path": report_path,
            "resultado": resultado.model_dump(),
            "projeto_nome": resultado.nome,
        }

    def _resumo_para_llm(self, r: ResultadoLandBank) -> str:
        """
        Condensa o resultado da engine para o LLM.

        O fluxo de caixa ano a ano fica de fora de propósito: é volume sem uso
        estratégico e o que importa dele já está nos indicadores do cluster.
        """
        linhas = [
            f"# Land Bank: {r.nome}",
            f"Horizonte: {r.horizonte_anos} anos | Glebas: {r.total_glebas}",
            "",
            "## Consolidado",
            f"- Área total mapeada: {r.area_total_ha:,.0f} ha",
            f"- Área elegível: {r.area_elegivel_ha:,.0f} ha",
            f"- Área com adicionalidade condicionada: {r.area_condicionada_ha:,.0f} ha",
            f"- Área contratada: {r.area_contratada_ha:,.0f} ha",
            f"- Área em pipeline: {r.area_prospeccao_ha:,.0f} ha",
            f"- Créditos líquidos: {r.vcus_liquidos:,.0f} tCO2e",
            f"- Créditos já contratados: {r.vcus_contratados:,.0f} tCO2e",
            f"- Receita bruta projetada: R$ {r.receita_bruta_brl:,.0f}",
            f"- Resultado líquido Zion (nominal): R$ {r.resultado_liquido_zion_brl:,.0f}",
            f"- VPL consolidado: R$ {r.vpl_total_brl:,.0f}",
            f"- Carbon Readiness médio: {r.readiness_medio:.2f}/10",
        ]

        if r.meta_tco2e:
            linhas.append(
                f"- Meta: {r.meta_tco2e:,.0f} tCO2e "
                f"({(r.atingimento_meta or 0) * 100:.1f}% atingido)"
            )

        linhas += ["", "## Clusters"]
        for c in r.clusters:
            prevenda = (
                "dispensável" if c.prevenda_minima == 0
                else (f"{c.prevenda_minima * 100:.0f}%" if c.prevenda_minima else "não resolve")
            )
            linhas.append(
                f"- {c.id} ({c.nome}): {c.area_elegivel_ha:,.0f} ha elegíveis, "
                f"{c.area_contratada_ha:,.0f} ha contratados, {c.vcus_liquidos:,.0f} tCO2e, "
                f"VPL R$ {c.vpl_brl:,.0f}, TIR {(c.tir or 0) * 100:.1f}%, "
                f"custo R$ {c.custo_por_vcu_brl:,.2f}/tCO2e, "
                f"equilíbrio R$ {c.preco_equilibrio_brl or 0:,.2f}/tCO2e, "
                f"pré-venda mínima {prevenda}, escala: {c.escala}"
            )
            for alerta in c.alertas:
                linhas.append(f"  - alerta: {alerta}")

        linhas += ["", "## Glebas"]
        for g in r.glebas:
            linhas.append(
                f"- {g.gleba_id} {g.nome} ({g.municipio}/{g.uf}): "
                f"{g.area_total_ha:,.0f} ha totais, {g.area_elegivel_ha:,.0f} ha elegíveis, "
                f"{g.vcus_liquidos:,.0f} tCO2e, status {g.status_dominial.value}, "
                f"readiness {g.readiness_score:.1f} ({g.classificacao})"
            )
            for b in g.bloqueios:
                linhas.append(f"  - BLOQUEIO: {b}")
            for p in g.pendencias:
                linhas.append(f"  - pendência: {p}")

        linhas += ["", "## Fila de agregação sugerida pela engine"]
        for p in r.prioridades:
            linhas.append(
                f"{p.prioridade}. {p.gleba_id} {p.nome} — instrumento sugerido: "
                f"{p.instrumento_recomendado.value}, {p.area_elegivel_ha:,.0f} ha, "
                f"{p.vcus_liquidos:,.0f} tCO2e, entrada R$ {p.custo_entrada_brl:,.0f}, "
                f"{p.vcus_por_mil_brl:,.1f} tCO2e por R$ mil, "
                f"destrava escala: {'sim' if p.destrava_escala else 'não'}"
            )

        linhas += ["", "## Cenários"]
        for c in r.cenarios:
            linhas.append(
                f"- {c.nome}: {c.vcus_liquidos:,.0f} tCO2e, "
                f"receita R$ {c.receita_bruta_brl:,.0f}, VPL R$ {c.vpl_brl:,.0f}"
            )

        if r.alertas:
            linhas += ["", "## Alertas do portfólio"]
            linhas += [f"- {a}" for a in r.alertas]

        return "\n".join(linhas)

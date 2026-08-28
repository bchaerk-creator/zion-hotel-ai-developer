"""
Agente do ZION CRM & LEAD INTELLIGENCE™.

Score, temperatura, roteamento, higiene, funil e reativação são determinísticos
e rodam sem LLM. O modelo entra na camada de julgamento comercial: abordagem,
mensagem e leitura de padrão.
"""

import logging
from datetime import date
from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent
from src.crm.models import BaseComercial, Lead, LeadQualificado, RelatorioComercial
from src.crm.operacoes import analisar_base
from src.crm.relatorio import briefing_lead, gerar_relatorio_comercial
from src.crm.engine import qualificar
from src.prompts import PROMPT_CRM

logger = logging.getLogger(__name__)


class CRMAgent(BaseAgent):
    """Inteligência comercial sobre a base de leads da Zion."""

    def __init__(self):
        super().__init__(etapa=9, nome="Zion CRM & Lead Intelligence")

    @property
    def system_prompt(self) -> str:
        return PROMPT_CRM

    # ------------------------------------------------------------------
    # Determinístico
    # ------------------------------------------------------------------

    @staticmethod
    def carregar(dados: Dict[str, Any]) -> BaseComercial:
        payload = dados.get("base_comercial", dados)
        if "leads" not in payload:
            raise ValueError(
                "Dados de CRM inválidos: nenhuma chave 'leads' encontrada. "
                "Use data/exemplo_base_comercial.json como referência."
            )
        return BaseComercial(**payload)

    def analisar(
        self, dados: Dict[str, Any], hoje: Optional[date] = None
    ) -> tuple[RelatorioComercial, str]:
        """ANALISAR CRM — roda a análise completa e devolve o relatório."""
        base = self.carregar(dados)
        relatorio = analisar_base(base, hoje)
        logger.info(
            "Base analisada: %s leads, %s oportunidades, %s achados de higiene",
            relatorio.total_leads, relatorio.oportunidades, len(relatorio.higiene),
        )
        return relatorio, gerar_relatorio_comercial(relatorio)

    def qualificar_lead(self, lead: Lead, hoje: Optional[date] = None) -> LeadQualificado:
        """QUALIFICAR LEAD — score, temperatura e roteamento."""
        score, roteamento = qualificar(lead, hoje)
        return LeadQualificado(lead=lead, score=score, roteamento=roteamento)

    def preparar_reuniao(self, lead: Lead, hoje: Optional[date] = None) -> str:
        """PREPARAR REUNIÃO — briefing determinístico do lead."""
        return briefing_lead(self.qualificar_lead(lead, hoje))

    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise da base com camada estratégica de IA."""
        relatorio, markdown = self.analisar(project_data)

        analise = self.analyze(
            user_input=(
                "Analise a base comercial abaixo e produza a leitura estratégica: "
                "padrões reais na base, prioridades da semana, abordagem recomendada para "
                "as cinco maiores oportunidades e onde o funil está perdendo gente.\n\n"
                f"{self._resumo_para_llm(relatorio)}"
            ),
            use_thinking=True,
        )

        conteudo = f"{markdown}\n\n---\n\n# Leitura Estratégica\n\n{analise}"
        report_path = self.generate_report(
            content=conteudo,
            title="Relatório Comercial Zion",
            projeto_nome="Base Comercial",
        )

        return {
            "etapa": 9,
            "status": "concluido",
            "analise": analise,
            "relatorio_numerico": markdown,
            "relatorio_path": report_path,
            "total_leads": relatorio.total_leads,
        }

    def _resumo_para_llm(self, r: RelatorioComercial) -> str:
        """Condensa o relatório para o modelo, sem o histórico completo de interações."""
        linhas = [
            f"# Base comercial em {r.data}",
            f"Leads: {r.total_leads} | Novos: {r.novos} | Oportunidades: {r.oportunidades} | "
            f"Quentes: {r.quentes} | Parados: {r.parados} | Follow-ups atrasados: {r.followups_atrasados}",
            f"Pipeline aberto: R$ {r.pipeline_aberto_brl:,.0f}",
            "",
            "## Leads qualificados (ordem de prioridade)",
        ]
        for q in r.qualificados:
            l, s, rot = q.lead, q.score, q.roteamento
            ativos = ", ".join(l.ativos.possui()) or "nenhum ativo confirmado"
            linhas.append(
                f"{q.prioridade}. {l.nome} ({l.perfil.value}) — estágio {l.estagio.value}, "
                f"{s.temperatura.value}, score {s.score:.1f} com confiança {s.confianca:.0%}. "
                f"Ativos: {ativos}. Porta: {rot.porta.value}. "
                f"Próximo passo: {rot.proximo_passo_logico}"
            )
            for alerta in s.alertas:
                linhas.append(f"   - alerta: {alerta}")
            if rot.nao_ofertar:
                linhas.append(f"   - não ofertar: {'; '.join(rot.nao_ofertar)}")

        if r.funil:
            linhas += ["", "## Funil", f"Diagnóstico: {r.funil.diagnostico}"]
            for e in r.funil.etapas:
                conv = f"{e.conversao_da_anterior:.0%}" if e.conversao_da_anterior is not None else "—"
                linhas.append(f"- {e.estagio.value}: {e.quantidade} leads, conversão {conv}")
            if r.funil.motivos_perda:
                linhas.append(f"Motivos de perda: {r.funil.motivos_perda}")

        if r.higiene:
            linhas += ["", "## Higiene da base"]
            for a in r.higiene:
                linhas.append(f"- [{a.gravidade}] {a.tema}: {len(a.leads)} registro(s)")

        if r.reativacao:
            linhas += ["", "## Candidatos a reativação"]
            for i in r.reativacao:
                linhas.append(
                    f"- {i.nome} (score {i.score:.1f}, parado {i.dias_parado} dias): "
                    f"{i.provavel_problema} Porta: {i.porta_potencial.value}"
                )

        return "\n".join(linhas)

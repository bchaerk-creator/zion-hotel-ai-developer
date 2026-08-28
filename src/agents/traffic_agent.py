"""
Agente do ZION TRAFFIC & ACQUISITION ARCHITECT™.

Métricas, gate, diagnóstico, decisão de otimização e atribuição rodam sem LLM.
O modelo entra em copy, criativo, estrutura de campanha e leitura estratégica.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

from .base_agent import BaseAgent
from src.crm.models import BaseComercial
from src.prompts import PROMPT_TRAFFIC
from src.traffic.atribuicao import leitura_da_atribuicao
from src.traffic.models import Campanha, ContaTrafego, RelatorioTrafego
from src.traffic.relatorio import analisar_conta, gerar_relatorio_trafego

logger = logging.getLogger(__name__)


class TrafficAgent(BaseAgent):
    """Aquisição digital: da campanha à receita atribuída."""

    def __init__(self):
        super().__init__(etapa=10, nome="Zion Traffic & Acquisition Architect")

    @property
    def system_prompt(self) -> str:
        return PROMPT_TRAFFIC

    # ------------------------------------------------------------------
    # Determinístico
    # ------------------------------------------------------------------

    @staticmethod
    def carregar(dados: Dict[str, Any]) -> ContaTrafego:
        payload = dados.get("conta_trafego", dados)
        if "campanhas" not in payload:
            raise ValueError(
                "Dados de tráfego inválidos: nenhuma chave 'campanhas' encontrada. "
                "Use data/exemplo_conta_trafego.json como referência."
            )
        return ContaTrafego(**payload)

    def analisar(
        self, dados: Dict[str, Any], dados_crm: Optional[Dict[str, Any]] = None
    ) -> Tuple[RelatorioTrafego, str]:
        """Roda a análise completa. Com dados de CRM, atribui receita por campanha."""
        conta = self.carregar(dados)
        base = None
        if dados_crm:
            payload = dados_crm.get("base_comercial", dados_crm)
            base = BaseComercial(**payload)

        relatorio = analisar_conta(conta, base)
        logger.info(
            "Conta analisada: %s campanhas, R$ %.0f investidos, gargalo em %s",
            len(conta.campanhas), relatorio.investimento_total_brl,
            relatorio.gargalo_geral.value if relatorio.gargalo_geral else "nenhum",
        )
        return relatorio, gerar_relatorio_trafego(relatorio, conta)

    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise da conta com leitura estratégica de IA."""
        dados_crm = project_data.get("base_comercial")
        relatorio, markdown = self.analisar(project_data, dados_crm)

        analise = self.analyze(
            user_input=(
                "Analise a conta de aquisição abaixo. Produza: leitura do que os números "
                "dizem, onde realocar orçamento e por quê, e os próximos testes a rodar "
                "com hipótese explícita.\n\n"
                f"{self._resumo_para_llm(relatorio)}"
            ),
            use_thinking=True,
        )

        conteudo = f"{markdown}\n\n---\n\n# Leitura Estratégica\n\n{analise}"
        report_path = self.generate_report(
            content=conteudo,
            title="Relatório de Aquisição Zion",
            projeto_nome="Aquisição",
        )

        return {
            "etapa": 10,
            "status": "concluido",
            "analise": analise,
            "relatorio_numerico": markdown,
            "relatorio_path": report_path,
        }

    def criar_copy(self, campanha: Campanha, quantidade: int = 5) -> str:
        """CRIAR COPY — ângulos de performance para uma campanha específica."""
        return self.analyze(
            user_input=(
                f"CRIAR COPY: {quantidade} conceitos de anúncio para a campanha abaixo.\n\n"
                f"{self._contexto_campanha(campanha)}"
            ),
            use_thinking=True,
        )

    def criar_campanha(self, briefing: str) -> str:
        """CRIAR CAMPANHA — estratégia completa a partir de um briefing."""
        return self.analyze(user_input=f"CRIAR CAMPANHA:\n\n{briefing}", use_thinking=True)

    # ------------------------------------------------------------------

    def _contexto_campanha(self, c: Campanha) -> str:
        b = c.briefing
        linhas = [
            f"Campanha: {c.nome} ({c.id})",
            f"Canal: {c.canal.value} | Produto: {c.produto.value}",
            f"Intenção: {c.intencao.value} | Estágio do público: {c.estagio_publico.value}",
            f"Objetivo: {c.objetivo}",
            "",
            "Briefing:",
            f"- Vendemos: {b.o_que_vendemos or 'NÃO RESPONDIDO'}",
            f"- Para quem: {b.para_quem or 'NÃO RESPONDIDO'}",
            f"- Problema: {b.qual_problema or 'NÃO RESPONDIDO'}",
            f"- Desejo: {b.qual_desejo or 'NÃO RESPONDIDO'}",
            f"- Transformação: {b.qual_transformacao or 'NÃO RESPONDIDO'}",
            f"- Oferta: {b.qual_oferta or 'NÃO RESPONDIDO'}",
            f"- Preço: {b.qual_preco_brl if b.qual_preco_brl is not None else 'NÃO RESPONDIDO'}",
            f"- Funil: {b.qual_funil or 'NÃO RESPONDIDO'}",
        ]
        if c.criativos:
            linhas += ["", "Criativos em veiculação:"]
            for cr in c.criativos:
                ctr = cr.cliques / cr.impressoes if cr.impressoes else None
                linhas.append(
                    f"- {cr.nome} ({cr.funcao.value}, ângulo {cr.angulo.value}): "
                    f'hook "{cr.hook}", CTR '
                    + (f"{ctr:.2%}" if ctr is not None else "sem dados")
                )
        return "\n".join(linhas)

    def _resumo_para_llm(self, r: RelatorioTrafego) -> str:
        linhas = [
            f"# Conta de aquisição — {r.data}" + (f" ({r.periodo})" if r.periodo else ""),
            f"Investimento R$ {r.investimento_total_brl:,.0f} | "
            f"Receita atribuída R$ {r.receita_total_brl:,.0f} | "
            f"ROAS {r.roas_geral:.2f}x" if r.roas_geral else "ROAS n/a",
            f"Leads {r.leads} | Oportunidades {r.oportunidades} | Vendas {r.vendas}",
            f"Custo por oportunidade qualificada: R$ {r.cpqo_geral_brl:,.0f}"
            if r.cpqo_geral_brl else "CPQO n/a",
            f"Gargalo predominante: {r.gargalo_geral.value if r.gargalo_geral else 'nenhum'}",
            "",
            "## Campanhas",
        ]
        decisao = {d.campanha_id: d for d in r.decisoes}
        for d in r.diagnosticos:
            m = d.metricas
            dec = decisao[d.campanha_id]
            linhas.append(
                f"- {d.nome} ({d.campanha_id}): investimento R$ {m.investimento_brl:,.0f}, "
                f"CTR {m.ctr:.2%}" if m.ctr else f"- {d.nome}: sem CTR"
            )
            linhas.append(
                f"  CPL R$ {m.cpl_brl:,.0f} | CPQO "
                + (f"R$ {m.cpqo_brl:,.0f}" if m.cpqo_brl else "n/a")
                + " | CAC " + (f"R$ {m.cac_brl:,.0f}" if m.cac_brl else "n/a")
                + " | ROAS " + (f"{m.roas:.2f}x" if m.roas else "n/a")
                if m.cpl_brl else "  sem leads"
            )
            linhas.append(f"  Gargalo: {d.gargalo.value if d.gargalo else 'nenhum'}. {d.leitura}")
            linhas.append(f"  Decisão da engine: {dec.acao}. {dec.justificativa}")
            for a in d.achados:
                linhas.append(f"    - [{a.gravidade}] {a.etapa.value}: {a.sintoma} {a.causa_provavel}")

        bloqueadas = [g for g in r.gates if not g.liberada]
        if bloqueadas:
            linhas += ["", "## Campanhas bloqueadas no gate"]
            for g in bloqueadas:
                linhas.append(f"- {g.campanha_id}: {g.veredito}")
                for p in g.perguntas_sem_resposta:
                    linhas.append(f"    - sem resposta: {p}")

        if r.atribuicao:
            linhas += ["", "## Atribuição pelo CRM"]
            for a in sorted(r.atribuicao, key=lambda x: -x.receita_brl):
                linhas.append(
                    f"- {a.nome}: {a.leads} leads, {a.oportunidades} oportunidades, "
                    f"{a.clientes} clientes, receita R$ {a.receita_brl:,.0f} "
                    f"(ranking {a.ranking_por_leads}º em leads, {a.ranking_por_receita}º em receita)"
                )
            for o in leitura_da_atribuicao(r.atribuicao):
                linhas.append(f"  - {o}")

        return "\n".join(linhas)

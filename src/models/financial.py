"""
Modelo de dados para o Estudo de Viabilidade Econômico-Financeira (Etapa 2).
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class EstimativaCapex(BaseModel):
    """Estimativa detalhada de CAPEX."""
    terreno_brl: Optional[float] = Field(None, description="Custo do terreno em BRL")
    construcao_brl: float = Field(..., description="Custo de construção em BRL")
    equipamentos_brl: float = Field(..., description="Custo de equipamentos e mobiliário em BRL")
    infraestrutura_brl: float = Field(..., description="Custo de infraestrutura em BRL")
    projetos_licencas_brl: float = Field(..., description="Custo de projetos e licenças em BRL")
    capital_giro_brl: float = Field(..., description="Capital de giro inicial em BRL")
    contingencia_brl: float = Field(..., description="Contingência em BRL")
    capex_total_brl: float = Field(..., description="CAPEX total em BRL")
    custo_por_uh_brl: Optional[float] = Field(None, description="Custo por unidade habitacional em BRL")


class ProjecaoReceitas(BaseModel):
    """Projeção de receitas operacionais."""
    receita_hospedagem_anual_brl: float = Field(..., description="Receita de hospedagem anual em BRL")
    receita_ab_anual_brl: Optional[float] = Field(None, description="Receita de A&B anual em BRL")
    receita_outros_anual_brl: Optional[float] = Field(None, description="Outras receitas anuais em BRL")
    receita_total_anual_brl: float = Field(..., description="Receita total anual em BRL")
    premissas_ocupacao: float = Field(..., description="Taxa de ocupação premissa (%)")
    premissas_adr_brl: float = Field(..., description="ADR premissa em BRL")
    revpar_brl: float = Field(..., description="RevPAR calculado em BRL")


class ProjecaoDespesas(BaseModel):
    """Projeção de despesas operacionais."""
    folha_pagamento_brl: float = Field(..., description="Folha de pagamento anual em BRL")
    custos_operacionais_brl: float = Field(..., description="Custos operacionais em BRL")
    marketing_brl: float = Field(..., description="Marketing e distribuição em BRL")
    manutencao_brl: float = Field(..., description="Manutenção e reposição em BRL")
    administrativo_brl: float = Field(..., description="Custos administrativos em BRL")
    despesa_total_anual_brl: float = Field(..., description="Despesa total anual em BRL")
    margem_operacional_pct: float = Field(..., description="Margem operacional (%)")


class IndicadoresRetorno(BaseModel):
    """Indicadores de retorno do investimento."""
    ebitda_anual_brl: float = Field(..., description="EBITDA anual projetado em BRL")
    ebitda_margem_pct: float = Field(..., description="Margem EBITDA (%)")
    tir_pct: float = Field(..., description="TIR - Taxa Interna de Retorno (%)")
    vpl_brl: float = Field(..., description="VPL - Valor Presente Líquido em BRL")
    payback_anos: float = Field(..., description="Payback em anos")
    break_even_meses: int = Field(..., description="Break-even em meses de operação")
    cap_rate_pct: Optional[float] = Field(None, description="Cap Rate (%)")


class CenarioFinanceiro(BaseModel):
    """Um cenário financeiro (conservador, realista ou otimista)."""
    nome: str = Field(..., description="Nome do cenário")
    ocupacao_pct: float = Field(..., description="Taxa de ocupação do cenário (%)")
    adr_brl: float = Field(..., description="ADR do cenário em BRL")
    ebitda_margem_pct: float = Field(..., description="Margem EBITDA do cenário (%)")
    tir_pct: float = Field(..., description="TIR do cenário (%)")
    vpl_brl: float = Field(..., description="VPL do cenário em BRL")
    payback_anos: float = Field(..., description="Payback do cenário em anos")


class FluxoCaixaAnual(BaseModel):
    """Fluxo de caixa de um ano específico."""
    ano: int = Field(..., description="Ano da projeção")
    receita_brl: float = Field(..., description="Receita do ano em BRL")
    despesa_brl: float = Field(..., description="Despesa do ano em BRL")
    ebitda_brl: float = Field(..., description="EBITDA do ano em BRL")
    fluxo_livre_brl: float = Field(..., description="Fluxo de caixa livre em BRL")
    fluxo_acumulado_brl: float = Field(..., description="Fluxo acumulado em BRL")


class FinancialModelResult(BaseModel):
    """Resultado completo do Estudo de Viabilidade Econômico-Financeira."""
    projeto_id: str = Field(..., description="ID do projeto")
    capex: EstimativaCapex = Field(..., description="Estimativa de CAPEX")
    receitas: ProjecaoReceitas = Field(..., description="Projeção de receitas")
    despesas: ProjecaoDespesas = Field(..., description="Projeção de despesas")
    indicadores: IndicadoresRetorno = Field(..., description="Indicadores de retorno")
    cenarios: List[CenarioFinanceiro] = Field(default_factory=list, description="Cenários financeiros")
    fluxo_caixa_10_anos: List[FluxoCaixaAnual] = Field(default_factory=list, description="Fluxo de caixa 10 anos")
    analise_sensibilidade: Optional[str] = Field(None, description="Análise de sensibilidade textual")
    conclusao_financeira: str = Field(..., description="Conclusão da viabilidade financeira")
    resumo_executivo: str = Field(..., description="Resumo executivo do modelo financeiro")

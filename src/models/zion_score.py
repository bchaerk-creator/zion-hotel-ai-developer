"""
Modelo de dados para o resultado do Zion Score (Etapa 0).
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class VocacaoDestino(BaseModel):
    """Análise da vocação turística do destino."""
    vocacao_principal: str = Field(..., description="Vocação turística principal identificada")
    vocacoes_secundarias: List[str] = Field(default_factory=list, description="Vocações secundárias")
    justificativa: str = Field(..., description="Justificativa da vocação identificada")


class ConcorrenciaRegional(BaseModel):
    """Mapeamento da concorrência regional."""
    concorrentes_diretos: List[str] = Field(default_factory=list, description="Concorrentes diretos identificados")
    concorrentes_indiretos: List[str] = Field(default_factory=list, description="Concorrentes indiretos")
    nivel_saturacao: str = Field(..., description="Nível de saturação do mercado (baixo/médio/alto)")
    oportunidades_identificadas: List[str] = Field(default_factory=list, description="Oportunidades de mercado")


class RiscosTerritorio(BaseModel):
    """Análise de riscos e pontos fortes do território."""
    pontos_fortes: List[str] = Field(default_factory=list, description="Pontos fortes do território")
    riscos_identificados: List[str] = Field(default_factory=list, description="Riscos identificados")
    mitigacoes_sugeridas: List[str] = Field(default_factory=list, description="Mitigações sugeridas")


class ZionScoreResult(BaseModel):
    """Resultado completo do diagnóstico preliminar Zion Score."""
    projeto_id: str = Field(..., description="ID do projeto analisado")
    zion_score: float = Field(..., ge=0, le=10, description="Nota Zion Score de 0 a 10")
    classificacao: str = Field(..., description="Classificação (excelente/bom/regular/insuficiente)")
    vocacao_destino: VocacaoDestino = Field(..., description="Análise de vocação do destino")
    adr_estimado_brl: float = Field(..., description="ADR estimado de referência em BRL")
    capex_orientativo_brl: Optional[float] = Field(None, description="CAPEX orientativo preliminar em BRL")
    mercado_emissor: str = Field(..., description="Mercado emissor principal identificado")
    concorrencia_regional: ConcorrenciaRegional = Field(..., description="Mapeamento de concorrência")
    riscos_territorio: RiscosTerritorio = Field(..., description="Análise de riscos do território")
    recomendacao: str = Field(..., description="Recomendação de prosseguimento")
    proximos_passos: List[str] = Field(default_factory=list, description="Próximos passos recomendados")
    resumo_executivo: str = Field(..., description="Resumo executivo do diagnóstico")

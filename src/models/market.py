"""
Modelo de dados para o Estudo de Viabilidade Mercadológica (Etapa 1).
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class PerfilTuristico(BaseModel):
    """Perfil turístico do destino."""
    fluxo_visitantes_anual: Optional[int] = Field(None, description="Fluxo estimado de visitantes/ano")
    perfil_predominante: str = Field(..., description="Perfil predominante do visitante")
    motivacao_principal: str = Field(..., description="Motivação principal de viagem")
    tempo_medio_estadia: Optional[float] = Field(None, description="Tempo médio de estadia em noites")
    ticket_medio_brl: Optional[float] = Field(None, description="Ticket médio do visitante em BRL")


class AnaliseSazonalidade(BaseModel):
    """Análise de sazonalidade do destino."""
    alta_temporada: List[str] = Field(default_factory=list, description="Meses de alta temporada")
    baixa_temporada: List[str] = Field(default_factory=list, description="Meses de baixa temporada")
    eventos_relevantes: List[str] = Field(default_factory=list, description="Eventos que impactam demanda")
    taxa_ocupacao_alta: Optional[float] = Field(None, description="Taxa de ocupação estimada na alta (%)")
    taxa_ocupacao_baixa: Optional[float] = Field(None, description="Taxa de ocupação estimada na baixa (%)")
    estrategias_dessazonalizacao: List[str] = Field(default_factory=list, description="Estratégias sugeridas")


class OfertaConcorrente(BaseModel):
    """Análise de um concorrente."""
    nome: str = Field(..., description="Nome do estabelecimento")
    tipo: str = Field(..., description="Tipo (hotel, pousada, resort, etc.)")
    categoria: str = Field(..., description="Categoria (econômico, midscale, upscale, luxo)")
    numero_unidades: Optional[int] = Field(None, description="Número de unidades")
    adr_estimado: Optional[float] = Field(None, description="ADR estimado em BRL")
    diferenciais: List[str] = Field(default_factory=list, description="Diferenciais identificados")
    pontos_fracos: List[str] = Field(default_factory=list, description="Pontos fracos identificados")


class BenchmarkEstrategico(BaseModel):
    """Benchmark estratégico nacional e internacional."""
    referencias_nacionais: List[str] = Field(default_factory=list, description="Referências nacionais")
    referencias_internacionais: List[str] = Field(default_factory=list, description="Referências internacionais")
    oportunidades_diferenciacao: List[str] = Field(default_factory=list, description="Oportunidades de diferenciação")
    posicionamento_recomendado: str = Field(..., description="Posicionamento estratégico recomendado")


class MarketStudyResult(BaseModel):
    """Resultado completo do Estudo de Viabilidade Mercadológica."""
    projeto_id: str = Field(..., description="ID do projeto")
    perfil_turistico: PerfilTuristico = Field(..., description="Perfil turístico do destino")
    sazonalidade: AnaliseSazonalidade = Field(..., description="Análise de sazonalidade")
    oferta_concorrente: List[OfertaConcorrente] = Field(default_factory=list, description="Mapeamento da oferta")
    benchmark: BenchmarkEstrategico = Field(..., description="Benchmark estratégico")
    demanda_identificada: bool = Field(..., description="Se há demanda real identificada")
    adr_mercado_brl: float = Field(..., description="ADR médio do mercado em BRL")
    adr_posicionamento_brl: float = Field(..., description="ADR recomendado para posicionamento em BRL")
    taxa_ocupacao_projetada: float = Field(..., description="Taxa de ocupação projetada (%)")
    conclusao_mercadologica: str = Field(..., description="Conclusão mercadológica")
    recomendacoes: List[str] = Field(default_factory=list, description="Recomendações estratégicas")
    resumo_executivo: str = Field(..., description="Resumo executivo do estudo")

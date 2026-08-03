"""
Modelos de dados para entrada e perfil do projeto hoteleiro.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class LocationData(BaseModel):
    """Dados de localização do terreno/destino."""
    cidade: str = Field(..., description="Cidade do projeto")
    estado: str = Field(..., description="Estado/Província")
    pais: str = Field(default="Brasil", description="País")
    regiao_turistica: Optional[str] = Field(None, description="Região turística")
    coordenadas: Optional[str] = Field(None, description="Coordenadas GPS")
    area_terreno_m2: Optional[float] = Field(None, description="Área do terreno em m²")
    zoneamento: Optional[str] = Field(None, description="Zoneamento atual")
    acesso_principal: Optional[str] = Field(None, description="Principal via de acesso")
    distancia_aeroporto_km: Optional[float] = Field(None, description="Distância ao aeroporto mais próximo em km")
    distancia_centro_km: Optional[float] = Field(None, description="Distância ao centro urbano em km")


class ProjectInput(BaseModel):
    """Dados de entrada para análise de um novo projeto hoteleiro."""
    nome_projeto: str = Field(..., description="Nome do projeto ou empreendimento")
    localizacao: LocationData = Field(..., description="Dados de localização")
    tipo_produto: Optional[str] = Field(
        None,
        description="Tipo de produto pretendido (hotel, resort, glamping, pousada, etc.)"
    )
    numero_unidades_estimado: Optional[int] = Field(None, description="Número estimado de unidades habitacionais")
    investimento_estimado_brl: Optional[float] = Field(None, description="Investimento estimado em BRL")
    publico_alvo_pretendido: Optional[str] = Field(None, description="Público-alvo pretendido")
    diferenciais_pretendidos: Optional[List[str]] = Field(None, description="Diferenciais pretendidos")
    estagio_atual: Optional[str] = Field(
        None,
        description="Estágio atual do projeto (terreno, conceito, projeto, obra, operação)"
    )
    objetivos_proprietario: Optional[str] = Field(None, description="Objetivos do proprietário")
    prazo_desejado_meses: Optional[int] = Field(None, description="Prazo desejado para implantação em meses")
    observacoes: Optional[str] = Field(None, description="Observações adicionais")


class ProjectProfile(BaseModel):
    """Perfil consolidado do projeto após análise inicial."""
    projeto_id: str = Field(..., description="Identificador único do projeto")
    nome_projeto: str = Field(..., description="Nome do projeto")
    localizacao: LocationData = Field(..., description="Dados de localização")
    tipo_produto_recomendado: Optional[str] = Field(None, description="Tipo de produto recomendado pela análise")
    segmento_mercado: Optional[str] = Field(None, description="Segmento de mercado identificado")
    vocacao_destino: Optional[str] = Field(None, description="Vocação turística do destino")
    etapa_atual: int = Field(default=0, description="Etapa atual no método Zion (0-6)")
    zion_score: Optional[float] = Field(None, description="Nota Zion Score (0-10)")
    status: str = Field(default="em_analise", description="Status do projeto")
    data_criacao: Optional[str] = Field(None, description="Data de criação do perfil")
    historico_etapas: List[dict] = Field(default_factory=list, description="Histórico de etapas concluídas")

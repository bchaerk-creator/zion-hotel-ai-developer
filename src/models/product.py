"""
Modelo de dados para Definição de Produto, Posicionamento e Master Plan (Etapa 3).
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class ConceitoEmpreendimento(BaseModel):
    """Definição conceitual do empreendimento."""
    conceito_central: str = Field(..., description="Conceito central do projeto")
    posicionamento_mercado: str = Field(..., description="Posicionamento estratégico no mercado")
    publico_alvo: str = Field(..., description="Diretriz de público-alvo")
    proposta_valor: str = Field(..., description="Proposta de valor única")
    experiencia_hospede: str = Field(..., description="Diretrizes de experiência do hóspede")
    diferenciais_competitivos: List[str] = Field(default_factory=list, description="Elementos de diferenciação")


class NarrativaMarca(BaseModel):
    """Estratégia de marca e narrativa territorial."""
    narrativa_territorial: str = Field(..., description="Narrativa territorial do empreendimento")
    proposito_marca: str = Field(..., description="Propósito da marca")
    tom_comunicacao: str = Field(..., description="Tom de comunicação recomendado")
    pilares_marca: List[str] = Field(default_factory=list, description="Pilares da marca")
    base_conceitual_branding: str = Field(..., description="Base conceitual para branding")


class ArquiteturaBandeira(BaseModel):
    """Estratégia de bandeira e arquitetura de marca."""
    modelo_recomendado: str = Field(..., description="Modelo de bandeira recomendado")
    justificativa: str = Field(..., description="Justificativa da recomendação")
    opcoes_avaliadas: List[str] = Field(default_factory=list, description="Opções avaliadas")
    implicacoes_operacionais: str = Field(..., description="Implicações operacionais do modelo")


class DiretrizMasterPlan(BaseModel):
    """Diretrizes para o master plan."""
    fases_desenvolvimento: List[str] = Field(default_factory=list, description="Fases macro de desenvolvimento")
    diretriz_expansao: str = Field(..., description="Diretriz estratégica de expansão")
    cronograma_macro: str = Field(..., description="Cronograma macro indicativo")
    preparacao_ampliacoes: str = Field(..., description="Preparação para ampliações futuras")
    briefing_arquitetura: str = Field(..., description="Briefing técnico para arquitetura")
    briefing_paisagismo: str = Field(..., description="Briefing para paisagismo")
    briefing_engenharia: str = Field(..., description="Briefing para engenharia")


class ProductDefinitionResult(BaseModel):
    """Resultado completo da Definição de Produto e Posicionamento."""
    projeto_id: str = Field(..., description="ID do projeto")
    conceito: ConceitoEmpreendimento = Field(..., description="Definição conceitual")
    narrativa: NarrativaMarca = Field(..., description="Estratégia de marca e narrativa")
    bandeira: ArquiteturaBandeira = Field(..., description="Estratégia de bandeira")
    master_plan: DiretrizMasterPlan = Field(..., description="Diretrizes para master plan")
    implantacao_faseada: bool = Field(default=True, description="Se recomenda implantação faseada")
    numero_fases: Optional[int] = Field(None, description="Número de fases recomendadas")
    resumo_executivo: str = Field(..., description="Resumo executivo da definição de produto")

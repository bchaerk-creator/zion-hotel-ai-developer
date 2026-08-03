"""
Modelo de dados para Estruturação do Negócio (Etapa 4).
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class EstruturaSocietaria(BaseModel):
    """Definição da estrutura societária."""
    tipo_spe: str = Field(..., description="Tipo de SPE recomendado")
    modelo_societario: str = Field(..., description="Modelo societário proposto")
    estrategia_entrada_investidores: str = Field(..., description="Estratégia de entrada de investidores")
    estrutura_operacional: str = Field(..., description="Estrutura operacional proposta")
    governanca: str = Field(..., description="Modelo de governança")
    preparacao_capital: str = Field(..., description="Preparação para acesso a capital")


class CoordenacaoJuridica(BaseModel):
    """Coordenação jurídica necessária."""
    instrumentos_contratuais: List[str] = Field(default_factory=list, description="Instrumentos contratuais necessários")
    acordo_socios: bool = Field(default=True, description="Necessidade de acordo de sócios")
    mutuo_conversivel: bool = Field(default=False, description="Uso de mútuo conversível")
    scp: bool = Field(default=False, description="Uso de SCP")
    alinhamento_captacao: str = Field(..., description="Alinhamento com estrutura de captação")
    checklist_juridico: List[str] = Field(default_factory=list, description="Checklist jurídico")


class BusinessStructureResult(BaseModel):
    """Resultado completo da Estruturação do Negócio."""
    projeto_id: str = Field(..., description="ID do projeto")
    estrutura_societaria: EstruturaSocietaria = Field(..., description="Estrutura societária definida")
    coordenacao_juridica: CoordenacaoJuridica = Field(..., description="Coordenação jurídica")
    riscos_societarios: List[str] = Field(default_factory=list, description="Riscos societários identificados")
    recomendacoes_governanca: List[str] = Field(default_factory=list, description="Recomendações de governança")
    proximos_passos_juridicos: List[str] = Field(default_factory=list, description="Próximos passos jurídicos")
    resumo_executivo: str = Field(..., description="Resumo executivo da estruturação")

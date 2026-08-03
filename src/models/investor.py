"""
Modelo de dados para Modelagem e Apresentação para Investidores (Etapa 5).
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class TeseInvestimento(BaseModel):
    """Estruturação da tese de investimento."""
    titulo_tese: str = Field(..., description="Título da tese de investimento")
    resumo_oportunidade: str = Field(..., description="Resumo da oportunidade")
    mercado_alvo: str = Field(..., description="Mercado-alvo")
    diferencial_competitivo: str = Field(..., description="Diferencial competitivo principal")
    modelo_receita: str = Field(..., description="Modelo de receita")
    retorno_esperado: str = Field(..., description="Retorno esperado para o investidor")
    horizonte_investimento: str = Field(..., description="Horizonte de investimento")
    estrategia_saida: str = Field(..., description="Estratégia de saída / eventos de liquidez")


class InstrumentoEntrada(BaseModel):
    """Definição do instrumento de entrada de capital."""
    tipo: str = Field(..., description="Tipo de instrumento (equity, dívida conversível, SCP, etc.)")
    valor_minimo_brl: Optional[float] = Field(None, description="Valor mínimo de entrada em BRL")
    participacao_pct: Optional[float] = Field(None, description="Participação percentual oferecida")
    retorno_projetado: str = Field(..., description="Retorno projetado ao investidor")
    distribuicao_resultados: str = Field(..., description="Modelo de distribuição de resultados")
    eventos_liquidez: List[str] = Field(default_factory=list, description="Eventos de liquidez previstos")


class MaterialInvestidor(BaseModel):
    """Material de apresentação para investidores."""
    tipo: str = Field(..., description="Tipo de material (teaser, info memo, pitch deck, data room)")
    titulo: str = Field(..., description="Título do material")
    conteudo_resumido: str = Field(..., description="Resumo do conteúdo")
    publico_alvo: str = Field(..., description="Público-alvo do material")
    formato: str = Field(..., description="Formato de entrega")


class AdequacaoPublico(BaseModel):
    """Adequação por perfil de investidor."""
    perfil: str = Field(..., description="Perfil do investidor")
    linguagem: str = Field(..., description="Linguagem adequada")
    foco_apresentacao: str = Field(..., description="Foco da apresentação para este perfil")
    materiais_recomendados: List[str] = Field(default_factory=list, description="Materiais recomendados")


class InvestorPackageResult(BaseModel):
    """Resultado completo da Modelagem para Investidores."""
    projeto_id: str = Field(..., description="ID do projeto")
    tese: TeseInvestimento = Field(..., description="Tese de investimento estruturada")
    instrumento: InstrumentoEntrada = Field(..., description="Instrumento de entrada definido")
    materiais: List[MaterialInvestidor] = Field(default_factory=list, description="Materiais gerados")
    adequacao_publicos: List[AdequacaoPublico] = Field(default_factory=list, description="Adequação por público")
    cronograma_captacao: str = Field(..., description="Cronograma de captação")
    uso_recursos: str = Field(..., description="Use of proceeds")
    resumo_executivo: str = Field(..., description="Resumo executivo do pacote para investidores")

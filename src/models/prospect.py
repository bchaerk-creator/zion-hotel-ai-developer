"""
Modelo de dados para prospects (carteira de clientes potenciais da Zion).
"""

from datetime import datetime, date
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator


class Modalidade(str, Enum):
    """Modalidade Zion à qual o prospect se encaixa."""

    DEVELOPMENT = "development"   # tem terreno, quer transformar em ativo
    MANAGEMENT = "management"     # tem operação, quer gestão profissional
    COLLECTION = "collection"     # tem operação, quer a bandeira
    INDEFINIDA = "indefinida"


class Estagio(str, Enum):
    """Estágio do prospect no funil comercial."""

    IDENTIFICADO = "identificado"       # apareceu numa coleta, ainda não qualificado
    QUALIFICADO = "qualificado"         # bate com o ICP
    CONTATADO = "contatado"
    DIAGNOSTICO = "diagnostico"         # aceitou o diagnóstico territorial
    PROPOSTA = "proposta"
    CLIENTE = "cliente"
    DESCARTADO = "descartado"


class BaseLegal(str, Enum):
    """Base legal LGPD que autoriza o tratamento deste registro (Art. 7º)."""

    LEGITIMO_INTERESSE = "legitimo_interesse"   # dado público de PJ, prospecção B2B
    CONSENTIMENTO = "consentimento"             # o titular pediu contato
    EXECUCAO_CONTRATO = "execucao_contrato"     # já é cliente


class Origem(BaseModel):
    """
    Procedência do registro. Obrigatória: sem rastro de origem não há como
    demonstrar boa-fé numa eventual fiscalização da ANPD.
    """

    fonte: str = Field(..., description="De onde veio o dado (URL, evento, indicação)")
    tipo: str = Field(..., description="Tipo da fonte: web, evento, indicacao, inbound, manual")
    coletado_em: datetime = Field(default_factory=datetime.now, description="Quando foi coletado")
    coletado_por: str = Field(default="manual", description="Processo ou pessoa que coletou")


class Territorio(BaseModel):
    """Território associado ao prospect."""

    municipio: Optional[str] = Field(None, description="Município")
    uf: Optional[str] = Field(None, description="Unidade federativa (sigla)")
    bioma: Optional[str] = Field(None, description="Bioma predominante")
    area_ha: Optional[float] = Field(None, ge=0, description="Área do terreno em hectares")
    unidades: Optional[int] = Field(None, ge=0, description="Unidades habitacionais em operação")

    @field_validator("uf")
    @classmethod
    def uf_maiuscula(cls, v: Optional[str]) -> Optional[str]:
        return v.upper().strip() if v else v


class Prospect(BaseModel):
    """
    Um cliente potencial da Zion.

    Guarda apenas dado de contexto de negócio e contato profissional. Não
    modelamos dado pessoal sensível (Art. 5º, II da LGPD) porque a prospecção
    B2B da Zion não precisa dele.
    """

    id: str = Field(..., description="Identificador estável (slug derivado do nome)")
    nome: str = Field(..., description="Nome do contato ou da empresa")
    empresa: Optional[str] = Field(None, description="Razão social ou nome fantasia")
    cargo: Optional[str] = Field(None, description="Cargo do contato")

    email: Optional[str] = Field(None, description="E-mail profissional")
    telefone: Optional[str] = Field(None, description="Telefone profissional")
    site: Optional[str] = Field(None, description="Site institucional")
    instagram: Optional[str] = Field(None, description="Perfil no Instagram")

    modalidade: Modalidade = Field(default=Modalidade.INDEFINIDA, description="Modalidade Zion alvo")
    estagio: Estagio = Field(default=Estagio.IDENTIFICADO, description="Estágio no funil")
    territorio: Territorio = Field(default_factory=Territorio, description="Território associado")

    score: Optional[float] = Field(None, ge=0, le=10, description="Aderência ao ICP, de 0 a 10")
    score_motivos: List[str] = Field(default_factory=list, description="O que pesou no score")

    origem: Origem = Field(..., description="Procedência do registro")
    base_legal: BaseLegal = Field(
        default=BaseLegal.LEGITIMO_INTERESSE,
        description="Base legal LGPD para tratar este registro",
    )
    nao_contatar: bool = Field(
        default=False,
        description="Titular pediu para não ser contatado — bloqueia qualquer disparo",
    )
    revisar_ate: Optional[date] = Field(
        None,
        description="Data limite para revisar ou descartar o registro (retenção)",
    )

    notas: Optional[str] = Field(None, description="Observações livres")
    atualizado_em: datetime = Field(default_factory=datetime.now, description="Última atualização")

    @property
    def contatavel(self) -> bool:
        """Se pode receber abordagem comercial."""
        return (
            not self.nao_contatar
            and self.estagio != Estagio.DESCARTADO
            and bool(self.email or self.telefone or self.instagram)
        )

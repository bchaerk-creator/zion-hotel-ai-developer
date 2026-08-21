"""
Modelos de dados do Land Bank Zion — banco de terras para agregação
territorial e originação de créditos de carbono.

Conceito central: uma gleba isolada quase nunca paga o custo fixo de um
projeto de carbono. O que paga é o AGRUPAMENTO de glebas sob um mesmo
projeto (grouped project), dividindo validação, verificação e MRV entre
todas as áreas. Estes modelos descrevem esse portfólio.
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enumerações de domínio
# ---------------------------------------------------------------------------

class Bioma(str, Enum):
    """Bioma brasileiro onde a gleba está inserida."""
    MATA_ATLANTICA = "mata_atlantica"
    AMAZONIA = "amazonia"
    CERRADO = "cerrado"
    CAATINGA = "caatinga"
    PAMPA = "pampa"
    PANTANAL = "pantanal"


class UsoSolo(str, Enum):
    """Uso e cobertura atual do solo — define a metodologia elegível."""
    PASTAGEM_DEGRADADA = "pastagem_degradada"
    PASTAGEM_ATIVA = "pastagem_ativa"
    AGRICULTURA = "agricultura"
    SOLO_EXPOSTO = "solo_exposto"
    SILVICULTURA = "silvicultura"
    REGENERACAO_INICIAL = "regeneracao_inicial"
    FLORESTA_DEGRADADA = "floresta_degradada"
    FLORESTA_CONSERVADA = "floresta_conservada"
    AREA_EDIFICADA = "area_edificada"
    CORPO_DAGUA = "corpo_dagua"


class Metodologia(str, Enum):
    """
    Rota metodológica de crédito.

    ARR_PLANTIO      — restauração ativa por plantio de mudas nativas
    ARR_REGENERACAO  — regeneração natural assistida (custo menor, curva mais lenta)
    SAF              — sistema agroflorestal
    REDD_CONSERVACAO — desmatamento evitado sobre floresta ameaçada
    IFM              — manejo florestal melhorado
    NAO_ELEGIVEL     — área que não gera crédito (edificação, lâmina d'água, etc.)
    """
    ARR_PLANTIO = "arr_plantio"
    ARR_REGENERACAO = "arr_regeneracao"
    SAF = "saf"
    REDD_CONSERVACAO = "redd_conservacao"
    IFM = "ifm"
    NAO_ELEGIVEL = "nao_elegivel"


class StatusDominial(str, Enum):
    """Grau de controle da Zion sobre a gleba."""
    PROPRIO = "proprio"                # imóvel da holding / SPE
    CONTRATADO = "contratado"          # instrumento assinado e registrado
    EM_NEGOCIACAO = "em_negociacao"    # MOU, proposta, tratativa avançada
    PROSPECCAO = "prospeccao"          # mapeada, sem contato formal


class Instrumento(str, Enum):
    """Instrumento jurídico de agregação da gleba ao Land Bank."""
    COMPRA = "compra"
    ARRENDAMENTO_CARBONO = "arrendamento_carbono"
    CESSAO_DIREITOS_CARBONO = "cessao_direitos_carbono"
    PARCERIA_RECEITA = "parceria_receita"
    SERVIDAO_AMBIENTAL = "servidao_ambiental"
    PERMUTA_PARTICIPACAO = "permuta_participacao"


class ClasseElegibilidade(str, Enum):
    """Resultado da triagem de elegibilidade de um talhão."""
    ELEGIVEL = "elegivel"              # entra no núcleo bancável
    CONDICIONADA = "condicionada"      # depende de adicionalidade/pendência
    INELEGIVEL = "inelegivel"          # não gera crédito


# ---------------------------------------------------------------------------
# Entradas
# ---------------------------------------------------------------------------

class Talhao(BaseModel):
    """Subdivisão homogênea de uma gleba por uso do solo."""
    id: str = Field(..., description="Identificador do talhão")
    descricao: Optional[str] = Field(None, description="Descrição do talhão")
    area_ha: float = Field(..., gt=0, description="Área do talhão em hectares")
    uso_solo: UsoSolo = Field(..., description="Uso e cobertura atual do solo")
    obrigacao_legal: bool = Field(
        default=False,
        description="Área com passivo legal de recomposição (APP/Reserva Legal). "
                    "Adicionalidade condicionada — não entra no núcleo bancável por padrão.",
    )
    metodologia_forcada: Optional[Metodologia] = Field(
        None, description="Sobrescreve a metodologia sugerida pela engine"
    )
    observacoes: Optional[str] = Field(None, description="Observações do talhão")


class Gleba(BaseModel):
    """Uma área de terra candidata ou já integrada ao Land Bank."""
    id: str = Field(..., description="Código interno da gleba (ex.: GL-URU-01)")
    nome: str = Field(..., description="Nome da gleba / fazenda")
    proprietario: Optional[str] = Field(None, description="Proprietário registral")
    municipio: str = Field(..., description="Município")
    uf: str = Field(..., description="Unidade federativa")
    bioma: Bioma = Field(..., description="Bioma predominante")
    latitude: Optional[float] = Field(None, description="Latitude do centroide (graus decimais)")
    longitude: Optional[float] = Field(None, description="Longitude do centroide (graus decimais)")

    area_total_ha: float = Field(..., gt=0, description="Área total da gleba em hectares")
    talhoes: List[Talhao] = Field(default_factory=list, description="Talhões mapeados")
    uso_solo_predominante: Optional[UsoSolo] = Field(
        None, description="Usado quando não há talhões mapeados"
    )

    status_dominial: StatusDominial = Field(
        default=StatusDominial.PROSPECCAO, description="Grau de controle da Zion"
    )
    instrumento: Optional[Instrumento] = Field(
        None, description="Instrumento de agregação previsto ou assinado"
    )
    percentual_receita_terrenista: Optional[float] = Field(
        None, ge=0, le=1,
        description="Fatia da receita de carbono do terrenista (0-1). "
                    "Se nulo, usa o padrão das premissas.",
    )

    car_ativo: bool = Field(default=False, description="CAR ativo e sem pendência")
    matricula_regular: bool = Field(default=False, description="Matrícula regular e georreferenciada")
    litigio_dominial: bool = Field(default=False, description="Existe litígio sobre a posse/domínio")
    sobreposicao_sensivel: bool = Field(
        default=False,
        description="Sobreposição com terra indígena, território quilombola ou UC de proteção integral",
    )
    desmatamento_recente: bool = Field(
        default=False,
        description="Houve supressão de vegetação nativa dentro da janela de corte (10 anos). "
                    "Bloqueia elegibilidade ARR.",
    )

    custo_aquisicao_ha_brl: Optional[float] = Field(
        None, ge=0, description="Preço por hectare, quando o instrumento for compra"
    )
    custo_negociacao_brl: float = Field(
        default=0.0, ge=0, description="Custo fixo de originação (due diligence, comissão, jurídico)"
    )
    distancia_hub_km: Optional[float] = Field(
        None, description="Distância ao ativo hoteleiro / hub operacional Zion"
    )
    observacoes: Optional[str] = Field(None, description="Observações gerais")


class PremissasCarbono(BaseModel):
    """
    Premissas paramétricas do modelo de carbono.

    Todos os valores são calibráveis. Os defaults refletem ordens de grandeza
    públicas do mercado voluntário brasileiro e devem ser revalidados antes de
    qualquer uso contratual ou de captação.
    """
    horizonte_anos: int = Field(default=30, ge=5, le=40, description="Período de creditação")
    taxa_desconto: float = Field(default=0.12, gt=0, description="Taxa real de desconto para VPL")

    preco_tco2e_remocao_brl: float = Field(
        default=180.0, gt=0,
        description="Preço por tCO2e de remoção (ARR/SAF) em BRL. Referência: faixa premium de "
                    "remoções florestais brasileiras com co-benefícios, na ordem de US$ 30-35",
    )
    preco_tco2e_evitada_brl: float = Field(
        default=55.0, gt=0, description="Preço por tCO2e de emissão evitada (REDD) em BRL"
    )
    preco_tco2e_ifm_brl: float = Field(
        default=70.0, gt=0, description="Preço por tCO2e de manejo florestal melhorado em BRL"
    )

    buffer_remocao: float = Field(
        default=0.18, ge=0, lt=1, description="Buffer de não permanência para remoções"
    )
    buffer_evitada: float = Field(
        default=0.22, ge=0, lt=1, description="Buffer de não permanência para emissão evitada"
    )
    incerteza_desconto: float = Field(
        default=0.05, ge=0, lt=1, description="Desconto adicional por incerteza de inventário"
    )

    custo_estruturacao_brl: float = Field(
        default=660_000.0, ge=0,
        description="Custo fixo por projeto agrupado: PDD, validação, inventário, jurídico",
    )
    custo_verificacao_brl: float = Field(
        default=120_000.0, ge=0, description="Custo por evento de verificação"
    )
    intervalo_verificacao_anos: int = Field(default=5, ge=1, description="Intervalo entre verificações")
    ano_primeira_emissao: int = Field(
        default=5, ge=1, description="Ano da primeira emissão de VCUs (caixa entra aqui)"
    )
    custo_mrv_fixo_ano_brl: float = Field(
        default=60_000.0, ge=0, description="Custo fixo anual de monitoramento por projeto"
    )
    custo_mrv_ha_ano_brl: float = Field(
        default=25.0, ge=0, description="Custo variável de monitoramento por hectare/ano"
    )
    taxa_registro_por_vcu_brl: float = Field(
        default=1.20, ge=0, description="Taxa de emissão/registro por VCU"
    )
    anos_implantacao: int = Field(
        default=3, ge=1, description="Anos para diluir o CAPEX de restauração"
    )

    percentual_receita_terrenista: float = Field(
        default=0.40, ge=0, le=1, description="Fatia padrão da receita destinada ao terrenista"
    )
    base_reparticao: str = Field(
        default="liquida",
        description="Base do split com o terrenista: 'liquida' (após recuperação de custos, "
                    "padrão quando a Zion banca o CAPEX) ou 'bruta' (sobre a receita do evento)",
    )

    percentual_prevenda: float = Field(
        default=0.0, ge=0, le=1,
        description="Fração dos créditos vendida antecipadamente a um offtaker (forward)",
    )
    desconto_prevenda: float = Field(
        default=0.30, ge=0, lt=1,
        description="Deságio praticado na pré-venda em relação ao preço spot",
    )
    ano_adiantamento: int = Field(
        default=1, ge=0, description="Ano em que o adiantamento da pré-venda entra no caixa"
    )

    area_minima_cluster_ha: float = Field(
        default=500.0, gt=0, description="Escala mínima para um projeto agrupado fechar conta"
    )
    area_alvo_cluster_ha: float = Field(
        default=1_000.0, gt=0, description="Escala alvo para diluição confortável dos custos fixos"
    )
    raio_cluster_km: float = Field(
        default=50.0, gt=0, description="Raio máximo para agrupar glebas num mesmo projeto"
    )

    custo_implantacao_ha_brl: Dict[str, float] = Field(
        default_factory=lambda: {
            Metodologia.ARR_PLANTIO.value: 20_000.0,
            Metodologia.ARR_REGENERACAO.value: 8_000.0,
            Metodologia.SAF.value: 28_000.0,
            Metodologia.REDD_CONSERVACAO.value: 0.0,
            Metodologia.IFM.value: 1_200.0,
            Metodologia.NAO_ELEGIVEL.value: 0.0,
        },
        description="CAPEX de implantação por hectare, por metodologia (inclui 3 anos de manutenção)",
    )
    custo_protecao_ha_ano_brl: Dict[str, float] = Field(
        default_factory=lambda: {
            Metodologia.REDD_CONSERVACAO.value: 80.0,
            Metodologia.IFM.value: 40.0,
        },
        description="Custo operacional anual de proteção da área, por metodologia",
    )
    taxa_desmatamento_baseline: float = Field(
        default=0.008, ge=0, lt=1,
        description="Taxa anual de desmatamento da linha de base para REDD (fração)",
    )


class LandBank(BaseModel):
    """Portfólio territorial consolidado."""
    nome: str = Field(..., description="Nome do Land Bank")
    operador: str = Field(
        default="Zion Hotel Group International", description="Operador do portfólio"
    )
    descricao: Optional[str] = Field(None, description="Descrição / tese do portfólio")
    glebas: List[Gleba] = Field(default_factory=list, description="Glebas do portfólio")
    premissas: PremissasCarbono = Field(
        default_factory=PremissasCarbono, description="Premissas do modelo de carbono"
    )
    meta_tco2e: Optional[float] = Field(
        None, description="Meta de créditos (tCO2e líquidos) que o portfólio precisa atingir"
    )


# ---------------------------------------------------------------------------
# Saídas
# ---------------------------------------------------------------------------

class TalhaoAvaliado(BaseModel):
    """Resultado da avaliação de um talhão."""
    talhao_id: str
    area_ha: float
    uso_solo: UsoSolo
    metodologia: Metodologia
    classe: ClasseElegibilidade
    motivo: str
    fator_tco2e_ha_ano: float = 0.0
    tco2e_bruto_horizonte: float = 0.0
    vcus_liquidos: float = 0.0
    custo_implantacao_brl: float = 0.0


class GlebaAvaliada(BaseModel):
    """Resultado consolidado por gleba."""
    gleba_id: str
    nome: str
    municipio: str
    uf: str
    bioma: Bioma
    status_dominial: StatusDominial
    area_total_ha: float
    area_elegivel_ha: float = 0.0
    area_condicionada_ha: float = 0.0
    area_inelegivel_ha: float = 0.0
    tco2e_bruto_horizonte: float = 0.0
    vcus_liquidos: float = 0.0
    vcus_condicionados: float = 0.0
    custo_implantacao_brl: float = 0.0
    custo_entrada_brl: float = 0.0
    readiness_score: float = 0.0
    classificacao: str = ""
    bloqueios: List[str] = Field(default_factory=list)
    pendencias: List[str] = Field(default_factory=list)
    talhoes: List[TalhaoAvaliado] = Field(default_factory=list)


class FluxoAnual(BaseModel):
    """Linha do fluxo de caixa anual de um cluster."""
    ano: int
    vcus_emitidos: float = 0.0
    receita_bruta_brl: float = 0.0
    receita_terrenistas_brl: float = 0.0
    custos_brl: float = 0.0
    fluxo_liquido_brl: float = 0.0
    fluxo_acumulado_brl: float = 0.0


class ClusterCarbono(BaseModel):
    """
    Agrupamento de glebas que compartilha um único projeto de carbono.
    É a unidade econômica real do Land Bank.
    """
    id: str
    nome: str
    bioma: Bioma
    municipios: List[str] = Field(default_factory=list)
    glebas_ids: List[str] = Field(default_factory=list)
    centro_lat: Optional[float] = None
    centro_lon: Optional[float] = None
    raio_max_km: float = 0.0
    area_total_ha: float = 0.0
    area_elegivel_ha: float = 0.0
    area_contratada_ha: float = 0.0
    vcus_liquidos: float = 0.0
    escala: str = ""
    gap_escala_ha: float = 0.0

    receita_bruta_brl: float = 0.0
    receita_terrenistas_brl: float = 0.0
    custo_estruturacao_brl: float = 0.0
    custo_implantacao_brl: float = 0.0
    custo_mrv_brl: float = 0.0
    custo_entrada_brl: float = 0.0
    resultado_liquido_zion_brl: float = 0.0
    vpl_brl: float = 0.0
    tir: Optional[float] = None
    payback_ano: Optional[int] = None
    custo_por_vcu_brl: float = 0.0
    preco_equilibrio_brl: Optional[float] = Field(
        None, description="Preço de tCO2e de remoção que zera o VPL do cluster"
    )
    prevenda_minima: Optional[float] = Field(
        None,
        description="Fração mínima de pré-venda com adiantamento que leva o VPL a zero "
                    "mantendo o preço spot modelado",
    )
    fluxo: List[FluxoAnual] = Field(default_factory=list)
    viavel: bool = False
    alertas: List[str] = Field(default_factory=list)


class PrioridadeAquisicao(BaseModel):
    """Recomendação de próxima terra a agregar."""
    gleba_id: str
    nome: str
    cluster_id: Optional[str]
    status_dominial: StatusDominial
    instrumento_recomendado: Instrumento
    area_elegivel_ha: float
    vcus_liquidos: float
    custo_entrada_brl: float
    vcus_por_mil_brl: float
    destrava_escala: bool
    prioridade: int
    justificativa: str


class CenarioCarbono(BaseModel):
    """Cenário de sensibilidade sobre preço e produtividade de carbono."""
    nome: str
    fator_preco: float
    fator_produtividade: float
    vcus_liquidos: float
    receita_bruta_brl: float
    resultado_liquido_zion_brl: float
    vpl_brl: float


class ResultadoLandBank(BaseModel):
    """Saída completa da análise do Land Bank."""
    nome: str
    data_analise: str
    horizonte_anos: int
    total_glebas: int
    area_total_ha: float = 0.0
    area_elegivel_ha: float = 0.0
    area_condicionada_ha: float = 0.0
    area_contratada_ha: float = 0.0
    area_prospeccao_ha: float = 0.0
    vcus_liquidos: float = 0.0
    vcus_condicionados: float = 0.0
    vcus_contratados: float = 0.0
    receita_bruta_brl: float = 0.0
    resultado_liquido_zion_brl: float = 0.0
    vpl_total_brl: float = 0.0
    readiness_medio: float = 0.0
    meta_tco2e: Optional[float] = None
    atingimento_meta: Optional[float] = None
    glebas: List[GlebaAvaliada] = Field(default_factory=list)
    clusters: List[ClusterCarbono] = Field(default_factory=list)
    prioridades: List[PrioridadeAquisicao] = Field(default_factory=list)
    cenarios: List[CenarioCarbono] = Field(default_factory=list)
    alertas: List[str] = Field(default_factory=list)
    premissas: Dict[str, Any] = Field(default_factory=dict)

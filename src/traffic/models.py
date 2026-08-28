"""
Schema do ZION TRAFFIC & ACQUISITION ARCHITECT™.

Modela campanhas, métricas e a cadeia de aquisição inteira — de impressão a
receita. O princípio que organiza tudo: não se compra tráfego, compra-se
oportunidade comercial qualificada.
"""

from datetime import date
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Classificação
# ---------------------------------------------------------------------------

class Canal(str, Enum):
    META = "meta_ads"
    GOOGLE_SEARCH = "google_search"
    GOOGLE_PMAX = "google_pmax"
    GOOGLE_DISPLAY = "google_display"
    YOUTUBE = "youtube"
    ORGANICO = "organico"
    EMAIL = "email"
    WHATSAPP = "whatsapp"


class Intencao(str, Enum):
    """Nível de consciência do usuário. Define mensagem e orçamento."""
    DESCOBERTA = "descoberta"        # não sabe que tem o problema
    CONSIDERACAO = "consideracao"    # sabe e está pesquisando
    DECISAO = "decisao"              # procura solução
    COMPRA = "compra"                # pronto para comprar


class EstagioPublico(str, Enum):
    FRIO = "frio"
    MORNO = "morno"
    QUENTE = "quente"
    CLIENTE = "cliente"
    ASCENSAO = "ascensao"


class FuncaoCriativo(str, Enum):
    """Todo criativo tem uma função. 'Imagem bonita da Zion' não é função."""
    EDUCAR = "educar"
    PROVOCAR = "provocar"
    PROVAR = "provar"
    GERAR_DESEJO = "gerar_desejo"
    QUEBRAR_OBJECAO = "quebrar_objecao"
    VENDER = "vender"


class Angulo(str, Enum):
    PATRIMONIO = "patrimonio"
    RENDA = "renda"
    ERRO = "erro"
    DESCOBERTA = "descoberta"
    LIBERDADE = "liberdade"
    INVESTIMENTO = "investimento"
    TRANSFORMACAO = "transformacao"
    AUTORIDADE = "autoridade"


class ProdutoZion(str, Enum):
    LIVRO = "livro"
    EBOOK = "ebook"
    DIAGNOSTICO = "diagnostico"
    MENTORIA = "mentoria"
    CONSULTORIA = "consultoria"
    DESENVOLVIMENTO = "desenvolvimento"
    PRODUTO = "produto"
    INVESTIMENTO = "investimento"


class EtapaCadeia(str, Enum):
    """A cadeia de aquisição. O gargalo pode estar em qualquer ponto."""
    PUBLICO = "01_publico"
    CRIATIVO = "02_criativo"
    CLIQUE = "03_clique"
    PAGINA = "04_pagina"
    LEAD = "05_lead"
    QUALIFICACAO = "06_qualificacao"
    OFERTA = "07_oferta"
    VENDA = "08_venda"


# ---------------------------------------------------------------------------
# Campanha
# ---------------------------------------------------------------------------

class BriefingCampanha(BaseModel):
    """
    As dez respostas obrigatórias antes de qualquer campanha existir.

    Campo nulo significa pergunta sem resposta — e pergunta sem resposta
    bloqueia a criação da campanha.
    """
    o_que_vendemos: Optional[str] = None
    para_quem: Optional[str] = None
    qual_problema: Optional[str] = None
    qual_desejo: Optional[str] = None
    qual_transformacao: Optional[str] = None
    qual_oferta: Optional[str] = None
    qual_preco_brl: Optional[float] = None
    qual_funil: Optional[str] = None
    qual_evento_conversao: Optional[str] = None
    meta_receita_brl: Optional[float] = None


class MetasCampanha(BaseModel):
    """Metas contra as quais a campanha é julgada."""
    cpa_alvo_brl: Optional[float] = None
    cac_alvo_brl: Optional[float] = None
    cpqo_alvo_brl: Optional[float] = Field(
        None, description="Custo por oportunidade qualificada — a métrica que manda"
    )
    receita_alvo_brl: Optional[float] = None
    roas_alvo: Optional[float] = None


class Criativo(BaseModel):
    """Uma peça, com função declarada e métricas próprias."""
    id: str
    nome: str
    funcao: FuncaoCriativo
    angulo: Angulo
    formato: str = Field(default="video", description="video, imagem, carrossel")
    hook: Optional[str] = None
    impressoes: int = 0
    cliques: int = 0
    investimento_brl: float = 0.0
    leads: int = 0
    ativo: bool = True


class MetricasCampanha(BaseModel):
    """Dados brutos vindos da plataforma. Nada calculado aqui."""
    investimento_brl: float = 0.0
    impressoes: int = 0
    cliques: int = 0
    visitas_pagina: int = 0
    leads: int = 0
    leads_qualificados: int = 0
    oportunidades: int = 0
    vendas: int = 0
    receita_brl: float = 0.0


class Campanha(BaseModel):
    """Uma campanha documentada conforme a estrutura obrigatória."""
    id: str
    nome: str
    canal: Canal
    produto: ProdutoZion
    intencao: Intencao
    estagio_publico: EstagioPublico
    objetivo: str

    briefing: BriefingCampanha = Field(default_factory=BriefingCampanha)
    metas: MetasCampanha = Field(default_factory=MetasCampanha)
    metricas: MetricasCampanha = Field(default_factory=MetricasCampanha)
    criativos: List[Criativo] = Field(default_factory=list)

    orcamento_diario_brl: Optional[float] = None
    landing_page: Optional[str] = None
    evento_conversao: Optional[str] = None
    utm_campaign: Optional[str] = None
    data_inicio: Optional[date] = None
    data_revisao: Optional[date] = None
    ativa: bool = True
    observacoes: Optional[str] = None


class ContaTrafego(BaseModel):
    """Conjunto de campanhas sob análise."""
    nome: str = "Aquisição Zion"
    periodo: Optional[str] = None
    data_referencia: Optional[date] = None
    campanhas: List[Campanha] = Field(default_factory=list)
    ticket_medio_por_produto_brl: Dict[str, float] = Field(
        default_factory=dict, description="Ticket de referência por produto, para metas de CAC"
    )
    margem_por_produto: Dict[str, float] = Field(
        default_factory=dict, description="Margem bruta (0-1) por produto"
    )


# ---------------------------------------------------------------------------
# Saídas
# ---------------------------------------------------------------------------

class ResultadoGate(BaseModel):
    """Veredito do gate: a campanha pode ser criada?"""
    campanha_id: str
    liberada: bool
    perguntas_sem_resposta: List[str] = Field(default_factory=list)
    pendencias_estruturais: List[str] = Field(default_factory=list)
    veredito: str


class Metricas(BaseModel):
    """Métricas derivadas. None quando o denominador é zero — nunca zero falso."""
    investimento_brl: float = 0.0
    cpm_brl: Optional[float] = None
    ctr: Optional[float] = None
    cpc_brl: Optional[float] = None
    taxa_conversao_pagina: Optional[float] = None
    cpl_brl: Optional[float] = None
    taxa_qualificacao: Optional[float] = None
    cpql_brl: Optional[float] = None
    cpqo_brl: Optional[float] = Field(None, description="Custo por oportunidade qualificada")
    taxa_fechamento: Optional[float] = None
    cac_brl: Optional[float] = None
    receita_brl: float = 0.0
    roas: Optional[float] = None
    lucro_bruto_brl: Optional[float] = None


class AchadoDiagnostico(BaseModel):
    """Um ponto da cadeia que está quebrando."""
    etapa: EtapaCadeia
    gravidade: str
    sintoma: str
    causa_provavel: str
    acao: str
    confianca_estatistica: str


class DiagnosticoCampanha(BaseModel):
    campanha_id: str
    nome: str
    metricas: Metricas
    gargalo: Optional[EtapaCadeia] = None
    achados: List[AchadoDiagnostico] = Field(default_factory=list)
    volume_suficiente: bool = False
    leitura: str = ""


class DecisaoOtimizacao(BaseModel):
    """Recomendação de ação sobre a campanha, com o critério explícito."""
    campanha_id: str
    acao: str = Field(..., description="escalar, manter, investigar, pausar, aguardar_volume")
    justificativa: str
    evidencia: str
    bloqueios_de_escala: List[str] = Field(default_factory=list)


class AtribuicaoCampanha(BaseModel):
    """O que uma campanha realmente gerou, medido pelo CRM."""
    campanha_id: str
    nome: str
    canal: Canal
    investimento_brl: float
    leads: int
    qualificados: int
    oportunidades: int
    clientes: int
    receita_brl: float
    cpl_brl: Optional[float] = None
    cpqo_brl: Optional[float] = None
    cac_brl: Optional[float] = None
    roas: Optional[float] = None
    ranking_por_leads: int = 0
    ranking_por_receita: int = 0
    divergencia_de_ranking: bool = False


class RelatorioTrafego(BaseModel):
    """Saída consolidada da análise de aquisição."""
    data: str
    periodo: Optional[str] = None
    investimento_total_brl: float = 0.0
    receita_total_brl: float = 0.0
    roas_geral: Optional[float] = None
    leads: int = 0
    oportunidades: int = 0
    vendas: int = 0
    cpqo_geral_brl: Optional[float] = None
    cac_geral_brl: Optional[float] = None
    gates: List[ResultadoGate] = Field(default_factory=list)
    diagnosticos: List[DiagnosticoCampanha] = Field(default_factory=list)
    decisoes: List[DecisaoOtimizacao] = Field(default_factory=list)
    atribuicao: List[AtribuicaoCampanha] = Field(default_factory=list)
    gargalo_geral: Optional[EtapaCadeia] = None
    acoes_recomendadas: List[str] = Field(default_factory=list)

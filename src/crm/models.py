"""
Schema do ZION CRM & LEAD INTELLIGENCE™.

Modela a travessia CONTATO → LEAD → OPORTUNIDADE → CLIENTE → PROJETO → ASCENSÃO,
com o que o CRM precisa responder sobre cada pessoa: contexto, classificação,
estágio, potencial e próxima ação.
"""

from datetime import date
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Classificação
# ---------------------------------------------------------------------------

class Perfil(str, Enum):
    """Os nove perfis principais da base Zion."""
    PROPRIETARIO_TERRENO = "01_proprietario_terreno"
    INVESTIDOR = "02_investidor"
    EMPREENDEDOR = "03_empreendedor"
    OPERADOR = "04_operador"                 # Airbnb, pousada, hotel
    DESENVOLVEDOR = "05_desenvolvedor"
    PROFISSIONAL = "06_profissional"         # arquiteto, engenheiro, corretor
    INVESTIDOR_INSTITUCIONAL = "07_investidor_institucional"
    ALUNO = "08_aluno"
    POTENCIAL_PARCEIRO = "09_potencial_parceiro"
    NAO_CLASSIFICADO = "00_nao_classificado"


class Tri(str, Enum):
    """Sim / Não / Desconhecido. Desconhecido nunca é sinônimo de não."""
    SIM = "sim"
    NAO = "nao"
    DESCONHECIDO = "desconhecido"


class Objetivo(str, Enum):
    """O que a pessoa quer — define a porta de entrada."""
    APRENDER = "quer_aprender"
    COMPRAR = "quer_comprar"
    DESENVOLVER = "quer_desenvolver"
    CAPITAL = "precisa_capital"
    OPERAR = "quer_operar"
    INVESTIR = "quer_investir"
    PARCERIA = "quer_parceria"
    NAO_SABE = "nao_sabe"
    DESCONHECIDO = "desconhecido"


class Porta(str, Enum):
    """Oferta Zion para onde o lead deve ser roteado."""
    DIAGNOSTICO = "diagnostico"
    MENTORIA = "mentoria"
    PRODUTO = "produto"
    DESENVOLVIMENTO = "desenvolvimento"
    CAPITAL = "capital"
    INVESTIMENTO = "investimento"
    MANAGEMENT = "management"
    PARCERIA = "parceria"
    NUTRICAO = "nutricao"


class Estagio(str, Enum):
    """Pipeline comercial. Só muda com mudança real de situação."""
    NOVO_LEAD = "01_novo_lead"
    CONTATO_INICIADO = "02_contato_iniciado"
    QUALIFICACAO = "03_qualificacao"
    DIAGNOSTICO = "04_diagnostico"
    REUNIAO = "05_reuniao"
    OFERTA = "06_oferta"
    NEGOCIACAO = "07_negociacao"
    DECISAO = "08_decisao"
    GANHO = "09_ganho"
    PERDIDO = "10_perdido"


class Temperatura(str, Enum):
    FRIO = "frio"
    MORNO = "morno"
    QUENTE = "quente"
    OPORTUNIDADE = "oportunidade"


class MotivoPerda(str, Enum):
    """Perda sem motivo não é permitida."""
    SEM_CAPITAL = "sem_capital"
    SEM_TERRENO = "sem_terreno"
    SEM_DECISAO = "sem_decisao"
    TIMING = "timing"
    PRECO = "preco"
    CONCORRENTE = "escolheu_concorrente"
    PROJETO_INVIAVEL = "projeto_inviavel"
    NAO_RESPONDEU = "nao_respondeu"
    DESISTIU = "desistiu"
    ADIOU = "adiou"
    SEM_FIT = "sem_fit"
    OUTRO = "outro"


class Origem(str, Enum):
    INSTAGRAM = "instagram"
    META_ADS = "meta_ads"
    GOOGLE_ADS = "google_ads"
    ORGANICO = "organico"
    YOUTUBE = "youtube"
    WHATSAPP = "whatsapp"
    INDICACAO = "indicacao"
    EVENTO = "evento"
    PODCAST = "podcast"
    SITE = "site"
    LIVRO = "livro"
    MENTORIA = "mentoria"
    PARCEIRO = "parceiro"
    OUTRO = "outro"
    DESCONHECIDA = "desconhecida"


# ---------------------------------------------------------------------------
# Lead
# ---------------------------------------------------------------------------

class Ativos(BaseModel):
    """O que o lead possui. Determina qual porta da Zion faz sentido."""
    terreno: Tri = Tri.DESCONHECIDO
    capital: Tri = Tri.DESCONHECIDO
    operacao: Tri = Tri.DESCONHECIDO
    projeto: Tri = Tri.DESCONHECIDO
    marca: Tri = Tri.DESCONHECIDO
    experiencia: Tri = Tri.DESCONHECIDO
    rede: Tri = Tri.DESCONHECIDO

    def conhecidos(self) -> int:
        return sum(1 for v in self.model_dump().values() if v != Tri.DESCONHECIDO.value)

    def possui(self) -> List[str]:
        return [k for k, v in self.model_dump().items() if v == Tri.SIM.value]


class DadosTerreno(BaseModel):
    area_ha: Optional[float] = None
    localizacao: Optional[str] = None
    tipo_propriedade: Optional[str] = None
    documentacao_regular: Tri = Tri.DESCONHECIDO


class DadosFinanceiros(BaseModel):
    capital_disponivel_brl: Optional[float] = None
    faixa_investimento_brl: Optional[float] = None
    origem_capital: Optional[str] = None
    busca_financiamento: Tri = Tri.DESCONHECIDO


class DadosProjeto(BaseModel):
    estagio: Optional[str] = Field(None, description="terreno, conceito, projeto, obra, operação")
    objetivo: Optional[str] = None
    numero_unidades: Optional[int] = None
    modelo_desejado: Optional[str] = None
    prazo_meses: Optional[int] = None


class Interacao(BaseModel):
    """Registro de contato. Atividade não é avanço de estágio."""
    data: date
    canal: str
    o_que_foi_enviado: str
    resposta: Optional[str] = None


class ProximaAcao(BaseModel):
    """Todo lead aberto precisa de uma. 'Aguardando retorno' não é ação."""
    acao: str
    data_prevista: date
    responsavel: str


class Lead(BaseModel):
    """Uma pessoa na base comercial da Zion."""
    id: str
    nome: str
    empresa: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    pais: str = "Brasil"
    instagram: Optional[str] = None
    site: Optional[str] = None

    perfil: Perfil = Perfil.NAO_CLASSIFICADO
    objetivo: Objetivo = Objetivo.DESCONHECIDO
    origem_primeira: Origem = Origem.DESCONHECIDA
    origem_ultima: Origem = Origem.DESCONHECIDA

    ativos: Ativos = Field(default_factory=Ativos)
    terreno: DadosTerreno = Field(default_factory=DadosTerreno)
    financeiro: DadosFinanceiros = Field(default_factory=DadosFinanceiros)
    projeto: DadosProjeto = Field(default_factory=DadosProjeto)

    estagio: Estagio = Estagio.NOVO_LEAD
    e_decisor: Tri = Tri.DESCONHECIDO
    valor_potencial_brl: Optional[float] = None
    responsavel: Optional[str] = None
    proxima_acao: Optional[ProximaAcao] = None
    motivo_perda: Optional[MotivoPerda] = None
    observacao_perda: Optional[str] = None

    interacoes: List[Interacao] = Field(default_factory=list)
    data_criacao: Optional[date] = None
    data_ultima_atividade: Optional[date] = None
    cliente_desde: Optional[date] = None
    produtos_contratados: List[Porta] = Field(default_factory=list)

    observacoes: Optional[str] = None


class BaseComercial(BaseModel):
    """A base de leads da Zion."""
    nome: str = "Base Comercial Zion"
    data_referencia: Optional[date] = None
    leads: List[Lead] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Saídas
# ---------------------------------------------------------------------------

class DimensaoScore(BaseModel):
    """Uma das oito dimensões do Zion Lead Score™."""
    nome: str
    valor: float = Field(..., ge=0, le=10)
    peso: float
    base: str = Field(..., description="informada, derivada ou desconhecida")
    justificativa: str


class ZionLeadScore(BaseModel):
    """
    Pontuação do lead, com confiança separada da nota.

    Um lead sem informação não é um lead ruim: é um lead não qualificado.
    Por isso a nota vem acompanhada da confiança — quanto dela se apoia em
    dado real, e não em ausência de dado.
    """
    lead_id: str
    score: float = Field(..., ge=0, le=10)
    confianca: float = Field(..., ge=0, le=1, description="Fração do score apoiada em dado conhecido")
    temperatura: Temperatura
    dimensoes: List[DimensaoScore]
    alertas: List[str] = Field(default_factory=list)


class Roteamento(BaseModel):
    """Para onde este lead deve ir e por quê."""
    lead_id: str
    porta: Porta
    justificativa: str
    proximo_passo_logico: str
    nao_ofertar: List[str] = Field(
        default_factory=list, description="Ofertas que seriam empurrar venda neste momento"
    )
    perguntas_de_qualificacao: List[str] = Field(default_factory=list)


class LeadQualificado(BaseModel):
    """Lead com score, temperatura e roteamento resolvidos."""
    lead: Lead
    score: ZionLeadScore
    roteamento: Roteamento
    prioridade: int = 0


class AchadoHigiene(BaseModel):
    """Inconsistência encontrada na base."""
    codigo: str
    gravidade: str
    tema: str
    descricao: str
    leads: List[str] = Field(default_factory=list)
    acao: str


class EtapaFunil(BaseModel):
    estagio: Estagio
    quantidade: int
    valor_potencial_brl: float = 0.0
    conversao_da_anterior: Optional[float] = None


class AnaliseFunil(BaseModel):
    etapas: List[EtapaFunil]
    gargalo: Optional[str] = None
    diagnostico: str = ""
    total_leads: int = 0
    pipeline_aberto_brl: float = 0.0
    ganhos: int = 0
    perdidos: int = 0
    taxa_conversao_total: Optional[float] = None
    motivos_perda: Dict[str, int] = Field(default_factory=dict)


class ItemReativacao(BaseModel):
    """Lead antigo com fit que merece nova abordagem."""
    lead_id: str
    nome: str
    contexto: str
    ultima_interacao: Optional[date]
    dias_parado: Optional[int]
    score: float
    porta_potencial: Porta
    provavel_problema: str
    abordagem_recomendada: str


class RelatorioComercial(BaseModel):
    """Saída consolidada da análise da base."""
    data: str
    total_leads: int
    novos: int
    quentes: int
    oportunidades: int
    parados: int
    followups_atrasados: int
    pipeline_aberto_brl: float
    qualificados: List[LeadQualificado] = Field(default_factory=list)
    funil: Optional[AnaliseFunil] = None
    higiene: List[AchadoHigiene] = Field(default_factory=list)
    reativacao: List[ItemReativacao] = Field(default_factory=list)
    acoes_recomendadas: List[str] = Field(default_factory=list)

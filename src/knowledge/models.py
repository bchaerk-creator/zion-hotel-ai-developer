"""
Schema do Zion Knowledge Engine™.

Estruturas que preservam conhecimento com proveniência, hierarquia e versão.
A regra que governa este módulo: nada entra sem fonte declarada, e o que não
tem fonte entra marcado como pendente — nunca como fato.
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Classificação
# ---------------------------------------------------------------------------

class Nivel(str, Enum):
    """Hierarquia da informação — do mais abstrato ao mais concreto."""
    PRINCIPIO = "1_principio"      # filosofia central
    METODO = "2_metodo"            # como a Zion organiza o raciocínio
    FRAMEWORK = "3_framework"      # estrutura de análise
    FERRAMENTA = "4_ferramenta"    # instrumento de aplicação
    PROCESSO = "5_processo"        # sequência operacional
    ENTREGAVEL = "6_entregavel"    # resultado produzido
    CASE = "7_case"                # evidência prática


class Pilar(str, Enum):
    """Os sete pilares do Método Zion 360°."""
    TERRITORIO = "01_territorio"
    MERCADO = "02_mercado"
    PRODUTO = "03_produto"
    ESTRATEGIA = "04_estrategia"
    INVESTIMENTO = "05_investimento"
    IMPLANTACAO = "06_implantacao"
    LANCAMENTO = "07_lancamento"
    TRANSVERSAL = "00_transversal"


class Proveniencia(str, Enum):
    """De onde a informação vem. Nunca misturar."""
    ZION = "zion"              # vem dos materiais oficiais
    EXTERNO = "externo"        # pesquisa ou conhecimento geral de mercado
    INFERENCIA = "inferencia"  # conclusão estratégica, não metodologia oficial


class Status(str, Enum):
    """Estado de validação do registro."""
    ATUAL = "atual"
    HISTORICA = "historica"
    OBSOLETA = "obsoleta"
    PENDENTE_VALIDACAO = "pendente_validacao"
    PENDENTE_DE_FONTE = "pendente_de_fonte"  # nome conhecido, conteúdo não documentado


# ---------------------------------------------------------------------------
# Proveniência
# ---------------------------------------------------------------------------

class Fonte(BaseModel):
    """Origem rastreável de uma informação."""
    documento: str = Field(..., description="Nome do documento, livro ou material")
    tipo: str = Field(default="documento", description="livro, documento, código, sessão, operação")
    localizacao: Optional[str] = Field(None, description="Capítulo, seção, arquivo ou linha")
    data: Optional[str] = Field(None, description="Data do material")
    disponivel_no_sistema: bool = Field(
        default=False,
        description="Se o material está carregado no repositório. Falso significa que "
                    "o conteúdo foi declarado mas não pode ser verificado aqui.",
    )


# ---------------------------------------------------------------------------
# Itens de conhecimento
# ---------------------------------------------------------------------------

class ItemBase(BaseModel):
    """Campos comuns a todo item registrado."""
    id: str = Field(..., description="Identificador único")
    nome: str = Field(..., description="Nome oficial — preservar exatamente")
    nivel: Nivel
    pilar: Pilar = Field(default=Pilar.TRANSVERSAL)
    proveniencia: Proveniencia = Field(default=Proveniencia.ZION)
    status: Status = Field(default=Status.ATUAL)
    fonte: Fonte
    observacoes: Optional[str] = None


class Conceito(ItemBase):
    """Uma ideia da metodologia."""
    definicao: str = Field(..., description="O que é")
    problema_que_resolve: Optional[str] = None
    quando_utilizar: Optional[str] = None
    conceitos_relacionados: List[str] = Field(default_factory=list)
    ferramentas_relacionadas: List[str] = Field(default_factory=list)
    entregaveis_relacionados: List[str] = Field(default_factory=list)
    perguntas: List[str] = Field(default_factory=list)
    decisao_que_permite: Optional[str] = Field(
        None, description="Qual decisão este conhecimento habilita"
    )
    exemplos: List[str] = Field(default_factory=list)
    cases: List[str] = Field(default_factory=list)


class Ferramenta(ItemBase):
    """Instrumento proprietário de aplicação. Nome e função são invioláveis."""
    objetivo: str
    problema_resolvido: Optional[str] = None
    entradas: List[str] = Field(default_factory=list)
    processo: List[str] = Field(default_factory=list)
    saida: Optional[str] = None
    interpretacao: Optional[str] = None
    entregavel_id: Optional[str] = None
    decisao_gerada: Optional[str] = None
    modulo_sistema: Optional[str] = Field(
        None, description="Onde a ferramenta está implementada no código, se estiver"
    )


class Entregavel(ItemBase):
    """Resultado produzido pela metodologia."""
    objetivo: str
    responsavel: Optional[str] = None
    momento: Optional[str] = None
    entradas: List[str] = Field(default_factory=list)
    estrutura: List[str] = Field(default_factory=list)
    criterios: List[str] = Field(default_factory=list)
    ferramenta_id: Optional[str] = None
    decisao_produzida: Optional[str] = None
    proximo_entregavel: Optional[str] = None


class Pergunta(BaseModel):
    """Unidade pedagógica: conhecimento transformado em raciocínio."""
    id: str
    pergunta: str
    pilar: Pilar
    desdobramentos: List[str] = Field(
        default_factory=list, description="Perguntas que vêm depois desta"
    )
    decisao_associada: Optional[str] = None
    fonte: Fonte


class Erro(BaseModel):
    """Erro recorrente de developer."""
    id: str
    nome: str
    pilar: Pilar
    o_que_e: str
    por_que_acontece: Optional[str] = None
    consequencia: Optional[str] = None
    como_evitar: Optional[str] = None
    como_diagnosticar: Optional[str] = None
    ferramenta_que_combate: Optional[str] = None
    fonte: Fonte


class Decisao(BaseModel):
    """Decisão que o developer precisa tomar."""
    id: str
    numero: int
    pergunta: str
    pilar: Pilar
    conhecimento_necessario: List[str] = Field(default_factory=list)
    ferramenta_id: Optional[str] = None
    entregavel_id: Optional[str] = None
    decisao_anterior: Optional[str] = None
    decisao_seguinte: Optional[str] = None
    fonte: Fonte


class Case(BaseModel):
    """Evidência prática. Nunca inventar resultado."""
    id: str
    nome: str
    pilar: Pilar
    contexto: str
    problema: Optional[str] = None
    hipotese: Optional[str] = None
    decisao: Optional[str] = None
    execucao: Optional[str] = None
    resultado: str = Field(
        default="Resultado não documentado.",
        description="Se não houver resultado documentado, manter o texto padrão",
    )
    aprendizado: Optional[str] = None
    aplicacao: Optional[str] = None
    fonte: Fonte
    status: Status = Field(default=Status.PENDENTE_VALIDACAO)


class RegistroNumerico(BaseModel):
    """
    Número com contexto obrigatório.

    Um número sem período e sem origem não é informação, é boato com aparência
    de dado. Este modelo existe para tornar isso impossível.
    """
    id: str
    indicador: str
    valor: float
    unidade: str
    periodo: str = Field(
        default="Período não informado na fonte.",
        description="Período de referência. Manter o texto padrão quando ausente.",
    )
    contexto: str = Field(..., description="A que operação, projeto ou cenário se refere")
    fonte: Fonte
    status: Status = Field(default=Status.PENDENTE_VALIDACAO)

    def citacao(self) -> str:
        """Formata o número no padrão de citação obrigatório."""
        return (
            f"Segundo {self.fonte.documento} ({self.periodo}), "
            f"{self.indicador} foi {self.valor:g} {self.unidade} — {self.contexto}."
        )


class Divergencia(BaseModel):
    """
    Conflito entre fontes que não pode ser resolvido em silêncio.

    Registrar a divergência é obrigatório; escolher um lado sozinho é proibido.
    """
    id: str
    tema: str
    descricao: str
    versao_a: str
    fonte_a: Fonte
    versao_b: str
    fonte_b: Fonte
    impacto: str = Field(..., description="O que muda na prática dependendo da escolha")
    status: Status = Field(default=Status.PENDENTE_VALIDACAO)
    resolucao: Optional[str] = Field(None, description="Preenchido só por decisão do fundador")


class Lacuna(BaseModel):
    """Conhecimento que a Zion tem mas o sistema ainda não recebeu."""
    id: str
    item: str
    tipo: str = Field(..., description="ferramenta, livro, case, número, documento")
    por_que_importa: str
    o_que_falta: str
    bloqueia: List[str] = Field(
        default_factory=list, description="O que não pode ser produzido sem isso"
    )

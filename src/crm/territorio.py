"""
Ponte entre o ZION CRM & LEAD INTELLIGENCE™ e o Land Bank Zion.

O CRM sabe quem é o dono da terra; o Land Bank sabe o que a terra vale em
carbono. Enquanto as duas bases vivem separadas, ninguém consegue responder
três perguntas simples de diretoria:

    1. Quantas oportunidades existem, de fato, abertas?
    2. Quanto de investimento foi declarado por essas pessoas?
    3. Quantos hectares a Zion já tem no banco de áreas?

Este módulo responde as três de forma determinística — contagem e regra, sem
LLM e sem chave de API — e faz a única coisa que uma consolidação honesta
precisa fazer: separar o que é declarado do que é verificado, e nunca contar
o mesmo hectare duas vezes.

Regra de ouro da consolidação: uma gleba já registrada no Land Bank e também
declarada por um lead é UMA área, não duas. O vínculo (`lead.glebas_land_bank`)
é o que permite enxergar a sobreposição e descontá-la do total.
"""

import unicodedata
from collections import defaultdict
from datetime import date
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel, Field

from src.crm.engine import qualificar
from src.crm.models import BaseComercial, Estagio, Lead, Perfil, Temperatura, Tri
from src.crm.operacoes import ESTAGIOS_ABERTOS
from src.models.land_bank import Gleba, LandBank, StatusDominial

# Estágios em que existe uma oferta concreta sobre a mesa.
ESTAGIOS_COM_OFERTA = [Estagio.OFERTA, Estagio.NEGOCIACAO, Estagio.DECISAO]

# Divergência de área tolerada entre a declaração do lead e o registro da gleba
# antes de virar alerta. Acima disso, alguém mediu errado — ou são áreas diferentes.
TOLERANCIA_AREA = 0.10

# Perfis que tipicamente trazem terra para o banco de áreas.
PERFIS_TERRITORIAIS = [
    Perfil.PROPRIETARIO_TERRENO,
    Perfil.DESENVOLVEDOR,
    Perfil.POTENCIAL_PARCEIRO,
    Perfil.EMPREENDEDOR,
    Perfil.OPERADOR,
]


# ---------------------------------------------------------------------------
# Saídas
# ---------------------------------------------------------------------------

class VinculoTerritorial(BaseModel):
    """Amarração entre um lead do CRM e uma gleba do Land Bank."""
    lead_id: str
    lead_nome: str
    gleba_id: str
    gleba_nome: Optional[str] = None
    municipio: Optional[str] = None
    uf: Optional[str] = None
    area_lead_ha: Optional[float] = None
    area_gleba_ha: Optional[float] = None
    status_dominial: Optional[StatusDominial] = None
    origem: str = Field(..., description="'declarado' (vínculo na base) ou 'sugerido' (inferido)")
    evidencia: str = ""
    divergencia_area: Optional[float] = Field(
        None, description="Diferença relativa entre a área declarada e a registrada"
    )


class TotalOportunidades(BaseModel):
    """
    Contagem de oportunidades, com a definição explícita de cada número.

    'Oportunidade' é palavra que cada empresa usa de um jeito. Aqui os três
    recortes convivem, cada um com seu nome, para ninguém discutir número.
    """
    abertas: int = Field(..., description="Leads em estágio aberto — o pipeline real")
    com_oferta_na_mesa: int = Field(..., description="Em oferta, negociação ou decisão")
    sinalizadas_quentes: int = Field(..., description="Temperatura 'oportunidade' pelo Zion Lead Score™")
    territoriais: int = Field(..., description="Oportunidades abertas que trazem terra")
    ganhas: int = 0
    perdidas: int = 0
    total_base: int = 0
    por_estagio: Dict[str, int] = Field(default_factory=dict)
    por_perfil: Dict[str, int] = Field(default_factory=dict)


class TotalInvestimentos(BaseModel):
    """
    Investimento declarado pela base. Declarado, não verificado.

    Ninguém conferiu extrato. Este número é a soma do que as pessoas disseram
    ter ou pretender investir — serve para dimensionar apetite, não para
    lastrear captação. A cobertura diz sobre quantos leads ele se apoia.
    """
    declarado_brl: float = 0.0
    declarado_aberto_brl: float = Field(0.0, description="Parcela em leads de pipeline aberto")
    declarado_ganho_brl: float = 0.0
    declarado_perdido_brl: float = 0.0
    leads_declarantes: int = 0
    leads_sem_declaracao: int = 0
    cobertura: float = Field(0.0, description="Fração da base que declarou algum valor")
    ticket_medio_brl: float = 0.0
    maior_declaracao_brl: float = 0.0
    maior_declarante: Optional[str] = None
    por_perfil: Dict[str, float] = Field(default_factory=dict)
    pipeline_zion_brl: float = Field(
        0.0, description="Soma de valor_potencial_brl — receita da Zion, número diferente e não somável"
    )


class TotalAreas(BaseModel):
    """
    Hectares consolidados entre o banco de áreas e a originação do CRM,
    sem contar o mesmo hectare duas vezes.
    """
    land_bank_ha: float = 0.0
    land_bank_glebas: int = 0
    por_status_ha: Dict[str, float] = Field(default_factory=dict)
    sob_controle_ha: float = Field(0.0, description="Própria + contratada — o que a Zion realmente tem")
    originacao_aberta_ha: float = Field(
        0.0, description="Área declarada por leads abertos que ainda não está no banco"
    )
    originacao_fechada_ha: float = Field(
        0.0, description="Área em leads já ganhos ou perdidos, fora do banco"
    )
    sobreposicao_ha: float = Field(
        0.0, description="Área presente nas duas bases — contada uma única vez no total"
    )
    total_consolidado_ha: float = Field(
        0.0, description="Land Bank + originação aberta, já descontada a sobreposição"
    )
    leads_com_area: int = 0
    leads_terreno_sem_area: int = Field(
        0, description="Leads que dizem ter terreno mas não declararam a área"
    )
    cobertura_area: float = 0.0
    por_uf_ha: Dict[str, Dict[str, float]] = Field(
        default_factory=dict, description="Por UF: hectares no banco e em originação"
    )


class OportunidadeTerritorial(BaseModel):
    """Lead aberto que traz terra e ainda não está no banco de áreas."""
    lead_id: str
    nome: str
    municipio: Optional[str] = None
    uf: Optional[str] = None
    area_ha: float
    estagio: Estagio
    temperatura: Temperatura
    score: float
    confianca: float
    investimento_declarado_brl: Optional[float] = None
    documentacao_regular: Tri = Tri.DESCONHECIDO
    responsavel: Optional[str] = None
    observacao: str = ""


class PainelTerritorial(BaseModel):
    """Painel consolidado Land Bank × CRM."""
    data: str
    land_bank_nome: Optional[str] = None
    base_nome: str = ""
    oportunidades: TotalOportunidades
    investimentos: TotalInvestimentos
    areas: TotalAreas
    vinculos: List[VinculoTerritorial] = Field(default_factory=list)
    sugestoes_vinculo: List[VinculoTerritorial] = Field(default_factory=list)
    originacao: List[OportunidadeTerritorial] = Field(default_factory=list)
    alertas: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Auxiliares
# ---------------------------------------------------------------------------

def _norm(texto: Optional[str]) -> str:
    """Minúsculas, sem acento, sem espaço nas pontas — para comparar nomes."""
    if not texto:
        return ""
    sem_acento = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    return " ".join(sem_acento.lower().split())


def investimento_declarado(lead: Lead) -> Optional[float]:
    """
    O que o lead declarou que pretende ou pode investir.

    Prioriza a faixa de investimento (intenção declarada) sobre o capital
    disponível (capacidade declarada). Quando só existe um dos dois, usa o que
    existe. Ausência dos dois é ausência de informação — nunca zero.
    """
    fin = lead.financeiro
    if fin.faixa_investimento_brl:
        return float(fin.faixa_investimento_brl)
    if fin.capital_disponivel_brl:
        return float(fin.capital_disponivel_brl)
    return None


def area_declarada(lead: Lead) -> Optional[float]:
    area = lead.terreno.area_ha
    return float(area) if area and area > 0 else None


def _indice_glebas(land_bank: Optional[LandBank]) -> Dict[str, Gleba]:
    return {g.id: g for g in land_bank.glebas} if land_bank else {}


# ---------------------------------------------------------------------------
# Vínculos
# ---------------------------------------------------------------------------

def _vinculo_declarado(lead: Lead, gleba: Gleba) -> VinculoTerritorial:
    area_lead = area_declarada(lead)
    divergencia = None
    if area_lead:
        divergencia = abs(area_lead - gleba.area_total_ha) / gleba.area_total_ha
    return VinculoTerritorial(
        lead_id=lead.id,
        lead_nome=lead.nome,
        gleba_id=gleba.id,
        gleba_nome=gleba.nome,
        municipio=gleba.municipio,
        uf=gleba.uf,
        area_lead_ha=area_lead,
        area_gleba_ha=gleba.area_total_ha,
        status_dominial=gleba.status_dominial,
        origem="declarado",
        evidencia="Vínculo registrado na base comercial",
        divergencia_area=divergencia,
    )


def sugerir_vinculos(
    base: BaseComercial, land_bank: LandBank, ja_vinculadas: Optional[set] = None
) -> List[VinculoTerritorial]:
    """
    Aponta prováveis pares lead ↔ gleba que ninguém amarrou ainda.

    Sugestão nunca vira vínculo sozinha e nunca entra na conta de área: a
    consolidação só desconta sobreposição de vínculo declarado. O critério é
    conservador de propósito — mesmo município e UF MAIS uma corroboração
    (área compatível ou nome do proprietário batendo com o do lead).
    """
    ja_vinculadas = ja_vinculadas or set()
    sugestoes: List[VinculoTerritorial] = []

    for lead in base.leads:
        if lead.glebas_land_bank:
            continue
        cidade, uf = _norm(lead.cidade), _norm(lead.estado)
        if not cidade or not uf:
            continue
        area_lead = area_declarada(lead)
        tokens_lead = {t for t in _norm(lead.nome).split() if len(t) >= 4}

        for gleba in land_bank.glebas:
            if gleba.id in ja_vinculadas:
                continue
            if _norm(gleba.municipio) != cidade or _norm(gleba.uf) != uf:
                continue

            evidencias: List[str] = []
            if area_lead:
                divergencia = abs(area_lead - gleba.area_total_ha) / gleba.area_total_ha
                if divergencia <= TOLERANCIA_AREA:
                    evidencias.append(f"área compatível ({area_lead:.0f} ha × {gleba.area_total_ha:.0f} ha)")
            proprietario = _norm(gleba.proprietario)
            if tokens_lead and proprietario and any(t in proprietario for t in tokens_lead):
                evidencias.append("nome do proprietário bate com o do lead")

            if not evidencias:
                continue

            sugestoes.append(
                VinculoTerritorial(
                    lead_id=lead.id,
                    lead_nome=lead.nome,
                    gleba_id=gleba.id,
                    gleba_nome=gleba.nome,
                    municipio=gleba.municipio,
                    uf=gleba.uf,
                    area_lead_ha=area_lead,
                    area_gleba_ha=gleba.area_total_ha,
                    status_dominial=gleba.status_dominial,
                    origem="sugerido",
                    evidencia="Mesmo município; " + " e ".join(evidencias),
                    divergencia_area=(
                        abs(area_lead - gleba.area_total_ha) / gleba.area_total_ha
                        if area_lead else None
                    ),
                )
            )
    return sugestoes


# ---------------------------------------------------------------------------
# Totais
# ---------------------------------------------------------------------------

def contar_oportunidades(base: BaseComercial, hoje: Optional[date] = None) -> TotalOportunidades:
    """Total de oportunidades, nos três recortes que a Zion usa."""
    por_estagio: Dict[str, int] = defaultdict(int)
    por_perfil: Dict[str, int] = defaultdict(int)
    abertas = com_oferta = quentes = territoriais = ganhas = perdidas = 0

    for lead in base.leads:
        por_estagio[lead.estagio.value] += 1
        aberto = lead.estagio in ESTAGIOS_ABERTOS
        if aberto:
            abertas += 1
            por_perfil[lead.perfil.value] += 1
            if lead.estagio in ESTAGIOS_COM_OFERTA:
                com_oferta += 1
            if area_declarada(lead) or lead.ativos.terreno == Tri.SIM:
                territoriais += 1
        elif lead.estagio == Estagio.GANHO:
            ganhas += 1
        elif lead.estagio == Estagio.PERDIDO:
            perdidas += 1

        score, _ = qualificar(lead, hoje)
        if aberto and score.temperatura == Temperatura.OPORTUNIDADE:
            quentes += 1

    return TotalOportunidades(
        abertas=abertas,
        com_oferta_na_mesa=com_oferta,
        sinalizadas_quentes=quentes,
        territoriais=territoriais,
        ganhas=ganhas,
        perdidas=perdidas,
        total_base=len(base.leads),
        por_estagio=dict(sorted(por_estagio.items())),
        por_perfil=dict(sorted(por_perfil.items())),
    )


def somar_investimentos(base: BaseComercial) -> TotalInvestimentos:
    """Soma o investimento declarado pela base, com a cobertura à vista."""
    por_perfil: Dict[str, float] = defaultdict(float)
    total = aberto = ganho = perdido = 0.0
    declarantes = 0
    maior = 0.0
    maior_nome: Optional[str] = None

    for lead in base.leads:
        valor = investimento_declarado(lead)
        if valor is None:
            continue
        declarantes += 1
        total += valor
        por_perfil[lead.perfil.value] += valor
        if lead.estagio in ESTAGIOS_ABERTOS:
            aberto += valor
        elif lead.estagio == Estagio.GANHO:
            ganho += valor
        elif lead.estagio == Estagio.PERDIDO:
            perdido += valor
        if valor > maior:
            maior, maior_nome = valor, lead.nome

    n = len(base.leads)
    return TotalInvestimentos(
        declarado_brl=total,
        declarado_aberto_brl=aberto,
        declarado_ganho_brl=ganho,
        declarado_perdido_brl=perdido,
        leads_declarantes=declarantes,
        leads_sem_declaracao=n - declarantes,
        cobertura=(declarantes / n) if n else 0.0,
        ticket_medio_brl=(total / declarantes) if declarantes else 0.0,
        maior_declaracao_brl=maior,
        maior_declarante=maior_nome,
        por_perfil=dict(sorted(por_perfil.items())),
        pipeline_zion_brl=sum(
            l.valor_potencial_brl or 0.0 for l in base.leads if l.estagio in ESTAGIOS_ABERTOS
        ),
    )


def somar_areas(
    base: BaseComercial, land_bank: Optional[LandBank], vinculos: List[VinculoTerritorial]
) -> TotalAreas:
    """
    Consolida hectares das duas bases descontando a sobreposição.

    Quando um lead está vinculado a uma gleba, o hectare já está no banco: ele
    entra no total pelo registro do Land Bank, que é o dado auditável, e a
    declaração do lead é registrada como sobreposição — não somada.
    """
    glebas = land_bank.glebas if land_bank else []
    por_status: Dict[str, float] = defaultdict(float)
    por_uf: Dict[str, Dict[str, float]] = defaultdict(lambda: {"land_bank_ha": 0.0, "originacao_ha": 0.0})

    land_bank_ha = 0.0
    for g in glebas:
        land_bank_ha += g.area_total_ha
        por_status[g.status_dominial.value] += g.area_total_ha
        por_uf[g.uf.upper()]["land_bank_ha"] += g.area_total_ha

    leads_vinculados = {v.lead_id for v in vinculos if v.origem == "declarado"}
    sobreposicao = sum(
        v.area_lead_ha for v in vinculos if v.origem == "declarado" and v.area_lead_ha
    )

    originacao_aberta = originacao_fechada = 0.0
    com_area = terreno_sem_area = 0
    for lead in base.leads:
        area = area_declarada(lead)
        if area is None:
            if lead.ativos.terreno == Tri.SIM:
                terreno_sem_area += 1
            continue
        com_area += 1
        if lead.id in leads_vinculados:
            continue  # já está no banco; contado uma vez só, pelo Land Bank
        if lead.estagio in ESTAGIOS_ABERTOS:
            originacao_aberta += area
            if lead.estado:
                por_uf[lead.estado.upper()]["originacao_ha"] += area
        else:
            originacao_fechada += area

    n = len(base.leads)
    return TotalAreas(
        land_bank_ha=land_bank_ha,
        land_bank_glebas=len(glebas),
        por_status_ha=dict(sorted(por_status.items())),
        sob_controle_ha=(
            por_status.get(StatusDominial.PROPRIO.value, 0.0)
            + por_status.get(StatusDominial.CONTRATADO.value, 0.0)
        ),
        originacao_aberta_ha=originacao_aberta,
        originacao_fechada_ha=originacao_fechada,
        sobreposicao_ha=sobreposicao,
        total_consolidado_ha=land_bank_ha + originacao_aberta,
        leads_com_area=com_area,
        leads_terreno_sem_area=terreno_sem_area,
        cobertura_area=(com_area / n) if n else 0.0,
        por_uf_ha={k: v for k, v in sorted(por_uf.items())},
    )


def listar_originacao(
    base: BaseComercial, vinculados: set, hoje: Optional[date] = None
) -> List[OportunidadeTerritorial]:
    """
    Terra que está no CRM e ainda não entrou no banco de áreas.

    Ordenado por hectare, porque hectare é o que falta para um projeto agrupado
    fechar escala. O score vem junto para mostrar quais desses hectares são
    trabalháveis hoje — área grande em lead frio não é ativo, é lista.
    """
    itens: List[OportunidadeTerritorial] = []
    for lead in base.leads:
        if lead.id in vinculados or lead.estagio not in ESTAGIOS_ABERTOS:
            continue
        area = area_declarada(lead)
        if area is None:
            continue
        score, _ = qualificar(lead, hoje)
        observacao = ""
        if lead.terreno.documentacao_regular == Tri.NAO:
            observacao = "Documentação irregular declarada — resolver antes de qualquer instrumento"
        elif lead.terreno.documentacao_regular == Tri.DESCONHECIDO:
            observacao = "Situação documental desconhecida — perguntar antes de prometer prazo"
        itens.append(
            OportunidadeTerritorial(
                lead_id=lead.id,
                nome=lead.nome,
                municipio=lead.cidade,
                uf=lead.estado,
                area_ha=area,
                estagio=lead.estagio,
                temperatura=score.temperatura,
                score=score.score,
                confianca=score.confianca,
                investimento_declarado_brl=investimento_declarado(lead),
                documentacao_regular=lead.terreno.documentacao_regular,
                responsavel=lead.responsavel,
                observacao=observacao,
            )
        )
    itens.sort(key=lambda i: (i.area_ha, i.score), reverse=True)
    return itens


# ---------------------------------------------------------------------------
# Consolidação
# ---------------------------------------------------------------------------

def _alertas(
    base: BaseComercial,
    land_bank: Optional[LandBank],
    vinculos: List[VinculoTerritorial],
    sugestoes: List[VinculoTerritorial],
    areas: TotalAreas,
    investimentos: TotalInvestimentos,
    orfaos: List[Tuple[str, str]],
) -> List[str]:
    alertas: List[str] = []

    for lead_id, gleba_id in orfaos:
        alertas.append(
            f"Lead {lead_id} aponta para a gleba '{gleba_id}', que não existe no Land Bank "
            f"carregado. Vínculo ignorado no total de áreas."
        )

    for v in vinculos:
        if v.divergencia_area and v.divergencia_area > TOLERANCIA_AREA:
            alertas.append(
                f"{v.lead_nome} declara {v.area_lead_ha:.0f} ha e a gleba {v.gleba_id} está "
                f"registrada com {v.area_gleba_ha:.0f} ha "
                f"({v.divergencia_area:.0%} de diferença). Conferir antes de usar em proposta."
            )

    for s in sugestoes:
        alertas.append(
            f"Possível vínculo não registrado: {s.lead_nome} ({s.lead_id}) × gleba {s.gleba_id}. "
            f"{s.evidencia}. Confirmar — sem vínculo, a área pode estar contada duas vezes."
        )

    if areas.leads_terreno_sem_area:
        alertas.append(
            f"{areas.leads_terreno_sem_area} lead(s) declaram ter terreno sem informar a área. "
            f"São hectares invisíveis no banco de áreas."
        )

    if investimentos.cobertura < 0.5:
        alertas.append(
            f"Só {investimentos.cobertura:.0%} da base declarou investimento. O total declarado "
            f"é um piso, não uma medida do apetite da base."
        )

    if land_bank:
        minima = land_bank.premissas.area_minima_cluster_ha
        for uf, dados in areas.por_uf_ha.items():
            no_banco = dados["land_bank_ha"]
            em_originacao = dados["originacao_ha"]
            if no_banco and no_banco < minima and em_originacao:
                falta = minima - no_banco
                if em_originacao >= falta:
                    alertas.append(
                        f"{uf}: o banco tem {no_banco:,.0f} ha, abaixo da escala mínima de "
                        f"{minima:,.0f} ha — e existem {em_originacao:,.0f} ha em originação no CRM, "
                        f"suficientes para fechar a escala."
                    )

    sem_dono = []
    if land_bank:
        com_lead = {v.gleba_id for v in vinculos}
        for g in land_bank.glebas:
            if g.status_dominial == StatusDominial.EM_NEGOCIACAO and g.id not in com_lead:
                sem_dono.append(g.id)
    if sem_dono:
        alertas.append(
            f"{len(sem_dono)} gleba(s) em negociação sem lead correspondente no CRM "
            f"({', '.join(sem_dono)}). Negociação sem dono no CRM é negociação sem follow-up."
        )

    return alertas


def consolidar_territorio(
    base: BaseComercial,
    land_bank: Optional[LandBank] = None,
    hoje: Optional[date] = None,
) -> PainelTerritorial:
    """
    ATRELAR LAND BANK AO CRM — painel único de oportunidades, investimento
    declarado e hectares no banco de áreas.
    """
    hoje = hoje or base.data_referencia or date.today()
    indice = _indice_glebas(land_bank)

    vinculos: List[VinculoTerritorial] = []
    orfaos: List[Tuple[str, str]] = []
    for lead in base.leads:
        for gleba_id in lead.glebas_land_bank:
            gleba = indice.get(gleba_id)
            if gleba is None:
                orfaos.append((lead.id, gleba_id))
                continue
            vinculos.append(_vinculo_declarado(lead, gleba))

    sugestoes = (
        sugerir_vinculos(base, land_bank, {v.gleba_id for v in vinculos}) if land_bank else []
    )

    oportunidades = contar_oportunidades(base, hoje)
    investimentos = somar_investimentos(base)
    areas = somar_areas(base, land_bank, vinculos)
    originacao = listar_originacao(base, {v.lead_id for v in vinculos}, hoje)

    return PainelTerritorial(
        data=hoje.strftime("%d/%m/%Y"),
        land_bank_nome=land_bank.nome if land_bank else None,
        base_nome=base.nome,
        oportunidades=oportunidades,
        investimentos=investimentos,
        areas=areas,
        vinculos=vinculos,
        sugestoes_vinculo=sugestoes,
        originacao=originacao,
        alertas=_alertas(base, land_bank, vinculos, sugestoes, areas, investimentos, orfaos),
    )

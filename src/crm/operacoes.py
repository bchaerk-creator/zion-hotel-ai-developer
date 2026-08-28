"""
Operações do ZION CRM & LEAD INTELLIGENCE™.

Higiene da base, análise de funil, lista de reativação e relatório comercial.
Tudo determinístico: são contagens e regras, não opinião.
"""

from collections import Counter, defaultdict
from datetime import date
from typing import Dict, List, Optional

from src.crm.engine import qualificar
from src.crm.models import (
    AchadoHigiene,
    AnaliseFunil,
    BaseComercial,
    Estagio,
    EtapaFunil,
    ItemReativacao,
    Lead,
    LeadQualificado,
    Perfil,
    Porta,
    RelatorioComercial,
    Temperatura,
    Tri,
)

ESTAGIOS_ABERTOS = [
    Estagio.NOVO_LEAD, Estagio.CONTATO_INICIADO, Estagio.QUALIFICACAO,
    Estagio.DIAGNOSTICO, Estagio.REUNIAO, Estagio.OFERTA,
    Estagio.NEGOCIACAO, Estagio.DECISAO,
]

DIAS_PARADO = 30
DIAS_ABANDONADO = 90


def _dias(desde: Optional[date], hoje: date) -> Optional[int]:
    return (hoje - desde).days if desde else None


# ---------------------------------------------------------------------------
# Higiene
# ---------------------------------------------------------------------------

def auditar_base(base: BaseComercial, hoje: Optional[date] = None) -> List[AchadoHigiene]:
    """LIMPAR CRM — encontra inconsistências que travam a operação comercial."""
    hoje = hoje or base.data_referencia or date.today()
    achados: List[AchadoHigiene] = []

    def add(codigo, gravidade, tema, descricao, leads, acao):
        if leads:
            achados.append(AchadoHigiene(
                codigo=codigo, gravidade=gravidade, tema=tema,
                descricao=descricao, leads=leads, acao=acao,
            ))

    # Duplicidade por e-mail, telefone ou nome normalizado.
    chaves: Dict[str, List[str]] = defaultdict(list)
    for lead in base.leads:
        for chave in filter(None, [
            (lead.email or "").strip().lower() or None,
            "".join(filter(str.isdigit, lead.telefone or "")) or None,
            lead.nome.strip().lower(),
        ]):
            chaves[chave].append(lead.id)
    duplicados = sorted({
        f"{ids[0]} ≈ {', '.join(ids[1:])}" for ids in chaves.values() if len(ids) > 1
    })
    add("CRM_DUPLICADO", "alta", "Contatos duplicados",
        "Mesmo e-mail, telefone ou nome em mais de um registro.",
        duplicados, "Mesclar os registros preservando o histórico mais completo.")

    add("CRM_SEM_CONTATO", "bloqueante", "Lead sem canal de contato",
        "Sem e-mail e sem telefone não existe operação comercial possível.",
        [l.id for l in base.leads if not l.email and not l.telefone],
        "Buscar o canal de contato ou arquivar o registro.")

    add("CRM_EMAIL_INVALIDO", "media", "E-mail com formato inválido",
        "Endereço sem estrutura de e-mail válida.",
        [l.id for l in base.leads if l.email and ("@" not in l.email or "." not in l.email.split("@")[-1])],
        "Corrigir ou remover o e-mail.")

    add("CRM_SEM_PERFIL", "alta", "Lead sem perfil classificado",
        "Sem perfil não há roteamento de oferta possível.",
        [l.id for l in base.leads if l.perfil == Perfil.NAO_CLASSIFICADO],
        "Aplicar o roteiro de qualificação e classificar o perfil.")

    abertos = [l for l in base.leads if l.estagio in ESTAGIOS_ABERTOS]

    add("CRM_SEM_PROXIMA_ACAO", "bloqueante", "Lead aberto sem próxima ação",
        "'Aguardando retorno' não é gestão. Todo lead aberto precisa de próxima ação com data.",
        [l.id for l in abertos if l.proxima_acao is None],
        "Definir ação, data e responsável para cada lead aberto.")

    add("CRM_FOLLOWUP_ATRASADO", "alta", "Follow-up vencido",
        "A data prevista da próxima ação já passou.",
        [l.id for l in abertos if l.proxima_acao and l.proxima_acao.data_prevista < hoje],
        "Executar o follow-up ou reagendar com novo critério.")

    add("CRM_PARADO", "alta", "Lead aberto sem atividade",
        f"Sem qualquer atividade há mais de {DIAS_PARADO} dias.",
        [l.id for l in abertos
         if (d := _dias(l.data_ultima_atividade, hoje)) is not None and d > DIAS_PARADO],
        "Retomar contato ou mover para requalificação — nunca perder em silêncio.")

    add("CRM_SEM_RESPONSAVEL", "alta", "Negócio sem responsável",
        "Oportunidade em andamento sem dono não avança.",
        [l.id for l in abertos if not l.responsavel],
        "Atribuir responsável a cada oportunidade aberta.")

    add("CRM_SEM_VALOR", "media", "Oportunidade sem valor potencial",
        "Sem valor não há pipeline mensurável nem priorização possível.",
        [l.id for l in base.leads
         if l.estagio in (Estagio.OFERTA, Estagio.NEGOCIACAO, Estagio.DECISAO)
         and l.valor_potencial_brl is None],
        "Estimar o valor potencial de cada oportunidade.")

    add("CRM_PERDA_SEM_MOTIVO", "bloqueante", "Perda sem motivo registrado",
        "'Perdido' sem explicação destrói a capacidade de aprender com o funil.",
        [l.id for l in base.leads if l.estagio == Estagio.PERDIDO and l.motivo_perda is None],
        "Registrar o motivo da perda em cada oportunidade encerrada.")

    ordem = {"bloqueante": 0, "alta": 1, "media": 2}
    achados.sort(key=lambda a: ordem.get(a.gravidade, 9))
    return achados


# ---------------------------------------------------------------------------
# Funil
# ---------------------------------------------------------------------------

def analisar_funil(base: BaseComercial) -> AnaliseFunil:
    """
    ANALISAR CONVERSÃO — onde os leads estão parando.

    O gargalo é a maior queda percentual entre etapas consecutivas. Se a queda
    grande está no topo, o problema é qualificação; se está no fim, é oferta.
    """
    contagem = Counter(l.estagio for l in base.leads)
    valor_por_estagio: Dict[Estagio, float] = defaultdict(float)
    for lead in base.leads:
        valor_por_estagio[lead.estagio] += lead.valor_potencial_brl or 0.0

    sequencia = ESTAGIOS_ABERTOS + [Estagio.GANHO]

    # Volume acumulado: quem chegou ao estágio 5 já passou pelo 4.
    acumulado: Dict[Estagio, int] = {}
    for i, estagio in enumerate(sequencia):
        acumulado[estagio] = sum(contagem[e] for e in sequencia[i:])

    etapas: List[EtapaFunil] = []
    anterior: Optional[int] = None
    quedas: List[tuple] = []

    for estagio in sequencia:
        volume = acumulado[estagio]
        conversao = None
        if anterior is not None and anterior > 0:
            conversao = round(volume / anterior, 4)
            if anterior >= 3:
                quedas.append((1 - conversao, estagio, anterior, volume))
        etapas.append(EtapaFunil(
            estagio=estagio, quantidade=volume,
            valor_potencial_brl=round(valor_por_estagio[estagio], 2),
            conversao_da_anterior=conversao,
        ))
        anterior = volume

    gargalo = None
    diagnostico = "Volume insuficiente para diagnosticar o funil com segurança."
    if quedas:
        queda, estagio, de, para = max(quedas, key=lambda q: q[0])
        gargalo = estagio.value
        posicao = sequencia.index(estagio)
        if posicao <= 2:
            causa = (
                "A queda está no topo: o problema é qualificação, não venda. "
                "Entram leads que não deveriam entrar, ou entram sem informação."
            )
        elif posicao <= 4:
            causa = (
                "A queda está no meio: o problema é diagnóstico. O lead chega à conversa "
                "mas não enxerga valor suficiente para avançar."
            )
        else:
            causa = (
                "A queda está no fim: o problema é oferta ou preço. O lead entende o valor "
                "mas não fecha."
            )
        diagnostico = (
            f"Maior queda em {estagio.value}: de {de} para {para} "
            f"({queda * 100:.0f}% de perda). {causa}"
        )

    ganhos = contagem[Estagio.GANHO]
    perdidos = contagem[Estagio.PERDIDO]
    total = len(base.leads)
    pipeline = sum(
        l.valor_potencial_brl or 0.0 for l in base.leads if l.estagio in ESTAGIOS_ABERTOS
    )
    motivos = Counter(
        l.motivo_perda.value for l in base.leads
        if l.estagio == Estagio.PERDIDO and l.motivo_perda
    )

    return AnaliseFunil(
        etapas=etapas, gargalo=gargalo, diagnostico=diagnostico,
        total_leads=total, pipeline_aberto_brl=round(pipeline, 2),
        ganhos=ganhos, perdidos=perdidos,
        taxa_conversao_total=round(ganhos / total, 4) if total else None,
        motivos_perda=dict(motivos),
    )


# ---------------------------------------------------------------------------
# Reativação
# ---------------------------------------------------------------------------

def listar_reativacao(
    base: BaseComercial, hoje: Optional[date] = None, score_minimo: float = 5.0
) -> List[ItemReativacao]:
    """
    ZION REACTIVATION LIST™ — leads antigos com fit que merecem nova abordagem.

    Silêncio não é desinteresse: pode ser mensagem errada, canal errado, oferta
    errada ou timing. Antes de perder, requalificar.
    """
    hoje = hoje or base.data_referencia or date.today()
    itens: List[ItemReativacao] = []

    for lead in base.leads:
        if lead.estagio in (Estagio.GANHO,):
            continue
        dias = _dias(lead.data_ultima_atividade, hoje)
        parado = dias is not None and dias > DIAS_PARADO
        perdido_recuperavel = lead.estagio == Estagio.PERDIDO and (
            lead.motivo_perda is None
            or lead.motivo_perda.value in ("timing", "adiou", "nao_respondeu", "sem_decisao")
        )
        if not (parado or perdido_recuperavel):
            continue

        score, roteamento = qualificar(lead, hoje)
        if score.score < score_minimo:
            continue

        if lead.estagio == Estagio.PERDIDO:
            if lead.motivo_perda:
                problema = (
                    f"Perdido por {lead.motivo_perda.value.replace('_', ' ')} — "
                    f"a condição pode ter mudado."
                )
            else:
                problema = (
                    "Perdido sem motivo registrado — não se sabe por que saiu, "
                    "então não há razão para não voltar."
                )
        elif dias and dias > DIAS_ABANDONADO:
            problema = f"Sem contato há {dias} dias. Provável oferta ou canal errado na última tentativa."
        else:
            problema = f"Parado há {dias} dias no estágio {lead.estagio.value}."

        ativos = ", ".join(lead.ativos.possui()) or "ativos não levantados"
        itens.append(ItemReativacao(
            lead_id=lead.id, nome=lead.nome,
            contexto=f"{lead.perfil.value}, {ativos}. Estágio: {lead.estagio.value}.",
            ultima_interacao=lead.data_ultima_atividade, dias_parado=dias,
            score=score.score, porta_potencial=roteamento.porta,
            provavel_problema=problema,
            abordagem_recomendada=roteamento.proximo_passo_logico,
        ))

    itens.sort(key=lambda i: i.score, reverse=True)
    return itens


# ---------------------------------------------------------------------------
# Relatório consolidado
# ---------------------------------------------------------------------------

def analisar_base(base: BaseComercial, hoje: Optional[date] = None) -> RelatorioComercial:
    """ANALISAR CRM — qualificação, priorização, higiene, funil e reativação."""
    hoje = hoje or base.data_referencia or date.today()

    qualificados: List[LeadQualificado] = []
    for lead in base.leads:
        score, roteamento = qualificar(lead, hoje)
        qualificados.append(LeadQualificado(lead=lead, score=score, roteamento=roteamento))

    # Prioridade: oportunidade e temperatura acima de tudo, score como desempate.
    peso_temp = {
        Temperatura.OPORTUNIDADE: 3, Temperatura.QUENTE: 2,
        Temperatura.MORNO: 1, Temperatura.FRIO: 0,
    }
    # Lead fechado não disputa atenção com lead aberto: ganho e perdido vão para
    # o fim da fila. Continuam listados — servem à ascensão e à reativação — mas
    # a fila de trabalho é dos abertos.
    qualificados.sort(
        key=lambda q: (
            1 if q.lead.estagio in ESTAGIOS_ABERTOS else 0,
            peso_temp[q.score.temperatura],
            q.score.score,
            q.score.confianca,
        ),
        reverse=True,
    )
    for i, q in enumerate(qualificados, start=1):
        q.prioridade = i

    higiene = auditar_base(base, hoje)
    funil = analisar_funil(base)
    reativacao = listar_reativacao(base, hoje)

    abertos = [q for q in qualificados if q.lead.estagio in ESTAGIOS_ABERTOS]
    parados = [
        q for q in abertos
        if (d := _dias(q.lead.data_ultima_atividade, hoje)) is not None and d > DIAS_PARADO
    ]
    atrasados = [
        q for q in abertos
        if q.lead.proxima_acao and q.lead.proxima_acao.data_prevista < hoje
    ]

    return RelatorioComercial(
        data=hoje.strftime("%d/%m/%Y"),
        total_leads=len(base.leads),
        novos=sum(1 for q in qualificados if q.lead.estagio == Estagio.NOVO_LEAD),
        quentes=sum(1 for q in qualificados if q.score.temperatura == Temperatura.QUENTE),
        oportunidades=sum(
            1 for q in qualificados if q.score.temperatura == Temperatura.OPORTUNIDADE
        ),
        parados=len(parados),
        followups_atrasados=len(atrasados),
        pipeline_aberto_brl=funil.pipeline_aberto_brl,
        qualificados=qualificados,
        funil=funil,
        higiene=higiene,
        reativacao=reativacao,
        acoes_recomendadas=_acoes(qualificados, higiene, funil, reativacao, atrasados, parados),
    )


def _acoes(qualificados, higiene, funil, reativacao, atrasados, parados) -> List[str]:
    """De 3 a 5 ações prioritárias, na ordem em que movem o resultado."""
    acoes: List[str] = []

    oportunidades = [q for q in qualificados if q.score.temperatura == Temperatura.OPORTUNIDADE]
    if oportunidades:
        nomes = ", ".join(q.lead.nome for q in oportunidades[:3])
        acoes.append(f"Trabalhar hoje as oportunidades abertas: {nomes}.")

    if atrasados:
        acoes.append(
            f"Executar {len(atrasados)} follow-up(s) vencido(s) — são compromissos já assumidos."
        )

    bloqueantes = [a for a in higiene if a.gravidade == "bloqueante"]
    if bloqueantes:
        acoes.append(
            f"Resolver {len(bloqueantes)} problema(s) bloqueante(s) de higiene: "
            + "; ".join(a.tema for a in bloqueantes[:3]) + "."
        )

    if funil.gargalo:
        acoes.append(f"Atacar o gargalo do funil. {funil.diagnostico}")

    baixa_confianca = [q for q in qualificados if q.score.confianca < 0.5]
    if baixa_confianca:
        acoes.append(
            f"Qualificar {len(baixa_confianca)} lead(s) com informação insuficiente — "
            f"não descartar, levantar dado. Score baixo por falta de informação não é lead ruim."
        )

    if reativacao:
        acoes.append(
            f"Rodar a lista de reativação: {len(reativacao)} lead(s) parados com fit acima da linha."
        )

    return acoes[:5]

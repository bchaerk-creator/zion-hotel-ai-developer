"""
AUDITAR MÉTODO — verificação de integridade do Zion Knowledge Engine™.

Procura o que está faltando, o que está em conflito e o que está sendo
afirmado sem fonte. A auditoria não conserta nada: ela expõe, para que a
decisão seja de quem tem autoridade sobre o método.
"""

from typing import Dict, List

from pydantic import BaseModel, Field

from src.knowledge.base import PERGUNTA_DO_PILAR, SEQUENCIA_PILARES, KnowledgeBase
from src.knowledge.models import Status


class Achado(BaseModel):
    """Uma inconsistência encontrada na auditoria."""
    codigo: str
    gravidade: str = Field(..., description="bloqueante, alta, media")
    tema: str
    descricao: str
    itens: List[str] = Field(default_factory=list)
    acao: str


class ResultadoAuditoria(BaseModel):
    total_itens: int
    achados: List[Achado]
    resumo_bancos: Dict[str, int]
    cobertura_por_pilar: Dict[str, int]
    matriz: List[Dict[str, str]]

    @property
    def bloqueantes(self) -> List[Achado]:
        return [a for a in self.achados if a.gravidade == "bloqueante"]


def auditar(kb: KnowledgeBase) -> ResultadoAuditoria:
    """Roda todas as verificações sobre a base de conhecimento."""
    achados: List[Achado] = []

    # 1. Divergências não resolvidas — a regra de não escolher em silêncio.
    pendentes = [d for d in kb.divergencias.values() if d.resolucao is None]
    if pendentes:
        achados.append(Achado(
            codigo="AUD_DIVERGENCIA",
            gravidade="bloqueante",
            tema="Divergência entre fontes oficiais sem resolução",
            descricao=(
                "Existem versões conflitantes do método em fontes oficiais. Nenhuma pode "
                "ser adotada em silêncio — a escolha é do fundador."
            ),
            itens=[f"{d.id}: {d.tema}" for d in pendentes],
            acao="Definir qual versão é oficial e registrar a resolução na divergência.",
        ))

    # 2. Ferramentas proprietárias sem definição documentada.
    sem_fonte = [
        f for f in kb.ferramentas.values() if f.status == Status.PENDENTE_DE_FONTE
    ]
    if sem_fonte:
        achados.append(Achado(
            codigo="AUD_FERRAMENTA_SEM_FONTE",
            gravidade="bloqueante",
            tema="Ferramenta com nome preservado e conteúdo ausente",
            descricao=(
                "O nome e a posição na metodologia estão registrados, mas a definição não "
                "está no sistema. Não podem ser usadas em aula, ebook ou material comercial."
            ),
            itens=[f"{f.id}: {f.nome}" for f in sem_fonte],
            acao="Carregar a documentação de origem de cada ferramenta.",
        ))

    # 3. Números sem período de apuração.
    sem_periodo = [
        n for n in kb.numeros.values() if n.periodo.startswith("Período não informado")
    ]
    if sem_periodo:
        achados.append(Achado(
            codigo="AUD_NUMERO_SEM_PERIODO",
            gravidade="alta",
            tema="Indicador sem período de apuração",
            descricao=(
                "Número sem período e sem demonstrativo de origem não pode ser citado "
                "externamente nem usado para calibrar estimativa auditável."
            ),
            itens=[f"{n.id}: {n.indicador} = {n.valor:g} {n.unidade}" for n in sem_periodo],
            acao="Informar período de apuração e a fonte contábil de cada indicador.",
        ))

    # 4. Pilares sem instrumentação.
    for pilar in SEQUENCIA_PILARES:
        faltas = []
        if not any(f.pilar == pilar for f in kb.ferramentas.values()):
            faltas.append("ferramenta")
        if not any(e.pilar == pilar for e in kb.entregaveis.values()):
            faltas.append("entregável")
        if not any(d.pilar == pilar for d in kb.decisoes.values()):
            faltas.append("decisão")
        if faltas:
            achados.append(Achado(
                codigo=f"AUD_PILAR_INCOMPLETO_{pilar.name}",
                gravidade="alta",
                tema=f"Pilar {pilar.value} sem instrumentação completa",
                descricao=(
                    f"'{PERGUNTA_DO_PILAR[pilar]}' é a pergunta do pilar, mas falta "
                    f"{', '.join(faltas)} para respondê-la de forma replicável."
                ),
                itens=faltas,
                acao=f"Documentar o que falta no pilar {pilar.value}.",
            ))

    # 5. Ferramentas que não desembocam em entregável.
    orfas = [f for f in kb.ferramentas.values() if not f.entregavel_id]
    if orfas:
        achados.append(Achado(
            codigo="AUD_FERRAMENTA_SEM_ENTREGAVEL",
            gravidade="media",
            tema="Ferramenta sem entregável associado",
            descricao="Ferramenta que não produz entregável não fecha o ciclo da metodologia.",
            itens=[f"{f.id}: {f.nome}" for f in orfas],
            acao="Associar cada ferramenta ao entregável que ela produz.",
        ))

    # 6. Decisões sem ferramenta que as sustente.
    sem_ferramenta = [d for d in kb.decisoes.values() if not d.ferramenta_id]
    if sem_ferramenta:
        achados.append(Achado(
            codigo="AUD_DECISAO_SEM_FERRAMENTA",
            gravidade="alta",
            tema="Decisão sem ferramenta de apoio",
            descricao=(
                "Decisão que o developer precisa tomar sem instrumento Zion que a sustente "
                "é decisão tomada por intuição."
            ),
            itens=[f"{d.id}: {d.pergunta}" for d in sem_ferramenta],
            acao="Definir ou documentar a ferramenta que sustenta cada decisão.",
        ))

    # 7. Ausência de prova.
    com_resultado = [
        c for c in kb.cases.values() if not c.resultado.startswith("Resultado não documentado")
    ]
    if not com_resultado:
        achados.append(Achado(
            codigo="AUD_SEM_CASE",
            gravidade="bloqueante",
            tema="Nenhum case com resultado documentado",
            descricao=(
                "Sem case documentado, o sistema não pode fornecer prova para narrativa, "
                "oferta ou material de captação. Qualquer prova afirmada seria invenção."
            ),
            itens=[],
            acao="Documentar ao menos um case completo: contexto, decisão, execução e resultado.",
        ))

    # 8. Lacunas de fonte primária.
    if kb.lacunas:
        achados.append(Achado(
            codigo="AUD_LACUNAS",
            gravidade="bloqueante",
            tema="Fontes primárias ausentes no sistema",
            descricao=(
                "O Knowledge Engine se declara fonte de verdade do método, mas os materiais "
                "que contêm esse método não estão carregados."
            ),
            itens=[f"{l.id}: {l.item}" for l in kb.lacunas.values()],
            acao="Carregar os materiais listados para que a base deixe de ser esqueleto.",
        ))

    ordem = {"bloqueante": 0, "alta": 1, "media": 2}
    achados.sort(key=lambda a: ordem.get(a.gravidade, 9))

    return ResultadoAuditoria(
        total_itens=sum(kb.resumo().values()),
        achados=achados,
        resumo_bancos=kb.resumo(),
        cobertura_por_pilar=kb.cobertura_por_pilar(),
        matriz=kb.matriz_conhecimento_decisao(),
    )


def relatorio_auditoria(resultado: ResultadoAuditoria) -> str:
    """Renderiza a auditoria em Markdown."""
    linhas = [
        "# Auditoria do Método Zion",
        "",
        f"**Itens registrados:** {resultado.total_itens}  ",
        f"**Achados:** {len(resultado.achados)} "
        f"({len(resultado.bloqueantes)} bloqueantes)",
        "",
        "## Matriz Conhecimento → Decisão",
        "",
        "| Pilar | Pergunta | Ferramenta | Entregável | Completa |",
        "|---|---|---|---|---|",
    ]
    for linha in resultado.matriz:
        linhas.append(
            f"| {linha['pilar']} | {linha['pergunta']} | {linha['ferramenta']} | "
            f"{linha['entregavel']} | {linha['completa']} |"
        )

    linhas += ["", "## Achados", ""]
    for a in resultado.achados:
        linhas.append(f"### [{a.gravidade.upper()}] {a.tema}")
        linhas.append("")
        linhas.append(a.descricao)
        linhas.append("")
        for item in a.itens:
            linhas.append(f"- {item}")
        if a.itens:
            linhas.append("")
        linhas.append(f"**Ação:** {a.acao}")
        linhas.append("")

    return "\n".join(linhas)

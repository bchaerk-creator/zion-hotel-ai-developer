"""
População inicial do Zion Knowledge Engine™.

REGRA QUE GOVERNA ESTE ARQUIVO: só entra o que é verificável.

Verificável aqui significa uma de duas coisas — está implementado no código
deste repositório, ou foi declarado explicitamente pelo fundador em sessão
registrada. Os sete livros da Zion, o livro-mãe e os materiais da mentoria
NÃO estão carregados no sistema. Tudo que depende deles está registrado como
lacuna, não como conhecimento.

Ferramentas citadas sem definição disponível entram com nome e função
preservados e status PENDENTE_DE_FONTE. Nunca com definição inventada.
"""

from src.knowledge.base import KnowledgeBase
from src.knowledge.models import (
    Conceito,
    Decisao,
    Divergencia,
    Entregavel,
    Erro,
    Ferramenta,
    Fonte,
    Lacuna,
    Nivel,
    Pergunta,
    Pilar,
    Proveniencia,
    RegistroNumerico,
    Status,
)

# ---------------------------------------------------------------------------
# Fontes
# ---------------------------------------------------------------------------

F_REPO = Fonte(
    documento="Repositório zion-hotel-ai-developer",
    tipo="código",
    localizacao="src/prompts/base.py, src/config/",
    disponivel_no_sistema=True,
)
F_SPEC_KE = Fonte(
    documento="Spec ZION KNOWLEDGE ENGINE™",
    tipo="sessão",
    localizacao="Declaração do fundador em sessão",
    data="2026-08-28",
    disponivel_no_sistema=True,
)
F_SPEC_PILARES = Fonte(
    documento="Pilares Comerciais da Zion",
    tipo="sessão",
    localizacao="src/config/pilares.py",
    data="2026-08-28",
    disponivel_no_sistema=True,
)
F_LAND_BANK = Fonte(
    documento="Módulo Land Bank",
    tipo="código",
    localizacao="src/modules/carbon_engine.py, docs/LAND_BANK.md",
    data="2026-08-28",
    disponivel_no_sistema=True,
)
F_LIVROS = Fonte(
    documento="Os 7 livros da Zion",
    tipo="livro",
    disponivel_no_sistema=False,
)
F_LIVRO_MAE = Fonte(
    documento="Transforme Seu Terreno em um Destino Turístico",
    tipo="livro",
    disponivel_no_sistema=False,
)
F_MERCADO = Fonte(
    documento="Conhecimento geral de mercado de carbono",
    tipo="externo",
    disponivel_no_sistema=True,
)


# ---------------------------------------------------------------------------
# Conceitos
# ---------------------------------------------------------------------------

def _conceitos():
    return [
        Conceito(
            id="C_TERRITORIO_PRIMEIRO",
            nome="Comece pelo território",
            nivel=Nivel.PRINCIPIO,
            pilar=Pilar.TERRITORIO,
            fonte=F_SPEC_KE,
            definicao="Nunca comece pelo hotel. Comece pelo território.",
            problema_que_resolve=(
                "Developer que começa pela arquitetura constrói um produto que o "
                "território não sustenta e o mercado não pede."
            ),
            quando_utilizar="Antes de qualquer decisão de produto, projeto ou investimento.",
            perguntas=["O que este território sustenta?"],
            decisao_que_permite="Desenvolver ou não?",
            ferramentas_relacionadas=["FE_ZION_SCORE"],
            entregaveis_relacionados=["EN_DIAGNOSTICO_TERRITORIAL"],
        ),
        Conceito(
            id="C_VALIDAR_ANTES",
            nome="Validar antes de construir",
            nivel=Nivel.PRINCIPIO,
            pilar=Pilar.TRANSVERSAL,
            fonte=F_REPO,
            definicao="Sempre validar mercado e retorno antes de desenhar o produto.",
            problema_que_resolve="Capital imobilizado em produto que o mercado não valida.",
            decisao_que_permite="Seguir para a próxima etapa ou parar.",
        ),
        Conceito(
            id="C_ZION_360",
            nome="Método Zion 360°",
            nivel=Nivel.METODO,
            pilar=Pilar.TRANSVERSAL,
            fonte=F_SPEC_KE,
            definicao=(
                "Sistema de desenvolvimento de destinos turísticos organizado em sete "
                "pilares: Território, Mercado, Produto, Estratégia, Investimento, "
                "Implantação e Lançamento."
            ),
            problema_que_resolve=(
                "Desenvolvimento turístico tratado como soma de decisões isoladas, sem "
                "sequência lógica entre território, demanda, produto e capital."
            ),
            perguntas=[
                "O que este território sustenta?",
                "Existe demanda?",
                "O que devemos criar?",
                "Como transformar isso em negócio?",
                "Os números fecham?",
                "Como tirar do papel?",
                "Como colocar no mercado?",
            ],
            observacoes=(
                "Não simplificar para 'sete passos para ganhar dinheiro'. É um sistema de "
                "desenvolvimento de destinos, não uma fórmula."
            ),
        ),
        Conceito(
            id="C_PIRAMIDE_INVERTIDA",
            nome="Pirâmide Invertida©",
            nivel=Nivel.FRAMEWORK,
            pilar=Pilar.TRANSVERSAL,
            fonte=F_REPO,
            definicao=(
                "Framework de sete etapas sequenciais (0 a 6) implementado no Zion Hotel "
                "AI Developer: Diagnóstico Preliminar, Viabilidade Mercadológica, "
                "Viabilidade Econômico-Financeira, Produto e Master Plan, Estruturação do "
                "Negócio, Modelagem para Investidores, Acompanhamento de Implantação."
            ),
            problema_que_resolve="Falta de lastro técnico entre uma etapa e a seguinte.",
            ferramentas_relacionadas=["FE_ZION_SCORE", "FE_MODELO_FINANCEIRO"],
            observacoes=(
                "ATENÇÃO: divergência registrada em D_ORDEM_PRODUTO_INVESTIMENTO, "
                "D_LANCAMENTO_AUSENTE e D_NOME_INVESTIMENTO. Ver divergências antes de "
                "usar este framework junto com o Zion 360°."
            ),
        ),
        Conceito(
            id="C_LAND_BANK",
            nome="Land Bank",
            nivel=Nivel.FRAMEWORK,
            pilar=Pilar.TERRITORIO,
            fonte=F_LAND_BANK,
            definicao=(
                "Portfólio territorial agregado em clusters, tratado como máquina de "
                "atingir escala mínima por projeto agrupado de carbono, e não como lista "
                "de terrenos."
            ),
            problema_que_resolve=(
                "Gleba isolada não paga o custo fixo de um projeto de carbono."
            ),
            quando_utilizar="Quando há mais de uma gleba disponível na mesma região e bioma.",
            ferramentas_relacionadas=["FE_LAND_BANK"],
            decisao_que_permite="Qual terra agregar primeiro.",
        ),
        Conceito(
            id="C_DESCASAMENTO_CAIXA",
            nome="Descasamento de caixa em ciclo longo",
            nivel=Nivel.FRAMEWORK,
            pilar=Pilar.INVESTIMENTO,
            proveniencia=Proveniencia.INFERENCIA,
            fonte=F_LAND_BANK,
            definicao=(
                "Projetos de ciclo longo quebram pelo intervalo entre o desembolso e a "
                "primeira receita, não pela ausência de resultado nominal."
            ),
            problema_que_resolve="Projeto com resultado positivo no papel e caixa negativo na prática.",
            decisao_que_permite="Quando buscar adiantamento, e de quem.",
            observacoes=(
                "INFERÊNCIA estratégica derivada da modelagem do Land Bank e aplicada aos "
                "pilares comerciais. Não é metodologia Zion documentada."
            ),
        ),
    ]


# ---------------------------------------------------------------------------
# Ferramentas
# ---------------------------------------------------------------------------

def _ferramentas():
    return [
        Ferramenta(
            id="FE_ZION_SCORE",
            nome="Zion Score™",
            nivel=Nivel.FERRAMENTA,
            pilar=Pilar.TERRITORIO,
            fonte=F_REPO,
            objetivo="Atribuir nota de 0 a 10 ao potencial de um território para desenvolvimento hoteleiro.",
            problema_resolvido="Decidir se vale a pena investir tempo e dinheiro em um terreno.",
            entradas=["Localização", "Área", "Acessos", "Tipo de produto pretendido"],
            processo=[
                "Analisar vocação do destino",
                "Estimar ADR de referência",
                "Estimar CAPEX orientativo",
                "Mapear mercado emissor e concorrência",
                "Consolidar nota de 0 a 10",
            ],
            saida="Nota Zion Score™ com classificação e recomendação",
            interpretacao="8-10 excelente · 6-7,9 bom · 4-5,9 regular · 0-3,9 insuficiente",
            entregavel_id="EN_DIAGNOSTICO_TERRITORIAL",
            decisao_gerada="Desenvolver ou não?",
            modulo_sistema="src/agents/zion_score_agent.py",
        ),
        Ferramenta(
            id="FE_MODELO_FINANCEIRO",
            nome="Modelo financeiro Zion",
            nivel=Nivel.FERRAMENTA,
            pilar=Pilar.INVESTIMENTO,
            fonte=F_REPO,
            objetivo="Projetar CAPEX, receitas, EBITDA e indicadores de retorno do empreendimento.",
            entradas=["Produto definido", "ADR estimado", "Número de unidades", "CAPEX"],
            processo=["Projetar receita e despesa", "Calcular EBITDA", "Calcular TIR, VPL, payback"],
            saida="Estudo de viabilidade econômico-financeira com três cenários",
            entregavel_id="EN_VIABILIDADE",
            decisao_gerada="Quanto investir?",
            modulo_sistema="src/agents/financial_agent.py",
        ),
        Ferramenta(
            id="FE_LAND_BANK",
            nome="Engine de Carbono do Land Bank",
            nivel=Nivel.FERRAMENTA,
            pilar=Pilar.TERRITORIO,
            fonte=F_LAND_BANK,
            objetivo=(
                "Agregar glebas em clusters e dimensionar o potencial de crédito de "
                "carbono, com fluxo de caixa, preço de equilíbrio e fila de agregação."
            ),
            problema_resolvido="Saber qual terra perseguir primeiro e quanta área falta para fechar conta.",
            entradas=["Glebas com bioma, área, uso do solo, status dominial e coordenadas"],
            processo=[
                "Triagem de elegibilidade por talhão",
                "Clusterização por bioma e raio",
                "Estimativa de créditos com curva, buffer e incerteza",
                "Fluxo de caixa, VPL, TIR e preço de equilíbrio",
                "Priorização da fila de agregação",
            ],
            saida="Relatório do Land Bank com clusters, alavancas e prioridades",
            decisao_gerada="Qual terra agregar primeiro e por qual instrumento.",
            modulo_sistema="src/modules/carbon_engine.py",
        ),
        Ferramenta(
            id="FE_IPM_Z",
            nome="IPM-Z™",
            nivel=Nivel.FERRAMENTA,
            pilar=Pilar.MERCADO,
            status=Status.PENDENTE_DE_FONTE,
            fonte=F_SPEC_KE,
            objetivo="Ferramenta de análise de mercado citada na matriz Conhecimento → Decisão.",
            observacoes=(
                "Nome e posição na matriz preservados conforme declarado. Definição, "
                "entradas, processo e critérios de interpretação NÃO estão documentados no "
                "sistema. Não usar em aula, ebook ou material comercial até a fonte ser carregada."
            ),
        ),
        Ferramenta(
            id="FE_DNA_TERRITORIO",
            nome="DNA do Território™",
            nivel=Nivel.FERRAMENTA,
            pilar=Pilar.TERRITORIO,
            status=Status.PENDENTE_DE_FONTE,
            fonte=F_SPEC_KE,
            objetivo="Ferramenta de leitura territorial citada no Modo Mentoria.",
            observacoes=(
                "Nome preservado conforme declarado. Definição não documentada no sistema. "
                "Relação com o Zion Score™ precisa ser esclarecida: são a mesma leitura em "
                "profundidades diferentes ou instrumentos distintos?"
            ),
        ),
        Ferramenta(
            id="FE_LAUNCH_SYSTEM",
            nome="Launch System",
            nivel=Nivel.FERRAMENTA,
            pilar=Pilar.LANCAMENTO,
            status=Status.PENDENTE_DE_FONTE,
            fonte=F_SPEC_KE,
            objetivo="Ferramenta de lançamento citada na matriz Conhecimento → Decisão.",
            observacoes=(
                "Nome preservado. Definição não documentada. É o único instrumento do pilar "
                "Lançamento, que também é o pilar sem cobertura no framework da Pirâmide Invertida."
            ),
        ),
    ]


# ---------------------------------------------------------------------------
# Entregáveis
# ---------------------------------------------------------------------------

_ENTREGAVEIS = [
    ("EN_DIAGNOSTICO_TERRITORIAL", "Diagnóstico Territorial", Pilar.TERRITORIO,
     "Leitura do potencial do território", "FE_ZION_SCORE", "Desenvolver ou não?", "EN_ESTUDO_MERCADO"),
    ("EN_ESTUDO_MERCADO", "Estudo de Mercado", Pilar.MERCADO,
     "Demanda, concorrência e mercado emissor", "FE_IPM_Z", "Existe demanda?", "EN_CONCEITO_PRODUTO"),
    ("EN_CONCEITO_PRODUTO", "Conceito de Produto", Pilar.PRODUTO,
     "Definição do que será construído", None, "O que criar?", "EN_POSICIONAMENTO"),
    ("EN_POSICIONAMENTO", "Posicionamento", Pilar.PRODUTO,
     "Lugar que o produto ocupa no mercado", None, "Para quem e a que preço?", "EN_MODELO_NEGOCIO"),
    ("EN_MODELO_NEGOCIO", "Modelo de Negócio", Pilar.ESTRATEGIA,
     "Como o empreendimento gera e captura valor", None, "Como operar?", "EN_VIABILIDADE"),
    ("EN_VIABILIDADE", "Viabilidade", Pilar.INVESTIMENTO,
     "Demonstração de que os números fecham", "FE_MODELO_FINANCEIRO", "Os números fecham?", "EN_ESTRATEGIA_CAPITAL"),
    ("EN_ESTRATEGIA_CAPITAL", "Estratégia de Capital", Pilar.INVESTIMENTO,
     "Como o projeto será financiado", None, "Como financiar?", "EN_ROADMAP"),
    ("EN_ROADMAP", "Roadmap", Pilar.IMPLANTACAO,
     "Sequência e marcos da execução", None, "É executável?", "EN_PLANO_IMPLANTACAO"),
    ("EN_PLANO_IMPLANTACAO", "Plano de Implantação", Pilar.IMPLANTACAO,
     "Plano operacional de execução da obra e da operação", None, "Como implantar?", "EN_PLANO_LANCAMENTO"),
    ("EN_PLANO_LANCAMENTO", "Plano de Lançamento", Pilar.LANCAMENTO,
     "Plano de entrada no mercado", "FE_LAUNCH_SYSTEM", "Como vender?", "EN_DOSSIE_DEVELOPER"),
    ("EN_DOSSIE_DEVELOPER", "Dossiê do Developer", Pilar.TRANSVERSAL,
     "Consolidação de todos os entregáveis do projeto", None, "O projeto está completo?", None),
]


def _entregaveis():
    return [
        Entregavel(
            id=eid, nome=nome, nivel=Nivel.ENTREGAVEL, pilar=pilar, fonte=F_SPEC_KE,
            objetivo=objetivo, ferramenta_id=ferramenta,
            decisao_produzida=decisao, proximo_entregavel=proximo,
        )
        for eid, nome, pilar, objetivo, ferramenta, decisao, proximo in _ENTREGAVEIS
    ]


# ---------------------------------------------------------------------------
# Decisões, erros e perguntas
# ---------------------------------------------------------------------------

_DECISOES = [
    (1, "Desenvolver ou não?", Pilar.TERRITORIO, "FE_ZION_SCORE", "EN_DIAGNOSTICO_TERRITORIAL"),
    (2, "Qual mercado?", Pilar.MERCADO, "FE_IPM_Z", "EN_ESTUDO_MERCADO"),
    (3, "Qual público?", Pilar.MERCADO, "FE_IPM_Z", "EN_ESTUDO_MERCADO"),
    (4, "Qual produto?", Pilar.PRODUTO, None, "EN_CONCEITO_PRODUTO"),
    (5, "Quantas unidades?", Pilar.PRODUTO, None, "EN_CONCEITO_PRODUTO"),
    (6, "Qual modelo?", Pilar.ESTRATEGIA, None, "EN_MODELO_NEGOCIO"),
    (7, "Quanto investir?", Pilar.INVESTIMENTO, "FE_MODELO_FINANCEIRO", "EN_VIABILIDADE"),
    (8, "Como financiar?", Pilar.INVESTIMENTO, None, "EN_ESTRATEGIA_CAPITAL"),
    (9, "Como implantar?", Pilar.IMPLANTACAO, None, "EN_PLANO_IMPLANTACAO"),
    (10, "Como lançar?", Pilar.LANCAMENTO, "FE_LAUNCH_SYSTEM", "EN_PLANO_LANCAMENTO"),
]

_ERROS = [
    ("começar pela arquitetura", Pilar.PRODUTO,
     "Desenhar o empreendimento antes de saber o que o território e o mercado sustentam.",
     "Arquitetura é tangível e sedutora; território e demanda são abstratos.",
     "Produto caro que o mercado não paga.", "FE_ZION_SCORE"),
    ("construir antes de validar mercado", Pilar.MERCADO,
     "Iniciar obra sem estudo de demanda concluído.",
     "Pressa e excesso de confiança no próprio gosto.",
     "Ativo construído com ocupação estruturalmente baixa.", "FE_IPM_Z"),
    ("copiar concorrente", Pilar.PRODUTO,
     "Replicar o produto vizinho sem entender por que ele funciona.",
     "Parece caminho seguro e reduz esforço de concepção.",
     "Competição por preço em vez de diferenciação.", None),
    ("subestimar CAPEX", Pilar.INVESTIMENTO,
     "Orçar a obra abaixo do custo real de execução.",
     "Orçamento feito sem projeto executivo e sem contingência.",
     "Obra parada por falta de recurso.", "FE_MODELO_FINANCEIRO"),
    ("ignorar infraestrutura", Pilar.TERRITORIO,
     "Não considerar acesso, energia, água, saneamento e conectividade.",
     "O foco vai para a paisagem, não para a viabilidade de operar.",
     "Custo de implantação explode ou a operação não funciona.", "FE_ZION_SCORE"),
    ("superestimar ocupação", Pilar.MERCADO,
     "Projetar taxa de ocupação acima do que o mercado sustenta.",
     "Modelo financeiro construído para justificar a decisão já tomada.",
     "Receita projetada nunca se realiza.", "FE_MODELO_FINANCEIRO"),
    ("ignorar sazonalidade", Pilar.MERCADO,
     "Usar média anual sem considerar a distribuição da demanda no ano.",
     "A média esconde os meses de baixa.",
     "Caixa negativo na baixa temporada mesmo com ano fechando positivo.", "FE_MODELO_FINANCEIRO"),
    ("confundir diária com rentabilidade", Pilar.INVESTIMENTO,
     "Tratar ADR alta como sinônimo de negócio rentável.",
     "ADR é o número mais visível e mais fácil de comparar.",
     "Operação com diária alta e margem baixa.", "FE_MODELO_FINANCEIRO"),
    ("não prever capital de giro", Pilar.INVESTIMENTO,
     "Financiar o CAPEX e esquecer o custo de operar até o ponto de equilíbrio.",
     "O plano termina na inauguração.",
     "Empreendimento pronto e sem caixa para operar.", "FE_MODELO_FINANCEIRO"),
    ("lançar tarde", Pilar.LANCAMENTO,
     "Começar a vender depois que a obra terminou.",
     "Lançamento é tratado como consequência da obra, não como frente própria.",
     "Abertura sem demanda e queima de caixa nos primeiros meses.", "FE_LAUNCH_SYSTEM"),
    ("não criar demanda antes da abertura", Pilar.LANCAMENTO,
     "Inaugurar sem lista de espera, sem audiência e sem reservas.",
     "Confiança de que o produto vende sozinho.",
     "Ocupação inicial muito abaixo do projetado.", "FE_LAUNCH_SYSTEM"),
]


def _decisoes():
    itens = []
    for i, (numero, pergunta, pilar, ferramenta, entregavel) in enumerate(_DECISOES):
        anterior = f"D{_DECISOES[i-1][0]:02d}" if i > 0 else None
        seguinte = f"D{_DECISOES[i+1][0]:02d}" if i < len(_DECISOES) - 1 else None
        itens.append(Decisao(
            id=f"D{numero:02d}", numero=numero, pergunta=pergunta, pilar=pilar,
            ferramenta_id=ferramenta, entregavel_id=entregavel,
            decisao_anterior=anterior, decisao_seguinte=seguinte, fonte=F_SPEC_KE,
        ))
    return itens


def _erros():
    return [
        Erro(
            id=f"ER{i:02d}", nome=nome, pilar=pilar, o_que_e=o_que_e,
            por_que_acontece=por_que, consequencia=consequencia,
            ferramenta_que_combate=ferramenta, fonte=F_SPEC_KE,
        )
        for i, (nome, pilar, o_que_e, por_que, consequencia, ferramenta) in enumerate(_ERROS, 1)
    ]


def _perguntas():
    base = [
        ("P_TERRITORIO", "O que este território sustenta?", Pilar.TERRITORIO,
         ["O que este lugar possui?", "O que falta de infraestrutura?", "O que é único aqui?"], "D01"),
        ("P_MERCADO", "Existe demanda?", Pilar.MERCADO,
         ["De onde virá o hóspede?", "Por que ele viajaria?", "Quanto ele pagaria?",
          "O produto foi desenhado para esse público?"], "D02"),
        ("P_PRODUTO", "O que devemos criar?", Pilar.PRODUTO,
         ["Quantas unidades?", "Que experiência entregamos?", "O que nos diferencia?"], "D04"),
        ("P_ESTRATEGIA", "Como transformar isso em negócio?", Pilar.ESTRATEGIA,
         ["Qual o modelo de operação?", "Em que veículo o negócio mora?"], "D06"),
        ("P_INVESTIMENTO", "Os números fecham?", Pilar.INVESTIMENTO,
         ["Qual o CAPEX real?", "Qual o capital de giro até o equilíbrio?",
          "Qual o retorno e em quanto tempo?"], "D07"),
        ("P_IMPLANTACAO", "Como tirar do papel?", Pilar.IMPLANTACAO,
         ["Quem executa?", "Em que sequência?", "O que trava a obra?"], "D09"),
        ("P_LANCAMENTO", "Como colocar no mercado?", Pilar.LANCAMENTO,
         ["Como criamos demanda antes de abrir?", "Qual o canal?", "Qual a primeira safra de hóspedes?"], "D10"),
    ]
    return [
        Pergunta(id=pid, pergunta=p, pilar=pilar, desdobramentos=desd,
                 decisao_associada=dec, fonte=F_SPEC_KE)
        for pid, p, pilar, desd, dec in base
    ]


# ---------------------------------------------------------------------------
# Números, divergências e lacunas
# ---------------------------------------------------------------------------

def _numeros():
    return [
        RegistroNumerico(
            id="N_ADR_URUBICI", indicador="ADR", valor=1571.0, unidade="BRL",
            contexto="Operação Zion Bubble Urubici, citada como benchmark de calibração",
            fonte=F_REPO, status=Status.PENDENTE_VALIDACAO,
        ),
        RegistroNumerico(
            id="N_EBITDA_URUBICI", indicador="margem EBITDA", valor=43.46, unidade="%",
            contexto="Operação Zion Bubble Urubici, citada como benchmark de calibração",
            fonte=F_REPO, status=Status.PENDENTE_VALIDACAO,
        ),
    ]


def _divergencias():
    return [
        Divergencia(
            id="D_ORDEM_PRODUTO_INVESTIMENTO",
            tema="Ordem entre Produto e Investimento",
            descricao=(
                "Os dois mapas oficiais colocam a decisão de produto e a de viabilidade "
                "financeira em ordens opostas."
            ),
            versao_a=(
                "Pirâmide Invertida©: Etapa 2 é Viabilidade Econômico-Financeira e vem "
                "ANTES da Etapa 3, Produto e Master Plan."
            ),
            fonte_a=F_REPO,
            versao_b=(
                "Método Zion 360°: o pilar 03 Produto vem ANTES do pilar 05 Investimento."
            ),
            fonte_b=F_SPEC_KE,
            impacto=(
                "Muda o que o developer decide primeiro. Na Pirâmide, o número restringe o "
                "produto. No 360°, o produto define o número a ser testado. São teses "
                "diferentes sobre como se desenvolve, não diferença de redação."
            ),
        ),
        Divergencia(
            id="D_LANCAMENTO_AUSENTE",
            tema="Pilar Lançamento sem correspondência no framework",
            descricao="O Zion 360° tem sete pilares; a Pirâmide Invertida não cobre o sétimo.",
            versao_a=(
                "Pirâmide Invertida©: termina na Etapa 6, Acompanhamento e Consultoria de "
                "Implantação. Não há etapa de lançamento ou go-to-market."
            ),
            fonte_a=F_REPO,
            versao_b="Método Zion 360°: o pilar 07 é Lançamento — como colocar no mercado.",
            fonte_b=F_SPEC_KE,
            impacto=(
                "Dois dos onze erros documentados de developer são de lançamento — lançar "
                "tarde e não criar demanda antes da abertura. O framework implementado no "
                "sistema não tem etapa que os combata."
            ),
        ),
        Divergencia(
            id="D_NOME_INVESTIMENTO",
            tema="Colisão de nome entre Investimento e captação",
            descricao="O mesmo termo nomeia coisas diferentes nos dois mapas.",
            versao_a=(
                "Pirâmide Invertida©: Etapa 5 é Modelagem e Apresentação para Investidores "
                "— captação de capital. A viabilidade é a Etapa 2."
            ),
            fonte_a=F_REPO,
            versao_b=(
                "Método Zion 360°: o pilar 05 Investimento pergunta 'os números fecham?' — "
                "ou seja, é viabilidade, não captação."
            ),
            fonte_b=F_SPEC_KE,
            impacto=(
                "Aluno, mentor e agente de IA podem usar a mesma palavra para viabilidade e "
                "para captação. É o tipo de ambiguidade que corrompe material didático e "
                "conversa comercial ao mesmo tempo."
            ),
        ),
    ]


def _lacunas():
    return [
        Lacuna(
            id="L_LIVROS", item="Os 7 livros da Zion", tipo="livro",
            por_que_importa="São a fonte primária declarada do método.",
            o_que_falta="Nenhum dos sete está carregado no sistema.",
            bloqueia=["Banco de conceitos completo", "Extração de ferramentas", "Modo Aula com fonte"],
        ),
        Lacuna(
            id="L_LIVRO_MAE", item="Transforme Seu Terreno em um Destino Turístico", tipo="livro",
            por_que_importa="É o livro-mãe, base de toda a narrativa e do funil de entrada.",
            o_que_falta="Conteúdo não carregado.",
            bloqueia=["Narrativa oficial", "Alinhamento entre livro e mentoria"],
        ),
        Lacuna(
            id="L_IPM_Z", item="IPM-Z™", tipo="ferramenta",
            por_que_importa="É a ferramenta do pilar Mercado na matriz Conhecimento → Decisão.",
            o_que_falta="Definição, entradas, processo, saída e critérios de interpretação.",
            bloqueia=["Pilar Mercado operacional", "Decisões 02 e 03", "Estudo de Mercado como entregável"],
        ),
        Lacuna(
            id="L_DNA_TERRITORIO", item="DNA do Território™", tipo="ferramenta",
            por_que_importa="Citada no Modo Mentoria como ferramenta da Semana 1.",
            o_que_falta="Definição e relação com o Zion Score™.",
            bloqueia=["Estrutura da mentoria", "Clareza sobre duplicidade de ferramentas"],
        ),
        Lacuna(
            id="L_LAUNCH_SYSTEM", item="Launch System", tipo="ferramenta",
            por_que_importa="É a única ferramenta do pilar Lançamento.",
            o_que_falta="Definição completa.",
            bloqueia=["Pilar Lançamento", "Decisão 10", "Plano de Lançamento"],
        ),
        Lacuna(
            id="L_CASES", item="Cases com resultado documentado", tipo="case",
            por_que_importa="Prova é o que sustenta narrativa comercial e material de captação.",
            o_que_falta=(
                "Nenhum case com contexto, decisão, execução e resultado documentado foi "
                "carregado. Sem isso, nenhuma prova pode ser afirmada."
            ),
            bloqueia=["Modo Narrativa", "Modo Comercial", "Material de captação com prova"],
        ),
        Lacuna(
            id="L_NUMEROS_URUBICI", item="Período e origem dos números de Urubici", tipo="número",
            por_que_importa=(
                "ADR de R$ 1.571 e margem EBITDA de 43,46% circulam como benchmark e "
                "calibram estimativas do sistema."
            ),
            o_que_falta="Período de apuração e demonstrativo de origem.",
            bloqueia=["Citação dos números em material externo", "Calibração auditável de estimativas"],
        ),
        Lacuna(
            id="L_PRECOS", item="Preço e fee por pilar comercial", tipo="documento",
            por_que_importa="Sem faixa de preço, o sistema não estima receita por frente.",
            o_que_falta="Faixa de ticket dos seis pilares comerciais.",
            bloqueia=["Projeção de receita por pilar", "Regra de oferta com valor"],
        ),
    ]


def construir_base() -> KnowledgeBase:
    """Monta a base de conhecimento com tudo que é verificável hoje."""
    kb = KnowledgeBase()
    kb.registrar_todos(_conceitos())
    kb.registrar_todos(_ferramentas())
    kb.registrar_todos(_entregaveis())
    kb.registrar_todos(_perguntas())
    kb.registrar_todos(_decisoes())
    kb.registrar_todos(_erros())
    kb.registrar_todos(_numeros())
    kb.registrar_todos(_divergencias())
    kb.registrar_todos(_lacunas())
    return kb

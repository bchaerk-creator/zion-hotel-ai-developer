# Arquitetura Técnica — Zion Hotel AI Developer

## Visão Geral da Arquitetura

O Zion Hotel AI Developer segue uma arquitetura de **agentes especializados orquestrados**, onde cada etapa do método da Pirâmide Invertida© é implementada por um agente dedicado, coordenado por um orquestrador central.

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI / Interface                            │
│                     (src/main.py)                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    ZionOrchestrator                           │
│              (src/agents/orchestrator.py)                     │
│                                                              │
│  • Gerencia estado do projeto                                │
│  • Coordena execução sequencial                              │
│  • Acumula contexto entre etapas                             │
└──┬───┬───┬───┬───┬───┬───┬──────────────────────────────────┘
   │   │   │   │   │   │   │
   ▼   ▼   ▼   ▼   ▼   ▼   ▼
┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐
│ E0 ││ E1 ││ E2 ││ E3 ││ E4 ││ E5 ││ E6 │  Agentes Especializados
└──┬─┘└──┬─┘└──┬─┘└──┬─┘└──┬─┘└──┬─┘└──┬─┘
   │     │     │     │     │     │     │
   └─────┴─────┴─────┴─────┴─────┴─────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   Camada de Suporte                           │
│                                                              │
│  ┌──────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │  LLM Client  │  │ Report Generator │  │    Logger      │  │
│  │  (OpenAI)    │  │   (Jinja2/MD)    │  │   (Rich)       │  │
│  └──────────────┘  └──────────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Fluxo de Dados

O fluxo segue a sequência natural do método Zion. Cada agente recebe os dados de entrada do projeto mais os resultados acumulados das etapas anteriores como contexto.

```
Input (JSON) → Etapa 0 → Etapa 1 → Etapa 2 → Etapa 3 → Etapa 4 → Etapa 5 → Output
                 │          │          │          │          │          │
                 ▼          ▼          ▼          ▼          ▼          ▼
              Score      Mercado    Financeiro  Produto   Negócio   Investidor
              Report     Report     Report      Report    Report    Report
```

## Componentes Principais

### 1. Orquestrador (`ZionOrchestrator`)

Responsável por coordenar a execução dos agentes, gerenciar o estado do projeto e acumular contexto entre etapas. Oferece dois modos de operação: execução de etapa individual e pipeline completo.

### 2. Agentes Especializados (`BaseAgent` → agentes concretos)

Cada agente herda de `BaseAgent` e implementa a lógica específica de sua etapa. Os agentes possuem system prompts especializados que definem seu comportamento e formato de saída.

### 3. Cliente LLM (`ZionLLMClient`)

Abstração sobre a API OpenAI que oferece três modos de chamada: `chat` (padrão), `think` (raciocínio estendido) e `fast` (rápido e econômico). Também suporta output estruturado via JSON Schema.

### 4. Gerador de Relatórios (`ReportGenerator`)

Produz relatórios formatados em Markdown seguindo a identidade visual e padrão editorial da Zion. Suporta templates Jinja2 e geração direta.

## Modelos de Dados

Todos os modelos são definidos com Pydantic v2, garantindo validação rigorosa e serialização consistente. A hierarquia reflete a estrutura do método Zion.

## Estratégia de LLM

| Tipo de Tarefa | Modelo | Justificativa |
|----------------|--------|---------------|
| Diagnóstico rápido | gpt-5-nano | Volume, custo baixo |
| Análises gerais | gpt-5-mini | Custo-benefício |
| Raciocínio complexo | gpt-5 | Qualidade de análise |
| Modelagem financeira | gpt-5 (thinking) | Precisão numérica |

## Módulo Transversal: Land Bank

O Land Bank (módulo 7) não segue o padrão dos agentes de etapa, porque o problema que ele
resolve é aritmético antes de ser interpretativo. A arquitetura tem duas camadas:

```
┌──────────────────────────────────────────────────────────────┐
│  LandBankAgent (src/agents/land_bank_agent.py)               │
│                                                              │
│  analisar()  → determinístico, roda sem chave de API         │
│  execute()   → determinístico + camada estratégica com LLM   │
└───────────────┬──────────────────────────────────────────────┘
                │
      ┌─────────┴──────────┐
      ▼                    ▼
┌──────────────────┐  ┌─────────────────────────┐
│  carbon_engine   │  │  land_bank_report       │
│                  │  │                         │
│ elegibilidade    │  │ relatório Markdown      │
│ clusterização    │  │ no padrão Zion          │
│ curva/buffer     │  └─────────────────────────┘
│ fluxo de caixa   │
│ preço equilíbrio │
│ pré-venda mínima │
│ priorização      │
└──────────────────┘
```

A separação é deliberada: números que vão para mesa de negociação e comitê de investimento
precisam ser reproduzíveis e auditáveis. A engine é determinística e coberta por testes; o LLM
recebe o resultado pronto e trabalha apenas a camada que não é cálculo — originação, negociação,
estrutura jurídica e sequenciamento. O prompt instrui explicitamente a não recalcular nem
inventar números.

Consequência prática: `BaseAgent` instancia o cliente LLM sob demanda, para que agentes com
camada determinística rodem sem credencial configurada.

## Extensibilidade

O sistema é projetado para ser estendido com novos agentes, módulos de dados externos (APIs de mercado hoteleiro, dados de turismo) e integrações com ferramentas de apresentação.

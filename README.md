# Zion Hotel AI Developer

**Agente de Inteligência Artificial para Desenvolvimento Hoteleiro**

> Plataforma de IA que implementa o método da Pirâmide Invertida© da Zion Hotel Group International, automatizando o ciclo completo de desenvolvimento hoteleiro — do diagnóstico preliminar à captação de investimento.

---

## Visão Geral

O **Zion Hotel AI Developer** é um agente de IA especializado em desenvolvimento hoteleiro que opera como copiloto inteligente para estruturação de projetos turísticos e hoteleiros. Baseado na metodologia proprietária da Zion Hotel Group International, o agente cobre todas as etapas do processo de desenvolvimento:

| Etapa | Módulo | Função |
|-------|--------|--------|
| 0 | Zion Score | Diagnóstico preliminar automatizado com nota de 0 a 10 |
| 1 | Market Intelligence | Estudo de viabilidade mercadológica completo |
| 2 | Financial Engine | Modelagem econômico-financeira com cenários |
| 3 | Product Designer | Definição de produto, posicionamento e master plan conceitual |
| 4 | Business Structuring | Estruturação societária e jurídica do negócio |
| 5 | Investor Readiness | Modelagem e apresentação para investidores |
| 6 | Implementation Gov | Acompanhamento e consultoria de implantação |

E os módulos transversais, que rodam em paralelo a todas as etapas:

| Módulo | Nome | Função |
|-------|--------|--------|
| 7 | Land Bank | Agregação territorial e originação de crédito de carbono |
| 8 | Knowledge Engine | Fonte de verdade do Método Zion 360°, com proveniência e auditoria |
| 9 | CRM & Lead Intelligence | Qualificação, roteamento comercial e inteligência de funil |

---

## Arquitetura

```
zion-hotel-ai-developer/
├── src/
│   ├── agents/           # Agentes especializados por etapa
│   ├── modules/          # Módulos de processamento (engine de carbono, relatórios)
│   ├── models/           # Modelos de dados e schemas
│   ├── utils/            # Utilitários compartilhados
│   ├── prompts/          # System prompts especializados por etapa
│   ├── config/           # Configurações do sistema
│   └── main.py           # Orquestrador principal
├── tests/                # Testes unitários e de integração
├── docs/                 # Documentação técnica e de uso
├── data/
│   └── templates/        # Templates de relatórios e apresentações
├── scripts/              # Scripts auxiliares
├── requirements.txt      # Dependências Python
├── .env.example          # Variáveis de ambiente (template)
└── README.md
```

---

## Funcionalidades Principais

### Etapa 0 — Zion Score™
- Análise automatizada de vocação do destino
- Estimativa de ADR de referência
- CAPEX orientativo preliminar
- Mapeamento de mercado emissor
- Análise de concorrência regional
- Pontuação consolidada de 0 a 10

### Etapa 1 — Viabilidade Mercadológica
- Perfil turístico e fluxo de visitantes
- Análise de sazonalidade
- Infraestrutura e vetores de crescimento
- Mapeamento da oferta concorrente
- Benchmark nacional e internacional
- Posicionamento estratégico

### Etapa 2 — Viabilidade Econômico-Financeira
- Estimativa de CAPEX detalhada
- Projeção de receitas e despesas operacionais
- Cálculo de EBITDA projetado
- Fluxo de caixa para 10 anos
- TIR, VPL, Payback e Break-even
- Análise de sensibilidade com cenários (conservador, realista, otimista)

### Etapa 3 — Produto e Posicionamento
- Definição conceitual do empreendimento
- Posicionamento estratégico de mercado
- Diretriz de público-alvo
- Estratégia de marca e narrativa territorial
- Arquitetura de bandeira (Zion Collection, By Zion, marca própria)
- Diretrizes para master plan

### Etapa 4 — Estruturação do Negócio
- Orientação para definição de SPE
- Modelo societário recomendado
- Estratégia de entrada de investidores
- Checklist de coordenação jurídica
- Preparação para acesso estruturado a capital

### Etapa 5 — Apresentação para Investidores
- Estruturação da tese de investimento
- Geração de teaser executivo
- Information memorandum
- Pitch deck institucional
- Adequação por perfil de investidor

### Etapa 6 — Governança de Implantação
- Acompanhamento de milestones
- Validação de aderência à tese original
- Coordenação com stakeholders
- Relatórios de governança periódicos

### Módulo 7 — Land Bank™ (Agregação Territorial e Carbono)
- Triagem de elegibilidade por talhão (rota metodológica, bloqueios, passivo legal)
- Clusterização geográfica de glebas em projetos agrupados
- Estimativa de créditos líquidos por bioma e rota, com curva de sequestro e buffer
- Fluxo de caixa do projeto de carbono, com VPL, TIR, payback e custo por crédito
- Preço de equilíbrio e pré-venda mínima por cluster
- Carbon Readiness Score por gleba e fila priorizada de agregação
- Instrumento jurídico recomendado por gleba

A camada numérica é determinística e roda sem chave de API. O LLM entra apenas na
camada estratégica. Documentação completa em [`docs/LAND_BANK.md`](docs/LAND_BANK.md).

### Módulo 8 — Zion Knowledge Engine™
- Hierarquia de sete níveis, de princípio a case, com proveniência declarada por item
- Distinção entre conhecimento Zion, conhecimento externo e inferência estratégica
- Grafo conceito → pilar → ferramenta → entregável → decisão → próximo pilar
- Matriz Conhecimento → Decisão por pilar do Método Zion 360°
- Auditoria do método: divergências entre fontes, ferramentas sem definição, números sem
  período, pilares sem instrumentação
- Modos professor, aula, exercício e avaliação

Documentação em [`docs/KNOWLEDGE_ENGINE.md`](docs/KNOWLEDGE_ENGINE.md).

### Módulo 9 — Zion CRM & Lead Intelligence™
- Zion Lead Score™ com oito dimensões, e confiança reportada separadamente do score
- Temperatura por situação comercial real, não por engajamento
- Roteamento de oferta com a regra de não empurrar venda
- Higiene da base: duplicidade, follow-up vencido, lead sem próxima ação, perda sem motivo
- Análise de funil com diagnóstico de gargalo por posição
- Lista de reativação e briefing de reunião

Documentação em [`docs/CRM.md`](docs/CRM.md).

---

## Pilares Comerciais

A Zion gera receita por seis frentes, definidas em [`src/config/pilares.py`](src/config/pilares.py)
e injetadas no system prompt de todos os agentes:

| Pilar | Oferta |
|-------|--------|
| Produto | Venda de bubbles e cabanas |
| Desenvolvimento | Escopo inteiro do desenvolvimento hoteleiro como prestação de serviço |
| Capital | Estruturação para apresentar a bancos, crédito e investidores |
| Conhecimento | Mentoria para quem quer desenvolver o próprio projeto |
| Parceria | Zion Joint Venture — entra com as bubbles e entra no equity |
| Sustentabilidade | Selos ambientais, crédito de carbono e projetos fotovoltaicos |

Leitura estratégica completa em [`docs/PILARES_COMERCIAIS.md`](docs/PILARES_COMERCIAIS.md).

---

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/SEU_USUARIO/zion-hotel-ai-developer.git
cd zion-hotel-ai-developer

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas credenciais
```

---

## Uso

```bash
# Executar o agente principal
python -m src.main

# Executar diagnóstico preliminar (Zion Score)
python -m src.main --stage 0 --input data/projeto_exemplo.json

# Executar estudo de viabilidade completo
python -m src.main --stage 1 --input data/projeto_exemplo.json

# Executar modelagem financeira
python -m src.main --stage 2 --input data/projeto_exemplo.json

# Consultar os pilares comerciais
python -m src.main pilares
python -m src.main pilares --pilar PARCERIA

# Analisar o Land Bank (roda sem chave de API)
python -m src.main land-bank --input data/exemplo_land_bank.json

# Auditar o método (Knowledge Engine)
python -m src.main knowledge

# Analisar a base comercial (CRM)
python -m src.main crm -i data/exemplo_base_comercial.json

# Land Bank com relatório em Markdown, exportação JSON e camada estratégica de IA
python -m src.main land-bank -i data/exemplo_land_bank.json \
    -o output/land_bank.md --json output/land_bank.json --ia
```

---

## Configuração

Copie o arquivo `.env.example` para `.env` e configure:

```env
OPENAI_API_KEY=sua_chave_aqui
OPENAI_API_BASE=https://api.openai.com/v1
ZION_MODEL=gpt-5-mini
ZION_THINKING_MODEL=gpt-5
```

---

## Tecnologias

- **Python 3.11+** — Linguagem principal
- **OpenAI SDK** — Integração com modelos de linguagem
- **Pydantic** — Validação de dados e schemas
- **Rich** — Interface de terminal rica
- **Jinja2** — Templates de relatórios
- **Pandas** — Processamento de dados financeiros
- **NumPy** — Cálculos numéricos

---

## Licença

Propriedade intelectual da **Zion Hotel Group International**.
Uso restrito sob autorização expressa.

---

## Contato

**Bruno Chaerk** — CEO & Founder
Zion Hotel Group International
Florianópolis (SC) · Barcelona (ESP)

---

> *"Transformamos seu terreno em um destino turístico. Estruturamos seu projeto para captar investimentos."*
